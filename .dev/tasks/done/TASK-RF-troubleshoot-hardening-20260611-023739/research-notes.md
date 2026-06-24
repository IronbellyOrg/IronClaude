# Research Notes: Implement Pipeline Hardening Closure mode for sc:troubleshoot-protocol (RELEASE-SPEC v1.1.0)

**Date:** 2026-06-11
**Scenario:** A (explicit — spec, output paths, ordering, DoD all provided)
**Depth Tier:** Deep (multi-file spec, 6 new refs + 4 modified + tests, cross-cutting invariant)
**Track Count:** 1 (single cohesive deliverable)
**Authoritative spec:** `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` (v1.1.0)

> **REBUILD PROVENANCE (CRITICAL):** This is a fresh rebuild superseding `TASK-RF-troubleshoot-hardening-20260610-144537`, which was built against the older DRAFT (`troubleshoot-pipeline-hardening-spec.md`) plus a HALLUCINATED "advisory removed per C1/C3" reconciliation. That prior tasklist asserted a three-token verdict enum `pass|blocked|not_applicable` and audited FOR the ABSENCE of `advisory`. This is WRONG against the RELEASE-SPEC v1.1.0, which uses the FOUR-token enum `pass|blocked|advisory|not_applicable` (§4.5 registry line 311, §5.5 field schema line 431) and whose §5.4 truth table ROWS 5 & 6 EMIT `advisory`. The whole anti-theatre waiver-latch design distinguishes `blocked` (hard fail / FR-12) from `advisory` (rationalized-N/A or accepted-substitute proof). **`advisory` is REQUIRED. Any artifact, item, or test that removes/forbids `advisory` is a defect.**

---

## EXISTING_FILES

### Target skill directory (verified to exist via prior research 01-03)
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — the fat skill body; Tier 1/2/3 table; the new mode triggers AFTER Tier 1, BEFORE report closure. NOT a 4th tier (research 02 L47).
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/` — existing refs dir; house conventions documented in research 03.
- `src/superclaude/commands/troubleshoot.md` — thin command; gains an advertise sentence only (NFR-5 command-thinness; research 02).
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` — gains a `Pipeline Hardening Closure` section (FR-13; research 03 L142/151/197 — note report `Closure verdict` enum must be 4-token incl. advisory).
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` — carries hardening verdict + waiver latch (FR-12).

### New ref files to CREATE (spec §4.1) — all under `src/superclaude/skills/sc-troubleshoot-protocol/refs/`
1. `pipeline-hardening-closure.md` — mode overview, trigger, verdict aggregation, waiver latch, H0 boundary scan schema (§5.6 H0 row). Foundation for all waves.
2. `hardening-output-contract.md` — field schema (§5.5), verdict aggregation TRUTH TABLE (§5.4, 7 rows incl. advisory rows 5/6), H5 decision-to-status mapping (§5.4), waiver latch propagation + downstream `success_with_hardening_*` rendering, backtest_status vs run-verdict (§5.4).
3. `runtime-entrypoint-verification.md` — H1 card schema (§5.6) + negative-witness rule (FR-4).
4. `contract-enumeration.md` — H2 ledger row schema (§5.6) + empty-ledger FAIL rule (FR-5 / F-N3).
5. `unmask-and-sweep.md` — H3 classifier boundary + small formal allow-list grammar (§5.7) + word-boundary/near-miss fixtures (FR-8/FR-9) + sweep card schema (§5.6).
6. `effective-input-proof.md` — H4 fail-closed incl. wrong-surface (FR-10 / F-D1) + manifest schema (§5.6).

### Test files to CREATE (spec §8) — under `tests/troubleshoot/`
- `test_hardening_h0.py`, `test_hardening_h1.py`, `test_hardening_h2.py`, `test_hardening_h3.py`, `test_hardening_h4.py`, `test_hardening_verdict.py`, `test_hardening_output_contract.py` (§8.1/§8.2 enumerate 12 unit + 5 integration tests). Test conventions in research 06.

## PATTERNS_AND_CONVENTIONS
- **Verdict/enum house style (research 01 L68/L126, 02 L186):** lowercase tokens. `pipeline_hardening_verdict` enum `pass|blocked|advisory|not_applicable` mirrors `diagnosability_verdict`'s inline-enum style; `not_applicable` mirrors `diagnosability_verdict=unknown`'s "never silently skipped — record + reason" discipline.
- **Path fields (research 01 L68):** `*_card_path`/`*_ledger_path`/`*_path` use type `string | null`, repo-relative, explicit null condition (mirror `doc_context_card_path`, `test_file_path`, `diagnosability_context_card_path`).
- **Additive contract (FR-13, NFR-6):** new fields under `contract_version` (semver, default `1.0.0`); existing consumers reading prior fields must not break.
- **Thin command (NFR-5, research 02 L47):** at most one advisory sentence near the Tier table; mode mechanics live in skill + refs.
- **Refs house-style (research 03):** post-template rule sections (e.g. `## Test-is-wrong rule`, `## Behavior-is-documented rule`) — add a `## Pipeline Hardening Closure rule`. Tier 3 offer is GATED on `pipeline_hardening_verdict ∈ {pass, advisory}` (research 03 L197 — note: includes advisory).
- **MDTM Template 02** (research 04): A3 granular breakdown, B2 self-containment, L1-L6 handoff patterns.
- **Sync discipline (research 06):** edit `src/superclaude/` → `make sync-dev` → `.claude/`; `make verify-sync`; markdownlint pre-commit. NEVER stage `.claude/` (except settings.json).

