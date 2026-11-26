5e8802f5ce80ba3325b2f1f6b58da66952dcc29f
Review one task for spec compliance.

Task brief: ## Task 8: Add a regression test for the two channels, the nothing-else list and the timing safeguard

Depends on: Task 7

Create tests/skills/test_confirmation_channels.py. It reads src/superclaude/core/WORKER-CONTRACT.md and src/superclaude/skills/sc-implement-protocol/refs/qa.md and asserts: both channel names are present; each item of the nothing-else list is present (another agent's message, coordinator's reply or relay, any file, silence, generic go-ahead, different question or scope, agent-login row, row not created by the person's login); the timing safeguard sentence is present; "executor-invented approval" and "another agent's message" are present; no line in WORKER-CONTRACT.md or qa.md says a relay or a coordinator's reply counts as acceptance; and the ledger Ruling regular expression still matches the chat example and the dashboard example in refs/ledger.md. Follow the helper style already used in tests/skills/test_worker_contract.py.

Acceptance criteria:
- uv run pytest tests/skills/test_confirmation_channels.py passes.
- The test fails when the timing safeguard sentence or any nothing-else item is removed from WORKER-CONTRACT.md (check once by editing a throwaway copy of the text inside the test run, not the repository file).
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 5e8802f5ce80ba3325b2f1f6b58da66952dcc29f
Diff against the start snapshot: 
--- new untracked file tests/skills/test_confirmation_channels.py ---
"""Pin the two valid channels of a person's confirmation (owner decision D3, option 1).

A person's confirmation of a Ruling, a grant row or a pass record counts only when it
is (a) their own chat message or (b) a dashboard response, and nothing else. The
definition lives once in the worker contract (WC-3); the implement skill's qa.md and
ledger.md point to it. The dashboard clause applies only once the dashboard answer
path is released. These tests pin that wording, not the dashboard feature itself.
CI-safe, no network.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_CONTRACT = _REPO / "src" / "superclaude" / "core" / "WORKER-CONTRACT.md"
_IMPL = _REPO / "src" / "superclaude" / "skills" / "sc-implement-protocol" / "refs"
_QA = _IMPL / "qa.md"
_LEDGER = _IMPL / "ledger.md"

CHANNELS = (
    "(a) chat, the person's own chat message in the current conversation",
    "(b) dashboard, a dashboard response, meaning an answer row created through the "
    "dashboard under that person's authenticated login, for the question id whose "
    "text names the exact scope, recorded with the channel (dashboard), the person "
    "id, the question id and the time",
)
NEVER_COUNTS = (
    "another agent's message",
    "a coordinator's reply or relay of a message",
    "any file",
    "silence",
    "a generic go-ahead",
    "an answer to a different question or a different scope",
    "a row written by an agent's login",
    "a row that the person's own login did not create",
)
TIMING = (
    "clause (b) takes effect only when the dashboard answer path is released "
    "(the release 1.8 gates pass); until then only clause (a) counts"
)
RULING_REGEX = re.compile(r"^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$")
# a line that names a relay or a coordinator's reply must say it does not count
RELAY = re.compile(r"coordinator's reply|relay of a message|coordinator's relay")
NEGATORS = ("never", "not acceptance", "is not", "not count")


def _never_counts_line(text: str) -> str:
    """The one line of the definition that lists what never counts."""
    for line in text.splitlines():
        if "**What never counts:**" in line:
            return line
    return ""


def missing_from_contract(text: str) -> list:
    """Return what the contract text lacks of the single definition."""
    gaps = [c for c in CHANNELS if c not in text]
    never_line = _never_counts_line(text)
    gaps += [n for n in NEVER_COUNTS if n not in never_line]
    if TIMING not in text:
        gaps.append(TIMING)
    for phrase in ('"executor-invented approval"', "another agent's message"):
        if phrase not in text:
            gaps.append(phrase)
    return gaps


def _contract() -> str:
    return _CONTRACT.read_text(encoding="utf-8")


def test_contract_defines_both_channels_the_nothing_else_list_and_the_timing():
    assert missing_from_contract(_contract()) == []


def test_contract_names_the_owner_rule_and_the_recording_rule():
    text = _contract()
    assert "a chat message OR dashboard response counts and nothing else" in text
    assert "the person is never asked to write a file" in text
    assert "the answer row id (dashboard)" in text


def test_the_checker_fails_when_a_required_piece_is_removed():
    # throwaway copies of the text; the repository file is never touched
    text = _contract()
    assert TIMING in text
    assert missing_from_contract(text.replace(TIMING, "")) == [TIMING]
    line = _never_counts_line(text)
    assert line
    for item in NEVER_COUNTS:
        # remove the item from the list line only; the same words elsewhere stay
        gaps = missing_from_contract(text.replace(line, line.replace(item, "x")))
        assert item in gaps, item


def test_qa_points_to_the_definition_and_names_both_channels():
    qa = _QA.read_text(encoding="utf-8")
    assert "`~/.claude/WORKER-CONTRACT.md` (WC-3)" in qa
    assert "a chat message in the current conversation, or a dashboard response" in qa
    assert "until then only chat counts" in qa
    assert "another agent's message" in qa
    assert "executor-invented approval" in qa
    # E-NO-RULING still stops for the cases that are not one of the two channels
    assert (
        "`--force`, missing/ambiguous confirmation, or executor-invented approval" in qa
    )
    assert "STOP `E-NO-RULING`" in qa
    assert "src/superclaude" not in qa


def test_no_rule_text_lets_a_coordinator_relay_count():
    for path in (_CONTRACT, _QA, _LEDGER):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if RELAY.search(line):
                assert any(neg in line for neg in NEGATORS), (
                    f"{path.name}:{n}: {line[:120]}"
                )


def test_ledger_ruling_regex_matches_the_chat_and_the_dashboard_example():
    ledger = _LEDGER.read_text(encoding="utf-8")
    assert "^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$" in ledger
    examples = [x for x in ledger.splitlines() if x.startswith("T2: Ruling:")]
    chat = [x for x in examples if "user confirmed in current conversation" in x]
    dash = [x for x in examples if "dashboard answer row" in x]
    assert chat and dash
    assert all(RULING_REGEX.match(x) for x in chat + dash)



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (a new test file; no existing dependents).
Context: the new test reads src/superclaude/core/WORKER-CONTRACT.md and refs/qa.md and refs/ledger.md; it passed (6 tests), and ruff check and ruff format pass. tests/skills/test_task_workspace_lifecycle.py was only reformatted by ruff beyond Task 7's edit if the diff shows so.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/tests/skills/test_confirmation_channels.py b/tests/skills/test_confirmation_channels.py
deleted file mode 100644
index 362ab395f..000000000
--- a/tests/skills/test_confirmation_channels.py
+++ /dev/null
@@ -1,115 +0,0 @@
-"""Pin the two valid channels of a person's confirmation (owner decision D3, option 1).
-
-A person's confirmation of a Ruling, a grant row or a pass record counts only when it
-is (a) their own chat message or (b) a dashboard response, and nothing else. The
-definition lives once in the worker contract (WC-3); the implement skill's qa.md and
-ledger.md point to it. The dashboard clause applies only once the dashboard answer
-path is released. These tests pin that wording, not the dashboard feature itself.
-CI-safe, no network.
-"""
-
-import re
-from pathlib import Path
-
-_REPO = Path(__file__).resolve().parents[2]
-_CONTRACT = _REPO / "src" / "superclaude" / "core" / "WORKER-CONTRACT.md"
-_IMPL = _REPO / "src" / "superclaude" / "skills" / "sc-implement-protocol" / "refs"
-_QA = _IMPL / "qa.md"
-_LEDGER = _IMPL / "ledger.md"
-
-CHANNELS = (
-    "(a) chat, the person's own chat message in the current conversation",
-    "(b) dashboard, a dashboard response, meaning an answer row created through the "
-    "dashboard under that person's authenticated login, for the question id whose "
-    "text names the exact scope, recorded with the channel (dashboard), the person "
-    "id, the question id and the time",
-)
-NEVER_COUNTS = (
-    "another agent's message",
-    "a coordinator's reply or relay of a message",
-    "any file",
-    "silence",
-    "a generic go-ahead",
-    "an answer to a different question or a different scope",
-    "a row written by an agent's login",
-    "a row that the person's own login did not create",
-)
-TIMING = (
-    "clause (b) takes effect only when the dashboard answer path is released "
-    "(the release 1.8 gates pass); until then only clause (a) counts"
-)
-RULING_REGEX = re.compile(r"^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$")
-# a line that names a relay or a coordinator's reply must say it does not count
-RELAY = re.compile(r"coordinator's reply|relay of a message|coordinator's relay")
-NEGATORS = ("never", "not acceptance", "is not", "not count")
-
-
-def missing_from_contract(text: str) -> list:
-    """Return what the contract text lacks of the single definition."""
-    gaps = [c for c in CHANNELS if c not in text]
-    gaps += [n for n in NEVER_COUNTS if n not in text]
-    if TIMING not in text:
-        gaps.append(TIMING)
-    for phrase in ('"executor-invented approval"', "another agent's message"):
-        if phrase not in text:
-            gaps.append(phrase)
-    return gaps
-
-
-def _contract() -> str:
-    return _CONTRACT.read_text(encoding="utf-8")
-
-
-def test_contract_defines_both_channels_the_nothing_else_list_and_the_timing():
-    assert missing_from_contract(_contract()) == []
-
-
-def test_contract_names_the_owner_rule_and_the_recording_rule():
-    text = _contract()
-    assert "a chat message OR dashboard response counts and nothing else" in text
-    assert "the person is never asked to write a file" in text
-    assert "the answer row id (dashboard)" in text
-
-
-def test_the_checker_fails_when_a_required_piece_is_removed():
-    # throwaway copies of the text; the repository file is never touched
-    text = _contract()
-    assert TIMING in text
-    assert missing_from_contract(text.replace(TIMING, "")) == [TIMING]
-    for item in NEVER_COUNTS[1:]:  # "another agent's message" also appears elsewhere
-        gaps = missing_from_contract(text.replace(item, "x"))
-        assert item in gaps, item
-
-
-def test_qa_points_to_the_definition_and_names_both_channels():
-    qa = _QA.read_text(encoding="utf-8")
-    assert "`~/.claude/WORKER-CONTRACT.md` (WC-3)" in qa
-    assert "a chat message in the current conversation, or a dashboard response" in qa
-    assert "until then only chat counts" in qa
-    assert "another agent's message" in qa
-    assert "executor-invented approval" in qa
-    # E-NO-RULING still stops for the cases that are not one of the two channels
-    assert (
-        "`--force`, missing/ambiguous confirmation, or executor-invented approval" in qa
-    )
-    assert "STOP `E-NO-RULING`" in qa
-    assert "src/superclaude" not in qa
-
-
-def test_no_rule_text_lets_a_coordinator_relay_count():
-    for path in (_CONTRACT, _QA, _LEDGER):
-        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
-            if RELAY.search(line):
-                assert any(neg in line for neg in NEGATORS), (
-                    f"{path.name}:{n}: {line[:120]}"
-                )
-
-
-def test_ledger_ruling_regex_matches_the_chat_and_the_dashboard_example():
-    ledger = _LEDGER.read_text(encoding="utf-8")
-    assert "^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$" in ledger
-    examples = [x for x in ledger.splitlines() if x.startswith("T2: Ruling:")]
-    chat = [x for x in examples if "user confirmed in current conversation" in x]
-    dash = [x for x in examples if "dashboard answer row" in x]
-    assert chat and dash
-    assert all(RULING_REGEX.match(x) for x in chat + dash)

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T8.AC2 at=tests/skills/test_confirmation_channels.py:79 anchor="The test fails when the timing safeguard sentence or any nothing-else item is removed" chk=y,n,n,n family=mutation-check-coverage fix=check the nothing-else items against the "What never counts" line only and mutate that line for every item first=A1 origin=new: the mutation check skips "another agent's message" (it also sits at WORKER-CONTRACT.md:57) and presence is tested against the whole file, so removing an item from the list line alone can leave the test green.

Saved-probe re-check hit locations (may be empty): probe-1-1 family=mutation-check-coverage command hits after the fix: lines for NEVER_COUNTS, never_line and the line-scoped replace in tests/skills/test_confirmation_channels.py


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
