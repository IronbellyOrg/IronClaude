# Evidence-validator gate (Wave 5), run reflect-post-20261112T192600Z-TASK-RF-sweep-phase1

Validator: evidence-validator agent a93128dbbe19281a7 (read-only), after a mechanical script check.

- Mechanical check (orchestrator script): 122 distinct `path:line` citations in REPORT.md (after expanding the TL/SPEC/DESIGN/PROBES/CLASSIFY aliases), 0 missing files, 0 out-of-range lines; 56 quoted evidence strings, 0 not found within 3 lines of their citation.
- Semantic re-Read (agent): 95 citations (100% of D-01, D-04, D-10, D-11, all five verification logs, about half of the rest; budget policy sampled).
- citations_dropped: 1. The claim "HOW-WE-WORK file and plugin mirror are byte-identical" (and its three neighbours) was listed under "verified by running things" with no logged run. Resolution: the orchestrator ran cmp, git and grep and recorded them in `verify-logs/inspections.yaml` (INS-1 to INS-4); the report wording was changed to say so, and the item stays counted as dropped (drop, not downgrade).
- Partial / wording findings applied: (1) D-10 [INFERRED] label understated the evidence: the task's own safety gate reports a reproduction (qa/final/qa-readonly-safety-report.md:13); reworded. (2) D-14 Authorized rests on a DESIGN line that says planning only: the owner's separate execution authorization (step-7.10-style-exception.md:5-12) is now cited and the caveat that it cannot be checked against the session transcript is stated. (3) D-11 remediation named the transcript reader, which already checks is_file; removed. (4) Header placeholders replaced with real counts.
- Not applied: D-04's omission of the `ccsession orca-tabs` row (classify.py:705-707) is harmless for the Orca-row argument; D-07's Necessary split rests on SPEC :238 (SP-15), kept as stated.
- Consistency: verdict counts match the register (17: 1 regression, 11 drift of which 3 medium, 4 authorized, 1 necessary); 9 grounding gaps each with a hunk ref; every deviation block carries the seven template fields plus an optional [INFERRED] line (authorization is folded into the rationale).
- Zero-drop flag: not applicable (1 drop).
- Verdict: ship after the fixes above; all other sampled citations support their claims.
