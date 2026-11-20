689be7ef40fbe927dd7c7e368dfc5417ea6f1d65
Review one task for spec compliance.

Task brief: ## Task 2: Make launch_real use the file's terminal, layers and a saved copy

Depends on: Task 1

Edit `launch_real` in `.dev/issues/442/scripts/session-gov.sh` (lines 155 to 190 on master) and `run_c` (lines 341 to 355):

- Resume branch (lines 158 to 161): the saved record becomes a copy of the result file, `$OB/claim-$t.json`, not claim text. Condition: `[ -n "$(state_get "RESUME_LAUNCH_$t")" ] && [ -s "$OB/claim-$t.json" ]`; on resume set `CLAIM_FILE="$OB/claim-$t.json"`, call `load_claim_result` on it without the staleness test (it was validated when it was saved) and `CLAIM_STATUS=launched`. When `RESUME_LAUNCH_$t` is set but only an older `$OB/claim-$t.txt` exists, `die resume` with a message saying that run saved text only and the claim must not be repeated (a repeat would be `already_launched` and write nothing); this is one line and protects the live workspace.
- Fresh branch: `claim_send "$n" "$2"`; `[ "$CLAIM_STATUS" = launched ] || die "$sub-claim" "status=$CLAIM_STATUS warning=$CLAIM_WARNING file=$CLAIM_FILE"`; then `cp -- "$CLAIM_FILE" "$OB/claim-$t.json"` and `state_set "RESUME_LAUNCH_$t" ...` as before.
- Layers (line 168): `claim_layer_has 'L1 guard: effective'` replaces `claim_has 'L1 guard: effective'`; the failure record keeps its `$sub-layers` id and names `enforcement_hook` and the layers read from the file (`jq -r '(.layers // []) | join(" | ")'`) instead of grepping `CLAIM_LAST`. The `OK` record says the line came from `launch-result.json`.
- Terminal (lines 169 to 183): `h=$CLAIM_TERMINAL`. Delete the `case` over `CLAIM_LAST` and the whole `orca terminal list` lookup including the `$sub-terminal` record. When `h` is empty or does not match `^[0-9A-Za-z_-]+$`, keep the two `runlog` lines (record text is now `$CLAIM_JSON`; the `worktree.json` launch record line stays) and `pending "reason=terminal-handle-missing file=$CLAIM_FILE (full record in $PKG_ART/t10-run-log.md)"`.
- `run_c` (line 345): move `MAIN=${OB_MAIN:-$(main_checkout)}` above the `launch_real T2` call (line 344); on master it is set after the call, and the new reader needs `MAIN`. `run_b`, `run_d` and `run_e` already set it before their `launch_real`/`claim_send` calls (lines 280, 373, 436).

Acceptance criteria:
- `grep -n 'terminal list' .dev/issues/442/scripts/session-gov.sh` prints nothing, and `grep -n 'orca ' .dev/issues/442/scripts/session-gov.sh` shows no `orca terminal list`.
- `launch_real` passes `driver.sh adopt` only a handle read from the file (`jq`) after the character check.
- A launched result saved at `$OB/claim-T1.json` is byte-equal to the result file (`cmp`), checked by the self-test in Task 4.
- In `run_c` the line setting `MAIN` precedes the line calling `launch_real T2`.

AC ids in source order of the Acceptance criteria bullets: T2.AC1 (no terminal list), T2.AC2 (adopt only a jq-read handle after the character check), T2.AC3 (saved claim-T1.json byte-equal to the result file), T2.AC4 (MAIN set before launch_real T2 in run_c).
Global constraints: ## Constraints

