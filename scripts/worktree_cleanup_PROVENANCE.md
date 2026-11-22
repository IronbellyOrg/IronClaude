# worktree_cleanup.py: Provenance of the adapted rules

`scripts/worktree_cleanup.py` adapts rules from three files written by Jay Wedgeworth, used with the owner's approval. This file records the source, the licence, and what was kept, changed or dropped for each rule. The script is rewritten for git worktrees of IronbellyOrg repos; no line of his code is copied as it stands, and the rules are adapted. The root `NOTICE` lists the component.

## Source

| Field | Value |
|---|---|
| Upstream repository | https://github.com/Simple-With-Us/AI-Fleet-Coordinator |
| Author and copyright | Jay Wedgeworth, Copyright 2026 Jay Wedgeworth |
| Licence | Apache License, Version 2.0 (Apache-2.0); the licence text is kept verbatim at `src/superclaude/skills/sc-closeout-protocol/LICENSE` |
| Upstream NOTICE file | none (the upstream repository has no `NOTICE` file, so there is nothing to carry under section 4(d) of the licence) |
| Date read | 2026-11-20, in full; none of it was run |
| Fetched automatically later | never; a drift review compares the files by hand |

| Upstream file | Lines | Git blob | Last commit | Where it went |
|---|---|---|---|---|
| `scripts/fleet_lanes/retire.py` | 1,923 | not recorded | not recorded | the rules and the removal order of `scripts/worktree_cleanup.py` |
| `docs/protocols/lane-map.md` | 300 | not recorded | not recorded | the "Cleaners" contract: `list` is the doctor and `prune` runs the same decision |
| `scripts/disk-janitor.sh` | 1,161 | not recorded | not recorded | the idle floor of 7 days, the run lock, the dry run default and the check for a checkout inside a worktree |
| `scripts/branch-landed.sh` | 85 | not recorded | not recorded | not adopted again: it is reused through `/sc:closeout` (its provenance is in `src/superclaude/skills/sc-closeout-protocol/PROVENANCE.md`) |

The specification records no blob or commit pin for any of these files, so none is written here and none is invented. A search of the three code files for model or inference calls found none.

## Notice in the adapted file

`scripts/worktree_cleanup.py` carries a comment block after the shebang that names the three source files, Jay Wedgeworth's copyright, the Apache License, Version 2.0, a line saying what IronClaude changed, and a pointer to this file.

## What changed

The label is one of three words. `kept as is` means the idea or logic carries over unchanged. `changed` means only the part this setup needs is different, or the text itself changed. `dropped` means it names a surface this setup does not have or a step the issue does not ask for. When the specification used a different word, the row says it after the label.

| # | Upstream rule or piece | Label | What happens here, and why |
|---|---|---|---|
| 1 | `retire.py`: linked worktree under the lanes root, never the integration tree | changed | Rule 1. Our worktrees sit in several places, so any linked worktree of our repos qualifies, never a main checkout. |
| 2 | `retire.py`: the lane belongs to the chosen seat (folder name and `lane.json`) | dropped | Each Coder workspace runs its own automation and sees only its own worktrees. |
| 3 | `retire.py`: not locked, no process with its folder inside, no git operation in progress, no `.janitor-keep` | changed (the specification says adopted) | Rules 6 and 8. It reads `/proc/<pid>/cwd` because `lsof` is not installed here; the worktree's own Orca terminals no longer keep it, they are closed first and everything is checked again; the keep file is `.worktree-keep`. Added from the janitor: a worktree that holds another checkout is never removed. |
| 4 | `retire.py`: `git status` clean, and no git-ignored local state | changed (the specification says adopted) | Rule 5. Files under `.dev/` are allowed after the archive step. |
| 5 | `retire.py`: nothing unpushed (HEAD on a branch that exists on the remote, or in the default branch, or held by a merged or closed pull request) | changed | Rule 3. HEAD equals the merged pull request's last commit or is behind it. GitHub keeps that commit, so a squash merge or a deleted branch does not matter. Stricter than his: no "in the default branch" shortcut. |
| 6 | `retire.py`: the work is done (pull request merged or closed, or merged into the default branch, or the upstream was deleted, or a tree or byte-identical proof, or local evidence) | changed | Rule 2. Only a merged pull request counts, judged through the landed check. The tree and byte-identical proofs, closed counting as done and the local-evidence fallback are dropped in version 1. |
| 7 | `retire.py`: review checkouts `review-pr-<n>` are done when the pull request is merged or closed | dropped | We have no such naming. |
| 8 | `retire.py prune`: kept if active in the last 15 minutes; a lane made and never used is kept 24 hours | changed (the specification says replaced) | Rule 7. Seven days idle, which is the janitor's value, because this job runs unattended for many people. The number is a setting. |
| 9 | `retire.py`: remove under a per-repo lock, check again, `git worktree remove` without force, then `git branch -d` (never the forced form) | changed (the specification says adopted) | Labelled changed because the Orca removal is added to his order. The same order, with the Orca removal for worktrees Orca lists. A branch that git says is not fully merged, as after a squash merge, is reported as kept. `git worktree prune` is never run (a missing folder is only reported). |
| 10 | `retire.py`: a runner that only allows a fixed list of commands (`check_allowed`) | changed (the specification says adopted) | Labelled changed because the runner is rewritten. The idea is kept. The script runs commands only through one runner with a positive allowlist of exact argument shapes, and a test records every command. |
| 11 | `retire.py`: dry run is the default; exit codes 0, 64, 69 | kept as is | The same default and the same three exit codes. |
| 12 | `branch-landed.sh` | kept as is (the specification says reused through `/sc:closeout`) | Not adopted a second time: the landed check is the one installed with `/sc:closeout`, and its own provenance file says what was changed there. |
| 13 | `lane-map.md`, "Cleaners": act only on the doctor's candidate list; `git worktree remove`, never `rm -rf`; never create a keep file as protection | kept as is (the specification says adopted) | `list` is the doctor and `prune` runs the same decision code in the same run, so it never acts on a stale report. |
| 14 | `disk-janitor.sh`: every 30 minutes, only when disk is low, with a pressure gate on load and swap | dropped (the specification says not adopted) | He runs often because his disk was nearly full; ours has plenty of space, so the job is daily and light, with no disk gate and no pressure gate in version 1. |
| 15 | `disk-janitor.sh`: the `REAP_WORKTREES` master switch, a dry run switch, a run lock with a heartbeat | changed (the specification says adopted in spirit) | Dry run by default, a per-repo lock, and the automation itself is the master switch (off until a person switches it on). |

Jay's other cleanup pieces (the dependency reaper, "delete branch on merge" as a repository setting, a low-disk trigger, main-checkout sync, the placement watcher and orphan process cleanup) are not part of version 1 and are not specified here.

## What this version adds

Only what the issue asks for: the archive step that saves untracked and ignored `.dev/` files to the evidence repo `IronbellyOrg/run-evidence`, the table and its two output files, the `/sc:worktrees` command, the tests, and a definition of a daily automation that is written and not switched on.

## Drift review

Nothing is fetched automatically. To review drift, read the three upstream files and compare them with the rows above. A later pin would be added to the source table in the same change that updates the script.
