# Round 1: Advocate for Variant 1 (persona: qa)

Variant 1 = proposal A: name no owner yet, hold the watcher's first live test (FU-1) until ownership and cleanup are decided together.
Paths below are relative to the repository root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/` unless stated. "MR" = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. "ADJ" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. "R2-V2" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V2.md`. "Setup" = `docs/designs/issue-watcher-setup.md`. "Design" = `docs/designs/issue-watcher.md`. Every line number cited here was read in this round.

## Position summary

From a failure-scenario view, Variants 2 and 3 both answer "who owns it" without answering the question that actually produces failures: "who ends these sessions, and how". The sources say plainly that nothing does:

- "nothing closes or reaps those sessions" (R2-V2 line 91).
- The stop switch cannot stop a started session: "a session that has already been started cannot be stopped by it (risk R15) ... To end a running session, close it in Orca yourself; this runbook gives no command for that." (Setup line 309).
- The one guard against a double launch, `reset --forfeit-guarantee`, depends on a person looking "in Orca for a session for that issue. This runbook gives no Orca command for the second check." (Setup line 499).

Variant 1 refuses to accept "up to 6 a day, never coordinator-owned" until the cleanup rule is decided alongside it (proposal A, "What happens next", fourth bullet). That pairing is the only one of the three answers that treats session end-of-life as a precondition rather than a residual risk. It is the spec's own default (MR line 547), so choosing it costs no new design work.

I also concede below that Variant 1 holds too much: FU-1 launches one session, not six a day, so the hold falls on the wrong step.

## Steelman of Variant 2

Strongest version: Variant 2 is the spec's recommended answer word for word (MR line 547; ADJ line 790). It matches the watcher's design exactly: "The poller is a plain process, never an Orca worker, so WC-13 ... does not apply to it" (Design line 68). It follows the written ownership rule: "Every worktree gets an agent, and its creator owns it ... A worktree a human creates needs an agent too." (CLAUDE.md line 312). The day cap itself was sized for person review: "day cap | 6 per rolling 24 h | bounds sessions the owner must review" (Design line 817), so "a person reviews up to 6 a day" is the design intent, not a new burden. It unblocks WA-03, #450 edit 4 and WA-04 (MR lines 304 to 306), and it adds the useful runbook note that every watcher session writes `.dev/issues/<N>/` so the sweep shows the worktree as uncommitted (source W-07, `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-2-original.md` line 48). It is honest about its own costs (proposal B, "What it costs or risks").

What it genuinely gets right: a person is the stable, accountable owner; it keeps watcher sessions out of the coordinator contract, which the source debate explicitly recommended (R2-V2 line 93); and it lets FU-1 produce the evidence (D-A, D-B) every later decision needs.

## Steelman of Variant 3

Strongest version: Variant 3 gives the open watcher sessions an owner that already looks at the program on a schedule, instead of a person who must remember to look. The project rule permits a session to own a worktree's agent: "The eligible session that creates a worktree owns its agent(s)." (CLAUDE.md line 312). The coordinator already runs `/sc:sweep` on every wake (WORKER-CONTRACT.md line 288), so watcher sessions would at least be listed somewhere on a schedule. It points toward the deferred watcher-to-orchestrator handoff (WA-07, MR line 309), and it keeps closing as a person's action, so it does not grant the coordinator a new destructive power.

What it genuinely gets right: it is the only variant that puts the watcher sessions into a recurring check. Of the three, it addresses most directly the failure "a person forgets to look".

## Strengths claimed

