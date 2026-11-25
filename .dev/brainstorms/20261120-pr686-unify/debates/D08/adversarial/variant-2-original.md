# D08 position paper: CLAY: the word "orchestrator" and the command /sc:orchestrator

Topic: naming and identity of the primitive (session role, command, and how issues 339, 423, 444 and Clay's design nest). Status: stub, filled below.

Written as the strongest honest case for Clay's line. Evidence paths: "master" = /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6); "pr-a" = /home/coder/.cache/ic-snap-20261120/pr-a (PR 686, Clay's rewrite of the watcher, head 8e5ae29ad); "D:nnn" = docs/designs/orchestrator.md on master (merged by PR 681, Clay's design).

## Claim

The per-repo, issue-polling session is an **orchestrator**, the command is `/sc:orchestrator` and the skill is `sc-orchestrator-protocol` (decision OQ5, D:133). "Coordinator" stays what it already is in the installed contract: a session a person opened. Two roles with two authority models get two nouns. Issues 339, 423 and 444 are the same family under one word: #339 is the general orchestrator for all sessions (a separate, later job, D:65), this design is the issue-polling orchestrator, #444's `--sub` is a sub-orchestrator, and #423 is a later knowledge layer for orchestrators.

## Mechanism

A noun is a handle for a rule set. In `WORKER-CONTRACT.md` "the coordinator" means a session the person opened that acts outward only when told (lines 70 and 239-246). The design's session is woken by a script, holds standing grants and merges on its own (ADD1, D:135; DQ6, DQ8). Giving it the same noun would silently apply or silently contradict every coordinator rule. A second noun forces the contract to say what the second role may do, which is what ADD1's new section "Orchestrated issue flow" does. The command, skill, verbs (`superclaude orchestrator ...`), the state folder `.orchestrator/` and the session tag `orchestrator-<short>-<n>` all follow from the one word, so a reader can find everything by one search term.

## Cited facts

1. **The merged design fixes the names.** D:65 gives the name `/sc:orchestrator` to the issue-polling orchestrator and leaves `--sub` to issue 444; D:133 (OQ5) fixes `src/superclaude/commands/orchestrator.md`, `src/superclaude/skills/sc-orchestrator-protocol/`, and the flags `--wake`, `--hourly`, `--resume`, `--take`. The design was merged by PR 681 on 2026-11-20 00:02 UTC and its decisions are marked "Decided" (D:1146 and following). The design's own check that the name is free (OQ5 evidence: "no command or folder with this name exists on `origin/master`") is true for file names.
2. **The word is the vocabulary of the merged and open work.** The design file uses "orchestrator" 759 times against 121 for "coordinator". PR 686 raises the word's count in `src` and `tests` from 1179 to 1816 and the number of files containing it from 237 to 279 (counted over the master and pr-a snapshots). Master already carries a forward reference: `src/superclaude/skills/agent-work-report/SKILL.md:12` ("The orchestrator (`/sc:orchestrator`) does every check-in itself"), merged by PR 684 (Clay, moves the work-report skill into IronClaude). Issue 655's title is "Issue-polling orchestrator".
3. **The owner's own tracker uses the word for this role, and proposed this very command first.** Issue 444 (owner, 2026-11-08) is titled "Evaluate ... /sc:orchestrator having a Sub-Orchestrator or Coordinator mode" and its body says "the proposed `/sc:orchestrator` command" and "As an orchestrator, I want ...". Issue 339 (owner, 2026-11-01) is "Orchestrator - To Run and manage ALL sessions": "main session goes into orchestrator mode ... that session will be permanently flagged as the Orchestrator". Issue 423 (owner) is "Orchestrator v2" and says "Each Orchestrator". Issues 431 and 462 (owner, closed) say "Orchestrator waits on quiet workers" and "Orchestrator-spawned sessions default to Opus". The owner's wording is also "coordinator (aka orchestrator)" (D08 topic block in TOPICS.md; primary source not found, UNVERIFIED).
4. **The owner's own "everywhere" rule was recorded narrowly.** ZS-REQ row R10 (zero-setup requirements, line 41) sits in a row about the name of the watcher's worktree and branch (`Coordinator`), and its "everywhere" is a requirements-file paraphrase of a Coder issue (516) whose text could not be read here (UNVERIFIED). The owner did not rename issues 339, 423 and 444 afterwards: all three still say "orchestrator" on 2026-11-20. So the rule did not reach the owner's own tracker.
5. **"Coordinator" is already taken in Clay's deployed world.** D:93 and D:714: the single report session has the ccsession tag `coordinator` and is woken by the automations `coordinator-morning-wake` and `coordinator-missed-check`; D:862: its state is `.dev/coordinator/`; the `agent-work-report` skill on master uses the word 23 times; the spec file is `SPEC-AGENT-WORK-COORDINATOR-20261027.md`. Calling the new per-repo session a coordinator too would put two different sessions under one tag family (the analyst file C-worktrees.md line 45 already counts "a third coordinator in the design").
6. **The Orca layer is "orchestration", and the session drives it.** The design's wave table (issue 655 section 2) is built from `orca orchestration run-create`, `worker-start`, `check`, `gate-create` and the rest; the session binds a Run and reads the mailbox. "Orchestration" (Orca's layer name, `orca orchestration --help`) plus "-or" is the natural agent noun for the session that drives it. The same pattern names `agents/debate-orchestrator.md` and the skill orchestrators in 63 installed files: in this repository "the orchestrator" is the session that runs a wave-based protocol and delegates the work.
7. **The conflict with the contract is real and is already handled by a second noun.** D:135 (ADD1) lists the contradictions with `WORKER-CONTRACT.md:23`, `:244` and `:239-246`, and resolves them by adding a section that defines "the orchestrator" as a separate party (D:799: "a standing-grant coordinator and not a worker"). A distinct noun is the cheapest way to keep the person-opened rules intact: the coordinator rules are not touched and an orchestrator rule cannot leak into them.
8. **The nesting is already written down.** D:65 places #339 (the general orchestrator for all sessions) outside this design, this design as the issue-polling orchestrator, `--sub` with #444, and D:1277 (U19) records "how #444 joins ... the owner reconciles when #444 is evaluated". Issue 423 says v2 follows "after the v1 orchestrator (#339) is complete" and uses "Orchestrator" for the actor throughout.

