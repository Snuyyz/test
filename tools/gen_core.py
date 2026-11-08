from dry import *
import os

LIB = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sd_lib.js'), encoding='utf-8').read()

# =============================================================================
# info.dry
# =============================================================================
write('info.dry', """title: Social Democracy: An Alternate History - Dynamic America (2014-2026)
author: Dynamic Social Democracy: America mod (based on Social Democracy by Autumn Chen)
ifid: 3C5A1F0E-8D2B-4B7A-9E21-6A4D0B7C2F11
""")

# =============================================================================
# root.scene.dry
# =============================================================================
write('scenes/root.scene.dry', """title: Root Scene
new-page: true
go-to: post_event if started = 1; start_menu if started = 0

@start_menu
new-page: true
go-to: start_menu_2

= Social Democracy: An Alternate History
== Dynamic America, 2014 - 2026

@start_menu_2

- @start_1: Start game
- @modinfo: Mod Info
- @credits: Credits

@start_1
go-to: start

@start
on-arrival: """ + js("""
%s
SD.init(Q);
""" % LIB) + """
go-to: post_event
""")

# =============================================================================
# post_event.scene.dry : monthly tick
# =============================================================================
POST = """
%s
Q.last_advisor_action = 0;
Q.last_cabinet_action = 0;
SD.refresh(Q);

// achievements that can trigger at any time
if (this.achieve) {
    if (Q.dem_president && Q.dem_house && Q.dem_senate && Q.year >= 2021 && Q.democracy_score >= 75) this.achieve('trifecta_of_democracy');
    if (Q.abundance_discovered && Q.populist_discovered && Q.dissent_percent < 20) this.achieve('big_tent');
    if (Q.gerrymander_bias <= 1) this.achieve('fair_maps');
}

// 1. update dates when a month passes (each action takes a month, as in the original)
if (Q.month_actions >= 1) {
    Q.just_inaugurated = 0;
    Q.just_seated = 0;
    var was_dem = Q.dem_president;
    SD.advanceMonth(Q);
    if (Q.inauguration_due) {
        SD.inaugurate(Q);
        Q.just_inaugurated = 1;
        Q.flipped_presidency = (was_dem != Q.dem_president) ? 1 : 0;
    } else if (Q.transition_due) {
        SD.seatCongress(Q);
        Q.just_seated = 1;
    }
    SD.refresh(Q);
    Q.last_time_updated = Q.time;
}

// 2. democratic collapse check
if (!Q.game_lost && !Q.game_over) {
    if (!Q.dem_president && Q.president == Q.maga_leader && Q.institutions <= 12 && Q.pro_democracy <= 40) {
        Q.game_lost = 1;
    }
}

// 3. which events are queued?
Q.has_event = 0;
var scene = this.game.scenes['post_event.events_choice'];
var choices = this._compileChoices(scene);
if (choices && choices[0].title != "Continue...") {
    Q.has_event = 1;
} else {
    Q.has_event = 0;
}
""" % LIB

write('scenes/post_event.scene.dry', """title: Post Event
new-page: true
on-arrival: """ + js(POST) + """
go-to: events_choice if has_event = 1; main if has_event = 0

= [+ month : month +] [+ year +]

@events_choice

- #event

# This scene routes to scheduled and dynamic events, then returns to the monthly hub (main).
""")

# =============================================================================
# main.scene.dry : monthly hub, news, decks
# =============================================================================
news = []
def N(cls, cond, text):
    news.append('{!<p class="%s">!}[? if %s: %s ?]{!</p>!}' % (cls, cond, text.strip()))

# --- state-dependent / dynamic lines ----------------------------------------
N('both', 'year = 2014 and month = 1',
  'It is January 2014. The %s hold the White House and the Senate; the %s control the House. The Affordable Care Act\'s coverage provisions have just taken effect, the recovery from the Great Recession is uneven, and anger at institutions is building on both left and right. The next test is the midterms in November. Your job: keep the party together, win elections, and keep American democracy intact through whatever comes next.' % (DEM(), GOP()))
N('both', 'dem_president = 0 and year = 2017 and month = 1 and just_inaugurated',
  'A new %s administration takes office. The %s are in opposition, and the question is how to resist without breaking the guardrails that protect everyone.' % (GOP(), DEM()))
N('both', 'dem_president = 1 and just_inaugurated and year >= 2017',
  'A new %s administration takes office. Governing will test the party\'s factions as much as the opposition does.' % DEM())
N('both', 'democracy_score < 40 and not game_lost',
  'Alarm bells are ringing: independent monitors warn that American democracy is in serious danger of backsliding.')
N('both', 'democracy_score >= 85 and year >= 2018',
  'Civil society and institutions appear robust; political scientists describe American democracy as resilient despite the polarization.')
N('rightnews', 'maga_strength >= 40 and maga_strength < 60',
  'The %s movement dominates Republican primaries and rallies, reshaping the party in its image.' % MAGA)
