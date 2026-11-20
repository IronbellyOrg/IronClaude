3c9f44f2999f170591688e616b51374100112ff8
Review one task for spec compliance.

Task brief: ## Task 5: Point the runbook at launch-result.json

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

AC ids in source order of the Acceptance criteria bullets: T5.AC1 (line count changes only by rows added to section 6; lines 536 and 698 keep their headings; 228, 505, 520 keep the anchors), T5.AC2 (launch-result.json appears in lines 534, 546, 560, 566, 580, 635 and 769; no instruction tells a person to read terminal, layers or release from printed text or an Orca lookup), T5.AC3 (a new statement about live behaviour carries the word UNVERIFIED in the same sentence; no existing UNVERIFIED label is turned into VERIFIED), T5.AC4 (git diff --stat shows only changed lines in the places listed; no edit to results sections or evidence quotes).
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

Start sha: 3c9f44f2999f170591688e616b51374100112ff8
Diff against the start snapshot: 
```diff
diff --git a/.dev/issues/442/observation-runbook.md b/.dev/issues/442/observation-runbook.md
index 99394883c..ee0ee301f 100644
--- a/.dev/issues/442/observation-runbook.md
+++ b/.dev/issues/442/observation-runbook.md
@@ -533,3 +533,3 @@ GSID=$(jq -r 'select(.session_id) | .session_id' "$L.jsonl" | head -1); echo "$G
 
-All launches below are made from an ordinary Claude session in your main checkout started with `env -u CLICKUP_API_TOKEN claude` (section 1.4). The claim prints one result with `status`, `warning`, `detail`, `release` and two `layers` lines (VERIFIED: `refs/claim.md` lines 113-130 and `orca_worktree.py`). Copy all of them into the results file. Right after each launch, check that the probe loaded: `wc -l < "$L.jsonl"` is above 0.
+All launches below are made from an ordinary Claude session in your main checkout started with `env -u CLICKUP_API_TOKEN claude` (section 1.4). The claim saves its launch result as `.dev/issues/<N>/launch-result.json` in the main checkout, with `status`, `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook`, `release` and `layers` (VERIFIED by reading `write_launch_result` in `orca_worktree.py` and `refs/claim.md` line 125). Read terminal, layers and release from that file with `jq`, never from the agent's printed text and never from `orca terminal list`; a `launch-result.json` whose mtime is older than the moment the claim was sent counts as missing. That a live claim leaves the file in the main checkout is UNVERIFIED until the owner-approved live OB-H2 rerun. Copy the file's contents into the results file. Right after each launch, check that the probe loaded: `wc -l < "$L.jsonl"` is above 0.
 
@@ -545,3 +545,3 @@ printf '{' > "$WT_T1/.claude/settings.local.json"
 
-In the claim session: `/sc:issue --claim <T1> --pipeline worktree`. Expect `status` `failed`, `warning` `W-ENFORCEMENT-ABSENT`, a `detail` containing `settings.local.json cannot be read as JSON`, and no agent tab. VERIFIED in `orca_worktree.py` lines 1212-1237: the preflight runs before the pending record is published, so a refusal leaves no launch record. Confirm:
+In the claim session: `/sc:issue --claim <T1> --pipeline worktree`. Read `status`, `warning` and `detail` from the file (`jq '{status,warning,detail}' .dev/issues/<T1>/launch-result.json` in the main checkout). Expect `status` `failed`, `warning` `W-ENFORCEMENT-ABSENT`, a `detail` containing `settings.local.json cannot be read as JSON`, and no agent tab. VERIFIED in `orca_worktree.py` lines 1212-1237: the preflight runs before the pending record is published, so a refusal leaves no launch record. Confirm:
 
@@ -559,3 +559,3 @@ printf '{"disableAllHooks": true}' > "$WT_T1/.claude/settings.local.json"
 
-Claim again. Expect `failed`, `W-ENFORCEMENT-ABSENT`, and a `detail` containing `sets disableAllHooks to true, so no hook runs` (VERIFIED, `orca_worktree.py` line 907). Run the same three checks. Then restore the probe and claim for real:
+Claim again. Read `status`, `warning` and `detail` from the file (`jq '{status,warning,detail}' .dev/issues/<T1>/launch-result.json` in the main checkout). Expect `failed`, `W-ENFORCEMENT-ABSENT`, and a `detail` containing `sets disableAllHooks to true, so no hook runs` (VERIFIED, `orca_worktree.py` line 907). Run the same three checks. Then restore the probe and claim for real:
 
@@ -565,3 +565,3 @@ cp /tmp/ob/t1-local.json "$WT_T1/.claude/settings.local.json"
 
-`/sc:issue --claim <T1> --pipeline worktree`. Expect `status` `launched`, `layers` with `L1 guard: effective`, and an agent tab that says it was launched in `$WT_T1` at level worktree. The claim installs the L2 pre-push hook into the shared hooks folder of the main repository, so `W-L2-ABSENT` may or may not appear (UNVERIFIED until observed); record the `layers` lines and the `warning` as printed (`refs/claim.md` lines 127-129 name `W-L2-ABSENT` as the case where L2 is not in effect).
+`/sc:issue --claim <T1> --pipeline worktree`. Expect `status` `launched`, `layers` with `L1 guard: effective`, and an agent tab that says it was launched in `$WT_T1` at level worktree. The claim installs the L2 pre-push hook into the shared hooks folder of the main repository, so `W-L2-ABSENT` may or may not appear (UNVERIFIED until observed); record the `layers` lines and the `warning` from the file (`jq -r '.layers[], .warning' .dev/issues/<T1>/launch-result.json`) (`refs/claim.md` lines 127-129 name `W-L2-ABSENT` as the case where L2 is not in effect).
 
@@ -579,3 +579,3 @@ stat -c '%i %h %n' ~/.claude/state/launch-level/sessions/"$GSID"
 
-PASS when a file named `$GSID` exists, holds `worktree`, and its inode matches the number in the claim's `release` text. Record the link count (`%h`); the claim says the guard keeps the session file as a hard link of the record (VERIFIED in `refs/claim.md` line 119), but the count once the pending entry is gone is not stated anywhere this worker found.
+PASS when a file named `$GSID` exists, holds `worktree`, and its inode matches the number in the `release` field of `.dev/issues/<T1>/launch-result.json`. Record the link count (`%h`); the claim says the guard keeps the session file as a hard link of the record (VERIFIED in `refs/claim.md` line 119), but the count once the pending entry is gone is not stated anywhere this worker found.
 
@@ -634,3 +634,3 @@ jq -r 'select(.session_id) | .session_id' "$L.jsonl" | uniq      # a second id a
 
-Record F4 for the new id. The distinction case of §19.1: `sleep 241` (the old governed child) and `sleep 242` (after `/clear` in the same Claude process) are alive at the same time; compare their `identify` output and the ancestors in `tree-gov-bg.txt` and `tree-gov-clear.txt`. Finally release: run, in your own terminal, the `rm` command from the claim's `release` line, then:
+Record F4 for the new id. The distinction case of §19.1: `sleep 241` (the old governed child) and `sleep 242` (after `/clear` in the same Claude process) are alive at the same time; compare their `identify` output and the ancestors in `tree-gov-bg.txt` and `tree-gov-clear.txt`. Finally release: run, in your own terminal, the `rm` command in the `release` field of the result file (`jq -r .release .dev/issues/<T1>/launch-result.json`), then:
 
@@ -650,3 +650,3 @@ OB-CTX is PASS only when every case of part 1 and part 2 is recorded and `sleep
 
