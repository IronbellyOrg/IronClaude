# BUILD-REQUEST Structural Index — Step 1.4

**Captured:** 2026-05-31 04:45
**Source:** `.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md` (225 lines)
**Cross-reference:** `.dev/tasks/to-do/TASK-RF-20260531-042405/research/01-file-inventory.md` (339 lines)

Purpose: provide a canonical index of the 10 Contract items, 6 architectural axes, 9 LLM steps, and every file:line citation in the BUILD-REQUEST, cross-validated against the R1 file inventory. Subsequent items cite by section anchor (e.g., `§Contract #4`) and this index ensures consistent citations.

## 1. §Contract — 10 Brittleness-Elimination Items (verbatim from §Contract section)

| # | Topic | Pipeline-blocking? | PR-blocking? | Trigger condition | New test file |
|---|---|---|---|---|---|
| 1 | Recurrence regression fixture | YES | (always) | Any fix to roadmap pipeline | `tests/roadmap/test_recurrence_regression.py` |
| 2 | Dispatch-reachability invariant | YES | (always) | New builder/runner/gate/hook symbol added | `tests/roadmap/test_dispatch_reachability.py` |
| 3 | Producer-side constraint preferred over validator | NO | YES (override-w-reason) | PRs touching `gates.py`, `structural_checkers.py`, `*_validator.py` | PR description lint (CI scan) |
| 4 | No silent PASS on empty/wrong-target inputs | YES | (always) | Every gate consuming dir/file-list/token-set | `tests/roadmap/test_gate_empty_target.py` |
| 5 | No `return True` fragility stubs with comments | YES | (always) | Source files in `src/superclaude/cli/` | `tests/roadmap/test_no_fragility_stubs.py` (CI lint) |
| 6 | Frontmatter/parser consistency | NO | YES (override-w-reason) | Adds/modifies/touches any frontmatter parser | `tests/roadmap/test_parser_consistency.py` |
| 7 | Retry-mutates-input contract | NO | YES (override-w-reason) | Adds/modifies retry/loop/convergence step | `tests/roadmap/test_retry_contract.py` |
| 8 | Threshold registry conformance | NO | YES (override-w-reason) | Numeric thresholds in source code | `tests/roadmap/test_threshold_registry.py` |
| 9 | Spec↔Roadmap ID-set containment | NO | YES (override-w-reason) | Touches generate/merge/extract/spec-fidelity | `tests/roadmap/test_spec_roadmap_id_containment.py` |
| 10 | Adversarial false-positive corpus for regex/keyword | NO | YES (override-w-reason) | Regex/keyword check on LLM-generated prose | `tests/roadmap/test_anti_instinct_recurrence.py` (and per-gate variants) |

**§Contract Pass criterion (verbatim):** "A fix is durable when items 1, 2, 4 are MUST-MET for the specific failure class; items 5, 6, 7, 8 are MUST-MET when touched code matches trigger conditions; items 3, 9, 10 are MUST-MET when the failure class is in scope. CI gates 1, 2, 4, 5 are pipeline-blocking; 3, 6–10 are PR-review-blocking with explicit override-with-reason allowed."

**Note on H1 remediation (sc:reflect Tier-2):** Per the launch instructions, Contract #5 is **pipeline-blocking** (already correctly classified above), Contract #9 is **PR-blocking** (already correctly classified above). No discrepancy with the BUILD-REQUEST text.

## 2. §MVR — 6 Architectural Axes (Preserve vs Invert)

From §Decision codification frontmatter + §MVR sections 1-5.

