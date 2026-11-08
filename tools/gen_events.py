from dry import *

def ev(id, *a, **k):
    write('scenes/events/%s.scene.dry' % id, event(id, *a, **k))

SHARE = '(1-dissent)'

# =============================================================================
# SCHEDULED
# =============================================================================
ev('intro_2014', 'January 2014: The Democratic Party', 'year = 2014 and month = 1', """
You lead the %s through one of the most turbulent periods in American history. Each month you may take **one action** by playing a card from your hand: Party Affairs cards manage fundraising, messaging, organizing, and relations; Government Affairs cards let you govern whenever the party holds power. **Advisors** can offer free actions once every six months.

Your coalition (workers, suburbanites, college-educated professionals, rural voters, minority communities, and the young) is shifting beneath your feet. Your factions (progressives, establishment, labor, moderates, and later abundance and populist wings) will quarrel. Enemies are rising on the right and on the left. The calendar is fixed: elections come every November of an even year; you have until the end of December 2026.

The goal is simple, and far from easy: **keep American democracy afloat**, and win as often as you can.
""" % DEM(), priority=500)

ev('election_midterm', 'Midterm Election Day', 'election_due = 1 and midterm_year = 1 and election_shown != year', """
Americans have voted in the [+ year +] midterm elections.

The national House vote: %s [+ el_dem_votes +]%%, %s [+ el_gop_votes +]%%, left parties [+ el_left_votes +]%%, far-right parties [+ el_farright_votes +]%%. Turnout was [+ el_turnout +]%% of eligible voters.

[? if el_house >= 218 : The %s **win control of the House**, [+ el_house +] seats to [+ el_house_gop +]. ?][? if el_house < 218 : The %s will **control the House**, [+ el_house_gop +] seats to [+ el_house +]. ?]In the Senate the new balance is [+ el_senate +] Democratic-caucus seats to [+ el_senate_gop +].

<div class="sd-chart" data-chart="house" data-dem="[+ el_house +]" data-prev="[+ house_dem +]"></div>

<div class="sd-chart" data-chart="senate" data-dem="[+ el_senate +]" data-prev="[+ senate_dem +]"></div>

[? if dem_president = 1 : The president\'s party historically suffers in midterms, and tonight the pattern holds in most of the country. ?][? if dem_president = 0 : Voters have delivered a verdict on the president\'s first term in office. ?]
""" % (DEM(), GOP(), DEM(), GOP()), fx='election_shown = year', priority=800, max_visits=0)

ev('election_presidential', 'Presidential Election Day', 'election_due = 1 and pres_year = 1 and election_shown != year', """
Americans have voted in the [+ year +] presidential election.

Popular vote: %s [+ el_dem_votes +]%%, %s [+ el_gop_votes +]%%, left candidates [+ el_left_votes +]%%, far-right candidates [+ el_farright_votes +]%%. Turnout: [+ el_turnout +]%%.

Electoral College: **Democrats [+ el_dem_ev +]**, **Republicans [+ el_gop_ev +]**.

<div class="sd-chart" data-chart="ec" data-dem-ev="[+ el_dem_ev +]" data-gop-ev="[+ el_gop_ev +]" data-margins="[+ el_blue_core +],[+ el_rust_belt +],[+ el_heartland_swing +],[+ el_sun_belt +],[+ el_red_core +]" data-wins="[+ el_blue_core_win +],[+ el_rust_belt_win +],[+ el_heartland_swing_win +],[+ el_sun_belt_win +],[+ el_red_core_win +]"></div>

Battleground margins (Democratic lead in points): industrial Midwest [+ el_rust_belt +], Florida/Ohio/Iowa [+ el_heartland_swing +], Sun Belt [+ el_sun_belt +].

[? if el_pres_winner == "D" : The **Democratic nominee wins the presidency**. ?][? if el_pres_winner == "R" : The **Republican nominee wins the presidency**. ?]Congress: House [+ el_house +]-[+ el_house_gop +] and Senate [+ el_senate +]-[+ el_senate_gop +] (Democratic-Republican, new Congress seated in January).

<div class="sd-chart" data-chart="house" data-dem="[+ el_house +]" data-prev="[+ house_dem +]"></div>

<div class="sd-chart" data-chart="senate" data-dem="[+ el_senate +]" data-prev="[+ senate_dem +]"></div>
""" % (DEM(), GOP()), fx='election_shown = year', priority=800, max_visits=0)

ev('new_congress', 'A New Congress', 'just_seated = 1 and just_inaugurated = 0 and congress_shown != time', """
The new Congress convenes. The House has [+ house_dem +] Democrats and [+ house_gop +] Republicans; the Senate has [+ senate_dem +] in the Democratic caucus against [+ senate_gop +] Republicans.

[? if dem_house = 1 and dem_senate = 1 : We control both chambers. ?][? if dem_house = 1 and dem_senate = 0 : We control the House but not the Senate. ?][? if dem_house = 0 and dem_senate = 1 : We control the Senate but not the House. ?][? if dem_house = 0 and dem_senate = 0 : We are in the minority in both chambers. ?]
""", fx='congress_shown = time', priority=700, max_visits=0)

ev('inauguration', 'Inauguration Day', 'just_inaugurated = 1 and inaug_shown != time', """
On January 20, [+ year +], **[+ president +]** is sworn in as president.

[? if dem_president = 1 : A Democrat is back in the White House. The party now has to govern: expectations will be very high, and the factions are already fighting over priorities. ?][? if dem_president = 0 : A Republican takes the oath of office. We are in opposition: our task is to organize, to protect institutions from abuse, and to win the next elections. ?]

[? if dem_house = 1 and dem_senate = 1 and dem_president = 1 : Democrats hold a **trifecta**: the White House, the House, and the Senate. ?][? if dem_president = 0 and dem_house = 0 and dem_senate = 0 : Republicans hold a **trifecta**. ?]
""", fx='inaug_shown = time', priority=750, max_visits=0)

# =============================================================================
# PRIMARIES
# =============================================================================
DNOM = [
 ('establishment_nominee', 'The establishment standard-bearer', "Q.dem_nominee_mod = {suburban: 4, educated: 3, minority: 3, working: -1, young: -3};", 'establishment_strength += 5; progressive_dissent += 6; dem_enthusiasm -= 0.3', 'the Establishment nominee',
  'A seasoned figure with deep party ties and a long record, who excels with suburbanites and minority voters but struggles to excite the young. [? if year = 2016 : (Historically: Hillary Clinton.) ?][? if year = 2020 : (Historically: Joe Biden.) ?][? if year = 2024 : (Historically: Kamala Harris.) ?]'),
 ('progressive_nominee', 'The progressive insurgent', "Q.dem_nominee_mod = {young: 6, educated: 1, minority: 1, working: 3, suburban: -4};", 'progressive_strength += 6; establishment_dissent += 6; moderate_dissent += 4; dem_enthusiasm += 0.8; farleft_strength -= 3', 'the Progressive nominee',
  'A movement candidate who electrifies the young and the left but frightens suburban moderates. [? if year = 2016 or year = 2020 : (Historically: Bernie Sanders.) ?]'),
 ('heartland_nominee', 'The heartland moderate', "Q.dem_nominee_mod = {rural: 3, working: 3, suburban: 2, minority: -1, young: -2};", 'moderate_strength += 5; progressive_dissent += 4; populist_strength += 2', 'the Heartland nominee',
  'A governor or senator from a swing state who can talk to rural and working-class voters, though the base finds the candidate less thrilling.'),
 ('outsider_nominee', 'The charismatic young outsider', "Q.dem_nominee_mod = {young: 5, minority: 2, suburban: 1, educated: 2, rural: 1};", 'abundance_strength += 4; establishment_dissent += 3; dem_enthusiasm += 1.0', 'the Young nominee',
  'A fresh face with a gift for communication and a thin résumé. Voters are intrigued; the establishment is nervous. [? if year = 2020 : (Historically: Pete Buttigieg ran in this lane.) ?]'),
]
opts = []
for oid, label, mod, fx, nm, desc in DNOM:
    js_lines = []
    for x in [t.strip() for t in fx.split(';') if t.strip()]:
        sign = '+' if '+=' in x else '-'
        k, v = x.split('+=') if '+=' in x else x.split('-=')
        js_lines.append('Q.%s = (Q.%s || 0) %s %s;' % (k.strip(), k.strip(), sign, v.strip()))
    block = '{!\n%s\nQ.dem_nominee_name = "%s"; Q.dem_nominee_done = Q.year;\n%s\n!}' % (mod, nm, '\n'.join(js_lines))
    opts.append(opt(oid, label, fx=block, text=desc + '\n\nOur backing helps decide the nomination. The party rallies, however grudgingly.',
                    sub='A candidate for the nominating convention.'))
