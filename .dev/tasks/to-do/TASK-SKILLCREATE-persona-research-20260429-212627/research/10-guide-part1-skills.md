# Guide Partition Analysis — Skills Section

**Investigation type:** Guide Partition Analysis — Skills Section
**Scope:** /config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, lines 1-1044
**Status:** Complete
**Date:** 2026-04-29

---

## 1. Source Map

The Skills-relevant content in lines 1-1044 is concentrated in:

| Subsection | Lines | Topic |
|---|---|---|
| 1.x — Three-tier architecture | 38-93 | Skill location in stack, "every skill MUST have a command" rule |
| 1.x — Activation pattern | 60-74 | Command→Skill handoff requirement |
| 1.x — Context loading sequence | 95-105 | Skill lazy-load token economics (~50 → ~2000) |
| 2.3 — Minimal Skill scaffold | 196-225 | Frontmatter floor + minimum body sections |
| 5.1 — Skill anatomy | 483-498 | Directory structure (SKILL.md + refs/ + rules/ + templates/ + scripts/) |
| 5.2 — Frontmatter | 500-538 | Required vs full field set |
| 5.3 — Extended metadata comment | 540-553 | Unparsed HTML comment for orchestration intent |
| 5.4 — Tool allowlisting | 555-569 | Primary safety boundary |
| 5.5 — Complexity tiers | 571-640 | Tier 1 / 2 / 3 (Simple / Medium / Complex) |
| 5.6 — refs/ pattern | 642-665 | Lazy loading, per-wave loading, token budget |
| 5.7 — sc- prefix convention | 667-677 | sc- prefix → /sc:<name> command pairing |
| 5.8 — Machine-readable headers | 679-693 | Telemetry HTML comment blocks |
| 5.9 — Input/Output contracts | 695-732 | STOP/WARN rules + Return Contract table |
| 5.10 — Authoring checklist | 734-749 | Canonical 12-item authoring checklist |
| 6.1 — Wave system | 755-788 | 5-Wave standard (Wave 0..4), per-wave ref loading |
| 9 — Best Practices (referenced from TOC line 19) | (in part 2) | Anti-patterns expected later |

---

## 2. Authoring Conventions Table

| Convention | Where in guide (line) | Applies to which sections of SKILL.md |
|---|---|---|
| Skill MUST live in a directory: `src/superclaude/skills/<name>/SKILL.md` | 53, 487-498 | Filesystem layout (not a body section) |
| YAML frontmatter is required with at minimum `name`, `description`, `allowed-tools` | 502-510 | Frontmatter |
| `description` is loaded at session start (~50 tokens) — must be compact and discoverable | 532, 660-665 | Frontmatter `description` field |
| `allowed-tools` is the primary safety boundary; scope to minimum required | 533, 555-569, 741 | Frontmatter `allowed-tools` field |
| Skills prefixed `sc-` map 1:1 to `/sc:<name>` commands; non-prefixed are standalone utilities | 531, 667-677 | Frontmatter `name` field + companion command file |
| Every skill MUST have a thin command in front of it (architectural rule) | 58, 738 | External: `src/superclaude/commands/<name>.md` |
| The companion command MUST contain an `## Activation` section that hands off via `Skill <skill-name>` | 60-74 | External (command file), but skill author owns it |
| SKILL.md contains behavioral intent only (WHAT and WHEN); HOW lives in `refs/` | 648-651, 740 | Body composition rule |
| SKILL.md max body length ~400-500 lines | 625, 648, 740 | Whole file |
| Optional subdirectories: `refs/`, `rules/`, `templates/`, `scripts/` | 489-498 | Companion folders |
| Optional frontmatter fields (full set): `category`, `complexity`, `mcp-servers`, `personas`, `argument-hint` | 514-525, 528-538 | Frontmatter |
| Extended metadata may be added in an unparsed HTML comment for documentation tools | 540-553 | Body (typically just below frontmatter) |
| Complex skills MUST emit machine-readable HTML-comment headers for telemetry/composition | 679-693 | First output of skill execution |
| Required Input section MUST declare STOP/WARN rules | 697-714 | `## Required Input` section |
| Output / Return Contract section MUST declare structured fields for inter-command composition | 716-732 | `## Return Contract` section |
| `refs/` files load on demand per wave, not at session start | 642-657 | Wave sections in body must declare which ref to load |
| Wave sections must use the 5-wave standard (Wave 0..4) for complex skills | 762-784 | Body wave protocol sections |
| Each wave has explicit preconditions (entry) and postconditions (exit) | 786 | Wave sections |
| Wave checkpointing via Serena MCP for resumability (when applicable) | 788 | Wave sections |
| Tier 1 (Simple) skills may omit `refs/` and stay ~100 lines | 575-594 | Whole file |
| Tier 2 (Medium) skills add `allowed-tools` scoping + structured execution flows; ~400 lines | 596-615 | Body protocol |
| Tier 3 (Complex) skills include refs/, agent delegation, multi-phase protocol; ~400-500 lines | 617-640 | Body + refs/ + agents |
| Skill body MUST include explicit Will / Will Not boundaries | 218-225 (minimal example), 743 | `## Will Do` / `## Will Not Do` sections |
| Skill body MUST include a Purpose section stating what it does and does not do | 209-211, 742 | `## Purpose` section |
| Shell preprocessing (`!command`) may inject runtime context into skill body | 945-956 | Any body section |