| Axis | Direction | Mechanism | Source |
|---|---|---|---|
| Adversarial debate mechanism | PRESERVE | Keep `diff`/`debate`/`score`/`merge` 4-step debate; no Q/A protocol change | master:§Recurrence #18 RESOLVED, A8 P3 |
| v3.05 deterministic structural-checker layer | PRESERVE | `structural_checkers.py` (1,069 LOC) untouched | §MVR §3, file-inventory §A.3 |
| Convergence wrapper concept | PRESERVE | `convergence.py` public API + atexit + `compute_stable_id` SHA256 input format stable | §MVR §5, file-inventory §A.3 |
| Markdown-as-interchange-substrate | INVERT | → `PipelineEnvelope` sidecar JSON; markdown becomes render-only | §MVR §1 |
| Content-string gate signature | INVERT | → `GateCriteria.code_assertions` slot; AST/codegraph predicates | §MVR §2 |
| LLM-as-black-box producer | INVERT | → tool-write structured outputs at all 9 LLM steps | §MVR §3 |
| Implicit cross-skill contracts | INVERT | → `superclaude.contracts` SoT module with arch-lint | §MVR §5 |

(7 rows — frontmatter lists 3 preserves + 4 inverts.)

## 3. §MVR §3 — 9 LLM Steps R1.4 Rewrites to Tool-Write

Each `build_*_prompt` in `prompts.py` becomes a tool definition with JSON schema. Markdown is rendered from tool output by deterministic Jinja templates. Side-by-side validation ≥3 release cycles per step before deletion. Per launch instruction H3+H4+H5: run interim rf-qa after Steps 9.5 and 9.10; split Step 9.11 into 9.11.a-d; build cutover counter at `.dev/migrations/r1-4-cutover-counters.yaml` before Step 9.2.

| # | Step name | `build_*_prompt` site (file:line) | Step name in `_build_steps` |
|---|---|---|---|
| 1 | extract | `prompts.py:181` `build_extract_prompt` | `extract` |
| 2 | extract_tdd | `prompts.py:329` `build_extract_prompt_tdd` | `extract-tdd` |
| 3 | generate | `prompts.py:533` `build_generate_prompt` | `generate-*` (multi-agent) |
| 4 | diff | `prompts.py:854` `build_diff_prompt` | `diff` |
| 5 | debate | `prompts.py:879` `build_debate_prompt` | `debate` |
| 6 | score | `prompts.py:906` `build_score_prompt` | `score` |
| 7 | merge | `prompts.py:964` `build_merge_prompt` | `merge` |
| 8 | spec_fidelity | `prompts.py:1085` `build_spec_fidelity_prompt` | `spec-fidelity` |
| 9 | wiring_verification | `prompts.py:1220` `build_wiring_verification_prompt` | `wiring-verification` |

**Secondary R1.4 targets (Phase 9 Step 9.11, split into 9.11.a-d per H4):**

- `prompts.py:1278` `build_test_strategy_prompt`
- `certify_prompts.py:21` `build_certification_prompt`
- `validate_prompts.py:16` `build_reflect_prompt`
- `validate_prompts.py:149` `build_merge_prompt` (validate path)
- `remediate_prompts.py:17` `build_remediation_prompt`

## 4. File:Line Citation Cross-Reference (BUILD-REQUEST ↔ R1 file inventory)

Every file:line citation in the BUILD-REQUEST text below — cross-validated against research/01 inventory. All confirmed verbatim, no drift.

### R0-scope citations

| BUILD-REQUEST citation | Inventory location | Status |
|---|---|---|
| §R0.1: `src/superclaude/cli/roadmap/id_registry.py` (NEW) | research/01 §E (file does not exist; R0.1 creates it) | CONFIRMED — needs creation |
| §R0.2: `obligation_scanner.py` term list near `scan_obligations` | research/01 §A.4 — `scan_obligations` L208, `_DESCRIPTOR_NOUNS` L109-125, `_DEMOTED_H3_SUBSECTIONS` L137-142 | CONFIRMED |
| §R0.2: MultiModelSwarm halt lines 207/211/213 | task notes line 90 — "stub transport", "stub-worker parallelism test" | CONFIRMED (task spec authoritative for FP seeds) |
| §R0.3: `src/superclaude/contracts/__init__.py` (NEW) with `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES` | research/01 §E (does not exist; R0.3 creates) | CONFIRMED — needs creation |

### R1-scope citations

