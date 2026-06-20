# Research: Features and User Flows for Unified /sc:task

**Investigation type:** Feature Analyst
**Scope:** RELEASE-SPEC §1.2 verdict matrix + §2 surface contract + §3 protocol changes, FINAL-REPORT §6 best-of-breed, context-task-current-state full file, live code task.md + SKILL.md + COMMANDS.md + ORCHESTRATOR.md
**Status:** Complete
**Date:** 2026-05-14

---

## 1. Command Surface — Live Code (CODE-VERIFIED Inventory)

### 1.1 Command frontmatter and metadata

**Source:** `/config/workspace/IronClaude/src/superclaude/commands/task.md:1-10` **[CODE-VERIFIED]**

- `name: task` (single canonical name; no `task-unified`)
- `description: "Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation"`
- `category: special`, `complexity: advanced`
- `allowed-tools`: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, **Skill**
- `mcp-servers`: sequential, context7, serena, playwright, magic, morphllm
- `personas`: architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer
- `version: "2.0.0"` (the v3.75 RELEASE-SPEC §1.1 plans a bump to 2.2.0)

### 1.2 The two orthogonal dimensions

**Source:** `task.md:18-27` **[CODE-VERIFIED]**

`/sc:task [operation] --strategy [systematic|agile|enterprise] --compliance [strict|standard|light|exempt]`

| Dimension | Purpose | Options |
|-----------|---------|---------|
| Strategy | HOW to coordinate work | systematic, agile, enterprise, auto |
| Compliance | HOW strictly to enforce quality | strict, standard, light, exempt, auto |

Philosophy line (verbatim, `task.md:27`): "Better false positives than false negatives" — when uncertain, escalate to higher compliance tier.

### 1.3 Eight CLI flags — verified against COMMANDS.md:86-119

**Source:** `/config/workspace/IronClaude/src/superclaude/core/COMMANDS.md:86-119` **[CODE-VERIFIED]** plus `task.md:44` **[CODE-VERIFIED]**

The eight flags called out as the "no new flags this release" surface (RELEASE-SPEC §2.1):

| # | Flag | Category | Description |
|---|------|----------|-------------|
| 1 | `--strategy {systematic\|agile\|enterprise\|auto}` | Orchestration | How to coordinate work |
| 2 | `--compliance {strict\|standard\|light\|exempt\|auto}` | Quality | Tier override / auto-detect |
| 3 | `--verify {critical\|standard\|skip\|auto}` | Verification | Sub-agent vs direct test vs skip |
| 4 | `--skip-compliance` | Execution control | Escape hatch; bypass all compliance enforcement |
| 5 | `--force-strict` | Execution control | Override auto-detection to STRICT |
| 6 | `--parallel` | Execution control | Enable parallel sub-agent execution |
| 7 | `--delegate` | Execution control | Enable sub-agent delegation |
| 8 | `--no-escalation` | Execution control | Bypass TFEP triggers (voids ad-hoc-fix protection) |

The `--reason "..."` arg shown at COMMANDS.md:118 is described as **required justification for tier override**, not a top-level surface flag. RELEASE-SPEC §3.5 makes `--reason` mandatory companion to `--skip-compliance`, `--compliance`, and `--force-strict` for BLOCKED-state overrides.

**Verification done:** Grep `--caller task-unified` returns one hit at `SKILL.md:196`; grep of the sentinel `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` returns six paired open/close hits at `task.md:60,66,108,114,119,125,130,136,141,147`. Both naming artifacts are **carry-overs preserved verbatim** per RELEASE-SPEC §2.1 (Q1/Q2 DEFER-GATED to R3).

### 1.4 Triggers (auto-routing into /sc:task)

**Source:** `task.md:30-37` **[CODE-VERIFIED]**

| Trigger | Condition | Confidence |
|---------|-----------|------------|
| Complexity Score | Task complexity >0.6 with code modifications | 90% |
| Multi-file Scope | Estimated affected files >2 | 85% |
| Security Domain | Paths contain `auth/`, `security/`, `crypto/` | 95% |
| Refactoring Scope | Keywords: refactor, remediate, multi-file | 90% |

## Key Takeaways

- The command surface is stable at **exactly 8 CLI flags** plus `--reason` qualifier. v3.75 explicitly forbids adding a 9th flag (Rejection of `--output-type` per RELEASE-SPEC §1.6).
- Two carry-over naming artifacts (`SC:TASK-UNIFIED:CLASSIFICATION` sentinel + `--caller task-unified`) are intentional and gated to R3 — they remain live in source.
- The command has two orthogonal axes (Strategy × Compliance) but only the Compliance axis drives the classification header.

---

## 2. Classification Header Schema (MANDATORY FIRST OUTPUT)

### 2.1 Current four-tier schema (LIVE)

**Source:** `task.md:50-67` **[CODE-VERIFIED]**

Header is emitted as the very FIRST output, text-only, no tool invocation before it. The exact sentinel + body:

```
<!-- SC:TASK-UNIFIED:CLASSIFICATION -->
TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
CONFIDENCE: [0.00-1.00]
KEYWORDS: [matched keywords or "none"]
OVERRIDE: [true|false]
RATIONALE: [one-line reason]
<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->
```

Four "CRITICAL RULES" gate emission (`task.md:52-56`):

1. TEXT-ONLY — no Skill/Read/Grep before classification.
2. EXACT FORMAT — the HTML comment block, not `**CLASSIFICATION: ...**`.
3. VALID TIERS ONLY — `STRICT, STANDARD, LIGHT, EXEMPT`. Values like "ITERATIVE", "SIMPLE", "IMPLEMENT", "COMPLEX" are explicitly INVALID.
4. FIRST OUTPUT — header MUST precede any other text.

Low-confidence rule **as currently coded** (`task.md:91`): "If confidence <0.70, prompt user: 'Override with `--compliance [tier]`'." — this is a soft prompt, not a halt.

