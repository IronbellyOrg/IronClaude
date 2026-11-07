b9af89d68d7c18af63eeb5b0e513b9a01a44cc38
Review one task for spec compliance.

Task brief: ## Task 7: Implement git classification and the canonical push check

Depends on: Task 6

In src/superclaude/hooks/scripts/launch-level-guard.sh add the git rules of design section 5.1: the G0 word definitions (git word, gated COMMIT, PUSH and MERGE words including git-<name> forms), the G1 global rule applied to G, G2 (alias, pushurl, insteadof, hookspath, remote., url., include., includeif. and set-url give UNKNOWN), G3 command position (skipped NAME=value words, options, numeric words, wrappers env sudo nohup exec command builtin timeout xargs setsid time nice stdbuf ionice doas unbuffer eval, shells with a -c flag, reserved words if then else elif do while until coproc) with the subcommand table of the design (none, NONE, COMMIT, MERGE, PUSH and UNKNOWN rows including the long read-only list and the remote, config and worktree list exceptions), and G4 (a dollar sign in the subcommand after any git word adds UNKNOWN; a value-taking option with no following value adds UNKNOWN). Add the canonical push check (FR-L-33, FR-L-34): any call with PUSH tests the raw command against the anchored expression printed in design section 5.1; no match gives PUSHFORM; a match takes the destination (capture 5, else capture 3, minus one refs/heads/ or heads/ prefix); master or main gives PROTECTED; HEAD gives PUSHFORM.

Extend tests/hooks/test_launch_level_guard.py with the T-GIT and T-PSH cases of MR section 8.2, the accepted and rejected push lists PA1, PA4, PA6, PR1, PR3, PR6, PR13, PR15, PR24 and PD1, and the hand-written oracle rows for COMMIT, PUSH, PUSHFORM, PROTECTED, MERGE and UNKNOWN across W, WA, F and FS.

Acceptance criteria:
- At FS: git push origin feature, git push -u origin feature and git push origin 3f2a9c1e:feature/x exit 0; git push, git push --force origin f, git push origin f piped to tail, and cd x && git push origin a:b exit 2 with LL-PUSH-FORM; git push origin main and git push -u origin feature:main exit 2 with LL-PROTECTED.
- At W, WA and F every git push form exits 2 (LL-PUSH, LL-PUSH-FORM or LL-PROTECTED as the grid says) and git commit -m x exits 2 with LL-COMMIT; at FS git commit -m x exits 0.
- git merge x, git pull and git log --grep merge exit 2 with LL-MERGE at every level, and the LL-TEXT note is printed for the text-derived ones.
- git status, git diff, git log and git -C "$(git rev-parse --show-toplevel)" status exit 0 at every level.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "GIT or PSH or git or push" -v passes.

AC ids (source order):
T7.AC1: At FS: git push origin feature, git push -u origin feature and git push origin 3f2a9c1e:feature/x exit 0; git push, git push --force origin f, git push origin f piped to tail, and cd x && git push origin a:b exit 2 with LL-PUSH-FORM; git push origin main and git push -u origin feature:main exit 2 with LL-PROTECTED.
T7.AC2: At W, WA and F every git push form exits 2 (LL-PUSH, LL-PUSH-FORM or LL-PROTECTED as the grid says) and git commit -m x exits 2 with LL-COMMIT; at FS git commit -m x exits 0.
T7.AC3: git merge x, git pull and git log --grep merge exit 2 with LL-MERGE at every level, and the LL-TEXT note is printed for the text-derived ones.
T7.AC4: git status, git diff, git log and git -C "$(git rev-parse --show-toplevel)" status exit 0 at every level.
T7.AC5: uv run pytest tests/hooks/test_launch_level_guard.py -k "GIT or PSH or git or push" -v passes.
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
Start sha: b9af89d68d7c18af63eeb5b0e513b9a01a44cc38
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log
new file mode 100644
index 00000000..08a0a35c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log
@@ -0,0 +1,5 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "GIT or PSH or git or push" -q  (after the fix pass)
+
+==================== 1041 passed, 459 deselected in 19.04s =====================
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q
+====================== 1464 passed, 36 xfailed in 27.66s =======================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index 8aa89899..d2a6c376 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -5,8 +5,8 @@
 # with a message on stderr; never exit 1, no onFailure. Only a session that the
 # claim script launched (a valid top-level session_id bound in the store) is
 # governed; every other session is ordinary and never blocked (FR-L-53).
-# Ten-part layout (DD-1); Tasks 5 and 6 classify Skill calls and Bash/Monitor
-# BIG and NM1a UNKNOWN; anything else is NONE until Tasks 7 to 10.
+# Ten-part layout (DD-1); Tasks 5 to 7 classify Skill, BIG, NM1a and git (G0 to
+# G4, canonical push); anything else is NONE until Tasks 8 to 10.
 # launch-level-guard-version: 1
 
 # 1. Settings
@@ -412,6 +412,100 @@ if [ "$LL_BRANCH" = tool ]; then
             # segs: the segments of W; a segment's words are ws=($seg) under set -f, and (NM7) a word's basename is ${w##*/}.
             IFS=';' read -r -a segs <<<"$W"
             # <<< normalise
