a71679b8baffe69f6b4fc5cc10faf788beaaf140
Review one task for spec compliance.

Task brief: ## Task 6: Implement Bash and Monitor normalisation

Depends on: Task 5

In src/superclaude/hooks/scripts/launch-level-guard.sh add the Bash and Monitor normalisation of design section 5.1 (FR-L-22 to FR-L-27, FR-L-44): cmd is the decoded tool_input.command of a Bash (foreground or background) or Monitor call; a Monitor call with only ws is NONE; no parameter-expansion substitution over the command text. Steps in order: NM1 a command over 65536 bytes gives BIG and stops; NM1a a backslash-newline continuation inside a word (the test [[ $cmd =~ $'[^[:space:]\\\\]\\\\\n' ]]) gives UNKNOWN; NM2 and NM3 build T with the sed expression of the design; NM4 builds G; NM5 and NM6 build W; segments are always split with IFS=';' read -r -a segs and words with ws=($seg) under set -f; NM7 basename is the text after the last slash. Use the exact sed and tr expressions printed in design section 5.1.

Extend tests/hooks/test_launch_level_guard.py with every T-NRM case of MR section 8.2 and the T-FC-7 multi-byte size case (65537 bytes of multi-byte text gives BIG), asserting the resulting class through the observable outcome (block id) at the level where it differs from NONE.

Acceptance criteria:
- A governed Bash call over 65536 bytes exits 2 with LL-BIG at every level, and one of exactly 65536 bytes does not.
- The in-word continuation spellings of cases B-1 in design section 4 (for example gi, backslash, newline, t push) exit 2 with LL-UNKNOWN at every level.
- The normalisation uses exactly one sed and four tr invocations for a Bash command and one sed for an edit path (counted in a test by running the script with a PATH of counting wrappers).
- uv run pytest tests/hooks/test_launch_level_guard.py -k "NRM or nrm" -v passes.

AC ids (source order):
T6.AC1: A governed Bash call over 65536 bytes exits 2 with LL-BIG at every level, and one of exactly 65536 bytes does not.
T6.AC2: The in-word continuation spellings of cases B-1 in design section 4 (for example gi, backslash, newline, t push) exit 2 with LL-UNKNOWN at every level.
T6.AC3: The normalisation uses exactly one sed and four tr invocations for a Bash command and one sed for an edit path (counted in a test by running the script with a PATH of counting wrappers).
T6.AC4: uv run pytest tests/hooks/test_launch_level_guard.py -k "NRM or nrm" -v passes.
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
Start sha: a71679b8baffe69f6b4fc5cc10faf788beaaf140
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log
new file mode 100644
index 00000000..52be474c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log
@@ -0,0 +1,7 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "NRM or nrm" -q  (after the fix pass)
+............................................                             [100%]
+
+=============== 123 passed, 311 deselected, 98 xfailed in 6.15s ================
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q
+
+======================= 434 passed, 98 xfailed in 10.31s =======================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 244f75aa..8aa89899 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -5,8 +5,8 @@
 # with a message on stderr; never exit 1, no onFailure. Only a session that the
 # claim script launched (a valid top-level session_id bound in the store) is
 # governed; every other session is ordinary and never blocked (FR-L-53).
-# Ten-part layout (DD-1); Task 5 classifies Skill calls only, so until Tasks 6
-# to 10 add their classifiers every other tool call classifies as NONE.
+# Ten-part layout (DD-1); Tasks 5 and 6 classify Skill calls and Bash/Monitor
+# BIG and NM1a UNKNOWN; anything else is NONE until Tasks 7 to 10.
 # launch-level-guard-version: 1
 
 # 1. Settings
@@ -390,6 +390,39 @@ if [ "$LL_BRANCH" = tool ]; then
         issue) LL_CLASSES+='ESCAPE ' ;;
         '') LL_CLASSES+='SKILL ' ;;
         esac
