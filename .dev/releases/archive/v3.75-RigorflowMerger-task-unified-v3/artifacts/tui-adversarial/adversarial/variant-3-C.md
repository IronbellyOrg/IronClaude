# Variant C — Top-5 Shortlist

## Lens Statement (self-declared)

This variant evaluates proposals against **effort-to-impact ratio**. Cheap fixes that ship broad visible improvement beat expensive fixes that deliver a single deep win, *unless* the expensive fix has uniquely-large impact that the cheap stack cannot match. Engineering days are the scarce resource. The §3 effort labels (S = <1 day, M = 1–3 days, L = >3 days) are the cost axis; the §2 symptom coverage and §3 expected-behavior claims are the impact axis. An L-effort proposal must clear a higher bar — its impact must be *uniquely* large, not merely large.

Three of the ten proposals are S-effort (P-02, P-03, P-05, P-07, P-10 — actually five), three are M-effort (P-01, P-04, P-06, P-08 — actually four), and one is L-effort (P-09). The S-effort cluster is the natural place to start because shipping 4 S-fixes in two weeks delivers more user-facing improvement than shipping 1 M-fix in the same window — *unless* the M-fix is the keystone.

## Viability Methodology

Viability = `(impact × probability_of_success) / effort` where:
- `impact` (0–5) = number of §2 symptoms addressed (×) weight for "primary" (×2) vs "amplifier" (×1)
- `probability_of_success` (0–1.0) = 1.0 minus penalties for stated risks ("threading hazard" = −0.15, "test rebaseline" = −0.05, "subsumed by other proposal" = −0.10)
- `effort` (S=1, M=3, L=7) = engineering-days approximation

Score normalised to 0–100 by mapping raw ratios to a 0..100 scale where the highest raw ratio = 100.

---

## Top-5 Ranked

### #1 — P-05: Rich spinner on RUNNING status cell and active-panel title

- **Viability**: 95
- **Effort**: S (<1 day)
- **Why it leads (effort-to-impact lens)**: This is the canonical "highest ROI in the file." §2.2 ¶3 establishes that `Live` is already running at 2 Hz, *without any external push being required*. A spinner inserted into the render tree costs zero plumbing — Rich repaints the spinner state every tick using the same `Live` background thread that already exists. Total code surface: one import, two render-tree changes, no executor changes, no monitor changes, no threading changes. The visible-motion impact is large enough to materially change the user's "is it hung?" perception. From a cost-benefit standpoint, this is the *cheapest fix that addresses any §2 symptom at all* (Symptom 2: no real-time indicators). The only competitor on cost is P-02 (one-line change), but P-02 has a dependency on the per-task path that P-05 does not. P-05's effort-to-impact ratio is unbeatable.
- **Effort tier**: S
- **Risks / flaws (effort lens)**:
  1. Snapshot-test rebaseline cost — the proposal admits "Snapshot-based tests of the table will need to be re-baselined." Test count not quantified. Probability_of_success penalty: −0.05.
  2. `Spinner` in `Table.add_row` requires the object, not a string — proposal flags this. The risk is low because `rich.table` accepts renderables, but it warrants a single smoke test. Penalty: −0.02.
  3. No threading risk because no new thread is introduced — the spinner cycles under the existing `Live` thread. This is the proposal's structural advantage and is the reason its effort-to-impact ratio dominates.
- **Effort-to-impact rationale**: 1 engineering-day for ~30% of the §2.2 symptom resolved (i.e. the user-visible "is it alive?" question), with zero plumbing cost. Ratio: ~30 impact-points/day.
- **Dependencies**: none. Ships immediately.

### #2 — P-02: Replace `stall_seconds` with elapsed-since-phase-start

- **Viability**: 90
- **Effort**: S
- **Why it leads (effort-to-impact lens)**: One-line change against a field that already exists (`phase_started_at`, models.py:609). §2.1 final ¶ shows the current Duration column is *categorically wrong* (showing stall-gap instead of phase-elapsed). Fixing wrong data is higher-leverage than adding new data, and this one-liner fixes wrong data. The freeform path benefits *immediately* even before P-01; the per-task path benefits as soon as P-01 lands. Two beneficiaries for one engineering-hour is exceptional ROI.
- **Effort tier**: S
- **Risks / flaws (effort lens)**:
  1. The per-task fallback ("wire `phase_started_at` from the TUI side via `time.monotonic()` captured at first observation of `phase` change") effectively introduces a second writer for the field. Penalty: −0.05 because clean cleanup will eventually be required.
  2. Snapshot tests asserting "0s" need re-baselining. Same low penalty as P-05.
