# Summary

Choose C, Decision Desk: one selected human question beside its explicitly linked evidence.
Its narrow evidence boundary avoids pretending that a fleet overview proves an outcome.
Build the offline decision workflow first; today’s live mode can show workers, not verified questions.
Release live questions only after their identity, meaning and affected-dispatch links are verified.
Use Python Rich in this repository; keep every count scoped, every refresh bounded and every action local.

# First buildable slice

The unit of inspection is a question plus a justified set of dispatches, not a worktree.
This is C, not a fleet dashboard with a question banner attached.
The existing composition selects a request, filters affected sessions and counts other questions.
Its fixture request schema is PROPOSED; no production parser may assume that schema exists in Orca.

Proposed screen contract, tested at 44 rows; shorter terminals scroll within the focused panel.
- At 160 columns: 76-cell request panel left, 80-cell affected-evidence panel right.
  Other observed questions sit below the request; a full-width source strip precedes the footer.
- At 116 columns: 114-cell request above a 66-cell evidence ledger and 46-cell other-questions panel.
  The source strip remains full width; longer identifiers move to the detail view.
- At 80 columns: 78-cell request, then a 78-cell affected ledger, then other questions.
  Each section has a visible capacity count; vertical overflow is scrollable, never silently discarded.
- All widths: selected-question identity, source scope and collection age remain visible.
- A local detail screen shows full IDs, raw state labels, timestamps and association provenance.
- Tab changes panel; arrows move selection; Enter inspects; Escape returns; export copies no commands.
  These are proposed inspection keys, not Orca verbs; input must restore terminal state on exit.

Offline mode is prominently marked SYNTHETIC, with no automatic transition to live data.
Today’s live mode replaces the request with “Question source UNVERIFIED” and offers worker inspection.
It shows “Affected scope unknown”; it must not relabel all observed workers as affected evidence.
The complete decision-first live MVP is blocked until the question-link contract is verified.
That honest gate is preferable to shipping a persuasive but invented decision desk.

# Verified sources needed

The seed brief is the contract baseline verified on 2026-11-08, not a promise of future CLI stability.
Only these live read surfaces are eligible; no live CLI call was needed to write this proposal.

1. `orca orchestration worker-list --json` supplies `result.workers[]`.
   Identity/state: `dispatchId`, `taskId`, `runId`, `workerState`, `dispatchStatus`,
   `agentTerminalHandle`, `terminalState`.
   Resource: `resource.{id,ownershipState,releaseState,worktreeId,ownerDispatchId,`
   `originDispatchId,recoveryAttemptCount,terminalHandle}`.
   Projection: `projection.stage.{worker,dispatch,activity,detail}`;
   `projection.liveness.{verdict,source,observedAt}`;
   `projection.evidence.{durable,liveStatus,lastObservedAt}`;
   `projection.outcome`, `projection.nextAction.kind`, `projection.host.{id,kind}`,
   `projection.workspace.{id,kind}`, `projection.provider.id`, `projection.role`.
   Collection: `result.page.{limit,total,hasMore,nextCursor}`, `result.scope.source`,
   `result.counts.{active,reclaimable,retained,released}`, `result.warnings[]`.
   Page limit is 1–100; continuation argument spelling must be verified before implementation.
2. `orca orchestration check --peek` and `orca orchestration check --all` are non-consuming.
   Empty-peek JSON establishes only `result.{count,dispatchId,runId}`.
   `--all` and a Run `--peek` return at most 100 rows; message row fields are UNVERIFIED.
   Target-selection and JSON-option invocation details also need verification before execution.
3. `orca orchestration inbox` has `--limit`, `--terminal`, `--full`, but its JSON shape is UNVERIFIED.
   It is not an MVP parser dependency and is not used as an alternative history feed.

Terminal state is process accounting, not task outcome; `projection.outcome` is not human acceptance.
The static design’s `totalCount` wording is superseded by the seed’s verified `page.total`.

# Shown as unknown / stale / partial

UNKNOWN means not established; UNAVAILABLE means no usable source; neither means false or zero.
STALE means a retained observation is older than the proposed 30-second freshness budget.
PARTIAL means collection coverage is bounded or pagination did not finish consistently.
Show these words, the last successful collection time and the source scope without relying on color.
A fresh fetch with old evidence remains “collection fresh / evidence stale.”
A failed fetch retains last-known observations with a failure badge, never a fabricated empty fleet.

