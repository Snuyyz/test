# Social Democracy: An Alternate History - Dynamic America (2014-2026)

A mod/port of *Social Democracy: An Alternate History* (Dendry engine) to US politics.
You play the **Democratic Party**, month by month, January 2014 - December 2026.
Real-world shocks (Ukraine, COVID, inflation, Gaza...) happen around you, but **elections,
nominees, who holds power and whether democracy survives are decided by your play**, not by history.

## Build (needs network once)
```
npm install
npx dendrynexus make-html      # same tool as the original project
```
Output goes to `out/html/` (game.json + the UI files already included).
To use it as a mod in the original UI, host the compiled `game.json` and load it from the Mods screen.

## Mechanics carried over from the original
- One action = one month; hand of 4 cards drawn from decks (Party Affairs / Government Affairs); "return card to hand" option
- Advisors as free actions every 6 months; leadership reshuffle
- Resources, annual dues, party dissent, six factions with strength/dissent
- Demographic-group x party vote matrix driving elections (6 groups, 5 "parties" incl. non-voters)
- Relations, forces (militias, civic mobilization, military/police loyalty), rising enemies
- Economy (unemployment / inflation / growth / budget), event system with priorities, endings + achievements

## US-specific conversions
- Electoral College (5 state blocs), House seats with gerrymander bias, Senate map by cycle, midterm turnout drop
- Government cards unlock only with the powers needed (presidency / House / Senate)
- Election-night screens (`election_presidential`, `election_midterm`) show d3 charts: House and Senate hemicycles (with change vs. the outgoing Congress) and, for presidential years, an Electoral College bar + per-bloc table. Scenes emit `<div class="sd-chart" data-chart="house|senate|ec" ...>` placeholders; `out/html/game.js` (`renderElectionCharts`) fills them in.
- Enemies: MAGA movement (subversion meter -> contested-election crisis), far-right militias, far-left splinter
- Nominee choice each cycle; GOP nominee depends on how strong the insurgent movement has become

## Dev tools (tools/)
`gen_*.py` regenerate every .dry file; `sd_lib.js` is the shared engine (injected into root/post_event);
`validate.py` static checks; `test_ops.py` executes every effect; `sim_game.py N policy` plays N full games
(`idle`, `random`, `greedy`) for balance testing.

## Status
Statically validated, simulated headlessly, and compiled successfully with dendrynexus (`npx dendrynexus make-html`).
