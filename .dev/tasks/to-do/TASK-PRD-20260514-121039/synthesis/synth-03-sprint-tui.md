# Synthesis 03: Sprint Runtime + TUI UX for /sc:task PRD

**Source research:** 03-sprint-and-tui-ux.md, 02-architecture-and-integration.md
**Template sections covered:** S21 (all subsections), S23, S24 (S22 and S25 SKIPPED per Lightweight tier)
**Date:** 2026-05-14

---

## Skipped Sections (Lightweight Tier Rationale)

Per the PRD template's Tiered Usage table (Lightweight = single-feature PRD, <10 sections), the following template sections are **intentionally not produced** in this synthesis:

- **S22 Customer Journey Map** — Skipped at Lightweight tier. The /sc:task feature is an internal developer-facing command, not a multi-stage customer-acquisition product; awareness/consideration/acquisition/onboarding stages do not apply. Core developer interaction flow is captured in S24 (User Interaction & Design) and in the upstream S16.2 Core User Flows synthesis.
- **S25 API Contract Examples** — Skipped at Lightweight tier. /sc:task does not expose an HTTP/REST API surface; its "contracts" are CLI prompt strings (sprint `build_prompt()` at `src/superclaude/cli/sprint/process.py:170-171` and the five cleanup-audit builders in `src/superclaude/cli/cleanup_audit/prompts.py`), the classification header sentinel block, and the JSONL audit-log schema — all of which are documented in upstream synth files (synth-01 audit, synth-02 architecture).

---

## S21. Implementation Plan

> This section consolidates the full delivery plan for the v3.75 sprint-runtime + TUI work-stream (R2): what to build (epics, stories, requirements), how to phase it across R1/R2, what "done" means, and when it lands. Read top to bottom for the complete implementation picture.

### S21.1 Epics, Features & Stories

> **Format:** Each epic contains user stories in the format: "As a [persona], I want [goal] so that [benefit]" with testable acceptance criteria.

#### S21.1.1 Epic Summary

The 13 v3.75 features map into **4 epics**:

| Epic # | Epic Name | Features | Stories | Priority | Phase |
|--------|-----------|----------|---------|----------|-------|
| 1 | Sprint Gate Hardening & Resume | SE-001, SE-002, SE-003 | US-1.1, US-1.2, US-1.3 | P0 | R2 |
| 2 | Sprint Typed Taxonomy | SE-004, SE-005 | US-2.1, US-2.2 | P1 | R2 |
| 3 | TUI Liveness & Cosmetic Fixes | P-05, P-02, P-03, P-07 | US-3.1, US-3.2, US-3.3 | P0 (P-05/P-02), P1 (P-03+P-07) | R2 |
| 4 | TUI Per-Task Activation (Keystone) | P-01 | US-4.1 | P0 | R2 (ships last) |

**Cross-reference to R1 features (out of scope for this synth file but listed for completeness — task-surface epics covered in synth-01/synth-02):** TU-001 (CRITICAL FAIL audit), TU-003 (universal quality principles), TU-004 (BLOCKED state), TU-007 (carry-over preservation). R1 totals 4 features; R2 totals 9 features (5 SE-* + 4 TUI top-five with P-03/P-07 paired as a single combined PR but counted as separate features). Total: 13. [CODE-VERIFIED RELEASE-SPEC.md:49–53, :604–613]

---

#### Epic 1: Sprint Gate Hardening & Resume (R2)

**Description:** Harden the sprint executor's failure-gate surface (SE-001) and add a stable per-task identifier + sub-phase resume pairing (SE-002+SE-003) so users get clearer failure reasons and faster re-invocations after partial progress. SE-002 and SE-003 ship as a paired PR per RELEASE-SPEC.md:607.

---

**US-1.1: Fail-closed empty-output gate**

- **As a** sprint owner running phase-by-phase Claude sub-agents
- **I want** an empty output file to deterministically fail with the literal reason `'empty output file'`
- **So that** runs that previously "succeeded with no output" surface as failures I can investigate, instead of soft-passing

**Acceptance Criteria:**

- ✅ `gate_passed()` in `src/superclaude/cli/pipeline/gates.py` (currently lines 20–39) returns `(False, 'empty output file')` on zero-byte output files [CODE-VERIFIED current literal is `f"File empty (0 bytes): {output_file}"` at line 39 — must change to spec literal]
- ✅ The soft-pass surface elsewhere in `src/superclaude/cli/sprint/executor.py` is found and closed (likely candidates: `_classify_from_result_file` at line 1683, `_determine_phase_status` at line 1976, or the anti-instinct hook short-circuit at line 828 — exact site to be confirmed during PR scoping) [inference]
- ✅ `tests/sprint/test_gate_passed_empty_output.py::test_empty_output_returns_false` is authored and passes [CODE-VERIFIED file does not yet exist]
- ✅ Sprint suite delta is at most +1 to +2 new failures per phase during the first week (per RELEASE-SPEC.md:554 user-impact estimate)

**Success Metrics:**

- New-failure surfacing rate: 1–2 net-new failures per phase during the first week of R2 release [CODE-VERIFIED RELEASE-SPEC §6.5]
- Zero regressions in the existing 921-passed sprint baseline (RELEASE-SPEC.md:473–474)

---

**US-1.2: Per-task stable UID**

- **As a** sprint executor (the system, on behalf of the user)
- **I want** each per-task launch to compute and persist a stable UID of the form `f"{phase_id}-{task_index:04d}"` into the result file
- **So that** sub-phase resume (US-1.3) and downstream parsers have a phase-scoped, zero-padded, sortable identifier separate from `TaskEntry.task_id`

**Acceptance Criteria:**

- ✅ `execute_phase_tasks` in `src/superclaude/cli/sprint/executor.py:913–1051` writes `task_uid = f"{phase_id}-{task_index:04d}"` into each `TaskResult`
- ✅ The UID is **distinct from** `TaskEntry.task_id` (which is the user-facing `"T01.01"` form) — both are persisted [CODE-VERIFIED no `task_uid` symbol exists in `src/superclaude/cli/sprint/` today]
- ✅ Legacy result files without `task_uid` are accepted without error (graceful fallback per RELEASE-SPEC Q10 (a))
- ✅ `tests/sprint/test_task_uid.py` is authored and passes
- ✅ Lands **after** SE-004 ExecutionMode per RELEASE-SPEC.md:607 dependency

**Success Metrics:**

- 100% of new result files contain `task_uid` field
- Zero legacy-result-file load failures in regression suite

---

**US-1.3: Sub-phase resume via task_uid**

- **As a** sprint owner re-invoking a sprint with `--start <phase>` after a partial run
- **I want** completed tasks (identified by `task_uid` in the result file) to be skipped automatically
- **So that** I don't re-pay token cost or rerun deterministic work on resumption

**Acceptance Criteria:**

- ✅ On re-invocation, the executor reads the result file, builds the set of completed `task_uid`s, and skips them
- ✅ Mid-task crash (subprocess crash, `KeyboardInterrupt`) leaves the partial Nth task entry without a finish timestamp — resume logic treats it as not-done and re-launches [behavior implied by RELEASE-SPEC §2.2; mitigation captured in S23]
- ✅ Tasklist-drift edge case (user inserts a task at position 3 between runs, shifting indices) — escalated to S23 / Open Questions per research file G3 [inference] — minimum bar: resume produces a clearly-logged warning OR forces full re-run; resume MUST NOT silently skip the wrong task
- ✅ `tests/sprint/test_subphase_resume.py` is authored and passes
- ✅ Wave-4 checkpoint-heading-parser tests (RK-15, +3 tests in `tests/sprint/test_checkpoint_parser.py::test_wave4_*` per RELEASE-SPEC.md:480) all pass; if not present in repo, MUST be authored as part of this PR

