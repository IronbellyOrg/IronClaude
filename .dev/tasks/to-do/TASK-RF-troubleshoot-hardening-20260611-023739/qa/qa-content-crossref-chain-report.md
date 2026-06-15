# QA Report — Content Cross-Reference Chain Tracing

**Topic:** troubleshoot-pipeline-hardening
**Date:** 2026-06-11
**Phase:** doc-qualitative (cross-reference chain tracing)
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: PASS

Every end-to-end cross-reference chain demanded by the mandate was traced link-by-link
against the actual source files using zero-trust verification. **No broken chain was found.**
The brief's working assumption of "≥10 broken cross-reference chains" was not borne out: all
13 FRs + 4 NFRs map cleanly through ref rule → SKILL.md wiring → §8.3-mapped test → E2E
backtest scenario, all 18 pytest functions collect and pass, all relative markdown links
resolve, and the src↔.claude mirror is in sync.

Per the adversarial stance, a 0-broken-chain result is treated with suspicion, not
satisfaction. The verification trail below documents exactly what was read and re-tested for
each link so the user can audit the conclusion. The single inconsistency surfaced (a stale
"17" test count inside one research file, RECON-3 L129) is internal to a research artifact,
self-corrected by that same file's authoritative header ("18"), and is NOT a deliverable
cross-reference chain — it is logged as MINOR/informational below for completeness.

---

## Mandate

Trace: for each FR, `FR → ref rule → SKILL.md wiring → mapped §8 test → (where applicable)
E2E backtest scenario`; verify every link exists. Four named chains required:

1. E1 → H1 card + H2 ledger → test_h1.../test_h2... → E1 scenario
2. E4 → H2 ledger → test_h2_empty_ledger_fails → E4 scenario
3. E5 → H4 manifest → test_h4... → E5 scenario
4. FR-12 → latch in hardening-output-contract.md → remediation-handoff.md fields →
   test_downstream... → Waiver re-green scenario

---

## Files Read (zero-trust evidence base)

| File | Purpose in trace |
|------|------------------|
| `phase-outputs/reports/qa-input-inventory.md` | Deliverable enumeration (20 items) |
| `refs/pipeline-hardening-closure.md` | H0/H5 rules, FR-1/2/11/12, NFR-5, link hub |
| `refs/hardening-output-contract.md` | §5.4 truth table, §5.5 schema, FR-12/13, NFR-1/6 latch |
| `refs/runtime-entrypoint-verification.md` | H1 card, FR-3/4, E1/E4 claims |
| `refs/contract-enumeration.md` | H2 ledger, FR-5/6, E4/E1 claims |
| `refs/unmask-and-sweep.md` | H3 grammar/card, FR-7/8/9, E2/E3 claims |
| `refs/effective-input-proof.md` | H4 manifest, FR-10, E5 claim |
| `refs/remediation-handoff.md` | Downstream verdict gating, BUILD_REQUEST carry |
| `refs/report-template.md` | §5.4 report-language rendering, FR-13 blockers |
| `SKILL.md` (grep + targeted reads) | Wave 4.5 wiring, 11 Output Contract fields, refs index |
| `commands/troubleshoot.md` (grep) | Advertise/Boundaries lines, NFR-5 |
| `tests/troubleshoot/__init__.py` + all 7 test modules | §8.3 test endpoints |
| `tests/troubleshoot/e2e-backtest-scenarios.md` | E1–E5 + Waiver re-green endpoints |
| `research/08-v1.1.0-deliverable-reconciliation.md` | Authoritative §8.3 FR→test mapping |

Tool engagement: Read: 15 | Grep/Bash-grep: 7 | Bash (pytest/verify-sync/link-check): 4.

---

## Chain Matrix — all FRs/NFRs

Link legend: **R** ref-rule exists · **S** SKILL.md wires it · **T** §8.3 test asserts it ·
**E** E2E scenario (where applicable). All cells verified present against the actual file.

