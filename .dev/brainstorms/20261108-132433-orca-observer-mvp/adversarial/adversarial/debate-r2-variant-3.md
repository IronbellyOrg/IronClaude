# Round 2 Rebuttal: Variant 3 (Decision Desk)

## Rebuttals to Criticisms

This is C's backend rebuttal, based on the supplied diff, all three Round 1 arguments and A/B's Round 2 documents. References use section names and criticism numbers rather than claiming new source inspection. The design schema is PROPOSED, not an Orca API. The verified baseline is paged `worker-list --json`, `result.page.{limit,total,hasMore,nextCursor}` with limit 1–100, and non-consuming `check --peek` / `check --all` capped at 100 rows. Message row fields and inbox JSON remain UNVERIFIED. No Orca command was run.

### A-1 / B-1: two unknown panels and no distinctive worker-only product

Conceded as a delivery argument. A is the better default while only worker listing is usable; C's preview should not rebuild a weaker fleet screen around two large notices. Accept A/B's Round 2 worker-ledger default, compact question-source warning and scoped source counts. The synthetic Decision Desk remains a design walkthrough, not a live capability claim.

Also accept a retained question list before affected links verify. This is a further concession: my Round 1 still required link semantics for complete C, and allowed individual missing links, not an entirely unverified link contract. Split the gates now: verified question identity/classification and invocation permit a bounded question preview; verified explicit-link semantics permit the complete Decision Desk. Unknown scope never populates an affected ledger. A/B are right that useful discovery need not wait; that does not make evidence inspection redundant once links exist.

### A-2: multi-panel focus and scrolling exceed an unproven Rich key reader

Agreed; my Round 1 already conceded the interaction spike. A/B's Round 2 height contract without simultaneous scrolling panes is the smaller preview: minimum rows, disclosed overflow and one focused list/detail screen. Keep C's side-by-side composition as the target, not a promise that Rich supplies its interaction model. Test input, redraw, resize, interruption and restoration together. If this requires a custom widget system, use Textual for interaction while retaining the pure text renderer/export. Do not implement both stacks. This is a proposed switch rule, not verification of Textual's export contract.

### A-3 / B-3 / B-5: tight timeouts and one selected scope leave freshness undefined

Correct. Two seconds per child, ten seconds per cycle and a thirty-second row-age verdict were unmeasured proposals. Keep finite call/time/output budgets, single-flight collection, atomic publication, timeout kill/reap and coalesced refresh; set timeout/deadline values only after representative latency measurements and acceptance of the budget. One successful call is evidence, not tail-latency certification.

Replace selected-source-only polling with fair round-robin among explicitly configured, invocation-verified message scopes. After the question gate, reserve at most one message read per cycle under the five-child ceiling; allow at most four worker-page reads and disclose unfinished traversal. Selection cannot reset or monopolize message rotation. Show each scope's last successful read, never-read state, deferred count and failures. With ten eligible scopes and fifteen-second cycles, nominal revisit time is 150 seconds before failures/backoff; retention preserves already observed questions, not unseen ones.

B's Round 2 rate argument identifies a real risk, but `average rate × rotation time < 100` is not a completeness proof: bursts and unverified window/ordering semantics can still lose unseen rows. Message rates, row ordering, targeting and coverage semantics are UNVERIFIED. Measurements inform the budget; they do not establish complete enumeration. Adopt rotation only as bounded best effort, never as a complete backlog feed.

### A-4: continuation verification is a cheap gate, not permanent one-page scope

Agreed. A/B report help evidence for `--cursor`; I did not inspect that help here and do not turn their report into a newly verified invocation contract. Pin continuation spelling and a multi-page sample in WORKER-SNAPSHOT, then use repeated/missing-cursor rejection and PARTIAL fallback. C's one-page rule is failure behavior, not the desired steady state. `page.total`, not `totalCount`, is the source-reported denominator; completed traversal is not an atomic cross-host snapshot.

