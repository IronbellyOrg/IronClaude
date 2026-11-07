```yaml
contract_version: 1.8.0
status: partial   # the debate's invariant gate is blocked (INV-019 is open in the plan) and three debate points are unresolved
mode: pre
tier_reached: 2
confidence_calibrated: 0.73   # blind score of the Tier 1 card; the merged card was not re-scored (reviewer cards scored 0.73, 0.73, 0.75)
citations_total: 49           # distinct file:line tokens; 47 were in the draft the validator checked, 2 supporting lines (SKILL.md:199, .github/workflows/test.yml:99) were added afterwards at its request
citations_revalidated: 47     # the validator re-read all 47 (45 supported, 2 narrowed); I re-read the 2 added lines myself
citations_dropped: 0
citations_dropped_extrapolated: 0
citations_inferred: 3
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

# Pre-execution reflection: regenerated brainstorm nested-analyze plan

Spec (brief): `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/source.md`
Tasklist: `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md` (7 tasks, 4 phases)
Paths below are relative to the repository root. `plan:N` means line N of the tasklist above, `brief:N` means line N of the brief above (`source.md`), `spec:N` means line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, `SKILL.md:N` means `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `handoff-routing.md:N` means `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `analyze.md:N` means `src/superclaude/commands/analyze.md`, `brainstorm.md:N` means `src/superclaude/commands/brainstorm.md`, `WORKER-CONTRACT.md:N` means `src/superclaude/core/WORKER-CONTRACT.md`. The full merged result is `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/adversarial/merged-verdict.yaml`.

## Verdict

The plan is a faithful copy of the corrected brief and every task can be carried out as written, but it is **not ready for `/sc:implement`** until the owner amends one sentence of the brief (Part 4, the live-check sentence) and the plan copies it. The plan copies that sentence byte for byte, as the brief demands, so the defect belongs to the brief, not to the plan.

The defect: the sentence requires the nested `nested/analyze-<n>/` folder whenever any `Skill`, `Agent` or `Task` call "passes" the `--report-dir` flag text. Wave 2A hands every enrichment source to a `Task` agent (`SKILL.md:183`), and the prompt of that agent can carry the flag text while the agent then takes the auggie or `fallback_1` path. That is the same false FAIL the plan was written to remove (the live check lc10). The fix is ready in `adversarial/merged-verdict.yaml`, key `recommended_wording_fix`.

No other finding blocks execution. Four more findings are P2 (all fixed by the same brief amendment or a one-line plan edit) and eleven are P3 notes.

## How the review ran

- Tier 1 scored 0.73 in a blind re-grade, below the 0.85 floor, so the tier rule escalated to Tier 2 (rule 6). Independently, the plan carries labels the strict ID pattern does not match (`F-n`, `INV-n`), so strict parsing found 0 labelled requirements against 28 inferred ones. The sparse-labels guard (`coverage_degraded: parsed-sparse`) forbids a Tier 1 stop either way.
- Three reviewers (sonnet, the haiku slot which resolves to glm-5.3, and opus) audited the plan. Blind re-grades of their cards: 0.73, 0.73, 0.75. Every available model class was already used by a reviewer, so calibrator diversity is degraded. The model that wrote the plan could not be identified (`executor_class_resolved: false`), so the guard against a reviewer reviewing its own work is weakened.
- A three-advocate debate over 26 differing points agreed on 23 (88.5%, above the 80% bar). Unresolved: C-002 and X-003 (how severe it is that the plan's Constraints line departs from the brief's line, split 50%) and C-007 (which contract holds `domain` and `enrichment_used` when a brief passes `--report-dir`, split 50%).
- The invariant probe found one HIGH item that no card raised and the debate did not fix: INV-019 (the trigger problem above). The skill's gate treats that as blocking, so the debate status is `BLOCKED_BY_INVARIANTS` and this report's status is partial.
- Variant 1 (sonnet, analyzer) was the base card, with a combined score of 0.829 against 0.773 for Variant 3 and 0.676 for Variant 2. The gap was 0.056, so no tie-break was needed.
- The haiku-slot model was too slow for the Round 1 advocate role, so that one advocate ran on sonnet. This is recorded in `audit.log`.

## Coverage matrix

| Brief span | Plan task(s) | Result |
|---|---|---|
| Part 1: say the fallback tier writes no nested folder, in skill, command file and routing ref | Tasks 1, 2, 3 | matched |
| Part 1: pin the wording in tests | Tasks 4, 5 | matched, with one vacuous-check note (M-06) |
| Part 1: sync copies, check the plugin copy | Task 7, Constraints | matched |
| Part 1: record the corrected live-check wording | Task 6 | matched, but the brief's wording has the trigger defect (M-01) |
| Part 1: run tests and lint | Task 7 | matched, no format check (M-09) |
| Part 3: 17 corrections F-1 to F-17 with the Part 4 replacement wording | Tasks 1 to 7 | 15 copied byte for byte; F-13 and F-16 differ and the plan does not record why (M-07, M-08) |
| Part 4 and Part 5 (copy exactly; residual-risk recording; open conflict) | Tasks 1 to 3, 6; plan Constraints | matched |

Parsed requirement rows: 0 (`coverage_pct: null`). Inferred rows: 28, matched 23 (`coverage_pct_union: 0.8214`, `s_dev_density: 0.1786`). The full 28-row matrix is `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/artifacts/coverage-matrix.yaml`.

## Inferred requirements (Pass 2)

Twenty-three of the 28 inferred rows matched a task by the containment rule (threshold 0.6). The five that did not are real coverage, worded differently in the plan; a manual review of each is below. The matrix file holds the verbatim quote and line of all 28.

| INF id | Brief line | Match result |
|---|---|---|
| INF-002 | `brief:11` | unmatched by wording (ratio 0.588): covered by Tasks 4 and 5 |
| INF-007 | `brief:42` | unmatched by wording (ratio 0.562): covered by Task 6 |
| INF-009 | `brief:63` | unmatched by wording (ratio 0.588): covered by Tasks 1 to 5 |
| INF-018 | `brief:159` | unmatched by wording (ratio 0.444): covered by the shared phrases in Tasks 1 to 5 |
| INF-022 | `brief:199` | unmatched by wording (ratio 0.571): the plan narrows the line instead of copying it, see M-07 |

## Findings

Priorities are the final ones from the debate and the invariant probe. "Brief-owned" means the plan copied the brief's text faithfully, so only the owner of the brief can fix it. Each finding's file, exact change and verifier are in `adversarial/merged-verdict.yaml`.

| ID | Priority | Finding | Evidence |
|---|---|---|---|
| M-01 | P1 | [INFERRED] The required-folder trigger counts any `Skill`, `Agent` or `Task` call that passes the flag text. A `Task` prompt can carry it while the subagent takes the auggie or `fallback_1` path (the lc10 condition), so a correct run is failed and plan:133's "no known false FAIL" is false. Fix: require an actual `Skill` call that invokes `sc:analyze` and returns no tool error. Brief-owned; stays open in the plan until the owner amends brief Part 4. | `brief:217`, `plan:128`, `SKILL.md:183`, `SKILL.md:187`, `SKILL.md:195`, `SKILL.md:199`, `plan:133` |
| M-02 | P2 | Task 1's "the nested contract is listed in `artifacts`, also when the call failed" and the live-check clause "every `nested/analyze-` path listed in `artifacts` exists" conflict for a call that timed out (recorded `skipped`) or whose folder `/sc:analyze` refused. Fix by moving the existence check inside the required-folder clause; Task 1's sentence stays (the brief's rule at `brief:225` requires it). Brief-owned. | `plan:38`, `brief:229`, `plan:128`, `handoff-routing.md:77`, `analyze.md:97`, `analyze.md:98` |
| M-03 | P2 | `artifacts` lists files, but the live-check sentence tests a listed path as a directory. A literal checker would look for `<listed file>/return-contract.yaml` and fail a correct run. Same fix. Brief-owned. | `WORKER-CONTRACT.md:32`, `SKILL.md:388`, `plan:128` |
| M-04 | P2 | The residual-risk list (plan:133 to 137) must match the amended sentence: risk 2 is wrong (the spec already names the Skill and Agent tools; only the session-file encoding is inferred), risk 3 misses that one `codebase` entry exempts every call, and a fifth false-PASS risk exists. | `plan:133`, `plan:135`, `plan:136`, `spec:62`, `spec:302` |
| M-05 | P2 | No Task 6 acceptance bullet tells the amended sentence from the old one: all three pins are in both. Add the pin `invokes `sc:analyze``. | `plan:143`, `brief:109` |
| M-06 | P3 | The routing-ref half of Task 4's `git show HEAD:` check names only the short path. A wrong path makes git fail with empty output, `grep -c` prints 0, which is the required result, so the check passes without testing. | `plan:95` |
| M-07 | P3 | The Constraints line departs from the brief's mandated line ("only after they are committed to a branch the live-check worktree is built from" against "only after the owner commits and merges them") and the plan does not record the departure. The plan's wording matches `spec:282`; the brief's does not. Unresolved in the debate (split 50%); a Constraints line cannot stop `/sc:implement`, hence P3. | `plan:25`, `brief:199`, `brief:201`, `spec:282` |
| M-08 | P3 | Task 7 widens the mandated sentence to "it writes only the logs and the status snapshot", unrecorded, and "only" is untrue because `make sync-dev` rewrites the ignored `.claude/` copies. | `plan:152`, `brief:169`, `plan:21` |
| M-09 | P3 | [INFERRED] Task 7 runs no `ruff format --check` on the two edited test files, which CI runs. | `plan:152`, `plan:156`, `pyproject.toml:50-54`, `.github/workflows/test.yml:99` |
| M-10 | P3 | Task 6's anchor for the step 4 line omits its leading "4. ". Cosmetic. | `plan:125`, `spec:286` |
| M-11 | P3 | The pre-edit status snapshot has no checkable guard that it was taken before the first edit. | `plan:33`, `plan:44` |
| M-12 | P3 | Owner note (unresolved, split 50%): with `--report-dir`, `domain` and `enrichment_used` are in brainstorm's own contract, not the worker contract; the sentence is right for `--output` briefs, which the spec requires. | `brainstorm.md:153-154`, `SKILL.md:381`, `spec:142` |
| M-13 | P3 | Owner note: the companion sentence in section 2.1 states a rule for every command, and the installed `WORKER-CONTRACT.md` twin is not edited. A fix needs a seventh file. | `plan:122`, `plan:21`, `WORKER-CONTRACT.md:24` |
| M-14 | P3 | Owner note: the routing bullet says the scan is recorded "with this tier's `quality_tier`", but a timed-out source is recorded `skipped`. | `plan:54`, `handoff-routing.md:77` |
| M-15 | P3 | Review note: the coverage matrix never sampled brief Part 2, the Part 3 preamble or Part 4. The plan satisfies them. | `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/artifacts/coverage-matrix.yaml:9-36` |
| M-16 | P3 | [INFERRED] Owner note: `plan:19` names two archived P1 artifacts as read-only and `plan:21`'s six-file list excludes the archived P1 brief, so the next live-plan author has no pointer to the new 7.2 step 4 sentence; the owner should point the P2 author at the spec. | `plan:19`, `plan:21` |

Confirmations (no defect): Task 7's git-status check holds on today's tree (`...001016` is staged as `A`; only this package is untracked); Tasks 2, 3 and 6 need no "Depends on: Task 1" (the executor runs tasks in source order); pins, slices and the Part 4 copy hold (plan:38, 54, 69, 122, 128 equal brief:229, 230, 231, 221, 217); `-k brainstorm` collects 17 tests today and 19 after Task 5; the lc10 replay passes under the amended sentence.

Claims the debate withdrew: reviewer 3's P1 on the earlier-package git-status risk (the earlier package is already staged), reviewer 3's fix of rewording Task 1's tail (it breaks `brief:225`), reviewer 2's P1 on the Constraints wording (conceded to P3), and the exit-code half of reviewer 1's Task 7 note (`make` prints `Error N` on failure).

## Recommended wording fix (owner amendment of brief Part 4)

Replace the live-check sentence at `brief:217` (and so `plan:128`) with this one, then mirror the residual-risk and pin changes listed in `adversarial/merged-verdict.yaml` under `recommended_wording_fix.part_c_residual_risk_block` and `part_d_plan_lines_to_change`:

> A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).

Residual risk after the fix (false PASS only): a `/sc:analyze` run made another way, or recorded under another skill name, is missed and its missing folder passes. How the session file records the `Skill` input and a tool error is inferred from Claude Code's session format (`spec:302` says only that it records `tool_use` blocks with a `name`). The amended sentence was not put through a further debate round. If the owner declines the amendment, the plan must narrow plan:133 to "has two known false-FAIL paths" and name them, recorded as a departure; INV-019 then stays open.

## Invariant probe disposition

| Item | Severity | Disposition | Status |
|---|---|---|---|
| INV-019 | HIGH | M-01 | Addressed in the recommendation, **open in the plan** until the owner amends brief Part 4 |
| INV-005 | MEDIUM | M-05 | Addressed in the recommendation, open in the plan |
| INV-011 | MEDIUM | M-03 | Addressed in the recommendation, open in the plan |
| INV-020 | MEDIUM | M-16 owner note; fix would touch the read-only archived P1 package | Open (owner) |
| INV-021 | MEDIUM | Not changed: research enrichment from P2 stays an open conflict recorded at plan:26 | Accepted, open (owner and P2 author) |
| INV-002 | LOW | M-11 | Addressed in the recommendation |
| INV-013 | LOW | M-04 (recorded risk) | Addressed in the recommendation |
| INV-017 | LOW | Not made: `brief:225` binds only Tasks 1 to 3 | Accepted, open |

The other 14 probe rows were addressed by the debate or by the findings above.

## Dropped by validation

No citation was dropped. The validator narrowed two:

- `brainstorm.md:153` (M-12) showed only that a brief passes one of `--output` or `--report-dir`; the separate worker contract that lists the own contract is on line 154, so the citation is now `brainstorm.md:153-154`.
- `plan:19` (M-16) shows only that two named archived artifacts are read, never edited; M-16 now says that and cites `plan:21` for the six-file list.

The validator also named two supporting lines (`SKILL.md:199` for the `fallback_1` path in M-01, `.github/workflows/test.yml:99` for CI's `ruff format --check` in M-09); both were added to the findings after I re-read them. The validator could not write its own per-citation table to disk (it has read-only tools), so `artifacts/evidence-validation.md` holds its counts and narrowings only, not the row-by-row table.

## Open conflicts for the owner

- INV-019 (HIGH) and INV-005, INV-011: amend brief Part 4 as above, or accept the false-FAIL path in writing.
- INV-021: research enrichment from phase P2 also passes a nested report directory; the corrected wording covers only the codebase wave. Not resolved here.
- INV-020: the archived P1 package is read-only, so pointing the P2 author at the new spec sentence is the owner's step.
- C-002 / X-003 and C-007: split 50% in the debate; handled as P3 notes (M-07, M-12).

## Inferred-claim audit

- `citations_inferred: 3` (M-01, M-09, M-16 are tagged INFERRED).
- The M-01 failure path (a `Task` prompt carrying the flag while the subagent uses auggie or `fallback_1`) has no session record behind it; it follows from the prescribed delegation at `SKILL.md:183` and the lc10 condition.

## Recommendations

### Recommendation R-001: Owner amends brief Part 4, then the plan mirrors it

- **File:** `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/source.md` (lines 217, 109, 239 to 241), then `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md` (lines 128, 135, 136, a new bullet after 137, line 143)
- **Change:** apply M-01, M-02, M-03, M-04 and M-05 from `adversarial/merged-verdict.yaml`. This review does not edit the plan; regenerate it from the amended brief, or edit it by hand.
- **Verifier:** the quoted sentence at `plan:128` equals the one at `brief:217` byte for byte and contains `a `Skill` tool call (not a `Task` or `Agent` call` and `invokes `sc:analyze``, and no longer contains `a `Skill`, `Agent` or `Task` tool call`.
- **Linked deviation(s):** none (proactive; findings M-01 to M-05)
- **Priority:** P1

### Recommendation R-002: Apply the small plan edits in the same pass (optional)

- **File:** `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md` (lines 25, 44, 95, 125, 152, 156)
- **Change:** M-06 to M-11, each with its exact text in the merged verdict. All are P3.
- **Verifier:** each finding's verifier in `merged-verdict.yaml` passes.
- **Linked deviation(s):** none (proactive)
- **Priority:** P3

### Recommendation R-003: Record the research-wave conflict for the P2 author

- **File:** n/a (owner decision; later `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`)
- **Change:** record whether INV-021 is an accepted risk or must be fixed in the P2 live plan, and point the P2 author at spec 7.2 step 4 (INV-020).
- **Verifier:** the decision is written where the P2 live-plan author will read it.
- **Linked deviation(s):** none (INV-020, INV-021)
- **Priority:** P2