**Success Metrics:**

- Resume time delta: re-run of an already-completed phase short-circuits to "0 tasks executed, N skipped" within seconds (no LLM cost)
- Zero false-skips on the regression suite (tasklist-drift detection must catch all reshuffles)

---

#### Epic 2: Sprint Typed Taxonomy (R2)

**Description:** Promote two existing string/conceptual surfaces to typed enums so SE-002+SE-003 have a stable foundation (SE-004) and so reporting/audit downstream consumers can switch on severity (SE-005). Pure-additive; no behavior change.

---

**US-2.1: ExecutionMode enum**

- **As a** sprint codebase author
- **I want** the current `execution_mode: str` parameter (default `"claude"`, used at `src/superclaude/cli/sprint/config.py:391` and `:487`) replaced by a typed `ExecutionMode` enum
- **So that** SE-002+SE-003's per-task UID logic and the wider Wave-4 codepath have a typed contract instead of a string

**Acceptance Criteria:**

- ✅ A new `ExecutionMode` enum is defined with three values [CODE-VERIFIED test name `test_three_values_present`; exact member names are spec-deferred per research G6 — to be enumerated in the PR]
- ✅ All existing `execution_mode="claude"` call sites in `src/superclaude/cli/sprint/config.py` and downstream consumers continue to work (backward-compat string→enum coercion at entry points)
- ✅ `tests/sprint/test_execution_mode_enum.py::test_three_values_present` passes
- ✅ Lands **before** SE-002+SE-003 paired PR per RELEASE-SPEC.md:607
- ✅ Zero behavior change observable from outside the codebase

**Success Metrics:**

- Sprint baseline remains 921 passed / 57 failed (or better) after PR merge [CODE-VERIFIED RELEASE-SPEC.md:473–474]
- No new public API surface visible to end users

---

**US-2.2: GateFailureSeverity enum + TFEP mapping**

- **As a** downstream reporting/audit-log consumer (audit.py, dashboards, telemetry)
- **I want** a typed `GateFailureSeverity` enum that bidirectionally maps from existing TFEP (Trailing Fail-Escape Path) outcomes
- **So that** failure taxonomy can be switched on without parsing free-text gate-reason strings

**Acceptance Criteria:**

- ✅ A new `GateFailureSeverity` enum is defined with three values [CODE-VERIFIED test name `test_three_values_present`; member names spec-deferred — research G6]
- ✅ Bidirectional mapping `TFEP outcome ↔ GateFailureSeverity` is implemented and tested (`test_tfep_maps_to_severity`, `test_severity_maps_to_tfep` per RELEASE-SPEC.md:387–389)
- ✅ The existing `TrailingGateResult` surface in `src/superclaude/cli/pipeline/trailing_gate.py` (called from `src/superclaude/cli/sprint/executor.py:1035–1037`) is **decorated**, not replaced — operational gate behavior is unchanged per RELEASE-SPEC §3.3 ("reporting taxonomy only") [CODE-VERIFIED no `GateFailureSeverity` symbol exists today]
- ✅ `tests/sprint/test_gate_failure_severity_enum.py` is authored and passes

**Success Metrics:**

- Zero behavior change in TFEP gate evaluation (regression suite confirms)
- audit.py (separate work, synth-02) can switch on enum value when logging gate failures

---

#### Epic 3: TUI Liveness & Cosmetic Fixes (R2)

**Description:** Three TUI fixes that ride on Rich.Live's existing 2 Hz auto-refresh (no new data wiring needed) — spinner on RUNNING (P-05), monotonic Duration column (P-02), and width-aware truncation (P-03+P-07 paired). These ship **before** the P-01 keystone so the dashboard is already polished when the activity stream lights up. [CODE-VERIFIED FINAL-REPORT.md:858 "fireworks landing" rationale]

---

**US-3.1: Spinner on RUNNING + active-panel title (P-05) — ships first**

- **As a** sprint user watching the TUI dashboard
- **I want** the RUNNING status cell and the active-panel title to show a cycling Rich spinner glyph
- **So that** I have continuous "the dashboard is alive" feedback even when the per-task path is silent (pre-P-01) or the executor is in a slow phase (PreFlight, between-phase transitions)

**Acceptance Criteria:**

- ✅ `from rich.spinner import Spinner` is imported in `src/superclaude/cli/sprint/tui.py` (currently absent per CODE-VERIFIED grep at research §4.2)
- ✅ In `_build_phase_table` (currently `src/superclaude/cli/sprint/tui.py:221`), when `status == PhaseStatus.RUNNING`, the cell uses `Spinner("dots", text="RUNNING", style="yellow")` instead of the static `STATUS_ICONS[PhaseStatus.RUNNING]` markup at line 69
- ✅ In `_build_active_panel` (currently `src/superclaude/cli/sprint/tui.py:360`), a `Spinner("dots2")` is prepended to the panel title (currently `f"[bold yellow]ACTIVE: Phase {self.current_phase.number}[/]"` at lines 408–412)
- ✅ Smoke test: within 2 s of sprint start, the RUNNING status cell shows a visible cycling glyph
- ✅ Smoke test: when executor is intentionally paused (PreFlight), the spinner continues to cycle (proves anchoring to `Live.refresh_per_second=2`, not push events) [CODE-VERIFIED `tui.py:101–106` Live config]
- ✅ TUI Waves 1-2 + tmux + summarizer + retrospective tests remain at 125/125 pass after snapshot rebaseline [CODE-VERIFIED RELEASE-SPEC.md:475]

**Success Metrics:**

- Time-to-first-motion after sprint start: ≤2 s (smoke-test)
- Zero false-success: spinner cycling does NOT correlate with subprocess liveness pre-P-01 (documented as known limitation; P-10 heartbeat is the follow-on mitigation per research §4.2 risk ¶a)

---

**US-3.2: Monotonic Duration column (P-02)**

- **As a** sprint user reading the phase table
- **I want** the Duration column for a RUNNING phase to show wall-clock elapsed time since the phase started (monotonically increasing)
- **So that** I can read Duration as "how long has this phase been running" instead of the current erratic idle-gap-since-last-event value

**Acceptance Criteria:**

- ✅ `src/superclaude/cli/sprint/tui.py:265–273` Duration cell expression for RUNNING phases changes from `f"{int(self.monitor_state.stall_seconds)}s"` (line 269) to `f"{int(time.monotonic() - self.monitor_state.phase_started_at)}s"` [CODE-VERIFIED `phase_started_at: float = field(default_factory=time.monotonic)` already exists at `src/superclaude/cli/sprint/models.py:610`]
- ✅ Optional `m:ss` formatting when elapsed ≥ 60 s [inference — research §4.3 marks as "optional"]
- ✅ Smoke test: Duration ticks up monotonically every second for the running phase; never decreases; matches wall-clock ±1 s after phase ends
- ✅ Documented caveat in CHANGELOG: sub-second phases (≤0.9 s) show `0s` then jump to `1s` on completion (research §8.2 edge case)
- ✅ INV-002 dual-writer hazard surfaced as a paired risk with P-01 (research §4.3 risk ¶a, §6.5): until P-01 lands, the per-task path constructs fresh empty `MonitorState()` at `src/superclaude/cli/sprint/executor.py:981, 1045` each with a brand-new `phase_started_at`, so Duration reads ~0 throughout per-task work. Mitigation: pair P-02 with P-01 OR wire `phase_started_at` from TUI-side `time.monotonic()` captured at first observation of a `current_phase` change

