---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-planIssue691Part-20261120-204103
version: "1"
priority: Medium
created_date: "2026-11-20"
---

# Issue 691 Part B: the #442 observation scripts read launch-result.json only

Source: ./source.md
Goal: `.dev/issues/442/scripts/session-gov.sh` and `.dev/issues/442/observation-runbook.md` take the claim's terminal handle, layers and release text from `.dev/issues/<N>/launch-result.json` in the main checkout, never from the claim session's screen and never from an `orca terminal list` lookup; a result file older than the claim's start counts as missing; every self-test of the folder still ends in `SELFTEST_OK`.

## Constraints

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

## Phase 1: session-gov.sh reads the claim result from the file

## Task 1: Replace claim_send and claim_has with a file reader in session-gov.sh

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

## Task 2: Make launch_real use the file's terminal, layers and a saved copy

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

## Task 3: Read the release text and inode from the file; update the other callers

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

## Phase 2: session-gov self-test covers the file

## Task 4: Extend session-gov-selftest.sh with the file fixtures and the new cases

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

## Phase 3: runbook wording and anchors

## Task 5: Point the runbook at launch-result.json

Depends on: Task 3

Edit `.dev/issues/442/observation-runbook.md`. Every edit inside lines 1 to 698 replaces text within its existing physical line; the line count above line 698 does not change. Read each line first (line numbers on master 1a6c8723f):

- Line 534: the sentence `The claim prints one result with ... Copy all of them into the results file.` becomes: the claim saves its launch result as `.dev/issues/<N>/launch-result.json` in the main checkout, with `status`, `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook`, `release` and `layers` (VERIFIED by reading `write_launch_result` in `orca_worktree.py` and `refs/claim.md` line 125); read terminal, layers and release from that file with `jq`, never from the agent's printed text and never from `orca terminal list`; a file whose mtime is older than the moment the claim was sent counts as missing; that a live claim leaves the file is UNVERIFIED until the owner-approved live OB-H2 rerun; copy the file's contents into the results file.
- Lines 546 and 560: add that `status`, `warning` and `detail` are read from the file (`jq '{status,warning,detail}' .dev/issues/<T1>/launch-result.json` in the main checkout), keeping the existing expectations and the VERIFIED citations.
- Line 566: `record the layers lines and the warning as printed` becomes recorded from the file (`jq -r '.layers[], .warning' ...`); keep the `W-L2-ABSENT` UNVERIFIED sentence.
- Line 580: the inode number is the one in the file's `release` field.
- Line 635: the `rm` command is the one in the file's `release` field (`jq -r .release .dev/issues/<T1>/launch-result.json`).
- Line 769: the claim's `release` line becomes the file's `release` field; update the two script citations to the new line numbers of `rm -f -- "${p1:?}" "${p2:?}"` and `refusing an odd session id` in `session-gov.sh`.
- Line 767: update the two citations (`session-gov.sh:423` and `session-gov.sh:421` on master) to their new line numbers.
- Line 856 (section 6 table): update `session-gov.sh:82` only if Task 1 left lines 1 to 113 unchanged (expected: it stays 82). Add table rows in section 6 for the new printed literals `reason=claim-result-` (pending and fail forms) and `reason=terminal-handle-missing`, each citing its `session-gov.sh` line; each new row must keep the quoted literal on the cited line, because `runbook-selftest.sh` checks it, and rows may add lines (section 6 is after line 698).
- Appendix item 18 (line 893): say the result fields are read from `launch-result.json` (VERIFIED by reading the source; live behaviour UNVERIFIED). Add one UNVERIFIED entry to the not-verified list, worded: whether a live claim from the main checkout leaves `.dev/issues/<N>/launch-result.json` there and whether its `terminal`, `layers` and `release` equal what the session prints; how to confirm: the owner-approved live OB-H2 rerun. Update the counts in the appendix headings of that list to match.
- Run `grep -n 'terminal list\|printed text\|claim.s .release. line\|as printed' .dev/issues/442/observation-runbook.md` and justify every remaining hit: a hit may stay only when it describes the removed behaviour as history or an unrelated meaning.

Acceptance criteria:
- `wc -l < .dev/issues/442/observation-runbook.md` changes only by the number of rows added to section 6; `sed -n '536p;698p'` still print the `#### 2.2.1 Ses...` heading and the `## 3.` heading; `sed -n '228p;505p;520p'` still show the anchors `runbook-selftest.sh` checks.
- The runbook contains the string `launch-result.json` in lines 534, 546, 560, 566, 580, 635 and 769, and no instruction in the file tells a person to read terminal, layers or release from printed text or an Orca lookup.
- A new statement about live behaviour carries the word UNVERIFIED in the same sentence; no existing UNVERIFIED label is turned into VERIFIED.
- `git diff --stat` for the file shows only changed lines in the places listed above (no edit to the results sections or evidence quotes).

