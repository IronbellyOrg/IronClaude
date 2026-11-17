# Proposal A: scope folders with one active coordinator per scope (a lease)

**In one sentence.** The unit of ownership is the scope (an epic or a release), not the person: each scope has one folder, one ledger and at most one live coordinator at a time, and a developer holds the scope through a lease file that git itself turns into a lock; all scopes live on one shared `coordinators` branch.

**Terms.** A *coordinator* is a person-opened Claude session that keeps a decision ledger, a grant table (the outward actions an approver has allowed, one row each), an intake record, worker briefs and result paths, and starts workers through Orca (the local agent-orchestration app). An *epic* is a body of work spanning several issues (for example issue #339 "orchestrator mode"). A *release* is a shipped version (for example `v5.1.0`; the project's version is 5.0.0 in `pyproject.toml`). A *developer handle* is the developer's GitHub login, lower-cased.

**Facts this proposal rests on (read 2026-11-14).**
- `gh api user --jq .login` prints `ironbelly` on this host; `git config user.name` prints `coder`, the Coder workspace default, so `user.name` is not an identity and is never used in a name. Commit authors in the last 200 commits include `Ironbelly`, `Ryan wiancko`, `clayphi` and `coder`.
- `git worktree list` shows Orca-created worktrees at `/home/coder/workspaces/worktrees/IronClaude/<name>` on branch `ironbelly/<name>` (for example `issue-339-orchestrator-mode` on `ironbelly/issue-339-orchestrator-mode`). Where the `ironbelly/` prefix comes from (an Orca setting or the login) is UNVERIFIED; this proposal calls it `<orca-prefix>`.
- One worktree never holds two live agents (merged spec 6.2, `merged-requirements.md:951`). So one coordinator session needs one worktree of its own.
- The slug grammar `^[a-z0-9]+(-[a-z0-9]+)*$` is already used by `/sc:issue` (`src/superclaude/skills/sc-issue-protocol/refs/create.md:15`); UTC stamps `YYYYMMDD-HHMMSS` are already used by `.dev/tasks/to-do/TASK-WF-*` and `.dev/sweeps/<stamp>-sweep.md`.
- `.dev/coordinators/` does not exist today (checked with `ls`); no `.gitignore` rule names it.

## Layout

```text
.dev/coordinators/
├── README.md                                   # how this tree works; changed only by a PR to master
├── epic-orchestrator-mode/                     # one folder per scope, named <kind>-<scope-slug>
│   ├── scope.md                                # create-once: kind, slug, title, issues, release, created-by, created-at
│   ├── holder.md                               # THE lease: one fixed path; who holds the scope now
│   ├── holders/                                # history: one file per finished lease
│   │   └── 20261114-091500-ironbelly.md
│   ├── ledger/                                 # one file per decision entry, never edited after creation
│   │   ├── 20261114-091812-ironbelly-q26.md
│   │   └── 20261114-101030-clayphi-q1.md
│   ├── grants/                                 # one file per grant row, never edited after creation
│   │   └── 20261114-093000-ironbelly-g0001.md
│   ├── intake/20261114-091500-ironbelly.md     # one intake record per lease
│   ├── briefs/sw-07/20261114-110000-ironbelly.md
│   └── results/sw-07/20261114-140000-ironbelly.md   # pointer: worker contract path, worktree, revision
├── epic-issue-watcher/
│   └── ...
└── release-v5-1-0/                             # a release is a scope of its own
    ├── scope.md                                # lists member epics by folder name; never their items
    ├── holder.md
    ├── ledger/ grants/ intake/ briefs/ results/
```

The ledger the owner reads is not a file: it is the sorted list of `ledger/*.md` (a reader script or `ls` makes the table). No file in a scope is a running summary that two writers could both edit.

## Naming convention

| Thing | Grammar | Example | Limits |
|---|---|---|---|
| developer handle `<dev>` | GitHub login, lower-cased: `^[a-z0-9]+(-[a-z0-9]+)*$` | `ironbelly`, `clayphi` | 1 to 39 characters (GitHub's published limit; not read in this repo) |
| scope kind `<kind>` | `epic` or `release` | `epic` | fixed words |
| scope slug `<scope>` | `^[a-z0-9]+(-[a-z0-9]+)*$`; a release writes its version with dots as hyphens | `orchestrator-mode`, `v5-1-0` | 1 to 40 characters |
| scope folder | `<kind>-<scope>` | `epic-orchestrator-mode`, `release-v5-1-0` | at most 48 characters |
| shared branch | the literal `coordinators` on `origin` (the fork) | `coordinators` | one per project |
| worktree name (Orca `--name`) | `coord-<kind>-<scope>` | `coord-epic-orchestrator-mode` | at most 54 characters |
| worktree branch | whatever Orca gives, observed `<orca-prefix>/<name>` | `ironbelly/coord-epic-orchestrator-mode` | set by Orca (UNVERIFIED rule) |
| entry file | `<YYYYMMDD-HHMMSS>-<dev>-<tag>.md`, UTC, `<tag>` a slug | `20261114-091812-ironbelly-q26.md` | at most 120 characters |
| grant id | `g` plus 4 digits, counted per scope | `g0001` | the file name carries the stamp, so two holders never mint the same file even if both pick `g0001` |
| item folder | the item id lower-cased | `sw-07` | the scope's own ids |

**Collision rules.**
1. Scope folder: created only by a commit that adds `scope.md`; if `origin/coordinators` already has that folder, the creator picks a different slug (a scope is never shared by reuse of a name).
2. Lease: `holder.md` is one fixed path. Two developers who both try to take a free scope both add or change that one file; the second push meets a git conflict on it and loses. The path is the lock.
3. Entry files: the stamp plus the handle makes names unique across developers; two entries by one developer in the same second get `-2`, `-3` before `.md`.
4. Worktree folder: before `orca worktree create`, the developer reads `orca worktree list`; a name already present on the host means pick `coord-<kind>-<scope>-2`.
5. Branch: `coordinators` must not be a prefix of another branch name (git cannot hold both `coordinators` and `coordinators/x`, because a branch name is a file path inside `.git/refs`). Orca's branches start with `<orca-prefix>/`, so they never clash unless a prefix is literally `coordinators`.

## Concurrency

- **Single writer per scope.** Only the session named in `holder.md` writes inside that scope folder, and only by creating new files (ledger, grants, intake, briefs, results). It never edits an existing entry; a correction is a new entry that names the one it replaces.
- **Append by creation.** Every ledger and grant entry is a new file with a unique name, so two coordinators never edit the same file, and a rebase of one coordinator's commits onto another's never conflicts on content.
- **Lease handover.** The holder ends a lease by moving its record into `holders/` and emptying `holder.md` in one commit; the next developer writes their name into `holder.md` in a new commit. A forced takeover (holder gone) is the project owner's act only, recorded as a ledger entry.
- **Double dispatch.** Inside one scope it cannot happen: one holder. Across scopes, an item belongs to exactly one scope (listed in that scope's `scope.md`); a release scope lists epics, never their items, so a release coordinator never dispatches an epic's item.
- **What a merge looks like.** Every coordinator's worktree branch is based on `origin/coordinators`. To publish, the coordinator runs `git pull --rebase origin coordinators` then `git push origin HEAD:coordinators`. Because writers own disjoint folders and only create files, the rebase is clean; the only conflict that can happen is on a `holder.md`, and that conflict is the intended "someone else took this scope" signal.
- **Stale reads.** Every ledger entry records the `origin/coordinators` revision it read (`git rev-parse origin/coordinators`) before it acted.

- **A lease counts only once pushed.** A coordinator dispatches nothing until its `holder.md` commit is on `origin/coordinators`; a local, unpushed lease is not a lease.

## Visibility

- The branch `coordinators` is pushed to the fork (`origin` = `IronbellyOrg/IronClaude`), never merged to `master` in this version. Developer B sees developer A's scope with `git fetch origin coordinators` and `git show origin/coordinators:.dev/coordinators/epic-orchestrator-mode/holder.md` (or `git ls-tree`), with no checkout and no worktree.
- Visibility lags by the time between A's commit and A's push. Because the lease must be pushed before dispatch, the lag never hides who holds a scope; it can hide the newest ledger entries for minutes.
- Cost: every coordinator commits and pushes routinely, which today's rule forbids without the owner asking (the ledger "is committed only when the owner asks", `merged-requirements.md` XC-01). A standing owner grant for "commit and push under `.dev/coordinators/` to `origin coordinators` only" is needed (see Relation to existing rules).

## Lifecycle

| State | Meaning | Who may move it there |
|---|---|---|
| created | `scope.md` and the first `holder.md` committed and pushed | any developer, for a slug not yet on `origin/coordinators` |
| active | `holder.md` names a live session | the holder (by taking the lease) |
| paused | `holder.md` names a holder who wrote a `paused` ledger entry; nobody may dispatch | the holder |
| handed over | the old record moved to `holders/`, `holder.md` rewritten by the new holder | the old holder releases; the new holder takes; a forced takeover only by the project owner |
| closed | a `closed` ledger entry by the holder; `holder.md` emptied; nothing is dispatched again | the holder, or the project owner |
| archived | the scope folder moves to `.dev/coordinators/archive/<kind>-<scope>/` | the project owner only (a move rewrites every path others may cite) |
| deleted | the folder is removed from the branch; git history keeps it | the project owner only, with written approval |

## Relation to existing rules

- **`.dev/tasks/` always staged.** Untouched: workers' plan packages stay in their own worktrees under `.dev/tasks/`. The coordinator's ledger moves out of `.dev/tasks/<program-package>/` into its scope folder. `.dev/coordinators/` needs its own rule: always staged and, unlike `.dev/tasks/`, committed and pushed by the coordinator under a standing grant, because a shared lease that is not pushed does not exist.
- **`.claude/` never staged.** Untouched; nothing here lives under `.claude/`.
- **Orca-only worktrees with `--agent`.** Each coordinator worktree is created by the developer with `orca worktree create --name coord-<kind>-<scope> --base-branch origin/coordinators --agent claude --prompt "<coordinator brief>"`. Whether Orca accepts a non-master base branch here is UNVERIFIED (the project's own examples use `origin/master`).
- **Fork-only PRs.** The `coordinators` branch is pushed only to `origin` (the fork) and never opened as a PR in this version; any later PR uses `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`.
- **Grant rows for outward writes.** Grants stay one file per grant inside the scope; a grant names the approver's handle and is valid only for the scope folder it sits in. A new grant action is needed for the coordinator's own pushes to `coordinators` (today's actions in 6.8 do not include it).

## Cost and risk

- Lowest risk of two coordinators acting on one item: within a scope there is only ever one.
- Two developers cannot work one epic at the same time; a big epic either waits on handovers or is split into smaller epics (more scopes).
- The developer axis is only a field (`holder.md`, entry names), so "show me everything clayphi is coordinating" needs a scan of every `holder.md`.
- Handover needs discipline; a holder who disappears blocks the scope until the project owner forces a takeover.
- Every coordinator pushes to one shared branch: frequent small pushes, and a non-fast-forward retry loop when two push at once (clean rebases, but still a retry).

## What stays unresolved

- Whether Orca can base a worktree on `origin/coordinators` and how its branch prefix is chosen (UNVERIFIED).
- Who counts as "the project owner" for forced takeovers, archive and delete when several developers share the project.
- Whether each developer may write grants for their own lease, or only the project owner.
- Whether a release coordinator may hold an item that belongs to no epic (release-only items such as the changelog).
