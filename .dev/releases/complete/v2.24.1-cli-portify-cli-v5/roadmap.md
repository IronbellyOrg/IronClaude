---
spec_source: "portify-release-spec.md"
complexity_score: 0.65
adversarial: true
---

# Roadmap: CLI Portify v2.24.1 — Multi-Form Target Resolution & Component Tree Discovery

## Executive Summary

This release extends the CLI Portify pipeline to accept 6 input forms (bare command name, prefixed name, command path, skill directory, skill name, SKILL.md path) instead of just skill directory paths. It adds a deterministic resolution layer (`resolution.py`), hierarchical component tree discovery (commands + skills + agents with tiered subcomponents), enriched artifact output, and controlled subprocess directory scoping — all without modifying base `pipeline/` or `sprint/` modules.

The work is a bounded MEDIUM-complexity extension (0.65): one new module (`resolution.py`), modifications to 6 existing files, ~37 new tests across 4 phases. The primary architectural risk is backward compatibility across the expanded input surface. All new logic is synchronous and deterministic, preserving existing behavior for current skill-directory inputs while broadening supported target types.

The roadmap prioritizes resolution correctness first, data model and discovery integrity second, CLI integration and subprocess scoping third, with validation woven throughout. The `resolution_log` serves as a first-class observability asset for debugging, operator trust, and future v2.25 design decisions.

---

## Phased Implementation Plan

### Phase 1: Data Model, Resolution Core & Algorithm

**Goal**: Ship the resolution algorithm and data model additions so all 6 input forms resolve to a `ResolvedTarget`. Models and resolution are combined because they are tightly coupled — `ResolvedTarget` is meaningless without the algorithm that produces it, and the algorithm can't be tested without the models it returns.

**Milestone A**: `resolve_target()` passes all 6 input form tests with models reviewable in context.

#### Prerequisites (Architecture Constraints)

- No edits to `pipeline/` or `sprint/` (NFR-WORKFLOW.2)
- No `async def` or `await` (NFR-WORKFLOW.3)
- No step renumbering
- `Path` internally, `str` at backward-compat boundaries
- Dependency direction: `cli.py → resolution.py → models.py`

#### Tasks

1. **FR-PORTIFY-WORKFLOW.2e** — Add `AgentEntry`, `CommandEntry`, `SkillEntry`, `ComponentTree` dataclasses to `models.py`. Extend `PortifyConfig` with 10 new fields. Preserve `ComponentEntry.path: str`.
2. **FR-PORTIFY-WORKFLOW.1a** — Input validation (Step R0): reject empty/whitespace/None targets, strip whitespace, handle `"sc:"` edge case.
3. **FR-PORTIFY-WORKFLOW.1b** — Input classification into `TargetInputType` enum (5 values: `COMMAND_NAME`, `COMMAND_PATH`, `SKILL_DIR`, `SKILL_NAME`, `SKILL_FILE`).
4. **FR-PORTIFY-WORKFLOW.1c** — Command resolution (Step R1): locate `.md` in `commands_dir`, parse YAML frontmatter, parse `## Activation` for skill reference. Reverse-resolve for skill inputs.
5. **FR-PORTIFY-WORKFLOW.1d** — Skill resolution (Step R2): construct `sc-<name>-protocol` directory name, locate in `skills_dir`, validate `SKILL.md` exists.
6. **FR-PORTIFY-WORKFLOW.1e** — Ambiguity resolution: `ERR_AMBIGUOUS_TARGET` for multiple matches within same class. Command-first policy for bare names.
7. **FR-PORTIFY-WORKFLOW.1f** — Skill-less command guard: skip R3/R4 when `skill_dir` is `None`, proceed to R5 with empty agents/refs/rules/templates/scripts. Emit `"Standalone command"` in `resolution_log`.
8. **FR-PORTIFY-WORKFLOW.1g** — Project root auto-detection: walk up to find `src/superclaude/` or `pyproject.toml`, fall back to CWD. Support `--commands-dir`, `--skills-dir`, `--agents-dir` overrides with actionable error messages on failure.
9. Add `time.monotonic()` instrumentation for sub-second performance verification (NFR-WORKFLOW.1).

#### Validation