**Success Metrics:**

- User-reported "Duration is confusing" issues drop to zero post-merge [inference]
- 125/125 TUI Waves 1-2 baseline preserved

---

**US-3.3: Width-aware truncation (P-03 + P-07 combined PR)**

- **As a** sprint user on a wide terminal (>80 columns)
- **I want** the Prompt: and Agent: lines, error messages, and activity-stream descriptions to fit my terminal width rather than be hard-capped at 60 or 80 characters
- **So that** I can read full prompts without manually checking source files

**Acceptance Criteria:**

- ✅ **P-03 changes:**
  - Extraction-time `[:60]` slices in `src/superclaude/cli/sprint/config.py:179, 193, 203, 204` (inside `_extract_phase_prompt_preview` at lines 167–204) raised to `[:240]` or removed entirely
  - `_build_active_panel` computes `avail = max(40, self.console.width - 14)` (panel-border + `Prompt:` prefix budget) and passes to `_truncate`
  - Same width-aware truncation applied to Agent: line, error messages (currently 80-char cap at `src/superclaude/cli/sprint/tui.py:459, 539`), and activity-stream descriptions (currently 50-char cap at `src/superclaude/cli/sprint/tui.py:424`)
- ✅ **P-07 changes:**
  - `ASSISTANT_TEXT_MAX_LEN = 80` constant at `src/superclaude/cli/sprint/monitor.py:121` is removed or raised to 400 chars (a 4 KB monitor-memory budget)
  - Slicing at `src/superclaude/cli/sprint/monitor.py:466–467` removed; trim moved to render-time using P-03's width budget
  - **Layering correction:** monitor stores, renderer trims (research §6.4)
- ✅ **Combined acceptance:** on a 200-column terminal, Prompt: line displays text wider than 60 chars AND Agent: line displays wider than 80 chars; resizing terminal mid-sprint reflows the next render; panel does NOT flicker height-wise
- ✅ **INV-004 audit (mandatory pre-merge):** 15-minute grep audit of `Phase.prompt_preview` downstream consumers (log formatters, error reporters, JSONL writers) to confirm none assume ≤60 chars; audit documented in the PR [CODE-VERIFIED RELEASE-SPEC.md:393]
- ✅ **ANSI handling decision** captured in PR description: either (a) ship with `Text.from_ansi` render-time pass, or (b) ship with passthrough and document escape-code risk as known limitation (research §6.3 G4 [UNVERIFIED] open question)
- ✅ Smoke test on at least two terminal widths {80, 200}-column (research §8.3)

**Success Metrics:**

- Wider-terminal acceptance criterion validated at 200-column smoke test (Prompt: line >60 chars rendered)
- Zero panel-height flicker reports
- 125/125 TUI baseline preserved after snapshot rebaseline

---

#### Epic 4: TUI Per-Task Activation — Keystone (R2, ships LAST)

**Description:** Wire `OutputMonitor` into the per-task execution path (`src/superclaude/cli/sprint/executor.py:913–1051`) so the activity stream, Tasks bar, growth-rate, and live duration populate during per-task subprocess execution. This is THE keystone fix — every other TUI fix is cosmetic and rides on Rich.Live's auto-refresh; P-01 is the only one that wires new data into the dominant per-task code path. Ships LAST so cosmetic fixes are already polished — the "fireworks landing." [CODE-VERIFIED FINAL-REPORT.md:858]

---

**US-4.1: OutputMonitor on per-task path (P-01) — fireworks landing**

- **As a** sprint user watching a per-task phase (the dominant modern code path)
- **I want** the activity log, Tasks bar, growth rate, and Duration column to populate in real time during each per-task subprocess execution
- **So that** the dashboard transitions from "two updates per task with a frozen middle" to "continuously animated" — when this ships, the spinner is alive (already), bars advance (newly), Duration ticks (newly), prompt/agent lines are full-width (already), and the activity stream populates (newly), all at once

**Acceptance Criteria:**

- ✅ `OutputMonitor` is instantiated once per phase before the per-task for-loop in `execute_phase_tasks` (`src/superclaude/cli/sprint/executor.py:913–1051`), analogous to the freeform path's pattern at `src/superclaude/cli/sprint/executor.py:1276–1277`
- ✅ Per-task iteration calls a NEW public method `OutputMonitor.reset_for_next_task()` (NOT `monitor.reset(output_path)` — that discards `total_tasks_in_phase`)
- ✅ Per-task `proc.wait()` is replaced by a poll loop: `while proc._process.poll() is None: tui.update(sprint_result, monitor.state, phase); time.sleep(0.5)` (or equivalent via a new `ClaudeProcess.is_running()` public method to remove the underscore-coupling per research §4.1 risk ¶c)
- ✅ **Mandatory mitigation contract** (RELEASE-SPEC.md:454–461, TUI-ADVERSARIAL §1):
  1. New test file `tests/sprint/test_monitor_reset_between_tasks.py` containing:
     - `test_events_received_equals_6_after_two_3_event_tasks_with_reset` — writes 3 events for task 1, calls `monitor.reset_for_next_task()`, writes 3 events for task 2, asserts `monitor.state.events_received == 6`
     - `test_last_read_pos_correct_after_reset` — asserts `_last_read_pos` is at the correct file offset after each reset
  2. `OutputMonitor.reset_for_next_task()` is **public** (no underscore prefix), **idempotent** against partial-read state (finishes in-flight reads before resetting), and **distinct from** `OutputMonitor.reset()` [CODE-VERIFIED `OutputMonitor.reset(...)` exists at `src/superclaude/cli/sprint/monitor.py:291–308` and discards `total_tasks_in_phase` by constructing a fresh `MonitorState` at line 305]
  3. P-01 ships LAST in the TUI sequence
- ✅ **Smoke-test ACCEPT criteria** (TUI-ADVERSARIAL Manual Smoke-Test block):
  - 3-task per-task phase shows the Tasks bar advancing at task boundaries (not in one jump at end)
  - Activity log shows ≥1 event per task
  - `growth_rate_bps` is nonzero during task execution
  - NDJSON event count from the output file matches TUI-displayed count within 1, across phase boundaries (INV-001/005)
- ✅ **Smoke-test REJECT criteria**: bars still jump in one step at phase end; activity log shows `— — —` for the full task; `growth_rate_bps` stays at zero
- ✅ **Per-task stall watchdog:** confirm during PR scoping whether the freeform-path stall watchdog at `src/superclaude/cli/sprint/executor.py:1330–1364` is ported to the per-task path now that `proc.wait()` is replaced with a poll loop (research G5 [inference] — currently no per-task stall enforcement exists)

**Success Metrics:**

- "Fireworks landing" experience: all five dashboard transitions (spinner alive, bars alive, Duration ticks, full-width prompts, activity stream live) visible in a single demo session
- NDJSON-to-TUI event-count invariant holds across at least 5 sample sprints (within ±1)
- Sprint baseline 921 passed / 57 failed preserved (no net-new failures attributable to threading-model change)
- Total wave cost: ~5 engineering-days (P-05 day 1 → P-02 day 1–2 → P-03+P-07 day 2–2.5 → P-01 days 3–5) [CODE-VERIFIED TUI-ADVERSARIAL ¶170, RELEASE-SPEC.md:574]

---

### S21.2 Product Requirements

#### S21.2.1 Core Features (R2 — Sprint Runtime + TUI)

