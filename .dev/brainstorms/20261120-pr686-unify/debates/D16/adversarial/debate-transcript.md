# Adversarial Debate Transcript (D16)

## Metadata
- Depth: standard (Round 1, Round 2, Round 2.5; no Round 3)
- Rounds completed: 2 plus the invariant probe (2.5)
- Advocates: 2 (Variant 1 OURS, Variant 2 CLAY), each a separate sub-agent; Round 1 in parallel, Round 2 in sequence (OURS first, CLAY second, so CLAY saw OURS' rebuttal); one independent fault-finder sub-agent for Round 2.5
- Convergence threshold: 0.80 (default)
- Focus areas: all
- The full advocate statements are kept unedited on disk next to this file and are the authoritative transcript; this file records the structure, the per-point outcomes and the residual disputes:
  - Round 1, OURS: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/round1-advocate-1-ours.md`
  - Round 1, CLAY: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/round1-advocate-2-clay.md`
  - Round 2, OURS: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/round2-advocate-1-ours.md`
  - Round 2, CLAY: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/round2-advocate-2-clay.md`
  - Round 2.5: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/invariant-probe.md`
- Orchestrator re-checks during the debate (read-only): issue 290 owner comments of 2026-10-29 (quotes confirmed); `IB-JonathanB` has no PR authored or reviewed; PR 682 matches the OURS path list on 4 of 36 files; base branches of the last 100 merged PRs (master 71, integration 23, other 6; integration `protected=false`); PRs 686 and 690 are not Draft; PR 662 (owner revert of release 6.1.0) opened 2026-11-19T01:17:35Z, merged 01:20:30Z by `ironbelly`; organisation plan `free`.

## Round 1: Advocate Statements

Both advocates opened with a steelman of the other side and converged quickly, so Round 1 already narrowed the gap.

- OURS (narrowed): take Clay's words first; add one admin-only ruleset with code-owner review on a short path list; drop the in-flight table, the 24 hour timer, `/sc:overlap` and the `/sc:issue` stop; conceded that the section 11 path list matches 27 of the last 60 merged PRs (too wide) and that CONTRIBUTING.md:77-79 is a rot-budget disclaimer, not team governance. Argued that a sentence in a file already failed once (PR 681's body said "the owner reviews and merges"; its author merged it).
- CLAY (agreement first, ruleset in reserve): roles by login, silence rule with a 3 working day fallback, a reversal line, publish within a day, finish issue 290; hold the admin setting behind a tripwire ("one self-merged design or deletion after the agreement lands"); conceded that master is unprotected, the shared-login argument is overstated and that the owner must publish the decisions open work depends on. Argued the OURS path list is brittle (PR 682 matched 4 of 36 files; the 1,597 deleted lines of `cli/issue_pipeline/` are off it) and that the rule text must reach sessions (CLAUDE.md).
- A-001 to A-004: both QUALIFY, except A-002 where OURS ACCEPTs.

## Round 2: Rebuttals

Residual disputes after Round 1, each settled or narrowed:

| Dispute | OURS Round 2 | CLAY Round 2 |
|---|---|---|
| R-1 ruleset now or tripwire | Now, narrow, 14 day review, one-click off; PR 686 is exposed now and a tripwire fires after harm | Accepts now (moved by the data: owner median 4.4 h on PRs merged; rulesets free; nobody watches merges); asks for admin bypass, a zero-approval test first, and a direct hold on 686 and 690 |
| R-2 trigger | Both (two paths plus temporary `issue_watch/` plus a computed deletion check pasted into the PR body) | Computed check fires on 11 of 100 PRs, mostly an author's own work, no revert exemption; keep the sentence, make the commands an optional helper; the two paths caught all six large deletions in the window (withdrew "brittle") |
| R-3 decision log | One file `docs/decisions.md`, seeded once, entries recorded by the agent from the owner's chat words | Accepts the file (Augment search sees files, not comments) |
| R-4 silence fallback | 3 working days is an ask-again timer, never permission; owner names a deputy or "nobody" in chat; do not rely on `IB-JonathanB`; any one non-author owner suffices | Accepts; adds: do not name `IB-JonathanB` until they agree; owner names the channel they read |
| R-5 where the words go | Root `CLAUDE.md` carries the text; pointers in HOW-WE-WORK.md and CONTRIBUTING.md; template as a reminder (14 of 100 PRs carry it) | Accepts; costs the HOW-WE-WORK.md pointer at about 15 minutes (byte copy and tests) |

New measurements by OURS (all 11 spot-checked by CLAY and held): template reaches 14 of 100 PRs and none of 681, 682, 686; 89 of 100 self-merged; Clay's self-merge median 0.76 h, owner-merged Clay PRs median 4.4 h; 31 gated PRs in 11 days; PR 686 has 59 files, 0 on the two paths. New measurement by CLAY: the computed deletion check flags 11 of 100 PRs, 9 of them Clay's; PR 662 (owner revert) would have been flagged.

Residual disagreements after Round 2: (a) admin bypass (CLAY yes, for pull requests only; OURS no bypass); (b) required paste of the deletion check (OURS yes; CLAY optional helper); (c) `IB-JonathanB` on CODEOWNERS (OURS yes, CLAY no); (d) direct hold on 686 and 690 (CLAY adds; OURS silent but its R1 item (b) accepts a hold). The adjudication is in `refactor-plan.md`.

## Round 2.5: Invariant Probe
One independent fault-finder (not an advocate) probed the emerging consensus in six categories. 27 findings: 9 ADDRESSED, 18 UNADDRESSED (4 HIGH, 10 MEDIUM, 4 LOW). Full table: `invariant-probe.md`. The four HIGH items:

- INV-001: the ruleset on `master` does not cover `integration` (23 of the last 100 merged PRs went there, all self-merged by Clay; `integration` is `protected=false`).
- INV-007: whether "require review from code owners" at 0 required approvals blocks an author who is himself a listed code owner is unverified, and one community report says it does not. Both incident PRs were Clay's, and Clay was a listed owner in the consensus.
- INV-026: "ranks 1 to 7 alone would have prevented 681 and 682" holds only if one admin setting works (INV-007); the text items add no prevention of their own.
- INV-027: the throwaway-PR test and the 14 day review would not detect a gate that never blocks, unless the test is run as Clay's account on an owned path against `master`, with no approval and no `--admin`.

## Scoring Matrix

Winner after Round 2. Confidence follows the protocol rules (never 100 percent unless explicitly conceded by all).

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | Neutral | 90% | Layout only; both advocates say no effect |
| S-002 | L1 | Neutral | 90% | Fact lists differ in purpose; one misread in CLAY (CONTRIBUTING.md:77-79), conceded |
| C-001 | L2 | Both (hybrid) | 80% | Unanswered question and undefined "owner" are inputs; unprotected master is the failure (R1 both) |
| C-002 | L3 | OURS (narrowed, now) | 90% | CLAY moved to "now" in Round 2 (rulesets free, owner replies in hours, nobody watches merges); keeps three conditions |
| C-003 | L3 | Hybrid | 80% | Two paths caught all six large deletions in the window (CLAY withdrew "brittle"); 686 and 690 sit on no path, so a direct hold and the written 30 day sentence |
| C-004 | L2 | Agreed | 90% | Roles by login; carrier is root CLAUDE.md |
| C-005 | L3 | Hybrid | 85% | CLAY's sentence plus a fallback; OURS's required reviewer makes it bite; 3 working days is an ask-again timer |
| C-006 | L2 | CLAY | 85% | OURS dropped the command and the stop; one template line remains (reach 0 of the last 79 PRs per INV-014, so only a reminder) |
| C-007 | L2 | OURS | 85% | One file, not a folder; CLAY conceded (search sees files, not comments) |
| C-008 | L2 | CLAY | 95% | Draft PR or issue comment within a day; table dropped by both |
| C-009 | L3 | CLAY | 95% | GitHub cannot enforce a delay; the review does the work |
| C-010 | L2 | CLAY | 95% | Days of work; contradicts issue 290's "only file issues" |
| C-011 | L2 | Agreed | 85% | Finish issue 290 with a date; its rule text feeds the CLAUDE.md section |
| C-012 | L2 | Hybrid | 75% | Words about 1 to 1.5 hours; admin 15 to 30 minutes; queue is real (INV-013 recount: 17 of 23 gated master PRs are the owner's) |
| C-013 | L3 | OURS (limit stated) | 75% | The gate gives "a second login", not "the owner read it" (INV-008) |
| X-001 | L2 | Both | 80% | Same data; trust works daily and nothing stopped this event |
| X-002 | L2 | CLAY | 85% | Searching cannot reach unpublished work; publishing and a file can |
| X-003 | L3 | OURS | 85% | A convention with no second person did not hold (PR 681 body; PR 683 self-merged 75 minutes later, INV-019) |
| A-001 | L3 | Agreed (qualified) | 80% | Owner names a deputy or "nobody" and the channel in chat; ask-again timer |
| A-002 | L2 | Agreed | 90% | Rule text in root CLAUDE.md; template reach 14 of 100, 0 of the last 79 |
| A-003 | L3 | Agreed (qualified) | 90% | Prerequisite: owner says it in chat, Clay accepts in the PR, before the ruleset is announced |
| A-004 | L2 | Agreed (qualified) | 85% | Path gate plus decisions file plus draft-PR habit; a duplicate feature on unlisted paths is not covered |

## Convergence Assessment

- Points resolved: 22 of 22 (every diff point has an agreed or adjudicated outcome)
- Alignment: 100 percent; threshold 80 percent
- Taxonomy gate: L1, L2 and L3 all covered (no forced round needed)
- Invariant gate: BLOCKED. 4 HIGH UNADDRESSED invariants (INV-001, INV-007, INV-026, INV-027). Depth standard has no Round 3, so they are not debated further; the protocol says to resolve them in a later round or accept them as risk. This run resolves each as a binding condition of the merged recommendation (see `refactor-plan.md`, section "Invariant conditions") and lists them as `unaddressed_invariants` in the return contract. Status: BLOCKED_BY_INVARIANTS, force-selected by score, flagged for the owner.
- Residual disputes (admin bypass, required paste, `IB-JonathanB` on CODEOWNERS, direct hold) are adjudicated by the verdict under the weighting rule, in `refactor-plan.md`.
