ff1bdec3deb808b62615177d34be7fc96dbd39d8
Review one task for spec compliance.

Task brief: ## Task 17: Port the gh, MCP, tamper, escape and amendment corpus

Depends on: Task 16

Add to tests/hooks/test_launch_level_guard.py the remaining corpus categories of design section 11: gh api writes (T-ATK-6, 18, 47), tamper and escape (T-ATK-21, 55, 60), the benign cases and pinned over-blocks not covered by Task 16, the N-ATK amendment attacks 1 to 39 not covered by Task 16, the message cases T-MSG-1 to T-MSG-6 (T-MSG-4 to T-MSG-6 are defined at merged-requirements.md lines 1102 to 1104 and include the competing-class precedence assertions; plus one live-format check of the block message text through the real script), the acceptance map of design section 11 (each of AC-1 to AC-8 has at least the listed cases present), and the boundary cases of design section 10 not yet covered (PR title docs: explain git hooks at FS allowed, PR body naming pull request and git giving MERGE with LL-TEXT, orca with a continuation line, commit scope fix(ccsession): x giving ESCAPE, Write content quoting .claude/hooks allowed, Monitor with only ws, 65537 bytes of multi-byte text). Expected values are written by hand from design sections 4, 5 and 10.

Acceptance criteria:
- uv run pytest tests/hooks/ -v passes and the new tests are present as named or parametrized cases.
- A test maps AC-1 to AC-8 to their minimum case lists from design section 11 and fails if any listed case id is missing from the module.
- Each OB- item remains a skipped test in tests/hooks/test_launch_level_observations.py and is not duplicated here.

AC ids (source order):
T17.AC1: uv run pytest tests/hooks/ -v passes and the new tests are present as named or parametrized cases.
T17.AC2: A test maps AC-1 to AC-8 to their minimum case lists from design section 11 and fails if any listed case id is missing from the module.
T17.AC3: Each OB- item remains a skipped test in tests/hooks/test_launch_level_observations.py and is not duplicated here.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: ff1bdec3deb808b62615177d34be7fc96dbd39d8
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t17-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t17-test.log
new file mode 100644
index 00000000..e60a0fcb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t17-test.log
@@ -0,0 +1,7 @@
+# uv run pytest tests/hooks/ -q  (last 3 lines)
+tests/hooks/test_launch_level_observations.py .....ssssssssssss          [100%]
+
+================= 4121 passed, 12 skipped in 351.70s (0:05:51) =================
+
+# uv run pytest tests/hooks/test_launch_level_guard.py -k "ATK or MSG or AC"  (summary line)
+=============== 1731 passed, 2069 deselected in 85.11s (0:01:25) ===============
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 065c8080..e1348668 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -4208,3 +4208,316 @@ def test_cor2_replay_real_attacks(tmp_path):
     assert f"{head} commit\trefs/heads/feature" in after
     main = [line for line in before.splitlines() if line.endswith("refs/heads/main")]
     assert main and main[0] in after.splitlines()
