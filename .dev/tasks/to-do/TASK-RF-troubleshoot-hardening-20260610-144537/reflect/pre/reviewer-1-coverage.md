# Reviewer 1 — Coverage Matrix (UC-1 Pre-Execution Audit)

- Persona: analyzer / coverage-completeness lens
- Spec: `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md`
- Tasklist: `TASK-RF-troubleshoot-hardening-20260610-144537.md`
- Question: if executed as written, does the tasklist fully satisfy the spec?

## Method

Every spec requirement below is mapped to the tasklist item(s) that produce it. "Covered?" is
Y (an item demonstrably produces it), PARTIAL (item touches it but with a gap/risk), or N (no item
produces it). Anchors quote the tasklist (Step n.n) or cite the spec (§ref). Inferences I could not
verify against a literal item are tagged [INFERRED].

## Coverage Matrix

| # | Spec requirement | Covered? | Tasklist item anchor (quote) | Notes |
|---|---|---|---|---|
| 1 | §5.1 cmd: behavioral-summary advertises pipeline hardening | Y | Step 2.6 "extend the frontmatter `description:` … and (b) additively append a hardening clause to the `## Behavioral Summary` step" | Maps §5.1 bullet 1 directly. |
| 2 | §5.1 cmd: output description mentions hardening evidence paths | Y | Step 2.7 "additively extend the `--output-dir` Options-row artifact enumeration … lists the pipeline-hardening evidence artifacts" | Maps §5.1 bullet 2. |
| 3 | §5.1 cmd: command stays thin (handoff intact) | Y | Step 2.6 "ADVERTISING ONLY with NO H0-H5 logic … the existing 'keep thin' sentence and Activation handoff remain intact"; Step 4.8 thinness lens | §5.1 bullet 3 + acceptance #1. Double-covered by QA lens. |
| 4 | §5.2 skill: pipeline-hardening trigger after Tier 1, before report closure | Y | Step 2.9 "insert a new `### Wave 4.5: Pipeline Hardening Closure (conditional)` section at the `---` seam between Wave 4 and Wave 5" | "between Wave 4 and Wave 5" = after Tier-1/before Wave-5 report closure. |
| 5 | §5.2 skill: refs/templates for closure cards | Y | Steps 2.1–2.5 create 5 refs; Step 2.10 "append 5 new rows to the `## Refs` registry table" | Hub + 4 gate refs + registration. |
| 6 | §5.2 skill: output-contract extension | Y | Step 2.8a (5 non-gate rows) + Step 2.8b (4 `*_status` + 4 `*_card_path` rows + M7 note) | All 13 fields split across 2.8a/2.8b. |
| 7 | §5.2 skill: failure-state wiring (escape not remediated when gates missing/FAIL/NA-without-rationale) | Y | Step 2.11a completeness gate; Step 2.11b Wave 6 precondition `pipeline_hardening_verdict ∈ {pass, not_applicable}`; Step 2.11c Will-Not-Do bullet; Step 2.14 remediation-handoff | Four-point wiring; strongest area. |
| 8 | §6.1 triggers T1–T9 enumerated | Y | Step 2.1 "reproduce the §6.1 **T1–T9 trigger→gate map** as a raw GFM pipe table" | Hub ref carries full table. |
| 9 | §6.1 trigger→gate map (each trigger pins ≥1 gate) | Y | Step 2.1 trigger→gate table; Step 2.9 "H0 computes the run's **mandatory gate set SOLELY from the §6.1 T1–T9 trigger→gate map**" | Acceptance #13. |
| 10 | §6.1 testable skip rule (`applicable=false` only zero-trigger + boundary scan) | Y | Step 2.1 "skippable ONLY when ZERO triggers T1–T9 fire; record `pipeline_hardening_applicable=false` … AND the boundary scan" | Verbatim from §6.1. |
| 11 | §6.1 trigger-overrides-skip precedence (non-overridable) | Y | Step 2.1 "**trigger-overrides-skip** precedence … 'the symptom looks local' is not a skip basis"; Step 2.9 "trigger-overrides-skip precedence is documented" | §6.1 non-overridable rule. |
| 12 | §6.2 verdict enum exactly `{pass,blocked,not_applicable}` (NO advisory) | Y | Step 2.1 "values exactly `pass | blocked | not_applicable` — NO `advisory`, per C3"; Step 2.8a same | Acceptance #11. Reinforced across many items. |
| 13 | §6.2 per-gate status `{PASS|FAIL|NA|NOT_PROVEN}` | Y | Step 2.8b "each enum `PASS | FAIL | NA | NOT_PROVEN`; default `NA`" | All 4 status fields. |
| 14 | §6.2 status/path rule M7 (path=null only when status∈{NA,NOT_PROVEN}) | Y | Step 2.8b "add the **status/path rule (M7)** as a one-line note"; Step 2.1 hub | Acceptance #14. |
| 15 | §6.2 `gate_na_rationale` (required per NA gate; bare NA ⇒ NOT_PROVEN) | Y | Step 2.8a "`gate_na_rationale` (map[gate→string]; default `{}`; … a `NA` without a rationale entry … MUST be treated as `NOT_PROVEN`)" | Present in hub + report rule too. |
| 16 | §6.2 field defaults | Y | Step 2.8a/2.8b "fold the §6.2 default into the Description cell — `Default: <x>. <meaning>`" | Defaults preserved via 3-col fold (MD056-safe). |
| 17 | §6.2 `known_escapes_caught` pattern `^E\d+$`/`^E\d+\+$` | Y | Step 2.8a "each item MUST match `^E\d+$` or `^E\d+\+$` so `E6+` is valid" | Pattern reproduced. |
| 18 | §6.2 C2 verdict invariant (total function; vacuous-pass closed) | Y | Step 2.1 "`## Verdict invariant` (NEW section reproducing the §6.2 C2 total-function invariant … vacuous-pass-closed)"; Step 2.9 verdict per C2 | Acceptance #12. |
| 19 | §6.2 off-path→verdict invariant M2 (`required ∧ ¬(performed∨waived) ⇒ blocked`) | Y | Step 2.1 "also state the off-path→verdict invariant … (M2)"; Step 2.11b | Co-located on H5 + Wave 6. |
| 20 | §7 H0: applicability decision written before any read | Y | Step 2.1 "`pipeline_hardening_applicable` written before any read"; Step 2.8a default note | §7 H0 required output. |
| 21 | §7 H0: mandatory-gate-set computation (solely from trigger map; incl H5) | Y | Step 2.1 "the firing-trigger set and resulting mandatory gate set computed SOLELY from the §6.1 trigger→gate map"; Step 2.9 | H5-inclusion: see Gap G3 (PARTIAL nuance). |
| 22 | §7 H1: runtime-entrypoint card (13 fields, verbatim) | Y | Step 2.2 "the H1 card reproduced VERBATIM inside a ```text``` fence (all 13 fields exactly as in the spec)" | §9 file #1 new ref. |
| 23 | §7 H1: blocking rule (2 bullets) | Y | Step 2.2 "`## Blocking rule` (the two spec bullets …)" | Includes negative-control bullet. |
| 24 | §7 H1: escapes-caught E1–E5 | Y | Step 2.2 "`## Escapes caught in one shot` (the E1/E2/E3/E4/E5 mappings)" | |
| 25 | §7 H2: contract ledger (9-row table) | Y | Step 2.3 "`## Ledger` containing the 9-row ledger reproduced VERBATIM as a raw GFM pipe table" | §9 file #3 new ref. |
| 26 | §7 H2: consumer-discovery manifest ⇒ NOT_PROVEN if absent (M11) | Y | Step 2.3 "`## Consumer-discovery manifest` … 'absence of the manifest ⇒ H2 `status = NOT_PROVEN`'" | Acceptance #15. |
| 27 | §7 H2: blocking rule (4 bullets) | Y | Step 2.3 "`## Blocking rule` (the four spec bullets …)" | Includes manifest-absence bullet. |
| 28 | §7 H3: unmask-sweep required outputs (10 items) + min regression pattern (4) | Y | Step 2.4 "`## Required outputs` (the 10-item bullet list verbatim), `## Minimum regression pattern` (the 4-item ordered list verbatim)" | §9 file #4 new ref. |
| 29 | §7 H3: E3-style sibling-fixture completion criterion | Y | Step 2.4 "`## Completion criteria` … a passing **E3-style sibling-heading negative fixture** … is an EXPLICIT H3 completion criterion" | Acceptance #15. |
| 30 | §7 H3: fixpoint-after-discovery M9 (re-trigger H0/H2 OR dispositioned follow-up) | Y | Step 2.4 "`## Fixpoint after discovery` (reproduce the §7 H3 M9 paragraph …)" | Acceptance #15. |
| 31 | §7 H3: blocking rule (3 bullets) | Y | Step 2.4 "`## Blocking rule` (the three spec bullets …)" | |
| 32 | §7 H4: effective-input card (10 fields) | Y | Step 2.5 "`## Required proof` (the 'Effective Input Proof' card reproduced VERBATIM inside a ```text``` fence, all 10 fields)" | §9 file #5 new ref. |
| 33 | §7 H4: no-op-vs-empty branch M5 (NA+proof vs FAIL) | Y | Step 2.5 "`## No-op vs empty` (reproduce the §7 H4 M5 both-branches rule …)" | Acceptance #15. |
| 34 | §7 H4: blocking rule (3 bullets) + trigger sentence | Y | Step 2.5 "`## Trigger` (the §7 H4 trigger sentence verbatim) … `## Blocking rule` (the three spec bullets)" | |
| 35 | §7 H5: off-path-reviewer rule, MANDATORY when triggers hold | Y | Step 2.1 "`## Rule H5 — off-path-reviewer` (H5 is MANDATORY when its triggers hold … `off_path_review_decision = required` joins the mandatory gate set …)" | Folded into hub (R-003 §4.6 rationale). |
| 36 | §7 H5: trigger list + acceptable forms + waiver standard | Y | Step 2.1 "then the §7 H5 trigger list + acceptable off-path forms + waiver standard" | |
| 37 | §8 report template: status tokens + rationale + 3-token verdict | Y | Step 2.12 "`## Pipeline Hardening Closure` section … the §8 bullet list EXACTLY as the spec gives it" | §9 file #2 edit (report-template). |
| 38 | §8 report: firing-triggers line + off-path→verdict line | Y | Step 2.12 reproduces "`Firing triggers / mandatory gate set: T... → H...`" and "`Off-path review decision: … ⇒ verdict = blocked`" | Both §8 lines listed verbatim. |
| 39 | §8 report: NOT_PROVEN first-class (not prose) | Y | Step 2.13 "append a `## Pipeline Hardening Closure rule` … `NOT_PROVEN` is a FIRST-CLASS gate status … NOT merely a prose blocker" | After-EOF rule section. |
| 40 | §8 M3/M7 status/path/rationale render rules | Y | Step 2.12 "add the M3/M7 status/path/rationale note" | |
| 41 | §10 acceptance #1 (thin command) | Y | Step 4.8 command-thinness lens; Step 2.6 | See #3. |
| 42 | §10 acceptance #2 (clear trigger + explicit closure verdict) | Y | Step 2.9 Wave 4.5; Step 2.1 hub verdict sections | |
| 43 | §10 acceptance #3 (H1 blocking for the named boundaries) | Y | Step 2.2 H1 ref; Step 2.11a completeness gate | |
| 44 | §10 acceptance #4 (shared-contract ⇒ full ledger) | Y | Step 2.3 H2 ref | |
| 45 | §10 acceptance #5 (parser/gate ⇒ whole-artifact pos + sibling-neg) | Y | Step 2.4 H3 ref completion criteria | |
| 46 | §10 acceptance #6 (any escape fix ⇒ unmask-sweep) | Y | Step 2.4 H3 ref | |
| 47 | §10 acceptance #7 (review gates ⇒ effective-input proof) | Y | Step 2.5 H4 ref | |
| 48 | §10 acceptance #8 (off-path required/waived w/ evidence) | Y | Step 2.1 H5 section | |
| 49 | §10 acceptance #9 (report identifies escapes caught; issue-agnostic closure) | Y | Steps 2.2–2.5 escapes-caught sections; Step 2.12 "Known escapes this would have caught" line | |
| 50 | §10 acceptance #10 (sync/verify-sync pass; .claude not staged) | Y | Step 3.1 sync-dev; Step 3.2 verify-sync; Step 3.4 staging check | |
| 51 | §10 acceptance #11 (enum reconciliation §6.2≡§8, no advisory) | Y | Step 2.12 "DELETE any GF-5/advisory reconciliation wording"; internal-consistency lens 4.3 | OQ2 confirms in-spec resolution. |
| 52 | §10 acceptance #12 (vacuous-pass closed) | Y | Step 2.1 `## Verdict invariant`; Step 2.11a completeness gate | |
| 53 | §10 acceptance #13 (every trigger pins ≥1 gate; H0 set solely from map; H5 mandatory) | Y | Step 2.1 + Step 2.9 | See G3 nuance. |
| 54 | §10 acceptance #14 (per-gate status distinct from path; NOT_PROVEN forces blocked) | Y | Step 2.8b; Step 2.13 | |
| 55 | §10 acceptance #15 (H2 manifest / H3 fixture+fixpoint / H4 no-op) | Y | Steps 2.3, 2.4, 2.5 | |
| 56 | §9 file edit: `commands/troubleshoot.md` | Y | Steps 2.6, 2.7 | |
| 57 | §9 file edit: `SKILL.md` | Y | Steps 2.8a, 2.8b, 2.9, 2.10, 2.11a, 2.11b, 2.11c | |
| 58 | §9 file edit: `refs/report-template.md` | Y | Steps 2.12, 2.13 | |
| 59 | §9 file edit: `refs/remediation-handoff.md` | Y | Step 2.14 | |
| 60 | §9 new ref: `pipeline-hardening-closure.md` | Y | Step 2.1 | |
| 61 | §9 new ref: `runtime-entrypoint-verification.md` | Y | Step 2.2 | |
| 62 | §9 new ref: `contract-enumeration.md` | Y | Step 2.3 | |
| 63 | §9 new ref: `unmask-and-sweep.md` | Y | Step 2.4 | |
| 64 | §9 new ref: `effective-input-proof.md` | Y | Step 2.5 | |
| 65 | Validation: make sync-dev | Y | Step 3.1 | |
| 66 | Validation: make verify-sync ("✅ All components in sync.") | Y | Step 3.2 | |
| 67 | Validation: markdownlint on edited/new src .md | Y | Step 3.3 | 9 source files. |
| 68 | Validation: no .claude staging | Y | Step 3.4 | |
| 69 | §4 six rejected proof substitutions (verbatim, gate-mapped) | Y | Step 2.1 "`## Rejected proof substitutions` (the §4 six-item numbered list VERBATIM, each item mapped to the gate …)" | §4 is a spec normative list; not in coverage-target enumeration but is a fidelity requirement. |
| 70 | §3 / §11 E1–E5 one-shot coverage assertion | PARTIAL | Steps 2.2–2.5 escapes-caught sections; no item reproduces the §3 escape table or §11 justification narrative | See Gap G1. The escapes-caught bullets per gate exist, but the §3 "canonical escapes this must catch in one shot" table and the §11 closure-question list (the 6 reusable invariants) have no dedicated reproduction item. |

