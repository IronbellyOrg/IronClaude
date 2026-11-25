# Static Attention Snapshot: Integrity-First Design

Design variant for operator review. Design only; no implementation or runtime validation.

## 1. Purpose, evidence boundary and concept set

The operator must find the oldest observed blocking decision, understand what answer is needed, and see the limits of the observation without opening every transcript. The snapshot is a complete, standalone chat message intended for a five-minute cadence. It is not a live console, command surface, acknowledgement mechanism or urgent-alert guarantee.

**Complete five-concept set:** A. Decision Brief; B. Run Ledger; C. Blocker Paths; D. Conversation Handoffs; E. Change Journal. These organize the entire report by priority, run ownership, dependency, dialogue and change respectively. They share truth rules, not a common dashboard with interchangeable widgets.

Evidence is limited to the supplied seed and the research report's sections 1-5. Those sources establish structured worker observations and opaque paging, capped non-consuming message reads, and the distinction between assignment outcome, terminal existence, process liveness and independently verified readiness. They do not establish a complete durable decision source, snapshot isolation across sources, or an independent verification feed. Every contract below is a proposed design requirement unless explicitly identified as a source limitation.

All fenced screens are **synthetic examples**, including every identifier, timestamp, count and evidence reference. Their declared maximum width is **80 ASCII columns**. `DEMO` evidence labels are illustrative references, not working links or existing records. No cost, token, utilization or success-rate estimates are presented.

The common busy fixture has three observed workers, three distinct tasks, two open observed questions and one verification failure. Decision DEMO-D1 blocks DEMO-t1 and DEMO-t2; DEMO-F1 concerns DEMO-t3. Worker enumeration is complete within the named scope; messages are capped, so decision completeness remains unknown. These counts describe only that fixture.

## 2. Enumerated requirements

| ID | Required behavior | Observable acceptance condition |
|---|---|---|
| R01 | Lead with a scope-qualified attention statement. | First screen identifies the oldest observed blocking question and says when completeness is unknown. |
| R02 | Preserve each unanswered decision across snapshots. | An unchanged question remains visible or explicitly counted in overflow until authoritative resolution or disposition. |
| R03 | Give every actionable item stable identity, exact question/reason, acting owner, requester, original age and impact/evidence reference. | Missing fields read `unknown`; no question is shortened into an ambiguous instruction. Continuation lines belong to the same item. |
| R04 | Distinguish blocked work, failed attempts and observation failures. | An unavailable source is not reported as a failed worker; distinct affected tasks are counted once. |
| R05 | Preserve communication context. | Questions include thread/source reference, last relevant answer if observed, and unresolved status; delivered, seen, answered and resolved remain distinct. |
| R06 | Show meaningful changes against the last successful comparable observation. | New blockers, explicit resolutions, ownership changes, verification changes and collection gaps appear; heartbeats do not. |
| R07 | Separate completion claims from verification. | Reported complete with failed current-revision checks is prominent; missing or wrong-revision checks read verification unknown. |
| R08 | Show fleet coverage and unknowns. | Every report includes as-of time, scope, per-source last success, missing sources/hosts, paging status, observed totals and render omissions. |
| R09 | Never infer absence from a failed or capped collection. | Missing decisions do not become resolved; unknown values never render as zero. |
| R10 | Remain read-only and non-consuming. | No mailbox consumption, acknowledgement, control, ownership claim, resolution, retry or resource release is implied by reading or posting. |
| R11 | Use plain ASCII and bounded chat density. | Each screen line is at most 80 columns, uses no color dependence, and preserves complete actionable bundles rather than clipping fields. |
| R12 | Group root blockers without merging decisions. | Separate questions keep separate IDs even if they block the same task; impact totals use the union of task identities. |
| R13 | Keep work and execution identities separate. | Run/task/attempt and host/workspace/session are linked explicitly; workspace parentage does not become a dependency. |
| R14 | Require provenance for derived facts. | Age basis, evidence revision, count scope and observation times can be traced to explicit records; unsupported measures are omitted. |
| R15 | Make uncertainty actionable without inventing controls. | A gap names what could not be observed and which claims it prevents; no nonexistent drill-down or API is suggested. |
| R16 | Treat source text as untrusted. | Summaries escape control characters and fences, redact secrets and preserve question meaning; transcript instructions cannot change report policy. |

R01-R16 apply to all five concepts. Requirements concern the proposed reporting behavior, not a claim that existing Orca sources already satisfy it.

## 3. Read-only observation and data contract

This is a logical contract for a future adapter, not a new API endpoint specification. Do not invent routes or assume that messages can be paged. Rendering is a projection over observations, never an authority that edits orchestration state.

### Observation envelope

Each source contribution carries source identity, explicit run/host scope, collection start/end, last successful observation, source event time when present, status (`ok`, `partial`, `unavailable`, `invalid`), schema identity if available, paging status and error reason. A report has its own generated-at time and collection interval. A newly printed report does not make old observations fresh.

