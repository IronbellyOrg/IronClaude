# Brainstorm Summary — Reflect Detection Contract Flow

## Recommendation

Implement a shared evidence-first detection-contract setup helper, keep `/sc:pr-submit --monitor >=1` fail-closed, and make `/sc:reflect` diagnose/validate contract readiness without default write or monitor side effects.

## Key Outputs

- Seed brief: `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/seed-brief.md`
- Merged requirements: `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`
- Codebase enrichment: `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/enrichment/codebase-context.md`
- Adversarial artifacts: `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/adversarial/`
- Return contract: `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/return-contract.yaml`

## Next Recommended Step

Use the merged requirements as input to a design/tasklist pass before implementation.

Paste-ready prompt:

`/sc:design @/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`