1. **It is the only variant with no unowned-session failure mode.** Under Variants 2 and 3 the sessions accumulate with no closer (R2-V2 line 91; Setup line 309). At the cap, an unattended worktree can collect up to 42 sessions in a week (6 x 7, arithmetic on Design line 817). Under Variant 1 no such session is started.
2. **It ties ownership to end-of-life.** Proposal A, "What happens next", fourth bullet: the question is asked again "together with a decision on closing or reaping watcher sessions". Neither other variant decides who closes sessions; both list it under "What stays unresolved".
3. **It exposes a gap the other two hide: ownership of the creation agent is not ownership of the watcher's sessions.** Orca's creator rule covers the agent made by `orca worktree create --agent` (CLAUDE.md line 312; R2-V2 line 91). The watcher's sessions are different sessions, started later by the watcher process with `orca agent launch ... --worktree path:<worktree>` (Design lines 619 to 626). Whether Orca records those as belonging to the worktree's creator is UNVERIFIED. So under Variant 2 the named person owns one agent and only by declaration "reviews" the rest; under Variant 3 the same is true of the coordinator. Variant 1 does not make that unproven claim.
4. **It protects the double-launch guard.** `reset --forfeit-guarantee` on an `unknown` entry is safe only if a person can confirm there is no live session for that issue (Setup lines 497 to 501; WA-03 clause 2, MR line 305). With up to 6 sessions a day left open in one worktree, and those sessions visible to the sweep only as "could not determine" transcript rows (ADJ line 242), that manual check is harder each day the sessions pile up. A wrong judgement re-launches the issue (Setup line 507).
5. **It is the documented default, so it is safe to leave unanswered.** MR line 547 makes it the outcome if the owner does nothing; the remaining #450 edits still post once (MR line 304, clause 7).

## Weaknesses identified in others

**Variant 2**
- Cleanup is "closed by hand by the named person" (proposal B, first risk bullet), but the runbook gives no command to close a session (Setup line 309). The answer assigns a duty with no tool for it.
- Launched sessions run with no permission flag in the host's default mode (source W-08, `variant-2-original.md` line 49, citing runbook 14.2 and FU-6), and the session may stall at the Session Name prompt (WA-04 item (h), MR line 306). A stalled or prompt-waiting session that nobody closes is exactly the accumulation case. Proposal B names this ("open sessions with permission checks off ... sit unattended") but adds no control.
- Shared-checkout collisions: all sessions start in one checkout and each writes `.dev/issues/<N>/` there (W-07). Whether two claim sessions running in the same checkout at once can disturb each other's git state is UNVERIFIED; Variant 2 accepts the shared worktree without asking.
- "Owns that agent" covers the creation agent only (Strength 3).

**Variant 3**
- The coordinator loop is scoped to its own Run: it "keeps watching its Run until every Task it created is settled" (WORKER-CONTRACT.md line 288). Watcher sessions are not Tasks of any Run (Design line 68; ADJ line 242), so they never hold the loop open. When the program's Run settles, the coordinator stops while the watcher keeps launching: ownership lapses with no signal. Proposal C names the general instability ("A coordinator session ends and is resumed") but not this concrete failure.
- WC-16 says person-started sessions "appear in the report ... they are never messaged" (WORKER-CONTRACT.md line 288). The coordinator's "review" is therefore listing rows it cannot classify (ADJ line 242), as proposal C concedes.
- The coordinator performs outward actions "only when the user's instruction names that action" (WORKER-CONTRACT.md line 240). Creating the `issue-watch` worktree would need that instruction, which proposal C does not mention.
- It contradicts the source debate's recommended statement that watcher sessions are never coordinator-owned (R2-V2 line 93), and whether a coordinator may adopt them is UNVERIFIED (proposal C says so itself).

## Concessions

1. **Variant 1 holds the wrong step.** FU-1 (WA-04) launches one session on one test issue (MR line 306). The 6-a-day exposure starts only when the schedule is enabled (WA-05, MR line 307). The QA risks I list above arise at WA-05, not at FU-1. Holding FU-1 is over-cautious.
2. **The hold is circular.** A good cleanup rule needs FU-1's facts: does a launch create a Run (D-A), what the session rows hold (D-B) (MR line 306, items (d) and (e)). Variant 1 waits for a cleanup decision that cannot be well made without the test it blocks. Proposal A admits a deferred answer "with no trigger may stall the watcher indefinitely".
3. Variant 1 does not raise the visibility limit (C-005) at all; Variants 2 and 3 do.
4. Variant 1 leaves Q21 waiting too (MR line 548), since Q21 needs FU-1.
5. Variant 2 is the spec's recommendation and matches the design's own reason for the cap (Design line 817).

