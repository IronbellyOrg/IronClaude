# Adversarial Debate Transcript (D10 wake transport)

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe
- Convergence achieved: 80% (12 of 15 diff points agreed), then BLOCKED_BY_INVARIANTS (2 HIGH UNADDRESSED invariants)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, Variant 2 = CLAY), plus 1 independent fault-finder
- Full statements are kept as separate files in this folder; this transcript condenses them and cites the file:
  - `round1-advocate-1-ours.md`, `round1-advocate-2-clay.md`
  - `round2-rebuttal-1-ours.md`, `round2-rebuttal-2-clay.md`
  - `invariant-probe.md` (28 findings)
- Process notes: the advocates were Task agents given read access to the code exports and told to verify, not trust. The CLAY advocate ran one read-only `gh issue view 516` against `IronbellyOrg/Coder` (outside the `--repo IronbellyOrg/IronClaude` rule of the common brief); it disclosed it. The orchestrator's own earlier reads of Coder issues 477, 515 and 516 were the same kind (read-only, repo `IronbellyOrg/Coder`, because the topic names Coder issue 477). No write happened.

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)
**Position**: Add no delivery channel. Launch one claim session through one Orca verb with an integer-only prompt; the coordinator pulls the claim's files. Concedes there is no acknowledgment and no answer for a down coordinator; recommends keeping OURS as the transport and taking Clay's durable file plus acknowledgment as an optional layer.

**Steelman of Variant 2**: a fire-and-forget launch cannot notice a dead session; Clay's durable file is the truth, delivery is at-least-once with 3 resends and an unread mark, the security rule covers every channel, an idle poll costs no tokens, the typed line is existing report-waker practice, and Clay discloses its weak points (K11, K16, U5, U25).

**Key strengths claimed**: D1 option A and NG-1 reject push designs (`issue-watcher.md:47`, `:76`); one integer reaches the prompt (`launch.py:33`, `:84-92`); one Orca verb with an operation id (`launch.py:96-132`); no copied terminal code (`orca_term.py:3`); owner Q3 narrowed Coder 477; Clay's wake is unproven by its own register (D:1233, D:1263, D:1283); typing races a person (`wake.py:746`).

**Weaknesses identified in Variant 2**: mailbox may not work (U5); a copy of about 100 lines with no parity test against the original; the wake file carries an issue title (D:185); a larger surface (8,322 lines) with no consumer yet; starting a session is an extra script action.

**Concessions**: decision 6 covers worker approvals only; OURS has no ack and no push to a running coordinator; OURS is also unproven live; cost per claim is one model session.

**Corrections found**: the parity tests exist on master, so PR 686 did not add them; `WORKER-CONTRACT.md:300` is about worker plan approval; Q36 is approval latency; `issue-watcher.md:43` is a merge-ordering note.

### Variant 2 Advocate (CLAY)
**Position**: Only Clay's line has a wake at all. The coordinator cannot see a claim while it sits in a long wait; the mailbox reaches a busy session; delivery is checkable; typed line is practice on master; no tokens until read; a down coordinator is started.

**Steelman of Variant 1**: every channel is attack surface; the launch is one verb with a pending record, operation id and retry; the claim leaves plain files the coordinator reads; the integer-only rule stays in one place; honest about its gaps.

**Concessions**: wake unproven live; about 100 copied lines with no parity test for the copy; typing race narrowed not closed; the plan-request title is GitHub text for the model; nothing consumes a wake until PR B exists.

**Corrections found**: Q36 and decision 6 stretched by OURS; `orca_term.py:3` is a header note, not a repo rule; line-range drift of 1 to 3 lines in D:112's `orca_term.py` citation; Clay's own claim about issue 516 was cut to the header.

## Round 2: Rebuttals

### Variant 1 Rebuttal (OURS)
Conceded C-001 (65% to CLAY) and C-006 (55% to CLAY): the poll never signals the coordinator. Argued that a bounded `check --wait` (`WORKER-CONTRACT.md:101` 300000 ms; D:572 and D:748 240000 ms) plus a sweep "after every wake or timeout" (`:110`) already gives a pull every 4 to 5 minutes, so the mailbox buys little, if the loop is told to read the claim store or the wake directory (UNVERIFIED that master says so). Backed a HYBRID: file plus ack plus unread mark required; typed line only to an idle person-opened session; mailbox optional behind U5; integer-only launch for a start needs a second fixed pattern and a spike on whether `orca agent launch` carries the ccsession tag. Separable: envelope, atomic write, ack buckets, `build_wake_line`, resend and unread logic, session lookup. Not separable: `assigned[]` (assignment-only trigger), `plan_requests[]` (plan hold), `target.resume`. New fact: PR 686's poll claims nothing, so D10 entangles with "who claims".

