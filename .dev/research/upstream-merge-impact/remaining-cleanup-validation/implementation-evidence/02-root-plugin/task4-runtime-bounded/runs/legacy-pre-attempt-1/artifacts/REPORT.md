# sc:sc-reflect report: UC-1 pre-execution, Tier 1

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 1
confidence_calibrated: 0.9160         # artifacts/calibration.yaml:17 [C25]
citations_total: 28
citations_revalidated: 28
citations_dropped: 0
citations_inferred: 2
citation_budget_policy: full_reread
coverage_degraded: null
```

- **Audit root:** `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project` (Git root from `git -C <dir> rev-parse --show-toplevel`. Running `git -C <root> rev-list --all --count` printed `0`, so the repo has no commits.).
- **Inputs:** `spec.md` is the driving spec and `proposed.md` is the proposed tasklist. Paths below are relative to the audit root. `artifacts/coverage-matrix.yaml` is relative to the run output.
- **Run provenance (recorded by the orchestrator in audit.log, not audit evidence):** the legacy flags `--type task --analyze` map to `--mode pre`. `--tier 1` pins Tier 1, and `--no-promote` was honoured. Wave 7 does not apply to UC-1 and nothing was moved.
- **Degraded:** Serena, Auggie and Context7 MCP tools were not exposed, so native Read was used throughout. The scripted `think_about_*` checkpoints that were reached (Wave 1A and Wave 1C) were skipped and logged. The optional `tech-research` best-practice lookup is unavailable in the plugin distribution and was not run.

## Verdict

The proposed plan **covers every requirement in the spec**. Parsed coverage and union coverage are both 3/3 = 1.0 [C15, C20, C21]. There are no unmapped requirements [C21]. There are no orphan tasks: each of the three tasks references a spec ID in its heading [C03, C07, C11]. The plan is **conditionally ready**. One requirement is carried into its task with only partial fidelity, and the plan has no file targets and no verification step. The best-practice grade is **3** on the 0-5 contract scale. The Tier-1 card gave 3 [C26] and the Wave-1B matrix gave 4 [C17]. The card's lower grade is used because it reflects the fidelity gap.

## Coverage matrix

| Req | Spec | Task | Plan | Match | Fidelity |
|---|---|---|---|---|---|
| R-001 | spec.md:5 heading; spec.md:6 "MUST return the exact string Hello, Ada! for Ada." [C01, C02] | T-101 | proposed.md:3 heading; proposed.md:4 "returning the required greeting" [C03, C04] | exact | **partial** |
| R-002 | spec.md:8; spec.md:9 "MUST reject an empty name with ValueError." [C05, C06] | T-102 | proposed.md:6; proposed.md:7 "Reject an empty name using ValueError." [C07, C08] | exact | full |
| R-003 | spec.md:11; spec.md:12 "Tests MUST exercise the ordinary greeting and empty-input rejection." [C09, C10] | T-103 | proposed.md:9; proposed.md:10 "Add ordinary and empty-name test cases." [C11, C12] | exact | full |

- **Pass 1 (regex):** 3 parsed IDs [C20] and 3 tasks [C03, C07, C11].
- **Pass 2 (inference):** emitted 0 rows [C18]. The three MUST sentences (spec.md:6, 9, 12) fall inside the spans of their parsed headings, so span dedup dropped them [C19]. `coverage_degraded` is null [C24]: zero inferred rows [C18] is not more than 3 parsed rows [C20].
- **Values:** `coverage_pct` = `coverage_pct_union` = 1.0 [C15, C21]. `S_dev_density` = 0.0 [C23]. `S_scope` = 3 [C22].
- **[INFERRED]** `S_domains` = 2 (code and tests). This is judged from the task text, because the tasklist names no file paths.

No Inferred-requirements (Pass 2) section is included because Pass 2 produced zero rows.

## Findings (plan-quality gaps; no deviations because nothing has been executed)

- **F-001 (medium) — T-101 drops the exact-output acceptance criterion.** spec.md:6 fixes the string "Hello, Ada!" for Ada. proposed.md:4 says only "the required greeting". [C02, C04]
- **F-002 (medium) — T-103 states no assertions.** The tests could pass with weak checks: a non-empty result, or any exception. The spec's exact-string criterion (spec.md:6) and ValueError criterion (spec.md:9) would then go unchecked, even though the test requirement (spec.md:12) appears to be met. proposed.md:10. [C02, C06, C10, C12]
- **F-003 (low) — "Empty" is undefined.** spec.md:9 says "empty name" and spec.md:12 says "empty-input". T-102 (proposed.md:7) repeats "empty name" without saying whether whitespace-only names or None count. [C06, C10, C08]
- **F-004 (low) — [INFERRED] The general greeting format for names other than Ada is unstated.** The spec gives only the Ada example (spec.md:6), and T-101 carries no template (proposed.md:4). [C02, C04]
- **F-005 (low) — No file targets and no verification step.** The plan names no file targets, no module path, no test runner, no verification or acceptance step, and no per-task done criteria anywhere in proposed.md:3-10. [C13]
- **F-006 (low, calibration caution) — Headline numbers should not be read as readiness.** The Wave-1B matrix reports `coverage_pct: 1.0` and `best_practice_grade: 4` even though its R-001 row is partial and S_domains is inferred. See artifacts/coverage-matrix.yaml:6, 20, 27 and 29. [C14, C15, C16, C17]

## Risk register

- **RK-1 (low-medium):** the greeting is implemented in the wrong format and the tests don't catch it. Comes from F-001 and F-002.
- **RK-2 (medium likelihood, low impact):** whitespace-only or None names are handled inconsistently. Comes from F-003.
- **RK-3 (low):** files land in unexpected locations, and completion is claimed without a test run. Comes from F-005.
- **RK-4 (low-medium):** readers trust "coverage 1.0" and skip the R-001 fix. Comes from F-006.
- Neither file contains a `durable_sink:` or `@sink` annotation: a full read of spec.md:1-13 and proposed.md:1-10 found none [C27, C28], and so did a `grep -nE 'durable_sink|@sink'`. The reachability gate is UC-2 only in any case.

## Grounding Gaps

None: no report claim lacked evidence, so no `grounding-gaps.yaml` was written. Note: skipping the optional `tech-research` best-practice lookup is a recorded degradation, not a classified gap.

## Inferred-claim audit

- `citations_inferred: 2` (F-004's template claim and S_domains)
- Inferred fraction: 2 / 28 = 0.07

## Recommendations

### Recommendation R-001: State the exact greeting in T-101
- **File:** proposed.md
- **Change:** rewrite T-101 (proposed.md:4) to say `greet("Ada")` returns exactly `Hello, Ada!`. Then either state the format for other names or flag it as an open spec question.
- **Verifier:** re-Read T-101 and confirm the literal `Hello, Ada!` is present. Re-run `/sc:sc-reflect --mode pre` and confirm R-001 fidelity is full.
- **Linked finding(s):** F-001, F-004
- **Priority:** P0

### Recommendation R-002: Specify the assertions in T-103
- **File:** proposed.md
- **Change:** add two assertions to T-103 (proposed.md:10): the ordinary test checks equality with `Hello, Ada!`, and the empty-name test checks that `ValueError` is raised.
- **Verifier:** confirm T-103 names both assertions. After execution, confirm the test source contains the literal string and a ValueError assertion.
- **Linked finding(s):** F-002
- **Priority:** P1

### Recommendation R-003: Define "empty" in T-102
- **File:** proposed.md
- **Change:** add one sentence to T-102 (proposed.md:7) that defines "empty" (either `""` only, or `""` plus whitespace-only) and add the chosen boundary case to T-103.
- **Verifier:** T-102 contains the definition, and T-103 lists the boundary case.
- **Linked finding(s):** F-003
- **Priority:** P1

### Recommendation R-004: Add file targets and a verification task
- **File:** proposed.md
- **Change:** name the target paths for `greet` and its tests, and add a final task that runs the test suite with an explicit pass criterion.
- **Verifier:** every task lists a path, and a verification step with a pass/fail criterion exists.
- **Linked finding(s):** F-005
- **Priority:** P2

## Evidence gate

`sc:evidence-validator` ran 2 passes and re-read 28 of 28 citations; 0 were dropped. `zero-drop-flag: true` is logged per §11.2 (see artifacts/evidence-validation.yaml).

## Citation index

| ID | Citation | Claimed content |
|---|---|---|
| C01 | spec.md:5 | `## R-001 Greeting` heading |
| C02 | spec.md:6 | greet MUST return exact string Hello, Ada! for Ada |
| C03 | proposed.md:3 | `## T-101 R-001` |
| C04 | proposed.md:4 | "Implement greet(name) returning the required greeting." (no literal string) |
| C05 | spec.md:8 | `## R-002 Empty input` |
| C06 | spec.md:9 | MUST reject an empty name with ValueError |
| C07 | proposed.md:6 | `## T-102 R-002` |
| C08 | proposed.md:7 | "Reject an empty name using ValueError." (no definition of empty) |
| C09 | spec.md:11 | `## R-003 Evidence` |
| C10 | spec.md:12 | Tests MUST exercise ordinary greeting and empty-input rejection |
| C11 | proposed.md:9 | `## T-103 R-003` |
| C12 | proposed.md:10 | "Add ordinary and empty-name test cases." (no assertions stated) |
| C13 | proposed.md:3-10 | no file paths, module path, test runner or verification step |
| C14 | artifacts/coverage-matrix.yaml:6 | R-001 row with `fidelity: partial` |
| C15 | artifacts/coverage-matrix.yaml:20 | `coverage_pct: 1.0` |
| C16 | artifacts/coverage-matrix.yaml:27 | `S_domains: 2` marked [INFERRED] |
| C17 | artifacts/coverage-matrix.yaml:29 | `best_practice_grade: 4` |
| C18 | artifacts/coverage-matrix.yaml:15 | `inferred_rows_emitted: 0` |
| C19 | artifacts/coverage-matrix.yaml:16 | `dropped_by_span_dedup` lists spec.md:6, 9, 12 |
| C20 | artifacts/coverage-matrix.yaml:18 | `parsed_count: 3` |
| C21 | artifacts/coverage-matrix.yaml:21-23 | `coverage_pct_union: 1.0`; `unmapped_requirements: []`; `unmapped_requirements_union: []` |
| C22 | artifacts/coverage-matrix.yaml:26 | `S_scope: 3` |
| C23 | artifacts/coverage-matrix.yaml:28 | `S_dev_density: 0.0` |
| C24 | artifacts/coverage-matrix.yaml:25 | `coverage_degraded: null` |
| C25 | artifacts/calibration.yaml:17 | `C: 0.9160` |
| C26 | reflection-card.yaml:173 | `best_practice_grade: 3` |
| C27 | spec.md:1-13 | whole spec; contains no `durable_sink:` / `@sink` |
| C28 | proposed.md:1-10 | whole plan; contains no `durable_sink:` / `@sink` |
