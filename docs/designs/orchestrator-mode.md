# Orchestrator mode, Phase 1: `/sc:sweep` architecture design

## 1. Status, scope and inputs

Status: design for review, issue #339 Phase 1, written 2026-11-08 by `/sc:design --type architecture --format spec`. It holds no implementation code. Owner approval of the WC-16 text (section 8) was given: the rule id WC-16 on 2026-11-09 (OQ-3) and the wording "On every coordinator wake or wait timeout" on 2026-11-12 (OQ-3 addendum).

Review status: the third review did not pass cleanly, and the three blocking findings it left open (R3-B1 to R3-B3 below) are now closed. They were still open after the review cap (2 fix cycles, 3 reviews: `orchestrator-mode-review-1.md` to `-3.md`). With coordinator approval (the reply to `msg_ee6f54c3b8a4`, delivery `delivery_17bd071084c5`, 2026-11-08), they are carried as the first required design-fix tasks of the `/task-builder` task file. Each one was closed by its own review gate before any code task started (the R3-B1, R3-B2 and R3-B3 gates all passed at cycle 1 in the task package):

- R3-B1: the session-to-Dispatch time-window rule reads three time fields (Dispatch start, Dispatch end, and the earliest transcript timestamp) that the data model (`OrcaObservation`, `TranscriptTail`) lacks.
- R3-B2: two Dispatch rows on one pane give conflicting results (False and None, or a join to both rows), and no rule decides between them.
- R3-B3: three SPEC FR-010 fixtures (outage, full page, `call_failed`) were dropped from `test_classify.py`.

Phase 1 adds one read-only command, `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-protocol` skill that call it, the WC-16 "Coordinator loop" contract text, and the routing and doc rows that name it. A successful run leaves one filesystem change: one dated report under `<root>/.dev/sweeps/`, plus that directory when it is new. A dot-prefixed temp file exists only during publication (section 3).

Inputs and the short names used below:

| Short name | Path | Used for |
|---|---|---|
| SPEC | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (653 lines) | FR-001 to FR-026 (lines 95-120), NFR-001 to NFR-015 (lines 130-144), sections 5 to 18 |
| PANEL | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-review.md` | SP-19 to SP-27 and the G-1 recommendation (lines 289-296) |
| FIXREVIEW | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-fix-review-1.md` | Verdict PASS; minor notes M1 to M10 |
| REPORT | `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md` | Steps 1.0a to 1.29 (from line 1237). Not edited. |
| GAPS | `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md` | GQ-101 to GQ-113 (lines 124-136), row count (line 138) |

Facts checked on this host on 2026-11-08 for this design (read-only):

- `src/superclaude/cli/sweep/` does not exist yet.
- `src/superclaude/cli/main.py` registers deferred subcommands at lines 519-565; the last pair is `issue-watch` (563, 565); `if __name__ == "__main__":` is at 568.
- `src/superclaude/cli/recommend/__init__.py:12-20` is the lazy `__getattr__` export pattern.
- `/opt/Orca/resources/app.asar.unpacked/out/package.json` has `"version": "1.4.245-aidev02.780594c521aa"`.
- `uv run --help` (uv 0.11.8) documents `--no-sync` as "Avoid syncing the virtual environment" and `--frozen` as "Run without updating the `uv.lock` file". This is the help text; the flags were not run.
- The ccsession tab map is one file per Orca pane under `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/<pane key with : written as +>`, holding three lines: session id, launch folder (`pwd -P`), Orca terminal handle (`src/superclaude/skills/ccsession-tag/ccsession:564-602`; README lines 355-360). The folder also holds `.ccsession-lock` and transient `.ccsession-tab.*` temp files. It records no Run id and no dispatch id. It does not hold an entry for every Orca-pane session (checked in the source for fix cycle 1): the `session-name.sh` hook writes one only when the Claude Code process is the one a `ccsession` launch started (`CCSESSION_LAUNCH_ID` set, `ccsession:1889`; owner check `hooks/session-name.sh:144-163`), `ORCA_PANE_KEY` and `ORCA_TERMINAL_HANDLE` are set and valid (`session-name.sh:177`, `ccsession:566-587`), and only at session start and prompt submit (`session-name.sh:178-180`). A plain `claude` in an Orca pane, or a `ccsession` run inside Claude Code (`ccsession:1881-1883`), writes none. Each pane keeps only its latest session, and an entry is removed when its session moves to another pane or is no longer saved (`ccsession:590-602`), so an earlier session of a reused pane has no entry. Nothing in the file tells a worker pane from a person pane.
- A Claude Code transcript record carries top-level `"timestamp"` (ISO 8601 UTC with `Z`) and `"sessionId"` keys (one transcript sampled under `~/.claude/projects/<project key>/`). This is one sample of a format IronClaude does not own.

Out of scope for Phase 1 (unchanged from SPEC section 2): any write verb, `/sc:close`, `gh` reads, a scheduler, report retention (SP-22: the person deletes old reports by hand), and remote hosts.

## 2. GQ resolutions

### 2.1 GQ-103(1) first: lock-free git in the seam

Decision: `--no-optional-locks` is built into the `_git` seam, so no caller can build a git argv without it. `probes._git(cwd, *args)` is the only function in the package that starts git. It builds the argv as

```
["git", "--no-optional-locks", "-C", str(cwd), "-c", "core.fsmonitor=false", *args]
```

