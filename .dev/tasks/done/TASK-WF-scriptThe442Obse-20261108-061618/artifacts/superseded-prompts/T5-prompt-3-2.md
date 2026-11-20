6fdae45fcfb2d8f73b7acb9b87a530ab57ee0517

Task brief: Task 5 of plan .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (read it, lines 122-146). Deliverables: setup-github.sh for runbook section 1.4 (lines 170-200): four disposable issues (copy ~/.claude/ISSUE-HANDOFF.md to a temp file, fill every section, gh_fork issue create --title ... --body-file <copy>, record each number in the state file); refuses to create issues when the state file already holds numbers; starts the claim session in the main checkout with the driver (start claim path:<main checkout> "env -u CLICKUP_API_TOKEN claude"); for each issue sends /sc:issue --claim <T> --pipeline none, reads "Worktree: <path> (created)" from the screen, records WT_T1..WT_T4; writes each worktree's .claude/settings.local.json with the runbook line-197 generator, labels h2-T1..h2-T4; when that file already exists stops with "EXISTS: merge by hand", never overwrites. AC ids: T5.AC1 = "With the stub `gh`, the self-test shows four `issue create` calls, each carrying `--repo IronbellyOrg/IronClaude` and a `--body-file`, and no second set on a rerun."; T5.AC2 = "The self-test shows the generated `settings.local.json` equal to the output of the runbook's line 197 generator, and the script refusing to overwrite an existing file."; T5.AC3 = "The worktree paths are read from the claim screen, not guessed. A self-test case with a scripted screen records `WT_T1`."

Global constraints: plan lines 17-27 (read them). Key: creating the four issues and the disposable PR is within the owner authorization (plan line 19); every gh call via gh_fork (--repo pinned); nothing targets SuperClaude-Org; no Orca --issue/--pr flags; uv only; every external call timeout-bounded; set -u -o pipefail umask 077; scratch under /tmp/ob (OB overridable); no src/ or tests/ changes; the claim session starts env -u CLICKUP_API_TOKEN claude.

Start sha: 6fdae45fcfb2d8f73b7acb9b87a530ab57ee0517

Diff against the start snapshot: new files — read setup-github.sh and setup-github-selftest.sh in full, plus the changed selftest.sh (gh stub now prints real issue URLs) and lib.sh if changed. The saved run log is .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t5-selftest.txt (read it). Runbook grounding: .dev/issues/442/observation-runbook.md lines 170-200; the template is ~/.claude/ISSUE-HANDOFF.md (4 sections with angle-bracket placeholders).

Delta diff from the previous reviewed tree (the repair-round fix applied after the A3 review; the review package is still the full change against the start sha):
diff --git a/.dev/issues/442/scripts/selftest.sh b/.dev/issues/442/scripts/selftest.sh
index 67a23207b..6e053832c 100644
--- a/.dev/issues/442/scripts/selftest.sh
+++ b/.dev/issues/442/scripts/selftest.sh
@@ -65,6 +65,12 @@ printf '%s\n' "$*" >> "$L/gh.log"
 case "$1 $2" in
   'issue create')
     n=$(( $(cat "$L/issue-n" 2>/dev/null || echo 420) + 1 )); printf '%s' "$n" > "$L/issue-n"
+    # capture the --body-file content so a case can assert what the body says
+    prev=""
+    for a in "$@"; do
+      [ "$prev" = "--body-file" ] && cat "$a" >> "$L/bodies.txt" 2>/dev/null
+      prev=$a
+    done
     printf 'https://github.com/IronbellyOrg/IronClaude/issues/%s\n' "$n" ;;
   *)  case "$1" in
         --version) printf 'gh version 0.0.0-stub\n' ;;
diff --git a/.dev/issues/442/scripts/setup-github-selftest.sh b/.dev/issues/442/scripts/setup-github-selftest.sh
index 4f63db464..33af2a52d 100644
--- a/.dev/issues/442/scripts/setup-github-selftest.sh
+++ b/.dev/issues/442/scripts/setup-github-selftest.sh
@@ -67,8 +67,13 @@ ck sg-done "$(tail -1 "$T/out1")" "SETUP_GITHUB_OK"
 # 2. four issue-create calls, each --repo pinned and --body-file used, no rerun set
 grep -c -- '--repo IronbellyOrg/IronClaude' "$L/gh.log" | grep -qx 4 && ck sg-four-creates ok ok || ck sg-four-creates "$(grep -c -- '--repo IronbellyOrg/IronClaude' "$L/gh.log")" 4
 grep -c -- '--body-file' "$L/gh.log" | grep -qx 4 && ck sg-bodyfile ok ok || ck sg-bodyfile "$(grep -c -- '--body-file' "$L/gh.log")" 4
-# this case checks only the create count: the stub gh logs its arguments and does
-# not inspect the template content (the fill itself is not asserted here)
+# the stub gh copies each --body-file into $L/bodies.txt: the filled body must carry
+# the runbook's body text verbatim (runbook line 178) and leave no placeholder.
+grep -c -F 'Touch nothing else. Close without merging anything.' "$L/bodies.txt" | grep -qx 4 \
+  && ck sg-body-instruction ok ok || ck sg-body-instruction "$(grep -c -F 'Touch nothing else. Close without merging anything.' "$L/bodies.txt")" 4
+grep -c -F 'The only change wanted: create the file ob-442/' "$L/bodies.txt" | grep -qx 4 \
+  && ck sg-body-change ok ok || ck sg-body-change "$(grep -c -F 'The only change wanted: create the file ob-442/' "$L/bodies.txt")" 4
+grep -c -E '^<[^>]*>$' "$L/bodies.txt" | grep -qx 0 && ck sg-body-no-placeholder ok ok || ck sg-body-no-placeholder "$(grep -c -E '^<[^>]*>$' "$L/bodies.txt")" 0
 grep -c 'issue create' "$L/gh.log" | grep -qx 4 && ck sg-create-count ok ok || ck sg-create-count "$(grep -c 'issue create' "$L/gh.log")" 4
 
 # 3. rerun refused: state holds numbers, so no second create set
