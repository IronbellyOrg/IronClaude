# QA Report: Final gate, maintainability lens

Reviewer: rf-qa-qualitative (T324). fix_authorization: false. Report is the only file written.

## Scope read

Read from disk now, in chunks of at most 150 lines: `final-inventory.md`; every line of `src/superclaude/cli/sweep/{__init__,models,probes,classify,commands,report}.py`; `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md`; the `main.py` diff and lines 540-571; `git diff` of `pragmatic.md` and `WORKER-CONTRACT.md`; the house patterns `cli/tasklist/__init__.py`, `cli/issue_watch/` (listing, `__init__.py`, grep of `runner.py`, `cycle.py`, `launch.py`), `cli/reflect/contract.py:55-100`; the DESIGN lines cited below; helper sections of the sweep tests (`conftest.py`, `test_classify.py`, `test_report.py`, `test_cli_contract.py`, `test_probes_allowlist.py`); the contract templates `skills/sc-workflow-protocol/refs/return-contract.md:44-57`; `followups.md`.

Commands run (all read-only): `uv run ruff check`, `uv run ruff format --check`, `make verify-sync`, `uv run pytest tests/sweep tests/commands/test_sweep_command.py -q` (694 passed), plain `grep`/`sed`/`git diff`/`git status`. One experiment on a private /tmp copy of `probes.py` and `models.py` (deleted afterwards; `git status` shows no repository file changed by this review).

Not run: any live Orca, ccsession or Claude command; `make sync-dev`; `superclaude sweep run`. Not re-judged here: behaviour correctness of the classifier rules and the contract/style wording (other lenses); the maintainability lens counts them only where they affect the next maintainer.

## Findings

### F1. MAJOR. A hand-written YAML reader duplicates `yaml.safe_load`, which the repo already uses on the same file, and it misreads valid YAML

- Evidence: `src/superclaude/cli/sweep/probes.py:686-721` (`_yaml_top`, `_unquote`) parses `return-contract.yaml`. PyYAML is a hard dependency (`pyproject.toml:38`, `"pyyaml>=6.0"`) used in 22 modules, and `src/superclaude/cli/reflect/contract.py:65-82` (`parse_contract`) reads the same file name with `yaml.safe_load` plus `except yaml.YAMLError`. DESIGN `orchestrator-mode.md:211` lists no `yaml` among what `probes.py` may import, and the enforced ban list (`tests/sweep/test_classify.py:1827`) does not forbid it, so the design neither requires nor forbids the hand parser; no comment in `probes.py` says why it exists.
- Measured on a private /tmp copy (`_yaml_top` against `yaml.safe_load`): `worker_status: blocked  # waiting on owner` gives `'blocked  # waiting on owner'` (PyYAML: `'blocked'`); a two-line plain scalar `blocked_question: first line\n  second line` gives `'first line'` (PyYAML: `'first line second line'`); `artifacts: [a.md, "b, c.md"]` gives `['a.md', '"b', 'c.md"']` (PyYAML: `['a.md', 'b, c.md']`).
- The format workers are told to write already uses trailing comments: `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52` (`artifacts: [...]   # ...`) and `:54` (`reason: ...   # only when failed`), and `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:388-389`. With `artifacts: [...]   # ...` the value no longer ends in `]`, so `_yaml_top` returns a string and `probes.py:741` silently yields `artifacts=()` (harmless today: `ContractRecord.artifacts` is never read in `classify` or `report`). The same slip on the `worker_status` line is not harmful in the templates (line 49 has no comment) but is not guarded either.
- Why it matters: `classify.py:165-170` (rule 1) requires `contract.worker_status == "blocked"` exactly, so a valid contract whose status line carries a comment is not seen as blocked, and the report can then show `working` or `could not determine` for a worker that waits on a person, the case this command exists to surface. No test pins `_yaml_top` against such inputs (`grep _yaml_top tests/sweep` finds nothing). I did not observe a misclassification on a template-shaped contract; this is a demonstrated parser divergence with a latent output effect, graded MAJOR because rule 1 depends on it and the fix is small.
- Smallest fix: replace `_yaml_top` and `_unquote` with `yaml.safe_load(text)` inside `try/except yaml.YAMLError`, treating a non-mapping result as `{}`, as `reflect/contract.py:65-82` does, and add `yaml` to the DESIGN 7.1 line 211 import list. If the owner wants a stdlib-only reader, strip a trailing ` #` comment from scalar and flow values, join continued plain scalars, split flow items with the quotes respected, add a one-line why-comment, and pin the three inputs above in `tests/sweep/test_probes_allowlist.py`.

