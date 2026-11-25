# QA Report: Task / Research Alignment (task-integrity, LENS task-research-alignment)

**Task file:** TASK-TECHREF-issue-pipeline-20261120-040158.md (2,365 lines)
**Inputs checked:** BUILD-REQUEST.md, research-notes.md, scope/scope-1..6
**Source snapshot:** /home/coder/.cache/ic-snap-20261120/master (read-only)
**Date:** 2026-11-20
**Status:** Complete (0 Blocking, 8 Medium, 14 Notes)

---

## Method

Read in full: BUILD-REQUEST.md, research-notes.md, scope-1..scope-6, and the task file (Phases 1-7 and the Task Log; the repeated safety/protocol blocks were read once and diffed by grep). Spot-checked against the read-only snapshot: templates folder, tests/hooks listing, tests/skills|unit|cli|core listings, WORKER-CONTRACT.md:57, cycle.py:35/44/58-72/216, orca_worktree.py:822, launch-level-guard.sh:405-412, launch.py:95-116, line counts of all hook and issue_watch modules, agent model pins, setup doc line 288, SUPERVISED-ORCHESTRATION reference lines 268/276, agent-work-report common.py.

## Checklist 1+2: findings per research input, and the task item that acts on each

### Required content (a)-(g) of BUILD-REQUEST (checklist item 2, "encoded as checks")

| Required content | Producer item | Assembly check | QA check | Result |
|---|---|---|---|---|
| (a) live-vs-off ledger, 8 pieces + status words | Step 5.1 (2.3 ledger, 8 rows + extra rows) | Step 6.1 rule D(a), rule 5 (ledger agrees with Section 5 and 14.2) | Gate 2 5.7/5.8, template-conformance check (8) at task line 1782, domain-accuracy lens | ENCODED |
| (b) writes-to-GitHub table per piece | Step 5.2 (4.5), Step 5.4 (5.2 writes table), 5.5 (8.1) | rule D(b) | same | ENCODED (content gap, see M5) |
| (c) trigger table | Step 5.2 (4.4) | rule D(c) | same | ENCODED (input gap, see M3) |
| (d) test-pin matrix, one row per test file | Step 5.5 Appendix A (43 files + fixtures dir = 44 rows) | rule D(d) | Gate 2 partition 2 check (k) row-count equals research-notes list | ENCODED; my count of research-notes tests: 20 issue_watch + 1 fixtures + 9 hooks + 7 skills + 1 commands + 2 cli + 3 unit + 1 core = 44, matches |
| (e) doc-vs-code contradiction table | Step 5.6 (14.1) incl. the eight BUILD-REQUEST warnings | rule D(e), rule 5 | check (l) | ENCODED |
| (f) Appendix "Removed on 2026-11-20" | Step 5.6 B.1-B.9 | rule D(f) | fidelity gate 4 | ENCODED |
| (g) exactly one PR 686 sentence | rules D (synth-01), "do NOT mention" in synth-02..06 | assembler rule C | count checks in Gate 2, Gate 3 (task line 1782), Step 7.1(4) | ENCODED. Appendix B is allowed to name PR 682, not 686: consistent |

### Per scope file / research-notes section