### A-5 / B-7: weak test traceability, unnamed harness and flat structure

Conceded in Round 1 and made explicit. Adopt B's criterion/test IDs and fake subprocess runner on permissioned, redacted samples; A's recorded-console width tests and pure source/model/view seams. Missing required envelopes are shape failures; absent optional facts remain unknown; null, invalid and absent remain distinguishable internally. Use one title, subordinate sections, width/height matrix, release/gate table and separate risks from UNVERIFIED claims. No tests were executed here; synthetic renders cannot clear live-source gates. Exact issue-body traceability still needs a later cross-check.

### A-6 / B-4: dispatch-ID order and prototype first-row selection neglect old questions

These are separate orders. My Round 1 already adopted oldest-first questions by verified original time, unknown times last; stable dispatch ordering was for evidence rows. This answers B's Round 2 remaining disagreement: C does not advocate production `requests[0]` by source order. Initial selection is oldest observed, not globally oldest; thereafter only human navigation retargets it. Stable question identity anchors selection through reordering, with a same-ID last-known placeholder on non-observation. Evidence can group by raw run reference with stable dispatch order inside groups; a run is not a verified orchestrator or human owner.

### B-2: retention was deferred past the first live questions

The original release prose was ambiguous despite its retention tests. B was right; my Round 1 moved retention to the first live-question release, and that remains binding. A non-consuming all-rows read is the preferred candidate only after targeting and row semantics verify; it is not an available question API today. Empty peek, disappearance, marking looked, time passing and source loss never prove closure. Closure semantics remain UNVERIFIED, so until they verify there is no automatic resolved transition.

Adopt B's proposed 1,000-detail session-local retention bound, with disclosed omission and a separately bounded compact identity ledger of the same capacity. Re-observation of retained IDs is idempotent; eviction cannot lower an apparent unresolved total or create a closure-like change event. If omitted identity tracking overflows, stop reporting a numeric unresolved total: show `unknown (retention exceeded)` plus the number currently retained. A/B's Round 2 eviction correction is accepted, but their compact ID ledger must also be bounded. Restart must disclose a new observation baseline, not an empty backlog.

### B-6: owner decisions include classification policy and sensitive-content permission

Agreed, as my Round 1 closing split already said. Engineering verifies shapes, identity, timestamps, targeting and links. If several verified types could qualify as human questions, the owner chooses among them; the owner also grants capture permission, redaction rules and content-display/export policy. A policy vote or fixture cannot make an UNVERIFIED API true. Adopt A's safer exposure default: no automatic body exposure/export without explicit permission; disclose when decision text is withheld.

### Responses to the other Round 2 positions

- **Conditional defaults:** worker ledger before question verification and oldest-first question preview before links are accepted. C need not automatically become a third full layout. Once links verify, test whether its selected question and age-ranked other-questions list handle discovery and inspection without maintaining three screens.
- **Proxy withdrawal and counts:** agreed. Preserve raw `projection.nextAction.kind` as literal, non-executable worker-reported data, not a question classifier. Keep compact source-count/scope/coverage disclosures at every width, no health bars or invented SETTLED mapping. A/B report matching static readings of the narrow prototype; accept those as their reported X-001 evidence, not an independent render here.
- **State convergence:** retain C's independent clocks, four-state facts, explicit-link provenance, literal Rich text and atomic publication, plus A's local generation guard. This does not verify a remote source namespace or ownership join. If a stable namespace cannot be established, isolate scopes or label identity unresolved instead of merging.
- **Freshness:** source STALE follows last successful collection; evidence age is a separate plain age, not row health inferred from unmeasured cadence. Old evidence can remain relevant; timeout is not task failure.
- **Read-only:** release-specific argv templates beat a permanent source-string ban on `check`. Only non-consumption is verified; absence of audit, lease or probe effects remains UNVERIFIED and needs a per-verb check. No operational controls.
- **Disagreements still attributed to C:** measured timeouts, oldest-first questions, interaction spike and capture permission were already accepted or softened in Round 1. Those are settled. Full link-gate release order and default composition were the real remaining differences.

