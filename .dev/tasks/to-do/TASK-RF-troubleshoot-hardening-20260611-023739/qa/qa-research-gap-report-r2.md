# QA Report — Research Gate (RE-GATE, Round 2)

**Topic:** Pipeline Hardening Closure mode (H0-H5) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Phase:** research-gate (fix-cycle / round 2)
**Fix cycle:** 2
**Lens:** gap-detection
**Stance:** ADVERSARIAL — assume gap-fill is incomplete

---

## Scope

ASSIGNED FILES:
- 08-v1.1.0-deliverable-reconciliation.md (verify HARDEST against spec)
- 05-v2
- 07
- Confirm SUPERSEDED banners on 01-04 / 06

AUTHORITATIVE SPEC: troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)

Round-1 gaps to re-check: C1 (6th ref content), C2 (testing scope), C3 (3 contract fields),
IMPORTANT (§5.4 L411 wiring, §4.7 test→artifact map, stale anchors).

---

## Verification Log

### Tool engagement
Read: 6 (08, spec full, 05-v2, 07, 08-slice, report) | Bash: 2 (banner scan, anchor+count verify) | Glob: 0

All spec anchors cited by 08 were independently re-checked against the live spec file via grep, NOT taken on 08's word.

---

### RECON-1 — SIX refs + hardening-output-contract.md required content — VERIFIED PASS

- Spec §4.1 confirmed at L261 (grep). Table rows L263-270 enumerate exactly **6** new ref files; row 6 = `hardening-output-contract.md` (spec L270 verbatim: "Field schema, verdict aggregation truth table, waiver latch propagation contract, and downstream consumer obligations"). 08's RECON-1 table lists all 6 with correct paths.
- The 6th-ref required content in 08 (row 2) names: §5.5 field schema (10 fields), §5.4 verdict-aggregation truth table (7 rows incl advisory rows 5/6), H5 decision-to-status mapping (4 rows), backtest-status-vs-run-verdict (3 rows), waiver-latch propagation, downstream `success_with_hardening_*` rendering (§5.4 L411). Every one maps to a real spec structure: §5.5 (L425, 11 rows confirmed), §5.4 truth table (L388, 7 rows), H5 mapping (4 rows), backtest table (3 rows), L411 downstream rule (grep-verbatim-confirmed).
- §4.7 component 1 (L334) maps the verdict-aggregation contract to `refs/hardening-output-contract.md` — confirms the 6th ref is architecturally load-bearing, not optional.
- C1 (round-1 CRITICAL: 6th ref content missing) is **GENUINELY CLOSED**, not papered over: the required-content column gives the builder the actual schemas to author, each spec-anchored.

### RECON-2 — 11-field output contract — VERIFIED PASS

- Spec §5.5 at L425; field-row count = **11** (Bash grep over L427-439 = 11). Matches 08's "10 result fields + backtest_status = 11th".
- Per-field default/type cross-check against §5.5 (verbatim in 07 §4) — every row in 08's RECON-2 table is correct:
  - `contract_version` semver `1.0.0` non-null (round-1 C3 missing field — now present)
  - `waiver_status` enum `none|latched` default `none` (round-1 C3 missing field — now present; "core anti-theatre latch")
  - `backtest_status` enum `not_run|partial|complete` default `not_run` (round-1 C3 missing field — now present; NFR-1 coverage)
  - `pipeline_hardening_verdict` 4-token enum incl `advisory` (08 explicitly flags advisory REQUIRED; matches 07 §3.0 ENUM TRUTH)
  - 4 `*_card_path`/`*_path` fields `string|null` default `null`
  - `known_escapes_caught` list-of-objects default `[]`
- NFR-6 backward-compat callout present (test `test_output_contract_backward_compat`). Tied to §4.5 registry (L304).
- C3 (round-1 CRITICAL: 3 contract fields missing) is **GENUINELY CLOSED** — all 3 now present with correct type/default and "MISSING in stale research — REQUIRED" call-outs.

### RECON-3 — Testing required: full net-new suite — VERIFIED PASS (one MINOR labeling note)