### Variant 2 Rebuttal (CLAY)
Accepted that the bounded wait covers a looping coordinator and that the pull is not yet written in the design (`D:571` lists "the state files"; no line tells wave 5 to scan `wakes/`); accepted the typed line is for an idle person-opened session or a freshly started one (D:319, D:710). Conceded the copy and the parity-test error. Accepted separating the envelope; `assigned[]` can ride as plain numbers; defer `plan_requests[]`; conceded no titles in the wake file; proposed a neutral ack bucket name `accepted`. Accepted the HYBRID with three conditions (wave 5 scans `wakes/` on each timeout; one fixed-pattern start only if a live spike passes; one shared terminal helper with a parity test before a second consumer ships). Rejected dropping the typed line.

## Round 2.5: Invariant Probe
See `invariant-probe.md`. 28 findings: 8 ADDRESSED, 20 UNADDRESSED (HIGH 2, MEDIUM 15, LOW 3). The orchestrator re-read the code behind both HIGH items (`pr-a` `cycle.py:752-810`, `route.py:407-413`, `:592-603`; `master` `orchestrator.md:536-539`) and they stand:
- INV-001 (HIGH): the acknowledgment makes the poll mark the entry acked and move the wake file to `wakes/done/` (`cycle.py:786-810`); the order "record first, acknowledgment second" is pinned only for plan requests (D:539), not for assigned items (D:536). A crash between the ack and the state file loses the issue.
- INV-002 (HIGH): an entry that runs out of attempts is abandoned and never woken again; its wake files name an orchestrator that route.py can mark ended (`route.py:407-413`, `:598-602`), so a new orchestrator rejects them as `wrong_target` and the directory scan cannot recover them.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | none (not a merit point) | 90% | 3 steps against 5 reflects scope. |
| C-001 | CLAY (hybrid) | 62% | Only CLAY reaches the coordinator; a bounded wait already covers a looping session if wave 5 scans the wake directory (not yet written). |
| C-002 | CLAY | 85% | Ack, resend, unread mark (D:112); OURS has only the pending guard. But see INV-001, INV-002: the ack protocol needs two fixes. |
| C-003 | tie | 95% | Both reject the listener; owner Q3 narrowed Coder 477 to read-only with no prompt routing. |
| C-004 | OURS | 65% | One verb with receipt and operation id, if a spike shows it carries the ccsession tag and a first prompt. |
| C-005 | OURS | 78% | `orca_term.py:3` "reused, never copied"; `wake.py:12` "duplicates ... on purpose"; no parity test for the copy. |
| C-006 | CLAY (weak) | 55% | Decision 6 covers worker approvals only; the line holds a wake id; but INV-007 finds a guard gap (a dialog shows an empty draft). |
| C-007 | CLAY | 72% | Idle poll costs no tokens (D:120); OURS starts a model session per claim. |
| C-008 | CLAY | 70% | The poll starts a session when none is live (D:112); OURS idles. But INV-008 shows a blind lookup starts duplicates. |
| X-001 | split | 55% | Report waker exists on master; the orchestrator wake has no live run. |
| X-002 | OURS on origin, CLAY on breadth | 65% | D3 is the owner's; the wider rule (D:234) is an improvement; the title-in-file weakness is conceded, so titles are dropped. |
| U-001 | OURS | 68% | Q3 narrows 477; decision 6 is narrower than first claimed. |
| U-002 | OURS | 65% | Pending write and operation-id retry protect the claim; live replies are still assumed. |
| U-003 | CLAY | 82% | Durable file plus ack makes loss loud (K14), with fixes INV-001, INV-002. |
| U-004 | CLAY | 62% | The rule on every argv (D:234) stands; the title in the file is dropped. |
| A-001 | agreed QUALIFY | 80% | Push is for latency below about 4 minutes and for non-looping sessions; the loop must read the file. |
| A-002 | disputed | 55% | OURS rejects as a premise; CLAY qualifies (typed half only). INV-007 shows the guard is incomplete. |
| A-003 | agreed ACCEPT | 90% | Single host for both lines. |
| A-004 | agreed QUALIFY | 85% | Envelope separable; `assigned[]` as plain numbers; `plan_requests[]` deferred. |

## Convergence Assessment
- Points resolved: 12 of 15 diff points (S-001, C-001 to C-008, A-001, A-003, A-004); unresolved: X-001, X-002, A-002
- Alignment: 80%
- Threshold: 80%
- Taxonomy coverage: L1, L2, L3 all covered (AD-5 gate satisfied)
- Status: BLOCKED_BY_INVARIANTS. Two HIGH UNADDRESSED invariants (INV-001, INV-002). Standard depth has no Round 3, so they are not debated further; unattended mode records them as unaddressed invariants and carries them into the refactoring plan as mandatory conditions of adopting the CLAY wake path.
- Unresolved points: X-001, X-002, A-002 (all three resolve in substance: X-001 both halves true; X-002 not a factual conflict; A-002 the guard is incomplete per INV-007)
