# Research: Sprint Runtime + TUI UX for Unified /sc:task

**Investigation type:** UX Investigator
**Scope:** SE-001..005 behavioral changes + TUI top-5 fixes + edge cases + interaction patterns
**Status:** Complete
**Date:** 2026-05-14

---

## 1. Orientation: spec scope vs. live-code state

The v3.75 release spec at `.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/artifacts/RELEASE-SPEC.md` defines two sibling release streams:

- **R1 (task-surface):** TU-001/003/004/007 — out of scope for this research.
- **R2 (sprint-runtime + TUI, sibling to R1):** SE-001, SE-002+SE-003 paired, SE-004, SE-005 + TUI top-5 (P-01 keystone, P-02/P-03/P-05/P-07 supporting fixes). This is the focus.

A blanket grep of `src/superclaude/cli/` for `ExecutionMode`, `GateFailureSeverity`, `task_uid`, and the `"empty output file"` failure-reason literal returns **zero hits in the sprint module** [CODE-VERIFIED via `grep -rnE 'ExecutionMode|GateFailureSeverity|task_uid|empty output file' src/superclaude/cli/`]. Only a test file references `PhaseExecutionMode` (`tests/sprint/test_preflight.py:26,309`), which is unrelated to the SE-004 `ExecutionMode` enum the spec describes. Therefore **every SE-001..005 row below describes a planned-but-not-yet-implemented behavior change.** The user-facing impact statements come from RELEASE-SPEC §2.2 and §6.5; the file:line evidence cited is the *change site* the spec mandates (the code that must be modified), not an existing implementation.

The TUI top-5 fixes are in the same state: **none are implemented in the live tree.** TUI-ANALYSIS.md and TUI-ADVERSARIAL.md catalog the *bugs* and the *fix sites*; the code at those sites still exhibits the bugs.

This research file documents (a) what the spec says will land, (b) where in the live code each change attaches, (c) the user-visible delta, and (d) the edge cases & interaction patterns the consumer (synthesis sections S16.2 / S20 / S21 / S23 / S24) needs to reason about.

---

## 2. SE-001..005 behavioral inventory

### 2.1 SE-001 — fail-closed empty-output gate

- **Spec source:** RELEASE-SPEC.md:49 (verdict matrix), :122 (surface contract), :510 (migration table), :554 (user-facing impact summary), :381–382 (acceptance test).
- **Change:** Empty output file → `(False, 'empty output file')` instead of soft PASS. STRICT only on the task-surface side; spec language says "sprint runs relying on inconclusive PASS will fail."
- **Behavioral break:** YES (spec §2.2). Spec §6.5 quantifies the user impact as "1-2 new failures per phase during the first week" for sprint owners.
- **Live code context [CODE-VERIFIED]:**
  - `src/superclaude/cli/pipeline/gates.py:20-39` — current `gate_passed(output_file, criteria)` already returns a tuple `(bool, str | None)` and already fails on empty files, *but with the failure reason* `f"File empty (0 bytes): {output_file}"` (line 39), not the spec-mandated `'empty output file'` string.
  - Sprint executor consumes this via `src/superclaude/cli/sprint/executor.py:820,828`: `passed, failure_reason = gate_passed(output_path, ANTI_INSTINCT_GATE)`.
- **What changes for the user:** Today, the sprint emits a verbose path-bearing reason (`"File empty (0 bytes): /tmp/foo.json"`). After SE-001, the literal `'empty output file'` is the failure reason, and the spec frames it as a *new* fail-closed surface — implying the current behavior in *some* code path is permissive. [UNVERIFIED: which sprint-side code path currently soft-passes empty output. The `gate_passed` function is already fail-closed; the SE-001 change must therefore live in a different gate (likely the anti-instinct hook or `_classify_from_result_file` at `executor.py:1683`).]
- **Acceptance test (spec):** `tests/sprint/test_gate_passed_empty_output.py::test_empty_output_returns_false` — file does not yet exist.

### 2.2 SE-002 + SE-003 — per-task UID + sub-phase resume (paired)

- **Spec source:** RELEASE-SPEC.md:50–51 (verdict matrix), :123 (surface contract), :415–419 (acceptance tests), :511 (migration), :607 (PR ordering).
- **Change pair:**
  - SE-002 adds a stable per-task identifier in the **canonical form `f"{phase_id}-{task_index:04d}"`** (from the research-task brief; spec calls this "per-task UID" without naming the format, but the form is the stable-string contract the consumer-side tests must assert against). Result files gain an additional `task_uid` field.
  - SE-003 makes sub-phase resume work by reading the task_uid set in the result file and skipping completed tasks on re-invocation.
- **Behavioral break:** Additive — spec marks "No (additive; graceful fallback per Q10 (a))." Legacy result files without `task_uid` continue to work; resume is just faster when UIDs are present.
- **Live code context:**
  - `src/superclaude/cli/sprint/executor.py:913-1051` — `execute_phase_tasks` is the per-task orchestrator. Today every task is launched unconditionally; no `task_uid` is computed or written [CODE-VERIFIED: `grep -nE 'task_uid|task_index|:04d' src/superclaude/cli/sprint/` returns only an unrelated `D-{i:04d}` artifact-root pattern in `process.py:136`].
  - The closest existing UID is `task.task_id` (e.g. `"T01.01"`), which the executor populates into `TaskResult.task` and which the per-task TUI update writes to `_tui_state.last_task_id` (executor.py:984, 1048).
  - **`f"{phase_id}-{task_index:04d}"` is a NEW key** distinct from `TaskEntry.task_id`. The spec leaves namespace collision to the implementor; the consumer (`/sc:task` synthesis) should treat the two as separate fields.
- **Dependency [CODE-VERIFIED]:** SE-002+SE-003 must land *after* SE-004 ExecutionMode (RELEASE-SPEC.md:607). The Wave-4 checkpoint-heading-parser tests (`tests/sprint/test_checkpoint_parser.py::test_wave4_*`, three tests, RK-15) are a hard pre-merge gate — RELEASE-SPEC.md:480 says they MUST be authored as part of the SE-002+SE-003 PR if they don't exist.

### 2.3 SE-004 — ExecutionMode enum

