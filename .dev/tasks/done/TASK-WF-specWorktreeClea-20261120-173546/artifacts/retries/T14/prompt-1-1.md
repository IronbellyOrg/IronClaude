717e440a21ff0663988ee43a6c1d63706dca3302
Review one task for spec compliance.

Task brief: ## Task 14: Add the `/sc:worktrees` command file and its static test

Depends on: Task 12

Create `src/superclaude/commands/worktrees.md`, modelled on `src/superclaude/commands/closeout.md` (frontmatter with name `worktrees`, version, description, category `workflow`, complexity, `mcp-servers: []`, personas, and `argument-hint: "<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"`; sections Triggers, Usage, Options, STOP rules, Examples, Outputs, Boundaries). It is a thin command and a command, not a skill (source section 5): it runs `uv run --no-project python scripts/worktree_cleanup.py <verb> ...` from the top of the current git checkout (`git rev-parse --show-toplevel`) and prints the table; no skill is activated. Decision made by this plan because `scripts/` does not install with the command: when `scripts/worktree_cleanup.py` does not exist at the top of the current checkout, the command stops, runs nothing and prints "`/sc:worktrees` runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`". It passes `--apply` only when the person typed it, never adds `--apply` or any force flag, and says in Boundaries that it never merges, never pushes to a source repo, that removal needs `--apply`, and (as `src/superclaude/commands/sweep.md` does in its line 18) that it is for a person only and is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`. Plain English, no em or en dashes, no `src/superclaude/...` path in the text (the repository rule for installed primitives). `tests/skills/test_worker_contract.py` scans the command files for literal `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` or `git worktree remove` and `gh pr` or `gh api` text and fails on an unclassified hit (its `WRITE_VERB_CLASSIFICATION` table), so the command text avoids those literal verbs (or the table gets a classified entry for each). Then create `tests/commands/test_worktrees_command.py` modelled on `tests/commands/test_closeout_command.py` (static tests of the command file text).

Acceptance criteria:
- `tests/commands/test_worktrees_command.py` passes and asserts: frontmatter fields and the exact `argument-hint`, the four verbs and the `--apply` and `--out` options in the Options table, the outside-a-checkout stop sentence, that none of `--force`, `--yes` or `--unattended` appears as an option, that no `src/superclaude/` path appears, and that the file has no em or en dash.
- `make sync-dev` copies the command to its dev copy and `make verify-sync` is clean for it (the dev copy is gitignored and is not staged).
- `superclaude install`'s glob in `src/superclaude/cli/install_commands.py` picks the file up with no list edit (no change to that file).

AC ids (in source order): T14.AC1, T14.AC2, T14.AC3
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
Start sha: 717e440a21ff0663988ee43a6c1d63706dca3302
Diff against the start snapshot: 
===== new file: src/superclaude/commands/worktrees.md =====
---
name: worktrees
version: "1.0.0"
description: "List the git worktrees of our repos with the reason each is kept or removable, save a finished worktree's .dev files to the evidence repo, and remove the ones whose work is safe (a dry run unless --apply is typed)"
category: workflow
complexity: standard
mcp-servers: []
personas: [analyzer]
argument-hint: "<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"
allowed-tools: Bash
---

# /sc:worktrees: Clean Up Finished Git Worktrees

`/sc:worktrees <verb>` runs the cleanup script of this checkout, `scripts/worktree_cleanup.py`, and prints its table. A worktree is removed only when all eight rules hold: it is a linked worktree of one of our repos, its own pull request is merged, nothing was added after that pull request, every issue it relates to is closed, nothing unsaved is in it, nothing but its own Orca terminals is using it, it has been idle for the idle floor, and it is not pinned. Untracked and ignored `.dev/` files are first saved to the evidence repo and checked against GitHub. If anything cannot be read or finished, the worktree is kept and the reason is shown.

Every verb is a dry run unless you type `--apply`. `/sc:worktrees` is for a person only. It is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`, so a dispatched worker never runs it.

## Triggers

Explicit only: a person types `/sc:worktrees <verb>`. Nothing starts it automatically.

## Usage

```text
/sc:worktrees list
/sc:worktrees archive <worktree> [--out <dir>]
/sc:worktrees retire <worktree> [--apply] [--out <dir>]
/sc:worktrees prune [--apply] [--out <dir>]
```

## Options

| Argument | Meaning |
|---|---|
| `list` | Print the table of every worktree of every repo of ours with its decision and reason; removes nothing |
| `archive <worktree>` | Run only the save step for one worktree and print `VERIFIED` when the copy matches GitHub; removes nothing |
| `retire <worktree>` | Remove one worktree whose work is safe; run it from outside that worktree; takes a path or a unique folder name |
| `prune` | Apply the same decision to every worktree; with `--apply` it removes the removable ones, without it it writes the table to `<out>/prune-<UTC stamp>.md` and `.json` |
| `--apply` | Actually remove. Pass it only when the person typed it. Without it nothing is removed |
| `--out <dir>` | The folder for the table files and the per-repo lock files; never inside a worktree (default `~/.local/state/worktree-cleanup`) |

## STOP rules (checked before anything runs)

Print the usage block and stop, running nothing, for: no verb; a verb that is not one of the four; `archive` or `retire` without a `<worktree>`; an unknown flag; a flag with no value. When `scripts/worktree_cleanup.py` does not exist at the top of the current git checkout (found with `git rev-parse --show-toplevel`), print "`/sc:worktrees` runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`" and stop, running nothing.

## Activation

Run this one command from the top of the current checkout, passing the person's arguments unchanged and adding nothing:

```text
uv run --no-project python scripts/worktree_cleanup.py <verb> [<worktree>] [--apply] [--out <dir>]
```

No skill is activated. Print the table and the summary line it prints. The exit code is 0 when the run completed, 64 for a usage error or a `retire` of a worktree that is not removable, and 69 when a lookup or a removal failed (the table still shows what happened).

## Examples

```text
/sc:worktrees list
/sc:worktrees archive issue-687
/sc:worktrees retire issue-687 --apply
/sc:worktrees prune
```

## Outputs

One table with a row per worktree (repo, folder, branch, in Orca, pull request, issues, idle days, size, saved copy, decision, reason), then one summary line with the counts of removed, kept and failed. `prune` also writes `prune-<UTC stamp>.md` and `.json` under `--out`; the JSON holds the same rows and the list of commands that ran. The script writes nothing inside any worktree.

## Boundaries

**Will:**

- Run the script of this checkout with the arguments the person typed and print its table
- Pass `--apply` only when the person typed it

**Will Not:**

- Add `--apply`, a force flag or any other flag of its own
- Merge anything, push to a source repo or delete a remote branch
- Remove, move or clear anything without `--apply`
- Run as a dispatched worker
- Run outside an IronClaude checkout that has `scripts/worktree_cleanup.py`

## Related Commands

| Command | Difference |
|---|---|
| `/sc:sweep` | A read-only report on Orca Runs, worktrees and sessions; it changes nothing |
| `/sc:closeout` | Settles a merged pull request and its issue; it does not touch worktrees |


===== new file: tests/commands/test_worktrees_command.py =====
"""Static tests for the /sc:worktrees command file (issue 687, source section 5).

Enforcement type: STATIC (command file text).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "src/superclaude/commands/worktrees.md"

OPTION_ROWS = ["list", "archive", "retire", "prune", "--apply", "--out"]
FORBIDDEN_OPTIONS = ["--force", "--yes", "--unattended"]
STOP_SENTENCE = (
    "`/sc:worktrees` runs only inside an IronClaude checkout "
    "that has `scripts/worktree_cleanup.py`"
)
RUN_LINE = (
    "uv run --no-project python scripts/worktree_cleanup.py "
    "<verb> [<worktree>] [--apply] [--out <dir>]"
)


def _text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def _frontmatter() -> dict:
    head = _text().split("\n---\n", 1)[0]
    assert head.startswith("---\n")
    fields = {}
    for line in head[4:].splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def _options_first_cells() -> list[str]:
    section = _text().split("## Options", 1)[1].split("\n## ", 1)[0]
    cells = []
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cell = line.strip().strip("|").split("|")[0].strip().strip("`")
        cells.append(cell.split(" ")[0])
    return cells


def _section(title: str) -> str:
    text = _text()
    start = text.index(f"## {title}")
    end = text.find("\n## ", start + 1)
    return text[start:] if end == -1 else text[start:end]


def test_frontmatter_fields():
    fields = _frontmatter()
    assert fields["name"] == "worktrees"
    assert fields["version"]
    assert fields["description"]
    assert fields["category"] == "workflow"
    assert fields["complexity"]
    assert fields["mcp-servers"] == "[]"
    assert "personas" in fields
    assert (
        fields["argument-hint"]
        == '"<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"'
    )


def test_the_sections_of_a_thin_command_are_all_there():
    text = _text()
    for title in (
        "Triggers",
        "Usage",
        "Options",
        "STOP rules",
        "Examples",
        "Outputs",
        "Boundaries",
    ):
        assert f"\n## {title}" in text, title


def test_options_table_lists_the_four_verbs_and_the_two_options():
    assert _options_first_cells() == OPTION_ROWS


def test_no_forbidden_option_is_listed_or_offered():
    cells = _options_first_cells()
    for flag in FORBIDDEN_OPTIONS:
        assert flag not in cells
        assert flag not in _text()


def test_the_stop_sentence_for_outside_a_checkout_is_exact():
    stop = _section("STOP rules")
    assert f'print "{STOP_SENTENCE}" and stop, running nothing' in stop
    assert "git rev-parse --show-toplevel" in stop
    assert "usage block" in stop and "running nothing" in stop


def test_it_runs_the_script_with_the_typed_arguments_and_no_skill():
    activation = _section("Activation")
    assert RUN_LINE in activation
    assert "No skill is activated" in activation
    assert "adding nothing" in activation
    assert "Skill sc:" not in _text()


def test_apply_is_passed_only_when_typed():
    text = _text()
    assert "Pass `--apply` only when the person typed it" in text
    assert "Add `--apply`, a force flag or any other flag of its own" in _section(
        "Boundaries"
    )
    assert "dry run unless you type `--apply`" in text


def test_boundaries_and_the_worker_rule():
    text = _text()
    boundaries = _section("Boundaries")
    assert "**Will:**" in boundaries and "**Will Not:**" in boundaries
    assert "Merge anything, push to a source repo" in boundaries
    assert "Run as a dispatched worker" in boundaries
    assert "never-as-worker list in `~/.claude/WORKER-CONTRACT.md`" in text
    assert not re.search(r"^#+\s*Unattended mode", text, re.M | re.I)


def test_no_source_tree_path():
    assert "src/superclaude/" not in _text()


def test_no_em_or_en_dash():
    dashes = (chr(0x2014), chr(0x2013))  # built from code points so this file has none
    for text in (_text(), Path(__file__).read_text(encoding="utf-8")):
        assert not any(d in text for d in dashes)


def test_the_command_is_thin():
    assert len(_text().splitlines()) <= 110


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
