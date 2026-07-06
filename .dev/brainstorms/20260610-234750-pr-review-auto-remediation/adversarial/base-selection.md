---
contract_version: "1.0"
artifact: base-selection
topic: "PR Review Auto-Remediation Monitor (V1.0)"
step: 3-hybrid-scoring-and-base-selection
variants_scored: 3
source: ../merged-requirements.md
generated: 2026-06-11
---

# Base Selection — Hybrid Scoring (Step 3)

Variants:

- **A** = `variant-1-opus-architect.md` (architect / FSM-centric)
- **B** = `variant-2-sonnet-backend.md` (backend / run-log reliability)
- **C** = `variant-3-haiku-qa.md` (QA / test + edge + loop-guard correctness)

Weighting: `variant_score = 0.50·quant + 0.50·qual`. Quant = `RC·0.30 + IC·0.25 + SR·0.15 + DC·0.15 + SC·0.15`. Qual = `met/30` over a 6-dimension × 5-criterion additive binary rubric.

---

## Quantitative Scoring

Source requirement universe for RC: FR-1..7 (7) + NFR-1..5 (5) + AC-1..7 (7) = **19 items**.

| Metric (weight) | A | B | C | Determination basis |
|---|---|---|---|---|
| **RC** requirement_coverage (0.30) | **1.00** (19/19) | **0.947** (18/19) | **1.00** (19/19) | A relabels FR-A1..A10 covering all 7 FR + NFR-1..6 + AC-1..9. C maps FR-1..7, NFR-1..5, AC-1..7 1:1 (§4.2 matrix). B partials on source NFR-5 (NFR-9 covers absolute paths but not single-line paste-ready → 0.5) and AC-2 (level-3 behavior present, the exact "1 Medium + 1 High → 2 troubleshoot sessions" assertion absent → 0.5): 18/19. |
| **IC** internal_consistency (0.25) | **0.97** | **0.93** | **0.94** | A: single normative FSM; only X-005 round-0-vs-increment phrasing (1 minor). B: `finding_id="aug-<comment_id>-<stable_hash>"` embeds comment_id, defeating fix-dedup vs `replied_comment_ids` keyed on `source_comment_id` (X-003/INV-010); push write-ahead claim vs FM-6 detecting via post-push `push_completed` (INV-007); max-rounds=0 muddle (X-001) → 3 tensions. C: INV-1 "starts at 0" vs T-630 `round_counter==2` for 2 cycles (X-005 indexing/count drift); reply comment_id vs EC-4 file:line+hash → 2 tensions. |
| **SR** specificity_ratio (0.15) | **0.86** | **0.90** | **0.87** | B densest: full JSON schemas (envelope, snapshot), 29 event types, HTTP codes (403/429/5xx), 30→300 backoff, abs paths, commit template. C: 90 test IDs + fixture filenames + fence-post numerics. A: SoT paths, YAML contract, gate table, but "seam/capability-ceiling" prose is conceptual. |
| **DC** dependency_completeness (0.15) | **0.97** | **0.96** | **0.97** | A: FR-A/AC/VG/C-ids/R-ids all cross-resolved (seam→§2.3 table). C: §4.2 FR→T matrix + test-file layout resolve all T-ids. B: FR/NFR/AC/FM/S-states/event-types resolve; AC→FR mapping implicit. |
| **SC** section_coverage (0.15) | **0.929** (13/14) | **0.857** (12/14) | **1.00** (14/14) | H2 counts: A=13, B=12, C=14. max=14 (C). |
| **quant_score** | **0.956** | **0.924** | **0.961** | |

Quant ranking: **C (0.961) > A (0.956) > B (0.924)**.

---

## Qualitative Scoring (30-criterion CEV rubric)

### Dimension 1 — Completeness

| # | Criterion | A | B | C | Evidence (Claim–Evidence–Verdict) |
|---|---|---|---|---|---|
| 1.1 | All 7 FR covered | 1 | 1 | 1 | A FR-A1..A10; B FR-1..10; C FR-1..7 tables. MET all. |
| 1.2 | All 5 NFR covered | 1 | 1 | 1 | A NFR-1..6; B NFR-1..9; C NFR-1..5 (incl. single-line T-N41). MET all. |
| 1.3 | All 7 AC as testable | 1 | 1 | 1 | A AC-1..9; B AC-1..16; C AC-1..7 (§9 verification-method table). MET all. |
| 1.4 | Source Red-Team R1–R4 addressed | 1 | 1 | 1 | A R1..R5; B R-1..R10; C R1..R10 + P0..P3. MET all. |
| 1.5 | Build-artifact component inventory + SoT paths | 1 | 1 | **0** | A §2.2 exact source-tree; B C1..C7 abs paths. C: only `tests/submit_pr/` tree (§4.3) — no skill/command/refs/scripts/hook source inventory. NOT MET for C. |
| **Subtotal** | | **5/5** | **5/5** | **4/5** | |