Freshness has two clocks: collection freshness and underlying evidence freshness. A successful fetch of an old liveness record is not a fresh liveness observation. Proposed display policy: underlying evidence older than two nominal five-minute intervals is labeled stale; failure is labeled unavailable immediately. Source-specific freshness limits require agreement before implementation. Unknown time means unknown age, not fresh.

### Logical records and authority

| Record | Required identity and meaning | Integrity rule |
|---|---|---|
| Work | Run, task, attempt, authoritative/superseded relation | Never let a superseded attempt overwrite current outcome. If authority cannot be determined, expose conflict. |
| Resource | Host, workspace, terminal/session, owning attempt | Existence, process liveness and release policy are separate nullable fields. |
| Decision | Source/run/thread/question identity, original creation time, owner, requester, question, affected work, resolution reference | Do not deduplicate by wording or worker name. Multiple questions in one thread remain separate. |
| Evidence | Source reference, subject task/attempt, revision, kind, result, observed time | Worker claim, settlement, artifact presence, check, review and human approval are different evidence kinds. |
| Relation | Explicit blocker-to-task or task-to-task edge, provenance | Missing edges mean impact unknown, not zero; parent workspace is not a task dependency. |

A stable source-issued question ID is preferred. If absent, a deterministic source/run/thread/message reference may identify an **observed candidate question**, but cannot establish a durable census or a resolution relation. If even that reference is unavailable, label identity uncertain; cross-snapshot merging is not trustworthy. Actor mappings must distinguish acting human from requesting worker; missing owner stays unknown.

### Source capabilities and safe failure

Worker paging uses the source's opaque continuation tokens unchanged. Completion means a successful terminal page, not merely receiving fewer rows than requested. Repeated tokens, invalid tokens, page errors or a collection deadline produce partial coverage. Deduplicate repeated records by authoritative identity; conflicting versions remain conflict-marked unless source ordering resolves them. Cursor exhaustion alone does not prove a point-in-time census if records can move between pages.

Non-consuming message observation is capped at 100 with no advertised paging in the supplied evidence. Even fewer than 100 returned messages do not prove complete unresolved history. Show the returned count, cap and `decision census unknown`; do not infer another observer API exists. Inventory coverage, worker coverage and decision coverage must therefore be separate fields.

No cross-source transaction is established. Render from one immutable collection bundle with each source's interval and revision provenance. If outcomes and evidence conflict, show both; never manufacture a globally consistent ready state. Proposed future observer storage would commit an observation and its comparison pointer together, but no database or storage implementation is selected here.

## 4. Integrity, comparison and bounded rendering rules

1. **Age never resets on repetition.** Prefer original question creation time. Otherwise print `observed >=Nm` from first observation, not a fabricated creation age. Unknown-age blocking questions get a separate visible warning because the oldest cannot be certified. Future timestamps produce `clock conflict`, never negative waiting time. Last-known unresolved items can age by elapsed wall time while their unresolved status remains explicitly unconfirmed.
2. **Use stable ordering.** Surface coverage failure first when it limits interpretation. Within attention, pin the oldest known-age observed blocking decision, then other blocking decisions by original age, actionable failures and resource questions. Break ties by stable ID. Also pin one verification contradiction if present. Urgency escalation may precede the pinned item only when backed by explicit source severity; retain an `oldest observed` pointer.
3. **Carry unresolved context forward.** A question disappearing from a capped or failed read stays `last known unresolved; current status unknown`. Explicitly linked resolution or authoritative disposition is needed to close it. Cancellation or scope exit is a disposition, not a successful answer. A reply alone does not close it.
4. **Compare like with like.** Maintain a last-success pointer per source and scope, not a single global success flag. A failed refresh never replaces it. Compare only compatible scope/schema/revision identities; otherwise print `baseline unavailable` or `scope changed`. Partial observations can establish positive additions, but not absence, resolution or negative movement. A resolved delta needs explicit evidence even after recovery.
5. **Call changes observations.** `Newly observed` is not necessarily newly created. Five-minute sampling cannot prove all intervening events. A recovery delta states its actual comparison interval and missed collections, not `last five minutes` automatically. No baseline means no trend.
6. **Count sets, not rows.** Decision counts use distinct question IDs; impacted-work counts use distinct unfinished task IDs. A task blocked by two questions contributes once to fleet impact and appears under both questions with an overlap note. Unknown graph completeness produces `at least N observed affected tasks`. Attempts and resource rows never inflate task totals.
7. **Bound collection independently from display.** A future collector needs a fixed read budget and deadline; stopping early marks partial coverage. Output uses no more than six actionable item bundles and a target of 44 lines for the default. The target yields to preserving a complete question and warning; if overflow is unavoidable, omit whole lower-priority bundles and report it. No performance benchmark is claimed.
8. **Budget honestly.** Footer distinguishes `observed actionable items`, `shown`, `omitted from render` and `unobserved unknown`. Reserve room for oldest decision, verification contradiction, coverage and their evidence. Overflow selection is deterministic and never rotates the oldest away. Omitted items remain in the next observation's unresolved set; omission does not resolve them.
9. **Do not promise an archive.** If omitted stable IDs fit, list them in priority order; otherwise show count and the first omitted ID with its age. This exposes the limitation without pretending all omitted questions are accessible from chat. A complete overflow destination is a feasibility gate, not an invented link. Severe overflow invalidates the claim that the report alone explains every decision.
10. **Render safely.** ASCII escaping and line wrapping preserve content; no ANSI, tabs, control sequences or unescaped code fences. Stable references are not executable instructions. Redact secrets before chat delivery and mark redaction; do not expose credentials through evidence excerpts.