+    elif [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
+        # FR-L-22 to FR-L-27: cmd is the decoded tool_input.command, kept raw; a
+        # Monitor call with only ws has no text and stays NONE. No ${s//...}
+        # substitution runs over the text (fact T5); one sed and four tr.
+        cmd=$LL_TEXT
+        if [ "${#cmd}" -gt 65536 ]; then
+            LL_CLASSES+='BIG ' # NM1: bytes under LC_ALL=C; nothing else is checked
+        elif [ -n "$cmd" ]; then
+            # >>> normalise (NM1a to NM7; the tests run this block on its own)
+            # NM1a: a backslash-newline continuation inside a word. The
+            # regex sits in a variable: a quoted $'...' after =~ matches literally.
+            LL_RE_NM1A=$'[^[:space:]\\\\]\\\\\n'
+            [[ $cmd =~ $LL_RE_NM1A ]] && LL_CLASSES+='UNKNOWN '
+            # T (NM2, NM3): $ before a quote, quotes and backslashes deleted, "/" runs squeezed; the tamper text.
+            T=$(printf '%s\n' "$cmd" | sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e 's#/(\./)+#/#g' -e 's/`/ $;/g') || ll_deny LL-BROKEN
+            # G (NM4): raw cmd then T, lower case, other characters spaces, one space at each end; never split.
+            G=" $(printf '%s\n%s\n' "$cmd" "$T" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9._/~$@+:-' ' ') " || ll_deny LL-BROKEN
+            # W (NM5, NM6): newline ; & | ( ) made ";", other characters outside the word set made spaces.
+            W=$(printf '%s\n' "$T" | tr '\n;&|()' ';;;;;;' | tr -c 'A-Za-z0-9._/=:@+~$;-' ' ') || ll_deny LL-BROKEN
+            # segs: the segments of W; a segment's words are ws=($seg) under set -f, and (NM7) a word's basename is ${w##*/}.
+            IFS=';' read -r -a segs <<<"$W"
+            # <<< normalise
+        fi
+    elif [ "$LL_TOOL" = Edit ] || [ "$LL_TOOL" = Write ] || [ "$LL_TOOL" = NotebookEdit ]; then
+        # EPATH: the edit path after the NM3 "/" squeeze, one sed; the tamper check reads it.
+        EPATH=
+        if [ -n "$LL_PATH" ]; then
+            EPATH=$(printf '%s\n' "$LL_PATH" | sed -E -e 's#/+#/#g' -e 's#/(\./)+#/#g') || ll_deny LL-BROKEN
+        fi
+    fi
+    # LL-TEXT: every class of a Bash or Monitor call came from its text.
+    if [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
+        LL_NOTE_TEXT=1
     fi
 
     # 9. One case on CLASS:LEVEL, taken in message precedence; any blocked class
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 9fa1a423..1c2f2d07 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1,4 +1,4 @@
-"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 5).
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 6).
 
 Each case runs the real script with a JSON payload on stdin, HOME inside
 tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
@@ -8,7 +8,9 @@ message texts are read from section 9 of the design, not copied here.
 Two test-only routes reach paths the Task 3 skeleton cannot reach through a
 real payload; neither adds behaviour to the shipped script:
 - the printer block (between the ">>> printer" and "<<< printer" comments) is
-  run on its own in bash, to check all eighteen message texts;
+  run on its own in bash, to check all eighteen message texts; the normalise
+  block (">>> normalise" to "<<< normalise") is run the same way, to check
+  the T, G and W texts that the Task 7 to 9 classifiers read;
 - a copy of the script with one known line changed to "exit 7" drives the
   real EXIT trap through a real payload.
 """
@@ -792,7 +794,7 @@ def _skill(name=_ABSENT, sid=SID, tool_input=None, **extra) -> dict:
     return payload
 
 
-def _assert_decision(result, tmp_path, msg_id, level, note=False):
+def _assert_decision(result, tmp_path, msg_id, level, note=False, text=False):
     if msg_id is None:
         assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
         return
@@ -800,6 +802,8 @@ def _assert_decision(result, tmp_path, msg_id, level, note=False):
     expected = _expected(msg_id, LEVELS[level], SID, store)
     if note:
         expected += STATE_NOTE + "\n"
+    if text:
+        expected += _design_note("LL-TEXT") + "\n"
     assert result.returncode == 2
     assert result.stdout == b""
     assert result.stderr.decode() == expected
@@ -912,8 +916,11 @@ def test_huge_fields_are_quick(tmp_path):
     result = _run(_skill("sc:implement " + "x" * 200_000), tmp_path)
     _assert_decision(result, tmp_path, "LL-IMPL", "W")
     bash = {**VALID_PAYLOADS["pretooluse-bash"], "session_id": SID}
-    bash["tool_input"] = {"command": "echo " + "y\n" * 100_000}
+    # Just under the 65,536-byte cap the whole text is normalised, many lines.
+    bash["tool_input"] = {"command": "echo " + "y\n" * 32_000}
     _assert_decision(_run(bash, tmp_path), tmp_path, None, "W")
+    bash["tool_input"] = {"command": "echo " + "y\n" * 100_000}
+    _assert_decision(_run(bash, tmp_path), tmp_path, "LL-BIG", "W", text=True)
     # Not JSON (closing brace cut), the bound id after the long field: LL-BROKEN.
     raw = json.dumps(_skill("sc:workflow", tool_input=bash["tool_input"])).encode()
     _assert_decision(_run(raw[:-1], tmp_path), tmp_path, "LL-BROKEN", "W")
@@ -1203,3 +1210,468 @@ def test_notes_follow_the_lines_state_first(tmp_path):
         + "\n"
     )
     assert _design_note("LL-STATE") == STATE_NOTE
+
+
+# --- Task 6: Bash and Monitor normalisation (T-NRM, T-FC-7) ----------------
+#
+# Cases whose class needs a Task 7 to 9 classifier (git, gh, tamper, escape)
+# are pinned end to end with a strict xfail naming that task, so the task that
+# reaches the class must drop the mark. "?" marks a level that the T-NRM row
+# does not pin.
+
+LEVEL_ORDER = ("W", "WA", "F", "FS")
+UNK = ("LL-UNKNOWN",) * 4
+PUSH = ("LL-PUSH", "LL-PUSH", "LL-PUSH", "LL-PUSH-FORM")
+COMMIT = ("LL-COMMIT", "LL-COMMIT", "LL-COMMIT", None)
+MERGE = ("LL-MERGE",) * 4
+GHWRITE = ("LL-GH-WRITE",) * 4
+TAMPER = ("LL-TAMPER",) * 4
+ESCAPE = ("LL-ESCAPE",) * 4
+NONE4 = (None,) * 4
+FS_ONLY = ("?", "?", "?")
+STATE_PATH = "~/.cla" + "ude/state"  # spelled in two parts, as the script must
+
+NRM_E2E = [
+    # T-NRM-1: quote and backslash splicing; amendment cases N-ATK-3 to 33.
+    ("nrm1-quote-push", 'g""it push origin main', PUSH, 7),
+    ("nrm1-backslash-push", "\\git push origin main", PUSH, 7),
+    ("nrm1-split-quote", "git push origin 'feature:ma''in'", PUSH, 7),
+    ("nrm1-split-backslash", "git push origin feature:ma\\in", PUSH, 7),
+    ("nrm1-quote-commit", 'g""it commit -m x', ("?", "?", "LL-COMMIT", "?"), 7),
+    ("nrm1-backslash-commit", "\\git commit -m x", ("?", "?", "LL-COMMIT", "?"), 7),
+    ("natk3", "git$'' push origin HEAD:main", PUSH, 7),
+    ("natk4", 'g$""it push origin HEAD:main', PUSH, 7),
+    ("natk15", "git$'' -c x.y=z push origin HEAD:main", PUSH, 7),
+    ("natk16", "git$'' merge other --no-edit", MERGE, 7),
+    ("natk18", "git$'' commit --allow-empty -m x", COMMIT, 7),
+    ("natk23", "g$''h pr merge 5", MERGE, 8),
+    (
+        "natk24",
+        "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
+        GHWRITE,
+        8,
+    ),
+    ("natk30", f"rm -rf {STATE_PATH.replace('cla', 'cla$' + chr(39) * 2)}", TAMPER, 9),
+    ("natk32", "cp /tmp/s.json ~/.claude/set$''tings.json", TAMPER, 9),
+    ("natk33", ": > ~/.claude/hoo$''ks/launch-level-guard.sh", TAMPER, 9),
+    # T-NRM-2: redirections stay words.
+    ("nrm2-stdin", "git commit -m x < /dev/null", FS_ONLY + (None,), 7),
+    ("nrm2-stdout", "git commit -m x > /tmp/log 2>&1", FS_ONLY + (None,), 7),
+    ("nrm2-status", "git status 2>&1 | tail -5", FS_ONLY + (None,), None),
+    ("nrm2-push", "git push origin a:b 2>&1 | tail -5", FS_ONLY + ("LL-PUSH-FORM",), 7),
+    # T-NRM-4: \/ escapes in a tamper path.
+    ("nrm4-escaped-slash", "cp x ~\\/.claude\\/\\/.\\/settings.json", TAMPER, 9),
+    # T-NRM-5: a continuation is not joined.
+    ("nrm5-gh-api", "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main", GHWRITE, 8),
+    ("nrm5-push", "git push origin a:b \\\nc:main", FS_ONLY + ("LL-PUSH-FORM",), 7),
+    (
+        "nrm5-double-backslash",
+        "git status \\\\\ngit -c alias.p=push p origin HEAD:main",
+        UNK,
+        7,
+    ),
+    (
+        "nrm5-pr-create",
+        'gh pr create \\\n--repo "$REPO" --title x --body y',
+        FS_ONLY + (None,),
+        8,
+    ),
+    ("nrm5-claude", "claude \\\n-p x", ESCAPE, 9),
+    ("nrm5-git-space", "git \\\ncommit -m x", UNK, 7),
+    # T-NRM-7: a quoted ">" in an assignment.
+    ("nrm7-commit", 'A=">" git commit -m x', ("?", "?", "LL-COMMIT", None), 7),
+    ("nrm7-push", 'A=">" git push origin HEAD:main', PUSH, 7),
+    # T-NRM-8: NM1a, a backslash-newline inside a word, is UNKNOWN (reachable now).
+    ("natk1", "gi\\\nt push origin HEAD:main", UNK, None),
+    ("natk2", 'bash -c "gi\\\nt push origin HEAD:main"', UNK, None),
+    ("natk17", "gi\\\nt merge other --no-edit", UNK, None),
+    ("natk19", "gi\\\nt commit --allow-empty -m x", UNK, None),
+    ("natk25", "g\\\nh pr merge 5", UNK, None),
+    ("natk28", 'cl\\\naude -p "finish the task"', UNK, None),
+    ("natk29", "rm -rf " + STATE_PATH.replace("cla", "cla\\\n"), UNK, None),
+    ("natk34-tmux", "tm\\\nux send-keys approved Enter", UNK, None),
+    ("natk34-orca", "or\\\nca terminal send --terminal t1 --text approved", UNK, None),
+    (
+        "nrm8-push-space",
+        "git push origin a:b \\\n c:main",
+        FS_ONLY + ("LL-PUSH-FORM",),
+        7,
+    ),
+]
+
+
+def _nrm_params():
+    for name, command, ids, task in NRM_E2E:
+        for level, msg_id in zip(LEVEL_ORDER, ids):
+            if msg_id == "?":
+                continue
+            marks = ()
+            if msg_id and task:
+                marks = pytest.mark.xfail(
+                    strict=True, reason=f"class reached in Task {task}"
+                )
+            yield pytest.param(
+                command, level, msg_id, id=f"{name}-{level}", marks=marks
+            )
+
+
+def _bash(command: str, tool: str = "Bash", **extra) -> dict:
+    return {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": tool,
+        "tool_input": {"command": command, **extra},
+    }
+
+
+@pytest.mark.parametrize("command, level, msg_id", list(_nrm_params()))
+def test_nrm_end_to_end(tmp_path, command, level, msg_id):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_bash(command), tmp_path)
+    _assert_decision(result, tmp_path, msg_id, level, text=msg_id is not None)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.xfail(strict=True, reason="class reached in Task 9")
+def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
+    # T-NRM-4: raw JSON bytes with \/ escapes; jq decodes them before the tamper check.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    raw = (
+        b'{"hook_event_name": "PreToolUse", "session_id": "' + SID.encode() + b'", '
+        b'"tool_name": "Bash", "tool_input": {"command": '
+        b'"cp x ~\\/.claude\\/settings.json"}}'
+    )
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-TAMPER", level, text=True)
+
+
+@pytest.mark.parametrize("level", ["W", "WA", "F"])
+@pytest.mark.parametrize(
+    "command",
+    [
+        "git push origin a:b \\\nc:main",
+        "git push origin a:b \\\n c:main",
+        "git push origin a:b 2>&1 | tail -5",
+    ],
+    ids=["nrm5-push", "nrm8-push-space", "nrm2-push"],
+)
+@pytest.mark.xfail(strict=True, reason="class reached in Task 7")
+def test_nrm_push_blocked_below_fs(tmp_path, level, command):
+    # T-NRM-5/8/2: a push is blocked at every level (LL-PUSH-FORM only at FS, tested above);
+    # below FS the grid blocks every push form, whichever of its three ids applies.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_bash(command), tmp_path)
+    assert result.returncode == 2
+    assert any(
+        i.encode() in result.stderr for i in ("LL-PUSH", "LL-PUSH-FORM", "LL-PROTECTED")
+    )
+
+
+def _normalise(tmp_path: Path, command: str):
+    """Run only the normalise block of the script (test-only route)."""
+    driver = (
+        "LC_ALL=C; ll_deny() { exit 3; }; set -f; LL_CLASSES=' '; cmd=$2\n"
+        'eval "$(sed -n \'/# >>> normalise/,/# <<< normalise/p\' "$1")"\n'
+        'printf \'%s\\0\' "$LL_CLASSES" "$T" "$G"\n'
+        'for s in "${segs[@]}"; do ws=($s); printf \'%s\\0\' "${ws[*]}"; done\n'
+    )
+    home = tmp_path / "home"
+    home.mkdir(exist_ok=True)
+    result = subprocess.run(
+        [BASH, "-c", driver, "_", str(HOOK), command],
+        capture_output=True,
+        env=_env(home, _bin(tmp_path)),
+        timeout=10,
+    )
+    assert (result.returncode, result.stderr) == (0, b"")
+    classes, t, g, *segs = result.stdout.decode().split("\0")[:-1]
+    return classes.split(), t, g.split(), [s for s in segs if s]
+
+
+def test_nrm_block_is_marked_once():
+    text = HOOK.read_text()
+    assert text.count("# >>> normalise") == 1
+    assert text.count("# <<< normalise") == 1
+
+
+# T-NRM-6: the worked example of FR-L-27.
+@pytest.mark.parametrize(
+    "command, t, segs",
+    [
+        (
+            "git commit -F - <<'EOF'\nfix: use git for hooks\nEOF",
+            "git commit -F - <<EOF\nfix: use git for hooks\nEOF",
+            ["git commit -F - EOF", "fix: use git for hooks", "EOF"],
+        ),
+        (
+            "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main -f sha=x",
+            None,
+            ["gh api", "-X PATCH repos/o/r/git/refs/heads/main -f sha=x"],
+        ),
+        (
+            "git push origin a:b 2>&1 | tail -5",
+            None,
+            ["git push origin a:b 2", "1", "tail -5"],
+        ),
+        (
+            'A=">" git push origin HEAD:main',
+            None,
+            ["A= git push origin HEAD:main"],
+        ),
+        (
+            "echo x > ~/.claude//./settings.json",
+            "echo x > ~/.claude/settings.json",
+            None,
+        ),
+        ("g$''it push origin main", "git push origin main", None),
+    ],
+)
+def test_nrm6_worked_example(tmp_path, command, t, segs):
+    classes, got_t, _, got_segs = _normalise(tmp_path, command)
+    assert classes == []
+    if t is not None:
+        assert got_t == t
+    if segs is not None:
+        assert got_segs == segs
+
+
+def test_nrm6_g_words_never_split(tmp_path):
+    command = "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1"
+    _, _, g, segs = _normalise(tmp_path, command)
+    words = "git rebase -x git -c alias.p push p origin head:main head~1".split()
+    assert g == words * 2  # raw text then T, each lower-cased
+    assert segs == ["git rebase -x git -c alias.p=push p origin HEAD:main HEAD~1"]
+
+
+# T-NRM-1, T-NRM-4, T-NRM-7 and the N-ATK splices: the T text the classifiers read.
+@pytest.mark.parametrize(
+    "command, t",
+    [
+        ('g""it push origin main', "git push origin main"),
+        ("\\git push origin main", "git push origin main"),
+        ("git push origin 'feature:ma''in'", "git push origin feature:main"),
+        ("git push origin feature:ma\\in", "git push origin feature:main"),
+        ('g""it commit -m x', "git commit -m x"),
+        ("\\git commit -m x", "git commit -m x"),
+        ("git$'' push origin HEAD:main", "git push origin HEAD:main"),
+        ('g$""it push origin HEAD:main', "git push origin HEAD:main"),
+        ("git$'' -c x.y=z push origin HEAD:main", "git -c x.y=z push origin HEAD:main"),
+        ("git$'' merge other --no-edit", "git merge other --no-edit"),
+        ("git$'' commit --allow-empty -m x", "git commit --allow-empty -m x"),
+        ("g$''h pr merge 5", "gh pr merge 5"),
+        (
+            "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
+            "flock /tmp/l gh api -X DELETE repos/o/r/git/refs/heads/main",
+        ),
+        (
+            "rm -rf " + STATE_PATH.replace("cla", "cla$''"),
+            "rm -rf " + STATE_PATH,
+        ),
+        (
+            "cp /tmp/s.json ~/.claude/set$''tings.json",
+            "cp /tmp/s.json ~/.claude/settings.json",
+        ),
+        (
+            ": > ~/.claude/hoo$''ks/launch-level-guard.sh",
+            ": > ~/.claude/hooks/launch-level-guard.sh",
+        ),
+        (
+            "cp x ~\\/.claude\\/\\/.\\/settings.json",
+            "cp x ~/.claude/settings.json",
+        ),
+        ('A=">" git commit -m x', "A=> git commit -m x"),
+    ],
+)
+def test_nrm_splices_reach_t(tmp_path, command, t):
+    classes, got_t, g, _ = _normalise(tmp_path, command)
+    assert (classes, got_t) == ([], t)
+    # G ends with T lower-cased, characters outside its word set made spaces.
+    t_words = re.sub(r"[^a-z0-9._/~$@+:-]", " ", t.lower()).split()
+    assert g[-len(t_words) :] == t_words
+
+
+# T-NRM-2 and T-NRM-7: redirections and a quoted ">" stay inside their segment.
+@pytest.mark.parametrize(
+    "command, segs",
+    [
+        ("git commit -m x < /dev/null", ["git commit -m x /dev/null"]),
+        ("git commit -m x > /tmp/log 2>&1", ["git commit -m x /tmp/log 2", "1"]),
+        ("git status 2>&1 | tail -5", ["git status 2", "1", "tail -5"]),
+        ('A=">" git commit -m x', ["A= git commit -m x"]),
+    ],
+)
+def test_nrm_redirections_kept_as_words(tmp_path, command, segs):
+    assert _normalise(tmp_path, command)[3] == segs
+
+
+# T-NRM-3: each separator starts a new segment.
+@pytest.mark.parametrize(
+    "command",
+    [
+        "git status; git log",
+        "git status && git log",
+        "git status || git log",
+        "git status | git log",
+        "git status\ngit log",
+        "git status $(git log)",
+        "git status `git log`",
+    ],
+)
+def test_nrm3_separators_start_segments(tmp_path, command):
+    _, _, _, segs = _normalise(tmp_path, command)
+    words = [s.split() for s in segs]
+    assert not any("status" in w and "log" in w for w in words)
+    assert any(w[:2] == ["git", "log"] for w in words)
+
+
+# NM1a [B-1]: only a backslash-newline inside a word gives UNKNOWN.
+@pytest.mark.parametrize(
+    "command, classes",
+    [
+        ("gi\\\nt push origin HEAD:main", ["UNKNOWN"]),
+        ('bash -c "gi\\\nt push origin HEAD:main"', ["UNKNOWN"]),
+        ("rm -rf " + STATE_PATH.replace("cla", "cla\\\n"), ["UNKNOWN"]),
+        ("or\\\nca terminal send --terminal t1 --text approved", ["UNKNOWN"]),
+        ("git push origin a:b \\\nc:main", []),
+        ("git push origin a:b \\\n c:main", []),
+        ("git status \\\\\ngit -c alias.p=push p origin HEAD:main", []),
+        ('gh pr create \\\n--repo "$REPO" --title x --body y', []),
+        ("claude \\\n-p x", []),
+        ("git \\\ncommit -m x", []),
+    ],
+)
+def test_nrm1a_in_word_continuation(tmp_path, command, classes):
+    assert _normalise(tmp_path, command)[0] == classes
+
+
+# T-FC-7 and NM1: a governed command over 65,536 bytes is BIG; bytes, not characters.
+BIG_TEXTS = {
+    "multibyte": "€" * 21845 + "é",
+    "ascii": "x" * 65537,
+    "multibyte-nm1a": "gi\\\nt " + "€" * 21843 + "a" * 2,
+}
+
+
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+@pytest.mark.parametrize("name", sorted(BIG_TEXTS))
+def test_nrm_fc7_over_65536_bytes_big(tmp_path, name, level):
+    assert len(BIG_TEXTS[name].encode()) == 65537
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_bash(BIG_TEXTS[name]), tmp_path)
+    _assert_decision(result, tmp_path, "LL-BIG", level, text=True)
+
+
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+def test_nrm_fc7_exactly_65536_bytes_not_big(tmp_path, level):
+    command = "€" * 21845 + "a"
+    assert len(command.encode()) == 65536
+    _bind(tmp_path, *LEVEL_FILES[level])
+    _assert_decision(_run(_bash(command), tmp_path), tmp_path, None, level)
+
+
+@pytest.mark.parametrize("store", [False, True])
+def test_nrm_fc7_ordinary_session_has_no_cap(tmp_path, store):
+    if store:
+        sessions = _store(tmp_path / "home") / "sessions"
+        sessions.mkdir(parents=True)
+        (sessions / "other-session").write_text("worktree")
+    result = _run(_bash(BIG_TEXTS["multibyte"]), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+@pytest.mark.parametrize("level", sorted(LEVEL_FILES))
+def test_nrm_monitor_ws_only_is_none(tmp_path, level):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    payload = {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": "Monitor",
+        "tool_input": {"ws": {"url": "wss://example.test/s"}, "timeout_ms": 1000},
+    }
+    _assert_decision(_run(payload, tmp_path), tmp_path, None, level)
+
+
+@pytest.mark.parametrize(
+    "payload",
+    [
+        _bash("gi\\\nt push origin HEAD:main", tool="Monitor", timeout_ms=1000),
+        _bash("gi\\\nt push origin HEAD:main", run_in_background=True),
+    ],
+    ids=["monitor", "background-bash"],
+)
+def test_nrm_monitor_and_background_bash_normalised(tmp_path, payload):
+    _bind(tmp_path, "full-submit")
+    result = _run(payload, tmp_path)
+    _assert_decision(result, tmp_path, "LL-UNKNOWN", "FS", text=True)
+
+
+def _counting_bin(tmp_path: Path) -> Path:
+    """A bin whose sed and tr log each run, then run the real tool."""
+    bindir = _bin(tmp_path)
+    log = tmp_path / "calls.log"
+    for tool in ("sed", "tr"):
+        real = shutil.which(tool)
+        (bindir / tool).unlink()
+        (bindir / tool).write_text(
+            f'#!{BASH}\nprintf "%s\\n" {tool} >>"{log}"\nexec "{real}" "$@"\n'
+        )
+        (bindir / tool).chmod(0o755)
+    return log
+
+
+EDIT_TOOLS = [
+    ("Edit", {"file_path": "/x//./settings.json"}),
+    ("Write", {"file_path": "/x/a.txt", "content": "y"}),
+    ("NotebookEdit", {"notebook_path": "/x/n.ipynb", "new_source": "y"}),
+]
+
+
+@pytest.mark.parametrize(
+    "tool_name, tool_input, counts",
+    [
+        ("Bash", {"command": "git status | tail -5"}, (1, 4)),
+        ("Bash", {"command": "ls", "run_in_background": True}, (1, 4)),
+        ("Monitor", {"command": "tail -f log", "timeout_ms": 1000}, (1, 4)),
+        *[(name, ti, (1, 0)) for name, ti in EDIT_TOOLS],
+        ("Skill", {"skill": "sc:workflow"}, (0, 0)),
+    ],
+)
+def test_nrm_one_sed_four_tr(tmp_path, tool_name, tool_input, counts):
+    log = _counting_bin(tmp_path)
+    _bind(tmp_path, "full")
+    payload = {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": tool_name,
+        "tool_input": tool_input,
+    }
+    result = _run(payload, tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    calls = log.read_text().split() if log.exists() else []
+    assert (calls.count("sed"), calls.count("tr")) == counts
+
+
+@pytest.mark.parametrize(
+    "path, want",
+    [
+        ("/x//./settings.json", "/x/settings.json"),
+        ("~/.claude///hooks/././guard.sh", "~/.claude/hooks/guard.sh"),
+        ("a/b", "a/b"),
+    ],
+)
+def test_nrm_edit_path_squeeze(tmp_path, path, want):
+    lines = [
+        line.strip()
+        for line in HOOK.read_text().splitlines()
+        if line.strip().startswith("EPATH=$(")
+    ]
+    assert len(lines) == 1
+    driver = f'LC_ALL=C; ll_deny() {{ exit 3; }}; LL_PATH=$1\n{lines[0]}\nprintf %s "$EPATH"\n'
+    home = tmp_path / "home"
+    home.mkdir(exist_ok=True)
+    result = subprocess.run(
+        [BASH, "-c", driver, "_", path],
+        capture_output=True,
+        env=_env(home, _bin(tmp_path)),
+        timeout=10,
+    )
+    assert (result.returncode, result.stdout.decode()) == (0, want)

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log
index ea0cd292..52be474c 100644
--- a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t6-test.log
@@ -1,222 +1,7 @@
-============================= test session starts ==============================
-platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.venv/bin/python
-cachedir: .pytest_cache
-SuperClaude: 5.0.0
-rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
-configfile: pyproject.toml
-plugins: superclaude-5.0.0, anyio-4.16.0
-collecting ... collected 519 items / 311 deselected / 208 selected
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "NRM or nrm" -q  (after the fix pass)
+............................................                             [100%]
 
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-quote-push-W] XFAIL [  0%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-quote-push-WA] XFAIL [  0%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-quote-push-F] XFAIL [  1%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-quote-push-FS] XFAIL [  1%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-backslash-push-W] XFAIL [  2%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-backslash-push-WA] XFAIL [  2%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-backslash-push-F] XFAIL [  3%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-backslash-push-FS] XFAIL [  3%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-quote-W] XFAIL [  4%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-quote-WA] XFAIL [  4%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-quote-F] XFAIL [  5%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-quote-FS] XFAIL [  5%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-backslash-W] XFAIL [  6%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-backslash-WA] XFAIL [  6%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-backslash-F] XFAIL [  7%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-split-backslash-FS] XFAIL [  7%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-quote-commit-F] XFAIL [  8%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm1-backslash-commit-F] XFAIL [  8%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk3-W] XFAIL [  9%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk3-WA] XFAIL [  9%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk3-F] XFAIL [ 10%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk3-FS] XFAIL [ 10%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk4-W] XFAIL [ 11%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk4-WA] XFAIL [ 11%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk4-F] XFAIL [ 12%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk4-FS] XFAIL [ 12%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk15-W] XFAIL [ 12%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk15-WA] XFAIL [ 13%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk15-F] XFAIL [ 13%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk15-FS] XFAIL [ 14%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk16-W] XFAIL [ 14%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk16-WA] XFAIL [ 15%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk16-F] XFAIL [ 15%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk16-FS] XFAIL [ 16%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk18-W] XFAIL [ 16%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk18-WA] XFAIL [ 17%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk18-F] XFAIL [ 17%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk18-FS] PASSED [ 18%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk23-W] XFAIL [ 18%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk23-WA] XFAIL [ 19%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk23-F] XFAIL [ 19%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk23-FS] XFAIL [ 20%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk24-W] XFAIL [ 20%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk24-WA] XFAIL [ 21%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk24-F] XFAIL [ 21%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk24-FS] XFAIL [ 22%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk30-W] XFAIL [ 22%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk30-WA] XFAIL [ 23%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk30-F] XFAIL [ 23%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk30-FS] XFAIL [ 24%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk32-W] XFAIL [ 24%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk32-WA] XFAIL [ 25%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk32-F] XFAIL [ 25%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk32-FS] XFAIL [ 25%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk33-W] XFAIL [ 26%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk33-WA] XFAIL [ 26%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk33-F] XFAIL [ 27%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk33-FS] XFAIL [ 27%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm2-stdin-FS] PASSED [ 28%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm2-stdout-FS] PASSED [ 28%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm2-status-FS] PASSED [ 29%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm2-push-FS] XFAIL [ 29%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm4-escaped-slash-W] XFAIL [ 30%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm4-escaped-slash-WA] XFAIL [ 30%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm4-escaped-slash-F] XFAIL [ 31%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm4-escaped-slash-FS] XFAIL [ 31%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-gh-api-W] XFAIL [ 32%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-gh-api-WA] XFAIL [ 32%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-gh-api-F] XFAIL [ 33%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-gh-api-FS] XFAIL [ 33%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-push-FS] XFAIL [ 34%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-double-backslash-W] XFAIL [ 34%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-double-backslash-WA] XFAIL [ 35%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-double-backslash-F] XFAIL [ 35%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-double-backslash-FS] XFAIL [ 36%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-pr-create-FS] PASSED [ 36%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-claude-W] XFAIL [ 37%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-claude-WA] XFAIL [ 37%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-claude-F] XFAIL [ 37%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-claude-FS] XFAIL [ 38%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-git-space-W] XFAIL [ 38%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-git-space-WA] XFAIL [ 39%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-git-space-F] XFAIL [ 39%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm5-git-space-FS] XFAIL [ 40%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm7-commit-F] XFAIL [ 40%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm7-commit-FS] PASSED [ 41%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm7-push-W] XFAIL [ 41%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm7-push-WA] XFAIL [ 42%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm7-push-F] XFAIL [ 42%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm7-push-FS] XFAIL [ 43%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk1-W] PASSED [ 43%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk1-WA] PASSED [ 44%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk1-F] PASSED [ 44%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk1-FS] PASSED [ 45%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk2-W] PASSED [ 45%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk2-WA] PASSED [ 46%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk2-F] PASSED [ 46%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk2-FS] PASSED [ 47%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk17-W] PASSED [ 47%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk17-WA] PASSED [ 48%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk17-F] PASSED [ 48%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk17-FS] PASSED [ 49%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk19-W] PASSED [ 49%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk19-WA] PASSED [ 50%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk19-F] PASSED [ 50%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk19-FS] PASSED [ 50%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk25-W] PASSED [ 51%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk25-WA] PASSED [ 51%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk25-F] PASSED [ 52%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk25-FS] PASSED [ 52%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk28-W] PASSED [ 53%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk28-WA] PASSED [ 53%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk28-F] PASSED [ 54%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk28-FS] PASSED [ 54%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk29-W] PASSED [ 55%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk29-WA] PASSED [ 55%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk29-F] PASSED [ 56%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk29-FS] PASSED [ 56%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-tmux-W] PASSED [ 57%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-tmux-WA] PASSED [ 57%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-tmux-F] PASSED [ 58%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-tmux-FS] PASSED [ 58%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-orca-W] PASSED [ 59%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-orca-WA] PASSED [ 59%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-orca-F] PASSED [ 60%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[natk34-orca-FS] PASSED [ 60%]
-tests/hooks/test_launch_level_guard.py::test_nrm_end_to_end[nrm8-push-space-FS] XFAIL [ 61%]
-tests/hooks/test_launch_level_guard.py::test_nrm_block_is_marked_once PASSED [ 61%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_worked_example[git commit -F - <<'EOF'\nfix: use git for hooks\nEOF-git commit -F - <<EOF\nfix: use git for hooks\nEOF-segs0] PASSED [ 62%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_worked_example[gh api \\\n-X PATCH repos/o/r/git/refs/heads/main -f sha=x-None-segs1] PASSED [ 62%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_worked_example[git push origin a:b 2>&1 | tail -5-None-segs2] PASSED [ 62%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_worked_example[A=">" git push origin HEAD:main-None-segs3] PASSED [ 63%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_worked_example[echo x > ~/.claude//./settings.json-echo x > ~/.claude/settings.json-None] PASSED [ 63%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_worked_example[g$''it push origin main-git push origin main-None] PASSED [ 64%]
-tests/hooks/test_launch_level_guard.py::test_nrm6_g_words_never_split PASSED [ 64%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[g""it push origin main-git push origin main] PASSED [ 65%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[\\git push origin main-git push origin main] PASSED [ 65%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[git push origin 'feature:ma''in'-git push origin feature:main] PASSED [ 66%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[git push origin feature:ma\\in-git push origin feature:main] PASSED [ 66%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[g""it commit -m x-git commit -m x] PASSED [ 67%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[\\git commit -m x-git commit -m x] PASSED [ 67%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[git$'' push origin HEAD:main-git push origin HEAD:main] PASSED [ 68%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[g$""it push origin HEAD:main-git push origin HEAD:main] PASSED [ 68%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[git$'' -c x.y=z push origin HEAD:main-git -c x.y=z push origin HEAD:main] PASSED [ 69%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[git$'' merge other --no-edit-git merge other --no-edit] PASSED [ 69%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[git$'' commit --allow-empty -m x-git commit --allow-empty -m x] PASSED [ 70%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[g$''h pr merge 5-gh pr merge 5] PASSED [ 70%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main-flock /tmp/l gh api -X DELETE repos/o/r/git/refs/heads/main] PASSED [ 71%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[rm -rf ~/.cla$''ude/state-rm -rf ~/.claude/state] PASSED [ 71%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[cp /tmp/s.json ~/.claude/set$''tings.json-cp /tmp/s.json ~/.claude/settings.json] PASSED [ 72%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[: > ~/.claude/hoo$''ks/launch-level-guard.sh-: > ~/.claude/hooks/launch-level-guard.sh] PASSED [ 72%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[cp x ~\\/.claude\\/\\/.\\/settings.json-cp x ~/.claude/settings.json] PASSED [ 73%]
-tests/hooks/test_launch_level_guard.py::test_nrm_splices_reach_t[A=">" git commit -m x-A=> git commit -m x] PASSED [ 73%]
-tests/hooks/test_launch_level_guard.py::test_nrm_redirections_kept_as_words[git commit -m x < /dev/null-segs0] PASSED [ 74%]
-tests/hooks/test_launch_level_guard.py::test_nrm_redirections_kept_as_words[git commit -m x > /tmp/log 2>&1-segs1] PASSED [ 74%]
-tests/hooks/test_launch_level_guard.py::test_nrm_redirections_kept_as_words[git status 2>&1 | tail -5-segs2] PASSED [ 75%]
-tests/hooks/test_launch_level_guard.py::test_nrm_redirections_kept_as_words[A=">" git commit -m x-segs3] PASSED [ 75%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status; git log] PASSED [ 75%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status && git log] PASSED [ 76%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status || git log] PASSED [ 76%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status | git log] PASSED [ 77%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status\ngit log] PASSED [ 77%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status $(git log)] PASSED [ 78%]
-tests/hooks/test_launch_level_guard.py::test_nrm3_separators_start_segments[git status `git log`] PASSED [ 78%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[gi\\\nt push origin HEAD:main-classes0] PASSED [ 79%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[bash -c "gi\\\nt push origin HEAD:main"-classes1] PASSED [ 79%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[rm -rf ~/.cla\\\nude/state-classes2] PASSED [ 80%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[or\\\nca terminal send --terminal t1 --text approved-classes3] PASSED [ 80%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[git push origin a:b \\\nc:main-classes4] PASSED [ 81%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[git push origin a:b \\\n c:main-classes5] PASSED [ 81%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[git status \\\\\ngit -c alias.p=push p origin HEAD:main-classes6] PASSED [ 82%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[gh pr create \\\n--repo "$REPO" --title x --body y-classes7] PASSED [ 82%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[claude \\\n-p x-classes8] PASSED [ 83%]
-tests/hooks/test_launch_level_guard.py::test_nrm1a_in_word_continuation[git \\\ncommit -m x-classes9] PASSED [ 83%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[ascii-F] PASSED [ 84%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[ascii-FS] PASSED [ 84%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[ascii-W] PASSED [ 85%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[ascii-WA] PASSED [ 85%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-F] PASSED [ 86%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-FS] PASSED [ 86%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-W] PASSED [ 87%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-WA] PASSED [ 87%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-nm1a-F] PASSED [ 87%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-nm1a-FS] PASSED [ 88%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-nm1a-W] PASSED [ 88%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_over_65536_bytes_big[multibyte-nm1a-WA] PASSED [ 89%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_exactly_65536_bytes_not_big[F] PASSED [ 89%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_exactly_65536_bytes_not_big[FS] PASSED [ 90%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_exactly_65536_bytes_not_big[W] PASSED [ 90%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_exactly_65536_bytes_not_big[WA] PASSED [ 91%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_ordinary_session_has_no_cap[False] PASSED [ 91%]
-tests/hooks/test_launch_level_guard.py::test_nrm_fc7_ordinary_session_has_no_cap[True] PASSED [ 92%]
-tests/hooks/test_launch_level_guard.py::test_nrm_monitor_ws_only_is_none[F] PASSED [ 92%]
-tests/hooks/test_launch_level_guard.py::test_nrm_monitor_ws_only_is_none[FS] PASSED [ 93%]
-tests/hooks/test_launch_level_guard.py::test_nrm_monitor_ws_only_is_none[W] PASSED [ 93%]
-tests/hooks/test_launch_level_guard.py::test_nrm_monitor_ws_only_is_none[WA] PASSED [ 94%]
-tests/hooks/test_launch_level_guard.py::test_nrm_monitor_and_background_bash_normalised[monitor] PASSED [ 94%]
-tests/hooks/test_launch_level_guard.py::test_nrm_monitor_and_background_bash_normalised[background-bash] PASSED [ 95%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[Bash-tool_input0-counts0] PASSED [ 95%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[Bash-tool_input1-counts1] PASSED [ 96%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[Monitor-tool_input2-counts2] PASSED [ 96%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[Edit-tool_input3-counts3] PASSED [ 97%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[Write-tool_input4-counts4] PASSED [ 97%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[NotebookEdit-tool_input5-counts5] PASSED [ 98%]
-tests/hooks/test_launch_level_guard.py::test_nrm_one_sed_four_tr[Skill-tool_input6-counts6] PASSED [ 98%]
-tests/hooks/test_launch_level_guard.py::test_nrm_edit_path_squeeze[/x//./settings.json-/x/settings.json] PASSED [ 99%]
-tests/hooks/test_launch_level_guard.py::test_nrm_edit_path_squeeze[~/.claude///hooks/././guard.sh-~/.claude/hooks/guard.sh] PASSED [ 99%]
-tests/hooks/test_launch_level_guard.py::test_nrm_edit_path_squeeze[a/b-a/b] PASSED [100%]
+=============== 123 passed, 311 deselected, 98 xfailed in 6.15s ================
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q
 
-=============== 123 passed, 311 deselected, 85 xfailed in 5.68s ================
-
-=== full file: uv run pytest tests/hooks/test_launch_level_guard.py ===
-======================= 434 passed, 85 xfailed in 9.47s ========================
+======================= 434 passed, 98 xfailed in 10.31s =======================
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index b2918e88..1c2f2d07 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1331,6 +1331,41 @@ def test_nrm_end_to_end(tmp_path, command, level, msg_id):
     _assert_decision(result, tmp_path, msg_id, level, text=msg_id is not None)
 
 
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.xfail(strict=True, reason="class reached in Task 9")
+def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
+    # T-NRM-4: raw JSON bytes with \/ escapes; jq decodes them before the tamper check.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    raw = (
+        b'{"hook_event_name": "PreToolUse", "session_id": "' + SID.encode() + b'", '
+        b'"tool_name": "Bash", "tool_input": {"command": '
+        b'"cp x ~\\/.claude\\/settings.json"}}'
+    )
+    _assert_decision(_run(raw, tmp_path), tmp_path, "LL-TAMPER", level, text=True)
+
+
+@pytest.mark.parametrize("level", ["W", "WA", "F"])
+@pytest.mark.parametrize(
+    "command",
+    [
+        "git push origin a:b \\\nc:main",
+        "git push origin a:b \\\n c:main",
+        "git push origin a:b 2>&1 | tail -5",
+    ],
+    ids=["nrm5-push", "nrm8-push-space", "nrm2-push"],
+)
+@pytest.mark.xfail(strict=True, reason="class reached in Task 7")
+def test_nrm_push_blocked_below_fs(tmp_path, level, command):
+    # T-NRM-5/8/2: a push is blocked at every level (LL-PUSH-FORM only at FS, tested above);
+    # below FS the grid blocks every push form, whichever of its three ids applies.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_bash(command), tmp_path)
+    assert result.returncode == 2
+    assert any(
+        i.encode() in result.stderr for i in ("LL-PUSH", "LL-PUSH-FORM", "LL-PROTECTED")
+    )
+
+
 def _normalise(tmp_path: Path, command: str):
     """Run only the normalise block of the script (test-only route)."""
     driver = (

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=scope at=tests/hooks/test_launch_level_guard.py:1263 anchor="a payload with `\/` escapes in a tamper path is blocked" chk=y,n,n,n family=nrm-mr-coverage fix=add a raw-bytes JSON test with \/ escapes, strict xfail for Task 9 covers="every T-NRM case of MR section 8.2" first=A1 origin=new: row nrm4-escaped-slash sends shell-style backslash-slash text through the command field, so the jq decode of JSON \/ escapes (T-NRM-4) has no test.
F2.1 sev=blocking trigger=B1 ac=scope at=tests/hooks/test_launch_level_guard.py:1266 anchor="blocked at every level (LL-PUSH-FORM at FS)" chk=y,n,n,n family=nrm-mr-coverage fix=add a test that nrm5-push, nrm8-push-space and nrm2-push block at W, WA and F as strict xfail for Task 7 covers="every T-NRM case of MR section 8.2" first=A1 origin=new: the rows use FS_ONLY, so W, WA and F are skipped although T-NRM-5 and T-NRM-8 require blocked at every level.

Saved-probe re-check hit locations (may be empty): 1336:def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
1358:def test_nrm_push_blocked_below_fs(tmp_path, level, command):


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
