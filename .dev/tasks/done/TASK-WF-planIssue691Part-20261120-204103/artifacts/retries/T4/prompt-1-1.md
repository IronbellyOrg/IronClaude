c69194da6e2f9d7bd78ddf4af97e9f97c5666cbb
Review one task for spec compliance.

Task brief: ## Task 4: Extend session-gov-selftest.sh with the file fixtures and the new cases

Depends on: Task 3

Edit `.dev/issues/442/scripts/session-gov-selftest.sh` (379 lines on master). The test must prove the script reads the file and ignores the screen:

- Stub `orca` (lines 23 to 51): log every call to `$L/calls.log`. On `terminal send` to handle `h-claim` whose text starts `/sc:issue --claim <N>`: take the first queued fixture of `q-h-claim` as the body of `$OB_STUB_MAIN/.dev/issues/<N>/launch-result.json` (so every existing `qpush h-claim n "$(claim_json ...)"` call becomes a file fixture without being rewritten), and put a deliberately wrong text on the claim screen (`"terminal":"term_screen_wrong"` and an `rm "/nonexistent/a" "/nonexistent/b"` line, no `L1 guard` line) so a script that still parsed the screen would fail. `STUB_RESULT_MODE` selects: unset writes the fixture fresh; `none` writes nothing; `stale` writes it then runs `touch -d '2 hours ago'`; `oldlaunched` writes it fresh but with `launched_at` set to a day ago; `symlink` makes the path a symlink to the fixture. Export `OB_STUB_MAIN="$S/main"` in `runsub` (line 131).
- Replace the yaml-form case (lines 254 to 263, `launch_status:` text) with an unreadable-file case: fixture body is not JSON; expect rc 1 and `FAIL claim-result`.
- Rename `claim-T1.txt` to `claim-T1.json` in the resume case (line 246).
- New cases, each with its own `mkenv` scenario, named in the output so a failure is attributable:
  - fresh file: the existing sessions b, c, d, e keep passing (that is the fresh case); plus `cmp` of `$S/ob/claim-T2.json` against the result file for session c, and a check that `calls.log` has no line containing `terminal list` in any scenario.
  - screen ignored: with the misleading claim screen, session c adopts `term_gc` (`driver.sh adopt` target visible in `calls.log` or the `OK c-launched terminal=term_gc` record) and releases the session files named by the file's `rm` pair.
  - missing: `STUB_RESULT_MODE=none` gives rc 0 and `PENDING reason=claim-result-missing`, and no `/sc:implement` is sent afterwards.
  - stale: `STUB_RESULT_MODE=stale` gives rc 0 and `PENDING reason=claim-result-stale`; `oldlaunched` does the same.
  - unreadable: not-JSON body, a JSON array body and `{}` (no string `status`) each give rc 1 and `FAIL claim-result`; `symlink` gives rc 1.
  - failed result: a `status: failed` file for a real launch (`launch_real`) gives rc 1 and `FAIL c-claim` with the file's warning in the text; the session b refusal cases (lines 194 to 224) already cover `failed W-ENFORCEMENT-ABSENT` through the file.
  - already_launched: pre-seed `$S/main/.dev/issues/421/launch-result.json` with a `launched` result, back-date it with `touch -d '2 hours ago'`, keep a `cp -p` copy, run with `STUB_RESULT_MODE=none` (the claim writes nothing, as Part A does for `already_launched`); expect `PENDING reason=claim-result-stale`, and `cmp` plus `stat -c %Y` prove the pre-seeded file is byte- and mtime-identical afterwards.
  - terminal null: a launched fixture with `"terminal": null` gives `PENDING reason=terminal-handle-missing` and no `terminal list` call.
  - layers: a launched fixture whose `layers` lack `L1 guard: effective` records `FAIL c-layers` and the run continues as it did before this change.
  - resume with only a text copy: `RESUME_LAUNCH_T1` set and only `claim-T1.txt` present gives rc 1 and a `FAIL resume` record, and no claim is sent.