N('rightnews', 'maga_strength >= 60',
  'The %s movement has effectively captured the Republican Party; dissenters within the party are being primaried or silenced.' % MAGA)
N('rightnews', 'maga_strength < 25',
  'Establishment Republicans hold the party firmly; the insurgent right is restless but fragmented.')
N('rightnews', 'farright_strength >= 20',
  'Far-right militias and online extremist networks are growing, with rising reports of intimidation of election workers and officials.')
N('other', 'farleft_strength >= 25',
  'Left-wing protest movements and third-party groups are gaining strength, accusing the Democrats of betraying their base.')
N('both', 'unemployed >= 10',
  'Unemployment stands at [+ unemployed_2 +] percent; millions are out of work.')
N('both', 'inflation >= 6',
  'Inflation is running at [+ inflation_2 +] percent, squeezing household budgets and dominating political debate.')
N('both', 'months_to_election <= 3 and months_to_election >= 0 and not (year = 2014 and month = 1)',
  'Election season: the generic ballot and battleground polls show %s [+ dem_votes_d +] percent, %s [+ gop_votes_d +] percent.' % ('Democrats', 'Republicans'))

# --- exogenous world headlines ------------------------------------------------
W = [
 ('other', 'year = 2014 and month = 2', 'The Winter Olympics open in Sochi, Russia.'),
 ('other', 'year = 2014 and month = 3', 'Russia annexes Crimea following a disputed referendum; the West responds with sanctions.'),
 ('other', 'year = 2014 and month = 4', 'The Supreme Court strikes down aggregate limits on campaign contributions in McCutcheon v. FEC.'),
 ('other', 'year = 2014 and month = 6', 'ISIS seizes Mosul and proclaims a caliphate across parts of Iraq and Syria.'),
 ('other', 'year = 2014 and month = 7', 'Malaysia Airlines Flight 17 is shot down over eastern Ukraine.'),
 ('other', 'year = 2014 and month = 8', 'Protests erupt in Ferguson, Missouri, after a police shooting.'),
 ('other', 'year = 2014 and month = 9', 'Scotland votes to remain in the United Kingdom.'),
 ('other', 'year = 2014 and month = 10', 'A case of Ebola is diagnosed in Dallas, setting off a national scare.'),
 ('other', 'year = 2014 and month = 12', 'The United States and Cuba announce steps toward restoring diplomatic relations.'),
 ('other', 'year = 2015 and month = 1', 'Gunmen attack the offices of Charlie Hebdo in Paris.'),
 ('other', 'year = 2015 and month = 6', 'A white supremacist murders nine worshippers at a historic Black church in Charleston, South Carolina.'),
 ('other', 'year = 2015 and month = 7', 'Iran and six world powers reach a nuclear agreement in Vienna.'),
 ('other', 'year = 2015 and month = 9', 'A refugee crisis grips Europe; Pope Francis visits the United States.'),
 ('other', 'year = 2015 and month = 11', 'Coordinated attacks kill 130 people in Paris.'),
 ('other', 'year = 2015 and month = 12', 'Nearly 200 nations adopt the Paris climate agreement; the Federal Reserve raises interest rates for the first time since 2006.'),
 ('other', 'year = 2016 and month = 2', 'Supreme Court Justice Antonin Scalia dies, leaving a vacancy in an election year.'),
 ('other', 'year = 2016 and month = 6', 'A gunman kills 49 people at an Orlando nightclub. Days later, British voters choose to leave the European Union.'),
 ('other', 'year = 2016 and month = 8', 'The Summer Olympics open in Rio de Janeiro.'),
 ('other', 'year = 2017 and month = 8', 'A white-supremacist rally in Charlottesville, Virginia, turns deadly; Hurricane Harvey devastates the Texas coast.'),
 ('other', 'year = 2017 and month = 9', 'Hurricane Maria devastates Puerto Rico.'),
 ('other', 'year = 2017 and month = 10', 'A gunman kills 58 people at a Las Vegas concert. The #MeToo movement spreads after allegations against a Hollywood producer.'),
 ('other', 'year = 2018 and month = 2', 'A school shooting in Parkland, Florida, leaves 17 dead and mobilizes student activists.'),
 ('other', 'year = 2018 and month = 10', 'A gunman kills eleven worshippers at a Pittsburgh synagogue.'),
 ('other', 'year = 2019 and month = 3', 'A gunman kills 51 worshippers at two mosques in Christchurch, New Zealand.'),
 ('other', 'year = 2019 and month = 6', 'Mass protests erupt in Hong Kong.'),
 ('other', 'year = 2019 and month = 12', 'Chinese authorities report a cluster of pneumonia cases in Wuhan caused by a novel coronavirus.'),
 ('other', 'year = 2020 and month = 1', 'The novel coronavirus spreads across Asia; the first US case is confirmed.'),
 ('other', 'year = 2020 and month = 8', 'A massive explosion devastates the port of Beirut.'),
 ('other', 'year = 2020 and month = 12', 'The first COVID-19 vaccines receive emergency authorization in the United States.'),
 ('other', 'year = 2021 and month = 3', 'The Ever Given blocks the Suez Canal as vaccination campaigns accelerate.'),
 ('other', 'year = 2021 and month = 8', 'Kabul falls to the Taliban as the last Western forces withdraw from Afghanistan.'),
 ('other', 'year = 2021 and month = 11', 'The Omicron variant is identified; world leaders gather for the COP26 climate summit.'),
 ('other', 'year = 2022 and month = 2', 'Russia launches a full-scale invasion of Ukraine.'),
 ('other', 'year = 2022 and month = 9', 'Queen Elizabeth II dies after seventy years on the throne.'),
 ('other', 'year = 2022 and month = 11', 'OpenAI releases ChatGPT, setting off a race in artificial intelligence.'),
 ('other', 'year = 2023 and month = 3', 'Silicon Valley Bank collapses, shaking confidence in regional banks.'),
 ('other', 'year = 2023 and month = 6', 'The Wagner Group briefly mutinies against the Russian military leadership.'),
 ('other', 'year = 2023 and month = 10', 'Hamas attacks Israel on October 7, and Israel launches a war in Gaza.'),
 ('other', 'year = 2024 and month = 7', 'The Summer Olympics open in Paris.'),
 ('other', 'year = 2024 and month = 12', 'The Assad regime falls in Syria after a rebel offensive.'),
 ('other', 'year = 2025 and month = 1', 'Wildfires devastate Los Angeles County.'),
 ('other', 'year = 2025 and month = 5', 'Cardinal Robert Prevost is elected Pope Leo XIV, the first pope from the United States.'),
 ('other', 'year = 2025 and month = 6', 'Israel and Iran exchange strikes in a twelve-day war.'),
 ('other', 'year = 2026 and month = 2', 'The Winter Olympics open in Milan and Cortina d\'Ampezzo.'),
 ('other', 'year = 2026 and month = 6', 'The FIFA World Cup opens across the United States, Canada, and Mexico.'),
 ('other', 'year = 2026 and month = 7', 'The United States marks the 250th anniversary of the Declaration of Independence.'),
]
for cls, cond, text in W:
    N(cls, cond, text)

