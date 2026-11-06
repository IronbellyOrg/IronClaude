# Concept comparison

## First set
| Design | Dominant composition / five-second question | Intentional omission and failure mode |
|---|---|---|
| Signal Bridge | Three unequal vertical regions: question/sources, session register, counts. Who needs attention while work continues? | Time history omitted; dense registers can distract from the selected question |
| Fleet Quilt | Stable owner territories and identified session cells. Where are exceptions clustered? | Detailed proof omitted; cells must not hide full identity or imply progress |
| Time Loom | Shared-axis lanes beside selected question and source rail. Where did recorded time go? | Costs omitted; observation gaps must not look like idle work |
| Worktree Atlas | Workspace directory with selected branch/base/path inspector. What is isolated or shared? | Dependency topology omitted; shared paths are not confirmed conflicts |
| Decision Desk | Selected human question, other asks and affected-session evidence. What is mine to decide? | Unaffected fleet omitted; question ownership cannot be inferred from a relay |
| Proof Gate | Revision ledger with selected proof and admission details. Are checks tied to the current head? | Timeline omitted; revision match alone does not mean fresh, passing or admitted |
| Budget Engine | Owner spend bars plus coverage and resource sidebar. What was actually measured? | Forecasts omitted; a partial subtotal or zero samples must not read as total spend |
| Relay Map | Declared owner dependency routes with evidence labels. Which handoff crosses owners? | Undeclared links omitted; cables must not invent topology |
| Delta Deck | Sequence-ordered change journal with separate counts/baseline panel. What materially changed? | Full current inventory omitted; silence cannot imply resolution |
| Watchkeeper | Source sentinel plus bounded exception and handover notes. What remains unverified? | Throughput rankings omitted; quiet observations cannot justify all-clear |

Per-concept data prerequisites and missing-state behavior are carried in manifest.json and shown in the offline gallery. Every concept uses the same fixture, not separately invented totals.

## Agent-supervision set
| Design | Dominant composition / supervision question | Omission and failure mode |
|---|---|---|
| Leverage Board | Large affected-session figure over decision bundles. Which answer has broad declared impact? | No ETA; overlapping scopes must be deduplicated |
| Attention Ledger | Spacious age-ranked question ledger and ownership rail. What is still waiting for a human? | Resources omitted; seen/delivered is not answered |
| Handoff Switchboard | Heavy terminal sockets and meaningful horizontal cables. Who depends on whose result? | No inferred traffic graph; missing link evidence stays unknown |
| Loop Detector | Repeated attempt boxes with provenance and interpretation panels. Where are retries recorded? | No retry action; repeated output is not repeated execution |
| Collision Lens | Shared-path headline above three branch inspection cards. Which work may overlap? | No merge prediction; same path is not a conflict |
| Outcome Ledger | Explicit lifecycle/report/packet/admission columns. Are finished assignments accepted? | Activity counts omitted; an inspectable packet is not approval |
| Revision Drift | Large mismatch count and old-to-new revision rows. Which proof is stale against the head? | No rerun control; old passes cannot certify current state |
| Mission Pulse | Mission rows with independent lifecycle and admitted counts. What outcomes do owners have? | No composite health score; admission is a subset, not another lifecycle bucket |
| Owner Load | Ownership bars with cautious interpretation and attention rail. Is observed ownership uneven? | No capacity assumption; number of sessions is not utilization |
| Shift Brief | Large human-question count, short narrative and explicit unverified footer. What must the next human know? | Raw logs omitted; handover is not an assurance of completeness |

All second-set functions are separately authored layouts using the same cell renderer and fixtures. They emphasize oversight rather than add operational controls.

## Compact modes and navigation
160-column exports use 48 rows. 116- and 80-column exports use 42 rows and are freshly composed, never shrunk from images. At 116, side inspectors become stacked bands where needed. At 80, selected question/owner/affected scope and header freshness stay visible; secondary inventory is bounded with omission counts and remains accessible in the gallery inspector.

The gallery presents one exact terminal frame in a scroll container at natural monospace size. Long IDs are truncated by display width in the frame and exposed in sanitized full detail. Tab traverses controls; left/right switches concepts; j/k selects inspector records; Space holds the fixture view. Owner/search filtering is deliberately inspector-only and reports filtered versus global record counts. No hidden operational behavior exists. Narrow layouts and full IDs can be inspected independently of the browser viewport by choosing the width control.

No blinking, animations, forced autoscroll, external network calls, LLM polling or live orchestration commands. Color-free mode retains labels/structure; ASCII exports replace box drawings and non-ASCII text safely. Prototype source gaps are disclosed in integration-gaps.md.

## Top three and smallest experiment
**Provisional design judgment, not user approval or measured comprehension:**

1. **Signal Bridge:** useful baseline cockpit with the question separate from raw session state and source coverage.
2. **Proof Gate:** strongest differentiation from simple agent activity views; makes revision evidence and admission visibly independent.
3. **Fleet Quilt:** the most direct overview of 80 sessions while retaining orchestrator territories and individual identity.

For a more distinctive secondary view, pair **Time Loom** with **Relay Map**. For hands-on supervision in the second set, start with **Leverage Board**, **Collision Lens** and **Revision Drift**.

Smallest next experiment: a human walkthrough of those three preferred first-set views with the same synthetic fixture. Ask the viewer to locate the cross-owner decision, identify a stale passing check, find a frozen worktree and state which costs are unknown. Record answers and confusion; do not call five-second readability proven until measured. Only after the human chooses a direction should a separate read-only Charm-stack implementation experiment begin.
