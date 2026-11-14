# Round 1 advocate statement: Variant 1 (accept now with caveats, fix in a tracked follow-up with a hard trigger)

Persona: analyzer (evidence quality and logical consistency). Mode A, depth quick, Round 1.
Sources read: `../question.md`, the three variants, `diff-analysis.md`; checked against `merged-requirements.md` rows SW-01 (line 190), SW-02 (191), SW-05 (194), XC-04 (452), Q1 (528), TB-GIT (630), TB-PERM (631), lines 169, 183, 562, 571; `adversarial/adversarial/invariant-probe.md` rows INV-004 (line 12), INV-011 (line 19), INV-018 (line 26); `adversarial/adversarial/round2-rebuttal-V1.md:17`.

## Position summary

Variant 1 is the only answer that both makes every published "read-only" claim honest at merge time and commits to closing the hole, while keeping a security fix that touches an owner-signed allow-list out of a 1003-file PR. Its price is two passes over the same 16-plus texts and a hole that sits on master until a trigger fires, so it is the best answer only if the owner values merging #539 now over a single clean pass.

## Steelman

### Variant 2 (fix before merge, F1 or F2)

Strongest version: the sweep is sold as read-only, and the measurement of 2026-11-13 shows that claim is false through six channels (`question.md` line 30). Fixing before merge makes the claim true as written, so none of the 16-plus statements needs a caveat (INV-011, `invariant-probe.md:19`); the decision stays reversible (SW-01 "undo" column: "a fix choice, yes", `merged-requirements.md:190`); master never carries the hole; and the regression test is already fully specified, including `.process` (SW-02 (1), `merged-requirements.md:191`), which closes the INV-004 gap. It also matches the spec's own recommended answer (F1 or F2, about 70 percent, `merged-requirements.md:528`) and the target state (`merged-requirements.md:183`). It is the only variant whose step 1 meets SW-01 (3) (allow-list edit authorised).

Critique: (1) Its step 1 states no premise, but SW-01 (2) requires the ruling to "state which premise it relies on" (`merged-requirements.md:190`); diff C-004 records this gap. (2) Its claimed unique unlock, that XC-04 "can run on master code as soon as the sweep is runnable", is not unique: TB-GIT, which gates every sweep run including XC-04, is "satisfied only when SW-02's landed test covers every channel the ruling puts in scope, or Q1 = F3 is recorded with its caveats" (`merged-requirements.md:630`), and the debate that produced the rule wrote "JOIN runs only after SW-02 has landed F1/F2 in the code being run, or Q1 = F3 is recorded" (`round2-rebuttal-V1.md:17`). XC-04 (4)'s "never the unfixed sweep" wording (`merged-requirements.md:452`) is ambiguous against that, so V2's advantage holds only under the strict reading. (3) It puts an allow-list change, three pinned golden tests (INV-009) and a path-scope separation (INV-039) inside a PR of 1003 files (`qa-merged-spec.md:85`), which is the hardest place to review a security change, and it lengthens every lane behind SW-05 (`merged-requirements.md:194`, "blocks" column).

### Variant 3 (accept with caveats, no code change)

Strongest version: on this host every launched session already runs with permission checks off (TB-PERM, `merged-requirements.md:631`; E-11), a clone cannot ship config and `.gitattributes` alone ran nothing (`question.md` line 32), and severity was judged Medium in practice (line 34). So the marginal privilege the sweep grants is near zero, and spending an allow-list change, three pinned tests and a path-scope separation on it is cost without matching benefit. F3 is a first-class option in the question (`question.md` line 7) and TB-GIT accepts it (`merged-requirements.md:630`). V3 also adds the best ledger hygiene of all three: the acceptance carries its own void conditions (U-004).

Critique: (1) It is internally inconsistent (X-003): its premise says "the sweep grants no privilege a session does not already have", yet its own risk section says anything that can write host git config "can make every sweep run a program in every listed worktree, at least 18 of 29 of which share one config". The fan-out across worktrees from one call is exactly what a single session does not otherwise do. (2) It leaves the hole permanently, while the acceptance is "reversible only before merge" (SW-01 undo column), so after merge the only way back is a new fix PR, which V3 does not schedule. (3) Its own unresolved list names setup changes (a second host, a shared Coder workspace, the watcher starting sessions from issue text) that would void the premise, but nothing mechanical detects them. (4) Its XC-04 claim ("blocked unless ... an owner exception the spec does not provide") misreads the spec: TB-GIT is satisfied by a recorded F3 (`merged-requirements.md:630`).

