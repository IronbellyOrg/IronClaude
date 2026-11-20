a1e2fccc638e10cffcda33551cfb0c731966ccbd
Review one task for spec compliance.

Task brief: ## Task 3: Read the release text and inode from the file; update the other callers

Depends on: Task 2

Edit `.dev/issues/442/scripts/session-gov.sh` (line numbers on master 1a6c8723f):

- `release_session` (lines 192 to 211): the second argument becomes the path of a saved claim JSON file (`$OB/claim-T<n>.json`); read `.release` with `jq -r '.release // empty'`. Replace the space-stripped `rm"..""..."` grep and `sed` (lines 196 to 200) with a bash `[[ $rel =~ rm\ \"([^\"]+)\"\ \"([^\"]+)\" ]]` match and `BASH_REMATCH`; the placeholder in the real text is `<session id>` with a space (`orca_worktree.py:1482`), so substitute `${p1//<session id>/$gsid}`. Keep the odd-session-id refusal (line 195), the fallback that records `release-text FAIL` and releases only this run's two own session files when the file's `release` has no `rm` pair (lines 201 to 205), the exact-path comparison (lines 206 to 208) and the line `rm -f -- "${p1:?}" "${p2:?}"` (line 209) word for word, because the runbook quotes them.
- Call sites: `run_b` line 330 (`$(cat "$OB/claim-T1.txt")`), `run_c` line 353, `run_d` line 382, `run_e` line 467 pass `"$OB/claim-T1.json"`, `claim-T2.json`, `claim-T3.json`, `claim-T4.json`.
- `inode_record` (lines 263 to 275): `want` comes from `$CLAIM_RELEASE` (`grep -oE 'inode number [0-9]+' | head -1 | tr -dc '0-9'`), replacing the `inodenumber[0-9]+` match on `CLAIM_LAST`; the three outcomes (match OK, mismatch FAIL, no number PENDING) and their record ids stay.
- `preflight_refusal` (lines 239 to 254): `claim_send "$N1" "--pipeline worktree"` stays; the `launched|already_launched` guard now reads `CLAIM_STATUS` from the file; the pass test becomes `[ "$CLAIM_STATUS" = failed ] && [ "$CLAIM_WARNING" = W-ENFORCEMENT-ABSENT ] && claim_detail_has "$2"`; the failure record names `file=$CLAIM_FILE` instead of `screen=`. The `no-record`, `no-mirror` and `pending` checks (lines 248 to 253) are not claim-text reads and stay.
- Update the header comment block of the file (lines 1 to 5) only if it names screen parsing of the claim; update the comment above the claim block to say the claim's result is read from `launch-result.json`.

