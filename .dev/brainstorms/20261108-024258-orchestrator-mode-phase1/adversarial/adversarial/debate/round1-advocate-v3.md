# Round 1 Advocate V3

## Steelman of the opposing variants
V1's strongest case is that a safe observer needs enforceable boundaries, not merely cautious prose. Its Architecture and component boundaries section fixes dependency direction, separates future write seams, and requires fresh collection before later action. Its Data model and classification states section gives a total ordered rule table, explicit unreadable fencing, and an unknown package state. Those are stronger implementation contracts than V3's prose model groups. Its deliberately small Git allowlist is defensible because the report cannot grant removal anyway.

V2's strongest case is that requirements should explain the failure they prevent and the evidence that proves prevention. Problem and Root Cause joins the missing observation point with the missing coordinator duty. NFR-002 includes a real Git control experiment that may report inconclusive instead of claiming a pass. Report Format puts uncertainty before apparently healthy rows, and FR-026 protects task content with a negative ignore test. These are valuable operational checks, not decorative analysis.

## Position and strengths
Prefer V1's structural skeleton with V3's observation and publication guarantees, plus V2's evidence-focused checks. V3 is strongest at the boundary between collected facts and the person or program consuming the report.

- Publication is an API commitment. V3's CLI contract and re-run idempotency section reserves paths exclusively, preserves previous observations, prints JSON only after a successful write, and documents crash leftovers rather than promising atomic publication. NFR-006 and the Verification checklist require concurrent same-second cases. V1 and V2 specify timestamp paths but not collision behavior. This is preservation of existing data, not an extra service.
- Missing is not false. FR-007, NFR-005 and Data model and classification precedence keep absent, null and unreadable separate. Positive absence of both completion and fencing is needed for stalled proof. Duplicate contradictory Dispatch observations retain one identity and a conflict reason. This stops failed reads from becoming operational authority.
- Bounded discovery remains honest. FR-003 and FR-020 preserve discovered rows, deduplicate Dispatch IDs and reconcile visible, historical and omitted totals. NFR-003 limits each call by remaining overall time, and NFR-007 adds byte limits. Report format exposes lower-bound totals and the collection interval. These are proposed contracts, not verified runtime capabilities.
- The window must not erase unresolved work. FR-013 and the classification section exempt open Tasks, waits and unread-report candidates from age-based exclusion. An old question is not resolved by becoming old.
- Report content is an input boundary. FR-019, NFR-008, NFR-009 and Report format constrain hostile Markdown, unsafe parsing, secret dumps and wholesale transcript copies. Owner-only output mode is a proposed file-permission requirement, not a new identity model.
- The report remains inspection-only. FR-017 and WC-14 reject stop, retry, release, merge or removal proposals from this incomplete read model. WC-14 ends after settlement and recorded admission or rejection, rather than waiting forever for an unusable result to become admitted.

Evidence notation below uses variant section names and requirement IDs. Source-code, runtime-schema, executable-name and external-PR claims not inspected in the supplied documents remain UNVERIFIED. No live behavior was checked.

## Critiques and concessions
### V2

1. Its classifier converts unknown fencing into proved absence. Data Model rule 2 uses `consumer_fenced is not True`, which admits null. Rule 3 cannot repair that because first-match rule 2 already returned stalled. FR-009's positive-proof intent does not fix the actual predicate. Replace it with known false fencing and explicit unreadable handling, as V1 and V3 require. This is the strongest safety critique.
2. Its WC-14 recommends cancellation, removal and a replacement Task while FR-013 admits that report-reading, result-reading and PR facts are unobserved. Text-only output prevents direct execution, not a person acting on an unjustified proposal. Prefer inspection steps, with any later action governed by fresh evidence and separate authorization. Owner decision on proposals remains open in V2 itself.
3. Its rule 7 catches everything before idle. Its package model has no unreadable state. Both are gaps between the promised unknown semantics and executable ordering. Adopt V1's total precedence and explicit package unknown.
4. Its rollback removes the ignore line while calling preserved reports ignored. Those instructions cannot both hold. Its report-path acceptance also leaves simultaneous publication unspecified.

