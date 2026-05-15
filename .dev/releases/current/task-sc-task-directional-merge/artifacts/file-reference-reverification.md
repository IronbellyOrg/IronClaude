# File Reference Re-verification — Phase 7 / T07.02

**Task:** T07.02 — Re-verify file references & check compat hazards
**Roadmap Item:** R-025
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Deliverable artifact #1 of T07.02 (companion: `compat-hazard-report.md`).

---

## 0. Scope & corpus

**Plan corpus re-verified:**

`merge-master.md` is the intended single unified plan, but per `CP-P06-END.md` it is **0 bytes (empty)** — T06.05 did not execute its consolidation step. The five upstream refactor files contain the full change-row inventory and are individually complete (gate-pass at CP-P06-END):

| Source file | Lines | Role |
|---|---|---|
| `refactor-task-skill.md` | 349 | `[src] src/superclaude/skills/task/SKILL.md` edits (CR-TASK-01..12) |
| `refactor-mdtm-frontmatter.md` | 193 | MDTM `Tier:` field + inline-marker schema (CR-FM-01..04) |
| `refactor-sctask-deprecation.md` | 224 | `/sc:task` command + `sc-task-protocol/` deprecation (CR-DEP-01..05) |
| `refactor-references.md` | 558 | Cross-repo reference enumeration & treatment (CR-REF-NN) |
| `refactor-distribution.md` | 242 | Installer / sync rule edits (CR-DIST-NN) |
| `refactor-documentation.md` | 412 | Documentation surface edits (CR-DOC-NN) |

This re-verification operates on the union of file references across those six files (Phase 7 must accept that `merge-master.md` is the consolidation gap, not a content gap — every Phase 7 row is sourced from a verified Phase 6 refactor file).

**Side-tagging convention (R-RULE-10):** every operative path is `[src]` (`src/superclaude/...`, top-level source) or `[.claude]` (`.claude/...` dev-copy mirror). `[.claude]` is refreshed by `make sync-dev` from `[src]`; manual `[.claude]` edits are forbidden. Task data (under `.dev/tasks/to-do/TASK-*/`) and release artifacts (under `.dev/releases/...`) are *not synced* — neither side tag applies; they are repo-resident state.

---

## 1. Re-verification methodology

For each unique path string extracted from the six source files:

1. **Concrete files** (no glob): `test -e <path>` on disk.
2. **Directories** (trailing slash): `test -d <path>` on disk.
3. **Glob patterns** (`**/*.md`, `*.md`, `TASK-*/`): verify the **anchor directory** exists and count matching files to confirm the population is real, not a phantom.
4. **Side tag**: classify each path as `[src]` / `[.claude]` / `.dev` (release/task data) / `docs` / `tests` / `scripts` / `Makefile` / `top-level` based on the path prefix.
5. **Planned-new files** (paths that do not exist but are introduced by a CR-NN row): flag as `PLANNED-NEW` with the originating CR-ID. These are *not* failures.

Total unique paths extracted: **185** (raw); after de-duplication of partial/truncated strings, the **operative** set is enumerated below.

---

## 2. Concrete-path verification table

### 2.1 `[src]` — source-of-truth code under `src/superclaude/`