## Gap Registry

### G1 — §3 escape table + §11 justification narrative not explicitly reproduced — MINOR

The spec's §3 ("Canonical escapes this must catch in one shot" — the E1–E5 failure-shape/catcher
table) and §11 (the 6 reusable closure-question invariants + "catches E1..En in one shot"
rationale) have no tasklist item that reproduces them as a block. Coverage is indirect: each gate
ref's `## Escapes caught in one shot` bullets (Steps 2.2–2.5) carry the per-escape mappings, and the
hub's `## Rejected proof substitutions` (Step 2.1) carries §4. But the *issue-agnostic coverage
assertion* called out in acceptance #9 ("the closure definition asserts issue-agnostic coverage") is
only weakly anchored — Step 2.1 hub sections do not explicitly require a "catches E1..En by
invariant, not by patch" statement drawn from §11. [INFERRED] the Task Overview narrative (lines
61–65) conveys this intent, so a faithful builder will likely include it, but no checklist item
*forces* the §11 invariant list into output. Severity MINOR because the operative mechanism (the
gates themselves) is fully covered; only the meta-justification prose is at risk of omission.

### G2 — §8 "Severity/blast-radius decision" line covered, but H3 "Severity cost review" cross-wiring not asserted — MINOR

§8 report block includes a `Severity/blast-radius decision:` line, and §7 H3 required-outputs item
10 is "Severity cost review for hard gates." Step 2.12 reproduces the §8 line and Step 2.4 reproduces
the H3 10-item list (which includes severity cost review). Both endpoints are covered. The gap is
only that no item explicitly *links* the §8 severity line to the H3 severity-cost output — they are
covered independently but a reader could leave them disconnected. Severity MINOR (both required
elements are present; only their cross-reference is unasserted). No action strictly required.