diff --git a/.dev/issues/442/scripts/setup-github.sh b/.dev/issues/442/scripts/setup-github.sh
index 012ae8b1d..77a1a91b1 100644
--- a/.dev/issues/442/scripts/setup-github.sh
+++ b/.dev/issues/442/scripts/setup-github.sh
@@ -18,10 +18,12 @@ else
     # issue rule (never edit the installed template itself).
     tpl=$(mktemp)
     cp "$HOME/.claude/ISSUE-HANDOFF.md" "$tpl"
+    # The runbook's body text (runbook line 178) is carried verbatim: the first
+    # sentence under "What was tried", the rest under "Done when".
     sed -i \
-      -e "s|<what has been tried so far, and what happened>|Nothing yet: this is a disposable target for the #442 live observations ($t).|" \
-      -e "s|<paths, links, branches, pull requests>|ob-442/$t.txt (to be created)|" \
-      -e "s|<the condition that means this work is finished>|ob-442/$t.txt exists holding the single line: ob-442 $t|" \
+      -e "s|<what has been tried so far, and what happened>|Disposable target for the #442 live observations ($t).|" \
+      -e "s|<paths, links, branches, pull requests>|ob-442/$t.txt|" \
+      -e "s|<the condition that means this work is finished>|The only change wanted: create the file ob-442/$t.txt holding the single line ob-442 $t. Touch nothing else. Close without merging anything.|" \
       -e "s|<the person or agent this is handed to>|The observation run's governed sessions ($t)|" \
       "$tpl"
     n=$(gh_fork issue create --title "[ob-442 disposable $t] launch-level observation target" --body-file "$tpl" 2>&1 \

Earlier blocking findings of this start (empty on the first review):
F5.2 sev=blocking trigger=B4 ac=scope at=.dev/issues/442/scripts/setup-github.sh:22 anchor="fills every section with the runbook's title and body text for that issue (line 177 and line 178)" chk=amiss:n,false:n,harm:n,constraint:y family=body-text-fidelity fix="Fill the template sections with the runbook's body text verbatim, including 'The only change wanted: create the file ob-442/$t.txt holding the single line ob-442 $t. Touch nothing else. Close without merging anything.'" covers="fills every section with the runbook's title and body text for that issue (line 177 and line 178)" first=A1 origin=new: the filled body paraphrases the runbook body and drops "The only change wanted... Touch nothing else. Close without merging anything."; the governed sessions later work these issues and "Touch nothing else" is the part that matters.

Saved-probe re-check hit locations (may be empty): the saved probe was re-run (grep -n -F over setup-github.sh, setup-github-selftest.sh and selftest.sh for the body-text and issue-create sites); current hits:
.dev/issues/442/scripts/setup-github.sh:24:      -e "s|<what has been tried so far, and what happened>|Disposable target for the #442 live observations ($t).|" \
.dev/issues/442/scripts/setup-github.sh:26:      -e "s|<the condition that means this work is finished>|The only change wanted: create the file ob-442/$t.txt holding the single line ob-442 $t. Touch n
.dev/issues/442/scripts/setup-github.sh:29:    n=$(gh_fork issue create --title "[ob-442 disposable $t] launch-level observation target" --body-file "$tpl" 2>&1 \
.dev/issues/442/scripts/setup-github-selftest.sh:70:# the stub gh copies each --body-file into $L/bodies.txt: the filled body must carry
.dev/issues/442/scripts/setup-github-selftest.sh:72:grep -c -F 'Touch nothing else. Close without merging anything.' "$L/bodies.txt" | grep -qx 4 \
.dev/issues/442/scripts/setup-github-selftest.sh:73:  && ck sg-body-instruction ok ok || ck sg-body-instruction "$(grep -c -F 'Touch nothing else. Close without merging anything.' "$L/bodies.txt")" 4
.dev/issues/442/scripts/setup-github-selftest.sh:74:grep -c -F 'The only change wanted: create the file ob-442/' "$L/bodies.txt" | grep -qx 4 \
.dev/issues/442/scripts/setup-github-selftest.sh:75:  && ck sg-body-change ok ok || ck sg-body-change "$(grep -c -F 'The only change wanted: create the file ob-442/' "$L/bodies.txt")" 4
.dev/issues/442/scripts/setup-github-selftest.sh:76:grep -c -E '^<[^>]*>$' "$L/bodies.txt" | grep -qx 0 && ck sg-body-no-placeholder ok ok || ck sg-body-no-placeholder "$(grep -c -E '^<[^>]*>$' "$L/bo
.dev/issues/442/scripts/setup-github-selftest.sh:77:grep -c 'issue create' "$L/gh.log" | grep -qx 4 && ck sg-create-count ok ok || ck sg-create-count "$(grep -c 'issue create' "$L/gh.log")" 4
.dev/issues/442/scripts/setup-github-selftest.sh:80:before=$(grep -c 'issue create' "$L/gh.log")
.dev/issues/442/scripts/setup-github-selftest.sh:82:after=$(grep -c 'issue create' "$L/gh.log")
.dev/issues/442/scripts/selftest.sh:66:  'issue create')
.dev/issues/442/scripts/selftest.sh:71:      [ "$prev" = "--body-file" ] && cat "$a" >> "$L/bodies.txt" 2>/dev/null

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
