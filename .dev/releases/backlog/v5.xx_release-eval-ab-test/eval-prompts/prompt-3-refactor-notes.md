# Prompt 3 Refactor Notes

**Date**: 2026-03-19
**Reviewer**: Claude Opus 4.6 (1M context)

## Change Applied

**Expanded the `/sc:reflect` invocation** at the end of the 4-skill chain to check both faithfulness (brainstorm-to-design drift) AND completeness (presence of all 6 required design elements per eval).

### What changed

The original reflect instruction:
```
/sc:reflect "Verify the 3 eval designs do not deviate from the brainstorm spec, and that any deviations are improvements"
```

Was replaced with a two-part verification:
1. **FAITHFULNESS** (original scope): check brainstorm-to-design drift, flag deviations that narrow measurement scope
2. **COMPLETENESS** (new scope): check that each eval design contains all required elements (pseudocode with main(), CLI invocations, artifact schemas, assertion criteria with thresholds, comparison report format)

The forward-context template was also updated to carry completeness findings to Prompt 4.

### Why this improvement was selected

The prior reflection (reflect-prompt-3.md) identified this failure mode but proposed the wrong solution: adding a new intermediate gate between `/sc:design` and `/sc:reflect`. That approach was correctly rejected for adding structural complexity and duplicating Prompt 4's responsibility.

The correct solution is simpler: expand the existing reflect instruction to cover completeness. This:
- Costs zero additional tool calls (same `/sc:reflect` invocation, just a broader instruction)
- Does not change the prompt's 4-skill chain structure
- Catches the exact failure mode Prompt 4 checks for (criteria 1: REAL EXECUTION traceability requires traceable main(); criteria 6: assertion criteria must be present)
- Prevents a costly Prompt 3 + Prompt 4 re-run cycle when designs are structurally incomplete

### Improvements considered and rejected

1. **Brainstorm output contract**: Would over-constrain the brainstorm step's divergent exploration. The design step's job is to impose structure on brainstorm output, not the brainstorm itself.

2. **Prompt 2 cross-reference during impact selection**: Already applied in a prior refactoring pass (visible at line 49 of the current file).

3. **Fail-stop for broken chain**: Natural error handling covers most failure modes. The criteria for "insufficient output" were too vague to be actionable.

### Risk

The expanded reflect instruction adds ~8 lines to the prompt. If the reflect skill interprets the completeness check as requiring it to fix gaps (rather than just flag them), it could attempt edits to eval-e2e-design.md that introduce new issues. The instruction mitigates this by framing the check as "list the gap" rather than "fix the gap."
