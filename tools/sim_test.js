global.window = undefined;
require('./sd_lib.js');
const SD = global.SD;
const Q = {};
SD.init(Q);
SD.refresh(Q);
console.log('INIT 2014: D',Q.dem_votes,'R',Q.gop_votes,'L',Q.left_votes,'FR',Q.farright_votes,'turnout',Q.turnout,'EV',Q.dem_ev_proj,'house',Q.house_proj,'senate',Q.senate_proj);
const passive = process.argv[2] !== 'active';
function covid(){ Q.economic_growth=-8; Q.unemployed=13; Q.inflation=0.5; Q.budget-=3; }
function inflation(){ Q.inflation=7.5; Q.economic_growth=1; }
for (let i=0;i<156;i++){
  SD.refresh(Q);
  if (!passive) { // crude "good play": a few boosts
    Q.trump_urgency = Math.min(8, (Q.trump_urgency||0)+0.1);
    Q.left_relation = Math.min(70, Q.left_relation+0.2);
    Q.dem_enthusiasm = Math.min(7, Q.dem_enthusiasm+0.15);
    Q.working_dem += 0.05; Q.rural_dem += 0.02; Q.pro_democracy += 0.04;
  }
  if (Q.year==2020&&Q.month==3) covid();
  if (Q.year==2021&&Q.month==6) inflation();
  if (Q.year==2008) {}
  SD.advanceMonth(Q);
  if (Q.inauguration_due){ SD.inaugurate(Q); }
  if (Q.transition_due && !Q.inauguration_due){ SD.seatCongress(Q); }
  if (Q.month==1 && Q.year%2==1) SD.seatCongress(Q);
  // nominee names stub
  if (Q.month==10 && Q.year%4==0) { Q.dem_nominee_name='Dem'; Q.gop_nominee_name = Q.maga_strength>=30?'Trump':'Mainstream'; }
  if (Q.month==12 && Q.last_election && Q.last_election.year==Q.year) {
    const E=Q.last_election; 
    console.log(E.year, E.midterm?'MID':'PRES', 'D',E.dem_votes,'R',E.gop_votes,'L',E.left_votes,'FR',E.farright_votes,'TO',E.turnout, E.midterm?'':('EV '+E.dem_ev+'-'+E.gop_ev+' '+E.winner), 'House',E.house,'Sen',E.senate,
     '| maga',Q.maga_strength.toFixed(0),'inst',Q.institutions.toFixed(0),'prodem',Q.pro_democracy.toFixed(0),'sub',Q.subversion_progress.toFixed(1),'unemp',Q.unemployed.toFixed(1),'infl',Q.inflation.toFixed(1),'polar',Q.polarization.toFixed(0),'fl',Q.farleft_strength.toFixed(0),'fr',Q.farright_strength.toFixed(0));
  }
}
console.log('END', Q.year, Q.month, 'pres',Q.president,Q.president_party);