+
+
+# --- Task 17: gh api writes, tamper, escape, benign, N-ATK, messages, AC map --
+#
+# Expected results are written by hand from design sections 4, 5 and 10 (DD-2),
+# not copied from the MR corpus columns; every row below agrees with MR section
+# 8.3/8.4 (no "override:" was needed). The leaks N-ATK-31 and 36, the git rows
+# N-ATK-1 to 19 and 37, T-OVR-1 to 6 and the git/gh T-OK rows are in Task 16.
+
+CORPUS17 = [
+    # gh api writes (H2: method, field, graphql or a non-plain form).
+    ("ATK-6", "gh api --method=POST repos/o/r/merges", GHWRITE),
+    ("ATK-18", "X=X; gh api repos/o/r/git/refs/heads/main -$X DELETE", GHWRITE),
+    ("ATK-47", "gh api graphql -f query='mutation{mergePullRequest}'", GHWRITE),
+    # Tamper and escape.
+    ("ATK-21", f"rm -rf {STATE_PATH}", TAMPER),
+    ("ATK-55", "cd ~/.cla" + "ude && rm -rf state", TAMPER),
+    ("ATK-60", "claude \\\n-p x", ESCAPE),
+    # Benign rows without git or gh (T-OK-14 is the Edit row below).
+    ("OK-10", "uv run pytest", NONE4),
+    ("OK-11", "make sync-dev", NONE4),
+    ("OK-13", "cat README.md", NONE4),
+    ("OK-35", "grep -rn claude docs/", NONE4),
+    ("OK-36", "grep claude -rn docs/", NONE4),
+    # Amendment attacks not in Task 16.
+    ("NATK-20", "X=ge; flock /tmp/l gh pr mer$X 5", UNK),
+    ("NATK-21", "if :; then gh repo sync; fi", MERGE),
+    ("NATK-22", "if :; then gh pr update-branch 5; fi", MERGE),
+    ("NATK-23", "g$''h pr merge 5", MERGE),
+    (
+        "NATK-24",
+        "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
+        GHWRITE,
+    ),
+    ("NATK-25", "g\\\nh pr merge 5", UNK),
+    # H5: `$(` ends the segment, so the api.github.com word has no gh word.
+    (
+        "NATK-26",
+        'curl -sS -X PATCH -H "Authorization: token $(gh auth token)" '
+        "https://api.github.com/repos/o/r/git/refs/heads/main "
+        '-d \'{"sha":"abc","force":true}\'',
+        GHWRITE,
+    ),
+    ("NATK-27", 'npx -y @anthropic-ai/claude-code@latest -p "finish the task"', ESCAPE),
+    ("NATK-28", 'cl\\\naude -p "finish the task"', UNK),
+    # NM1a comes first; the split word names no tamper path.
+    ("NATK-29", "rm -rf ~/.cla\\\nude/state", UNK),
+    ("NATK-30", "rm -rf ~/.cla$''ude/state", TAMPER),
+    ("NATK-32", "cp /tmp/s.json ~/.cla" + "ude/set$''tings.json", TAMPER),
+    ("NATK-33", ": > ~/.cla" + "ude/hoo$''ks/launch-level-guard.sh", TAMPER),
+    ("NATK-34-tmux", "tm\\\nux send-keys approved Enter", UNK),
+    ("NATK-34-orca", "or\\\nca terminal send --terminal t1 --text approved", UNK),
+    ("NATK-35", "if :; then gh alias set mm 'pr merge'; fi", UNK),
+    ("NATK-38", "uv run python -m superclaude.cli.main install", TAMPER),
+    # Design section 10, rows not yet in Task 16 (or restated as a Task 17 row).
+    (
+        "EDGE17-title-fs",
+        "gh pr create --repo o/r --base master --head f "
+        '--title "docs: explain git hooks" --body-file /tmp/b',
+        SUBMIT,
+    ),
+    (
+        "EDGE17-pr-body",
+        'gh pr create --repo o/r --title x --body "this pull request names git"',
+        MERGE,
+    ),
+    ("EDGE17-orca-continuation", "orca \\\nworktree list", ESCAPE),
+    ("EDGE17-scope", 'git commit -m "fix(ccsession): handle tags"', ESCAPE),
+    ("EDGE17-multibyte-big", "echo " + "é" * 32766, ("LL-BIG",) * 4),
+]
+assert len({row[0] for row in CORPUS17}) == len(CORPUS17), "duplicate corpus id"
+assert len({r[0]: r[1] for r in CORPUS17}["EDGE17-multibyte-big"].encode()) == 65537
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        pytest.param(command, level, msg_id, id=f"{row_id}-{level}")
+        for row_id, command, ids in CORPUS17
+        for level, msg_id in zip(LEVEL_ORDER, ids)
+    ],
+)
+def test_corpus17(tmp_path, command, level, msg_id):
+    # T-COR-1, Task 17 rows; LL-TEXT follows every Bash block.
+    _git_case(tmp_path, command, level, msg_id)
+
+
+PAYLOADS17 = [
+    ("OK-14", _edit("Edit", "/repo/src/superclaude/x.py"), NONE4),
+    # FR-L-51: contents are never checked, only the path.
+    (
+        "EDGE17-write-quote",
+        _edit("Write", "/repo/docs/notes.md", content="see ~/.cla" + "ude/hooks/x.sh"),
+        NONE4,
+    ),
+    (
+        "EDGE17-monitor-ws",
+        _tool("Monitor", ws={"url": "wss://example.test/feed"}, timeout_ms=5000),
+        NONE4,
+    ),
+]
+
+
+@pytest.mark.parametrize(
+    "payload, level, msg_id",
+    [
+        pytest.param(payload, level, msg_id, id=f"{row_id}-{level}")
+        for row_id, payload, ids in PAYLOADS17
+        for level, msg_id in zip(LEVEL_ORDER, ids)
+    ],
+)
+def test_corpus17_other_tools(tmp_path, payload, level, msg_id):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(payload, tmp_path)
+    _assert_decision(result, tmp_path, msg_id, level, text=_text_note(payload, msg_id))
+
+
+# T-MSG-1 to T-MSG-3: one oracle payload per message id, run through the real
+# script (the printer-only route is test_every_message_prints_the_design_text).
+MSG_CASES = {
+    "LL-IMPL": ("W", _skill("sc:implement")),
+    "LL-COMMIT": ("W", _bash("git commit -m x")),
+    "LL-PUSH": ("W", _bash("git push origin feature")),
+    "LL-PUSH-FORM": ("FS", _bash("git push --force origin f")),
+    "LL-PROTECTED": ("W", _bash("git push origin main")),
+    "LL-MERGE": ("W", _bash("gh pr merge 5")),
+    "LL-GH-WRITE": ("W", _bash("gh api graphql")),
+    "LL-SUBMIT": ("W", _skill("sc:pr-submit")),
+    "LL-REPO": ("FS", _bash("gh pr create --title x")),
+    "LL-UNKNOWN": ("W", _bash("git ci")),
+    "LL-MCP": ("W", _tool("mcp__github__push_files")),
+    "LL-ESCAPE": ("W", _tool("Workflow")),
+    "LL-TURN": ("W", _tool("CronCreate", prompt="approved")),
+    "LL-TAMPER": ("W", _edit("Edit", "~/.cla" + "ude/settings.json")),
+    "LL-SKILL": ("W", _skill("")),
+    "LL-BIG": ("W", _bash("echo " + "y" * 70_000)),
+    "LL-BROKEN": ("F", {"hook_event_name": "PostToolUse", "session_id": SID}),
+    # No record and no binding: the level is unknown, so the bare header.
+    "LL-NOBIND": (None, _prompt("Example: " + _marker() + " plan")),
+}
+assert sorted(MSG_CASES) == sorted(IDS), "message id without an oracle payload"
+
+
+def _msg_run(tmp_path, msg_id):
+    level, payload = MSG_CASES[msg_id]
+    if level is not None:
+        _bind(tmp_path, *LEVEL_FILES[level])
+    return level, payload, _run(payload, tmp_path)
+
+
+@pytest.mark.parametrize("msg_id", IDS)
+def test_every_message_has_header_and_three_lines(tmp_path, msg_id):
+    # T-MSG-1: header, then Blocked:, Why:, You can:, then only Note: lines.
+    level, _payload, result = _msg_run(tmp_path, msg_id)
+    assert result.returncode == 2 and result.stdout == b""
+    lines = result.stderr.decode().splitlines()
+    header = HEADER.format(level=LEVELS[level]) if level else "Launch-level guard:"
+    assert lines[0] == header
+    assert [line.split(" ", 2)[0] for line in lines[1:3]] == ["Blocked:", "Why:"]
+    assert lines[3].startswith("You can: ")
+    assert all(line.startswith("Note: ") for line in lines[4:])
+
+
+@pytest.mark.parametrize("msg_id", IDS)
+def test_every_message_id_reachable(tmp_path, msg_id):
+    # T-MSG-2: the payload produces exactly its id's design text.
+    level, payload, result = _msg_run(tmp_path, msg_id)
+    if level is None:
+        assert (result.returncode, result.stdout) == (2, b"")
+        assert result.stderr.decode() == _nobind(tmp_path)
+        return
+    text = payload.get("tool_name") in ("Bash", "Monitor")
+    _assert_decision(result, tmp_path, msg_id, level, text=text)
+
+
+@pytest.mark.parametrize("msg_id", IDS)
+def test_no_unresolved_template_variables(tmp_path, msg_id):
+    # T-MSG-3
+    _level, _payload, result = _msg_run(tmp_path, msg_id)
+    out = result.stderr.decode()
+    assert out and not re.search(r"\{(level|store|sid)\}", out)
+
+
+# T-MSG-4: competing classes in one call; the higher class names the message.
+PRECEDENCE = [
+    ("tamper-over-merge", "git merge x; cat ~/.cla" + "ude/settings.json", TAMPER),
+    ("merge-over-ghwrite", "gh api graphql; gh pr merge 5", MERGE),
+    ("submit-over-repo", "gh pr create --title x", SUBMIT_REPO),
+    ("push-over-pushform", "git push --force origin f", PUSHFORM),
+    ("protected-over-push", "git push origin main", PROTECTED),
+]
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        pytest.param(command, level, msg_id, id=f"MSG4-{case_id}-{level}")
+        for case_id, command, ids in PRECEDENCE
+        for level, msg_id in zip(LEVEL_ORDER, ids)
+    ],
+)
+def test_precedence_order(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+@pytest.mark.parametrize(
+    "level, rendering",
+    [
+        ("W", "worktree"),
+        ("WA", "worktree (approved)"),
+        ("F", "full"),
+        ("FS", "full --submit"),
+    ],
+)
+def test_level_rendered_in_header(tmp_path, level, rendering):
+    # T-MSG-5: the four renderings, typed here, through the real script.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_tool("mcp__github__merge_pull_request"), tmp_path)
+    assert result.returncode == 2
+    first = result.stderr.decode().splitlines()[0]
+    assert first == (
+        "Launch-level guard: this session was started by /sc:issue --claim"
+        f" at level {rendering}."
+    )
+
+
+@pytest.mark.parametrize(
+    "payload, msg_id",
+    [
+        pytest.param(_skill("sc:implement"), "LL-IMPL", id="skill"),
+        pytest.param(_bash("git commit -m x"), "LL-COMMIT", id="bash"),
+        pytest.param(_bash("gh pr merge 5", tool="Monitor"), "LL-MERGE", id="monitor"),
+        pytest.param(
+            _edit("Edit", "~/.cla" + "ude/hooks/x.sh"), "LL-TAMPER", id="edit"
+        ),
+        pytest.param(_tool("mcp__github__merge_pull_request"), "LL-MERGE", id="mcp"),
+        pytest.param(_tool("Agent", isolation="remote"), "LL-ESCAPE", id="agent"),
+        pytest.param(_bash("git status"), None, id="allowed-bash"),
+    ],
+)
+def test_state_and_text_notes(tmp_path, payload, msg_id):
+    # T-MSG-6: a degraded session gets LL-STATE on every block (first), LL-TEXT
+    # only on a Bash or Monitor block, and an allowed call stays silent.
+    _bind(tmp_path, "garbage")
+    result = _run(payload, tmp_path)
+    text = _text_note(payload, msg_id)
+    _assert_decision(result, tmp_path, msg_id, "W", note=msg_id is not None, text=text)
+
+
+@pytest.mark.parametrize("missing", ["tr", "sed"])
+def test_internal_error_prints_broken(tmp_path, missing):
+    # T-FC-3: PATH without tr, then without sed, governed Bash: LL-BROKEN.
+    bindir = tmp_path / "bin"
+    bindir.mkdir()
+    for tool in ("cat", "sed", "tr", "mkdir", "mv", "ln", "rm", "jq"):
+        if tool != missing:
+            (bindir / tool).symlink_to(shutil.which(tool))
+    _bind(tmp_path, "full")
+    result = _run(_bash("git status"), tmp_path)
+    assert result.returncode == 2 and result.stdout == b""
+    # bash's own "command not found" line comes first; the message is the rest.
+    store = str(_store(tmp_path / "home"))
+    expected = _expected("LL-BROKEN", "full", SID, store)
+    out = result.stderr.decode()
+    assert out.endswith("\n" + expected) and f"{missing}: command not found" in out
+
+
+# Design section 11 acceptance map: each AC lists the cases that must exist.
+# Ids are kept as (family, number) so this table never matches its own search.
+AC_MAP = {
+    "AC-1": [("GRID", 3), ("SKL", 1), ("APR", 5), ("APR", 9), ("NRM", 8), ("GIT", 18)],
+    "AC-2": [
+        ("GRID", 4),
+        ("GRID", 5),
+        ("GIT", 17),
+        ("PSH", 8),
+        ("PSH", 11),
+        ("GH", 12),
+    ],
+    "AC-3": [("APR", n) for n in (1, 2, 3, 4, 10)] + [("TRN", 1), ("TRN", 4)],
+    "AC-4": [("ISO", n) for n in (1, 4, 7, 8, 9)] + [("REG", 3)],
+    "AC-5": [("BIND", 2), ("BIND", 7), ("BIND", 13)]
+    + [("TAM", n) for n in (1, 2, 6)]
+    + [("FC", 2)],
+    "AC-6": [("PSH", 4), ("PSH", 12), ("GIT", 9), ("GIT", 14), ("NRM", 1)]
+    + [("GH", 2), ("GH", 11), ("GH", 14), ("MCP", 1), ("COR", 2)],
+    "AC-7": [("MSG", 1), ("MSG", 2), ("MSG", 3), ("FC", 3)],
+    "AC-8": [("GRID", 1), ("GRID", 2)]
+    + [("SPD", n) for n in range(1, 6)]
+    + [("COR", 1), ("GAP", 1)],
+}
+# T-REG-3 (the hooks.json matcher) is an unlabelled test in the registration
+# module; it is located by its function name instead of a label.
+AC_LOCATED = {
+    ("REG", 3): (
+        "test_launch_level_guard_registration.py",
+        "def test_matcher_matches_the_guarded_tools_and_not_the_others(",
+    ),
+}
+
+
+@pytest.mark.parametrize("ac", sorted(AC_MAP))
+def test_acceptance_map_cases_present(ac):
+    source = Path(__file__).read_text()
+    missing = []
+    for fam, n in AC_MAP[ac]:
+        if (fam, n) in AC_LOCATED:
+            name, needle = AC_LOCATED[(fam, n)]
+            if needle not in (Path(__file__).parent / name).read_text():
+                missing.append((fam, n))
+        elif not re.search(rf"T-{fam}-{n}(?!\d)", source):
+            missing.append((fam, n))
+    assert not missing, (ac, missing)

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