- **Effort-to-impact rationale**: 1 hour of engineering to remove a "wrong number" display defect that hits every sprint. Highest absolute impact per minute of any proposal in the file.
- **Dependencies**: composes with P-01 for full per-task benefit; standalone-useful on freeform.

### #3 — P-01: Wire OutputMonitor into the per-task path

- **Viability**: 85
- **Effort**: M (1–3 days)
- **Why it leads (effort-to-impact lens)**: M-effort proposals must pass a stricter bar. P-01 passes because it is the *only* M-effort proposal whose impact is uniquely large — every other M-effort proposal (P-04, P-06, P-08) depends on P-01 to be useful, so P-01 is *load-bearing* for the M-cluster. From an effort-to-impact lens, paying M-effort once for P-01 enables the entire M-cluster downstream. That is a multiplier the other M-proposals cannot offer. Additionally, §2.1 ¶3 establishes the per-task path is "the modern code path used by virtually every current sprint" — so the *frequency-weighted* impact of P-01 is the impact applied to ~100% of current sprints, not a fraction. That frequency weighting tips the cost-benefit decisively.
- **Effort tier**: M — and I am scrutinising this label carefully because M is the bar where I become picky. The proposal lists three sub-changes (instantiate OutputMonitor in `execute_phase_tasks`, replace `proc.wait()` with poll loop, reset `_last_read_pos`+`_seen_files` between tasks). Each is small in isolation; together they touch the executor's most-used path and require new tests. Three days is plausible; two days is possible if the existing freeform poll loop pattern (executor.py:1303–1381) is genuinely directly copyable as the proposal claims.
- **Risks / flaws (effort lens)**:
  1. The `_last_read_pos` / `_seen_files` reset between tasks is a correctness hazard. Penalty: −0.10 because get-it-wrong scenarios are subtle (lost events, double-counted tasks).
  2. The proposal accesses `proc._process` (an underscore-prefixed attribute) — coupling the executor to `ClaudeProcess` internals. Adding a public `is_running()` adds a tiny amount of work but eliminates a fragile coupling. The "real" effort tier is M+epsilon. Penalty: −0.03.
  3. Test fixtures need updating — proposal flags this. Test count not quantified, but `tests/sprint/test_execute_phase_tasks*.py` are the relevant files; a quick glance suggests 5–10 tests need fixture updates. Penalty: −0.05.
- **Effort-to-impact rationale**: 2–3 days of engineering for the largest single visible improvement on the file. ROI per day is lower than P-05's, but cumulative impact is much larger. Eligible for top-5 despite M-tier because the impact is *uniquely large* — exactly the "unless its impact is uniquely large" exception in the lens definition.
- **Dependencies**: none upstream. Hard prerequisite for P-04 pulse, P-06, P-10's meaningful values.

### #4 — P-03: Drive prompt/agent line width from `console.width`

- **Viability**: 78
- **Effort**: S
- **Why it leads (effort-to-impact lens)**: §2.3 is one of the three reported symptoms. P-03 is the only S-effort proposal that addresses §2.3 directly. The other §2.3-adjacent proposals (P-07, P-08) compound or extend P-03 but P-03 is the minimum viable fix. Cost is roughly 0.5 day (the proposal lists three discrete changes to small areas of two files: tui.py constants, _build_active_panel, config.py extraction slices). Impact is fixing 1/3 of the reported symptoms entirely. That is exceptionally favourable ROI.
- **Effort tier**: S
- **Risks / flaws (effort lens)**:
  1. Flicker risk if panel height changes on text re-flow. Pre-computed `avail` mitigates if the width math is right. Penalty: −0.05.
  2. The proposal bumps extraction caps to `[:240]` without an audit of downstream consumers. Penalty: −0.03 for missing scope.
  3. Without P-07 the Agent: line is still clipped at 80 (because monitor.py:121 pre-trims). So P-03 alone is a partial visible fix. Acceptance might be soft-rejected on review. Penalty: −0.05 with a strong recommendation to combine P-03+P-07 in a single PR (which would push the combined effort to S+S = ~1 day, still excellent ROI).
- **Effort-to-impact rationale**: ~0.5 day for ~80% of §2.3 fixed (Prompt: line, partial Agent: line). With P-07 added (~0.3 additional days) the symptom is 100% fixed at a total cost still under 1 engineering-day.
- **Dependencies**: P-07 is a strong "ship-together" recommendation; not a hard dependency.

### #5 — P-07: Width-aware caps for assistant text, activity, errors