The QA-strongest answer is therefore not Variant 1 as written but Variant 2 with Variant 1's pairing moved later: a named person owns the agent and FU-1 runs, and enabling the schedule (WA-05) additionally waits for a written rule on who closes watcher sessions and when. This is a refinement for the owner to weigh, not a fourth variant.

## Shared assumptions

- **A-001 (the day cap of 6 is fixed and not a choice here): QUALIFY.** It is not configurable at run time: `DAY_CAP = 6` is a module constant under the comment "They are module constants, not operator knobs." (`src/superclaude/cli/issue_watch/cycle.py` lines 33 and 36), and the runbook says it is "fixed in the code, not in the configuration file ... If one of them has to change, that is a code change, not a configuration edit." (Setup line 238). But the same line says "The design lists them as proposals for you to confirm after the shadow run", so the number is still an owner choice. A lower cap is a one-constant code change and is a cheaper control on accumulation than any ownership rule.
- **A-002 (one shared configured worktree, whatever Q2 answers): QUALIFY.** One worktree is the design: `worktree` is a single required config value (Design line 135; Setup line 97), and every launch passes `--worktree path:<worktree>` (Design line 622). But at the default claim level each claim also starts a second agent in a worktree the claim script creates or reuses, governed by the launch-level hook (R2-V2 line 92; `claim.md` lines 99 to 120 as cited there, not re-read: UNVERIFIED by me). Under the creator rule that second worktree's agent is owned by the watcher-started claim session, which nobody owns, so the ownership gap repeats one level down. Q2 decides whether that happens.

## Per-point verdicts

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (no variant superior) | 90% | Same five sections in all three |
| C-001 | Variant 2 | 65% | Matches the creator rule (CLAUDE.md line 312) and the design (Design line 68); "nobody yet" leaves the gap open |
| C-002 | Variant 2 | 55% | The cap was sized for person review (Design line 817); my reservation is that nothing closes sessions (Setup line 309) |
| C-003 | Variant 2 | 60% | FU-1 is one session (MR line 306); holding it blocks the evidence every later decision needs |
| C-004 | Variant 1 | 60% | Only Variant 1 makes a cleanup rule a precondition; 2 and 3 leave closing to a person with no command for it (Setup line 309) |
| C-005 | Variant 2 | 55% | States the limit (ADJ line 242) and ties it to Q21's label; Variant 1 does not raise it |
| X-001 | Variant 2 | 65% | WC-16 is scoped to the coordinator's own Run (WORKER-CONTRACT.md line 288); the source debate recommended "never" (R2-V2 line 93) |
| X-002 | Variant 2 | 70% | A person outlives a coordinator session; the coordinator stops when its Run settles (WORKER-CONTRACT.md line 288) |
| X-003 | Variant 2 | 60% | The cleanup rule belongs before WA-05, not before a one-session FU-1 (Concession 1) |
| U-001 | Variant 1 | 70% | Pairing ownership with end-of-life is the one control on accumulation any variant proposes |
| U-002 | Variant 2 | 75% | Concrete, sourced (W-07) and needed by whoever reads the sweep |
| U-003 | Variant 3 | 50% | Real value for "forgot to look", weakened by the Run-scoped loop |
| A-001 | Variant 1 | 50% | Holding keeps room to pair the answer with a lower cap; 2 and 3 take 6 as given though Setup line 238 says it is a proposal |
| A-002 | Variant 2 | 50% | Only Variant 2 notes a consequence of the shared worktree (the `.dev/issues/<N>/` writes); none addresses the second-agent chain |

## Overall

Overall: the variant I judge best for the owner is Variant 2, confidence 60%. I would raise that to about 75% if the owner adds Variant 1's condition at the right step: the schedule (WA-05) is not enabled until a written rule says who closes watcher sessions and how, and the owner confirms or lowers the day cap after the shadow run as Setup line 238 invites.