- Keep section 10 (prompt files equal runbook lines 536 to 697) unchanged.

Acceptance criteria:
- `bash .dev/issues/442/scripts/session-gov-selftest.sh` prints only `OK ...` lines (no `FAIL`) and exits 0, and its `OK` lines include each case name above. Run from the repository root; it needs `jq`, `git`, `bash` and `/tmp` only (no `uv`).
- Reverting Task 1 to the master `claim_send` (screen parsing) makes at least the screen-ignored, missing and stale cases fail, shown by running the new self-test against the master `session-gov.sh` from `git show master:.dev/issues/442/scripts/session-gov.sh` in a temporary copy of the scripts folder; record the failing case names in `./artifacts/t4-negative-check.txt`.
- The self-test removes everything it creates (its `trap` removes `$T`); `ls /tmp/ob-gov.*` after the run lists nothing new.

AC ids in source order of the Acceptance criteria bullets: T4.AC1 (the self-test prints only OK lines and exits 0, and its OK lines include each case name), T4.AC2 (reverting Task 1 to master screen parsing makes at least the screen-ignored, missing and stale cases fail; failing case names recorded in ./artifacts/t4-negative-check.txt), T4.AC3 (the self-test removes everything it creates; /tmp/ob-gov.* lists nothing new).
Evidence file for T4.AC2: .dev/tasks/to-do/TASK-WF-planIssue691Part-20261120-204103/artifacts/t4-negative-check.txt (produced by running the new self-test against git show HEAD:.dev/issues/442/scripts/session-gov.sh, where HEAD is the commit before this change; the plan calls it master 1a6c8723f).
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

