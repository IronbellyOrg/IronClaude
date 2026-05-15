# Variant B — Top-5 Shortlist

## Lens Statement (self-declared)

This variant evaluates proposals by **user-perceived freshness**. A fix that is internally correct but does not visibly change what the user sees on screen is, from this lens, indistinguishable from no fix at all. The three reported symptoms are user-facing: progress bars hang, no real-time indicators, prompts cut off. Each proposal must answer one question to earn a slot: **"if a user watches the screen for 30 seconds after this lands, what visibly changes?"** Proposals whose visible change requires another proposal to land first are downgraded — not excluded, but their viability score is multiplied by `P(dependency_lands)`.

This lens is openly suspicious of "structurally correct" fixes that the user cannot see. A perfect refactor that produces an identical-looking screen is wasted engineering.

## Viability Methodology

Viability = `visible_movement × cadence × symptom_coverage` where:
- `visible_movement` (0–1.0) = does the user actually see motion / wider text / corrected number? scored against the screen, not the code
- `cadence` (0–1.0) = how often the visible change updates (per-second = 1.0, per-task = 0.5, per-phase = 0.2)
- `symptom_coverage` (0–1.0) = fraction of the three §2 symptoms the user perceives as fixed after this lands

Score is rendered as a 0–100 integer.

---

## Top-5 Ranked

### #1 — P-01: Wire OutputMonitor into the per-task path

- **Viability**: 92
- **Effort**: M
- **Why it leads (QA lens)**: I openly resisted putting this at #1 because the QA lens is suspicious of plumbing fixes — but the source forces my hand. §2.1 ¶3 states: "from the user's seat, both bars sit at the post-last-phase value for the entire duration of every task subprocess (often minutes)." That is not an internal correctness problem — that is the *primary* visible symptom of the entire complaint. A user watching the screen for 30 seconds sees frozen bars for 100% of those seconds on the per-task path. P-01 is the only proposal that turns that 100% into a meaningful percentage of motion. Every other proposal in this list (spinner, heartbeat, Duration column, sparkline) is *additional* motion on top of motion-restored-by-P-01. Without P-01, P-10's heartbeat would read `0.0s ago` forever (§2.2 says `last_event_time` is reset at construction, models.py:609); without P-01, P-06's sparkline would be flat (the proposal itself admits this); without P-01, P-02's Duration would tick correctly but be the *only* moving thing on screen. The visible-motion delta from P-01 is the largest among all 10 proposals.
- **Risks / flaws (visibility-specific)**:
  1. **Invisibility failure mode**: if the `_last_read_pos` reset is wrong, the monitor starts mid-stream — activity log shows partial data, growth-rate-bps is incorrect — *but the bars still move*. This is the failure mode I worry about most, because it would be "fixed enough" to look like success and ship with subtle wrong numbers. QA acceptance test: count NDJSON events written by the subprocess vs events counted by the TUI; they must match within 1.
  2. The user-visible motion appears only when NDJSON output exists. Subprocess startup (first ~2 s before the SDK emits anything) still shows frozen state. The user's first impression of "is it working?" is unchanged unless paired with P-05 or P-10.
  3. The proposal is silent on what happens to the `Tasks` bar's `completed_task_estimate` during a single long task that never completes — does it sit at 0 until the task finishes, or does the regex (monitor.py:540–549) catch intra-task `T<PP>.<TT>` heading echoes? If the latter, the bar may jump *backward* on retry, which is worse than not moving.
- **Dependencies**: none upstream. **Hard dependency for P-06, P-10. Soft dependency for P-04's `pulse` feature, P-02's per-task Duration.**

### #2 — P-05: Rich spinner on RUNNING status cell and active-panel title

