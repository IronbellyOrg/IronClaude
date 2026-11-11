98d1765254823766d1c954aae97fe1388c056e46
Review one task for spec compliance.

Task brief: 
## Task 2: Build the sanitizer `sanitize.py`

Depends on: Task 1

Create `src/superclaude/cli/observe/sanitize.py` and `tests/observe/test_sanitize.py`, following `ARCHITECTURE-SPINE.md` AD-9, `adapter-contract.md` section "Paging, errors, sanitizing" and tests T29 and T44 in `acceptance-tests.md`. Write it in this package: do not import `canvas.py`, and treat `ANSI_ESCAPE_RE` in `src/superclaude/cli/eval/pty_stream.py` as too weak. `sanitize(text, mode="line")` keeps printable characters only. It removes CSI and OSC sequences (7-bit and 8-bit introducers; OSC ended by BEL or ST or unterminated through the end of the string), DCS, SOS, PM and APC strings, any other ESC plus the next character, the C1 range U+0080 to U+009F (including the 8-bit `\x9b`), C0 controls and DEL, and Unicode `Cf` format characters (bidi controls such as U+202E included). Line mode replaces each newline with one space; block mode keeps newlines (used only for `stage.detail`, `stage.activity` and stderr in the inspector). The function always returns `str`.

Acceptance criteria:
- [T2.AC1] `uv run pytest tests/observe/test_sanitize.py -v` passes.
- [T2.AC2] An injection test (CSI colour, OSC 8 hyperlink, unterminated OSC, `\x9b`, BEL, U+202E, a window-title sequence) shows the output contains no ESC, no C1 character, no C0 control other than a newline in block mode, and no `Cf` character, and that the visible words around the sequences survive.
- [T2.AC3] A test puts `\n` inside a value and shows line mode returns one line while block mode keeps the newline.
- [T2.AC4] Plain text, CJK text and emoji pass through unchanged.
- [T2.AC5] Square brackets such as `[bold]x[/bold]` pass through unchanged (markup safety is enforced by the renderers, asserted in Task 10).

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

