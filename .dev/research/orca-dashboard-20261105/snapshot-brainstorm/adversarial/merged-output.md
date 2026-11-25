<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (haiku:backend) -->
<!-- Merge date: 2026-11-05 -->

# Orca Fleet Snapshot: Five Report Concepts (merged design)

## 1. Purpose, evidence boundary and concept set
<!-- Source: Base (original, modified) — concept names and fixture paragraph replaced per Changes 1, 4-9 -->

Design variant for operator review. Design only; no implementation or runtime validation.

The operator must find the oldest observed blocking decision, understand what answer is needed, and see the limits of the observation without opening every transcript. The snapshot is a complete, standalone chat message intended for a five-minute cadence. It is not a live console, command surface, acknowledgement mechanism or urgent-alert guarantee.

**Complete five-concept set:** A. Attention Brief (default); B. Ball-Holder Board; C. Root-Blocker Tree; D. Conversation Ledger; E. Delta Journal. A is ranked by age and need, B by responsibility (who holds the next move), C by causal structure, D by conversation, E by time. Each organizes the entire report on its own axis. They share one frame (section 6), one data contract (section 4) and one set of integrity rules (section 5), not a common dashboard with interchangeable widgets.

Evidence is limited to the supplied seed and the research report's sections 1-5. Those sources establish structured worker observations and opaque paging, capped non-consuming message reads, and the distinction between assignment outcome, terminal existence, process liveness and independently verified readiness. They do not establish a complete durable decision source, snapshot isolation across sources, or an independent verification feed. Every contract below is a proposed design requirement unless explicitly identified as a source limitation.

All fenced screens are **synthetic examples**, including every identifier, timestamp, count and evidence reference. Every screen draws on the one shared fixture in section 7. Their declared maximum width is **78 content columns in an 80-column budget** (section 16). `DEMO` evidence labels are illustrative references, not working links or existing records. No cost, token, utilization or success-rate estimates are presented.

## 2. Layer model
<!-- Source: Variant 1 (opus:architect), s.2 Architectural Model — merged per Change 1 -->

This is a logical design, not an implementation plan. It names boundaries so that the honesty rules live in exactly one layer and the five concepts stay swappable. The layer model does not hide integrity fields from the renderer: the data contract (section 4) and integrity rules (section 5) stay separate sections, and every field they require reaches layer 4.

```
  sources (read-only)          layer 1            layer 2          layer 3
 +--------------------+    +-------------+    +-------------+   +-----------+
 | worker-list (paged)|--->|  collector  |--->| observation |-->| derivation|
 | check --peek (cap) |--->|  adapters   |    |    store    |   |  (report  |
 | inbox (no cursor)  |--->| one per src |    | last-good + |   |   model)  |
 | worktree ps (hosts)|--->|             |    | gap records |   +-----+-----+
 +--------------------+    +-------------+    +-------------+         |
                                                                       v
                                       +---------------------------------+
                                       | layer 4: frame + concept render |
                                       | A brief | B ball-holder         |
                                       | C tree | D ledger | E journal   |
                                       +---------------------------------+
```

| Layer | Owns | Must never |
|---|---|---|
| 1. Collector adapters | One adapter per source. Records what was asked, what came back, page/cap status, errors and the collection time. | Consume, acknowledge or deliver a coordinator message. Turn an error into an empty result. |
| 2. Observation store | Last successful observation per source; an explicit gap record for each failed or partial collection. | Overwrite last-good data with a failed collection, or store a failure as zero. |
| 3. Derivation | Builds the report model: attention items with stable keys, root-blocker groups, deltas against the last successful observation, coverage and omission totals. | Invent a value a source did not supply; sum overlapping dependents; compute a percentage without a known denominator. |
| 4. Frame + renderer | Pure function from report model to ASCII text. The frame (header, coverage, footer) is shared; the body is concept-specific. | Read sources directly, hide coverage gaps, or drop an item without counting it as omitted. |

**Report model (logical fields, proposed):**

- `frame`: report sequence number, as-of time, previous successful as-of, scope (runs, hosts), per-source status (`ok`, `partial`, `capped`, `failed`, `stale since T`), paging coverage, decision census status, observed and omitted totals.
- `attention_items[]`: stable key, kind (`decision`, `unclassified`, `failure`, `verify-gap`, `resource`, `unassigned-ready`), question or reason, requester, acting owner, original age with its basis, impact (direct/indirect dependents as distinct sets), evidence references, source and freshness, first-seen and last-changed observation.
- `groups[]`: root blocker to distinct dependent task keys, with a `shared-with` list for tasks under more than one root.
- `threads[]`: thread key, original question text, last message summary, delivery ladder state per field (enqueued/delivered/processed/answered/resolved, each `y`/`n`/`?`).
- `deltas[]`: newly observed, escalated, aged-past-threshold, resolved, vanished-without-resolution, all relative to the previous successful comparable observation only (section 5, rules 4-5).
- `fleet`: liveness counts deduplicated by authoritative identity with an explicit `?` bucket; outcome counts kept separate from liveness.

**Why this shape is the maintainable choice:**

1. **Honesty is centralized.** Coverage, staleness and unknown handling live in layers 2-3 and the shared frame. A new renderer cannot accidentally print an all-clear because it never decides coverage, and the integrity fields stay visible to it.
2. **The default is reversible.** Switching from concept A to E is a renderer swap, not a data change. Evaluation (section 17) can render all five from the one shared fixture (section 7).
3. **Source churn is contained.** If a complete decision source is found later (gate FG-1, section 20), only one collector adapter changes; the `>= N observed` labels flip to exact counts without renderer edits.
4. **Rendering is testable as golden text.** A pure model-to-text function suits fixture-based snapshot tests and a 78-column width assertion. This is a property of the proposed design, not a test that exists.
5. **Interactive reuse.** The later interactive-terminal brainstorm can reuse layers 1-3 unchanged and replace only layer 4.

## 3. Requirements
<!-- Source: Variant 1 (opus:architect), s.3.1-3.7 with Variant 2 (sonnet:analyzer) s.3 Basis column — merged per Change 2 -->

All requirements are proposed product requirements, not claims about existing Orca fields or behavior. "Must" applies to every concept unless a concept section says otherwise. **Layer** names where the requirement is enforced in the section 2 model. **Basis** cites the seed brief (SB), a research report section (RP n) or marks the requirement as proposed ([P]), and lists the earlier requirement IDs it absorbs (Base R01-R16; Variant 2 R-xxx). **Acceptance condition** is what a reader or a mechanical check can observe in one rendered report. Every Base requirement R01-R16 maps to at least one row below.

| ID | Requirement | Layer | Basis | Acceptance condition |
|---|---|---|---|---|
| DEC-1 | Pending human decisions, including `unclassified` items (COM-7), come before any other body content. | 4 | SB attention first; R01; R-DEC-01 | Nothing but the frame header precedes the decision block. No VERIFY, failure, change or fleet row sits above it. |
| DEC-2 | Each decision row carries stable key, the question in its original wording (truncated with a marker, never paraphrased only), requester, acting owner, original age, impact and at least one evidence reference. | 3, 4 | SB constraints; R03; R-DEC-03; R-COM-01 | Missing fields read `?`/`unknown`; continuation lines belong to the same item; no question is shortened into an ambiguous instruction. |
| DEC-3 | The oldest observed blocking decision is findable without scanning: every concept, the default included, prints the fixed `OLDEST observed` frame line (section 6). | 3, frame | RP 3, SB success; R01; R-DEC-02 | Line 7 of every screen is the OLDEST line. It reads `OLDEST observed` while the decision census is unknown (section 4, census and the oldest claim). |
| DEC-4 | Decision counts read `N` only when the decision source is complete; otherwise `>=N observed`. | 3 | RP 2, RP 4; R09; R-DEC-04 | No bare decision count appears while the census is unknown. |
| DEC-5 | Age is from the original creation time when the source gives it; otherwise from first observation, labelled `seen>=`. Future times read `clock conflict`. | 3 | RP 3; R14 | Ages never reset on repetition; every age without a creation time carries `seen>=`. |
| DEC-6 | A decision stays listed until an explicit resolution or authoritative disposition is observed. A reply, read flag, snooze or vanished message is not resolution. | 3 | SB; RP 3, RP 5; R02; R-DEC-05; R-COM-02 | An unchanged question remains visible or explicitly counted in overflow across reports until resolution or disposition. |
| DEC-7 | Unknown-age, `seen>=` and `clock conflict` items print above known-age items in the decision block, each with its age qualifier. | 3, 4 | [P]; INV-007 | In a block holding both, every qualified-age row precedes every known-age row. |
| BLK-1 | Failed authoritative attempts without an accepted replacement or disposition are attention items. | 3 | RP 3; R04; R-BLK-04 | Listed after the decision block; an unavailable source is never shown as a failed worker. |
| BLK-2 | Blocked work is grouped under its root blocker, but each distinct decision stays its own row. | 3 | SB constraints; R12; R-BLK-01; R-BLK-03 | Two questions blocking one task keep separate IDs. |
| BLK-3 | Impact counts distinct task keys, direct and indirect apart. A task under two roots counts once in the total and is marked `shared`/`also under` at each root. | 3 | RP 3 metrics; R12; R-BLK-02 | Impact totals equal the size of the union of task IDs. |
| BLK-4 | Unknown outcomes are a separate bucket from failures and successes. | 3 | RP 3; R04; R-BLK-04 | `?` outcomes are counted apart. |
| BLK-5 | Repeated reports of one blocker collapse into one item with an affected-worker count. | 3 | [P] | One incident across N workers renders as one row. |
| BLK-6 | Work identities (run/task/attempt) and execution identities (host/workspace/session) stay separate; superseded attempts never override the current authoritative attempt. | 3 | RP 3; R13; R-BLK-05 | Links between them are explicit; workspace parentage never renders as a dependency. |
| COM-1 | Communication context is kept: thread or source reference, last relevant answer if observed, unresolved status. | 3, 4 | RP 3; R05; R-COM-01 | Every unresolved thread shows its original question beside any summary. |
| COM-2 | Delivery state is separate facts (enqueued, delivered, coordinator-processed, answered, resolved), each `y`, `n` or `?`. | 3 | RP 3; R05; R-COM-03 | No single flag stands for more than one of these facts. |
| COM-3 | Unanswered context persists across reports, not only when it changes. | 3 | SB; R02; R-COM-02 | An unchanged open thread appears in consecutive reports. |
| COM-4 | Only a message that matches an explicit routine form (COM-7) is a heartbeat; heartbeats never become rows and update a last-seen time only. | 3 | SB; R06; R-COM-04 | No row is a heartbeat; no unmatched message is silently dropped. |
| COM-5 | Message reads are non-consuming. If the only available read would consume or acknowledge, the source is `unavailable (would consume)`. | 1 | RP 2, RP 3; R10; R-COM-05 | No report causes consumption, acknowledgement or delivery. |
| COM-6 | Source text is untrusted: quoted, truncated with a marker, control characters and fences escaped, secrets redacted and marked; it cannot change report policy. | 4 | RP 3; R16; R-COM-05 | Redaction is marked `[redacted]`; question meaning is preserved or the row says it may not be (INV-023, section 20). |
| COM-7 | A message that matches no explicit routine form and no decision form is `unclassified`: it is shown in the decision block, ranked, and eligible for OLDEST (section 4). | 3 | [P]; INV-005 | The `attn` header line counts unclassified items; each one is a row, never a heartbeat. |
| CHG-1 | Deltas compare only against the last successful comparable observation of the same source and scope. | 2, 3 | SB; R06; R-CHG-01 | The window line names the baseline time. |
| CHG-2 | A failed or partial collection never supplies a zero baseline or a negative delta; deltas for that source print `n/a (no baseline)`. | 2, 3 | SB, RP 3; R09; R-CHG-02 | Partial reads produce only `newly observed` additions (rule 4). |
| CHG-3 | Change kinds are: newly observed, escalated, crossed-age-threshold, resolved (with evidence), vanished-without-resolution (after a full read only, rule 4). | 3 | [P]; R06; R-CHG-03 | Resolved needs explicit evidence; VANISHED never reads as resolved. |
| CHG-4 | Liveness flaps and heartbeats are not deltas. | 3 | SB; R06 | No heartbeat appears in a change section. |
| CHG-5 | Each report states the window it compares; missed collections and the gap length are called out. | frame | RP 3, RP 4; R-CHG-04 | Transitions inside a gap are declared unobserved. |
| CHG-6 | Trends, rates and response times appear only with a source, window and sample size. | 3 | SB, RP 3; R-CHG-05 | Otherwise omitted. |
| VER-1 | Assignment completion, terminal existence, process liveness and independent verification are four separate fields. | 3 | SB, RP 3; R07; R-FLT-04 | None implies another on any screen. |
| VER-2 | Evidence is labelled by kind: `[claim]`, `[settled]`, `[artifact]`, `[checks@rev]`, `[review]`, `[human]`. No confidence percentage. | 3, 4 | RP 3; R14; R-VER-05 | Every verification statement carries a kind label. |
| VER-3 | Reported complete with failing current-revision checks is a `verify-gap` attention item, never done/green; checks for another revision read `verification unknown: revision mismatch`. | 3 | SB success, RP 3, RP 4; R07; R-VER-02; R-VER-03 | Listed after the decision block and before fleet context. |
| VER-4 | Reported complete with no verification evidence renders `complete (claim only)`. | 4 | RP 3; R07; R-VER-01; R-VER-04 | Counted as unverified, apart from failing. |
| VER-5 | A completed task that still owns a live terminal or resource is a resource item, not a liveness problem. | 3 | RP 3; R13 | Rendered under resources. |
| COV-1 | Every report prints, in the header: sequence number, as-of, previous successful as-of, scope, per-source status, freshness and paging, decision census status, shown/observed counts and omitted bundles. The footer repeats the coverage line and ends with the end marker. | frame | SB, RP 2, RP 3; R08; R-FLT-02; R-FLT-03 | A paste cut anywhere after line 7 still carries every qualifier (section 6). |
| COV-2 | Uncovered hosts are never treated as empty. Without an expected-host inventory the host field reads `N covered of ? expected`; no percentage, and never "missing hosts: none". | 3, frame | RP 2, RP 3; R08; R-FLT-01 | No host-coverage percentage or "none missing" text appears. |
| COV-3 | If a source relevant to a section is failed, capped or stale, that section header carries the marker, and an empty section reads `0 observed (partial)`, never `none`. | 3, 4 | SB; R09; R-INT-02 | Unknown never renders as zero, blank or green. |
| COV-4 | No concept, in any state, prints a fleet-wide all-clear or an equivalent green summary. The empty state reads `no attention items observed in <scope>` followed by the coverage and census qualifiers. | frame | SB; INV-006; replaces Variant 1 COV-4 and Variant 2 R-INT-01 | MC-4 (section 17) finds no all-clear wording on any screen. |
| COV-5 | Unknown prints as `?` and is never summed, averaged or rendered as zero. | 3, 4 | SB; R09; R-INT-02 | No `?` value contributes to a total. |
| COV-6 | Cost, token, trend and percentage figures appear only with a reliable source and a printed denominator. | 3 | SB; R-INT-03 | The default renderer has no cost or token line. |
| COV-7 | Derived facts carry provenance: age basis, evidence revision, count scope and observation times. | 3 | RP 3; R14 | Unsupported measures are omitted. |
| COV-8 | Each gap names what was not observed and which claims it prevents, without inventing controls or drill-downs. | 3, 4 | RP 3; R15; R-OVF-01 | No link, command or drill-down is suggested that is not verified to exist. |
| COV-9 | Liveness, process existence, outcome and verification counts go after all attention content; unknown counts print `?`. | 3, 4 | RP 3; R-FLT-04; R-FLT-05 | Fleet context is the last body section. |
| FMT-1 | One plain-ASCII fenced block; no ANSI, emoji, box-drawing Unicode, tabs, colour or font dependence. | 4 | SB; R11; R-FMT-01; R-FMT-02 | Optional colour export carries no meaning the plain text lacks. |
| FMT-2 | Width: at most 78 content columns in an 80-column budget (2-column wrap margin). | 4 | SB; R11; R-FMT-01; INV-012 | No fenced line exceeds 78 characters. |
| FMT-3 | Line budget: at most 60 lines per report, frame included. Only the oldest complete question may push past it, and the report then says so (section 16). | 4 | [P]; R11; R-FMT-03; INV-010 | Fenced line count is at most 60, or the footer prints `over budget: oldest question kept whole`. |
| FMT-4 | Row order and column positions are deterministic for the same model; sort keys are documented per concept. | 3, 4 | RP 5; R-FMT-04 | Two reports of an unchanged model are byte-identical except time fields. |
| FMT-5 | The report is read-only: no writes, acknowledgements, claims, retries, releases or scheduling; next actions are text only. | all | RP 2; R10 | No row implies a control was used. |
| FMT-6 | The report states that it is a five-minute sample and not an urgent-alert channel. | frame | SB | Line 2 carries `(sample, not an alert)`. |
| FMT-7 | A paste without its `=== END SNAPSHOT seq N ===` line is invalid and incomplete. | frame | [P]; INV-010; INV-028 | The end marker's sequence equals the title's sequence. |
| FMT-8 | Every concept keeps the fixed `attn` header line of attention counts so that its organizing principle cannot push them out of view. | frame | [P]; R-INT-05 | Line 6 of every screen is the `attn` line. |
| OVF-1 | When items exceed a section's budget, the report prints `shown + omitted = observed` in whole bundles, lists omitted IDs in sort order up to one line, and implies no drill-down. | 3, 4 | SB open questions; R-OVF-01 | The arithmetic can be checked by eye (section 16). |
| SYN-1 | Every mockup uses synthetic DEMO-marked identifiers from the shared fixture; no real run record is reused. | all | SB; R-INT-04 | Every ID on every screen appears in section 7. |

