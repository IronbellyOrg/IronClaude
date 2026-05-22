---
Status: Complete
---

# Research Notes: Add Wave 1.5 (Documentation Grounding) to sc:troubleshoot

**Date:** 2026-05-22
**Scenario:** A (explicit — user provided full spec including files, structure, downstream wiring, and verification steps)
**Depth Tier:** Standard (4 researchers)
**Track Count:** 1 (single cohesive output: extend sc:troubleshoot with documentation grounding wave)

---

## EXISTING_FILES

### Command file (edit target)

- **`src/superclaude/commands/troubleshoot.md`** (198 lines) — `/sc:troubleshoot` command surface
  - Frontmatter line 1-9 — name, description, argument-hint
  - Options table lines 46-57 — flag definitions (must add `--no-doc-discovery` row)
  - Behavioral Summary lines 59-74 — tier table (must mention Documentation Grounding)
  - Boundaries lines 155-177 — Will/Will-Not (must add doc-grounding entries)
  - Skill activation lines 76-81 — hands off to `sc:troubleshoot-protocol`

### Skill file (edit target)

- **`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`** (385 lines) — wave protocol owner
  - Frontmatter lines 1-12 — name, description, allowed-tools, extended-metadata comment
  - Output Contract lines 37-66 — structured return dict (potentially extend with `behavior_is_documented`)
  - Wave Structure block lines 67-79 — wave list (must add Wave 1.5)
  - Wave 0 line 83 — parse + validate
  - Wave 1 line 121 — Tier 1 Triage (Wave 1.5 inserts AFTER this)
  - Wave 2 line 147 — Confidence Gate
  - Wave 3 line 167 — Tier 2 Parallel Hypotheses (PATTERN TO MIRROR for parallel fan-out)
  - Wave 4 line 219 — Adversarial Fix Debate (must reference Restrictions section)
  - Wave 5 line 248 — Synthesis + Report (must add Documentation Context section)
  - Wave 6 line 292 — Remediation Chain
  - Refs loaded table — must add `refs/doc-discovery.md`
  - Graceful Degradation table — must add Auggie-unavailable + --no-mcp rows for Wave 1.5
  - MCP Integration block — Auggie now load-bearing in Wave 1.5

### Existing refs (read for pattern reference, NOT edit targets)

- `refs/escalation-rubric.md` (52 lines) — confidence calibration + escalation decision (Wave 1/2)
- `refs/triage-checklist.md` (65 lines) — Wave 1 brief checklist
- `refs/hypothesis-card-template.md` (107 lines) — hypothesis card schema (MUST extend with `consistency_with_docs` field)
- `refs/report-template.md` (153 lines) — REPORT.md template (MUST extend with Documentation Context section + `behavior_is_documented` field)
- `refs/remediation-handoff.md` (122 lines) — Wave 6 hand-off prompt

### New file (create target)

- **`src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md`** — new ref for Wave 1.5
  - Section 1: Auggie query templates for Branch A (release-doc), Branch B (architectural), Branch C (semantic-restriction)
  - Section 2: Branch B currency-check procedure with `stat` + `grep` examples
  - Section 3: Structured-output schema per branch (Branch A: release_slug/artifact_paths/summary/confidence; Branch B: docs_considered + currency_verdict; Branch C: constraint citations)
  - Section 4: Documentation Context Card template (sections: Release context, Architectural docs consulted, Restrictions, Re-frame signals)

### Discovery surfaces (read by Branch A/B agents at runtime — NOT edit targets)

- `.dev/releases/current/` — 5 active release dirs (cliEval, CLIPRD-schemaMismatch, roadmap-cli-skill-converge, task-builder-merge, task-sc-task-directional-merge)
- `.dev/releases/complete/` — 10 completed release dirs
- `docs/` — has reference/, developer-guide/, analysis/, troubleshooting/, plus standalone .md files

### Build/sync infrastructure

- `make sync-dev` — copies `src/superclaude/{skills,agents,commands}/` → `.claude/`
- `make verify-sync` — fails if `.claude/` has dirs without `src/` counterparts
- Pre-commit hook + project convention: `.claude/` is gitignored except `settings.json`

---

## PATTERNS_AND_CONVENTIONS

### Wave block structure (from existing waves 0-6)

Each wave in SKILL.md follows this template:

```
### Wave N: <Name>

**Preconditions**: <state required to enter>.

**Steps**:

1. <Numbered step>
2. <Numbered step>
...

**Exit criteria**: <what must be true to advance>.
```

Wave 3 (line 167) is the canonical parallel-fan-out pattern: spawn 2-4 specialist agents via `Task` in a single message, each gets a hypothesis-card-template.md brief, each writes its own card to `<output-dir>/hypothesis-cards/`. Wave 1.5 mirrors this for the three discovery branches.

### Refs loader convention

Each ref is loaded only by the wave that needs it (lazy load). SKILL.md has a table near the bottom mapping `refs/foo.md | Wave N (purpose)`. New entry: `refs/doc-discovery.md | Wave 1.5 (passed to each branch agent as part of the brief)`.