| # | Path | Side | Status | Source CR(s) | Notes |
|---|---|---|---|---|---|
| 1 | `src/superclaude/skills/task/SKILL.md` | `[src]` | **VERIFIED present** | CR-TASK-01..12, CR-FM-01..04 (schema doc target) | Recipient surface; 32951 B per T06.01 |
| 2 | `src/superclaude/skills/sc-task-protocol/SKILL.md` | `[src]` | **VERIFIED present** | CR-DEP-03 (delete target) | Donor; 14925 B per T06.01 |
| 3 | `src/superclaude/skills/sc-task-protocol/__init__.py` | `[src]` | **VERIFIED present** | CR-DEP-04 (delete target) | Package marker |
| 4 | `src/superclaude/commands/task.md` | `[src]` | **VERIFIED present** | CR-DEP-01 (rewrite to stub) | `/sc:task` command file; soft-deprecate target |
| 5 | `src/superclaude/commands/adversarial.md` | `[src]` | **VERIFIED present** | refactor-references.md `[src]` corpus | Adjacent command — no edit by this sprint |
| 6 | `src/superclaude/commands/help.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 7 | `src/superclaude/commands/release-split.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 8 | `src/superclaude/commands/tasklist.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 9 | `src/superclaude/commands/validate-roadmap.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 10 | `src/superclaude/commands/validate-tests.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 11 | `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 12 | `src/superclaude/skills/sc-release-split-protocol/SKILL.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 13 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 14 | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 15 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 16 | `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md` | `[src]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 17 | `src/superclaude/cli/sprint/process.py` | `[src]` | **VERIFIED present** | CR-REF-01 (lines 124 + 170) | Sprint executor emitting `/sc:task` |
| 18 | `src/superclaude/cli/sprint/config.py` | `[src]` | **VERIFIED present** | CR-REF-03 (line 240) | Adjacent docstring fix |
| 19 | `src/superclaude/cli/sprint/checkpoints.py` | `[src]` | **VERIFIED present** | CR-REF-03 (line 28) | Adjacent docstring fix |
| 20 | `src/superclaude/cli/cleanup_audit/prompts.py` | `[src]` | **VERIFIED present** | CR-REF-02 (lines 26, 47, 69, 92, 116) | 5 prompt builders |
| 21 | `src/superclaude/cli/tasklist/prompts.py` | `[src]` | **VERIFIED present** | CR-REF-03 (line 158) | Adjacent docstring fix |
| 22 | `src/superclaude/cli/roadmap/validate_prompts.py` | `[src]` | **VERIFIED present** | CR-REF-03 (lines 82, 126) | Adjacent docstring fix |
| 23 | `src/superclaude/cli/install_skills.py` | `[src]` | **VERIFIED present** | CR-DIST-NN (installer gate) | Distribution |
| 24 | `src/superclaude/cli/install_skill.py` | `[src]` | **VERIFIED present** | refactor-distribution.md | Singular install helper |
| 25 | `src/superclaude/cli/install_commands.py` | `[src]` | **VERIFIED present** | CR-DIST-NN | Installer |
| 26 | `src/superclaude/cli/main.py` | `[src]` | **VERIFIED present** | refactor-references.md mention | No edit by this sprint |
| 27 | `src/superclaude/core/COMMANDS.md` | `[src]` | **VERIFIED present** | refactor-references.md / refactor-documentation.md | Documentation source |
| 28 | `src/superclaude/core/ORCHESTRATOR.md` | `[src]` | **VERIFIED present** | refactor-references.md / refactor-documentation.md | Documentation source |
| 29 | `src/superclaude/examples/release-spec-template.md` | `[src]` | **VERIFIED present** | refactor-references.md | Template — no edit |
| 30 | `src/superclaude/examples/tasklist_index_template.md` | `[src]` | **VERIFIED present** | refactor-references.md | Template — no edit |
| 31 | `src/superclaude/examples/tasklist_phase_template.md` | `[src]` | **VERIFIED present** | refactor-references.md | Template — no edit |

**`[src]` directories cross-verified (enumeration anchors):** `src/superclaude/skills/`, `src/superclaude/commands/`, `src/superclaude/examples/` — all present.

### 2.2 `[.claude]` — dev-copy mirrors under `.claude/`