### Dimension 2 — Correctness

| # | Criterion | A | B | C | CEV |
|---|---|---|---|---|---|
| 2.1 | Loop-guard counter defined, off-by-one resolved | 1 | 1 | 1 | A L8.1–8.5 (authored winning INV-016 G-push); B round_index "is not" list + off-by-one analysis + ordered predicate (authored INV-007 recovery ordering); C INV-1..7 + T-626 canonical. MET all. |
| 2.2 | Severity re-grade (hint advisory, unknown→Medium) | 1 | 1 | 1 | A FR-A4; B l.282–284 (+contradictory→Medium); C QD-6 14 mappings (authored verifying tests). MET all. |
| 2.3 | Fork-target / PR-creation discipline | 1 | 1 | 1 | A FR-A2/AC-7/VG-6; B enumerated checks + AC-15; C T-104..108. MET all. |
| 2.4 | Validation gate: lint AND format both (the gotcha) | 1 | 1 | 1 | A VG-3+VG-4; B 5-step ordered; C T-511 format-fails-lint-green. MET all. |
| 2.5 | needs_human_decision HALT even at L3 | 1 | 1 | 1 | A override predicate (sole short-circuit); B FR-6.5/FM-10; C T-430/EC-7 (authored INV-009 fresh-comment). MET all. |
| **Subtotal** | | **5/5** | **5/5** | **5/5** | |

### Dimension 3 — Structure

| # | Criterion | A | B | C | CEV |
|---|---|---|---|---|---|
| 3.1 | Logical section flow | 1 | 1 | 1 | A seam→FSM→contracts; B state→poll→guard→log→FM; C FR→matrix→edge→guard. MET all. |
| 3.2 | Central spine artifact | 1 | 1 | 1 | A seam §2.1 + FSM; B run-log substrate; C 90-test + fence-post matrix. MET all. |
| 3.3 | Component decomposition, single-responsibility | 1 | 1 | **0** | A §2.3 (C3/C3b split for pure unit test); B C1–C7. C has only test-file decomposition, no build-component cut. NOT MET C. |
| 3.4 | Data contracts / interface schemas | 1 | 1 | **0** | A DetectionContract YAML + 4 JSON contracts; B full envelope/snapshot schemas. C references fixtures but specifies no formal contract schemas. NOT MET C. |
| 3.5 | Build sequencing / dependency DAG | 1 | **0** | **0** | A §12 dependency DAG (DET gates all). B has state model but no build-order; C has §13 test-execution but no build sequence. MET A only. |
| **Subtotal** | | **5/5** | **4/5** | **2/5** | |

### Dimension 4 — Clarity

| # | Criterion | A | B | C | CEV |
|---|---|---|---|---|---|
| 4.1 | Unambiguous requirements | 1 | 1 | 1 | A prose+rationale; B declarative "must"; C tables. MET all. |
| 4.2 | Concrete examples / code / schemas | 1 | 1 | 1 | A YAML/JSON; B JSON schemas; C pytest code blocks. MET all. |
| 4.3 | State/glossary definitions clear | 1 | 1 | 1 | A 7 states; B 15 S-states + 3 D-states; C 7 INV + 3 detection states. MET all. |
| 4.4 | Consistent terminology (no drift) | 1 | 1 | **0** | A single FSM lexicon; B terms defined despite 2 dedup keys. C: INV-1 "starts at 0" vs T-630 `round_counter==2` for 2 cycles + reply comment_id vs EC-4 file:line+hash → term drift. NOT MET C. |
| 4.5 | Operator-facing output clarity | 1 | 1 | 1 | A NFR-5; B NFR-9 terminal prints; C NFR-5 + T-N40/41. MET all. |
| **Subtotal** | | **5/5** | **5/5** | **4/5** | |

### Dimension 5 — Risk Coverage

| # | Criterion | A | B | C | CEV |
|---|---|---|---|---|---|
| 5.1 | R1 detection-unknown mitigated | 1 | 1 | 1 | A locked:false hard build-gate (AC-8, strongest); B empirical capture + fixtures; C runtime HALT T-210. MET all. |
| 5.2 | R2 infinite-remediation mitigated | 1 | 1 | 1 | A L8.x; B off-by-one analysis; C fence-post matrix. MET all. |
| 5.3 | R3 session-longevity / resume mitigated | 1 | 1 | 1 | A write-ahead = checkpoint; B --resume first-class + FM-1 + AC-16 (owns run-log substrate); C documented limitation + logged session_closed. MET all. |
| 5.4 | R4 auto-push blast-radius mitigated honestly | 1 | 1 | 1 | A VG-dual + HALT + opt-in; B R-6/R-7 + no-push-on-fail + commit preconditions; C R4 P1 + audit log. MET all (INV-015: none fully closes, but all mitigate). |
| 5.5 | Additional failure-mode catalog | **0** | 1 | 1 | A has only R1–R5, no crash-window FM catalog (INV-007 hole unenumerated). B FM-1..12 (crash-after-push-before-reply etc.); C EC catalog (gh-not-installed, base-nonexistent, review-disappears). NOT MET A. |
| **Subtotal** | | **4/5** | **5/5** | **5/5** | |