and starts the child with `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. Fsmonitor is always off because a command named by repository configuration or the environment would otherwise run during status (issue 547). `args` must equal one of the four `ALLOWED_GIT` templates exactly, else the seam raises `ValueError` before any process starts (exit 1). Callers pass only `cwd`; they never pass the prefix, so a missing flag cannot be expressed.

Ordering: this seam and its recorded-argv test (NFR-002) are the first code commit and the first test of the build (step 1.4a in section 15.2), before any other probe code. Anchors: SPEC section 15 line 552, NFR-002 (line 131), section 8 lines 282-292 and 299; GAPS line 126. The `GIT_OPTIONAL_LOCKS` variable comes from git's documentation and stays UNVERIFIED here (SPEC line 299); the flag alone carries the guarantee and the variable is belt and braces.

### 2.2 GQ-101 to GQ-110

Each row takes the SPEC section 15 proposal (SPEC lines 553-563) and fixes the concrete design element that carries it. GAPS rows are at lines 124-133.

| GQ | Decision | Design element | Anchors |
|---|---|---|---|
| GQ-101 | A package counts toward "shared" only when it is active in a worktree: that worktree's one `git status` lists a changed or untracked path whose path starts with the package folder `.dev/tasks/{to-do,done}/<id>/`. Committed, unchanged folders never count. `mark_shared_packages` takes the per-worktree active sets and flags an id active in 2 or more worktrees; the report prints one Retained problems line naming every worktree. | `classify.mark_shared_packages(worktrees) -> tuple[WorktreeState, ...]`; `PackageRecord.active`; `WorktreeState.shared_package_ids` | SPEC FR-015 (line 109), line 553; GAPS line 124 |
| GQ-102 | `conflict` is the first package state checked: one id present as a folder in both `to-do/` and `done/` of the same worktree. It blocks removal and lists under Retained problems. | `classify.package_state`; state order in section 7.2 | SPEC FR-014 (line 108), line 554; GAPS line 125 |
| GQ-103(2) | The window is data, not a constant: `SweepContext(now, window, window_start, root, runs)` is the second argument of `classify_all`, and no module holds a window constant except the CLI default `"6h"`. | `classify.classify_all(SweepInput, SweepContext)` | SPEC FR-007 (line 101), line 555 |
| GQ-103(3) | The model carries every field a rule reads: `SessionRow.gate_policy` (from the Task spec text), `OrcaObservation.worker_done_seen`, `SessionRow.transcript_readable`, `ContractRecord.report_path`, `ContractRecord.artifacts`, `OrcaObservation.dispatch_started`, `dispatch_ended`, `dispatch_status` and `TranscriptTail.first_record_ts` and `tail_complete` (the path-B window). | `models.py` (section 7.2) | SPEC line 556, section 7 lines 229-243 |
| GQ-104 | No `run-list` call and no fallback. No `--run` plus no binding exits 2 (`no Run bound: pass --run <id>`); no `--run` plus an unavailable first call exits 2 with the SP-21 message (section 13, D3). `run-list` is not in `ALLOWED_ORCA`, so the seam refuses it. | `commands.run`, `probes.ALLOWED_ORCA` | SPEC FR-002 (line 96), line 557; GAPS line 127 |
| GQ-105 | `archive-blocked` is a package in `to-do/` whose `progress.md` has a line starting `FINAL:` after optional leading whitespace. A `to-do/` package without such a line is `unfinished`. For a ledger over 1 MiB the head 512 KiB and the tail 512 KiB are read and the tail is searched (M8 is accepted as a proposed split, SPEC line 295). | `probes` ledger reader sets `PackageRecord.has_final_line`; `classify.package_state` | SPEC FR-014, line 558; GAPS line 128 |
| GQ-106 | `.dev/sweeps/` goes into `.gitignore` and the rollback table, so a sweep's own report never makes its worktree look dirty. | Section 10, section 16 | SPEC FR-025 (line 119), line 559; GAPS line 129 |
| GQ-107 | `sanitize()` escapes `|` as `\|`, in addition to the FR-016 stripping and HTML neutralizing. The injection fixture gets one pipe case. | `report.sanitize` | SPEC FR-016 (line 110), line 560; GAPS line 130 |
| GQ-108 | Person-started is a transcript under a scanned project key that the tab map joins to no Orca row. The join is fixed in section 7.2 (`SessionRow`) as two paths: (A) an Orca row field that holds a Claude session id, matched to the transcript `sessionId`; (B) an Orca row field that holds a pane key or terminal handle, matched to a tab-map file name or line 3, whose line 1 is the session id. Both Orca-side fields are UNVERIFIED until step 1.0a (section 17). Until 1.0a shows at least one of them, no transcript can be proved unjoined, so `person_started` is None for every unmatched transcript and those rows print could not determine with note `tab map join not observable`. This is the FR-010 completeness guard applied, not a weakening. | `probes` tab-map and transcript readers; `SessionRow.person_started` | SPEC FR-010 (line 104), line 561; GAPS line 131 |
| GQ-109 | `gate-list`, `worker-read` and every `git stash` form are absent from both allowlists and from step 1.0a. `--include-remote` is the only forbidden token, checked in every argv; `worktree ps --agent-wait` is allowed (R5, owner 2026-11-08). | `probes.ALLOWED_ORCA`, `probes.FORBIDDEN_TOKENS` | SPEC line 562, NFR-014 (line 143); GAPS line 132 |
| GQ-110 | Exactly one `git status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all` per worktree, parsed once into `WorktreeState`. Before it, up to three read-only inspection calls (`config --show-origin --list -z`, then `ls-files -z` and `check-attr --stdin -z filter` only when a filter driver with a command is defined) decide whether a git filter selected by a tracked path could run a program; if so status is not run and the worktree is `unscanned` ("git filter could run a program"). Every git call runs with `-c core.fsmonitor=false` (issue 547). The recorded-argv test asserts one status argv per discovered worktree. | `probes.read_worktree`, `probes.ALLOWED_GIT` | SPEC line 563, section 8 lines 325-336; GAPS line 133 |

Two details of the git parse that the SPEC left open are fixed here (M7):

- `WorktreeState.unpushed` is `bool | None`. It is True when the branch header shows `ahead N` with N greater than 0, False when an upstream is shown with no `ahead` part, and None for `No commits yet`, detached HEAD (note `detached HEAD`), `[gone]` (note `upstream gone`) and a branch with no upstream (note `no upstream`). The ahead count goes into the note text (`ahead N`), not the type.
- FR-013 is kept in full: a branch with no upstream still makes the worktree `removable: no` with condition `no upstream`, even though `unpushed` is None. A None from the other header cases gives no `no` condition by itself; the worktree then prints the could-not-determine reason of section 7.

### 2.3 GQ-111 to GQ-113 (stale REPORT citations)

These three rows are stale citations inside the REPORT. They are carried, not fixed, and this design does not edit the REPORT (SPEC line 565; GAPS lines 134-136).

- GQ-111 and GQ-112: wherever this design or a later task needs the gaps-log count, it cites GAPS line 138: 113 rows, 88 open, 25 resolved. It never repeats the REPORT's old "Open 75" or "GQ-01 to GQ-103; 78 open" figures.
- GQ-113: REPORT line 1537 ("Every open GQ row is cited") is read as covering GQ-01 to GQ-100 only. GQ-101 to GQ-110 are cited by this design (section 2.2); GQ-111 to GQ-113 are cited here.
- `/task-builder` must copy the same rule into the task file: cite GAPS line 138 for counts and never edit the REPORT.

## 3. G-1 with SP-20: report publication

SPEC section 18 G-1 (lines 637-645) leaves open what a run that exits 1 leaves on disk. PANEL SP-20 (line 220) notes that `write_report` in `report.py` puts file I/O in a module the NFR-004 purity test is meant to cover. Both are resolved together here.

### 3.1 Where the write lives

Decision: the single write path is a private function `commands._publish(text, output_dir, now) -> Path` in `commands.py`. `report.py` keeps only pure code: `sanitize`, `render`, `SECTIONS`, the fixed strings and `CHECKED_ORCA_VERSION`. No `write_report` exists.

Why `commands.py` and not `probes.py` or a seventh module:

- `commands.py` is already the impure shell: it parses arguments, calls `collect`, calls `classify_all` and `render`, prints JSON and maps exceptions to exit codes. The publish step is one more shell step.
- `probes.py` is the read side. FR-021 keeps read and write code apart ("the sweep package holds no write verb"); putting the one filesystem write in the module that owns the read allowlist would blur the B3 boundary.
- A separate `writer.py` adds a module, a boundary row and an import test for about 30 lines with one caller.
- With the write gone, the NFR-004 AST test covers the whole of `report.py` unchanged, and B1 (`commands -> {probes, classify, report} -> models`) still holds.

Cost: the SPEC section 6 module table changes. `commands.py` gains `os` in its may-import list, and `report.py` loses `write_report`. This is deviation D1 (section 13).

### 3.2 The one write mechanism

Decision: write a temp file in the output directory, `fsync` it, then publish it under the report name with `os.link`, which fails when the name exists. This is the PANEL G-1 recommendation (lines 289-296). There is one mechanism and no fallback.

`_publish` runs only after every exit-2 check, `collect`, `classify_all` and `render` have succeeded, so a usage error or an internal error in those steps never reaches the filesystem. Steps:

1. `stem = now.strftime("%Y%m%d-%H%M%S") + "-sweep"` (UTC, `SweepContext.now`).
2. `os.makedirs(output_dir, exist_ok=True)`, then resolve `output_dir` again and confirm it is still `<root>/.dev/sweeps/` or below. A path that now escapes exits 1 with `[sweep publish] output dir escaped <root>/.dev/sweeps/` and writes nothing.
3. `fd = os.open(output_dir / f".{stem}.{os.getpid()}.tmp", O_WRONLY | O_CREAT | O_EXCL, 0o666)`. The process umask applies, as for any new file. `O_EXCL` also refuses a symlink at that name.
4. Write every byte of `text.encode("utf-8")` (loop until all are written), `os.fsync(fd)`, `os.close(fd)`.
5. For `name` in `stem.md`, `stem-2.md` to `stem-99.md`, in order: `os.link(tmp, output_dir / name)`. `FileExistsError` moves to the next name; success stops the loop. The successful link is the commit point.
6. No name left: unlink the temp file and exit 1 with `[sweep publish] report name space exhausted: <dir>` (SPEC section 5.3, line 174).
7. After the commit point: `os.unlink(tmp)`. If it fails, exit 1 with no success JSON (table below). Otherwise return the published path. `commands.run` then prints the one success JSON object with that `report_path`.

Why a link and not the alternatives:

- A direct exclusive create of the final name (`open(name, "x")`) makes the final name visible while it is still being written; a kill then leaves a `-sweep.md` file without its footer. With a link, a report name only ever appears for complete, flushed bytes. SPEC section 11 (line 453) tolerates the partial file; this design is stricter.
- `os.rename` and `os.replace` overwrite an existing target on POSIX, which would break "never reuses or overwrites an earlier path" (SPEC line 177). `os.link` fails with `EEXIST` instead, so it is the exclusive reservation SPEC line 175 asks for.
- No directory `fsync` after the link: if power is lost before the directory entry reaches disk, the name is simply absent, which is the same outcome as a crash before the link and never shows partial content.

Error handling inside `_publish`:

| Failure | Result |
|---|---|
| `makedirs` fails | Exit 1, `[sweep publish] <error>`; no file written (directories it did create may remain, section 3.4) |
| Temp name exists (`O_EXCL` fails) | Exit 1, `[sweep publish] temp file exists: <path>`; that file is not touched, because this run did not create it |
| Write, `fsync` or close fails (for example a full disk) | Unlink this run's temp file, exit 1 |
| `os.link` fails with anything but `FileExistsError` (for example a filesystem without hard links) | Unlink this run's temp file, exit 1 with `[sweep publish] cannot link report: <error>`. No fallback; which filesystems refuse is UNVERIFIED (section 17) |
| Unlink of the temp file fails on an exit-1 path | Second stderr line naming the left temp path; still exit 1 |
| Unlink of the temp file fails after the commit point | Stderr `[sweep publish] could not remove temp file <path>`, no success JSON, exit 1; the complete report stays. Publication counts as finished only when the temp file is gone, so a successful run never leaves two files (NFR-001) |
| Printing the success JSON fails after the commit point | Exit 1; the complete report stays |

### 3.3 What a crash can leave, and why it is never reused

A kill, OOM or power loss can stop the run at any point. What stays on disk depends on where:

| Stopped | Left on disk |
|---|---|
| Before step 3 | Nothing, or only the output directory if this run created it |
| Between step 3 and the commit point | This run's own `.<stem>.<pid>.tmp`, possibly partial. No `-sweep.md` name exists for it |
| Between the commit point and the unlink | One complete report ending in `Report complete`, plus the same bytes under the temp name (two names for one file). No success JSON was printed, so this is never a successful run |
| After the unlink | One complete report only |

Why the next run never reuses that path:

- Report names: every publish goes through `os.link`, which never writes to an existing name. A later run with the same second picks the next free suffix (the FR-017 two-files test).
- Temp names: a later run has a new `now` or a new pid, and opens its temp file with `O_EXCL`. In the improbable case of the same second and a recycled pid, it exits 1 rather than open the old file.
- No reader: the output directory may not overlap any input directory (FR-004), `collect` never reads `.dev/sweeps/`, and the skill reads only the `report_path` printed in the success JSON, which can only name a linked, complete report. A leftover temp file is never read and never shown as a report.
- No cleanup sweep: a later run never deletes a file it did not create. Leftover temp files are dot-prefixed, ignored by git through the `.dev/sweeps/` line (section 10), and removed by hand like old reports (SP-22).

### 3.4 Final exit-1 rule

This closes SPEC G-1 (lines 637-645) and adds the missing rule to section 5.3 (line 179):

> A run that exits 1 before the commit point (the successful `os.link`) leaves no file at any report name, neither `<stem>.md` nor a suffixed form. It may leave the output directory and any parent it created under `<root>/.dev/sweeps/`, and, only when it was killed or its own unlink failed, its own dot-prefixed temp file, which no later run reads or reuses. A run that exits 0 has removed its temp file, so it leaves exactly one report and nothing else. A run that exits 1 after the commit point, because the success JSON could not be printed or its own temp file could not be removed, leaves exactly one complete report that ends in `Report complete`, plus in the second case its own dot-prefixed temp file, and prints no success JSON. A run that exits 2 writes nothing, because every exit-2 check runs before `_publish` creates any directory. No run deletes or overwrites a file it did not create.

The allowlist miss (SPEC section 11 line 447) and every collection, classification or render error raise before `_publish`, so they fall under the first sentence with nothing left at all. The V3:184, V3:356 and V3:357 positions quoted in G-1 are all met: this run removes only its own incomplete output, earlier reports are never touched, and a killed run leaves no file that looks complete.

## 4. Component diagram

```
  person / coordinator session
            |
            |  /sc:sweep  (~/.claude/commands/sc/sweep.md, allowed-tools: Skill)
            v
  sc-sweep-protocol skill  (~/.claude/skills/sc-sweep-protocol/SKILL.md)
            |  Bash, timeout 120000 ms:
            |  superclaude sweep run ...      (PATH first)
            |  uv run --frozen --no-sync superclaude sweep run ...   (on "command not found")
            v
 +------------------------------ superclaude.cli.sweep ------------------------------+
 |                                                                                   |
 |  __init__.py   lazy __getattr__ -> sweep_group      (registered in cli/main.py)   |
 |                                                                                   |
 |  commands.py   click group "sweep", subcommand "run"          [impure shell]      |
 |     parse + validate args (exit 2) -> collect -> classify_all -> render           |
 |     -> _publish (the one write) -> print success JSON -> exit 0                   |
 |        |                    |                    |                                |
 |        v                    v                    v                                |
 |  probes.py  [read side]   classify.py  [pure]   report.py  [pure]                 |
 |   _orca seam               RULES (9)             sanitize                         |
 |   _git seam                classify              render, SECTIONS                 |
 |   ALLOWED_ORCA (10)        policy_of             CHECKED_ORCA_VERSION             |
 |   ALLOWED_GIT (4)          package_state                                          |
 |   FORBIDDEN_TOKENS         mark_shared_packages                                   |
 |   Budget                   safe_to_close                                          |
 |   disk readers             classify_all                                           |
 |   collect                                                                         |
 |        \                    |                    /                                |
 |         +-------------------+-------------------+                                 |
 |                             v                                                     |
 |                      models.py  frozen dataclasses, class constants,              |
 |                                 JSON_SCHEMA_VERSION = 1                           |
 +-----------------------------------------------------------------------------------+
        |                    |                          |
        v                    v                          v
  orca-ide (or $ORCA_CLI_COMMAND)   git (4 read calls)  files, read only:
  10 read templates                 --no-optional-locks   .dev/tasks/{to-do,done}/*/progress.md,
                                                          .archiving, worker contracts,
                                                          ~/.claude/projects/<key>/*.jsonl,
                                                          ccsession orca-tabs/, Orca package.json

  one write:  <root>/.dev/sweeps/<YYYYMMDD-HHMMSS>-sweep[-N].md   (commands._publish)
```

Boundaries (SPEC section 6, with D1 applied):

| Module | May import | Must not import |
|---|---|---|
| `__init__.py` | `commands` (inside `__getattr__` only) | anything at import time |
| `models.py` | standard library `dataclasses`, `datetime`, `typing`, `pathlib` (type only) | every other sweep module |
| `classify.py` | `models` | `probes`, `report`, `commands`, `subprocess`, `click`, `os`, `shutil` |
| `probes.py` | `models`, `subprocess`, `os`, `json`, `time`, `datetime` | `classify`, `report`, `click` |
| `report.py` | `models` | `probes`, `classify`, `commands`, `subprocess`, `click`, `os`, `shutil` |
| `commands.py` | all of the above, `click`, `json`, `os` (D1) | nothing further is needed |

- B1: imports go one way, `commands -> {probes, classify, report} -> models`.
- B2: `classify` and `render` treat every path as data only (SPEC section 6 B2): they never open, stat or resolve one, which the NFR-004 import test enforces by forbidding `os` and `shutil`, and they print paths through `sanitize`.
- B3: the read allowlist lives only in `probes.py`. Phase 2 `/sc:close` gets its own package, seam and allowlist; nothing in this package grows a write verb (FR-021).
- B4: the command and skill are thin: no parsing, no classification, no file writes.
- B5: no type is redeclared from `superclaude.contracts`.

Extension points, each additive: a new rule appended to `RULES` before `fallback` (NFR-010 pin updated in the same change); a new template in `ALLOWED_ORCA` (only after a capture or a recorded owner decision (R5, 2026-11-08), and never a write verb); a new `SourceCoverage` row; a new JSON key in v1 (never a removal or rename, NFR-009); a new entry in `report.SECTIONS`. A tenfold growth in Runs or rows is bounded by `Budget` (50 shows, 90 s), so it shows up as more `unscanned` rows and lower-bound totals, never as a longer run.

## 5. Sequence diagram

```
skill        commands.run            probes                 Orca / git / disk        classify / report
  |  sweep run   |                       |                          |                         |
  |------------->|                       |                          |                         |
  |              | validate --window, --root (walk to .git), --output, --run regex            |
  |              |   any failure ------------------------------------------------> EXIT 2 (nothing written)
  |              | now (UTC, read once), window, window_start, root; budget = Budget()        |
  |              |                       |                          |                         |
  |              |== RUN BINDING ========|                          |                         |
  |              | [no --run]            |                          |                         |
  |              |--bind_run(budget)---->| _orca run-current ------>|                         |
  |              |                       |<-- result class ---------|                         |
  |              |   unavailable (call 1, incl. empty body) -----------------> EXIT 2 "Orca unavailable (<reason>); ..."
  |              |   no_binding ------------------------------------------------> EXIT 2 "no Run bound: pass --run <id>"
  |              |   ok -> runs = (bound id)                        |                         |
  |              | [--run R...] runs = deduplicated ids, first call is worker-list            |
  |              | ctx = SweepContext(now, window, window_start, root, runs)                  |
  |              |--collect(ctx, runs, root, budget)-------------->|                         |
  |              |                       |                          |                         |
  |              |== ORCA READS (per Run, Budget-checked) ==========|                         |
  |              |                       | worker-list --run R ---->|  unknown Run id: ok, zero rows; task-list --run R fails (7.2)
  |              |                       | task-list --ready --run R|                         |
  |              |                       | task-list --run R ------>|                         |
  |              |                       | worker-show --dispatch D | (<= 50 total, share per Run)
  |              |                       | worktree ps (once) ----->|                         |
  |              |                       |   later unavailable: stop Orca reads, keep evidence,|
  |              |                       |   mark rest unscanned, orca_available = false     |
  |              |                       |   allowlist miss: ValueError --------------------> EXIT 1 (nothing written)
  |              |                       |                          |                         |
  |              |== GIT READS (per worktree: root + worktree ps paths) ==                    |
  |              |                       | _git(path) status --porcelain=v1 -z --branch --untracked-files=all
  |              |                       |        --ignore-submodules=all (after config/ls-files/check-attr inspection)
  |              |                       |   (--no-optional-locks, -c core.fsmonitor=false, GIT_OPTIONAL_LOCKS=0, 10 s, Budget)
  |              |                       |                          |                         |
  |              |== DISK READS =========| progress.md, .archiving, contracts, transcripts,  |
  |              |                       | orca-tabs/, Orca package.json (bounded, resolve()) |
  |              |<-- SweepInput --------| (collected_start, collected_end)                  |
  |              |                       |                          |                         |
  |              |== CLASSIFY =====================================================> classify_all(input, ctx)
  |              |                 per row, first rule that matches wins:                     |
  |              |                 1 blocked_contract  2 orca_exit_proof  3 fenced            |
  |              |                 4 waiting_signal (a, b)  5 working  6 finished  7 idle      |
  |              |                 8 person_active  9 fallback (could not determine)          |
  |              |                 then package_state, mark_shared_packages, safe_to_close    |
  |              |<-- SweepResult ----------------------------------------------------------|
  |              |== RENDER =======================================================> render(result, ctx) -> text
  |              |   internal error anywhere above -------------------------------------> EXIT 1 (nothing written)
  |              |                       |                          |                         |
  |              |== PUBLISH: _publish(text, output_dir, now) =======|                         |
  |              | makedirs; temp O_EXCL; write; fsync; os.link to first free name (commit)   |
  |              |   failure before commit: unlink own temp -------------------------------> EXIT 1
  |              |   names -2..-99 exhausted -------------------------------------------> EXIT 1
  |              | unlink temp           |                          |                         |
  |              |   unlink fails: report stays, no JSON ----------------------------------> EXIT 1
  |              | print success JSON (report_path) to stdout       |                         |
  |              |   print fails: report stays --------------------------------------------> EXIT 1
  |<-- EXIT 0 ---|                       |                          |                         |
  | read report at report_path; print path and (a)/(b) counts       |                         |
```

Notes:

- With an explicit `--run`, or after a successful binding, an unavailable result is never an exit 2: the run continues on disk sources and publishes (FR-002 tests 2 and 3).
- A budget-cut timeout is `call_failed`, never `unavailable` (SPEC section 11 line 445).
- `worktree list` and `worktree current` are not called in Phase 1 (section 7.3).

## 6. Data flow with counts

Symbols: R selected Runs (after deduplication), D distinct Dispatch rows returned by `worker-list`, W worktrees (the root plus each distinct canonical path from `worktree ps`), P package folders summed over all worktrees, C contract records named by Orca rows, T transcripts under the scanned project keys, M tab-map files.

```
 CLI args --> validate --> (no --run) run-current --> runs (R ids)
                |               1 call                     |
          exit 2 on any                                    v
          usage error        +----- Orca argv, at most 1 + 3R + 1 + 50 -----------+
                             | worker-list        R  (one page each, <= 100 rows) |
                             | task-list --ready  R                               |
                             | task-list          R                               |
                             | worktree ps        1                               |
                             | worker-show        min(D, 50), split across Runs   |
                             | worktree list 0, worktree current 0                |
                             +------------------------+---------------------------+
                                                      | D rows, W - 1 worktree paths
                                                      v
                             +----- git argv, exactly W --------------------------+
                             | status --porcelain=v1 -z --branch                  |
                             |  --untracked-files=all --ignore-submodules=all     |
                             | one per worktree, no retry (a filter refusal makes |
                             | none; up to 3 read-only inspection calls before it)|
                             +------------------------+---------------------------+
                                                      v
                             +----- disk reads (no subprocess) -------------------+
                             | package folders  P  (progress.md, .archiving stat) |
                             | contracts        C <= D  (> 1 MiB is unscanned)    |
                             | transcripts      T  (last 256 KiB each)            |
                             | tab-map files    M  (3 lines each)                 |
                             | Orca version     1 file, field "version" only      |
                             +------------------------+---------------------------+
                                                      v
                             SweepInput: D Orca rows, T transcripts, W WorktreeState,
                                         P PackageRecord, S SourceCoverage rows
                                                      | classify_all (pure)
                                                      v
                             SweepResult: N = D + U session rows (U = transcripts
                                          joined to no Orca row), one class each;
                                          W worktrees; P package states
                                                      | render (pure), to_json (pure)
                                                      v
                                    1 report file  +  1 JSON object on stdout   (exit 0)
                                    0 files at a report name, 0 JSON            (exit 1 before commit, exit 2)
```

Counts that tests pin:

| Stage | Count | Pinned by |
|---|---|---|
| `run-current` | 1 without `--run`, 0 with it | FR-002 tests |
| Orca argv total | at most `1 + 3R + 1 + 50`; every argv equals one template | NFR-003 recording test |
| `worker-show` | `min(D, 50)` when time allows; 2 Runs of 40 rows get 25 each | FR-020 (60-row, 50-row, 2-Run fixtures) |
| `worktree list`, `worktree current` | 0 in Phase 1 | NFR-003 recording test (section 7.3) |
| git status argv | exactly W (up to three read-only inspection calls precede each), each git argv with `--no-optional-locks` at index 1 | NFR-002, GQ-110 |
| Session rows | `N = D + U` | FR-005 (3 workers, 1 person session: 4 rows) |
| Reconciliation | `summary.total = summary.visible + summary.historical`; `summary.bound_reached <= summary.visible` | FR-005, FR-020 |
| Lower bound | `total_is_lower_bound` is true when any list is truncated (a full 100-row page) or unscanned | FR-005, section 8 paging |
| Output | 1 report and 1 JSON object on exit 0; no JSON on exit 1 or 2 | FR-017, FR-018, NFR-001 |

When Orca is unavailable after a binding, the Orca box stops at the failing call, W falls to 1 plus any paths already returned, and the header prints the worktree lower-bound line (SPEC section 9). When a later Orca read is cut by the budget, the remaining rows keep their identity and print could not determine with the budget reason; they are never dropped, so N and the reconciliation do not change.

## 7. Interfaces

### 7.1 Module signatures

Signatures only. Every name below is new and proposed by this design; none exists in the repository yet. The SPEC names (`collect`, `classify_all`, `render`, `sanitize`, `RULES`, `policy_of`, `package_state`, `mark_shared_packages`, `safe_to_close`, `Budget`, `_orca`, `_git`) keep their SPEC meaning.

`__init__.py`

```
def __getattr__(name: str) -> object        # "sweep_group" only; imports commands lazily
```

`probes.py` (read side; the only module that starts a subprocess)

```
class Budget:
    def __init__(self, shows: int = 50, total_s: float = 90.0, per_call_s: float = 10.0,
                 clock: Callable[[], float] = time.monotonic) -> None
    def share_shows(self, runs: tuple[str, ...]) -> None     # even split, remainder to the first Run
    def take_show(self, run: str) -> bool                    # False: "show cap reached (50)"
    def call_timeout(self) -> float | None                   # min(10, remaining); None below 1 s left
    def cut(self) -> bool                                    # last timeout was cut below 10 s

@dataclass(frozen=True)
class OrcaResult:
    kind: str            # "ok" | "no_binding" | "unavailable" | "call_failed"
    data: object | None  # parsed JSON for "ok"
    reason: str | None   # e.g. "binary not found: orca-ide", "unscanned: time budget reached (90 s)"

class BindingError(Exception)               # carries the exit-2 message; commands maps it to exit 2

def orca_binary() -> str                                     # $ORCA_CLI_COMMAND, else "orca-ide"
def check_orca_argv(args: tuple[str, ...]) -> None           # ValueError unless an exact template match
def check_git_args(args: tuple[str, ...]) -> None            # ValueError unless args is an ALLOWED_GIT entry
def _orca(*args: str, timeout: float) -> OrcaResult
def _git(cwd: Path, *args: str, timeout: float) -> str       # raises GitCallFailed on nonzero, timeout, > 8 MiB
class GitCallFailed(Exception)

def bind_run(budget: Budget) -> str                          # run-current; BindingError on unavailable or no_binding
def parse_time(value: object) -> datetime | None             # never raises; the one time rule of section 7.2; used by read_transcript_tail and parse_worker_show (and so by collect)
def parse_worker_show(run: str, list_row: object, show: object | None) -> OrcaObservation   # never raises; the show value wins; sets dispatch_started, dispatch_ended, dispatch_status through parse_time
def collect(ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget) -> SweepInput

# disk and git readers called only by collect; each returns data plus a SourceCoverage row, never raises past collect
def read_worktree(path: Path, budget: Budget) -> tuple[WorktreeState, SourceCoverage]
def parse_status(raw: str) -> StatusParse                    # NUL fields, rename pairs, branch header (M7)
def read_packages(worktree: Path) -> tuple[PackageRecord, ...]
def read_ledger(path: Path) -> bool | None                   # has a FINAL: line; head 512 KiB + tail 512 KiB over 1 MiB
def read_contract(path: Path) -> ContractRecord | None       # None plus "over 1 MiB" coverage when too large
def read_transcript_tail(path: Path) -> TranscriptTail       # last 256 KiB, first partial line dropped; sets first_record_ts, last_record_ts and tail_complete (times via parse_time)
def read_tab_map(state_dir: Path) -> tuple[TabMapEntry, ...]
def read_orca_version(path: Path = ORCA_VERSION_FILE) -> str | None
```

`classify.py` (pure)

```
@dataclass(frozen=True)
class Rule:
    name: str
    match: Callable[[SessionRow, SweepContext], Classification | None]

RULES: tuple[Rule, ...]                      # 9 rules, order in section 7.2
def classify(row: SessionRow, ctx: SweepContext) -> Classification
def policy_of(row: SessionRow) -> str | None # "frozen" or None, independent of class (GQ-96)
def package_state(pkg: PackageRecord) -> str
def mark_shared_packages(worktrees: tuple[WorktreeState, ...]) -> tuple[WorktreeState, ...]
def safe_to_close(row: SessionRow, worktree: WorktreeState | None) -> SafeToClose
def removable(worktree: WorktreeState) -> tuple[str, str]  # ("no", "<first FR-013 condition>") or ("could not determine", reason)
def classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult
```

`report.py` (pure)

```
CHECKED_ORCA_VERSION: str = "1.4.245"
CELL_MAX: int = 200                          # SP-23 (D4)
SECTIONS: tuple[Callable[[SweepResult, SweepContext], str], ...]   # order of section 7.5
def sanitize(text: str) -> str
def cell(text: str) -> str                   # sanitize, then cut to CELL_MAX ending "..."
def render(result: SweepResult, ctx: SweepContext) -> str
def to_json(result: SweepResult, ctx: SweepContext, report_path: str) -> dict[str, object]
```

`commands.py` (impure shell)

```
sweep_group: click.Group                     # "sweep"
def run(run_ids: tuple[str, ...], window: str, root: str | None, output: str | None) -> None   # "sweep run"
def _parse_window(text: str) -> timedelta    # FR-003; click.UsageError -> exit 2
def _find_root(start: Path) -> Path          # FR-004 walk, plain stat only
def _check_output(output: Path | None, root: Path, inputs: tuple[Path, ...]) -> Path   # FR-004 containment
def _check_run_ids(values: tuple[str, ...]) -> tuple[str, ...]   # regex from step 1.0a, deduplicated
def _publish(text: str, output_dir: Path, now: datetime) -> Path  # section 3.2, the one write
```

Exit mapping in `commands.run`: `click.UsageError` and `BindingError` give exit 2 with the message; `ValueError` from an allowlist check, any other exception, and every `_publish` failure give exit 1 with a `[sweep <stage>]` stderr prefix (FR-018). Only `commands.run` calls `sys.exit` or raises `click` exit types.

### 7.2 Data model

All types are frozen dataclasses in `models.py`, as SPEC section 7 (lines 227-243) lists them. Class and state names are `str` constants collected in tuples. This design keeps every SPEC field and adds only the items marked (design).

| Type | Fields (SPEC section 7 unless marked) |
|---|---|
| `SweepContext` | `now`, `window`, `window_start = now - window`, `root`, `runs` |
| `SweepInput` | `orca_rows: tuple[OrcaObservation, ...]`, `contracts`, `transcripts: tuple[TranscriptTail, ...]`, `tab_map: tuple[TabMapEntry, ...]`, `worktrees: tuple[WorktreeState, ...]`, `sources: tuple[SourceCoverage, ...]`, `orca_available: bool`, `orca_binary: str`, `orca_version: str \| None`, `truncated: bool`, `collected_start: datetime`, `collected_end: datetime` (aware UTC, see Time parsing below; field names other than the last two are design) |
| `OrcaObservation` | SPEC list (line 231) plus `dispatch: str`, `run: str`, `session_join: str \| None` (design: the Orca-side join value, section 2.2 path A or B; None until step 1.0a names the field), `dispatch_started: datetime \| None`, `dispatch_ended: datetime \| None`, `dispatch_status: str \| None` (design: from `worker-show` `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status`, names read statically from the Orca 1.4.245 bundle and UNVERIFIED until step 1.0a item 4 (open item 23); all three are None for a row with no `worker-show` result, such as a row past the 50-call cap or a `call_failed` show) |
| `ContractRecord` | `path`, `worker_status`, `blocked_question`, `reason`, `report_path`, `artifacts`, `command` |
| `TranscriptTail` (design) | `path`, `session_id: str \| None`, `readable: bool`, `last_record_ts: datetime \| None`, `first_record_ts: datetime \| None` (the earliest `timestamp` among the complete records in the tail; for a file over 256 KiB this is not the session start), `tail_complete: bool` (True when the read began at byte 0, so the first complete record is the file's first; False when the read began later and the first partial line was dropped, which is every file over 256 KiB), `mtime: datetime`, `project_key: str` |
| `TabMapEntry` (design) | `file_name` (pane key with `:` written as `+`), `session_id`, `launch_dir`, `terminal_handle` (the three lines of the ccsession file) |
| `SessionRow` | SPEC list (line 235): `id`, `person_started`, `orca`, `contract`, `transcript_path`, `transcript_readable`, `last_activity`, `gate_policy`, `row_id`, the ten #409 dimensions |
| `StatusParse` (design) | `entries: tuple[tuple[str, str], ...]` (XY code, path), `branch_header: str`, `ahead: int \| None`, `has_upstream: bool \| None`, `header_note: str \| None` |
| `PackageRecord` | `id`, `location`, `has_final_line`, `archiving_marker`, `active`, `state` |
| `WorktreeState` | `path`, `status_read`, `uncommitted`, `unpushed: bool \| None` (M7, section 2.2), `dev_tasks_unsaved`, `changed_paths`, `packages`, `shared_package_ids`, `frozen`, plus `upstream_note: str \| None` (design: `ahead N`, `no upstream`, `detached HEAD`, `upstream gone`, `no commits yet`) |
| `Classification` | `class_name` (JSON key `class`), `waiting_kind`, `rule`, `evidence`, `notes` |
| `SafeToClose` | `terminal`, `worktree`, `reason` |
| `SourceCoverage` | `name`, `coverage`, `age_seconds`, `unscanned` |
| `SweepResult` (design fields) | `rows: tuple[ClassifiedRow, ...]` (row plus `Classification`, policy and `SafeToClose`), `worktrees` (after `mark_shared_packages`, with `removable` and `removable_reason`), `waiting_a`, `waiting_b` (row ids), `summary` (counts per class with zeros, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`), carried header data from `SweepInput` |

Time parsing (design): every Orca and transcript time is parsed to an aware UTC `datetime`. Accepted forms are SQLite `YYYY-MM-DD HH:MM:SS` (no zone, read as UTC; the form `datetime('now')` writes) and ISO 8601 with `Z` or an offset (`Z` is rewritten to `+00:00` first, because Python 3.10 `datetime.fromisoformat` does not accept `Z`). An unparseable or missing value is None and raises nothing (the "Unknown row schema" bullet below). One function, `probes.parse_time` (section 7.1), applies this rule; `read_transcript_tail` and `parse_worker_show` both call it. The times the sweep itself creates are aware UTC `datetime` values too: `now`, `collected_start`, `collected_end` and `TranscriptTail.mtime`. `collected_start` is read once at the top of `collect`, before the first Orca call, and `collected_end` once when `collect` returns. A naive value never reaches `classify`.

Constants in `models.py`: `JSON_SCHEMA_VERSION = 1`; `CLASSES` (`waiting on a person`, `stalled (proved)`, `fenced`, `working`, `finished`, `idle`, `person session (active)`, `could not determine`); `PACKAGE_STATES` in precedence order (`conflict`, `interrupted-archive`, `archive-blocked`, `unfinished`, `archived`, `unknown`); `SAFE_VALUES` (`yes`, `no`, `could not determine`).

Rule table (`classify.RULES`, SPEC section 7 lines 247-257; numbering is the SPEC's 1 to 9, per M10):

| Order | `Rule.name` | Class |
|---|---|---|
| 1 | `blocked_contract` | waiting on a person (a) |
| 2 | `orca_exit_proof` | stalled (proved) |
| 3 | `fenced` | fenced |
| 4 | `waiting_signal` | waiting on a person (a) or (b) |
| 5 | `working` | working |
| 6 | `finished` | finished |
| 7 | `idle` | idle |
| 8 | `person_active` | person session (active) |
| 9 | `fallback` | could not determine |

Rule conditions are the SPEC table text. Three readings are fixed here:

- Rule 1 notes (M6): a decline under `ask the coordinator` on a live unsettled row adds the note `blocked contract under ask the coordinator; may be re-running`; a decline with `gate_policy` None on a live row adds the same note; a contract with no Orca row declines with `blocked contract; Orca state not observed` unless a Ruling halt matches.
- Rule 5 (SP-24), one condition per line: `liveness_verdict == "live"`; `status == "in_progress"`; `agent_wait_present is True`; `agent_wait is None`. All four must hold once the names are known. Until step 1.0a item 4 records them (open item 6) Rule 5 is inert: it returns None and a row that would reach it falls to the fallback, and these four conditions are kept in `classify.py` as the text to restore. Field sources (the `worker-show` field names, the `live` and `in_progress` values and the `agentWait` key are NOT yet captured, UNVERIFIED): `liveness_verdict`, `status`, `agentWait` presence and value would come from `worker-show`; `worker_done_seen` is None on every live row; `fenced_evidence` is `unreadable` on every live row (SPEC line 231).
- Age (SP-26, D5): a `last_activity` or waiting timestamp later than `now` is unknown age, adds note `timestamp in the future`, and never satisfies rule 7.

Joins (GQ-108, SP-16, SP-29):

- `row_id` is `orca:<dispatch>` or `transcript:<session_id>` (SPEC line 236).
- A transcript joins an Orca row when its `sessionId` equals that row's `session_join` value (path A), or when a tab-map entry whose `session_id` equals the transcript `sessionId` has a `file_name` or `terminal_handle` equal to the row's `session_join` (path B). Which path applies, and the Orca field behind `session_join`, are decided from the step 1.0a capture (section 17).
- A worker, for FR-010, is a transcript that joins a Dispatch row of a scoped Run by path A or path B. A tab-map entry counts only through that join. A joined transcript is `person_started` False, and it is shown as the Orca row `orca:<dispatch>`, not as a separate transcript row (FR-010: a positive join makes it False). Under path B the join names the pane's latest session only, because the tab map keeps one session per pane and `/clear`, a resume or a person running the command again in the tab replaces it (`ccsession:574-602`, `:607-613`). A path-B join therefore also needs session identity: `first_record_ts`, cut to whole seconds, must fall inside the row's window, from `dispatch_started` to `dispatch_ended`, both ends included, or to `collected_start` when `dispatch_ended` is None and `dispatch_status` is `pending` or `dispatched`. Times are compared as UTC instants. A row whose `dispatch_started` is None, or whose `dispatch_status` is anything else while `dispatch_ended` is None, has no observable window. When the window is observable but the transcript has `tail_complete` False, the session start is not observable: `first_record_ts` is only the first record of the tail, so it can place a later session inside the window or an earlier one outside it. That match does not join: the row is could not determine with note `session start not observable: transcript tail only`, and that transcript is None with the same note. The names behind the three fields come from the static bundle read and are UNVERIFIED until step 1.0a item 4 confirms them (open item 23). Clock skew or the seconds cut can only move a session to could not determine or False, never to True. A path-B match outside that window does not join: the row is could not determine with note `pane moved to a later session` when `first_record_ts` is after the window end, and with note `session started before this Dispatch window` when it is before `dispatch_started`. A match on a row with no observable window does not join: the row is could not determine with note `Dispatch time window not observable`. Several matching rows follow the R3-B2 rule below. A path-B join inside the window is False and carries note `joined by pane: latest session of the pane`, because a person rerun inside the window cannot be told apart. Several scoped Dispatch rows can match one tab-map entry by path B (a reused pane or two rows on one terminal handle). Rows that share one Dispatch id are merged first (the Duplicate Dispatch bullet below): the merged identity counts as one matching row, has no observable window, and keeps its reason `conflict: duplicate Dispatch rows disagree`. If the transcript has `tail_complete` False, the several-rows rule does not apply and no window is tested: every matching row with an observable window is could not determine with `session start not observable: transcript tail only`, every other matching row is could not determine with `Dispatch time window not observable`, and the transcript is None with the tail-only note when at least one matching row has an observable window, else with `Dispatch time window not observable`. The rest of this paragraph applies only when `tail_complete` is True. A matching row that does not hold the transcript gets `pane moved to a later session` when `first_record_ts` is after its window end, `session started before this Dispatch window` when it is before its `dispatch_started`, and `Dispatch time window not observable` when it has no observable window. The result does not depend on row order, and no row wins by position (as for duplicate Dispatch rows, in the Duplicate Dispatch bullet of this section). If exactly one matching row's window holds the transcript, the transcript joins that row only and is False with note `joined by pane: latest session of the pane`; each other matching row is could not determine with the note for its case above, and those notes are not added to the transcript. If two or more matching rows' windows hold it, it joins none of them: each of those rows is could not determine with note `conflict: one pane session matches several Dispatch rows`, the other matching rows get the notes above, and the transcript is None with the `conflict:` note. If no matching row's window holds it, every matching row is could not determine with its note, and the transcript is None with the first of `pane moved to a later session`, `session started before this Dispatch window` and `Dispatch time window not observable` that any matching row received (the last when no matching row has an observable window). A join outcome that makes a row could not determine is applied after rules 1 to 8: it replaces their class with rule `fallback` and keeps the rule's own evidence in `evidence`, so a `completed` row with a settled contract is could not determine, not `finished`. A transcript with a tab-map entry that joins no row because of the tail, window or several-rows rules takes these notes instead of `Orca pane session, not in scoped Runs` (in the bullet that follows this one). Two limits are accepted here and stated for the owner in D9. First, an open window has no upper bound: while a row stays `pending` or `dispatched`, a later session of the same pane that a person starts, for example by running the command again after the worker died, falls inside the window and joins as False, shown as `orca:<dispatch>`, and the worker's own session is None. Second, a second Dispatch sent to an agent still running in the pane does not start a new session: that session joins the older row whose window holds its first record, and the newer row, which the session may be serving, is could not determine with `session started before this Dispatch window`.
- A tab-map entry alone does not make a worker, because the file cannot tell a worker pane from a person pane (section 1). A transcript whose tab-map entry joins no scoped Orca row may be a person's pane or a worker of a Run outside the scope, whose rows Phase 1 does not read. It gets None with note `Orca pane session, not in scoped Runs` (D9).
- Under path A only, a transcript with no tab-map entry that joins no scoped Orca row may be True when the FR-010 guard holds. Under path B, when any scoped Dispatch row exists, this True path never applies (fourth guard case below). Having no entry does not prove the session ran outside Orca: a plain `claude` launch and an earlier session of a reused pane have none (section 1). A worker of an unscoped Run can therefore reach True this way. D9 records this narrowing of SP-29. Every True reached this way carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and in the JSON `notes`, so such a session is never shown as person-started without a note.
- List-incomplete cases (SPEC FR-010): no transcript can be proved unjoined when the Orca worker list or the tab map is incomplete. There are five cases: four are the SPEC reasons (Orca unavailable, worker list truncated, worker list call failed, tab map unreadable) and one is added by this design (Run not confirmed). `classify_all` evaluates all five from `orca_available`, `truncated`, `orca_rows` and `sources` only. First, Orca is unavailable (`orca_available` False). Second, any scoped Run's worker list is truncated (`truncated` True: a full page of `WORKER_LIST_PAGE` rows whose continuation is not read). Third, any scoped Run's `worker-list` result is `call_failed`: its `sources` row `orca worker-list <run>` has `unscanned` set while `orca_available` is True. Every Run in `ctx.runs` has that row, a call cut by the time budget counts, and a Run whose `worker-list` was never started because the budget ran out carries `unscanned: time budget reached (90 s)` and counts as `call_failed` for this rule. While `orca_available` is False the outage note alone covers the unavailable case: the Orca sources left unread after an outage are marked `unscanned: orca unavailable` (section 5) and do not also count as `call_failed`. Fourth (the design addition), a scoped Run is not confirmed: its `orca worker-list <run>` row has no `unscanned` and no `OrcaObservation` has that Run, while its `orca task-list <run>` row (the `task-list --run <run>` call) has `unscanned` set, again only while `orca_available` is True. An unknown Run id gives a complete, empty `worker-list` with exit 0 and `ok` true (read-only live read on 2026-11-08; the shape stays UNVERIFIED until step 1.0a item 8, open item 4), while `task-list --run <id>` returns `run_not_found`. A real Run with zero rows whose `task-list` did not fail is complete and is not this case. Fifth, the tab map is unreadable: `collect` set `unscanned` on the source row `ccsession orca-tabs` (the folder exists but cannot be listed or read; a missing folder and an empty readable folder are readable and are not this case). Every unjoined transcript is then None with every note that holds, attached in this order: `origin unknown: Orca unavailable`, `origin unknown: worker list truncated`, `origin unknown: worker list call failed`, `origin unknown: Run not confirmed`, `origin unknown: tab map unreadable`, all before any join-guard note (next bullet). It prints could not determine and is never idle or Historical, even when its activity is older than the window.
- The guard's "join completed" condition fails, and every unjoined transcript is None, in four cases. First, `session_join` is None on any scoped Dispatch row: note `tab map join not observable` (section 2.2). Second, Orca returned at least one worker row and no transcript joined any Orca row (SPEC line 236, SP-16); a transcript that matched a tab-map entry of a scoped Dispatch row and was left unjoined by the tail, window or several-rows rules carries its pane or tail note only, not the SP-16 line. Third, under path B, a scoped Dispatch row's `session_join` matches no tab-map entry, so that worker's transcript could be any unjoined one. Fourth, under path B, at least one scoped Dispatch row exists. The tab map holds only each pane's latest session, so an earlier session of the same pane, which may be that worker's own transcript after a `/clear`, a resume or a person rerun, has no entry. Every unjoined transcript with no tab-map entry is then None with note `earlier pane session not joinable (tab map keeps only the latest session)`. When the first and second cases hold together, the transcript carries the SP-16 literal first and then `tab map join not observable`. In the second and third cases, Could not determine also prints the line `could not join Orca workers to transcripts (tab map empty or stale)`, and each affected transcript carries it as its note; the line is not printed when every affected transcript is one that the second case leaves with its pane or tail note only.
- The SPEC's `worker of Run <id>, outside scope` False path needs a Run id in the tab map, which the ccsession file does not hold (section 1), so that path does not occur in Phase 1.

Observation rules (SPEC section 11 failure modes and the section 7 cross-cutting note). Each one leaves the run at exit 0:

- WC-13: an Orca row with a non-null `parent` adds note `WC-13 violation, review` (SPEC line 261, GQ-40). The note does not change the class. The row is also listed under `## Retained problems` (SPEC line 380).
- List and show disagree: the `worker-show` value wins for every field both return. A `worker-list` row with no `worker-show` result is could not determine (WC-10), never stalled (SPEC line 443).
- Unknown row schema: a missing `worker-show` key leaves that field None (`unknown`) and raises nothing; an extra key is ignored (SPEC line 446).
- Duplicate Dispatch: rows that share one Dispatch id but differ in state are merged into one `orca:<dispatch>` identity. That row is could not determine with reason `conflict: duplicate Dispatch rows disagree`. No row wins by position (SPEC lines 319 and 452). The merge comes before every join rule: the merged identity counts as one row in the several-rows rule, and its `dispatch_started`, `dispatch_ended` and `dispatch_status` are None, so it has no observable window.
- Input changed between reads: each file reader records `(st_size, st_mtime_ns)` before and after it reads. If they differ, it reads the file once more while the budget allows. If the second read also changes, or no budget is left, the row is could not determine with reason `conflict: inconsistent observation` (SPEC line 451).
- Path escapes its source: every discovered input path is passed through `Path.resolve()`. It must stay under the folder it was found in: the root, a scanned project-key folder or the `orca-tabs/` folder. A path that escapes is not read, and its source is reported `unscanned: outside root` (SPEC line 450; REPORT step 1.6).
- Worktree removed mid-sweep: a `_git` error or an `os.stat` failure on a worktree path makes that worktree could not determine with `unscanned: worktree not readable`. The other worktrees continue (SPEC line 440).
- Unreadable transcript or contract: a transcript is unreadable when its open raises `OSError`, or when its tail read (`read_transcript_tail`, the last 256 KiB with the first partial line dropped) holds no complete JSON record with both `timestamp` and `sessionId`. That covers a truncated or malformed JSONL. A last line cut mid-object is skipped, and the transcript stays readable when an earlier complete record has both fields. Either case sets `transcript_readable` False. A contract is unreadable when its open raises `OSError`. Rules 2 and 1 then decline, and the row is could not determine with note `unscanned: transcript not readable` or `unscanned: contract not readable` (SPEC line 442).
- Rule 6 wording: a finished row's JSON values and report text never contain `admitted` or `accepted`. A contract body whose later line quotes `guard refused:` is not finished (SPEC line 259, SP-07).
- `FINAL:` counts only at the start of a line, after optional leading whitespace. `FINAL:` inside other text does not make `archive-blocked` (SPEC line 269, GQ-105).
- Remote hosts: `## Source coverage` always has a row `remote hosts` with coverage `unknown`. The Scope line's session count is followed by `(lower bound: remote hosts not scanned)`. The report never says there are no sessions (SPEC line 454).

### 7.3 Allowlist constants

All in `probes.py`. Templates are tuples of tokens; `<run>` and `<dispatch>` are placeholders that match only the id regexes `RUN_ID_RE` and `DISPATCH_ID_RE`, which are fixed from the step 1.0a capture (UNVERIFIED today, section 17). Matching is token for token over the whole argv after argv[0]: same length, same literal tokens, placeholders matched by regex. No prefix match (NFR-003).

```
ORCA_BINARY_DEFAULT = "orca-ide"            # never bare "orca" (SPEC section 8, INV-017)

ALLOWED_ORCA: tuple[tuple[str, ...], ...] = (
    ("orchestration", "run-current"),
    ("orchestration", "worker-list", "--run", "<run>", "--json"),
    ("orchestration", "worker-show", "--dispatch", "<dispatch>", "--json"),
    ("orchestration", "task-list", "--ready", "--run", "<run>", "--json"),
    ("orchestration", "task-list", "--run", "<run>", "--json"),
    ("worktree", "ps", "--json"),
    ("worktree", "list", "--json"),          # pinned, not called in Phase 1
    ("worktree", "current", "--json"),       # pinned, not called in Phase 1
    ("worktree", "ps", "--agent-wait"),      # allowed by R5 (owner 2026-11-08), not called in Phase 1
    ("worktree", "ps", "--agent-wait", "--json"),   # allowed by R5 (owner 2026-11-08), not called in Phase 1
)                                            # 10 templates, 7 verbs (NFR-014)

FORBIDDEN_TOKENS = frozenset({"--include-remote"})   # rejected in any position

ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
    ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all",
     "--ignore-submodules=all"),
    ("config", "--show-origin", "--list", "-z"),
    ("ls-files", "-z"),
    ("check-attr", "--stdin", "-z", "filter"),
)                                            # the seam prepends git --no-optional-locks -C <path> -c core.fsmonitor=false

ORCA_VERSION_FILE = Path("/opt/Orca/resources/app.asar.unpacked/out/package.json")
OUTPUT_LIMIT = 8 * 1024 * 1024               # subprocess stdout + stderr
CONTRACT_LIMIT = LEDGER_LIMIT = 1024 * 1024  # hit when size > limit
LEDGER_SPLIT = 512 * 1024                    # head and tail read of a ledger over the limit
TRANSCRIPT_TAIL = 256 * 1024
WORKER_LIST_PAGE = 100                       # a full page sets truncated
```

The FR-021 forbidden verb list (`check`, `ask`, `reply`, `send`, `inbox`, `open`, `worker-start`, `task-create`, `task-update`, `dispatch`, `stop`, `rm`) lives in the test, not in `probes.py`, so the package holds no write verb even as a string.

Decision on `worktree list` and `worktree current` (M3): they stay in the pinned set because the owner sign-off for INV-005 condition 1 names exactly these seven verbs and, since R5 (owner 2026-11-08), ten templates (NFR-014), and dropping them would need a second owner note. Phase 1 code does not call them: worktree discovery uses `worktree ps --json`, and the root comes from the FR-004 path walk. The NFR-003 full-sweep recording test asserts zero argv for both, and also for both `worktree ps --agent-wait` templates, so all four templates marked "not called in Phase 1" are never issued by a sweep. That wording is a design statement; R5 only allowed the two `--agent-wait` templates. The decision is revisited after step 1.0a only if `worktree ps --json` lacks the worktree path field.

`run-current` has no `--json` (M2). If the step 1.0a capture shows it needs `--json` for a parseable result, that is a template change and needs the same owner note as any other allowlist change; until then the parser reads the captured plain shape.

The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320).

### 7.4 JSON schema v1

One object on stdout, printed only after the commit point (section 3.2). Every key is always present; an unknown value is `null`, an empty list is `[]`, and class counts include zeros (SPEC section 5.2, line 392). Built by `report.to_json` from `SweepResult` only. Values are sanitized (FR-016) but never cut (SP-23).

```
{
  "schema_version": 1,
  "observed_at": "<UTC ISO 8601, ctx.now>",
  "collected": {"start": "<UTC ISO>", "end": "<UTC ISO>"},              # design addition, additive
  "scope": {"runs": ["<run>", ...], "root": "<path>", "worktrees": <int>},
  "window": "<6h>",
  "orca_available": <bool>,
  "sources": [{"name": str, "coverage": str, "age_seconds": int|null, "unscanned": str|null}, ...],
  "rows": [{
      "row_id": "orca:<dispatch>" | "transcript:<session_id>",
      "class": str, "waiting_kind": "a"|"b"|null, "rule": str,
      "evidence": str, "notes": [str, ...], "policy": str|null,
      "person_started": bool|null,
      "safe_to_close": {"terminal": str, "worktree": str, "reason": str|null}
  }, ...],
  "worktrees": [{
      "path": str, "status_read": bool, "uncommitted": bool|null, "unpushed": bool|null,
      "dev_tasks_unsaved": bool|null, "frozen": bool|null,
      "packages": [{"id": str, "location": "to-do"|"done"|"both", "state": str}, ...],
      "shared_package_ids": [str, ...], "removable": str, "removable_reason": str|null
  }, ...],
  "waiting": {"a": ["<row_id>", ...], "b": ["<row_id>", ...]},
  "summary": {
      "counts": {"<class>": int, ...},                   # every class in CLASSES, zeros included
      "bound_reached": int, "visible": int, "historical": int, "total": int,
      "total_is_lower_bound": bool
  },
  "report_path": "<absolute path of the published report>"
}
```

Every Run in `ctx.runs` has its own source row named `orca worker-list <run>` and another named `orca task-list <run>` (the `task-list --run <run>` call); `orca` there is the literal word, not `$ORCA_CLI_COMMAND`. A `call_failed` result sets the row's `unscanned` reason (for example `orca call failed (exit 1)`), and a Run whose call was never started because the time budget ran out gets `unscanned: time budget reached (90 s)` on the row. `collect` sets `truncated` when a Run's `worker-list` returns `WORKER_LIST_PAGE` (100) rows. The tab-map folder has the row `ccsession orca-tabs`. The list-incomplete rule of section 7.2 reads these rows.

Pinned v1 key set (NFR-009 golden test): the SPEC top-level keys (`schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`, `rows`, `worktrees`, `waiting`, `summary`, `report_path`), the SPEC row keys (`row_id`, `class`, `rule`, `evidence`, `notes`, `safe_to_close`), the SPEC worktree keys (line 392) and the SPEC summary keys. The design additions `collected`, `waiting_kind`, `policy`, `person_started` and `summary.counts` as the container for per-class counts are in the v1 set from the first release, so they are additive, not a later change. `rows[].class` values are the `CLASSES` strings; `unpushed` is a bool or null, never a count (M7). `safe_to_close.worktree` is never `"yes"` (FR-012). NFR-005: two renders from one fixture give equal JSON apart from `report_path`.

### 7.5 Report layout

The layout is SPEC section 9 (lines 342-392), copied from #409 at `495eb96d` because #409 is unmerged. `render(result)` joins the output of each function in `SECTIONS`, in this order, and returns one string ending in `Report complete\n`. Every function is pure over `SweepResult`; no function reads a clock, a file or an environment variable.

```
READ ONLY . observed <UTC ISO> . collected <start> to <end> (not an atomic runtime snapshot)
Scope: Runs <ids> . worktrees <n> . sessions <shown>/<total> (lower bound: remote hosts not scanned) . window <6h>
Orca binary: <resolved binary name>
Sources: <name> <coverage> (age <s>s) . ...
Messages coverage: partial
Orca lock risk: unlikely (checked for Orca 1.4.245)
            or: UNVERIFIED (checked for Orca 1.4.245; observed <version or unknown>)
Untracked paths: listed per file (--untracked-files=all); not observed in a worktree whose status was unread
[child worktrees not discovered: Orca unavailable; worktree count is a lower bound]     (Orca unavailable)
[child worktrees not discovered: orca worktree ps unscanned (<reason>); worktree count is a lower bound]     (Orca answered but the worktree list is incomplete: truncated, call failed or budget)
[Show cap or time budget reached; row total is a lower bound]                           (bound_reached >= 1)
[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]                (full worker-list page)

## Source coverage
## Waiting on a person (a)
| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |
Seen is not resolved
Answered: could not determine
## Waiting on a person (b)
### Ready Tasks needing ownership review (creator not observable in Phase 1)
Ready Tasks: <N>
## Could not determine
## Retained problems
## Sessions (<shown>/<total>)
Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.   (SP-24, D7)
## Worktrees
## Historical sessions
## Shift Brief
## What I could not determine
Inspection only.
<source list>
Report complete
```

Rules the renderer applies:

- `SECTIONS` is a tuple of 12 functions (header, source coverage, waiting a, waiting b, could not determine, retained problems, sessions, worktrees, historical, shift brief, what I could not determine, footer). A later phase appends a function; it does not edit one.
- Waiting (a) rows sort oldest first, then rows of unknown age. Waiting (b) lists frozen-plan rows, then the Ready Tasks sub-heading and its count line.
- The Sessions table has the ten #409 dimensions, then `Class`, `Rule`, `Evidence`, `Safe to close (terminal / worktree)`, `Notes`, `Next inspection`. The `next inspection` value comes from a fixed map keyed by rule name in `report.py` and names only a read or check (for example "read the worker's last transcript lines"). It is never empty and never names stop, retry, release, merge or removal (SPEC line 388).
- The exact cap wording for the `bound_reached` line is the design's; the SPEC fixes only its meaning (FR-020). The test pins the design's string.
- An empty section prints `No matching records. This is not an all-clear.` Every count over sessions prints `Distinct affected sessions: <N> (set union, not a sum)`.
- Every table cell goes through `cell()`: `sanitize` first, then a cut at `CELL_MAX` (200) characters ending in `...` (SP-23, D4). JSON values are never cut.
- The report holds no action control, no command to paste and no advice to delete anything under `.dev/tasks/`.

### 7.6 Command and skill surface

Two new primitives, edited in `src/superclaude/` and copied by `make sync-dev`. Neither names a `src/superclaude/` path (NFR-011).

**Command** `src/superclaude/commands/sweep.md` (installs to `~/.claude/commands/sc/sweep.md`):

- Frontmatter: `name: sweep`, a one-line description, `allowed-tools: Skill`, and an `argument-hint` of `[--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]`.
- Body headings follow `issue.md` (title, Triggers, Usage, Options), with an `## Activation` block in the form `graph.md` uses (`graph.md` line 9 has `allowed-tools: Skill, ...`, line 41 `## Activation`). The block invokes `~/.claude/skills/sc-sweep-protocol/SKILL.md`, and names the project `.claude/skills/sc-sweep-protocol/SKILL.md` copy as the dual surface (skills read `~/.claude/skills/` first).
- Triggers: explicit only. No `## Unattended mode` section, no `--unattended` flag. `sweep.md` has no `## Unattended mode` section. `/sc:sweep` is on the never-as-worker list (section 8).

**Skill** `src/superclaude/skills/sc-sweep-protocol/SKILL.md`:

- Frontmatter `allowed-tools: Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read`.
- Steps: (1) run `superclaude sweep run <args>` with Bash timeout 120000 ms; (2) only when that fails with "command not found", run `uv run --frozen --no-sync superclaude sweep run <args>` with the same timeout; (3) on exit 0, parse the stdout JSON, take `report_path` and `summary` only, and Read the report at `report_path`; (4) print the counts from `summary` and the report path; (5) on exit 1 or 2, print the stderr line and stop.
- The skill prints no recommendation, proposes no action and never edits, stages or deletes a file. This is narrower than REPORT step 1.15 (section 13, REPORT differences).
- The fallback literal contains `--no-sync` and `--frozen`; both flags appear in `uv run --help` (SPEC FR-022). Their effect was not run here (open item).

**Test** `tests/commands/test_sweep_command.py` asserts: the two `allowed-tools` literals exactly; the installed skill path and the dual-surface path in the Activation block; the PATH-first order and the "command not found" trigger; `--no-sync` in the fallback literal; timeout 120000; no `## Unattended mode` heading; no `src/superclaude/` substring in either file; and no stop, retry, release, merge or removal advice in the skill text.

## 8. WC-16 and the never-as-worker list

**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and step 1.16a has written its record. Step 1.16a is record-only: PR #422 is merged on master (merge commit `2327fbd3`), so the step waits for nothing and writes `artifacts/pr422-409-check.md` with four points (see section 15.2); the gate on step 1.17 is satisfied as soon as that record exists. R1, R2 and R8 name WC-16 and the never-as-worker entry, so steps 1.21 and 1.24b are gated on steps 1.18 and 1.17 and so on the same answer (section 15.2). WC-16 and its pins stay deliverables of this PR whatever #422 does (SPEC line 420). WC-14 and WC-15 on master are worker duties from PR #434 and are not changed.

**Placement.** `src/superclaude/core/WORKER-CONTRACT.md`, a new subsection after the fan-in rule paragraph (line 273) and before `### Worked example: gate hit, answer, new Task` (line 275).

**Final text.** The SPEC section 10 text (lines 404-408) with four changes, all deviation D6: the heading is renumbered WC-16 (R4); the cadence clause of contract line 110 is added and "It sweeps on every wake" is dropped, because master already bounds the sweep to at most once every 5 minutes (R4); `/sc:sweep` is written as an added read beside the unchanged line 110 sweep, not a replacement, with one sentence that its own reads are not L1 probes and do not count against the L1 cap (R4); and one sentence is appended at the end (SP-27). Master's sweep is "The sweep." in the contract; the text calls the command `/sc:sweep` and uses "The sweep." only for master's sweep. The additive reading and the L1 sentence are part of the proposed WC-16 text and wait for the owner's approval of that text with GQ-11 (step 1.0b). WC-16 does not reword contract line 110 (the sweep) or line 151 (the L1 probe row):

```markdown
### WC-16. Coordinator loop

The coordinator keeps watching its Run until every Task it created is settled and every result has been inspected and its admission or rejection recorded. It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake or wait timeout, at most once every 5 minutes, the coordinator runs "The sweep." under `### Liveness supervision` unchanged and, in the same pass, runs `/sc:sweep` and reads its report before it acts. `/sc:sweep` is an added read: it does not replace that sweep, it is not a second pass, and it does not update heartbeat records or run the `worktree ps --agent-wait` listing. Its own reads are not L1 probes and do not count against the L1 cap; the coordinator's own L1 probes stay limited to workers a trigger fired for. The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler. The `/sc:sweep` classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. A missing heartbeat is absence, never death. The coordinator escalates to the person, and does not act alone, on: a failed or blocked result it cannot retry under WC-6, a partial result it judges unusable, a third brief-guard refusal, a ready Task it did not create, needing ownership review, a frozen plan, and a fan-in with fewer than 2 admitted inputs. Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged. The `/sc:sweep` report is a dated local file; it is never posted. `/sc:sweep` recommends nothing: no stop, retry, release, merge or removal. The coordinator decides and performs any action under those rules. The coordinator records each admission or rejection in its run notes; `/sc:sweep` does not observe them.
```

The appended sentence closes a gap the panel found (SP-27): the end condition names "admission or rejection recorded", but `/sc:sweep` has no source for that record, so the text says where it lives and that `/sc:sweep` cannot see it. It adds no pin. The text holds no lock sentence (SPEC line 410).

**Pins** (five edits) in `tests/skills/test_worker_contract.py`:

- Add to `RULE_PHRASES` (the dict at line 25), after the `"WC-15"` entry (lines 165-172) and before the `"heartbeats"` entry (line 173): `"WC-16": ("WC-16", ["WC-16. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"])`. Each phrase occurs verbatim in the final text above.
- Append `"/sc:sweep"` to `NEVER_AS_WORKER` (lines 382-391), giving 9 entries. The parametrized removal test at lines 1081-1082 then covers it with no further change.
- Rename `test_never_as_worker_list_names_all_seven_commands` (line 912) to `test_never_as_worker_list_names_every_listed_command`. The body is unchanged.
- Add `assert "sweep" not in UNATTENDED_COMMANDS` next to the existing `"load"` assertion (line 1322, inside `test_load_usage_line_declares_checkpoint_and_load_is_not_converted`, def at line 1318). The equality check at line 837 holds with no edit, because `sweep.md` has no `## Unattended mode` section.
- Change the `RULE_PHRASES["never-as-worker"]` phrase at line 89 from ``"`/sc:spawn` and `/sc:swarm-wizard`, "`` to ``"`/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, "``, so the pinned phrase matches the new contract line 23 below.

Steps 1.18 and 1.19 land in one commit. Once step 1.18 rewrites contract line 23, the old `never-as-worker` phrase is no longer a substring of the contract, so `test_contract_states_rule[never-as-worker]` stays red until pin 5 changes it; step 1.19 carries pin 5 (section 15.2).

**Constraints from master `5dc29d23`** (read in `tests/skills/test_worker_contract.py`; they add no pin and no deviation):

- `_check_p2_set` (line 1556) asserts `UNATTENDED_EXPECT` has exactly 31 entries, so `sweep` is never added to it.
- `_check_no_unattended_sections` (lines 831-839) globs every `src/superclaude/commands/*.md`, so `sweep.md` has no `## Unattended mode` section.
- The write-verb audit (`AUDIT_ROOTS`, lines 1940-1944; categories `wc9-allowed`, `deferred:P1` to `deferred:P4`, `never-worker`, `no-command` and `read-only`, lines 1953-1955) needs a `WRITE_VERB_CLASSIFICATION` row (the dict at line 2016) for any write-verb text in `sweep.md` or `sc-sweep-protocol/`. The `never-worker` category is available once `/sc:sweep` is on the never-as-worker list.
- A `read-only` `gh api` entry must not look like a post to `_is_gh_api_post` (line 1966).
- `RULE_PHRASES["liveness-sweep-and-states"]` (lines 209-219) and `RULE_PHRASES["liveness-ladder-and-restart"]` (lines 228-237) must not be reworded.
- `_check_rule` (lines 755-762) needs the rule ident on the heading line, so the WC-16 heading carries `WC-16`.

**Never-as-worker addition.** `WORKER-CONTRACT.md` line 23 becomes:

> - **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.

Only the command list changes. The term line stays one line, which `_check_never_as_worker` (line 765) requires. Adding `/sc:sweep` is a change to the coordinator-only command set, so it fits the line's own rule. The same list is copied in the developer guide (section 9).

## 9. Routing and documentation changes

All edits are to existing files; no new doc file. Rows and bullets are added, none removed or reworded.

| # | File | Change | Checked by |
|---|---|---|---|
| R1 | `src/superclaude/core/HOW-WE-WORK.md`, `<!-- other-commands:v1 -->` table (lines 318-337) | One row, placed after `/sc:spawn` (line 333): `` `/sc:sweep` `` with "Read-only supervision snapshot of the bound Orca Run, its worktrees and person-started sessions. Writes one dated report under `.dev/sweeps/` and prints JSON; it changes nothing else and recommends nothing. Coordinator or person only, never a worker." | `tests/core/test_how_we_work_routing_table.py` |
| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403): "**The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep."** WC-16 in `~/.claude/WORKER-CONTRACT.md` has the coordinator run `/sc:sweep` in that same pass and read its report before it acts. `/sc:sweep` adds to that sweep and does not replace it. It is read-only and is itself never a worker." | R1 test plus parity test |
| R3 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte copy of R1+R2 result, made in the same commit | `tests/commands/test_routing_plugin_parity.py` line 38 (`filecmp.cmp(..., shallow=False)`) |
| R4 | `tests/core/test_how_we_work_routing_table.py` `_OTHER_COMMANDS` (line 27) | Add `"sc:sweep"` | itself |
| R5 | `tests/recommend/test_routing_refresh.py` `_POST_REFRESH_ADDITIONS` (line 33) | `{"graph", "impact", "issue", "sweep"}` | itself (assertion at line 648) |
| R6 | `docs/user-guide/commands.md`, `### 8. UTILITIES` (line 105) | One row after `/sc:issue` (line 115): `` `/sc:sweep` `` . "Read-only snapshot of a Run, its worktrees and person sessions" . `sweep.md` . "Report only (writes `.dev/sweeps/`)" | manual review |
| R7 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 991 | Add `/sc:sweep` to the copied never-as-worker list, same order as section 8 | manual review against `WORKER-CONTRACT.md` line 23 |
| R8 | `CHANGELOG.md`, `## [Unreleased]` (line 5) | A `### sweep: read-only supervision snapshot (Phase 1)` heading under `## [Unreleased]` with a `#### Added (sweep)` sub-heading: `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-16, `.dev/sweeps/` ignored | manual review |

Rules:

- R1 to R4 land in one commit. Editing R1 or R2 without R3 fails the parity test, and a `/sc:sweep` row in R1 without R4 fails `test_other_commands_membership_and_live_references` in `tests/core/test_how_we_work_routing_table.py`, which asserts the table members equal `_OTHER_COMMANDS`.
- The level table is not touched, so the `src/superclaude/core/CLAUDE.md` level-table copy (project CLAUDE.md, Key Documentation Files) needs no re-run. If a later edit touches the level table, that copy is re-run in the same commit.
- R1 and R6 avoid the words stop, retry, release, merge and removal in the description of `/sc:sweep`.
- No `.claude/` path is staged; `make sync-dev` then `make verify-sync` (step 1.25) refresh the dev copies.

## 10. `.gitignore`

A grep on 2026-11-08 found no `sweeps` entry (SPEC FR-025). Two lines go after the `.dev/sprint-state/` entry (`.gitignore` line 254), next to the other `.dev/` operator-local entries:

```gitignore
# superclaude sweep reports: dated, operator-local, never posted (WC-16). Never tracked.
.dev/sweeps/
```

- The pattern names `.dev/sweeps/` only. It does not cover `.dev/tasks/`, which stays tracked and always staged (CLAUDE.md rule).
- The NFR-002 real-git test copies the repository `.gitignore` into its `tmp_path` repository and checks: `git check-ignore .dev/sweeps/x.md` succeeds; `git check-ignore .dev/tasks/to-do/x.md` fails; writing a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged (FR-025).
- A non-default `--output` below `.dev/sweeps/` (for example `.dev/sweeps/archive/`) is covered by the same pattern; FR-004 rejects any output outside it.
- On rollback the line stays until existing reports are dealt with (section 16).

## 11. Test plan mapped to files

Seven new files under `tests/sweep/` (the REPORT names, steps 1.8 to 1.13), one new command test, and edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged). Every test runs with the seams patched; none starts Orca, ccsession or Claude (NFR-013).

Shared setup in `tests/sweep/conftest.py` (step 1.8):

- `patch_orca` and `patch_git` replace `probes._orca` and `probes._git` with fakes that record every argv and return fixture data, as `tests/cli/reflect/conftest.py` does for its seams.
- An autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`. It steps aside only for a test carrying the existing `integration` marker, which is used by exactly one test, the real-git test below. `pyproject.toml` runs pytest with `--strict-markers`, and `integration` is already registered there, so no new marker and no `pyproject.toml` edit is needed.
- A fixed `now` and a `tmp_path` layout with `HOME` and `XDG_STATE_HOME` moved inside it, holding packages, contracts, transcripts and a ccsession `orca-tabs/` folder.
- Fixtures copied from captured Orca output keep their source name; hand-made ones carry `synthetic` in the file name until step 1.0a replaces them.

| File | Covers | Main cases |
|---|---|---|
| `tests/sweep/test_readonly.py` (created at step 1.4a, extended at 1.11) | NFR-002, FR-025, GQ-103(1), GQ-110, NFR-001, NFR-013 | Step 1.4a part: every recorded `_git` argv has `--no-optional-locks` at index 1 and `-C <path>` after it, then `-c core.fsmonitor=false`; the child env holds `GIT_OPTIONAL_LOCKS=0`; one git status argv per discovered worktree, each preceded by its read-only config inspection call; the one `integration`-marked real-git test in a `tmp_path` repository with the four SPEC assertions (control, `check-ignore` of `.dev/sweeps/x.md` succeeds, of `.dev/tasks/to-do/x.md` fails, a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged). Step 1.11 part: the snapshot diff (path, size, `st_mtime_ns`, SHA-256) over the root, `HOME` and the XDG dirs: exactly one added report file plus the output directory when new; no temp file and no second name for the report remain after exit 0 |
| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, SPEC section 11 failure modes, FR-010 | Full-sweep recording: each argv equals one template token for token, argv[0] is `$ORCA_CLI_COMMAND` when set, else `orca-ide`; zero argv for all four templates marked "not called in Phase 1" (`worktree list`, `worktree current` and both `worktree ps --agent-wait` forms, with and without `--json`); exact-set pin of the ten templates; negatives that raise `ValueError` before a subprocess (`check`, `inbox`, `worker-read`, `gate-list`, an extra flag, `--include-remote`, `run-list`); a positive case that both `worktree ps --agent-wait` templates (with and without `--json`) are accepted; the FR-021 forbidden list held in the test; git negatives (`rev-parse`, `log`, `branch`, `--version`, any `stash` form). Result classes: each unavailable cause on call one, the quoted-marker negative fixture, a middle `worker-show` exit 1, a malformed zero-exit body, the empty `run-current` body, and the captured no-binding fixture (gated on 1.0a). The `collect` source rows and `truncated` that the FR-010 list-incomplete rule reads (`test_collect_worker_list_source_rows_and_truncated`, over a fake `_orca`): R1 `worker-list` ok and R2 `worker-list` `call_failed` (not call one) give the `sources` rows whose name starts with `orca worker-list` exactly `orca worker-list R1` and `orca worker-list R2` (the prefix is the literal word `orca`, not `$ORCA_CLI_COMMAND`), R2 `unscanned` non-null and R1 `unscanned` None; a failed `task-list --run R2` sets `unscanned` on `orca task-list R2` and not on `orca worker-list R2`; with the budget spent before R2's `worker-list`, no argv is recorded for it and the row `orca worker-list R2` has `unscanned: time budget reached (90 s)`; an `orca-tabs/` folder that cannot be read sets `unscanned` on the row `ccsession orca-tabs`, while a missing folder and an empty readable one do not; a `worker-list` body of 100 rows sets `truncated` True and a body of 99 rows leaves it False. Budget: 60 rows give 50 `worker-show` and `bound_reached == 10`; 50 rows give 50 and 0; 2 Runs of 40 get 25 each; with 20 s left the per-call timeout is at most 20 s; full-timeout fakes finish under 120 s and still render the report (publication itself is exercised by `test_cli_contract.py`, not under the full-timeout fakes). Byte limits: a contract over 1 MiB is unscanned with a reason; a ledger over 1 MiB is read as head and tail (GQ-105); nine boundary fixtures at limit minus 1, at the limit and at limit plus 1 for each of the 1 MiB contract and ledger limit, the 256 KiB transcript tail and the 8 MiB subprocess output (SPEC line 297; the limit is hit only when size is over it, section 7.3). Failure modes (section 7.2 observation rules): the worktree directory deleted between the two seams gives that worktree `unscanned: worktree not readable` while the others continue (SPEC line 440); list and show disagree and the `worker-show` value is used (443); one missing and one extra `worker-show` key leave the field None and raise nothing (446); a symlink-out fixture is rejected with `unscanned: outside root` (450); a contract changed between two reads gets one re-read, and a contract that changes on every read gets `conflict: inconsistent observation` (451); a duplicate Dispatch fixture with two states gives one `orca:<dispatch>` row with `conflict: duplicate Dispatch rows disagree` (452). `parse_status` cases for M7: `ahead 3`, upstream with no ahead, no upstream, `[gone]`, detached HEAD, `No commits yet`, a rename pair in `-z` form, a `??` path under `.dev/tasks/`. Path-B time fields (R3-B1, FR-010; the first three call `probes.read_transcript_tail` and the last three call `probes.parse_worker_show`, both through `probes.parse_time`, section 7.1): `test_read_transcript_tail_sets_first_and_last_record_ts` (a JSONL file of 3 complete records at 07:00:01Z, 07:00:05Z and 07:00:09Z with one `sessionId` gives `first_record_ts` 07:00:01 UTC and `last_record_ts` 07:00:09 UTC, both aware, and `tail_complete` True); `test_read_transcript_tail_first_record_ts_is_minimum` (records out of file order, 07:00:05Z, 07:00:01Z, 07:00:09Z, give `first_record_ts` 07:00:01, the earliest value and not the first line); `test_read_transcript_tail_first_record_ts_over_256k` (a file over 256 KiB whose first record, 07:00:00Z, lies before the tail and whose first complete tail record is 08:00:00Z gives `first_record_ts` 08:00:00, not 07:00:00, because only the tail is read, and `tail_complete` False); `test_worker_show_dispatch_times_sqlite_form` (a synthetic `worker-show` JSON with `dispatch.dispatchedAt: "2026-11-08 07:00:00"`, `completedAt: null` and `status: "dispatched"` gives `dispatch_started` 2026-11-08 07:00:00 UTC, aware, `dispatch_ended` None and `dispatch_status` `"dispatched"`); `test_worker_show_dispatch_times_iso_z_form` (`dispatchedAt: "2026-11-08T07:00:00.123Z"` and `completedAt: "2026-11-08T08:00:00Z"` both parse as aware UTC); `test_worker_show_dispatch_times_missing_or_bad` (one fixture with no `dispatch` times and one with `dispatchedAt: "yesterday"` leave the field None and raise nothing, per the unknown row schema rule) |
| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-015, NFR-010, NFR-004, GQ-101, GQ-102, GQ-105, GQ-108, SP-07, SP-16, SP-24, SP-26, SP-29, D9, WC-13, M6, M9, SPEC section 11 unreadable inputs | One parametrized case per rule 1 to 9 (the `working` case expects rule `fallback` while Rule 5 is inert, open item 6), reaching every name in `CLASSES` except `working` until Rule 5 is restored; rule-name order pin `[r.name for r in RULES]`; window cases (5 h old row, windows under and at 6 h; record timestamp older than mtime); the four FR-008 inputs; a late-heartbeat live row is never `stalled (proved)` (SPEC line 444); the two FR-009 cases with the exact note; rule 1 decline notes (M6); the rule 5 case (it never matches while the names are uncaptured; the four-condition case returns when Rule 5 is restored); a future timestamp gives unknown age and never idle; FR-010 complete-negative join, the control (an 8 h old unmapped transcript T goes to Historical when the list is complete; its Given is the shared Given below), the three SPEC incomplete cases (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`; each stays visible with `person_started` None and its `origin unknown:` note, never idle or Historical), and three more fixtures that are not SPEC fixtures (a Run that is not confirmed; a Run never reached because of the budget, which counts as `call_failed`; and the SPEC's tab-map reason, which the SPEC names but gives no fixture), pinned by seven `test_fr010_*` fixtures plus the control: the three SPEC fixtures, `test_fr010_unknown_run_empty_list_unknown`, `test_fr010_run_not_reached_budget_unknown` and `test_fr010_tab_map_unreadable_older_transcript_unknown` (these three are not SPEC fixtures), and `test_fr010_incomplete_notes_order`. Shared Given of the control and the first six fixtures (path A; each fixture changes only the list-completeness inputs it names): `now` fixed, window 6 h; `--run R1` unless a fixture names more Runs; R1 `worker-list` ok with one row D1; transcript T readable, `last_activity` 8 h before `now`, no tab-map entry, joined to no Orca row; transcript U readable, active inside the window, whose `sessionId` equals D1's `session_join` (so U is joined and guard case 2 does not hold); `session_join` present on every scoped row; `orca_available` True, `truncated` False, no `unscanned` source row, and a readable empty tab-map folder. In the control T is True with the `origin not proved` note and is Historical. In each of the first six fixtures below T is None, could not determine, visible and not Historical (`summary.historical` is 0), and its notes are exactly the one `origin unknown:` note the fixture names, with no SP-16 literal and no `tab map join not observable`: `test_fr010_outage_older_transcript_unknown_not_historical` (`--run R1`; `orca_available` False and `orca_rows` empty, so D1 and the join of U are absent and guard case 2 does not hold; `sources` holds `orca worker-list R1` with `unscanned` `orca unavailable`, which does not also count as `call_failed`; the run continues on disk sources: T has `person_started` None, class could not determine and the one note `origin unknown: Orca unavailable`; T is in the visible rows, not Historical; `summary.historical` is 0); `test_fr010_full_page_uncaptured_continuation` (a hand-built `SweepInput`, not a page: scoped R1 with exactly `WORKER_LIST_PAGE` (100) `OrcaObservation` rows with distinct Dispatch ids and `session_join` values that differ from T's, one of them D1 matching U, and `truncated` True; the rule that a 100-row page sets `truncated` is tested in `collect` (`test_probes_allowlist.py`), and the continuation field of the live read, `page.nextCursor`, is UNVERIFIED until step 1.0a item 3 (open item 5) and is not an input here: T is None, could not determine, with the one note `origin unknown: worker list truncated`; not Historical; `summary.total_is_lower_bound` True); `test_fr010_call_failed_incomplete_list` (scoped Runs R1 and R2; R1 `worker-list` ok; R2 `worker-list` is `call_failed`, not call one, because a nonzero exit on call one is `unavailable` (open item 4), so `sources` holds `orca worker-list R1` without `unscanned` and `orca worker-list R2` with `unscanned` `orca call failed (exit 1)`; `orca_available` True, which the trigger needs: T is None, could not determine, with the one note `origin unknown: worker list call failed`; not Historical); `test_fr010_unknown_run_empty_list_unknown` (not a SPEC fixture; scoped Runs R1 and BAD; `worker-list` for BAD is ok with zero rows, so `orca worker-list BAD` has no `unscanned` and no row has Run BAD, and `orca task-list BAD` has `unscanned` `orca call failed (exit 1)`; `orca_available` True: T is None, could not determine, with the one note `origin unknown: Run not confirmed`; not Historical; the same input with `orca task-list BAD` not unscanned, a real Run with no Dispatch rows, gives the control result); `test_fr010_run_not_reached_budget_unknown` (not a SPEC fixture; scoped Runs R1 and R2; the budget ran out before R2's `worker-list` started, so `sources` holds `orca worker-list R1` without `unscanned` and `orca worker-list R2` with `unscanned: time budget reached (90 s)`, and no row has Run R2; `orca_available` True: T is None, could not determine, with the one note `origin unknown: worker list call failed`; not Historical); `test_fr010_tab_map_unreadable_older_transcript_unknown` (not a SPEC fixture; `--run R1`; `tab_map` is empty and the source row `ccsession orca-tabs` has `unscanned` `tab map not readable`; `orca_available` True: T is None, could not determine, with the one note `origin unknown: tab map unreadable`; not Historical; the same input with the row not unscanned, an empty readable folder, gives the control result); `test_fr010_incomplete_notes_order` (it departs from the shared Given, and all notes that hold are attached, in the order of section 7.2. Part (a), a partial outage: R1 `worker-list` ok with one row D1 whose `session_join` is None, then `orca_available` False; no U; T unjoined with no tab-map entry. Guard cases 1 and 2 hold, so T is None, could not determine, and its notes are exactly, in this order, `origin unknown: Orca unavailable`, `could not join Orca workers to transcripts (tab map empty or stale)` and `tab map join not observable`. Part (b), several list-incomplete cases together, with the shared Given otherwise: R1 has 100 rows with `truncated` True and D1 matching U; R2 `worker-list` is `call_failed`; R3 `worker-list` is ok with zero rows and `orca task-list R3` has `unscanned`; the source row `ccsession orca-tabs` has `unscanned`; `orca_available` True. T's notes are exactly, in this order, `origin unknown: worker list truncated`, `origin unknown: worker list call failed`, `origin unknown: Run not confirmed` and `origin unknown: tab map unreadable`, and no join-guard note); the five exemptions and the SP-29 two-Run fixture (none of the R2 transcripts True or Historical); `person_started` None for every unjoined transcript while `session_join` is None; the D9 join fixtures: a transcript joined to a scoped Dispatch row through its tab-map entry (path B) is False and shown as `orca:<dispatch>`, a tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs` even when the guard holds, under path A a transcript with no tab-map entry and no join is True when the guard holds and carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope` (the declared D9 limit), and a worker of an unscoped Run with no tab-map entry, placed in the same worktree, is never True without that note; a path-B scoped row whose `session_join` matches no tab-map entry makes every unjoined transcript None with the SP-16 literal; the R2-B1 pane-reuse fixtures under path B, one each for `/clear`, a resume and a person rerunning the command in the tab: the worker's earlier transcript has no entry and is None with note `earlier pane session not joinable (tab map keeps only the latest session)`, never True or Historical; the later session, whose earliest timestamp is outside the Dispatch row's window, does not join, the row is could not determine with note `pane moved to a later session`, and that later transcript is None with the same note; a later session inside the window is False with note `joined by pane: latest session of the pane`; a row with no observable start time never joins by path B; the R3-B2 several-rows fixtures, all under path B and all with aware UTC times, on 2026-11-08, with `now` and `collected_start` 12:00, `window` 6 h, `tail_complete` True unless a fixture says otherwise, S `last_record_ts` 11:30, and every row in Run R1 (in `ctx.runs`): `test_path_b_pane_reused_joins_later_row_only` (D1 on pane P, 09:00 to 10:00, `completed`, with a settled contract that rule 6 would class `finished` if the join had succeeded; D2 on pane P, from 10:30, `dispatched`; tab-map entry P to session S; S `first_record_ts` 10:40: S joins D2 only, is False and is shown as `orca:D2` with `joined by pane: latest session of the pane`; D1 is could not determine with rule `fallback`, not `finished`, and with `pane moved to a later session`; S's notes do not contain `pane moved`); `test_path_b_two_windows_hold_session_is_conflict` (D1 on P from 09:00, `dispatched`, no end; D2 on P from 10:00, `pending`, no end; S first 10:05: no join; D1 and D2 are each could not determine with `conflict: one pane session matches several Dispatch rows`; S is None (`person_started` None) with the same note and no `orca:` row carries S; `Could not determine` does not print the SP-16 line); `test_path_b_shared_boundary_second_is_conflict` (D1 on P 09:00:00 to 10:00:00 `completed`; D2 on P from 10:00:00 `dispatched`; S first 10:00:00.400: both windows hold S, because the seconds are cut and both ends are included, so both rows get the `conflict:` note and S is None); `test_path_b_no_matching_window_holds` (D1 09:00 to 09:30 and D2 10:00 to 10:30, both `completed`, both on P; S first 11:00: both rows are could not determine with `pane moved to a later session`; S is None with `pane moved to a later session` and no SP-16 line); `test_path_b_multi_row_result_ignores_row_order` (the first two fixtures with `orca_rows` reversed: same classes, notes and `row_id` values as the forward order); `test_path_b_entry_failing_window_note_order` (a tab-map entry P to S, D1 on P ended before S's first record: S's note is `pane moved to a later session`, not `Orca pane session, not in scoped Runs`, and `Could not determine` does not print the SP-16 line); `test_path_b_rows_share_terminal_handle` (as the first fixture, but D1 and D2 match by `terminal_handle`, tab-map line 3, not file name: same result as the first fixture); `test_path_b_two_rows_incomplete_tail` (D1 on P, 09:00 to 10:00, `completed`; D2 on P from 10:30, `dispatched`; S `first_record_ts` 10:40 and `tail_complete` False, `orca_rows` in both orders: no join; D1 and D2 are each could not determine with `session start not observable: transcript tail only`; S is None with the same note, never False; no SP-16 line; with D2's `dispatch_started` None instead, D1 and S keep the tail-only note and D2 gets `Dispatch time window not observable`); `test_path_b_live_session_spans_two_dispatches` (D1 on P, 09:00 to 10:00, `completed`; D2 on P from 10:30, `dispatched`; S `first_record_ts` 09:05, complete tail, one session serving both Dispatches: S joins D1 only, is False and is shown as `orca:D1`; D2 is could not determine with `session started before this Dispatch window`, not `pane moved to a later session`; this pins the second D9 limit); `test_path_b_duplicate_dispatch_rows_count_once` (D1a `dispatched` from 09:00 and D1b `completed` 09:00 to 10:00, one Dispatch id D1, both on P; S `first_record_ts` 09:30: one `orca:D1` row, could not determine with `conflict: duplicate Dispatch rows disagree` and `Dispatch time window not observable`; no join; S is None with `Dispatch time window not observable`; neither the row nor S has the `conflict: one pane session` note; no SP-16 line); when guard cases 1 and 2 hold together, the transcript carries the SP-16 literal first, then `tab map join not observable`; the SPEC line 236 fixture (worker rows present, no transcript joined) gives the same; SP-07: a contract body whose later line quotes `guard refused:` is not finished (SPEC line 259); a `progress.md` with `FINAL:` inside other text is not `archive-blocked` (269); a truncated-JSONL transcript (last record cut mid-object, no complete record with both `timestamp` and `sessionId`) and an unreadable contract (open raises `OSError`) each give could not determine with their `unscanned:` note (442); a transcript cut only in its last line that still has an earlier complete record with both fields stays readable and is classified normally; a transcript whose open raises `OSError` gives `unscanned: transcript not readable`; an Orca row with a non-null `parent` carries `WC-13 violation, review` and keeps its class (261); FR-012 over all fixtures (`worktree` never `yes`); one FR-013 fixture per condition with the condition named; one FR-014 fixture per state including `conflict`; the FR-015 fixtures (44 committed folders in 3 worktrees give no flag, one modified folder in 3 worktrees gives one line naming all 3, one `??` path marks a package active); the FR-005 person-session fixture uses an active session (M9); AST import test that `classify.py` and `report.py` import none of `subprocess`, `click`, `os`, `shutil`. The R3-B1 path-B window fixtures (every time in them is aware UTC; `tail_complete` is True unless a fixture says otherwise): `test_path_b_window_open_row_joins` (row D1 with `session_join` pane P, `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`, a tab-map entry from P to session S, transcript S with `first_record_ts` 10:05, `collected_start` 12:00: S joins D1, `person_started` is False, S is shown as `orca:D1` with note `joined by pane: latest session of the pane`; this join is the first D9 limit, which needs the owner's sign-off at step 1.0b: S may be a person's later session in the pane, because the window has no upper bound); `test_path_b_window_inclusive_bounds` (D1 from 10:00:00 to 11:00:00, `completed`; three runs with S `first_record_ts` 10:00:00.700, 11:00:00.400 and 11:00:01.000: the first two join, because the seconds are cut and both ends are included; the third does not join, D1 is could not determine with `pane moved to a later session` and S is None); `test_path_b_terminal_row_without_end_has_no_window` (D1 started 10:00, `dispatch_ended` None, `dispatch_status` `completed`, S first record 10:30: no join, D1 is could not determine with `Dispatch time window not observable` and S is None with the same note); `test_path_b_row_without_start_has_no_window` (D1 `dispatch_started` None, for example past the 50-call show cap: no join, D1 is could not determine with `Dispatch time window not observable`, S is None, never True); `test_path_b_incomplete_tail_has_no_session_start` (D1 from 10:00:00 to 11:00:00, `completed`; S with `first_record_ts` 10:30:00 and `tail_complete` False: no join, D1 is could not determine with `session start not observable: transcript tail only` and S is None with the same note, never False or True) |
| `tests/sweep/test_report.py` | FR-011, FR-016, NFR-005, NFR-008, NFR-015, SP-23, SP-24, FR-020 header line, FR-006 (rule 6 wording), SP-16, WC-13, SPEC section 11 remote coverage | Heading order equals section 7.5; (a) sort with 3 ages plus one unknown, tie-break by ID; (b) never prints question text; injection fixture (`a\|b`, ANSI, bidi override, `<script>`, a Markdown link) keeps the column count and leaves no active tag or link; a 300-character cell prints 200 characters ending `...` while the JSON value is whole; render twice gives equal bytes and equal JSON apart from `report_path`; source-loss fixture gives could not determine with the `unscanned:` reason, never finished, failed, not frozen or a recommendation; version line for `1.4.245-aidev02.780594c521aa`, `1.4.246` and a missing file; the `bound_reached` line text; the SP-24 footnote; the empty-section string; the `next inspection` map has an entry for every rule name and no stop, retry, release, merge or removal word; rule 6 wording: a finished row's report text and JSON contain neither `admitted` nor `accepted` (SPEC line 259); the remote-coverage fixture: `## Source coverage` has the `remote hosts` row with coverage `unknown` and the Scope line carries `(lower bound: remote hosts not scanned)`, never a no-sessions line (454); the WC-13 row appears under `## Retained problems` (380); the SP-16 literal `could not join Orca workers to transcripts (tab map empty or stale)` appears under `## Could not determine` (236); a True row with the `origin not proved` note prints the note in its row and in the JSON `notes` (D9); the lower-bound line: a result with `truncated` True (the 100-row case) prints `[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]` in the header and its JSON `summary.total_is_lower_bound` is True (SPEC line 321); the last line is `Report complete` |
| `tests/sweep/test_cli_registration.py` | FR-001, NFR-006 | `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner`; importing `superclaude.cli.sweep` records no seam call and does not import `commands` until `sweep_group` is read |
| `tests/sweep/test_cli_contract.py` | FR-002, FR-003, FR-004, FR-005, FR-017, FR-018, FR-019, NFR-009, G-1 (section 3) | Run id cases (`""`, `'r;x'`, duplicate, unknown-Run then R2); the three binding tests and the fourth gated on 1.0a; disk-only continuation prints `unscanned: orca unavailable`; the FR-003 parser cases; the FR-004 output and root cases; the FR-005 fixture (4 rows, 2 worktrees, `(4/4)`) and the reconciliation equalities; golden v1 key set and types at every level; zero counts present; `waiting` lists hold ids only; two runs with one injected `now` give `stem.md` and `stem-2.md`; one test per exit code. Publication cases from section 3: a link failure, a full disk on write, `stem.md` to `stem-99.md` all taken, an existing temp name, and an output path that escapes after `makedirs` each exit 1 with no file at a report name and no success JSON; a print failure after the commit point exits 1 and leaves one complete report; `os.unlink` patched to raise after a successful `os.link` gives exit 1, no success JSON, exactly one complete report ending in `Report complete`, and a stderr line `[sweep publish] could not remove temp file <path>` naming the temp path; an existing earlier report is byte-identical afterwards |
| `tests/commands/test_sweep_command.py` (new, step 1.16) | FR-022, NFR-011, NFR-007 (static half) | The section 7.6 assertions |
| `tests/skills/test_worker_contract.py` (edit, step 1.19, same commit as step 1.18) | FR-023 | The section 8 pins |
| `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py` (edits); `tests/commands/test_routing_plugin_parity.py` (unchanged, must pass) | FR-024 | R1 to R5 of section 9 |

NFR-012 is checked by the gates of steps 1.25 to 1.27, not by a test file. Run line for the sweep tests: `uv run pytest tests/sweep -v`.

## 12. Traceability

Every SPEC requirement (SPEC lines 95 to 120 and 130 to 144) maps to the design element that meets it and the test file that checks it. Test file names are those of section 11; `tests/sweep/` is shortened to `sweep/`.

| ID | Design element (section) | Test file |
|---|---|---|
| FR-001 | `sweep_group`, `commands.run`; `main.py` registration (7.1, 7.6, step 1.7) | `sweep/test_cli_registration.py` |
| FR-002 | `_check_run_ids`, `bind_run`, `BindingError`; first call per Run is `worker-list` (5, 7.1) | `sweep/test_cli_contract.py` |
| FR-003 | `_parse_window` (7.1) | `sweep/test_cli_contract.py` |
| FR-004 | `_find_root`, `_check_output`, re-check in `_publish` (3.2, 7.1) | `sweep/test_cli_contract.py` |
| FR-005 | `SweepResult` rows and worktrees; `summary` reconciliation (6, 7.2, 7.4) | `sweep/test_cli_contract.py` |
| FR-006 | `classify.RULES`, `CLASSES`; rule 6 wording and SP-07 (7.1, 7.2) | `sweep/test_classify.py` (SP-07 `guard refused:` case), `sweep/test_report.py` (no `admitted` or `accepted`) |
| FR-007 | `SweepContext`; `last_activity` source rule (7.2) | `sweep/test_classify.py` |
| FR-008 | Rule 9 `fallback`; could not determine as its own class (7.2) | `sweep/test_classify.py` |
| FR-009 | Rule 2 `orca_exit_proof` decline and note (7.2) | `sweep/test_classify.py` |
| FR-010 | `person_started` tri-state, completeness guard with its five list-incomplete cases (the three SPEC cases: outage, full page, `call_failed`, where a Run the budget never reached counts as `call_failed`; the SPEC's `tab map unreadable`; and the design's Run not confirmed, an empty `worker-list` with a failed `task-list --run`), with the notes attached in one order, and with its four join-incomplete cases (the fourth is the path-B earlier pane session), worker defined by a join to a scoped Dispatch row, with a path-B join also needing the Dispatch row's time window and a transcript whose tail is complete, and one rule for several rows matching one pane session (join only the one row whose window holds it; `conflict:` when two or more do; duplicate Dispatch rows are merged first and an incomplete tail is handled before the count), SP-29 other-Run rule as narrowed by D9 with the `origin not proved` note on every no-entry True, `read_tab_map` (2.2 GQ-108, 7.1, 7.2, 13) | `sweep/test_classify.py` (the D9 join fixtures, the three SPEC incomplete-case fixtures, the three non-SPEC list-incomplete fixtures with the note-order fixture, seven `test_fr010_*` in all, and the SPEC line 236 fixture), `sweep/test_probes_allowlist.py` (the six reader and parser fixtures of the path-B time fields and the `collect` source-row and `truncated` test), `sweep/test_report.py` (SP-16 literal and the lower-bound line) |
| FR-011 | `SECTIONS` order and the (a) sort (7.5) | `sweep/test_report.py` |
| FR-012 | `safe_to_close`; `worktree` never `yes` (7.1, 7.2) | `sweep/test_classify.py` |
| FR-013 | `removable` with the named condition; M7 `unpushed`; a worktree removed mid-sweep is unscanned (7.1, 7.2) | `sweep/test_classify.py`, `sweep/test_probes_allowlist.py` (`parse_status`, worktree-removed fixture) |
| FR-014 | `package_state`, `PACKAGE_STATES`; `FINAL:` only at line start (2.2 GQ-102, GQ-105; 7.1, 7.2) | `sweep/test_classify.py` (one fixture per state, the `FINAL:` inside-text negative) |
| FR-015 | `mark_shared_packages`; `--untracked-files=all` in `ALLOWED_GIT` (2.2 GQ-101, 7.3) | `sweep/test_classify.py` |
| FR-016 | `sanitize`, `cell` (7.1, 2.2 GQ-107) | `sweep/test_report.py` |
| FR-017 | `_publish` naming and suffixes; `to_json` printed after the commit point (3, 7.4) | `sweep/test_cli_contract.py` |
| FR-018 | Exit mapping in `commands.run` (3.4, 7.1) | `sweep/test_cli_contract.py` |
| FR-019 | `OrcaResult` `unavailable`; disk-only continuation; banner (5, 7.1) | `sweep/test_cli_contract.py` |
| FR-020 | `Budget` (7.1); byte limits in the readers (7.1, 7.3); WC-13 rows under Retained problems (7.2) | `sweep/test_probes_allowlist.py` (budget cases, the nine byte-limit boundary fixtures), `sweep/test_report.py` (header line, WC-13 Retained problems line) |
| FR-021 | Read-only package; `FORBIDDEN` list held in the test only (7.3) | `sweep/test_probes_allowlist.py` |
| FR-022 | `/sc:sweep` command and `sc-sweep-protocol` skill (7.6) | `tests/commands/test_sweep_command.py` |
| FR-023 | WC-16 and the never-as-worker addition (8) | `tests/skills/test_worker_contract.py` |
| FR-024 | R1 to R8 (9) | `tests/recommend/`, `tests/core/`, `tests/commands/test_routing_plugin_parity.py` |
| FR-025 | `.gitignore` line (10) | `sweep/test_readonly.py` (real-git test) |
| FR-026 | `OrcaResult` kinds and the result parser in `_orca` (7.1) | `sweep/test_probes_allowlist.py` |
| NFR-001 | One write in `_publish`; exit 0 only after the temp file is removed (3.2, 3.4) | `sweep/test_readonly.py` (snapshot diff), `sweep/test_cli_contract.py` (unlink-failure case exits 1) |
| NFR-002 | `_git` argv and env (2.1, 7.1, 7.3) | `sweep/test_readonly.py` |
| NFR-003 | `check_orca_argv`, `check_git_args`, `orca_binary` (7.1, 7.3) | `sweep/test_probes_allowlist.py` |
| NFR-004 | Pure `classify.py` and `report.py` (4, 7.1) | `sweep/test_classify.py` (AST test) |
| NFR-005 | `render` and `to_json` read no clock; `collected` interval in `SweepInput` (7.1, 7.4) | `sweep/test_report.py` |
| NFR-006 | Lazy `__getattr__` in `__init__.py` (7.1) | `sweep/test_cli_registration.py` |
| NFR-007 | `Budget` 90 s; skill timeout 120000 ms; one re-read of a changed input only while the budget allows (7.1, 7.2, 7.6) | `sweep/test_probes_allowlist.py` (budget cases, changed-contract fixture), `tests/commands/test_sweep_command.py` |
| NFR-008 | `unscanned:` reasons flow to could not determine (6, 7.2) | `sweep/test_report.py` |
| NFR-009 | JSON v1 key set (7.4) | `sweep/test_cli_contract.py` |
| NFR-010 | `RULES` order pinned by name (7.2) | `sweep/test_classify.py` |
| NFR-011 | `~/.claude/...` paths in the command and skill (7.6) | `tests/commands/test_sweep_command.py`; step 1.28 grep |
| NFR-012 | Repo gates (15.2, steps 1.25 to 1.27) | none (gate commands) |
| NFR-013 | Patched seams and the autouse subprocess guard (11) | every `sweep/` file through `conftest.py` |
| NFR-014 | `ALLOWED_ORCA` ten templates (7.3) | `sweep/test_probes_allowlist.py` |
| NFR-015 | `CHECKED_ORCA_VERSION`, `read_orca_version` (7.1) | `sweep/test_report.py` |
| G-1 | `_publish` and the exit-1 rule, including exit 1 when the temp unlink fails after the commit point (3) | `sweep/test_cli_contract.py` (publication cases, unlink-failure case), `sweep/test_readonly.py` |
| GQ-101 to GQ-110 | Section 2.2 | as the FR rows above name them |
| SPEC section 11 failure modes (lines 440-454) | Observation rules (7.2): worktree removed, unreadable transcript or contract, list and show disagree, unknown schema field, path escapes its source, input changed, duplicate Dispatch, remote hosts. The other rows map to the FR, NFR and D rows above: 438 and 439 to FR-019 and FR-026, 441 to NFR-002 and NFR-015, 444 to FR-008, 445 to FR-020, 447 to NFR-003, 448 to FR-017, 449 to FR-016, 453 to D2 | `sweep/test_probes_allowlist.py` (440, 443, 446, 450, 451, 452), `sweep/test_classify.py` (442), `sweep/test_report.py` (454) |
| SPEC section 7 cross-cutting notes (lines 236, 259, 261, 269) | SP-16 literal, rule 6 wording and SP-07, WC-13 note, `FINAL:` reading (7.2) | `sweep/test_classify.py`, `sweep/test_report.py` |

## 13. Deviations from SPEC

A deviation is a place where this design states something the SPEC text does not say, or says differently. Each one comes from the PANEL, FIXREVIEW or the design review (`docs/designs/orchestrator-mode-review-1.md`) and is applied in the section named. D-numbers here are this design's own; they are not the owner decision D3 that `WORKER-CONTRACT.md` line 23 mentions (quoted in section 8).

| ID | SPEC text | Design | Source | Section |
|---|---|---|---|---|
| D1 | Module table line 199: `report.py` holds `write_report(text, output_dir, now) -> Path`, the package's only write; line 200: `commands.py` calls `write_report`; section 11 line 448 names `OSError` in `write_report` | No `write_report`. The one write is `commands._publish`; `os` joins the `commands.py` may-import list; `report.py` is pure as a whole | SP-20 | 3.1, 4 |
| D2 | Section 11 line 453: a killed process may leave a report file without the `Report complete` footer; G-1 (lines 637-645) leaves the exit-1 disk state open | Temp file, `fsync`, then `os.link` as the commit point; no report name ever holds partial bytes; the exit-1 rule of section 3.4 is added to SPEC section 5.3 | G-1, PANEL lines 289-296 | 3.2 to 3.4 |
| D3 | FR-002 and FR-019 message `Orca unavailable; no Run binding could be established: pass --run <id>` | `Orca unavailable (<reason>); no Run binding could be established: pass --run <id>`, with the `OrcaResult.reason` in the parentheses | SP-21 | 5 |
| D4 | No cell length limit | `report.cell` cuts a Markdown table cell at 200 characters ending `...`; JSON values are never cut | SP-23 | 7.1, 7.5 |
| D5 | Age has no rule for a timestamp after `now` | A future timestamp is unknown age, adds note `timestamp in the future`, and never satisfies rule 7 (idle) | SP-26 | 7.2 |
| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-16, with master's cadence "at most once every 5 minutes" (contract line 110) in place of "It sweeps on every wake"; `/sc:sweep` stated as an added read beside the unchanged line 110 sweep (not a replacement, not a second pass, no heartbeat update, no `--agent-wait` listing), with a sentence that its own reads are not L1 probes and do not count against the L1 cap; and one sentence appended: the coordinator records each admission or rejection in its run notes; `/sc:sweep` does not observe them. No new pin | SP-27 | 8 |
| D7 | Rule 5 at line 253 reads only "`live`, `in_progress`, `agent_wait_present` and null"; the report says nothing about classes Phase 1 cannot observe | Rule 5 restated as four conditions, one per line, with each field source; the report adds the footnote that stalled and fenced are not observed in Phase 1 and a zero count does not mean none occurred | SP-24 | 7.2, 7.5 |
| D8 | Branch header case at line 335: `ahead N` gives `unpushed N` (a count) | `unpushed` is `bool \| None` as SPEC line 240 types it, with `upstream_note` carrying `ahead N` and the other notes; JSON `unpushed` is never a count | M7 | 2.2, 7.2, 7.4 |
| D9 | FR-010 and SP-29 (line 104): a transcript that the tab map marks as an Orca worker session (any Run), or whose session id appears in any Orca row of any Run, is never True | A worker is a transcript joined to a Dispatch row of a scoped Run (path A or B). A tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs`, so person sessions started through `ccsession` in Orca panes are never idle or Historical in Phase 1. Under path A only, a transcript with no tab-map entry and no scoped join may be True when the guard holds, so a worker of an unscoped Run that has no entry can be True. Every True reached this way carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and in the JSON `notes`, so such a session is never shown as person-started without a note. Under path B the guard has four join-incomplete cases; the fourth (an earlier session of a reused pane has no entry) makes every unjoined no-entry transcript None, and a path-B join also needs the Dispatch row's time window, a transcript whose tail is complete and, when several rows match one pane session, exactly one window holding it. D9 as first written covers only True becoming None. Two residual path-B cases are new and need the same owner sign-off, which is still pending: a window with no end (a row still `pending` or `dispatched`) has no upper bound, so a person's later session in that pane, started after the worker died, joins the row as False and is shown as `orca:<dispatch>`, not as a person session; and a live session that serves two Dispatches joins the older row only, while the newer row is could not determine. Reason: the ccsession file cannot tell a worker pane from a person pane and holds no Run id, it has no entry for plain `claude` launches or earlier sessions of a reused pane (section 1), and no allowlisted verb lists the rows of Runs outside the scope (section 7.3). Needs the owner's sign-off at step 1.0b. Pinned by the D9 join fixtures in `sweep/test_classify.py` | Review 1 B2; review 2 R2-B1 and R2-B2 | 1, 7.2, 11 |
| D10 | NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619: `worktree ps` never carries `--agent-wait` | `worktree ps --agent-wait` (with and without `--json`) is allowed; `FORBIDDEN_TOKENS` holds only `--include-remote`; the NFR-014 exact-set pin covers ten templates, not eight | Owner decision R5, 2026-11-08: "Allow it, no conditions needed." | 2.2, 4, 7.3, 11, 12, 15.1 |

Total: 10 deviations.

Not counted as deviations:

- The JSON keys `collected`, `waiting_kind`, `policy`, `person_started` and `summary.counts` are additions that the SPEC's additive-only rule (NFR-009) allows; they are in the pinned v1 set from the first release (section 7.4).
- The SP-29 False path (`worker of Run <id>, outside scope`) is kept as SPEC text but does not occur in Phase 1, because the ccsession tab map holds no Run id (section 7.2). The SPEC states it conditionally, so this is a finding, not a change.
- Exit 1 when the temp file cannot be removed after the commit point (section 3.2). FR-017 says failed publication exits 1 without success JSON; this design counts publication as finished only when the temp file is gone, because otherwise a run would exit 0 with two names on disk, against NFR-001. This reads FR-017 and NFR-001 together; it adds no rule the SPEC lacks.

REPORT differences. These are places where the design follows the SPEC over the REPORT's step text; they are listed so `/task-builder` does not copy the REPORT version:

| REPORT step | REPORT text | Design (following the SPEC) |
|---|---|---|
| 1.0a | Probe with `worker-read` and a throwaway Run | Only templates 1 to 8 of the ten allowlisted templates, against an existing Run the person names; no `worker-read` (section 15.1) |
| 1.4 | Timing of `worker-list --include-remote` | Dropped; `--include-remote` is a forbidden token (section 7.3) |
| 1.5 | `write_report` in `report.py` | `commands._publish` (D1) |
| 1.6 | A `run-list` fallback; an `--output` default outside `.dev/sweeps/` | No fallback (GQ-104); `--output` defaults to `<root>/.dev/sweeps/` (FR-004) |
| 1.14 | `allowed-tools` form of the REPORT draft | The two exact literals of FR-022 (section 7.6) |
| 1.15 | The skill recommends next actions | The skill recommends nothing (section 7.6) |
| 1.17 | The REPORT's WC-14 (WC-16 in this design) draft | The SPEC section 10 text plus D6 (section 8) |

## 14. Panel notes carried into the design

How each PANEL item (SP-19 to SP-27), the two SPEC items this design acts on (SP-28, SP-29), and each FIXREVIEW minor note (M1 to M10, FIXREVIEW lines 103-112) is handled. "Applied" means the design text already carries it; the section is named.

| Note | Handling | Where |
|---|---|---|
| SP-19, M5 | FR-019 repeats the pre-fix FR-002 paragraph without the SP-09 `--run` check. The design treats FR-002 plus SPEC section 5.1 as the single source; FR-019 adds only the disk-only continuation and the `unscanned: orca unavailable` text. Tests cite FR-002 for the run-id cases | 5, 11 |
| SP-20 | Applied as D1 | 3.1 |
| SP-21 | Applied as D3 | 5 |
| SP-22 | Report retention stays out of scope; the person deletes old reports and leftover temp files by hand | 1, 3.3 |
| SP-23 | Applied as D4 | 7.1, 7.5 |
| SP-24 | Applied as D7 | 7.2, 7.5 |
| SP-25 | Already applied in the SPEC (FR-022 names both `allowed-tools` literals); the command test asserts them | 7.6 |
| SP-26 | Applied as D5 | 7.2 |
| SP-27 | Applied as D6 | 8 |
| SP-28 | The byte limits stay "proposed"; the rationale required before release is an open item | 7.3, 17 |
| SP-29 | Applied with the D9 narrowing: a worker is a transcript joined to a scoped Dispatch row; a tab-map entry that joins no scoped row gets `person_started` None; under path A only, a transcript with no entry and no scoped join may be True, and always with the `origin not proved` note; under path B the four join-incomplete cases apply, the fourth being an earlier session of a reused pane, and a path-B join needs the Dispatch row's time window, a transcript whose tail is complete and, when several rows match one pane session, exactly one window holding it; D9 as first written covers only True becoming None, and the two residual path-B cases of D9 (a window with no end can join a person's later session as False; a live session serving two Dispatches joins the older row only) need the same owner sign-off, which is still pending; the False path cannot occur in Phase 1 | 7.2, 13 |
| M1 | `--include-remote` is forbidden in Phase 1, not deferred: it is in `FORBIDDEN_TOKENS` and has a negative test. GQ-22 is for a later phase only | 7.3 |
| M2 | `run-current` keeps no `--json` until the step 1.0a capture decides; adding it is an allowlist change with an owner note | 7.3, 15.1, 17 |
| M3 | Decided: `worktree list` and `worktree current` stay pinned and are not called | 7.3 |
| M4 | The Orca read-verb lock claim for `worker-show` rests on the static read only; the report's lock line is version-scoped (NFR-015) and the design claims nothing further. Step 1.0a records `worker-show` before and after the other reads as its only live check | 15.1 |
| M6 | Applied: the rule 1 decline notes are named | 7.2 |
| M7 | Applied as D8 | 2.2, 7.2 |
| M8 | Accepted as a proposed split (head 512 KiB, tail 512 KiB) | 2.2, 7.3 |
| M9 | Applied: the FR-005 fixture's person session is active (rule 8), so it is counted in Sessions, not Historical | 11 |
| M10 | Rule numbers in this design are the SPEC's 1 to 9 (section 7 of the SPEC) | 7.2 |

## 15. REPORT step mapping for `/task-builder`

### 15.1 What step 1.0a captures

Step 1.0a replaces the REPORT version (REPORT steps list, lines 1237 to 1300). It is a manual, pre-implementation capture run by the person or the coordinator, never by a test, and it writes only its own notes file.

Rules for the capture:

- It runs against an existing Run that the person names. It creates no Run, Task or Dispatch; the REPORT's throwaway Run is dropped.
- The `ALLOWED_ORCA` allowlist of section 7.3 has ten templates; step 1.0a issues only templates 1 to 8 of it, with the binary `orca-ide` or `$ORCA_CLI_COMMAND`. `worktree ps --agent-wait` is allowed by R5 but is not run in step 1.0a. No `worker-read` (with or without `--source transcript`), no `gate-list`, no `check`, no `inbox`, no `--include-remote`, and no `git stash` in any form.
- `--json` is tried only where a template already has it. Whether `run-current` needs `--json` is answered by reading its plain output and, only if that is not parseable, by recording the fact for an owner note (M2); the capture does not run `run-current --json`.
- `worker-show` and `task-list` are each run once before and once after all other reads. The two outputs must be identical apart from timestamps; that is the only live check that these reads change nothing (M4). A difference stops the build and goes to the owner.
- Output goes to `.dev/tasks/<pkg>/artifacts/readonly-probe.md` in the task package (always staged, CLAUDE.md rule). Sanitized samples that become test fixtures are copied under `tests/sweep/fixtures/` with their source named.

What it records:

| # | Item | Feeds |
|---|---|---|
| 1 | `run-current` output when a Run is bound, and when none is bound (the no-binding shape) | `bind_run`, FR-002 fourth test, FR-026 case 4 |
| 2 | Whether `run-current` output is parseable without `--json` | M2, section 7.3 |
| 3 | `worker-list --run <run> --json` schema, page size and the cursor or continuation field, if any | `WORKER_LIST_PAGE`, the cursor template (section 7.3) |
| 4 | `worker-show --dispatch <dispatch> --json` field names: the field that can carry `session_join` (a Claude session id, pane key or terminal handle), `agentWait` presence and value, `liveness.verdict`, `status`, and whether `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` are present and in what shape (the static bundle read gives the SQLite form `YYYY-MM-DD HH:MM:SS` UTC for `dispatchedAt` only; the form of `completedAt` is UNVERIFIED and either that form or ISO 8601 is possible, which 7.2 accepts; `status` is one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`); also record, for one worker, whether `dispatchedAt` is earlier than the first transcript record of its session, and whether `completedAt` is set for `failed` and `circuit_broken` rows | Rule 5, the join paths of section 7.2, the path-B time window, GQ-108, open item 23 |
| 5 | `task-list --ready --run <run> --json` and `task-list --run <run> --json` shapes, and whether a creator field exists | Rule 4 (b), Waiting (b) sub-heading |
| 6 | `worktree ps --json`: the worktree path field | Worktree discovery, M3 |
| 7 | `worktree list --json` and `worktree current --json` shapes (recorded only; Phase 1 does not call them) | M3 |
| 8 | What `worker-list --run <unknown id>` returns (a read-only live read on 2026-11-08 gave exit 0 and an empty list, not an error; record the body) and the error shape of `task-list --run <unknown id>` (stderr and exit code; `run_not_found` was seen) | FR-002 unknown-Run case, the Run-not-confirmed rule (7.2) |
| 9 | The `runtime_unavailable` shape, only if Orca is already unavailable during the capture; it is never induced | FR-026 case 1 marker |
| 10 | Run id and Dispatch id samples, from which `RUN_ID_RE` and `DISPATCH_ID_RE` are written | `_check_run_ids`, template placeholders |
| 11 | Whether each template accepts its flags as written (exit 0 with parseable output) | NFR-014 pin |
| 12 | The installed Orca version string from `/opt/Orca/resources/app.asar.unpacked/out/package.json` | NFR-015 |
| 13 | For each worker of the named Run: whether `orca-tabs/` holds an entry for its pane (read the files only), and whether the item 4 field equals that entry's file name or terminal handle. Also whether workers are launched through `ccsession`, which decides whether they get an entry at all (section 1) | Join path B, the D9 fixtures, open item 22 |

If an item cannot be captured, it stays UNVERIFIED in section 17 and the code path it feeds keeps its could-not-determine behaviour (for example, no `session_join` means `person_started` None for every unmatched transcript).

Pre-implementation steps: 1.0a (this capture), 1.0b (owner decisions) and 1.16a (the record-only PR #422 check) run before any code for the steps they gate. Step 1.29 is a manual check after the build.

### 15.2 Step table

REPORT step numbers are kept so the task file can cite the REPORT; one step is new (1.4a). "Pre" marks a pre-implementation step. Where the REPORT text and this design differ, this design wins (section 13, REPORT differences).

| Step | Pre | Work | Design section | Gate before the step |
|---|---|---|---|---|
| 1.0a | Pre | Read-only capture of section 15.1 | 15.1 | An existing Run named by the person |
| 1.0b | Pre | Owner decisions GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, and sign-off on the D9 narrowing of SP-29 (section 13); read `.dev/orca-command-refactor/decisions/APPROVED.md`; record in `.dev/tasks/<pkg>/artifacts/owner-decisions.md` | 8 | none |
| 1.1 | | `src/superclaude/cli/sweep/__init__.py` with lazy `__getattr__` | 7.1 | none |
| 1.2 | | `models.py` | 7.2 | none |
| 1.3 | | `classify.py`, the 9 rules | 7.1, 7.2 | 1.2 |
| 1.4a | | `probes._git`, `ALLOWED_GIT`, `check_git_args`, and `tests/sweep/test_readonly.py` with the NFR-002 recorded-argv, env and real-git tests, plus the `.gitignore` lines. The first code commit | 2.1, 7.3, 10, 11 | 1.2 |
| 1.4 | | Rest of `probes.py`: `_orca`, `ALLOWED_ORCA`, `Budget`, `OrcaResult`, `bind_run`, `collect`, readers. Live check saved to `.dev/tasks/<pkg>/artifacts/sweep-live-check-1.4.json`; no `--include-remote` timing | 7.1, 7.3 | 1.0a (parsers, regexes), 1.4a |
| 1.5 | | `report.py`: `sanitize`, `cell`, `render`, `to_json`, `SECTIONS`; no `write_report` | 7.1, 7.4, 7.5, D1 | 1.3 |
| 1.6 | | `commands.py`: `run`, `_parse_window`, `_find_root`, `_check_output`, `_check_run_ids`, `_publish`; no `run-list` fallback; `--output` default `<root>/.dev/sweeps/` | 3, 5, 7.1 | 1.4, 1.5 |
| 1.7 | | Register `sweep_group` in `src/superclaude/cli/main.py` with the deferred-import pattern (after line 565) | 7.1 | 1.6 |
| 1.8 | | `tests/sweep/conftest.py` and fixtures | 11 | 1.0a for captured fixtures |
| 1.9 | | `tests/sweep/test_classify.py` | 11 | 1.3 |
| 1.10 | | `tests/sweep/test_probes_allowlist.py` | 11 | 1.4 |
| 1.11 | | Extend `tests/sweep/test_readonly.py` with the NFR-001 snapshot diff and NFR-013 | 11 | 1.6 |
| 1.12 | | `tests/sweep/test_report.py` | 11 | 1.5 |
| 1.13 | | `tests/sweep/test_cli_registration.py` and `tests/sweep/test_cli_contract.py` | 11 | 1.7 |
| 1.14 | | `src/superclaude/commands/sweep.md` | 7.6 | 1.7 |
| 1.15 | | `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, recommending nothing | 7.6 | 1.14 |
| 1.16 | | `tests/commands/test_sweep_command.py` | 7.6, 11 | 1.15 |
| 1.16a | Pre | Record-only: write `.dev/tasks/<pkg>/artifacts/pr422-409-check.md` with four points: (1) the `gh pr view 422 --repo IronbellyOrg/IronClaude` state line (MERGED, merge commit `2327fbd3`); (2) `git merge-base --is-ancestor 2327fbd3 HEAD` succeeding; (3) `git merge-base --is-ancestor 495eb96d origin/master` failing, so the `495eb96d` pin stands and no layout diff is needed; (4) a note that every `WORKER-CONTRACT.md` and `test_worker_contract.py` line cited by steps 1.17 to 1.19 is re-read at HEAD before it is edited | 8 | none; the record gates 1.17 and is satisfied as soon as it is written |
| 1.17 | | WC-16 in `src/superclaude/core/WORKER-CONTRACT.md` | 8 | 1.0b (GQ-11 answered), 1.16a |
| 1.18 | | `WORKER-CONTRACT.md` line 23, never-as-worker list; lands in one commit with 1.19, which carries the `never-as-worker` phrase edit (pin 5) | 8 | 1.17 |
| 1.19 | | Pins in `tests/skills/test_worker_contract.py` and the rename | 8 | same commit as 1.18 |
| 1.20 | | R5 | 9 | 1.14 |
| 1.21 | | R1 and R2; lands in one commit with 1.22 (R4) and 1.23 (R3) | 9 | 1.14, 1.18 |
| 1.22 | | R4 | 9 | same commit as 1.21 |
| 1.23 | | R3, in the same commit as 1.21 and 1.22 | 9 | 1.21 |
| 1.24 | | R6 | 9 | 1.14 |
| 1.24a | | R7 | 9 | 1.18 |
| 1.24b | | R8 | 9 | 1.16, 1.17 |
| 1.25 | | `make sync-dev`, then `make verify-sync`; no `.claude/` path staged | 9 | 1.24b |
| 1.26 | | `make lint`, `uv run ruff check .`, `uv run ruff format --check src/ tests/` | none | 1.25 |
| 1.27 | | `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend`, then `uv run pytest` | 11 | 1.26 |
| 1.28 | | `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`, every hit justified | 7.6 | 1.27 |
| 1.29 | Manual | `superclaude sweep --help` under a pipx install; output saved to `.dev/tasks/<pkg>/artifacts/sweep-help-pipx.txt` | 7.6 | 1.28 |

The `.gitignore` lines (section 10) have no REPORT step of their own. They go into step 1.4a because the real-git test created there copies the repository `.gitignore`, so its FR-025 check-ignore assertions fail until the line exists.

## 16. Rollback

The SPEC rollback (section 17, lines 587-607) holds unchanged: Phase 1 is additive, a successful run's only filesystem change is one report file (plus its directory when new; a dot-prefixed temp file exists only during publication, section 3), and rollback is one revert of the branch's commits as one unit, with no data migration. This design adds only the rows marked (design).

| Item | Rollback |
|---|---|
| `src/superclaude/cli/sweep/` and `tests/sweep/` (including `tests/sweep/fixtures/`) | Delete |
| `src/superclaude/cli/main.py` deferred import and `add_command` lines (after line 565) | Remove |
| `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`, `tests/commands/test_sweep_command.py` | Delete; run `make sync-dev`. Whether it removes the `.claude/` copies is UNVERIFIED (section 17); if not, delete them by hand. Never stage them |
| WC-16 with the D6 sentence, the line 23 never-as-worker entry, the `RULE_PHRASES["WC-16"]` entry, the `RULE_PHRASES["never-as-worker"]` phrase at test line 89, the `NEVER_AS_WORKER` entry, the `UNATTENDED_COMMANDS` assertion (design) and the test rename | Revert |
| R1, R2, R3, R4, R5 | Revert together, so the plugin byte copy stays equal |
| R6, R7, R8 | Revert; add a CHANGELOG revert entry |
| `.gitignore` `.dev/sweeps/` lines | Keep until existing reports are dealt with, then remove (GQ-106) |
| Reports and leftover dot-prefixed temp files under `.dev/sweeps/` (design: temp files) | Stay; they are ignored local files and the owner decides |
| Step artifacts under `.dev/tasks/<pkg>/artifacts/` (design: `readonly-probe.md`, `owner-decisions.md`, the 1.4, 1.16a and 1.29 captures) | Stay, as all of `.dev/tasks/` does |
| `.dev/tasks/` | Never removed: rollback removes no `.dev/tasks/` folder and no file in it |

Rollback check, as in the SPEC: `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_worker_contract.py tests/recommend tests/core tests/commands` pass on the reverted tree. `tests/sweep` no longer exists after the revert, so it is not in the check.

## 17. Open items

Each item is unverified or undecided today. The design names the safe behaviour that holds until it is closed, so none of them blocks the design; several block the step named.

| # | Item | Closed by | Behaviour until closed |
|---|---|---|---|
| 1 | The Orca `worker-show` field behind `session_join`, and whether join path A or B applies (section 7.2, GQ-108) | Step 1.0a item 4 | `person_started` None for every unmatched transcript, note `tab map join not observable` |
| 2 | `RUN_ID_RE` and `DISPATCH_ID_RE` | Step 1.0a item 10 | Steps 1.4 and 1.6 do not start; no placeholder can match |
| 3 | The `run-current` bound and no-binding shapes, and whether its plain output parses without `--json` (M2) | Step 1.0a items 1 and 2 | FR-002 fourth test and FR-026 case 4 stay gated; a `--json` need goes to the owner as an allowlist change |
| 4 | The unknown-Run response of `worker-list` (a live read on 2026-11-08 shows exit 0 and an empty list, not an error) and the unknown-Run error shape of `task-list` | Step 1.0a item 8 | Any nonzero `worker-list` exit on call one is `unavailable`, not `call_failed (unknown run)`; an empty `worker-list` for a scoped Run counts as complete only while `task-list --run <run>` did not fail (Run not confirmed, section 7.2) |
| 5 | `worker-list` page size and cursor field | Step 1.0a item 3 | A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template |
| 6 | `worker-show` names for `agentWait`, `liveness.verdict` and `status` | Step 1.0a item 4 | Rule 5 cannot match; rows fall to the fallback |
| 7 | Whether `task-list` exposes a Task creator | Step 1.0a item 5 | Creator is could not determine; ready Tasks go to the ownership-review sub-heading |
| 8 | The worktree path field of `worktree ps --json` | Step 1.0a item 6 | Only the root worktree is scanned, with `unscanned:` coverage for the rest; M3 is revisited |
| 9 | The `runtime_unavailable` shape | Step 1.0a item 9, only if seen; never induced | The anchored-marker check of SPEC section 8 is written from the SPEC text and tested with synthetic fixtures only |
| 10 | Whether each template accepts its flags as written | Step 1.0a item 11 | A template that fails is dropped only with an owner note (NFR-014) |
| 11 | That `worker-show` and `task-list` change nothing in Orca: checked statically only (M4) | Step 1.0a before-and-after comparison | The report's lock line stays version-scoped (NFR-015) |
| 12 | The effect of `GIT_OPTIONAL_LOCKS=0` (git documentation only) | Step 1.4a real-git test, control assertion | `--no-optional-locks` carries the guarantee alone |
| 13 | That `--untracked-files=all` overrides `status.showUntrackedFiles` (git documentation only) | Step 1.4a real-git test, if a case is added for it | FR-015 relies on the flag as documented |
| 14 | Which filesystems refuse `os.link` | Observed in use | Exit 1 with `[sweep publish] cannot link report: <error>`; no fallback (section 3.2) |
| 15 | The Orca version file as the version source (NFR-015) | Step 1.0a item 12 | A missing or unreadable file prints the `UNVERIFIED ... observed unknown` lock line |
| 16 | The Claude Code transcript format (one sample read) and how a worktree path maps to its `~/.claude/projects/<project key>/` folder | Step 1.0a, by reading transcripts of the named Run's worktrees (a disk read, not an Orca call) | A transcript is unreadable as defined in 7.2 (observation rule for SPEC line 442: open raises `OSError`, or the tail holds no complete record with both `timestamp` and `sessionId`), and its row is could not determine |
| 17 | Whether `make sync-dev` removes deleted `.claude/` copies | First rollback, or a dry check at step 1.25 | Rollback deletes them by hand and never stages them (section 16) |
| 18 | The effect of `uv run --frozen --no-sync` (flags seen in `uv run --help`, not run) | Step 1.29 or a manual run before release | The skill tries PATH first; the fallback is used only on "command not found" |
| 19 | The rationale for the proposed byte limits (1 MiB, 256 KiB, 8 MiB; SP-28) | Before release, recorded in the task package | The limits apply as proposed and are marked proposed in `probes.py` |
| 20 | Owner decisions GQ-10, GQ-11 (WC-16 approval), GQ-35, GQ-61 and GQ-63 | Step 1.0b | Steps 1.17 to 1.19 do not start; R1 and R2 (step 1.21) wait for step 1.18 and R8 (step 1.24b) waits for step 1.17, so none of them names WC-16 or the new list entry before the contract has it |
| 21 | PR #422 overlap with WC-16, the never-as-worker list and the #409 dimensions | Step 1.16a | Steps 1.17 to 1.19 do not start; WC-16 stays a deliverable of this PR whatever #422 does |
| 22 | Whether Orca workers get tab-map entries (launched through `ccsession`) and which tab-map value equals the item 4 field; and the owner's sign-off on the D9 narrowing of SP-29 (D9 as first written covers only that True becomes None) and on its two residual path-B cases: a window with no end can join a person's later session in the pane as False, and a live session serving two Dispatches joins the older row only | Step 1.0a item 13; step 1.0b | Join path B is not used; a tab-map entry that joins no scoped row gives None; the classify step does not start until the owner signs off D9 or names a stricter rule. Until closed, every no-entry True carries the `origin not proved` note (7.2) |
| 23 | UNVERIFIED: that `worker-show` `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` (read statically from the 1.4.245 bundle) carry a Dispatch row's start time, end time and status live, in the parsed form of 7.2 | Step 1.0a item 4 | No path-B join is made: every path-B match is could not determine with note `Dispatch time window not observable`, and its transcript is None |

Total: 23 open items.

## 18. Revision log: fix cycle 1

Changes made for the blocking findings of `docs/designs/orchestrator-mode-review-1.md`. Minor note m5 was applied because it falls inside the B1 edit; the other minor notes are not addressed in this cycle.

| ID | Finding | Change |
|---|---|---|
| B1 | A temp-file unlink failure after the commit point exited 0 with two names on disk, against NFR-001 | That case now exits 1 with `[sweep publish] could not remove temp file <path>` and no success JSON, and the complete report stays (3.2 step 7 and table, 3.3, 3.4 rule, sequence diagram). Section 1 and the section 16 rollback sentence (m5) now say a successful run leaves one report plus its directory when new. Added the `os.unlink` failure case to `test_cli_contract.py` and the no-second-name check to `test_readonly.py` (11). Updated the NFR-001 and G-1 rows (12). Recorded under "Not counted as deviations" as a joint reading of FR-017 and NFR-001 (13) |
| B2 | The person-started rule assumed every Orca-pane session has a tab-map entry and treated any entry as a worker, which FR-010 does not say | Checked the ccsession source: entries are written only for `ccsession` launches with a valid pane key and terminal handle, each pane keeps only its latest session, and nothing marks a worker pane (1). A worker is now a transcript joined to a scoped Dispatch row; an unjoined tab-map entry gives None; a transcript with no entry may be True when the guard holds; path B adds a stale-entry case to the guard (7.2). The narrowing is D9, with its reason, the owner sign-off at step 1.0b and four `test_classify.py` fixtures (11, 13, 14, 15). Added capture item 13 and open item 22 (15.1, 17). Updated the FR-010 row (12) |
| B3 | SPEC behaviours had no rule, fixture or traceability row | Added the observation rules to 7.2: WC-13 note and Retained problems, show wins, unknown schema field, duplicate Dispatch, input changed between reads, path escapes its source, worktree removed, unreadable transcript or contract, rule 6 wording and SP-07, `FINAL:` reading, remote coverage, and the SP-16 literal. Added each fixture to `test_probes_allowlist.py` (nine byte-limit boundaries, 440, 443, 446, 450, 451, 452), `test_classify.py` (SP-07, `FINAL:`, 442, WC-13, late heartbeat) and `test_report.py` (rule 6 wording, 454, WC-13, SP-16) (11). Named them in the FR-006, FR-010, FR-013, FR-014, FR-020 and NFR-007 rows and added rows for the SPEC section 11 failure modes and the section 7 cross-cutting notes (12) |

### Fix cycle 2

Changes made for the blocking findings of `docs/designs/orchestrator-mode-review-2.md`. Minor note m4 was applied because it falls inside the R2-B1 edit; the other minor notes are not addressed in this cycle. The `tab map join not observable` note for a None `session_join` is kept on purpose, because SPEC line 236 requires the SP-16 literal only when worker rows exist and nothing joined (review 2 m5).

| ID | Finding | Change |
|---|---|---|
| R2-B1 | Under path B, a scoped worker's pane can move to a later session (`/clear`, resume, person rerun), so the later session joins the Dispatch row and the worker's real transcript can become True | A path-B join now also needs session identity: the earliest `timestamp` in the transcript tail must fall inside the Dispatch row's time window, else the row is could not determine and the transcript None with note `pane moved to a later session`; a join inside the window carries `joined by pane: latest session of the pane` (7.2). Added a fourth guard case: under path B with any scoped Dispatch row, every unjoined no-entry transcript is None with note `earlier pane session not joinable (tab map keeps only the latest session)`, and the no-entry True path is path A only (7.2). Said which notes apply when guard cases 1 and 2 hold together (m4). Added `/clear`, resume and person-rerun fixtures and changed "three" to "four" incomplete cases (11). Updated D9, the FR-010 and SP-29 rows (12, 13, 14), capture item 4 (15.1) and added open item 23 for the time fields (17) |
| R2-B2 | A worker of an unscoped Run with no tab-map entry could be shown as person-started True with no note | Every no-entry True now carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and the JSON `notes` (7.2, D9). Changed the third D9 fixture and added an unscoped-Run worker fixture in `test_classify.py`, and a `test_report.py` case that prints the note (11). Open item 22 states the note until it closes (17) |
| R2-B3 | The unreadable-transcript rule fired only on `OSError` at open, but its truncated-JSONL fixture expected `unscanned: transcript not readable` | A transcript is now unreadable when its open raises `OSError` or its 256 KiB tail holds no complete JSON record with both `timestamp` and `sessionId`; a last line cut mid-object is skipped, and the transcript stays readable when an earlier complete record exists (7.2). The fixture now names the cut record, adds the readable last-line-cut case and an `OSError` case (11). Open item 16 points to the same rule (17) |

### Fix cycle 3

Changes made for the blocking findings of review 3 and the re-anchor to master `5dc29d23`.

| ID | Finding | Change |
|---|---|---|
| R3-B1 | The path-B window compares the earliest transcript timestamp with the Dispatch row's start and end times, but `OrcaObservation` and `TranscriptTail` carry no such time fields, so pure `classify.py` cannot evaluate the rule and GQ-103(3) is false | Added `OrcaObservation.dispatch_started`, `dispatch_ended`, `dispatch_status` and `TranscriptTail.first_record_ts` and `tail_complete`, the time-parsing rule, the aware-UTC statement for `now`, `collected_start`, `collected_end` and `mtime`, and the inclusive UTC window with its incomplete-tail case (7.2); `parse_time` and `parse_worker_show` signatures, the `datetime` import and the `read_transcript_tail` comment (4, 7.1); GQ-103(3) list (2.2); capture item 4 and open item 23 name the bundle fields and keep them UNVERIFIED (15.1, 17); reader, parser and window fixtures, the incomplete-tail fixture and the count of existing test files (11); the FR-010 row (12) |
| R3-B2 | Two Dispatch rows on one pane give conflicting results and no rule decides | Added the several-rows rule with the `conflict: one pane session matches several Dispatch rows` note, and the note order for a tab-map entry that fails the window (m11) (7.2); fixtures (11); FR-010, D9 and SP-29 rows (12, 13, 14). Gate fixes: the incomplete tail is handled before the several-rows count, duplicate Dispatch rows are merged first, a session earlier than a row's window gets `session started before this Dispatch window`, a join outcome replaces rules 1 to 8 with rule `fallback`, the SP-16 line is not printed for a pane-matched unjoined transcript, three more fixtures and the setup values of the others (7.2, 11), and the two residual path-B cases stated in D9, SP-29 and open item 22 (13, 14, 17) |
| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_failed`) were dropped from `test_classify.py` | Restored the three SPEC incomplete-case fixtures in `test_classify.py` (11), added the list-incomplete rule and its three `origin unknown:` notes (7.2), named them in the FR-010 row (12), and named the per-Run source row `orca worker-list <run>` (7.4). Corrects cycle 2's "changed three to four incomplete cases": the four join-incomplete cases stay in 7.2, D9 and the FR-010 and SP-29 rows. Gate fixes: an unknown Run id is a complete, empty `worker-list`, so the list-incomplete rule now has five cases, adding Run not confirmed (zero rows and a failed `task-list --run`, note `origin unknown: Run not confirmed`) and the SPEC's tab-map reason (note `origin unknown: tab map unreadable`); the `call_failed` case holds only while `orca_available` is True and covers a Run the budget never reached; all notes that hold are attached in one order; the join-guard bullet no longer says "in the window"; the shared Given has a joined second transcript, the full-page fixture is a hand-built `SweepInput`, the note-order fixture has an exact Given and note list, three fixtures were added (seven `test_fr010_*` in all), and a `collect` test and a lower-bound line test were added (7.2, 7.4, 11, 12). Capture item 8 and open item 4 were reworded, not added (15.1, 17) |
| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coordinator sweep at most once every 5 minutes, and a moved `main.py` insertion point | Renamed the coordinator-loop rule to WC-16 everywhere (1, 8, 9, 10, 12, 15, 16, 17), and marked the SPEC and REPORT draft names in 13 and 14; aligned the cadence with contract line 110 in WC-16 and routing row R2, and recorded the renumbering and the cadence as part of D6 (8, 9, 13); re-anchored contract, test and `main.py` lines; added the fifth pin; recorded the master test constraints (7.6, 8); made step 1.16a record-only; routing row R8 uses the CHANGELOG topic-heading style (9). Gate fixes: the section 16 rollback row now names the `RULE_PHRASES["never-as-worker"]` phrase edit (pin 5); steps 1.18 and 1.19 land in one commit, because the old phrase stops matching once line 23 changes (8, 15.2); step 1.21 now waits for 1.14 and 1.18 and step 1.24b for 1.16 and 1.17, with open item 20 stating it (8, 15.2, 17); R1 to R4 land in one commit and step 1.22 is gated "same commit as 1.21", because R1 without R4 fails the membership test (9, 15.2); WC-16, R2 and D6 now state that `/sc:sweep` is an added read beside master's "The sweep." and stop calling the command "the sweep" (8, 9, 13); and WC-16 says `/sc:sweep` reads are not L1 probes and do not count against the L1 cap (8, 13) |
| R5 | Master's sweep runs `worktree ps --agent-wait`; INV-005 condition 1 forbade it | RESOLVED by the owner 2026-11-08 ("Allow it, no conditions needed."): both `--agent-wait` templates added to `ALLOWED_ORCA`, `--agent-wait` removed from `FORBIDDEN_TOKENS`, D10 recorded; the allowlist pin and the version-scoped claim (Orca 1.4.245) are kept. Gate fixes: the full-sweep recording test now asserts zero argv for both `worktree ps --agent-wait` templates as well as for `worktree list` and `worktree current`, so the "not called in Phase 1" statement is tested for all four templates (7.3, 11) (2.2, 4, 7.3, 11, 12, 13, 15.1) |

## Scoped normative addendum: sweep final chat-summary exception

For section 7.6, section 15.2's GQ-63/style/skill/test allocation, section 17 item 20's GQ-63 boundary and the associated style rollback only, read [the bounded normative addendum](../../.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md). It is a resolved source of this design, not a hidden execution checklist. It narrowly qualifies contrary historical no-exception/(a)-only text; all other design/SPEC/REPORT rules, decisions, QA and history remain unchanged. The owner chose (b), but this revision is planning only: fresh revision checks/PRE and separate execution authorization remain required. The future source allocation is existing 7.10 (canonical Markdown style only, an explicit early-edit exception to its historical pre-implementation phase), 11.3 (skill only) and 11.4 (existing planned test module only); no QA item is repurposed. Eligibility is an instruction contract, not an enforced role detector or a grant to any actual session. Python report/JSON and action authority are unchanged. Original-start retry may erase this appended reference: safe stop before destructive restore is required, never Q0 reseeding or assumed automatic replay.
