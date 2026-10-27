---
spec_source: "portify-release-spec.md"
generated: "2026-03-20T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 3
nonfunctional_requirements: 5
total_requirements: 8
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, cli, tooling, developer-experience]
risks_identified: 6
dependencies_identified: 7
success_criteria_count: 12
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 112.0, started_at: "2026-03-20T16:43:37.286114+00:00", finished_at: "2026-03-20T16:45:29.304795+00:00"}
---

## Functional Requirements

### FR-PORTIFY-WORKFLOW.1: Multi-Form Target Resolution

**Description**: Accept 6 input forms (bare command name, prefixed name, command path, skill directory, skill name, SKILL.md path) and resolve to a normalized `ResolvedTarget` containing the command path, skill directory, and project root.

**Acceptance Criteria**:
- `resolve_target("roadmap")` resolves to command + skill + agents
- `resolve_target("sc:roadmap")` strips prefix and resolves identically
- `resolve_target("src/.../sc-roadmap-protocol/")` backward-resolves command
- `resolve_target("nonexistent")` returns `ERR_TARGET_NOT_FOUND`
- Resolution completes in <1s for all input forms
- `--commands-dir`, `--skills-dir`, `--agents-dir` override auto-detection

**Sub-decomposition**:

- **FR-PORTIFY-WORKFLOW.1a: Input Validation (Step R0)** — Reject empty, whitespace-only, or `None` targets with `ERR_TARGET_NOT_FOUND`. Strip whitespace before classification. Return `ERR_TARGET_NOT_FOUND` for `"sc:"` (empty after prefix strip).
- **FR-PORTIFY-WORKFLOW.1b: Input Classification** — Classify target into one of 5 `TargetInputType` enum values: `COMMAND_NAME`, `COMMAND_PATH`, `SKILL_DIR`, `SKILL_NAME`, `SKILL_FILE`.
- **FR-PORTIFY-WORKFLOW.1c: Command Resolution (Step R1)** — For command inputs: locate `.md` file in `commands_dir`, parse YAML frontmatter, parse `## Activation` section for skill reference. For skill inputs: reverse-resolve command by stripping `sc-` prefix and `-protocol` suffix.
- **FR-PORTIFY-WORKFLOW.1d: Skill Resolution (Step R2)** — Construct expected directory name `sc-<name>-protocol`, locate in `skills_dir`, validate `SKILL.md` exists.
- **FR-PORTIFY-WORKFLOW.1e: Ambiguity Resolution** — `ERR_AMBIGUOUS_TARGET` only for multiple matches within the same input type class. Command-first policy: bare name matching both command and skill resolves as command.
- **FR-PORTIFY-WORKFLOW.1f: Skill-less Command Guard** — If `skill_dir` is `None` after R2, skip R3/R4, proceed to R5 with empty agents/refs/rules/templates/scripts. Log "Standalone command" in `resolution_log`.
- **FR-PORTIFY-WORKFLOW.1g: Project Root Auto-Detection** — Walk up from target path to find `src/superclaude/` or `pyproject.toml`. For bare names, search known locations. Fall back to CWD-relative paths. Suggest `--*-dir` flags on failure.

**Dependencies**: None

---

### FR-PORTIFY-WORKFLOW.2: Full Component Tree Discovery

**Description**: Build a hierarchical `ComponentTree` containing Tier 0 (command), Tier 1 (skill + refs/rules/templates/scripts), and agents. Enrich `component-inventory.md` with Command, Agents, and Data Flow sections.

**Acceptance Criteria**:
- `ComponentTree` contains `CommandEntry`, `SkillEntry`, `AgentEntry` for a standard workflow
- Agent extraction finds references matching 6 regex patterns in SKILL.md
- `--include-agent` adds manually specified agents to the tree
- Missing agents recorded with `found=False`, emitted as warnings, not errors
- `component-inventory.md` frontmatter includes `source_command`, `agent_count`, `has_command`
- `to_flat_inventory()` produces backward-compatible `ComponentInventory`
- `to_manifest_markdown()` produces readable Markdown (for `--save-manifest`)
- Standalone command (no skill) produces ComponentTree with skill=None, agents=[], refs/rules/templates/scripts=[]

**Sub-decomposition**:

- **FR-PORTIFY-WORKFLOW.2a: Agent Extraction (Step R3)** — Parse SKILL.md using 6 regex patterns (`AGENT_PATTERNS`). For each extracted name: resolve to `agents_dir/<name>.md`, record found/missing status, deduplicate by name.
- **FR-PORTIFY-WORKFLOW.2b: Manual Agent Injection** — `--include-agent` CLI option injects agents resolved by name or path. Empty strings silently ignored. Deduplication rule: manual overrides auto-discovered (sets `referenced_in="cli-override"`).
- **FR-PORTIFY-WORKFLOW.2c: Tier 2 Inventory (Step R4)** — Scan skill directory subdirectories: `refs/` (`.md` files), `rules/` (all files), `templates/` (all files), `scripts/` (all files). Identical to existing `discover_components.py` scan.
- **FR-PORTIFY-WORKFLOW.2d: ComponentTree Assembly (Step R5)** — Assemble all components into `ComponentTree`. New `Path`-based dataclasses for type safety. `to_flat_inventory()` converts `Path` → `str` at boundary for backward compat.
- **FR-PORTIFY-WORKFLOW.2e: Data Model Additions** — Add `AgentEntry`, `CommandEntry`, `SkillEntry`, `ComponentTree` dataclasses to `models.py`. Extend `PortifyConfig` with 10 new fields. Preserve existing `ComponentEntry.path: str` convention.
- **FR-PORTIFY-WORKFLOW.2f: Enriched Artifact Output** — `component-inventory.md` enriched with `## Command`, `## Agents`, `## Cross-Tier Data Flow`, `## Resolution Log` sections. New frontmatter fields: `source_command`, `source_skill`, `agent_count`, `has_command`, `has_skill`.
- **FR-PORTIFY-WORKFLOW.2g: Manifest Save** — When `--save-manifest` specified, serialize `ComponentTree` via `to_manifest_markdown()` after Step 2 completes. Write-only; no load flag in v2.24.1.
- **FR-PORTIFY-WORKFLOW.2h: Discovery Refactoring** — New `run_discover_component_tree()` entry point. Existing `run_discover_components()` becomes thin wrapper calling new function + `to_flat_inventory()`.
- **FR-PORTIFY-WORKFLOW.2i: derive_cli_name() Enhancement** — Prefer command name when available (`command_path.stem`). Fall back to existing skill directory name derivation logic.

**Dependencies**: FR-PORTIFY-WORKFLOW.1

---

### FR-PORTIFY-WORKFLOW.3: Extended Subprocess Scoping

**Description**: Extend `PortifyProcess` to pass all discovered component directories via `--add-dir`, enabling Claude subprocesses to read command files, agent definitions, and cross-skill references.

**Acceptance Criteria**:
- `PortifyProcess` accepts `additional_dirs` parameter
- `_build_add_dir_args()` includes all dirs from `ComponentTree.all_source_dirs`
- Duplicate directories are deduplicated
- \>10 directories triggers consolidation warning
- `additional_dirs=None` preserves existing v2.24 behavior

**Sub-decomposition**:

- **FR-PORTIFY-WORKFLOW.3a: PortifyProcess Extension** — Add `additional_dirs: list[Path] | None = None` parameter to `__init__`. Resolve all paths via `.resolve()`.
- **FR-PORTIFY-WORKFLOW.3b: Deduplication in _build_add_dir_args()** — Use `set[Path]` to deduplicate work_dir, workflow_path, and all additional_dirs.
- **FR-PORTIFY-WORKFLOW.3c: Directory Cap and Consolidation** — If >10 dirs: emit warning, group by nearest common parent (2-level depth), replace with parent if parent has ≤3x file count, fall back to top-10 by component count. Record consolidation decisions in `resolution_log`.

**Dependencies**: FR-PORTIFY-WORKFLOW.2

---

## Non-Functional Requirements

### NFR-WORKFLOW.1: Target Resolution Performance
- **Requirement**: All 6 input forms resolve in <1 second
- **Measurement**: `time.monotonic()` instrumentation in `resolve_target()`
- **Rationale**: Pure Python filesystem operations only; no subprocess budget consumed

### NFR-WORKFLOW.2: Zero Base-Module Modifications
- **Requirement**: Zero changes to `pipeline/` or `sprint/` base modules
- **Measurement**: `git diff --name-only` verification
- **Rationale**: Resolution runs within existing Step 1 (validate-config); no step renumbering or resume logic changes

### NFR-WORKFLOW.3: Synchronous-Only Execution
- **Requirement**: No `async def` or `await` in new code
- **Measurement**: `grep -r "async def\|await"` on new/modified files
- **Rationale**: Keeps resolution deterministic and simple; no event loop dependencies

