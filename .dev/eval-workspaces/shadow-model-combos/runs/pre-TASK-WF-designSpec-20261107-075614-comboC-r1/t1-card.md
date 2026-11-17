# Tier 1 reflection card: UC-1 pre-execution audit

- run: pre-TASK-WF-designSpec-20261107-075614-comboC-r1
- spec: input/TASK-WF-designSpec-20261107-075614/source.md (378 lines, "Design Spec: pr-submit merge guard (issue #375)", v3)
- plan: input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (200 lines, 13 tasks, 5 phases)
- attribution note: both files are an archived package (frozen copy). The spec's repo facts were read at master e8db2fe6 (2026-11-07). Repository HEAD has moved since and already carries the shipped feature. HEAD code is NOT evidence about what the plan says or whether the plan was sound when written. Check a repo fact with `git show e8db2fe6:<path>`.

## Coverage (Wave 1B, two-pass extraction)

- Pass 1 (ID_REGEX `R-/REQ-/SPEC-/T-`): 0 parsed IDs. The spec labels its requirements FR-n, F-n, G-n, O-n, D-n, which the regex does not match. parsed_count = 0.
- Pass 2 (quote-pinned inference): 45 INF rows, every quote verified verbatim at its cited line (0 dropped).
- Matching (containment >= 0.6): 37 matched, 8 unmatched. coverage_pct = null (parsed total 0); coverage_pct_union = 0.8222; S_dev_density = 8/45 = 0.1778.
- Step 1B.2b: inferred (45) > parsed (0) so coverage_degraded = parsed-sparse; no Tier 1 stop may fire.
- The 8 unmatched rows (INF-001, 014, 017, 018, 027, 028, 029, 031) were read by hand against the plan. Each is carried by a task by other wording (Tasks 3, 4, 6, 7, 8, 12). The deterministic rule reports them as unmapped; this is a matcher false negative, not a plan gap [INFERRED].

## Grounding performed (Read / git show at e8db2fe6)

- Import cycle risk (spec F13, plan Task 3 constraint): `conflicts.py` imports only `.fsm` and `.models`; `fsm.py` imports `.loop_guard`, `.models`, `.severity_router`; `run_log.py` imports only `.models`; only `recovery.py` imports `.run_log`. No cycle run_log -> merge_guard -> conflicts. The spec's claim holds.
- Enum-count pins (Task 2): the "43" claims sit in `models.py` (module docstring and class docstring), `run_log.py` (append docstring), `refs/loop-guard.md` (heading and "EXACTLY 43"), `test_run_log.py` (test name and two asserts) and `test_codex_reviews.py` (one assert). Task 2 names all of them.
- Allowed-tools rule (Task 8/9 worry): the SKILL front matter grants `Bash(gh *)`, `Bash(git *)`, `Bash(uv *)`, `Bash(make *)`, `Bash(jq *)`; `test_allowed_tools_cover_every_program` only checks that a `scripts/` path exists on disk. No front-matter edit is needed for the new script. Hypothesis refuted.
- Plan symbols all exist at e8db2fe6: `_NEW_KEY_DEFAULTS`, `CORE_PURE_FILES`, `_RESOLUTION_SCRIPTS`, `WRITE_VERB_CLASSIFICATION`, `test_conflict_max_tier_default_and_bounds`, `test_t105_runtime_repo_pin`, `test_tn50_core_pure_no_gh_git_tokens`, `test_allowed_tools_cover_every_program`, `test_intent_and_validator_lines_say_tier_2`, `scripts/retrigger-review.sh`, `tests/pr_submit/test_conflict_scripts.py`.

## Findings

F1 (MAJOR, not blocking, missing-requirement). Task 7 never fixes the timeline count semantics with a failable check. Spec section 4.4 requires `gh api --paginate` over the timeline and a count of `convert_to_draft` plus `ready_for_review` events (source.md:230), and the toggle classifier depends on that count (source.md:114-125). Task 7's acceptance criteria (plan:111-113) check only that the JSON line carries the keys and that a failing timeline call gives `transitions: null`. No criterion feeds N timeline events and asserts `transitions == N`, nor asserts `--paginate` in the recorded call. An implementation that counts one event type, or drops `--paginate`, passes every criterion.

F2 (MINOR, contradiction). Task 9 asks for a Wave 0 bullet that "carries no L3 or `draft` condition" (plan:137) and in the same sentence has it print the off line "at L3 with `--merge-guard off`". Its first criterion fails the bullet when it "names an L3 or `draft` condition" (plan:140). The required text names L3 and the word draft ("no draft call is made"). The spec has the same tension (source.md:241). The executor must guess what "condition" means (a gate on loading the ref).

F3 (MINOR, missing-requirement). The auto-merge signal has no failable criterion. Spec engage row 11 says `notes` carries `auto_merge_armed` when set (source.md:143) and the traceability table ties FR-10 and FR-11 to the `autoMergeRequest` field (source.md:352). Task 4's criteria assert action, reason and cause per row (plan:73) and Task 7's criteria never check the `autoMergeRequest` value. A decision function that drops `notes`, or a script that always prints false, passes.

F4 (MINOR, missing-requirement). The owner decision that "the run that opens the PR must not enable the feature (`--merge-guard off`)" and that "the PR body states the gate plainly" (source.md:326) is recorded in Task 1's prose (plan:33) but Task 1's criteria (plan:36-38) check the base-commit record, G1-G6 rows and O1-O4, not this instruction. Nothing mechanical can fail on it.

F5 (MINOR, missing-requirement). Spec fold row for a settled `not_applied` ready request returns to `HELD`, "or `RELEASE_PENDING` when a failed release preceded it" (source.md:201). Task 3's criterion tests only the `HELD` outcome (plan:60). The failed-release variant is untested.

## Self-reported confidence

0.80 overall. Every finding is a plan-versus-spec acceptance-criterion gap, with citations into the two snapshot files. The one sweep that could contain a stronger defect (a design-level logic error in the spec's decision tables) was not exhausted at Tier 1.