- **Spec source:** RELEASE-SPEC.md:52, :131 (additive), :385 (test), :605 (independent foundation).
- **Change:** Pure enum addition (`ExecutionMode` with three values per the test spec `test_three_values_present`). No behavior change; landed early in R2 because SE-002+SE-003 depend on it.
- **Behavioral break:** None.
- **Live code context [CODE-VERIFIED]:** No `ExecutionMode` symbol exists in `src/superclaude/cli/sprint/`. The closest existing concept is the dataclass-attribute `execution_mode: str` (default `"claude"`) passed through `parse_tasklist(content, execution_mode=...)` at `config.py:391` and `:487`. SE-004 promotes this string parameter to a typed enum.

### 2.4 SE-005 — GateFailureSeverity enum

- **Spec source:** RELEASE-SPEC.md:53, :132 (additive), :387–389 (tests `test_three_values_present` + `test_tfep_maps_to_severity`/`test_severity_maps_to_tfep`), :651 (Q9 (c) "map TFEP → Sev").
- **Change:** Reporting-taxonomy-only enum addition. The TFEP (Trailing Fail-Escape Path) gate result already classifies failures; SE-005 surfaces a typed `GateFailureSeverity` enum that maps from TFEP outcomes. Spec is explicit ("reporting taxonomy only") that *operational* gate behavior is unchanged.
- **Behavioral break:** None.
- **Live code context [CODE-VERIFIED]:** No `GateFailureSeverity` symbol exists. The current TFEP surface lives in `src/superclaude/cli/pipeline/trailing_gate.py` (referenced from sprint executor.py:1035–1037 `run_post_task_anti_instinct_hook`). SE-005 adds an enum that decorates the existing `TrailingGateResult` — it does not replace it.

### 2.5 Key Takeaways (SE-001..005)

- All five SE rows are **planned, not implemented.** The "post-v3.75 sprint runtime changes" are R2-scope work *for* v3.75; the live tree does not have them yet.
- The user-visible deltas are concentrated in SE-001 (new fail surface) and SE-002+SE-003 (faster resume); SE-004 and SE-005 are invisible to end users (typed enums under the hood).
- The five rows have an explicit PR ordering — **SE-001 → SE-004 → SE-005 → SE-002+SE-003 paired** (RELEASE-SPEC.md:604–607). SE-002+SE-003 are paired; they cannot ship separately.
- The two acceptance-test files that already exist (`tests/sprint/test_gate_passed_empty_output.py`, `tests/sprint/test_task_uid.py`, `tests/sprint/test_subphase_resume.py`, `tests/sprint/test_execution_mode_enum.py`, `tests/sprint/test_gate_failure_severity_enum.py`) are spec-mandated **new** files; the spec is the only place they exist.

---

## 3. Live rendering paths (per-task vs. freeform)

### 3.1 The per-task path is the modern path

[CODE-VERIFIED] `src/superclaude/cli/sprint/executor.py:1234`: `tasks = _parse_phase_tasks(phase, config)` — when this returns a non-empty list (the modern code path; any phase using `### T<PP>.<TT>` headings hits this), control transfers to `execute_phase_tasks(...)` at line 1239. The freeform path beneath (lines 1266–1390) only runs when `_parse_phase_tasks` returns `None`/`[]`.

[CODE-VERIFIED] `execute_phase_tasks` at lines 913–1051:
- Updates the TUI exactly twice per task — at executor.py:980-985 before launch and at 1043-1049 after completion.
- Constructs a **fresh `MonitorState()` each update** (executor.py:981, 1045) and populates only `events_received`, `last_event_time`, `last_task_id`. Every other MonitorState field stays at its dataclass default (`stall_seconds=0.0`, `growth_rate_bps=0.0`, `activity_log=[]`, `last_assistant_text=""`).
- No `OutputMonitor` is instantiated or started in this function. The grep `grep -nE 'OutputMonitor|monitor.start' src/superclaude/cli/sprint/executor.py` confirms `monitor.start()` appears only on the freeform path at line 1277.

### 3.2 The freeform path has the live monitor

[CODE-VERIFIED] `executor.py:1271-1390`:
- Line 1276: `monitor.reset(output_path, phase_file=phase.file)` — `MonitorState` constructed with `phase_started_at = time.monotonic()` (models.py:610 default factory).
- Line 1277: `monitor.start()` spins up the 0.5 s polling thread.
- Lines 1303–1381: poll loop calls `tui.update(sprint_result, monitor.state, phase)` once per 500 ms tick.

So **the live `MonitorState` only flows to the renderer on the freeform path.** On the per-task path the renderer sees a series of empty `MonitorState()` snapshots — confirmed by reading the literal construction sites at executor.py:981 and 1045.

### 3.3 Rich.Live cadence

[CODE-VERIFIED] `src/superclaude/cli/sprint/tui.py:101-106`:
```
self._live = Live(
    self._render(),
    console=self.console,
    refresh_per_second=2,
    screen=False,
)
```
`Live` re-renders the *same renderable tree* every 500 ms on its background thread, regardless of executor pushes. Any dynamic field — spinner glyph, `SprintResult.duration_display` (computed against `datetime.now()`), idle counters using `time.time()` — animates without an executor call. Static fields (`MonitorState.stall_seconds`, `last_assistant_text`, etc.) are *frozen* between explicit `tui.update(...)` calls.

This is the architectural lever P-05 (spinner) exploits.

### 3.4 Key Takeaways (rendering paths)

- The per-task path is the **dominant user-experience path** today and is also the broken one — it cannot animate intra-task because no monitor feeds it.
- The freeform path works as designed, but its Duration column still reads `stall_seconds` (the *idle gap*, not phase-elapsed) — a categorical mislabel P-02 fixes.
- The 2 Hz `Live.refresh_per_second` is the resource the cosmetic fixes (P-05 spinner, P-02 Duration recompute, P-03 width-aware truncate) all ride on.

---

## 4. TUI top-5 acceptance criteria (P-01 / P-05 / P-02 / P-03+P-07)

The ship order is **P-05 → P-02 → P-03+P-07 → P-01** (RELEASE-SPEC.md:610–613, FINAL-REPORT.md:858, TUI-ADVERSARIAL.md sequencing block). Ranking order is different: P-01 leads the ranked top-5 but ships LAST because it is the keystone — see §5 below.

