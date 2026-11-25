# Adversarial Debate Transcript (D01 trigger and approval gate)

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A then B) plus Round 2.5 invariant probe; no Round 3 (depth standard)
- Convergence achieved: 89% of debated points (17 of 19; S-001 and S-002 were not put to the advocates), but status BLOCKED_BY_INVARIANTS until INV-001 and INV-002 are made requirements (see Convergence Assessment)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Advocate A = OURS, Advocate B = CLAY)
- Verification note: after Round 1 the orchestrator verified `orchestrator.md:317`, `:488`, `:551`, `:1135`, `:1234` and corrected diff point C-006 (B is not silent about edits; AD-A3 / ruling 23 decides they are fine).

## Round 1: Advocate Statements

### Variant A Advocate (OURS)

**Position summary.** Assignment is necessary but not sufficient. A deliberate approval by an approved login, bound to the content the person saw, stays the start signal. Assignment already half-triggers discovery; the dispute is whether it may be the whole trigger. Spot-checked: REQ R19 (line 45), REQ lines 101-104, `SKILL.md:87` (`/sc:issue --claim` runs `--add-assignee @me`), `hold.py:131` ("does not say whether the plan is good").

**Steelman of B.** The system's point is that nobody starts work by hand; each extra human act is a failure mode. Assignment is a decision by someone trusted; only the same three accounts hold triage or write, so the approval widens nothing and removing it narrows nothing. L-1: an agent on the same login can apply the approval, so it is a speed bump. B adds `plan_check` (a real readiness check) and `hold:backlog` (a cheap opt-out), proposed in writing (#450, "What do you think?"), and the owner's trend runs toward fewer gates (R35, R36). R1 at D:73 is a clean rule.

**Strengths claimed.** (1) Assignment is also an effect of claiming (`SKILL.md:87`, `refs/claim.md:48`); whether a manual claim would be launched twice is UNVERIFIED. (2) The owner decided this more than once: R19 line 45, lines 103-104; R36 (line 62) withdraws only R31 and says `unchanged_since` "stays"; marked built. (3) Edit-after-approval binding exists only in A; PR 686 removes `unchanged_since`; B's live re-read compares against nothing a person saw. (4) Larger consequence profile: same assignment ends in a worker that pushes and an orchestrator that merges (D:117, D:118); `master` unprotected (read by A, not re-checked by the advocate). (5) Replacement is a presence check (`hold.py:122-143`). (6) The approval flow is built, tested and gated (REQ line 70: 10677 passed; closed ship gate R33).

**Weaknesses identified in B.** (1) Gate removal on a bigger blast radius; bounded automation (day cap, 3 in flight, merge conditions) does not bind content to a person's reading; none of it ran live. (2) Central premise marked UNVERIFIED by B's own source (D:74 R2; OQ6 D:134 two gaps). (3) Contradicts the owner's recorded R19; B's design was approved by its author calling themselves the owner. (4) The "burden" argument is partly self-inflicted: the one-hour wait and plan request add delay and a new automated write path against NG-2 (topic D09). (5) L-1 cuts both ways: a same-login agent that can pass any login signal can also assign; the approval at least adds a second timestamped event that `approval_of` rejects when the actor is a bot.

**Concessions.** L-1 is real (gate proves a deliberate act by an approved login, not a human body). Trigger label plus approval is one signal more than may be needed. `plan_check` and `hold:backlog` are genuine, separable additions and should be adopted. R35 and R36 show the owner loosening. Nothing ran live; the R35 field-event path rests on assumed-shape fixtures (UNVERIFIED live).