| BUILD-REQUEST citation | Inventory location | Status |
|---|---|---|
| §MVR §1: `gates.py:168` `_parse_frontmatter` | research/01 §A.2 — `_parse_frontmatter` L168 | CONFIRMED |
| §MVR §1: `_check_frontmatter` (second variant) | research/01 §B — `cli/pipeline/gates.py:_check_frontmatter` L91 | CONFIRMED |
| §MVR §2: `executor.py:1899` `build_certify_step` | research/01 §A.1 — `build_certify_step` L1899 | CONFIRMED |
| §MVR §4: `fidelity_checker.py:165-200` AST scan | research/01 §A.4 — `FidelityChecker` class L143, scan helpers around L165-200 | CONFIRMED (range, exact entry per inventory) |
| §MVR §4: `fidelity_checker.py:287-303` fail-open | research/01 §A.4 — L287-303 fail-open verbatim cited | CONFIRMED |
| Vector A: `executor.py:1947-2025` `_build_steps` | research/01 §A.1 — `_build_steps` L1947, full step list | CONFIRMED |
| Vector A: `gates.py:317-383` semantic check region | research/01 §A.2 — 35 semantic-check functions enumerated | CONFIRMED (region) |
| R1.6: `executor.py:2167` `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` | research/01 §A.1 R1.6 row — L2167 verbatim | CONFIRMED |
| R1.6 audit: `obligation_scanner.py` L719/L722/L725/L729/L733/L737/L741/L760 `return True` stubs | research/01 §A.4 — all 8 verbatim | CONFIRMED |
| R1.6 audit: `remediate_executor.py` L326/L345/L362/L397/L412/L423/L706 `return True` stubs | research/01 §A.6 — all 7 verbatim | CONFIRMED |
| R1.6 audit: `gates.py:_cross_refs_resolve` L48-91 return-True stub | research/01 §A.2 — `_cross_refs_resolve` L48, returns True L88-91 | CONFIRMED |

### Skill protocol citations

