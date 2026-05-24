# Feature Characterization — MCP Server Declarations

**Task:** T02.03 — Characterize MCP declarations, persona activation, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-006
**Donor Catalog Anchors:** D02 (Frontmatter `mcp-servers`) and D27 (MCP Integration — required servers by tier + circuit breaker) — see `donor-feature-catalog.md` lines 48, 78
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` (canonical) — byte-identical to `.claude/` mirrors
**Generated:** 2026-05-15

---

## 1. What It Is

A **two-layer MCP server declaration model** consisting of:

- **Layer A (declarative, command-frontmatter):** A static list `[sequential, context7, serena, playwright, magic, morphllm]` declared in the `/sc:task` command frontmatter, advertising the command's intended MCP surface to the Claude Code command loader at parse time.
- **Layer B (tier-conditioned, runtime):** A per-tier required-server matrix plus a circuit-breaker rule that hard-blocks STRICT execution when required servers are unavailable and permits graceful degradation for STANDARD/LIGHT/EXEMPT.

The two layers are **independently shaped** — Layer A is a flat advertisement read once at command-load time; Layer B is a runtime gate that consumes the tier classification (feature D09) and either proceeds, falls back, or blocks. Layer B is *not* a refinement of Layer A — the two lists do not match (Layer A lists six servers; Layer B's STRICT row names only Sequential and Serena).

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Layer A — Frontmatter advertisement (`src/superclaude/commands/task.md:7`, `src/`):**

```
mcp-servers: [sequential, context7, serena, playwright, magic, morphllm]
```

- **Entry condition:** The Claude Code command loader parses the command's frontmatter at registration time (when the command is loaded into `~/.claude/commands/sc/task.md`).
- **Mechanism:** Static metadata — the loader reads the list and *makes those servers available* to the command's runtime if they are installed.
- **Exit condition:** The list is held as part of the command's metadata for the lifetime of the session; no further interaction unless the command frontmatter is re-parsed.

**Layer B — Per-tier required-server matrix (`src/superclaude/skills/sc-task-protocol/SKILL.md:253-263`, `src/`):**

```
Required Servers by Tier:
- STRICT: Sequential, Serena (fallback not allowed)
- STANDARD: Sequential, Context7 (fallback allowed)
- LIGHT: None required (fallback allowed)
- EXEMPT: None required

Circuit Breaker Behavior:
- If required servers unavailable for STRICT tier, block task execution
- For other tiers, use fallbacks with noted limitations
```

- **Entry condition:** The `sc:task-protocol` skill has been invoked (i.e. dispatch went to STANDARD or STRICT — see feature D10 and `src/superclaude/commands/task.md:99-100`, `src/`). The tier value from the classification header is in scope.
- **Mechanism:** For the current tier, check whether the named required servers are reachable. If STRICT and any of `{Sequential, Serena}` are down, **block** (refuse to execute). If STANDARD and `{Sequential, Context7}` are partially down, **degrade** (continue with documented limitations). LIGHT/EXEMPT have no MCP requirement so the check is vacuous.
- **Exit condition:** Either (a) all required servers reachable → execution proceeds, (b) STRICT with missing required server → execution halts, (c) STANDARD/LIGHT/EXEMPT with degradation → execution proceeds under fallback.

**Auxiliary references:**
- The `sc:task-protocol` skill carries its own `allowed-tools` slot at `src/superclaude/skills/sc-task-protocol/SKILL.md:4` (`src/`) — `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task` — which does **not** match Layer A's `mcp-servers` list (these are tool names, not MCP server names; the two surfaces are different namespaces).
- Layer B's enumerated servers (`Sequential, Context7, Serena`) is a **subset** of Layer A's six-server list; the remaining three (`playwright, magic, morphllm`) appear in Layer A but never in Layer B's tier requirements — they are advertised but tier-unbound.

## 3. What It Produces

**Layer A produces:**
- A registered metadata entry for the command in the command loader's index, listing six MCP server names.
- An invariant available to upstream tooling (e.g. command browsers, docs generators) that introspects the frontmatter.

**Layer B produces:**
- A **boolean gate decision** consumed at execution entry: `proceed` | `degrade` | `block`.
- Implicit documentation: "what does this tier need" is answered by reading the matrix.

Neither layer produces a structured artifact on disk. Both layers' outputs are consumed in-process by the command/skill runtime.

## 4. What Invokes It

- **Layer A:** Invoked by the Claude Code command loader when the `/sc:task` command is registered. No user action triggers it directly; it is parsed once per session-load.
- **Layer B:** Invoked at the start of `sc:task-protocol` skill execution, after the tier is known. Specifically, by whatever logic in the skill's behavioral flow reaches `## MCP Integration` (`src/superclaude/skills/sc-task-protocol/SKILL.md:253`, `src/`) — note that the section is **descriptive prose**, not procedural code, so "invokes" here means "the LLM is expected to honor the matrix during the skill's execution span."