ev('dem_primary', 'The Democratic Presidential Primary', 'pres_year = 1 and month = 3 and dem_nominee_done != year and (dem_president = 0 or president_terms >= 2)', """
The race for our presidential nomination is underway. The party apparatus, donors, unions, and activists all have their favorites, and as party leadership we can quietly tilt the field, or watch it sort itself out.

Which kind of candidate should we help bring to the convention?
""", opts, priority=600, max_visits=0)

ev('dem_incumbent', 'The President Seeks Re-election', 'pres_year = 1 and month = 3 and dem_nominee_done != year and dem_president = 1 and president_terms < 2', """
**[+ president +]** is running for a second term and faces no serious challenger. The party rallies behind the president, for better or worse: the record belongs to us all.
""", fx='dem_nominee_name = president; dem_nominee_done = year; incumbent_bonus = 1', priority=600, max_visits=0)

GOP_MAGA_MOD = "Q.gop_nominee_mod = {rural: 5, working: 4, young: 1, minority: 1, suburban: -3, educated: -5};"
GOP_MAIN_MOD = "Q.gop_nominee_mod = {suburban: 2, educated: 2, rural: 1, working: 1, minority: 1};"
ev('gop_primary_maga', 'The Republican Primary: The Insurgent Wins', 'pres_year = 1 and month = 4 and gop_nominee_done != year and not (dem_president = 0 and president_terms < 2) and ((year = 2016 and (trump_active = 1 or maga_strength >= 45)) or (year > 2016 and maga_strength >= 40))', """
The populist-nationalist movement has won the Republican nomination. **[+ maga_leader +]** captured the primaries with a message of grievance against elites, trade deals, and immigration, defying the party establishment.

The %s will have a loyal, energized base; the %s will have an enemy with a gift for dominating the news cycle, and a movement that has never promised to accept defeat quietly.
""" % (GOP(), DEM()),
   fx="""{!
Q.gop_nominee_mod = {rural: 5, working: 4, young: 1, minority: 1, suburban: -3, educated: -5};
Q.gop_nominee_name = Q.maga_leader; Q.gop_nominee_type = 'maga'; Q.gop_nominee_done = Q.year;
Q.gop_enthusiasm = Math.min(10, Q.gop_enthusiasm + 1.2); Q.trump_urgency = (Q.trump_urgency || 0) + 0.8; Q.trump_active = 1;
!}""", priority=590, max_visits=0)

ev('gop_primary_main', 'The Republican Primary: The Establishment Wins', 'pres_year = 1 and month = 4 and gop_nominee_done != year and not (dem_president = 0 and president_terms < 2) and not ((year = 2016 and (trump_active = 1 or maga_strength >= 45)) or (year > 2016 and maga_strength >= 40))', """
The Republican establishment has held its party. A mainstream conservative wins the nomination without dramatic upheaval. The insurgent right is restless, but the party\'s institutions held.

Our opponent will run a conventional campaign: competent, well-funded, and cautious.
""", fx="""{!
Q.gop_nominee_mod = {suburban: 2, educated: 2, rural: 1, working: 1, minority: 1};
Q.gop_nominee_name = 'the mainstream Republican'; Q.gop_nominee_type = 'mainstream'; Q.gop_nominee_done = Q.year;
!}""", priority=590, max_visits=0)

ev('gop_incumbent', 'The Republican President Seeks Re-election', 'pres_year = 1 and month = 4 and gop_nominee_done != year and dem_president = 0 and president_terms < 2', """
**[+ president +]** is running for re-election and faces no serious primary challenge. Republicans rally to the incumbent.
""", fx="gop_nominee_name = president; gop_nominee_done = year; incumbent_bonus = 1", priority=590, max_visits=0)

# =============================================================================
# 2014 - 2016
# =============================================================================
ev('aca_rollout', 'The Healthcare Rollout', 'year = 2014 and month = 2', """
The Affordable Care Act\'s coverage provisions have taken effect, but the rollout has been rocky: website failures, cancelled plans, and a flood of attack ads. Millions are nonetheless enrolling.

How should the party respond?
""", [
 opt('aca_defend', 'Defend the law loudly', fx='uninsured -= 1; progressive_dissent -= 2; moderate_dissent += 2; dem_enthusiasm += 0.3; gop_enthusiasm += 0.3', text='We run a loud, proud campaign on healthcare. Enrollment surges; so do the attacks.'),
 opt('aca_fix', 'Focus on fixing the problems', fx='uninsured -= 1.5; moderate_strength += 2; suburban_dem += 2*(1-dissent); progressive_dissent += 2', text='We concede mistakes, fix the website, and extend enrollment deadlines. Coverage numbers improve.'),
 opt('aca_distance', 'Keep our distance', fx='moderate_dissent -= 2; progressive_dissent += 4; working_dem -= 2*(1-dissent)', text='Vulnerable candidates avoid mentioning the law. Our base notices.')])

ev('crimea', 'Russia Annexes Crimea', 'year = 2014 and month = 3', """
Russian forces have seized Crimea, and Moscow annexes the peninsula after a referendum the West calls illegitimate. The American public is tired of war; yet Europe expects leadership.
""", [
 opt('crimea_sanctions', 'Support strong sanctions and aid', fx='intl_relation += 6; moderate_strength += 2; progressive_dissent += 2', text='We back coordinated sanctions and aid to Kyiv. Allies are reassured.'),
 opt('crimea_restraint', 'Emphasize restraint', fx='progressive_strength += 2; intl_relation -= 3; moderate_dissent += 3; populist_strength += 1', text='We caution against escalation. Some call it appeasement; others call it prudence.')])

ev('isis', 'The Rise of ISIS', 'year = 2014 and month = 6', """
The Islamic State has seized Mosul and proclaims a caliphate. Pressure mounts for American military action in Iraq and Syria. Public opinion is weary after a decade of war.
""", [
 opt('isis_strikes', 'Back limited air strikes', fx='moderate_strength += 2; intl_relation += 2; progressive_dissent += 5; military_loyalty += 0.02', text='We support targeted strikes and support for local partners. The left is uneasy.'),
 opt('isis_vote', 'Demand a congressional vote', fx='institutions += 1; progressive_strength += 1; moderate_dissent += 2; pro_democracy += 0.5', text='We insist Congress, not the president alone, authorize any war.'),
 opt('isis_oppose', 'Oppose any new military action', fx='progressive_strength += 3; progressive_dissent -= 4; moderate_dissent += 5; intl_relation -= 2', text='We warn of another quagmire. The base cheers; hawks worry.')])

ev('ferguson', 'Ferguson', 'year = 2014 and month = 8', """
A police shooting in Ferguson, Missouri, has ignited protests across the country. Images of armored vehicles on American streets stun the nation. Our coalition is united in grief and divided in tactics.
""", [
 opt('ferguson_reform', 'Champion police reform', fx='minority_dem += 4*(1-dissent); young_dem += 2*(1-dissent); progressive_dissent -= 3; local_police_loyalty -= 0.03; polarization += 1', text='We back body cameras, accountability, and community policing.'),
 opt('ferguson_calm', 'Call for calm and dialogue', fx='suburban_dem += 2*(1-dissent); minority_dem += 1*(1-dissent); progressive_dissent += 3; polarization -= 0.5', text='We appeal for calm and dialogue. Some activists feel patronized.'),
 opt('ferguson_order', 'Emphasize public order', fx='suburban_dem += 3*(1-dissent); working_dem += 1*(1-dissent); minority_dem -= 3*(1-dissent); progressive_dissent += 6; directleft_strength += 5', text='We stress that violence helps no one. Our base is angry.')])

ev('charleston', 'Charleston', 'year = 2015 and month = 6', """
A white supremacist has murdered nine worshippers at a historic Black church in Charleston, South Carolina. The nation mourns; the argument over firearms and the Confederate flag erupts again.
""", [
 opt('charleston_guns', 'Push for gun safety legislation', fx='suburban_dem += 3*(1-dissent); rural_dem -= 2*(1-dissent); minority_dem += 2*(1-dissent); gop_enthusiasm += 0.4; polarization += 1', text='We call for background checks. The bill stalls, but the fight energizes our suburban base.'),
 opt('charleston_flag', 'Focus on racism and the Confederate flag', fx='minority_dem += 3*(1-dissent); pro_democracy += 1; polarization += 0.5; farright_strength += 0.5', text='Statehouses begin to remove Confederate symbols; the moment unites many.'),
 opt('charleston_unity', 'Lead a unifying moment of mourning', fx='pro_democracy += 1.5; polarization -= 1.5; minority_dem += 1*(1-dissent); suburban_dem += 1*(1-dissent)', text='A national moment of unity gives the country a brief respite.')])

