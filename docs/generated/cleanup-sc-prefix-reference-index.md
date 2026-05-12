# sc: Prefix Reference Index
Generated: 2026-03-24

## Summary
- Total files with sc: framework references: ~1,350+ (deduplicated across search patterns)
- By type: DISPATCH: 12, CONFIG: 6, SKILL: 25 directories (12 src + 13 .claude), COMMAND: 83 files (41 .claude + 42 src), PATH: 138+, DOC: 88, TEST: 18, DEV/RELEASE: 1,228

## CRITICAL: Dispatch & Config Files (code that routes commands)

### Python CLI Dispatch Files

| File | Lines | Context | Type |
|------|-------|---------|------|
| `src/superclaude/cli/main.py` | 32, 33, 217, 218 | `default="~/.claude/commands/sc"` and help text for install target dir | DISPATCH |
| `src/superclaude/cli/install_commands.py` | 4, 17, 23, 147 | Installs commands to `~/.claude/commands/sc/`, default path, list commands | DISPATCH |
| `src/superclaude/cli/install_skills.py` | 9, 59, 96, 100 | Skips `sc-*` skills with `/sc:` commands; maps `name -> /sc:{cmd_name}` | DISPATCH |
| `src/superclaude/cli/sprint/process.py` | 124, 170 | Builds `/sc:task-unified` prompt for phase execution | DISPATCH |
| `src/superclaude/cli/cleanup_audit/prompts.py` | 26, 47, 69, 92, 116 | Five prompt templates all invoking `/sc:task-unified` | DISPATCH |
| `src/superclaude/cli/roadmap/validate_prompts.py` | 49, 57 | References to `sc:tasklist`'s splitter in prompt text | DISPATCH |
| `src/superclaude/cli/cli_portify/resolution.py` | 4, 12, 75, 76, 79, 184, 201, 202 | Resolves `sc:` prefix targets; regex matches `> Skill sc:<name>` | DISPATCH |
| `src/superclaude/cli/cli_portify/commands.py` | 22-25, 128 | CLI examples `superclaude cli-portify run sc:roadmap`; docstring refs | DISPATCH |
| `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py` | 7, 55 | Checks if `sc:brainstorm` skill is installed | DISPATCH |
| `scripts/sync_from_framework.py` | 82-84, 96, 99, 102, 444 | Content transformer: rewrites `/analyze` to `/sc:analyze`; maps `commands` dir | DISPATCH |

### Config/Build Files

| File | Lines | Context | Type |
|------|-------|---------|------|
| `Makefile` | 130, 134, 139, 203-207, 215, 253, 282, 298, 310 | `mkdir -p .claude/commands/sc`, copy commands, verify-sync, skill glob `sc-*-protocol` | CONFIG |
| `.claude/skills/sc-validate-tests-protocol/classification-algorithm.yaml` | -- | Skill config YAML with sc: references | CONFIG |
| `.claude/skills/sc-cli-portify-protocol/decisions.yaml` | -- | Skill config YAML with sc: references | CONFIG |
| `src/superclaude/skills/sc-cli-portify-protocol/decisions.yaml` | -- | Source copy of decisions.yaml | CONFIG |
| `src/superclaude/skills/sc-validate-tests-protocol/classification-algorithm.yaml` | -- | Source copy of classification-algorithm.yaml | CONFIG |
| `PROJECT_INDEX.md` | 84 | `commands/sc/` path reference in project structure | CONFIG |

## HIGH: Skill Protocol Directories (directory/file renames needed)

### Source of Truth: `src/superclaude/skills/` (13 directories)

| Directory | Has SKILL.md |
|-----------|-------------|
| `src/superclaude/skills/sc-adversarial-protocol/` | Yes |
| `src/superclaude/skills/sc-cleanup-audit-protocol/` | Yes |
| `src/superclaude/skills/sc-cli-portify-protocol/` | Yes |
| `src/superclaude/skills/sc-forensic-qa-protocol/` | No SKILL.md found |
| `src/superclaude/skills/sc-pm-protocol/` | Yes |
| `src/superclaude/skills/sc-recommend-protocol/` | Yes |
| `src/superclaude/skills/sc-release-split-protocol/` | Yes |
| `src/superclaude/skills/sc-review-translation-protocol/` | Yes |
| `src/superclaude/skills/sc-roadmap-protocol/` | Yes |
| `src/superclaude/skills/sc-task-unified-protocol/` | Yes |
| `src/superclaude/skills/sc-tasklist-protocol/` | Yes |
| `src/superclaude/skills/sc-validate-roadmap-protocol/` | Yes |
| `src/superclaude/skills/sc-validate-tests-protocol/` | Yes |

