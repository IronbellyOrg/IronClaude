# FINAL-REPORT-draft-A — v3.75 RigorflowMerger / task-unified-v3

> Synthesizer S-A draft. Optimized for **completeness and traceability**. Every concrete claim cites a source extract or live file:line. Inferential statements are marked `[inference]`. The companion draft (S-B) optimizes for decision-readiness; this draft does not.

---

## 1. Scope

### 1.1 What this release does

This release consolidates the historical strengths of the retired `/sc:task-unified` command — tier classification rigor, CRITICAL FAIL semantics, MCP compliance gating, output-type discrimination, universal quality principles, anti-sycophancy, and the deterministic low-confidence block state — into the **canonical `/sc:task` command** without reintroducing `/sc:task-unified` as a live command name.

The substantive merge targets, all evidenced in the Wave-1 extracts, are:

- **TU-001** Programmatic CRITICAL FAIL conditions for STRICT-tier tasks (Sequential/Serena MCP unavailable; output absent after max turns; classification header absent). Source: R4 `improve-task-unified-tier.md:26-31` (extracts file `wave1-extracts.md` R4 Recommendations).
- **TU-002** Output-type-specific gate tables (`code | analysis | documentation | opinion`) layered onto the existing tier axis. Source: R4 `improve-task-unified-tier.md:48-50`; R2 `comparison-task-unified-tier.md:81-85`.
- **TU-003** Six universal quality principles as an NFR baseline that the verification agents enforce: Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy. Source: R4 `improve-task-unified-tier.md:70`; R2 `comparison-task-unified-tier.md:89`.
- **TU-004** Deterministic BLOCKED state at confidence < 0.70 (not soft degradation), with blocking message including computed tier, competing tier, and split keywords. Source: R4 `improve-task-unified-tier.md:89-93`.
- **SE-001..SE-005** Sprint-executor improvements that consume the same tier vocabulary: fail-closed gate evaluation (R3 `improve-sprint-executor.md:26-27`), per-task UID tracking (`:47`), sub-phase resume (`:48`), ExecutionMode enum (`:68`), auto-diagnostic threshold (`:88`), three-tier gate severity (`:109`).

Per R8 §1 (`context-task-unified-current-state.md:9-16`), `/sc:task-unified` has already been retired by the v3.7 naming consolidation. Therefore "merging the best qualities" here means **inheriting and rigorizing**, not "creating two commands and then merging them."

### 1.2 What this release does NOT do (explicit non-goals)

- **NG-1.** Reintroduce `/sc:task-unified` as a live command. Anti-regression of v3.7 N1-N12. Source: R8 §5 `context-task-unified-current-state.md:217-219`; `v3.7-task-unified-v2/HANDOVER.md:51-60` cited at R8 §1.
- **NG-2.** Resurrect `task-unified.md` or `sc-task-unified-protocol/` directories. Source: R8 §4 `context-task-unified-current-state.md:129-135` confirms 0 live references; `HANDOVER.md:64-72` cited at R8 §4.
- **NG-3.** Replace IC's automatic keyword-based tier classification with LW's manual gate menu. Source: R2 extracts `wave1-extracts.md` (R2 Recommendations, "Do NOT adopt: LW's manual gate application without automation").
- **NG-4.** Adopt LW's bash-implementation, multi-backup, or subprocess-from-bash mass. Source: R1 extracts (R1 Recommendations, "Do NOT adopt: the bash implementation, the multiple-backup versioning strategy, the Python subprocess call from bash").
- **NG-5.** Remove or rename the lingering `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header sentinel and `--caller task-unified` forensic string without an explicit telemetry-compat plan. Source: R7 §5 item 1 (`context-task-current-state.md:242-245`); R8 §6 item 2 (`context-task-unified-current-state.md:225`). Both notes flag these as possibly intentional telemetry compat — the decision is open (see §8 below).
- **NG-6.** Build TypeScript plugin-system features (v5.0 scope). `[inference]` from project CLAUDE.md "TypeScript plugin system planned for v5.0".

---

## 2. Source index

| File (absolute) | Role | Key sections / line ranges |
|---|---|---|
| `/config/workspace/IronClaude/.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/wave1-extracts.md` | Verbatim R1-R6 extracts from the six backlog comparison/improvement/strategy docs | R1: L7-39 (sprint-executor comparison); R2: L43-69 (task-unified tier comparison); R3: L72-101 (sprint-executor improvement); R4: L104-130 (task-unified tier improvement); R5: L133-164 (sprint-executor strategy); R6: L167-206 (task-unified strategy) |
| `/config/workspace/IronClaude/.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/context-task-current-state.md` | R7 — Current `/sc:task` snapshot. Canonical state | §1 Surface (L5-83), §2 Protocol/Skill (L85-178), §3 MCP (L180-209), §4 Eval history (L211-238), §5 Known issues (L240-263) |
| `/config/workspace/IronClaude/.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/context-task-unified-current-state.md` | R8 — Current `/sc:task-unified` snapshot (now retired, historical) | §1 Surface (L5-56), §2 Protocol/Skill (L58-103), §3 MCP (L105-125), §4 Eval history (L127-189), §5 Prior-art constraints from v3.7 (L191-219), §6 Known issues (L221-239) |
| `src/superclaude/commands/task.md` (referenced) | Live command file (source of truth) | Metadata `:1-9`; description `:14-27`; usage `:40-42`; flags `:44-48`; classification header `:50-67`; tier logic `:69-91`; execution routing `:93-100`; examples `:106-148`. Cited via R7 §1-§2 |
| `.claude/commands/sc/task.md` (referenced) | Dev copy of command file | Mirrors `src/superclaude/commands/task.md`. R8 §1 confirms parity for inspected surface |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` (referenced) | Live protocol skill | Metadata `:1-5`; entry rule `:7-9`; execution per tier `:76-123`; TFEP gates `:125-244`; MCP requirements `:253-263`; tool coordination `:265-284`; broken config refs `:359-365`. Cited via R7 §2-§3 |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (referenced) | Parallel tier-classification logic for generated tasklists | `:505-575` extended keyword tables and weights. Cited via R7 §2 |
| `src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md` (referenced) | Read-only mirror of tier-classification logic | `:1-81` extracted classification, including additional STRICT keywords (`password, credential, secret, jwt, transaction, query`) not in live `/sc:task`. Cited via R8 §2 |
| `src/superclaude/core/ORCHESTRATOR.md` (referenced) | Five-step classification decision tree | `:151-213`. Cited via R7 §2 |
| `src/superclaude/core/COMMANDS.md` (referenced) | Full flag inventory | `:86-119`. Cited via R7 §1 |
| `src/superclaude/cli/sprint/process.py` (referenced) | Sprint CLI prompt builder | `:123-183` (builder); `:170` (canonical `/sc:task` prompt). Cited via R7 §3 and R8 §4 |
| `src/superclaude/cli/cleanup_audit/prompts.py` (referenced) | Five `/sc:task` prompt builders | `:26, :47, :69, :92, :116`. Cited via R7 §3 and R8 §4 |
| `.dev/releases/complete/v3.7-task-unified-v2/HANDOVER.md` (referenced) | v3.7 release handover — canonicalization | `:16-60` three strands; `:51-60` rename evidence; `:64-72` validation; `:113-121` test summary; `:125-163` not-validated; `:182-305` anomalies; `:253-304` Wave-4 parser fix; `:375-391` open follow-ups. Cited via R7 §4 and R8 §4-§5 |
| `.dev/releases/complete/v3.7-task-unified-v2/TEST-SPEC.md` (referenced) | v3.7 test spec — enforces no `/sc:task-unified` strings | `:34-80`. Cited via R7 §4 |
| `.dev/releases/complete/v3.7-task-unified-v2/release-split/release-split-report.md` (referenced) | v3.7 release split into R1+R2 | Cited via R7 §4 |
| `.dev/releases/complete/v3.7-task-unified-v2/release-split/boundary-rationale.md` (referenced) | R1 handoff criteria | `:55-65`. Cited via R8 §5 |
| `.dev/releases/complete/v.2.0-task-unified/UNIFIED-TASK-COMMAND-SPEC.md` (referenced) | Original v2.0 merger spec | `:32-37` intent; `:38-45` problem; `:46-58` interface; `:134-172` flag inventory. Cited via R7 §4 and R8 §1 |
| `.dev/releases/complete/v.2.0-task-unified/task-vs-task-unified-*.md` (referenced) | v2.0 collision analysis bundle | risk-assessment `:9-13, :132-169`; crossrefs `:19-23, :149-161`; adversarial-challenge `:10-20`; trigger-risks `:9-12`. Cited via R7 §4 and R8 §4 |
| `.dev/releases/complete/v3.7-task-unified-v2/artifacts/troubleshoot-missing-p03-checkpoint.md` (referenced) | Checkpoint RCA | `:10-18, :21-75, :111-119`. Cited via R7 §4 |

