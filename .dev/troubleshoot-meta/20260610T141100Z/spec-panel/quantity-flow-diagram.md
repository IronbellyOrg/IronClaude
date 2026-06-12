# Quantity Flow Diagram — Troubleshoot Pipeline Hardening Wave Pipeline

> Fowler count-divergence artifact. `/sc:spec-panel --focus correctness`.
> Source: `troubleshoot-pipeline-hardening-spec.md` §7 (H0–H5) + §3 (E1–E5 catcher map) + `EFFICACY-REPORT-MERGED.md` §5 (predicted coverage) + §10 (waiver→status).
> Goal: trace counts through each wave, flag every point where an input count must converge/diverge, and mark CRITICAL any consumer that assumes **count conservation** (input count == output count) when the contract requires reduction-to-zero or fan-out-to-K.

---

## 1. The pipeline as a quantity flow

```
                          ┌─────────────────────────────────────────────────────────────┐
                          │  ENTER Pipeline Hardening Closure (SV-1 applicable == true)    │
                          └─────────────────────────────────────────────────────────────┘
                                                    │
   [H0] Applicability                               ▼
   ─────────────────          1 diagnosis  ──▶  classify ──▶  {applicable: bool, escapes_candidate: list}
   count in : 1 symptom                                        ⚠ DIVERGENCE-0: 1 symptom may map to N boundary
   count out: 1 verdict + a candidate-escapes LIST                classes (1→N); spec gives no N bound (H0 overflow GAP)
                                                    │
   [H1] Runtime-entrypoint                          ▼
   ─────────────────          P producers,    ──▶  prove call-chain ──▶  ≥1 negative control per forbidden interp.
   count in : P producers + T transformers          ⚠ DIVERGENCE-1: F forbidden-interpretations require F neg-controls,
              + C consumers (a tuple)                  but spec says "at least ONE" → F→1 collapse (UNDER-COUNT, CRITICAL-adj)
   count out: 1 entrypoint card (reaches boundary?)
                                                    │
   [H2] Contract-enumeration                        ▼
   ─────────────────       N candidate consumers ─▶ ENUMERATE+CLASSIFY ─▶ M classified consumers
   count in : N producers/transformers/consumers     ★ CONVERGENCE GATE: unclassified_count MUST reach 0
   count out: M classified  (REQUIRE M == N)            i.e. M == N. If M < N ⇒ FAIL. ⚠ but empty ledger N=0,M=0
                                                        vacuously passes (CRITICAL — see Scenario A)
                                                    │
   [H3] Unmask-and-sweep                            ▼
   ─────────────────       1 anchor failure   ──▶  FAN-OUT  ──▶  K sibling surfaces swept
   count in : 1 repro anchor                          ★ FAN-OUT GATE: 1 → K. K = |same-token/same-shape siblings|
   count out: K swept + per-K disposition              ⚠ DIVERGENCE-3: K is UNBOUNDED & UNVERIFIED (was K found
                                                        completely? did sampling occur?) (CRITICAL — Scenario B)
                                                    │
   [H4] Effective-input                             ▼
   ─────────────────       1 selector         ──▶  RESOLVE  ──▶  E effective-input items
   count in : 1 indirect selector (diff/glob/...)     ★ FAIL-CLOSED GATE: E must be the RIGHT E, not just E>0
   count out: E consumed items                         ⚠ DIVERGENCE-4: spec guards E==0 (empty) but NOT
                                                        "E>0 wrong-surface" (the real E5) (CRITICAL — Scenario C)
                                                    │
   [H5] Off-path                                    ▼
   ─────────────────       J required-when    ──▶  DECIDE   ──▶  decision ∈ {perf, waived, not_req}
   count in : J matched conditions (of 9)             ★ WAIVER LATCH: each waived/skipped probe ⇒ +1 `partial`
   count out: 1 decision + W waived-probe count          ⚠ DIVERGENCE-5: W `partial` probes must stay partial;
                                                        no aggregation rule for W>1; re-green not blocked (CRITICAL —
                                                        Scenario D)
                                                    │
                                                    ▼
                          ┌─────────────────────────────────────────────┐
                          │  CLOSURE: verdict = f(H1..H5 status, W, M==N) │
                          │  known_escapes_caught accumulates E-IDs       │
                          └─────────────────────────────────────────────┘
```

