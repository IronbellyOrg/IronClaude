# Proposal C: developer folders on developer branches, nothing shared to write

**In one sentence.** The unit of ownership is the developer: each developer has their own coordinators branch and their own folder `.dev/coordinators/<dev>/`, holding one sub-folder per coordinator (an epic, a release, or ad hoc work); no developer ever writes a file or a branch another developer writes, and others see it only by fetching it read-only.

**Terms.** A *coordinator* is a person-opened Claude session that keeps a decision ledger, a grant table (the outward actions an approver has allowed, one row each), an intake record, worker briefs and result paths, and starts workers through Orca (the local agent-orchestration app). An *epic* is a body of work spanning several issues (for example issue #339 "orchestrator mode"). A *release* is a shipped version (for example `v5.1.0`; the project's version is 5.0.0 in `pyproject.toml`). A *developer handle* is the developer's GitHub login, lower-cased.

**Facts this proposal rests on (read 2026-11-14).**
- `gh api user --jq .login` prints `ironbelly` on this host; `git config user.name` prints `coder`, the Coder workspace default, so `user.name` is not an identity and is never used in a name. Commit authors in the last 200 commits include `Ironbelly`, `Ryan wiancko`, `clayphi` and `coder`.
- `git worktree list` shows Orca-created worktrees at `/home/coder/workspaces/worktrees/IronClaude/<name>` on branch `ironbelly/<name>`; the remote also has hand-made developer-prefixed branches such as `origin/clayphi/433-ccsession-orca-resume`. Where Orca's `ironbelly/` prefix comes from is UNVERIFIED; this proposal calls it `<orca-prefix>` and expects it to equal the handle.
- One worktree never holds two live agents (merged spec 6.2, `merged-requirements.md:951`). So each coordinator session needs one worktree of its own.
- The slug grammar `^[a-z0-9]+(-[a-z0-9]+)*$` is already used by `/sc:issue` (`src/superclaude/skills/sc-issue-protocol/refs/create.md:15`); UTC stamps `YYYYMMDD-HHMMSS` are already used by `.dev/tasks/to-do/TASK-WF-*` and `.dev/sweeps/<stamp>-sweep.md`.
- `.dev/coordinators/` does not exist today (checked with `ls`); no `.gitignore` rule names it.

## Layout

```text
# on branch <dev>/coordinators (one per developer), e.g. ironbelly/coordinators
.dev/coordinators/
└── ironbelly/                                  # only this developer's folder exists on this branch
    ├── profile.md                              # handle, hosts, how to reach them
    ├── epic-orchestrator-mode/                 # one coordinator
    │   ├── coordinator.md                      # manifest: kind, scope, state, worktree, branch
    │   ├── ledger.md                           # the decision ledger (6.8 format); single writer
    │   ├── grants.md                           # the grant table; single writer
    │   ├── intake.md
    │   ├── claims.md                           # items this coordinator says it owns (advisory)
    │   ├── briefs/sw-07.md
    │   └── results.md
    ├── epic-issue-watcher/
    └── release-v5-1-0/

# on branch clayphi/coordinators
.dev/coordinators/
└── clayphi/
    └── epic-orchestrator-mode/                 # same epic, different developer: no clash, different branch and folder
```

Each coordinator also runs in its own Orca worktree (one live agent per worktree), on a branch based on the developer's `<dev>/coordinators`; it merges its commits back into `<dev>/coordinators` (the developer's coordinators never touch each other's sub-folders, so these merges are clean).

## Naming convention

| Thing | Grammar | Example | Limits |
|---|---|---|---|
| developer handle `<dev>` | GitHub login, lower-cased: `^[a-z0-9]+(-[a-z0-9]+)*$` | `clayphi` | 1 to 39 characters (GitHub's published limit; not read in this repo) |
| developer branch | `<dev>/coordinators` | `ironbelly/coordinators` | one per developer per project |
| coordinator folder | `<kind>-<scope>` with `<kind>` = `epic`, `release` or `adhoc` | `release-v5-1-0`, `adhoc-pr-539-triage` | scope slug 1 to 40 characters |
| coordinator id | `<dev>:<kind>-<scope>` | `ironbelly:epic-orchestrator-mode` | at most 90 characters |
| worktree name (Orca `--name`) | `coord-<kind>-<scope>` | `coord-epic-orchestrator-mode` | at most 54 characters |
| worktree branch | Orca's, observed `<orca-prefix>/<name>` | `ironbelly/coord-epic-orchestrator-mode` | set by Orca (UNVERIFIED) |
| ledger row id / grant id | `<YYYYMMDD-HHMMSS>` / `g<4 digits>`, unique within one coordinator | `g0003` | the coordinator id qualifies them project-wide |

**Collision rules.**
1. Branch: `<dev>/coordinators` cannot clash between developers because handles are unique; inside one developer's namespace, `coordinators` is a leaf, so no other branch may be named `<dev>/coordinators/...` (git cannot hold both).
2. Folder: a developer's branch carries only `.dev/coordinators/<dev>/`; a commit touching another developer's folder is refused by review (no hook exists for this today).
3. Coordinator folder: unique within the developer; a second coordinator on the same scope by the same developer gets `-2`.
4. Worktree folder: read `orca worktree list` first; an existing name means add `-2`.

## Concurrency

- **Nothing shared is ever written.** Each developer branch and folder has one human owner; each coordinator sub-folder has one session writer. Two developers never edit the same file and never push the same branch.
- **Append-only files.** `ledger.md`, `grants.md`, `results.md` and `claims.md` take new rows at the end only.
- **Double dispatch is not prevented by structure.** Before dispatching an item, a coordinator runs `git fetch origin` and reads `claims.md` on every `origin/*/coordinators` branch; if another coordinator lists the item, it asks its developer. Between the fetch and the other side's push there is a window in which both can claim one item; the check is advisory.
- **What a merge looks like.** Developer branches are never merged into each other. A developer's coordinators merge into that developer's `<dev>/coordinators`; each writes a different sub-folder, so merges are clean. If the owner later wants one combined view, merging all `<dev>/coordinators` branches is also clean, because the folders are disjoint.
- **Stale reads.** Each ledger row that relied on another developer's state records which `origin/<dev>/coordinators` revision it read.

## Visibility

- Each developer pushes `<dev>/coordinators` to the fork (`origin`). Developer B reads A's state with `git fetch origin` and `git show origin/ironbelly/coordinators:.dev/coordinators/ironbelly/epic-orchestrator-mode/ledger.md`; no checkout is needed. Reading is always read-only, because B never has a reason to write A's branch.
- A developer who never pushes is invisible. That is allowed: a private coordinator is a valid choice, at the price that nobody else can see its claims.
- "Everything on epic X" needs a scan across every developer branch (`git for-each-ref refs/remotes/origin/*/coordinators` then `git ls-tree` each); "everything developer Y runs" is one branch.
- Cost: a push grant per developer for their own branch only, narrower than a shared-branch grant.

## Lifecycle

| State | Meaning | Who may move it there |
|---|---|---|
| created | `<dev>/<kind>-<scope>/coordinator.md` committed with `state: active` | the developer, after creating the worktree through Orca |
| active | the session runs | the developer's session |
| paused | a `paused` ledger row | the developer |
| closed | a `closed` ledger row; its `claims.md` gets a final row "released" | the developer |
| archived | `state: archived` row; the folder stays | the developer |
| deleted | folder removed from the developer's own branch, or the whole branch deleted | the developer for their own branch; the project owner for a departed developer's branch |

## Relation to existing rules

- **`.dev/tasks/` always staged.** Unchanged for workers' plan packages. The coordinator's ledger moves from `.dev/tasks/<program-package>/` into `.dev/coordinators/<dev>/<kind>-<scope>/`. `.dev/coordinators/` needs its own rule: always staged in a coordinator worktree; committed and pushed only to the developer's own `<dev>/coordinators` branch, under a grant the developer gives.
- **`.claude/` never staged.** Unchanged.
- **Orca-only worktrees with `--agent`.** The developer runs `orca worktree create --name coord-<kind>-<scope> --base-branch origin/<dev>/coordinators --agent claude --prompt "<coordinator brief>"`; whether Orca accepts that base is UNVERIFIED.
- **Fork-only PRs.** Developer branches go only to `origin`; no PR in this version.
- **Grant rows for outward writes.** A grant lives in the coordinator's own `grants.md` on the developer's own branch, so a grant cannot be read as another developer's: the path names the developer. Whether a developer may grant their own coordinator's outward writes, or the project owner must, is unresolved.

## Cost and risk

- Strongest isolation and simplest permissions: every developer writes only their own branch.
- Matches the existing habit of developer-prefixed branches (`ironbelly/...`, `clayphi/...`).
- Weakest protection against two coordinators doing the same item: the check is advisory and racy, and it depends on everyone pushing.
- The owner asked for "a Coordinator branch" per project; this gives one per developer, which departs from that wording.
- A per-epic or per-release view across developers needs tooling that scans many branches.

## What stays unresolved

- Whether the owner accepts one branch per developer instead of one per project.
- Whether Orca can base a worktree on `origin/<dev>/coordinators`, and whether its prefix equals the handle (UNVERIFIED).
- How the project-wide release view is built and who keeps it.
- Who grants outward writes for each developer's coordinators.
