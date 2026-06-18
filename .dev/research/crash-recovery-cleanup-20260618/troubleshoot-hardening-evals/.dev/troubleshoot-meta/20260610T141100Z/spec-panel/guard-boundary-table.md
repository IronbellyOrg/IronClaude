# Guard Condition Boundary Table — Troubleshoot Pipeline Hardening

> **HARD GATE artifact** (Crispin boundary-test lead, Whittaker adversarial). `/sc:spec-panel --focus correctness`.
> Source guards: `troubleshoot-pipeline-hardening-spec.md` §7 (H0–H5 blocking rules) + §6.1 trigger + `EFFICACY-REPORT-MERGED.md` §10 (waiver policy / anti-theatre invariant) + Appendix A.
> Rule: each guard gets ≥6 input-condition rows — Zero/Empty, One/Minimal, Typical, Maximum/Overflow, **Sentinel Value Match**, Legitimate Edge Case.
> **FR-8: any GAP row = MAJOR+ finding. FR-9: any blank "Specified Behavior" = MAJOR+ finding.** GAP fires wherever the draft leaves behavior unspecified.

Status key: **OK** = spec states the behavior unambiguously. **GAP** = spec is silent / ambiguous / leaves behavior to the agent.

---

## Guard H0 — Applicability skip-condition (§6.1, §7 H0)

Guard: "Pure local bug fixes MAY skip; but report must say `pipeline_hardening_applicable=false` with a one-sentence reason when symptom looks near a pipeline boundary."

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H0-skip | §6.1 last para | **Zero/Empty**: diagnosis touches no boundary class at all | `pipeline_hardening_applicable` unset | skip H1–H4 | "Pure local bug fixes may skip" — but no rule for *fully empty/no-symptom* case | **GAP** (empty diagnosis → applicable=? undefined) |
| H0-skip | §6.1 | **One/Minimal**: exactly one boundary bullet matches (e.g. only "persisted state") | =true | enter mode | "If the issue involves a runtime boundary … H1-H4 cannot be skipped" | OK |
| H0-skip | §6.1 | **Typical**: CLI subprocess + generated artifact both match | =true | enter mode | enter, H1–H4 mandatory | OK |
| H0-skip | §6.1 | **Maximum/Overflow**: all nine trigger bullets match at once | =true | enter mode | enter — but no guidance on prioritizing/bounding wave effort under max breadth | **GAP** (overflow effort/scope unspecified) |
| H0-skip | §6.1 | **Sentinel Value Match**: symptom *near* a boundary but is genuinely local (looks-like-pipeline) | =false | skip + 1-sentence reason | "must say `applicable=false` with a one-sentence reason when the symptom looks near a pipeline boundary" | OK |
| H0-skip | §6.1 | **Legitimate Edge Case**: boundary touched but change is a pure comment/doc edit | unspecified | ? | No carve-out for non-behavioral boundary-adjacent edits | **GAP** (no doc/comment-only exemption) |

---

## Guard H1 — Runtime-entrypoint blocking rule (§7 H1)

