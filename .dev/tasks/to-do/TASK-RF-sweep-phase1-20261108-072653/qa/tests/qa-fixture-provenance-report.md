# QA Report - Fixture Provenance Lens (T229)

**Date:** 2026-11-12
**Phase:** code-gate, fixture-provenance lens (fix_authorization: false)
**Scope:** tests/sweep/fixtures/ against readonly-probe.md

## Method

- Read `tests/sweep/fixtures/SOURCES.md` (43 lines) and every one of the 19 `captured-*.json` files; read `readonly-probe.md` sections 0, 1, 3, 4, 6, 7, 8, 10, 11, 13 and the Compliance/Deviations text in chunks of at most 150 lines.
- Wrote throwaway scripts under `/tmp/t229-prov/` (deleted at the end; no repository file touched). They (a) walked each fixture against the stored raw capture in `artifacts/readonly-probe-raw/` key by key, accepting only a difference that SOURCES.md rules 1 to 6 explain; (b) scanned every fixture for a leftover home path, account name, non-fake UUID, 32+ hex string, e-mail, IP, token word; (c) checked the fake-UUID numbering and the tab-map joins.
- Raw baseline check: `sha256sum` of `s1.json`, `m-t2-workerlist.json`, `b-tl-all.json` equals the hash recorded in `readonly-probe.md` lines 18, 465, 759; the five `b-ws-*.json` hashes start with the prefixes recorded at lines 481-485. The `a-*` files (used as the baseline) hold the same payload as the `b-*` files (probe lines 775-781, "Payload identical: yes").
- No live Orca, ccsession or Claude command was run. pytest was not re-run (not needed for this lens; `phase10-validation.md` records exit 0).

## Evidence summary

| Fixture | Compared against | Result |
|---|---|---|
| `captured-worker-list.json` | `readonly-probe-raw/s1.json` (probe sec. 0 and 3) | Same keys, types, row counts (5 workers, `counts` `{"released": 5}`, `page` limit 100 total 5). Every differing string is a home-path, UUID or account-name substitution. |
| `captured-worker-show-1..5.json` | `a-ws-ctx_*.json` (probe sec. 4), matched by `dispatch.id` | Same. No free-text key present, so none removed; `terminal.preview` kept; preview lengths equal the raw lengths (266, 248, 251, 300, 282). |
| `captured-task-list.json` | `a-tl-all.json` (probe sec. 5) | Same keys and types; `spec` (5 values) and the inner `result` strings over 80 characters (`body`, `reportPath`) are `<text removed>`; no replaced inner string was 80 characters or shorter; no inner string over 80 characters kept. |
| `captured-task-list-ready.json` | `a-tl-ready.json` | Identical apart from UUIDs. |
| `captured-run-current.json` | probe sec. 1, lines 447-449 | Same sentence, exit 0. |
| `captured-worker-list-unknown-run.json`, `captured-task-list-unknown-run.json` | probe sec. 8, lines 919-939, 949-959 | Bodies equal apart from envelope id and runtime id; exit 0 and 1 as recorded. |
| `captured-worktree-current.json` | probe sec. 7, lines 841-905 (full stdout) | Same after rules 1 to 3. |
| `captured-worktree-ps.json`, `captured-worktree-list.json` | probe sec. 6 and 7 (shape, counts, one redacted entry) | No raw stored; checked as far as the probe allows (see F6). |
| `captured-tab-map-1..5.json` | probe sec. 13 table, lines 1048-1052 | File name, session id and terminal handle map to the recorded real values; all 5 joins hold (below). |

Joins, checked for all 5 workers: `dispatch.assigneePaneKey` with `:` replaced by `+` equals the tab-map `file_name`; `dispatch.assigneeHandle` and `terminal.handle` equal tab-map `lines[2]`; the `claude --resume <id>` line in `terminal.preview` equals tab-map `lines[0]`. `worktreeInstanceId`, `repoId` and `runtimeId` agree across ps, list, current and the worker files.

Fake UUIDs: 54 distinct values, all of the form `00000000-0000-4000-8000-<12 digits>`, contiguous 1 to 54, and in first-seen order when the files are read worker-list, worker-show 1-5, task-list-ready, task-list, ps, list, current, unknown-run pair, tab-map 1-5. The real-to-fake mapping learned from 39 aligned pairs had no conflict (no real UUID with two fakes, no fake for two reals). No UUID-shaped string in the folder is non-fake.

## Findings

All findings are MINOR. None is BLOCKING or MAJOR.

### F1 (MINOR) Real path tails and a real project name survive; rule 2 misses `Coder`

