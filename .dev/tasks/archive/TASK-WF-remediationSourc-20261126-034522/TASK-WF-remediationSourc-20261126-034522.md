---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261126-034522
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Apply the one-time Orca upstream override for issue 780 and record the result in CLAUDE.md

Source: ./source.md
Goal: Orca's stored record for this repository stops naming the upstream project as its identity when the one-time override takes effect (stored upstream null, project id github:ironbellyorg/ironclaude); the result, effective or not, is observed and written down with evidence; and the Orca paragraph of CLAUDE.md states the verified cause and the observed result without claiming more than was observed.

## Constraints

- Orca state is changed by exactly one repo.update call that carries only `upstream: null` for the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8. The Orca command line has no verb for it, so the call goes through the app's own client class in a one-off script.
- The agent must not restart Orca (it hosts every running agent session) and must not open this repo's Settings panel. Durability across an Orca restart and after opening that panel therefore stays unverified and is reported as such.
- No Orca link flag (`--issue`, `--pr` or any other) is passed in any command, no worktree is created, no upstream git remote is added, and the upstream repository (SuperClaude-Org/SuperClaude_Framework) is not contacted.
- Files that must not change: pyproject.toml, package.json, anything under src/superclaude, the Orca files orca-data.json and its backups, the Orca database, any git remote, the captured fixtures tests/sweep/fixtures/captured-worktree-current.json and tests/sweep/fixtures/captured-worktree-list.json (they record the old id as history), and every part of CLAUDE.md outside the Orca paragraph.
- The second state change that also replaces the repo icon (step B of the REPORT.md Proposed Fix) is not run without the owner's approval. If the override does not take effect, the decided fallback is to change Orca, which is outside this plan and is reported for the owner.
- Evidence files are written under ./artifacts/ inside this package. The one-off script is not a delivery file: it lives at `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js` and is not added to any commit.
- Timestamps written into any evidence file are copied from the output of `date -u +%Y-%m-%dT%H:%M:%SZ`, never typed from memory.

## Phase 1: Prepare the override

## Task 1: Write the one-off override script and record the before state

Create the file `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js` with the script text taken verbatim from the section "One-off script (from REPORT.md Proposed Fix)" of ./source.md. Before anything is run, check the pre-conditions and record the before state in `./artifacts/t1-before.txt`: the projectId printed by `orca worktree current --json`; the `upstream`, `gitRemoteIdentity` and `repoIcon` (type and source) fields printed by `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`; whether each of the environment variables ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT is set or unset (never print a value that is set); whether the file `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json` exists and holds an `upstream` object for the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8 (the rollback record); and the output of `node --version`. Use only read-only commands with no link flag.

Acceptance criteria:
- The script file exists at the path above, contains a single `repo.update` call whose updates object holds only `upstream: null`, and contains no link flag and no other update field.
- `./artifacts/t1-before.txt` records every pre-condition with its observed result (each of the three environment variables as set or unset, the rollback record as present or absent, node as available or missing) and the before readings, with a UTC timestamp from `date -u`.
- The before readings in `./artifacts/t1-before.txt` match what the commands printed: projectId is github:superclaude-org/superclaude_framework and upstream is the SuperClaude-Org/SuperClaude_Framework object, or the file states the different values that were observed.
- No Orca state was changed by this task: a second `orca repo show` after the task prints the same upstream as before.

## Phase 2: Apply the override and observe

## Task 2: Run the override once and record the outcome

Depends on: Task 1

Read `./artifacts/t1-before.txt`. If every pre-condition it records passed (all three environment variables unset, the rollback record present, node available), run the script `.dev/troubleshoot/bug-orca-registers-this-repository-under-20261126031957/override-upstream-null.js` once with `node`, with no retry, and capture its standard output and error. Then repeat the two readings of Task 1 (the projectId from `orca worktree current --json`, and `upstream`, `gitRemoteIdentity`, `repoIcon` from `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`) and write everything to `./artifacts/t2-after.txt`, with the exact commands run, the script output and a UTC timestamp from `date -u`. If any pre-condition failed, do not run the script and write that to `./artifacts/t2-after.txt` instead. Write `./artifacts/t2-outcome.md`; its first line is exactly one of `outcome: effective` (upstream reads null and projectId reads github:ironbellyorg/ironclaude), `outcome: applied-not-effective` (the call reported success but the readings still show the upstream) or `outcome: not-applied` (a pre-condition failed or the call failed). Later lines state that Orca was not restarted and the repo's Settings panel was not opened, that durability across a restart and after opening that panel is unverified, and the two checks the owner should make (restart Orca and open the repo's Settings panel, then read the two states again). When the outcome is not `effective`, add a line that the decided fallback is to change Orca and that the repo-icon change needs the owner's approval.

