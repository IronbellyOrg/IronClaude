---
title: Spec-Fidelity Convergence Failure — Tier 2 Deep-Dive Diagnosis
status: partial
tier_reached: 2
confidence: 0.90
escalation_reason: forced_by_depth_deep
adversarial_invoked: true
fix_authorized: true
test_is_wrong: false
behavior_is_documented: false
doc_context_card_path: .dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/doc-context.md
---

# REPORT — Spec-Fidelity Convergence Failure (TUIBBS v1-MVP)

## Header

- Target failure: `Convergence not reached after 3 runs. Remaining active HIGHs: 54. TurnLedger: available=31, consumed=46.` at `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/spec-fidelity.md`.
- Tier reached: **2** (forced by `--depth deep`)
- Confidence (calibrated): **0.90**
- Escalation reason: `forced_by_depth_deep` (Tier 1 already scored above the 0.85 auto-escalation threshold; the user requested forced Tier 2 + adversarial debate)
- Adversarial debate: **YES** (5 fix proposals, Round 1 + Round 2 + Round 2.5 invariant probe)
- Output directory: `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/`

## Summary

The TUIBBS v1-MVP roadmap pipeline halts because `structural_checkers.py:380` does a raw `set` difference of requirement IDs (`phantom_ids = roadmap_ids - spec_ids`) whose extractor (`spec_parser.py:329`) is lenient (regex `\bD-?\d+\b` matches both `D1` and `D01`) but whose comparator is strict (`'D01' != 'D1'`). Spec has `{D1, D3, D5}`, roadmap has `{D01..D54}`, so all 54 are flagged as HIGH `phantom_id`. Their only structurally-correct fix exceeds the 30% per-patch diff guard at `remediate_executor.py:309-362`, and the convergence loop's binary pass predicate (`active_highs == 0` at `convergence.py:539`) has no MANUAL_TRIAGE escape. The recurrence vector is structural: **no shipped remediation has ever touched the comparator itself** (confirmed by `.dev/releases/complete/v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md:127`). The merged fix canonicalizes ID forms in the checker, demotes drift-only findings to MEDIUM `id_schema_drift`, and adds a property-based + flatline-halt test layer to catch the next-family drift at construction.

## Documentation Context

Wave 1.5 surfaced two project-blessed precedents that make this fix consistent with prior patterns:
1. **Canonicalization precedent** (`integration_contracts.py:445`, KNOWLEDGE.md 2026-05-25 "Fix B Merged"): `_canonicalize_identifiers` collapses semantically-identical mechanism IDs in the anti-instinct gate. The merged fix mirrors this pattern for D-family requirement IDs.
2. **Severity-demotion precedent** (`structural_checkers.py:309-327`, S5 fix from `.dev/releases/backlog/roadmap-spec-fidelity-fix/`): `_classify_nfr_severity` demotes NFR softs to MEDIUM so they bypass the HIGH-only convergence gate. The merged fix uses the same MEDIUM-demotion mechanism for `id_schema_drift`.

The architectural decision to **not** touch `convergence.py:539` (binary pass condition), **not** introduce a new severity tier, and **not** modify the spec is documented in the 7 restrictions in `doc-context.md` and honored by the merged fix.

Note: `--no-doc-discovery` was NOT set; doc-grounding is load-bearing for this diagnosis.

## Diagnosis (the structural root cause, not just the immediate trigger)

**Structural cause** (verified, end-to-end mechanism):

1. **Asymmetric extractor/comparator**: `spec_parser.py:329` accepts `D-?\d+` leniently but `extract_requirement_ids` (line 333-344) returns the raw matched form. `structural_checkers.py:380` compares with strict set difference. The asymmetry between lenient extraction and strict comparison is the *mechanical* defect.

2. **Missing fixability invariant at finding-emission time**: `_make_finding` (`structural_checkers.py:269-286`) constructs every HIGH without verifying the finding is reachable by an additive roadmap edit fitting inside the 30% diff guard. When this implicit contract is violated — by ID-schema drift today, by something else next release — the loop cannot distinguish "agent failed" from "fix is structurally unreachable" and burns 3 runs producing a budget-shaped halt message.

3. **No MANUAL_TRIAGE escape**: `convergence.py:539` is strictly binary (`active_highs == 0`). S6 ("MANUAL_TRIAGE halt") was deferred from the `roadmap-spec-fidelity-fix` backlog as "not required if top-3 converge" — but the present failure shape (54 HIGHs the agent cannot fix) is exactly the scenario S6 was designed for. Without it the loop is structurally guaranteed to halt opaquely on any unfixable-finding class.

4. **The pattern is the recurrence vector**: every prior remediation has hardened the orchestration around the comparator (DeviationRegistry, TurnLedger, monotonic-progress invariant, regression detection, S1/S2/S5) without touching the comparator itself. The v3.0 adversarial debate-transcript explicitly recorded the consensus: "none of them fix the actual broken component." Each new release surfaces a *new* shape because the structural primitive — exact-string comparison + binary pass + 30% per-patch guard + no fixability invariant — hasn't changed.

