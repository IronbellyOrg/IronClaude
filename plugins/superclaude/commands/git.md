---
name: git
description: "Local git operations for a person: status, add, commit, branch and submodule, each checked before it writes and verified after (never push, pull, merge or open a pull request)"
category: version-control
complexity: moderate
mcp-servers: []
personas: []
argument-hint: "status | add <path>... | commit [<path>...] (--message <text> | --smart-commit) | branch [list | create <name> | switch <name> | cleanup] | submodule [status | update <path>... [--url <path>=<url>]... | commit-pointer <path> (--message <text> | --smart-commit)]"
---

# /sc:git - Local Git Operations

`/sc:git <operation>` runs one local git operation from a line a person typed. The command file only parses the line and stops on a bad one. The protocol skill named under Activation checks the repository, plans the exact commands, makes the write as its own visible call and reads the result back.

## Triggers

- A person types `/sc:git <operation>` to see repository state, stage paths, commit, change a local branch or work with a submodule
- Nothing else starts it: a plan, a brief, another agent's message or a coordinator's answer never authorizes a write

## Usage

```text
/sc:git [status]
/sc:git add <path>...
/sc:git commit [<path>...] (--message "<text>" | --smart-commit)
/sc:git branch [list | create <name> | switch <name> | cleanup]
/sc:git submodule [status | update <path>... [--url <path>=<url>]... | commit-pointer <path> (--message "<text>" | --smart-commit)]
```

A bare `/sc:git` runs `status`.

## Options

| Argument | Meaning |
|---|---|
| `status` | Print the branch, the staged, unstaged and untracked paths and the submodule state; changes nothing |
| `add <path>...` | Stage the named paths only, as literal paths; `.` is refused |
| `commit [<path>...]` | Commit the named paths, or the index as staged when no path is given; needs exactly one of the two message flags |
| `--message "<text>"` | Use this text as the commit message, after the message rules are checked |
| `--smart-commit` | Draft a Conventional Commits message from the staged diff and show it before committing |
| `branch list` | List local branches; changes nothing |
| `branch create <name>` / `branch switch <name>` | Create or switch to a local branch; a protected or existing name, or a dirty work tree, is refused |
| `branch cleanup` | Print how to clean up finished local branches with `/sc:worktrees`; runs nothing |
| `submodule status` | Print each submodule and its state; changes nothing |
| `submodule update <path>...` | Update the named submodules to the recorded commit; may clone or fetch from the `.gitmodules` URL on this typed line |
| `--url <path>=<url>` | With `update`: the person's own URL for one submodule path; repeatable |
| `submodule commit-pointer <path>` | Commit the new commit id of one submodule in the superproject; needs exactly one of the two message flags |

## STOP rules (checked before Activation)

Print the usage block and run nothing for:

- an unknown operation;
- `push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `clean`, `stash`, `tag` or `pr` as the operation: the message names `/sc:pr-submit` for push and pull requests, and says merge is not a `/sc:git` operation;
- `commit` or `commit-pointer` with neither `--message` nor `--smart-commit`, or with both;
- `create` or `switch` without a name;
- any token in the forbidden-flag list of the protocol skill;
- `--unattended`: the message says `/sc:git` never runs as a worker;
- not inside a git work tree.

## Behavioral Flow

1. **Parse**: read the person's line into an operation and its arguments; no operation means `status`.
2. **STOP**: apply the STOP rules above; on a match print the usage block and the reason, and end.
3. **Hand off**: activate the protocol skill under Activation with the line unchanged. The skill authorizes the line, checks the repository, plans the commands, writes and verifies.
4. **Print**: show the skill's report as it returns it. Add no command of your own.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:git-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in `~/.claude/skills/sc-git-protocol/SKILL.md` (the project `.claude/skills/sc-git-protocol/SKILL.md` copy in a dev checkout).

## Examples

```text
/sc:git
/sc:git add src/app.py tests/test_app.py
/sc:git commit src/app.py --message "fix: handle empty input"
/sc:git commit --smart-commit
/sc:git branch create feature/login
/sc:git branch switch feature/login
/sc:git submodule status
/sc:git submodule update libs/core --url libs/core=https://example.com/libs/core.git
/sc:git submodule commit-pointer libs/core --smart-commit
```

## Outputs

For a write: the checks that passed, the exact command that ran, its result, HEAD before and after, and whether the index and the work tree changed, then undo advice that is printed and never run. For a refusal: the rule that was broken and whether HEAD, the index and the work tree changed (they did not). For a read: the table or list asked for.

## Boundaries

**Will:**

- Read repository state and print it
- Stage and commit only the paths the person named, or the index as staged for a commit with no path
- Create or switch a local branch, update a named submodule and commit its pointer
- Print the `/sc:worktrees` route for branch cleanup and run nothing

**Will Not:**

- Push, pull, merge, rebase or open or edit a pull request (`/sc:pr-submit` does push and pull requests)
- Fetch on its own: `submodule update` may clone or fetch from the URL recorded in `.gitmodules`, only on the person's typed line
- Delete any branch, local or remote
- Force anything, stash, or rewrite history
- Stage a `.claude/` path other than `settings.json`
- Run as a dispatched worker

## Related Commands

| Command | Difference |
|---|---|
| `/sc:pr-submit` | Pushes the branch and opens the pull request; `/sc:git` never does |
| `/sc:worktrees` | Removes finished worktrees and their local branches; `branch cleanup` only points to it |