Keep lifecycle, report status, acceptance, tests and human approval in separate fields.
Only lifecycle/process and supplied projection values have today’s verified worker source.
Report validation, test result, revision match and human approval therefore display UNKNOWN.
Literal policy-frozen evidence stays frozen; missing freeze evidence displays UNKNOWN, not unfrozen.
No cost feed means “cost unavailable,” never $0; no token-to-progress conversion is allowed.

Proposed denominator wording:
- “Showing 6 / 9 observed affected dispatches; 2 linked IDs not observed.”
- “Filter matches 20 / 80 observed dispatches; source reports 287 total in this scope.”
- “Collected 80 unique / reported 287; PARTIAL”; do not call 287 the fleet across all hosts.
- Counts supplied by `result.counts` are labeled source-reported with `result.scope.source`.
  They are not added to page-derived counts or assumed to describe the selected filter.
- “Other observed questions: x / y shown”; y excludes the selected question and names its scope.
  For example, 2 / 7 means two displayed from seven other observed questions, not seven globally open.
- Before question parsing is verified: “Other observed questions: unknown / unknown.”
- Once verified: “At most 100 message rows per read; total question coverage unknown.”
  One hundred message rows are not necessarily one hundred questions; fewer rows do not prove completeness.

# Deliberately left out

- No approve, answer, acknowledge, retry, terminate, spawn, merge, rebase or delete-worktree controls.
  Read-only remains a command allowlist, not a disclaimer over hidden mutation paths.
- No plain `check`, no `--ack`, and no automatic “mark seen” interaction with Orca.
- No inferred human question classifier over free text, and no LLM polling or summarization loop.
- No complete open-question inventory or durable message history claim from a capped read.
- No cross-host ownership inference from matching worktree names, paths, terminal labels or task IDs.
- No native terminal/worktree deep links; full identifiers are inspectable as inert text.
- No cost estimates, utilization gauges, progress bars or fleet health score without source contracts.
- No admission, passing-test or acceptance badge inferred from worker completion or report presence.
- No durable event store, SQLite service, background server or external network listener in the slice.
  Session-local snapshots support comparison, not replay or an audit trail.
- No production import of the synthetic fixture schema, renderer or AGPL TUIBBS-scp code.
- No parallel stack implementations: the comparison ends in one proposed implementation path.
- No automatic source discovery across hosts or unbounded per-terminal collection fan-out.

# Where A (Signal Bridge) and B (Attention Ledger) are stronger

A is stronger when the human asks “What changed across my fleet?” before choosing a question.
Its source-freshness area and session ledger are useful even without a verified question feed.
At 160 columns its built layout also has a dedicated SIGNALS panel.
At narrower widths it collapses rather than retaining the same full signals composition.
A could therefore ship a more useful live worker-only view sooner than C.

B is stronger when the bottleneck is finding the oldest unanswered request among many owners.
Its requester/owner/affected-ID rows and retained-context list make queue review more efficient.
“Seen is not resolved” is a valuable invariant C adopts, not evidence that closure is available.
B’s age ranking and persistent open-question claims still need verified question and closure semantics.

C wins for the chosen job: inspecting the evidence needed for one human decision.
It reduces incidental fleet reading and exposes weak associations directly beside the request.
It loses breadth and cannot honestly bypass the same missing message contract that limits B.

# Build order from MVP to later releases

Release 0 — offline Decision Desk walkthrough; gate: OFFLINE-FIXTURE contract reviewed and labeled.
Verify the proposed request identity, explicit affected IDs, missing-data states and export behavior.
Owner chooses C before production integration; fixture success is not a live-source acceptance pass.

Release 1 — worker-only live evidence preview; gate: WORKER-SNAPSHOT contract.
The existing worker fields are verified; continuation invocation and error fixtures must be pinned.
Without verified continuation invocation, collect one page and disclose partial coverage.
Ship question/association panels as unavailable, not synthetic live content.

Release 2 — first complete live Decision Desk MVP; gate: QUESTION-LINK contract.
Observe non-empty non-consuming rows and verify stable identity, question type, original timestamp,
requester, responsible owner, source handle/run scope and explicit affected-dispatch references.
Unknown optional values are acceptable; an absent question identity/type contract is not.
If affected references are absent for a particular question, show unknown scope and no affected ledger.
Bounded observed questions may ship only if the owner accepts the explicit 100-row coverage warning.

