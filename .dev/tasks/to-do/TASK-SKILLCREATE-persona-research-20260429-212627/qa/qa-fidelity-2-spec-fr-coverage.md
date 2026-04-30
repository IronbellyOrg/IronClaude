# QA Report — Source-Document Fidelity Verification

**Topic:** sc-persona-research-protocol SKILL.md — SPEC FR COVERAGE LENS
**Date:** 2026-04-30
**Phase:** skillcreate-source-fidelity (lens: spec-fr-coverage)
**Fix cycle:** N/A (REPORT-ONLY)
**Generated SKILL.md:** `/config/workspace/IronClaude/.temp/skills/sc-persona-research-protocol/SKILL.md` (1,887 lines)
**Source spec:** `/config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md` (993 lines)

---

## Overall Verdict: PASS

All 11 fidelity checks pass. Every FR-1 through FR-26 from spec §11 acceptance criteria is encoded in the SKILL.md. The §10.1 disclaimer appears verbatim 4 times (≥3 required). The §5.2 worker JSON contract is fully reproduced in the S20 Archetype-Driven Research Worker prompt. The Guard tables (G1-G4), Quantity Flow Diagram, model tiering, Tavily routing, three-questions test, sequential identity gate (FR-2), no-first-person-attribution rule (FR-7), and archetype-generic-purity linter (FR-22) are all explicitly encoded.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FR-1 through FR-26 coverage exhaustive | PASS | grep verified each FR-N appears at minimum 1 location in SKILL.md (most appear 4-10 times). Detailed mapping below. |
| 2 | §10.1 disclaimer verbatim ≥3 times | PASS | `grep -c "Modeled on the public posture of"` → 4 hits at lines 1642 (S25), 1680 (S25 ref), 1736 (S26.1), 1808 (S27 Rule 23). Em-dash U+2014 and apostrophe U+0027 preserved. §10.2 unsuitable-subject rules described in Identity Verifier S20 (lines 652-706) and S26.2 (lines 1742-1747). |
| 3 | §5.2 worker JSON schema fully embedded in S20 | PASS | S20 Archetype-Driven Research Worker prompt (lines 825-871) contains the complete §5.2 contract. All 14 fields present (subject_input, identity_verification, archetype_resolution, slot_bindings, footprint_score, dossier_markdown, sources, stable_traits, context_specific_lens, three_questions, persona_toml_block, archetype_refinement_proposal, warnings, status). Note: prompt requested "10 fields"; the spec actually defines 14 — all present. |
| 4 | Guard tables §A G1-G4 runtime emission | PASS | Lines 174 (output path `${TASK_DIR}synthesis/guard-boundary-tables.md`), 224 (FR-12 mandatory emission statement), 1584 (G1-G4 enumerated: identity_verified, subject_is_living_adult_public_figure, public_footprint_above_threshold, archetype_match_resolution), 1619 (S24 Assembly emission step). |
| 5 | Quantity-flow §B runtime emission | PASS | Lines 173 (output path `${TASK_DIR}synthesis/quantity-flow-diagram.md`), 224 (FR-12 mandatory), 995 (Aggregator appends Quantity Flow Diagram), 1002 (App B with ACTUAL N → N' → P+Q → M → K counts), 1497 (in run summary stdout), 1505 (ALWAYS emit even when N==M). |
| 6 | Model tiering §9.2 (Haiku/Opus) | PASS | Line 482-487 (S20 worker prompt header MODEL TIERING RULES block: "Workers MUST NOT call Opus for per-source processing (FR-24)"); line 758 (S20 Archetype-Driven Worker: Haiku per-source, Opus consolidation only); line 642 (Identity Verifier explicit Haiku model tag). Critical Rules section also references model tiering. |
| 7 | Tavily routing §9.2/FR-25 with 5xx fallback | PASS | Line 484 (Tavily MCP routing rule), 759 (S20 Archetype-Driven Worker: "fallback to direct fetch only when Tavily is unavailable"), 796 (Step 2 of research protocol explicitly Tavily-routed), 484-485 (Critical Rule). Note: spec §9 Operations Q9 calls out 5xx threshold as an open question; SKILL.md correctly describes the fallback behavior. |
| 8 | Three-questions test §8/FR-23 | PASS | S20 Validator prompt (lines 1042-1085): Sequencing line "runs the three-questions test (FR-23) against a context_artifact" + Validation Protocol step 2 prompts the spawned subagent to answer each of three_questions; fidelity scoring 0-10 per Acceptance Criterion #4 (target ≥ 7/10). |
| 9 | FR-2 sequential identity gate (EXPLICIT) | PASS | (a) Critical Rule 24 (line 1812): "No research worker may spawn for a subject before the Identity Verifier completes for that subject and emits `identity_verified == true`". (b) S20 Identity Verifier (line 641): "Phase 2 — runs BEFORE any research worker spawns (FR-2 sequential gate)". (c) S20 Research Worker (line 757): "spawned in parallel after ALL identity verifications complete". Also reinforced at line 577 (Parallel Spawning section) and line 1683 (S25 IDENTITY_VERIFIED_BEFORE_RESEARCH check). |
| 10 | FR-7 no-first-person-attribution (EXPLICIT) | PASS | (a) S25 line 1579: concrete static regex `grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'` and `grep -nE '^[A-Z][a-z]+:\s*"'`. (b) S26 Content Rule 7 (line 1729): no first-person attributed quotes — same regex referenced. (c) S27 Critical Rule 25 (line 1814): the same two grep regexes are encoded as the static check. Aligns precisely with spec FR-7 acceptance criterion. |
| 11 | FR-22 archetype-generic-purity (EXPLICIT) | PASS | (a) S25 line 1580: linter check on `display_name`, `persona_description_template`, and `stable_traits` fields; `identity_signals.affiliation_keywords` named as sole exception. (b) S26 Content Rule 9 (line 1731): same explicit field list with example "Crypto-Native Venture Investor" vs forbidden "Polychain-style VC". (c) S27 Critical Rule 26 (line 1816): "rejects any archetype whose `display_name`, `persona_description_template`, or `stable_traits` mentions any specific firm/person/fund". Also enforced in S20 Discovery Worker (line 967, 1037 verdict gates). |

## Detailed FR-by-FR Coverage Map

| FR | Spec definition (abbreviated) | SKILL.md anchor lines | Status |
|----|-------------------------------|----------------------|--------|
| FR-1 | Accept 1-N subjects; reject empty | 60, 102, 250 | PRESENT |
| FR-2 | Identity verification BEFORE deep research (sequential) | 26, 212, 455, 577, 641, 1582, 1649, 1683, 1812 | PRESENT |
| FR-3 | One research subagent per verified subject, in parallel (single message) | 214, 316, 457, 577, 1650 | PRESENT |
| FR-4 | Three artifacts per worker (dossier/persona/three-questions) | 1491-1493, 1557, 1651 | PRESENT |
| FR-5 | Every claim source-cited with URL + retrieval date | 1491, 1557-1558, 1581, 1652 | PRESENT |
| FR-6 | Verbatim §10.1 disclaimer prepended | 477, 1492, 1506, 1562, 1578, 1642, 1736, 1808 | PRESENT |
| FR-7 | No first-person quotes (static check) | 25, 221, 460, 477, 811, 1579, 1654, 1729, 1814 | PRESENT |
| FR-8 | Unified diff against config.toml; no auto-write | 74, 178, 222, 982, 1001 | PRESENT |
| FR-9 | Refuse deceased/minor/private subjects | 127, 261, 315, 1586, 1656 | PRESENT |
| FR-10 | Halt on ambiguous identity | 135, 315, 612, 684, 704 | PRESENT |
| FR-11 | INSUFFICIENT_PUBLIC_DATA sentinel; no fabrication | 1556, 1566, 1658 | PRESENT |
| FR-12 | Mandatory Quantity Flow Diagram emission | 173, 221, 224, 459, 1497, 1505 | PRESENT |
| FR-13 | Cache by `{name|affiliation|isodate}`; 24h TTL | 186, 239, 300, 1660, 1834 | PRESENT |
| FR-14 | --validate runs three-questions per persona; fidelity 0-10 | 320, 1500, 1561, 1626, 1661 | PRESENT |
| FR-15 | Companion archetype default (`archetype_companion: true`) | 1662 | PRESENT |
| FR-16 | Archetype resolution gate before research | 319, 1554, 1663 | PRESENT |
| FR-17 | On MATCH, load source_recipe + slot_schema + templates | 316, 1554, 1664 | PRESENT |
| FR-18 | On NO_MATCH, discovery worker + new archetype proposal | 94, 317, 887, 896, 1495 | PRESENT |
| FR-19 | refinement_mode==auto folds new evidence with version bump | 1496, 1563, 1666 | PRESENT |
| FR-20 | AMBIGUOUS halts; surface top-K | 319, 704, 738, 1554, 1667 | PRESENT |
| FR-21 | New/refined archetypes never auto-saved | 216, 222, 461, 477, 964 | PRESENT |
| FR-22 | Archetype generic-purity (no person/firm/fund names in core fields) | 28, 221, 460, 477, 750, 1266, 1580, 1669, 1731, 1816 | PRESENT |
| FR-23 | Archetype store portable (single dir of YAML) | 181, 320, 1045, 1081, 1374 | PRESENT |
| FR-24 | Workers MUST NOT call Opus for per-source processing | 316, 457, 482-483, 758, 1664 | PRESENT |
| FR-25 | Web searches route through Tavily MCP | 316, 371, 457, 484, 758-759, 796 | PRESENT |
| FR-26 | Run summary reports per-tier token spend; <15% Opus target | 371, 488, 758, 1170, 1366 | PRESENT |

## §5.2 Worker JSON Field Verification

The SKILL.md S20 Archetype-Driven Research Worker prompt (lines 825-871) reproduces the full §5.2 contract with all fields:

| # | Field | In SKILL.md S20 | In spec §5.2 | Match |
|---|-------|----------------|--------------|-------|
| 1 | subject_input | line 829 | line 253 | ✅ |
| 2 | identity_verification | line 830-840 (with extra ethics_screen sub-object) | line 254-258 | ✅ (SKILL adds ethics_screen — enhancement, not deviation) |
| 3 | archetype_resolution | line 841-846 | line 259-266 | ✅ |
| 4 | slot_bindings | line 847-851 | line 267-272 | ✅ |
| 5 | footprint_score | line 852 | line 273 | ✅ |
| 6 | dossier_markdown | line 853 | line 274 | ✅ |
| 7 | sources[] | line 854-856 | line 275-277 | ✅ |
| 8 | stable_traits | line 857 | line 278 | ✅ |
| 9 | context_specific_lens | line 858 | line 279 | ✅ |
| 10 | three_questions | line 859 | line 280 | ✅ |
| 11 | persona_toml_block | line 860 | line 281 | ✅ |
| 12 | archetype_refinement_proposal | line 861-867 | line 282-288 | ✅ |
| 13 | warnings | line 868 | line 289 | ✅ |
| 14 | status | line 869 | line 290 | ✅ |

The Discovery Worker also references the §5.2 JSON contract (line 954, "all §5.2 fields...subject_input, identity_verification, archetype_resolution, slot_bindings, footprint_score, dossier_markdown, sources, stable_traits, context_specific_lens, three_questions, persona_toml_block, archetype_refinement_proposal, warnings, status") and adds the discovery-only `discovered_archetype_proposal` field per spec §5.2 NO_MATCH path.

## Confidence Gate

- **Verified:** 11/11 (every checklist item has direct grep/Read evidence with line citations)
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 4 | Grep/Bash: 7 | Glob: 0
- **Verdict eligibility:** PASS (≥95% threshold met, 0 unchecked items)

## Summary
- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY mode)