The chosen fix addresses (1) directly (canonicalize at comparator) and (4) partially (property-based test catches family-agnostic asymmetric-form drift at construction). (2) and (3) are documented as forward-looking improvements: (2) is partially captured by the new `id_schema_drift` rule_id (a specific instance of the deeper fixability concept), to be generalized when calibration data exists; (3) remains a defensible defense-in-depth addition for non-ID drift classes.

## Evidence

Every claim has been independently verified by Read of the cited file:line.

- `src/superclaude/cli/roadmap/structural_checkers.py:380` — `phantom_ids = roadmap_ids - spec_ids` — the raw set difference that drives the 54 findings.
- `src/superclaude/cli/roadmap/structural_checkers.py:381-391` — `for pid in sorted(phantom_ids): findings.append(_make_finding(... description=f"Roadmap references ID '{pid}' not found in spec" ...))` — the emission shape (1 finding per drifted ID).
- `src/superclaude/cli/roadmap/spec_parser.py:329` — `"D": re.compile(r"\bD-?\d+\b")` — lenient D-family regex.
- `src/superclaude/cli/roadmap/spec_parser.py:333-344` — `extract_requirement_ids` returns `sorted(set(pattern.findall(text)))` (raw matched form).
- `src/superclaude/cli/roadmap/convergence.py:539` — `if active_highs == 0:` — sole pass branch; binary.
- `src/superclaude/cli/roadmap/convergence.py:242-244` — `get_active_high_count` whitelist-filters HIGH only (MEDIUM excluded from gate).
- `src/superclaude/cli/roadmap/convergence.py:440` — `max_runs: int = 3` — hard default.
- `src/superclaude/cli/roadmap/convergence.py:653-668` — halt formatter: `"Convergence not reached after {max_runs} runs. Remaining active HIGHs: {final_highs}. TurnLedger: available=..., consumed=..."` — budget-shaped message that mislocates the cause.
- `src/superclaude/cli/roadmap/remediate_executor.py:309-362` — `check_patch_diff_size` rejects patches with `ratio > 0.30`.
- `src/superclaude/cli/roadmap/integration_contracts.py:445` — `_canonicalize_identifiers` — canonicalization precedent.
- `src/superclaude/cli/roadmap/structural_checkers.py:309-327` — `_classify_nfr_severity` — MEDIUM-demotion precedent (S5).
- `src/superclaude/cli/roadmap/structural_checkers.py:155-176` — `FIX_GUIDANCE_TEMPLATES` dict; phantom_id NOT in the dict (generic fallback at line 279).
- `src/superclaude/cli/roadmap/structural_checkers.py:205-213` — `_route_findings` applies templates by `rule_id`; `phantom_id` falls through to the generic guidance.
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/deviation-registry.json` — 58 total findings: 4 FIXED (data_models), 54 ACTIVE (signatures / structural / phantom_id, D01..D54).
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/spec-fidelity.md` — convergence halt report.
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md` — spec uses `D1, D3, D5`.
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md` — roadmap uses `D01..D54`.
- `.dev/releases/complete/v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md:127` — "no shipped remediation has touched the actual broken component."
- `.dev/releases/backlog/roadmap-spec-fidelity-fix/RANKING.md` — prior 6-way debate, S1+S2+S5 merged, S3 + S6 deferred.

## Proposed Fix

(Verbatim from `adversarial/merged-output.md` — base = fix-5, with strengths from fix-2 and fix-3 incorporated via docstrings; fix-4 deferred.)

### Files to change

| # | File | Change | Lines |
|---|---|---|---|
| 1 | `src/superclaude/cli/roadmap/structural_checkers.py` | Add `_canonicalize_requirement_id(family, raw) -> str` helper near `_make_finding` (around line 260). Pure function. Strip leading zeros from numeric tail; preserve family prefix and sub-ID structure. Docstring tags `id_schema_drift` as an instance of the broader fixability concept and notes the helper could move upstream into `extract_requirement_ids` in a future refactor. | ~15 added |
| 2 | `src/superclaude/cli/roadmap/structural_checkers.py` | Modify the phantom_id block at lines 372-391 — compute canonical sets, emit MEDIUM `id_schema_drift` for canonical-match-but-form-differs cases, preserve HIGH `phantom_id` for canonical-form-not-in-spec cases. Add `("signatures", "id_schema_drift"): "MEDIUM"` to `SEVERITY_RULES` at lines 42-67. Add templated `id_schema_drift` entry to `FIX_GUIDANCE_TEMPLATES` at lines 155-176. | ~10 modified + ~10 added |
| 3 | `tests/cli/roadmap/test_structural_checkers.py` (path may be `tests/roadmap/test_structural_checkers.py` per repo convention) | Add 5 golden-fixture asymmetric-ID tests covering all 5 requirement families (FR, NFR, SC, G, D) with zero-pad and sub-ID drift cases. | ~50 added |
| 4 | NEW `tests/cli/roadmap/test_structural_checkers_properties.py` + `tests/cli/roadmap/test_convergence.py` + `tests/cli/roadmap/test_remediate_executor.py` | Add property-based test (`importorskip("hypothesis")`-gated, matches `tests/sprint/test_property_based.py` precedent), flatline-halt regression test, and cross-cutting "all-fixes-unfixable" integration test. | ~95 added |

