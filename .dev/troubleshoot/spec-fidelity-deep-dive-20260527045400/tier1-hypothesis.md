# Hypothesis: `check_signatures` compares requirement IDs by exact string set-difference, and the convergence loop has no exit valve for findings provably unfixable by additive roadmap edit — so any spec/roadmap ID-schema drift becomes a guaranteed 3-run halt

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-27T05:10:00Z
**Cause class**: Comparator-canonicalization gap + missing escape state (structural design defect, not LLM noise)
**Consistency with docs**: aligned

## Claim

The spec-fidelity gate has two coupled structural defects that together guarantee recurrence. (1) `check_signatures` extracts requirement IDs with a lenient regex (`\bD-?\d+\b`) but then compares them with a strict raw-string set difference (`phantom_ids = roadmap_ids - spec_ids`), so any superficial schema drift between spec and roadmap (e.g. `D01` vs `D1`) is amplified into N findings — one per drifted ID. (2) The 3-run convergence loop's only pass condition is `active_highs == 0`, with no `MANUAL_TRIAGE` or "structurally unfixable" terminal state, so when the only correct fix exceeds the per-patch 30% diff guard or requires editing the spec (which the agent is forbidden to do), the loop is guaranteed to burn its budget and emit a misleading "Convergence not reached" halt. The TUIBBS v1-MVP halt with 54 ACTIVE `phantom_id` HIGHs is the deterministic intersection of these two defects.

## Evidence

