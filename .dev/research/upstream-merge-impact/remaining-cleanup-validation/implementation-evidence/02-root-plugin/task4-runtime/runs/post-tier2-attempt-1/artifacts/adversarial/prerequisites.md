# Prerequisites (sc:sc-adversarial-protocol, Mode A)
- Output-path policy guard: PASS (not under .claude/{skills,agents,commands}; no plugin-component overlap; realpath-component compare).
- Inputs: 2 files (within 2-10), both exist/readable. WARN: inputs are .yaml, not .md — proceeding per type_check rule.
- artifacts_dir = caller --output itself (/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/adversarial) (caller already names the adversarial/ dir; no nested adversarial/adversarial/).
- Variants: variant-1-original.md <- reviewer-cards/reviewer-1-card.yaml (sonnet:analyzer, calibrated C=0.82); variant-2-original.md <- reviewer-cards/reviewer-2-card.yaml (haiku:qa, calibrated C=0.84). Normalized: trailing whitespace stripped.
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe; no Round 3). Convergence threshold 0.80. Focus: correctness, coverage, deviation-classification. Interactive: false. Blind: false.
- Advocate model assignment: variant's originating class (V1 sonnet, V2 haiku); judge/orchestrator/scorers/fault-finder: opus (disjoint from debaters, Khan ICML 2024).
- invocation_method: skill-direct
Prerequisites validated.
