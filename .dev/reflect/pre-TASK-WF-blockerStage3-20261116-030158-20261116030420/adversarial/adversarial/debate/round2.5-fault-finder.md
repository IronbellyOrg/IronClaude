# Round 2.5: invariant probe, independent fault-finder, model class sonnet, agent a132c84bc6e265043

(Persisted verbatim by the orchestrator from the agent's final message; hand-back frame indentation removed. The agent wrote no file.)

**INV-001** | state_variables | The consensus fix for C-001 (run `shadow_summary.py` inside this package, then check the entry conditions) assumes the entry condition can be met after the owner's go. | UNADDRESSED | HIGH | `source.md:3` requires the summary to exist "and the owner has read it". The go is checked at PLAN:36, before any regenerated summary exists, so the owner cannot have read the 5-run numbers when saying go. Stage 2 `PLAN:110` allows "zero is allowed". The regeneration has to be an owner-read step before the go, or the go has to be re-recorded after it.

**INV-002** | guard_conditions | A failed acceptance line halts the run and nothing alters the evidence file. | UNADDRESSED | HIGH | `sc-implement-protocol/SKILL.md:145` says a non-compliant task gets "exactly one fix pass, re-run Q2–Q4 once", then a repair round. That fix pass could edit `seeded-recall-result.md`, the stage 2 summary or the ledger row until the check passes. The C-003 fix ("recorded owner ruling") has the same hole. Task 1 should record the result file's hash. The ruling must be dated after that hash and cite it.

**INV-003** | collection_boundaries | The Task 3 gate (PLAN:62) can be passed on the seeded set. | UNADDRESSED | HIGH | PLAN:33 requires "the cosmetic block share falls", which is a strict fall. If the old rule blocks 0 of the cosmetic defects, the new rule cannot fall below 0. Stage 0 `:109` plants only "at least one defect in each of the four classes". Stage 0 `:106` says "the advisory fallback is the expected outcome". Halting is therefore the expected path, not an edge case. C-003 needs a rule for zero-base and small-n classes as well as advisory ones.

**INV-004** | guard_conditions | The U-004 fix (add `test_review_severity_registry.py` to PLAN:125) is enough. | UNADDRESSED | MEDIUM | Stage 1 `:209` says "a row at `legacy` is accepted" and `:213` says the test passes "with all `digest` rows at `legacy`". Tasks 4 and 5 say "Set the registry row to `v2`" but have no acceptance line for it (PLAN:75-79, 87-91). A forgotten flip passes silently. Add an explicit `v2` check for the three stage 3 rows.

**INV-005** | sufficiency_challenge | U-006 is only under-specification. | UNADDRESSED | MEDIUM | `test_review_severity_rule.py:181-203` checks all ten files against `canonical_rule_bullets()`. PLAN:122 makes that read `refs/rule.md`. The 8 files still at `legacy` hold the old bullets, so `_rule_body(s1) in flat` fails for them. PLAN:125 ("passes") cannot be met unless the implementer invents frozen legacy text.

**INV-006** | interaction_effects | Task 3 changes the rule, and `make sync-dev` makes it live. | UNADDRESSED | MEDIUM | `Makefile:126-130` and `:112-125` copy agents and skills into `.claude/`. That includes the v2 `rf-qa.md` after Task 4 and the task skill after Task 7. The Makefile has no `output-styles` copy, and `pragmatic-subagent.js:7` reads `~/.claude/output-styles`. So the QA for Tasks 5 to 11 runs under the new `rf-qa` digest plus the old injected style, which is the RK15 blend, and the plan does not say so. Task 3's "run `make sync-dev`" does nothing for `pragmatic.md`.

**INV-007** | sufficiency_challenge | Tasks 4 to 7 cover the carriers' cap and fix-step edits. | UNADDRESSED | MEDIUM | Spec `:866` lists `rf-qa-qualitative.md` "110, 809, 994" for the cap and L2 edits. Task 5 touches none of them. Only `rf-qa.md` gets L2 and L3 (PLAN:73). Line 994 sits inside the hashed `## Critical Rules` block, so it would also move the Task 9 hash.

**INV-008** | guard_conditions | The L2 helper can be called by the text that requires it. | UNADDRESSED | MEDIUM | PLAN:45 creates only `fixcheck.py` and its test. It adds no subcommand and no registration in `cli/review/__init__.py`. Stage 1 `:171` shows the pattern a command needs. The Fix Cycle text in `rf-qa.md` and the task skill (Tasks 4 and 7) therefore has nothing to invoke.

**INV-009** | sufficiency_challenge | Tasks 8 and 9 re-run every test the edits can break. | UNADDRESSED | MEDIUM | `tests/skills/test_task_builder_merge.py:436-439` pins "Retry Monotonicity Protocol", "PR-02" and "INV-012" in `rf-qa.md`. Task 4 rewrites its Fix Cycle section. PLAN:125 and Task 9 (`tests/audit`) never run that file.

**INV-010** | state_variables | Task 1 tests the same digest that Task 3 ships. | UNADDRESSED | MEDIUM | PLAN:33 uses "the digest of spec section 4.1". PLAN:63 ships the digest section of `refs/rule.md`, written by stage 1. Nothing checks that the two are equal.

**INV-011** | guard_conditions | The answer key stays hidden. | UNADDRESSED | MEDIUM | Stage 0 `:106` puts the planted text and the correct text in `seeded-recall-set.md`. That is the file Task 1 reads for the three requirement lines. Stage 0 `:111` only says the key is "in a file reviewers are never given". PLAN:40 does not say which files the reviewers receive.

**INV-012** | collection_boundaries | Recall and Wilson intervals are computed on a clear unit. | UNADDRESSED | MEDIUM | PLAN:33 does not say whether "found" means any, majority or each reviewer. Three reviewers on the same defects are not independent trials. Separately, "zero safety misses" in stage 2 `:110` is a count over ledger rows. It cannot see a defect nobody recorded, so Task 11 should say "detected".

**INV-013** | sufficiency_challenge | Task 11 states the triggers and baselines the window needs. | UNADDRESSED | MEDIUM | PLAN:158-161 names RT1, RT2 and M12. Spec `:989` RT5 needs an M1 baseline, and `:962` sources it from "stage 2 paired data". Stage 2's summary (`:110`) does not produce it. This extends U-003.

**INV-014** | state_variables | The revert in PLAN:162 undoes the pilot. | UNADDRESSED | MEDIUM | "Per carrier row" covers 3 digest rows. `rf-analyst.md`, the task skill's L1 to L3 text and `promote` on (Task 7) have no registry row. Spec `:981` defines a revert only as restoring "the previous digest".

**INV-015** | count_divergence | The counts in the plan match the files. | ADDRESSED | LOW | Checked and holding:
- The scan finds 14 hit lines in 11 files. Excluding the auggie file gives the plan's "13 lines in 10 files". `plugins/superclaude` has none.
- There are 8 FAIL lines in `rf-qa-qualitative.md` (240 to 784, each with a PASS bullet one line above).
- The cap sentence appears 3 times in `task/SKILL.md` and 2 times in `rf-qa.md` (402, 549).
- `S1_S3_FILES` has 10 files, and `pragmatic.md` lines 225, 226 and 229 match PLAN:59.

Still stale: "Tasks 34 to 37" and `t38` (C-005). PLAN:19 says "the ids are in the stage ledger", but `README.md:18-21` leaves the package-id cells blank for stages 1 to 4.

**INV-016** | collection_boundaries | The Task 10 allow-list is always readable. | UNADDRESSED | LOW | PLAN:149 fails only when a listed file is missing. A missing or empty section, or a prose line parsed as a path, is not covered. The existing tests read `git ls-files` (`test_review_severity_rule.py:36-44`). A temp-tree test and a current-tree scan need a disk walk. The L1 text written in Tasks 4 and 7 must avoid the three phrases, and Tasks 4 and 5 must avoid them in `scale-map.md`.

**INV-017** | guard_conditions | Task 1 does not decide whether the run proceeds. | UNADDRESSED | LOW | PLAN:33 says "the owner decides whether stage 3 may proceed". The go was already recorded at PLAN:36, so a pass at PLAN:62 proceeds with no owner action.

Total 17 findings. UNADDRESSED: 3 HIGH, 11 MEDIUM, 2 LOW. INV-015 is ADDRESSED.

**Sufficiency.** The claim is falsified even with all seven blocking items fixed. INV-003 halts the gate by construction. INV-001 and INV-002 let the entry and result gates be satisfied by editing evidence. INV-005 and INV-009 leave a re-pin check that cannot pass and a pinned file that is never run.