### 4.1 P-01 — Wire OutputMonitor into the per-task path (keystone)

- **Viability:** 92 (TUI-ADVERSARIAL §1) — highest in the slate.
- **Symptoms addressed:** §2.1 (hang) + §2.2 (no real-time) per TUI-ANALYSIS.
- **Code surface [CODE-VERIFIED]:** `executor.py:913-1051` (`execute_phase_tasks`) and `executor.py:1054-1093` (`_run_task_subprocess`). The freeform poll-loop pattern at `executor.py:1303-1381` is the template.
- **Concrete change:**
  - Instantiate `OutputMonitor` once per phase before the for-loop (analogous to executor.py:1276–1277).
  - In each per-task iteration, call `monitor.reset_for_next_task()` (a NEW public method specified by the mitigation contract) — *not* `monitor.reset(output_path)` because that would discard `total_tasks_in_phase`.
  - Replace `proc.wait()` with a poll loop: `while proc._process.poll() is None: tui.update(sprint_result, monitor.state, phase); time.sleep(0.5)`.
- **Mandatory mitigation contract (TUI-ADVERSARIAL §1, RELEASE-SPEC.md:454-461):**
  1. New test file `tests/sprint/test_monitor_reset_between_tasks.py` with `test_events_received_equals_6_after_two_3_event_tasks_with_reset` and `test_last_read_pos_correct_after_reset`.
  2. `OutputMonitor.reset_for_next_task()` public method must exist and be idempotent.
  3. P-01 ships LAST in the TUI sequence — "fireworks landing" rationale (§5).
- **Acceptance (TUI-ADVERSARIAL Manual Smoke-Test block):**
  - ACCEPT: 3-task per-task phase shows Tasks bar advancing at task boundaries (not in one jump); Activity log shows ≥1 event per task; `growth_rate_bps` is nonzero; **NDJSON event count from the file matches TUI-displayed count within 1, across phase boundaries** (INV-001/005 invariant).
  - REJECT: Bars still jump in one step at phase end; Activity log shows `— — —` for the full task; `growth_rate_bps` stays at zero.
- **Risks named in adversarial:** (a) OutputMonitor reset hazard — incremental-read pointer must reset between tasks or first task's output is skipped; (b) threading model change for most-used path; (c) underscore coupling to `proc._process.poll()` — recommend adding `ClaudeProcess.is_running()`.

### 4.2 P-05 — Rich spinner on RUNNING + active-panel title (ships first)

- **Viability:** 88 (TUI-ADVERSARIAL §2).
- **Symptoms addressed:** §2.2 (no real-time).
- **Code surface [CODE-VERIFIED]:**
  - `tui.py:58-72` — `STATUS_ICONS` dict; the RUNNING entry is `"[yellow]RUNNING[/]"` (line 69) — pure static markup.
  - `tui.py:408-412` — active panel title `f"[bold yellow]ACTIVE: Phase {self.current_phase.number}[/]"`.
  - `tui.py` imports list at line 11 — `from rich.live import Live` is present; `from rich.spinner import Spinner` is **not** [CODE-VERIFIED].
- **Concrete change:**
  - Import `from rich.spinner import Spinner`.
  - In `_build_phase_table` (tui.py:221), when `status == PhaseStatus.RUNNING`, replace the cell value with `Spinner("dots", text="RUNNING", style="yellow")` instead of `STATUS_ICONS[PhaseStatus.RUNNING]`.
  - In `_build_active_panel` (tui.py:360), prepend a `Spinner("dots2")` to the panel title.
- **Why it ships first:** Zero coupling — Rich.Live's 2 Hz auto-refresh re-renders the spinner state every tick without any executor call. P-05 delivers "the dashboard is alive" feedback even before P-01 lands and even when the per-task path is silent.
- **Acceptance:** Within 2 s of sprint start, RUNNING row's status cell shows a visible cycling glyph; active-panel title also cycles. When the executor is intentionally paused (PreFlight), the spinner *continues* to cycle (proves it anchors to `Live.refresh_per_second`, not push events).
- **Risks named:** (a) false-positive risk — spinner that animates while subprocess is genuinely hung still implies progress (mitigated by P-10 follow-on heartbeat); (b) snapshot rebaseline cost for table tests; (c) two-spinner synchronicity.

### 4.3 P-02 — Elapsed-since-phase-start in Duration column

- **Viability:** 82.
- **Symptoms addressed:** §2.1 (hang appearance) + §2.2 (clearer real-time signal).
- **Code surface [CODE-VERIFIED]:**
  - `tui.py:265-273` — Duration cell currently reads `f"{int(self.monitor_state.stall_seconds)}s"` when `status == PhaseStatus.RUNNING`. That is the idle gap since last NDJSON event, not phase-elapsed.
  - `models.py:610` — `phase_started_at: float = field(default_factory=time.monotonic)` already exists on `MonitorState`.
- **Concrete change:** Replace the line 269 expression with `f"{int(time.monotonic() - self.monitor_state.phase_started_at)}s"`. Optional `m:ss` formatting when ≥60 s.
- **Acceptance:**
  - ACCEPT: Duration ticks up monotonically every second for the running phase; never decreases; matches wall-clock ±1 s after phase ends.
  - REJECT: Duration shows `0s` while phase is running (means SE-001 + the per-task `MonitorState()` issue still dominates — see Risks); Duration decreases when new events arrive (means original `stall_seconds` is still being read).
- **Risks named:** (a) **INV-002 dual-writer hazard** — `phase_started_at` is set by `monitor.reset(...)` (monitor.py:308 [CODE-VERIFIED — `new_state = MonitorState()` at line 305, then assigned at line 308; default factory fires when constructed]) which is *not* called on the per-task path today. Until P-01 lands, the per-task path's `MonitorState()` constructions at executor.py:981, 1045 each get a *fresh* `phase_started_at = time.monotonic()`, so Duration reads ~0 throughout the task. Fix: pair P-02 with P-01 OR wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of a `current_phase` change.
  - (b) Semantics change — on freeform path today Duration *decreases* when output arrives; users who learned this as a "thinking-gap indicator" lose that signal. Spec recommends a changelog note.

### 4.4 P-03 + P-07 — Width-aware truncation (combined PR)

