from dry import *

# ---------------------------------------------------------------- utility scenes
write('scenes/easy_discard.scene.dry', """title: Return card to hand.
view-if: difficulty <= 0 and last_advisor_action = 0 and last_cabinet_action = 0
go-to: root
on-arrival: """ + js("""
if (Q.month_actions > 0) {
    Q.month_actions -= 1;
}
// return card to hand
var card = this.state.lastPlayedCard;
card.image = card.cardImage;
this.state.currentHands['main'].push(card);
// reset the timer...
if (Q[card.id + "_timer"]) {
    Q[card.id + "_timer"] = 0;
}
// reduce visit count
if (this.state.visits[card.id]) {
    this.state.visits[card.id] -= 1;
}
""") + "\n")
write('scenes/return.scene.dry', "title: Back to main\ngo-to: root\n")

tail = 'advisor_action_timer = 6'
AV = 'advisor_action_timer = 0'
UA = '[? if advisor_action_timer > 0 : [+ advisor_action_timer +] months before next advisor action. ?]'

# ---------------------------------------------------------------- advisors (free, once per 6 months)
ADV = [
 ('dolores_reyes', 'Dolores Reyes', 'progressive',
  'Reyes is the party\'s organizing director, a veteran of field campaigns and immigrant-rights coalitions who believes elections are won door by door.',
  [('field_ops', 'Build the Field Operation', 'Invest in neighborhood organizers and volunteer networks.',
    'civic_strength += 300; dem_enthusiasm += 0.8; progressive_dissent -= 5; moderate_dissent += 2',
    'We have funded thousands of new organizers. Enthusiasm is up, and moderates grumble about the cost.'),
   ('infrequent_voters', 'Turn Out Infrequent Voters', 'Targeted outreach to young and minority voters.',
    'minority_dem += 4*(1-dissent); young_dem += 3*(1-dissent); progressive_strength += 2; establishment_dissent += 2',
    'Canvassers knock on doors that campaigns usually skip. Turnout among occasional voters ticks up.')]),
 ('marcus_hale', 'Marcus Hale', 'establishment',
  'Hale is the party\'s chief pollster, a numbers man who distrusts slogans that have not been tested in focus groups.',
  [('message_testing', 'Message Testing', 'Refine our message for swing voters.',
    'suburban_dem += 4*(1-dissent); working_dem += 2*(1-dissent); establishment_strength += 2; progressive_dissent += 3',
    'Focus groups reveal what persuadable voters actually care about. The new message is sharper, and some on the left call it focus-grouped mush.'),
   ('battleground_polls', 'Battleground Polling', 'Find where we are weakest and fix it.',
    'resources += 1; dem_enthusiasm += 0.3; trump_urgency += 0.3',
    'The polling shows exactly where our coalition is cracking. The data is sobering and useful.')]),
 ('tom_brandt', 'Tom Brandt', 'labor',
  'Brandt is the labor liaison, a former union local president who keeps the party honest about working-class life.',
  [('union_drive', 'Support Union Organizing', 'Back organizing drives in warehouses, hospitals, and factories.',
    'labor_strength += 5; labor_relation += 6; working_dem += 3*(1-dissent); biz_relation -= 3; labor_dissent -= 5',
    'Union drives win across several industries. Business groups complain; workers notice who showed up.'),
   ('workers_message', 'A Message for Workers', 'Make the economy about paychecks, not abstractions.',
    'working_dem += 4*(1-dissent); rural_dem += 1*(1-dissent); populist_strength += 2; abundance_dissent += 2',
    'The new message talks about wages, healthcare costs, and dignity. It lands in union halls and diners alike.')]),
 ('elaine_whitcomb', 'Elaine Whitcomb', 'establishment',
  'Whitcomb is the party\'s election lawyer, quietly preparing for every way an election can go wrong.',
  [('litigate_access', 'Litigate for Ballot Access', 'Fight restrictive voting rules in court.',
    'election_admin += 4; voting_rights += 0.2; subversion_progress -= 0.3; resources -= 0',
    'Our lawyers win several cases protecting access to the ballot and clear procedures for counting votes.'),
   ('contested_results', 'Prepare for Contested Results', 'Plan for attempts to overturn an election.',
    'subversion_progress -= 0.8; trump_urgency += 0.8; institutions += 1.5; civic_strength += 100',
    'A network of lawyers, poll watchers, and state officials rehearses how to defend a clean count.')]),
 ('sam_okafor', 'Sam Okafor', 'abundance',
  'Okafor runs the party\'s digital operation: a young, data-driven strategist who thinks the party loses online before it loses at the ballot box.',
  [('online_youth', 'Reach Young Voters Online', 'Meet young people on the platforms where they live.',
    'young_dem += 4*(1-dissent); educated_dem += 1*(1-dissent); abundance_strength += 2; establishment_dissent += 2',
    'The digital team floods feeds with short, human-sounding content. Young voters notice.'),
   ('counter_disinfo', 'Counter Disinformation', 'Rapid-response against viral falsehoods.',
    'polarization -= 1; press_freedom += 1; pro_democracy += 1; progressive_dissent += 2',
    'A rapid-response team debunks viral falsehoods within hours. Critics call it paternalistic; it does slow the worst rumors.')]),
 ('ruth_calloway', 'Ruth Calloway', 'moderate',
  'Calloway is a retired general turned national security adviser, trusted by the Pentagon and wary of both isolationism and adventurism.',
  [('reassure_allies', 'Reassure Allies', 'Quiet diplomacy with foreign partners.',
    'intl_relation += 8; moderate_strength += 2; progressive_dissent += 2',
    'Calloway\'s calls to allied capitals calm nerves about American reliability.'),
   ('civil_military', 'Reinforce Civil-Military Norms', 'Reaffirm the military\'s constitutional role.',
    'military_loyalty += 0.05; subversion_progress -= 0.4; institutions += 1',
    'Retired generals and current officers publicly restate their oath to the Constitution rather than to any individual.')]),
 ('jake_moretti', 'Jake Moretti', 'moderate',
  'Moretti is a rural outreach director from a county the party hasn\'t won in a generation. He insists we show up everywhere.',
  [('listening_tour', 'Rural Listening Tour', 'Show up in places the party has abandoned.',
    'rural_dem += 5*(1-dissent); working_dem += 1*(1-dissent); populist_strength += 3; progressive_dissent += 3',
    'We spend weeks in diners and fairgrounds. Turnout in rural counties improves a little; the press covers the effort kindly.'),
   ('gun_farm', 'Back Practical Rural Priorities', 'Highlight broadband, hospitals, and farm policy.',
    'rural_dem += 3*(1-dissent); populist_strength += 2; moderate_strength += 2; progressive_dissent += 2',
    'Broadband, rural hospitals, and farm credit give rural voters concrete reasons to listen.')]),
]
for aid, name, fac, bio, acts in ADV:
    lines = ['title: %s' % name, 'is-pinned-card: true', 'tags: advisor, %s' % fac, 'view-if: %s_advisor = 1' % aid, 'new-page: true', '', '= %s' % name, '', bio, '']
    for a in acts:
        lines.append('- @%s' % a[0])
    lines.append('- @root: Return to main')
    lines.append('')
    for a in acts:
        lines += ['@%s' % a[0], 'title: %s' % a[1], 'subtitle: %s' % a[2], 'unavailable-subtitle: %s' % UA,
                  'choose-if: advisor_action_timer = 0', 'on-arrival: advisor_action_timer = 6; %s' % a[3], '', a[4], '']
    write('scenes/advisors/%s.scene.dry' % aid, '\n'.join(lines))

