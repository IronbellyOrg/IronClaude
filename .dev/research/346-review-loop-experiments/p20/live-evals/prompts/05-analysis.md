# Prompt 05: analysis and recommendation

Inputs: `stage-c/scores/*.json`, `stage-c/key.json`, `stage-c/slots.json`, the run states (token logs), Stage A `profile/` results.

Produce `stage-c/RESULTS.md` with:
1. A per-run table (panel, slot, fixed, weighted residual, blocking residual, introduced defects) and a per-panel table (n, mean and sd of fixed and weighted residual).
2. Permutation tests (50k shuffles, two-sided) of every panel against C0 and against C1 (live7) on fixed and weighted residual; a pooled test of any shared structure (for example all panels with a t4 slot against those without).
3. Start-order check (Spearman of slot index and fixed) and the first-k versus later runs comparison; flag any panel confounded with launch time.
4. Cost: mean tokens per run split into the primary lane (Sonnet) and the parallel lane (all other models), audits excluded, per panel; fixed per million tokens.
5. Defect variety: distinct defects fixed per panel across runs, defects fixed in all runs, and the defects each panel fixes that C0 never does.
6. How well Stage B's simulated E[fixed] predicted the observed means (list both).
7. The decision under `combos.json` `stage_c.decision_rule`, stated as: adopt <panel> / keep C0, with the numbers that decide it and the caveats (single spec, single ledger, scorer family, replicates per panel).
Do not pool Stage C panels with the Haiku experiments except in a clearly labelled comparison table.