| Source | Key finding | Task item that acts on it | Status |
|---|---|---|---|
| research-notes EXISTING_FILES watcher table (8 modules, line counts) | module roles, MAX_LAUNCHES_PER_CYCLE dead | Agents 01-03, Step 5.3 required content (2),(8) | OK |
| scope-1 sec 2 triggers (no scheduler artefact) | only a person/external scheduler runs `once` | Agent 03 deliverable (d) plus grep for scheduler artefacts; Step 5.3 (1) | OK |
| scope-1 sec 2.2 verb table, exit 0/1/2/3/4/5/6/7/75, `status` skips platform check | verbs and codes | Agent 03 topic (1); Step 5.5 10.1 | OK; platform-check asymmetry not named (Note N7) |
| scope-1 sec 3 doc-vs-code (skew 300 vs 60, PR numbers [UNVERIFIED]) | contradictions | Agents 01/03 hints; 14.1; 14.3 | OK |
| scope-2 G1-G7 argv, 35 calls + 3 reserved (+2 shared = 37) | read-only gh calls | Agent 02 topic (1); synth-03 (4); synth-05 8.1 | OK |
| scope-2 `rate_limit_wait` works only for G1 (headers via `--include`) | nuance | Agent 02 mentions "rate-limit handling and clamp" only | Note N8 |
| scope-2 audit: 59 reasons, rotation 5 MiB x 4, "never" title/body claim is narrower than code guarantee (host/login accept any printable token) | nuance | Agent 01 audit schema | Note N8 (not forced) |
| scope-3 launch argv 12 elements, no worktree created | launch | Agent 02 (2); synth-03 (5) | OK |
| scope-3 record: 17 fields, 6 states, T-1..T-13, crash C1-C5, modes | store | Agent 02 (3) | OK |
| scope-3 sec 2.4 "who reads dispatch.json" = only record.py/cycle.py; hooks read a DIFFERENT store; third consumer `agent-work-report` reads `~/.config/superclaude/issue-watch.json` | cross-store findings | Agent 02 (5) greps `dispatch.json`; Section 6 asks "who reads dispatch.json" | dispatch.json OK; third config reader DROPPED (M6) |
| scope-3 sec 2.4 inference: watcher's `--pipeline none` session is not a governed launch-level session | coverage fact | no item | DROPPED (M7) |
| scope-3 marker `<!-- sc:issue:claim -->` closes the loop (T-10/11/12, 300 s window) | claim to watcher hand-off | zero occurrences of the marker text in the task file; only `test_marker_contract.py` is assigned (agent 01) | DROPPED as a cross-piece contract (M4) |
| scope-4 waves 0-8, writes (assign, 2 comments, ClickUp PUT), STOP/warning codes | claim flow | Agent 04 topics (1)-(3); synth-04 5.2 (2)-(4) | OK |
| scope-4 default-level rule is prose-only (refs/claim.md:81) | no code | Agent 04 (4); synth-04 5.2 (5) | OK |
| scope-4 IR7_REFUSE=False (:822), IR-3 pipeline.json not built, `pending` has no caller | unwired | Agent 04 (5); ledger rows; 14.2 | OK (IR7 verified in snapshot at orca_worktree.py:822) |
| scope-4 `--submit` agent-side commit/push/`/sc:pr-submit --monitor 3` | GitHub writes by the launched agent | Agent 04 reads launch-prompt.md and lists `full --submit`; no item asks for the push/PR command as a GitHub write | M5 |
| scope-4 worker pins t1 tier1b, t2 tier2, t3 tier2b; design says tier3 | contradiction | Agent 04 hint; 5.2 (7) | OK (pins verified: model lines at agents/issue-worker-t*.md:6) |
| scope-4 related tests: test_clickup_claim.py, test_model_alias_policy.py | extra pinning tests | not in any agent or Appendix A | M8 |
| scope-5 L1 matrix W/WA/F/FS, classifiers, LL-* words, fail-open/closed, exit 0/2 | guard | Agent 05 (1); 5.3 (3)-(5) | OK |
| scope-5 G2 rule 2 allow-list, no `--to` | rule | Agent 05 (1); 5.3 (6) | OK |
| scope-5 job identity, `identify`, L2 pre-push, hooks.json, install skip-if-exists unless force | stack | Agent 05 (2)-(4); 5.3 (7)-(9) | OK |
| scope-5 ccsession carries NO level; claim detects shim (SHIM_MARKERS / SHIM_TITLE) | contradiction of premise | Agent 04 hint, agent 05 (5); 5.3 (10) | OK |
| scope-5 IMPL list code `implement|task|cleanup` vs design 6 skills | contradiction | Agent 05 hint; 14.1 | OK (verified launch-level-guard.sh:409) |
| scope-5 `degraded` word: guard = level W, identity hook blocks every Bash call (pinned test_launch_level_guard_with_identity.py:187) | interaction edge | no explicit clause | Note N5 |
| scope-5 G1/G2/route built-vs-retired ledger | ledger | Agent 05 (6); 5.3 (11) | OK |
| scope-5 observation run, 10 payloads in temp HOME | observation | Agent 05 (7), sandbox moved INSIDE task folder (research/05-guard-run-sandbox/); rationale recorded in Builder Notes | OK; consistent with write rules |
| scope-6 current contract: no WC-17, no "Issue pipeline duties"; hits l.23/57/66/241-245 | coordinator text | Agent 06 Part A; 5.4 | OK |
| scope-6 removed package: 10 files, 10 verbs, 116 tests, WC-17, G2 rule 1 TAMPER case, test edits | appendix | Agent 06 Part B; B.1-B.9 | OK |
| scope-6 commit also edited main.py (-4 registration), docs/user-guide/cli-groups.md, CHANGELOG.md, SUPERVISED ref l.268, plugin copy of the guard | commit-level scope | Agent 06 Part B list omits them | Note N9 |
| research-notes "Built vs not built" list | ledger content | Step 5.1 extra rows | OK |

