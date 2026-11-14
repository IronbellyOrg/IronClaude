# Q20 final: who owns the agent in the watcher worktree, and may it hold up to 6 coordinator-less sessions a day?

Q20 is about the issue watcher (issue #331, rolled out under #450): a background process that, when an issue is approved, starts a Claude session to claim it. All its sessions start in one configured Orca worktree, at most 6 in 24 hours, and nothing closes them. The question asks who owns that worktree's agent, and whether those sessions may stay outside any coordinator (the person-opened Claude session that runs this program).

## Debate result

Winner: proposal B (a person you name creates the watcher worktree with an agent and owns it; watcher sessions stay ordinary top-level sessions that person reviews, never coordinator-owned). Confidence 70 percent. The advocates agreed 3 of 3: the advocates for A and C both judged B best (60, 70 and 70 percent). Convergence 91 percent (10 of 11 points; the open point was whether the 6-a-day cap is fixed, carried into the merge).

Evidence that decided it:
- The watcher's own design is built around one person: "The poller is a plain process, never an Orca worker" (`docs/designs/issue-watcher.md` line 68); the day cap "bounds sessions the owner must review" (line 817); the runbook already says "Expect sessions to stay open ... look at the open sessions now and then" (`docs/designs/issue-watcher-setup.md` line 571).
- A coordinator is a poor owner: its loop "keeps watching its Run until every Task it created is settled" (`src/superclaude/core/WORKER-CONTRACT.md` line 288), while the watcher has no end date; and watcher sessions read text any commenter can write, which should not flow into the session that "performs every outward action" (WORKER-CONTRACT.md line 69).
- Holding everything (proposal A) blocks the wrong step: the first live test (FU-1) launches one session on one test issue (merged-requirements.md line 306); the 6-a-day exposure only starts when the schedule is enabled (WA-05, line 307).

Proposal A (name no owner yet; hold FU-1; this is the spec's default). Strength: the only answer that treats ending sessions as a precondition; the runbook gives no command to end a running session (setup line 309). Weakness: circular, because a good cleanup rule needs FU-1's facts; no trigger to resume; its own advocate judged B better.

Proposal B (named person owns). Strength: matches every person-anchored trust control in the watcher, keeps outsider-written text away from the coordinator, and lets FU-1 record the session's real permission mode. Weakness: nothing closes sessions; relies on one person's diligence; a single point of failure.

Proposal C (the coordinator session creates and owns the agent). Strength: puts watcher sessions into a check that already runs. Weakness: the coordinator's duty ends with its Run, it cannot see these sessions beyond "could not determine" transcript rows (ADJ line 242), it would need a coordinator-contract change no plan schedules, and it contradicts the source debate's recommendation that watcher sessions are never coordinator-owned (round2-rebuttal-V2.md line 93).

Merged answer: OUT/Q20/merged-proposal.md (B plus: a written rule on who closes watcher sessions before the schedule is enabled; the cap stated as "the confirmed day cap, default 6", since `DAY_CAP = 6` is a code constant the design lists as a proposal to confirm after the shadow run, verified at `src/superclaude/cli/issue_watch/cycle.py` lines 33 and 36 and setup line 238; a review cadence and an absence fallback; a note that the person owns later sessions by this decision, not by Orca's record; an optional read-only count of open sessions in the coordinator's check, with no transcript reading; and, if Q2 keeps the default claim level, naming who owns the per-issue `issue-<N>` agents).

## Final recommendation

Name one person who creates the `issue-watch` worktree with an agent and owns it. Accept up to the confirmed day cap (default 6) of watcher sessions a day, as ordinary top-level sessions that person reviews, never coordinator-owned. Let the one-session first live test run now; before the schedule is switched on, write down who closes watcher sessions and by when, how often the person checks, and who covers (or that the schedule is off) while they are away.

Confidence: 70 percent.

Single strongest reason: the watcher was designed as a plain process whose sessions a person reviews (its day cap exists to bound that review), and a coordinator's duty ends with its own Run while the watcher runs indefinitely.

Equals the spec's recommended answer: yes. The merged additions (cleanup rule before the schedule, confirmed cap, cadence and fallback) refine it.

## What would change the answer

If the watcher-to-orchestrator handoff (WA-07, deferred and unbuilt) were built with a contract that lets a coordinator own sessions it did not start, proposal C would become viable. If you cannot name a person who will actually review the sessions, proposal A (hold) is safer.

## Criticality rating

- Security or trust boundary: high
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer must name a real person and accept, in writing, that up to six sessions a day reading outsider-written issue text may stay open outside any coordinator, which only the owner can do. The debate converged on the shape of the answer, but no file holds who that person is or whether they will review the sessions.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q20/adversarial/ (diff-analysis.md, round1-advocate-1.md to round1-advocate-3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml)
- fallback_mode: false (three advocate sub-agents and a merge-executor sub-agent were spawned; the diff analysis, scoring and refactor plan were done by this worker session in the orchestrator role)