### V1

1. Its Report format claims Shift Brief adoption but omits the section, and its Sessions columns omit next action and waiting-on. The seed success criterion requires those fields for every session. V3's next inspection is a safe way to satisfy that requirement without adding actions.
2. Its exact timestamp report name does not establish no-overwrite behavior. Concurrent or repeated same-second sweeps can select the same path; whether implementation would truncate is UNVERIFIED. V3 closes the contract gap with exclusive creation and explicit failure behavior.
3. Its WC-14 end condition says every Task is admitted. Rejected results need a defined stopping outcome too. V3 requires recorded admission or rejection while keeping unresolved decisions visible.
4. Its structural tests are useful but not runtime proof. Recorded argv cannot establish that an Orca read never consumes messages or internally runs locking Git. V3 explicitly carries that uncertainty, although its proposed live release gate must be removed from this work.

### Concessions and repairs to V3

- X-001: adopt V2's explicit disk-only exception when Orca is unavailable and no Run was supplied. An unavailable binding lookup is not a successful lookup returning no binding. Still exit 2 for a confirmed missing binding. The seed does not explicitly distinguish these cases, so this is a proposed resolution rather than a proven seed mandate.
- C-007 and X-005: drop V3's fixed-base comparison. It adds an unresolved baseline and argv gate where V1's single local status parse already avoids unchanged shared folders. Changed-since-base can also flag committed historical work without current activity.
- S-005, S-006, C-001 and X-007: take V1's module boundaries, typed models and reachable idle-before-fallback order. V3's prose is less precise and its idle position needs correction.
- C-008 and X-011: V3 needs a non-ready Task-list read to supply blocked-gate policy. V1 names the source; its exact runtime form is still UNVERIFIED. A model field without an admitted source is not a complete probe contract.
- C-006 and X-006: restore explicit unknown package state and interrupted-archive blocking from V1. Archive-blocked alone is a report state, not automatically unfinished work; other blockers still apply and yes remains unreachable.
- X-016: remove V3's mandatory disposable-Run release check from Phase 1 acceptance. The seed prohibits live launches in this work. Mocks do not prove runtime non-consumption, so retain UNVERIFIED status and defer any separately authorized check outside this scope.
- X-017 and X-018: take V1's exact contract pins and its guard-refused finished exception. V3's broad unreadable-source failure row should not erase independent, sufficient guard-refusal evidence. Finished still does not mean admitted or releasable.
- X-010: use V2's isolated real-Git control test as an exception to mocked subprocess tests. The seed forbids live Orca, ccsession and Claude, not temporary Git repositories. No such test is run in this debate.
- C-023 and X-008: keep V3's periodic-sweep duty because the supplied owner memory explicitly calls for it, subject to contract-text approval. Do not turn its suggested five-minute cadence into a Phase 1 scheduler or fixed contractual interval.

## Per-point positions
Each row is a preference, not acceptance of every sentence in the named variant. Merges include V3 only when retaining a substantive V3 contribution. Preferences excluding V3 are concessions. Confidence measures the design preference, not verification of runtime facts.