## Checklist 2 (continued): research assignments 01-06, test-file coverage

Every test file in research-notes EXISTING_FILES maps to exactly one agent:

| Agent | Test files assigned in the task | Matches research-notes row? |
|---|---|---|
| 01 | test_cycle, test_predicates, test_audit, test_marker_contract, conftest (5 named) | yes, but the item text and header say "six test files" (Note N1) |
| 02 | test_github, test_launch, test_record, test_concurrency, test_crash_injection, test_find_orca_parity, test_origin_parity, test_runner, `fixtures/_assumed_shape/` (8 + dir) | yes |
| 03 | test_cli, test_cli_e2e, test_slo_helper, test_no_shell, test_no_text, test_security_invariants, test_module_boundaries (7) | yes |
| 04 | test_issue_protocol, test_issue_orca_worktree, test_issue_repo_resolution, test_issue_worker_agents, test_issue_t1_fallback, test_issue_l2_install, test_issue_command, test_issue_body_templates (8) | yes |
| 05 | guard + four companions (by Glob), test_launch_job_identity, pre_push, pre_push_records, observations, test_install_hooks, test_install_ccsession, test_ccsession_tag, test_ccsession_tiers, test_orca_session_launch_guidance | yes (companion names left to Glob, see below) |
| 06 | test_worker_contract (current) + removed tests | yes |

Count check: 20 + 9 + 7 + 1 + 2 + 3 + 1 = 43 test files plus the fixtures directory = 44 Appendix A rows. Consistent with Gate 2 check (k).

### The four tests/hooks companion files (the builder could not confirm the names)

Checked with `ls /home/coder/.cache/ic-snap-20261120/master/tests/hooks/`. The research-notes shorthand `_l2_tokens.py`, `_registration.py`, `_with_identity.py`, `_worker.py` are suffixes of `test_launch_level_guard`. The real files, all present, none wrong:

- tests/hooks/test_launch_level_guard_l2_tokens.py (160 lines per scope-5)
- tests/hooks/test_launch_level_guard_registration.py (127)
- tests/hooks/test_launch_level_guard_with_identity.py (212)
- tests/hooks/test_launch_level_guard_worker.py (300)

Also present and named correctly in the task: test_launch_level_guard.py, test_launch_job_identity.py, test_launch_level_pre_push.py, test_launch_level_pre_push_records.py, test_launch_level_observations.py. No file in tests/hooks starts with an underscore (only `__init__.py`). So the phrasing "Glob on `test_launch*` and `_*` patterns" (Step 2.5, task line 577) and "the underscore-named launch-level companion files" (Gate 4 prompt, task line 2136) is wrong, but harmless: `test_launch*` already matches all nine launch tests. Recommend replacing both phrases with the four exact names above (Note N2).

tests/hooks also holds test_require_orca_worktree_agent.py and test_require_orca_worktree_agent_governed.py (pin the worktree gate hook that hooks.json registers). Not in research-notes, not assigned (Note N10).

## Checklist 3: facts in the task that are not in the research inputs (fabrication scan)

Verified against research inputs and the snapshot, no discrepancy: 59-entry REASON_TABLE; 35 calls with 3 reserved; 12-element launch argv (launch.py:95-116 read); 17 fields / 6 states / T-1..T-13; 1906-line orca_worktree.py; 808/582/208-line guard scripts; hooks.json 192; install_hooks.py 614; install_ccsession.py 161; WORKER-CONTRACT 339 lines with WC-2..WC-16; 116 removed tests; 10 removed files; 10 verbs; cycle.py:35 dead constant, :44 SKEW_WARN_S = 60; orca_worktree.py:822 IR7_REFUSE = False; guard :409 `implement | task | cleanup`; design doc line counts (942, 706, 509, 470, 627, 119, 57, 51); 19 fixture files; refs/ has the five named files; agent pins.

