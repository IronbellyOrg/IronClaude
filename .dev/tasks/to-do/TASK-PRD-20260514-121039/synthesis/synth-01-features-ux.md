# Synthesis 01: Features and UX for /sc:task PRD

**Source research:** 01-features-and-user-flows.md, 03-sprint-and-tui-ux.md
**Template sections covered:** S1, S2, S3, S4, S5 (abbreviated), S6, S7, S12, S13, S16, S19
**Date:** 2026-05-14

> **Scope note — S8 and S9 are N/A in this synth file.** Section 8 (Value Proposition Canvas) and Section 9 (Competitive Analysis) are platform-level concerns; this is a Feature PRD scoped to the v3.75 RigorflowMerger changes against the existing `/sc:task` surface, so per the PRD template's scope notes for feature PRDs, those sections defer to a future Platform PRD. They are not produced here.

> **Verification legend used throughout this file:**
> - **[CODE-VERIFIED]** — claim observed directly in source by upstream research.
> - **[UNVERIFIED]** — RELEASE-SPEC-designed behavior not yet present in source; flagged for S13 Open Questions.
> - **[CODE-CONTRADICTED]** — documentation claim disagrees with source; corrected here.
> - **[inference]** — propagated verbatim from RELEASE-SPEC / FINAL-REPORT where it appears as an explicit `[inference]` tag in the source artifact.

---

## 1. Executive Summary

The `/sc:task` command is the single canonical SuperClaude task-execution surface, with v3.75 RigorflowMerger formalizing five additive behavioral capabilities on top of the existing four-tier compliance classifier (STRICT, STANDARD, LIGHT, EXEMPT) and the eight-flag CLI surface that v3.7 finalized [CODE-VERIFIED `src/superclaude/commands/task.md:1-10`, `core/COMMANDS.md:86-119`]. The release adds a deterministic fifth header state (BLOCKED) for low-confidence classifications, three CRITICAL FAIL conditions for STRICT execution (MCP availability, output presence, header presence), a six-principle quality NFR enforced on STANDARD/STRICT verification, a mandatory completion checklist, and a JSONL-based audit log so override and skip-compliance use becomes measurable for the first time [RELEASE-SPEC §3.3–§3.7].

In parallel, the sprint runtime gains a fail-closed empty-output gate (SE-001), a stable per-task UID with sub-phase resume (SE-002+SE-003), and two reporting-taxonomy enums (SE-004 ExecutionMode, SE-005 GateFailureSeverity), while the Sprint TUI receives a five-fix top-5 wave (P-05 Rich spinner, P-02 elapsed Duration, P-03+P-07 width-aware truncation, P-01 OutputMonitor wired into the per-task path) that transforms the dashboard from "two-jump updates per task with frozen middle" to "continuously animated" — the "fireworks landing" sequenced as P-05 → P-02 → P-03+P-07 → P-01. None of these task-side or runtime-side changes alter the eight-flag surface; the only externally visible surface extension is the additive BLOCKED value in the classification header TIER enum.

Together, the changes resolve four observed gaps: classification ambiguity at confidence <0.70 that currently soft-prompts instead of halting; STRICT executions that today can complete with empty output or a missing classification header undetected; sprint runs that consume soft-passing empty output as success; and per-task TUI updates that render a frozen `MonitorState()` snapshot because no OutputMonitor is started on the dominant code path. The release ships in two sibling streams (R1 task-surface, R2 sprint + TUI) totalling roughly 10–15 dev-days `[inference]`, gated on a 9-item acceptance checklist that includes a mandatory pre-merge LW-source verification for the TU-007 canonical completion-checklist condition list.

**Key Success Metrics:**

| Metric | Target | Source |
|---|---|---|
| Tier classification accuracy | ≥80% | `SKILL.md:349-357` [CODE-VERIFIED] |
| User confusion rate ("which command?") | <10% | `SKILL.md:349-357` [CODE-VERIFIED] |
| `--skip-compliance` usage | <12% | `SKILL.md:349-357` [CODE-VERIFIED] |
| Regression prevention (post-verification bug detection) | ≥85% | `SKILL.md:349-357` [CODE-VERIFIED] |
| STRICT tier overhead | <25% | `SKILL.md:349-357` [CODE-VERIFIED] |
| Sprint regression baseline (pass / fail) | 921 / 57 maintained | RELEASE-SPEC §5.7 / §9 |
| TUI regression baseline | 125/125 maintained | RELEASE-SPEC §5.7 / §9 |
| ClaudeProcess regression baseline | 16/16 maintained | RELEASE-SPEC §5.7 / §9 |

---

## 2. Problem Statement

> **Scope:** Feature PRD — no TAM/SAM/SOM. Market context belongs in a future Platform PRD.

### 2.1 The Core Problem

**The current `/sc:task` surface classifies, verifies, executes, and observes correctly on the happy path, but four operational gaps allow incorrect or invisible outcomes to slip through: ambiguous classifications soft-prompt instead of halting, STRICT executions can finish without enforceable evidence, sprint runs can consume empty output as success, and the TUI's dominant code path renders frozen state during real task work.**

The current state across the four gaps:

- **Classification quality.** Today's classifier emits the header `TIER: [STRICT|STANDARD|LIGHT|EXEMPT]` and, at confidence <0.70, only soft-prompts the user with "Override with `--compliance [tier]`" [CODE-VERIFIED `task.md:91`]. There is no halt — the agent proceeds with a low-confidence pick. RELEASE-SPEC §2.2 estimates that **5–10% of `--compliance auto` users** will encounter such ambiguous cases `[inference]`, which is the user-impact scope of the BLOCKED state being introduced (TU-004).
- **Fail-closed safety on STRICT.** Only one of three intended CRITICAL FAIL conditions is enforced today: required MCP (Sequential or Serena) unavailability blocks STRICT execution [CODE-VERIFIED `SKILL.md:255-263`]. STRICT tasks that finish with empty output or never emit a classification header are not detected today — both are net-new for v3.75 [UNVERIFIED in code, RELEASE-SPEC §3.3].
- **Sprint runtime reliability.** The sprint executor consumes empty output via `gate_passed(output_path, ANTI_INSTINCT_GATE)` [CODE-VERIFIED `cli/sprint/executor.py:820,828`]; while `gate_passed` itself is already fail-closed on empty files [CODE-VERIFIED `cli/pipeline/gates.py:20-39`], RELEASE-SPEC §6.5 implies a separate code path still soft-passes empty output ("sprint runs relying on inconclusive PASS will fail"). The exact soft-pass surface has not been located via the upstream Phase 3 grep [UNVERIFIED — see G1].
- **TUI usability.** The per-task path (the dominant user-visible path; any phase using `### T<PP>.<TT>` headings) updates the TUI exactly twice per task — once at launch (executor.py:980-985) and once at completion (executor.py:1043-1049) — and constructs a fresh empty `MonitorState()` for each update with no `OutputMonitor` running [CODE-VERIFIED]. The user sees frozen activity, frozen Duration (`stall_seconds` not phase-elapsed), and full-width prompts clipped at a hard 60-char cap regardless of terminal width.

**Who is affected:** End users invoking `/sc:task` directly; the sprint executor in `cli/sprint/process.py:170` that prefixes every phase invocation with `/sc:task`; cleanup-audit prompt builders in `cli/cleanup_audit/prompts.py` (five distinct `/sc:task` builders); and the forensic self-handshake (`--caller task-unified` at `SKILL.md:196`).

**Cost of not solving:** Low-confidence misclassification proceeds undetected; STRICT tasks that should fail closed are reported as success; sprint runs report soft passes that mask empty-output regressions; users watching the TUI report apparent hangs because the dashboard does not animate during real work.

**Barriers today:** The audit-log infrastructure required to measure skip-compliance, override patterns, and BLOCKED rates does not exist (`audit.py` is a NEW file in RELEASE-SPEC §3.7 [UNVERIFIED in code]); three of the five live success metrics (`SKILL.md:349-357`) are unmeasurable without it (RELEASE-SPEC RK-04).

### 2.2 Why Existing Solutions Fall Short

**Live v3.7 `/sc:task` (the current baseline):**
- Soft-prompts at confidence <0.70 rather than halting — no audit trail of override decisions.
- No CRITICAL FAIL enforcement for empty STRICT output or missing classification headers.
- No completion checklist; STRICT/STANDARD tasks can return `complete` despite gaps.
- No NFR-style universal quality principles (verifiability, completeness, correctness, consistency, clarity, anti-sycophancy) declared in the skill.

**Live sprint runtime (R2 baseline):**
- The per-task path uses `proc.wait()` inside `_run_task_subprocess` (executor.py:1054-1093), which blocks unconditionally with no stall watchdog — the freeform path's `config.stall_timeout` enforcement at executor.py:1303-1381 does NOT cover the per-task path [CODE-VERIFIED].
- No stable per-task UID — the closest existing identifier is `task.task_id` (e.g. `"T01.01"`); sub-phase resume cannot key off a sortable, zero-padded UID.
- No typed `ExecutionMode` / `GateFailureSeverity` enums; `execution_mode` is a plain string parameter (`config.py:391, :487`).