- `src/superclaude/cli/roadmap/structural_checkers.py:380` — `phantom_ids = roadmap_ids - spec_ids` (verified). Raw Python `set` difference of strings; no canonicalization step before the subtraction. The findings are emitted verbatim at lines 381–391 with `description=f"Roadmap references ID '{pid}' not found in spec"`.
- `src/superclaude/cli/roadmap/spec_parser.py:329` — `"D": re.compile(r"\bD-?\d+\b")` (verified). Same regex matches both `D1` and `D01`, and `extract_requirement_ids` at line 341 returns `sorted(set(pattern.findall(text)))` — the *matched* form, with no normalization. So the extractor is lenient but the comparator at `structural_checkers.py:380` is strict — that asymmetry IS the bug.
- `src/superclaude/cli/roadmap/convergence.py:539` — `if active_highs == 0:` (verified). The pass predicate is strictly binary. There is no branch for "the remaining findings are not addressable by remediation"; everything that is not zero is failure, and the only halt formatter at lines 655–660 emits `"Convergence not reached after {max_runs} runs. Remaining active HIGHs: {final_highs}. TurnLedger: available=…, consumed=…"` — a budget-shaped message that mislocates the cause when the root issue is comparator semantics.
- `src/superclaude/cli/roadmap/remediate_executor.py:309-362` — `check_patch_diff_size` rejects any patch where `changed_lines / patch_original_count > 0.30` (verified, threshold at line 335). A schema migration renaming all 54 zero-padded `D01..D54` references in `roadmap.md` is by construction > 30% of the affected document and will be rejected, so the *only* roadmap-side fix the agent could attempt is structurally pre-rejected.
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/deviation-registry.json` (per Wave 1 grounding) — 54 ACTIVE HIGHs, every one with `dimension=signatures, source_layer=structural, mismatch_type=phantom_id`, descriptions `"Roadmap references ID 'D0N' not found in spec"` for N=01..54. Identical-shape findings only emerge from a single-rule mismatch, not from agent failure — confirming the comparator, not remediation, is the source.
- `src/superclaude/cli/roadmap/integration_contracts.py:445` — `_canonicalize_identifiers` (verified). A pure-function token canonicalizer already exists in the codebase as the project-blessed precedent for collapsing semantically-identical IDs (per `KNOWLEDGE.md` 2026-05-25 "Fix B Merged"). The pattern this hypothesis proposes for `structural_checkers.py` is the same one shipped 2 days ago in a sibling module.

## Why it recurs (Phase 0 pattern)

Every prior remediation has hardened the orchestration *around* the comparator without touching the comparator itself: v3.05 added the 3-run loop + `DeviationRegistry` + monotonic-progress invariant + `TurnLedger`; the mid-May `roadmap-spec-fidelity-fix` shipped S1 (parser sanitization), S2 (`_route_findings` + `files_affected=[roadmap.md]`), and S5 (NFR severity demotion). Each fix was shape-specific to its triggering failure (severity drift; parser noise; `files_affected=[]`), and each new release surfaces a *new* shape because the structural primitive — exact-string set-difference plus a binary pass condition plus a 30% per-patch guard plus no MANUAL_TRIAGE escape — was never disturbed. The v3.0 fidelity-investigation adversarial debate (`debate-transcript.md:127`) recorded this explicitly: "all three [Variants A/B/C] are architecturally excellent for their own gates but none of them fix the actual broken component." That unaddressed comparator is what the TUIBBS halt is now exposing.

## Proposed Fix

**One change, two parts in the same module — comparator canonicalization + MANUAL_TRIAGE classification, both inside `structural_checkers.py` (preserves module-ownership restriction 1 and pure-function contract restriction 2).**

Part A (mechanical): Add a pure `_canonicalize_requirement_id(pid: str) -> str` helper (e.g. strips leading zeros within the numeric tail of the regex match) and apply it to both sides before the set difference:

```python
spec_ids_canon = {_canonicalize_requirement_id(p) for p in spec_ids}
roadmap_ids_canon = {_canonicalize_requirement_id(p) for p in roadmap_ids}
phantom_ids = roadmap_ids_canon - spec_ids_canon
```

This is one helper + two lines changed inside `check_signatures` — well under the 30% per-patch guard, no API change, no shared state, pure transformation (NFR-4 compliant). It mirrors `integration_contracts.py:445`'s already-merged precedent.

Part B (structural escape): When `check_signatures` would emit a `phantom_id` finding whose canonical form *does* exist in the spec but whose surface form differs, classify it as `mismatch_type="id_schema_drift"` with `severity="MEDIUM"` and `fix_guidance="Spec uses 'D1' form; roadmap uses 'D01' form. Either normalize roadmap IDs OR canonicalize the comparator — this finding does not block convergence."` so the convergence loop's HIGH-only pass condition (`convergence.py:539`) no longer gates on it. This re-shapes 54 unfixable HIGHs into 54 informational MEDIUMs without changing `convergence.py` (restriction 1), without adding a MANUAL_TRIAGE state machine (S6 stays deferred), and without touching the spec (restriction 5).

Files that would change:
- `src/superclaude/cli/roadmap/structural_checkers.py` — add `_canonicalize_requirement_id` helper near `_make_finding`, modify the phantom_id block at lines 372–391 to do canonicalization first and demote drift-only findings to MEDIUM with a templated `fix_guidance`.

Tests that would prove the fix:
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_canonicalizes_zero_padded_d_ids` — feed a spec with `D1, D3, D5` and a roadmap with `D01, D03, D05`, assert 0 HIGH findings and 3 MEDIUM `id_schema_drift` findings.
- New: `tests/cli/roadmap/test_convergence.py::test_id_schema_drift_does_not_block_pass` — registry containing only `id_schema_drift` MEDIUMs should yield `active_highs == 0` and pass on Run 1.
- Regression: existing tests asserting genuine phantom IDs (e.g. `D99` not in spec at all) still emit HIGH.

## Confidence

Self-reported confidence: 0.88