| BUILD-REQUEST citation | Inventory location | Status |
|---|---|---|
| `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | research/01 §D — 1,094 LOC | CONFIRMED |
| `refs/extraction-pipeline.md` | research/01 §D — 700 LOC | CONFIRMED |
| `refs/templates.md` | research/01 §D — 519 LOC | CONFIRMED |
| `refs/adversarial-integration.md` (PRESERVE) | research/01 §D — 692 LOC, PRESERVE per MVR | CONFIRMED |
| `refs/scoring.md` | research/01 §D — 322 LOC | CONFIRMED |
| `refs/validation.md` | research/01 §D — 474 LOC | CONFIRMED |

### Preserve-axis citations

| BUILD-REQUEST citation | Inventory location | Status |
|---|---|---|
| `commands.py` 20 `--flag` options + 2 subcommands (PRESERVE) | research/01 §A.1 — `run(...)` L175, `accept_spec_change(...)` L303, `validate(...)` L353 | CONFIRMED |
| `structural_checkers.py` (PRESERVE) | research/01 §A.3 — 1,069 LOC, 5 structural checkers | CONFIRMED |
| `convergence.py` (PRESERVE) | research/01 §A.3 — 778 LOC, `compute_stable_id` L63 | CONFIRMED |
| `cosmetic_remediator.py` (PASSTHROUGH) | research/01 §A.8 — 1,096 LOC | CONFIRMED |

## 5. Acceptance Gates (8 items, from §Acceptance gates section)

| # | Item | Verification phase | Step count delta |
|---|---|---|---|
| 1 | All Contract items 1-10 enforced as CI gates | Phase 13 (Step 13.4, 13.7) | N/A |
| 2 | All current passing tests in `tests/roadmap/` still pass | Phase 13 (Step 13.5) | N/A |
| 3 | Pipeline runs on every spec under `.dev/releases/complete/*/spec*.md` without halts | Phase 13 (Step 13.6) | N/A |
| 4 | Recurrence corpus seeded — ≥1 fixture per RECURRENT row #1,2,4,5,6,7,8,9,10,12,14,15,16,17,19,20,21,22 (18 fixtures min) | Phase 13 (Step 13.1, 13.2) | N/A |
| 5 | MultiModelSwarm anti-instinct halt resolved | Phase 5 (Step 5.2) — R0 milestone | N/A |
| 6 | Step count does not increase — final ≤ current (14) | Phase 13 (Step 13.7) | R1.5 adds verify-implementation; R1.6 consolidates ≥1 step (or verify-implementation replaces wiring-verification) |
| 7 | Zero `return True` fragility stubs in `src/superclaude/cli/` | Phase 11 (Step 11.4, 11.5) | N/A |
| 8 | `verify-implementation` terminal step live and wired | Phase 10 (R1.5) | net +1 step → mitigated by gate #6 |

## 6. C1 Remediation (sc:reflect Tier-2) — Frontmatter Parser Canonicalization

Per launch instruction #6: "DELETE both `_check_frontmatter` AND `_parse_frontmatter`; canonical parser is the PipelineEnvelope post-step extractor. There is no `superclaude.contracts.parsers` submodule."

The frontmatter parser landscape per research/01 §B (6 variants):

1. `src/superclaude/cli/roadmap/gates.py:_parse_frontmatter` L168 — **DELETE in R1.6 Step 11.2** (C1)
2. `src/superclaude/cli/pipeline/gates.py:_check_frontmatter` L91 — **DELETE in R1.6 Step 11.2** (C1)
3. `src/superclaude/cli/roadmap/spec_parser.py:parse_frontmatter` L109 — keep (third parser variant, also Contract #6 ripple)
4. `src/superclaude/cli/roadmap/spec_patch.py:_extract_frontmatter` L285 — **DELETE in R1.6** (research/01 §A.7)
5. `src/superclaude/cli/cli_portify/utils.py:parse_frontmatter` L11 — out-of-scope (cli_portify subsystem)
6. `src/superclaude/cli/audit/wiring_gate.py:_extract_frontmatter_values` L931 — Contract #6 ripple

**Canonical post-rewrite:** PipelineEnvelope post-step extractor parses frontmatter once at extract time and persists to sidecar JSON. All downstream consumers read from envelope, not from re-parsing markdown. No `superclaude.contracts.parsers` submodule exists or should exist.

## 7. Hard Constraints from BUILD-REQUEST

- "The task-builder MUST NOT invent new requirements. If a checklist item cannot be sourced to one of the 6 file sets above, drop it." — applies recursively to in-flight phase findings.
- "Sync `src/superclaude/` → `.claude/` via `make sync-dev` before any commits (CLAUDE.md absolute rule)."
- "PR target: `IronbellyOrg/IronClaude` only (CLAUDE.md absolute rule). NEVER `gh pr create` without `--repo IronbellyOrg/IronClaude`."
- "NEVER stage `.claude/{skills,commands,agents,hooks,templates}/*` (CLAUDE.md absolute rule)."
- "R1 should land step-by-step with at-least-one-release-cycle co-existence per migrated step."

## 8. Drift Check Verdict

**Zero drift detected.** Every file:line citation in the BUILD-REQUEST is found verbatim in `research/01-file-inventory.md`. All file path references resolve to inventoried files (or are explicitly enumerated as NEW files for creation in R0/R1).

The BUILD-REQUEST is consistent with the file inventory and is safe to cite by section anchor in subsequent checklist items.

## 9. Next-Phase Citation Style (for Phase 2+ items)

Subsequent items should cite using:

- BUILD-REQUEST: `BUILD-REQUEST §Contract #N`, `BUILD-REQUEST §MVR §N`, `BUILD-REQUEST §R0 item N`, `BUILD-REQUEST §R1.N`, `BUILD-REQUEST §Acceptance gate #N`
- Master report: `master:§Flaw N`, `master:§Recurrence #N`, `master:§Verdict`
- File inventory: `research/01 §A.N`, `research/01 §B`, `research/01 §F`
- Patterns research: `research/02 §N`
- Template research: `research/03 §N`

This index file itself is cited as `phase-outputs/discovery/build-request-index.md` and supersedes ad-hoc rederivation.