**Live TUI (top-5 baseline):**
- `STATUS_ICONS[PhaseStatus.RUNNING] = "[yellow]RUNNING[/]"` (tui.py:69) — static markup, no motion.
- Duration column reads `stall_seconds` (tui.py:265-273), the *idle gap since last NDJSON event*, not phase-elapsed wall-clock.
- Truncation is layered and width-blind: `config.py:179, 193, 203, 204` slice to `[:60]` at extraction; `tui.py:386` truncates again at `_LLM_LINE_MAX=60`; `monitor.py:121` caps assistant text at `ASSISTANT_TEXT_MAX_LEN=80`. The renderer never reads `console.width`.
- On the per-task path, `activity_log` is always empty because no `OutputMonitor` is started; the user sees three `—` lines for the entire task.

**Other prior approaches considered and explicitly rejected for v3.75 (RELEASE-SPEC §1.6):**
- Full TU-002 (output-type axis) + TU-005 (SoT YAML) + TU-006 (skill sub-files) in v3.75 — REJECTED (X-001..X-003, 80% confidence).
- Q1 + Q2 renames (sentinel + forensic caller) with telemetry-compat shim — REJECTED pending A-005 forensic-consumer investigation.
- New `--output-type {auto|override}` CLI flag — REJECTED (C-012/X-005, 80% confidence). Flag count stays at 8.
- 3.0.0 major version bump — REJECTED (C-013, 60% confidence). Bump is 2.0.0 → 2.2.0.
- SE-006 auto-diagnostic threshold — REJECTED for v3.75 (X-006, 80% confidence; RK-OOS-3 unresolved).

### 2.3 Why This Feature is Required

This is a feature PRD; market opportunity belongs in a future Platform PRD. The feature-scoped justification is four-fold:

1. **Classification quality.** Replacing the soft-prompt at confidence <0.70 with a deterministic BLOCKED state (TU-004) closes the gap where ambiguous classifications quietly proceed. The user is forced to provide explicit `--reason` justification via one of three override paths (`--compliance <tier>`, `--skip-compliance`, `--force-strict`), and each path writes an audit log entry — making the previously invisible 5–10% `[inference]` ambiguous-classification volume visible and accountable.
2. **Fail-closed safety.** Formalizing three CRITICAL FAIL conditions for STRICT (TU-001) plus the mandatory completion checklist (TU-007) eliminates two scenarios where STRICT executions today complete despite missing evidence: empty output after `max_turns` and absent classification header after first turn. Combined with the six-principle universal NFR (TU-003) enforced on STANDARD/STRICT verification, this raises the verification floor without changing the user-facing surface.
3. **Sprint runtime reliability.** SE-001's fail-closed empty-output gate, paired with SE-002+SE-003's per-task UID and sub-phase resume, makes sprint runs deterministic on retry: a sprint that previously soft-passed on empty output now fails closed, and a sprint that crashes mid-phase can resume by skipping already-completed `task_uid`s rather than re-running the entire phase from scratch.
4. **TUI usability.** The top-5 fixes (P-05 → P-02 → P-03+P-07 → P-01) make the dashboard continuously animated — the "fireworks landing" — so a user watching a long-running phase can immediately distinguish "live and progressing" from "hung." P-01 (the keystone) incidentally fixes the missing per-task stall watchdog by replacing `proc.wait()` with a poll loop, closing a latent bug where a hung per-task subprocess hangs the sprint with no timeout enforcement beyond the subprocess-level `timeout_seconds`.

---

## 3. Background & Strategic Fit

> **Scope:** Feature PRD — no platform-level market trends, no company-revenue framing. Why THIS FEATURE is needed now and what enablers are in place.

### 3.1 Why Now?