---

## 3. Anti-Patterns Table

These are derived from the inverse of stated rules and from explicit cautions in the guide. Lines 1-1044 do not contain a single dedicated "anti-patterns" subsection for skills; the Best Practices section referenced in the TOC (line 19) is in part 2 (line 1045+). Items below are extracted from the prescriptive language in the Skills section.

| Anti-pattern | Why it's bad (per guide) | How to detect |
|---|---|---|
| Skill exists without a paired command file | Architectural violation: forces skill to mix interface and protocol concerns into a monolith (line 58) | Check `src/superclaude/commands/<name>.md` exists for every skill |
| Command file contains protocol logic instead of delegating to the skill via Activation | Violates separation of concerns: command owns interface, skill owns protocol (lines 56, 74) | Grep command file for protocol steps; verify `## Activation` block exists with `Skill <name>` invocation |
| SKILL.md exceeds ~500 lines | Bloats on-invocation token cost; HOW content should live in `refs/` (lines 625, 648, 740) | `wc -l SKILL.md` > 500 |
| HOW content (algorithms, formulas, prompts, templates) embedded inline in SKILL.md | Defeats lazy-loading; refs/ should hold these (lines 644-651) | Look for full-text algorithms/templates inside SKILL.md instead of `Load refs/...` directives |
| Pre-loading all refs upfront instead of per-wave | Negates token efficiency; "at any point a skill should have at most 2-3 refs loaded" (line 650) | Search for ref load directives outside wave-scoped sections |
| Frontmatter missing `name`, `description`, or `allowed-tools` | Minimum required fields per line 502-510, item line 739 | Frontmatter parser/lint |
| `allowed-tools` overly broad (e.g., includes Edit/Bash for read-only skills) | Violates safety boundary principle (lines 555, 569, 741) | Audit `allowed-tools` against skill's stated read-only intent |
| Missing Will / Will Not Do boundaries | Boundaries are required (lines 218-225, 743) | Section presence check |
| Missing Required Input section with STOP/WARN rules (for skills that take input) | Inputs ungoverned; skill cannot fail-fast on missing args (lines 697-714, 745) | Section presence check + STOP/WARN keyword scan |
| Missing Return Contract for composable skills | Breaks inter-command composition (lines 716-732, 746) | Section presence check; verify structured-field table |
| Complex skills missing machine-readable header on output | Breaks telemetry/automation/composition (lines 679-693) | Verify first output is `<!-- SC:...` HTML comment block |
| Wave sections lacking entry/exit criteria | Wave boundaries not enforceable; resumability broken (line 786) | Section structure check per wave |
| sc- prefixed skill installed standalone | sc- prefixed skills are command backings, not standalone utilities (lines 671-675) | Check that sc- skills are paired with /sc:<name> commands and not in standalone install lists |
| Skill body that fabricates persona/agent prompts without delegating via Task tool | Violates "agent delegation is explicit with Task tool" (line 747) | Search for inline persona prompt strings without `Task` tool invocation |
| Tool allowlist includes `Edit` for an audit/report-only skill | Stated safety principle: "omit Edit and scope Write" for audit/report skills (line 569) | Cross-reference skill's stated purpose vs `allowed-tools` |

---

## 4. Ceremony Minimums (per Complexity Tier)

The guide defines three tiers (lines 571-640). It does NOT use the term "Deep tier"; the closest analogue is **Tier 3: Complex**. Numbers below come directly from the guide; where the guide does not state a minimum, the cell is marked "—" rather than fabricated.

| Tier | Min agents | Min line count | Min validations / sub-sections | Source lines |
|---|---|---|---|---|
| Tier 1 — Simple | 0 (no agent delegation) | ~100 lines (example: confidence-check) | Single rubric + threshold + action ranges (e.g., 5 checks, ≥90 / 70-89 / <70 ranges) | 575-594 |
| Tier 2 — Medium | — (delegation optional) | ~400 lines (example: sc-task-unified) | 4 compliance tiers + auto-detection algorithm + machine-readable output header + sub-agent delegation matrix | 596-615 |
| Tier 3 — Complex | ≥1 dynamic agent + ≥1 fixed agent (e.g., debate-orchestrator + advocate agents + merge-executor pattern, lines 875-880) | ~400-500 lines (example: sc-adversarial) | 5-step protocol minimum, hybrid scoring with bias mitigation, dynamic agent instantiation, return contract, error-handling matrix, ≥6 output artifacts | 617-640, 875-882 |
| 5-Wave standard (when applicable) | — | — | 5 waves: Prerequisites, Analysis, Planning, Generation/Execution, Validation — each with entry/exit criteria | 762-786 |