- **Viability**: 88
- **Effort**: S
- **Why it leads (QA lens)**: This is the only proposal whose visible-motion guarantee is *independent of the broken per-task plumbing*. §2.2 ¶3 establishes that `Live` re-renders every 500 ms regardless of executor pushes — and §2.2 ¶1 confirms the *absence* of any animated spinner today ("Rich's `rich.spinner.Spinner` is not imported or used"). Importing it and embedding it in the render tree gives the user *immediate, unconditional* "the dashboard is alive" feedback. This is the single fix that gives the user *visible motion within the same week the PR merges*, without requiring P-01 to be in place. From the QA lens that's worth more than three "structurally correct" fixes that wait on P-01.
- **Risks / flaws (visibility-specific)**:
  1. **False-positive risk**: a spinner that animates while the subprocess is genuinely hung still creates the *appearance* of progress. A user trained on "spinner = work happening" might wait longer before reporting a real hang. Acceptance test must explicitly distinguish "spinner spinning because Rich Live is refreshing" from "spinner spinning because the subprocess is producing output". The first is true here, the second is what users assume.
  2. The spinner cycles even after the subprocess is dead — until `tui.stop()` is called. This is correct behaviour but could be confusing if the subprocess exits silently and the executor hasn't yet noticed.
  3. Two spinners (table cell + active-panel title) refreshing at the same rate could look synchronised or look mismatched depending on terminal vsync. A single spinner is safer; two is showmanship. QA preference: ship one (active-panel title), evaluate before adding the second.
- **Dependencies**: none — works at PR-merge time. Highest "visibility per engineering day" of any proposal.

### #3 — P-02: Replace `stall_seconds` with elapsed-since-phase-start in Duration column

- **Viability**: 82
- **Effort**: S
- **Why it leads (QA lens)**: The Duration column today shows `0s` for the duration of every per-task subprocess (§2.1 final ¶: "the phase Duration column likewise reads `int(monitor_state.stall_seconds)` (tui.py:269) which is permanently 0 in per-task mode, so it shows `0s` while the phase is actually running — a strong 'hung' signal"). A user looking at a column literally labelled "Duration" that shows `0s` while their work runs for minutes is being lied to. That is the worst kind of UX defect — not absent information but *wrong* information presented as correct. P-02 swaps the wrong value for the right value, and the proposal's own claim ("Duration ticks up monotonically every second for the active phase; users see *something* numerically moving even before any other plumbing changes land") is precisely what my QA lens optimises for. The acceptance test is trivial: open a sprint, watch the Duration column, confirm it counts up monotonically, every second, never decreases.
- **Risks / flaws (visibility-specific)**:
  1. The proposal admits that on the per-task path `phase_started_at` is not actually set by `monitor.reset(...)` today because the monitor never starts. The fallback ("wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of `phase` change") relies on the TUI observing a phase transition. If the executor does not push a `tui.update()` at phase boundary on the per-task path, the captured timestamp is wrong. The proposal does not verify this — it should.
  2. The Duration display uses `int(...)` rounding. If a phase completes in 0.9 s the user sees `0s` then `1s` then phase ends. That's fine, but flicker between `0s` and `1s` at sub-second cadence on a 4 Hz refresh would be ugly. Confirm `int(time.monotonic() - start)` doesn't oscillate.
  3. On the freeform path today the Duration *decreases* (§2.1 final ¶: "*decreases* whenever new output arrives") — users may have *learned to read* the current behaviour as "thinking gap indicator". Changing the metric semantics changes the readability of an existing display they may have adapted to. Worth a deprecation comment in the changelog.
- **Dependencies**: composes with P-01 for the per-task case. Standalone-useful on the freeform path.

### #4 — P-03: Drive prompt/agent line width from `console.width`