- **NFR-WORKFLOW.1**: All 6 forms resolve in <1s (instrumented).
- **NFR-WORKFLOW.3**: No `async def` or `await` in `resolution.py`.
- **NFR-WORKFLOW.4**: Existing `resolve_workflow_path()` preserved unchanged; `TARGET` is a superset.
- **SC-3**: 6 input forms resolve correctly.
- **SC-10**: Sync-only enforcement via grep check.

#### Tests (~15)

Unit tests for each input form, edge cases (empty, `sc:`, nonexistent), ambiguity, command-first policy, root detection fallback, standalone command path.

#### Risks Addressed

| Risk | Severity | Governance | Mitigation | Contingency |
|------|----------|------------|------------|-------------|
| RISK-2: Backward compat break | High | Release-blocking | Preserve `resolve_workflow_path()` unchanged; TARGET is a superset; regression fixtures for current skill-directory flows | Narrow new resolution logic to explicit new input forms only; preserve legacy path-first routing for old forms |
| RISK-5: Root detection fails | Low | Managed | Explicit `--*-dir` overrides as escape hatch with helpful error messages | Promote override flags in operator docs or CLI help |
| RISK-6: Naming convention fragility | Low | Managed | Best-effort reverse-resolution with warning, not error; standalone skills remain valid | Add explicit metadata linkage in future release if naming drift appears |

#### Exit Criteria

- All six input forms resolve to `ResolvedTarget` with correct classification.
- Performance instrumentation confirms <1s resolution.
- Existing skill-directory workflow behavior unchanged.
- `resolution_log` captures resolution path for all forms.

**Estimated effort**: 2–3 days

---

### Phase 2: Component Tree Discovery & Agent Extraction

**Goal**: Build the hierarchical `ComponentTree` with Tier 0 (command), Tier 1 (skill + subdirectories), and agent entries.

**Milestone B**: `run_discover_component_tree()` produces a complete `ComponentTree` for a standard workflow.

#### Tasks

1. **FR-PORTIFY-WORKFLOW.2a** — Agent extraction (Step R3): parse SKILL.md with 6 `AGENT_PATTERNS` regexes, resolve to `agents_dir/<name>.md`, record found/missing status, deduplicate by name.
2. **FR-PORTIFY-WORKFLOW.2b** — Manual agent injection via `--include-agent`: resolve by name or path, ignore empty values, deduplicate (manual overrides auto-discovered via `referenced_in="cli-override"`).
3. **FR-PORTIFY-WORKFLOW.2c** — Tier 2 inventory (Step R4): scan `refs/` → `.md`, `rules/` → all files, `templates/` → all files, `scripts/` → all files.
4. **FR-PORTIFY-WORKFLOW.2d** — ComponentTree assembly (Step R5): assemble all components with `Path`-based dataclasses.
5. **FR-PORTIFY-WORKFLOW.2h** — Discovery refactoring: new `run_discover_component_tree()` entry point; existing `run_discover_components()` becomes thin wrapper calling new function + `to_flat_inventory()`.
6. **FR-PORTIFY-WORKFLOW.2i** — `derive_cli_name()` enhancement: prefer `command_path.stem` when available, fall back to existing skill-name derivation.

#### Validation

- **NFR-WORKFLOW.4**: Existing test suite passes unchanged — `to_flat_inventory()` produces identical `ComponentInventory`.
- **SC-4**: Missing agents produce warnings, not errors.
- **SC-5**: `--include-agent` injects agents into tree with correct deduplication.
- **SC-7**: Existing tests pass.

#### Tests (~12)

Agent extraction (found, missing, dedup), manual injection, tier 2 scan, `to_flat_inventory()` backward compat, standalone command (no skill) produces empty tree.

#### Risks Addressed

| Risk | Severity | Governance | Mitigation | Contingency |
|------|----------|------------|------------|-------------|
| RISK-1: Agent regex misses | Medium | Release-gating | Implement all 6 known patterns; `--include-agent` escape hatch; mark missing agents as warnings; log gaps in `resolution_log` | Maintain pattern audit list for v2.25 updates based on observed misses |
| RISK-4: YAML parse failures | Low | Managed | Treat frontmatter as additive metadata, not hard dependency; fall back to naming conventions; emit warnings instead of aborting | Add malformed fixture tests to prevent crash regressions |

#### Exit Criteria