### Graceful Degradation convention

Existing table maps scenario → behavior → fallback. Pattern: when auggie unavailable, use Glob+Grep; when MCP entirely unavailable, run native-tools-only with audit note. New rows for Wave 1.5: Branch A degrades to Glob+Grep over `.dev/releases/{current,complete}/`; Branch B always uses native tools (Bash stat + Grep) so no degradation needed; Branch C degrades to Grep over the artifact paths surfaced by Branch A.

### Boundaries Will / Will Not convention

List of bullets. New entries to add:

- Will: "Always run documentation grounding before recommending any fix unless `--no-doc-discovery` is set."
- Will Not: "Recommend a fix that violates a documented constraint without flagging it as a doc-update + code-fix bundle."

### Options table convention

Pipe-delimited markdown table with three columns: Flag | Default | Description. New row format:

```
| `--no-doc-discovery` | `false` | Skip Wave 1.5 (release/doc/restriction search). Use only when the user has confirmed there are no relevant PRD/TDD/Spec docs. The skip is recorded in REPORT.md's Grounding Gaps. |
```

### Output Contract extension

SKILL.md has a structured return dict at lines 39-55. The new `behavior_is_documented` field plus a `doc_context_card_path` field would slot in there.

### Hypothesis card extension

`refs/hypothesis-card-template.md` defines the per-agent card schema. New field `consistency_with_docs: { aligned | conflicts | not_applicable | no_docs_found }` with a one-line justification.

### Report template extension

`refs/report-template.md` defines REPORT.md. New section "Documentation Context" (≤6 lines summary + constraints honored/overridden list). Extends existing `test_is_wrong` semantics with a parallel `behavior_is_documented` boolean.

---

## GAPS_AND_QUESTIONS

None blocking — the user's spec is explicit on every integration point. Open considerations the researchers may surface:

1. **Wave 1.5 conditional-or-always**: User says "ALWAYS in Tier 1 and Tier 2". Confirms: not gated on --type. The `--no-doc-discovery` flag is the only skip lever.

2. **Branch B currency check precision**: User says compare doc mtime against issue's component mtimes. If --scope is a directory, take max(mtime) across files. If no --scope, currency-check is impossible — should the agent (a) skip Branch B entirely or (b) consult all docs with `unknown` verdict? Spec interpretation: graceful default to `unknown` and exclude from Branch C input.

3. **Branch C's "applies_to" field semantics**: Free-text scope description (e.g., "the eval pipeline retry handler") vs structured path glob. The agent decides per citation.

4. **Whether `behavior_is_documented=true` AND `test_is_wrong=false` is the canonical "doc says this is intentional" path**: REPORT.md should recommend a spec change in that case, not a code change. The user's wording confirms this.

5. **Wave 1.5 timing in tier 2**: User says "runs ALWAYS in Tier 1 and Tier 2". Wave 1.5 runs ONCE, between Wave 1 and Wave 2 (i.e., before the escalation gate). The Tier 2 hypothesis agents in Wave 3 consume the card produced by the single Wave 1.5 invocation; they do NOT re-run Wave 1.5 per agent.

---

## RECOMMENDED_OUTPUTS

The task file the builder produces should drive an executor to:

