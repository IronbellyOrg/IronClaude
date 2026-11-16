# Adversarial Debate Transcript

## Metadata

- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: depth=quick; Round 3 skipped: depth=quick)
- Convergence achieved: 95 percent (19 of 20 points)
- Convergence threshold: 80 percent
- Focus areas: All
- Advocate count: 3, each a spawned sub-agent (general-purpose), one per variant, run in parallel
- Neutral recommendations: V1 advocate 75 percent for a B-based merge; V2 advocate 70 percent for a B-based merge; V3 advocate 70 percent for a B-based merge. Mean 72 percent.

## Round 1: Advocate Statements

The full statements are the advocates' own files; they are not copied here so that each statement exists once.

### Variant 1 Advocate (proposal A)
Full text: `round1-advocate-V1.md`. Position: the write-ahead claim per (issue, stage, plan version) is the real guard in all three designs, and A alone progresses without a coordinator. Concessions: A reverses the owner's recorded watcher decision D2 and non-goal NG-2; the permission-free agent becomes an actuator ("Not solved"); the claim is per host; echo suppression is forgeable; A is the "safeguards" option, not "single source". Neutral: B as base, plus C's event id as evidence and C's read-only verb, built on the watcher's existing lock and fsync code; 75 percent.

### Variant 2 Advocate (proposal B)
Full text: `round1-advocate-V2.md`. Position: B is the owner's "single source" option taken literally and leaves the watcher as built. Concessions that change the design: (1) B's claim that Orca approvals wait in the Run mailbox while the coordinator is down is overstated, because an approval typed in the coordinator session cannot be made while it is down; (2) typing the approval line into the agent's waiting prompt collides with the coordinator's own input veto, "never answer a person prompt" (`WORKER-CONTRACT.md` line 136, re-read by the orchestrator); (3) the watcher's `unchanged_since` skips comments by the watcher's own login (`predicates.py` lines 253 to 255, re-read by the orchestrator), and the coordinator posts the plan reply as that login, so reusing it would not detect an edit to the plan reply; `approval_of` also orders against a trigger label and the store's creation time, so a stage variant is needed; (4) a backward Status move has no readable actor, so C's label removal is the better revocation signal. Neutral: B-based merge with C's verb, label-removal revocation and event id as evidence, with the GitHub channel limited to a second approver account or off until FU-6; 70 percent.

### Variant 3 Advocate (proposal C)
Full text: `round1-advocate-V3.md`. Position: C is the only design with one authority as well as one actuator. Concessions: X-002 is real and unresolvable on one login; Orca approvals can "not take" until GitHub returns the event; the watcher's predicates need new stage versions; C's consumed list is local, so it should also post a consumed marker on the issue; the key must be (issue, stage, plan version), not the event id, or a remove-and-reapply would restart finished work; C has no acknowledgement step. Neutral: B as base, with Orca approvals recorded directly in B's ledger, GitHub approvals accepted only as label events through C's read-only verb, label removal as revocation, B's ack, and a consumed marker on the issue; 70 percent.

### Shared assumption responses

| A-NNN | V1 | V2 | V3 | Result |
|---|---|---|---|---|
| A-001 coordinator exists and owns each issue | QUALIFY | ACCEPT | QUALIFY | Holds only once an owner decides who opens it and its scope; not built |
| A-002 something may type into the agent's waiting prompt | ACCEPT | QUALIFY | QUALIFY | Conflicts with the "never answer a person prompt" veto; needs an explicit exception, a verified Orca permission, or the supervised-worker route |
| A-003 one stable, identically hashed plan | QUALIFY | QUALIFY | QUALIFY | Plan version must be defined over named files (or a package manifest) by one shared helper and printed in the plan reply |
| A-004 owner accepts label as the signal | QUALIFY | QUALIFY | QUALIFY | Forced by the code (only the current Status value is read); owner must accept, or the Status actor must be shown readable |
| A-005 standing issue-write grant | ACCEPT | ACCEPT | ACCEPT | New grant shape needed |
| A-006 agent stays alive while waiting | QUALIFY | QUALIFY | QUALIFY | A dead session must lead to "recorded, not delivered" and a report to the person, never an automatic relaunch |

No omissions.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | none (identical) | 95% | All three say identical skeleton |
| C-001 | L3 | V2 | 75% | V1 and V2 advocates for B's one actuator; V3 advocate for C, whose actuator is also single |
| C-002 | L3 | V2 | 70% | Locked local row works for both channels without GitHub lag; C's event id kept as evidence |
| C-003 | L2 | V3 | 95% | Unanimous: watcher unchanged plus a read-only verb so checks run as code |
| C-004 | L3 | V2 (tie with V3) | 90% | Unanimous that the bare `approved` path must go; A keeps the self-approval hole |
| C-005 | L3 | unresolved | 50% | V1, V2 and "owner" each chosen once: liveness against duplicate risk is the owner's call |
| C-006 | L3 | V2 | 95% | Unanimous: record then instruct, no GitHub round trip, no account contradiction |
| C-007 | L3 | V3 | 90% | Unanimous: one record means no echo rule to get wrong |
| C-008 | L3 | V3 | 75% | Label removal has a readable actor; keep B's never-auto-restart |
| C-009 | L2 | V2 | 95% | Unanimous: only B names the supervised-worker route |
| C-010 | L2 | V2 | 95% | Unanimous: smallest change to built code |
| X-001 | L2 | V2 (V3 equal) | 95% | Unanimous that A loses: it reverses D2 and NG-2 |
| X-002 | L3 | V2 | 95% | Unanimous: B has no write-through contradiction |
| X-003 | L3 | none/owner | 95% | Unanimous: owner must accept the label substitute |
| A-001 | L2 | none/owner | 70% | Two of three: no design is complete without an owner-defined coordinator |
| A-002 | L3 | V2 | 95% | Unanimous: B alone names a fallback delivery route |
| A-003 | L3 | none/owner | 95% | Unanimous: shared definition needed |
| A-004 | L3 | none/owner | 95% | Unanimous: owner decision |
| A-005 | L2 | none/owner | 70% | Two of three: shared grant need |
| A-006 | L3 | none/owner | 70% | Two of three: shared gap |

Points won: V2 9 (C-001, C-002, C-004, C-006, C-009, C-010, X-001, X-002, A-002); V3 3 (C-003, C-007, C-008); V1 0.

## Convergence Assessment

- Points resolved: 19 of 20
- Alignment: 95 percent
- Threshold: 80 percent
- Taxonomy coverage: L1 (S-001), L2 (6 points), L3 (13 points) all covered
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: C-005 (whether progress may continue while the coordinator is down)
