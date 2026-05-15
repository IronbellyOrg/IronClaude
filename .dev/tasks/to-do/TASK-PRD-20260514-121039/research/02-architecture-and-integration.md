# Research: Architecture and Integration for Unified /sc:task

**Investigation type:** Architecture Analyst
**Scope:** command-skill split + audit log contract + MCP matrix + TFEP/forensic + sprint+cleanup_audit integrations + dependency graph + tech stack
**Status:** Complete
**Date:** 2026-05-14

---

## 1. Command-Skill Architectural Split

### 1.1 Command file: `src/superclaude/commands/task.md`

Verbatim header gate at `task.md:50-67` enforces a **TEXT-ONLY classification phase** that runs *before* any skill or tool is invoked. Four CRITICAL RULES at `task.md:50-56` [CODE-VERIFIED]:

1. **TEXT-ONLY**: "Do NOT invoke ANY tools (Skill, Read, Grep, etc.) for classification. Tool invocation begins AFTER classification."
2. **EXACT FORMAT**: HTML comment block `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->...<!-- /SC:TASK-UNIFIED:CLASSIFICATION -->` with fields `TIER`, `CONFIDENCE`, `KEYWORDS`, `OVERRIDE`, `RATIONALE`.
3. **VALID TIERS ONLY**: `STRICT | STANDARD | LIGHT | EXEMPT` (invalid: ITERATIVE/SIMPLE/IMPLEMENT/COMPLEX).
4. **FIRST OUTPUT**: classification header must be the very first output.

Tier rules at `task.md:69-91` prioritize STRICT > EXEMPT > LIGHT > STANDARD (first match wins; `--compliance` override checked first). Sub-0.70 confidence currently triggers a *soft* prompt: "Override with `--compliance [tier]`" — TU-004 (RELEASE-SPEC §3.5) replaces this with a deterministic BLOCKED state.

### 1.2 Skill file: `src/superclaude/skills/sc-task-protocol/SKILL.md`

Skill-entry note at `SKILL.md:7-9` (verbatim) [CODE-VERIFIED]:

> "Classification has already been performed by the `/sc:task` command before this skill was invoked. The classification header has already been emitted. Do NOT emit it again. This skill handles **execution only** for STANDARD and STRICT tier tasks."

Fallback (`SKILL.md:9`): if no classification header was emitted, the skill emits one using only the four valid tier values.

### 1.3 Execution routing table (`task.md:93-100`) [CODE-VERIFIED]

| Tier | Routes to skill? | Behavior |
|------|------------------|----------|
| EXEMPT | No | Execute immediately; read-only answer, no Skill invocation. |
| LIGHT | No | Direct trivial change; no Skill invocation. |
| STANDARD | Yes | `> Skill sc:task-protocol` (5-step protocol). |
| STRICT | Yes | `> Skill sc:task-protocol` (11-step protocol). |

### 1.4 Skill metadata and package contents

`SKILL.md:1-5` [CODE-VERIFIED]:
- `name: sc:task-protocol`
- `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task`

Skill directory contents (verified): only `SKILL.md` and a one-line `__init__.py` ("`# sc-task skill package`"). No `refs/`, `rules/`, `templates/`, `scripts/`, `config/`. The skill references `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml`, `MCP.md`, `ORCHESTRATOR.md` at `SKILL.md:359-365`, **but these files do not exist** (G7 in FINAL-REPORT §6.1; RK-18). [CODE-CONTRADICTED]

### 1.5 Per-tier execution protocols (`SKILL.md:76-123`) [CODE-VERIFIED]

- **STRICT (11 steps):** activate Serena → verify clean git → codebase-retrieval → check memories → identify affected files+tests → make changes with checklist → identify importers → update affected files → spawn quality-engineer → `pytest [path] -v` → answer adversarial questions.
- **STANDARD (5 steps):** load context via codebase-retrieval → search downstream impacts (`find_referencing_symbols` OR grep) → make changes → run affected tests OR document manual verification → verify basic functionality.
- **LIGHT (4 steps):** quick scope check → make changes → quick sanity check → proceed with judgment. *(Note: contradiction with task.md routing — LIGHT does NOT invoke this skill per `task.md:97-98`; the skill documents LIGHT execution defensively in case it is invoked anyway.)* [CODE-CONTRADICTED — minor]
- **EXEMPT (2 steps):** execute immediately → no verification overhead. *(Same defensive-only listing.)*

### Key Takeaways

- The split is enforced **textually, not programmatically**: command instructions tell the model not to invoke tools during classification, and the skill instructions tell the model the classification already happened. There is no runtime gatekeeper between them.
- Only **STANDARD and STRICT** route to the skill; LIGHT and EXEMPT bypass it entirely.
- The classification header is **load-bearing across processes**: downstream parsers (sprint, cleanup-audit, telemetry) rely on the sentinel block.
- The skill currently has **no Python sibling** — `__init__.py` is one comment line. The proposed `audit.py` (RELEASE-SPEC §3.7) would be the first executable Python in this skill package.