ev('obergefell', 'Marriage Equality', 'year = 2015 and month = 6', """
The Supreme Court has ruled that same-sex couples have a constitutional right to marry. The moment is a landmark for civil rights, and a flashpoint for cultural conservatives.
""", [
 opt('marriage_celebrate', 'Celebrate the ruling', fx='young_dem += 3*(1-dissent); educated_dem += 2*(1-dissent); rural_dem -= 1*(1-dissent); progressive_dissent -= 2; gop_enthusiasm += 0.3', text='Celebrations erupt across the country, and not everywhere.'),
 opt('marriage_respect', 'Celebrate and respect dissenters', fx='young_dem += 2*(1-dissent); suburban_dem += 1*(1-dissent); polarization -= 0.5', text='We celebrate while pledging to protect religious liberty.')])

ev('iran_deal', 'The Iran Nuclear Deal', 'year = 2015 and month = 7', """
Negotiators have reached an agreement limiting Iran\'s nuclear program. Critics call it dangerous; supporters call it the best alternative to war. The vote in Congress will be bitter.
""", [
 opt('iran_support', 'Back the deal', fx='intl_relation += 4; progressive_dissent -= 2; moderate_dissent += 2; biz_relation -= 1', text='We defend the agreement as the best way to prevent war.'),
 opt('iran_hedge', 'Support it, with conditions', fx='moderate_strength += 2; intl_relation += 2; progressive_dissent += 2', text='We back the deal with new inspection guarantees.')])

ev('maga_outsider', 'An Outsider Enters the Race', 'year = 2015 and month >= 6 and trump_checked = 0', """
[? if maga_strength >= 29 : A brash outsider has entered the Republican primary, with no political experience, a talent for television, and a message about trade, immigration, and elites that resonates with millions of disaffected voters. The Republican establishment is horrified, and polls are not reassuring. ?][? if maga_strength < 29 : A handful of political outsiders have entered the Republican primary. The anti-establishment mood is real, but the movement lacks a champion capable of breaking through. ?]

How seriously do we take this?
""", [
 opt('outsider_serious', 'Take the threat seriously', fx='trump_urgency += 1.5; trump_checked = 1; dem_enthusiasm += 0.3; pro_democracy += 0.5; maga_strength -= 0.5', text='We start preparing early, in case the outsider breaks through.'),
 opt('outsider_laugh', 'Treat it as a sideshow', fx='trump_checked = 1; trump_urgency -= 0.3; maga_strength += 1', text='We treat the whole thing as a joke. Some of us will regret it.'),
 opt('outsider_grievances', 'Engage with the grievances', fx='trump_checked = 1; trump_urgency += 0.5; working_dem += 2*(1-dissent); rural_dem += 2*(1-dissent); populist_strength += 2; maga_strength -= 1.5', text='We study why the message resonates and adjust our economic pitch.')],
 fx='trump_active = 1 if maga_strength >= 29', priority=400)

ev('paris_attacks', 'Paris Attacks', 'year = 2015 and month = 11', """
Coordinated terrorist attacks have killed 130 people in Paris. In the United States a fierce debate begins over refugees and security.
""", [
 opt('refugees_welcome', 'Defend refugee resettlement', fx='progressive_dissent -= 3; rural_dem -= 2*(1-dissent); maga_strength += 1.5; minority_dem += 1*(1-dissent)', text='We argue that refusing refugees hands the terrorists a victory.'),
 opt('refugees_vetting', 'Support stricter vetting', fx='suburban_dem += 2*(1-dissent); rural_dem += 1*(1-dissent); progressive_dissent += 4; maga_strength -= 0.5', text='We back tougher screening while keeping the program alive.')])

ev('flint_water', 'The Flint Water Crisis', 'year = 2016 and month = 1', """
Residents of Flint, Michigan, have been drinking poisoned water. The crisis exposes decaying infrastructure and indifference to poor communities across the country.
""", [
 opt('flint_infra', 'Make infrastructure a national issue', fx='working_dem += 2*(1-dissent); minority_dem += 2*(1-dissent); abundance_strength += 1; populist_strength += 1', text='We call for large infrastructure investment, with bipartisan potential.'),
 opt('flint_accountability', 'Demand accountability', fx='minority_dem += 2*(1-dissent); progressive_dissent -= 2; polarization += 1; institutions += 0.5', text='Officials are investigated, and the issue becomes a symbol.')])

ev('scalia_vacancy', 'A Supreme Court Vacancy', 'year = 2016 and month = 3', """
Justice Scalia\'s death has left a vacancy on the Supreme Court in an election year.

[? if dem_president = 1 and dem_senate = 1 : A Democratic Senate stands ready to confirm a moderate nominee. ?][? if dem_president = 1 and dem_senate = 0 : The Republican Senate has signaled it will not hold hearings on any Democratic nominee. ?][? if dem_president = 0 : The Republican president will fill the seat quickly. ?]
""", [
 opt('scalia_nominee', 'Press the nomination fight', fx='{!\nif (Q.dem_president && Q.dem_senate) { Q.court_lean -= 1; }\nif (Q.dem_president && !Q.dem_senate) { Q.dem_enthusiasm = Math.min(10, Q.dem_enthusiasm + 0.8); Q.polarization += 1; }\nif (!Q.dem_president) { Q.court_lean += 1; Q.dem_enthusiasm = Math.min(10, Q.dem_enthusiasm + 0.4); }\n!}', text='We use every procedural tool and every public platform to make the Court a campaign issue.'),
 opt('scalia_compromise', 'Seek a compromise', fx='{!\nif (Q.dem_president && Q.dem_senate) { Q.court_lean -= 0.5; }\nif (Q.dem_president && !Q.dem_senate) { Q.court_lean += 0.3; }\nif (!Q.dem_president) { Q.court_lean += 0.8; }\nQ.gopmod_relation += 4; Q.progressive_dissent += 3; Q.institutions += 1;\n!}', text='We appeal for a consensus nominee to protect the Court\'s legitimacy.')], priority=300)

ev('brexit_warning', 'Brexit and the Populist Wave', 'year = 2016 and month = 6', """
British voters have chosen to leave the European Union, and populist movements across the West are riding a wave of anger at globalization and elites. Many ask whether the same wave is coming for America.
""", [
 opt('brexit_econ', 'Sharpen our economic message', fx='working_dem += 3*(1-dissent); rural_dem += 1*(1-dissent); populist_strength += 2; crisis_urgency += 1', text='We stress wages, jobs, and community, and take the anger seriously.'),
 opt('brexit_warn', 'Warn of the dangers of nationalism', fx='trump_urgency += 1; suburban_dem += 2*(1-dissent); educated_dem += 1*(1-dissent); rural_dem -= 1*(1-dissent)', text='We warn that economic anxiety is being exploited.')])

ev('convention_platform', 'The Democratic Convention', 'pres_year = 1 and month = 7 and convention_done != year', """
Delegates gather for the party\'s national convention. The platform is a battlefield: progressives want bold commitments, moderates want caution, labor wants trade protections, and everyone wants unity.
""", [
 opt('platform_bold', 'A bold platform', fx='convention_done = year; progressive_dissent -= 6; moderate_dissent += 4; left_relation += 5; farleft_strength -= 1; suburban_dem -= 1*(1-dissent); young_dem += 2*(1-dissent); dem_enthusiasm += 0.4', text='The platform embraces ambitious commitments. The left is pleased.'),
 opt('platform_balanced', 'A balanced platform', fx='convention_done = year; progressive_dissent += 1; moderate_dissent -= 1; labor_dissent -= 1; suburban_dem += 1*(1-dissent)', text='A carefully negotiated platform offends few and thrills fewer.'),
 opt('platform_unity', 'A unity convention', fx='convention_done = year; progressive_dissent -= 3; moderate_dissent -= 3; labor_dissent -= 3; populist_dissent -= 3; establishment_dissent -= 3; abundance_dissent -= 3; resources -= 1', text='Speakers across the spectrum embrace each other onstage. The show of unity helps.', choose='resources >= 1', unavail='Need 1 resource.')], priority=250, max_visits=0)

ev('october_surprise', 'An October Surprise', 'pres_year = 1 and month = 10 and october_done != year and (dissent_percent >= 10 or maga_strength >= 30)', """
Days before the election, a damaging story about our campaign breaks, whether it is an investigation, a leak, or a hacked email trove. The media amplifies it. Our opponents seize on it.
""", [
 opt('surprise_transparent', 'Release everything', fx='october_done = year; dem_enthusiasm -= 0.3; pro_democracy += 0.5; suburban_dem += 1*(1-dissent); resources -= 0', text='We insist on full transparency. The story fades, though not before it hurts.'),
 opt('surprise_counter', 'Counterattack', fx='october_done = year; polarization += 1; dem_enthusiasm += 0.3; suburban_dem -= 2*(1-dissent); gop_enthusiasm += 0.3', text='We attack the sources and the motive. The story drags on.'),
 opt('surprise_silence', 'Ignore it and keep campaigning', fx='october_done = year; suburban_dem -= 3*(1-dissent); dem_enthusiasm -= 0.5; working_dem -= 1*(1-dissent)', text='We say nothing. The story grows in the vacuum.')], priority=260, max_visits=0)

