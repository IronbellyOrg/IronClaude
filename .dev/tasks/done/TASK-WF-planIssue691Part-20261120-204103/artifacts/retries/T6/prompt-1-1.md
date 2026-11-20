aa43ccadbff95140727bf95d750f3d8c325c9ef3
Review one task for spec compliance.

Task brief: ## Task 6: Add runbook-selftest checks and run the whole folder's self-tests

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

AC ids in source order of the Acceptance criteria bullets: T6.AC1 (runbook-selftest prints no FAIL, exits 0, and its new checks fail on the master copies; shown in ./artifacts/t6-negative-check.txt), T6.AC2 (the last line of selftest.sh is SELFTEST_OK, exit 0; tail in ./artifacts/t6-selftest.txt), T6.AC3 (make lint and make verify-sync exit 0; exit codes in ./artifacts/t6-make.txt), T6.AC4 (the diff touches only the four Part B files and this package; the self-tests created no file under .dev/issues/442/).
Artifacts live in .dev/tasks/to-do/TASK-WF-planIssue691Part-20261120-204103/artifacts/. In this checkout the plan's "master 1a6c8723f" is HEAD (1a6c8723f); the local branch named master is an older commit, so the negative checks use git show HEAD:<path>.
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

Start sha: aa43ccadbff95140727bf95d750f3d8c325c9ef3
Diff against the start snapshot: 
```diff
diff --git a/.dev/issues/442/scripts/runbook-selftest.sh b/.dev/issues/442/scripts/runbook-selftest.sh
index 971ff121d..d9b3e2c63 100644
--- a/.dev/issues/442/scripts/runbook-selftest.sh
+++ b/.dev/issues/442/scripts/runbook-selftest.sh
@@ -80,6 +80,12 @@ uncited=$(printf '%s\n' "$sec" | awk '
   !/[a-z0-9-]+\.sh:[0-9]+/ { print NR ": " $0 }')
 ck sec6-every-line-cited "${uncited:-none}" none
 
+# 4b. the claim's terminal, layers and release come from launch-result.json, not from screen text or an Orca lookup (issue 691, Part B)
+ck result-file-cited "$([ "$(grep -c 'launch-result.json' "$RB")" -ge 7 ] && echo yes)" yes
+ck gov-no-terminal-list "$(grep -c 'terminal list' "$here/session-gov.sh" || true)" 0
+ck rb-terminal-list-only-as-removed "$(grep 'orca terminal list' "$RB" | grep -vc 'no longer\|never' || true)" 0
+ck gov-no-screen-parse "$(grep -c 'CLAIM_LAST\|CLAIM_TXT' "$here/session-gov.sh" || true)" 0
+
 # 5. the line anchors other self-tests read (session A 228-472, filters 505-520, sessions B to E 536-697)
 ck anchor-session-a "$(sed -n '228p' "$RB" | cut -c1-16)" '### 2.1 Session '
 ck anchor-filters "$(sed -n '505p' "$RB" | cut -c1-5)" '# F1:'
```

Codegraph context
index_state: fresh; checked_at: 2026-11-20T20:49:34Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff (shell files are not indexed by codegraph, so this ran on the Grep floor): runbook-selftest.sh is run only by selftest.sh.
Diff scope evidence: git diff --name-only HEAD lists the four Part B files and the package files; git status --short .dev/issues/442 lists only those four files.
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