1. **v3.7 canonicalization is complete.** The `/sc:task` command surface has stabilized at exactly 8 CLI flags plus the `--reason` qualifier [CODE-VERIFIED `task.md:44`, `core/COMMANDS.md:86-119`], the four-tier classifier with the `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel is locked in source (six paired open/close hits at `task.md:60,66,108,114,119,125,130,136,141,147` [CODE-VERIFIED]), and v3.7's hard constraints (NG-1 through NG-6 in RELEASE-SPEC §1.4) are stable. The surface is in a state where additive behavioral capabilities can land without re-litigating the foundational shape.
2. **task-unified strengths backlog needs reintegration.** v3.7 retired `/sc:task-unified` as a live command but the carry-over naming artifacts (`SC:TASK-UNIFIED:CLASSIFICATION` sentinel, `--caller task-unified` forensic string at `SKILL.md:196`) and the strengths of the unified-protocol design (CRITICAL FAIL conditions, completion checklist, universal NFR) were left as a backlog. RELEASE-SPEC §6 enumerates these as the four task-side additions (TU-001, TU-003, TU-004, TU-007); v3.75 is the first release that explicitly takes ownership of reintegrating them.
3. **Sprint + TUI gaps are blocking observability.** The audit-log infrastructure (Q11) is the prerequisite for measuring three of the five existing success metrics (`SKILL.md:349-357`) — skip rate, regression prevention, STRICT overhead — none of which is measurable today (RELEASE-SPEC RK-04). The TUI's frozen per-task path makes "is the sprint actually running?" a user-perception problem that no telemetry can resolve until the dashboard animates. Both must land together to make the system observable end-to-end.
4. **Regression baselines are precise and inherited.** v3.7 left clean regression numbers (921 sprint pass / 57 fail, 125/125 TUI, 16/16 ClaudeProcess) that R1 and R2 must not regress (RELEASE-SPEC §5.7). The sibling-release structure (R1 task-surface + R2 sprint+TUI shipping in parallel) is feasible *because* the existing test baselines are precise — there is no ambiguity about what "passes" means.

### 3.2 How This Fits Framework Objectives

- **Behavioral integrity.** The five additive task-side capabilities (TU-001, TU-003, TU-004, TU-007, Q11 audit) raise the verification floor on STRICT and STANDARD without touching the surface that v3.7 stabilized. No flag count change. No new compliance tier. No new command name.
- **Observability foundation.** The Q11 audit log (`audit.py` JSONL daily-rotated, append-only, per-task write lock per INV-005) is the first piece of telemetry infrastructure that captures classification + override + escape-hatch use. It is the enabler for future metric work (skip rate, override patterns).
- **Sprint determinism.** SE-001 + SE-002+SE-003 + SE-004 + SE-005 make the sprint runtime deterministic on empty output (fail-closed), resumable on partial completion (sub-phase resume keyed off `f"{phase_id}-{task_index:04d}"`), and machine-typed for reporting (`ExecutionMode`, `GateFailureSeverity` enums).
- **TUI usability.** The top-5 fixes transform the per-task path from broken (frozen `MonitorState()`) to alive (OutputMonitor + spinner + monotonic Duration + width-aware truncation).

### 3.3 Strategic Bets

1. **The carry-over preservation bet.** v3.75 keeps the `SC:TASK-UNIFIED:CLASSIFICATION` sentinel and `--caller task-unified` forensic string verbatim (Q1 / Q2 DEFER-GATED to R3 per RELEASE-SPEC §1.6) — betting that downstream forensic consumers depend on the exact string and that an A-005 investigation must complete before rename. If the bet is wrong, R3 must do a telemetry-compat shim.
2. **The BLOCKED-state bet.** v3.75 replaces the soft-prompt at confidence <0.70 with a deterministic halt — betting that the friction of forcing explicit `--reason` overrides for an estimated 5–10% `[inference]` of `--compliance auto` users is a net positive over the silent low-confidence proceed. If the bet is wrong, the override rate will exceed the <12% skip-compliance target and the audit-log skip-rate metric will trigger a re-evaluation.
3. **The fireworks-landing bet.** TUI top-5 ships in the order P-05 → P-02 → P-03+P-07 → P-01, which means the cosmetic-feeling fixes ship before the structural fix (P-01) — betting that users perceive a polished-but-quiet dashboard as more usable than an animated-but-incomplete one. If the bet is wrong, users will report that the spinner + Duration changes feel cosmetic without the activity-stream wiring P-01 delivers, and the ship order may need to invert.
4. **The deferral bet.** TU-002, TU-005, TU-006, Q1, Q2 are DEFER-GATED to R3; SE-006 is DEFER-GATED to R4 — betting that the v3.75 scope is the right "two-release split" granularity. If the bet is wrong, the R3 backlog accumulates faster than it can be drained and the four-location drift problem (RELEASE-SPEC RK-05, classification logic in `commands/task.md` + `ORCHESTRATOR.md` + `sc-task-protocol/SKILL.md` + `sc-tasklist-protocol/SKILL.md`) becomes a maintenance hazard.

---

## 4. Product Vision

**"A single canonical `/sc:task` surface that classifies every invocation deterministically, fails closed when STRICT evidence is missing, halts when classification is ambiguous, audits every override, and animates the sprint dashboard so users can see real work happening in real time."**

In the future state where v3.75 has shipped, every `/sc:task` invocation produces a classification header as its first output before any tool call, with the TIER value drawn from a five-element enum (STRICT, STANDARD, LIGHT, EXEMPT, BLOCKED). Ambiguous classifications halt deterministically rather than proceeding under low confidence; the user re-invokes explicitly with `--reason` justification and the audit log captures every such decision. STRICT executions cannot finish silently — the absence of output or the absence of a classification header is a CRITICAL FAIL, not a soft pass — and the mandatory completion checklist gates the `complete` status until every condition is satisfied. The sprint runtime reads the same audit-log infrastructure, gates empty output fail-closed, and resumes sub-phase work by skipping already-completed `task_uid`s on retry. Watching a sprint in the TUI, the user sees a spinner cycling on RUNNING phases (P-05), a monotonically increasing Duration counter (P-02), prompts truncated to terminal width rather than a hard 60-char cap (P-03+P-07), and an activity stream that populates in real time as tools run (P-01). The "fireworks landing" is the moment all four cosmetic and structural fixes compose into a continuously animated dashboard — the user-visible outcome that closes the apparent-hang reports.

The vision is conservative: no new commands, no new flags, no new compliance tiers, no semantic-NLP classifier (NG-3), no bash-orchestrator pattern (NG-4). v3.75 is an additive consolidation — the existing four-tier surface plus a deterministic fifth header value plus four behavioral guarantees plus an audit substrate plus a working TUI.

---

## 5. Business Context

> **Scope:** Feature PRD — no TAM/SAM/SOM, no revenue projections, no pricing tiers. Feature-specific business justification only. KPIs are not duplicated here; see **Section 19: Success Metrics & Measurement** for the single source of truth on metrics.

The business case for v3.75 RigorflowMerger is operational, not commercial:

- **Engineering velocity.** The four-location classification-logic drift (`commands/task.md`, `core/ORCHESTRATOR.md`, `sc-task-protocol/SKILL.md`, `sc-tasklist-protocol/SKILL.md`) is a maintenance cost on every tier-enum change; v3.75 does not consolidate it (TU-005 is DEFER-COUPLED to R3) but it does land the audit-log substrate (Q11) that future consolidation can key off. The sub-phase resume (SE-002+SE-003) eliminates wasted compute on sprint retries that today must re-run already-completed tasks.
- **Fail-closed safety.** Three new STRICT CRITICAL FAIL conditions (TU-001) plus the mandatory completion checklist (TU-007) prevent the largest class of silent-success defects: STRICT tasks that report `complete` with empty output or missing headers, sprint runs that consume soft-passing empty output. The user-impact summary at RELEASE-SPEC §6.5 notes "Expected net positive" for both TU-001 and TU-007 — STRICT tasks that previously completed with empty output are "likely buggy completions" `[inference]`.
- **Audit traceability.** The `audit.py` JSONL log (`.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`, append-only, daily rotation, per-task write lock for INV-005) captures classification + override + skip-compliance + force-strict + critical-fail events per task. Three of the five currently-coded success metrics (skip rate <12%, regression prevention ≥85%, STRICT overhead <25%) are unmeasurable today and become measurable once the audit log is deployed. The audit log is the prerequisite for any future business-level conversation about override behavior and tier accuracy.

Forward reference: **all KPIs and measurement methods are consolidated in Section 19 (Success Metrics & Measurement).** This section intentionally does not duplicate them.

---

## 6. Jobs To Be Done (JTBD)

> **Framework:** Format is "When [situation], I want to [motivation], so I can [expected outcome]." Jobs framed against the four observed gaps in §2.1.

### 6.1 Primary Jobs

**Job 1: Get an ambiguous task halted rather than misclassified**
- **When**: I invoke `/sc:task "<ambiguous task>"` with `--compliance auto` and the classifier's max-tier score has confidence <0.70 (a tie between STRICT 0.45 and STANDARD 0.42, for example).
- **I want to**: be halted with a BLOCKED classification header and a clear three-path override menu instead of having the agent proceed under low confidence.
- **So I can**: make an explicit, audited decision about which tier the task belongs in — every override path writes a JSONL audit entry, so my decision is traceable.
- **Current alternatives**: Today the agent soft-prompts ("Override with `--compliance [tier]`") at `task.md:91` and proceeds anyway. There is no halt, no audit, no `--reason` requirement.
- **Pain with alternatives**: An estimated **5–10%** `[inference]` of `--compliance auto` invocations sit in the <0.70-confidence range and proceed under a guess. Misclassifications are invisible until downstream verification fails (or doesn't catch the gap).

**Job 2: Get STRICT tasks to fail loudly instead of completing silently**
- **When**: I invoke `/sc:task "fix security vulnerability"` and one of three failure modes occurs — required MCP (Sequential or Serena) is unavailable, the task finishes after `max_turns` with empty output, or the agent never emitted the mandatory classification header.
- **I want to**: see a CRITICAL FAIL with the specific condition recorded in the audit log instead of a soft pass.
- **So I can**: distinguish "STRICT task succeeded" from "STRICT task ran without enforceable evidence."
- **Current alternatives**: Only the MCP-availability condition is enforced today (`SKILL.md:255-263`). The other two are NOT in source.
- **Pain with alternatives**: STRICT tasks that finish empty or without a header are "likely buggy completions" `[inference]` reported as success.

**Job 3: Run a sprint phase and have it fail closed on empty output**
- **When**: I run `superclaude sprint run` and a phase task emits an empty result file (subprocess crash, no progress, malformed output).
- **I want to**: get a clear `(False, 'empty output file')` failure reason rather than a soft pass.
- **So I can**: distinguish "phase succeeded" from "phase ran with no observable output."
- **Current alternatives**: `gate_passed` is already fail-closed on empty files (`cli/pipeline/gates.py:20-39`), but a separate sprint-side code path soft-passes — exact site UNVERIFIED (G1).
- **Pain with alternatives**: Sprints can report success on phases that produced nothing. Expected post-fix: "1-2 new failures per phase during the first week" per RELEASE-SPEC §6.5.

**Job 4: Resume a crashed sprint mid-phase without re-running completed tasks**
- **When**: A sprint dies after task 3 of 5 in a phase (subprocess crash, `KeyboardInterrupt`, machine reboot).
- **I want to**: re-invoke `superclaude sprint run --start <phase>` and have it skip already-completed `task_uid`s based on a stable, sortable per-task key.
- **So I can**: avoid the wasted compute and time of re-running tasks 1–3 from scratch.
- **Current alternatives**: Re-run the entire phase. There is no `task_uid` field in result files today.
- **Pain with alternatives**: Wasted compute proportional to phase size; risk of side-effect re-execution on tasks 1–3.

**Job 5: Watch a sprint in the TUI and see real-time progress**
- **When**: A sprint is running a phase using `### T<PP>.<TT>` headings (the per-task path, the dominant code path).
- **I want to**: see the RUNNING spinner cycling, the Duration column ticking up monotonically, prompts truncated to my terminal width, and the activity stream populating as tools run.
- **So I can**: distinguish "the sprint is alive and progressing" from "the sprint is hung."
- **Current alternatives**: Status is static markup `[yellow]RUNNING[/]` (tui.py:69); Duration reads `stall_seconds` (the idle gap, not phase-elapsed); prompts clip at hard 60-char cap; activity log is always empty on the per-task path because no `OutputMonitor` runs.
- **Pain with alternatives**: Users report apparent hangs during long-running phases that are in fact progressing.

### 6.2 Related Jobs (the 13 v3.75 features)

| Job (feature) | Frequency | Importance | Satisfaction with Current Solutions |
|---|---|---|---|
| TU-001 — Three CRITICAL FAIL conditions (STRICT) | Per STRICT task | Critical | 2/10 — only condition #1 enforced today |
| TU-003 — Six-principle universal NFR (STANDARD/STRICT verify) | Per verification | High | 1/10 — no NFR in skill today |
| TU-004 — BLOCKED state (5th header tier value) | ~5–10% of `--compliance auto` `[inference]` | Critical | 3/10 — soft-prompt at <0.70 today |
| TU-007 — Mandatory completion checklist | Per STANDARD/STRICT completion | Critical | 1/10 — no checklist coded today |
| Q11 — Audit log infrastructure (`audit.py`) | Per task | Critical | 0/10 — no audit log today |
| SE-001 — Fail-closed empty-output gate | Per phase | High | 4/10 — gate_passed already fail-closed; separate soft-pass surface exists |
| SE-002 + SE-003 — Per-task UID + sub-phase resume (paired) | Per sprint retry | High | 2/10 — no `task_uid` today |
| SE-004 — `ExecutionMode` enum | Per sprint | Medium | 3/10 — plain string today |
| SE-005 — `GateFailureSeverity` enum | Per gate result | Medium | 3/10 — no typed severity today |
| P-05 — Rich spinner on RUNNING + active panel title | Continuous | High | 2/10 — static markup today |
| P-02 — Elapsed-since-phase-start in Duration column | Continuous | High | 2/10 — reads `stall_seconds` today |
| P-03 + P-07 — Width-aware truncation (combined) | Continuous | Medium | 3/10 — hard 60/80 caps today |
| P-01 — OutputMonitor wired into per-task path (keystone) | Continuous | Critical | 1/10 — frozen MonitorState() today |

