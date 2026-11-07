b6b47cc0ea49c7d90d4925c73e3502c94c740339
Review one task for spec compliance.

Task brief: ## Task 8: Implement gh, curl and API classification

Depends on: Task 7

In src/superclaude/hooks/scripts/launch-level-guard.sh add the gh rules of design section 5.1 (FR-L-35 to FR-L-39): H1 group and action words (skipping -R and --repo values), H2 the gh api rule (GHWRITE unless the raw command matches the anchored read-only expression, no word after api matches the method, field or input options, and the endpoint exists, is not graphql and does not end /merge or /merges), H3 the first-match table (api no class; help or version NONE; merge, update-branch and sync give MERGE anywhere; alias and extension groups and any dollar sign give UNKNOWN; the read-only groups and actions give NONE; pr create, pr edit, pr comment, pr ready, issue create, issue edit and issue comment give SUBMIT anywhere; else UNKNOWN in command position), H4 each recognized pr create occurrence needs a nonempty operand after -R or --repo (or --repo=value) in its own segment, otherwise REPO, and H5 when no gh word is present a word with repos/ ending /merge or /merges gives MERGE and a word containing api.github.com or uploads.github.com gives GHWRITE. Print the LL-TEXT note when the class came from Bash or Monitor text.

Extend tests/hooks/test_launch_level_guard.py with the T-GH cases of MR section 8.2 and the oracle rows for SUBMIT, REPO and GHWRITE across the four levels.

Acceptance criteria:
- gh api repos/o/r/pulls/5 --jq .state exits 0 at every level; gh api -X POST repos/o/r/merges, gh api graphql with any query, and curl -X PATCH https://api.github.com/repos/o/r exit 2 with LL-GH-WRITE at every level.
- gh pr create --repo o/r --title x exits 2 with LL-SUBMIT at W, WA and F and 0 at FS; gh pr create --title x exits 2 with LL-REPO at FS.
- gh pr merge 5 and gh repo sync exit 2 with LL-MERGE at every level; gh pr view 5 and gh pr checks exit 0.
- gh alias set co with a merge value exits 2 with LL-UNKNOWN.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "GH or gh" -v passes.

AC ids (source order):
T8.AC1: gh api repos/o/r/pulls/5 --jq .state exits 0 at every level; gh api -X POST repos/o/r/merges, gh api graphql with any query, and curl -X PATCH https://api.github.com/repos/o/r exit 2 with LL-GH-WRITE at every level.
T8.AC2: gh pr create --repo o/r --title x exits 2 with LL-SUBMIT at W, WA and F and 0 at FS; gh pr create --title x exits 2 with LL-REPO at FS.
T8.AC3: gh pr merge 5 and gh repo sync exit 2 with LL-MERGE at every level; gh pr view 5 and gh pr checks exit 0.
T8.AC4: gh alias set co with a merge value exits 2 with LL-UNKNOWN.
T8.AC5: uv run pytest tests/hooks/test_launch_level_guard.py -k "GH or gh" -v passes.
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
Start sha: b6b47cc0ea49c7d90d4925c73e3502c94c740339
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t8-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t8-test.log
new file mode 100644
index 00000000..ad34601c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t8-test.log
@@ -0,0 +1,8 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "GH or gh" -q
+==================== 635 passed, 1490 deselected in 11.74s =====================
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q
+====================== 2101 passed, 24 xfailed in 38.59s =======================
+$ bash -n src/superclaude/hooks/scripts/launch-level-guard.sh
+syntax ok
+$ grep -c '.claude/state' src/superclaude/hooks/scripts/launch-level-guard.sh
+0
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
index d2a6c376..6262f9f6 100755
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -5,8 +5,8 @@
 # with a message on stderr; never exit 1, no onFailure. Only a session that the
 # claim script launched (a valid top-level session_id bound in the store) is
 # governed; every other session is ordinary and never blocked (FR-L-53).
-# Ten-part layout (DD-1); Tasks 5 to 7 classify Skill, BIG, NM1a and git (G0 to
-# G4, canonical push); anything else is NONE until Tasks 8 to 10.
+# Ten-part layout (DD-1); Tasks 5 to 8 classify Skill, BIG, NM1a, git (G0-G4,
+# push) and gh, curl, API text (H1-H5); the rest is NONE until Tasks 9 and 10.
 # launch-level-guard-version: 1
 
 # 1. Settings