Acceptance criteria:
- `bash -n .dev/issues/442/scripts/session-gov.sh` exits 0; `shellcheck --severity=warning` on the file exits 0 when a `shellcheck` binary is on `PATH` (none is installed in this workspace on 2026-11-20, so this check is UNVERIFIED locally; the repository's pre-commit config `.pre-commit-config.yaml` lines 98 to 102 runs it in CI; do not install it).
- `grep -n 'CLAIM_TXT\|CLAIM_LAST\|CLAIM_SCREEN\|claim_has\|terminal list\|claim-T[0-9]\.txt\|inodenumber' .dev/issues/442/scripts/session-gov.sh` prints nothing.
- The release line `rm -f -- "${p1:?}" "${p2:?}"` and the text `refusing an odd session id` still appear verbatim, each on one line, and `grep -c` of the string `refused: the printed rm paths are not this run` is still 1.
- No `eval`, `source` of file text or `bash -c` is introduced (`grep -nE '\beval\b|bash -c' .dev/issues/442/scripts/session-gov.sh` shows only lines already on master, if any).

AC ids in source order of the Acceptance criteria bullets: T3.AC1 (bash -n exits 0; shellcheck only if a binary exists), T3.AC2 (the grep for CLAIM_TXT, CLAIM_LAST, CLAIM_SCREEN, claim_has, terminal list, claim-T<n>.txt, inodenumber prints nothing), T3.AC3 (the release line, the odd-session-id text and the refused-rm-paths text still appear verbatim and the last is counted once), T3.AC4 (no eval, source of file text or bash -c introduced).
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

Start sha: a1e2fccc638e10cffcda33551cfb0c731966ccbd
Diff against the start snapshot: 
```diff
diff --git a/.dev/issues/442/scripts/session-gov.sh b/.dev/issues/442/scripts/session-gov.sh
index 49d597128..44c36bf56 100644
--- a/.dev/issues/442/scripts/session-gov.sh
+++ b/.dev/issues/442/scripts/session-gov.sh
@@ -141,7 +141,7 @@ claim_result_state() {  # claim_result_state <n>: prints missing, stale, unreada
   fi
   printf '%s' "$CLAIM_STATE"
 }
-load_claim_result() {  # load_claim_result: fill the CLAIM_* globals from the ok file named by CLAIM_FILE (jq only, no eval)
+load_claim_result() {  # load_claim_result: fill the CLAIM_* globals from the ok file named by CLAIM_FILE (jq only)
   CLAIM_STATUS=$(command timeout "$T" jq -r '.status' "$CLAIM_FILE")
   CLAIM_WARNING=$(command timeout "$T" jq -r '.warning // empty' "$CLAIM_FILE")
   CLAIM_DETAIL=$(command timeout "$T" jq -r '.detail // empty' "$CLAIM_FILE")
@@ -222,18 +222,17 @@ launch_real() {  # launch_real <T1..T4> <flags> <session name> [first-stop wait
   [ "${4:-0}" = 0 ] || wait_first_stop "$label" "$4" || pending "reason=no-first-stop label=$label"
 }
 
-# --- release: the claim's printed rm, only for this run's GSID --------------------
-release_session() {  # release_session <gsid> <claim text>
-  local gsid=$1 m p1 p2
+# --- release: the rm in the claim's launch-result.json, only for this run's GSID -----
+release_session() {  # release_session <gsid> <saved claim result file, $OB/claim-T<n>.json>
+  local gsid=$1 rel p1 p2
   case "$gsid" in ''|*[!0-9A-Za-z_-]*) die release "refusing an odd session id" ;; esac
-  m=$(printf '%s' "$2" | grep -oE 'rm"[^"]+""[^"]+"' | tail -1)
-  if [ -n "$m" ]; then
-    p1=$(printf '%s' "$m" | sed -E 's/^rm"([^"]+)""([^"]+)"$/\1/')
-    p2=$(printf '%s' "$m" | sed -E 's/^rm"([^"]+)""([^"]+)"$/\2/')
-    p1=${p1//<sessionid>/$gsid}; p2=${p2//<sessionid>/$gsid}
+  rel=$(command timeout "$T" jq -r '.release // empty' "$2" 2>/dev/null)
+  if [[ $rel =~ rm\ \"([^\"]+)\"\ \"([^\"]+)\" ]]; then
+    p1=${BASH_REMATCH[1]}; p2=${BASH_REMATCH[2]}
+    p1=${p1//<session id>/$gsid}; p2=${p2//<session id>/$gsid}   # the real text has the placeholder with a space (orca_worktree.py)
   else
-    # the claim session paraphrased the release text (no printed rm line, seen live): the same two files, named from this run's GSID
-    rec release-text FAIL "the claim output has no printed rm line; releasing this run's own two session files (UNVERIFIED claim text)"
+    # the result's release field has no rm pair: the same two files, named from this run's GSID
+    rec release-text FAIL "the result file's release field has no rm pair; releasing this run's own two session files (UNVERIFIED release text)"
     p1=$SESS/$gsid; p2=$SESS/$gsid.ok
   fi
   if [ "$p1" != "$SESS/$gsid" ] || [ "$p2" != "$SESS/$gsid.ok" ]; then
@@ -273,10 +272,10 @@ preflight_refusal() {  # preflight_refusal <tag> <needle>: runbook lines 546-552
   local now sig rec2
   claim_send "$N1" "--pipeline worktree"
   case "$CLAIM_STATUS" in launched|already_launched) die "b-$1" "a refused launch started an agent (status=$CLAIM_STATUS)" ;; esac
-  if [ "$CLAIM_STATUS" = failed ] && claim_has W-ENFORCEMENT-ABSENT && claim_has "$2"; then
+  if [ "$CLAIM_STATUS" = failed ] && [ "$CLAIM_WARNING" = W-ENFORCEMENT-ABSENT ] && claim_detail_has "$2"; then
     rec "b-$1-claim" OK "failed W-ENFORCEMENT-ABSENT"
   else
-    rec "b-$1-claim" FAIL "status=$CLAIM_STATUS screen=$CLAIM_SCREEN"
+    rec "b-$1-claim" FAIL "status=$CLAIM_STATUS warning=$CLAIM_WARNING file=$CLAIM_FILE"
   fi
   now=$(pend_count)
   if [ "$now" = "$PEND0" ]; then rec "b-$1-pending" OK "count $now"; else rec "b-$1-pending" FAIL "before=$PEND0 after=$now"; fi
@@ -295,7 +294,7 @@ ident() {  # ident <id> <pgrep pattern>: record what identify prints for that pr
 
 inode_record() {  # runbook step 2 (lines 576-580): the session file's inode against the number in the claim's release text
   local want have f=$SESS/$GSID
-  want=$(printf '%s' "$CLAIM_LAST" | grep -oE 'inodenumber[0-9]+' | head -1 | tr -dc '0-9')
+  want=$(printf '%s' "$CLAIM_RELEASE" | grep -oE 'inode number [0-9]+' | head -1 | tr -dc '0-9')
   if [ ! -e "$f" ]; then rec b-inode FAIL "no session file named $GSID in $SESS"; return 0; fi
   have=$(stat -c '%i %h' "$f")
   if [ -z "$want" ]; then
@@ -360,7 +359,7 @@ run_b() {
   n=$(command timeout "$T" jq -r 'select(.session_id) | .session_id' "$L.jsonl" | uniq | wc -l | tr -d ' ')
   rec b-session-ids OK "$n distinct id runs in the log (a second id after /clear is U18)"
   # release mid step 4 (runbook 635), then the final identify of sleep 241
-  release_session "$GSID" "$(cat "$OB/claim-T1.txt")"
+  release_session "$GSID" "$OB/claim-T1.json"
   ident b-id-241-released 'sleep 241'
   case "$IDENT_OUT" in
     no-process) : ;;
@@ -383,7 +382,7 @@ run_c() {
   gsend gC h2-T2 "$cmd" 1800
   ok_file_check "$GSID" c-implement-ok
   gsend gC h2-T2 "$(cat "$P/g02-commit.txt")" 600
-  release_session "$GSID" "$(cat "$OB/claim-T2.txt")"
+  release_session "$GSID" "$OB/claim-T2.json"
   printf 'SESSION_C_DONE\n'
 }
 
@@ -412,7 +411,7 @@ run_d() {
   done
   rec d-final-status OK "agent ended with git status --short"
   gsend gD h2-T3 "$(cat "$P/g02-commit.txt")" 600
-  release_session "$GSID" "$(cat "$OB/claim-T3.txt")"
+  release_session "$GSID" "$OB/claim-T3.json"
   printf 'SESSION_D_DONE\n'
 }
 
@@ -497,7 +496,7 @@ run_e() {
   gsend gE h2-T4 "$(cat "$P/g09-e-merge.txt")" 600
   restore_push
   rec e-versions OK "claude=$(command timeout "$T" claude --version 2>&1 | head -1) orca=$(command timeout "$T" orca --version 2>&1 | head -1) sha=$(command timeout "$T" sha256sum "$HOME/.claude/settings.json" "$HOME/.claude/hooks/launch-level-guard.sh" 2>&1 | tr '\n' ' ')"
-  release_session "$GSID" "$(cat "$OB/claim-T4.txt")"
+  release_session "$GSID" "$OB/claim-T4.json"
   printf 'SESSION_E_DONE\n'
 }
 
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (shell and markdown files are not indexed by codegraph, so this ran on the Grep floor): symbols release_session, inode_record, preflight_refusal, claim-T<n>.txt, and the strings the runbook quotes, outside session-gov.sh:
  .dev/issues/442/observation-runbook.md:767:- **The O-10 conflict edit** during the `/sc:pr-submit` monitoring window is made through `gh_fork api repos/IronbellyOrg/IronC
  .dev/issues/442/observation-runbook.md:769:- **The release.** The LL-TAMPER block applies only to a governed session, so the claim's `release` line, an `rm`, is run from 
  .dev/issues/442/observation-runbook.md:846:| 6 | `session-gov.sh b`, `c`, `d`, `e` | `runbook §2.2 governed sessions B to E` (session-gov.sh:2) |
  .dev/issues/442/observation-runbook.md:856:| `reason=needs-input` (session-gov.sh:82) | Same as `NEEDS_INPUT`: read the screen file, answer only a disposable target, and 
  .dev/issues/442/scripts/session-gov-selftest.sh:246:claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.txt"
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