- **Viability:** P-03=78, P-07=70.
- **Symptoms addressed:** §2.3 (cut-off).
- **Code surface [CODE-VERIFIED]:**
  - `tui.py:34` — `_LLM_LINE_MAX = 60` constant.
  - `tui.py:386-387` — `prompt_text = _truncate(self.current_phase.prompt_display, _LLM_LINE_MAX)`; `agent_text = _truncate(ms.last_assistant_text, _LLM_LINE_MAX)`.
  - `tui.py:80` — `self.console = console or Console()` (Rich auto-detects width but the renderer never reads it).
  - `tui.py:424` — `truncated = _truncate(desc, 50)` (activity-stream description cap).
  - `tui.py:459, 539` — error-message caps of 80 chars (`_truncate(message.replace("\n", " "), 80)` appears at both lines).
  - `monitor.py:121` — `ASSISTANT_TEXT_MAX_LEN = 80`; `monitor.py:466-467` — `if len(tail) > ASSISTANT_TEXT_MAX_LEN: tail = tail[-ASSISTANT_TEXT_MAX_LEN:]` (extraction-time pre-trim).
  - `config.py:179, 193, 203, 204` — four `[:60]` slices in `_extract_phase_prompt_preview` (config.py:167-204).
- **Concrete change (P-03):**
  1. Bump `config.py` extraction-time caps from `[:60]` to `[:240]` (or remove the slice entirely and let the renderer decide).
  2. In `_build_active_panel`, compute `avail = max(40, self.console.width - 14)` (panel-border + `Prompt:  ` prefix budget) and pass to `_truncate`.
  3. Apply to Agent: line, error messages, and activity-stream descriptions.
- **Concrete change (P-07):** Stop trimming in `monitor.py:466-467` (or raise the cap to ~400 chars as a 4 KB monitor-memory budget). Move the trim to render-time using the P-03 width budget.
- **Why ship together:** TUI-ADVERSARIAL §3 ¶3: P-03 alone leaves the Agent: line clipped at 80 (because `ASSISTANT_TEXT_MAX_LEN = 80` pre-trims in the monitor before the renderer ever sees the full text). The two are a "classic two-stage lossy-compression bug" — P-07 fixes the layering by making the monitor store, renderer trim.
- **Mandatory mitigation — INV-004 audit (TUI-ADVERSARIAL §4 ¶2, RELEASE-SPEC.md:393):** 15-minute pre-merge grep audit of `Phase.prompt_preview` consumers to confirm no log formatter or error reporter assumes ≤60. The audit is documented in the PR.
- **Acceptance:**
  - ACCEPT: On a 200-column terminal, the Prompt: line displays text wider than 60 chars AND the Agent: line displays wider than 80 chars; resizing terminal mid-sprint reflows the next render; panel does not flicker height-wise.
  - REJECT: Prompt: line widens but Agent: line stays at 80 (P-07 not properly applied); panel height flickers; long prompts wrap to a second line (truncation math off).
- **Risks named:** (a) panel-height flicker if math is off-by-one against border + padding; (b) INV-004 downstream-consumer audit must complete pre-merge; (c) half-fix without P-07; (d) ANSI escape sequences from echoed tool output — TUI-ADVERSARIAL §5 ¶2 recommends a `Text.from_ansi` or strip-ansi render-time pass; not in proposal as written.

### 4.5 Key Takeaways (top-5)

- The five fixes are **all on tui.py / monitor.py / config.py boundaries**; none of them touch the SE-001..005 surface in executor.py. The two work streams (sprint runtime SE-* and TUI top-5) are independent, only sharing R2 release status.
- P-01 is the single fix that wires *new data* into the per-task path; the other four operate on data Rich.Live can already see (P-05 spinner, P-02 phase_started_at, P-03+P-07 width).
- Each fix has a named acceptance test in RELEASE-SPEC §5; only P-01's is mandatory (`test_monitor_reset_between_tasks.py`). The others are smoke-tested per FINAL-REPORT §11.5.

---

## 5. Ship order rationale — "fireworks landing"

[CODE-VERIFIED via direct read of FINAL-REPORT.md:858] The phrase originates in Variant A's structural-correctness lens of the adversarial debate; it was ratified by Variant C's per-day ROI methodology and Variant B's saliency weighting. The exact rationale, from TUI-ADVERSARIAL.md ¶168:

> "Days 3–5 — P-01 (OutputMonitor on per-task path): The keystone. Lands with the cosmetic fixes already in place, so the day P-01 ships the user sees *everything come alive simultaneously* — the spinner is alive (was already), the bars are alive (newly), Duration ticks correctly (newly), prompt and agent lines are full-width (already), the activity stream populates (newly). **This is the 'fireworks landing'** — Variant A's term, ratified by C's independent day-numbered timing and B's saliency analysis."

Three reinforcing reasons:

1. **Visibility timing.** P-05 ships Day 1 → users see motion immediately. P-02, P-03+P-07 by Day 2.5 → users see correct Duration & full-width prompts. Then on Day 3-5 P-01 lights up the activity stream, growth rate, and Tasks-bar advancement — *all at once*, against an already-polished dashboard.

2. **Risk shape.** P-01 is the only M-effort fix in the slate and the only one that touches `proc.wait()` / threading model. Shipping it last means the cosmetic fixes can be reviewed, merged, and validated independently — and if P-01 needs another revision, the dashboard still looks polished.

3. **Per-day ROI math (TUI-ADVERSARIAL ¶25).** P-05 delivers ~30% of §2.2 resolution per engineering-day (1-day ship); P-01 delivers ~80% of §2.1+§2.2 per engineering-day-equivalent (2.5-day ship → 32%/day). The two are within noise on per-day return. The tiebreak goes to P-01 on *impact magnitude*, while the *sequencing* honors C's "ship certain wins first" intuition.

### 5.1 Key Takeaways (ship order)

- P-01 ranks #1 but ships LAST. This is intentional; consumers (S21 Implementation Plan) must reproduce both pieces of metadata.
- The "fireworks landing" is the user-visible outcome — not a metric in itself but a UX experience: by Day 5, every dashboard element transitions from "mostly frozen" to "mostly alive" in one merge.
- Total wave cost: ~5 engineering-days (TUI-ADVERSARIAL ¶170, RELEASE-SPEC.md:574).