### 2.2 Planned five-state schema (v3.75 TU-004)

**Source:** RELEASE-SPEC.md `§2.4 Surface diff:143-145` and `§3.5 BLOCKED state:238-265` **[UNVERIFIED in code — not yet implemented]**

Surface diff:

```
- TIER: [STRICT|STANDARD|LIGHT|EXEMPT]
+ TIER: [STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED]
```

When `max_tier_score confidence < 0.70` after deployment of TU-004:

- DO NOT auto-classify.
- Emit header with TIER: BLOCKED, computed CONFIDENCE, comma-separated split-keywords, RATIONALE = "split between <tier-A> (<score-A>) and <tier-B> (<score-B>)".
- **Halt execution.** Do NOT invoke `Skill sc:task-protocol`.
- Require explicit re-invocation: `--compliance <tier> --reason "..."` OR `--skip-compliance --reason "..."` OR `--force-strict --reason "..."`.
- Each override path writes an audit log entry.

Release-boundary note (RELEASE-SPEC §3.5:261-264): tasks initiated **before** TU-004 deployment continue under their original classification. No in-flight reclassification.

### 2.3 Tier priority and decision tree

**Source:** `task.md:69-91` plus `ORCHESTRATOR.md:151-213` **[CODE-VERIFIED]**

Priority order (first match wins; `--compliance` override checked first):

1. **STRICT** (P1, safety-critical). Keywords: security, authentication, authorization, database, migration, refactor, breaking change, encrypt, token, session, oauth. Boosters: >2 files +0.3; security paths +0.4. Compounds: "fix security", "add authentication", "update database", "change api". Note: "quick security" → STRICT; "minor auth change" → STRICT.
2. **EXEMPT** (P2, non-code). Keywords: explain, search, commit, push, plan, discuss, brainstorm, what, how, why. Boosters: is_read_only +0.4; is_git_operation +0.5; all doc files +0.5. Patterns: starts with what/how/why/explain; docs-only paths (*.md, docs/).
3. **LIGHT** (P3, trivial). Keywords: typo, comment, whitespace, lint, docstring, formatting, spacing, minor. Boosters: single file +0.1; ≤50 lines estimated. Compounds: "quick fix", "minor change", "fix typo", "refactor comment".
4. **STANDARD** (P4, default). Keywords: implement, add, create, update, fix, build, modify, change. Default when no higher tier matches.

ORCHESTRATOR.md:151-213 decision tree (5 steps): override → compound → keyword scoring → resolve ties by priority → confidence threshold. **[CODE-VERIFIED]** — file exists, lines 151-213 contain `tier_classification` YAML block, priority rules table, context boosters, and compound phrase overrides exactly as described in context-task-current-state.md.

## Key Takeaways

- Live code has a **four-tier** schema; the **fifth state (BLOCKED)** is planned per TU-004 in RELEASE-SPEC §3.5 but **not yet in source**.
- The sentinel `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` appears literally at `task.md:60,66,108,114,119,125,130,136,141,147` — confirmed by grep. RELEASE-SPEC §2.1 preserves it verbatim.
- The header is gated to four critical rules — TEXT-ONLY, EXACT FORMAT, VALID TIERS ONLY, FIRST OUTPUT — that constrain agent behavior before any tool call.
- The orchestrator decision tree (step_1 override → step_2 compound → step_3 keywords → step_4 resolve → step_5 confidence) lives in `ORCHESTRATOR.md:151-213`. Priority on ties: STRICT > EXEMPT > LIGHT > STANDARD.

---

## 3. Execution Routing — Per-Tier User Flow

### 3.1 EXEMPT — User Flow

**Source:** `task.md:97` + `SKILL.md:106-108` **[CODE-VERIFIED]**

1. User invokes `/sc:task "explain how the routing middleware works"` (or any read-only/question).
2. Agent emits classification header in-line: `TIER: EXEMPT`, e.g. CONFIDENCE 0.92, KEYWORDS "explain, how".
3. Agent **executes immediately** — answers question or performs read-only op.
4. **No Skill invocation. No verification overhead.** Zero compliance tokens spent.

### 3.2 LIGHT — User Flow

**Source:** `task.md:98` + `SKILL.md:100-104` **[CODE-VERIFIED]**

1. User invokes `/sc:task "fix typo in error message"` or `/sc:task "fix typo in README"`.
2. Agent emits header `TIER: LIGHT`, e.g. CONFIDENCE 0.95, KEYWORDS "typo, fix".
3. Agent executes change directly: quick scope check (files/lines within bounds) → make changes → quick sanity check (syntax valid) → proceed with judgment.
4. **No Skill invocation. No verification.**

### 3.3 STANDARD — User Flow

**Source:** `task.md:99-100` + `SKILL.md:93-99` **[CODE-VERIFIED]**

1. User invokes `/sc:task "add pagination to user list endpoint"`.
2. Agent emits header `TIER: STANDARD`, e.g. CONFIDENCE 0.85, KEYWORDS "add, endpoint".
3. Agent invokes `Skill sc:task-protocol`.
4. Skill executes the 5-step STANDARD flow: load context via codebase-retrieval → search downstream impacts (`find_referencing_symbols` or grep) → make changes → run affected tests OR document manual verification → verify basic functionality.
5. Verification: **direct test execution** (300-500 tokens, 30s timeout) per `SKILL.md:114-119`.
6. MCP requirements: Sequential + Context7 (fallback allowed) per `SKILL.md:255-263`.

### 3.4 STRICT — User Flow

**Source:** `task.md:99-100` + `SKILL.md:80-91` **[CODE-VERIFIED]**