**Shared assumptions.** A-001 QUALIFY (the trigger rule cannot be separated from what the worker may do; under claim-only and a closed ship gate, dropping the gate is cheap; with push and merge it is costly; decide D05 and D06 first or make the rule conditional). A-002 QUALIFY (R35 "built" but field timeline events unverified against live GitHub). A-003 REJECT (the window is not reliably short; `unchanged_since` exists because issues are edited; B's flow adds a one-hour quiet period and a plan-request round trip). A-004 ACCEPT.

**Per-point view (superior side, confidence).** C-001 A 78; C-002 A 55; C-003 A 65; C-004 B 60; C-005 B 70; C-006 A 85; C-007 A 72; C-008 A 85; C-009 B 55; C-010 B 55; C-011 tie 50; X-001 A 85; X-002 A 60.

### Variant B Advocate (CLAY)

**Position summary.** Assignment alone should start the work; safety comes from a script (`plan_check`), a person's veto (`hold:backlog`) and bounded automation. B is strongest on the manual burden, the new readiness and veto signals, and the weakness of a same-login approval. A is stronger on edit-after-approval binding (C-006), the consequence profile (C-007) and the owner's records. Confidence that B's rule is right as written is below 50%; a hybrid is better: take `plan_check` and `hold:backlog`, keep an A-style start signal until the guard questions are settled.

**Steelman of A.** Assignment is an ownership act, not "go" (`SKILL.md:87`). Under B the same assignment ends in a worker that pushes and an orchestrator that merges, with no human act between; `master` unprotected; the design admits workers run with no launch-level guard (K12, `orchestrator.md:1234`, verified). `unchanged_since` is the only code tying what a person said yes to with what the worker reads. The owner confirmed "approval label plus issue state stay the gate" (REQ R19) and R36 withdrew only R31. A concedes `plan_check` and `hold:backlog`, so the disagreement is narrow.

**Strengths claimed.** (1) A readiness signal exists where none did (`hold.py:122-143`); `table_row` makes `hold:backlog` win over everything (`hold.py:153`). (2) Live re-read at wake: "still open, still assigned to the user, and the check still passes" (`orchestrator.md:317`, verified); it re-runs `plan_check`, it does not compare content. (3) L-1 is real (`E-pr682.md:75`; UNVERIFIED by the advocate). (4) The burden is the stated target (REQ line 9; remaining manual gate is approval and state, REQ lines 102-104). (5) The trust set is identical. (6) Merge safety is specified: `--match-head-commit`, never `--auto`, `--admin` or `--delete-branch` (ADD5, `orchestrator.md:139`), tests T7 and T8.

**Weaknesses identified in A.** (1) Its tested-code argument is partly circular: 10677 tests show the code works as built, not that a human gate is right; the gate currently guards only Pipeline None (R33). (2) Approval is bypassable by the same login (L-1). (3) Five conditions where two would do; trigger label, approval field, Status allow-list are manual setup against "zero setup"; A admits one signal too many. (4) More failure reasons for correct issues (`events_incomplete`, `project_mismatch`); partly verified.

**Concessions.** C-006 is B's real hole: nothing in PR 686 compares the issue now with what a person looked at (advocate's "silent" label was later corrected by the orchestrator, see metadata). B's own flow lets an agent write the plan (T7, `orchestrator.md:1135`, verified), so plan creation, building and merge can all be agent work, weakening "the plan is reviewed at creation". K12 and unprotected `master` are real; B's safety rests on allow-list, caps and merge conditions, not a person. B relies on a premise its author marks UNVERIFIED. B does not address a manual claim versus a watcher start (UNVERIFIED). X-001: REQ line 62 shows R36 withdraws only R31; B's use of R36 as a trend is a stretch.

