# /sc:task — Current State Snapshot

> Source: Wave-1 R7 (Explore agent) verbatim output. Citations are file:line.

## 1. Surface

### Command file paths
- Source of truth: `src/superclaude/commands/task.md`
- Dev copy: `.claude/commands/sc/task.md`
- Source and dev copy match for the inspected surface.

### Command metadata (`src/superclaude/commands/task.md:1-9`)
- `name: task`
- `description: "Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation"`
- `category: special`
- `complexity: advanced`
- `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`
- `mcp-servers: [sequential, context7, serena, playwright, magic, morphllm]`
- `personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]`
- `version: "2.0.0"`

### Description / philosophy (`src/superclaude/commands/task.md:14-27`)
- Orthogonal dimensions: `/sc:task [operation] --strategy [systematic|agile|enterprise] --compliance [strict|standard|light|exempt]`
- Strategy: how to coordinate work. Compliance: how strictly to enforce quality.
- Philosophy: "Better false positives than false negatives" when uncertain.

### Arguments and modes
- Command file usage (`src/superclaude/commands/task.md:40-42`): `/sc:task [operation] [target] [flags]`
- Skill usage (`src/superclaude/skills/sc-task-protocol/SKILL.md:39-45`):
  - `/sc:task [description]`
  - `/sc:task [description] --compliance strict`
  - `/sc:task [description] --compliance light`
  - `/sc:task [description] --skip-compliance`
  - `/sc:task [description] --verify auto`

### Flags

#### Listed directly in command file (`src/superclaude/commands/task.md:44-48`)
- `--strategy`, `--compliance`, `--verify`, `--skip-compliance`, `--force-strict`, `--parallel`, `--delegate`, `--no-escalation`
- Only `--no-escalation` has an in-file table description (default `false`): "Bypass TFEP (Test Failure Escalation Protocol) triggers. When set, agents may fix test failures directly without structured forensic analysis. WARNING: Using --no-escalation voids TFEP protection against ad-hoc fixes."

#### Expanded flag inventory (`src/superclaude/core/COMMANDS.md:86-119`)
Strategy:
- `--strategy systematic` — comprehensive, methodical; large features & multi-domain.
- `--strategy agile` — iterative, sprint-oriented; feature backlog.
- `--strategy enterprise` — governance-focused, compliance-heavy; regulated.
- `--strategy auto` — auto-detect; default.

Compliance:
- `--compliance strict` — full MCP workflow enforcement; multi-file, security, refactoring.
- `--compliance standard` — core rules enforcement; single-file code changes.
- `--compliance light` — awareness only; minor fixes/formatting.
- `--compliance exempt` — no enforcement; questions, exploration, docs.
- `--compliance auto` — auto-detect; default.

Verification:
- `--verify critical` — full sub-agent verification.
- `--verify standard` — direct test execution only.
- `--verify skip` — skip verification, use with caution.
- `--verify auto` — auto-select by compliance tier; default.

Execution control:
- `--skip-compliance` — escape hatch; bypass all compliance enforcement.
- `--force-strict` — override auto-detection to STRICT.
- `--parallel` — parallel sub-agent execution.
- `--delegate` — sub-agent delegation.
- `--reason "..."` — required justification for tier override.

Global flags (`src/superclaude/commands/help.md:89-126`):
- `--delegate [auto|files|folders]`, `--concurrency [n]`, `--loop`, `--iterations [n]`, `--validate`, `--safe-mode`, `--token-efficient`, `--scope [file|module|project|system]`, `--focus [performance|security|quality|architecture|accessibility|testing]`

### Examples (`src/superclaude/commands/task.md:106-148`)
1. `/sc:task "fix security vulnerability in auth module"` → STRICT, conf 0.95, keywords security/vulnerability/auth.
2. `/sc:task "explain how the routing middleware works"` → EXEMPT, conf 0.92.
3. `/sc:task "fix typo in error message"` → LIGHT, conf 0.95.
4. `/sc:task "add pagination to user list endpoint"` → STANDARD, conf 0.85.

Additional protocol examples (`src/superclaude/skills/sc-task-protocol/SKILL.md:288-331`):
- `/sc:task "implement user authentication with JWT"` → STRICT
- `/sc:task "add pagination to user list"` → STANDARD
- `/sc:task "fix typo in README"` → LIGHT
- `/sc:task "explain how the auth flow works"` → EXEMPT
- `/sc:task "update config file" --compliance strict` → user-forced STRICT

