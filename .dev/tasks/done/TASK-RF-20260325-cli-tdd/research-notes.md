# Research Notes: CLI TDD Integration — Task File Build

**Date:** 2026-03-25
**Scenario:** A (explicit — research already completed)
**Depth Tier:** Deep (14+ files, 3 subsystems, architectural decisions)
**Track Count:** 1
**Status:** Complete

---

## SOURCE RESEARCH

This task file build uses pre-existing, QA-verified research from `TASK-RESEARCH-20260325-001/`:

| Research File | Topic | Key Finding |
|---|---|---|
| `research/01-executor-data-flow.md` | How spec_file flows through all pipeline steps | 3 steps receive spec_file directly: extract, anti-instinct, spec-fidelity. Generate steps receive ONLY extraction output — extract is the single chokepoint. |
| `research/02-prompt-language-audit.md` | All prompt builders — spec-language assumptions | `build_extract_prompt()` is Critical severity — 8 sections miss all TDD structural content. `build_spec_fidelity_prompt()` is High. |
| `research/03-pure-python-modules.md` | spec_parser, fidelity_checker, integration_contracts, fingerprint, obligation_scanner | Most modules are format-agnostic. fidelity_checker is Python-only (TypeScript blind spot). |
| `research/04-gate-compatibility.md` | All 14 gate definitions | 5 gates already compatible, 9 conditional on `spec_source` aliasing, DEVIATION_ANALYSIS_GATE structurally incompatible. |
| `research/05-cli-entry-points.md` | CLI flags, models, extension points | No `--input-type` flag exists. Established backward-compat extension pattern via additive defaulted fields. |
| `research/06-tdd-template-structure.md` | 28 TDD sections vs extraction coverage | 5 CAPTURED, 15 PARTIAL, 8 MISSED. Missing: §7 Data Models, §8 API Specs, §9 State, §10 Components, §15 Testing, §25 Ops, §26 Cost, §28 Glossary. |

**QA Status:**
- Research gate: PASS (10/10 checks)
- Report assembled: 770 lines, validated
- Report structural QA: PASS (19/19 checks)
- Report qualitative QA: PASS (4 issues found and fixed)

## IMPLEMENTATION PLAN (from research report §8)

The recommended approach is **Option A: Dual extract prompt with explicit `--input-type` flag**.

6 implementation phases targeting CLI Python files only:

| Phase | Files to Change | Changes |
|---|---|---|
| 1. CLI & Config | `commands.py`, `models.py` (roadmap + tasklist) | Add `--input-type [spec\|tdd]` flag, `input_type` + `tdd_file` fields to config dataclasses |
| 2. TDD Extract Prompt | `roadmap/prompts.py` | Create `build_extract_prompt_tdd()` with 14 sections (8 existing + 6 new) |
| 3. Executor Branching | `roadmap/executor.py` | Branch on `config.input_type` at extract step construction |
| 4. Gate Schema | `roadmap/gates.py` | Keep `spec_source` for backward compat; defer DEVIATION_ANALYSIS_GATE redesign |
| 5. Fidelity Prompt | `roadmap/prompts.py` | Generalize `build_spec_fidelity_prompt()` for TDD dimensions |
| 6. Tasklist Validate | `tasklist/executor.py`, `tasklist/prompts.py` | Add `--tdd-file` flag, TDD enrichment for §15/§19 |

## TEMPLATE_NOTES

Template 02 (Complex Task). The implementation involves:
- Multiple distinct phases with different file targets
- Conditional logic (executor branching)
- Per-function granularity (each prompt builder is a separate item)
- Testing/verification steps (backward compatibility, gate pass verification)

Note: MDTM templates at `.gfdoc/templates/` may not exist in IronClaude. Builder should construct from BUILD_REQUEST structure directly.

## AMBIGUITIES_FOR_USER

None — implementation plan is fully specified in the research report with specific file paths, function names, and code patterns.

## OPEN QUESTIONS (from research — carry into task file)

| # | Question | Impact |
|---|---|---|
| C-1 | Does `semantic_layer.py` read spec_file in active pipeline? | If yes, it's a 4th implementation point |
| C-2 | Does `structural_checkers.py` have spec-format assumptions? | If yes, may need TDD changes |
| I-1 | Does `run_wiring_analysis` wiring_config reference spec_file? | If yes, it's a 5th implementation point |
| I-5 | ANTI_INSTINCT_GATE TDD performance (more identifiers → better coverage) — unverified hypothesis | Testing needed |
| B-1 | DEVIATION_ANALYSIS_GATE `ambiguous_count` vs `ambiguous_deviations` field mismatch — pre-existing bug | Separate fix |
