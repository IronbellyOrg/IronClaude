# Debate — Prosecutor Findings (G1 Spec Hardening)

Spec: `troubleshoot-pipeline-hardening-spec.md` (382 lines)
Critiques: `spec-critiques-G1.md` (C1–C3, M1–M11, m1–m2 = 16)
Role: PROSECUTOR — confirm real defects with exact spec-line evidence, re-rate severity, and flag WEAK / DUPLICATE / over-engineered critiques.
Date: 2026-06-10

---

## CORE INVARIANT TRACE — Can a vacuous `pass` be emitted? (C2)

**Question:** Under the spec AS WRITTEN, can a run with every `*_card_path = null` and `known_escapes_caught = []` legally emit `pipeline_hardening_verdict = pass`?

Tracing every line that could constrain `pass`:

1. **§6.2 line 105** — `pipeline_hardening_verdict` is typed only as `string` with enumerated *legal values* `{pass, blocked, advisory, not_applicable}`. There is **no predicate** stated tying `pass` to any gate outcome. An enum of legal *spellings* is not an invariant on *when* each is permitted.
2. **§6.2 lines 106–109** — `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path` are each typed `string | null`. `null` is an *explicitly legal* value. Nothing says "a null path forbids pass."
3. **§6.2 line 111** — `known_escapes_caught: list[string]`. No minimum cardinality. `[]` is legal.
4. **§7 H1 "Blocking rule" lines 153–156** — H1 "fails if proof stops at helper construction…". This only fires *when H1 is actually run and proof exists but is helper-only*. If no card is produced at all (path=null), there is no proof to evaluate, so the blocking rule has no antecedent to match. It blocks *bad proof*, not *absent proof*.
5. **§7 H2 line 185** — "H2 fails if any live consumer is unclassified." Same gap: with an empty/absent ledger there are zero *classified* consumers, but the rule keys on "unclassified live consumer," which presupposes the wave ran and enumerated live consumers. A skipped wave that enumerates nothing trivially satisfies "no unclassified consumer remains."
6. **§7 H3 lines 220–223 / H4 lines 256–258** — both "fail" clauses are conditioned on the wave executing (a fix that "only addresses the reported repro," an effective input that is "empty despite known changes"). None fires when the wave is simply not run.
7. **§8 line 314** — "The protocol must use `NOT PROVEN` blockers when any required proof is absent." This is the ONLY line that gestures at absent-proof handling — but (a) `NOT PROVEN` is **not a member of the verdict enum** (§6.2 line 105 nor §8 line 311), so it has no machine consequence on `pipeline_hardening_verdict`, and (b) "required proof" is never bound to a specific gate→field mapping, so "absent" is unadjudicable. M8 confirms this gap independently.
8. **§10 acceptance criteria** (lines 346–357) are *post-implementation* acceptance criteria for the human, not runtime verdict predicates the protocol enforces on itself.

**Verdict on the trace: CONFIRMED, CRITICAL.** Under the spec as written, `applicable=true`, all card_paths=null, `known_escapes_caught=[]`, every gate skipped, `pipeline_hardening_verdict=pass` is a **legal, internally consistent output**. No line forbids it. This directly defeats the spec's stated whole purpose (§1 line 9; §4 lines 52–59 "reject the following proof substitutions"; §8 line 314). The protocol can certify a pipeline escape "remediated" having proven nothing. This is the single most important defect in the set and every other gate-binding critique (M2, M3, M7, M8, M9, M11, m2) is a facet of, or a precondition for, closing it.

---

## PER-CRITIQUE FINDINGS

