ed51a97d3a9328a8f1e6f5d5dc9e51c8f4e64d6c
Review one task for spec compliance.

Task brief: ## Task 6: Add the launch subcommand, the launch record and the shim check

Depends on: Task 2, Task 5

Add `launch --number <N> --source <D> --level worktree|full [--submit]` to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` and extend `tests/skills/test_issue_orca_worktree.py`. Source: design sections 6 and 8.4, and hook design `docs/designs/sc-issue-launch-level-hook.md` IR-1, IR-2, IR-5. Output: `{status, warning, detail, terminal, launched_at, enforcement_hook, hand_command}` with `status` one of `launched`, `failed`, `already_launched`.

Behaviour: read `worktree.json` in the source directory through the record guard (path exists, git-common-dir equals the main checkout's by realpath); a missing or failing record is `failed` with `W-LAUNCH-FAILED`. A record with a `launch` entry returns `already_launched` with its `at` time and calls neither `orca` nor writes a launch record. `enforcement_status()` returns `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`; `missing` sets `W-ENFORCEMENT-ABSENT` but does not stop the launch. Publish the launch record at `$HOME/.claude/state/launch-level/pending/<nonce>` (nonce `secrets.token_hex(16)`, directories mode 0700, file mode 0600, content exactly one word `worktree`, `full` or `full-submit`, written to a temporary name and renamed to the nonce); a write error is `failed` with `W-LAUNCH-FAILED` and no launch. Then run `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` with no `--model` and no `--effort`; a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command` (the same call without the marker). Then the ccsession shim check: take the first string value under any key named `handle` in the launch JSON by a recursive walk, call `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart (the sleep is injectable so tests run fast), and pass when `result.terminal.tail` text contains `[ccsession]` or `Session name (Enter or Ctrl+C`; no handle, an unreadable terminal or no match sets `W-LAUNCH-NOT-CCSESSION` and keeps the launch. Finally write `launch: {level, submit, at}` (UTC ISO time) into `worktree.json` whatever the shim result, and return `launched`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k launch` passes with LA-1 (exact launch argument list, prompt starts with `[sc-launch:v1:` plus 32 hex characters and `] `, no leading `/`, no `--model`, no `--effort`, no link flag), LA-2 (record is a regular file of mode 0600 in a 0700 directory holding the exact word for the level, published before the launch call, same nonce in the prompt), LA-3 (failed launch removes the record; read-only store makes no launch call), LA-4 (`launch` entry gives `already_launched` with no `orca` call; the entry is written even when the shim check fails), LA-5 (shim pass on `[ccsession]` and on the question text; fail on neither, unreadable terminal, no handle), LA-6 (`installed` and `missing` hook script, launch happens in both).
- No file is created inside the worktree or the source directory by `launch` other than the `launch` entry in `worktree.json`.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T6.AC1, T6.AC2, ... in the order of the 'Acceptance criteria:' bullets). Section 18 items that touch this task: A5 (`warning` holds the first code, every other applicable code is appended to `detail`; `enforcement_hook` is null on `already_launched`), B-6 (LA-7 no launch call for a failed worktree record; per-subcommand bad-argument case; on a launch timeout `detail` says to check Orca before re-running; `hand_command` states that a hand-started agent is not governed by the hook; the pending record stays after a failed shim check), the 0700 mode on each level of the pending path, and `launched_at` named as the `already_launched` time field.
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: ed51a97d3a9328a8f1e6f5d5dc9e51c8f4e64d6c
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T6-r1-2.patch (read it in full); the live files are in the repository for anchor checks
Delta diff from the previous reviewed tree (empty on the first review): the unified diff is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T6-r1-2-delta.patch (read it in full)
Earlier blocking findings of this start (empty on the first review): F6.1 ac=scope at=src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:615 anchor=src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:813 chk=n,y,n,n family=remedy-after-agent-started fix=use a distinct text for the record-update failure; the agent is running so the claim must not be re-run: when the launch entry cannot be written after a successful launch, detail carries the remedy "re-run the claim", which would start a second agent.

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
