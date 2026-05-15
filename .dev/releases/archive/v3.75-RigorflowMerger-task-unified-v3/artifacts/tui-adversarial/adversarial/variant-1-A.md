# Variant A — Top-5 Shortlist

## Lens Statement (self-declared)

This variant scores proposals against **structural correctness and root-cause coverage**. A keystone fix that resolves the dominant defect outweighs three cosmetic fixes that paper over symptoms. A proposal is downgraded if it does not engage with the per-task code path identified in §2.1 as the source of the worst user-visible breakage. A proposal is upgraded if it composes cleanly with the keystone — that is, if it makes the keystone's improvement *visible* rather than duplicating work or contradicting it.

## Viability Methodology

Viability = coverage × confidence × independence where:
- coverage (0–1.0) = fraction of the three symptoms in §2 the fix addresses *structurally*, not by accident
- confidence (0–1.0) = probability the fix lands without requiring rework — penalised when the proposal admits known unresolved issues (e.g. "_last_read_pos must be reset between tasks") or known threading hazards
- independence (0–1.0) = 1.0 if the fix is useful standalone, scaled down by the number of upstream proposals it depends on

Score is rendered as a 0–100 integer.

---

## Top-5 Ranked

### #1 — P-01: Wire OutputMonitor into the per-task path

- **Viability**: 88
- **Effort**: M (1–3 days)
- **Why it leads (architect lens)**: This is the keystone. §2.1 establishes that the per-task path (`execute_phase_tasks`, executor.py:919–1051) is "the modern code path used by virtually every current sprint" (TUI-ANALYSIS.md §2.1 ¶2). On that path:
  - No `OutputMonitor` is started at all (executor.py:1276–1390 is the only construction site, and it lives on the freeform path).
  - `_tui_state = MonitorState()` (executor.py:981) constructs a *fresh empty* state for every per-task TUI update, so every field the renderer reads (`stall_seconds`, `last_event_time`, `completed_task_estimate`, `activity_log`) is zero by construction.
  - `proc.wait()` (executor.py:1088) is a blocking call between the two TUI updates — so there is no event loop where any other proposal could attach.

  Every other proposal that depends on monitor state being live (P-04 pulse, P-06 sparkline, P-09 queue-driven render, P-10 heartbeat-with-tokens) is structurally inert on this path until P-01 lands. Skipping P-01 means shipping fixes that only ever fire on the obsolete freeform path — high-blast-radius failure mode (work that does nothing for the common case).
- **Risks / flaws (own-side honesty)**:
  1. The proposal explicitly admits "per-task subprocess writes to a shared NDJSON file so the monitor's incremental-read pointer must be reset between tasks (otherwise it skips the first task's output)" — real correctness hazard. Mitigation stated but not verified against monitor.py reset semantics. A bad reset firing *during* the first task would lose lines.
  2. Threading model change for the most-used path; test fixtures in `tests/sprint/test_execute_phase_tasks*.py` need `_subprocess_factory` + fake-monitor injection. Unmeasured rework.
  3. Pivots `proc.wait()` to a `proc._process.poll() is None` loop — accessing the underscore-prefixed `_process` attribute couples the executor to `ClaudeProcess` internals. Cleaner to add a public `is_running()` method in the same patch.
- **Dependencies**: none upstream; unblocks P-02 (per-task `phase_started_at`), P-04 pulse, P-06, P-10.

### #2 — P-02: Replace `stall_seconds` with elapsed-since-phase-start in Duration column