-Expect `ls ~/.claude/state/launch-level/sessions/"$GSID".ok` to list the file and the implement step to run (VERIFIED on the guard: a prompt starting with `/sc:implement` unlocks, while `please run /sc:implement now` does not). Then the commit prompt of session B: expect the LL-COMMIT text. Release with the claim's `rm` line.
+Expect `ls ~/.claude/state/launch-level/sessions/"$GSID".ok` to list the file and the implement step to run (VERIFIED on the guard: a prompt starting with `/sc:implement` unlocks, while `please run /sc:implement now` does not). Then the commit prompt of session B: expect the LL-COMMIT text. Release with the `rm` command in the `release` field of the claim's `launch-result.json`.
 
@@ -654,3 +654,3 @@ Expect `ls ~/.claude/state/launch-level/sessions/"$GSID".ok` to list the file an
 
-`L=/tmp/ob/logs/h2-T3`. Claim with `--pipeline full`. The agent runs every step, stages nothing, and ends with `git status --short` (VERIFIED in the launch prompt template). Then the commit prompt of session B: expect the LL-COMMIT text. Evidence: F5 (the git commands `/sc:implement` uses, U10), F6, F7, F8. Release with the claim's `rm` line.
+`L=/tmp/ob/logs/h2-T3`. Claim with `--pipeline full`. The agent runs every step, stages nothing, and ends with `git status --short` (VERIFIED in the launch prompt template). Then the commit prompt of session B: expect the LL-COMMIT text. Evidence: F5 (the git commands `/sc:implement` uses, U10), F6, F7, F8. Release with the `rm` command in the `release` field of the claim's `launch-result.json`.
 
