4350880e0eae9c514ca0b21bc3285ef89b75f33d
Review one task for spec compliance.

Task brief: ## Task 11: Implement typed approval at the worktree level

Depends on: Task 10

In src/superclaude/hooks/scripts/launch-level-guard.sh add the approval rules of design section 6 (FR-L-15 to FR-L-19) to the UserPromptSubmit branch. The event is UserPromptSubmit only (O-4). A prompt matches when the whole prompt, trimmed and lower-cased, matches ^approved[.!]?$, or its first line matches ^/(sc:implement|sc:task|task)([[:space:]]|$); /task-builder, /tasks, /sc:implement-protocol, "please approved", "approved, but" and /sc:pr-submit do not match. Approval is written only for a bound session, a payload without agent_id, and a level of worktree (or an invalid word including degraded): touch sessions/<sid>.ok. At full and full-submit nothing is written. The effect is the WA level, which unlocks IMPL and TURN but never COMMIT, PUSH, SUBMIT or MERGE; a failed touch shows later as LL-IMPL; approval lasts until a person deletes the files (O-6). The prompt event runs before expansion, so the approval file exists before a Skill sc:implement-protocol call (T-APR-9 asserts the order with typed prompt then Skill call).

Extend tests/hooks/test_launch_level_guard.py with every T-APR case of MR section 8.2 and the T-TRN cases that depend on approval.

Acceptance criteria:
- At W: the prompt approved, the prompt /sc:implement x, and the prompt /task y each create sessions/<sid>.ok and exit 0; /task-builder x, please approved and approved, but create nothing.
- A prompt carrying agent_id creates nothing; at full and full-submit approved creates nothing.
- After approval a Skill sc:implement call exits 0 and git commit -m x, git push origin feature and gh pr create --repo o/r --title x still exit 2.
- A read-only sessions directory leaves no .ok file and the next Skill sc:implement call exits 2 with LL-IMPL.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "APR or approval" -v passes.

AC ids (source order):
T11.AC1: At W: the prompt approved, the prompt /sc:implement x, and the prompt /task y each create sessions/<sid>.ok and exit 0; /task-builder x, please approved and approved, but create nothing.
T11.AC2: A prompt carrying agent_id creates nothing; at full and full-submit approved creates nothing.
T11.AC3: After approval a Skill sc:implement call exits 0 and git commit -m x, git push origin feature and gh pr create --repo o/r --title x still exit 2.
T11.AC4: A read-only sessions directory leaves no .ok file and the next Skill sc:implement call exits 2 with LL-IMPL.
T11.AC5: uv run pytest tests/hooks/test_launch_level_guard.py -k "APR or approval" -v passes.
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
Start sha: 4350880e0eae9c514ca0b21bc3285ef89b75f33d
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t11-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t11-test.log
new file mode 100644
index 00000000..cbddba53
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t11-test.log
@@ -0,0 +1,8 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "APR or approval" -q
+tests/hooks/test_launch_level_guard.py ................................. [ 52%]
+..............................                                           [100%]
+
+===================== 63 passed, 3103 deselected in 1.85s ======================
+
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q (summary)
+============================ 3166 passed in 57.35s =============================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index fb1a041c..8c56ddae 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -281,7 +281,7 @@ PreToolUse) LL_BRANCH=tool ;;
     [ "$LL_GOVERNED" = 1 ] || exit 0 ;;
 esac
 
-# 5. Prompt branch: binding (FR-L-09, B1 to B13); approval is Task 11.
+# 5. Prompt branch: binding (FR-L-09, B1 to B13), then approval (FR-L-15 to FR-L-19).
 # Writes: mkdir -p sessions; take pending/<nonce> with one rename (mv) to
 # sessions/.take-<sid>, so a nonce is consumed once; publish sessions/<sid> with
 # a hard link (ln), which fails when the target exists, so the first binding is
@@ -338,7 +338,30 @@ if [ "$LL_BRANCH" = prompt ]; then
     if [ "$LL_GOVERNED" = 1 ]; then
         # B8: already bound; the level never changes, a supplied record is consumed.
         [ "$LL_USABLE" = 1 ] && rm -f -- "$LL_PEND/$LL_NONCE" 2>/dev/null
