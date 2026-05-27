# Hypothesis: Tier 1 names the right mechanical bug but mis-locates the load-bearing defect — the gate has no finding-time "fixability" classification, so every comparator class that emits HIGHs the agent cannot resolve under the 30% diff guard recurs as a 3-run halt; the comparator is the trigger, not the root

**Agent**: root-cause-analyst (Tier 2, deeper-framing)
**Tier**: 2
**Timestamp**: 2026-05-27T05:45:00Z
**Cause class**: Missing fixability invariant at finding-emission boundary (architectural design defect). Comparator-asymmetry is the *symptom* class, not the root.
**Consistency with docs**: aligned

## Claim

Tier 1 correctly identifies `phantom_ids = roadmap_ids - spec_ids` as a deterministic comparator bug (Part A of its fix is mechanically valid and I endorse it). But Tier 1's framing — "comparator-asymmetry plus missing escape" — under-states the recurrence vector. The deeper structural defect is that `_make_finding` emits every HIGH with an implicit, unverified contract: "*this finding can be resolved by an additive roadmap edit that fits inside the 30% per-patch diff guard*." That contract is never checked at emission time. When it is violated — by ID-schema drift today, by hierarchical/cross-family ID drift tomorrow, by path-prefix forms next release — the convergence loop has no way to distinguish a structurally-unfixable finding from agent failure, and burns 3 runs producing a budget-shaped halt that mislocates the cause. Pattern 2 of the historical context ("every prior failure shape has been distinct") is the direct empirical witness for this: each fix shipped a shape-specific patch; the underlying invariant violation went unaddressed. Patching only the D-family canonicalizer treats the comparator class that fired this time and leaves the next comparator class unguarded.

## Evidence

- `src/superclaude/cli/roadmap/structural_checkers.py:269-286` (verified by Read of lines 260-286) — `_make_finding` constructs every Finding with `severity = severity_override or get_severity(dimension, mismatch_type)`, where `get_severity` looks up `SEVERITY_RULES` at line 31-56. The severity is a constant per `(dimension, mismatch_type)` pair. **There is no evaluation of whether the finding is reachable by an additive roadmap edit.** A `phantom_id` is HIGH regardless of whether it is a genuine missing reference (additive-fixable) or a schema drift class with 54 siblings (NOT additive-fixable under the 30% guard).
- `src/superclaude/cli/roadmap/structural_checkers.py:380-391` (verified by Read of lines 260-400) — the phantom_id emission path. Note line 381 `for pid in sorted(phantom_ids):` emits *one finding per drifted ID*, with no awareness that the 54 IDs share an identical regex-canonical form. The emission shape itself (`N findings` not `1 finding with cardinality N`) is the architectural smell: 54 HIGHs are a single rule violation expressed as 54 instances. A fixability classifier would recognize "this is a 1-rule class-drift, not 54 independent defects" and emit one MEDIUM `id_schema_drift` rule, not 54 HIGH `phantom_id` instances.
- `src/superclaude/cli/roadmap/convergence.py:539` (verified by Read of lines 430-668) — `if active_highs == 0:` is the only pass branch. Lines 488-651 confirm there is no `MANUAL_TRIAGE`, no "structurally unfixable" terminal state, no per-rule_id soft-pass — exactly as Tier 1 noted. But the deeper point is at lines 620-630: the `reimburse_for_progress` + monotonic-progress invariant is the only mechanism by which the loop reasons about whether remediation is "succeeding." It cannot distinguish (a) `54 → 54` because the agent failed from (b) `54 → 54` because the findings are structurally unfixable. Both look identical to the loop because the loop has no fixability signal to consult. **This is the load-bearing absence.**
- `src/superclaude/cli/roadmap/remediate_executor.py:309-362` (per Wave 1 grounding, verified `ratio > 0.30` at line 335) — the 30% diff guard is enforced at patch-submission time, *after* the loop has been entered and remediation has been attempted. The information needed to predict "this finding's only valid fix exceeds 30%" is available at finding-emission time (count cardinality, drift class, additive-vs-migration nature) but is never computed. The guard is a *consumer* of fixability information that is never produced; it can only reject patches reactively.
- `src/superclaude/cli/roadmap/integration_contracts.py:445` (per Wave 1.5 doc-context restriction 7) — `_canonicalize_identifiers` exists as project precedent for the *canonicalization* half of the fix, but does NOT extend to a fixability classifier. The precedent endorses Part A of any fix but does not constrain Part B. A purely-canonicalization fix would be consistent with this precedent yet still leave the deeper defect intact.
- `.dev/releases/complete/v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md:127` (per Wave 1.5) — the consensus that "all three [Variants A/B/C] are architecturally excellent for their own gates but none of them fix the actual broken component." Re-reading this through the deeper-framing lens: "the actual broken component" is not just the comparator; it is the absence of fixability semantics in the Finding emission contract. Every variant addressed a *different* gate's correctness; none added a fixability invariant. That is why each subsequent failure has a distinct shape.