1. **Read pre-work files** (troubleshoot.md, SKILL.md, refs/*.md, sanity-check .dev/releases/ + docs/)
2. **Edit `src/superclaude/commands/troubleshoot.md`** — Options table row, Behavioral Summary update, Boundaries Will/Will-Not bullets
3. **Edit `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`** — wave list, new Wave 1.5 block, refs loader table, Graceful Degradation table, MCP Integration update, Output Contract extension (`behavior_is_documented`), Wave 1 brief enhancement, Wave 3 brief enhancement, Wave 4 weighting rule, Wave 5 Documentation Context section
4. **Edit `refs/hypothesis-card-template.md`** — add `consistency_with_docs` field
5. **Edit `refs/report-template.md`** — add Documentation Context section + `behavior_is_documented` field
6. **Create `refs/doc-discovery.md`** — 4-section new ref
7. **Run** `make sync-dev` then `make verify-sync` (must both pass)
8. **Verify** with grep/test commands listed in the user spec

Granularity per MDTM A3: ONE checklist item per file edit (or per discrete edit anchor where multiple anchors exist in the same file). The task file should NOT batch as "edit all 3 files in one item".

---

## SUGGESTED_PHASES (researcher assignments)

Standard tier — 4 researchers spawned in parallel:

### Researcher 1: File Inventory + Anchor Identification

**Scope:** `src/superclaude/commands/troubleshoot.md` AND `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` AND `refs/*.md`
**Output:** `${TASK_DIR}research/01-file-inventory.md`
**Focus:** For each edit-target file, document:

- Exact line ranges of every section that must be edited (Options table start/end, Behavioral Summary, Boundaries, Wave Structure block, Wave 3 fan-out pattern, Refs loader table, Graceful Degradation table, MCP Integration, Output Contract, hypothesis-card-template's field list, report-template's section headers)
- Current section content (verbatim quote) so the builder can write items that say "replace X with Y" with no ambiguity
- For NEW Wave 1.5 block: identify the exact insertion line (after end of Wave 1, before "### Wave 2")
- Refs file inventory with line counts + section headers
- Coverage: which `.dev/releases/` and `docs/` subdirs Branch A/B agents will search at runtime (NOT verifying their contents — just confirming existence)

### Researcher 2: Patterns & Conventions

**Scope:** Existing wave blocks in SKILL.md (Wave 0-6) + refs file structure
**Output:** `${TASK_DIR}research/02-patterns-and-conventions.md`
**Focus:**

- Extract the canonical Wave block template (Preconditions, Steps, Exit criteria) with line citations
- Document Wave 3's parallel-fan-out pattern (the model to mirror) — exact Task-spawn block, brief-construction approach, output collection
- Document refs loader table format and where new entries go alphabetically
- Document Graceful Degradation table format and existing rows
- Document Boundaries Will/Will-Not bullet style
- Document Options table cell format
- Document Output Contract field-row format

### Researcher 3: Integration Points (downstream wiring)

**Scope:** SKILL.md waves 1, 3, 4, 5 + hypothesis-card-template.md + report-template.md
**Output:** `${TASK_DIR}research/03-integration-points.md`
**Focus:**

- Wave 1: where the root-cause-analyst brief is constructed; how the Documentation Context Card path gets passed in
- Wave 3: where each specialist agent's brief is constructed; how the card propagates per-agent
- Wave 4: where adversarial fix proposals are weighted; how to inject the Restrictions section as a debate input
- Wave 5: where REPORT.md is composed; insertion point for the Documentation Context section
- hypothesis-card-template.md: exact field list, where `consistency_with_docs` slots
- report-template.md: exact section headers, where Documentation Context slots, where `behavior_is_documented` boolean appears alongside `test_is_wrong`
- Output Contract dict: exact field list, where `behavior_is_documented` and `doc_context_card_path` slot

### Researcher 4: Template & Examples

**Scope:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` + prior `.dev/tasks/to-do/TASK-RF-*` for spec-edit examples
**Output:** `${TASK_DIR}research/04-template-and-examples.md`
**Focus:**

- Read template 02 PART 1 completely; document the A3 (Complete Granular Breakdown) and B2 (self-contained item pattern) rules with verbatim quotes
- Document the L1-L6 handoff patterns if relevant
- Find 1-2 prior TASK-RF examples that edit spec/protocol markdown files (e.g., `TASK-RF-20260518-cliEval-P4-wire-and-ship` likely has spec-edit phases) and extract effective patterns for: (a) per-anchor edit items, (b) sync-dev + verify-sync items, (c) grep-based verification items
- Document the "Execution Context" block emission rules (DM-001 from rf-task-builder spec) — when to emit, what goes in References / Source areas / Key constraints

---

## TEMPLATE_NOTES

**Template selection:** **Template 02 (Complex Task)** — the work involves multiple distinct phases (pre-work reading, per-file editing, file creation, sync/verify, post-verification), each with quality gates. The MDTM template 01 (simple) would lose granularity on the multi-anchor edits.

**Tier selection:** Standard (4 researchers).

- 3 files modified + 1 new file + 2 existing refs to extend = ~6 edit surfaces
- Single subsystem (sc:troubleshoot)
- Moderate discovery (need to read full SKILL.md + refs/ + Wave 3 pattern)
- Spec is highly detailed (low ambiguity), so Deep tier (6-8 researchers) would be overkill

**MDTM features the generated task file should use:**

- **Granular per-anchor items** (A3): each edit anchor in SKILL.md gets its own item (Wave list update, Wave 1.5 insertion, Refs loader table row, Graceful Degradation rows, MCP Integration update, Output Contract extension, Wave 1 brief enhancement, Wave 3 brief enhancement, Wave 4 weighting rule, Wave 5 doc-context section, hypothesis-card field addition, report-template extension). Do NOT batch as "edit SKILL.md".
- **Self-contained item structure** (B2): each item carries context + action + output + verification + completion gate.
- **Quality gates** (QA_GATE_REQUIREMENTS: PER_PHASE): include checklist items that run grep verification after each phase.
- **Validation items** (VALIDATION_REQUIREMENTS): include `make sync-dev` + `make verify-sync` items and the 5 user-supplied verification greps.
- **Testing requirements** (TESTING_REQUIREMENTS: NONE) — this is a spec edit, no runtime tests. Validation gates substitute.
- **Execution Context block** (AUTO): the BUILD_REQUEST has ≥3 inferable source areas (command file, protocol skill, refs subsystem) — emit fully-populated 3-bullet form.

---

## AMBIGUITIES_FOR_USER

None — intent is clear from the user-supplied spec and the codebase context. The five open considerations in GAPS_AND_QUESTIONS are interpretation calls the researchers can resolve from spec text + existing-pattern study; none require user adjudication.