---

## 2. Count-divergence point inventory

| ID | Stage | Expected relation | What the spec assumes | Conservation assumed? | Severity |
|---|---|---|---|---|---|
| DIV-0 | H0 | 1 symptom → N boundary classes | N unbounded; no overflow rule | Implicitly 1→1 in skip path | MINOR |
| DIV-1 | H1 | F forbidden-interpretations → F negative controls | "at least one" collapses F→1 | Under-counts: assumes 1 control conserves coverage of F | MAJOR |
| **DIV-2** | **H2** | **N consumers in → M classified, REQUIRE M==N, unclassified==0** | empty ledger (N=0) passes vacuously; "live consumer" set is itself unverified | **YES — assumes the enumerated N *is* the true live-consumer count** | **CRITICAL** |
| **DIV-3** | **H3** | **1 anchor → K siblings, REQUIRE all K swept** | K unbounded; no "found all K" proof; sampling not forbidden | **YES — consumer of sweep assumes K_swept == K_true** | **CRITICAL** |
| **DIV-4** | **H4** | **1 selector → E items, REQUIRE E == correct surface** | guards E==0 only; E>0-wrong-surface uncaught | **YES — assumes E>0 ⇒ correct (count present ⇒ content right)** | **CRITICAL** |
| DIV-5 | H5 | J conditions → 1 decision; W waived → W `partial` latches | no aggregation for W>1; latch not variable-bound | Partially — assumes W `partial` probes don't aggregate to a hard FAIL | MAJOR (CRITICAL via re-green, see adversarial F-S1) |

---

## 3. CRITICAL dimensional-mismatch scenarios (concrete count traces)

### Scenario A — H2 empty-ledger conservation trap (DIV-2) — CRITICAL

The H2 contract is **reduction-to-zero**: `unclassified_consumer_count` must reach 0. The blocking rule is "fails if any live consumer is unclassified." A consumer that reads the ledger to compute `unclassified == 0 ⇒ PASS` **assumes the enumerated set N is the complete live set**.

Concrete count trace (this is exactly E4):
- True live consumers of `SemanticCheck.advisory`: **N_true = 2** (generic `gate_passed`, PRD `PrdExecutor._evaluate_gate`).
- Agent enumerates only the generic path: **N_enum = 1**, classifies it: **M = 1**.
- Guard computes `unclassified = N_enum − M = 1 − 1 = 0` → **PASS**.
- Reality: `N_true − M = 2 − 1 = 1` live consumer (the PRD evaluator) unclassified and divergent → **E4 escapes**.

The dimensional mismatch: the gate measures `N_enum` not `N_true`. **Count conservation between the enumerated ledger and the real call-graph is assumed, never proven.** Degenerate sub-case: `N_enum = 0, M = 0 ⇒ unclassified = 0 ⇒ PASS` on an empty ledger. Fix: H2 must require a *discoverability proof* (the "How found" column must enumerate the search that bounds N_true), and `N_enum == 0` with `applicable==true` must hard-FAIL.

### Scenario B — H3 fan-out under-count (DIV-3) — CRITICAL

The H3 contract is **fan-out 1→K**: one anchor failure must expand to all K same-token/same-shape siblings. A sweep consumer assumes `K_swept == K_true`.

Concrete count trace (this is exactly E3 following E2):
- E2 fix narrows the completion-phase matcher. Sibling surfaces in the full generated MDTM corpus carrying `### Phase N … Findings` placeholder headings: **K_true = (e.g.) 4** (one per generated phase).
- Sweep searches only the final-phase region: **K_swept = 1**.
- Guard sees K_swept ≥ 1 positive + the anchor → **PASS**.
- Reality: 3 unswept sibling headings hard-fail at runtime → **E3 escapes** (the "fix unmasks a sibling" patch-relative defect, §8 of the efficacy report).