## Why it recurs (Phase 0 pattern re-read)

Historical-context Pattern 2 ("every prior failure shape has been distinct") is the empirical signature of a missing fixability invariant. Each shape — severity drift (v3.0), parser noise + `files_affected=[]` (mid-May), ID-schema drift (TUIBBS today) — is a *different* way for emitted HIGHs to be unreachable by additive remediation, and each shipped fix patched the surface that fired *that time*. Pattern 1 ("convergence loop solves wrong problem") is the same defect viewed from the loop side: the loop is sound *given* the contract that emitted HIGHs are reachable, but the contract has never been a verified invariant. The team has been re-discovering the violation in increasingly expensive ways. Patching only the D-family canonicalizer would suppress the current symptom class, but the next release will surface a different shape (most likely candidates: FR-7.1 vs FR-7-1 sub-ID drift; G1 vs G-1 family drift; path-prefix forms `src/` vs `./src/`; hierarchical CLI mode names that the parser canonicalizes differently than the comparator). Each will reproduce the same 3-run-halt pattern under a different `mismatch_type` until the fixability invariant is added at finding-emission time.

## Proposed Fix

**One change, two coordinated parts, both in `structural_checkers.py` (preserves restriction 1, restriction 2, restriction 5) — a fixability classifier at finding-emission time, with the D-family canonicalizer as its first concrete user.**

Part A (the generalizable infrastructure — the load-bearing change):

1. Add a `_classify_fixability(dimension, mismatch_type, finding_count, drift_canonical_form) -> FixabilityClass` pure helper near `_make_finding` (around line 260). FixabilityClass is one of: `ADDITIVE_FIXABLE` (current default — additive edit fits 30% guard), `CLASS_DRIFT` (N findings reduce to 1 rule-violation under regex-canonical form; demote to single MEDIUM with templated guidance), `SCHEMA_MIGRATION` (only fix is a roadmap-wide rewrite > 30%; demote to MEDIUM with explicit guidance to use `--allow-regeneration` or normalize the comparator). Implementation: pure inspection of (mismatch_type, count, canonical-form match between spec and roadmap sets). No shared state.
2. Modify `_make_finding` (lines 263-286) to accept an optional `fixability` arg; when present and not `ADDITIVE_FIXABLE`, override severity to `MEDIUM` and replace `fix_guidance` with a class-specific template. This is a 3-line addition to `_make_finding` plus a new dict `FIXABILITY_GUIDANCE_TEMPLATES` near line 98 (alongside the existing `FIX_GUIDANCE_TEMPLATES`).