| Point ID | Preferred variant | Confidence 0-100 | One-line evidence |
|---|---|---:|---|
| S-001 | V1 | 82 | Header metadata gives date and status explicitly; this is a presentation preference. |
| S-002 | merge V1+V3 | 93 | V1 architecture organization plus V3's dedicated publication and re-run contract. |
| S-003 | V1 | 82 | Functional-requirement table keeps statement and acceptance together. |
| S-004 | V1 | 94 | Use one canonical requirement namespace and renumber merged requirements; existing IDs collide. |
| S-005 | V1 | 97 | Architecture B1-B5 makes dependency and future-write boundaries testable. |
| S-006 | V1 | 95 | Typed immutable records and explicit unknown package state beat V3's field groups. |
| S-007 | merge V1+V2 | 88 | V1 supplies exits; V2 adds failure evidence and containment tests. |
| S-008 | V2 | 82 | Risk likelihood and impact distinguish frequent noise from destructive misclassification. |
| S-009 | V2 | 83 | Gap table connects the stated root cause to the proposed fix. |
| S-010 | V2 | 85 | OQ identifiers support stable approval references without relying on bullet order. |
| S-011 | V3 | 94 | Verification and rollback adds concurrency, source-loss and input-race checks. |
| S-012 | V2 | 90 | Sources read explicitly separates inspected inputs; external claims still need verification. |
| S-013 | V2 | 86 | Fenced WC-14 block is directly reusable and preserves the actual heading. |
| C-001 | V1 | 99 | Data model rules place idle before an explicit fallback. |
| C-002 | V1 | 97 | Rule 1 explicitly returns unknown for unreadable policy on a live blocked row. |
| C-003 | merge V1+V3 | 99 | Both require known absent fencing and reject unreadable proof. |
| C-004 | V3 | 96 | Rule 6 separates partial usability, finished lifecycle and admission. |
| C-005 | V3 | 94 | Rule 4 calls unknown creator evidence ownership review, not definitively foreign. |
| C-006 | V1 | 94 | Package-state table includes unreadable unknown and interrupted-archive blocking. |
| C-007 | V1 | 98 | FR-015 uses the existing status parse without V3's unresolved base comparison. |
| C-008 | V1 | 95 | Non-ready Task-list form supplies gate-policy text missing from V3's closed forms. |
| C-009 | V1 | 94 | Git allowlist omits ancestry probes when removal already cannot be yes. |
| C-010 | V1 | 94 | Seam constructs the prefix and environment itself, rather than trusting callers. |
| C-011 | V2 | 96 | NFR-002 adds an isolated real-Git control and distinguishes inconclusive from passed. |
| C-012 | V1 | 86 | A single explicit root-resolution template is clearer than V3's unspecified method. |
| C-013 | V1 | 91 | Unknown unmerged state is honest and avoids a new baseline-dependent read. |
| C-014 | V3 | 95 | FR-003 and Probe seams forbid invented continuation flags and preserve partial coverage. |
| C-015 | V2 | 93 | FR-002 explicitly distinguishes runtime outage from a confirmed missing binding. |
| C-016 | V3 | 97 | CLI contract ties exit 0 to successful report publication, not complete evidence. |
| C-017 | merge V1+V3 | 95 | V1 schema stability plus V3 ID-only waiting lists and publication-before-JSON guarantee. |
| C-018 | merge V2+V3 | 95 | V2 promotes uncertainty; V3 includes Shift Brief, complete inventory and coverage counts. |
| C-019 | V3 | 99 | Re-run contract reserves unique paths exclusively and preserves existing reports. |
| C-020 | V3 | 99 | Dedicated idempotency contract prohibits lifecycle changes and consuming cursor advancement. |
| C-021 | V3 | 95 | NFR-002 makes identical normalized inputs and injected time render identically. |
| C-022 | V3 | 94 | WC-14 records admission or rejection, so rejected results need not become admitted. |
| C-023 | V3 | 92 | WC-14 periodic duty matches supplied owner memory without implementing a scheduler. |
| C-024 | merge V1+V3 | 96 | Both choose no action recommendations from an incomplete read model. |
| C-025 | V3 | 93 | WC-14 separates scheduling duty from software and rejects heartbeat-based death inference. |
| C-026 | V1 | 96 | WC-14 pins preserve exact phrases and the count-free test name avoids needless churn. |
| C-027 | merge V1+V2+V3 | 95 | Combine V1 output errors, V2 symlink controls and V3 input-race and crash cases. |
| C-028 | merge V2+V3 | 94 | Snapshot hashes and metadata across isolated roots plus V3 publication-failure checks. |
| C-029 | V3 | 97 | NFR-003 caps each call by remaining total time; NFR-007 also caps bytes. |
| C-030 | V3 | 94 | Report format neutralizes hostile HTML and active links as well as pipes and controls. |
| C-031 | merge V1+V3 | 96 | Both preserve reports and keep the ignore rule until their disposition is decided. |
| C-032 | V1 | 91 | Capture before fixing fixture/model mappings, not merely before final release. |
| C-033 | V2 | 89 | Report format copies chosen sections so it does not require unmerged code imports. |
| C-034 | V3 | 93 | Open questions keeps WC-14 part of done instead of silently deferring required scope. |
| C-035 | V3 | 97 | FR-013 and classification preserve old unresolved Tasks and waits, not only recent activity. |
| C-036 | merge V1+V3 | 96 | V1 defaults ten dimensions unknown; V3 explicitly forbids inferred admission or approval. |
| C-037 | merge V2+V3 | 95 | V2 names deciding rule and field; V3 adds observation time and unavailable reason. |
| C-038 | V3 | 97 | Sessions includes next inspection for every session, satisfying next-action needs without execution. |
| C-039 | merge V1+V3 | 94 | V1 fixed forbidden list plus V3 rejection before spawn prevents silent permission expansion. |
| C-040 | V3 | 98 | CLI contract rejects symlink escape and output overlap with input directories. |
| C-041 | merge V2+V3 | 96 | Fixed direct reads plus V3 admitted-root membership and canonical-root deduplication. |
| C-042 | V2 | 90 | Gap resolution carries stale citations without pretending to repair the research report. |
| C-043 | V1 | 88 | Later-phase table provides explicit blocker provenance; source correctness remains UNVERIFIED here. |
| X-001 | V2 | 93 | Confirmed missing binding differs from unavailable lookup; use V2's explicit disk-only exception. |
| X-002 | merge V1+V3 | 99 | V2's null fencing passes `is not True`; V1 and V3 demand positive absence. |
| X-003 | merge V1+V3 | 96 | Unknown admission and PR evidence cannot justify cancellation or removal proposals. |
| X-004 | V1 | 95 | Two exact Git templates are sufficient when ancestry may remain unknown. |
| X-005 | V1 | 98 | One status parse already distinguishes unchanged shared folders from current local changes. |
| X-006 | V1 | 93 | Archive-blocked alone is not unfinished; interrupted archive explicitly blocks removal. |
| X-007 | V1 | 99 | Idle precedes fallback and is therefore reachable under first-match semantics. |
| X-008 | V3 | 92 | Supplied owner memory requires periodic sweep duty; exact cadence and text still need approval. |
| X-009 | merge V1+V3 | 72 | Both consistently name orca-ide; executable correctness remains UNVERIFIED, not decided by votes. |
| X-010 | V2 | 96 | Seed forbids live Orca, ccsession and Claude, not isolated real-Git control experiments. |
| X-011 | V1 | 97 | Its Task-spec read supplies a required policy field absent from V3's allowlist. |
| X-012 | V1 | 85 | Adopt one public class key, `class`, and pin it instead of exposing inconsistent spellings. |
| X-013 | merge V1+V3 | 98 | Keeping reports while removing their ignore rule contradicts V2's ignored-report claim. |
| X-014 | merge V2+V3 | 98 | Both actually list Shift Brief; V1 promises it but leaves it out of the section list. |
| X-015 | V3 | 98 | Report Sessions explicitly includes waiting-on and next inspection for every row. |
| X-016 | merge V1+V2 | 99 | Remove V3 mandatory live release gate from this work; seed prohibits live launches. |
| X-017 | V1 | 98 | Exact never-posted pin is present and testable, unlike V3's paraphrase. |
| X-018 | V1 | 92 | Independently observed guard refusal can prove finished without a readable contract; never admission. |
| X-019 | V3 | 99 | Same-second invocations must preserve separate observations or fail without overwriting. |

