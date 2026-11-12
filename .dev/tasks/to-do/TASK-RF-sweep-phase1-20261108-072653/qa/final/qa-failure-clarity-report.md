# QA Report: Failure-path clarity lens (final gate, T323)

Reviewer: qa-final-* (rf-qa-qualitative), fix_authorization: false.
Date: 2026-11-12.

## Scope and method

Lens: for an Orca outage, a full page, `call_failed`, a missing transcript, a publish collision and a bad `--window`, does the exit code, stderr text and report text say what happened and that nothing was changed; report anything silent, misleading or claiming a fact it did not observe.

Read from disk now: `src/superclaude/cli/sweep/commands.py` (all 288 lines), `probes.py` (60-370, 1020-1392), `report.py` (1-673), `classify.py` (150-410, 700-850), `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `src/superclaude/commands/sweep.md`, the `pragmatic.md` diff against the base, DESIGN 3.2 (lines 99-130), 5 (225-288), 7.5 (601-647), the resolved addendum, `tests/sweep/test_cli_contract.py` (372-460, 530-570, 1160-1456), `tests/sweep/test_report.py` (575-613).

Experiments, all run from a private copy (`/tmp/qa-t323/exp1.py`, a temporary HOME, `probes._orca` and `probes._git` replaced by fakes fed with the captured fixtures; no live Orca, no repository file written, copy deleted at the end). They drove `collect`, `classify_all` and `render` and printed the report lines quoted below:

| Run | Fake Orca behaviour | Purpose |
|---|---|---|
| s1 | worker-list and both task-lists fine; `worktree ps` returns `call_failed` (invalid response) | `call_failed` on one source |
| s2 | worker-list and task-lists fine, then every later call `unavailable` (timeout) | Orca drops mid-run |
| s3 | everything fine, no transcripts, no tab map | missing transcript |
| s4 | everything fine, `worktree ps` answers with `truncated: true` | a full (cut) page |
| s5 | worker-list answers `hasMore: true` with 5 rows | full-page wording |

Tests run: `uv run pytest tests/sweep tests/commands/test_sweep_command.py -q` gave 694 passed. `uv run ruff check` and `ruff format --check` on the sweep source and tests: clean. No web research was done (no Tavily or fallback call).

## Findings

### F1. MAJOR. The header banner says "Orca unavailable" when Orca answered

- Evidence: `src/superclaude/cli/sweep/report.py:155-158` (`_discovery_incomplete` is true for ANY `orca worktree ps` source with an unscanned reason), `:186-187` (prints `WORKTREES_LINE`), `:33` (the literal "...Orca unavailable; worktree count is a lower bound"). The reasons that reach that source row are produced in `probes.py:1254-1272`: `worktree list truncated` (`:1261`), a `call_failed` reply, or the time budget running out.
- Reproduced:
  - s4 (Orca answered, list cut): header `[child worktrees not discovered: Orca unavailable; worktree count is a lower bound]` while the same report's Source coverage row says `| orca worktree ps | read | unknown | unscanned: worktree list truncated |`.
  - s1 (invalid reply to `worktree ps`): same banner; Orca had answered three other calls.
- What is wrong: the report states a cause (Orca unavailable) that was not observed and that its own table contradicts. This is the "full page" scenario for worktrees (a cut list) and the `call_failed` scenario, both misreported in the first lines a person reads.
- Prior gates saw this as "DESIGN's literal" (`qa/tests/verify-cycle1-rf-qa-qualitative.md:111`). It is still a false statement, and DESIGN 7.5 line 614 pins both the text and the broad condition, so the fix needs the DESIGN line, `tests/sweep/test_report.py:598-613` and `tests/sweep/test_cli_contract.py:443` to move together (owner decision on the pinned literal).
- Smallest fix: keep the literal only when `result.orca_available` is false; otherwise print `[child worktrees not discovered: orca worktree ps unscanned (<its reason>); worktree count is a lower bound]`.

### F2. MAJOR. "Orca sources were not read" contradicts the same report when Orca drops mid-run

- Evidence: `report.py:504-505` prints `- Orca was unavailable; Orca sources were not read` whenever `orca_available` is false. `probes.py:1061-1062` and `:1206-1207` set it false on ANY later `unavailable` result, after earlier sources were read.
- Reproduced (s2): under "What I could not determine": `- Orca was unavailable; Orca sources were not read`, directly above the footer lines `- orca worker-list run_0123456789ab: read`, `- orca task-list --ready ...: read`, `- orca task-list ...: read`.
- What is wrong: a false statement about what was read, in the section whose job is to say what was not read. A person cannot tell which Orca data is real.
- Not pinned by any test (`grep` of `tests/` for the sentence: no match).
- Smallest fix: `- Orca became unavailable; the Orca sources marked unscanned above were not read`.

### F3. MAJOR (relay layer). The chat reply drops the Orca outage; an exit 0 outage run reads as a normal run

- Evidence: `SKILL.md:25` ("take only `report_path` and `summary`"), `:26` (print the summary numbers, the lower-bound note and the path), `:39-43` (exempt reply is counts and path only). `orca_available` and the unscanned sources are in the JSON (`report.py:610-619`) but the skill never reads them; `grep` of `SKILL.md` and `tests/commands/test_sweep_command.py` for `orca_available|unavailable|unscanned`: no match. `total_is_lower_bound` is the constant `True` (`classify.py:976`), so the only caveat printed is the always-present remote-hosts one.
- Why it matters: with `--run` given, or after a successful binding, an outage exits 0 and publishes (design 5 note at line 286; `tests/sweep/test_cli_contract.py:392-426`). The reply then carries counts built from disk sources only, for example no waiting (a) rows, with nothing that says Orca was not read. The report says it; the reply does not.
- Lens boundary: this is outside the three surfaces the lens names (exit code, stderr, report text), included because the skill is the only thing that relays the result to the person. If the gate owner treats the reply as out of this lens, downgrade it to MINOR; the verdict stands on F1 and F2 either way.
- Smallest fix: step 3 also takes `orca_available`; step 4 adds one line when it is false ("Orca was unavailable; the counts come from disk sources only"). The exempt-reply wording in `pragmatic.md` and the addendum ("counts and path alone") must allow that one line, so this needs the owner.
### F4. MINOR. After the commit point, exit 1 does not say a complete report exists

- Evidence: `commands.py:195` (commit point), `:202-207` (unlink failure: stderr is only `[sweep publish] could not remove temp file <tmp>`), `:276-278` and `:286-288` (print failure: `[sweep output] <text>`). Pinned by `tests/sweep/test_cli_contract.py:1406-1424` and `:1427-1456`.
- What is wrong: exit 1 everywhere else means nothing was written; here a complete report stays (and in the unlink case a second hard link, named only by its hidden temp name). Neither stderr line names the report, and the skill (`SKILL.md:27`) prints no path on exit 1. DESIGN 3.2 lines 128-129 documents the disk state; the person is not told.
- Smallest fix: a second stderr line `[sweep publish] report kept: <path>` on these two paths.

### F5. MINOR. No failure line says "no report was written"

- Evidence: every pre-commit stderr line (`commands.py:70, 83, 91, 107-122, 160-201, 287`) names a cause but never the state left behind. `makedirs` can leave new folders (DESIGN line 123), and the escaped-path case calls `makedirs` first (`:158-164`); neither says so.
- Impact: low; the tests prove nothing is written. A person has to trust the exit code convention.

### F6. MINOR. The exit-1 handler can print an empty or opaque cause

- Evidence: `commands.py:286-288` prints `[sweep <stage>] ` plus `sanitize(exc)` with no class name (pinned by `test_cli_contract.py:1420`). Run in this review: `KeyError('dispatch')` prints `[sweep classify] 'dispatch'`; `AssertionError()` and `TimeoutError()` print `[sweep classify] ` with nothing after it.

### F7. MINOR. The full-page line states "100 shown" as a fixed fact

- Evidence: `report.py:32` and `:190-191`; the trigger is `len(workers) >= 100 or hasMore` (`probes.py:1079-1081`). s5 (`hasMore` true, 5 rows) prints `[Orca rows: 100 shown; ...]`. With several Runs, 100 is per Run, not the total shown. Real Orca returns `limit 100` (`tests/sweep/fixtures/captured-worker-list.json:390-393`), so the common case is true.

### F8. MINOR. A missing transcript folder is not listed under "What I could not determine"

- Evidence: `probes.py:1375-1376` records `no folder` with an empty unscanned reason; `report.py:498-503` lists only sources with an unscanned reason; the fallback row's next step (`report.py:53`) is "read the sources in Source coverage that were not scanned". s3: five rows are `could not determine` (evidence `no rule 1 to 8 matched (...; person_started None)`), the Source coverage row reads `| claude project ... | no folder | unknown | none |`, and "What I could not determine" mentions neither transcripts nor the empty tab map. The rows are honest (not idle, not finished); the cause is only inferable.

### Checked and found sound (no finding)

- `--window`: `commands.py:43-52` rejects with `invalid --window value: <text> (use <N>h or <N>d, at most 720h or 30d)`, exit 2, text sanitized, before any Orca call or write (`test_cli_contract.py:533-567`, 17 bad values).
- Orca outage with no `--run`: exit 2 `Orca unavailable (<reason>); no Run binding could be established: pass --run <id>` (`probes.py:352-362`, test `:375-389`); the advice is true because `--run` continues on disk sources.
- Publish collision: `os.link` never overwrites; names `-2` to `-99`; exhaustion gives `[sweep publish] report name space exhausted: <dir>`, temp file removed, earlier reports byte-identical (`commands.py:182-201`, tests `:1327-1354`). The temp-name collision leaves the other file alone (`:1356-1365`).
- `call_failed`: each failed source gets an `unscanned` row with its reason (s1 table: `unscanned: orca call failed (invalid response)`), rows fall to `could not determine`, and empty sections print `No matching records. This is not an all-clear.` (`report.py:29`).
- Unreadable transcript: forced to `could not determine` with the note `unscanned: transcript not readable` (`classify.py:376-377`).
- The report always says READ ONLY in its header and `Inspection only.` in its footer (`report.py:173, 520`).
- The Phase 14 argument holds: `git diff --stat <base> -- tests/cli/eval tests/hooks src/superclaude/hooks src/superclaude/cli/eval` is empty and the venv has no `ruff` module (`find_spec` printed `False`), so the two ruff tests fail on this checkout's environment; the timing test touches unchanged paths.

## Checks

A check marked FAIL carries the severity of its worst finding; only BLOCKING and MAJOR findings fail the gate.

| Id | Check | Result |
|---|---|---|
| C1 | Bad `--window`: exit 2, cause and valid form named, nothing written | PASS |
| C2 | Other usage errors (`--root`, `--output`, `--run`): exit 2, cause named, sanitized | PASS |
| C3 | Orca outage, no `--run`: exit 2 with a true cause and a true remedy | PASS |
| C4 | Orca outage or drop with `--run`: report text states only observed facts | FAIL (F1 MAJOR, F2 MAJOR) |
| C5 | Orca outage: the reply that relays the result to the person says so | FAIL (F3 MAJOR, relay layer) |
| C6 | Full worker-list page: lower-bound line present and true | PASS (F7 MINOR) |
| C7 | Cut worktree list: the report says what was cut and why, truthfully | FAIL (F1 MAJOR) |
| C8 | `call_failed` source: unscanned row with reason; rows fall to could not determine; no all-clear | PASS |
| C9 | Missing transcript folder: rows are not claimed idle or finished; cause visible | PASS (F8 MINOR) |
| C10 | Unreadable transcript: forced to could not determine with a note | PASS |
| C11 | Publish collision `-2` to `-99`, exhaustion, temp-name collision: no overwrite, message names the cause | PASS |
| C12 | Pre-commit publish failures (makedirs, write, link, escape): cause named, own temp file removed | PASS (F5 MINOR) |
| C13 | Post-commit failures (print, unlink): the person learns a report exists | FAIL (F4 MINOR) |
| C14 | Exit-1 handler text is a usable cause | FAIL (F6 MINOR) |
| C15 | Exit codes agree across code, DESIGN section 5 and the skill (0 published, 1 internal, 2 usage) | PASS |
| C16 | Echoed user input in stderr goes through `sanitize` | PASS (`commands.py:51, 70, 83, 91, 107-121`) |
| C17 | Report says it only inspected (header and footer) | PASS |
| C18 | Failure paths have pinned tests; sweep tests pass | PASS (694 passed) |
| C19 | Phase 14 pre-existing-failure argument | PASS (checked, holds) |
| C20 | `ruff check` and `ruff format --check` on sweep source and tests | PASS |

Counts: 20 checks, 15 PASS, 5 FAIL. BLOCKING 0, MAJOR 3 (F1, F2, F3), MINOR 5 (F4 to F8, with F4 to F6 also marked on C13 and C14).
Verdict: FAIL

Blocking count: 3
