from dry import *

FAC = [('progressive', 'Progressives', '#2a9d3a'), ('establishment', 'Establishment', '#1a5fb4'), ('labor', 'Labor', '#c64600'),
       ('moderate', 'Moderates', '#5e5c64'), ('abundance', 'Abundance', '#9141ac'), ('populist', 'Populists', '#a51d2d')]

fac_lines = []
for f, name, col in FAC:
    cond = ''
    if f == 'abundance': cond = '[? if abundance_discovered : '
    if f == 'populist': cond = '[? if populist_discovered : '
    end = ' ?]' if cond else ''
    fac_lines.append('%s<span style="color: %s;">**%s**</span>: strength [+ %s_strength_r +]%%, dissent [+ %s_dissent_r +]%s' % (cond, col, name, f, f, end))

status = """title: Status
new-page: true
is-special: true

= Status

[+ month : month +] [+ year +]

Resources available: [+ resources +] | Annual dues: [+ dues +] | Budget room: [+ budget_r +]

President: **[+ president +]** ([? if dem_president = 1 : <span style="color: #1a5fb4;">**D**</span> ?][? if dem_president = 0 : <span style="color: #c01c28;">**R**</span> ?]), term [+ president_terms +]

House: [+ house_dem +] D - [+ house_gop +] R ([? if dem_house = 1 : <span style="color: #1a5fb4;">**we control**</span> ?][? if dem_house = 0 : opposition-controlled ?]). Senate: [+ senate_dem +] D - [+ senate_gop +] R ([? if dem_senate = 1 : <span style="color: #1a5fb4;">**we control**</span> ?][? if dem_senate = 0 : opposition-controlled ?]).

Democratic governors: [+ dem_governors_r +] of 50. State legislatures: [+ dem_legislatures_r +].

Next election: November [+ next_election_year +], in [+ months_to_election +] months.

Party dissent: [+ dissent_percent_r +]%

""" + '\n\n'.join(fac_lines) + """

Economy: unemployment [+ unemployed_2 +]%, inflation [+ inflation_2 +]%, growth [+ economic_growth_2 +]%

Democratic health index: [+ democracy_score_r +] / 100 (institutions [+ institutions_r +], civic culture [+ pro_democracy_r +])

@emergency
title: Emergency
new-page: true

= Emergency

There is currently no emergency.

@politics
title: Politics
new-page: true

= Politics

**Relations**

Republican moderates: [+ gopmod_relation_r +] ([+ gopmod_relation : relationships +])

The organized left: [+ left_relation_r +] ([+ left_relation : relationships +])

Business community: [+ biz_relation_r +] ([+ biz_relation : relationships +])

Labor unions: [+ labor_relation_r +] ([+ labor_relation : relationships +])

Allies abroad: [+ intl_relation_r +] ([+ intl_relation : relationships +])

**Enthusiasm**

Democrats: [+ dem_enthusiasm_r +] / 10. Republicans: [+ gop_enthusiasm_r +] / 10.

**Rules of the game**

Voting rights reform level: [+ voting_rights +]. Court reform: [+ court_reform +]. Ethics reform: [+ ethics_reform +]. Filibuster reform: [+ filibuster_reform +]. Partisan gerrymander bias against us: [+ gerrymander_bias_r +] points.

**Public opinion**

Polarization: [+ polarization_r +] / 100. Press freedom: [+ press_freedom_r +]. Election administration integrity: [+ election_admin_r +]. Judicial independence: [+ courts_independence_r +].

@paramilitaries
title: Forces
new-page: true

= Forces

**Civil society mobilization**: Our network of volunteers, unions, and community groups is about [+ civic_strength_r +] strong.

**Right-wing militias**: about [+ militia_strength_r +] members. Street extremists: [+ streetright_strength_r +].

**Direct-action left**: about [+ directleft_strength_r +] activists.

**The institutions**

Military loyalty to the Constitution: [+ military_loyalty_r +]%

Federal law enforcement independence: [+ federal_law_loyalty_r +]%

Local police: [+ local_police_loyalty_r +]% reliable

@polls
title: Polls
new-page: true

= Polls

*If an election were held now ([? if midterm_year = 1 : midterm turnout ?][? if midterm_year = 0 : presidential-year turnout ?] assumed):*

Popular vote: <span style="color: #1a5fb4;">**Democrats**</span> [+ dem_votes_d +]%, <span style="color: #c01c28;">**Republicans**</span> [+ gop_votes_d +]%, left parties [+ left_votes +]%, far right [+ farright_votes +]%. Turnout: [+ turnout +]%.

Presidential projection: Democrats [+ dem_ev_proj_r +] electoral votes, Republicans [+ gop_ev_proj_r +].

Battleground leans (Democratic lead, points): Industrial Midwest [+ rust_belt_margin +], Florida/Ohio/Iowa [+ heartland_swing_margin +], Sun Belt [+ sun_belt_margin +].

Congress projection: House Democrats [+ house_proj_r +] seats. Senate Democrats [+ senate_proj_r +].

**Demographic support (the share of each group voting each way, normalized, before turnout adjustments)**

Working-class voters: D [+ working_dem_n +]  R [+ working_gop_n +]. Suburbanites: D [+ suburban_dem_n +]  R [+ suburban_gop_n +]. College-educated: D [+ educated_dem_n +]  R [+ educated_gop_n +]. Rural: D [+ rural_dem_n +]  R [+ rural_gop_n +]. Minority communities: D [+ minority_dem_n +]  R [+ minority_gop_n +]. Young voters: D [+ young_dem_n +]  R [+ young_gop_n +].
"""
write('scenes/status.scene.dry', status)