- **Viability**: 78
- **Effort**: S
- **Why it leads (QA lens)**: Symptom 3 ("prompt cut-off in wider terminals") is the *only* symptom of the three that does not require any plumbing or threading fix — it is pure rendering. §2.3 paragraph 3 reads: "Console never reads its actual width." That is the entire problem. A user on a 200-column terminal sees prompts clipped to 57 chars (the `_truncate` adds `...`, so `60-3=57`) while their terminal has ~143 columns of dead space available. This proposal turns those 143 dead columns into legible prompt text. The visible change is *immediate* — the user widens their terminal, the next render uses the new width. QA acceptance test: resize the terminal while a sprint runs and confirm the next render reflows.
- **Risks / flaws (visibility-specific)**:
  1. The proposal admits flicker risk if the panel height changes when text wraps. Pre-computing `avail` mitigates this *only if the math is right*. Off-by-one against panel border + padding gives the user a "wider than before but still clipped" experience — they will report this as "still broken".
  2. The proposal bumps extraction-time caps from `[:60]` to `[:240]` but does not address whether the goal-line itself (which may contain markdown bullets, line breaks, code fences in the source heading text) renders cleanly when fully expanded. A 240-char prompt extracted from a multi-paragraph goal section might include broken markdown that displays as literal `**Goal:**` or other artefacts. Needs render-side strip-markdown pass.
  3. The Agent: line is also widened — but the assistant text is *already* trimmed to 80 chars by `ASSISTANT_TEXT_MAX_LEN` (monitor.py:121) before the renderer sees it. So P-03 alone makes the Prompt: line wider but leaves the Agent: line at 80 chars max regardless of terminal width. Without P-07, the user sees *partial* responsiveness to terminal width — Prompt line moves, Agent line doesn't. Acceptance test must explicitly test both lines or it will declare success prematurely.
- **Dependencies**: P-07 is a hard must-land-with for full visible benefit. Without P-07, the Agent: line is still clipped at 80 — half-fix.

### #5 — P-10: Heartbeat line in active panel

- **Viability**: 70 (downgraded from 85 by P(dependency) = 0.82)
- **Effort**: S
- **Why it leads (QA lens)**: The heartbeat directly answers the user's most-asked diagnostic question — *"is it dead?"* — and answers it with a number plus a colored dot that anyone can interpret. The proposal's own statement nails the QA value: "every Live refresh tick (2 Hz today, 4 Hz with P-09) the heartbeat counter ticks; even if all other widgets are frozen the user sees something move, *and* immediately knows whether the freeze is genuine subprocess silence or a stuck dashboard." That is the QA-lens dream feature: a single line that *both* shows liveness *and* diagnoses the failure mode. It earns slot #5 over P-04/P-07/P-06 because (a) its visible value is highest of any "always-on widget", and (b) its dependency (`last_event_time` must be meaningful, which means the monitor must be running on the active path) is satisfied by P-01.
- **Risks / flaws (visibility-specific)**:
  1. **Dead-on-arrival without P-01** — proposal explicitly states "On the per-task path before P-01 lands, `last_event_time` is reset to `time.monotonic()` at construction (models.py:609) so the heartbeat would always show `0.0s ago`". This is a *visible* failure: the heartbeat would tick forever as `0.0s ago`, which would confuse users worse than showing nothing. QA acceptance: heartbeat must NOT ship before P-01, OR ship with the proposal's sentinel fix ("lazily setting `last_event_time = 0` (sentinel 'never') or by gating the heartbeat on `events_received > 0`"). The latter is preferred and the proposal needs that change explicitly enforced.
  2. The dot-color cycling (green → yellow >5 s → red >30 s) requires the user to understand the colour code. A legend in the active-panel title is unobtrusive; without it the colour is ambiguous on first encounter.
  3. The "tokens 4.5K/s" suffix is *derived* from `growth_rate_bps` (models.py:611) via EMA. On the per-task path with the monitor wired (post-P-01), the first ~5 s of any task show a misleadingly low rate while the EMA seeds. Not a defect, but acceptance test should confirm "ramps up to true rate within 10 s".
- **Dependencies**: hard on P-01 for meaningful values; gracefully degrades to "sentinel" mode otherwise.

---

## Held Back