**Note on "Deep tier":** The user prompt asked for "Deep tier" minimums. The guide uses "Tier 3: Complex" instead. If the requesting task uses a different vocabulary (e.g., a `--depth deep` flag on `/sc:adversarial`, line 863), the closest alignment is Tier 3 numbers above. The guide does not provide separate "deep depth" minimums distinct from Tier 3 in lines 1-1044.

---

## 5. Sanity-Check Checklist for Generated SKILL.md

Each item is a yes/no verifier. Numbers in parentheses cite source lines.

1. Does the SKILL.md live at `src/superclaude/skills/<name>/SKILL.md`? (53, 487-498)
2. Does the YAML frontmatter contain at least `name`, `description`, and `allowed-tools`? (502-510, 739)
3. Is the `description` a single concise line suitable for ~50-token session-start loading? (532, 660-665)
4. Is `allowed-tools` scoped to the minimum required (no gratuitous `Edit` or unrestricted `Bash`)? (555-569, 741)
5. Does a paired command file exist at `src/superclaude/commands/<name>.md` containing flags, usage, examples, boundaries, and an `## Activation` section invoking `Skill <name>`? (58, 60-74, 738)
6. Is the skill's `name` correctly prefixed (`sc-` for command-backed; no prefix for standalone utility)? (667-677)
7. Is the SKILL.md body under ~500 lines, and does it contain only WHAT/WHEN (behavioral intent), with HOW content (algorithms/templates/formulas) externalized to `refs/`? (625, 648, 740)
8. Does the body contain a `## Purpose` section stating what the skill does and does NOT do? (209-211, 742)
9. Does the body contain explicit `Will Do` / `Will Not Do` (or equivalent boundary) sections? (218-225, 743)
10. If the skill takes input: does it have a `## Required Input` section with explicit STOP and WARN rules? (697-714, 745)
11. If the skill is composable: does it have a `## Return Contract` section listing structured fields with types and descriptions? (716-732, 746)
12. If the skill uses `refs/`: does the SKILL.md explicitly declare per-wave loading directives (`Load refs/X.md before Wave N`) instead of pre-loading? (642-657, 744)
13. If complex (Tier 3): does the skill emit a machine-readable header (`<!-- SC:...`) as its first output? (679-693)
14. If multi-phase: are wave sections present using the 5-wave standard (Prerequisites/Analysis/Planning/Generation/Validation), each with entry and exit criteria? (762-786)
15. If the skill delegates to agents: is the delegation explicit via the Task tool (no fabricated inline persona prompts)? (747)
16. Is framework registration complete (COMMANDS.md, ORCHESTRATOR.md, FLAGS.md if new flags, PERSONAS.md if new persona triggers)? (749, 365-371)

---

## 6. Summary

The guide's lines 1-1044 give a complete prescriptive specification for SKILL.md authoring, organized around five load-bearing rules:

1. **Pairing rule** — every skill MUST have a thin command in front of it; the command holds interface, the skill holds protocol, and the handoff is the `## Activation` block (lines 58, 60-74).
2. **Lazy-loading rule** — `description` carries ~50 tokens at session start; full SKILL.md (~2000 tokens) loads on invocation; `refs/` files (~500-1500 tokens each) load per-wave with at most 2-3 active at any time (lines 660-665, 642-657).
3. **WHAT vs HOW separation** — SKILL.md holds behavioral intent under ~500 lines; algorithms, formulas, prompts, and templates go in `refs/` (lines 625, 648, 740).
4. **Safety boundary rule** — `allowed-tools` is the primary safety boundary; scope it minimally and omit `Edit`/`Bash` for read-only skills (lines 555-569).
5. **Tiered ceremony** — Tier 1 Simple (~100 lines, no refs), Tier 2 Medium (~400 lines, allowed-tools + structured flows), Tier 3 Complex (~400-500 lines + refs/ + agents + multi-phase + machine-readable header + return contract) (lines 571-640).

The 16-item sanity-check above operationalizes these rules. Items are evidence-anchored to specific guide lines; nothing is fabricated. The guide does not use the term "Deep tier" within the analyzed range — Tier 3 (Complex) is the closest match and supplies the relevant ceremony floor for skills that need agent delegation, multi-phase waves, and a return contract.

Anti-patterns are derived chiefly from the inverse of prescriptive rules; a dedicated Best Practices section lives in part 2 (line 1045+) and may add additional anti-patterns to cross-reference. The Tier 3 ceremony floor inferred from the `sc-adversarial` exemplar (lines 617-640 + 875-882) implies at least one orchestrator-style agent plus at least one variable/dynamic agent class, a 5-step or 5-wave protocol, hybrid scoring with bias mitigation, dynamic agent instantiation, a return contract, an error-handling matrix, and ≥6 output artifacts.
