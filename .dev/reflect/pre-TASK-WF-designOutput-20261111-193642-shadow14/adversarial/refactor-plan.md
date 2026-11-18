# Refactoring Plan — merge non-base findings into Card 1 (base)

Base: variant-1-original.md (Card 1, analyzer/sonnet, combined 0.83).
Non-base contributors: Card 2 (qa/haiku, 0.80), Card 3 (refactorer/opus, 0.78).
Target: merged-output.md — a unified findings verdict (10 merged findings, MF-1..MF-10), every original finding accounted for per the 13-to-10 provenance map.

## Changes to make (all LOW merge risk — findings cards, no executable surface)

| # | Action | Source | Into | Risk | Integration point |
|---|---|---|---|---|---|
| R1 | Adopt MF-1 wording guard: "cannot fail mechanically against spec AC6 as written"; fold C2-F3's green-run detail (1167 passed, rc=0) into the latent note | C1-F1 + C2-F3 | MF-1 | LOW | Claim text only |
| R2 | Replace base F4's "not a plan defect" framing with the settled D2 form: category contradiction + deviation tag "Drift, unamended plan", conf .80; keep C3-F1's "plan was not amended" fact | C1-F4 + C3-F1 | MF-2 | LOW | Category + claim text |
| R3 | Recategorize base F2 from `other`/advisory to unpassable-check (panel's tightened A-005 rule); fold C3-F3b (AC1 half) as corroboration; record adv-1/2 advisory dissent in provenance | C1-F2 + C3-F3b | MF-3 | LOW | Category |
| R4 | Insert MF-4 (C2-F4 plan-side AC gap, narrowed to "unchecked requirements", `other`, .70) — not present in base | C2-F4 | new | LOW | New section |
| R5 | Insert MF-5 (C3-F2 shipped absence of SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off mention, missing-requirement + Drift class, .70), cross-linked to MF-4 (same spec item 7) and MF-10 (same shipped fallback collection) | C3-F2 | new | LOW | New section |
| R6 | Insert MF-6 (C2-F1 item-5 "no re-check" tail omitted from Task 1 + no matrix row, missing-requirement, .80) — not present in base | C2-F1 | new | LOW | New section |
| R7 | Insert MF-7 (C2-F2 INF-007 matrix grounded at Task-1 AC lines for Task-2 work, traceability, `other`, .65) | C2-F2 | new | LOW | New section |
| R8 | Fold C3-F4a ("worker contract gets no new field") into base F3's spec 3.2-6 conditional finding (MF-8); keep Grounding-placement gap for --format code/diagram | C1-F3 + C3-F4a | MF-8 | LOW | Claim text |
| R9 | Reword base F5 to "inadequate check, no baseline or scoped diff" (advocate-1's Round-2 concession); stays `other`, .60 | C1-F5 | MF-9 | LOW | Claim text |
| R10 | Insert MF-10 (C3-F4b extra shipped tokens graph:empty/truncated/unresolved) as CANDIDATE authorized expansion at .45 with validator drop-guard; not Drift | C3-F4b | new | LOW | New section |
| R11 | Add evidence-validator flag to ALL 10 merged findings (A-003 REJECT + probe IP-2: flag not limited to >.70) | debate | header | LOW | Header note |
| R12 | Add provenance comments per finding (carrier, corroborators, folds, dissent) | debate | each | LOW | Per-finding |

## Changes NOT being made (documented)

- N1: No severity raised above MINOR. No card produced a non-MINOR finding and the invariant probe (IP-5) noted but did not action the shipped-vs-plan confidence inversion; raising severity post-hoc would override scoring without documented justification.
- N2: No confidence inflation for MF-4/MF-5 despite convergence (probe IP-3): the Round-2 decision — same requirement, no model-independent corroboration, no double-counting — stands; recorded in unaddressed_invariants.
- N3: Card-level self-reports and calibration blocks are preserved verbatim in the merged header rather than averaged; the merged verdict carries its own merged confidences.
- N4: D3's advisory-vs-plan-defect advocate split is recorded as dissent, not resolved in favor of either side's argument; the unpassable-check category comes from the panel's own tightened A-005 rule, not from an advocate's position winning.
- N5: No re-verification of any cited file:line (A-003 stands): the merge is about the cards' findings; every finding carries the evidence-validator flag for the downstream gate.

## Execution order

R11 and R12 first (scaffold), then R1-R3 and R8-R9 (base mutations), then R4-R7, R10 (insertions), then the return contract. Single executor pass; no parallel edits needed (one output file).
