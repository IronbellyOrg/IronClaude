<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (opus:analyzer, CLAY position paper) -->
<!-- Merge date: 2026-11-20 -->

# D11 merged recommendation: one data source, one report, one dashboard

Topic: Observability stack: work report, sweep, observer, TUI dashboard.

Source conventions (kept from the two position papers):

- "M:" is the read-only export of origin/master 61ac2c2e6 at `/home/coder/.cache/ic-snap-20261120/master`. "A:" is the PR 686 head export `pr-a` at `/home/coder/.cache/ic-snap-20261120/pr-a`.
- A path with no prefix is under `src/superclaude/` of the master export unless it starts with `docs/` or `.dev/`.
- "UNVERIFIED" is kept wherever the inputs call a point UNVERIFIED. Nothing in this file is a new fact: each one comes from the two position papers, the debate transcript, the invariant probe or the refactoring plan, and carries its source.
- Rules and facts are cross-referenced as "rule N" (section "Testable rules for the spec") and "F N" (section "Cited facts").

## The claim

<!-- Source: Variant 1 (opus:architect), Section The claim - merged per Change #1 (debate outcome X-001 HYBRID 73%, C-002 HYBRID 75%, C-003 CLAY 80%) -->

The sweep JSON (schema version 1) is the one source of session facts. The observer is the one screen. The work report is the one plain-English report and the work-item layer (GitHub, ClickUp and per-issue text), and it meets the asks Clay made on issue 409 today (F 4, F 5). Clay's report features are adopted as listed in the section "Adoption table for Clay's features". Do not hold the working report behind unwritten design.

Why this split, in one line each:

- The sweep is a zero-token, read-only script with proof-based classes and runs at most every 5 minutes; it belongs at the bottom (F 3; X-001, OURS 75% in Round 1, CLAY advocate conceded).
- Only the report gives a person, per issue, what is done, what is left, whether it needs them, and a link, and the observer's Decision Desk is "NOT BUILT" (F 4, F 5; C-003, CLAY 80%).
- The sweep has no GitHub call and no summary text, so the work-item layer has to come from the report's code, joined to the sweep, not run as a parallel stack (F 3, F 4; C-002, HYBRID 75%).

One exception to "one data source" stays open for the owner: the observer's own questions panel is a second Orca reader (rule 9, INV-005).

## The mechanism

<!-- Source: Variant 1 (opus:architect), Section The mechanism - merged per Change #2 (three layers plus the notice step; X-001, X-002) -->
<!-- Source: Base (original, modified) - entry files, join, sort, compare and gate (base mechanism items 1 to 3) kept inside Layer 2 and the notice step -->

Direction of data: session facts flow from the sweep to the report; work items flow from the report to the observer (X-001, HYBRID 73%).

| Layer | What it is | What it reads | What it costs |
|---|---|---|---|
| 1. Facts | The sweep (`superclaude sweep run`, JSON schema v1, PR 539). It classifies every session by fixed rules into eight classes. | Orca (only the fixed `ALLOWED_ORCA` commands), git state, transcripts, package ledgers (F 3). | No model. At most one run per 5 minutes (WC-16). |
| 2. Work items | The report skill (PR 684). One entry file per issue the orchestrator holds, in a per-user, configurable state folder (today `.dev/coordinator/orchestrated/`). The daily run leaves those issues out (`exclude.py`, Step 4b), so nothing is reported twice. | Session facts from the sweep JSON; GitHub and ClickUp through `collect.py` and `clickup.py`; each session's transcript from the saved position, for the session ids in rule 5 (F 2, F 7). | One model step per daily run; `run.py refresh` rebuilds the page with no model call (F 8). |
| 3. Screen | The observer (`superclaude observe`, issue 409). | The sweep JSON for sessions; the report's entry files for work items. | No model. Navigation only, no recommendation, no write (section "Read-only and recommend-nothing rules"). |

Layer 2 in detail (base items 1 to 3, kept):

