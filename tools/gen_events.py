#!/usr/bin/env python3
"""Generates event scenes for the US Democrats mod from a compact table.
Run:  python3 tools/gen_events.py   (from the project root)"""
import os, re, textwrap

OUT = os.path.join(os.path.dirname(__file__), '..', 'source', 'scenes', 'events')
os.makedirs(OUT, exist_ok=True)

def fx(s):
    return s.strip().rstrip(';') if s else ''

def emit(ev):
    lines = []
    lines.append(f"title: {ev['title']}")
    if ev.get('subtitle'): lines.append(f"subtitle: {ev['subtitle']}")
    lines.append("new-page: true")
    lines.append("tags: event")
    lines.append(f"view-if: {ev['when']}")
    lines.append("max-visits: 1")
    lines.append(f"priority: {ev.get('priority', 1)}")
    if ev.get('arrive'): lines.append(f"on-arrival: {fx(ev['arrive'])}")
    if ev.get('js'):
        lines.append("on-arrival: {!\n" + ev['js'].strip() + "\n!}")
    lines.append("")
    lines.append(f"= {ev['title']}")
    lines.append("")
    lines.append(ev['body'].strip())
    lines.append("")
    ch = ev.get('choices', [])
    for c in ch:
        lines.append(f"- @{c[0]}: {c[1]}")
    lines.append("")
    for c in ch:
        cid, label, sub, effects, text = c
        lines.append(f"@{cid}")
        if sub: lines.append(f"subtitle: {sub}")
        if effects: lines.append(f"on-arrival: {fx(effects)}")
        lines.append("")
        lines.append(text.strip())
        lines.append("")
    path = os.path.join(OUT, ev['id'] + '.scene.dry')
    open(path, 'w').write("\n".join(lines))

def election(eid, year, title, hist, typ, house_base, senate_base, intro, extra_js='', ec=51.5):
    """typ: 'pres' or 'mid'.  hist = historical D two-party share."""
    js = f"""
var delta = Q.pop_mod + (Q.enthusiasm-50)*0.02 + (Q.unity-55)*0.012 + (Q.stability-60)*0.006;
if (Q.far_left >= 40) delta -= 0.3;
if (Q.far_left >= 60) delta -= 0.4;
delta += (Q.nominee_mod || 0);
if (delta > 3.5) delta = 3.5;
if (delta < -3.5) delta = -3.5;
var dp = {hist} + delta;
Q.dem_pop = dp;
Q.dem_pop_str = dp.toFixed(1);
Q.rep_pop_str = (100-dp).toFixed(1);
Q.house_d = Math.max(150, Math.min(300, Math.round({house_base} + (dp-{hist})*8)));
Q.senate_d = Math.max(35, Math.min(65, Math.round({senate_base} + (dp-{hist})*0.8)));
Q.pop_mod = Q.pop_mod * 0.5;
Q.nominee_mod = 0;
Q.house_won = Q.house_d >= 218 ? 1 : 0;
Q.senate_won = Q.senate_d >= 50 ? 1 : 0;
"""
    if typ == 'pres':
        js += f"""
Q.pres_won = dp >= {ec} ? 1 : 0;
if (Q.pres_won) {{
    Q.white_house = 'D';
    Q.president = Q.nominee;
}} else {{
    Q.white_house = 'R';
    Q.president = 'Trump';
}}
Q.pres_result = Q.pres_won ? 'won the Electoral College' : 'lost the Electoral College';
Q.stability += Q.pres_won ? 2 : -2;
Q.enthusiasm += Q.pres_won ? 6 : -4;
"""
    js += extra_js
    body = intro.strip() + "\n\n"
    if typ == 'pres':
        body += "[? if pres_won == 1: **We have won the presidency.** ?][? if pres_won == 0: **We have lost the presidency.** ?] The national two-party vote came in at [+ dem_pop_str +]% for our side and [+ rep_pop_str +]% for theirs. In the Electoral College, we " + "[+ pres_result +]" + ".\n\n"
    else:
        body += "The national House vote came in at [+ dem_pop_str +]% for our side and [+ rep_pop_str +]% for theirs.\n\n"
    body += "**House:** [+ house_d +] Democratic seats. [? if house_won == 1: We hold the majority. ?][? if house_won == 0: We are in the minority. ?]\n\n**Senate:** [+ senate_d +] Democratic seats. [? if senate_won == 1: We control the chamber. ?][? if senate_won == 0: We are in the minority. ?]"
    ev = dict(id=eid, title=title, when=f"year = {year} and month = 10", priority=10, js=js, body=body, choices=[])
    return ev

EVENTS = []
E = EVENTS.append

# ---------------- 2014 ----------------
E(dict(id='aca_rollout', title='The Rollout', subtitle='Healthcare.gov crashes on launch.', when='year = 2014 and month = 1', priority=3,
 body="""The Affordable Care Act's central promise is that the uninsured can finally buy coverage. In practice, the website has struggled and millions of people have had their plans cancelled. Our opponents are gleeful. Our own side is worried.""",
 choices=[('defend','Defend the law and the substance.','Enthusiasm up, moderates nervous.','aca_secured += 1; enthusiasm += 2; mod_dissent += 3; capital -= 1 if capital > 0','We argue the website is a technical failure and the law is a moral and economic success. It holds the base. It does not convince everyone.'),
          ('fix','Fix it quietly and let results speak.','Slower, steadier.','funds -= 1 if funds > 0; media_trust += 1; stability += 1; pop_mod += 0.1','Engineers are brought in. By spring the site works, and enrollment surges. The story shifts, slowly.'),
          ('admit','Admit the mistakes loudly.','Credibility, but ammunition for opponents.','media_trust += 2; enthusiasm -= 2; pop_mod -= 0.1; mod_dissent -= 2','We say what went wrong and what we are doing about it. Some voters respect it. Others hear only the admission.')]))
