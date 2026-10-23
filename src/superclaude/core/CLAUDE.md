# SuperClaude — Framework Context

@BASH_INSPECTION_POLICY.md

## Python Environment

Use UV for all Python operations. Never use `python -m`, `pip install`, or `python script.py`.

```
uv run pytest                    # run tests
uv run pytest tests/path/ -v     # specific tests
uv pip install package           # install deps
uv run python script.py          # execute scripts
```

## MCP Servers

| Server         | Primary Use                                  | Flag (advisory) |
|----------------|----------------------------------------------|-----------------|
| auggie         | Codebase search — call before significant edits | (auto)  |
| serena         | Symbol navigation, project memory            | --serena   |
| context7       | Official library/framework docs              | --c7       |
| tavily         | Web search, current information              | --tavily   |
| playwright     | Browser automation, E2E testing              | --play     |

The Flag column is advisory: these are hints Claude may honour, not options every command accepts. A command's own flags are in its file under `~/.claude/commands/sc/`; check there before passing one.

## Core Rules

1. **UV only** — never `python -m` or bare `pip`
2. **Parallel by default** — batch independent tool calls; sequential only for true dependencies
3. **Confidence check** — ≥90% proceed, 70-89% present options, <70% ask. Trigger surface is not just code edits: run it (or its lightweight form — verify the specific token via `--help`/grep/file read/`codebase-retrieval`) BEFORE any reply that suggests an action, emits a command/snippet, or names a specific flag/path/function/version. Recommendation = action.
4. **Git** — feature branches only; never commit directly to master/main. `.dev/tasks/` is always staged (`git add .dev/tasks`): packages, ledgers and each package's `.dev/tasks/<pkg>/artifacts/` included. Never gitignore it, never leave it untracked. Staging is not committing. The project-root `artifacts/` is a different folder and is never staged
5. **Output paths** — write files next to their source or to the `--output` dir the CLI command specifies; `docs/generated/` is a roadmap pipeline artifact directory, not a general output sink
6. **Finish what you start** — no TODO stubs for core logic; if you begin a feature, complete it to working state
7. **Scope discipline** — build exactly what's asked; no speculative additions
8. **Auggie first** — call `codebase-retrieval` before significant edits to load relevant context
9. **Temporal** — verify current date from env context before any date/version reasoning

## Key Docs

- `~/.claude/HOW-WE-WORK.md` — which command or skill to use for each kind of work, in what order (read it when you choose a workflow; it is not loaded automatically)
- `~/.claude/RULES.md` — full behavioral rules (referenced by skills)
- `~/.claude/PRINCIPLES.md` — engineering principles (referenced by skills)

## How to choose a workflow

Decide how much process a job needs before you start. Use the first row that fits; if you are unsure between two rows, choose the heavier one.

<!-- level-table:v1 -->

| Level | Use this when | What you run | What you end up with |
|---|---|---|---|
| **1. Ask a question** | You want to understand code, a decision, or how something works, and you do not want anything changed. | Ask Claude in plain English. For an explanation of specific code, `/sc:explain src/jobs/runner.py`. | An answer. No files change. |
| **2. Make a small, direct change** | The change is in one source file (plus its test file), needs five edits or fewer, and you already know exactly what it should be. | Ask Claude to make the change and run the related test, or use `/sc:task "Rename recieved_at to received_at in src/jobs/runner.py and update its tests"`. `/sc:task` prints a `Tier:` line at the start. If it says `STANDARD` or `STRICT`, it runs the affected tests itself; if it says `LIGHT` (typos, comments, formatting) or `EXEMPT` (no code change, such as explain or commit), it skipped checking, so run the test yourself afterwards. | The edited file and a passing test. |
| **3. Follow a simple checked plan** | The change touches a few files, the requirements are clear, and it fits in one or two sessions. | `/sc:workflow "<what to change, why, which files>" --depth quick` writes a plan in which every step has acceptance criteria (a written definition of "done" for that step), then checks the plan against your request automatically. It prints the plan path, `.dev/tasks/to-do/<id>/<id>.md`, and the check result. `<id>` is the plan folder's name, for example `TASK-WF-retry-limit-20261013-142530`; the plan file is `<id>.md` inside it. Copy the path `/sc:workflow` prints. Read the plan, then run `/sc:implement <that path>`. It builds one step at a time and has a reviewer check each step against its criteria. | A plan folder holding the plan and `progress.md` (one line per step), plus the code changes in your repository. If interrupted, run the same `/sc:implement` command again; it continues from the first unfinished step. When every step passes, a final independent review runs and the folder moves to `.dev/tasks/done/`. On any system other than Linux (including macOS) the move is refused on purpose: the folder stays in `.dev/tasks/to-do/` and the run reports archive-blocked. That is expected; never move the folder by hand. |
| **4. Build and run a task file** | The work touches many files, will take more than one session, or must not drift from what was agreed. | `/task-builder "<what to build, why, which code>"` researches the code and writes a task file: a checklist under `.dev/tasks/to-do/`. If you have a spec, PRD, or TDD, add `--spec <path to it>` so the task file is checked against it. Read the task file, then run `/task <path to task file>`. | `/task` works through the checklist item by item. The items are grouped into phases; after each phase except the first (setup) one, a panel of independent reviewer agents checks the work. At the end it runs the tests and an independent audit comparing what was built with the plan. It survives crashes. |
| **5. Research first** | You do not yet know how the current system works, what needs to change, or whether the idea is feasible. | `/tech-research "<question, why you need it, which code to look at>"`. Then build the task file from it: `/task-builder "<what to build> as recommended in <path to the report>. Code: <folders>"` (level 4). | A report at `.dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md` with findings, options, and a recommended plan. |
| **6. Write a full specification** | You are building a new product, a new component, or a major feature that other people will build against. | `/prd`, then `/tdd`, then `/roadmap`. See workflow 3.1 of the routing guide (`HOW-WE-WORK.md`). | A product requirements document, a technical design document, a phased roadmap, and a task file for every phase. |

