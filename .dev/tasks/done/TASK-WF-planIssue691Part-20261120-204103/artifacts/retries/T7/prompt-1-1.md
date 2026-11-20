f3352f71ec875e4423522e59113b9d5ffd640bd9
Review one task for spec compliance.

Task brief: ## Task 7: Write the hand-off note for the pull request and the owner-gated steps

Depends on: Task 6

Create `./artifacts/part-b-handoff.md` in this package. It is the text the coordinator pastes into the pull request body and uses to ask the owner. It contains: the list of the four changed files with a one-line reason each; the decisions in Constraints (file location, claim start rule, outcomes and exit codes, screen kept only for liveness and dialogs); the commands and results of Task 6 (self-test tail, `make` exit codes); and a section `Owner-gated, not run` with two entries, each with the owner's yes/no consequence. Entry one: `superclaude install` (yes: the installed skill gains the file writer so a live claim writes the file; no: the live rerun cannot happen). Entry two: the live OB-H2 rerun on T1 to T4 (yes: a real claim is made, the file's presence, mtime and fields are recorded in a new results entry and the runbook's UNVERIFIED sentence can then be revised in a follow-up change; no: Part B stays open). It also lists the remaining UNVERIFIED items: the `--source` the live claim passes, whether the live claim leaves the file in the main checkout, `shellcheck` not run locally, and the same-second edge of the staleness rule.

Acceptance criteria:
- `./artifacts/part-b-handoff.md` exists, names every changed file by repo-relative path, and states that `superclaude install` and the live OB-H2 rerun were not run.
- The file contains no credential, no absolute path outside the repository and no instruction for the implementer to run either owner-gated step.
- Part B's Done-when is quoted with its two halves: "the observation scripts read the file only" is shown met by the grep and self-test results, and "a live claim leaves it in place" is marked open and owner-gated.

AC ids in source order of the Acceptance criteria bullets: T7.AC1 (the handoff file exists, names every changed file by repo-relative path, states that superclaude install and the live OB-H2 rerun were not run), T7.AC2 (no credential, no absolute path outside the repository, no instruction for the implementer to run either owner-gated step), T7.AC3 (Part B Done-when quoted with its two halves; first half shown met by the grep and self-test results, second half marked open and owner-gated).
The quoted Done-when is in the plan source file source.md line 15 of the package: "the observation scripts read the file only, and a live claim leaves it in place".
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

