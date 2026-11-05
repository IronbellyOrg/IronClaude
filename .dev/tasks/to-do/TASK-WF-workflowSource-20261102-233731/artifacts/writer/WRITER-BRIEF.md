# Implementer brief (one task of a /sc:implement run)

Repo root: /home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0 (IronClaude, tag v5.0.0; this worktree is the tagged code). Your task number N is given in your prompt.

- Plan: `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md`. Read its `## Constraints` section and the section `## Task N:` in full; implement ONLY Task N.
- If the task names an item (A-W*, B-W*, C-W*) or a guide row (D01-D16, E01, E02) in `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md` (sections "Writer worklist" and "Test guide plan (D and E)"), read that item or row in full and apply every numbered correction or listed capability in it (match target files by quoted text, not line number).
- Supporting evidence: `.dev/releases/current/v5.0.0/post-release/scan/` (A1, A2, B, C, DE1, DE2 inventories) and `docs/testing/v5.0.0/c-e2e-transcript.txt` / `c-e2e-run.sh`.
- Guides (D/E): Read the template named in the Constraints first and keep its structure; group steps under Tier A (free), Tier B (local writes in a throwaway HOME or /tmp), Tier C (API, proxy, PR or long runs) headings as the Test guide plan describes; fill the template header fields (Capability, Audience, Source of truth, Est. time; Gate for sysop guides).

Rules:

- Verify every corrected or new claim against the code or `uv run superclaude <cmd> --help` before writing it. If a planned correction is wrong against code, write the code-true statement and append the item, the planned text and the evidence to `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/artifacts/deviations.md`.
- A removal check in an AC ("grep X returns nothing", "contains no X") means the doc must not present X as usable; prefer removing the mention over describing its absence, unless the item tells you to state it.
- Never file issues, push, commit, stage, or write post-release-report/manifest files. `[EXTERNAL]` guide steps are only written, never run. Do not install anything into `~/.claude` or the user's pipx; do not touch running ccsession shims.
- Guides that run Claude Code sessions against the tester's real `~/.claude`: do not say a session writes only its own history. The installed hooks also write `~/.claude/state/` and `~/.claude/logs/`: the freshness hooks at session start and on each prompt (`src/superclaude/hooks/hooks.json:18,49`; `hooks/scripts/freshness-session-start.sh:8-9`, `freshness-user-prompt.sh:8-10`), and `auggie-flag-clear.sh` after auggie tool calls (PostToolUse, `hooks.json:104`; `auggie-flag-clear.sh:10-12`); say so.
- Do not edit files other than those the task and its item name. After editing anything under `src/superclaude/` or `plugins/`, run `make sync-dev` then `make verify-sync`; never stage `.claude/`.
- Save any artifact the AC asks for (`./artifacts/<name>`) under `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/artifacts/`. Run checks with `PYTHONDONTWRITEBYTECODE=1` and remove caches/temp files they create inside the repo.
- Check your own acceptance criteria before finishing. Markdown check: `npx --yes markdownlint-cli@0.38.0 -c .markdownlint.json <file>`; fix every violation in files you create and in lines you touch (pre-existing violations on untouched lines: fix them if trivial, else record them in deviations.md).

When done, write the list of repo-relative paths you created or modified (one per line; include files you wrote under the package `artifacts/`, excluding the files list itself) to `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/artifacts/writer/T<N>-files.txt`. Return only a 5-line summary.