- **P-04 (Rich `Progress` with `BarColumn(bar_width=None)`)** — Visible benefit (bars stretch to terminal width, plus `pulse=True` during thinking gaps) is real and material from the QA lens, but the `pulse` only fires when `stall_status in {"thinking...", "STALLED"}` which on the per-task path is meaningless until P-01 lands. Without P-01, this is "bars are wider but still hung" — a half-visible improvement. With P-01 + P-04, the visible effect IS large — but P-04 + P-01 is M+M total effort, whereas P-01 + P-05 (cheaper second) achieves comparable visible motion. Held back; would be a strong slot #6.
- **P-06 (events/sec sparkline)** — Visible only when there ARE events to plot. On a working post-P-01 system, this is a nice histogram of subprocess intensity. But the proposal admits it: "requires P-01 to be useful on the per-task path; otherwise the sparkline is flat during per-task runs." A flat sparkline ships *more* visual "is it dead?" anxiety than no sparkline. The QA lens excludes any widget whose absence-of-motion is itself a misleading signal.
- **P-07 (width-aware caps in monitor)** — Strong composition with P-03 but listed separately in held-back because *individually* it changes only the Agent: line width (not the prompt — that's P-03's job) and the activity/error caps. Its visible-on-screen effect alone is smaller than P-03's. The right call is to ship it *with* P-03 as a single PR; in this isolated ranking it scores below P-10's diagnostic value.
- **P-08 (Layout tree)** — The visible benefit on resize is real but only differs from P-03+P-07 by handling the *progress section's* width adaptively too. Once P-04 ships `BarColumn(bar_width=None)`, the progress section auto-stretches anyway. P-08 is a deeper architectural fix whose visible value is captured by P-03+P-04+P-07 collectively. Excluded as marginal.
- **P-09 (queue-driven render thread)** — From the QA lens, the user-visible benefit ("latency between an NDJSON event landing and the screen updating drops from up to 500 ms to ≤250 ms") is *imperceptible* to a human watching a sprint. A 250 ms latency cut is not visible. The proposal's other claims (steady 4 Hz refresh, decoupled cadence) are *internal* properties. From this lens P-09 is "internally correct but invisible" — exactly the failure mode I disqualify by design. L-effort makes the exclusion easy.

## Contested Calls

### Defending #2 (P-05 above P-02) — likely contested by the structural-correctness camp

**Strongest counterargument**: "P-02 fixes a *wrong number on screen* (Duration showing `0s`). P-05 adds a spinner. A wrong number is worse than a missing motion. P-02 must rank above P-05."

**Steelmanned**: Categorically wrong information masquerading as correct is a higher-severity defect than absent information. The Duration column is *labelled* — that's a contract with the user. The spinner is decorative.

**Defence**: I almost ranked P-02 above P-05 for exactly this reason and the call is genuinely close (Viability 88 vs 82). The reason P-05 wins by 6 points: the *frequency* with which a user encounters each visible bug. The Duration column is one cell in one row; the user might not even notice it shows `0s` if they're watching the bars and active panel. The spinner is a high-saliency artefact at the centre of attention. P-05's visible footprint is larger even if P-02's bug is more severe in isolation. From a "what does the user notice in 30 seconds" perspective, the spinner wins. Reasonable engineers can disagree here; I would accept P-02 at #2 and P-05 at #3 in mediation.

### Defending exclusion of P-09 against the "long-term architecture" camp

**Strongest counterargument**: "P-09 is the only proposal that fixes the fundamental cadence problem. Every other proposal is a workaround. From a multi-year perspective P-09 is the right answer."

**Steelmanned**: All other proposals are tactical patches against a broken push model. P-09 fixes the model itself. Long-term, every other proposal becomes unnecessary.

**Defence**: From the QA lens "long-term correct but currently invisible" is the worst combination on this list. A user looking at the screen *today* cannot perceive the difference between a 500 ms update latency and a 250 ms update latency. P-09's user-visible benefit at delivery time is approximately zero — even though its architectural benefit is approximately maximum. I am not arguing P-09 is wrong; I am arguing it is *the wrong ranking for this lens*. The architect lens might rank it #1 of the held-back; the QA lens ranks it dead last because the user never sees it.

### Defending #5 (P-10) ahead of P-04 — likely contested

**Strongest counterargument**: "P-04 makes the bars actually fill correctly *and* pulse during thinking gaps. That's a direct visible fix to a primary symptom. P-10 is a single line of text. P-04 should rank ahead of P-10."

**Steelmanned**: P-04 produces a wider visible change (two bars stretching, pulse during gaps) than P-10's one heartbeat line.

