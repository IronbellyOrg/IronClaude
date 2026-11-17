# Q26 follow-up final: how coordinators share one project

The owner's answer of 2026-11-14 settles where coordinators live: a Coordinator branch and worktree and a `.dev/coordinators/` directory in every project, unmerged for now, shared by several developers each running several coordinators. This file works out the layout and naming. It advises; it decides nothing.

**Terms used here.**
- *Coordinator*: a Claude session a person opens (or launches through Orca, see owner decision 1) that keeps the program's records and hands work to workers. It is work item XC-09 ("stand up the coordinator") in the merged spec `../../merged-requirements.md`.
- *Orca*: the local app that creates worktrees (separate checkouts of the repository) and starts agents in them.
- *Decision ledger*: the list of the owner's answers and open facts (work item XC-01, format in spec section 6.8).
- *Grant table*: the list of outward actions (push, PR, issue post) the owner has approved, one entry each (spec 6.8). In the spec an edge `GRANT(<item>,<action>)` is satisfied only by a matching entry.
- *Intake record*: the first checks a coordinator records before work starts (work item XC-10, "W0 intake").
- *Epic*: a body of work across several issues, for example issue #339 "orchestrator mode". *Release*: a shipped version, for example `v5.1.0` (a made-up example; the project is at 5.0.0 in `pyproject.toml`).
- *Handle*: a developer's GitHub login in lower case, for example `ironbelly`.
- *Claim*: a file whose existence says "this coordinator owns this item". *Decision file*: a file whose existence records one decision that binds a whole epic or release.
- *The fork*: `origin`, the repository `IronbellyOrg/IronClaude`, the only place anything is pushed.

## The problem in plain words

**What a coordinator keeps.** Its decision ledger, its grant table, its intake record, the briefs it writes for workers, and pointers to where each worker's results are. Today one coordinator would write all of this into one always-staged folder, `.dev/tasks/<program-package>/` (spec XC-01).

**Who writes and who reads.** The coordinator session writes. The owner writes the wording that becomes a grant and answers questions. Workers read their briefs. Other developers, other coordinators, and later sessions resuming the work read everything.

**What goes wrong when several developers run several coordinators on one project:**
1. *Same file edited twice.* Two coordinators append to one ledger file; one push overwrites or conflicts with the other.
2. *Merge conflicts.* Two branches of coordinator state that both touched shared files cannot be combined without someone choosing a side, and an agent may choose its own side.
3. *Two coordinators dispatch the same item.* Both brief a worker on the same issue or PR; two PRs, two issue edits, or two contradictory comments follow.
4. *Stale reads.* A coordinator acts on another developer's state as it was an hour ago.
5. *One developer's grant read as another's.* A grant written for developer A's coordinator is quoted by developer B's coordinator as permission.
6. *Branch and folder name clashes.* Two developers pick the same branch or worktree name; git also cannot hold both a branch `coordinators` and a branch `coordinators/x`.
7. *Unmerged state nobody can see.* State that lives only on one person's local branch is invisible to everyone else, including their claims on work.
8. *Identity.* On this host `git config user.name` is `coder`, a shared default, and the last 200 commits show one person under three author names (`Ironbelly`, `Ryan wiancko`, `coder`), so commit metadata cannot say which developer wrote what. `gh api user --jq .login` (`ironbelly` here) can.

## Can developer, epic and release be separated cleanly?

