---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-scIssueClaimPipe-20261107-063237
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Add the --pipeline and --submit flags to /sc:issue --claim

Source: ./source.md
Goal: `/sc:issue --claim <N> [--pipeline worktree|full|none] [--submit]` creates or reuses an Orca worktree `issue-<N>`, launches a Claude Code agent behind the ccsession shim at the chosen level, and records the level in the hook's launch store, with all behaviour covered by unit tests that use a fake `orca`.

## Constraints

- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.

## Phase 1: The worktree step

## Task 1: Create scripts/orca_worktree.py with its shared helpers and the preflight subcommand

Create `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (Python standard library only, executable-style header like `clickup_claim.py` in the same folder) and `tests/skills/test_issue_orca_worktree.py`. Source: design sections 8 (intro) and 8.1.

The script uses `argparse` subparsers `preflight`, `worktree`, `prompt`, `launch` (the last three are added by later tasks; register only `preflight` now). It prints exactly one JSON object on stdout, exits 0 for every runtime outcome and 2 only for bad arguments (argparse default). A shared `run(argv, timeout)` helper runs a command without a shell, captures output, and returns a failed result (never raises) on timeout, nonzero exit or missing binary. Timeouts: 120 s default, 30 s for `preflight`, 15 s for each `orca terminal read`.

`preflight` runs `orca status --json` and prints `{"ok": true}` only when the command exits 0 and the JSON has `ok: true` and `result.runtime.reachable: true`; otherwise `{"ok": false, "detail": "<first stderr line or why the JSON failed>"}`. A missing `orca` binary gives the same shape.

The test file builds the reusable fixtures for the whole feature: a fake `orca` script written to a temporary directory that logs every argv to a file and answers from per-test JSON, a temporary git repository with an `origin` remote, and a temporary `HOME`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k preflight` passes with cases PF-1 (ok: true) and PF-2 (not reachable, nonzero exit, invalid JSON, and no `orca` on `PATH` each give `ok: false` with a non-empty detail).
- A call with a bad subcommand or missing required argument exits 2.
- A hanging fake `orca` is cut by the timeout and reported as `ok: false`, not as a crash (the timeout is overridable in the test through an environment variable or function argument so the test runs in under 5 seconds).

## Task 2: Add the worktree subcommand to orca_worktree.py

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

## Task 3: Add the --pipeline and --submit flags to the /sc:issue command file

Edit `src/superclaude/commands/issue.md` and `tests/commands/test_issue_command.py`. Source: design section 4 and section 11 (new STOPs).

In `src/superclaude/commands/issue.md`: add `version: "1.1.0"` to the frontmatter; extend `argument-hint`, the Usage block, the Options table (rows `--pipeline`: mode claim, default `worktree`, values `worktree`, `full`, `none`; `--submit`: mode claim, default off, no value), Examples (`--claim 302`, `--claim 302 --pipeline none`, `--claim 302 --pipeline full`, `--claim 302 --pipeline full --submit`) and the Outputs table (claim also produces `launch-prompt.md` and `worktree.json`). Rewrite the claim bullet and the Will list so a claim now also creates or reuses the worktree and launches one agent at the chosen level and never merges. In Will Not replace "Run any next-step command (brainstorm, design, workflow, implement, troubleshoot)" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose)" and add "Pass an Orca link flag" and "Merge anything".

Add three STOP rules after the existing ones and before Activation, in this order: `--pipeline` or `--submit` with `--create` is STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only"); a `--pipeline` value that is not `worktree`, `full` or `none` (or `--pipeline` with no value) is STOP listing the three values; `--submit` with a value, or without `--pipeline full`, is STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full"). `E-CREATE-ONLY-FLAG` for `--depth`, `--mode`, `--type` with `--claim` stays the first rule. Update `tests/commands/test_issue_command.py`: the Options-table test lists exactly seven flags with the new values and defaults; the STOP-rule test requires the new codes before `## Activation`; add a check that Will Not names `/sc:implement`, `/task`, a commit, a push and `/sc:pr-submit` and no longer contains "Run any next-step command"; check `version: "1.1.0"`.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py` passes, covering pins ST-1, ST-2 and ST-3 of design section 13.
- `grep -n "src/superclaude" src/superclaude/commands/issue.md` finds nothing.

## Task 4: Add the Orca check and Wave 7 to the issue skill and claim ref

Depends on: Task 2

Edit `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `tests/skills/test_issue_protocol.py`. Source: design sections 7 (Wave 0, Wave 6, Wave 7), 10 and 11.

