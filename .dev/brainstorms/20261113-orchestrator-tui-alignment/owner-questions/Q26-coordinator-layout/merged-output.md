<!-- Provenance: produced by /sc:adversarial; base Variant 2 (proposal B); merge date 2026-11-14 -->
# Merged layout: shared coordinators branch, scope folders with developer sub-folders, claim and decision files as locks

<!-- Source: Base (original, modified): changes 4 and 13 (ad hoc kind; scope-wide decision files) -->
**In one sentence.** One shared `coordinators` branch per project; under `.dev/coordinators/` the first level is the scope (an epic, a release or ad hoc work), the second level is the developer, so one coordinator is the pair (scope, developer) and owns exactly one folder; several developers may coordinate one epic at once, a top-level `claims/` folder of create-once files stops two coordinators dispatching the same item, and a `decisions/` folder of create-once files in each scope stops two coordinators recording contradictory scope-wide decisions.

<!-- Source: Base (original, modified): changes 4 and 13 (ad hoc scope and decision file terms added) -->
**Terms.** A *coordinator* is a person-opened Claude session that keeps a decision ledger, a grant table (the outward actions an approver has allowed, one grant each), an intake record, worker briefs and result paths, and starts workers through Orca (the local agent-orchestration app). An *epic* is a body of work spanning several issues (for example issue #339 "orchestrator mode"). A *release* is a shipped version (for example `v5.1.0`; the project's version is 5.0.0 in `pyproject.toml`). An *ad hoc* scope is triage or one-off coordination that belongs to no epic or release. A *developer handle* is the developer's GitHub login, lower-cased. A *claim* is a file whose existence says "this coordinator owns this item". A *decision file* is a file whose existence records one decision that binds a whole scope.

<!-- Source: Base (original, modified): change 15 (second bullet corrected) -->
**Facts this proposal rests on (read 2026-11-14).**
- `gh api user --jq .login` prints `ironbelly` on this host; `git config user.name` prints `coder`, the Coder workspace default, so `user.name` is not an identity and is never used in a name. Commit authors in the last 200 commits include `Ironbelly`, `Ryan wiancko`, `clayphi` and `coder`.
- `git worktree list` shows Orca-created worktrees at `/home/coder/workspaces/worktrees/IronClaude/<name>`, usually on branch `ironbelly/<name>`. The `<prefix>/<name>` branch shape is a habit with exceptions: `brainstorm-reflect-panel` is on `ironbelly/shadow-runs` and `issue-409-mvp` is on `409-Phase2`. Where the `ironbelly/` prefix comes from is UNVERIFIED; this proposal calls it `<orca-prefix>`, and no lock depends on it.
- One worktree never holds two live agents (merged spec 6.2, `merged-requirements.md:951`). So each coordinator session needs one worktree of its own.
- The slug grammar `^[a-z0-9]+(-[a-z0-9]+)*$` is already used by `/sc:issue` (`src/superclaude/skills/sc-issue-protocol/refs/create.md:15`); UTC stamps `YYYYMMDD-HHMMSS` are already used by `.dev/tasks/to-do/TASK-WF-*` and `.dev/sweeps/<stamp>-sweep.md`.
- `.dev/coordinators/` does not exist today (checked with `ls`); no `.gitignore` rule names it.

## Layout

<!-- Source: Base (original, modified): change 1 (grants/ folder), change 3 (-N folder), change 4 (adhoc scope), change 13 (decisions/ folder) -->
```text
.dev/coordinators/
├── README.md                                   # how this tree works; changed only by a PR to master
├── claims/                                     # one create-once file per claimed item, project-wide
│   ├── issue-450.md                            # body: coordinator id, stamp, revision read
│   ├── pr-539.md
│   └── item-orchestrator-mode-sw-07.md
├── epic-orchestrator-mode/
│   ├── scope.md                                # create-once by whoever opens the scope first
│   ├── decisions/                              # create-once: one file per decision that binds the scope
│   │   └── q26.md                              # body: coordinator id, stamp, revision read, the decision
│   ├── ironbelly/                              # coordinator epic-orchestrator-mode/ironbelly
│   │   ├── coordinator.md                      # manifest: handle, state, worktree path, branch, started
│   │   ├── ledger.md                           # single writer: this coordinator; append-only rows
│   │   ├── grants/                             # single writer; one immutable file per grant
│   │   │   └── 20261114-093000-g0001.md
│   │   ├── intake.md
│   │   ├── briefs/sw-07.md
│   │   └── results.md                          # append-only: item, worker contract path, revision
│   ├── ironbelly--2/                           # the same developer's second coordinator on this scope
│   │   └── ...
│   └── clayphi/                                # a second developer's coordinator on the same epic, other items
│       └── ...
├── epic-issue-watcher/
│   └── clayphi/ ...
├── adhoc-pr-539-triage/                        # ad hoc scope: triage or one-off coordination
│   └── ironbelly/ ...
└── release-v5-1-0/
    ├── scope.md                                # lists member epics; release-only items
    └── ironbelly/ ...                          # the release coordinator
```

## Naming convention

<!-- Source: Base (original, modified): changes 1, 2, 3, 4, 8, 9, 13, 15 (table rows); change 8 (identity paragraph) -->
| Thing | Grammar | Example | Limits |
|---|---|---|---|
| developer handle `<dev>` | GitHub login, lower-cased: `^[a-z0-9]+(-[a-z0-9]+)*$`; read once from `gh` and frozen in `coordinator.md` (see Identity below) | `ironbelly` | 1 to 39 characters (GitHub's published limit; not read in this repo) |
| scope folder | `<kind>-<scope>`, `<kind>` = `epic`, `release` or `adhoc`, `<scope>` a slug, release version dots as hyphens | `epic-orchestrator-mode`, `release-v5-1-0`, `adhoc-pr-539-triage` | scope slug 1 to 40 characters |
| coordinator id | `<kind>-<scope>/<dev>` or `<kind>-<scope>/<dev>--<N>` (its folder path under `.dev/coordinators/`) | `epic-orchestrator-mode/ironbelly` | at most 88 characters, plus the `--<N>` suffix |
| second and later coordinator by one developer on one scope | `<dev>--<N>` (two hyphens), where `<N>` is the next unused integer, starting at 2 | `ironbelly--2` | a number is never reused; the rule does not depend on whether an earlier coordinator is still active; two hyphens because a single hyphen is legal inside a GitHub login (`ironbelly-2` could be another person), while GitHub's published rule allows no double hyphen (not read in this repo) |
| shared branch | literal `coordinators` on `origin` (the fork) | `coordinators` | one per project |
| worktree name (Orca `--name`) | `coord-<dev>-<kind>-<scope>` | `coord-ironbelly-epic-orchestrator-mode` | at most 94 characters |
| worktree branch | Orca's, usually `<orca-prefix>/<name>` | `ironbelly/coord-ironbelly-epic-orchestrator-mode` | set by Orca (UNVERIFIED rule; a habit with exceptions, and no lock depends on it) |
| claim file | `issue-<N>.md`, `pr-<N>.md` or `item-<scope>-<item-id>.md`, all lower-case | `item-orchestrator-mode-sw-07.md` | at most 100 characters |
| decision file | `<kind>-<scope>/decisions/<key>.md`, `<key>` a slug | `epic-orchestrator-mode/decisions/q26.md` | create-once; no length limit set here |
| ledger row id | `<YYYYMMDD-HHMMSS>` (UTC); a second row in the same second adds `-2`, `-3` | `20261114-091812` | unique within one coordinator |
| grant id | `<YYYYMMDD-HHMMSS>-g<4 digits>`, the stem of its file under `grants/`, `g` counted per coordinator; a same-second clash adds `-2`, `-3` | `20261114-093000-g0001` | unique within one coordinator |
| qualified id (how a row or grant is cited project-wide) | `<coordinator-id>/<row id or grant id>` | `epic-orchestrator-mode/ironbelly/20261114-093000-g0001` | the coordinator id makes it unique project-wide; no id repeats |

<!-- Source: Variant 1 assumption A-001 via refactor-plan change 8 -->
**Identity.** The handle comes from `gh api user --jq .login`, lower-cased, read once when the coordinator is created and frozen in its `coordinator.md`. A session without an authenticated `gh` gets no folder and makes no claim. `git config user.name` is never used: commit author names identify nobody (`coder` is the shared default).

<!-- Source: Base (original, modified): change 14 (rule 1), change 5 (rule 3), change 13 (rule 4 added), change 9 (rule 5) -->
**Collision rules.**
1. Scope folder and `scope.md`: whoever pushes `scope.md` first owns its wording. A second developer whose push is refused keeps the pushed `scope.md`, drops their own copy, and writes a ledger row in their own folder saying what they would change, so the loss is recorded, not silent. Any change to `scope.md` after creation needs the project owner.
2. Developer folder: one developer per folder; the handle is unique on GitHub, so two developers never share one.
3. Claim: one fixed path per item. Two coordinators who claim the same item both add the same path with different bodies; the second push is refused and that coordinator loses the claim. The path is the lock; a claim counts only once pushed. The steps are in "Claim procedure" under Concurrency.
4. Decision file: one fixed path per decision key in a scope, with the same lock and the same procedure as a claim.
5. Worktree folder: read `orca worktree list` first; an existing name means `coord-<dev>-<kind>-<scope>-2`.
6. Branch: `coordinators` must not be the start of another branch name followed by `/` (git cannot hold both `coordinators` and `coordinators/x`); Orca's `<orca-prefix>/` branches never clash with it.

## Concurrency

<!-- Source: Base (original, modified): change 1 (grant files) -->
- **Single writer per developer folder.** Only the coordinator whose id is the folder writes in it. Its ledger and results files are append-only: new rows at the end, never an edit of an old row (a correction is a new row naming the old one). Each grant is its own file under `grants/`, created once and never edited, so a changed grant shows as a modified file; a correction to a grant is a new grant file naming the old one. The ledger stays one file because it is the owner's reading surface; it has one writer, and git history recovers a careless whole-file rewrite.
<!-- Source: Base (original, modified): change 13 (decision files added to the create-once set) -->
- **Shared files are create-once.** `scope.md`, every `claims/*.md` and every `<kind>-<scope>/decisions/*.md` are written once and never edited; releasing a claim is deleting its file, done only by the coordinator named in it (or the project owner).
<!-- Source: Base (original, modified): change 5 (refers to the claim procedure) -->
- **Double dispatch.** Before briefing a worker, the coordinator claims the item (and each issue or PR the item writes to) by the claim procedure below. No pushed claim, no dispatch. Two coordinators on one epic split its items by claims.
<!-- Source: Variant 1, strength 1 (one decision authority per scope), refactor-plan change 13 -->
- **Scope-wide decisions.** Any decision that binds the whole scope (an owner answer, an epic design choice) lives in a create-once file `<kind>-<scope>/decisions/<key>.md`, taken with the same lock and procedure as a claim, and ledger rows cite it. Decisions that bind only one coordinator stay ledger rows. This stops two coordinators on one epic from recording contradictory scope-wide decisions.
<!-- Source: Base (original) -->
- **Release and epic overlap.** A release coordinator claims only release-only items (for example the changelog or the tag); an epic item it needs to gate is read, not claimed.
<!-- Source: Base (original, modified): change 13 (decisions/ added to the possible conflicts) -->
- **What a merge looks like.** Each coordinator's worktree branch is based on `origin/coordinators` (see Relation to existing rules for the fallback when Orca refuses that base). To publish: `git pull --rebase origin coordinators`, then `git push origin HEAD:coordinators`. Writers touch disjoint folders, append at the end of their own files and create new grant files, so rebases are clean; the only conflicts possible are on `claims/*.md`, `decisions/*.md` or `scope.md`, and each one is the intended "someone got there first" signal.
<!-- Source: Diff assumption A-003 (all advocates), refactor-plan change 6 -->
- **Never force-push or rewrite `coordinators`.** Nobody force-pushes the branch or rewrites its history; after a force push the claim lock means nothing. Branch protection for `coordinators` on the fork is an owner decision (UNVERIFIED that the fork's plan supports it).
<!-- Source: Base (original) -->
- **Stale reads.** Each ledger row records the `origin/coordinators` revision read before acting; a coordinator re-fetches before every claim.

### Claim procedure

<!-- Source: V2 advocate concession 1 and V3 advocate weakness 3 (debate transcript), refactor-plan change 5 -->
The same steps take a claim, a decision file or a new `scope.md`.

1. Fetch `origin/coordinators` and start from it, with no other unpushed commit in the worktree.
2. Create the file. Its body always holds the coordinator id, a stamp and the revision read, so two bodies are never byte-identical (identical bodies would merge without a conflict and hide the loss).
3. Commit the file on its own and push at once with `git push origin HEAD:coordinators`.
4. If the push is refused, fetch. If the path now exists on `origin/coordinators`, the claim is lost: drop the local claim commit and pick other work. If the path does not exist there, rebase onto `origin/coordinators` and push again.
5. Nobody ever resolves a conflict under `claims/`, under `decisions/` or on `scope.md` by keeping their own side.

### Reading current code and documents

<!-- Source: Diff assumption A-004 (two REJECT, one QUALIFY), refactor-plan change 7 -->
A coordinator worktree holds only its branch base plus `.dev/coordinators/`, so code and program documents committed to master after that base, and documents on other unmerged branches, are not in its checkout. The coordinator never assumes its checkout is current. It reads code and program documents with `git show origin/master:<path>` (or the same command on the branch that owns the document), records in the ledger row the revision it read, and never rebases `coordinators` onto master.

## Visibility

<!-- Source: Base (original) -->
- `coordinators` is pushed to the fork (`origin` = `IronbellyOrg/IronClaude`) and stays unmerged in this version. Developer B reads A's state with `git fetch origin coordinators` and `git show origin/coordinators:.dev/coordinators/epic-orchestrator-mode/ironbelly/ledger.md`, or lists every coordinator with `git ls-tree -d origin/coordinators:.dev/coordinators/epic-orchestrator-mode`; no checkout and no worktree are needed.
- Claims must be pushed before dispatch, so the item-ownership view is never stale in a way that matters; ledger rows may lag by minutes.
<!-- Source: Base (original, modified): change 3 (-N folders) -->
- "Everything on epic X" is one folder; "everything developer Y runs" is `*/<dev>/` plus `*/<dev>--*/`.
<!-- Source: Variant 3, Visibility (A-006 reconciled with C-003), refactor-plan change 10 -->
- **Unpushed coordinators.** A coordinator may stay unpushed (private work), but an unpushed coordinator cannot claim, so it cannot dispatch.
<!-- Source: Base (original) -->
- Cost: routine commits and pushes by every coordinator, which today's rule forbids without the owner asking (XC-01: "committed only when the owner asks"); a standing grant is needed.

## Lifecycle

<!-- Source: Base (original, modified): change 10 ("created" row allows an unpushed coordinator) -->
| State | Meaning | Who may move it there |
|---|---|---|
| created | `<scope>/<dev>/coordinator.md` committed with `state: active` and pushed (an unpushed coordinator is allowed but cannot claim; see Visibility) | the developer, after creating the worktree through Orca |
| active | the session is live and holds its claims | the developer's session |
| paused | a `paused` ledger row; claims kept; nothing new dispatched | the developer |
| closed | a `closed` ledger row; every claim it holds released (claim files deleted) or handed over by a ledger row naming the new coordinator | the developer, or the project owner |
| archived | `coordinator.md` gets `state: archived` (append a row); the folder stays where it is, so no path anyone cited breaks | the developer, after `closed` |
| deleted | folder removed from the branch; git history keeps it | the project owner only, with written approval |

<!-- Source: Base (original) -->
A scope (the `<kind>-<scope>/` folder) is closed when every coordinator under it is closed; nobody edits `scope.md` to say so.

## Relation to existing rules

<!-- Source: Base (original, modified): change 1 (grants/ folder) -->
- **`.dev/tasks/` always staged.** Unchanged for workers' plan packages. The coordinator's ledger, grants and intake move from `.dev/tasks/<program-package>/` to `.dev/coordinators/<kind>-<scope>/<dev>/`. `.dev/coordinators/` needs its own rule: always staged in a coordinator worktree, committed and pushed by the coordinator to `origin coordinators` only, under a standing grant.
<!-- Source: Base (original) -->
- **`.claude/` never staged.** Unchanged.
<!-- Source: Base (original, modified): change 9 (handle in the worktree name), change 15 (base branch fallback and branch prefix wording) -->
- **Orca-only worktrees with `--agent`.** The developer runs `orca worktree create --name coord-<dev>-<kind>-<scope> --base-branch origin/coordinators --agent claude --prompt "<coordinator brief>"`. Whether Orca accepts that base branch is UNVERIFIED (the project's examples use `origin/master`). If Orca refuses it, the developer creates the worktree from `origin/master` (as merged spec 6.2 says) and, inside the worktree, runs `git merge origin/coordinators` once and pushes that merge alone (`git push origin HEAD:coordinators`, a fast-forward) before writing anything else; that bootstrap push is the only push exempt from the path check below, and it is recorded as the coordinator's first ledger row. It moves `coordinators` forward to the newer master; that is harmless, because `coordinators` already carries master's tree as of its base and the coordinator reads code and documents through `git show origin/master:<path>`, never from its checkout (see "Reading current code and documents"). The worktree's branch name is whatever Orca gives; the `<prefix>/<name>` shape is a habit with exceptions, and no lock depends on it. The coordinator never creates its own worktree.
<!-- Source: Diff assumption A-003 (all advocates), refactor-plan change 6 -->
- **No force push.** `coordinators` is never force-pushed or rewritten (see Concurrency).
<!-- Source: Base (original) -->
- **Fork-only PRs.** `coordinators` goes only to `origin`; no PR in this version; later PRs only through `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude`.
<!-- Source: Base (original, modified): changes 1 and 2 (grant files, coordinator-qualified grant ids) -->
- **Grant rows for outward writes.** Each coordinator's `grants/` folder holds only grants for that coordinator, one file each; a grant is cited project-wide by its qualified id (`<coordinator-id>/<grant id>`); a coordinator never acts on a grant outside its own folder. A new action (the coordinator's own push to `coordinators`) is added to the 6.8 action list.
<!-- Source: Variant 3, C-008 (adapted to one branch), refactor-plan change 11 -->
- **Path-narrowed push grant.** The standing grant covers `git push origin HEAD:coordinators` only, and only commits whose paths are the coordinator's own folder, `claims/` files naming it, `decisions/` files naming it, or a new `scope.md`. Before each push the coordinator lists `git diff --name-only origin/coordinators..HEAD` and stops on any other path. The one exception is the fallback bootstrap merge (Orca-only worktrees bullet above): it is pushed alone, first, before any other write, and recorded as a ledger row. This check is procedural; no hook exists for it.
<!-- Source: Orchestrator post-merge fix N1 (decisions/ was missing from the path list) and N2 (bootstrap exception), see merge-log.md -->

<!-- Source: Diff assumption A-006 and V3 advocate concession 7, refactor-plan change 12 -->
- **Content of pushed files.** Nothing under `.dev/coordinators/` holds tokens, secrets, or host or contact details; captures are sanitized before commit. The fork is private, but grants quote owner wording.

## Cost and risk

<!-- Source: Base (original) -->
- Two or more developers can coordinate one epic at once, which matches "multiple developers with multiple coordinators" on one project.
- Item collisions are caught by git itself (add/add conflict on one path), at the cost of a push before every dispatch.
<!-- Source: Base (original, modified): changes 5 and 13 (decision files; written conflict rule) -->
- Create-once shared files (`scope.md`, claims, decision files) are a small new discipline; an agent that edits a claim instead of creating one, or keeps its own side of a conflict, breaks the lock. The claim procedure writes this down.
<!-- Source: Refactor-plan risk summary, change 13 -->
- Too many decisions could be forced into create-once decision files; only decisions that bind the whole scope go there, and the rest stay ledger rows.
<!-- Source: Base (original, modified): change 1 (grants are one file each; ledger stays one file) -->
- The append-only `ledger.md` is simpler to read than one file per entry, but a careless whole-file rewrite by the writer could drop rows (single writer, so no other developer is hurt, and git history recovers them). Grants avoid that risk: each is its own immutable file.
<!-- Source: Base (original) -->
- One shared branch receives every coordinator's pushes; simultaneous pushes need a fetch, rebase and retry.
<!-- Source: Refactor-plan risk summary, change 6 -->
- A force push would remove claims; the rule forbids it, and the branch can be restored from any coordinator's local copy of `origin/coordinators`.

## What stays unresolved

<!-- Source: Base (original, modified): change 15 (first bullet), change 9 (second bullet), change 6 (branch protection bullet added) -->
- Whether Orca can base a worktree on `origin/coordinators` (the fallback is `origin/master` plus one merge), and how its branch prefix is chosen (UNVERIFIED; no lock depends on the prefix).
- Whether two developers ever share one host (UNVERIFIED); worktree names now carry the handle, so a shared host no longer causes a name clash.
- Whether the fork's plan supports branch protection for `coordinators` (UNVERIFIED), and whether the owner turns it on.
<!-- Source: Base (original) -->
- Who is "the project owner" for delete and forced claim release.
- Whether each developer writes grants for their own coordinator or only the project owner does.
- How a claim is reclaimed from a coordinator whose developer has left.
