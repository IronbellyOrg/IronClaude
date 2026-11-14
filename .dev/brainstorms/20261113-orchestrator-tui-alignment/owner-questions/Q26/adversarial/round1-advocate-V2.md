# Round 1 advocate statement: Variant 2 (main checkout, owner switches it to a program branch from origin/master)

Persona: analyzer (evidence quality, logical consistency). Depth: quick, Round 1 only.

## Position summary

Variant 2 is the only option that satisfies every hard requirement the spec puts on the coordinator today: a person opens it (XC-09 part 1), it runs in an existing home the project rule names for the orchestrator, and the ledger lands on disk on a branch that carries nothing unrelated. Its real weakness is that "staged on a branch" is not durable in git (A-001) and that the main checkout is also the owner's general workplace (A-002); both need a stated mitigation, not a different home.

## Steelman of Variant 1

Strongest version: a person (the owner, not a session) runs `orca worktree create --base-branch origin/master --agent claude`, so no session creates a worktree for its own use, and the project rule explicitly allows it: "A worktree a human creates needs an agent too" (project `CLAUDE.md:312`). The result is a home whose only purpose is the program: its branch never switches, so the staged ledger can never ride a later `git switch` onto another branch (the exact hazard of diff-analysis A-001), and no second session of the owner's other work can land in it (A-002). The main checkout and its 21 untracked entries stay untouched (V1 step 4). The refactor plan itself agrees the probe's "only the main checkout" claim is too strong (`refactor-plan.md:90`: "V1 and V3 are right that a human may create a worktree that gets an agent ... (PARTLY)"). On isolation and long-run state hygiene, V1 is genuinely better than V2.

## Steelman of Variant 3

Strongest version: Q26's own default is exactly V3 (`merged-requirements.md:553`, default column), so V3 is the spec-sanctioned safe choice when the owner lacks the facts. Two of the facts that decide between V1 and V2 are open today: ORCA-AVAILABLE was unreachable on 2026-11-13 and "this spec does not claim that outage is still current" (`merged-requirements.md:604`), and whether an `--agent` agent counts as person-opened is UNVERIFIED (question.md fact 8). Since XC-09 cannot dispatch anything without Orca anyway (edge 118, `merged-requirements.md:765`), naming a home now buys nothing until Orca answers; and the work that does not need a coordinator (SW-01 to SW-05, GitHub-only edits, SW-01's ruling which "never waits for the ledger", `refactor-plan.md:91`) still proceeds. V3's re-ask rule (U-003) makes the eventual answer use then-current facts instead of stale ones.

## Key strengths claimed

1. **Only variant that meets XC-09 part 1 with certainty.** XC-09 requires "A person opens it (a coordinator is person-opened; it is not a worker)" (`merged-requirements.md:457`), and section 6 restates "a person-opened Claude session" (`merged-requirements.md:931`). In V2 the owner opens the session by hand (V2 step 3). V1's equivalent is UNVERIFIED by its own admission (V1 "What it costs or risks", first bullet), and the refactor plan rejected V1 as the recommendation for that reason (`refactor-plan.md:618`, row 31).
2. **Follows the project's named orchestrator location.** Project `CLAUDE.md:336`: "Session A: Open the main checkout (current branch); it is the orchestrator that creates the worktrees below." The invariant probe found the main checkout to be "the only rule-conforming home" among existing worktrees (`invariant-probe.md:10`). Note the qualifier in strength 7 below on "current branch".
3. **Matches the spec's own recommended answer.** Q26's recommended answer (`merged-requirements.md:553`), XC-09's "runs in" cell (`:457`) and the 5.4 table row (`:900`) all name the main checkout on a dedicated program branch from `origin/master`. V2 is that answer, verbatim in substance.
4. **Setting up the home does not depend on Orca.** V2's first action is a git branch switch plus opening a session (diff-analysis C-003). V1 cannot even create its home while Orca is down (V1 risk 2; `merged-requirements.md:604`). V2 can therefore record XC-10 part (3) and write the ledger (XC-01) before Orca returns, which XC-09's own text allows ("XC-01 may be kept by the owner before it exists", `:457`), and still keep the grant table on disk.
5. **Precondition already measured, and re-measured today.** V2 cites the docs branch state of 2026-11-13 (U-002). I re-checked read-only on 2026-11-14 (`git --no-optional-locks -C /home/coder/workspaces/IronClaude status`): branch `docs/409-orca-dashboard-designs` at `495eb96d1`, in sync with `origin/docs/409-orca-dashboard-designs`, 0 modified tracked files, 21 untracked entries, none under `.dev/tasks/`. So "safe to leave" already appears to hold; the switch carries no tracked changes.
6. **Respects "the coordinator never switches a checkout's branch on its own"** (`merged-requirements.md:900`, `:951`, `:976` rule 3): V2 assigns the switch to the owner (V2 step 2).
7. **Avoids the accepted cost the question warns about.** Q26 states that "main checkout, current branch" stages the ledger on "the unrelated docs branch" (`merged-requirements.md:553`). V2 departs from `CLAUDE.md:336`'s literal "(current branch)" for exactly that reason; the location is followed, the branch is changed by the owner. I flag this openly: V2 follows the rule's place, not its parenthetical.