### G3 — H5-in-mandatory-gate-set computation: covered in hub prose, lighter in Wave 4.5/completeness-gate — MINOR

§6.1 mandatory-gate rule and §7 H0 state the mandatory gate set is "the union of pinned gates over
all firing triggers" PLUS "H5 when any §7-H5 trigger holds." Step 2.1 (hub) reproduces this fully
(H5 "joins the mandatory gate set"). Step 2.9 (Wave 4.5) says H0 computes the set "SOLELY from the
§6.1 T1–T9 trigger→gate map" — which is literally true for T1–T9 but the §6.1 map table does NOT
contain an H5 column (H5 is pinned by a *separate* rule, "H5 is additionally mandatory whenever any
§7-H5 trigger condition holds," spec line 98). Step 2.11a (completeness gate) requires "EVERY gate in
the run's mandatory gate set has `status=PASS`" — correct only if that set *includes* H5 when its
triggers fire. The off-path→blocked invariant (Step 2.11b, 2.1) does enforce H5 independently, so the
verdict cannot be `pass` with an unsatisfied required off-path review. Net: H5's mandatory force is
preserved via the off-path→verdict invariant even if the "mandatory gate set" phrasing in Step 2.9 is
read narrowly. Severity MINOR — no functional escape, but the Step 2.9 wording "SOLELY from the
trigger map" risks a builder under-including H5 in the H0-computed set unless they also read the
separate H5 rule. Recommend the builder explicitly note "plus H5 when its §7-H5 triggers hold" in the
Wave 4.5 H0 step. (This is a robustness nit, not a coverage gap — H5 IS covered by item 35/19.)

### G4 — §6.1 mandatory-gate rule "union of pinned gates" + C2 "reads the mandatory gate set" — Y but worth flagging — not a gap

Verified covered: Step 2.1 hub `## Trigger` states "the union over all firing triggers is the run's
mandatory gate set, which the C2 verdict invariant reads." No gap. Listed only to confirm the C2↔H0
linkage (the most escape-prone invariant) is explicitly wired.

## Coverage Summary

- Total requirements assessed: **70** (matrix rows 1–70; row 71 is the §3/§11 assertion).
- Including row 71 (the E1–En one-shot assertion): **71** total.
- Covered (Y): **70**.
- PARTIAL: **1** (row 71 / G1).
- N (uncovered): **0**.

**coverage_pct = 70 / 71 = 0.986** (counting the single PARTIAL as not-fully-covered).

If PARTIAL is counted as half-covered: 70.5 / 71 = 0.993. Stated conservatively, **coverage_pct ≈ 0.986**.

## Gap count

- CRITICAL: 0
- IMPORTANT: 0
- MINOR: 3 (G1, G2, G3) — G4 is a confirmation, not a gap.
- Total gaps: **3 (all MINOR)**.

## Verdict (coverage lens)

The tasklist provides full, item-level coverage for every normative spec requirement in the
coverage-target set: all 9 §9 files (4 edits + 5 refs), the entire §6.2 13-field output contract,
all §7 H0–H5 waves/gates with their cards/ledgers/blocking-rules, the §8 report block, every §6.1
trigger/skip/precedence rule, and all 15 §10 acceptance criteria. The C2 verdict invariant,
vacuous-pass closure, NOT_PROVEN-as-first-class, H2 manifest, H3 fixture+fixpoint, H4 no-op-vs-empty,
and H5-mandatory/off-path→blocked invariants each map to a concrete checklist item. Validation
(sync/verify-sync/markdownlint/staging) is fully covered. The only shortfalls are three MINOR
prose/cross-wiring nits (G1 §11 justification narrative not item-forced; G2 §8↔H3 severity
cross-link unasserted; G3 Step 2.9 "SOLELY from trigger map" wording could under-include H5 in the
H0-computed set, though H5 is independently enforced via the off-path→verdict invariant). None block
execution; none represent an uncovered requirement that would let a spec invariant escape.

## Self-confidence

**0.88**

Calibration basis: I read the spec in full (§1–§12) and the entire tasklist (frontmatter, Phases
1–5, Post-Completion, lines 1–399). Mappings are anchored to literal Step quotes and § references.
Confidence is held below 0.90 because: (a) I assessed the tasklist's *instructions to produce*
content, not produced artifacts (UC-1 is necessarily pre-execution, so fidelity of the eventual
output to byte-faithful spec templates is asserted by the items but unverifiable here); (b) the 5 new
refs and 4 edits do not yet exist on disk, so anchor-text correctness for the edit items (Steps
2.6–2.14) rests on the discovery inventory the tasklist itself generates (Step 1.4), not on my own
read of the live edit-target files; (c) research files R-001..R-007 are cited by the items but I did
not independently read them to confirm the house-style/insertion-seam claims. The three MINOR gaps
are low-confidence-to-matter (prose/cross-wiring), so even if mis-severitized they do not change the
"fully covered, execute" conclusion.
