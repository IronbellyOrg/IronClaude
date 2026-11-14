# Round 1 advocate statement: Variant 2 (proposal B, "fix before merge")

Persona: security (vulnerabilities, attack surface, trust boundaries). Mode A, depth quick, Round 1.
Paths below are relative to `.dev/brainstorms/20261113-orchestrator-tui-alignment/` unless stated. `MR` = `merged-requirements.md`; `Q` = `owner-questions/Q01/question.md`.

## Position summary

Close the hole inside PR #539 before it merges, by neutralising (F1) or refusing and reporting `unscanned` (F2), with every measured channel in scope. It is the only answer that keeps the sweep's "read-only" claims true without a caveat, lets the one real-id comparison (XC-04) run on master code with no extra fix PR, and leaves a decision that can still be reversed after merge.

## Steelman

### Variant 1 (accept now, fix in a tracked follow-up with a trigger)

Strongest version: the hole is Medium in practice on one owner, one host (Q line 34), every session already runs with permission checks off (Q line 39, ADJ E-11), and a fix touches an owner-signed one-entry allow-list, three pinned tests and a shared path list (Q lines 35-36; INV-009, INV-039). Holding a 1003-file PR (ADJ E-08, as cited by Variant 1) for that design risks a rushed security change buried in a huge diff. Variant 1 gets the merge moving, keeps the docs honest with caveats meanwhile, still commits to a fix, and names concrete triggers (before XC-04, before any unattended or scheduled sweep, before a second user or host: Variant 1 "Answer"). It also gives the fix its own focused review (U-002). That is a sound risk-management shape, and its trigger list (U-001) is the best single idea in the three proposals.

Critique: its own costs section concedes the main gain is illusory for the slowest lane: "The one real-id comparison (XC-04) must still wait for the follow-up fix ... So the slowest downstream lane gains nothing" (Variant 1, costs bullet 2), which matches `MR:844` and `MR:889` ("JOIN never runs the unfixed sweep"). It also concedes "the trigger is a promise in a table, not a mechanical gate" (costs bullet 4): from a trust-boundary view, a control that depends on someone re-reading a #534 row before a second host or an unattended sweep appears is not a control. And the acceptance stops being reversible at merge (SW-01 row, `MR:190`, undo column), so between merge and the follow-up the hole is on master, which is what other programs and the v2 knowledge layer will read. Finally it pays twice over the 16-plus texts (caveat, then un-caveat; INV-011).

### Variant 3 (accept with caveats, no code change)

Strongest version: it is the most honest about the actual threat model. A program runs only if config on this host already names it; a clone cannot ship config and `.gitattributes` alone ran nothing (Q line 32). If the only party who can write that config is the owner's own OS user, and every session is already permission-free (ADJ E-11), the sweep adds no privilege. It is the shortest path to merge (no INV-009/INV-039 work), it makes the docs honest at once, it states its premise explicitly (satisfying SW-01 AC (2), `MR:190`), and it records its own void conditions (U-004). It needs no #539 code author, so it depends least on the unanswered Q33.

Critique: its premise is contradicted by its own risk section: "Anyone or anything that can write this host's git config, an included config file, or the sweep's environment can make every sweep run a program in every listed worktree, at least 18 of 29 of which share one config" (Variant 3 costs bullet 1; diff X-003). That fan-out is exactly what the sweep adds: one invocation executes config-named programs across every worktree `worktree ps` lists (`MR:30`), with the inherited environment. It leaves XC-04 blocked with no path the spec provides (Variant 3 costs bullet 3; `MR:452` (4) "never the unfixed sweep"). And it weakens a claim that future readers rely on (Variant 3 costs bullet 4). Its void conditions include "untrusted config", but nothing detects that condition arriving, for example the watcher starting sessions from issue text (Variant 3 "Unresolved").

## Strengths claimed