### NFR-WORKFLOW.4: Backward Compatibility
- **Requirement**: All existing skill-directory inputs produce identical behavior
- **Measurement**: Existing test suite passes unchanged
- **Rationale**: `resolve_workflow_path()` preserved unchanged; `TARGET` is a superset of `WORKFLOW_PATH`

### NFR-WORKFLOW.5: Subprocess Directory Cap
- **Requirement**: Warning emitted when >10 `--add-dir` entries; consolidation applied
- **Measurement**: Consolidation logic in `_build_add_dir_args()`
- **Rationale**: Prevents `--add-dir` argument explosion while limiting over-scoping

---

## Complexity Assessment

**Score**: 0.65 / 1.0
**Class**: MEDIUM

**Scoring Rationale**:
| Factor | Score | Justification |
|--------|-------|---------------|
| New module count | Low (0.2) | 1 new file (`resolution.py`), all others are extensions |
| Integration surface | Medium (0.6) | 6 files modified, touches CLI, config, validation, discovery, and subprocess layers |
| Algorithm complexity | Medium (0.5) | 6-step resolution algorithm with 6 regex patterns, but all deterministic pure-Python |
| Backward compatibility burden | High (0.8) | Must preserve 4 existing API surfaces identically while extending them |
| Edge case density | Medium (0.6) | 7 explicit edge cases (standalone command/skill, multi-skill, circular refs, broken links, root detection failure, etc.) |
| Test scope | Medium (0.7) | ~37 new tests across 5 test files plus fixture creation |
| Data model changes | Medium (0.5) | 4 new dataclasses + 10 new fields on existing config, but no migration |

The spec's self-assessed complexity of 0.65 (moderate) is well-calibrated. The work is a bounded extension of an existing pipeline with no new infrastructure, no async, and no base-module changes. The primary challenge is maintaining backward compatibility across 6 input forms while enriching the discovery model.

---

## Architectural Constraints

1. **Pure Python, synchronous only** — No `async def`, `await`, or subprocess calls in resolution logic. All filesystem operations are synchronous `Path` operations.
2. **No base-module modifications** — `pipeline/` and `sprint/` modules must remain untouched. Resolution integrates into existing Step 1 (validate-config).
3. **No step renumbering** — Pipeline step numbering is unchanged. Resolution runs within Step 1, not as a new Step 0.
4. **Type convention: Path vs str** — New dataclasses use `Path` objects; existing `ComponentEntry.path` stays `str`. Boundary conversion via `str()` in `to_flat_inventory()`.
5. **Command-first resolution policy** — Bare names always resolve as commands first. Skill matching only attempted if no command match found.
6. **O(1)-depth agent discovery** — Only SKILL.md is scanned for agent references. No recursive agent-to-agent resolution in v2.24.1.
7. **UV-only Python execution** — All Python operations use UV toolchain per project rules.
8. **Module dependency direction** — `resolution.py` → `models.py`; `cli.py` → `resolution.py`; `discover_components.py` → `resolution.py`; `process.py` → `models.py`. No circular dependencies.
9. **Click CLI framework** — CLI changes use Click decorators (`@click.argument`, `@click.option`). `TARGET` argument removes `exists=True` constraint (resolution handles validation).
10. **Artifact enrichment only** — `component-inventory.md` gets new sections but gate evaluation logic is unchanged. Phase contracts and `PortifyContract` schema are unchanged.

---

## Risk Inventory

1. **RISK-1: Agent extraction regex misses references** — Severity: **medium**. The 6 regex patterns cover known formats but may miss novel reference styles. Mitigation: `--include-agent` escape hatch for manual injection; patterns iterable via real-world testing.

2. **RISK-2: Backward-compatible resolution breaks existing workflows** — Severity: **high**. Changing the CLI argument from `WORKFLOW_PATH` to `TARGET` could break existing invocations. Mitigation: Extensive test coverage with existing fixtures; `resolve_workflow_path()` preserved unchanged; `TARGET` is a superset of `WORKFLOW_PATH`.

3. **RISK-3: `--add-dir` with many directories causes subprocess issues** — Severity: **medium**. Large component trees could produce excessive `--add-dir` arguments. Mitigation: Cap at 10 directories with consolidation algorithm using `os.path.commonpath()`.

4. **RISK-4: YAML frontmatter parsing failures** — Severity: **low**. Malformed frontmatter in command or SKILL.md files. Mitigation: Graceful degradation — if frontmatter fails, still discover by convention.

5. **RISK-5: Project root detection fails in non-standard layouts** — Severity: **low**. Auto-detection relies on finding `src/superclaude/` or `pyproject.toml`. Mitigation: Explicit `--commands-dir`, `--skills-dir`, `--agents-dir` overrides with error messages suggesting these flags.

