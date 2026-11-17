2bedf84882d076e45f7dc00fec100b1f32d104c7
Review one task for spec compliance.

Task brief: Task 1 of the plan .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (AC ids T1.AC1 to T1.AC5 in source order).
## Task 1: Build the post-fix mechanical-check helper and its command

First run the entry check of the Constraints and write `./artifacts/pre-edit-check.md` with one line per condition (the file read, what it said, PASS or FAIL); stop with no edit when a line reads FAIL. The helper is kept even though the follow-up ledger is cut: the L2 step of Tasks 4 and 5 calls it, and its purpose (mechanical checks over the lines a fix pass edited) does not read any ledger.

Create `src/superclaude/cli/review/fixcheck.py` for L2: over the lines a fix pass edited it runs every mechanical check that exists (table pipe count per row, byte-present quotes, recomputed counts, link existence) and returns one result per check for the fix log. Create `src/superclaude/cli/review/fixcheck_cmd.py` exporting `command` (a click command named `fixcheck`, like the other `*_cmd.py` modules) and add `"fixcheck_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py` (re-read the tuple first; stage 1 registered its safety-scan module there). Call shape: `superclaude review fixcheck --file <edited file> (--base <copy saved before the fix> | --lines <start-end>)`, repeatable for several files. It prints one line per check run (check id, file, line, PASS or FAIL, detail) and a last line with the totals, and exits 0 whatever the results, because they go to the fix log and the verifier decides. A defect a verifier finds on a line named in the fix log carries `origin: fix-induced`; the consolidator writes that tag in the carrier text of Tasks 4 and 5, not this code. Add `tests/review/test_review_fixcheck.py` with the run-2 case (an unescaped pipe in a backticked command gives 8 pipes in a 7-cell row).