Per-dimension self-assessment:
- Evidence grounding: 1.0 — every cited file:line was Read in this turn and matches the verbatim snippet.
- Symptom coverage: 1.0 — explains the 54-HIGH count, the flatline Run 2→Run 3 (8f6eba→d6070e roadmap edit but no count drop), the misleading "TurnLedger" halt message, and the recurrence pattern across releases.
- Reproducibility fit: 1.0 — fully deterministic; no LLM dependence; reproducible by running `check_signatures` on the TUIBBS spec+roadmap pair.
- Fix directness: 1.0 — single module, ~15 lines, exact precedent already merged in `integration_contracts.py`, sized well below 30% per-patch guard, fits NFR-4 pure-function contract.
- Domain coherence: 0.5 — the MEDIUM-demotion sub-fix is functionally a lightweight S6-substitute. A purist might argue this belongs in a proper MANUAL_TRIAGE state machine in `convergence.py` rather than as severity reclassification in the checker. I chose the checker because (a) restriction 1 puts ID semantics in `structural_checkers.py`, (b) it's surgical, (c) it leaves S6 free to land later as a more general escape. The "0.5" reflects that this is a defensible-but-not-unique architectural choice.

## Risks

- **False normalization**: if any project legitimately uses `D1` and `D01` as DIFFERENT requirements, canonicalization will collapse them and hide a real phantom. Mitigation: the canonical-form change only suppresses *drift* findings where the canonical form matches on both sides; an ID present in roadmap with no canonical match in spec still emits HIGH.
- **Regex scope**: `_REQUIREMENT_PATTERNS` (`spec_parser.py:329`) covers FR, NFR, SC, G, D. The canonicalizer must be agnostic — applying zero-strip only to the numeric tail, not to alphabetic prefixes. Implementation risk is low but the helper must be unit-tested across all five families.
- **MEDIUM-demotion side effects**: any downstream gate (e.g. release-readiness scoring) that counts MEDIUMs may see a spike. Mitigation: tag the new `id_schema_drift` rule_id and audit downstream consumers via `grep -r "rule_id" src/`.
- **Does not address LLM attention drift** (Pattern 1 of historical-context.md sec. 5). A semantic-fluctuation-driven failure with a different shape can still occur; this fix only forecloses the *structural* recurrence vector.

## If I'm wrong, it's probably because...

The real structural recurrence vector is the convergence loop's binary pass condition itself (`convergence.py:539`), not the comparator — meaning the right fix is a full MANUAL_TRIAGE escape state in the loop (S6 re-promoted) rather than a checker-side demotion, because checker-side demotion just relocates the next failure shape one rule_id over.

## Alternatives considered

- **Promote S6 (MANUAL_TRIAGE halt) alone, leave comparator strict**: rejected — fixes the *halt-message* problem but leaves the deterministic comparator bug intact, so the next release with `D01`/`D1` drift still emits 54 spurious findings; S6 just labels them better. Comparator must be fixed first; S6 is a complementary upgrade for the next-shape failure.
- **Move canonicalization into `spec_parser.py:329` (return canonical IDs from the extractor)**: rejected — violates restriction 1 (parser owns FR-2/FR-5 extraction, checker owns FR-1/FR-3 comparison) and risks breaking downstream consumers of `extract_requirement_ids` that expect raw matched form.
- **Tiered diff-relax (S3 from backlog) so the agent CAN rename 54 IDs in roadmap**: rejected — addresses a symptom (the per-patch 30% guard rejects a large but correct edit) without resolving the underlying comparator asymmetry; would also encourage agents to make large schema-migration edits which is a higher-risk change pattern.

## Grounding gaps

- Did not run the proposed fix end-to-end on the TUIBBS artifacts; the claim that canonicalization drops the 54 HIGHs to 0 HIGHs is inferred from the verified set-difference semantics, not measured.
- Did not enumerate every downstream consumer of `Finding.severity == "HIGH"` to confirm the MEDIUM-demotion has no second-order effects beyond `convergence.py:539`.
- Did not verify that other requirement families (FR, NFR, SC, G) actually exhibit the same drift pattern in the wild — the TUIBBS evidence is `D`-family only. Other families may need family-specific canonicalization rules (e.g. FR sub-IDs `FR-7.1` vs `FR-7-1`).
