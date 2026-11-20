# Diff analysis: three remediation variants for watcher plan v3 (Q-1 to Q-10)

Variants: V1 = opus security (`variant-1-opus-security.md`), V2 = opus architect (`variant-2-opus-architect.md`), V3 = sonnet analyzer (`variant-3-sonnet-analyzer.md`). Paths are under `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/adversarial/`. Taxonomy: L1 surface, L2 structural, L3 state mechanics (guards, invariants, state changes).

## 1. Structural differences

| Aspect | V1 | V2 | V3 | Severity |
|---|---|---|---|---|
| Order | safety boundaries first (Q-1A, Q-1B, Q-2), then Q-3..Q-10 | register order, each tagged BLOCKING/OWNER/NOTE | ranked table by impact, then register order | Low |
| Per-finding shape | Change / Files / Risks / Tests / Rejected | Evidence / change / plan edits / tests / rejected | Fix / What it breaks / Failure modes / Tests / Rollback / Rejected | Low |
| Scope flags | none | marks `[SCOPE+]` on edits beyond the finding | none | Low |
| Unverified items | listed in residual risks | listed per finding | listed in a final "Unverified" list | Low |

## 2. Content differences per finding (points)

| ID | Point | V1 | V2 | V3 | Level |
|---|---|---|---|---|---|
| D-01 | Q-1 guard class name and match scope | new class `ISSUEWRITE`: issue create/edit/comment plus close/reopen/delete/transfer/lock/unlock/pin/unpin/develop, plus every `label` and `project` verb except list/view | new class `ISSUE`: `'issue '*` placed after guard:652 so view/list/status stay allowed | new class `ISSUEW`: only create/edit/comment | L3 |
| D-02 | Q-1 coordinator-only pattern (guard:444) | `*issue-pipeline*complete* \| *issue_pipeline*complete*` | `*issue-pipeline*complete* \| *issue_pipeline.complete* \| *issue_pipeline/complete.py* \| *issue_pipeline*import*complete*` (avoids refusing `pytest tests/issue_pipeline/test_complete.py`) | same as V1 | L3 |
| D-03 | Q-1 guard version stamp (guard:10) | not mentioned | bump to 2, scope+ (stale host guard passes IR-4 preflight) | says unread, check | L3 |
| D-04 | Q-1 part B: self-approval by the launch account | `excluded_ids` in `approval_of`, watcher's own account cannot approve; owner approves from another login | not proposed; residual risk only | not proposed; residual risk only | L3 |
| D-05 | Q-2 ship gate mechanism | module `ship_gate.py` with `REQUIRED`/`PASSED = frozenset()`; new Task 4b; skip `ship_gate_closed`; coupling test with `_PENDING` list | Option A: constant `GOVERNED_LEVELS_ALLOWED = False` in launch.py, reason `level_gated`; Option B waiver; A2 split per level; recommends A | config key `launch_levels_gate` default `closed`, reason `launch_gate_closed`; flip or waive | L3 |
| D-06 | Q-2 who can open the gate | code edit only; rejects config key and env var as agent-writable | code constant, reviewed PR | config key flipped by the owner | L3 |
| D-07 | Q-3 updatedAt approach | read Status/Pipeline value `createdAt/updatedAt` plus item time; owner observation artifact; fallback level label | Option C field-value times, confirmed once by owner Task 3a (scope+); B fallback | owner observation with decision table; tolerance window rejected | L3 |
| D-08 | Q-4 reason precedence in `_revalidate` | order: approval reread, time rule (`edited_after_approval`), then project_check/equality (`revalidation_failed`) | `edited_after_approval` first after items reread, then `revalidation_failed` | all `_revalidate` failures give `revalidation_failed`; `edited_after_approval` only from `_examine` | L3 |
| D-09 | Q-5 Project target | `project_id` param, compare-and-set Status only if currently Research/Spec/Plan/Debug, else comment only `status_moved_by_person` | `project_id` validated `^PVT_...`, refusals `project_missing/ambiguous/status_option_missing`, verb takes `--project-id` | Project id from repo config, reuse Task 6 helper, refusal word | L3 |
| D-10 | Q-6 marker | `<!-- issue-watch:complete issue=<N> op=<id> -->` with launch op id | `<!-- sc:issue:result -->` | `<!-- sc:issue:result -->` | L2 |
| D-11 | Q-7 test file move | move prompt-pin rewrite of `test_security_invariants.py` into Task 6 (new regex written out in the test) | move 7 watcher test files (45 hits) into Task 6 | rewrite prompt-pin parts of `test_security_invariants.py` into Task 6 | L2 |
| D-12 | Q-8 `String!` | header must equal `query($owner: String!, $name: String!, $number: Int!, $after: String) {` and `count("String!") == 2` | regex `\$(\w+): String!` gives exactly {owner, name}; read DF-14 rationale first | restate, or maybe `$owner: String = "IronbellyOrg"` (unverified) | L1 |
| D-13 | Q-9 governed sessions | document in plan:23; add a guard test pinning unrecorded session allowed | document in plan:23 | document in Task 10/design note; test unbound session allowed | L1 |
| D-14 | Q-10 ordering | Task 4 depends on Task 1; cycle.py order 4, 6, 12, 18; Task 15 depends on Task 9; push sentence text given | same plus Constraints line for all shared files | same, less detail | L1 |

