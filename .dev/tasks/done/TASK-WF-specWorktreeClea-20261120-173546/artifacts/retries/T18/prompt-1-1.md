6bd8fc9836cd09a324190eb72a72d227d4d63274
Review one task for spec compliance.

Task brief: ## Task 18: Write the automation definition (switched off) and its test

Depends on: Task 12

Create `scripts/worktree_cleanup_orca_automation.md`, modelled on `scripts/merged_pr_log_orca_automation.md` (it has the lines `Name:`, `Trigger (UTC):`, `Status:`, then "Why the name and the trigger are what they are", "Command to run (precheck shape)", "Environment variables (names only; no value belongs in any file)", "Human steps, in order" and "When a run fails"). Name: `worktree-cleanup-daily` (never starts with `coordinator-`). Trigger (UTC): `0 8 * * *`, with the note that this is 2:00 AM Central in winter and 3:00 AM in daylight saving time, and that whether `--timezone America/Chicago` can hold 2:00 AM all year is UNVERIFIED (source section 11, item 8). Status: `written, not switched on`. The command is the precheck shape of source section 5: `bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1`, with no `--apply` in it, and the text says the skipped run shows as `skipped_precheck` and that this is UNVERIFIED in this Orca build (item 6). Add the rollout ladder (switched on by each workspace's owner; first week report only; read the tables; then the owner edits the automation to add `--apply`; the worker does none of this), the environment names without values, and "When a run fails". Create `tests/worktree_cleanup/test_automation_definition.py` asserting these fields, that the command contains `prune` and no `--apply`, ends with `exit 1`, that the name does not start with `coordinator-`, that no token value appears, and that there is no em or en dash.

Acceptance criteria:
- `scripts/worktree_cleanup_orca_automation.md` exists with Name `worktree-cleanup-daily`, Trigger `0 8 * * *`, Status `written, not switched on`, and the command above.
- `uv run pytest tests/worktree_cleanup/test_automation_definition.py -v` passes.
- No Orca automation was created, run or switched on to produce the file (definition text only).

AC ids (in source order): T18.AC1, T18.AC2, T18.AC3
Global constraints: ## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.
- The pull request for this change is opened by the finishing step of the run, `/sc:pr-submit --monitor 3` (source section 15, step 7), after the last task; no task of this plan opens it.
- Corrections the implementer made to this plan before the first task started, from the advisory reflect review of the plan (the list is in `./artifacts/plan-corrections.md`): Task 1 (the item 1 fallback, the open pull request proof, item 7), Task 2 (a positive allowlist runner and its own first tests), Tasks 3 to 5 (their own tests, so no check waits for a later task), Task 7 (shared fixtures only), Tasks 11 and 12 (Orca read back, the command list in the JSON), Task 14 (the write-verb classification), Task 19 (15 rows), Task 20 (dependencies).
Start sha: 6bd8fc9836cd09a324190eb72a72d227d4d63274
Diff against the start snapshot: 
===== new file: scripts/worktree_cleanup_orca_automation.md =====
# Orca automation for the worktree cleanup

Definition only. Nothing in this file has been created in Orca, switched on or triggered. A person sets the automation up in Orca once, and the owner of each workspace switches it on.

The exact file format Orca expects for an automation is not confirmed here. The fields below are what a person enters when creating the automation.

Name: worktree-cleanup-daily
Trigger (UTC): 0 8 * * *
Status: written, not switched on

## Why the name and the trigger are what they are

- The name must not start with `coordinator-`. Orca run history under that prefix is copied into the daily work report, and this job must stay out of it.
- Orca triggers are UTC, so the cron string is in UTC: 08:00 every day of the week. That is 2:00 AM Central in winter and 3:00 AM Central in daylight saving time. Whether the `--timezone America/Chicago` option can hold 2:00 AM all year, for a cron string and not only for a preset such as `daily --time 02:00`, is UNVERIFIED (source section 11, item 8). If it cannot, keep `0 8 * * *`.
- The command below has no `--apply`. The script's default is a dry run, so this job only prints and writes the table of what it would remove (`prune-<UTC stamp>.md` and `.json` under the output folder) and removes nothing.

## Command to run (precheck shape)

This is the shape the workspace's existing scheduled jobs use (not re-verified here): load the workspace environment, start the script detached, and exit non-zero so Orca starts no agent session and leaves no terminal. A run that exits this way shows as `skipped_precheck`; that this happens in this Orca build is UNVERIFIED (source section 11, item 6). `<checkout>` is a checkout of this repository and `<out dir>` is a folder outside every worktree.

```
bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1
```

`uv run --no-project` is used on purpose: a plain `uv run` inside a checkout can rewrite `uv.lock`, which an unattended job must not do. The script itself reads credentials only from environment variables; the command above only loads the workspace's own environment first. If the variables are already in the environment of the process Orca starts, drop the two `. ~/...` loads.

## Rollout ladder

1. The owner of each workspace switches the automation on. Nobody switches it on for another workspace, and a dispatched worker does none of this.
2. The first week it reports only: the command stays exactly as written above, with no `--apply`. Each day the owner reads the table in `<out dir>`.
3. When the tables show only worktrees the owner would remove by hand, the owner edits the automation and adds `--apply` to the command. This edit is the owner's decision and is never made by a worker.

## Environment variables (names only; no value belongs in any file)

- `GH_TOKEN`: a token that can read pull requests and issues in IronbellyOrg and, for the evidence push, write to `IronbellyOrg/run-evidence`.

Optional, not secret: `RUN_EVIDENCE_REPO` (default `IronbellyOrg/run-evidence`), `RUN_EVIDENCE_DIR` (the local clone of the evidence repo) and `WORKTREE_CLEANUP_IDLE_DAYS` (default 7).

## Human steps, in order

- Run `uv run --no-project python scripts/worktree_cleanup.py list` once by hand in the workspace and read the table.
- Run `prune` once by hand without `--apply` and read the two files it writes under the output folder.
- Create the automation in Orca from the fields at the top of this file and leave it switched off.
- The workspace owner switches the automation on, then follows the rollout ladder above.

## When a run fails

A failed run exits non-zero and removes nothing it could not finish: a worktree whose save or check failed is kept, and the table shows the reason. Because the name stays out of the daily work report, nothing else reports the failure. `<out dir>/run.log` holds the error text (it never holds a token), and the newest `prune-<UTC stamp>.md` shows when the job last ran.


===== new file: tests/worktree_cleanup/test_automation_definition.py =====
"""The definition file of the daily Orca automation (Task 18): text only, switched off.

Nothing here creates, runs or switches on an automation; the test reads one Markdown file.
"""

from __future__ import annotations

import re
from pathlib import Path

DEFINITION = (
    Path(__file__).resolve().parents[2] / "scripts/worktree_cleanup_orca_automation.md"
)


def text() -> str:
    return DEFINITION.read_text(encoding="utf-8")


def field(name: str) -> str:
    match = re.search(rf"^{re.escape(name)}: (.+)$", text(), re.M)
    assert match, f"no {name} line"
    return match.group(1).strip()


def command() -> str:
    section = text().split("## Command to run (precheck shape)", 1)[1]
    block = section.split("```", 2)[1]
    return block.strip()


def test_the_three_header_fields():
    assert field("Name") == "worktree-cleanup-daily"
    assert field("Trigger (UTC)") == "0 8 * * *"
    assert field("Status") == "written, not switched on"


def test_the_name_never_starts_with_coordinator():
    assert not field("Name").startswith("coordinator-")


def test_the_sections_of_the_model_file_are_all_there():
    body = text()
    for heading in (
        "## Why the name and the trigger are what they are",
        "## Command to run (precheck shape)",
        "## Rollout ladder",
        "## Environment variables (names only; no value belongs in any file)",
        "## Human steps, in order",
        "## When a run fails",
    ):
        assert heading in body, heading


def test_the_command_is_the_precheck_shape_for_prune_without_apply():
    cmd = command()
    assert cmd.startswith("bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv;")
    assert "[ -f ~/.env ] && . ~/.env; set +a;" in cmd
    assert (
        "setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune"
        in cmd
    )
    assert "--out <out dir>" in cmd and ">> <out dir>/run.log 2>&1 < /dev/null &" in cmd
    assert re.search(r"\bprune\b", cmd)
    assert "--apply" not in cmd  # the first week reports only
    assert cmd.endswith("'; exit 1")


def test_the_trigger_notes_and_the_unverified_items_are_stated():
    body = text()
    assert "2:00 AM Central in winter" in body and "3:00 AM" in body
    assert "--timezone America/Chicago" in body
    assert body.count("UNVERIFIED") >= 2
    assert "skipped_precheck" in body


def test_the_rollout_ladder_and_the_environment_names():
    body = text()
    ladder = body.split("## Rollout ladder", 1)[1].split("\n## ", 1)[0]
    assert "first week it reports only" in ladder
    assert "adds `--apply`" in ladder
    assert "a dispatched worker does none of this" in ladder
    for name in (
        "GH_TOKEN",
        "RUN_EVIDENCE_REPO",
        "RUN_EVIDENCE_DIR",
        "WORKTREE_CLEANUP_IDLE_DAYS",
    ):
        assert f"`{name}`" in body


def test_no_token_value_appears():
    body = text()
    assert not re.search(r"(GH_TOKEN|GITHUB_TOKEN)\s*=\s*\S", body)
    # token shapes, spelled from two pieces so this file holds none itself
    shapes = [
        r"gh" + r"[pousr]_[A-Za-z0-9]{20,}",
        r"github" + r"_pat_[A-Za-z0-9_]{20,}",
    ]
    for shape in shapes:
        assert not re.search(shape, body)


def test_no_em_or_en_dash():
    dashes = (chr(0x2014), chr(0x2013))  # built from code points so this file has none
    for content in (text(), Path(__file__).read_text(encoding="utf-8")):
        assert not any(d in content for d in dashes)


def test_the_file_only_describes_it_nothing_is_created_or_run():
    body = text()
    assert "Definition only. Nothing in this file has been created in Orca" in body
    assert "leave it switched off" in body


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

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