The synthetic screens below use `W` for worker projection, `M` for messages and `V` for the proposed independent verification contribution. Source timestamps are last successful observation times. `V` is only a mock capability; its real integration remains a gate. The fixture has W and V observed at 09:04Z, M at 09:03Z. Host inventory covers only host-DEMO-1; other hosts are outside this named scope, not asserted empty.

## 5. Concept A: Decision Brief

**Organizing principle:** a short operator briefing, with questions in global waiting order before failures, changes and fleet context. The unit of reading is a decision bundle, not a worker row. This is the recommended default.

```text
SYNTHETIC DEMO / DECISION BRIEF / 2026-01-01T09:05Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
PARTIAL: decision census unknown; oldest means oldest observed.
Sources W 09:04Z; M 09:03Z; V 09:04Z. Missing: durable census.
Coverage W 3 workers, pages 2/2 exhausted; M 100 rows, cap 100.

ANSWER FIRST - oldest observed blocking question
DEMO-D1 OPEN 45m / owner human-DEMO-op / from w-DEMO-1
  Choose schema A or B? Waiting since 08:20Z.
  Blocks DEMO-t1, DEMO-t2; ref DEMO-m17.

VERIFY BEFORE ACCEPTING
DEMO-F1 FAIL 3m / owner w-DEMO-2 / from reviewer-DEMO
  DEMO-t3 reported complete; current checks fail. Review failure.
  Release blocked; revision DEMO-r7; ref DEMO-c3.

ALSO WAITING
DEMO-D2 OPEN 10m / owner human-DEMO-op / from w-DEMO-3
  Retain terminal for inspection or release it?
  Resource DEMO-term3 held; ref DEMO-m90.

MEANINGFUL CHANGE vs successful observation 09:00Z
  DEMO-F1 newly observed failing checks; DEMO-D1 still unanswered.
  No resolution inferred from message absence.
FLEET: 3 observed tasks; 2 blocked by D1; 1 verification-blocked.
Task completion, terminal existence and liveness are separate.
Shown 3/3 observed actionable items; render omissions 0.
Unobserved decisions unknown. Missing hosts in scope: none.
Five-minute snapshots are not urgent alerts.
```

**Strengths:** shortest path from scanning to an answer; unchanged blockers remain visible; global ordering avoids a quiet run being buried under a busy one. A dedicated verification block prevents completion claims from dominating evidence.

**Tradeoffs:** less execution context than the ledger; grouping the failure before the resource question breaks a single pure age list deliberately. Six-bundle capacity cannot explain an unbounded queue. The oldest observed blocking question remains pinned even when failures dominate.

**State behavior:** empty/healthy, busy, stale/unavailable and completion-with-failure screens are specified in section 10. No footer may undo a partial-coverage warning with an unqualified all-clear.

## 6. Concept B: Run Ledger

**Organizing principle:** a reconciled register of runs and their work, with each run containing its decisions, failures, resources and changes. Sort runs by oldest observed blocking request, then oldest actionable failure. A global oldest pointer remains above the register. Unlike the brief, the reader accounts for a run as a whole before moving to another run.