E(dict(id='ferguson', title='Ferguson', subtitle='A shooting, a grand jury, and a movement.', when='year = 2014 and month = 7', priority=2,
 body="""The killing of Michael Brown by a police officer in Ferguson, Missouri, sets off protests that spread across the country. The questions are about policing, race, and accountability. The party has to decide how to speak.""",
 choices=[('listen','Back the protesters and the call for reform.','Base energized. Law-and-order voters uneasy.','enthusiasm += 4; prog_dissent -= 3; mod_dissent += 2; pop_mod -= 0.1; far_left += 1','We say the protesters have a point and that the pattern of policing demands reform. Our base responds.'),
          ('both','Call for calm and reform together.','The middle path.','enthusiasm += 1; stability += 1; prog_dissent += 1','We condemn violence, defend the right to protest, and call for federal review. Everybody is a little unsatisfied.'),
          ('quiet','Stay quiet. Let the DOJ do its work.','Avoids a fight, loses some trust.','enthusiasm -= 3; prog_dissent += 3; media_trust -= 1','Silence is read as indifference by some and prudence by others.')]))
E(dict(id='midterm_2014_stub', title='placeholder', when='year = 0', body='x'))  # removed below

# ---------------- 2015 ----------------
E(dict(id='sanders_enters', title='A Senator from Vermont', subtitle='An insurgent challenge from the left.', when='year = 2015 and month = 4', priority=2,
 body="""A democratic socialist senator from Vermont announces he will seek the Democratic nomination. Crowds are bigger than anyone expected. The establishment has a plan to coronate a front-runner. The question is how to treat the insurgency.""",
 choices=[('neutral','Insist on a neutral, open primary.','Fairer, riskier.','dnc_neutral = 1; prog_dissent -= 5; unity += 2; prog_strength += 3; nominee_mod += 0','We promise a level field. The left believes us, mostly.'),
          ('establishment','Quietly back the front-runner.','Safer in the short run, corrosive later.','dnc_neutral = 0; estab_strength += 2; prog_dissent += 6; far_left += 2','The party apparatus lines up behind the front-runner. It is not a secret.'),
          ('absorb','Invite the insurgents into the platform process.','Co-opts energy.','prog_dissent -= 3; unity += 2; mod_dissent += 2; prog_strength += 2','We give their ideas a seat at the table. Some call it co-optation. Others call it politics.')]))
E(dict(id='trump_escalator', title='The Escalator', subtitle='A television personality enters the race.', when='year = 2015 and month = 4', priority=1,
 body="""A real-estate developer and television star descends a golden escalator to announce his candidacy for the Republican nomination, opening with a harsh attack on immigrants. Commentators call it a joke. The Republican field is crowded. His numbers are not a joke.""",
 arrive='maga += 12; far_right += 4',
 choices=[('ignore','Treat it as a sideshow.','Safer in the short run.','maga += 2; stability -= 1','We assume the primary electorate will sort it out. It does not.'),
          ('engage','Take it seriously. Start building a contrast.','Early preparation.','funds -= 1 if funds > 0; media_trust += 1; stability += 2','Researchers and rapid-response staff are hired early. The files are thick by the fall.'),
          ('amplify','Quietly hope he wins the nomination.','A gamble that has side effects.','maga += 5; stability -= 3; far_right += 2; pop_mod += 0.1','Some strategists decide he is the easiest opponent. The risk to the system is not their department.')]))
E(dict(id='obergefell', title='A Landmark Summer', subtitle='Marriage equality and a massacre in Charleston.', when='year = 2015 and month = 7', priority=1,
 body="""In one week, a gunman murders nine people at a church in Charleston and the Supreme Court rules that same-sex couples have a constitutional right to marry. Grief and celebration share a news cycle.""",
 choices=[('unite','Speak to the moment, not the factions.','Rare unity.','enthusiasm += 3; unity += 3; media_trust += 2','For a few days the country looks like it is speaking to itself.'),
          ('gun','Press for gun reform.','Base energized, rural voters wary.','enthusiasm += 4; mod_dissent += 3; pop_mod -= 0.1; far_right += 1','We say what many are thinking. We do not win the votes.')]))