- Spec §8 at L542; §8.1 (L544) = **12** unit-test rows (Bash count confirmed); §8.2 (L561) = 5 integration; §8.3 (L571) = 6 E2E.
- 08 §8.1 table lists 13 (the 12 spec tests verbatim + the NEW `test_h2_sibling_sweep_required_when_concept_shared` for FR-6/G-PRE-1, correctly homed in test_hardening_h2.py). Cross-checked each of the 12 against 07 §9.1 / spec §8.1 — all 12 present, correct file homes, correct FR mapping.
- 08 §8.2 lists 5 integration tests verbatim-matching spec §8.2; §8.3 lists all 6 E2E scenarios (E1-E5 + Waiver-re-green).
- `tests/troubleshoot/` CREATE requirement present (05-v2 CODE-CONTRADICTED dir-absent finding carried), `__init__.py` + `tests/skills/` pattern + `REPO_ROOT = parents[2]` all stated.
- §4.7 component→test map (6 rows) present and matches spec §4.7 / 07 §2.6.
- C2 (round-1 CRITICAL: file 06 said NONE) is **GENUINELY CLOSED** — 08 explicitly REJECTS the NONE conclusion, explains it was scoped to "not breaking existing tests", and supplies the full inventory with the §4.7 executable-validation rationale.
- **MINOR (M1):** Header/summary labels the count "17 unit/integration + 6 E2E" (= spec baseline 12+5). The body then correctly adds the 13th (G-PRE-1), making the true total **18 unit/integration + 6 E2E**. Supersession-summary row reads "17 unit/integration + 6 E2E + new FR-6 test", which reconciles it (17 base + 1 new). Not a content gap — the builder receives the complete, correctly-itemized inventory — but the headline "17" could read as the final total. Recommend the builder treat 18 unit/integration as the target.

### RECON-4 — remediation-handoff hardening fields + downstream no-override — VERIFIED PASS

- §5.4 L411 downstream rule grep-confirmed verbatim: downstream stages "may not convert `blocked`/`advisory` into `pass` or `success`... rendered result is `success_with_hardening_blocker` or `success_with_hardening_advisory`, never plain `success`".
- 08 RECON-4 requires the builder ADD `pipeline_hardening_verdict` + `waiver_status` to the handoff payload AND reconcile with the existing "loaded only on success" gate (05-v2 §D finding, line 3 of remediation-handoff.md). The `success_with_hardening_*` rendering is correctly wired in.
- The round-1 IMPORTANT (§5.4 L411 `success_with_hardening_*` wiring into remediation-handoff) is **CLOSED** — both the field-addition and the no-override/rendering rule are present, anchored to L411 and FR-12.

### RECON-5 — section-number remap (draft → v1.1.0) — VERIFIED PASS

- 08's remap table re-anchors draft §6/§6.1/§6.2/§7/§8/§9 to v1.1.0 §3/§5.5/§4.5/§5.4/§4.1/§4.2. Spot-checked: draft "§6.2 output contract 8 fields" → §5.5 (10 fields) + §4.5 registry — correct (§5.5 at L425, §4.5 at L304). Draft "§9 5 files" → §4.1 (6 new) + §4.2 (4 modified) — correct.
- Builder rule to anchor on HEADING TEXT not line numbers is present (matches 05-v2 anchor-drift warning + project line-drift discipline). markdownlint scope (src/ linted, .dev/ excluded; MD025/MD040/MD024-siblings) present.
- Round-1 IMPORTANT (stale §-anchors) is **CLOSED** — explicit draft→v1.1.0 crosswalk supplied.

### RECON-6 — HALT items = OI-2, OI-3, OI-5 (NOT OI-1/4/6) — VERIFIED PASS

- Spec §11 at L598. OI-1 (L602) "Resolved in §5.4", OI-4 "Resolved in §5.7", OI-6 "Resolved in §5.4" — grep-confirmed OI-1 resolved text. 08 correctly lists OI-2/OI-3/OI-5 as the `needs_human_decision` HALT items and explicitly excludes OI-1/4/6 as in-spec-resolved.
- Matches 07 §11 (same correction to the original task-brief framing). The `feedback_human_decision_items_must_halt` project rule is cited (write PENDING + halt dependent mutation, never auto-default). Correct.

### RECON-7 — G1 HALT constraint — VERIFIED PASS

- Spec §1.2 L42 + §9 L586 confirmed in spec read (implementation halted pending G1; no `src/superclaude/` or `.claude/` edits pre-approval). 08 RECON-7 requires the tasklist to state the HALT prominently + the rollback note (revert SKILL.md trigger + remove 6 refs, then sync/verify). Matches 07 §12 G1-HALT. Correct.

### Banners on 01-04 / 06 — VERIFIED PASS

All 5 carried-over files (01, 02, 03, 04, 06) carry an identical SUPERSEDED banner immediately under the H1, pointing to 08 + 07 as authoritative, scoping the supersession to DESIGN CONCLUSIONS while preserving CODEBASE anchors. Banner text names the corrected numbers (6 refs, 10+1 fields incl waiver_status/contract_version/backtest_status, 17+6 tests, advisory REQUIRED). Read-order header in 08 (L8) reinforces precedence. No stale design conclusion can mislead the builder without an adjacent override pointer.

