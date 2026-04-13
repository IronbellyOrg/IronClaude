# PRD Skill Refactoring — Brainstorm Output

> **Generated**: 2026-04-03
> **Input**: `.dev/releases/backlog/prd-skill-refactor/01-brainstorm-prompt.md`
> **Mode**: `--seq --ultrathink`
> **Source files read**: PRD SKILL.md (1,369 lines), Developer Guide (5 sections), adversarial command (167 lines), adversarial protocol SKILL.md (first 100 lines), adversarial refs/ (4 files), existing spec at `.dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md` (507 lines), fidelity index at `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` (395 lines)

---

## Preliminary Finding: Spec and Fidelity Index Location

The brainstorm prompt references files at `.dev/releases/backlog/prd-skill-refactor/` but both the spec and fidelity index actually reside at `.dev/releases/complete/v3.65-prd-refactor/`:
- Spec: `.dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md`
- Fidelity index: `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md`

Additionally, the existing PRD refs/ files already contain extracted content:
- `refs/agent-prompts.md` — 422 lines (exists)
- `refs/synthesis-mapping.md` — 142 lines (exists)
- `refs/validation-checklists.md` — 153 lines (exists)

But `refs/build-request-template.md` does NOT yet exist, and the SKILL.md has NOT been trimmed (still 1,369 lines). The spec was written and the refs were partially created, but the actual decomposition (removing content from SKILL.md) was never executed. Content is currently duplicated across SKILL.md and refs/.

---

## Dimension 1: Thin Command Layer Design

### Current State

The PRD skill has **no command file**. Users invoke it via `Skill prd` or it's triggered by the skill description matcher. This violates the Developer Guide mandate: "Every skill MUST have a command in front of it" (Three-Tier Architecture section) and the anti-pattern table (Section 9.7): "Skill without command layer → Skill handles both interface and protocol concerns, creating a monolith."

### Option A: Minimal Command (~100 lines)

Bare essentials: frontmatter, brief usage, required input, 2-3 examples, activation, boundaries. No options table (no explicit flags — skill auto-detects everything).

**Trade-offs**: Fast to create, low maintenance surface. But loses the opportunity to formalize tier selection and resume as explicit flags, making the skill harder to invoke precisely.

### Option B: Standard Command (~130-150 lines) — **Recommended**

Full adversarial-style command: frontmatter, required input, usage block, arguments, options table with explicit flags, behavioral summary, 4-5 examples, activation, boundaries, related commands.