- Evidence: `tests/sweep/fixtures/captured-worktree-ps.json:8,13,93,98,193,198` (`/home/user/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`, `/home/user/workspaces/Coder`, `/home/user/workspaces/worktrees/Coder/dashboard-bmad`), `:12,97,197` (`"repo": "IronClaude"` / `"Coder"`), `:14,199` (branches `refs/heads/ironbelly/...`); `captured-worktree-list.json:7,21,54,63,72,102`; `captured-worktree-current.json:6,20,53`; `captured-tab-map-1.json:7` (and the same line in tab-map 2 to 5: `.../IronClaude/issue-504`); every `captured-worker-*.json` `worktreeId`/`worktreePath`. A case-insensitive grep for `coder` finds 9 lines, all the word `Coder` (ps 93, 97, 98, 193, 197, 198; list 63, 72, 102).
- What is wrong: SOURCES.md rule 1 (line 7) replaces only the home prefix, so each path is a real path from the capture machine with a fake prefix. Rule 2 (line 8) replaces the account name "as a whole word"; `Coder` is a real folder name of another project and is not touched because the match is case-sensitive. Item 7.18's own check (`grep -rn '/home/coder\|coder'`) is case-sensitive and passes with these in place. No secret is exposed, and the same strings are already tracked in `readonly-probe.md`; but the lens statement "no fixture holds a real path" does not hold literally.
- Smallest fix: either say in SOURCES.md rule 1 that only the home prefix is sanitized and worktree/repo names are kept on purpose, or rename `Coder` and `dashboard-bmad` to neutral names in ps and list (both are never read by a test, see F5), and keep the one this-worktree entry that `_stock_captured` reads.

### F2 (MINOR) Task wording of other sessions is kept in `captured-task-list.json`

- Evidence: `captured-task-list.json:16-17, 33-34, 50-51, 67-68, 84-85` (`task_title` and `display_name` such as `"504 analyze: codegraph"`); the inner `result` strings keep `subject` (for example `"#504 analyze: codegraph support in /sc:analyze d..."`, 80 characters or fewer).
- What is wrong: SOURCES.md rule 5 (line 11) says free text that "could carry other sessions' conversation or task wording" is removed, but lists the key `taskTitle` (camel case); this file uses `task_title`, `display_name`, `subject`, which are not listed, so short task titles of issue 504 stay. Low risk (titles, not conversation).
- Smallest fix: add the three key names to rule 5 and replace them, or state in SOURCES.md that short titles are kept on purpose.

### F3 (MINOR) Terminal and session identifiers that are not UUIDs are kept, and rule 3 does not say so

- Evidence: `@@98e8ea49`, `@@846850e6`, `@@ff748a50`, `@@389ca4c5`, `@@773fac13` (pty and endpoint suffixes) at `captured-worker-list.json:22,98,174,250,326` and at lines 13, 161, 193 of each `captured-worker-show-N.json`; `@@jZX0PmCW` at `captured-task-list.json:14,31,48,65,82`; ccsession session labels such as `issue-504-1111-193642-2121` in `terminal.title` and `terminal.preview` of every `captured-worker-show-N.json`.
- What is wrong: rule 3 (line 9) promises that session ids, pane keys and terminal handles are replaced; these suffixes and labels are identifiers of the same kind that are left as captured, and rule 4 (line 10) does not list them as kept. They are not credentials: they match the shape of other Orca internal ids and carry no authority.
- Smallest fix: add them to rule 4 as kept ids, or replace them with a stable fake of the same length.

### F4 (MINOR) Wording in SOURCES.md that the files do not match exactly

- Evidence: SOURCES.md line 11 says the worker-show terminal preview is "266-300 character"; the measured preview lengths in the five files are 266, 248, 251, 300, 282 (raw lengths are the same). Line 11 also says the keys `comment` and `prompt` are replaced by `<text removed>`, yet `captured-worktree-ps.json:36,52,117,221`, `captured-worktree-list.json:28,79` and `captured-worktree-current.json:27` hold `""`; the raw `worktree current` stdout (probe line 867) is `"comment": ""` too, so the empty value was kept, not replaced. The table rows for `captured-worktree-list.json` and `captured-worktree-current.json` name Rule 5, but no value in those two files was changed by it.
- Smallest fix: write "248-300" and "empty values are kept as captured"; drop the Rule 5 mention from the list and current rows.

### F5 (MINOR) Seven fixtures are read by no test, and no test guards the folder

- Evidence: `mean_Grep` over `tests/sweep/*.py` finds a literal read only of `captured-worker-list`, `-task-list-ready`, `-task-list`, `-worker-show-{n}` (probes test lines 319-327, 1530), `-worktree-ps` (328), `-run-current` (probes 762; contract 451, 461), `-worker-list-unknown-run` and `-task-list-unknown-run` (contract 336-337). No test names `captured-tab-map-*`, `captured-worktree-list` or `captured-worktree-current`, and none lists the folder or reads `SOURCES.md`.
- What is wrong: these 7 files are provenance records only (SOURCES.md line 41 says Phase 1 does not call those templates), so nothing fails if one is edited or a real value is pasted in. The only guard is the one-time grep of item 7.18.
- Smallest fix: none required for the gate. Optional: one test that every `captured-*.json` parses, has a SOURCES.md row, and holds no `/home/` other than `/home/user`.