- **Viability**: 78
- **Effort**: S (<1 day)
- **Why it leads (architect lens)**: §2.1 final paragraph identifies a *secondary* correctness bug independent of the per-task plumbing: even on the freeform path, the Duration cell reads `int(self.monitor_state.stall_seconds)` (tui.py:269), which is the *idle gap since last NDJSON event*, not phase-elapsed. The label is "Duration" — the metric shown is something else. That is categorical wrongness, not a UX preference. The fix is a one-line replacement against an already-populated field (`phase_started_at`, models.py:609). Structurally correct in isolation and amplifies P-01 once P-01 lands. Without P-01 it works for the freeform path; with P-01 it is the simplest "moving number" the user sees during a per-task subprocess.
- **Risks / flaws**:
  1. P-02 admits a sequencing wart: `phase_started_at` is set by `monitor.reset(...)` (monitor.py:308), which is not called on the per-task path today. Proposal hand-waves a fallback ("wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of `phase` change") — clean enough but means the field has *two* writers (monitor and TUI) until P-01 lands. Code-smell.
  2. No unit-test regression risk if tests assert substring match on Duration rather than exact `"0s"`. Snapshot tests need re-baselining.
- **Dependencies**: composes with P-01; independent fix still valuable.

### #3 — P-03: Drive the prompt/agent line width from `console.width`

- **Viability**: 82
- **Effort**: S
- **Why it leads (architect lens)**: §2.3 establishes that cut-off is **double truncation** — once at extraction time (config.py:179,193,203,204 all return `[:60]`) and again at render time (`_LLM_LINE_MAX = 60` at tui.py:34, applied at tui.py:386–387). Crucially, "Console never reads its actual width" (§2.3 final paragraph). Structural mistake: a renderer hard-coded against a constant that should be the result of querying the medium it renders to. The fix removes the constant and reads `self.console.width`. Minimum fix for symptom 3; independent of monitor/threading work, so ships in parallel with P-01 without coupling. Architect lens favours it because it removes a hard-coded magic-number coupling between the renderer and the terminal, replacing it with a query against the actual constraint.
- **Risks / flaws**:
  1. Proposal warns: "Rich's outer Panel already wraps long lines if you don't truncate, which can change the active panel's height frame-to-frame and cause flicker." Pre-computing `avail` mitigates, but requires accurate accounting for panel border + padding (proposal estimates "console.width - 14"). If heuristic is off by one or two cells, lines either clip prematurely or wrap — both produce reportable defects.
  2. Proposal pairs render-side fix with bumping extraction-time caps from `[:60]` to `[:240]` — `Phase.prompt_preview` (models.py:296) now stores up to 240 chars. Downstream consumers that assume ≤60 (log formatters, error reporters) need an audit. No such audit included.
- **Dependencies**: independent. P-07 composes naturally and is half-subsumed.

### #4 — P-07: Width-aware caps for assistant text, activity, errors

- **Viability**: 70
- **Effort**: S
- **Why it leads (architect lens)**: §2.3 final paragraph lists *four* hard-coded caps: `_LLM_LINE_MAX = 60` (handled by P-03), activity desc 50 chars (tui.py:424), error messages 80 chars (tui.py:459, 539), and assistant text 80 chars at the monitor layer (`ASSISTANT_TEXT_MAX_LEN = 80`, monitor.py:121). P-03 only removes one. P-07 removes the other three, with one important structural improvement: it moves the assistant-text trim out of the monitor entirely ("stop trimming in the monitor — store the full assistant text") so the layering is clean: monitor stores, renderer trims. That layering correction is the architect-lens reason this earns a slot over P-05 or P-10 in this position. The current arrangement (monitor pre-trims to 80, renderer further trims to 60) is a classic two-stage lossy-compression bug — by the time the renderer has the string it cannot widen it even if the terminal grew.
- **Risks / flaws**:
  1. Storing full assistant text widens the monitor's memory ring-buffer footprint. Proposal estimates "10-entry ring buffer × 400 char cap = 4 KB" — negligible, but the actual cap should be a constant in monitor.py with a comment citing the budget.
  2. Activity-stream and error strings can contain raw ANSI escape codes if a tool echoes them. Proposal acknowledges ("Existing behavior already passes through whatever the SDK emits, so this isn't a regression") but if P-03+P-07 widens the visible range, the failure mode (ANSI literal-rendering on a 200-column terminal) is more visible. A `Text.from_ansi` or strip-ansi pass at render-time would close the loop — not in the proposal as written.
  3. Tight coupling to P-03: without P-03 in place, P-07 still works for activity/error caps but the assistant-text path is unfixed since `_LLM_LINE_MAX=60` would still clip after monitor stores full string.
