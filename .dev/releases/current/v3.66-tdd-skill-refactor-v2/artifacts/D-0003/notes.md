# D-0003: Developer Guide Reference Notes

**Task:** T01.03
**Source:** `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`
**Sections:** 9.3 (Skill Design / Separation of Concerns), 9.7 (Anti-Patterns / Skill-Command Boundaries), 5.10 (Skill-Authoring Checklist)

---

## Section 9.3 — Skill Design (Separation of Concerns)

**Location:** Lines 1107-1126

### DO Rules:
1. **Create a thin command layer** (`commands/<name>.md`, ~80-150 lines) for every skill — flags, usage, examples, boundaries, and an `## Activation` section that invokes the skill. No exceptions, including when refactoring existing skills.
2. Keep SKILL.md under 500 lines (behavioral intent only)
3. Move algorithms and templates to `refs/` for lazy loading
4. Use `allowed-tools` as the primary safety boundary
5. Define input contracts with STOP/WARN conditions
6. Define return contracts for composability
7. Declare per-wave ref loading instructions

### DO NOT Rules:
1. Ship a skill without a command in front of it (the command is the user-facing interface; the skill is the behavioral engine)
2. Put flags, usage examples, or CLI interface concerns in SKILL.md (belongs in the command)
3. Pre-load all refs at skill invocation (violates lazy loading)
4. Put implementation details in SKILL.md (belongs in refs/)
5. Use unrestricted `Bash` when specific commands suffice
6. Create skills without tool allowlisting
7. Skip the Will Do / Will Not Do boundaries

### Key Separation Principle:
- **Command** = user-facing interface (flags, usage, examples, boundaries, activation)
- **Skill** = behavioral engine (protocol, WHAT/WHEN, under 500 lines)
- **Refs** = implementation details (algorithms, templates, HOW content)

---

## Section 9.7 — Anti-Patterns (Skill/Command Boundaries)

**Location:** Lines 1174-1187

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| Skill without command layer | Skill handles both interface and protocol concerns, creating a monolith; no standardized user-facing entry point | Create a thin command file (~80-150 lines) with flags, usage, examples, boundaries, and `## Activation` handoff to the skill |
| Monolithic SKILL.md | Exceeds token budget, slow loading | Split into SKILL.md + refs/ |
| Unrestricted `Bash` in allowed-tools | Safety risk, unbounded execution | Use `Bash(git *)`, `Bash(wc *)` patterns |
| Agent that orchestrates AND executes | Role confusion, inconsistent behavior | Separate into orchestrator + worker |
| Command without Boundaries | Scope creep, unpredictable behavior | Always include Will / Will Not |
| Pre-loading all refs | Token waste, slow invocation | Load refs per-wave on demand |
| Hardcoded file paths in skills | Breaks portability | Use arguments and relative paths |
| Skipping framework registration | Command invisible to routing | Update COMMANDS.md + ORCHESTRATOR.md |
| No error handling matrix | Silent failures, confusing behavior | Define scenario/behavior/fallback table |

### Key Boundary Rule (from Anti-Patterns):
The first anti-pattern is the most relevant to this refactoring: **"Skill without command layer"** — a skill that handles both interface and protocol concerns creates a monolith. The solution is always a thin command file with `## Activation` handoff.

---

## Section 5.10 — Skill-Authoring Checklist

**Location:** Lines 734-750

Checklist items for creating or refactoring a skill:

- [ ] **Thin command layer exists** — a command file at `src/superclaude/commands/<name>.md` (~80-150 lines) with flags, usage, examples, boundaries, and an `## Activation` section that invokes `Skill <skill-name>`. The command contains zero protocol logic.
- [ ] SKILL.md has YAML frontmatter with `name`, `description`, `allowed-tools`
- [ ] SKILL.md contains only behavioral protocol (WHAT/WHEN) — under 500 lines
- [ ] `allowed-tools` is scoped to minimum required (no unnecessary `Edit` or `Bash`)
- [ ] Purpose section clearly states what the skill does and does not do
- [ ] Will Do / Will Not Do boundaries are explicit
- [ ] If complex: refs/ directory contains algorithm and template details (HOW content)
- [ ] SKILL.md declares when each ref should be loaded (per-wave)
- [ ] Input contract defines STOP/WARN conditions for missing inputs
- [ ] Output contract defines return fields for composability
- [ ] If the skill uses agents: agent delegation is explicit with Task tool
- [ ] Framework registration is complete (COMMANDS.md, ORCHESTRATOR.md, etc.)

---

## Implications for TDD Skill Refactoring

These three sections establish the authoritative architectural rules governing the refactoring:

1. **The TDD skill MUST have a thin command layer** (Section 9.3 Rule #1, Section 5.10 Checklist Item #1, Section 9.7 Anti-Pattern #1)
2. **Flags, usage, examples, and CLI concerns must migrate FROM SKILL.md TO the command** (Section 9.3 DO NOT #2)
3. **SKILL.md must contain only behavioral protocol** (WHAT/WHEN), under 500 lines (Section 9.3 DO #2, Section 5.10 Item #3)
4. **The command file's `## Activation` section invokes the skill** — command contains zero protocol logic (Section 5.10 Item #1)
5. **Implementation details (algorithms, templates) belong in refs/**, not SKILL.md (Section 9.3 DO NOT #4)
