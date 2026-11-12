# QA Report: CLI failure-path lens (T206)

**Topic:** `superclaude sweep run` failure paths (commands.py, probes.py seams)
**Date:** 2026-11-12
**Phase:** code gate, failure-path lens (adversarial, report-only, `fix_authorization: false`)
**Fix cycle:** N/A (first review)

Method: read `commands.py` (1-288), `probes.py` (80-350, 1015-1300), the `main.py` diff, DESIGN `docs/designs/orchestrator-mode.md` sections 3, 5, 7.1 (compared with `artifacts/design-base.md` using `diff`: section 3 identical; section 7.1 differs by two added signature lines and one extended comment; section 5 differs in one line, the unknown-Run row), SPEC `merged-requirements.md` 5.1-5.3, FR-002/004/017/018/019 and failure-mode table (lines 432-455), the OQ-2 and OQ-5 records, the step-1.7 help text, phase9-validation and the live-check records. Then ran scratch snippets under a private `/tmp` folder (no live Orca, a fake `ORCA_CLI_COMMAND` script, private `HOME` and `XDG_STATE_HOME`).

Scratch evidence: every case below ran under one private folder `/tmp/t206-qa.*` (a fake Orca script chosen through `ORCA_CLI_COMMAND`, `HOME` and `XDG_STATE_HOME` inside the folder, throwaway `git init` repos). No live Orca call was made, `superclaude sweep run` was never run against live Orca, and no repository file was edited. Case ids P1-P14 call `commands._publish` with injected failures; B1-B23 and S1-S3 call the real `sweep run` command through `CliRunner` with the fake Orca.

## Findings

### F1 (MAJOR) A wrong-shape Orca reply is accepted as a successful, empty read

- Evidence: `src/superclaude/cli/sweep/probes.py:280-286` (`_orca` calls any reply `ok` once it is JSON with `ok: true` and a dict `result`); `probes.py:1058-1062` (`worker-list`: a missing or non-list `workers` becomes an empty list), `1072-1078` (`task-list --ready`), `1083-1087` (`task-list`), `1238-1247` and `1213-1214` (`worktree ps`: a missing `worktrees` list is recorded as `read`, only the root is scanned).
- Scratch result B7: fake Orca answers every verb with `{"ok":true,"result":{}}`. The command exits 0, `orca_available` is `true`, 0 rows, no `unscanned` source, and the report prints `orca worker-list run_aaaaaaaaaaaa | read | unknown | none` (and the same for both `task-list` rows and `worktree ps`). Compare B6, where non-JSON text gives `unscanned: orca call failed (invalid response)` and `orca_available: false`.
- What is wrong: SPEC section 8 (`merged-requirements.md:287`) says "Invalid response includes empty or unparseable stdout and JSON that cannot establish the operation's captured success or no-binding shape ... `ok` requires the captured success shape", and the failure-modes table (line 439) sends such a reply to `call_failed`. The captured worker-list shape is `result.workers` plus `result.page` (live record `artifacts/sweep-live-check-1.4-workers.json`). With a renamed or missing key (for example a different Orca version, the drift NFR-015 warns about) the sweep claims the Run was read and holds no workers, the worker-list incomplete note (`classify.py:694-697`, which keys on `listing.unscanned`) never fires, and the first-call rule of SPEC section 8 (an invalid first reply means unavailable) is bypassed. DESIGN section 5 line 245 allows "ok, zero rows" only for a list that is present and empty (case B8 passes).
- Smallest fix: in `probes._call` (or `_orca`), after an `ok` result for `worker-list`, `task-list` or `worktree ps`, require `data.get("workers" | "tasks" | "worktrees")` to be a list; otherwise return `OrcaResult("call_failed", None, "orca call failed (invalid response)")` so the existing first-call, `record()` and origin-unknown logic apply. About 6 lines; add one test per verb.

### F2 (MINOR) Default-output failure names `--output` and says the path must be itself