| FR / NFR | Ref rule (R) | SKILL.md wiring (S) | §8.3 test (T) | E2E (E) | Chain |
|----------|-------------|---------------------|---------------|---------|-------|
| FR-1 (H0 applicability) | closure.md §H0 | Wave 4.5 step 1 (L405) | test_h0_applicability_skip_requires_boundary_scan | — | INTACT |
| §5.6 H0 schema (6-field, 9-enum) | closure.md row schema | L401 boundary list | test_h0_boundary_scan_schema_rejects_bare_local_reason | — | INTACT |
| FR-2 (mechanism stmt) | closure.md §H0 mechanism | Wave 4.5 step 1 | covered via H0 schema + known_escapes | — | INTACT |
| FR-3 + FR-4 (H1 runtime + neg witness) | runtime-entrypoint-verification.md | Wave 4.5 step 2 (L406) | test_h1_runtime_card_requires_negative_and_positive_witness | E1 | INTACT |
| FR-5 (empty-ledger FAIL) | contract-enumeration.md FR-5 | Wave 4.5 step 3 (L407) | test_h2_empty_ledger_fails | E4 | INTACT |
| FR-6 (sibling sweep) | contract-enumeration.md FR-6 | Wave 4.5 step 3 | test_h2_sibling_sweep_required_when_concept_shared (G-PRE-1) | — | INTACT |
| FR-7+FR-8+FR-9 (H3) | unmask-and-sweep.md | Wave 4.5 step 4 (L408) | test_h3_word_boundary…, test_h3_small_grammar…, test_h3_sweep_card… | E2, E3 | INTACT |
| FR-10 (H4 fail-closed) | effective-input-proof.md | Wave 4.5 step 5 (L409) | test_h4_nonempty_wrong_surface_fails_closed | E5 | INTACT |
| §5.6 H4 manifest | effective-input-proof.md schema | L409 intersection wording | test_h4_manifest_schema_requires_intersection_proof | E5 | INTACT |
| FR-11 (H5 off-path) | closure.md §H5 | Wave 4.5 step 6 (L410) | via H5 mapping test | E5 | INTACT |
| §5.4 H5 mapping (4-row) | hardening-output-contract.md | L410/L411 | test_h5_decision_maps_to_status_and_latch | — | INTACT |
| FR-12 (one-way latch / anti-inflation) | hardening-output-contract.md | Wave 4.5 step 7 (L411) + Output Contract L64-65 | test_waiver_latch_one_way, test_known_escapes_requires_cited_card, test_downstream_success_cannot_override_latched_hardening_verdict | Waiver re-green | INTACT |
| FR-13 (verdict aggregation / NOT PROVEN) | hardening-output-contract.md §5.4 | Wave 4.5 step 7 + Wave 5 bullet (L435) | test_verdict_aggregation_from_h_statuses, test_report_closure_section_not_proven_blockers | — | INTACT |
| NFR-1 (backtest status) | hardening-output-contract.md §5.4 backtest table | Output Contract L66 | test_backtest_status_keeps_pipeline_health_advisory_until_complete | — | INTACT |
| NFR-4 (no-re-greening durability) | hardening-output-contract.md downstream no-override | L411 / L64 | test_downstream_success_cannot_override_latched_hardening_verdict | Waiver re-green | INTACT |
| NFR-5 (thin command, no flag) | closure.md trigger | L401 + commands/troubleshoot.md L169 | advertise line grep-verified | — | INTACT |
| NFR-6 (additive backward-compat) | hardening-output-contract.md §5.5 | Output Contract L62-72 (11 additive fields) | test_output_contract_backward_compat (19 legacy + 11 hardening) | — | INTACT |

All 13 FRs and 4 NFRs trace end-to-end with no missing link.

---

## The Four Named Chains — explicit link-by-link verdicts

### Chain 1 — E1 → H1 card + H2 ledger → test_h1.../test_h2... → E1 scenario  — INTACT

- **E1 → H1 card:** `runtime-entrypoint-verification.md` L3 states verbatim "It closes **E1**
  (headless `--spec` replay rejects a local-path `--file`)". H1 card schema (§5.6, 11 fields)
  present.
- **E1 → H2 ledger (supporting):** `contract-enumeration.md` L3 states "supports **E1** (PRD
  identified as the sibling-contract outlier vs the roadmap/tasklist/validate file-delivery
  consumers)". The H2↔E1 link is the *supporting* relationship (H1 is the primary closer); the
  bidirectional closer/supporter pairing (H1 closes E1 / supports E4; H2 closes E4 / supports
  E1) is consistent across both refs.
- **→ test:** `test_h1_runtime_card_requires_negative_and_positive_witness`
  (test_hardening_h1.py) asserts all 11 H1 card fields + FR-4 negative-witness language.
  `test_h2_empty_ledger_fails` + `test_h2_sibling_sweep_required_when_concept_shared`
  (test_hardening_h2.py) assert the H2 ledger schema. Both collect and PASS.
