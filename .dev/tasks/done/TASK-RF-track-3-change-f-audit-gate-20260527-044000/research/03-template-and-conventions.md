# Research Output 03 — Template & Conventions (Change F)

**Date:** 2026-05-27
**Researcher:** template-conventions (Track 3)
**Status:** Complete
**Scope:** MDTM Template 02 fit assessment, Makefile sync/verify conventions, pre-commit hook conventions, skill-body subsection conventions, Change B precedent.

---

## Section 1: Template Selection — Template 02 (Complex)

**Selected template:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines total; Part 1 instructions L1-805, Part 2 task scaffold L806-1205).

**Why Template 02 fits Change F (and Template 01 does not):**

Template 02 extends Template 01 with **Section L: Intra-Task Handoff Patterns** (L711-805). Per the template's own statement at L713-716: "This section defines patterns for complex tasks where checklist items need to pass information to later items via artifact files. These patterns enable discovery, testing, review, conditional logic, and aggregation within a single task file."

Change F is not a single self-contained insertion (which would warrant Template 01, the path Change B took). Change F requires **discovery before execution** across at least five independent unknowns:

1. **Insert anchor inside Wave 3** — must be discovered by reading the current SKILL.md (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:230-282`); the proposal's "after the calibrator dispatch step" wording maps to a line range that needs byte-level resolution.
2. **Audit-log conventions** — the existing skill body references an `audit.log` at L108-121 (Wave 0 opens it) and various waves emit to it; the new gate adds `calibration: missing` entries. The append format must be inferred from existing usage before the gate can write to it.
3. **Retry semantics for the calibrator subagent** — the spec says "2-minute extended timeout (one retry only)"; the existing skill's calibrator dispatch at L263 (`spawn N confidence-calibrator instances in parallel ... with card_tier=2 and output_path=...`) does NOT currently specify per-spawn timeouts. The retry instruction has to land in a way that compiles with the existing Task-tool invocation pattern.
4. **Force-degrade math** — `min(self_reported, 0.65)` with `calibration_status: failed_to_calibrate` annotation requires knowing the REPORT.md template structure (`refs/report-template.md`) to identify where the annotation slots in, and the existing confidence handling in Wave 5 step 2 (`SKILL.md:319-329`) to confirm the math composes cleanly.
5. **Glob-vs-Bash verification approach** — the spec uses Glob-style semantics ("for every `tier2-h<N>-*.md` card") but also names a Bash "Verification command (run before publishing)". The orchestrator must pick the approach consistent with the existing skill's filesystem-verification idiom.

These discoveries map directly to Template 02 patterns:

| Template 02 Pattern | L# | How Change F uses it |
|---|---|---|
| **L1 Discovery item** | 737-747 | Phase 1 discovery items: capture current Wave 3 byte state at the insertion anchor; locate `audit.log` writer pattern; locate REPORT.md schema. Output: `phase-outputs/discovery/*.md` consumed by Phase 2 build items. |
| **L2 Build-from-discovery** | 749-759 | Phase 2 item that performs the Edit on SKILL.md, reading both the discovery file (which gives the unique `old_string` context) AND the spec extraction (`research/01-change-f-spec-extraction.md`) for the verbatim new content. |
| **L4 Review/QA** | 773-783 | Phase 3 structural review: confirm gate is INSIDE Wave 3, references resolve, MUST/MUST NOT wording matches the spec. PASS/FAIL verdict. |
| **L5 Conditional-action** | 785-797 | If markdownlint `--fix` modifies the file, branch to re-sync; if structural review fails, branch to fix cycle. |

Template 01 (simple/atomic) does not provide L's handoff scaffolding, so it cannot express the "discover-then-build" flow without inventing patterns. Change B used Template 01 cleanly because its five insertion blocks were already pinned to specific anchors in the spec — no discovery needed.

**SECTIONS REQUIRED PER TEMPLATE 02 (Section D, L233-273):**

- Frontmatter (all 30+ fields per L1-44 of template).
- `## MANDATORY WORKFLOW COMPLIANCE` (informational; D1 L238-246) — applies when a governing workflow doc exists; for Change F the governing doc is the cross-env proposal, so include it as informational.
- `## Cross-Stage Integration Requirements` (informational; D2 L247-267).
- **NO checklist items before Phase 1** (D3 L269-273). All actions appear inside Phase 1+ as `- [ ]` items.
- `## Post-Completion Actions` (per I13 L580-585 + I17 L626-635) — final task items only: rf-qa structural validation, rf-qa-qualitative operational validation, frontmatter status→Done update.
- `## Task Log / Notes` at the bottom with `### Phase N Findings` subsections for blocker logging (per J1 L659-663).

**SELF-CONTAINED CHECKLIST DISCIPLINE (Section B, L130-196):**

Every `- [ ]` item must be a **single paragraph** that embeds: (1) context reference with why, (2) action with why, (3) output spec, (4) integrated "ensuring..." verification clause, (5) blocker-log fallback, (6) explicit completion gate. Forbidden: standalone "read context" items, multi-line/bulleted checklist items, separate verification items, parent-before-children patterns.

---

## Section 2: Sync-Dev + Verify-Sync Workflow (Verbatim Makefile)

**Target file:** `Makefile` (repository root). Two targets define the source-of-truth mirror:

### 2.1 `sync-dev` target — `Makefile:109`

Header comment at `Makefile:108`: `# Sync src/superclaude/{skills,agents} → .claude/{skills,agents} for local dev`.

Behavior (L109-163):
- Prints `🔄 Syncing src/superclaude/ → .claude/ for local development...` (L110).
- Walks `src/superclaude/skills/*/` (L112): for each directory whose basename does NOT start with `__` (skipping `__init__.py` / `__pycache__`), if `SKILL.md` or `skill.md` exists, mirrors every non-`__init__.py` non-`__pycache__` file into `.claude/skills/<skill_name>/` preserving subdirectory structure (L114-124). **This means edits under `src/superclaude/skills/sc-troubleshoot-protocol/` — including `SKILL.md` itself — propagate to `.claude/skills/sc-troubleshoot-protocol/SKILL.md`.**
- Mirrors agents from `src/superclaude/agents/*.md` → `.claude/agents/` (L126-130), skipping `README.md`.
- Mirrors commands from `src/superclaude/commands/*.md` → `.claude/commands/sc/` (L131-136).
- Mirrors hooks from `src/superclaude/hooks/scripts/*.sh` → `.claude/hooks/` with `chmod +x` (L137-143).
- Mirrors templates from `src/superclaude/templates/` → `.claude/templates/` (L148-157).
- Final stdout: `✅ Sync complete.` followed by per-component counts (Skills, Agents, Commands, Hooks, Templates) (L158-163).

Exit code: 0 on success. The target uses `@`-prefixed lines (silent) and shell `for` loops; failures inside the loops would surface via shell error propagation but the target as written does not `set -e`, so an individual `cp` failure would not fail the build. **Operational invariant:** after `make sync-dev` exits 0, every `src/superclaude/skills/<name>/**` file has a byte-identical mirror at `.claude/skills/<name>/**`.

### 2.2 `verify-sync` target — `Makefile:166`

Header comment at `Makefile:165`: `# Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)`.

Behavior (L166-301; spans skills, agents, commands, hooks, templates):
- Prints `🔍 Verifying src/superclaude/ ↔ .claude/ sync...` (L167).
- Sets local `drift=0` and prints `=== Skills ===` (L168, L170).
- For each `src/superclaude/skills/*/` (L171): if `.claude/skills/<name>/` is missing, prints `❌ MISSING in .claude/skills/: <name>` and sets `drift=1` (L174-176); otherwise runs `diff -rq --exclude='__init__.py' --exclude='__pycache__'` between the two trees (L178). Any output from diff prints `⚠️  DIFFERS: <name>` with the indented diff output and sets `drift=1` (L179-183). Clean directories print `✅ <name>` (L184).
- **Reverse check** at L188-199: every `.claude/skills/*/` without a corresponding `src/superclaude/skills/<name>/` is flagged either as "no SKILL.md — not a skill, must not live in .claude/skills/" (L193-194) or "MISSING in src/superclaude/skills/: <name> (not distributable!)" (L196).
- Agents (L202-226), Commands (L228-252), Hooks (L254-278), Templates (L280-end) follow the same bidirectional pattern.
- Final exit: prints `❌ Drift detected! Run 'make sync-dev' to fix...` and exits 1 if `drift=1`; prints `✅ All components in sync` and exits 0 otherwise (per the Change B execution log at L267 which observed this exact success line).

**Operational invariant:** `make verify-sync` exits 0 iff `make sync-dev` has been run since the last edit to `src/superclaude/`. **Order matters: sync-dev MUST precede verify-sync** — running verify-sync first after a `src/` edit will fail with `DIFFERS`.

---

## Section 3: Markdownlint Hook (`.pre-commit-config.yaml:70-82`)

Block declaration at `.pre-commit-config.yaml:70-82`:

- **L70 comment:** `# Markdown linting`
- **L71 repo:** `https://github.com/igorshubovych/markdownlint-cli`
- **L72 rev:** `v0.38.0`
- **L73 hooks:** list start
- **L74 id:** `markdownlint`
- **L75 args:** `['--fix']` — **the hook AUTO-MODIFIES the file** when fixable violations are present. The first pass exits non-zero with `files were modified by this hook`; the next pass on the already-fixed file exits 0.
- **L76-82 exclude:** verbose regex excluding `CHANGELOG.md`, any path containing `node_modules`, any `*.min.md`, and `\.dev/.*`. **Implication for Change F:** the target file `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` is NOT in `.dev/`, so it IS subject to markdownlint. The task file itself (under `.dev/tasks/to-do/`) is excluded.

**Invocation pattern used by Change B (precedent from execution log L268):** `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` returned `Passed` (exit 0); no `--fix` modifications were applied that pass. Change F can use the same invocation against `SKILL.md`. The `uv run` prefix is required because pre-commit may not be on PATH in worktrees — Change B's deviations log records this (L275).

---

## Section 4: `block-claude-generated-mirrors` Hook (`.pre-commit-config.yaml:102-109`) + Source-of-Truth Rule

Block declaration at `.pre-commit-config.yaml:98-109`:

- **L98-101 comment:** `# AC11 / R-017 / T01.20 — source-of-truth discipline gate`; "Rejects generated `.claude/` mirrors on the commit path. Full mirror drift remains available via `make verify-sync`, but pre-commit must not require staging generated mirrors when this repository edits its own src/ sources."
- **L102 repo:** `local`
- **L104 id:** `block-claude-generated-mirrors`
- **L105 name:** `Block generated .claude mirror commits (AC11)`
- **L106 entry:** `scripts/precommit_block_claude_mirrors.sh`
- **L107 language:** `script`
- **L108 pass_filenames:** `false`
- **L109 files:** `'^\.claude/(skills|agents|commands|hooks|templates)/'` — the hook fires only for staged paths under those five subdirectories of `.claude/`.

**Operational implication for Change F:** if a researcher or executor accidentally stages a `.claude/skills/sc-troubleshoot-protocol/SKILL.md` mirror (e.g., via `git add -A .` or `git add .claude/`), this hook blocks the commit. The fix is to stage the `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` source file only; the mirror lives in `.claude/` for local dev but is `.gitignore`d.

**Source-of-truth rule (per CLAUDE.md and memory `feedback_claude_dir_gitignored.md`):**

> Never edit `~/.claude/` or `<project>/.claude/` directly. Edit `src/superclaude/` then `make sync-dev`. If `git add` needs `-f` for `.claude/*`, STOP.

Per `.gitignore` semantics + the memory note, only `.claude/settings.json` is tracked in this repo; `.claude/skills`, `.claude/agents`, `.claude/commands`, `.claude/hooks`, `.claude/templates` are sync-dev output and are gitignored. Change F editor MUST edit `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (NOT the `.claude/` mirror).

---

## Section 5: Skill-Body Subsection Conventions (`sc-troubleshoot-protocol/SKILL.md` self-consistency + cross-skill spot-check)

### 5.1 Heading conventions

From `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (456 lines total):

- **`##` (level 2)** used for top-level sections: `## Purpose` (L16), `## Required Input (STOP if missing)` (L26), `## Output Contract` (L37), `## Wave Structure` (L73).
- **`### Wave N: ...`** (level 3) used for each wave header: `### Wave 0: Parse + Validate Input` (L91), `### Wave 1: Tier 1 — Real-Code Grounding` (L129), `### Wave 1.5: Documentation Grounding` (L152), `### Wave 1.7: Tier 1 — Hypothesis Formation` (L190), `### Wave 2: Confidence Gate` (L210), `### Wave 3: Tier 2 — Parallel Hypotheses` (L230), `### Wave 4: Tier 2 — Adversarial Fix Debate` (L283), `### Wave 5: Synthesis + Report` (L312), `### Wave 6: Tier 3 — Remediation Chain` (L359).
- **`####`** (level 4) is NOT used inside Wave bodies in this file. Subsections inside a Wave use **bolded paragraph headers** (e.g., `**Goal**:`, `**Preconditions**:`, `**Steps**:`, `**Exit criteria**:`, `**Failure handling**:`, `**Skip conditions**:`) rather than further heading nesting.

Cross-skill spot check: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1491 lines) uses `##` for top-level sections, `###` for numbered subsections (`### 4.1 Parse Roadmap Items` etc.), AND `####` for nested algorithm subsections (`#### 5.2.1 Effort mapping (deterministic)` at L492). So `####` IS acceptable when needed for deep nesting, but the troubleshoot SKILL.md does NOT currently use it.

**Implication for Change F's new gate subsection:** the natural fit is to add a `**bolded paragraph header**` block INSIDE Wave 3 (after step 3.5 calibrator dispatch, before step 4 cluster-and-distill), parallel to the existing `**Exit criteria**:`, `**Failure handling**:` blocks. The spec at proposal L374-401 already uses the `**Calibration completeness gate (hard precondition for report publishing)**` framing as a bolded header — researcher 02 should confirm this fits Wave 3's existing layout, but the bolded-paragraph-header convention is the right level.

Alternative: a new `**Pre-publication audit gate**:` subsection could be promoted to `#### Audit gate` (level 4) for stronger structural emphasis — this is consistent with sc-tasklist-protocol's L492 usage and might be preferable given the gate enforces an orchestrator obligation. Either form is conventionally valid; researcher 04 (wave3-integration) should make the final call based on the exact anchor.

### 5.2 Embedded code-block conventions

- The troubleshoot SKILL.md has **6 fence delimiters total** (= 3 fenced code blocks), and **NONE are language-tagged**:
  - L75 + L85: plain text fence wrapping the Wave Structure ASCII listing.
  - L110 + L121: plain text fence wrapping the audit-log header schema (`<!-- SC:TROUBLESHOOT:TARGET ... -->`).
  - L294 + L300: plain text fence wrapping the `Skill sc:adversarial-protocol with --compare ...` invocation.
- No bash/yaml language-tagged fences in this file. Inline `commands` use single backticks.

**Implication for Change F:** if the new gate includes a "verification command" code block (the spec includes one), follow the existing convention: **plain unfenced block (no language tag)** matching the audit-log-header and adversarial-invocation pattern. Do NOT introduce bash-tagged fences. If the command is short enough, inline single-backticks are equally valid (and used widely throughout the file at L20, L47, L83 for `refs/escalation-rubric.md`, etc.).

### 5.3 MUST / MUST NOT / NEVER phrasing patterns

Observed in `sc-troubleshoot-protocol/SKILL.md`:

- L49 (Output Contract): `Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is true; the remediation target is the test file.`
- L51 (Output Contract): `Asymmetric-cost flag — downstream automation MUST NOT auto-apply a code fix when this is true; the remediation target is the spec/docs file(s)...`
- L198 (Wave 1.7 step 1): `The hypothesis card MUST set consistency_with_docs to one of aligned | conflicts | not_applicable | no_docs_found ...`

Observed in `sc-tasklist-protocol/SKILL.md`:

- L98: `Phase files MUST use the phase-N-tasklist.md convention (canonical Sprint CLI convention). Do not emit mixed aliases unless explicitly requested.`
- L100: `Phase heading: MUST be # Phase N -- <Name> (level 1 heading, em-dash separator, name <= 50 chars).`
- L102: `Index references: The "Phase Files" table in the index MUST contain literal filenames ...`
- L131: `... it MUST read them and use their structured content to produce more specific, actionable task decomposition.`

**Pattern:** MUST / MUST NOT appears as plain English imperatives inline within sentences, not as separate boxed callouts. MUST NOT is paired with an explicit remediation alternative (`...MUST NOT auto-apply X; the remediation target is Y`). NEVER is used more sparingly — generally for absolute prohibitions ("self-reported confidence is NEVER passed through unmodified" per the Change F spec aligns with this).

**Implication for Change F:** the spec's three required statements map cleanly:

1. `orchestrator MUST verify on disk` → fits the L198 pattern (imperative MUST on the actor).
2. `MUST NOT publish REPORT.md with the un-calibrated card's confidence` → fits the L49/L51 pattern (MUST NOT + remediation alternative).
3. `Self-reported confidence is NEVER passed through unmodified` → fits the absolute-prohibition pattern.

All three should land as plain English sentences inside the gate subsection, not as separate callouts.

### 5.4 Cross-reference patterns

- **Internal refs:** backticked paths relative to the skill dir, e.g., `refs/escalation-rubric.md` (L20, L47, L80, L83, L199), `refs/doc-discovery.md` (L78, L160, L163), `refs/hypothesis-card-template.md` (L198, L260), `refs/report-template.md` (L83, L318).
- **External refs to agents:** unbacked agent names, e.g., `root-cause-analyst` (L198), `confidence-calibrator` (L199, L263), `quality-engineer` (L240), `self-review` (L304).
- **Cross-skill refs:** `/sc:adversarial` (L285, L294) for slash-command-style invocation.
- **MCP tool refs:** `mcp__auggie__codebase-retrieval`, `mcp__serena__find_symbol`, etc. (L137, L138-140, L252-254) — full tool name in monospace.

**Implication for Change F:** the new gate's references to the audit log and REPORT.md should follow this style — backticked `audit.log`, backticked `REPORT.md` (or `<output-dir>/REPORT.md` for path-explicit form), backticked `refs/report-template.md` if a template slot is referenced.

### 5.5 Verification command conventions

The skill already uses Bash-style verification in the audit log (Wave 0 emits a machine-readable header per L108-121). There is no existing precedent for a Bash `ls`/`find` command being inline in the SKILL.md body for filesystem checks — Wave 3's existing exit criteria (L266-269) describe the check in English ("≥ 1 hypothesis card written to disk", "a `candidate-fixes.md` index file written") and leave the actual verification to the orchestrator's discretion.

**Implication for Change F:** the spec's "Verification command (run before publishing)" is best rendered as a plain English instruction listing the check (e.g., "for every `tier2-h<N>-*.md` card, the orchestrator MUST confirm the sibling `tier2-h<N>-*-calibration.md` exists on disk; failure to find one triggers the retry-then-force-degrade ladder below"). If a concrete Bash command is needed for unambiguity, render it as an unfenced backtick block matching the L110-121 audit-log-header pattern. Researcher 04 (wave3-integration) should make the final call.

---

## Section 6: Known Gotchas (cross-referenced with Change B execution log)

**G1. Sync order: `make sync-dev` MUST precede `make verify-sync`.**
Per Makefile L165-301, `verify-sync` runs `diff -rq` between `src/` and `.claude/`. If `.claude/` is stale after a `src/` edit, drift is reported and the command exits 1. Recovery: re-run `make sync-dev` then `make verify-sync`. Change B's task file at L226 ("`verify-sync` will FAIL if `sync-dev` has not yet run") and L232-234 (re-run recovery branch) encode this gotcha verbatim.

**G2. `markdownlint --fix` may modify the file → must re-sync.**
Per `.pre-commit-config.yaml:75` (`args: ['--fix']`), the hook auto-modifies fixable violations on first pass and reports `files were modified by this hook` with exit 1. The second pass on the same file (now fixed) exits 0. **If `--fix` modifies `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, the `.claude/` mirror is now stale and `make sync-dev` + `make verify-sync` MUST be re-run.** Change B's task file at L238 encodes this as "If `--fix` modifies the file (pre-commit reports `files were modified by this hook` which initially yields exit code 1), re-run `make sync-dev` and `make verify-sync` from Steps 2.1-2.2 a single time so the `.claude/` mirror reflects the lint fixes, then re-run the markdownlint command and confirm exit 0 on the second pass."

**G3. `block-claude-generated-mirrors` blocks `.claude/` paths from being committed.**
Per `.pre-commit-config.yaml:102-109`, any staged file matching `^\.claude/(skills|agents|commands|hooks|templates)/` triggers the block via `scripts/precommit_block_claude_mirrors.sh`. **Researchers/executors MUST stage only `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` and never the mirror.** If `git add` requires `-f` for any `.claude/*` path, STOP (per memory `feedback_claude_dir_gitignored.md`).

**G4. `pre-commit` may not be on PATH in worktrees — use `uv run pre-commit`.**
Change B's deviations log at L275 records: "`pre-commit` was not on PATH in this worktree. Resolved by `uv pip install pre-commit` then running via `uv run pre-commit run markdownlint --files ...`. Tool-installation step, not a content blocker." For Change F, the canonical invocation is `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`. If `uv run pre-commit` is unavailable: `uv pip install pre-commit` first.

**G5. Skill-body edits that introduce new orchestrator obligations MUST include both the obligation statement AND the failure-handling path.**

Per the existing skill's pattern at L271-279 (Wave 3 `**Failure handling**:` table), every orchestrator obligation has a documented failure-handling branch. The Change F spec at proposal L374-401 satisfies this requirement:

- **Obligation statement:** the three MUST / MUST NOT / NEVER clauses (Section 5.3 above).
- **Failure-handling path:** the 3-step retry-then-force-degrade ladder (retry once with extended timeout → if retry succeeds, use calibrated value; if retry fails, force-degrade to `min(self_reported, 0.65)` with `calibration_status: failed_to_calibrate` in REPORT.md → emit `calibration: missing` to audit.log).

Both halves must land in the inserted text. The reviewer in Phase 3 (structural review) should confirm both are present and that the failure-handling table or paragraph format matches Wave 3's existing convention.

**G6. The proposal's Diff sketch uses `+` prefix — strip before inserting.**
Per `research-notes.md` "PATTERNS_AND_CONVENTIONS" bullet 3, the proposal's verbatim insertion content is prefixed with `+` characters. Researchers must strip these to produce paste-ready text. Spec-extraction (researcher 01) is responsible for delivering `+`-stripped content; the executor pastes that content directly.

---

## Section 7: Change B Precedent — Template 01 vs Template 02 Comparison

**Change B** (executed task at `.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/`) was an **additive schema change** to a SINGLE refs/ template file with FIVE pre-pinned insertion blocks delivered verbatim by the spec. No discovery was required: every `old_string` was directly available from the spec text and the target file's pre-edit byte state. Template 01 (simple/atomic) was the right fit.

**Change F** is also an additive change to a SINGLE skill body file with ONE pre-pinned insertion block delivered verbatim by the spec — but the insertion **anchor** is not pre-pinned (the spec says "after the calibrator dispatch step" which spans multiple lines), and the insertion **integrates with multiple existing fields** (audit.log, REPORT.md, Wave 3 failure-handling table). These integration points require discovery before execution. Template 02 (complex) is the right fit.

**What is identical between Change B and Change F (re-use the same workflow verbatim):**

1. Sync-dev + verify-sync verification (Makefile L109 / L166) — same two-step gate at the end of every structural change.
2. Markdownlint hook invocation (`.pre-commit-config.yaml:70-82`) — same `uv run pre-commit run markdownlint --files <target>` pattern.
3. Source-of-truth rule (edit `src/`, never `.claude/`) — same gitignore enforcement via `block-claude-generated-mirrors`.
4. Self-contained checklist item discipline (Template 02 Section B mirrors Template 01 Section B).
5. Post-Completion Actions (rf-qa structural validation, frontmatter status→Done) — same I17 pattern.

**What is different between Change B (T01) and Change F (T02):**

| Aspect | Change B (Template 01) | Change F (Template 02) |
|---|---|---|
| Discovery phase | None — insertion anchors pre-pinned in spec | Required — anchor inside Wave 3 must be byte-resolved; audit.log + REPORT.md conventions must be inventoried |
| Section L (Handoff Patterns) | Not used | L1 Discovery + L2 Build-from-discovery + L4 Review/QA + L5 Conditional-action all in play |
| Integration-point unknowns | Zero | Five (anchor, audit log, retry semantics, force-degrade math, Glob-vs-Bash) |
| QA gates | FINAL_ONLY (executor-performed structural check) | FINAL_ONLY (same), plus Phase 3 review/QA item that PASS/FAILs the structural integration |
| Testing requirements | None (no automated harness exists for refs/) | None (no automated harness exists for skill body either — see research-notes.md TESTING_REQUIREMENTS) |
| Conditional-action items | None | One — if markdownlint `--fix` modifies file, branch to re-sync |

**Re-usable patterns from Change B's executed task file (paste-ready Bash for Change F):**

From Change B L226-238 (with paths swapped to Change F target):

- Step 2.1 sync: `make sync-dev` → expect exit 0 + `🔄 Syncing src/superclaude/ → .claude/ for local development...` in stdout + per-component success counts.
- Step 2.2 verify: `make verify-sync` → expect exit 0 + no `MISSING`/`DIFFERS` for `sc-troubleshoot-protocol` + final `✅ All components in sync`. **Recovery branch:** if drift detected, re-run sync-dev once and re-verify.
- Step 2.3 lint: `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` → expect `Passed` (exit 0). **Recovery branch:** if `--fix` modifies file, re-run sync-dev + verify-sync, then re-run lint.

---

## Summary

Template 02 (Complex MDTM) is the correct fit for Change F because the change requires **discovery before execution** across five integration-point unknowns (insert anchor inside Wave 3, audit.log conventions, retry semantics for the calibrator subagent, force-degrade math against REPORT.md schema, Glob-vs-Bash verification approach). Template 01 — used by Change B — does not provide Section L's handoff patterns (Discovery item L1 → Build-from-discovery L2 → Review/QA L4 → Conditional-action L5) needed to express the discover-then-build flow.

The sync/lint/structural-check workflow is identical to Change B's executed precedent: `make sync-dev` (Makefile:109) → `make verify-sync` (Makefile:166) → `uv run pre-commit run markdownlint --files <target>` (config at .pre-commit-config.yaml:70-82). Six gotchas carry forward verbatim, including the source-of-truth rule (edit `src/`, never `.claude/`) enforced by `block-claude-generated-mirrors` at .pre-commit-config.yaml:102-109.

The new gate subsection should land INSIDE Wave 3 of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (the file uses `##` for top-level + `### Wave N: ...` for waves + bolded paragraph headers for in-wave subsections; no `####` is currently used in this file but is conventionally valid per sc-tasklist-protocol L492 if stronger emphasis is wanted). MUST / MUST NOT / NEVER phrasing follows the existing inline-imperative pattern (no boxed callouts; MUST NOT paired with explicit remediation alternative). Code blocks use plain unfenced blocks without language tags, matching the three existing fences in the file at L75-85, L110-121, L294-300. The new gate must include BOTH the obligation statement (3 MUST/MUST NOT/NEVER clauses) AND the failure-handling path (3-step retry-then-force-degrade ladder), per the existing Wave 3 convention of pairing obligations with failure-handling tables/paragraphs.

**Key file:line citations delivered:**

- `Makefile:108` (sync-dev comment), `Makefile:109` (sync-dev target), `Makefile:165` (verify-sync comment), `Makefile:166` (verify-sync target).
- `.pre-commit-config.yaml:70-82` (markdownlint hook block), `.pre-commit-config.yaml:74` (id), `.pre-commit-config.yaml:75` (args `--fix`), `.pre-commit-config.yaml:76-82` (exclude regex including `\.dev/.*`).
- `.pre-commit-config.yaml:98-109` (block-claude-generated-mirrors block), `.pre-commit-config.yaml:106` (entry script), `.pre-commit-config.yaml:109` (files regex `^\.claude/(skills|agents|commands|hooks|templates)/`).
- `.claude/templates/workflow/02_mdtm_template_complex_task.md:711-805` (Section L handoff patterns), L737-747 (L1 Discovery), L749-759 (L2 Build-from-discovery), L773-783 (L4 Review/QA), L785-797 (L5 Conditional-action).
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:230-282` (Wave 3 body), L263 (calibrator dispatch step 3.5 — the anchor neighborhood), L271-279 (Wave 3 failure-handling table — the pattern Change F's failure path must match).
- Change B precedent: `.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/TASK-RF-20260527-022700-change-b-hypothesis-card-schema.md:226-238` (sync/verify/lint workflow), L267-268 (execution log success lines), L275 (uv pip install pre-commit deviation).
