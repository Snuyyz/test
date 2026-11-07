// Headless bot playtest. Usage: node tools/playtest.js [runs] [policy]
const path = require('path');
const engine = require('../node_modules/dendrynexus/lib/engine.js');
const fs = require('fs');
const gameData = fs.readFileSync(path.join(__dirname, '../out/game.json'), 'utf8');
const RUNS = parseInt(process.argv[2] || '20', 10);
const POLICY = process.argv[3] || 'random';

function makeUI(log) {
  const ui = new engine.UserInterface();
  ui.displayContent = function(p) { log.text = (log.text || '') + JSON.stringify(p).slice(0, 0); };
  ui.displayChoices = function() {};
  ui.displayGameOver = function() { log.over = true; };
  return ui;
}

function runOnce(seed) {
  const log = {};
  const ui = makeUI(log);
  let game; engine.convertJSONToGame(gameData, function(err, g) { if (err) throw err; game = g; });
  const eng = new engine.DendryEngine(ui, game);
  eng.beginGame([seed, seed + 1, seed + 2, seed + 3, seed + 4]);
  let rng = seed * 9301 + 49297;
  const rand = () => (rng = (rng * 9301 + 49297) % 233280) / 233280;
  let steps = 0, visited = {}; const elec = {};
  let lastQ;
  while (steps++ < 6000) {
    const Q = eng.state.qualities;
    const scene = eng.state.sceneId;
    visited[scene] = (visited[scene] || 0) + 1;
    { const m = /^election_(\d+)/.exec(scene); if (m && !elec[m[1]]) elec[m[1]] = {pop: Math.round(Q.dem_pop*10)/10, wh: Q.white_house, h: Q.house_d, s: Q.senate_d, stab: Math.round(Q.stability)}; }
    if (/^game_over\.ending/.test(scene)) { return {steps, scene, over: true, Q: snapshot(Q), visited, elec}; }
    const choices = eng.getCurrentChoices();
    if (!choices || choices.length === 0) break;
    const ok = choices.map((c, i) => ({c, i})).filter(x => x.c.canChoose);
    if (ok.length === 0) { return {err: 'no choosable at ' + scene, steps, Q: snapshot(Q)}; }
    let pick;
    if (POLICY === 'greedy') {
      // 1-ply lookahead: try each option, score the resulting state, restore
      const saved = JSON.stringify(eng.state);
      let best = null, bestScore = -1e9;
      const tried = ok.slice();
      for (const x of tried) {
        try {
          eng.choose(x.i);
          const q = eng.state.qualities;
          let sc = q.stability*3 + q.pop_mod*8 + q.enthusiasm*0.3 + q.unity*0.3 + q.capital*0.6 + q.funds*0.4 - q.maga*0.5 - q.far_right*0.5 - q.far_left*0.4 - (q.prog_dissent+q.mod_dissent+q.estab_dissent+q.labor_dissent)*0.1 + q.media_trust*0.2;
          sc += (Math.random()*0.8);
          if (/Back/.test(x.c.title)) sc -= 3; if (/Let the quarter pass/.test(x.c.title)) sc -= 6;
          if (q.month_actions > (Q.month_actions||0) || q.time > (Q.time||0)) sc += 1; // prefer progress
          if (sc > bestScore) { bestScore = sc; best = x; }
        } catch (e) {}
        eng.setState(JSON.parse(saved));
      }
      pick = best || ok[0];
    } else if (POLICY === 'pass') {
      const passy = ok.filter(x => /Let the quarter pass/.test(x.c.title));
      const evt = ok.filter(x => !/Back|Party affairs|Government|Full status/.test(x.c.title));
      pick = (scene === 'main' && passy.length) ? passy[0] : (evt.length ? evt[Math.floor(rand()*evt.length)] : ok[0]);
    } else if (POLICY === 'random') {
      pick = ok[Math.floor(rand() * ok.length)];
    } else {
      // prefer non-back, non-pass options; deterministic-ish
      const nonBack = ok.filter(x => !/Back|Let the quarter pass/.test(x.c.title));
      const pool = nonBack.length ? nonBack : ok;
      pick = pool[Math.floor(rand() * pool.length)];
    }
    try { eng.choose(pick.i); } catch (e) { return {err: 'exception at ' + scene + ': ' + e.message, steps, Q: snapshot(Q)}; }
    if (log.over || eng.isGameOver()) break;
    // detect NaN
    const Q2 = eng.state.qualities;
    for (const k of Object.keys(Q2)) {
      const v = Q2[k];
      if (typeof v === 'number' && isNaN(v)) return {err: 'NaN in ' + k + ' after ' + scene, steps, Q: snapshot(Q2)};
    }
    lastQ = Q2;
  }
  return {steps, scene: eng.state.sceneId, over: !!log.over, Q: snapshot(eng.state.qualities), visited};
}
function snapshot(Q) {
  const keys = ['year','month','stability','enthusiasm','unity','maga','far_right','far_left','house_d','senate_d','white_house','president','nominee','dem_pop','game_over_flag','collapse_flag'];
  const o = {}; keys.forEach(k => o[k] = (typeof Q[k] === 'number') ? Math.round(Q[k]*10)/10 : Q[k]); return o;
}
let errs = 0; const endings = {}; const agg = {stab: [], d26: 0, wins: {2016:0,2020:0,2024:0}, h26: [], s26: [], pop: {}}; let n = 0;
for (let s = 1; s <= RUNS; s++) {
  const r = runOnce(s * 17);
  if (r.err) { errs++; console.log('RUN', s, 'ERR', r.err, JSON.stringify(r.Q)); continue; }
  const key = r.scene;
  endings[key] = (endings[key] || 0) + 1;
  if (r.elec) { n++; agg.stab.push(r.Q.stability); for (const y of [2016,2020,2024]) if (r.elec[y] && r.elec[y].wh === 'D') agg.wins[y]++; if (r.elec[2026]) { agg.h26.push(r.elec[2026].h); agg.s26.push(r.elec[2026].s); } for (const y in r.elec) { (agg.pop[y] = agg.pop[y] || []).push(r.elec[y].pop); } }
  if (s <= 3) console.log('RUN', s, 'steps', r.steps, 'scene', r.scene, JSON.stringify(r.Q));
}
const avg = a => a.length ? Math.round(a.reduce((x,y)=>x+y,0)/a.length*10)/10 : null;
const mm = a => a.length ? [Math.min(...a), Math.max(...a)] : null;
console.log('SUMMARY n=' + n, 'stability avg', avg(agg.stab), 'range', JSON.stringify(mm(agg.stab)), 'D wins', JSON.stringify(agg.wins), 'house26 avg', avg(agg.h26), 'senate26 avg', avg(agg.s26));
for (const y in agg.pop) console.log('  pop', y, 'avg', avg(agg.pop[y]), 'range', JSON.stringify(mm(agg.pop[y])));
console.log('errors:', errs, 'of', RUNS, 'endings:', JSON.stringify(endings));