### Dev Copies: `.claude/skills/` (13 directories)

| Directory | Has SKILL.md |
|-----------|-------------|
| `.claude/skills/sc-adversarial-protocol/` | Yes |
| `.claude/skills/sc-cleanup-audit-protocol/` | Yes |
| `.claude/skills/sc-cli-portify-protocol/` | Yes |
| `.claude/skills/sc-pm-protocol/` | Yes |
| `.claude/skills/sc-recommend-protocol/` | Yes |
| `.claude/skills/sc-release-split-protocol/` | Yes |
| `.claude/skills/sc-release-split-protocol-workspace/` | No (workspace/eval data, not a skill) |
| `.claude/skills/sc-review-translation-protocol/` | Yes |
| `.claude/skills/sc-roadmap-protocol/` | Yes |
| `.claude/skills/sc-task-unified-protocol/` | Yes |
| `.claude/skills/sc-tasklist-protocol/` | Yes |
| `.claude/skills/sc-validate-roadmap-protocol/` | Yes |
| `.claude/skills/sc-validate-tests-protocol/` | Yes |

## HIGH: Command Definition Files

### Dev Copies: `.claude/commands/sc/` (41 files)

| File |
|------|
| `.claude/commands/sc/adversarial.md` |
| `.claude/commands/sc/agent.md` |
| `.claude/commands/sc/analyze.md` |
| `.claude/commands/sc/brainstorm.md` |
| `.claude/commands/sc/build.md` |
| `.claude/commands/sc/business-panel.md` |
| `.claude/commands/sc/cleanup-audit.md` |
| `.claude/commands/sc/cleanup.md` |
| `.claude/commands/sc/cli-portify.md` |
| `.claude/commands/sc/design.md` |
| `.claude/commands/sc/document.md` |
| `.claude/commands/sc/estimate.md` |
| `.claude/commands/sc/explain.md` |
| `.claude/commands/sc/git.md` |
| `.claude/commands/sc/help.md` |
| `.claude/commands/sc/implement.md` |
| `.claude/commands/sc/improve.md` |
| `.claude/commands/sc/index-repo.md` |
| `.claude/commands/sc/index.md` |
| `.claude/commands/sc/load.md` |
| `.claude/commands/sc/pm.md` |
| `.claude/commands/sc/recommend.md` |
| `.claude/commands/sc/reflect.md` |
| `.claude/commands/sc/release-split.md` |
| `.claude/commands/sc/research.md` |
| `.claude/commands/sc/review-translation.md` |
| `.claude/commands/sc/roadmap.md` |
| `.claude/commands/sc/save.md` |
| `.claude/commands/sc/sc.md` |
| `.claude/commands/sc/select-tool.md` |
| `.claude/commands/sc/spawn.md` |
| `.claude/commands/sc/spec-panel.md` |
| `.claude/commands/sc/task-mcp.md` |
| `.claude/commands/sc/task-unified.md` |
| `.claude/commands/sc/task.md` |
| `.claude/commands/sc/tasklist.md` |
| `.claude/commands/sc/test.md` |
| `.claude/commands/sc/troubleshoot.md` |
| `.claude/commands/sc/validate-roadmap.md` |
| `.claude/commands/sc/validate-tests.md` |
| `.claude/commands/sc/workflow.md` |

### Source of Truth: `src/superclaude/commands/` (42 files)

| File |
|------|
| `src/superclaude/commands/adversarial.md` |
| `src/superclaude/commands/agent.md` |
| `src/superclaude/commands/analyze.md` |
| `src/superclaude/commands/brainstorm.md` |
| `src/superclaude/commands/build.md` |
| `src/superclaude/commands/business-panel.md` |
| `src/superclaude/commands/cleanup-audit.md` |
| `src/superclaude/commands/cleanup.md` |
| `src/superclaude/commands/cli-portify.md` |
| `src/superclaude/commands/design.md` |
| `src/superclaude/commands/document.md` |
| `src/superclaude/commands/estimate.md` |
| `src/superclaude/commands/explain.md` |
| `src/superclaude/commands/git.md` |
| `src/superclaude/commands/help.md` |
| `src/superclaude/commands/implement.md` |
| `src/superclaude/commands/improve.md` |
| `src/superclaude/commands/index-repo.md` |
| `src/superclaude/commands/index.md` |
| `src/superclaude/commands/load.md` |
| `src/superclaude/commands/pm.md` |
| `src/superclaude/commands/README.md` |
| `src/superclaude/commands/recommend.md` |
| `src/superclaude/commands/reflect.md` |
| `src/superclaude/commands/release-split.md` |
| `src/superclaude/commands/research.md` |
| `src/superclaude/commands/review-translation.md` |
| `src/superclaude/commands/roadmap.md` |
| `src/superclaude/commands/save.md` |
| `src/superclaude/commands/sc.md` |
| `src/superclaude/commands/select-tool.md` |
| `src/superclaude/commands/spawn.md` |
| `src/superclaude/commands/spec-panel.md` |
| `src/superclaude/commands/task-mcp.md` |
| `src/superclaude/commands/task-unified.md` |
| `src/superclaude/commands/task.md` |
| `src/superclaude/commands/tasklist.md` |
| `src/superclaude/commands/test.md` |
| `src/superclaude/commands/troubleshoot.md` |
| `src/superclaude/commands/validate-roadmap.md` |
| `src/superclaude/commands/validate-tests.md` |
| `src/superclaude/commands/workflow.md` |