+            # Git (FR-L-28 to FR-L-34): G1 and G2 test G; G3 and G4 read the
+            # words of each segment; then the canonical push check on raw cmd.
+            LL_RE='( |/)git(-[a-z][a-z-]*)? '
+            if [[ $G =~ $LL_RE ]]; then
+                LL_RE='( |/git-| git-)(merge|pull) '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='MERGE '
+                LL_RE='( |/git-| git-)(push|send-pack|http-push) '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='PUSH '
+                LL_RE='( |/git-| git-)(commit|cherry-pick|am|commit-tree) '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='COMMIT '
+                LL_RE='alias\.|pushurl|insteadof|hookspath| (remote|url|include|includeif)\.| set-url '
+                [[ $G =~ $LL_RE ]] && LL_CLASSES+='UNKNOWN '
+                LL_RE_NAME='^[A-Za-z_][A-Za-z0-9_]*='
+                LL_RE_NUM='^[0-9]+(\.[0-9]+)?[smhd]?$'
+                LL_RE_DASH='^git-[a-z][a-z-]*$'
+                for seg in "${segs[@]}"; do
+                    ws=($seg)
+                    LL_CP=-1 # index of the command-position word, -1 while skipping
+                    for ((i = 0; i < ${#ws[@]}; i++)); do
+                        w=${ws[i]}
+                        if [ "$LL_CP" = -1 ]; then
+                            case $w in -*) continue ;; esac
+                            LL_B=${w##*/} # wrappers and shells match by basename (NM7)
+                            case $LL_B in
+                            env | sudo | nohup | exec | command | builtin | timeout | xargs | setsid | time | nice | stdbuf | ionice | doas | unbuffer | eval | if | then | else | elif | do | while | until | coproc) continue ;;
+                            bash | sh | zsh | dash | ksh)
+                                if [[ ${ws[i + 1]:-} =~ ^-[a-z]*c$ ]]; then
+                                    i=$((i + 1))
+                                    continue
+                                fi ;;
+                            esac
+                            [[ $w =~ $LL_RE_NAME || $w =~ $LL_RE_NUM ]] && continue
+                            LL_CP=$i
+                        fi
+                        b=${w##*/}
+                        case $b in git) ;; git-*) [[ $b =~ $LL_RE_DASH ]] || continue ;; *) continue ;; esac
+                        # S: the dashed name, or the first non-option word after git.
+                        LL_S= LL_SI=$i LL_HV=0 LL_LV= LL_DG=0
+                        if [ "$b" != git ]; then
+                            LL_S=${b#git-}
+                        else
+                            j=$((i + 1))
+                            while [ "$j" -lt "${#ws[@]}" ]; do
+                                case ${ws[j]} in
+                                -C | -c | --git-dir | --work-tree | --namespace | --config-env | --attr-source)
+                                    if [ $((j + 1)) -ge "${#ws[@]}" ]; then
+                                        LL_DG=1
+                                        break
+                                    fi
+                                    LL_LV=${ws[j + 1]}
+                                    j=$((j + 2)) ;;
+                                --version | --help | -h) LL_HV=1 j=$((j + 1)) ;;
+                                -*) j=$((j + 1)) ;;
+                                *) LL_S=${ws[j]} LL_SI=$j; break ;;
+                                esac
+                            done
+                        fi
+                        # G4: every git word, in command position or not.
+                        if [ "$LL_DG" = 1 ] || [[ $LL_S == *'$'* ]]; then
+                            LL_CLASSES+='UNKNOWN '
+                        fi
+                        [ "$LL_CP" = "$i" ] || continue
+                        # G3: the subcommand table, command position only.
+                        LL_NX=${ws[LL_SI + 1]:-}
+                        case $LL_S in
+                        '') [ "$LL_HV" = 1 ] || [ "$LL_LV" = '$' ] || LL_CLASSES+='UNKNOWN ' ;;
+                        commit | cherry-pick | revert | am | commit-tree) LL_CLASSES+='COMMIT ' ;;
+                        update-ref)
+                            for ((j = LL_SI + 1; j < ${#ws[@]}; j++)); do
+                                case ${ws[j]} in HEAD | --stdin | refs/heads/*) LL_CLASSES+='COMMIT ' && break ;; esac
+                            done ;;
+                        merge | pull) LL_CLASSES+='MERGE ' ;;
+                        push) LL_CLASSES+='PUSH ' ;;
+                        add | apply | bisect | blame | branch | cat-file | check-attr | check-ignore | check-ref-format | checkout | clean | count-objects | describe | diff | diff-files | diff-index | diff-tree | fetch | for-each-ref | format-patch | fsck | gc | grep | hash-object | help | log | ls-files | ls-remote | ls-tree | merge-base | merge-tree | mv | name-rev | range-diff | read-tree | rebase | reflog | reset | restore | rev-list | rev-parse | rm | shortlog | show | show-branch | show-ref | stash | status | switch | tag | var | version | whatchanged | write-tree) ;;
+                        remote) case $LL_NX in '' | -v | --verbose | get-url | show) ;; *) LL_CLASSES+='UNKNOWN ' ;; esac ;;
+                        config) case $LL_NX in --get | --get-all | --get-regexp | --list | -l | get | list) ;; *) LL_CLASSES+='UNKNOWN ' ;; esac ;;
+                        worktree) [ "$LL_NX" = list ] || LL_CLASSES+='UNKNOWN ' ;;
+                        *) LL_CLASSES+='UNKNOWN ' ;;
+                        esac
+                    done
+                done
+                # Canonical push (FR-L-33, FR-L-34): only one plain git push to origin passes.
+                case $LL_CLASSES in
+                *' PUSH '*)
+                    LL_RE='^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$'
+                    if [[ $cmd =~ $LL_RE ]]; then
+                        LL_D=${BASH_REMATCH[5]:-${BASH_REMATCH[3]}}
+                        case $LL_D in refs/heads/*) LL_D=${LL_D#refs/heads/} ;; heads/*) LL_D=${LL_D#heads/} ;; esac
+                        case $LL_D in master | main) LL_CLASSES+='PROTECTED ' ;; HEAD) LL_CLASSES+='PUSHFORM ' ;; esac
+                    else
+                        LL_CLASSES+='PUSHFORM '
+                    fi ;;
+                esac
+            fi
         fi
     elif [ "$LL_TOOL" = Edit ] || [ "$LL_TOOL" = Write ] || [ "$LL_TOOL" = NotebookEdit ]; then
         # EPATH: the edit path after the NM3 "/" squeeze, one sed; the tamper check reads it.
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 1c2f2d07..9aa07070 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1,4 +1,4 @@
-"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 6).
+"""Behavioral tests for launch-level-guard.sh (issue #394, plan Tasks 3 to 7).
 
 Each case runs the real script with a JSON payload on stdin, HOME inside
 tmp_path, CLAUDE_CONFIG_DIR unset and a PATH holding only a temporary bin
@@ -929,7 +929,6 @@ def test_huge_fields_are_quick(tmp_path):
 @pytest.mark.parametrize(
     "tool_name, tool_input",
     [
-        ("Bash", {"command": "git push origin main"}),
         ("Edit", {"file_path": "/x/settings.json"}),
         ("Agent", {"isolation": "remote"}),
         ("Read", {"file_path": "/etc/passwd"}),
@@ -939,7 +938,7 @@ def test_huge_fields_are_quick(tmp_path):
 def test_other_tools_are_none_until_their_classifiers_exist(
     tmp_path, tool_name, tool_input
 ):
-    # Tasks 6 to 10 add these classifiers; until then a non-Skill call is NONE.
+    # Tasks 8 to 10 add these classifiers; until then such a call is NONE.
     _bind(tmp_path, "worktree")
     payload = {
         "hook_event_name": "PreToolUse",
@@ -1214,9 +1213,9 @@ def test_notes_follow_the_lines_state_first(tmp_path):
 
 # --- Task 6: Bash and Monitor normalisation (T-NRM, T-FC-7) ----------------
 #
-# Cases whose class needs a Task 7 to 9 classifier (git, gh, tamper, escape)
-# are pinned end to end with a strict xfail naming that task, so the task that
-# reaches the class must drop the mark. "?" marks a level that the T-NRM row
+# Cases whose class needs a Task 8 or 9 classifier (gh, tamper, escape) are
+# pinned end to end with a strict xfail naming that task, so the task that
+# reaches the class must drop the mark (Task 7, git, has dropped its marks). "?" marks a level that the T-NRM row
 # does not pin.
 
 LEVEL_ORDER = ("W", "WA", "F", "FS")
@@ -1233,17 +1232,17 @@ STATE_PATH = "~/.cla" + "ude/state"  # spelled in two parts, as the script must
 
 NRM_E2E = [
     # T-NRM-1: quote and backslash splicing; amendment cases N-ATK-3 to 33.
-    ("nrm1-quote-push", 'g""it push origin main', PUSH, 7),
-    ("nrm1-backslash-push", "\\git push origin main", PUSH, 7),
-    ("nrm1-split-quote", "git push origin 'feature:ma''in'", PUSH, 7),
-    ("nrm1-split-backslash", "git push origin feature:ma\\in", PUSH, 7),
-    ("nrm1-quote-commit", 'g""it commit -m x', ("?", "?", "LL-COMMIT", "?"), 7),
-    ("nrm1-backslash-commit", "\\git commit -m x", ("?", "?", "LL-COMMIT", "?"), 7),
-    ("natk3", "git$'' push origin HEAD:main", PUSH, 7),
-    ("natk4", 'g$""it push origin HEAD:main', PUSH, 7),
-    ("natk15", "git$'' -c x.y=z push origin HEAD:main", PUSH, 7),
-    ("natk16", "git$'' merge other --no-edit", MERGE, 7),
-    ("natk18", "git$'' commit --allow-empty -m x", COMMIT, 7),
+    ("nrm1-quote-push", 'g""it push origin main', PUSH, None),
+    ("nrm1-backslash-push", "\\git push origin main", PUSH, None),
+    ("nrm1-split-quote", "git push origin 'feature:ma''in'", PUSH, None),
+    ("nrm1-split-backslash", "git push origin feature:ma\\in", PUSH, None),
+    ("nrm1-quote-commit", 'g""it commit -m x', ("?", "?", "LL-COMMIT", "?"), None),
+    ("nrm1-backslash-commit", "\\git commit -m x", ("?", "?", "LL-COMMIT", "?"), None),
+    ("natk3", "git$'' push origin HEAD:main", PUSH, None),
+    ("natk4", 'g$""it push origin HEAD:main', PUSH, None),
+    ("natk15", "git$'' -c x.y=z push origin HEAD:main", PUSH, None),
+    ("natk16", "git$'' merge other --no-edit", MERGE, None),
+    ("natk18", "git$'' commit --allow-empty -m x", COMMIT, None),
     ("natk23", "g$''h pr merge 5", MERGE, 8),
     (
         "natk24",
@@ -1255,20 +1254,25 @@ NRM_E2E = [
     ("natk32", "cp /tmp/s.json ~/.claude/set$''tings.json", TAMPER, 9),
     ("natk33", ": > ~/.claude/hoo$''ks/launch-level-guard.sh", TAMPER, 9),
     # T-NRM-2: redirections stay words.
-    ("nrm2-stdin", "git commit -m x < /dev/null", FS_ONLY + (None,), 7),
-    ("nrm2-stdout", "git commit -m x > /tmp/log 2>&1", FS_ONLY + (None,), 7),
+    ("nrm2-stdin", "git commit -m x < /dev/null", FS_ONLY + (None,), None),
+    ("nrm2-stdout", "git commit -m x > /tmp/log 2>&1", FS_ONLY + (None,), None),
     ("nrm2-status", "git status 2>&1 | tail -5", FS_ONLY + (None,), None),
-    ("nrm2-push", "git push origin a:b 2>&1 | tail -5", FS_ONLY + ("LL-PUSH-FORM",), 7),
+    (
+        "nrm2-push",
+        "git push origin a:b 2>&1 | tail -5",
+        FS_ONLY + ("LL-PUSH-FORM",),
+        None,
+    ),
     # T-NRM-4: \/ escapes in a tamper path.
     ("nrm4-escaped-slash", "cp x ~\\/.claude\\/\\/.\\/settings.json", TAMPER, 9),
     # T-NRM-5: a continuation is not joined.
     ("nrm5-gh-api", "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main", GHWRITE, 8),
-    ("nrm5-push", "git push origin a:b \\\nc:main", FS_ONLY + ("LL-PUSH-FORM",), 7),
+    ("nrm5-push", "git push origin a:b \\\nc:main", FS_ONLY + ("LL-PUSH-FORM",), None),
     (
         "nrm5-double-backslash",
         "git status \\\\\ngit -c alias.p=push p origin HEAD:main",
         UNK,
-        7,
+        None,
     ),
     (
         "nrm5-pr-create",
@@ -1277,10 +1281,10 @@ NRM_E2E = [
         8,
     ),
     ("nrm5-claude", "claude \\\n-p x", ESCAPE, 9),
-    ("nrm5-git-space", "git \\\ncommit -m x", UNK, 7),
+    ("nrm5-git-space", "git \\\ncommit -m x", UNK, None),
     # T-NRM-7: a quoted ">" in an assignment.
-    ("nrm7-commit", 'A=">" git commit -m x', ("?", "?", "LL-COMMIT", None), 7),
-    ("nrm7-push", 'A=">" git push origin HEAD:main', PUSH, 7),
+    ("nrm7-commit", 'A=">" git commit -m x', ("?", "?", "LL-COMMIT", None), None),
+    ("nrm7-push", 'A=">" git push origin HEAD:main', PUSH, None),
     # T-NRM-8: NM1a, a backslash-newline inside a word, is UNKNOWN (reachable now).
     ("natk1", "gi\\\nt push origin HEAD:main", UNK, None),
     ("natk2", 'bash -c "gi\\\nt push origin HEAD:main"', UNK, None),
@@ -1295,7 +1299,7 @@ NRM_E2E = [
         "nrm8-push-space",
         "git push origin a:b \\\n c:main",
         FS_ONLY + ("LL-PUSH-FORM",),
-        7,
+        None,
     ),
 ]
 
@@ -1354,16 +1358,19 @@ def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
     ],
     ids=["nrm5-push", "nrm8-push-space", "nrm2-push"],
 )
-@pytest.mark.xfail(strict=True, reason="class reached in Task 7")
 def test_nrm_push_blocked_below_fs(tmp_path, level, command):
     # T-NRM-5/8/2: a push is blocked at every level (LL-PUSH-FORM only at FS, tested above);
     # below FS the grid blocks every push form, whichever of its three ids applies.
     _bind(tmp_path, *LEVEL_FILES[level])
     result = _run(_bash(command), tmp_path)
     assert result.returncode == 2
-    assert any(
-        i.encode() in result.stderr for i in ("LL-PUSH", "LL-PUSH-FORM", "LL-PROTECTED")
-    )
+    # The printed text carries no id, so compare with each id's full message.
+    store = str(_store(tmp_path / "home"))
+    note = _design_note("LL-TEXT") + "\n"
+    assert result.stderr.decode() in {
+        _expected(i, LEVELS[level], SID, store) + note
+        for i in ("LL-PUSH", "LL-PUSH-FORM", "LL-PROTECTED")
+    }
 
 
 def _normalise(tmp_path: Path, command: str):
@@ -1675,3 +1682,487 @@ def test_nrm_edit_path_squeeze(tmp_path, path, want):
         timeout=10,
     )
     assert (result.returncode, result.stdout.decode()) == (0, want)
+
+
+# --- Task 7: git classification and the canonical push check (T-GIT, T-PSH) ---
+#
+# Every expected tuple below is written by hand from the grid of MR section 8.1
+# (W, WA, F, FS); none is derived from the script's case statements. A Bash
+# block always carries the LL-TEXT note.
+
+PUSH_OK = ("LL-PUSH", "LL-PUSH", "LL-PUSH", None)  # class PUSH only
+PUSHFORM = ("LL-PUSH", "LL-PUSH", "LL-PUSH", "LL-PUSH-FORM")  # PUSH and PUSHFORM
+PROTECTED = ("LL-PROTECTED",) * 4
+MULTILINE = "git commit -m \"$(cat <<'EOF'\nfeat: x\n{line}\nEOF\n)\""
+
+# Grid rows 12 to 18 and 30 to 33 of MR section 8.1, git parts only (gh, curl
+# and MCP parts belong to Task 8). They cover T-GIT-2, 5, 6, 10, 11, 16 and
+# T-PSH-2, 3, 5 and 7.
+GIT_ORACLE = {
+    "NONE": (
+        NONE4,
+        [
+            "git status",
+            "git diff",
+            "git log --oneline",
+            "git add -A",
+            "git stash",
+            "git rebase origin/master",
+            "git fetch origin",
+            "git remote get-url origin",
+            "git merge-tree a b",
+            "git update-ref refs/superclaude/implement/p/T1 abc123",
+            "git -C /x status",
+            "NAME=x git status",
+            "git --attr-source HEAD status",
+            "git status 2>&1 | tail -5",
+            'git -C "$(git rev-parse --show-toplevel)" status',
+            # Row 30: text that names git without a gated word.
+            'echo "use git for hooks"',
+            'grep -rn "git worktree" docs/',
+            "cd git-tools",
+            "grep -rn push docs/",
+            # Row 33: the pinned gaps of residual R1 (git parts).
+            "G=gi; ${G}t push origin main",
+            "$'\\x67it' push origin main",
+            "$GIT push origin main",
+            "/usr/bin/gi[t] push origin main",
+        ],
+    ),
+    "COMMIT": (
+        ("LL-COMMIT", "LL-COMMIT", "LL-COMMIT", None),
+        [
+            "git commit -m x",
+            "git commit --only -- a b",
+            "git cherry-pick x",
+            "git revert x",
+            "git am p.patch",
+            "git commit-tree t",
+            "git update-ref refs/heads/f abc123",
+            "git update-ref HEAD abc123",
+            "sudo git commit -m x",
+            'sh -c "git commit -m x"',
+            "git bisect run git commit",
+            'A=">" git commit -m x',
+            "git$'' commit --allow-empty -m x",
+            'echo "git commit"',
+            'git status && echo "I am done"',
+            MULTILINE.format(line="use git for hooks"),
+        ],
+    ),
+    "PUSH": (
+        PUSH_OK,
+        [
+            "git push origin 3f2a9c1e:feature",
+            "git push -u origin feature:feature",
+            "git push origin feature",
+            "git push --set-upstream origin feature",
+        ],
+    ),
+    "PUSHFORM": (
+        PUSHFORM,
+        [
+            "git push",
+            "git push origin",
+            "git push origin HEAD",
+            "git push origin x:@",
+            "git push upstream a:b",
+            "git push --repo=x a:b",
+            "git push origin a:$B",
+            "git push origin a:b 2>&1",
+            "git push origin f 2>&1 | tail -5",
+            "cd x && git push origin a:b",
+            "git push origin a:b `echo c:main`",
+            "git push origin a:b \\\nc:main",
+            "git-push origin feature",
+            "/usr/lib/git-core/git-push origin main",
+            "git push --force origin f",
+            "git push origin +f:f",
+            "git push --all",
+            "git push --mirror",
+            "git push --receive-pack=x origin a:b",
+            "git push --exec=x origin a:b",
+            "git push origin --all",
+            "git push origin --mirror",
+            "git push origin -f",
+            "git push origin x:--all",
+            "git --attr-source HEAD push origin main",
+            "echo f:main | xargs git push origin f:f",
+            'A=">" git push origin HEAD:main',
+            'git -c "x.y=a status" push origin HEAD:main',
+            'git rebase -x "git push origin main" main',
+            "git commit -m x && git push origin f",
+            "timeout 30 git push origin main",
+            "GIT=git; $GIT push origin main",
+            "$'git' push origin main",
+            "git$'' push origin HEAD:main",
+            'g$""it push origin HEAD:main',
+            "timeout -s KILL 30 git send-pack /tmp/r.git HEAD:refs/heads/main",
+            "taskset -c 0 git send-pack /tmp/r.git HEAD:refs/heads/main",
+            "find . -maxdepth 0 -exec git send-pack /tmp/r.git HEAD:refs/heads/main \\;",
+            "git rebase -x 'git send-pack /tmp/r.git HEAD:refs/heads/main' HEAD~1",
+            # Row 32: pinned G1 over-match on text.
+            'git commit -m "explain git push"',
+            MULTILINE.format(line="git push origin main is never run"),
+            "git log --grep push",
+            "git log --oneline | grep push",
+        ],
+    ),
+    "PROTECTED": (
+        PROTECTED,
+        [
+            "git push origin main",
+            "git push origin x:main",
+            "git push origin x:refs/heads/master",
+            "git push origin x:heads/main",
+            "git push -u origin feature:main",
+        ],
+    ),
+    "MERGE": (
+        MERGE,
+        [
+            "git merge x",
+            "git merge --abort",
+            "git pull",
+            "git pull --rebase",
+            "git -c merge.conflictStyle=zdiff3 merge --no-commit --no-ff abc123",
+            "git-merge x",
+            "git$'' merge other --no-edit",
+            "git log --grep merge",  # row 32a
+        ],
+    ),
+    "UNKNOWN": (
+        UNK,
+        [
+            "git ci",
+            "git -c alias.ci=commit ci",
+            "X=commit git --config-env=alias.ci=X ci",
+            "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1",
+            "Q=sh git rebase -x 'git pu$Q origin HEAD:main' HEAD~1",
+            "git rebase -x 'git `echo pu`sh origin HEAD:main' HEAD~1",
+            "git $(echo push) origin a:b",
+            "cmd=push; git $cmd",
+            "printf x | xargs git",
+            "git notes add",
+            "git worktree add",
+            "git remote set-url origin u",
+            "git config alias.ci commit",
+            'git -C "/dir with space" push',
+            "git-lfs push",
+            "$(git --exec-path)/git-push origin main",
+            "gi\\\nt push origin HEAD:main",
+            "if true; then git send-pack /tmp/r.git HEAD:refs/heads/main; fi",
+            "env -u FOO git config remote.origin.push refs/heads/feature:refs/heads/main",
+            "flock /tmp/l git config remote.origin.push refs/heads/feature:refs/heads/main",
+            "sudo -u coder git remote set-url --push origin https://github.com/evil/x",
+            # Row 31: pinned over-match in command position.
+            MULTILINE.format(line="git hooks run on save"),
+            "git \\\ncommit -m x",
+            "git config --get-regexp alias.",
+        ],
+    ),
+}
+
+
+def _git_params(prefix: str, rows):
+    for i, (command, ids) in enumerate(rows):
+        for level, msg_id in zip(LEVEL_ORDER, ids):
+            yield pytest.param(command, level, msg_id, id=f"{prefix}{i}-{level}")
+
+
+def _git_case(tmp_path, command, level, msg_id):
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_bash(command), tmp_path)
+    _assert_decision(result, tmp_path, msg_id, level, text=msg_id is not None)
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        p
+        for cls, (ids, commands) in GIT_ORACLE.items()
+        for p in _git_params(f"{cls}-", [(c, ids) for c in commands])
+    ],
+)
+def test_git_grid_oracle(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize(
+    "command",
+    [
+        "/usr/bin/env git ci",
+        "/usr/bin/sudo git worktree add x",
+        '/bin/bash -c "git ci"',
+        "/usr/bin/timeout 30 git notes add",
+        "env git ci",
+    ],
+    ids=["env", "sudo", "bash-c", "timeout", "bare-env"],
+)
+def test_git_wrapper_matched_by_basename(tmp_path, level, command):
+    # NM7 / G3: a path-qualified wrapper or shell is still a wrapper, so the git
+    # word after it is in command position and its UNKNOWN-class subcommand blocks.
+    _git_case(tmp_path, command, level, "LL-UNKNOWN")
+
+
+# T-GIT-1, 3, 7, 8, 9, 12, 13, 14, 15 and 18: the cases the oracle rows above do
+# not already hold.
+GIT_NAMED = [
+    # T-GIT-1: read or local git commands of /sc:implement and /sc:pr-submit.
+    *[
+        (c, NONE4)
+        for c in (
+            "git rev-parse HEAD",
+            "git rev-parse --show-toplevel",
+            "git show --stat HEAD",
+            "git branch --show-current",
+            "git diff --cached --name-only",
+            "git status --porcelain",
+            "git log -1 --format=%H",
+            "git rev-list --count origin/master..HEAD",
+            "git merge-base HEAD origin/master",
+            "git worktree list",
+            "git config --get user.name",
+            "git remote -v",
+            "git ls-files -m",
+            "git restore --staged a",
+            "git checkout -- a",
+            "git reset --hard HEAD",
+            "git cat-file -t HEAD",
+            "git fetch origin master",
+        )
+    ],
+    # T-GIT-3: the three alias forms of fact T2.
+    (
+        "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.ci GIT_CONFIG_VALUE_0=commit git ci",
+        UNK,
+    ),
+    # T-GIT-7: update-ref.
+    ('git update-ref "$ref" "$sha"', NONE4),
+    ("git update-ref refs/heads/x abc123", COMMIT),
+    ("git update-ref --stdin", COMMIT),
+    # T-GIT-8: nested git words.
+    ('git commit -m "fix git handling"', COMMIT),
+    # T-GIT-9: wrappers; a wrapped commit is COMMIT, a wrapped push PUSHFORM.
+    *[
+        (w.format(c="git commit -m x"), COMMIT)
+        for w in (
+            'bash -c "{c}"',
+            'sh -c "{c}"',
+            "env {c}",
+            "command {c}",
+            "exec {c}",
+            "sudo {c}",
+            "nohup {c}",
+            "timeout 30 {c}",
+            "xargs {c}",
+            "/usr/bin/{c}",
+            "NAME=x {c}",
+        )
+    ],
+    ("git -C /x commit -m x", COMMIT),
+    *[
+        (w.format(c="git push origin main"), PUSHFORM)
+        for w in (
+            'bash -c "{c}"',
+            'sh -c "{c}"',
+            "env {c}",
+            "command {c}",
+            "exec {c}",
+            "sudo {c}",
+            "nohup {c}",
+            "xargs {c}",
+            "/usr/bin/{c}",
+            "NAME=x {c}",
+        )
+    ],
+    ("git -C /x push origin main", PUSHFORM),
+    ("python -c \"subprocess.run(['git','push','origin','main'])\"", PUSHFORM),
+    # T-GIT-12: dashed builtins.
+    ("git-commit -m x", COMMIT),
+    ("cat docs/git-workflow.md", NONE4),
+    # T-GIT-13: the message text passed by file.
+    ("git commit -F msg.txt", COMMIT),
+    # T-GIT-14: T-ATK-11, 12, 34 (10, 35 and 36 are oracle rows).
+    ("git status \\\\\ngit -c alias.p=push p origin HEAD:main", UNK),
+    ("git bisect run git -c alias.c=commit c", UNK),
+    ("X=sh git rebase -x 'git -c alias.p=pu$X p origin HEAD:main' HEAD~1", UNK),
+    # T-GIT-15.
+    ("git -C 'a b' push origin HEAD:main", UNK),
+    # T-GIT-18: N-ATK-8 (5, 6, 9 to 13 and 37 are oracle rows).
+    (
+        "if true; then git config remote.origin.push"
+        " refs/heads/feature:refs/heads/main; fi",
+        UNK,
+    ),
+    ("flock /tmp/l git send-pack /tmp/r.git HEAD:refs/heads/main", PUSHFORM),
+]
+
+
+@pytest.mark.parametrize("command, level, msg_id", list(_git_params("g", GIT_NAMED)))
+def test_git_named_cases(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+def test_git_alias_cannot_shadow_builtin(tmp_path):
+    # T-GIT-4: the hook calls the command UNKNOWN, and real git runs status, not commit.
+    git = shutil.which("git")
+    if git is None:
+        pytest.skip("git is not installed")
+    repo = tmp_path / "repo"
+    repo.mkdir()
+    env = {
+        "HOME": str(tmp_path),
+        "PATH": os.environ.get("PATH", ""),
+        "GIT_CONFIG_NOSYSTEM": "1",
+        "GIT_CONFIG_GLOBAL": os.devnull,
+    }
+
+    def run(*args):
+        return subprocess.run(
+            [git, "-c", "user.name=t", "-c", "user.email=t@t", *args],
+            cwd=repo,
+            env=env,
+            capture_output=True,
+            timeout=30,
+        )
+
+    assert run("init", "-q").returncode == 0
+    (repo / "a").write_text("x")
+    assert run("add", "a").returncode == 0
+    assert run("-c", "alias.status=commit", "status").returncode == 0
+    assert run("rev-parse", "--verify", "-q", "HEAD").returncode != 0
+    command = "git -c alias.status=commit status"
+    for level in LEVEL_ORDER:
+        _git_case(tmp_path / level, command, level, "LL-UNKNOWN")
+
+
+def _retry_block() -> str:
+    # Extracted as tests/skills/test_implement_retry_revert.py extracts it.
+    text = (
+        ROOT / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
+    ).read_text()
+    blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
+    return next(b for b in blocks if "sc_retry_revert()" in b)
+
+
+@pytest.mark.parametrize("level", ["WA", "F"])
+@pytest.mark.parametrize(
+    "command",
+    [
+        "retry",
+        'git update-ref "refs/superclaude/implement/p/T1" "$start"',
+        'idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && '
+        'GIT_INDEX_FILE="$idx" git add -A && '
+        'start=$(GIT_INDEX_FILE="$idx" git write-tree); rm -f "$idx"',
+        'git -C "$(git rev-parse --show-toplevel)" status',
+    ],
+    ids=["retry-block", "T-OK-21", "T-OK-22", "toplevel"],
+)
+def test_implement_git_blocks_allowed(tmp_path, command, level):
+    # T-GIT-17 [B-10].
+    if command == "retry":
+        command = _retry_block()
+    _git_case(tmp_path, command, level, None)
+
+
+# T-PSH-11 and T-PSH-12: the named push cases of FR-L-33 and FR-L-34.
+PUSH_ACCEPT = [
+    "git push origin feature",
+    "git push -u origin feature",
+    "git push --set-upstream origin feature",
+    "git push origin 3f2a9c1e:feature/x",
+    "git push origin feature:feature",
+    "git push origin feature/main:feature/main",
+    "git push origin HEAD:feature",
+    "git push origin fix-394.v2",
+    "  git push origin feature  ",
+    "git push origin a:refs/heads/feature",
+    "git push origin release_1.2",
+    "git push origin feature\n",
+    "git push origin refs/heads/heads/main",
+]
+PUSH_REJECT = [
+    "git push origin a:b `echo c:main`",
+    "git push origin a:b \\\n c:main",
+    "git-push origin main",
+    "/usr/lib/git-core/git-push origin feature",
+    "git push origin +feature:feature",
+    "git push --force origin feature",
+    "git push --all origin",
+    "git -c remote.origin.push=refs/heads/f:refs/heads/main push origin f",
+    "git --config-env=remote.origin.push=V push origin f",
+    "git push origin 'feature:ma''in'",
+    "git push origin a:$(echo main)",
+    "git push origin a:$B",
+    "git push upstream feature",
+    "git push origin a:b 2>&1",
+    "cd x && git push origin a:b",
+    "git push origin a:b; git push origin c:main",
+    "git push origin :feature",
+    "git push origin a:b c:main",
+    "GIT_CONFIG_COUNT=1 git push origin f",
+    "git push origin a:b\ngit push origin c:main",
+    "git  push origin feature",
+    "echo feat:main | xargs git push origin feat:feat",
+    "git push origin HEAD",
+    "git push origin --all",
+    "git push origin --mirror",
+    "git push origin -f",
+    "git push origin x:--all",
+    "git push origin --delete",
+    "git push origin ..",
+    "git push origin x:@",
+]
+PUSH_PROTECTED = [
+    "git push origin main",
+    "git push origin x:refs/heads/master",
+    "git push origin x:heads/main",
+    "git push origin heads/main",
+    "git push -u origin feature:main",
+]
+# T-PSH-4, 6, 8 (Bash parts; the Write is Task 9) and 10.
+PUSH_NAMED = [
+    ("git push origin +main", PUSHFORM),
+    ("git push origin :main", PUSHFORM),
+    ("git push -o ci.skip origin a:b", PUSHFORM),
+    (
+        "git -c remote.origin.push=refs/heads/feature:refs/heads/main"
+        " push origin feature",
+        UNK,
+    ),
+    ("git config remote.origin.push x", UNK),
+    ("git push --force-with-lease origin a:b", PUSHFORM),
+    ("git push -f origin a:b", PUSHFORM),
+    ("git push origin +a:b", PUSHFORM),
+]
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        *_git_params("PA", [(c, PUSH_OK) for c in PUSH_ACCEPT]),
+        *_git_params("PD", [(c, PROTECTED) for c in PUSH_PROTECTED]),
+        *_git_params("PSH", PUSH_NAMED),
+    ],
+)
+def test_push_named_cases(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize(
+    "command", PUSH_REJECT, ids=[f"PR{i}" for i in range(1, len(PUSH_REJECT) + 1)]
+)
+def test_push_form_reject_cases(tmp_path, command, level):
+    # T-PSH-12: LL-PUSH-FORM or LL-UNKNOWN at FS, LL-PUSH or LL-UNKNOWN below.
+    _bind(tmp_path, *LEVEL_FILES[level])
+    result = _run(_bash(command), tmp_path)
+    store = str(_store(tmp_path / "home"))
+    note = _design_note("LL-TEXT") + "\n"
+    ids = ("LL-PUSH-FORM" if level == "FS" else "LL-PUSH", "LL-UNKNOWN")
+    assert (result.returncode, result.stdout) == (2, b"")
+    assert result.stderr.decode() in {
+        _expected(i, LEVELS[level], SID, store) + note for i in ids
+    }

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log
index 650cedd8..08a0a35c 100644
--- a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t7-test.log
@@ -1,7 +1,5 @@
-$ uv run pytest tests/hooks/test_launch_level_guard.py -k "GIT or PSH or git or push" -q
-==================== 1021 passed, 459 deselected in 18.72s =====================
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "GIT or PSH or git or push" -q  (after the fix pass)
+
+==================== 1041 passed, 459 deselected in 19.04s =====================
 $ uv run pytest tests/hooks/test_launch_level_guard.py -q
-====================== 1444 passed, 36 xfailed in 26.68s =======================
-remaining xfails: 36, all name Task 8 or 9; XPASS: 0
-bash -n: OK; grep -c .claude/state: 0; ruff check/format: clean
-timing (FS, 50 runs each): git status 14.5 ms/run; git push origin feature 14.8 ms/run
+====================== 1464 passed, 36 xfailed in 27.66s =======================
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index aa2f8536..d2a6c376 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -433,8 +433,10 @@ if [ "$LL_BRANCH" = tool ]; then
                     for ((i = 0; i < ${#ws[@]}; i++)); do
                         w=${ws[i]}
                         if [ "$LL_CP" = -1 ]; then
-                            case $w in
-                            -* | env | sudo | nohup | exec | command | builtin | timeout | xargs | setsid | time | nice | stdbuf | ionice | doas | unbuffer | eval | if | then | else | elif | do | while | until | coproc) continue ;;
+                            case $w in -*) continue ;; esac
+                            LL_B=${w##*/} # wrappers and shells match by basename (NM7)
+                            case $LL_B in
+                            env | sudo | nohup | exec | command | builtin | timeout | xargs | setsid | time | nice | stdbuf | ionice | doas | unbuffer | eval | if | then | else | elif | do | while | until | coproc) continue ;;
                             bash | sh | zsh | dash | ksh)
                                 if [[ ${ws[i + 1]:-} =~ ^-[a-z]*c$ ]]; then
                                     i=$((i + 1))
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index e23cf98d..9aa07070 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1888,6 +1888,24 @@ def test_git_grid_oracle(tmp_path, command, level, msg_id):
     _git_case(tmp_path, command, level, msg_id)
 
 
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+@pytest.mark.parametrize(
+    "command",
+    [
+        "/usr/bin/env git ci",
+        "/usr/bin/sudo git worktree add x",
+        '/bin/bash -c "git ci"',
+        "/usr/bin/timeout 30 git notes add",
+        "env git ci",
+    ],
+    ids=["env", "sudo", "bash-c", "timeout", "bare-env"],
+)
+def test_git_wrapper_matched_by_basename(tmp_path, level, command):
+    # NM7 / G3: a path-qualified wrapper or shell is still a wrapper, so the git
+    # word after it is in command position and its UNKNOWN-class subcommand blocks.
+    _git_case(tmp_path, command, level, "LL-UNKNOWN")
+
+
 # T-GIT-1, 3, 7, 8, 9, 12, 13, 14, 15 and 18: the cases the oracle rows above do
 # not already hold.
 GIT_NAMED = [

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:437 anchor="one of the wrapper basenames `env sudo nohup exec" chk=n,n,n,y family=g3-wrapper-basename fix=match wrappers and shells by ${w##*/} and add oracle rows for path-qualified wrappers covers="one of the wrapper basenames `env sudo nohup exec" first=A1 origin=new: the wrapper and shell skip compared the raw word, so /usr/bin/env git ci escaped the UNKNOWN class.

Saved-probe re-check hit locations (may be empty): 437:                            LL_B=${w##*/} # wrappers and shells match by basename (NM7)
438:                            case $LL_B in


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