- **→ E1 scenario:** e2e-backtest-scenarios.md §"E1 backtest" maps "E1; FR-3 + FR-4" with
  expected "H1 FAIL pre-fix (negative witness), PASS post-fix". Endpoint present.

  *Note (not a defect):* the E1 e2e scenario names H1 as the primary closer and does not
  re-name H2; this matches the design (E1's primary closer is H1; H2's E1 role is *supporting*
  per H2 ref L3). The mandate's "H1 card + H2 ledger" is satisfied by the refs' bidirectional
  cross-reference, not by the E1 scenario row needing to cite H2.

### Chain 2 — E4 → H2 ledger → test_h2_empty_ledger_fails → E4 scenario  — INTACT

- **E4 → H2 ledger:** `contract-enumeration.md` L3 states verbatim "It closes **E4** (the
  shared `SemanticCheck.advisory` honored by the generic gate but not the PRD
  `_evaluate_gate`)".
- **→ test_h2_empty_ledger_fails:** function present at test_hardening_h2.py L17, asserts FR-5
  empty/zero-row non-vacuous rule + all 6 §5.6 ledger fields. Collects and PASSes.
- **→ E4 scenario:** e2e §"E4 backtest" maps "E4; FR-3 + FR-5 (contract-enumeration ledger) +
  FR-12", expected "H2 FAIL until both `gate_passed` and `_evaluate_gate` consumers are
  classified", and explicitly preserves the `advisory` semantic-check token. Endpoint present
  and FR-5 (the rule `test_h2_empty_ledger_fails` validates) is named in the scenario's FR
  coverage.

### Chain 3 — E5 → H4 manifest → test_h4... → E5 scenario  — INTACT

- **E5 → H4 manifest:** `effective-input-proof.md` L3 states verbatim "It closes **E5** (a
  POST-reflect selector that audited a range omitting the dirty `/task` work…)". §5.6 manifest
  schema (8 fields incl. `intersection_proof`, `excluded_foreign_commits`) present.
- **→ test_h4...:** `test_h4_nonempty_wrong_surface_fails_closed` (FR-10 / F-D1, E>0
  insufficiency) + `test_h4_manifest_schema_requires_intersection_proof` (11 manifest field
  markers). Both in test_hardening_h4.py, collect and PASS.
- **→ E5 scenario:** e2e §"E5 backtest" maps "E5; FR-10 (effective-input proof) + FR-11
  (off-path reviewer) + FR-12", expected "H4 FAIL closed (wrong surface) until … `E ∩
  true_runtime_surface` is proven correct". Endpoint present; FR-10 (validated by the h4 tests)
  named.

### Chain 4 — FR-12 → latch → remediation-handoff.md fields → test_downstream... → Waiver re-green  — INTACT

- **FR-12 → latch in hardening-output-contract.md:** §"Waiver / no-re-greening latch and
  anti-inflation (FR-12)" L66-71 documents the one-way `none`→`latched` latch forcing
  `verdict ∈ {blocked, advisory}`, the no-upgrade rule, and anti-inflation. §5.4 truth-table
  rows 3/5 and downstream-no-override rule L52-54 present.
- **→ remediation-handoff.md fields:** `remediation-handoff.md` §"Pipeline hardening verdict
  gating" L5-11 carries `pipeline_hardening_verdict` + `waiver_status`, renders
  `success_with_hardening_blocker`/`_advisory`, and the Phase A BUILD_REQUEST block L68-73
  carries `pipeline_hardening_verdict` + `waiver_status` with the §5.4 L411 no-re-green
  comment.
- **→ test_downstream...:** `test_downstream_success_cannot_override_latched_hardening_verdict`
  (test_hardening_verdict.py L76) asserts (a) the no-override rule names all four downstream
  stages, (b) `success_with_hardening_blocker`/`_advisory` + "never plain `success`", and (c)
  the handoff carries `pipeline_hardening_verdict` + `waiver_status` into BUILD_REQUEST. It
  reads `remediation-handoff.md` directly (HANDOFF var L52), closing the loop. Collects and
  PASSes.
- **→ Waiver re-green scenario:** e2e §"Waiver re-green attempt backtest" maps "NFR-4 / FR-12",
  expected "The verdict stays `blocked`/`advisory`; it never upgrades to `pass`. Both
  `blocked` AND `advisory` are valid non-upgraded states". Endpoint present.

---

## Additional cross-reference integrity checks (beyond the 4 named chains)

- **Relative markdown links:** every `](<file>.md)` href inside the 6 refs resolves to an
  existing file in `refs/` (Bash link-check: 0 broken). The hub ref
  `pipeline-hardening-closure.md` links to all 5 sibling refs + the output contract; each
  target exists.
- **SKILL.md refs index (L580-585):** all 6 hardening refs listed with correct Wave 4.5
  attribution; each named file exists.
