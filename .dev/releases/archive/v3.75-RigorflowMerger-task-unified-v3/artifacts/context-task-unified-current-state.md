# /sc:task-unified — Current State Snapshot

> Source: Wave-1 R8 (Explore agent) verbatim output. Citations are file:line.

## 1. Surface

### Current command file path

**There is no live `task-unified.md` command file in `src/` or `.claude/`.** The v3.7 naming consolidation already merged/renamed the command back to canonical `/sc:task`.

Live command files:
- `src/superclaude/commands/task.md`
- `.claude/commands/sc/task.md`

Historical rename (`.dev/releases/complete/v3.7-task-unified-v2/HANDOVER.md:51-60`):
> "/sc:task is now the single canonical name. N1-N4: commands/task-unified.md → commands/task.md; skills/sc-task-unified-protocol/ → skills/sc-task-protocol/; old paths deleted. N5: ClaudeProcess.build_prompt emits /sc:task Execute all tasks..."

Current live surface (`src/superclaude/commands/task.md:1-9`, `.claude/commands/sc/task.md:1-9`):
- `name: task`
- `description: "Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation"`
- `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`
- `mcp-servers: [sequential, context7, serena, playwright, magic, morphllm]`
- `version: "2.0.0"`

### Command description and invocation (`task.md:14-25`, `:38-44`)
- Orthogonal dimensions: `/sc:task [operation] --strategy [systematic|agile|enterprise] --compliance [strict|standard|light|exempt]`
- Usage: `/sc:task [operation] [target] [flags]`

### Flag inventory

Live command lists (`task.md:44`):
`--strategy, --compliance, --verify, --skip-compliance, --force-strict, --parallel, --delegate, --no-escalation`

Detailed in-file entry (`task.md:46-48`): only `--no-escalation` (default `false`): "Bypass TFEP (Test Failure Escalation Protocol) triggers... WARNING: Using --no-escalation voids TFEP protection against ad-hoc fixes."

Skill examples (`SKILL.md:37-45`): only `--compliance strict|light`, `--skip-compliance`, `--verify auto`.

Fuller historical inventory (`v.2.0-task-unified/UNIFIED-TASK-COMMAND-SPEC.md:134-172`):
- Strategy: systematic, agile, enterprise, auto
- Compliance: strict, standard, light, exempt, auto
- Execution: --skip-compliance, --force-strict, --parallel, --delegate, --reason
- Verification: --verify critical|standard|skip|auto

**Gap**: command file says "See protocol skill for full flag reference" but skill only shows subset; full inventory only in historical v2.0 spec and `core/COMMANDS.md`.

### Arguments / modes (`task.md:19-25`, `:52-56`)
- Strategy: systematic, agile, enterprise, auto
- Compliance: strict, standard, light, exempt, auto
- Tiers: STRICT, STANDARD, LIGHT, EXEMPT

### Examples (`task.md:106-148`, `SKILL.md:286-332`)
- Security/auth fix → STRICT
- Read-only explanation → EXEMPT
- Typo fix → LIGHT
- Feature addition → STANDARD
- `/sc:task "update config file" --compliance strict` → user-forced STRICT

## 2. Protocol / Skill

### Skill paths (live source)
- `src/superclaude/skills/sc-task-protocol/SKILL.md`
- `src/superclaude/skills/sc-task-protocol/__init__.py`
- Dev copy: `.claude/skills/sc-task-protocol/SKILL.md`
- **No** `refs/`, `rules/`, `templates/`, or `scripts/` subdirectories.

Related: `sc-tasklist-protocol/rules/tier-classification.md` (read-only reference extracted from SKILL.md Section 5.3).

### Protocol entry rule (`SKILL.md:7-9`)
> "Classification has already been performed by the /sc:task command before this skill was invoked. The classification header has already been emitted. Do NOT emit it again. This skill handles execution only for STANDARD and STRICT tier tasks."

