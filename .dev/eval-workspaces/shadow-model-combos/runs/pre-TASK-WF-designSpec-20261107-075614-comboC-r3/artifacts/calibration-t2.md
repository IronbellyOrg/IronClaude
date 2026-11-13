# Tier 2 blind calibration (Wave 3C): one confidence-calibrator instance per card, in parallel

calibrator_model_class: opus (alias claude-gw-tier1a[1m]); calibrator_diversity: degraded (reviewer classes sonnet, haiku, opus leave no disjoint class)

| card | citation | coverage | classification | risk | actionability | C | citations checked / failed | self-report |
|---|---|---|---|---|---|---|---|---|
| reviewer-1 (analyzer, sonnet) | 0.92 | 0.55 | 0.65 | 0.70 | 0.80 | 0.72 | 12 / 0 | claude-gw-tier1a[1m] (Claude, Anthropic) |
| reviewer-2 (qa, haiku) | 0.90 | 0.85 | 0.70 | 0.80 | 0.65 | 0.78 | 22 / 0 | claude-gw-tier1a (Claude, Anthropic gateway tier1a alias) |
| reviewer-3 (refactorer, opus) | 0.90 | 0.75 | 0.55 | 0.80 | 0.90 | 0.78 | 22 / 0 | Claude (Anthropic), served as claude-gw-tier1a |

per-finding confidence (blind, from the calibrators' fenced yaml blocks; stored in panel/cards/):
- reviewer-1: F1 0.85, F2 0.85, F3 0.80
- reviewer-2: F1 0.85, F2 0.75, F3 0.80, F4 0.90, F5 0.80
- reviewer-3: F1 0.85, F2 0.60, F3 0.65, F4 0.70, F5 0.75, F6 0.70

anchoring_concerns (verbatim summaries): all three calibrators note severity/category labels instead of the Aligned/Refinement/Drift/Regression taxonomy; reviewer-3's calibrator could not check base-commit citations (SKILL.md, test_worker_contract.py) because it had no git, so F2 and F3 rest on unverified line content (the orchestrator re-reads them in Wave 5); reviewer-2's calibrator found plan:168 and plan:33 off by one to four lines.
All three escalation_recommendation: escalate.
