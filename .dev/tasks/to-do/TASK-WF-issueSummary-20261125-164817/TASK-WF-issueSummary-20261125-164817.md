---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-issueSummary-20261125-164817
version: "1"
priority: Medium
created_date: "2026-11-25"
---

# Add the OB-H3 scratch file and open one unmerged pull request (issue 842)

Source: ./source.md
Goal: `.dev/ll-obs/C.txt` exists with the single line `observation C`, it is committed on a feature branch and pushed, and exactly one pull request against IronbellyOrg/IronClaude is open and not merged.

## Constraints

- Create only `.dev/ll-obs/C.txt`. Change no enforcement code and open no ship gate; the source calls this a disposable change for the OB-H3 observation.
- Never merge the pull request. Never push to the default branch (the source names `integration`; `master` and `main` are also off limits). Push only the current feature branch to `origin`.
- Open the pull request only through `/sc:pr-submit --monitor 3`, which targets IronbellyOrg/IronClaude.
- Stage `.dev/tasks` and the changed file. Never stage anything under `.claude/` or `.dev/issues/`.
- The coordinator closes the pull request without merging and closes the issue; this plan does neither.

## Phase 1: Create the scratch file

## Task 1: Create .dev/ll-obs/C.txt

Create the directory `.dev/ll-obs/` (it does not exist today) and write the file `.dev/ll-obs/C.txt` holding exactly one line, `observation C`, ended by a single newline. Touch no other file. The file has no code callers or dependents (see `./artifacts/codegraph-grounding.md`).

Acceptance criteria:
- `.dev/ll-obs/C.txt` exists and its content is exactly `observation C` plus one trailing newline.
- `git status --short` shows `.dev/ll-obs/C.txt` as the only change under `.dev/ll-obs/` and no change to any source, test or hook file.

## Phase 2: Publish

## Task 2: Commit, push and open one pull request

Depends on: Task 1

On the current feature branch, stage `.dev/ll-obs/C.txt` and `.dev/tasks`, and commit with a conventional-commit message such as `chore(ll-obs): add OB-H3 scratch file C.txt`. Run `git push origin <current feature branch>`. Before committing, check with `gh pr list --repo IronbellyOrg/IronClaude --head <branch> --state all` that no pull request exists for the branch. Then run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` through the Skill tool. Do not merge.

Acceptance criteria:
- The commit on the feature branch contains `.dev/ll-obs/C.txt` and no path under `.claude/` or `.dev/issues/`.
- `git push origin <branch>` succeeds for the feature branch, and nothing is pushed to `master`, `main` or `integration`.
- `gh pr list --repo IronbellyOrg/IronClaude --head <branch> --state all` lists exactly one pull request, it is open, and its URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