# ---------------------------------------------------------------- shuffle leadership
write('scenes/advisors/shuffle_leadership_pinned.scene.dry', """title: Shuffle Leadership
view-if: started and shuffle_leadership_timer <= 0
new-page: true
is-card: true
is-pinned-card: true
on-arrival: month_actions += 1; shuffle_leadership_timer = 10
go-to: shuffle_leadership_menu

@shuffle_leadership_menu

= Shuffle Leadership

Our advisory circle is limited to a handful of trusted figures at any time. Who should we bring in, and who should we let go?

- @swap_prog: Swap in the organizer and rural strategist (Reyes, Moretti); drop Hale and Whitcomb.
- @swap_estab: Swap in the pollster and election lawyer (Hale, Whitcomb); drop Reyes and Moretti.
- @swap_econ: Swap in the economist and digital director (Nair-style technocrats: Okafor, Calloway); drop Brandt and Hale.
- @swap_labor: Swap in Brandt and Hale; drop Okafor and Calloway.
- @remove_none: Don't change advisors.

@swap_prog
on-arrival: dolores_reyes_advisor = 1; jake_moretti_advisor = 1; marcus_hale_advisor = 0; elaine_whitcomb_advisor = 0; progressive_strength += 2; moderate_strength += 2

Reyes and Moretti join the circle. The grassroots are energized.

@swap_estab
on-arrival: marcus_hale_advisor = 1; elaine_whitcomb_advisor = 1; dolores_reyes_advisor = 0; jake_moretti_advisor = 0; establishment_strength += 4

Hale and Whitcomb take center stage. The party apparatus hums.

@swap_econ
on-arrival: sam_okafor_advisor = 1; ruth_calloway_advisor = 1; tom_brandt_advisor = 0; marcus_hale_advisor = 0; abundance_strength += 3; moderate_strength += 2; labor_dissent += 3

Okafor and Calloway join. Labor leaders are unhappy.

@swap_labor
on-arrival: tom_brandt_advisor = 1; marcus_hale_advisor = 1; sam_okafor_advisor = 0; ruth_calloway_advisor = 0; labor_strength += 4; abundance_dissent += 3

Brandt and Hale join. The party leans into its working-class identity.

@remove_none
on-arrival: month_actions -= 1; shuffle_leadership_timer = 0
go-to: root

We keep our team as is.
""")

# ---------------------------------------------------------------- party affairs cards
P = 'party_affairs'
cards = []
def C(*a, **k):
    cards.append(card(*a, **k))

def party(id, title, view_if, timer, intro, options, **k):
    t = card(id, title, P, view_if, timer, intro, options, **k)
    write('scenes/party_affairs/%s.scene.dry' % id, t)

def govt(id, title, view_if, timer, intro, options, **k):
    t = card(id, title, 'govt_affairs', view_if, timer, intro, options, **k)
    write('scenes/government_affairs/%s.scene.dry' % id, t)

