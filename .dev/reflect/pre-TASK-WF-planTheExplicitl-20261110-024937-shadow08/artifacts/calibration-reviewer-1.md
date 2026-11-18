# Calibration reviewer-1 (haiku)
per_finding:
- F1: 0.40
- F2: 0.30
- F3: 0.60
- F4: 0.25
card_score: 0.39
notes:
- F1: Citations resolve. Core CLAUDE.md:55-61 and the test at 33-36 already hold the clarified wording. The plan is archived under done/, so this may be post-implementation state, not the state the pre-plan review saw. The "vacuous before-state" claim cannot be fully grounded, though the plan does define no baseline.
- F2: The claim that the test only checks absence of the old phrase is partly wrong. Test line 34 requires the worker-ban text in both distributable copies. The remaining valid gap is that root CLAUDE.md is untested, which F3 already covers.
- F3: Verified. Root CLAUDE.md:312 "An Orca coordinator is person-opened"; core CLAUDE.md:58 "A supervised orchestrator's coordinator is person-opened". Test COPIES (line 8) omits root CLAUDE.md. Real but minor; root may intentionally differ.
- F4: "Where necessary" mirrors the spec's own "only as necessary" (source.md:1). The hedge is faithful to the spec; an implementer would not act on it as a defect.