##### Feature 1: SE-001 Fail-closed empty-output gate

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) — MoSCoW: Must |
| **Description** | Empty output file produces `(False, 'empty output file')` deterministically; close any remaining soft-pass surface in the sprint codepath |
| **User Value** | Sprint owners see clearer, classifiable failures instead of false successes (RELEASE-SPEC.md:554) |
| **Dependencies** | None (foundation — ships first in R2 per RELEASE-SPEC.md:604–607) |
| **Effort** | S [inference] |

**Acceptance Criteria:** See US-1.1.
**Success Metrics:** 1–2 net-new failures per phase in first week (expected, not a regression). [CODE-VERIFIED RELEASE-SPEC §6.5]

---

##### Feature 2: SE-004 ExecutionMode enum

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) — MoSCoW: Should |
| **Description** | Replace `execution_mode: str` parameter with typed `ExecutionMode` enum (three values) |
| **User Value** | None directly visible to end users; enables SE-002+SE-003 |
| **Dependencies** | SE-001 lands first; SE-004 lands before SE-002+SE-003 paired PR per RELEASE-SPEC.md:607 |
| **Effort** | S [inference] |

**Acceptance Criteria:** See US-2.1.

---

##### Feature 3: SE-005 GateFailureSeverity enum

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) — MoSCoW: Should |
| **Description** | Typed enum decorating existing TFEP outcomes; bidirectional mapping; reporting taxonomy only |
| **User Value** | Enables audit-log and downstream-reporting consumers to switch on enum |
| **Dependencies** | SE-004 lands first per ship order |
| **Effort** | S [inference] |

**Acceptance Criteria:** See US-2.2.

---

##### Feature 4: SE-002 + SE-003 Per-task UID + sub-phase resume (paired)

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) — MoSCoW: Must |
| **Description** | Add stable per-task UID (`f"{phase_id}-{task_index:04d}"`) and sub-phase resume that skips completed tasks on re-invocation. Additive; legacy result files continue to work |
| **User Value** | Faster re-invocations after partial sprint progress; no re-paying token cost for completed tasks |
| **Dependencies** | SE-004 ExecutionMode enum (RELEASE-SPEC.md:607); Wave-4 checkpoint-parser tests (RK-15, +3 tests in `tests/sprint/test_checkpoint_parser.py::test_wave4_*`) — MUST be authored as part of this PR if missing (RELEASE-SPEC.md:480) |
| **Effort** | M [inference] |

**Acceptance Criteria:** See US-1.2 and US-1.3.

---

##### Feature 5: P-05 Spinner on RUNNING + active-panel title

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) — MoSCoW: Must (visibility/UX core) |
| **Description** | Replace static RUNNING markup with `rich.spinner.Spinner`; add spinner to active-panel title |
| **User Value** | Continuous "dashboard is alive" feedback even when the per-task path is silent |
| **Dependencies** | None — rides on Rich.Live's existing 2 Hz refresh |
| **Effort** | S [inference] |
| **Ship order** | **Day 1 (FIRST)** [CODE-VERIFIED RELEASE-SPEC.md:610–613] |

**Acceptance Criteria:** See US-3.1.

---

##### Feature 6: P-02 Monotonic Duration column

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) — MoSCoW: Must |
| **Description** | Duration cell for RUNNING phase reads `time.monotonic() - phase_started_at` instead of `stall_seconds` |
| **User Value** | Duration column matches user mental model ("wall-clock time the phase has been running") |
| **Dependencies** | INV-002 dual-writer hazard paired with P-01 (until P-01 lands, per-task path constructs fresh empty `MonitorState()`; Duration reads ~0) |
| **Effort** | S [inference] |
| **Ship order** | Day 1–2 (after P-05) |

**Acceptance Criteria:** See US-3.2.

---

##### Feature 7: P-03 + P-07 Width-aware truncation (combined PR)

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) — MoSCoW: Should |
| **Description** | Raise extraction-time caps; compute render-time width budget from `console.width`; move assistant-text trim from monitor to render path (layering correction) |
| **User Value** | Wider terminals show full prompts/agent lines instead of 60/80-char clipping |
| **Dependencies** | INV-004 15-minute downstream-consumer audit (mandatory pre-merge per RELEASE-SPEC.md:393); ANSI handling decision (research G4) |
| **Effort** | S [inference] |
| **Ship order** | Day 2–2.5 (after P-02) |

**Acceptance Criteria:** See US-3.3.

---

##### Feature 8: P-01 OutputMonitor on per-task path (keystone)

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) — MoSCoW: Must |
| **Description** | Instantiate `OutputMonitor` per phase, call new `reset_for_next_task()` per task, replace `proc.wait()` with poll loop |
| **User Value** | Activity stream + bars + growth rate populate in real time during per-task execution; "fireworks landing" |
| **Dependencies** | Mandatory `tests/sprint/test_monitor_reset_between_tasks.py` (INV-001/005); new `OutputMonitor.reset_for_next_task()` public method |
| **Effort** | M [inference] (only M in the slate; only one that touches threading model) |
| **Ship order** | **Days 3–5 (LAST)** [CODE-VERIFIED FINAL-REPORT.md:858 — "fireworks landing"] |

**Acceptance Criteria:** See US-4.1.

---

#### S21.2.2 Feature Prioritization Matrix (MoSCoW)