- Discovery produces complete trees for standard and standalone workflows.
- Missing agents degrade gracefully with warnings.
- `to_flat_inventory()` backward compatibility confirmed.
- `resolution_log` records extraction gaps.

**Estimated effort**: 2 days

---

### Phase 3: CLI Integration & Artifact Enrichment

**Goal**: Wire resolution and discovery into the CLI, enrich `component-inventory.md`, add `--save-manifest`. This phase isolates the high-risk `WORKFLOW_PATH → TARGET` user-facing argument change for focused review.

**Milestone C**: `superclaude cli-portify run roadmap --dry-run` produces enriched inventory with command/agent sections.

#### Tasks

1. **CLI argument change** — Replace `WORKFLOW_PATH` with `TARGET` argument (remove `exists=True` constraint). Add `--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest` options via Click decorators.
2. **FR-PORTIFY-WORKFLOW.2f** — Enriched `component-inventory.md`: add `## Command`, `## Agents`, `## Cross-Tier Data Flow`, `## Resolution Log` sections. New frontmatter fields: `source_command`, `source_skill`, `agent_count`, `has_command`, `has_skill`.
3. **FR-PORTIFY-WORKFLOW.2g** — `--save-manifest`: serialize `ComponentTree` via `to_manifest_markdown()` after Step 2. Write-only in v2.24.1.
4. **SC-11 compliance** — Ensure `ValidateConfigResult.to_dict()` includes `warnings`, `command_path`, `skill_dir`, `target_type`, `agent_count`.

#### Validation

- **NFR-WORKFLOW.2**: Zero changes to `pipeline/` or `sprint/` — verified via `git diff --name-only`.
- **SC-1**: Dry-run produces enriched inventory.
- **SC-2**: Existing skill-dir input produces identical behavior plus additional discovery.
- **SC-6**: `--save-manifest` writes valid Markdown manifest.
- **SC-9**: No base-module changes.
- **SC-11**: `to_dict()` field completeness verified.

#### Tests (~5)

CLI argument parsing, enriched artifact content validation, manifest output, `to_dict()` field presence.

#### Risks Addressed

| Risk | Severity | Governance | Mitigation | Contingency |
|------|----------|------------|------------|-------------|
| RISK-2: CLI argument change | High | Release-blocking | Existing `WORKFLOW_PATH` inputs continue to work as `TARGET` is a superset; regression against v2.24 baseline | Revert to `WORKFLOW_PATH` with optional `--target` flag if breakage detected |

#### Exit Criteria

- `WORKFLOW_PATH → TARGET` migration passes all existing CLI tests.
- Enriched inventory contains all required sections and frontmatter.
- `to_dict()` serialization includes all new fields without breaking downstream consumers (`contract.py`, `resume.py`).

**Estimated effort**: 1–2 days

---

### Phase 4: Subprocess Scoping & Directory Consolidation

**Goal**: Extend `PortifyProcess` to pass discovered directories to Claude subprocesses with controlled scoping.

**Milestone D (partial)**: Subprocess invocations include all component directories via `--add-dir` with consolidation.

#### Tasks

1. **FR-PORTIFY-WORKFLOW.3a** — Add `additional_dirs: list[Path] | None = None` to `PortifyProcess.__init__()`. Normalize all paths with `.resolve()`.
2. **FR-PORTIFY-WORKFLOW.3b** — Deduplication in `_build_add_dir_args()`: `set[Path]` across work_dir, workflow_path, and all additional_dirs.
3. **FR-PORTIFY-WORKFLOW.3c** — Directory cap and consolidation: >10 dirs triggers warning, group by nearest common parent (2-level depth via `os.path.commonpath`), replace with parent if ≤3x file count, fall back to top-10 by component count. Record all consolidation decisions in `resolution_log`.
4. Verify `additional_dirs=None` preserves existing v2.24 behavior.

#### Validation

- **NFR-WORKFLOW.5**: Warning emitted at >10 dirs.
- **SC-12**: Consolidation triggers with warning and log entries.
- Existing behavior preserved when `additional_dirs=None`.

#### Tests (~5)

Deduplication, consolidation trigger, fallback behavior, None passthrough, diagnostic output verification.

#### Risks Addressed

