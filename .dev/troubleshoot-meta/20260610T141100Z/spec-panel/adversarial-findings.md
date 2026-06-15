# Adversarial + Correctness Findings — Troubleshoot Pipeline Hardening

> Correctness + adversarial cluster: **Whittaker** (five attack methodologies, lead adversary), **Nygard** (failure-mode / zero-empty guards), **Fowler** (count-divergence), **Crispin** (boundary test cases).
> `/sc:spec-panel --focus correctness`. Target: `troubleshoot-pipeline-hardening-spec.md` §6–§10 + `EFFICACY-REPORT-MERGED.md` §9–§10 + Appendix A.
> Attack template: "I can break this spec by **[attack]**. The invariant at **[location]** fails when **[condition]**. Concrete attack: **[step-by-step state trace]**."
> Cross-refs: `state-variable-registry.md` (SV-*), `guard-boundary-table.md` (GAP rows), `quantity-flow-diagram.md` (DIV-*/Scenario A–D).

---

## Whittaker Attack 1 — ZERO / EMPTY

### F-N1 (CRITICAL) — H4 fail-closed has no defined default; empty state is undefined-not-failed
**Attack:** I can break this spec by submitting a closure where the H4 effective-input card was **never produced**. The invariant at **§7 H4 "fails closed when effective input is absent"** fails when **the variable `h4_status` (SV-13) has no specified initial value** — the spec never says it starts in FAIL and must be *promoted* to PASS by proof. "Fails closed" describes a runtime condition, not the variable's default.
**Concrete attack (state trace):**
1. H0 → `pipeline_hardening_applicable = true`; an indirect selector is consumed → H4 required.
2. Agent skips H4 entirely (no card). `effective_input_card_path = null`, `h4_status` unset.
3. Closure verdict reads "no FAIL recorded among H1–H5" → computes `pass`.
4. Result: an absent H4 reads as not-FAIL, not as fail-closed. The fail-closed semantics live in prose tied to "input absent," but the *gate-skipped* path is a different, unguarded state.
**Severity: CRITICAL** (it is the literal E5 fail-closed control). **Fix:** SV-13 initial = `FAIL`; verdict = `blocked` if any required wave status is unset.

### F-A1z (MAJOR) — `known_escapes_caught` empty-list semantics undefined
**Attack:** The invariant at **SV-8 / §6.2** fails when **`known_escapes_caught` is `[]` while `applicable == true`**. The spec never states the initial value or what an empty list *means* at closure.
**Concrete attack:** Agent enters mode, runs no escape-mapping, leaves the list `[]`. §11 justification cross-check ("known escapes this would have caught") is satisfied trivially by an empty set → closure passes asserting it caught nothing, which is indistinguishable from "not evaluated." **Severity: MAJOR.** **Fix:** empty `known_escapes_caught` with `applicable==true` forces H0 re-statement or `blocked`.