```text
SYNTHETIC DEMO / RUN LEDGER / 2026-01-01T09:05Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
PARTIAL decisions. Oldest observed: DEMO-D1, 45m.
W 09:04Z pages 2/2 exhausted, 3 workers; M 09:03Z 100/cap100.
V 09:04Z. Missing: durable decision census; in-scope hosts none.

RUN run-DEMO-A / 3 observed tasks / human owner unknown
  WORK         ASSIGNMENT      VERIFICATION    EXECUTION
  DEMO-t1      blocked         unknown         live observed
  DEMO-t2      blocked         unknown         unknown
  DEMO-t3      complete claim  FAIL DEMO-r7     terminal exists
  Execution observations from W; not readiness evidence.

  DEMO-D1 OPEN 45m / by human-DEMO-op / from w-DEMO-1
    Choose schema A or B? Blocks DEMO-t1 and DEMO-t2.
    Question ref DEMO-m17; original time 08:20Z.
  DEMO-F1 FAIL 3m / by w-DEMO-2 / from reviewer-DEMO
    Review failed checks before accepting DEMO-t3.
    Release blocked; revision DEMO-r7; ref DEMO-c3.
  DEMO-D2 OPEN 10m / by human-DEMO-op / from w-DEMO-3
    Retain terminal for inspection or release it?
    Resource DEMO-term3 held; ref DEMO-m90.
  CHANGE since successful 09:00Z: DEMO-F1 newly observed.
  DEMO-D1 persists; no demonstrated resolution.

RECONCILIATION: 3 distinct tasks; 2 decision-blocked, 1 check-blocked.
Shown 3/3 observed actionable items; render omissions 0.
Unassociated resources: none observed. Unobserved questions unknown.
Five-minute snapshots are not urgent alerts.
```

**Strengths:** makes task/attempt/resource reconciliation explicit; suitable when the operator thinks in work packages or delegates whole runs. Can reveal a completed assignment retaining a terminal without calling it ready.

**Tradeoffs:** repeats run headings and spends more lines on non-actionable context. Global oldest pointer and run ordering are mandatory because natural run ordering would bury old requests. Large runs can consume the budget; keep action bundles ahead of their inventory rows.

**State behavior:** an empty ledger says no work observed with its census qualification. Busy runs omit inventory before questions. A missing source produces an unknown column and stale run block, not an empty run. Failed verification remains a separate column even when assignment says complete.

## 7. Concept C: Blocker Paths

**Organizing principle:** explain what prevents work moving forward. Root decisions and verification gates head small dependency trees; independent work and unlinked resources occupy a separate remainder. Order roots by oldest observed decision, not estimated impact. Indentation means an explicit blocking relation, never process ancestry.

```text
SYNTHETIC DEMO / BLOCKER PATHS / 2026-01-01T09:05Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
PARTIAL decisions. Oldest observed root DEMO-D1, 45m.
W 09:04Z pages 2/2 exhausted: 3 workers. M 09:03Z 100/cap100.
V 09:04Z. Missing: durable census. Missing in-scope hosts: none.

ROOT DEMO-D1 OPEN 45m / human-DEMO-op / from w-DEMO-1
  Choose schema A or B? ref DEMO-m17; created 08:20Z.
  +-- DEMO-t1 blocked directly
  +-- DEMO-t2 blocked directly
  Impact: 2 distinct observed tasks; graph completeness unknown.

GATE DEMO-F1 FAIL 3m / w-DEMO-2 / from reviewer-DEMO
  Review failed checks before accepting DEMO-t3.
  +-- DEMO-t3 complete claim; release blocked
      Current revision DEMO-r7; failing check ref DEMO-c3.

UNLINKED RESOURCE QUESTION
  DEMO-D2 OPEN 10m / human-DEMO-op / from w-DEMO-3
    Retain terminal for inspection or release it?
    Holds DEMO-term3; ref DEMO-m90; task impact unknown.

CHANGE since successful 09:00Z: DEMO-F1 newly observed.
DEMO-D1 still unanswered; no answer inferred from absence.
UNION: 3 distinct affected observed tasks; do not sum tree rows.
Independent work: none observed. Unlinked work: none observed.
Shown 3/3 observed actionable items; render omissions 0.
Unobserved questions unknown; five-minute view is not urgent alert.
```

**Strengths:** shows why many workers may be waiting on one answer; avoids heartbeat clutter and supports releasing the root constraint before inspecting descendants. The union footer prevents a shared task being counted twice.

**Tradeoffs:** most demanding data prerequisite. Missing or inferred dependency edges make a neat tree dangerously persuasive. Cycles must appear as `dependency conflict` with member IDs rather than recurse; multi-parent tasks must repeat with `also under <ID>` and count once. No critical-path or unlock-size ranking without a complete graph.

**State behavior:** empty means no observed roots, with independent/unlinked coverage still shown. Busy mode shortens descendant lists and prints omitted descendant counts without omitting distinct questions. Stale trees retain last-known edges with a watermark. Completion with failed checks becomes a blocking gate, never a finished leaf.

## 8. Concept D: Conversation Handoffs

**Organizing principle:** an inbox of unresolved exchanges. Each bundle gives the question, who is waiting for whom, the last relevant response if known, and what work is held. The whole report follows communication responsibility rather than task stage. An evidence disagreement is a conversation requiring disposition, not merely another status light.