---

## 6. Mandatory mitigations from TUI-ADVERSARIAL

Four named mitigations span the top-5 PRs. Consumer (S20 Risk Analysis → RK-TUI-01..05) must enumerate each.

### 6.1 Reset-test (INV-001 / INV-005) — mandatory for P-01

[CODE-VERIFIED RELEASE-SPEC.md:454-461 and TUI-ADVERSARIAL §1 mitigation block]

- New test file `tests/sprint/test_monitor_reset_between_tasks.py` with two tests:
  - `test_events_received_equals_6_after_two_3_event_tasks_with_reset` — writes 3 events for task 1, calls `monitor.reset_for_next_task()`, writes 3 events for task 2, asserts `monitor.state.events_received == 6`.
  - `test_last_read_pos_correct_after_reset` — asserts `_last_read_pos` is at the correct file offset after each reset.
- `OutputMonitor.reset_for_next_task()` must be:
  - **Public** (no underscore prefix).
  - **Idempotent** against partial-read state — if called mid-task, finish the in-flight read before resetting.
  - **Distinct from `OutputMonitor.reset(output_path, phase_file=...)`** [CODE-VERIFIED that today there is only `reset(...)` at monitor.py:291-308 which discards `total_tasks_in_phase` by constructing a fresh `MonitorState`. The new method must preserve phase-scoped fields and only reset task-scoped ones].
- INV-001 = "events flowing through the file are observable downstream." INV-005 = "monitor state advances strictly forward; the reset operation does not re-emit a stale value."

### 6.2 INV-004 audit — mandatory pre-merge for P-03

[CODE-VERIFIED RELEASE-SPEC.md:393 and TUI-ADVERSARIAL §3 risk ¶2]

15-minute grep audit of `Phase.prompt_preview` consumers to confirm no log formatter / error reporter / JSONL writer assumes the value is ≤60 chars. The audit must be documented in the P-03 PR. The cap is being raised from 60 to 240 chars (or removed entirely); downstream truncation must be width-derived, not assumed.

### 6.3 ANSI pass — recommended (not strictly mandatory) for P-03+P-07

[CODE-VERIFIED TUI-ADVERSARIAL §5 risk ¶2]

> "Activity-stream and error strings can contain raw ANSI if a tool echoed them. Proposal acknowledges; recommend a `Text.from_ansi` or strip-ansi render-time pass — not in proposal as written."

Risk: when full strings are stored (P-07 raises monitor cap to 400 chars), raw `\x1b[31m` sequences will be carried through to the renderer. Rich's `Text.from_markup` handles `[...]` syntax but not ANSI CSI sequences; literal escape codes will render as garbled characters. Mitigation: pipe assistant-text and activity-description strings through `Text.from_ansi(...)` (Rich-native ANSI→Text decoder) at the render-time truncate site in `_build_active_panel`.

### 6.4 Layering correction — structural value-add of P-07

[CODE-VERIFIED TUI-ADVERSARIAL §5 ¶2]

> "It relocates the assistant-text trim out of the monitor entirely. The current arrangement (monitor pre-trims to 80, renderer further trims to 60) is a classic two-stage lossy-compression bug — by the time the renderer has the string it cannot widen it even if the terminal grew. P-07 makes the layering clean: monitor stores, renderer trims."

Concrete: remove or raise the `ASSISTANT_TEXT_MAX_LEN = 80` constant in `monitor.py:121` (and the slicing at `monitor.py:466-467`); push truncation entirely into the `_build_active_panel` / `_render_activity_stream` render path. After this change the monitor's job is "extract & store"; the renderer's job is "fit to width." The two responsibilities never overlap.

### 6.5 Two outstanding MEDIUM invariants (TUI-ADVERSARIAL §Convergence Statement)

- **INV-002** — `phase_started_at` dual-writers. P-02 fix introduces a TUI-side writer if shipped before P-01. Accepted as a follow-on cleanup *after* P-01 lands (which makes the monitor the single source).
- **INV-004** — `prompt_preview` downstream-consumer audit (§6.2 above). Mandatory pre-merge for the P-03 PR.

### 6.6 Key Takeaways (mitigations)

- The reset-test for P-01 is the **single most important pre-merge artifact** in R2 — TUI-ADVERSARIAL §1 names it as a "load-bearing acceptance criterion."
- INV-004 is a 15-minute audit, not a coding task — but skipping it could break log formatters that grep `prompt_preview` for short identifiers. Consumer (S20) must record this as a risk and an action.
- ANSI handling is **not in any proposal as written** — TUI-ADVERSARIAL flags it but no PR is committed. The synthesis should surface this as an open question for the implementation kickoff.

---

## 7. Error and edge cases

### 7.1 Empty output file (SE-001)

- **Today [CODE-VERIFIED gates.py:38-39]:** `gate_passed` returns `(False, f"File empty (0 bytes): {output_file}")`. The path is included in the failure reason. This is *already* fail-closed at the `gate_passed` layer.
- **After SE-001:** The failure reason becomes the literal `'empty output file'`. Spec §6.5 implies that *some* sprint-side code path today permissively soft-passes empty output despite `gate_passed` being fail-closed. [UNVERIFIED — exact soft-pass site. Most likely candidates: anti-instinct hook short-circuits at executor.py:828, `_classify_from_result_file` at executor.py:1683, or `_determine_phase_status` at executor.py:1976.]
- **User visibility:** Sprint runs that previously "succeeded with no output" emit a clearer failure reason; "1-2 new failures per phase during the first week" per spec §6.5.

### 7.2 Missing checkpoint (SE-003 sub-phase resume)

- **Today [CODE-VERIFIED executor.py:1720-1803]:** `_verify_checkpoints` runs at end-of-phase per `config.checkpoint_gate_mode` (off/shadow/soft/full). In `full` mode missing checkpoints set the phase to `PASS_MISSING_CHECKPOINT`. The checkpoint manifest is written at sprint-end (executor.py:1623-1644). There is no per-task resume that consults the manifest to skip already-completed tasks.
- **After SE-002+SE-003:** Result file gains `task_uid` field; sub-phase resume reads the result file, builds the set of completed `task_uid`s, and skips them when re-invoked with `--start <phase>`. Graceful fallback (Q10 (a)) means a legacy result file without `task_uid` re-runs every task — not a regression.
- **Edge case:** Partial-result resume. If a sprint dies mid-task (subprocess crash, `KeyboardInterrupt`), the result file has N-1 completed tasks plus a partial Nth entry without finish timestamp. Spec §2.2 implies the resume logic must treat the Nth task as "not done" and re-launch. Form `f"{phase_id}-{task_index:04d}"` is the stable key the resume logic groups by.

