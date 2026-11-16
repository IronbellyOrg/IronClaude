# Recall fixture repair (Sweep Sheet freeze check), 2026-11-15

Context for a reader with no history: the first freeze check (`results/freeze-check-20261115.md`) failed, and named two fixture gaps: the four recall plans had no `snapshot/` (so the evidence-searching extractors had nothing to search) and class C8 had one seed. This repair closes both gaps. It changes no extractor and was done by a fresh Sonnet session (claude-sonnet-5-5) that had not read the extractors or any ground truth and knew the first failing result. Nothing was run on the extractors, so this note says nothing about recall.

## Files created or changed (all under `fixtures/recall/` except this report)

| File | What |
|---|---|
| `build-snapshots.sh` (new, executable) | Rebuilds `<plan>/snapshot/` for all four plans, or for plan ids given as arguments. About 8 seconds for all four. |
| `<plan>/snapshot/` x4 (new, untracked) | DD-5 scope of the repository at the base commit, `.dev/` removed, a throwaway git repository inside. 30 to 45 MB each, about 155 MB in all. |
| `.gitignore` (new) | Lists `*/snapshot/` so a stray `git add` skips the snapshots (each has a nested `.git`). Not asked for; added to keep the "never commit" rule from depending on memory. |
| `TASK-WF-removeTheAnyIssu-20261102-053741/seeds.json` | Seeds s12 to s15 added (class C8, each with a `note` field naming the pinned file). The first 11 seeds are byte-identical in content. |
| `TASK-WF-removeTheAnyIssu-20261102-053741/seeded.md` | One edit: the Constraints note that named `docs/guides/tdd-skill-release-guide.md` (as out of scope) was removed, which creates seed s12. |
| `AUTHORS.md` | Seed counts, base shas, snapshot section, repair section, C8 limits, the second-author statement. |

## Base shas

| Plan | Base commit |
|---|---|
| `TASK-WF-diagnosticRefres-20261109-144413` | `94e609ccef2a5ee67fa8918426157046be1f32c8` |
| `TASK-WF-devGuideRefactor-20261104-135403` | `8db29f1165508187b7a14a48f2f66793e269d596` (feature branch commit; the plan names `WORKER-CONTRACT.md` and `test_worker_contract.py`, which master at that date does not hold) |
| `TASK-WF-removeTheAnyIssu-20261102-053741` | `d6b02a4bfb5c64f3c7125aaae1e220724d590517` |
| `TASK-WF-renameTheScIssue-20261104-174359` | `b5c09e90e6584c4bb8b340723f4008ffb21b3460` |

How chosen: the latest commit on any branch before the UTC timestamp in the plan's folder name (read as UTC because the implement ledgers of all four plans start after it in UTC), except `devGuideRefactor`, where an earlier commit holds all 8 existing files the plan names and the latest does not. The ledger "start sha" values in the plan packages are tree hashes, not commits, so they were not usable. My first choice (last commit on master) was wrong for `devGuideRefactor` (it lacked the worker contract files) and older than the latest commit for `diagnosticRefres` and `renameTheScIssue`; I found that by counting the plan-named files present at each candidate, then rebuilt.

## Seed counts per class (41 in all, was 37)

C1 5, C2 7, C4 6, C5 5, C6 6, C7 7, **C8 5 (was 1)**. Per plan: diagnosticRefres 7, devGuideRefactor 12, removeTheAnyIssu 15 (was 11), renameTheScIssue 7. Every one of the 41 quotes occurs exactly once in its `seeded.md` (checked with `grep -o -F`).

## The four new C8 seeds (all in removeTheAnyIssu; pinned file shown in each seed's `note`)

| Seed | Plan sentence quoted | Pinned by (in the snapshot) | Kind |
|---|---|---|---|
| s12 | Task 7, tdd build-request-template "lines 124 and 152" | `docs/guides/tdd-skill-release-guide.md:345` ("Zero leniency ...") and `:271` | inserted (original out-of-scope note for this guide removed) |
| s13 | Task 7, prd build-request-template "lines 129 and 157" | `docs/guides/prd-skill-release-guide.md:332` and `:261` | located |
| s14 | Task 17, `models.py:203` `max_research_fix_cycles` | `docs/guides/prd-skill-release-guide.md:455` ("max 3 for research") | located |
| s15 | Task 2, "the research-gate Verdict bullets (171-172)" | `docs/reference/nfr-conv-2-prose-determinism.md:131-133` (quotes the rf-qa gate rule) | located |

Each pin was confirmed with `git grep` in the snapshot, and the plan names none of these documents (the plan never says `prd-skill-release-guide`, `nfr-conv-2` or `docs/reference`).

## What I could not do, and what you should decide

1. **Only 1 of 4 C8 seeds is an inserted edit.** s13, s14 and s15 are defects the original plan already had (it edits something a document pins and never names the document); I located and verified them but did not edit the plan text for them. `AUTHORS.md` says so. This is a real departure from "seeds are additions". If you want inserted seeds only, drop s13 to s15; C8 then has 2 seeds (s11, s12), still below 5.
2. **No other plan can hold C8 seeds.** `diagnosticRefres` edits no repository file (it refreshes an installed skill). `devGuideRefactor` edits only the developer guide, and `git grep` finds no test or document outside the tests the plan runs that pins it. `renameTheScIssue` edits `/sc:issue` files that were untracked when the plan was written (first committed in `6542ca72b` together with the plan's own work), so no snapshot can hold them and its evidence searches will find nothing; its snapshot is a valid tree but a weak fixture for E2 to E4.
3. **C8 recall rests on one plan.** All five C8 seeds are in removeTheAnyIssu, and four of them are pinned by documents, not tests (the plan already runs every test directory that pins its edits, so no further test pin was found). s11 is pinned by a test in a directory the plan runs (`tests/audit`), without naming that file, so under the strict "never names or runs" reading s11 is the weakest C8 seed. I did not change it.
4. **Snapshots are untracked and big.** They must be rebuilt (`fixtures/recall/build-snapshots.sh`) on any other checkout before the `freeze` tests. The `.gitignore` also hides them from `git status`.
5. **Search scope.** The DD-5 scope is implemented in the script (tests/, scripts/, docs/, root files, change-log files, directories of plan-named paths, same-basename copies, no `.dev/` or dependency folders). It pulls in some `src/` and `plugins/` files through plan-named directories. If the extractor's scope function is stricter, the snapshots hold more than it reads, which is harmless.
6. **Not done:** no extractor, freeze test or lint was run; no overlap check against the hold-out set; nothing was staged or committed.

## Recommended next step

Re-run the freeze check with the snapshots in place before changing any extractor, and read the E2, E3 and E4 numbers against the missing-snapshot explanation in the first result. Treat any C8 figure as a single-plan figure.