## Issues Found

None — all 11 fidelity checks pass with explicit evidence.

## Minor Observations (NON-BLOCKING — informational)

| # | Severity | Location | Observation |
|---|----------|----------|-------------|
| 1 | INFORMATIONAL | QA prompt language | The QA prompt states the §5.2 worker contract has "10 fields" but the spec actually defines 14 (subject_input, identity_verification, archetype_resolution, slot_bindings, footprint_score, dossier_markdown, sources, stable_traits, context_specific_lens, three_questions, persona_toml_block, archetype_refinement_proposal, warnings, status). All 14 are present in the SKILL.md S20 worker prompt — this is a discrepancy in the QA prompt count, not in the SKILL.md output. |
| 2 | INFORMATIONAL | S20 Identity Verifier JSON | The SKILL.md S20 Identity Verifier output JSON (lines 689-700) adds an `ethics_screen` sub-object (deceased/minor/private_individual/active_witness_in_litigation) which is consistent with §10.2 ethics floor and FR-9 but goes beyond what the spec §5.2 strictly mandates. This is a positive enhancement that operationalizes the §10.2 refusal categories — not a deviation. |
| 3 | INFORMATIONAL | FR-23 ambiguity | The QA checklist item 8 references "three-questions test §8/FR-23". Note: in the source spec, FR-23 actually defines archetype-store portability ("The archetype store SHALL be portable: a single directory of YAML files"), while the three-questions test concept is fundamentally tied to FR-14 (--validate flag). The SKILL.md correctly handles BOTH interpretations: Validator prompt cites FR-23 (line 1045) for the three-questions probe AND FR-14 for fidelity scoring. The mapping is internally consistent within the SKILL.md even where the QA-prompt-to-FR mapping is loose. |

## Actions Taken

None — REPORT-ONLY mode. No fixes applied.

## Recommendations

The SKILL.md has comprehensive FR coverage. No remediation required for this lens. Green light to proceed.

If the orchestrator wishes to harden further, consider:
1. Adding a hashed sentinel for the §10.1 disclaimer (e.g., SHA256) so the FR-6 string-equality check is robust to invisible character drift (e.g., U+00A0 NBSP injection). Currently the rule states "byte-equality" — a hash sentinel would make this auto-verifiable.
2. Confirming with the source spec that FR-23 ↔ three-questions-test mapping (per QA prompt) is intentional, given the spec's FR-23 is archetype-store portability. The skill correctly handles both, but downstream tooling that reads FR-N labels should be aware.

## QA Complete