---

## 7. User Personas

### 7.1 Primary Persona: End User — Direct `/sc:task` Invoker

| Attribute | Details |
|---|---|
| **Demographics** | Developer using Claude Code with SuperClaude installed; varies from solo developer to enterprise contributor. Familiar with `/sc:` slash-command surface. |
| **Goals** | Get a task classified appropriately, execute with the right rigor (STRICT for security/auth/database; LIGHT for typos; EXEMPT for read-only questions), receive honest pass/fail outcomes. |
| **Pain Points** | Today's soft-prompt at confidence <0.70 quietly proceeds; STRICT tasks can complete with empty output; no `--reason` audit; no visibility into how often the classifier picks the wrong tier. |
| **Technical Proficiency** | High — uses CLI, reads classification headers, understands tier semantics. |
| **Budget Authority** | N/A (internal framework feature) |
| **Success Metrics** | Tier classification matches expectation ≥80% (per `SKILL.md:349-357`); user confusion rate <10%; can override deterministically when needed via `--compliance`, `--skip-compliance`, or `--force-strict` paths. |

**Quote:** "TBD"

**A Day in Their Life:** Invokes `/sc:task "fix security vulnerability in auth module"` and expects STRICT classification with the 11-step verification flow. When the classifier is uncertain (BLOCKED), explicitly chooses an override path with `--reason "..."` rather than letting a guess proceed. Reviews the classification header (`TIER`, `CONFIDENCE`, `KEYWORDS`, `OVERRIDE`, `RATIONALE`) on every invocation.

### 7.2 Primary Persona: Sprint Executor (Programmatic `/sc:task` Invoker)