### Classification header (`task.md:58-67`, `.claude/commands/sc/task.md:58-67`)
Still uses `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel — carry-over naming artifact.

### Tier logic — live command (`task.md:50-91`)
Pre-tool TEXT-ONLY classification rule. Priority order: STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4). Full verbatim rules captured in context-task-current-state.md §2. Low-confidence: <0.70 prompt user with override hint.

### Tier logic — tasklist rules reference (`sc-tasklist-protocol/rules/tier-classification.md:1-81`)
- Read-only mirror; skill uses inline copy.
- Same priority order.
- **More extensive STRICT keywords**: includes `password, credential, secret, jwt, transaction, query` — NOT in live `/sc:task` command. Drift risk.
- Verification routing (`:74-81`): STRICT sub-agent quality-engineer 3-5K/60s; STANDARD direct 300-500/30s; LIGHT quick ~100/10s; EXEMPT skip 0/0s.

### Execution routing (`task.md:93-100`)
- EXEMPT: execute immediately, no Skill.
- LIGHT: execute directly, no Skill.
- STANDARD/STRICT: invoke `Skill sc:task-protocol`.

### Execution per tier (`SKILL.md:76-108`)
STRICT (11 steps): Serena activate → git clean → codebase-retrieval → memories → affected files/tests → make changes → find importers → update files → quality-engineer agent → pytest -v → adversarial Qs.

STANDARD (5): codebase-retrieval → find_referencing_symbols/grep downstream → changes → run tests or document → verify basic.

LIGHT (4): scope check → changes → sanity check → proceed.

EXEMPT (2): execute → no verification.

### Decision rules / gates (`SKILL.md:110-264`)
- Critical path override: `auth/, security/, crypto/, models/, migrations/` → always CRITICAL verification.
- Trivial path override: `*.md, docs/, *test*.py` → may skip verification.
- MCP circuit breaker: STRICT requires Sequential + Serena (no fallback); STANDARD Sequential + Context7 (fallback OK); LIGHT/EXEMPT none. STRICT MCP unavailable → BLOCK.
- TFEP prohibitions: no code fixes on test failure without TFEP; no test-expectation modification without adversarial validation; ad-hoc patches PROHIBITED.
- Must-escalate: any pre-existing test fails; ≥3 new tests fail; runtime exceptions.
- Forensic invocation (`SKILL.md:191-197`): `/sc:forensic --tier {tier} --intent triage --caller task-unified ...` — naming artifact.

## 3. MCP integration

Command frontmatter (`task.md:7`): sequential, context7, serena, playwright, magic, morphllm.

Tier required servers (`SKILL.md:253-259`):
- STRICT: Sequential, Serena.
- STANDARD: Sequential, Context7.
- LIGHT: none.
- EXEMPT: none.

Live skill execution references:
- `mcp__serena__activate_project`
- `codebase-retrieval`
- `list_memories` / `read_memory`
- `find_referencing_symbols`

Tool coordination phases (`SKILL.md:265-285`):
- Planning: TodoWrite, codebase-retrieval, memories.
- Execution: Edit/MultiEdit/Write, Grep/Glob, find_referencing_symbols.
- Verification: Task quality-engineer, Bash, `think_about_task_adherence`.
- Completion: write_memory, `think_about_whether_you_are_done`.

## 4. Eval / release history

### Confirmed v3.7 rename completed
- No live `commands/task-unified.md` in `src/` or `.claude/`.
- No live `skills/sc-task-unified-protocol/`.
- CLI integrations call `/sc:task`:
  - `cli/sprint/process.py:170` — `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic`
  - `cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116`

### Past release directories touching task-unified
- `.dev/releases/complete/v.2.0-task-unified/`
- `.dev/releases/complete/v.2.0-task-unified/v2.1-task-unified-accountability/`
- `.dev/releases/complete/v3.7-task-unified-v2/`
- `.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/` (this release)
- `.dev/releases/backlog/v3.xxRigorFlowMerger/`
- `.dev/releases/backlog/v4.xx-SkillRefactor/refactoring-spec-task-unified-protocol.md`
- `.dev/releases/complete/cross-framework-deep-analysis/artifacts/` (3 task-unified analysis docs)

### v2.0 original unified task command spec
- Intent (`UNIFIED-TASK-COMMAND-SPEC.md:32-37`): merge orchestration of `sc:task` with MCP compliance enforcement of `sc:task-mcp`.
- Problem (`:38-45`): dual-command system caused confusion, naming collision, capability gaps, decision paralysis.
- Interface (`:46-58`): `/sc:task [operation] --strategy [...] --compliance [...]`.

### Prior merger / collision analysis
- `task-vs-task-unified-risk-assessment.md:9-14` — both `task.md` and `task-unified.md` declared `name: task`. HIGH risk.
- `task-vs-task-unified-risk-assessment.md:132-169` — recommended: delete `task.md`; rename `task-unified.md` to `task.md`; keep `name: task`.
- `task-vs-task-unified-crossrefs.md:149-161` — root cause: project mid-migration from two-command system.
- `task-vs-task-unified-adversarial-challenge.md:10-20` — adversarial: risk overstated (filename-based routing), but migration intent confirmed.

### v3.7 eval / handover
Three strands: Checkpoint Enforcement, Sprint TUI v2, Naming Consolidation (`HANDOVER.md:16-60`).

Validated naming (`HANDOVER.md:64-72`):
- `/sc:task-unified` removed from source — 0 references in `src/` and `.claude/`.
- `task.md`, `task-mcp.md`, `tasklist.md` present; `task-unified.md` absent.
- Skill renamed to `sc-task-protocol/`.

Test/eval summary (`HANDOVER.md:113-121`):
- `tests/sprint/` full run: 921 passed, 57 failed (matches baseline).
- TUI Waves 1-2 + tmux + summarizer + retrospective: 125/125 pass.
- `test_process.py::TestClaudeProcess`: 16/16 including `test_build_prompt_contains_task_command`.

Not fully validated (`HANDOVER.md:125-163`): live sprint execution requires real claude CLI or stream-json stub.

Known anomalies (`HANDOVER.md:182-305`): missing `--checkpoint-gate-mode` flag; `_resolve_release_dir` anchor-file dependency; `--dry-run` doesn't exercise TUI; ruff baseline mismatch; `verify-checkpoints --json` affected by UV warnings; Wave-4 checkpoint heading parser bug (fixed).

### Current v3.75 backlog merger inputs
- `strategy-ic-task-unified.md` — tier system rationale, classification weaknesses.
- `improve-task-unified-tier.md` — 4 improvement items (TU-001..TU-004).
- `comparison-task-unified-tier.md` — IC vs LW comparison, verdict IC STRONGER, adoptable LW patterns.

Strategy weakness (`strategy-ic-task-unified.md:89-103`):
> "The classification algorithm is documented in multiple places... Changes to keyword tables or booster weights must be propagated to all copies, creating synchronization risk between source files and dev copies."
> "The keyword-scoring approach cannot handle context-dependent semantics."

Improvement plan (TU-001..TU-004):
- TU-001: CRITICAL FAIL conditions (Sequential/Serena unavailable, output absent, classification header absent → unconditional FAIL).
- TU-002: output-type-specific gates (code/analysis/documentation/opinion).
- TU-003: six universal quality principles (Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy).
- TU-004: confidence <0.70 explicit BLOCKED state (not soft degradation).

Comparison verdict (`comparison-task-unified-tier.md:75-89`):
> "IC STRONGER. Conditions where LW patterns should be adopted into IC: output-type-specific gate tables, universal quality principles, anti-sycophancy, mandatory task completion checklist."

## 5. Prior-art constraints from v3.7-task-unified-v2

### What v3.7 tried
Three domains unified into one release (`v3.7-task-unified-v2-release-spec.md:37-48`):
1. Checkpoint Enforcement
2. Sprint TUI v2
3. Naming Consolidation

Naming problem (`:123-144`, `:248-272`): three-layer collision `/sc:task`, `task-unified.md`, `sc-task-unified-protocol`.

Migration recommended (`:261-286`): rename `task-unified.md` → `task.md`; delete deprecated legacy; rename `sc-task-unified-protocol/` → `sc-task-protocol/`; update `process.py`, cleanup_audit prompts, tasklist references; sync dev copies.

Naming consolidation task list (N1-N12, `:869-890`): delete legacy → rename command → rename skill → update frontmatter → Sprint CLI prompt → cleanup_audit → tasklist → command cross-refs → other protocol refs → core docs → sync → confirm task-mcp status.

### What worked
- `HANDOVER.md:64-72` — `/sc:task-unified` removed; 0 source references.
- Current repo state matches this except intentional carry-over strings:
  - `SC:TASK-UNIFIED:CLASSIFICATION` header sentinel.
  - `--caller task-unified` in TFEP forensic invocation.

### What failed / remained partial
- Live sprint execution not validated (no real claude CLI or stream-json stub at that time).
- Full 2N parallel validation agents abbreviated to downstream-verified equivalent (HANDOVER `:83-85`).
- Follow-up items (`:375-391`): `--checkpoint-gate-mode` flag; `_resolve_release_dir` grandparent walk; live run; ruff fix; optional 10-stage agents.

### Carry-over decisions / constraints
- **Release split decision**: SPLIT release; "Fix the Pipeline" (R1, naming + checkpoint) vs "Show the Pipeline" (R2, TUI). R2 depended on R1.
- **R1 handoff criteria** (`boundary-rationale.md:55-65`): `/sc:task` resolves correctly; zero remaining `sc:task-unified` references in `src/superclaude/` except historical artifacts.
- **CRITICAL prior-art constraint for any new merger**: canonical surface must remain `/sc:task`; reintroducing `/sc:task-unified` as a separate live command would regress the v2/v3.7 collision fix UNLESS explicitly designed as an alias or historical compatibility layer.

## 6. Known issues / gaps

1. **No live `/sc:task-unified` command exists.** Any spec saying "merge /sc:task-unified into /sc:task" treats `/sc:task-unified` as historical/retired name; this release should not regress canonicalization.

2. **Naming artifacts remain**: `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` (task.md:58-67) and `--caller task-unified` (SKILL.md:196). Possibly telemetry compatibility; not explained in source.

3. **Flag documentation incomplete**: command says "See protocol skill for full flag reference"; skill only shows subset; fuller descriptions only in historical v2.0 spec and `core/COMMANDS.md`.

4. **Classification logic duplicated and drifting**: command, skill, tasklist rules, and v3.75 strategy docs all contain tier logic. Live `/sc:task` STRICT keywords narrower than `sc-tasklist-protocol/rules/tier-classification.md` (missing password, credential, secret, jwt, transaction, query).

5. **Low-confidence behavior underspecified operationally**: live command says "prompt"; v3.75 TU-004 says it should be explicit BLOCKED with tier/competing tier/keyword split.

6. **STRICT critical failure conditions not formalized**: live skill has STRICT MCP unavailability circuit breaker but no full CRITICAL condition model.

7. **Output-type-specific gates pending** (TU-002): current routing is tier-only + path overrides; no code/analysis/documentation/opinion axis.

8. **v3.7 operational gaps remain** (HANDOVER `:125-178, :182-305, :375-391`): `--checkpoint-gate-mode`, `_resolve_release_dir`, `--dry-run` TUI gap, live-run validation, full 10-stage validation.

9. **Sprint prompt already canonical `/sc:task`** (`cli/sprint/process.py:170` and 5 cleanup_audit prompts). Any spec must NOT assume runtime integration points call `/sc:task-unified` — they've already been migrated.
