65d8bd254e86b9e9332250bd0fdeb62269ccdf8a
Review one task for spec compliance.

Task brief: ## Task 2: Add the worktree subcommand to orca_worktree.py

Depends on: Task 1

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` add `worktree --repo <R> --number <N> --base origin/<B> --source <D>`, printing `{status, path, branch, match_key, warning, detail}` with `status` one of `created`, `reused`, `failed`. Source: design section 8.3 (algorithm table steps 1 to 7, command list, record guard), merged-requirements.md sections 2.4, 2.5 and 5, and FR-15, FR-16, FR-17, FR-18, FR-20.

The commands the script runs are exactly: `git rev-parse --path-format=absolute --git-common-dir`; `git fetch origin`; `git rev-parse --verify origin/<B>`; `orca worktree list --repo path:<main> --limit 500 --json`; `orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json`; `git -C <wt> rev-parse --path-format=absolute --git-common-dir`; `git -C <wt> ls-files .dev/issues/<N>`. No other `orca` or `git worktree` call (no `git worktree add`, no `orca worktree rm`, no commit, push or stage).

Behaviour to implement and test in `tests/skills/test_issue_orca_worktree.py`, with list fixtures copied from the live `orca worktree list --json` shape (nested `result.worktrees` rows with `id`, `path`, `branch` as full refs, `comment`, `isMainWorktree`, `isArchived`; `result.truncated`; `result.hostScope.omittedHostIds`):
- List unusable (`ok` not true, `truncated` true, `omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true`), including the after-create list: a `worktree.json` record in the source directory whose path exists and shares the git-common-dir is reused with match key `record` and detail "unverified"; otherwise `failed` with `W-ORCA-LIST-FAILED` and no create call.
- Lookup over rows with `isArchived` false, key order marker (comment contains `sc:issue <R>#<N>` not followed by a digit), record, basename (`^issue-<N>(-|$)`), branch (same pattern on the last `/` segment). Hits deduplicated by row id, first key with a hit decides; one live hit is `reused`; stale hits only is `failed` with `W-WORKTREE-STALE`; two or more live hits is `failed` with `W-WORKTREE-AMBIGUOUS` listing all paths; none of these calls create.
- No hit: a missing `origin/<B>` is `failed` with `W-ORIGIN-BASE-MISSING` and no create call; a failed `git fetch origin` with the ref present continues with warning `W-ORIGIN-BASE-STALE`. After create (exit 0 or timeout) list once more and take the row-id set difference: exactly one new row whose basename matches the issue pattern is `created` and its `path` is the worktree path (never read from the create JSON); zero new rows is `failed` with `W-WORKTREE-CREATE-FAILED` ("created but not listed"); two or more is `failed` with `W-WORKTREE-AMBIGUOUS` and no copy or record; a nonzero create exit is `failed` with `W-WORKTREE-CREATE-FAILED` and the first stderr line, never retried.
- Copy the source directory into `<wt>/.dev/issues/<N>/` file by file including `analysis/`, never as one recursive directory copy: skip entirely when source and destination share a realpath; never copy `worktree.json`; skip and name a file that `git ls-files` shows as tracked; copy a missing file; skip an identical file; rename a differing untracked file to `<name>.prev` (replacing an older `.prev`), copy, and name it in `W-WORKTREE-COPY-FAILED`. A copy error or byte mismatch after copy is `failed` with `W-WORKTREE-COPY-FAILED`; a destination whose git-common-dir differs from the main checkout's is `failed` with `W-WORKTREE-STALE`.
- Only on `created` or `reused`, write `worktree.json` in the source directory as `{"path": "<absolute>", "status": "created|reused"}`, keeping any existing `launch` entry.
- The warning field holds the one code that set the status; any other problem goes in `detail`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k "FO or worktree"` passes with cases FO-1, FO-2, FO-3, FO-4, FO-6, FO-7, FO-8, FO-9, FO-10, FO-11, FO-12, FO-13, FO-14, FO-15, FO-16, FO-17 and FO-18 of design section 13 (each named in the test function name or id).
- FO-18 asserts the create argument list equals the command above exactly and that no forbidden flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`) appears in any recorded `orca` call.
- `grep -n "worktree add\|worktree rm\|git commit\|git push\|git add" src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` finds no executed command.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T2.AC1, T2.AC2, ... in the order of the 'Acceptance criteria:' bullets).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: 65d8bd254e86b9e9332250bd0fdeb62269ccdf8a
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T2-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