Release 3 — retained queue and cross-owner breadth; gates: QUESTION-CLOSURE and OWNERSHIP-JOIN.
Add B-style aging and verified resolution; add A-style owner rollups only for authoritative joins.
Complete backlog claims additionally require COMPLETE-MESSAGE-ENUMERATION, not just closure fields.

Release 4 — richer decision evidence; gates: REVISION-VERIFICATION and ADMISSION-HUMAN-LINK.
Only then add revision-pinned tests, validated report/admission evidence and approval attribution.
Cost or history views require separate COST-COVERAGE and DURABLE-REPLAY contracts; they are not MVP promises.
Every gate needs representative success, missing, stale and contradictory source samples plus parser tests.

# Stack recommendation

Recommend Python Rich, within the existing Python CLI; this intentionally differs from the issue’s Go preference.
The seed’s dated research table is the comparison baseline, not a fresh dependency/version certification.

| Choice | License/toolchain | Maintenance cost and fit |
|---|---|---|
| Go Bubble Tea v2 / Lip Gloss v2 / Bubbles v2 | MIT; new Go toolchain and platform binaries | Strong focus/list widgets; lower upstream maintenance risk, but a second language and release pipeline here. |
| Python Rich | MIT; existing dependency/toolchain | Best repo fit and text export; medium upstream risk; custom keyboard handling is the main additional burden. |
| Python Textual | MIT; new pure-Python dependency | Better built-in focus and headless tests; medium community-maintenance risk; plain-text export remains UNVERIFIED. |
| Rust Ratatui | MIT; new Rust toolchain plus binary or maturin | Strong lists and text snapshots; low-medium pre-1.0 risk, highest language mismatch for this slice. |
| TUIBBS-scp | AGPL | Excluded as implementation source; no copied code, regardless of the underlying MIT libraries. |

Seed comparison versions are Go 2.1.1 / 2.0.6 / 2.2.1, Textual 8.2.8, Rich 15.0.0 and Ratatui 0.30.2.
The reference manifest’s Go pins 2.0.6 / 2.0.3 / 2.1.0 are different; neither set is a proposed latest-version claim.
Go’s reported boolean NO_COLOR parsing needs an application override for any nonempty value, including “yes.”
Its text export and wide-character behavior need explicit validation; widgets do not settle those contracts.
Rich supplies width measurement and recorded text export, but current house views do not solve keyboard input.
Budget a small, tested terminal-input boundary; do not pretend Live alone provides stable selection.
Reuse house rendering/failure patterns, not their length-based truncation or incomplete sanitizer.
Choose Textual instead only if a keyboard/terminal restoration spike exceeds the agreed maintenance budget.
Choose Go only if the owner explicitly funds its packaging/toolchain ownership; do not build both first.

# Smallest trustworthy read-only adapter

This is a proposed application contract, not a claim that Orca returns these normalized names.
Use one collector and one immutable published view; rendering never invokes the CLI.
Reuse existing `_find_orca()` discovery from `cli/install_user_setup.py` rather than trusting PATH’s `orca`.
The seed records its `orca-ide`/`orca` candidates, `skills list --json` validation and 10-second timeout.
Keep discovery bounded at startup; a missing or wrong executable becomes a source error, not a crash loop.
Use argv arrays, no shell, no interpolated terminal commands, and a strict read-verb allowlist.
Worker listing is enabled now; message reads remain disabled until QUESTION-LINK and invocation tests pass.
Never execute plain `check`, append `--ack`, or execute `projection.nextAction.kind`.

Proposed normalized records:
- Observation envelope: source identity/scope, local generation, collection start/end, last success,
  freshness, coverage status, reported total, collected unique count, warnings and sanitized error class.
- Worker identity: source namespace plus `dispatchId`; retain `runId` and `taskId` as nullable references.
- Worker process facts: separate `workerState`, `dispatchStatus`, `terminalState`, terminal handles.
- Worker resource facts: preserve the resource block; do not rename `ownerDispatchId` to “human owner.”
- Worker projection facts: preserve stage, liveness, evidence, outcome, host/workspace, provider and role.
- Verification slots: report validation, acceptance, tests and human approval are independently UNKNOWN.
- Each optional fact distinguishes absent, explicit null, valid value and invalid value.
- Proposed question record: stable source-scoped question ID, text, requester, owner, original time,
  explicit affected-dispatch references, closure evidence and provenance; all need QUESTION-LINK verification.
  These names describe requirements, not known message row JSON keys.