| Risk | Severity | Governance | Mitigation | Contingency |
|------|----------|------------|------------|-------------|
| RISK-3: `--add-dir` explosion | Medium | Release-gating | Cap at 10 with consolidation algorithm; dedup by resolved path; warning logs | Add diagnostic output to clarify which directories were retained or collapsed |

#### Exit Criteria

- Add-dir generation is deterministic and deduplicated.
- Over-scoping controlled via cap and consolidation.
- Existing v2.24 behavior unchanged when `additional_dirs=None`.
- `resolution_log` records consolidation decisions.

**Estimated effort**: 1 day

---

### Phase 5: Integration Testing & Final Validation

**Goal**: Full end-to-end validation across all input forms, backward compatibility, and NFR enforcement.

**Milestone D (complete)**: All ~37 new tests pass, existing suite unchanged, all 12 success criteria met.

#### Tasks

1. Run full test suite: `uv run pytest` — confirm zero regressions.
2. Verify NFR-WORKFLOW.2: `git diff --name-only` shows no `pipeline/` or `sprint/` changes.
3. Verify NFR-WORKFLOW.3: `grep -r "async def\|await"` on new/modified files returns empty.
4. End-to-end smoke tests for SC-1 through SC-12.
5. Document decisions on open questions OQ-1 through OQ-7 — confirm deferral to v2.25 with tracking issues.

#### Exit Criteria

- All 12 success criteria (SC-1 through SC-12) green.
- All 5 NFRs verified with evidence.
- No unresolved high-severity compatibility risk.
- OQ-1 through OQ-7 tracked in issue tracker for v2.25.

**Estimated effort**: 1 day

---

## Risk Assessment

### Consolidated Risk Table

| Risk | Severity | Governance Tier | Phase Mitigated | Mitigation Strategy | Contingency |
|------|----------|----------------|-----------------|---------------------|-------------|
| RISK-2: Backward compat break | High | Release-blocking | 1, 3, 5 | Preserve `resolve_workflow_path()`; TARGET superset of WORKFLOW_PATH; full existing test suite; gate on SC-2, SC-7, SC-9 | Narrow new resolution to explicit new input forms only; preserve legacy path-first routing |
| RISK-1: Agent regex misses | Medium | Release-gating | 2 | All 6 patterns; `--include-agent` escape hatch; warnings not errors; `resolution_log` gaps | Pattern audit list for v2.25 based on observed misses |
| RISK-3: `--add-dir` explosion | Medium | Release-gating | 4 | Cap at 10; consolidation algorithm; dedup by resolved path; warning logs | Diagnostic output for retained/collapsed directories |
| RISK-4: YAML parse failures | Low | Managed | 2 | Additive metadata, not hard dependency; convention-based fallback; warnings not aborts | Malformed fixture tests to prevent crash regressions |
| RISK-5: Root detection fails | Low | Managed | 1 | `--*-dir` overrides; actionable error messages; fallback chain | Promote override flags in docs/help |
| RISK-6: Naming convention fragility | Low | Managed | 1 | Best-effort with warning; standalone skills valid; post-release audit | Explicit metadata linkage in future release |

### Governance Definitions

- **Release-blocking**: Must be resolved before release. Unresolved = no-go.
- **Release-gating**: Must be mitigated to warning-only degradation. Unresolved hard failures = no-go.
- **Managed**: Monitored with observability. Acceptable to ship with known limitations if warnings are in place.

---

## Resource Requirements

### Engineering Resources

1. **Primary backend/CLI engineer** — Implements resolution, discovery, models, CLI wiring, and process changes.
2. **QA-focused engineer or reviewer** — Builds regression fixtures and validates all 12 success criteria.
3. **Architect/reviewer** — Verifies boundary discipline, compatibility posture, and downstream contract safety.

### Technical Dependencies

#### Internal (must exist before Phase 1)

- `models.py` — existing `ComponentEntry`, `ComponentInventory`, `PortifyConfig`
- `discover_components.py` — existing discovery logic to wrap
- `process.py` — existing `PortifyProcess` / `ClaudeProcess`
- `contract.py`, `resume.py` — downstream consumers of `ValidateConfigResult`

#### External

- **Click** >=8.0.0 — CLI framework (already in deps)
- **Python stdlib**: `pathlib.Path`, `re`, `os.path.commonpath`, `time.monotonic`
- **UV toolchain** — all execution via `uv run`

