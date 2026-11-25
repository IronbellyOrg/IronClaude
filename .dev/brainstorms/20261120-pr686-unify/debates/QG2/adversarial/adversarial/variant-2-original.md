# Position CLAY (QG2): escalation channel and naming rule

Paths: D:nnn = `docs/designs/orchestrator.md` on master (snapshot `/home/coder/.cache/ic-snap-20261120/master`). D15 = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md`.

## Claim
OD-3: scope A as ruled (ruling 15): nothing the poll, the orchestrator or a worker it started writes where a person reads it names the agent or model; the handoff prompt carries the rule for workers. OD-4: fail closed: a text that fails `names_check` is refused (exit 2, nothing written, nothing sent). OD-5: audit escalations (AU4a, AU4c, AU5) reach the person by entry lines plus the notice step (ClickUp DM or Orca unread mark), with the daily cap key at its default.

## Mechanism
- OD-3/OD-4: one function `names_check(text)` in `src/superclaude/cli/orchestrator/names.py` holds deny and allow lists as data, skips backtick spans, link titles and quoted-data fences, is run by `report-entry` and `escalate` (refuse, exit 2), by a test over every template, fixture and `gh`/`orca` body the end-to-end tests produce, and by a fake `launch.effective` test (D:847). Item 5 of the nine handoff-prompt sections tells workers never to add an attribution line (D:841).
- OD-5: an escalation reaches the person three ways (D:682): lines of the issue's own entry, an Orca decision gate, the notice. AU4a, AU4c and AU5 are written as entry lines, "one escalation per pull request, never one per finding", warnings never reach the person (D:825 item 2, AD-E1, ruling 27).

## Cited facts
1. Ruling 15 (2026-11-19) is the stated source of the rule (D:830): people are credited by name, never the agent, so a reader of a report sees who is responsible. The design lists seven places a person reads text and what the rule does to each (D:836-845).
2. The rule is already narrowed by its author: the one exception is the repository's commit trailer (ruling 39, D:832); review apps' names are allowed; quoted data is skipped (D:847). AD-X1 (ruling 28) already declined a ninth audit check for worker PR bodies (D:847, D:1205).
3. A refusing writer is the cheapest way to make a rule real: `escalate` already refuses an entry that names no row (exit 2, nothing written, nothing sent; D:684). Refusal is the design's one style for bad input, so a text check that refuses is consistent.
4. A fail-open path is a bypass: "the rule is bypassed for that text" (D15 OD-4 wording). A rule with a built-in exception is not a rule, and a masked span changes the text a person reads without saying so.
5. The false-positive risk is bounded by data, not guessed: U54 (D:1312) measures the deny list over the last 50 titles; R2-OURS found 1 title with "IronClaude" and 6 with "Jev" in 50 (a measurement, not a verdict, D15 INV-013).
6. The notice exists for what entry lines cannot do: reach a person who is not reading the report. AU4a, AU4c and AU5 are the cases where the merged result is possibly broken or unreviewed (D:825 item 2); INV-014 shows the audit arrives after the merge on an unprotected `master`.
7. The cap makes the notice safe: `reach_daily_max` 0 to 50, never drops an entry, a notice over the cap is held and sent as one DM later (D:686). The table has nine rows with a "Was" column mapping the older rules (D:676-680), and "If you do not answer" lines (D:692).
8. The notice step needs no new design from the owner: it is the third of three ways already written (D:682), and `answer-check`, `escalate` and `report-entry` are being built in one verb group (D15 R-7).

## What it costs
- Scope A needs the handoff line plus a check that cannot scan worker PR bodies (D:847), so it is a convention for the largest class of writers.
- Fail closed can leave a mandatory escalation unwritten; a coordinator that has just been refused must rewrite the text or the person is not told.
- The notice step costs a ClickUp DM sender or Orca unread mark (not shown built in master; UNVERIFIED), the nine-row list, and a cap decision.

## What it risks
- 25 of 30 recent merged PR bodies carry "Generated with" (counted read-only: clayphi 17 of 21, ironbelly 8 of 9); scope A makes today's practice a violation.
- INV-013: a refused merge-safety escalation (the files list holds `.claude/settings.json` and the repo is IronClaude) fails silently.
- Cap default 0 means no cap (`pr-a/.../repos.py:262-269`); a bad value reads as no cap (INV-003); a burst of audit notices is possible.

## What it gets right
Plain credit to people is a legitimate goal, the design tests it end to end, and the notice reaches a person who is away. The escalation shape (one per PR, warnings never reach the person, entry always written) is careful and fits the owner's decision-only rule.