| # | Path | Side | Status | Source CR(s) | Notes |
|---|---|---|---|---|---|
| 32 | `.claude/skills/task/SKILL.md` | `[.claude]` | **VERIFIED present** | CR-TASK-01..12 sync target | Mirror of #1 (md5-paired per T06.01) |
| 33 | `.claude/skills/sc-task-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | CR-DEP-04 delete-via-sync target | Mirror of #2 |
| 34 | `.claude/commands/sc/task.md` | `[.claude]` | **VERIFIED present** | CR-DEP-02 (sync of stub) | Mirror of #4; note layout reshape `commands/` → `commands/sc/` |
| 35 | `.claude/commands/sc/adversarial.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 36 | `.claude/commands/sc/help.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 37 | `.claude/commands/sc/release-split.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 38 | `.claude/commands/sc/tasklist.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 39 | `.claude/commands/sc/validate-roadmap.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 40 | `.claude/commands/sc/validate-tests.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 41 | `.claude/skills/sc-cli-portify-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 42 | `.claude/skills/sc-release-split-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 43 | `.claude/skills/sc-roadmap-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 44 | `.claude/skills/sc-tasklist-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 45 | `.claude/skills/sc-validate-roadmap-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 46 | `.claude/skills/sc-validate-tests-protocol/SKILL.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Adjacent — no edit |
| 47 | `.claude/agent-memory/rf-assembler/assembly-patterns.md` | `[.claude]` | **VERIFIED present** | refactor-references.md (one match) | Agent-memory adjacent |
| 48 | `.claude/templates/documents/release-spec-template.md` | `[.claude]` | **VERIFIED present** | refactor-references.md | Template adjacent |
| 49 | `.claude/settings.json` | `[.claude]` | **VERIFIED present** | refactor-documentation.md (workspace-override hook) | Hook config |

**`[.claude]` directories cross-verified:** `.claude/commands/sc/`, `.claude/skills/`, `.claude/templates/`, `.claude/agent-memory/` — all present.

### 2.3 Documentation (`docs/`) — neither `[src]` nor `[.claude]`

| # | Path | Side | Status | Source CR(s) | Notes |
|---|---|---|---|---|---|
| 50 | `docs/user-guide/commands.md` | docs | **VERIFIED present** | CR-DOC-NN | ~27 `/sc:task` matches per refactor-documentation.md § 0.1 |
| 51 | `docs/user-guide/flags.md` | docs | **VERIFIED present** | CR-DOC-NN | 1 match |
| 52 | `docs/user-guide/freshness-hooks.md` | docs | **VERIFIED present** | adjacent (not edited) | Mentioned in inventory only |
| 53 | `docs/sprint-cli-deep-dive.md` | docs | **VERIFIED present** | CR-DOC-NN | 1 match |
| 54 | `docs/analysis-sc-tasklist.md` | docs | **VERIFIED present** | refactor-documentation.md inventory | — |
| 55 | `docs/analysis/bmad-vs-superclaude-comparison.md` | docs | **VERIFIED present** | refactor-documentation.md | 1 of 4 analysis files |
| 56 | `docs/analysis/claude-code-best-practice-vs-superclaude.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 57 | `docs/analysis/openclaw-vs-superclaude-comparison.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 58 | `docs/analysis/superpowers-vs-superclaude-comparison.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 59 | `docs/guides/cli-portify-and-pipeline-runner-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | 1 of 6 guides |
| 60 | `docs/guides/prd-skill-release-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 61 | `docs/guides/roadmap-cli-tools-release-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 62 | `docs/guides/sprint-cli-tools-release-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 63 | `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 64 | `docs/guides/tdd-skill-release-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 65 | `docs/research/competitive-landscape-final-report-2026-03-23.md` | docs | **VERIFIED present** | refactor-documentation.md | 1 of 3 top-level research files |
| 66 | `docs/research/competitive-landscape-tasklist-execution-2026.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 67 | `docs/research/superpowers-vs-superclaude-comparison.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 68 | `docs/research/dev-guide-research/00-file-inventory.md` | docs | **VERIFIED present** | refactor-documentation.md | dev-guide-research bucket |
| 69 | `docs/research/dev-guide-research/extract-haiku-08-commands-core.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 70 | `docs/research/dev-guide-research/extract-haiku-09-orchestrator-core.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 71 | `docs/research/dev-guide-research/extract-haiku-12-skills-multi.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 72 | `docs/research/dev-guide-research/extract-haiku-15-commands-examples.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 73 | `docs/research/dev-guide-research/extract-opus-06-advanced-patterns.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 74 | `docs/research/dev-guide-research/extract-opus-08-commands-core.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 75 | `docs/research/dev-guide-research/extract-opus-09-orchestrator-core.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 76 | `docs/research/dev-guide-research/extract-opus-12-skills-multi.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 77 | `docs/research/dev-guide-research/extract-opus-15-commands-examples.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 78 | `docs/research/dev-guide-research/extract-opus-20-roadmap-v2-spec.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 79 | `docs/generated/cleanup-sc-prefix-reference-index.md` | docs | **VERIFIED present** | refactor-documentation.md | Generated artifact |
| 80 | `docs/generated/cleanup-sc-prefix-rename-tasklist.md` | docs | **VERIFIED present** | refactor-documentation.md | Generated artifact |
| 81 | `docs/generated/cli-portify-release-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | Generated artifact |
| 82 | `docs/generated/contributor-knowledge-base/architecture-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 83 | `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 84 | `docs/generated/contributor-knowledge-base/components-guide.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 85 | `docs/generated/contributor-knowledge-base/visual-architecture-summary.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 86 | `docs/generated/sprint-cli/00-overview.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 87 | `docs/generated/sprint-cli/03-execution-engine.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 88 | `docs/generated/sprint-cli/05-pm-agent.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 89 | `docs/generated/sprint-cli/07-skills-commands.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 90 | `docs/generated/sprint-cli/09-wiring-validation.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 91 | `docs/generated/sprint-cli/10-critique-validation.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 92 | `docs/generated/sprint-cli/debates/debate-file-preloading.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 93 | `docs/generated/sprint-cli/debates/debate-strict-halt.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 94 | `docs/generated/sprint-cli/v3.7-refactor/chunk-03-naming-consolidation.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 95 | `docs/generated/sprint-cli/v3.7-refactor/chunk-05-cross-cutting.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 96 | `docs/generated/sprint-cli/v3.7-refactor/context-01-path-a-deficiencies.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 97 | `docs/generated/sprint-cli/v3.7-refactor/context-03-v37-spec-gap-analysis.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 98 | `docs/generated/sprint-cli/v3.7-refactor/MERGED-REFACTORING-RECOMMENDATION.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 99 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-adversarial/merged-spec-gen-prompt.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 100 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-prompt-architect.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 101 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-prompt-incremental.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 102 | `docs/generated/sprint-cli/v3.7-refactor/spec-gen-prompt-qa.md` | docs | **VERIFIED present** | refactor-documentation.md | — |
| 103 | `docs/generated/tasklist-unwired-components-remediation.md` | docs | **VERIFIED present** | refactor-documentation.md | — |

