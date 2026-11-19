# Retrospective: IronClaude 6.1.0 release (addendum to the 6.0.0 retrospective)

Written by the `ic6-orchestrator` session after the post-release merge. Proposals only; nothing in the release procedure or the skills was changed. It adds to `../v6.0.0/RETROSPECTIVE.md`; the proposals there still stand. Facts are in `PROCESS-LOG.md` entries 1 to 12 and `RELEASE-READINESS.md` of this folder.

## 1. What we did, in order (UTC)

| When | What |
|---|---|
| 11-18 20:57 | Clay (via GeneralIronFlow) approved the 6.1.0 job: merge #650, #653, #656, #657 into `integration` in order, then run the release as 6.0.0 |
| 11-18 20:58 to 22:16 | Four pull requests of the bundle agent merged one after another (each rebased by the agent after the previous merge): #650 21:17, #653 21:31, #656 21:56, #657 22:16. One review finding in between (#656), one changelog gap found by my completeness check (#646) |
| 11-18 21:17 | `master` merged into `integration` once (#641 had been added to the release by Clay and merged into `master` first) |
| 11-18 22:18 | Release PR #658 opened; Augment found a wrong 365-day statement in the installation guide (#641 changed the limit to 90); small fix #659 merged 22:53 |
| 11-18 22:33 | **Ryan squash-merged #658 by mistake on his phone** (found by me only at 23:24, see below) |
| 11-19 01:17 to 01:20 | Ryan reverted the squash (#662) and opened #664 (redo); my merge-back PR #663 became unnecessary and was closed |
| 11-19 01:29 to 01:33 | Ryan merged #660 and #661 into `master` while #664 waited; I synced `integration` after #660 and re-ran both reviewers |
| 11-19 01:47 | #664 merged with a merge commit (`64dfc0e86`); G2 green 01:57; tag `v6.1.0` and the GitHub release 01:57 (39 minutes from Clay's go) |
| 11-19 01:58 to 03:35 | Post-release (#667): docs sync and real install and upgrade runs; four review rounds on the evidence script; merged 03:35 |

## 2. What worked, what did not

**Worked:** the 6.0.0 lesson "list what the release depends on with an owner" (`RELEASE-READINESS.md` section 1): Part B was in the plan from the start this time, and the open scope questions (#641, post-release scope) were answered before the release PR opened. The changelog completeness check caught #646. Verifying every pull request on GitHub myself caught the open threads and the missing reviews. The gate in a temporary clone (not a worktree switch) kept the records branch intact. Every merge was pinned with `--match-head-commit`.

**Did not work:**

| Problem | Cause | Cost |
|---|---|---|
| The release PR was squash-merged by a person on a phone | Nothing enforces the merge method; the PR body line "merge with a merge commit" is a request, not a control | revert, a second release PR, about 2 hours of plan change |
| I found the merge 50 minutes late | My status script did not print the PR state; I read `merge=UNKNOWN` as GitHub lag; my wait loop did not stop on `MERGED` | 50 minutes of work on a closed PR (none of it harmful) |
| `master` kept moving after the release PR was green (#660, #661) | Two reviewed pull requests were merged into `master` directly while it waited | one extra sync, CI and review round (about 25 minutes), and two changes in the tag without changelog entries |
| Reviewers do not re-run on a push | By design of both bots | the head was green for 9 minutes with no review; I had to re-trigger both |
| A documented limit changed (365 to 90 days) and the guide still said 365 | `/sc:post-release` would have found it, but only after the tag; the PR that changed the code did not search the docs | a fix PR before the release (about 35 minutes) |
| Review of the evidence script ran four rounds in 6.1.0, as in 6.0.0 | The script's guards were written after the fact, and each guard invited a finer one | four full 7-minute reruns and about 50 minutes of waiting |
| The Orca app became unreachable for about 20 minutes | Orca restart | the terminal watch lost the agent; GitHub watches kept working |
| `make verify-deps` failed in my gate venv | The gate used `uv pip install -e '.[dev]'`, which ignores `uv.lock`; the newest `pytest-benchmark` needs `py-cpuinfo2`. CI audits a separate `uv.lock` environment | a false failure, explained in the records |
| Eight ccsession PTY tests fail in a full run on this host | A LiteLLM shim runs on `127.0.0.1:4555` on this machine; the tests see it | a known host effect to explain in every gate record |

## 3. Proposals (in addition to the 6.0.0 list)

1. **Enforce the merge method.** A repository ruleset for `master` that allows only "merge commit" for pull requests, and a named list of who may merge a release PR. (Ryan's squash was a mistake any person could make.)
2. **Freeze `master` during the release window** (from the last review of the release PR until the tag), or have the orchestrator re-sync and re-run reviews when it moves. Say so in the release plan.
3. **The orchestrator watches the release PR for `MERGED` and for new commits on `master`**, and its status script prints `state`, `mergedBy` and the head SHA. "Unknown for more than two minutes" is checked, not assumed.
4. **Re-trigger Augment and Codex after any head change**, including a merge of `master` into the release branch, and say in the procedure that they do not re-run on a push.
5. **A pull request that changes a documented limit or default must search the docs for the old value** (here 365 days). Add the check to the pull request template and to the release preparation.
6. **Gate script in the repository** (as already proposed for 6.0.0), with these corrections from this release: run `make verify-deps` the way CI does (`UV_PROJECT_ENVIRONMENT=<separate venv>`), run in a clone, and list the host conditions that make known tests fail (a shim on port 4555, a running `claude` auto-update).
7. **Evidence scripts for post-release:** write the exit checks, the fingerprint coverage and the self-test modes first, run the full pipeline once, and check `git status --ignored` for the output folder before the first commit (`*.log` was silently dropped from the first commit in both releases). Count a review finding about such a script as non-blocking after the second round unless it shows a data or safety risk.
8. **Release PR created by a person:** if a person opens the release PR (as Ryan did with #664), the orchestrator says at once whether it takes it over, and for which tree it gates.
9. **Records branch:** keep the 6.0.0 rule (never merge a PR from it with `--delete-branch`); this release reused the same branch for two releases without trouble.

## 4. Open items for the owner (not process changes)

- #647 stays open for Clay to close; #571 stays open.
- #666 (typed confirmation before `ccsession --prune --apply`, Clay's answer to the `--classify` design question) is open and not part of 6.1.0.
- The two rules files that still name the old `/rf:taskbuilder` command (`rules/contextual/context_embedding.md`, `rules/prompts/agent_library.md`) belong to issue 572.
- Follow-ups listed in the 6.1.0 post-release report (`docs/testing/v6.1.0/post-release-report.md`, 18 gaps).
- `docs/releases/v6.1.0.md` in the repository says "Other pull requests ... #660, #661" and the GitHub release body has an "About this tag" section; `master` does not yet have the post-release documentation (it is on `integration`; it reaches `master` with the next release).
- Worktrees to remove later: `v61-merge-master`, `v61-post-release` (and the 6.0.0 list in `../v6.0.0/RELEASE-READINESS.md` section 7).