## 2. Protocol / Skill

### Skill paths
- Source: `src/superclaude/skills/sc-task-protocol/SKILL.md`
- Init: `src/superclaude/skills/sc-task-protocol/__init__.py`
- Dev copy: `.claude/skills/sc-task-protocol/SKILL.md`
- Skill metadata (`SKILL.md:1-5`): `name: sc:task-protocol`; allowed tools `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task`.

### Sub-files in skill
Only `SKILL.md` and `__init__.py`. **No** `refs/`, `rules/`, `templates/`, `scripts/`, or `config/` subdirectories exist under the skill — though the protocol references config files (see Known Issues §3).

### Architectural split (command vs skill)
- Command performs classification first; skill handles execution for STANDARD/STRICT only.
- `sc-task-protocol/SKILL.md:7-9` (verbatim):
  > "Classification has already been performed by the `/sc:task` command before this skill was invoked. The classification header has already been emitted. Do NOT emit it again. This skill handles execution only for STANDARD and STRICT tier tasks."

### Classification header gate (`task.md:50-67`)
- First output MUST be exact HTML comment block:
  ```
  <!-- SC:TASK-UNIFIED:CLASSIFICATION -->
  TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
  CONFIDENCE: [0.00-1.00]
  KEYWORDS: [matched keywords or "none"]
  OVERRIDE: [true|false]
  RATIONALE: [one-line reason]
  <!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
  ```
- Rules: no tool invocation during classification; exact format; only STRICT/STANDARD/LIGHT/EXEMPT valid; header must be first output.

### Tier logic — command file (`task.md:69-91`, verbatim)
Priority order (first match wins; `--compliance` override checked first):
1. **STRICT** (P1, safety-critical) — keywords: security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth. Context boosters: >2 files (+0.3), security paths `auth/`, `security/`, `crypto/` (+0.4). Compound: "fix security", "add authentication", "update database", "change api". Note: "quick security" → STRICT; "minor auth change" → STRICT.
2. **EXEMPT** (P2, non-code) — explain, search, commit, push, plan, discuss, brainstorm, what, how, why. Boosters: is_read_only +0.4, is_git_operation +0.5, all doc files +0.5. Patterns: starts with what/how/why/explain, docs-only paths.
3. **LIGHT** (P3, trivial) — typo, comment, whitespace, lint, docstring, formatting, spacing, minor. Boosters: single file +0.1, ≤50 lines. Compound: "quick fix", "minor change", "fix typo", "refactor comment".
4. **STANDARD** (P4, default) — implement, add, create, update, fix, build, modify, change. Default tier when no higher-priority tier matches.

Low-confidence rule: if confidence <0.70, prompt user with `--compliance [tier]` override hint.

### Tier logic — orchestrator (`src/superclaude/core/ORCHESTRATOR.md:151-213`)
Classification decision tree:
- step_1_override: `user_override_tier != null` → use override @ 100% confidence.
- step_2_compound: compound phrase detected → use compound tier @ 90% confidence.
- step_3_keywords: score all keywords, apply context boosters (sum of `keyword_matches * weight` + context_boosts).
- step_4_resolve: scores within 0.1 → escalate to higher priority. Priority STRICT > EXEMPT > LIGHT > STANDARD.
- step_5_confidence: <0.7 → prompt user for confirmation.

Context boosters (orchestrator):
- `estimated_files > 2` → STRICT +0.3.
- `estimated_files == 1` → LIGHT +0.1.
- Security path → STRICT +0.4.
- All test files → STANDARD +0.2.
- All doc files → EXEMPT +0.5.
- Read-only → EXEMPT +0.4.
- Git operation → EXEMPT +0.5.

### Tier logic — tasklist protocol (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:505-575`)
Includes a parallel deterministic classification algorithm for generated tasklists, with extended keyword tables (e.g. `small update`, `update comment`, `fix spacing`, `fix lint`, `rename variable`). Weight scheme: STRICT/EXEMPT +0.4, LIGHT +0.3, STANDARD +0.2 per keyword. Compound match: +0.15 confidence. Path boosters: `auth|security|crypto` +0.4 STRICT, `docs|*.md` +0.5 EXEMPT, `tests/` +0.2 STANDARD. Base confidence `max(tier_scores)` capped 0.95; –15% if top-two within 0.1; +15% if compound; –30% if no keywords; <0.7 requires confirmation.