## Concessions Added in Round 2

These supplement, rather than rebrand, the concessions in my Round 1.

1. **A is the initial live default (C-001).** Use its useful worker ledger instead of building a distinctive but mostly unavailable C preview. Preserve the separate synthetic C walkthrough.
2. **Split question readability from affected links (X-012).** A/B's bounded retained queue may ship while all affected-link semantics remain UNVERIFIED. That is a question preview, not the complete linked Decision Desk.
3. **Fair scope rotation replaces selection-bound reads (C-002, X-007).** Keep one message read per cycle and the aggregate child ceiling, but do not leave other configured scopes permanently unobserved. Show revisit ages; do not guarantee coverage from average rates.
4. **Withdraw the fixed row-age STALE verdict (C-011, X-006).** The numeric freshness proposals already needed measurement in Round 1; now evidence displays plain age until cadence/semantics support more. Collection freshness remains separate.
5. **Bound retention now (C-010).** Specify B's 1,000-detail proposal, bounded omitted-ID tracking and unknown totals when tracking overflows. Session-local is not a memory bound; eviction is not closure.
6. **Reduce preview interaction scope (S-005, C-015, X-013).** Keep the height contract, but defer independent scrolling panes; the Rich interaction spike remains a prerequisite rather than a promise.
7. **Accept all-width compact source disclosures (C-005).** A/B's revised no-bars, no-health-name strip is consistent with C's scoped-accounting rule.
8. **Qualify X-001 more accurately.** A/B report two agreeing static reads. My lack of a render does not make those reports a continuing factual dispute, but neither is it independent verification here.

## Revised Positions

| Topic | Round 1 | Round 2 |
|---|---|---|
| Default composition | C product with B retention and A freshness; A wins immediate worker-only utility | A is explicitly the worker-only live default; B-style question preview may precede links; C remains the preferred complete decision-inspection composition once links verify |
| Question gate | Complete C requires question identity/type and link semantics; individual missing links allowed | Separate QUESTION-OBSERVATION (new proposed observer gate) from QUESTION-LINK; first permits retained readable questions, second permits linked affected evidence |
| Message scheduler | One selected source read per cycle | One fair rotating, invocation-verified scope read per cycle; at most five children total, so worker paging is bounded to four calls after enabling messages |
| Capacity claims | Numeric budgets need latency/cadence checks | No two-second timeout or ten-second deadline promoted to a shipping default without representative evidence; fifteen-second interval and five-child/8 MiB caps remain proposals to validate |
| Evidence freshness | Separate collection/evidence ages; calibrate thresholds | Explicitly no row STALE verdict from unverified cadence; collection STALE and evidence plain age are distinct |
| Retention | Retain from first question release; future bound required | Proposed 1,000 detail records plus bounded omitted-ID tracking; partial/unknown unresolved coverage on eviction/overflow; no implicit closure |
| Interaction | C panels subject to early Rich spike | Preview has one active list/detail flow and disclosed overflow; richer focus/scrolling requires the spike or Textual switch |
| Source counts | Raw scoped accounting, no health gauges | Same, with compact disclosures kept at every width as A/B now propose |
| Queue selection | Verified oldest-first questions, stable worker evidence, selection by ID | Unchanged; initial oldest observed selection never silently retargets on disappearance or new arrivals |
| Verification | B harness and IDs, A seams/generation, C atomic model | Unchanged; adoption is a proposal, not executed-test evidence |

Every new gate is an observer requirement, not an Orca endpoint. Gates require permissioned representative success, missing, stale and contradictory samples plus parser/invocation tests. No sample was collected in this round. The selected-question body is withheld unless exposure policy permits it; that may limit live decision usefulness and must be visible.