Explicit flags to surface:
| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<product>` | - | Yes | - | Product, feature, or platform to document |
| `--tier` | `-t` | No | Auto | `lightweight`, `standard`, `heavyweight` |
| `--resume` | `-r` | No | `false` | Resume from existing task file |
| `--output` | `-o` | No | Auto | Output path for final PRD |
| `--scope` | `-s` | No | Auto | `product` or `feature` (PRD scope classification) |
| `--focus` | `-f` | No | All | Comma-separated directories/subsystems to focus on |
| `--purpose` | `-p` | No | - | What this PRD is for (engineering planning, investor materials, etc.) |

**Trade-offs**: Slightly more work, but formalizes implicit parameters that are currently buried in the SKILL.md's Input section. Matches the adversarial command pattern precisely.

### Option C: Heavy Command (~180+ lines)

Includes inline tier selection table, full prompt examples, and the "What to Do If Prompt Is Incomplete" template.

**Trade-offs**: Pushes too much content into the command. The tier table and prompt completeness template are behavioral protocol content (they guide the skill's A.2 triage logic), not pure interface concerns.

### Option D: Two Commands (prd.md + prd-update.md)

Separate command for updating an existing PRD (lines 1361-1373 of SKILL.md).

**Trade-offs**: Over-splitting. The update flow is a minor variant, not a distinct command. A `--update` flag on the main command suffices.

### Recommendation: Option B

A ~130-150 line command file at `commands/sc/prd.md` with explicit flags for tier, resume, output, scope, focus, and purpose. This follows the adversarial gold standard precisely.

**What moves from SKILL.md to command:**
1. **Effective Prompt Examples** (lines 46-60) → Examples section of command
2. **"What to Do If Prompt Is Incomplete" template** (lines 62-73) → Behavioral Summary or command-level note (brief version — the full template stays in SKILL.md A.2 for protocol use)
3. **Tier Selection table** (lines 79-92) → Options section description for `--tier` flag (brief summary; detailed selection logic stays in SKILL.md A.3/A.6)

**What stays in SKILL.md:**
1. The 4-input description (lines 35-44) — the SKILL needs this for A.2 parsing
2. Tier selection rules (the logic, not the table) — behavioral protocol
3. Output Locations full table — execution context

**Activation section:**
```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill prd

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.
```

**Naming for Skill invocation**: `Skill prd` (not `Skill sc-prd-protocol`) — see Dimension 3 for full naming analysis.

**Confidence**: High
**Impact on existing spec**: Requires a new FR (FR-PRD-R.0) for the command file. Line count estimates for SKILL.md (FR-PRD-R.1) decrease slightly as ~20-30 lines of prompt examples move to the command.

---

## Dimension 2: Skill Body Decomposition

### Current State

The existing spec decomposes SKILL.md into 5 files (SKILL.md + 4 refs/). The refs were partially created but SKILL.md was never trimmed. Let me validate the decomposition.

### Analysis of Current Line Budget

**Behavioral blocks staying in SKILL.md (per fidelity index):**

| Block | Lines | Content |
|-------|-------|---------|
| B01: Frontmatter | 4 | Frontmatter |
| B02: Header + Process | 25 | Purpose, how it works, why |
| B03: Input Section | 42 | Input parameters + examples + incomplete prompt template |
| B04: Tier Selection | 19 | Table + selection rules |
| B05: Output Locations | 32 | Variable block + artifact table |
| B06: Execution Overview | 30 | Stage A/B overview |
| B07: Stage A — A.1-A.3 | 97 | Check existing, parse/triage, scope discovery |
| B08: Stage A — A.4 | 43 | Research notes file template |
| B09: Stage A — A.5 | 24 | Sufficiency gate |
| B10: Stage A — A.6 | 17 | Template triage |
| B12: A.7 Spawning + A.8 | 18 | Builder spawn instruction + verification |
| B13: Stage B | 23 | Delegation protocol |
| B28: Critical Rules | 39 | 16 non-negotiable rules |
| B29: Quality Signals | 30 | Strong/weak/when-to-spawn |
| B30: Artifact Locations (dup) | 21 | Near-duplicate of B05 → merge |
| B31: Session Management | 11 | Resume instructions |
| B32: Updating PRD | 13 | Update flow |
| **Total** | **~488** | **Without B30 dedup: ~467** |

With the command layer absorbing ~20-30 lines of prompt examples (B03 partial), the SKILL.md drops to **~437-447 lines** — comfortably under 500.

### Option A: Keep 4 refs/ (Current Spec)

4 files as specified: agent-prompts.md, build-request-template.md, synthesis-mapping.md, validation-checklists.md.

**Trade-offs**: Already validated in the spec. Groupings follow usage phase. Agent prompts are all loaded together during A.7. Validation content all loaded together during A.7 (by builder).

### Option B: Split agent-prompts.md into 2 files

`refs/codebase-agent-prompts.md` (Codebase Research + Doc Analyst + Integration + UX + Architecture — all Phase 2) and `refs/qa-agent-prompts.md` (Research Analyst + Research QA + Synthesis QA + Report Validation + Assembly — Phases 3/5/6).

**Trade-offs**: The builder loads ALL agent prompts during A.7 regardless of phase, because it needs to embed them all in the task file at construction time. Splitting would force the builder to load 2 files instead of 1 for the same purpose. No token savings. Added complexity for no benefit.

### Option C: 5 refs/ (add output-structure.md)

Separate the PRD section outline (B22, ~117 lines) from the synthesis mapping table (B23, ~19 lines) into its own file.

**Trade-offs**: The output structure and synthesis mapping are semantically coupled (the mapping references the structure). Splitting them apart makes the builder load 2 refs instead of 1. Marginal complexity increase, no meaningful benefit.

### Option D: 3 refs/ (merge build-request into SKILL.md)

Keep the BUILD_REQUEST inline in SKILL.md and only extract 3 refs.

**Trade-offs**: BUILD_REQUEST is 165 lines of template content only needed at A.7. Keeping it inline pushes SKILL.md to ~600+ lines, violating the 500-line ceiling. The spec correctly identifies it as a separate ref.

### Should Stage A content move to refs/?

Stage A (B07-B10) is ~181 lines of behavioral protocol. It MUST stay in SKILL.md because:
1. It's WHAT/WHEN content (scope discovery behavioral flow), not HOW content
2. It's needed immediately on invocation (before any refs are loaded)
3. Moving it would require loading a ref at the start of every invocation, defeating lazy loading

The BUILD_REQUEST (B11, ~165 lines) is the only Stage A content that correctly moves to refs/ — it's a HOW template, not behavioral protocol.

### Recommendation: Option A (4 refs/, as-is)

The existing spec's 4-file decomposition is correct. The groupings are optimal. No changes needed to the refs/ structure.

**With the command layer added**, the line budget math improves:
- SKILL.md: ~437-447 lines (B03 partially moves to command, B30 deduped into B05)
- refs/agent-prompts.md: ~415 lines (already exists at 422 lines)
- refs/build-request-template.md: ~165 lines (not yet created)
- refs/synthesis-mapping.md: ~137 lines (already exists at 142 lines)
- refs/validation-checklists.md: ~127 lines (already exists at 153 lines)

**Confidence**: High
**Impact on existing spec**: Minimal — the 4-file decomposition stands. FR-PRD-R.1 line count targets shift slightly downward (~437-447 vs 430-480) due to content moving to command.

---

## Dimension 3: Naming Convention

### Current State

- Skill directory: `.claude/skills/prd/` (no `sc-` prefix)
- Skill name in frontmatter: `prd`
- Invocation: `Skill prd`
- No command file exists

### Option A: Keep `prd/` — **Recommended**

Keep the current directory name. Create the command as `commands/sc/prd.md`. The command's activation section says `Skill prd`.

**Analysis**: The Developer Guide Section 5.7 says: "Skills prefixed with `sc-` have a special relationship with commands" and "skills without the `sc-` prefix (like `confidence-check`) are standalone utilities invocable by any command or agent."

The PRD skill is BOTH user-facing (invoked via `/prd`) AND a utility that other skills could invoke (e.g., `/sc:workflow` could orchestrate a PRD creation). The `sc-` prefix would lock it into the "protocol backing a specific command" pattern and make it less portable.

Precedent: The existing `prd/` and `tdd/` skills are standalone utilities. The `sc-adversarial-protocol/` skill is explicitly a protocol backing only the `/sc:adversarial` command.

**Trade-offs**: Clean, minimal change. Consistent with existing `prd/` and `tdd/` naming. The command at `commands/sc/prd.md` provides the user-facing entry point; the skill's name doesn't need to change.

### Option B: Rename to `sc-prd-protocol/`

Matches the `sc-adversarial-protocol/` pattern exactly. Command activation: `Skill sc-prd-protocol`.

**Trade-offs**: Requires renaming the directory, updating the frontmatter `name` field, updating any cross-references (spec, fidelity index, BUILD_REQUEST), and verifying `make sync-dev` handles the rename. More work for cosmetic alignment. Reduces skill portability.

### Option C: Rename to `sc-prd/`

Shorter, matches `sc-task-unified/`.

**Trade-offs**: Same rename overhead as Option B. The `-protocol` suffix adds nothing for a skill that's both utility and protocol.

### Option D: Rename to `prd-protocol/`

Hybrid — keeps the utility flavor, adds protocol suffix.

**Trade-offs**: Doesn't match any existing convention. Neither `sc-` nor standalone.

### Recommendation: Option A (keep `prd/`)

No rename. The command file at `commands/sc/prd.md` with `Skill prd` activation is sufficient. The PRD skill is a dual-purpose utility (invocable by users and by other skills). The `sc-` prefix convention is for protocol skills that exclusively back a single command.

**If renamed, files needing update:**
- `SKILL.md` frontmatter `name` field
- Existing spec (`.dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md`) — all references to `prd/`
- Fidelity index — all destination paths
- BUILD_REQUEST's SKILL CONTEXT FILE paths
- `make sync-dev` → `src/superclaude/skills/` directory
- Framework registration files (COMMANDS.md, ORCHESTRATOR.md if they exist)

Since we recommend NO rename, none of this is needed.

**Confidence**: High
**Impact on existing spec**: None — the spec already uses `prd/` naming.

---

## Dimension 4: What Can Move to the Command Layer

### Block-by-Block Analysis

#### B03: Input Section (lines 33-73, 42 lines)

This block contains three distinct sub-blocks:

**Sub-block 1: 4-input description (lines 34-44, ~11 lines)**
- What: WHAT/WHY/WHERE/OUTPUT parameters
- Verdict: **BOTH** — Brief version in command's Arguments section, full version stays in SKILL.md for A.2 parsing

**Sub-block 2: Effective Prompt Examples (lines 46-60, ~15 lines)**
- What: 4 strong examples, 2 weak examples with explanations
- Verdict: **COMMAND** — These are usage examples, the command's Examples section territory. Remove from SKILL.md. The skill doesn't need prompt examples to execute; it uses the A.2 triage logic.

**Sub-block 3: "What to Do If Prompt Is Incomplete" template (lines 62-73, ~12 lines)**
- What: Template for asking user to clarify vague requests
- Verdict: **SKILL** — This is behavioral protocol (A.2 triage). The skill needs this template to decide when and how to ask for clarification. A brief note in the command's Behavioral Summary can mention that vague prompts trigger clarification, but the actual template stays in the skill.

#### B04: Tier Selection (lines 75-93, 19 lines)

**Sub-block 1: Tier table (lines 79-85, ~7 lines)**
- What: Lightweight/Standard/Heavyweight table with when/agents/lines
- Verdict: **COMMAND** — This is the `--tier` flag's reference documentation. Move to Options section as a brief table.

**Sub-block 2: Selection rules (lines 87-92, ~6 lines)**
- What: Decision logic ("if in doubt pick Standard", "if user says detailed → Heavyweight")
- Verdict: **SKILL** — Behavioral protocol for A.3/A.6 tier selection logic. The command just provides the flag; the skill decides.

#### B05: Output Locations (lines 95-126, 32 lines)

- What: Variable reference block + full artifact location table
- Verdict: **SKILL** — Execution context needed by Stage A. The command can include a brief note ("Artifacts go to `.dev/tasks/to-do/TASK-PRD-*/`") but the full variable block and table stay in the skill.

### Summary of Content Migration

| Content | Lines | From | To | Net effect on SKILL.md |
|---------|-------|------|----|------------------------|
| Effective Prompt Examples | ~15 | B03 in SKILL.md | Command Examples | -15 lines |
| Tier Selection table | ~7 | B04 in SKILL.md | Command Options | -7 lines (keep selection rules) |
| Brief 4-input description | ~11 | B03 in SKILL.md | Command Arguments | 0 (stays in both; command gets brief version) |
| "Prompt Is Incomplete" template | ~12 | B03 in SKILL.md | stays in SKILL.md | 0 |
| Output Locations | ~32 | B05 in SKILL.md | stays in SKILL.md | 0 |

**Net SKILL.md reduction from command layer**: ~22 lines

This brings the SKILL.md estimate from ~467 (post-B30 dedup) to ~445 lines.

### Recommendation

Move the Effective Prompt Examples and the Tier Selection table to the command file. Keep the 4-input description (brief in command, full in skill), the incomplete prompt template, the tier selection rules, and the full output locations table in SKILL.md.

**Confidence**: High
**Impact on existing spec**: The fidelity index B03 and B04 destination entries need updating to show partial migration to command. FR-PRD-R.1 line target decreases by ~22 lines.

---

## Dimension 5: Complexity & Risk Rating

### Complexity Score: 0.40

| Factor | Score | Rationale |
|--------|-------|-----------|
| Files changed | 0.3 | 1 new file (command), 1 edited file (SKILL.md), 1 new ref (build-request-template.md). Refs already partially exist. |
| Cross-references | 0.5 | BUILD_REQUEST has ~7 section references that need path updates. Well-documented in existing spec's cross-reference map. |
| Content migration complexity | 0.3 | Mostly verbatim removal from SKILL.md (content already exists in refs/). BUILD_REQUEST is the only new ref to create. |
| New files created | 0.4 | 2 new files: command file (from scratch) + build-request-template.md (extract from SKILL.md). Command is templated from adversarial. |
| Behavioral change risk | 0.1 | Zero behavioral change. Reorganization only. |
| **Weighted average** | **0.40** | |

### Risk Assessment

| Risk Category | Rating | Detail |
|---------------|--------|--------|
| **Content loss** | LOW | Agent prompts, synthesis mapping, and validation checklists already exist in refs/ files. The only new extraction is BUILD_REQUEST (~165 lines) which is a contiguous block. Fidelity index provides first/last 10-word markers for verification. |
| **Cross-reference breakage** | LOW-MEDIUM | 7 well-documented references in BUILD_REQUEST need updating from section names to refs/ paths. The cross-reference map in the existing spec (Section 12.2) lists every one. Grep after implementation catches stragglers. |
| **Naming collision** | NONE | Keeping `prd/` directory name. No rename. |
| **Regression risk** | LOW | The skill's execution behavior is identical — same phases, same agents, same prompts. Only the file organization changes. The `/task` skill reads the task file (created at A.7), not SKILL.md or refs/ directly. |
| **Scope creep** | MEDIUM | The command layer is genuinely NEW work (not just reorganization). Temptation to also improve prompt examples, add new flags, or polish content. Mitigation: strict scope boundary — verbatim migration + new command file only. |
| **Fidelity drift** | MEDIUM | When removing content from SKILL.md, the implementer might "improve" wording, reformat tables, or fix typos they notice. Mitigation: diff against original to verify zero-change on migrated content. |

### Effort Estimate

| Metric | Estimate |
|--------|----------|
| Files in final state | 6 total: `commands/sc/prd.md` (NEW), `skills/prd/SKILL.md` (EDITED), `skills/prd/refs/agent-prompts.md` (EXISTS, verify), `skills/prd/refs/build-request-template.md` (NEW), `skills/prd/refs/synthesis-mapping.md` (EXISTS, verify), `skills/prd/refs/validation-checklists.md` (EXISTS, verify) |
| Total lines across all files | ~1,010-1,060 (command ~140 + SKILL.md ~445 + refs ~422+165+142+153 = ~882 in refs). Note: refs are larger than SKILL.md, which is correct — the HOW content is the bulk. |
| Single session? | Yes — this is a ~2 hour task. The hardest part is creating the command file from scratch; the rest is content removal and verification. |
| Optimal implementation order | 1. Create command file → 2. Create build-request-template.md → 3. Trim SKILL.md (remove moved content, add loading declarations, merge B30 into B05) → 4. Verify refs/ content matches original → 5. Fidelity audit → 6. `make sync-dev` + `make verify-sync` |

### Complexity Class: MEDIUM (unchanged from existing spec)

---

## Dimension 6: Gaps in the Existing Spec

The existing spec at `.dev/releases/complete/v3.65-prd-refactor/prd-refactor-spec.md` is thorough for the refs/ decomposition but has **one critical gap**: it completely omits the thin command layer.

### Gap 1: No Command File FR (CRITICAL)

**What's missing**: No functional requirement for creating `commands/sc/prd.md`. The spec's scope boundary (Section 1.2) explicitly says "Modifying any files outside the `prd/` skill directory" is out of scope, which excludes the command file.

**Impact**: The refactored skill would still violate the Developer Guide's three-tier architecture mandate. The spec solves the "monolithic SKILL.md" anti-pattern but not the "skill without command layer" anti-pattern.

**Required additions**:
- New FR-PRD-R.0: Create `commands/sc/prd.md` (~130-150 lines) with flags, usage, examples, boundaries, and activation section
- Expand scope boundary to include `commands/sc/prd.md`
- Update Architecture Section 4.1 to include the command file
- Update Section 4.4 dependency graph to show command → skill → refs/ three-tier chain

### Gap 2: FR-PRD-R.1 Line Count Shifts

**What changes**: With the command layer absorbing ~22 lines of interface content (prompt examples + tier table), the SKILL.md target shifts from 430-480 to ~420-450.

**Required revision**: Update FR-PRD-R.1 acceptance criteria line range.

### Gap 3: Fidelity Index Missing B03/B04 Split

**What changes**: B03 (Input Section) now splits: prompt examples → command, the rest stays. B04 (Tier Selection) now splits: table → command, rules → stay.

**Required additions**:
- Fidelity index needs new entries for the command-bound content
- B03 destination changes from "SKILL.md (Input section)" to "SKILL.md (partial) + commands/sc/prd.md (Examples)"
- B04 destination changes similarly

### Gap 4: Missing Test Coverage for Command

**Required additions to Test Plan**:
- **Structural test**: Command file exists at `commands/sc/prd.md`, line count 100-170
- **Activation test**: Command contains `## Activation` section with `Skill prd`
- **Flag parsing test**: Command documents `--tier`, `--resume`, `--output`, `--scope`, `--focus`, `--purpose` flags
- **Boundary test**: Command has `## Boundaries` with Will/Will Not sections
- **Integration test**: Invoking `/sc:prd <product>` triggers the command, which activates the skill

