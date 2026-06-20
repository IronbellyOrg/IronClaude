# Research Notes: Roadmap Pipeline Brittleness-Elimination Refactor + Rewrite

**Date:** 2026-05-31
**Scenario:** A (Explicit) — BUILD-REQUEST is highly structured with R0/R1 phasing, MVR spec, Brittleness-Elimination Contract, file:line citations sourced from a 27-agent retrospective
**Depth Tier:** Deep (~2,800 LOC delta, 6 subsystems, two-phase R0+R1)
**Track Count:** 1 (R0 and R1 share substrate work — `superclaude.contracts` starts in R0 and extends in R1; not independent enough to split)
**BUILD-REQUEST path:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md`
**Authoritative evidence corpus:** 14 partition reports + master report + 4 vector analyses + observed runtime data — ~430KB across `wave1-partition-reports/`, `wave2-master-report/`, `wave3-vector-analyses/`

---

## EXISTING_FILES

### `src/superclaude/cli/roadmap/` (24 files, 16,698 LOC)

| File | LOC | Role | Touched by R0/R1 |
|---|---|---|---|
| `executor.py` | 3,701 | Central pipeline orchestrator — `_build_steps`, `execute_pipeline`, step dispatch, gate evaluation | R1.3 (GateCriteria slot), R1.5 (verify-implementation wiring), R1.6 (cleanup gate=None bypass at L2167) |
| `gates.py` | 1,441 | Gate registry — `SemanticCheck` signatures, gate predicates (anti-instinct, spec-fidelity, wiring-verification, etc.), `_cross_refs_resolve` stub at L82, gate criteria at L317-383 | R0.3 (contracts registry), R1.3 (GateCriteria.code_assertions slot), R1.6 (delete `_cross_refs_resolve` stub) |
| `prompts.py` | 1,367 | LLM prompt builders for all generator stages — `build_extract_prompt`, `build_generate_prompt`, `build_merge_prompt`, `build_remediate_prompt`, etc. (~85K tokens of prompt strings) | R1.4 (tool-write rewrite for 9 LLM steps) |
| `cosmetic_remediator.py` | 1,096 | Post-merge cosmetic fix layer | R1 (passthrough; not primary target) |
| `structural_checkers.py` | 1,069 | v3.05 deterministic structural-check layer — **PRESERVE per MVR** | R1.1 (no changes); contract documents this as preserved |
| `remediate_executor.py` | 859 | Remediate-step execution | R1 (envelope migration; possibly tool-write) |
| `obligation_scanner.py` | 825 | Anti-instinct scanner — Layer 1-5 detectors, current direct ancestor of MultiModelSwarm FP per master:§Recurrence#6 | R0.2 (allowlist add); R1.4 (regenerate as tool-write?) |
| `convergence.py` | 778 | Convergence wrapper concept — **PRESERVE per MVR** | R1 (envelope migration only) |
| `semantic_layer.py` | 692 | Semantic-check helpers | R1 (envelope migration) |
| `spec_parser.py` | 639 | Spec parsing | R0.1 (ID extraction), R1.4 (tool-write?) |
| `validate_executor.py` | 519 | Validate-step execution | R1 (envelope migration) |
| `integration_contracts.py` | 477 | Integration contract checking | R0.3, R1.1 (contract registry) |
| `remediate.py` | 433 | Remediate-step prompt + helpers | R1.4 (tool-write) |
| `fidelity_checker.py` | 417 | Spec-fidelity checker — fail-open default at L287-303 per master:§Flaw 4 | R0.1 (ID-set containment), R1.5 (verify-implementation AST link), R1.6 (delete fail-open default) |
| `commands.py` | 401 | Click CLI surface — **PRESERVE per MVR** (Vector A explicit) | R1 (no changes) |
| `remediate_parser.py` | 391 | Remediate-output parser | R1.4 (tool-write makes parser deterministic) |
| `certify_prompts.py` | 337 | Certify prompts | R1.4 (tool-write); already evidenced as dead code per master:§Recurrence#2 |
| `spec_patch.py` | 304 | Spec-patch helpers | R1 (envelope migration) |
| `fingerprint.py` | 216 | Fingerprint extraction | R0.2 (vocab-lint extends fingerprints) |
| `validate_prompts.py` | 197 | Validate prompts | R1.4 (tool-write) |
| `models.py` | 143 | Dataclasses — `RoadmapConfig` (L94-127) holds only inputs/flags, no cross-step state | R1.2 (add `PipelineEnvelope` here or new `envelope.py`) |
| `remediate_prompts.py` | 134 | Remediate prompts | R1.4 (tool-write) |
| `spec_structural_audit.py` | 111 | Spec structural audit | R0.1 |
| `templates.py` | 71 | Markdown templates | R1.4 (Jinja templates for tool-write rendering) |

### `tests/roadmap/` (64 test files, 28,036 LOC)

Existing testing infrastructure: pytest, fixtures, conftest. 64 test files cover the current pipeline; recurrence-corpus seed cases need to be added per Contract item #1. New test files to create per Contract:

- `tests/roadmap/test_recurrence_regression.py` (Contract #1)
- `tests/roadmap/test_dispatch_reachability.py` (Contract #2)
- `tests/roadmap/test_gate_empty_target.py` (Contract #4)
- `tests/roadmap/test_no_fragility_stubs.py` (Contract #5; CI lint)
- `tests/roadmap/test_parser_consistency.py` (Contract #6)
- `tests/roadmap/test_retry_contract.py` (Contract #7)
- `tests/roadmap/test_threshold_registry.py` (Contract #8)
- `tests/roadmap/test_spec_roadmap_id_containment.py` (Contract #9)
- `tests/roadmap/test_anti_instinct_recurrence.py` (Contract #10)
- `tests/roadmap/fixtures/recurrence/` (directory tree for seeded fixtures)

### `src/superclaude/contracts/` — **DOES NOT EXIST**

Must be created per MVR §5 (R0.3 starts it; R1.1 extends it). Initial content:
- `__init__.py` — exports `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`, `RETURN_CONTRACTS`
- Arch-lint extension to flag re-definitions of registry constants

### `src/superclaude/skills/sc-roadmap-protocol/`

- `SKILL.md` — top-level skill prose; needs alignment with new envelope/registry per master:§Flaw 5
- `refs/extraction-pipeline.md` — extract step prose
- `refs/templates.md` — output templates
- `refs/adversarial-integration.md` — adversarial debate prose (preserve)
- `refs/scoring.md` — scoring prose
- `refs/validation.md` — validation gate prose

### Authoritative retrospective corpus (read-only inputs to the task)

- Master report: 961 lines, REWRITE verdict, 5 flaws
- Vector A (Architecture): MVR specification (embedded verbatim in BUILD-REQUEST)
- Vector B (Process): non-architectural failures + input-quality contract
- Vector C (Recurrence): Brittleness-Elimination Contract (embedded verbatim in BUILD-REQUEST)
- Vector D (Cost): R0/R1 phasing rationale + token-economics
- 14 partition reports A1a-A12

---

## PATTERNS_AND_CONVENTIONS

### Codebase conventions (from CLAUDE.md + observation)

- **UV-only Python ops** — `uv run pytest`, `uv pip install`, never bare `pip` or `python -m`
- **Sync discipline** — `src/superclaude/` is SoT; `make sync-dev` mirrors to `.claude/`; `.claude/` is gitignored except `settings.json`
- **PR target** — `IronbellyOrg/IronClaude` only; never upstream
- **Pre-commit hooks** — verify-sync, markdownlint, ruff lint, ruff format
- **Test markers** — `@pytest.mark.confidence_check`, `@pytest.mark.self_check`, `@pytest.mark.reflexion`, auto-markers for `/unit/` and `/integration/`
- **Branch policy** — `master` ← `integration` ← `feature/*`; never direct to master

### Pipeline code patterns

- **Gate signature** (current — INHERENT FLAW per Vector A): `SemanticCheck = Callable[[str], bool]` at `gates.py:317-383`
- **Step list** (current): `_build_steps(config) -> list[Step | list[Step]]` at `executor.py:1947`
- **Frontmatter parsers** (TWO disagreeing variants — Contract #6 target):
  - `_parse_frontmatter` (gates.py)
  - `_check_frontmatter` (different module)
- **State persistence** (current): `.roadmap-state.json` per release dir — partial; LLM-self-reported
- **Convergence wrapper**: `convergence.py` — preserve per MVR

### MDTM Template 02 conventions (target output)

- Per-item structure: Context + Action + Output + Verification + Completion gate
- Granularity: one item per file/component, NOT batch items
- Self-contained: each item readable without external context
- Phase ordering: dependencies explicit
- L1-L6 handoff patterns for subagent spawning

---

## GAPS_AND_QUESTIONS

1. **R0/R1 boundary on `superclaude.contracts`.** R0 starts the module (minimal `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`); R1 extends with full `RETURN_CONTRACTS` + arch-lint. The task needs to be clear about which constants land in R0 vs R1.
2. **Tool-write rewrite migration strategy.** Vector A specifies "Stage one step at a time, run side-by-side against current markdown output for ≥3 releases each before deletion." The task needs concrete cutover criteria per step.
3. **PipelineEnvelope migration.** Dual-write envelope + markdown for one release cycle, then markdown becomes render-only. Cutover criterion: what triggers the deletion of markdown-as-substrate code?
4. **Existing `.claude/skills/sc-roadmap-protocol/` skill prose updates.** SKILL.md and refs files describe current pipeline; updates required after R1 lands. Worth a dedicated migration phase.
5. **Recurrence corpus seeding source.** Contract #1 requires ≥1 fixture per RECURRENT failure (master report rows #1-22). The task needs to enumerate which fixtures come from which historical incidents.

---

## RECOMMENDED_OUTPUTS

The generated MDTM task file must contain phases approximately:

- **Phase 1:** R0 Preparation — read master/vectors, verify file:line citations still match (already done above; codify)
- **Phase 2:** R0.1 — Spec-ID registry (`id_registry.py`, fidelity_checker integration, ID-containment test)
- **Phase 3:** R0.2 — Anti-instinct vocab-lint allowlist (obligation_scanner extension, MultiModelSwarm seed fixtures, test)
- **Phase 4:** R0.3 — `superclaude.contracts` minimal SoT module + arch-lint
- **Phase 5:** R0 acceptance — CI gates wired, MultiModelSwarm run passes anti-instinct
- **Phase 6:** R1.1 — Extend `superclaude.contracts` with `RETURN_CONTRACTS`, threshold registry, arch-lint coverage
- **Phase 7:** R1.2 — `PipelineEnvelope` dataclass + sidecar JSON persistence + post-step extractors + dual-write migration
- **Phase 8:** R1.3 — `GateCriteria.code_assertions` slot + first `CodeAssertion` (build_certify_step wiring)
- **Phase 9:** R1.4 — Tool-write rewrite for 9 LLM steps (sub-phases per step, with side-by-side validation)
- **Phase 10:** R1.5 — `verify-implementation` terminal step
- **Phase 11:** R1.6 — Cleanup (delete duplicate parsers, return-True stubs, fail-open defaults)
- **Phase 12:** Skill protocol alignment (sc-roadmap-protocol prose updates)
- **Phase 13:** Final acceptance gates (all Contract items 1-10 CI-enforced, recurrence corpus complete, end-to-end runs pass, step count ≤14)
- **Phase 14:** Task completion (frontmatter status update, summary)

---

## SUGGESTED_PHASES (Researcher assignments)

The BUILD-REQUEST is already evidence-grounded from a 27-agent retrospective. Researchers focus on **current codebase state at file:line granularity** needed to write granular per-file/per-component checklist items — NOT re-discovering the retrospective. Minimum 3 researchers per skill rules.

### Researcher R1 — File Inventory (Current Pipeline)
**Scope:** All 24 files under `src/superclaude/cli/roadmap/`, plus `tests/roadmap/`, plus skill protocol files at `src/superclaude/skills/sc-roadmap-protocol/`
**Focus:** Per-file inventory: purpose, key exports, dependencies, expected R0/R1 touch points. The task builder will create one checklist item per touched file.
**Output:** `${TASK_DIR}research/01-file-inventory.md`
**Other researchers cover:** Patterns (R2), MDTM templates (R3).

### Researcher R2 — Patterns & Conventions (Current Pipeline)
**Scope:** Read 5-6 representative pipeline files in detail — `executor.py` (sections around `_build_steps`/gate dispatch), `gates.py` (SemanticCheck signatures, gate registry), `fidelity_checker.py` (fail-open default), `obligation_scanner.py` (Layer 1-5 detectors), `convergence.py` (preserve target), `commands.py` (preserve target).
**Focus:** Current naming, gate-registration patterns, frontmatter parser variants (Contract #6), `return True` stubs (Contract #5), `gate=None` bypasses, fail-open defaults. Cite file:line.
**Output:** `${TASK_DIR}research/02-patterns-conventions.md`
**Other researchers cover:** File inventory (R1), MDTM templates (R3).

### Researcher R3 — MDTM Template + Recurrence-Corpus Precedent
**Scope:** Read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 completely. Browse `.dev/tasks/done/` for similar prior tasks (large rewrite/refactor) — especially `TASK-RF-20260527-043715-sc-reflect-rebuild/`, `TASK-RF-20260527055700-spec-fidelity-canonicalizer/`. Browse `tests/roadmap/` for any existing fixtures/recurrence patterns.
**Focus:** Template 02 rules (especially A3 granular breakdown, B2 self-contained items, L1-L6 handoff). Successful precedent for multi-phase refactor tasks. Where recurrence fixtures should live and what format they take.
**Output:** `${TASK_DIR}research/03-template-and-precedent.md`
**Other researchers cover:** File inventory (R1), patterns (R2).

---

## TEMPLATE_NOTES

**Template selection:** **02 (Complex)** — discovery + multi-phase build + tests + cleanup + migration. R0/R1 phasing + 9-LLM-step tool-write rewrite + recurrence corpus + skill prose alignment justifies complex template.

**Tier selection:** **Deep** — 14 expected phases, ~2,800 LOC across 6 subsystems, ~10-12 eng-weeks total estimated. Far above the >20-file Deep threshold.

**Specific MDTM features the task should use:**
- Per-phase QA gates: rf-analyst + rf-qa after each major phase (R0 acceptance, R1.1, R1.2, R1.3, R1.4 per-step, R1.5, R1.6)
- Recurrence corpus: a sub-tree of fixtures keyed by failure class (Contract #1)
- Side-by-side validation phases: dual-write envelope vs markdown until cutover (R1.2); tool-write vs markdown per LLM step (R1.4 sub-phases)
- CI gate wiring as explicit checklist items (Contract items 1-10)
- `pre-commit` config updates as explicit items (arch-lint hooks)

---

## AMBIGUITIES_FOR_USER

None blocking — intent is clear from the BUILD-REQUEST, master report, and 4 vector analyses. Genuine ambiguities (R0/R1 boundary on contracts module, tool-write migration cadence) are documented in GAPS_AND_QUESTIONS for the task builder to address via Open Questions in the final task file.