@@ -412,10 +412,49 @@ if [ "$LL_BRANCH" = tool ]; then
             # segs: the segments of W; a segment's words are ws=($seg) under set -f, and (NM7) a word's basename is ${w##*/}.
             IFS=';' read -r -a segs <<<"$W"
             # <<< normalise
-            # Git (FR-L-28 to FR-L-34): G1 and G2 test G; G3 and G4 read the
-            # words of each segment; then the canonical push check on raw cmd.
+            # Git (FR-L-28 to FR-L-34) and gh (FR-L-35 to FR-L-39): G1, G2 and
+            # H2 test G; G3, G4, H1, H3, H4 and H5 read the words of each
+            # segment; then the canonical push check on raw cmd.
             LL_RE='( |/)git(-[a-z][a-z-]*)? '
-            if [[ $G =~ $LL_RE ]]; then
+            LL_GIT=0
+            [[ $G =~ $LL_RE ]] && LL_GIT=1
+            LL_RE='( |/)gh '
+            LL_GH=0
+            [[ $G =~ $LL_RE ]] && LL_GH=1
+            # H5 can only fire when G (lower case) holds one of these texts.
+            LL_URL=0
+            case $G in *repos/* | *api.github.com* | *uploads.github.com*) LL_URL=1 ;; esac
+            if [ "$LL_GH" = 1 ] && [[ $G == *' api '* ]]; then
+                # H2: a gh word and the word api anywhere is GHWRITE unless the
+                # raw cmd is one plain GET: the anchored form, no method, field
+                # or input word, and an endpoint that is not graphql or a merge.
+                LL_RE='^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$'
+                LL_RE_W='^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$'
+                LL_OK=0
+                if [[ $cmd =~ $LL_RE ]]; then
+                    ws=($cmd) # the form admits no glob, quote or separator
+                    LL_OK=1 LL_EP= LL_V=0
+                    for ((i = 2; i < ${#ws[@]}; i++)); do
+                        w=${ws[i]}
+                        if [[ $w =~ $LL_RE_W ]]; then
+                            LL_OK=0
+                            break
+                        fi
+                        if [ "$LL_V" = 1 ]; then
+                            LL_V=0
+                            continue
+                        fi
+                        case $w in
+                        -H | --header | -q | --jq | -t | --template | --hostname | -p | --preview | --cache) LL_V=1 ;;
+                        -*) ;;
+                        *) [ -n "$LL_EP" ] || LL_EP=$w ;;
+                        esac
+                    done
+                    case ${LL_EP,,} in '' | graphql | */merge | */merges) LL_OK=0 ;; esac
+                fi
+                [ "$LL_OK" = 1 ] || LL_CLASSES+='GHWRITE '
+            fi
+            if [ "$LL_GIT" = 1 ]; then
                 LL_RE='( |/git-| git-)(merge|pull) '
                 [[ $G =~ $LL_RE ]] && LL_CLASSES+='MERGE '
                 LL_RE='( |/git-| git-)(push|send-pack|http-push) '
@@ -424,12 +463,15 @@ if [ "$LL_BRANCH" = tool ]; then
                 [[ $G =~ $LL_RE ]] && LL_CLASSES+='COMMIT '
                 LL_RE='alias\.|pushurl|insteadof|hookspath| (remote|url|include|includeif)\.| set-url '
                 [[ $G =~ $LL_RE ]] && LL_CLASSES+='UNKNOWN '
+            fi
+            if [ "$LL_GIT$LL_GH$LL_URL" != 000 ]; then
                 LL_RE_NAME='^[A-Za-z_][A-Za-z0-9_]*='
                 LL_RE_NUM='^[0-9]+(\.[0-9]+)?[smhd]?$'
                 LL_RE_DASH='^git-[a-z][a-z-]*$'
                 for seg in "${segs[@]}"; do
                     ws=($seg)
                     LL_CP=-1 # index of the command-position word, -1 while skipping