1. User invokes `/sc:task "fix security vulnerability in auth module"` (or any security/auth/database/refactor keyword).
2. Agent emits header `TIER: STRICT`, e.g. CONFIDENCE 0.95, KEYWORDS "security, vulnerability, auth".
3. Agent invokes `Skill sc:task-protocol`.
4. Skill executes the 11-step STRICT flow:
   1. `mcp__serena__activate_project`
   2. Verify git working directory clean (`git status`)
   3. Load codebase context (`codebase-retrieval`)
   4. Check relevant memories (`list_memories` → `read_memory`)
   5. Identify all affected files and test files
   6. Make changes with full checklist
   7. Identify all files that import changed code
   8. Update all affected files
   9. Spawn verification agent (quality-engineer)
   10. Run comprehensive tests: `pytest [path] -v`
   11. Answer adversarial questions
5. Verification: **sub-agent (quality-engineer)** (3-5K tokens, 60s timeout) per `SKILL.md:114-119`.
6. MCP requirements: Sequential + Serena, **fallback NOT allowed** per `SKILL.md:255-263`. If unavailable → block task execution (current behavior is block; TU-001 makes it CRITICAL FAIL).
7. **Critical Path Override** (`SKILL.md:121-123`): paths `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always trigger CRITICAL verification regardless of computed tier.

### 3.5 BLOCKED (NEW — planned v3.75 TU-004) — User Flow

**Source:** RELEASE-SPEC.md §3.5:238-265 **[UNVERIFIED in code; planned per v3.75 release-spec]**

1. User invokes `/sc:task "<ambiguous task>"`.
2. Classifier computes max_tier_score with confidence <0.70 (e.g. STRICT 0.45 vs STANDARD 0.42 — within 0.1 tie band).
3. Agent emits header with `TIER: BLOCKED`, computed CONFIDENCE, comma-separated split-keywords, RATIONALE = "split between STRICT (0.45) and STANDARD (0.42)".
4. **Execution halts.** Skill is NOT invoked.
5. Audit log entry written.
6. User must re-invoke explicitly using one of three override paths:
   - `/sc:task "..." --compliance <tier> --reason "..."` (bypass with explicit tier)
   - `/sc:task "..." --skip-compliance --reason "..."` (bypass tier check entirely)
   - `/sc:task "..." --force-strict --reason "..."` (force STRICT regardless)
7. RELEASE-SPEC §2.2:120 estimates **5-10% of `--compliance auto` users** will encounter BLOCKED (`[inference]` tag explicit in spec).

### 3.6 Override-Initiated User Flow

**Source:** `task.md:44` + `SKILL.md:326-332` **[CODE-VERIFIED]**

1. User invokes `/sc:task "update config file" --compliance strict`.
2. Agent emits header with `TIER: STRICT, OVERRIDE: true`.
3. Override sets OVERRIDE=true and bypasses keyword scoring (decision tree step_1 — 100% confidence per ORCHESTRATOR.md:158-160).
4. Skill executes the chosen tier's flow.

## Key Takeaways

- The four current tier flows differ dramatically in cost: EXEMPT/LIGHT skip the Skill entirely; STANDARD invokes the Skill with direct testing; STRICT invokes the Skill with a sub-agent quality-engineer.
- The Skill itself is **only invoked for STANDARD and STRICT** — explicitly stated in `SKILL.md:7-9` and `task.md:97-100`.
- BLOCKED is the planned fifth flow: classifier halts before Skill invocation, forcing explicit user re-invocation with `--reason`. Three documented override paths.
- Critical Path Override is a separate safety net: certain paths (auth/, security/, crypto/, models/, migrations/) escalate verification REGARDLESS of tier — preserved in v3.75.

---

## 4. v3.75 Additions — Protocol Changes (per RELEASE-SPEC §3)

### 4.1 TU-001 CRITICAL FAIL conditions (STRICT only)

**Source:** RELEASE-SPEC §3.3:191-214 **[UNVERIFIED in code]** + FINAL-REPORT §6.1 TU-001:397-405

Verdict: **ADOPT-WITH-DEPRECATION** (per §1.2 decision tree). Three unconditional FAIL conditions applicable to STRICT only:

| # | Condition | When checked | Always blocks? |
|---|-----------|--------------|----------------|
| 1 | Sequential or Serena MCP unavailable | task entry, after each turn | Yes |
| 2 | Output file absent after max_turns | after final turn | Yes (STRICT only) |
| 3 | Classification header absent | after first turn | Yes (STRICT only) |

**Current state:** Only Condition #1 exists today (`SKILL.md:255-263` blocks STRICT execution when required MCP unavailable). Conditions #2 and #3 are net-new.

Implementation: `CriticalFailCondition` dataclass in NEW file `audit.py`:

```python
@dataclass
class CriticalFailCondition:
    condition_type: str
    description: str
    always_blocks: bool = True
