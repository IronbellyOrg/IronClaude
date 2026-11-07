f63cf1234e6b12d99fdf0a03387947a5de13a0ab
Review one task for spec compliance.

Task brief: ## Task 9: Implement tamper and escape classification

Depends on: Task 8

In src/superclaude/hooks/scripts/launch-level-guard.sh add the tamper rules (FR-L-49 to FR-L-51) and escape rules (FR-L-47, FR-L-48) of design section 5.1 and the Edit-tool part of section 5.2. Tamper: T, or an edit path after the same slash squeeze, containing .claude/state, .claude/settings, .claude/hooks, disableAllHooks, .gitconfig, .git/config or .config/git; Bash only: a word ending .claude or .claude/, a superclaude word followed later in its segment by install, a word containing install_hooks; Edit, Write and NotebookEdit only: a parent-directory segment or trailing parent-directory path. Contents, prompts and arguments are never checked. Edit, Write and NotebookEdit apply the tamper check only (FR-L-42, source edits are not gated, O-8). Escape: orca is NONE when the segment ends --help or -h, the first word is status, help or --version, or the first two words are worktree current, worktree list, worktree show, terminal list, terminal show, terminal read, or orchestration check, inbox, run-current, task-list, worker-show; any other orca word is ESCAPE; ccsession words are ESCAPE; claude and claude-code (basename cut at @) are ESCAPE when any word in the command is one of -p --print --continue --resume --bare --settings --dangerously-skip-permissions --fork-session --session-id --permission-mode; tmux, screen, xdotool and ydotool are ESCAPE.

Extend tests/hooks/test_launch_level_guard.py with the T-TAM and T-ESC cases of MR section 8.2 and the oracle rows for TAMPER and ESCAPE across the four levels.

Acceptance criteria:
- A governed Edit of ~/.claude/settings.json, a Write of ~/.config/git/config, and a Bash rm -rf ~/.claude/state exit 2 with LL-TAMPER at every level; an Edit of a source file under src/ exits 0; a Write whose content only quotes .claude/hooks exits 0.
- npx -y @anthropic-ai/claude-code@latest -p x, claude -p x, tmux send-keys approved Enter, and orca terminal send exit 2 with LL-ESCAPE at every level; orca worktree list and orca status exit 0.
- The LL-TAMPER message for a bound session includes the exact rm command naming the store and the session id, and for an invalid id uses the LL-BROKEN wording.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "TAM or ESC or tamper or escape" -v passes.

AC ids (source order):
T9.AC1: A governed Edit of ~/.claude/settings.json, a Write of ~/.config/git/config, and a Bash rm -rf ~/.claude/state exit 2 with LL-TAMPER at every level; an Edit of a source file under src/ exits 0; a Write whose content only quotes .claude/hooks exits 0.
T9.AC2: npx -y @anthropic-ai/claude-code@latest -p x, claude -p x, tmux send-keys approved Enter, and orca terminal send exit 2 with LL-ESCAPE at every level; orca worktree list and orca status exit 0.
T9.AC3: The LL-TAMPER message for a bound session includes the exact rm command naming the store and the session id, and for an invalid id uses the LL-BROKEN wording.
T9.AC4: uv run pytest tests/hooks/test_launch_level_guard.py -k "TAM or ESC or tamper or escape" -v passes.
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
Start sha: f63cf1234e6b12d99fdf0a03387947a5de13a0ab
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t9-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t9-test.log
new file mode 100644
index 00000000..4c9263b4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t9-test.log
@@ -0,0 +1,6 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "TAM or ESC or tamper or escape" -q
+..........                                                               [100%]
+
+==================== 619 passed, 2100 deselected in 10.43s =====================
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q (summary)
+============================ 2719 passed in 47.77s =============================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 6262f9f6..ba7321bd 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -5,8 +5,8 @@
 # with a message on stderr; never exit 1, no onFailure. Only a session that the
 # claim script launched (a valid top-level session_id bound in the store) is
 # governed; every other session is ordinary and never blocked (FR-L-53).
-# Ten-part layout (DD-1); Tasks 5 to 8 classify Skill, BIG, NM1a, git (G0-G4,
-# push) and gh, curl, API text (H1-H5); the rest is NONE until Tasks 9 and 10.
+# Ten-part layout (DD-1); Tasks 5 to 9 classify Skill, BIG, NM1a, git, gh, curl,
+# API text, tamper and escape; the rest is NONE until Task 10.
 # launch-level-guard-version: 1
 
 # 1. Settings