R01-R16 mapping summary: R01 to DEC-1, DEC-3; R02 to DEC-6, COM-3; R03 to DEC-2; R04 to BLK-1, BLK-4; R05 to COM-1, COM-2; R06 to CHG-1, CHG-3, CHG-4, COM-4; R07 to VER-1, VER-3, VER-4; R08 to COV-1, COV-2; R09 to DEC-4, CHG-2, COV-3, COV-5; R10 to COM-5, FMT-5; R11 to FMT-1, FMT-2, FMT-3; R12 to BLK-2, BLK-3; R13 to BLK-6, VER-5; R14 to DEC-5, VER-2, COV-7; R15 to COV-8; R16 to COM-6.

## 4. Observation and data contract
<!-- Source: Base (original, modified) — V3 s.3 kept verbatim; classification rule added per Change 12 (invariant INV-005) and census/oldest rule added per Change 16 (invariant INV-026) -->

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

### Message classification and the visible fallback

Every observed message falls into exactly one class:

| Class | How a message enters it | What the report does with it |
|---|---|---|
| decision | Matches an explicit decision form (a question record, or a message linked to one) | A decision row in the decision block (DEC-1, DEC-2) |
| routine | Positively matches an explicit, listed routine form (for example a heartbeat or a progress tick in a fixed format) | Updates the sender's last-seen time only; never a row (COM-4) |
| unclassified | Matches neither list, or the match is ambiguous | A row in the decision block marked `unclassified`, owner `?`, ranked by age like a decision and eligible for the OLDEST line (COM-7) |

The routine list is closed: a message becomes a heartbeat only by matching it. Silence of the classifier, a partial match or a classifier error yields `unclassified`, never routine. This trades noise for safety: a misclassified decision is visible as an extra row, never hidden as a heartbeat. The evidence that the routine forms are complete and stable is an open gate (FG-9, section 20).

### Census and the oldest claim

Because the non-consuming message read is capped with no paging or cursor (above), the true oldest decision can sit outside the read window on every run. Therefore:

- While the decision census is `unknown`, the frame line reads `OLDEST observed`, never `OLDEST`, and no screen states that an item is the oldest decision without that qualifier.
- `unclassified` items are ranked with decisions and can hold the OLDEST line.
- Unknown-age, `seen>=` and `clock conflict` items print above known-age items in the decision block with their qualifier (DEC-7), because each could be older than the oldest known-age item. The OLDEST line still names the oldest known-age observed item, and the decision block prints the rule 1 warning `oldest not certified: N item(s) lack a creation time` under the qualified-age items.
- Dropping the `observed` qualifier requires paging or a cursor over the decision source and a complete census (gate FG-10, section 20).

### Source capabilities and safe failure

Worker paging uses the source's opaque continuation tokens unchanged. Completion means a successful terminal page, not merely receiving fewer rows than requested. Repeated tokens, invalid tokens, page errors or a collection deadline produce partial coverage. Deduplicate repeated records by authoritative identity; conflicting versions remain conflict-marked unless source ordering resolves them. Cursor exhaustion alone does not prove a point-in-time census if records can move between pages.

Non-consuming message observation is capped at 100 with no advertised paging in the supplied evidence. Even fewer than 100 returned messages do not prove complete unresolved history. Show the returned count, cap and `decision census unknown`; do not infer another observer API exists. Inventory coverage, worker coverage and decision coverage must therefore be separate fields.

No cross-source transaction is established. Render from one immutable collection bundle with each source's interval and revision provenance. If outcomes and evidence conflict, show both; never manufacture a globally consistent ready state. Proposed future observer storage would commit an observation and its comparison pointer together, but no database or storage implementation is selected here.

## 5. Integrity rules
<!-- Source: Base (original, modified) — V3 s.4 rules 1-10 kept; rule 2 modified per Change 16 and DEC-1, rule 7 per Change 14, rule 8 per Change 15; closing fixture paragraph replaced by section 7 -->

1. **Age never resets on repetition.** Prefer original question creation time. Otherwise print `observed >=Nm` from first observation (notation `seen>=Nm`, section 6), not a fabricated creation age. Unknown-age blocking questions get a separate visible warning because the oldest cannot be certified. Future timestamps produce `clock conflict`, never negative waiting time. Last-known unresolved items can age by elapsed wall time while their unresolved status remains explicitly unconfirmed.
2. **Use stable ordering.** Coverage failure that limits interpretation is surfaced in the frame header, never as a body row above decisions. Body order follows DEC-1: the decision block first (decisions and `unclassified` items), then actionable failures, verification contradictions and resource questions. Within the decision block, unknown-age, `seen>=` and `clock conflict` items print first with their qualifier (DEC-7); then pin the oldest known-age observed blocking decision, then other blocking decisions by original age. Break ties by stable ID. Also pin one verification contradiction, if present, at the top of the section after the decision block. Urgency escalation may precede the pinned item only when backed by explicit source severity; retain an `oldest observed` pointer in the frame OLDEST line.
3. **Carry unresolved context forward.** A question disappearing from a capped or failed read stays `last known unresolved; current status unknown`. Explicitly linked resolution or authoritative disposition is needed to close it. Cancellation or scope exit is a disposition, not a successful answer. A reply alone does not close it.
4. **Compare like with like.** Maintain a last-success pointer per source and scope, not a single global success flag. A failed refresh never replaces it. Compare only compatible scope/schema/revision identities; otherwise print `baseline unavailable` or `scope changed`. Partial observations can establish positive additions, but not absence, resolution or negative movement. A resolved delta needs explicit evidence even after recovery.
5. **Call changes observations.** `Newly observed` is not necessarily newly created. Five-minute sampling cannot prove all intervening events. A recovery delta states its actual comparison interval and missed collections, not `last five minutes` automatically. No baseline means no trend.
6. **Count sets, not rows.** Decision counts use distinct question IDs; impacted-work counts use distinct unfinished task IDs. A task blocked by two questions contributes once to fleet impact and appears under both questions with an overlap note. Unknown graph completeness produces `at least N observed affected tasks`. Attempts and resource rows never inflate task totals.
7. **Bound collection independently from display.** A future collector needs a fixed read budget and deadline; stopping early marks partial coverage. Output uses a hard budget of 60 lines per report, frame included, at no more than 78 content columns (section 16). The budget yields only to preserving the oldest complete question and its warning; the report then prints `over budget: oldest question kept whole`. If overflow is otherwise unavoidable, omit whole lower-priority bundles and report it. No performance benchmark is claimed.
8. **Budget honestly.** The header `cover` line distinguishes `observed` actionable items, `shown`, `omitted` whole bundles and the unobserved unknown (`census unknown`); the footer repeats that line before the end marker. Reserve room for oldest decision, verification contradiction, coverage and their evidence. Overflow selection is deterministic and never rotates the oldest away. Omitted items remain in the next observation's unresolved set; omission does not resolve them.
9. **Do not promise an archive.** If omitted stable IDs fit, list them in priority order; otherwise show count and the first omitted ID with its age. This exposes the limitation without pretending all omitted questions are accessible from chat. A complete overflow destination is a feasibility gate, not an invented link. Severe overflow invalidates the claim that the report alone explains every decision.
10. **Render safely.** ASCII escaping and line wrapping preserve content; no ANSI, tabs, control sequences or unescaped code fences. Stable references are not executable instructions. Redact secrets before chat delivery and mark redaction; do not expose credentials through evidence excerpts.

The synthetic screens draw every identifier, time and count from the shared fixture in section 7. Source tokens in the `src` frame line give each source's last successful observation. The verification contribution is only a mock capability; its real integration remains a gate (FG-2). Host inventory covers only host-DEMO-1; other hosts are outside this named scope, not asserted empty.

## 6. Frame contract
<!-- Source: Variant 1 (opus:architect), s.4.1-4.4 Shared Report Frame Contract — merged per Change 3, with header qualifiers per Change 15 and OLDEST wording per Change 16 -->

Every concept renders the same header and footer. Only the body between them differs. Coverage, freshness, census, omission and the oldest observed decision are always in the same place, whichever concept is chosen. The qualifiers sit in the header so that a split, truncated or stale paste that loses its footer still carries them; the footer repeats the coverage line and closes with an end marker.

### 6.1 Frame header and footer (all concepts)

```
=== ORCA SNAPSHOT [A:BRIEF] seq 0412 ================= SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
   ... concept-specific body, decision block first (DEC-1) ...
------------------------------------------------------------------------------
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0412 ===
```

The frame costs 12 lines; the body therefore has at most 48 of the 60-line budget (section 16).

### 6.2 Frame fields

| Line | Content | Requirement |
|---|---|---|
| 1 Title | Concept code, report sequence number `seq N`, `SYNTHETIC DEMO DATA` marker in mockups only. The sequence number and as-of time identify the paste, so an older paste is recognizable. | FMT-1, FMT-7 |
| 2 `as-of` | Current collection time, previous successful time, window, sample disclaimer. | COV-1, CHG-5, FMT-6 |
| 3 `scope` | Runs in scope; hosts covered of expected (`?` when inventory unknown). Never `missing hosts: none`. | COV-2 |
| 4 `src` | One token per source: `ok`, `CAPPED n/cap`, `no-paging`, `PARTIAL`, `FAILED`, `STALE since T`, `unavailable (would consume)`. Paging as `pages read/pages known pg` or `more?`. | COV-1, COV-3 |
| 5 `cover` | `observed N (census unknown)` (never a total while the census is unknown), `shown`, `omitted` in whole bundles. | COV-1, OVF-1, rule 8 |
| 6 `attn` | Fixed attention counts: decisions (`>=N` while census unknown), unclassified, answered-open, failing, unverified. | FMT-8, DEC-4 |
| 7 `OLDEST` | `OLDEST observed` key, age with its qualifier, quoted question (truncated with `...`). Reads `OLDEST observed none in <scope> (census unknown)` when no decision is observed. The `observed` qualifier is dropped only under gate FG-10. | DEC-3, Change 16 |
| footer `cover` | Repeats line 5 exactly. | COV-1 |
| footer `legend` | Fixed glossary for `?`, `>=N`, `seen>=N`, `~`. | COV-5, DEC-4, DEC-5 |
| footer end marker | `=== END SNAPSHOT seq N ===`, same N as the title. A paste without it is invalid. | FMT-7 |

