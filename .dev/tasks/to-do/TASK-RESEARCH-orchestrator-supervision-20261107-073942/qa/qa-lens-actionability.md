# QA Report — Report Lens: Actionability

**Topic:** Orchestrator mode Phase 1 (issue #339)
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Date:** 2026-11-07
**Phase:** report-lens-actionability
**Fix cycle:** N/A
**Fix authorization:** false

## Actionability QA Report

**Overall Verdict: FAIL** (CRITICAL 0, IMPORTANT 14, MINOR 10)

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | S8 1.4, 1.10; SC-3 | The probe allowlist includes `worktree ps --json`, but the same step says every argv is `orca-ide orchestration <verb>`. `orca worktree ps [--limit] [--agent-wait] [--json]` is a top-level verb (verified with Orca help); `orca-ide orchestration worktree` returns "Unknown command". A developer who follows 1.4 literally builds a probe that cannot run, or writes an SC-3 argv-prefix test that rejects the probe the report needs. (checklist a, b) | In 1.4, 1.10 and SC-3, list `orca-ide worktree ps --json` as a named exception to the `orchestration` prefix. Have the 1.10 test assert the exact argv tuples, not only the prefix. |
| 2 | IMPORTANT | S9 :1507 [CONTRADICTION]; S8 1.15, 1.16; SC-16 | The `allowed-tools` form for the skill is left open: colon form or space form. Step 1.16 has to pin this string in a test, so the test cannot be written until someone decides. A new developer cannot start 1.15 or 1.16 from S8 alone. The repo already has a precedent: `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md:7` uses the space form `Bash(uv run superclaude swarm *)`. (checklist a, d) | Resolve the marker in the report. State the exact line (for example `Bash(uv run superclaude sweep *)`, space form, following sc-swarm-wizard-protocol) in 1.15 and SC-16, and have 1.16 assert that literal. Keep the [CONTRADICTION] marker with its resolution recorded beside it. |
| 3 | MINOR | S7 step 6 (:1078 [CONTRADICTION]) | S7 gives the HOW-WE-WORK other-commands range as :314-337. The `<!-- other-commands:v1 -->` markers are at `src/superclaude/core/HOW-WE-WORK.md:318` and `:337` (verified), which matches S8 1.21. The step still works because the developer edits between the markers, but S7 and S8 disagree. | Change S7 step 6 to :318-337, or cite the markers instead of line numbers. Record the resolution next to the marker. |
| 4 | IMPORTANT | S7 steps 1, 4 vs S8 1.5, 1.15 | It is unclear what renders the Markdown report. S7 step 1 lists the modules without `report.py`, and S7 step 4 has the skill compose the report. S8 1.5 makes `report.py` the only write and the renderer. A developer cannot tell whether the skill writes anything, and that decides the skill's `allowed-tools` (Write or no Write) and the read-only claim. (checklist a) | State in S7 and S8 that `report.py` renders and writes the file and that the skill only runs the CLI and reads the result back. Add `report.py` to the S7 step 1 module list, and leave Write out of the skill's allowed-tools in 1.15. |
| 5 | IMPORTANT | S8 1.4; S9 row 63 (GQ-99) | Step 1.4 calls for a bound on probe calls (GQ-99) but gives no number, and does not say what happens when the bound is hit (stop, mark rows "could not determine", or exit nonzero). S9 row 63 still lists the bound as open. The step cannot be implemented or tested as written. (checklist b, c) | Give a number (for example a maximum of N `worker-read` calls per sweep). Define the behaviour at the bound: remaining rows get "could not determine (call bound reached)" and the summary line counts them. Add the case to the 1.10 tests and close S9 row 63. |
| 6 | IMPORTANT | S8 1.3 rule 2; S9 row 70 | Rule 2 depends on a turn having been "proved final", but the report never says which transcript record or Orca field proves that. S9 row 70 still lists it as open. `classify.py` is meant to be pure and table-tested, and that is impossible while the predicate has no definition. (checklist a, c) | Name the exact `worker-read` record type or field that proves a final turn. If none exists today, limit rule 2 to `terminalState == exited` and route everything else to "could not determine". |
| 7 | IMPORTANT | S3.1; S8 1.3 rule 3 | Rule 3 depends on `consumer_fenced` evidence, but the report names no Orca field, file or command that supplies it. The probe list in 1.4 has no call that returns it, so the developer cannot write a probe for it. (checklist a) | Name the field and the probe call (the `worker-list` / `worker-read` JSON key) that carries fencing. If no source exists, mark rule 3 as not buildable in Phase 1 and say so in SC-4. |
| 8 | IMPORTANT | S8 1.3 rule 4 | Rule 4 (frozen plan, Ruling halt, foreign ready Task) gives no detection algorithm. It does not say which ledger file the sweep reads, which `WORKER-CONTRACT.md` field defines "frozen" (:133 covers both the ledger and the contract), or how a Task's creator is told apart from the coordinator for "foreign" (:129). A developer would have to go back to the contract and choose a rule. (checklist a) | For each sub-case in 1.3, name the file path pattern, the field or literal it matches, and the Orca JSON key for the Task creator. Add one fixture per sub-case to 1.8. |
| 9 | IMPORTANT | S8 1.3 (rules 5-7, idle) | The class table has a gap: a person-started (non-dispatched) session that shows activity inside the 6 h window matches no rule and is not idle. "Activity" is also never defined as a field (PTY output time, transcript record time, or Orca `lastActivity`). Either gap stops a developer from writing the precedence function and its exhaustive table test. (checklist a, c) | Add the missing class or route it explicitly ("person session, active"). Define activity as one named Orca field and its source probe, and state that person-wait time is excluded (as S5 R4 already says). |
| 10 | IMPORTANT | S8 1.3 rule 6; safe-to-close dimension | Rule 6 and safe-to-close depend on facts the sweep cannot observe: whether the worker "read the contract" and whether "the result was already read" by the coordinator. Neither has a probe in 1.4. Without an observable proxy the sweep has no basis for marking a row safe to close, and SC tests cannot pin the behaviour. (checklist a, c) | Define an observable proxy for each (for example a contract-acknowledgement record in `worker-read`, or the coordinator's read cursor), or state that Phase 1 always prints "safe to close: could not determine" for these cases. |
| 11 | MINOR | S8 1.8 | The fixture for a non-null `agentWait` is built from a guessed shape (GQ-36 is open). The fixture may not match real Orca output, but 1.8 can still be written and later corrected. | Mark the fixture as provisional in 1.8 and add a 1.29 step that captures one real `agentWait` payload and replaces the guess. |
| 12 | IMPORTANT | S8 1.6 | The CLI contract is incomplete. The JSON output schema (keys and types) is not given. The default for `--run` is ambiguous (current run or all runs). The purpose of `--root` is unclear. The format of `--window` is undefined (hours as an integer, or a `6h` string). Nothing enforces that the report path is under `.dev/`. Step 1.15 gives no default report directory. Each of these would be invented by the implementer, and the 1.10 / 1.12 tests depend on all of them. (checklist b, c, d) | Add a small schema block to 1.6 (top-level keys, the row fields, the summary fields). State each option's default and type. Say that `--out` outside `.dev/` is rejected with a nonzero exit, and give the default directory in 1.6 and 1.15. |
| 13 | IMPORTANT | S8 1.17, 1.19 (WC-14) | The WC-14 steps leave the content to the implementer. G3 has no cadence (how often the coordinator sweeps). G6 is left waiting on the owner. The exact phrases to add to `RULE_PHRASES` in `tests/skills/test_worker_contract.py` for WC-14 are not given. The text of the new never-as-worker phrase is not given either: the phrase at :86-92 and `NEVER_AS_WORKER` at :245-254 (8 entries) both have to change, and a mismatch fails the test. (checklist b, d) | Give the verbatim WC-14 clause text (G1-G7) or the exact phrases the test pins. Give a number for G3, or state "on every coordinator wake". Mark G6 as an owner decision that blocks only 1.17's G6 sentence. Give the new never-as-worker sentence and the updated 9-entry `NEVER_AS_WORKER` set. |
| 14 | IMPORTANT | S8 dependencies; S1; S4 GQ-62 | S1 and the GQ-62 row say Phase 1 is sequenced after PR #422, but the S8 dependency list and step ordering do not include that prerequisite. A developer starting from S8 alone may branch before #422 lands and then conflict on the same files. (checklist d) | Add "PR #422 merged (or rebased onto)" as step 0 or as an S8 prerequisite, name the files it touches that overlap with Phase 1, and say what to do if it has not merged. |
| 15 | IMPORTANT | S8 1.4 acceptance; 1.29 | The live checks need a running Orca and give no pass threshold, no place to record the result, and no expected output. "Run against live Orca and check it looks right" is not a pass/fail criterion. (checklist c) | State the command, the expected classes for a known run (or "no row 'could not determine' caused by a probe error"), the time limit, and the file under the task package `artifacts/` where the output is saved. |
| 16 | IMPORTANT | S8 Integration Checklist | The integration checklist has no live end-to-end run (CLI, skill, command, real Orca, report file) and no check that the WC-14 clause content matches G1-G7. Every listed item can pass while the feature does not work end to end. (checklist c, d) | Add one end-to-end item: run `/sc:sweep` in a session with a known run, confirm the report file exists under `.dev/` with the expected sections, and confirm the Orca state is unchanged before and after. Add one item that checks WC-14 against G1-G7. |
| 17 | MINOR | SC-2; SC-11 vs S8 1.21 | SC-2 and SC-11 have conditions attached. SC-11 holds "unless GQ-24" decides otherwise, while 1.21 treats the routing entry as already decided. The criteria still read as pass/fail once the condition is settled. | Drop the "unless" from SC-11 to match 1.21, or make 1.21 conditional too. Keep a single source for the decision. |
| 18 | MINOR | SC-9; SC-1 | SC-9 is worded loosely (it has no observable assertion), and SC-1 says "every entry point" without listing them. | Rewrite SC-9 as an assertion on the output, and list SC-1's entry points (CLI, skill, command). |
| 19 | MINOR | S8 1.11 | 1.11 says to allow the report path in the write guard, but does not say how (which pattern, which file, and the test). The step can be done once the guard file is opened. | Name the guard file and the exact path pattern to add. |
| 20 | MINOR | S8 1.4 | The `worker-read` argv in 1.4 leaves out the required `--dispatch <dispatch_id>`, and `--limit` / `--json` (verified with `worker-read` help). It is easy to fix during implementation, but the allowlist pinned by SC-2 would be wrong. | Write the full argv: `orca-ide orchestration worker-read --dispatch <id> --limit <n> --json`. |
| 21 | MINOR | S8 (missing step) | Several items are marked "read before implementation" (GQ-14 `tests/commands/test_help_command.py`, GQ-100 `APPROVED.md`, the ccsession-tag README), but no S8 step tells the developer to read them or says what to look for. | Add a step 1.0 "Read before starting" that lists these files and the question each answers. |
| 22 | MINOR | S8 1.15; GQ-63 | GQ-63 (the DONE/NEXT exemption) changes the 1.15 output, and the report gives no default while it is open. | State a default (for example "no exemption in Phase 1") so 1.15 can be written now. |
| 23 | MINOR | S8 report layout (Retained problems line) | The retained-problems line carries "stale" and "policy frozen" counts from the #409 layout, but the report does not define either term for sweep rows. | Define "stale" and "policy frozen" for sweep rows, or leave them out of the Phase 1 line. |
| 24 | MINOR | S8 (#409 layout pinned to 495eb96d) | The layout is pinned to commit 495eb96d (verified reachable; the branch `docs/409-orca-dashboard-designs` exists locally and on origin), but the report does not say how to read the files at that commit. | Add `git show 495eb96d:<path>` for each layout file cited. |

**Judgement on the NB-4 exception record (actionability lens):** actionable. The exception is concrete: the allowlist is written out in 1.4 and pinned by SC-2, and the developer is told exactly what is permitted. It has no finding of its own; the defects in the allowlist's argv strings are recorded in rows 1 and 20.

**Judgement on the two [CONTRADICTION] markers:** :1507 blocks steps 1.15 and 1.16 (row 2, IMPORTANT). :1078 does not block, because S8 1.21 holds the correct range (row 3, MINOR). Neither marker should be removed. Both should have their resolution recorded beside them.

### Summary

| Checklist item | Result | Rows |
|---|---|---|
| (a) S7 recommendations executable without more research | FAIL | 1, 2, 4, 6, 7, 8, 9, 10 |
| (b) S8 steps state action, target files, expected outcome | FAIL | 1, 5, 12, 13 |
| (c) Success criteria testable pass/fail | FAIL | 5, 6, 9, 10, 12, 15, 16 |
| (d) A developer outside the investigation could start from S8 alone | FAIL | 2, 12, 13, 14, 16 |

- Total findings: 24
- CRITICAL: 0
- IMPORTANT: 14 (rows 1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16)
- MINOR: 10 (rows 3, 11, 17, 18, 19, 20, 21, 22, 23, 24)
- Issues fixed in place: 0 (fix authorization false)

What works: the module split in S7 and S8 (models / classify / probes / report / commands), the registration point in `src/superclaude/cli/main.py` (reflect at :559-561, before the `__main__` guard at :564-565), and the HOW-WE-WORK marker edit in 1.21 can all be done as written.

**Verdict: FAIL**

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(Each checklist item was checked against the S7/S8/S9 text and, where it cited code, against source. Live Orca behaviour beyond `--help` output was not exercised because state-changing commands were forbidden.)

**Tool engagement:** Read: 14 | Grep: 10 | Glob: 0 | Bash: 3 | Write: 1 | Edit: 3. No web research was performed (none needed; Tavily not used).

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for structural re-check):**
- None. No `## Inherited Structural Verdict` was provided, so this was a standalone review.

**(b) Independent semantic checks (at least one required, INV-019):**
- Orca verb placement: `orca worktree ps` help shows a top-level verb, and `orca-ide orchestration worktree` returns "Unknown command". This is the basis for row 1.
- `worker-read` help shows that `--dispatch` is required. This is the basis for row 20.
- `src/superclaude/cli/main.py:559-565`: the registration point in 1.7 is correct.
- `tests/cli/test_cli_registration.py:31-49, :102`: the subset check means 1.13 is correctly optional.
- `src/superclaude/core/HOW-WE-WORK.md:318, :337` markers: these resolve the :1078 [CONTRADICTION] (row 3).
- `tests/skills/test_worker_contract.py:86-92, :245-254`: the never-as-worker phrase and the 8-entry set the new text must update (row 13).
- `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md:7`: the space-form `allowed-tools` precedent for the :1507 marker (row 2).
- `git cat-file` on 495eb96d and the branch listing: the commit is reachable (row 24).
- `tests/recommend/test_routing_refresh.py:33` and `tests/commands/test_help_command.py`: the routing additions set and the absence of a static help table, both consistent with 1.21 and 1.22.

## QA Complete
