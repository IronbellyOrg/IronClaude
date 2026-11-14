# Q26: Where does the coordinator run, and on which branch is the ledger package staged?

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q26 (line 553).

> Where does the coordinator run, and on which branch is the ledger package staged? (new, R25-INV-002). If you answer "main checkout, current branch", the ledger is staged on the unrelated docs branch: that is your accepted cost

## The spec's recommended answer (verbatim)

> The main checkout (`/home/coder/workspaces/IronClaude`, today on `docs/409-orca-dashboard-designs`), on a dedicated program branch from `origin/master` that you switch to only after the current work there is safe. Alternative: an owner-created Orca worktree with `--agent` whose agent is the coordinator

## Default if unanswered (verbatim)

> XC-09 does not start; the owner keeps the ledger by hand; no program file is written on any branch; SW-01's ruling is recorded as the owner's reply on the Codex thread only (the ruling never waits for the ledger)

## What it gates (in words)

- XC-09: standing up the coordinator session, a person-opened Claude session that keeps the ledger, creates the program's worktrees through Orca with their agents, dispatches supervised workers and tracks PRs (`merged-requirements.md:457`, section 6). Edge 118 (`merged-requirements.md:765`): Q26, XC-10 and ORCA-AVAILABLE must all hold before XC-09.
- Through XC-09, every work item the coordinator dispatches to a worker (edge 119, `merged-requirements.md:766`): SW-07, SW-08, SW-10, SW-14 (sweep follow-ups), OB-05, OB-06, OB-07 (observer guard flip and routing row), WA-01, WA-03 (watcher changes), XC-05, XC-06, XC-07 (the contract note between observer and sweep), V2-03, V2-05 (Orchestrator v2 work).
- XC-01's location: the decision ledger, an always-staged package `.dev/tasks/<program-package>/` holding the owner's answers and the grant table, lives in the coordinator home on the branch Q26 names (`merged-requirements.md:449`).
- XC-10 (the first-wave intake, W0) part (3) records the answer (`merged-requirements.md:458`).
- Wave: W0 (the first wave). Ask order: Q1, then Q33, then Q26 (`merged-requirements.md:523`).

## Facts the question depends on

1. Project rule: a session never creates a worktree for its own use; every Orca worktree gets an agent; the session that creates a worktree owns its agent (project `CLAUDE.md`, section "Parallel Development with Git Worktrees"; global `~/.claude/CLAUDE.md`, "Orca session launches").
2. Project rule: "Session A: Open the main checkout (current branch); it is the orchestrator that creates the worktrees below" (project `CLAUDE.md`, "Usage" list).
3. Project rule: `.dev/tasks/` is always staged; staging is not committing (project `CLAUDE.md`, "ABSOLUTE RULE: `.dev/tasks/` Is Always Staged"). So the ledger is staged on whatever branch its checkout is on.
4. The coordinator never runs in the #539 checkout (this worktree), and no program artifact is created there (`merged-requirements.md:976`, rule 3; R25-INV-002 in `adversarial/adversarial/invariant-probe.md:10`).
5. The coordinator never switches a checkout's branch on its own (`merged-requirements.md:900`, `:951`).
6. Observed 2026-11-13 (this worker, read-only `git -C /home/coder/workspaces/IronClaude ...`): the main checkout is on `docs/409-orca-dashboard-designs` at `495eb96d1`, tracking `origin/docs/409-orca-dashboard-designs` with 0 unpushed commits; one commit ahead of the local `origin/master` ref; no modified tracked files; 21 untracked entries (all under `.claude-audit/` and `.dev/`, none under `.dev/tasks/`). `gh pr list --repo IronbellyOrg/IronClaude --head docs/409-orca-dashboard-designs --state all` returned no PR.
7. Probe finding (`invariant-probe.md:10`): every non-main worktree is bound to another issue's branch; the main checkout is the only rule-conforming existing home.
8. The alternative (an owner-created Orca worktree with `--agent` whose agent is the coordinator) depends on an `--agent`-launched agent counting as "person-opened"; no source confirms that (`refactor-plan.md:90`, `:618`). UNVERIFIED.
9. Every worker dispatch or wait also needs the Orca app to answer (ORCA-AVAILABLE); the probe found it unreachable on 2026-11-13 (`merged-requirements.md:604`). Current state UNVERIFIED.
10. SW-01's ruling on INV-008 never waits for the ledger (`refactor-plan.md:91`).
