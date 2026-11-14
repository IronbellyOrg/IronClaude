# Q20: who owns the agent in the watcher worktree, and may it hold up to 6 sessions a day never owned by a coordinator?

## The question (verbatim from the spec row)

"Who owns the agent in the watcher worktree; may it hold up to 6 sessions a day never owned by a coordinator?"
Source: merged-requirements.md section 3, row Q20 (line 547). ADJ Part 7 row Q20 (line 790): "Who owns the agent in the watcher worktree, and may that one worktree hold up to 6 new sessions a day that are never owned by a coordinator?"

## The spec's recommended answer

"A named person owns it; watcher sessions stay person-reviewed top-level sessions." Source: merged-requirements.md line 547; ADJ line 790.

## Default if unanswered

"PLAN INFERENCE: WA-03 not shipped; WA-04 does not run; #450 edit 4 is omitted from the WA-02 set and recorded (XC-02 (6))." In words: the watcher runbook step that creates the watcher worktree and names its owner is not written, the watcher's first live test (FU-1) does not run, and the edit to issue #450 (the watcher rollout issue) that would add that runbook step is left out of the single ordered set of #450 edits, with the omission recorded. Source: merged-requirements.md line 547.

## What it gates (work items, in words)

- WA-03: runbook step 1.3a in `docs/designs/issue-watcher-setup.md`: a person creates the watcher worktree with `orca worktree create --name issue-watch --agent claude --prompt "<task>"` and names who owns its agent; plus the rule that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in that worktree. merged-requirements.md line 305.
- WA-02 edit 4: the #450 edit that adds step 1.3a. merged-requirements.md line 304.
- WA-04: FU-1, the watcher's first live test on one test issue, which runs in the `issue-watch` worktree that WA-03's step creates. merged-requirements.md line 306.
- Wave: W1. Line 547.

## Facts the question depends on

1. The watcher (issue #331, rollout #450) is a poller that starts a claim session for an approved issue. ADJ glossary line 79.
2. "The watcher is a plain process, never an Orca Worker (`issue-watcher.md:68`), so no coordinator, Run or WC-16 loop owns the first session; WC-13 does not apply to it. It starts in one configured worktree ... up to the day cap of 6 per 24 h (`issue-watcher.md:501`), and nothing closes or reaps those sessions." round2-rebuttal-V2.md line 91 (code and design citations as quoted there, not re-read here).
3. Orca's rule: the creator of a worktree made with `orca worktree create --agent` owns its agent; "the runbook does not say who that person is (V2 W-07)". round2-rebuttal-V2.md line 91. The project rule says the same: "Every worktree gets an agent, and its creator owns it ... The eligible session that creates a worktree owns its agent(s)" (ROOT/CLAUDE.md, Git Workflow section).
4. Review 02 finding W-07: all watcher sessions (up to 6 a day, left open) start in one configured worktree; every watcher session writes `.dev/issues/<N>/` there, so the sweep will show the worktree as uncommitted, not removable. variant-2-original.md line 48.
5. Whether any later Phase 2 coordinator would adopt watcher sessions is UNVERIFIED; the recommended action is that the owner names the person and states that watcher sessions are never coordinator-owned. round2-rebuttal-V2.md line 93. A watcher-to-orchestrator handoff is a deferred, unbuilt item (WA-07, merged-requirements.md line 309).
6. Sessions with no Orca Run (watcher-launched, person-started) are not observable by the observer and appear in the sweep only as transcript rows, "could not determine" today. ADJ line 242.
7. At the default claim level a second agent is started by the claim script and is governed by the launch-level hook; the first session is not. round2-rebuttal-V2.md line 92. Q2 (the claim level, recommended `--pipeline none`) decides whether that second agent exists.
8. Related: Q21 (may the sweep label machine-started sessions separately) is recommended "yes, in Phase 2, only after FU-1 shows what the rows hold". merged-requirements.md line 548.
