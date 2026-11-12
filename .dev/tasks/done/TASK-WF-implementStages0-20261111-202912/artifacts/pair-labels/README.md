# AI labels for the 50-pair cluster check

The Stage 0 exit names a hand-labelled 50-pair check (`merged-requirements.md`, "Staged migration", row 0). These labels were made by AI labelers at the owner's request after the owner's own labels did not exist. They are **not human labels** and do not replace the owner's check; the original blank sheet `../cluster-pairs-50.csv` is unchanged (Task 5's deliverable).

## Method

- Three independent labelers (opus, sonnet, opus with a deliberately skeptical stance) each labelled all 50 pairs from a full-context brief: `labeler-A.csv`, `labeler-B.csv`, `labeler-C.csv` (columns `pair_id,label,confidence,reason`). They did not see each other's files and were told not to use `cluster_v2`'s verdict.
- Every label is yes or no, so every pair has a majority of at least two: 46 pairs are unanimous and 4 are 2-to-1 (P01, P09, P12, P38). There is no "remaining unique labels" list to fill.
- The 2-to-1 pairs went to a minority-side advocate (`debate-split-pairs.md`) who opened the full cards and reviewed documents.
- Final labels: `../cluster-pairs-50.ai-labelled.csv` (`human_same_defect` filled; the column name is the scorer's).

## Rule for bundled findings (ruling)

A pair is the same defect when one edit to the reviewed document fully resolves at least one separable part of each finding; other parts about other flaws do not change the label. Applied: P01 yes, P09 yes, P38 yes (the debate found the same Task 37 ordering flaw in both findings, `CONSOLIDATED-PLAN.md:481`; the majority had no), P12 no (different commands and spec rows; one finding states no defect). P38 is the only label that differs from the plain majority. The owner may overrule the rule; the whole-finding rule would give P01 and P09 as no.

## Result

`uv run python scripts/reflect_cluster_pairs.py score --sheet cluster-pairs-50.ai-labelled.csv`: TP 21, FP 4, FN 1, TN 24; precision 0.84 (21/25), recall 0.9545 (21/22). The sample holds 25 pairs `cluster_v2` merged and 25 it kept apart by design, so these are sample figures, not rates.

## Caveats

- AI labelers and `cluster_v2` come from the same family of models and were all written in this work; agreement is weaker evidence than human agreement.
- Labelers differed in depth: labeler B judged from the sheet text and did not open the cards.
- The sheet's claim text is cut at about 300 characters, and several findings state no defect (P12 A, P34 A, P36 A, P50 B), which makes those pairs easy "no" answers.
- The `cluster_v2` weaknesses the sample cannot see or only touched are listed in `../cluster-v2-known-weaknesses.md` (bundled findings, `P1` taken from "D-P1", `spec:N` resolved against the short brief).

## "Additional labels to get it up to 50" (owner request, 2026-11-12)

The sheet already holds 50 labelled pairs (50 of 50 rows, no shortfall), so no label is missing to reach 50 and none was added. The request is read as: make the 50 count as far as an AI can, and say what an AI cannot do. An AI cannot supply the owner's hand labels that the Stage 0 exit item names; those stay PENDING.

The one sampling gap worth filling is the pair type the sampler skips by design: two findings from the same reviewer (the P09 bundled-finding case). A supplementary set of such pairs, labelled the same way and scored separately from the 50 so the sample figures stay comparable, is NOT BUILT. It needs a sampler option for same-reviewer pairs; it is the next labelling step if the owner wants W-1 measured.