Found wrong:

- **"17 templates" / "list the 17 files"** (task lines 451 and 469, Agent 04). The snapshot folder `src/superclaude/skills/sc-issue-protocol/templates/` holds **15** files (accuracy-check-comment, claim-comment, create-review-comment, description, draft-notes, flags-decision, issue-bug-complex, issue-bug-simple, issue-feature-complex, issue-feature-simple, issue-summary, launch-prompt, next-steps, recommend-record, scout-report). research-notes says 17; scope-4's own enumeration is 15 (7 claim + 8 create). The false number is inherited from research-notes (M1).

Facts the task adds that research does not contain (decisions, not facts): sandbox location inside the task folder; Section 6/7 assigned to synth-02; Appendix A/B naming; N = max(5, lines/100). All are recorded in Builder Notes. No invented file names or numbers beyond M1 and N1.

## Checklist 4: edge cases from the research and their verification clauses

| Edge case (source) | Reflected in a clause? |
|---|---|
| Dead constant MAX_LAUNCHES_PER_CYCLE, real limit is `self.halt` (scope-1) | Yes: Agent 01 topic, hint, Step 5.3 (8), Section 11 |
| `enabled` false: dry-run ignores it; DISABLED checked twice (scope-1/3) | Yes: Agents 01/02/03, 5.3 (1) |
| All Orca reply shapes `_assumed_shape`; live-test record absent (scope-1/2/3) | Yes: Agent 02 hint, 14.3 |
| PR numbers #447/#448 and "never run live" unverifiable (scope-1) | Yes: 14.3, synth-01 evidence-limits paragraph |
| Default-level rule is prose, not code (scope-4) | Yes |
| IR7_REFUSE=False, `pending` has no caller, pipeline.json not built (scope-4/5) | Yes: ledger rows, 14.2 |
| `orca worktree create` has no `--agent`, no link flag (scope-4 #1) | Not explicit; Agent 04 asked to give exact orca argv (covered by "orca_worktree.py ... what it actually does") |
| Shim not carrying level (scope-5) | Yes |
| Plugin copies byte-identical, but plugin hooks.json differs (lacks three ccsession-tag registrations) (scope-5) | Scripts: yes (Step 2.5 compares the three scripts). hooks.json difference: not named (Note N6) |
| `degraded` marker word blocks all Bash in identity hook (scope-5) | No (Note N5) |
| Claim marker as the claim-to-watcher feedback path (scope-3) | No (M4) |
| Watcher-launched and coordinator-started sessions are not governed (scope-3/5) | No (M7) |
| Third reader of the watcher config file (scope-3) | No (M6) |
| `status` skips platform check; `reset` usage errors write no audit line vs design 7.1 (scope-1) | No explicit clause; Agent 03 line-by-line reconciliation of design sec 4/7/10 would likely catch it (Note N7) |
| `grant row` phrase exists once in the snapshot contract (WORKER-CONTRACT.md:57) (scope-6 gap) | Conflicts with the "not found in snapshot" rule (M2) |
| Removed-code appendix must be read only via `git show 01e7a9e23^` | Yes, all Part B prompts |
| Approvals-store default path unknown in the removed code (scope-6) | Agent 06 deliverable (e) State stores covers it |

## Checklist 5: dependencies and phase ordering

Phase 1 (template digest, tier, fingerprint) before Phase 2: correct. Phase 2 parallel spawn, 2.7 aggregation, then Gate 1 (3 report-only agents in parallel), consolidation (3.4), gap-fill, verification, decision, verdict (3.13), gaps-and-questions.md (3.14) before any synthesis: correct. Phase 4 skip item. Phase 5 synthesis in parallel (independent), Gate 2 after all six, assembly after Gate 2, Gate 3 after assembly, Gate 4 only if gate3-verdict PASS, final checks after both. Input dependencies per synth file:

| Synth | Reads research | Needed by its content requirements | Gap |
|---|---|---|---|
| synth-01 | 01-06 + gap log + FEATURE_ANALYSIS | all rows of the ledger | none |
| synth-02 | 01-05 + gap log + EXISTING_FILES | trigger table 4.4 and gate table 4.6 cover every piece, including coordinator text and removed package | **does not read 06** (M3) |
| synth-03 | 01-03 | 5.1 | none |
| synth-04 | 04, 05, 06 (part A) | 5.2-5.4 | none |
| synth-05 | 01-06 | sections 8-11, Appendix A | none |
| synth-06 | all six, 06 in full | 14, Appendix B | none |

## Checklist 6: is any `[CODE-CONTRADICTED]` doc claim treated as true?

No item adopts a contradicted claim. Each of the eight BUILD-REQUEST warnings is passed to the relevant research agent as a "hint, re-verify", each synth prompt has rule 10 ("[CODE-CONTRADICTED] claims must be corrected to match the code") and rule 11, and the three accuracy lenses check it. Two phrasings need care:

- BUILD-REQUEST warning 3 and the task's 14.1 template list "has no dispatcher or zero-setup step" inside the doc-vs-code CONTRADICTION table. There is no doc claim to contradict (the concept exists only in the owner's memory notes, which are not sources). Placed in table 14.1 it forces an invented "doc claim" column. It belongs in 14.2 as a NOT BUILT row (Note N11).
- The task's Section 2.4 hand-off list and the ledger say "L2 pre-push BUILT-ON". scope-4/5 show the L2 hook is installed only by the claim at governed levels and the watcher always passes `--pipeline none`, so for the watcher path it is never installed. The ledger "Trigger" column covers this only if the synth agent states it (see M7).