Guards: (a) "proof-stops-at-helper" → FAIL; (b) "negative-control-required" when contract has a forbidden interpretation.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H1-helper-stop | §7 H1 blocking rule 1 | **Zero/Empty**: no replay command produced at all | `runtime_entrypoint_card_path`=null | should FAIL | Spec says FAIL if proof stops at helper; **silent on zero-replay (card absent entirely)** | **GAP** (absent card vs helper-only card not distinguished) |
| H1-helper-stop | §7 H1 | **One/Minimal**: one helper-construction proof, defect lives only at subprocess | helper-only | FAIL | "H1 fails if proof stops at helper construction while the defect can appear only at a subprocess…" | OK |
| H1-neg-control | §7 H1 | **Typical**: replay reaches subprocess + 1 negative control | card populated | PASS | "requires at least one negative control when the contract has a forbidden interpretation" | OK |
| H1-neg-control | §7 H1 | **Maximum/Overflow**: contract has many forbidden interpretations (local-path, advisory-fatal, dirty-omitted, empty-accepted, heading-executable) | N negative controls | PASS only if all? | Spec lists 5 forbidden interpretations but says "**at least one** negative control" — does ONE suffice when FIVE forbidden interpretations exist? | **GAP** (one-control-covers-many ambiguity → under-proof) |
| H1-neg-control | §7 H1 | **Sentinel Value Match**: negative control "passes" because the harness silently never reached the boundary (false-green replay) | card claims PASS | must FAIL | §8 "Evidence the replay reaches the production boundary" is a card field but **no guard rejects a card whose replay-reaches-boundary field is unproven/empty** | **GAP** (CRITICAL-adjacent: false-green negative witness, see adversarial F-N2) |
| H1-neg-control | §7 H1 | **Legitimate Edge Case**: helper-only proof IS equivalent (pure in-process function, no boundary) | card "why equivalent" filled | PASS | Card field "If helper-only proof is used, why it is equivalent" exists | OK |

---

## Guard H2 — Contract-enumeration fails-if (§7 H2 three blocking rules)

Guards: (a) unclassified-live-consumer; (b) generic-proof-for-product-path; (c) sibling-not-swept.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H2-unclassified | §7 H2 rule 1 | **Zero/Empty**: ledger lists zero consumers | `contract_ledger_path` populated, 0 rows | should FAIL | "H2 fails if any live consumer is unclassified" — but a **zero-row ledger has no *unclassified* consumer either** (vacuously passes) | **GAP** (CRITICAL: empty ledger satisfies "no unclassified consumer", see F-A2/F-N3) |
| H2-unclassified | §7 H2 rule 1 | **One/Minimal**: 1 consumer, classified | 1 row, role set | PASS | enumerate + classify | OK |
| H2-generic-product | §7 H2 rule 2 | **Typical**: generic gate proven, PRD path present | generic classified | FAIL unless reachability proven | "fails if generic/shared proof is used for a product path without proving the product path reaches that implementation" — this is exactly E4 | OK |
| H2-sibling-sweep | §7 H2 rule 3 | **Maximum/Overflow**: 6 sibling pipelines share the concept | siblings partially swept | FAIL if any unswept | "fails if sibling pipelines or duplicate evaluators are not swept when the concept is shared" — but **how is the sibling *set* enumerated/bounded?** No closure rule for "did we find all siblings?" | **GAP** (sibling-set completeness unbounded → Fowler count-divergence, F-F1) |
| H2-unclassified | §7 H2 | **Sentinel Value Match**: a consumer is labeled `dead/legacy` (a valid Role value) to dodge classification, but is actually live | row role=`dead/legacy` | must FAIL if live | Role enum includes `dead/legacy` but **no guard requires proof that a dead-labeled consumer is truly unreachable** | **GAP** (CRITICAL: dead-label escape hatch, see F-S2) |
| H2-unclassified | §7 H2 | **Legitimate Edge Case**: consumer is genuinely unaffected, proof attached | row decision=`unaffected with proof` | PASS | Decision enum includes "unaffected with proof" | OK |

---

## Guard H3 — Unmask-and-sweep fails-if (§7 H3 blocking rule)