### 6.3 Shared notation

| Token | Meaning |
|---|---|
| `?` | Unknown. Never zero, never `none`, never healthy. |
| `>=5` | At least 5 observed; the source is capped or partial. |
| `seen>=12m` | Original creation time unavailable; age counted from first observation. |
| `~` | Last-known value from an earlier successful collection, not confirmed current. |
| `[claim]`, `[settled]`, `[artifact]`, `[checks@rev]`, `[review]`, `[human]` | Evidence kind (VER-2). |
| `ev:` | Evidence reference: a source plus a stable record reference (message, page, check run). |
| `STALE` | Data is last-good from an earlier collection; age printed. |
| `n/a` | Not applicable or no baseline (deltas after a failed collection). |
| `a > b` | Requester `a`, acting owner `b`. The owner is never the coordinator relay; a missing owner prints `?`. |

### 6.4 Stable identity rule

Row keys come from source-native identifiers (decision record, thread, task, attempt) when the source provides them. When a source provides none, the derivation layer prints the composite source reference (`run/task/attempt + message ref`) and tags it `id:derived`. A derived key is not promised to survive across reports; the tag tells the reader that cross-report comparison of that row is best effort. Display keys may be shortened, but the shortening must be deterministic and collision-checked within a report.

## 7. Shared fixture
<!-- Source: Variant 2 (sonnet:analyzer), s.2.6 Synthetic fixture world — merged per Change 9 -->

One invented world keeps the five screens comparable. All values are fake, and every identifier carries `DEMO`. The busy screens in sections 8-12 are the same report (seq 0412) rendered five ways. The state screens in sections 15-16 vary this world as stated beside each screen. Ages are measured at 09:05Z.

| Item | Fixture |
|---|---|
| Report | seq 0412 at 2026-01-01T09:05Z; previous successful report seq 0411 at 09:00Z; window 5m |
| Scope | run-DEMO-A (tasks T-DEMO-02 to T-DEMO-07), run-DEMO-B (tasks T-DEMO-08 to T-DEMO-11); host-DEMO-1 covered; expected-host inventory unknown |
| Sources | workers ok, 3 of 3 pages (terminal page reached); messages CAPPED 100 of 100, no paging, decision census unknown; checks last ok 09:02Z |
| People and relay | operator human-DEMO-op; coordinator relay coord-DEMO (never an acting owner) |
| Q-DEMO-01 (oldest observed) | w-DEMO-07 > human-DEMO-op, on T-DEMO-04, created 06:51Z (2h14m). "Approve schema change for T-DEMO-04?" Blocks T-DEMO-04 directly; T-DEMO-05, 06, 07 indirectly. ev M-DEMO-118, thread TH-DEMO-11 |
| Q-DEMO-02 | w-DEMO-03 > human-DEMO-op, on T-DEMO-06, created 08:20Z (45m). "Target API v2 or v3 for T-DEMO-06?" Blocks T-DEMO-06, which is shared with Q-DEMO-01. ev M-DEMO-131, thread TH-DEMO-19 |
| Q-DEMO-03 | w-DEMO-11 > `?` (coord-DEMO relayed it; no acting owner recorded), on T-DEMO-09, created 08:58Z (7m). "Retain or release worktree wt-DEMO-9?" No task link seen, impact `?`. ev M-DEMO-137, thread TH-DEMO-22. First observed at 09:05Z |
| Q-DEMO-04 (answered, not resolved) | w-DEMO-02 > human-DEMO-op, on T-DEMO-08, asked 07:30Z (1h35m); human reply 08:55Z "Use the staging bucket."; no resolution linkage. ev M-DEMO-122, thread TH-DEMO-14 |
| M-DEMO-140 (unclassified) | from w-DEMO-04 on T-DEMO-11; no creation time; first observed 08:33Z (`seen>=32m`). "Lockfile drift vs main, holding here." Matches neither a decision form nor a routine form. Owner `?`. T-DEMO-11 ready: `?`. No thread |
| A-DEMO-12 (failure) | w-DEMO-12, attempt A-DEMO-12 on T-DEMO-10 failed 08:41Z (24m); no replacement attempt seen. ev worker-list page 2 |
| T-DEMO-03 (complete, checks failing) | w-DEMO-05 reported done 08:40Z `[claim]`; checks on revision demo-b7 at 09:02Z: 2 failed of 14 ran (lint-DEMO, unit-DEMO-3); structured source field nextAction names the coordinator: "fix failing checks" |
| T-DEMO-02 (claim only) | w-DEMO-01 reported done 08:12Z `[claim]`; no independent check seen |
| w-DEMO-09 (watch) | last evidence time 08:49Z (16m); silence limit 15m; holds T-DEMO-07 |
| Q-DEMO-00 (resolved) | created 05:59Z; answered and resolved 09:01Z with resolution linkage ev M-DEMO-102; thread TH-DEMO-02 |
| Fleet | 12 workers listed (w-DEMO-01 to w-DEMO-12): 8 live, 3 exited, 1 unverifiable (w-DEMO-09) |
| Previous report seq 0411 | Q-DEMO-01, 02, 04, M-DEMO-140, Q-DEMO-00 and A-DEMO-12 observed open; T-DEMO-03 had no checks; w-DEMO-09 inside its limit |

**Derived counts (seq 0412).** Observed actionable bundles: 8 (M-DEMO-140, Q-DEMO-01, Q-DEMO-02, Q-DEMO-03, Q-DEMO-04, A-DEMO-12, T-DEMO-03, T-DEMO-02). Decisions `>=3` (Q-DEMO-01, 02, 03); unclassified 1; answered-open 1; failing 2 (A-DEMO-12, T-DEMO-03); unverified 1 (T-DEMO-02). Tasks blocked by observed decisions: union {T-DEMO-04, 05, 06, 07} = 4, not 5, because T-DEMO-06 is shared. Q-DEMO-04 is shown in its own band and, pending INV-021 (section 20), is neither counted as a decision nor eligible for the OLDEST line.

The fixture checks are counts from the invented world, each with its own denominator. No cost, token, percentage or trend appears anywhere in the mockups.

## 8. Concept A: Attention Brief (default)
<!-- Source: Variant 1 (opus:architect), s.6 Attention Brief, with Base s.5 integrity content and Variant 2 (sonnet:analyzer) s.4.1 and s.6 ANSWERED band, WATCH row and SINCE strip — merged per Change 4 -->

**Organizing principle:** the report is a triage queue. Everything a human must decide is ranked by the age of the blocking need; everything else is compressed below it. The unit of reading is a decision bundle, not a worker row. This is the recommended default (section 14).

### 8.1 Body grammar

| Order | Section | Line budget | Sort key | Requirements |
|---|---|---|---|---|
| 1 | NEEDS YOU (decisions and `unclassified` items) | header + up to 18 (bundles of 3 lines, plus the rule 1 warning) | qualified-age items first (DEC-7), then original age descending; ties by key | DEC-1..7, COM-1, COM-7 |
| 2 | ANSWERED, NOT RESOLVED | header + up to 4 | original age descending | DEC-6, COM-3 |
| 3 | FAILING / NOT VERIFIED | header + up to 8 | one pinned verification contradiction (rule 2), then failures, then `complete (claim only)`; age descending | BLK-1, BLK-4, VER-1..4 |
| 4 | SINCE strip | 2 | newly observed, worse, resolved (with evidence), vanished (full read only) | CHG-1..5 |
| 5 | WATCH | up to 2 | silence beyond the stated limit, by evidence time | COV-9 |
| 6 | FLEET | up to 2 | fixed | COV-9, VER-5 |

No VERIFY, failure, change or fleet row sits above the decision block (DEC-1). A verification contradiction is pinned at the top of section 3, not above the decisions. Answered-but-unresolved decisions sit in their own band directly under NEEDS YOU, because the next actor may no longer be the human but the item is not resolved (DEC-6). Whether they count toward DEC-1 and OLDEST is open question INV-021; until it is decided they are shown but not counted as decisions and not OLDEST-eligible.

### 8.2 Busy screen (synthetic, fixture seq 0412)

```
=== ORCA SNAPSHOT [A:BRIEF] seq 0412 ================= SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
NEEDS YOU  decisions >=3 + unclassified 1 (census unknown)
 ! M-DEMO-140 seen>=32m w-DEMO-04 > ?  T-DEMO-11 run-DEMO-B UNCLASSIFIED
     "Lockfile drift vs main, holding here."
     blocks ? | T-DEMO-11 ready ? | ev M-DEMO-140 (no thread)
   oldest not certified: 1 item(s) lack a creation time
 ! Q-DEMO-01 2h14m w-DEMO-07 > human-DEMO-op  T-DEMO-04 run-DEMO-A
     "Approve schema change for T-DEMO-04?"
     blocks 4 (1 direct, 3 indirect) | ev M-DEMO-118 TH-DEMO-11
 ! Q-DEMO-02   45m w-DEMO-03 > human-DEMO-op  T-DEMO-06 run-DEMO-A
     "Target API v2 or v3 for T-DEMO-06?"
     blocks 1 (direct; shared with Q-DEMO-01) | ev M-DEMO-131 TH-DEMO-19
 ! Q-DEMO-03    7m w-DEMO-11 > ?  T-DEMO-09 run-DEMO-B
     "Retain or release worktree wt-DEMO-9?"
     blocks ? (no task link) | relay coord-DEMO is not owner | ev M-DEMO-137
ANSWERED, NOT RESOLVED  1  (a reply is not a resolution)
   Q-DEMO-04 1h35m w-DEMO-02 > human-DEMO-op  T-DEMO-08 run-DEMO-B
     human replied 08:55Z "Use the staging bucket."; no resolution seen
------------------------------------------------------------------------------
FAILING / NOT VERIFIED  failing 2, unverified 1               3 shown of 3
 V T-DEMO-03  25m w-DEMO-05 reported complete; checks FAIL 2 of 14 ran
     [claim] [checks@demo-b7:fail] lint-DEMO unit-DEMO-3 | not done
 X A-DEMO-12  24m w-DEMO-12 T-DEMO-10 attempt failed 08:41Z, no replacement
     ev worker-list page 2
 U T-DEMO-02  53m w-DEMO-01 complete (claim only) [claim] | no check seen
------------------------------------------------------------------------------
SINCE 09:00Z (seq 0411)  newly observed Q-DEMO-03 | worse T-DEMO-03 checks
  resolved Q-DEMO-00 [human] answered+resolved 09:01Z ev M-DEMO-102
WATCH  w-DEMO-09 last evidence 08:49Z (16m, limit 15m); holds T-DEMO-07
FLEET  12 workers listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0412 ===
```

Reading notes: M-DEMO-140 is first because its age is only a lower bound (`seen>=32m`) and it matched no routine form, so it is `unclassified` rather than a hidden heartbeat (section 4). The OLDEST line still names Q-DEMO-01, the oldest known-age item, and the warning line says the oldest cannot be certified. `blocks ?` means dependency data was not seen, not that nothing is blocked. Q-DEMO-03's owner is `?`: the coordinator relayed it, and a relay is never the acting owner. The union of blocked tasks is 4, not 5, because T-DEMO-06 is shared. WATCH uses the worker's last evidence time, not the collection time (INV-022, section 20).

### 8.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Answers the success criterion directly: the oldest observed blocking decision is ranked in the decision block and repeated in `OLDEST observed`. | Location context is thin: the reader sees runs per row but no fleet-wide shape. |
| Each decision row carries question, requester, owner, impact and evidence; no transcript needed for the common case. | Three-line bundles cap the visible queue at about five decisions; a busy fleet relies on the overflow line (section 16). |
| Lowest learning cost; reads top-down. | Root-cause structure is reduced to a `blocks N` number, so one unblock that frees many tasks is not obvious. |
| The SINCE strip gives change awareness without letting changes displace unanswered context (COM-3). | Unclassified rows add noise; noise is preferred to a hidden decision (COM-7). |

**State handling:** section 15 renders this concept in the empty, stale and checks-failing states; section 16 renders its overflow state.

## 9. Concept B: Ball-Holder Board
<!-- Source: Variant 2 (sonnet:analyzer), s.4.2 Ball-Holder Board — merged per Change 5; owner field corrected per Base rule (A-002) -->

**Organizing principle:** the report is split by who holds the next move. The operator sees at once which items are theirs and which wait on someone else, so coordinator backlog stops masquerading as human work and orphaned work becomes visible. The axis is responsibility, not age (A), cause (C), conversation (D) or time (E).

### 9.1 Body grammar

| Order | Band | Content | Rules |
|---|---|---|---|
| 0 | NEXT MOVE | One line of band counts | Counts are bundles in this report; `>=` where the census is unknown. |
| 1 | HUMAN (decision block) | Decisions owned by the human, plus decisions and `unclassified` items whose owner is `?` | DEC-1: this band is always first. Owner `?` items stay here until an owner is seen, because nobody else is shown to hold them. Order per DEC-7 and rule 2. |
| 2 | ANSWERED, NOT RESOLVED | Decisions with an observed reply and no resolution | Next mover printed as `?` unless a source names it; a reply is not resolution (DEC-6). |
| 3 | COORDINATOR | Items whose next move a source field assigns to the coordinator | Quoted from the source field (`nextAction as reported by source`); not inferred from relaying. |
| 4 | WORKER | Workers silent past the stated limit | Clock is the worker's last evidence time (INV-022). |
| 5 | NOBODY KNOWN | Failures and verification gaps with no owner seen | These do not move by themselves. |
| 6 | RECONCILIATION | Per-run task accounting (section 9.3) | Assignment, verification and execution kept apart (VER-1). |
| 7 | SINCE, FLEET | Change strip and fleet counts | Last in the body (COV-9). |

The owner in `a > b` is never the coordinator relay (section 6.3). Where Variant 2 printed `> coord`, the merged screens print the acting human or `?`.

### 9.2 Busy screen (synthetic, fixture seq 0412)