Start sha: 98d1765254823766d1c954aae97fe1388c056e46
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/sanitize.py b/src/superclaude/cli/observe/sanitize.py
new file mode 100644
index 000000000..0e411ae4f
--- /dev/null
+++ b/src/superclaude/cli/observe/sanitize.py
@@ -0,0 +1,48 @@
+"""The observer's own text sanitizer: untrusted text in, printable literal text out (AD-9).
+
+Written for this package; the weaker ``ANSI_ESCAPE_RE`` in ``eval/pty_stream.py`` and the
+design prototype are not used. Markup safety is not this module's job: renderers build
+``rich.text.Text`` objects from data and never parse worker text as markup.
+"""
+
+from __future__ import annotations
+
+import re
+import unicodedata
+
+# One pass over every escape form. Strings (OSC, DCS, SOS, PM, APC) run to their
+# terminator or, when there is none, to the end of the text.
+_ESCAPES = re.compile(
+    r"(?:\x1b\]|\x9d)[\s\S]*?(?:\x07|\x1b\\|\x9c|\Z)"  # OSC: BEL, ST or end
+    r"|(?:\x1b[PX^_]|[\x90\x98\x9e\x9f])[\s\S]*?(?:\x1b\\|\x9c|\Z)"  # DCS, SOS, PM, APC
+    r"|(?:\x1b\[|\x9b)[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]?"  # CSI, 7-bit and 8-bit
+    r"|\x1b[\s\S]?"  # any other ESC plus the next character
+)
+_NEWLINES = re.compile(
+    r"\r\n|\r|" + chr(0x2028) + "|" + chr(0x2029)
+)  # CRLF, CR, LS, PS
+_DROPPED = frozenset({"Cc", "Cf", "Cs"})  # C0, DEL, C1, format (bidi) and surrogates
+
+
+def sanitize(text: object, mode: str = "line") -> str:
+    """Return ``text`` as printable characters only.
+
+    ``mode="line"`` turns each newline into one space; ``mode="block"`` keeps newlines
+    (used only for ``stage.detail``, ``stage.activity`` and stderr in the inspector).
+    """
+    if mode not in ("line", "block"):
+        raise ValueError(f"unknown sanitize mode: {mode!r}")
+    if text is None:
+        return ""
+    if isinstance(text, bytes):
+        text = text.decode("utf-8", errors="replace")
+    elif not isinstance(text, str):
+        text = str(text)
+    text = _ESCAPES.sub("", text)
+    text = _NEWLINES.sub("\n", text)
+    newline = " " if mode == "line" else "\n"
+    return "".join(
+        newline if ch == "\n" else ch
+        for ch in text
+        if ch == "\n" or unicodedata.category(ch) not in _DROPPED
+    )
diff --git a/tests/observe/test_sanitize.py b/tests/observe/test_sanitize.py
new file mode 100644
index 000000000..7e673261a
--- /dev/null
+++ b/tests/observe/test_sanitize.py
@@ -0,0 +1,122 @@
+"""Sanitizer tests (AD-9; T29 and T44 in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import unicodedata
+
+import pytest
+
+from superclaude.cli.observe.sanitize import sanitize
+
+RLO = chr(0x202E)  # bidi override, a Unicode Cf character
+LINE_SEPARATOR = chr(0x2028)
+IDEOGRAPHIC_SPACE = chr(0x3000)
+REPLACEMENT = chr(0xFFFD)
+
+INJECTION = (
+    "a\x1b[31mred\x1b[0m "  # CSI colour
+    "b\x1b]8;;http://evil.example\x1b\\link\x1b]8;;\x1b\\ "  # OSC 8 hyperlink, ST terminated
+    "c\x1b]2;window title\x07title "  # window-title sequence, BEL terminated
+    "d\x9b31mC1 "  # 8-bit CSI
+    "e\x07bell "  # BEL
+    f"f{RLO}RLO "  # bidi override (Cf)
+    "g\x1bPdcs payload\x1b\\dcs "  # DCS string
+    "h\x1b_apc payload\x1b\\apc "  # APC string
+    "i\x1b(Bplain "  # other ESC plus next character
+    "end\x1b]0;unterminated"  # unterminated OSC runs to the end
+)
+
+
+def _bad_chars(text: str, allow_newline: bool = False) -> list[str]:
+    bad = []
+    for ch in text:
+        if ch == "\n" and allow_newline:
+            continue
+        if ch == "\x1b" or unicodedata.category(ch) in ("Cc", "Cf", "Cs"):
+            bad.append(repr(ch))
+    return bad
+
+
+@pytest.mark.parametrize("mode", ["line", "block"])
+def test_injection_leaves_no_control_or_format_characters(mode):
+    out = sanitize(INJECTION, mode)
+    assert _bad_chars(out, allow_newline=(mode == "block")) == []
+    assert "\x9b" not in out and RLO not in out
+    for word in (
+        "red",
+        "link",
+        "title",
+        "C1",
+        "bell",
+        "RLO",
+        "dcs",
+        "apc",
+        "plain",
+        "end",
+    ):
+        assert word in out
+    for payload in (
+        "evil.example",
+        "window title",
+        "dcs payload",
+        "apc payload",
+        "unterminated",
+    ):
+        assert payload not in out
+
+
+def test_unterminated_osc_runs_to_the_end_of_the_text():
+    assert sanitize("keep\x1b]0;gone forever") == "keep"
+    assert sanitize("keep\u009d0;gone forever") == "keep"
+
+
+def test_incomplete_csi_is_removed_without_eating_text_before_it():
+    assert sanitize("ok\x1b[31") == "ok"
+    assert sanitize("ok\x1b") == "ok"
+
+
+def test_newline_line_mode_is_one_line_and_block_mode_keeps_it():
+    value = f"first\nsecond\r\nthird\rfourth{LINE_SEPARATOR}fifth"
+    assert sanitize(value, "line") == "first second third fourth fifth"
+    assert "\n" not in sanitize(value, "line")
+    assert sanitize(value, "block") == "first\nsecond\nthird\nfourth\nfifth"
+
+
+def test_default_mode_is_line():
+    assert sanitize("a\nb") == "a b"
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        "plain text 123",
+        "日本語のテキスト",
+        "中文 and English",
+        "rocket 🚀 ok",
+        f"café{IDEOGRAPHIC_SPACE}spaced",
+    ],
+)
+def test_plain_cjk_and_emoji_pass_through_unchanged(text):
+    assert sanitize(text) == text
+    assert sanitize(text, "block") == text
+
+
+def test_square_brackets_pass_through_unchanged():
+    assert sanitize("[bold]x[/bold] [red]y") == "[bold]x[/bold] [red]y"
+
+
+def test_always_returns_str():
+    assert sanitize(None) == ""
+    assert sanitize(b"bytes \xff ok") == f"bytes {REPLACEMENT} ok"
+    assert sanitize(42) == "42"
+    assert isinstance(sanitize(""), str)
+
+
+def test_sanitize_is_idempotent():
+    once = sanitize(INJECTION, "block")
+    assert sanitize(once, "block") == once
+
+
+def test_unknown_mode_is_rejected():
+    with pytest.raises(ValueError):
+        sanitize("x", "other")

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
