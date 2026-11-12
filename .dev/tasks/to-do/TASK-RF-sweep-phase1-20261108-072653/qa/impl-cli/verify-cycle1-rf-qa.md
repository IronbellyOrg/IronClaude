# QA Report - Verify Cycle 1 (rf-qa)

**Topic:** sweep Phase 1 impl-cli, re-check after fix-log-cycle1 (items 9.14)
**Date:** 2026-11-12
**Phase:** fix-cycle (verification of F_0 = CLI-F1, CLI-F2 and the cycle-0 PASS set)
**Fix cycle:** 1
**fix_authorization:** false (report is the only file written)

**Package folder:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/`
**Files written:** this report only. No live Orca command was run and `superclaude sweep run` was never pointed at the real Orca. Scratch runs used a fake Orca script, a throwaway `git init` root, and `HOME` / `XDG_STATE_HOME` inside private `/tmp/vc1-scratch.*` folders; each folder was deleted by an exit trap (`CLEANUP_OK ... gone` printed three times).

## Overall Verdict: PASS

CLI-F1 and CLI-F2 are RESOLVED. All 147 check ids of the cycle-0 PASS set still PASS. I found no new BLOCKING or MAJOR finding. Blocking count is 0, so `|F_1| = 0 < |F_0| = 2` (monotonicity holds) and no PASS-set id regressed.

## Evidence bases used in the Checks table

| Code | Meaning |
|---|---|
| RE | Re-executed by me in this review (scratch id in brackets, or command named) |
| UN | Not re-executed (a cycle-0 scratch case that cannot be re-run, or code path outside the fix). Confirmed from disk that nothing the check relied on was changed by the fix: see E1 |
| AR | Saved artifact or record; confirmed unchanged on disk (E6) |

| Id | Evidence |
|---|---|
| E1 | `stat` mtimes. Newest of `commands.py` (03:09:43), `models.py` (02:41:03), `report.py` (02:42:35), `__init__.py` (01:14:42), `main.py` (03:10:56), `tests/sweep/*` (02:20:19 at latest), DESIGN `docs/designs/orchestrator-mode.md` (11-09 14:15:47), OQ-2 and OQ-5 records (11-09), `step-1.7-help.txt` (03:11:02) and the first live-check artifacts (03:11 to 03:13) is earlier than the first cycle-0 report (`qa-registration-report.md`, 03:23:26). Only `classify.py` (03:36:57) and `probes.py` (03:37:25) are newer than the cycle-0 reports. `git diff -- src/superclaude/cli/main.py` still shows the same 4 added lines (`main.py:567-569`). |
| E2 | The fix hunks read in full: `classify.py:961-977` (summary dict) and `probes.py:316-349` (`_LIST_KEY`, `_call`). Nothing else in those files was changed by the fix (fix log); the unchanged lines I spot-read agree with the cycle-0 citations (`probes.py:41-58`, `:203-221`, `:243-313` (`_orca`, `_git`) and `classify.py:197`). Lines after `probes.py:316` moved by +16 (for example `_ledger` was `:572-584`, now `:588-600`; `_contract_candidates` was `:1001`, now `:1017`; the three `open(..., "rb")` were `:559,:810,:874`, now `:575,:826,:890`). A moved line number on a true claim is minor and does not change any result. |
| E3 | `uv run pytest tests/sweep -v`: 4 passed. `uv run ruff check src/superclaude/cli tests/sweep`: `All checks passed!`. `uv run ruff format --check src/superclaude/cli/sweep src/superclaude/cli/main.py tests/sweep`: `11 files already formatted`. `sweep --help`, `sweep run --help`: exit 0, stderr 0 bytes, byte-identical to `step-1.7-help.txt` lines 5-13 and 19-31. `superclaude --help`: exit 0, stderr 0 bytes, lists `sweep`. `tests/unit` was not run (285 s, excluded by the prompt). |
| E4 | Package greps after the fix: write calls (`os.unlink/write/fsync/makedirs/open/link`) only in `commands.py` lines 140, 149, 150, 158, 170, 186, 203 (the cycle-0 list); `subprocess` start only at `probes.py:248` and `:299`; `open(` only the three `"rb"` reads; zero `run-list`, zero `superclaude.cli.main` imports in `sweep/`; `--include-remote` appears only as the forbidden token (`probes.py:60`); `sys.exit` only at `commands.py:281,285,288`. |
| E5 | Scratch fake-Orca runs of the real command. Part 1 (A1-A15, `--run`): A1 real captured shapes, A2 empty lists, A3 `{"ok":true,"result":{}}` for every verb, A4/A5/A6 `workers` string, null, dict, A7 `tasks` missing, A8 `tasks` string, A9/A10 `worktrees` missing, string, A11 unknown-Run shape (`worker-list` empty, `task-list` exit 1), A12 exit 1, A13 empty body, A14 plain text, A15 `runtime_unavailable`. Part 2 (B1-B9): B1 real shapes with classes and argv count, B2 binary missing, B3/B4/B5 `run-current` exit 1, empty, `runtime_unavailable`, B6 no binding, B7 bound and empty lists, B8 bound but wrong-shape `worker-list`, B9 hang. Part 3 (C1, X2, E1 and python probes): two Runs with the first unknown, five exit-2 inputs, `.dev/sweeps` is a file, four same-second `_publish` calls, eight hostile Orca argvs, git allowlist. |
| E6 | Artifact check. `sweep-live-check-1.4.json` (03:12:44, 319791 bytes, 12 top-level keys), `-workers.json`, `.md`, the OQ records and the first report `.dev/sweeps/20261112-031239-sweep.md` (605 lines, last line `Report complete`) all exist with their cycle-0 mtimes. The executor's re-run `sweep-live-check-1.4-rerun-9.14.json` (03:45:16) has the same 12 keys, the same 71 source rows (non-transcript source names identical), 0 unscanned, `orca_available` true, the five Orca worker rows identical to the first record (same class, rule and notes: md5 `77d33ae6...` for both), and `total` 182 against 180 (two more live session rows). |

## Findings: F_0 re-check

### CLI-F1 (MAJOR): RESOLVED

- Fix location: `src/superclaude/cli/sweep/classify.py:976` (`"total_is_lower_bound": True,`), with the `shortcut:` comment at `:973-975` inside the `summary` dict that starts at `:967`. The unused local `unscanned` was removed with it (no other reader of it exists: `grep unscanned classify.py` shows only note/source uses at `:83-86`, `:695-710`, `:819-863`).
- Consumer path unchanged: `report.py:670` copies `summary["total_is_lower_bound"]` into the JSON. The report keeps printing the lower-bound wording unconditionally at `report.py:178` (header) and `report.py:510` (What I could not determine). Both outputs now say "lower bound" in every run.
- Evidence now: the executor's re-run JSON has `summary.total_is_lower_bound` true (first record: false), and its report `.dev/sweeps/20261112-034511-sweep.md:2` reads `sessions 182/182 (lower bound: remote hosts not scanned)` and `:534` reads `Remote hosts were not scanned; the session count is a lower bound`. All 19 of my scratch runs that produced a JSON (A1-A15, B1, B7, B8, C1; B2-B6 and B9 exit 2 with no JSON) printed `lb=true`; the report from B1, B7 and B8 holds 2 `lower bound` mentions each. SPEC FR-005 (`merged-requirements.md:99`: "Totals that cannot be known are shown as lower bounds") supports the constant.
- Note, not a finding (minor, wording): DESIGN 7.4 (`docs/designs/orchestrator-mode.md:346`) still says the flag is true "when any list is truncated (a full 100-row page) or unscanned". The constant is a superset of that rule, so it is not contradicted, but the row should be reworded in a later design pass (the fix agent already passed this note to the coordinator).

### CLI-F2 (MAJOR): RESOLVED

- Fix location: `src/superclaude/cli/sweep/probes.py:316-321` (`_LIST_KEY`: `worker-list` to `workers`, `task-list` to `tasks`, `worktree ps` to `worktrees`) and `:332-339` (in `_call`, an `ok` result whose list key is not a list becomes `OrcaResult("call_failed", None, "orca call failed (invalid response)")`). The existing first-call rule at `:346-348` then turns a first-call failure into `unavailable`. `_orca` itself (`:243-286`) is untouched.
- Captured shapes still pass: `tests/sweep/fixtures/captured-worker-list.json`, `captured-worker-list-unknown-run.json` (`workers` is an array, empty for the unknown Run), `captured-task-list.json`, `captured-task-list-ready.json` (`tasks` array) and `captured-worktree-ps.json` (`worktrees` array) all hold the key as a list. Scratch A1 (real captured shapes) gave `avail=true`, 9 argvs, 5 rows, all sources `read`.
- Scratch results for the wrong shapes (all exit 0, stderr empty, one report):

| Case | Result |
|---|---|
| A3 `{"ok":true,"result":{}}` for every verb (the cycle-0 B7 case) | `orca_available` false; `worker-list` `unscanned: orca call failed (invalid response)`; the other three Orca sources `unscanned: orca unavailable` |
| A4, A5, A6 `workers` string, null, dict | same as A3 |
| A7 `tasks` missing, A8 `tasks` a string | `orca_available` true; both `task-list` rows `unscanned: orca call failed (invalid response)`; `worker-list` and `worktree ps` `read` |
| A9 `worktrees` missing, A10 `worktrees` a string | `orca_available` true; `worktree ps` `unscanned: orca call failed (invalid response)`; the rest `read` |
| B8 `run-current` ok, then `worker-list` `{}` | `orca_available` true (first-call rule not applied because `run-current` was call 1); `worker-list` row `unscanned` with the invalid-response reason |
| A2 well-formed empty lists | `orca_available` true, all four sources `read`, 0 rows (an empty list is still accepted) |

- Unchanged behaviours re-checked alongside: A12-A15 (exit 1, empty body, text, `runtime_unavailable` on call 1) still give `orca_available` false with the reason on `worker-list`; A11 unknown-Run shape still reads `worker-list` and marks both `task-list` rows `unscanned: orca call failed (exit 1)`; C1 with two Runs (first unknown) issues exactly 7 argvs and still reads the second Run.
- Minor, not a finding: no durable test pins the new check (scheduled for Phase 10 per the fix log; `tests/sweep/` still holds only `test_readonly.py`, 4 passed).

## New findings

None at BLOCKING or MAJOR. Notes only (minor, none triggers a fix pass):

| Id | Note |
|---|---|
| N1 | DESIGN 7.4 flag wording is narrower than the code (see CLI-F1). Reword in a later design pass. |
| N2 | `.dev/sweeps/` now holds four reports, not three: the fourth (`20261112-034511-sweep.md`, 609 lines, ends `Report complete`) is the executor's recorded 9.14 re-run, not a side effect of the fix. The three cycle-0 reports are unchanged. |
| N3 | A first Orca reply that is JSON but has the wrong list shape now counts as unavailable (A3-A6), the same as non-JSON text (A14). That is what SPEC section 8 asks for, but a reader may expect `call_failed` only. No action. |
| N4 | MINOR findings CLI-F3 to CLI-F37 were left alone by the fix agent. Their `file:line` citations into `probes.py` after line 316 have moved by +16; the defects themselves are unchanged and remain notes. |

## Checks

One row per id of the 147-id cycle-0 PASS set (`<report name>:C<n>`). Basis codes and E-ids are defined above.

| Check id | Result | Basis | Note |
|---|---|---|---|
| qa-failure-path-report:C1 | PASS | RE | B2-B5, X2: exit 2, reason in message, only `run-current` issued, nothing created |
| qa-failure-path-report:C2 | PASS | RE | B9: exit 2 after 10 s, `Orca unavailable (timeout after 10 s)` |
| qa-failure-path-report:C3 | PASS | RE | B6: `no Run bound: pass --run <id>`, exit 2 |
| qa-failure-path-report:C4 | PASS | RE | A12-A15: exit 0, one report, `orca_available` false, reason in Source coverage |
| qa-failure-path-report:C5 | PASS | RE | A7-A11, B8: later failure is `call_failed`, `orca_available` stays true |
| qa-failure-path-report:C6 | PASS | RE | A2: empty lists accepted, all sources `read`, 0 rows (the new shape check does not reject them) |
| qa-failure-path-report:C8 | PASS | RE+UN | X2 `--root` without `.git`: `invalid --root:` exit 2; the walk-up wording is in unchanged `commands.py` (E1) |
| qa-failure-path-report:C9 | PASS | RE | X2 five exit-2 inputs: `.dev` not created, 0 Orca argvs |
| qa-failure-path-report:C10 | PASS | RE+UN | E1: `.dev/sweeps` is a file gives exit 1, `[sweep publish] [Errno 17] File exists`, stdout 0 bytes; read-only folder case UN |
| qa-failure-path-report:C11 | PASS | UN | injected write/fsync/link/close failures not re-run; `commands.py:137-208` unchanged (E1) |
| qa-failure-path-report:C12 | PASS | RE+UN | four same-second `_publish` calls gave `-sweep`, `-2`, `-3`, `-4`; 99-name exhaustion UN |
| qa-failure-path-report:C13 | PASS | UN | `commands.py:168-172` unchanged |
| qa-failure-path-report:C14 | PASS | UN | `commands.py:202-207` unchanged |
| qa-failure-path-report:C15 | PASS | UN | `commands.py:161-164` unchanged |
| qa-failure-path-report:C16 | PASS | UN | `commands.py:276-288` and `report.py` unchanged |
| qa-failure-path-report:C17 | PASS | UN | `_publish` unchanged; E1 case left no report name |
| qa-failure-path-report:C18 | PASS | UN | Ctrl-C case is a cycle-0 scratch; `commands.py:175-196` unchanged |
| qa-failure-path-report:C20 | PASS | RE+UN | `sys.exit` only at `commands.py:281,285,288` (E4); `_publish` and DESIGN 7.1 unchanged |
| qa-failure-path-report:C21 | PASS | RE | `git diff -- main.py`: the same 4 added lines, `main.py:567-569` |
| qa-failure-path-report:C22 | PASS | RE+AR | help text identical, ruff clean, `tests/sweep` 4 passed (E3); first live-check JSON unchanged, 12 keys (E6) |
| qa-failure-path-report:C23 | PASS | RE | help `[default: 6h]`; `git check-ignore` gives `.gitignore:256:.dev/sweeps/`; report name `20261112-035221-sweep.md` (UTC pattern) |
| qa-input-edge-report:C1 | PASS | RE+UN | X2 `--run BAD` exit 2; `--run ''` UN, `commands.py:87-92` unchanged |
| qa-input-edge-report:C2 | PASS | RE | X2 `--run BAD`: exit 2, nothing written, 0 argvs |
| qa-input-edge-report:C3 | PASS | UN | `_check_run_ids` unchanged |
| qa-input-edge-report:C4 | PASS | UN | `RUN_ID_RE` at `probes.py:44` unchanged |
| qa-input-edge-report:C5 | PASS | RE | X2 window, run id, output and root errors each issued 0 Orca argvs |
| qa-input-edge-report:C6 | PASS | RE | C1 scratch: two Runs, first unknown shape: 7 argvs, `worker-list` read, both `task-list` rows `unscanned: orca call failed (exit 1)`, second Run read, exit 0 |
| qa-input-edge-report:C8 | PASS | RE | B2-B7: unavailable, no-binding and success paths |
| qa-input-edge-report:C9 | PASS | RE | A12-A15: explicit `--run`, first call fails, report published, exit 0 |
| qa-input-edge-report:C10 | PASS | RE+UN | X2 `--window 7m` exit 2; help `[default: 6h]`; `_parse_window` unchanged |
| qa-input-edge-report:C11 | PASS | UN | walk-up in `commands.py:64-70` unchanged |
| qa-input-edge-report:C13 | PASS | RE+UN | X2 `--root` without `.git`: `invalid --root:`; other root forms UN |
| qa-input-edge-report:C15 | PASS | UN | `_check_output` unchanged |
| qa-input-edge-report:C16 | PASS | RE+UN | X2 `--output /tmp` and `--output <root>/.dev/tasks`: exit 2, nothing written |
| qa-input-edge-report:C17 | PASS | UN | overlap guard in `commands.py` unchanged |
| qa-input-edge-report:C18 | PASS | UN | escape-after-`makedirs` is a cycle-0 injected case; `commands.py:158-164` unchanged |
| qa-input-edge-report:C20 | PASS | RE | X2: `.dev` not created in all five exit-2 runs |
| qa-input-edge-report:C21 | PASS | RE | four same-second publishes, UTC name pattern |
| qa-input-edge-report:C22 | PASS | RE | `main.py` diff unchanged; `sweep --help` and `sweep run --help` identical to `step-1.7-help.txt` |
| qa-input-edge-report:C23 | PASS | AR | first live-check record: `window` `6h`, report under `.dev/sweeps/`, one JSON object; unchanged (E6) |
| qa-interface-exit-report:C1 | PASS | UN | signatures in `commands.py` and DESIGN 7.1 unchanged (E1) |
| qa-interface-exit-report:C2 | PASS | RE | `main.commands["sweep"].name` `sweep`, subcommands `['run']` |
| qa-interface-exit-report:C3 | PASS | RE | `sweep run --help` lists `--run`, `--window`, `--root`, `--output` |
| qa-interface-exit-report:C4 | PASS | RE | help `[default: 6h]` and `Default: <root>/.dev/sweeps/.`; OQ records unchanged |
| qa-interface-exit-report:C5 | PASS | RE | `DEFAULT_WINDOW` only at `commands.py:27,228`; the two fix hunks hold no window constant |
| qa-interface-exit-report:C6 | PASS | RE | C1 scratch: `20261112-035221-sweep.md`; `.gitignore:256` matches |
| qa-interface-exit-report:C7 | PASS | RE+UN | X2 `7m` exit 2; accept/reject list UN, `_parse_window` unchanged |
| qa-interface-exit-report:C8 | PASS | RE+UN | X2 `--root`, `--output /tmp`, `.dev/tasks` exit 2 with stdout empty |
| qa-interface-exit-report:C9 | PASS | RE | X2 `--run BAD`: `invalid --run value: BAD` |
| qa-interface-exit-report:C10 | PASS | RE | X2: exit 2, stdout 0 bytes, message only |
| qa-interface-exit-report:C11 | PASS | RE | B6 `no Run bound: pass --run <id>`; B3-B5 `Orca unavailable (<reason>); ...`; stdout empty |
| qa-interface-exit-report:C12 | PASS | UN | stubbed `ValueError` cases are cycle-0 scratch; `commands.py:276-288` unchanged |
| qa-interface-exit-report:C13 | PASS | UN | stage labels in `commands.py` unchanged |
| qa-interface-exit-report:C14 | PASS | RE+UN | E1: `[sweep publish]` prefix, exit 1; the other seven injected modes UN |
| qa-interface-exit-report:C15 | PASS | RE | `sys.exit` only at `commands.py:281,285,288` (E4) |
| qa-interface-exit-report:C16 | PASS | RE | C1 scratch: exit 0, stdout one JSON (`jq -s length` 1, one trailing newline), stderr empty, one report |
| qa-interface-exit-report:C17 | PASS | RE | X2: nothing created after exit 2 |
| qa-interface-exit-report:C18 | PASS | UN | post-commit failures: `commands.py:202-207,276-288` unchanged |
| qa-interface-exit-report:C19 | PASS | RE | main diff 4 insertions; `main.commands` last two `issue-watch`, `sweep`; top help lists `sweep` |
| qa-interface-exit-report:C20 | PASS | RE | help identical; ruff check and format clean (E3) |
| qa-interface-exit-report:C21 | PASS | RE | `tests/sweep` 4 passed; ruff lines match `phase9-validation.md` |
| qa-interface-exit-report:C22 | PASS | AR | first JSON: 12 keys, `window` `6h`, 71 sources, 0 unscanned; `probes.py:49` still holds the `worker-list` template |
| qa-live-check-report:C1 | PASS | AR+UN | exit-0 path in `commands.py:274-288` unchanged; first JSON and 605-line report present |
| qa-live-check-report:C2 | PASS | AR+RE | first JSON `collected` 03:12:39Z to 03:12:44Z, 0 unscanned; B1 scratch with real shapes issues 9 argvs over the same four verbs |
| qa-live-check-report:C3 | PASS | AR | first JSON unchanged; the re-run also has every row classed (182 rule `fallback`) |
| qa-live-check-report:C4 | PASS | AR+RE | rule code unchanged except the summary dict (`classify.py:197` unchanged); the re-run's five worker rows are identical to the first record (E6) |
| qa-live-check-report:C5 | PASS | AR | note texts in the first JSON unchanged; re-run has 0 unscanned |
| qa-live-check-report:C6 | PASS | RE | `probes.py:49` template unchanged; no `--include-remote` (E4) |
| qa-live-check-report:C7 | PASS | AR | `-workers.json` unchanged (03:11:44) |
| qa-live-check-report:C8 | PASS | AR | transcript sizes are filesystem facts the fix cannot alter |
| qa-live-check-report:C9 | PASS | AR | saved worker list and first JSON unchanged |
| qa-live-check-report:C10 | PASS | AR+RE | `_contract_candidates` now at `probes.py:1017` (moved +16, same body role); `a-tl-all.json` unchanged |
| qa-live-check-report:C11 | PASS | AR | first report 605 lines, last line `Report complete`; four reports on disk now (N2) |
| qa-live-check-report:C12 | PASS | RE | `.gitignore:256` matches; default folder and name pattern from C1 scratch |
| qa-live-check-report:C13 | PASS | RE | help default 6h; first JSON `window` `6h` |
| qa-live-check-report:C14 | PASS | UN | `commands.py:242-288` unchanged |
| qa-live-check-report:C15 | PASS | RE | main diff unchanged; `sweep run --help` exit 0 |
| qa-live-check-report:C16 | PASS | RE | ruff check and format and `tests/sweep` re-run (E3); `tests/unit` not re-run |
| qa-live-check-report:C17 | PASS | RE | E4: no new write or process start, forbidden tokens absent |
| qa-live-check-report:C18 | PASS | RE | `_ledger` at `probes.py:588-600` keeps the `FileNotFoundError` branch returning `False, None` |
| qa-live-check-report:C19 | PASS | AR | 320 KB JSON (319791 bytes) and the retained-problem figures are saved facts |
| qa-live-check-report:C20 | PASS | AR | `issue-504` row data in the first JSON unchanged |
| qa-operator-output-report:C1 | PASS | RE | C1 and B7 scratch: one JSON object, one trailing newline, stderr empty |
| qa-operator-output-report:C2 | PASS | AR | first JSON: 12 keys, `schema_version` 1, 319791 bytes |
| qa-operator-output-report:C3 | PASS | RE | X2: exit 2, stdout 0 bytes |
| qa-operator-output-report:C4 | PASS | RE | E1: exit 1, stdout 0 bytes |
| qa-operator-output-report:C5 | PASS | RE | E1: stderr starts `[sweep publish]` |
| qa-operator-output-report:C8 | PASS | RE | help lists all options with `[default: 6h]` |
| qa-operator-output-report:C9 | PASS | RE | help identical to `step-1.7-help.txt` (E3) |
| qa-operator-output-report:C12 | PASS | UN | `report.py` unchanged; fix touched only the summary flag and the Orca shape check |
| qa-operator-output-report:C15 | PASS | AR | first live-check record and JSON unchanged |
| qa-operator-output-report:C16 | PASS | RE | OQ-2 default folder and name; `.gitignore:256` |
| qa-operator-output-report:C17 | PASS | RE | OQ-5 default `6h` at `commands.py:27` |
| qa-operator-output-report:C18 | PASS | RE | main diff 4 lines; `superclaude --help` stderr 0 bytes |
| qa-operator-output-report:C19 | PASS | UN | DESIGN 3.2 and 7.1 strings and `commands.py` unchanged |
| qa-operator-output-report:C20 | PASS | RE | ruff check and `tests/sweep` (E3) |
| qa-publication-report:C1 | PASS | RE | UTC stem pattern `20261112-030000-sweep.md` from a fixed `now` |
| qa-publication-report:C2 | PASS | UN | `commands.py:156-164` unchanged |
| qa-publication-report:C3 | PASS | UN | `commands.py:168-170` unchanged; listing after each run shows no hidden temp |
| qa-publication-report:C4 | PASS | UN | `commands.py:146-150,175-181` unchanged |
| qa-publication-report:C5 | PASS | RE | four collision names `-sweep`, `-2`, `-3`, `-4` |
| qa-publication-report:C6 | PASS | UN | `commands.py:197-201` unchanged |
| qa-publication-report:C7 | PASS | UN | `commands.py:202-207` unchanged |
| qa-publication-report:C8 | PASS | UN | error-table rows live in unchanged `commands.py` |
| qa-publication-report:C9 | PASS | RE+UN | E1 `[Errno 17] File exists` text; other messages UN |
| qa-publication-report:C10 | PASS | RE | X2: no exit-2 run created `.dev` or issued an argv |
| qa-publication-report:C11 | PASS | UN | no `rename`, `replace` or truncate anywhere (E4); collision names kept earlier files |
| qa-publication-report:C12 | PASS | RE | E4 write-verb grep over `sweep/*.py` |
| qa-publication-report:C13 | PASS | UN | concurrent same-second runs not re-run; `_publish` unchanged |
| qa-publication-report:C14 | PASS | RE+UN | exit 0 left one report with no hidden file (C1 `ls -A`); exit 1 E1 left no report |
| qa-publication-report:C15 | PASS | RE | main diff unchanged |
| qa-publication-report:C16 | PASS | RE | help text matches OQ-2 and OQ-5 |
| qa-publication-report:C17 | PASS | AR | first JSON `report_path` and report unchanged; one more report on disk is the recorded re-run (N2) |
| qa-publication-report:C18 | PASS | RE | E3 |
| qa-publication-report:C19 | PASS | UN | stderr sanitising in `commands.py` unchanged (note M1 stays minor) |
| qa-publication-report:C20 | PASS | UN | `tests/sweep` still holds only `test_readonly.py` (note M4 stays minor) |
| qa-readonly-safety-report:C1 | PASS | RE | E4: writes only in `commands.py` lines 140, 149, 150, 158, 170, 186, 203 |
| qa-readonly-safety-report:C2 | PASS | RE+UN | X2 `--output /tmp` and `.dev/tasks` rejected; symlink matrix UN |
| qa-readonly-safety-report:C3 | PASS | RE+UN | same X2 cases; 12-case matrix UN, `_check_output` unchanged |
| qa-readonly-safety-report:C4 | PASS | RE | X2: tree unchanged after each exit-2 run |
| qa-readonly-safety-report:C5 | PASS | RE+UN | C1 scratch: `ls -A .dev/sweeps` shows exactly one report, no temp; git index byte check UN |
| qa-readonly-safety-report:C6 | PASS | RE | collision names `-2`..`-4`, none overwritten |
| qa-readonly-safety-report:C7 | PASS | RE | `subprocess.run` only at `probes.py:248` and `:299`; no `shell=` |
| qa-readonly-safety-report:C8 | PASS | UN | `commands.py` unchanged; B2-B6 issued only `run-current` |
| qa-readonly-safety-report:C9 | PASS | RE | 8 of 8 hostile argvs raised `ValueError`; 10 templates, 7 verbs; good argvs accepted |
| qa-readonly-safety-report:C10 | PASS | RE | `check_git_args` rejected `status`, `status ... --ignored`, `stash`; accepted the exact argv; `probes.py:296-297` unchanged |
| qa-readonly-safety-report:C11 | PASS | RE | zero `run-list`; B3-B6 issued only `orchestration run-current` |
| qa-readonly-safety-report:C12 | PASS | RE | three `open(..., "rb")` at `probes.py:575,826,890` |
| qa-readonly-safety-report:C13 | PASS | AR | first live-check record and OQ-8 record unchanged |
| qa-readonly-safety-report:C14 | PASS | RE | main diff: 4 insertions, 0 deletions |
| qa-readonly-safety-report:C15 | PASS | RE | help diff clean (E3) |
| qa-readonly-safety-report:C16 | PASS | RE | `DEFAULT_WINDOW` `6h`; `.gitignore:256` |
| qa-readonly-safety-report:C17 | PASS | RE | ruff clean, `tests/sweep` 4 passed; `git status` for `src/superclaude/cli`, `tests/sweep`, `docs/designs` shows only ` M main.py` and untracked new files |
| qa-registration-report:C1 | PASS | RE | `main.commands` last two `issue-watch`, `sweep`; one hunk |
| qa-registration-report:C2 | PASS | RE | diff line carries the same `noqa` comment as the `issue-watch` line |
| qa-registration-report:C3 | PASS | RE | import is `from superclaude.cli.sweep import sweep_group` (diff) |
| qa-registration-report:C4 | PASS | RE | `add_command(sweep_group, name="sweep")`; group name `sweep` |
| qa-registration-report:C5 | PASS | RE | `git diff` is 4 insertions, 0 deletions |
| qa-registration-report:C6 | PASS | RE | 19 commands, `sweep` last, no duplicate seen |
| qa-registration-report:C7 | PASS | RE+UN | `__init__.py` unchanged (01:14:42); star import gives `['sweep_group']` |
| qa-registration-report:C8 | PASS | RE | after purge and re-import no sweep submodule loaded; reading `sweep_group` loaded `commands`, `models`, `probes`, `classify`, `report` |
| qa-registration-report:C9 | PASS | RE | `pkg.nope` raises `AttributeError: module 'superclaude.cli.sweep' has no attribute 'nope'` |
| qa-registration-report:C10 | PASS | RE | no `superclaude.cli.main` import in `sweep/`; fresh interpreter `import superclaude.cli.sweep.commands` printed `sweep` |
| qa-registration-report:C11 | PASS | RE | ruff check and format clean (E3) |
| qa-registration-report:C12 | PASS | RE | help identical; top help lists `sweep` |
| qa-registration-report:C13 | PASS | UN | DESIGN unchanged since 11-09 |
| qa-registration-report:C14 | PASS | RE | the fix adds only the constant `_LIST_KEY` at module level in `probes.py`; no process or write at import |

Rows: 147. PASS: 147. FAIL: 0.

Informational (not part of the 147): the two cycle-0 FAIL ids that were caused by the F_0 findings now hold. `qa-failure-path-report:C7` (wrong-shape reply treated as an invalid response) is PASS (A3-A6, A9, A10). `qa-operator-output-report:C14` (JSON and report agree on the lower bound) is PASS (`lb=true` and two lower-bound lines in every run). The other cycle-0 FAIL ids concern MINOR findings and stay notes.

## Self-audit

- Count check: the table has 147 rows (failure-path 21, input-edge 19, interface-exit 22, live-check 20, operator-output 14, publication 20, readonly-safety 17, registration 14), matching the ids in `cycle-ledger.md` row 0 and the end of `consolidated-findings-cycle0.md`.
- What would make me wrong: a check marked UN that depends on code in `classify.py` or `probes.py`. I looked for these: only the live-check rule checks (C4, C5, C9, C10), which I tied to the re-run JSON with identical worker rows, and the failure-path Orca checks (C1-C6), which I re-ran.
- Not re-executed (limits): the cycle-0 injected-failure cases P1-P14 (write, fsync, link, close, unlink failures, Ctrl-C, concurrency, 99-name exhaustion), the stubbed `ValueError` / `RuntimeError` stage cases, the symlink containment matrix, and `tests/unit` (285 s). All sit in files whose mtimes are earlier than the cycle-0 reports (E1) and no fix hunk reaches them. The 726-passed line in `fix-log-cycle1.md` is the fix agent's own and was not reproduced.
- The executor's hash check of 74 protected files (fix log) was not reproduced; E1 mtimes are my independent evidence that no protected source file other than the two fix files changed.

**Confidence:** Verified: 149/149 (147 check ids plus CLI-F1 and CLI-F2) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. UN rows are verified by the file-unchanged evidence (E1), as the prompt asks, not by re-execution.
**Tool engagement:** Read: 28 | Grep: 6 | Glob: 0 | Bash: 17 (three scratch harnesses with a fake Orca, ruff, pytest `tests/sweep`, help diffs, `stat`, `jq` on the saved JSON, two `python -I` import probes). No web research.

Verdict: PASS
Blocking count: 0

## QA Complete
