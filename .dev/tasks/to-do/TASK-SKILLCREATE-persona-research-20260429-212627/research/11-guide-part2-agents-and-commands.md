# Guide Partition Analysis — Agents and Commands

**Investigation type:** Guide Partition Analysis — Agents and Commands
**Scope:** /config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, lines 1045-2088
**Status:** Complete
**Date:** 2026-04-29

---

## Scope Note and Vocabulary Mismatch

The investigation prompt directed me to extract conventions for `agent_name` format, `agent_role` line format, `parent_skill` linkage, and `agent_family` classification. **None of these field names appear in the guide.** The guide consistently uses YAML frontmatter fields named `name`, `description`, and `category` (lines 385-388, 2010-2013). It does NOT define a `parent_skill` linkage field or an `agent_family` taxonomy field.

Additionally, the prompt asks about an `rf-` prefix rule for agent names. **The guide does not document an `rf-` prefix.** It only documents an `sc-` prefix and only for SKILLS, not agents (Glossary, line 2081: "**sc- prefix** | Skill prefix indicating it backs a `/sc:` command"). All example agents in the guide use plain bare names (`summary-reporter`, `debate-orchestrator`, `merge-executor`, `pm-agent`, `deep-research-agent`).

I report below what the guide *actually* contains, mapping the prompt's intent (agent identity, role specification, skill linkage, classification) onto the fields the guide actually defines. Any prompt term unsupported by the guide is marked **[NOT IN GUIDE]**.