```

Decision rule for future additions: deterministic, STRICT-only, non-recoverable.

### 4.2 TU-003 Quality Principles NFR (six universal principles)

**Source:** RELEASE-SPEC §3.4:216-236 **[UNVERIFIED in code]** + FINAL-REPORT §6.1 TU-003:417-425

Verdict: **ADOPT** (clean — no break, no flag, no behavior change per `[inference]`).

The six principles enforced on **STANDARD and STRICT** verification only:

1. **Verifiability** — every claim cites file:line evidence.
2. **Completeness** — acceptance criteria explicit and verified.
3. **Correctness** — implementation matches stated specification intent.
4. **Consistency** — no internal contradictions.
5. **Clarity** — statements unambiguous and actionable.
6. **Anti-Sycophancy** — verdict independent of implementer's stated confidence.

Enforcement (Q14 (c) both): prompt names the six principles AND verification artifact contains a checklist with citation field per row. Audit log captures checklist completeness.

### 4.3 TU-004 BLOCKED state

See §2.2 and §3.5 above. Net-new fifth header tier value + halt semantics + three override paths + audit log entries. User impact estimated **5-10% of `--compliance auto` users** per RELEASE-SPEC §2.2:120 — **[inference]** explicitly marked in spec.

### 4.4 TU-007 Mandatory completion checklist

**Source:** RELEASE-SPEC §3.6:267-294 **[UNVERIFIED in code]** + FINAL-REPORT §6.1 TU-007:457-466

Verdict: **ADOPT-WITH-INVESTIGATION**. Pre-merge gate: LW-source verification must produce canonical condition list. Parameterized tests handle any count (5/6/7/8).

**Working placeholder** (subject to LW-source verification — RELEASE-SPEC explicitly flags this as `[inference]`):

1. All affected files have been identified and updated.
2. All tests pass (or manual verification documented for STANDARD/LIGHT).
3. No pre-existing test failures introduced.
4. No new contradictions or invariants violated.
5. Adversarial verification (STRICT) returned a non-FAIL verdict.
6. `think_about_whether_you_are_done` confirms completion.

**Pre-merge gate:** investigation completes; either confirms list matches LW original OR supplies canonical list. NO MERGE until investigation complete.

Test stub: `tests/skills/test_task_completion_checklist.py` — parameterized over canonical list from `docs/tu-007-completion-checklist-verification.md`.

### 4.5 Q11 Audit log infrastructure

**Source:** RELEASE-SPEC §3.7:296-323 **[UNVERIFIED in code — NEW file]**

NEW: `src/superclaude/skills/sc-task-protocol/audit.py`.

Three downstream goals:

1. TU-001 audit trail (CRITICAL FAIL events).
2. TU-004 BLOCKED override audit (per Q6 (c)).
3. Q11 `--skip-compliance` metering (currently unmetered).

JSONL schema per entry:

```json
{
  "ts": "ISO-8601",
  "task_id": "uuid",
  "tier": "STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED",
  "confidence": 0.85,
  "user_override_tier": null,
  "skip_compliance": false,
  "force_strict": false,
  "reason": null,
  "critical_fail": null
}
```

Persisted to `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`. Append-only; daily rotation.

**Concurrency contract (INV-005 mitigation):** writes within a single task lifecycle MUST be serialized through a single writer. Per-task write lock; cross-task ordering is timestamp-based but not strictly serial.

## Key Takeaways

- v3.75 adds four task-side capabilities to the protocol: TU-001 (three CRITICAL FAIL conditions, STRICT only), TU-003 (six-principle NFR), TU-004 (BLOCKED state), TU-007 (completion checklist).
- Plus Q11 audit log infrastructure (new `audit.py` module with daily-rotated JSONL).
- All four task-side additions are designed to ship in **R1** of the four-stage split. No new CLI flags introduced (flag surface stays at 8).
- TU-007 canonical condition list is explicitly **[inference]** — RELEASE-SPEC blocks merge until LW-source verification supplies the canonical list.
- TU-004 user-impact figure (5-10%) is explicitly **[inference]** in RELEASE-SPEC §2.2.

---

## 5. Invoker Personas (Who Calls /sc:task)

### 5.1 End-User Direct Invocation

**Source:** `task.md:39-44`, examples `task.md:106-148`, `SKILL.md:288-331` **[CODE-VERIFIED]**

Manual prompt-line use:

- `/sc:task "fix security vulnerability in auth module"` → STRICT
- `/sc:task "explain how the routing middleware works"` → EXEMPT
- `/sc:task "fix typo in error message"` → LIGHT
- `/sc:task "add pagination to user list endpoint"` → STANDARD
- `/sc:task "update config file" --compliance strict` → user-forced STRICT

User cares about: tier outcome, override mechanism, getting their work done with appropriate rigor.

### 5.2 Sprint Executor (Sprint CLI)

**Source:** `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:124,170` **[CODE-VERIFIED]**

The sprint CLI builds prompts of the form (verbatim from process.py:170):

```
/sc:task Execute all tasks in @{phase_file} ...
```

Method `build_prompt` (referenced as `ClaudeProcess.build_prompt` in `TEST-SPEC.md`) prefixes every phase-execution call with `/sc:task`. The context-snapshot (line 206 in context-task-current-state.md) cites `src/superclaude/cli/sprint/process.py:123-183` building `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` + tier instructions.

Sprint executor cares about: deterministic STRICT compliance, checkpoint emission, per-task UID stability (SE-002), sub-phase resume (SE-003), fail-closed gate (SE-001).

### 5.3 Cleanup-Audit Prompt Builders

**Source:** `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/prompts.py:26,47,69,92,116` **[CODE-VERIFIED]**

Five prompt builders, each producing a `/sc:task` invocation:

- L26: `/sc:task Perform a surface-level scan ...` (initial scan)
- L47: `/sc:task Perform deep structural analysis ...`
- L69: `/sc:task Detect duplication, sprawl, and consolidation ...`
- L92: `/sc:task Consolidate audit findings into a final summary ...`
- L116: `/sc:task Validate audit findings by spot-checking claims ...`

Cleanup-audit pipeline cares about: well-defined read-only/analysis behavior (likely EXEMPT or STANDARD tier), consistent output structure, evidence citations (TU-003 Verifiability principle directly relevant).

### 5.4 Forensic Invocation (`--caller task-unified`)

**Source:** `SKILL.md:196` **[CODE-VERIFIED — single hit]**

Within the TFEP flow, the skill self-invokes `/sc:forensic` with `--caller task-unified` string. This is **not user-facing**; it is a machine handshake between skill and the forensic pipeline.

- 1st TFEP trigger: `/sc:forensic --tier light --intent triage --caller task-unified --context ...` (~5-8K tokens)
- 2nd TFEP trigger: `/sc:forensic --tier standard ...` (~15-20K tokens)
- 3rd TFEP trigger: FULL STOP. Report to user.

The `task-unified` string is a lingering naming artifact (Q2 DEFER-GATED to R3 per RELEASE-SPEC §1.2). The forensic pipeline consumer reads this caller value; RELEASE-SPEC §1.6 explicitly preserves it pending A-005 investigation.

### 5.5 Tasklist Generator (`/sc:tasklist`)

**Source:** Referenced in context-task-current-state.md §2 (citing `sc-tasklist-protocol/SKILL.md:505-575`). **[CODE-VERIFIED in Phase 3 follow-up]**: direct Read of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:505-575` confirms drift. STRICT keyword list at `:528-531` includes `password, credential, token, secret, encrypt, permission, session, oauth, jwt` (security category) and `database, migration, schema, model, transaction, query` (data category) and `refactor, remediate, restructure, overhaul, multi-file, system-wide, breaking change, api contract` (scope category) — superset of live `/sc:task` STRICT keywords in `commands/task.md:71-75`. Compound overrides at `:513-521` and confidence scoring at `:567-575` match the original drift claim. **Drift is real and warrants TU-005 SoT YAML in R3.**