# ---------------- 2016 ----------------
E(dict(id='primary_2016', title='The Primary', subtitle='Clinton or Sanders?', when='year = 2016 and month = 1', priority=3,
 js="""
if (Q.dnc_neutral == 1 && Q.prog_strength >= 28) { Q.primary_leaning = 'sanders'; } else { Q.primary_leaning = 'clinton'; }
""",
 body="""The Iowa caucuses are weeks away. The front-runner has the endorsements, the money, and the delegates. The challenger has the crowds, the small donors, and an electrified left.""",
 choices=[('clinton','Consolidate around Clinton.','A safe path, if she can energize the base.','nominee = "Clinton"; nominee_mod += 0; estab_strength += 3; prog_dissent += 3; unity += 2','The apparatus delivers. The nomination is hers by spring, and the left is not happy.'),
          ('open','Let the voters decide, and mean it.','Higher risk, higher energy.','nominee = "Clinton"; nominee_mod += 0.2; enthusiasm += 4; unity -= 2; prog_dissent -= 3; prog_strength += 3','The race is long and the nominee is bruised, but the party is energized and the left feels respected. She still wins, narrowly.'),
          ('sanders','Back the insurgent.','A radical bet.','nominee = "Sanders"; nominee_mod -= 0.1; enthusiasm += 6; prog_strength += 8; mod_dissent += 8; estab_dissent += 5; unity -= 4; far_left += 3','The party takes the biggest swing in its modern history. The base is on fire. The establishment is terrified. The general election is the test.')]))
E(dict(id='dnc_hack', title='The Leak', subtitle='Foreign intelligence leaks party e-mails.', when='year = 2016 and month = 7', priority=2,
 body="""Thousands of internal party e-mails appear on a transparency website. U.S. intelligence agencies will later attribute the hack to Russian military intelligence. The e-mails show staffers disparaging the insurgent campaign. The convention opens in disarray.""",
 choices=[('apologize','Apologize, replace the chair, and move on.','Costs the party some pride.','unity += 3; prog_dissent -= 4; media_trust += 1; stability += 1','The chair steps down. The convention proceeds. The story will not go away.'),
          ('blame','Focus on the foreign interference.','Right on facts, mixed politically.','stability += 3; media_trust += 1; prog_dissent += 3; enthusiasm -= 1','We say, accurately, that a foreign government is trying to influence our election. Some hear it as an excuse.'),
          ('security','Rebuild cybersecurity quickly.','Boring, necessary.','funds -= 2 if funds >= 2; stability += 3; media_trust += 1','The party hires real security professionals. Too late for this cycle, in time for the next.')]))
# ---------------- 2017 ----------------
E(dict(id='dem_inaug_2017', title='A Democratic Inauguration', subtitle='Alt-history: we hold the White House.', when="year = 2017 and month = 1 and white_house == \"D\"", priority=5,
 body="""A Democratic president takes the oath. The coalition held, narrowly. The Republican Party's internal fight over its populist wing is only beginning. The question now is whether we can govern, and whether we can keep the opposition inside the rules.""",
 arrive='enthusiasm += 4; maga += 8',
 choices=[('govern','Govern boldly.','Capital and goodwill spent early.','capital += 1; pop_mod += 0.2; unity += 2','We aim high.'),
          ('bridge','Reach across the aisle.','Slower, steadier.','mod_dissent -= 3; stability += 3; media_trust += 2','We offer bipartisan ground.')]))
E(dict(id='trump_inaug_2017', title='Inauguration', subtitle='A different kind of presidency.', when="year = 2017 and month = 1 and white_house == \"R\"", priority=5,
 body="""The new president takes the oath. Millions of people will march the next day. Within weeks, the administration issues a sweeping travel restriction, fires officials, and tests the boundaries of presidential power. The party's task is no longer to win a campaign but to defend the structure of the republic.""",
 arrive='maga += 15; stability -= 4; enthusiasm += 8; far_right += 5',
 choices=[('resist','Total resistance.','Energy, but little room for deals.','enthusiasm += 6; prog_strength += 3; mod_dissent += 2; far_left += 1','We oppose, loudly and constantly. Our base loves it.'),
          ('selective','Selective opposition.','Hold the line where the republic is at stake.','stability += 3; media_trust += 2; enthusiasm += 2; mod_dissent -= 2','We pick our fights. Some on our side call it weakness. Others call it strategy.'),
          ('legal','Lawyer up and fight in court.','The institutional road.','stability += 4; funds -= 1 if funds > 0; media_trust += 1','Attorneys general sue; courts block some actions and permit others.')]))
E(dict(id='aca_repeal', title='Repeal and Replace', subtitle='A thin Senate margin.', when="year = 2017 and month = 7 and white_house == \"R\"", priority=2,
 body="""The Republican majorities attempt to repeal the Affordable Care Act. In the Senate the margin is a single vote. Town halls fill with angry constituents. Our base is watching.""",
 choices=[('mobilize','Flood town halls and phone lines.','Maximum pressure.','enthusiasm += 5; aca_secured += 1; pop_mod += 0.3; stability += 1','In the end, one senator walks to the well and gives a thumbs-down. The law survives.'),
          ('negotiate','Offer a narrow compromise.','Awkward, unusual.','mod_dissent -= 3; prog_dissent += 3; enthusiasm -= 1','The offer is rejected by both sides, but it shows we are willing to talk.')]))
E(dict(id='charlottesville', title='Charlottesville', subtitle='A rally, a killing, a president\'s response.', when="year = 2017 and month = 7", priority=2,
 body="""Torch-bearing white supremacists march through a Virginia college town. One of them drives a car into a crowd of counter-protesters, killing a woman. The president's response draws bipartisan criticism. Organized extremism has stepped out of the shadows.""",
 arrive='far_right += 6',
 choices=[('condemn','Unite the country in condemnation.','Moral clarity, broad appeal.','stability += 3; media_trust += 2; enthusiasm += 2; far_right -= 2','Leaders of both parties speak against hatred. The rally leaders are shunned.'),
          ('confront','Confront the far right in the streets.','Risky, can escalate.','enthusiasm += 4; far_left += 3; far_right += 2; stability -= 2; pop_mod -= 0.1','Counter-protests grow. Some are peaceful. Some are not. The fringes feed on each other.'),
          ('legal','Press for stronger domestic-extremism enforcement.','Institutional.','far_right -= 4; stability += 2; prog_dissent += 2','Civil libertarians worry about the tools. Law enforcement welcomes the attention.')]))
