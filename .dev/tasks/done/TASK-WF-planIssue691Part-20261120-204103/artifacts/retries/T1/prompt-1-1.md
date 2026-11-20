02fe6e07f5be894dd5dda69dc9386ef6f334bb92
Review one task for spec compliance.

Task brief: ## Task 1: Replace claim_send and claim_has with a file reader in session-gov.sh

Edit `.dev/issues/442/scripts/session-gov.sh`. Do not change lines 1 to 113 (header, gate, `gsend`, `screen_text`, `wait_*`), so the runbook citation `session-gov.sh:82` stays valid. Replace the block that runs from the comment at line 114 through `claim_has` ending at line 152 (`claim_send` at 118 and `claim_has` at 148 on master 1a6c8723f) with:

- Globals `CLAIM_START`, `CLAIM_FILE`, `CLAIM_JSON`, `CLAIM_STATUS`, `CLAIM_WARNING`, `CLAIM_DETAIL`, `CLAIM_TERMINAL`, `CLAIM_RELEASE` (replacing `CLAIM_TXT`, `CLAIM_LAST` and `CLAIM_SCREEN`).
- `claim_file <n>`: prints `$MAIN/.dev/issues/<n>/launch-result.json`; stops with `die claim-result "MAIN is not set"` when `MAIN` is empty.
- `claim_result_state <n>`: sets `CLAIM_FILE` and a one-line `CLAIM_WHY`, and prints exactly one of `missing`, `stale`, `unreadable`, `ok`. Rules: not a regular file or a symlink gives `missing` for an absent path and `unreadable` for a symlink; `stat -c %Y` below `CLAIM_START` gives `stale`; `jq -e 'type == "object" and (.status | type == "string")'` failing gives `unreadable`; `launched_at` a string whose `date -u -d` epoch is below `CLAIM_START` gives `stale`; otherwise `ok`.
- `load_claim_result`: after `ok`, fills the globals with one `command timeout "$T" jq -r` call each (`.status`, `.warning // empty`, `.detail // empty`, `.terminal // empty`, `.release // empty`) and `CLAIM_JSON=$(jq -c .)` for log lines. No `eval`.
- `claim_send <issue number> <flags>`: keep the vanished-terminal check (lines 119 to 123) and the `/clear` send (line 127); then set `CLAIM_START=$(date +%s)`, fire the claim exactly as line 129 does, keep the `rec send-N` line, and poll up to `${OB_CLAIM_POLLS:-180}` times with `${OB_CLAIM_SLEEP_S:-5}` between: `ok` breaks the loop; the screen dialog check (`Do you want|/login|Not logged in`) keeps its `pending "step=$SN reason=needs-input name=claim"`. After the loop evaluate once more (so `OB_CLAIM_POLLS=0`, used by the self-tests, still reads the file once) and map: `ok` loads the result; `missing` gives `pending "reason=claim-result-missing file=$CLAIM_FILE"`; `stale` gives `pending "reason=claim-result-stale file=$CLAIM_FILE ($CLAIM_WHY; a claim that is already_launched writes no new result)"`; `unreadable` gives `die claim-result "$CLAIM_WHY"`. The poll loop treats `stale`, `missing` and `unreadable` alike as "not ready yet".
- `claim_layer_has <text>`: true when some element of `.layers` starts with the text (`jq -e --arg s "$1" '(.layers // []) | any(.[]; startswith($s))'`). `claim_detail_has <text>`: true when `.detail` contains the text (`jq -e --arg s "$1" '(.detail // "") | contains($s)'`). Both read `$CLAIM_FILE`. Delete `claim_has`.

Acceptance criteria:
- `grep -n 'CLAIM_TXT\|CLAIM_LAST\|CLAIM_SCREEN\|claim_has' .dev/issues/442/scripts/session-gov.sh` prints nothing once Tasks 1 to 3 are done (until Task 3 finishes the callers, `bash -n` may fail; after Task 3 it must pass).
- `claim_send` contains no `grep`, `sed` or `case` over screen text for status, terminal, layers or release, and the only `screen_text`/`driver.sh screen claim` uses left inside it are the vanished-terminal check and the dialog check.
- The four states map to the exits listed in Constraints: missing and stale exit 0 with a `PENDING reason=claim-result-` line, unreadable exits 1 with `FAIL claim-result`.
- Lines 1 to 113 of `session-gov.sh` are byte-identical to master (`git diff -U0 .dev/issues/442/scripts/session-gov.sh` shows no hunk starting at or before line 113).

AC ids in source order of the Acceptance criteria bullets: T1.AC1 (grep prints nothing), T1.AC2 (claim_send has no screen parsing), T1.AC3 (four states map to the exits), T1.AC4 (lines 1 to 113 byte-identical).
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