Start sha: f3352f71ec875e4423522e59113b9d5ffd640bd9
Diff against the start snapshot: 
New untracked file (full contents):
```diff
+++ b/.dev/tasks/to-do/TASK-WF-planIssue691Part-20261120-204103/artifacts/part-b-handoff.md
@@ -0,0 +1,52 @@
+# Issue 691 Part B: hand-off note
+
+Issue: https://github.com/IronbellyOrg/IronClaude/issues/691 (Part A is merged as PR 693; this is Part B). This note is the text for the pull request body and for the question to the owner. `superclaude install` and the live OB-H2 rerun were NOT run.
+
+## Done-when of Part B, both halves
+
+Quoted from the issue brief: "the observation scripts read the file only, and a live claim leaves it in place".
+
+- First half, "the observation scripts read the file only": MET, shown by `grep -n 'CLAIM_TXT\|CLAIM_LAST\|CLAIM_SCREEN\|claim_has\|terminal list\|claim-T[0-9]\.txt\|inodenumber' .dev/issues/442/scripts/session-gov.sh` printing nothing, by `bash .dev/issues/442/scripts/session-gov-selftest.sh` (135 OK lines, no FAIL, exit 0) and by `bash .dev/issues/442/scripts/selftest.sh` ending in `SELFTEST_OK` (exit 0).
+- Second half, "a live claim leaves it in place": OPEN and owner-gated. Only the live OB-H2 rerun after merge can show it.
+
+## The four changed files
+
+- `.dev/issues/442/scripts/session-gov.sh`: `claim_send`, `launch_real`, `release_session`, `inode_record` and `preflight_refusal` now take status, warning, detail, terminal, layers and release from `launch-result.json` with `jq`; the `orca terminal list` lookup and the screen parsing are gone.
+- `.dev/issues/442/scripts/session-gov-selftest.sh`: the stub claim now writes the result file and leaves a deliberately wrong claim screen; new cases cover fresh, screen ignored, missing, stale, unreadable (not JSON, array, no status, symlink), failed result, already_launched (earlier file untouched), terminal null or odd, missing layer, and a resume that only has saved text.
+- `.dev/issues/442/scripts/runbook-selftest.sh`: four new checks that fail on the old text (file cited at least 7 times, no `terminal list` in the script, `orca terminal list` named only as no longer used, no `CLAIM_LAST` or `CLAIM_TXT`).
+- `.dev/issues/442/observation-runbook.md`: the claim steps and the release steps point at `launch-result.json`; three section 6 table rows for the new printed literals; one new UNVERIFIED entry (item 15) in the not-verified list.
+
+## Decisions (from the plan Constraints)
+
+- File location: `$MAIN/.dev/issues/<N>/launch-result.json` in the main checkout (the worktree copy never receives it, `orca_worktree.py` skips it when copying).
+- Claim start: the script records `CLAIM_START=$(date +%s)` right before it types the claim (after the `/clear`). A result is fresh only when its integer mtime is at least `CLAIM_START` and, when `launched_at` is a string, its epoch is also at least `CLAIM_START`. No clock-skew allowance.
+- Outcomes: file absent after the poll loop is `PENDING reason=claim-result-missing` (exit 0); present but stale is `PENDING reason=claim-result-stale` (exit 0), which is also what an `already_launched` claim produces; a symlink, a non-object or a missing string `status` is `FAIL claim-result` (exit 1); a result whose status is not `launched` in `launch_real` is `FAIL <sub>-claim` (exit 1); a missing or invalid terminal handle is `PENDING reason=terminal-handle-missing` (exit 0).
+- The claim screen is still read for two non-result jobs only: the vanished-terminal check and the `Do you want|/login|Not logged in` dialog check.
+- JSON is read only through `jq` with `command timeout "$T"`; nothing from the file reaches `eval`, `source`, `bash -c` or an unquoted expansion; the terminal handle is checked against `^[0-9A-Za-z_-]+$` before `driver.sh adopt`.
+
+## Task 6 commands and results
+
+- `bash .dev/issues/442/scripts/selftest.sh`: exit 0, last line `SELFTEST_OK`, 0 FAIL lines (tail in `artifacts/t6-selftest.txt`).
+- `bash -n` on `session-gov.sh`, `session-gov-selftest.sh`, `runbook-selftest.sh`: exit 0. `shellcheck` was not run (no binary on the machine; UNVERIFIED locally).
+- `make sync-dev`: exit 0. `make verify-sync`: exit 0 (`All components in sync.`). `make lint`: exit 0 (`All checks passed!`) (`artifacts/t6-make.txt`).
+- Negative checks: the new session-gov self-test fails 78 cases against the old `session-gov.sh` (`artifacts/t4-negative-check.txt`); the new runbook checks `result-file-cited`, `gov-no-terminal-list` and `gov-no-screen-parse` fail on the old text (`artifacts/t6-negative-check.txt`).
+
+## Owner-gated, not run
+
+1. `superclaude install`. Yes: the installed skill gains the file writer, so a live claim writes the file. No: the live rerun cannot happen.
+2. The live OB-H2 rerun on the disposable issues T1 to T4. Yes: a real claim is made, the file's presence, mtime and fields are recorded in a new results entry, and the runbook's UNVERIFIED sentence can then be revised in a follow-up change. No: Part B stays open.
+
+## Still UNVERIFIED
+
+- Which `--source` folder the live claim passes (the plan assumes it resolves to the main checkout's `.dev/issues/<N>`).
+- Whether a live claim leaves the file in the main checkout, and whether its `terminal`, `layers` and `release` equal what the session prints.
+- `shellcheck --severity=warning` was not run locally (the repository's pre-commit config runs it in CI).
+- The same-second edge of the staleness rule: a result written by an earlier claim in the very same second as this claim's start would be accepted; the several-second claim run makes this negligible.
+
+## Differences from the plan
+
+- Four more runbook lines (651, 655, 694, 796) said "release with the claim's rm line"; they now point at the `release` field of `launch-result.json`, so no instruction tells a person to take the release text from printed text.
+- The appendix list gained one item, so the runbook grew by 4 lines (3 section 6 rows and 1 list item), all after line 698.
+- In this checkout the plan's "master 1a6c8723f" is `HEAD`; the negative checks use `git show HEAD:<path>`.
+- An unparseable `launched_at` string is ignored (the file mtime check already applies); the plan names only the below-`CLAIM_START` case.
+- `claim_result_state` also sets a `CLAIM_STATE` variable, because the globals it sets would be lost if callers read its printed word through `$(...)`.
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none (a new markdown file; nothing reads it).
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