# ---------------- 2018 ----------------
E(dict(id='insurgent_primaries', title='Primary Season', subtitle='A bartender beats a ten-term congressman.', when='year = 2018 and month = 4', priority=2,
 body="""Insurgent left-wing candidates win a string of primaries, including a 28-year-old who unseats a senior House Democrat in New York. At the same time, moderates win a different set of swing-district primaries. The party's internal debate is now very public.""",
 choices=[('embrace','Embrace the new energy.','Base enthusiasm surges.','prog_strength += 5; enthusiasm += 5; mod_dissent += 4; far_left += 2; pop_mod += 0.1','New faces, new ideas, and a new set of disagreements.'),
          ('balance','Support both insurgents and moderates.','Big tent.','unity += 3; prog_dissent -= 2; mod_dissent -= 2; pop_mod += 0.3','The campaign committee backs the candidates best suited to their districts. The party is, for once, more flexible than its reputation.'),
          ('suppress','Back incumbents against challengers.','Defends experience.','estab_strength += 3; prog_dissent += 6; unity -= 3; far_left += 3','Incumbents are protected. The left remembers.')]))
E(dict(id='kavanaugh', title='The Confirmation', subtitle='A Supreme Court fight and an allegation.', when='year = 2018 and month = 7', priority=2,
 body="""A Supreme Court nominee faces credible allegations of sexual misconduct from his youth. The Senate hearing becomes a national drama. The nominee is confirmed on a narrow vote. The midterms are weeks away.""",
 choices=[('fight','Fight the nomination with everything.','Energizes the base. Red-state senators vulnerable.','enthusiasm += 6; pop_mod += 0.1; mod_dissent += 2; senate_d -= 1','We lose the vote, but the energy is real.'),
          ('measured','Press for a thorough investigation, then stand down.','Measured.','stability += 1; media_trust += 1; enthusiasm += 2','We argue for process and accept the result.')]))
# ---------------- 2019 ----------------
E(dict(id='ukraine_call', title='A Phone Call', subtitle='Impeachment becomes a live question.', when="year = 2019 and month = 7 and white_house == \"R\"", priority=2,
 body="""A whistleblower alleges that the president pressed a foreign leader to investigate a political rival while withholding military aid. Pressure builds on the House to act. The Senate will not convict.""",
 choices=[('impeach','Impeach.','Principle over strategy.','stability += 4; enthusiasm += 4; maga += 3; mod_dissent += 3; unity += 2','The House impeaches. The Senate acquits. The record is made.'),
          ('censure','Pursue censure and investigation.','Lower-risk.','stability += 1; media_trust += 1; enthusiasm -= 2; prog_dissent += 4','The pressure on the leadership is intense. They resist.'),
          ('avoid','Avoid impeachment. Focus on the election.','Political caution.','stability -= 3; enthusiasm -= 4; prog_dissent += 5; mod_dissent -= 3','We decide that the voters will decide. Many wonder what norms are left.')]))
E(dict(id='squad_feud', title='The Squad', subtitle='Intraparty feud goes public.', when='year = 2019 and month = 1', priority=1,
 body="""A handful of insurgent freshmen clash openly with the Speaker. Social media amplifies everything. The press loves a civil war. Our opponents love it more.""",
 choices=[('unify','Hold a unity summit.','Calming.','unity += 4; prog_dissent -= 3; mod_dissent -= 2; capital -= 1 if capital > 0','Nobody is pleased, but everyone is in the room.'),
          ('leadership','Back the leadership.','Order.','estab_strength += 2; prog_dissent += 5; far_left += 1; unity += 1','The leadership prevails. The left grumbles.'),
          ('insurgents','Back the insurgents.','Disruptive.','prog_strength += 4; mod_dissent += 5; enthusiasm += 3; unity -= 3','Their influence grows. So does the friction.')]))
# ---------------- 2020 ----------------
E(dict(id='incumbent_2020', title='The Incumbent Runs Again', subtitle='Alt-history: a Democrat holds the White House.', when='year = 2020 and month = 1 and white_house == "D"', priority=3,
 arrive='nominee = president',
 body="""With a Democrat in the White House, the 2020 nomination is a formality. The question is whether the coalition will hold together through a pandemic and a divided country.""",
 choices=[('go','Run on the record.','Continuity.','enthusiasm += 2; unity += 2','The campaign is built on the record.')]))
