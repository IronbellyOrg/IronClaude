# D-0001: Template Analysis Notes -- `adversarial.md` Gold-Standard

**Source file:** `src/superclaude/commands/adversarial.md` (canonical), `.claude/commands/sc/adversarial.md` (dev copy)
**Line count:** 168 lines (both copies identical)
**Task:** T01.01

---

## Section Ordering (10 sections)

| # | Section | Lines | Level | Notes |
|---|---------|-------|-------|-------|
| 1 | **Frontmatter** | 1-9 | YAML block | 8 fields: `name`, `description`, `category`, `complexity`, `allowed-tools`, `mcp-servers`, `personas` |
| 2 | **Required Input** | 12-16 | `## Required Input` | Bullet list of mode signatures (Mode A, Mode B, Pipeline) |
| 3 | **Usage** | 18-32 | `## Usage` | Fenced bash code blocks showing invocation patterns per mode |
| 4 | **Arguments** | 34-48 | `### Arguments` | Subsection under Usage; bold mode headers with bullet descriptions |
| 5 | **Options** | 50-68 | `## Options` | Markdown table with columns: Flag, Short, Required, Default, Description |
| 6 | **Behavioral Summary** | 70-72 | `## Behavioral Summary` | Single dense paragraph summarizing protocol steps and artifacts produced |
| 7 | **Examples** | 74-129 | `## Examples` | 9 named subsections (`###`), each with a fenced bash code block |
| 8 | **Activation** | 130-136 | `## Activation` | **MANDATORY** skill invocation directive; blockquote with `Skill` call; two-line prohibition on proceeding without the skill |
| 9 | **Boundaries** | 138-157 | `## Boundaries` | Split into **Will:** (9 items) and **Will Not:** (6 items) bullet lists |
| 10 | **Related Commands** | 159-167 | `## Related Commands` | Markdown table with columns: Command, Integration, Usage |

---

## Frontmatter Fields (7 fields in YAML block)

```yaml
name: adversarial                          # command identifier
description: "..."                         # human-readable summary (quoted string)
category: analysis                         # command category
complexity: advanced                       # complexity tier
allowed-tools: Read, Glob, Grep, ...      # comma-separated tool whitelist
mcp-servers: [sequential, context7, serena] # YAML array of MCP servers
personas: [architect, analyzer, scribe]     # YAML array of personas
```

**Key observations:**
- Frontmatter is delimited by `---` fences (lines 1 and 9)
- `allowed-tools` uses comma-separated string format
- `mcp-servers` and `personas` use YAML array `[...]` format
- No `version`, `author`, or `tags` fields present

---

## Activation Pattern

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:adversarial-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.
```

**Pattern structure:**
1. Bold `MANDATORY` label
2. Blockquote containing the exact `Skill` invocation target (`sc:<name>-protocol`)
3. Two-line prohibition statement separating command (routing) from skill (behavior)

---

## Boundaries Format

**Structure:** Two labeled bullet lists under a single `## Boundaries` heading.

- **Will:** -- 9 bullet items describing what the command does (positive capabilities)
- **Will Not:** -- 6 bullet items describing explicit exclusions (negative constraints)

**Pattern:** Each item is a single sentence, starting with a verb (infinitive form). Parenthetical clarifications appear at end of some items for context (e.g., "(calling command's responsibility)").

---

## Template Structural Rules Derived

1. **Heading hierarchy:** `#` for title (line 11), `##` for major sections, `###` for subsections
2. **Title format:** `# /sc:<name> - <Human-Readable Title>`
3. **Section separator:** Blank lines between sections (no `---` dividers within body)
4. **Code blocks:** All examples use ` ```bash ` fencing
5. **Options table:** Standard 5-column markdown table (Flag, Short, Required, Default, Description)
6. **Related Commands table:** Standard 3-column markdown table (Command, Integration, Usage)
7. **Activation is a routing layer only** -- the command file defines interface; the protocol skill defines behavior