@@ -374,6 +374,7 @@ if [ "$LL_BRANCH" = tool ]; then
     # 7. The tool fields come from the one jq parse in part 4.
     # 8. Classifiers add classes to LL_CLASSES (Tasks 5 to 10); none gives NONE.
     LL_CLASSES=' '
+    LL_TT= # the text the tamper tokens are looked for in (T or the edit path)
     if [ "$LL_TOOL" = Skill ]; then
         # FR-L-40: first word, lower case, one leading "/", text after the last
         # ":", one leading "sc-", one trailing "-protocol".
@@ -412,6 +413,50 @@ if [ "$LL_BRANCH" = tool ]; then
             # segs: the segments of W; a segment's words are ws=($seg) under set -f, and (NM7) a word's basename is ${w##*/}.
             IFS=';' read -r -a segs <<<"$W"
             # <<< normalise
+            # Tamper (FR-L-49, FR-L-50) on T and the words; escape (FR-L-47,
+            # FR-L-48) on the words of each segment, any position. W has no "_",
+            # so install_hooks is looked for in T.
+            LL_TT=$T
+            case $T in *install_hooks*) LL_CLASSES+='TAMPER ' ;; esac
+            LL_CL=0 LL_CF=0 # a claude word; a claude launch flag word (whole command)
+            for seg in "${segs[@]}"; do
+                ws=($seg)
+                LL_SC=0 # a superclaude word earlier in this segment
+                for ((i = 0; i < ${#ws[@]}; i++)); do
+                    w=${ws[i]}
+                    b=${w##*/}
+                    case $w in *.claude | *.claude/) LL_CLASSES+='TAMPER ' ;; esac
+                    [ "$w" = install ] && [ "$LL_SC" = 1 ] && LL_CLASSES+='TAMPER '
+                    case $w in -p | --print | --continue | --resume | --bare | --settings | --dangerously-skip-permissions | --fork-session | --session-id | --permission-mode) LL_CF=1 ;; esac
+                    case ${b%%@*} in claude | claude-code) LL_CL=1 ;; esac
+                    case $b in
+                    superclaude | superclaude.*) LL_SC=1 ;;
+                    ccsession* | tmux | screen | xdotool | ydotool) LL_CLASSES+='ESCAPE ' ;;
+                    orca)
+                        # w1, w2: the next two non-option words; --version counts as w1.
+                        LL_W1= LL_W2=
+                        for ((j = i + 1; j < ${#ws[@]}; j++)); do
+                            case ${ws[j]} in
+                            --version) [ -n "$LL_W1" ] || { LL_W1=--version && break; } ;;
+                            -*) ;;
+                            *)
+                                if [ -z "$LL_W1" ]; then
+                                    LL_W1=${ws[j]}
+                                else
+                                    LL_W2=${ws[j]}
+                                    break
+                                fi ;;
+                            esac
+                        done
+                        case "$LL_W1 $LL_W2" in
+                        'status '* | 'help '* | '--version '* | 'worktree current' | 'worktree list' | 'worktree show' | 'terminal list' | 'terminal show' | 'terminal read') ;;
+                        'orchestration check' | 'orchestration inbox' | 'orchestration run-current' | 'orchestration task-list' | 'orchestration worker-show') ;;
+                        *) case ${ws[${#ws[@]} - 1]} in --help | -h) ;; *) LL_CLASSES+='ESCAPE ' ;; esac ;;
+                        esac ;;
+                    esac
+                done
+            done
+            [ "$LL_CL$LL_CF" = 11 ] && LL_CLASSES+='ESCAPE '
             # Git (FR-L-28 to FR-L-34) and gh (FR-L-35 to FR-L-39): G1, G2 and
             # H2 test G; G3, G4, H1, H3, H4 and H5 read the words of each
             # segment; then the canonical push check on raw cmd.
@@ -607,7 +652,15 @@ if [ "$LL_BRANCH" = tool ]; then
         if [ -n "$LL_PATH" ]; then
             EPATH=$(printf '%s\n' "$LL_PATH" | sed -E -e 's#/+#/#g' -e 's#/(\./)+#/#g') || ll_deny LL-BROKEN
         fi
+        # FR-L-42, FR-L-51: the tamper check only; contents are never read.
+        LL_TT=$EPATH
+        case $EPATH in */../* | */..) LL_CLASSES+='TAMPER ' ;; esac
     fi
+    # FR-L-49: the tamper tokens in T or the edit path; the store part is
+    # built from LL_S1 and LL_S2, so this text never names it joined.
+    case $LL_TT in
+    *"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git*) LL_CLASSES+='TAMPER ' ;;
+    esac
     # LL-TEXT: every class of a Bash or Monitor call came from its text.
     if [ "$LL_TOOL" = Bash ] || [ "$LL_TOOL" = Monitor ]; then
         LL_NOTE_TEXT=1
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 49830d10..e38e85cd 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1213,9 +1213,9 @@ def test_notes_follow_the_lines_state_first(tmp_path):
 
 # --- Task 6: Bash and Monitor normalisation (T-NRM, T-FC-7) ----------------
 #
-# Cases whose class needs a Task 9 classifier (tamper, escape) are pinned end
-# to end with a strict xfail naming that task, so the task that reaches the
-# class must drop the mark (Tasks 7 and 8, git and gh, have dropped theirs).
+# A row whose class needs a later classifier names that task in its last field
+# and is pinned with a strict xfail, so the task that reaches the class must
+# drop the mark (Tasks 7 to 9, git, gh, tamper and escape, have dropped theirs).
 # "?" marks a level that the T-NRM row does not pin.
 
 LEVEL_ORDER = ("W", "WA", "F", "FS")
@@ -1250,9 +1250,14 @@ NRM_E2E = [
         GHWRITE,
         None,
     ),
-    ("natk30", f"rm -rf {STATE_PATH.replace('cla', 'cla$' + chr(39) * 2)}", TAMPER, 9),
-    ("natk32", "cp /tmp/s.json ~/.claude/set$''tings.json", TAMPER, 9),
-    ("natk33", ": > ~/.claude/hoo$''ks/launch-level-guard.sh", TAMPER, 9),
+    (
+        "natk30",
+        f"rm -rf {STATE_PATH.replace('cla', 'cla$' + chr(39) * 2)}",
+        TAMPER,
+        None,
+    ),
+    ("natk32", "cp /tmp/s.json ~/.claude/set$''tings.json", TAMPER, None),
+    ("natk33", ": > ~/.claude/hoo$''ks/launch-level-guard.sh", TAMPER, None),
     # T-NRM-2: redirections stay words.
     ("nrm2-stdin", "git commit -m x < /dev/null", FS_ONLY + (None,), None),
     ("nrm2-stdout", "git commit -m x > /tmp/log 2>&1", FS_ONLY + (None,), None),
@@ -1264,7 +1269,7 @@ NRM_E2E = [
         None,
     ),
     # T-NRM-4: \/ escapes in a tamper path.
-    ("nrm4-escaped-slash", "cp x ~\\/.claude\\/\\/.\\/settings.json", TAMPER, 9),
+    ("nrm4-escaped-slash", "cp x ~\\/.claude\\/\\/.\\/settings.json", TAMPER, None),
     # T-NRM-5: a continuation is not joined.
     ("nrm5-gh-api", "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main", GHWRITE, None),
     ("nrm5-push", "git push origin a:b \\\nc:main", FS_ONLY + ("LL-PUSH-FORM",), None),
@@ -1283,7 +1288,7 @@ NRM_E2E = [
         ("LL-SUBMIT",) * 3 + ("LL-REPO",),
         None,
     ),
-    ("nrm5-claude", "claude \\\n-p x", ESCAPE, 9),
+    ("nrm5-claude", "claude \\\n-p x", ESCAPE, None),
     ("nrm5-git-space", "git \\\ncommit -m x", UNK, None),
     # T-NRM-7: a quoted ">" in an assignment.
     ("nrm7-commit", 'A=">" git commit -m x', ("?", "?", "LL-COMMIT", None), None),
@@ -1339,7 +1344,6 @@ def test_nrm_end_to_end(tmp_path, command, level, msg_id):
 
 
 @pytest.mark.parametrize("level", LEVEL_ORDER)
-@pytest.mark.xfail(strict=True, reason="class reached in Task 9")
 def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
     # T-NRM-4: raw JSON bytes with \/ escapes; jq decodes them before the tamper check.
     _bind(tmp_path, *LEVEL_FILES[level])
@@ -1699,7 +1703,7 @@ PROTECTED = ("LL-PROTECTED",) * 4
 MULTILINE = "git commit -m \"$(cat <<'EOF'\nfeat: x\n{line}\nEOF\n)\""
 
 # Grid rows 12 to 18 and 30 to 33 of MR section 8.1, git parts only (gh and
-# curl parts are in GH_ORACLE below; MCP belongs to Task 9). They cover T-GIT-2, 5, 6, 10, 11, 16 and
+# curl parts are in GH_ORACLE below; MCP belongs to Task 10). They cover T-GIT-2, 5, 6, 10, 11, 16 and
 # T-PSH-2, 3, 5 and 7.
 GIT_ORACLE = {
     "NONE": (
@@ -2125,7 +2129,7 @@ PUSH_PROTECTED = [
     "git push origin heads/main",
     "git push -u origin feature:main",
 ]
-# T-PSH-4, 6, 8 (Bash parts; the Write is Task 9) and 10.
+# T-PSH-4, 6, 8 (Bash parts; the Write is in TAMPER_EDITS) and 10.
 PUSH_NAMED = [
     ("git push origin +main", PUSHFORM),
     ("git push origin :main", PUSHFORM),
@@ -2501,3 +2505,277 @@ def test_gh_class_from_text_prints_text_note(tmp_path, tool):
     _bind(tmp_path, *LEVEL_FILES["FS"])
     result = _run(_bash("gh pr merge 5", tool=tool), tmp_path)
     _assert_decision(result, tmp_path, "LL-MERGE", "FS", text=True)
+
+
+# --- Task 9: tamper and escape (T-TAM, T-ESC) -------------------------------
+#
+# Hand-written oracle for the TAMPER and ESCAPE grid rows (MR 8.1 rows 25 to
+# 27, design section 8): both classes block at every level. It is written out
+# per level rather than derived from the script's case statement.
+TAMPER_ESCAPE_ORACLE = {
+    "TAMPER": {
+        "W": "LL-TAMPER",
+        "WA": "LL-TAMPER",
+        "F": "LL-TAMPER",
+        "FS": "LL-TAMPER",
+    },
+    "ESCAPE": {
+        "W": "LL-ESCAPE",
+        "WA": "LL-ESCAPE",
+        "F": "LL-ESCAPE",
+        "FS": "LL-ESCAPE",
+    },
+    "NONE": {"W": None, "WA": None, "F": None, "FS": None},
+}
+HOME_U = "/home/u"
+STATE_ABS = STATE_PATH.replace("~", HOME_U)
+
+# T-TAM-1, T-TAM-5, T-TAM-6: MR row 27 and the reinstall forms.
+TAMPER_BASH = [
+    f"cat {STATE_PATH}/launch-level/sessions/x",
+    f"rm -rf {STATE_PATH}/launch-level",
+    f"rm -rf {STATE_PATH}",
+    f"cd {STATE_PATH} && rm -rf launch-level",
+    f"find {STATE_ABS} -delete",
+    f"mv {STATE_PATH} ~/.claude/s2",
+    "cd ~/.claude && rm -rf state",
+    "cd ~/.claude/ && rm -rf state",
+    "echo '{\"disableAllHooks\":true}' > ~/.claude/settings.json",
+    "cd ~/.claude && : > hooks/x.sh",
+    "cd ~/.claude && : > hooks/launch-level-guard.sh",
+    "cat ~/.gitconfig",
+    "cat .git/config",
+    "cat ~/.config/git/config",
+    "rm -rf ~/.cla$''ude/state",
+    "cp /tmp/s.json ~/.claude/set$''tings.json",
+    ": > ~/.claude/hoo$''ks/launch-level-guard.sh",
+    "uv run superclaude install",
+    'uv run python -c "import superclaude.cli.install_hooks"',
+    "uv run python -m superclaude.cli.main install",
+    "~/.local/bin/superclaude install",
+    "ls; uv run superclaude install --force",
+]
+# T-ESC-1, T-ESC-2, T-ESC-5, T-ESC-6: MR row 25 and the T-ESC forms.
+ESCAPE_BASH = [
+    "claude -p x",
+    "/usr/local/bin/claude --print x",
+    "npx @anthropic-ai/claude-code -p x",
+    "npx -y @anthropic-ai/claude-code@latest -p x",
+    'npx -y @anthropic-ai/claude-code@latest -p "finish the task"',
+    "claude --resume abc",
+    "claude --dangerously-skip-permissions",
+    "ls && claude --continue",
+    "orca agent launch --name w",
+    "orca agent launch --name -h x",
+    "orca terminal send",
+    "orca terminal send --text approved",
+    "orca computer type-text approved",
+    "orca automations run x",
+    "orca orchestration send x",
+    "orca orchestration dispatch x",
+    "orca worktree create --name x",
+    "ls; orca agent launch",
+    "tmux send-keys approved Enter",
+    "tmux new-session -d 'claude \"x\"'",
+    "screen -X stuff x",
+    "xdotool type approved",
+    "ydotool type x",
+    "ccsession",
+    "ccsession-orca 'x'",
+    "/usr/local/bin/ccsession -h",
+]
+# T-TAM-4, MR row 26 and the orca allowlist pairs of T-ESC-2.
+NONE_BASH = [
+    "ls",
+    "cat src/superclaude/hooks/scripts/launch-level-guard.sh",
+    "cat docs/hook-launch-level-394.md",
+    "uv run superclaude doctor",
+    "grep -rn claude docs/",
+    "grep claude -rn docs/",
+    "which claude",
+    "claude --version",
+    "orca status",
+    "orca status --json",
+    "orca help",
+    "orca --version",
+    "orca worktree current",
+    "orca worktree current --json",
+    "orca worktree list",
+    "orca worktree show x",
+    "orca terminal list",
+    "orca terminal show t1",
+    "orca terminal read t1",
+    "orca orchestration check",
+    "orca orchestration inbox",
+    "orca orchestration run-current",
+    "orca orchestration task-list",
+    "orca orchestration worker-show w1",
+    "orca list --help",
+    "orca agent launch -h",
+]
+
+
+def _oracle_params(prefix: str, rows):
+    for i, (payload, cls) in enumerate(rows):
+        for level in LEVEL_ORDER:
+            msg_id = TAMPER_ESCAPE_ORACLE[cls][level]
+            yield pytest.param(payload, level, msg_id, id=f"{prefix}{i}-{level}")
+
+
+def _edit(tool: str, path: str, **extra) -> dict:
+    key = "notebook_path" if tool == "NotebookEdit" else "file_path"
+    return {
+        "hook_event_name": "PreToolUse",
+        "session_id": SID,
+        "tool_name": tool,
+        "tool_input": {key: path, **extra},
+    }
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        *_oracle_params("TAM", [(c, "TAMPER") for c in TAMPER_BASH]),
+        *_oracle_params("ESC", [(c, "ESCAPE") for c in ESCAPE_BASH]),
+        *_oracle_params("NONE", [(c, "NONE") for c in NONE_BASH]),
+    ],
+)
+def test_tamper_escape_bash_oracle(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+@pytest.mark.parametrize("tool", ["Bash", "Monitor"])
+@pytest.mark.parametrize(
+    "command, msg_id",
+    [("rm -rf " + STATE_PATH, "LL-TAMPER"), ("claude -p x", "LL-ESCAPE")],
+)
+def test_tamper_escape_from_monitor_text(tmp_path, tool, command, msg_id):
+    _bind(tmp_path, *LEVEL_FILES["W"])
+    result = _run(_bash(command, tool=tool), tmp_path)
+    _assert_decision(result, tmp_path, msg_id, "W", text=True)
+
+
+# T-TAM-2: each token path, a "//" path, a "/./" path and a ".." path, and
+# [B-4] a Write of ~/.config/git/config (also the Write of T-PSH-8).
+TAMPER_PATHS = [
+    STATE_ABS + "/launch-level/sessions/x",
+    "~/.claude/settings.json",
+    HOME_U + "/.claude/settings.local.json",
+    HOME_U + "/.claude/hooks/launch-level-guard.sh",
+    HOME_U + "/notes/disableAllHooks.txt",
+    HOME_U + "/.gitconfig",
+    "/r/.git/config",
+    "~/.config/git/config",
+    HOME_U + "/.config/git/config",
+    HOME_U + "//.claude/settings.json",
+    HOME_U + "/.claude//hooks/x.sh",
+    HOME_U + "/./.claude/hooks/x.sh",
+    "/r/src/../x.py",
+    "/r/src/..",
+]
+# T-TAM-4 and the Task 9 acceptance: a source file and the guard source path.
+NONE_PATHS = [
+    "src/x.py",
+    "/r/src/x.py",
+    "/r/src/superclaude/hooks/scripts/launch-level-guard.sh",
+    "/r/.dev/hook-launch-level-394/notes.txt",
+    "/r/src/..x/y.py",
+]
+EDIT_TOOL_NAMES = ["Edit", "Write", "NotebookEdit"]
+
+
+@pytest.mark.parametrize("tool", EDIT_TOOL_NAMES)
+@pytest.mark.parametrize(
+    "path, level, msg_id",
+    [
+        *_oracle_params("TAMP", [(p, "TAMPER") for p in TAMPER_PATHS]),
+        *_oracle_params("NONEP", [(p, "NONE") for p in NONE_PATHS]),
+    ],
+)
+def test_tamper_paths(tmp_path, tool, path, level, msg_id):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_edit(tool, path), tmp_path)
+    # Edit tools are not text classes, so no LL-TEXT note.
+    _assert_decision(result, tmp_path, msg_id, level)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize(
+    "tool, extra",
+    [
+        ("Write", {"content": "see ~/.claude/hooks and disableAllHooks"}),
+        ("Edit", {"old_string": ".claude/hooks", "new_string": "disableAllHooks"}),
+        ("NotebookEdit", {"new_source": "~/.claude/settings.json"}),
+    ],
+)
+def test_tamper_ignores_content(tmp_path, level, tool, extra):
+    # T-TAM-3, FR-L-51: contents are never read, only the path.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    _assert_decision(
+        _run(_edit(tool, "/r/src/x.py", **extra), tmp_path), tmp_path, None, level
+    )
+
+
+@pytest.mark.parametrize(
+    "payload",
+    [
+        _bash("rm -rf " + STATE_PATH),
+        _bash("uv run superclaude install"),
+        _bash("claude -p x"),
+        _bash("orca terminal send"),
+        _edit("Edit", "~/.claude/settings.json"),
+        _edit("Write", "~/.config/git/config"),
+    ],
+    ids=[
+        "rm-store",
+        "reinstall",
+        "claude-p",
+        "orca-send",
+        "edit-settings",
+        "write-gitconfig",
+    ],
+)
+def test_tamper_escape_in_ordinary_session_allowed(tmp_path, payload):
+    # T-TAM-7 (X-005): an unbound session is never blocked.
+    _bind(tmp_path, *LEVEL_FILES["W"])
+    payload = {**payload, "session_id": "ordinary-session"}
+    result = _run(payload, tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+# The Task 9 acceptance examples, each at every level.
+TASK9_ACCEPTANCE = [
+    (_edit("Edit", "~/.claude/settings.json"), "TAMPER"),
+    (_edit("Write", "~/.config/git/config"), "TAMPER"),
+    (_bash("rm -rf " + STATE_PATH), "TAMPER"),
+    (_edit("Edit", "src/x.py"), "NONE"),
+    (_edit("Write", "/r/src/x.py", content="quotes .claude/hooks here"), "NONE"),
+    (_bash("npx -y @anthropic-ai/claude-code@latest -p x"), "ESCAPE"),
+    (_bash("claude -p x"), "ESCAPE"),
+    (_bash("tmux send-keys approved Enter"), "ESCAPE"),
+    (_bash("orca terminal send"), "ESCAPE"),
+    (_bash("orca worktree list"), "NONE"),
+    (_bash("orca status"), "NONE"),
+]
+
+
+@pytest.mark.parametrize(
+    "payload, level, msg_id", list(_oracle_params("acc", TASK9_ACCEPTANCE))
+)
+def test_tamper_escape_task9_acceptance(tmp_path, payload, level, msg_id):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(payload, tmp_path)
+    is_text = payload["tool_name"] == "Bash" and msg_id is not None
+    _assert_decision(result, tmp_path, msg_id, level, text=is_text)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+def test_tamper_message_names_store_and_session(tmp_path, level):
+    # A bound session's LL-TAMPER gives the exact rm command for its own files.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_edit("Edit", "~/.claude/settings.json"), tmp_path)
+    store = _store(tmp_path / "home")
+    rm = f'rm "{store}/sessions/{SID}" "{store}/sessions/{SID}.ok"'
+    assert result.returncode == 2
+    you_can = result.stderr.decode().splitlines()[3]
+    assert you_can.startswith("You can: ") and you_can.endswith(f": {rm}")

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