1. Entry files and the living page: one entry file per issue; `run.py refresh` rebuilds the shared page from the last daily report plus the entry files with no model call (M:skills/agent-work-report/SKILL.md, "The living report" and Step 12).
2. Everything else is joined into one item each (`match.py`), sorted by fixed rules (the report skill's `classify.py`), compared with the previous report (`compare.py`) and checked by script before delivery (`check.py`, then `run.py gate` prints PASS). "No report that failed a check reaches Clay" (M:skills/agent-work-report/SKILL.md Step 11).
3. The session split (C-001, HYBRID 70%): the sweep finds sessions and judges their state, because its classes follow written proof rules while `sessions.py` says "status is decided by the model from these facts" (M:skills/agent-work-report/scripts/sessions.py:5-6). The report keeps reading what each session did from its saved transcript position, because the sweep reads only a 256 KiB tail (M:cli/sweep/probes.py:865-867).

Notice step (detail in the section "The notice step: nine rows and the cap"): one table of nine rows says what may reach the person; anything else the orchestrator decides and records; a notice (DM or unread mark) is capped per repo per 24 hours, as a proposed default; the entry on the page is never dropped (M:docs/designs/orchestrator.md:664-696, 1177).

Order of work (X-002, HYBRID 68%): the report keeps running as it is. The contract note `docs/designs/observe-sweep-contract.md` (not written, F 1) and the `session_id` field (rule 1) come next; then the report switches its session reads to sweep data, under rules 5 and 6.

## Testable rules for the spec

<!-- Source: Debate evidence (invariant-probe.md, Round 2.5, INV-001 to INV-012) - merged per Change #3 -->

Twelve rules, each testable, each naming the finding that forces it. Rules 5 and 6 are the two HIGH findings that blocked convergence (AD-1); they are written here as required statements, which is how the standard-depth gate is cleared (invariant-probe.md, "Convergence gate"). The other findings are carried as open requirements. Evidence paths are as in the probe.

1. **The sweep JSON v1 row gains `session_id` and `worktree_path` as additive fields, each allowed to be empty (INV-003, MEDIUM).** This is a reviewed edit to the golden test (NFR-009, `docs/designs/orchestrator-mode.md:605`; test `sweep/test_cli_contract.py`, `orchestrator-mode.md:817`). `row_id` is not a contract: it holds the session id only for transcript rows (`transcript:<session id>`, `cli/sweep/classify.py:933`, falling back to the file name at `:923`), and Orca rows get `orca:<dispatch>` with no session id (`:903`). Test: a row built with no join still passes the contract with both fields empty.
2. **One session shown as two rows is merged by `session_id` where both rows have one (INV-003, MEDIUM).** When the `orca-tabs` join is empty or stale the join fails (`cli/sweep/classify.py:69`, `:890-903`) and the transcript can appear again as a separate `transcript:` row; transcript-only rows have `orca=None` (`:924-933`) and `TranscriptTail` keeps only `project_key` (`cli/sweep/models.py:129-140`), so they have no worktree path. Test: a fixture with an Orca row and a transcript row for one session produces one merged row.
3. **The sweep JSON is saved as a file next to the Markdown report, or the spec says each consumer runs its own sweep (INV-006, MEDIUM).** Today the JSON is printed to standard output only (`cli/sweep/commands.py:277-278`) and only the Markdown report is saved (`:182`). The observer polls every 15 s (`cli/observe/commands.py:391`) while WC-16 bounds sweeps to one per 5 minutes (`docs/designs/orchestrator-mode.md:681`). The owner decides which (open decision 4).
4. **The report passes `--window` equal to the time since the previous report, and 24 h on the first run (INV-007, MEDIUM).** "Idle" in the sweep window never means "no progress since the previous report". The sweep window defaults to 6 h (`cli/sweep/commands.py:27`) and a session idle before the window is "idle" and "historical" (`cli/sweep/classify.py:303-310`, `:977`); the report covers everything since the previous report, or 24 h on the first run (`skills/agent-work-report/scripts/sessions.py:14`, `:48`). A session that progressed 10 h ago would otherwise read as idle.
5. **HIGH (INV-001): the report reads transcripts for the session ids in the sweep rows PLUS every not-done session of the previous report, even when its terminal or worktree is gone.** A session is closed only by a source-confirmed reason, as today (`skills/agent-work-report/scripts/sessions.py:378-400`, which keeps any not-done session and reads on from the saved `read_offset`). The sweep reads transcripts only from the Claude project folders of the root plus the worktrees `worktree ps` returns (`cli/sweep/probes.py:1308-1319`, `:1445-1468`); a removed worktree drops out of the sweep, so reading only sweep ids would drop it and break "carry items, never close them". Test: a not-done session of the previous report whose worktree is gone is still read and still carried.
6. **HIGH (INV-002): before the report's own terminal-to-session map is removed, one live side-by-side run compares the sessions both maps find; the old map stays until the sweep's `orca-tabs` map finds every session the old one finds.** The old map is `orca terminal list` plus the Orca hook file (`sessions.py:291-334`); its own evidence is "VERIFIED live 2026-10-30, 15 of 18" (`sessions.py:9`). Which map covers more is UNVERIFIED (both rebuttals). A fixture test alone does not satisfy this rule, because once the old map is removed the check can run only on fixtures.
7. **"Orca unavailable" or "sweep failed" is written as `read: false` in the report's session step; the previous reads are skipped, never read as "sessions ended" (INV-004, MEDIUM).** With Orca down `_worktree_paths` returns only the root (`cli/sweep/probes.py:1310-1311`) and the JSON then says only `orca_available` (`cli/sweep/report.py:632`). Today `sessions.py:282-306` writes `read: false` when it cannot read, and `previous_reads` skips those runs (`:77-96`).
8. **The report skips the coordinator's own workspace session; the counts of the two tools are compared only after that skip; totals from the sweep are lower bounds (INV-010, MEDIUM).** The report skips the coordinator's workspace (`sessions.py:325`); the sweep always includes the root (`cli/sweep/probes.py:1310`) and adds person-started and historical sessions, while the report counts only Claude sessions in Orca terminals. `total_is_lower_bound` is always true (`cli/sweep/classify.py:986-989`).
9. **The observer's coordinator-questions panel is a second Orca reader (INV-005, MEDIUM). The spec states it as an accepted exception, or the sweep gains a questions block; the owner decides (open decision 3).** `QUESTION_GATE_PASSED = True` (`cli/observe/commands.py:67`); the observer itself calls `orchestration check --all --types question` (`cli/observe/adapter.py:32`); the sweep JSON has no question data (`cli/sweep/report.py:619-695`). The probe says this condition alone falsifies "one data source" unless one of the two is chosen.
10. **One question gets one id across the observer (Run, message id), the sweep (`row_id`) and the report (issue URL), or the three are shown as separate lists; no duplicate "Needs you" and question row (INV-009, MEDIUM).** The three keys today: observer (`cli/observe/questions.py:29`, `:76-78`); sweep waiting rows `row_id` (`cli/sweep/classify.py:994-999`); report entries, the issue URL (`exclude.py` docstring). There is no shared id.
11. **Entry files store only `session_id`; the class is read from the sweep at display time (INV-008, MEDIUM, ADDRESSED in part).** `refresh` takes each session's status from the entry file (`docs/designs/orchestrator.md:122`) and `exclude.py` removes those sessions from the daily run, so the observer would otherwise show the sweep class beside an entry-file status that can disagree.
12. **The observer shows text from entry files only after `cli/observe/sanitize.py`; an empty `orchestrated/` folder and zero sweep rows each show an explicit "none", separate from "could not read"; a list cut at the 100-row page or the show cap says "lower bound" (INV-012, LOW).** The worker list pages at `--limit 100` (`cli/observe/adapter.py:29`); a row cut by the show cap counts to `bound_reached` (`cli/sweep/classify.py:979`) and becomes "could not determine". Entry text comes from GitHub and ClickUp; `page.py` HTML-escapes it (`page.py:62-81`) but nothing says the observer runs it through `cli/observe/sanitize.py:27`. UNVERIFIED: whether `sanitize.py` already handles arbitrary file text.

The cap finding (INV-011, LOW) is handled in the section "The notice step: nine rows and the cap", not as a thirteenth rule. The probe reviewed master only, not pr-a or pr-p.

## Read-only and recommend-nothing rules

<!-- Source: Variant 1 (opus:architect), Section Cited facts item 3 - merged per Change #4 (C-004, OURS 83%; CLAY conceded 85%) -->

- The sweep (`skills/sc-sweep-protocol/SKILL.md:61`: "Recommend anything, propose an action, or add advice" is a Will Not) and the observer (navigation only, issue 409 item 2) carry no Options, no Recommendation and no write.
- Options, Recommendation, the typed answer, the ClickUp DM and the commit of the report's own state folder belong to the report or the orchestrator session only (templates/needs-you-template.md; M:docs/designs/orchestrator.md:690).
- Whether the observer may show an entry's text word for word, labelled as from the report, is an owner decision (UNVERIFIED; open decision 2).

## Person-specific values and naming

<!-- Source: Variant 1 (opus:architect), Section Cited facts item 4 - merged per Change #5 (C-005 OURS 73%, C-010 OURS 73%) -->
<!-- Source: Base (original, modified) - the base's cost line on one-person config and naming drift kept and turned into a rule -->

- `person`, the time zone, the ClickUp user and token and the DM channel move to per-user config; the shipped `config.json` names no person (today: `"person": "clayphi"`, America/Chicago, one ClickUp token; F 9).
- The skill's text follows the owner's naming (coordinator, not orchestrator) and layout (`.dev/coordinators/`, not `.dev/coordinator/`; F 10). D08 settles the final name.
- The report still needs `$AWR_ROOT` or `orchestrator_repo` (M:skills/agent-work-report/scripts/common.py:35-50), so it is not zero-setup (A-004: both advocates accepted that the "zero-setup" assumption is false).

## The notice step: nine rows and the cap

<!-- Source: Variant 1 (opus:architect), Section Cited facts item 7 and Mechanism item 4 - merged per Change #6 (C-006 HYBRID 75%) and Change #7 (C-007 HYBRID leaning OURS 63%) -->

**Nine rows (Change 6).** Adopted with "the person" instead of Clay (row 1 says "his own identity", M:docs/designs/orchestrator.md:672; A-002). The table lives in the notice step only. The sweep and the observer never pick a row; they may show the row number an entry already records. The planned test "exactly nine rows" is kept (M:docs/designs/orchestrator.md:1116). The rule "when in doubt, a case does not reach Clay" stays (M:docs/designs/orchestrator.md:668). Rows 1 to 7 are never low-stakes. Choosing a row is a judgment, and the sweep refuses judgments (`skills/sc-sweep-protocol/SKILL.md:61`).

**Cap of 5 notices a day (Change 7).** Adopted as a PROPOSED default of 5 per repo per 24 hours, for notices only; entries are never dropped (M:docs/designs/orchestrator.md:686). It is not "settled":

- Ruling 39 is Clay's, not the owner's. The design says so by implication, not in that line: line 3 calls the design "approved by the owner (Clay)" under ruling 37; line 1170 lists "Clay's rulings 23 to 35" and then "ruling 39" without naming who made it; lines 688 and 877 say the cap changes "only on Clay's recorded word" (all M:docs/designs/orchestrator.md).
- AD-B4 calls the cap "not ruled on; open", and says "5 is this design's number; Jay's own default is 0, no cap" (M:docs/designs/orchestrator.md:1177).
- An absent key means 0, which is no cap (M:docs/designs/orchestrator.md:686), and the built parser returns 0 for an absent or bad value (A:cli/issue_watch/repos.py:262-269; the config key is `reach_daily_max`, parsed at `:91,262`).
- The `escalate` verb and the file `asks.json` that would enforce it do not exist in master, pr-a or pr-p (greps found none). The cap counts per `<short>` (per repo) in `asks.json` (M:docs/designs/orchestrator.md:684-688).
- No generator writes a value until the owner records a ruling (INV-011, LOW; open decision 1).

## The living report and the status words

<!-- Source: Base (original, modified) - living report kept (base mechanism item 1, cited fact 7); extended per Change #8 (C-009 HYBRID 72%, C-008 OURS 78%, INV-008) -->

- The report keeps its entry files with a per-user, configurable state path, and `refresh` stays model-free (M:skills/agent-work-report/SKILL.md line 16).
- The six work-item words (working, progressed, waiting on you, stuck, stalled, done) stay for work items only.
- Any session state on the screen is the sweep's class word for word (the sweep has eight classes, including "could not determine"; M:cli/sweep/models.py:50-59). Entry files store only the `session_id` (rule 11).

## Adoption table for Clay's features

<!-- Source: Variant 2 (CLAY), Section Final recommended merge (d), as modified by the debate outcome - merged per Change #9 -->

| Feature | Verdict | What changes | Evidence |
|---|---|---|---|
| Living report | Adopt with change | The state path becomes configurable per user; entry files take sweep facts and store only `session_id` (rule 11); `refresh` stays model-free. | C-009 HYBRID 72%; SKILL.md line 16; F 8 |
| Nine rows | Adopt with change | "The person" in place of Clay; the table lives in the notice step only; the sweep and observer never pick a row; the "exactly nine rows" test is kept; rows 1 to 7 are never low-stakes. | C-006 HYBRID 75%; A-002; orchestrator.md:668, 672, 1116 |
| Cap of 5 notices a day | Adopt as a proposal, not settled | Proposed default of 5 per repo per 24 hours, notices only, entries never dropped; no generator writes a value until the owner records a ruling. | C-007 HYBRID leaning OURS 63%; INV-011; orchestrator.md:686, 1177 |
| Silent-loss check | Adopt as is | Stays in the report layer so the sweep stays stateless and zero-token. | U-005 CLAY adopted as HYBRID 80%; SKILL.md:21-24 |
| Plain-English item template | Adopt with change | Generic wording for the person instead of Clay; the observer's Decision Desk shows the same fields. | templates/item-template.md; F 4 |
| `check.py` gate | Adopt as is | `check.py` gates delivery; `run.py gate` prints PASS. | SKILL.md Step 11 and line 24; F 4 |

## Cited facts

<!-- Source: Base (original, modified) - base cited facts 1 to 8 merged and de-duplicated with Variant 1 (opus:architect) cited facts 1 to 8 and the debate corrections, per Change #10 -->

1. **Two collectors on master do not talk.** `observe/` has zero references to `sweep` (`grep -rn sweep src/superclaude/cli/observe/*.py` returns nothing). The fix, "read the sweep's JSON", is in issue 409 and in `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`, which lists the contract note `docs/designs/observe-sweep-contract.md` as "NOT WRITTEN"; `find` over the master export finds no such file. It has been unwritten since 2026-11-13. Waiting for it delays a daily tool that works now.
2. **The report is a third reader of Orca sessions.** `sessions.py` finds terminals through `orca terminal list` and the Orca hook file and reads transcripts from a saved position (M:skills/agent-work-report/scripts/sessions.py:1-28); `collect.py` reads GitHub; `clickup.py` reads ClickUp. No file in the skill refers to `cli/sweep` or `cli/observe` (the only hit for "sweep" is an unrelated paging function in `clickup.py`). Its status is "decided by the model from these facts" (`sessions.py:5-6`).
3. **What the sweep is.** It may call Orca only through a fixed list of command templates, `ALLOWED_ORCA` (M:cli/sweep/probes.py:49-56), has no GitHub call (a grep for `gh` and `api.github` in `cli/sweep/*.py` finds none), uses no model, and classifies into eight classes by fixed rules (M:cli/sweep/models.py, `CLASSES`; "could not determine", `models.py:50-59`). The coordinator runs it on every wake, at most every 5 minutes (WC-16, M:core/WORKER-CONTRACT.md:287). It reads only a 256 KiB transcript tail (`probes.py:865-867`). It splits people-waiting rows only by kind a or b, with no reason list (M:cli/sweep/report.py:230-236, 282-286). A search of `cli/sweep/` found no comparison with a previous run (Variant 1 rebuttal); for the observer this was not checked (UNVERIFIED).
4. **The report answers the issue 409 asks.** Issue 409 comment of 2026-11-11 by `clayphi`: "a simple plain english summary of the task/issue, whats done, whats left to do, and if it needs me. Link to the pr/issue". `templates/item-template.md` (73 lines) lays out state (one of nine), priority, Done with evidence, Still to do, Needs you, Next and links, and `check.py` fails an item that departs from it (M:skills/agent-work-report/SKILL.md:10). Issue 409 "Alignment decisions": item 1, read "the sweep's JSON, not a second collector"; item 2, the observer is "navigation only"; item 3, the asks "need GitHub reads and phase data. Phase 1 excludes GitHub reads, and the sweep has no per-session summary text. Decide which phase adds them". The Decision Desk is "NOT BUILT" (alignment spec 0.3). The sweep JSON v1 also lacks per-item plain-English text, issue and PR links, a step flow and a session-open link (issue 409 item 1); adding them is an additive change to schema v1 or a schema v2.
5. **The report is built and tested.** PR 684 "move the agent-work-report skill into IronClaude and add the living report" merged 2026-11-20 02:01 UTC; it adds 10,488 lines in 28 files, moves the IronFlow test (102 cases kept) and adds 28 cases (PR 684 body); `tests/skills/test_agent_work_report.py` has 142 test functions and 4,005 lines (M: `grep -c "def test"`). The waker automations were "VERIFIED 2026-11-03" (SKILL.md Input section). The page is served at 127.0.0.1:8765 and opened as a tab in Orca (SKILL.md Step 13).
6. **No silent loss.** "Every item open in the previous report is listed or closed with a reason the source confirmed; a failed read carries items, never closes them"; every source not read is listed under "Not checked"; an unanswered "Needs you" entry stays until answered (M:skills/agent-work-report/SKILL.md:21-24, "Why This Process Works").
7. **What the report reads that the sweep does not.** GitHub items across both orgs and Projects boards, ClickUp tasks, DM replies and each session's transcript from where the last report stopped (prompts, files written, git commands, item URLs; up to 30 MB on the first run) (`sessions.py:1-28`, `:14-17`, `:142`, `:170`, `:346`).
8. **Cost of the report.** "Target: about 5 minutes and well under 1M new tokens a run" (SKILL.md line 10); Step 10 is "MODEL". The living page costs no model call: `run.py refresh` rebuilds it from the last daily report plus the entry files "with no model call" (SKILL.md line 16), so only the daily run spends tokens.
9. **The report is built for one person and writes outside.** `config.json` sets `"person": "clayphi"`, time zone America/Chicago, that person's ClickUp token and session tag `coordinator` (M:skills/agent-work-report/config.json:2, 6, 11). The notice is a ClickUp direct message (SKILL.md Step 13; M:docs/designs/orchestrator.md:666) and the report commits its own state folder (SKILL.md Step 14). The sweep and observer write nothing outside their own report or state folder. The skill exits without `$AWR_ROOT` or `orchestrator_repo` (M:skills/agent-work-report/scripts/common.py:35-50).
10. **Naming drift.** PR 684's skill still says `/sc:orchestrator` and `.dev/coordinator/` (singular) (SKILL.md:12, 14); the owner's naming (coordinator) and layout (`.dev/coordinators/`) have not yet cleared it.
11. **Two rule sets.** The sweep "will not recommend anything, propose an action, or add advice" (M:skills/sc-sweep-protocol/SKILL.md:61); the observer's contract is "navigation only" (issue 409 item 2); the report's entries carry Options, a Recommendation and a typed answer (M:skills/agent-work-report/templates/needs-you-template.md; orchestrator.md:690).
12. **The join key is not in the JSON yet.** A sweep JSON v1 row carries `row_id`, `class`, `waiting_kind`, `rule`, `evidence`, `notes`, `policy`, `person_started` and `safe_to_close` (M:cli/sweep/report.py:642-661), with no `session_id`, terminal handle or `worktree_path` (`report.py:612-695`). The sweep's models do carry `worktree_path`, a `session_id` on the transcript record and a `TabMapEntry` linking `session_id` to `terminal_handle` (M:cli/sweep/models.py:103, 131, 146-148). UNVERIFIED: that a transcript file name always equals its session id. The v1 keys are pinned by a golden test (NFR-009, `docs/designs/orchestrator-mode.md:605`; `sweep/test_cli_contract.py`, `:817`); five keys were already added under NFR-009's additive-only rule (`:850`).
13. **The table and the cap are spec text.** Nine rows and the notice rule: M:docs/designs/orchestrator.md:664-696, 1164 (ruling 39, OD13), 1177 (AD-B4); the test "exactly nine rows" is planned at line 1116. Escalations go into each issue's own entry on the living page (orchestrator.md:666, 682). In PR 686's head the only trace of the cap is the config key `reach_daily_max` (A:cli/issue_watch/repos.py:91, 262); no `escalate` verb, no `orchestrator` command group and no `asks.json` exist in master, pr-a or pr-p. Nothing built depends on the table or the cap.
14. **The observer reads Orca by itself.** It polls `worker-list` (M:cli/observe/adapter.py:29) and, with the questions panel on (`QUESTION_GATE_PASSED = True`, M:cli/observe/commands.py:63-67, turned on by a recorded owner pass), the coordinator's open questions (`adapter.py:32`).
15. **Design order.** The PR 681 design never mentions sweep, observe or issue 409 (H-design681-map.md lines 10 and 59, in `/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/`), although the analyst map calls the living report "a third view beside `/sc:sweep` reports and the observer" (line 59). The owner's alignment decisions (PRs 587 to 589) set the chain watcher, then orchestrator, then dashboard. The owner's standing rule for automated reports is to show outstanding user decisions only, no heartbeat or timeout chatter (owner memory "Orchestration decision ledger only"); the cap and "when in doubt" agree with it.
16. **Two terminal-to-session maps.** The sweep reads `ccsession/orca-tabs` (`cli/sweep/probes.py:870-871`); the report reads Orca's agent-hook file `last-status.json` and falls back to the ccsession tag (`sessions.py:9-13`). Which covers more sessions is UNVERIFIED. The evidence for rules 1 to 12 is cited inside each rule and is not repeated here.

## What it costs

<!-- Source: Base (original, modified) - base cost list kept; extended per Change #10 with Variant 1 (opus:architect) costs and the debate findings -->

- One more place a person reads (page, DM, session summary) beside the sweep report and the TUI. For a while three outputs exist, because the report keeps working meanwhile (Variant 1 costs).
- The report is tied to one person today and its model step costs tokens each day (F 8, F 9).
- PR 684's skill still says `/sc:orchestrator` and `.dev/coordinator/` (F 10).
- The report is not zero-setup: it exits without `$AWR_ROOT` or `orchestrator_repo` (F 9; A-004).
- A contract note and a pinning test, named in the alignment spec and not written, before the observer can read the sweep JSON (F 1).
- The JSON field and golden-test edit: `session_id` and `worktree_path` need a reviewed edit to the NFR-009 test (rule 1; A-003: cheap, not free). The per-item text, links, step flow and session-open link of issue 409 item 1 are a further additive change or a schema v2 (F 4).
- The two-map coverage check: one live side-by-side run before the old map is removed (rule 6).
- The observer questions exception: either the spec carries a second Orca reader or the sweep gains a questions block (rule 9).
- The cap ruling: the owner must record a ruling before any value is written (open decision 1).
- A saved JSON file, or a spec for how each consumer runs its own sweep (rule 3).

## What it risks

<!-- Source: Base (original, modified) - base risk list kept; each risk now carries a mitigation taken from the plan or the debate; extended per Change #10 -->

| Risk | Mitigation | Source |
|---|---|---|
| Three overlapping readers of Orca sessions (sweep, observer, `sessions.py`) can disagree about one session's status; the report's six words differ from the sweep's eight classes. | The sweep finds sessions and judges state; the screen shows the sweep class word for word; the six words stay for work items only; entry files store only `session_id`; the old map is removed only after the side-by-side run. | C-001, C-008; rules 6 and 11; section "The living report and the status words" |
| The report's DM and commit steps are writes the sweep and observer rules forbid. | Options, Recommendation, typed answer, DM and commit stay in the report or the orchestrator session; the sweep and observer carry none. | C-004 (OURS 83%); section "Read-only and recommend-nothing rules" |
| The unification stays on paper: the contract note has been "not written" since 2026-11-13. | Do not freeze the report; write the contract note and add the `session_id` field next, then switch the report's session reads. | F 1; X-002 HYBRID 68%; section "The mechanism" |
| Clay's real daily need stays unmet for months because the Decision Desk is "NOT BUILT". | The report is the work-item layer and meets the issue 409 asks today. | F 4; C-003 (CLAY 80%) |
| Adding fields to the sweep JSON breaks the golden test or understates the cost. | The fields are additive and allowed to be empty; the golden test gets a reviewed edit; there is a precedent of five added keys. | Rule 1; F 12; A-003 |
| The report loses sessions of removed worktrees, or closes sessions when Orca is down. | Rule 5 (read previous not-done sessions) and rule 7 (`read: false`, previous reads skipped). | INV-001, INV-004 |
| A session found by the old map is missing from the sweep after the switch. | Rule 6: live side-by-side comparison; the old map stays until the sweep's map finds every session the old one finds. | INV-002 |
| "One data source" is false while the observer's questions panel calls Orca itself. | Rule 9: state it as an accepted exception, or add a questions block to the sweep; the owner decides. | INV-005 |
| A cap of 5 written as a default is read as settled, or counted as "no cap". | Proposed only; no generator writes a value until the owner records a ruling. | C-007; INV-011; section "The notice step: nine rows and the cap" |
| A wrong or unneeded rule in this list misleads the spec. | Each rule cites one finding, so a rule can be dropped without touching the others. | Plan, risk summary for Change 3 |
| The observer shows duplicate or unsafe text (the same question twice; unsanitized entry text). | Rules 10 and 12: one id or separate lists; entry text goes through `cli/observe/sanitize.py`. | INV-009, INV-012 |

## Open decisions for the owner

<!-- Source: Base (original, modified) - new section added per Change #10; questions drawn from the plan and the debate outcome (C-007, C-004, INV-005, INV-006) -->

1. **Notice cap: what value, and who rules?** The design records changes to the cap "only on Clay's recorded word" (orchestrator.md:688) and AD-B4 is "not ruled on; open" (orchestrator.md:1177).
   - A recorded 5: generators may write 5 as the default and a test pins it.
   - Another recorded value: the same, with that value.
   - No ruling, or a ruling of 0: no value is written; an absent key stays 0, which means no cap (`repos.py:262-269`).
2. **May the observer show an entry's text word for word, labelled as from the report?** (UNVERIFIED.)
   - Yes: the observer shows entry text after `cli/observe/sanitize.py` (rule 12), and the report's plain-English fields reach the screen.
   - No: the observer shows only the row number an entry already records, and stays navigation only.
3. **Is the observer's questions panel an accepted second Orca reader, or does the sweep gain a questions block?** (rule 9, INV-005.)
   - Accepted exception: the spec states it, and the claim "one data source" carries a written exception.
   - Questions block: the sweep JSON gains a block (an additive change with a golden-test edit, like rule 1) so the sweep is the only Orca reader.
4. **Where does the sweep JSON live?** (rule 3, INV-006.)
   - Saved as a file next to the Markdown report: one sweep serves the report and the observer within WC-16; the cost is one new file.
   - Each consumer runs its own sweep: no new file, but the spec must say how the observer's 15 s poll fits the one-per-5-minutes bound.

## What the merge gets right from each side

<!-- Source: Base (original, modified) - "What CLAY gets right" kept and extended with Variant 1 (opus:architect) "What OURS gets right", per Change #1 and Change #10 -->

From CLAY (the base): it is the only piece that already gives a person the plain-English "what is done, what is left, does it need me" per issue that issue 409 asks for, with a script gate that stops a bad report. It fills three gaps the sweep leaves open: the reason list for "needs a person", the cap on notices, and one living entry per issue. Its no-model `refresh` and its "carry, never close" rule are real, separable strengths (C-009, U-005).

From OURS: the sweep and observer follow the owner's decided chain and the read-only rule, run without a model, and have proof-based classes with "could not determine" instead of guesses. The dependency direction, session facts from the sweep into the report, keeps the most stable layer at the bottom (X-001). The owner's rules win on the sweep and observer surfaces (C-004), person-specific values leave the shipped config (C-005), and the owner's naming wins (C-010).

What the debate added beyond either paper: a join key that is not in the JSON yet (rule 1), and two HIGH risks of switching session reads (rules 5 and 6).
