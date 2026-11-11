c05a22e8a540c1db881117a0495c5b2414964ad1
Review one task for spec compliance.

Task brief: 
## Task 14: Register `superclaude observe` in the shipped CLI

Depends on: Task 13

Edit `src/superclaude/cli/main.py` and create `tests/observe/test_registration.py`. Add one block before `if __name__ == "__main__":`, in the same form as the existing registrations (for example the `reflect_group` block): `from superclaude.cli.observe.commands import observe_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` followed by `main.add_command(observe_group, name="observe")`. This is production integration under reading 1 of `release-gates.md` and is covered by the authorization evidence in the Constraints; nothing else in `main.py` changes. It runs only after Task 13 has passed: `release-gates.md` makes the golden samples of the four kinds and T32 the R1 gate, and a failed gate keeps the previous view. If Task 13 is blocked (for example no Orca CLI validates), this task is blocked too and `main.py` is not edited.

Acceptance criteria:
- [T14.AC1] Before the edit, `uv run pytest tests/observe/test_golden_contract.py -v` passes, and the final report says so.
- [T14.AC2] `uv run superclaude observe --help` exits 0 and lists `--once`, `--width`, `--ascii`, `--fixture`, `--run` and `--snapshot`.
- [T14.AC3] `uv run superclaude --help` lists `observe` among the commands.
- [T14.AC4] `uv run superclaude observe --once --fixture base` exits 0 and prints a record whose first line contains `SYNTHETIC FIXTURE base, not Orca data`.
- [T14.AC5] `uv run pytest tests/observe/test_registration.py -v` passes using click's `CliRunner`, and the existing test suite for the CLI group still passes (`uv run pytest tests/cli -v`).
- [T14.AC6] `git diff` for this task touches `src/superclaude/cli/main.py` only by the two added lines and their blank-line spacing, plus the new test file.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: c05a22e8a540c1db881117a0495c5b2414964ad1
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/main.py b/src/superclaude/cli/main.py
index ffe4a34df..b0497914c 100644
--- a/src/superclaude/cli/main.py
+++ b/src/superclaude/cli/main.py
@@ -560,6 +560,10 @@ from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  #
 
 main.add_command(reflect_group, name="reflect")
 
+from superclaude.cli.observe.commands import observe_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
+
+main.add_command(observe_group, name="observe")
+
 
 if __name__ == "__main__":
     main()
diff --git a/tests/observe/test_registration.py b/tests/observe/test_registration.py
new file mode 100644
index 000000000..cadfc6ce1
--- /dev/null
+++ b/tests/observe/test_registration.py
@@ -0,0 +1,49 @@
+"""``superclaude observe`` is registered in the shipped CLI (AD-2; release-gates.md reading 1)."""
+
+from __future__ import annotations
+
+import importlib.util
+import re
+from pathlib import Path
+
+from click.testing import CliRunner
+
+from superclaude.cli.main import main
+from superclaude.cli.observe.commands import observe_group
+
+
+def test_the_group_lists_observe_among_its_commands():
+    assert main.commands["observe"] is observe_group
+    result = CliRunner().invoke(main, ["--help"])
+    assert result.exit_code == 0
+    assert re.search(r"^\s+observe\s", result.output, re.M)
+
+
+def test_observe_help_lists_every_option():
+    result = CliRunner().invoke(main, ["observe", "--help"])
+    assert result.exit_code == 0
+    for option in ("--once", "--width", "--ascii", "--fixture", "--run", "--snapshot"):
+        assert option in result.output
+
+
+def test_once_fixture_base_prints_a_record_with_the_synthetic_banner_first():
+    result = CliRunner().invoke(main, ["observe", "--once", "--fixture", "base"])
+    assert result.exit_code == 0
+    first = result.output.splitlines()[0]
+    assert "SYNTHETIC FIXTURE base, not Orca data" in first
+    assert "\x1b" not in result.output
+
+
+def test_main_py_registers_observe_with_one_deferred_block_in_the_house_form():
+    spec = importlib.util.find_spec(
+        "superclaude.cli.main"
+    )  # the package attribute `main` is the group
+    text = Path(spec.origin).read_text(encoding="utf-8")
+    block = (
+        "from superclaude.cli.observe.commands import observe_group  # noqa: E402,I001  "
+        "# intentional: deferred subcommand registration to avoid circular imports\n"
+        "\n"
+        'main.add_command(observe_group, name="observe")\n'
+    )
+    assert text.count(block) == 1
+    assert text.index(block) < text.index('if __name__ == "__main__":')

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