---

## 2. audit.py Contract (Spec — file not yet present)

**File status:** `src/superclaude/skills/sc-task-protocol/audit.py` does **NOT** exist in the working tree. The contract below is sourced from RELEASE-SPEC §3.3 and §3.7. [UNVERIFIED — spec-only; verify in implementation]

### 2.1 Purpose (RELEASE-SPEC §3.7)

The audit log serves three downstream goals:

1. **TU-001** CRITICAL FAIL audit trail.
2. **TU-004** BLOCKED override audit (per Q6 (c) — `--skip-compliance --reason "..."` overrides BLOCKED).
3. **Q11** `--skip-compliance` metering (target `<12%` per R2 L27 / R6 L17).

### 2.2 `CriticalFailCondition` dataclass (RELEASE-SPEC §3.3)

Verbatim from RELEASE-SPEC §3.3 [UNVERIFIED]:

```python
@dataclass
class CriticalFailCondition:
    condition_type: str
    description: str
    always_blocks: bool = True
```

Three canonical STRICT-only conditions [UNVERIFIED]:

| condition_type | When checked | always_blocks |
|---|---|---|
| Sequential or Serena MCP unavailable | task entry, after each turn | True |
| Output file absent after max_turns | after final turn | True |
| Classification header absent | after first turn | True |

Decision rule for future additions: any new condition must be **deterministic**, **STRICT-only**, and have a **non-recoverable failure mode**.

### 2.3 JSONL schema (RELEASE-SPEC §3.7)

Per-entry schema, verbatim [UNVERIFIED]:

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

Note: `tier` enum **includes BLOCKED** (TU-004 additive extension to the existing four-value enum).

### 2.4 File path and rotation

- **Path:** `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl` (under repo root, daily rotation).
- **Mode:** append-only.
- **Concurrency contract (INV-005 mitigation):** writes within a single task lifecycle MUST be serialized through a single writer. Per-task write lock. Cross-task ordering is timestamp-based but not strictly serial.

### 2.5 No-PII data handling (S17 compliance note)

The schema above contains: ISO timestamp, task UUID, tier enum, numeric confidence, boolean flags, and free-text `reason` string. The `reason` field is user-supplied and is the **only free-text field** — implementation must avoid accidentally logging arguments, file contents, or environment variables.

### Key Takeaways

- audit.py is **spec-complete but not implemented**. All claims in this section are [UNVERIFIED] until the file lands.
- Daily JSONL rotation under `.dev/audit/` aligns with project convention (`.dev/` is the canonical generated-artifact root per CLAUDE.md). [CODE-VERIFIED for path convention]
- Concurrency model is single-writer-per-task — not globally serialized. Downstream consumers must tolerate timestamp-only ordering across tasks.
- `tier` enum extension to include `BLOCKED` is the only schema-level coupling to TU-004.

---

## 3. MCP Requirements Matrix and Circuit Breaker Semantics

### 3.1 Authoritative source: `SKILL.md:253-263` (verbatim) [CODE-VERIFIED]

```
**Required Servers by Tier**:
- STRICT: Sequential, Serena (fallback not allowed)
- STANDARD: Sequential, Context7 (fallback allowed)
- LIGHT: None required (fallback allowed)
- EXEMPT: None required

**Circuit Breaker Behavior**:
- If required servers unavailable for STRICT tier, block task execution
- For other tiers, use fallbacks with noted limitations
```

### 3.2 Matrix