### F6 (MINOR, UNVERIFIABLE) `worktree ps` and `worktree list` entries 2 and 3 have no raw baseline

- Evidence: probe lines 789 and 834 say the raw bytes of both outputs were not stored. I could compare entry 1 of ps and the single entry of `worktree current` with the raw `worktree current` stdout (probe 841-905): `createdAt` 1794035783506, `sortOrder` 1794432910840, `lastActivityAt` 1794432847370, `liveTerminalCount` 3, `status` `working`, two agents `done` and `working`, `instanceId` and `repoId` all agree. For the other entries I could check only that every field named in probe lines 793 and 834 is present, that `totalCount` is 3 and 2 (captured 28), and that ps and list agree on `instanceId`, `sortOrder` and `lastActivityAt`.
- What is wrong: I cannot show that entries 2 and 3 are unaltered captured data (for example that the missing `createdAt` and `projectId` on the `Coder` entry in list, `captured-worktree-list.json:62-109`, are as captured). Nothing contradicts it.
- Smallest fix: none possible after the fact; the design choice not to store raw bytes (probe line 10) is the cause.

### F7 (MINOR, note) Hand-made data is inline, not a `synthetic` file

- Evidence: `grep -ci synthetic tests/sweep/*.py` gives 0. Hand-made Orca-shaped payloads are built inline: `tests/sweep/test_probes_allowlist.py:256-297` (`did`, `_rows`, `_show_result`, `_stock_run`) and the `SweepRoot` builders in `tests/sweep/conftest.py:172-324`, whose docstring (line 180-181) states none of them is a file under `tests/sweep/fixtures/`.
- Assessment: DESIGN section 11 line 754 ties the `synthetic` marker to file names, and the folder holds no hand-made file (SOURCES.md line 3), so the rule is met. The inline builders are not marked, so a reader of a test cannot tell a captured shape from an invented one except through the `_captured(...)` call.

## Not graded (outside this lens)

- `artifacts/readonly-probe-raw/*.json` and `readonly-probe.md` hold the unsanitized capture (real home path, real session ids, owner task text in `a-tl-all.json`); they are task-package files that are always staged by repository rule, so this is intended.
- `tests/sweep/__pycache__/scratch_explore.cpython-311-pytest-9.2.0.pyc` has no source file; `__pycache__/` is gitignored (`.gitignore:2`), so nothing is committed.
- `tests/sweep/` is untracked in git (`?? tests/sweep/`); staging is a later step.


## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | SOURCES.md has a row for every file in the folder and no row for a missing file (19 rows, 19 files, empty set difference) | PASS |
| C2 | The folder holds only `captured-*.json` and `SOURCES.md`; every hand-made fixture file carries `synthetic` in its name (none exists) | PASS |
| C3 | `captured-worker-list.json` equals raw `s1.json` apart from rules 1 to 3 | PASS |
| C4 | `captured-worker-show-1..5.json` equal raw `a-ws-*.json` apart from rules 1 to 3; preview kept | PASS |
| C5 | `captured-task-list.json` and `captured-task-list-ready.json` equal raw `a-tl-*.json` apart from rules 1 to 3 and 5 | PASS |
| C6 | `captured-run-current.json` and both unknown-Run fixtures equal probe sections 1 and 8 (bodies, exit codes) | PASS |
| C7 | `captured-worktree-current.json` equals probe section 7 full stdout apart from rules 1 to 3 | PASS |
| C8 | `captured-worktree-ps.json` and `captured-worktree-list.json` match the probe as far as it allows (fields, counts 28 to 3 and 2, cross-joins with raw current); entries 2 and 3 have no raw baseline | PASS (see F6, UNVERIFIABLE part) |
| C9 | `captured-tab-map-1..5.json` equal probe section 13 and join to worker-show on pane key, handle and session id for all 5 workers | PASS |
| C10 | Fake UUIDs: all 54 of the stated shape, contiguous, first-seen order, one fake per real value; no non-fake UUID left | PASS |
| C11 | No `/home/coder`, no lower-case `coder`, no real UUID, no real Claude session id, no e-mail, IP, token or key string in any fixture or in SOURCES.md | PASS |
| C12 | No real path or other-project name left in a fixture | FAIL (F1, MINOR) |
| C13 | Every sanitization statement in SOURCES.md (rules 2 to 5, preview length, Rule 5 per row) matches the files | FAIL (F2, F3, F4, MINOR) |
| C14 | SOURCES.md per-file facts (probe section, command template, exit code, row and task counts, array cuts and `totalCount`, wrapper keys) match the probe and the files | PASS |
| C15 | Hand-made data in tests is marked `synthetic` where the design requires it (file names, DESIGN section 11 line 754) | PASS (F7 note) |
| C16 | Every captured fixture is exercised by a test and a test guards the folder | FAIL (F5, MINOR) |

Verdict: PASS

Blocking count: 0
