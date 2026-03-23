---
spec_source: "portify-release-spec.md"
complexity_score: 0.65
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a bounded, backward-compatible extension to the CLI portify workflow so it can resolve multiple target forms, discover the full workflow component tree, and scope subprocesses with richer source context.

From an architecture perspective, the release is favorable because it:
- Extends existing workflow boundaries without modifying `pipeline/` or `sprint/` base modules, satisfying **NFR-WORKFLOW.2**.
- Keeps all new logic synchronous and deterministic, satisfying **NFR-WORKFLOW.3**.
- Preserves current behavior for existing skill-directory inputs while broadening supported target types, satisfying **NFR-WORKFLOW.4**.
- Adds visibility and traceability through enriched inventory artifacts and resolution logs.

The primary architectural challenge is not algorithmic complexity; it is compatibility control across multiple entry points and downstream consumers. The roadmap therefore prioritizes:
1. Resolution correctness first.
2. Data model and discovery integrity second.
3. Subprocess scoping and operational hardening third.
4. Validation and regression protection throughout.

## Key architectural outcomes

1. Implement **FR-PORTIFY-WORKFLOW.1** as a deterministic target resolution layer:
   - Accept six target forms.
   - Normalize them into a single `ResolvedTarget`.
   - Preserve command-first semantics and explicit override paths.

2. Implement **FR-PORTIFY-WORKFLOW.2** as a structured discovery layer:
   - Build `ComponentTree` with command, skill, agents, and tiered subcomponents.
   - Enrich `component-inventory.md` without changing gate evaluation contracts.

3. Implement **FR-PORTIFY-WORKFLOW.3** as a controlled execution-context layer:
   - Pass expanded source directories into subprocesses.
   - Deduplicate and consolidate when directory counts grow.

## Delivery posture

- **Complexity class**: MEDIUM
- **Primary domains**: backend, cli, tooling, developer-experience
- **Risk count to actively mitigate**: 6
- **Dependencies to coordinate**: 7
- **Validation target**: 12 success criteria

# 2. Phased implementation plan with milestones

## Phase 0 — Architecture confirmation and change envelope

### Objectives
- Lock architectural boundaries before code changes.
- Prevent scope creep and accidental base-module modification.

### Scope
- Confirm implementation boundaries for:
  - **FR-PORTIFY-WORKFLOW.1**
  - **FR-PORTIFY-WORKFLOW.2**
  - **FR-PORTIFY-WORKFLOW.3**
  - **NFR-WORKFLOW.2**
  - **NFR-WORKFLOW.3**
  - **NFR-WORKFLOW.4**
  - **NFR-WORKFLOW.5**

### Action items
1. Confirm target files and dependency direction:
   - `resolution.py` → `models.py`
   - `cli.py` → `resolution.py`
   - `discover_components.py` → `resolution.py`
   - `process.py` → `models.py`
2. Freeze architectural rules:
   - No edits to `pipeline/` or `sprint/`
   - No `async def` or `await`
   - No step renumbering
   - `Path` internally, `str` at backward-compat boundaries
3. Define acceptance gates for every functional requirement family before implementation starts.
4. Identify downstream validation points for `ValidateConfigResult.to_dict()` to protect **SC-11**.

### Milestone
- Approved implementation map covering modified files, new dataclasses, CLI changes, and artifact updates.

### Exit criteria
- Architectural constraints documented and accepted.
- No unresolved ambiguity about where each requirement lands.

### Timeline estimate
- **0.5 day**

---

## Phase 1 — Target resolution foundation

### Objectives
Implement the normalized target resolution system required by **FR-PORTIFY-WORKFLOW.1**.

### Scope
- **FR-PORTIFY-WORKFLOW.1**
- **FR-PORTIFY-WORKFLOW.1a**
- **FR-PORTIFY-WORKFLOW.1b**
- **FR-PORTIFY-WORKFLOW.1c**
- **FR-PORTIFY-WORKFLOW.1d**
- **FR-PORTIFY-WORKFLOW.1e**
- **FR-PORTIFY-WORKFLOW.1f**
- **FR-PORTIFY-WORKFLOW.1g**
- **NFR-WORKFLOW.1**
- **NFR-WORKFLOW.4**

