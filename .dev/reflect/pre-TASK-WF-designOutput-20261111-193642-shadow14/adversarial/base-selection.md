# Base Selection — hybrid quantitative-qualitative scoring

Panel: reflect Tier-2 shadow run 14. Mode A, depth=standard, focus: correctness, coverage, deviation-classification.
Position-bias mitigation: dual-pass scoring (Pass 1 order C1, C2, C3; Pass 2 order C3, C2, C1). Both passes produced identical rankings, so no order bias correction was needed.

## Layer 1 — Quantitative (deterministic metrics)

### Requirement coverage vs the 13 panel findings

Coverage = distinct panel diff points a card contributes a finding to (carrier or corroborator), out of 9 diff points.

| Metric | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| Findings | 5 | 4 | 4 |
| Diff points touched (of 9) | 5 (D1, D2, D3, D7, D8) | 4 (D1, D4, D5, D6) | 4 (D1, D2, D3, D4, D9) = 5 |
| Carrier of final merged finding | 4 (MF-1, MF-3, MF-8, MF-9) | 3 (MF-4, MF-6, MF-7) | 3 (MF-2, MF-5, MF-10) |
| Corroborator only | D2 | D1 | D1, D3 |
| Silent on | D4, D5, D6, D9 | D2, D3, D8, D9 | D5, D6, D7, D8 |

Card 1 and Card 3 each touch 5 points; Card 2 touches 4 but two of its points (D4, D5) are untouched by Card 1.

### Internal consistency

| Metric | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| Category-vs-claim mismatches | 1 (F4 filed `contradiction`, claim text says "drift... not a plan defect") | 0 | 1 (F3 bundles two distinct defects under `other`) |
| Self-contradictory statements | 0 | 0 | 0 |
| Consistency score | 0.80 | 1.00 | 0.75 (bundling penalty) |

### Specificity

| Metric | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| Findings with verbatim quotes | 5/5 | 1/4 | 2/4 |
| Findings with >= 2 citations | 5/5 | 3/4 | 3/4 |
| Median confidence | .65 | .70 | .625 |
| Specificity score | 0.95 | 0.70 | 0.75 |

### Dependency completeness / section coverage

Findings-card surface: persona, model class, findings block, self-report, calibration block.

| Section | Card 1 | Card 2 | Card 3 |
|---|---|---|---|
| persona / model_class / model present | yes | yes | yes (no model_observed line — minor omission) |
| findings JSON-lines well-formed | 5/5 | 4/4 | 4/4 |
| self-report present | yes | yes | yes |
| calibration: per-finding values complete | 5/5 | 4/4 | 4/4 |
| Section coverage score | 1.00 | 1.00 | 0.92 |

### Quantitative subtotals (weights: coverage .35, consistency .20, specificity .25, sections .20)

- Card 1: coverage 5/9=.556, consistency .80, specificity .95, sections 1.00 → (.556x.35)+(.80x.20)+(.95x.25)+(1.00x.20) = .195+.160+.238+.200 = **0.79**
- Card 2: coverage 4/9=.444, consistency 1.00, specificity .70, sections 1.00 → .156+.200+.175+.200 = **0.73**
- Card 3: coverage 5/9=.556, consistency .75, specificity .75, sections .92 → .195+.150+.188+.184 = **0.72**

## Layer 2 — Qualitative 30-criterion binary rubric (Claim-Evidence-Verdict)

Grouped in 6 clusters of 5 (correctness, evidence discipline, coverage breadth, classification discipline, calibration honesty, actionability). CEV = Claim / Evidence / Verdict.

### Cluster A — Correctness (5)
A1 C: quoted AC language matches claim. E: C1-F1 quotes plan:46 "not attributable to design.md" vs spec:62 "The related tests pass". V: PASS.
A2 C: vantage limits correctly identified. E: C1-F2 names missing before-state baseline. V: PASS.
A3 C: no factual overreach. E: F5's "cannot be attributed" slightly overstates; advocate conceded in Round 2. V: FAIL (one overstatement).
A4 C: severity consistent with claims. E: all MINOR; no claim implies higher. V: PASS.
A5 C: ref/AC tagging correct. E: F1 refs AC6, F3 refs 3.2-6, F4 refs 3.2-4, F5 refs AC5. V: PASS.

### Cluster B — Evidence discipline (5)
B1 C: quotes verbatim where load-bearing. E: 5/5 findings quoted. V: PASS.
B2 C: citations span both plan and spec. E: all 5 findings cite >= 1 plan + 1 spec/artifact. V: PASS.
B3 C: no unverified line-number assertions beyond citation form. E: line refs given as citations, not asserted facts. V: PASS.
B4 C: artifacts cited only where relevant. E: F3/F4 cite design.md with role labels. V: PASS.
B5 C: no invented evidence. E: none apparent; green-run detail absent (conservative). V: PASS.

### Cluster C — Coverage breadth (5)
C1 C: covers test-escape-hatch class. E: F1. V: PASS.
C2 C: covers vantage/baseline class. E: F2, F5. V: PASS.
C3 C: covers requirement-drop class. E: F3. V: PASS.
C4 C: covers shipped-vs-plan divergence class. E: F4 only, and framed as drift not contradiction — partial. V: FAIL.
C5 C: covers matrix/traceability class. E: none (silent on D5, D6). V: FAIL.