```
=== ORCA SNAPSHOT [B:BALL-HOLDER] seq 0412 =========== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
NEXT MOVE human 2 | owner ? 2 | answered 1 | coord 1 | worker 1 | nobody 2
------------------------------------------------------------------------------
HUMAN (decision block; owner ? stays here until an owner is seen)
 ! M-DEMO-140 seen>=32m w-DEMO-04 > ?  T-DEMO-11 UNCLASSIFIED
     "Lockfile drift vs main, holding here."  T-DEMO-11 ready ?
   oldest not certified: 1 item(s) lack a creation time
 ! Q-DEMO-01 2h14m w-DEMO-07 > human-DEMO-op  holds 4 (1 direct)
     "Approve schema change for T-DEMO-04?"  ev M-DEMO-118
 ! Q-DEMO-02   45m w-DEMO-03 > human-DEMO-op  holds 1 (shared)
     "Target API v2 or v3 for T-DEMO-06?"  ev M-DEMO-131
 ! Q-DEMO-03    7m w-DEMO-11 > ?  (relayed by coord-DEMO, not owner)
     "Retain or release worktree wt-DEMO-9?"  holds ?  ev M-DEMO-137
------------------------------------------------------------------------------
ANSWERED, NOT RESOLVED (next mover ?; a reply is not a resolution)
   Q-DEMO-04 1h35m w-DEMO-02 > human-DEMO-op  T-DEMO-08 waiting
     replied 08:55Z "Use the staging bucket."  ev M-DEMO-122
------------------------------------------------------------------------------
COORDINATOR (per source field; not yours unless it stays past 30m)
 V T-DEMO-03 25m w-DEMO-05 complete [claim]; checks@demo-b7 FAIL 2 of 14
     nextAction as reported by source: fix failing checks
------------------------------------------------------------------------------
WORKER (listed only when silent past limit 15m)
   w-DEMO-09 last evidence 08:49Z (16m); holds T-DEMO-07
------------------------------------------------------------------------------
NOBODY KNOWN (no owner seen; these do not move by themselves)
 X A-DEMO-12 24m T-DEMO-10 attempt failed 08:41Z, no replacement seen
 U T-DEMO-02 53m complete (claim only) [claim]; no verifier seen
------------------------------------------------------------------------------
RECONCILIATION per run (assignment, verification, execution kept apart)
 run-DEMO-A 6 tasks: waiting on decisions 4 (T-DEMO-04 to T-DEMO-07)
   complete [claim] 2: T-DEMO-02 no check | T-DEMO-03 checks fail
 run-DEMO-B 4 tasks: T-DEMO-08 waiting | T-DEMO-10 attempt failed
   T-DEMO-09 status ? | T-DEMO-11 ready ?
 decision-blocked tasks 4 (union) | resource wt-DEMO-9, others ?
------------------------------------------------------------------------------
SINCE 09:00Z (seq 0411)  newly observed Q-DEMO-03 | worse T-DEMO-03
  resolved Q-DEMO-00 [human] 09:01Z ev M-DEMO-102
FLEET 12 listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0412 ===
```

Reading notes: the NEXT MOVE counts are the eight observed bundles split by band (2 + 2 + 1 + 1 + 2), plus the one silent worker, which is not an attention bundle. Q-DEMO-03 and M-DEMO-140 have owner `?` and sit in the decision block, not under NOBODY KNOWN, so DEC-1 holds and no decision is pushed below a failure. T-DEMO-03 is under COORDINATOR only because a structured source field names its next action; the band would read `?` without it.

### 9.3 Supporting block: run reconciliation
<!-- Source: Base (original, modified) — V3 s.6 Run Ledger reconciliation retained as the RECONCILIATION band of Concept B per Change 5 -->

The RECONCILIATION band keeps the Run Ledger's accounting: each run lists its distinct tasks with assignment outcome, verification evidence and execution observation as separate facts, so a completed assignment that keeps a terminal is never read as ready and a failed check stays visible even when the assignment says complete. Busy runs omit inventory rows before any question; a missing source produces an unknown value and a stale run block, never an empty run. Execution observations from the worker list are not readiness evidence. The band reports the union of decision-blocked tasks, not a sum of per-decision holds.

### 9.4 Tradeoffs

| Strength | Weakness |
|---|---|
| Answers "is this mine" without reading text; isolates coordinator backlog and orphaned work. | Ownership for messages is inferred from structured fields where they exist; elsewhere it is `?`, and a band of `?` owners is less informative. |
| Makes missing ownership visible rather than assumed. | The oldest decision is first within the HUMAN band only; the frame OLDEST line carries it when the band is long. |
| The reconciliation band keeps whole-run accounting without a second report. | The 30m coordinator threshold is a design choice, not an observed norm. |
| Fits several humans or a coordinator sharing responsibility. | Spends more lines on non-decision context than A. |

**State handling:** section 15.5 gives this concept's empty, stale, checks-failing and busy behaviour.

## 10. Concept C: Root-Blocker Tree
<!-- Source: Variant 1 (opus:architect), s.8 Root-Blocker Tree layout, with Base s.7 Blocker Paths rules (age-ranked roots, dependency conflict, also under, union footer) — merged per Change 6 -->

**Organizing principle:** the report is a forest of root causes. Each root (a decision, an `unclassified` item, a failure or a verification gap) is listed once, with the distinct tasks waiting on it drawn beneath. Indentation means an explicit blocking relation, never process or workspace ancestry. The reader sees why several workers wait on one answer.

### 10.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| DECISION ROOTS | Decisions and `unclassified` items, each its own root | Always first (DEC-1). Qualified-age items first (DEC-7), then by original age, oldest first; never by estimated impact, because no complete graph exists. Two decisions blocking one task stay separate roots (BLK-2). A root without dependency data prints `deps?` and no tree. |
| ANSWERED, NOT RESOLVED | Answered decisions with their waiting task | Not a root while INV-021 is open; one line each. |
| OTHER ROOTS | Verification gaps and failures | One pinned verification contradiction first (rule 2), then failures, then `complete (claim only)`, each by age. |
| UNION | Distinct blocked tasks with keys; runs with unknown dependencies | Do not sum tree rows. A task under two roots is drawn under the older root and printed `also under [n]` at the other, counted once (BLK-3). |
| SINCE, FLEET | Change strip and fleet counts | Last in the body (COV-9). |

A cycle is never recursed: its members print once as `dependency conflict: <IDs>` under the oldest member's root, and count once in the union. Tree depth is capped at 3 levels below a root; deeper descendants fold into `+N deeper (keys)`.

### 10.2 Busy screen (synthetic, fixture seq 0412)

```
=== ORCA SNAPSHOT [C:TREE] seq 0412 ================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
DECISION ROOTS (qualified age first, then oldest first)         4 roots
[1] M-DEMO-140 seen>=32m UNCLASSIFIED w-DEMO-04 > ?           deps?
    "Lockfile drift vs main, holding here."  T-DEMO-11 ready ?
    oldest not certified: 1 item(s) lack a creation time
[2] Q-DEMO-01 2h14m w-DEMO-07 > human-DEMO-op     affects 4 (1 direct)
    "Approve schema change for T-DEMO-04?"  ev M-DEMO-118
    `- T-DEMO-04 waiting                                       direct
       |- T-DEMO-05 waiting                                    indirect
       `- T-DEMO-06 waiting  also under [3]                    indirect
          `- T-DEMO-07 waiting (w-DEMO-09 silent 16m)          indirect
[3] Q-DEMO-02   45m w-DEMO-03 > human-DEMO-op     affects 1 (shared)
    "Target API v2 or v3 for T-DEMO-06?"  ev M-DEMO-131
    `- T-DEMO-06  also under [2] (counted once)                direct
[4] Q-DEMO-03    7m w-DEMO-11 > ?  relay coord-DEMO is not owner  deps?
    "Retain or release worktree wt-DEMO-9?"  no task link seen
------------------------------------------------------------------------------
ANSWERED, NOT RESOLVED (not a root while INV-021 is open)
    Q-DEMO-04 1h35m replied 08:55Z, no resolution; T-DEMO-08 waiting
------------------------------------------------------------------------------
OTHER ROOTS (pinned verification contradiction, then failures)  3 roots
[5] V T-DEMO-03 25m complete [claim]; checks@demo-b7 FAIL 2 of 14
    lint-DEMO unit-DEMO-3 | dependents ? (links not seen)
[6] X A-DEMO-12 24m T-DEMO-10 attempt failed 08:41Z, no replacement
    dependents ? (links not seen)
[7] U T-DEMO-02 53m complete (claim only), no check seen
------------------------------------------------------------------------------
UNION distinct blocked tasks 4: T-DEMO-04 05 06 07 (do not sum roots)
  dependency conflict 0 observed | run-DEMO-B links ? | graph partial
------------------------------------------------------------------------------
SINCE 09:00Z (seq 0411)  newly observed Q-DEMO-03 | worse T-DEMO-03
  resolved Q-DEMO-00 [human] 09:01Z ev M-DEMO-102
FLEET 12 listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0412 ===
```

Reading notes: Q-DEMO-01 affects 4 and Q-DEMO-02 affects 1, but the union is 4, because T-DEMO-06 is drawn once under the older root [2] and referenced at [3]. Roots [1] and [4] have no tree because dependency data was not seen, not because nothing waits on them. Failure roots print `dependents ?` for the same reason.

### 10.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Shows the leverage of one answer and makes shared dependents explicit without double counting. | Most demanding data prerequisite: missing or inferred edges make a neat tree dangerously persuasive, and with `deps?` on many roots the tree degrades into a list. |
| Age ranking keeps the oldest decision first among the decision roots, so the success criterion does not depend on the frame line alone. | No critical-path or unlock-size ranking is possible without a complete graph. |
| Separates "blocking others" from "merely open" decisions. | Deep or wide trees exceed the line budget quickly; folding loses detail. |
| Natural precursor to an interactive drill-down. | Communication context is limited to the question line. |

**State handling:** section 15.5.

## 11. Concept D: Conversation Ledger
<!-- Source: Variant 1 (opus:architect), s.9 Conversation Ledger with its y/n/? delivery ladder, with Base s.8 acting-human versus requester distinction — merged per Change 7 -->

**Organizing principle:** the report is a ledger of open conversations. Each thread shows what was originally asked, the last thing said, and which delivery facts are known. Work status appears only as context for a thread.

### 11.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| WAITING ON A DECISION | Decision threads and `unclassified` messages, each a 3-line bundle | Always first (DEC-1). Qualified-age items first (DEC-7), then oldest first. Ladder `enq dlv proc ans res`, each `y`, `n` or `?` (COM-2): `n` only when a source affirmatively shows the fact is false; a fact not seen in a capped read is `?`. Original question always shown (COM-1); if its text was not in the read, the row says so. |
| ANSWERED, NOT RESOLVED | Threads with an observed answer and no resolution evidence | A reply is not resolution (DEC-6). Not counted as a decision while INV-021 is open. |
| STUCK AGENT-TO-AGENT | Worker-to-coordinator threads unprocessed beyond 15m | Only those past the threshold; an empty section under a capped read prints `0 observed (partial)` (COV-3). |
| CLOSED THREADS | Threads resolved in this window, with resolution evidence | Resolution only with explicit linkage (rule 3). |
| WORK CONTEXT, WATCH, FLEET | Failures and verification gaps in compact form; silence watch; fleet counts | After all thread content (COV-9). |

Each row names the requester and the acting owner as `requester > owner`. A coordinator relay is never the owner (section 6.3); its message prints as `relay (not an answer)`. Routine messages update last-seen times only and are never listed (COM-4). Repeated messages in one thread fold into `(repeat xN folded)` (BLK-5).

### 11.2 Busy screen (synthetic, fixture seq 0412)

```
=== ORCA SNAPSHOT [D:LEDGER] seq 0412 ================ SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
WAITING ON A DECISION  >=3 + unclassified 1 (msgs capped)      4 shown of 4
 key         thread       age         enq dlv proc ans res
 M-DEMO-140  (no thread)  seen>=32m    y   ?   ?    ?   ?
   w-DEMO-04 > ?  UNCLASSIFIED  T-DEMO-11 ready ?
   "Lockfile drift vs main, holding here."
   oldest not certified: 1 item(s) lack a creation time
 Q-DEMO-01   TH-DEMO-11   2h14m        y   ?   ?    ?   ?
   w-DEMO-07 > human-DEMO-op  T-DEMO-04 | ev M-DEMO-118
   Q "Approve schema change for T-DEMO-04?"  last: none after Q
 Q-DEMO-02   TH-DEMO-19   45m          y   ?   ?    ?   ?
   w-DEMO-03 > human-DEMO-op  T-DEMO-06 | ev M-DEMO-131
   Q "Target API v2 or v3 for T-DEMO-06?"  last: none after Q
 Q-DEMO-03   TH-DEMO-22   7m           y   ?   y    ?   ?
   w-DEMO-11 > ?  T-DEMO-09 | ev M-DEMO-137
   Q "Retain or release worktree wt-DEMO-9?"
   last: coord-DEMO relay (not an answer); a relay is not the owner
------------------------------------------------------------------------------
ANSWERED, NOT RESOLVED  1  (a reply is not a resolution)
 Q-DEMO-04   TH-DEMO-14   1h35m        y   y   ?    y   ?
   w-DEMO-02 > human-DEMO-op  T-DEMO-08 | ev M-DEMO-122
   Q text not in this read | A 08:55Z "Use the staging bucket."
------------------------------------------------------------------------------
STUCK AGENT-TO-AGENT (unprocessed > 15m)  0 observed (partial: msgs capped)
CLOSED THREADS since 09:00Z  TH-DEMO-02 Q-DEMO-00 res y [human] 09:01Z
  resolution linkage ev M-DEMO-102
------------------------------------------------------------------------------
WORK CONTEXT  V T-DEMO-03 complete [claim]; checks@demo-b7 FAIL 2 of 14
  X A-DEMO-12 T-DEMO-10 failed 08:41Z, no replacement
  U T-DEMO-02 complete (claim only), no check seen
WATCH  w-DEMO-09 last evidence 08:49Z (16m, limit 15m); holds T-DEMO-07
FLEET  12 workers listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0412 ===
```