## Weaknesses identified in Variant 1

1. **Its central premise is UNVERIFIED and load-bearing.** If an `--agent`-launched agent is not person-opened, the session is "a top-level agent" in the spec's own vocabulary (`merged-requirements.md:457` part 3 distinguishes `worker-start` workers from `--agent` top-level agents), not a coordinator, and XC-09 part 1 fails. V1 acknowledges this; it does not resolve it.
2. **Blocked by the same outage that blocks dispatch, one step earlier.** V1 needs Orca to create the home (V1 risk 2), so nothing, not even the ledger on disk, can exist until ORCA-AVAILABLE holds. V2 gets the ledger on disk now.
3. **Leaves the project's named orchestrator location unused and argues it is "an example"** (V1 "What stays unresolved", second bullet). The text at `CLAUDE.md:336` sits under a heading "Usage" in an ABSOLUTE RULE section; reading it as an example is possible but is V1's interpretation, not a cited fact (UNVERIFIED either way).
4. **Ownership chain is muddier.** `CLAUDE.md:312` says "The eligible session that creates a worktree owns its agent(s)". In V1 a person, not a session, creates it; the rule then only says "A worktree a human creates needs an agent too", with no statement of who owns that agent. V1 step 1 asserts the person owns it; that is a reasonable reading but UNVERIFIED.
5. Minor: a twentieth worktree on a host with 19 (V1 risk 3; probe count in `invariant-probe.md:10`), and a first-screen check the owner must do (U-001).

## Weaknesses identified in Variant 3

1. **Unlocks nothing.** Every edge-119 item waits (V3 risk 1): SW-07, SW-08, SW-10, SW-14, OB-05 to OB-07, WA-01, WA-03, XC-05 to XC-07, V2-03, V2-05 (`merged-requirements.md:766`).
2. **Breaks the grant mechanism in practice.** XC-01 part (5) says an edge `GRANT(<item>,<action>)` "is satisfied only by a matching row" in the ledger (`merged-requirements.md:449`). With the ledger in the owner's notes, no agent can read that row from disk, so every grant is restated per session (V3 risk 2; diff-analysis X-003). That is the opposite of the always-staged practice (`CLAUDE.md`, "`.dev/tasks/` Is Always Staged").
3. **Defers without changing the facts V2 needs.** V2's preconditions (owner present, docs branch safe) are already measured true (strength 5). The two facts V3 waits for (Orca reachability, `--agent` person-opened) only matter to V1's home or to dispatch, not to whether V2's home can be named.
4. **W0 exit criterion.** Rule 3 says "before W0 exits the owner names the coordinator's home and the branch" (`merged-requirements.md:976`). V3 records a hold under XC-10 (which XC-10 allows: "or held with a reason", `:458`), so it is legal, but it keeps W0 from exiting cleanly.

## Concessions

