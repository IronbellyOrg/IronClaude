# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines)
Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks)
Author: orchestrator inline (requirements-analyst delegation replaced by inline Step 1B.0, see audit.log)

## Coverage summary (Step 1B.0, deterministic matcher over 40 quote-pinned rows)

- Pass 1 (regex `R-|REQ-|SPEC-|T-`): 0 parsed IDs in the spec (its labels are `FR-n`, `F<n>`, `G<n>`, `O<n>`, which the ID regex does not match) and 0 in the plan.
- Pass 2: 40 inferred rows (`INF-001..040`), all quote-pinned and validated against `source.md`.
- `coverage_pct` = null (parsed total 0). `coverage_pct_union` = 0.925 (37 of 40). `coverage_degraded: parsed-sparse` (inferred 40 > parsed 0), so no Tier-1 stop is allowed.
- Unmatched by the containment rule: INF-004, INF-005, INF-007. Manual read shows each IS covered (Task 3 static purity test, Task 3 `fix_cycle_id` ValueError criterion, Task 4 `classify_toggles` criteria); these are matcher misses on short quotes, not plan gaps.
- Three matcher picks are not the best task by reading (INF-037 best is Task 5, INF-040 best is Task 11, INF-034 spans Task 1 plus all tasks). Recorded in the report, not corrected in the matrix.
- Every spec requirement span has at least one owning task. The gaps below are about depth of the acceptance criteria, not missing tasks.

## Findings (author confidence in brackets)

1. [0.80] Task 8 builds `refs/merge-guard.md` "from ./source.md sections 3, 4.1, 4.5, 4.6 and 5" and omits section 4.2 (plan line 124). Section 4.2 holds the only definition of the event fields the SKILL must append: `timeline_baseline` and `original_is_draft` on the first request only, `idempotency_key = guard:<run_id>:<cycle_id>:<to>:a<k>`, and what `k` counts (spec lines 182-185). No Task 8 acceptance criterion names any event field (plan lines 126-130). Task 3's fold reads these fields; nothing in the plan makes the protocol write them. A ref without them gives events the fold cannot interpret (no `baseline` makes `classify_toggles` subtract from nothing).
2. [0.70] Task 9 requires the Wave 0 bullet to "carry no L3 or `draft` condition" and its test to fail "when it names an L3 or `draft` condition" (plan lines 137, 140), yet the same task requires the bullet to say that "at L3 with `--merge-guard off`" the unprotected line prints once (plan line 137). The sentence the task requires names L3. The spec has the same tension (source.md line 241). An implementer must guess whether the test forbids the word or a gate.
3. [0.65] Task 4 states the `classify_toggles` slack correctly (`run_toggles + unsettled + failed_mutations`, plan line 70) but its acceptance test only checks `observed == run_toggles + failed_mutations` for `ok` (plan line 74). An implementation that drops the `unsettled` term passes every listed criterion. Spec lines 118-120 define slack with `unsettled`; a landed-but-unsettled request would then read as `foreign` and disable the guard.
4. [0.60] Task 3 never fixes how the fold's `cycle_id` moves. `held_cycle_published` compares a `push_completed` against `guard.cycle_id` (spec line 108, plan line 56) and the fold table lists the field without an update rule (spec lines 187-193). No Task 3 criterion covers a second cycle (`fix-2` after a released `fix-1`). An implementation that keeps the first cycle's id returns `published: false` for later cycles, and a crash after a normal push of cycle 2 leaves the PR draft.
5. [0.55] Task 10's acceptance criteria never check the cycle-id reuse that spec section 4.6 requires (the id minted at the end of Wave 3 is the `cycle_id` of the push triad and of `rereview_requested`, spec line 251). Task 8 states it in the ref and Task 11 checks the event order, but no protocol-text test pins the reuse in `SKILL.md`.
6. [0.50] Task 5 asserts `state["draft_guard"]["phase"] == "held"` and `engage_pending` (plan line 90), but Task 3 never fixes the `Phase` string values (spec lines 77-80 list names only). The first value choice that differs fails Task 5 rather than Task 3.
7. [0.45] Task 7's criteria do not test that `autoMergeRequest` is emitted as a boolean (spec line 230 shows `"autoMergeRequest":false`; `gh pr view --json autoMergeRequest` yields an object or null), which `GuardRead.auto_merge_armed` needs.

## Structural signals

- S_scope: 13 tasks; S_domains: 4 (python core, shell script, protocol prose, docs); S_dev_density (union): 3/40 = 0.075 (matcher misses, see above).
- Recommended rubric result: ESCALATE. Tier 2 is pinned by the caller (`--tier 2`), so the pin decides.
- Grounding note: the repository already contains the landed implementation of this plan (files named by the plan exist). Plan claims were checked against existing symbols (all named tests and constants resolve); no finding relies on the landed code being absent or present.