### Minor notes (never fail the gate)

**F2. MINOR. Repeated blocks inside `probes.py`.**
- The "ok means a `read` source row, anything else means an `unscanned` row and, for `unavailable`, `state.available = False`" block appears three times: `probes.py:1053-1063` (`record`, a closure inside `_orca_reads`), `probes.py:1202-1208` (`_show`) and `probes.py:1254-1272` (`collect`, the `worktree ps` call). `record` cannot be reused because it is a closure.
- The list filter `[x for x in raw if isinstance(x, dict)] if isinstance(raw, list) else []` appears at `probes.py:1076-1078` and `probes.py:1090-1094`.
- "Read the last N bytes and drop the partial first line" appears at `probes.py:576-581` (`_ledger_has_final`) and `probes.py:827-832` (`_transcript.read`).
- Fix: lift `record` to a module function taking `state` and `sources`; add `_dict_rows(raw)` and `_tail_bytes(handle, size, n)`.

**F3. MINOR. Constants copied between modules, where `models.py` already shows the safe pattern.**
- `report.py:34` `COULD_NOT_JOIN` equals `classify.py:68-70` `NOTE_COULD_NOT_JOIN`; `report.py:35` `WC13_NOTE` equals `classify.py:78` `NOTE_WC13`; the report matches classify's notes by string equality (`report.py:328`, `report.py:355`), so a one-sided edit silently drops a report line.
- `report.py:26-27` `_IDLE = CLASSES[5]`, `_UNKNOWN = CLASSES[7]` re-derive by index what `classify.py:42-51` already names `C_IDLE` and `C_UNKNOWN`; a reorder of `CLASSES` renames them silently.
- `report.py:32` hard-codes `100` where `probes.py:73` has `WORKER_LIST_PAGE`.
- `models.py:19-21` and `models.py:26-28` carry the comment "so the two cannot drift" for the same reason. Mitigation: each side is pinned by its own literal in the tests (`test_classify.py:79,86`, `test_report.py:68,69`), so drift fails a test. Fix: move the two notes and the class names for idle and unknown into `models.py`.

**F4. MINOR. Paths and environment rules repeated between `commands.py` and `probes.py`.**
- `commands.py:253` and `probes.py:1287-1289` both resolve `XDG_STATE_HOME`; `commands.py:260` and `probes.py:855` both spell `ccsession/orca-tabs`; `commands.py:259` and `probes.py:1368` both spell `~/.claude/projects`. The `--output` overlap guard (`commands.py:254-262`) only protects what `commands.py` lists, so a change to where `probes` reads makes the guard stale without any failing test noticing. `cli/issue_watch/cycle.py:189` has a third copy of the `XDG_STATE_HOME` rule elsewhere in the repo.
- `commands.py:95-96` `_within` has a redundant `path == folder or` (`Path.is_relative_to` is already true for equal paths; checked with `uv run python`), and it duplicates the idea of `probes.py:545-550` `_inside`.
- Fix: one `state_dir()` and the two folder names exposed from `probes` and used by `commands`.