# =============================================================================
# 2017 - 2020
# =============================================================================
ev('resistance', 'The Resistance', 'year = 2017 and month = 2 and dem_president = 0', """
Millions march in cities across the country the day after the inauguration. A new kind of opposition is born: decentralized, female-led, and furious.
""", [
 opt('resist_channel', 'Channel the energy into elections', fx='dem_enthusiasm += 1.2; civic_strength += 500; dem_legislatures += 0; progressive_strength += 2', text='We convert marches into volunteer lists, candidate recruitment, and voter registration.'),
 opt('resist_noncollab', 'Embrace total opposition', fx='dem_enthusiasm += 1.5; polarization += 2; progressive_dissent -= 4; moderate_dissent += 3; gopmod_relation -= 5', text='Our base cheers; bipartisan deals become harder.'),
 opt('resist_selective', 'Oppose selectively and legislate where we can', fx='moderate_strength += 2; gopmod_relation += 3; suburban_dem += 2*(1-dissent); progressive_dissent += 5; dem_enthusiasm += 0.3', text='We fight on the biggest issues and cut deals on others.')])

ev('repeal_fight', 'The Healthcare Repeal Fight', 'year = 2017 and month = 7 and dem_president = 0', """
Republicans in Congress are trying to repeal the Affordable Care Act, a bill that would take coverage away from millions. The vote in the Senate will be razor-thin.
""", [
 opt('repeal_mobilize', 'Mobilize patients and providers', fx='{!\nQ.civic_strength += 300; Q.dem_enthusiasm = Math.min(10, Q.dem_enthusiasm + 1);\nQ.uninsured -= 0.0;\nif (Q.maga_strength < 60) { Q.uninsured += 0; }\nQ.healthcare_agenda += 1; Q.working_dem += 2 * (1 - Q.dissent);\n!}', text='Town halls overflow. The repeal effort collapses by a single vote.'),
 opt('repeal_negotiate', 'Negotiate behind the scenes', fx='gopmod_relation += 4; moderate_strength += 2; progressive_dissent += 3; uninsured += 0.5', text='We trade quietly with moderates. The bill is softened.')])

ev('charlottesville', 'Charlottesville', 'year = 2017 and month = 8', """
Neo-Nazis and white supremacists have marched in Charlottesville, Virginia; a counter-protester has been killed by a car driven into the crowd. The country watches as the lines of acceptable politics are tested.
""", [
 opt('charlottesville_condemn', 'Demand universal condemnation', fx='pro_democracy += 1.5; polarization += 0.5; farright_strength -= 1; suburban_dem += 2*(1-dissent); minority_dem += 1*(1-dissent)', text='We insist that leaders of both parties condemn the marchers without qualification.'),
 opt('charlottesville_crackdown', 'Press for investigations of hate groups', fx='farright_strength -= 2.5; militia_strength -= 30; federal_law_loyalty += 0.01; press_freedom -= 0.5; progressive_dissent -= 2', text='Federal agencies are pressed to prioritize domestic extremism.'),
 opt('charlottesville_street', 'Back mass counter-protest', fx='directleft_strength += 10; civic_strength += 200; polarization += 1.5; farleft_strength += 1; young_dem += 2*(1-dissent); suburban_dem -= 1*(1-dissent)', text='Counter-protests grow, and so does the danger of confrontation.')])

ev('tax_and_budget_2017', 'Tax Cuts and the Budget', 'year = 2017 and month = 12 and dem_president = 0', """
Congressional Republicans are pushing through a sweeping tax cut. Critics say it favors the wealthy and balloons the deficit; supporters say it will boost investment.
""", [
 opt('tax_opposition', 'Unified opposition', fx='progressive_dissent -= 3; working_dem += 2*(1-dissent); suburban_dem += 1*(1-dissent); inequality += 1', text='We make inequality the center of our message.'),
 opt('tax_alternatives', 'Offer a middle-class alternative', fx='economic_plan = 1; working_dem += 3*(1-dissent); suburban_dem += 2*(1-dissent); moderate_strength += 1', text='Our counter-proposal gives credits to families and small businesses.')])

ev('parkland', 'Parkland', 'year = 2018 and month = 2', """
Seventeen students and teachers were killed in a school shooting in Parkland, Florida. The surviving students launch a national movement demanding action on guns.
""", [
 opt('parkland_back', 'Stand with the students', fx='young_dem += 4*(1-dissent); suburban_dem += 3*(1-dissent); rural_dem -= 1*(1-dissent); dem_enthusiasm += 0.8; polarization += 0.5', text='Student leaders become the faces of a new civic movement.'),
 opt('parkland_bipartisan', 'Seek a bipartisan compromise', fx='suburban_dem += 2*(1-dissent); gopmod_relation += 3; moderate_strength += 1; progressive_dissent += 2', text='A modest package of reforms passes at the state level.')])

ev('kavanaugh', 'A Supreme Court Confirmation Fight', 'year = 2018 and month = 10 and court_lean >= 0', """
A Supreme Court vacancy has produced a brutal confirmation fight, with allegations, hearings, and furious protests. The stakes: the Court\'s balance for a generation.
""", [
 opt('confirm_fight', 'Fight with everything we have', fx='dem_enthusiasm += 1; gop_enthusiasm += 1; polarization += 2; civic_strength += 200; progressive_dissent -= 3', text='We fight, and lose or win narrowly, and the country is more polarized than ever.'),
 opt('confirm_process', 'Insist on a fair, thorough process', fx='institutions += 1; gopmod_relation += 2; progressive_dissent += 3; dem_enthusiasm += 0.3; pro_democracy += 0.5', text='We press for a full investigation and restraint.')])

ev('shutdown_2018', 'A Government Shutdown', 'year = 2018 and month = 12 and dem_president = 0 and maga_strength >= 30', """
The government has partially shut down in a fight over border-wall funding. Hundreds of thousands of federal workers are unpaid.
""", [
 opt('shutdown_hold', 'Hold the line', fx='working_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); dem_enthusiasm += 0.5; progressive_dissent -= 2; polarization += 1', text='The public blames the president for the shutdown.'),
 opt('shutdown_deal', 'Seek a quick deal', fx='gopmod_relation += 3; moderate_strength += 1; progressive_dissent += 3; dem_enthusiasm -= 0.2', text='Federal workers return to work, with little to show for the fight.')])

ev('oversight_crisis', 'The Impeachment Question', 'year >= 2019 and month = 9 and dem_president = 0 and dem_house = 1 and maga_strength >= 35 and impeach_done != 1', """
With a Democratic House, serious allegations of abuse of power by the president have reached the point where Congress must decide: investigate, censure, or impeach.
""", [
 opt('impeach_go', 'Proceed with impeachment', fx='impeach_done = 1; institutions += 2; subversion_progress -= 0.5; dem_enthusiasm += 0.6; gop_enthusiasm += 1.2; polarization += 3; maga_strength += 1.5; suburban_dem += 1*(1-dissent)', text='The House impeaches; the Senate acquits along party lines. The country is, if anything, more divided.'),
 opt('impeach_hearings', 'Hold hearings but not impeach', fx='impeach_done = 1; institutions += 1; polarization += 1; moderate_strength += 1; progressive_dissent += 5; dem_enthusiasm -= 0.2', text='Our base feels abandoned; our moderates feel relief.'),
 opt('impeach_focus', 'Focus on the economy', fx='impeach_done = 1; working_dem += 3*(1-dissent); moderate_strength += 2; progressive_dissent += 6; subversion_progress += 0.3', text='We choose pocketbook politics over process. Critics say we shrank from our duty.')])

# =============================================================================
# 2020 - 2021: COVID and its aftermath
# =============================================================================
ev('covid_outbreak', 'The Coronavirus Pandemic', 'year = 2020 and month = 3', """
A novel coronavirus has reached the United States. Hospitals fill; schools and businesses close; the economy collapses almost overnight. It is the largest public health crisis in a century.

[? if dem_president = 1 : A Democratic administration is in charge of the response. The country will judge us on every decision. ?][? if dem_president = 0 : A Republican administration is responsible for the federal response. We have to decide how to oppose and how to help. ?]
""", [
 opt('covid_science', 'Follow the science: aggressive public health measures', fx="{!\nQ.pandemic = 1; Q.economic_growth = -7; Q.unemployed = Math.max(Q.unemployed, 11); Q.inflation = 0.6; Q.budget -= 2;\nQ.suburban_dem += 3 * (1 - Q.dissent); Q.educated_dem += 3 * (1 - Q.dissent); Q.rural_dem -= 2 * (1 - Q.dissent);\nQ.pro_democracy += 1; Q.polarization += 1; Q.covid_deaths_handled = 2;\n!}", text='We back strict measures and urge vaccine development. The country is deeply divided over masks and lockdowns.'),
 opt('covid_balance', 'Balance health and economy', fx="{!\nQ.pandemic = 1; Q.economic_growth = -6; Q.unemployed = Math.max(Q.unemployed, 10.5); Q.inflation = 0.7; Q.budget -= 2;\nQ.suburban_dem += 1 * (1 - Q.dissent); Q.working_dem += 1 * (1 - Q.dissent); Q.moderate_strength += 2; Q.covid_deaths_handled = 1;\n!}", text='We try to find a middle path. Neither side is satisfied.'),
 opt('covid_reopen', 'Prioritize reopening', fx="{!\nQ.pandemic = 1; Q.economic_growth = -5; Q.unemployed = Math.max(Q.unemployed, 10); Q.inflation = 0.8; Q.budget -= 2;\nQ.rural_dem += 2 * (1 - Q.dissent); Q.working_dem += 1 * (1 - Q.dissent); Q.suburban_dem -= 3 * (1 - Q.dissent); Q.progressive_dissent += 5; Q.covid_deaths_handled = 0;\n!}", text='We press for reopening. The recession is milder, the toll is heavier.')], priority=900)