### Gap 5: Architecture Section Missing Command Tier

**What changes**: Section 4.1 (New Files) and Section 4.4 (Dependency Graph) only show the skill + refs/ tier. Need to add:

```
commands/sc/prd.md (thin command, ~140 lines)
  |
  v [Activation: Skill prd]
skills/prd/SKILL.md (behavioral protocol, ~445 lines)
  |
  +-- [Stage A.7] --> refs/build-request-template.md
  |                     +-- references --> refs/agent-prompts.md
  |                     +-- references --> refs/synthesis-mapping.md
  |                     +-- references --> refs/validation-checklists.md
  |
  +-- [Stage B] --> /task skill
```

### Gap 6: Spec Scope Boundary Too Narrow

The spec's "Out of scope" says: "Modifying any files outside the `prd/` skill directory" and "Changing the PRD skill's external interface (command invocation, inputs, outputs)."

Creating a command file IS changing the external interface (adding a standardized entry point). The scope boundary needs to be expanded to include:
- Creating `commands/sc/prd.md`
- Corresponding `src/superclaude/commands/prd.md` (source of truth)
- Framework registration updates if required

### Gap 7: Migration Steps Missing Command Sync

Section 9 (Migration & Rollout) lists `make sync-dev` for skills but doesn't mention syncing the command file to `src/superclaude/commands/`.