No, not as three independent folder levels, for three reasons:
1. **Developer is not a scope; it is an attribute of every coordinator.** A coordinator is opened by exactly one person, so every coordinator has one developer whatever its scope. Developer and scope are two independent dimensions, and a folder tree must pick an order. The debate picked scope first, developer second.
2. **Epic and release overlap.** A release contains epics, and an epic can slip to a later release. Nesting epics inside releases would force a folder move (and break every cited path) whenever an epic slips. Both also act on the same issues and PRs (for example a release coordinator and the #339 epic coordinator both care about PR #539). So epic and release are best kept as two sibling kinds of scope, linked by a list in the release's `scope.md`, with collisions stopped by item claims rather than by the folder tree.
3. **Some coordinator work is neither.** PR triage or one-off coordination belongs to no epic or release, so a third kind, `adhoc`, is needed.

## Debate result and confidence

Three layouts were debated (proposal files in this folder; letters assigned arbitrarily):
- Proposal A: one folder per epic or release, at most one live coordinator per scope through a lease file, one shared branch.
- Proposal B: one shared branch; scope folders with one sub-folder per developer; project-wide create-once claim files as locks.
- Proposal C: one branch and one folder per developer; nothing shared is ever written.

**Winner: proposal B as the base, with 15 changes taken from A, C and the advocates' concessions.** The three advocates (separate agents, one per proposal) agreed on all 22 debated points (18 unanimously, 4 by two of three): convergence 100 percent. All three advocates' overall positions named B as the base: A's advocate wrote that B "wins more points than mine", and C's advocate proposed "variant 2's scope-first reading surface and project-wide claim keys with variant 3's per-developer write isolation". Scoring put B first (0.874) ahead of A (0.843) and C (0.813); the B to A margin was inside the 5 percent band, so the tiebreaker (debate points won: B 8, A 1) decided.

Deciding evidence:
- Only B meets every part of the owner's answer: one branch per project, developers sharing one space, developer and scope sub-directories, several developers on one epic.
- Only B stops two coordinators dispatching the same issue, PR or item with a lock git enforces across the whole project. A's lease cannot see an epic and a release both writing to one PR; C's check is advisory and has a race window (C's own advocate conceded this).
- A contributed one immutable file per grant and a place for epic-wide decisions; C contributed the `adhoc` kind, a path-narrowed push grant, and the rule that a private coordinator may exist but cannot dispatch.

**Confidence: 70 percent.** Not higher because the debate ran at quick depth (one round, no invariant probe), the scores were close, the scoring and plan were done in one context, and two facts the layout leans on are UNVERIFIED: whether Orca accepts `--base-branch origin/coordinators` (a fallback is given) and whether the fork can protect the branch against force pushes.

## Recommended layout and naming convention

Full text with every rule: `merged-output.md` in this folder. The short form:

**One branch.** The literal branch `coordinators` on the fork, one per project, never merged to master in this version, never force-pushed or rewritten.

**One worktree per coordinator.** One worktree never holds two live agents (spec 6.2), so each coordinator gets its own Orca worktree, created by its developer with `--agent`, based on `origin/coordinators`. Every coordinator publishes with `git pull --rebase origin coordinators` then `git push origin HEAD:coordinators`.

**Folders.**

```text
.dev/coordinators/
├── README.md                       # how this tree works
├── claims/                         # project-wide; one create-once file per claimed issue, PR or item
├── <kind>-<scope>/                 # kind = epic | release | adhoc
│   ├── scope.md                    # create-once: title, issues, member epics (for a release)
│   ├── decisions/<key>.md          # create-once: one decision that binds the whole scope
│   └── <dev>/  (or <dev>--<N>/)    # one coordinator: the only writer in this folder
│       ├── coordinator.md          # handle (from gh), state, worktree path, branch
│       ├── ledger.md               # append-only decision ledger
│       ├── grants/<stamp>-g<NNNN>.md   # one immutable file per grant
│       ├── intake.md
│       ├── briefs/<item>.md
│       └── results.md              # append-only: item, worker result path, revision
```

**Naming grammar.** All parts are lower case. `<slug>` means `^[a-z0-9]+(-[a-z0-9]+)*$` (the grammar `/sc:issue` already uses, `src/superclaude/skills/sc-issue-protocol/refs/create.md:15`). Stamps are UTC `YYYYMMDD-HHMMSS`, as `.dev/tasks/` and `.dev/sweeps/` already use.

| Thing | Grammar | Example | Limit and collision rule |
|---|---|---|---|
| handle `<dev>` | GitHub login, lower-cased, read from `gh api user --jq .login` once and frozen | `clayphi` | 1 to 39 characters (GitHub's published limit, not read in this repo); no `gh`, no coordinator |
| scope folder | `<kind>-<slug>`; a release version writes dots as hyphens | `epic-orchestrator-mode`, `release-v5-1-0`, `adhoc-pr-539-triage` | slug 1 to 40 characters; first `scope.md` pushed wins, the loser records a ledger row |
| coordinator folder | `<dev>`, or `<dev>--<N>` for the same developer's second and later coordinator on one scope | `ironbelly--2` | `<N>` = next unused number, never reused; two hyphens because a login can contain one hyphen but not two |
| coordinator id | `<kind>-<slug>/<dev>[--<N>]` | `epic-orchestrator-mode/clayphi` | unique project-wide |
| Orca worktree name | `coord-<dev>-<kind>-<slug>` | `coord-clayphi-epic-orchestrator-mode` | at most 94 characters; if `orca worktree list` already shows it, add `-2` |
| worktree branch | whatever Orca gives (usually `<prefix>/<name>`, with exceptions) | `ironbelly/coord-ironbelly-epic-orchestrator-mode` | nothing depends on it |
| claim file | `claims/issue-<N>.md`, `claims/pr-<N>.md`, `claims/item-<slug>-<item-id>.md` | `claims/item-orchestrator-mode-sw-07.md` | the path is the lock: second pusher loses |
| decision file | `<kind>-<slug>/decisions/<key>.md` | `epic-orchestrator-mode/decisions/q26.md` | same lock as a claim |
| ledger row id | `<stamp>`, same-second `-2` | `20261114-091812` | unique within the coordinator |
| grant id | `<stamp>-g<NNNN>` (its file name) | `20261114-093000-g0001` | unique within the coordinator |
| cited id | `<coordinator id>/<row or grant id>` | `epic-orchestrator-mode/ironbelly/20261114-093000-g0001` | unique project-wide, so one developer's grant can never be read as another's |

**The claim procedure** (also for a decision file or a new `scope.md`): fetch `origin/coordinators` with no other unpushed commit; create the file with the coordinator id, a stamp and the revision read in it; commit it alone; push at once. If the push is refused and the path now exists upstream, the claim is lost: drop the local commit and pick other work. Nobody ever resolves a conflict on a claim, decision or `scope.md` by keeping their own side. No pushed claim, no dispatch.

**Reading current code.** A coordinator's checkout holds only its branch base plus `.dev/coordinators/`; it reads code and program documents with `git show origin/master:<path>` (or the owning branch) and records the revision.

**If Orca refuses the `origin/coordinators` base (UNVERIFIED):** create the worktree from `origin/master`, run `git merge origin/coordinators` once inside it, and push that merge alone as the first push, recorded as the first ledger row.

## Worked example: two developers, four epic coordinators, one release coordinator

Developers `ironbelly` and `clayphi` (handles seen in this repository's commits and branches), each on their own host. All epic, release and item names below are examples.

- `ironbelly` coordinates two epics: orchestrator mode (#339) and the Orca observer (#409).
- `clayphi` coordinates two epics: orchestrator mode (#339, the same epic, different items) and ccsession failover (#392).
- `ironbelly` also runs the release coordinator for `v5.1.0`.

**Worktrees** (each created by its developer with `orca worktree create --name <name> --base-branch origin/coordinators --agent claude --prompt "<coordinator brief>"`):

| Host | Worktree name | Coordinator id |
|---|---|---|
| ironbelly's | `coord-ironbelly-epic-orchestrator-mode` | `epic-orchestrator-mode/ironbelly` |
| ironbelly's | `coord-ironbelly-epic-orca-observer` | `epic-orca-observer/ironbelly` |
| ironbelly's | `coord-ironbelly-release-v5-1-0` | `release-v5-1-0/ironbelly` |
| clayphi's | `coord-clayphi-epic-orchestrator-mode` | `epic-orchestrator-mode/clayphi` |
| clayphi's | `coord-clayphi-epic-ccsession-failover` | `epic-ccsession-failover/clayphi` |

**Tree on `origin/coordinators` after a day:**

```text
.dev/coordinators/
├── README.md
├── claims/
│   ├── item-orchestrator-mode-sw-07.md     # body: epic-orchestrator-mode/ironbelly, 20261114-110000, <revision>
│   ├── item-orchestrator-mode-ob-05.md     # body: epic-orchestrator-mode/clayphi, ...
│   ├── pr-539.md                           # epic-orchestrator-mode/ironbelly (SW-07's PR work)
│   ├── issue-409.md                        # epic-orca-observer/ironbelly
│   ├── issue-392.md                        # epic-ccsession-failover/clayphi
│   └── item-v5-1-0-changelog.md            # release-v5-1-0/ironbelly (release-only item)
├── epic-orchestrator-mode/
│   ├── scope.md                            # pushed first by ironbelly
│   ├── decisions/q26.md                    # the owner's answer, binding both coordinators on this epic
│   ├── ironbelly/  coordinator.md ledger.md grants/20261114-093000-g0001.md intake.md briefs/sw-07.md results.md
│   └── clayphi/    coordinator.md ledger.md grants/20261114-101500-g0001.md intake.md briefs/ob-05.md results.md
├── epic-orca-observer/
│   ├── scope.md
│   └── ironbelly/ ...
├── epic-ccsession-failover/
│   ├── scope.md
│   └── clayphi/ ...
└── release-v5-1-0/
    ├── scope.md                            # member epics: epic-orchestrator-mode, epic-orca-observer, epic-ccsession-failover
    └── ironbelly/ ...
```

**What happens in the awkward moments:**
- *Both developers want item SW-07.* ironbelly pushes `claims/item-orchestrator-mode-sw-07.md` at 11:00:00; clayphi's push of the same path at 11:00:20 is refused; clayphi fetches, sees the path exists, drops the local claim commit and takes OB-05 instead. Nobody briefed two workers.
- *Two `g0001` grants.* Both developers have a grant numbered `g0001`, but they are cited as `epic-orchestrator-mode/ironbelly/20261114-093000-g0001` and `epic-orchestrator-mode/clayphi/20261114-101500-g0001`; neither coordinator acts on a grant outside its own folder.
- *Epic-wide decision.* The owner's answer to a question binding the whole epic goes in `epic-orchestrator-mode/decisions/q26.md` once; both coordinators' ledgers cite it. A second attempt to write a different `q26.md` loses like a claim.
- *Release gate.* The release coordinator reads the epics' ledgers with `git show origin/coordinators:.dev/coordinators/epic-orchestrator-mode/clayphi/ledger.md`; it claims only release-only items (the changelog), never SW-07 or OB-05.
- *ironbelly wants a second coordinator on orchestrator mode.* It becomes `epic-orchestrator-mode/ironbelly--2`, worktree `coord-ironbelly-epic-orchestrator-mode-2`.
- *clayphi reads ironbelly's state.* `git fetch origin coordinators`, then `git show` or `git ls-tree` on `origin/coordinators`; no checkout, no write.

## Ten rules a person can check

Each rule names how to check it. None of these checks exists as a hook or script today; they are manual or future tooling.

1. **One shared branch.** `git ls-remote origin 'refs/heads/coordinators*'` shows exactly `refs/heads/coordinators` and nothing under `coordinators/`.
2. **Every folder name follows the grammar.** `git ls-tree -r --name-only origin/coordinators -- .dev/coordinators` lists only `README.md`, `claims/<file>`, and paths under `<kind>-<slug>/` with `<kind>` in `epic`, `release`, `adhoc` and a coordinator folder `<dev>` or `<dev>--<N>`.
3. **Each commit stays in its lane.** In `git log --name-only origin/master..origin/coordinators`, every commit (except a recorded bootstrap merge) touches only one coordinator folder plus `claims/`, `decisions/` files or a new `scope.md` naming that coordinator.
4. **Shared files are never edited.** `git log --diff-filter=M --name-only origin/coordinators -- .dev/coordinators/claims '.dev/coordinators/*/decisions' '.dev/coordinators/*/scope.md' '.dev/coordinators/*/*/grants'` prints nothing (claims may be deleted by the coordinator named in them; nothing is modified).
5. **No dispatch without a pushed claim.** For every brief `briefs/<item>.md`, a claim naming the same coordinator was on `origin/coordinators` in an earlier commit than the brief.
6. **No force push.** The `origin/coordinators` you fetched yesterday is an ancestor of today's: `git merge-base --is-ancestor <yesterday's revision> origin/coordinators` succeeds.
7. **Identity comes from GitHub.** Every `coordinator.md` records a handle equal to its folder name (without `--<N>`) and to that developer's `gh api user --jq .login`; no name is taken from `git config user.name`.
8. **Every grant is citable and owned.** Every grant a ledger row cites by `<coordinator id>/<grant id>` resolves to exactly one file in that coordinator's own `grants/` folder.
9. **Worktrees come from Orca with an agent.** `orca worktree list` on each host shows each coordinator worktree named `coord-<dev>-<kind>-<slug>` with its agent; none sits under `.dev/worktrees/` or `.claude/worktrees/`.
10. **Nothing private is pushed, and the old ledger home is retired.** A search of `.dev/coordinators/` on `origin/coordinators` for tokens, secrets, host names or contact details finds none; no new coordinator ledger appears under `.dev/tasks/`; the branch adds nothing under `.claude/` of its own: `git diff --name-only origin/master origin/coordinators -- .claude/` prints nothing (the inherited `.claude/settings.json` is expected).

## What to decide later

- **Merging to master.** The owner allowed "unmerged in the current version". When (if ever) `coordinators` content goes to master, and whether history is squashed, is open. A merge brings every developer's ledgers into master.
- **Departed developers.** How a claim held by a developer who left is released (proposed: by the project owner, recorded as a ledger row in the owner's own coordinator).
- **Archive and clean-up.** Archive is a state row; the folder stays. Whether closed scopes are ever deleted from the branch is open.
- **Reader tooling.** A small read-only script to list every coordinator, claim and open decision would make rules 2 to 5 mechanical. Not needed to start.
- **Other projects.** The owner wants this "in all projects". Projects not hosted on GitHub, or without `gh`, need another handle source.
- **Shared hosts.** If two developers ever share one host, the handle in the worktree name already prevents a name clash; whether Orca itself copes is UNVERIFIED.
- **`.log` files.** `.gitignore` lines 78 and 79 (`logs/`, `*.log`) would silently hide any log file under `.dev/coordinators/`, as they would under `.dev/tasks/` without its exemption (lines 83 to 85). Either forbid log files there or add the same exemption (see the gitignore edit below).

## Changes this implies for the merged spec (listed, NOT applied)

Spec file: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. Line numbers were read on 2026-11-14. `<P>` below stands for this program's scope folder; the suggested value is `epic-orchestrator-tui-alignment` (owner decision 6), and `<dev>` is the handle of the developer who runs the program's coordinator.

1. **XC-01 (line 449), "Location" sentence in the acceptance criteria.** Replace "Location: the always-staged ledger package `.dev/tasks/<program-package>/` in the coordinator home, on the branch the owner names in Q26; never in the #539 checkout; committed only when the owner asks (project rule: `.dev/tasks/` is always staged; staging is not committing)." with "Location: the coordinator folder `.dev/coordinators/<P>/<dev>/` (`ledger.md`, `grants/`, `intake.md`) on the shared `coordinators` branch, in that coordinator's own Orca worktree; owner answers that bind the whole program are create-once files `.dev/coordinators/<P>/decisions/<qid>.md`; always staged in the coordinator worktree; committed and pushed only to `origin coordinators`, only the coordinator's own paths, under `GRANT(XC-01,coordinator-push)`; never in the #539 checkout." In part (5), replace "it holds the grant table of 6.8" with "it holds the grant table of 6.8 as one immutable file per grant under `grants/`". In "Observe", replace "the ledger file in the package Q26 locates" with "`git show origin/coordinators:.dev/coordinators/<P>/<dev>/ledger.md`". In "runs in", replace "the coordinator home named in Q26 (never the #539 checkout)" with "the coordinator worktree `coord-<dev>-<P>` (never the #539 checkout)".
2. **XC-09 (line 457).** In (1), replace "A person opens it (a coordinator is person-opened; it is not a worker)" with "Its developer creates its worktree through Orca with `--agent` (the owner's ruling that this counts as person-opened is decision file `<P>/decisions/q26.md`; it is not a worker)". In "blocked-by", replace "Q26 (owner opens it in the home Q26 names; default if unanswered: XC-09 does not start)" with "Q26 (answered 2026-11-14) and the Q26 follow-up decisions 1, 2 and 4 of `owner-questions/Q26-coordinator-layout/final.md`". In "runs in", replace the whole cell with "its own Orca worktree `coord-<dev>-<P>`, created with `orca worktree create --name coord-<dev>-<P> --base-branch origin/coordinators --agent claude --prompt "<coordinator brief>"` (if Orca refuses that base: from `origin/master` plus one recorded bootstrap merge of `origin/coordinators`); never the #539 checkout; never switches a checkout's branch". In "Observe", replace "the session's home and branch recorded in the ledger" with "`coordinator.md` in `.dev/coordinators/<P>/<dev>/` on `origin/coordinators`".
3. **5.4 worktree map, "coordinator home" row (line 900).** Replace the row with: `| coord-<dev>-<P> (new; Q26 answered 2026-11-14) | no | origin/coordinators (fallback origin/master plus one recorded merge of origin/coordinators) | XC-09 session; .dev/coordinators/<P>/<dev>/ (XC-01) | the developer who creates it through Orca | pushes only HEAD:coordinators, only its own paths; never force-pushes; never switches branch |`. In the "ledger only" row (line 910), replace "In the coordinator home (Q26), never in the #539 checkout" with "In `.dev/coordinators/<P>/` on `coordinators`, never in the #539 checkout".
4. **6.1 inputs, "Decision ledger" row (line 941).** Replace the path cell with "XC-01: `.dev/coordinators/<P>/<dev>/ledger.md` and `.dev/coordinators/<P>/decisions/` on `origin/coordinators` (read with `git show`); never in the #539 checkout".
5. **6.2 (line 951).** Replace "The coordinator runs in the home the owner names in Q26;" with "The coordinator runs in its own Orca worktree on the shared `coordinators` branch (Q26, answered 2026-11-14; layout in `owner-questions/Q26-coordinator-layout/final.md`);". At line 954, after "A top-level agent's worktree is created with `orca worktree create --name <name> --base-branch origin/master --agent claude --prompt "<task>"`", add: "except a coordinator worktree, which uses `--base-branch origin/coordinators` (fallback as in 5.4)."
6. **6.4 rule 3 (line 976).** Replace "before W0 exits the owner names the coordinator's home and the branch that stages the always-staged ledger package `.dev/tasks/<program-package>/` (Q26); the ledger is committed only when the owner asks;" with "coordinator state (ledger, grants, intake, briefs, result pointers, scope-wide decisions) lives only under `.dev/coordinators/` on the shared `coordinators` branch, in the coordinator's own Orca worktree (Q26); it is always staged there and committed and pushed by the coordinator only to `origin coordinators`, only its own paths, under its standing push grant, never force-pushed; every claim and decision file is taken by the claim procedure of `owner-questions/Q26-coordinator-layout/merged-output.md`;". Keep the rest of the rule (no `.claude/` staging; `.dev/tasks/` always staged).
7. **6.8 grant table (line 1047).** Replace "a second table in the same ledger" with "one immutable file per grant under the coordinator's `grants/` folder, cited project-wide as `<coordinator id>/<grant id>`". Add `coordinator-push` to the action list, defined as "`git push origin HEAD:coordinators` of the coordinator's own paths only".
8. **Section 3, Q26 row (line 553).** Mark it answered: "Answered 2026-11-14: a dedicated shared `coordinators` branch per project, one Orca worktree per coordinator, `.dev/coordinators/` in every project, unmerged for now; layout and naming in `owner-questions/Q26-coordinator-layout/final.md`; follow-up owner decisions 1 to 7 there." Add the same pointer to the Q26 row of the questions appendix (line 1291).
9. **`.dev/README.md`.** Add a row to the Subdirectories table: "`coordinators/` | Coordinator state, on the shared `coordinators` branch only (not on master in this version): one folder per epic, release or ad hoc scope, one sub-folder per developer's coordinator, project-wide `claims/`. See `.dev/coordinators/README.md` on that branch." Add to the decision guide: "Coordinator ledger, grants, briefs, claims | `.dev/coordinators/<kind>-<scope>/<dev>/` on branch `coordinators`". This lands on master only through a PR (owner decision 7).
10. **`.gitignore` and staging rule.** No ignore rule for `.dev/coordinators/` (checked with `git check-ignore`: `.md` files there are not ignored). Either forbid `.log` files and `logs/` folders under it, or add `!.dev/coordinators/**/logs/` and `!.dev/coordinators/**/*.log` next to the `.dev/tasks/` exemption (lines 84 and 85). Add to project `CLAUDE.md`, beside the `.dev/tasks/` rule: "`.dev/coordinators/` is always staged in a coordinator worktree; a coordinator commits and pushes only its own paths to `origin coordinators` under its standing grant; it is never staged in any other worktree and never force-pushed."
11. **New owner-decision rows.** Add the seven decisions of the next section to section 3 (as Q26a to Q26g, or new numbers after Q33), each gating XC-09.

## Remaining owner decisions

Ask these one at a time, in this order. Each is written for a reader who has never seen the project. Decisions 1, 2 and 4 must be answered before the first coordinator starts.

**Decision 1. Does a coordinator session that a developer launches through Orca count as "opened by a person"?**
Background: project rules say a coordinator, the session that hands work to AI workers, must be opened by a person, not started by another AI session. In this layout each coordinator runs in its own worktree, which the developer creates with Orca's `orca worktree create ... --agent claude`; Orca then starts the Claude session. No written rule says whether that counts.
- Yes: every coordinator is created this way; the developer's act of running the command is the "opening". This is what your 2026-11-14 answer ("create and maintain a Coordinator branch and worktree") implies.
- No: each coordinator must be a session the developer starts by hand inside an existing folder, which conflicts with "one worktree per coordinator through Orca" and sends the design back to the drawing board.
Recommended: Yes. Example answer: "Q26 follow-up 1: yes, a coordinator I or another developer launch through Orca with `--agent` counts as person-opened."

**Decision 2. May every coordinator commit and push its own records to the shared `coordinators` branch without asking each time?**
Background: today the rule is that the decision ledger is committed only when you ask. With several developers, nobody can see anyone else's coordinator, or their claims on work, unless it is pushed to the shared branch on the fork. Pushing is an outward write and needs your standing approval.
- Yes, narrowed: a standing approval to push to `origin coordinators` only, only the coordinator's own folder, its own claim and decision files and a new scope file, never a force push. Every other push still needs its own approval.
- Yes, unrestricted: any push to `coordinators`. Simpler, weaker.
- No: coordinators stay local. Then claims are invisible and two coordinators can work on the same issue.
Recommended: Yes, narrowed.

**Decision 3. Who may approve a coordinator's outward actions (pushes to PRs, issue posts, merges), and who is "the project owner" for cross-developer acts?**
Background: today one owner writes every approval. With several developers, either you approve everything, or each developer approves their own coordinator's actions. Some acts touch other developers' work: releasing a claim someone else holds, changing a scope file after it was created, deleting a folder.
- You approve everything for every developer; you are the project owner for all cross-developer acts.
- Each developer approves their own coordinator's outward actions; you remain the project owner for cross-developer acts.
Recommended: the second, with you named as project owner. It keeps each developer in control of their own work and keeps you as the single referee.

**Decision 4. Who creates the `coordinators` branch the first time?**
Background: the branch does not exist yet (checked 2026-11-14). Someone has to push its first commit (a `.dev/coordinators/README.md`) to the fork.
- You do it once by hand from `origin/master`.
- The first coordinator does it under its push approval.
Recommended: you, once by hand, so the first coordinator starts from a branch you have seen.

**Decision 5. Should the fork forbid force pushes to `coordinators`?**
Background: the claim lock works because git refuses the second of two conflicting pushes. A force push overwrites history and silently erases everyone's claims. GitHub can forbid force pushes on a branch through branch protection; whether this fork's plan allows it is UNVERIFIED.
- Yes, turn on protection (if available) for `coordinators`: no force push, no deletion.
- No, rely on the written rule only.
Recommended: yes if available; the written rule applies either way.

**Decision 6. What is this program's scope folder called?**
Background: the current alignment program (orchestrator mode, observer, issue watcher, the Coder listener and Orchestrator v2) needs one folder name under `.dev/coordinators/`. It spans several issues, so it is an epic.
- `epic-orchestrator-tui-alignment` (matches the brainstorm folder `20261113-orchestrator-tui-alignment`).
- `epic-orchestrator-mode` (named after issue #339 only).
Recommended: `epic-orchestrator-tui-alignment`, because the program is wider than #339.

**Decision 7. When does `.dev/README.md` on master learn about `.dev/coordinators/`?**
Background: the branch stays unmerged, so master's `.dev/README.md` (the "where things go" guide) would not mention the folder. Adding the entry on master needs a PR to the fork.
- Now, in a small PR opened with `/sc:pr-submit --monitor 3`.
- Later, with the first PR that touches coordinator tooling.
- Never while the branch is unmerged; the branch's own `.dev/coordinators/README.md` is enough.
Recommended: later, with the first coordinator-tooling PR; until then the branch README carries the rules.

## Record

- Proposals: `proposal-A.md`, `proposal-B.md`, `proposal-C.md` (this folder)
- Debate: `adversarial/` (`diff-analysis.md`, `round1-advocate-V1.md` to `V3.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`)
- Merged layout: `merged-output.md`
- fallback_mode: false. The three advocates and the merge executor were spawned as separate agents. The diff analysis, transcript assembly, scoring (both position-bias passes in one context), the refactor plan and four post-merge fixes (listed at the end of `adversarial/merge-log.md`) were done in-context by this worker, and the fixes were not re-reviewed by a separate agent. Return contract status: partial for that reason.
- Not checked: Orca's behaviour with a non-master base branch, Orca's branch-prefix rule, branch protection on the fork, GitHub's login rules (taken from GitHub's published rules, not read here). All are marked UNVERIFIED where used.
- Nothing was committed, pushed, posted or created outside this folder.
