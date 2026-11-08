global.window = undefined;
require('./sd_lib.js');
const SD = global.SD;
const N = +process.argv[2], POLICY = process.argv[3] || 'random';
let seed = 12345; function rnd(){ seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; }
function fresh(){ const Q = {}; SD.init(Q); SD.refresh(Q); return Q; }
function ev(expr, Q){ return (new Function('Q', 'return (' + expr + ');'))(Q); }
function run(code, Q){
  if (!code) return;
  const th = { achieve(){}, game:{scenes:{}}, state:{qualities:Q,currentHands:{main:[]},visits:{},lastPlayedCard:{id:'x'}}, _compileChoices(){ return [{title:'Continue...'}]; } };
  if (code.startsWith('JS:')) { (new Function('Q','window','document','dendryUI', code.slice(3))).call(th, Q, undefined, undefined, {dendryEngine:{state:{qualities:Q}}}); }
  else { (new Function('Q', code.slice(4)))(Q); }
}
function clone(Q){ return JSON.parse(JSON.stringify(Q, (k,v)=> (v===undefined? null: v))); }
function U(Q){ SD.refresh(Q); return 1.6*Q.dem_two_party + 0.45*Q.democracy_score - 0.35*Q.maga_strength - 0.25*Q.dissent_percent + 0.004*Q.civic_strength - 0.2*Q.farleft_strength - 0.2*Q.farright_strength + 0.8*Q.dem_enthusiasm; }
function avail(opts, Q){ return opts.filter(o => !o.choose || ev(o.choose, Q)); }
function pick(Q, scene, opts, how){
  const a = avail(opts, Q); if (!a.length) return null;
  if (how === 'random' || how === 'idle') return a[Math.floor(rnd()*a.length)];
  let best = null, bu = -1e9;
  for (const o of a) { const c = clone(Q); try { run(scene.code, c); run(o.code, c); } catch(e){ continue; } const u = U(c) + rnd()*0.5; if (u > bu) { bu = u; best = o; } }
  return best || a[0];
}
const stats = { byYear:{}, n:0, collapse:0, ending:{}, trifecta:0, demPres:{}, demWinsPres:[0,0,0], dsum:0, nominee:{maga:0,mainstream:0}, loops:0, elections:[], maga_sum:0, house_wins:0, errors:0, timeLost:[] };
function play(how){
  const Q = fresh(); const visits = {}; let steps = 0; const seen = {};
  const presWins = [];
  while (!Q.game_over && steps++ < 4000) {
    SD.refresh(Q);
    if (Q.month_actions >= 1) {
      Q.just_inaugurated = 0; Q.just_seated = 0;
      SD.advanceMonth(Q);
      if (Q.inauguration_due) { SD.inaugurate(Q); Q.just_inaugurated = 1; } else if (Q.transition_due) { SD.seatCongress(Q); Q.just_seated = 1; }
      SD.refresh(Q);
    }
    if (!Q.game_lost && !Q.game_over && !Q.dem_president && Q.president == Q.maga_leader && Q.institutions <= 12 && Q.pro_democracy <= 40) Q.game_lost = 1;
    const evs = SCENES.filter(s => s.kind === 'event' && (!s.maxv || (visits[s.id]||0) < s.maxv) && ev(s.view, Q)).sort((a,b) => b.prio - a.prio);
    if (evs.length) {
      const e = evs[0]; visits[e.id] = (visits[e.id]||0) + 1;
      const key = e.id + '@' + Q.time; seen[key] = (seen[key]||0) + 1;
      if (seen[key] > 3) { stats.loops++; console.log('LOOP', e.id, Q.year, Q.month); Q.game_over = 1; break; }
      run(e.code, Q);
      if (e.id === 'election_presidential') presWins.push(Q.el_pres_winner);
      if (e.id === 'election_presidential' || e.id === 'election_midterm') { const k = Q.year; (stats.byYear[k] = stats.byYear[k] || {d:0,r:0,n:0,h:0,s:0,ev:0}); const b = stats.byYear[k]; b.d += Q.el_dem_votes; b.r += Q.el_gop_votes; b.h += Q.el_house; b.s += Q.el_senate; b.ev += (Q.el_dem_ev||0); b.n++; }
      if (e.id === 'collapse' || e.id === 'ending') { Q.game_over = 1; break; }
      const o = pick(Q, {code:''}, e.opts, how); if (o) run(o.code, Q);
      continue;
    }
    // advisor (free action)
    if (how === 'idle') { Q.month_actions += 1; continue; }
    if (Q.advisor_action_timer <= 0) {
      const adv = SCENES.filter(s => s.kind === 'advisor' && ev(s.view, Q));
      if (adv.length) { const s = adv[Math.floor(rnd()*adv.length)]; const o = pick(Q, {code:''}, s.opts, how); if (o) { run(o.code, Q); } continue; }
    }
    // draw a hand of up to 4 cards
    let cards = SCENES.filter(s => s.kind === 'card' && ev(s.view, Q));
    for (let i = cards.length - 1; i > 0; i--) { const j = Math.floor(rnd()*(i+1)); [cards[i], cards[j]] = [cards[j], cards[i]]; }
    cards = cards.slice(0, 4);
    let bestC = null, bestO = null, bu = -1e9;
    for (const c of cards) { const o = pick(Q, c, c.opts, how); if (!o) continue; const cc = clone(Q); run(c.code, cc); run(o.code, cc); const u = (how === 'random') ? rnd() : U(cc); if (u > bu) { bu = u; bestC = c; bestO = o; } }
    if (bestC) { run(bestC.code, Q); run(bestO.code, Q); } else { Q.month_actions += 1; }
  }
  // classify
  const d = Q.democracy_score; let id;
  if (Q.game_lost) id = 'collapse'; else if (d >= 75 && Q.maga_strength < 45) id = 'resilient'; else if (d >= 55) id = 'fragile'; else id = 'authoritarian_drift';
  stats.n++; stats.ending[id] = (stats.ending[id]||0) + 1; if (id === 'collapse') { stats.collapse++; stats.timeLost.push(Q.year); }
  if (Q.dem_president && Q.dem_house && Q.dem_senate) stats.trifecta++;
  presWins.forEach((w,i) => { if (w === 'D') stats.demWinsPres[i]++; });
  stats.dsum += d; stats.maga_sum += Q.maga_strength;
  if (Q.gop_nominee_type) stats.nominee[Q.gop_nominee_type] = (stats.nominee[Q.gop_nominee_type]||0) + 1;
  return Q;
}
for (let g = 0; g < N; g++) { try { play(POLICY); } catch (e) { stats.errors++; if (stats.errors < 4) console.log('ERR', e.stack.split('\n').slice(0,3).join(' | ')); } }
console.log(POLICY, 'games', stats.n, 'errors', stats.errors, 'loops', stats.loops);
console.log('endings', JSON.stringify(stats.ending), 'avg democracy score', (stats.dsum/stats.n).toFixed(1), 'avg maga', (stats.maga_sum/stats.n).toFixed(1));
console.log('Dem presidential wins (2016,2020,2024) out of', stats.n, ':', JSON.stringify(stats.demWinsPres), '| final trifecta', stats.trifecta, '| last GOP nominee type (maga/mainstream):', JSON.stringify(stats.nominee));
console.log('collapse years', JSON.stringify(stats.timeLost.reduce((a,y)=>{a[y]=(a[y]||0)+1;return a;},{})));

for (const y in stats.byYear) { const b = stats.byYear[y]; console.log(y, 'D', (b.d/b.n).toFixed(1), 'R', (b.r/b.n).toFixed(1), 'House', (b.h/b.n).toFixed(0), 'Sen', (b.s/b.n).toFixed(0), 'EV', (b.ev/b.n).toFixed(0)); }
