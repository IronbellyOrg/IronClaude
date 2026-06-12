# Base Selection — Step 3 Hybrid Scoring (BLIND)

**Stage:** Step 3 — hybrid quantitative + qualitative scoring and merge-base selection.
**Inputs:** `blind/variant-A.md`, `blind/variant-B.md`, `blind/variant-C.md`, `diff-analysis.md`, `invariant-probe.md`, `round3-resolution.md`.
**Mode:** Blind to authorship. Debate is COMPLETE; established facts honored.

## Established Facts Applied (binding)

1. Variant-A §6 "rollback-replay 8/8 / 100%" and §5 "Coverage 8/8" are **FABRICATED** — the troubleshoot-protocol refactor was never built (`git diff 94d5baa0..master` on `sc-troubleshoot-protocol/SKILL.md` + `troubleshoot.md` is EMPTY); no replay ran. Hallucinated claims.
2. Variant-B "7/7 rollback-replay / 100%" is likewise **FABRICATED** (same git evidence). Hallucinated.
3. Variant-C's "implementation pending G1 / refactor unbuilt" framing is **factually correct** (round3-resolution §B 3-bucket ledger).
4. Canonical escape set = **E1–E5**. A's 8 (M1–M6+F-A/F-B) and B's 7 (M1–M7) are *instances*, not a competing canonical set. The **59% / 41% headline is a per-stage value/ceremony blended mean** (`scorecard:5`), NOT an escape-catch rate (round3 §A.3).

---

## Quantitative Scoring (50%)

Five metrics per variant. Weights: RC 0.30, IC 0.25, SR 0.15, DC 0.15, SC 0.15.

### RC — Requirement / Topic Coverage (0.30)
Expected topics: exec verdict/theatre, miss timeline+root causes, systemic causes, generalized remediation, troubleshoot refactor/forward spec, coverage stance, committed/unbuilt boundary, irreducibility/bottom-line, escape-set freeze.

| Variant | Topics present | RC |
|---|---|---|
| A | theatre scorecard, M1–M6+F-A/F-B timeline, SC-1..3, R-1..3, 3 new waves, would-have-caught, replay, §7 irreducibility. Missing: honest committed/unbuilt boundary. | **0.92** |
| B | scorecard, M1–M7 timeline, SC1..4, 4.1–4.4, refactor, matrix, replay, bottom-line. Missing: committed/unbuilt honesty. | **0.90** |
| C | exec verdict, E1–E5 freeze, RC1..5, 7 controls, full H0–H5 spec, output contract, edit scope, G1 halt. Missing (correctly): scorecard table, caught-matrix, replay. | **0.88** |

### IC — Internal Consistency = 1 − contradictions/claims (0.25) — A & B PENALIZED for fabricated-replay
| Variant | Contradiction cluster | IC |
|---|---|---|
| A | Replay §6 (8/8, 100%, round 2) + §5 "Coverage 8/8" + §7 "the replay confirms it" assert a run that git proves never happened — load-bearing fabrication penalized. | **0.85** |
| B | §6 "7/7 … 100%" + §5 all-Yes + §7 "based on the rollback replay … would have caught all" same fabrication; plus "PR #158-equivalent" treats a non-existent ref as real. | **0.84** |
| C | State-claims git-consistent (unbuilt/pending, escapes point-fixed); no replay/matrix asserted. Sole minor: M6 line-provenance not separately frozen. | **0.98** |

### SR — Specificity (0.15)
| Variant | Evidence | SR |
|---|---|---|
| A | `executor.py ~764→850`, `config.py:102`, SHAs `7601ad25→07cb149f`, `b97c9960`, named waves 4.7/4.8/6.5, output fields, cross-domain analogies. | **0.93** |
| B | SHAs, `PrdExecutor._evaluate_gate`/`gate_passed`, named statuses + auditor agents; fewer line cites; "#158-equivalent" vague. | **0.85** |
| C | base `94d5baa0`, H0–H5, output-contract fields, exact SoT file paths, paste-ready prompt; fewer line-level code cites. | **0.84** |