- **Dependencies**: composes with P-03 (must-land-with); independent of P-01.

### #5 — P-05: Rich spinner on RUNNING status cell and active-panel title

- **Viability**: 65
- **Effort**: S
- **Why it leads (architect lens)**: A spinner is the *cheapest correct answer* to the "is it dead?" question and it has a structural property that matters: Rich's `Spinner` advances under `Live.refresh_per_second=2` *without any external push*. §2.2 ¶3 confirms `Live` auto-refreshes the same render-tree at 2 Hz on a background thread — so a Spinner object embedded in the render tree literally cycles frames with zero coupling to the executor, the monitor, or any of the bugs P-01 fixes. From the architect lens that is a *very* clean fix: it bypasses the broken-push model entirely by using Rich's own pull-based refresh on a self-animating widget. Earns slot #5 over P-10 because P-10 *also* needs the monitor wired to be informative ("On the per-task path before P-01 lands, `last_event_time` is reset to `time.monotonic()` at construction (models.py:609) so the heartbeat would always show `0.0s ago`") — P-10 is partially dead-on-arrival without P-01. P-05's spinner is *unconditionally* alive.
- **Risks / flaws**:
  1. Snapshot-based tests of rendered table need re-baselining. Flagged in proposal; no quantified test count.
  2. `Spinner` inside `Table.add_row` requires passing the Spinner object, not its rendered string — proposal flags this ("confirm cell rendering works with the current `box=None` table") but does not include a smoke test asserting the cell type. Risk low; flagging is honest.
  3. Two spinners refreshing simultaneously could create the illusion of mismatched cadence on terminals with slow scrollback (tmux + slow ssh). Both share the same `refresh_per_second` so this is paranoia — flagging because architect lens punishes "fix X by adding two of Y where one suffices". One spinner (active-panel title) is probably sufficient; the table cell is the bonus.
- **Dependencies**: none — works *immediately* under existing 2 Hz refresh.

---

## Held Back

- **P-04 (Rich `Progress` with `BarColumn(bar_width=None)`)** — Strong structural fix and explicitly cited as the original v3.7b SPEC intent, but partly redundant with the hand-rolled bars once P-01 makes them actually update. The `pulse=True` feature is the unique value-add and that subset can be revisited after P-01+P-02+P-05 ship. M-effort with rebaseline cost not justified ahead of the keystone landing.
- **P-06 (events/sec sparkline)** — Depends on P-01 to be useful ("requires P-01 to be useful on the per-task path; otherwise the sparkline is flat during per-task runs"). On its own merit it is a *display* of data, not a fix to the underlying gap. Defer.
- **P-08 (`Layout` tree)** — Structurally the most correct fix for resize behaviour, but M-effort with TUI snapshot rebaseline and "Layouts behave differently with variable-height children" — substantial blast radius for marginal incremental value once P-03 ships dynamic widths.
- **P-09 (queue-driven render thread)** — L-effort; strongest long-term architecture and cleanest fix to the "push-based render is fragile" critique. Source itself recommends deferring ("defer until P-01..P-05 land and the cadence shortcomings of the push-based model are clearly measured") and that lines up with my lens: don't refactor the threading model until measurements prove the threading model is the bottleneck. Threading hazards listed (stale `MonitorTick` after `PhaseStart`, sentinel shutdown) are real.
- **P-10 (heartbeat line)** — Excellent diagnostic widget but the proposal openly states "On the per-task path before P-01 lands, `last_event_time` is reset to `time.monotonic()` at construction (models.py:609) so the heartbeat would always show `0.0s ago`". Dead-on-arrival failure mode for the most-used path. Once P-01 lands, the heartbeat is informative — but at that point we already have moving bars, a spinner, and a working Duration column. Marginal value of the heartbeat shrinks. Held back; not rejected.