> **Framework:** MoSCoW (Must/Should/Could/Won't). RICE not required at Lightweight tier per PRD template.

| Feature | MoSCoW | Effort [inference] | Ship Order (R2) | Rationale |
|---------|--------|--------------------|------------------|-----------|
| SE-001 fail-closed empty output | **Must** | S | 1 (foundation) | Closes a soft-pass failure surface; user-facing fail-clarity gain |
| SE-004 ExecutionMode enum | **Should** | S | 2 | Foundation for SE-002+SE-003; invisible to users |
| SE-005 GateFailureSeverity enum | **Should** | S | 3 | Reporting taxonomy only; enables audit/dashboard switching |
| SE-002 + SE-003 task_uid + resume (paired) | **Must** | M | 4 | Headline R2 user benefit — faster resume |
| P-05 spinner | **Must** | S | TUI day 1 (FIRST) | Zero-coupling, immediate liveness signal |
| P-02 Duration | **Must** | S | TUI day 1–2 | Corrects user mental model |
| P-03 + P-07 width-aware truncation | **Should** | S | TUI day 2–2.5 | Visible only to wide-terminal users; layering correction |
| P-01 OutputMonitor keystone | **Must** | M | TUI days 3–5 (LAST) | "Fireworks landing" — dominant per-task path activation |
| **R1 task-surface features (cross-reference only)** | | | | |
| TU-001 CRITICAL FAIL audit | **Must** | M [inference] | R1 (out of scope here) | Audit trail for STRICT failures (synth-02) |
| TU-003 universal quality principles | **Must** | S [inference] | R1 (out of scope here) | Adoption on faith of A-004; programmatic checklist enforcement |
| TU-004 BLOCKED state | **Must** | S [inference] | R1 (out of scope here) | Replaces soft <0.70 confidence prompt |
| TU-007 carry-over preservation | **Should** | S [inference] | R1 (out of scope here) | DEFER-lock tests via SoT constants (A-005 unresolved) |
| **Could (deferred to R3+)** | | | | |
| TU-005 keyword drift (tasklist-protocol) | Could | (R3) | — | Wider STRICT keywords in tasklist-protocol vs task.md per research §11.4 |
| TU-006 missing config files | Could | (R3) | — | `config/tier-keywords.yaml` etc. referenced but absent (research §10.2, RK-18) |
| SE-006 (TBD per A-002) | Could | (R3) | — | Closed candidate set per A-002 |
| **Won't (permanently out)** | | | | |
| `task-unified` rename (Q1/Q2) | Won't (this release) | — | — | DEFER-gated on A-005; preserved verbatim until forensic-caller consumers enumerated in R3 |
| API/HTTP surface for /sc:task | Won't | — | — | Out of scope; /sc:task is a CLI/text contract, not an HTTP API |

---

### S21.3 Implementation Phasing (R1 / R2 per RELEASE-SPEC §7 split)

The v3.75 release is split into **two sibling release streams** per RELEASE-SPEC.md §7 [CODE-VERIFIED research file §1]:

| Phase | Features | Rationale |
|-------|----------|-----------|
| **R1 (task-surface)** | TU-001 (CRITICAL FAIL audit), TU-003 (universal quality principles), TU-004 (BLOCKED state), TU-007 (carry-over preservation) | Task-surface layer: command file + skill file + new `audit.py` module. No sprint or TUI changes. Out of scope for THIS synthesis file — covered in synth-01 (audit) and synth-02 (architecture). |
| **R2 (sprint-runtime + TUI)** | SE-001, SE-004, SE-005, SE-002+SE-003 (paired) + TUI top-five (P-05, P-02, P-03+P-07, P-01) | Sprint-side + TUI work. **Ship order within R2:** SE-001 → SE-004 → SE-005 → SE-002+SE-003 paired (sprint); P-05 → P-02 → P-03+P-07 → P-01 (TUI). Sprint and TUI streams are independent; only sharing R2 release status [CODE-VERIFIED research file §4.5]. |
| **R3 (deferred — future release)** | TU-005, TU-006, SE-006, `task-unified` rename (Q1/Q2 after A-005 consumer enumeration) | Closed candidate set per A-002. Not in v3.75. |

**Within-R2 PR sequencing:**

- Sprint PRs: **SE-001 → SE-004 → SE-005 → SE-002+SE-003 paired** [CODE-VERIFIED RELEASE-SPEC.md:604–607]
- TUI PRs: **P-05 (day 1) → P-02 (day 1–2) → P-03+P-07 paired (day 2–2.5) → P-01 (days 3–5)** [CODE-VERIFIED RELEASE-SPEC.md:610–613, FINAL-REPORT.md:858, TUI-ADVERSARIAL sequencing block]
- The two PR streams can run in parallel; only the P-01 ship date is the synchronization point ("fireworks landing")

---

### S21.4 Release Criteria & Definition of Done

#### S21.4.1 R2 Release Criteria

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality (sprint)** | 921 passed / 57 failed sprint suite baseline preserved or improved | `uv run pytest tests/sprint/` — new failures must be net-new, not pre-existing [CODE-VERIFIED RELEASE-SPEC.md:473–474] | ⬜ |
| **Functionality (TUI)** | 125/125 TUI Waves 1-2 + tmux + summarizer + retrospective baseline preserved | `uv run pytest tests/tui/` (path inferred — exact path per RELEASE-SPEC) [CODE-VERIFIED RELEASE-SPEC.md:475] | ⬜ |
| **Functionality (process)** | 16/16 `test_process.py::TestClaudeProcess` baseline preserved, including `test_build_prompt_contains_task_command` | `uv run pytest tests/sprint/test_process.py -v` [CODE-VERIFIED RELEASE-SPEC.md:477] | ⬜ |
| **Functionality (Wave-4 checkpoint parser)** | +3 tests in `tests/sprint/test_checkpoint_parser.py::test_wave4_*` pass (RK-15) | `uv run pytest tests/sprint/test_checkpoint_parser.py::test_wave4_task_checkpoint_heading_form tests/sprint/test_checkpoint_parser.py::test_wave4_legacy_heading_back_compat tests/sprint/test_checkpoint_parser.py::test_wave4_checkpoint_manifest_uses_label_not_basename` [CODE-VERIFIED RELEASE-SPEC.md:480]. MUST be authored as part of SE-002+SE-003 PR if missing | ⬜ |
| **Classification accuracy** | Tier classification accuracy targets met for STRICT/STANDARD/LIGHT/EXEMPT (operationalized via R1 audit-log; surfaced here as cross-stream criterion) | Audit-log JSONL inspection across sample sprint runs [inference — exact target per RELEASE-SPEC TBD] | ⬜ |
| **Audit log integrity (cross-ref to R1)** | Daily-rotated JSONL at `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl` is append-only, per-task write-locked, no PII in `reason` field (synth-02) | R1-side criterion; R2 sprint integration must not corrupt the format (cleanup_audit emits `/sc:task` without `--compliance` per synth-02 §6.3) | ⬜ |
| **Coverage (new code)** | ≥80% line coverage on new R2 code (SE-001..005 changes) | `uv run pytest --cov=superclaude tests/sprint/` [CODE-VERIFIED research file §9] | ⬜ |
| **TUI smoke tests** | P-05/P-02/P-03+P-07 smoke tests pass at minimum {80, 200}-column terminal widths | Manual smoke (FINAL-REPORT §11.5) | ⬜ |
| **P-01 keystone reset-test** | `tests/sprint/test_monitor_reset_between_tasks.py` both tests pass | `uv run pytest tests/sprint/test_monitor_reset_between_tasks.py -v` [CODE-VERIFIED RELEASE-SPEC.md:454–461] | ⬜ |
| **INV-004 audit** | 15-minute downstream-consumer audit of `Phase.prompt_preview` documented in P-03 PR | PR description includes audit results [CODE-VERIFIED RELEASE-SPEC.md:393] | ⬜ |
| **Documentation** | CHANGELOG note for P-02 (sub-second phases show `0s` then jump to `1s`); CHANGELOG note for SE-001 expected 1–2 net-new failures per phase first week | Documentation review | ⬜ |
| **Operations** | Sprint and cleanup-audit subprocess pipelines unaffected by R2 changes (no `/sc:task` prompt-line drift) | `tests/sprint/test_process.py::test_build_prompt_contains_task_command` passes [CODE-VERIFIED research file §9, RELEASE-SPEC.md:477] | ⬜ |

#### S21.4.2 Definition of Done (Feature Level)

A feature in R2 (SE-*or P-*) is "Done" when:

- [ ] All acceptance criteria in the corresponding user story (S21.1) are met
- [ ] Unit tests written and passing (per-feature acceptance test file per RELEASE-SPEC §5)
- [ ] Sprint baseline 921/57 not regressed (or net-new failures classified)
- [ ] TUI baseline 125/125 not regressed (after snapshot rebaseline where applicable)
- [ ] `tests/sprint/test_process.py` 16/16 preserved
- [ ] Coverage ≥80% on new code
- [ ] Code reviewed and approved
- [ ] CHANGELOG entry written (where user-visible behavior changes)
- [ ] Smoke test executed (TUI features at {80, 200}-column; sprint features against a 3-task per-task phase)
- [ ] Mandatory mitigation contracts satisfied (P-01 reset-test; P-03 INV-004 audit; SE-002+SE-003 Wave-4 +3 tests)
- [ ] `make verify-sync` passes (`src/superclaude/` ↔ `.claude/` parity)
- [ ] Product owner (TBD) acceptance

#### S21.4.3 Rollback & Contingency Plans

| Scenario | Detection Method | Rollback Procedure | Decision Maker |
|----------|------------------|--------------------|----------------|
| SE-001 net-new failures exceed 2/phase/first week | Audit-log JSONL + sprint failure-rate dashboard [inference] | Revert SE-001 PR; restore previous failure-reason literal `f"File empty (0 bytes): {output_file}"` at `src/superclaude/cli/pipeline/gates.py:39` | TBD |
| SE-002+SE-003 sub-phase resume silently skips wrong task (tasklist drift) | User-reported issue + result-file inspection | Revert SE-003 resume logic; SE-002 task_uid persistence kept (additive, no regression) | TBD |
| P-01 introduces threading regression (sprint hangs, deadlocks) | `tests/sprint/test_process.py` failures or sprint-suite regression below 921 passed | Revert P-01; P-05/P-02/P-03+P-07 stay merged (independent fixes) | TBD |
| P-01 reset-test (`tests/sprint/test_monitor_reset_between_tasks.py`) intermittently fails | CI flakiness telemetry [inference] | Tighten test determinism (file-flush, sleep barriers); do NOT mark xfail | TBD |
| P-03 INV-004 audit surfaces a downstream consumer that breaks at >60 char prompt_preview | Pre-merge audit | Cap extraction-time at consumer's tolerance (e.g., `[:120]` instead of `[:240]`); keep render-time width-aware | TBD |
| TUI snapshot rebaseline introduces 125/125 regression | `uv run pytest tests/tui/` | Re-snapshot with fixed-width terminal env vars; restore baseline | TBD |

---

### S21.5 Timeline & Milestones

#### S21.5.1 High-Level Timeline (TBD calendar dates)

```
R2 (Sprint Runtime + TUI) — Total ~5 engineering-days for TUI stream; sprint stream parallel

[Sprint Stream: SE-001 → SE-004 → SE-005 → SE-002+SE-003] ─── TBD start - TBD end
    ├── Milestone S1: SE-001 merged           TBD
    ├── Milestone S2: SE-004 merged           TBD
    ├── Milestone S3: SE-005 merged           TBD
    └── Milestone S4: SE-002+SE-003 paired PR merged + Wave-4 +3 tests passing  TBD

[TUI Stream: P-05 → P-02 → P-03+P-07 → P-01] ─── TBD start - TBD end (~5 eng-days)
    ├── Milestone T1: P-05 spinner merged    TBD (Day 1)
    ├── Milestone T2: P-02 Duration merged   TBD (Day 1-2)
    ├── Milestone T3: P-03+P-07 paired merged + INV-004 audit documented  TBD (Day 2-2.5)
    └── Milestone T4: P-01 keystone merged + reset-test passing — "FIREWORKS LANDING"  TBD (Days 3-5)

R2 Release Gate: all sprint + TUI PRs merged, baselines (921/57, 125/125, 16/16) preserved
```

#### S21.5.2 Detailed Phase Breakdown

##### R2 Sprint-Stream Phase (TBD start – TBD end)

**Focus:** Harden sprint-side failure surface; add typed taxonomy; enable sub-phase resume.

**Deliverables:**

- [ ] SE-001 fail-closed empty-output PR merged (S [inference])
- [ ] SE-004 ExecutionMode enum PR merged (S [inference])
- [ ] SE-005 GateFailureSeverity enum PR merged (S [inference])
- [ ] SE-002 + SE-003 paired PR merged with Wave-4 +3 checkpoint-parser tests (M [inference])

**Success Criteria:**

- Sprint baseline 921/57 preserved or improved
- Resume on a partially-completed phase short-circuits to "0 tasks executed, N skipped" within seconds
- `tests/sprint/test_process.py` 16/16 preserved

**Target Completion:** TBD

---

##### R2 TUI-Stream Phase (TBD start – TBD end, ~5 engineering-days)

**Focus:** Transform the dashboard from "two updates per task with frozen middle" to "continuously animated" — fireworks landing.

**Deliverables:**

- [ ] P-05 spinner PR merged (S [inference]) — Day 1
- [ ] P-02 Duration PR merged (S [inference]) — Day 1–2
- [ ] P-03 + P-07 paired truncation PR merged + INV-004 audit doc (S [inference]) — Day 2–2.5
- [ ] P-01 OutputMonitor keystone PR merged + `tests/sprint/test_monitor_reset_between_tasks.py` (M [inference]) — Days 3–5

**Success Criteria:**

- TUI 125/125 baseline preserved
- All five dashboard transitions visible in a single demo session on Day 5 ("fireworks landing")
- NDJSON event-count matches TUI-displayed count within ±1 across phase boundaries

**Target Completion:** TBD

---

##### R2 Release Gate (TBD)

**Focus:** Both streams merged; release criteria validated.

**Deliverables:**

- [ ] R2 release notes published
- [ ] CHANGELOG updated with SE-001 first-week failure-rate note and P-02 sub-second-phase note
- [ ] `make verify-sync` clean
- [ ] Audit-log entries (cross-ref R1) intact across sample sprints

**Target Completion:** TBD

---

## S23. Error Handling & Edge Cases

### S23.1 Error Categories

| Category | Examples | User Experience | Recovery |
|----------|----------|-----------------|----------|
| **Gate validation errors (SE-001)** | Empty output file from per-task subprocess | Phase result shows failure with literal reason `'empty output file'` instead of soft-pass [CODE-VERIFIED current literal `f"File empty (0 bytes): {output_file}"` at `src/superclaude/cli/pipeline/gates.py:39` — must change to spec literal] | User inspects output path; investigates why subprocess produced no output; re-runs after fixing root cause. STRICT-tier task failure halts sprint per `src/superclaude/cli/sprint/process.py:197–215` execution-rules block (`EXIT_RECOMMENDATION: HALT`) |
| **Checkpoint integrity errors** | Missing checkpoint at end-of-phase | Phase status set to `PASS_MISSING_CHECKPOINT` in `full` mode per `_verify_checkpoints` at `src/superclaude/cli/sprint/executor.py:1720–1803` | Operator inspects which checkpoint failed via checkpoint manifest at end-of-sprint (executor.py:1623–1644); choice between re-run vs. accept missing |
| **Resume integrity errors (SE-003)** | Mid-task crash (subprocess crash, `KeyboardInterrupt`) leaves partial Nth task entry without finish timestamp | Resume logic treats partial task as not-done and re-launches; completed N-1 tasks are skipped via `task_uid` set | Automatic — user runs `--start <phase>` and partial work re-executes from the partial-task boundary |
| **TUI render errors** | Display glitch (e.g., terminal closed mid-render, malformed Rich markup) | `tui.update()` is wrapped in `try/except` at `src/superclaude/cli/sprint/executor.py:1370–1380`; sets `self._live_failed = True` on first error at `src/superclaude/cli/sprint/tui.py:130–152` and silences subsequent updates | Sprint continues; TUI is silenced. User can `Ctrl+C` to abort and re-run in a healthy terminal |
| **MCP/circuit-breaker errors (cross-ref R1)** | Sequential or Serena MCP unavailable on STRICT tier | CRITICAL FAIL audit entry written; task halts | Operator can use `--skip-compliance --reason "..."` override; logged for <12% metering target |

### S23.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| **Empty output → SE-001 fail-closed** | `gate_passed()` returns `(False, 'empty output file')`; sprint executor surfaces as failure (not soft-pass) | `tests/sprint/test_gate_passed_empty_output.py::test_empty_output_returns_false` [CODE-VERIFIED RELEASE-SPEC.md:381–382] |
| **Missing checkpoint → SE-003 sub-phase resume** | When result file has `task_uid` for tasks 1..N-1 but the partial Nth task lacks finish timestamp, resume re-launches the Nth task. Legacy result files without `task_uid` re-run every task (graceful fallback per RELEASE-SPEC Q10 (a)) | `tests/sprint/test_subphase_resume.py` [authored by SE-002+SE-003 PR per RELEASE-SPEC.md:415–419] |
| **TUI hang on per-task path (P-01 + P-05 mitigations)** | Pre-P-01: per-task `proc.wait()` blocks unconditionally — `src/superclaude/cli/sprint/executor.py:1054–1093` `_run_task_subprocess` — and there is NO per-task stall watchdog (the freeform-path watchdog at `src/superclaude/cli/sprint/executor.py:1330–1364` does not apply). After P-01: poll loop replaces `proc.wait()`, enabling per-task watchdog port (research G5 [inference]). P-05 spinner provides "alive" signal in the meantime so user can distinguish "frozen TUI" from "running but silent subprocess" | Smoke test: spinner continues to cycle when subprocess is paused (proves `Live.refresh_per_second=2` anchoring); poll loop terminates within `config.stall_timeout` when subprocess hangs |
| **Prompt cut-off at 60/80 chars (P-03+P-07)** | Pre-fix: double-truncation at extraction-time `[:60]` (`src/superclaude/cli/sprint/config.py:179, 193, 203, 204`) AND render-time `_LLM_LINE_MAX=60` (`src/superclaude/cli/sprint/tui.py:34, 386–387`); console width never read. Assistant text additionally pre-trimmed to 80 chars at `src/superclaude/cli/sprint/monitor.py:121, 466–467`. Post-fix: extraction-time cap 240; render-time width-aware (`avail = max(40, console.width - 14)`); monitor stores, renderer trims | Smoke test on {80, 200}-column terminals (research §8.3); INV-004 downstream-consumer audit pre-merge per RELEASE-SPEC.md:393 |
| **Partial result resume via stable task_uid** | Stable form `f"{phase_id}-{task_index:04d}"` is the cross-session resume key. Properties: phase-scoped, sortable (zero-padded `:04d` means string sort = integer sort), idempotent (computed from inputs at task-iteration time at `src/superclaude/cli/sprint/executor.py:957 for i, task in enumerate(tasks)`) | `tests/sprint/test_task_uid.py` validates form + uniqueness across phases |
| **Tasklist drift between sprint invocations** | User edits tasklist and inserts a task at position 3 between runs — all `task_index ≥ 3` shift by one. Resume could skip the wrong task. **Minimum bar:** resume MUST NOT silently skip; produce a clearly-logged warning OR force full re-run. Mitigation not in spec as written (research G3 [UNVERIFIED]) — implementation must decide: (a) combine `task_index` with stable content hash, OR (b) detect tasklist drift via tasklist-fingerprint comparison and force full re-run | Escalated to Open Questions; consumer implementation decides between (a) and (b) |
| **BLOCKED state recovery (cross-ref R1 TU-004)** | Confidence <0.70 produces classification header with `TIER: BLOCKED`; sprint halts at this phase. Operator escape: re-run with `--compliance [tier]` (forces specific tier), `--skip-compliance --reason "..."` (overrides BLOCKED with audit-log entry), or `--force-strict` (escalates) | Cross-stream: BLOCKED handling lives in R1 audit.py; sprint integration at `src/superclaude/cli/sprint/process.py:170–171` hardcodes `--compliance strict` so BLOCKED would only arise if model fails to classify; STRICT-tier failure triggers HALT per execution-rules block |
| **Sub-second phase Duration (P-02 edge case)** | Phases that complete in <1 s show Duration `0s` then jump to `1s` on terminal status. Not a regression — documented in CHANGELOG per US-3.2 | Smoke test, no automated test required |
| **ANSI escape codes in echoed tool output (P-07 risk)** | If tool output contains raw `\x1b[31m` etc., the renderer (after P-07 raises monitor cap) will display garbled characters. Rich's `Text.from_markup` handles `[...]` markup but not ANSI CSI. Mitigation: pipe assistant-text and activity-description strings through `Text.from_ansi(...)` at render time (research §6.3, [UNVERIFIED] in any committed PR) | ANSI handling decision captured in P-03+P-07 PR description per US-3.3; smoke test with a contrived ANSI-containing prompt |

### S23.3 Graceful Degradation

| Component Failure | Degraded Experience | User Communication |
|-------------------|--------------------|--------------------|
| **TUI render path fails** | Sprint executor continues; TUI silenced after first `_live_failed = True` at `src/superclaude/cli/sprint/tui.py:130–152` | No active surface; user sees stdout fallback if any |
| **OutputMonitor crash during per-task path (post-P-01)** | Per-task subprocess continues to completion; TUI shows last-known state; activity stream freezes | Operator can `Ctrl+C` and re-run; result file still produced via subprocess |
| **MCP server outage on STANDARD tier** | Skill falls back per `src/superclaude/skills/sc-task-protocol/SKILL.md:253–263` (Context7 fallback allowed); audit log records fallback [inference — even though fallback is allowed, audit log should record it for transparency] | None — execution proceeds with noted limitation |
| **MCP server outage on STRICT tier (cross-ref R1)** | CRITICAL FAIL — no fallback per `SKILL.md:253–263` ("fallback not allowed"); task halts | Operator must restore MCP or invoke `--skip-compliance` with reason |
| **Sprint subprocess hangs (pre-P-01 per-task path)** | No timeout enforcement beyond subprocess-level `timeout_seconds`; sprint hangs indefinitely until `Ctrl+C`. Spinner (P-05) continues cycling — **false reassurance** documented in P-05 risk ¶a (research §4.2) | P-10 follow-on heartbeat is the long-term mitigation; for v3.75 R2, document as known limitation in CHANGELOG |
| **Resume on a phase where output files were deleted between runs** | task_uid set is empty; all tasks re-execute (no false-skip) | None — automatic |
| **Resume after tasklist edit (drift)** | Per S23.2 above — clear-logged warning or full re-run | Warning surfaces in stdout and audit log |

### S23.4 Cross-Reference Map (Research §10 Synthesis-Mapping)

- **S23.1 Empty output / SE-001:** research §2.1, §7.1, §10 cross-ref
- **S23.2 Missing checkpoint / SE-003:** research §2.2, §7.2, §10 cross-ref
- **S23.2 TUI hang / P-01+P-05:** research §4.1, §4.2, §7.3, §10 cross-ref — including the **critical finding that no per-task stall watchdog exists today**
- **S23.2 Prompt cut-off / P-03+P-07:** research §4.4, §7.4, §10 cross-ref
- **S23.2 Partial-result resume / task_uid:** research §2.2, §7.5, §10 cross-ref
- **S23.2 Tasklist drift (G3):** research §7.5 edge case + Gaps & Questions G3 — [UNVERIFIED] not in spec as written
- **S23.2 BLOCKED state recovery:** cross-ref R1 TU-004 in synth-01/synth-02

---

## S24. User Interaction & Design

### S24.1 Wireframes & Mockups

| Screen/Flow | Link | Status | Notes |
|-------------|------|--------|-------|
| Sprint TUI dashboard — current state (pre-R2) | TBD | TBD | Reference screenshot of current TUI showing static "RUNNING" markup, idle-gap `stall_seconds` in Duration column, 60-char prompt clipping |
| Sprint TUI dashboard — P-05 + P-02 (Day 1–2) | TBD | TBD | Cycling spinner glyph in RUNNING status cell; monotonic Duration ticking |
| Sprint TUI dashboard — P-03+P-07 (Day 2–2.5) | TBD | TBD | 200-column terminal showing Prompt: line >60 chars and Agent: line >80 chars |
| Sprint TUI dashboard — P-01 fireworks landing (Day 5) | TBD | TBD | Full-motion dashboard: spinner cycling, bars advancing at task boundaries, Duration ticking, prompt/agent full-width, activity stream populating in real time |
| TUI failure-state — TUI silenced after render error | TBD | TBD | Show `self._live_failed = True` fallback (terminal returns to stdout-only) |
| Sprint failure-state — SE-001 fail-closed empty output | TBD | TBD | Phase row shows `FAIL: empty output file` instead of legacy reason |

### S24.2 Design System

> **Render conventions** are operationalized in `src/superclaude/cli/sprint/tui.py` and ride on the `rich` library. Below is the design system checklist for the TUI surface:

- [ ] **Rich.Live cadence**: `refresh_per_second=2` (`src/superclaude/cli/sprint/tui.py:101–106`) — 500 ms tick. All dynamic content (spinner, Duration, etc.) animates at this rate without explicit executor push. [CODE-VERIFIED]
- [ ] **Per-task path TUI updates**: `tui.update(sprint_result, monitor.state, phase)` called exactly twice per task today (`src/superclaude/cli/sprint/executor.py:980–985` before launch, `:1043–1049` after completion); post-P-01 this becomes a 500 ms poll loop within each task
- [ ] **Spinner (P-05) from RUNNING state**: `Spinner("dots", text="RUNNING", style="yellow")` in status cell; `Spinner("dots2")` in active-panel title. Mental model: "cycling = alive." Known caveat: spinner cycling does NOT correlate with subprocess liveness pre-P-01 (false-reassurance risk per research §4.2 risk ¶a) — long-term mitigation is P-10 heartbeat
- [ ] **Duration column (P-02)**: elapsed-since-`phase_started_at` via `time.monotonic()` arithmetic (`src/superclaude/cli/sprint/models.py:610`). Monotonically increasing; never decreases. Mental model matches "wall-clock time the phase has been running." Sub-second phases (≤0.9 s) show `0s` → `1s` on completion (documented edge case)
- [ ] **Width-aware truncation (P-03 + P-07)**: render-time budget `avail = max(40, console.width - 14)` derived from `self.console.width` (Rich's auto-detected terminal width). Layering: monitor stores full string, renderer trims to width. Applied to Prompt: line, Agent: line, error messages, activity-stream descriptions. INV-004 downstream-consumer audit MUST run pre-merge
- [ ] **Per-task `path` display**: `last_task_id` populated in `MonitorState` per-task update path (`src/superclaude/cli/sprint/executor.py:984, 1048`); rendered in dashboard active panel
- [ ] **Activity stream** (`src/superclaude/cli/sprint/tui.py:404–435`): three lines of `(timestamp, tool_name, description)` from `MonitorState.activity_log` (capped `ACTIVITY_LOG_MAX = 3` at `src/superclaude/cli/sprint/monitor.py:117`); `[thinking... Ns]` indicator when idle >2 s (`_THINKING_IDLE_SECONDS = 2` at `src/superclaude/cli/sprint/tui.py:38`). Empty on per-task path pre-P-01; populates after P-01 ships
- [ ] **Color tokens (Rich markup)**:
  - RUNNING: `yellow` (status cell + active panel title)
  - PASS/SUCCESS: green (per existing `STATUS_ICONS` at `src/superclaude/cli/sprint/tui.py:58–72`)
  - FAIL/ERROR: red
  - PENDING: dim/`"-"`
- [ ] **Typography**: monospace (terminal default); no custom typography
- [ ] **Responsive breakpoints**: terminal width 40 (floor, hard `max(40, ...)`), 80 (legacy), 200 (wide-terminal acceptance criterion); resize mid-sprint reflows on next 500 ms tick
- [ ] **Animation/motion guidelines**:
  - Rich `Spinner("dots")` (~10 Hz internal, visible at 2 Hz `Live.refresh_per_second`)
  - Rich `Spinner("dots2")` for active-panel title (different glyph set so two spinners don't visually sync)
  - Duration column updates once per Rich.Live refresh tick (500 ms)
  - No flashing/blinking (accessibility)
- [ ] **Icon set**: Unicode glyphs via Rich's spinner library; no custom icon set required
- [ ] **Wireframes**: TBD
- [ ] **Mockups**: TBD
- [ ] **Component library documentation**: TBD — Rich primitives (`Table`, `Panel`, `Live`, `Spinner`, `Text`) are the de facto library

### S24.3 Prototype Links

| Prototype | Purpose | Link |
|-----------|---------|------|
| P-05 spinner standalone demo | Demonstrate Rich.Live + Spinner cycling at 2 Hz independent of executor pushes | TBD |
| P-02 Duration monotonic tick demo | Demonstrate `time.monotonic() - phase_started_at` arithmetic in a minimal Rich.Live harness | TBD |
| P-03+P-07 width-aware truncation demo | Show resize behavior on a contrived 200-char prompt across {40, 80, 200}-column terminals | TBD |
| P-01 fireworks landing end-to-end demo | Full 3-task per-task phase showing all five dashboard transitions live | TBD |

### S24.4 Ship Order — Fireworks Landing (Authoritative)

The ship order is **P-05 → P-02 → P-03+P-07 → P-01** (RELEASE-SPEC.md:610–613; FINAL-REPORT.md:858; TUI-ADVERSARIAL sequencing block). The phrase **"fireworks landing"** originates in Variant A's structural-correctness lens of the adversarial debate and was ratified by Variant C's per-day ROI methodology and Variant B's saliency weighting. From TUI-ADVERSARIAL ¶168 verbatim:

> "Days 3–5 — P-01 (OutputMonitor on per-task path): The keystone. Lands with the cosmetic fixes already in place, so the day P-01 ships the user sees *everything come alive simultaneously* — the spinner is alive (was already), the bars are alive (newly), Duration ticks correctly (newly), prompt and agent lines are full-width (already), the activity stream populates (newly). **This is the 'fireworks landing'** — Variant A's term, ratified by C's independent day-numbered timing and B's saliency analysis."

Three reinforcing reasons (research §5):

1. **Visibility timing.** P-05 ships Day 1 → users see motion immediately. P-02, P-03+P-07 by Day 2.5 → users see correct Duration & full-width prompts. Then on Day 3-5 P-01 lights up the activity stream, growth rate, and Tasks-bar advancement — all at once, against an already-polished dashboard.
2. **Risk shape.** P-01 is the only M-effort fix in the slate and the only one that touches `proc.wait()` / threading model. Shipping it last means the cosmetic fixes can be reviewed, merged, and validated independently — and if P-01 needs another revision, the dashboard still looks polished.
3. **Per-day ROI math** (TUI-ADVERSARIAL ¶25). P-05 delivers ~30% of §2.2 resolution per engineering-day (1-day ship); P-01 delivers ~80% of §2.1+§2.2 per engineering-day-equivalent (2.5-day ship → 32%/day). The two are within noise on per-day return. The tiebreak goes to P-01 on *impact magnitude*, while the *sequencing* honors C's "ship certain wins first" intuition.

**P-01 ranks #1 but ships LAST. This is intentional; both pieces of metadata must be preserved in implementation planning.**

Total wave cost: **~5 engineering-days** [CODE-VERIFIED TUI-ADVERSARIAL ¶170, RELEASE-SPEC.md:574].

---