### C1 — Verdict enum contradiction (§6.2 ↔ §8)
- **Verdict: CONFIRMED.**
- **Evidence:** §6.2 line 105 enumerates 4 values: `pass`, `blocked`, `advisory`, or `not_applicable`. §8 line 311 closure line enumerates 3: `Closure verdict: pass | blocked | advisory`. §6.2 line 104 + §6.1 line 96 establish `not_applicable`/`applicable=false` as a reachable state (a pure local fix sets `pipeline_hardening_applicable=false`). The §8 report line that materializes the verdict cannot represent `not_applicable`. §8 line 302 separately carries "Applicability: applicable | not applicable" — so the report *can* express applicability, but the **Closure verdict field itself** (line 311) cannot carry `not_applicable`. Two normative statements of the same field's domain disagree.
- **Pre-empt defender:** A defender may argue line 302's applicability line covers the not_applicable case, so line 311 needn't. But §6.2 line 105 makes `not_applicable` a value *of the verdict field*, not of a separate applicability field — the report template is the serialization of the contract and drops a contract-legal value. Inconsistency stands.
- **Severity (re-rated): Minor → upgraded to Major** because the field is the protocol's terminal signal; a downstream consumer reading the §8 report cannot round-trip the §6.2 contract. But it is mechanical, not value-defeating.
- **Minimal fix:** Make §6.2 the single normative enum; either add `not_applicable` to §8 line 311, or state §8 line 311 is the 3-value verdict emitted ONLY when applicable=true and pin the §6.2→§8 mapping (`applicable=false ⇒ verdict=not_applicable`, reported via line 302; line 311 omitted/`N/A`).
- **Dependency:** Interacts with C3 (advisory) and M4 (defaults) — all three touch the §6.2 verdict domain; fix them together to avoid re-introducing a mismatch.

### C2 — Vacuous pass is reachable
- **Verdict: CONFIRMED — CORE INVARIANT.** (Full trace above.)
- **Evidence:** §6.2 lines 105–111 (verdict + paths + list all permit the empty/null/`pass` combination with no binding predicate); §7 blocking rules lines 153–156, 185–187, 220–223, 256–258 all key on *executed-wave* antecedents, never on *absent* gates; §8 line 314 NOT PROVEN has no enum membership (line 105/311) → no machine consequence. Contradicts §1 line 9 and §4 lines 52–59.
- **Severity (re-rated): Critical — confirmed.** This is the defect that strikes the spec's core value: it lets the protocol "certify nothing as remediated," the exact failure §4 exists to prevent.
- **Minimal fix:** Add a single normative verdict invariant (one paragraph in §6.2 or a new §6.3): `verdict=pass` requires — (1) `pipeline_hardening_applicable` written by H0; (2) every gate mandatory under the reconciled H0 set has status=PASS with a non-null artifact path; (3) zero NOT PROVEN blockers; (4) `off_path_review_decision ∈ {performed, not_required, waived_with_rationale}`. Everything else (M2, M7, M8, m2) feeds the precision of this invariant.
- **Dependency:** **C2 is the apex.** It SUBSUMES M8 (NOT PROVEN⇒blocked is clause 3), SUBSUMES m2 (off-path⇒blocked is clause 4 + M2). It *depends on* M7 (a real per-gate status field is required for clause 2 to be expressible) and M1 (the "mandatory gate set" referenced by clause 2 must first be reconciled). The critique itself flags M8 as subsumed — correct.