+                    LL_SGH=0 LL_H5= # a gh word in this segment; its H5 classes
                     for ((i = 0; i < ${#ws[@]}; i++)); do
                         w=${ws[i]}
                         if [ "$LL_CP" = -1 ]; then
@@ -446,7 +488,58 @@ if [ "$LL_BRANCH" = tool ]; then
                             [[ $w =~ $LL_RE_NAME || $w =~ $LL_RE_NUM ]] && continue
                             LL_CP=$i
                         fi
+                        if [ "$LL_URL" = 1 ]; then
+                            # H5: a merge endpoint or a GitHub API host in any word.
+                            LL_LW=${w,,}
+                            if [[ $LL_LW == *repos/* && ($LL_LW == */merge || $LL_LW == */merges) ]]; then
+                                LL_H5+='MERGE '
+                            fi
+                            case $LL_LW in *api.github.com* | *uploads.github.com*) LL_H5+='GHWRITE ' ;; esac
+                        fi
                         b=${w##*/}
+                        if [ "$b" = gh ]; then
+                            # H1: group and action, skipping -R and --repo values.
+                            LL_SGH=1 LL_GG= LL_GA= LL_HV=0
+                            for ((j = i + 1; j < ${#ws[@]}; j++)); do
+                                case ${ws[j]} in
+                                -R | --repo) j=$((j + 1)) ;;
+                                --version | --help) LL_HV=1 ;;
+                                -*) ;;
+                                *)
+                                    if [ -z "$LL_GG" ]; then
+                                        LL_GG=${ws[j]}
+                                    else
+                                        LL_GA=${ws[j]}
+                                        break
+                                    fi ;;
+                                esac
+                            done
+                            # G4: a repo option that ends the segment has no value.
+                            case ${ws[${#ws[@]} - 1]} in -R | --repo) LL_CLASSES+='UNKNOWN ' ;; esac
+                            # H3, first match wins (the space cannot occur in a word).
+                            case "$LL_GG $LL_GA" in
+                            'api '*) ;;
+                            ' ') [ "$LL_HV" = 1 ] || [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
+                            *' merge' | *' update-branch' | *' sync') LL_CLASSES+='MERGE ' ;;
+                            'alias '* | 'extension '* | *'$'*) LL_CLASSES+='UNKNOWN ' ;;
+                            'search '* | 'status '* | 'auth '* | 'browse '* | 'help '* | 'completion '*) ;;
+                            *' view' | *' list' | *' status' | *' diff' | *' checks' | *' watch' | *' checkout') ;;
+                            'pr create' | 'pr edit' | 'pr comment' | 'pr ready' | 'issue create' | 'issue edit' | 'issue comment') LL_CLASSES+='SUBMIT ' ;;
+                            *) [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN ' ;;
+                            esac
+                            # H4: each pr create needs a nonempty repo operand in its own segment.
+                            if [ "$LL_GG $LL_GA" = 'pr create' ]; then
+                                LL_RP=0
+                                for ((j = 0; j < ${#ws[@]}; j++)); do
+                                    case ${ws[j]} in
+                                    -R | --repo) [[ -n ${ws[j + 1]:-} && ${ws[j + 1]} != -* ]] && LL_RP=1 ;;
+                                    --repo=?*) LL_RP=1 ;;
+                                    esac
+                                done
+                                [ "$LL_RP" = 1 ] || LL_CLASSES+='REPO '
+                            fi
+                            continue
+                        fi
                         case $b in git) ;; git-*) [[ $b =~ $LL_RE_DASH ]] || continue ;; *) continue ;; esac
                         # S: the dashed name, or the first non-option word after git.
                         LL_S= LL_SI=$i LL_HV=0 LL_LV= LL_DG=0
@@ -492,6 +585,7 @@ if [ "$LL_BRANCH" = tool ]; then
                         *) LL_CLASSES+='UNKNOWN ' ;;
                         esac
                     done
+                    [ "$LL_SGH" = 1 ] || LL_CLASSES+=$LL_H5 # H5 only where no gh word is
                 done
                 # Canonical push (FR-L-33, FR-L-34): only one plain git push to origin passes.
                 case $LL_CLASSES in
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 9aa07070..49830d10 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -1213,10 +1213,10 @@ def test_notes_follow_the_lines_state_first(tmp_path):
 
 # --- Task 6: Bash and Monitor normalisation (T-NRM, T-FC-7) ----------------
 #