Part B (the first concrete user — the canonicalizer, building on Tier 1's Part A):

3. In `check_signatures` lines 372-391, before the set-difference at line 380, compute `spec_ids_canon` and `roadmap_ids_canon` via a new `_canonicalize_requirement_id(pid: str) -> str` helper (strips leading zeros within the numeric tail of the matched ID). Compute `phantom_ids_raw = roadmap_ids - spec_ids` (existing behavior) AND `phantom_ids_canon = roadmap_ids_canon - spec_ids_canon` (new). For each `pid` in `phantom_ids_raw`, look up its canonical form: if canonical-form IS in `spec_ids_canon`, emit through `_make_finding` with `fixability=CLASS_DRIFT` (which will demote to MEDIUM `id_schema_drift` with guidance "Spec uses raw form X; roadmap uses padded form Y. Normalize one side OR rely on the canonicalized comparator. Does not block convergence."). If canonical-form is NOT in `spec_ids_canon`, emit as HIGH `phantom_id` (genuine missing reference; current behavior).

Files that would change:
- `src/superclaude/cli/roadmap/structural_checkers.py` — add `_classify_fixability` (~15 lines), add `FIXABILITY_GUIDANCE_TEMPLATES` dict (~10 lines), add `_canonicalize_requirement_id` (~8 lines), modify `_make_finding` to accept `fixability` arg (~3 lines), modify the phantom_id block at lines 372-391 to do canonicalization + fixability classification (~12 lines). Total ~48 lines added, ~3 modified. Well under the 30% per-patch guard for this ~700-line module.

Tests that would prove the fix:
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_canonicalizes_zero_padded_d_ids` — spec `{D1, D3, D5}`, roadmap `{D01, D03, D05}` → 0 HIGH, 3 MEDIUM `id_schema_drift` findings.
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_real_missing_still_emits_high` — spec `{D1, D3}`, roadmap `{D1, D99}` → 1 HIGH `phantom_id` for `D99` (genuine missing; canonical form not in spec).
- New: `tests/cli/roadmap/test_structural_checkers.py::test_fixability_classifier_class_drift_aggregation` — confirms 54 same-class drift IDs are emitted as 54 MEDIUMs (not 1 MEDIUM with cardinality 54) for backward-compat reasons, but all share `fixability=CLASS_DRIFT` and rule_id `id_schema_drift`, so a future aggregator can dedupe at presentation time.
- New: `tests/cli/roadmap/test_convergence.py::test_class_drift_medium_does_not_block_pass` — registry containing only `id_schema_drift` MEDIUMs yields `active_highs == 0` on Run 1.
- Regression: existing tests asserting genuine phantom IDs (e.g. `D99` not in spec at all) still emit HIGH.

## Compliance with the 7 restrictions (doc-context.md)

1. **Module ownership** — all changes in `structural_checkers.py`. No edits to `spec_parser.py` (extraction stays raw, downstream consumers unaffected) or `convergence.py` (loop logic untouched). COMPLIES.
2. **Pure-function contract (NFR-4)** — `_classify_fixability`, `_canonicalize_requirement_id`, and the modified `_make_finding` are all pure functions over inputs; no shared mutable state, no I/O. COMPLIES.
3. **30% diff guard is per-patch** — proposed change is ~48 added + ~3 modified lines in a ~700-line module = ~7% diff. COMPLIES. (Note: this fix is intentionally designed to fit *under* the guard rather than to lobby for raising it, which is what S3 from the deferred backlog would have required.)
4. **Pass condition is strictly binary** — `convergence.py:539` is NOT modified. The fix re-shapes 54 unfixable HIGHs into 54 informational MEDIUMs at emission time; the binary `active_highs == 0` pass condition then naturally succeeds on Run 1. No MANUAL_TRIAGE state machine needed. COMPLIES.
5. **Spec is an input the agent cannot modify** — fix touches only `structural_checkers.py`; no spec edits required, no roadmap edits required for the convergence to pass on schema-drift findings. COMPLIES.
6. **`max_runs=3` is the default, hard-coded** — `convergence.py:440` is NOT modified. COMPLIES.
7. **Precedent for canonicalization exists locally** — `_canonicalize_requirement_id` mirrors `integration_contracts.py:445`'s `_canonicalize_identifiers`. The added `_classify_fixability` is a *new* pattern, but it is the minimal extension necessary to address the deeper defect and is consistent with the project's preference for pure-function classifiers (e.g. `_classify_nfr_severity` at line 309-327 of the same module — direct in-module precedent for a pure classifier that returns a severity-related verdict). COMPLIES.

## Confidence

Self-reported confidence: 0.86

Per-dimension self-assessment:
- Evidence grounding: 1.0 — every cited file:line was Read in this turn; the cardinality argument (54 instances of 1 rule violation) is directly observable in `deviation-registry.json` per Wave 1.
- Symptom coverage: 1.0 — explains the 54-HIGH count, the flatline Run 2→Run 3, the misleading halt message, AND the recurrence-across-distinct-shapes pattern (the latter is the differentiator from Tier 1, which only explained the current shape).
- Reproducibility fit: 1.0 — fully deterministic; no LLM dependence.
- Fix directness: 0.5 — slightly larger than Tier 1's (~48 vs ~15 lines), because it adds the fixability scaffolding alongside the canonicalizer. Justified by the recurrence argument, but a reviewer who accepts only the current-shape symptom would reasonably prefer the smaller fix.
- Domain coherence: 1.0 — the fixability classifier is the natural place to encode the precondition that the convergence loop and the 30% guard tacitly assume. Adding it at finding-emission time is the architecturally clean location.

## Risks

- **Over-engineering risk**: the fixability classifier is a new abstraction. If no future failure shape ever surfaces (i.e. Pattern 2 was coincidence, not signal), the extra ~30 lines of scaffolding never pay off and the smaller Tier 1 fix would have been preferable. Mitigation: the scaffolding is gated by an opt-in arg to `_make_finding`; checkers that don't pass `fixability=` retain current behavior. Backward-compat is zero-risk.
- **Mis-classification risk**: `_classify_fixability` could wrongly classify a genuine phantom as `CLASS_DRIFT`. Mitigation: classification is structural (does the canonical form exist on both sides? does the count exceed a class-drift threshold?), not heuristic. Unit-tested across all 5 requirement families per Tier 1's grounding-gap note.
- **MEDIUM-spike side effects on downstream gates**: same as Tier 1's risk — release-readiness scoring that counts MEDIUMs may see a spike. Mitigation: tag the new `id_schema_drift` rule_id; audit downstream consumers via `grep -r "rule_id" src/` and `grep -r "severity.*MEDIUM" src/`.
- **Does not address LLM attention drift** (Pattern 1 of sec. 5) — this fix forecloses the structural recurrence vector, not the semantic one. Future LLM-driven false positives would still be possible. That is acceptable scope: structural and semantic recurrence are separable concerns; this fix names and treats the structural one.
- **Does not resurrect S6** — by design. The convergence loop stays HIGH-binary. S6 (MANUAL_TRIAGE halt) remains a defensible future addition for unanticipated shapes that escape the fixability classifier, but is no longer required for the present-shape failure or near-neighbor shapes I can predict.

## If I'm wrong, it's probably because...

The recurrence-across-distinct-shapes pattern is not actually load-bearing — Pattern 2 may be a coincidence of three data points rather than evidence of a structural invariant violation, in which case the smaller Tier 1 fix (canonicalizer + MEDIUM-demotion for D-family only) is the right answer, and adding the `_classify_fixability` scaffolding would be over-engineering that pays off only if/when a fourth distinct shape emerges.

## Alternatives considered

- **Endorse Tier 1 verbatim (canonicalizer + per-mismatch MEDIUM-demotion, no fixability scaffolding)**: rejected because it patches the trigger, not the recurrence vector. Each future drift class would require another shape-specific patch following the same pattern, which is the exact failure mode historical-context Pattern 2 names. Tier 1's fix is necessary but insufficient.
- **Re-promote S6 (MANUAL_TRIAGE halt) instead of adding a fixability classifier**: rejected because S6 acts after the loop has already burned a run; the fixability classifier acts at emission and never gates the loop on the unfixable findings. S6 is reactive ("halt gracefully"); fixability classification is proactive ("don't gate convergence on this finding to begin with"). Proactive is cheaper and clearer. S6 stays a defensible defense-in-depth addition for unanticipated shapes, but should not be the primary fix.
- **Tiered diff-relax (S3 from backlog) — let the agent submit a > 30% patch for `signatures:phantom_id`**: rejected for the same reason Tier 1 rejected it — it would encourage large schema-migration edits as a routine remediation pattern, raising risk of correlated regressions. The fixability classifier removes the *need* for the agent to attempt a > 30% fix at all; that is preferable to enlarging the budget for risky edits.

## Grounding gaps

- Did not enumerate every existing checker call site that uses `_make_finding` to confirm the optional `fixability` arg is backward-compatible across all callers. Wave 5 evidence-validator should grep `_make_finding(` in `structural_checkers.py` and confirm all current invocations omit the arg and would continue to behave identically.
- Did not measure whether the cardinality threshold for `CLASS_DRIFT` should be `>= 2` (any case where canonical-form matches on both sides) or `>= N` for some specific N. The TUIBBS evidence is 54 instances; the right N is plausibly 1 (the asymmetry itself is the defect signature, independent of count). I chose `>= 1` (any canonical match) in the proposed implementation but flag this as a calibration choice for adversarial review in Wave 4.
- Did not enumerate the predicted next-shape failure modes (FR-7.1 vs FR-7-1, G1 vs G-1, path-prefix forms, etc.) with the same rigor as the D-family case; these are claims about future failures based on the regex shapes at `spec_parser.py:329`, not verified empirical observations.
- Did not verify that the proposed MEDIUM `id_schema_drift` findings, once emitted, are filterable from any release-readiness or audit-trail report that consumes the registry. Wave 5 should grep `severity.*MEDIUM` and `rule_id` callers in `src/superclaude/cli/roadmap/` to confirm.