**Defence**: P-04's pulse only fires when `stall_status` is set, which requires the monitor to be running on the active path. On the per-task path, `stall_status` is empty until P-01 lands. So P-04's visible benefit is *conditional* on P-01 in the same way P-10's is. Given equivalent dependencies, P-10 wins because it answers a *diagnostic* question ("is it dead?") that P-04's pulse merely soothes. A pulse cannot tell the user whether the subprocess is dead or thinking; a heartbeat with a timer can. Diagnostic value > soothing value when the user is debugging.

---

## Sequencing

QA-preferred order, optimised for visible-improvement-per-week:

1. **P-05** (spinner) — Week 1. Ships visible motion before anything else lands. Buys patience for the harder work.
2. **P-03 + P-07** (combined) — Week 1–2. Width fixes ship together because shipping P-03 alone produces the half-fix described above (Prompt: widens, Agent: stays at 80).
3. **P-02** (Duration semantics) — Week 2. Lands once snapshot rebaseline from P-05/P-03 is settled.
4. **P-01** (OutputMonitor on per-task path) — Weeks 2–4. The keystone. With P-05/P-03/P-07/P-02 already in, the day P-01 ships the user sees *everything come alive* — bars move, activity stream populates, growth rate ticks, heartbeat (if shipped) becomes meaningful.
5. **P-10** (heartbeat) — Week 4. Ships immediately *after* P-01 to take advantage of meaningful `last_event_time`. Optional in week 4 if P-01 slips; ship in week 5 instead.

This sequencing front-loads the QA-visible wins and back-loads the structurally hard work, which is the opposite of the architect-preferred order — but it is the order in which a user watching the dashboard reports the most successive "this got better" experiences.

---

## Manual Smoke-Test Acceptance Criteria

For each top-5 fix, what would QA ACCEPT or REJECT as proof during manual smoke?

**P-01 (OutputMonitor on per-task path)**:
- ACCEPT: Run a 3-task per-task phase. The Tasks bar advances visibly (not in one jump) at task boundaries. The activity log shows ≥1 event during each task. growth_rate_bps is nonzero. The TUI does *not* require a keypress to refresh.
- REJECT: Bars still jump in one step at phase end. Activity log shows `— — —` for the full task. growth_rate_bps stays at zero. NDJSON event count from the file does not match TUI-displayed count within 1.

**P-02 (Duration column)**:
- ACCEPT: Open a sprint; the Duration column for the running phase displays an integer that *increases monotonically every second* and never decreases. After phase ends, the column shows the final elapsed time (matching wall-clock observation ±1 s).
- REJECT: Duration shows `0s` while phase is running. Duration decreases when new events arrive (indicates the bug was not fixed and the stall_seconds value is still being read).

**P-03 (dynamic prompt/agent width)**:
- ACCEPT: On a 200-column terminal, the Prompt: line displays text wider than 60 chars. Resizing the terminal mid-sprint reflows the next render's Prompt: line to the new width. The active panel does not flicker height-wise.
- REJECT: Prompt: line still clipped at 60. Active panel height flickers on every refresh. Long prompts wrap to a second line (because truncation math is off).

**P-05 (spinner)**:
- ACCEPT: Within 2 s of sprint start, the RUNNING row's status cell shows a visible cycling glyph. The active-panel title also shows a cycling glyph. Both cycle at ~10 Hz (the Rich default for `dots`). When the executor is intentionally paused (e.g. during PreFlight), the spinner continues to cycle.
- REJECT: Status cell shows static `RUNNING` text. Spinner cycles only when events arrive (means it's coupled to push events rather than `Live.refresh_per_second`). Spinner glyphs render as `?` or boxed characters (terminal font issue).

**P-10 (heartbeat)**:
- ACCEPT: A line in the active panel reads `Heartbeat: ● Ns ago — tokens N/s`. The N value increments approximately every second when no events are arriving and resets to 0 when an event lands. The dot is green when `<5 s`, yellow when `5–30 s`, red when `>30 s`. (Test by intentionally blocking the subprocess and watching the dot change colour.)
- REJECT: Heartbeat permanently reads `0.0s ago` (means the sentinel fix from the proposal was not applied). Dot colour does not change. Token rate is permanently zero (means `growth_rate_bps` is not flowing — failure of P-01 dependency rather than P-10 itself, but blocks acceptance).