## What it costs

- Two nouns for two roles, forever: a glossary line in `HOW-WE-WORK.md` and the contract, and a reader has to learn which is person-opened and which is script-woken.
- A word collision with the parent-agent meaning in 63 installed files (reflect, troubleshoot, adversarial, `debate-orchestrator`): "the orchestrator" now has two meanings in installed text. The mitigation is the longer names `sc-orchestrator-protocol` and `/sc:orchestrator`.
- A visible contradiction with the owner's decision of 2026-11-18 (ZS-REQ R10) and with Coder issue 516's `COORD-<RepoName>` session name, which would need a second session or a decision that the owner's coordinator and Clay's orchestrator share one session (D07 decides topology).

## What it risks

- The owner reads "orchestrator" as the exact word they ruled out and sees the merge as a reversal made without them; the debate weighting rule makes that decisive unless there is a separable benefit.
- If the owner's coordinator and Clay's orchestrator end up as one session per repo (D07), the second noun names nothing and is pure overhead.
- Issue 655's body, 15 comments and the PR texts all say "orchestrator" and cannot be edited by this debate; a rename leaves GitHub text and master text disagreeing until the owner edits them.

## What it gets right

- It notices that the per-repo script-woken session has a different authority model and gives it a name, rather than hiding that in a qualifier.
- It names the third thing (the report session) and keeps it apart.
- It gives one complete naming scheme (command, skill, verbs, state folder, tag) that is already merged as design text.
- It records the collision with issue 444 and leaves `--sub` to it (D:65, U19), which is more care than the owner's own issue titles took.