**`docs/` directories cross-verified:** `docs/user-guide/`, `docs/analysis/`, `docs/guides/`, `docs/reference/`, `docs/developer-guide/`, `docs/generated/`, `docs/research/`, `docs/research/dev-guide-research/`, `docs/generated/contributor-knowledge-base/`, `docs/generated/sprint-cli/` — all present.

### 2.4 Tests, scripts, top-level

| # | Path | Side | Status | Source CR(s) | Notes |
|---|---|---|---|---|---|
| 104 | `tests/cli/test_install_hooks.py` | tests | **VERIFIED present** | refactor-distribution.md (cited as parallel pattern) | Already exists per git status |
| 105 | `tests/sprint/test_process.py` | tests | **VERIFIED present** | CR-REF-09 (update `assert prompt.startswith(...)`) | — |
| 106 | `tests/sprint/test_tui_v2_wave2.py` | tests | **VERIFIED present** | refactor-references.md adjacency mention | No edit by this sprint |
| 107 | `tests/pipeline/test_process.py` | tests | **VERIFIED present** | refactor-references.md adjacency | — |
| 108 | `Makefile` | top-level | **VERIFIED present** | refactor-distribution.md (sync rules) | — |
| 109 | `scripts/sync_from_framework.py` | scripts | **VERIFIED present** | CR-REF-11 (line 84 doc reference) | — |
| 110 | `CLAUDE.md` | top-level | **VERIFIED present** | adjacent (no edit) | — |
| 111 | `README.md` | top-level | **VERIFIED present** | refactor-documentation.md (top-level inventory) | — |
| 112 | `pyproject.toml` | top-level | **VERIFIED present** | refactor-distribution.md (entry points) | — |