Acceptance criteria:
- The script was run at most once, and only if every pre-condition in `./artifacts/t1-before.txt` passed; `./artifacts/t2-after.txt` lists every command that was run and none carries a link flag (`--issue`, `--pr` or similar), a worktree creation or a git remote change.
- `./artifacts/t2-after.txt` holds the after readings and the script's output, and the first line of `./artifacts/t2-outcome.md` is exactly one of the three outcome values and agrees with those readings.
- `./artifacts/t2-outcome.md` states that no Orca restart and no Settings panel opening took place, and names the two owner checks.
- Orca still answers `orca worktree current --json` after the call, and the repo with id e8e07d51-c261-4936-815e-06aeceeb5bf8 is still listed by `orca repo list`.
- If the outcome is not `effective`, the repository is unchanged by this task and the reason is written in `./artifacts/t2-outcome.md`.

## Phase 3: Record the result in the repository

## Task 3: Rewrite the Orca paragraph of CLAUDE.md

Depends on: Task 2

Edit only the paragraph of CLAUDE.md that begins `**Orca:**` (line 54, inside the section "ABSOLUTE RULE: PR Target = Fork"). Replace the sentence that says the source of the id is unverified (possibly the upstream URLs in pyproject.toml or package.json) with the verified cause: Orca derives the project id from the upstream field stored in its repo record before it looks at the git remote, the stored value equals the fork's GitHub parent, and pyproject.toml and package.json are not read. Then state the observed result by the first line of `./artifacts/t2-outcome.md`. For `outcome: effective`, give the date and the new id github:ironbellyorg/ironclaude and say that durability across an Orca restart and after opening the repo's Settings panel is not verified. For any other outcome, say only that the id still shows the upstream. Keep the rule that Orca link flags (`--issue`, `--pr` and others) are never passed for this repo, now worded as holding until the owner agrees to lift the ban (a corrected id alone does not lift it). Do not touch the section "Parallel Development with Git Worktrees": tests/core/test_claude_md_worktree_rule.py pins text there. The static fixtures tests/sweep/fixtures/captured-worktree-current.json and tests/sweep/fixtures/captured-worktree-list.json keep the old id as history and are not edited.

Acceptance criteria:
- The paragraph still begins with `**Orca:**`, names the verified cause (stored upstream read before the git remote; pyproject.toml and package.json not read), and no longer contains the phrase "possibly the upstream URLs in".
- The paragraph's result statement matches the first line of `./artifacts/t2-outcome.md`, and for any outcome other than `effective` it makes no claim that the id was corrected.
- The sentence that Orca link flags are never passed for this repo is kept and says the ban holds until the owner agrees to lift it.
- `git diff --stat` shows CLAUDE.md as the only tracked file changed by this task, and `git diff` for CLAUDE.md touches only the Orca paragraph.
- `uv run pytest tests/core/test_claude_md_worktree_rule.py tests/core/test_claude_md_routing_block.py tests/core/test_orca_session_launch_guidance.py tests/core/test_default_branch_agreement.py tests/core/test_research_routing_rule.py -q` passes, and no Python file was edited.

## Phase 4: Hand over for the pull request

## Task 4: Write the pull request note with the identity evidence

Depends on: Task 3

Write `./artifacts/t4-pr-note.md`, the text the pull request description quotes. It holds these parts: the outcome (the first line of `./artifacts/t2-outcome.md` with one sentence of meaning); the evidence (the before and after readings copied from `./artifacts/t1-before.txt` and `./artifacts/t2-after.txt`); the owner checks that remain (restart Orca and open the repo's Settings panel, then read `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json` again, expecting upstream null and project id github:ironbellyorg/ironclaude); the fallback (if the id reverts, the next try is the second state change that also replaces the repo icon, which needs the owner's approval, then changing Orca); a line that issue 769 (trimming the CLAUDE.md startup context) also touches the same paragraph and asks for fresh identity evidence, which this note supplies; and the keyword line, which says to write `Refs #780` and not `Fixes #780`, because durability is unverified and the link-flag ban stays until the owner agrees to lift it. The note also carries the decided route word for word: Question: Change Orca so origin wins, or override the stored upstream once? Decided: Try the one-time override first; if it does not hold, change Orca.

Acceptance criteria:
- `./artifacts/t4-pr-note.md` exists and holds the outcome, the before and after readings, the owner checks, the fallback, the issue 769 line and the keyword line, each as its own labelled part.
- The decided route sentence appears in the note word for word as written in this task.
- The readings in the note equal the readings in `./artifacts/t1-before.txt` and `./artifacts/t2-after.txt`, and the note makes no claim of durability.
- The note's keyword line says `Refs #780`, and the note names what is left (the two owner checks and the lifting of the link-flag ban).