### 7.3 TUI hang on long output

[CODE-VERIFIED executor.py:1304-1311, 1330-1364] The sprint executor already has a stall-watchdog with `config.stall_timeout`. On the freeform path:
- `ms.stall_seconds > config.stall_timeout AND ms.events_received > 0` triggers a single-fire watchdog action (`kill` or `warn`).
- On `kill`, the process is terminated; exit code is set to 124 (timeout).
- Reset: `if _stall_acted and ms.stall_seconds == 0.0` clears the guard.

The TUI itself has independent protection [CODE-VERIFIED executor.py:1370-1380]: `tui.update(...)` is wrapped in `try/except` so a display glitch cannot abort the sprint. The TUI sets `self._live_failed = True` on first render error [CODE-VERIFIED tui.py:130-152] and silences subsequent updates.

**Per-task path edge case [CODE-VERIFIED]:** The poll loop / watchdog logic at executor.py:1303-1381 lives *only* on the freeform path. The per-task path uses `proc.wait()` (called inside `_run_task_subprocess` at executor.py:1054-1093) which blocks unconditionally. **There is no stall watchdog for per-task subprocesses today.** P-01 fixes this by replacing `proc.wait()` with a poll loop. Until P-01 lands, a hung per-task subprocess hangs the sprint with no timeout enforcement beyond the subprocess-level `timeout_seconds`. This is a significant edge case for synthesis S23.

### 7.4 Prompt cut-off (P-03+P-07 target)

- **Today [CODE-VERIFIED]:** Double-truncation at `config.py:179,193,203,204` (`[:60]` extraction-time) AND `tui.py:386` (`_truncate(..., _LLM_LINE_MAX=60)` render-time). Console width is never read.
- **After P-03+P-07:** Extraction-time cap raised to 240; render-time cap is `max(40, console.width - 14)`; monitor cap raised to 400 chars or removed.
- **Edge case — wider terminal still clipped before fix:** The user's reported symptom. The fix is width-aware but not unbounded; very wide terminals (>250 chars) still clip at the extraction-time cap of 240 unless that is also raised. The 240 cap is a "soft limit" for log-formatter compatibility, not a hard UX limit.
- **Edge case — flickering height:** If `_truncate` math is off by one against panel border + padding, the prompt wraps to two lines, panel height changes, every Live tick re-paints with shifted content. Mitigation: pre-compute `avail` and pad/truncate to that exact width.

### 7.5 Partial result resume via task_uid stable form

- The stable-form contract `f"{phase_id}-{task_index:04d}"` (from the research brief) is the cross-session resume key. Properties:
  - **Phase-scoped:** Same `task_index` in different phases produces different UIDs.
  - **Sortable:** Zero-padded `:04d` means string sort matches integer sort.
  - **Idempotent:** Computed from inputs available at task-iteration time (executor.py:957 `for i, task in enumerate(tasks)`).
- **Edge case — task reordering:** If the user edits the tasklist between sprint invocations and adds a task at position 3, all `task_index ≥ 3` shift by one. The UID for the *new* task 5 was the old task 4's UID. Resume would skip the wrong task. Mitigation [UNVERIFIED — not in spec as written; consumer should flag as an open question]: combine `task_index` with a stable content hash, OR detect tasklist drift and force full re-run.

### 7.6 Key Takeaways (edge cases)

- The **per-task stall watchdog is missing today** — this is a latent bug P-01 incidentally fixes by replacing `proc.wait()` with a poll loop.
- SE-001's "fail-closed" framing is at least partially redundant with the existing `gate_passed` fail-closed behavior; the spec implies a *different* code path soft-passes empty output today. Synthesis should treat SE-001 as "find and close the remaining soft-pass surface" rather than "introduce fail-closed semantics from scratch."
- Partial-result resume via `task_uid` is the headline SE-003 user benefit; the tasklist-drift edge case is not addressed in the spec as written.

---

## 8. User interaction patterns

### 8.1 RUNNING spinner (P-05 interaction)