## Issues

### Blocking

None. Executing the task as written would not lose a required deliverable of BUILD-REQUEST items (a)-(g) and would not by itself print a false fact in the final document. The Medium items below should be fixed before execution because each one either puts a false number into a prompt or leaves a research finding with no task item that carries it.

### Medium

**M1. False count "17 templates" in Agent 04 (task lines 451 and 469).** The snapshot templates folder holds 15 files (list under Checklist 3). Origin: research-notes.md "templates/ (17 files)"; scope-4 itself lists 15. The item says "list the 17 files" and "(the 17 templates)". Fix: replace with "list every file in the folder (15 at the snapshot)" or drop the number. If the number reaches the Section 1 statistics table it becomes a false fact.

**M2. "grant row" rule conflicts with the snapshot.** Rule C (every research, synth, QA prompt) and Step 7.1 check (5) (task line 2250: "confirm each [zero-setup / COORD- / grant row] is stated as 'not found in snapshot'") treat "grant row" as absent. `grep -n -i 'grant row' src/superclaude/core/WORKER-CONTRACT.md` finds it at line 57 ("such as a grant row or a pass record, are still written by the owner"), as scope-6 sec 1 and sec 7 record. The removed "Issue pipeline duties" text (Appendix B.5) also says "post an issue write without that issue's grant row". A faithful document must say "appears once at WORKER-CONTRACT.md:57, no definition, no store or verb named" and must not say "not found". As written, Step 7.1(5) and the QA lenses can force a false statement or a false blocker. Fix: restrict the "not found in snapshot" rule to `zero-setup watcher`, `COORD-` and `dispatcher` (as an issue-watch component), and add "grant row: report the single hit at WORKER-CONTRACT.md:57 and the old-tree hit".

**M3. synth-02 (Step 5.2) does not read research file 06.** Its required content includes the trigger table 4.4 "Piece | What starts it | Who or what runs it ..." and the gate table 4.6 for every piece. Research 06 deliverables (d) triggers and (f) gates are the only source for the coordinator-text and removed-package rows (the removed verbs were run by a coordinator following WC-17; the current contract names no trigger). Without 06 the agent must write "no trigger found in snapshot" without evidence, which for the removed package is false, and will disagree with the ledger Trigger column that synth-01 (which reads 06) writes. Fix: add `06-coordinator-text-and-removed-code.md` (deliverables (d) and (f) only) to the Step 5.2 read list.

**M4. The claim-to-watcher feedback contract is not carried by any item.** The only link from a running claim back to the watcher is the claim comment ending `<!-- sc:issue:claim -->`: watcher reads it via G4 and `MARKER_JQ`, applies the 300 s marker window, and moves the entry to `claimed` (T-10/11/12) (scope-3 sec 2.4; scope-2 sec 2.2/2.3). The string does not occur anywhere in the task file. Section 2.4 (integration map) lists watcher to claim, claim to guard, claim to L2, guard to orchestration, but not claim to watcher; 8.3 (hand-off contracts) lists the launch prompt, launch-level files and install_l2 only. The owner's question "how do the pieces cooperate" loses its closing edge. Fix: add "claim marker comment (`<!-- sc:issue:claim -->`, MARKER_JQ, marker window, T-10..T-12, pinned by test_marker_contract.py)" to the Step 5.1 2.4 list and the Step 5.5 8.3 list, and to Agent 02 topic (2).