6. **RISK-6: Reverse-resolution (skill → command) fragile with non-standard naming** — Severity: **low**. Stripping `sc-` prefix and `-protocol` suffix assumes naming convention. Mitigation: Best-effort; missing command is a warning, not error. Standalone skills are a valid edge case.

---

## Dependency Inventory

1. **Click** (>=8.0.0) — CLI framework for argument/option parsing. New `@click.argument("target")`, `@click.option("--commands-dir")`, etc.
2. **Python pathlib.Path** — Core filesystem resolution. Used for all new dataclass path fields and resolution algorithm.
3. **Python re (regex)** — Agent extraction via 6 `AGENT_PATTERNS` regex patterns.
4. **Python os.path.commonpath** — Directory consolidation when >10 dirs detected.
5. **Existing `models.py` / `ComponentEntry` / `ComponentInventory`** — Backward-compatible data model that `ComponentTree.to_flat_inventory()` must produce.
6. **Existing `PortifyProcess` / `ClaudeProcess`** — Subprocess execution class extended with `additional_dirs` parameter.
7. **Downstream consumers: `contract.py`, `resume.py`** — Consume `ValidateConfigResult` fields. New fields must be included in `to_dict()` to avoid silent data loss in pipeline telemetry.

---

## Success Criteria

1. **SC-1**: `superclaude cli-portify run roadmap --dry-run` resolves command + skill + agents and produces enriched `component-inventory.md` with all tiers.
2. **SC-2**: `superclaude cli-portify run src/.../sc-roadmap-protocol/` (existing skill-dir input) produces identical pipeline behavior to v2.24 plus additional command/agent discovery.
3. **SC-3**: All 6 input forms (bare name, prefixed name, command path, skill dir, skill name, SKILL.md path) resolve correctly in <1 second.
4. **SC-4**: Missing agent references produce warnings (not errors) and pipeline continues with `found=False`.
5. **SC-5**: `--include-agent` successfully injects manually specified agents into the `ComponentTree`.
6. **SC-6**: `--save-manifest` writes a valid Markdown manifest file with full tree serialization.
7. **SC-7**: Existing test suite passes unchanged (backward compatibility).
8. **SC-8**: ~37 new tests pass covering resolution, models, validation, process, and discovery.
9. **SC-9**: Zero changes to `pipeline/` or `sprint/` base modules (`git diff --name-only` verification).
10. **SC-10**: No `async def` or `await` in any new or modified code.
11. **SC-11**: `ValidateConfigResult.to_dict()` includes all new fields (`warnings`, `command_path`, `skill_dir`, `target_type`, `agent_count`).
12. **SC-12**: Directory consolidation triggers at >10 dirs with warning message and resolution_log entries.

---

## Open Questions

1. **OQ-1 (OI-1): Recursive agent-to-agent resolution** — Should agents that delegate to sub-agents have their references recursively resolved? Impact: Medium (some agents delegate). Currently deferred to v2.25 with O(1)-depth in v2.24.1. *Stakeholder decision needed if use cases emerge before v2.25.*

2. **OQ-2 (OI-2): Manifest loading as input** — Should `--manifest` (load) be supported alongside `--save-manifest` (write)? Currently write-only in v2.24.1. Deferred to v2.25 pending user demand. *Need signal on whether debugging workflows would benefit from re-loading manifests.*

3. **OQ-3 (OI-3): `--exclude-component` support** — Should users be able to exclude auto-discovered components? Not needed if discovery is accurate. Deferred to v2.25. *Monitor for false-positive discovery issues post-launch.*

4. **OQ-4: Multi-skill command handling** — Commands referencing multiple skills extract only the primary from `## Activation`. Secondary references are logged as warnings. *Is there a known command that requires multi-skill resolution? If so, v2.24.1 may under-serve it.*

5. **OQ-5: Agent regex pattern completeness** — The 6 patterns cover known formats but are heuristic. *Are there additional agent reference patterns in the codebase not covered by the 6 regexes? An audit of all SKILL.md files would confirm coverage.*

6. **OQ-6: Naming convention fragility** — Reverse-resolution assumes `sc-<name>-protocol` naming convention for skills and `<name>.md` for commands. *Are there existing skills or commands that deviate from this convention? Non-standard names would silently fail backward-resolution.*

7. **OQ-7: `to_dict()` downstream consumers** — The spec states `contract.py` and `resume.py` consume `ValidateConfigResult` fields. *Are there other downstream consumers that read the validation dict? Omitted fields would cause silent data loss.*
