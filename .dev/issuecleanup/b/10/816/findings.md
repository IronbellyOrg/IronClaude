# Round 2 findings: issue #816 (W8, alert after three bad cycles, FU-4)

Checked 2026-11-24 on branch `ironbelly/Realign` at `f2894fc44`. Sources: issue #816, round 1 findings (`/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/3/816/findings.md`), umbrella #717 and its closing review, the plan files under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`, and `src/superclaude/cli/issue_watch/`. Master check: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick` (`.dev/issuecleanup/b/10/analyze/analyze-report.md`, findings A2, A3, A4).

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): ALIGNED. FU-4 is a follow-up row of the merged watcher's runbook (`docs/designs/issue-watcher-setup.md:671`, `docs/designs/issue-watcher.md:863`) and section 12 (`:545-557`), not a Clay element.
- **D09, the poll stays read-only on GitHub; a held or skipped issue shows only in `issue-watch status` and the audit log** (`DECISIONS.md:379-406`; `debates/D09/VERDICT.md:70`): ALIGNED and supportive. It expects `status` or the audit log to be the place to see skips, so a reader of the audit log is in line.
- **NFR-04** (`spec/SPEC.md:217`, extend `status --json` with new keys) and **S12** (`spec/SPEC.md:496`, schema-pinned status; the loader rejects unknown keys): PARTLY ALIGNED. The plan wants one status-schema change; W8 adds a status key and an exit rule. #717's review calls S11/S12/S17 unverified as current build gates after PR #729, so the rule kept is: land the new key together with other status changes. Not a conflict.
- **NFR-02, one writer** (`SPEC.md:215`): ALIGNED; reading `audit.jsonl` is read-only.
- **Contract text W8 must amend** (not a decision): `status_report` is documented as reading "`dispatch.json` and the `DISABLED` mtime and nothing else" (`cycle.py:1416-1418`), and the runbook says `status` "reads only the local store" (`docs/designs/issue-watcher-setup.md:553`). Reading the audit log changes both statements and their tests. PARTLY ALIGNED until amended.
- **FR-44** (`SPEC.md:255`, the observer reads `status --json`): ALIGNED, W8's new key would be read by the observer; keep it typed scalars only (NFR-002, `VERDICT.md:49`: no GitHub text in the audit log or store).
- **D02 scheduler is cron** (`DECISIONS.md:175-203`): ALIGNED and a constraint: cron hides the cycle exit codes, so the codes must come from `status` and the audit log (the issue's own watch-out).
- **WORKER-CONTRACT.md**: the watcher is not a worker; WC-9 (outward actions) matters only if the sink were a GitHub or chat post, which the watcher must not make (D09). None apply to the reader itself.
- Searched `DECISIONS.md`, `SPEC.md`, `FOLLOW-UPS.md`, `debates/*/VERDICT.md` for `alert`, `FU-4`, `status`, `audit`; no decision picks an alert sink. In conflict: none.

## Complementary issues

- **#814** (W6, shadow-run check: every cycle exit 0 or a named reason): both need one reducer over `audit.jsonl` cycle lines. Interface: a shared function that yields, per cycle, its exit and reason; W6 uses it once as a script, W8 uses it in `status`.
- **#820** (W12, 7-day SLO review): `slo_numbers` (`cycle.py:1497`) also reads audit lines and has no caller; its "reader first (maybe a status field)" note asks for the same reader. Interface: same reader, W12 adds the four numbers.
- **#811** (W3, configurable poll interval): `HEALTH_AGE_S = 900` (`cycle.py:45`) equals three 5-minute cycles. If the interval changes, the stale rule breaks unless it scales; W8's "three cycles" rule must count cycles, not seconds.
- **#813** (W5, live firing tests): the restart test expects `status` not to exit 6, so a new exit code must not reuse 6 (`cli.py:39`), 1 (`cli.py:36-37`) or 75 (`cli.py:40`).
- **#777** (map of manual pieces) and **#774** (docs refresh): the alert sink is one manual piece to list; #774 edits the same runbook section 12.
- **#823** (W15): rewrites the runbook after the live test; section 12 text changes with W8.

## Closest overlap

**#814** (W6), "Shadow-run acceptance check: every cycle ends with exit 0 or a named reason". Shared: the same reducer over `audit.jsonl` cycle lines and the same exit-code table (exits 3 to 7). Estimated cover of W8's done-when: about 10 percent of the acceptance text (W6 proves cycles are classified; it does not make `status` exit non-zero or clear on a good cycle), but about a third of the build effort (the reader). Next two closest: **#820** (W12, same reader, about 10 percent) and **#811** (W3, the 900 s age rule depends on the interval, about 5 percent).

## Standalone or merge

Verdict: **stand alone**. Share the reader code, not the issue.

- Owner and trigger: W6 is a one-time acceptance check before switch-on, and #450's closure (2026-11-24) already replaced the old gates with automatic first-run checks. W8 is a permanent `status` feature plus an owner decision (the alert sink). W12 is a dated review. Three different moments.
- Acceptance test: W8's test is three scripted failing cycles make `status` exit non-zero and a good cycle clears it. W6's is a script that lists unexplained exits over a shadow run. W12's is a written review after 7 live days. Different tests.
- Files touched: W8 changes `cycle.py` (`status_report`), `cli.py` (`status_command`, exit code), tests that pin the "reads nothing else" contract, and runbook section 12. W6 is a script. W12 adds a caller for `slo_numbers`.
- Build phase: W8 can go first because its trigger (a chosen sink) is an owner decision; W6 may be dropped after #450 closed.
- Risk if merged: one 3-in-1 issue would block on the alert-sink decision and on a verified first-enable date at once; a done-when with three tests is hard to close honestly.
- Merging would be right only if the owner drops W6 (then W8 absorbs the reader) or builds W6, W8 and W12 as one PR by one builder; a single "audit-log reader" prerequisite issue is the cleaner way, not a merge.

## Closed issues and merged PRs checked

- **#450** (rollout, closed completed): substituted automatic first-run checks; its comment says the runbook's old and new enable steps conflict. Does not build W8; the runbook still says "the alert sink has not been chosen".
- **#331** and **PR #447** (poller, `status`, state, SLO ingredients): delivered `status_report` and `slo_numbers` but no reader of the audit log; contradicts nothing.
- **PR #485** (runbook, rollout checklist): wrote the FU-4 row and section 12; leaves alerting out.
- **PR #707** (merged zero-setup watcher): keeps `status` store-only. **PR #729** (R38): the owner baseline; W8 remains a tracked uncovered feature.
- **#751 and PR #759**: failed-first-run retry; not a bad-cycle alert. **PR #448, #591**: unrelated to alerting.
- **#655** (closed not planned): source design only. Nothing delivers or supersedes W8.

## Updated recommendation

Keep open with changes: (1) the owner chooses the alert sink in chat first; (2) build one audit-log reducer shared with #814 and #820; (3) the new exit code must differ from 1, 6 and 75; (4) land the new status key together with other status changes (#814, #820, #811) so the schema changes once; (5) the three-cycle rule counts cycles, not seconds (#811); (6) answer clayphi's open question on #717 about showing skipped issues and the 100-issue stop; (7) state that the existing 900 s stale rule (`cycle.py:45`, `cycle.py:1233-1234`) already makes `status` exit 1 about 15 minutes after three failing cycles, so W8's real additions are the cause class and the sink. Priority **P2**. Complexity **medium**, size **M**. Unchanged from round 1; the only addition is item (5) (the interval dependency was listed as a conflict in round 1 but not as a done-when change).

## Scan record

Lists read in full: open-issues.tsv 134 lines, closed-issues.tsv 157 lines, merged-prs.tsv 508 lines. Search terms: alert, audit, status, health, stale, exit, cycle, SLO, shadow, poll interval, runbook, W6, W12, W3. Opened in full or to the done-when lines (raw copies in `.dev/issuecleanup/b/10/raw/`): open #717 (with both comments), #722, #812, #814, #820, #811, #813 via #812's body, #822, #823, #818, #761, #777, #774, #753, #770 (15 distinct); closed #331, #450, #655, #665, #751 (5); merged PRs #447, #485, #548, #584, #591, #700, #707, #729 (8). UNVERIFIED: whether a cycle that writes an entry as failed or unknown (exit 7) skips step 14 (the line needs `_exit() == 0`, so it most likely does); live-host behaviour (not checked); no test or cycle was run.