---

## 3. `/sc:task-unified` inventory (historical strengths to preserve)

This section enumerates the qualities of the (now retired) `/sc:task-unified` lineage that are candidates for consolidation into `/sc:task`. All items are sourced from R6 (strategy), R4 (improvements), R2 (comparison), and R8 (history).

### 3.1 Flags / surface from the v2.0 lineage

Per v2.0 spec (`UNIFIED-TASK-COMMAND-SPEC.md:134-172`, cited at R8 §1):

- **Strategy:** `systematic, agile, enterprise, auto` (4 values).
- **Compliance:** `strict, standard, light, exempt, auto` (5 values).
- **Execution control:** `--skip-compliance, --force-strict, --parallel, --delegate, --reason`.
- **Verification:** `--verify critical, --verify standard, --verify skip, --verify auto`.

Live tier flag values from R6 `wave1-extracts.md` (R6 Flag mentions):
- `--compliance flag: user can force any tier regardless of auto-classification` (L82).
- `--force-strict override: escalate to STRICT without providing rationale` (L83).
- `--skip-compliance escape hatch: bypass all compliance` (L84).
- `--parallel / --delegate: enable parallel sub-agent execution for large STRICT tasks` (L85).
- `Confidence threshold (0.70): not currently user-configurable; hardcoded` (L87).

### 3.2 Tier-classification logic worth preserving

R6 Capability comparisons (`strategy-ic-task-unified.md`):
- `Score all keywords by tier weight (STRICT +0.4, EXEMPT +0.4, LIGHT +0.3, STANDARD +0.2)` (L34).
- `Apply context boosters (>2 files +0.3 STRICT; security paths +0.4 STRICT; docs paths +0.5 EXEMPT)` (L35).
- `apply with +0.15 boost` for compound phrases (L33).
- `If confidence < 0.70, prompt user for confirmation` (L37).
- `Resolve conflicts: priority STRICT > EXEMPT > LIGHT > STANDARD` (L36).
- `STRICT → quality-engineer sub-agent (3–5K token budget, 60s timeout)` (L54).
- `STANDARD → direct test execution (300–500 tokens, 30s timeout)` (L55).
- `LIGHT → quick sanity check (~100 tokens, 10s)` (L56).
- `EXEMPT → no verification (0 tokens, 0s)` (L57).
- `MCP Requirements: Required: Sequential, Serena; Fallback Allowed: No` (L66).
- `Paths matching auth/, security/, crypto/, models/, migrations/ always trigger CRITICAL verification regardless of compliance tier` (L59 / R6 L20 in extracts file).

R2 (`comparison-task-unified-tier.md`) verdict: "IC STRONGER" (L8, L77).

R2 Scoring claims:
- `Confidence threshold: <70% triggers user confirmation before execution begins` (L26).
- `Context boosters: >2 files +0.3 STRICT; security paths +0.4 STRICT` (L46).
- `STRICT → quality-engineer (3-5K tokens, 60s)` (L44).
- `Three-tier severity system: Sev 1 (block), Sev 2 (cycle), Sev 3 (when able)` (L35).

R2 Capability quote (L79):
> "Automatic classification with confidence scoring eliminates a category of user error that LW's manual gate application cannot prevent. The critical path override (filesystem-path-based safety backstop) provides semantic safety beyond keyword matching. The STRICT MCP requirement block (rather than degraded execution) is a safety decision LW has no equivalent for."

### 3.3 Protocol elements worth preserving

From R6 Recommendations (L13-46):
- `automatic tier classification with transparent confidence scoring` (L13).
- `Merging them into a single /sc:task with orthogonal --compliance and --strategy flags eliminates the decision by automating it` (L15).
- `when uncertain, escalate` (L17). ("Better false positives than false negatives" — also at live `task.md:14-27`, cited R7 §1.)
- STRICT protocol steps (L46): activate project (Serena) → verify git state → load codebase context (Auggie) → make changes → identify all affected files → spawn quality-engineer sub-agent for verification → run comprehensive tests.

### 3.4 Best-of-task-unified candidates for elevation