E(dict(id='primary_2020', title='The 2020 Primary', subtitle='A crowded field narrows.', when='year = 2020 and month = 1 and white_house == "R"', priority=3,
 body="""Two dozen candidates have entered. Only a few remain. The front-runners are a former vice president and a democratic-socialist senator. A South Carolina primary may decide it.""",
 choices=[('biden','Consolidate behind the former vice president.','Electability argument.','nominee = "Biden"; estab_strength += 3; mod_strength += 4; prog_dissent += 4; unity += 3; nominee_mod += 0','Moderates rally. The race is settled by March.'),
          ('open2','Let it play out.','Lets the voters decide.','nominee = "Biden"; nominee_mod += 0.2; enthusiasm += 3; unity -= 1; prog_dissent -= 2','The nomination goes to the former vice president. The campaign was long but the left felt heard.'),
          ('sanders2','Back the senator.','Higher risk, higher variance.','nominee = "Sanders"; nominee_mod -= 0.2; prog_strength += 6; mod_dissent += 7; estab_dissent += 4; unity -= 3; far_left += 2; enthusiasm += 5','A rough, historic bet. The base is thrilled. The establishment is anxious.')]))
E(dict(id='covid', title='The Pandemic', subtitle='A new coronavirus spreads across the world.', when='year = 2020 and month = 1', priority=2,
 arrive='stability -= 2; enthusiasm -= 2; media_trust -= 3',
 body="""A new coronavirus is spreading. By March, schools and offices close. Hospitals are overwhelmed. Everything about politics changes: campaigns, conventions, voting itself.""",
 choices=[('relief','Press for rapid, large-scale relief.','Government acts.','covid_relief = 1; pop_mod += 0.3; mod_dissent += 2; labor_dissent -= 4; stability += 2','The relief package passes with votes of both parties. Millions are spared the worst.'),
          ('science','Defer to public-health experts.','Credibility, unpopular lockdowns.','media_trust += 3; stability += 2; enthusiasm -= 1; pop_mod -= 0.1; far_right += 2','We follow public-health guidance. A noisy minority resists.'),
          ('voting','Fight for mail-in voting and expanded early voting.','Protects the franchise.','stability += 4; far_right += 3; pop_mod += 0.2','We expand access to the ballot. Opponents allege fraud, without evidence.')]))
E(dict(id='floyd', title='A Summer of Protest', subtitle='The killing of George Floyd.', when='year = 2020 and month = 4', priority=2,
 arrive='enthusiasm += 4; far_left += 4; far_right += 3',
 body="""A police officer kneels on George Floyd's neck for nine minutes. The video spreads worldwide. Protests fill cities for weeks. Most are peaceful. Some end in looting and burning. A slogan about defunding the police dominates the debate.""",
 choices=[('reform','Back structural police reform.','Concrete, can pass.','police_reform = 1; enthusiasm += 3; prog_dissent -= 3; mod_dissent += 2; pop_mod -= 0.05','We write the legislation. The details are hard.'),
          ('defund','Embrace the slogan.','The base cheers. Suburbs flinch.','enthusiasm += 5; prog_dissent -= 5; mod_dissent += 5; pop_mod -= 0.5; far_left += 3','The slogan is more popular on social media than it is at the ballot box.'),
          ('distance','Distance the party from "defund".','Wedge.','mod_dissent -= 4; prog_dissent += 5; pop_mod += 0.2; enthusiasm -= 2','We say reform, not abolition. Activists are unsatisfied.')]))
E(dict(id='capitol_attack', title='January 6th', subtitle='The Capitol is stormed.', when='year = 2021 and month = 1 and lost_2020_trump = 1', priority=9,
 arrive='stability -= 8; far_right += 10; maga += 3',
 body="""A mob, stirred by false claims that the election was stolen, breaks into the Capitol while Congress is certifying the results. Lawmakers shelter in place. Police are beaten. Hours later, Congress finishes the job. Many Republican members still vote to object to the results.""",
 choices=[('commission','Demand a full, bipartisan accounting.','Slow, institutional.','stability += 6; media_trust += 2; far_right -= 3','We pursue a commission. Republicans block it in the Senate. A House select committee investigates instead.'),
          ('prosecute','Press for accountability.','Courts and the rule of law.','stability += 5; far_right -= 4; maga += 1','Hundreds of rioters are prosecuted.'),
          ('move_on','Move on and focus on governing.','Looks to the future.','stability -= 3; enthusiasm -= 2; media_trust -= 1; pop_mod += 0.1','We say we will focus on the economy. The wound does not close.')]))
E(dict(id='r_2021', title='A Second Term', subtitle='Alt-history: the incumbent wins.', when="year = 2021 and month = 1 and white_house == \"R\" and lost_2020_trump = 0", priority=5,
 arrive='stability -= 4; maga += 8',
 body="""The incumbent has won re-election. The movement is emboldened. The opposition must find a way to resist for four more years.""",
 choices=[('hold','Hold the line.','Persist.','enthusiasm += 3; stability += 1','We continue.')]))
# ---------------- 2021 ----------------
E(dict(id='rescue_plan', title='The Rescue Plan', subtitle='Relief, reconciliation, and the debate over size.', when="year = 2021 and month = 4 and white_house == \"D\"", priority=2,
 body="""With a narrow trifecta, we can pass a large pandemic-relief package through budget reconciliation. Moderates worry about the size. Progressives want more.""",
 choices=[('big','Go big.','Stronger recovery, inflation risk.','covid_relief = 1; pop_mod += 0.4; enthusiasm += 4; mod_dissent += 3; labor_dissent -= 4; unity += 3','The package passes without a single Republican vote. The economy roars back. So, eventually, do prices.'),
          ('smaller','Go smaller.','Moderates happy.','covid_relief = 1; pop_mod += 0.1; mod_dissent -= 3; prog_dissent += 5; enthusiasm -= 1','A smaller package passes with a few bipartisan votes. The recovery is slower.')]))