party('fundraising', 'Fundraising', 'fundraising_timer <= 0', 12,
 'The campaign never ends, and neither does the need for money. Where do we turn?',
 [opt('small_dollar', 'Small-dollar drive', 'resources += 2; dues += 1*(1-dissent); progressive_dissent -= 2; biz_relation -= 1',
      'Millions of small donations roll in, powered by grassroots outrage and relentless emails. The base feels ownership.', sub='+2 resources, +1 annual dues', unavail='Needs time.'),
  opt('big_donors', 'Courting major donors', 'resources += 3; biz_relation += 5; progressive_dissent += 5; left_relation -= 3',
      'Dinners in the Hamptons and Silicon Valley fill the war chest. Progressives complain about who is buying access.', sub='+3 resources; business happy, left angry'),
  opt('grassroots_events', 'Grassroots house parties', 'resources += 1; dem_enthusiasm += 0.6; labor_dissent -= 2',
      'Living-room fundraisers and union-hall suppers are slower but build loyalty.', sub='+1 resource, +enthusiasm')])

party('campaigning', 'Campaign Blitz', 'campaigning_timer <= 0', 6,
 'Every election is decided by who shows up. Where should we deploy our surrogates and ads?',
 [opt('blue_wall', 'Industrial heartland', 'resources -= 1; working_dem += 5*(1-dissent); rural_dem += 1*(1-dissent); labor_dissent -= 3', 'We flood Pennsylvania, Michigan, and Ohio with ads, surrogates, and union canvassers.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('suburban_push', 'Suburban professionals', 'resources -= 1; suburban_dem += 5*(1-dissent); educated_dem += 2*(1-dissent); progressive_dissent += 2', 'Targeted mail and digital ads speak to suburban parents worried about schools, healthcare, and extremism.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('rights_turnout', 'Mobilize our base', 'resources -= 1; minority_dem += 5*(1-dissent); young_dem += 3*(1-dissent); dem_enthusiasm += 0.5', 'We invest in churches, campuses, and community centers. Turnout in our core groups rises.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('sun_belt', 'Sun Belt expansion', 'resources -= 1; minority_dem += 3*(1-dissent); suburban_dem += 3*(1-dissent); rural_dem += 1*(1-dissent)', 'Arizona, Georgia, North Carolina: long-term investment pays early dividends.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.')])

party('ideology', 'Define Our Ideology', 'ideology_timer <= 0', 10,
 'The party stands for many things. Voters, donors, and activists want a clear answer about what we are.',
 [opt('progressive_turn', 'A bolder, progressive agenda', 'progressive_strength += 6; moderate_strength -= 2; establishment_strength -= 2; progressive_dissent -= 8; moderate_dissent += 6; biz_relation -= 4; left_relation += 4; farleft_strength -= 0.5; young_dem += 3*(1-dissent); suburban_dem -= 2*(1-dissent)',
      'We champion universal programs and confront concentrated wealth. The left feels heard; swing voters watch nervously.'),
  opt('pragmatic_center', 'Pragmatic center', 'moderate_strength += 5; establishment_strength += 2; progressive_strength -= 4; progressive_dissent += 6; moderate_dissent -= 5; suburban_dem += 4*(1-dissent); biz_relation += 4; left_relation -= 5; farleft_strength += 0.6',
      'We emphasize competence and bipartisan achievements. Moderates breathe easier; activists wonder where the fight went.'),
  opt('abundance_agenda', 'The abundance agenda', 'abundance_discovered = 1; abundance_strength += 6; progressive_dissent += 2; labor_dissent += 1; suburban_dem += 2*(1-dissent); young_dem += 2*(1-dissent); economic_growth += 0.2',
      'Build more housing, clean energy, and transit; make government deliver. The agenda draws new energy and some skepticism from those wary of deregulation.'),
  opt('populist_economics', 'Economic populism', 'populist_discovered = 1; populist_strength += 6; labor_strength += 2; working_dem += 4*(1-dissent); rural_dem += 2*(1-dissent); educated_dem -= 2*(1-dissent); abundance_dissent += 3; progressive_dissent += 2',
      'We take on monopolies, trade deals, and corporate power with a message aimed at working families of every background.')])

party('media', 'Media Strategy', 'media_timer <= 0', 8,
 'The media landscape is fractured: cable, podcasts, influencers, and algorithms all pull voters in different directions.',
 [opt('local_news', 'Invest in local outreach', 'resources -= 1; rural_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); press_freedom += 1; polarization -= 0.5', 'We back local-news partnerships and town halls, reaching voters who tune out national shouting matches.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('influencer_network', 'Build an influencer and podcast network', 'resources -= 1; young_dem += 5*(1-dissent); working_dem += 1*(1-dissent); educated_dem += 1*(1-dissent)', 'Friendly creators and podcasters carry our message in their own voices.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('attack_ads', 'Go negative on the opposition', 'resources -= 1; suburban_gop -= 3; trump_urgency += 0.3; polarization += 1; gop_enthusiasm += 0.4', 'Contrast ads hit hard, and the other side is energized too.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.')])

party('organizing', 'Grassroots Organizing', 'organizing_timer <= 0', 8,
 'Movements win elections that candidates cannot. Whom should we organize?',
 [opt('indivisible_model', 'Neighborhood resistance groups', 'civic_strength += 400; dem_enthusiasm += 0.6; radicalization -= 0; progressive_strength += 2', 'Thousands of volunteer-run local chapters sprout up, trained in nonviolent tactics.'),
  opt('labor_community', 'Labor and community coalition', 'civic_strength += 250; labor_strength += 3; labor_relation += 5; working_dem += 2*(1-dissent); minority_dem += 2*(1-dissent)', 'Unions and community groups share staff, phone banks, and trust.'),
  opt('faith_and_veterans', 'Faith and veterans outreach', 'civic_strength += 200; rural_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); moderate_strength += 2', 'Pastors and veterans vouch for us in places where partisan labels are suspect.')])

party('voter_protection', 'Voter Protection Program', 'voter_protection_timer <= 0', 10,
 'A democracy is only as strong as its election machinery. How do we protect it?',
 [opt('poll_watchers', 'Recruit and train poll workers and watchers', 'election_admin += 4; civic_strength += 200; subversion_progress -= 0.3; pro_democracy += 0.5', 'Volunteers staff polling places and observe counts, defending both access and integrity.'),
  opt('state_partners', 'Partner with state election officials', 'election_admin += 3; institutions += 1; gopmod_relation += 4; progressive_dissent += 1', 'Nonpartisan officials, including Republicans, learn they can count on us to defend clean administration.'),
  opt('legal_war_chest', 'Build a legal war chest', 'resources -= 1; election_admin += 3; voting_rights += 0.15; subversion_progress -= 0.5', 'Lawyers on retainer are ready for any challenge.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.')])

party('confronting_trump', 'Confronting the Trump Movement', 'confronting_trump_timer <= 0 and maga_strength >= 25', 8,
 'A populist, nationalist movement is reshaping the Republican Party and challenging democratic norms. How do we respond?',
 [opt('expose_threat', 'Sound the alarm', 'trump_urgency += 1.5; pro_democracy += 1; polarization += 1; maga_strength -= 1; dem_enthusiasm += 0.5; gopmod_relation -= 2',
      'We warn that democratic norms are under threat. The base is energized, though some say we cry wolf.', sub='raises urgency'),
  opt('address_grievances', 'Address the grievances behind the movement', 'maga_strength -= 3; working_dem += 3*(1-dissent); rural_dem += 3*(1-dissent); populist_strength += 2; progressive_dissent += 3; polarization -= 1',
      'We talk honestly about trade, towns left behind, and distrust of elites, and offer real alternatives.'),
  opt('build_cross_party', 'Build a cross-party defense of democracy', 'gopmod_relation += 6; maga_strength -= 1.5; institutions += 2; progressive_dissent += 2; trump_urgency += 0.8; pro_democracy += 1.5',
      'Never-Trump Republicans, civil libertarians, and business leaders join us in a coalition that tolerates uneasy bedfellows.'),
  opt('mock_it', 'Mock and ignore', 'trump_urgency -= 0.5; polarization += 1.5; maga_strength += 2; gop_enthusiasm += 0.5; suburban_dem += 1*(1-dissent)',
      'Satire lands well with our base but also galvanizes our opponents. Ignoring the movement is not working.')])

party('crisis_program', 'Economic Message and Program', 'crisis_program_timer <= 0', 12,
 'Voters do not just want a defense of norms; they want an economy that works for them. What do we propose?',
 [opt('middle_class', 'Middle-class tax relief and childcare', 'economic_plan = 1; working_dem += 3*(1-dissent); suburban_dem += 4*(1-dissent); moderate_strength += 2; crisis_urgency += 1', 'We lay out tax credits and childcare support for working families.'),
  opt('industrial_policy', 'Industrial policy and reshoring', 'economic_plan = 1; working_dem += 4*(1-dissent); rural_dem += 2*(1-dissent); labor_strength += 2; populist_strength += 2; abundance_dissent += 2; crisis_urgency += 1', 'We invest in factories, supply chains, and apprenticeships.'),
  opt('green_new_deal', 'A climate jobs program', 'economic_plan = 1; young_dem += 4*(1-dissent); educated_dem += 3*(1-dissent); progressive_strength += 3; rural_dem -= 1*(1-dissent); biz_relation -= 2; climate_agenda += 1; crisis_urgency += 1', 'A big program of green investment energizes the young but frightens energy workers.'),
  opt('fiscal_hawk', 'Credibility on deficits', 'economic_plan = 1; suburban_dem += 3*(1-dissent); biz_relation += 5; progressive_dissent += 5; labor_dissent += 3; budget += 1', 'We pair promises with offsets. Voters reward seriousness; activists call it timidity.')])

party('outreach', 'Cross-Party Outreach', 'outreach_timer <= 0', 8,
 'Divided government requires deals, and deals require relationships across the aisle.',
 [opt('gop_moderates', 'Cultivate Republican moderates', 'gopmod_relation += 8; moderate_strength += 2; progressive_dissent += 3; suburban_dem += 1*(1-dissent)', 'Quiet dinners and joint bills build trust.'),
  opt('business_groups', 'Meet with business leaders', 'biz_relation += 8; moderate_strength += 1; labor_dissent += 3; resources += 1', 'Chambers of commerce and tech executives are courted; some are even friendly.'),
  opt('governors', 'Work with Republican governors', 'gopmod_relation += 5; dem_governors += 0; rural_dem += 1*(1-dissent); suburban_dem += 1*(1-dissent); institutions += 1', 'Practical state-level cooperation offers a model for national dealmaking.')])

party('left_outreach', 'Outreach to the Left', 'left_outreach_timer <= 0', 8,
 'Our left flank is restless: some want to work within the party, others point toward third parties and street protest.',
 [opt('dsa_activists', 'Welcome left activists into the party', 'left_relation += 8; farleft_strength -= 1.5; progressive_strength += 3; progressive_dissent -= 5; moderate_dissent += 3; biz_relation -= 2; young_dem += 2*(1-dissent)', 'Democratic socialists and movement groups find seats at the table.'),
  opt('policy_concessions', 'Offer policy concessions', 'left_relation += 5; farleft_strength -= 1; progressive_dissent -= 4; resources -= 1; budget -= 1', 'We adopt several demands in the platform.', choose='resources >= 1', sub='-1 resource, -1 budget', unavail='Need 1 resource.'),
  opt('discipline_left', 'Draw a line against extremism', 'left_relation -= 6; farleft_strength += 1; radicalization -= 0; suburban_dem += 3*(1-dissent); progressive_dissent += 6; moderate_dissent -= 3; directleft_militancy -= 0.05', 'We condemn violence and fringe positions. Swing voters approve; activists fume.')])

party('international_relations', 'International Relations', 'international_relations_timer <= 0', 12,
 'America\'s alliances and reputation affect both security and economic stability.',
 [opt('allies_trip', 'Tour allied capitals', 'intl_relation += 8; moderate_strength += 2; progressive_dissent += 1', 'Our leaders reassure allies that American democracy remains reliable.'),
  opt('human_rights', 'Champion human rights and democracy abroad', 'intl_relation += 4; progressive_strength += 2; pro_democracy += 1; biz_relation -= 2', 'We put democracy and rights at the heart of foreign policy.'),
  opt('america_first_lite', 'Emphasize domestic priorities', 'intl_relation -= 3; working_dem += 3*(1-dissent); rural_dem += 2*(1-dissent); populist_strength += 3; moderate_dissent += 2', 'We say charity begins at home. The foreign-policy establishment groans.')])

party('party_disunity', 'Party Unity', 'party_disunity_timer <= 0 and dissent_percent >= 8', 10,
 'The party\'s factions are quarreling. Unity is a resource; disunity is a drain.',
 [opt('unity_retreat', 'Hold a unity retreat', 'progressive_dissent -= 6; establishment_dissent -= 6; labor_dissent -= 6; moderate_dissent -= 6; abundance_dissent -= 6; populist_dissent -= 6; resources -= 1', 'Leaders talk it out. Grievances remain, but they are heard.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('big_tent', 'Promise every faction a seat at the table', 'progressive_dissent -= 3; moderate_dissent -= 3; labor_dissent -= 3; populist_dissent -= 3; abundance_dissent -= 3; establishment_dissent -= 3; budget -= 1', 'Platform planks and committee seats are distributed to all.'),
  opt('crack_whip', 'Enforce discipline', 'progressive_dissent += 3; moderate_dissent += 3; establishment_dissent -= 8; resources += 1', 'Leadership imposes order. The establishment is pleased; rebels are not.')])

party('state_affairs', 'State and Local Affairs', 'state_affairs_timer <= 0', 6,
 'Governors, legislatures, and secretaries of state decide how elections are run and how policy is lived. Where do we fight?',
 [opt('legislatures', 'Flip state legislatures', 'resources -= 1; dem_legislatures += 1; gerrymander_bias -= 0.15; civic_strength += 100', 'Targeted spending in legislative races begins to pay off.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('secretaries', 'Back secretary of state candidates', 'resources -= 1; election_admin += 3; subversion_progress -= 0.3', 'Election administration races become a priority.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('ballot_measures', 'Pursue ballot initiatives', 'resources -= 1; gerrymander_bias -= 0.3; voting_rights += 0.1; dem_enthusiasm += 0.3', 'Voters approve independent redistricting commissions and voting access measures.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.'),
  opt('governors_races', 'Invest in governors races', 'resources -= 1; dem_governors += 1; rural_dem += 1*(1-dissent)', 'A strong bench of governors produces future leaders.', choose='resources >= 1', sub='-1 resource', unavail='Need 1 resource.')])

# ---------------------------------------------------------------- government cards
E = 'dem_president = 1'
L = 'dem_president = 1 and dem_house = 1 and dem_senate = 1'
govt('economic_policy', 'Economic Policy', 'economic_policy_timer <= 0 and ' + E, 6,
 'The economy is the foundation of everything. Unemployment stands at [+ unemployed_2 +] percent and inflation at [+ inflation_2 +] percent.',
 [opt('stimulus', 'Stimulus spending', 'budget -= 2; economic_growth += 1.2; inflation += 0.3; stimulus_level += 1; working_dem += 2*(1-dissent); progressive_dissent -= 3', 'Federal dollars flow. Growth picks up; some economists warn of overheating.', choose='budget >= 2', sub='-2 budget', unavail='Need 2 budget.'),
  opt('investment', 'Public investment', 'budget -= 1; economic_growth += 0.5; unemployed -= 0.2; working_dem += 2*(1-dissent); abundance_strength += 1', 'Roads, grids, and research labs get funding.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.'),
  opt('trade_policy', 'Retool trade policy', 'rural_dem += 2*(1-dissent); working_dem += 3*(1-dissent); biz_relation -= 3; intl_relation -= 2; populist_strength += 2', 'We rebalance trade rules toward workers and domestic industry.'),
  opt('consolidate', 'Consolidate and cut deficits', 'budget += 2; economic_growth -= 0.3; biz_relation += 3; progressive_dissent += 4; labor_dissent += 3', 'Fiscal prudence restores room on the books but costs us on the left.')])

govt('healthcare', 'Healthcare Policy', 'healthcare_timer <= 0 and ' + L, 8,
 'Roughly [+ uninsured +] percent of Americans lack health insurance, and costs still strain families.',
 [opt('expand_aca', 'Expand ACA subsidies and Medicaid', 'budget -= 1; uninsured -= 2; working_dem += 2*(1-dissent); minority_dem += 2*(1-dissent); healthcare_agenda += 1; progressive_dissent -= 3', 'More families get covered. Cost curves bend a little.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.'),
  opt('public_option', 'Create a public option', 'budget -= 2; uninsured -= 3; progressive_strength += 2; biz_relation -= 3; moderate_dissent += 3; healthcare_agenda += 2', 'The public option sparks a fierce lobbying fight, and passes.', choose='budget >= 2', sub='-2 budget', unavail='Need 2 budget.'),
  opt('drug_prices', 'Negotiate drug prices', 'budget += 1; working_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); biz_relation -= 2; healthcare_agenda += 1', 'Seniors save; pharmaceutical lobbyists fume.'),
  opt('stabilize', 'Stabilize the current system', 'budget -= 0; uninsured -= 0.5; moderate_strength += 1; progressive_dissent += 2', 'We patch what exists and avoid bigger fights.')])

govt('labor_policy', 'Labor Policy', 'labor_policy_timer <= 0 and ' + E, 8,
 'Unions are the backbone of the party but face headwinds. What can we do for workers?',
 [opt('pro_act', 'Strengthen the right to organize', 'labor_strength += 5; labor_relation += 8; working_dem += 3*(1-dissent); biz_relation -= 5; labor_dissent -= 6', 'New rules make organizing easier. Business groups mobilize against us.'),
  opt('minimum_wage', 'Raise the minimum wage', 'labor_relation += 4; working_dem += 3*(1-dissent); young_dem += 2*(1-dissent); biz_relation -= 3; unemployed += 0.05', 'Millions get raises.'),
  opt('worker_training', 'Invest in apprenticeships', 'budget -= 1; unemployed -= 0.2; working_dem += 2*(1-dissent); rural_dem += 1*(1-dissent); moderate_strength += 1', 'A skills agenda wins support across lines.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.')])

govt('social_welfare', 'Social Welfare', 'social_welfare_timer <= 0 and ' + L, 8,
 'The social safety net can reduce poverty or become a political target. What do we expand?',
 [opt('child_credit', 'Expand the child tax credit', 'budget -= 2; working_dem += 3*(1-dissent); suburban_dem += 2*(1-dissent); minority_dem += 2*(1-dissent); inequality -= 3', 'Child poverty falls sharply.', choose='budget >= 2', sub='-2 budget', unavail='Need 2 budget.'),
  opt('paid_leave', 'Paid family leave', 'budget -= 1; working_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); young_dem += 1*(1-dissent)', 'Workers get leave to care for newborns and sick relatives.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.'),
  opt('housing', 'Build housing and loosen zoning', 'abundance_strength += 3; budget -= 1; young_dem += 3*(1-dissent); suburban_dem -= 1*(1-dissent); inequality -= 2; economic_growth += 0.2', 'A housing bill makes building easier and cheaper, over local objections.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.')])

govt('judiciary', 'The Judiciary', 'judiciary_timer <= 0 and ' + E, 10,
 'Courts shape every policy fight. Federal judges serve for life, so choices made today last for decades.',
 [opt('appoint_judges', 'Prioritize judicial appointments', 'courts_independence += 3; court_lean -= 0.4; progressive_dissent -= 2', 'We move nominees through the Senate and fill vacancies.', choose='dem_senate = 1', sub='needs Senate control', unavail='Needs a Democratic Senate.'),
  opt('bipartisan_picks', 'Seek consensus nominees', 'courts_independence += 4; gopmod_relation += 4; progressive_dissent += 3; institutions += 1', 'We pick respected jurists acceptable across the spectrum.'),
  opt('court_reform_push', 'Push structural court reform', 'court_reform += 1; court_lean -= 1; progressive_dissent -= 5; moderate_dissent += 5; institutions -= 1; polarization += 2; trump_urgency += 0.3', 'Term limits and expansion spark a firestorm.', choose='dem_senate = 1 and dem_house = 1', sub='needs Congress', unavail='Needs both chambers.')])

govt('voting_policy', 'Democracy Reforms', 'voting_policy_timer <= 0 and ' + L, 10,
 'The rules of democracy are themselves contested. Reformers want federal standards; skeptics fear overreach.',
 [opt('voting_rights_act', 'Pass voting rights legislation', 'voting_rights += 1; election_admin += 6; minority_dem += 3*(1-dissent); polarization += 1; gop_enthusiasm += 0.4; resources -= 0', 'Federal standards protect access to the ballot nationwide.'),
  opt('ethics_reform_bill', 'Ethics and anti-corruption reform', 'ethics_reform += 1; institutions += 3; pro_democracy += 2; biz_relation -= 2', 'Disclosure rules and conflict-of-interest limits rebuild some public trust.'),
  opt('fair_maps_bill', 'Ban partisan gerrymandering', 'gerrymander_bias -= 1.2; institutions += 1; gopmod_relation -= 3; polarization += 0.5', 'Independent commissions draw the lines, nationwide.'),
  opt('filibuster_change', 'Reform the filibuster', 'filibuster_reform += 1; institutions -= 1; progressive_dissent -= 4; moderate_dissent += 4; gopmod_relation -= 6', 'A rules change opens the way for faster legislation, and sharper polarization.')])

govt('foreign_policy', 'Foreign Policy', 'foreign_policy_timer <= 0 and ' + E, 8,
 'Allies and rivals alike are watching how America manages itself at home.',
 [opt('alliance_renewal', 'Renew alliances', 'intl_relation += 8; moderate_strength += 2; progressive_dissent += 1', 'Diplomats work the phones and hold joint summits.'),
  opt('diplomacy_first', 'Diplomacy over force', 'intl_relation += 4; progressive_strength += 2; moderate_dissent += 2; rural_dem -= 0', 'We prioritize negotiation and arms control.'),
  opt('trade_deals', 'Pursue new trade agreements', 'intl_relation += 4; biz_relation += 4; labor_dissent += 4; economic_growth += 0.2', 'New agreements open markets and anger some unions.')])

govt('defense_policy', 'Defense and the Military', 'defense_policy_timer <= 0 and ' + E, 10,
 'A professional military loyal to the Constitution is the last backstop of any republic.',
 [opt('civil_military_reform', 'Reinforce civil-military norms', 'military_loyalty += 0.06; institutions += 2; subversion_progress -= 0.5; progressive_dissent += 1', 'New codes of conduct and training reaffirm the oath to the Constitution.'),
  opt('veterans_programs', 'Expand veterans programs', 'budget -= 1; military_loyalty += 0.03; rural_dem += 2*(1-dissent); working_dem += 1*(1-dissent)', 'We win the gratitude of veterans.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.'),
  opt('cut_pentagon', 'Trim the defense budget', 'budget += 2; military_loyalty -= 0.04; progressive_dissent -= 3; moderate_dissent += 3; intl_relation -= 2', 'Savings are redirected, though generals grumble.')])

govt('immigration', 'Immigration', 'immigration_timer <= 0 and ' + E, 8,
 'Immigration is among the country\'s most emotionally charged issues. The Right uses it; the Left wants justice; most voters want order and humanity.',
 [opt('border_enforcement', 'Border security with legal pathways', 'rural_dem += 3*(1-dissent); working_dem += 2*(1-dissent); minority_dem -= 1*(1-dissent); progressive_dissent += 5; maga_strength -= 1', 'We pair stricter enforcement with legal pathways.'),
  opt('path_to_citizenship', 'A path to citizenship', 'minority_dem += 4*(1-dissent); young_dem += 2*(1-dissent); rural_dem -= 3*(1-dissent); working_dem -= 1*(1-dissent); progressive_dissent -= 4; maga_strength += 1.5; gop_enthusiasm += 0.3', 'Millions gain legal status, and the Right energizes.'),
  opt('executive_action', 'Act by executive order', 'minority_dem += 2*(1-dissent); rural_dem -= 2*(1-dissent); institutions -= 0.5; polarization += 1', 'Executive action helps some families, but invites courtroom battles.')])

govt('climate_energy', 'Climate and Energy', 'climate_energy_timer <= 0 and ' + E, 8,
 'Climate change is a growing threat and an economic opportunity.',
 [opt('clean_investment', 'Massive clean-energy investment', 'budget -= 2; climate_progress += 2; young_dem += 3*(1-dissent); educated_dem += 2*(1-dissent); economic_growth += 0.3; abundance_strength += 2', 'Subsidies for clean energy spark a manufacturing boom.', choose='budget >= 2', sub='-2 budget', unavail='Need 2 budget.'),
  opt('permitting_reform', 'Streamline permitting', 'climate_progress += 1; abundance_strength += 3; progressive_dissent += 2; economic_growth += 0.2; labor_relation += 2', 'We make it easier to build transmission lines, solar farms, and nuclear plants.'),
  opt('regulate', 'Tighten emissions rules', 'climate_progress += 1.5; young_dem += 2*(1-dissent); rural_dem -= 2*(1-dissent); biz_relation -= 3; economic_growth -= 0.2', 'Regulators tighten limits on pollution.')])

govt('justice_policing', 'Justice and Policing', 'justice_policing_timer <= 0 and ' + E, 8,
 'Public safety and civil rights both matter. The Department of Justice must remain independent from politics.',
 [opt('doj_independence', 'Protect DOJ independence', 'federal_law_loyalty += 0.06; institutions += 2; courts_independence += 1; progressive_dissent += 1', 'Rules insulate prosecutors from political pressure.'),
  opt('police_reform', 'Fund police reform and training', 'budget -= 1; minority_dem += 3*(1-dissent); suburban_dem += 1*(1-dissent); local_police_loyalty += 0.03; directleft_militancy -= 0.03', 'Modest reforms improve accountability while keeping officers on side.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.'),
  opt('community_safety', 'Invest in community violence prevention', 'budget -= 1; minority_dem += 2*(1-dissent); suburban_dem += 2*(1-dissent); progressive_dissent -= 2', 'Cities see gradual declines in violent crime.', choose='budget >= 1', sub='-1 budget', unavail='Need 1 budget.')])

govt('domestic_extremism', 'Domestic Extremism', 'domestic_extremism_timer <= 0 and ' + E + ' and (farright_strength >= 8 or farleft_strength >= 20)', 8,
 'Militias, extremist networks, and violent fringe groups threaten public safety and democratic order across the spectrum.',
 [opt('task_force', 'Create an interagency task force', 'farright_strength -= 2.5; militia_strength -= 40; farleft_strength -= 0.5; federal_law_loyalty += 0.02; progressive_dissent += 2', 'Federal agencies target violent plots while respecting civil liberties.'),
  opt('online_extremism', 'Counter online radicalization', 'farright_strength -= 1.5; press_freedom -= 1; polarization -= 0.5; progressive_dissent += 2; resources += 0', 'Platforms and prosecutors cooperate, with free-speech critics watching closely.'),
  opt('prevent_overreach', 'Safeguard civil liberties', 'press_freedom += 1; institutions += 1; progressive_dissent -= 3; farright_strength += 0.5', 'We reaffirm limits on surveillance and protest policing.')])

govt('oversight', 'Congressional Oversight', 'oversight_timer <= 0 and dem_house = 1', 8,
 'With the House in our hands, we can investigate, subpoena, and hold hearings.',
 [opt('investigate_abuse', 'Investigate abuses of power', 'institutions += 2; subversion_progress -= 0.6; trump_urgency += 0.4; polarization += 1.5; gop_enthusiasm += 0.5; dem_enthusiasm += 0.4', 'Hearings expose misconduct and energize both sides.'),
  opt('bipartisan_oversight', 'Pursue bipartisan oversight', 'institutions += 1.5; gopmod_relation += 5; polarization -= 0.5; progressive_dissent += 3', 'Narrower, bipartisan inquiries command broader respect.'),
  opt('legislative_agenda', 'Focus on the legislative agenda', 'budget += 0; working_dem += 2*(1-dissent); suburban_dem += 1*(1-dissent); progressive_dissent -= 1', 'We spend our time on popular bills, even if the Senate blocks them.')])

govt('fiscal_policy', 'Fiscal Policy', 'fiscal_policy_timer <= 0 and ' + E, 10,
 'Budgets are moral documents, and the debt limit is a recurring hostage.',
 [opt('raise_taxes', 'Raise taxes on high earners', 'budget += 3; biz_relation -= 5; working_dem += 1*(1-dissent); progressive_dissent -= 3; moderate_dissent += 2', 'The rich pay more; the treasury breathes easier.'),
  opt('close_loopholes', 'Close loopholes and boost enforcement', 'budget += 2; biz_relation -= 2; inequality -= 1', 'Tax enforcement raises substantial revenue.'),
  opt('grand_bargain', 'Seek a grand bargain', 'budget += 3; gopmod_relation += 6; progressive_dissent += 6; labor_dissent += 4; moderate_strength += 2', 'A bipartisan bargain trims deficits at some political cost.')])

govt('civil_rights', 'Civil Rights', 'civil_rights_timer <= 0 and ' + E, 8,
 'Equal rights under law remain the core promise of the republic.',
 [opt('lgbtq_protections', 'Strengthen LGBTQ and gender protections', 'young_dem += 3*(1-dissent); educated_dem += 2*(1-dissent); rural_dem -= 2*(1-dissent); gop_enthusiasm += 0.3; progressive_dissent -= 3', 'New protections pass amid fierce debate.'),
  opt('racial_justice', 'Advance racial-equity initiatives', 'minority_dem += 4*(1-dissent); suburban_dem -= 1*(1-dissent); working_dem -= 1*(1-dissent); polarization += 1', 'We tackle disparities in housing, lending, and justice.'),
  opt('universal_framing', 'Frame rights in universal terms', 'minority_dem += 2*(1-dissent); working_dem += 2*(1-dissent); suburban_dem += 1*(1-dissent); progressive_dissent += 2; polarization -= 0.5', 'Universal programs lift everyone while narrowing gaps.')])

govt('tech_media_policy', 'Technology and Media Policy', 'tech_media_policy_timer <= 0 and ' + E, 10,
 'Platforms, algorithms, and artificial intelligence are reshaping the economy and democratic discourse.',
 [opt('platform_rules', 'Regulate social media platforms', 'press_freedom += 1; polarization -= 1; pro_democracy += 1; biz_relation -= 3; abundance_dissent += 2', 'New rules on transparency and child safety pass.'),
  opt('antitrust', 'Break up monopolies', 'populist_strength += 3; working_dem += 2*(1-dissent); biz_relation -= 5; economic_growth -= 0.1; abundance_dissent += 2', 'Antitrust enforcers go after giants.'),
  opt('ai_guardrails', 'AI safety and worker protections', 'working_dem += 2*(1-dissent); young_dem += 1*(1-dissent); economic_growth -= 0.1; inequality -= 1; abundance_dissent += 1', 'Guardrails and retraining funds soften disruption.')])

print('cards written')
