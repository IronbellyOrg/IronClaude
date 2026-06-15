# Phase 1 Theatre-vs-Value Scorecard

## Overall verdict

**Estimated net defect-catching value: 41% value / 59% theatre or mis-targeted ceremony.**

Phase 1 produced real evidence and some important catches, but its assurance surface was repeatedly aimed at review artifacts, local source/test inspection, and generic protocol compliance rather than the runtime and contract boundaries where the canonical escapes occurred. The strongest value came when stages forced downstream execution or identified a concrete contract mismatch. The weakest pattern was repeated confidence without mandatory replay of the exact failing entrypoint, full generated-task parser sweeps, or enumeration of every producer/consumer of a contract.

The blended score is grounded in the four Phase 1 cards:

| Stage | Estimated value | Ceremony / mistargeted assurance | Main contribution | Main miss pattern |
|---|---:|---:|---|---|
| `sc:troubleshoot` | 52% | 48% | Best direct contract mapping; exposed concrete evaluator divergence behind E4 and confirmed prior PRD/spec-fidelity defects. | Did not prevent E1, E2/E3, or E5 before follow-up; review surface often stopped at local symptom analysis. |
| `task-builder` | 35% | 65% | Durable routing, auditability, PRE/POST reflect wiring, schemas, and downstream dogfood value in #138/#142. | Generated tasks lacked mandatory runtime contract cards, parser sweeps, and semantic consumer enumeration. |
| `sc:reflect` | 40% | 60% | Caught E5/REFLECT-E01 wrong-diff trap and surfaced some emitted-output/TCS and PRD durability follow-ups. | Rubber-stamped or validated after the fact on E1, did not force E2 unmask-and-sweep, and missed E4's actual PRD evaluator path. |
| QA gates | 35% | 65% | Useful for fabricated/current-state claims, integration-chain gaps, late report/state-file defects, and small remediation fixes. | Mostly missed runtime/off-path canonical failures: headless PRD `--spec`, parser false positives, evaluator divergence, and reflect base semantics. |

## Cross-stage synthesis

### What was real value

1. **Contract-focused troubleshooting worked when it reached actual consumers.** `sc:troubleshoot` was the highest-scoring stage because it tied symptoms to concrete PRD/spec-fidelity contracts and identified the evaluator split behind E4.
2. **Downstream dogfooding created signal.** The task-builder path around #138/#142 caught issues only because generated artifacts were exercised through scanner/sprint-like surfaces, not merely reviewed as documents.
3. **Reflect had a distinct high-value niche.** `sc:reflect` caught the wrong-diff/base-selection trap in E5, a class of error that ordinary source review can easily miss.
4. **QA gates helped with evidence hygiene.** They were valuable for catching fabricated or stale current-state claims and for adversarially probing integration-chain assumptions.

### What was theatre or mis-targeted ceremony

1. **Exact runtime entrypoints were not mandatory.** E1 escaped because review did not require headless PRD `--spec` / `claude --file` replay before confidence was granted.
2. **Parser fixes were not followed by an unmask-and-sweep.** E2 and E3 show that local parser remediation did not force a full generated-MDTM corpus sweep for adjacent false positives.
3. **Contract consumers were not enumerated.** E4 persisted because generic advisory semantics and PRD-specific evaluator semantics diverged; reviews verified one path and implied coverage of the other.
4. **Diff/base semantics were treated as review plumbing, not a primary invariant.** E5 shows POST-reflect could audit the wrong surface unless base selection and uncommitted-work visibility were explicitly checked.
5. **Many gates produced audit artifacts without changing the failure probability.** Durable reports, checklists, and stage labels improved traceability, but often did not add a new observation capable of catching the canonical defects.

## Single highest-leverage stage to fix

**Fix `task-builder` first.**

Rationale: `task-builder` is upstream of the other assurance stages. It shapes the work items, required evidence, PRE/POST reflect prompts, QA expectations, and remediation checklists. If task-builder outputs require the right runtime and contract evidence, every downstream stage has a better surface to inspect. If task-builder omits that evidence, downstream `sc:reflect`, QA gates, and troubleshooting are likely to review the same incomplete proof packet and rubber-stamp the same blind spots.

Highest-leverage change:

**Require a Generated-Task Runtime Contract Card in every pipeline-mutating task-builder output.** The card should be blocking, not advisory, and should require:

- exact runtime entrypoint replay for the changed behavior;
- boundary inventory for file/stdin/subprocess/CLI invocation paths;
- producer and all-consumer enumeration for every changed contract;
- generated-artifact parser sweep when parser logic changes;
- diff/base and uncommitted-work visibility checks for reflect/review tasks;
- explicit `NOT PROVEN` blockers when any required runtime or consumer check was not executed.

Expected impact: this single change attacks all five canonical escape modes at their source. It would have forced E1 runtime replay, E2/E3 parser corpus sweeps, E4 consumer enumeration, and E5 diff/base validation before downstream stages began their reviews.

## Bottom line

Phase 1 was not empty theatre: it found meaningful issues and created useful auditability. But the dominant assurance failure was that stages often verified the shape of the review process rather than the runtime contract that could fail. The scorecard therefore lands below breakeven at **41% value / 59% theatre**, with `task-builder` as the best first fix because it can make the right evidence mandatory for every later gate.