### Execution routing (`task.md:93-100`)
- EXEMPT: execute immediately; no Skill.
- LIGHT: execute directly; no Skill.
- STANDARD / STRICT: invoke `Skill sc:task-protocol`.

### Protocol execution per tier (`SKILL.md:76-123`)
STRICT (11 steps): activate Serena project → verify clean git → load codebase context (Auggie) → check memories → identify affected files & tests → make changes with checklist → identify all importers → update affected files → spawn quality-engineer → `pytest [path] -v` → answer adversarial questions.

STANDARD (5 steps): load context via codebase-retrieval → search downstream impacts (`find_referencing_symbols` or grep) → make changes → run affected tests or document manual verification → verify basic functionality.

LIGHT (4 steps): quick scope check → make changes → quick sanity check → proceed with judgment.

EXEMPT (2 steps): execute immediately → no verification overhead.

Verification routing table (`SKILL.md:110-123`):
- STRICT → quality-engineer sub-agent, 3-5K tokens, 60s.
- STANDARD → direct test execution, 300-500 tokens, 30s.
- LIGHT → skip verification.
- EXEMPT → skip verification.
- Critical path override (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) → always CRITICAL verification regardless of tier.
- Trivial path override (`*.md`, `docs/`, `*test*.py`) → may skip verification.

### TFEP gates (`SKILL.md:125-244`)
Prohibitions: no ad-hoc fixes on test failures; no modifying test expectations without adversarial validation; no patches derived from test output.

Permitted direct-fix exceptions: single ImportError/NameError in newly written test scaffolding affecting ≤2 tests; lint/formatting; deprecation warnings.

Baseline: capture existing test files/functions before implementation; classify failures as pre-existing or new.

Escalation triggers: any pre-existing test fails; ≥3 new tests fail simultaneously; runtime exceptions in implementation code; repeated failure, multi-file blast radius, low-confidence RCA, unresolved adversarial outcome, second failed retest, cross-domain regression.

Forensic invocation (`SKILL.md:191-197`):
- First trigger: `/sc:forensic --tier light --intent triage --caller task-unified ...`
- Second trigger: `/sc:forensic --tier standard ...`
- Third trigger: full stop.
- The `--caller task-unified` string is a lingering naming artifact.

## 3. MCP integration

### Servers referenced by command (`task.md:7`)
`sequential, context7, serena, playwright, magic, morphllm`

### Core command docs (`src/superclaude/core/COMMANDS.md:81-84`)
- Sequential for analysis. Serena for context. Context7 for patterns.
- Tools: TodoWrite, Read, Grep, Glob, Edit, MultiEdit, Task, Bash.

### MCP requirements by tier (`SKILL.md:253-263`)
- STRICT: Sequential + Serena (fallback NOT allowed).
- STANDARD: Sequential + Context7 (fallback allowed).
- LIGHT: none required (fallback allowed).
- EXEMPT: none required.
- Required servers unavailable for STRICT → block task execution.

### Tool coordination (`SKILL.md:265-284`)
- Planning: TodoWrite, codebase-retrieval, `list_memories`/`read_memory`.
- Execution: Edit/MultiEdit/Write, Grep/Glob, `find_referencing_symbols`.
- Verification: Task quality-engineer (STRICT), Bash (STANDARD), `think_about_task_adherence`.
- Completion: `write_memory`, `think_about_whether_you_are_done`.

### Auggie / codebase retrieval
`codebase-retrieval` invoked at `SKILL.md:83, 94, 269`. Tool capability named rather than server `auggie`.

### Sprint CLI integration
`src/superclaude/cli/sprint/process.py:123-183` builds: `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` plus tier instructions.

### Cleanup audit integration
Five prompt builders at `src/superclaude/cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116` invoke `/sc:task`.

## 4. Eval / release history

### v2.0-task-unified — namespace collision (HIGH risk)
`.dev/releases/complete/v.2.0-task-unified/`:
- `UNIFIED-TASK-COMMAND-SPEC.md` — original goal: merge `sc:task` orchestration with `sc:task-mcp` compliance enforcement.
- `task-vs-task-unified-framework.md:9-23` — judged sc:task and sc:task-unified as versions of the same command; `task-unified.md` was canonical successor; legacy `task.md` still installed.
- `task-vs-task-unified-crossrefs.md:19-23` — both `task.md` and `task-unified.md` declared `name: task`; routing ambiguity.
- `task-vs-task-unified-risk-assessment.md:9-13` — HIGH risk; three `.md` files coexisted: `task.md`, `task-unified.md`, `task-mcp.md`.
- `task-vs-task-unified-trigger-risks.md:9-12` — multiple collision vectors; skill directed users to `/sc:task`, not `/sc:task-unified`.