The tasklist protocol contains a **parallel deterministic classification algorithm** that mirrors and extends `/sc:task` tier logic. Extra keywords (`small update`, `update comment`, `fix spacing`, `fix lint`, `rename variable`) and numeric weights not in the command file. This drift is a known gap (RELEASE-SPEC RK-05, TU-005 DEFER-COUPLED to R3).

## Key Takeaways

- Four invoker personas: **end-user**, **sprint executor**, **cleanup-audit pipeline**, and **forensic self-handshake**. A fifth (**tasklist generator**) duplicates classification logic in parallel and is a drift source.
- Sprint executor is the **highest-volume programmatic invoker** and always uses STRICT (`--compliance strict --strategy systematic`).
- Cleanup-audit uses /sc:task as a multi-stage analysis runner with five distinct prompt templates.
- The forensic self-handshake hard-codes `--caller task-unified` — Q2 DEFER preserves this verbatim until A-005 forensic-consumer investigation completes.

---

## 6. Scope Statement (v3.75 RigorflowMerger)

### 6.1 In-scope (TL;DR) — RELEASE-SPEC §1.2

**Task-side (R1):** TU-001, TU-003, TU-004, TU-007.
**Sprint-side (R2):** SE-001, SE-002+SE-003 paired, SE-004, SE-005.
**TUI bundle (R2):** top-5 (P-05, P-02, P-03, P-07, P-01) in ship order.
**Infrastructure:** Audit log (Q11) — new `audit.py` module.

**Deferred to R3:** TU-002 (output-type axis), TU-005 (SoT YAML), TU-006 (skill sub-files), Q1 (sentinel rename), Q2 (forensic-caller rename).
**Deferred to R4:** SE-006 (auto-diagnostic threshold).

Effort per RELEASE-SPEC §7.1: R1 ~3-5 dev-days, R2 ~7-10 dev-days. Total v3.75 ~10-15 dev-days `[inference]`.

### 6.2 Out-of-scope (Non-goals, hard constraints from v3.7)

**Source:** RELEASE-SPEC §1.4 + FINAL-REPORT §1.2 **[CODE-VERIFIED constraints]**