1. **A-001 hits V2 hardest.** Staged files live in the index, not on a branch. If the owner later switches the main checkout back to a docs branch while the ledger is staged but uncommitted, it goes along and could be committed there. V2 does not mention this. Because "staging is not committing" and the ledger is "committed only when the owner asks" (`merged-requirements.md:449`), V2 needs an explicit rule: the main checkout does not leave the program branch while the ledger is uncommitted, or the owner asks for a ledger commit before any switch. V1 does not need this rule.
2. **A-002 also hits V2.** The main checkout is the owner's everyday workplace; a second Claude session there would be a second live agent in the coordinator home, which conflicts with "one worktree never holds two live agents" (`merged-requirements.md:951`). Whether that rule covers the main checkout is UNVERIFIED, but V2's cost bullet ("other work ... must move or share the branch") understates it: other work must move, not share.
3. **V1 has the cleaner branch.** In V2 the 21 untracked entries from other work sit beside the ledger (V2's own U-004); in V1 nothing unrelated is present.
4. **V2 still needs Orca for everything after the ledger.** The setup advantage (strength 4) does not let XC-09 dispatch anything while Orca is down (edge 118).
5. **V2 changes the literal "(current branch)" of `CLAUDE.md:336`.** Justified by the question's warning, but it is a departure.

## Shared assumption responses

- **A-001 (the ledger "is staged on branch X" holds over time): QUALIFY.** Correct as a git fact: staged new files are in the checkout's index and follow a non-conflicting `git switch`. It is true at the moment of staging and false as a durable guarantee. For V1 it holds in practice because the dedicated worktree never switches. For V2 it holds only with an added rule: no branch switch in the main checkout while the ledger is uncommitted (or an owner-requested commit first). I accept that V2 must carry that rule.
- **A-002 (only one live session in the coordinator home): QUALIFY.** The spec rule is "one worktree never holds two live agents" (`merged-requirements.md:951`), written about `worker-start` versus `--agent` (Change 1). Applying it to the owner's own extra sessions in the main checkout is a reasonable extension but UNVERIFIED. Either way, V2 should state that the owner's other Claude work leaves the main checkout for the program's life; V1 satisfies this by construction.
- **A-003 (Orca must answer before XC-09 starts): ACCEPT.** Stated directly in edge 118 (`merged-requirements.md:765`) and the ORCA-AVAILABLE definition (`:604`). It binds all three. It costs V1 more, because V1 also needs Orca to create the home itself; V2 and V3 can do their pre-Orca steps without it.

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie (all three) | Identical five-section structure with four steps each; no variant gains here. |
| C-001 (where the coordinator runs) | V2 | Only home that is both person-opened for certain and named by `CLAUDE.md:336` and the spec's recommended answer (`merged-requirements.md:553`). |
| C-002 (where the ledger is staged) | V1 | A dedicated branch in a worktree that never switches keeps the staged ledger isolated; V2 matches only with an added no-switch rule (A-001). |
| C-003 (first owner action and dependency) | V2 | A git switch the owner can do now, with the precondition measured true on 2026-11-14; V1 needs Orca, V3 does nothing. |
| C-004 (effect on the main checkout) | V1 | Leaves the main checkout and its untracked work untouched; V2 occupies it for the program's life. |
| X-001 (is the coordinator person-opened) | V2 | The owner opens it by hand; V1's claim is UNVERIFIED by its own text and by `refactor-plan.md:618`. |
| X-002 (`CLAUDE.md` "Session A" rule) | V2 | Follows the named place; V1 reclassifies a rule as an example without a source (V2 does change the "(current branch)" parenthetical). |
| X-003 (where the grant table lives) | V2 (V1 equal on this point) | Both V1 and V2 put it on disk where agents can read it (`merged-requirements.md:449` part 5); V2 can do so before Orca returns, V3 cannot at all. |
| A-001 (staged-on-branch durability) | V1 | The worktree never switches; V2 needs an explicit no-switch or commit-first rule to match. |
| A-002 (one live session in the home) | V1 | Exclusive by construction; V2 must move the owner's other sessions out of the main checkout. |