Non-negotiable contracts remain unchanged: scoped identity; independent component clocks and visible equal-time conflict; identical accepted input leaves facts, selection and change badges unchanged; partial-page non-observation is not deletion; unknown is never zero/false; explicit associations only. Keep lifecycle, report status, acceptance, tests and human approval separate. Complete history, cross-host ownership joins, admission and revision-pinned evidence feeds, cost/usage coverage, durable replay and native deep links remain UNVERIFIED and excluded. No operational controls, copied AGPL code, production prototype imports or synthetic-to-live automatic transition.

## Updated Per-Point Stances

Levels follow the diff-analysis order. Confidence concerns the design preference, not whether an UNVERIFIED source exists. Changed means a substantive shift from C's Round 1 table, not merely adjusted confidence or reordered variant names. For A points, the required variant column names the preferred handling; QUALIFY/REJECT in Reason states the assumption verdict. REJECT rejects reliance on an unverified premise, not a claim it was empirically disproved.

| ID | Level | Preferred variant | Confidence | Changed? | Reason |
|---|---|---|---|---|---|
| S-001 | L1 | V1 | 0.98 | no | A title and subordinate numbered sections are easier to reference than C's flat headings. |
| S-002 | L1 | V2 | 0.95 | no | Width and evidence subsections aid navigation. |
| S-003 | L1 | V1+V2+V3 | 0.99 | no | The shared topic sequence already meets the brief. |
| S-004 | L1 | V1+V2 | 0.96 | no | Tables clarify bounds, release gates and acceptance mapping. |
| S-005 | L2 | V1+V2+V3 | 0.94 | yes | Combine width matrix/coordinates and C's height contract, but defer per-panel scrolling. |
| S-006 | L2 | V2 | 0.98 | no | Number criteria and tests; exact issue wording still needs cross-checking. |
| S-007 | L2 | V3+V2 | 0.95 | yes | Keep named gates and fallback, splitting question observation from link verification. |
| S-008 | L2 | V3+V2 | 0.97 | no | Engineering verifies contracts; owner grants capture/exposure permission and chooses among verified types. |
| S-009 | L1 | V2 | 0.96 | no | Separate design risks from UNVERIFIED capabilities. |
| S-010 | L2 | V3+V1 | 0.97 | no | One immutable atomic publication with pure source/view seams and generation guard suffices. |
| S-011 | L1 | V2 | 0.95 | no | Plain self-criticism is more useful than repeating the preferred winner. |
| C-001 | L2 | V1+V2+V3 | 0.93 | yes | A for worker-only live mode, B-style question preview before links, C for complete linked decision inspection. |
| C-002 | L2 | V3+V2+V1 | 0.94 | yes | Prefer verified non-consuming all-rows reads with retention, fair scope rotation, one message call per cycle and exposure permission. |
| C-003 | L3 | V3+V2 | 0.99 | no | Question source UNVERIFIED and zero interpreted rows never mean zero real questions. |
| C-004 | L2 | V3+V1 | 0.98 | no | Raw next-action facts belong in ledger/detail, never executed or interpreted as human questions. |
| C-005 | L2 | V1+V2+V3 | 0.97 | yes | Keep source counts/scope/coverage at every width, without health bars or mixing source and observed totals. |
| C-006 | L3 | V3+V2+V1 | 0.93 | yes | Retain finite child/output bounds and backoff; fair rotation and representative latency evidence replace fixed tight timing claims. |
| C-007 | L3 | V3+V1 | 0.99 | no | Independent component clocks and visible conflicts plus local generation prevent rollback without inventing event order. |
| C-008 | L3 | V3+V2 | 0.99 | no | Preserve absent/null/valid/invalid internally and disclose unknown aggregate members. |
| C-009 | L3 | V3+V2 | 0.98 | no | Explicit local baseline, first-observation baseline and partial-page non-observation remain separate from closure. |
| C-010 | L3 | V2+V3 | 0.99 | yes | Retain from first live questions; bound details and omitted-ID tracking, degrading totals to partial/unknown rather than resolution. |
| C-011 | L3 | V3+V2 | 0.98 | yes | Source STALE follows collection success; evidence shows plain age, not a cadence-dependent verdict. |
| C-012 | L2 | V3+V1 | 0.97 | no | Hide unrelated history with disclosed count; linked historical evidence stays inspectable and is not called active. |
| C-013 | L2 | V3+V2 | 0.99 | no | page.total is source-reported, not a filtered or proven all-host fleet denominator. |
| C-014 | L3 | V3+V2 | 0.99 | no | At most 100 message rows per read, not 100 questions; below-cap reads still do not prove completeness. |
| C-015 | L1 | V1+V2+V3 | 0.94 | yes | Preview uses local list/detail inspection, filtering and mark-looked; defer multi-panel input pending the spike. |
| C-016 | L1 | V1 | 0.95 | no | A visible trailing truncation marker is necessary; preserve full values in detail/export. |
| C-017 | L1 | V3+V2 | 0.98 | no | ASCII-safe export retains IDs, source times, denominators and caveats subject to body-exposure policy. |
| C-018 | L2 | V3+V1 | 0.96 | no | Rich interaction must pass a small combined spike; otherwise switch interaction stack without parallel implementations. |
| C-019 | L1 | V1 | 0.90 | no | A short in-repository observer command is sufficient; the suggested name is not an implemented capability. |
| C-020 | L3 | V3+V2 | 0.99 | no | Literal Rich text and full terminal-control sanitization; no prototype import or unverified-provenance reuse. |
| C-021 | L2 | V1+V2+V3 | 0.99 | no | Fake runner/redacted golden samples and recorded-console tests; synthetic passes cannot satisfy live gates. |
| C-022 | L3 | V3 | 0.99 | no | Supplied frozen evidence stays frozen; missing evidence is unknown/unavailable, never unfrozen. |
| C-023 | L2 | V3+V2 | 0.99 | no | Cost unavailable is an honest disclosure; no zero or unsupported estimate. |
| C-024 | L2 | V2+V1 | 0.97 | no | Explicit POSIX interactive scope and portable text fallback are better than silence. |
| C-025 | L2 | V3+V2+V1 | 0.98 | no | Verified oldest-observed question first, untimed last; stable workers grouped by run and selection anchored to identity. |
| X-001 | L2 | V1 | 0.88 | yes | A/B report agreeing static reads that 116 omits counts; accept that reported finding, not an independent render here. |
| X-002 | L3 | V3+V2 | 0.99 | no | Worker-only R1; message reads require verified invocation and interpretation first. |
| X-003 | L3 | V3+V2 | 0.99 | no | UNVERIFIED count semantics cannot support unread wording or cap interpretation. |
| X-004 | L3 | V3+V2 | 0.95 | no | Pin reported cursor syntax with multi-page invocation evidence; reject loops/missing cursors and retain PARTIAL fallback. |
| X-005 | L3 | V3 | 0.99 | no | Namespace dispatch identity only by established stable source scope; cross-host uniqueness/joins remain UNVERIFIED. |
| X-006 | L3 | V3+V2 | 0.98 | yes | Withdraw fixed per-row STALE; show collection freshness and independent evidence age. |
| X-007 | L3 | V3+V2 | 0.97 | yes | One fair rotating message read within the total child ceiling; expose per-scope ages and unknown message coverage. |
| X-008 | L3 | V2+V3 | 0.99 | no | Provenance before reuse; no production prototype imports and no copied AGPL code. |
| X-009 | L2 | V3+V2 | 0.98 | no | Engineering verifies semantics; owner chooses among verified candidate types and authorizes sensitive capture. |
| X-010 | L2 | V3+V1 | 0.98 | no | Hide unrelated historical rows with a count, never suppress explicitly linked evidence just for being historical. |
| X-011 | L2 | V1 | 0.99 | no | SETTLED has no verified mapping; no product definition alone creates outcome evidence. |
| X-012 | L2 | V1+V2+V3 | 0.96 | yes | Allow retained question preview before links verify; complete C still requires verified association semantics. |
| X-013 | L2 | V1+V3 | 0.97 | yes | Defer independent scrolling panes in the preview; richer C interaction must pass the spike or trigger Textual. |
| A-001 | L3 | V3+V2 | 0.99 | no | QUALIFY: non-consuming is verified, absence of lease/probe/audit effects is UNVERIFIED; check each admitted verb. |
| A-002 | L3 | V3+V2 | 0.99 | no | REJECT as premise: source cadence is UNVERIFIED, so age cannot establish worker health. |
| A-003 | L3 | V3+V2 | 0.99 | no | QUALIFY: bound stdout, require complete JSON/envelope validation and preserve last-good data on failure. |
| A-004 | L2 | V3+V1+V2 | 0.98 | no | QUALIFY: recorded width tests need real-terminal CJK/emoji/combining checks. |
| A-005 | L3 | V3+V1+V2 | 0.98 | no | QUALIFY: combined input/redraw/resize/restore testing is required before accepting Rich interaction. |
| A-006 | L2 | V3+V2 | 0.97 | no | QUALIFY: measure render and selection responsiveness separately from collection budgets. |
| A-007 | L2 | V3+V1+V2 | 0.98 | no | QUALIFY: declare terminal requirements and give unsupported terminals an ASCII-safe fallback. |
| A-008 | L3 | V3 | 0.99 | no | REJECT aggregate-load premise: per-process caps multiply with observers; disclose rather than inventing a singleton service. |