### Action items
1. Build target normalization and validation flow:
   - Reject `None`, empty, whitespace-only, and `"sc:"` inputs per **FR-PORTIFY-WORKFLOW.1a**.
2. Implement classification into:
   - `COMMAND_NAME`
   - `COMMAND_PATH`
   - `SKILL_DIR`
   - `SKILL_NAME`
   - `SKILL_FILE`
3. Implement command resolution rules per **FR-PORTIFY-WORKFLOW.1c**:
   - Resolve command files in `commands_dir`
   - Parse YAML frontmatter
   - Parse `## Activation` skill references
4. Implement skill resolution rules per **FR-PORTIFY-WORKFLOW.1d**:
   - Derive `sc-<name>-protocol`
   - Validate `SKILL.md`
5. Implement ambiguity policy per **FR-PORTIFY-WORKFLOW.1e**:
   - Emit `ERR_AMBIGUOUS_TARGET` only for same-class collisions
   - Preserve command-first behavior
6. Implement standalone-command path per **FR-PORTIFY-WORKFLOW.1f**:
   - Allow `skill_dir=None`
   - Emit `"Standalone command"` in `resolution_log`
7. Implement root detection and override fallback per **FR-PORTIFY-WORKFLOW.1g**:
   - Walk upward for `src/superclaude/` or `pyproject.toml`
   - Support `--commands-dir`, `--skills-dir`, `--agents-dir`
8. Add instrumentation for sub-second performance verification to satisfy **NFR-WORKFLOW.1**.

### Milestone
- All six input forms resolve to `ResolvedTarget`.
- Existing workflow-path behavior remains intact.

### Exit criteria
- Acceptance criteria for **FR-PORTIFY-WORKFLOW.1** pass.
- Performance evidence confirms **NFR-WORKFLOW.1**.
- Regression tests confirm **NFR-WORKFLOW.4**.

### Timeline estimate
- **1.5 days**

---

## Phase 2 — Data model and component tree architecture

### Objectives
Create the new structured model layer that supports richer discovery without breaking existing consumers.

### Scope
- **FR-PORTIFY-WORKFLOW.2d**
- **FR-PORTIFY-WORKFLOW.2e**
- **FR-PORTIFY-WORKFLOW.2h**
- **FR-PORTIFY-WORKFLOW.2i**
- **SC-11**

### Action items
1. Add dataclasses required by **FR-PORTIFY-WORKFLOW.2e**:
   - `AgentEntry`
   - `CommandEntry`
   - `SkillEntry`
   - `ComponentTree`
2. Extend `PortifyConfig` with the required new fields.
3. Implement `ComponentTree.to_flat_inventory()` boundary conversion:
   - Preserve `ComponentEntry.path: str`
   - Convert internal `Path` objects to `str`
4. Implement `run_discover_component_tree()` per **FR-PORTIFY-WORKFLOW.2h**.
5. Refactor existing `run_discover_components()` to become a thin wrapper.
6. Enhance CLI name derivation per **FR-PORTIFY-WORKFLOW.2i**:
   - Prefer `command_path.stem`
   - Fall back to existing skill-name derivation
7. Update `ValidateConfigResult.to_dict()` to include:
   - `warnings`
   - `command_path`
   - `skill_dir`
   - `target_type`
   - `agent_count`

### Milestone
- Backward-compatible model layer supports full-tree discovery.

### Exit criteria
- No downstream serialization gaps.
- Wrapper behavior preserves legacy API expectations.

### Timeline estimate
- **1.0 day**

---

## Phase 3 — Full component tree discovery and artifact enrichment

### Objectives
Deliver discovery completeness and improved observability for the workflow inventory.