```text
SYNTHETIC DEMO / CONVERSATION HANDOFFS / 2026-01-01T09:05Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
PARTIAL inbox: durable unanswered census unavailable.
W 09:04Z: 3 workers, pages 2/2 exhausted. M 09:03Z: 100/cap100.
V 09:04Z. Missing in-scope hosts: none. Oldest observed: DEMO-D1.

WAITING ON human-DEMO-op
  DEMO-D1 / thread DEMO-th1 / w-DEMO-1 asks / age 45m
    Q: Choose schema A or B? Original 08:20Z; ref DEMO-m17.
    Last relevant answer: none observed; seen status unknown.
    Holds DEMO-t1, DEMO-t2; answer needed, resolution unproven.
  DEMO-D2 / thread DEMO-th2 / w-DEMO-3 asks / age 10m
    Q: Retain terminal for inspection or release it?
    Last relevant answer: none observed; ref DEMO-m90.
    Holds DEMO-term3; task impact unknown.

WAITING ON w-DEMO-2
  DEMO-F1 / reviewer-DEMO requests disposition / age 3m
    Review failure before accepting DEMO-t3; release blocked.
    Worker says complete; checks say FAIL at revision DEMO-r7.
    Evidence DEMO-c3; acceptance answer not observed.

CHANGE since successful 09:00Z: DEMO-F1 newly observed.
Unanswered DEMO-D1 persists. Message delivery is not resolution.
FLEET: 3 distinct tasks; 2 decision-blocked, 1 check-blocked.
Liveness and terminal presence are not human response evidence.
Shown 3/3 observed actionable items; render omissions 0.
Unobserved questions unknown. Five-minute view is not urgent alert.
```

**Strengths:** preserves question meaning and prior response context; exposes when ownership is unclear; strong fit when communication volume rather than task topology is the main source of operator overload.

**Tradeoffs:** thread-to-decision and human identity mapping are not established by the supplied message surface. Without durable IDs, the design must label candidate questions and cannot claim a complete inbox. Long exchanges cost lines; quote the exact unresolved question, not a long transcript. No read receipt or acknowledgement is implied.

**State behavior:** empty says no unanswered exchanges observed, never inbox cleared on capped history. Busy mode keeps original questions and shortens prior-answer excerpts first. Stale mode says waiting status unconfirmed, preserving last-known text. Failed checks appear beside the conflicting completion claim and requesting party.

## 9. Concept E: Change Journal

**Organizing principle:** a checkpoint journal. First show the changes since a named successful observation, then a mandatory carried-forward register and current fleet reconciliation. The carried-forward register prevents a delta-only design from losing the oldest unanswered request. This report answers what changed before explaining what is still owed.

```text
SYNTHETIC DEMO / CHANGE JOURNAL / 2026-01-01T09:05Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
PARTIAL decisions. Oldest observed pending: DEMO-D1, 45m.
W 09:04Z: 3 workers, pages 2/2 exhausted. M 09:03Z 100/cap100.
V 09:04Z. Missing: durable census; in-scope hosts none.
Window: last successful comparable observation 09:00Z -> 09:05Z.

NEWLY OBSERVED / not necessarily newly created
  DEMO-F1 FAIL 3m / owner w-DEMO-2 / from reviewer-DEMO
    DEMO-t3 says complete; current DEMO-r7 checks FAIL.
    Review failure; release blocked; ref DEMO-c3.
EXPLICITLY RESOLVED
  None evidenced; absence from capped messages proves nothing.

CARRIED FORWARD / still needs an answer
  DEMO-D1 OPEN 45m / owner human-DEMO-op / from w-DEMO-1
    Choose schema A or B? Original 08:20Z; ref DEMO-m17.
    Blocks DEMO-t1, DEMO-t2. Oldest observed blocking question.
  DEMO-D2 OPEN 10m / owner human-DEMO-op / from w-DEMO-3
    Retain terminal for inspection or release it?
    Holds DEMO-term3; ref DEMO-m90.

NOW: 3 observed tasks; 2 decision-blocked, 1 check-blocked.
No heartbeat changes shown. Execution presence is not readiness.
Shown 3/3 distinct observed actionable items; render omissions 0.
Unobserved questions unknown. Five-minute view is not urgent alert.
```

**Strengths:** helps an operator returning to the same fleet avoid rereading routine activity; makes comparison gaps and recovery visible; clearly separates newly observed facts from ongoing obligations.

**Tradeoffs:** a large change burst can displace old decisions unless space is reserved. The oldest pointer and carried-forward register are mandatory, reducing compression gains. A change window is an observation comparison, not an event-complete timeline.

**State behavior:** first observation has `baseline unavailable` and a full pending register. Healthy mode says no meaningful changes only if comparable sources succeeded. Stale mode states comparison unavailable and retains last-known pending items. Recovery compares with the last successful source observation and names the longer window. Completion-with-failure is a verification change even if the assignment status did not change.

## 10. Recommended default and four operating states