- **NG-1.** Reintroduce `/sc:task-unified` as a live command (v3.7 hard constraint).
- **NG-2.** Resurrect `task-unified.md` or `sc-task-unified-protocol/` directories.
- **NG-3.** Replace keyword classifier with semantic NLP.
- **NG-4.** Adopt LW's bash-orchestrator / Python-from-bash / multi-backup patterns.
- **NG-5.** TypeScript plugin work (v5.0 scope).
- **NG-6 (FINAL-REPORT only):** Remove or rename the `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel and `--caller task-unified` forensic string without telemetry-compat plan.

### 6.3 Considered and explicitly rejected (RELEASE-SPEC §1.6)

- Full TU-002 + TU-005 + TU-006 in v3.75 → REJECTED (X-001..X-003, 80% confidence).
- Q1+Q2 renames with telemetry-compat shim in v3.75 → REJECTED (X-002, 80% confidence; A-005 unresolved).
- New `--output-type {auto|override}` CLI flag → **REJECTED** (C-012/X-005, 80% confidence). **Flag surface stays at 8.**
- 3.0.0 major version bump → REJECTED (C-013, 60% confidence). Bump is 2.0.0 → 2.2.0.
- SE-006 auto-diagnostic threshold → REJECTED for v3.75 (X-006, 80% confidence; RK-OOS-3 unresolved).

### 6.4 Surface contract — what stays unchanged (RELEASE-SPEC §2.1)

- Command name `/sc:task`.
- **All 8 CLI flags** (no new flag this release).
- Strategy axis values (systematic, agile, enterprise, auto).
- Compliance tier values (strict, standard, light, exempt).
- Verification axis (critical, standard, skip, auto).
- Carry-over strings preserved verbatim: `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`, `--caller task-unified`.

## Key Takeaways

- v3.75 is a **two-release split** (R1 task-surface + R2 sprint+TUI) shipping in parallel siblings, with R3 + R4 deferred to future releases.
- The release introduces **zero new CLI flags** — the only surface extension is the additive `BLOCKED` value in the classification header TIER enum.
- Five candidate changes are explicitly rejected as out-of-scope. Carry-over naming artifacts are preserved verbatim pending A-005 investigation.

---

## 7. Success Metrics

### 7.1 Live skill targets (currently coded)

**Source:** `SKILL.md:349-357` **[CODE-VERIFIED]**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tier classification accuracy | ≥80% | User feedback on appropriateness |
| User confusion rate | <10% | "Which command?" questions eliminated |
| Skip rate (`--skip-compliance`) | <12% | Override tracking |
| Regression prevention | ≥85% | Post-verification bug detection |
| STRICT tier overhead | <25% | Execution telemetry |

These are the **existing** success metrics in source. The audit-log infrastructure (Q11, planned for v3.75) is what enables actual measurement of skip rate and override patterns — currently unmetered per RELEASE-SPEC RK-04.

### 7.2 v3.75 Acceptance criteria (RELEASE-SPEC §9)

The release ships when:

1. All §5.1 + §5.2 + §5.2.5 + §5.5 + §5.6 tests pass.
2. §5.3 TU-007 LW-source verification complete (`docs/tu-007-completion-checklist-verification.md` published; parameterized tests pass against canonical condition list).
3. Regression baselines green: 921 sprint pass / 57 fail baseline; 125/125 TUI; 16/16 ClaudeProcess; **+3 Wave-4 parser tests** (RK-15); `TEST-SPEC.md:34-80` (no `/sc:task-unified` in build_prompt).
4. Migration guide published (`docs/migration/v3.75.md`) with one entry per ADOPT-WITH-DEPRECATION candidate.
5. Release notes cover behavioral changes (TU-001, TU-004, TU-007, SE-001), migration pointer, user-facing impact summary, carry-over preservation explanation, R3/R4 future plan.
6. Audit log infrastructure deployed and capturing every classification + override + escape-hatch use.
7. Backlog tasks created for A-005 forensic-consumer investigation, Q3 output-type-precedence confirmation, RK-OOS-3 diagnostic-chain hardening.
8. R2 (if shipped paired with R1): Wave-4 parser tests pass; `test_monitor_reset_between_tasks.py` passes (P-01); SE-002+SE-003 paired PR is single artifact.
9. Convergence and invariant gates: adversarial pipeline at convergence 86.8% (CONVERGED); 0 HIGH-severity UNADDRESSED invariant probe findings.

### 7.3 User-facing impact summary (RELEASE-SPEC §6.5)

| Change | What users see | Mitigation |
|--------|----------------|------------|
| TU-004 BLOCKED | Tasks with ambiguous keyword classification (~5-10% of historical traffic, `[inference]`) will halt where they previously auto-classified. | Release notes call this out; `--compliance auto` users see the change first. Error message points to `--compliance <tier> --reason "..."` or `--skip-compliance --reason "..."`. |
| TU-001 STRICT output absent | STRICT tasks that previously completed with empty output (likely buggy completions) will now FAIL. | Expected net positive; users with legitimate "no-output" STRICT tasks should reclassify to EXEMPT. |
| TU-007 completion checklist | STRICT/STANDARD tasks that previously returned `complete` despite gaps will now block. | Expected net positive; canonical condition list in release notes. |
| SE-001 empty output gate | Sprint runs that previously soft-passed on empty output will now fail-closed. | Sprint owners should expect 1-2 new failures per phase during the first week; classify each as pre-existing or net-new. |

### 7.4 Coverage targets (RELEASE-SPEC §5.7)

- 80% line coverage on all new code (TU-001, TU-003, TU-004, TU-007, audit.py, SE-001..005).
- **100% on `audit.py`** (security-sensitive write path).
- No coverage requirement on canonical-form-agnostic preservation tests (existence checks).

## Key Takeaways

- Live skill has **five success metrics** in source; three of them (skip rate, regression prevention, overhead) require the new audit-log infrastructure to be measurable.
- v3.75 acceptance is gated on a **9-item checklist** including the TU-007 LW-source verification as a hard pre-merge gate.
- Regression baselines are precise (921/57, 125/125, 16/16, +3 Wave-4) and inherited from v3.7. No new baseline definitions.
- User-impact figures (~5-10% for TU-004, "likely buggy" for TU-001) are explicitly `[inference]` and need post-deploy telemetry confirmation.

---

## 8. Edge Cases and Failure Modes

### 8.1 Low-confidence classification (current → planned BLOCKED)

**Current:** `task.md:91` prompts user with `--compliance [tier]` hint. Soft, non-blocking. **[CODE-VERIFIED]**

**Planned v3.75 (TU-004):** Deterministic BLOCKED state. Halts execution, requires explicit `--reason` re-invocation, writes audit log. Three override paths (`--compliance <tier>`, `--skip-compliance`, `--force-strict`). All require `--reason "..."`.

### 8.2 MCP missing for STRICT (TU-001 condition #1)

**Current:** `SKILL.md:259-263` says "If required servers unavailable for STRICT tier, block task execution." This is the only currently-enforced critical condition. **[CODE-VERIFIED]**

**Planned v3.75 (TU-001):** Formalized as `CriticalFailCondition` dataclass with `always_blocks=True`, persisted to audit log.

### 8.3 Absent output after max_turns (TU-001 condition #2 — NEW)

**Current:** No source-coded enforcement of empty-output-after-max-turns for STRICT. **[UNVERIFIED in code]** — RELEASE-SPEC §3.3 marks this as net-new for v3.75. STRICT only.

### 8.4 Absent classification header (TU-001 condition #3 — NEW)

**Current:** `task.md:50-67` instructs the agent to emit the header as FIRST output, but no source-coded enforcement that detects absent header and FAILs. **[UNVERIFIED in code]** — RELEASE-SPEC §3.3 makes this a CRITICAL FAIL after first turn. STRICT only.

### 8.5 Test Failure Escalation Protocol (TFEP)

**Source:** `SKILL.md:125-244` **[CODE-VERIFIED — extensive coverage]**

Three-trigger escalation budget:

- 1st: `/sc:forensic --tier light --intent triage --caller task-unified` (~5-8K tokens)
- 2nd: `/sc:forensic --tier standard` (~15-20K tokens)
- 3rd: FULL STOP. Report to user; do not attempt further fixes.

MUST-escalate triggers: any pre-existing test fails; ≥3 new tests fail simultaneously; runtime exceptions in implementation code.

Permitted direct-fix exceptions: single ImportError/NameError in newly-written test scaffolding (≤2 tests, error in test file not impl); lint/formatting failures; deprecation warnings.

`--no-escalation` flag (`task.md:48`) explicitly voids TFEP protection — "agents may fix test failures directly without structured forensic analysis. WARNING: voids TFEP protection."

### 8.6 Override invariants

- `--compliance <tier>` → forces tier regardless of keyword scoring (step_1 in decision tree; 100% confidence).
- `--force-strict` → bypasses everything, forces STRICT.
- `--skip-compliance` → bypasses all compliance enforcement (escape hatch; target <12% usage).
- All override paths in v3.75 will write audit log entries (Q11).

## Key Takeaways

- Of the three TU-001 CRITICAL FAIL conditions, **only #1 (MCP missing) is currently enforced** in source. #2 and #3 are net-new for v3.75.
- TFEP provides a substantial forensic escalation pipeline already in source — the v3.75 work does not change TFEP semantics but does add audit log capture.
- `--no-escalation` is a documented escape hatch that voids TFEP; its use will be metered through the audit log.

---

## 9. Integration Opportunities (Extension Points)

### 9.1 Extension point: New tier values

The classification header schema is enum-extensible: TIER values are validated against an explicit list (currently STRICT/STANDARD/LIGHT/EXEMPT; v3.75 adds BLOCKED). Adding a sixth tier requires:

- Update enum in `task.md:61`.
- Update enum in skill reference (`SKILL.md:7-9` plus tier execution sections).
- Update orchestrator decision tree priorities (`ORCHESTRATOR.md:181-186`).
- Update tasklist-protocol parallel logic (`sc-tasklist-protocol/SKILL.md:505-575`) — drift point per RK-05.
- Add to audit log schema.

The four-location drift problem (RELEASE-SPEC RK-05; TU-005 DEFER-COUPLED to R3) means every tier-enum extension currently touches 4 files. R3 SoT YAML (`config/tier-keywords.yaml` per Annex B) consolidates this.

### 9.2 Extension point: New compliance modes (output-type axis)

TU-002 (DEFER to R3) introduces `output_type ∈ {code, analysis, documentation, opinion}` as a layered axis on top of tier. Annex B preserves the design. This is an explicit forward-looking integration opportunity; v3.75 does NOT ship it but does not foreclose it (`--output-type` flag is explicitly rejected for v3.75 to keep flag count at 8).

### 9.3 Extension point: New CRITICAL FAIL conditions

TU-001 dataclass-based design (`CriticalFailCondition`) is extensible by adding new instances. Decision rule for additions (RELEASE-SPEC §3.3): deterministic, STRICT-only, non-recoverable failure mode. This pattern can absorb future conditions (e.g. invariant violations) without surface change.

### 9.4 Extension point: New quality principles

TU-003 six-principle NFR is enforced via prompt + checklist. Adding a 7th principle requires updating both the SKILL.md NFR section and the verification artifact template. The audit-log captures checklist completeness, allowing principle-level telemetry.

### 9.5 Extension point: New invokers

The skill currently supports four invoker patterns (end-user, sprint executor, cleanup-audit, forensic self-handshake). Adding a 5th invoker requires:

- Prompt building convention (e.g. `cli/<new_invoker>/prompts.py`).
- TEST-SPEC enforcement that the build_prompt method emits `/sc:task` (per `TEST-SPEC.md:34-80`).
- No changes to skill code (skill is invoker-agnostic).

## Key Takeaways

- The architecture has **four documented extension points**: tier enum (current), output-type axis (deferred R3), CRITICAL FAIL conditions (open via dataclass), quality principles (open via NFR list).
- Tier-enum extensions hit the **classification logic drift surface** (4 files). R3 SoT YAML is the planned consolidation.
- Adding new invokers is essentially free because the skill is invoker-agnostic — only prompt-building and TEST-SPEC need updates.

---

## Gaps and Questions

### Inference propagation (explicit `[inference]` items in RELEASE-SPEC / FINAL-REPORT)

1. **TU-007 canonical condition list is `[inference]`** (RELEASE-SPEC §3.6 KNOWN GAP; FINAL-REPORT §6.1 TU-007). The 6 conditions in §4.4 of this research are a **working placeholder**, not a verified list. Pre-merge gate: LW-source verification must produce or confirm the canonical list. Until then, the count itself (5/6/7/8) is unknown.

2. **TU-004 user-impact 5-10% is `[inference]`** (RELEASE-SPEC §2.2 row TU-004; §6.5 row TU-004 BLOCKED). The estimate of how many `--compliance auto` users will encounter BLOCKED has no telemetry backing — audit-log infrastructure (Q11) is what enables future measurement.

3. **Effort labels S/M/L are `[inference]`** (FINAL-REPORT §6.1 through §6.3 throughout). No empirical timing data; "S ≤0.5d, M 1-3d, L >3d" is convention not measurement.

4. **R3+R4 target windows are `[inference]`** (RELEASE-SPEC §1.5 + §7.1). "Within 2 release cycles" is soft, not an SLA.

5. **Verdicts (ADOPT/DEFER/REJECT) themselves are `[inference]`** synthesis where not directly cited from source extracts (FINAL-REPORT §6 lead paragraph).

### UNVERIFIED claims (planned features not yet in source)

6. **TU-001 condition #2 (empty STRICT output → FAIL)** — RELEASE-SPEC §3.3 designs this; **not present in `SKILL.md` today**. [UNVERIFIED]

7. **TU-001 condition #3 (missing STRICT header → FAIL)** — RELEASE-SPEC §3.3 designs this; **not present in `SKILL.md` today**. [UNVERIFIED]

8. **TU-003 NFR section in SKILL.md** — RELEASE-SPEC §3.4 designs the six principles; **no NFR section currently in `SKILL.md`**. [UNVERIFIED]

9. **TU-004 BLOCKED state** — RELEASE-SPEC §3.5 designs the halt + override semantics; **no BLOCKED handling currently in `task.md` or `SKILL.md`**. [UNVERIFIED]

10. **TU-007 completion checklist** — RELEASE-SPEC §3.6 designs the pre-`complete`-status gate; **no completion checklist currently coded**. [UNVERIFIED]

11. **Audit log infrastructure (`audit.py`)** — RELEASE-SPEC §3.7 designs the JSONL schema + concurrency contract; **file does not exist today**. [UNVERIFIED]

12. **Tasklist protocol parallel classification logic** — context-task-current-state.md §2 cites `sc-tasklist-protocol/SKILL.md:505-575` with extended keyword tables and numeric weights. **[CODE-VERIFIED in Phase 3 follow-up]** — direct Read confirms drift; see §5.5 above for the verified keyword superset. TU-005 (R3) is the planned consolidation.

### Open questions surfaced by adversarial review

13. **A-005 forensic-consumer investigation** — what downstream consumers read `--caller task-unified` and the `SC:TASK-UNIFIED:CLASSIFICATION` sentinel? Blocking gate for Q1/Q2 renames in R3.

14. **Q3 output-type precedence rule** — when both tier-axis and output-type-axis match, which wins? Blocking gate for TU-002 in R3.

15. **RK-OOS-3 diagnostic-chain hardening** — diagnostic chain must be robust to sprint-context input before SE-006 can ship. Blocking gate for R4.

16. **Confidence threshold (0.70)** — currently hard-coded (per FINAL-REPORT §3.1 R6 L87); not user-configurable. Should it be? No verdict in RELEASE-SPEC.

17. **CLAUDE.md `--no-escalation`** — flag is documented as voiding TFEP. Is there an audit-log capture for `--no-escalation` use planned? RELEASE-SPEC §3.7 lists `skip_compliance` and `force_strict` in JSONL schema but not `no_escalation`. [UNVERIFIED gap]

---

## Stale Documentation Found

### S-1. SKILL.md references config files that do not exist

**Source:** `SKILL.md:359-365` references `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml`. **[CODE-CONTRADICTED]** — the directory listing earlier in this research showed only `__init__.py` and `SKILL.md` under `sc-task-protocol/`. No `config/` subdirectory exists. This is the gap that TU-006 (DEFER to R3) addresses.

### S-2. `task.md:44` flag-reference pointer is incomplete

`task.md:44` says "See protocol skill for full flag reference." **[CODE-CONTRADICTED]** — `SKILL.md:37-45` shows only a subset (`--compliance strict|light`, `--skip-compliance`, `--verify auto`). The actual full 8-flag inventory lives only in `core/COMMANDS.md:86-119`. Documentation hygiene gap; not addressed in v3.75.

### S-3. SKILL.md numbering anomaly

`SKILL.md` jumps from Section "0. Classification (Already Performed)" to "2. Confidence Display" with no Section 1. **[CODE-VERIFIED anomaly]** — line 49 says "### 0. Classification (Already Performed)" then line 60 says "### 2. Confidence Display (Human-Readable)". Stale section numbering after a prior edit. Not addressed in v3.75 spec.

### S-4. context-task-current-state.md references TFEP "lingering naming artifact"

The TFEP forensic invocation includes `--caller task-unified` (`SKILL.md:196`). The context document (line 178) flags this as "a lingering naming artifact." **[CODE-VERIFIED string exists]** but flagged as intentional carry-over preserved verbatim per RELEASE-SPEC §2.1 — so the "stale" framing is itself stale: per v3.75 it is **deliberate carry-over**, not stale.

### S-5. Live skill says "Will:" twice instead of "Will:" then "Will Not:"

`task.md:152-163` lists "**Will:**" twice (`:152` and `:159`) before "**Will Not:**" at `:163`. **[CODE-VERIFIED]** — visible structural typo in the boundaries block. Not flagged by RELEASE-SPEC.

---

## Summary

The live `/sc:task` command implements a four-tier compliance classification (STRICT, STANDARD, LIGHT, EXEMPT) with an exact-format HTML-comment classification header (sentinel `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` preserved verbatim from the retired `/sc:task-unified` lineage) that is gated by four critical rules and emitted as the FIRST output before any tool invocation. The surface is **8 CLI flags** plus `--reason`, and the skill is invoked **only for STANDARD and STRICT** — EXEMPT and LIGHT bypass the skill entirely.

Four distinct invoker personas exercise this surface: end-user manual prompts, the sprint executor (`cli/sprint/process.py:170` building `/sc:task Execute all tasks in @<phase_file>`), five cleanup-audit prompt builders, and the TFEP forensic self-handshake (`--caller task-unified` at `SKILL.md:196`). A fifth shadow invoker — the tasklist protocol — duplicates classification logic with drift, the known issue that TU-005 will eventually consolidate in R3.

v3.75 adds five capabilities to this surface without changing the flag count: TU-001 (three CRITICAL FAIL conditions for STRICT — currently only condition #1 is enforced), TU-003 (six-principle universal NFR for STANDARD/STRICT verification), TU-004 (deterministic BLOCKED fifth state replacing the soft prompt at confidence <0.70), TU-007 (mandatory completion checklist with canonical condition list gated on LW-source verification), and Q11 audit log infrastructure (new `audit.py` JSONL daily-rotated module). All four task-side additions plus audit log ship in R1; R2 ships sprint-runtime + TUI fixes in parallel.

The success metrics in source today (`SKILL.md:349-357`) target ≥80% classification accuracy, <10% user confusion, <12% skip rate, ≥85% regression prevention, <25% STRICT overhead — but three of the five are unmeasurable without the v3.75 audit log. Acceptance is gated on a 9-item checklist including a mandatory LW-source verification for TU-007 before merge.

Five `[inference]` items propagate from RELEASE-SPEC: TU-007 condition count, TU-004 user-impact estimate, S/M/L effort labels, R3/R4 target windows, and the verdict synthesis itself. Six `UNVERIFIED` claims correspond to planned features not yet in source (TU-001 conditions #2/#3, TU-003 NFR, TU-004 BLOCKED, TU-007 checklist, `audit.py`). Three documentation-staleness gaps remain (missing `config/` directory referenced by skill; incomplete flag pointer in `task.md`; SKILL.md numbering anomaly).

---

**Status:** Complete
