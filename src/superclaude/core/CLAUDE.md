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

Match the requested outcome and any explicit command or existing plan first. Most planned implementation uses level 3; choose level 4 only for its stated explicit or exceptional machinery need. Research breadth and document output alone do not require an implementation plan.

<!-- level-table:v1 -->

| Level | Use this when | What you run | What you end up with |
|---|---|---|---|
| **1. Ask a question** | You want to understand code, a decision, or how something works, and you do not want anything changed. | Ask Claude in plain English. For an explanation of specific code, `/sc:explain src/jobs/runner.py`. | An answer. No files change. |
| **2. Make a small, direct change** | The change is in one source file (plus its test file), needs five edits or fewer, and you already know exactly what it should be. | Ask Claude to make the change and run the related test, or use `/sc:task "Rename recieved_at to received_at in src/jobs/runner.py and update its tests"`. Inspect the actual classification and verification evidence: STANDARD permits affected tests or documented manual verification; LIGHT includes scope/sanity checks; EXEMPT covers non-code operations. Do not assume every tier ran tests, describe LIGHT as unchecked, or report manual verification as a test pass. Run the related test if it has not run. | The bounded edit and its recorded verification, including an observed related-test result when available. |
| **3. Follow a checked implementation plan** | Ordinary implementation needs a written plan, including work across many files or several sessions, with or without an existing spec. | `/sc:workflow "<what to change, why, which files or spec>" --depth standard --handoff none` writes a plan with acceptance criteria (a written definition of "done" for each step) and runs an advisory check against your request. Standard is the default; use quick for smaller checked plans, not all ordinary work. It prints the actual plan path, `.dev/tasks/to-do/<id>/<id>.md`, and the check result. `<id>` is the generated plan folder's name. Read the plan and check result, then, only when execution is requested, run `/sc:implement <that path>`. It implements each step and checks compliance with its criteria. | A plan folder holding the plan and `progress.md` (one line per step), plus code changes if execution was requested. If interrupted, run the same `/sc:implement` command again; it continues from the first unfinished step. When every step passes, a final independent review runs and the folder moves to `.dev/tasks/done/`. On any system other than Linux (including macOS) the move is refused on purpose: the folder stays in `.dev/tasks/to-do/` and the run reports archive-blocked. That is expected; never move the folder by hand. |
| **4. Explicit or exceptional task-file work** | You explicitly select MDTM (the task-file/checklist format), supply an existing MDTM task for execution, or have an exceptionally complex, long-running phased program with a stated need for its research, checklist and phase-reviewer machinery. | For creation, `/task-builder "<what to build, why, which code, why MDTM>"` researches the code and writes a task file under `.dev/tasks/to-do/`. Add `--spec <path>` when a spec, PRD or TDD exists. Read the task file and check result; only when execution is requested, run `/task <path to task file>`. An existing MDTM task goes directly to `/task`, without rebuilding it. | The requested task file, or its execution through the checklist and reviewer panels after each phase except setup, followed by tests and a final audit. Resume with the same executor. |
| **5. Research first** | You do not yet know how the current system works, what needs to change, or whether the idea is feasible. | `/tech-research "<question, why you need it, which code to look at>"`. Stop at the report for a research-only request. If you decide to build, use `/sc:workflow "<what to build> as recommended in <report path>. Code: <folders>"`, then read its plan and use `/sc:implement <printed plan path>` when execution is requested (level 3). Level 4 needs its own explicit or exceptional justification. | A report at `.dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md` with findings, options, and a recommended plan; implementation is a separate decision. |
| **6. Write a full specification** | You need a PRD and TDD for a new product, component or major feature that others will build against. | `/prd`, then `/tdd`, with the requested reviews. Stop after the requested documents for document-only work. Ordinary subsequent implementation planning uses `/sc:workflow`, then `/sc:implement` when execution is requested. Offer `/roadmap` only for explicit composer selection or the exceptional level-4 machinery need; it internally uses `/task-builder` and `/task` and can create phase task files. See workflow 3.1 of the routing guide (`HOW-WE-WORK.md`). | The requested reviewed documents. Planning and execution are separate; expressly selected document skills and the roadmap composer keep their own internal machinery. |

**Hard limit:** if the work needs more than 5 edits or touches more than one source file (its matching test file does not count), it must go through a written plan: normally level 3, not automatic level 4. An edit is one change in one place in a file (one block of consecutive changed lines); renaming a name used in 8 places is 8 edits and requires a written plan. The one exception is contained `/sc:cleanup` and `/sc:improve` work on a folder (section 3.7 of the routing guide): commit first and review `git diff` afterwards. This exception does not cover structural migrations. Direct command selection does not waive the written-plan requirement.

File count, multiple sessions, an existing spec/PRD/TDD, risk, auditability, drift concerns or resume alone never select level 4. A twelve-file feature across several sessions still uses level 3 without a concrete MDTM machinery need. Inspection breadth is not mutation breadth: reading thirty files for an explanation or report does not require an implementation plan.

When an adequate approved plan already exists, use its existing executor directly; do not rebuild it. Managed workflow packages use `/sc:implement`; existing MDTM execution uses `/task`. Explicit `/sc:implement` selection retains that executor's own semantics, not MDTM checklist/phase execution, even if the source resembles MDTM.

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