Start sha: 02fe6e07f5be894dd5dda69dc9386ef6f334bb92
Diff against the start snapshot: 
```diff
diff --git a/.dev/issues/442/scripts/session-gov.sh b/.dev/issues/442/scripts/session-gov.sh
index 4a24985e8..4fc08e07e 100644
--- a/.dev/issues/442/scripts/session-gov.sh
+++ b/.dev/issues/442/scripts/session-gov.sh
@@ -111,44 +111,79 @@ wait_gsid() {  # wait_gsid <label>: the governed session id from the probe log
   done
 }
 
-# --- the claim and its printed result ---------------------------------------------
-# CLAIM_TXT is the claim session's screen with spaces, newlines and backslashes
-# removed, so wrapped JSON still matches; CLAIM_LAST is the text after the newest
-# "status" key (the stale results of earlier claims stay above it).
+# --- the claim and its result file ------------------------------------------------
+# The claim saves its result as $MAIN/.dev/issues/<N>/launch-result.json (issue 691, Part A). Terminal, layers
+# and release text are read from that file with jq, never from the claim session's screen. The screen is read
+# for two jobs only: a vanished claim terminal and a login or permission dialog.
+CLAIM_START=0; CLAIM_FILE=""; CLAIM_STATE=""; CLAIM_WHY=""
+CLAIM_JSON=""; CLAIM_STATUS=""; CLAIM_WARNING=""; CLAIM_DETAIL=""; CLAIM_TERMINAL=""; CLAIM_RELEASE=""
+claim_file() {  # claim_file <issue number>: the result file of that claim, in the main checkout
+  [ -n "${MAIN:-}" ] || die claim-result "MAIN is not set"
+  printf '%s/.dev/issues/%s/launch-result.json' "$MAIN" "$1"
+}
+claim_result_state() {  # claim_result_state <n>: prints missing, stale, unreadable or ok; also sets CLAIM_STATE, CLAIM_FILE, CLAIM_WHY
+  local mt la le
+  [ -n "${MAIN:-}" ] || die claim-result "MAIN is not set"   # not inside the $(...) below, where die would only end the subshell
+  CLAIM_FILE=$(claim_file "$1"); CLAIM_WHY=""
+  if [ -L "$CLAIM_FILE" ]; then CLAIM_STATE=unreadable; CLAIM_WHY="$CLAIM_FILE is a symlink"
+  elif [ ! -e "$CLAIM_FILE" ]; then CLAIM_STATE=missing; CLAIM_WHY="$CLAIM_FILE does not exist"
+  elif [ ! -f "$CLAIM_FILE" ]; then CLAIM_STATE=unreadable; CLAIM_WHY="$CLAIM_FILE is not a regular file"
+  else
+    mt=$(stat -c %Y "$CLAIM_FILE" 2>/dev/null || echo 0)
+    la=$(command timeout "$T" jq -r 'if (.launched_at | type) == "string" then .launched_at else empty end' "$CLAIM_FILE" 2>/dev/null)
+    le=""; [ -z "$la" ] || le=$(date -u -d "$la" +%s 2>/dev/null)
+    if [ "$mt" -lt "$CLAIM_START" ]; then CLAIM_STATE=stale; CLAIM_WHY="mtime $mt is older than the claim start $CLAIM_START"
+    elif ! command timeout "$T" jq -e 'type == "object" and (.status | type == "string")' "$CLAIM_FILE" >/dev/null 2>&1; then
+      CLAIM_STATE=unreadable; CLAIM_WHY="$CLAIM_FILE is not a JSON object with a string status"
+    elif [ -n "$le" ] && [ "$le" -lt "$CLAIM_START" ]; then CLAIM_STATE=stale; CLAIM_WHY="launched_at $la is older than the claim start $CLAIM_START"
+    else CLAIM_STATE=ok
+    fi
+  fi
+  printf '%s' "$CLAIM_STATE"
+}
+load_claim_result() {  # load_claim_result: fill the CLAIM_* globals from the ok file named by CLAIM_FILE (jq only, no eval)
+  CLAIM_STATUS=$(command timeout "$T" jq -r '.status' "$CLAIM_FILE")
+  CLAIM_WARNING=$(command timeout "$T" jq -r '.warning // empty' "$CLAIM_FILE")
+  CLAIM_DETAIL=$(command timeout "$T" jq -r '.detail // empty' "$CLAIM_FILE")
+  CLAIM_TERMINAL=$(command timeout "$T" jq -r '.terminal // empty' "$CLAIM_FILE")
+  CLAIM_RELEASE=$(command timeout "$T" jq -r '.release // empty' "$CLAIM_FILE")
+  CLAIM_JSON=$(command timeout "$T" jq -c . "$CLAIM_FILE")
+}
 claim_send() {  # claim_send <issue number> <flags>
   # a claim terminal that no longer exists shows an empty screen for ever: stop at once, send nothing
   local cs; cs=$(bash "$here/driver.sh" screen claim 2>/dev/null | tail -1)
   if [ -z "$cs" ] || [ "$(command timeout "$T" jq -r '(.result.terminal.tail // []) | length' "$cs" 2>/dev/null || echo 0)" = 0 ]; then
     pending "reason=claim-terminal-gone screen=${cs:-none}"
   fi
-  # A clean screen first, so the result read below is this claim's. Then type and return at once: the driver's own turn
-  # wait has no probe log for the claim session and can hold the full 900 s after the claim is done (seen live).
+  # A clean screen first. Then type and return at once: the driver's own turn wait has no probe log for the claim
+  # session and can hold the full 900 s after the claim is done (seen live). CLAIM_START is taken after the /clear:
+  # a result file older than it belongs to an earlier claim and counts as missing.
   local i raw fo
   if [ "${OB_CLAIM_POLLS:-180}" -ne 0 ]; then bash "$here/driver.sh" send claim "/clear" claim 60 >/dev/null 2>&1; fi
+  CLAIM_START=$(date +%s)
   SN=$((SN+1))
   fo=$(bash "$here/driver.sh" fire claim "/sc:issue --claim $1 $2" 2>&1) || die "send-$SN" "claim send failed: $(printf '%s' "$fo" | tail -1)"
   rec "send-$SN" OK "claim claim /sc:issue --claim $1 $2"
   for i in $(seq 1 "${OB_CLAIM_POLLS:-180}"); do
+    claim_result_state "$1" >/dev/null
+    [ "$CLAIM_STATE" = ok ] && break
     raw=$(screen_text claim)
-    if printf '%s' "$raw" | grep -qE 'launch_status:|"status"' && ! printf '%s' "$raw" | grep -q 'esc to interrupt'; then break; fi
     if printf '%s' "$raw" | grep -qE 'Do you want|/login|Not logged in'; then pending "step=$SN reason=needs-input name=claim"; fi
     command sleep "${OB_CLAIM_SLEEP_S:-5}"
   done
-  CLAIM_SCREEN=$(bash "$here/driver.sh" screen claim)
-  raw=$(command timeout "$T" jq -r '.result.terminal.tail // [] | join("\n")' "$CLAIM_SCREEN" 2>/dev/null)
-  CLAIM_TXT=$(printf '%s' "$raw" | tr -d ' \t\r\n\\')
-  case "$CLAIM_TXT" in
-    *'"status":"'*) CLAIM_LAST=${CLAIM_TXT##*\"status\":\"}; CLAIM_STATUS=${CLAIM_LAST%%\"*} ;;
-    *launch_status:*)   # the claim prints "launch_status: <value>" lines (seen live); the text after the newest issue_number line is this claim's
-      CLAIM_STATUS=$(printf '%s\n' "$raw" | grep -oE 'launch_status: *[a-z_]+' | tail -1 | sed 's/.*: *//')
-      CLAIM_LAST=${CLAIM_TXT##*issue_number:}; [ -n "$CLAIM_LAST" ] || CLAIM_LAST=$CLAIM_TXT ;;
-    *) pending "reason=claim-unreadable screen=$CLAIM_SCREEN" ;;
+  claim_result_state "$1" >/dev/null   # once more after the loop, so OB_CLAIM_POLLS=0 still reads the file once
+  case "$CLAIM_STATE" in
+    ok) load_claim_result ;;
+    missing) pending "reason=claim-result-missing file=$CLAIM_FILE" ;;
+    stale) pending "reason=claim-result-stale file=$CLAIM_FILE ($CLAIM_WHY; a claim that is already_launched writes no new result)" ;;
+    *) die claim-result "$CLAIM_WHY" ;;
   esac
 }
-claim_has() {  # claim_has <text>: the newest claim result contains that text
-  local n; n=$(printf '%s' "$1" | tr -d ' ')
-  case "$CLAIM_LAST" in *"$n"*) return 0 ;; esac
-  return 1
+claim_layer_has() {  # claim_layer_has <text>: some element of .layers in the result file starts with that text
+  command timeout "$T" jq -e --arg s "$1" '(.layers // []) | any(.[]; startswith($s))' "$CLAIM_FILE" >/dev/null 2>&1
+}
+claim_detail_has() {  # claim_detail_has <text>: .detail in the result file contains that text
+  command timeout "$T" jq -e --arg s "$1" '(.detail // "") | contains($s)' "$CLAIM_FILE" >/dev/null 2>&1
 }
 pend_count() { ls -A "$HOME/.claude/state/launch-level/pending" 2>/dev/null | wc -l | tr -d ' '; }
 
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (shell and markdown files are not indexed by codegraph, so this ran on the Grep floor): symbols claim_send, claim_has, CLAIM_TXT, CLAIM_LAST, CLAIM_SCREEN outside session-gov.sh:
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
