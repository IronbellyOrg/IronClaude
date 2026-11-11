# Shared design contract

## Ownership
Parent owns fixtures.py, canvas.py, render.py, tests, fixture/scenario JSON, gallery and exports. Group A owns layouts/group_a.py only; group B owns layouts/group_b.py only. No nested delegation, skills, debate or external research. Do not edit other files. Return bounded findings directly if report writing is restricted.

## Layout interface
Read fixtures.py and canvas.py. Implement `DESIGNS = {slug: {'name': name, 'question': five_second_question, 'omits': text, 'tradeoff': text, 'data': text, 'missing': text, 'render': function}}`.
Each render function signature `(c, f, m)` mutates Canvas; no return required. Canvas is freshly created at widths 160/144/116/80, height 48 for wide and 42 compact/narrow. Call c.header(name,f,m) and c.footer(). Body rows 5 through c.h-4. Horizontal inset 1 or 2. Use c.text(...width=...), c.panel, c.bar, c.line and c.lines from canvas.py. All positions must be in bounds. c.regions records panels for tests. Panel bodies must not overwrite border rows. Empty/missing records must render a useful view, not crash. No hardcoded session/owner counts; use m/f. Respect varying 5/8/10 owners and 50/80/100 sessions, uneven/shared/unmapped/historical, stale, missing fields and empty fixture. c.ascii translates rendering to ASCII. Safe text clip handles wide glyphs; full record detail is supplied by gallery.

## Required semantics
All fixture values synthetic. Worker result is not admission. Dirty != dangerous; stale != failed; overlap != conflict; partial cost subtotal != total spend; tokens != progress. Evidence flags must use current revision equality. Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only. Handle messages coverage unavailable vs partial. Header prints scope/freshness. Narrow views retain first human decision + owner + affected scope/freshness; use selected_summary helper if needed. Show omission counts when limited. Data model is proposed fixture schema, never Orca API schema.

## Distinct visual geometry
No repeated equal card grid. Group A: Signal Bridge, Fleet Quilt, Time Loom, Worktree Atlas, Decision Desk. Group B: Proof Gate, Budget Engine, Relay Map, Delta Deck, Watchkeeper. Wide compositions 160/144; 116 must rearrange, 80 must simplify to selected detail. Favor strong framed hierarchy, fine dim rules, quiet white values, amber attention and labeled semantic markers. Meaningful patch cables only on Relay Map using f.edges. Distinct screen silhouettes even without titles/colors. Time lanes are 20 equal buckets across 60 minutes: work/review/queue/dependency/gap with legend. No scale invented from elapsed time.

## Bounded execution
Use <=300 lines per module where practical. Complete actual Python render functions, not prose mockups. No third-party code/assets copied. Parent runs exports/tests. One targeted fix handoff if integration exposes a real issue; no repeated design review cycles.