E(dict(id='afghanistan', title='Kabul', subtitle='The longest war ends in chaos.', when="year = 2021 and month = 7 and white_house == \"D\"", priority=2,
 body="""The withdrawal from Afghanistan collapses into a frantic evacuation. A suicide bombing kills thirteen service members. The pictures are devastating. The policy had wide public support. The execution did not.""",
 choices=[('defend','Defend the decision to leave.','Principle over image.','pop_mod -= 0.3; mod_dissent += 2; unity += 1','The argument is right on the substance and weak on the politics.'),
          ('accountability','Acknowledge failures and review.','Honest, costly.','media_trust += 2; pop_mod -= 0.2; stability += 1','The after-action review is long. The damage is done.')]))
E(dict(id='reconciliation_standoff', title='Two Senators', subtitle='The filibuster and the reconciliation fight.', when="year = 2021 and month = 10 and white_house == \"D\"", priority=2,
 body="""Our majority in the Senate is 50 plus the Vice President. Two moderate Democratic senators block the more ambitious plans and refuse to change the filibuster. Activists threaten primaries. The Senate calendar slips.""",
 choices=[('infra','Pass the bipartisan infrastructure bill first.','A win.','pop_mod += 0.3; enthusiasm -= 1; prog_dissent += 3; mod_dissent -= 3','The infrastructure bill passes with Republican votes. The larger social package stalls.'),
          ('hold','Hold the infrastructure bill hostage.','Leverage.','prog_dissent -= 2; mod_dissent += 3; unity -= 2; capital -= 1 if capital > 0','Hardball. It does not move the two senators.'),
          ('filibuster','Push for filibuster reform on voting rights.','Principle.','voting_rights += 1; stability += 2; enthusiasm += 2; mod_dissent += 2; capital -= 1 if capital > 0','The effort fails when two senators refuse to go along. The voting-rights bills die.')]))
# ---------------- 2022 ----------------
E(dict(id='inflation', title='Prices', subtitle='Inflation reaches a forty-year high.', when="year = 2022 and month = 1", priority=2,
 arrive='pop_mod -= 0.4; enthusiasm -= 3',
 body="""Prices are rising at the fastest rate in four decades. Gas costs more. Groceries cost more. Supply chains are strained, and a war in Europe is about to make it worse. Whichever party is in power gets the blame.""",
 choices=[('supply','Focus on supply chains and competition.','Plausible, slow.','pop_mod += 0.1; mod_dissent -= 2','We name specific causes and propose specific fixes.'),
          ('deficit','Embrace deficit reduction.','Credibility with moderates.','mod_dissent -= 3; prog_dissent += 3; pop_mod += 0.1','We argue that restraint now will help prices later.'),
          ('transitory','Say it is temporary.','Risky.','pop_mod -= 0.2; media_trust -= 2','"Transitory" will be remembered.')]))
E(dict(id='dobbs', title='Dobbs', subtitle='The Supreme Court overturns Roe.', when='year = 2022 and month = 4', priority=2,
 arrive='enthusiasm += 8; pop_mod += 0.5',
 body="""The Supreme Court overturns Roe v. Wade. Abortion is now a state-by-state fight. For the first time in a generation, many Democratic voters feel an urgent reason to turn out.""",
 choices=[('legislate','Push for national legislation.','Likely to fail, but clarifies the stakes.','enthusiasm += 3; prog_dissent -= 3; pop_mod += 0.2','The bill fails in the Senate. The campaign is on.'),
          ('ballot','Take the fight to state ballot measures.','Wins where it counts.','pop_mod += 0.4; stability += 1; enthusiasm += 2','Referendums in several states show the issue is more popular than many expected.')]))
# ---------------- 2023 ----------------
E(dict(id='debt_ceiling', title='The Debt Ceiling', subtitle='A hostage crisis, again.', when='year = 2023 and month = 4', priority=2,
 body="""The new House majority demands cuts in exchange for raising the debt ceiling. The Treasury warns of default. The Constitution says the debt must be paid.""",
 choices=[('negotiate','Negotiate a deal.','Pragmatic.','stability += 2; prog_dissent += 3; mod_dissent -= 2; pop_mod += 0.1','A compromise passes, with some cuts and a suspension of the ceiling.'),
          ('stand','Refuse to negotiate.','Principle, risk.','stability -= 2; enthusiasm += 2; prog_dissent -= 2; mod_dissent += 1','The standoff stretches to the last minute.')]))
E(dict(id='gaza_split', title='A Divided Party', subtitle='War in the Middle East splits the coalition.', when='year = 2023 and month = 10', priority=2,
 arrive='far_left += 4; unity -= 4',
 body="""After the October 7th attacks on Israel and the war in Gaza that follows, the Democratic coalition splits. Young voters and progressives press for a ceasefire. Older voters and many in leadership support Israel. Campuses erupt. Antisemitism and Islamophobia both rise.""",
 choices=[('balance','Hold a balanced position.','Satisfies few.','unity += 1; prog_dissent += 3; mod_dissent += 1','We call for humanitarian relief, a hostage deal, and a long-term settlement. Nobody is fully satisfied.'),
          ('ceasefire','Press for a ceasefire.','Left satisfied.','prog_dissent -= 5; mod_dissent += 4; enthusiasm += 2; pop_mod -= 0.1','The administration is pressured. Some donors are furious.'),
          ('stand_israel','Stand with Israel firmly.','Moderates satisfied.','mod_dissent -= 3; prog_dissent += 8; far_left += 4; enthusiasm -= 3; unity -= 2','Youth turnout is a concern.')]))
