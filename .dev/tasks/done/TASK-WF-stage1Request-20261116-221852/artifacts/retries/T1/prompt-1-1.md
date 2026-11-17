6dac6232c3c4ad56101c2e2f640800698ad1dda1
Review one task for spec compliance.

Task brief: Task 1 of the plan .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md (AC ids T1.AC1 to T1.AC8 in source order).
## Task 1: Build the safety scan module and the `safety-scan` command

Before creating any file, run the entry check: the stage ledger `stage-requests/README.md` in PF must hold an owner go for stage 1 with a date; when it does not, create nothing and report to the owner. Then create three things.

First, `src/superclaude/cli/review/safety_route.py`. It keeps the GR1 vocabulary in one list and nowhere else: delete, overwrite, force, token, secret, password, chmod and similar words (the spec's GR1 row lists these; further words are added only to that list). A word matches case-insensitively at the start of a word, so `deleted` and `tokens` hit and `reinforce` does not. It takes plain row text, one row per line (blank lines are not rows, and a row that begins with `superseded ` is history: it is skipped and counted, never scanned), and returns for each hit the line number, the matched word and the row text, plus the count of rows read and rows skipped. It holds the GR12 rule as one function over the three outcomes in their fixed order Note, Medium, Blocking: given the outcome a reviewer graded a row and whether the row has a hit, it returns Blocking for a hit and the given outcome otherwise, so it can only raise an outcome and a hit is never a plain follow-up. It imports no codec, no ledger reader and no classifier, and no function in it lowers an outcome. Input that cannot be read (path missing, a folder, not valid UTF-8) is a typed unreadable result with its reason, a different value from a read that found zero hits.

Second, `src/superclaude/cli/review/safety_cmd.py`, exporting `command` (a click command named `safety-scan`), registered by adding `"safety_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py` (the name does not clash with `panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations` or `manifest`; `lint_cmd` and `estimate_cmd` are optional names in that tuple whose modules do not exist). `superclaude review safety-scan <file> [--unattended]` prints one line per hit in the form `SAFETY HIT line <n> (<word>), graded blocking: <row text>`, then one summary line `safety-scan: <r> rows read, <s> skipped, <h> hits`. With one or more hits and no `--unattended`, it also prints a line that names the person prompt: `Show these rows to the person before they are treated as follow-ups.` With `--unattended` and one or more hits, its last line is `safety-scan signal: partial` (the run is then recorded as partial and waits for nobody); with `--unattended` and no hit, the last line is `safety-scan signal: none`. An empty file prints `safety-scan: file is empty, 0 rows read`. Unreadable or missing input prints `safety-scan: cannot read <file>: <reason>` on standard output, exits 2, and never prints a hit count. In every other case the command exits 0 (a hit is information, not a failure). It calls no `gh`, no network and no subprocess.

Third, the tests: `tests/review/test_review_safety_route.py` (each vocabulary word hits; case and word-start rule; a `superseded ` row is skipped and counted; the outcome function never returns an outcome below the one given, checked over all three outcomes with and without a hit; a Medium or Note row with a hit becomes Blocking; a row without a hit keeps its outcome; unreadable input is its own result and not zero hits; the module source holds no import of a codec, ledger reader or classifier) and `tests/review/test_review_safety_cmd.py` (help exits 0; the output lines above for a hit, no hit and an empty file; attended person-prompt line; unattended `partial` and `none` last lines; a missing file, a folder and a non-UTF-8 file each give exit 2 and the `cannot read` line with no hit count).

Acceptance criteria:
- The entry check passed: the stage ledger in PF holds an owner go for stage 1 with a date. When it does not, no file is created.
- `uv run pytest tests/review/test_review_safety_route.py tests/review/test_review_safety_cmd.py tests/review/test_review_cli.py -v` passes, and the first two files cover each case named in the task body.
- `uv run superclaude review safety-scan --help` exits 0, and `uv run superclaude review --help` lists `safety-scan` and every earlier subcommand (`panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations`, `manifest`).
- A readable file with no hit prints a summary line with `0 hits`; a missing path prints `cannot read` with exit 2 and no `hits` text. The two outputs differ, shown in `./artifacts/print-smoke.txt` (Task 2 appends the rest of that file).
- No function in `safety_route.py` lowers an outcome: the test over the three outcomes passes and the outcome order Note, Medium, Blocking is defined once.
- `grep -n -i "classif\|codec\|follow_up\|ledger" src/superclaude/cli/review/safety_route.py src/superclaude/cli/review/safety_cmd.py` prints nothing, and `grep -n "subprocess\|requests\|httpx\|\bgh\b" src/superclaude/cli/review/safety_route.py src/superclaude/cli/review/safety_cmd.py` prints nothing.
- The vocabulary list appears in one place only: `grep -c "chmod" src/superclaude/cli/review/safety_route.py src/superclaude/cli/review/safety_cmd.py` shows the word in `safety_route.py` and not in `safety_cmd.py`.
- `make lint` reports no new findings for the two modules.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` and the cuts list `cuts-debate/final-cuts.md` both sit inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF. The cuts list is authoritative where it differs from the earlier stage requests (revision 4 of the source says so); the rows C1 to C4, C7 and C10 of its section (a) decide what this package builds. Section numbers, requirement ids (REQ-nn) and guardrails (GR1, GR12) refer to the spec.
- One package, two tasks. This is stage 1 of four packages (stages 0, 1, 3 and 4); stage 2 is withdrawn into this package and has no package of its own. The package adds new files only (the scan module, its command module and their tests) and edits exactly three existing files: `src/superclaude/cli/review/__init__.py` (one name added to the tuple of subcommand modules, Task 1) and `SKILL.md` and `refs/managed-workspace.md` of the `sc-implement-protocol` skill (Task 2), plus the two plugin twins of those skill files. It edits no other review-loop carrier. It runs only after the owner has said go for stage 1 in chat and the go is recorded in the stage ledger `stage-requests/README.md` in PF (Task 1 checks that). Stage 3 starts only after this package is done, as its own entry check reads.
- Depth. The source's revision 4 says this package has two tasks in two phases and `depth: quick`; the program gate checker that requires `depth: standard` and 4 to 8 phases fails it for that reason only. The owner chose `quick` in chat on 2026-11-16.
- Not built (cuts rows C1, C2, C3, C4 and C10): the follow-up ledger and its codec, the classifier and its inputs supplier, the carrier registry and scale map, the new skill folder and its references, the install check for digest versions, the registry drift tests, the owner summary file, the sweep and the shadow stage. Nothing here reads, writes or names any of them, and no stored tag for a safety hit exists: the scan only prints.
- Also not built: any Jev or other external judge call, key or account (owner decision OD3 stays open; no finding text leaves the machine); any edit of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` or its plugin twin (it keeps its own scale, and its final summary "never asks the user anything"); any edit of `src/superclaude/cli/review/ledger.py`, `WORKER-CONTRACT.md` or the own-scale primitives; code-assigned severity in `src/superclaude/cli/**/*.py`, with one exception: the safety-only raise function of the new `src/superclaude/cli/review/safety_route.py` (the GR12 raise-only rule of Task 1, which promotes a row with a safety hit to Blocking and never lowers an outcome) is built; any change to the cap of 2 fix cycles.
- Retired carriers stay unedited. `/sc:task` and task-builder are being retired (owner, 2026-11-16): no task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`.
- Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface. The one existing hand-kept twin it touches is `plugins/superclaude/skills/sc-implement-protocol/`, and only its two files `SKILL.md` and `refs/managed-workspace.md`, because `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins them byte for byte to their sources. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this plan does not decide it.
- Carrier choice. The owner approved the final review step of `/sc:implement` as the follow-up carrier, "record and print only". The once-per-run offer question stays with the top-level session through the output style, so the added paragraph asks the user nothing, makes no offer and adds no stop code.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. New text added to installed primitives avoids the words the static scans pin (the halt, stop and ruling words of `tests/skills/test_implement_severity_static.py`, the old cap wording and the sweep-phrase patterns of `tests/skills/test_review_severity_rule.py`) and cites no `SKILL.md:<number>` style pointer.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...` and `uv run python ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.

Start sha: 6dac6232c3c4ad56101c2e2f640800698ad1dda1

Diff against the start snapshot:
```diff
diff --git a/src/superclaude/cli/review/__init__.py b/src/superclaude/cli/review/__init__.py
index 6b2d8aa87..f19bc5347 100644
--- a/src/superclaude/cli/review/__init__.py
+++ b/src/superclaude/cli/review/__init__.py
@@ -26,6 +26,7 @@ for _name in (
     "cluster_cmd",
     "verify_cmd",
     "manifest_cmd",
+    "safety_cmd",
 ):
     try:
         _module = importlib.import_module(f"{__name__}.{_name}")
diff --git a/src/superclaude/cli/review/safety_route.py b/src/superclaude/cli/review/safety_route.py
new file mode 100644
index 000000000..88d13ecff
--- /dev/null
+++ b/src/superclaude/cli/review/safety_route.py
@@ -0,0 +1,114 @@
+"""Safety scan of plain row text (GR1 vocabulary) and the raise-only outcome rule (GR12).
+
+The scan reads one row per line and reports rows that hold destructive or secret
+vocabulary. It stores nothing and calls nothing: it only reports. The outcome rule can
+raise an outcome and never lowers one, so a hit is never a plain follow-up.
+"""
+
+from __future__ import annotations
+
+import re
+from dataclasses import dataclass
+from pathlib import Path
+
+# Outcomes in their fixed order, defined once. A higher index is a higher outcome.
+OUTCOMES = ("Note", "Medium", "Blocking")
+
+# The GR1 vocabulary, kept in this one list and nowhere else. A word matches
+# case-insensitively at the start of a word: "deleted" and "tokens" hit, "reinforce" does not.
+VOCABULARY = (
+    "delete",
+    "overwrite",
+    "force",
+    "token",
+    "secret",
+    "password",
+    "chmod",
+    "credential",
+    "wipe",
+)
+
+_PATTERN = re.compile(
+    r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(w) for w in VOCABULARY) + ")",
+    re.IGNORECASE,
+)
+
+# A row that starts with this prefix is history: skipped and counted, never scanned.
+SUPERSEDED_PREFIX = "superseded "
+
+
+@dataclass(frozen=True)
+class Hit:
+    line: int  # 1-based line number in the input
+    word: str  # the matched vocabulary word, as written in the row
+    row: str  # the row text
+
+
+@dataclass(frozen=True)
+class ScanResult:
+    hits: tuple[Hit, ...]
+    rows_read: int
+    rows_skipped: int
+    empty: bool  # the input held no text at all (only whitespace)
+
+
+@dataclass(frozen=True)
+class Unreadable:
+    """The input could not be read. Different from a read that found zero hits."""
+
+    path: str
+    reason: str
+
+
+def scan_text(text: str) -> ScanResult:
+    """Scan plain row text, one row per line. Blank lines are not rows."""
+    hits: list[Hit] = []
+    rows_read = 0
+    rows_skipped = 0
+    for number, raw in enumerate(text.splitlines(), start=1):
+        row = raw.strip()
+        if not row:
+            continue
+        if row.startswith(SUPERSEDED_PREFIX):
+            rows_skipped += 1
+            continue
+        rows_read += 1
+        found = _PATTERN.search(row)
+        if found:
+            hits.append(Hit(line=number, word=found.group(1), row=row))
+    return ScanResult(
+        hits=tuple(hits),
+        rows_read=rows_read,
+        rows_skipped=rows_skipped,
+        empty=not text.strip(),
+    )
+
+
+def scan_file(path: str | Path) -> ScanResult | Unreadable:
+    """Read a file as UTF-8 and scan it; an unreadable input is its own result."""
+    name = str(path)
+    try:
+        data = Path(path).read_bytes()
+    except FileNotFoundError:
+        return Unreadable(name, "no such file")
+    except IsADirectoryError:
+        return Unreadable(name, "is a directory")
+    except OSError as exc:
+        return Unreadable(name, exc.strerror or "unreadable")
+    try:
+        text = data.decode("utf-8")
+    except UnicodeDecodeError:
+        return Unreadable(name, "not valid UTF-8")
+    return scan_text(text)
+
+
+def raise_outcome(graded: str, has_hit: bool) -> str:
+    """GR12: a row with a hit becomes Blocking; otherwise the graded outcome stands.
+
+    The result is never below the graded outcome.
+    """
+    if graded not in OUTCOMES:
+        raise ValueError(f"unknown outcome {graded!r}; expected one of {OUTCOMES}")
+    if not has_hit:
+        return graded
+    return max(graded, OUTCOMES[-1], key=OUTCOMES.index)
diff --git a/src/superclaude/cli/review/safety_cmd.py b/src/superclaude/cli/review/safety_cmd.py
new file mode 100644
index 000000000..1ea33f5ab
--- /dev/null
+++ b/src/superclaude/cli/review/safety_cmd.py
@@ -0,0 +1,44 @@
+"""`superclaude review safety-scan <file>`: print rows that hold destructive or secret words.
+
+A hit is information, not a failure, so the command exits 0 on any readable input.
+Unreadable or missing input exits 2 and never prints a hit count.
+"""
+
+from __future__ import annotations
+
+import click
+
+from superclaude.cli.review import safety_route as route
+
+PERSON_PROMPT = "Show these rows to the person before they are treated as follow-ups."
+
+
+@click.command(name="safety-scan")
+@click.argument("file", type=str)
+@click.option(
+    "--unattended",
+    is_flag=True,
+    default=False,
+    help="Worker mode: end with a signal line instead of asking a person.",
+)
+def command(file: str, unattended: bool) -> None:
+    """Scan FILE (one row per line) for destructive or secret vocabulary."""
+    result = route.scan_file(file)
+    if isinstance(result, route.Unreadable):
+        click.echo(f"safety-scan: cannot read {result.path}: {result.reason}")
+        raise SystemExit(2)
+    for hit in result.hits:
+        click.echo(
+            f"SAFETY HIT line {hit.line} ({hit.word}), graded blocking: {hit.row}"
+        )
+    if result.empty:
+        click.echo("safety-scan: file is empty, 0 rows read")
+    else:
+        click.echo(
+            f"safety-scan: {result.rows_read} rows read, "
+            f"{result.rows_skipped} skipped, {len(result.hits)} hits"
+        )
+    if unattended:
+        click.echo(f"safety-scan signal: {'partial' if result.hits else 'none'}")
+    elif result.hits:
+        click.echo(PERSON_PROMPT)
diff --git a/tests/review/test_review_safety_route.py b/tests/review/test_review_safety_route.py
new file mode 100644
index 000000000..5c6f9eb37
--- /dev/null
+++ b/tests/review/test_review_safety_route.py
@@ -0,0 +1,125 @@
+"""Safety scan module: vocabulary, row handling and the raise-only outcome rule."""
+
+from __future__ import annotations
+
+import ast
+import re
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.review import safety_route as route
+
+SOURCE = Path(route.__file__)
+
+
+@pytest.mark.parametrize("word", route.VOCABULARY)
+def test_each_vocabulary_word_hits(word):
+    result = route.scan_text(f"the recipe will {word} the target\n")
+    assert [h.word.lower() for h in result.hits] == [word]
+    assert result.rows_read == 1
+
+
+@pytest.mark.parametrize(
+    "row,hit",
+    [
+        ("Files were DELETED by the step", True),
+        ("two tokens leak", True),
+        ("a Secret value", True),
+        ("we reinforce the wall", False),  # "force" inside a word does not hit
+        ("untokenized input", False),
+        ("nothing risky here", False),
+    ],
+)
+def test_case_and_word_start_rule(row, hit):
+    assert bool(route.scan_text(row).hits) is hit
+
+
+def test_vocabulary_is_one_list_with_the_gr1_words():
+    for word in (
+        "delete",
+        "overwrite",
+        "force",
+        "token",
+        "secret",
+        "password",
+        "chmod",
+    ):
+        assert word in route.VOCABULARY
+    assert len(set(route.VOCABULARY)) == len(route.VOCABULARY)
+
+
+def test_superseded_row_is_skipped_and_counted_never_scanned():
+    text = "superseded this row says delete everything\nlive row says delete\n\n"
+    result = route.scan_text(text)
+    assert result.rows_skipped == 1
+    assert result.rows_read == 1
+    assert [h.line for h in result.hits] == [2]
+
+
+def test_blank_lines_are_not_rows_and_hits_carry_line_numbers():
+    result = route.scan_text("\n\nfirst\n\nsecond has a password\n")
+    assert result.rows_read == 2
+    assert result.hits[0].line == 5
+    assert result.hits[0].row == "second has a password"
+
+
+def test_empty_input_is_flagged_empty():
+    assert route.scan_text("").empty
+    assert route.scan_text("  \n\n").empty
+    assert not route.scan_text("x\n").empty
+
+
+@pytest.mark.parametrize("graded", route.OUTCOMES)
+def test_outcome_is_never_lowered(graded):
+    for has_hit in (True, False):
+        out = route.raise_outcome(graded, has_hit)
+        assert route.OUTCOMES.index(out) >= route.OUTCOMES.index(graded)
+
+
+def test_hit_promotes_note_and_medium_to_blocking_and_no_hit_keeps_outcome():
+    assert route.raise_outcome("Note", True) == "Blocking"
+    assert route.raise_outcome("Medium", True) == "Blocking"
+    assert route.raise_outcome("Blocking", True) == "Blocking"
+    for graded in route.OUTCOMES:
+        assert route.raise_outcome(graded, False) == graded
+
+
+def test_outcome_order_is_defined_once_and_unknown_outcome_is_rejected():
+    assert route.OUTCOMES == ("Note", "Medium", "Blocking")
+    with pytest.raises(ValueError):
+        route.raise_outcome("Minor", True)
+
+
+def test_unreadable_input_is_its_own_result_not_zero_hits(tmp_path):
+    missing = route.scan_file(tmp_path / "nope.md")
+    folder = route.scan_file(tmp_path)
+    bad = tmp_path / "bad.md"
+    bad.write_bytes(b"\xff\xfe\x00 not utf-8 \x80")
+    binary = route.scan_file(bad)
+    for result, reason in (
+        (missing, "no such file"),
+        (folder, "is a directory"),
+        (binary, "not valid UTF-8"),
+    ):
+        assert isinstance(result, route.Unreadable)
+        assert result.reason == reason
+    ok = tmp_path / "ok.md"
+    ok.write_text("clean row\n", encoding="utf-8")
+    result = route.scan_file(ok)
+    assert isinstance(result, route.ScanResult)
+    assert result.hits == ()
+
+
+def test_module_imports_no_unrelated_reader_and_makes_no_call_out():
+    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
+    imported = []
+    for node in ast.walk(tree):
+        if isinstance(node, ast.Import):
+            imported += [a.name for a in node.names]
+        elif isinstance(node, ast.ImportFrom):
+            imported.append(node.module or "")
+    banned = re.compile(
+        r"classif|codec|ledger|follow_up|subprocess|requests|httpx|socket", re.I
+    )
+    assert not [name for name in imported if banned.search(name)], imported
diff --git a/tests/review/test_review_safety_cmd.py b/tests/review/test_review_safety_cmd.py
new file mode 100644
index 000000000..0036510f9
--- /dev/null
+++ b/tests/review/test_review_safety_cmd.py
@@ -0,0 +1,96 @@
+"""`superclaude review safety-scan`: output lines, exit codes and the unattended signal."""
+
+from __future__ import annotations
+
+from click.testing import CliRunner
+
+from superclaude.cli.main import main
+
+PROMPT = "Show these rows to the person before they are treated as follow-ups."
+
+
+def run(*args):
+    return CliRunner().invoke(main, list(args))
+
+
+def write(tmp_path, text, name="notes.md"):
+    path = tmp_path / name
+    path.write_text(text, encoding="utf-8")
+    return str(path)
+
+
+def test_help_exits_zero_and_review_help_lists_the_new_and_earlier_commands():
+    assert run("review", "safety-scan", "--help").exit_code == 0
+    listing = run("review", "--help")
+    assert listing.exit_code == 0
+    for name in (
+        "safety-scan",
+        "panel",
+        "merge",
+        "ledger",
+        "telemetry",
+        "cluster",
+        "verify-citations",
+        "manifest",
+    ):
+        assert name in listing.output
+
+
+def test_hit_prints_hit_line_then_summary_then_the_person_prompt(tmp_path):
+    path = write(
+        tmp_path, "abc123\nthe step will delete the tree\nsuperseded old delete\n"
+    )
+    res = run("review", "safety-scan", path)
+    assert res.exit_code == 0, res.output
+    assert res.output.splitlines() == [
+        "SAFETY HIT line 2 (delete), graded blocking: the step will delete the tree",
+        "safety-scan: 2 rows read, 1 skipped, 1 hits",
+        PROMPT,
+    ]
+
+
+def test_no_hit_prints_zero_hits_and_no_prompt(tmp_path):
+    res = run("review", "safety-scan", write(tmp_path, "abc123\nall fine here\n"))
+    assert res.exit_code == 0
+    assert res.output.splitlines() == ["safety-scan: 2 rows read, 0 skipped, 0 hits"]
+
+
+def test_empty_file_prints_the_empty_line(tmp_path):
+    res = run("review", "safety-scan", write(tmp_path, ""))
+    assert res.exit_code == 0
+    assert res.output.splitlines() == ["safety-scan: file is empty, 0 rows read"]
+
+
+def test_unattended_hit_ends_with_partial_and_has_no_person_prompt(tmp_path):
+    res = run(
+        "review", "safety-scan", "--unattended", write(tmp_path, "rotate the secret\n")
+    )
+    assert res.exit_code == 0
+    lines = res.output.splitlines()
+    assert lines[-1] == "safety-scan signal: partial"
+    assert PROMPT not in res.output
+    assert lines[0].startswith("SAFETY HIT line 1 (secret)")
+
+
+def test_unattended_no_hit_ends_with_none(tmp_path):
+    res = run("review", "safety-scan", "--unattended", write(tmp_path, "fine\n"))
+    assert res.exit_code == 0
+    assert res.output.splitlines()[-1] == "safety-scan signal: none"
+
+
+def test_missing_folder_and_non_utf8_each_exit_two_without_a_hit_count(tmp_path):
+    bad = tmp_path / "bad.md"
+    bad.write_bytes(b"\xff\xfe\x00\x80")
+    for target in (str(tmp_path / "missing.md"), str(tmp_path), str(bad)):
+        res = run("review", "safety-scan", target)
+        assert res.exit_code == 2, res.output
+        assert res.output.startswith(f"safety-scan: cannot read {target}: ")
+        assert "hits" not in res.output
+        assert "rows read" not in res.output
+
+
+def test_missing_input_is_different_from_a_clean_read(tmp_path):
+    clean = run("review", "safety-scan", write(tmp_path, "fine\n"))
+    missing = run("review", "safety-scan", str(tmp_path / "missing.md"))
+    assert "0 hits" in clean.output and clean.exit_code == 0
+    assert "hits" not in missing.output and missing.exit_code == 2
diff --git a/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt b/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt
new file mode 100644
index 000000000..cb611c59b
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt
@@ -0,0 +1,9 @@
+## Task 1 smoke: clean file
+$ superclaude review safety-scan <clean file>
+safety-scan: 2 rows read, 0 skipped, 0 hits
+exit=0
+
+## Task 1 smoke: missing path
+$ superclaude review safety-scan <missing file>
+safety-scan: cannot read <tmp>/missing.md: no such file
+exit=2
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:06:11Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none. The two modules are new; the only existing file changed is src/superclaude/cli/review/__init__.py, whose tuple loop imports each module name and calls add_command on its `command`.

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