Reading notes: most ladder cells are `?` because the fixture's capped read shows that each question was enqueued but not whether it was delivered, processed or answered; `?` is not `n`. Q-DEMO-03 has `proc y` because the coordinator relayed it, yet its owner stays `?`. Q-DEMO-04 has `ans y` and `res ?`: the reply is visible, the resolution is not. Its original question text was not in this read, and the row says so rather than paraphrasing the answer as the question.

### 11.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Strongest communication context: original question, last statement and delivery facts side by side. | Most dependent on message sources, which are exactly the capped, non-paged ones; counts stay `>=N` and many ladder cells are `?`. |
| Makes "relayed but not answered" and "answered but not resolved" visible, which other concepts compress. | Work status (failures, verification gaps) is pushed into a compact context block and can be missed. |
| Shows agent-to-agent stalls that may become human decisions later. | Ladder fields `proc` and `res` need sources not yet verified (gate FG-12, section 20). |
| Folding repeats suppresses spam without losing the thread. | Tall per item (3 lines), so only a few threads fit the budget. |

**State handling:** section 15.5.

## 12. Concept E: Delta Journal
<!-- Source: Variant 1 (opus:architect), s.10 Delta Journal (THIS WINDOW, STILL OPEN, TRAIL), repaired under DEC-1, with Base s.4 rules 4-5 and s.9 delta semantics — merged per Change 8 -->

**Organizing principle:** the report is a journal entry for the window since the last successful comparable observation. Below the decision block, changes come first; a carried-forward list keeps every other open item visible so unanswered context is not lost when nothing changes (COM-3), and a short trail summarizes earlier windows so a reader joining late sees recent history and collection gaps.

### 12.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| OPEN DECISIONS | Every open decision and `unclassified` item, 2-line bundles, each tagged with its change in this window | Always first (DEC-1), even when nothing changed. Qualified-age items first (DEC-7), then oldest first. Answered-but-unresolved items get one line at the end of the block. |
| THIS WINDOW | Change entries: NEWLY OBSERVED, ESCALATED, AGED (crossed a stated threshold), WORSE / VERIFY-GAP, RESOLVED, VANISHED | Only against the last successful comparable observation of the same source and scope (CHG-1, rule 4). Heartbeats and liveness flaps excluded (CHG-4). |
| STILL OPEN | Every other open attention item, one line each | Pinned verification contradiction first, then by age. Items that changed are repeated here with a pointer, so the open list stays complete. |
| TRAIL | Earlier windows, one line each, counts only | A failed window prints `COLLECTION FAILED (src) - no deltas, baseline kept`, never zeros (CHG-2). Needs stored observation history. |

Delta semantics (rules 4-5):

- A partial or capped read can establish only positive additions, labelled `newly observed`, never absence, resolution or negative movement. An item first seen after the cap window moves is `newly observed`, not `new`: newly observed is not necessarily newly created.
- RESOLVED needs explicit resolution evidence (rule 3).
- VANISHED is shown only after a full read of the relevant source, and then as `last known unresolved` with its last-seen time, never as a resolution. Under a capped read the VANISHED entry prints `n/a`.
- With no stored baseline (first run, empty store or scope change) THIS WINDOW prints `baseline unavailable` and the report still renders OPEN DECISIONS and STILL OPEN in full (INV-002, section 20).

### 12.2 Busy screen (synthetic, fixture seq 0412)

```
=== ORCA SNAPSHOT [E:JOURNAL] seq 0412 =============== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
OPEN DECISIONS (carried every report; qualified age first)     4 shown of 4
 M-DEMO-140 seen>=32m UNCLASSIFIED w-DEMO-04 > ?  T-DEMO-11   no change
   "Lockfile drift vs main, holding here."  T-DEMO-11 ready ?
   oldest not certified: 1 item(s) lack a creation time
 Q-DEMO-01 2h14m w-DEMO-07 > human-DEMO-op  blocks 4          no change
   "Approve schema change for T-DEMO-04?"  ev M-DEMO-118
 Q-DEMO-02   45m w-DEMO-03 > human-DEMO-op  blocks 1 shared   no change
   "Target API v2 or v3 for T-DEMO-06?"  ev M-DEMO-131
 Q-DEMO-03    7m w-DEMO-11 > ?  relay coord-DEMO not owner   newly obs.
   "Retain or release worktree wt-DEMO-9?"  ev M-DEMO-137
 answered, not resolved: Q-DEMO-04 1h35m reply 08:55Z, no resolution
------------------------------------------------------------------------------
THIS WINDOW 09:00Z -> 09:05Z vs seq 0411 (transitions inside may be missed)
 + NEWLY OBSERVED Q-DEMO-03 7m (not necessarily newly created)
 V WORSE      T-DEMO-03 no checks -> checks@demo-b7 FAIL 2 of 14
 > AGED       w-DEMO-09 silence crossed 15m limit (16m); holds T-DEMO-07
 - RESOLVED   Q-DEMO-00 [human] 09:01Z resolution linkage ev M-DEMO-102
 ^ ESCALATED  0 observed (partial: msgs capped)
 ! VANISHED   n/a (msgs capped: absence proves nothing)
------------------------------------------------------------------------------
STILL OPEN (pinned verification gap, then by age)              3 shown of 3
 V T-DEMO-03 25m complete [claim]; checks FAIL (worse above)
 U T-DEMO-02 53m complete (claim only), no check seen
 X A-DEMO-12 24m T-DEMO-10 attempt failed 08:41Z, no replacement
------------------------------------------------------------------------------
TRAIL  08:55Z->09:00Z and earlier: n/a (no stored history in fixture)
FLEET  12 workers listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 8 (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0412 ===
```

Reading notes: the decision block comes first even though Q-DEMO-01 did not change; without it the oldest observed decision would sit below a newer, lower-impact change (the urgency bias named in the tradeoffs). VANISHED is `n/a` because the message read is capped: Q-DEMO-03 can be added as newly observed, but nothing can be declared gone. RESOLVED Q-DEMO-00 carries its resolution linkage, not just its disappearance.

### 12.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Best for an operator who reads every paste: the change lines say exactly what moved since the last good observation. | Requires durable observation history to render TRAIL and AGED; without it, the journal degrades to a two-section diff. |
| TRAIL makes collection gaps visible over time, which no other concept shows. | Change wording can create urgency bias; the decision block above THIS WINDOW is the repair, at a cost of lines. |
| Threshold-based AGED entries make slow drift visible without a trend metric. | Duplication between THIS WINDOW and STILL OPEN costs lines. |
| Natural fit for chat, where earlier pastes scroll away. | Under capped reads half of the change kinds (ESCALATED, VANISHED) print as partial or `n/a`. |

**State handling:** section 15.5.

## 13. Comparison and data dependency
<!-- Source: Variant 1 (opus:architect), s.11.1 Comparison and s.11.2 Data dependency per concept — merged per Change 10; cells marked * adjusted for Changes 4-8 -->

### 13.1 Comparison

Ratings are design judgments about the mockups in this document, not measured results. `+` strong, `o` adequate, `-` weak. A cell marked `*` differs from the original rating because the merged concept differs: B is the Ball-Holder Board (Change 5), not a run-by-lane matrix; C ranks roots by age (Change 6); E puts the decision block first (Change 8).

| Criterion | A Brief | B Ball-Holder | C Tree | D Ledger | E Journal |
|---|---|---|---|---|---|
| Oldest blocking decision is structurally first (success criterion) | + | o* (first within the HUMAN band) | +* (age-ranked roots) | + | +* (decision block first) |
| Needed action understandable without a transcript | + | o* (question line per decision) | o | + | o |
| Partial coverage visible where it matters | o (global) | +* (per-run reconciliation) | o | o | + (trail) |
| Stale/unavailable without false zero | + | + | o | o | + |
| Reported-complete-but-checks-failing visible | + | + | + | - | + |
| No double counting of dependents | + | +* (union in reconciliation) | + | + | + |
| Fleet shape at a glance | - | o* (responsibility split, not a matrix) | o | - | - |
| Who holds the next move | o | +* | - | o | - |
| Change visibility | o (SINCE strip) | o* (SINCE strip) | o* (SINCE strip) | - | + |
| Works with only the sources inspected so far | + | o* (needs ownership fields) | - (needs dependency data) | - (needs delivery ladder) | o (needs history) |
| Reuse as the interactive terminal's default view | + (queue) | o* (filter by owner) | o (drill-down) | o (thread pane) | - |

The "who holds the next move" row is added for the Ball-Holder axis; it has no counterpart in the original comparison.

### 13.2 Data dependency per concept

| Concept | Needs beyond worker-list and capped message reads | Degrades to |
|---|---|---|
| A | Nothing required; dependency data improves `blocks N` | `blocks ?` |
| B | Structured ownership and next-action fields per item; per-run collection status for reconciliation | Owner `?` rows held in the decision block; starred stale run blocks |
| C | Complete task dependency graph | Decision roots with `deps?` and no tree (UNROOTED-style list) |
| D | Delivery ladder facts (delivered, processed, resolved) and thread identity | Mostly `?` ladder cells |
| E | Durable observation history across windows | Two-section diff without TRAIL or AGED; `baseline unavailable` on first run |

## 14. Default and switch rule
<!-- Source: Variant 1 (opus:architect), s.11.3 Recommended default, with Variant 2 (sonnet:analyzer) s.6 rationale and switch condition — merged per Change 10 (invariant INV-020: one switch rule) -->

**Default: Concept A, Attention Brief, with the SINCE strip** (section 8). The strip gives one line of change awareness without displacing the decision block; the ANSWERED, NOT RESOLVED band and the WATCH row are part of the default body grammar.

**Rationale, in order of weight.**

1. **It matches the stated success criterion directly.** The operator's success test is finding the oldest observed blocking decision without opening every transcript. A ranks that decision in a fixed position and carries question, requester, owner, impact and evidence on the row, and the `OLDEST observed` frame line repeats it.
2. **Lowest source coupling.** A renders honestly with only the sources already inspected: paged worker-list and capped non-consuming message reads. C, D and E each depend on a source or history that is not yet verified (section 13.2), and B depends on ownership fields. A default should not depend on an open feasibility gate.
3. **It degrades gracefully.** Without dependency data a row reads `blocks ?` and stays valid. Without a stored baseline the SINCE strip prints `baseline unavailable` and the rest of the report is unchanged.
4. **It is stable.** Rows are ordered by age with qualified-age items first (DEC-7), so placement does not jump between reports of an unchanged model (FMT-4).
5. **It is cheap to replace.** Every concept is a renderer over the same model and frame (section 2); choosing A now does not lock out B, C, D or E.

**Costs accepted.** A shows no dependency shape and no fleet matrix; one unblock that frees many tasks is visible only as a `blocks N` number. "Who holds the next move" is expressed only by the ANSWERED, NOT RESOLVED band and the owner field. These are the reasons B, C, D and E remain full alternates rather than discards.

**The one switch rule.** Switch the default from A to E, Delta Journal, only if evaluation shows that E **ties** A on ET-1 (finding the oldest observed decision: both meet the ET-1 accuracy target and E's median time is within 5 seconds of A's) **and wins** on ET-6 (E's change recall is higher than A's at the ET-6 precision target). No other result changes the default. If A misses its own ET-1 or ET-4 target, A's wording is revised and re-tested (section 17.3); that is not a switch.

**Whichever concept is the default keeps the shared frame** (section 6), including the `OLDEST observed` line, the header qualifiers and the end marker. A switch to E changes only the layer-4 body renderer.

B, C and D can be offered as companion views once their gates close (section 20), but they do not replace the default under this rule.

## 15. Default across four states and concept x state matrix
<!-- Source: Variant 2 (sonnet:analyzer), s.7.2-7.4 four states and s.8 other concepts under the four states, with Base s.10 scope-qualified empty state and last-known stale bundles — merged per Change 9; all-clear wording removed per Change 13 (invariant INV-006) -->

Each state uses the default, Concept A, inside the shared frame. The section order and symbols do not change between states, so the reader learns one layout. No state prints a fleet-wide all-clear or any conditional variant of one (COV-4); the strongest calm statement any screen can make is `no attention items observed in <scope>`, always beside the coverage and census qualifiers. An empty band or row prints `0 observed`, never disappears, so omission cannot be confused with suppression or failure (INV-017, section 18).

### 15.1 Empty (nothing observed)

Variation: the same runs at 12:05Z (seq 0501; previous successful report seq 0500 at 12:00Z). Every seq 0412 item was closed before seq 0500 by explicit evidence: Q-DEMO-01 to Q-DEMO-04 and M-DEMO-140 by linked resolutions, T-DEMO-10 by a replacement attempt with passing checks, T-DEMO-02 and T-DEMO-03 by passing checks on their head revisions. Messages read: 22 of cap 100. Fleet: 12 listed, 4 live, 8 exited.

```
=== ORCA SNAPSHOT [A:BRIEF] seq 0501 ================= SYNTHETIC DEMO DATA ===
as-of 2026-01-01T12:05Z prev-ok 12:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs ok 22/100 no-paging | checks ok 12:02Z
cover observed 0 (census unknown) | shown 0 | omitted 0 bundles
attn decisions >=0, unclassified 0, answered-open 0, failing 0, unverified 0
OLDEST observed none in run-DEMO-A run-DEMO-B (census unknown)
------------------------------------------------------------------------------
NEEDS YOU  no attention items observed in run-DEMO-A run-DEMO-B
  read: workers 3/3 pages, msgs 22 of cap 100, decision census unknown
  hosts: 1 covered of ? expected; other hosts were not observed
ANSWERED, NOT RESOLVED  0 observed
------------------------------------------------------------------------------
FAILING / NOT VERIFIED  0 observed; complete (claim only) 0 observed
------------------------------------------------------------------------------
SINCE 12:00Z (seq 0500)  newly observed 0 | worse 0 | resolved 0
WATCH  0 observed beyond limit 15m
FLEET  12 workers listed: live 4, exited 8, unverifiable 0
------------------------------------------------------------------------------
cover observed 0 (census unknown) | shown 0 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0501 ===
```