From R4 (`improve-task-unified-tier.md`) Recommendations:
- **CriticalFailCondition dataclass** with `condition_type`, `description`, `always_blocks: bool = True` (L26).
- **Three CRITICAL FAIL conditions for STRICT:** (1) Sequential or Serena MCP unavailable → unconditional FAIL; (2) output file absent after max turns → unconditional FAIL; (3) classification header absent in STRICT-tier task output → unconditional FAIL (L28).
- **output_type column:** `code (compile/test required), analysis (evidence citation required, no lint), documentation (structure check only, no code testing), opinion (CEV structure required, no automated verification)` (L48).
- **output-type detection rules:** all `*.md` → documentation; comparison/analysis report → analysis; code changes → code (L50).
- **Six universal quality principles** as NFR (L70): Verifiability (file:line evidence), Completeness (acceptance criteria), Correctness (matches spec intent), Consistency (no contradictions), Clarity (unambiguous + actionable), Anti-Sycophancy (independent of implementer's stated confidence).
- **BLOCKED state at confidence < 0.70** (L89): "the task classification is BLOCKED and requires user confirmation. The blocking message must include: the computed tier, the competing tier (highest alternative), and the specific keywords causing the split."
- **Determinism mandate** (L93): "confidence <0.70 must produce a deterministic outcome (BLOCKED, awaiting user confirmation) not a soft degradation to the computed tier."

From R2 Recommendations (L89), the LW-side patterns worth adopting:
- Six universal quality principles as the IC verification agent's check framework.
- Output-type-specific gate application (code gates for code tasks, evidence gates for analysis tasks).
- Three-tier severity model (Sev 1 blocks immediately, Sev 2 fixes in cycle, Sev 3 when able).

---

## 4. `/sc:task` inventory (current canonical surface)

### 4.1 Command surface (R7 §1, cited from `src/superclaude/commands/task.md`)

- **Path:** source `src/superclaude/commands/task.md`; dev copy `.claude/commands/sc/task.md`; surfaces match (R7 §1 L10).
- **Metadata (`task.md:1-9`):** `name: task`; description `"Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation"`; `category: special`; `complexity: advanced`; `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`; `mcp-servers: [sequential, context7, serena, playwright, magic, morphllm]`; `personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]`; `version: "2.0.0"`.
- **Philosophy (`task.md:14-27`):** orthogonal `--strategy` × `--compliance`; "Better false positives than false negatives."
- **Usage (`task.md:40-42`):** `/sc:task [operation] [target] [flags]`.

### 4.2 Flags (full inventory)

In-file (`task.md:44-48`, R7 §1):
- `--strategy, --compliance, --verify, --skip-compliance, --force-strict, --parallel, --delegate, --no-escalation` (8 flags).
- Only `--no-escalation` has an in-file table description (default `false`, R7 §1 L39-40, quoted from `task.md:46-48`):
  > "Bypass TFEP (Test Failure Escalation Protocol) triggers. When set, agents may fix test failures directly without structured forensic analysis. WARNING: Using --no-escalation voids TFEP protection against ad-hoc fixes."

Expanded in `core/COMMANDS.md:86-119` (R7 §1 L42-67):
- **Strategy:** systematic, agile, enterprise, auto.
- **Compliance:** strict, standard, light, exempt, auto.
- **Verification:** critical, standard, skip, auto.
- **Execution control:** `--skip-compliance, --force-strict, --parallel, --delegate, --reason "..."` (required justification for tier override).

Global flags reachable from help.md `:89-126` (R7 §1 L69-70):
`--delegate [auto|files|folders], --concurrency [n], --loop, --iterations [n], --validate, --safe-mode, --token-efficient, --scope [file|module|project|system], --focus [performance|security|quality|architecture|accessibility|testing]`.

### 4.3 Examples (R7 §1 L72-83, `task.md:106-148`, `SKILL.md:288-331`)

Command file (`task.md:106-148`):
1. `/sc:task "fix security vulnerability in auth module"` → STRICT, conf 0.95.
2. `/sc:task "explain how the routing middleware works"` → EXEMPT, conf 0.92.
3. `/sc:task "fix typo in error message"` → LIGHT, conf 0.95.
4. `/sc:task "add pagination to user list endpoint"` → STANDARD, conf 0.85.

Skill (`SKILL.md:288-331`):
- `/sc:task "implement user authentication with JWT"` → STRICT.
- `/sc:task "add pagination to user list"` → STANDARD.
- `/sc:task "fix typo in README"` → LIGHT.
- `/sc:task "explain how the auth flow works"` → EXEMPT.
- `/sc:task "update config file" --compliance strict` → user-forced STRICT.

### 4.4 Protocol / skill

Skill `sc-task-protocol` (R7 §2):
- Source: `src/superclaude/skills/sc-task-protocol/SKILL.md`.
- Init: `src/superclaude/skills/sc-task-protocol/__init__.py`.
- Dev copy: `.claude/skills/sc-task-protocol/SKILL.md`.
- Metadata (`SKILL.md:1-5`): `name: sc:task-protocol`; allowed tools `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task`.
- **Sub-files: only `SKILL.md` and `__init__.py`. No `refs/`, `rules/`, `templates/`, `scripts/`, `config/`** (R7 §2 L93-94).

Protocol entry rule (`SKILL.md:7-9`, R7 §2 L98-99):
> "Classification has already been performed by the `/sc:task` command before this skill was invoked. The classification header has already been emitted. Do NOT emit it again. This skill handles execution only for STANDARD and STRICT tier tasks."

### 4.5 Classification header gate (`task.md:50-67`, R7 §2 L101-112)

Exact required first output:
```
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
CONFIDENCE: [0.00-1.00]
KEYWORDS: [matched keywords or "none"]
OVERRIDE: [true|false]
RATIONALE: [one-line reason]
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```
Rules: no tool invocation during classification; exact format; only STRICT/STANDARD/LIGHT/EXEMPT valid; header must be first output. The sentinel still contains `SC:TASK-UNIFIED:`, a naming carry-over.

### 4.6 Tier logic — command file (`task.md:69-91`, R7 §2 L114-121)

Priority order (first match wins; `--compliance` override checked first):

1. **STRICT (P1, safety-critical)** — keywords: `security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth`. Boosters: >2 files (+0.3), security paths `auth/, security/, crypto/` (+0.4). Compound: `"fix security", "add authentication", "update database", "change api"`. Notes: "quick security" → STRICT; "minor auth change" → STRICT.
2. **EXEMPT (P2, non-code)** — keywords: `explain, search, commit, push, plan, discuss, brainstorm, what, how, why`. Boosters: is_read_only +0.4, is_git_operation +0.5, all doc files +0.5. Patterns: starts with what/how/why/explain, docs-only paths.
3. **LIGHT (P3, trivial)** — keywords: `typo, comment, whitespace, lint, docstring, formatting, spacing, minor`. Boosters: single file +0.1, ≤50 lines. Compounds: `"quick fix", "minor change", "fix typo", "refactor comment"`.
4. **STANDARD (P4, default)** — keywords: `implement, add, create, update, fix, build, modify, change`. Default tier.

Low-confidence rule: confidence <0.70 → prompt user with `--compliance [tier]` override hint.

### 4.7 Tier logic — orchestrator (`core/ORCHESTRATOR.md:151-213`, R7 §2 L123-138)

Five-step decision tree:
1. **step_1_override:** `user_override_tier != null` → use override @ 100%.
2. **step_2_compound:** compound phrase detected → use compound tier @ 90%.
3. **step_3_keywords:** sum `keyword_matches * weight` + context boosts.
4. **step_4_resolve:** scores within 0.1 → escalate to higher priority. Priority STRICT > EXEMPT > LIGHT > STANDARD.
5. **step_5_confidence:** <0.7 → prompt user.

Context boosters (orchestrator):
- `estimated_files > 2` → STRICT +0.3.
- `estimated_files == 1` → LIGHT +0.1.
- Security path → STRICT +0.4.
- All test files → STANDARD +0.2.
- All doc files → EXEMPT +0.5.
- Read-only → EXEMPT +0.4.
- Git operation → EXEMPT +0.5.

### 4.8 Tier logic — tasklist protocol (`sc-tasklist-protocol/SKILL.md:505-575`, R7 §2 L140-141)

A parallel deterministic classification for generated tasklists with **extended keyword tables** beyond live `/sc:task`:
- Adds LIGHT compounds: `small update, update comment, fix spacing, fix lint, rename variable`.
- Adds STANDARD: `remove, delete, deprecate` (cited at R7 §5 item 4).
- Adds STRICT (from `sc-tasklist-protocol/rules/tier-classification.md`, R8 §2 L77-81): `password, credential, secret, jwt, transaction, query` — NOT present in live `/sc:task`. Drift risk.
- Weights: STRICT/EXEMPT +0.4 each keyword; LIGHT +0.3; STANDARD +0.2. Compound match: +0.15. Path boosters: `auth|security|crypto` +0.4 STRICT, `docs|*.md` +0.5 EXEMPT, `tests/` +0.2 STANDARD. Base confidence `max(tier_scores)` capped 0.95; –15% if top-two within 0.1; +15% if compound; –30% if no keywords; <0.7 requires confirmation.

### 4.9 Execution routing (`task.md:93-100`, R7 §2 L143-146)

- EXEMPT: execute immediately; no Skill.
- LIGHT: execute directly; no Skill.
- STANDARD / STRICT: invoke `Skill sc:task-protocol`.

### 4.10 Protocol execution per tier (`SKILL.md:76-123`, R7 §2 L148-163)

- **STRICT (11 steps):** activate Serena project → verify clean git → load codebase context (Auggie) → check memories → identify affected files & tests → make changes with checklist → identify all importers → update affected files → spawn quality-engineer → `pytest [path] -v` → answer adversarial questions.
- **STANDARD (5 steps):** load context via codebase-retrieval → search downstream impacts (`find_referencing_symbols` or grep) → make changes → run affected tests or document manual verification → verify basic functionality.
- **LIGHT (4 steps):** quick scope check → make changes → quick sanity check → proceed with judgment.
- **EXEMPT (2 steps):** execute immediately → no verification overhead.

Verification routing table (`SKILL.md:110-123`):
- STRICT → quality-engineer sub-agent, 3-5K tokens, 60s.
- STANDARD → direct test execution, 300-500 tokens, 30s.
- LIGHT → skip.
- EXEMPT → skip.
- Critical path override (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) → always CRITICAL regardless of tier.
- Trivial path override (`*.md`, `docs/`, `*test*.py`) → may skip.

### 4.11 TFEP gates (`SKILL.md:125-244`, R7 §2 L165-178)

- Prohibitions: no ad-hoc fixes on test failures; no modifying test expectations without adversarial validation; no patches derived from test output.
- Permitted direct-fix exceptions: single ImportError/NameError in newly written test scaffolding affecting ≤2 tests; lint/formatting; deprecation warnings.
- Baseline: capture existing test files/functions before implementation; classify failures as pre-existing or new.
- Escalation triggers: any pre-existing test fails; ≥3 new tests fail simultaneously; runtime exceptions in implementation code; repeated failure; multi-file blast radius; low-confidence RCA; unresolved adversarial outcome; second failed retest; cross-domain regression.
- Forensic invocation (`SKILL.md:191-197`):
  - First trigger: `/sc:forensic --tier light --intent triage --caller task-unified ...`
  - Second trigger: `/sc:forensic --tier standard ...`
  - Third trigger: full stop.
  - `--caller task-unified` is a lingering naming artifact.

### 4.12 MCP integration (R7 §3, R8 §3)

- Servers referenced by command (`task.md:7`): `sequential, context7, serena, playwright, magic, morphllm`.
- Core docs (`core/COMMANDS.md:81-84`): Sequential for analysis; Serena for context; Context7 for patterns; Tools TodoWrite, Read, Grep, Glob, Edit, MultiEdit, Task, Bash.
- MCP requirements by tier (`SKILL.md:253-263`):
  - STRICT: Sequential + Serena (fallback NOT allowed).
  - STANDARD: Sequential + Context7 (fallback allowed).
  - LIGHT: none required.
  - EXEMPT: none.
  - Required servers unavailable for STRICT → block.
- Tool coordination (`SKILL.md:265-284`):
  - Planning: TodoWrite, codebase-retrieval, `list_memories`/`read_memory`.
  - Execution: Edit/MultiEdit/Write, Grep/Glob, `find_referencing_symbols`.
  - Verification: Task quality-engineer (STRICT), Bash (STANDARD), `think_about_task_adherence`.
  - Completion: `write_memory`, `think_about_whether_you_are_done`.
- Auggie / codebase retrieval: `codebase-retrieval` invoked at `SKILL.md:83, 94, 269`. Tool capability named rather than server `auggie` (R7 §3 L202-203).

### 4.13 Sprint CLI integration (R7 §3 L205-206, R8 §4 L132-133)

`src/superclaude/cli/sprint/process.py:123-183` builds:
```
/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic
```
plus tier instructions. Canonical `/sc:task` already; no `/sc:task-unified` in prompt.

### 4.14 Cleanup audit integration (R7 §3 L208-209, R8 §4 L134)

Five prompt builders at `src/superclaude/cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116` invoke `/sc:task`. Canonical surface.

---

## 5. Overlap matrix

Maps each task-unified concept (rows) to its current `/sc:task` state (columns). Status legend: **MERGED** = already present in live `/sc:task`; **PARTIAL** = some elements present, others missing; **NOT-YET** = absent from live `/sc:task`, candidate for this release.

| # | task-unified concept | Source extract | Current `/sc:task` state | Status | Gap / delta |
|---|---|---|---|---|---|
| O1 | Single canonical command name `/sc:task` | R8 §1 (`HANDOVER.md:51-60`); R8 §5 | `name: task` at `task.md:1` | **MERGED** | None — must NOT regress |
| O2 | Orthogonal `--strategy` × `--compliance` axes | R6 L15 | `task.md:14-27` confirms orthogonal axes | **MERGED** | — |
| O3 | Automatic tier classification with confidence scoring | R6 L13 | `task.md:69-91`, `ORCHESTRATOR.md:151-213` | **MERGED** | — |
| O4 | Keyword weights (STRICT/EXEMPT +0.4, LIGHT +0.3, STANDARD +0.2) | R6 L34 | Live command file does not state numeric weights inline; weights live in `sc-tasklist-protocol` and orchestrator. R7 §5 item 4 flags drift | **PARTIAL** | Weights duplicated in 3+ places, not unified |
| O5 | Compound match +0.15 confidence | R6 L33 | Tasklist protocol does it; command file mentions compounds without numeric weight | **PARTIAL** | Not formalized in `task.md` |
| O6 | Context boosters (>2 files +0.3 STRICT; security paths +0.4 STRICT; docs +0.5 EXEMPT) | R6 L35; R2 L46 | Yes in `task.md:69-91` and `ORCHESTRATOR.md:151-213` | **MERGED** | — |
| O7 | Priority order STRICT > EXEMPT > LIGHT > STANDARD | R6 L36 | `task.md:69-91`; ORCHESTRATOR step_4 | **MERGED** | — |
| O8 | Critical path override (`auth/, security/, crypto/, models/, migrations/`) | R6 L59 | `SKILL.md:110-123` (R7 §2 L162) | **MERGED** | — |
| O9 | Trivial path override (`*.md, docs/, *test*.py`) | R7 §2 L163 | `SKILL.md:110-123` | **MERGED** | — |
| O10 | STRICT MCP block (Sequential + Serena required, no fallback) | R2 L47; R6 L66 | `SKILL.md:253-263` (R7 §3 L189-194) | **MERGED** | — |
| O11 | Low-confidence prompt at <0.70 | R6 L37 | `task.md:91`: "prompt user" | **PARTIAL** | TU-004 wants deterministic BLOCKED state with tier/competing-tier/keywords. Current is "prompt", not "block". |
| O12 | Verification routing (STRICT 3-5K/60s; STANDARD 300-500/30s; LIGHT ~100/10s; EXEMPT 0/0s) | R6 L54-57; R2 L44 | `SKILL.md:110-123` | **MERGED** | — |
| O13 | Per-tier execution protocols (STRICT 11-step, STANDARD 5-step, LIGHT 4-step, EXEMPT 2-step) | R8 §2 L88-95 | `SKILL.md:76-108` | **MERGED** | — |
| O14 | CRITICAL FAIL conditions for STRICT (3 conditions) | R4 L26-31 | Only #1 (Sequential/Serena unavailable → block) present. #2 (output file absent after max turns) and #3 (classification header absent) not formalized. R7 §5 item 5 | **PARTIAL** | TU-001 candidate |
| O15 | `CriticalFailCondition` dataclass | R4 L26 | Absent from skill | **NOT-YET** | TU-001 candidate |
| O16 | Output-type axis: `code | analysis | documentation | opinion` | R4 L48-50; R2 L81 | Absent. Routing is tier-only + path overrides. R7 §5 item 6; R8 §6 item 7 | **NOT-YET** | TU-002 candidate |
| O17 | Output-type detection rules (all `*.md` → documentation; comparison report → analysis; code changes → code) | R4 L50 | Absent | **NOT-YET** | TU-002 candidate |
| O18 | Six universal quality principles (Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy) | R4 L70; R2 L89 | Absent as a named NFR section in skill | **NOT-YET** | TU-003 candidate |
| O19 | Anti-Sycophancy as a universal gate principle (not just tier-level) | R2 L83 | Absent | **NOT-YET** | TU-003 candidate |
| O20 | Mandatory task completion checklist (six conditions before "complete" status) | R2 L85 | TFEP exists; explicit 6-condition completion checklist not stated as such | **PARTIAL** | TU-003 candidate |
| O21 | Three-tier gate severity (Sev 1 block, Sev 2 cycle, Sev 3 advisory) | R2 L35; R3 L109 | Not formalized as a severity enum in skill | **NOT-YET** | SE-005 candidate (sprint side) |
| O22 | BLOCKED state at <0.70 with tier/competing-tier/keywords blocking message | R4 L89 | `task.md:91` is a soft prompt | **NOT-YET** | TU-004 candidate |
| O23 | Deterministic outcome guarantee (no soft degradation) | R4 L93 | Soft "prompt user" behavior | **NOT-YET** | TU-004 candidate |
| O24 | `--skip-compliance` escape hatch with <12% usage target | R2 L27; R6 L17, L84 | Flag exists at `task.md:44`; usage target not enforced/measured | **PARTIAL** | Telemetry gap (`[inference]` — no metering code cited) |
| O25 | `--force-strict` override (escalate to STRICT without rationale) | R6 L83 | Flag exists; `--reason "..."` documented at `COMMANDS.md:86-119` as required justification | **PARTIAL** | "without rationale" vs "with required justification" tension |
| O26 | `--parallel` / `--delegate` | R6 L85 | Flags exist | **MERGED** | — |
| O27 | `--no-escalation` (TFEP bypass) | R7 §1 L39-40, `task.md:46-48` | Present | **MERGED** | — |
| O28 | `--verify critical|standard|skip|auto` | R8 §1 L42 | Present in `COMMANDS.md:86-119` | **MERGED** | — |
| O29 | "Better false positives than false negatives" philosophy | R6 L17 | `task.md:14-27` | **MERGED** | — |
| O30 | Classification header sentinel `SC:TASK-UNIFIED:CLASSIFICATION` | R7 §5 item 1; R8 §6 item 2 | Present; lingering naming artifact | **MERGED (artifact)** | Open question — rename or keep for telemetry compat |
| O31 | `--caller task-unified` in forensic invocation | R7 §5 item 1; R8 §6 item 2 | Present at `SKILL.md:196` | **MERGED (artifact)** | Open question — rename or keep |
| O32 | Sprint-side fail-closed gate (empty output → FAIL, not PASS) | R3 L26-27 | Sprint executor side; not part of `/sc:task` proper. R5 L46 notes shadow-gates risk | **NOT-YET** | SE-001 candidate |
| O33 | Per-task UID tracking in phase task set | R1 L80-84; R3 L47, L100 | Sprint executor; phase-level only today | **NOT-YET** | SE-002 candidate |
| O34 | Sub-phase resume (`--start N` lands on first non-DONE task) | R3 L48, L54 | Today re-runs all tasks in the phase. R5 L77 | **NOT-YET** | SE-003 candidate |
| O35 | `ExecutionMode` enum (NORMAL, INCOMPLETE_RESUME, CORRECTION) | R1 L80-84; R3 L68 | Absent | **NOT-YET** | SE-004 candidate |
| O36 | `--auto-diagnostic-threshold N` CLI option | R3 L88-89 | Absent | **NOT-YET** | SE-006 candidate |
| O37 | `GateFailureSeverity` enum (SEV1_BLOCK, SEV2_CYCLE, SEV3_ADVISORY) | R3 L109 | Absent | **NOT-YET** | SE-005 candidate |
| O38 | Shadow-gates mode (`--shadow-gates`) | R5 L63 | Present in sprint executor (`[inference]` — extracted from R5; not directly cited in R7/R8) | **MERGED** | — |
| O39 | `--start / --end` phase range | R5 L62 | Present in sprint executor (R5) | **MERGED** | — |
| O40 | `--no-tmux` flag | R5 L67 | Present (R5) | **MERGED** | — |
| O41 | TurnLedger budget arithmetic (80% PASS reimbursement, min_alloc=5) | R1 L23; R5 L32 | Present (R1, R5) | **MERGED** | — |
| O42 | TurnLedger persistence to disk | R1 L66; R5 L75 | NOT persisted — known gap | **NOT-YET** | Out of scope for this release (sprint-runtime concern); listed for completeness |
| O43 | Phase discovery regex generality | R5 L81-85 | Hard-coded `PHASE_FILE_PATTERN` | **PARTIAL** | Out of scope unless wave-N tasklists collide |
| O44 | Skill sub-files (`refs/`, `rules/`, `templates/`, `scripts/`, `config/`) | R7 §2 L93-94 | None exist under `sc-task-protocol`; `SKILL.md:359-365` references nonexistent `config/tier-keywords.yaml` etc. R7 §5 item 2 | **NOT-YET** | TU-003 candidate (operationalizing skill assets) |
| O45 | STRICT keywords drift (live missing `password, credential, secret, jwt, transaction, query`) | R8 §2 L77-81; R7 §5 item 4 | Live keywords narrower than tasklist rules | **PARTIAL** | TU-001/TU-004 align candidate |
| O46 | Tasklist-protocol extended LIGHT compounds (`small update, update comment, fix spacing, fix lint, rename variable`) | R7 §5 item 4 | In tasklist protocol, not in live task command | **PARTIAL** | Drift |
| O47 | Tasklist-protocol STANDARD additions (`remove, delete, deprecate`) | R7 §5 item 4 | Same drift | **PARTIAL** | — |

Summary tallies (`[inference]` from row counts above):
- MERGED: 19 (including 2 artifacts).
- PARTIAL: 13.
- NOT-YET: 15 (TU-001..004 + SE-001..006 + a few skill-assets/anti-sycophancy items).

---

## 6. Best-of-breed candidates (sorted by value × tractability)

Each candidate notes: source extract, current state, proposed change, and a rough value/tractability rating. Values are `[inference]` unless an extract gives an explicit cost/benefit.

### 6.1 Task-side (TU-series)

#### TU-001: CRITICAL FAIL conditions for STRICT-tier tasks (HIGH value, HIGH tractability)

- **Source:** R4 `improve-task-unified-tier.md:26-31`; `wave1-extracts.md` R4 Recommendations.
- **Current state:** Only condition #1 (Sequential/Serena unavailable → block) lives in `SKILL.md:253-263`. Conditions #2 (output file absent) and #3 (classification header absent) are not enforced. R7 §5 item 5.
- **Proposed:** Add a `CriticalFailCondition` dataclass (`condition_type: str, description: str, always_blocks: bool = True`) and document the three STRICT conditions as `always_blocks=True`. Programmatically enforce, not just instruct (R4 L23 capability quote).
- **Risk per R4:** "Low. Additive to gate model" (L35).
- **Value:** Closes a documented safety gap. **Tractability:** Additive change, low blast radius.

#### TU-002: Output-type discrimination (HIGH value, MEDIUM tractability)

- **Source:** R4 L48-50; R2 L81-85.
- **Current state:** Tier routing applies uniformly; no `output_type` axis (R7 §5 item 6, R8 §6 item 7).
- **Proposed:** Add `output_type ∈ {code, analysis, documentation, opinion}` with detection rules (all `*.md` → documentation; comparison/analysis report → analysis; code changes → code). Per-output-type gate tables (code: compile/test; analysis: evidence citation, no lint; documentation: structure check only, no code testing; opinion: CEV structure required, no automated verification).
- **Risk per R4:** "Medium. Changes the routing logic for documentation and analysis tasks; requires re-evaluation of existing STRICT-tier doc tasks" (L57).
- **Value:** Eliminates over-verification of doc/analysis tasks (R2 L71 explicit critique). **Tractability:** Medium — requires both detection logic and per-type gate tables.

#### TU-003: Six universal quality principles + Anti-Sycophancy (MEDIUM value, HIGH tractability)

- **Source:** R4 L70; R2 L83, L89.
- **Current state:** Not formalized in skill as an NFR section. Anti-Sycophancy not surfaced as a universal gate.
- **Proposed:** Add "Quality Principles NFR" section to `sc-task-protocol/SKILL.md` listing six principles: Verifiability (file:line evidence), Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy. Use as the verification agent's check framework.
- **Risk per R4:** "Low. Agent instruction addition; no code changes" (L77).
- **Value:** Codifies what verification agents check. **Tractability:** High — instructional addition only.

#### TU-004: Deterministic BLOCKED state at <0.70 confidence (MEDIUM value, MEDIUM tractability)

- **Source:** R4 L89, L93.
- **Current state:** `task.md:91` says "prompt user" (soft) (R7 §2 L121).
- **Proposed:** Replace prompt with explicit BLOCKED state requiring user confirmation. Blocking message MUST include: computed tier, competing tier (highest alternative), specific keywords causing the split. Deterministic outcome, no soft degradation.
- **Risk:** R4 doesn't tag this item with an explicit risk; inferred LOW-MEDIUM `[inference]`. Behavioral change for borderline classifications.
- **Value:** Closes the "soft" gap identified in R7 §5 item 7 / R8 §6 item 5. **Tractability:** Medium — touches both command file and orchestrator.

#### TU-005: Resolve classification-logic duplication / drift (MEDIUM value, MEDIUM tractability)

- **Source:** R7 §5 item 4; R8 §2 L77-81; R6 L93 ("Changes to keyword tables or booster weights must be propagated to all copies, creating synchronization risk").
- **Current state:** Tier logic duplicated across `task.md:69-91`, `ORCHESTRATOR.md:151-213`, `sc-tasklist-protocol/SKILL.md:505-575`, `sc-tasklist-protocol/rules/tier-classification.md`. STRICT keywords drift (live missing `password, credential, secret, jwt, transaction, query`).
- **Proposed:** Establish single source of truth (e.g. `sc-task-protocol/config/tier-keywords.yaml`, referenced at `SKILL.md:359-365` but currently missing). Sync via `make sync-dev`. Reconcile keyword lists.
- **Value:** Eliminates drift risk. **Tractability:** Medium — requires creating the referenced config and updating consumers.

#### TU-006: Materialize the missing skill sub-files (LOW value, HIGH tractability)

- **Source:** R7 §5 item 2; `SKILL.md:359-365` references nonexistent files.
- **Current state:** `sc-task-protocol/` has only `SKILL.md` + `__init__.py`. No `refs/, rules/, templates/, scripts/, config/`.
- **Proposed:** Either create the referenced files or remove the references. Aligns with project convention "`src/superclaude/skills/<name>/` should contain `SKILL.md` + `refs/, rules/, templates/, scripts/`" (CLAUDE.md project structure).
- **Value:** Documentation hygiene. **Tractability:** High — file ops only.

### 6.2 Sprint-side (SE-series, in-scope per R1/R3/R5)

#### SE-001: Fail-closed gate evaluation (HIGH value, HIGH tractability)

- **Source:** R3 L26-27.
- **Current state:** R5 L46 notes shadow-gates trade safety for observability.
- **Proposed:** In `execute_phase_tasks()`, an "inconclusive completion" must classify as FAIL (not soft PASS). Confirm `gate_passed()` on empty output file returns `(False, 'empty output file')`.
- **Risk per R3:** "Low. Tightens existing behavior; edge case for empty output files" (L34).

#### SE-002: Per-task UID tracking (MEDIUM value, MEDIUM tractability)

- **Source:** R1 L80-84; R3 L47, L100.
- **Proposed:** Add `task_uid: str` field, generated at phase-load time as `f'{phase_id}-{task_index:04d}'`. Stable across session resets.
- **Risk per R3:** "Medium. Requires compatibility with existing result files; may need migration with graceful fallback" (L55).

#### SE-003: Sub-phase resume on `--start N` (HIGH value, MEDIUM tractability)

- **Source:** R3 L48, L54; R1 L66, L70; R5 L77.
- **Proposed:** When `--start N` is provided and the phase has a partial result file with per-task UIDs, re-enter at the first task with status != DONE (not at task 0).
- **Risk per R3:** "Medium. Changes prompt construction; may affect output format for resumed phases" (L75).

#### SE-004: `ExecutionMode` enum (MEDIUM value, HIGH tractability)

- **Source:** R1 L80-84 ("three-mode execution"); R3 L68.
- **Proposed:** Add `ExecutionMode` enum with values `NORMAL, INCOMPLETE_RESUME, CORRECTION`.
- **Risk:** `[inference]` Low — enum addition; consumers must select correct prompt template.

#### SE-005: `GateFailureSeverity` enum (MEDIUM value, HIGH tractability)

- **Source:** R3 L109; R2 L35.
- **Proposed:** Enum `SEV1_BLOCK, SEV2_CYCLE, SEV3_ADVISORY`. Default mapping: STRICT-tier gate failures → SEV1_BLOCK; STANDARD-tier with partial output → SEV2_CYCLE; LIGHT-tier → SEV3_ADVISORY.
- **Risk:** `[inference]` Low-Medium — assigns severity by tier, then downstream handlers act on severity.

#### SE-006: `--auto-diagnostic-threshold N` (LOW value, MEDIUM tractability)

- **Source:** R3 L88-89.
- **Proposed:** New CLI flag (default 3, range 1-10). After N consecutive gate failures, invoke `run_diagnostic_chain()`.
- **Risk per R3:** "Medium. Adds new invocation path for diagnostic chain; requires diagnostic chain robustness to sprint-context input" (L96).

### 6.3 Sorted summary (value × tractability)

Inferred ranking (`[inference]` — no explicit ROI tables in extracts):

1. **TU-001** (CRITICAL FAIL) — HIGH/HIGH.
2. **SE-001** (Fail-closed gate) — HIGH/HIGH.
3. **TU-003** (Six principles + Anti-Sycophancy) — MEDIUM/HIGH.
4. **SE-003** (Sub-phase resume) — HIGH/MEDIUM.
5. **TU-002** (Output-type discrimination) — HIGH/MEDIUM.
6. **TU-004** (BLOCKED at <0.70) — MEDIUM/MEDIUM.
7. **TU-005** (Drift consolidation) — MEDIUM/MEDIUM.
8. **SE-002** (Per-task UID) — MEDIUM/MEDIUM.
9. **SE-005** (Severity enum) — MEDIUM/HIGH.
10. **SE-004** (ExecutionMode enum) — MEDIUM/HIGH.
11. **TU-006** (Materialize skill sub-files) — LOW/HIGH.
12. **SE-006** (Auto-diagnostic threshold) — LOW/MEDIUM.

---

## 7. Risks

Risk register synthesizing R1-R8 + v3.7 prior-art. Each row: ID, source, description, likelihood, blast radius, mitigation hook.

| ID | Source | Description | Likelihood | Blast radius | Mitigation hook |
|---|---|---|---|---|---|
| RK-01 | R6 L17, L93, L99, L103 | Automatic classification false positives (over-classifying trivial change as STRICT) → unnecessary verification overhead | Medium | Wasted token/time budget on trivial tasks | Honor "better false positives than false negatives"; require `--reason` for tier override (`COMMANDS.md:86-119`); telemetry on `--skip-compliance` usage |
| RK-02 | R6 L17 | Automatic classification false negatives (under-classifying security-critical task as LIGHT) → skipped verification | Low (because of safety bias) | HIGH (production safety) | Critical path override (`auth/, security/, crypto/, models/, migrations/`); STRICT MCP block (`SKILL.md:253-263`); TU-001 unconditional FAIL on missing classification header |
| RK-03 | R6 L66; R2 L47 | STRICT-required MCP servers (Sequential, Serena) unavailable → STRICT cannot proceed | Medium | Blocks high-priority work | Already implemented as MCP circuit breaker; reinforces TU-001 #1 |
| RK-04 | R6 L78 | `--skip-compliance` escape hatch creates a security hole if applied to truly STRICT task | Low (target <12% usage per R2 L27) | HIGH if misused | Require `--reason` for override; telemetry on skip rate (currently unmetered, see Open Questions) |
| RK-05 | R6 L93, R7 §5 item 4, R8 §6 item 4 | Classification logic duplicated across `task.md`, `ORCHESTRATOR.md`, `sc-tasklist-protocol/SKILL.md`, `sc-tasklist-protocol/rules/tier-classification.md` → drift between copies | High (already manifest — STRICT keyword drift demonstrated) | Inconsistent classification of same input | TU-005 consolidation; `make verify-sync` |
| RK-06 | R6 L99, L103 | Keyword-scoring cannot handle context-dependent semantics; high-keyword-but-trivial task gets high-confidence elevated tier → user must override manually | Medium | Wasted verification overhead, user friction | TU-002 output-type detection helps; TU-004 BLOCKED state for low-confidence borderline cases |
| RK-07 | R2 L65 | LW's quality gates are agent-behavioral, not programmatic — if agent does not apply them they provide no protection. Applies to IC's existing TFEP and the new six-principles NFR | Medium | Verification skipped silently | TU-001 programmatic CRITICAL FAIL; TU-003 explicit principle list reduces ambiguity; sprint-side SE-001 fail-closed |
| RK-08 | R2 L67 | Classification uses keyword matching; cannot handle semantic context — task description omitting "security" misses elevation | Medium | Missed STRICT classifications | Critical path override is structural backstop; future improvement (out of scope `[inference]`): semantic classifier |
| RK-09 | R2 L71 | Output-type discrimination missing — code-level overhead applied to doc tasks | Medium | Wasted overhead on docs | TU-002 |
| RK-10 | R1 L66; R5 L75 | TurnLedger state not persisted — supervisor crash mid-phase loses budget tracking | Low (crashes infrequent) | Re-estimate budget on restart | Out of release scope but listed; mitigates partly with SE-003 sub-phase resume |
| RK-11 | R1 L66, L70; R5 L77 | Phase-level checkpointing is coarse — Phase 3 task 14 failure requires re-running all 15 tasks | Medium | Wasted turns on resume | SE-002 (UID) + SE-003 (sub-phase resume) |
| RK-12 | R5 L46 | Shadow-gates trade safety for observability — pipelines can proceed past failing gates accumulating invalid artifacts | Medium when `--shadow-gates` active | Invalid downstream artifacts | Never use `--shadow-gates` in production sprint runs; tighten SE-001 fail-closed semantics |
| RK-13 | R5 L85; R8 §6 item 8 | Phase discovery regex depends on filesystem sort order; same-number-prefix collisions possible | Low | Wrong phase order | Out of scope unless wave-N tasklist collides |
| RK-14 | R5 L17 | Single subprocess per phase blocks all subsequent tasks in that phase if one task is long-running | Medium | Phase latency | Out of release scope `[inference]` |
| RK-15 | R8 §5 L217-219; v3.7 prior art | Regression of v3.7 canonicalization — accidentally reintroducing `/sc:task-unified` as a separate live command | Low (explicit non-goal NG-1) | HIGH (re-collision) | TEST-SPEC.md:34-80 already enforces no `/sc:task-unified` strings; ensure new release inherits that test |
| RK-16 | R7 §5 item 1; R8 §6 item 2 | Lingering `SC:TASK-UNIFIED:CLASSIFICATION` header and `--caller task-unified` may be intentional telemetry compat — removing them may break downstream parsers | Unknown | Unknown — depends on telemetry consumers | Decision required (see Open Questions §8) |
| RK-17 | R7 §5 item 2; `SKILL.md:359-365` | Skill protocol references config files that do not exist (`config/tier-keywords.yaml` etc.) → operationally broken references | High (deterministic) | Confusion / documentation rot | TU-006 materialize or remove |
| RK-18 | R3 L96 | New auto-diagnostic invocation path requires `run_diagnostic_chain()` robustness to sprint-context input | Medium | Wasted diagnostic invocations or runtime errors | SE-006 only if diagnostic chain is hardened first |
| RK-19 | R3 L75 | Sub-phase resume changes prompt construction → affects output format for resumed phases | Medium | Downstream parser breakage | SE-003 requires careful prompt-template testing |
| RK-20 | R8 §5 L211-214; HANDOVER `:125-163` | Live sprint execution still not validated end-to-end (no real claude CLI or stream-json stub at v3.7 cutover) | Medium | Latent runtime bugs | Address as part of v3.7 follow-ups before adding SE-002..SE-006 changes |

---

## 8. Open questions

These require explicit decisions before implementation can begin.

### 8.1 Naming-artifact policy (BLOCKER for surface stability)

- **Q1.** Should the `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header sentinel at `task.md:50-67` (R7 §2 L101-112) be renamed to `<!-- SC:TASK:CLASSIFICATION -->`?
  - Evidence the rename is mechanically safe: zero live `/sc:task-unified` references in `src/` and `.claude/` (R8 §4 L130-131, `HANDOVER.md:64-72`).
  - Evidence the rename may break things: R7 §5 item 1 and R8 §6 item 2 note "May be intentional telemetry compatibility; not explained in source." No telemetry consumer is cited in the extracts.
  - **Recommendation:** Decide once. If kept, document the reason in a comment adjacent to the sentinel.

- **Q2.** Should `--caller task-unified` at `SKILL.md:191-197` / `:196` be renamed to `--caller task`?
  - Same risk profile as Q1. The string is consumed by `/sc:forensic` — confirm forensic side does not pattern-match on `task-unified` `[inference]`.

### 8.2 Output-type axis design (TU-002 prerequisites)

- **Q3.** What is the precedence rule when tier AND output-type conflict? E.g., a `*.md` analysis report (`output_type=analysis`) requested with `--compliance strict`. Does output-type-specific gate REPLACE or AUGMENT tier verification?
- **Q4.** How is `output_type=opinion` detected automatically? R4 L48 mentions "CEV structure required" but no detection rule appears in extracts.

### 8.3 BLOCKED-state UX (TU-004)

- **Q5.** What is the exact format of the blocking message? R4 L89 says it must include "computed tier, competing tier (highest alternative), and specific keywords causing the split" — but is this CLI prompt text, an inline comment in the classification header, or a tool error?
- **Q6.** Can the user override BLOCKED with `--compliance` in the same invocation, or must they re-run? `[inference]` re-run is implied but not stated.

### 8.4 Skill sub-file materialization (TU-006)

- **Q7.** Should `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml` (referenced at `SKILL.md:359-365`, R7 §5 item 2) be created as the single source of truth — and the inline tier logic in `task.md`/`ORCHESTRATOR.md`/`sc-tasklist-protocol/SKILL.md` migrated to load from them? Or should the broken references simply be removed?
- **Q8.** Same question for `MCP.md` and `ORCHESTRATOR.md` references — these exist in `core/` already, so the skill reference may just need path correction.

### 8.5 Severity-enum scope (SE-005)

- **Q9.** Does `GateFailureSeverity` apply only to sprint executor gates, or also to `/sc:task` per-tier gates? R3 L109 ties severity to STRICT/STANDARD/LIGHT tiers (sprint side), but TU-003 anti-sycophancy / six-principles enforcement could also use Sev 1/2/3. Decide whether to share the enum across both subsystems or keep them separate.

### 8.6 Sprint-side back-compat (SE-002, SE-003)

- **Q10.** Existing result files lack `task_uid` (R3 L55). R3 says "graceful fallback to full-phase restart is acceptable" — confirm this is the chosen migration path vs. forced backfill.

### 8.7 Telemetry / escape-hatch metering

- **Q11.** R2 L27 / R6 L17 target `<12%` usage for `--skip-compliance`. There is no extract evidence of usage metering today (`[inference]` — none of R1-R8 cite a counter or logging point). Should this release add metering, or is the target aspirational only?

### 8.8 Tasklist-protocol keyword reconciliation (TU-005)

- **Q12.** Live `/sc:task` STRICT keywords (R7 §2 L116) omit `password, credential, secret, jwt, transaction, query` that appear in `sc-tasklist-protocol/rules/tier-classification.md` (R8 §2 L80). Adopt the wider list for `/sc:task`, or narrow the tasklist protocol? Same question for LIGHT compounds (`small update, update comment, ...`) and STANDARD additions (`remove, delete, deprecate`) — R7 §5 item 4.

### 8.9 v3.7 unfinished follow-ups (cross-cutting, may be prerequisites)

- **Q13.** Should this release also close any of the v3.7 operational follow-ups (HANDOVER `:375-391`, R7 §5 item 8, R8 §6 item 8)? Specifically: `--checkpoint-gate-mode` flag; `_resolve_release_dir` grandparent walk; live run with stream-json stub or real claude; ruff cleanup; optional full 10-stage validation agents.

### 8.10 Six-principles enforcement mechanism (TU-003)

- **Q14.** R4 L77 calls TU-003 "agent instruction addition; no code changes." Will the principles be enforced only via the verification agent's prompt, or also via a programmatic checklist run by `sc-task-protocol`? The latter would tighten R7's known issue that gates are behavioral-only.

---

## 9. Prior-art constraints from v3.7-task-unified-v2

These are hard constraints inherited from the completed v3.7 release that this merger MUST honor.

### 9.1 Canonical `/sc:task` surface (BLOCKING constraint)

Evidence:
- `v3.7-task-unified-v2/HANDOVER.md:51-60`, cited at R8 §1 L15-16:
  > "/sc:task is now the single canonical name. N1-N4: commands/task-unified.md → commands/task.md; skills/sc-task-unified-protocol/ → skills/sc-task-protocol/; old paths deleted. N5: ClaudeProcess.build_prompt emits /sc:task Execute all tasks..."
- `HANDOVER.md:64-72` validation: zero live `/sc:task-unified` references in `src/` and `.claude/`.
- `TEST-SPEC.md:34-80` (R7 §4 L226): enforces no `/sc:task-unified` strings; `ClaudeProcess.build_prompt` must start with `/sc:task`.

**Constraint:** Do not reintroduce `/sc:task-unified` as a separate live command. Maps to non-goal NG-1.

### 9.2 N1-N12 rename map must remain green

From R8 §5 L202-203, the v3.7 naming consolidation task list (N1-N12):
- Delete legacy → rename command → rename skill → update frontmatter → Sprint CLI prompt → cleanup_audit → tasklist → command cross-refs → other protocol refs → core docs → sync → confirm task-mcp status.

**Constraint:** Any new merger artifact (extra commands, skill subdirectories, prompt strings) must not regress any of these 12 renames. CI tests added in v3.7 (TEST-SPEC.md:34-80) should remain green.

### 9.3 R1 / R2 split semantics (boundary discipline)

From R8 §5 L217 (`release-split-report.md`, `boundary-rationale.md:55-65`):
- v3.7 was SPLIT into R1 ("Fix the Pipeline" — naming + checkpoint) and R2 ("Show the Pipeline" — TUI).
- R1 handoff criterion: "`/sc:task` resolves correctly; zero remaining `sc:task-unified` references in `src/superclaude/` except historical artifacts."
- R2 depended on R1.

**Constraint:** Any further splits in this v3.75 release must respect the same handoff principle — the canonical-surface invariant is non-negotiable for any sub-release boundary. `[inference]` This suggests the release-split protocol should be applied to v3.75 if it grows beyond a single coherent slice (e.g., separating task-side TU-series from sprint-side SE-series).

### 9.4 Intentional carry-over artifacts must be documented

From R8 §5 L207-209, the v3.7 release explicitly preserved two strings as carry-overs:
- `SC:TASK-UNIFIED:CLASSIFICATION` header sentinel.
- `--caller task-unified` in TFEP forensic invocation.

**Constraint:** Any change to either string must come with explicit documentation of the telemetry-compat consequences. Removing without analysis would regress an intentional v3.7 decision. See Open Questions Q1, Q2.

### 9.5 Test baselines from v3.7

From R8 §4 L164-167 (`HANDOVER.md:113-121`):
- `tests/sprint/` full run: 921 passed, 57 failed (matches baseline).
- TUI Waves 1-2 + tmux + summarizer + retrospective: 125/125 pass.
- `test_process.py::TestClaudeProcess`: 16/16 including `test_build_prompt_contains_task_command`.

**Constraint:** This release must not regress these baselines. The 57 pre-existing sprint failures are inherited baseline — new failures introduced by this release must be net-new, not regressions.

### 9.6 v3.7 known anomalies still open (operational debt)

From R8 §5 L211-214 and R7 §5 item 8 (`HANDOVER.md:125-163, :182-305, :375-391`):
- `--checkpoint-gate-mode` CLI flag missing.
- `_resolve_release_dir` anchor-file dependency vs. grandparent-walk inconsistency.
- `--dry-run` doesn't exercise TUI path.
- Ruff baseline mismatch.
- `verify-checkpoints --json` affected by UV warnings.
- Live sprint execution not validated end-to-end.

**Constraint:** Not blockers for this release per se, but the spec MUST acknowledge them so that SE-002..SE-006 are not built on unstable foundations. See Open Question Q13.

### 9.7 Wave-4 checkpoint heading parser regression (do not reintroduce)

From R7 §5 item 9 (HANDOVER `:253-304`):
- Pre-fix parser matched legacy `### Checkpoint:` but not Wave-4 `### T<PP>.<NN> -- Checkpoint:`.
- Fix verified with +3 tests, no regressions.

**Constraint:** Any sprint-side prompt template change (SE-003 sub-phase resume changes prompt construction per R3 L75) MUST not regress the Wave-4 heading format. Re-run the +3 checkpoint-parser tests.

### 9.8 v2.0 / v3.7 collision lessons (must-avoid pattern)

From R8 §4 L150-154 (`task-vs-task-unified-risk-assessment.md:9-13, :132-169`):
- Both `task.md` and `task-unified.md` once declared `name: task`. HIGH risk.
- v2.0 recommendation that was eventually executed: delete `task.md`; rename `task-unified.md` to `task.md`; keep `name: task`.

**Constraint:** Never have two command files declare the same `name:`. Never add a new `name: task-unified` command. CI should fail if any file under `commands/` re-introduces the duplicate. `[inference]` — extract does not say CI enforces this explicitly, but R7 §4 indicates `TEST-SPEC.md` already tests for `/sc:task-unified` strings.

### 9.9 Skill sub-file convention (project-level)

From CLAUDE.md ("Project Structure"):
> `src/superclaude/skills/` — Skill packages (SKILL.md + refs/ + rules/ + templates/)

**Constraint:** When TU-006 materializes the missing skill sub-files for `sc-task-protocol`, it should align with this convention.

---

## Coverage notes (S-A synthesizer self-check)

- **§1 Scope:** 4 in-scope task-side targets (TU-001..004), 6 sprint-side targets (SE-001..006), 6 non-goals (NG-1..NG-6).
- **§2 Source index:** 18 distinct source files indexed, including the 3 input artifacts and 15 underlying source files referenced via R7/R8/R1-R6 citations.
- **§3 task-unified inventory:** flags (12 items), classification logic (11 items), protocol elements (7 items), best-of-breed candidates (10+ items) — all cited.
- **§4 /sc:task inventory:** 14 subsections covering command surface, flags, protocol, classification, MCP, sprint+cleanup integrations.
- **§5 Overlap matrix:** 47 rows (O1-O47) mapping concept → state, with `MERGED / PARTIAL / NOT-YET` labels and per-row evidence.
- **§6 Best-of-breed candidates:** 12 candidates total (TU-001..006, SE-001..006), each with source extract, current state, proposal, risk, value/tractability rating. Sorted ranking provided.
- **§7 Risks:** 20-row risk register (RK-01..RK-20).
- **§8 Open questions:** 14 questions (Q1-Q14) grouped into 10 decision areas. Explicitly includes the `SC:TASK-UNIFIED:CLASSIFICATION` sentinel and `--caller task-unified` artifact questions.
- **§9 Prior-art constraints:** 9 subsections enumerating constraints inherited from v3.7.

**Known gaps:**
- The extracts do not contain numeric ROI tables, so value/tractability rankings in §6.3 are `[inference]`.
- Telemetry consumer of `--caller task-unified` is not identified in any extract — Q2 cannot be answered from current sources alone.
- TFEP completion-checklist comparison (O20 "six conditions before complete status") cites R2 L85 but R2's extract does not enumerate the six conditions verbatim — implementation will need to consult the original LW source.
- The `--shadow-gates`, `--start/--end`, `--no-tmux`, `--auto-diagnostic-threshold` CLI surfaces appear in R5/R3 extracts but were not directly verified against `cli/sprint/` Python code in R7/R8; marked `[inference]` where they affect overlap rows.
- v3.7 operational follow-ups (Q13) are listed as cross-cutting but no decision is forced by S-A — S-B should pick whether to scope-in.