---

## Consolidated Recommendation

### The Refactoring Plan (6 Steps)

1. **Create `commands/sc/prd.md`** (~130-150 lines)
   - Modeled after `commands/sc/adversarial.md`
   - Frontmatter: name, description, category, complexity, allowed-tools, mcp-servers, personas
   - Flags: `--tier`, `--resume`, `--output`, `--scope`, `--focus`, `--purpose`
   - Examples: migrated from SKILL.md B03 (Effective Prompt Examples)
   - Tier table: migrated from SKILL.md B04 (as Options reference)
   - Behavioral Summary: one-paragraph overview of the two-stage process
   - Activation: `Skill prd`
   - Boundaries: Will (create PRDs, investigate code, research externally, validate quality) / Will Not (modify source code, make architectural decisions, execute PRD recommendations)

2. **Create `refs/build-request-template.md`** (~165 lines)
   - Extract B11 (lines 344-508) verbatim from SKILL.md
   - Update SKILL CONTEXT FILE references from section names to refs/ paths per cross-reference map
   - Add a brief header explaining purpose and loading context

3. **Trim SKILL.md** (1,369 → ~445 lines)
   - Remove B11 (BUILD_REQUEST, ~165 lines) — replaced by loading declaration pointing to `refs/build-request-template.md`
   - Remove B14-B21 (Agent Prompt Templates, ~415 lines) — already in `refs/agent-prompts.md`
   - Remove B22-B23 (Output Structure + Synthesis Mapping, ~137 lines) — already in `refs/synthesis-mapping.md`
   - Remove B24-B27 (Checklists + Assembly + Content Rules, ~147 lines) — already in `refs/validation-checklists.md`
   - Remove B03 prompt examples (~15 lines) — moved to command file
   - Remove B04 tier table (~7 lines) — moved to command file
   - Merge B30 into B05 (deduplicate artifact locations, append QA-specific paths)
   - Add loading declarations at A.7 section