### Cluster D — Classification discipline (5)
D1 C: categories match claim type. E: F4 mismatch (contradiction vs drift text). V: FAIL.
D2 C: one defect per finding. E: yes, all 5 single-purpose. V: PASS.
D3 C: `other` used only when nothing fits. E: F2/F5 `other` — baseline-vantage findings; defensible at card time. V: PASS.
D4 C: deviation classes distinguished from plan defects. E: F4 explicitly says "not a plan defect". V: PASS.
D5 C: ref keys used consistently. E: AC6/AC1/3.2-6/3.2-4/AC5 all valid spec/plan keys. V: PASS.

### Cluster E — Calibration honesty (5)
E1 C: confidences not uniformly high. E: range .60-.80, decreasing with weaker evidence. V: PASS.
E2 C: highest confidence on best-evidenced finding. E: F1 .80 = most-quoted finding. V: PASS.
E3 C: hypothetical-based findings marked lower. E: F5 .60 lowest. V: PASS.
E4 C: card self-report matches model_class. E: self-report claude-gw-tier1b vs model claude-sonnet-5-5 — card discloses observed model honestly. V: PASS.
E5 C: no severity inflated to look impactful. E: all MINOR despite 5 findings. V: PASS.

### Cluster F — Actionability (5)
F1 C: each finding names a locatable defect. E: all cite file:line pairs. V: PASS.
F2 C: findings distinguish latent vs active. E: F1 says "run was green, so this is latent". V: PASS.
F3 C: findings suggest the checking mechanism affected. E: F2/F5 name the specific check mechanics (git diff, git status --short). V: PASS.
F4 C: no duplicate findings within card. E: F2 vs F5 distinct ACs. V: PASS.
F5 C: card-level score consistent with content. E: calibrated 0.63 matches mid-range confidences. V: PASS.

Card 1 qualitative: 26/30 PASS (4 FAIL).

### Card 2 rubric (abbreviated to FAIL items; all others PASS)
- B1 FAIL: only 1/4 findings quoted (F3, the AC3 finding, cites bare line refs where Cards 1 quotes).
- B2 FAIL: F1's plan citation bare (line only, no quote) — one-sided evidence on its flagship finding.
- C2 PASS-equivalent for its scope: covers requirement-drop (F1), traceability (F2, F4), escape hatch (F3) but is silent on the entire vantage/baseline class and shipped-divergence class — C-cluster: 2 FAILs (vantage class absent, shipped-divergence absent).
- E4 PASS: self-report honestly discloses the runtime/model-brief mismatch.
- All A, D, F clusters PASS (no category mismatch; single-purpose findings; `other` used for traceability only; confidences .65-.80).

Card 2 qualitative: 26/30 PASS (4 FAIL: B1, B2, C-cluster x2).

### Card 3 rubric (abbreviated to FAIL items; all others PASS)
- A-cluster FAIL: F1 calls it a contradiction while attributing it to the shipped file — but its claim is internally consistent (it does call the shipped text narrower than the plan); the FAIL is on the plan-defect attribution ambiguity.
- D1 FAIL: F3 bundles two defects under `other` (advocate conceded in Round 2).
- D2 FAIL: bundling again (same root cause).
- C5 PASS: covers shipped-divergence class best of all cards.
- B1 partial: 2/4 quoted (F3, F4 bare) — scored PASS at cluster level (load-bearing findings quoted).
- Section FAIL folded into quantitative layer (no model_observed line).

Card 3 qualitative: 25/30 PASS (5 FAIL: A1, D1, D2, plus 2 minor evidence/discipline).

## Layer 3 — Combined scoring

Combined = 0.5 x quantitative + 0.5 x (qualitative_pass_rate).

| Card | Quantitative | Qualitative | Combined | Rank (both passes) |
|---|---|---|---|---|
| Card 1 (analyzer/sonnet) | 0.79 | 26/30 = .867 | **0.83** | 1 |
| Card 2 (qa/haiku) | 0.73 | 26/30 = .867 | **0.80** | 2 |
| Card 3 (refactorer/opus) | 0.72 | 25/30 = .833 | **0.78** | 3 |

Dual-pass check: scoring in reverse order (C3 first) produced identical card-level scores (metrics are order-independent) and identical ranking. No tiebreaker needed: Card 1 leads by 0.03 over Card 2.

Cross-check against calibrated card scores (0.63 / 0.69 / 0.59): the panel's own blind calibration ranks Card 2 first. The hybrid ranking differs because (a) the calibrated score rewards per-finding confidence, not coverage or citation hygiene, and (b) Card 2's two unique findings (D5, D6) are high-confidence but its AC3 finding is the least-evidenced version of D1. The merge takes carriers from all three cards regardless (10 merged findings, 4/3/3 carriers), so base selection affects structure and defaults, not which findings survive.

## Selection

**Base variant: Card 1 (analyzer/sonnet, variant-1-original.md).**

Rationale: highest combined score (0.83) on the strength of the panel's best citation hygiene (5/5 quoted findings, 5/5 dual citations), the largest carrier count in the debate outcome (MF-1, MF-3, MF-8, MF-9), and complete card structure. Its weaknesses (F4 category mismatch, F5 overstatement, silence on matrix/traceability and shipped-divergence classes) are exactly the gaps Cards 2 and 3 fill, and both weaknesses were already corrected during the debate (Drift tag adopted; F5 reworded). Card 2 remains the calibration leader and contributes 3 carried findings; Card 3 contributes the shipped-artifact lens the base lacks.