Guards: (a) only-repro (no adjacent search); (b) heuristic-hard-fatal-without-fixtures (+ cost rationale).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H3-only-repro | §7 H3 rule 1 | **Zero/Empty**: sweep dimensions list is empty | `unmask_sweep_path` present, no dims | should FAIL | "fails if a fix only addresses the reported repro and does not search for adjacent masked defects" — but **empty-dimensions still produces a path**; presence-of-path ≠ search-performed | **GAP** (path present, sweep empty — F-9 blank-behavior risk) |
| H3-only-repro | §7 H3 | **One/Minimal**: 1 positive control, 0 sibling negatives | partial controls | FAIL | §7 min pattern requires positive + sibling-negative + full-artifact; one control insufficient | OK |
| H3-heuristic-fatal | §7 H3 rule 2 | **Typical**: heuristic parser, hard-fatal, adversarial FP fixtures + cost rationale present | fixtures attached | PASS | "fails if a heuristic parser over generated prose is hard-fatal without adversarial false-positive fixtures and a cost rationale" | OK |
| H3-heuristic-fatal | §7 H3 | **Maximum/Overflow**: full generated MDTM corpus, K sibling surfaces, only a sample swept | K siblings, sample only | FAIL? | **No rule on sweep *coverage* of K siblings** — is sampling acceptable or must all K be swept? (this is the exact E3 unmask gap) | **GAP** (CRITICAL: K-sibling coverage unbounded — Fowler F-F2) |
| H3-only-repro | §7 H3 | **Sentinel Value Match**: sibling-negative fixture uses `incomplete`/`representation` (substring of `complete`/`present`) | fixture token collides | must catch + still PASS gate only if matcher word-bounded | §7 H3 requires near-miss negatives **implicitly** via E3, but the **substring-vs-word-boundary requirement is in Appendix A research-refinement, NOT bound into the H3 blocking rule** | **GAP** (CRITICAL: the E2 substring bug — Sentinel Collision — is not a stated H3 guard, see F-SC1) |
| H3-only-repro | §7 H3 | **Legitimate Edge Case**: anchor fix genuinely has no siblings (unique surface) | sweep=∅ justified | PASS | §7 min pattern assumes siblings exist; **no explicit "no-siblings, here's the proof" pass path** | **GAP** (no formal empty-sibling pass justification) |

---

## Guard H4 — Effective-input fail-closed (§7 H4 blocking rule)

Guard: "fails closed when effective input is absent, empty despite known changes, non-reproducible, or includes known foreign work."

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H4-fail-closed | §7 H4 | **Zero/Empty**: effective input absent | `effective_input_card_path`=null | FAIL (closed) | "fails closed when effective input is absent" | OK |
| H4-fail-closed | §7 H4 | **One/Minimal**: 1 file in effective input, matches 1 known change | card populated | PASS | proof of consumed surface | OK |
| H4-fail-closed | §7 H4 | **Typical**: diff range consumed, dirty work included, foreign excluded | card fields set | PASS | §7 H4 card fields cover dirty/staged + foreign-excluded | OK |
| H4-empty-despite | §7 H4 | **Maximum/Overflow**: huge diff, includes 1 foreign commit among 200 | foreign present | FAIL | "fails closed when … includes known foreign work" — but **"known" foreign is undefined**: known-to-whom? how is foreignness detected at scale? | **GAP** (foreign-detection mechanism unspecified — F-F3) |
| H4-empty-despite | §7 H4 | **Sentinel Value Match**: input non-empty but is the *wrong* surface (right size, wrong content — e.g. staged-but-not-the-task-work) | card non-empty | must FAIL | Spec catches "empty despite known changes" but **not "non-empty but wrong surface"** — the E5 trap is precisely a non-empty wrong range | **GAP** (CRITICAL: non-empty-wrong-surface — the actual E5 mechanism — F-D1) |
| H4-fail-closed | §7 H4 | **Legitimate Edge Case**: genuinely no changes expected (no-op task), empty IS correct | empty + "no changes expected" | PASS? | Spec says empty-despite-known-changes fails; **silent on legitimately-empty (no expected changes)** → risks false-FAIL | **GAP** (legitimate-empty false-FAIL — F-9) |

---

## Guard H5 — Off-path required-when + waiver-validity (§7 H5) + waiver-policy anti-theatre invariant (§10 / Appendix A)