Rules visible here. `decisions >=0` is a lower bound because the message read has no paging; 22 returned messages under the cap of 100 do not prove a complete history (section 4). The body names its scope and repeats what was read, so the line cannot be read as a statement about hosts or runs outside the scope. Claim-only completions keep their own count even when it is 0, so a reader can see the category was checked.

### 15.2 Stale or unavailable

Variation: the 09:10Z and 09:15Z worker-list collections both failed (timeout); the message read and checks were not refreshed after seq 0412. Report seq 0502 at 09:15Z; last successful report seq 0412 at 09:05Z. Every row is the seq 0412 bundle, carried forward in full under the last-known banner (rule 3); ages advance by elapsed wall time while status is unconfirmed (rule 1).

```
=== ORCA SNAPSHOT [A:BRIEF] seq 0502 ================= SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:15Z prev-ok 09:05Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts ? covered of ? expected
src workers FAILED x2 | msgs STALE since 09:05Z | checks STALE since 09:02Z
cover observed 8~ last-known (census unknown) | shown 8 | omitted 0 bundles
attn ~ decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed ~Q-DEMO-01 2h24m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
LAST KNOWN UNRESOLVED / not confirmed current (from seq 0412, 09:05Z)
  worker-list failed 09:10Z and 09:15Z; messages and checks not refreshed
NEEDS YOU ~  decisions >=3 + unclassified 1 (census unknown)
 ! M-DEMO-140 seen>=42m~ w-DEMO-04 > ?  T-DEMO-11 run-DEMO-B UNCLASSIFIED
     "Lockfile drift vs main, holding here."
     blocks ? | T-DEMO-11 ready ? | ev M-DEMO-140 (no thread)
   oldest not certified: 1 item(s) lack a creation time
 ! Q-DEMO-01 2h24m~ w-DEMO-07 > human-DEMO-op  T-DEMO-04 run-DEMO-A
     "Approve schema change for T-DEMO-04?"
     blocks 4 (1 direct, 3 indirect) | ev M-DEMO-118 TH-DEMO-11
 ! Q-DEMO-02   55m~ w-DEMO-03 > human-DEMO-op  T-DEMO-06 run-DEMO-A
     "Target API v2 or v3 for T-DEMO-06?"
     blocks 1 (direct; shared with Q-DEMO-01) | ev M-DEMO-131 TH-DEMO-19
 ! Q-DEMO-03   17m~ w-DEMO-11 > ?  T-DEMO-09 run-DEMO-B
     "Retain or release worktree wt-DEMO-9?"
     blocks ? (no task link) | relay coord-DEMO is not owner | ev M-DEMO-137
ANSWERED, NOT RESOLVED ~ 1  (a reply is not a resolution)
   Q-DEMO-04 1h45m~ w-DEMO-02 > human-DEMO-op  T-DEMO-08 run-DEMO-B
     human replied 08:55Z "Use the staging bucket."; no resolution seen
------------------------------------------------------------------------------
FAILING / NOT VERIFIED ~ failing 2, unverified 1              3 shown of 3
 V T-DEMO-03  35m~ w-DEMO-05 reported complete; checks FAIL 2 of 14 ran
     [claim] [checks@demo-b7:fail] lint-DEMO unit-DEMO-3 | not done
 X A-DEMO-12  34m~ w-DEMO-12 T-DEMO-10 attempt failed 08:41Z, no replacement
     ev worker-list page 2 (seq 0412)
 U T-DEMO-02 1h03m~ w-DEMO-01 complete (claim only) [claim] | no check seen
------------------------------------------------------------------------------
SINCE n/a (no valid comparison; baseline kept at seq 0412, 2 samples missed)
WATCH ~ w-DEMO-09 last evidence 08:49Z (26m, limit 15m); holds T-DEMO-07
FLEET  ? (worker-list failed); 12 listed at 09:05Z, not confirmed current
------------------------------------------------------------------------------
cover observed 8~ last-known (census unknown) | shown 8 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0502 ===
```

The stale state keeps full bundles, not a summary (C-013): the question text, owner and evidence the reader needs are still there, marked `~`. Distinct failure labels stay distinct (C-014): `FAILED` for the worker list, `STALE since T` for sources not refreshed. Items newer than seq 0412 cannot appear, which the banner and `census unknown` state. SINCE refuses a delta rather than comparing against a failed collection (rule 4).

**First run or empty store (INV-002, open question in section 20).** If no successful observation exists to carry forward, the banner reads `No last-known records available` with the same failure labels, `cover` reads `observed ? (no successful read yet)`, the OLDEST line reads `OLDEST observed ? (no successful read yet)` and the body prints no `~` bundles. This is the interim rule until INV-002 is decided.

### 15.3 Reported complete, checks failing

Variation: seq 0503 at 09:05Z is the seq 0412 world plus one item, T-DEMO-08: w-DEMO-02 reported it complete at 08:25Z `[claim]`; its head revision demo-b9 was pushed at 08:58Z, and checks were seen only for the older revision demo-b7. Observed bundles become 9; unverified becomes 2.

```
=== ORCA SNAPSHOT [A:BRIEF] seq 0503 ================= SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 9 (census unknown) | shown 9 | omitted 0 bundles
attn decisions >=3, unclassified 1, answered-open 1, failing 2, unverified 2
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
NEEDS YOU  decisions >=3 + unclassified 1 (census unknown)
 ! M-DEMO-140 seen>=32m w-DEMO-04 > ?  T-DEMO-11 run-DEMO-B UNCLASSIFIED
     "Lockfile drift vs main, holding here."
     blocks ? | T-DEMO-11 ready ? | ev M-DEMO-140 (no thread)
   oldest not certified: 1 item(s) lack a creation time
 ! Q-DEMO-01 2h14m w-DEMO-07 > human-DEMO-op  T-DEMO-04 run-DEMO-A
     "Approve schema change for T-DEMO-04?"
     blocks 4 (1 direct, 3 indirect) | ev M-DEMO-118 TH-DEMO-11
 ! Q-DEMO-02   45m w-DEMO-03 > human-DEMO-op  T-DEMO-06 run-DEMO-A
     "Target API v2 or v3 for T-DEMO-06?"
     blocks 1 (direct; shared with Q-DEMO-01) | ev M-DEMO-131 TH-DEMO-19
 ! Q-DEMO-03    7m w-DEMO-11 > ?  T-DEMO-09 run-DEMO-B
     "Retain or release worktree wt-DEMO-9?"
     blocks ? (no task link) | relay coord-DEMO is not owner | ev M-DEMO-137
ANSWERED, NOT RESOLVED  1  (a reply is not a resolution)
   Q-DEMO-04 1h35m w-DEMO-02 > human-DEMO-op  T-DEMO-08 run-DEMO-B
     human replied 08:55Z "Use the staging bucket."; no resolution seen
------------------------------------------------------------------------------
FAILING / NOT VERIFIED  failing 2, unverified 2               4 shown of 4
 V T-DEMO-03  25m w-DEMO-05 reported complete; checks FAIL 2 of 14 ran
     [claim] [checks@demo-b7:fail] lint-DEMO unit-DEMO-3 | not done
 X A-DEMO-12  24m w-DEMO-12 T-DEMO-10 attempt failed 08:41Z, no replacement
     ev worker-list page 2
 ? T-DEMO-08  40m w-DEMO-02 reported complete 08:25Z [claim] | not done
     verification unknown: revision mismatch (head demo-b9 08:58Z,
     checks seen only for demo-b7)
 U T-DEMO-02  53m w-DEMO-01 complete (claim only) [claim] | no check seen
------------------------------------------------------------------------------
SINCE 09:00Z (seq 0411)  newly observed Q-DEMO-03 | worse T-DEMO-03 checks
  resolved Q-DEMO-00 [human] answered+resolved 09:01Z ev M-DEMO-102
WATCH  w-DEMO-09 last evidence 08:49Z (16m, limit 15m); holds T-DEMO-07
FLEET  12 workers listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 9 (census unknown) | shown 9 | omitted 0 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0503 ===
```

Two different problems stay separate: a failing result (`V` T-DEMO-03, pinned as the verification contradiction) versus no result for the current revision (`?` T-DEMO-08, `verification unknown: revision mismatch`). The worker's completion is shown as a claim and is never turned into "done" (VER-1..4). The screen carries no banner summarizing the fleet; the attention counts on the `attn` line are the summary.

### 15.4 Busy

The busy state is the screen in section 8.2 (seq 0412). Busy with overflow, where the body budget is reached, is the screen in section 16.1.

### 15.5 Other concepts under the four states

Described in words, because the frame, symbols and wording rules apply unchanged. Every concept carries the same frame, so the fixed `attn` line (FMT-8) and the `OLDEST observed` line are present in every state below; that is the common repair that keeps the weaker concepts from hiding a decision, a failure or an unverified completion. The last column names the residual risk of a falsely calm reading that remains for the concept.

| Concept | Empty | Busy | Stale or unavailable | Checks failing | Residual risk |
|---|---|---|---|---|---|
| B Ball-Holder | Every band prints `0 observed`; NOBODY KNOWN stays visible with its count so an ownership gap is not hidden; body leads with `no attention items observed in <scope>`. | HUMAN band by age (owner `?` items included); COORDINATOR and NOBODY KNOWN visible; overflow per band, each with shown + omitted = observed. | Bands print last-known bundles with `~` under the banner; NEXT MOVE counts become `>=` or `?`; each band names its source so one failed source does not leave other bands looking fresh. | Lands under COORDINATOR only when a source field names the coordinator (T-DEMO-03), otherwise under NOBODY KNOWN; T-DEMO-08 prints `verification unknown: revision mismatch`. | Several `0 observed` bands look calmer than one line; an item under COORDINATOR may be read as being handled. |
| C Tree | One line `no decision roots observed in <scope>` plus graph coverage; with graph coverage unknown, `0 roots` can mean `no links seen`, and the line says `deps?`. | Roots by age; deep trees fold into `+N deeper (keys)`; union line counts distinct tasks once. | All roots `~` under the banner; no new root can appear; union prints `>=N~`. | Appears under OTHER ROOTS (pinned contradiction first) unless it blocks tasks. | A stale tree looks authoritative because of its structure; failures outside any root have low prominence. |
| D Ledger | WAITING ON A DECISION prints `0 observed` with the cap note; STUCK AGENT-TO-AGENT prints `0 observed (partial)` under a capped read. | Threads by age with ladders; overflow lists IDs only; ladder columns kept. | Ladders freeze and every cell becomes `~` or `?`; no `y` is carried forward as current. | Appears in WORK CONTEXT, below all threads. | Highest: work status sits in the compact block and is easy to miss; ladder cells can hide that nothing was read. |
| E Journal | OPEN DECISIONS prints `0 observed in <scope>`; THIS WINDOW prints its counts; STILL OPEN prints `0 observed`. | Decision block first; THIS WINDOW capped first, STILL OPEN second; each prints shown + omitted = observed. | THIS WINDOW replaced by `n/a (no valid comparison)`; OPEN DECISIONS and STILL OPEN carried with `~`; TRAIL prints `COLLECTION FAILED (src) - no deltas, baseline kept`. | WORSE / VERIFY-GAP entry when the result flipped; otherwise in STILL OPEN with the pinned contradiction first. | `0` changes can read as "fine" when the open blocks are also empty because a source is partial; a check already failing at the last baseline never appears as a change. |

The default's own residual risk in these states is the noise of `unclassified` rows and the thin location context noted in section 8.3.

## 16. Overflow and budget
<!-- Source: Variant 2 (sonnet:analyzer), s.7.1 busy with overflow, with Variant 1 (opus:architect) s.13 OVF rules and Base s.4 rules 7-9 — merged per Change 9 and Change 14 (invariant INV-010) -->

### 16.1 Busy with overflow (default, seq 0504)

Variation: the seq 0412 world at 09:05Z plus 16 more decision questions, all owned by human-DEMO-op. Q-DEMO-20 (w-DEMO-06 on T-DEMO-05, created 07:00Z, "Pin dependency lib-DEMO at version 4.2?", ev M-DEMO-108, thread TH-DEMO-08) is older than Q-DEMO-02; Q-DEMO-21 to Q-DEMO-35 were created between 08:21Z and 08:57Z in ID order, so all are younger than Q-DEMO-02 and older than Q-DEMO-03. Q-DEMO-34 and Q-DEMO-35 were first observed at 09:05Z. T-DEMO-05 was already blocked indirectly by Q-DEMO-01, so the union of blocked tasks stays 4.

Counts: decisions observed 19 (Q-DEMO-01, 02, 03, 20 to 35); observed bundles 24 (19 decisions, 1 unclassified, 1 answered-open, 2 failing, 1 unverified). NEEDS YOU has a budget of a header and 18 lines (section 8.1), which holds the unclassified bundle with its warning, three decision bundles and three overflow lines. Shown decisions 3 (Q-DEMO-01, 20, 02); omitted 16 (Q-DEMO-21 to 35 and Q-DEMO-03), whole bundles in sort order.

