# Proposal B: one shared coordinators branch, scope folders with one sub-folder per developer, and claim files as locks

**In one sentence.** One shared `coordinators` branch per project; under `.dev/coordinators/` the first level is the scope (an epic or a release), the second level is the developer, so one coordinator is the pair (scope, developer) and owns exactly one folder; several developers may coordinate one epic at once, and a top-level `claims/` folder of create-once files stops two coordinators dispatching the same item.

**Terms.** A *coordinator* is a person-opened Claude session that keeps a decision ledger, a grant table (the outward actions an approver has allowed, one row each), an intake record, worker briefs and result paths, and starts workers through Orca (the local agent-orchestration app). An *epic* is a body of work spanning several issues (for example issue #339 "orchestrator mode"). A *release* is a shipped version (for example `v5.1.0`; the project's version is 5.0.0 in `pyproject.toml`). A *developer handle* is the developer's GitHub login, lower-cased. A *claim* is a file whose existence says "this coordinator owns this item".

**Facts this proposal rests on (read 2026-11-14).**
- `gh api user --jq .login` prints `ironbelly` on this host; `git config user.name` prints `coder`, the Coder workspace default, so `user.name` is not an identity and is never used in a name. Commit authors in the last 200 commits include `Ironbelly`, `Ryan wiancko`, `clayphi` and `coder`.
- `git worktree list` shows Orca-created worktrees at `/home/coder/workspaces/worktrees/IronClaude/<name>` on branch `ironbelly/<name>`. Where the `ironbelly/` prefix comes from is UNVERIFIED; this proposal calls it `<orca-prefix>`.
- One worktree never holds two live agents (merged spec 6.2, `merged-requirements.md:951`). So each coordinator session needs one worktree of its own.
- The slug grammar `^[a-z0-9]+(-[a-z0-9]+)*$` is already used by `/sc:issue` (`src/superclaude/skills/sc-issue-protocol/refs/create.md:15`); UTC stamps `YYYYMMDD-HHMMSS` are already used by `.dev/tasks/to-do/TASK-WF-*` and `.dev/sweeps/<stamp>-sweep.md`.
- `.dev/coordinators/` does not exist today (checked with `ls`); no `.gitignore` rule names it.

## Layout

```text
.dev/coordinators/
├── README.md                                   # how this tree works; changed only by a PR to master
├── claims/                                     # one create-once file per claimed item, project-wide
│   ├── issue-450.md                            # body: coordinator id, stamp, revision read
│   ├── pr-539.md
│   └── item-orchestrator-mode-sw-07.md
├── epic-orchestrator-mode/
│   ├── scope.md                                # create-once by whoever opens the scope first
│   ├── ironbelly/                              # coordinator epic-orchestrator-mode/ironbelly
│   │   ├── coordinator.md                      # manifest: state, worktree path, branch, started
│   │   ├── ledger.md                           # single writer: this coordinator; append-only rows
│   │   ├── grants.md                           # single writer; append-only rows
│   │   ├── intake.md
│   │   ├── briefs/sw-07.md
│   │   └── results.md                          # append-only: item, worker contract path, revision
│   └── clayphi/                                # a second coordinator on the same epic, other items
│       └── ...
├── epic-issue-watcher/
│   └── clayphi/ ...
└── release-v5-1-0/
    ├── scope.md                                # lists member epics; release-only items
    └── ironbelly/ ...                          # the release coordinator
```

## Naming convention

| Thing | Grammar | Example | Limits |
|---|---|---|---|
| developer handle `<dev>` | GitHub login, lower-cased: `^[a-z0-9]+(-[a-z0-9]+)*$` | `ironbelly` | 1 to 39 characters (GitHub's published limit; not read in this repo) |
| scope folder | `<kind>-<scope>`, `<kind>` = `epic` or `release`, `<scope>` a slug, release version dots as hyphens | `epic-orchestrator-mode`, `release-v5-1-0` | scope slug 1 to 40 characters |
| coordinator id | `<kind>-<scope>/<dev>` (its folder path under `.dev/coordinators/`) | `epic-orchestrator-mode/ironbelly` | at most 88 characters |
| second coordinator by one developer on one scope | `<dev>-2`, `<dev>-3` | `ironbelly-2` | only when the first is still active |
| shared branch | literal `coordinators` on `origin` (the fork) | `coordinators` | one per project |
| worktree name (Orca `--name`) | `coord-<kind>-<scope>` (on one host the developer is implied) | `coord-epic-orchestrator-mode` | at most 54 characters |
| worktree branch | Orca's, observed `<orca-prefix>/<name>` | `ironbelly/coord-epic-orchestrator-mode` | set by Orca (UNVERIFIED rule) |
| claim file | `issue-<N>.md`, `pr-<N>.md` or `item-<scope>-<item-id>.md`, all lower-case | `item-orchestrator-mode-sw-07.md` | at most 100 characters |
| ledger row id | `<dev>-<YYYYMMDD-HHMMSS>` | `ironbelly-20261114-091812` | unique per writer |
| grant id | `<dev>-g<4 digits>` | `ironbelly-g0001` | the handle keeps two developers' grants apart |

**Collision rules.**
1. Scope folder and `scope.md`: whoever pushes `scope.md` first owns its wording; a second developer who meets an add/add conflict on `scope.md` drops their copy and keeps the pushed one.
2. Developer folder: one developer per folder; the handle is unique on GitHub, so two developers never share one.
3. Claim: one fixed path per item. Two coordinators who claim the same item both add the same path with different bodies; the second push meets an add/add conflict and loses the claim. The path is the lock; a claim counts only once pushed.
4. Worktree folder: read `orca worktree list` first; an existing name means `coord-<kind>-<scope>-2`.
5. Branch: `coordinators` must not be the start of another branch name followed by `/` (git cannot hold both `coordinators` and `coordinators/x`); Orca's `<orca-prefix>/` branches never clash with it.

## Concurrency

- **Single writer per developer folder.** Only the coordinator whose id is the folder writes in it. Its ledger, grants and results files are append-only: new rows at the end, never an edit of an old row (a correction is a new row naming the old one).
- **Shared files are create-once.** `scope.md` and every `claims/*.md` are written once and never edited; releasing a claim is deleting its file, done only by the coordinator named in it (or the project owner).
- **Double dispatch.** Before briefing a worker, the coordinator pushes a claim for the item (and for each issue or PR the item writes to). No pushed claim, no dispatch. Two coordinators on one epic split its items by claims.
- **Release and epic overlap.** A release coordinator claims only release-only items (for example the changelog or the tag); an epic item it needs to gate is read, not claimed.
- **What a merge looks like.** Each coordinator's worktree branch is based on `origin/coordinators`. To publish: `git pull --rebase origin coordinators`, then `git push origin HEAD:coordinators`. Writers touch disjoint folders and append at the end of their own files, so rebases are clean; the only conflicts possible are on `claims/*.md` or `scope.md`, and each one is the intended "someone got there first" signal.
- **Stale reads.** Each ledger row records the `origin/coordinators` revision read before acting; a coordinator re-fetches before every claim.

## Visibility

- `coordinators` is pushed to the fork (`origin` = `IronbellyOrg/IronClaude`) and stays unmerged in this version. Developer B reads A's state with `git fetch origin coordinators` and `git show origin/coordinators:.dev/coordinators/epic-orchestrator-mode/ironbelly/ledger.md`, or lists every coordinator with `git ls-tree -d origin/coordinators:.dev/coordinators/epic-orchestrator-mode`; no checkout and no worktree are needed.
- Claims must be pushed before dispatch, so the item-ownership view is never stale in a way that matters; ledger rows may lag by minutes.
- "Everything on epic X" is one folder; "everything developer Y runs" is `*/<dev>/` (one glob).
- Cost: routine commits and pushes by every coordinator, which today's rule forbids without the owner asking (XC-01: "committed only when the owner asks"); a standing grant is needed.

## Lifecycle

| State | Meaning | Who may move it there |
|---|---|---|
| created | `<scope>/<dev>/coordinator.md` pushed with `state: active` | the developer, after creating the worktree through Orca |
| active | the session is live and holds its claims | the developer's session |
| paused | a `paused` ledger row; claims kept; nothing new dispatched | the developer |
| closed | a `closed` ledger row; every claim it holds released (claim files deleted) or handed over by a ledger row naming the new coordinator | the developer, or the project owner |
| archived | `coordinator.md` gets `state: archived` (append a row); the folder stays where it is, so no path anyone cited breaks | the developer, after `closed` |
| deleted | folder removed from the branch; git history keeps it | the project owner only, with written approval |

A scope (the `<kind>-<scope>/` folder) is closed when every coordinator under it is closed; nobody edits `scope.md` to say so.

## Relation to existing rules

- **`.dev/tasks/` always staged.** Unchanged for workers' plan packages. The coordinator's ledger, grants and intake move from `.dev/tasks/<program-package>/` to `.dev/coordinators/<kind>-<scope>/<dev>/`. `.dev/coordinators/` needs its own rule: always staged in a coordinator worktree, committed and pushed by the coordinator to `origin coordinators` only, under a standing grant.
- **`.claude/` never staged.** Unchanged.
- **Orca-only worktrees with `--agent`.** The developer runs `orca worktree create --name coord-<kind>-<scope> --base-branch origin/coordinators --agent claude --prompt "<coordinator brief>"`; whether Orca accepts that base branch is UNVERIFIED (the project's examples use `origin/master`). The coordinator never creates its own worktree.
- **Fork-only PRs.** `coordinators` goes only to `origin`; no PR in this version; later PRs only through `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude`.
- **Grant rows for outward writes.** Each coordinator's `grants.md` holds only grants for that coordinator; a grant id carries the developer handle; a coordinator never acts on a grant outside its own folder. A new action (the coordinator's own push to `coordinators`) is added to the 6.8 action list.

## Cost and risk

- Two or more developers can coordinate one epic at once, which matches "multiple developers with multiple coordinators" on one project.
- Item collisions are caught by git itself (add/add conflict on one path), at the cost of a push before every dispatch.
- Create-once shared files (`scope.md`, claims) are a small new discipline; an agent that edits a claim instead of creating one breaks the lock.
- Append-only single files (`ledger.md`) are simpler to read than one-file-per-entry, but a careless whole-file rewrite by the writer could drop rows (single writer, so no other developer is hurt).
- One shared branch receives every coordinator's pushes; simultaneous pushes need a fetch, rebase and retry.

## What stays unresolved

- Whether Orca can base a worktree on `origin/coordinators`, and how its branch prefix is chosen (UNVERIFIED).
- Whether two developers ever share one host (then worktree names would need the handle too); assumed not (UNVERIFIED).
- Who is "the project owner" for delete and forced claim release.
- Whether each developer writes grants for their own coordinator or only the project owner does.
- How a claim is reclaimed from a coordinator whose developer has left.