### Scope
- **FR-PORTIFY-WORKFLOW.2**
- **FR-PORTIFY-WORKFLOW.2a**
- **FR-PORTIFY-WORKFLOW.2b**
- **FR-PORTIFY-WORKFLOW.2c**
- **FR-PORTIFY-WORKFLOW.2f**
- **FR-PORTIFY-WORKFLOW.2g**

### Action items
1. Implement agent extraction from `SKILL.md` per **FR-PORTIFY-WORKFLOW.2a**:
   - Support all 6 `AGENT_PATTERNS`
   - Deduplicate by name
   - Mark missing agents with `found=False`
2. Implement manual agent injection per **FR-PORTIFY-WORKFLOW.2b**:
   - Support name or path
   - Ignore empty values
   - Ensure CLI override precedence via `referenced_in="cli-override"`
3. Implement tier scanning per **FR-PORTIFY-WORKFLOW.2c**:
   - `refs/` → `.md`
   - `rules/` → all files
   - `templates/` → all files
   - `scripts/` → all files
4. Assemble complete `ComponentTree` per **FR-PORTIFY-WORKFLOW.2d**.
5. Enrich `component-inventory.md` per **FR-PORTIFY-WORKFLOW.2f** with:
   - `## Command`
   - `## Agents`
   - `## Cross-Tier Data Flow`
   - `## Resolution Log`
   - frontmatter fields: `source_command`, `source_skill`, `agent_count`, `has_command`, `has_skill`
6. Implement manifest output per **FR-PORTIFY-WORKFLOW.2g** using `to_manifest_markdown()`.

### Milestone
- Rich component discovery works for standard and standalone workflows.
- Inventory artifacts become operator-useful, not just machine-adjacent.

### Exit criteria
- Discovery produces complete trees for normal cases.
- Missing agents degrade gracefully.
- Manifest save path works end-to-end.

### Timeline estimate
- **1.5 days**

---

## Phase 4 — Subprocess scoping and execution-context hardening

### Objectives
Ensure Claude subprocesses receive sufficient but controlled directory scope.

### Scope
- **FR-PORTIFY-WORKFLOW.3**
- **FR-PORTIFY-WORKFLOW.3a**
- **FR-PORTIFY-WORKFLOW.3b**
- **FR-PORTIFY-WORKFLOW.3c**
- **NFR-WORKFLOW.5**

### Action items
1. Extend `PortifyProcess` per **FR-PORTIFY-WORKFLOW.3a**:
   - Add `additional_dirs: list[Path] | None = None`
   - Normalize with `.resolve()`
2. Implement deduplicated add-dir argument generation per **FR-PORTIFY-WORKFLOW.3b**:
   - Include work dir, workflow path, and additional dirs
   - Deduplicate with `set[Path]`
3. Implement directory-cap control per **FR-PORTIFY-WORKFLOW.3c**:
   - Warn when count exceeds 10
   - Consolidate by common parent where file-count threshold is acceptable
   - Fall back to top-10 by component count if needed
4. Ensure consolidation decisions are recorded in `resolution_log`.
5. Verify `additional_dirs=None` preserves existing v2.24 behavior.

### Milestone
- Subprocess scoping becomes broader, safer, and operationally bounded.

### Exit criteria
- Add-dir generation is deterministic.
- Over-scoping is controlled.
- Existing v2.24 behavior remains unchanged when new feature is unused.

### Timeline estimate
- **1.0 day**

---

## Phase 5 — Validation, regression protection, and release readiness

### Objectives
Prove the release meets compatibility, performance, and quality requirements.

### Scope
- **SC-1** through **SC-12**
- **NFR-WORKFLOW.1**
- **NFR-WORKFLOW.2**
- **NFR-WORKFLOW.3**
- **NFR-WORKFLOW.4**
- **NFR-WORKFLOW.5**

### Action items
1. Implement and run the targeted new test suite:
   - Resolution
   - Models
   - Validation
   - Process
   - Discovery