## Shared assumptions
These decisions concern shared assumptions, not permission to run probes. ACCEPT means retain the design requirement; it does not certify undocumented runtime behavior.

| Assumption ID | Decision | Reason |
|---|---|---|
| A-001 | ACCEPT | A1 keeps collection, classification and publication separable and mock-testable; CLI reachability remains a delivery check. |
| A-002 | QUALIFY | Require the fixed flag on every direct Git call, but indirect locking by Orca remains UNVERIFIED under A-101. |
| A-003 | QUALIFY | Explicit Runs or current binding is the correct scope rule; child-process binding visibility remains UNVERIFIED. |
| A-004 | QUALIFY | Positive exit proof is necessary but insufficient without known absent completion and fencing; evidence mappings remain UNVERIFIED. |
| A-005 | ACCEPT | Both REVIEW dimensions must stay below yes while result-reading, report-reading and PR facts are unobserved. |
| A-006 | QUALIFY | A failed or partial tab-map join must mean unknown origin, not positive proof that a session was person-started. |
| A-007 | QUALIFY | Accept caps as limits, not as evidence that typical Runs fit; show discovered rows, omissions and lower-bound totals. |
| A-008 | QUALIFY | Keep the ignored dated base name but reject second-resolution uniqueness; reserve collision-safe names exclusively. |
| A-009 | ACCEPT | Separate published partial success, internal safety/write failure and confirmed usage failure; pin these with CLI tests. |
| A-010 | QUALIFY | Require sanitization but verify representative viewer rendering; pipe escaping alone does not cover hostile HTML or links. |
| A-011 | ACCEPT | Partial message coverage must stay explicit; absence of the substitute signals is not proof that nobody is waiting. |
| A-012 | ACCEPT | Keep contract eligibility and owner/overlap gates; current external PR status remains UNVERIFIED. |
| A-013 | QUALIFY | Carry documentation debt without changing the research report; this debate has not independently verified the original gap counts. |
| A-014 | ACCEPT | Positive integer hours or days with six-hour default is a clear proposed input contract. |
| A-015 | ACCEPT | Reuse one status parse per root for dirt, ahead, task paths and local package activity. |
| A-016 | QUALIFY | Contract-only coordinator eligibility matches scope but is not enforcement or proof that a caller is authorized. |
| A-017 | QUALIFY | Mock both runtime seams for sweep behavior; allow V2's isolated real-Git safety control, never live Orca, ccsession or Claude. |
| A-101 | QUALIFY | Orca read verbs' indirect Git effects are UNVERIFIED; direct argv tests cannot prove their absence. |
| A-102 | QUALIFY | Child-process visibility of the current binding is UNVERIFIED; explicit Run selection must remain usable without guessing history. |
| A-103 | QUALIFY | A readable source proving completion absence is UNVERIFIED; absent such evidence, exited rows remain unknown. |
| A-104 | QUALIFY | Stable readable tab-map format is UNVERIFIED; missing or unsupported maps require explicit join-coverage failure. |
| A-105 | QUALIFY | Worktree-to-project-key derivation is UNVERIFIED; ambiguous mappings must not broaden scope or create confident joins. |
| A-106 | QUALIFY | Transcript mtime is at most an activity proxy, UNVERIFIED as a semantic event clock; unresolved waits bypass the window. |
| A-107 | REJECT | No evidence establishes typical Run size; the design must report cap exhaustion honestly instead of assuming it rare. |
| A-108 | QUALIFY | Literal-pipe rendering is viewer-dependent and UNVERIFIED here; include rendering checks rather than claiming universal Markdown behavior. |

Unique contributions are supporting ideas, not additional voting rows. Retain V1's boundary, named-rule and schema tests; V2's real-Git control, negative task-ignore test and uncertainty-first ordering; and V3's publication, byte limits, evidence timestamps, deduplication, coverage reconciliation and unresolved-work visibility. Drop V3's in-scope live release gate. Keep exact runtime syntax and indirect read-only guarantees UNVERIFIED until evidence exists within an authorized scope.

No code, runtime, QA material or live tool behavior was checked. Recommended synthesis is V1's explicit models and boundaries, V3's preservation and publication guarantees, and V2's evidence-led tests, with the concessions above applied before implementation.