@@ -693,3 +693,3 @@ git -C "$WT_T4" config --unset extensions.worktreeConfig      # only if you set
 
-Also record: one block message as you saw it in the tab (AC-7); the time from launch to the first block; the outputs of `claude --version`, `orca --version` and `sha256sum ~/.claude/settings.json ~/.claude/hooks/launch-level-guard.sh`. L2 (the pre-push hook) stays pending here: §19.5 needs a disposable bare destination, and this run does not push to one. Release with the claim's `rm` line.
+Also record: one block message as you saw it in the tab (AC-7); the time from launch to the first block; the outputs of `claude --version`, `orca --version` and `sha256sum ~/.claude/settings.json ~/.claude/hooks/launch-level-guard.sh`. L2 (the pre-push hook) stays pending here: §19.5 needs a disposable bare destination, and this run does not push to one. Release with the `rm` command in the `release` field of the claim's `launch-result.json`.
 
@@ -766,5 +766,5 @@ Copy the evidence lines into the results file before cleanup. Cleanup deletes `/
 - **Seeing the block message.** Whether a blocked prompt's message is visible in the tab (U20) and how one live block message reads (AC-7) can only be judged on screen.
-- **The O-10 conflict edit** during the `/sc:pr-submit` monitoring window is made through `gh_fork api repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt` (session-gov.sh:423) with `-X PUT` (session-gov.sh:421), not in the GitHub web UI. Whether `/sc:pr-submit` reacts to it the same way as to a web edit is UNVERIFIED.
+- **The O-10 conflict edit** during the `/sc:pr-submit` monitoring window is made through `gh_fork api repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt` (session-gov.sh:455) with `-X PUT` (session-gov.sh:453), not in the GitHub web UI. Whether `/sc:pr-submit` reacts to it the same way as to a web edit is UNVERIFIED.
 - **Judging retries** in F7 and F8: whether the next command is a reworded retry of a blocked one is a reading, not a filter. Record readings with `usage: evidence.sh --reading <u20|retry-f7-f8|ac7>` (evidence.sh:42).
-- **The release.** The LL-TAMPER block applies only to a governed session, so the claim's `release` line, an `rm`, is run from the driving agent's own shell (`refs/claim.md` line 119): `rm -f -- "${p1:?}" "${p2:?}"` (session-gov.sh:209) after `refusing an odd session id` (session-gov.sh:195). The guard still blocks a governed agent that touches the launch-level state (LL-TAMPER).
+- **The release.** The LL-TAMPER block applies only to a governed session, so the `release` field of `launch-result.json` (an `rm`) is run from the driving agent's own shell (`refs/claim.md` line 119): `rm -f -- "${p1:?}" "${p2:?}"` (session-gov.sh:241) after `refusing an odd session id` (session-gov.sh:228). The guard still blocks a governed agent that touches the launch-level state (LL-TAMPER).
 
@@ -795,3 +795,3 @@ for n in 241 242 243; do for p in $(pgrep -xf "sleep $n"); do [ "$(ps -o etimes=
 
-2. Release every governed session that is still bound. Use the `rm` line each claim printed. Then compare the store with the baseline:
+2. Release every governed session that is still bound. Use the `rm` command in the `release` field of each claim's `launch-result.json`. Then compare the store with the baseline:
 
@@ -856,2 +856,5 @@ Cleanup `--apply` rule: `Default: print the plan and delete nothing.` (cleanup.s
 | `reason=needs-input` (session-gov.sh:82) | Same as `NEEDS_INPUT`: read the screen file, answer only a disposable target, and check whether the step's prompt is shown before you send it again. |
+| `reason=claim-result-` (session-gov.sh:177, session-gov.sh:178) | `PENDING`: the claim left no fresh `launch-result.json` in the main checkout (`missing`), or only one older than the claim's start (`stale`, which is also what an `already_launched` claim leaves, because it writes no file). Look at the claim session and at `.dev/issues/<N>/launch-result.json`; never run the claim again before you know it did not launch. |
+| `claim-result` (session-gov.sh:179) | `FAIL claim-result <why>`: the result file is a symlink, is not a JSON object, or has no string `status`. Repair the cause; do not delete the file. |
+| `reason=terminal-handle-missing` (session-gov.sh:215) | `PENDING`: the file's `terminal` is empty or not a plain handle. The full record is in the run log named on the line; take the handle by hand and run `driver.sh adopt`. |
 | `NEEDS_INPUT claim` (setup-github.sh:100) | Same as `NEEDS_INPUT`. |
@@ -892,3 +895,3 @@ Checked by reading the source (8):
 
-18. The claim's result fields, including `release` and the two `layers` lines (`refs/claim.md` lines 113-130).
+18. The claim's result fields, including `release` and the two `layers` lines, are saved to `launch-result.json` and read from it by the scripts (`refs/claim.md` lines 113-130 and 125, `write_launch_result` in `orca_worktree.py`; live behaviour is UNVERIFIED, see item 15 of the not-verified list).
 19. The preflight runs before the pending record is published, so a refusal leaves no launch record (`orca_worktree.py` lines 1212-1237).
@@ -901,3 +904,3 @@ Checked by reading the source (8):
 
-### Not verified (14)
+### Not verified (15)
 
@@ -919,2 +922,3 @@ Each is marked UNVERIFIED where it is used, with the way to confirm it:
 14. Whether entries left in `jobs/` or `requests/` can safely be removed by hand (section 5.2).
+15. Whether a live claim from the main checkout leaves `.dev/issues/<N>/launch-result.json` there, and whether its `terminal`, `layers` and `release` equal what the session prints (sections 2.2.1 and 4.2). To confirm: the owner-approved live OB-H2 rerun on T1 to T4.
 
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (markdown is not indexed by codegraph, so this ran on the Grep floor): the readers of the runbook are session-gov-selftest.sh (lines 536 to 697, section 10) and runbook-selftest.sh (quotes, section 6, anchors 228, 505, 520, 536, 698).
Run evidence taken by the orchestrator: bash runbook-selftest.sh printed no FAIL and exited 0 against the edited runbook; wc -l before 921, after 925 (3 section 6 rows and 1 appendix list item added); the 534 to 698 span has the same line count.
Note on lines 651, 655, 694 and 796: the orchestrator also pointed these four "release with the claims rm line" sentences at the release field of launch-result.json, so that no instruction in the file tells a person to take the release text from printed text (T5.AC2). They are outside the list of lines the brief names.
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