-# Cases whose class needs a Task 8 or 9 classifier (gh, tamper, escape) are
-# pinned end to end with a strict xfail naming that task, so the task that
-# reaches the class must drop the mark (Task 7, git, has dropped its marks). "?" marks a level that the T-NRM row
-# does not pin.
+# Cases whose class needs a Task 9 classifier (tamper, escape) are pinned end
+# to end with a strict xfail naming that task, so the task that reaches the
+# class must drop the mark (Tasks 7 and 8, git and gh, have dropped theirs).
+# "?" marks a level that the T-NRM row does not pin.
 
 LEVEL_ORDER = ("W", "WA", "F", "FS")
 UNK = ("LL-UNKNOWN",) * 4
@@ -1243,12 +1243,12 @@ NRM_E2E = [
     ("natk15", "git$'' -c x.y=z push origin HEAD:main", PUSH, None),
     ("natk16", "git$'' merge other --no-edit", MERGE, None),
     ("natk18", "git$'' commit --allow-empty -m x", COMMIT, None),
-    ("natk23", "g$''h pr merge 5", MERGE, 8),
+    ("natk23", "g$''h pr merge 5", MERGE, None),
     (
         "natk24",
         "flock /tmp/l gh a$''pi -X DELETE repos/o/r/git/refs/heads/main",
         GHWRITE,
-        8,
+        None,
     ),
     ("natk30", f"rm -rf {STATE_PATH.replace('cla', 'cla$' + chr(39) * 2)}", TAMPER, 9),
     ("natk32", "cp /tmp/s.json ~/.claude/set$''tings.json", TAMPER, 9),
@@ -1266,7 +1266,7 @@ NRM_E2E = [
     # T-NRM-4: \/ escapes in a tamper path.
     ("nrm4-escaped-slash", "cp x ~\\/.claude\\/\\/.\\/settings.json", TAMPER, 9),
     # T-NRM-5: a continuation is not joined.
-    ("nrm5-gh-api", "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main", GHWRITE, 8),
+    ("nrm5-gh-api", "gh api \\\n-X PATCH repos/o/r/git/refs/heads/main", GHWRITE, None),
     ("nrm5-push", "git push origin a:b \\\nc:main", FS_ONLY + ("LL-PUSH-FORM",), None),
     (
         "nrm5-double-backslash",
@@ -1274,11 +1274,14 @@ NRM_E2E = [
         UNK,
         None,
     ),
+    # Design H4 overrides MR row 21 and T-NRM-5 (design section 11, "nonempty
+    # PR repo operands"): the repo operand must sit in the pr create segment,
+    # and the newline ends that segment, so FS gets LL-REPO, not an allow.
     (
         "nrm5-pr-create",
         'gh pr create \\\n--repo "$REPO" --title x --body y',
-        FS_ONLY + (None,),
-        8,
+        ("LL-SUBMIT",) * 3 + ("LL-REPO",),
+        None,
     ),
     ("nrm5-claude", "claude \\\n-p x", ESCAPE, 9),
     ("nrm5-git-space", "git \\\ncommit -m x", UNK, None),
@@ -1695,8 +1698,8 @@ PUSHFORM = ("LL-PUSH", "LL-PUSH", "LL-PUSH", "LL-PUSH-FORM")  # PUSH and PUSHFOR
 PROTECTED = ("LL-PROTECTED",) * 4
 MULTILINE = "git commit -m \"$(cat <<'EOF'\nfeat: x\n{line}\nEOF\n)\""
 
-# Grid rows 12 to 18 and 30 to 33 of MR section 8.1, git parts only (gh, curl
-# and MCP parts belong to Task 8). They cover T-GIT-2, 5, 6, 10, 11, 16 and
+# Grid rows 12 to 18 and 30 to 33 of MR section 8.1, git parts only (gh and
+# curl parts are in GH_ORACLE below; MCP belongs to Task 9). They cover T-GIT-2, 5, 6, 10, 11, 16 and
 # T-PSH-2, 3, 5 and 7.
 GIT_ORACLE = {
     "NONE": (
@@ -2166,3 +2169,335 @@ def test_push_form_reject_cases(tmp_path, command, level):
     assert result.stderr.decode() in {
         _expected(i, LEVELS[level], SID, store) + note for i in ids
     }
+
+
+# --- Task 8: gh, curl and API text (H1 to H5; FR-L-35 to FR-L-39) -----------
+#
+# Each tuple below is written by hand from the grid (design section 8; MR
+# section 8.1 rows 18 to 22), not taken from the script's case statement.
+
+SUBMIT = ("LL-SUBMIT", "LL-SUBMIT", "LL-SUBMIT", None)
+SUBMIT_REPO = ("LL-SUBMIT", "LL-SUBMIT", "LL-SUBMIT", "LL-REPO")
+REPO_FLAG = '--repo "$REPO"'
+
+GH_ORACLE = {
+    "NONE": (
+        NONE4,
+        [
+            # Row 19 and the FR-L-36 consequences.
+            "gh pr view 5 --json mergeable,mergeStateStatus",
+            "gh issue view 5",
+            "gh pr checks 5",
+            "gh pr checks",
+            "gh repo view",
+            "gh pr view 5",
+            "gh api repos/o/r/pulls/5",
+            "gh api repos/o/r/pulls/5 --jq .state",
+            "gh api repos/o/r/commits/abc123/check-runs --jq .total_count",
+            "gh api repos/o/r/pulls -H Accept:application/json --paginate -i --silent -q .total_count",
+            "gh api --hostname github.com repos/o/r/pulls",
+            "gh --version",
+            "gh --help",
+            "gh auth status",
+            "gh -R o/r pr list",
+            'echo "use gh to view"',
+            # Residual R17 (N-ATK-36): a gh word out of command position.
+            "flock /tmp/l gh mm 5",
+        ],
+    ),
+    "SUBMIT": (
+        SUBMIT,
+        [
+            # Row 20 and row 21.
+            "gh issue create",
+            "gh issue comment 5",
+            "gh issue edit 5",
+            "gh pr comment 5",
+            "gh pr edit 5",
+            "gh pr ready 5",
+            f"gh pr create {REPO_FLAG} --base master --head f",
+            "gh pr create -R o/r --title x",
+            "gh pr create --repo=o/r --title x",
+            "gh pr create --repo o/r --title x",
+            "gh -R o/r pr create --title x",
+            f'gh pr create {REPO_FLAG} --base master --head f --title "docs: explain git hooks" --body "x"',
+        ],
+    ),
+    "REPO": (
+        SUBMIT_REPO,
+        [
+            # Row 22 and the H4 operand rules.
+            "gh pr create --title x",
+            "gh pr create --repo --title x",
+            "gh pr create --repo= --title x",
+            "gh pr create -R -t x",
+            "gh issue view 5; gh pr create --title x",
+            # The operand of another segment does not count (design H4).
+            "gh pr create --title x; gh pr list --repo o/r",
+            'gh pr create \\\n--repo "$REPO" --title x --body y',
+        ],
+    ),
+    "GHWRITE": (
+        GHWRITE,
+        [
+            "gh api -X POST repos/o/r/merges",
+            "gh api graphql",
+            "gh api graphql -f query={viewer{login}}",
+            "gh api graphql -f 'query=query { viewer { login } }'",
+            "gh api repos/o/r/pulls/5/merge",
+            "gh api repos/o/r/merges",
+            "gh api --method GET repos/o/r/pulls",
+            "gh api",
+            "gh api -q .x",
+            'gh api "repos/$REPO/pulls"',
+            "gh api repos/o/r/pulls | jq .",
+            "curl -X PATCH https://api.github.com/repos/o/r",
+            "curl -sS https://api.github.com/repos/o/r/pulls",
+            "wget https://uploads.github.com/repos/o/r/releases/1/assets",
+            # O-21: the word api in a gh command's text.
+            'gh pr create --repo o/r --title "fix api docs"',
+        ],
+    ),
+    "MERGE": (
+        MERGE,
+        [
+            "gh pr merge 5",
+            "gh pr update-branch 5",
+            "gh repo sync",
+            "gh -R o/r pr merge 5 --squash",
+            "/usr/bin/gh pr merge 5",
+            "echo gh pr merge 5",
+            "curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge",
+            "curl -X POST https://api.github.com/repos/o/r/merges",
+            "wget --method=PUT example.test/repos/o/r/pulls/5/merge",
+        ],
+    ),
+    "UNKNOWN": (
+        UNK,
+        [
+            "gh alias set co 'pr merge'",
+            "gh co 5",
+            "gh extension install x",
+            "gh pr $(echo merge) 5",
+            "gh pr `echo merge` 5",
+            "gh pr close 5",
+            "gh repo delete o/r",
+            "gh release create v1",
+            "gh",
+            "gh pr create -R",
+            "echo gh alias list",
+        ],
+    ),
+}
+
+
+def _gh_params(prefix: str, rows):
+    for i, (command, ids) in enumerate(rows):
+        for level, msg_id in zip(LEVEL_ORDER, ids):
+            yield pytest.param(command, level, msg_id, id=f"gh-{prefix}{i}-{level}")
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        p
+        for cls, (ids, commands) in GH_ORACLE.items()
+        for p in _gh_params(f"{cls}-", [(c, ids) for c in commands])
+    ],
+)
+def test_gh_grid_oracle(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+# The T-GH cases of MR section 8.2, by their MR test names.
+GH_NAMED = {
+    # T-GH-1
+    "test_gh_pr_merge_every_level": [
+        (c, MERGE) for c in ("gh pr merge 5", "gh pr update-branch 5", "gh repo sync")
+    ],
+    # T-GH-2
+    "test_gh_api_merge_and_ref_writes": [
+        (c, GHWRITE)
+        for c in (
+            "gh api -X POST repos/o/r/merges -f base=main -f head=f",
+            "gh api graphql -f query='mutation { mergePullRequest(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
+            "gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
+            "gh api -X PATCH repos/o/r/git/refs/heads/main -f sha=abc -F force=true",
+            "gh api -X PUT repos/o/r/contents/x -f message=m -f content=Yg== -f branch=main",
+        )
+    ],
+    # T-GH-3
+    "test_gh_pr_create_without_repo": [("gh pr create --title x", SUBMIT_REPO)],
+    # T-GH-4
+    "test_gh_pr_create_repo_forms": [
+        (c, SUBMIT)
+        for c in (
+            f"gh pr create {REPO_FLAG} --title x",
+            "gh pr create -R o/r --title x",
+            "gh pr create --repo=o/r --title x",
+        )
+    ],
+    # T-GH-5 (row 20)
+    "test_gh_writes_need_submit": [
+        (c, SUBMIT)
+        for c in (
+            "gh issue create",
+            "gh issue comment 5",
+            "gh pr comment 5",
+            "gh pr edit 5",
+            "gh pr ready 5",
+        )
+    ],
+    # T-GH-6 (O-3)
+    "test_gh_pr_ready_submit_class": [("gh pr ready 5", SUBMIT)],
+    # T-GH-7 (row 19)
+    "test_gh_reads_every_level": [
+        (c, NONE4)
+        for c in (
+            "gh pr view 5 --json mergeable,mergeStateStatus",
+            "gh issue view 5",
+            "gh pr checks 5",
+            "gh repo view",
+            "gh api repos/o/r/pulls/5",
+            "gh api repos/o/r/commits/abc123/check-runs --jq .total_count",
+        )
+    ],
+    # T-GH-8
+    "test_merge_url_suffix": [
+        ("curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge", MERGE),
+        ("curl -X POST https://api.github.com/repos/o/r/merges", MERGE),
+        ("gh api repos/o/r/pulls/5/merge", GHWRITE),
+    ],
+    # T-GH-9
+    "test_gh_unknown_group_or_action": [
+        (c, UNK)
+        for c in (
+            "gh alias set co 'pr merge'",
+            "gh co 5",
+            "gh extension install x",
+            "gh pr $(echo merge) 5",
+            "gh pr `echo merge` 5",
+            "gh pr close 5",
+        )
+    ],
+    # T-GH-10: every GHWRITE flag word and endpoint of FR-L-36; one allowed read.
+    "test_gh_api_get_only": [
+        *[
+            (f"gh api repos/o/r/pulls {flag}", GHWRITE)
+            for flag in (
+                "-XPOST",
+                "-X",
+                "-iXPOST",
+                "--method=POST",
+                "--method",
+                "--raw-field=x=y",
+                "--raw-field",
+                "-f",
+                "-F",
+                "-Fbody=x",
+                "-fa=b",
+                "--field",
+                "--field=a=b",
+                "--input",
+                "--input=f",
+            )
+        ],
+        *[
+            (f"gh api {endpoint}", GHWRITE)
+            for endpoint in ("graphql", "repos/o/r/pulls/5/merge", "repos/o/r/merges")
+        ],
+        ("gh api repos/o/r/pulls", NONE4),
+        ("gh api repos/o/r/pulls/5", NONE4),
+        (
+            "gh api repos/o/r/pulls -H Accept:application/json --paginate -i --silent -q .total_count",
+            NONE4,
+        ),
+        ("gh api repos/o/r/pulls --hostname github.com -t {{.x}}", GHWRITE),
+        ("gh api repos/o/r/pulls --hostname github.com -t .x", NONE4),
+    ],
+    # T-GH-11: T-ATK-18, 19, 20, 31, 56 and a variable endpoint.
+    "test_gh_api_shell_built_flag": [
+        *[
+            (c, GHWRITE)
+            for c in (
+                "X=X; gh api repos/o/r/git/refs/heads/main -$X DELETE",
+                "gh api repos/o/r/git/refs/heads/main `echo -e '\\055X'` DELETE",
+                "gh api repos/o/r/git/refs/heads/main {-X,DELETE}",
+                'gh api repos/o/r/git/refs/heads/main --jq ".a >" -X DELETE',
+                "gh api repos/o/r/git/refs/heads/main -X\\\nDELETE",
+                'gh api "repos/$REPO/pulls"',
+            )
+        ],
+        ("gh api repos/o/r/commits/abc123/check-runs --jq .total_count", NONE4),
+    ],
+    # T-GH-12
+    "test_gh_text_rules": [
+        (
+            f'gh pr create {REPO_FLAG} --base master --head f --title "docs: explain git hooks" --body "x"',
+            SUBMIT,
+        ),
+        ('gh pr create --repo o/r --title "fix api docs"', GHWRITE),
+        ('echo "use gh to view"', NONE4),
+    ],
+    # T-GH-13: N-ATK-20, 21, 22 and 35 (B-3), and N-ATK-36 (residual R17).
+    "test_gh_anywhere_rules": [
+        ("X=ge; flock /tmp/l gh pr mer$X 5", UNK),
+        ("if :; then gh repo sync; fi", MERGE),
+        ("if :; then gh pr update-branch 5; fi", MERGE),
+        ("if :; then gh alias set mm 'pr merge'; fi", UNK),
+        ("flock /tmp/l gh mm 5", NONE4),
+    ],
+    # T-GH-14: N-ATK-26 (B-7).
+    "test_direct_github_api_blocked": [
+        (
+            'curl -sS -X PATCH -H "Authorization: token $(gh auth token)" '
+            "https://api.github.com/repos/o/r/git/refs/heads/main "
+            '-d \'{"sha":"abc","force":true}\'',
+            GHWRITE,
+        ),
+    ],
+}
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        p
+        for name, rows in GH_NAMED.items()
+        for p in _gh_params(f"{name.removeprefix('test_')}-", rows)
+    ],
+)
+def test_gh_named_cases(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+# Task 8 acceptance criteria, as written in the plan.
+GH_ACCEPTANCE = [
+    ("gh api repos/o/r/pulls/5 --jq .state", NONE4),
+    ("gh api -X POST repos/o/r/merges", GHWRITE),
+    ("gh api graphql -f query='{ viewer { login } }'", GHWRITE),
+    ("gh api graphql", GHWRITE),
+    ("curl -X PATCH https://api.github.com/repos/o/r", GHWRITE),
+    ("gh pr create --repo o/r --title x", SUBMIT),
+    ("gh pr create --title x", SUBMIT_REPO),
+    ("gh pr merge 5", MERGE),
+    ("gh repo sync", MERGE),
+    ("gh pr view 5", NONE4),
+    ("gh pr checks", NONE4),
+    ("gh alias set co 'pr merge'", UNK),
+]
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id", list(_gh_params("acc-", GH_ACCEPTANCE))
+)
+def test_gh_task8_acceptance(tmp_path, command, level, msg_id):
+    _git_case(tmp_path, command, level, msg_id)
+
+
+@pytest.mark.parametrize("tool", ["Bash", "Monitor"])
+def test_gh_class_from_text_prints_text_note(tmp_path, tool):
+    # A gh class from Bash or Monitor text carries the LL-TEXT note.
+    _bind(tmp_path, *LEVEL_FILES["FS"])
+    result = _run(_bash("gh pr merge 5", tool=tool), tmp_path)
+    _assert_decision(result, tmp_path, "LL-MERGE", "FS", text=True)

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