Dimensional mismatch: `K_swept (1) ≠ K_true (4)`. The spec's "sweep dimensions searched" is a free-text field with **no requirement that the search bound K_true**. Fix: H3 must require an enumerated candidate-sibling count from a defined search (corpus-wide token grep), and assert `K_swept == K_candidate`.

### Scenario C — H4 right-count-wrong-content (DIV-4) — CRITICAL

The H4 contract is **correctness of E**, not cardinality. Spec guards `E == 0` (empty). A consumer assumes `E > 0 ⇒ correct surface`.

Concrete count trace (this is exactly E5):
- `/task` produced dirty working-tree work: expected surface = 1 dirty tree + 0 committed.
- Generated POST-reflect selector resolves to `<start_commit>..HEAD`: **E = 5 commits** (3 foreign + 2 unrelated; 0 of the dirty `/task` work).
- Guard checks `E > 0` → non-empty → **PASS**.
- Reality: E=5 but **0 overlap with the true work surface**; reviewer audits the wrong 5 → **E5 escapes**.

Dimensional mismatch: the count `E=5` is conserved/non-zero, but `|E ∩ true_surface| = 0`. **Cardinality is the wrong dimension; the spec measures presence, the contract requires intersection.** Fix: H4 must assert `|effective_input ∩ runtime_produced_surface| == |runtime_produced_surface|` AND `|effective_input ∖ runtime_produced_surface| == 0` (foreign-exclusion), not merely `E > 0`.

### Scenario D — H5 waiver-latch accumulation (DIV-5) — CRITICAL via re-green

The waiver contract is **monotonic**: W waived probes each latch to `partial`; the latch is one-way. A downstream consumer (`task-builder`/`sc:reflect`/`adversarial`) re-reads gate status and may write `success`.

Concrete count trace:
- H5 waives W = 2 mandatory runtime probes → 2 `partial` latches; closure verdict should be ≤ `advisory`.
- Downstream `sc:reflect` runs, sees 2 `partial`, "resolves" them to `success` → effective `partial` count drops 2→0.
- Production signoff now reads 0 `partial` → **green** despite 2 unproven runtime boundaries.

Dimensional mismatch: the `partial` count is **not conserved** across stages (2→0) although the invariant (§10) demands it be a one-way latch. The spec states the latch in §10 prose but binds it to no variable and provides no aggregation rule for W>1. Fix: bind SV-15 as monotonic; production signoff FAIL when `partial_count > 0`.

---

## 4. Escape→wave coverage map (E1–E5 mapped to the count gates)

| Escape | Primary count gate | Divergence exploited if gate weak |
|---|---|---|
| E1 (`--file` misuse) | H1 boundary reach + H2 sibling sweep | DIV-2 (PRD as sibling-contract outlier uncounted) |
| E2 (completion-phase FP) | H3 fan-out + H1 full-artifact replay | DIV-3 + Sentinel Collision (substring) |
| E3 (Task-Log heading FP) | H3 fan-out (1→K siblings) | **DIV-3** (the canonical K under-count) |
| E4 (evaluator divergence) | H2 reduction-to-zero | **DIV-2** (the canonical N_enum≠N_true) |
| E5 (POST-reflect wrong-diff) | H4 intersection-correctness | **DIV-4** (the canonical right-count-wrong-content) |

---

## Summary for the spec

- **CRITICAL dimensional mismatches: 3 stand-alone (DIV-2 H2, DIV-3 H3, DIV-4 H4) + 1 CRITICAL-via-re-green (DIV-5 H5).** Each is the exact mechanism of a canonical escape (E4, E3, E5 respectively).
- **The unifying defect:** three gates measure the *enumerated/present* count (N_enum, K_swept, E>0) and silently assume it equals the *true* count (N_true, K_true, correct-surface). This is count conservation assumed where the contract requires proven reduction-to-zero (H2), proven fan-out completeness (H3), or proven set-intersection (H4).
- **Spec action:** every count gate must require the *bounding search* that establishes the true count, and must hard-FAIL the degenerate zero/empty case rather than vacuously passing it.