## 3. Contradictions

- C-1 (D-08): V3 says every `_revalidate` failure is `revalidation_failed`; V1 and V2 say the time rule runs first and reports `edited_after_approval`. Both cannot be the acceptance of plan:71 and plan:108.
- C-2 (D-05/D-06): V1 rejects any config key because the config directory is not tamper-protected (guard:764); V3 recommends a config key as the gate switch.
- C-3 (D-01): V1/V2 refuse more verbs than V3 (V3 leaves close/reopen/label/project writes as UNKNOWN in command position only).
- C-4 (D-12): V3 suggests `$owner: String = "IronbellyOrg"`; V1 rejects it because it silently reads the fork on a missing variable.
- C-5 (D-02): V1/V3 use `*issue_pipeline*complete*`, which V2 shows would refuse `pytest tests/issue_pipeline/test_complete.py` in a launched session.

## 4. Unique contributions

| Variant | Contribution | Value |
|---|---|---|
| V1 | `excluded_ids` approver exclusion (part B) | High (closes a self-approval path) but changes the owner's workflow |
| V1 | `ISSUEWRITE` also covers `label` and `project` verbs | Medium |
| V1 | marker carries the op id | Low |
| V1 | coupling test `ship_gate.PASSED` vs `_PENDING` | Medium |
| V1 | compare-and-set Status only from the four allowed Statuses | High |
| V2 | guard version bump to 2 | Medium |
| V2 | Task 3a owner observation task | Medium |
| V2 | Constraints line listing files edited by several tasks | Medium |
| V2 | pytest-safe module pattern | High |
| V3 | ranked impact table | Low |
| V3 | same-second approval and item time test case | Medium |
| V3 | rollback notes per finding | Low |

## 5. Shared assumptions (all three variants agree)

| ID | Assumption | Class | Level |
|---|---|---|---|
| A-001 | Moving `issue create/edit/comment` out of SUBMIT does not break `/sc:pr-submit` at Full Submit | STATED (grep found no `gh issue` call) but scripts such as `reply-resolve-thread.sh:131` post issue comments through `gh api`, never seen by the text-only guard | L3 |
| A-002 | The guard is text-only and cannot read scripts (guard:774-775), so a launched agent can bypass any text rule through a script | STATED as residual risk; none proposes a control inside this plan | L3 |
| A-003 | `gh api` POSTs from pr-submit are already refused by GHWRITE, so `--monitor 3` cannot reply or re-trigger from a launched agent | STATED | L3 |
| A-004 | Whether a field change or a label moves Project item timestamps is unverified GitHub behaviour | STATED | L3 |
| A-005 | The claim session at level None has no level record and is not governed | UNSTATED in V3 and V1 (inference), STATED in V2 | L3 |
| A-006 | `unchanged_since` ignores comments by the watcher's own login (predicates.py:253-255), so the completion comment never voids an approval | STATED | L3 |
| A-007 | Fail-closed outcomes (extra refusals) are acceptable cost for the owner | UNSTATED | L2 |

## 6. Convergent points (no debate needed beyond confirmation)

Q-6 marker must not equal `CLAIM_MARKER`; Q-7 move the prompt-pin test rewrite into Task 6; Q-9 document governed sessions in plan:23; Q-10 ordering and the Task 15 to Task 9 dependency; Q-5 project id and exact item selection.

## 7. Points sent to debate (L3 first)

D-01 (class scope), D-02/C-5 (pattern), D-03 (version bump), D-04 (self-approval exclusion), D-05/D-06/C-2 (ship gate mechanism), D-07 (updatedAt approach), D-08/C-1 (reason precedence), D-09 (Status compare-and-set), D-12/C-4 (`String!`), A-001, A-002 (script bypass), A-007.