# ---------------- 2024 ----------------
E(dict(id='biden_debate', title='The Debate', subtitle='A president under scrutiny.', when='year = 2024 and month = 4 and white_house == "D" and president == "Biden"', priority=3,
 body="""A June debate goes badly. For weeks, an elderly president's stamina has been quietly questioned. Now it is on every screen. Donors, members of Congress, and ordinary voters are asking whether he should continue.""",
 choices=[('stay','Stay in the race.','Loyalty and continuity.','pop_mod -= 0.6; unity += 1; enthusiasm -= 3; media_trust -= 1; stability -= 1','The president stays. The campaign is on defense. The polls do not move.'),
          ('withdraw','Withdraw and pass the torch.','A stunning, historic move.','nominee = "Harris"; pop_mod += 0.2; enthusiasm += 6; unity += 2; estab_dissent += 2; media_trust += 1','The president withdraws. The Vice President is the nominee. The energy returns. So does the time pressure.'),
          ('open_conv','Withdraw and call for an open convention.','Democratic, chaotic.','nominee = "Harris"; pop_mod += 0.1; unity -= 2; enthusiasm += 3; prog_dissent -= 3','An open process might have produced a better candidate. It might have produced chaos.')]))
E(dict(id='primary_2024_alt', title='The Nominee', subtitle='Alt-history: the nominee is chosen.', when='year = 2024 and month = 4 and (white_house == "R" or president != "Biden")', priority=3,
 body="""The incumbent Republican administration is deeply unpopular in some quarters and beloved in others. The party must choose a standard-bearer for 2024.""",
 choices=[('gov','A governor.','Fresh face.','nominee = "Newsom"; pop_mod += 0.2','A governor takes the nomination.'),
          ('vp','The Vice President.','Continuity.','nominee = "Harris"; pop_mod += 0.0','The Vice President takes the nomination.')]))
# ---------------- 2025 ----------------
E(dict(id='second_term', title='The Return', subtitle='A second Trump administration begins.', when="year = 2025 and month = 1 and white_house == \"R\"", priority=5,
 arrive='stability -= 6; maga += 12; enthusiasm -= 4; far_right += 2',
 body="""The president takes the oath again, with unified control of Congress and a Supreme Court inclined to defer on executive power. In the first days come dozens of executive orders, mass pardons of January 6th defendants, a sweeping reshuffling of the civil service, and a campaign to shrink the federal government. The party is in the minority in both chambers.""",
 choices=[('court','Sue first. Ask questions later.','Institutional.','stability += 3; funds -= 1 if funds > 0; media_trust += 1','State attorneys general and civil-society groups file suit after suit. Some injunctions stand. Many do not.'),
          ('regroup','Take time to regroup.','Avoids a reflexive fight.','unity += 3; enthusiasm -= 2; capital += 1','We do an honest post-mortem. The base is impatient.'),
          ('fight','Fight everywhere, immediately.','Energy.','enthusiasm += 4; prog_dissent -= 3; stability += 1; capital -= 1 if capital > 0','We make noise. Parts of the base love it. Moderates ask what the plan is.')]))
E(dict(id='d_2025_win', title='A Democratic Presidency Begins', subtitle='Alt-history: we won the White House.', when="year = 2025 and month = 1 and white_house == \"D\"", priority=5,
 arrive='enthusiasm += 4; maga += 4',
 body="""A Democrat is sworn in as president. The previous president and his movement are not going away. The next four years are a test of whether the coalition can govern and whether the republic can heal.""",
 choices=[('govern','Governing and delivery.','The mission.','capital += 1; stability += 2','We start with delivery.')]))
E(dict(id='tariffs_doge', title='Tariffs and Cuts', subtitle='The administration moves fast.', when="year = 2025 and month = 4 and white_house == \"R\"", priority=2,
 body="""Broad tariffs rattle markets. Aid and research grants are frozen. Thousands of federal employees are dismissed. The administration claims a mandate. The courts, Congress, and the public all push back, unevenly.""",
 choices=[('economy','Make the economic case.','Kitchen-table politics.','pop_mod += 0.4; mod_dissent -= 2; stability += 1','Prices, jobs, and retirement accounts become the focus. The message resonates.'),
          ('rights','Make the rule-of-law case.','Principled.','stability += 3; media_trust += 2; enthusiasm += 2','We argue that the government is not following the law. Many voters agree and many do not care.'),
          ('mobilize','Mobilize protests.','Mass energy.','enthusiasm += 5; far_left += 1; pop_mod += 0.2','Protests grow and stay peaceful, overwhelmingly.')]))
E(dict(id='political_violence', title='Violence', subtitle='A hostile year for democratic politics.', when="year = 2025 and month = 7", priority=2,
 arrive='stability -= 3; far_left += 2; far_right += 2',
 body="""Political violence reaches new heights: state lawmakers are shot, an activist is assassinated at a campus event, and threats against judges and election officials multiply. The temperature is far too high.""",
 choices=[('denounce','Denounce violence from any direction.','Principled.','stability += 4; media_trust += 2; far_right -= 2; far_left -= 2; enthusiasm -= 1','We say, clearly, that violence is never acceptable.'),
          ('security','Fund security for officials and election workers.','Practical.','stability += 3; funds -= 1 if funds > 0; far_right -= 1','Funds flow to local security.'),
          ('blame','Blame the other side.','Cathartic, corrosive.','enthusiasm += 2; stability -= 3; far_right += 2; far_left += 2; media_trust -= 2','Rhetoric escalates. The temperature does not drop.')]))