**Hard limit:** if the work needs more than 5 edits or touches more than one source file (its matching test file does not count), it must go through a written plan: level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier. An edit is one change in one place in a file (one block of consecutive changed lines); renaming a name used in 8 places is 8 edits. The one exception is `/sc:cleanup` and `/sc:improve` run on a folder (section 3.7 of the routing guide): commit first and review `git diff` afterwards.

<!-- /level-table -->

**`/sc:` commands must load their skill when their file names one.** When a message starts with `/sc:<name>` and that command's file (`~/.claude/commands/sc/<name>.md`) says to invoke a skill, invoke the matching skill with the Skill tool before any other output. That step is blocking: answering from your memory of the protocol instead is a violation. A command whose file names no skill runs from its own file. If context pressure would make you skip the skill or improvise, stop, warn the user, and tell them to run the command again in a new chat.

For the full step-by-step workflows, read `~/.claude/HOW-WE-WORK.md` with the Read tool when you need it (it is not loaded automatically). Unsure which tool fits? Run `/sc:recommend "<what you want to do, and why>"`. To see everything installed, run `/sc:help`.

Commands are in `~/.claude/commands/sc/`, skills in `~/.claude/skills/` (loaded on demand), agents in `~/.claude/agents/` (used by skills and commands).

## Context freshness discipline

Long sessions accumulate **derived facts** in working memory: file paths,
line numbers, IPs, credential IDs, mtime relationships. These age out
silently when the user (or other agents) modifies the underlying files.
The hook layer enforces this at edit time; this section binds the
behavior for **citations made in chat responses with no tool call**, which
hooks cannot catch.

### The five content-signal triggers

Treat the following as **mandatory re-verification triggers** before
output:

- **S1.** About to cite `file:line` or "at line N" of a specific file.
- **S2.** About to issue an Edit / Write / replace_content / replace_symbol_body
  / insert_*_symbol against a file. (Hook enforces; mention here for completeness.)
- **S3.** About to assert that file A agrees or disagrees with file B.
- **S4.** About to quote an IP, hostname, credential ID, port, path, or
  config value tied to a specific source file.
- **S5.** About to recommend an infrastructure change that depends on a
  remembered fact.

### Self-check pattern (factual phrasing)

Before producing output that hits S1, S3, S4, or S5: ask, "Did I Read the
source file in the last 5 tool calls of this turn, AND has nothing
modified it since?" If the answer is no, OR uncertain, perform a fresh
Read first. The cost of a Read is trivial compared to a wrong citation.

### Refresh-tool selection

Pick the refresh tool by the content type of the claim:

| Content | Tool |
|---|---|
| Exact line numbers / file content | `Read` |
| Symbolic queries (which function, where defined, what references) | `mcp__serena__find_symbol` / `find_referencing_symbols` |
| Semantic / cross-cutting ("is there an X anywhere") | `mcp__auggie__codebase-retrieval` |
| Runtime state (permissions, mounts, sockets) | `Bash` (user-executed read-only command) |

### Session context envelope

Every user prompt is prefixed with a `<session-context>` block injected
by the UserPromptSubmit hook. Fields like `turn=`, `Δ=`, `git=dirty=...`,
`changed_since_last_turn=...` are factual and current as of that prompt.
Treat as ground truth for that turn; do not override from older context.