1. **The claims become true, not caveated.** The spec's requirement offers exactly two outcomes before merge: no config-defined command runs, or caveats in the same PR (`MR:33`). Variant 2 is the only option that satisfies (a), so none of the at-least-16 statements (INV-011; Q line 37), two of them in a byte-equal mirror, needs editing (Variant 2 "Unlocks" bullet 1).
2. **It is the only option under which XC-04 needs no further fix PR.** XC-04 must run "on master code (never the unfixed sweep)" (`MR:452` (4)); the added graph edge says "Running the unfixed sweep exercises INV-008 on a permission-free host" (`MR:844`). Under Variant 2 the master sweep is the fixed sweep (Variant 2 "Unlocks" bullet 2). Variants 1 and 3 both concede XC-04 waits on a fix that does not yet exist.
3. **Reversibility.** SW-01's undo column reads "an acceptance is reversible only before merge; a fix choice, yes" (`MR:190`). Choosing a fix keeps every later option open; choosing acceptance closes them at merge.
4. **Channel coverage is enforced by a test, not a promise.** SW-02 (1) requires a regression test that reproduces the probe and covers every channel the ruling puts in scope, "so a fix that blanks only `.clean` fails it" (`MR:191`); TB-GIT counts as satisfied only then (`MR:36`, `MR:1153`). Variant 2 adopts this and adds "names any channel it deliberately leaves out" (U-005), which matches SW-01 AC (4) wording (`MR:190`).
5. **It handles the second-order bug the fix creates.** Variant 2 step 3 separates the git-status scope from the contract allow-list and transcript scans (INV-039; U-003), so a fix does not misreport a contract in another repository's worktree as "outside root". Neither other variant needs this, but neither would get it right if its later fix landed without it.
6. **It is the spec's own recommended default.** "Fix by F1 or F2 (about 70 percent ...); (b) yes to all" (Q line 13; `MR:528`), noting this is a PLAN INFERENCE default, not a debate verdict.
7. **It scopes the allow-list authority.** Q1's risk choice does not authorise arbitrary git allow-list edits (Q line 41; NFR-014). Variant 2 step 1 states the edit is authorised "for this purpose only", which answers SW-01 AC (3) and prevents a later re-widening of `ALLOWED_GIT` (a residual risk named at `MR:1153`).

## Weaknesses identified in other variants

1. **Variant 1: the trigger is not a gate.** Its own text: "a promise in a table, not a mechanical gate" and "a future change ... could arrive without anyone checking the #534 row" (Variant 1 costs bullet 4, "Unresolved" bullet 2). The triggers that matter most (unattended sweep, second host) are exactly the events no one is watching for.
2. **Variant 1: the speed gain does not reach the slowest lane.** It concedes XC-04 "gains nothing" (costs bullet 2). The merge-speed gain is real only for lanes that do not need a safe sweep (post-merge wording, contract-note links), and those lanes also wait on Q29/SWEEP-RUNNABLE before the sweep is usable (`MR:556`, `MR:1154`).
3. **Variant 1: double edit of mirrored texts.** Caveat now, un-caveat later across 16-plus locations including a byte-equal mirror (Variant 1 costs bullet 1; `MR:191` F3 branch). Each pass is a chance for mirror drift.
4. **Variant 3: internal contradiction on privilege.** "The sweep grants no privilege a session does not already have" (step 1) versus "can make every sweep run a program in every listed worktree" (costs bullet 1). The fan-out across up to 29 worktrees from one coordinator call is an expanded blast radius even if no privilege boundary is crossed.
5. **Variant 3: XC-04 has no route.** It names the problem and admits "the spec does not provide" an exception (costs bullet 3; `MR:452`, `MR:889`).
6. **Variant 3: permanent weakening of a contract claim.** A caveated "read-only" becomes the long-term statement other programs build on (Variant 3 costs bullet 4).

## Concessions

1. **Variant 2 does not state its premise.** SW-01 AC (2) requires the ruling to state "which premise it relies on (`SECURITY.md:L166-L170` versus INV-011's 'every session on this image runs permission-free')" (`MR:190`). Variant 2's step 1 omits it (diff C-004). Variant 3 is better on this point and Variant 2 would need that sentence added to be a complete ruling.
2. **Cost and delay are real.** An owner-signed allow-list edit, three pinned tests and the path-scope separation (INV-009, INV-039; Q lines 35-36) lengthen the #539 lane and everything behind it (Variant 2 costs bullet 1). Variant 1's point that a security change inside a 1003-file PR gets weaker review (U-002) is fair.
3. **It depends most on the unanswered author question (Q33).** A fix needs someone to write code; an acceptance needs only caveat edits.
4. **Enumeration is never complete.** "A channel nobody listed ... could still run" (Variant 2 costs bullet 2). The "names any channel it leaves out" clause makes gaps visible, not impossible.
5. **F2 costs information.** Refusing makes some worktrees show `unscanned`, which is less information for the coordinator (Variant 2 costs bullet 3).
6. **Measurement scope is narrower than any variant implies.** Q line 30 says `filter.<driver>.process` ran on 2026-11-13, but `MR:36` and `MR:1153` describe `.process` as "documentation only, not run". The two sources disagree; which is current is UNVERIFIED here. All three variants inherit this, and only one git version (2.47.3) was tested (Variant 2 "Unresolved").
7. **A fix narrows the sweep's exposure, not necessarily the host's** (see A-003 below).