ev('relief_package', 'The Relief Package', 'year = 2020 and month = 4', """
The economy is in free fall. Congress is negotiating a historic relief bill: direct payments, expanded unemployment insurance, and loans to business. How big should it be?
""", [
 opt('relief_huge', 'Go big', fx='stimulus_level += 2; economic_growth += 2.5; unemployed -= 0.8; budget -= 2; working_dem += 3*(1-dissent); progressive_dissent -= 3; inflation += 0.3', text='We back the largest relief effort in history. The recovery will be faster, and perhaps hotter.'),
 opt('relief_mid', 'A targeted package', fx='stimulus_level += 1; economic_growth += 1.5; unemployed -= 0.4; budget -= 1; moderate_strength += 2', text='A targeted package passes, with bipartisan support.'),
 opt('relief_small', 'Hold the line on spending', fx='economic_growth -= 0.5; unemployed += 0.4; budget += 1; progressive_dissent += 6; working_dem -= 2*(1-dissent); biz_relation += 2', text='We refuse to be spenders. Families face a long recovery.')], priority=500)

ev('george_floyd', 'The Killing of George Floyd', 'year = 2020 and month = 6', """
The killing of George Floyd by a police officer in Minneapolis has sparked the largest protests in American history, from small towns to big cities. Some protests turn to rioting and looting; the president threatens to deploy troops.
""", [
 opt('floyd_reform', 'Back reform and peaceful protest', fx='minority_dem += 4*(1-dissent); young_dem += 3*(1-dissent); suburban_dem += 1*(1-dissent); directleft_militancy -= 0.05; progressive_dissent -= 3; polarization += 1', text='We call for concrete reforms and condemn violence in the same breath.'),
 opt('floyd_defund', 'Embrace the most radical demands', fx='young_dem += 3*(1-dissent); minority_dem += 1*(1-dissent); suburban_dem -= 4*(1-dissent); working_dem -= 2*(1-dissent); progressive_dissent -= 6; moderate_dissent += 8; directleft_strength += 10; polarization += 2; gop_enthusiasm += 1', text='The slogan spreads faster than the policy. Opponents have a new weapon.'),
 opt('floyd_order', 'Stress law and order', fx='suburban_dem += 3*(1-dissent); working_dem += 2*(1-dissent); minority_dem -= 3*(1-dissent); young_dem -= 3*(1-dissent); progressive_dissent += 8; farleft_strength += 2; local_police_loyalty += 0.05', text='We prioritize safety. Our base accuses us of betrayal.')], priority=500)

ev('rbg_vacancy', 'A Vacancy on the Court', 'year = 2020 and month = 9', """
Justice Ruth Bader Ginsburg has died six weeks before the presidential election, and the question of who will fill her seat will shape the Court for a generation.

[? if dem_president = 0 and dem_senate = 0 : The Republican Senate says it will move quickly. ?][? if dem_president = 1 or dem_senate = 1 : We have the tools to shape the outcome. ?]
""", [
 opt('rbg_fight', 'Make the vacancy the campaign issue', fx='{!\nQ.dem_enthusiasm = Math.min(10, Q.dem_enthusiasm + 1);\nif (!Q.dem_president && !Q.dem_senate) { Q.court_lean += 1.5; }\nif (Q.dem_president || Q.dem_senate) { Q.court_lean -= 0.5; }\nQ.polarization += 1; Q.progressive_dissent -= 2;\n!}', text='The fight dominates the final weeks.'),
 opt('rbg_norms', 'Appeal to the Senate\'s precedent', fx='{!\nQ.institutions += 0.5; Q.gopmod_relation += 2; Q.progressive_dissent += 2;\nif (!Q.dem_president && !Q.dem_senate) { Q.court_lean += 1.5; }\n!}', text='We appeal to institutional memory. It matters less than we hoped.')], priority=400)

ev('election_dispute', 'The Loser Will Not Concede', 'pres_year = 1 and month = 12 and el_pres_winner == "D" and gop_nominee_type == "maga" and dispute_done != year and election_done = year', """
The Republican nominee has refused to concede defeat, alleging fraud without evidence, filing lawsuits, and pressuring state officials to overturn results. For the first time in modern American history, the peaceful transfer of power is in doubt.

[? if institutions >= 60 : State officials, courts, and the military have so far shown no appetite to go along. ?][? if institutions < 60 : The pressure is working on some institutions, and some officials are wavering. ?]
""", [
 opt('dispute_legal', 'Mobilize lawyers and state officials', fx="{!\nQ.dispute_done = Q.year;\nvar score = SD.resilience(Q) + 4;\nQ.dispute_score = Math.round(score);\nQ.dispute_ok = score >= 80 ? 1 : 0;\nif (Q.dispute_ok) { Q.institutions += 3; Q.subversion_progress = Math.max(0, Q.subversion_progress - 2); Q.maga_strength -= 2; Q.pro_democracy += 2; }\nelse { Q.institutions -= 20; Q.subversion_progress = 10; Q.game_lost = 1; }\n!}", text="[? if dispute_ok = 1 : Courts rule against every challenge; state officials certify results; lawyers swarm every courtroom. The dispute fails. ?][? if dispute_ok = 0 : The legal defenses prove too thin. State legislatures and officials buckle, and the election is overturned. ?]"),
 opt('dispute_public', 'Mobilize the public and pressure Republicans', fx="{!\nQ.dispute_done = Q.year;\nvar score = SD.resilience(Q) + Math.min(Q.civic_strength, 3000) / 3000 * 6 + 0.02 * Q.pro_democracy;\nQ.dispute_score = Math.round(score);\nQ.dispute_ok = score >= 80 ? 1 : 0;\nif (Q.dispute_ok) { Q.institutions += 2; Q.civic_strength += 400; Q.subversion_progress = Math.max(0, Q.subversion_progress - 2); Q.maga_strength -= 1; Q.pro_democracy += 3; Q.polarization += 1; }\nelse { Q.institutions -= 20; Q.subversion_progress = 10; Q.game_lost = 1; }\n!}", text="[? if dispute_ok = 1 : Millions fill the streets peacefully, and Republican officials one by one refuse to join the scheme. ?][? if dispute_ok = 0 : The protests are large but the pressure points hold. The scheme succeeds. ?]"),
 opt('dispute_quiet', 'Negotiate quietly with party leaders', fx="{!\nQ.dispute_done = Q.year;\nvar score = SD.resilience(Q) + Q.gopmod_relation * 0.08;\nQ.dispute_score = Math.round(score);\nQ.dispute_ok = score >= 80 ? 1 : 0;\nif (Q.dispute_ok) { Q.institutions += 1; Q.subversion_progress = Math.max(0, Q.subversion_progress - 1); Q.gopmod_relation += 4; }\nelse { Q.institutions -= 20; Q.subversion_progress = 10; Q.game_lost = 1; }\n!}", text="[? if dispute_ok = 1 : Republican leaders, privately, make clear that the end is near. The transfer will proceed. ?][? if dispute_ok = 0 : The quiet approach is too slow. Events move faster than conversations. ?]")], priority=850, max_visits=0)

ev('capitol_attack', 'The Capitol Under Siege', 'year >= 2021 and month = 1 and dispute_done = prev_year and dispute_ok = 1 and capitol_done != year', """
On the day Congress meets to certify the election, an angry crowd stirred by claims of fraud storms the Capitol. Lawmakers flee. Police are overwhelmed. Hours later, order is restored and Congress completes its task.

Whatever the verdict of the courts, history will remember the day American democracy came closer to the edge than at any time in generations.
""", [
 opt('capitol_commission', 'Demand a full independent investigation', fx='capitol_done = year; institutions += 3; pro_democracy += 3; polarization += 2; maga_strength -= 3; farright_strength -= 2; militia_strength -= 60; gopmod_relation -= 3', text='A bipartisan commission is stymied; yet the investigation goes ahead and documents what happened.'),
 opt('capitol_prosecute', 'Support prosecution of those responsible', fx='capitol_done = year; institutions += 2; farright_strength -= 3; militia_strength -= 80; federal_law_loyalty += 0.03; polarization += 1; pro_democracy += 2', text='Hundreds of rioters face charges, with sentences that hit militia networks hard.'),
 opt('capitol_move_on', 'Move on to the legislative agenda', fx='capitol_done = year; working_dem += 2*(1-dissent); moderate_strength += 2; progressive_dissent += 4; institutions -= 1; pro_democracy -= 1', text='We want to turn the page, but the page does not turn.')], priority=840, max_visits=0)