- **Before fix [CODE-VERIFIED tui.py:69]:** Status cell for RUNNING phase shows the static markup `"[yellow]RUNNING[/]"` — yellow text, no motion.
- **After fix:** `Spinner("dots", text="RUNNING", style="yellow")` advances frames at Rich's default `dots` cadence (~10 Hz internally; visible at 2 Hz `Live.refresh_per_second`). The active-panel title also spins (`Spinner("dots2")`).
- **User mental model:** "Spinner cycling = process is alive." This is universally understood; the risk is *false reassurance* — a spinner that cycles while the subprocess is truly hung (P-05 risk #1 in TUI-ADVERSARIAL). Mitigation is the follow-on P-10 heartbeat that exposes time-since-last-event.
- **Interaction with executor pauses:** Even when the executor is in PreFlight (long sync I/O) or transitioning between phases, the spinner continues cycling because Rich.Live's refresh thread is independent of executor pushes [CODE-VERIFIED tui.py:101-106].

### 8.2 Duration column behavior (P-02 interaction)

- **Before fix [CODE-VERIFIED tui.py:265-273]:** Three possible Duration values:
  - Terminal-status phase: `result.duration_display` (correct).
  - RUNNING phase: `f"{int(self.monitor_state.stall_seconds)}s"` — *idle gap since last NDJSON event*. Decreases when output arrives, increases during thinking. Erratic.
  - PENDING phase: `"-"`.
- **After fix:** RUNNING phase reads `f"{int(time.monotonic() - self.monitor_state.phase_started_at)}s"` — monotonically increasing wall-clock elapsed.
- **User mental model:** "Duration is wall-clock time the phase has been running." This is the conventional reading; the current implementation violates it.
- **Visual behavior:** Ticks once per Rich.Live refresh tick (500 ms). At human perception threshold for change-detection (~250 ms), the user sees a steady increment every other tick — a noticeable "moving number."
- **Edge case [TUI-ADVERSARIAL §3 risk ¶2]:** Sub-second phases (≤0.9 s) show `0s` then jump to `1s` on completion. Not a regression but worth noting; the spec recommends a changelog note.

### 8.3 Width-aware truncation at 60 chars and beyond (P-03+P-07 interaction)

[CODE-VERIFIED multiple file sites]

- **At terminal width 80 columns:** `avail = console.width - 14 = 66`. Prompt and Agent lines fit in 66 chars; `_truncate` clips to 63 chars + `"..."` if longer.
- **At terminal width 60 columns:** `avail = max(40, 60 - 14) = 46`. Lines clip more aggressively but stay on one line.
- **At terminal width 200 columns:** `avail = 186`. Full prompt visible up to the extraction cap of 240 chars (or 400 for assistant text).
- **At terminal width 40 columns (the floor):** `avail = max(40, 40 - 14) = 40`. The `max(40, ...)` floor prevents pathological widths from rendering as a 0-char ellipsis.
- **Resize behavior:** Rich.Console auto-detects width on each render. Resizing mid-sprint causes the *next* Live tick (≤500 ms later) to re-truncate at the new width. The user perceives a near-instant reflow.
- **Flicker risk:** If `avail` computation is off by one relative to panel border + padding, a "borderline" prompt wraps to two lines on tick N and fits on one line on tick N+1, causing the panel height to oscillate. Mitigation: explicit pre-computation against panel border = 2, padding = 2 (lines 192-197 in tui.py: `padding=(1, 2)`). So budget = `console.width - 14` (border 2 + padding 2 × 2 = 6 + `Prompt:  ` prefix 9 = 15, rounded to 14 per the proposal).
- **Boundary at 60 chars:** This is the legacy hard cap. Users on 80-column terminals (the historical default) see *no* change from P-03+P-07 because `avail = 66` is barely larger than the old cap of 60. The fix is **only visible to users with wider terminals**. Acceptance criterion ("on a 200-column terminal the Prompt: line displays text wider than 60 chars") explicitly tests the wide-terminal case.

### 8.4 Activity stream and thinking-indicator interactions

[CODE-VERIFIED tui.py:404-435]

- The activity stream renders three lines of `(timestamp, tool_name, description)` tuples from `MonitorState.activity_log` (capped at `ACTIVITY_LOG_MAX = 3` in monitor.py:117).
- When idle exceeds `_THINKING_IDLE_SECONDS = 2` (tui.py:38), the last line is replaced with `[thinking... Ns]`.
- On the per-task path today: `activity_log` is always empty (no monitor running), so the user sees three `—` lines for the entire task. P-01 fixes this by wiring the monitor.
- After P-01: activity stream populates in real time; thinking indicator appears between tool calls; growth-rate-bps is nonzero.

### 8.5 Key Takeaways (interaction patterns)

- The TUI top-5 fixes transform the user experience from "two-jump status updates with frozen middle" to "continuously animated dashboard." The transformation is *all-at-once* by design (fireworks landing).
- The 60-char vs. wider-terminal distinction is the only acceptance criterion that requires testing on multiple terminal widths; smoke tests must cover at minimum {80, 200}-column.
- The spinner's false-reassurance risk and the Duration column's sub-second flicker are minor but real UX caveats the synthesis should surface in S24.

---

## 9. Test baseline and regression boundary

[CODE-VERIFIED RELEASE-SPEC.md:473-486]

- **Sprint suite baseline:** 921 passed / 57 failed. New failures introduced by R2 must be net-new (not pre-existing).
- **TUI Waves 1-2 + tmux + summarizer + retrospective:** 125/125 pass. Must remain 125/125 after the top-5 land.
- **`test_process.py::TestClaudeProcess`:** 16/16 including `test_build_prompt_contains_task_command`. Must remain 16/16.
- **Coverage target:** 80% line coverage on new code (`audit.py`, SE-001..005). 100% on `audit.py` (security-sensitive write path; not in R2 scope but called out for cross-reference).
- **Wave-4 checkpoint heading parser:** +3 tests must pass (RK-15). Specific paths from RELEASE-SPEC.md:480:
  - `tests/sprint/test_checkpoint_parser.py::test_wave4_task_checkpoint_heading_form`
  - `::test_wave4_legacy_heading_back_compat`
  - `::test_wave4_checkpoint_manifest_uses_label_not_basename`
  These MUST be authored as part of the SE-002+SE-003 PR if they do not already exist.

[UNVERIFIED — whether these test files currently exist in `tests/sprint/`. Spec language is conditional: "If these tests do not yet exist in `tests/sprint/`, they MUST be authored as part of the SE-002+SE-003 PR before merge."]

---

## 10. Synthesis-Mapping Cross-References

For downstream consumer (S16.2 / S20 / S21 / S23 / S24):

- **S16.2 Core User Flows — TUI interaction:** §8 of this file (interaction patterns) + §3 (rendering paths) + §4 (top-5 acceptance criteria).
- **S20 Risk Analysis — RK-TUI-01..05:**
  - RK-TUI-01: OutputMonitor reset hazard (§6.1 INV-001/005).
  - RK-TUI-02: phase_started_at dual-writers (§4.3, §6.5 INV-002).
  - RK-TUI-03: prompt_preview downstream-consumer audit (§6.2 INV-004).
  - RK-TUI-04: false-reassurance spinner (§4.2 risk ¶a).
  - RK-TUI-05: panel-height flicker (§4.4 risk ¶a, §8.3 flicker risk).
- **S21 Implementation Plan — TUI sub-section + ship order:** §4 (per-fix code surface) + §5 (fireworks-landing rationale) + §6 (mandatory mitigations).
- **S23 Error Handling & Edge Cases:** §7 (empty output, missing checkpoint, TUI hang, prompt cut-off, partial result resume) + §7.3 critical finding on missing per-task stall watchdog.
- **S24 User Interaction & Design:** §8 (RUNNING spinner, Duration column, width-aware truncation at 60-chars-and-beyond, activity stream).

---

## Gaps and Questions

- **G1.** [UNVERIFIED] Exact location of the "soft-pass empty output" code path SE-001 is targeting. `gate_passed` is already fail-closed; some other gate is permissive. Likely candidates: `_classify_from_result_file` (executor.py:1683), `_determine_phase_status` (executor.py:1976), or the anti-instinct hook short-circuit (executor.py:828). Implementation kickoff should grep for `return True.*output` or `passed = True` near classification logic. **Phase 3 follow-up:** a focused grep `return (True|False)|passed = True|status.*PASS` across `executor.py` filtered for classify/determine_phase/anti_instinct/hook returned zero matches in the executor body — the soft-pass surface is NOT a simple boolean return. Elevate to S13/S21 as an explicit PRD-level open question (implementation kickoff must trace the actual code path during SE-001 PR scoping). `[inference]` retained.
- **G2.** [UNVERIFIED] Whether `tests/sprint/test_checkpoint_parser.py::test_wave4_*` tests currently exist in the repo. Spec assumes they may or may not; the SE-002+SE-003 PR author owns authoring them if missing.
- **G3.** [UNVERIFIED] How `f"{phase_id}-{task_index:04d}"` handles tasklist drift (user adds/removes tasks between sprint runs). Spec is silent on detection/mitigation; consumer should treat this as an open implementation question.
- **G4.** [UNVERIFIED] ANSI escape handling in P-07. TUI-ADVERSARIAL §5 flags raw `\x1b[...]` sequences in echoed tool output but no PR commits to the `Text.from_ansi` mitigation. Implementation kickoff should decide whether to ship P-07 with ANSI passthrough or pre-strip.
- **G5.** [UNVERIFIED] Per-task stall watchdog after P-01. The freeform path has `config.stall_timeout` enforcement at executor.py:1330-1364; P-01 replaces `proc.wait()` with a poll loop but the spec doesn't explicitly require the stall watchdog to be ported to the per-task path. Recommend confirming during P-01 implementation.
- **G6.** The three SE-004 / SE-005 enum values are named in tests (`test_three_values_present`) but not enumerated in the spec text. Synthesis cannot list the concrete enum members without reading the test specs once authored.

## Stale Documentation Found

- **SD-1.** TUI-ANALYSIS.md ¶33 cites `Phase.prompt_preview` at `models.py:296`. [CODE-VERIFIED]: `prompt_preview: str = ""` is at `models.py:296` of the live tree. **Not stale.**
- **SD-2.** TUI-ANALYSIS.md ¶33 cites `MonitorState` at `models.py:590-657`. [CODE-VERIFIED]: class definition starts at `models.py:591` (not 590, off-by-one within a doc comment). **Effectively current.**
- **SD-3.** TUI-ANALYSIS.md ¶34 cites `_extract_phase_prompt_preview` at `config.py:167`. [CODE-VERIFIED]: function starts at `config.py:167`. **Current.**
- **SD-4.** TUI-ANALYSIS.md ¶57 cites `executor.py:1088` for `proc.wait()`. [CODE-VERIFIED]: `_run_task_subprocess` is at `executor.py:1054-1093`; current code uses `_Base.__init__` and `ClaudeProcess` machinery rather than a literal `proc.wait()` call in the executor body. The architectural claim ("subprocess blocks") still holds — the wait happens inside `ClaudeProcess` — but the exact line citation is **slightly stale.**
- **SD-5.** TUI-ANALYSIS.md ¶33 cites monitor caps `ACTIVITY_LOG_MAX=3, ERRORS_MAX=10`. [CODE-VERIFIED monitor.py:117,119]: `ACTIVITY_LOG_MAX = 3` and `ERRORS_MAX = 10`. **Current.**
- **SD-6.** TUI-ANALYSIS.md ¶60 cites `_LLM_LINE_MAX = 60` at `tui.py:34`. [CODE-VERIFIED]: `_LLM_LINE_MAX = 60` at `tui.py:34`. **Current.**
- **SD-7.** RELEASE-SPEC.md:454-461 references `OutputMonitor.reset_for_next_task()` as a new public method. [CODE-CONTRADICTED in the sense that this method does not yet exist]: only `OutputMonitor.reset(new_output_path, phase_file=...)` exists at `monitor.py:291-308`. Not stale-doc but a planned addition; mentioned here so consumer doesn't assume the method exists.

## Summary

The SE-001..005 sprint-runtime changes (R2 work-stream) and the TUI top-5 fixes are **both planned but not implemented** in the live tree as of branch `feat/workspace-rca-remediation`. RELEASE-SPEC.md and TUI-ADVERSARIAL.md are the authoritative behavioral inventory; live code at the cited file:line positions shows the *change sites*, not the *new behavior*.

Key facts the synthesis consumer must carry forward:

1. **Per-task path is the dominant user-experience path** and the broken one. `execute_phase_tasks` (executor.py:913-1051) constructs a fresh empty `MonitorState()` for each of the two per-task TUI updates and never starts an `OutputMonitor`. P-01 is the keystone that wires the monitor in; everything else in the top-5 is cosmetic.

2. **Ship order is reversed from rank order.** P-05 → P-02 → P-03+P-07 → P-01. P-01 ranks #1 but ships LAST so it lands "on top of cosmetic fixes" — the "fireworks landing" rationale.

3. **Three mandatory mitigations:** (a) `tests/sprint/test_monitor_reset_between_tasks.py` for P-01 with `OutputMonitor.reset_for_next_task()` public method (INV-001/005); (b) INV-004 15-minute downstream-consumer audit pre-merge for P-03; (c) Wave-4 checkpoint-parser tests for SE-002+SE-003 (RK-15).

4. **SE-001 is partially redundant** with the existing `gate_passed` fail-closed behavior — implementation must find and close the remaining soft-pass surface elsewhere in the sprint code path.

5. **Edge cases concentrate on the per-task path:** no stall watchdog today (executor.py:1303-1381 poll loop is freeform-only); partial-result resume key form is `f"{phase_id}-{task_index:04d}"`; tasklist-drift handling is unaddressed.

6. **User interaction transformation:** the dashboard moves from "two updates per task with frozen middle" to "continuously animated" — Spinner (P-05) + monotonic Duration (P-02) + width-aware truncation (P-03+P-07) + live activity stream (P-01) compose into the fireworks landing.

**Status: Complete.**