### C3 — advisory verdict reintroduces E4
- **Verdict: CONFIRMED.**
- **Evidence:** §3 line 45 defines E4 as `SemanticCheck.advisory` treated as fatal by a bespoke runtime. §6.2 line 105 introduces `advisory` as a verdict value with (a) no selection criterion vs `blocked` anywhere in §6.2 or §7, and (b) no consumer contract stating who must treat it non-fatally. §11 line 366 claims the controls catch E4. The spec thus recreates an advisory-severity contract with an undefined consumer disposition — structurally identical to the E4 mechanism, now inside the protocol's own output. §8 line 311 compounds it by listing `advisory` as a terminal closure verdict with no halt/continue semantics attached.
- **Pre-empt defender:** A defender may say "advisory" is self-evidently non-halting. But E4's whole lesson (§3 line 45, §4 line 58) is that "advisory" semantics are NOT self-evident across consumers — a bespoke consumer treated advisory as fatal. The spec cannot rely on the very assumption it was built to destroy.
- **Severity (re-rated): Major.** Not Critical — it does not by itself produce a vacuous pass — but it is a genuine self-contradiction (§11 vs §6.2) and re-opens the canonical escape class inside the new contract. The "internal contradiction" framing is justified, not inflated.
- **Minimal fix (narrower than critique's):** Prefer the critique's first option — **remove `advisory`** from §6.2 line 105 and §8 line 311; collapse to `{pass, blocked, not_applicable}`. The "non-mandatory gate failed" case is already representable as `blocked` (fail-closed) which is the safer default given E4's lesson. If advisory is kept, the critique's second option (total function over gate states + pinned non-halting consumer contract + parity test) is required — but that is more machinery than the spec needs at G1.
- **Dependency:** Conflicts with C1/M4 (verdict domain) — resolve the enum once. If `advisory` is removed, C1's mapping simplifies and m1 is unaffected.

### M1 — Trigger set (9) ≠ H0 mandatory set (5)
- **Verdict: CONFIRMED.**
- **Evidence:** §6.1 lines 84–94 list **9** trigger bullets. §7 H0 pass criteria line 127 makes H1–H4 mandatory for **5** boundary classes ("runtime boundary, generated artifact, shared contract, hard gate, or independent review selector"). The 4 unmapped triggers — file/stdin/prompt delivery (line 87), persisted-state/resume/recovery (line 90), sibling pipelines (line 93), prior-escape/unmasked-sibling (line 94) — can fire the mode (§6.1) while mandating no gate (§7 line 127). E1 (cloud `--file`) is itself a file-delivery escape and E5 a persisted/selector escape, so the unmapped triggers are not hypothetical.
- **Severity (re-rated): Major — confirmed.** Feeds C2: an entry condition with no mandated gate is a direct path to vacuous pass for that trigger class.
- **Minimal fix:** Add a trigger→mandatory-gate map (one table) so every §6.1 entry condition pins ≥1 gate; reconcile the two enumerations to one list. E.g. file/stdin/prompt⇒H1; persisted-state⇒H1+H2; sibling⇒H2+H3; prior-escape⇒H3.
- **Dependency:** **Prerequisite for C2 clause 2** — C2's "every gate mandatory under the reconciled H0 set" is undefined until M1 reconciles that set. C2 ⊋ M1 in the sense that C2 cannot be fully specified without M1's map.

### M2 — H5 never mandatory
- **Verdict: CONFIRMED.**
- **Evidence:** §7 H0 line 127 enumerates H1–H4 as non-skippable and **omits H5**. §7 H5 lines 270–280 list the highest-blast-radius triggers (line 280: "controls HALT/WARN/CONTINUE, data loss, review integrity, or external process invocation"). So the control gating the most dangerous changes is, by line 127, never mandatory — H5 is governed only by its own "required when" prose (line 270) with no binding to the verdict.
- **Severity (re-rated): Major — confirmed.** The off-path reviewer is the catcher for E4/E5-class divergences (§7-H5 maps to R1,R3,R4,R5,R6 line 268); leaving it non-mandatory undermines the off-path-reviewer design pillar (§1 line 16).
- **Minimal fix:** Make H5 mandatory when its line-270 conditions hold; add invariant `off_path_review_decision=required ∧ ¬(performed ∨ waived_with_rationale) ⇒ verdict=blocked`.
- **Dependency:** **m2 is a DUPLICATE of M2** (m2 line 74 itself says "Folds into M2"). M2's invariant is also C2 clause 4. So C2 ⊇ M2 ⊇ m2 for the verdict-binding half; M2 adds the orthogonal "make H5 mandatory" half that C2 does not cover.

### M3 — N/A rationale has no field
- **Verdict: CONFIRMED.**
- **Evidence:** §5.2 line 78 forbids marking a gate `N/A` "without rationale." §8 template lines 304–308 render each gate as `PASS | FAIL | N/A — <card path>` with **no rationale slot** — the trailing `<card path>` is a path, not a rationale, and for an N/A gate there is typically no card. The §5.2 constraint is therefore unenforceable through the prescribed report shape.
- **Severity (re-rated): Major — confirmed (not Minor).** Without a rationale field, every gate can be N/A'd into oblivion with no recorded justification — another concrete route to the C2 vacuous pass (all-N/A is observationally close to all-null).
- **Minimal fix:** Add `— rationale: <…>` to each gate line in §8 lines 304–308; declare a bare `N/A` (no rationale) invalid in §5.2 / H0.
- **Dependency:** Supports C2 (closes the all-N/A variant) and M7 (status field). Pairs with M7: rationale belongs adjacent to the explicit status field.

### M4 — No initial/default values
- **Verdict: CONFIRMED (but partly mitigated by H0).**
- **Evidence:** §6.2 lines 104–111 specify Type and Meaning columns but **no defaults/initial values**. There is no way for a consumer to distinguish "field unset because mode never ran" from "deliberately not_required/not_applicable." Note: H0 (line 121 "`pipeline_hardening_applicable` decision") partially addresses `applicable` by requiring H0 to write it — so the critique's claim "applicable→must be written by H0 before any read" is already half-present in the spec, which slightly narrows M4.
- **Severity (re-rated): Major → Minor.** Real but lower-value: for a prose/markdown protocol consumed by a skill (not a typed API), "unset vs not_required" ambiguity is mostly cosmetic *once C2's invariant exists*, because the invariant reads gate status, not field presence. The defaults are good hygiene but not value-defeating.
- **Minimal fix:** Add a default column to §6.2: verdict→`not_applicable`, paths→`null`, `off_path_review_decision`→`not_required`, `known_escapes_caught`→`[]`, `pipeline_hardening_applicable`→(no default; H0 must write before read).
- **Dependency:** Cosmetic relative to C2/M7. Resolve enum domain consistently with C1/C3.

### M5 — H4 empty-and-no-changes undefined
- **Verdict: CONFIRMED.**
- **Evidence:** §7 H4 line 258 "fails closed when effective input is absent, empty despite known changes, non-reproducible, or includes known foreign work." The legitimate **no-changes ⇒ empty-input** case is not covered: "empty despite known changes" implies changes exist; the spec is silent on empty input when there are *no* changes. Without that, a true no-op review either spuriously FAILs (over-strict) or falls through to an undefined state.
- **Severity (re-rated): Minor → Major borderline; settle on Major.** An undefined branch in a fail-closed gate is exactly the ambiguity that produces either false blocks (eroding adoption) or silent passes (eroding the invariant). H4 is the E5 catcher (§7 line 262), so precision here is load-bearing.
- **Minimal fix:** Add to §7 H4: `no runtime changes ⇒ H4 = N/A with no-op proof (runtime-produced expected surface = ∅, asserted)`; `changes ∧ empty input ⇒ FAIL`.
- **Dependency:** Interacts with M7 (N/A vs FAIL needs the explicit status field) and M3 (N/A needs rationale/no-op proof).

### M6 — Skip predicate non-testable; no trigger/skip precedence
- **Verdict: CONFIRMED.**
- **Evidence:** §6.1 line 96 "Pure local bug fixes may skip this mode, but the report must say `pipeline_hardening_applicable=false` … when the symptom **looks near** a pipeline boundary." "Looks near" is an unverifiable human impression. Separately, nothing resolves the conflict "any §6.1 trigger is objectively true ∧ operator writes applicable=false" — there is no precedence rule making a true trigger override the skip. M9-style sweep discoveries (line 94 trigger) make this worse: a trigger can become true mid-run.
- **Severity (re-rated): Major — confirmed.** A non-testable skip predicate plus no trigger-override is *the* operator-discretion hole that lets the whole mode be skipped — the human-judgment analogue of C2.
- **Minimal fix:** Replace "looks near a pipeline boundary" with "any §6.1 trigger is true"; add precedence: `∃ §6.1 trigger true ⇒ applicable=true (non-overridable); applicable=false permitted only when zero triggers fire`.
- **Dependency:** Pairs with M1 (the trigger enumeration M6 references must be the reconciled one). Together M1+M6 fully close the entry surface; C2 closes the exit surface.

### M7 — null card-path is an overloaded sentinel
- **Verdict: CONFIRMED.**
- **Evidence:** §6.2 lines 106–109 type the four card paths `string | null` and §6.2 Meaning column gives null no semantics. §8 lines 304–307 allow a gate to be `FAIL` — but a FAILed gate that wrote no card also yields path=null, colliding with the "N/A / not produced" reading of null. One sentinel, two opposite meanings (passed-N/A vs failed-no-artifact).
- **Severity (re-rated): Major — confirmed.** This is the **enabling defect** for C2 clause 2: without a status field distinct from the path, the verdict invariant *cannot* express "every mandatory gate PASS with non-null artifact," because null is ambiguous between FAIL and N/A.
- **Minimal fix:** Add an explicit per-gate status field `{PASS, FAIL, NA, NOT_PROVEN}` to §6.2, distinct from the path; permit path=null only when status ∈ {NA, NOT_PROVEN}.
- **Dependency:** **M7 is a precondition for C2, M3, M5, M8.** The critique header flags "M7 status-field enables M8/C2/M5/M3 enforcement" — confirmed: all four verdict/branch invariants need a status field to key on. Fix M7 first.

### M8 — NOT PROVEN unmapped to verdict
- **Verdict: CONFIRMED — but DUPLICATE-subsumed by C2.**
- **Evidence:** §8 line 314 "The protocol must use `NOT PROVEN` blockers when any required proof is absent." `NOT PROVEN` appears in **neither** the §6.2 line 105 verdict enum nor the §8 line 311 closure enum, so it has no effect on the terminal verdict — a run can carry a NOT PROVEN gate and still emit `pass`.
- **Severity (re-rated): Major as a standalone gap; but it is C2 clause 3.** The critique line 52 itself says "(subsumed by C2's invariant)."
- **Minimal fix:** Define `∃ NOT PROVEN ⇒ verdict=blocked`; add NOT_PROVEN to the per-gate status set (M7). Implemented as clause 3 of the C2 invariant.
- **Dependency:** **DUPLICATE of C2** (subset). Keep as a named sub-clause of the C2 fix; do not author a separate competing invariant. Depends on M7 for a status token to carry NOT_PROVEN.

### M9 — No fixpoint after H3 discovery
- **Verdict: CONFIRMED.**
- **Evidence:** §7 H3 lines 196–231 is the wave that "search[es] for adjacent masked defects" (line 222) — i.e. it *discovers new boundaries/consumers*. But §7 H0 (lines 115–128) and H2 (lines 165–194) are described as forward passes with **no re-entry/fixpoint** when H3 surfaces a new boundary or consumer. §6.2 `known_escapes_caught` (line 111) lets a sweep-discovered escape be *recorded* with no gate ever applied to it. The escape-coverage logic (E3, §3 line 44) is literally the "incomplete sweep" class — proving the spec needs iteration to closure.
- **Severity (re-rated): Major — confirmed.** A one-pass pipeline against a problem class defined by *masking* (E2→E3) is structurally insufficient; without a fixpoint, the protocol re-creates the E3 escape mechanism.
- **Minimal fix:** Add to §7 H3: a sweep hit that introduces a new boundary/consumer MUST either (a) re-enter H0 reclassification + H2 enumeration for that surface, or (b) be logged as an explicit follow-up escape with a named disposition (owner + gate) — and an undispositioned discovery ⇒ verdict=blocked.
- **Dependency:** Feeds C2 (undispositioned discovery must block). Pairs with M11 (H2 completeness) — the fixpoint re-invokes H2, so H2 must be verifiable.

### M10 — E3 has single-gate coverage
- **Verdict: WEAK (real but over-stated as a spec defect).**
- **Evidence:** §3 line 44 confirms E3 arose from an incomplete E2 fix. §7 H3 lines 225–231 and §11 line 365 do assign E3 primarily to H3. **However**, §7 H1 line 161 ("E2/E3: full generated artifact replay would show whether the gate applies only to executable work sections") and §7 H2 line 192 ("E2/E3: executable phase-plan headings would be classified separately…") **already cross-list E3 under H1 and H2**. So the premise "E3 is caught by H3 alone" is factually contradicted by the spec's own escape-caught lines. The redundancy the critique asks for is largely *already present*.
- **Severity (re-rated): Minor.** What survives is a narrower, legitimate ask: make the E3-style sibling-heading negative fixture an *explicit H3 completion criterion* (currently H3 line 216 lists it as a "minimum regression pattern" step but not a named pass/fail completion gate). That is a worthwhile tightening, not a Major coverage hole.
- **Minimal fix:** Add to §7 H3 blocking rule: "H3 is not PASS until a sibling-heading (E3-class) negative fixture is exercised and does not hard-fail." Drop the "cross-list under H1" half — already done at line 161.
- **Dependency:** Folds into the M3/M5/M9 H3-tightening cluster. Not independent enough to rate Major.

### M11 — H2 completeness is self-attested
- **Verdict: CONFIRMED.**
- **Evidence:** §7 H2 line 185 "H2 fails if any live consumer is unclassified" — but completeness rests entirely on the author-filled "How found" column (§7 H2 ledger line 177: "Semantic retrieval, exact search terms, symbol/reference search…") with **no machine-checkable manifest**. "I classified all live consumers" is unfalsifiable from the artifact alone. This is the H2 analogue of C2: the gate *claims* completeness but provides no evidence binding.
- **Severity (re-rated): Major — confirmed.** H2 is the contract-parity catcher for E4 (the most subtle escape); a self-attested completeness claim is exactly the "adjacent proof accepted as runtime proof" pattern §1 forbids.
- **Minimal fix:** Require a consumer-discovery manifest (exact search terms + raw symbol/reference-search result set) attached as H2 evidence; absence ⇒ H2 = NOT_PROVEN (not PASS).
- **Dependency:** Depends on M7 (NOT_PROVEN status token). Pairs with M9 (fixpoint re-invokes H2; manifest makes re-invocation checkable). Strengthens C2 clause 2 for the H2 gate specifically.

### m1 — known_escapes_caught typing vs H0 vocabulary
- **Verdict: CONFIRMED (Minor).**
- **Evidence:** §7 H0 line 123 lists candidate values "`E1`, `E2`, `E3`, `E4`, `E5`, or `Future E6+`" but §6.2 line 111 types the field `list[string]` with no format constraint. The literal "Future E6+" is not a valid single escape ID and would not match a naive `^E\d+$`. Mild vocabulary drift.
- **Severity (re-rated): Minor — confirmed.** Cosmetic; no value impact, but a real typing gap.
- **Minimal fix:** Constrain §6.2 line 111 to `items matching ^E\d+$` plus the literal `"E6+"` (or `"Future"`) for forward-looking entries; align H0 line 123 wording.
- **Dependency:** Independent; trivial. Resolve alongside M4 defaults.

### m2 — §8 closure section lacks explicit off-path→verdict line
- **Verdict: DUPLICATE of M2** (the critique itself states "Folds into M2," line 74).
- **Evidence:** §8 line 308 reports `Off-path review decision: required | performed | waived_with_rationale | not_required` but the §8 closure section states no verdict consequence; §6.2 line 110 same. The missing rule (`required ∧ ¬performed/¬waived ⇒ blocked`) is exactly M2's invariant and C2 clause 4.
- **Severity (re-rated): Minor.** Co-location nicety; the substantive rule is owned by M2/C2.
- **Minimal fix:** When implementing the M2/C2 invariant, also add the consequence line to §8 after line 308. No separate fix.
- **Dependency:** **DUPLICATE — subsumed by M2 (and C2 clause 4).** Do not track separately.

---

## SUMMARY TABLE

| ID | Verdict | Re-rated severity | Minimal fix (≤10 words) |
|---|---|---|---|
| C1 | CONFIRMED | Major | Single normative enum; map applicable=false→not_applicable into §8 |
| **C2** | **CONFIRMED (CORE)** | **Critical** | Add verdict=pass invariant binding gates+NOT_PROVEN+off-path |
| C3 | CONFIRMED | Major | Remove `advisory`; collapse to pass/blocked/not_applicable |
| M1 | CONFIRMED | Major | Add trigger→mandatory-gate map; reconcile 9 vs 5 |
| M2 | CONFIRMED | Major | Make H5 mandatory; required∧¬performed⇒blocked |
| M3 | CONFIRMED | Major | Add rationale field to each N/A gate line |
| M4 | CONFIRMED | Minor | Add default column to §6.2 fields |
| M5 | CONFIRMED | Major | Define no-changes⇒N/A; changes∧empty⇒FAIL |
| M6 | CONFIRMED | Major | Replace "looks near"; trigger overrides skip |
| M7 | CONFIRMED | Major | Add per-gate status field distinct from path |
| M8 | CONFIRMED (⊂C2) | Major | Define NOT_PROVEN⇒blocked (C2 clause 3) |
| M9 | CONFIRMED | Major | H3 discovery re-enters H0/H2 or logs follow-up |
| M10 | WEAK | Minor | Make E3 sibling fixture an H3 completion criterion |
| M11 | CONFIRMED | Major | Require consumer-discovery manifest; absent⇒NOT_PROVEN |
| m1 | CONFIRMED | Minor | Constrain field to `^E\d+$`+`E6+` literal |
| m2 | DUPLICATE (M2) | Minor | Co-locate off-path→blocked consequence in §8 |

**Counts:** CONFIRMED = 13 (C1, C2, C3, M1, M2, M3, M4, M5, M6, M7, M9, M11, m1) · WEAK = 1 (M10) · DUPLICATE = 2 (M8⊂C2, m2⊂M2). Note: M8 is confirmed-but-subsumed (counted under DUPLICATE for tracking; the underlying defect is real).

---

## DEPENDENCY GRAPH OF FIXES

```
                         ┌──────────────────────────────┐
                         │  M7  (per-gate STATUS field)  │   ← ENABLER: fix FIRST
                         │  PASS|FAIL|NA|NOT_PROVEN       │
                         └───────────────┬───────────────┘
                                         │ provides status tokens
          ┌───────────────┬─────────────┼─────────────┬───────────────┐
          ▼               ▼             ▼             ▼               ▼
    ┌───────────┐   ┌───────────┐ ┌───────────┐ ┌───────────┐  ┌──────────────┐
    │ C2 clause2│   │ M8=clause3│ │ M5 (NA vs │ │ M3 (NA    │  │ M11 (H2 NOT_ │
    │ gate=PASS │   │ NOT_PROVEN│ │ FAIL split│ │ rationale)│  │ PROVEN if no │
    │ ∧ non-null│   │ ⇒ blocked │ │           │ │           │  │ manifest)    │
    └─────┬─────┘   └─────┬─────┘ └───────────┘ └───────────┘  └──────────────┘
          │               │
          │   ┌───────────┴───────────────────────────┐
          ▼   ▼                                       │
  ┌─────────────────────────────────────────┐         │
  │  C2  VERDICT INVARIANT (apex)            │◄────────┘  (m2 ⊂ clause4; M2 verdict-half ⊂ clause4)
  │  pass ⇔ applicable∧allMandatoryPASS∧     │
  │         0 NOT_PROVEN ∧ off_path∈{ok}     │
  └───────┬───────────────────────┬──────────┘
          │ needs reconciled set  │ needs off-path mandatory
          ▼                       ▼
   ┌──────────────┐        ┌──────────────────────────┐
   │ M1 trigger→  │        │ M2 (H5 mandatory half —  │
   │ gate map     │        │ orthogonal to C2)        │
   │ (9 vs 5)     │        └──────────────────────────┘
   └──────┬───────┘
          │ shares trigger enumeration
          ▼
   ┌──────────────┐
   │ M6 skip-pred │   entry-surface close (pairs with M1)
   │ + precedence │
   └──────────────┘

  Independent / verdict-domain cluster (resolve enum once):
   C1 ── C3 (remove advisory) ── M4 (defaults) ── m1 (escape-id format)

  H3-iteration cluster:
   M9 (fixpoint) ── M11 (H2 manifest verifiable on re-entry) ── M10 (E3 H3 completion criterion, WEAK)
```

**Critical path to close the core defect:** M7 (status field) → M1 (reconcile mandatory-gate set) → C2 (verdict invariant, absorbing M8 + m2 + M2-verdict-half) → M6 (entry-surface override). Without M7 the C2 invariant is inexpressible; without M1 its "mandatory gate set" is undefined; without M6 the whole mode is skippable.