### DC — Dependency / Reference Completeness (0.15)
| Variant | Evidence | DC |
|---|---|---|
| A | Rich git/forensics refs; does NOT list SoT files to edit (ends at analysis). | **0.80** |
| B | "Relevant paths" list (troubleshoot.md, SKILL.md, gates.py, executor.py, process.py, config.py). | **0.88** |
| C | Exact edit-scope files + new refs/templates + `make sync-dev`/`verify-sync` + G1 prompt + base commit — most complete for the next action. | **0.95** |

### SC — Section Coverage vs Max (0.15)
Max H2 sections = C (~14). A=7, B=7.
| Variant | SC |
|---|---|
| A | 7/14 = **0.50** |
| B | 7/14 = **0.50** |
| C | 14/14 = **1.00** |

### quant_score = 0.30·RC + 0.25·IC + 0.15·SR + 0.15·DC + 0.15·SC
| Variant | Computation | **quant_score** |
|---|---|---|
| A | .276+.2125+.1395+.120+.075 | **0.823** |
| B | .270+.210+.1275+.132+.075 | **0.815** |
| C | .264+.245+.126+.1425+.150 | **0.928** |

---

## Qualitative Scoring (50%)

30-criterion additive binary rubric, 6 dimensions × 5 criteria. Claim-Evidence-Verdict: MET(1)/NOT MET(0) with citation; no citation → NOT MET.

### D1 — Completeness
| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1.1 | Executive verdict present | ✓ §1 | ✓ §1 | ✓ Exec verdict |
| 1.2 | Per-miss timeline + root causes | ✓ §2 | ✓ §2 | ✓ escape set + merged RC |
| 1.3 | Systemic causes enumerated | ✓ SC-1..3 | ✓ SC1..4 | ✓ RC1..5 |
| 1.4 | Generalized remediation set | ✓ R-1..3 | ✓ 4.1–4.4 | ✓ 7 controls |
| 1.5 | Refactor / forward spec | ✓ §5 | ✓ §5 | ✓ H0–H5 |
| **Subtotal** | | **5/5** | **5/5** | **5/5** |

### D2 — Correctness  *(established facts: A & B fabricated-replay fails 2.1 and 2.5)*
| # | Criterion | A | B | C |
|---|---|---|---|---|
| 2.1 | No hallucinated claims | ✗ §6 100% replay fabricated | ✗ §6 7/7 replay fabricated | ✓ "pending G1", no replay asserted |
| 2.2 | Escape set correctly bounded (E-set or valid instances) | ✓ M-instances of E-set | ✓ M1–M7 instances | ✓ E1–E5 canonical |
| 2.3 | M4 evaluator-divergence / #158 handled correctly | ✓ "#158 does not exist; real fix b97c9960" | ✗ "#158-equivalent" asserts non-existent ref | ✓ E4 divergence, no false #158 |
| 2.4 | Committed-vs-unbuilt boundary honest | ✗ claims refactor built+replayed | ✗ same | ✓ explicit G1 halt, unbuilt |
| 2.5 | Claims supported by evidence (no unsupported run-results) | ✗ replay 8/8 unsupported by git | ✗ 7/7 unsupported | ✓ grounded in G0/Phase-0, no run claim |
| **Subtotal** | | **2/5** | **1/5** | **5/5** |

### D3 — Structure
| # | Criterion | A | B | C |
|---|---|---|---|---|
| 3.1 | Clear section hierarchy | ✓ | ✓ | ✓ |
| 3.2 | Tabular per-stage scorecard | ✓ §1 table | ✓ §1 table | ✗ only global % (S-004) |
| 3.3 | Dense escape/timeline table | ✓ §2 8-row | ✗ prose-per-miss, no dense table | ✓ 5-row table |
| 3.4 | Remediation mapped to causes | ✓ 1:1 | ✓ | ✓ N:M |
| 3.5 | Logical flow verdict→evidence→remediation→forward | ✓ | ✓ | ✓ |
| **Subtotal** | | **5/5** | **4/5** | **4/5** |