**M5. GitHub writes by the launched agent at `--pipeline full --submit` are not requested.** BUILD-REQUEST emphasises "what each piece writes to GitHub". scope-4 sec 2.1/2.3: the launched agent runs, at `full --submit`, a conventional commit, `git push origin <branch>` and `/sc:pr-submit --monitor 3` (launch-prompt.md:28-34), which creates a PR. Agent 04 item (2) lists "assign, comments, summary, next-step prompt, labels" and the `--create` path; Step 5.4 5.2 (3) lists "every write ... of the claim path vs create path". The submit-time push and PR creation are never named as writes, nor as the point where guard classes SUBMIT/PUSH/COMMIT are allowed (FS only). Fix: add a third group "launched-agent writes at level full --submit (git push, gh pr create via /sc:pr-submit, evidence launch-prompt.md and guard matrix)" to Agent 04 (2), Step 5.4 5.2 (3) and Step 5.2 4.5.

**M6. A scope-3 finding about a shared config file was dropped, and it hides a likely real contradiction.** scope-3 sec 2.4: `skills/agent-work-report/scripts/common.py:22-25` reads `~/.config/superclaude/issue-watch.json`, key `orchestrator_repo` (comment: "is the one place that holds the absolute path of the orchestrator repo (spec 4.4)"). scope-1 sec 3 #7 records that `load_config` rejects unknown keys. I verified: cycle.py:58-67 `_TOP_KEYS` has no `orchestrator_repo`, and cycle.py:216-219 raises `unknown configuration key`. So a config that satisfies the other consumer fails `issue-watch once`/`check-config` (exit 2). No task item asks any agent to find, tag or place this (Agent 03 deliverables: config schema; Step 5.2 Section 6: readers of dispatch.json only). Fix: add to Agent 03 topic (2) "grep the snapshot for other readers of `issue-watch.json` and compare their keys with `_TOP_KEYS`", and to 14.1 as a candidate contradiction.

**M7. "Which launch paths are governed by which guard layer" is not assigned.** scope-3 sec 2.4 (marked inference) and scope-5 doc-vs-code row 7 [CODE-VERIFIED] say: the watcher always launches with `--pipeline none`, which creates no worktree and writes no pending record; a session with no `sessions/<sid>` record is "ordinary" to L1 and to the identity hook; L2 is only installed by the claim at governed levels; a coordinator-started worker has no marker and so no L1/L2 (orchestrator.md DQ7, SUPERVISED ref l.268). So for the watcher-driven path every guard layer is dormant. This is the answer to "guard layers versus launch paths" that the owner asked for (BUILD-REQUEST WHY), and the scope-3 inference was never converted into a check item. Agent 05 covers "fail-closed governed versus fail-open ordinary" generically. Fix: add to Agent 05 an explicit table "launch path (watcher `--pipeline none`; manual claim worktree/full/full-submit; coordinator-started worker) x layer (L1, identity, L2, G2 rule 2) with evidence", and one ledger/4.3 row for it.

**M8. Appendix A will miss tests the research itself names as pinning pipeline behaviour.** scope-4 sec 4 names `tests/skills/test_clickup_claim.py` (pins `clickup_claim.py`, a claim write path that Agent 04 is told to document) and `tests/skills/test_model_alias_policy.py` (cited at refs/tiers.md:54); scope-5 names `tests/unit/test_cli_doctor.py`. All three exist in the snapshot. They are on no agent list and the Appendix A rule only lets a row be added "if a research file shows it pins pipeline behaviour", which cannot happen when no agent is pointed at them. BUILD-REQUEST asks for "every test file that pins behaviour". Fix: add `test_clickup_claim.py` and `test_model_alias_policy.py` to Agent 04's test list, `test_cli_doctor.py` (ccsession references only) to Agent 05's, and name them in the Appendix A list.

### Notes (form or low impact)