**Shared assumptions.** A-001 QUALIFY (same as A: bounded consequences are needed; with a claim-only or guarded worker the gate is cheap to drop). A-002 QUALIFY (B does not use the `Approved` field; it binds A, not B; fixtures UNVERIFIED live are a cost for A and a point for B's smaller surface). A-003 REJECT (the hold waits up to an hour for a plan request, and the plan request itself edits the body; bounding the window needs content binding, which only A has). A-004 ACCEPT.

**Per-point view.** C-001 A 60; C-002 A 55; C-003 A 60; C-004 B 60; C-005 B 70; C-006 A 80; C-007 A 65; C-008 A 65; C-009 tie 50; C-010 B 65; C-011 A 55; X-001 A 80; X-002 A 60.

## Round 2: Rebuttals

Note: a first Round 2 request to advocate A (agent a1d1dbe17ff356b81) never returned; the orchestrator re-ran Round 2 with fresh agents (A: aef0ee7b1a8aea099, B: ac6caa064cd8da772), A first, B second with A's rebuttal supplied.

### Variant A Advocate (OURS), rebuttal

- **Tests are circular: conceded.** 10677 passing tests show the code does what was built, not that a human gate is right. The real support is the owner's records (R19 line 45, R35, R36 line 62).
- **Five conditions where two would do: half right.** The trigger label is redundant (already conceded). Status allow-list and `hold:backlog` overlap, because Backlog is already outside the allow-list (R22). Only three do separate work: assignment plus approval (start act), `unchanged_since` (content binding), `plan_check` (readiness skip). The two vetoes are cheap read-only skips.
- **L-1 speed bump:** L-1 cuts against every login-based signal including assignment. The approval adds a separate timestamped act and `approval_of` rejects a bot actor (`predicates.py:216-223`). `/sc:issue --claim` assigns routinely (`SKILL.md:87`); nothing suggests an agent applies the approval routinely. A speed bump still stops accidents.
- **C-006 after `orchestrator.md:488`:** B is not silent; AD-A3 / ruling 23 is deliberate. Accepting post-assignment edits is defensible where the worker is claim-only or guarded. `plan_check` tests that three headings are filled (`hold.py:131`: "does not say whether the plan is good"); a rewritten body with three filled headings still passes. `unchanged_since` ties a person's yes to what they read and also catches renames and foreign comments. Its value matters only if the worker can push and merge (D:117-118). Conceded: any edit voids the approval, so a typo needs re-approval, which is B's burden. C-006 lowered from 85 to 65.
- **Minimum start signal kept:** assignment to the own login on an open issue, plus the approver's `Approved=Yes`, unedited since (`unchanged_since`) and after store init; skips for `plan_check` not ok, `hold:backlog`, Status outside the allow-list. The separate trigger label should not survive as a manual act (assignment fills its discovery role, `github.py:180-198`), but R35 line 61 says it stays, so that is the owner's call. Whether the timeline carries an assignment time the watcher can compare is UNVERIFIED.
- **Accept from B:** `plan_check` as a skip reason before the approval; `hold:backlog` as a read-only veto. **Refuse:** assignment alone as the start. Reopen dropping the approval once D05 and D06 deliver a guard and claim-only workers.
- **Revised:** A-001 QUALIFY, A-002 QUALIFY, A-003 REJECT, A-004 ACCEPT. Confidences: C-001 A72, C-002 A50, C-003 A60, C-004 B65, C-005 B75, C-006 A65, C-007 A70, C-008 A80, C-009 tie, C-010 B60, C-011 tie, X-001 A85, X-002 A55.

### Variant B Advocate (CLAY), rebuttal

- **Assignment is an effect of claiming: conceded** (`SKILL.md` claim wave 3 runs `--add-assignee @me`). A manual claim plus a watcher start is a real double-start hazard; whether the watcher skips an issue with a claim record or worktree is UNVERIFIED for PR 686. A skip check is mandatory under B's rule, so assignment alone is a weaker "go" than B wrote.
- **`master` unprotected, workers unguarded (`orchestrator.md:117, 118, 1234`): conceded.** B's safety rests on the allow-list, day cap, three in flight and merge conditions, none of which ties a person's reading to the content. REQ R33 says only Pipeline None launches today, so the present exposure is a claim, not a push.
- **Owner records: conceded and decisive.** R19 (line 45), R36 (line 62, withdraws only R31 and keeps the edit rule) and "Gates that stay manual" keep the approval. B's "trend" is an inference; the #450 proposal has no recorded answer. B cannot adopt assignment alone unless the owner reverses R19 in chat.
- **Best case for assignment-only:** if D05 and D06 deliver an effective launch guard and claim-only workers, a wrong start costs a comment and a worktree and unassigning undoes it. Assignment alone would be safe only if: (1) the launch guard refuses to start when not effective, with tests; (2) workers cannot push or merge (ship gate closed or equal control); (3) the watcher skips any issue that already has a claim record or worktree; (4) the owner records the R19 reversal in chat. The hybrid (plan_check, hold:backlog, `Approved` field as the start signal) is acceptable for now.
- **Dropping the trigger label:** a benefit, not a clear one: it is clear only together with the claim-record skip check; R35 says it stays; owner's call.
- **Lighter approval:** the `Approved` field with no void-on-edit is acceptable only while workers are claim-only (it then is a presence check by a login, a speed bump). Better: keep void-on-edit but ignore edits by the approver's own login (whether `unchanged_since` already exempts the approver is UNVERIFIED).
- **Revised:** A-001 QUALIFY (stronger), A-002 QUALIFY, A-003 REJECT, A-004 ACCEPT. Confidences: C-001 A75, C-002 A50, C-003 A60, C-004 B55, C-005 B75, C-006 A65, C-007 A75, C-008 A85, C-009 tie, C-010 B60, C-011 tie, X-001 A85, X-002 A55.

## Round 2.5: Invariant Probe (fault-finder, agent a8f916068f69d205f)

Full findings are in `invariant-probe.md`. Orchestrator verification: INV-002 confirmed (master `cycle.py:858,946-947` uses `marker_in_window`; PR 686 only keeps the constant `CLAIM_MARKER`, `pr-a/.../predicates.py:18`; `refs/claim.md:30,92` posts the marker); INV-001 confirmed (master `_revalidate` at `cycle.py:979`, called at `:1058`; PR 686's wave-1 re-check covers `hold:backlog` and `plan_check` only, `orchestrator.md:488`).

## Scoring Matrix

Winner per point from the Round 2 positions of both advocates (both name the same side in every debated case). Confidence is the mean of the two Round 2 figures (no concession boost added beyond what the advocates stated).

| Diff point | Winner | Confidence | Evidence summary |
|---|---|---|---|
| S-001 | none (not debated; form only) | n/a | Structure of the two papers differs only because they describe different code |
| S-002 | Variant A | derived from C-001 | Five-condition rule follows the C-001 outcome; not put to the advocates |
| C-001 | A (OURS) | 74% | Assignment is an effect of `--claim` (`SKILL.md:87`); owner records R19, R35, R36; both advocates agree |
| C-002 | A, weak | 50% | Same trust set; the gate adds an act, not narrower trust; both advocates at 50 |
| C-003 | A | 60% | Premise UNVERIFIED in 655 and D:134 OQ6 |
| C-004 | B (CLAY) | 60% | L-1 weakens any login-based signal; A concedes; a speed bump still stops accidents |
| C-005 | B | 75% | `plan_check` is a new readiness signal; both want it as a skip reason |
| C-006 | A, narrow | 65% | B is deliberate (AD-A3), but the approval ties yes to content; matters only with push and merge |
| C-007 | A | 72% | Same assignment ends in push and merge on unprotected `master` with unguarded workers (D:117, 118, K12) |
| C-008 | A | 82% | R19 line 45, R36 line 62, "Gates that stay manual"; B concedes it is decisive |
| C-009 | tie | 50% | Clay's #450 comment was addressed to the owner; no recorded answer |
| C-010 | B | 60% | PR 686 removes about 30 functions and their failure reasons; A concedes the trigger label is redundant |
| C-011 | tie | 50% | Neither has run live |
| X-001 | A | 85% | REQ line 62: R36 withdraws only R31 |
| X-002 | A | 55% | Same trust set protects against accident and stale content, not outsiders |
| A-001 | agreed QUALIFY | n/a | Trigger rule depends on D05 and D06 |
| A-002 | agreed QUALIFY | n/a | Field events UNVERIFIED live |
| A-003 | agreed REJECT | n/a | Window not short (plan request edits the body); B's AD-A3 does not rely on it |
| A-004 | agreed ACCEPT | n/a | `is_intended_owner` |

## Convergence Assessment

- Points resolved: 17 of 19 debated (C 11, X 2, A 4); S-001 and S-002 not put to the advocates (form only, and derived from C-001)
- Alignment: 89% (17/19); every debated point had the same winner or an agreed tie from both advocates
- Threshold: 80%
- Taxonomy coverage gate: L1 (C-009, C-011), L2 (C-001, C-002, C-003, C-005, C-008, C-010, X-001), L3 (C-004, C-006, C-007, X-002, A-001 to A-004) all covered
- Invariant probe gate: BLOCKED_BY_INVARIANTS. INV-001 and INV-002 are HIGH and UNADDRESSED in the advocates' consensus. Depth standard has no Round 3. Resolution (recorded, not hidden): both are made mandatory requirements MR-1 and MR-2 of the merged recommendation (re-check approval, `unchanged_since` and Status allow-list at the moment of start; keep the claim-marker guard `marker_in_window`). They are therefore addressed by the merged output, not by an extra debate round. Return contract status is `partial` and lists both ids.
- MEDIUM UNADDRESSED (warnings, do not block): INV-003, INV-004, INV-005, INV-006, INV-007, INV-009
- Unresolved points: none contested; open for the owner: R19 reversal (owner chat decision), trigger label (R35 says it stays)
