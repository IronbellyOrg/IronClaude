# Feature Characterization — Declared `allowed-tools` Frontmatter

**Task:** T02.03 — Characterize MCP declarations, persona activation, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-006
**Donor Catalog Anchor:** D01 (Frontmatter — declared `allowed-tools`) — see `donor-feature-catalog.md` line 47
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` (canonical) — byte-identical to `.claude/commands/sc/task.md`
**Generated:** 2026-05-15

---

## 1. What It Is

A **declarative tool-surface gate** in the `/sc:task` command's frontmatter, restricting the set of tools the LLM may invoke while running the command to exactly: `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`. Nine tools, comma-separated, on a single frontmatter line. The list excludes (notably): `WebFetch, WebSearch, NotebookEdit`, the MCP-tool namespace (`mcp__*`), `EnterPlanMode/ExitPlanMode`, and the Monitor/CronCreate/PushNotification family.

It is a **negative-space allowlist** — anything not on the list is implicitly denied. The gate is enforced by Claude Code's command loader before any of the listed tools is dispatched, not by prose discipline inside the command body.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Mechanism (declarative, command-frontmatter, loader-enforced):**

The list lives at exactly one location: `src/superclaude/commands/task.md:6` (`src/`):

```
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
```

- **Entry condition:** Claude Code command loader parses the command's frontmatter when the command is registered. The `allowed-tools:` value becomes part of the command's metadata, scoped to the command's invocation span.
- **Mechanism:** When the LLM, while inside a `/sc:task` turn, attempts a tool call, the framework checks the tool's name against the allowlist. Tools on the list are dispatched normally; tools not on the list are *blocked at the framework boundary* (the LLM may attempt the call, but it is rejected before execution).
- **Exit condition:** The allowlist is in effect for the duration of the `/sc:task` turn. When the turn ends — or when the command dispatches into the `sc:task-protocol` skill (D10) — the *skill's* own `allowed-tools` slot at `src/superclaude/skills/sc-task-protocol/SKILL.md:4` (`src/`) takes over: `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task` — note the skill list is **almost identical** to the command list but **omits `Skill`** (the skill itself cannot dispatch into another skill).

**Auxiliary references:**
- The `sc:task-protocol` skill's frontmatter at `src/superclaude/skills/sc-task-protocol/SKILL.md:4` (`src/`) carries an analogous slot, suggesting the convention is honored on both Command and Skill loaders. The two lists differ by one tool (`Skill` is command-only).
- The donor catalog (T01.03 audit, see `donor-feature-catalog.md` line 47, D01) verified that the `/task` skill frontmatter at `src/superclaude/skills/task/SKILL.md:1-4` (`src/`) has **no `allowed-tools` slot** — the recipient's analogous mechanism is the prose Critical Rule 6 at `src/superclaude/skills/task/SKILL.md:337` (`src/`), which is a *runtime tool-selection prescription* (positive: "use Glob/Grep/Read/codebase-retrieval"; negative: "do NOT use bash find/grep/cat/head/tail/rg/awk"), not a declarative gate.

## 3. What It Produces

- A **registered allowlist** in the command-loader's metadata, consumed by the framework at every tool-dispatch boundary.
- A **runtime denial decision** (allow vs deny) for each LLM tool-call attempt during the command's turn. The denial is implicit (not surfaced as visible output unless the framework emits an error).
- **No file output, no header emission, no terminal text** under normal operation. The list's effect is felt only in the *absence* of certain tool calls.

## 4. What Invokes It

- **Primary:** The Claude Code command-execution dispatcher — for every tool the LLM requests during a `/sc:task` turn, the dispatcher queries the command's frontmatter allowlist before granting permission.
- **No internal invoker:** The command body does not reference its own `allowed-tools` — `grep -n "allowed-tools" src/superclaude/commands/task.md` returns only line 6 (the declaration site). The list is consumed externally by the framework.
- **The skill side has its own gate:** Once `Skill sc:task-protocol` is invoked (`src/superclaude/commands/task.md:100`, `src/`), the skill's allowlist takes over for the skill's execution span — see `src/superclaude/skills/sc-task-protocol/SKILL.md:4` (`src/`).

## 5. What It Depends On

- **The Claude Code command-loader convention** that recognizes `allowed-tools:` as a frontmatter key with deny-by-default semantics. If the loader does not recognize the key, the gate is inert and all tools are implicitly available.
- **Tool name stability** — the listed names (`Read, Glob, Grep, ...`) must match the framework's tool registry exactly. If a tool is renamed upstream (e.g., `Read` → `ReadFile`), the allowlist silently invalidates the old entry.
- **Consistency between command-side and skill-side allowlists** — the command lists `Skill` but the skill (`sc:task-protocol`) does not, by intent (a skill cannot itself dispatch a Skill). However, neither file documents this distinction; the asymmetry is convention, not specification.
- **The absence of overrides** — the framework provides no documented `--allow-tool X` escape hatch on `/sc:task`'s flag set (`src/superclaude/commands/task.md:44-48`, `src/`). If the user needs an excluded tool (e.g., `WebFetch` to look up a library), the command cannot grant it; the user must invoke a different command or skill.

## 6. Standalone Value Claim

**Claim:** The declared `allowed-tools` allowlist provides three distinct values:

1. **Tool-surface predictability.** A reviewer reading the command's frontmatter knows exactly which 9 tools may be dispatched during a `/sc:task` turn. This bounds the command's blast radius — `/sc:task` cannot accidentally invoke `WebFetch` (and exfiltrate data), cannot invoke `NotebookEdit` (and corrupt a notebook), cannot invoke MCP-server tools that haven't been intentionally enabled.
2. **Loader-enforced (not prose-enforced) safety.** Unlike a prose rule like "do not use bash find" (which depends on LLM discipline), a declarative allowlist denies the call at the framework boundary — even if the LLM attempts to call `WebFetch`, the framework refuses. This shifts safety from "the LLM follows instructions" to "the framework rejects the action."
3. **Capability-discovery surface.** Upstream tooling (capability auditors, security reviewers, docs generators) can answer "what can `/sc:task` touch?" by reading a single line. This makes capability inventory mechanical.

For a security-sensitive deployment, the gate is the difference between (a) "I trust the LLM not to call dangerous tools" and (b) "the framework refuses to dispatch dangerous tools regardless of LLM intent."

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under these specific conditions:

- **The allowlist is too permissive to be a meaningful safety boundary.** `Bash` is on the list, and `Bash` can do *anything* the user's shell can do — including the command-shell equivalents of every excluded tool (`curl` substitutes for `WebFetch`, `jupyter nbconvert` for `NotebookEdit`, `mcp_client` calls for the MCP namespace). The gate restricts a few high-level tools but leaves the universal-purpose `Bash` open. For a tightly-scoped command this would be a real safety boundary; for `/sc:task` (which legitimately needs `Bash` to run tests), the allowlist excludes high-level convenience tools but does not actually contain capability.
- **The skill's allowlist subtly weakens the command's.** When the command dispatches into `sc:task-protocol` (STANDARD/STRICT tiers), the skill's allowlist takes over. The skill omits `Skill` (so it cannot dispatch further skills) but otherwise mirrors the command. A reviewer trying to reason about "what tools can fire during a STRICT task?" must reconcile two near-identical allowlists across a Command→Skill boundary, with no documentation of the asymmetry. Predictability is reduced, not increased.
- **No override path is documented.** If a legitimate `/sc:task` invocation needs `WebFetch` (e.g. "fix this bug per the linked GitHub issue"), the user has no flag-level escape hatch (verified: `src/superclaude/commands/task.md:44-48`, `src/`, lists 8 flags, none of them tool-related). The user must abandon `/sc:task` and use a different command — at which point the value of the allowlist flips from safety to friction.
- **The list is opaque about *why* each tool is included.** `TodoWrite` is on the list but the donor file at `src/superclaude/commands/task.md` makes only one indirect reference to it (the `sc:task-protocol` skill's Tool Coordination section at `src/superclaude/skills/sc-task-protocol/SKILL.md:268`, `src/`, lists `TodoWrite` for the Planning phase). A reviewer cannot tell from the allowlist alone whether removing `TodoWrite` would break the command — the dependency is implicit.

## 7. Coupling Cost Claim

**Claim:** Attaching the declared `allowed-tools` mechanism to `/task` requires the recipient to take on **all four** of the following concrete burdens, *one of which is a direct conflict with the recipient's existing analog rule*:

1. **A new frontmatter slot in the `/task` skill, plus loader-recognition verification.** `/task`'s SKILL.md frontmatter at `src/superclaude/skills/task/SKILL.md:1-4` (`src/`) contains only `name` and `description`. Adding `allowed-tools:` requires extending the skill-frontmatter convention. Crucially, because `/task` is a Skill, not a Command, the recipient must verify (or build) Skill-loader recognition of the `allowed-tools` key — the donor lives in a Command file, and the Command-loader and Skill-loader semantics are not documented as identical in this repo. If only the Command loader honors the key, the recipient gains a frontmatter line that does nothing.

2. **Resolution of the conflict with Critical Rule 6.** `/task`'s Critical Rule 6 at `src/superclaude/skills/task/SKILL.md:337` (`src/`) is the recipient's existing tool-selection rule, but it is *prescriptive runtime guidance* (positive: "use Glob/Grep/Read/codebase-retrieval"; negative: "do NOT use bash `find/grep/cat/head/tail/rg/awk`"), not a declarative gate. The donor's mechanism is the inverse shape — declarative-gate-by-allowlist. Adopting the donor without rewriting Critical Rule 6 produces two sources of truth for "what tools may fire," and they would inevitably drift. The recipient must commit to one (rewrite Critical Rule 6 to point at the frontmatter) or accept the duplication risk.

3. **A tool-list calibration step.** The donor's list (`Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`) excludes `WebFetch, WebSearch, NotebookEdit, Monitor, CronCreate, PushNotification, EnterPlanMode/ExitPlanMode, ReadMcpResourceTool, ListMcpResourcesTool` and the entire `mcp__*` namespace. The recipient must decide whether `/task`'s legitimate operating envelope matches this list. `/task` spawns subagents (uses `Task`/`Agent`), reads files extensively (`Read, Glob, Grep`), edits the task file (`Edit`), and runs Bash for tests — so the donor list is mostly compatible. But `/task` does not use `Skill` (it IS a Skill, dispatching deeper Skills is unusual; actually `/task`'s subagent dispatcher at `src/superclaude/skills/task/SKILL.md:291-299` uses Agent, not Skill). The recipient must validate item-by-item.

4. **An override / weakening path for legitimate exceptions.** `/task` items can include heterogeneous actions — a research item may legitimately need `WebFetch`, a documentation item may legitimately need `WebSearch`. Since `/task` is item-driven (not prompt-driven), the per-item action types vary widely. The recipient must either (a) accept that any item needing an excluded tool fails closed, (b) add a per-item "tool-grant" annotation (extends task-file schema), or (c) make the list maximally permissive (which dilutes the safety value back toward zero). The donor offers no guidance because its prompt-driven model has narrower per-turn variance.

**Net coupling cost:** the recipient must extend its frontmatter convention (1), resolve the conflict with Critical Rule 6 (2), recalibrate the tool list against `/task`'s legitimate use (3), and decide on an exception/override path (4) — four distinct extensions, with #2 forcing a *change to one of `/task`'s 14 numbered Critical Rules*, which is a high-cost edit per the recipient's "Critical Rules are inviolable" framing.

---

## Cross-Reference

- D01 in `donor-feature-catalog.md` (Frontmatter `allowed-tools`) — primary anchor.
- D02 in `donor-feature-catalog.md` (Frontmatter `mcp-servers`) — parallel-shape declaration with non-overlapping namespace; see `feature-mcp-declarations.md`.
- D03 in `donor-feature-catalog.md` (Frontmatter `personas`) — parallel-shape declaration; see `feature-persona-activation.md`.
- D28 in `donor-feature-catalog.md` (Tool Coordination by phase) — DUPLICATE-OF-EXISTING; the recipient's analog is the F1 EXECUTE action-to-tool mapping at `src/superclaude/skills/task/SKILL.md:89-96` (`src/`) — relevant context for coupling cost #2.
- Recipient row 13 (Required frontmatter schema slot, `src/superclaude/skills/task/SKILL.md:69`, `src/`) — extension point for adding the `allowed-tools` slot.
- Critical Rule 6 (`src/superclaude/skills/task/SKILL.md:337`, `src/`) — directly conflicts with the donor's declarative-gate model; named explicitly in coupling cost #2.
