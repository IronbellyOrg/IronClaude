# D: PR #686 against the code and design documents on master

Lens: master code and design docs versus what PR #686 adds and removes. Read-only; every claim comes from `git show`, `git diff`, `git grep` on `origin/master` (d7d645ddd) and `origin/pr-686` (4e7f12b1a), plus one `gh pr view 681`.

## Summary

1. PR #686 is not a new idea. It is "PR A: poll core" of the owner-approved design `docs/designs/orchestrator.md`, already on master (merged by PR #681 on 2026-11-20; `gh pr view 681`: MERGED, one added file, 1,412 lines). Section 8.1 of that design lists PR A's files, acceptance tests and the 62-reason table, and the PR follows it closely.
2. It rewrites in place the existing `src/superclaude/cli/issue_watch/` package (9 files on master) and reuses its runner, audit log, store, call budget and rate-limit code. It adds four new modules: `wake.py`, `route.py`, `hold.py`, `repos.py`.
3. What it removes (approval, claim marker, edit history, Project board reads, `orca agent launch`) is the plan-approval gate that PR D (#682, merged, `01e7a9e23`) already retired. Master has no `issue_pipeline` directory under `src/superclaude/cli/`.
4. One real duplication: `wake.py` copies about 100 lines of `src/superclaude/skills/agent-work-report/scripts/orca_term.py`, which is on master (PR C, #684). The design chose this on purpose (4.10 row `wake.py`, section 11).
5. Observer (`cli/observe/`) and sweep (`cli/sweep/`) cannot see the PR's registry or wake files. They read Orca's own state through `orca orchestration ...`. The PR is a separate file island, neither a rival nor a duplicate of either.
6. Nothing on master reads `orchestrator-wake/1` yet: the `superclaude orchestrator` verbs and the skill are PR B. The PR writes and parses the format, but no orchestrator exists to acknowledge it.

## What the PR really does

It changes the watcher from "claim an issue, launch a worker session, wait for an approval comment" to "route a new assigned issue to a per-repo orchestrator and wake it".

- `repos.py` (395 new lines): reads and validates `repos.yaml` of an external orchestrator repo with `yaml.safe_load`. Knows `plan_tier`, `worker_tier`, `orchestrator_tier` (defaults tier1b, tier2, tier1b), reads the allowed tiers from `ccsession --help`, fallback order `TIER_ORDER`, `max_in_flight` default 3.
- `route.py` (603 new): the registry `.orchestrator/orchestrators.json` (written only by the poll), reads of `.orchestrator/runs/<id>.json` and `.orchestrator/issues/*.json` (written by orchestrators, read only by the poll), the in-flight count, routing under `.orchestrator/state.lock`.
- `hold.py` (276 new): `plan_check(body)` (three sections `## Priority`, `## Fix approach`, `## Test plan`), the six-row decision table, hold transitions, Orca evidence reads. Labels `hold:plan` and `hold:backlog` are constants in PR `predicates.py:30,33`.
- `wake.py` (1,009 new): wake file schema `orchestrator-wake/1` (64 KiB cap), strict parser, ack reader (`orchestrator-wake-ack/1`), and `Waker`. Delivery: `orca orchestration send --to run:<id> --type status` (PR `wake.py:826`), a typed line into an idle Claude terminal found by process and ccsession tag, or `ccsession <tag> --tier <tier>` in a new terminal.
- `cycle.py` (+1,472/-652): reordered per design 4.5; `_wake` replaces `_launch`; hold step, resend of unacknowledged wakes, plan requests.
- `github.py` (+535/-426): search-based discovery, label writer, evidence reads; events, marker, edits and Project (GraphQL) readers removed.
- `record.py` (+553/-300): schema 2 (`pending, woken, acked, unknown, failed, abandoned`, `wake_id`, `holds`).
- `audit.py`, `predicates.py`, `launch.py`, `cli.py`: reason table 59 to 62 (`tests/issue_watch/test_audit.py:78-79` pins 62); approval predicates gone; `build_claim_prompt`, `launch_argv`, `retry_argv` replaced by `build_wake_line` and `session_command`.
- Files touched outside `src/superclaude/cli/issue_watch/` and `tests/issue_watch/`: only `CHANGELOG.md`. `main.py` is unchanged (`issue-watch` group at master `main.py:577-579` stays).

## Reused versus new

| Building block | Status | Evidence |
|---|---|---|
| `runner.py` (`Runner`, `CommandResult`), `find_orca`, `parse_origin`, `check_origin`, `LaunchOutcome`, `Launcher` | Reused, lightly reshaped | PR imports `.runner`; PR `launch.py:152,204,222,248,270` |
| `install_user_setup._ORCA_CLIS` | Reused import | PR `launch.py` imports |
| Audit log, `Store`/`FileStore`, lock, backoff, lease, `CallBudget`, rate-limit and error classification, `Deadline`, dry-run files | Reused (design 4.10 "keep") | `cycle.py`, `record.py`, `github.py` still carry them |
| Orca CLI: `terminal list/send/wait/create`, `orchestration send` | Reused through the runner | PR `wake.py:713,786,805,826` |
| ccsession `--tier` and its `--help` tier list | Reused as external CLI | PR `repos.py`, `launch.py:111` |
| `orca_term.py` session lookup logic | Copied, not imported | PR `wake.py:9,603-622`; master `skills/agent-work-report/scripts/orca_term.py` (`claude_processes` line 34, `find_session` 61, `send` 124) |
| Observer, sweep, `.dev/coordinators/` | Not used | no `observe` or `sweep` import in added source lines; `.dev/coordinators/` does not exist on master (only `.dev/coordinator/` state of the report skill, and nothing in the PR reads it) |
| `wake.py`, `route.py`, `hold.py`, `repos.py` | New | 2,283 lines, no deletions |
| `.orchestrator/{orchestrators.json,runs,issues,wakes}` layout | New on disk | `git grep` for `orchestrators.json`, `.orchestrator/`, `orchestrator-wake` in master `src` and `tests`: no hits |
| `hold:plan` label, `plan_requests[]`, plan records | New | no `hold:plan` or `hold:backlog` on master src or tests |
| Golden `orchestrator_wake_golden.json` (64 lines) | New; shared with PR B by design | design 3.7, 9.1 |

## Overlap with master

| Idea | Master path | PR #686 path | Verdict |
|---|---|---|---|
| Session lookup by process and tag, idle check, typed send | `skills/agent-work-report/scripts/orca_term.py` | `issue_watch/wake.py:603-960` | Duplicate on purpose (design 4.10, section 11); consolidation is a follow-up |
| A waker that types a fixed line into a session | `skills/agent-work-report/scripts/waker.py` (morning wake of the report session) | `wake.py` `Waker.deliver` | Same pattern, different target (report session versus per-repo orchestrator); complementary |
| Claim then launch a session | `issue_watch/launch.py` (`launch_argv`, `build_claim_prompt`, `retry_argv`), `cycle.py` (`_launch`, `_claim`, `_approve`) | replaced by `wake.py` and `_wake` | Supersedes; old path never ran live (`issue-watcher.md` banner) |
| Plan-approval gate | `issue_pipeline/` (deleted by PR D) | approval rules removed from `predicates.py` | Finishes the retirement |
| Orchestrator or coordinator registry | none on master | `route.py` | New |
| Hold label and plan check | none | `hold.py`, `hold:plan` | New; the `/sc:issue` plan mode that fills the sections is PR P, not on master |
| Tier configuration | `skills/ccsession-tag/ccsession-models.json` (profiles claude, gpt, grok, muse), `ccsession` tier mode | `repos.py` tier names | Uses ccsession's tier list; does not read `ccsession-models.json` (no hit in added lines; I did not read all of `repos.py`, so UNVERIFIED) |
| Report state of orchestrated issues | `skills/agent-work-report/scripts/exclude.py`, `common.py` (`.dev/coordinator/orchestrated/` entries; `POLL_CONFIG = ~/.config/superclaude/issue-watch.json`, key `orchestrator_repo`) | PR keeps the `orchestrator_repo` config key | Master's report skill already expects the poll's config and PR B's entry files. The PR is the poll side of that contract |
| Worker contract | `core/WORKER-CONTRACT.md` | untouched | PR B territory |

## Is it connected to the observer and sweep

No, at the level of file formats and readers.

- Observer: `cli/observe/adapter.py:29,32` runs `orca orchestration worker-list --json --limit 100` and `orca orchestration check --all --types question`. It reads Orca Runs, not files. `observe/` has no mention of `.orchestrator`, `wake`, `issue_watch` or `orchestrators.json`.
- Sweep: `cli/sweep/probes.py:50-54,1150-1282` reads `orchestration run-current`, `worker-list`, `task-list`, `worker-show`. Orca state only.
- The PR changes neither and adds no reader of its files to either.
- Indirect visibility only: once PR B starts orchestrators as Orca Runs with workers, both tools will list those Runs like any other, and the mailbox message `orchestration send --to run:<id>` lands in that Run. That depends on PR B: UNVERIFIED.
- The registry, wake files and plan records are read only by the poll, later by the PR B orchestrator CLI, and (entry files, a different folder) by the report skill. A separate island.

## Design documents

- `docs/designs/orchestrator.md` (master, from #681; status line: approved by the owner 2026-11-19, ruling 37). Section 4.10 is a symbol-by-symbol keep, reshape or remove table; 8.1 lists PR A's files and acceptance checks. The PR matches them: four new modules; `build_claim_prompt` to `build_wake_line`; 62 reasons (4.7: 59 - 14 - 5 + 5 + 17 = 62, mirrored at `test_audit.py:98`); schema 2; `.orchestrator/orchestrators.json` (5.7); `hold:plan` (4.11).
- Follows: closed reason table, one orchestrator per repo with `max_in_flight` 3, mailbox plus typed line plus session start, no GitHub text in a typed line (3.7), three tier keys (5.8).
- Departs, flagged by the PR itself: the `repos.py` docstring says it resolves a conflict between design 4.4 ("accepts only a listed tier") and 5.8 ("an unlisted tier falls once") and raises a question for the owner. A documented reading, not a contradiction of intent.
- Design 8.1 also expects PR A to include the `status` output of held issues, the updated golden wake file and a fake-runner end-to-end test (four issues of one repo give two wakes). I did not verify each in the test files: UNVERIFIED.
- `docs/designs/issue-watcher.md` (older design, #331): banner says "Implemented and merged in PRs #447 and #448; never run live; `enabled` ships as `false`". The PR rewrites that implemented code. Banner updates on the older design docs are PR E, not this PR (8.1).
- `WORKER-CONTRACT.md` on master: the first lines I read describe the coordinator and workers; a grep for "issue pipeline" found nothing in the lines shown, consistent with PR D removing WC-17 and its section, but I did not read the whole file: UNVERIFIED. The new "Orchestrated issue flow" section is PR B.

## Line counts

`git diff --numstat origin/master...origin/pr-686` (59 files, +14,256 / -16,637):

| Class | Added | Deleted |
|---|---|---|
| New source modules (`wake`, `route`, `hold`, `repos`) | 2,283 | 0 |
| Rewritten source (`cycle`, `github`, `record`, `launch`, `predicates`, `audit`, `cli`) | 3,060 | 1,822 |
| New test files (`test_wake`, `test_route`, `test_hold`, `test_repos`, `test_fixtures`) | 3,138 | 0 |
| Rewritten existing test files | 5,402 | 14,647 |
| Fixtures (`_assumed_shape/*`, golden wake) | 369 | 168 |
| CHANGELOG | 4 | 0 |
| Total | 14,256 | 16,637 |

About 88 percent of the deleted lines (14,647 of 16,637) are legacy tests of the retired claim flow; source deletions are 1,822. New production code is about 5.3k lines (2,283 new plus 3,060 added in rewrites); test code added is about 8.5k (3,138 plus 5,402). Biggest deletion: `test_cycle.py` (+884/-4,692). Biggest additions: `cycle.py` (+1,472), `test_hold.py` (1,055), `test_wake.py` (1,052), `wake.py` (1,009). Net -2,381.

## Caveats

I did not run tests or read PR `cycle.py` in full; "reused" comes from header imports, greps and the design's keep table. The items marked UNVERIFIED above were not read in a source.
