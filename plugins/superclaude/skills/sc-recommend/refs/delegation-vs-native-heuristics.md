# Net-Value Rubric — When Delegation Beats Native Tooling

This reference owns the **how** of Phase 1 in SKILL.md. The skill's job is to recommend the smallest delegation that wins; this file explains *smallest* and *wins*.

## The default is native

When no explicit verified command, existing executor or specialized deliverable already decides the route, the default recommendation is "use `Read`, then `Edit`" (or the equivalent bounded native sequence). Preserve the requested outcome and authorization ceiling first. Delegation must **earn** its overhead — spawning a subagent, loading a 500-line skill body, running a multi-phase protocol, or invoking an MCP server are not free. A recommendation engine that delegates reflexively trains users to over-invoke. That is bad for the user and bad for the framework.

If the honest answer to **all** of the following is "yes", recommend native. Do not delegate.

- The task is one source file (plus its test), five edits or fewer, and the exact change is known (level 2 in the routing guide).
- The model can hold the relevant context for the whole task without losing accuracy.
- There is no specialized capability (semantic search across thousands of files, multi-agent debate, structured tasklist generation, browser automation, etc.) that the model genuinely lacks natively.
- The user has not asked for a structured artifact (spec, PRD, TDD, tasklist, roadmap) that a skill is designed to produce.

When even one of those is "no" or "uncertain", delegation may be appropriate — proceed to the rubric below.

## The net-value rubric

Score the candidate delegation across these five axes. The candidate wins only if it scores higher than "native" on the **dominant** axis, *and* does not regress hard on the others.

### 1. Specialized capability