### 2.5 `.dev/` release artifacts & task data

| # | Path | Side | Status | Source CR(s) | Notes |
|---|---|---|---|---|---|
| 113 | `.dev/releases/current/task-sc-task-directional-merge/artifacts/transfer-manifest.md` | `.dev` | **VERIFIED present** | self-reference | Manifest |
| 114 | `.dev/releases/current/task-sc-task-directional-merge/` | `.dev` | **VERIFIED present** | self-reference | Sprint root |
| 115 | `.dev/releases/backlog/prd-artifact-containment/spec.md` | `.dev` | **VERIFIED present** | refactor-references.md (adjacent only) | Untracked new dir per git status |
| 116 | `.dev/releases/backlog/tdd-artifact-containment/spec.md` | `.dev` | **VERIFIED present** | refactor-references.md (adjacent only) | Untracked new dir per git status |
| 117 | `.dev/releases/backlog/prd-skill-refactor/02-brainstorm-output.md` | `.dev` | **VERIFIED present** | refactor-references.md | — |
| 118 | `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 9 `.md` files |
| 119 | `.dev/releases/backlog/v3.9-UnifiedTasklist-CLI/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 2 `.md` files |
| 120 | `.dev/releases/backlog/v3.xxRigorFlowMerger/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 45 `.md` files |
| 121 | `.dev/releases/backlog/v4.xx-SkillRefactor/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 5 `.md` files |
| 122 | `.dev/releases/backlog/v4xx-analyze-auggie/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 13 `.md` files |
| 123 | `.dev/releases/backlog/v4.xx-SpawnV2/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 26 `.md` files |
| 124 | `.dev/releases/backlog/v4.xx-SprintReportScaffolding/release-spec.md` | `.dev` | **VERIFIED present** | CR-REF-NN | — |
| 125 | `.dev/releases/backlog/v5.xxforensic/` | `.dev` | **VERIFIED present** | CR-REF-NN per-file rows (14 files) | 46 `.md` files; highest-density region |
| 126 | `.dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md` | `.dev` | **VERIFIED present** | refactor-references.md | — |
| 127 | `.dev/releases/backlog/v5.xx-sc-troubleshoot-v2/adversarial-auggie-mcp.md` | `.dev` | **VERIFIED present** | refactor-references.md | — |
| 128 | `.dev/releases/backlog/v5xx-Spec-generator-framework/SC_SPEC_COMMAND.md` | `.dev` | **VERIFIED present** | refactor-references.md | — |
| 129 | `.dev/releases/backlog/v6.xx_spec-workshop/batch-1-orchestration.md` | `.dev` | **VERIFIED present** | refactor-references.md | — |
| 130 | `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` archive bucket | 47 `.md` files; untracked-new per git status (move from backlog → archive) |
| 131 | `.dev/benchmarks/v2.20-baseline/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 87 `.md` files |
| 132 | `.dev/test-fixtures/` | `.dev` | **VERIFIED present** | CR-REF-NN `leave-as-is` | 183 `.md` files |
| 133 | `.dev/tasks/to-do/` | `.dev` | **VERIFIED present** | refactor-references.md (INV-04 guidance row) | 676 `.md` files |
| 134 | `.dev/tasks/to-do/TASK-*/` (anchor: 25+ TASK directories) | `.dev` | **VERIFIED present** | CR-FM-03 (compat shim scope), CR-REF-NN (INV-04) | Populated; ≥25 TASK directories observed |

---

## 3. Planned-new paths (flag, not failure)

These paths are introduced by Phase 7 execution. They do **not** exist on disk today; their non-existence is by design and is verified against the originating CR row.

| # | Path | Side | Status | Originating CR | Justification |
|---|---|---|---|---|---|
| 135 | `tests/cli/test_install_skills.py` | tests | **PLANNED-NEW** | refactor-distribution.md CR-DIST-NN | New regression test parallel to existing `test_install_hooks.py`. Acceptance: `uv run pytest tests/cli/test_install_skills.py` passes post-merge. |
| 136 | `.dev/releases/backlog/v5.xxforensic/DEPRECATION-NOTE.md` | `.dev` | **PLANNED-NEW** | refactor-references.md (CR-REF-NN bucket-level row, `leave-with-note` treatment) | One annotation file covering all 14 files in `v5.xxforensic/` that reference `/sc:task` / `sc-task-protocol`. Acceptance: `test -f` returns true post-merge. |
| 137 | `.dev/tasks/README.md` | `.dev` | **PLANNED-NEW** | refactor-references.md (new-task guidance row) | One-line guidance: "New tasks should use `/task` (canonical) instead of `/sc:task` (soft-deprecated since 2026-MM-DD)." Acceptance: file present and contains the guidance line. |
| 138 | `docs/research/_archive/` | docs | **PLANNED-NEW (OPTIONAL)** | refactor-documentation.md (optional move) | Phase 7 may relocate `docs/research/dev-guide-research/` here to make the "frozen" nature explicit. **Not blocking**; Phase 7 records the choice. |
| 139 | `~/.claude/commands/sc/task.md` (user-side install target) | install-time | **CREATED BY** `superclaude install` (CR-DIST-NN) | Not a repo path; user environment artifact. Acceptance verified by `superclaude doctor` per refactor-distribution.md. |

---

## 4. Glob / wildcard pattern coverage

| Pattern in plan corpus | Anchor directory | Anchor exists? | Pop. (md count) | Note |
|---|---|---|---|---|
| `.claude/commands/sc/*.md` | `.claude/commands/sc/` | yes | populated | Phase 7 edits only the rows in § 2.2 |
| `.claude/skills/*/` | `.claude/skills/` | yes | populated | Adjacent skills untouched |
| `.claude/skills/sc-*-protocol/` | `.claude/skills/` | yes | populated | Adjacent `sc-*-protocol` skills untouched except `sc-task-protocol` (delete) |
| `.claude/skills/*-workspace/` | `.claude/skills/` | yes | none expected | CLAUDE.md override blocks creation; PreToolUse hook in `.claude/settings.json` enforces |
| `.dev/benchmarks/v2.20-baseline/**/*.md` | `.dev/benchmarks/v2.20-baseline/` | yes | 87 | `leave-as-is` |
| `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/**/*.md` | `.dev/releases/archive/v3.75-RigorflowMerger-task-unified-v3/` | yes | 47 | `leave-as-is` (archive bucket) |
| `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/**/*.md` | `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/` | yes | 9 | `leave-as-is` |
| `.dev/releases/backlog/v3.xxRigorFlowMerger/**/*.md` | `.dev/releases/backlog/v3.xxRigorFlowMerger/` | yes | 45 | `leave-as-is` |
| `.dev/releases/backlog/v4xx-analyze-auggie/**/*.md` | `.dev/releases/backlog/v4xx-analyze-auggie/` | yes | 13 | `leave-as-is` |
| `.dev/releases/backlog/v4.xx-SpawnV2/**/*.md` | `.dev/releases/backlog/v4.xx-SpawnV2/` | yes | 26 | `leave-as-is` |
| `.dev/releases/backlog/v5.xxforensic/**/*.md` | `.dev/releases/backlog/v5.xxforensic/` | yes | 46 | Per-file rows in CR-REF-NN for the 14 that grep-match; `leave-as-is` for the rest with single bucket `DEPRECATION-NOTE.md` (planned-new row 136) |
| `.dev/test-fixtures/**/*.md` | `.dev/test-fixtures/` | yes | 183 | `leave-as-is` |
| `.dev/tasks/to-do/TASK-*/**/*.md` | `.dev/tasks/to-do/` | yes | 676 | `leave-as-is` per INV-04 (existing TASK-* bodies are not rewritten) |
| `.dev/releases/backlog/*` | `.dev/releases/backlog/` | yes | 294 `.md` total | Bucket-level treatment in CR-REF-NN |

**All glob anchors verified.** Phase 7 has no orphaned pattern.

---

## 5. Truncated / prose-only path strings (informational, no edit target)

The plan corpus contains a small number of truncated path strings that appear in narrative prose (e.g., "see `.claude/skills/NAME` for any name", "src/superclaude/cli/install_*"). These are descriptive, not edit targets, and each is anchored to a concrete row in § 2 above:

| Prose form | Resolved concrete target(s) |
|---|---|
| `.claude/...` | covered by § 2.2 rows |
| `.claude/skills/NAME` | template form; resolved per § 2.1 / § 2.2 row pairs |
| `docs/...`, `docs/generated/...` | covered by § 2.3 |
| `docs/generated/cleanup-sc-prefix-` (truncated) | rows 79 + 80 |
| `src/superclaude/...`, `src/superclaude/skills/sc-`, `src/superclaude/cli/install_` | covered by § 2.1 |
| `src/superclaude/skills/NAME` | template form; resolved per § 2.1 |

**No truncated string maps to a missing or ambiguous target.**

---

## 6. Roll-up

| Category | Count | Verified | Planned-new | Flagged |
|---|---|---|---|---|
| `[src]` paths | 31 | 31 | 0 | 0 |
| `[.claude]` paths | 18 | 18 | 0 | 0 |
| `docs/` paths | 54 | 54 | 1 (`docs/research/_archive/` optional) | 0 |
| `tests/` paths | 4 | 4 | 1 (`test_install_skills.py`) | 0 |
| `scripts/`, `Makefile`, top-level | 5 | 5 | 0 | 0 |
| `.dev/` paths (concrete + anchored glob) | 22 | 22 | 2 (`DEPRECATION-NOTE.md`, `.dev/tasks/README.md`) | 0 |
| Glob patterns (anchor verified) | 14 | 14 | — | 0 |
| **Total operative paths** | **148** | **148** | **4** (3 mandatory + 1 optional) | **0** |

**Every plan file reference is accounted for. Zero unresolved paths. All four planned-new paths trace to a named CR row.**

---

## 7. Acceptance Criteria recap (T07.02 AC #1)

1. **`file-reference-reverification.md` exists.** ✅ — this file.
2. **Every plan file reference is re-verified or explicitly flagged.** ✅ — § 2 enumerates 134 concrete paths (all VERIFIED), § 3 enumerates 4 PLANNED-NEW paths with originating CR rows, § 4 verifies the 14 glob anchors, § 5 resolves truncated prose forms.
3. **Side-tagged.** ✅ — every `[src]` / `[.claude]` row in § 2.1 / § 2.2 carries the side tag; `docs/`, `tests/`, `scripts/`, `Makefile`, top-level, and `.dev/` paths are classified per R-RULE-10 (R-RULE-10 itself only mandates the `[src]` / `[.claude]` distinction; the other categories are non-synced and are labeled by path prefix).
4. **No unauthorized scope expansion.** ✅ — every concrete row maps to a CR row in one of the six Phase 6 refactor files (or is adjacency-only with "no edit by this sprint"); no path was discovered in T07.02 that the Phase 6 plan does not already account for.

**T07.02 file-reverification deliverable: COMPLETE.**