- Proposed association: question ID, affected dispatch ID, source scope and explicit-link provenance.
  A task ID, shared worktree, matching title or proximity in time is not enough to create this edge.
- When message fields are UNVERIFIED, there are no live question records or association edges.
  Never let an unknown link set become an empty-but-complete set of affected sessions.

Deduplication and ordering:
- Dedup worker rows by source namespace plus `dispatchId`, never by task, worktree or terminal handle.
- Missing dispatch identity quarantines the row, increments a rejected-row count and marks coverage partial.
- Order liveness facts by valid `projection.liveness.observedAt` within the same dispatch/source.
- Order evidence facts separately by valid `projection.evidence.lastObservedAt`; do not conflate the clocks.
- An older component cannot overwrite a newer component; missing timestamps cannot prove recency.
- Identical duplicates collapse; conflicting equal-time facts become a visible conflict, not last-row-wins.
- Untimestamped conflicts retain qualified last-known facts; show newest fetched raw state as unsequenced.
- Display ordering is stable dispatch ID unless the human selects an explicit age sort; missing ages sort last.
- Question dedup/order needs verified identity/time semantics; never synthesize IDs from message text.
- Refreshing identical input changes only collection metadata, not facts, selection, counts or change badges.
- “Since last look” compares local accepted observations only; first observation is a baseline, not an event.
  Missing rows in a later partial page are “not reobserved,” not deleted, completed or resolved.

Bounded collection and publication, proposed defaults:
- One cycle at most every 15 seconds, no overlap and at most four worker pages of at most 100 rows.
- After the message gate, allow one selected source’s non-consuming read per cycle, at most 100 rows.
  Other question scopes remain unobserved; never suggest this is fleet-wide message coverage.
- At most five subprocesses, two seconds each, ten seconds total and 8 MiB stdout per cycle.
  A timeout kills/reaps that child; manual refresh coalesces rather than creating parallel subprocesses.
- Follow `nextCursor` only after its invocation contract is verified; reject repeated/missing cursors.
- Check `page.total` and `hasMore` on every page; dedup counts before computing coverage.
  Exhaustion with matching totals means traversal complete for that source, not an atomic cross-host snapshot.
- Changing totals, continued `hasMore`, page-limit exhaustion, rejected rows or read failure mean PARTIAL.
- Publish each bounded generation atomically with its coverage label; never display half-decoded new rows.
- Keep last successful view on decode/exit failure; back off to 30 then 60 seconds and show STALE after 30.
- Validate envelope/types and bound strings before normalization; unknown enum values remain unknown labels.
- Keep snapshots in memory only; diagnostics include duration, counts and errors, not full message bodies.

# MVP acceptance tests mapped to each issue acceptance criterion

Mapping below covers the issue requirements as represented in the seed, not invented verbatim AC numbers.
The issue body was not fetched; exact issue-numbered traceability needs a later owner-provided AC cross-check.
All are proposed tests, not claims of execution; synthetic passes cannot clear live-source gates.

| Seed-carried issue criterion | Required acceptance evidence |
|---|---|
| One human supervises many orchestrators/workers | Base 8 orchestrators / 80 workers, then all nine 5/8/10 × 50/80/100 combinations; exact unique counts and bounded collection. |
| Human attention with reasons | Fixture question, requester and reason stay visible at all widths; live mode remains UNVERIFIED until QUESTION-LINK samples pass. |
| Affected scope | Explicit affected IDs select exactly their dispatches; unresolved references are counted; missing links produce UNKNOWN scope, not all workers. |
| Inspectable supporting evidence | Detail exposes full stable IDs, source, timestamps and distinct process/outcome/verification fields; no completion-to-approval inference. |
| Meaningful changes since last look | Same snapshot twice adds no change; newer liveness/evidence updates only their own fields; first collection is a baseline. |
| Unknown, stale and partial disclosed | Missing field, timeout, parse error, source loss, page drift and incomplete traversal each show explicit status and last success. |
| Verified outcomes distinct from activity | Running, exited, reported, accepted, tests and human approval vary independently; absent verification stays UNKNOWN. |
| Scope/count clarity | Filter/global denominators and source scope remain visible; other questions show x/y; message row cap never becomes total-question count. |
| Responsive terminal inspection | At 160/116/80 columns and reduced heights, selection stays anchored to stable ID; full identifiers remain available in detail. |
| Accessible, safe output | NO_COLOR, ASCII/text export, display-cell clipping and hostile terminal sequences preserve the same facts without terminal side effects. |
| Strictly read-only operation | Captured argv contains only allowed reads; no plain check, ack or operational verb on keypress, refresh, export or failure recovery. |
| Human design selection before integration | Written owner choice precedes live integration; offline walkthrough is separately labeled and accepted. |