### v3.7-task-unified-v2 — naming consolidation completed
`.dev/releases/complete/v3.7-task-unified-v2/`:
- Three strands: Checkpoint Enforcement, Sprint TUI v2, Naming Consolidation.
- `HANDOVER.md:51-60`: canonicalized on `/sc:task`; `commands/task-unified.md` → `commands/task.md`; `skills/sc-task-unified-protocol/` → `skills/sc-task-protocol/`.
- `HANDOVER.md:64-71`: zero live `/sc:task-unified` references in `src/` or `.claude/`.
- `TEST-SPEC.md:34-80`: enforces no `/sc:task-unified` strings; `ClaudeProcess.build_prompt` must start with `/sc:task`.
- `ValidationReport.md:1-33`: CLEAN structural self-check.
- `release-split/release-split-report.md`: SPLIT release; R1 ("Fix the Pipeline") delivered naming + checkpoint; R2 ("Show the Pipeline") depended on R1.

### Checkpoint-RCA (`v3.7-task-unified-v2/artifacts/troubleshoot-missing-p03-checkpoint.md`)
- Phase 3 completed tasks but failed to write checkpoint files (`:10-18`).
- Triple-failure chain (`:21-75`): no checkpoint instructions in prompt; phase had two structurally distinct checkpoint sections; no post-phase checkpoint enforcement in sprint executor.
- Historical failure trace (`:111-119`) still shows `/sc:task-unified Execute all tasks...` (pre-canonicalization history).

### v3.75-RigorflowMerger backlog (current)
`.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/`:
- `strategy-ic-task-unified.md`, `improve-task-unified-tier.md`, `comparison-task-unified-tier.md`
- `strategy-ic-sprint-executor.md`, `improve-sprint-executor.md`, `comparison-sprint-executor.md`

## 5. Known issues / gaps

1. **Lingering `task-unified` naming artifacts in live protocol**:
   - `task.md:60,66` — `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header sentinel.
   - `SKILL.md:196` — `--caller task-unified` in TFEP forensic invocation.
   - May be intentional telemetry compatibility; not explained in source.

2. **Skill protocol references config files that do not exist**:
   - `SKILL.md:359-365` references `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml`, `MCP.md`, `ORCHESTRATOR.md`.
   - No `config/` directory under `sc-task-protocol`.

3. **Flag reference split**: `task.md:44` says "See protocol skill for full flag reference"; protocol skill (`SKILL.md:37-45`) only shows subset (`--compliance strict|light`, `--skip-compliance`, `--verify auto`). Full inventory lives only in `core/COMMANDS.md:86-119`.

4. **`/sc:tasklist` duplicates and extends tier logic** (`sc-tasklist-protocol/SKILL.md:505-575`). Drift: tasklist protocol adds `small update`, `update comment`, `fix spacing`, `fix lint`, `rename variable` LIGHT compounds; adds remove/delete/deprecate STANDARD keywords; assigns numeric weights not in command file. Sync risk between source files and dev copies.

5. **STRICT critical-fail conditions not formalized**: live skill has STRICT MCP unavailability block but no full CRITICAL condition model (output absent, classification header absent).

6. **Output-type discrimination missing**: live routing is tier-only + path overrides; no `code|analysis|documentation|opinion` output-type axis.

7. **Low-confidence behavior under-specified operationally**: `task.md:91` says "prompt user"; not deterministic blocking with reason/competing tier/keyword split.

8. **v3.7 operational follow-ups still open** (HANDOVER `:375-391`): wire `--checkpoint-gate-mode` CLI flag; `_resolve_release_dir` consistent grandparent walk; live run with stream-json stub or real claude; ruff cleanup; optional full 10-stage validation agents.

9. **Wave-4 checkpoint heading parser bug** (fixed in v3.7 HANDOVER `:253-304`): pre-fix parser matched legacy `### Checkpoint:` but not Wave-4 `### T<PP>.<NN> -- Checkpoint:`. Verified +3 tests, no regressions.
