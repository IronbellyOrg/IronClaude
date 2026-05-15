# Diff Analysis: TUI Top-5 Shortlist Comparison

## Metadata
- Generated: 2026-05-14
- Variants compared: 3 (anonymised A, B, C)
- Total differences found: 18 (5 structural, 4 content, 2 contradictions, 3 unique contributions, 4 shared assumptions)
- Categories: structural (5), content (4), contradictions (2), unique (3), shared assumptions (4)

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | Top-section order | Lens Statement → Methodology → Top-5 | Lens Statement → Methodology → Top-5 | Lens Statement → Methodology → Top-5 | Low |
| S-002 | Methodology formula | coverage × confidence × independence | visible_movement × cadence × symptom_coverage | (impact × P_success) / effort | Medium |
| S-003 | Held-back item count | 5 | 5 | 5 | Low |
| S-004 | Distinctive section beyond template | (none beyond template) | "Manual Smoke-Test Acceptance Criteria" — adds ACCEPT/REJECT criteria per proposal | "Flagged Large-Effort Proposals" — explicit analysis of P-09 cost | Medium |
| S-005 | Sequencing labels | Step-numbered list with rationale | Week-numbered (W1, W1-2, W2, W2-4, W4) | Day-numbered (Day1, Day1-2, Days3-5) | Low |

## Content Differences

| # | Topic | Variant A approach | Variant B approach | Variant C approach | Severity |
|---|---|---|---|---|---|
| C-001 | Slot #1 (highest-ranked proposal) | P-01 keystone-first; viability 88 | P-01 keystone-first; viability 92 | **P-05 spinner**; viability 95 — P-01 demoted to #3 | **High** |
| C-002 | Treatment of P-07 | Slot #4; layering-correction rationale | Held-back (subsumed-with-P-03); ranks P-10 #5 | Slot #5; cost-bundling-with-P-03 rationale | Medium |
| C-003 | Treatment of P-10 | Held-back; partially dead-on-arrival critique | Slot #5; downgraded to viability 70 via P(dependency)=0.82 multiplier | Held-back; "effective effort is S+M not S" | High |
| C-004 | Sequencing of P-01 | P-01 ships *last* among top-5 ("fireworks") | P-01 ships in weeks 2-4 (after P-05/P-03/P-07/P-02) | P-01 ships on days 3-5 (after P-05/P-02/P-03/P-07) | Low — all three agree P-01 ships after the cheap fixes |

## Contradictions

| # | Point of Conflict | Variant A | Variant B | Variant C | Impact |
|---|---|---|---|---|---|
| X-001 | What is the #1 proposal? | P-01 (keystone) at rank #1, viability 88 | P-01 (keystone) at rank #1, viability 92 | **P-05 (spinner) at rank #1, viability 95; P-01 demoted to #3 with viability 85** | **High** — direct ranking contradiction at the top slot. Resolution: lens collision. A+B treat P-01 as load-bearing; C ranks portfolio-risk-adjusted ROI and places the certain S-fix above the higher-impact M-fix. |
| X-002 | Is P-10 in or out of the top-5? | OUT (held-back) | **IN at slot #5** with viability 70 (P(dep)-discounted) | OUT (held-back; "effective effort is S+M") | **Medium** — 2-vs-1 split. A and C exclude P-10 on the same evidence base (dead-on-arrival without P-01); B includes it on the proposal's sentinel-mitigation footnote. |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | B | **Per-proposal Manual Smoke-Test Acceptance Criteria** (ACCEPT/REJECT statements grounded in observable screen behavior, with explicit edge cases) | **High** — converts ranking into a testable spec the implementer can execute against. Neither A nor C provides this. |
| U-002 | C | **Explicit per-day ROI calculations** (e.g. "P-05 = 30%/day = 0.30, P-01 = 80%/2.5 = 0.32") and L-effort flagging methodology | **High** — quantifies the cost-benefit reasoning A and B describe qualitatively. Useful as evidence in a decision review. |
| U-003 | A | **Architectural layering critique** (assistant-text trim relocation from monitor.py to render-time; "monitor stores, renderer trims") | **Medium** — identifies a structural correction in P-07 that neither B nor C surfaces; the layering insight is the architect-specific lens. |

## Shared Assumptions

| # | Source Agreement | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three rank P-01 in top-5 and all three identify §2.1's per-task-path-bypasses-OutputMonitor as the dominant root cause | "The §2 root-cause diagnosis is accurate — i.e. `_tui_state = MonitorState()` at executor.py:981 really does construct a fresh empty state on every per-task TUI update, and no `OutputMonitor` is started on the per-task path." | STATED (cited in all three variants) | No |
| A-002 | All three sequence P-05 (spinner) before P-01 (monitor wiring) | "Snapshot test rebaseline cost from P-05 will not block subsequent PRs (i.e. test-rebaseline serialisation is acceptable)." | UNSTATED — none of the variants state this; all three assume the test surface can absorb back-to-back rebaselines | **YES → A-002** |
| A-003 | All three accept that the freeform poll-loop pattern at executor.py:1303–1381 is "directly copyable" to the per-task path | "OutputMonitor's incremental-read pointer state machine actually works correctly when reset between tasks — i.e. the proposal's mitigation ('reset _last_read_pos and _seen_files between tasks') is implementable without further refactoring of monitor.py." | UNSTATED — the proposal flags the hazard but does not verify the reset semantics | **YES → A-003** |
| A-004 | All three treat the effort labels (S/M/L) in §3 as accurate | "The effort estimates in the source are correct. M-effort really is 1-3 days for P-01 with the test fixture work included." | UNSTATED — no variant audits the effort labels against actual code complexity | **YES → A-004** |

### A-002 — Test rebaseline serialisation
**Impact**: All three sequencing recommendations assume snapshot tests for tui.py can be rebaselined in successive PRs without blocking each other. If snapshot rebaseline requires a longer review cycle than coding, the bottleneck is review-throughput not engineering-days, and the cost analysis shifts.
**Status**: Promoted for debate.

### A-003 — Reset semantics implementable
**Impact**: P-01's risk callout flags the reset hazard but assumes the mitigation is straightforward. If monitor.py's `_seen_files` requires significant refactoring to safely reset between tasks (e.g. it's stateful in ways the proposal doesn't anticipate), the M-effort label for P-01 is wrong and the entire sequencing shifts.
**Status**: Promoted for debate.

### A-004 — Effort labels accurate
**Impact**: All viability scores are computed against the source's effort labels. If any label is wrong by one tier (e.g. P-01 is actually L not M, or P-09 is actually M not L), the rankings change materially. No variant audits the labels.
**Status**: Promoted for debate.

---

## Summary

- Total structural differences: 5
- Total content differences: 4
- Total contradictions: 2 (one HIGH at rank #1, one MEDIUM at P-10 inclusion)
- Total unique contributions: 3 (one each from A, B, C — all rated Medium-High)
- Total shared assumptions surfaced: 4 (STATED: 1, UNSTATED promoted: 3, CONTRADICTED: 0)
- Highest-severity items: X-001 (Variant C ranks P-05 above P-01), C-001 (same content lens)

**Convergence baseline**:
- All three variants include: P-01, P-02, P-03, P-05 (4 of 5 slots)
- Slot #5 split: A picks P-07, B picks P-10, C picks P-07 → 2/3 majority for P-07
- Variants agree on the same 4-of-5 proposals and 2/3 agree on slot #5 — high baseline convergence on *which* proposals belong, despite disagreement on ranking order.