Additional test obligations, across the matrix where relevant:
- Uneven ownership: one owner has most workers; owner totals never assume equal distribution.
- Shared/unmapped worktrees: two dispatches share a worktree, one has none; neither is collapsed or assigned an owner by location.
- Historical records: retained/released dispatches stay distinct from active and from current question scope.
- Duplicate/out-of-order input: duplicate rows across pages, opposite page orders and repeated generations preserve counts and newer component facts.
- Conflicting timestamps: equal-time contradictions, missing times, invalid times and future clock skew display uncertainty, never negative age.
- Paging: totals 0, 80, 100 and above 400; repeated cursor, hasMore without cursor, shifting total and child failure retain correct coverage labels.
- Message boundaries: empty peek does not clear an observed question; 99 and 100 rows both retain unknown completeness.
- Question retention: disappearing unread rows do not mean resolution; source loss keeps last-known items stale within this session.
- Missing fields: no dispatch ID quarantines; no owner, role, resource, time or verification field becomes zero/false or a guessed join.
- Injection: ESC/C1 CSI, OSC hyperlinks/clipboard/title, unterminated OSC, carriage returns, bare controls and bidi/Cf spoofing are neutralized.
  Treat external strings as literal text, not Rich markup; never execute or emit their control sequences.
- Width: CJK wide cells, combining marks, emoji, long IDs and control-stripped text cannot overrun a panel or split an escape sequence.
- NO_COLOR: unset, empty, “1” and “yes” cases; every nonempty value disables color, with labels still understandable.
- Export: plain ASCII-safe text contains full IDs, source times, caveats and denominators; no ANSI/OSC or live links; no SVG required.
- Operations: timeout/reap, malformed/oversized JSON, binary discovery failure, broken output and Ctrl-C restore the terminal and preserve read-only guarantees.
- Performance: all scale fixtures finish within the proposed collection budget; UI accepts inspection while a bounded read is outstanding.

# Open owner decisions

1. Select the MVP direction before production integration.
   Recommendation: choose C for decision inspection and accept its deliberate loss of fleet density.
2. Accept a staged release rather than pretending live questions are already available.
   Recommendation: approve offline C first; permit worker-only preview, but reserve “live Decision Desk MVP” for Release 2.
3. Accept or reject a bounded observed-question product when complete history is unavailable.
   Recommendation: accept explicit per-source 100-row coverage limits; reject claims of a complete open queue.
4. Decide production placement and who owns its toolchain.
   Recommendation: an in-repository Python CLI surface using Rich, not a separate Go binary/repository.
5. Set the human-facing freshness tolerance and collection budget.
   Recommendation: begin with 15-second cycles and a 30-second stale threshold; tighten only from measured need.

Verifying JSON shapes, cursor syntax and join semantics are engineering obligations, not owner preference votes.
The owner cannot make an UNVERIFIED contract true by approving the visual design.

# Risks and UNVERIFIED items

The largest risk is product validity: C requires trustworthy question-to-evidence links that are not verified today.
Do not substitute a title match or worktree join to get a more attractive screenshot.
Message row identity, question classification, requester/owner attribution, timestamps and closure are UNVERIFIED.
So are inbox JSON, complete history, cross-host ownership joins, admission/revision evidence and human-owner linkage.
Cost/usage coverage, durable replay/ordering and native deep links remain UNVERIFIED and excluded.
Worker pagination is verified structurally, not as a transactional snapshot; cross-page drift remains possible.
Raw lifecycle changes without timestamps cannot be reliably sequenced; label them rather than claiming event order.
Question memory is session-local; restart loses “since last look,” and retained items must not imply durable history.
Any future retention cap must disclose omitted historical items, never silently mark them resolved.
Rich keyboard input, sanitization and terminal restoration are implementation risks requiring tests, not existing capabilities.
The seed’s stack research and prototype test count are inherited evidence, not fresh dependency or production certification.
Exact issue-body acceptance wording was not read; the acceptance table is explicitly limited to the seed’s representation.
This proposal changes only the requested specification; no implementation, live collection or test run was performed.