-        exit 0 # the approval check (Task 11) runs here
+        # Approval (FR-L-15 to FR-L-17): only at worktree (an invalid word
+        # included), never at full or full-submit. The whole prompt trimmed and
+        # lower-cased is approved, approved. or approved!; or the first line,
+        # leading whitespace removed, starts /sc:implement, /sc:task or /task
+        # as a whole word. The [[:space:]] after the command name also matches
+        # the newline that ends the first line.
+        LL_RE_APR='^[[:space:]]*/(sc:implement|sc:task|task)([[:space:]]|$)'
+        LL_APR=0
+        if [ "$LL_LEVEL" = W ]; then
+            [[ $LL_PROMPT =~ $LL_RE_APR ]] && LL_APR=1
+            LL_P=${LL_PROMPT#"${LL_PROMPT%%[![:space:]]*}"}
+            LL_P=${LL_P%"${LL_P##*[![:space:]]}"}
+            [[ ${LL_P,,} =~ ^approved[.!]?$ ]] && LL_APR=1
+        fi
+        if [ "$LL_APR" = 1 ]; then
+            # No-replace create of a regular file in the owned sessions
+            # directory; an existing .ok of any kind is left alone. A failed
+            # write still allows the prompt and shows later as LL-IMPL.
+            if [ -d "$LL_STORE/sessions" ] && [ ! -L "$LL_STORE/sessions" ] && [ -O "$LL_STORE/sessions" ] &&
+                [ ! -e "$LL_FILE.ok" ] && [ ! -L "$LL_FILE.ok" ]; then
+                (set -C; : >"$LL_FILE.ok") 2>/dev/null
+            fi
+        fi
+        exit 0 # approval lasts until a person deletes the session's files (O-6)
     fi
     if [ -z "$LL_NONCE" ] && [ "$LL_LOOSE" = 0 ]; then
         exit 0 # B9: unbound, no marker
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index d980034c..633d726c 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1,4 +1,4 @@
-"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 10).
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 11).
 
 Each case runs the real script with a JSON payload on stdin, HOME inside
 tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
@@ -3197,3 +3197,247 @@ def _corpus_params():
 def test_regression_corpus(tmp_path, command, level, msg_id):
     # T-COR-1
     _git_case(tmp_path, command, level, msg_id)
