# Round 1 advocate statement: Variant 1 (owner-created Orca worktree whose agent is the coordinator)

Advocate persona: architect (structure, dependencies, long-term impact). Depth: quick, Round 1 only.

## Position summary

Variant 1 gives the program a home that belongs to the program alone: its own worktree, its own branch from `origin/master`, and its own git index, so the always-staged ledger can never be carried onto an unrelated branch and no second session shares the folder. Its one real gap is whether an `--agent` launch counts as "person-opened"; that gap is a definitional question the owner can settle in one sentence, while Variant 2's gaps (a moving branch under a staged ledger, a shared workspace) are structural and last for the program's whole life.

## Steelman of Variant 2

Strongest version: the spec, the worker contract and the routing guide all describe the coordinator as a session the person opened (`merged-requirements.md:931` "a person-opened Claude session"; `~/.claude/WORKER-CONTRACT.md:69` "an Orca coordinator session the person opened"; `~/.claude/HOW-WE-WORK.md:401` "The coordinator is a session the person opened"). Variant 2 is the only option that meets that wording with no interpretation at all: the owner types `claude` in a checkout they already own. It also sits in the place the project names ("Session A: Open the main checkout (current branch); it is the orchestrator", project `CLAUDE.md`, Usage list), creates no new worktree, and its first step is a plain git switch that does not need Orca. That last point is real: the ledger (XC-01) could be written before Orca is reachable again, which Variant 1 cannot do. Its measured evidence is also good: the docs branch had 0 unpushed commits, no modified tracked files and no PR on 2026-11-13 (`question.md:32`), so "safe to leave" already appears to hold. The reconciliation in `refactor-plan.md:90` chose this route for exactly these reasons.

## Steelman of Variant 3

Strongest version: three facts that decide Q26 are unsettled today (Orca reachability, `merged-requirements.md:604`; whether `--agent` counts as person-opened, `refactor-plan.md:90`; whether the docs branch work is finished), so any home named now may be wrong, and the cheapest wrong answer is no answer. Nothing urgent is lost: SW-01's ruling never waits for the ledger (`refactor-plan.md:91`), SW-01 to SW-05 run under the #539 author, and while Orca is down XC-09 could not dispatch anything anyway (A-003). Variant 3 is the only option with zero irreversible steps and it builds in a re-ask point (U-003) tied to the first real need.

## Key strengths claimed