MAIN_ARRIVAL = """
if (Q.advisor_action_timer <= 0) {
    Q.pinnedCardsDescription = 'Advisors - an action is available';
} else if (Q.advisor_action_timer == 1) {
    Q.pinnedCardsDescription = 'Advisors - next action available in 1 month';
} else {
    Q.pinnedCardsDescription = 'Advisors - next action available in ' + Q.advisor_action_timer + ' months';
}
if (Q.shuffle_leadership_timer <= 0) {
    Q.pinnedCardsDescription += '\\n- a reshuffle is available.';
} else if (Q.shuffle_leadership_timer == 1) {
    Q.pinnedCardsDescription += '\\n- next reshuffle in 1 month';
} else {
    Q.pinnedCardsDescription += '\\n- next reshuffle in ' + Q.shuffle_leadership_timer + ' months.';
}
Q.last_time_updated = Q.time;
"""

MAIN_DISPLAY = """
if (!document.getElementById('news_tab')) {
    var button = document.createElement('button');
    button.style.backgroundColor = '#dddddd';
    button.className = 'tab_button';
    button.id = 'news_tab';
    button.textContent = 'View Right-Wing News';
    button.onclick = function () {
        toggleNews();
    };
    var contentDiv = document.getElementById('content');
    contentDiv.appendChild(button);
    const elements = document.querySelectorAll('.rightnews');
    let hasTextContent = false;
    elements.forEach(function (element) {
        if (element.textContent.trim() !== '') {
            hasTextContent = true;
        }
    });
    if (hasTextContent) {
        button.style.backgroundColor = 'rgba(255, 0, 0, 0.5)';
    } else {
        button.style.backgroundColor = '#dddddd';
    }
    document.querySelectorAll('p').forEach(p => {
        if (!p.textContent.trim()) {
            p.remove();
        }
    });
}
const boxes = document.querySelectorAll('.scrollable-box');
if (boxes.length >= 2) {
    boxes[1].remove();
}
"""

write('scenes/main.scene.dry', """title: Next month
is-hand: true
max-cards: 4
on-arrival: """ + js(MAIN_ARRIVAL) + """
on-display: """ + js(MAIN_DISPLAY) + """

# Here, the main deck will be displayed. Clicking on a deck draws a card into your hand. Clicking on a card plays that card (one action = one month).

{!<div class="scrollable-box">!}

""" + '\n\n'.join(news) + """

{!</div>!}

- @party
- @govt
- #advisor
- @shuffle_leadership_pinned

@party
title: Party Affairs
is-deck: true

- #party_affairs

@govt
title: Government Affairs
view-if: dem_president or dem_house or dem_senate or dem_governors >= 15
is-deck: true

- #govt_affairs
""")
print('core ok; news items:', len(news))