ev('american_rescue', 'Recovery Legislation', 'year = 2021 and month = 3 and dem_president = 1 and dem_house = 1 and dem_senate = 1', """
With unified control we can pass a major recovery package using the budget reconciliation process. The economy is still recovering and the virus is not yet beaten.
""", [
 opt('rescue_big', 'A huge package ($1.9 trillion)', fx='stimulus_level += 2; economic_growth += 2; unemployed -= 0.8; inflation += 1; budget -= 2; working_dem += 3*(1-dissent); progressive_dissent -= 3; moderate_dissent += 2', text='Checks go out and the child tax credit expands. The economy booms, and prices begin to climb.'),
 opt('rescue_mid', 'A moderate package', fx='stimulus_level += 1; economic_growth += 1; unemployed -= 0.4; inflation += 0.3; budget -= 1; moderate_strength += 2; progressive_dissent += 2', text='A smaller package passes with a bipartisan flavor.'),
 opt('rescue_small', 'A targeted, minimal bill', fx='economic_growth += 0.3; budget += 1; progressive_dissent += 6; working_dem -= 1*(1-dissent)', text='We pare back. The recovery is slow.')], priority=500)

ev('afghanistan', 'The Fall of Kabul', 'year = 2021 and month = 8', """
The Taliban have swept into Kabul as American forces complete their withdrawal. Chaotic images of evacuations at the airport dominate the news.

[? if dem_president = 1 : The administration takes the blame. ?][? if dem_president = 0 : The Republican administration\'s earlier agreements are under scrutiny. ?]
""", [
 opt('afghan_owned', 'Defend ending the forever war', fx='progressive_strength += 2; moderate_dissent += 2; intl_relation -= 3; working_dem += 1*(1-dissent)', text='We argue it was time to end America\'s longest war, regardless of how it ended.'),
 opt('afghan_accountability', 'Demand accountability and help evacuees', fx='intl_relation += 2; moderate_strength += 2; military_loyalty += 0.02; progressive_dissent += 3; suburban_dem += 1*(1-dissent)', text='We insist on a full accounting and aid for those left behind.')])

ev('infrastructure', 'The Infrastructure Bill', 'year = 2021 and month = 11 and dem_president = 1 and dem_senate = 1', """
A bipartisan infrastructure bill awaits a vote, while a much bigger social-spending package is stalled by moderate senators. Progressives want to hold the first hostage to the second.
""", [
 opt('infra_pass', 'Pass infrastructure now', fx='budget -= 1; economic_growth += 0.4; abundance_strength += 2; gopmod_relation += 4; progressive_dissent += 5; working_dem += 2*(1-dissent); institutions += 1', text='The bipartisan bill becomes law; roads, bridges, and broadband get funded.'),
 opt('infra_hostage', 'Hold it until the bigger bill passes', fx='progressive_dissent -= 4; moderate_dissent += 6; gopmod_relation -= 4; working_dem -= 1*(1-dissent); polarization += 1; budget -= 0', text='Weeks of brinkmanship follow; both bills end up in trouble.')])

# =============================================================================
# 2022 - 2026
# =============================================================================
ev('ukraine_war', 'Russia Invades Ukraine', 'year = 2022 and month = 3', """
Russia has launched a full-scale invasion of Ukraine, the largest war in Europe since 1945. Energy and food prices spike; the West debates how far to go.
""", [
 opt('ukraine_support', 'Lead a coalition in support of Ukraine', fx='intl_relation += 8; moderate_strength += 2; inflation += 0.5; progressive_dissent += 2; maga_strength += 0.5', text='We back sanctions and arms. NATO unity is strengthened.'),
 opt('ukraine_limits', 'Support Ukraine, with limits', fx='intl_relation += 3; moderate_strength += 1; progressive_dissent += 0; populist_strength += 1', text='We help Ukraine while ruling out direct US involvement.'),
 opt('ukraine_negotiate', 'Push for negotiations', fx='progressive_strength += 2; intl_relation -= 4; moderate_dissent += 4; populist_strength += 1', text='We press for a settlement. Allies are alarmed.')])

ev('inflation_peak', 'Inflation Peaks', 'year = 2022 and month = 6', """
Prices are rising at their fastest pace in forty years. Voters say the economy is their top concern.

[? if stimulus_level >= 3 : Critics blame the scale of recent spending. ?][? if stimulus_level < 3 : Critics blame supply chains and war. ?]
""", [
 opt('inflation_fight', 'Support aggressive action to fight inflation', fx='{!\nQ.inflation += 3 + Math.max(0, Q.stimulus_level - 1); Q.economic_growth -= 1.5; Q.unemployed += 0.3; Q.suburban_dem += 1 * (1 - Q.dissent); Q.progressive_dissent += 2;\n!}', text='The Federal Reserve raises rates; inflation begins to cool; so does growth.'),
 opt('inflation_prices', 'Target prices directly', fx='{!\nQ.inflation += 2.2 + Math.max(0, Q.stimulus_level - 1) * 0.7; Q.economic_growth -= 0.5; Q.working_dem += 2 * (1 - Q.dissent); Q.biz_relation -= 3; Q.populist_strength += 2;\n!}', text='We go after corporate pricing power and supply chain bottlenecks.'),
 opt('inflation_blame', 'Blame the war and companies', fx='{!\nQ.inflation += 3.8 + Math.max(0, Q.stimulus_level - 1); Q.working_dem -= 2 * (1 - Q.dissent); Q.suburban_dem -= 2 * (1 - Q.dissent); Q.polarization += 1;\n!}', text='Voters are unimpressed by excuses.')], priority=400)

ev('abortion_ruling', 'The Court Rules on Abortion', 'year = 2022 and month = 6', """
[? if court_lean >= 1 : The Supreme Court has overturned Roe v. Wade, ending the constitutional right to abortion and sending the issue to the states. ?][? if court_lean < 1 : The Supreme Court has upheld abortion rights in a major ruling that nevertheless leaves much unsettled. ?]
""", [
 opt('abortion_codify', 'Make it a central issue', fx='{!\nif (Q.court_lean >= 1) { Q.dem_enthusiasm = Math.min(10, Q.dem_enthusiasm + 1.5); Q.suburban_dem += 4 * (1 - Q.dissent); Q.young_dem += 3 * (1 - Q.dissent); Q.educated_dem += 2 * (1 - Q.dissent); Q.gop_enthusiasm = Math.min(10, Q.gop_enthusiasm + 0.5); }\nelse { Q.suburban_dem += 1 * (1 - Q.dissent); Q.polarization += 0.5; }\nQ.progressive_dissent -= 3;\n!}', text='Abortion rights ballot measures win in state after state.'),
 opt('abortion_moderate', 'Frame it around freedom and privacy', fx='{!\nif (Q.court_lean >= 1) { Q.dem_enthusiasm = Math.min(10, Q.dem_enthusiasm + 1); Q.suburban_dem += 3 * (1 - Q.dissent); Q.rural_dem += 1 * (1 - Q.dissent); }\nQ.moderate_strength += 1; Q.progressive_dissent += 1;\n!}', text='A messaging approach that appeals beyond our base.')], priority=300)

ev('climate_law', 'The Climate and Healthcare Bill', 'year = 2022 and month = 8 and dem_president = 1 and dem_house = 1 and dem_senate = 1', """
A scaled-down version of our agenda is within reach: climate investment, healthcare cost reductions, and a minimum tax on large corporations.
""", [
 opt('climate_pass', 'Pass it', fx='climate_progress += 3; budget += 1; abundance_strength += 2; young_dem += 2*(1-dissent); progressive_dissent -= 3; inflation -= 0.3; healthcare_agenda += 1', text='The law passes narrowly. It is smaller than we wanted, but historic.'),
 opt('climate_hold', 'Hold out for more', fx='progressive_dissent -= 1; moderate_dissent += 3; budget -= 0; polarization += 1', text='The window may close.')], priority=300)

ev('debt_ceiling', 'The Debt Ceiling Standoff', 'year = 2023 and month = 5 and dem_president = 1 and dem_house = 0', """
Republicans in the House are threatening default unless we accept deep spending cuts. Markets are nervous; time is running out.
""", [
 opt('debt_negotiate', 'Negotiate a deal', fx='budget += 2; economic_growth -= 0.2; progressive_dissent += 5; gopmod_relation += 3; institutions += 1', text='A deal averts default, with cuts we dislike.'),
 opt('debt_stand', 'Refuse to negotiate over the debt limit', fx='polarization += 2; biz_relation -= 3; institutions += 0; economic_growth -= 0.8; progressive_dissent -= 2; moderate_dissent += 3', text='We refuse. The brinkmanship is terrifying, and the outcome is uncertain.')])