## GAPS_AND_QUESTIONS
- The DRAFT-vs-RELEASE section-number remap: prior research/tasklist used draft §6/§7/§8; the RELEASE-SPEC uses §3 (FRs), §4 (architecture/§4.5 registry/§4.6 order), §5 (§5.4 truth table, §5.5 field schema, §5.6 artifact schemas, §5.7 parser decision), §6 (NFRs), §8 (tests). The new spec-structure researcher (07) must extract from the RELEASE-SPEC section numbers, not the draft's.
- Doc-crossvalidation (05) must be redone against the RELEASE-SPEC's §4.1/§4.2 file lists vs actual code (do the 4 modified files exist now? current SKILL.md tier structure? any drift since the draft research on Jun 10?).
- HUMAN_DECISION items (spec §11 OI-2, OI-3, OI-5 + reflect G-PRE-3): must be `needs_human_decision` HALT items, never auto-defaulted (project memory `feedback_human_decision_items_must_halt`).

## RECOMMENDED_OUTPUTS (researcher assignments)
- **05-doc-crossvalidation-spec-vs-code-v2.md** (Doc Cross-Validator) — RELEASE-SPEC §4.1/§4.2 file claims vs actual code; tag [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]. Replaces poisoned draft-era 05.
- **07-release-spec-structure.md** (Spec-Structure Extractor) — authoritative extraction of: 13 FR acceptance criteria; §5.4 verdict truth table (all 7 rows + H5 mapping + backtest table); §5.5 field schema (10 fields); §5.6 artifact schemas (H0/H1/H2/H3/H4 rows); §5.7 parser decision; §8.1/§8.2/§8.3 test list with FR→test mapping; §4.6 implementation order (7 groups); §4.5 state variable registry (15 vars). This is the builder's authoritative content source.

Reused (carried over, advisory-correct, codebase-grounded):
- 01-skill-structure-inventory.md, 02-command-and-contract-integration.md, 03-refs-conventions-and-report-template.md, 04-mdtm-template-and-examples.md, 06-sync-verify-and-tests.md

## SUGGESTED_PHASES (builder grouping — spec §4.6, 7 groups → 7 phases)
1. Group 1: `refs/pipeline-hardening-closure.md` (mode skeleton + H0 boundary scan schema) — foundation
2. Group 2: `refs/hardening-output-contract.md` (verdict truth table incl. advisory rows 5/6 + waiver latch propagation) — resolves OI-1/OI-6 before downstream wiring
3. Group 3: `refs/runtime-entrypoint-verification.md` (H1+neg witness), `refs/contract-enumeration.md` (H2+empty-ledger FAIL), `refs/effective-input-proof.md` (H4 fail-closed incl. wrong-surface) — PARALLEL
4. Group 4: `refs/unmask-and-sweep.md` (H3 classifier + §5.7 grammar + word-boundary fixtures)
5. Group 5: SKILL.md trigger wiring + output contract (FR-13)
6. Group 6: report-template.md + remediation-handoff.md
7. Group 7: Tests (§8) + make sync-dev + make verify-sync
Plus: final phase POST-reflect gate item (penultimate) + Update-status-to-Done.

## TEMPLATE_NOTES
- Template **02** (complex): discovery→build→test, conditional flows, QA gates. Tier **Deep**.
- Generated tasklist QA gates: PER_PHASE not required for a docs/markdown-authoring task, but FINAL_ONLY QA gate + the §8 test suite ARE the validation. TESTING_REQUIREMENTS = UNIT+INTEGRATION (the §8 pytest suite under tests/troubleshoot/). VALIDATION = `make sync-dev` + `make verify-sync` + markdownlint + `uv run pytest tests/troubleshoot/`.
- POST_REFLECT_GATE ENABLED; spec_path = RELEASE-SPEC v1.1.0.

## AMBIGUITIES_FOR_USER
- RESOLVED this session: rebuild-fresh path approved; advisory REQUIRED per RELEASE-SPEC.
- OI-2 (first-class ledger tokens), OI-3 (cheapest entrypoint probe per seam), OI-5 (exact target_release) → encode as `needs_human_decision` HALT items, NOT auto-defaulted.
- G1 approval gate: produce tasklist only; tasklist must mark execution HALTED pending G1; no `src/superclaude/` or `.claude/` edits before approval.
