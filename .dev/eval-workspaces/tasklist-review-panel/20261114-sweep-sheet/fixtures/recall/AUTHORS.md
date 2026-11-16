# Authors of the recall fixtures (F-RECALL, REQ-21)

## Who seeded

A fresh Claude Code session, not a person. Model: claude-sonnet-5-5. Date: 2026-11-15 (UTC).
The session was started only for this task (plan step 14.1).

## What the author had and had not read

The author had **not** read the extractors or any ground truth. Specifically, the session did not open, list the contents of or run anything that prints: `sweep/*.py`, `analysis/*.py`, `scaffold/*.py`, `tests/test_e*.py`, `tests/test_recall.py`, `tests/test_g0.py`, any `ground-truth*.json` or `score*.json`, `results/`, `runs/`, the older evaluation workspaces (`20261111-a1`, `20261113-collab`, `20261114-recipe-ledger`), `.dev/reflect/`, `.dev/brainstorms/`, or the three study packages. It did not run pytest on the `freeze` marker or on any extractor, so it never saw which seeds are found.

What it did read: `TESTING.md` section 2 (F-RECALL), requirements REQ-21 and REQ-08, `DESIGN.md` only for the class names, `cards/*.json`, `cards/README.md`, `tests/test_cards.py`, `tests/test_readme.py`, the four plans below with their `source.md`, and a few repository files (tests, `install_skill.py`, `src/` file names) to confirm that a seed points at something real.

## Plans

| Plan id (package folder under `.dev/tasks/done/`) | Seeds |
|---|---|
| `TASK-WF-diagnosticRefres-20261109-144413` | 7 |
| `TASK-WF-devGuideRefactor-20261104-135403` | 12 |
| `TASK-WF-removeTheAnyIssu-20261102-053741` | 15 |
| `TASK-WF-renameTheScIssue-20261104-174359` | 7 |

None is one of the three study packages (`TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649`, `TASK-WF-design-20261108-041415`). The plan `TASK-WF-launcherFollowup-20261105-131531` was read and dropped because its source points into a study package.

Seeds per class (41 in all, after the repair of 2026-11-15 below): C1 5, C2 7, C4 6, C5 5, C6 6, C7 7, C8 5. Class C3 is not seeded (it is not in the list for this fixture). The first version had 37 seeds and one C8 seed.

## Overlap caveat

The author cannot know the hold-out documents or the planted-set plans. **Overlap of these four plans with the hold-out set was not checked.** If any of them is a hold-out or planted-set document, drop that folder before the freeze.

## Other limits to know

- Class C8 has 5 seeds, and all of them are in one plan (`TASK-WF-removeTheAnyIssu-20261102-053741`). Of the other three plans, `diagnosticRefres` edits no repository file (it refreshes an installed skill), `devGuideRefactor` edits only the developer guide, which no test or document outside those the plan names pins (checked with `git grep` in its snapshot), and `renameTheScIssue` edits files that were untracked when the plan was written, so its snapshot does not hold them (see the snapshot limits below). The C8 recall figure therefore rests on one plan. The C8 seeds s12 to s15 are pinned by documents (release guides and a reference page), not by tests, because `git grep` found no test pinning the plan's edits outside the test directories the plan runs; s11 is pinned by a test in a directory the plan runs without naming that file.
- Two kinds of C8 seed exist, and the `note` field of each new seed says which. s12 is **inserted** (the original note that named its pinned guide was removed in `seeded.md`). s13, s14 and s15 are **located**: their quoted sentence is unchanged from `original.md`, and the original plan never named the document that pins it, so they were already defects of the original. Counting them as seeds means a reviewer who reports them is credited as a hit, and they are not in the set that counts against precision. If the owner wants only inserted seeds, drop s13 to s15; C8 then has 2 seeds.
- The plans are real and finished, and the repository is now at a later state than the plans' base commit, so a few repository facts a reviewer sees differ from what the plan assumed. Each seed was written to be visible from the plan text (or its source) alone; the description says what the wrong outcome is.
- The original plans carry real defects of their own. The seeds are additions, so a reviewer may also report defects that are in `original.md`; those count against precision, not recall.
- Each seed is an edit of the plan text, except the three located C8 seeds s13 to s15 of `removeTheAnyIssu` (see above). A seed that removes text is quoted at the sentence where the missing text should have been; the C8 seed s12 is quoted at the plan sentence that makes the edit, not at the place where the note was removed. Every quote in `seeds.json` occurs exactly once in `seeded.md` (checked by script, outside the repository, before this file was written; rechecked with `grep -o -F` for all 41 quotes on 2026-11-15).
- Some seeds fit two classes (for example, a criterion wider than its instruction is also one that cannot pass). The class in `seeds.json` is the author's one chosen label.

