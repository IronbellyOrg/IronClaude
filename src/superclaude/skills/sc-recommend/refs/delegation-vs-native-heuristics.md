# Net-Value Rubric — When Delegation Beats Native Tooling

This reference owns the **how** of Phase 1 in SKILL.md. The skill's job is to recommend the smallest delegation that wins; this file explains *smallest* and *wins*.

## The default is native

The default recommendation is "use `Read`, then `Edit`" (or the equivalent 2-3 step native sequence). Delegation must **earn** its overhead — spawning a subagent, loading a 500-line skill body, running a multi-phase protocol, or invoking an MCP server are not free. A recommendation engine that delegates reflexively trains users to over-invoke. That is bad for the user and bad for the framework.

If the honest answer to **all** of the following is "yes", recommend native. Do not delegate.

- The task fits in 1-3 file reads and one or two edits.
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
| Roadmap → multi-file tasklist bundle (`/sc:tasklist`) | Manual structured writing | YES if user wants the artifact |
| Repository-wide semantic ranking | Many Grep/Glob calls | YES (auggie/serena beats brute Grep) |
| Multi-pass cleanup audit with evidence (`/sc:cleanup-audit`) | Manual review | YES if scope > a few files |
| Spec / PRD / TDD generation following project templates | Free-form writing | YES — templates are load-bearing |
| Single-file refactor of a small util | Read + Edit | NO — native wins |
| Renaming a symbol with a handful of references | Read + Edit + Grep | NO — native wins |
| Reading a config file and explaining it | Read | NO — native wins, always |
| Adding a print statement | Edit | NO |

### 2. Scope / breadth

- Scope ≤ 3 files, single-domain: native almost always wins.
- Scope = whole subsystem (5-20 files), single-domain: skill may win if the skill is purpose-built (e.g., `tech-research` for codebase research).
- Scope = whole repo or cross-domain (security + perf + arch + maintainability): delegation almost always wins (`/sc:cleanup-audit`, `/sc:troubleshoot` Tier 2+).

### 3. Output structure required

If the user wants a **structured artifact** that follows a project template (PRD, TDD, technical reference, tasklist, roadmap, release spec, MDTM task file), the skill that owns that template almost always wins, because the skill knows the structure and the native path duplicates the template by hand.

If the user wants free-form prose, native usually wins — skills add overhead, not structure, here.

### 4. Token budget vs. value

Skills with large protocol bodies (`/sc:adversarial`, `/sc:roadmap`, `/sc:cleanup-audit`) cost real tokens just to load. For a small task, the loading cost dwarfs the work. Rule of thumb: if the user's task is < ~500 tokens of actual work, do not invoke a skill whose protocol is > ~2000 tokens to load.

### 5. Repeatability and discipline

Even when native would technically work, delegation can win because the skill **enforces discipline** the user has previously asked for: evidence gathering, adversarial validation, audit trails, freshness re-reads. If the user has prior context indicating they want these guarantees (or the work touches CLAUDE.md absolute rules like `make verify-sync`), prefer the skill that bakes them in.

## Commands vs. skills vs. agents — choosing the right tier

The framework's three tiers (commands → skills → agents) have different optimal use cases. Pick the *outermost* tier that fits.

- **Command (`/sc:<name>`)** — the user-facing surface. Almost always the right thing to recommend when delegation wins. The command's `## Activation` handoff loads the skill automatically.
- **Skill directly (`Skill <name>`)** — recommend only when there is no command in front of the skill (rare in this project — most skills have a command), or when the user explicitly wants the skill body's behavior outside the command's flag surface.
- **Agent directly (`Agent <name>`)** — recommend when the work is a single specialist execution (e.g., a single `Agent deep-research` call for a focused research question) and the broader skill protocol around it would add overhead without value.

**Special case — parallel agent fan-out.** When the user's request is naturally parallel (e.g., "research these 3 files independently and synthesize"), recommend a **single message with multiple `Agent` tool calls** rather than a sequential chain of skill invocations. The parallel fan-out wins on wall-clock and on context isolation; a sequential skill chain would serialize unnecessarily. The prompt should make the parallel structure explicit:

```text
Use the Agent tool to spawn 3 parallel Explore agents in a SINGLE message:
  - Agent 1: <focus + file>
  - Agent 2: <focus + file>
  - Agent 3: <focus + file>
Then synthesize the three returns into <deliverable>.
```

## When the skill should say "use native"

These are the cases where the recommendation must be native tooling, no delegation:

- Reading a single file and reporting its contents.
- Renaming a variable or symbol with < 10 references — `Grep` + `Edit` is faster than any skill.
- Adding or removing a single line.
- Reformatting a code block.
- Answering a factual question about a known file.
- Writing a 1-3 line shell command (the user can do this themselves; recommending `Bash` is the answer).
- "Refactoring this small util" — unless the util is genuinely tangled, native wins.
- "Fix this typo" — native, always.

When emitting a native recommendation, name the tools and the order, and stop. No prompt block. No flags. The user does not need 200 tokens of meta-explanation to run `Read` and `Edit`.

## Tie-break heuristic

When two delegations both score reasonably well:

1. Prefer the one with the fewer protocol phases (less overhead).
2. Prefer the one with the more recent / better-exercised eval history in this repo (auggie surfaces this in Phase 0).
3. Prefer the command-level surface (`/sc:<x>`) over invoking a skill or agent directly — commands are the documented entry point.

If after tie-breaking there are still two genuinely-different-approach candidates, emit both as multi-path prompts with a one-line disambiguator on each. Do not flatten them into a vague "alternatives" list.