Acceptance criteria:
- `./artifacts/pre-edit-check.md` has one line for each of the three entry conditions, each reading PASS and naming the file it read.
- `uv run pytest tests/review/test_review_fixcheck.py -v` passes and the run-2 pipe case is detected.
- The helper reports a result for every check it ran, including passes, so the fix log is complete.
- A test shows it edits no file (the bytes of its input files are unchanged after a run).
- `uv run superclaude review fixcheck --help` exits 0; `uv run superclaude review --help` still lists `panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations` and `manifest`, the stage 1 command `safety-scan` and now `fixcheck`; `uv run pytest tests/review/test_review_cli.py -v` passes.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. The cuts that shaped this plan are in `cuts-debate/final-cuts.md` in PF (rows C1 to C14, the S3 table of its section (b), the cross-package facts of its section (c)); where that file and the spec disagree about scope, the cuts file wins. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger `stage-requests/README.md` in PF), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044` and the stage 1 package `TASK-WF-blockerStage1-20261116-030154`. The stage 2 package is withdrawn: its one survivor, the `/sc:implement` print, is task 2 of the stage 1 package.
- One package, one stage. This is stage 3 of the packages that remain (stage 0, stage 1, this one, stage 4). It changes the live review rule. Entry check, read from files and not from memory: the stage 0 package's `./artifacts/stage0c-regrade.md` exists; the stage 1 package is done (it is in the done subfolder of the repository task folder, or it is in the to-do subfolder with a `complete` line for every task in its `progress.md` and a latest `FINAL:` line that reads `FINAL: pass`); the stage 0 errata task has reworded the spec's RT1 row to read "any real blocker found in a Medium list" (`grep -c -F "any real blocker found in a Medium list"` over the spec prints 1 or more; Task 10 quotes it); the stage 3 row of `stage-requests/README.md` in PF holds the owner's go with a date (the go is a chat message recorded there by the session that received it; no hash and no line ruling are part of it). Task 1 runs this check before it creates any file under `src/` or `tests/`, and Task 2 runs it again before the first rule-file edit. A failed check stops the task before any edit and halts the run for the owner. While the check fails, no fix pass, repair, retry or adviser step edits a file under `src/`, `tests/` or `plugins/`, and the acceptance lines of that task that describe the edit do not apply. No task edits the ledger row. Stage 4 starts only after the owner has read the first five runs' Medium lists after the switch and RT1 did not trip (the stage 3 note says how), and the owner's go in chat.
- Limit of what this package shows. The stage 0 regrade is a lower bound: it regrades findings that were already supplied and cannot measure whether a reviewer would have found a defect. The stage 0 result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept); both arms carried the old rule through the same hook, so no task here and no sentence of the Task 10 note cites that regrade as evidence that the new text works. No seeded-defect experiment is run here (the earlier one was confounded: both arms carried the old output style through the SubagentStart hook). What covers discovery is RT1 (spec section 13.2) read by the owner on the first five runs' Medium lists and one small planted-defect check run as part of the live RT1 audit after the switch; both go into the Task 10 note and neither is a build task.
- Owner decisions use the spec's recommendations unless the owner changes them, and none of them is converted into an owner answer here: OD1 no new skill folder, the S1 to S5 bullets of `pragmatic.md` are the one source; OD2 the Medium offer once per run plus at any escalation halt; OD9 reviewer-named consumer; OD11 replace label-max merging, staged (this stage the three agents; the rest is stage 4); OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD16 option (b) for Rule 6 of `rf-qa-qualitative.md`. OD3 (finding text leaving the machine) is open and no task depends on its answer; OD4 stands (no classifier in version 1).
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. Tests that exist only to pin those files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up list. The list of minors is the reviewers' own `follow-up candidates` section plus each task's `notes.md`; no list file, codec, sweep or registry is built. The stage 1 package prints that list at the end of `/sc:implement` (one paragraph titled "Follow-up print (record and print only).", command `superclaude review safety-scan`). This package edits no `sc-implement-protocol` file, no plugin file and no `refs/qa.md`. The once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 2), so no command gains a question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package edits nothing under `plugins/` and creates no plugin mirror, parity test or plugin registry row. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`; that wording moves in stage 4.
- Not built here: no classifier (`superclaude review classify` does not exist), no follow-up list file or `follow-ups` command group, no `sc-review-severity` skill folder, scale map, carrier registry, doctor check or registry drift test, no seeded-recall run, hash-bound owner ruling, shadow stage or baseline file, no Jev or other external judge call, no change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), to `src/superclaude/cli/review/ledger.py` or `review-ledger/1`, to the own-scale primitives of spec section 9.3, to code-assigned severity in `src/superclaude/cli/**/*.py`, to the cap of 2 fix cycles, or to the 35 percent target. Stage 4 edits the doubt wording and the merge text of the templates and rule prompts; this package only copies the S1 to S3 and S5 bullets into the ten tuple files (Task 3).
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`). The installed `~/.claude/output-styles/pragmatic.md` therefore changes only at a refresh (Task 10 says how). Staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Kept mechanical gates (fixed FAIL triggers that stay as named gates) are recorded in the editing task's own `./artifacts/kept-mechanical-gates.md`, one bullet per gate: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to (the Missing condition of the digest), the reason. No `refs/scale-map.md` exists and none is created.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.

Start sha: 2bedf84882d076e45f7dc00fec100b1f32d104c7

Diff against the start snapshot:
```diff
diff --git a/src/superclaude/cli/review/__init__.py b/src/superclaude/cli/review/__init__.py
index f19bc5347..75ac37831 100644
--- a/src/superclaude/cli/review/__init__.py
+++ b/src/superclaude/cli/review/__init__.py
@@ -27,6 +27,7 @@ for _name in (
     "verify_cmd",
     "manifest_cmd",
     "safety_cmd",
+    "fixcheck_cmd",
 ):
     try:
         _module = importlib.import_module(f"{__name__}.{_name}")
