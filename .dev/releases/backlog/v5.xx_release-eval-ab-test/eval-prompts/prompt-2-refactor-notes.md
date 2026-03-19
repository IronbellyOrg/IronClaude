# Prompt 2 Refactor Notes

## Change Applied

Differentiated adversarial debate depth between unchanged stages (1-8) and new v3.0 stages (9-12).

- Agents 1-8: remain at `--depth quick` (stages largely unchanged in v3.0)
- Agents 9-12: upgraded to `--depth standard` (spec-fidelity, wiring-verification, remediate, certify -- all new in v3.0)

The spawn instruction was updated to explain the depth-level assignment rationale inline, so the executing agent applies the correct depth per agent.

## Rationale

Stages 9-12 are the primary targets of the v3.0 Unified Audit Gating release. They represent entirely new pipeline behavior (convergence loop, static wiring analysis, conditional remediation/certification). Using `--depth quick` uniformly treated the most critical stages with the same shallow analysis as stages where the review is mostly "do upstream changes affect me?"

The asymmetry in the codebase (stages 1-8 are unchanged, stages 9-12 are new) should be reflected in asymmetric analysis depth. Deeper adversarial review on stages 9-12 will surface more eval spec gaps where they matter most, producing higher-quality input for Prompt 3's impact analysis.

## Trade-offs Accepted

- Agents 9-12 will produce longer output, increasing token cost for synthesis.
- The summary step may need to weight findings by depth level to avoid over-representing stages 9-12 simply because they have more text. This is acceptable because those stages genuinely warrant more scrutiny.

## Improvements Considered and Rejected

1. **Embedding gate acceptance criteria in agent assignments**: Rejected because line 47 already instructs agents to read gates.py directly, and hardcoding criteria creates a staleness risk if gate definitions change.

2. **Adding explicit FAIL labels to debate questions**: Rejected because forcing binary verdicts on nuanced analysis produces false precision, and conflicts with the adversarial skill's own output protocol.