### Dimension 6 — Invariant & Edge Case Coverage

| # | Criterion | A | B | C | CEV |
|---|---|---|---|---|---|
| 6.1 | Formal round-counter invariants | 1 | 1 | 1 | A L8.1–8.5; B "is not" list + termination predicate; C INV-1..7. MET all. |
| 6.2 | Fence-post / off-by-one matrix | **0** | 1 | 1 | A single AC-6 assertion (not exhaustive). B off-by-one analysis + AC-7 three-review + AC-8. C T-620..629 10-row + T-626 canonical. NOT MET A. |
| 6.3 | Edge catalog (empty/single/max/dup/malformed) | **0** | 1 | 1 | A no edge catalog. B FM-3/4/8 (unknown shape/identity/duplicate). C EC-1..16 exhaustive. NOT MET A. |
| 6.4 | Boundary values (max-rounds 0/1/5, poll<30, timeout) | **0** | 1 | 1 | A: 0 undefined (X-001), 2/5 only. B max-rounds 0/1 rules + <30s reject + cap 5. C T-627/628/624 + T-220. NOT MET A. |
| 6.5 | Interaction/race edges (review-during-fix, disappears, mixed-delta) | **0** | **0** | 1 | A none. B crash races (FM-6/7) but not review-during-fix/disappears. C EC-5 during-fix + EC-12 disappears. (INV-013 mixed-delta uncovered by all.) MET C only. |
| **Subtotal** | | **1/5** | **3/5** | **5/5** | |

### Qualitative subtotals

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 5 | 5 | 4 |
| Correctness | 5 | 5 | 5 |
| Structure | 5 | 4 | 2 |
| Clarity | 5 | 5 | 4 |
| Risk Coverage | 4 | 5 | 5 |
| Invariant & Edge | 1 | 3 | 5 |
| **met/30** | **25** | **27** | **25** |
| **qual_score** | **0.833** | **0.900** | **0.833** |

### Edge-Case Floor Check

Threshold: a variant scoring **<1/5** on Invariant & Edge Case Coverage is INELIGIBLE as base (suspend only if ALL score 0/5).

- A = **1/5** → at the floor, **eligible** (not <1).
- B = **3/5** → eligible.
- C = **5/5** → eligible (maxes the dimension the floor exists to protect).

No suspension. All three eligible; no variant is knocked out.

---

## Position-Bias Mitigation (disagreement log)

Rubric evaluated in both orders: **(A,B,C)** and **(C,B,A)**. Citation-anchored criteria are order-stable; two criteria showed pass-to-pass drift and were re-evaluated once:

| # | Criterion | Pass 1 (A,B,C) | Pass 2 (C,B,A) initial | Re-evaluation | Final |
|---|---|---|---|---|---|
| D1 | Clarity 4.4 (C terminology) | 0 | leaned 1 (C-first; tables look deliberate) | INV-1 "starts at 0" vs T-630 `round_counter==2` is a real indexing/count contradiction | **0** (original) |
| D2 | Completeness 1.5 (C component inventory) | 0 | leaned 1 (C names the skill narratively) | No source-path inventory for skill/command/refs/scripts/hook; only the test tree | **0** (original) |

**Disagreement count: 2.** Both on Variant C, both resolved to the original NOT-MET verdict. **No qual scores changed.**

---

## Combined Scoring

| Variant | quant (0.50) | qual (0.50) | **variant_score** | Rank |
|---|---|---|---|---|
| **B** (sonnet-backend) | 0.924 | 0.900 | **0.912** | **1** |
| **C** (haiku-qa) | 0.961 | 0.833 | **0.897** | **2** |
| **A** (opus-architect) | 0.956 | 0.833 | **0.8945** | 3 |

**Top-two margin:** B − C = 0.912 − 0.897 = **0.015 < 0.05 → TIEBREAKER FIRES.**

### Tiebreaker — L1 debate points won (B vs C)

From the scoring matrix:

- **B won (solo):** C-005, C-007, C-009, X-006, X-007 = **5 points**, 0 co-wins.
- **C won (solo):** C-006, X-001, X-002, X-008 = 4; **co-won:** C-002, C-004, X-005, X-008 (X-008 already counted) = 3 distinct co-wins.