## Remaining Disagreements

| Point | C's remaining position | A/B position or unresolved issue | Evidence/decision that settles it |
|---|---|---|---|
| C-001 after links verify | C's selected decision and age-ranked other-questions panel may serve discovery and inspection as one complete composition; do not automatically build three full layouts | A/B make B the default and C a later third view | Permissioned question/link samples plus an owner walkthrough comparing finding an old observed question and inspecting its evidence at all three widths; link availability alone establishes feasibility, not preferred workflow |
| C-002 / X-007 message scheduling | One rotating message-scope read per cycle, no selection starvation, five-child total ceiling | A/B also rotate under the cap but may spend more message calls if affordable | Representative latency/burst observations and explicit coverage tolerance; row targeting/window semantics remain UNVERIFIED, and faster polling alone cannot certify complete history |
| Retention totals | If bounded omitted-identity tracking overflows, numeric unresolved coverage becomes unknown; retained-count and unresolved-total are different quantities | A/B propose partial counts and compact ID retention; B also mentions a later bound | Contract tests for duplicate reappearance, both-cap overflow and restart; no eviction, parser failure or source loss may count as closure |
| X-013 full C interaction | Simpler preview now; the complete composition may justify Textual instead of maintaining custom Rich focus/scrolling | A/B defer such interactions behind the switch rule | Combined real-terminal spike and maintenance-budget acceptance, not a library capability claim from memory |
| A-008 assumption verdict | REJECT using single-observer behavior as a fleet-load guarantee; per-process disclosure is sufficient for this slice | A/B use QUALIFY and leave prevention to the owner | Mostly terminology: all agree caps are per process and no singleton service is required; expected deployment concurrency determines whether later coordination is needed |

No remaining disagreement on first-release retention, zero-versus-unknown, independent clocks, literal rendering, initial oldest-observed question order, explicit links, capture permission, component separation or no operational controls. Worker lifecycle, report status, acceptance, tests and human approval remain separate. Message row fields, inbox JSON, complete history, cross-host ownership joins, admission/revision feeds, cost/usage coverage, durable replay and native deep links are still UNVERIFIED. No implementation, live collection or runtime test result is claimed.
