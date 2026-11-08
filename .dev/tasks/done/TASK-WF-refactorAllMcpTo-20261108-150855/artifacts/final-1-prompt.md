# Managed FINAL review (archive gate), attempt 1

You are the fresh, independent FINAL reviewer for a managed `/sc:implement` package. Do not trust the implementer's report. Start from an adversarial position: assume defects exist and look for them. You are read-only on the repository: do not edit any file except your own output file.

Repository root (absolute): /home/coder/workspaces/worktrees/IronClaude/mcp-litellm-migration
Package root (absolute): /home/coder/workspaces/worktrees/IronClaude/mcp-litellm-migration/.dev/tasks/to-do/TASK-WF-refactorAllMcpTo-20261108-150855
`./artifacts/` tokens in the ledger resolve against the package root.

## Inputs (read the real current files)

1. Plan: `<package>/TASK-WF-refactorAllMcpTo-20261108-150855.md` (16 tasks, `## Constraints` at line 17). Read it in full, in ranges of at most 150 lines.
2. Source snapshot: `<package>/source.md`. Design it points to: `<repo>/.dev/issues/454/design/design.md` (read only the parts you need).
3. Ledger: `<package>/progress.md` (37 lines). Read all of it. The latest `complete` line of each task is the one that counts; T14 was reopened after an owner decision (see its Ruling line and its second `complete` line).
4. Delivery files: the list `<package>/artifacts/final-1-delivery-files.txt` (131 repo-relative paths named in ledger `files=` fields). Read the current contents of the parts each task's AC concerns.
5. Whole product diff since the first task's start snapshot (6e1870367dd8fe9dc22746e993adb567c1aee5f3): `<package>/artifacts/review-diffs/final-1-product.diff` (2924 lines, 125 files). It excludes the package, `.dev/issues`, `.dev/reflect` and the untracked new test `tests/skills/test_mcp_proxy_names.py` (read that file directly). `.mcp.json` shows as deleted (Task 14 reopen, owner-approved).
6. Every file under `<package>/artifacts/retries/T<id>/` (notes.md, prompt-*.md, review-*.out, probe-*.md, q0-head) for every task, including `retries/T14/reopen-1/`, and any `superseded-prompts/` folder if present. Also read every brief named by a `retry … step=revert` ledger record, if any.
7. The evidence logs in `<package>/artifacts/` (t1-pytest.log to t16-*.log, including the `t16-rerun-*.log` files written after the T14 reopen).

Severity rules: `~/.claude/skills/sc-implement-protocol/refs/qa.md`, sections "## Severity model", "## FINAL derived test" and "## Managed FINAL review (archive gate)". Read those sections before judging. Only a `blocking` defect at the end state makes the result `issues`. A notes entry whose checklist answers are all `n` is never `issues`; a confirmed `yes` is `issues`. A per-task `evidence=` line number that moved because a later task edited the file is never `issues` on its own. Saved prompts `prompt-<k>-<j>.md`: compare the lines after the start-sha header and outside the slots with the reviewer template in qa.md as that section says; blank-line or trailing-whitespace-only differences are notes, not `issues`.

## What to check

- For every task T1 to T16 and every AC id (`Ti.ACk`) in the plan: met or unmet at the end state, with `path:line` evidence from the current files or the package logs, not copied from the ledger.
- Every plan `## Constraints` item holds at the end state. In particular: no `.claude/` mirror is staged (`git diff --cached --name-only -- .claude` must be empty), nothing under `.dev/issues/` is staged, no `src/superclaude/...` path was added to an installed primitive as an instruction to read another primitive, no secret or token value appears in the diff, and no commit was made (HEAD is 0423fe5f1feabe5bf826a2a131c1e24a2dadf188).
- No later change contradicts an earlier task's AC (for example a later task re-introducing an old tool name a prior task removed).
- Each log cited on a task's latest `complete` line shows success at its outcome line. The final suite numbers are in `t16-rerun-make-test.log`, lint in `t16-rerun-lint.log`, sync in `t16-rerun-verify-sync.log` and `t16-rerun-sync-dev.log`.
- T14 reopen: `.mcp.json` is gone, nothing in the repo still depends on the repository-root `.mcp.json` (docs, installer text, hooks, Makefile, tests), and `tests/cli/test_mcp_project_config.py` asserts the auggie stdio entry is absent.

You may run read-only commands (git diff, git status, grep, and `uv run pytest -p no:cacheprovider <path>` for spot checks). Never run `python` bare; use `uv run`. Do not modify, stage or delete anything.

## Output

Create the output file `<package>/artifacts/final-1.out` as a stub first, then fill it section by section. Format:

```
FINAL review attempt 1. State at start: 6aead53f5721edcd9262b3a7a85521c0f8798ee9f43edb9cef183189f3981dba
Result: pass | issues

Per-task AC
T1.AC1 met <path:line> ...
(one line per AC id, every task)

Constraints
<one line per constraint item: holds | violated <path:line>>

Notes read
<one line per task: notes lines read, any confirmed yes (none expected)>

Saved prompts
<one line per task: compared, result>

Blocking findings
<none | one line each: id, path:line, what is wrong, which AC or constraint>

Minor findings (non-blocking)
<one line each>

Self-audit
<what you actively checked and why no blocking defect exists, if the result is pass>
```

When done, reply with only the absolute path of `final-1.out` and the one word `pass` or `issues`.