Choose **Decision Brief**. It puts the oldest blocking question in a fixed location, keeps unanswered context across quiet periods, and does not depend on a complete dependency graph or thread history to remain useful. Run Ledger is stronger for reconciliation; Blocker Paths for graph-rich investigations; Conversation Handoffs for dialogue-heavy queues; Change Journal for frequent returning readers. None removes the need for a trustworthy observation contract.

The four independent synthetic state fixtures below are design examples, not a recorded sequence or runtime validation. W, M and V use the definitions from section 4. Screens remain at most 80 ASCII columns. A real missing V integration would read `V unavailable`, not borrow the illustrative check results.

### Empty/healthy observation with incomplete decision coverage

```text
SYNTHETIC DEMO / DECISION BRIEF / 2026-01-01T09:05Z
Scope run-DEMO-EMPTY / host-DEMO-1 / READ ONLY
NO WORK OBSERVED IN SCOPE; decision census unknown.
W 09:04Z: 0 workers, pages 1/1 exhausted; M 09:03Z: 0/cap100.
V not applicable: no observed verification subjects.
Missing: durable decision census. Missing in-scope hosts: none.
ANSWER FIRST: no blocking questions observed; oldest unknown.
FAILURES: none observed. This is not a fleet-wide all-clear.
CHANGE vs successful 09:00Z: no meaningful change observed.
Shown 0/0 observed actionable items; render omissions 0.
Unobserved decisions unknown; no work outside scope assessed.
Five-minute snapshots are not urgent alerts.
```

This is a healthy collection, not proof that no durable request exists. If a future source proves complete fresh decision enumeration, the wording may become `No unresolved decisions in the named scope`; it still must not imply all code is ready or all outside hosts are healthy. Empty collection and source failure have different banners.

### Busy observation

```text
SYNTHETIC DEMO / DECISION BRIEF / 2026-01-01T09:05Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
PARTIAL: oldest blocking decision means oldest observed.
W 09:04Z: 3 workers, pages 2/2 exhausted; M 09:03Z: 100/cap100.
V 09:04Z. Missing: durable census; in-scope hosts none.
ANSWER FIRST
DEMO-D1 OPEN 45m / human-DEMO-op / from w-DEMO-1
  Choose schema A or B? Blocks DEMO-t1, DEMO-t2; ref DEMO-m17.
VERIFY BEFORE ACCEPTING
DEMO-F1 FAIL 3m / w-DEMO-2 / from reviewer-DEMO
  Review DEMO-t3 failed checks; release blocked.
  Complete claim conflicts with DEMO-r7 checks; ref DEMO-c3.
ALSO WAITING
DEMO-D2 OPEN 10m / human-DEMO-op / from w-DEMO-3
  Retain terminal for inspection or release it?
  Holds DEMO-term3; ref DEMO-m90.
CHANGE vs successful 09:00Z: DEMO-F1 newly observed.
FLEET: 3 tasks; 2 decision-blocked; 1 check-blocked.
Shown 3/3 observed actionable items; render omissions 0.
Unobserved questions unknown. Five-minute view is not urgent alert.
```

A busier variant obeys the six-bundle budget: retain the oldest observed blocking question, one verification contradiction, the coverage warning and overflow accounting. The count of rendered items must never be presented as the total pending queue.

### Stale/unavailable observation

```text
SYNTHETIC DEMO / DECISION BRIEF / 2026-01-01T09:20Z
Scope run-DEMO-A / host-DEMO-1 / READ ONLY
UNAVAILABLE: current attention and fleet totals unknown.
W last success 09:04Z; refresh failed; paging current unknown.
M last success 09:03Z; refresh failed; last 100/cap100 partial.
V last success 09:04Z; refresh failed. All evidence STALE.
Missing current: W, M, V, durable census; host status unknown.
LAST KNOWN UNRESOLVED / not confirmed current
DEMO-D1 age 60m / human-DEMO-op / from w-DEMO-1
  Choose schema A or B? Last blocked DEMO-t1 and DEMO-t2.
  Ref DEMO-m17; last observed question state at 09:03Z.
DEMO-F1 age 18m / w-DEMO-2 / from reviewer-DEMO
  Review failed DEMO-r7 checks; last release block DEMO-t3.
  Ref DEMO-c3; last observed result at 09:04Z.
DEMO-D2 age 25m / human-DEMO-op / from w-DEMO-3
  Retain terminal for inspection or release it?
  Last held DEMO-term3; ref DEMO-m90; state at 09:03Z.
CHANGE unavailable; last successful report at 09:05Z retained.
Shown 3/3 last-known items; last-known render omissions 0.
Current item count unknown. No resolution or zero inferred.
Five-minute snapshots are not urgent alerts.
```

Elapsed question age continues from known creation time; the item may already have been answered elsewhere. The text explicitly preserves that uncertainty. If no successful history exists, print `No last-known records available`, not an empty attention list.

### Reported complete, but current checks failing