1. **The staged ledger stays on the program branch for the program's life.** Staged files live in a checkout's index, not on a branch, and travel with a later `git switch` when nothing conflicts (diff-analysis A-001; standard git behaviour, not re-tested here). Each Orca worktree has its own index and its own branch, and the coordinator "never switches a checkout's branch on its own" (`merged-requirements.md:951`, `:976`). In Variant 1 nobody has any reason to switch that worktree, so "the ledger is staged on the program branch" stays true. In Variant 2 the main checkout is the owner's everyday folder; the first time the owner switches back to do docs work, the staged ledger rides along onto that branch. This is the exact failure the question warns about ("the ledger is staged on the unrelated docs branch", `question.md:7`), returning by a different door.
2. **One live agent per worktree holds without discipline.** Spec 6.2: "one worktree never holds two live agents" (`merged-requirements.md:951`). Variant 1's worktree exists only for the coordinator. Variant 2's main checkout is also where the owner drafts issues and does docs work (Variant 2's own cost list, `variant-2-original.md:21`), so every extra session the owner opens there breaks 6.2 (diff-analysis A-002).
3. **Ownership is clean under the project rules.** The person, not a session, runs `orca worktree create ... --agent claude --prompt ...`, so "no session creates a worktree for its own use" holds and "the eligible session that creates a worktree owns its agent(s)" resolves to the person (project `CLAUDE.md`, Parallel Development section; global `~/.claude/CLAUDE.md:58`). The refactor plan itself conceded "a human may create a worktree that gets an agent, so the probe's 'only the main checkout' is too strong" (`refactor-plan.md:90`).
4. **The worktree is made the way the spec already prescribes.** 6.2 line 954 gives the exact command form for a top-level agent's worktree: `orca worktree create --name <name> --base-branch origin/master --agent claude --prompt "<task>"`. Variant 1 uses that form unchanged (`variant-1-original.md:5`); it adds no new mechanism.
5. **Its Orca dependency adds no new gate.** XC-09 cannot start without ORCA-AVAILABLE in any variant (edge 118, `question.md:19`; `merged-requirements.md:604`). Variant 1's need for Orca to create the worktree is the same gate, met at the same moment, not an extra one.
6. **Clean commit surface.** The program branch starts from `origin/master` with nothing else in it, so a later "commit the ledger" request stages only program files. Variant 2's folder keeps 21 untracked entries from other work beside the ledger (`question.md:32`; diff-analysis U-004).
7. **The main checkout stays free.** The owner's other work keeps its branch and its folder (C-004), so the program does not hold the owner's primary workspace hostage for weeks.

## Weaknesses identified in Variant 2

1. **It does not follow the rule it cites.** The project text says "Open the main checkout (current branch)". Variant 2 changes the current branch before opening the session. Read literally, the rule produces the docs-branch staging the question calls an accepted cost; Variant 2 already treats the text as guidance to adapt, which is the same latitude Variant 1 takes (X-002). The line also sits under a "Usage" heading of examples next to illustrative worktree names (`integration`, `pm-agent`), which supports reading it as an example.
2. **The staged ledger is not anchored** (strength 1 above). Nothing in Variant 2 stops the owner's next ordinary branch switch from carrying the ledger off the program branch; it relies on the owner remembering, for weeks, not to switch.
3. **Concurrency in the owner's main workspace** (strength 2 above). Variant 2 admits other work "must move or share the branch" (`variant-2-original.md:21`); sharing the branch means sharing the folder, which is a second live session in the coordinator home.
4. **A manual, timing-sensitive switch.** The owner must judge "safe" and switch by hand (`variant-2-original.md:22`); the 2026-11-13 observation may be stale by the time Q26 is answered.

## Weaknesses identified in Variant 3

1. **It contradicts a hard W0 exit rule.** 6.4 rule 3: "before W0 exits the owner names the coordinator's home and the branch that stages the always-staged ledger package" (`merged-requirements.md:976`). Variant 3 leaves W0 unable to exit cleanly.
2. **The grant table goes off disk.** Every outward action needs a `GRANT(<item>,<action>)` row in the ledger (6.3 Owner row, `merged-requirements.md:961`). Variant 3 keeps it in the owner's notes, so no agent can read it and every grant must be restated each session (X-003; `variant-3-original.md:22`).
3. **It blocks 15 dispatched items** (SW-07, SW-08, SW-10, SW-14, OB-05 to OB-07, WA-01, WA-03, XC-05 to XC-07, V2-03, V2-05; `question.md:20`) and resolves nothing; it only defers the same question.

## Concessions

1. **"Person-opened" is Variant 1's real weak point.** The spec classifies an `--agent` launch as "a top-level agent" (`merged-requirements.md:951`), and the coordinator is defined as person-opened (`:931`; `WORKER-CONTRACT.md:69`). The routing guide's explicit exclusion is narrower, "never a session that Orca itself started as a worker" (`HOW-WE-WORK.md:401`), and a `worktree create --agent` session is not a `worker-start` worker, so Variant 1 is not ruled out; but no source says it qualifies. UNVERIFIED. The owner would need to state that a session they launch through Orca and then attend counts as person-opened. Whether the owner can simply attend that agent's terminal and drive it as an ordinary session is also UNVERIFIED.
2. **Variant 1 cannot start the ledger while Orca is down;** Variant 2 can (A-003 qualification below).
3. **One more worktree on a host that already has 19** (`variant-1-original.md:23`), and the owner must verify the coordinator's first screen, since a launch receipt is not proof (memory `orca-worker-resume-verify-screen.md`, which exists).
4. **On rule wording alone (X-001, X-002), Variant 2 is ahead.** My case is that structure over the program's life should outweigh wording, not that the wording favours me.

## Shared assumption responses

- **A-001 (staged ledger "on branch X" holds over time): ACCEPT.** The mechanism is right: staged files sit in the checkout's index and follow a non-conflicting switch (standard git behaviour; not re-tested in this round). It is the main structural reason to prefer Variant 1, whose worktree never needs to switch. Both Variant 1 and Variant 2 should replace "staged on that branch" with "staged in that checkout's index, which stays on that branch only while the checkout does".
- **A-002 (one live session in the coordinator home): ACCEPT.** It is a stated spec rule, not just an assumption: "one worktree never holds two live agents" (`merged-requirements.md:951`). Variant 1 meets it by construction; Variant 2 meets it only if the owner moves all other work out of the main checkout for the program's life.
- **A-003 (Orca must answer before XC-09): QUALIFY.** True for XC-09 and every dispatch in all three variants. But the gate falls at different points: in Variant 2 the ledger (XC-01) and the owner's answers can be staged before Orca returns, because the home is created with git alone; in Variant 1 the home itself needs Orca, so the ledger waits too. That is a real, if short, sequencing cost for Variant 1.

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie (V1 = V2 = V3) | All three use the same five sections and four steps; no structural edge. |
| C-001 | V1 | A home that belongs to the program alone avoids the index-travel and shared-folder problems for the program's whole life. |
| C-002 | V1 | The ledger's index lives in a worktree that never switches branch, so "staged on the program branch" stays true. |
| C-003 | V2 | A git-only switch needs no Orca and nothing unverified, so the ledger can start before ORCA-AVAILABLE. |
| C-004 | V1 | Leaves the main checkout untouched while still unlocking XC-09; V3 is untouched but unlocks nothing. |
| X-001 | V2 | Only V2 is person-opened by the plain wording of `merged-requirements.md:931` and `WORKER-CONTRACT.md:69`; V1's status is UNVERIFIED. |
| X-002 | V2 | V2 is closer to the "Session A" text, though it too departs from "(current branch)"; V1 treats it as an example. |
| X-003 | V1 | V1 and V2 both keep the grant table on disk; V1's copy cannot be carried off its branch by a later switch, and V3's is off disk. |
| A-001 | V1 | Only V1's home never switches branch, so the staged ledger cannot travel. |
| A-002 | V1 | V1's worktree is the coordinator's alone by construction; V2's is the owner's general workspace. |