**F5. MINOR. Comments that point at things a reader cannot open.**
- `classify.py:781`, `:789`, `:800` cite `REPORT:1248`. It resolves to `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md:1248` (line 1248 holds the dimension-source text), but the comment names no file and the package will move to `done/`.
- `classify.py:567` and `classify.py:809-810` say "see the final report" without a file name; no file in the repository carries that name.
- Fix: name the DESIGN section that records each decision (DESIGN line 468 covers `OQ-14`) or write the reason in the comment itself.

**F6. MINOR. Missing one-line why-comments on builder decisions.**
- `classify.py:190-207` (`_exit_proof`) and `classify.py:218-222` (`_rule_fenced`) read `orca.worker_done_seen` and `orca.fenced_evidence`, but `probes.py` never sets either (`grep` finds them only in `models.py` and `classify.py`; defaults are `None` and `"unreadable"`, `models.py:86-87`). So both rules cannot fire in a real run. Only `report.py:36-39` (`SP24_LINE`) says so. A maintainer reading `classify.py` sees two live rules that are dead; add one line saying "not observed in Phase 1 (SP-24); `probes` sets no value yet".
- `commands.py:170` opens the report with mode `0o666` and no reason (DESIGN line 107 records the choice).
- `classify.py:515-516` forces three window fields to `None` after the loop with no reason; `_window` (`classify.py:544`) already tests `conflicts`, so why the fields are also blanked is not visible.

**F7. MINOR. Names that hide what the code does.**
- `classify.py:595` `_add(book, key, note)` adds a note once; `_Joins.left` (`classify.py:592`), `.taken`, `.forced`, `.row_notes` do not say "unjoined transcript", "joined transcript indexes", "notes that force could not determine", "info notes".
- `classify.py:876`, `:900`, `:925`, `:929-933`, `:939` pass `(row, info, forced, source)` as an unnamed 4-tuple and index it as `b[0]`; a small named tuple reads better. `classify_all` (`classify.py:867-996`) is about 130 lines doing join, build, freeze, summary.
- `probes.py:608` `_marker` returns a bool (`_has_marker`); `classify.py:826` `_norm` strips a trailing slash; `probes.py:71` `LEDGER_SPLIT` suggests a head and tail split but only the tail is read (`probes.py:577-580`); `report.py:35-36` `WC13_NOTE`, `SP24_LINE` are named by spec id, not by content.
- `models.py:74` and `:76` `dispatch_status` and `status` both come from `dispatch.status` (`probes.py:431,433`); they differ only in the disagreeing-rows case (`probes.py:1157-1160`), and no comment says why there are two.
- `classify.py:210-215` `_rule_blocked_contract`/`_rule_orca_exit_proof` call `_blocked_contract(row)[0]` and `_exit_proof(row)[0]`, and `classify.py:370` calls both again for `[1]`; rules 1 and 2 run twice per row and the split names do not say why.

**F8. MINOR. Unused or test-only surface.**
- `models.py:83` `OrcaObservation.unsupervised` is never set or read (no hit in `src`, `tests` or the DESIGN text).
- Set but never read by production code: `TranscriptTail.project_key` (`models.py:118`, set at `probes.py:801,811`), `TabMapEntry.launch_dir` (`models.py:125`, `probes.py:878`), `StatusParse.branch_header` (`models.py:157`, `probes.py:512`).
- `probes.py:603`, `:677`, `:767`, `:849`, `:882`, `:978` (`read_ledger`, `read_packages`, `read_contract`, `read_transcript_tail`, `read_tab_map`, `read_worktree`) have no production caller; `collect` uses the private versions. DESIGN lines 397-401 list them as the API, so this is deliberate, but no comment says they are the test seam.

**F9. MINOR. Typing escapes that come from loose types.**
- Eight `# type: ignore` in the package: `report.py:78,82,142,188,357,665`, `classify.py:517`, `probes.py:845`. Three in `report.py` (`:188`, `:357`, `:665`) exist because `SweepResult.summary` is `dict[str, object]` (`models.py:247`); three (`:78`, `:82`, `:142`) because `_iso`, `_window_text` and `_distinct` take `object`. A frozen `Summary` dataclass and `datetime`/`timedelta` parameter types remove those six.

