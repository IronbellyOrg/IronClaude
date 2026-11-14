# Adversarial Debate Transcript: Q1 (INV-008)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: depth=quick; Round 3 skipped: depth=quick)
- Convergence achieved: 92.3% (12 of 13 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned as parallel sub-agents (general-purpose type). Variant 1 advocate persona analyzer, Variant 2 security, Variant 3 architect.
- Agent failure log: the first Variant 3 dispatch failed with "Concurrent subagent limit reached" (no work done); retried once per the error-handling rule and succeeded. No advocate was lost.
- Variant map: Variant 1 = proposal-A (accept now with caveats, fix later under a trigger); Variant 2 = proposal-B (fix before merge, neutralise or refuse, all channels); Variant 3 = proposal-C (accept with caveats, no code change).

## Round 1: Advocate Statements

The full statements are kept once, in their own files (not copied here):

### Variant 1 Advocate (analyzer)
File: `round1-advocate-V1.md`. Position: Variant 1 is the only answer that makes every published claim honest at merge and still commits to closing the hole, keeping an allow-list change out of a 1003-file PR. Concedes: double pass over 16-plus texts; hole on master until the trigger fires; trigger is not mechanical; the follow-up needs its own allow-list authorisation; XC-04 waits by Variant 1's own choice. Neutral recommendation: **Variant 2, 60 percent**.

### Variant 2 Advocate (security)
File: `round1-advocate-V2.md`. Position: close the hole before merge; it is the only option that keeps the claims true without caveats, lets XC-04 (the one real-id comparison) run on master with no further fix PR, and stays reversible after merge. Concedes: the ruling as drafted omits the premise SW-01 (2) requires; real cost and delay; most dependent on the unnamed #539 author; enumeration is never complete; refusing costs information. Neutral recommendation: **Variant 2, 65 percent**, on condition the ruling states its premise and is phrased by outcome.

### Variant 3 Advocate (architect)
File: `round1-advocate-V3.md`. Position: Variant 3 leaves the owner-signed structure untouched and states the fullest premise. Concedes: XC-04 is structurally blocked; the sweep runs on every coordinator wake across every listed worktree (`HOW-WE-WORK.md:406`), so the risk is exercised often; `SECURITY.md:168-170` assesses on worst-case configuration; the caveat permanently weakens the contract; reversal after merge needs a new fix PR. Neutral recommendation: **Variant 2, 62 percent**.

### Shared-assumption responses (omission check: none omitted)

| Point | V1 advocate | V2 advocate | V3 advocate |
|---|---|---|---|
| A-001 (measured channel list is complete) | QUALIFY | REJECT | QUALIFY |
| A-002 (#539 author and ruling poster available) | ACCEPT | QUALIFY | ACCEPT |
| A-003 (the sweep is the marginal exposure) | QUALIFY | QUALIFY | QUALIFY |

All three agree on A-003: the sweep is not the only `git status` on this host (the Claude Code harness reports a git status at session start; whether it honours the same config is UNVERIFIED), but it is the widest automatic one (fan-out across every listed worktree on every coordinator wake). All three agree A-001 must not be treated as complete: the ruling should be phrased by outcome, with the measured list as a minimum.

### Source conflicts raised in Round 1 (recorded, not silently resolved)

- **CONTRADICTION-1 (XC-04 gate).** `merged-requirements.md:630` (TB-GIT) says the git trust boundary is "satisfied only when SW-02's landed test covers every channel ... or Q1 = F3 is recorded with its caveats", which would let a recorded acceptance clear XC-04. `merged-requirements.md:452` (XC-04 (4)) and `:889` say the comparison runs "never the unfixed sweep". Raised by the V1 advocate. Unresolved by the sources; Variant 2's XC-04 advantage holds under either reading, Variants 1 and 3 are blocked only under the strict reading.
- **CONTRADICTION-2 (`.process` measurement).** The worker brief and `../question.md` (fact row 1) state that on 2026-11-13 `filter.<driver>.process`, `include.path`, per-worktree config and `GIT_CONFIG_*` variables were measured running a command. `merged-requirements.md:36` and `:1153` describe `.process` as "documentation only, not run". Raised by the V2 advocate. The brief is the later statement of measurement; this transcript cannot re-run it, so both versions stand and the measurement record should be cited when the ruling is posted.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | none (identical) | 90% | All three report the structure identical by design; agreed, no winner. |
| C-001 | L2 | Variant 2 | 78% | 3 of 3 advocates: closing before merge keeps master free of the hole and keeps the choice reversible (SW-01 undo column). Advocates' own confidence was moderate (60 to 70). |
| C-002 | L2 | Variant 2 | 85% | 3 of 3: true claims in one pass beat caveat-then-uncaveat and permanent caveats over a byte-equal mirror (INV-011). |
| C-003 | L3 | Variant 2 | 80% | 3 of 3: only Variant 2 lets XC-04 run on master with no further fix PR; held down from 90 by CONTRADICTION-1. |
| C-004 | L2 | Variant 3 | 85% | 3 of 3, and the Variant 2 advocate conceded: SW-01 (2) requires every ruling to state its premise; Variant 3 states the fullest one, Variant 2 none. |
| C-005 | L2 | Variant 2 | 88% | 3 of 3: "an acceptance is reversible only before merge; a fix choice, yes" (`merged-requirements.md:190`). |
| C-006 | L1 | Variant 2 | 80% | 3 of 3, Variant 3 advocate conceded: "names any channel it leaves out" matches SW-01 (4) and guards against an incomplete list. |
| X-001 | L2 | unresolved | 50% | Split: V1 advocate chose Variant 3 (fastest merge), V2 advocate chose Variant 2 (slowest lane moves soonest), V3 advocate chose Variant 1. Depends on whether the merge or XC-04 is the bottleneck. |
| X-002 | L3 | Variant 2 | 72% | 3 of 3: fan-out across 18-plus shared-config worktrees on every coordinator wake and `SECURITY.md:168-170`'s worst-case lens make the hole worth closing; Variant 1 named the defensible second. |
| X-003 | L3 | Variant 1 | 62% | 2 of 3 (V1 and V3 advocates): the sweep adds no privilege but adds a frequent automatic trigger; Variant 1's "temporary exposure worth tracking" fits both. Variant 3's premise contradicts its own risk section (V3 advocate conceded). |
| A-001 | L3 | Variant 2 | 75% | 3 of 3: only Variant 2 commits to naming excluded channels. |
| A-002 | L2 | Variant 3 | 60% | 2 of 3: Variant 3 needs the least from the unnamed #539 author (Q33 open). |
| A-003 | L3 | Variant 1 | 60% | 2 of 3: if the sweep is not the only exposure, a trigger list aimed at the real escalation points fits; all three QUALIFY the assumption. |

Points won: Variant 2: 7 (C-001, C-002, C-003, C-005, C-006, X-002, A-001); Variant 3: 2 (C-004, A-002); Variant 1: 2 (X-003, A-003); unresolved 1 (X-001); no-winner agreed 1 (S-001).

## Convergence Assessment
- Points resolved: 12 of 13 (S, C, X and A points)
- Alignment: 92.3%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001, C-006), L2 (C-001, C-002, C-004, C-005, X-001, A-002), L3 (C-003, X-002, X-003, A-001, A-003): all levels covered, no forced round.
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick).
- Status: CONVERGED
- Unresolved points: X-001
- Overall neutral recommendation by the advocates: Variant 2, 3 of 3 (60, 65, 62 percent; mean 62).