```
=== ORCA SNAPSHOT [A:BRIEF] seq 0504 ================= SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z prev-ok 09:00Z window 5m (sample, not an alert)
scope runs run-DEMO-A run-DEMO-B | hosts 1 covered of ? expected
src workers ok 3/3pg | msgs CAPPED 100/100 no-paging | checks ok 09:02Z
cover observed 24 (census unknown) | shown 8 | omitted 16 bundles
attn decisions >=19, unclassified 1, answered-open 1, failing 2, unverified 1
OLDEST observed Q-DEMO-01 2h14m "Approve schema change for T-DEMO-04?"
------------------------------------------------------------------------------
NEEDS YOU  decisions >=19 + unclassified 1 (census unknown)
 ! M-DEMO-140 seen>=32m w-DEMO-04 > ?  T-DEMO-11 run-DEMO-B UNCLASSIFIED
     "Lockfile drift vs main, holding here."
     blocks ? | T-DEMO-11 ready ? | ev M-DEMO-140 (no thread)
   oldest not certified: 1 item(s) lack a creation time
 ! Q-DEMO-01 2h14m w-DEMO-07 > human-DEMO-op  T-DEMO-04 run-DEMO-A
     "Approve schema change for T-DEMO-04?"
     blocks 4 (1 direct, 3 indirect) | ev M-DEMO-118 TH-DEMO-11
 ! Q-DEMO-20 2h05m w-DEMO-06 > human-DEMO-op  T-DEMO-05 run-DEMO-A
     "Pin dependency lib-DEMO at version 4.2?"
     blocks 1 (direct; also under Q-DEMO-01) | ev M-DEMO-108 TH-DEMO-08
 ! Q-DEMO-02   45m w-DEMO-03 > human-DEMO-op  T-DEMO-06 run-DEMO-A
     "Target API v2 or v3 for T-DEMO-06?"
     blocks 1 (direct; shared with Q-DEMO-01) | ev M-DEMO-131 TH-DEMO-19
 +16 decisions observed, not shown (shown 3 + omitted 16 = 19 observed)
   next in order: Q-DEMO-21 (44m) Q-DEMO-22 Q-DEMO-23 Q-DEMO-24 +12 more
   no drill-down is available from this report
ANSWERED, NOT RESOLVED  1  (a reply is not a resolution)
   Q-DEMO-04 1h35m w-DEMO-02 > human-DEMO-op  T-DEMO-08 run-DEMO-B
     human replied 08:55Z "Use the staging bucket."; no resolution seen
------------------------------------------------------------------------------
FAILING / NOT VERIFIED  failing 2, unverified 1               3 shown of 3
 V T-DEMO-03  25m w-DEMO-05 reported complete; checks FAIL 2 of 14 ran
     [claim] [checks@demo-b7:fail] lint-DEMO unit-DEMO-3 | not done
 X A-DEMO-12  24m w-DEMO-12 T-DEMO-10 attempt failed 08:41Z, no replacement
     ev worker-list page 2
 U T-DEMO-02  53m w-DEMO-01 complete (claim only) [claim] | no check seen
------------------------------------------------------------------------------
SINCE 09:00Z (seq 0411)  newly observed Q-DEMO-03 Q-DEMO-34 Q-DEMO-35
  worse T-DEMO-03 checks | resolved Q-DEMO-00 [human] 09:01Z ev M-DEMO-102
WATCH  w-DEMO-09 last evidence 08:49Z (16m, limit 15m); holds T-DEMO-07
FLEET  12 workers listed: live 8, exited 3, unverifiable 1 (w-DEMO-09)
------------------------------------------------------------------------------
cover observed 24 (census unknown) | shown 8 | omitted 16 bundles
legend ?=unknown >=N=lower bound seen>=N=age from first sight ~=last-known
=== END SNAPSHOT seq 0504 ===
```

The oldest observed decision stays in its pinned place; overflow never rotates it away (rule 8). The arithmetic is on screen twice: `shown 3 + omitted 16 = 19 observed` for the section, and `shown 8 | omitted 16` of `observed 24` in the frame. The overflow lines promise no way to see the rest. Q-DEMO-03 is omitted even though it is newly observed, because order is by age, not by novelty; the SINCE strip still names it. Omitted items remain in the next observation's unresolved set; omission does not resolve them.

### 16.2 Budget rules

| ID | Rule |
|---|---|
| FMT-3 (one budget) | One hard budget for every concept and state: at most 60 lines per report, frame included, and at most 78 columns per line. The 78-column width leaves a 2-column wrap margin inside an 80-column monospace block. The frame costs 12 lines, so the body has at most 48. The 40-line target of Variant 1 OVF-8 and the 44-line budget of the base are superseded by this single budget. |
| Precedence | The budget yields only to the oldest complete question and its warning, which are never cut or truncated mid-question (rule 7). If keeping them whole pushes the report past 60 lines, the report prints `over budget: oldest question kept whole` as the line before the footer `cover` line. No other content may exceed the budget. |
| Section budgets | Each concept's body grammar (sections 8.1 to 12.1) allocates the 48 body lines among its sections. A section that exceeds its own budget omits whole bundles, lowest in its sort order first. The pinned oldest observed decision, the pinned verification contradiction and the coverage lines are never omitted. |
| OVF-1 accounting | Every section that omits prints `shown + omitted = observed` in whole bundles; the frame `cover` line prints the same totals for the report. `observed` is always labelled `(census unknown)` while the census is unknown and is never called a total. |
| Omitted keys | Omitted IDs print in sort order on at most one line, with the first omitted ID's age, then `+N more`. If even one line is not available, print the count and the first omitted ID with its age. |
| No drill-down | The report never implies a drill-down, link or archive. It prints `no drill-down is available from this report` until an overflow destination is verified (gate FG-5, section 20). |
| Paging versus overflow | Source paging coverage (`3/3pg`, `PARTIAL`, `more?`) is reported in the `src` line and is distinct from display overflow. A capped read whose section is empty prints `0 observed (partial)`, never an empty section. |
| Transport limit | Whether 60 lines and 78 columns fit one chat message in the target client is unverified (A-003). Closing it is gate FG-11 (section 20); the budget does not assume it. |
| End marker (FMT-7) | A paste that lacks its `=== END SNAPSHOT seq N ===` line, or whose end-marker sequence number differs from the title's, is invalid: the reader must treat it as truncated and must not read absence of rows as absence of items. |

Overflow selection is deterministic: the same model renders the same shown and omitted sets. Severe overflow invalidates the claim that the report alone explains every decision (rule 9); the frame still carries the counts that say so.

## 17. Evaluation
<!-- Source: Variant 2 (sonnet:analyzer), s.9 protocol, s.9.1 reader tasks, s.9.2 mechanical checks and s.9.3 decision rule, with Base s.11 evaluation tasks and future contract cases — merged per Change 11; MC-4 rewritten per Change 13 (invariant INV-006); decision rule reduced to the one switch rule per Change 10 (invariant INV-020) -->

None of these tasks has been run. Targets are initial proposals to be calibrated on a pilot; they are not results and not claims about any concept.

### 17.1 Protocol (proposed)

Synthetic fixtures only (section 7 and the state variations in sections 15-16). Within-subject: each participant sees several concept/state combinations with the order counterbalanced. Participants are people who supervise multi-agent work; at least 8 for a quantitative read, otherwise the result is reported as qualitative with the number of participants. Each measure is reported as a proportion or median with its sample size. No statistical significance claim is made without a pre-stated test and a sufficient sample. Time is measured from first display to a spoken or typed final answer. No transcript drill-down exists in the test, matching the chat setting.

### 17.2 Reader tasks

The last two columns map the earlier task sets onto this one, so no task is lost: Base E01-E07 (five operators) and Variant 1 EV-1 to EV-10.

| ID | Task | Fixture | Measure | Initial target | Base | V1 |
|---|---|---|---|---|---|---|
| ET-1 | Name the id, age and requester of the oldest observed blocking decision | Busy (seq 0412), each concept | Correct answers; time to answer | Every concept at least 90% correct; A median 15 s or less; other medians reported | E01 | EV-1 |
| ET-2 | State what is being asked and who must answer, in one sentence | Busy | Rubric score on action and answerer | At least 90% match the rubric | - | EV-9 |
| ET-3 | "Could there be more open decisions than shown?" | Busy (messages CAPPED) | Share answering yes | At least 95% yes | E02 | EV-2 |
| ET-4 | "Is anything waiting for you?" | Stale (seq 0502) | Share answering "unknown / cannot tell"; any "no" is a critical failure | 100% no critical failures; at least 95% "unknown" | E04 | EV-4 |
| ET-5 | "How many distinct tasks are held by decisions?" | Busy, shared T-DEMO-06 | Exact answer (4) versus double count (5) | At least 85% exact | E05 | EV-6 |
| ET-6 | After viewing report N-1 then N, list what is newly observed, worse, resolved | Two consecutive reports (seq 0411, 0412) | Precision and recall of the list | Precision and recall at least 85% | E07 | EV-7, EV-8 |
| ET-7 | "Is T-DEMO-03 done?" and "Is T-DEMO-08 done?" | Checks failing (seq 0503) | Share answering "claimed done, not verified" | At least 95%; any "done" is a critical failure | E03 | EV-5 |
| ET-8 | "Is Q-DEMO-04 still open?" | Busy | Share answering yes, with reason | At least 90% | - | - |
| ET-9 | "How many decisions are not shown, and can you open them from this report?" | Overflow (seq 0504) | Exact count (16) and "no" | At least 90% both correct | E06 | - |
| ET-10 | Without the source rows, restate the coverage in one sentence | Busy | Rubric: names the capped message source and the unknown host inventory | At least 80% name both | E02 | EV-2 |
| ET-11 | "Is everything fine?" | Empty (seq 0501) and Busy | Share answering with a scope or census qualifier; any unqualified "yes, all fine" is a critical failure | 100% no critical failures | E02-E04 | EV-3 |

ET-11 carries the Base rule that a false all-clear reading blocks the design, and Variant 1 EV-3 (zero unqualified all-clear answers on the empty and partial fixtures). EV-10 (paste width at 80 columns) is a mechanical check, MC-1, plus gate FG-11; it needs no participants.

### 17.3 Decision rule for the default

A remains the default if it meets its ET-1 and ET-4 targets with no critical failure. The only result that changes the default is the one switch rule in section 14: E ties A on ET-1 and wins on ET-6. If A misses its ET-1 or ET-4 target, A's wording is revised and the task re-run; that is not a switch. A critical failure in ET-4, ET-7 or ET-11 disqualifies the concept in that state until its wording is fixed and re-tested. These thresholds are proposals. Record observed task results before claiming an improvement.

### 17.4 Mechanical checks (no participants)

| ID | Check | Pass rule |
|---|---|---|
| MC-1 | Width and character set | Every fenced line 78 columns or fewer (FMT-2); only printable ASCII; no escape bytes |
| MC-2 | Line budget | Every report at most 60 lines, frame included, or the line `over budget: oldest question kept whole` is present (FMT-3); the footer `cover` line states omissions |
| MC-3 | Header completeness | Title with `seq N`; `as-of` with prev-ok, window and sample note; `scope`; `src` with one token per source; `cover`; `attn`; `OLDEST observed`; footer `cover` equal to header `cover`; end marker with the title's sequence number |
| MC-4 | Forbidden wording | In every state, including empty, no screen contains "all clear", "all-clear", "healthy", "no problems", or a bare "none" that is not followed by a scope and the census qualifier. There is no exception for fully paged or all-OK sources (COV-4). |
| MC-5 | Unknown handling | Every `?` or "unknown" field is not rendered as 0, blank or a green word |
| MC-6 | Arithmetic | `shown + omitted = observed` for every capped section and for the frame `cover` line |
| MC-7 | Synthetic marker | Every identifier and name in fixtures matches the DEMO pattern and appears in section 7 or a declared state variation; no real record used |
| MC-8 | No invented metrics | No percentage, cost, token or trend line without a stated source and denominator |

### 17.5 Future contract acceptance cases

Before implementation approval, fixture-based checks are defined for the requirements in section 3. A future renderer must satisfy these deterministic cases:

- Replaying an identical successful observation produces the same item identities and ordering, with only time-derived labels changing as specified.
- A failed middle page or repeated cursor yields partial worker coverage; it does not delete unseen workers or close questions.
- Duplicate worker records do not inflate counts. Conflicting attempt authority is shown instead of arbitrarily choosing a success.
- A capped response omitting an older question retains that question as last-known unresolved, with current status unknown.
- A successful empty worker response plus a failed message response never produces all-clear wording; no input in any state produces it (COV-4).
- Same-task blockers remain separate decisions but contribute one task to the impact union. Cycles produce the label `dependency conflict`, not infinite expansion.
- A stale check, a wrong-revision pass, an unavailable check and a current-revision failure produce four distinct verification labels.
- Scope changes, unknown timestamps and clock conflicts disable unsupported ages and deltas instead of generating negative ages or invented trends.
- Observed actionable bundles beyond a section's budget are accounted for in whole bundles under the 60-line budget (section 16), retain the oldest observed decision and the verification contradiction, and leave unobserved totals unknown.
- Every fenced screen contains only printable ASCII and line breaks, stays within 78 columns, and includes coverage plus omission accounting in the header. No question is cut between its identity and required context.
- A message matching no routine form renders as an `unclassified` row in the decision block, never as a heartbeat (COM-7).
- A collection interruption cannot advance a source's last-success pointer. A rendering interruption cannot publish a half report as a successful snapshot, and a report without its end marker is invalid (FMT-7).
- A transcript containing ANSI sequences, fences, secrets or report-policy instructions cannot break the report or change its rules.

### 17.6 Status

No tests, collector calls, performance measurements or operator trials were performed for this design artifact.

## 18. Limits
<!-- Source: Variant 2 (sonnet:analyzer), s.10 limits and out of scope, with Base s.12 explicit limits and out of scope — merged per Change 1; LOW invariants INV-009, INV-015 and INV-017 recorded as limits per the refactor plan's open-questions list -->

### 18.1 Out of scope

- This deliverable is a design specification, not product code, a data-collection or parsing implementation, an implementation plan, a scheduler, a running observer or an integration benchmark. No scheduler for posting the report every five minutes is designed.
- Controls, acknowledgement, snooze, claim, reply, retry, dispatch, release, terminal attachment or any other write action. The report is read-only and must not consume or acknowledge any mailbox (COM-5, FMT-5). No seen, claimed, snoozed or resolved state is stored for a person.
- The interactive terminal brainstorm, the fork/build recommendation, terminal framework selection, infrastructure topology, storage engine and deployment procedure. Those are separate decisions.
- Web research, Orca commands and live fleet data.
- No API endpoint, durable decision store, overflow archive, independent check feed, expected-host inventory or reliable human-identity service is assumed to exist.
- Evidence references need not be clickable, but must be meaningful to the operator. Naming an unavailable record does not make it inspectable.

### 18.2 Explicit limits of the design