Guards: (a) required-when (9 conditions); (b) waiver-validity (must execute risky boundary, not "tests pass"); (c) **anti-theatre: waived probe → `partial`, never re-greened**.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H5-required-when | §7 H5 | **Zero/Empty**: zero required-when conditions hold | `off_path_review_decision`=`not_required` | OK to skip | implied: not_required valid when no condition holds | OK |
| H5-required-when | §7 H5 | **One/Minimal**: exactly one condition (CLI→subprocess) | =`required`→`performed` | enforce | required when "CLI invokes a subprocess" | OK |
| H5-waiver-valid | §7 H5 waiver standard | **Typical**: waiver says "local evidence directly executes the risky boundary" | =`waived_with_rationale` | accept | valid waiver standard stated | OK |
| H5-waiver-invalid | §7 H5 | **Sentinel Value Match**: waiver text = "tests pass and reviewer is independent" | =`waived_with_rationale` (claimed) | must REJECT | "Waiver is invalid if it merely says tests pass, the reviewer is independent, the command exists, or the issue looks local" | OK |
| H5-anti-theatre | §10 / App A | **Sequence**: probe waived (→`partial`), then `sc:reflect`/`task-builder`/`adversarial` re-marks gate `success` | `waiver_status` `partial`→`success` | must be FORBIDDEN | "A waived or skipped runtime probe MUST downgrade to `partial` — may **never** be re-converted to `success`" — stated in §10 prose, **but no guard binds it into H5; nothing in §7 mechanically blocks the re-green** | **GAP** (CRITICAL: the single anti-theatre control is not a §7 guard — F-S1) |
| H5-anti-theatre | §10 / App A | **Maximum/Overflow**: many mandatory probes waived in one closure | all `partial` | signoff FAIL | "Production-facing pipeline-health signoff fails when a mandatory runtime probe is absent" — but **threshold/aggregation across many `partial` probes unspecified** | **GAP** (aggregate-partial signoff rule unspecified — F-A3) |

---

## Summary for the spec

- **Guards enumerated: 6** (H0, H1, H2, H3, H4, H5 incl. anti-theatre).
- **Input-condition rows: 36** (6 per guard).
- **GAP rows: 16** of 36 → **16 MAJOR+ findings (FR-8)**. Several rows also have under-specified ("?") Specified Behavior → also FR-9 MAJOR+.
- **Top GAP guards (each auto-generates a MAJOR+ finding; CRITICAL ones cross-referenced to adversarial-findings.md):**
  1. **H3 Sentinel Collision (F-SC1)** — the E2 substring-vs-word-boundary bug (`complete`⊂`incomplete`, `present`⊂`representation`) is only in Appendix A research-refinement, **not** bound into the H3 blocking rule. **CRITICAL.**
  2. **H2 empty-ledger (F-A2/F-N3)** — a zero-row ledger vacuously satisfies "no unclassified consumer." **CRITICAL.**
  3. **H2 dead-label escape hatch (F-S2)** — labeling a live consumer `dead/legacy` dodges classification with no unreachability proof required. **CRITICAL.**
  4. **H4 non-empty-wrong-surface (F-D1)** — the actual E5 mechanism (right-size, wrong-range) is not caught; spec only guards empty-despite-changes. **CRITICAL.**
  5. **H5 anti-theatre re-green (F-S1)** — the one control that "prevents theatre returning through the back door" is §10 prose with no §7 guard. **CRITICAL.**
  6. **H2/H3 K-sibling coverage (F-F1/F-F2)** — sibling-set and K-sibling sweep completeness are unbounded (no "found all siblings" closure). MAJOR.
  7. **H1 one-control-covers-five-forbidden-interpretations** — "at least one negative control" under-proves when 5 forbidden interpretations exist. MAJOR.
- **Recommended spec action:** promote each CRITICAL GAP into a §7 blocking-rule clause (not Appendix prose), and add explicit empty-input pass/fail disambiguation to H2/H3/H4.