**F10. MINOR. Test helpers copied between files.**
- `make_ctx` is identical at `tests/sweep/test_classify.py:130-139` and `tests/sweep/test_report.py:124-133`; `orca()` and `obs()` have the same body (`test_classify.py:142-144`, `test_report.py:142-144`); `_captured` is identical at `test_cli_contract.py:73-74` and `test_probes_allowlist.py:228-229`. `tests/sweep/conftest.py` already holds the shared `fixed_now` and `sweep_root` fixtures, so these belong there.

**F11. MINOR. Two comments that restate the code.** `probes.py:638` (`# no such folder: nothing to read` after `except FileNotFoundError: continue`) and `models.py:59` (`window_start: datetime  # now - window`).

### Checked and fine

- `main.py:567-569` matches the six earlier deferred pairs, including the `# noqa: E402,I001  # intentional: ...` text (`main.py:543-565`). `cli/sweep/__init__.py` is the same lazy `__getattr__` export as `cli/tasklist/__init__.py:9-17` and `cli/recommend/__init__.py:12`.
- `issue_watch/runner.py` wraps subprocess for a different purpose (injectable runner); the sweep keeps its own two seams on purpose (one subprocess module with argv allowlists), so no reuse is missed there.
- The exemption text appears in both `pragmatic.md` and `SKILL.md` "Final reply" by design (SKILL.md line 33 says so), and parity tests pin both copies (`tests/commands/test_sweep_command.py:424,429,552-635`).
- No pre-existing repository helper does what `parse_time` does (`fromisoformat` callers elsewhere parse other formats), and no helper builds Claude's project key (`probes.py:1002-1004`).

## Checks

A check is FAIL only when it carries a BLOCKING or MAJOR finding; MINOR notes are listed in the third column.

| Check | Result | Basis |
|---|---|---|
| C1 No hand-written helper where a repo helper or dependency already does the job | FAIL | F1 (MAJOR): `_yaml_top` vs `yaml.safe_load`, measured divergence |
| C2 No repeated logic inside one module (probes) | PASS | notes F2 |
| C3 No constants or values copied between modules | PASS | notes F3 (each copy pinned by its own test literal) |
| C4 No paths or environment rules repeated between modules | PASS | notes F4 |
| C5 No comment that restates the code | PASS | note F11 |
| C6 Comments point at things a reader can open | PASS | note F5 |
| C7 One-line why-comment on each builder decision | PASS | note F6 |
| C8 Names say what the code does | PASS | note F7 |
| C9 No dead fields or test-only surface left unexplained | PASS | notes F8 |
| C10 Types do not need blanket escapes | PASS | note F9 |
| C11 Copies the house patterns (`main.py` deferred pair, lazy `__getattr__` export, `issue_watch` layout) | PASS | read `main.py:543-569`, `tasklist/__init__.py`, `issue_watch/` |
| C12 Duplicated normative text (style and skill) is pinned against drift | PASS | `test_sweep_command.py:424,429,552-635` |
| C13 Test helpers are shared, not copied | PASS | note F10 |
| C14 `uv run ruff check` and `ruff format --check` on the sweep files | PASS | "All checks passed!"; "16 files already formatted" |
| C15 `make verify-sync` | PASS | "All components in sync." |
| C16 `uv run pytest tests/sweep tests/commands/test_sweep_command.py` | PASS | 694 passed in 2.68s (the 3 full-run failures in `phase14-full-pytest.md` were not re-argued here; they are outside this lens) |
| C17 Experiment left no repository file changed | PASS | /tmp copy deleted; `git status --short -- src tests docs plugins` (first 10 lines read) showed only edited files named in `final-inventory.md`, no new path |

Verdict: FAIL
Blocking count: 1