diff --git a/src/superclaude/cli/review/fixcheck.py b/src/superclaude/cli/review/fixcheck.py
new file mode 100644
index 000000000..23f91288d
--- /dev/null
+++ b/src/superclaude/cli/review/fixcheck.py
@@ -0,0 +1,144 @@
+"""Mechanical checks over the lines a fix pass edited (L2 of the blocker work).
+
+Read-only: it opens files to read and writes nothing. It returns one result per check it ran,
+passes included, so the fix log is complete. Checks:
+
+- pipe: a markdown table row has as many unescaped pipes as the table's header row.
+- quote: `"quoted text"` followed by a `path:line` cite is byte-present on that cited line.
+- count: a line saying `N rows` right above a table matches the table's data row count.
+- link: a relative markdown link `[text](path)` points at a file or folder that exists.
+"""
+
+from __future__ import annotations
+
+import difflib
+import re
+from dataclasses import dataclass
+from pathlib import Path
+
+_PIPE = re.compile(r"(?<!\\)\|")
+_QUOTE_CITE = re.compile(r"\"([^\"\n]{8,})\"\s*\(?\s*`?([\w./-]+\.\w+):(\d+)")
+_ROWS = re.compile(r"\b(\d+) rows\b")
+_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
+
+
+@dataclass(frozen=True)
+class CheckResult:
+    check: str
+    file: str
+    line: int  # 1-based line in the edited file
+    ok: bool
+    detail: str
+
+
+def parse_range(text: str) -> list[int]:
+    """`5-9` -> [5..9]; `7` -> [7]. Raises ValueError on anything else."""
+    start, _, end = text.partition("-")
+    first, last = int(start), int(end or start)
+    if first < 1 or last < first:
+        raise ValueError(f"bad line range {text!r}")
+    return list(range(first, last + 1))
+
+
+def edited_lines(base_text: str, new_text: str) -> list[int]:
+    """1-based numbers of lines in new_text that are new or changed against base_text."""
+    old, new = base_text.splitlines(), new_text.splitlines()
+    out: list[int] = []
+    for tag, _i1, _i2, j1, j2 in difflib.SequenceMatcher(None, old, new).get_opcodes():
+        if tag in ("replace", "insert"):
+            out.extend(range(j1 + 1, j2 + 1))
+    return out
+
+
+def _table_block(lines: list[str], n: int) -> tuple[int, int]:
+    """Index range [first, last] of the run of `|` lines holding index n."""
+    first = n
+    while first > 0 and lines[first - 1].lstrip().startswith("|"):
+        first -= 1
+    last = n
+    while last + 1 < len(lines) and lines[last + 1].lstrip().startswith("|"):
+        last += 1
+    return first, last
+
+
+def _pipes(row: str) -> int:
+    return len(_PIPE.findall(row))
+
+
+def _cited_text(cite: str, line: int, base: Path) -> str | None:
+    for candidate in (Path(cite), base.parent / cite):
+        if candidate.is_file():
+            rows = candidate.read_text(encoding="utf-8", errors="replace").splitlines()
+            return rows[line - 1] if 1 <= line <= len(rows) else ""
+    return None
+
+
+def run_checks(path: str | Path, line_numbers: list[int]) -> list[CheckResult]:
+    """Run every check that applies to the given 1-based lines of the file."""
+    file = Path(path)
+    lines = file.read_text(encoding="utf-8").splitlines()
+    name = str(path)
+    results: list[CheckResult] = []
+    for number in sorted(set(line_numbers)):
+        if not 1 <= number <= len(lines):
+            continue
+        idx, row = number - 1, lines[number - 1]
+        if row.lstrip().startswith("|"):
+            first, _last = _table_block(lines, idx)
+            want, got = _pipes(lines[first]), _pipes(row)
+            results.append(
+                CheckResult(
+                    "pipe",
+                    name,
+                    number,
+                    got == want,
+                    f"{got} unescaped pipes, header row has {want}",
+                )
+            )
+        for quote, cite, cited_line in _QUOTE_CITE.findall(row):
+            text = _cited_text(cite, int(cited_line), file)
+            if text is None:
+                results.append(
+                    CheckResult(
+                        "quote", name, number, False, f"cited file {cite} not found"
+                    )
+                )
+            else:
+                present = quote in text
+                results.append(
+                    CheckResult(
+                        "quote",
+                        name,
+                        number,
+                        present,
+                        f"quote {'found' if present else 'not found'} at {cite}:{cited_line}",
+                    )
+                )
+        counted = _ROWS.search(row)
+        if counted and idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("|"):
+            first, last = _table_block(lines, idx + 1)
+            data_rows = max(last - first + 1 - 2, 0)  # minus header and separator
+            results.append(
+                CheckResult(
+                    "count",
+                    name,
+                    number,
+                    data_rows == int(counted.group(1)),
+                    f"says {counted.group(1)} rows, the table below has {data_rows}",
+                )
+            )
+        for target in _LINK.findall(row):
+            if "://" in target or target.startswith(("#", "mailto:")):
+                continue
+            bare = target.split("#", 1)[0]
+            exists = bool(bare) and (file.parent / bare).exists()
+            results.append(
+                CheckResult(
+                    "link",
+                    name,
+                    number,
+                    exists,
+                    f"{target} {'exists' if exists else 'does not exist'}",
+                )
+            )
+    return results
diff --git a/src/superclaude/cli/review/fixcheck_cmd.py b/src/superclaude/cli/review/fixcheck_cmd.py
new file mode 100644
index 000000000..3091aa808
--- /dev/null
+++ b/src/superclaude/cli/review/fixcheck_cmd.py
@@ -0,0 +1,61 @@
+"""`superclaude review fixcheck`: mechanical checks over the lines a fix pass edited.
+
+One line per check run, then a totals line. It exits 0 whatever the results, because they go
+to the fix log and the verifier decides. Unusable input (a file that cannot be read, or the
+wrong number of --base / --lines values) exits 2 with a usage message.
+"""
+
+from __future__ import annotations
+
+from pathlib import Path
+
+import click
+
+from superclaude.cli.review import fixcheck as fc
+
+
+def _lines_for(files: tuple[str, ...], bases: tuple[str, ...], ranges: tuple[str, ...]):
+    if len(bases) == len(files) and not ranges:
+        for file, base in zip(files, bases):
+            try:
+                old = Path(base).read_text(encoding="utf-8")
+                new = Path(file).read_text(encoding="utf-8")
+            except (OSError, UnicodeDecodeError) as exc:
+                raise click.UsageError(f"cannot read {file} or {base}: {exc}") from exc
+            yield file, fc.edited_lines(old, new)
+    elif len(ranges) == len(files) and not bases:
+        for file, text in zip(files, ranges):
+            try:
+                yield file, fc.parse_range(text)
+            except ValueError as exc:
+                raise click.UsageError(str(exc)) from exc
+    else:
+        raise click.UsageError(
+            "give one --base or one --lines for every --file, and not both kinds"
+        )
+
+
+@click.command(name="fixcheck")
+@click.option("--file", "files", multiple=True, required=True, help="Edited file.")
+@click.option(
+    "--base", "bases", multiple=True, help="Copy of the file saved before the fix."
+)
+@click.option("--lines", "ranges", multiple=True, help="Edited lines, START-END.")
+def command(
+    files: tuple[str, ...], bases: tuple[str, ...], ranges: tuple[str, ...]
+) -> None:
+    """Run the mechanical checks over the lines a fix pass edited."""
+    results: list[fc.CheckResult] = []
+    for file, numbers in _lines_for(files, bases, ranges):
+        try:
+            results.extend(fc.run_checks(file, numbers))
+        except (OSError, UnicodeDecodeError) as exc:
+            raise click.UsageError(f"cannot read {file}: {exc}") from exc
+    for r in results:
+        click.echo(
+            f"{r.check} {r.file} {r.line} {'PASS' if r.ok else 'FAIL'} {r.detail}"
+        )
+    failed = sum(not r.ok for r in results)
+    click.echo(
+        f"fixcheck: {len(results)} checks, {len(results) - failed} passed, {failed} failed"
+    )
diff --git a/tests/review/test_review_fixcheck.py b/tests/review/test_review_fixcheck.py
new file mode 100644
index 000000000..ceba715ca
--- /dev/null
+++ b/tests/review/test_review_fixcheck.py
@@ -0,0 +1,137 @@
+"""fixcheck: mechanical checks over the lines a fix pass edited."""
+
+from __future__ import annotations
+
+from click.testing import CliRunner
+
+from superclaude.cli.main import main
+from superclaude.cli.review import fixcheck as fc
+
+HEADER = "| a | b | c | d | e | f | g |"
+SEP = "|---|---|---|---|---|---|---|"
+GOOD = "| 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
+# run-2 case: an unescaped pipe inside a backticked command adds a cell to a 7-cell row
+BAD = "| 1 | `grep a|b` | 3 | 4 | 5 | 6 | 7 |"
+ESCAPED = "| 1 | `grep a\\|b` | 3 | 4 | 5 | 6 | 7 |"
+
+
+def write(tmp_path, text, name="doc.md"):
+    path = tmp_path / name
+    path.write_text(text, encoding="utf-8")
+    return path
+
+
+def run(*args):
+    return CliRunner().invoke(main, ["review", "fixcheck", *args])
+
+
+def test_run2_unescaped_pipe_in_backticked_command_is_detected(tmp_path):
+    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n")
+    results = fc.run_checks(doc, [3, 4])
+    assert [(r.check, r.line, r.ok) for r in results] == [
+        ("pipe", 3, True),
+        ("pipe", 4, False),
+    ]
+    assert "9 unescaped pipes, header row has 8" in results[1].detail
+
+
+def test_escaped_pipe_passes(tmp_path):
+    doc = write(tmp_path, "\n".join([HEADER, SEP, ESCAPED]) + "\n")
+    assert [r.ok for r in fc.run_checks(doc, [3])] == [True]
+
+
+def test_quote_check_finds_and_misses_cited_text(tmp_path):
+    source = write(tmp_path, "one\nthe exact words here\n", "src.md")
+    doc = write(
+        tmp_path,
+        f'ok "the exact words" ({source}:2)\nbad "not in the file" ({source}:2)\n'
+        f'gone "whatever text here" (nope/missing.md:1)\n',
+    )
+    got = [(r.check, r.line, r.ok) for r in fc.run_checks(doc, [1, 2, 3])]
+    assert got == [("quote", 1, True), ("quote", 2, False), ("quote", 3, False)]
+
+
+def test_count_check_compares_stated_rows_with_the_table_below(tmp_path):
+    doc = write(
+        tmp_path,
+        "The list has 2 rows\n| h |\n|---|\n| a |\n| b |\n\nIt has 3 rows\n| h |\n|---|\n| a |\n",
+    )
+    got = [(r.check, r.line, r.ok) for r in fc.run_checks(doc, [1, 7])]
+    assert got == [("count", 1, True), ("count", 7, False)]
+
+
+def test_link_check_skips_urls_and_anchors(tmp_path):
+    write(tmp_path, "x", "there.md")
+    doc = write(
+        tmp_path,
+        "[a](there.md#top) [b](missing.md) [c](https://example.com) [d](#local)\n",
+    )
+    got = [r.ok for r in fc.run_checks(doc, [1])]
+    assert got == [True, False]
+
+
+def test_every_check_that_ran_is_reported_including_passes(tmp_path):
+    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n")
+    assert len(fc.run_checks(doc, [1, 2, 3])) == 3
+
+
+def test_edited_lines_from_a_base_copy(tmp_path):
+    new = "a\nB\nc\nd\n"
+    assert fc.edited_lines("a\nb\nc\n", new) == [2, 4]
+    assert fc.parse_range("5-7") == [5, 6, 7]
+
+
+def test_command_prints_one_line_per_check_and_totals_and_exits_zero(tmp_path):
+    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n")
+    res = run("--file", str(doc), "--lines", "3-4")
+    assert res.exit_code == 0
+    assert res.output.splitlines() == [
+        f"pipe {doc} 3 PASS 8 unescaped pipes, header row has 8",
+        f"pipe {doc} 4 FAIL 9 unescaped pipes, header row has 8",
+        "fixcheck: 2 checks, 1 passed, 1 failed",
+    ]
+
+
+def test_command_with_base_and_several_files(tmp_path):
+    base = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n", "base.md")
+    one = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n", "one.md")
+    two = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n", "two.md")
+    res = run(
+        "--file", str(one), "--base", str(base), "--file", str(two), "--base", str(base)
+    )
+    assert res.exit_code == 0
+    assert res.output.splitlines()[-1] == "fixcheck: 1 checks, 0 passed, 1 failed"
+
+
+def test_it_edits_no_file(tmp_path):
+    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n")
+    base = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n", "base.md")
+    before = (doc.read_bytes(), base.read_bytes())
+    fc.run_checks(doc, [1, 2, 3, 4])
+    run("--file", str(doc), "--base", str(base))
+    run("--file", str(doc), "--lines", "1-4")
+    assert (doc.read_bytes(), base.read_bytes()) == before
+
+
+def test_usage_errors_exit_two(tmp_path):
+    doc = write(tmp_path, "x\n")
+    assert run("--file", str(doc)).exit_code == 2
+    assert run("--file", str(doc), "--lines", "9-2").exit_code == 2
+    assert run("--file", str(tmp_path / "none.md"), "--lines", "1").exit_code == 2
+
+
+def test_help_exits_zero_and_review_help_lists_every_subcommand():
+    assert run("--help").exit_code == 0
+    listing = CliRunner().invoke(main, ["review", "--help"]).output
+    for name in (
+        "fixcheck",
+        "safety-scan",
+        "panel",
+        "merge",
+        "ledger",
+        "telemetry",
+        "cluster",
+        "verify-citations",
+        "manifest",
+    ):
+        assert name in listing
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/pre-edit-check.md b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/pre-edit-check.md
new file mode 100644
index 000000000..5c94fbf98
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/pre-edit-check.md
@@ -0,0 +1,12 @@
+# Entry check for stage 3 (read from files, 2026-11-17)
+
+Format per line: condition | file read | what it said | result.
+
+## Task 1 (before any file under src/ or tests/)
+
+1. Stage 0 regrade exists | `.dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0c-regrade.md` | the file exists (15583 bytes); the package is in `done/`, which the plan allows ("to-do or done subfolder") | PASS
+2. Stage 1 package is done | `.dev/tasks/done/TASK-WF-stage1Request-20261116-221852/progress.md` | the package sits in `done/`, holds a `complete` line for T1 and T2 and a `FINAL: pass` line. The plan text names the id `TASK-WF-blockerStage1-20261116-030154`; that package is archived at `.dev/tasks/archive/to-do/` and superseded, and the ledger row of `stage-requests/README.md` names `TASK-WF-stage1Request-20261116-221852` as the stage 1 package | PASS (read against the real stage 1 package; the plan's id is stale)
+3. Spec RT1 row reworded | `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` line 988 | the row reads "Any real blocker found in a Medium list" (capital A). `grep -c -F "any real blocker found in a Medium list"` prints 0 only because of the capital letter; `grep -c -i -F` prints 1 | PASS (case difference only; the words are the plan's)
+4. Owner go for stage 3 recorded with a date | `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md` line 20 | the stage 3 row holds "2026-11-17, owner in chat ("Start stage 3")" | PASS
+
+Note: the Task 1 acceptance line says "three entry conditions"; the Constraints name four (regrade, stage 1 done, RT1 row, owner go). All four are listed above.
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t1-pytest.log b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t1-pytest.log
new file mode 100644
index 000000000..2e49a6fd6
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t1-pytest.log
@@ -0,0 +1,18 @@
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 12 items
+
+tests/review/test_review_fixcheck.py::test_run2_unescaped_pipe_in_backticked_command_is_detected PASSED [  8%]
+tests/review/test_review_fixcheck.py::test_escaped_pipe_passes PASSED    [ 16%]
+tests/review/test_review_fixcheck.py::test_quote_check_finds_and_misses_cited_text PASSED [ 25%]
+tests/review/test_review_fixcheck.py::test_count_check_compares_stated_rows_with_the_table_below PASSED [ 33%]
+tests/review/test_review_fixcheck.py::test_link_check_skips_urls_and_anchors PASSED [ 41%]
+tests/review/test_review_fixcheck.py::test_every_check_that_ran_is_reported_including_passes PASSED [ 50%]
+tests/review/test_review_fixcheck.py::test_edited_lines_from_a_base_copy PASSED [ 58%]
+tests/review/test_review_fixcheck.py::test_command_prints_one_line_per_check_and_totals_and_exits_zero PASSED [ 66%]
+tests/review/test_review_fixcheck.py::test_command_with_base_and_several_files PASSED [ 75%]
+tests/review/test_review_fixcheck.py::test_it_edits_no_file PASSED       [ 83%]
+tests/review/test_review_fixcheck.py::test_usage_errors_exit_two PASSED  [ 91%]
+tests/review/test_review_fixcheck.py::test_help_exits_zero_and_review_help_lists_every_subcommand PASSED [100%]
+
+============================== 12 passed in 0.35s ==============================
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:49:50Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none. Two new modules; the only existing file changed is src/superclaude/cli/review/__init__.py, whose tuple loop imports each module name and calls add_command on its command.

Delta diff from the previous reviewed tree (empty on the first review): 

Earlier blocking findings of this start (empty on the first review): 

Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