## Strengths claimed

1. **Honest claims at merge, true claims later.** The caveat pass (at least 16 locations, mirror byte-equal; INV-011 `invariant-probe.md:19`; SW-02 F3 branch `merged-requirements.md:191`) means no false "read-only" text ever ships, and the follow-up removes the caveats once they are true again (V1 "What happens next" step 5). V3 ships honest but permanently weaker claims; V2 ships true claims but only after the fix lands.
2. **A named trigger instead of an open-ended acceptance (U-001).** The follow-up must land before XC-04, before any unattended or scheduled sweep, and before a second user or host. These are the exact conditions under which the single-owner premise stops holding (V3's own "What stays unresolved" list; A-004). V3 records void conditions but no deadline for a fix.
3. **Fits the spec's own follow-up structure.** The target state requires that "#534 holds one table of every Phase 1 follow-up with item, owner and trigger" (`merged-requirements.md:183`; scope line 169). V1 step 3 uses that table as designed.
4. **Separates the security fix from a 1003-file PR (U-002).** #539 changes 1003 files (`qa-merged-spec.md:85`, confirmed by `gh pr view`). A fix that edits the owner-signed `ALLOWED_GIT` list, three pinned tests (INV-009) and the shared path list (INV-039) gets a focused review in a small PR, rather than inside the largest diff in the program.
5. **States its premise as SW-01 (2) requires.** V1 step 1 names the premise (single owner, single host, permission-free sessions, E-11) and the full channel list, meeting SW-01 (2) and (4) (`merged-requirements.md:190`). V2 does not state a premise.
6. **Unblocks the non-XC-04 lanes now.** SW-05 blocks SW-07, SW-08, SW-10 to SW-14, OB-07, XC-06, XC-07, V2-02 and SWEEP-RUNNABLE (`merged-requirements.md:194`). Under V1 these start after the caveat pass, not after an allow-list redesign.
7. **Honest about its own limits.** V1 already concedes that XC-04 gains nothing and that a trigger "is a promise in a table, not a mechanical gate" (variant-1 "What it costs or risks").

## Weaknesses identified in other variants

1. **V2 omits the premise SW-01 (2) requires** (diff C-004; `merged-requirements.md:190`). A ruling posted from V2's step 1 as written would fail SW-01's acceptance criteria.
2. **V2 overstates its XC-04 advantage.** Under TB-GIT (`merged-requirements.md:630`) and the debate that wrote the rule (`round2-rebuttal-V1.md:17`), a recorded F3 also satisfies the sweep-run gate; V2's advantage is real only under the strict reading of XC-04 (4).
3. **V2 holds every lane behind SW-05** for a change the spec itself calls "not a one-liner" (`question.md` line 35), and gives no estimate of how long.
4. **V3 contradicts itself on privilege** (X-003), as shown in its steelman critique above.
5. **V3 makes a permanent decision on a premise it admits may change** ("What stays unresolved"), and the decision becomes irreversible at merge (SW-01 undo column).
6. **V3 misreads the XC-04 gate** (see its critique point 4).

## Concessions

1. **Double pass.** V1 edits the same 16-plus texts twice, including two lines in a mirror that must stay byte-equal (`invariant-probe.md:19`). V2 edits them zero times.
2. **The hole sits on master** between merge and the follow-up, and the acceptance becomes irreversible at merge (SW-01 undo column).
3. **The trigger is not mechanical.** V1 concedes this; a second host or a scheduled sweep could arrive without anyone reading the #534 row.
4. **XC-04 gains nothing under V1**, but by V1's own choice, not by the spec: TB-GIT would accept a recorded F3 (`merged-requirements.md:630`). V1's statement that "the spec forbids running the unfixed sweep for it" (variant-1 Costs) over-reads XC-04 (4) the same way V3 does; the self-imposed trigger is the real reason XC-04 waits. I correct V1 on this point.
5. **V1 does not authorise the allow-list edit for the follow-up.** Q1's risk choice "does not authorize arbitrary git allow-list edits" (`merged-requirements.md:571`), so the follow-up needs its own NFR-014 authorisation, which V1 leaves unstated. V2 handles this in step 1.
6. **V1 needs the #539 author (or another) twice**, deepening the A-002 dependency on unanswered Q33.

## Shared assumption responses

| Id | Response | Reason |
|---|---|---|
| A-001 (measured channels are the complete set) | QUALIFY | The list is what was measured on one git version (2.47.3; `question.md` line 30), and INV-004 shows a previous "complete" list already missed `.process` (`invariant-probe.md:12`). Treat it as the known set, not the complete set: a fix needs a test per channel plus a statement of channels left out (SW-01 (4)); an acceptance must say it accepts "the measured channels and any channel of the same class". |
| A-002 (the #539 author and ruling poster exist and act) | ACCEPT | It is a real dependency for every variant: SW-01 needs the owner or `GRANT(SW-01,thread-reply)`, SW-02/SW-05 need the #539 author (`merged-requirements.md:190-194`), and Q33 is unanswered. No variant can avoid it; V1 depends on it twice (concession 6). |
| A-003 (the sweep is the marginal exposure) | QUALIFY | In this session the Claude Code harness attached a "git status at the start of the conversation" for this worktree, so session-level git status calls in a session's own worktree do occur; whether they honour the same config keys in all 29 worktrees is UNVERIFIED. The sweep's marginal exposure is therefore the fan-out (one call reaches every Orca-listed worktree, 18 of 29 sharing one config; `question.md` line 33) plus a published "read-only" promise, not the mechanism itself. This weakens V2's urgency and V3's "no privilege" premise equally, and favours a tracked, trigger-bound answer. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (all identical) | 95 | Same five sections in the same order by design of the brief. |
| C-001 | V2 | 60 | Closing before merge avoids the hole on master and an irreversible acceptance; V1 is the better choice only if merge speed outranks that. |
| C-002 | V2 | 75 | True claims in one pass beat caveat-then-uncaveat (V1) and permanent caveats (V3). |
| C-003 | V2 | 60 | Holds under both readings of XC-04 (4); V1 and V3 overstate the block, since TB-GIT accepts a recorded F3 (`merged-requirements.md:630`). |
| C-004 | V3 | 60 | Most complete premise (adds "a clone cannot ship config"), meets SW-01 (2); V2 states none. V3's premise overreaches (X-003), so V1 is close. |
| C-005 | V2 | 75 | A fix is reversible; both acceptances become irreversible at merge (SW-01 undo column). |
| C-006 | V2 | 70 | "Names any channel it leaves out" matches SW-01 (4) word for word and guards against A-001. |
| X-001 | V3 | 55 | V3's "shortest path to merging" is literally true; V1 ties it for merge but adds a follow-up; V2's XC-04 claim depends on the strict reading. |
| X-002 | V2 | 60 | The spec's recommended answer (`merged-requirements.md:528`) and target state (line 183) favour closing it; V1's temporary acceptance is the reasonable fallback. |
| X-003 | V1 | 65 | V1 treats the exposure as real but bounded; V3 contradicts itself; V2 asserts exposure without stating a premise. |
| A-001 | V2 | 70 | The only variant that makes unlisted channels visible by rule (U-005). |
| A-002 | Tie (V2 and V3) | 55 | Both need the author once; V1 needs the author twice. |
| A-003 | V1 | 55 | If the sweep is not the only exposure, a tracked, trigger-bound fix fits the uncertainty better than an immediate fix or a permanent acceptance. |

## Overall

If I were neutral I would recommend **Variant 2**, confidence 60. It makes the claims true in one pass, keeps the decision reversible, and matches the spec's recommended answer and target state; its premise gap is a wording fix in the ruling, not a structural flaw. **Variant 1** is the right choice if the owner judges that merging #539 now outweighs a second pass over 16-plus texts, provided the ruling also authorises the follow-up's allow-list edit (concession 5) and states that XC-04 waits by owner choice, not by spec rule (concession 4). Variant 3 is the weakest because its premise contradicts its own risk section and it closes no path back after merge.
