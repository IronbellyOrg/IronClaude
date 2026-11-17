# Quantitative layer (A.1) - slot C-04 reflect-tier2-engine-composition

Variant 1 = Proposal A (compose). Variant 2 = Proposal B (reconcile at the contract). Produced by `quant-score.py` (stdlib, deterministic); numbers in `quant-score-output.json`.

`quant_score = RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15`

| Metric | Weight | Variant 1 (A) | Variant 2 (B) | Basis |
|---|---|---|---|---|
| RC requirement coverage | 0.30 | 1.0000 (11/11) | 1.0000 (11/11) | ID regex over whole file |
| IC internal consistency | 0.25 | 0.9753 (2/81) | 0.9683 (2/63) | 1 - contradictions/claim lines |
| SR specificity ratio | 0.15 | 1.0000 (516 / 516) | 1.0000 (444 / 444) | concrete/(concrete+vague) |
| DC dependency completeness | 0.15 | 1.0000 (35/35) | 0.9787 (46/47) | resolved/total internal refs |
| SC section coverage | 0.15 | 1.0000 (9/9) | 1.0000 (9/9) | H2 count / max |
| **quant_score** | 1.00 | **0.9938** | **0.9889** | weighted sum |
| quant_score, IC from diff-analysis intra rows only (X-008, X-009) | | 0.9969 | 0.9928 | sensitivity |

## Rules

- RC source list (row C-04, verified against the row text): RE-1, RE-4, CV-8, CV-4, CV-5, INV-A, INV-B, INV-L, INV-M, INV-K, GQ-067. `06, 11, 01, 07` in the row are research file numbers, not IDs. Match = whole-token regex anywhere in the file.
- IC claim proxy (same for both): non-heading, non-metadata, non-separator lines that are table body rows, or contain a `[CODE-VERIFIED]`/`[UNVERIFIED]`/`[CODE-CONTRADICTED]` tag, a file:line or `:NNN` citation, or a number. Metadata = lines before the first H2 and `Status:`/`Position:`/`Date:`/`Code state:`/`Writer:`/`HEAD read at:`/`Slot:` lines. Contradiction = pair of statements inside one variant that cannot both hold, evidenced by diff-analysis.md (intra rows X-008, X-009; intra side of X-007 and X-006 with ledger rows V-15, V-32).
- SR: concrete = file:line citations + backtick identifiers (not pure citations) + standalone numbers (IDs such as CV-8, r06, s6.2 excluded); vague = appropriate/as needed/properly/adequate/should consider/might/various/etc./best practice(s)/industry standard. Headings, metadata, blank and table-separator/header lines excluded.
- DC scope: `section N`/`sections N and M`/`§N`, `see|in|under N.M`, parenthesised `(N.M)`, `E<N>`, `INV-<A-N>`, `M<N>` labels. Resolved = heading number, table-row first cell (E, INV, M) or bullet-leading M label defined in the same file. Excluded as external: references within 36 chars after `research/NN`, `rNN`, `sNN`, `synth-NN`, `SKILL`, `refs/`; `E1-F<N>` and E1 on lines citing research/07 (research experiment labels); M labels preceded by `r13`/`research/13` (optionally plus `row`), and M labels in a section citing `research/13 section 8` unless preceded by `measurement`.
- SC: lines matching `^## `, divided by the larger of the two counts.

## Variant 1 (A)

- Missing requirement IDs: none
- SR counts: citations 114, backtick identifiers 253, numbers 149, vague 0
- Defined internal targets: sections 0, 1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 4, 4.1, 4.2, 4.3, 5, 6, 7, 8; E E1, E2, E3, E4, E5, E6, E7, E8; M M1, M10, M13, M2, M3, M4, M5, M6, M9; INV INV-A, INV-B, INV-C, INV-D, INV-E, INV-F, INV-G, INV-H, INV-I, INV-J, INV-K, INV-L, INV-M, INV-N
- Intra-variant contradictions:
  - X-008 (diff-analysis X-008 (intra-A), V-28): line 133: "headless output directories"; line 141: "passes the lint". INV-M row says headless output directories are Preserved; M4 says a stub-lane run passes the 1.8.0 lint, which reads directories the headless lane does not create.
  - X-007(A side) (own scan; diff-analysis X-007 and V-15): line 88: "that is a skill text edit"; line 121: "the `### 9.1` block is not edited"; line 131: "SKILL.md edits stay under". Section 3.5 reconciles prose at SKILL.md :703, :839, :1317, :1481 as a text edit, while INV-K says edits stay under ### 4.3a and INV-A says the ### 9.1 block is not edited; V-15 shows those lines sit outside the allow-list and :838-839 inside 9.1.
- Unresolved internal references:
  - none

## Variant 2 (B)

- Missing requirement IDs: none
- SR counts: citations 88, backtick identifiers 248, numbers 108, vague 0
- Defined internal targets: sections 0, 1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 4, 5, 6, 7, 8; E E1, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E2, E20, E21, E22, E3, E4, E5, E6, E7, E8, E9; M M1, M2, M3, M4; INV INV-A, INV-B, INV-K, INV-L, INV-M
- Intra-variant contradictions:
  - X-009 (diff-analysis X-009 (intra-B), V-08): line 24: "CV-5 `merge_method: adversarial` means a disk-confirmed merge"; line 34: "own meaning and that EV-2". Section 1 (i) says CV-5 makes adversarial mean a disk-confirmed merge; section 2 keeps the count-derived label as engine A's own meaning.
  - X-006(B side) (own scan; diff-analysis X-006 ('also inconsistent inside B'), V-32): line 24: "GQ-067: "does the wrapper switch to engine B"; line 149: "GQ-067 / OQ-8: readers outside". Section 1 (and the section 5 trigger) uses GQ-067 as the owner question about the wrapper switching engines; section 8 defines GQ-067/OQ-8 as the readers-of-ten-keys question.
- Unresolved internal references:
  - line 105: INV `INV-F` (matched `INV-F`)
