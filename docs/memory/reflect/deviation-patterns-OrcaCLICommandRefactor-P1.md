# Reflect deviation patterns — OrcaCLICommandRefactor-P1

## pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956 (UC-1, brainstorm nested-analyze plan from the amended brief, 2026-11-06)
- Recurring pattern: briefs labelled F-/INV- yield 0 Pass-1 ids, so coverage_degraded parsed-sparse forces Tier 2 every time.
- Recurring plan-defect classes: (1) a brief that says "copy character for character" and "each AC must contain a check equivalent to its verifier" needs whole-text equality ACs, not substring pins; the executor's per-task reviewer reads explicit instructions (qa.md:9, :17) but that does not satisfy the brief's AC rule; (2) residual-risk lists the brief marks "copy exactly" get paraphrased when a plan is regenerated from an earlier plan; (3) an absence check that quotes the forbidden phrase trips a literal "the task no longer contains X" verifier; write it as a regex class.
- Lesson: a proposed check is itself a plan edit; the invariant probe found that the debate's agreed fix mixed package-relative and repo-relative paths. Run every proposed AC read-only from the executor's cwd before recommending it.