- Evidence: `commands.py:99-112`. Scratch S1 (`<root>/.dev/sweeps` is a symlink) and S3 (`<root>/.dev` is a symlink), run without `--output`: exit 2, stderr `invalid --output: <root>/.dev/sweeps (must be <root>/.dev/sweeps/ or a folder below it)`. The operator passed no `--output` and the sentence contradicts itself; nothing says a symlink is the cause. Nothing is written (correct per FR-004).
- Smallest fix: when `output is None`, or when `resolved` differs from `base` through a symlink, say `<root>/.dev/sweeps resolves outside the checkout (symlink?): <resolved>`.

### F3 (MINOR) Exit-1 handler hides the error type and garbles the text

- Evidence: `commands.py:286-288` uses `sanitize(exc)`, which is built for Markdown table cells (`report.py:547-577`, escapes `[ ] | < > \`).
- Scratch results: B16 `[sweep output] \[Errno 32\] Broken pipe`; B20 `[sweep args] \[Errno 2\] No such file or directory`; B18 (`KeyError`) `[sweep output] 'rows'`; B22 (`AssertionError()`) `[sweep classify] ` with nothing after the prefix. The operator sees the stage but not the exception class, and sometimes no text at all. The `BindingError` branch (`commands.py:279-281`) and the `_PublishError` lines (`commands.py:282-285`) are not sanitized at all, so the three stderr paths treat untrusted text three different ways.
- Smallest fix: `f"[sweep {stage}] {type(exc).__name__}: {exc}"` with control characters stripped but without the Markdown escapes.

### F4 (MINOR) After the commit point the stderr does not say that a complete report exists, or where

- Evidence: `commands.py:202-207` (unlink failure after link), `commands.py:276-288` (stage `output`). P9: stderr is only `[sweep publish] could not remove temp file <tmp>`; disk holds the complete report and the temp name. B16 and B18: stderr is `[sweep output] ...`, disk holds one complete report. The text matches DESIGN section 3.2 (table row for unlink after commit), but the operator and the skill cannot tell from it that `<stem>.md` is complete, and a retry adds another report.
- Smallest fix: add a second stderr line `[sweep publish] report kept: <path>` in these two cases (DESIGN 3.2 already allows a second line on other exit-1 paths).

### F5 (MINOR) Ctrl-C during publication leaves the temp file

- Evidence: `commands.py:175-181` and `182-196` catch only `OSError`. P12 (`KeyboardInterrupt` raised inside `os.write`): the `.tmp` file stays. B19 (Ctrl-C inside `collect`) shows click printing a bare `Aborted!` with exit 1 and no `[sweep <stage>]` prefix. DESIGN 3.4 allows a leftover temp "when it was killed", and SIGINT is arguably that, but SIGINT is catchable and the cleanup is one line.
- Smallest fix: `except BaseException: _drop_own_temp(tmp); raise` around the write and link steps.

### F6 (MINOR) Output-folder problems appear only after the full probe run, and two write errors do not name the folder

- Evidence: `commands.py:158-160` and `169-181`. B13 (`--output` names a regular file) and B13b (read-only folder) exit 1 only after `collect`, `classify_all` and `render` have finished (up to 90 s of Orca and git work). P4 and P5 print `[sweep publish] [Errno 28] No space left on device` and `[Errno 5] Input/output error` with no path, so the operator cannot tell write from fsync from close, or which folder. P1 prints `File exists: '<dir>'` for "a file sits where the folder must go". DESIGN 3.2 prescribes `[sweep publish] <error>`, so this conforms but is weak.
- Smallest fix: name the stage and folder (`write to <dir>:`), and optionally a read-only `is_dir` / `os.access` check in `_check_output` so these become an immediate exit 2.

### F7 (MINOR) Argument edge cases

- B12b: `--run ""` prints `invalid --run value: ` with nothing visible after the colon (`commands.py:91`); print the value with `repr`.
- B12d: `--root ""` is accepted as the current folder (`Path("")` resolves to cwd, `commands.py:76-84`) instead of `invalid --root:`; the default root walks upward, this does not.
- B20: when the current folder was deleted, `Path.cwd()` (`commands.py:75`) raises and the run exits 1 `[sweep args] ...` instead of the FR-004 exit 2 "no git checkout found above <cwd>".

### Notes (not findings)

- The publication, Orca-failure and CLI-contract tests for these paths are item 10.7 (`test_cli_contract.py`, task file line 1825) and do not exist yet (`tests/sweep/` holds `conftest.py` and `test_readonly.py` only). These failure paths are therefore verified only by the scratch cases in this report; this is the planned order, not a defect at this gate.
- `tests/unit` (the 726-passed line in `phase9-validation.md`) was not re-run (285 s, outside this lens). `ruff check`, `ruff format --check`, `sweep run --help` and `pytest tests/sweep` (4 passed) were re-run and match the records.

## Failure-case table (exit code, stderr, what stays on disk)

| Case | Exit | Stderr (abridged) | Left on disk | DESIGN 3 / 5 |
|---|---|---|---|---|
| Orca binary missing, no `--run` (B1) | 2 | `Orca unavailable (binary not found: <bin>); no Run binding could be established: pass --run <id>` | nothing | matches |
| Orca exits non-zero or empty body on call 1, no `--run` (B2, B3, B4b) | 2 | `Orca unavailable (orca call failed (exit 1) / (invalid response) / runtime_unavailable); ...` | nothing | matches |
| Orca hangs, no `--run` (B5, 10.3 s) | 2 | `Orca unavailable (timeout after 10 s); ...` | nothing | matches |
| No Run bound (B4) | 2 | `no Run bound: pass --run <id>` | nothing | matches |
| `--run`, call 1 non-JSON or exit 1 (B6, B6b) | 0 | empty | one report, no temp; `orca_available: false`, reason in Source coverage | matches (FR-019) |
| `--run`, worker list empty `[]` (B8) | 0 | empty | one report, no temp | matches |
| `--run`, worker list ok but `task-list` fails `run_not_found` (B9) | 0 | empty | one report; both task-list rows `unscanned: orca call failed (exit 1)` | matches |
| `--run`, worker list valid JSON without `workers` (B7) | 0 | empty | one report claiming `read` | DIFFERS (F1) |
| No `.git` above cwd (B10); bad `--root` (B11) | 2 | `no git checkout found above <cwd>` / `invalid --root: <path>` | nothing | matches |
| Deleted cwd (B20) | 1 | `[sweep args] \[Errno 2\] ...` | nothing | differs from FR-004 exit 2 (F7) |
| `--output` outside `.dev/sweeps` (B12), bad window (B12c, B23) | 2 | names the flag and value | nothing, `.dev` not created (B23) | matches |
| Symlinked `.dev` or `.dev/sweeps`, default output (S1, S3) | 2 | `invalid --output: X (must be X/ ...)` | nothing | exit matches; message F2 |
| Output path is a regular file (B13, P1) | 1 | `[sweep publish] [Errno 17] File exists: '<dir>'` | no report, no temp | matches |
| Read-only output folder (B13b, P13) | 1 | `[sweep publish] [Errno 13] Permission denied: '<tmp path>'` | no report, no temp | matches |
| Temp name already exists (P3) | 1 | `[sweep publish] temp file exists: <tmp>` | the other run's file, untouched | matches |
| Write or fsync fails (P4, P5) | 1 | `[sweep publish] [Errno 28] No space left on device` (no path) | no report, temp removed | matches; F6 |
| Write fails and unlink fails (P6) | 1 | two lines, second `[sweep publish] left temp file <tmp>` | temp only | matches |
| `os.link` fails with EPERM (P7, P7b) | 1 | `[sweep publish] cannot link report: [Errno 1] ...` (+ `left temp file` line when unlink fails) | no report; temp removed unless unlink fails | matches |
| 99 names taken (P8, P8b) | 1 | `[sweep publish] report name space exhausted: <dir>` (+ `left temp file`) | the 99 old reports untouched, no new name, temp removed | matches |
| Folder swapped for a symlink after `makedirs` (P10) | 1 | `[sweep publish] output dir escaped <root>/.dev/sweeps/` | nothing written outside | matches |
| Unencodable text (P11) | 1 | `[sweep publish] 'utf-8' codec can't encode ...` | folder only | matches |
| Ctrl-C while writing (P12) | 1 | `Aborted!` | own temp left | allowed as "killed"; F5 |
| Unlink fails after commit (P9) | 1 | `[sweep publish] could not remove temp file <tmp>` | complete report plus temp (same inode) | matches; F4 |
| Printing the JSON fails (B16) | 1 | `[sweep output] \[Errno 32\] Broken pipe` | complete report | matches; F3, F4 |
| `to_json` raises after commit (B18) | 1 | `[sweep output] 'rows'` | complete report | matches; F3, F4 |
| Allowlist miss in `collect` (B21) | 1 | `[sweep collect] orca arguments are not allowed: (...)` | nothing, `.dev` not created | matches |
| `classify_all` raises (B22) | 1 | `[sweep classify] ` (blank) | nothing | matches; F3 |
| Success twice in one second (P14) | 0 | empty | `<stem>.md`, `<stem>-2.md`, no temp | matches (FR-017) |

Follow-up checks on the scratch folders: P3's pre-existing temp still reads `OLD`; in P8 all 99 earlier files kept their content (99/99); in P9 the temp and the report share inode 17621405 with link count 2 and the report's last line is `Report complete`; P14 leaves exactly the two report names.

## Checks

| Id | Check | Result | Finding |
|---|---|---|---|
| C1 | Orca fails (binary missing, exit 1, empty body, `runtime_unavailable`) with no `--run`: exit 2, reason in the message, nothing on disk (B1-B3, B4b) | PASS | |
| C2 | Orca hangs with no `--run`: exit 2 after the 10 s per-call cap (B5, 10.3 s) | PASS | |
| C3 | No Run bound: exit 2 `no Run bound: pass --run <id>` (B4) | PASS | |
| C4 | `--run` with a failing or non-JSON first Orca reply: disk-only, exit 0, reason visible in Source coverage, no temp (B6, B6b) | PASS | |
| C5 | Later per-source failure: `call_failed`, `orca_available` stays true, exit 0 (B9) | PASS | |
| C6 | Worker list empty (`workers: []`): exit 0, zero rows, `read` (B8) | PASS | |
| C7 | Worker list valid JSON but wrong shape is treated as an invalid response (SPEC section 8) (B7) | FAIL | F1 (MAJOR) |
| C8 | No repository root: exit 2, names the folder, writes nothing (B10, B11) | PASS | |
| C9 | Every exit-2 path writes nothing, `.dev` not created (B1-B12, B23, S1-S3) | PASS | |
| C10 | Output folder cannot be created or written: exit 1, `[sweep publish]` plus path, no report, no temp (P1, P13, B13, B13b) | PASS | F6 minor |
| C11 | Write, fsync, link and close failures: exit 1, own temp removed, second line when the unlink also fails (P4-P7b) | PASS | |
| C12 | Report name space exhausted: exit 1, DESIGN text, 99 old files untouched, temp removed (P8, P8b) | PASS | |
| C13 | Existing temp name: exit 1, other file untouched (P3) | PASS | |
| C14 | Temp unlink fails after the link: exit 1, no JSON, one complete report plus own temp (P9) | PASS | F4 minor |
| C15 | Output folder swapped for a symlink after `makedirs`: exit 1, nothing written outside (P10) | PASS | |
| C16 | JSON print or `to_json` fails after the commit point: exit 1, report stays (B16, B18) | PASS | F3, F4 minor |
| C17 | Exit 1 before the commit point leaves no file at any report name (P1-P8, P10, P11, P13, B13, B21, B22) | PASS | |
| C18 | Interrupt during publication leaves no temp file (P12) | PASS | F5 minor (allowed as "killed" by DESIGN 3.4) |
| C19 | Operator can tell the failing input or stage from the message alone, for every exit 1 and exit 2 case | FAIL | F2, F3, F6, F7 (all MINOR; does not fail the gate) |
| C20 | `_publish` follows DESIGN 3.2 steps 1-7 and the 7.1 signature; exit mapping equals DESIGN 7.1 line 445 (`commands.py:153-208`, `279-288`) | PASS | |
| C21 | `main.py` diff: one deferred import plus `add_command(sweep_group, name="sweep")`, same pattern as `issue-watch` (`main.py:567` and `569`) | PASS | |
| C22 | Recorded evidence: `step-1.7-help.txt` equals today's `sweep run --help` (diff clean); ruff check and format re-run clean; `pytest tests/sweep` 4 passed; live-check JSON (exit 0, 180 rows, 0 unscanned, 5 workers, 9 Orca reads, report 605 lines ending `Report complete`) is internally consistent | PASS | `tests/unit` not re-run |
| C23 | OQ-2 and OQ-5 honoured: default output `<root>/.dev/sweeps/`, UTC name `<YYYYMMDD-HHMMSS>-sweep.md`, `.dev/sweeps/` ignored (`.gitignore:256`), default window `6h` (help text and live JSON `window: 6h`) | PASS | |

## Self-Audit

**(a) Reliance list:** no inherited structural verdict was supplied in the prompt, so no rf-qa PASS was relied on; standalone behaviour applies. I did rely on the task's own recorded outputs only as things to re-check (C22), not as evidence.

**(b) Independent semantic checks:**
- Wrong-shape reply accepted as `read` (F1): found by running the real command against a fake Orca (case B7) and comparing with SPEC section 8 line 287, not by reading the code alone.
- Leftover-file claims: each "what stays on disk" cell in the failure-case table comes from a directory listing taken after the injected failure (P1-P14, B-cases), plus inode, content and count checks.
- The 10 s timeout, exit codes and stderr text were measured, not inferred (B5 took 10.341 s).

Counts: factual claims verified with tool output: about 60 (23 checks plus the 29 table rows, which overlap). Files read: `commands.py`, `probes.py` (80-350, 555-605, 1015-1300), `classify.py` (660-730), `report.py` (520-583), `docs/designs/orchestrator-mode.md` (via diff against `artifacts/design-base.md`, sections 3, 5, 7.1), `design-base.md` 82-157, 223-290, 351-446, `design-addendum.md`, SPEC `merged-requirements.md` (150-190, 280-302, 428-456, FR rows), OQ-2 and OQ-5 records, `step-1.7-help.txt`, `phase9-validation.md`, the three live-check artifacts, the `main.py` diff, `tests/sweep/` listing. If I had found 0 issues this would be suspect; the one MAJOR comes from running a case the code's own tests do not yet cover. No web research was done (Tavily not needed).

**Confidence:** Verified: 22/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 95.7% (C19 is the one FAIL; every check was run with tool evidence, so the number counts checks carried out, not checks passed).
**Tool engagement:** Read: 23 | Grep: 11 | Glob: 2 | Bash: 21 (approximate tally from this session; every call maps to a check or a table row).
Unchecked items: none. Unverifiable items: none (the one out-of-lens item, `tests/unit`, is stated in Notes).

## Recommendations

1. Fix F1 before the CLI gate closes: shape-check the three list-bearing replies and add one `test_cli_contract.py` case per verb (empty `result`, `workers` not a list).
2. Take the MINOR items F2 to F7 with the same change if cheap; none blocks the gate. F3 (type name in the exit-1 line) and F4 (say that a complete report was kept) matter most to the skill that reads stderr.
3. Add the DESIGN section 11 publication cases (item 10.7) so P1-P14 and B7 become permanent tests.

Verdict: FAIL
Blocking count: 1

## QA Complete