ev('bank_failures', 'Bank Failures', 'year = 2023 and month = 3', """
Silicon Valley Bank and other regional lenders have collapsed, and depositors are panicking. Regulators have to decide whether to guarantee deposits.
""", [
 opt('bank_backstop', 'Back a broad deposit guarantee', fx='budget -= 1; biz_relation += 3; economic_growth += 0.2; progressive_dissent += 3; populist_dissent += 3', text='Panic ebbs, to the fury of populists on both sides.'),
 opt('bank_reform', 'Demand tougher bank regulation', fx='biz_relation -= 4; progressive_dissent -= 3; populist_strength += 2; economic_growth -= 0.1', text='We introduce a tough regulatory package.')])

ev('gaza_war', 'War in Gaza', 'year = 2023 and month = 10', """
Hamas has attacked Israel on October 7, killing some 1,200 people, and Israel has launched a devastating war in Gaza. American politics is torn: Jewish and Arab-American communities, the young, and the progressive base, and a majority of Americans, want different things.
""", [
 opt('gaza_israel', 'Stand firmly with Israel', fx='moderate_strength += 2; intl_relation += 2; left_relation -= 10; farleft_strength += 3; young_dem -= 4*(1-dissent); minority_dem -= 2*(1-dissent); progressive_dissent += 8', text='Support for Israel remains our official line; protests spread on campuses and the movement against us grows.'),
 opt('gaza_ceasefire', 'Push for a ceasefire and humanitarian aid', fx='left_relation += 4; farleft_strength -= 0.5; young_dem += 1*(1-dissent); progressive_dissent += 0; moderate_dissent += 4; intl_relation -= 2', text='We press for a ceasefire. Allies and critics are both unhappy.'),
 opt('gaza_conditional', 'Condition military aid', fx='left_relation += 7; farleft_strength -= 1.5; progressive_dissent -= 4; moderate_dissent += 6; intl_relation -= 4; young_dem += 2*(1-dissent)', text='We demand conditions on aid; the old guard is furious.')], priority=300)

ev('political_violence', 'Political Violence', 'year >= 2019 and (farright_strength >= 15 or farleft_strength >= 25 or maga_strength >= 50) and violence_done != 1', """
A wave of political violence has broken out: threats against election workers and judges, attacks on politicians, and clashes at protests. Experts warn the country is entering a dangerous new phase.
""", [
 opt('violence_condemn', 'Condemn violence from every side', fx='violence_done = 1; polarization -= 1.5; pro_democracy += 2; farright_strength -= 1; farleft_strength -= 0.5; institutions += 1', text='A rare moment of cross-party agreement offers hope.'),
 opt('violence_security', 'Increase security for officials and election workers', fx='violence_done = 1; budget -= 1; election_admin += 4; institutions += 1; federal_law_loyalty += 0.02', text='Protection of the people who run democracy becomes a priority.', choose='budget >= 1', unavail='Need 1 budget.'),
 opt('violence_blame', 'Blame the other side', fx='violence_done = 1; polarization += 3; dem_enthusiasm += 0.5; gop_enthusiasm += 0.8; farright_strength += 1.5', text='Rhetoric worsens, with predictable results.')], priority=350)

ev('trade_war', 'Tariffs and Trade War', 'year >= 2025 and month = 4 and dem_president = 0 and president == maga_leader and tariffs_done != 1', """
The Republican administration has launched a sweeping tariff offensive against allies and adversaries alike. Markets shudder, prices rise, and farmers and manufacturers brace for retaliation.
""", [
 opt('tariff_oppose', 'Oppose the tariffs and defend consumers', fx='tariffs_done = 1; economic_growth -= 1; inflation += 1; unemployed += 0.3; working_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); intl_relation += 3; biz_relation += 3', text='Polling shows tariffs unpopular; the economy slows.'),
 opt('tariff_selective', 'Support targeted tariffs, oppose chaos', fx='tariffs_done = 1; economic_growth -= 0.8; inflation += 0.8; working_dem += 2*(1-dissent); rural_dem += 1*(1-dissent); populist_strength += 2; abundance_dissent += 3', text='A nuanced position, which gets less attention than the slogans.')], priority=350)

ev('shutdown_2025', 'The Longest Shutdown', 'year >= 2025 and month = 10 and dem_president = 0 and shutdown_done != 1', """
The federal government has shut down in a fight over spending and health-care subsidies. Federal workers go unpaid, air travel is disrupted, and food benefits are in doubt.
""", [
 opt('shutdown_hold_firm', 'Hold firm on healthcare', fx='shutdown_done = 1; healthcare_agenda += 1; dem_enthusiasm += 0.8; progressive_dissent -= 4; moderate_dissent += 3; working_dem += 2*(1-dissent)', text='We refuse to cave. The standoff drags on for weeks.'),
 opt('shutdown_cave', 'Reopen the government', fx='shutdown_done = 1; progressive_dissent += 7; dem_enthusiasm -= 0.8; moderate_strength += 1', text='We reopen the government with promises of a vote later. Our base is furious.')], priority=300)

ev('ai_boom', 'The Artificial Intelligence Boom', 'year >= 2024 and month = 3 and ai_done != 1', """
Artificial intelligence is transforming the economy: soaring valuations, concerns for white-collar jobs, an arms race for data centers, and a flood of synthetic media.
""", [
 opt('ai_growth', 'Embrace the opportunity', fx='ai_done = 1; economic_growth += 0.6; abundance_strength += 3; progressive_dissent += 3; inequality += 2; educated_dem += 1*(1-dissent)', text='The boom lifts growth and stock portfolios; inequality grows too.'),
 opt('ai_guardrail', 'Impose guardrails and protect workers', fx='ai_done = 1; economic_growth -= 0.1; working_dem += 3*(1-dissent); young_dem += 1*(1-dissent); abundance_dissent += 4; biz_relation -= 2; inequality -= 1', text='We pair innovation with protections for workers and citizens.'),
 opt('ai_ignore', 'Leave it to the market', fx='ai_done = 1; polarization += 1; pro_democracy -= 1; press_freedom -= 2', text='Synthetic media floods the public square.')], priority=100)

ev('offyear_2025', 'The 2025 Off-Year Elections', 'year = 2025 and month = 11 and dem_president = 0', """
Voters in several states and cities have gone to the polls in off-year elections, a first test of the new political climate.

[? if dem_enthusiasm >= 6 : The results are strong for the Democrats. ?][? if dem_enthusiasm < 6 and dem_enthusiasm >= 4 : The results are mixed. ?][? if dem_enthusiasm < 4 : The results are poor for the Democrats. ?]
""", [
 opt('offyear_message', 'Draw lessons and double down', fx='dem_enthusiasm += 0.3; resources += 1', text='The party takes the results as a sign.')], priority=200)

ev('midterm_run_up', 'The Final Midterm Stretch', 'year = 2026 and month = 1', """
The 2026 midterm elections are ten months away. The next ten months will define how the story of this era ends.
""", [
 opt('final_all_in', 'All in on turnout', fx='dem_enthusiasm += 0.6; civic_strength += 200; resources -= 0', text='We commit everything to the final push.'),
 opt('final_bridge', 'Broaden the coalition', fx='suburban_dem += 2*(1-dissent); rural_dem += 2*(1-dissent); moderate_strength += 2; progressive_dissent += 2', text='We aim for persuasion over mobilization.')], priority=100)

# =============================================================================
# DYNAMIC
# =============================================================================
ev('abundance_emerges', 'A New Faction: Abundance', 'year >= 2019 and abundance_discovered = 0 and economic_growth >= 0 and month = 5', """
A group of younger policy thinkers, housing advocates, and technologists inside the party argue that the left has become too good at saying no. They want a politics of building: housing, transit, clean power, and a government that works.

The faction is small now, but it is attracting talent and money.
""", [
 opt('abundance_welcome', 'Welcome the new wing', fx='abundance_discovered = 1; abundance_strength += 6; abundance_dissent -= 5; progressive_dissent += 2', text='A new tent in the big tent opens.'),
 opt('abundance_ignore', 'Treat it as a fad', fx='abundance_discovered = 1; abundance_dissent += 5', text='The new wing grows resentful, but grows nonetheless.')], priority=150)

ev('populist_emerges', 'A New Faction: Economic Populists', 'year >= 2016 and populist_discovered = 0 and rural_dem < 17 and month = 9', """
Rust Belt and rural officials argue that the party has lost touch with the places it once represented. They want a message about jobs, trade, and dignity, with less cultural scolding.

A faction of populists is taking shape.
""", [
 opt('populist_welcome', 'Give them a platform', fx='populist_discovered = 1; populist_strength += 6; populist_dissent -= 5; progressive_dissent += 2; working_dem += 1*(1-dissent); rural_dem += 1*(1-dissent)', text='Voices from the heartland get a bigger megaphone.'),
 opt('populist_ignore', 'Hold the line', fx='populist_discovered = 1; populist_dissent += 6', text='The populist caucus grows restive.')], priority=150)