## Shared assumption responses

| Id | Response | Reason |
|---|---|---|
| A-001 (measured channel list is complete) | **REJECT** | No source claims completeness; `MR:36` states the requirement by outcome ("no command that repository configuration or the inherited environment defines runs") precisely because the list is open, and the `.process` channel's measured status is itself disputed between Q line 30 and `MR:36`/`MR:1153`. Whatever the owner picks, the ruling should be phrased by outcome with the list as a minimum. This hurts acceptance options more (they would accept an unknown set by naming a known one) than a refuse-style fix, but it hurts F1 too. |
| A-002 (the #539 author and the ruling poster exist and act) | **QUALIFY** | True for every option and a real dependency (Q33 unanswered; SW-05 lists Q33 as a blocker at `MR:194`). But it weighs unequally: Variants 1 and 3 need only caveat edits from the author now, Variant 2 needs a code change. The ruling itself (SW-01) needs only the owner, so the decision can be made before Q33 is answered. |
| A-003 (the sweep is the marginal exposure) | **QUALIFY** | Partly false: the Claude Code harness ran a `git status` in this very worktree at session start (visible in this session's own context), so other processes do run `git status` with the same config. What the sweep adds is fan-out: one call runs `git status` in every worktree `worktree ps` lists, with the inherited environment (`MR:30`), from a coordinator that may run unattended. So a fix removes the sweep's multiplier and makes its claim true, but does not by itself remove the host's exposure. Whether harness `git status` uses the same flags and runs filters is UNVERIFIED. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Equal (V1 = V2 = V3) | 90 | Identical section set by design; no difference to judge. |
| C-001 | V2 | 70 | Closing before merge keeps master free of the hole and keeps the decision reversible (`MR:190`). |
| C-002 | V2 | 75 | Claims become true; no caveat pass over 16-plus texts and a byte-equal mirror. |
| C-003 | V2 | 80 | Only V2 lets XC-04 run on master without a further fix PR (`MR:452` (4), `MR:844`). |
| C-004 | V3 | 75 | V3 states the premise SW-01 AC (2) requires; V2 omits it. |
| C-005 | V2 | 75 | SW-01 undo column: a fix is reversible, an acceptance only before merge. |
| C-006 | V2 | 60 | "Names any channel it leaves out" mirrors SW-01 AC (4); V3's "nothing accepted by silence" is close behind. |
| X-001 | V2 | 55 | V3 merges fastest, but the slowest lane (XC-04) moves soonest under V2; both are also gated on Q24/Q29. |
| X-002 | V2 | 65 | Fan-out across 18+ shared-config worktrees plus permission-free sessions makes the hole worth closing; V1 is a defensible second. |
| X-003 | V2 | 65 | V3 contradicts itself; V2 treats the exposure as real, though A-003 limits how much a fix reduces host risk. |
| A-001 | V2 | 60 | Outcome-stated test plus "names what it leaves out" copes best with an open list; still incomplete. |
| A-002 | V3 | 60 | V3 needs the least from an unnamed author. |
| A-003 | V1 | 55 | If the sweep is not the only `git status`, V1's trigger list (unattended sweep, second host) targets the real escalation points. |

## Overall

If neutral, I would recommend **Variant 2** to the owner, with **65** confidence, on the condition that its ruling adds the premise statement SW-01 AC (2) requires and is phrased by outcome rather than by channel list. Variant 1 is the credible alternative if the owner judges the #539 merge itself to be the bottleneck and accepts a non-mechanical trigger; it should then borrow Variant 2's test-enforced channel scope for the follow-up. Variant 3 is defensible only if the owner rules XC-04 out entirely or grants an explicit exception the spec does not yet provide.