Start sha: c69194da6e2f9d7bd78ddf4af97e9f97c5666cbb
Diff against the start snapshot: 
```diff
diff --git a/.dev/issues/442/scripts/session-gov-selftest.sh b/.dev/issues/442/scripts/session-gov-selftest.sh
index de74f72f0..4a8ef11d8 100644
--- a/.dev/issues/442/scripts/session-gov-selftest.sh
+++ b/.dev/issues/442/scripts/session-gov-selftest.sh
@@ -23,6 +23,7 @@ trap 'for p in "${SLEEPS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null; done;
 cat > "$T/bin/orca" <<'STUB'
 #!/usr/bin/env bash
 L=$OB_STUB_DIR; h=""; t=""; prev=""
+printf '%s\n' "$*" >> "$L/calls.log"
 for a in "$@"; do
   [ "$prev" = --terminal ] && h=$a
   [ "$prev" = --text ] && t=$a
@@ -37,7 +38,25 @@ case "$1 $2" in
     # STUB_OK_FILE: a typed /sc:implement (and nothing else) creates the unlock file
     case "$t" in /sc:implement\ *) [ -z "${STUB_OK_FILE:-}" ] || : > "$STUB_OK_FILE" ;; esac
     f=$(ls -1 "$L/q-$h"/*.txt 2>/dev/null | head -1)
-    [ -n "$f" ] && mv "$f" "$L/screen-$h.txt"
+    case "$h $t" in
+      'h-claim /sc:issue --claim '*)
+        # a claim saves its result as <main>/.dev/issues/<N>/launch-result.json (issue 691, Part A) and the screen holds
+        # a deliberately wrong text (a terminal key, an rm line, no L1 guard line): a script that read the screen would fail
+        n=$(printf '%s' "$t" | awk '{print $3}'); r=$OB_STUB_MAIN/.dev/issues/$n/launch-result.json
+        if [ -n "$f" ]; then
+          case "${STUB_RESULT_MODE:-}" in
+            none) ;;
+            symlink) cp "$f" "$L/linked-result.json"; rm -f "$r"; ln -s "$L/linked-result.json" "$r" ;;
+            oldlaunched) jq --arg d "$(date -u -d '1 day ago' +%FT%TZ)" '.launched_at = $d' "$f" > "$r" ;;
+            freshlaunched) jq --arg d "$(date -u +%FT%TZ)" '.launched_at = $d' "$f" > "$r" ;;
+            stale) cp "$f" "$r"; touch -d '2 hours ago' "$r" ;;
+            *) cp "$f" "$r" ;;
+          esac
+          rm -f "$f"
+        fi
+        printf 'claim done\n{"terminal":"term_screen_wrong"}\nrm "/nonexistent/a" "/nonexistent/b"\n' > "$L/screen-h-claim.txt" ;;
+      *) [ -n "$f" ] && mv "$f" "$L/screen-$h.txt" ;;
+    esac
     for lg in "$OB"/logs/*.jsonl; do
       [ -e "$lg" ] || continue
       # STUB_STOP_ONLY=<label>: only that log gets a Stop (the governed agent's first turn stays open)
@@ -128,7 +147,7 @@ seed() {  # seed <label> <gsid> [extra log lines...]: probe log with a session i
 }
 runsub() {  # runsub <b|c|d|e> [VAR=value ...]: sets OUT and RC
   local sub=$1; shift
-  OUT=$(env OB="$S/ob" HOME="$H" OB_STUB_DIR="$S/stub" OB_RESULTS="$S/results.md" OB_MAIN="$S/main" \
+  OUT=$(env OB="$S/ob" HOME="$H" OB_STUB_DIR="$S/stub" OB_STUB_MAIN="$S/main" OB_RESULTS="$S/results.md" OB_MAIN="$S/main" \
         OB_POLL_S=0 OB_LAUNCH_WAIT_S=2 OB_INITIAL_WAIT_S=2 OB_D_WAIT_S=2 OB_E_WAIT_S=2 OB_QUIET_S=0 OB_TIMEOUT_S=20 OB_CLAIM_POLLS=0 \
         PATH="$T/bin:$PATH" "$@" timeout 120 bash "$here/session-gov.sh" "$sub" 2>&1); RC=$?
 }
@@ -243,7 +262,7 @@ has b-inode-unreadable "$OUT" 'PENDING b-inode the claim printed no inode number
 # a launch that already happened in an earlier run is not claimed or refused again: steps 1 and 2 are skipped
 mkenv b7; results PASS PASS
 seed T1 gsid-b-1; printf x > "$H/.claude/state/launch-level/sessions/gsid-b-1"
-claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.txt"
+claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.json"
 printf 'RESUME_LAUNCH_T1=earlier\n' >> "$S/ob/state.env"
 printf 'plan written: .dev/issues/421/plan.md\n' > "$S/stub/screen-term_gb.txt"
 runsub b
@@ -251,16 +270,82 @@ has b-resume-skipped "$OUT" 'OK b-steps-1-2-skipped'
 has b-resume-launch "$OUT" 'OK b-resume launch of T1 reused'
 hasnt b-resume-no-claim "$(sent)" '/sc:issue --claim 421'
 
-# the claim result in the form the real claim session prints ("launch_status: <value>" lines, not JSON) is read too
-mkenv b6; results PASS PASS
+# a launch that saved claim text only (an older run) is not claimed again: a repeat is already_launched and writes no result file
+mkenv b8; results PASS PASS
 seed T1 gsid-b-1; printf x > "$H/.claude/state/launch-level/sessions/gsid-b-1"
-yaml() { printf 'issue_number: 421\nlaunch_status: failed\nlaunch_warning: W-ENFORCEMENT-ABSENT\nlaunch_detail: %s\nenforcement_hook: missing\n' "$1"; }
-qpush h-claim 1 "$(yaml 'settings.local.json cannot be read as JSON')"
-qpush h-claim 2 "$(yaml 'x sets disableAllHooks to true, so no hook runs')"
-qpush h-claim 3 "$(claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok")"
+claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$S/ob/claim-T1.txt"
+printf 'RESUME_LAUNCH_T1=earlier\n' >> "$S/ob/state.env"
 runsub b
-has b-yaml-claim "$OUT" 'OK b-badjson-claim failed W-ENFORCEMENT-ABSENT'
-has b-yaml-claim2 "$OUT" 'OK b-nohooks-claim failed W-ENFORCEMENT-ABSENT'
+ck resume-text-only-rc "$RC" 1; has resume-text-only-msg "$OUT" 'FAIL resume'
+hasnt resume-text-only-no-claim "$(sent)" '/sc:issue --claim 421'
+
+# --- 4b. the claim result is read from launch-result.json, never from the screen (issue 691, Part B) ------------
+# every stub claim leaves a wrong screen (terminal term_screen_wrong, an rm of /nonexistent paths, no L1 guard line)
+cenv() {  # cenv <tag> [jq filter on the launched fixture] [raw fixture body]: a session c scenario, T2 is issue 422
+  mkenv "$1"; results PASS PASS; seed T2 gsid-c-1
+  printf x > "$H/.claude/state/launch-level/sessions/gsid-c-1"
+  if [ $# -ge 3 ]; then qpush h-claim 1 "$3"
+  else qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gc "$(RELP)" "$(RELP).ok" | jq -c "${2:-.}")"; fi
+  printf 'run /sc:implement .dev/issues/422/plan.md\n' > "$S/stub/screen-term_gc.txt"
+  mkdir -p "$S/wts/T2/.dev/issues/422"; : > "$S/wts/T2/.dev/issues/422/plan.md"
+}
+cenv fresh
+runsub c; RES=$S/main/.dev/issues/422/launch-result.json
+ck fresh-file-rc "$RC" 0; ck fresh-file-done "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
+ck fresh-file-saved-copy-equal "$(cmp -s "$S/ob/claim-T2.json" "$RES" && echo equal)" equal
+has screen-ignored-adopts-file-terminal "$OUT" 'OK c-launched terminal=term_gc gsid=gsid-c-1'
+hasnt screen-ignored-not-screen-terminal "$OUT" 'term_screen_wrong'
+has screen-ignored-layers-from-file "$OUT" 'OK c-layers L1 guard: effective (read from launch-result.json)'
+ck screen-ignored-released-file-pair "$([ ! -e "$H/.claude/state/launch-level/sessions/gsid-c-1" ] && echo gone)" gone
+cenv freshstamp
+runsub c STUB_RESULT_MODE=freshlaunched
+ck fresh-launched-at-rc "$RC" 0; ck fresh-launched-at-done "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
+cenv missing
+runsub c STUB_RESULT_MODE=none
+ck missing-rc "$RC" 0; has missing-msg "$OUT" 'PENDING reason=claim-result-missing'
+ck missing-no-implement "$(sent | grep -c '/sc:implement' || true)" 0
+cenv stale
+runsub c STUB_RESULT_MODE=stale
+ck stale-rc "$RC" 0; has stale-msg "$OUT" 'PENDING reason=claim-result-stale'
+ck stale-no-implement "$(sent | grep -c '/sc:implement' || true)" 0
+cenv oldlaunched
+runsub c STUB_RESULT_MODE=oldlaunched
+ck stale-launched-at-rc "$RC" 0; has stale-launched-at-msg "$OUT" 'PENDING reason=claim-result-stale'
+cenv notjson . 'this is not json'
+runsub c
+ck unreadable-notjson-rc "$RC" 1; has unreadable-notjson-msg "$OUT" 'FAIL claim-result'
+cenv jsonarray . '[1,2]'
+runsub c
+ck unreadable-array-rc "$RC" 1; has unreadable-array-msg "$OUT" 'FAIL claim-result'
+cenv nostatus . '{}'
+runsub c
+ck unreadable-nostatus-rc "$RC" 1; has unreadable-nostatus-msg "$OUT" 'FAIL claim-result'
+cenv symlink
+runsub c STUB_RESULT_MODE=symlink
+ck unreadable-symlink-rc "$RC" 1; has unreadable-symlink-msg "$OUT" 'FAIL claim-result'
+cenv failedresult '.status="failed" | .warning="W-ENFORCEMENT-ABSENT" | .detail="refused"'
+runsub c
+ck failed-result-rc "$RC" 1; has failed-result-msg "$OUT" 'FAIL c-claim status=failed warning=W-ENFORCEMENT-ABSENT'
+cenv terminalnull '.terminal = null'
+runsub c
+ck terminal-null-rc "$RC" 0; has terminal-null-msg "$OUT" 'PENDING reason=terminal-handle-missing'
+cenv terminalodd '.terminal = "a b;c"'
+runsub c
+ck terminal-odd-rc "$RC" 0; has terminal-odd-msg "$OUT" 'PENDING reason=terminal-handle-missing'
+cenv nolayer '.layers = ["L2 pre-push: absent"]'
+runsub c
+ck layers-rc "$RC" 0; has layers-fail "$OUT" 'FAIL c-layers no '"'"'L1 guard: effective'"'"' layer'
+ck layers-run-continues "$(printf '%s' "$OUT" | tail -1)" SESSION_C_DONE
+# an already_launched claim writes no new result (Part A): the older result stays, counts as missing, and is left byte- and mtime-identical
+mkenv already; results PASS PASS
+RES=$S/main/.dev/issues/421/launch-result.json
+claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok" > "$RES"; touch -d '2 hours ago' "$RES"
+cp -p "$RES" "$S/prev-result.json"; before=$(stat -c %Y "$RES")
+qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gb "$(RELP)" "$(RELP).ok")"
+runsub b STUB_RESULT_MODE=none
+ck already-launched-rc "$RC" 0; has already-launched-msg "$OUT" 'PENDING reason=claim-result-stale'
+ck already-launched-bytes "$(cmp -s "$S/prev-result.json" "$RES" && echo equal)" equal
+ck already-launched-mtime "$(stat -c %Y "$RES")" "$before"
 
 # --- 5. session b: a failed backup stops before anything is touched -------------------------
 mkenv b2; results PASS PASS; rm -f "$S/wts/T1/.claude/settings.local.json"
@@ -366,6 +451,9 @@ qpush h-claim 1 "$(claim_json launched W-L2-ABSENT x term_gc "$(RELP)" "$(RELP).
 runsub c STUB_STOP_ONLY=claim OB_INITIAL_WAIT_S=1
 has c-first-stop-gate "$OUT" 'PENDING reason=no-first-stop label=h2-T2'
 
+# --- 9d. no scenario ever listed terminals: the handle comes from launch-result.json only -------------------------
+ck no-terminal-list-in-any-scenario "$(cat "$T"/*/stub/calls.log 2>/dev/null | grep -c 'terminal list' || true)" 0
+
 # --- 10. every prompt file equals its runbook text block, byte for byte (lines 536-697) ----------------
 names=(g01-b-implement g02-commit g03-approved g04-gov-bg g05-gov-det g06-gov-clear g07-c-implement g08-e-push g09-e-merge)
 sed -n '536,697p' "$RB" | awk -v d="$T/want" '/^```text$/{f=1;n++;next} /^```$/{f=0;next} f{print > sprintf("%s-%d.txt", d, n)}'
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (shell files are not indexed by codegraph, so this ran on the Grep floor): the only caller of session-gov-selftest.sh is selftest.sh:
  124:timeout 300 bash "$here/session-gov-selftest.sh" || fail gov "session-gov-selftest exited $?"
Run evidence taken by the orchestrator: bash session-gov-selftest.sh printed 135 OK lines, 0 FAIL, exit 0 in 20 s; ls /tmp/ob-gov.* before and after identical.
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