E(dict(id='shutdown_2025', title='Shutdown', subtitle='A standoff over health care subsidies.', when="year = 2025 and month = 10 and white_house == \"R\"", priority=2,
 body="""The government shuts down for weeks in a fight over expiring health-insurance subsidies. Federal workers go unpaid. Flights are delayed. Both sides claim the moral high ground. In November, elections in New Jersey and Virginia go strongly to our side, and a democratic socialist wins the New York City mayoralty.""",
 arrive='enthusiasm += 6; pop_mod += 0.3',
 choices=[('hold','Hold out for the subsidies.','Principle, pain.','enthusiasm += 4; prog_dissent -= 4; mod_dissent += 2; pop_mod += 0.1','We hold. The shutdown drags on, and the pressure builds on both sides.'),
          ('deal','Take a deal.','Reopens government.','unity -= 3; prog_dissent += 6; enthusiasm -= 3; mod_dissent -= 2','A deal is struck, with a promise to vote on the subsidies later. The base is not pleased.')]))
# ---------------- 2026 ----------------
E(dict(id='enforcement_surge', title='Enforcement', subtitle='Federal agents in American cities.', when="year = 2026 and month = 1 and white_house == \"R\"", priority=2,
 arrive='far_left += 2; stability -= 2',
 body="""A surge of federal immigration enforcement in major cities provokes protests, standoffs with local police, and fatal shootings. The administration says it is restoring order. The opposition says it is breaking the law. A divided public watches.""",
 choices=[('law','Press the rule-of-law case.','Principled.','stability += 3; media_trust += 2; enthusiasm += 3; pop_mod += 0.2','We argue for due process, judicial warrants, and accountability. It works with the public.'),
          ('shield','Pass state laws to limit cooperation.','State resistance.','enthusiasm += 4; far_right += 2; mod_dissent += 2; pop_mod += 0.1','States pass laws limiting cooperation. The federal-state conflict deepens.')]))
E(dict(id='midterm_push_2026', title='The Last Stretch', subtitle='The midterms are close.', when="year = 2026 and month = 7", priority=2,
 body="""With three months until Election Day, the question is whether the coalition can turn discontent into turnout, and whether the party can persuade the persuadable. The stakes are as high as they have been in our lifetimes.""",
 choices=[('turnout','All-in on turnout.','Base mobilization.','funds -= 2 if funds >= 2; enthusiasm += 6; pop_mod += 0.4','We pour resources into field operations.'),
          ('persuasion','All-in on persuasion.','Moderates and independents.','funds -= 2 if funds >= 2; pop_mod += 0.5; mod_dissent -= 3; media_trust += 1','We invest in persuasion and message testing.'),
          ('defense','Invest in election protection.','Defend the process.','funds -= 2 if funds >= 2; stability += 5; pop_mod += 0.1','We prepare for disputed results and intimidation.')]))

# remove placeholders
EVENTS = [e for e in EVENTS if e['id'] != 'midterm_2014_stub']

for ev in EVENTS:
    emit(ev)

# ---------------- elections ----------------
ELECTIONS = [
  ('election_2014', 2014, 'Midterms 2014', 47.0, 'mid', 188, 46,
   "The midterms of a two-term president's second term are rarely kind. This one is no exception."),
  ('election_2016', 2016, 'Election Night 2016', 51.1, 'pres', 194, 48,
   "A long election night. A long campaign. A result that will be debated for years."),
  ('election_2018', 2018, 'Midterms 2018', 54.4, 'mid', 235, 47,
   "A year of protests, special elections, and record turnout. The midterms are a referendum."),
  ('election_2020', 2020, 'Election 2020', 52.3, 'pres', 222, 50,
   "Voting takes place in the middle of a pandemic, by mail and in person. Counting takes days."),
  ('election_2022', 2022, 'Midterms 2022', 48.4, 'mid', 213, 51,
   "Inflation and abortion rights both shape the vote. Predictions of a wave prove premature."),
  ('election_2024', 2024, 'Election 2024', 49.2, 'pres', 215, 47,
   "The country votes in a year of rapid upheaval. The result will shape the next four years."),
  ('election_2026', 2026, 'Midterms 2026', 54.5, 'mid', 228, 52,
   "The midterms of a president's second term. The historical pattern points one way. The question is how hard."),
]
for eid, year, title, hist, typ, hb, sb, intro in ELECTIONS:
    extra = ''
    if year == 2020:
        extra = "\nQ.lost_2020_trump = Q.pres_won ? 1 : 0;\n"
    if year == 2026:
        extra = "\nQ.midterm_2026_done = 1;\n"
    ec = {2016: 51.5, 2020: 52.0, 2024: 50.5}.get(year, 51.5)
    ev = election(eid, year, title, hist, typ, hb, sb, intro, extra, ec)
    ev['choices'] = []
    emit(ev)

print("wrote", len(EVENTS), "events and", len(ELECTIONS), "elections")
