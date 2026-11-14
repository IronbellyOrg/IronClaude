# Adversarial Debate Transcript: Q2 (watcher claim level and permission acceptance)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% (13 of 13 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned in parallel as sub-agents (general-purpose type): Variant 1 persona security, Variant 2 architect, Variant 3 analyzer. No failures.
- Variant map: Variant 1 = proposal-A (claim-only, decline the permission acceptance, FU-1 waits); Variant 2 = proposal-B (keep the default `worktree` level, gated on the claim command's ship gates, acceptance for both sessions); Variant 3 = proposal-C (claim-only, accept permission-free for the one test issue).

## Round 1: Advocate Statements

Full statements are kept once in their own files: `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round1-advocate-V3.md`.

### Variant 1 Advocate (security)
Variant 1 is the only answer that does not rest on the assumption that a permission-free session makes only the intended writes. Concedes: it blocks all downstream learning; a permission-on session may be impossible unattended, and a third permission source (flags Orca passes by default, `README.md:578`, UNVERIFIED) may also need changing; the owner can author the test issue, which shrinks the untrusted-input risk. Neutral recommendation: **Variant 3, hardened, 70 percent**.

### Variant 2 Advocate (architect)
Variant 2 alone names the ship gates as FU-1 preconditions, and one of them (OB-H1 item 5) binds a claim at any level. Concedes: two permission-free sessions per approval; keeping the default ratifies a confirmed accident (ADJ X-001, 91 percent) against recorded design decision D2; unowned per-claim worktrees and agents; the full gate list is wrong for claim-only. Neutral recommendation: **Variant 3, 75 percent**, with Variant 2's item-5 gate folded in.

### Variant 3 Advocate (analyzer)
Variant 3 matches recorded decision D2 and keeps the exposure to one session on one test issue. Concedes: "FU-1 can run" is wrong as written, because OB-H1 item 5 is required before a claim at any level and is recorded "Pending, none run" (`docs/designs/sc-issue-launch-level-hook.md:625`, verified by the orchestrator); FU-1 also needs the live-test grant, Orca availability and Q20. Neutral recommendation: **Variant 3, 70 percent**, with the preconditions stated in full.

### Shared-assumption responses (omission check: none omitted)

| Point | V1 advocate | V2 advocate | V3 advocate |
|---|---|---|---|
| A-001 (FU-1's writes covered by Q2 alone) | REJECT | REJECT | REJECT |
| A-002 (a permission-free session makes only intended writes) | REJECT | REJECT | REJECT |
| A-003 (Orca reachable and Q20 answered) | QUALIFY | QUALIFY | QUALIFY |

All three cite the spec: "The first rollout is therefore a bounded test under `GRANT(WA-04,live-test)` with the owner's consent" (`merged-requirements.md:331`, verified) and dependency row 72 lists `GRANT(WA-04,live-test)` beside Q2 (`:719`, verified). All three agree the FU-1 write list is the intended set, not a limit, so the written acceptance covers whatever the one session does on the test issue.

### Facts verified by the orchestrator during the round
- `docs/designs/sc-issue-launch-level-hook.md:625`: "Pending, none run: OB-H1 items 1 to 9, OB-H2, OB-H3 ... §7 U1 requires ... OB-H1 item 5 (self-started turns wrapped) before a claim at any" level. So under every option FU-1 waits for item 5. Whether this line on this branch is current on master is UNVERIFIED.
- `merged-requirements.md:331` and `:719`: the live-test grant row is required for FU-1.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | none (identical) | 90% | Identical structure by design; agreed. |
| C-001 | L3 | Variant 3 (tied with Variant 1) | 88% | 3 of 3: `--pipeline none` matches recorded decision D2 (`issue-watcher.md:44`) and halves the permission-free sessions; the Variant 2 advocate conceded the default is an accident (ADJ X-001). |
| C-002 | L3 | Variant 3 | 72% | 3 of 3: a scoped, recorded, one-issue acceptance (`merged-requirements.md:572`) is bounded; declining blocks all learning; Variant 2 doubles the exposure. |
| C-003 | L3 | Variant 3, amended | 70% | 3 of 3: FU-1 runs after WA-01 to WA-03 once OB-H1 item 5, the live-test grant, Orca availability and Q20 hold. |
| C-004 | L2 | Variant 3 (tied with Variant 1) | 80% | 3 of 3: one small reversible PR makes the code match the recorded decision (ADJ line 271). |
| C-005 | L2 | Variant 3 | 75% | 3 of 3: only Variant 3 reaches WA-05, SW-10, SW-13 and WA-07 through a gate set that can be met. |
| C-006 | L2 | Variant 3 (tied with Variant 1) | 80% | 3 of 3: change the code, not the owner's recorded decision. |
| X-001 | L2 | Variant 2 | 72% | 3 of 3, and the Variant 3 advocate conceded: Variant 2 says plainly that FU-1 waits on gates; Variant 3's "FU-1 can run" contradicts its own risk line and `refs/claim.md:131`. |
| X-002 | L3 | Variant 3 (tied with Variant 1) | 78% | 3 of 3: claim-only is the owner's recorded intent (D2); "a ready plan" has no source. |
| X-003 | L3 | Variant 3 | 68% | 3 of 3: one bounded test session with scoped, recorded consent. |
| A-001 | L2 | none (shared gap) | 85% | 3 of 3 REJECT: every variant omits the live-test grant. |
| A-002 | L3 | Variant 1 | 70% | 3 of 3: only Variant 1 does not rely on the assumption; the others must tell the owner the acceptance covers more than the listed writes. |
| A-003 | L2 | none (shared gap) | 70% | 2 of 3 (V1 and V3 advocates); the V2 advocate gave Variant 2 a marginal edge. Orca availability and Q20 bind every option. |

Points won: Variant 3: 8 (C-001, C-002, C-003, C-004, C-005, C-006, X-002, X-003; four of them tied with Variant 1); Variant 2: 1 (X-001); Variant 1: 1 (A-002) plus 4 ties; shared gap or no winner: 3.

## Convergence Assessment
- Points resolved: 13 of 13
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-004, C-005, C-006, X-001, A-001, A-003), L3 (C-001, C-002, C-003, X-002, X-003, A-002): all covered.
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick).
- Status: CONVERGED
- Unresolved points: none
- Neutral recommendation by the advocates: Variant 3, 3 of 3 (70, 75, 70; mean 72), each with the same amendments: state every FU-1 precondition (OB-H1 item 5, the live-test grant, Orca availability, Q20) and word the acceptance to cover whatever the one session does on the test issue.