In `refs/claim.md` Wave 0 add a new step 3 after `gh auth status` and before the default-branch lookup: run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight`; `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`, before any GitHub or ClickUp write. Replace Wave 6 step 4 ("Print the `next-steps.md` path and STOP") with a hand-off: after both comments are posted, run Wave 7 (and Wave 8, added by a later task); any STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. Add Wave 7: run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>`, read its JSON, every failure is a warning and the claim `status` stays `success`; print the worktree path, status, match key, the "reused a worktree not created by /sc:issue" line for keys `basename` and `branch`, the "untracked, do not stage" line when no file under the worktree's `.dev/issues/<N>/` is tracked, "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive, and each warning with its remedy line from design section 11 (worktree codes).

In `SKILL.md`: add the `scripts/orca_worktree.py` row to the files table; update the claim-mode paragraph and claim step 1 (Wave 0 check) and step 7 (Wave 6 now continues to the worktree step); add `E-ORCA-REQUIRED` and the worktree warning codes to the error table; keep the file under 500 lines. Update `tests/skills/test_issue_protocol.py`: the files-table test accepts the new script, ST-5 (still five refs, script named and present), ST-6 (preflight in Wave 0 before Wave 1, Wave 7 after the Wave 6 posts).

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py` passes.
- `grep -n "src/superclaude" src/superclaude/skills/sc-issue-protocol/SKILL.md src/superclaude/skills/sc-issue-protocol/refs/claim.md` finds nothing.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` reports fewer than 500 lines.

## Phase 2: The launch

## Task 5: Add the launch prompt template and the prompt subcommand

Depends on: Task 1

Create `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` and add the `prompt` subcommand to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; extend `tests/skills/test_issue_orca_worktree.py` and `tests/skills/test_issue_protocol.py`. Source: design sections 8.2 and 9.

The template has exactly four blocks, each opened by an HTML-comment marker line of the form `block:<name>` wrapped as shown in design section 9 (names `common`, `worktree`, `full`, `submit`), with the required statements of the design section 9 table: common (read `issue-summary.md` and `next-steps.md`; run each step by invoking its command through the Skill tool in this session, never by reading a command file and never inside a subagent; report a model-tier mismatch with the tier named in `next-steps.md`; never merge, never push to `master` or `main`); worktree (follow the steps up to the `Plan boundary` line; do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`; print the plan path and `Waiting for approval`, then wait; after a human replies `approved` or runs the printed implement command, run the remaining steps, still without commit, push or `/sc:pr-submit`); full (run every step through the last, leave changes in the working tree, stage nothing, finish by printing `git status --short`); submit (the owner asked for the commit and push by passing `--submit`; check that no PR is already open or merged for the branch; commit with a conventional-commit message staging `.dev/tasks` and the changed files, never `.claude/` and never `.dev/issues/`; push the current feature branch to `origin`, never `master`; run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`; never merge).