The bulk of the assigned line range (1045-2088) consists of Best Practices (§9), Complete Examples (§10), and Appendices A-E. Section §9 contains the design rules and anti-patterns; the templates in Appendices B and C are the canonical structures for commands and agents. I cross-referenced lines 380-460 (Part 1's scope, but unavoidable for agent-frontmatter authority) for completeness, marked clearly.

---

## Agent Authoring Conventions

| Convention | Where in guide | Applies to which agent file element |
|---|---|---|
| Required frontmatter field `name: <agent-name>` (identifier, used in `@agent-<name>` references) | line 385 (Part 1, cross-ref) | YAML frontmatter, agent identity |
| Required frontmatter field `description: <one-line description>` | lines 386, 2011 | YAML frontmatter, summary |
| Required frontmatter field `category: <category>` (functional grouping: analysis, meta, utility, etc.) | lines 387, 2012 | YAML frontmatter, classification |
| Optional frontmatter `tools: [Read, Write, Glob]` (explicit tool allowlist) | line 394 | YAML frontmatter, tool restriction |
| Optional frontmatter `model: opus` (model preference) | line 395 | YAML frontmatter, model selection |
| Optional frontmatter `maxTurns: 10` and `permissionMode: restricted` | lines 396-397 | YAML frontmatter, agent constraints |
| Required body section `# <Agent Title>` (human-readable) | lines 404, 2015 | First H1 heading |
| Required body section `## Triggers` — when the agent activates | lines 405, 2017-2019 | Activation conditions list |
| Required body section `## Behavioral Mindset` — 1-3 sentences describing role, philosophy, constraints | lines 406, 1096, 2021-2022 | Behavioral framing |
| Recommended body section `## Model Preference` with rationale | lines 407, 2024-2025 | Model rationale |
| Recommended body section `## Tools` — list with WHY each tool is needed | lines 408, 1097, 2027-2028 | Tool justification |
| Required body section `## Responsibilities` (numbered list) | lines 409, 2030-2032 | Numbered duties |
| Required body section `## Outputs` — concrete artifact names and formats | lines 411, 1099, 2034-2036 | Output declaration |
| Required body section `## Does NOT` — explicit negative constraints | lines 412, 1098, 2038-2040 | Negative constraints |
| Required body section `## Boundaries` with `**Will:**` and `**Will Not:**` lists | lines 413, 2042-2048 | Will / Will Not boundaries |
| Behavioral Mindset should explain the WHY (philosophy), not just WHAT | line 1170 | `## Behavioral Mindset` content |
| Single, well-defined responsibility — focused agents | line 1160 | Overall agent scope |
| Constrained Worker pattern: small tool set, 40-60 lines, receives plan from orchestrator | lines 419-425 | Pattern 1 sizing |
| Specialist Investigator pattern: read-heavy, 80-120 lines, evidence-based output | lines 427-433 | Pattern 2 sizing |
| Process Orchestrator pattern: Task tool for delegation, strict neutrality, 60-100 lines, return contracts | lines 435-442 | Pattern 3 sizing |
| Meta-Layer Agent pattern: Serena MCP, PDCA, 100-150 lines | lines 444-450 | Pattern 4 sizing |
| Dynamic agent spec mini-language: `<model>[:persona[:"instruction"]]` | lines 456-457, 1709-1716, 2067 | Inline agent invocation in skills |
| Concrete artifact filenames must be declared in `## Outputs` | lines 1099, 1804-1808, 1862-1863 | Output specifications |

**[NOT IN GUIDE] — `agent_name` format with `rf-` prefix rule:** The guide does not define a project-specific name prefix for agents. Example agents are bare: `summary-reporter`, `debate-orchestrator`, `merge-executor`, `pm-agent`. Any `rf-` convention must come from a Rigorflow-specific source outside this guide.

**[NOT IN GUIDE] — `agent_role` line format:** The guide does not define a single "role line" field. The closest construct is the combination of `description:` (frontmatter, one-line) + `## Behavioral Mindset` (body, 1-3 sentences) + `## Responsibilities` (body, numbered list).

**[NOT IN GUIDE] — `parent_skill` linkage requirement:** The guide does not define a frontmatter field that links an agent back to a parent skill. Linkage is implicit and documented in two places: (a) the agent's `## Triggers` section names the invoking command/skill (e.g., line 1774: "Invoked by `/sc:adversarial` command"); (b) the skill's `## Delegation Pattern` table names the agent (e.g., lines 1620-1624). There is no parsed or required frontmatter field that enforces this linkage.

**[NOT IN GUIDE] — `agent_family` classification:** The guide does not define an `agent_family` field. The closest construct is the `category:` frontmatter field (line 387) which uses values like `analysis`, `meta`, `utility`. The four agent *patterns* (Constrained Worker, Specialist Investigator, Process Orchestrator, Meta-Layer Agent — lines 419-450) are documented as design archetypes but are NOT a parsed frontmatter field.

---

## Agent Anti-Patterns

| Anti-Pattern | Where in guide | What every agent file MUST AVOID |
|---|---|---|
| Agent that does everything | line 1102 | Unbounded scope — must constrain |
| Skipping the `## Triggers` section | line 1103 | Makes auto-activation unreliable |
| Allowing an agent to BOTH orchestrate AND execute | lines 1104, 1181 | Role confusion, inconsistent behavior — pick one role |
| Omitting the `## Boundaries` section | line 1105 | Will / Will Not is mandatory |
| Skipping the `## Does NOT` constraints | implicit at line 412 (required) and lines 1098, 2038 | Negative constraints are required |
| Tool list without explanation of WHY | line 1097 (rule states tools must include WHY) | Bare tool list is insufficient |
| Behavioral Mindset that only states what to do (no reasoning philosophy) | line 1170 | Must explain reasoning, not just commands |
| Behavioral Mindset longer than 1-3 sentences | line 1096 | Concision rule |
| Outputs without concrete artifact names and formats | line 1099 | Must declare filenames and formats |
| Trying to do too much (multiple unrelated responsibilities) | line 1160 | Inconsistent results — focus on one responsibility |
| Orchestrator agent that participates in the work it orchestrates | lines 441, 1810-1814, 1822 | Orchestrators delegate only; never advocate or execute |
| Worker agent that deviates from a plan | lines 1843-1845, 1865-1867, 1876-1878 | Worker agents follow plans precisely; no independent decisions |
| Agent without provenance annotations on outputs (when integrating from multiple sources) | lines 1842-1844, 1865, 1877 | Provenance documentation required for merge-style work |

---

## Command Authoring Conventions

| Convention | Where in guide | Applies to which command file element |
|---|---|---|
| File path: `src/superclaude/commands/<name>.md` | lines 1196, 1257, 2057 | File location |
| Installation target: `~/.claude/commands/sc/<name>.md` | line 2057 | Where it lands after install |
| Required frontmatter `name: <command-name>` (identifier, maps to `/sc:<name>`) | lines 252, 1956 | Identifier |
| Required frontmatter `description: "<one-line description>"` | lines 253, 1957 | Summary |
| Required frontmatter `category: <category>` | lines 1958, 1202, 1315 | Functional grouping |
| Required frontmatter `complexity: <simple\|moderate\|advanced\|high>` | line 1959 | Complexity tier |
| Required frontmatter `mcp-servers: [<servers>]` (declare even if empty: `[]`) | lines 1084, 1960 | MCP declaration |
| Required frontmatter `personas: [<personas>]` (declare even if empty: `[]`) | lines 1084, 1961 | Persona declaration |
| H1 heading format: `# /sc:<name> - <Title>` | lines 1208, 1321, 1501, 1964 | First heading uses `/sc:` prefix in title |
| Required body section `## Triggers` — `User invokes /sc:<name>` plus additional trigger conditions | lines 1210-1212, 1323-1325, 1966-1968 | Activation rules |
| Required body section `## Usage` with bash code block | lines 1214-1220, 1327-1333, 1970-1974 | Usage examples |
| Required body section `## Options` table with columns Flag / Short / [Required] / Default / Description | lines 1222-1227, 1335-1341, 1517-1528, 1976-1980 | Options table |
| Required body section `## Behavioral Flow` (numbered steps) — sometimes labeled `## Behavioral Summary` for advanced commands | lines 1229-1235, 1343-1352, 1530-1537, 1982-1985 | Numbered step list |
| Optional body section `## MCP Integration` — bullet list of `**<Server>**: <how used>` | lines 1354-1356, 1987-1988 | MCP usage |
| Optional body section `## Required Input` — for advanced commands with strict input contracts | lines 1503-1505 | Strict input declaration |
| Required body section `## Examples` — bash code block, 3-5 copy-paste examples | lines 1083, 1237-1243, 1358-1364, 1990-1995 | Worked examples |
| Required body section `## Boundaries` with `**Will:**` and `**Will Not:**` lists | lines 1245-1254, 1366-1376, 1539-1549, 1997-2003 | Will / Will Not boundaries |
| Skills have a thin command layer in front of them (~80-150 lines): flags, usage, examples, boundaries, `## Activation` handoff to skill | lines 1110, 1119, 1132, 1178 | Required for every skill |
| `sc-` (or `sc:`) prefix indicates a skill backing a `/sc:` command | line 2081 (Glossary) | Skill naming, not command naming |
| Use existing command archetypes as starting points | line 1085 | Pattern reuse |
| Use STOP language for required inputs (`STOP if missing`) | lines 1149, 1166, 1580-1588, 2083 (Glossary) | Input enforcement |
| Use `version` field in frontmatter for breaking interface changes | line 1164 | Versioning |
| Hardcoded file paths forbidden — use arguments and `@<path>` references | lines 1090, 1184 | Portability |
| Register the command in `COMMANDS.md` and `ORCHESTRATOR.md` after creation | lines 1091, 1185 | Framework integration / dispatcher |
| Three command archetypes: simple/moderate/advanced (see complexity field) | lines 1192, 1305, 1485 | Complexity tiers |

---

## Command Anti-Patterns

| Anti-Pattern | Where in guide | What every command file MUST AVOID |
|---|---|---|
| Command that does everything (violates SRP) | line 1088 | Single responsibility |
| Skipping the `## Boundaries` section | lines 1089, 1182 | Will / Will Not required — leads to scope creep |
| Hardcoding file paths | lines 1090, 1184 | Use arguments and `@<path>` references |
| Forgetting to register the command in `COMMANDS.md` and `ORCHESTRATOR.md` | lines 1091, 1185 | Command becomes invisible to dispatcher routing |
| Skipping `## Required Input` or `## Triggers` | line 1081 (rule: start with one of these) | Activation/input ambiguity |
| Frontmatter missing `mcp-servers` or `personas` (even when empty) | line 1084 | Must declare with `[]` if unused |
| Fewer than 3-5 worked examples | line 1083 | Examples required for usability |
| Skill without command layer (skill handles both interface and protocol) | line 1178 | Always create thin command in front of skill |
| Command that handles flags AND protocol logic instead of delegating to skill | lines 1119-1120 | Command is interface; skill is engine |
| Boundaries section omitted | line 1182 | Repeated rule for emphasis |
| Silent failures / no error matrix in the backing skill | line 1186 | Define scenario/behavior/fallback table |

---

## Sub-Agent Invocation Patterns

| Pattern | Where in guide | Detail |
|---|---|---|
| Permanent agent (defined as a file in `agents/`) — invoked via Task tool by skill or orchestrator | lines 1620-1624 (Delegation Pattern table) | Static agent file, listed in skill's `## Delegation Pattern` |
| Dynamic agent — instantiated per Task call using agent spec mini-language `<model>[:persona[:"instruction"]]` | lines 456-457, 1623-1624, 1709-1716, 2067 | Inline at Task tool call |
| Sub-agent auto-delegation triggers: `file_count > 50 AND complexity > 0.6` → `--delegate --sub-agents` (90% confidence) | line 827 (Part 1, cross-ref) | Framework auto-delegation rule |
| Skill's `## Delegation Pattern` table maps agent → role → instantiation type (Permanent/Dynamic) | lines 1620-1624, 1924-1928 (template) | Delegation manifest in SKILL.md |
| Tool requirement for delegating agents: `Task` tool must be in `## Tools` section with rationale | lines 1785, 1797 | Task tool rule |
| Orchestrator agent declares delegation explicitly in `## Does NOT` (e.g., "delegates to advocate agents") | lines 1810-1814, 1865-1867 | Negative-constraint enforcement of delegation |

---

## Sanity-Check Checklist (12 items)

Use this checklist to validate any companion agent file or command file generated by the skill-creator (Phase 7 nesting and `/sc:persona-research` command).

### Agent file checks

1. **Frontmatter has `name`, `description`, `category`** (lines 385-388, 2010-2013). The fields `agent_name`, `agent_role`, `parent_skill`, and `agent_family` are NOT guide-defined — do not require them; if a Rigorflow convention adds them, document the source.

2. **Body has all required sections in order:** `# <Title>`, `## Triggers`, `## Behavioral Mindset`, `## Tools`, `## Responsibilities`, `## Outputs`, `## Does NOT`, `## Boundaries` with Will/Will Not (lines 404-413, 2015-2048).

3. **Behavioral Mindset is 1-3 sentences and explains the WHY** (lines 1096, 1170), not just what to do.

4. **Each entry in `## Tools` has a rationale** (e.g., `**Read**: Access README and config files`) — bare tool names are an anti-pattern (lines 1097, 1278-1280).

5. **`## Outputs` declares concrete artifact filenames** (e.g., `merged-output.md`, not "the merged file") (lines 1099, 1804-1808, 1862-1863).

6. **Agent has ONE role: orchestrator OR worker, not both** (lines 1104, 1181). Orchestrators delegate via Task; workers execute and return artifacts.

7. **Linkage to invoking skill/command is documented in `## Triggers`** (lines 1774, 1839) since the guide has no `parent_skill` field. Trigger line should name the invoking `/sc:<command>` or skill explicitly.

8. **Line count matches pattern**: Constrained Worker 40-60, Specialist Investigator 80-120, Process Orchestrator 60-100, Meta-Layer 100-150 (lines 425, 433, 442, 450).

### Command file checks

9. **Frontmatter has `name`, `description`, `category`, `complexity`, `mcp-servers`, `personas`** — `mcp-servers` and `personas` declared even if empty (`[]`) (lines 1084, 1956-1962).

10. **H1 uses `# /sc:<name> - <Title>` format and `## Triggers` includes `User invokes /sc:<name>`** (lines 1208, 1964, 1210, 1966).

11. **Body has `## Usage`, `## Options` (table), `## Behavioral Flow` (numbered), `## Examples` (3-5 worked, lines 1083), and `## Boundaries` (Will/Will Not)** (lines 1214-1254, 1970-2003).

12. **No hardcoded paths; STOP language for required inputs; command is registered in COMMANDS.md + ORCHESTRATOR.md after creation** (lines 1090, 1166, 1091, 1185).

---

## Summary

This analysis covers lines 1045-2088 of the SuperClaude developer guide (Best Practices §9, Complete Examples §10, Appendices A-E), with cross-references to lines 380-460 for agent-frontmatter authority since the partition assignment requires those fields. Key extractions:

- **22 agent authoring conventions** — frontmatter shape, required body sections, four agent design patterns with size guidance, dynamic agent-spec mini-language.
- **13 agent anti-patterns** — primarily about scope discipline, missing sections, role confusion, and missing rationale.
- **24 command authoring conventions** — frontmatter shape, command-as-thin-layer-over-skill rule, required body sections, dispatcher registration.
- **11 command anti-patterns** — SRP violations, missing boundaries, hardcoded paths, missing registration.
- **6 sub-agent invocation patterns** — permanent vs dynamic, Task tool requirement, agent-spec mini-language, delegation manifest in skill.
- **12-item sanity checklist** for Phase 7 generated companion agents and `/sc:persona-research` command.

**Critical caveat for Phase 7 (agent-creator nesting):** The prompt's terms `agent_name` (with `rf-` prefix), `agent_role`, `parent_skill`, and `agent_family` are NOT vocabulary in this guide. The skill-creator skill or agent-creator skill must either (a) source these conventions from a Rigorflow-specific reference, or (b) map them to the guide's actual fields (`name`, `description` + `## Behavioral Mindset` + `## Responsibilities`, `## Triggers`-based linkage, `category`). The generated companion agents should follow the guide's `name/description/category` frontmatter unless a Rigorflow convention overrides — and that override should be cited from its source. Failing to acknowledge this mismatch risks producing agent files that satisfy a non-existent specification.

**Critical caveat for command generation:** If `/sc:persona-research` is generated, the guide REQUIRES it be registered in both `COMMANDS.md` and `ORCHESTRATOR.md` (lines 1091, 1185). The skill-creator should produce or instruct registration for these dispatcher files, not just the command file in `src/superclaude/commands/`.