### D4 — Clarity
| # | Criterion | A | B | C |
|---|---|---|---|---|
| 4.1 | Unambiguous verdict | ✓ | ✓ | ✓ |
| 4.2 | Defined metric basis | ✓ obligation counts | ✓ obligation counts | ✓ value/ceremony basis stated |
| 4.3 | "Theatre ≠ nothing" nuance | ✓ §1 explicit | ✓ net-value framing | ✓ "real value observed" |
| 4.4 | Readable mechanism descriptions | ✓ | ✓ | ✓ |
| 4.5 | Honest caveats stated | ✓ §7 | ✓ §7 | ✓ NOT PROVEN / halt |
| **Subtotal** | | **5/5** | **5/5** | **5/5** |

### D5 — Risk Coverage
| # | Criterion | A | B | C |
|---|---|---|---|---|
| 5.1 | Serial-unmasking / whack-a-mole risk | ✓ SC-2 | ✓ SC3 | ✓ RC3 |
| 5.2 | Cost/residual per remediation | ✓ per-R Cost | ✓ lighter | ✓ control 6 |
| 5.3 | Waiver/exemption abuse risk | ✓ audited exemption | ✓ §6 waiver abuse | ✓ H5 waiver |
| 5.4 | Fidelity-ceiling / residual honesty | ✓ §6 | ✓ §6 | ✓ NOT PROVEN blockers |
| 5.5 | Blast-radius / scope-containment risk | ✓ 6.5 commit-scope | ✗ not explicit | ✓ #6 blast-radius review |
| **Subtotal** | | **5/5** | **4/5** | **5/5** |

### D6 — Invariant & Edge Case Coverage
| # | Criterion | A | B | C |
|---|---|---|---|---|
| 6.1 | Adversarial-neighbor / substring boundary | ✓ 4.8 present⊄representation | ✓ M7 word-boundary | ✓ whole-artifact classifier (E2/E3) |
| 6.2 | Peer / sibling differential | ✓ R-3 peer-set | ✓ shared parser registry | ✓ consumer enum #2 |
| 6.3 | Producer/consumer contract-identity (E4/M6) | ✓ M6 row | ✓ Contract Identity Ledger | ✓ RC4 consumer ledger |
| 6.4 | Containment / commit-scope (F-B) | ✓ 6.5 | ✗ F-B excluded, no containment differential | ✗ severity≠commit-scope containment |
| 6.5 | Negative-witness / falsifiability | ✓ R-1 negative witness | ✓ 4.1 failure signal/impossibility waiver | ✓ negative control / NOT PROVEN |
| **Subtotal** | | **5/5** | **4/5** | **4/5** |

### qual_score = met / 30
| Variant | Comp | Corr | Struct | Clar | Risk | Inv | **met/30** | **qual_score** |
|---|---|---|---|---|---|---|---|---|
| A | 5 | 2 | 5 | 5 | 5 | 5 | 27 | **0.900** |
| B | 5 | 1 | 4 | 5 | 4 | 4 | 23 | **0.767** |
| C | 5 | 5 | 4 | 5 | 5 | 4 | 28 | **0.933** |

---

## Position-Bias Mitigation

Dual-pass evaluation: **forward (A, B, C)** and **reverse (C, B, A)**.

The decisive criteria — D2.1 (no hallucinations), D2.4 (committed/unbuilt honesty), D2.5 (evidence-supported) — are anchored to **git-verified established facts** (`git diff 94d5baa0..master` empty; round3-resolution §B). These verdicts are order-independent: the fabrication verdict on A and B holds regardless of which variant is read first. Presence-check criteria (D3.2 scorecard table, D3.3 escape table, D5.5 blast-radius, D6.4 containment) are also order-invariant.

**Criterion-variant disagreements between passes: NONE.** No flips detected. Forward and reverse passes both yield C > A > B with identical per-criterion verdicts. Final verdicts stand as scored above.

---

## Edge Case Floor Check

Per-variant Invariant & Edge Case (D6) dimension score:

| Variant | D6 score | Eligible as base? |
|---|---|---|
| A | 5/5 | ELIGIBLE |
| B | 4/5 | ELIGIBLE |
| C | 4/5 | ELIGIBLE |