### F-N3 (CRITICAL, Nygard zero-empty guard) — H2 empty ledger passes vacuously
**Attack:** I can break this by submitting a **zero-row contract ledger**. The invariant at **§7 H2 rule 1 "fails if any live consumer is unclassified"** fails when **the enumerated consumer set is empty** — there is no unclassified consumer in an empty set, so the gate is vacuously satisfied.
**Concrete attack (count trace = Quantity-Flow Scenario A):** `N_enum = 0`, `M = 0`, `unclassified = N_enum − M = 0` → PASS. The real call-graph had `N_true = 2` (E4's `gate_passed` + `_evaluate_gate`). **Severity: CRITICAL.** **Fix:** `applicable==true ⇒ N_enum ≥ 1` AND a discoverability proof bounding `N_true`; empty ledger hard-FAILs.

---

## Whittaker Attack 2 — DIVERGENCE (two paths that should agree, diverge)

### F-D1 (CRITICAL) — H4 guards empty input but not non-empty-WRONG-surface (the actual E5)
**Attack:** I can break this by feeding H4 a **non-empty but wrong** effective input. The invariant at **§7 H4 "fails closed when … empty despite known changes"** fails when **the input is large and non-empty yet shares zero intersection with the runtime-produced surface**. The guard measures presence, the contract requires correctness.
**Concrete attack (state trace = Scenario C, this is E5 verbatim):**
1. `/task` produces dirty working-tree work (expected surface S_true).
2. POST-reflect selector resolves to `<start_commit>..HEAD` = 5 commits, 3 of them foreign, **0** overlapping S_true.
3. H4 card "Effective input consumed" = 5 commits (non-empty). The "empty despite known changes" guard does not fire (it's not empty).
4. `h4_status = PASS`; reviewer audits the wrong 5; E5 escapes.
**Severity: CRITICAL.** **Fix:** assert `effective_input ⊇ runtime_produced_surface` AND `effective_input ∖ runtime_produced_surface == ∅`; cardinality is the wrong dimension (Fowler).

### F-D2 (MAJOR, Whittaker divergence + Sentinel) — generic-path proof diverges from product path with no reachability oracle
**Attack:** The invariant at **§7 H2 rule 2** is correctly stated ("prove the product path reaches that implementation") but **the *evidence form* for reachability is unspecified** — an agent can write "PRD reaches `_evaluate_gate` (by inspection)" with no executed proof, re-creating E4's map-vs-territory divergence (efficacy §8 irreducibility #1).
**Concrete attack:** Reviewer asserts reachability narratively; no entrypoint replay binds the symbol to the executed path. The two paths *look* consistent on paper, diverge at runtime. **Severity: MAJOR.** **Fix:** reachability claims in H2 must cite an H1 entrypoint card that *executed* the product path, not inspection.

---

## Whittaker Attack 3 — SENTINEL COLLISION (a value that collides with a special-cased token)

### F-SC1 (CRITICAL) — substring match collides: `complete` ⊂ `incomplete`, `present` ⊂ `representation` (the E2 goldmine)
**Attack:** I can break this spec by exploiting that the **substring-vs-word-boundary requirement is only in Appendix A research-refinement, not bound into the §7 H3 blocking rule**. The invariant "sibling/off-path negative case proves same-token … content does not hard-fail" (§7 H3 min pattern step 2) fails when **the matcher uses `sig in heading_line` instead of `\b`-anchored matching**, so a sentinel substring collides with a legitimate token.
**Concrete attack (state trace — this is the real F-A/E2 regression, efficacy §6):**
1. E2 fix adds a completion-phase exemption: `if sig in heading_line` for `sig ∈ {"complete", "present"}`.
2. A real work phase heading contains the word **`incomplete`** → `"complete" in "incomplete"` = `True` → the work phase is silently exempted from the parallel-work invariant.
3. Heading **`representation`** → `"present" in "representation"` = `True` → another work phase silently exempted.
4. The exemption (meant for the final completion bookend) now masks real work phases. H3's sibling-negative requirement *exists* but does not mandate near-miss tokens, so the fixture set never includes `incomplete`/`representation`.
5. Gate passes; regression ships. (Historically caught only by review-pass `r3383060121`, actor UNPROVEN — efficacy §6 caveat.)
**Severity: CRITICAL.** **Fix:** promote Appendix A's "mandatory near-miss negatives (`incomplete`, `representation`, decorated/bolded verdicts, wrong-case, setext-like headings)" into the §7 H3 *blocking rule*, and require allow-list/word-boundary grammars for all behavior-controlling tokens.

### F-SC2 (MAJOR) — Role enum value `dead/legacy` is a sentinel that disables the H2 guard
**Attack:** The invariant at **§7 H2 rule 1** fails when **a live consumer is labeled with the valid Role sentinel `dead/legacy`** (an enumerated legal value in the H2 ledger). Classifying-as-dead is treated as classifying, so `unclassified == 0` holds even though a live path was hidden.
**Concrete attack:** Agent labels the PRD `_evaluate_gate` consumer `dead/legacy` to clear the ledger; no unreachability proof is required by the spec. E4 escapes wearing a "classified" badge. **Severity: MAJOR.** **Fix:** `dead/legacy` and `unaffected with proof` Role/Decision values must carry an executed unreachability/no-op proof or the row counts as unclassified.

---

## Whittaker Attack 4 — SEQUENCE (operations valid alone, broken in a particular order)

### F-S1 (CRITICAL) — waiver `partial` re-greened by a later stage (the anti-theatre control has no mechanical guard)
**Attack:** I can break this spec by **ordering the stages so a waived `partial` is re-converted to `success` downstream**. The invariant at **§10 / Appendix A "a waived/skipped runtime probe … may never be re-converted to `success`"** fails when **the latch is stated in prose but bound to no variable and enforced by no §7 guard**, so the temporal property "once partial, always partial" is unprotected.
**Concrete attack (state trace = Scenario D):**
1. H5 waives a mandatory runtime probe → `waiver_status = partial`, verdict ≤ `advisory`. (Valid in isolation.)
2. Later `sc:reflect` (or `task-builder`/`adversarial`) re-evaluates and writes the gate `success`. (Each stage's write is locally valid.)
3. Production signoff reads `success`, ships. The exact "theatre returning through the back door" §10 names as the thing this control must prevent.
**Severity: CRITICAL.** **Fix:** bind SV-15 as a monotonic one-way latch; any downstream WRITE `partial→success` is rejected; production signoff FAILs while `partial_count > 0`.

### F-S2 (MAJOR, Sequence) — H0 skip locks out H1–H5 irreversibly with no re-entry on later evidence
**Attack:** The invariant at **§6.1 / H0** fails when **H0 sets `applicable=false` early, then later diagnosis reveals a boundary** — the spec provides skip→enter but no **re-entry** path. Order matters: an early benign read followed by a boundary-touching fix never re-triggers H0.
**Concrete attack:** H0 runs on the initial symptom (local-looking), writes `applicable=false` + one-sentence reason. Remediation then edits a subprocess boundary. No rule forces H0 re-evaluation after the fix changes the boundary surface. **Severity: MAJOR.** **Fix:** H0 must re-run (or its decision is invalidated) whenever remediation touches a §6.1 trigger class.

### F-S3 (MAJOR, Sequence) — H3 ordering: sweep performed BEFORE candidate fix applied (patch-relative blindness)
**Attack:** The invariant at **§7 H3 / efficacy §8 "apply the candidate patch in shadow and re-sweep"** fails when **the sweep is executed against baseline (pre-fix) code**. E3-class defects exist *only after* the fix is applied; a baseline-ordered sweep cannot see them.
**Concrete attack:** Agent runs H3 sweep, then applies the E2 fix. The E3 sibling false-positive (created by the fix) is invisible to the earlier sweep. **Severity: MAJOR.** **Fix:** H3 blocking rule must require sweep order = fix-applied-in-shadow, then sweep (make the §8 patch-relative requirement a §7 gate).

---

## Whittaker Attack 5 — ACCUMULATION (state that grows without bound / is never reset / inflates)

### F-A1 (CRITICAL) — `known_escapes_caught` accepts asserted (un-earned) membership; list inflates to claim full coverage
**Attack:** I can break this spec by **appending E1..E5 to `known_escapes_caught` without producing the evidence**. The invariant at **SV-8 / §6.2** fails when **membership is assertion-based, not evidence-earned** — the spec defines the field as "Known escape IDs the evidence would have caught" but adds **no guard that ties each ID to a produced H-wave artifact**.
**Concrete attack (state trace):**
1. Agent enters mode, produces a thin H1 card only.
2. Writes `known_escapes_caught = [E1, E2, E3, E4, E5]` (full inflation), citing the §11 narrative justification (which is generic mechanism prose, not per-escape evidence).
3. §8 report renders "Known escapes this would have caught: E1–E5"; closure looks maximally strong.
4. Reality: only E1's boundary was touched. The accumulation is unbounded and unaudited.
**Severity: CRITICAL.** **Fix:** each `known_escapes_caught` entry MUST reference the specific wave artifact (H-wave + card path + the negative control) that demonstrates the catch; un-referenced IDs are stripped and the inflation is itself a FAIL.

### F-A2 (MAJOR, Accumulation/Zero-Empty hybrid) — contract ledger has no de-duplication / completeness watermark
**Attack:** The invariant at **§7 H2** fails when **the ledger accumulates duplicate or partial rows across iterations with no "is this set complete" watermark** — `unclassified == 0` is computed over whatever happens to be in the table, which grows by addition, never validated against a discovery bound.
**Concrete attack:** Across re-runs the ledger gains rows but never a "search exhausted" assertion; M==N is checked over a self-referential set. **Severity: MAJOR.** **Fix:** H2 requires a completeness watermark (the bounding search of "How found" must assert exhaustion) before M==N is meaningful. (See Quantity-Flow DIV-2.)

### F-A3 (MAJOR, Accumulation) — W>1 waived probes have no aggregation rule; partials accumulate silently
**Attack:** The invariant at **§10** fails when **many mandatory probes are waived**: each is individually "downgrade to partial," but there is **no rule that an accumulation of `partial` probes escalates the closure verdict to `blocked`**. Partials pile up without a threshold.
**Concrete attack:** 4 mandatory probes waived → 4 `partial` latches → closure still computes `advisory` (not `blocked`) because no aggregate rule exists. **Severity: MAJOR.** **Fix:** define an aggregation rule (e.g. any mandatory `partial` ⇒ verdict ≤ `advisory`; production signoff requires zero mandatory `partial`).

---

## Nygard failure-mode findings (zero-empty / fail-closed)

- **F-N1 (CRITICAL, above)** — H4 default-not-fail-closed.
- **F-N3 (CRITICAL, above)** — H2 empty-ledger vacuous pass.
- **F-N4 (MAJOR)** — No global "unevaluated wave ⇒ blocked" rule. The closure verdict computation (SV-2) reads recorded statuses; an *unrecorded* (skipped, crashed, timed-out) wave is silently treated as not-FAIL. Nygard: absence of a signal must fail closed, not open. **Fix:** verdict = `blocked` unless every applicable required wave is explicitly PASS.

## Fowler count-divergence findings

- **DIV-2 / Scenario A (CRITICAL)** — H2 measures `N_enum`, assumes `== N_true`.
- **DIV-3 / Scenario B (CRITICAL)** — H3 measures `K_swept`, assumes `== K_true`.
- **DIV-4 / Scenario C (CRITICAL)** — H4 measures `E>0`, assumes correct surface (cardinality vs intersection).
- **F-F4 (MAJOR)** — DIV-1: H1 "at least one negative control" collapses F forbidden-interpretations → 1; assumes one control conserves coverage of all F. **Fix:** one negative control *per* forbidden interpretation the contract admits.

## Crispin boundary-test findings (from guard-boundary-table.md)

- **F-C1 (MAJOR)** — H3 legitimate-empty-sibling case has no formal pass path; risks false-FAIL when an anchor genuinely has no siblings (boundary: K=0 legitimate vs K=0 unsearched are conflated).
- **F-C2 (MAJOR)** — H4 legitimate-empty (no-op task, no expected changes) is indistinguishable from "empty despite known changes" → false-FAIL boundary. **Fix:** require an explicit "expected-change count" so empty-correct and empty-wrong are separable.
- **F-C3 (MINOR)** — H0 doc/comment-only boundary-adjacent edits have no exemption; over-triggers the mode on non-behavioral changes.

---

## Findings roll-up

| ID | Methodology | Severity | One-line |
|---|---|---|---|
| F-N1 | Zero/Empty (Nygard) | **CRITICAL** | H4 has no fail-closed default; skipped wave reads as not-FAIL — invariant §7 H4 / SV-13. |
| F-N3 | Zero/Empty (Nygard) | **CRITICAL** | H2 empty ledger passes vacuously (no unclassified in empty set) — §7 H2 rule 1. |
| F-D1 | Divergence | **CRITICAL** | H4 catches empty but not non-empty-wrong-surface (the real E5) — §7 H4. |
| F-SC1 | Sentinel Collision | **CRITICAL** | substring `complete`⊂`incomplete` / `present`⊂`representation`; word-boundary rule only in Appendix A, not §7 H3. |
| F-S1 | Sequence | **CRITICAL** | waiver `partial` re-greened to `success` downstream; anti-theatre latch has no §7 guard — §10 / SV-15. |
| F-A1 | Accumulation | **CRITICAL** | `known_escapes_caught` accepts un-earned (asserted) membership; inflates to E1–E5 — SV-8 / §6.2. |
| F-D2 | Divergence | MAJOR | H2 reachability evidence form unspecified; map-vs-territory (E4) recurs. |
| F-SC2 | Sentinel Collision | MAJOR | Role `dead/legacy` sentinel disables H2 guard with no unreachability proof. |
| F-S2 | Sequence | MAJOR | H0 skip is irreversible; no re-entry when later fix touches a boundary. |
| F-S3 | Sequence | MAJOR | H3 sweep may run pre-fix (baseline), blind to patch-relative E3-class defects. |
| F-A2 | Accumulation | MAJOR | H2 ledger has no completeness watermark; M==N over a self-referential set. |
| F-A3 | Accumulation | MAJOR | W>1 waived probes have no aggregation-to-`blocked` rule. |
| F-N4 | Zero/Empty (Nygard) | MAJOR | No global "unevaluated/crashed wave ⇒ blocked" rule. |
| F-F4 | Count-divergence (Fowler) | MAJOR | H1 "≥1 negative control" under-proves F>1 forbidden interpretations. |
| F-A1z | Zero/Empty | MAJOR | `known_escapes_caught` empty-list semantics undefined. |
| F-C1 | Boundary (Crispin) | MAJOR | H3 K=0-legitimate vs K=0-unsearched conflated → false-FAIL. |
| F-C2 | Boundary (Crispin) | MAJOR | H4 empty-correct (no-op) vs empty-wrong conflated → false-FAIL. |
| F-C3 | Boundary (Crispin) | MINOR | H0 over-triggers on doc/comment-only boundary-adjacent edits. |

**Totals: 6 CRITICAL, 10 MAJOR, 1 MINOR (18 findings).** All five Whittaker methodologies represented (Zero/Empty ×3, Divergence ×2, Sentinel Collision ×2, Sequence ×3, Accumulation ×3) plus Nygard, Fowler, Crispin lenses.