2. Verify all six input forms against **SC-3**.
3. Verify standard command flow against **SC-1**.
4. Verify legacy skill-dir path behavior against **SC-2**.
5. Verify missing-agent warning behavior against **SC-4**.
6. Verify `--include-agent` against **SC-5**.
7. Verify `--save-manifest` against **SC-6**.
8. Verify unchanged legacy suite for **SC-7**.
9. Verify approximate new suite breadth for **SC-8**.
10. Verify no base-module modifications for **SC-9** / **NFR-WORKFLOW.2**.
11. Verify no async usage for **SC-10** / **NFR-WORKFLOW.3**.
12. Verify serialization completeness for **SC-11**.
13. Verify directory-cap warning and consolidation behavior for **SC-12** / **NFR-WORKFLOW.5**.

### Milestone
- Release candidate is architecturally safe, regression-tested, and acceptance-complete.

### Exit criteria
- All success criteria met or explicitly waived.
- No unresolved high-severity compatibility risk remains.

### Timeline estimate
- **1.0 day**

---

## Phase 6 — Post-release observation and deferred design decisions

### Objectives
Stabilize release behavior and gather evidence for deferred v2.25 decisions.

### Scope
- **OQ-1**
- **OQ-2**
- **OQ-3**
- **OQ-4**
- **OQ-5**
- **OQ-6**
- **OQ-7**

### Action items
1. Observe real-world agent extraction misses to inform **OQ-5**.
2. Track requests for recursive agent resolution for **OQ-1**.
3. Track demand for manifest re-load support for **OQ-2**.
4. Track false-positive discovery concerns for **OQ-3**.
5. Audit multi-skill command cases for **OQ-4**.
6. Audit naming convention deviations for **OQ-6**.
7. Audit additional consumers of validation dicts for **OQ-7**.

### Milestone
- Evidence backlog prepared for v2.25 planning.

### Exit criteria
- Deferred work is prioritized using real operational data, not speculation.

### Timeline estimate
- **0.5 day active observation setup**, then ongoing passive monitoring

# 3. Risk assessment and mitigation strategies

## Risk-prioritized view

### 1. RISK-2: Backward-compatible resolution breaks existing workflows
- **Severity**: High
- **Architectural concern**: This is the release’s primary failure mode because it affects entry semantics and user expectations.
- **Mitigation**:
  1. Preserve existing `resolve_workflow_path()` unchanged.
  2. Treat `TARGET` as a superset, not a replacement in behavior.
  3. Add regression fixtures covering current skill-directory flows.
  4. Gate release on **SC-2**, **SC-7**, and **SC-9**.
- **Contingency**:
  - If regressions appear, narrow new resolution logic to explicit new input forms only and preserve legacy path-first routing for old forms.

### 2. RISK-1: Agent extraction regex misses references
- **Severity**: Medium
- **Architectural concern**: Discovery incompleteness degrades artifact quality and subprocess scoping.
- **Mitigation**:
  1. Implement all 6 known regex patterns exactly.
  2. Support `--include-agent` as an explicit override.
  3. Mark missing agents as warnings, not hard failures.
  4. Log extraction gaps in `resolution_log`.
- **Contingency**:
  - Maintain a pattern audit list for v2.25 updates based on observed misses.

### 3. RISK-3: `--add-dir` with many directories causes subprocess issues
- **Severity**: Medium
- **Architectural concern**: Operational overload and context overscoping.
- **Mitigation**:
  1. Deduplicate directories by resolved path.
  2. Cap at >10 with warning.
  3. Consolidate by nearest common parent when efficient.
  4. Fall back to top-10 by component count.
- **Contingency**:
  - Add diagnostic output to clarify which directories were retained or collapsed.

### 4. RISK-4: YAML frontmatter parsing failures
- **Severity**: Low
- **Architectural concern**: Convention-based fallback must keep discovery resilient.
- **Mitigation**:
  1. Treat frontmatter parsing as additive metadata, not a hard dependency.
  2. Fall back to naming conventions where possible.
  3. Emit warnings instead of aborting discovery.
