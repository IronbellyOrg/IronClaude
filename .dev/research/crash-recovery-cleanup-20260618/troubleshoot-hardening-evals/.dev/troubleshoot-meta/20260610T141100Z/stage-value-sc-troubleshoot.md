# Stage Value Score — sc:troubleshoot

Stage: `sc:troubleshoot`

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

## Verdict

**Estimated net defect-catching value: 52% value / 48% ceremony.**

`sc:troubleshoot` is not theatre: when it is forced onto the real contract surface, it catches meaningful defects and routes remediation with useful specificity. In this saga it confirmed concrete PRD `--spec` defects, produced strong analogous catches in integration-contract and spec-fidelity incidents, and the Phase-0 A2/A3 meta artifacts used troubleshoot-style contract mapping to expose the still-unresolved PRD evaluator divergence. However, for the five canonical escapes, the stage was late and inconsistent: the highest-impact PRD runtime crash, repeated parallel-gate false positives, and reflect wrong-base failure were not prevented by `sc:troubleshoot` before they escaped into follow-up PRs.

## What it caught or usefully routed

1. **Concrete PRD `--spec` defects before the `--file` crash fix.**
   - `/config/workspace/IronClaude/.dev/troubleshoot/prd-spec-review-r140-20260606174115/REPORT.md` confirmed duplicate `--spec` binding and resume-path WARN blindness with confidence 0.92, and provided targeted remediation steps.
   - This was real defect value, but it did not widen far enough to the sibling subprocess contract that later became canonical escape `E1-PRD-cloud-file-misuse`.

2. **Strong analogous contract/invariant catches outside the direct PRD escape path.**
   - `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/REPORT.md` reached Tier 2, used adversarial debate, surfaced multiple invariant violations, and routed a staged remediation plan.
   - `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/REPORT.md` diagnosed extractor/comparator asymmetry, convergence-loop limitations, and fixability gaps instead of stopping at the visible halt symptom.
   - These show the stage can produce high-value diagnosis when escalation/adversarial modes are actually applied.

3. **Meta-investigation value for current unresolved divergence.**
   - `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/contract-implementations.md` identifies that normal `superclaude prd run` uses `PrdExecutor._evaluate_gate()`, not generic `pipeline.gates.gate_passed()`, and that PR #155's advisory semantic-check change therefore likely landed partly off-path.
   - This directly maps to canonical escape `E4-PRD-generic-trailing-evaluator-divergence` and is the best example of `sc:troubleshoot`-style contract enumeration creating new actionable signal.

## Where it rubber-stamped or arrived too late

1. **Runtime-entrypoint mismatch persisted until late.**
   - `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` states runtime-entrypoint verification failed until late in the saga and that E1/E3 escaped artifacts that reasoned over source/test surfaces without executing the production headless path.
   - The direct local-file failure was eventually encoded in `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md`, not prevented by an earlier troubleshoot run.

2. **The stage caught local symptoms but did not enforce unmask-and-sweep.**
   - The PR #140 troubleshoot report diagnosed duplicate `--spec` and resume WARN issues, but did not ask the sibling contract question: every place PRD delivered local files to the Claude subprocess, and whether roadmap/tasklist/validate had an explicit no-`--file` contract.
   - Canonical E1 says roadmap/tasklist/validate already forbade `--file` while PRD still emitted it; that cross-pipeline contract sweep was missing.

3. **Hard-gate parser escapes were not prevented.**
   - Canonical E2 and E3 escaped in sequence: first final completion phase false-positive, then Task-Log placeholder heading false-positive. The stage did not force a full generated-task-file parser sweep after the first fix.
   - This is ceremony because the same semantic gate kept receiving narrow repairs rather than a generated-artifact surface inventory.

4. **Reflect wrong-base was caught by reflect, not troubleshoot.**
   - `/config/workspace/IronClaude/.dev/reflect/post-prd-local-file-20260609105644/REPORT.md` corrected the diff target from a stale committed range to the working-tree PRD diff. That is valuable meta-pipeline catching, but it belongs to `sc:reflect`, not `sc:troubleshoot`.

## Escape-by-escape scoring against the canonical set

| Escape | sc:troubleshoot contribution | Value judgement |
|---|---|---|
| E1 PRD cloud-file misuse | Earlier troubleshoot found adjacent `--spec` defects but missed the subprocess `--file` runtime contract and cross-pipeline sweep. | Low-to-medium value, late miss. |
| E2 completion-phase false-positive | No evidence it prevented the hard-gate false positive before PR #154. | Low value. |
| E3 Task-Log findings-heading sibling | No evidence it required a generated MDTM parser sweep after E2. | Low value. |
| E4 evaluator divergence | Strong current contract map identifies off-path generic evaluator vs PRD runtime evaluator. | High value, actionable. |
| E5 reflect wrong-base | Mostly caught by `sc:reflect`; troubleshoot meta-audit records the lesson. | Low direct value, useful secondary classification. |

## Percentage rationale

I score the stage slightly above break-even because the successful troubleshoot artifacts are materially useful and not merely procedural: they identify root contracts, preserve evidence, and route remediation. But the score is capped near 50% because the canonical escapes show the stage lacked a mandatory runtime-entrypoint replay and contract-consumer enumeration at exactly the seams where defects escaped.

A lower score would ignore the real catches in PR #140, PR86, spec-fidelity, and the A2 contract map. A higher score would over-credit post-hoc diagnosis while the main PRD saga still required PR #151, #154, #155, and the unresolved E4 report to expose defects that earlier review volume should have found.

## Highest-leverage improvement

Add a mandatory **runtime-entrypoint plus contract-consumer ledger** to every `sc:troubleshoot` report before it may declare success or offer remediation.

Minimum required fields:

1. **Runtime replay card**: exact command shape, environment/session assumptions, process boundary, artifact producer, artifact consumer, and whether the test/mocking path uses the same boundary.
2. **Contract-consumer ledger**: every touched CLI flag, subprocess arg, persisted field, gate criterion, semantic check, artifact filename pattern, and monitor must list all live consumers or be explicitly marked dead/off-path.
3. **Sibling sweep prompt**: after any anchor bug, require a grep/Auggie sweep for sibling implementations and generated-artifact surfaces before closing.

For this saga, that single improvement would have directly targeted E1 (`claude --file` subprocess semantics), E3 (generated Task-Log headings as sibling parser surfaces), and E4 (all `semantic_checks` consumers, including PRD's bespoke evaluator).