```text
SYNTHETIC DEMO / DECISION BRIEF / 2026-01-01T09:05Z
Scope run-DEMO-CHECK / host-DEMO-1 / READ ONLY
VERIFY BEFORE ACCEPTING: reported complete is not ready.
W 09:04Z: 1 worker, pages 1/1 exhausted; M 09:03Z: 1/cap100.
V 09:04Z. Missing: durable census; in-scope hosts none.
ANSWER FIRST: no human questions observed; census unknown.
DEMO-F1 FAIL 3m / w-DEMO-2 / from reviewer-DEMO
  Review failing checks before accepting DEMO-t3.
  Assignment: complete claim. Revision: DEMO-r7.
  Check: FAIL at DEMO-r7; release blocked; ref DEMO-c3.
  Terminal exists; process liveness unknown; neither proves ready.
CHANGE vs successful 09:00Z: failing verification newly observed.
Shown 1/1 observed actionable items; render omissions 0.
Unobserved questions unknown. Five-minute view is not urgent alert.
```

A passing check for a different revision changes the check line to `verification unknown: revision mismatch`, not pass. When check provenance is absent, report the claim and unavailable verification without fabricating an actionable failure. Readiness requires an agreed acceptance policy; passing one check alone does not establish it.

## 11. Measurable evaluation and acceptance

These are proposed evaluation tasks and pass criteria. They have not been run. Use only synthetic printed snapshots, with no transcript access, controls or real active-run records. Compare all five concepts using equivalent content, counterbalanced order and the same questions.

### Operator tasks

Recruit five representative operators for an initial design evaluation; this is a small usability sample, not statistical proof of superiority.

| Task | Measured outcome | Proposed acceptance |
|---|---|---|
| E01 Find the oldest observed blocking request in the busy fixture. | Time to correct ID, question, owner and age. | At least 4 of 5 operators identify all four within 20 seconds without transcripts. |
| E02 Explain what a partial report cannot establish. | Correctly distinguish worker paging completeness from decision census completeness. | All 5 reject the claim that no unseen decision exists; at least 4 explain the cap within 30 seconds. |
| E03 Compare completion with verification. | Correct task, revision, failure and proposed disposition. | All 5 reject release-readiness from assignment completion; at least 4 identify the evidence within 30 seconds. |
| E04 Read a failed refresh after a healthy one. | Retention of last-known question and recognition that current count is unknown. | All 5 reject zero pending and fabricated resolutions; at least 4 explain the stale watermark within 30 seconds. |
| E05 Reconcile overlapping blocker groups. | Count union of tasks and identify both separate decisions. | At least 4 compute the distinct task count within 45 seconds; none treats grouped questions as one answer. |
| E06 Handle overflow with an old unchanged blocker. | Find pinned oldest and identify shown, omitted and unobserved quantities. | At least 4 distinguish all quantities within 30 seconds; all reject completeness of omitted content. |
| E07 Read the change journal after recovery. | Identify actual comparison window and newly observed versus newly created. | At least 4 explain both within 30 seconds without inventing an event-complete timeline. |

Any false all-clear in E02-E04 is a design blocker regardless of average speed. Prefer Decision Brief unless another concept improves E01 and E06 without increasing such errors. Record observed task results before claiming an improvement.

### Future contract acceptance cases

Before implementation approval, define fixture-based checks for R01-R16. A future renderer must satisfy these deterministic cases:

- Replaying an identical successful observation produces the same item identities and ordering, with only time-derived labels changing as specified.
- A failed middle page or repeated cursor yields partial worker coverage; it does not delete unseen workers or close questions.
- Duplicate worker records do not inflate counts. Conflicting attempt authority is shown instead of arbitrarily choosing a success.
- A capped response omitting an older question retains that question as last-known unresolved, with current status unknown.
- A successful empty worker response plus failed message response never produces `all clear`.
- Same-task blockers remain separate decisions but contribute one task to the impact union. Cycles produce a conflict label, not infinite expansion.
- A stale check, wrong-revision pass, unavailable check and current-revision failure produce four distinct verification labels.
- Scope changes, unknown timestamps and clock conflicts disable unsupported ages/deltas instead of generating negative ages or invented trends.
- Seven observed actionable bundles under a six-bundle budget account for one omitted bundle, retain the oldest and verification contradiction, and leave unobserved totals unknown.
- Every fenced screen contains only printable ASCII and line breaks, stays within 80 columns and includes coverage plus omission accounting. No question is cut between its identity and required context.
- A collection interruption cannot advance a source's last-success pointer. A rendering interruption cannot publish a half report as a successful snapshot.
- A transcript containing ANSI sequences, fences, secrets or report-policy instructions cannot break the report or change its rules.

No tests, collector calls, performance measurements or operator trials were performed for this design artifact.

## 12. Risks, limits and feasibility gates

### Risks and mitigations