**Note**: `src/superclaude/commands/` files do NOT have `sc/` subdirectory -- the `sc/` namespace is applied during install by `install_commands.py` copying into `~/.claude/commands/sc/`.

## MEDIUM: Agent Files referencing sc: commands

### `.claude/agents/` (4 files)

| File | Lines | sc: References |
|------|-------|----------------|
| `.claude/agents/pm-agent.md` | 15 | `/sc:pm` |
| `.claude/agents/deep-research-agent.md` | 10 | `/sc:research` |
| `.claude/agents/debate-orchestrator.md` | 3, 10 | `sc:adversarial`, `/sc:adversarial` |
| `.claude/agents/socratic-mentor.md` | 157, 277-279 | `/sc:socratic-clean-code`, `/sc:socratic-patterns`, `/sc:analyze`, `/sc:implement`, `/sc:document` |

### `src/superclaude/agents/` (4 files, identical content)

| File | Lines | sc: References |
|------|-------|----------------|
| `src/superclaude/agents/pm-agent.md` | 15 | `/sc:pm` |
| `src/superclaude/agents/deep-research-agent.md` | 10 | `/sc:research` |
| `src/superclaude/agents/debate-orchestrator.md` | 3, 10 | `sc:adversarial`, `/sc:adversarial` |
| `src/superclaude/agents/socratic-mentor.md` | 157, 277-279 | `/sc:socratic-clean-code`, `/sc:socratic-patterns`, `/sc:analyze`, `/sc:implement`, `/sc:document` |

## MEDIUM: Test Files (18 files)

| File | Type |
|------|------|
| `tests/cli_portify/test_resolution.py` | Tests `sc:` prefix resolution logic |
| `tests/cli_portify/test_discover_components.py` | Tests component discovery with sc- paths |
| `tests/cli_portify/test_brainstorm_gaps.py` | Tests sc:brainstorm skill detection |
| `tests/cli_portify/integration/test_orchestration.py` | Integration test with sc: references |
| `tests/unit/test_review_translation.py` | References sc: commands |
| `tests/sprint/test_process.py` | Tests `/sc:task-unified` prompt building |
| `tests/sc-roadmap/compliance/test_critical_corrections.py` | sc-roadmap compliance tests |
| `tests/sc-roadmap/compliance/test_path_conventions.py` | Path convention tests with sc- |
| `tests/sc-roadmap/integration/test_return_contract_routing.py` | Integration routing tests |
| `tests/pipeline/test_mutation_inventory.py` | Pipeline tests with sc: refs |
| `tests/pipeline/test_process.py` | Pipeline process tests |
| `tests/pipeline/test_state_detector.py` | State detector tests |
| `tests/pipeline/test_fmea_domains.py` | FMEA domain tests |
| `tests/pipeline/test_guard_analyzer.py` | Guard analyzer tests |
| `tests/pipeline/test_guard_pass.py` | Guard pass tests |
| `tests/pipeline/test_guard_resolution.py` | Guard resolution tests |
| `tests/pipeline/test_invariant_pass.py` | Invariant pass tests |
| `tests/test_sc_roadmap_refactor.sh` | Shell test with 20+ sc- path references |

## MEDIUM: Script/Shell Files

| File | Lines | Context | Type |
|------|-------|---------|------|
| `scripts/sync_from_framework.py` | 82-84, 96, 99, 102, 444 | Content transformer rewrites commands to `/sc:` prefix | DISPATCH |
| `.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` | 2 | Comment: `File inventory for /sc:cleanup-audit` | PATH |
| `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` | 2 | Same as above (source copy) | PATH |
| `.dev/research/research-memory-optimization.sh` | 7, 31-32, 68, 85 | References `/sc:research` skill and `commands/sc/research.md` | PATH |

## LOW: Documentation Files (88 files in docs/)

