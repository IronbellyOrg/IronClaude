# Debate — Defender Position (Spec Steelman)

Role: DEFENDER. Steelman the G1 design spec `troubleshoot-pipeline-hardening-spec.md` as written.
Grain: G1 prose/protocol design spec for a reusable mode added to `sc:troubleshoot`. The §6.2 output contract is consumed by a markdown skill + refs, not a typed API. Some critiques demand appropriate formal-API rigor; some over-formalize a prose protocol.

Spec: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md` (382 lines)
Critiques: `spec-critiques-G1.md` (C1-C3, M1-M11, m1-m2)

Stances: REJECT (invalid) | CONCEDE (valid) | NARROW (valid but proposed fix over-scoped → minimal fix).

---

## C1 — Verdict enum contradiction (§6.2 ↔ §8)

**Stance: CONCEDE.**

Evidence: §6.2 line 105 defines `pipeline_hardening_verdict` ∈ `pass, blocked, advisory, not_applicable` (4 values). §8 line 311 defines the report line `- Closure verdict: pass | blocked | advisory` (3 values, omits `not_applicable`). Two normative statements of the same logical field disagree on cardinality. The critique's line cites are exact.

Real defect: When `pipeline_hardening_applicable=false` the §6.2 contract requires `not_applicable`, but the §8 report template literally cannot render that value, so a skip case cannot be expressed in the human-facing REPORT.md. One enumeration must be made normative (or §8 scoped as the applicable=true sub-enum with an explicit mapping). Genuine and cheap to fix.

---

## C2 — Vacuous pass is reachable

**Stance: CONCEDE.**

Evidence: I scanned the spec for any clause binding `pipeline_hardening_verdict=pass` to gate results. §6.2 (lines 104-111) defines the fields but states no constraint relating verdict to card paths or `known_escapes_caught`. The §7 blocking rules (lines 153-156, 184-187, 220-223, 255-258) define when an *individual gate* fails, but nothing aggregates those gate states into the top-level `verdict`. §8 line 314 says the protocol "must use `NOT PROVEN` blockers when any required proof is absent" but never states NOT PROVEN ⇒ ¬pass. §10 acceptance criteria are about implementation structure, not a verdict invariant.

Real defect: with no aggregation invariant, a result with every `*_card_path=null`, `known_escapes_caught=[]`, and `verdict=pass` is contract-legal — directly contradicting §4 (lines 52-59) and the §8 NOT PROVEN intent. For a spec whose whole purpose is "do not accept adjacent proof," a reachable vacuous pass is the most serious defect in the set. The proposed verdict invariant is the correct fix.

---

## C3 — advisory verdict reintroduces E4

**Stance: NARROW.**

Evidence: `advisory` appears only at line 105 (§6.2 enum) and line 311 (§8 closure line) — both as a bare enum member, never with halt/non-halt semantics, never with a selection criterion vs `blocked`. The E4 mechanism (§3 line 45) is exactly "a shared `advisory` contract whose real runtime consumer treated advisory as fatal." An undefined `advisory` verdict in this protocol's own output is therefore a latent re-instantiation of E4. Core finding valid.

Why NARROW: the critique offers (a) remove advisory, or (b) define it as a total function over gate states + pin its consumer contract + add a parity test. Option (b) is over-scoped for a G1 design spec. `advisory` is **not used anywhere as a gate-level state**: every gate H1-H4 is binary PASS/FAIL (lines 153, 184, 220, 255) or N/A, and the §8 per-gate lines are `PASS | FAIL | N/A` (lines 304-307). No gate ever emits "advisory"; it exists solely as a top-level verdict with no producer logic feeding it and no consumer told how to read it. A value nothing can justify emitting and nothing knows how to consume is dead enum surface. Removal (verdict ∈ `pass | blocked | not_applicable`) kills the E4-reintroduction risk at zero cost and avoids specifying a parity test a G1 design spec shouldn't yet own.

Minimal fix: remove `advisory` from lines 105 and 311. (Defining-and-pinning is the heavier path, justified only if a real non-halting "surface-for-review" state is demonstrated — the spec never demonstrates one.)

---

## M1 — Trigger set (9) ≠ H0 mandatory set (5)

**Stance: CONCEDE.**

Evidence: §6.1 lists 9 trigger conditions (lines 85-94). §7-H0 pass criteria line 127 makes H1-H4 mandatory only when the issue "involves a runtime boundary, generated artifact, shared contract, hard gate, or independent review selector" — 5 categories. Cross-checking the 9 triggers against the 5: file/stdin/prompt delivery (line 88), persisted-state/resume/recovery (line 91), sibling pipelines (line 93), and prior-escape/unmasked-sibling (line 94) have no obvious member in the 5-item mandatory list. So a run can enter the mode via, e.g., a sibling-pipeline trigger and mandate no gate.

Real defect: entry-condition set and mandatory-gate set are stated independently with no map between them, leaving 4 triggers that fire the mode but pin nothing. A trigger→gate map (or a single reconciled enumeration) is the right fix. Note this partially overlaps C2 — without C2's aggregation invariant the gap is worse — but M1 is a distinct, real authoring inconsistency.

---

## M2 — H5 never mandatory

**Stance: CONCEDE.**

Evidence: §7-H0 line 127 enumerates "H1-H4 cannot be skipped" — H5 is absent. §7-H5 (lines 266-281) defines off-path review as "required when any of the following are true" including the highest-blast-radius conditions: "controls HALT/WARN/CONTINUE, data loss, review integrity, or external process invocation" (line 280). So H5 has its own mandatory trigger surface, yet nothing makes the *mode-level* applicability force it, and (separately) no invariant turns `off_path_review_decision=required ∧ ¬performed` into `verdict=blocked`.

Real defect: the control guarding the most dangerous changes is structurally optional relative to H0's mandatory set, and its `required` state has no verdict consequence. Both halves are genuine. (The verdict-consequence half is shared with m2; see m2.)

---

## M3 — N/A rationale has no field

**Stance: CONCEDE.**

Evidence: §5.2 line 78 states a pipeline escape "cannot be marked remediated when required hardening gates are missing, failed, or marked `N/A` without rationale." The §8 template gate lines (304-307) are `PASS | FAIL | N/A — <card path>` — the trailing slot is a *card path*, not a rationale. There is no rationale field adjacent to an N/A selection anywhere in the template.

Real defect: the §5.2 constraint ("no bare N/A") is literally unenforceable through the §8 report shape because the template provides nowhere to write the rationale. Adding `— rationale: <…>` (or requiring it when the status is N/A) closes it. Cheap and correct.

---

## M4 — No initial/default values

**Stance: NARROW.**

Evidence: §6.2 (lines 100-111) defines field types and meanings but no defaults; the header says "Add optional fields … when pipeline-hardening mode is evaluated" (line 100). The critique is factually right that no defaults are stated.

Why NARROW: this is a real gap but the proposed fix over-reaches for a G1 design spec. The contract is consumed by a markdown skill + refs, not a typed deserializer, so "consumers cannot distinguish unset from not_required" is a softer problem than in a typed API — a human reading REPORT.md infers "not present ⇒ not evaluated." The minimal fix is the *one* default that has a correctness consequence: tie field presence to applicability. Specifically: when `pipeline_hardening_applicable=false`, `verdict` MUST be `not_applicable` and the gate/path fields need not be emitted; when `true`, H0 MUST write `applicable` before any gate reads it. The remaining "defaults" the critique lists (paths→null, off_path→not_required, list→[]) are nice-to-have field hygiene, not design-spec-blocking, and over-specifying a full default table at G1 pre-empts the implementation. So: CONCEDE the applicable/verdict default; the full FR-14.1 default table is implementation-detail polish.

---

## M5 — H4 empty-and-no-changes undefined

**Stance: CONCEDE.**

Evidence: §7-H4 blocking rule line 258 says "H4 fails closed when effective input is absent, empty despite known changes, non-reproducible, or includes known foreign work." The phrase "empty despite known changes" implies the existence of an empty-and-*no*-changes case, but the spec never states its disposition. The H4 proof template (lines 242-253) has an "Empty/missing/malformed input behavior" line but no rule for the legitimate no-op (no runtime changes ⇒ empty input is correct).

Real defect: a genuine no-op (nothing changed, so review input is legitimately empty) is left ambiguous and could be read as FAIL under a literal "empty input" interpretation. Defining no-changes ⇒ N/A-with-no-op-proof, changes ∧ empty ⇒ FAIL, removes the ambiguity. Valid.

---

## M6 — Skip predicate non-testable; no trigger/skip precedence

**Stance: CONCEDE.**

Evidence: §6.1 line 96 — "the report must say `pipeline_hardening_applicable=false` … when the symptom **looks near** a pipeline boundary and the mode is skipped." "Looks near" is an unverifiable human impression. Separately, nothing in §6.1 or §7-H0 resolves the case where a §6.1 trigger is true but the operator writes `applicable=false`: line 96 permits a skip with a one-sentence reason, and H0 line 128 only asks for "the concrete reason and the boundary scan," never asserting trigger-true overrides operator-skip.

Real defect: the skip gate hinges on an impression rather than the already-enumerated triggers, and trigger-vs-skip precedence is undefined — exactly the latitude that produced the escape class this spec exists to close. Replacing "looks near" with "any §6.1 trigger true" and asserting ∃trigger ⇒ applicable=true (non-overridable) is the right fix.

---

## M7 — null card-path is an overloaded sentinel

**Stance: NARROW.**

Evidence: §6.2 lines 106-109 type the four card-path fields as `string | null`, with null meaning the gate is N/A (no card produced). But a gate that runs and FAILs may also produce no card path → null. So null conflates "N/A" and "failed-without-artifact." The observation is correct.

Why NARROW: the underlying defect is real but the *clean* fix is already implied by the M3/§8 direction, and the critique's framing slightly overstates it for this contract. The §8 report already carries an explicit per-gate `PASS | FAIL | N/A` status line (lines 304-307) that disambiguates — the overloading exists only in the §6.2 *machine* field set, which lacks the status the §8 *report* has. So the minimal fix is to mirror §8's existing status into §6.2: add a per-gate status field (or a single status map) so `path=null` is interpreted via status, not alone. This also resolves M8's NOT-PROVEN representation (a gate can be `NOT PROVEN`/FAIL with null path). The critique's fix is correct; I narrow only to note it should reuse the §8 status vocabulary already in the spec rather than invent a parallel one.

---

## M8 — NOT PROVEN unmapped to verdict

**Stance: NARROW (dedup into C2).**

Evidence: §8 line 314 mandates "NOT PROVEN blockers when any required proof is absent," but the §6.2 verdict enum (line 105) has no NOT PROVEN member and no clause maps a NOT PROVEN gate to `verdict=blocked`. So a run can carry a NOT PROVEN gate and still emit `pass`. Factually correct.

Why NARROW: the critique itself concedes this is "subsumed by C2's invariant" (line 52). It is the *same* missing invariant as C2 — "no aggregation binds gate/proof state to the top-level verdict" — viewed through the NOT PROVEN lens specifically. C2's fix (verdict=pass requires zero NOT PROVEN blockers ∧ all mandatory gates PASS) fully covers M8. Treating M8 as an independent fix risks two overlapping invariants. Minimal action: fold M8 into C2 as the explicit clause "∃ NOT PROVEN ⇒ verdict=blocked; pass forbidden while any NOT PROVEN present," and do not author it as a separate control.

---

## M9 — No fixpoint after H3 discovery

**Stance: CONCEDE.**

Evidence: §7-H3 (lines 196-231) is the wave that searches for and surfaces same-class siblings ("Adjacent hits and dispositions," line 209; "Sibling negative controls," line 208). But neither H3's blocking rules (lines 220-223) nor H0 (lines 115-128) nor H2 (lines 165-194) say what happens when a sweep *discovers a new boundary or consumer*: nothing re-enters H0 reclassification or H2 enumeration. The "Decision" column in H2 includes "follow-up" (line 180), but that is for consumers already inventoried, not for sweep-discovered new ones.

Real defect: a sweep-discovered escape can be recorded as an "adjacent hit" with no gate ever applied to it — a real fixpoint gap in an iterative discovery protocol. Requiring H3 discoveries that introduce a new boundary/consumer to re-trigger H0/H2 (or be logged as a named follow-up escape with disposition) is sound and proportionate.

---

## M10 — E3 has single-gate coverage

**Stance: NARROW.**

Evidence: The critique claims E3 is "caught by H3 alone." Checking the spec's own coverage statements: §7-H1 "Escapes caught" (lines 158-163) lists "E2/E3: full generated artifact replay would show whether the gate applies only to executable work sections" (line 162) — so **H1 already cross-lists E3** at whole-artifact replay. §7-H2 line 192 lists E2/E3 under contract enumeration. §7-H3 line 228 lists E3. §3 line 44 (E3 row) names "Unmask-and-sweep regression wave + severity blast-radius review." So E3 is referenced under H1, H2, and H3 — not H3 alone. The critique's "single-gate coverage" premise is partly false.

Further: the critique's own proposed fix — "make a passing E3-style sibling-heading negative fixture an explicit H3 completion criterion" — is **already required** by §7-H3 "Minimum regression pattern" line 216: "A sibling/off-path negative case proves same-token or same-shape non-target content does not hard-fail." E3 is the canonical sibling-heading case; that minimum pattern already mandates exactly the fixture the critique asks for.

Why NARROW not REJECT: there is a residual valid sliver. The minimum-regression pattern (line 216) is stated *generically* ("a sibling/off-path negative case"); it does not *name* E3 as a required completion fixture, so an implementer could satisfy line 216 with some other sibling case and never exercise the specific findings-heading shape that escaped. Minimal fix: add E3's sibling-heading negative fixture as a *named* example under H3's line-216 pattern. The other half of the critique's fix ("cross-list E3 under H1 whole-artifact replay") is **already done** at line 162 and needs no change. So: NARROW to "name the E3 fixture under the existing line-216 pattern"; reject the H1 cross-listing half as already satisfied.

---

## M11 — H2 completeness is self-attested

**Stance: CONCEDE.**

Evidence: §7-H2 blocking rule line 185 — "H2 fails if any live consumer is unclassified." The completeness evidence is the ledger's "How found" column (line 177: "Semantic retrieval, exact search terms, symbol/reference search, template inventory, generated fixture inventory") and "Evidence" column (line 181). Both are author-filled prose; there is no required machine-checkable manifest. So "I classified all live consumers" rests on author attestation — unbounded and unverifiable, which is the precise failure mode (accepting an author's "covered" claim) the spec targets.

Real defect: H2's completeness is self-attested, with no manifest gate. Requiring a consumer-discovery manifest (exact search terms + symbol/reference-search results) as evidence, and treating its absence as H2 = NOT PROVEN, is consistent with the spec's own "effective-input/manifest" rigor elsewhere (H4 line 251 already demands a "Machine-checkable manifest or equivalent evidence"). The asymmetry — H4 requires a manifest, H2 does not — is itself evidence the critique is right. Valid.

---

## m1 — known_escapes_caught typing vs H0 vocabulary

**Stance: NARROW.**

Evidence: §6.2 line 111 types `known_escapes_caught` as `list[string]` with no format constraint. §7-H0 line 123 lists the candidate vocabulary as "`E1`, `E2`, `E3`, `E4`, `E5`, or `Future E6+`." So the field can legally hold free-form strings that don't match the H0 vocabulary. Mild real inconsistency.

Why NARROW: this is genuinely minor and the proposed regex (`^E\d+$`) is slightly wrong — it would reject the spec's own documented `Future E6+` / `E6+` literal token (line 123). The minimal fix is to constrain the field to the H0 vocabulary (`E\d+` or the `E6+` literal), not impose a regex that contradicts H0. Worth a one-line tightening; not worth formal schema machinery for a markdown-consumed field.

---

## m2 — §8 closure section lacks explicit off-path→verdict line

**Stance: NARROW (fold into M2).**

Evidence: §8 line 308 reports "Off-path review decision: required | performed | waived_with_rationale | not_required" but the §8 closure block (lines 300-312) states no verdict consequence when the decision is `required` and review was neither performed nor waived. Correct observation.

Why NARROW: the critique itself says "(Folds into M2.)" (line 74). M2's second half is exactly the missing invariant `off_path_review_decision=required ∧ ¬performed ⇒ verdict=blocked`. Authoring m2 separately duplicates M2. Minimal action: implement the invariant once under M2 and add the co-located §8 report line as a presentation detail of that same fix; do not track m2 as an independent change.

---

## Summary table

| ID | Stance | One-line reason |
|---|---|---|
| C1 | CONCEDE | §6.2 4-value enum vs §8 3-value line genuinely disagree; skip case unrenderable in REPORT.md. |
| C2 | CONCEDE | No invariant binds gate/proof state to verdict ⇒ vacuous `pass` reachable; the set's worst defect. |
| C3 | NARROW | `advisory` is dead enum surface (no gate emits it, no consumer defined); minimal fix is removal, not define-and-parity-test. |
| M1 | CONCEDE | 9 triggers vs 5 mandatory categories; 4 triggers fire the mode but pin no gate. |
| M2 | CONCEDE | H5 absent from H0 mandatory set and its `required` state has no verdict consequence. |
| M3 | CONCEDE | §5.2 forbids bare N/A but §8 template offers no rationale field ⇒ unenforceable. |
| M4 | NARROW | Only the applicable/verdict default is design-blocking; full FR-14.1 default table is implementation polish. |
| M5 | CONCEDE | Legitimate no-changes ⇒ empty-input no-op case is undefined; could be misread as FAIL. |
| M6 | CONCEDE | "Looks near" is non-testable and trigger-vs-operator-skip precedence is undefined. |
| M7 | NARROW | Real overload, but minimal fix reuses §8's existing PASS/FAIL/NA status in §6.2 rather than a new field set. |
| M8 | NARROW | Same missing aggregation invariant as C2 (critique concedes subsumption); fold into C2, don't author twice. |
| M9 | CONCEDE | No fixpoint: H3-discovered new boundary/consumer never re-enters H0/H2 ⇒ ungated escape recordable. |
| M10 | NARROW | "Single-gate" premise partly false — E3 already cross-listed under H1 (l.162) and the sibling-negative fixture already required by H3 l.216; only need to *name* the E3 fixture. |
| M11 | CONCEDE | H2 completeness is author-attested with no manifest; H4 already requires a manifest (l.251), exposing the asymmetry. |
| m1 | NARROW | Real typing gap, but proposed `^E\d+$` rejects the spec's own `E6+` token; constrain to H0 vocab instead. |
| m2 | NARROW | Folds into M2 (critique concedes); implement the off-path→verdict invariant once, not twice. |

**Tally (16 total):** CONCEDE = 9 (C1, C2, M1, M2, M3, M5, M6, M9, M11). NARROW = 7 (C3, M4, M7, M8, M10, m1, m2). REJECT = 0.

**Defender's net position:** No critique is a pure false positive — all 16 identify a real textual gap, which is consistent with a G1 design spec that specified rich gate-level rigor (H1-H4 blocking rules) but under-specified the *aggregation* layer (verdict invariant, trigger→gate map, status sentinels) that ties gates to the top-level contract. The seven NARROWs reduce scope: four are de-duplications (M8→C2, m2→M2) or already-partly-satisfied claims (M10's H1 cross-list at l.162, the H3 l.216 sibling pattern), and three argue the minimal fix (C3 remove-don't-define, M4 one default not a table, M7/m1 reuse-existing-vocabulary). The two CRITICALs that matter most — C1 (enum contradiction) and C2 (vacuous pass) — are fully conceded and should be fixed before G1 approval.