| Tier | Required MCP servers | Fallback allowed? | Action on outage |
|------|----------------------|-------------------|------------------|
| STRICT | Sequential **AND** Serena | **No** | **Block task execution** (CRITICAL FAIL per TU-001 #1) |
| STANDARD | Sequential **AND** Context7 | Yes | Use fallback with noted limitations |
| LIGHT | None | Yes | Proceed |
| EXEMPT | None | n/a | Proceed |

### 3.3 Command-file MCP declaration (`task.md:7`) [CODE-VERIFIED]

```yaml
mcp-servers: [sequential, context7, serena, playwright, magic, morphllm]
```

Command declares **six servers as available** (broader set); the **skill narrows the requirement per tier**. Playwright/Magic/Morphllm are not required by any tier per the matrix above — they are surface-available for tools like UI generation or large-edit operations.

### 3.4 Auggie / codebase-retrieval

`SKILL.md:83, 94, 269` invoke `codebase-retrieval` (the Auggie tool capability) during STRICT (step 3) and STANDARD (step 1) execution. The tool is referenced by capability name rather than server name (`auggie`) — invocation works through whatever MCP host provides `codebase-retrieval`. [CODE-VERIFIED]

### 3.5 Circuit breaker → CRITICAL FAIL coupling (TU-001)

RELEASE-SPEC §3.3 elevates the existing MCP-unavailable behavior from agent-instruction ("block task execution") to a **programmatic CriticalFailCondition** (`always_blocks=True`) checked at task entry AND after each turn. This is "deterministic, STRICT-only, non-recoverable" per the decision rule.

### 3.6 Assumption A-001 (FINAL-REPORT §10) [CODE-VERIFIED, claim UNVERIFIED]

> "The Sequential + Serena MCP hard requirement is correct current behavior, not itself a candidate for re-evaluation under STRICT-task outages."

This assumption is not validated; RK-03 ("STRICT-required MCP servers unavailable → STRICT cannot proceed") notes the operator escape is `--skip-compliance` (kept under 12% target). This couples MCP availability to the audit-metering goal.

### Key Takeaways

- STRICT MCP requirement is **fail-closed**: no fallback, no recovery, audit-logged.
- STANDARD MCP requirement is **fail-open with noted limitations** — implementation should record fallback in the audit log even though it's allowed.
- The command-vs-skill split puts the matrix in the skill file (`SKILL.md:253-263`), not in `task.md`. Skill is the authoritative source.
- Sequential is required by both STRICT and STANDARD; **Serena is STRICT-only**; **Context7 is STANDARD-only**. No tier requires both Serena and Context7 simultaneously.

---

## 4. TFEP and Forensic Invocation Flow

### 4.1 TFEP gates (`SKILL.md:125-244`) [CODE-VERIFIED]

Three VIOLATION-level prohibitions apply to STRICT and STANDARD tiers that run tests (`SKILL.md:129-135`):

1. No fixing code in response to test failures without TFEP workflow.
2. No modifying test expectations without adversarial validation.
3. No ad-hoc patches derived from test output.

Permitted direct-fix exceptions (`SKILL.md:137-141`):
- Single `ImportError`/`NameError` in test scaffolding the agent just wrote (≤2 tests).
- Lint/formatting failures.
- Deprecation warnings.

### 4.2 Test baseline snapshot (`SKILL.md:144-153`)

Pre-implementation baseline captured via `uv run pytest --collect-only -q` or directory listing. Each failing test classified as **pre-existing** (in baseline) or **new** (written this task). Classification drives MUST-escalate vs MAY-fix-directly.

### 4.3 Escalation triggers (`SKILL.md:157-168`)

MUST escalate when:
- Any **pre-existing test** fails (primary trigger).
- **≥3 new tests** fail simultaneously.
- **Runtime exceptions in implementation code** (TypeError, AttributeError, KeyError, etc.).

Gradient triggers (within-TFEP, future forensic integration):
- Repeated failure after fix attempt.
- Multi-file blast radius.
- Low-confidence RCA from adversarial debate.
- Unresolved adversarial outcome (tie/no-winner).
- Second failed retest.
- Cross-domain or non-obvious regression.

### 4.4 TFEP six-step execution flow (`SKILL.md:170-217`)

1. **Halt and freeze** — STOP testing, FREEZE implementation.
2. **Construct `failure_context`** YAML with `test_names`, `test_files`, `error_output`, `expected_behavior`, `actual_behavior`, `changes_made`, `task_description`, `test_baseline`, `escalation_count`. Write to `{output_dir}/context.yaml`.
3. **Invoke `/sc:forensic`** by escalation count.
4. **Consume forensic results** from `{output_dir}/return-contract.yaml`.
5. **Tasklist insertion** — read `tasklist_insertion_path`, add `## Failure Remediation Plan (Adjudicated)` heading, insert remediation tasks BEFORE existing test/verification tasks.
6. **Resume** with `--compliance strict` from the inserted remediation tasks.

### 4.5 Forensic invocation contract (`SKILL.md:191-197`) [CODE-VERIFIED]

Verbatim invocation pattern:

```
/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick
```

Escalation budget (`SKILL.md:240-244`):
- **1st trigger:** `--tier light --intent triage` (~5-8K tokens).
- **2nd trigger:** `--tier standard` (~15-20K tokens).
- **3rd trigger:** **FULL STOP**. Report to user. Do not attempt further fixes.

### 4.6 `--caller task-unified` carry-over (assumption A-005)

The literal string `task-unified` in `--caller task-unified` is a **lingering naming artifact** preserved verbatim per RELEASE-SPEC §2.1 (Q2 DEFER-GATED on A-005). FINAL-REPORT §10 A-005 [CODE-VERIFIED, downstream UNVERIFIED]:

> "The `--caller task-unified` string is consumed downstream by `/sc:forensic` but neither draft has verified what `/sc:forensic` does with it."

**Action required (FINAL-REPORT §10):** Implementation phase must enumerate `/sc:forensic` consumers of `--caller task-unified` before any rename in a future cleanup release. The DEFER-lock test at RELEASE-SPEC §5.2.5 (`test_caller_string_is_canonical`) reads the canonical form from a SoT constant — when R3 renames, only the SoT constant updates.

### 4.7 Forensic outcome handling

From `SKILL.md:201-205`:
- `test_is_wrong == true` → Present to user for review. **Do NOT auto-fix tests.**
- `status == "success"` → proceed to tasklist insertion.
- `status == "partial"` or `recommended_escalation != "none"` → increment `escalation_count`, return to Step 3.
- `status == "failed"` → Report to user, halt execution.

### Key Takeaways

- TFEP is the **only path** by which test failures may modify code in STRICT/STANDARD — ad-hoc patches are VIOLATION-level prohibited.
- The forensic pipeline is **autonomous after invocation** (runs through all its phases, returns a structured contract). `sc-task-protocol` is the *caller*, not the executor.
- 3 strikes = FULL STOP — no infinite escalation.
- `--caller task-unified` is **preserved verbatim until A-005 is validated**; tests assert canonical form via SoT constants, not literal substring, so the eventual rename is non-breaking.
- Incident reports (`tfep-incident-report.md` per `SKILL.md:222-236`) are committed to git alongside forensic artifacts — durable audit trail beyond the JSONL log.

---

## 5. Sprint CLI Integration

### 5.1 `ClaudeProcess.build_prompt` — exact emitted string [CODE-VERIFIED]

File: `src/superclaude/cli/sprint/process.py`. Class `ClaudeProcess` (lines 88-216) extends `pipeline.process.ClaudeProcess` with sprint-specific `__init__` and `build_prompt()`.

The prompt's **first line** (process.py:170-171) is verbatim:

```
/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic
```

This satisfies prior-art constraint 9.1 ("ClaudeProcess.build_prompt must start with /sc:task" per `v3.7-task-unified-v2/TEST-SPEC.md:34-80`).

### 5.2 Sprint context envelope appended to prompt (process.py:147-167)

After the `/sc:task` line, the prompt appends:

```
## Sprint Context
- Sprint: {sprint_name}
- Phase: {pn} of {total_phases}
- Artifact root: {release_dir}/artifacts
- Results directory: {results_dir}
- Prior-phase artifact directories: ...     (only if pn > 1)
- Prior-phase directories: ...              (only if pn > 1)
- All task details are in the phase file. Do not seek additional index files.
```

### 5.3 Execution rules block (process.py:175-185)

```
## Execution Rules
- Execute tasks in order (T{pn:02d}XX.01, T{pn:02d}XX.02, etc.)
- For STRICT tier tasks: use Sequential MCP for analysis, run quality verification
- For STANDARD tier tasks: run direct test execution per acceptance criteria
- For LIGHT tier tasks: quick sanity check only
- For EXEMPT tier tasks: skip formal verification
- If a STRICT-tier task fails, STOP and report -- do not continue to next task
- For all other tier failures, log the failure and continue
```

Note: Sprint hardcodes `--compliance strict --strategy systematic` at the **phase level**. Per-task tier classification still happens inside the model via the `/sc:task` classification header. The "STRICT-tier task fails → STOP" rule maps to the SE-001 fail-closed semantics (RELEASE-SPEC §2.2).

### 5.4 Checkpoint block (process.py:187-195)

Instructs the model to scan the phase file for `### Checkpoint:` sections, extract `Checkpoint Report Path:`, and write structured reports. This is the Wave-4 heading format (`### T<PP>.<NN> -- Checkpoint:` from v3.7 prior-art §9.7 — RK-15 requires this NOT regress).

### 5.5 Scope boundary and result file (process.py:197-215)

- After all tasks and checkpoints complete, STOP immediately.
- Do not read subsequent phase files.
- Write `EXIT_RECOMMENDATION: CONTINUE` to `config.result_file(phase)` as final action.
- Write `EXIT_RECOMMENDATION: HALT` instead if STRICT-tier task failed (SE-001 fail-closed).

### 5.6 Context injection helpers (process.py:257-385)

- `build_task_context(prior_results, start_commit, compress_threshold=3)` — produces structured markdown with prior task summaries, gate outcomes, remediation history, and git diff context. Compresses older tasks beyond `compress_threshold` to one-line summaries.
- `get_git_diff_context(start_commit)` — runs `git diff --stat` against the sprint start commit; returns markdown section or empty on error.
- `compress_context_summary(results, keep_recent=3)` — older tasks reduced to one-line summary, recent tasks at full detail.

### Key Takeaways

- Sprint emits the **canonical `/sc:task`** prompt (zero `/sc:task-unified` references — N5 of N1-N12 rename map).
- Sprint hardcodes `--compliance strict --strategy systematic` at the phase boundary; per-task tier is still classified by the model.
- Sprint's STRICT-fail semantics (HALT on STRICT failure, continue on non-STRICT) maps onto SE-001 fail-closed gate evaluation and SE-005 `GateFailureSeverity`.
- Sub-phase resume (SE-003) will need to **change `build_prompt`** to support resuming partway through a phase. RK-15 mandates re-running the Wave-4 checkpoint parser tests (+3 tests).

---

## 6. Cleanup-Audit CLI Integration

### 6.1 Five prompt builders [CODE-VERIFIED]

File: `src/superclaude/cli/cleanup_audit/prompts.py`. Each function returns a string whose **first line starts with `/sc:task`**:

| Function | Line | Pass / purpose | First-line action verb |
|----------|------|----------------|------------------------|
| `build_surface_scan_prompt` | 20-38 | Pass 1: surface scanning (DELETE/REVIEW/KEEP) | "Perform a surface-level scan..." |
| `build_structural_analysis_prompt` | 41-61 | Pass 2: deep structural (8-field profiles) | "Perform deep structural analysis..." |
| `build_cross_cutting_prompt` | 64-84 | Pass 3: cross-cutting (duplication, sprawl) | "Detect duplication, sprawl..." |
| `build_consolidation_prompt` | 87-108 | Pass 4: consolidation and summary | "Consolidate audit findings..." |
| `build_validation_prompt` | 111-130 | Pass 5: validation (spot-checking) | "Validate audit findings..." |

### 6.2 Common pattern

Every prompt:
1. Starts with `/sc:task` plus a one-line description of work.
2. Provides "Prior Context" pointing at the previous pass's output file.
3. Specifies "Output Requirements" with YAML frontmatter (status, pass, finding counts).
4. Mandates the machine-readable marker: `EXIT_RECOMMENDATION: CONTINUE` or `EXIT_RECOMMENDATION: HALT`.

### 6.3 No `--compliance` flag is passed [CODE-VERIFIED]

Unlike sprint (which forces `--compliance strict`), cleanup-audit prompts **omit `--compliance`** entirely. The model performs the auto-classification per `task.md:69-91`. For audit work (read-only analysis writing `.md` reports), this likely classifies as EXEMPT (read-only docs path) or STANDARD per the tier rules — **not** STRICT. This is intentional: audit passes do not modify production code.

### Key Takeaways

- Cleanup-audit produces **5 sequential `/sc:task`** invocations chained via prior-pass file references.
- Output discipline is enforced via YAML frontmatter contracts (not via STRICT tier compliance).
- The `EXIT_RECOMMENDATION` sentinel is the cleanup-audit equivalent of the sprint result-file marker.
- Auto-classification (no `--compliance` flag) means cleanup-audit will likely route to EXEMPT or STANDARD — neither invokes the heavy TFEP machinery.

---

## 7. Shared Assumptions A-001..A-005 (FINAL-REPORT §10) — Architectural Implications

| ID | Assumption | Architectural implication |
|----|------------|---------------------------|
| **A-001** | Sequential + Serena MCP hard requirement is correct (not itself a candidate for re-evaluation) | The STRICT MCP block is a **load-bearing axiom** of the architecture. Any future change to STRICT routing requires re-validating this assumption — RK-03 mitigations (audit-log skip-compliance, document operator escape) presume this stays. |
| **A-002** | Candidate set is closed at Wave-1 extracts (TU-001..TU-006, SE-001..SE-006, TU-007) | No novel candidates may be introduced inside this release. The dependency graph (§9) is **closed** — additions go to R3 (TU-005/TU-006/SE-006) or later. |
| **A-003** | Effort labels S/M/L and value/tractability ratings are reliable proxies without explicit estimation | Sizing risk: tasks marked S could exceed budget. The release split (R1=task-side, R2=sprint-side) provides a pressure-release valve if S/M/L proves inaccurate. |
| **A-004** | The six universal quality principles (TU-003) are sound design and need not be re-derived | TU-003 (Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy) is adopted **on faith of R4 source**. Q14 forces "both prompt and checklist" enforcement — programmatic checklist provides audit trail if adoption proves unsound. |
| **A-005** | `--caller task-unified` is consumed downstream by `/sc:forensic` but no draft verified what `/sc:forensic` does with it | **Hard pre-condition for Q1/Q2 rename.** Implementation must enumerate `/sc:forensic` consumers before any rename. The DEFER-lock tests (RELEASE-SPEC §5.2.5) encode this via SoT constants so the rename in R3 is mechanical. This is the **single biggest unknown** in the architecture. |

### Key Takeaways

- A-001 and A-005 are the **two architecturally load-bearing assumptions**. A-001 underwrites the STRICT MCP block; A-005 gates Q1/Q2 renames.
- A-002 closes the candidate set — no scope creep mid-release.
- A-004 is the basis for the TU-003 NFR section; if challenged, Q14's "both prompt and checklist" enforcement provides the rollback hook.
- All five assumptions are non-blocking for v3.75 per FINAL-REPORT §10 footer — but the implementation phase is **expected to validate A-005**.

---

## 8. Technology Stack (S15)

### 8.1 Languages & runtime

- **Python ≥ 3.10** (per `pyproject.toml`; PEP 517 build via hatchling).
- **Package name:** `superclaude` v4.2.0.
- **UV** for all Python operations (no `python -m`, no `pip install`, no bare `python script.py`).

### 8.2 Core libraries

| Layer | Library | Use |
|-------|---------|-----|
| Test runner | `pytest >= 7.0.0` | Test execution; auto-loaded plugin |
| CLI | `click >= 8.0.0` | Sprint, roadmap, tasklist, audit subcommands |
| TUI / output | `rich >= 13.0.0` | Sprint/cleanup-audit TUI rendering |
| Data classes | stdlib `dataclasses` | `CriticalFailCondition`, models |
| JSONL I/O | stdlib `json` | Audit log persistence |
| Concurrency | stdlib `threading` / file lock | Per-task audit write lock |
| Subprocess | stdlib `subprocess` | Sprint `git diff --stat`, `claude --print --verbose` |
| Datetime | stdlib `datetime` | ISO-8601 timestamps, daily rotation key |

### 8.3 MCP servers (external)

| Server | Role | Tier requirement |
|--------|------|------------------|
| Sequential | Token-efficient multi-step reasoning | STRICT, STANDARD |
| Serena | Symbol navigation, session memory | STRICT |
| Context7 | Official library/framework docs | STANDARD |
| Auggie (via `codebase-retrieval`) | Codebase context retrieval | Tool capability, not tied to one server |
| Playwright | Browser automation | Optional (per command file) |
| Magic | UI component generation | Optional |
| Morphllm | Large-edit operations | Optional |

### 8.4 Filesystem layout

- `src/superclaude/skills/sc-task-protocol/` — skill package (SKILL.md, future audit.py)
- `src/superclaude/commands/task.md` — command file (source of truth)
- `.claude/commands/sc/task.md` — dev copy (synced via `make sync-dev`)
- `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl` — daily-rotated audit log [spec, not yet created]
- `tests/skills/` — protocol-side tests
- `tests/sprint/` — sprint executor tests

### 8.5 Build / sync pipeline

- `make dev` — editable install + dev deps.
- `make sync-dev` — `src/superclaude/{skills,agents,commands}` → `.claude/`.
- `make verify-sync` — confirm src and dev copies match (CI gate).
- `make test`, `make lint`, `make format` — quality gates.

### Key Takeaways

- Pure-Python stdlib for audit.py — no new dependencies needed.
- MCP servers are runtime requirements, not Python packages — they must be available via gateway or direct connection.
- The two-tree layout (`src/superclaude/` source-of-truth, `.claude/` dev copy) is enforced by `make sync-dev` / `make verify-sync`. Any new file in `sc-task-protocol/` must round-trip through both.

---

## 9. Dependency Graph

### 9.1 Edit-time / runtime dependency graph

```
                ┌──────────────────────────────────────────────────┐
                │  src/superclaude/commands/task.md                │
                │  (classification, TEXT-ONLY, no tool calls)      │
                └──────────────────┬───────────────────────────────┘
                                   │ classification header emitted
                                   ▼
                ┌──────────────────────────────────────────────────┐
                │  Skill sc:task-protocol                          │
                │  src/superclaude/skills/sc-task-protocol/SKILL.md│
                │  (STANDARD + STRICT execution only)              │
                └────┬───────────────────────────────────┬─────────┘
                     │                                   │
                     │ (TU-001 critical-fail check)      │ (TFEP)
                     ▼                                   ▼
        ┌────────────────────────┐         ┌────────────────────────────┐
        │  audit.py (NEW)        │         │  /sc:forensic               │
        │  - CriticalFailCondition│         │  --caller task-unified      │
        │  - JSONL writer         │         │  (escalation 1→2→FULL STOP)│
        │  - .dev/audit/*.jsonl   │         └────────────────────────────┘
        └────────────────────────┘
                     │
                     │ (MCP requirements per tier)
                     ▼
        ┌────────────────────────────────────────────────┐
        │  MCP servers                                   │
        │  - Sequential   (STRICT, STANDARD)             │
        │  - Serena       (STRICT, no fallback)          │
        │  - Context7     (STANDARD, fallback allowed)   │
        │  - Auggie (codebase-retrieval)                 │
        └────────────────────────────────────────────────┘


  ┌─────────────────────────────────┐
  │  src/superclaude/cli/sprint/    │
  │  process.py::ClaudeProcess      │       ▶▶ /sc:task Execute all tasks
  │  build_prompt() (per phase)     │           in @<phase_file>
  └─────────────────────────────────┘           --compliance strict
                                                 --strategy systematic

  ┌─────────────────────────────────┐
  │ src/superclaude/cli/            │
  │ cleanup_audit/prompts.py        │       ▶▶ /sc:task (no --compliance)
  │ 5 builders (surface, structural,│           × 5 sequential passes
  │ cross-cutting, consolidation,   │
  │ validation)                     │
  └─────────────────────────────────┘
```

### 9.2 Call sequence — STRICT task happy path

1. User invokes `/sc:task "..."` (or upstream caller emits the line).
2. Command classifies (TEXT-ONLY) → emits header `TIER: STRICT, ...`.
3. Command routes to `Skill sc:task-protocol`.
4. Skill checks MCP availability (Sequential + Serena required, no fallback).
   - If unavailable → CRITICAL FAIL → audit.py writes entry with `critical_fail`.
5. Skill runs 11-step STRICT protocol (Serena activate, codebase-retrieval, etc.).
6. Tests run; if pass → quality-engineer verification → audit.py log success.
7. If tests fail → TFEP gates → `/sc:forensic --tier light --intent triage --caller task-unified`.

### 9.3 Call sequence — Sprint phase

1. `superclaude sprint run` invokes `ClaudeProcess` per phase.
2. `build_prompt()` produces `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` + context.
3. Subprocess `claude --print --verbose` consumes the prompt.
4. Inside the subprocess, per-task tier classification still happens via the command's classification rules.
5. Phase produces checkpoint reports + `EXIT_RECOMMENDATION: CONTINUE|HALT`.

### 9.4 Call sequence — Cleanup-audit pass

1. CLI emits `build_surface_scan_prompt(...)` → `/sc:task Perform a surface-level scan...`.
2. Subprocess executes; writes output file referenced in YAML frontmatter.
3. CLI emits `build_structural_analysis_prompt(..., surface_results=path)` referencing the prior file.
4. Repeat through cross-cutting, consolidation, validation.

### 9.5 Risk surface from dependencies

| Risk | Source | Mitigation |
|------|--------|------------|
| STRICT MCP outage cascades to all STRICT tasks | RK-03 | Audit log + operator `--skip-compliance` escape (<12% target via Q11 metering) |
| audit.py file I/O failure on rotating boundary | INV-005 | Per-task write lock; timestamp-only cross-task ordering |
| Forensic-caller carry-over (A-005) | Q2 / RK-10 | DEFER-lock test reads canonical form from SoT constant |
| Sprint sub-phase resume changes prompt construction | RK-15 | Re-run Wave-4 +3 checkpoint parser tests |
| Cleanup-audit auto-classification → unexpected STRICT routing | Inference | Could happen if a future audit pass keyword-matches STRICT (e.g., "authorization"); audit log captures tier so this is detectable |

### Key Takeaways

- The graph is **mostly tree-shaped**: command fans out to skill or direct execution; skill fans out to audit.py, MCP servers, and forensic.
- Sprint and cleanup-audit are **siblings** under `cli/`, both emitting `/sc:task` strings into subprocess prompts. They do not depend on each other.
- audit.py is a **new node** with **zero existing dependents** today — its absence means TU-001 audit, TU-004 BLOCKED audit, and Q11 metering all share the same risk of "file not yet implemented."
- The single biggest dependency-graph unknown is the **forensic-caller consumer enumeration (A-005)**.

---

## 10. Gaps and Questions

### 10.1 audit.py does not exist [UNVERIFIED]
The file `src/superclaude/skills/sc-task-protocol/audit.py` referenced by RELEASE-SPEC §3.7 is not present in the working tree. All implementation details (dataclass shape, JSONL schema, rotation behavior, write lock) are spec-only. Implementation must produce this file with tests under `tests/skills/test_task_protocol_critical_fail.py` per RELEASE-SPEC §5.2.

### 10.2 SKILL.md references nonexistent config files [CODE-CONTRADICTED]
`SKILL.md:359-365` references `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml`, `MCP.md`, `ORCHESTRATOR.md` under the skill. None of these exist in `sc-task-protocol/`. TU-006 DEFER (R3) means this stays broken in v3.75; documentation should at least be path-corrected (Q8 recommends path-correct in same release as Q7).

### 10.3 LIGHT/EXEMPT execution listed in SKILL.md but routing bypasses skill [CODE-CONTRADICTED — minor]
`SKILL.md:100-108` documents LIGHT (4 steps) and EXEMPT (2 steps) execution. But `task.md:97-98` explicitly says LIGHT and EXEMPT "No Skill invocation needed." The skill listings appear to be defensive fallbacks if the skill is invoked anyway. Not a functional bug, but doc dissonance.

### 10.4 A-005 forensic-caller consumer enumeration unresolved
Per FINAL-REPORT §10 action, implementation must enumerate `/sc:forensic` consumers of `--caller task-unified` before Q1/Q2 rename. v3.75 explicitly DEFERS rename; the work for R3 is to (a) audit consumers, (b) update SoT constant, (c) ship rename with shim.

### 10.5 Q14 enforcement mechanism for TU-003 not finalized
Q14 recommendation is "(c) both" — prompt + programmatic checklist. The skill changes in RELEASE-SPEC §3.4 specify "prompt + checklist" but the checklist implementation surface (where the checklist lives, who writes it) is not pinned. Likely lives inside the verification artifact produced by the quality-engineer agent.

### 10.6 Q11 audit metering scope
RELEASE-SPEC §3.7 includes `skip_compliance` boolean in the schema. The target is "<12% usage" but no consumer/dashboard is specified — metering is "(a) add metering this release" but no reporting layer is defined. Implementation likely just collects; reporting is TBD.

### 10.7 BLOCKED state UX (Q5) not pinned
Q5 recommendation is "(a) CLI prompt + (b) inline header for telemetry." The header schema in §3.5 covers (b); the CLI prompt format is not specified. Implementation choice.

### 10.8 Sprint sub-phase resume not in v3.75 task-side scope
SE-003 ships in the sprint-side sibling release (R2 per release-split). For v3.75 task-side (R1), sub-phase resume is out of scope but RK-15 still applies if any prompt change in sprint happens.

### 10.9 No-PII guarantee for `reason` field
The `reason` free-text field could leak PII or secrets if a user pastes them in the override rationale. Documentation should warn against pasting credentials/PII into `--reason`. Not architecturally enforced.

---

## 11. Stale Documentation Found

### 11.1 SKILL.md "Configuration References" section [CODE-CONTRADICTED]
`SKILL.md:359-365` lists five referenced config files. None exist. This has been a known gap since R7 §5 item 2 and is RK-18 in FINAL-REPORT §7.

### 11.2 task.md vs SKILL.md flag inventory split [Documentation discrepancy]
`task.md:44` says "See protocol skill for full flag reference" but `SKILL.md:37-45` shows only a subset (`--compliance strict|light`, `--skip-compliance`, `--verify auto`). Full inventory lives only in `src/superclaude/core/COMMANDS.md:86-119`. This is R7 §5 item 3 and is not closed in v3.75 scope.

### 11.3 Skill LIGHT/EXEMPT execution sections
As noted in §10.3, `SKILL.md:100-108` documents LIGHT/EXEMPT execution paths, but `task.md:97-98` routes those tiers away from the skill entirely. The skill listings are dead code in steady-state but serve as fallback if the skill is invoked off-protocol.

### 11.4 Tasklist-protocol keyword drift [Inferred]
`sc-tasklist-protocol/SKILL.md:505-575` has wider STRICT keywords (`password, credential, secret, jwt, transaction, query`) than `task.md:69-91`. TU-005 (DEFER to R3) addresses this — v3.75 leaves the drift.

### 11.5 `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel and `--caller task-unified`
Carry-over artifacts from pre-v3.7 naming. Preserved verbatim by RELEASE-SPEC §2.1 pending A-005 validation. Not stale per se — intentionally preserved.

---

## 12. Summary

The post-v3.75 `/sc:task` architecture is a **two-layer split** — a TEXT-ONLY classification command at `src/superclaude/commands/task.md` and an execution skill at `src/superclaude/skills/sc-task-protocol/SKILL.md`. The split is enforced via natural-language instructions, not runtime gatekeepers; the load-bearing contract is the classification header sentinel block.

Routing is tier-based: STRICT and STANDARD invoke the skill; LIGHT and EXEMPT bypass it. The skill enforces tier-specific MCP requirements with **fail-closed circuit-breaker semantics for STRICT** (Sequential + Serena, no fallback) and **fail-open with limitations for STANDARD** (Sequential + Context7, fallback allowed).

The v3.75 release adds three architectural surfaces:

1. **`CriticalFailCondition` dataclass** in a new `audit.py` module (spec-only; not yet implemented) defining three STRICT-only fail conditions: MCP unavailable, output absent, classification header absent.
2. **Daily-rotated JSONL audit log** at `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl` with per-task write locks, timestamp-only cross-task ordering, and a 10-field schema (including tier enum extended to include `BLOCKED`).
3. **TU-004 BLOCKED state** replacing the soft `<0.70 confidence` prompt with a deterministic header value + halt; overridable via `--compliance|--skip-compliance|--force-strict --reason`.

TFEP gates govern test-failure handling for STRICT/STANDARD: pre-existing test failures or ≥3 new failures trigger a three-strike forensic escalation (`/sc:forensic --tier light/standard`, then FULL STOP) with `--caller task-unified` as the canonical-but-deferred-rename identifier (A-005).

Integration surfaces:
- **Sprint CLI** (`cli/sprint/process.py:170`) emits `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` per phase, with sprint context, execution rules, checkpoint instructions, and an `EXIT_RECOMMENDATION` result-file contract.
- **Cleanup-audit CLI** (`cli/cleanup_audit/prompts.py`) emits five sequential `/sc:task` prompts (surface scan → structural → cross-cutting → consolidation → validation) **without `--compliance` flags**, relying on auto-classification.

Dependency graph: command → skill → (audit.py, MCP servers, `/sc:forensic`). Sprint and cleanup-audit are sibling consumers under `cli/`. audit.py is a new node with zero existing dependents.

Five shared assumptions (A-001..A-005) underpin the architecture. The two load-bearing ones are **A-001** (STRICT MCP block correctness) and **A-005** (forensic-caller consumer enumeration unverified). v3.75 explicitly DEFERS the rename of `task-unified` carry-over strings until R3 validates A-005. Tests in RELEASE-SPEC §5.2.5 encode the DEFER lock via SoT constants so the eventual rename is mechanical.

**Status:** Complete