Files per plan folder: `original.md` (byte copy of the plan), `seeded.md`, `seeds.json` (id, class, quote, description; seeds added on 2026-11-15 also carry `note`), `source.md` (byte copy of the driving source), and `snapshot/` (not committed, see below).

## Snapshots (repair of 2026-11-15)

Each plan folder has `snapshot/`: the repository as it was just before the plan was implemented, limited to the DD-5 search scope, with `.dev/` removed, and made its own throwaway git repository (the extractors run `git grep` in it). It is built with `git archive` by `fixtures/recall/build-snapshots.sh`, which holds the base commits below and rebuilds any or all snapshots (`./build-snapshots.sh [plan-id ...]`, about 8 seconds for all four). **The snapshot folders are not committed and stay untracked:** each holds a nested `.git`, and they total about 155 MB. `fixtures/recall/.gitignore` lists `*/snapshot/` so a stray `git add` skips them. Run the script after a fresh checkout and before the `freeze` tests.

Base commits (the commit object may sit on a feature branch, not on master). Rule: the latest commit on any branch before the UTC timestamp in the plan's folder name, except where an earlier commit holds more of the existing files the plan names (this applies to `devGuideRefactor` only, whose plan was written on the Orca feature branch). The ledger "start sha" values in the plan packages are tree hashes, not commits, so they were not used.

| Plan | Plan created (UTC, from the folder name) | Base commit | Commit date and subject |
|---|---|---|---|
| `TASK-WF-diagnosticRefres-20261109-144413` | 2026-11-09 14:44:13 | `94e609ccef2a5ee67fa8918426157046be1f32c8` | 2026-11-09 12:55:12Z, docs(dev): archive reviewed L2 implementation and final repair evidence (#441) |
| `TASK-WF-devGuideRefactor-20261104-135403` | 2026-11-04 13:54:03 | `8db29f1165508187b7a14a48f2f66793e269d596` | 2026-11-03 21:57:43Z, feat(core): Orca worker contract P0 static part |
| `TASK-WF-removeTheAnyIssu-20261102-053741` | 2026-11-02 05:37:41 | `d6b02a4bfb5c64f3c7125aaae1e220724d590517` | 2026-11-01 22:21:49-05:00, fix(gitignore): keep tests/ in scope for case-insensitive matchers (#340) |
| `TASK-WF-renameTheScIssue-20261104-174359` | 2026-11-04 17:43:59 | `b5c09e90e6584c4bb8b340723f4008ffb21b3460` | 2026-11-04 16:32:40Z, docs(orca): P0 live worker checks pass; spec 7.2 step 5 reads the session file |

Snapshot limits:

- `renameTheScIssue`: the `/sc:issue` files that plan edits (`sc-issue-protocol`, the `issue-worker` agents, `commands/issue.md`, `tests/skills/test_issue_worker_agents.py`, `docs/designs/sc-issue-command.md`) were untracked in the author's working tree when the plan was written and were first committed together with the plan's own work (commit `6542ca72b`). No earlier commit holds them, so this snapshot does not either. Evidence searches for those files find nothing, and no C8 seed is possible in this plan.
- The `.dev/` files that plans read (specs, inventories, `.dev/review-severity-rule/...`) are removed on purpose (DD-5 excludes `.dev/`).
- The scope also keeps the directory of each path a plan names and same-basename copies of named files, so a snapshot holds some `src/` and `plugins/` files (each 30 to 45 MB in all).
- The snapshots were built, and checked with `git grep` for the C8 pins, but no extractor was run on them.

## Repair of 2026-11-15 (who and what)

The snapshots and the C8 seeds s12 to s15 were added by a fresh Claude Code session (model claude-sonnet-5-5, 2026-11-15 UTC), a different session from the one that wrote the first seeds, started only for this repair. It had **not** read the extractors or any ground truth (it did not open or run `sweep/*.py`, `analysis/g0.py`, `tests/test_e*.py`, `tests/test_recall.py`, any `ground-truth*.json` or `score*.json`, `runs/`, the older evaluation workspaces, `.dev/reflect/`, `.dev/brainstorms/` or the three study packages, and it ran no extractor and no freeze test). It did read `results/freeze-check-20261115.md`, so it **knew the first failing result** (recall 0.18, 0.50, 0.00, 0.20, 0.00 and the two fixture gaps: no snapshot, one C8 seed). It also read this file, the seeds and seeded plans, `TESTING.md` section 2, `DESIGN.md` DD-5, and `bin/build-sandbox.sh` as a how-to. It chose the C8 seeds from pins found with `git grep` in the snapshots, not from any extractor output. No seed from the first version was changed.

second author (session): 2026-11-15
repair session (fresh Sonnet, did not read the extractors or any ground truth, knew the first failing result): 2026-11-15