4. **Verify existing refs/** — Diff `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` against original SKILL.md line ranges to confirm fidelity

5. **Fidelity audit** — Run structural tests (line counts), cross-reference tests (no stale section references), and content tests (diff verification)

6. **Sync** — `make sync-dev` + `make verify-sync` to propagate all changes to `src/superclaude/`

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Command file | YES — create `commands/sc/prd.md` | Developer Guide mandate; every skill needs a command |
| Directory rename | NO — keep `prd/` | Dual-purpose utility pattern; `sc-` prefix is for protocol-only skills |
| Number of refs/ | 4 (unchanged from spec) | Groupings follow usage phase; builder loads all at once |
| Stage A in SKILL.md | YES — all behavioral | WHAT/WHEN content needed immediately on invocation |
| BUILD_REQUEST to refs/ | YES — separate file | ~165 lines of HOW template, only needed at A.7 |
| Content migration | Verbatim except B03/B04 partial moves to command | Zero fidelity drift on core content |

---

## Complexity/Risk Scorecard

| Metric | Rating |
|--------|--------|
| **Overall Complexity** | **0.40** (MEDIUM) |
| **Content Loss Risk** | LOW |
| **Cross-Reference Breakage Risk** | LOW-MEDIUM |
| **Naming Collision Risk** | NONE |
| **Regression Risk** | LOW |
| **Scope Creep Risk** | MEDIUM |
| **Fidelity Drift Risk** | MEDIUM |
| **Estimated Effort** | Single session, ~2 hours |
| **Files Created** | 2 (command file + build-request-template.md) |
| **Files Modified** | 1 (SKILL.md trimmed) |
| **Files Verified** | 3 (existing refs/) |
| **Total Files in Final State** | 6 |
| **Can Complete in Single Session** | YES |

### Spec Revision Required

The existing spec needs these updates before implementation:
1. **Add FR-PRD-R.0** for the command file
2. **Expand scope boundary** to include `commands/sc/prd.md`
3. **Update FR-PRD-R.1** line targets (420-450 vs 430-480)
4. **Update Architecture 4.1** with command file
5. **Update Architecture 4.4** dependency graph to three-tier
6. **Update fidelity index** B03/B04 with split destinations
7. **Add test coverage** for command (structural, activation, flags, boundaries)
8. **Update Migration 9** with command sync steps

These are additive changes — the existing spec's refs/ decomposition is correct and unchanged.