ev('party_revolt', 'The Party in Revolt', 'dissent_percent >= 28 and month >= 1 and revolt_cooldown <= 0', """
Factional resentments have reached the breaking point. Leaders of several factions are airing grievances in public, donors are nervous, and the base is confused. Something must be done.
""", [
 opt('revolt_concede', 'Concede policy demands', fx='revolt_cooldown = 18; progressive_dissent -= 6; moderate_dissent -= 6; labor_dissent -= 6; populist_dissent -= 6; abundance_dissent -= 6; establishment_dissent -= 6; budget -= 1', text='We buy peace by promising more than we can deliver.'),
 opt('revolt_unity', 'Make a high-profile unity push', fx='revolt_cooldown = 18; progressive_dissent -= 4; moderate_dissent -= 4; labor_dissent -= 4; populist_dissent -= 4; abundance_dissent -= 4; establishment_dissent -= 4; resources -= 1', text='A summit and a joint statement calm the waters.', choose='resources >= 1', unavail='Need 1 resource.'),
 opt('revolt_purge', 'Reassert central control', fx='revolt_cooldown = 18; establishment_strength += 6; establishment_dissent -= 10; progressive_dissent += 6; moderate_dissent += 4; left_relation -= 6; dem_enthusiasm -= 0.6', text='Order returns, at a price.')], priority=450, max_visits=0)

ev('left_split', 'The Left Breaks Away', 'year >= 2015 and farleft_strength >= 22 and left_relation < 40 and left_split_done != 1', """
A coalition of left activists, disillusioned young voters, and third-party organizers is launching a challenge to our right flank, a candidate and a ballot line that could cost us close races.
""", [
 opt('left_split_negotiate', 'Negotiate a pact', fx='left_split_done = 1; left_relation += 12; farleft_strength -= 6; progressive_dissent -= 4; moderate_dissent += 4; biz_relation -= 2', text='A deal brings many back to the fold.'),
 opt('left_split_attack', 'Treat them as spoilers', fx='left_split_done = 1; left_relation -= 6; farleft_strength += 3; suburban_dem += 1*(1-dissent); progressive_dissent += 4', text='We call them spoilers. They call us sellouts.'),
 opt('left_split_ignore', 'Ignore them', fx='left_split_done = 1; farleft_strength += 2; young_dem -= 2*(1-dissent)', text='We hope they fade away.')], priority=350)

ev('militia_surge', 'The Militia Threat', 'year >= 2016 and farright_strength >= 18 and militia_done != 1', """
Armed militias, sometimes in uniform, show up at protests, state capitols, and polling places. Their numbers are small but growing, and some officials are tolerating them.
""", [
 opt('militia_ban', 'Demand the law be enforced', fx='militia_done = 1; farright_strength -= 4; militia_strength -= 100; federal_law_loyalty += 0.02; polarization += 1; maga_strength -= 1', text='Prosecutors move; militia numbers fall.'),
 opt('militia_civic', 'Build a civic counterweight', fx='militia_done = 1; civic_strength += 600; election_admin += 3; dem_enthusiasm += 0.3; radicalization += 1', text='Volunteers organize to protect polling places and officials.'),
 opt('militia_shrug', 'Downplay it', fx='militia_done = 1; farright_strength += 2; militia_strength += 60; pro_democracy -= 2', text='Downplaying the threat does nothing to reduce it.')], priority=350)

ev('power_grab', 'A Test of the Guardrails', 'not (dem_president = 1) and president == maga_leader and institutions < 70 and power_grab_done < 3 and month = 6 and power_grab_year != year', """
The Republican administration is testing the limits of executive power: firing independent officials, defying judicial orders, and threatening critics. The guardrails of American democracy are being tested daily.
""", [
 opt('grab_courts', 'Fight in the courts', fx='power_grab_done += 1; institutions += 2; courts_independence += 2; maga_strength += 0.5; resources -= 0', text='Lawsuits pile up. Some win; some drag.'),
 opt('grab_streets', 'Fight in the streets and at the ballot box', fx='power_grab_done += 1; civic_strength += 500; dem_enthusiasm += 1; polarization += 1; institutions += 1', text='Mass mobilization sends a warning.'),
 opt('grab_coalition', 'Build a bipartisan coalition for the rule of law', fx='power_grab_done += 1; gopmod_relation += 6; institutions += 3; pro_democracy += 2; progressive_dissent += 3', text='A handful of Republicans, business leaders, and judges join the effort.'),
 opt('grab_wait', 'Wait for the next election', fx='power_grab_done += 1; institutions -= 4; pro_democracy -= 2; subversion_progress += 0.5', text='We do not fight, and the guardrails weaken.')], fx='power_grab_year = year', priority=380, max_visits=0)

ev('subversion_crisis', 'The Crisis of the Republic', 'subversion_progress >= 9.9 and subversion_done != 1', """
The movement to subvert the democratic order has reached a critical mass: officials loyal to a leader rather than to the Constitution have been installed, courts are being defied, and elections are being undermined.

Everything we have built (or failed to build) will now be tested.
""", [
 opt('crisis_all_in', 'Mobilize every resource at our disposal', fx="{!\nQ.subversion_done = 1;\nvar score = SD.resilience(Q) + 5;\nQ.dispute_score = Math.round(score);\nQ.dispute_ok = score >= 80 ? 1 : 0;\nif (Q.dispute_ok) { Q.subversion_progress = 3; Q.institutions += 5; Q.maga_strength -= 6; Q.pro_democracy += 4; }\nelse { Q.game_lost = 1; Q.institutions = 8; }\n!}", text="[? if dispute_ok = 1 : The republic holds. Civil society, courts, and a handful of principled officials hold the line. ?][? if dispute_ok = 0 : The republic falters. The guardrails fail. ?]", choose='resources >= 0'),
 opt('crisis_negotiate', 'Seek a political settlement', fx="{!\nQ.subversion_done = 1;\nvar score = SD.resilience(Q) + Q.gopmod_relation * 0.08;\nQ.dispute_score = Math.round(score);\nQ.dispute_ok = score >= 80 ? 1 : 0;\nif (Q.dispute_ok) { Q.subversion_progress = 4; Q.institutions += 3; Q.gopmod_relation += 5; }\nelse { Q.game_lost = 1; Q.institutions = 8; }\n!}", text="[? if dispute_ok = 1 : A fragile settlement is reached. The danger recedes, for now. ?][? if dispute_ok = 0 : The settlement is a surrender. ?]")], priority=870)

ev('inflation_backlash', 'The Cost-of-Living Backlash', 'inflation >= 5.5 and dem_president = 1 and backlash_done != 1 and year >= 2021', """
Prices are eating into paychecks. Polls show the voters are blaming the party in power. The next election looks grim.
""", [
 opt('backlash_message', 'Tell voters about the real gains', fx='backlash_done = 1; working_dem -= 1*(1-dissent); dem_enthusiasm -= 0.3', text='Many voters think we are out of touch.'),
 opt('backlash_policy', 'Pivot to cost-of-living policies', fx='backlash_done = 1; working_dem += 2*(1-dissent); suburban_dem += 1*(1-dissent); populist_strength += 2; budget -= 0', text='We announce policies on housing, groceries, and healthcare costs.'),
 opt('backlash_blame', 'Blame corporate greed', fx='backlash_done = 1; working_dem += 1*(1-dissent); biz_relation -= 4; populist_strength += 2; progressive_dissent -= 2', text='A populist message resonates with some.')], priority=250, max_visits=0)

# =============================================================================
# COLLAPSE and ENDING
# =============================================================================
ev('collapse', 'The End of the Republic', 'game_lost = 1 and game_over != 1', """
The democratic order has failed. [? if dispute_ok = 0 : The attempt to overturn the will of the voters succeeded. ?][? if dispute_ok != 0 : Year after year, the guardrails were stripped away until nothing remained to hold. ?]

Elections still take place, but they no longer decide who governs. The courts, the press, and the civil service have been hollowed out. The opposition is surveilled, prosecuted, and divided.

This is how democracies die: not in a single moment, but through a sequence of choices, many of which seemed reasonable at the time.
""", go_to='game_over', priority=1000, subtitle='Game over')

ev('ending', 'December 2026', 'ending_due = 1 and game_over != 1', """
The calendar has turned to a new year. The era that began in January 2014 is over; what comes next has yet to be written.

Americans will judge you on whether democracy survived, whether the coalition held together, and whether the country was left better, or worse, than you found it.
""", go_to='game_over', priority=990, subtitle='The final reckoning')
print('events written')