+
+
+# --- UserPromptSubmit: typed approval at the worktree level (Task 11) --------
+
+
+def _ok_path(tmp_path: Path) -> Path:
+    return _store(tmp_path / "home") / "sessions" / f"{SID}.ok"
+
+
+def _approve(tmp_path: Path, text: str, **extra):
+    """Send one prompt; a prompt event always allows silently."""
+    result = _run(_prompt(text, **extra), tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+    return result
+
+
+APPROVING = [
+    # T-APR-1: the whole prompt, trimmed and lower-cased.
+    "approved",
+    "Approved.",
+    "  APPROVED!  ",
+    "approved\n",
+    "\t\r\napproved!\r\n",
+    # T-APR-2: the first line, leading whitespace removed (case-sensitive).
+    "/sc:implement x",
+    "/task",
+    "/sc:task y",
+    "/task y",
+    "/sc:implement",
+    "  /sc:implement x\nmore text",
+    "\n/task\tz",
+    "/task\nsecond line",
+]
+NOT_APPROVING = [
+    # T-APR-4
+    "please approved",
+    "approved, but",
+    "/task-builder x",
+    "/tasks",
+    "/sc:implement-protocol",
+    "/sc:pr-submit",
+    "approved approved",
+    "approved!!",
+    "approved?",
+    "approvedx",
+    "not approved",
+    "/sc:implementx",
+    "/SC:IMPLEMENT x",
+    "x\n/sc:implement y",
+    "sc:implement x",
+    "",
+]
+
+
+@pytest.mark.parametrize("text", APPROVING, ids=lambda t: f"APR-yes-{t!r}")
+def test_apr_matching_prompt_writes_ok_at_w(tmp_path, text):
+    # T-APR-1, T-APR-2: FR-L-16; the .ok file is empty, regular, not a link.
+    sessions = _bind(tmp_path, "worktree")
+    _approve(tmp_path, text)
+    ok = _ok_path(tmp_path)
+    assert ok.is_file() and not ok.is_symlink()
+    assert ok.read_bytes() == b""
+    assert sorted(p.name for p in sessions.iterdir()) == [SID, f"{SID}.ok"]
+
+
+@pytest.mark.parametrize("text", NOT_APPROVING, ids=lambda t: f"APR-no-{t!r}")
+def test_apr_exact_form_needed(tmp_path, text):
+    # T-APR-4
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, text)
+    assert _session_files(tmp_path) == [SID]
+
+
+@pytest.mark.parametrize("agent_id", ["agent-1", "a"])
+@pytest.mark.parametrize("text", ["approved", "/sc:implement x"])
+def test_apr_ignored_with_agent_id(tmp_path, text, agent_id):
+    # T-APR-3: a subagent prompt never approves (B5, U17).
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, text, agent_id=agent_id)
+    assert _session_files(tmp_path) == [SID]
+
+
+@pytest.mark.parametrize("word", ["full", "full-submit"])
+@pytest.mark.parametrize("text", ["approved", "/sc:implement x", "/task y"])
+def test_apr_ok_written_only_at_worktree(tmp_path, word, text):
+    # T-APR-6: FR-L-15, nothing is written at F and FS.
+    _bind(tmp_path, word)
+    _approve(tmp_path, text)
+    assert _session_files(tmp_path) == [SID]
+
+
+def test_apr_unbound_session_cannot_approve(tmp_path):
+    # T-APR-7: an unbound id writes nothing, with an empty or a nonempty store.
+    _approve(tmp_path, "approved")
+    assert not _store(tmp_path / "home").exists()
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, "approved", sid="other-session")
+    _approve(tmp_path, "approved", sid=None)
+    assert _session_files(tmp_path) == [SID]
+
+
+@pytest.mark.parametrize("word", ["degraded", "bogus", "", "worktree\n"])
+def test_apr_degraded_session_can_approve(tmp_path, word):
+    # T-APR-8: an invalid word is worktree, so approval is written and unlocks IMPL.
+    _bind(tmp_path, word)
+    _assert_decision(
+        _run(_skill("sc:implement"), tmp_path),
+        tmp_path,
+        "LL-IMPL",
+        "W",
+        note=word not in ("worktree\n",),
+    )
+    _approve(tmp_path, "approved")
+    assert _ok_path(tmp_path).is_file()
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")
+
+
+@pytest.mark.parametrize("text", ["/sc:implement x", "/task y", "approved"])
+def test_apr_typed_implement_then_skill_call_allowed(tmp_path, text):
+    # T-APR-9: FR-L-18, in order: the Skill call is blocked before the prompt,
+    # the prompt event writes .ok, then the expanded Skill call is allowed.
+    _bind(tmp_path, "worktree")
+    skill = _skill("sc:implement-protocol")
+    _assert_decision(_run(skill, tmp_path), tmp_path, "LL-IMPL", "W")
+    assert not _ok_path(tmp_path).exists()
+    _approve(tmp_path, text)
+    assert _ok_path(tmp_path).is_file()
+    _assert_decision(_run(skill, tmp_path), tmp_path, None, "WA")
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")
+
+
+APR_STILL_BLOCKED = [
+    ("commit", _bash("git commit -m x"), "LL-COMMIT"),
+    ("push", _bash("git push origin feature"), "LL-PUSH"),
+    ("pr-create", _bash("gh pr create --repo o/r --title x"), "LL-SUBMIT"),
+    ("pr-submit", _skill("sc:pr-submit"), "LL-SUBMIT"),
+    ("merge", _bash("gh pr merge 5"), "LL-MERGE"),
+    ("push-main", _bash("git push origin main"), "LL-PROTECTED"),
+]
+
+
+@pytest.mark.parametrize(
+    "payload, msg_id",
+    [pytest.param(p, m, id=f"APR-5-{n}") for n, p, m in APR_STILL_BLOCKED],
+)
+def test_apr_approval_never_unlocks_commit_push_submit(tmp_path, payload, msg_id):
+    # T-APR-5: FR-L-17, the typed approval gives WA, which unlocks IMPL only.
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, "approved")
+    result = _run(payload, tmp_path)
+    _assert_decision(result, tmp_path, msg_id, "WA", text=_text_note(payload, msg_id))
+
+
+@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory modes")
+def test_apr_failed_write_shows_later_as_impl(tmp_path):
+    # FR-L-17: a read-only sessions directory leaves no .ok, the prompt still
+    # goes ahead, and the next Skill sc:implement call is LL-IMPL.
+    sessions = _bind(tmp_path, "worktree")
+    sessions.chmod(0o500)
+    try:
+        _approve(tmp_path, "approved")
+        _approve(tmp_path, "/sc:implement x")
+        assert sorted(p.name for p in sessions.iterdir()) == [SID]
+        result = _run(_skill("sc:implement"), tmp_path)
+    finally:
+        sessions.chmod(0o700)
+    _assert_decision(result, tmp_path, "LL-IMPL", "W")
+
+
+def test_apr_existing_ok_link_never_followed(tmp_path):
+    # Task 4 discipline: no replace, regular non-symlink files only. A link at
+    # the .ok path is left alone, its target is not created and is no approval.
+    _bind(tmp_path, "worktree")
+    target = tmp_path / "elsewhere"
+    _ok_path(tmp_path).symlink_to(target)
+    _approve(tmp_path, "approved")
+    assert not target.exists() and _ok_path(tmp_path).is_symlink()
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+def test_apr_lasts_until_a_person_deletes_the_files(tmp_path):
+    # O-6: later prompts and calls never remove the approval.
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, "approved")
+    for text in ("please approved", "/sc:pr-submit", "approved", "anything"):
+        _approve(tmp_path, text)
+    assert _session_files(tmp_path) == [SID, f"{SID}.ok"]
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")
+    _ok_path(tmp_path).unlink()
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+WRAPPED_TURNS = {
+    "task-notification": (
+        "<task-notification>\n<task-id>b1</task-id>\n<status>completed</status>\n"
+        "<summary>Background command finished</summary>\n<result>\napproved\n"
+        "</result>\n</task-notification>"
+    ),
+    "monitor-line": "<monitor-event>\napproved\n</monitor-event>",
+    "subagent-result": (
+        "<task-notification>\n<result>/sc:implement x</result>\n</task-notification>"
+    ),
+}
+
+
+@pytest.mark.parametrize("text", WRAPPED_TURNS.values(), ids=list(WRAPPED_TURNS))
+def test_apr_wrapped_notification_does_not_approve(tmp_path, text):
+    # T-APR-10: hand-written shape until OB-H1 item 5 supplies the real one.
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, text)
+    assert _session_files(tmp_path) == [SID]
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+def test_apr_prompt_runs_no_sed_or_tr(tmp_path):
+    # Trimming and lower-casing are bash string operations.
+    log = _counting_bin(tmp_path)
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, "  APPROVED!  ")
+    _approve(tmp_path, "please approved " * 1000)
+    assert _ok_path(tmp_path).is_file()
+    assert not log.exists()
+
+
+@pytest.mark.parametrize("tool", ["CronCreate", "ScheduleWakeup"])
+def test_trn_turn_blocked_before_and_allowed_after_typed_approval(tmp_path, tool):
+    # T-TRN-1, T-TRN-2 through the real approval route.
+    _bind(tmp_path, "worktree")
+    payload = _tool(tool, prompt="approved")
+    _assert_decision(_run(payload, tmp_path), tmp_path, "LL-TURN", "W")
+    _approve(tmp_path, "approved")
+    _assert_decision(_run(payload, tmp_path), tmp_path, None, "WA")
+
+
+def test_trn_routes_never_write_approval(tmp_path):
+    # T-TRN-4: no route the agent can call writes an approval, and the turn a
+    # background route starts arrives wrapped (T-APR-10), so IMPL stays blocked.
+    _bind(tmp_path, "worktree")
+    for _name, payload, _msg_id in TRN_ROUTES:
+        _run(payload, tmp_path)
+    for text in WRAPPED_TURNS.values():
+        _approve(tmp_path, text)
+    assert _session_files(tmp_path) == [SID]
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")

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