No variant is <1/5 → no variant is INELIGIBLE. Not all are 0/5 → no suspension. **All three pass the floor.**

---

## Combined Scoring

variant_score = 0.50·quant + 0.50·qual

| Variant | quant | qual | **combined** | Rank |
|---|---|---|---|---|
| **C** | 0.928 | 0.933 | **0.930** | **1** |
| A | 0.823 | 0.900 | **0.862** | 2 |
| B | 0.815 | 0.767 | **0.791** | 3 |

**Margin (top two):** C − A = 0.930 − 0.862 = **0.068 (6.8%) > 5%** → no tiebreaker required. C wins outright.

*(Tiebreaker ladder, unused: L1 debate points won → L2 correctness criteria count [C=5, A=2] → L3 input order. Had a tiebreaker fired, C still wins on L2 correctness count.)*

---

## Selected Base: Variant C

**Rationale (evidence-grounded).** Variant C is the only candidate whose core state-claims are consistent with git ground truth: the troubleshoot-protocol hardening is **unbuilt and halted at G1** (`git diff 94d5baa0..master` on `SKILL.md`+`troubleshoot.md` EMPTY; round3-resolution §B), and the individual escapes E1/E2/E3/E5 are point-fixed in shipped PRs with E4's `b97c9960` committed-but-unmerged. Variants A and B both assert a **completed, validated rollback-replay** (A: 8/8 100%; B: 7/7 100%) that git proves never executed — a load-bearing fabrication that fails Correctness criteria 2.1 and 2.5 and drags both below C on internal consistency. C additionally carries the most operational forward spec (H0–H5 waves, machine-checkable output contract, named auditor surfaces, exact SoT edit scope, explicit `NOT PROVEN` blocker semantics and a G1 halt), and the most complete dependency/reference set for the actual next action. C is therefore the safest, most honest, most directly actionable container.

**Strengths to preserve (from base C):**
- Frozen canonical **E1–E5** escape set with the 4-of-5 table crosswalk discipline (E4 has no table row; sourced from `contract-implementations.md`).
- Full **H0–H5 Pipeline Hardening Closure** wave/gate spec with output-contract fields and `NOT PROVEN` blocker semantics.
- Honest **committed-vs-unbuilt boundary** and explicit **G1 halt** + paste-ready approval prompt.
- Exact source-of-truth edit scope + `make sync-dev`/`verify-sync` validation discipline.
- Severity / blast-radius and effective-input-proof controls for review/audit gates.

**Strengths to incorporate (from non-base variants), ranked:**
1. **[High] A — patch-relative & negative-witness primitives + git forensics:** the three patch-relative waves (4.7 Patched-Shadow Re-Sweep, 4.8 Fix-Patch Adversarial Linter, 6.5 Commit-Scope/Bisection Auditor) and the positive+negative witness pair (revert-and-rerun). Closes the M3 / F-A / F-B (unmasking + substring-regression + commit-scope) class that C's spec under-specifies.
2. **[High] A/B — per-stage theatre scorecard + would-have-caught matrix, RELABELED:** import the table *only* after applying round3 §D — strip every run-result token (8/8, 7/7, 100%, "round 2", ✓-caught), stamp each cell `NOT YET PROVEN (pre-build)`, and label 41%/59% as a qualitative per-stage value-blend, never an escape-catch rate.
3. **[High] B — Contract Identity Ledger:** executable owner/producer/consumer/grammar + round-trip proof + reasonable-negative example; strongest mechanism for the E4 + M6 contract-identity class. Keep **M6 and E4 as separate ledger rows** (distinct divergences, distinct files — round3 §C / INV-015).
4. **[Medium] A — explicit irreducibility analysis (§7):** enumerate what static reading cannot catch (map-vs-territory, shadowed downstream, unmasking) to sharpen C's runtime-boundary rationale.
5. **[Medium] B — "human-readable taxonomy vs executable API identity" (SC4)** as a named root-cause lens reinforcing C's RC4 consumer-ledger discipline.
