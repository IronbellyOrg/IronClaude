# Feature Characterization — Persona Auto-Activation List

**Task:** T02.03 — Characterize MCP declarations, persona activation, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-006
**Donor Catalog Anchor:** D03 (Frontmatter — `personas` auto-activation list) — see `donor-feature-catalog.md` line 49
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` (canonical) — byte-identical to `.claude/commands/sc/task.md`
**Generated:** 2026-05-15

---

## 1. What It Is

A **flat, frontmatter-declared list of 10 persona slugs** advertised by the `/sc:task` command as eligible for *auto-activation* during command execution: `architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer`. The list itself is the entire feature — there is no inline scoring function, no per-tier persona mapping, no activation-condition table embedded in the command file. The list serves as input to whatever persona auto-activation layer the broader Claude Code / SuperClaude framework exposes outside the command file.

Conceptually, it is a **capability advertisement** of the form "any of these 10 personas may be auto-activated when running `/sc:task`," with the activation logic itself living *external* to the command.

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Mechanism (declarative-only, command-frontmatter):**

The list lives at exactly one location: `src/superclaude/commands/task.md:8` (`src/`):

```
personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]
```

- **Entry condition:** Command-loader frontmatter parse — when Claude Code loads `~/.claude/commands/sc/task.md` (or `src/superclaude/commands/task.md`), the frontmatter is parsed, and the `personas:` array becomes part of the command's metadata.
- **Mechanism:** Static metadata — the array is consumed by *whatever* persona auto-activation logic the Claude Code framework provides. The command file does NOT contain the activation algorithm; it only contains the *eligibility list*. The actual activation rules (which prompt keywords map to which persona, what confidence threshold triggers an auto-activation, what the observable effect is) live in framework docs (e.g. the SuperClaude global CLAUDE.md persona table) outside this command.
- **Exit condition:** The list is held as command-metadata for the lifetime of the session. There is no per-invocation activation trace emitted; the user does not see "auto-activated `security` persona" output anywhere in the command's defined output.

**Auxiliary references:**
- The protocol skill (`src/superclaude/skills/sc-task-protocol/SKILL.md`, `src/`) has **no `personas:` slot** in its own frontmatter (`src/superclaude/skills/sc-task-protocol/SKILL.md:1-4`, `src/`) — only `name, description, allowed-tools`. Persona advertisement is a **command-layer concern only** in the donor surface.
- The user's global CLAUDE.md persona table (referenced in session context) defines what each persona slug *means* (e.g. `security → vulnerabilities, auth → Sequential MCP`) — but that table is not in this repo; the command's list is a pointer into that external taxonomy.
- The 10 personas selected here overlap *partly* with the standard SuperClaude persona roster — the donor list includes both the framework's canonical personas (`architect, analyzer, qa, refactorer, frontend, backend, security, devops`) and two role-tagged subagent types (`python-expert, quality-engineer`) that resemble agent names rather than personas.

## 3. What It Produces

- A **registered metadata entry** for the command, listing 10 persona slugs.
- An **eligibility set** consumed by the external persona auto-activation layer when it decides whether to activate one of these personas for the current `/sc:task` turn.
- **No file output, no header emission, no terminal text** — the list is invisible to the user unless they inspect the command file directly.

Critically, there is no observable runtime artifact tied to the list. If `security` is auto-activated for a STRICT auth task, nothing in the command's output sequence indicates that activation happened (contrast with the classification header D08, which *does* emit a visible sentinel).

## 4. What Invokes It

- **Primary invoker:** The Claude Code persona auto-activation layer — an external framework component that reads the command's `personas:` list at invocation time and matches it against the user's prompt to decide which (if any) persona to activate. The location of this layer is **not in this repo** — it lives in the Claude Code core, the SuperClaude installer's hook layer, or an upstream agent-routing component.
- **No internal invoker:** The command file itself does not reference its own `personas:` list anywhere — `grep -n "personas" src/superclaude/commands/task.md` returns only line 8 (the declaration site). No downstream branching reads the list to make decisions; no skill consumes it.
- **The skill side does not invoke it:** The `sc:task-protocol` skill has its own frontmatter without a personas slot, and no body text references the command's persona list.

## 5. What It Depends On

- **The Claude Code persona auto-activation layer** — a framework component that recognizes the `personas:` frontmatter key, reads the array, and applies an activation algorithm. If this component does not exist or does not recognize the key, the list is inert.
- **A persona taxonomy that defines what each slug means** — the user's global CLAUDE.md (or equivalent) maps slugs like `architect` and `security` to (a) trigger conditions (keywords, file paths), (b) primary MCP servers, (c) behavior tweaks. Without that taxonomy, a slug like `python-expert` is uninterpretable. The list trusts an external definition.
- **An override mechanism (`--persona-X` flag)** — referenced indirectly by the user's global rules ("auto-activated by context; override with `--persona-X`") but **NOT declared in the donor command file's flag set** at `src/superclaude/commands/task.md:44-48` (`src/`). The override path is implicit, not specified by `/sc:task`.
- **The absence of an explicit prohibition** in `/task`'s rules — relevant to coupling-cost reasoning: `/task`'s Critical Rule 12 at `src/superclaude/skills/task/SKILL.md:349` (`src/`) prohibits delegating the F1 loop to subagents, which implicitly constrains how persona-activation could attach.

## 6. Standalone Value Claim

**Claim:** The persona auto-activation list provides one main value: **context-sensitive default capability injection** without requiring the user to specify a persona explicitly. A user typing `/sc:task "fix sql injection in login flow"` benefits from the `security` persona auto-activating (which brings Sequential MCP as primary, a security-focused review stance, and stricter assumptions) without having to type `--persona-security`. For a 10-persona surface, the auto-activation amortizes the user's mental load: they describe the work, the framework chooses the persona.

For a heterogeneous workflow that touches frontend, backend, security, and devops in different turns, this is the difference between (a) the user manually selecting a persona each time and (b) the persona being chosen by the framework based on the prompt's keywords/paths.

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under these specific conditions:

- **The activation layer is undocumented and unverifiable from the command file alone.** Reading `src/superclaude/commands/task.md` in isolation gives the reader a list of 10 slugs and no information on (a) the trigger conditions that map prompt-text to a slug, (b) the threshold, (c) the observable effect, (d) the override path. Without inspecting the framework's persona table externally, the list is opaque. A reviewer who only has access to this repo cannot answer "what does adding `python-expert` to this list cause to happen?"
- **No observability for auto-activations.** Even if activation works, there is no header, log line, or sentinel in the command's defined output that says "auto-activated persona X with confidence Y." Contrast with D08's classification header — which makes tier choice auditable. Persona activation is invisible; the user cannot tell whether the framework chose `backend` or `frontend` for their prompt, nor can downstream telemetry measure persona-mix.
- **Persona-tier interaction is unspecified.** The list at line 8 is tier-agnostic — but classification (D09) produces a tier per invocation. Does STRICT prefer `security` over `python-expert`? Does EXEMPT skip persona activation entirely? The command file does not say. The 10-persona list and the 4-tier classification coexist without an interaction rule.
- **Two of the ten slugs are subagent types, not personas.** `python-expert` and `quality-engineer` are listed in the user's `~/.claude/agents/` directory as *agent definitions*, not in the persona table. The auto-activation layer must either (a) interpret them as personas (semantic stretch), (b) interpret them as agent-spawn hints (different mechanism), or (c) silently skip them. The value of having them in the list depends on a disambiguation rule that does not exist.

## 7. Coupling Cost Claim

**Claim:** Attaching the persona auto-activation list to `/task` requires the recipient to take on **all four** of the following concrete burdens — and at least one of them is *structurally prohibited* by `/task`'s F1 loop integrity rules:

1. **A new frontmatter slot in the `/task` skill.** `/task`'s SKILL.md frontmatter at `src/superclaude/skills/task/SKILL.md:1-4` (`src/`) contains only `name` and `description`. Adding a `personas:` array requires extending the skill-frontmatter convention and verifying that the Skill loader (distinct from the Command loader) honors the key — the donor lives in a Command file at `src/superclaude/commands/task.md`, not in a Skill, so direct frontmatter copy may not have equivalent semantics.

2. **A persona-activation layer that operates on a task-file input rather than a prompt-text input.** The donor's auto-activation reads the user's prompt to decide which persona to activate. `/task`'s input is a *task file path*, not a free-text prompt. The recipient must either (a) parse the task file's body text for keywords (a new responsibility for the skill, and one that conflicts with F2 "Working from memory" because the activation would happen pre-loop on a not-yet-fully-read file), (b) infer persona from the task file's frontmatter (requires extending frontmatter schema to include a persona hint), or (c) skip auto-activation entirely on `/task` (defeats the donor's value).

3. **A persona-vs-subagent disambiguation.** `/task`'s subagent dispatcher at `src/superclaude/skills/task/SKILL.md:291-299` (`src/`) lists agent types (`general-purpose, rf-analyst, rf-qa, rf-qa-qualitative, rf-assembler, rf-task-builder, rf-task-researcher, Explore`). The donor's list mixes personas (`security, frontend, backend`) with agent-style names (`python-expert, quality-engineer`). The recipient must commit to a rule resolving "is `python-expert` a persona-flavored behavior or a subagent to spawn?" — neither the donor's list nor `/task`'s dispatcher answers this.

4. **A Critical Rule 12 violation risk.** `/task`'s Critical Rule 12 at `src/superclaude/skills/task/SKILL.md:349` (`src/`) prohibits delegating the F1 loop itself to a subagent. Auto-activation of `quality-engineer` or `python-expert` — both of which exist as subagent types in `~/.claude/agents/` — risks the framework interpreting "activate `python-expert` for this whole task" as a loop-delegation. The recipient must either (a) carve out an exception explicit-enough that auto-activation cannot triangulate into loop-delegation, or (b) restrict auto-activation to per-item scope (every spawned subagent already has an `agent_type` decision — auto-activation would attach there). Either way, the recipient must extend its prohibition rules to accommodate auto-activation safely.

**Net coupling cost:** the recipient must extend its frontmatter convention (1), invent or skip an activation layer for non-prompt input (2), disambiguate persona-vs-subagent semantics (3), and harden F1 loop integrity rules to prevent persona-activation from triggering loop-delegation (4) — four distinct extensions, one of which directly touches the recipient's most-protected integrity rule (Critical Rule 12).

---

## Cross-Reference

- D03 in `donor-feature-catalog.md` (Frontmatter `personas` auto-activation list) — primary anchor.
- D02 in `donor-feature-catalog.md` (Frontmatter `mcp-servers`) — parallel-shape frontmatter declaration; see `feature-mcp-declarations.md`.
- D01 in `donor-feature-catalog.md` (Frontmatter `allowed-tools`) — parallel-shape frontmatter declaration; see `feature-allowed-tools.md`.
- Recipient extension point row 15 (Subagent dispatcher — type selection, `src/superclaude/skills/task/SKILL.md:291-299`, `src/`) — relevant to coupling cost #3 (persona-vs-subagent disambiguation).
- Recipient negative-space row N3 (F1 loop non-delegable, `src/superclaude/skills/task/SKILL.md:349`, `src/`) — directly relevant to coupling cost #4 (Critical Rule 12 violation risk).