# round group values for the polls tab through a tiny on-arrival (status tab arrival)
write('scenes/status_right.scene.dry', """title: Opposition
new-page: true
is-special: true

= Opposition

**The Republican Party**

[? if maga_strength >= 55 : <span style="color: #b5651d;">**MAGA**</span> controls the party. ?][? if maga_strength >= 35 and maga_strength < 55 : <span style="color: #b5651d;">**MAGA**</span> and the establishment are at war for control. ?][? if maga_strength < 35 : The establishment is in charge, with the insurgents on the fringes. ?]

Movement strength: [+ maga_strength_r +] / 100. Establishment grip: [+ gop_establishment_r +].

[? if trump_active = 1 : Insurgent leader: **[+ maga_leader +]** ?][? if gop_nominee_type == "maga" : (the party\'s latest presidential nominee) ?]

**Threat to the republic**

Subversion progress: [+ subversion_progress_r +] / 10

Your sense of urgency about the threat: [+ trump_urgency +]

**Far-left movements**

Strength: [+ farleft_strength_r +]. Our relations with the organized left: [+ left_relation_r +].

**Far-right extremism**

Strength: [+ farright_strength_r +].
""")

LIB = """title: The Library
new-page: true
is-special: true
go-to: menu

= The Library

Herein is background on how American politics works in this game.

@menu

- @government: The American system of government
- @demographics: Demographic groups
- @factions: Factions inside the Democratic Party
- @opposition: Opponents of democracy
- @elections: How elections work in this game
- @tips: Tips
- @backSpecialScene: Exit library.

@government
go-to: menu

The United States is a federal presidential republic. The **President** is elected every four years by the **Electoral College**; the 435-seat **House of Representatives** is elected every two years; the 100-seat **Senate** has six-year terms staggered in thirds. Government usually needs both chambers and the presidency for major legislation, and the filibuster means Senate bills often need sixty votes.

The game tracks who holds each branch. Government Affairs cards require the necessary power. Without control, you must fight through party affairs, state affairs, organizing, and elections.

@demographics
go-to: menu

Six groups matter: **working-class** voters, **suburbanites**, **college-educated professionals**, **rural** voters, **minority communities**, and **young voters**. Each group\'s support is split among Democrats, Republicans, left parties, far-right parties, and non-voting. Turnout is lower in midterm years, especially among minority and young voters.

@factions
go-to: menu

The party has six factions: **Progressives**, **Establishment**, **Labor**, **Moderates**, **Abundance** (builders and technocrats) and **Populists** (heartland economic nationalists). Each has strength and dissent. High dissent costs resources and reduces the effect of your actions.

@opposition
go-to: menu

Three forces threaten democratic stability: the **MAGA movement** which can capture the Republican Party and strain institutions; **far-right extremists and militias**; and the **far left**, whose rise can split our coalition and trigger backlash. Meters track institutions, civic culture, and the progress of any subversion effort.

@elections
go-to: menu

Elections occur every November in even years. Presidential years: the national vote is mapped onto five Electoral College blocs. Midterm years: House and Senate seats are projected from the national vote, a gerrymandering bias, and the Senate map of that cycle. The nominees you help choose carry their own strengths and weaknesses.

@tips
go-to: menu

Every action takes a month. Advisor actions are free. Don\'t neglect organizing, voter protection, and the economy: you cannot win elections or protect democracy with a collapsing coalition.
"""
write('scenes/library.scene.dry', LIB)

