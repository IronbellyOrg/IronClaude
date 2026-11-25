# Adversarial Debate Transcript

## Metadata

- **Depth:** deep
- **Rounds completed:** 3, plus the Round 2.5 invariant probe
- **Convergence achieved:** 90.9% (90 of 99 points), status NOT_CONVERGED (one HIGH invariant, INV-020, is UNADDRESSED)
- **Convergence threshold:** 75%
- **Focus areas:** all (worker liveness for the Orca coordinator: state model, wake and sweep, acknowledgement, response ladder, restart budget, contract (WC) rules, v1/v2 split)
- **Advocate count:** 3
- **Variants:**
  - A = `variant-1-opus-architect.md`
  - B = `variant-2-opus-analyzer.md`
  - C = `variant-3-haiku-backend.md`
- **Inputs:** `diff-analysis.md`, `debate-round{1,2,3}-variant-{A,B,C}.md`, `invariant-probe.md` (all in this directory)
- **Orchestrator stance:** neutral. The orchestrator takes no side; every winner below comes from the advocates' own stated picks, concessions and agreement lists.

### Scoring rules applied

1. Each advocate's **latest** stated label for a point is used (Round 3 final table, else Round 2 revised table, else Round 1 pick).
2. A point is **resolved** when all three labels name the same winner, or when the point appears in all three Round 2 Agreement Summaries or was finalized in Round 3 with the same design content. The recorded winner is then the majority label, or `merge` when the content is a merge or all three labels differ.
3. **A-points** are scored from each advocate's ACCEPT / REJECT / QUALIFY stance and the remedy that stance names. Promoted A-points (A-002, 003, 004, 005, 007, 008, 011, 012, 013) mirror their C-039..C-047 results.
4. A point that no round file discussed is **unresolved (not debated)**.
5. **U-points** are listed in the matrix but are outside the convergence denominator, per the skill formula `agreed / (S + C + X + A)`.
6. **Taxonomy tagging** follows the concept of the point's subject and its decisive content, not literal substrings inside quoted section titles. Priority is L3 > L2 > L1, with L2 the default.

## Round 1: Advocate Statements

### Variant A Advocate (`debate-round1-variant-A.md`, 231 lines)

**Position Summary:** A's three orthogonal evidence axes with `proof_class`, cost tiers T0-T2, the L0-L5 ladder with no interrupt, person-prompt priority, the status-body acknowledgement and an explicit v1/v2 test are the right backbone. B and C supply pieces A lacks.

**Steelman:** B's root-cause analysis, its arrival-versus-change matrix and its occurrence/detection split are the strongest diagnosis among the three. C's attempt fencing and durability (persist before ack, reconcile) are the strongest recovery-integrity design.