- **Contingency**:
  - Add malformed fixture tests to prevent crash regressions.

### 5. RISK-5: Project root detection fails in non-standard layouts
- **Severity**: Low
- **Architectural concern**: Environmental brittleness in developer tooling.
- **Mitigation**:
  1. Support `--commands-dir`, `--skills-dir`, `--agents-dir`.
  2. Emit actionable error messages suggesting override flags.
  3. Test fallback from bare names and path-based targets.
- **Contingency**:
  - Promote override flags in operator docs or CLI help.

### 6. RISK-6: Reverse-resolution fragile with non-standard naming
- **Severity**: Low
- **Architectural concern**: Convention dependence for skill-to-command mapping.
- **Mitigation**:
  1. Treat missing reverse match as warning, not failure.
  2. Preserve standalone-skill validity.
  3. Audit real naming variants after release.
- **Contingency**:
  - Add explicit metadata linkage in a future release if naming drift appears.

## Risk governance recommendations

1. Treat **RISK-2** as release-blocking.
2. Treat **RISK-1** and **RISK-3** as release-gating but not necessarily blocking if degradations remain warning-only.
3. Treat **RISK-4**, **RISK-5**, and **RISK-6** as managed resilience risks with explicit observability.

# 4. Resource requirements and dependencies

## Engineering resources

1. **Primary backend/CLI engineer**
   - Implements resolution, discovery, models, and process changes.
2. **QA-focused engineer or reviewer**
   - Builds regression fixtures and validates all success criteria.
3. **Architect/reviewer**
   - Verifies boundary discipline, compatibility posture, and downstream contract safety.

## Technical dependencies to plan around

1. **Click**
   - Needed for new `TARGET` argument behavior and override options.
   - Dependency impact: CLI surface and parsing semantics.
2. **Python pathlib.Path**
   - Core to all internal path normalization and type-safe dataclasses.
3. **Python re**
   - Required for the 6 `AGENT_PATTERNS`.
4. **Python os.path.commonpath**
   - Required for directory consolidation strategy.
5. **Existing `models.py` / `ComponentEntry` / `ComponentInventory`**
   - Backward-compat boundary that constrains model changes.
6. **Existing `PortifyProcess` / `ClaudeProcess`**
   - Execution layer that must accept richer source scoping.
7. **Downstream consumers: `contract.py`, `resume.py`**
   - Must continue receiving complete validation data without silent omissions.

## Artifact and validation resources

1. Test fixtures for:
   - All six input forms
   - Missing agents
   - Standalone commands
   - Non-standard path roots
   - Over-10 directory scenarios
2. Performance instrumentation for **NFR-WORKFLOW.1**
3. Diff verification for **NFR-WORKFLOW.2**
4. Static async scan for **NFR-WORKFLOW.3**

## Architectural dependency sequencing

1. `models.py` changes must land before full discovery assembly.
2. Resolution logic must land before discovery wrapper refactor.
3. Discovery must land before subprocess additional-dir wiring.
4. Validation must cover each stage before release candidate declaration.

# 5. Success criteria and validation approach

## Validation strategy

The validation approach should be phase-aligned and evidence-based. Each success criterion maps to a concrete validation activity.

### Functional validation

1. **SC-1**
   - Run `superclaude cli-portify run roadmap --dry-run`
   - Validate command + skill + agents in enriched `component-inventory.md`
2. **SC-2**
   - Run legacy skill-directory input
   - Compare behavior to v2.24 baseline
3. **SC-3**
   - Execute all six input forms
   - Capture timing and normalized output
4. **SC-4**
   - Use fixture with intentionally missing agent references
   - Confirm warnings and continued execution
5. **SC-5**
   - Inject manual agents via `--include-agent`
   - Confirm dedupe and override behavior