## 5. What It Depends On

- **Layer A** depends on: the Claude Code command-loader convention that recognizes `mcp-servers:` as a frontmatter key (an upstream contract, not declared in this repo). If the loader does not recognize the key, the declaration is inert.
- **Layer A** depends on: the actual installation of the six servers — `[sequential, context7, serena, playwright, magic, morphllm]`. If a server is named but not installed, the declaration advertises a non-existent capability.
- **Layer B** depends on: the tier classification (feature D09) having produced a tier label before this gate runs. If the tier is unknown or invalid, the matrix has no row to look up.
- **Layer B** depends on: a runtime ability to test server availability. The skill text does **not** specify *how* availability is checked — there is no Bash command, no probe sequence, no health-endpoint URL. The check is left to the LLM's discretion.
- **Layer B** depends on: an enforcement mechanism for the "block" outcome. The skill prose says "block task execution" but does not name the mechanism (no early `return`, no error sentinel) — enforcement is again LLM-discretionary.
- **Both layers** depend on: the absence of any contradiction-resolution rule when Layer A advertises servers that Layer B never requires (e.g. `playwright, magic, morphllm`). The two layers coexist by convention, not by spec.

## 6. Standalone Value Claim

**Claim:** The MCP server declaration model provides two distinct values:

1. **Layer A (advertisement) value:** Upstream tooling and human readers can answer "what MCP capability does this command expect?" by reading a single frontmatter line. This is a low-effort capability-discovery surface — useful for docs generation, capability auditing, and onboarding.
2. **Layer B (tier-conditioned gate) value:** A safety contract — STRICT tasks (security, auth, migrations) cannot execute if the high-reasoning + persistent-memory servers (Sequential, Serena) are down. The circuit breaker is the only mechanism in the `/sc:task` surface that ties MCP health to tier semantics: a STRICT change to a `crypto/` path will refuse to run on a degraded environment rather than silently producing lower-quality output. For a team that operates STRICT-tier work in a MCP-dependent workflow, this prevents the failure mode where "the agent worked but didn't have its critical reasoning server" goes unnoticed.

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under these specific conditions:

- **Layer A is dead metadata when downstream tooling ignores it.** No file in this repo reads the `mcp-servers:` frontmatter list — `grep -r "mcp-servers" src/superclaude/` finds only the declaration site, not a consumer. Until a consumer exists (a capability-discovery tool, a docs generator, a CI check), Layer A is a write-only annotation. The advertisement *adds zero behavior* — it is human-readable documentation pretending to be structured metadata.
- **Layer B is non-load-bearing in environments where the named servers are not installed by default.** If `Sequential` and `Serena` are not part of the user's MCP install (e.g. a developer running base Claude Code without the airis-mcp-gateway), the STRICT-tier block fires immediately and the user must either install the servers or override to a lower tier — at which point the gate has prevented *all* STRICT execution rather than catching genuine outages. The "circuit breaker" doubles as a "hard prerequisite" without distinguishing the two cases.
- **Layer B specifies behavior without enforcement.** The text "block task execution" has no implementation in this repo (no test, no runtime check, no error pathway). An LLM reading the skill prose at execution time is the only enforcement mechanism, and an LLM that decides "this server seems fine even though I can't reach it" silently violates the contract. The value is realized only as far as the LLM's self-discipline carries it.
- **The two layers are inconsistent.** Layer A advertises `playwright, magic, morphllm` but Layer B's tier matrix names none of them; conversely Layer B names `Context7` for STANDARD but Layer A includes `context7`. A reader trying to reconcile the lists has no rule that resolves the mismatch — value falls away the moment a user asks "so does STANDARD need Context7 or not?"