| Attribute | Details |
|---|---|
| **Demographics** | The `cli/sprint/process.py:124,170` `build_prompt` machinery that prefixes every phase-execution Claude call with `/sc:task`. Highest-volume programmatic invoker. |
| **Goals** | Deterministic STRICT compliance on every phase; per-task UID stability for sub-phase resume; fail-closed gate semantics on empty output; checkpoint emission; per-task observability. |
| **Pain Points** | Phase tasks that emit empty output currently soft-pass via an unidentified code path (G1 UNVERIFIED); no `task_uid` field in result files, so sub-phase resume cannot key off a sortable identifier; the per-task path uses `proc.wait()` with no stall watchdog. |
| **Technical Proficiency** | High (it's machine-driven). |
| **Budget Authority** | N/A |
| **Success Metrics** | 921 sprint pass / 57 fail baseline maintained; Wave-4 checkpoint-heading-parser tests pass (RK-15); `TEST-SPEC.md:34-80` (no `/sc:task-unified` in `build_prompt`) holds. |

**Quote:** "TBD"

**A Day in Their Life:** Builds the prompt `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` for each phase. Consumes the gate result `(passed, failure_reason)` from `gate_passed(output_path, ANTI_INSTINCT_GATE)`. Reads result-file `task_uid` fields (post-SE-002+SE-003) to drive sub-phase resume.

### 7.3 Primary Persona: Cleanup-Audit Prompt Builder

| Attribute | Details |
|---|---|
| **Demographics** | The five prompt builders in `cli/cleanup_audit/prompts.py` at lines 26, 47, 69, 92, 116. Each emits a `/sc:task` invocation for a specific analysis stage. |
| **Goals** | Well-defined read-only/analysis behavior (likely EXEMPT or STANDARD tier); consistent output structure across the five stages (surface scan, deep structural analysis, duplication detection, finding consolidation, validation); evidence citations tied to TU-003 Verifiability principle. |
| **Pain Points** | No NFR-style universal quality principles enforced today; verifiability (cite file:line) is a convention, not a contract. Without TU-003, audit findings can include sycophantic verdicts or unverified claims. |
| **Technical Proficiency** | High (machine-driven prompt builder). |
| **Budget Authority** | N/A |
| **Success Metrics** | Each of the five stages produces an output that satisfies the six-principle NFR (verifiability, completeness, correctness, consistency, clarity, anti-sycophancy) — measurable post-TU-003 via the per-row checklist citation field. |

**Quote:** "TBD"

**A Day in Their Life:** Builds five sequential `/sc:task` invocations across an audit pipeline. Expects evidence-bearing output that cites file:line for every claim and is independent of any stated implementer confidence.

### 7.4 Secondary Persona: Forensic Invocation User (Self-Handshake)

| Attribute | Details |
|---|---|
| **Demographics** | The TFEP (Test Failure Escalation Protocol) flow inside `sc-task-protocol/SKILL.md:196` that self-invokes `/sc:forensic --tier {light\|standard} --intent triage --caller task-unified --context ...`. This is a machine handshake, not user-facing. |
| **Goals** | Carry a stable caller string (`task-unified`) into the forensic pipeline so downstream consumers can identify the origin of the forensic invocation. |
| **Pain Points** | The `task-unified` string is a lingering naming artifact preserved verbatim pending A-005 forensic-consumer investigation (Q2 DEFER-GATED to R3). Renaming it without a telemetry-compat plan would break downstream consumers. |
| **Technical Proficiency** | High (machine-driven). |
| **Budget Authority** | N/A |
| **Success Metrics** | The string `--caller task-unified` continues to appear in source as a single hit (grep verification per RELEASE-SPEC §5.5); no R3 rename ships without A-005 resolution. |

**Quote:** "TBD"

**A Day in Their Life:** TFEP triggers a `/sc:forensic` invocation when test failures meet the MUST-escalate criteria (pre-existing test fails, ≥3 simultaneous new test fails, runtime exceptions in implementation code). The first trigger uses `--tier light` (~5–8K tokens), the second `--tier standard` (~15–20K tokens), the third FULL STOPs. v3.75 audit-log captures `skip_compliance` and `force_strict` use but NOT `no_escalation` (gap flagged at G17/G17b — see S13).

### 7.5 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|---|---|
| Users seeking a semantic-NLP classifier | NG-3 in RELEASE-SPEC §1.4 — explicit hard constraint. v3.75 preserves the keyword + booster + compound classifier; no semantic NLP. |
| Users seeking a bash-orchestrator or Python-from-bash pattern | NG-4 in RELEASE-SPEC §1.4 — LW's bash-orchestrator / multi-backup pattern is explicitly out of scope. |
| Users seeking a new `--output-type` flag or a 9th CLI flag | C-012/X-005, 80% confidence rejection in RELEASE-SPEC §1.6. The output-type axis (TU-002) is DEFER-GATED to R3; v3.75 does not foreclose it but does NOT ship it. Flag count stays at 8. |
| Users seeking the resurrected `/sc:task-unified` live command or the `task-unified.md` / `sc-task-unified-protocol/` directories | NG-1 / NG-2 in RELEASE-SPEC §1.4 — v3.7 hard constraint. The carry-over string artifacts are preserved; the command and directory are NOT. |
| Users wanting TypeScript-plugin integration with `/sc:task` | NG-5 — v5.0 scope. |

---

## 12. Scope Definition

### 12.1 In Scope (v3.75 — 13 Features Across R1 + R2)

> **MoSCoW prioritization** is used at the Lightweight tier per the PRD template — RICE is not required.

| Category | Included | MoSCoW | Notes |
|---|---|---|---|
| **R1 task-surface (4 features)** | TU-001 — Three CRITICAL FAIL conditions (STRICT only) | Must | RELEASE-SPEC §3.3; Verdict ADOPT-WITH-DEPRECATION. Only condition #1 (MCP missing) enforced today. |
| | TU-003 — Six-principle universal NFR (STANDARD/STRICT verify) | Must | RELEASE-SPEC §3.4; Verdict ADOPT clean — no break, no flag. |
| | TU-004 — BLOCKED 5th header state + halt + three override paths | Must | RELEASE-SPEC §3.5. ~5–10% `[inference]` `--compliance auto` user impact. |
| | TU-007 — Mandatory completion checklist | Must | RELEASE-SPEC §3.6; Verdict ADOPT-WITH-INVESTIGATION. Pre-merge gate: LW-source canonical-condition-list verification. |
| **Infrastructure (1 feature)** | Q11 — `audit.py` JSONL daily-rotated audit log | Must | RELEASE-SPEC §3.7. NEW file `src/superclaude/skills/sc-task-protocol/audit.py`. INV-005 per-task write lock. |
| **R2 sprint-runtime (5 features)** | SE-001 — Fail-closed empty-output gate (`'empty output file'`) | Must | RELEASE-SPEC §2.2 / §6.5. Soft-pass site UNVERIFIED (G1). |
| | SE-002 + SE-003 — Per-task UID `f"{phase_id}-{task_index:04d}"` + sub-phase resume (paired PR) | Must | RELEASE-SPEC §2.2; ship pair, single artifact. Wave-4 parser tests (+3) are pre-merge gate. |
| | SE-004 — `ExecutionMode` enum (3 values) | Should | RELEASE-SPEC §2.2. Foundation for SE-002+SE-003. PR order: SE-001 → SE-004 → SE-005 → SE-002+SE-003. |
| | SE-005 — `GateFailureSeverity` enum (3 values; TFEP↔severity map) | Should | RELEASE-SPEC §2.2. Reporting-taxonomy only; no behavior change. |
| **R2 TUI top-5 (4 PRs covering 5 fixes)** | P-05 — Rich spinner on RUNNING + active panel title (ships FIRST) | Must | TUI-ADVERSARIAL §2; viability 88. |
| | P-02 — Elapsed-since-phase-start in Duration column | Must | TUI-ADVERSARIAL §3; viability 82. INV-002 dual-writer hazard if shipped before P-01. |
| | P-03 + P-07 — Width-aware truncation (combined PR) | Should | TUI-ADVERSARIAL §3/§5; viability 78/70. INV-004 15-min downstream-consumer audit mandatory pre-merge. |
| | P-01 — OutputMonitor wired into per-task path (keystone, ships LAST) | Must | TUI-ADVERSARIAL §1; viability 92. Mandatory `tests/sprint/test_monitor_reset_between_tasks.py` + new public `OutputMonitor.reset_for_next_task()`. |

**Surface contract — what stays unchanged (RELEASE-SPEC §2.1):**
- Command name `/sc:task`.
- All 8 CLI flags (no new flag this release).
- Strategy axis values (systematic, agile, enterprise, auto).
- Compliance tier values (strict, standard, light, exempt). **Additive:** `BLOCKED` joins as a header *value*, not as a `--compliance` accepted value.
- Verification axis (critical, standard, skip, auto).
- Carry-over strings preserved verbatim: `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`, `--caller task-unified`.

### 12.2 Out of Scope (Deferred)

| Item | Reason | Target Phase |
|---|---|---|
| ❌ TU-002 — output-type axis (`output_type ∈ {code, analysis, documentation, opinion}`) | DEFER-GATED to R3 pending Q3 precedence rule between tier-axis and output-type-axis. RELEASE-SPEC §1.6: REJECTED for v3.75 (X-001). | R3 |
| ❌ TU-005 — SoT YAML (`config/tier-keywords.yaml`) consolidating four-location classifier drift | DEFER-COUPLED to R3 alongside TU-006. RELEASE-SPEC §1.6: REJECTED for v3.75 (X-002). | R3 |
| ❌ TU-006 — Skill sub-files (split monolithic `SKILL.md` into `config/` subdir + sub-files) | DEFER-COUPLED to R3. RELEASE-SPEC §1.6: REJECTED for v3.75 (X-003). Documentation gap S-1: `SKILL.md:359-365` references `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml` which do not exist [CODE-CONTRADICTED]. | R3 |
| ❌ Q1 — Sentinel rename (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` → new name) | DEFER-GATED to R3 pending A-005 forensic-consumer investigation. RELEASE-SPEC §1.6: REJECTED for v3.75 (X-002). | R3 |
| ❌ Q2 — Forensic-caller rename (`--caller task-unified` → new name) | DEFER-GATED to R3 pending A-005. RELEASE-SPEC §1.6: REJECTED for v3.75 (X-002). | R3 |
| ❌ SE-006 — Auto-diagnostic threshold | DEFER-GATED to R4 pending RK-OOS-3 diagnostic-chain hardening. RELEASE-SPEC §1.6: REJECTED for v3.75 (X-006, 80% confidence). | R4 |
| ❌ P-04, P-06, P-08, P-09, P-10 — TUI fixes below the top-5 cut line | Deferred to subsequent TUI waves; viability scores below P-07 (70) threshold. P-10 (heartbeat) is the named mitigation for P-05's false-reassurance-spinner risk. | Future TUI wave |

### 12.3 Permanently Out of Scope

| Item | Reason |
|---|---|
| ❌ Reintroduce `/sc:task-unified` as a live command | NG-1 in RELEASE-SPEC §1.4 — v3.7 hard constraint. |
| ❌ Resurrect `task-unified.md` or `sc-task-unified-protocol/` directories | NG-2 — v3.7 hard constraint. |
| ❌ Replace keyword classifier with semantic NLP | NG-3 — v3.7 hard constraint. |
| ❌ Adopt LW's bash-orchestrator / Python-from-bash / multi-backup patterns | NG-4 — v3.7 hard constraint. |
| ❌ TypeScript plugin work for `/sc:task` | NG-5 — v5.0 scope, not v3.75. |
| ❌ Remove or rename `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel and `--caller task-unified` forensic string without telemetry-compat plan | NG-6 (FINAL-REPORT §1.2). Until A-005 produces a downstream-consumer inventory, renames are out of scope. |
| ❌ New `--output-type {auto\|override}` CLI flag | RELEASE-SPEC §1.6 C-012/X-005 — REJECTED at 80% confidence. Flag count stays at 8 for v3.75 and the explicit decision is "no 9th flag this release." |
| ❌ 3.0.0 major version bump | RELEASE-SPEC §1.6 C-013 — REJECTED at 60% confidence. Bump is 2.0.0 → 2.2.0. |

---

## 13. Open Questions

Sources combined: **RELEASE-SPEC §8 questions** + **`[inference]` tags propagated verbatim from upstream research** + **`UNVERIFIED` claims** flagged from research §Gaps + Phase-3 follow-up gaps from `03-sprint-and-tui-ux.md`.

| # | Question | Owner | Target Date | Status | Resolution |
|---|---|---|---|---|---|
| Q1 | **A-005 forensic-consumer investigation:** which downstream consumers read `--caller task-unified` and the `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel? Blocking gate for Q1/Q2 renames in R3. | TBD | TBD | 🟡 Researching | — |
| Q2 | **Q3 output-type precedence:** when both tier-axis and output-type-axis match, which wins? Blocking gate for TU-002 in R3. | TBD | TBD | 🟡 Researching | — |
| Q3 | **RK-OOS-3 diagnostic-chain hardening:** diagnostic chain must be robust to sprint-context input before SE-006 can ship. Blocking gate for R4. | TBD | TBD | 🟡 Researching | — |
| Q4 | **Confidence threshold (0.70):** currently hard-coded per FINAL-REPORT §3.1 R6 L87; not user-configurable. Should it be? No verdict in RELEASE-SPEC. | TBD | TBD | 🟡 Researching | — |
| Q5 | **`--no-escalation` audit-log capture:** flag voids TFEP per `task.md:48`. RELEASE-SPEC §3.7 JSONL schema lists `skip_compliance` and `force_strict` but NOT `no_escalation`. Should `no_escalation` be captured? `[UNVERIFIED gap]` | TBD | TBD | 🔴 Urgent | — |
| Q6 | **`[inference]` — TU-007 canonical condition count:** working placeholder is 6 conditions. Pre-merge gate requires LW-source verification to confirm or supply the canonical list (5/6/7/8). RELEASE-SPEC §3.6 KNOWN GAP. **NO MERGE until investigation complete.** | TBD | TBD | 🔴 Urgent | — |
| Q7 | **`[inference]` — TU-004 user-impact 5–10%:** estimated `--compliance auto` user share that will encounter BLOCKED. No telemetry backing; Q11 audit log enables future measurement. RELEASE-SPEC §2.2 row TU-004 and §6.5. | TBD | TBD | 🟡 Researching | — |
| Q8 | **`[inference]` — Effort labels S/M/L:** "S ≤0.5d, M 1–3d, L >3d" is convention not measurement throughout FINAL-REPORT §6.1–§6.3. R1 ~3–5 dev-days, R2 ~7–10 dev-days, total ~10–15 dev-days `[inference]` per RELEASE-SPEC §7.1. | TBD | TBD | 🟡 Researching | — |
| Q9 | **`[inference]` — R3 + R4 target windows:** "within 2 release cycles" is soft, not an SLA. RELEASE-SPEC §1.5 + §7.1. | TBD | TBD | 🟡 Researching | — |
| Q10 | **`[inference]` — ADOPT/DEFER/REJECT verdict synthesis:** FINAL-REPORT §6 lead paragraph marks the verdicts themselves as inference where not directly cited from source extracts. | TBD | TBD | 🟡 Researching | — |
| Q11 | **`[UNVERIFIED]` — TU-001 condition #2** (empty STRICT output → FAIL): designed in RELEASE-SPEC §3.3; NOT present in `SKILL.md` today. | TBD | TBD | 🟡 Researching | — |
| Q12 | **`[UNVERIFIED]` — TU-001 condition #3** (missing STRICT header → FAIL): designed in RELEASE-SPEC §3.3; NOT present in `SKILL.md` today. | TBD | TBD | 🟡 Researching | — |
| Q13 | **`[UNVERIFIED]` — TU-003 NFR section in SKILL.md:** six-principle NFR designed in RELEASE-SPEC §3.4; no NFR section currently in `SKILL.md`. | TBD | TBD | 🟡 Researching | — |
| Q14 | **`[UNVERIFIED]` — TU-004 BLOCKED state:** halt + override + audit semantics designed in RELEASE-SPEC §3.5; no BLOCKED handling currently in `task.md` or `SKILL.md`. | TBD | TBD | 🟡 Researching | — |
| Q15 | **`[UNVERIFIED]` — TU-007 completion checklist:** pre-`complete`-status gate designed in RELEASE-SPEC §3.6; no completion checklist currently coded. | TBD | TBD | 🟡 Researching | — |
| Q16 | **`[UNVERIFIED]` — `audit.py` infrastructure:** JSONL schema + concurrency contract designed in RELEASE-SPEC §3.7; file does not exist today. | TBD | TBD | 🟡 Researching | — |
| Q17 | **G1 — SE-001 soft-pass surface (UNVERIFIED):** Phase-3 follow-up grep for `return (True\|False)\|passed = True\|status.*PASS` across `executor.py` filtered for classify/determine_phase/anti_instinct/hook returned **zero matches** — the soft-pass surface is NOT a simple boolean return. Implementation kickoff must trace the actual code path during SE-001 PR scoping. `[inference]` retained. | TBD | TBD | 🔴 Urgent | — |
| Q18 | **G2 — Wave-4 checkpoint-parser tests existence (UNVERIFIED):** whether `tests/sprint/test_checkpoint_parser.py::test_wave4_*` (three tests, RK-15) currently exist. Spec is conditional: SE-002+SE-003 PR author owns authoring them if missing. | TBD | TBD | 🟡 Researching | — |
| Q19 | **G3 — `task_uid` tasklist-drift handling (UNVERIFIED):** if user adds/removes tasks between sprint runs, `task_index` shifts and resume would skip the wrong task. Spec is silent. Mitigation candidates: combine `task_index` with stable content hash, OR detect tasklist drift and force full re-run. | TBD | TBD | 🟡 Researching | — |
| Q20 | **G4 — ANSI escape handling in P-07 (UNVERIFIED):** raw `\x1b[...]` sequences in echoed tool output. TUI-ADVERSARIAL §5 flags but no PR commits to the `Text.from_ansi` mitigation. Implementation kickoff decides: ship P-07 with ANSI passthrough or pre-strip. | TBD | TBD | 🟡 Researching | — |
| Q21 | **G5 — Per-task stall watchdog after P-01 (UNVERIFIED):** freeform path has `config.stall_timeout` enforcement at executor.py:1303–1381; P-01 replaces `proc.wait()` with poll loop but spec doesn't explicitly require porting the stall watchdog. Confirm during P-01 implementation. | TBD | TBD | 🟡 Researching | — |
| Q22 | **G6 — SE-004 / SE-005 enum members (UNVERIFIED):** three values are named in tests (`test_three_values_present`) but not enumerated in spec text. Concrete enum members cannot be listed without reading test specs once authored. | TBD | TBD | 🟡 Researching | — |
| Q23 | **`[CODE-CONTRADICTED]` — SKILL.md references missing config files:** `SKILL.md:359-365` cites `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml` — none exist. TU-006 (DEFER R3) addresses; documentation gap remains for v3.75. | TBD | TBD | 🟢 Resolved (deferred) | TU-006 in R3. |
| Q24 | **S-2 — `task.md:44` flag-reference pointer incomplete:** "See protocol skill for full flag reference" but `SKILL.md:37-45` shows only a subset; full 8-flag inventory lives only in `core/COMMANDS.md:86-119`. Documentation hygiene gap; not addressed in v3.75. | TBD | TBD | 🟢 Acknowledged | Doc gap, not blocking. |
| Q25 | **S-3 — SKILL.md numbering anomaly:** jumps from "0. Classification (Already Performed)" (line 49) to "2. Confidence Display" (line 60) with no Section 1. Stale section numbering. Not addressed in v3.75 spec. | TBD | TBD | 🟢 Acknowledged | Doc gap, not blocking. |
| Q26 | **S-5 — Live skill structural typo:** `task.md:152-163` lists "**Will:**" twice (`:152` and `:159`) before "**Will Not:**" at `:163`. Not flagged by RELEASE-SPEC. | TBD | TBD | 🟢 Acknowledged | Doc gap, not blocking. |

---

## 16. User Experience Requirements

> **Scope:** Feature PRD. **16.1 Onboarding, 16.3 Accessibility, 16.4 Localization are N/A here** — those are platform-level concerns that defer to a future Platform PRD. Only 16.2 Core User Flows is feature-specific.

### 16.1 Onboarding Experience

**N/A — see future Platform PRD.** Onboarding for `/sc:task` is part of the SuperClaude framework installation flow (`pipx install superclaude && superclaude install`) and the broader `/sc:` slash-command surface, which is platform-level.

### 16.2 Core User Flows

The feature-specific flows cover (a) the per-tier invocation flow for each of the five header values STRICT, STANDARD, LIGHT, EXEMPT, BLOCKED; (b) the sprint-emitted invocation flow; (c) the cleanup-audit invocation flow; (d) the TUI interaction flow. Steps are CODE-VERIFIED against `task.md`, `SKILL.md`, `ORCHESTRATOR.md`, `cli/sprint/`, and `cli/cleanup_audit/` unless flagged otherwise.

| Flow | Steps | Success Criteria |
|---|---|---|
| **F1 — EXEMPT per-tier invocation** | 1. User invokes `/sc:task "explain how the routing middleware works"`. 2. Agent emits classification header inline (`TIER: EXEMPT`, e.g. CONFIDENCE 0.92, KEYWORDS "explain, how"). 3. Agent executes immediately — answers question or performs read-only op. 4. No Skill invocation; no verification overhead; zero compliance tokens spent. | Header is FIRST output; Skill is NOT invoked; user receives answer directly. [CODE-VERIFIED `task.md:97`, `SKILL.md:106-108`] |
| **F2 — LIGHT per-tier invocation** | 1. User invokes `/sc:task "fix typo in error message"`. 2. Agent emits `TIER: LIGHT`, e.g. CONFIDENCE 0.95, KEYWORDS "typo, fix". 3. Agent executes change directly: quick scope check (files/lines within bounds) → make changes → quick sanity check (syntax valid) → proceed with judgment. 4. No Skill invocation; no verification. | Header is FIRST output; Skill is NOT invoked; change is applied with quick sanity check. [CODE-VERIFIED `task.md:98`, `SKILL.md:100-104`] |
| **F3 — STANDARD per-tier invocation** | 1. User invokes `/sc:task "add pagination to user list endpoint"`. 2. Agent emits `TIER: STANDARD`, e.g. CONFIDENCE 0.85, KEYWORDS "add, endpoint". 3. Agent invokes `Skill sc:task-protocol`. 4. Skill executes 5-step STANDARD flow: load context via codebase-retrieval → search downstream impacts → make changes → run affected tests OR document manual verification → verify basic functionality. 5. Verification: direct test execution (300–500 tokens, 30s timeout). 6. MCP: Sequential + Context7 (fallback allowed). | Header is FIRST output; Skill IS invoked; verification is direct test; six-principle NFR (TU-003, post-v3.75) applies. [CODE-VERIFIED `task.md:99-100`, `SKILL.md:93-99,114-119,255-263`] |
| **F4 — STRICT per-tier invocation** | 1. User invokes `/sc:task "fix security vulnerability in auth module"`. 2. Agent emits `TIER: STRICT`, e.g. CONFIDENCE 0.95, KEYWORDS "security, vulnerability, auth". 3. Agent invokes `Skill sc:task-protocol`. 4. Skill executes 11-step STRICT flow: activate_project → verify git clean → load codebase context → check memories → identify affected files → make changes with checklist → identify importing files → update them → spawn verification agent (quality-engineer) → run `pytest [path] -v` → answer adversarial questions. 5. Verification: sub-agent (quality-engineer), 3–5K tokens, 60s timeout. 6. MCP: Sequential + Serena, **fallback NOT allowed** — block if unavailable (TU-001 condition #1). 7. Critical Path Override: `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always trigger CRITICAL verification regardless of computed tier. 8. Post-v3.75: TU-001 condition #2 (empty output after max_turns → FAIL), condition #3 (missing header after first turn → FAIL), TU-003 NFR, TU-007 completion checklist all enforced. | Header is FIRST output; Skill IS invoked; 11-step flow executes; sub-agent verification runs; TU-001/003/007 gates enforced. [CODE-VERIFIED `task.md:99-100`, `SKILL.md:80-91,114-119,121-123,255-263`] |
| **F5 — BLOCKED per-tier invocation (NEW — TU-004)** | 1. User invokes `/sc:task "<ambiguous task>"`. 2. Classifier computes max_tier_score with confidence <0.70 (e.g. STRICT 0.45 vs STANDARD 0.42 — within 0.1 tie band). 3. Agent emits header with `TIER: BLOCKED`, computed CONFIDENCE, comma-separated split-keywords, RATIONALE = "split between STRICT (0.45) and STANDARD (0.42)". 4. **Execution halts.** `Skill sc:task-protocol` is NOT invoked. 5. Audit log entry written via `audit.py`. 6. User must re-invoke explicitly using one of three override paths, each requiring `--reason "..."`: (a) `/sc:task "..." --compliance <tier> --reason "..."`; (b) `/sc:task "..." --skip-compliance --reason "..."`; (c) `/sc:task "..." --force-strict --reason "..."`. 7. Tasks initiated **before** TU-004 deployment continue under their original classification — no in-flight reclassification. | Header is FIRST output with `TIER: BLOCKED`; Skill NOT invoked; audit log entry exists; user receives clear three-path override menu; re-invocation with `--reason` proceeds under chosen tier. [UNVERIFIED in code; per RELEASE-SPEC §2.4, §3.5] |
| **F6 — Override-initiated invocation** | 1. User invokes `/sc:task "update config file" --compliance strict`. 2. Agent emits header `TIER: STRICT, OVERRIDE: true` (decision tree step_1, 100% confidence per ORCHESTRATOR.md:158-160). 3. Override bypasses keyword scoring. 4. Skill executes the chosen tier's flow. 5. Post-v3.75: audit log captures `user_override_tier`. | Header has `OVERRIDE: true`; keyword scoring is bypassed; tier flow executes per the override choice; audit entry written. [CODE-VERIFIED `task.md:44`, `SKILL.md:326-332`, ORCHESTRATOR.md:158-160] |
| **F7 — Sprint-emitted invocation** | 1. `cli/sprint/process.py:124,170` `build_prompt` prefixes `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` for each phase. 2. Phase invocation reaches `/sc:task` with explicit STRICT override (F6 semantics). 3. Skill executes 11-step STRICT flow. 4. Output written to result file; `gate_passed(output_path, ANTI_INSTINCT_GATE)` evaluates `(passed, failure_reason)`. 5. Post-SE-001: empty output → `(False, 'empty output file')` (literal string). 6. Post-SE-002+SE-003: result file includes `task_uid = f"{phase_id}-{task_index:04d}"`; sub-phase resume reads completed UIDs on `--start <phase>` re-invocation and skips them. 7. Per-task TUI updates: before launch (executor.py:980-985) and after completion (executor.py:1043-1049). | Phase invocation classified STRICT via override; gate result is honest pass/fail; sub-phase resume skips completed UIDs; per-task TUI advances at task boundaries. [CODE-VERIFIED `cli/sprint/process.py:124,170`, `cli/sprint/executor.py:820,828,913-1051`, `cli/pipeline/gates.py:20-39`] |
| **F8 — Cleanup-audit invocation (5 builders)** | 1. `cli/cleanup_audit/prompts.py` emits one of five `/sc:task` invocations: (L26) surface-level scan; (L47) deep structural analysis; (L69) duplication/sprawl/consolidation detection; (L92) findings consolidation; (L116) findings validation by spot-checking claims. 2. Each invocation classifies (likely EXEMPT for read-only analysis or STANDARD for synthesis). 3. Skill executes per-tier flow. 4. Post-TU-003: six-principle NFR enforced on STANDARD verifications — every claim cites file:line; verdicts independent of stated confidence; per-row checklist with citation field. | Each of the 5 stages produces evidence-bearing output; TU-003 NFR satisfied; audit log captures classification per stage. [CODE-VERIFIED `cli/cleanup_audit/prompts.py:26,47,69,92,116`] |
| **F9 — TUI interaction flow (post-top-5)** | 1. User runs `superclaude sprint run <tasklist-index.md>`. 2. TUI launches via `Live(self._render(), refresh_per_second=2)` (tui.py:101-106). 3. Phase status cell on RUNNING shows `Spinner("dots", text="RUNNING", style="yellow")` (P-05); active panel title also spins (`Spinner("dots2")`). Spinner cycles every Rich.Live tick (500 ms) independent of executor pushes. 4. Duration column reads `f"{int(time.monotonic() - self.monitor_state.phase_started_at)}s"` (P-02) — monotonically increasing wall-clock elapsed. 5. Prompt: and Agent: lines truncate to `avail = max(40, console.width - 14)` (P-03 render-time width budget); monitor stores up to 240/400 chars (P-07 raises caps; trim moved to render-time). 6. Per-task path: `OutputMonitor` is instantiated once per phase, `monitor.reset_for_next_task()` called between tasks (NEW public method, P-01); per-task poll loop `while proc._process.poll() is None: tui.update(...); time.sleep(0.5)` replaces `proc.wait()`. Activity stream populates in real time; thinking indicator appears between tool calls; growth_rate_bps is nonzero. 7. "Fireworks landing" sequence: P-05 ships Day 1 → spinner alive; P-02 Day 2 → Duration ticks correctly; P-03+P-07 Day 2.5 → full-width prompt and agent lines; P-01 Days 3–5 → activity stream + Tasks-bar advancement at task boundaries. | Spinner cycles within 2s of sprint start; Duration ticks monotonically and matches wall-clock ±1s; on 200-column terminal Prompt: line displays text wider than 60 chars AND Agent: line wider than 80 chars; 3-task per-task phase shows Tasks bar advancing at task boundaries (not in one jump); Activity log shows ≥1 event per task; NDJSON event count from file matches TUI-displayed count within 1, across phase boundaries (INV-001/005 invariant). [CODE-VERIFIED change sites in `tui.py:34,58-72,80,101-106,221,265-273,360,386-387,408-412,424,459,539`; `monitor.py:117,119,121,121,291-308,466-467`; `config.py:167-204,179,193,203,204`; `executor.py:913-1051,980-985,1043-1049,1054-1093,1234,1239,1266-1390,1271-1390,1276-1277,1303-1381`. P-01/P-02/P-03/P-05/P-07 are UNVERIFIED as implemented — all are planned per RELEASE-SPEC R2 / TUI-ADVERSARIAL.] |

### 16.3 Accessibility Requirements

**N/A — see future Platform PRD.** Accessibility (WCAG compliance, keyboard navigation, screen reader support, color contrast) is a platform-level concern that applies to the SuperClaude framework as a whole, not specifically to `/sc:task`. The TUI is a terminal-based interface inheriting Rich's accessibility characteristics; Platform PRD owns the requirement set.

### 16.4 Localization Requirements

**N/A — see future Platform PRD.** Localization for `/sc:task` (and SuperClaude commands generally) is platform-scoped. Classification headers, audit log fields, and error messages are English-only in v3.75; localization decisions belong in the Platform PRD.

---

## 19. Success Metrics & Measurement

Consolidated single source of truth for all v3.75 KPIs. Metrics are grouped into the categories named in the task brief: classification accuracy, fail-closed coverage, audit log completeness, TUI rendering latency, BLOCKED-state recovery rate, regression test pass rate vs baseline.

| Category | KPI | Target | Measurement Method |
|---|---|---|---|
| **Classification accuracy** | Tier classification accuracy (user-judged appropriateness) | ≥80% | User feedback signals + override/correction rate from `audit.py` JSONL log. Inherited from `SKILL.md:349-357` [CODE-VERIFIED]. |
| **Classification accuracy** | User confusion rate ("which command?" questions) | <10% | Inherited from `SKILL.md:349-357` [CODE-VERIFIED]; measured via user feedback signals. |
| **Classification accuracy** | Classifier confidence ≥0.70 share | Track baseline | `audit.py` JSONL `confidence` field per entry; the complement of this is the BLOCKED rate (see below). |
| **Fail-closed coverage** | TU-001 CRITICAL FAIL conditions enforced (count of 3) | 3 of 3 for STRICT | Condition #1 (MCP missing) already enforced [CODE-VERIFIED `SKILL.md:255-263`]; condition #2 (empty output after max_turns) and #3 (missing header after first turn) net-new for v3.75 [UNVERIFIED in code]. Test files: `tests/skills/test_task_critical_fail_conditions.py` (parameterized per condition). |
| **Fail-closed coverage** | TU-007 completion-checklist enforcement | 100% of STANDARD/STRICT `complete` claims gated by canonical condition list | Test file: `tests/skills/test_task_completion_checklist.py` parameterized over canonical list from `docs/tu-007-completion-checklist-verification.md`. Canonical condition count is `[inference]` pending LW-source verification (Q6). |
| **Fail-closed coverage** | SE-001 empty-output gate fail-closed | `(False, 'empty output file')` literal returned for empty result files; soft-pass site closed | Test file: `tests/sprint/test_gate_passed_empty_output.py::test_empty_output_returns_false` (currently does not exist; spec-mandated NEW file). Implementation kickoff must trace the actual soft-pass code path (Q17 / G1). |
| **Fail-closed coverage** | Six-principle NFR (TU-003) compliance on STANDARD/STRICT verification | 100% verification artifacts contain checklist with citation field per row, naming the six principles | Audit log captures checklist completeness; per-row citation field enforced via prompt + verification-artifact template. |
| **Audit log completeness** | `audit.py` JSONL entry per task lifecycle | 1 entry per task minimum; additional entries for override paths and CRITICAL FAIL events | Persistence to `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`; append-only; daily rotation. Schema fields: `ts, task_id, tier, confidence, user_override_tier, skip_compliance, force_strict, reason, critical_fail`. Concurrency: per-task write lock (INV-005 mitigation). Coverage requirement: **100% line coverage on `audit.py`** per RELEASE-SPEC §5.7 (security-sensitive write path). |
| **Audit log completeness** | `--skip-compliance` use rate (now measurable) | <12% | Inherited from `SKILL.md:349-357` [CODE-VERIFIED]; previously unmeasurable per RELEASE-SPEC RK-04. |
| **Audit log completeness** | Override path coverage (`--compliance <tier>`, `--skip-compliance`, `--force-strict`) | 100% override invocations write audit entry | JSONL field presence: at least one of `user_override_tier`, `skip_compliance`, `force_strict` is truthy when override path taken; `reason` is non-null when any override is taken (RELEASE-SPEC §3.5). |
| **Audit log completeness** | Coverage gap — `--no-escalation` capture | TBD per Q5 | `--no-escalation` voids TFEP per `task.md:48` but is NOT in the JSONL schema as listed in RELEASE-SPEC §3.7. Resolve before R1 ships (Q5 in S13). |
| **TUI rendering latency** | Live refresh cadence | 2 Hz (`refresh_per_second=2`) maintained | `tui.py:101-106` [CODE-VERIFIED]. Spinner and Duration ride this cadence. |
| **TUI rendering latency** | Per-task TUI update latency (P-01 poll loop) | `tui.update(...)` invoked at minimum every 500 ms during per-task subprocess execution | P-01 replaces `proc.wait()` with `while proc._process.poll() is None: tui.update(sprint_result, monitor.state, phase); time.sleep(0.5)`. Acceptance: NDJSON event count from the file matches TUI-displayed count within 1, across phase boundaries (INV-001/005). |
| **TUI rendering latency** | Spinner visibility delay after sprint start (P-05) | <2s | TUI-ADVERSARIAL §2 acceptance: "Within 2 s of sprint start, RUNNING row's status cell shows a visible cycling glyph." |
| **TUI rendering latency** | Duration column accuracy (P-02) | Ticks up monotonically every second; matches wall-clock ±1s after phase ends; never decreases | TUI-ADVERSARIAL §3 acceptance. Underlying source: `phase_started_at` from `MonitorState` (models.py:610). Caveat: INV-002 dual-writer hazard if P-02 ships before P-01 — paired or wired from TUI side via `time.monotonic()`. |
| **TUI rendering latency** | Width-aware truncation (P-03+P-07) | At terminal width 200, Prompt: displays >60 chars AND Agent: displays >80 chars; resizing mid-sprint reflows next render; no panel-height flicker | TUI-ADVERSARIAL §3 / §5 acceptance. Caps: render-time `avail = max(40, console.width - 14)`; extraction-time cap raised from 60 to 240; monitor cap raised from 80 to 400 (or removed). INV-004 15-min downstream-consumer audit mandatory pre-merge. |
| **BLOCKED-state recovery rate** | BLOCKED-classification rate on `--compliance auto` invocations | Track against `[inference]` estimate of 5–10% per RELEASE-SPEC §2.2 row TU-004 / §6.5 (Q7) | `audit.py` JSONL: count entries where `tier == "BLOCKED"` divided by total `--compliance auto` invocations. Establishes baseline post-deploy. |
| **BLOCKED-state recovery rate** | BLOCKED → resolved (via override) rate | TBD baseline (no current target) | `audit.py` JSONL: count BLOCKED entries followed by re-invocation with one of (`user_override_tier`, `skip_compliance`, `force_strict`) within session. |
| **BLOCKED-state recovery rate** | BLOCKED → abandoned (no follow-up override) rate | TBD baseline (signal for classifier improvement) | Complement of resolved rate; if high, indicates classifier is producing BLOCKED on tasks users abandon — potential signal for tier-keyword refinement in R3 (TU-005). |
| **Regression test pass rate vs baseline** | Sprint regression baseline | 921 passed / 57 failed maintained | RELEASE-SPEC §5.7 / §9. New failures introduced by R2 must be net-new (not pre-existing). |
| **Regression test pass rate vs baseline** | TUI Waves 1-2 + tmux + summarizer + retrospective | 125/125 pass maintained | RELEASE-SPEC §5.7 / §9. Must remain 125/125 after the top-5 land. |
| **Regression test pass rate vs baseline** | `test_process.py::TestClaudeProcess` | 16/16 maintained, including `test_build_prompt_contains_task_command` | RELEASE-SPEC §5.7 / §9. Guarantees `/sc:task-unified` does NOT reappear in `build_prompt` (`TEST-SPEC.md:34-80`). |
| **Regression test pass rate vs baseline** | Wave-4 checkpoint-heading-parser tests | +3 tests pass (RK-15): `test_wave4_task_checkpoint_heading_form`, `test_wave4_legacy_heading_back_compat`, `test_wave4_checkpoint_manifest_uses_label_not_basename` | RELEASE-SPEC §5.7 / §9. Hard pre-merge gate for SE-002+SE-003 PR (author tests if missing — see Q18 / G2). |
| **Regression test pass rate vs baseline** | STRICT tier overhead | <25% | Inherited from `SKILL.md:349-357` [CODE-VERIFIED]; previously unmeasurable per RELEASE-SPEC RK-04; becomes measurable with `audit.py` JSONL `tier` field timing data. |
| **Regression test pass rate vs baseline** | Regression prevention (post-verification bug detection) | ≥85% | Inherited from `SKILL.md:349-357` [CODE-VERIFIED]; previously unmeasurable per RELEASE-SPEC RK-04. |
| **Coverage** | New-code line coverage (TU-001, TU-003, TU-004, TU-007, audit.py, SE-001..005) | 80% | RELEASE-SPEC §5.7. |
| **Coverage** | `audit.py` line coverage | **100%** | RELEASE-SPEC §5.7. Security-sensitive write path. |
| **Coverage** | Canonical-form-agnostic preservation tests | Existence checks only; no coverage requirement | RELEASE-SPEC §5.7. |
| **Convergence + invariant gates** | Adversarial pipeline convergence | 86.8% (CONVERGED) | RELEASE-SPEC §9 acceptance item 9. |
| **Convergence + invariant gates** | HIGH-severity UNADDRESSED invariant probe findings | 0 | RELEASE-SPEC §9 acceptance item 9. |

**User-facing impact summary (RELEASE-SPEC §6.5) cross-referenced into metrics:**

| Change | What users see | Mitigation |
|---|---|---|
| TU-004 BLOCKED | Tasks with ambiguous keyword classification (~5–10% of historical traffic, `[inference]`) halt where they previously auto-classified. | Release notes call this out; `--compliance auto` users see the change first. Error message points to `--compliance <tier> --reason "..."`, `--skip-compliance --reason "..."`, or `--force-strict --reason "..."`. |
| TU-001 STRICT output absent | STRICT tasks that previously completed with empty output (likely buggy completions `[inference]`) now FAIL. | Expected net positive; users with legitimate "no-output" STRICT tasks should reclassify to EXEMPT. |
| TU-007 completion checklist | STRICT/STANDARD tasks that previously returned `complete` despite gaps now block. | Expected net positive; canonical condition list in release notes (pending Q6 / TU-007 LW-source verification). |
| SE-001 empty output gate | Sprint runs that previously soft-passed on empty output now fail-closed. | Sprint owners should expect 1–2 new failures per phase during the first week; classify each as pre-existing or net-new. |

---

**End of synthesis-01-features-ux.md.**

Coverage:
- S1 Executive Summary (with Key Success Metrics table) ✅
- S2 Problem Statement (Feature-PRD scoped; "Why This Feature is Required" instead of TAM/SAM/SOM) ✅
- S3 Background & Strategic Fit (Feature-PRD scoped) ✅
- S4 Product Vision (one-sentence vision + expansion) ✅
- S5 Business Context (abbreviated; forward-references S19) ✅
- S6 JTBD (5 primary jobs + related-jobs table for 13 features) ✅
- S7 User Personas (3 primary + 1 secondary + anti-personas; TBD for quotes) ✅
- S12 Scope Definition (In Scope = 13 features with MoSCoW; Out of Scope = deferred items; Permanently Out of Scope = NG-1..NG-6 + flag/version rejections) ✅
- S13 Open Questions (26 questions covering RELEASE-SPEC §8 + propagated `[inference]` + `UNVERIFIED` + `CODE-CONTRADICTED`) ✅
- S16 UX Requirements (16.1/16.3/16.4 N/A with rationale; 16.2 = 9 core user flows F1–F9) ✅
- S19 Success Metrics (full table covering all task-brief categories + acceptance gates + user-facing impact summary) ✅
- S8, S9 N/A (rationale noted at file top) ✅