### Module Dependency Graph

```
cli.py → resolution.py → models.py
discover_components.py → resolution.py → models.py
process.py → models.py
```

No circular dependencies. `resolution.py` is the single new module.

### Architectural Dependency Sequencing

1. `models.py` dataclasses must land with resolution logic (Phase 1 — coupled by design).
2. Discovery wraps resolution output (Phase 2 depends on Phase 1).
3. CLI wires resolution + discovery together (Phase 3 depends on Phases 1–2).
4. Subprocess scoping consumes discovery output (Phase 4 depends on Phase 2).
5. Validation covers all phases (Phase 5 depends on Phases 1–4).

---

## Success Criteria Validation Matrix

| Criterion | Description | Phase | Validation Method |
|-----------|-------------|-------|-------------------|
| SC-1 | Dry-run enriched inventory | 3 | Manual + automated test |
| SC-2 | Skill-dir backward compat | 3, 5 | Existing test suite comparison to v2.24 baseline |
| SC-3 | 6 input forms resolve <1s | 1 | `time.monotonic()` instrumentation |
| SC-4 | Missing agents = warnings | 2 | Unit test with intentionally missing refs |
| SC-5 | `--include-agent` works | 2 | Unit test with dedup/override verification |
| SC-6 | `--save-manifest` output | 3 | Unit test for file structure/readability |
| SC-7 | Existing tests unchanged | 5 | `uv run pytest` full suite, zero regressions |
| SC-8 | ~37 new tests pass | 5 | `uv run pytest` with per-phase breakdown (~15+~12+~5+~5) |
| SC-9 | Zero pipeline/sprint changes | 5 | `git diff --name-only` exclusion check |
| SC-10 | No async code | 5 | `grep -r "async def\|await"` on modified files |
| SC-11 | `to_dict()` new fields | 3 | Unit test for `warnings`, `command_path`, `skill_dir`, `target_type`, `agent_count` |
| SC-12 | Dir consolidation at >10 | 4 | Unit test with >10-dir scenario |

---

## Timeline Summary

| Phase | Description | Effort | Cumulative |
|-------|-------------|--------|------------|
| 1 | Data Model & Resolution Core | 2–3 days | 2–3 days |
| 2 | Component Tree Discovery | 2 days | 4–5 days |
| 3 | CLI Integration & Artifacts | 1–2 days | 5–7 days |
| 4 | Subprocess Scoping | 1 day | 6–8 days |
| 5 | Integration & Validation | 1 day | 7–9 days |

**Total**: 7–9 working days for a single developer.

### Milestone Schedule

| Milestone | Gate | Phase | Covers |
|-----------|------|-------|--------|
| A | Resolution complete | 1 | FR-PORTIFY-WORKFLOW.1 family |
| B | Discovery complete | 2 | FR-PORTIFY-WORKFLOW.2 family |
| C | CLI integration complete | 3 | CLI wiring, artifacts, serialization |
| D | All success criteria validated | 4–5 | FR-PORTIFY-WORKFLOW.3 + SC-1 through SC-12 |

### Timeline Assumptions

1. Existing fixtures and current v2.24 behavior are available for comparison.
2. No hidden downstream consumers beyond `contract.py` and `resume.py` block `to_dict()` changes.
3. No previously unknown naming convention deviations materially affect reverse-resolution.
4. Validation runs continuously during implementation rather than being deferred to Phase 5.

---

## Open Questions Deferred to v2.25

| ID | Question | Monitoring Approach |
|----|----------|-------------------|
| OQ-1 | Recursive agent-to-agent resolution | Track requests; O(1)-depth in v2.24.1 |
| OQ-2 | `--manifest` load support | Write-only in v2.24.1; track demand |
| OQ-3 | `--exclude-component` support | Track user requests |
| OQ-4 | Multi-skill command handling | Watch for commands needing multi-skill resolution |
| OQ-5 | Agent regex completeness | Audit SKILL.md files for uncovered patterns post-launch |
| OQ-6 | Naming convention deviations | Track silent reverse-resolution failures |
| OQ-7 | `to_dict()` downstream consumers | Audit consumers beyond `contract.py` and `resume.py` |