## 7. Coupling Cost Claim

**Claim:** Attaching the MCP declaration model to `/task` requires the recipient to take on **all five** of the following concrete burdens:

1. **A new frontmatter slot in the `/task` skill.** `/task`'s SKILL.md frontmatter at `src/superclaude/skills/task/SKILL.md:1-4` (`src/`) contains only `name` and `description` — there is **no `mcp-servers` slot**. Adding Layer A requires extending the skill-frontmatter convention. Because `/task` is registered as a Skill (not a Command), it is not clear whether the Claude Code Skill loader recognizes `mcp-servers:` the same way the Command loader does — the recipient must verify or invent this contract.

2. **A tier-source data path before the gate can run.** Layer B branches on tier. `/task` does not produce or consume a tier value today (confirmed by `feature-tier-classification.md` coupling cost #2 and by the recipient extension points file: row 13 lists the required frontmatter slots as `id, title, status, created_date`, no `Tier:`). To run Layer B, `/task` must first acquire a tier — either by extending the schema, or by inheriting from upstream (`task-builder` or `sc:tasklist`), or by running a classifier inside the skill. Each is a non-trivial extension.

3. **A runtime MCP-availability probe.** The donor skill prose names what to require but not how to test. The recipient must define a probe (Bash health check? Tool-call rejection? A pre-flight Skill invocation?) and a deadline. `/task`'s Task File Validation gate at `src/superclaude/skills/task/SKILL.md:64-73` (`src/`) is the structural attach point for a pre-loop probe, but currently performs only file/schema checks — adding network/MCP checks broadens its responsibility.

4. **A block-vs-degrade decision and an enforcement mechanism.** "Block STRICT" implies the F1 loop must refuse to enter when prerequisites fail. `/task`'s Error Handling at `src/superclaude/skills/task/SKILL.md:170-179` (`src/`) currently handles per-item failures by logging blockers and continuing; it has no concept of "refuse to enter the loop." Adding a hard block requires either a pre-loop early-exit (extending the validation gate's outcomes) or a per-item gate that fails-closed on every STRICT item (changing per-item semantics). The recipient must commit to one.

5. **Per-tier MCP requirements have to live somewhere on the `/task` side.** The donor's table at `src/superclaude/skills/sc-task-protocol/SKILL.md:255-259` (`src/`) is hard-coded prose. `/task` has no externalized YAML pattern (see D32 in donor catalog — `config/verification-routing.yaml` is *referenced* but does not exist). The recipient must decide: inline the matrix in `/task`'s SKILL.md (couples MCP policy to skill content), extract to a YAML file (introduces a config-loading dependency the skill currently lacks), or move to a sibling skill (creates a new cross-skill data-flow contract). None match `/task`'s current shape.

**Net coupling cost:** the recipient must extend its frontmatter convention (1), introduce a tier-source data path (2), implement a runtime probe (3), invent a block enforcement mechanism (4), and decide where the per-tier matrix lives (5) — five distinct extensions, plus all the upstream tier-classification dependencies.

---

## Cross-Reference

- D02 in `donor-feature-catalog.md` (Frontmatter `mcp-servers`) — primary anchor for Layer A.
- D27 in `donor-feature-catalog.md` (MCP Integration + Circuit Breaker) — primary anchor for Layer B.
- D09 in `donor-feature-catalog.md` (tier classification model) — upstream producer of the tier value Layer B consumes; see `feature-tier-classification.md`.
- D32 in `donor-feature-catalog.md` (External configuration references) — relevant to coupling cost #5 (externalize-to-YAML alternative).
- Recipient extension point row 1 (Task File Validation gate, `src/superclaude/skills/task/SKILL.md:64-73`, `src/`) — structural attach point for any pre-loop MCP probe.
- Recipient extension point row 13 (Required frontmatter schema slot, `src/superclaude/skills/task/SKILL.md:69`, `src/`) — slot for adding a `Tier:` field that Layer B would branch on.
