<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B -->
<!-- Merged from: Variant A (structural-correctness lens), Variant B (user-perceived-freshness lens, base), Variant C (effort-to-impact lens) -->
<!-- Convergence achieved: 0.89 (threshold 0.85, depth=deep, blind=true) -->
<!-- Merge date: 2026-05-14 -->

# TUI Top-5 Shortlist — Adversarial-Merged Outcome

<!-- Source: Synthesis across all variants -->

## Lens Triangulation

Three independent advocates evaluated the 10 proposals in TUI-ANALYSIS.md §3 under different lenses and converged on the same 5-proposal slate. The three lenses were:

- **Structural correctness** (Variant A): keystone-fixes-first; downgrade proposals that don't engage with the dominant root cause.
- **User-perceived freshness** (Variant B — base): reject internally-correct-but-invisible fixes; rank by what the user sees in 30 seconds.
- **Effort-to-impact ratio** (Variant C): prefer S/M fixes with broad impact; flag any L-effort proposal unless its impact is uniquely large.

Despite different optimisation criteria, all three lenses produced the same final 5-proposal slate after three rounds of structured debate. **The convergence itself is evidence the slate is correct.** Where the lenses disagreed (rank #1, slot #5 candidate) the debate resolved each disagreement with documented evidence.

## Per-Day ROI Triangulation (incorporates Variant C's quantitative methodology)

<!-- Source: Variant C, U-002 — per-day ROI quantification -->

C's per-day ROI math was independently validated in Round 2: P-05 delivers ~30% of §2.2 resolved per engineering-day (1-day ship, ~30% impact); P-01 delivers ~80% of §2.1+§2.2 resolved per engineering-day-equivalent (2.5-day ship, ~80% impact = 32%/day). The two are *within noise* of each other on per-day return. This finding supported the Round 3 sequencing decision (P-05 ships day 1, P-01 lands days 3-5) and ratifies that P-01 at rank #1 is a methodological-tiebreak win, not a structural certainty.

---

## Top-5 Ranked

### #1 — P-01: Wire OutputMonitor into the per-task path

<!-- Source: Base (Variant B) + R3 converged ranking -->

- **Viability**: 92 (B's score, validated by A=88 and C=85 after R3 mitigation absorbs INV hazards)
- **Effort**: M (1–3 days, +0.3 day for INV-001/005 mitigation contract → still M-tier)
- **Symptoms addressed**: §2.1 (hang), §2.2 (no real-time)
- **Code surface**: `src/superclaude/cli/sprint/executor.py:919-1088`

**Why it leads**: §2.1 ¶3 establishes the per-task path is "the modern code path used by virtually every current sprint." On that path, no `OutputMonitor` is started at all; `_tui_state = MonitorState()` (executor.py:981) constructs a fresh empty state on every per-task TUI update, so every field the renderer reads is zero by construction; `proc.wait()` (executor.py:1088) blocks between the two TUI updates with no event loop where any other proposal could attach. P-01 is load-bearing for P-04 pulse, P-06 sparkline, P-09 architectural follow-on, and P-10 heartbeat-with-tokens — without P-01 those proposals are structurally inert on the per-task path.

**Risks / flaws**:
1. **OutputMonitor reset hazard (HIGH, mitigated)**: The proposal admits "per-task subprocess writes to a shared NDJSON file so the monitor's incremental-read pointer must be reset between tasks (otherwise it skips the first task's output)." Mitigation contract (mandatory unit test) added below.
2. **Threading model change** for the most-used path; test fixtures in `tests/sprint/test_execute_phase_tasks*.py` need `_subprocess_factory` + fake-monitor injection.
3. **Underscore-coupling**: Pivots `proc.wait()` to a `proc._process.poll() is None` loop — accessing the underscore-prefixed `_process` attribute couples the executor to `ClaudeProcess` internals. Recommended: add a public `is_running()` method to `ClaudeProcess` in the same patch (Variant A's structural recommendation).

**INV-001/005 Mitigation Contract (mandatory for P-01 PR)**:
1. Add `tests/sprint/test_monitor_reset_between_tasks.py` that:
   - Writes 3 events for task 1, calls `monitor.reset(...)`, writes 3 events for task 2
   - Asserts `monitor.state.events_received == 6` after both tasks
   - Asserts `_last_read_pos` is at the correct file offset after each reset
2. Make `monitor.reset(...)` idempotent against partial-read state — if called mid-task, finish the in-flight read before resetting.
3. Promote the reset call to a public method `OutputMonitor.reset_for_next_task()` documenting intent.

**Dependencies**: none upstream; unblocks P-04 pulse, P-06, P-10 heartbeat numerics, P-02 per-task `phase_started_at`.

### #2 — P-05: Rich spinner on RUNNING status cell and active-panel title

<!-- Source: Base (Variant B); A and C both rank in top-5 with high viability -->

- **Viability**: 88 (B's score, A=65, C=95; B's saliency-weighted score is the calibrated centre)
- **Effort**: S (<1 day)
- **Symptoms addressed**: §2.2 (no real-time)
- **Code surface**: `src/superclaude/cli/sprint/tui.py:58-72` (STATUS_ICONS), `tui.py:408-412` (active panel title)

**Why it leads**: The only proposal whose visible-motion guarantee is *independent of the broken per-task plumbing*. §2.2 ¶3 establishes `Live` re-renders every 500 ms regardless of executor pushes — and §2.2 ¶1 confirms the *absence* of any animated spinner today. Importing `rich.spinner.Spinner` and embedding it in the render tree gives the user *immediate, unconditional* "the dashboard is alive" feedback under the existing 2 Hz refresh, with zero coupling to the executor, monitor, or any of the bugs P-01 fixes.

**Risks / flaws**:
1. **False-positive risk**: a spinner that animates while the subprocess is genuinely hung still creates the *appearance* of progress. A user trained on "spinner = work happening" might wait longer before reporting a real hang. (Mitigated by P-10 follow-on which adds diagnostic colour-coded heartbeat.)
2. **Snapshot rebaseline cost**: Snapshot-based tests of the rendered table need re-baselining. Test count not quantified.
3. **Two spinners synchronicity**: refreshing simultaneously could look mismatched on terminals with slow scrollback. Recommendation: ship one (active-panel title) first, evaluate before adding the table cell.

**Dependencies**: none. Ships at PR-merge time. Highest "visibility per engineering day" of any proposal.

### #3 — P-02: Replace `stall_seconds` with elapsed-since-phase-start in Duration column

<!-- Source: Base (Variant B); A=78 viability, C=90 viability -->

- **Viability**: 82
- **Effort**: S (<1 day)
- **Symptoms addressed**: §2.1 (hang appearance), §2.2 (clearer real-time signal)
- **Code surface**: `tui.py:265-273` (Duration cell), `models.py:609` (`phase_started_at` already exists)

**Why it leads**: §2.1 final ¶ shows the current Duration column is *categorically wrong* — it reads `int(self.monitor_state.stall_seconds)` (tui.py:269), which is the *idle gap since last NDJSON event*, not phase-elapsed. The label is "Duration" — the metric shown is something else. One-line fix against an already-populated field. Freeform path benefits *immediately*; per-task path benefits once P-01 lands.

**Risks / flaws**:
1. **Dual-writer code-smell**: `phase_started_at` is set by `monitor.reset(...)` (monitor.py:308), which is not called on the per-task path today. The fallback ("wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of `phase` change") introduces a second writer until P-01 lands. Flagged as INV-002 (MEDIUM, follow-on cleanup).
2. **Sub-second flicker**: If a phase completes in 0.9 s the user sees `0s` then `1s`. Confirm `int(time.monotonic() - start)` doesn't oscillate.
3. **Semantics change**: On the freeform path today the Duration *decreases* when new output arrives. Users may have learned to read this as a "thinking gap indicator." Worth a deprecation comment in the changelog.

**Dependencies**: composes with P-01 for the per-task case; standalone-useful on the freeform path.

### #4 — P-03: Drive prompt/agent line width from `console.width`

<!-- Source: Base (Variant B) + Variant C P-03+P-07 bundling rationale -->

- **Viability**: 78
- **Effort**: S
- **Symptoms addressed**: §2.3 (cut-off)
- **Code surface**: `tui.py:30-36, 80, 386-387`, `config.py:179,193,203,204`

**Why it leads**: §2.3 establishes the cut-off is **double truncation** — once at extraction time (config.py:179,193,203,204 all return `[:60]`) and again at render time (`_LLM_LINE_MAX = 60` at tui.py:34). Crucially, "Console never reads its actual width" (§2.3 final ¶). The renderer is hard-coded against a constant that should be the result of querying the medium it renders to. This is the minimum fix for symptom 3, independent of monitor/threading work.

**Risks / flaws**:
1. **Panel-height flicker** if text wraps. Pre-computing `avail = console.width - 14` mitigates *only if the math is right*. Off-by-one against panel border + padding gives the user a "wider than before but still clipped" experience.
2. **Downstream-consumer audit (INV-004 mitigation, mandatory)**: The proposal bumps extraction-time caps from `[:60]` to `[:240]`. Before P-03 PR merge, a 15-minute grep audit of `Phase.prompt_preview` consumers is required to confirm no log formatter / error reporter assumes ≤60.
3. **Half-fix without P-07**: P-03 alone leaves the Agent: line clipped at 80 (because monitor.py:121 pre-trims). Must ship as P-03+P-07 combined PR for full §2.3 resolution.

**Dependencies**: P-07 is a hard "ship-together" recommendation; not a hard dependency but partial without it.

### #5 — P-07: Width-aware caps for assistant text, activity, errors

<!-- Source: Variant A slot #4 + Variant C slot #5; agreed in R2 by all three variants -->

- **Viability**: 70 (A's score)
- **Effort**: S
- **Symptoms addressed**: §2.3 (cut-off — completes P-03)
- **Code surface**: `monitor.py:121` (ASSISTANT_TEXT_MAX_LEN), `tui.py:424, 459, 539`

**Why it leads**: §2.3 final ¶ lists *four* hard-coded caps; P-03 only removes one. P-07 removes the other three, with one important structural improvement contributed by Variant A's architect lens: **it relocates the assistant-text trim out of the monitor entirely**. The current arrangement (monitor pre-trims to 80, renderer further trims to 60) is a classic two-stage lossy-compression bug — by the time the renderer has the string it cannot widen it even if the terminal grew. P-07 makes the layering clean: monitor stores, renderer trims. This layering correction is the architect-specific value-add and is the reason P-07 earns slot #5 over P-10.

**Risks / flaws**:
1. **Monitor memory footprint**: Storing full assistant text widens the ring-buffer footprint. Estimated 10-entry × 400-char cap = 4 KB; negligible. Recommend: explicit constant in monitor.py with a comment citing the budget.
2. **ANSI escape sequences**: Activity-stream and error strings can contain raw ANSI if a tool echoes them. Proposal acknowledges; recommend a `Text.from_ansi` or strip-ansi render-time pass — not in proposal as written.
3. **Coupling to P-03**: Without P-03 in place, P-07 still works for activity/error caps but the assistant-text path is unfixed since `_LLM_LINE_MAX=60` would still clip after monitor stores the full string. **Combined P-03+P-07 PR is the recommended ship vehicle.**

**Dependencies**: composes with P-03 (must-land-with for full §2.3 visible benefit); independent of P-01.

---

## Held Back (with explicit rationale)

<!-- Source: Synthesis of all three variants' held-back sections -->

- **P-04 (Rich `Progress` with `BarColumn(bar_width=None)`)** — Strong structural fix; explicitly cited as the original v3.7b SPEC intent. Partly redundant with the hand-rolled bars once P-01 makes them actually update. The `pulse=True` feature is the unique value-add. M-effort with rebaseline cost not justified ahead of the keystone landing. **Slot #6 candidate for the next wave.**

- **P-06 (events/sec sparkline)** — M-effort. Visible only when events ARE flowing; on a working post-P-01 system this is a nice histogram of subprocess intensity, but the proposal admits it "requires P-01 to be useful on the per-task path; otherwise the sparkline is flat during per-task runs." Symptom coverage is 0 of 3 (it's an additional widget, not a fix). **Defer until P-01 has shipped and we have telemetry on actual event throughput.**

- **P-08 (Layout tree)** — M-effort. Structurally the most correct fix for resize behaviour, but the visible benefit is already 80% achieved by P-03+P-07+P-04 collectively. Substantial blast radius (TUI snapshot rebaseline + variable-height children handling) for marginal incremental value. **Defer to architectural-refactor wave alongside P-09.**

- **P-09 (queue-driven render thread)** — L-effort. Strongest long-term architecture and the cleanest fix to the "push-based render is fragile" critique. From the user's lens, the visible benefit (latency reduction from 500 ms to 250 ms) is *imperceptible*. From the architect's lens, this is the right next-wave anchor. **Treated separately in the Flagged-Large-Effort section below.**

- **P-10 (heartbeat line)** — S-effort *on paper*, S+M-effort *effectively* (because the proposal openly states "On the per-task path before P-01 lands, `last_event_time` is reset to `time.monotonic()` at construction (models.py:609) so the heartbeat would always show `0.0s ago`"). Dead-on-arrival without P-01. **Ship as #6 immediately after P-01, with mandatory sentinel mitigation** (`events_received > 0` gating or `last_event_time` sentinel pattern). The original proposal treats the sentinel as a footnote; in this merged outcome it becomes a load-bearing acceptance criterion for the P-10 PR.

## Flagged Large-Effort Proposals

<!-- Source: Variant C — Flagged-L section + Variant A's exclusion rationale -->

There is exactly one L-effort proposal in the file: **P-09 (event-driven render thread)**. By the lens definition ("flag any Large-effort fix unless its impact is uniquely large"), P-09 fails the bar:

- **Visible impact**: ≈zero. The user cannot perceive a 250 ms latency reduction.
- **Internal impact**: large, but not addressing any §2 symptom directly. Architectural improvement that *enables* future fixes rather than delivering current ones.
- **Test surface impact**: large. Existing tests that simulate `tui.update` directly need to adapt to the event API.
- **Risk**: three named risks in proposal — new thread + queue, clean shutdown (sentinel event, `_render_thread.join(timeout=2)`), potential ordering bugs if `PhaseStart` is processed after a stale `MonitorTick`.

**Verdict**: Excluded from the top-5. **Strong candidate for the next-wave anchor** after the top-5 lands and the cadence shortcomings of the push model are measured (mirroring the source's §4 recommendation). It is the right *follow-on* L-fix once P-01..P-05 have shown what's still broken — *not* a "someday" item.

---

## Sequencing

<!-- Source: Variant C day-numbered scheme + Variant A "fireworks landing" rationale + Variant B saliency weighting -->

Day-numbered sequencing (more actionable than week-numbered for engineering scheduling):

1. **Day 1 — P-05** (spinner): Ships visible motion immediately. Zero downstream coupling, zero new threads. Buys reviewer goodwill and gives users an immediate "the dashboard is not frozen" signal even before P-01 lands. **First-merged proposal.**
2. **Days 1–2 — P-02 + (P-03 + P-07 combined PR)**: Three S-fixes shipped as two PRs (P-02 standalone; P-03+P-07 together because shipping P-03 alone produces a half-fix per the architect's layering critique). Total ~1.5 days. Snapshot rebaselines done once.
3. **Days 3–5 — P-01** (OutputMonitor on per-task path): The keystone. Lands with the cosmetic fixes already in place, so the day P-01 ships the user sees *everything come alive simultaneously* — the spinner is alive (was already), the bars are alive (newly), Duration ticks correctly (newly), prompt and agent lines are full-width (already), the activity stream populates (newly). **This is the "fireworks landing"** — Variant A's term, ratified by C's independent day-numbered timing and B's saliency analysis. Includes the mandatory INV-001/005 mitigation contract (`OutputMonitor.reset_for_next_task()` method + unit test).

**Total wave cost**: ~5 engineering-days for the full top-5.

**Next wave candidates** (in priority order):
1. **P-10** with mandatory sentinel mitigation (~Day 6, ships immediately after P-01)
2. **P-04** Rich Progress + BarColumn(bar_width=None) + pulse (now functional because P-01 sets stall_status)
3. **P-09** queue-driven render thread (the L-effort architectural follow-on)
4. **P-08** Layout tree (if P-04 doesn't sufficiently resolve resize behaviour)
5. **P-06** sparkline (lowest priority — pure widget, not a fix)

---

## Manual Smoke-Test Acceptance Criteria

<!-- Source: Variant B / U-001 — universally agreed unique contribution -->

For each top-5 fix, what would QA ACCEPT or REJECT as proof during manual smoke?

**P-01 (OutputMonitor on per-task path)**:
- ACCEPT: Run a 3-task per-task phase. The Tasks bar advances visibly (not in one jump) at task boundaries. Activity log shows ≥1 event during each task. `growth_rate_bps` is nonzero. TUI does *not* require a keypress to refresh. **Unit-test invariant**: NDJSON event count from the file matches TUI-displayed count within 1, across phase boundaries.
- REJECT: Bars still jump in one step at phase end. Activity log shows `— — —` for the full task. `growth_rate_bps` stays at zero. Event-count invariant fails.

**P-02 (Duration column)**:
- ACCEPT: Open a sprint; Duration column for the running phase displays an integer that *increases monotonically every second* and never decreases. After phase ends, the column shows final elapsed time (matching wall-clock observation ±1 s).
- REJECT: Duration shows `0s` while phase is running. Duration decreases when new events arrive (indicates the bug was not fixed and `stall_seconds` is still being read).

**P-03 + P-07 (dynamic prompt/agent/activity/error widths)**:
- ACCEPT: On a 200-column terminal, the Prompt: line displays text wider than 60 chars AND the Agent: line also displays wider than 80 chars. Resizing terminal mid-sprint reflows the next render. Active panel does not flicker height-wise. Activity and error lines also use available width.
- REJECT: Prompt: line widens but Agent: line stays at 80 (indicates P-07 was not properly applied). Active panel height flickers on every refresh. Long prompts wrap to a second line (truncation math is off).

**P-05 (spinner)**:
- ACCEPT: Within 2 s of sprint start, the RUNNING row's status cell shows a visible cycling glyph. Active-panel title also shows a cycling glyph. Both cycle at ~10 Hz (Rich default for `dots`). When the executor is intentionally paused (e.g. during PreFlight), the spinner continues to cycle (proves it's anchored to `Live.refresh_per_second`, not to executor pushes).
- REJECT: Status cell shows static `RUNNING` text. Spinner cycles only when events arrive (means it's coupled to push events rather than `Live`). Spinner glyphs render as `?` or boxed characters (terminal-font issue — not a P-05 defect but blocks acceptance).

---

## Viability Methodology (triangulated)

<!-- Source: Synthesis of all three variants' methodology sections -->

The merged viability scores in this shortlist are calibrated against three independent methodologies that produced consistent rankings after the position-bias dual-pass evaluation:

- **User-perceived freshness** (primary): does the user see visible change in 30 seconds of observation?
- **Structural correctness**: does the fix engage the dominant root cause without papering over symptoms?
- **Effort-to-impact ratio**: does each engineering-day deliver broad visible improvement, or does it concentrate on a single deep win?

Where the three methodologies disagreed (rank #1 between P-01 and P-05) the per-day ROI math confirmed the two were within noise of each other; the tiebreak goes to P-01 on impact-magnitude grounds while the *sequencing* honours C's "ship certain wins first" intuition (P-05 ships Day 1, P-01 lands Days 3-5).

---

## Convergence Statement

This shortlist is the converged outcome of a three-round adversarial debate at depth=deep, convergence threshold 0.85, with blind evaluation enabled. Final convergence score: **0.89**. All three variants agreed on the 5-proposal slate, agreed on the sequencing, and agreed on the held-back rationale. The two HIGH UNADDRESSED invariant-probe findings (INV-001 and INV-005, both concerning `OutputMonitor` reset semantics) were unanimously absorbed into the P-01 PR acceptance criteria via a mandatory unit-test contract.

Two MEDIUM UNADDRESSED invariant findings remain (INV-002: `phase_started_at` dual-writers; INV-004: `prompt_preview` downstream-consumer audit). INV-002 is accepted as a follow-on cleanup after P-01 lands; INV-004 is mandatory pre-merge for the P-03 PR as a 15-minute grep audit.

The adversarial process re-ranked the analyst's initial suggestion (§4 of TUI-ANALYSIS.md, which was P-01, P-02, P-03, P-05, P-10) by **swapping P-10 → P-07** in slot #5 — a change every variant ultimately agreed with after debate. The keystone fix (P-01) is preserved in the top-5 with strengthened acceptance criteria.