1. Nothing in this document was runtime-validated. Mockup layouts were checked for width and line count with a text tool and for consistency by reading; the comparison ratings in section 13 are judgments.
2. Five-minute sampling can miss any transition that starts and ends between samples. The report is not an urgent-alert channel and says so on line 2 of every report (FMT-6). Event replay, if available later, would need separate verification.
3. The accuracy of decision counts is bounded by the weakest source. Until gates FG-1 and FG-10 close, no decision count is presented as complete and the oldest decision is only `oldest observed`.
4. Hosts: the report covers only what the source reports. Without an expected-host inventory there is no host coverage percentage (gate FG-7).
5. Cost, token, throughput, retry-burden, response-time, utilization, percentage and trend figures are excluded because no verified source or denominator exists (COV-6).
6. Ranking is by age only, with qualified-age items first (DEC-7). The design does not model urgency or priority, because no source for either was verified.
7. Thresholds in the mockups (15-minute worker silence, 30-minute coordinator hold in concept B, the two-interval stale limit) are placeholders, not observed norms; real values need operator input.
8. Chat rendering varies. The design assumes a monospace code fence and gives no guarantee for proportional-font clients; whether one report fits the chat transport is gate FG-11.
9. Transcript or message text may be hostile or malformed. The report shows quoted, truncated text with control characters escaped and never executes or follows it (COM-6).
10. Terminal ANSI colour is an optional export, and nothing in the designs depends on it.
11. No dependency impact is claimed complete without graph completeness (gate FG-3). Unknown owner, age, host, revision or process state stays unknown.
12. **Threshold boundaries are ambiguous (INV-009).** The design does not yet say whether a threshold comparison is inclusive or exclusive: whether evidence exactly two intervals old is stale, and whether WATCH fires at exactly the limit. The mockups show w-DEMO-09 at 16m against a 15m limit, which is beyond the limit under either reading. Proposed rule, not yet adopted: "beyond the limit" means strictly greater than the limit.
13. **Equal-age ordering is only partly defined (INV-015).** Within one ID space, equal ages break ties by stable ID (rule 2). No tie-break is defined across ID spaces (for example a `Q-` decision and an `M-` unclassified item with the same age), or between an exact age and an equal `seen>=` lower bound beyond the DEC-7 rule that qualified ages print first.
14. **Empty bands (INV-017).** An empty band or row prints `0 observed`, or `0 observed (partial)` when a relevant source is capped, failed or stale (COV-3). It never disappears and never reads `none`.

## 19. Risks
<!-- Source: Variant 2 (sonnet:analyzer), s.11 risks RK-1 to RK-15 with requirement IDs remapped to section 3, plus Variant 1 (opus:architect) risks R-3 and R-8 and Base s.12 risks and mitigations — merged per Change 1 and Change 11 -->

Likelihood and impact are judgments, not measurements. RK-1 to RK-15 come from one risk register; RK-16 to RK-21 add risks the other sources named that the register did not cover. Wording already covered by an RK row was folded into that row.

| ID | Risk | Likelihood / impact (judgment) | Mitigation | Requirement |
|---|---|---|---|---|
| RK-1 | The decision source is capped, so a real decision is missing and the report looks complete | High / High | `>=N` and `observed (census unknown)` on every count; `CAPPED` and `no-paging` in the `src` line; `OLDEST observed`; MC-4; gates FG-1, FG-10 | DEC-3, DEC-4, COV-4 |
| RK-2 | A failed collection is mistaken for a calm fleet | Medium / High | Distinct `FAILED` and `STALE since T` labels, last-known bundles with `~` under the banner, no delta, fleet `?` (section 15.2); ET-4 | CHG-2, COV-3, COV-5 |
| RK-3 | A delta against a partial baseline reports phantom resolved items | Medium / Medium | Only a fully successful collection becomes a baseline; partial reads give only `newly observed` additions; the gap is stated (rule 4) | CHG-1, CHG-2, CHG-5 |
| RK-4 | A worker claim of completion is read as done | High / High | `[claim]` label, `complete (claim only)`, checks with revision and time, `not done`; ET-7 | VER-1, VER-3, VER-4 |
| RK-5 | Checks bound to an old revision look current | Medium / High | Revision and time shown; `verification unknown: revision mismatch` (section 15.3); gate FG-2 | VER-2, VER-3 |
| RK-6 | Root-blocker grouping hides a distinct decision or double counts a task | Medium / Medium | One row per decision; shared tasks counted once in the union; ET-5 | BLK-2, BLK-3 |
| RK-7 | A reply is read as resolution, so an answered question vanishes | Medium / Medium | ANSWERED, NOT RESOLVED band; only a resolution linkage removes a row; INV-021 open | DEC-6, COM-2 |
| RK-8 | Overflow hides the most important items | Medium / High | Qualified-age items first, oldest observed pinned; omitted IDs listed; arithmetic shown; failing and unverified shown before the cut | OVF-1, FMT-3, MC-6 |
| RK-9 | The report becomes noisy and operators stop reading it | Medium / High | Heartbeats collapse by explicit routine forms; one 60-line budget; stable placement. The `unclassified` fallback adds noise by design (COM-7); routine forms are tuned under gate FG-9, never by hiding rows | COM-4, COM-7, FMT-3 |
| RK-10 | Hostile message text injected into the report misleads the reader or the chat client | Low-Medium / High | Quote, truncate, escape control characters and fences, redact and mark secrets; never act on it | COM-6 |
| RK-11 | Placeholder thresholds (15m silence, 30m coordinator hold) are taken as facts | Medium / Low | Thresholds printed in the report and flagged as placeholders (section 18.2, limit 7) | CHG-6 |
| RK-12 | A reader has learned one layout and an alternate concept confuses them | Low / Medium | One default; alternates as companion views only; same frame, symbols and wording | Section 6, section 14 |
| RK-13 | Mockup numbers are mistaken for real data | Low / Medium | `SYNTHETIC DEMO DATA` in the title and DEMO in every ID; MC-7; no cost or percentage | SYN-1, COV-6 |
| RK-14 | The design is mistaken for validated | Medium / Medium | Section 17.6 status statement, limit 1, ratings labelled judgments | Section 17, section 18 |
| RK-15 | A stale `~` row misleads in the other direction: a question already answered shows as open | Medium / Low | Banner says `not confirmed current`; the report never silently drops the row | DEC-6, COV-1 |
| RK-16 | Derived keys change between reports, so a decision reappears as new and an old one as vanished | Medium / Medium | `id:derived` tag; VANISHED only after a full read and never as resolved; prefer source-native IDs (section 6.4); INV-004 open | CHG-3, SYN-1 |
| RK-17 | Renderer drift: each concept reimplements the honesty rules differently | Medium / High | Shared frame and single derivation layer (section 2); renderers cannot compute coverage | FMT-8, COV-1 |
| RK-18 | Pagination races or cross-source skew duplicate work, miss records or mislead about readiness | Medium / High | Deduplicate by identity; show collection intervals and evidence revisions; exhausted paging is an observation property, not a census (gate FG-14) | BLK-6, COV-7 |
| RK-19 | Incorrect authority or identity mapping lets an old attempt's claim override a current failure | Medium / High | Attempts kept separate; authority conflicts shown; provenance retained (gate FG-4) | BLK-6 |
| RK-20 | Evidence drift: a pass on an old revision becomes a readiness claim | Medium / High | Match subject, current revision, evidence kind and policy; stale or mismatched evidence prints unknown | VER-2, VER-3 |
| RK-21 | A long outage or missing history makes the last-known unresolved set grow or age without confirmation | Low / Medium | Confirmed-current kept apart from unconfirmed history; pending items never evicted silently to imply resolution; retention policy is part of gate FG-6 | DEC-6, COV-1 |

## 20. Gates and open questions
<!-- Source: Variant 2 (sonnet:analyzer), s.12.1 feasibility gates FG-1 to FG-8 including FG-8 Cannot ship, cross-mapped to Variant 1 (opus:architect) s.17 G1-G8 and Base s.12 G01-G08 — merged per Change 11 (invariant INV-029); FG-9 per Change 12, FG-10 per Change 16, FG-11 per Change 14; open questions per the refactor plan's open-questions list -->

### 20.1 Feasibility gates

A gate is closed by verifying a source, not by assuming one. While a gate is open, the dependent claim is printed only with its marker, or not at all. **A gate blocks shipping the dependent claim, not design exploration:** every concept in this document can be designed, mocked and evaluated on synthetic fixtures with all gates open (INV-029). FG-8 is the one gate that blocks shipping the report itself.

| Gate | Question | If open | Closing evidence | Concepts affected | Cross-map |
|---|---|---|---|---|---|
| FG-1 | Which complete, non-consuming source enumerates durable pending human decisions, with stable identity, original time, actor and explicit resolution linkage? | Counts print `>=N observed`; only an observed-attention design ships; the global oldest or every pending decision is never promised | A read-only source with paging and a known total, or a documented guarantee that the read covers all pending items | All; A least | V1 G1, Base G01 |
| FG-2 | Where do revision-bound check results and independent review records come from? | Verification lines show `?` or `complete (claim only)`; no invented check results or ready totals | A source that names subject, revision, result, time and reviewer | A, B, E verification lines; C OTHER ROOTS | V1 G6, Base G03 |
| FG-3 | Is a task dependency graph readable, and how complete is it? | `blocks ?`; C degrades to decision roots with `deps?` | A graph source with a coverage indicator | C; `blocks N` in A, B, E | V1 G4 |
| FG-4 | Which identities distinguish requester, acting owner, answerer and resolver, and can human-seen or human-claimed state be read per person (not the transport read flag)? How are cancellations and superseded questions represented? | Owner prints `?` when missing; communication states stay separate; no seen, claimed or snoozed state shown | Per-person ownership and resolution state from a named source | B owner bands; D ladder; ANSWERED, NOT RESOLVED band | V1 G8, Base G05 |
| FG-5 | Does any drill-down or complete read-only pending list exist for omitted rows? | Overflow prints `no drill-down is available from this report`; no link invented | A named, verified read-only command or view | Overflow in all concepts | Base G06 |
| FG-6 | Is the last successful observation stored durably, with gaps recorded, and what retention budget applies to unresolved history? | No delta (`n/a (no baseline)`); E has no TRAIL; no long-term carry-forward or trend claimed | A persisted baseline with a success flag and gap records, kept without touching source state | E; SINCE strip; RK-21 | V1 G7, Base G07 |
| FG-7 | Is there an expected-host or expected-workspace inventory, and who defines intended hosts and runs? | `N covered of ? expected`; named scope only; no coverage percentage | An inventory the report can compare against | `scope` frame line | V1 G3, Base G04 |
| FG-8 | Can the report be produced without consuming or acknowledging any mailbox? | **Cannot ship** | Evidence that every read used is non-consuming and idempotent | All | - |
| FG-9 | Are the explicit routine message forms complete and stable enough to classify heartbeats? | Every unmatched message is an `unclassified` row (COM-7); noise is accepted | A documented, closed list of routine forms checked against observed message samples | All decision blocks | new (Change 12) |
| FG-10 | Does the decision source offer paging or a cursor that reaches the oldest pending decision? | The OLDEST line keeps `observed`; no claim of the oldest decision | A paging or cursor mechanism plus a complete census (FG-1) | All OLDEST lines | new (Change 16) |
| FG-11 | Does one report of 60 lines and 78 columns fit one message in the target chat client? | The budget stands but is not claimed to fit; a paste without its end marker is invalid | A tested paste in the target client | All | new (Change 14, A-003) |
| FG-12 | Which sources expose delivery facts (enqueued, delivered, processed, answered, resolved) per thread? | Ladder cells print `?`; D is not viable as default | A source per fact, per thread | D ladder | V1 G5 |
| FG-13 | Do decision and thread records carry source-native stable identifiers and original creation times? | Derived keys tagged `id:derived`; ages from first sight (`seen>=`) | Source-native IDs and creation times on every record | All rows; E deltas | V1 G2 |
| FG-14 | Do opaque worker cursors enumerate a stable version during insertions, supersession and cursor expiry? | Exhausted paging is reported as an observation property, not an exact point-in-time census | Documented cursor semantics | `src` frame line; fleet counts | Base G02 |

Two earlier items are not gates here. Base G08 (density decision) is an evaluation question, settled by section 17 and the one switch rule in section 14. Variant 1 G1 listed "the complete-coverage empty-state wording" as unlocked by a complete decision source; under COV-4 no gate unlocks any all-clear wording, so closing FG-1 changes `>=N observed` to exact counts only.

### 20.2 Open questions

Each question below is undecided. The interim rule is what this document's screens do until it is decided.

| ID | Question | Interim rule |
|---|---|---|
| INV-001 | A partial read can mark an item `newly observed`, but the last-success pointer does not advance (rule 4), so the same item is `newly observed` again in the next comparison. Should the second report suppress it, and how? | Repetition is accepted. The SINCE strip names its baseline time and sequence, so the reader can see that the comparison did not move. |
| INV-002 | What does a report print on the first run, or when the observation store is empty and the first collection fails? | Section 15.2: banner `No last-known records available`, `cover` and OLDEST read `? (no successful read yet)`, no `~` bundles. |
| INV-004 | An observed candidate question with uncertain identity (section 4) reappears as new every report, can never link to a resolution, and stays last-known indefinitely. How does it age out, if ever? | It stays visible with `id:derived` and is never closed by disappearance (rule 3). Visible noise is preferred to a hidden decision. |
| INV-021 | Do ANSWERED, NOT RESOLVED items count toward the decision count (DEC-1, DEC-4) and the OLDEST line? This matters: Q-DEMO-04 (asked 07:30Z) is older than Q-DEMO-02 (08:20Z). | Shown in their own band directly under the decision block, counted on the `attn` line as `answered-open`, not counted as decisions and not eligible for OLDEST. |
| INV-022 | WATCH uses the worker's last evidence time, not the collection time. How should WATCH read when collection itself is stale or failed? | Evidence time, as in the fixture (`last evidence 08:49Z`); when the source was not refreshed, the WATCH row is marked `~` and its age advances by wall time (section 15.2). |
| INV-023 | Redaction of a secret can change what a question asks. How is the reader told? | Redaction is marked `[redacted]` in place (COM-6). Where the redaction removes part of the question, the row must say that its meaning may differ from the original; the exact wording is undecided. |
