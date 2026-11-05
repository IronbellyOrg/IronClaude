6ae8aab9ff77a0210ac8f284b45d2407e0b4dcfc
Review one task for spec compliance.

Task brief: ## Task 2: Redirect the informational lines in ccsession to standard error

Depends on: Task 1

Edit `src/superclaude/skills/ccsession-tag/ccsession` (line numbers are those at commit 8b4858f7; re-read each before editing):
- Add `>&2` to the ten informational `echo` lines: 965 (`Shim already running ... (reusing)`), 969 (`A shim with other settings or older code ...`), 984 (`Starting model-alias shim ...`), 1195, 1197 and 1199 (the `$what` profile and tier lines in `export_selection`), 1796 (`Starting untagged session`), 1840 (`... has no saved conversation; starting a new one`), 1849 (`Resuming ...`) and 1864 (`Starting new session labeled ...`).
- Change line 1028 from `python3 - <<'PY'` to `python3 - >&2 <<'PY'` so the Python `print` at line 1077 (`Cached N curated gateway models before launch`) goes to standard error, and add one comment line above the `if ! CC_CACHE_BASE_URL=...` command (line 1024) saying that status goes to standard error so standard output carries only Claude's output.
- Change line 1733 from `python3 "$CCSESSION_MODELS" refresh --wait "${CCSESSION_MODELS_WAIT:-2}" || true` to put `>&2` before `|| true`, so the two `models.py` notes it can print reach standard error without editing `models.py`.
- Do not touch any line that already ends in `>&2`, any `$(...)` capture of `models.py`, or the `--ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status` paths.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` exits 0.
- `grep -n 'echo "\[ccsession\]' src/superclaude/skills/ccsession-tag/ccsession | grep -v '>&2'` prints nothing, and line 1028 reads `python3 - >&2 <<'PY'`.
- The replay test from Task 1, run on the tree with this change, PASSES; its output is saved to `./artifacts/t2-positive.log`. This is the positive witness for the fix.

AC ids:
T2.AC1: `bash -n src/superclaude/skills/ccsession-tag/ccsession` exits 0.
T2.AC2: `grep -n 'echo "\[ccsession\]' src/superclaude/skills/ccsession-tag/ccsession | grep -v '>&2'` prints nothing, and line 1028 reads `python3 - >&2 <<'PY'`.
T2.AC3: The replay test from Task 1, run on the tree with this change, PASSES; its output is saved to `./artifacts/t2-positive.log`. This is the positive witness for the fix.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: 6ae8aab9ff77a0210ac8f284b45d2407e0b4dcfc
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index 2f443f04..bfcc85de 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -962,11 +962,11 @@ setup_shim() {
     health_status=$(shim_health_status)
     case "$health_status" in
       match)
-        echo "[ccsession] Shim already running on 127.0.0.1:$CC_SHIM_PORT (reusing)"
+        echo "[ccsession] Shim already running on 127.0.0.1:$CC_SHIM_PORT (reusing)" >&2
         break
         ;;
       stale)
-        echo "[ccsession] A shim with other settings or older code is on 127.0.0.1:$CC_SHIM_PORT; leaving it running for its sessions"
+        echo "[ccsession] A shim with other settings or older code is on 127.0.0.1:$CC_SHIM_PORT; leaving it running for its sessions" >&2
         ;;
       *)
         if [ "$_attempt" = 0 ]; then
@@ -981,7 +981,7 @@ setup_shim() {
     exit 1
   fi
   if [ "$start_shim" = 1 ]; then
-    echo "[ccsession] Starting model-alias shim on 127.0.0.1:$CC_SHIM_PORT"
+    echo "[ccsession] Starting model-alias shim on 127.0.0.1:$CC_SHIM_PORT" >&2
     # The shim inherits this session's env (tier settings fallback, show-all,
     # cooldown length); it reads the workspace env file itself on each request.
     # Start it from a subshell that exits at once, so the shim is not a
@@ -1021,11 +1021,12 @@ setup_shim() {
   # finishes when --model is supplied. Warm the cache synchronously so every
   # profile starts with the complete curated shim list.
   cache_file="$HOME/.claude/cache/gateway-models.json"
+  # Status goes to stderr: stdout carries only Claude's output (issue 389).
   if ! CC_CACHE_BASE_URL="$ANTHROPIC_BASE_URL" \
     CC_CACHE_FILE="$cache_file" \
     CC_CACHE_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-}" \
     CC_CACHE_API_KEY="${ANTHROPIC_API_KEY:-}" \
-    python3 - <<'PY'
+    python3 - >&2 <<'PY'
 import json
 import os
 import pathlib
@@ -1192,11 +1193,11 @@ export_selection() {
   fi
 
   if [ -z "$PROFILE_MODEL" ]; then
-    echo "[ccsession] $what: default model and context"
+    echo "[ccsession] $what: default model and context" >&2
   elif [ -n "$PROFILE_COMPACT_WINDOW" ]; then
-    echo "[ccsession] $what: model $PROFILE_MODEL, context $PROFILE_CONTEXT, auto-compact window $PROFILE_COMPACT_WINDOW"
+    echo "[ccsession] $what: model $PROFILE_MODEL, context $PROFILE_CONTEXT, auto-compact window $PROFILE_COMPACT_WINDOW" >&2
   else
-    echo "[ccsession] $what: model $PROFILE_MODEL, context $PROFILE_CONTEXT, native auto-compact"
+    echo "[ccsession] $what: model $PROFILE_MODEL, context $PROFILE_CONTEXT, native auto-compact" >&2
   fi
 }
 
@@ -1730,7 +1731,7 @@ fi
 # and never fatal, so offline launches use the cached or bundled copy.
 # Private add-on profiles (profiles.d) never use this data, so they skip it.
 if [ "${CCSESSION_MODELS_REFRESH:-1}" != 0 ] && [ "$CCSESSION_EXT_PROFILE" != 1 ]; then
-  python3 "$CCSESSION_MODELS" refresh --wait "${CCSESSION_MODELS_WAIT:-2}" || true
+  python3 "$CCSESSION_MODELS" refresh --wait "${CCSESSION_MODELS_WAIT:-2}" >&2 || true
 fi
 
 if [ "$TIER_MODE" = 1 ]; then
@@ -1793,7 +1794,7 @@ if [ "$NAME_GIVEN" != 1 ] && { [ "$#" -eq 0 ] || [[ "${1:-}" == -* ]]; }; then
   set -- "$@" ${CLAUDE_PASSTHROUGH[@]+"${CLAUDE_PASSTHROUGH[@]}"}
   # A label inherited from a ccsession session around this one is not ours.
   unset CLAUDE_TOPIC CCSESSION_TOPIC_CWD
-  echo "[ccsession] Starting untagged session"
+  echo "[ccsession] Starting untagged session" >&2
   orca_terminal_title
   if [ -n "${PROFILE_MODEL:-}" ]; then
     exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --model "$PROFILE_MODEL" "$@"
@@ -1837,7 +1838,7 @@ orca_terminal_title "$TOPIC"
 if [ -f "$TOPIC_FILE" ]; then
   SESSION_ID=$(head -n 1 "$TOPIC_FILE")
   if ! session_saved "$SESSION_ID"; then
-    echo "[ccsession] Session ${SESSION_ID:0:8} for '$TOPIC' has no saved conversation; starting a new one"
+    echo "[ccsession] Session ${SESSION_ID:0:8} for '$TOPIC' has no saved conversation; starting a new one" >&2
     rm -f "$TOPIC_FILE"
   fi
 fi
@@ -1846,7 +1847,7 @@ fi
 # so the two never differ. The hooks keep the label in step with /rename, so a
 # resume passes the session's current name.
 if [ -f "$TOPIC_FILE" ]; then
-  echo "[ccsession] Resuming '$TOPIC' (session ${SESSION_ID:0:8})"
+  echo "[ccsession] Resuming '$TOPIC' (session ${SESSION_ID:0:8})" >&2
   # Claude Code continues a resumed conversation in this folder. One that
   # belongs to another worktree that still exists would now edit and commit here.
   _jsonl=$(session_transcript "$SESSION_ID")
@@ -1861,7 +1862,7 @@ if [ -f "$TOPIC_FILE" ]; then
     exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --name "$TOPIC" --resume "$SESSION_ID" "$@"
   fi
 else
-  echo "[ccsession] Starting new session labeled '$TOPIC'"
+  echo "[ccsession] Starting new session labeled '$TOPIC'" >&2
   if [ -n "${PROFILE_MODEL:-}" ]; then
     exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --model "$PROFILE_MODEL" --name "$TOPIC" "$@"
   else

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t2-positive.log ---
============================= test session starts ==============================
collected 1 item

tests/unit/test_ccsession_tag.py .                                       [100%]

============================== 1 passed in 1.05s ===============================

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