## Contested Calls

### Defending #4 (P-07) against a probable "this is the same as P-03" counter

**Strongest counterargument**: "P-03 already removes hard-coded widths from the prompt/agent line. P-07 is the same fix on three more strings. You are double-counting a single conceptual change to fill a slot."

**Steelmanned**: P-07 looks like a duplicate because both are *about* hard-coded widths. A reasonable reviewer would collapse them into one ticket.

**Defence**: P-07 has a structural property P-03 does not — it relocates the assistant-text trim *out of the monitor* (monitor.py:121). That is a layering correction, not a width-tuning. After P-03 alone, a wide terminal still cannot see the full assistant text because the monitor already discarded it. The architect lens cares about *where* the truncation lives, not just *what value* the truncation uses. They could ship as one ticket but cannot be reduced to one decision.

### Defending #5 (P-05) against a probable "this is cosmetic" counter

**Strongest counterargument**: "A spinner does not fix a single bug. The per-task path is still hung. The Duration column is still wrong. The user is now deceived into thinking work is happening because a dot is rotating."

**Steelmanned**: A spinner that animates while the underlying subprocess is genuinely dead is *worse than nothing* — it creates a false signal of liveness.

**Defence**: The spinner animates the *render tree*, not the subprocess — and §2.2 ¶3 establishes that `Live` re-renders every 500 ms regardless. If the render tree is dead (TUI thread hung), the spinner is *also* frozen, which is itself a useful diagnostic. The spinner does not lie about the subprocess; it lies about *nothing*, because it is anchored to the renderer's own pulse. Second, the spinner ships before P-01 and gives users *something visibly alive* in the interim. Yes, cosmetic in the strict sense — but in the cost-benefit calculus, a 1-line fix that gives users a working "the dashboard is not frozen" signal is high-leverage.

### Defending exclusion of P-09 against a probable "this is the right architecture" counter

**Strongest counterargument**: "P-09 fixes the root cause of every push-related cadence bug in one move. Even if it is L-effort, shipping a queue-driven render thread once means you never have to add `tui.update(...)` calls again. P-01..P-05 are all band-aids on the push model."

**Steelmanned**: A queue-driven render thread is the textbook correct architecture for a live TUI. Every other proposal is working around the absence of one.

**Defence**: Sequencing, not principle. P-09 is correct; it is also expensive and reshapes the test surface. Shipping P-09 *first* means every other proposal needs to be rebuilt against the new event API; shipping P-01..P-05 first means P-09 lands later but user-visible improvements arrive in weeks not months. The source's §4 trailing paragraph captures this exactly: "queue for a later wave". My architect lens agrees — with the explicit caveat that P-09 should be the *next* wave, not "someday".

---

## Sequencing

Ship in this order; rationale ties to dependency graph and user-perceived improvement curve:

1. **P-05** (spinner) — ships in a day, gives the user an immediate "the dashboard is not frozen" signal even before P-01 lands. Buys air cover for the harder work.
2. **P-03** + **P-07** (combined PR) — width fixes ship together because P-07's layering change should not regress P-03's render-time budget. Combined PR avoids the architectural smell of P-03-then-P-07 shipping monitor-level changes in a second round.
3. **P-02** (Duration semantics) — one-line fix, lands once P-03+P-07 are in to avoid simultaneous TUI snapshot rebaselining churn.
4. **P-01** (OutputMonitor on per-task path) — the keystone. Lands once the cosmetic fixes are in place so that when the monitor goes live, *every other widget* (Duration, prompt width, spinner, activity stream) is already correct and the keystone visibly unblocks all of them at once. The "fireworks" landing.

Bench note: P-04 / P-06 / P-09 / P-10 / P-08 belong to a *follow-up wave* whose scope should be set based on telemetry from this wave. P-09 is the strongest follow-up candidate.