- **N1.** Agent 01 item and header say "six test files"; the prompt names five (test_cycle, test_predicates, test_audit, test_marker_contract, conftest). Harmless for the check as worded; fix the word.
- **N2.** Replace "Glob on `test_launch*` and `_*` patterns" (task line 577) and "underscore-named launch-level companion files" (task line 2136) with the four exact names: test_launch_level_guard_l2_tokens.py, test_launch_level_guard_registration.py, test_launch_level_guard_with_identity.py, test_launch_level_guard_worker.py. None of the names in the research is wrong; only the underscore-prefix idea is.
- **N3.** Agent 02's file list omits `src/superclaude/cli/swarm/atomic.py` (record.save atomic write, scope-3 sec 3.3) and `src/superclaude/cli/install_user_setup.py` (`_ORCA_CLIS`, `_find_orca`; test_find_orca_parity compares against it). Add both.
- **N4.** The "no placeholder text (`[`, ...)" check in Phase 5 and the `YYYY` grep in Step 7.1(3) will hit legitimate content: `[CODE-VERIFIED]` tags, `[sc-launch:v1:<nonce>]`, and the time-format spec `YYYY-MM-DDTHH:MM:SSZ` (scope-3 sec 3.2). The Phase 5 text says "outside table cells that quote code"; make it "outside tags and quoted source".
- **N5.** Guard edge case `degraded` word (guard level W with LL-STATE note; identity hook rejects it so every Bash call is blocked; pinned at test_launch_level_guard_with_identity.py:187) has no clause. Add to Agent 05 deliverable (a).
- **N6.** Plugin `hooks.json` differs from src by lacking the three ccsession-tag registrations (scope-5 sec 2.4). The task says "plugin byte-identical copies" in 5.3 (9) without limiting it to the three scripts; limit it.
- **N7.** scope-1 doc imprecisions with no clause: `status` skips the platform check (cli.py:169 vs :84); `reset` usage errors write no audit.jsonl line (design 7.1 says "every exit"). Agent 03's reconciliation should catch them; naming them would make it certain.
- **N8.** Nuances with no clause: `rate_limit_wait` header parsing works only for G1 (github.py:380-385); doc "never" for title/body text vs audit `host`/`login` accepting any printable token (audit.py:234-235).
- **N9.** Appendix B inventory: the removing commit (36 files) also changed main.py (registration -4), docs/user-guide/cli-groups.md, CHANGELOG.md (+4 lines), SUPERVISED ref line 268 (+1 sentence) and the plugin copy of the guard (scope-6 sec 5). Agent 06 Part B does not ask for these; add one line "other files touched by 01e7a9e23" to B.1.
- **N10.** tests/hooks/test_require_orca_worktree_agent.py and ..._governed.py (the worktree gate hook registered in hooks.json) are not on any list; the SUPERVISED ref (l.276) says the claim script's `orca worktree create` runs outside that hook. Decide whether this adjacent layer is in scope; if not, say so in 5.3.
- **N11.** Move "no dispatcher / zero-setup step" from the 14.1 contradiction list (task line 1323, BUILD-REQUEST warning 3) to the 14.2 NOT BUILT list.
- **N12.** Agent 03 is told to grep the whole snapshot for `dispatcher`; unrelated hits exist (cli/eval, cli/swarm, docs/eval/retention.md, and the Orca CLI dispatcher script at SUPERVISED ref l.276/1542). Say "relating to issue-watch or coordinator start of a worker" so the ledger row is not confused.
- **N13.** Target length is stated as "about 1,300" (Steps 1.4, 3.1) and "about 800-1,300" (Step 7.1); research-notes says 800-1,200 allowed to about 1,300. The per-section budgets in the synth prompts sum to roughly 1,280-2,095 lines. Information only.
- **N14.** Setup doc line 288 gives the cron as six fields, seconds first (`0 */5 * * * *`); standard cron has five. The doc says so itself, so it is not a contradiction, but it is an owner action risk (scope-2 sec 3, gap 6). Add to Agent 03 (5).

## Result summary

- Required findings of the six scope files and research-notes sections that have a task item: all but M4, M6, M7 (and the lesser N-items).
- Research assignments 01-06 cover the correct files and all 43 test files plus the fixtures directory; test counts per agent are right except N1.
- Fabricated or false facts in the task text: one (M1, 17 vs 15 templates), inherited from research-notes.
- `[CODE-CONTRADICTED]` claims treated as true: none.
- Phase ordering and dependencies: correct, with one missing input edge (M3).

VERDICT: PASS
