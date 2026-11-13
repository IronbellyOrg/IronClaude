# Tier 1 blind calibration (Wave 1D)

calibrator_agent: confidence-calibrator
calibrator_model_class: opus (alias ANTHROPIC_DEFAULT_OPUS_MODEL = claude-gw-tier1a[1m])
calibrator_diversity: degraded   # reviewer classes will be sonnet, haiku, opus: no disjoint class exists; opus is the highest-capability class
calibrator_self_report: claude-gw-tier1a (Claude, Anthropic)

calibration:
  citation_grounding: 0.92
  coverage_completeness: 0.78
  deviation_classification_clarity: 0.35
  risk_surface_coverage: 0.75
  recommendation_actionability: 0.88
  C: 0.74
  anchoring_concerns: Findings are graded by severity (MAJOR/MINOR) and never assigned an Aligned/Refinement/Drift/Regression category; union coverage is 0.8824 with no parsed requirement IDs, below the 0.90 floor; the import-cycle and __init__.py claims have no line citations.
  escalation_recommendation: escalate
  citations_spot_checked: 21
  citations_failed: 0