write('scenes/modinfo.scene.dry', """title: Mod Info
go-to: flavors

@flavors
new-page: true

= Dynamic Social Democracy: America 2014-2026

This mod ports the mechanics of *Social Democracy: An Alternate History* to American politics. You play the **Democratic Party**, month by month from January 2014 to December 2026. Nothing is scripted to match the real outcomes: the real-world shocks (the Ukraine war, a pandemic, inflation) happen around you, but elections, nominees, and who holds power depend on how well you play.

- @what: What is carried over from the original?
- @paths: What can happen?
- @root.start: Start game
- @root: Back

@what
go-to: flavors

The monthly action loop, decks and hands of cards, advisor free-actions, factions with strength and dissent, resources and dues, the demographic-group vote model, relations, paramilitary-style forces, rising enemies, dynamic opposition, and multiple endings are all kept. Weimar-specific content (coalitions, Reichstag proportional representation, the president\'s cabinet-making power) is converted to its US analogues.

@paths
go-to: flavors

Win elections and keep the institutions strong, and democracy endures. Neglect the threat, and the Trump movement, the far right, or a split left can drag the country toward collapse. You can lose power and still save democracy, or win power and lose it.
""")

write('scenes/credits.scene.dry', """title: Credits
go-to: c

@c
new-page: true

= Credits

Based on *Social Democracy: An Alternate History* by Autumn Chen, and the *Dynamic Social Democracy* mod by originn0.

This US 2014-2026 conversion keeps the original\'s engine and structure. Historical events are summarized from public record; all in-game outcomes are fictional.

- @root: Back
""")

write('scenes/mod_loader.scene.dry', """title: Mods
is-special: true

= Mods

Additional mods can be loaded from the official mod list in the full original game.

- @backSpecialScene: Back
""")

# ---------------------------------------------------------------- game over
GO = """
Q.game_over = 1;
Q.dem_norm = Math.round(Q.dem_votes);
// ending classification
var d = Q.democracy_score;
var inpow = (Q.dem_president ? 1 : 0) + (Q.dem_house ? 1 : 0) + (Q.dem_senate ? 1 : 0);
if (Q.game_lost) { Q.ending_id = 'collapse'; }
else if (d >= 75 && Q.maga_strength < 45) { Q.ending_id = 'resilient'; }
else if (d >= 55) { Q.ending_id = 'fragile'; }
else { Q.ending_id = 'authoritarian_drift'; }
if (!Q.game_lost) {
  if (this.achieve) {
    if (Q.dem_president && Q.dem_house && Q.dem_senate) this.achieve('trifecta_2026');
    if (d >= 75) this.achieve('guardrails_hold');
    if (Q.maga_strength < 25) this.achieve('movement_contained');
    if (Q.n_elections >= 7 && Q.dissent_percent < 10) this.achieve('united_party');
    if (Q.farleft_strength < 8 && Q.farright_strength < 8) this.achieve('fringes_shrunk');
    if (Q.gerrymander_bias <= 1) this.achieve('fair_maps');
    if (Q.voting_rights >= 1 && Q.ethics_reform >= 1) this.achieve('democracy_reformers');
    if (!Q.dem_president && d >= 70) this.achieve('loyal_opposition');
    if (Q.unemployed < 5 && Q.inflation < 3.5) this.achieve('soft_landing');
  }
} else if (this.achieve) {
  this.achieve('the_republic_fell');
}
"""
write('scenes/game_over.scene.dry', """title: Game Over.
new-page: true
go-to: eg_menu
on-arrival: """ + js(GO) + """

= The End

@eg_menu

= The Verdict

[? if ending_id == "collapse" : ## The Republic Falls ?]
[? if ending_id == "resilient" : ## A Resilient Republic ?]
[? if ending_id == "fragile" : ## A Fragile Republic ?]
[? if ending_id == "authoritarian_drift" : ## Democracy in Retreat ?]

[? if ending_id == "collapse" : American democracy has collapsed. Elections may continue, but the real power no longer answers to voters. The movement that rose in the 2010s, and the failures of those who might have stopped it, are now the subject of history, not politics. ?]
[? if ending_id == "resilient" : As 2026 closes, American democracy has weathered a decade of storms. Courts, election officials, civil society, and a majority of voters held the line, and a Democratic Party that adapted to a changing country helped lead the defense. ?]
[? if ending_id == "fragile" : American democracy survives, but it is bruised. Norms have eroded, trust is low, and the next crisis could break what this one only bent. The work continues. ?]
[? if ending_id == "authoritarian_drift" : American democracy has not formally collapsed, but the signs are alarming: weakened institutions, an intimidated press, and a party system that no longer plays by shared rules. Whether it recovers depends on what happens next. ?]

**Final state:** Democrats hold [? if dem_president = 1 : the presidency ?][? if dem_president = 0 : neither the presidency ?][? if dem_house = 1 : , the House ?][? if dem_senate = 1 : , the Senate ?]. Democratic health index: [+ democracy_score_r +]. Movement strength of MAGA: [+ maga_strength_r +]. Party dissent: [+ dissent_percent_r +]%.

[? if dem_president = 1 and dem_house = 1 and dem_senate = 1 : **A full trifecta.** ?]

- @root: Return to the main menu
""")
print('ui written')