| Subdirectory | File Count | Examples |
|--------------|-----------|----------|
| `docs/generated/` | 28 | audit-wiring-detection-analysis.md, roadmap-cli-tools-release-guide.md, SuperClaude-Developer-Guide-Commands-Skills-Agents.md |
| `docs/generated/dev-guide-research/` | 28 | extract-opus-*.md, extract-haiku-*.md (research extractions) |
| `docs/generated/contributor-knowledge-base/` | 3 | architecture-guide.md, commands-skills-cross-reference.md, visual-architecture-summary.md |
| `docs/user-guide/` | 7 | agents.md, commands.md, flags.md, mcp-installation.md, mcp-servers.md, modes.md, session-management.md |
| `docs/reference/` | 9 | commands-list.md, examples-cookbook.md, integration-patterns.md, troubleshooting.md, advanced-patterns.md |
| `docs/developer-guide/` | 4 | contributing-code.md, technical-architecture.md, testing-debugging.md, README.md |
| `docs/research/` | 6 | competitive-landscape-*.md, skills-migration-test.md, complete-python-skills-migration.md |
| `docs/analysis/` | 4 | superpowers-vs-superclaude-comparison.md, claude-code-best-practice-vs-superclaude.md |
| `docs/guides/` | 1 | cli-portify-and-pipeline-runner-guide.md |
| `docs/getting-started/` | 2 | quick-start.md, installation.md |

## LOW: Release/Dev Artifacts (1,228 files in .dev/)

The `.dev/releases/` tree contains the largest volume of `sc:` references across historical release artifacts, tasklist outputs, planning docs, and brainstorm results. These are archival and low-risk for rename impact.

| Subdirectory Pattern | Approx File Count |
|---------------------|-------------------|
| `.dev/releases/complete/` | ~1,100 |
| `.dev/releases/backlog/` | ~80 |
| `.dev/releases/current/` | ~30 |
| `.dev/research/` | ~18 |

## Cross-Reference: JSON Files with sc: (eval/workspace data)

| File | Type |
|------|------|
| `.claude/skills/sc-release-split-protocol-workspace/trigger-eval-set.json` | Eval prompts with `/sc:release-split` |
| `.claude/skills/sc-release-split-protocol-workspace/evals/evals.json` | Eval definitions with `/sc:release-split` |
| `.claude/skills/sc-release-split-protocol-workspace/iteration-1/benchmark.json` | Benchmark with skill path |
| `.claude/skills/sc-release-split-protocol-workspace/iteration-1/*/eval_metadata.json` | Per-eval metadata (4 files) |
| `.claude/skills/sc-release-split-protocol-workspace/iteration-1/*/with_skill/grading.json` | Grading results (2 files) |
| `.claude/skills/sc-release-split-protocol-workspace/fidelity-stress/*/fidelity-check-results.json` | Fidelity check results (2 files) |
| `.dev/releases/complete/v2.01-Architecture-Refactor/v2.01-release-validation-debates/results/*.json` | Historical validation results |
| `.dev/research/process-improvement-debate/manifest.json` | Debate orchestration manifest |

## Rename Impact Assessment

### Highest Risk (code changes break functionality)
1. **`src/superclaude/cli/main.py`** -- hardcoded default path `~/.claude/commands/sc`
2. **`src/superclaude/cli/install_commands.py`** -- all install logic targets `commands/sc/`
3. **`src/superclaude/cli/install_skills.py`** -- `sc-*` glob patterns and `/sc:` mapping
4. **`src/superclaude/cli/cli_portify/resolution.py`** -- `sc:` prefix parsing regex
5. **`scripts/sync_from_framework.py`** -- Content transformer adds `/sc:` prefix
6. **`Makefile`** -- `commands/sc` and `skills/sc-*-protocol` globs

### Medium Risk (prompts/behavior changes)
7. **`src/superclaude/cli/sprint/process.py`** -- `/sc:task-unified` in prompt strings
8. **`src/superclaude/cli/cleanup_audit/prompts.py`** -- 5 prompts with `/sc:task-unified`
9. **`src/superclaude/cli/roadmap/validate_prompts.py`** -- `sc:tasklist` references
10. **All agent `.md` files** (8 files, 4 pairs) -- `/sc:` command invocation references

### Lower Risk (directory renames, docs updates)
11. **26 skill directories** (13 src + 13 .claude) -- all named `sc-*-protocol`
12. **83 command files** (41 .claude/commands/sc/ + 42 src/superclaude/commands/) -- directory path
13. **88 documentation files** -- textual references
14. **18 test files** -- test expectations and path references
15. **1,228 .dev/ artifact files** -- historical/archival only