`prompt --template <path> --level worktree|full [--submit] --number <N> --out <file>` keeps `common` plus the level block (plus `submit` with `--submit`), drops every other block and all marker lines, replaces `<N>`, writes `--out` and prints `{"status": "written", "path": "<out>"}`. `--submit` with `--level worktree` exits 2.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k prompt` passes with PR-1 to PR-4 (levels keep only their own block, `--submit` adds the submit block, `--submit` with `worktree` exits 2, the rendered `full` output and the `common` block hold none of `/sc:pr-submit`, `git push`, `git commit`, `--monitor`).
- `tests/skills/test_issue_protocol.py` has ST-8: the template has exactly the four blocks, only the `submit` block contains `/sc:pr-submit --monitor 3`, `git push` and the commit instruction, and only the `worktree` block also contains those tokens (as a prohibition).
- The rendered `worktree` output contains the line telling the agent not to run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

## Task 6: Add the launch subcommand, the launch record and the shim check

Depends on: Task 2, Task 5

Add `launch --number <N> --source <D> --level worktree|full [--submit]` to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` and extend `tests/skills/test_issue_orca_worktree.py`. Source: design sections 6 and 8.4, and hook design `docs/designs/sc-issue-launch-level-hook.md` IR-1, IR-2, IR-5. Output: `{status, warning, detail, terminal, launched_at, enforcement_hook, hand_command}` with `status` one of `launched`, `failed`, `already_launched`.