## Task 6: Add runbook-selftest checks and run the whole folder's self-tests

Depends on: Task 4, Task 5

Edit `.dev/issues/442/scripts/runbook-selftest.sh` (90 lines on master). Add, in a new block placed before the anchors block (the comment `# 5. the line anchors ...` at line 83 of master), checks that fail on the old text and pass on the new: `grep -c 'launch-result.json' "$RB"` is at least 7; `grep -c 'terminal list' "$here/session-gov.sh"` is 0; the string `orca terminal list` appears in the runbook only in sentences that say it is no longer used (a count of lines that contain it and do not contain `no longer` or `never` is 0); `grep -c 'CLAIM_LAST\|CLAIM_TXT' "$here/session-gov.sh"` is 0. Keep every existing check, including the five anchors.

Then run the full folder's checks from the repository root and fix any failure in the file that causes it (inside the Part B file list only):

- `bash .dev/issues/442/scripts/selftest.sh` must end with the single line `SELFTEST_OK` and exit 0. Baseline on master 1a6c8723f (2026-11-20, run by the planner): `SELFTEST_OK`, exit 0, zero `FAIL` lines. `selftest.sh` is the only script that prints `SELFTEST_OK`; it runs `lib-selftest.sh`, `setup-selftest.sh`, `driver-selftest.sh`, `session-a-selftest.sh`, `setup-github-selftest.sh`, `session-gov-selftest.sh`, `evidence-selftest.sh`, `cleanup-selftest.sh` and `runbook-selftest.sh`, each of which exits with its failure count. `lib-selftest.sh` and `driver-selftest.sh` are unchanged and must stay green.
- `bash -n` on `session-gov.sh`, `session-gov-selftest.sh` and `runbook-selftest.sh`; `shellcheck --severity=warning` on the same three only if a `shellcheck` binary already exists (UNVERIFIED locally; do not install one).
- `make sync-dev` then `make verify-sync` (exit 0; this change adds nothing under `src/superclaude/`, so both must be a no-op), and `make lint` (exit 0).
- `git status --short` and `git diff --name-only master...HEAD` list only the four Part B files plus `.dev/tasks/...` for this package; nothing under `.claude/` is staged (`git diff --cached --name-only | grep '^\.claude/'` prints nothing); stage the package with `git add .dev/tasks`.

Acceptance criteria:
- `bash .dev/issues/442/scripts/runbook-selftest.sh` prints no `FAIL` and exits 0, and its new checks fail when run against the master copies of the runbook and `session-gov.sh` (shown in `./artifacts/t6-negative-check.txt`).
- The last line of `bash .dev/issues/442/scripts/selftest.sh` is `SELFTEST_OK` and its exit status is 0; the tail is saved to `./artifacts/t6-selftest.txt`.
- `make lint` and `make verify-sync` exit 0, with the exit codes saved in `./artifacts/t6-make.txt`.
- The diff touches only the four Part B files and this package, and the self-tests created no file under `.dev/issues/442/` (`git status --short .dev/issues/442` lists only the four files).

## Phase 4: hand-off to the owner-gated steps

## Task 7: Write the hand-off note for the pull request and the owner-gated steps

Depends on: Task 6

Create `./artifacts/part-b-handoff.md` in this package. It is the text the coordinator pastes into the pull request body and uses to ask the owner. It contains: the list of the four changed files with a one-line reason each; the decisions in Constraints (file location, claim start rule, outcomes and exit codes, screen kept only for liveness and dialogs); the commands and results of Task 6 (self-test tail, `make` exit codes); and a section `Owner-gated, not run` with two entries, each with the owner's yes/no consequence. Entry one: `superclaude install` (yes: the installed skill gains the file writer so a live claim writes the file; no: the live rerun cannot happen). Entry two: the live OB-H2 rerun on T1 to T4 (yes: a real claim is made, the file's presence, mtime and fields are recorded in a new results entry and the runbook's UNVERIFIED sentence can then be revised in a follow-up change; no: Part B stays open). It also lists the remaining UNVERIFIED items: the `--source` the live claim passes, whether the live claim leaves the file in the main checkout, `shellcheck` not run locally, and the same-second edge of the staleness rule.

Acceptance criteria:
- `./artifacts/part-b-handoff.md` exists, names every changed file by repo-relative path, and states that `superclaude install` and the live OB-H2 rerun were not run.
- The file contains no credential, no absolute path outside the repository and no instruction for the implementer to run either owner-gated step.
- Part B's Done-when is quoted with its two halves: "the observation scripts read the file only" is shown met by the grep and self-test results, and "a live claim leaves it in place" is marked open and owner-gated.