| Counting rule | B | C | Winner |
|---|---|---|---|
| Co-win-inclusive (full credit) | 5 | 7 | **C** |
| Co-win-weighted (0.5) | 5.0 | 5.5 | **C** |
| Solo-only (strict) | 5 | 4 | B |

Two of three reasonable weightings — and the standard inclusive reading (a co-win is a win on that contested point) — resolve **L1 in favor of C**. B wins only under the strict solo-only count. **L1 → C.** (L2 correctness-criteria count is a 5/5 tie; L3 input-order is moot since A is not in the top-two.)

**Tiebreaker status: FIRED → resolved to C on L1 (co-win-inclusive / 0.5-weighted debate-point count).**

> **Transparency note.** B is the raw combined-score leader; the flip to C depends on counting co-wins. The selection is reinforced by the **edge-case-floor design intent**: C scores 5/5 on Invariant & Edge — the single dimension this feature exists to get right (loop-guard correctness, auto-push safety) — whereas B is 3/5 and A is at the 1/5 floor. Note also that B loses the tiebreaker to **either** runner-up (vs A: A debate points = 5 solo + 2 co = 7 > B's 5), so B is not the base under any top-two pairing.

---

## Selected Base

### BASE = Variant C (`variant-3-haiku-qa.md`)

**Rationale.** C is the quantitative leader (0.961) and wins the fired L1 tiebreaker over the combined-score leader B on debate points. Decisively, C **maximizes the two dimensions that carry the feature's reason-to-exist** — Invariant & Edge Coverage (5/5) and Risk Coverage (5/5) — which the edge-case floor explicitly privileges. The hardest part to retrofit (exhaustive fence-post loop-guard proof + 16-case edge catalog + per-requirement test mapping) is **native to C**; architecture (A) and durability schema (B) are **additive imports** rather than spine replacements. C's two genuine weaknesses — Structure (2/5) and the absent build-component inventory/data contracts — are exactly the gaps A and B fill cleanly.

### Strengths to PRESERVE (native to base C)

1. **Fence-post loop-guard matrix** T-620..T-629 with **T-626 canonical off-by-one** (`assert round_counter == 2 NOT 3`) — the safety proof the whole feature exists for.
2. **EC-1..EC-16 edge catalog** — review-arrives-during-fix (EC-5), review-disappears-transient (EC-12), multiple-PRs-same-session (EC-14), gh-not-installed (EC-15), --base-nonexistent (EC-16).
3. **INV-1..INV-7 formal round-counter invariants** + validation-failure-does-NOT-consume-a-round (QD-1/INV-6/T-520).
4. **Per-requirement testability mapping** (§4.2 FR/NFR/AC → T-id coverage matrix) + p0/loop_guard/autonomy markers.
5. **Three-state detection classifier** (D0/D1/D2) proven behaviorally, and **rubric tested independently** (QD-6, 14 category mappings).

### Strengths to INCORPORATE from non-base variants (drive the refactor plan)

**From A (architect):**

1. **Capability-ceiling FSM** — one machine, `--monitor` ordinal as 3 gates (G-arm/G-edit/G-push) + 1 `needs_human_decision` override, not 4 code paths (U-001). Gives C's tests a real architecture to assert against and collapses the level-2/3 bug surface.
2. **`detection-contract.md` as a probe-locked constant with `locked:false` HARD BUILD GATE (AC-8)** + the unknown-boundary seam + **purity CI test (AC-9) / R5 seam-leakage** (U-002, U-003). Resolves X-004 toward the strongest (mechanically-enforced) form.
3. **Component decomposition + exact SoT source-tree** (skill / refs / scripts / command / hook paths) **+ build-sequencing dependency DAG (§12)** — fills C's Structure 3.3/3.4/3.5 and Completeness 1.5 gaps directly.

**From B (backend):**

4. **Write-ahead run-log substrate** — 29-event JSONL envelope + `state.snapshot.json` cache + "JSONL is authoritative" conflict rule (U-004). The durability/observability spine C lacks.
5. **FM-1..FM-12 failure modes + `--resume` first-class flag + AC-16** (U-005, U-006) — crash-after-push-before-reply, crash-after-reply-before-resolve, corrupt-log recovery. Directly closes the HIGH **INV-007** push-write-ahead idempotency hole.
6. **Disambiguated round_index** ("is not" list + ordered termination predicate) **+ the 5 idempotency sets / dedup-key precision** — picks ONE counter timing to resolve **INV-001**, and pins the reply-vs-fix dedup keys to close **INV-009 / INV-010 / X-003**.

These six imports map 1:1 onto C's weak dimensions (Structure, durability) and onto the HIGH unaddressed invariants (INV-001, INV-007, INV-009, INV-010, INV-015, INV-016) flagged in `invariant-probe.md` — making them the backbone of the Step 4 refactor plan.