| Capability the candidate provides | Native equivalent | Delegate? |
|---|---|---|
| Multi-agent debate with adversarial scoring (`/sc:adversarial`) | None | YES |
| Roadmap plus one task file per phase (`/roadmap`, then `/task` on each phase's task file; `/task-builder` for any build request it leaves) | Manual structured writing | YES if user wants the artifact |
| Repository-wide semantic ranking | Many Grep/Glob calls | YES (auggie beats brute Grep) |
| Multi-pass cleanup audit with evidence (`/sc:cleanup-audit`) | Manual review | YES if scope > a few files |
| Spec / PRD / TDD generation following project templates | Free-form writing | YES — templates are load-bearing |
| Single-file refactor of a small util, 5 edits or fewer | Read + Edit | NO — native wins |
| Renaming a symbol with 5 or fewer edits in total, in one source file and its test; more needs level 3 | Read + Edit + Grep | NO — native wins |
| Reading a config file and explaining it | Read | NO — native wins, always |
| Adding a print statement | Edit | NO |

### 2. Scope / breadth

- Choose the requested outcome and explicit command/executor before implementation-size heuristics. Reading many files for analysis, explanation, localization or other reports does not require an implementation plan. A specialist operation keeps its documented lifecycle, even when it writes many artifacts.
- For actual implementation, the routing guide's hard limit decides (`~/.claude/HOW-WE-WORK.md`, section 1): more than 5 edits or more than one source file plus its matching test requires a written plan, normally level 3 (`/sc:workflow` then `/sc:implement`). Standard is the ordinary workflow depth; quick is for a smaller checked plan, not a universal requirement.
- Level 4 (`/task-builder` then `/task`) needs explicit MDTM intent or an exceptionally complex, long-running phased program with a stated research/checklist/phase-reviewer machinery need. File count, sessions, an existing spec/PRD/TDD, risk, auditability, drift and resume alone do not justify it. No numerical workflow capacity ceiling is invented.
- Preserve the contained-folder `/sc:cleanup` and `/sc:improve` exception with a checkpoint commit and final `git diff` review; it does not exempt structural migrations. Explicit selection cannot waive the written-plan limit or add authority.
- Existing approved plans go directly to their executor. Workflow packages use implement; existing MDTM execution uses task; explicit implement retains its own semantics. Do not rebuild a plan or treat memory save/load as executor resume.
- Cross-domain static assessment can use `/sc:analyze`; cleanup evidence can use `/sc:cleanup-audit`; concrete broken behavior can use `/sc:troubleshoot`. Distinguish the objective rather than routing every broad request to debugging or implementation. Unknown current behavior may justify `/tech-research`, but a research-only request stops at its report.

### 3. Output structure required

If the user wants a **structured artifact** that follows a project template (PRD, TDD, technical reference, tasklist, roadmap, release spec, MDTM task file), the skill that owns that template almost always wins, because the skill knows the structure and the native path duplicates the template by hand.

If the user wants free-form prose, native usually wins — skills add overhead, not structure, here.

### 4. Token budget vs. value

Skills with large protocol bodies (`/sc:adversarial`, `/sc:roadmap`, `/sc:cleanup-audit`) cost real tokens just to load. For a small task, the loading cost dwarfs the work. Rule of thumb: if the user's task is < ~500 tokens of actual work, do not invoke a skill whose protocol is > ~2000 tokens to load.

### 5. Repeatability and discipline

Even when native would technically work, delegation can win because the skill **enforces discipline** the user has previously asked for: evidence gathering, adversarial validation, audit trails, freshness re-reads. If the user has prior context indicating they want these guarantees (or the work touches CLAUDE.md absolute rules like `make verify-sync`), prefer the skill that bakes them in.

## Commands vs. skills vs. agents — choosing the right tier

The framework's three tiers (commands → skills → agents) have different optimal use cases. Pick the *outermost* tier that fits.

- **Command (`/sc:<name>`)** - the user-facing surface. Prefer its verified interface when delegation wins. It may be self-contained or name a mandatory skill under Activation, Skill Invocation or another heading; read the actual handoff rather than guessing a protocol.
- **Skill directly** — many IronClaude skills have no `/sc:` command and are run by their own slash name (`/task-builder`, `/task`, `/prd`, `/tech-research`, `/roadmap`; `/tdd` also has `/sc:tdd`, which runs the same skill). Recommend them that way whenever the routing guide names them. Otherwise recommend a skill directly (`Skill <name>`) only when the user explicitly wants the skill body's behavior outside a command's flag surface.
- **Agent directly (`Agent <name>`)** — use `Agent <name>` directly only when no routing row or guide section covers the task (search the guide's routing table and sections 3.x first), the work is a single specialist execution, and the broader skill protocol around it would add overhead without value. When a routing row or guide section covers the job, use its command instead (a performance problem is `/sc:troubleshoot "<problem>" --type performance`; a focused web research question is `/sc:research "<question>" --depth deep`; neither is an agent).

**Special case — parallel agent fan-out.** When the user's request is naturally parallel (e.g., "research these 3 files independently and synthesize"), recommend a **single message with multiple `Agent` tool calls** rather than a sequential chain of skill invocations. The parallel fan-out wins on wall-clock and on context isolation; a sequential skill chain would serialize unnecessarily. The prompt should make the parallel structure explicit:

```text
Use the Agent tool to spawn 3 parallel Explore agents in a SINGLE message:
  - Agent 1: <focus + file>
  - Agent 2: <focus + file>
  - Agent 3: <focus + file>
Then synthesize the three returns into <deliverable>.
```

## When the skill should say "use native"

These favor native tooling only when no explicit verified selection or specialized deliverable takes precedence and the direct-change limit permits it. Do not override a requested command or inspection objective:

- Reading a single file and reporting its contents.
- Renaming a variable or symbol with 5 or fewer edits in total, in one source file and its test — `Grep` + `Edit` is faster than any skill. More needs level 3.
- Adding or removing a single line.
- Reformatting a code block.
- Answering a factual question about a known file.
- Writing a 1-3 line shell command (the user can do this themselves; recommending `Bash` is the answer).
- "Refactoring this small util" (one source file, 5 edits or fewer) — unless the util is genuinely tangled, native wins.
- "Fix this typo" — native, always.

When emitting a native recommendation, name the tools and the order, and stop. No prompt block. No flags. The user does not need 200 tokens of meta-explanation to run `Read` and `Edit`.

## Tie-break heuristic

When two delegations both score reasonably well:

1. Prefer the one with the fewer protocol phases (less overhead).
2. Prefer the one with the more recent / better-exercised eval history in this repo (auggie surfaces this in Phase 0).
3. Prefer the entry point the routing guide names for that step (a `/sc:` command, or a skill's own slash name such as `/task-builder`); when the guide names none, prefer the command-level surface (`/sc:<x>`) over invoking a skill or agent directly.

If after tie-breaking there are still two genuinely-different-approach candidates, emit both as multi-path prompts with a one-line disambiguator on each. Do not flatten them into a vague "alternatives" list.
