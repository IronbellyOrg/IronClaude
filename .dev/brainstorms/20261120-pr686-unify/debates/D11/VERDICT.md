# Verdict D11: Observability stack: work report, sweep, observer, TUI dashboard

## Question

Clay's PR 684 moved the `agent-work-report` skill and a living work report into IronClaude. OURS built `/sc:sweep` (PR 539, read-only report, WC-16), `superclaude observe` (the observer behind the issue 409 TUI dashboard design) and the dashboard design package (PR 409). The design 681 never mentions sweep, observe or 409. How should the three be unified (one data source, one report, one dashboard) and which of Clay's report features (living report, nine-row "what reaches Clay" table, cap of 5 notices a day) should be adopted?

## Winner

HYBRID. The sweep stays the one source of session facts (OURS), and the work report stays as the plain-English work-item layer (CLAY), with the owner's read-only rules governing the sweep and the observer.

Scoring of the debate (18 diff points): OURS wins 5, CLAY wins 2, HYBRID 7, and the 4 shared assumptions were all qualified or accepted by both sides. Note that the base-selection score (CLAY paper 0.8667, OURS paper 0.7723) rates the quality of the two papers as documents; it does not decide the question.

## Winning recommendation

The merged text is `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/adversarial/merged-d11-observability-recommendation.md`. The spec must say:

**One data source.** The sweep JSON (schema version 1, PR 539 "read-only report of Orca sessions") is the only source of session state. The report and the observer both read it. The report no longer decides session status itself.
- The sweep JSON row gains `session_id` and `worktree_path`, allowed to be empty, with a reviewed edit to the golden test that pins the v1 keys (NFR-009, `docs/designs/orchestrator-mode.md:605`). Today a row has neither (`src/superclaude/cli/sweep/report.py:642-661`), and `row_id` holds a session id only for transcript rows (`classify.py:933`).
- A test: a row built without a join passes the contract with both fields empty; a fixture with an Orca row and a transcript row for one session gives one row.
- The JSON is saved as a file beside the Markdown report, or the spec says each reader runs its own sweep (today it prints to standard output only, `commands.py:277-278`; the observer polls every 15 s, WC-16 allows one sweep per 5 minutes). The owner decides which.
- One honest exception is written down: the observer's questions panel calls Orca itself (`observe/adapter.py:32`), so "one data source" is false until the owner accepts that exception or the sweep gains a questions block.

**One report.** The work report is the one plain-English report: per issue, what is done, what is left, whether it needs the person, links. Session facts come from the sweep; work items come from GitHub and ClickUp (`collect.py`, `clickup.py`). `check.py` and `run.py gate` stay as the delivery gate.
- Two HIGH rules (found by the fault-finder): (1) the report reads transcripts for the session ids in the sweep rows PLUS every not-done session of the previous report, even when its worktree is gone; (2) the report's own terminal-to-session map is removed only after one live side-by-side run shows the sweep finds every session the old map finds. A fixture test alone does not satisfy rule 2.
- The report passes `--window` equal to the time since the previous report; "Orca unavailable" or "sweep failed" writes `read: false` and is never read as "sessions ended".
- The report keeps reading what each session did from its saved transcript position (the sweep reads only a 256 KiB tail, `probes.py:865-867`).

**One dashboard.** The observer is the one screen. It reads the sweep JSON for sessions and the report's entry files for work items, shows the sweep class word for word, and carries no Options, no Recommendation and no write. Entry text passes `observe/sanitize.py`. An empty folder, zero rows and "could not read" show as three different states.

**Clay's features.**

| Feature | Verdict |
|---|---|
| Living report (one entry file per held issue, refreshed with no model call) | Adopt with change: per-user configurable state path; entry files store only `session_id` and the class is read live |
| Nine-row "what reaches Clay" table | Adopt with change: "the person" in place of Clay; lives in the notice step only; sweep and observer never pick a row; keep the planned "exactly nine rows" test |
| Cap of 5 notices a day | Adopt as a PROPOSAL, not settled: notices only, entries never dropped; no generator writes a value until the owner records a ruling (today the parser returns 0, meaning no cap, `pr-a issue_watch/repos.py:262-269`) |
| Silent-loss rules and `check.py` gate | Adopt as is, in the report layer, so the sweep stays stateless |
| Plain-English item template | Adopt with change: generic wording |

## Strongest points