6. **SC-6**
   - Run with `--save-manifest`
   - Validate manifest file structure and readability

### Regression and compatibility validation

7. **SC-7**
   - Run existing test suite unchanged
8. **SC-8**
   - Run new targeted tests across 5 files / expected coverage surface
9. **SC-9**
   - Verify `git diff --name-only` excludes `pipeline/` and `sprint/`
10. **SC-10**
   - Verify no `async def` or `await` in new/modified code
11. **SC-11**
   - Validate `ValidateConfigResult.to_dict()` field completeness
12. **SC-12**
   - Create >10-dir scenario and confirm warning + consolidation log

## Requirement traceability emphasis

### FR traceability
- **FR-PORTIFY-WORKFLOW.1** family validated by six-form resolution matrix and performance instrumentation.
- **FR-PORTIFY-WORKFLOW.2** family validated by tree assembly, artifact enrichment, agent handling, and manifest output.
- **FR-PORTIFY-WORKFLOW.3** family validated by subprocess argument generation and consolidation scenarios.

### NFR traceability
- **NFR-WORKFLOW.1**: timing instrumentation in `resolve_target()`
- **NFR-WORKFLOW.2**: file-diff boundary verification
- **NFR-WORKFLOW.3**: async scan
- **NFR-WORKFLOW.4**: unchanged legacy suite + input equivalence
- **NFR-WORKFLOW.5**: over-cap consolidation test

## Release readiness gate

The release should proceed only when:
1. All high-severity compatibility checks pass.
2. **SC-1** through **SC-12** are green.
3. No unresolved issue exists in the resolution path, tree assembly, or add-dir consolidation path.

# 6. Timeline estimates per phase

## Summary timeline

1. **Phase 0 — Architecture confirmation and change envelope**
   - Estimate: **0.5 day**

2. **Phase 1 — Target resolution foundation**
   - Estimate: **1.5 days**

3. **Phase 2 — Data model and component tree architecture**
   - Estimate: **1.0 day**

4. **Phase 3 — Full component tree discovery and artifact enrichment**
   - Estimate: **1.5 days**

5. **Phase 4 — Subprocess scoping and execution-context hardening**
   - Estimate: **1.0 day**

6. **Phase 5 — Validation, regression protection, and release readiness**
   - Estimate: **1.0 day**

7. **Phase 6 — Post-release observation and deferred design decisions**
   - Estimate: **0.5 day setup**, then ongoing monitoring

## Total implementation estimate

- **Core delivery**: **6.5 engineering days**
- **Including post-release observation setup**: **7.0 days**

## Timeline assumptions

1. Existing fixtures and current v2.24 behavior are available for comparison.
2. No hidden downstream consumer beyond those already identified blocks `to_dict()` changes.
3. No previously unknown naming convention deviations materially affect reverse-resolution.
4. Validation can run continuously during implementation rather than being deferred to the end.

## Recommended milestone schedule

1. **Milestone A**: Resolution complete
   - Covers **FR-PORTIFY-WORKFLOW.1**
2. **Milestone B**: Model and tree discovery complete
   - Covers **FR-PORTIFY-WORKFLOW.2**
3. **Milestone C**: Subprocess scoping complete
   - Covers **FR-PORTIFY-WORKFLOW.3**
4. **Milestone D**: All success criteria validated
   - Covers **SC-1** through **SC-12**

# Recommended architectural priorities

1. Prioritize **FR-PORTIFY-WORKFLOW.1** before all other work because every downstream behavior depends on correct target normalization.
2. Protect **NFR-WORKFLOW.2** and **NFR-WORKFLOW.4** as non-negotiable release constraints.
3. Treat artifact enrichment as valuable, but never at the expense of compatibility.
4. Use `resolution_log` as a first-class observability asset for debugging, operator trust, and future v2.25 design decisions.
5. Defer recursive discovery and manifest re-load features until operational evidence justifies them, consistent with the bounded scope implied by the 0.65 complexity score.