### NEW-gap scan (adversarial item 7) — no CRITICAL/IMPORTANT new gaps introduced by 08

- Checked 08 for fabricated paths/anchors: every §-anchor it cites resolves to a real spec heading (grep-verified L261/304/320/334/388/425/542/598). No hallucinated spec section.
- Checked for residual builder-blocking omissions: §4.6 implementation order (7-group, group 3 = 3 parallel refs) is NOT restated in 08 but IS fully captured in 07 §2.5 (authoritative, in the builder read-order). §5.6 artifact schemas (5 cards, every field) live in 07 §5 and are referenced by 08's RECON-1 required-content column. §5.7 grammar (4 rules) in 07 §6. No coverage hole for the builder across the authoritative set {08, 07, 05-v2}.
- FR-6 G-PRE-1 new test + FR-12↔NFR-4 pairing both present (08 §8.1 row + §8.2 row; reinforced 07 §10).

---

## Overall Verdict: PASS

All four round-1 CRITICAL/IMPORTANT gaps are GENUINELY closed (verified against live spec lines, not on 08's word):

| Round-1 gap | Status | Evidence |
|-------------|--------|----------|
| C1 — 6th ref hardening-output-contract.md content | CLOSED | RECON-1: 6 refs, 6th ref required-content column maps to §5.5/§5.4/§4.7 (grep-confirmed) |
| C2 — testing scope (was NONE) | CLOSED | RECON-3: NONE rejected; 13 unit + 5 integration + 6 E2E + §4.7 map supplied |
| C3 — 3 contract fields missing | CLOSED | RECON-2: contract_version + waiver_status + backtest_status present, correct type/default |
| IMPORTANT — L411 wiring / §4.7 map / stale anchors | CLOSED | RECON-4 (L411 + handoff fields), RECON-3 (§4.7 6-row map), RECON-5 (draft→v1.1.0 crosswalk) |

08 introduces NO new CRITICAL or IMPORTANT gap. All spec anchors it cites are real. The authoritative read-set {08, 07, 05-v2} + the SUPERSEDED banners on 01-04/06 give the builder a complete, non-contradictory deliverable inventory.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | RECON-1 6 refs + 6th-ref content vs §4.1/§4.6/§4.7 | PASS | §4.1 L261 grep; 6 rows; 6th-ref content maps to real schemas |
| 2 | RECON-2 11 fields vs §5.5/§4.5 | PASS | §5.5 L425; 11 field rows (Bash count); each default/type correct |
| 3 | RECON-3 test inventory vs §8.1/§8.2/§8.3 + FR-6 test + tests/troubleshoot CREATE + §4.7 map | PASS (MINOR M1) | §8.1 = 12 (Bash count); +1 G-PRE-1; 5 integration; 6 E2E; §4.7 6-row map |
| 4 | RECON-4 handoff fields + success_with_hardening_* rule | PASS | §5.4 L411 grep-verbatim; handoff field-add + no-override present |
| 5 | RECON-5 section remap | PASS | §5.5 L425, §4.5 L304, §4.1 L261 — crosswalk targets correct |
| 6 | RECON-6 OI-2/3/5 HALT (not OI-1/4/6) | PASS | §11 L598; OI-1 "Resolved in §5.4" grep-confirmed |
| 7 | RECON-7 G1 HALT | PASS | §1.2 L42 + §9 L586 in spec; rollback note present |
| 8 | Banners on 01-04/06 | PASS | All 5 carry identical SUPERSEDED banner → 08+07 |
| 9 | NEW-gap scan (no fabricated anchors / no residual hole) | PASS | All §-anchors grep-resolve; §4.6/§5.6/§5.7 covered by 07 |

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (M1 — test-count headline labeling; reconciled in body; not a content gap)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| M1 | MINOR | 08 RECON-3 header + supersession summary | Headline "17 unit/integration" is the spec baseline (12+5); the true total after the G-PRE-1 addition is 18 unit/integration. Body itemizes all 18 correctly, so no inventory is lost — only the headline number could be misread as the final total. | Builder note: target **18 unit/integration + 6 E2E** (= 13 unit + 5 integration + 6 E2E = 24 test items). No research re-spawn needed. |

## Confidence Gate
- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Every check backed by a grep/Read tool call against the live spec, not 08's self-report.
- The single MINOR is a labeling imprecision, not a gap; it does not block synthesis/build because the body inventory is complete and correct.

## Recommendations
- PASS the research gate. The builder may proceed (A.9 rf-task-builder against RELEASE-SPEC v1.1.0).
- Carry the M1 note into the BUILD_REQUEST so the builder targets 18 unit/integration tests, not 17.

## QA Complete
