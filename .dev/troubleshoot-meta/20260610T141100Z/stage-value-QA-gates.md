# Stage Value Review — QA gates

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

Stage scored: **QA gates**

## Net defect-catching value estimate

**35% net value / 65% ceremony or mis-targeted assurance.**

This is not a claim that QA gates were useless. The record shows they did catch real defects, sometimes with fix authorization and in-place remediation. The problem is that their catches clustered around document completeness, report consistency, and local task-artifact quality, while the canonical escapes sat at runtime seams: production PRD subprocess behavior, duplicated gate evaluators, semantic-check consumer divergence, and generated-task reflect diff semantics. For the five canonical escapes, QA gates mostly either arrived after the escape was already discovered by another mechanism or rubber-stamped a narrower surface that did not exercise the failing path.

## Evidence of real value

1. **Research-gate QA caught fabricated/current-state claims before task building.**
   `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/qa/qa-research-gate-report.md` issued `FAIL`, found 3 failed checks, 1 critical issue, and identified false claims about existing `prd_file` prompt wiring. This is real QA value: it prevented bad baseline assumptions from flowing into generated E2E work.

2. **Adversarial QA found integration-chain gaps.**
   `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent11.md` failed the review and found the roadmap merge/diff/debate segment lacked PRD context. `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent6.md` failed on edge cases such as a dead `tdd_file` parameter, bad forced input-type handling, UTF-16 crashes, PRD-as-primary misclassification, and duplicated supplementary inputs. Those are substantive design/runtime issues, not pure ceremony.

3. **Late qualitative QA caught report and state-file defects.**
   `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/qa-qualitative-final.md` failed with 7/10 checks failed, including critical state-file bugs (`input_type: auto`, missing TDD auto-wire path) and contradictory PRD reference counts. This shows QA could still challenge a nominally completed verification package.

4. **Phase-gate QA routed small remediation.**
   `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/reviews/qa-phases-10-11-report.md` found missing report sections and follow-up sections, applied fixes, and moved from 4/6 to 6/6 checks. That is useful, but mostly artifact-hygiene value rather than escape-class prevention.

## Evidence of ceremony / rubber-stamping

1. **Task-integrity QA passed a task plan whose gate model was not truly the requested gate model.**
   `/config/workspace/IronClaude/.dev/tasks/done/TASK-E2E-20260327-prd-pipeline-e2e/qa/qa-task-validation-report.md` passed 15/15 and explicitly accepted replacing the required “spawn rf-qa after every phase” behavior with in-phase summary items. That may have been locally reasonable, but it weakened the independent QA surface into checklist summaries and did not force runtime-entrypoint validation.

2. **The canonical `--file` escape was not caught until a direct bug-fix task/post-reflect path.**
   Phase 0 classifies the headless PRD `--spec` crash as missed runtime-entrypoint verification: PRD passed local paths to Claude CLI `--file`; roadmap/tasklist/validate already forbade it; tests inspected construction without running the headless subprocess. See `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E04` and `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` runtime-entrypoint findings. QA gates did not require the one smoke/e2e that would have caught it.

3. **The `parallel_instructions` fixes show local symptom repair without parser/evaluator sweep.**
   Phase 0 records PRD-E05 and PRD-E06 as back-to-back escapes: first the final sequential completion phase false-positive, then the Task-Log heading false-positive. That sequence is strong evidence that QA around the first fix did not force an adversarial parser sweep across full generated MDTM task files.

4. **The advisory-gate fix escaped because QA did not prove the real runtime evaluator.**
   `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md` shows normal `superclaude prd run` uses `PrdExecutor._evaluate_gate()`, not generic `pipeline.gates.gate_passed()`. PR #155 made advisory behavior work in the generic evaluator and data model, but the actual PRD evaluator still ignores `SemanticCheck.advisory`. QA gates should have demanded a runtime call-graph proof and consumer sweep for every `semantic_checks` evaluator.

5. **POST-reflect was present but initially pointed at the wrong diff.**
   The canonical REFLECT-E01 escape shows off-path review existed, but the generated command audited `<start_commit>..HEAD`, which can miss uncommitted task work and include unrelated commits. `/config/workspace/IronClaude/.dev/reflect/post-prd-local-file-20260609105644/REPORT.md` only avoided this by correcting the diff target in the later direct local-file task. Presence of a QA/off-path gate was not enough; it had to audit the actual work surface.

## Escape-set mapping

| Canonical escape | QA-gate performance |
|---|---|
| E1 — PRD cloud `--file` misuse | **Missed.** QA gates did not require a headless PRD `--spec` subprocess e2e without session token or a sibling-pipeline no-`--file` contract sweep. |
| E2 — final completion phase false-positive | **Missed.** The gate fixture did not encode generated 7-phase PRD task-file semantics with sequential bookends. |
| E3 — Task-Log heading false-positive | **Missed after first repair.** No full generated-task parser sweep or adversarial heading false-positive suite was enforced after E2. |
| E4 — advisory evaluator divergence | **Missed/off-path.** QA did not enumerate all semantic-check consumers and did not prove the PRD runtime evaluator honored `advisory`. |
| E5 — reflect wrong-base diff | **Partially caught late.** The later post-reflect report corrected the diff target, but the original generated QA gate was itself the defect and could have rubber-stamped unrelated work. |

## Highest-leverage improvement

**Replace checklist-only QA gates with a mandatory “same-surface proof card” for every gate PASS.**

Before a QA gate may PASS, it must name and verify:

1. **Runtime entrypoint:** the exact production command/call chain under test, not just helper/unit construction.
2. **Contract consumers:** every implementation that consumes the changed contract (`semantic_checks`, CLI args, generated diff commands, artifact file maps, persisted state fields, etc.).
3. **Generated-artifact adversarial sample:** at least one full generated artifact containing sibling headings/placeholders/bookends, not just a minimal unit fixture.
4. **Off-path review target:** the exact diff/worktree scope reviewed, proving it includes uncommitted task work and excludes foreign commits.

For this saga, that single rule would have forced: headless PRD `--spec` smoke for E1, a 7-phase generated-task fixture for E2/E3, a `semantic_checks` consumer sweep plus PRD runtime regression for E4, and working-tree diff validation for E5.

## Bottom line

QA gates provided **meaningful but inconsistent** value. They were good at catching fabricated research claims, report contradictions, and local integration concerns. They were poor at catching the actual escape class: runtime/off-path contract mismatch. Net: **35% defect-catching value** because several real defects were caught, but most canonical escapes required later troubleshoot/reflect/direct bug-fix mechanisms rather than the QA gates that should have stopped them earlier.