**Key strengths claimed:**
1. `proof_class` (positive / absence / unknown) on every observation, so absence is never promoted to proof.
2. No interrupt of a worker, at any rung.
3. Person-prompt priority in the precedence order.
4. The `status` message body as the acknowledgement carrier.
5. A one-sentence test for what belongs in v1 and what waits for v2 (#423).
6. One timing-parameter table.
7. Placement of worker rules in the contract.
8. The same-cause rule against like-for-like restarts.
9. Signal and adapter registries.

**Weaknesses identified in others:**
- B: B1 manufactured stall proof (C-7/C-9); B2 interrupt on a person prompt; B3 AC-1's 20-minute bound; B4 NFR-004 call count against FR-009; B5 typing into an `ask`; B6 a 30-minute unreachable report; B7 a sweep on every wake.
- C: C1 heartbeat used as the ack; C2 the 2/5/10 ack bounds; C3 the `blocked_ask` handling; C4 self-exit from context-exhausted; C5 a 1-minute case-4 bound; C6 a 6-minute idle bound; C7 fleet cost.

**Concessions (13):** X-001 (all nine wake types, B); X-004 (exhaustion is not a proof class, C); X-010 (no typing into an ask, C); X-012/C-019 (C's restart budget); X-006 (B's finished-unreported order); S-010/C-001 (separate unreachable and exited); S-006/S-007 (B's case-mapping and contract-change layout); C-024 (B's handoff on failure); C-013/C-010 (B's scoped worktree stat and idle confirmation); C's durability; unstated assumptions; the WC-7 Skill amendment; hooks only as accelerators.

**Assumption stances:** ACCEPT A-006, A-009, A-015, A-016; REJECT A-004; QUALIFY the rest, with A-018 qualified as "nudge only at a confirmed prompt" (C's guard).

### Variant B Advocate (`debate-round1-variant-B.md`, 329 lines)

**Position Summary:** B's root-cause work (occurrence versus detection per case), the arrival matrix, the nine-type wake set and the status ack with a `queued` disposition explain the incidents. A and C supply structure and recovery safety.

**Steelman:** A's `proof_class`, evidence axes, cost tiers, ladder, adapter `Receipt` and `replaces` chain. C's fencing, crash safety, `uncertain_effects`, input guards, watchdog and WC-7 amendment.

**Key strengths claimed (12):** root cause; arrival matrix; nine-type wake; status ack with `queued`; adaptive window W; the case-8 sweep trigger; the WC-11-scoped worktree stat; H1-H4 case-5 hypotheses; the D2 freeze priority in resume notes; one home for rules; degraded mode with replay fixtures; handoff written on failure.

**Weaknesses identified in others:** seven critiques of A (A1-A7) and nine of C (C1-C9).

**Concessions (11):** interrupt is unsafe; the manufactured stall proof (called B's most serious error); precedence; AC-1's bound; NFR-004; the 30-minute unreachable report; the ask guard; C's fencing and crash safety; A's `proof_class`; a restart-budget merge (2 per 6 h plus 2 per lineage); A's parameter table (S-011).

**Assumption stances:** ACCEPT A-006, A-009, A-015 (with persist before ack), A-016, A-017; REJECT A-002, A-004, A-018 (C's FR-019 guard instead); QUALIFY the rest, with A-001 qualified toward C's watchdog and A-013 toward C's lock.

**B's own Round 1 tally:** A 13, B 27, C 11, merge 22.

### Variant C Advocate (`debate-round1-variant-C.md`, 158 lines)

**Position Summary:** C's transaction boundary, attempt identity, read-versus-execute answer lifecycle and refusal to add any new stall proof are the safety core. A's evidence split and B's case analysis should be layered on it.

**Steelman:** A's evidence / verdict / action split, cost tiers and person-first ordering. B's cause split, arrival matrix, nine-type wake, status ack and handoff.

**Key strengths claimed (8):** transaction boundary; attempt identity; read versus execute lifecycle; no new stall proof; input safety; persist before ack; degraded visibility; boundary discipline.

**Weaknesses identified in others:**
- A: the wake set; the v2 proof amendment; copying the ack into an ask; the incidental-write veto; report directories not idempotent.
- B: interrupt; precedence; S9's "contract exists" signal; AC-1 and the adaptive W; typing into an ask; silence during declared windows.

**Concessions (8):** A/B's status ack carrier; C's v1 timing overstated; a deterministic action policy is needed (A's person-first, B's exited/unreachable); A's cost tiers and parameter table; B's handoff; A/B's same-cause rule; terminal-copy qualification; a narrowing of X-020, X-003 and X-009.

**Assumption stances:** ACCEPT A-006, A-016; REJECT A-001 (watchdog), A-002, A-003, A-004, A-008, A-010, A-011, A-018; QUALIFY the rest.

**C's own Round 1 tally:** A 4, B 7, C 31, merge 31.

### Round 1 cross-variant picks (where all three already agreed)

S-005 merge, S-006 B, S-007 B, S-008 C, S-010 B; X-001 B, X-005 A, X-010 C; C-001 merge, C-002 merge, C-007 A, C-013 B, C-016 C, C-020 A, C-025 C, C-030 B, C-037 C.

## Round 2: Rebuttals

The Round 2 files have no separate steelman section. Each one answers the criticisms aimed at its variant ("Responses to Criticisms"); B and C also answer the other Round 2 files.

### Variant A Advocate (`debate-round2-variant-A.md`)

**Position Summary:** A moved in six places (Updated Assessment, lines 47-57): no automatic or person-blessed path to replace a context-exhausted worker (C's ladder is the backbone); input safety is a veto as well as a precedence; caps must survive new Task IDs; context-exhausted latches; command-internal checkpoints may live in commands; every bound is labelled v1 or v2.

**Responses to others:** answers B's and C's Round 1 critiques.

**New evidence:** WC-6 has no settlement path for a person-directed stop of a live worker, so A proposes a contract sentence ("A stop the person directs in their own session is the person's action..."); A's own L2 cap of "4 per Task" resets on each WC-6 replacement; heartbeats also stop during `check --wait`; B's adaptive W needs a gap filter; external prior art supports three concessions.

**Concessions / position changes:** 21 pick changes, including X-006, X-007, X-009, X-018, C-003, C-004, C-008, C-009, C-017, C-021, C-028, C-033..C-035, C-039..C-041 to merge, X-011 and C-018 to C, and C-026 to B.

### Variant B Advocate (`debate-round2-variant-B.md`)

**Position Summary:** B drops every path from exhaustion to L4 (exhaustion latches, then L5 with a ready plan); keeps a display precedence plus C's input veto; adopts C's persist-before-ack, fencing, `reconcile()` and lock for v2; accepts two homes for rules; labels every bound by phase; turns H1-H4 into an investigation order.

**Responses to others:** answers A's and C's Round 1 critiques and A's Round 2 file.

**New evidence:** B's own declared window (up to 45 min) suppresses its thrash trigger, so a declared window should defer typed actions only while the fixed 10-minute probe keeps running; WC-5 makes blocked and failed contracts terminal except inside WC-3's ask path; B's C-7 text read the coordinator's own actions as part of a proof; NFR-004 says three calls but FR-009 names two; `seed-brief.md:71` permits nudges and asks without making them evidence.

**Concessions / position changes:** 19, including X-004 and C-022 to C, X-007, X-014, X-015, X-017, X-018, C-003, C-005, C-008, C-011, C-014, C-017, C-023, C-031, C-033, C-041, C-043 to merge, and C-018 to C.

### Variant C Advocate (`debate-round2-variant-C.md`)

**Position Summary:** The strongest design is a merge: A's evidence axes and tiered observations, B's status-body ack, occurrence/detection analysis and v1 handoff, and C's recovery integrity and fail-closed v2 ledger. C withdraws compulsory broad inventory and tight default scheduling.

**Responses to others:** answers all 16 criticisms from A and B and responds to both Round 2 files.

**New evidence:** two unchanged reads do not prove a completed final turn (against B's C-7 rewrite and A's Round 1 assumption); persisted monotonic due times need a boot/clock-domain identity; C's own nudge cap resets per attempt, so a lineage aggregate (two automatic nudges per lineage) is proposed; a fresh contract is necessary but not proof that an answer was consumed; C's own probe budget does not prove its 6-minute bound.

**Concessions / position changes:** 10, all C to merge (C-003, X-007, C-008, C-011, C-015, C-017, C-018, C-031, X-017, C-033). C keeps C-019 and X-012 at C (one replacement per hour plus two per lineage).

### Round 2 Agreement Summaries (intersection)

- All three list as agreed in substance: X-001, X-002, X-004, X-005, X-008, X-010, X-011, X-014, X-015, X-016, X-019, X-020; C-001, C-002, C-006, C-007, C-010, C-012, C-013, C-014, C-016, C-020, C-022..C-025, C-027, C-029, C-030, C-032, C-036..C-038, C-042..C-047 (C names C-044 and C-045 as still open in wording); S-005, S-006, S-007, S-008, S-010.
- Still disputed after Round 2 (in at least one file): X-012 / C-019 (restart window), X-013 (idle latency), C-005, C-008, C-011, C-018, X-003 / C-044, C-045, X-006, declared-window behaviour (no point ID).

## Round 2.5: Invariant Probe

Source: `invariant-probe.md`.

- **Findings:** 28 in total. 17 ADDRESSED, 11 UNADDRESSED at probe time.
- **Severity:** HIGH 4, MEDIUM 16, LOW 8.
- **HIGH items:** INV-005, INV-008, INV-020, INV-023. INV-008 was already ADDRESSED in the probe. The other three were UNADDRESSED and were put to Round 3.
- **MEDIUM/LOW UNADDRESSED:** INV-001, INV-006, INV-009, INV-010, INV-011, INV-016, INV-022, INV-024. These are warnings only and do not block convergence.

### Resolution of the HIGH items after Round 3

| Item | Status after Round 3 | Basis |
|---|---|---|
| INV-005: case-1 thrash hidden by fresh heartbeats and transcript | **ADDRESSED** | All three adopt the same mechanism: a semantic-change record that excludes heartbeat arrival and transcript growth; a read-only screen plus transcript probe after 10 minutes without semantic change, which runs during declared windows too; a record or report by 15 minutes; never L4 (A R3 l.13-36, B R3 l.15-42, C R3 l.24-38). The only residual difference is one parameter: A's pattern-independent fallback is about 25 minutes (labelled degraded), against 15 minutes for B and C. |
| INV-008 | **ADDRESSED** (in the probe) | No further debate needed. |
| INV-020: answer enqueued, `ask` still blocked | **UNADDRESSED** | Each advocate proposes a resolution, but the three conflict on what the coordinator and worker do, not only on a number (details below). |
| INV-023: in-place `/clear` or compaction of a live worker | **ADDRESSED** | The three proposals are compatible and combine into one union (A R3 l.64-89, B R3 l.74-93, C R3 l.54-72). |

**INV-020, the disagreement.**
- **Report bound:** C reports by 10 minutes from first enqueue (C R3 l.42). B records by 15 minutes and reports to the person at about 25 minutes (B R3 l.65). A detects by 15 minutes on the absence route, reports at once on the positive route, with L5 as the only remedy while the ask runs (A R3 l.49-53).
- **Mailbox resend:** B re-sends the answer once as a reply to the question ID (B R3 l.63). A does not resend (A R3 l.53). C forbids a blind resend when delivery is uncertain (C R3 l.44).
- **Worker signal at the ask edges:** A adds one heartbeat on every `ask` return, answered or timed out (A R3 l.44). B adds a `status` on answer and a heartbeat on each timeout (B R3 l.52-54). C adds no new heartbeat and relies on the status-body ack at the first legal opportunity (C R3 l.46).
- **Why this is not treated like INV-005:** INV-005's three resolutions differ in one parameter of the same mechanism. INV-020's resolutions differ in actions (resend or not) and in the worker-side contract text, so the merged design has no single agreed rule yet.

**INV-023, merged resolution (union of the three):** lifecycle messages count only when their Task and Dispatch IDs match an unsettled attempt (B); two settlement paths, with an exited process settled by existing WC-6 proof and a live PTY handled by a new person-directed cancellation bullet that requires confirmed quiescence before the old Task is settled and a new Task is created (A, B, C); the person's statement in the coordinator conversation is the v1 evidence, and suspicion alone never settles (A, C); late lifecycle messages from the invalidated identity are quarantined, and dependents are stopped if Orca already accepted one (A, C); handoff files record the Task and Dispatch IDs (A); compaction is not a clear unless identity is lost (A, B, C).

**MEDIUM/LOW UNADDRESSED (warnings):** all three advocates accept fixes for INV-001, INV-006, INV-009, INV-010, INV-011, INV-016 and INV-024. For INV-022, A accepts a narrowed fix, B accepts it in part, and C accepts optional coarse declarations; all three keep commands free of Orca calls and rely on the fixed 10-minute probe.

## Round 3: Final Arguments

The Round 3 files have no separate steelman section. Each one resolves the HIGH items, answers the MEDIUM/LOW items and finalizes the points still disputed.

### Variant A Advocate (`debate-round3-variant-A.md`)

**Final position (l.3-9):** the merged design, not A alone. A contributes the extension scaffolding (signal registry, lineage-keyed action ledger, the v1/v2 test). The common principle: a v1 trigger must never depend on a signal the failing worker stops producing, or keeps producing by accident. Exhaustion never reaches L4.

**HIGH resolutions:** INV-005 by a payload-independent semantic fingerprint with a 15-minute pattern bound and a 25-minute degraded fallback; INV-020 by a heartbeat on every `ask` return plus an `ask-answer-undelivered` anomaly with no resend; INV-023 by splitting clear from compaction in Terms and treating a clear as a person-ended attempt.

**Final picks (l.106-119):** X-007/C-003 merge; X-017/C-031 merge; C-008 merge; C-011 C (scoped merge); C-018 C; C-005 merge; X-012/C-019 C; X-013 merge; X-003/C-044 C; C-045 C; declared window B; X-006 merge.

**Concessions:** accepts C on C-011, C-018, X-012/C-019, X-003/C-044 and C-045, and B on the declared window.

### Variant B Advocate (`debate-round3-variant-B.md`)

**Final position (l.3-11):** the merge stands. All three HIGH gaps share one root cause: every variant trusted the worker's own channel while the worker was in the failure state. B withdraws its Round 2 C-7 rewrite (two reads of the final turn as a stall proof).

**HIGH resolutions:** INV-005 by a semantic-stagnation probe on the coordinator's clock (15 minutes, with or without payload); INV-020 by a WC-3 amendment (status on answer, heartbeat on timeout) and an `answer_unconsumed` anomaly with one mailbox resend and a report at about 25 minutes; INV-023 by an identity check on every lifecycle message and a WC-6 bullet for the live-PTY case.

**Final picks (l.108-119):** X-003/C-044 C; X-007/C-003 merge; X-012/C-019 C; X-013 merge; C-005 merge; C-008 merge; C-011 merge; C-018 merge; C-045 C; declared window B.

**Concessions:** accepts C on X-003/C-044, X-012/C-019 and C-045, and C's scope or predicate inside the merges for C-011, C-018 and C-005.

### Variant C Advocate (`debate-round3-variant-C.md`)

**Final position (l.3-13):** adopt the merge. A heartbeat proves traffic, not useful work. Unknown evidence produces a bounded report, never an invented diagnosis or permission to restart. Keep the input veto even where it blocks the seed's terminal-copy remedy.

**HIGH resolutions:** INV-005 by separate last-traffic and last-useful-progress records with a screen read by 10 minutes and a report by 15; INV-020 by an `answered-ask-still-blocked` incident reported by 10 minutes, with no blind resend and no typing; INV-023 by an assignment-invalidation procedure with a person-directed cancellation exception.

**Final picks (l.91-105):** C-003 merge; X-007 merge; C-005 merge; C-011 merge; C-018 merge (two nudges per lineage); C-019 B; X-012 B; X-003 C; C-044 C; C-045 C; X-006 merge; C-015 merge; X-009 merge; C-033 merge; X-013 merge.

**Concessions:** accepts B's restart window (two per rolling six hours plus two per lineage) for C-019 and X-012, and A/B's capable-transcript preference for C-011.

### Round 3 outcome on the restart window (X-012 / C-019)

A and B moved to C's one replacement per 60 minutes plus two per lineage; C moved to B's two per rolling six hours plus two per lineage. The advocates crossed over, so the labels still split. All three agree on two per lineage, on the stricter failed-start and authority gates, and that neither rate is measured.

## Taxonomy Coverage

Levels: **L1** surface (naming, formatting, wording, presentation); **L2** structural (architecture, component, interface, dependency, organization); **L3** state mechanics (state, guard, boundary, invariant, concurrency, transition, validation rule). Priority L3 > L2 > L1, default L2. The tag follows the concept of the point and its decisive content, not words that happen to appear inside a quoted section title. For example, S-005 "Schema presentation" is L1 because its content is how a schema is shown, and S-010 is L3 because it decides whether unreachable and exited are separate states.

| Point | Level | Debated |
|---|---|---|
| S-001 Heading scheme | L1 | no |
| S-002 Requirement numbering | L1 | no |
| S-003 Diagrams | L1 | no |
| S-004 Citation style | L1 | no |
| S-005 Schema presentation | L1 | yes |
| S-006 Case-mapping structure | L2 | yes |
| S-007 Contract-change layout | L2 | yes |
| S-008 Durability/safety NFR section | L2 | yes |
| S-009 Acceptance layout | L1 | no |
| S-010 Unreachable vs exited as separate states | L3 | yes |
| S-011 Parameters table | L2 | yes |
| S-012 Never-on-silence list | L1 | no |
| S-013 Coordinator-side placement of rules | L2 | no |
| C-001 State model | L3 | yes |
| C-002 Precedence | L3 | yes |
| C-003 Exit from context-exhausted | L3 | yes |
| C-004 Payload fields | L2 | yes |
| C-005 Payload weight (claim vs corroboration) | L3 | yes |
| C-006 Wait filter and timeout | L3 | yes |
| C-007 Sweep composition | L2 | yes |
| C-008 Sweep trigger and cadence | L3 | yes |
| C-009 Detection bound per state | L3 | yes |
| C-010 Idle confirmation | L3 | yes |
| C-011 Screen/transcript primary or confirming | L3 | yes |
| C-012 Context-exhausted trigger | L3 | yes |
| C-013 Worktree activity | L3 | yes |
| C-014 Ack type and format | L2 | yes |
| C-015 Ack timing | L3 | yes |
| C-016 Ack idempotency | L3 | yes |
| C-017 Ladder steps | L3 | yes |
| C-018 Ladder caps | L3 | yes |
| C-019 Restart budget | L3 | yes |
| C-020 Same-cause rule | L3 | yes |
| C-021 Resume-note format | L2 | yes |
| C-022 Exhaustion as stall proof | L3 | yes |
| C-023 Where worker rules live | L2 | yes |
| C-024 Handoff artifact | L2 | yes |
| C-025 Chunked reads (context boundary) | L3 | yes |
| C-026 New WC numbers | L1 | yes |
| C-027 Amended WC rules | L2 | yes |
| C-028 v1/v2 split | L2 | yes |
| C-029 Adapter | L2 | yes |
| C-030 Hooks | L2 | yes |
| C-031 Case-5 hypothesis | L2 | yes |
| C-032 Case-4 mechanism | L3 | yes |
| C-033 Case-1/8 response | L3 | yes |
| C-034 Nudge text (guarded typing) | L3 | yes |
| C-035 Unknown types | L3 | yes |
| C-036 Unreachable handling | L3 | yes |
| C-037 Durable state | L3 | yes |
| C-038 Portability | L2 | yes |
| C-039 (A-002) Coordinator context cost | L2 | yes |
| C-040 (A-003) Empty-wait cost | L2 | yes |
| C-041 (A-004) Ack within the timeout | L3 | yes |
| C-042 (A-005) `agentWait` reliability | L2 | yes |
| C-043 (A-007) Payload reaches coordinator | L2 | yes |
| C-044 (A-008) Final-turn finality | L3 | yes |
| C-045 (A-011) Clock comparability | L3 | yes |
| C-046 (A-012) Resume input exists | L2 | yes |
| C-047 (A-013) Single coordinator | L3 | yes |
| X-001 Heartbeat in the wake set | L3 | yes |
| X-002 Interrupt | L3 | yes |
| X-003 Manufactured stall proof | L3 | yes |
| X-004 Exhaustion as a proof class | L3 | yes |
| X-005 Precedence: person prompt vs exhausted | L3 | yes |
| X-006 Precedence: finished-unreported vs exhausted | L3 | yes |
| X-007 Self-exit from exhausted | L3 | yes |
| X-008 Ack carrier | L2 | yes |
| X-009 C's ack bounds | L3 | yes |
| X-010 Typing into an ask | L3 | yes |
| X-011 Typing into a working session | L3 | yes |
| X-012 Restart budget | L3 | yes |
| X-013 Idle bound | L3 | yes |
| X-014 B's 20-minute AC | L3 | yes |
| X-015 B's call count | L2 | yes |
| X-016 Unreachable report time | L3 | yes |
| X-017 Case-5 ranking | L2 | yes |
| X-018 Rule home in commands | L2 | yes |
| X-019 Stop hook | L2 | yes |
| X-020 Heartbeat in an ask | L3 | yes |
| X-021 C's case-4 v1 bound | L3 | yes |
| A-001 Coordinator stays responsive | L3 | yes |
| A-002 Sweep output vs coordinator context | L2 | yes |
| A-003 Empty-wait cost | L2 | yes |
| A-004 Worker can ack within the timeout | L3 | yes |
| A-005 `agentWait` populated reliably | L2 | yes |
| A-006 `--wait-submit` terminal-only | L2 | yes |
| A-007 Raw payload reaches the coordinator | L2 | yes |
| A-008 Transcript shows a finished final turn | L3 | yes |
| A-009 Nudges and asks allowed on silence | L3 | yes |
| A-010 Workers follow written rules | L2 | yes |
| A-011 Clocks comparable across hosts | L3 | yes |
| A-012 Resume input exists | L2 | yes |
| A-013 Single coordinator | L3 | yes |
| A-014 `worker-list` fresh within one sweep | L3 | yes |
| A-015 Whole batch before `--ack` loses nothing | L3 | yes |
| A-016 Arrival is not progress | L3 | yes |
| A-017 Explicit `--types` list wakes each type | L3 | yes |
| A-018 Typed text into a busy session is queued | L3 | yes |

**U-point tags (outside the denominator):** L2 = U-003, U-007, U-011, U-012, U-016, U-018, U-021, U-027, U-033, U-034, U-035, U-036 (12). L3 = the other 24.

### Counts and coverage gate

| Level | Points | Debated | Not debated |
|---|---|---|---|
| L1 | 8 | 2 (S-005, C-026) | 6 (S-001, S-002, S-003, S-004, S-009, S-012) |
| L2 | 34 | 33 | 1 (S-013) |
| L3 | 57 | 57 | 0 |
| **Total** | **99** | **92** | **7** |

**Coverage gate: PASS.** Every level that has points has at least one debated point. Note that 6 of the 8 L1 points were never debated; they are cosmetic and unresolved, not disputed.

## Scoring Matrix

Confidence is the orchestrator's confidence that the advocates agree on the recorded winner: **High** = same label from all three, or agreed in all three Round 2 Agreement Summaries; **Medium** = the same design content under differing labels, finalized in Round 3; **n/a** = unresolved. It is not a measure of runtime correctness. "R1/R2/R3" name the round file of each advocate.

### Structural (S)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 Heading scheme | UNRESOLVED (not debated) | n/a | No round file discusses it. |
| S-002 Requirement numbering | UNRESOLVED (not debated) | n/a | No round file discusses it. |
| S-003 Diagrams | UNRESOLVED (not debated) | n/a | No round file discusses it. |
| S-004 Citation style | UNRESOLVED (not debated) | n/a | No round file discusses it. |
| S-005 Schema presentation | merge | High | All three R1 picks merge; in all three R2 Agreement Summaries. |
| S-006 Case-mapping structure | B | High | All three R1 picks B; A concession; in all three R2 Agreement Summaries. |
| S-007 Contract-change layout | B | High | All three R1 picks B; A concession; in all three R2 Agreement Summaries. |
| S-008 Durability/safety NFR section | C | High | All three R1 picks C; B R2 Updated Assessment 3 adopts it. |
| S-009 Acceptance layout | UNRESOLVED (not debated) | n/a | No round file discusses it. |
| S-010 Unreachable vs exited | B | High | All three R1 picks B; in all three R2 Agreement Summaries. |
| S-011 Parameters table | A | High | A R1 strength 6; B R1 concession 11; C R1 concession 4. |
| S-012 Never-on-silence list | UNRESOLVED (not debated) | n/a | No round file discusses it. |
| S-013 Coordinator-side placement | UNRESOLVED (not debated) | n/a | No round file discusses it as a structural point; the rule-home content is scored under X-018 / C-023. |

### Content (C)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| C-001 State model | merge | High | All three R1 merge (A's axes plus B/C states); unanimous in R2. |
| C-002 Precedence | merge | High | All three R1 merge; person-first order plus C's input veto (A R2 UA-2, B R2 UA-2). |
| C-003 Exit from context-exhausted | merge | High | All three R3 merge: A's latch with C's completed-unit predicate. |
| C-004 Payload fields | merge | High | A R2 merge (A fields, B fallback, C epoch/seq); B and C merge; in B and C R2 agreed lists. |
| C-005 Payload weight | merge | High | All three R3 merge: a claim needs a completed-unit corroboration. |
| C-006 Wait filter and timeout | B | High | A and B R1 B, C merge with the same content; all three R2 agreed. |
| C-007 Sweep composition | A | High | All three R1 A (cost tiers). |
| C-008 Sweep trigger and cadence | merge | High | All three R3 merge: due timer at S, any wake once due, at most once per S. |
| C-009 Detection bound per state | merge | High | A R2 merge; B and C merge: 15-minute v1, tighter v2 targets labelled. |
| C-010 Idle confirmation | B | High | A and B R1 B; C merge with the same content; all three R2 agreed. |
| C-011 Transcript vs screen | merge | Medium | B and C R3 merge, A R3 "C (scoped merge)": transcript preferred only when current and capable; screen confirms. |
| C-012 Context-exhausted trigger | merge | High | Labels A / merge / C; content agreed in all three R2 summaries (two sources, latch). |
| C-013 Worktree activity | B | High | All three R1 B (WC-11-scoped stat). |
| C-014 Ack type and format | merge | High | B R2 merge: status-body carrier (A/B) with C's identity, digest and disposition; all three R2 agreed. |
| C-015 Ack timing | merge | High | A and B R1 merge; C R2/R3 merge: first-enqueue age plus status opportunity. |
| C-016 Ack idempotency | C | High | All three R1 C. |
| C-017 Ladder steps | merge | High | All three R2 merge: A's L0-L5, no interrupt, C's reconcile/stop/settle gate. |
| C-018 Ladder caps | merge | High | B and C R3 merge, A R3 C; same content: lineage-keyed caps, two automatic nudges per lineage. |
| C-019 Restart budget | UNRESOLVED | n/a | A R3 and B R3 pick C (1 per 60 min + 2 per lineage); C R3 picks B (2 per rolling 6 h + 2 per lineage). 2 per lineage agreed. |
| C-020 Same-cause rule | A | High | All three R1 A. |
| C-021 Resume-note format | merge | High | A R2 merge, B and C merge: A's note, B's D2 priority, C's `uncertain_effects`. |
| C-022 Exhaustion as stall proof | C | High | A and C R1 C; B R2 moves to C. |
| C-023 Where worker rules live | merge | High | B R2 merge; A and C merge: contract section 3 plus command-internal checkpoints. |
| C-024 Handoff artifact | merge | High | Labels B / merge / merge; all three R2 agreed (B's handoff on failure). |
| C-025 Chunked reads | C | High | All three R1 C. |
| C-026 New WC numbers | B | High | B and C R1 B; A R2 moves to B. |
| C-027 Amended WC rules | merge | High | All three merge; all three R2 agreed. |
| C-028 v1/v2 split | merge | High | A R2 merge; B and C merge: A's test plus phase labels on every bound. |
| C-029 Adapter | merge | High | All three merge. |
| C-030 Hooks | B | High | All three R1 B (hooks optional accelerators). |
| C-031 Case-5 hypothesis | merge | High | All three R2/R3 merge: cause UNVERIFIED, H1-H4 as investigation order. |
| C-032 Case-4 mechanism | B | High | A and B R1 B; C merge with the same content; all three R2 agreed. |
| C-033 Case-1/8 response | merge | High | All three R2 merge: latch, L5 with ready plan, never L4 on exhaustion. |
| C-034 Nudge text | merge | High | All three merge: B's text, A's reply id, only at an identified prompt. |
| C-035 Unknown types | merge | High | A R2 merge, B merge; C label C, but C lists C-035 as agreed. |
| C-036 Unreachable handling | A | High | A and B R1 A; C label C with agreement in all three R2 summaries. |
| C-037 Durable state | C | High | All three R1 C. |
| C-038 Portability | C | High | A and C R1 C; B merge; all three R2 agreed. |
| C-039 (A-002) Context cost | merge | High | All three merge after A R2: cap output to changed workers, measure multi-hour budget. |
| C-040 (A-003) Empty-wait cost | merge | High | All three merge: UNVERIFIED, measure in replay fixtures. |
| C-041 (A-004) Ack within timeout | merge | High | All three merge: status opportunity plus `queued`; deadlines bound read_unknown only. |
| C-042 (A-005) `agentWait` reliability | merge | High | Labels C / merge / merge; all three R2 agreed. |
| C-043 (A-007) Payload reaches coordinator | merge | High | B R2 merge; A C, C merge; all three R2 agreed (conformance gate). |
| C-044 (A-008) Final-turn finality | C | High | All three R3 C: two identical reads never prove a completed final turn. |
| C-045 (A-011) Clock comparability | C | High | All three R3 C: monotonic due times with clock-domain identity. |
| C-046 (A-012) Resume input exists | C | High | A C, B C, C merge; all three R2 agreed. |
| C-047 (A-013) Single coordinator | C | High | All three C (controller lock). |

### Contradictions (X)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| X-001 Heartbeat in wake set | B | High | All three R1 B (all nine types). |
| X-002 Interrupt | A | High | A and B pick A, C picks C with the same content (never interrupt); all three R2 agreed. |
| X-003 Manufactured stall proof | C | High | All three R3 C; B withdraws its C-7 rewrite. |
| X-004 Exhaustion as proof class | C | High | A and C R1 C; B R2 moves to C. |
| X-005 Person prompt vs exhausted | A | High | All three R1 A. |
| X-006 Finished-unreported vs exhausted | merge | High | All three R3 merge: final `worker_status`, no open ask, no remaining `Command:` line, input veto. |
| X-007 Self-exit | merge | High | All three R2/R3 merge (latch). |
| X-008 Ack carrier | A | High | A and C pick A, B picks B with the same content (status body); all three R2 agreed. |
| X-009 C's ack bounds | merge | High | A R2 merge, C R3 merge; B lists it agreed: escalation deadlines, not proof of a missed read. |
| X-010 Typing into an ask | C | High | All three R1 C. |
| X-011 Typing into a working session | C | High | B and C R1 C; A R2 moves to C. |
| X-012 Restart budget | UNRESOLVED | n/a | Same crossed split as C-019. |
| X-013 Idle bound | merge | High | All three R3 merge: 15 minutes in v1; 6-minute v2 profile only after a capacity test. |
| X-014 B's 20-minute AC | merge | High | B R2 merge, C merge, A label A; all three R2 agreed (15 min to a recorded state). |
| X-015 B's call count | merge | High | B R2 merge, C merge, A label A; all three R2 agreed (fixed calls plus O(n) stats). |
| X-016 Unreachable report time | A | High | A and B pick A, C picks C; all three R2 agreed (report by ten minutes). |
| X-017 Case-5 ranking | merge | High | All three R2 merge. |
| X-018 Rule home in commands | merge | High | A and B R2 merge, C merge. |
| X-019 Stop hook | merge | High | Labels B / merge / C; all three R2 agreed (no compulsory Stop hook). |
| X-020 Heartbeat in an ask | A | High | A and B pick A, C merge (narrowed); all three R2 agreed. |
| X-021 C's case-4 v1 bound | merge | High | B picks B, A picks A, C merge; all three R2 agreed (five-minute v1 cycle, 1-minute drain only in v2). |

### Assumptions (A)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| A-001 Coordinator stays responsive | C | High | A, B qualify, C rejects; all name C's watchdog (with the person as the v1 backstop). |
| A-002 Sweep output vs context | merge | High | Mirrors C-039. |
| A-003 Empty-wait cost | merge | High | Mirrors C-040. |
| A-004 Worker can ack in time | merge | High | All three REJECT; remedy mirrors C-041. |
| A-005 `agentWait` reliability | merge | High | Mirrors C-042. |
| A-006 `--wait-submit` terminal-only | merge | High | All three ACCEPT. |
| A-007 Payload unmodified | merge | High | Mirrors C-043. |
| A-008 Finished final turn | C | High | Mirrors C-044. |
| A-009 Nudges and asks allowed | merge | High | A and B ACCEPT, C QUALIFY; all keep them as actions, never evidence (B R2 NE-5). |
| A-010 Workers follow rules | merge | High | Written rules plus a detection backstop (C's conformance test, A's v2 hook only as accelerator). |
| A-011 Clock comparability | C | High | Mirrors C-045. |
| A-012 Resume input exists | C | High | Mirrors C-046. |
| A-013 Single coordinator | C | High | Mirrors C-047. |
| A-014 `worker-list` freshness | merge | High | All QUALIFY: a projection stale after two sweeps means unknown. |
| A-015 Whole batch before `--ack` | merge | High | A and B ACCEPT, C QUALIFY: whole batch, persist before ack in v2. |
| A-016 Arrival is not progress | merge | High | All three ACCEPT. |
| A-017 Explicit `--types` list | merge | High | A QUALIFY, B ACCEPT, C QUALIFY: explicit nine-type list, tested at runtime. |
| A-018 Busy-session typing queued | C | High | A QUALIFY toward C's guard, B and C REJECT: type only at an identified prompt. |

### Unique contributions (U), outside the denominator

Winner is the originating variant. "Status" records how the other two advocates treated it.

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| U-001 Three orthogonal axes | A | High | Endorsed by all three. |
| U-002 `proof_class` | A | Medium | Partial: B adopts it (R1 concession); C praises it in its steelman only. |
| U-003 Cost tiers T0-T2 | A | High | Endorsed by all three (C-007). |
| U-004 Reply-id `R-<task>-<n>` | A | Medium | Partial: used inside the C-034 and INV-020 merges. |
| U-005 v2 Stop hook | A | High | Rejected: no compulsory Stop hook (X-019, C-030). |
| U-006 Adapter `Receipt` | A | High | Endorsed by all three. |
| U-007 Timing-parameter table | A | High | Endorsed by all three (S-011). |
| U-008 `expect_until` declaration | A | Medium | Partial: kept, but declared windows defer typed actions only (B R2 NE-1). |
| U-009 `replaces` chain as work unit | A | Medium | Partial: becomes the lineage key (A R2 UA-3), with C's lineage ID. |
| U-010 Arrival-vs-change matrix | B | High | Endorsed by all three (A-016). |
| U-011 Occurrence vs detection split | B | High | Endorsed by all three (S-006). |
| U-012 Case-5 H1-H4 | B | Medium | Partial: kept only as an unranked, UNVERIFIED investigation order. |
| U-013 Case-4 batch-ack hypothesis | B | High | Endorsed by all three (C-032). |
| U-014 Adaptive window W | B | Medium | Partial: C qualified; A requires a gap filter (A R2 NE-4). |
| U-015 Case-8 sweep trigger | B | High | Endorsed by all three. |
| U-016 Replay fixtures | B | Medium | Partial: used as a measurement gate. |
| U-017 Degraded mode, versioned patterns | B | Medium | Partial: patterns live in adapter data (A R3 INV-005). |
| U-018 Handoff on failure | B | High | Endorsed by all three (C-024). |
| U-019 Unacked-at-settlement | B | n/a | Not debated as a point; C R3 INV-020 uses the term. |
| U-020 D2 freeze in resume note | B | High | Endorsed by all three (C-021). |
| U-021 Self-verified CLI behaviour | B | Medium | Partial. |
| U-022 `attempt_epoch` fencing | C | High | Endorsed by all three (v2). |
| U-023 Checkpoint `sha256` | C | Medium | Partial. |
| U-024 Answer lifecycle | C | Medium | Partial: read versus applied kept; full lifecycle v2. |
| U-025 Persist before ack | C | High | Endorsed by all three. |
| U-026 Monotonic time, `coverage_degraded` | C | High | Endorsed by all three (C-045). |
| U-027 Control envelope JSON | C | Medium | Partial: v2 only. |
| U-028 `uncertain_effects` | C | High | Endorsed by all three. |
| U-029 `reconcile()` and crash tests | C | Medium | Partial: B and C explicit, A not explicit. |
| U-030 Untrusted-input limits | C | High | Endorsed by all three (C-035). |
| U-031 Controller lock | C | High | Endorsed by all three (C-047). |
| U-032 Watchdog | C | High | Endorsed by all three (A-001). |
| U-033 WC-7 Skill amendment | C | High | Endorsed by all three (A R1 concession). |
| U-034 Staged rollout | C | Medium | Partial. |
| U-035 Failure injection after a sweep | C | n/a | Not debated. |
| U-036 Retention and redaction | C | n/a | Not debated. |

**Not in the matrix:** declared-window behaviour (B R2 New Evidence 1) has no point ID. All three agree with B: a declared window defers typed actions only, and the fixed 10-minute read-only probe keeps running (A R3 90%, B R3 85%, C R2 accepts).

## Convergence Assessment

| Category | Points | Resolved | Unresolved |
|---|---|---|---|
| S | 13 | 6 | 7 (S-001, S-002, S-003, S-004, S-009, S-012, S-013; none debated) |
| C | 47 | 46 | 1 (C-019) |
| X | 21 | 20 | 1 (X-012) |
| A | 18 | 18 | 0 |
| **Total (denominator)** | **99** | **90** | **9** |
| U (outside the denominator) | 36 | 19 (18 endorsed by all, plus U-005 rejected by all) | 17 (14 partial, 3 not debated) |

- **Points resolved:** 90 of 99.
- **Alignment:** 90 / 99 = **90.9%**. For transparency only, counting the 19 agreed U-points as well gives 109 / 135 = 80.7%.
- **Threshold:** 75%. The score is above it.
- **Taxonomy gate:** PASS (L1, L2 and L3 each have at least one debated point).
- **HIGH invariants:** INV-005 ADDRESSED, INV-008 ADDRESSED, INV-023 ADDRESSED, **INV-020 UNADDRESSED**.
- **Status: NOT_CONVERGED.** The score and the taxonomy gate pass, but INV-020 is a HIGH invariant that the advocates resolved in three incompatible ways. Under the skill's rule, any HIGH UNADDRESSED invariant blocks convergence.
- **Unresolved points:**
  1. **C-019 / X-012, restart window.** One replacement per 60 minutes plus two per lineage, against two per rolling six hours plus two per lineage. The advocates crossed over in Round 3 (A and B to C's value, C to B's). All agree that both values are policy, not measured.
  2. **S-001, S-002, S-003, S-004, S-009, S-012, S-013.** Never debated. Six are L1 presentation choices; S-013's content is covered by the X-018 / C-023 merge.
- **MEDIUM warnings (not blocking):** INV-001, INV-006, INV-009, INV-010, INV-011, INV-016, INV-024 have fixes accepted by all three. INV-022 is accepted narrowed (A), in part (B) and as optional coarse declarations (C).

### Merge guidance

1. **Backbone:** A's three evidence axes with `proof_class` and cost tiers; B's occurrence/detection split, status-body acknowledgement and handoff files; C's proof, reconcile, stop and settle gates with the absolute input veto. All three Round 3 files state this merge.
2. **Never a stall proof:** context exhaustion, heartbeats, repeated identical transcript reads and the coordinator's own nudges never settle an attempt. Only Orca's three stall proofs, or the person's recorded stop under the proposed WC-6 amendment, do (X-003, X-004, C-022, C-044).
3. **INV-005:** adopt the shared semantic-change probe. Use the 15-minute record-or-report bound (B and C). A's 25-minute degraded fallback is the outlier; the 15-minute bound covers its case because the fallback outcome is a report, not an action.
4. **INV-020 (still open; the merge must decide it):**
   - No blind mailbox resend while delivery is uncertain (A and C). B's single resend with the same reply id is the alternative.
   - An L5 report to the person within 10-15 minutes of enqueue (C 10, A 15). B's 25 minutes is the slower option.
   - A worker signal when `ask` returns, so "answered" is observable (A heartbeat, B status plus timeout heartbeat). C's status-body ack at the first legal opportunity is the minimum all three accept.
   - The input veto stays absolute; a typed copy only at a positively identified idle prompt.
5. **INV-023:** apply the union in the Round 2.5 section: ID check on every lifecycle message, two settlement paths, the person's statement as evidence, quarantine of late messages, IDs in the handoff file.
6. **Restart window (C-019 / X-012):** keep two per lineage (agreed) and choose the rate window explicitly, labelled as unmeasured policy. Revisit with replay data.
7. **Phase labels:** every bound, ack deadline and cost claim carries v1 or v2. v1 commits to 15 minutes with available evidence; C's 6-minute and 1-minute figures are v2 profiles gated on a capacity test.
8. **Declared windows:** defer typed actions only; the fixed 10-minute read-only probe keeps running.

## Points Won per Variant

Counted over the 99 points in the denominator. `merge` and unresolved points are not credited to any variant.

| Variant | Points won | Points |
|---|---|---|
| A | 9 | X-002, X-005, X-008, X-016, X-020; C-007, C-020, C-036; S-011 |
| B | 10 | X-001; C-006, C-010, C-013, C-026, C-030, C-032; S-006, S-007, S-010 |
| C | 20 | X-003, X-004, X-010, X-011; C-016, C-022, C-025, C-037, C-038, C-044, C-045, C-046, C-047; S-008; A-001, A-008, A-011, A-012, A-013, A-018 |
| merge | 51 | 10 X, 28 C, 1 S, 12 A |
| unresolved | 9 | C-019, X-012, S-001, S-002, S-003, S-004, S-009, S-012, S-013 |
| **Total** | **99** | |

U-points by originating variant (outside the count): A 9, B 12, C 15.
