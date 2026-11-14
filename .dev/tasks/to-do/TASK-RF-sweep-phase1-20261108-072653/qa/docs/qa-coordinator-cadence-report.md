# QA Report: Coordinator-cadence lens (T296)

**Date:** 2026-11-12
**Phase:** doc-qualitative, coordinator-cadence lens
**Reviewer stance:** adversarial; `fix_authorization: false`
**Gate folder:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/docs/`

## Scope

Does WC-16, the guide row R2 / R2 bullet, `sweep.md` line 20 and the contract's Liveness supervision "The sweep." paragraph (at most once every 5 minutes) tell a coordinator one consistent thing about when to run `/sc:sweep`; and is the R5 decision recorded in OQ-1 reflected where the text names `worktree ps`.

## Findings

No BLOCKING or MAJOR finding. Three MINOR notes.

### CAD-1 (MINOR): guide R2 bullet says "on every wake" and omits "or wait timeout"

- Evidence: `src/superclaude/core/HOW-WE-WORK.md:405` ("The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep.""), against `src/superclaude/core/WORKER-CONTRACT.md:277` (WC-16: "On every coordinator wake or wait timeout, at most once every 5 minutes") and `WORKER-CONTRACT.md:110` ("After every wake or timeout, at most once every 5 minutes").
- What is wrong: the owner-approved OQ-3 addendum fixed this exact gap in WC-16 (CON-F2: a quiet timeout could be read as not needing a sweep) but left DESIGN row R2 and so the guide bullet unchanged on purpose (addendum, "Scope of this approval"). A coordinator that reads only the guide could treat a quiet 5-minute timeout as "not a wake" and skip `/sc:sweep`.
- Why it is not blocking: the same bullet binds the run to "beside 'The sweep.'" and to "that same pass" of WC-16, and the sweep it sits beside runs on wake or timeout. The cap and the rule agree; only the trigger noun differs. The R2 text is pinned byte-for-byte to DESIGN row R2 (verified, C6), and a change needs the owner.
- Smallest fix (owner approval needed, DESIGN row R2 and `HOW-WE-WORK.md:405` and its plugin copy together): "on every wake or wait timeout".

### CAD-2 (MINOR): the cadence wording is not pinned by any test

- Evidence: `tests/skills/test_worker_contract.py:173-181` pins WC-16 only by "On every coordinator wake" (a substring, so the approved change did not need a pin edit) plus three other phrases; line 221 pins the existing sweep's "at most once every 5 minutes, the coordinator runs one sweep". No test in `tests/commands/test_sweep_command.py`, `tests/recommend/test_routing_refresh.py` or `tests/core/test_how_we_work_routing_table.py` matches "5 minutes", "at most once", "wait timeout" or "liveness" (grep, no match).
- What is wrong: the 5-minute cap and the "wake or wait timeout" trigger in WC-16, `sweep.md:20` and the R2 bullet can drift apart without a test failing.
- Smallest fix: add the two phrases "On every coordinator wake or wait timeout, at most once every 5 minutes" (WC-16) and "inside its liveness sweep pass, at most once every 5 minutes" (`sweep.md`) to the existing pins. Optional; nothing is wrong today.

### CAD-3 (MINOR): "reads its report before it acts" has no rule for a wake inside the 5-minute cap

- Evidence: `WORKER-CONTRACT.md:277`. A `worker_done` or `question` can wake the coordinator 2 minutes after the last pass. The cap skips the pass, but "before it acts" does not say the previous report may be used.
- What is wrong: a coordinator could either wait for the cap to lapse before acting, or run `/sc:sweep` again and break the cap. Neither is stated. The existing "The sweep." text (line 110) has the same silence, so this is not new to WC-16.
- Smallest fix: one clause, "using the last report when the cap has not lapsed". Owner approval is needed because WC-16's text is approved. Not required.

### R5 / OQ-1 reflection: no defect

- OQ-1 (`phase-outputs/plans/OQ-1-agent-wait-decision.md:19-23,42`) allows `worktree ps --agent-wait` (with and without `--json`) and says `WORKER-CONTRACT.md:110` is not edited. `git diff -U0` on the contract shows only the line 23 entry and the new WC-16 hunk; line 110 is untouched and still names the listing.
- WC-16 says `/sc:sweep` does not "run the `worktree ps --agent-wait` listing". This matches code: `src/superclaude/cli/sweep/probes.py:56-57` lists the two forms as allowed and "not called"; the only call is `worktree ps --json` (`probes.py:1253`); the waiting-on-a-person signal comes from `worker-show` `agentWait` (`probes.py:424`). So the text names the listing in two places (contract line 110 and WC-16), and both are true under the R5 allow decision. No guide, command, skill, changelog or user/developer guide text names `worktree ps` (grep).

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | WC-16 cadence ("at most once every 5 minutes") agrees with contract line 110 and the wait timeout (`--timeout-ms 300000`, line 101) | PASS |
| C2 | WC-16 trigger "wake or wait timeout" agrees with line 110 "wake or timeout" | PASS |
| C3 | `sweep.md:20` carries the 5-minute cap and names WC-16 as the source, and the cap attaches to the coordinator, not to a person typing it | PASS |
| C4 | WC-16 makes `/sc:sweep` additive ("does not replace", "not a second pass", no heartbeat update, no `--agent-wait` listing); contract line 110 still owns the heartbeat update and the listing | PASS |
| C5 | Guide R2 bullet states the same cap and the same "beside the sweep / same pass" relation as WC-16 | PASS |
| C6 | R2 bullet is byte-identical to DESIGN row R2 (`docs/designs/orchestrator-mode.md:716` against `HOW-WE-WORK.md:405`); the plugin copy matches (`cmp`); WC-16 text in DESIGN line 679 is identical to the contract line 277 | PASS |
| C7 | R2 bullet trigger noun matches WC-16 ("wake or wait timeout") | FAIL (MINOR, CAD-1; owner kept R2 unchanged) |
| C8 | R5 decision reflected where the text names `worktree ps` (contract line 110 unedited and true; WC-16 says `/sc:sweep` does not run it; `probes.py:56-57` allowed, not called) | PASS |
| C9 | No other primitive, guide or changelog line states a different cadence (CHANGELOG:13, `commands.md:116`, developer guide line 991, SKILL.md checked) | PASS |
| C10 | "Phase 1 adds this duty, not a scheduler" agrees with the skill ("schedule anything" is forbidden, SKILL.md line 64) and with "keeps that pass scheduled" (the wake loop is the schedule) | PASS |
| C11 | Cadence wording is protected by a test pin | FAIL (MINOR, CAD-2) |
| C12 | A wake inside the cap has a stated action ("before it acts") | FAIL (MINOR, CAD-3) |
| C13 | `uv run pytest` on `tests/skills/test_worker_contract.py`, `tests/commands/test_sweep_command.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`: 1184 passed | PASS |

## Self-Audit

- Files read from disk now: `WORKER-CONTRACT.md` lines 93-137 and 268-297; `sweep.md` lines 1-69; `HOW-WE-WORK.md` lines 398-408; `SKILL.md` lines 1-36 (plus grep of the whole file); `docs/designs/orchestrator-mode.md` lines 668-687 and line 716; `OQ-1-agent-wait-decision.md` lines 1-43; `OQ-3-addendum-wc16-wait-timeout-decision.md` lines 1-28; `probes.py` lines 35-85 and 1225-1285; `CHANGELOG.md` lines 5-24; `test_worker_contract.py` lines 168-227. Grep over the guides, the developer guide, `commands.md` and the three other test files.
- Not read in full (outside this lens): the style-exception revision files, `.gitignore`, phase validation files and DESIGN 7.6 and 9 apart from row R2. The earlier gate reports were not used as evidence.
- `sweep.md` is untracked (`git status` shows `??`), so `git diff` cannot show it; I judged it from the file on disk.
- No file other than this report was written. The `/tmp` scratch files I made were deleted. No Orca, ccsession or Claude command was run.

Verdict: PASS
Blocking count: 0