- **Viability**: 65
- **Effort**: S
- **Why it leads (effort-to-impact lens)**: I considered P-10 (heartbeat) for this slot and ultimately gave it to P-07 for one cost-benefit reason: P-07 *completes* the §2.3 fix that P-03 starts, while P-10 only addresses §2.2 (already partially handled by P-05). Marginal-cost analysis: P-03 ships at 0.5 day, P-03+P-07 ships at ~0.8 day total for full §2.3 resolution. P-03+P-10 ships at ~1.0 day for partial §2.3 + partial §2.2 (since heartbeat needs P-01 to display meaningful numbers). The bundled P-03+P-07 has a higher symptom-coverage-per-day return.
- **Effort tier**: S
- **Risks / flaws (effort lens)**:
  1. Touches the monitor layer (relocating `ASSISTANT_TEXT_MAX_LEN` trim out of monitor.py to render-time). This is a small change but expands the test surface for monitor unit tests. Penalty: −0.05.
  2. ANSI escape sequences in error/activity strings could render literally on widened panels. Proposal acknowledges; no mitigation in code. Penalty: −0.03.
  3. P-03 is a soft prerequisite — without P-03's render-side `console.width` query, P-07's stored full assistant text still gets re-trimmed by `_LLM_LINE_MAX=60`. Penalty: −0.05.
- **Effort-to-impact rationale**: ~0.3 day to complete the §2.3 fix bundle started by P-03. Independent value is lower but bundled value with P-03 is the highest-leverage §2.3 ROI in the file.
- **Dependencies**: composes with P-03; independent value smaller.

---

## Held Back