OURS:
1. The sweep is a script with no model, reads Orca only through a fixed list of commands (`src/superclaude/cli/sweep/probes.py:49-56`), classifies into eight classes by written rules including "could not determine", and runs at most every 5 minutes (WC-16, `src/superclaude/core/WORKER-CONTRACT.md:287`). It belongs at the bottom.
2. The sweep "Will Not: recommend anything" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:61`) and the observer is navigation only (issue 409 item 2), while the report sends a ClickUp DM, commits its state folder and carries Options and a Recommendation (report `SKILL.md` Steps 13 and 14; `templates/needs-you-template.md`). The owner's rule must win on the sweep and observer surfaces.
3. The table and the cap are spec text only: no `escalate` verb, no `orchestrator` command group and no `asks.json` exist in master, pr-a or pr-p; AD-B4 calls the cap "not ruled on; open" (`docs/designs/orchestrator.md:1177`); the report is tied to one person and not zero-setup (`config.json` `"person": "clayphi"`, `common.py:35-50`).

CLAY:
1. The report is the only piece that gives the person, per issue, what is done, what is left, whether it needs them and a link, which is Clay's own ask on issue 409 (comment of 2026-11-11). The sweep has no GitHub call and no summary text (issue 409 alignment item 3; `probes.py:49-56`), and the Decision Desk is "NOT BUILT" (alignment spec 0.3).
2. A script gate and a no-silent-loss rule: a failed read carries items and never closes them, unread sources are listed under "Not checked", and delivery waits for `check.py` (report `SKILL.md:21-24`). The sweep has no such check (searched; OURS conceded).
3. It reads what a session did since the last report from a saved transcript position, up to 30 MB on the first run (`sessions.py:14-17`), where the sweep reads a 256 KiB tail (`probes.py:865-867`); the living page rebuilds with no model call (`SKILL.md:16`); and the nine rows give the sweep's bare "waiting on a person" lists a reason (`report.py:682-685`).

## Clay strengths to adopt

- **Work-item layer and plain-English item template.** What: GitHub, ClickUp and per-issue text. Why: fills a gap the sweep lacks and issue 409 asks for (alignment item 3). Merge: keep `collect.py`, `clickup.py` and the template; generic wording; session facts from the sweep.
- **Silent-loss rules and `check.py` / `run.py gate`.** Why: a real safety property, absent in sweep and observer. Merge: adopt as is, kept in the report so the sweep stays stateless and deterministic.
- **Living report with no-model refresh.** Why: no double reporting (`exclude.py`), no token cost. Merge: configurable per-user state path, entry files store only `session_id` (no stale status copy), naming follows the owner's decisions.
- **Transcript-since-last-report reader.** Why: clear capability the sweep lacks. Merge: keep it, keyed on the sweep's session ids plus the previous report's not-done sessions.
- **Nine-row table.** Why: the sweep has only "waiting a or b", no reason list. Merge: notice step only, "the person" wording, the sweep never chooses a row.
- **Cap of 5 notices.** Why: fits the owner's rule of showing outstanding decisions only. Merge: proposal only; the owner must rule; default stays 0 until then.

## Our strengths that must be kept

- The sweep as the single, stateless, zero-token, read-only source of session state, with its eight proof-based classes and "could not determine".
- "Recommend nothing" on the sweep and navigation only on the observer; Options, DM and commit only in the report or the orchestrator session.
- The owner's chain watcher, then orchestrator, then dashboard (PRs 587 to 589 alignment decisions).
- The owner's naming (coordinator) and layout (`.dev/coordinators/`); person-specific values out of the shipped config.
- The owner's rule: automated checks show outstanding user decisions only, no heartbeat chatter.
- The `UNVERIFIED` discipline: nothing unproven decides an outcome (for example, which session map covers more sessions).

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Write the contract note covering three readers (sweep, observer, report): names `session_id` as the join key, one owner and one amendment rule | DOC | `docs/designs/observe-sweep-contract.md` (not written since 2026-11-13) | First |
| Add `session_id` and `worktree_path` (empty allowed) to the sweep JSON v1 row, with the reviewed golden-test edit | LOCAL CHANGE | `src/superclaude/cli/sweep/report.py` (`to_json`), the sweep contract test | After the note |
| Owner rulings: cap value and who rules; may the observer show entry text; questions panel as exception or sweep questions block; where the sweep JSON lives | DECISION | the four open decisions in the merged recommendation | Before the matching code |
| Save the sweep JSON beside the report (if chosen) | LOCAL CHANGE | `src/superclaude/cli/sweep/commands.py` | After decision 4 |
| Live side-by-side run of the report's session map and the sweep's `orca-tabs` map | LOCAL CHANGE | `skills/agent-work-report/scripts/sessions.py` and `cli/sweep/probes.py:870-871` | Before the switch below |
| Switch the report's session reads to sweep rows plus previous not-done sessions; `read: false` on Orca down; pass `--window` | LOCAL CHANGE | `skills/agent-work-report/scripts/sessions.py` | After the field and the side-by-side run |
| Keep PR 684 (move of the report skill, merged); no revert | PR KEEP | PR 684 | Now |
| Follow-up PR: remove person-specific config, make the state path configurable, adopt the owner's naming and layout | PR KEEP-ADAPT | report skill (`config.json`, `common.py`, `SKILL.md`) | After D08 (naming) |
| Keep the cap key default at 0 and write no 5 until the owner rules | PR KEEP-ADAPT | PR 686 `issue_watch/repos.py` (`reach_daily_max`) | Until decision 1 |
| Add a short "related work" statement: the design says how the living report relates to sweep, observe and issue 409 | DOC | `docs/designs/orchestrator.md` section 6.3 | With D14 |
| Record that the report answers issue 409 alignment items 3 and 7 (report owns GitHub reads and text; the chat report is the interim surface) | DOC | issue 409 body (a recommendation; nothing posted here) | After the owner agrees |

## Implications

- **Watcher.** None directly. The poll still does not read sweep or observer files.
- **Coordinator or orchestrator.** WC-16 keeps running `/sc:sweep` on each wake; the report must not add a second Orca read for state. The orchestrator's entry files become the data the dashboard reads, so their format needs one owner and a fixed schema; entry creation at claim depends on D01 to D08.
- **Dashboard.** Clay's asks (summary, done, left, needs me, links) map to the report's fields; the observer's Decision Desk (not built; issue 606 visual parity work continues) reads entry files instead of building a second channel. Two question channels remain (observer questions and report "Needs you") until decision 3 and one shared question id.
- **Claim pipeline.** None, except that the report's "orchestrated" exclusion depends on entry files existing.
- **What breaks.** If the report's old session map is removed before the side-by-side run, sessions the old map finds could vanish silently; if the report reads only sweep ids, sessions of removed worktrees are dropped (HIGH findings). A cap default written as 5 would pass as settled.
- **What the owner must know.** Ruling 39 (the cap) is Clay's ruling, not the owner's; "one data source" is not literally true while the observer's question panel calls Orca; `docs/designs/observe-sweep-contract.md` has been unwritten since 2026-11-13 and every join depends on it.

## Confidence

72%. It would drop if a live comparison showed the sweep's session map covers fewer sessions than the report's, if the owner wants the report replaced entirely by the dashboard, or if adding fields to JSON v1 is refused. It would rise with a live run showing full coverage and an owner ruling on the cap.

## Unverified

- Which terminal-to-session map covers more sessions (sweep `orca-tabs` or the report's Orca hook file).
- Whether a transcript file name always equals its session id.
- Whether the observer has any check comparing one run with the previous run (the sweep was searched and has none).
- Whether `observe/sanitize.py` handles arbitrary entry-file text.
- Whether the observer may show entry text word for word (owner decision).
- Whether ruling 39 was made by Clay (the design implies it; `RULINGS.md` was not read).
- Whether Clay uses the daily report and whether its Orca waker automations were re-pointed after PR 684 (the PR body lists this as the owner's next step; not checked).
- The IronFlow coordinator spec was not read. The tech reference `techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md` did not exist, so code was read directly. The fault-finder reviewed master only, not pr-a or pr-p.

## Debate artifacts

Folder: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/`
- Position papers: `position-OURS.md`, `position-CLAY.md`
- Merged recommendation: `adversarial/merged-d11-observability-recommendation.md`
- Worker contract: `adversarial/return-contract.yaml`
- In `adversarial/adversarial/`: `diff-analysis.md`, `debate-transcript.md`, `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round2-rebuttal-V1.md`, `round2-rebuttal-V2.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`, `variant-1-original.md`, `variant-2-original.md`