Behaviour: read `worktree.json` in the source directory through the record guard (path exists, git-common-dir equals the main checkout's by realpath); a missing or failing record is `failed` with `W-LAUNCH-FAILED`. A record with a `launch` entry returns `already_launched` with its `at` time and calls neither `orca` nor writes a launch record. `enforcement_status()` returns `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`; `missing` sets `W-ENFORCEMENT-ABSENT` but does not stop the launch. Publish the launch record at `$HOME/.claude/state/launch-level/pending/<nonce>` (nonce `secrets.token_hex(16)`, directories mode 0700, file mode 0600, content exactly one word `worktree`, `full` or `full-submit`, written to a temporary name and renamed to the nonce); a write error is `failed` with `W-LAUNCH-FAILED` and no launch. Then run `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` with no `--model` and no `--effort`; a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command` (the same call without the marker). Then the ccsession shim check: take the first string value under any key named `handle` in the launch JSON by a recursive walk, call `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart (the sleep is injectable so tests run fast), and pass when `result.terminal.tail` text contains `[ccsession]` or `Session name (Enter or Ctrl+C`; no handle, an unreadable terminal or no match sets `W-LAUNCH-NOT-CCSESSION` and keeps the launch. Finally write `launch: {level, submit, at}` (UTC ISO time) into `worktree.json` whatever the shim result, and return `launched`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k launch` passes with LA-1 (exact launch argument list, prompt starts with `[sc-launch:v1:` plus 32 hex characters and `] `, no leading `/`, no `--model`, no `--effort`, no link flag), LA-2 (record is a regular file of mode 0600 in a 0700 directory holding the exact word for the level, published before the launch call, same nonce in the prompt), LA-3 (failed launch removes the record; read-only store makes no launch call), LA-4 (`launch` entry gives `already_launched` with no `orca` call; the entry is written even when the shim check fails), LA-5 (shim pass on `[ccsession]` and on the question text; fail on neither, unreadable terminal, no handle), LA-6 (`installed` and `missing` hook script, launch happens in both).
- No file is created inside the worktree or the source directory by `launch` other than the `launch` entry in `worktree.json`.

## Task 7: Add Wave 5 additions, Wave 8, the Plan boundary line and the claim return contract

Depends on: Task 4, Task 5, Task 6

Edit `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `tests/skills/test_issue_protocol.py`. Source: design sections 7 (Wave 5 additions, Wave 8, final output), 10 and 11.

In `templates/next-steps.md` add the line `Plan boundary: after step <K>` under the title. In `refs/claim.md` Wave 5 add: the skill sets `<K>` to the number of the last step before the first step whose command is `/sc:implement` or `/task` (the line reads `Plan boundary: before step 1` when the first step is the implementation step; `--pipeline full` ignores it); for any `--pipeline` value other than `none`, run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --out "<D>/launch-prompt.md"` before Wave 7 so the copy carries it. Add Wave 8: runs only when `--pipeline` is not `none` and Wave 7 status is `created` or `reused`; run `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`; never attempted for a `failed` worktree; failures are warnings and the claim stays `success`. Replace the Wave 6 hand-off with the final output of design section 7 (next-steps path, worktree line, launch result lines for launched, already_launched and none, every warning with its remedy line from design section 11 including the three launch codes, then the return contract).

In `SKILL.md`: add the `templates/launch-prompt.md` row to the files table; replace the claim-mode return contract with the ten fields of design section 10 (`pipeline_level`, `submit`, `worktree_status`, `worktree_path`, `worktree_branch`, `worktree_match_key`, `worktree_warning`, `launch_status`, `launch_warning`, `enforcement_hook`), create mode unchanged; add `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `E-CLAIM-ONLY-FLAG` and `E-SUBMIT-NEEDS-FULL` to the error table; update the Will and Will Not lists to match the command file (the skill itself still runs no next-step command; the launched agent does; nothing merges). Add tests ST-4 (no forbidden Orca flag in skill, refs, command or script outside the launch call), ST-7 (`Plan boundary` in the template and the `<K>` rule in the ref), ST-9 (Wave 8 skipped for `none`, prompt file written before Wave 7), ST-10 (the ten contract fields), ST-11 part one (no `src/superclaude/` path in any file of the skill).

Acceptance criteria:
- `uv run pytest tests/skills tests/commands` passes.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` reports fewer than 500 lines.
- `grep -rn "src/superclaude" src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol` finds nothing.

## Phase 3: Documentation and sync

## Task 8: Amend the original design document

Depends on: Task 7

Edit `docs/designs/sc-issue-command.md`. Source: design section 2 (B2 rewritten text, P6), section 12 (change table row for this file) and `docs/designs/sc-issue-claim-pipeline-flag.md`.

Rewrite the B2 row of the section 2 table to the new text (the claim writes the summary and `next-steps.md`, creates a worktree and launches one agent; neither the skill nor the default agent runs `/sc:implement` or `/task`; `--pipeline full` lets the agent run them; `--submit` additionally lets it commit, push and run `/sc:pr-submit`; merging never happens). Add rows B16 (a worktree is created after `next-steps.md`), B17 (launch levels worktree, full, none; launch behind the ccsession shim through `orca agent launch --surface terminal`) and B18 (`--submit` turns on commit, push and `/sc:pr-submit --monitor 3`, never merges). Add a short "Amended 2026-11-07" note pointing to `docs/designs/sc-issue-claim-pipeline-flag.md` in sections 1, 4, 7, 14, 16 and 20, and add the new script, template and test file to the section 15 file list.

Acceptance criteria:
- `grep -n "B16\|B17\|B18" docs/designs/sc-issue-command.md` shows the three new rows, and the B2 row no longer says the claim "stops after writing the next-step prompt".
- The folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` exists with `merged-requirements.md`, `launch-levels-addendum.md`, `seed-brief.md`, `adversarial/` and `enrichment/`, ready to be staged with the change.

## Task 9: Update the user guide and routing guide, then sync

Depends on: Task 7

Edit `docs/user-guide/commands.md` (the `/sc:issue` section starting at its `### /sc:issue` heading and its table row), `src/superclaude/core/HOW-WE-WORK.md` (the `/sc:issue` row of the "Other commands" table) and copy that file byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Source: design sections 1, 4 and 12.

In the user guide: update the usage lines, add the two flags with the four levels (`worktree` default stops at an approved plan, `full` implements without commit or push, `full` with `--submit` commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, `none` creates the worktree and launches no agent), state that no level merges and that Orca is required (`E-ORCA-REQUIRED`), and add examples. In the routing row replace "then stops without running them" with a statement that a claim also creates a worktree and launches an agent at the chosen level and never merges. Then run `make sync-dev`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference, and `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/cli/test_issue_body_templates.py -q` passes.
- `make sync-dev` completes and `make verify-sync` passes; `git status --short` shows no path under `.claude/` staged.
- `make lint` passes and `uv run ruff format --check src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_orca_worktree.py` passes with the ruff version the repository pins.
- `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` shows no hit introduced by this change.