- **P-10 (heartbeat line)** — S-effort, looks like a cheap win, but the proposal openly states the heartbeat is dead-on-arrival on the per-task path without P-01 ("would always show `0.0s ago`"). Net effort to get useful behaviour: P-10 + P-01 = M+S = M-effort total. ROI as a standalone S is misleading. After P-01 lands, P-10 becomes a strong slot-6 candidate; before P-01 lands, P-10 is wasted engineering.
- **P-04 (Rich Progress with BarColumn(bar_width=None))** — M-effort. Impact is real (bars stretch + pulse during thinking) but the pulse requires P-01's monitor wiring to set `stall_status` on the per-task path. So P-04 alone is "bars stretch but still hung" — a half-fix. With P-01, the visible benefit IS large, but at M+M = ~5 days total, compared to P-01+P-05 = M+S = ~4 days for comparable user-perceived motion. P-04 is the right *long-term* fix for the bars but loses the head-to-head against the P-01+P-05 stack on cost-per-visible-improvement. Held back.
- **P-06 (events/sec sparkline)** — M-effort. Visible value is "nice graph" rather than "fixed bug". Symptom coverage is 0 of 3 (it's an additional widget, not a fix). Even the proposal admits it's flat without P-01. Worst effort-to-impact ratio in the M-cluster. Excluded.
- **P-08 (Layout tree)** — M-effort. The visible benefit (resize-responsive layout) is already 80% achieved by P-03+P-07+P-04 collectively. P-08's marginal value over that stack is small. Test rebaseline cost is high (the proposal flags "Re-baseline TUI snapshot tests"). Worst effort-to-marginal-impact in the M-cluster. Excluded.
- **P-09 (event-driven render thread)** — L-effort. The only L-proposal. Visible impact (latency reduction from 500 ms to 250 ms) is imperceptible to humans. Internal-correctness impact is large but invisible. ROI per day is the worst on the file. The proposal *itself* recommends deferring ("queue for a later wave"). Excluded with the strong caveat that it should be the *next wave's* anchor proposal.

## Flagged Large-Effort Proposals

There is exactly one L-effort proposal in the file: **P-09 (event-driven render thread)**. By lens definition, an L-effort proposal must clear a uniquely-large impact bar to earn a slot. P-09 fails this bar:

- **Visible impact**: ≈zero. The user cannot perceive a 250 ms latency reduction.
- **Internal impact**: large, but not addressing any §2 symptom directly. It is an architectural improvement that *enables* future fixes rather than delivering current ones.
- **Test surface impact**: large. The proposal admits "existing tests that simulate `tui.update` directly need to adapt to the event API". Reshapes test contract for downstream changes.
- **Risk**: "introduces a new thread + queue; care needed around clean shutdown (sentinel event, `_render_thread.join(timeout=2)` in `stop()`); existing tests that simulate `tui.update` directly need to adapt to the event API; potential ordering bugs if `PhaseStart` is processed after a stale `MonitorTick`." Three named risks for one L-effort proposal.

**Verdict**: Excluded from top-5. Strong candidate for the *next* sprint after the top-5 lands and the cadence shortcomings of the push model are measured (mirroring the source's own §4 recommendation). It is the right *follow-on* L-fix once P-01..P-05 have shown what's still broken.

## Contested Calls

### Defending P-05 above P-01 — likely contested by architects

**Strongest counterargument**: "P-01 fixes the dominant root cause (per-task path bypasses OutputMonitor). P-05 adds a spinner. A spinner is a band-aid; P-01 is the cure. From any structural lens P-01 must rank above P-05."

**Steelmanned**: P-01 addresses the actual broken plumbing for the most-used path. P-05 paints over the symptom without fixing the disease. Long-term, P-01's value is much larger.

**Defence**: The lens here is effort-to-impact, not absolute impact. P-05 ships in 1 day; P-01 ships in 2–3 days. P-05 delivers ~30% of §2.2 resolved (the "is it alive?" feeling) for 1 day. P-01 delivers ~80% of §2.1+§2.2 resolved for 2.5 days. Per-day ROI: P-05 = 30%/day = 0.30, P-01 = 80%/2.5 = 0.32. They are *within* the noise of each other on per-day ROI — and P-05 has zero dependency risk. The tie-break that pushes P-05 to #1 is independence: P-05 ships immediately and is unaffected by failure of any other proposal. P-01 has named threading and reset risks. From a portfolio-risk lens, ship the highest ROI low-risk item first. That is P-05. P-01 is #3, not because its impact is low, but because we should ship the certain wins before the high-impact risky bets.

### Defending P-07 in slot #5 over P-10

**Strongest counterargument**: "P-10 directly answers the user's most-asked diagnostic question ('is it dead?') with a moving timer and a colored dot. P-07 widens some error and activity strings. P-10 has more user-visible impact than P-07."

**Steelmanned**: A heartbeat is a higher-information widget than a wider activity string. Information density per pixel is higher for P-10.

**Defence**: Per the lens, the question is impact-per-engineering-day, not impact-per-pixel. P-10's effort is S, but its *useful* effort is S + the cost of P-01 (because without P-01 the heartbeat reads `0.0s ago` permanently — a visible failure). P-07's useful effort is S, and it composes with P-03's S to fully resolve §2.3. P-07 ships meaningful improvement at S-cost; P-10 ships meaningful improvement at S+M cost (effective). Per-day ROI tips P-07 ahead. I would accept P-10 at slot #6.

### Defending exclusion of P-04

**Strongest counterargument**: "P-04 is the original v3.7b SPEC intent — it's what was always supposed to be there. The hand-rolled bars are a deviation from intent. Excluding P-04 means leaving the wrong design in place indefinitely."

**Steelmanned**: P-04 is not a 'nice to have' — it is *correctness against the original specification*. Excluding it perpetuates a documented design deviation.

**Defence**: I am genuinely persuaded this is a fair critique. P-04 is correct in intent and the source itself notes it was the original SPEC. The reason for exclusion is purely cost-benefit timing: post-P-01, the hand-rolled bars *will* update correctly; P-04 then becomes a *cosmetic* improvement (bars stretch + pulse) rather than a functional fix. M-effort for cosmetic-after-P-01 is bad cost-benefit. P-04 deserves to land in the next wave alongside P-09 — that wave's narrative is "land the architectural corrections that the SPEC always intended". The exclusion is timing, not principle.

---

## Sequencing

Optimised for cumulative visible-improvement-per-engineering-day:

1. **Day 1 — P-05** (spinner): Ships visible motion immediately. Zero downstream coupling. Zero new threads. Buys reviewer goodwill for the rest of the wave.
2. **Day 1–2 — P-02** (Duration semantics) + **P-03 + P-07** (combined width fix): Three S-fixes shipped as either one or two PRs (P-02 alone; P-03+P-07 together). Total ~1.5 days. Snapshot rebaselines done once.
3. **Days 3–5 — P-01** (OutputMonitor on per-task path): The keystone. Lands with the cosmetic fixes already in place so the day P-01 ships the user sees *all* widgets come alive simultaneously — the spinner is alive (was already), the bars are alive (newly), the Duration ticks correctly (newly), the prompt and agent lines are full-width (already), the activity stream populates (newly). Maximum perceptible-improvement-per-merge.

Total wave cost: ~5 engineering-days for full top-5 delivery. Subsequent wave: P-04 + P-10 (with sentinel fix) + P-09 as the architectural follow-on.

This ordering is the same as the QA-preferred order — agreement between the effort and QA lenses is the empirical signal that this sequencing is correct. The architect lens favours landing P-01 first; that ordering is structurally cleaner but ships less visible improvement per week.
