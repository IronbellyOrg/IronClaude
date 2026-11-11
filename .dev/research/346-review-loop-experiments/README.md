# Issue #346 review-loop experiments: artifacts (snapshot 2026-11-10)

Harnesses, plans, decisions, per-run state and review reports for the document-review-loop A/B series, copied from the coordinator scratchpad.
Directories: `p11` (Stage 2 baseline runs), `p12/ab1..ab3` (k=3 union+verify, verify gate, final gate), `p13` (panel designs PN1/PN2), `p14` (owner decisions, shared Haiku baseline),
`p15` (Jev experiments E1-E5 plans, adapter code, offline results), `central` (results matrix), `exp346`.

Left out on purpose: the Jev API key file, private git clones and repo copies, per-agent `home` folders, agent transcripts, files over 1 MB, and duplicated sandbox inputs (command.md, README.md, inventory/, specs/history/).

Status of p12/ab1 (n=6 Sonnet, n=4 Haiku): see `p12/ab1/RESULTS-tables.md`, `p12/ab1/anomalies.log`, `p12/ab1/clean_vf_compare.md`.
Caveats recorded there: token counts were recomputed by prompt-text match (`tokens_by_prompt.py`); 6 verify steps received finding lists with extra review text, and clean re-runs of those steps changed the confirmed set in 4 of 6 cases, so ab1 results are provisional until the affected runs are replayed.
The ab2 token figures are not yet re-audited.