| Risk | Consequence | Required mitigation |
|---|---|---|
| Capped messages mistaken for a durable queue | Oldest unanswered decision silently disappears. | Carry last-known unresolved items; label oldest observed and census unknown; gate complete-queue claims. |
| Pagination races or cross-source skew | Duplicated work, missed records or misleading readiness. | Deduplicate by identity, show collection intervals and evidence revisions; require documented source consistency before census claims. |
| Source failure presented as empty | False all-clear when observation is most needed. | Preserve last-success baseline; make current totals unknown; distinguish empty success from failure. |
| Root grouping hides separate questions | One answer appears to release unrelated work. | Stable question IDs, explicit edges, union task counts and visible overlap labels. |
| Incorrect authority or identity mapping | Old attempt claims override current failure. | Keep attempts separate, expose authority conflicts and retain provenance. |
| Evidence drift | A pass on an old revision becomes a readiness claim. | Match subject, current revision, evidence kind and policy; mark stale or mismatched evidence unknown. |
| Static overflow | Decisions exist but cannot be explained in one chat screen. | Deterministic omission accounting, oldest pin and first omitted reference; no promise of nonexistent drill-down. |
| Repeated posts cause fatigue | Operator stops reading even useful reports. | Stable placement, suppress heartbeat deltas, keep unresolved context concise; assess E01/E06 before expanding density. |
| Untrusted or sensitive transcript text | Prompt injection, misleading text or secret leakage into chat. | Deterministic field rendering, escaping, bounded excerpts and redaction; evidence access follows source permissions. |
| Long outage or missing history | Last-known unresolved set grows or ages without confirmation. | Separate confirmed-current from unconfirmed history; never silently evict pending items to imply resolution. Capacity/retention policy is a gate. |

### Explicit limits and out of scope

- This deliverable is a design specification, not product code, an implementation plan, a scheduler, a running observer or an integration benchmark.
- No source is consumed or acknowledged. No seen/claimed/snoozed/resolved state is stored for a person. No retries, dispatches, releases, terminal attachments, messages or other controls are provided.
- Five-minute posting cannot guarantee urgent delivery or record every transition. Event replay, if available later, would require separate verification.
- No API endpoint, durable decision store, overflow archive, independent check feed, expected-host inventory or reliable human-identity service is assumed to exist.
- No dependency impact is claimed complete without graph completeness. Unknown owner, age, host, revision or process state remains unknown.
- No cost, token, throughput, trend, utilization, percentage or latency statistic is inferred from process time or message volume. Future statistics require authoritative records, explicit window, numerator/denominator and missing-data policy.
- The design does not select a terminal framework, fork, interactive terminal concept, infrastructure topology, storage engine or deployment procedure. Those are separate decisions.
- Evidence references need not be clickable, but must be meaningful to the operator. This design cannot make unavailable records inspectable merely by naming them.

### Open questions and feasibility gates

| Gate | Question and evidence needed | If unresolved |
|---|---|---|
| G01 Durable decisions | Which non-consuming source enumerates unresolved questions with stable identity, original time, actor and explicit resolution linkage? | Ship only an observed-attention design; never promise the global oldest or every pending decision. This is the central feasibility gate. |
| G02 Enumeration consistency | Do opaque worker cursors enumerate a stable version? What happens during insertions, supersession and cursor expiration? | Report exhausted paging as an observation property, not an exact point-in-time census. |
| G03 Independent verification | Which source binds acceptance evidence to task, authoritative attempt and current revision, and what freshness/acceptance policy applies? | Show completion claims and verification unavailable; do not invent check results or ready totals. |
| G04 Scope and host inventory | Who defines intended hosts/runs, and can missing hosts be distinguished from intentionally excluded ones? | Show local/named scope and unknown wider coverage; no fleet-wide health statement. |
| G05 Ownership and resolution | Which identities distinguish requester, acting owner, answerer and resolver? How are cancellations and superseded questions represented? | Use explicit unknowns and preserve separate communication states. |
| G06 Overflow destination | Can the operator access a complete read-only pending list through an existing verified surface? If not, is a bounded supplementary paste acceptable? | Keep omissions explicit; the single report cannot satisfy full explanation of all overflow items. Do not invent a link. |
| G07 Freshness and retention | What per-source age/skew limits and unresolved-history retention budget are acceptable? Can the observer retain a last-success checkpoint without touching source state? | Keep conservative stale labels; do not claim reliable long-term carry-forward or trends. |
| G08 Density decision | Does the operator evaluation favor the brief, ledger, dependency, conversation or journal model under realistic queue sizes? | Retain Decision Brief as the provisional default, not a validated winner. |

**Decision for the next design review:** evaluate Decision Brief with the synthetic tasks, while verifying G01 before promising complete attention coverage. Improve layout only after the observation semantics are honest; a prettier incomplete census still loses decisions.