- Scope is Part B of issue 691 (https://github.com/IronbellyOrg/IronClaude/issues/691). Part A (PR 693, merge commit dd7bdf2f7) already writes the file: `write_launch_result` at `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:244`, called from `cmd_launch` (`finish`, line 1711) for `launched` and `failed` results and never for `already_launched` (the `emit` at line 1730). Do not edit `src/`, `tests/` or any file outside the Part B file list below. A verbatim-print rule for the claiming agent is out of scope.
- Part B file list (the only files the diff may touch besides this package): `.dev/issues/442/scripts/session-gov.sh`, `.dev/issues/442/scripts/session-gov-selftest.sh`, `.dev/issues/442/scripts/runbook-selftest.sh`, `.dev/issues/442/observation-runbook.md`. `lib.sh`, `driver.sh`, `evidence.sh`, `cleanup.sh`, `setup-github.sh`, `session-a*.sh` and their self-tests read no claim result from this launch path and stay unchanged (`setup-github.sh` makes `--pipeline none` claims, which never reach `cmd_launch`, so no file exists for it). `.dev/issues/442/observation-results.md`, `.dev/issues/442/run2/`, `.dev/issues/442/handoff-runbook.md` and every package under `.dev/tasks/done/` are recorded evidence or history: do not edit them.
- Where the file lives (verified by reading `orca_worktree.py`): `cmd_launch` writes to `source / "launch-result.json"` where `source` is the `--source <D>` folder `.dev/issues/<N>` of the checkout the claim session runs in; the runbook starts every claim from an ordinary Claude session in the main checkout (runbook line 534), and the script already reads `worktree.json` from `${MAIN:-.}/.dev/issues/$n/` (session-gov.sh lines 181 and 252). The worktree copy never receives the file (`orca_worktree.py:477` skips `RECORD_NAME` and `LAUNCH_RESULT_NAME`). So the path is `$MAIN/.dev/issues/$n/launch-result.json`. That the live claim passes a `--source` that resolves to the main checkout is UNVERIFIED until the owner-gated rerun.
- The claim's start: the script records `CLAIM_START=$(date +%s)` immediately before it types the claim (after the `/clear` that precedes it). A result is fresh only when the file's integer mtime (`stat -c %Y`) is at least `CLAIM_START`, and, when `launched_at` is a string, `date -u -d "$launched_at" +%s` is also at least `CLAIM_START`. Both clocks are the one host clock (the claim, the script and the checkout share a machine). Integer seconds can only err toward "stale" for a result written later in the same second, never toward accepting an older one, except a result written by a previous claim in the very same second as this claim's start, which the several-second claim run makes negligible; selftests use back-dated mtimes (`touch -d`), never `sleep`. No clock-skew allowance is added.
- Outcomes, mirroring the existing `pending`/`die` pattern (`pending` prints `PENDING <text>` and exits 0; `die` records `FAIL` and exits 1 by default): file absent after the poll loop is `pending "reason=claim-result-missing ..."` (exit 0); file present but stale is `pending "reason=claim-result-stale ..."` (exit 0), which is also what an `already_launched` claim produces because Part A writes nothing for it; a file that is a symlink, is not a JSON object, or has no string `status` is `die claim-result "<why>"` (exit 1). Existing outcomes stay: dialog on the claim screen is `pending ... reason=needs-input` (exit 0), a vanished claim terminal is `pending reason=claim-terminal-gone` (exit 0), a result whose `status` is not `launched` in `launch_real` is `die "$sub-claim"` (exit 1), a missing or invalid terminal handle is `pending reason=terminal-handle-missing` (exit 0).
- JSON is read only through `jq` with the repository's `command timeout "$T" jq ...` form; file text is never passed to `eval`, `source`, `bash -c` or an unquoted expansion. The terminal handle is checked against `^[0-9A-Za-z_-]+$` before it reaches `driver.sh adopt`.
- The claim terminal's screen is still read for two non-result jobs only: the vanished-terminal check and the `Do you want|/login|Not logged in` dialog check. It is never parsed for status, terminal, layers or release. `screen_text` stays for `plan_path` and `find_pr_url`.
- Do not delete, rename, rewrite or `touch` any real `launch-result.json`: Part A keeps an earlier file when a later claim is `already_launched`, and run evidence may sit beside it. Only temporary fixtures under the self-tests' `mktemp -d /tmp/ob-gov.*` folder may be created.
- Runbook line anchors other self-tests read: `session-gov-selftest.sh` extracts runbook lines 536 to 697 (`sed -n '536,697p'`), and `runbook-selftest.sh` pins lines 228, 505, 520, 536 and 698. Runbook edits in lines 1 to 698 must therefore replace text inside existing physical lines and add or remove no line. Section 6 and later lines may gain lines. The runbook cites script lines as `` `fragment` (session-gov.sh:N) ``; `runbook-selftest.sh` checks every such pair, so every citation shifted by the script edit must be updated.
- UNVERIFIED convention: a runbook statement about live behaviour (a real claim leaves the file; the file's fields equal what the agent prints) is written UNVERIFIED until the owner-gated rerun. A statement proven by reading `orca_worktree.py` or `refs/claim.md` may be written VERIFIED with its citation. This plan's change never flips an UNVERIFIED label to VERIFIED for live behaviour.
- Owner-gated steps, NOT executed by this plan and NOT to be run by the implementer: after the code is merged, the coordinator asks the owner in chat; only the owner's "yes" in chat starts either step. Step one: `superclaude install` (puts the Part A skill, with the file writer, into `~/.claude`, which is what a live claim runs). Step two: the live OB-H2 rerun on the disposable issues T1 to T4 only, to confirm a real claim leaves `.dev/issues/<N>/launch-result.json` in the main checkout and that the scripts pass reading it. The Part B done-when "a live claim leaves it in place" is satisfied only by step two, after merge.
- The implementer must NOT run: `superclaude install`, any `orca` command that launches, creates or closes anything, `session-gov.sh`, `driver.sh`, `setup*.sh`, `cleanup.sh` or `session-a*.sh` against the real `/tmp/ob` or real HOME, any `/sc:issue --claim`, any `gh` write, `git push`, a commit, or a pull request from this package. The self-tests are safe: they use stub `orca`, `gh` and `git` binaries and temporary HOME folders. Stage with `git add .dev/tasks` and the Part B files only; never stage anything under `.claude/`; commit only when asked. The pull request, when asked for, is opened with `/sc:pr-submit --monitor 3` only.
- UV only for Python. This change is bash and markdown; `make lint` (ruff plus architecture lint) and `make verify-sync` run unchanged and are expected to pass untouched.

Start sha: 689be7ef40fbe927dd7c7e368dfc5417ea6f1d65
Diff against the start snapshot: 
```diff
diff --git a/.dev/issues/442/scripts/session-gov.sh b/.dev/issues/442/scripts/session-gov.sh
index 4fc08e07e..49d597128 100644
--- a/.dev/issues/442/scripts/session-gov.sh
+++ b/.dev/issues/442/scripts/session-gov.sh
@@ -190,32 +190,30 @@ pend_count() { ls -A "$HOME/.claude/state/launch-level/pending" 2>/dev/null | wc
 launch_real() {  # launch_real <T1..T4> <flags> <session name> [first-stop wait secs; absent or 0 = do not wait]
   local t=$1 n h label=h2-$1
   need n "$t"
-  if [ -n "$(state_get "RESUME_LAUNCH_$t" 2>/dev/null)" ] && [ -s "$OB/claim-$t.txt" ]; then
-    # the real launch already happened in an earlier run of this script (its claim text was saved then): do not claim again
-    CLAIM_LAST=$(cat "$OB/claim-$t.txt"); CLAIM_STATUS=launched; CLAIM_SCREEN=none
-    rec "$sub-resume" OK "launch of $t reused from the saved claim text $OB/claim-$t.txt"
+  if [ -n "$(state_get "RESUME_LAUNCH_$t" 2>/dev/null)" ] && [ -s "$OB/claim-$t.json" ]; then
+    # the real launch already happened in an earlier run of this script (its result file was saved then, and checked when it was saved): do not claim again
+    CLAIM_FILE=$OB/claim-$t.json; load_claim_result; CLAIM_STATUS=launched
+    rec "$sub-resume" OK "launch of $t reused from the saved result file $OB/claim-$t.json"
+  elif [ -n "$(state_get "RESUME_LAUNCH_$t" 2>/dev/null)" ] && [ -e "$OB/claim-$t.txt" ]; then
+    die resume "an earlier run launched $t and saved claim text only ($OB/claim-$t.txt), not a result file; do not claim again (a repeat is already_launched and writes no result file)"
   else
     claim_send "$n" "$2"
-    [ "$CLAIM_STATUS" = launched ] || die "$sub-claim" "status=$CLAIM_STATUS screen=$CLAIM_SCREEN"
-    printf '%s\n' "$CLAIM_LAST" > "$OB/claim-$t.txt"
+    [ "$CLAIM_STATUS" = launched ] || die "$sub-claim" "status=$CLAIM_STATUS warning=$CLAIM_WARNING file=$CLAIM_FILE"
+    cp -- "$CLAIM_FILE" "$OB/claim-$t.json"
     state_set "RESUME_LAUNCH_$t" "$(date -u +%FT%TZ)"
   fi
-  claim_has 'L1 guard: effective' && rec "$sub-layers" OK "L1 guard: effective" || rec "$sub-layers" FAIL "no 'L1 guard: effective' line (the claim session printed its own summary; enforcement_hook line: $(printf '%s' "$CLAIM_LAST" | grep -oE 'enforcement_hook:[a-z]+' | head -1))"
-  case "$CLAIM_LAST" in
-    *'"terminal":"'*) h=${CLAIM_LAST#*\"terminal\":\"}; h=${h%%\"*} ;;
-    *) h="" ;;
-  esac
-  if [ -z "$h" ]; then
-    # the real claim output has no terminal key: take the one Orca terminal of this issue's worktree whose title is the launch marker
-    h=$(command timeout "$T" orca terminal list --json 2>/dev/null | command timeout "$T" jq -r --arg wt "$(state_get "WT_$t")" \
-        '[.result.terminals[] | select(.worktreePath == $wt and ((.title // "") | test("sc-launch")))] | if length == 1 then .[0].handle else empty end' 2>/dev/null)
-    [ -z "$h" ] || rec "$sub-terminal" OK "terminal $h found by worktree path and launch title (the claim output has no terminal key)"
-  fi
-  if [ -z "$h" ]; then
-    runlog "claim $t: no terminal key in the claim output; record: $CLAIM_LAST"
-    runlog "claim $t: launch record: $(command timeout "$T" jq -c '.launch // "none"' "${MAIN:-.}/.dev/issues/$n/worktree.json" 2>&1)"
-    pending "reason=terminal-handle-missing screen=$CLAIM_SCREEN (full record in $PKG_ART/t10-run-log.md)"
+  if claim_layer_has 'L1 guard: effective'; then
+    rec "$sub-layers" OK "L1 guard: effective (read from launch-result.json)"
+  else
+    rec "$sub-layers" FAIL "no 'L1 guard: effective' layer in $CLAIM_FILE (enforcement_hook=$(command timeout "$T" jq -r '.enforcement_hook // empty' "$CLAIM_FILE" 2>/dev/null); layers: $(command timeout "$T" jq -r '(.layers // []) | join(" | ")' "$CLAIM_FILE" 2>/dev/null))"
   fi
+  h=$CLAIM_TERMINAL
+  case "$h" in
+    ''|*[!0-9A-Za-z_-]*)
+      runlog "claim $t: no usable terminal handle in the result file; record: $CLAIM_JSON"
+      runlog "claim $t: launch record: $(command timeout "$T" jq -c '.launch // "none"' "${MAIN:-.}/.dev/issues/$n/worktree.json" 2>&1)"
+      pending "reason=terminal-handle-missing file=$CLAIM_FILE (full record in $PKG_ART/t10-run-log.md)" ;;
+  esac
   bash "$here/driver.sh" adopt "$3" "$h" >/dev/null
   GSID=$(wait_gsid "$label") || { rec "$sub-probe-loaded" FAIL "no session_id in $label.jsonl"; exit 1; }
   state_set "GSID_$t" "$GSID"
@@ -376,8 +374,8 @@ run_b() {
 run_c() {
   local s path cmd
   need N2 T2; need WT2 WT_T2
-  launch_real T2 "--pipeline worktree" gC "${OB_INITIAL_WAIT_S:-900}"
   MAIN=${OB_MAIN:-$(main_checkout)}
+  launch_real T2 "--pipeline worktree" gC "${OB_INITIAL_WAIT_S:-900}"
   path=$(plan_path gC "$WT2")
   [ -n "$path" ] || pending "reason=plan-path-not-on-screen name=gC"
   cmd=$(cat "$P/g07-c-implement.txt")
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (shell files are not indexed by codegraph, so this ran on the Grep floor): symbols launch_real, run_c, claim-T<n>.txt consumers outside session-gov.sh:
  .dev/issues/442/scripts/session-gov-selftest.sh:246:claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.txt"
  .dev/issues/442/scripts/session-gov-selftest.sh:247:printf 'RESUME_LAUNCH_T1=earlier\n' >> "$S/ob/state.env"
Same-file dependents (Task 3 owns them, still unchanged by design): release_session callers cat claim-T<n>.txt (run_b, run_c, run_d, run_e), inode_record and preflight_refusal read CLAIM_LAST/claim_has.
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