### Test plan

- New tests outlined in Changes 3-4 above (9 new tests total).
- Regression: existing tests asserting genuine `phantom_id` HIGHs from missing IDs still pass.
- End-to-end smoke (recommended, not blocking): re-run `superclaude roadmap run` against `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md` with `--resume` to confirm Run 1 passes with 0 active HIGHs.

## Alternative Fixes Considered (losers from the adversarial debate)

| Variant | One-line | Adversarial verdict |
|---|---|---|
| **fix-1** (Tier 1: minimal canonicalizer) | Same code as base (incorporated). Lacks the test surface that catches next-family drift at construction. | Loser by margin 7.2% — code is identical to base; what differentiates is the test layer. |
| **fix-2** (Tier 2 RCA: fixability classifier) | `_classify_fixability` infrastructure (~48 LOC). Addresses the recurrence vector proactively. | Loser — INV-003 (HIGH UNADDRESSED): the `CLASS_DRIFT` count threshold is undefined, making the classifier non-deterministic. Reconsider next release with calibrated threshold. |
| **fix-3** (Tier 2 refactoring-expert: upstream canonicalization) | Move canonicalization into `spec_parser.extract_requirement_ids`. Eliminates the asymmetric seam entirely. | Loser — minimal 12-LOC version breaks `Finding.roadmap_quote` at `structural_checkers.py:389`; full version is a value-object refactor exceeding stated scope. Insight preserved as future work in helper docstring. |
| **fix-4** (Tier 2 system-architect: ADVISORY severity tier + CLI lane) | New `ADVISORY` tier beneath MEDIUM + `--allow-advisory-drift` / `--strict-no-advisory` flags. | Loser — new tier introduces ongoing audit burden on every `Finding.severity` consumer; CLI flag is a permanent API surface. Justify only with 2+ drift classes. Defer. |

## Risk + Rollback

| Risk | Mitigation |
|---|---|
| False normalization (intentional `D1` and `D01` coexist) | Probability LOW; surfaces as `INV-002` in invariant probe. Document in helper docstring; collision-warning is a follow-up task. |
| Family-specific canonicalization correctness (FR-7.1 vs FR-7-1 sub-ID handling) | Property-based test in Change 4 covers all 5 families with sub-ID cases. Plus 5 golden-fixture tests in Change 3 lock specific scenarios. |
| MEDIUM-spike side effects on downstream gates that count MEDIUMs | The convergence gate at `convergence.py:242` whitelists HIGH only — MEDIUM-spike does NOT affect convergence. Other consumers should be audited (`grep -r "severity" src/superclaude/cli/roadmap/`); follow-up task. |
| Flatline-halt test brittleness (asserts on halt-reason marker text) | Recommend switching to a structured `result.halt_reason` enum once defined. For now, marker-string assertion is acceptable (test_flatline_halt_emits_structural_verdict). |
| Does NOT address LLM attention drift (Pattern 1 of historical-context.md) | Out of scope. Documented as future work. |

**Rollback**: revert the single commit; `_canonicalize_requirement_id` is purely additive in the checker so no migration needed.

## Next Steps

- **Without `--fix`**: review this REPORT.md; re-invoke `/sc:troubleshoot ... --fix` to authorize Tier 3 remediation chain.
- **With `--fix`** (this invocation): proceed to Wave 6 — Tier 3 remediation offer. The merged fix is ready for the `task-builder` handoff; the user will run `/task <path>` themselves.

## Grounding gaps

(Items not fully grounded in this report's evidence — to be re-grounded by the user or in a follow-up troubleshoot.)

1. Did not run the proposed fix end-to-end on the TUIBBS artifacts; the "54 HIGHs → 0 HIGHs" claim is inferred from the verified canonicalization semantics, not measured. Recommend a smoke test via `superclaude roadmap run ... --resume` after the fix lands.
2. Did not enumerate every downstream consumer of `Finding.severity == "HIGH"` outside `convergence.py:242` to confirm MEDIUM-demotion has zero second-order effects on release-readiness scoring or PR-review gates.
3. Did not verify that `tests/cli/roadmap/` vs `tests/roadmap/` is the correct test path (repo convention check needed at commit time).
4. Did not measure whether installing `hypothesis` as a declared dev-dep would break any existing CI configuration. `importorskip` sidesteps the policy question; broader question deferred.