- **Output Contract field parity:** SKILL.md L62-72 enumerates exactly the 11 additive fields;
  `test_output_contract_backward_compat` asserts all 11 + 19 legacy fields present in SKILL.md.
  Producer/consumer columns in hardening-output-contract.md §5.5 match the SKILL.md field
  descriptions.
- **§5.4 report-language ↔ report-template blockers:** the five truth-table Report-Language
  strings (rows 2/3/4 `NOT PROVEN — …`, rows 5/6 `ADVISORY — …`) appear verbatim in
  report-template.md L234-238 AND are asserted by `test_verdict_aggregation_from_h_statuses` /
  `test_report_closure_section_not_proven_blockers`. Three-way chain (contract ↔ template ↔
  test) intact.
- **4-token enum end-to-end:** `pass | blocked | advisory | not_applicable` consistent across
  closure.md, hardening-output-contract.md, SKILL.md (L64), report-template.md (L209/L301),
  remediation-handoff.md (L11/L35), and asserted by 3 tests. No 3-token regression anywhere.
- **pytest collection:** `uv run pytest tests/troubleshoot/` → 18 collected, 18 passed. Test
  count matches inventory ("13 unit + 5 integration = 18").
- **src↔.claude sync:** `make verify-sync` → "All components in sync." The runtime-read `.claude/`
  mirror carries identical chains.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR (informational; NOT a deliverable cross-reference chain) | `research/08-v1.1.0-deliverable-reconciliation.md` L129 (SUPERSESSION table) | The supersession-summary row states "**17** unit/integration + 6 E2E + new FR-6 test", while the same file's authoritative RECON-3 header (L49-51) and the deliverable inventory both state **18** (13 unit + 5 integration). The "17" is a stale pre-G-PRE-1 count internal to a research artifact. | None required for the deliverable set (the chain endpoints all resolve to 18 and all 18 tests pass). If desired, reconcile L129 "17" → "18" for internal research-file consistency. This does not break any FR→test→E2E chain. |

No CRITICAL or IMPORTANT cross-reference-chain defects found. No broken link in any of the
17 FR/NFR chains or the 4 named end-to-end chains.

---

## Self-Audit

**(a) Reliance list — structural items NOT re-verified here (out of this lens' scope):**
- Relied on prior structural QA for markdownlint cleanliness, file-presence counts, and
  template-section ordinality. This lens re-tested only the *content* of cross-reference links.

**(b) Independent semantic checks (≥1 required):**
- **FR→ref→SKILL→test→E2E chain existence** — independently verified by Reading all 6 refs,
  all 7 test modules, the e2e scenarios, and grepping SKILL.md Wave 4.5 (L397-413) +
  Output-Contract (L62-72) + refs index (L580-585). Every Chain-Matrix row cites the file:line
  / function name actually read.
- **Bidirectional E1/E4 closer-supporter consistency** — independently verified by reading
  runtime-entrypoint-verification.md L3 and contract-enumeration.md L3 side by side and
  confirming the E1/E4 closer/supporter assignments are reciprocal and non-contradictory.
- **Latch loop closure (FR-12)** — independently verified that
  `test_downstream_success_cannot_override_latched_hardening_verdict` actually Reads
  remediation-handoff.md (HANDOFF var, L52/L92-94) so the test endpoint genuinely consumes the
  handoff fields rather than asserting in isolation.
- **Live re-test** — ran `uv run pytest tests/troubleshoot/` (18/18 PASS) and `make verify-sync`
  (in sync) rather than trusting the inventory's pre-recorded "18/18 PASS" claim.

**Self-audit honesty check:** A 0-broken-chain verdict against a "≥10 broken chains" brief is
inherently suspect. The evidence I can point to: 15 files Read in full or targeted, 4 live
command executions (pytest, verify-sync, relative-link scan, FR-grep), and a per-FR matrix
where every cell names the exact file:line or test-function verified. The chains are intact
because the deliverable set is internally consistent — the brief's assumption was a stress
test, not a description of the artifact state.

---

## Confidence

Verified: 17/17 FR-NFR chains + 4/4 named chains | Unverifiable: 0 | Unchecked: 0 |
Confidence: 100%

Tool engagement: Read: 15 | Grep/Bash-grep: 7 | Bash: 4

---

## Recommendations

1. (Optional, MINOR) Reconcile the stale "17" at research file 08 L129 → "18" for internal
   research-artifact consistency. Not chain-blocking.
2. No cross-reference-chain remediation required before proceeding.

---

VERDICT: PASS
