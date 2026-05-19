# Research: Template & Examples — hook-sync-and-matcher-fix
**Topic type:** Template & Examples
**Scope:** MDTM template 02 mandatory rules, prior comparable task folders, frontmatter values, Execution Context block guidance
**Status:** Complete
**Date:** 2026-05-17
---

## 1. Template 02 Source

Location: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (lines 1-1198)
Structure: **PART 1** = orchestrator/builder instructions (Sections A–M, lines 47-870, never appears in output); **PART 2** = clean template to copy starting at `# [Task Title]` (lines 896-1197).

The task-builder MUST copy PART 2 only, replace placeholders, then strip orchestrator instruction blocks delineated by the `<!-- ╔════…╗ ORCHESTRATOR INSTRUCTION BLOCK - REMOVE THIS ENTIRE BLOCK FROM OUTPUT ╚════…╝` markers.

---

## 2. MANDATORY Rules (Verbatim, from PART 1)

### A3 — Complete Granular Breakdown (lines 91-95)
> "Break down EVERY workflow phase into atomic, verifiable checklist items. Create individual checklist items for EVERY file, component, or iteration. NO high-level or bulk operations allowed - everything must be granular. Include exact file paths, specific requirements, and measurable outcomes."

**Application to hook-sync-and-matcher-fix:** every file edit gets its own item — never "edit all 3 files," never "fix the matcher and add the test." One item per Makefile target edit, one per hooks-matcher patch site, one per pytest scenario.

### A4 — Iterative Process Structure (lines 97-116)
> "For ANY process involving multiple items (files, components, etc.): Pre-enumerate ALL items to be processed in initial step; Create individual checklist item for each specific item; Require incremental updates after each item; Include consolidation step only after all items complete."

Canonical pattern from the template:
```markdown
**Step X.1:** Scan and enumerate all [items] in [location]
- [ ] Complete [item] listing generated: [count] items identified

**Step X.2:** Process each [item] individually:
- [ ] [Item 1]: [exact identifier] - [specific action] completed
- [ ] [Item 2]: [exact identifier] - [specific action] completed

**Step X.3:** Consolidate all individual results
```

### B2 — Every Checklist Item MUST Be a Complete, Self-Contained Prompt (lines 142-148)
> Six mandatory elements:
> 1. **Context Reference with WHY** — what file(s) to read and why
> 2. **Action with WHY** — what to do and why
> 3. **Output Specification** — exact file name, location, content requirements, template
> 4. **Integrated Verification** — "ensuring..." clause; DO NOT assume, hallucinate, or make up info; 100% accuracy from source files; document negative evidence when verification fails
> 5. **Evidence on Failure Only** — log to task notes ONLY if blocked (output file IS evidence of success)
> 6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."

### B3 — One Full Paragraph (line 150)
> "Each checklist item should be written as ONE FULL PARAGRAPH (not multiple lines or bullets) that is verbose and explanatory. The item should read like a complete prompt that could be executed independently without any prior context."

### B5 — FORBIDDEN Patterns (lines 164-184) — TO AVOID
- Standalone "read context" items that produce no output (context lost across batches)
- Items missing context reference (no source of truth)
- Multi-line / bulleted items (must be single paragraph)
- Separate verification / confirmation items (integrate via "ensuring..." clause)
- Overly granular items (e.g., "create directory" alone)
- Separate REMINDER blocks between items

### E1/E2/E3 — Checklist Structure Rules (lines 278-365)
- Flat checkboxes only — NO nested checkboxes, NO parent checkboxes that summarize children
- Use `**Step X.Y:**` headers (NO checkbox) to group, then individual `- [ ]` items beneath
- Components first, summary checkbox LAST (never parent-before-children)
- Sequential top-to-bottom; never "go back and update"

### I15 — Phase-Gate QA Enforcement (lines 599-607)
> "Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint between the primary execution phase and any subsequent phase that depends on its outputs."

A phase-gate consists of: (1) aggregation item collecting phase outputs, (2) QA agent spawn item (rf-qa or rf-qa-qualitative), (3) conditional-action item that PASS-proceeds or FAIL-triggers fix cycle.

### I16 — QA Gate Verdict and Fix Cycles (lines 609-624)
Binary PASS/FAIL. ANY issue severity (CRITICAL/IMPORTANT/MINOR) = FAIL. Fix-cycle caps:
- research-gate / report-validation / any qualitative gate: **3** cycles, then HALT and escalate
- synthesis-gate / task-integrity: **2** cycles, then unresolved → Open Questions

### I17 — Post-Completion Validation Protocol (lines 626-635)
Before frontmatter is set to Done, validation items MUST verify: (1) all `- [ ]` are `- [x]`, (2) all output files exist on disk (Glob), (3) any blocker entries have resolution notes, (4) if source code modified — all relevant tests pass.

### I18 — Testing Requirements for Code-Modifying Tasks (lines 637-646)
> "If a task creates or modifies source code files (not documentation, not configuration), the orchestrator MUST include at least one testing checklist item. This item MUST: (1) Specify the test command to run; (2) Define pass criteria; (3) Specify where test results are captured; (4) Follow the self-contained item pattern from B2."

For Template 02 tasks: use the **L3 (Test/Execute) pattern**.

### L1–L6 — Intra-Task Handoff Patterns (lines 737-810)
- **L1 Discovery:** explore codebase, write structured findings to `phase-outputs/discovery/`. Discovery file IS the deliverable.
- **L2 Build-from-Discovery:** read discovery file AND original source; create output. Reference both paths.
- **L3 Test/Execute:** run command, capture BOTH raw output AND structured summary to `phase-outputs/test-results/`.
- **L4 Review/QA:** assess prior output against source; produce PASS/FAIL verdict file in `phase-outputs/reviews/`.
- **L5 Conditional-Action:** branch on prior result (handle BOTH branches; output always created).
- **L6 Aggregation:** Glob to find files, consolidate to `phase-outputs/reports/`.

### M1 — Phase-Gate QA Sequence (lines 843-850)
A phase-gate is a 2–3 item sequence: (1) L6 aggregation, (2) rf-qa or rf-qa-qualitative spawn, (3) L5 conditional proceed-or-fix-cycle.

### M2 — Phase-Gate Applicability (lines 852-860)
For **code-modifying tasks:** "After implementation phase and before testing phase (if testing is separate), or after combined implement+test phase."

---

## 3. Comparable Example: TASK-RF-track-3-20260517-032112

**Path:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-3-20260517-032112/TASK-RF-track-3-20260517-032112.md` (320 lines, Status 🟢 Done, merged PR #39)

**Why comparable:** Multi-phase release affecting many source files + Makefile targets + pytest suite + `make verify-sync`. Same template_schema_doc: `.claude/templates/workflow/02_mdtm_template_complex_task.md`.

### 3a. Frontmatter Pattern (lines 1-54)
```yaml
id: "TASK-RF-track-3-20260517-032112"
title: "PR3 — Manual rename of E741/N806/N811/F811/F841 violations (~81 manual edits)"
description: "Execute PR3 of the 5-PR CI rot cleanup. Manually rename/resolve..."
status: "🟢 Done"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
task_type: static
related_docs:
- path: ".dev/releases/backlog/ci-rot-cleanup-brainstorm.md"
  description: "Brainstorm spec defining the 5-PR cleanup scope, NFRs, and acceptance criteria"
- path: "src/superclaude/cli/audit/budget.py"
  description: "Primary E741 hotspot — three confirmed `l` loop-variable occurrences at lines 146, 294, 350"
tags:
- "ci-rot"
- "ruff"
- "manual-renames"
blockedBy: ["TASK-RF-track-2-20260517-032112"]
blocks: ["TASK-RF-track-4-20260517-032112"]
```

### 3b. Phase Structure (5 phases + 2 phase-gates)
| Phase | Purpose | Pattern used |
|-------|---------|--------------|
| Phase 1: Preparation | Status update, mkdir, dep check, branch cut, dev-env check | flat items per check |
| Phase 2: Discovery | Generate raw inventory + triage table | L1 Discovery |
| **Phase Gate PG-2** | Verify inventory completeness | L4 Review (verdict file) |
| Phase 3: Execute | Per-file rename batches (dynamic expansion) | L2/L3 hybrid, per-file granularity |
| Phase 4: Final verification | ruff scoped + full pytest + `make verify-sync` + verdict | 3× L3 (Test) + L4 (verdict) |
| **Phase Gate PG-4** | Final quality verdict | L4 |
| Phase 5: Commit + PR | git commit, gh pr create with heredoc body | flat items |
| Post-Completion | Output verification, summary, frontmatter update | I17-conformant |

### 3c. Per-File Edit Pattern (line 175, Step 3.TEMPLATE — most relevant for hook-sync-and-matcher-fix)
Each file gets **ONE self-contained item** that:
1. Reads the discovery inventory ("Read the rename inventory at `…/discovery/rename-inventory.md` to identify all rows for the file `<FILE_PATH>`")
2. Reads the file with Read tool
3. Applies edits with Edit tool
4. Runs pytest scoped to covering test file via Bash, tee'd to `phase-outputs/test-results/batch-<sanitized-file-path>.txt`
5. Runs ruff scoped to that file
6. Appends one-line summary to `per-file-summary.txt`
7. Has a fallback: "If pytest fails after a rename, immediately revert with `git checkout -- <FILE_PATH>`, log failing test names…"
8. Closes with the completion gate: "Once done, mark this item as complete."

### 3d. Pytest Item Pattern (line 191, Step 4.2 — full-suite)
```
Use the Bash tool to run `cd /config/workspace/IronClaude && uv run pytest 2>&1 | tee
.dev/tasks/.../phase-outputs/test-results/final-pytest.txt; echo "EXIT=${PIPESTATUS[0]}"
>> …/final-pytest.txt` to verify the full test suite still passes after all renames,
ensuring the captured file ends with `EXIT=0` and the pytest summary line shows zero
failures and zero errors. If any tests fail, list the failing test IDs and their
tracebacks in the ### Phase 3 Findings section…, return to Phase 3 to address the
regressions, then re-run this step (max 2 retry cycles). Once done, mark this item
as complete.
```
**Pytest items are batched at the suite level for final verification**, but per-file scoped pytest invocations live INSIDE the per-file edit item (NFR2 in that case).

### 3e. `make verify-sync` Item Pattern (line 195, Step 4.3)
Tee'd to a captured file, EXIT trapped via `${PIPESTATUS[0]}`, fallback clause for if sync drift is detected ("copy the canonical edits back to `src/superclaude/`… run `make sync-dev`, then re-run this step").

### 3f. Phase-Gate Pattern (lines 162-164, Step PG-2.1 + lines 197-199, Step PG-4)
Verdict file written to `phase-outputs/reviews/pg<N>-<purpose>-verdict.md` with PASS or FAIL plus per-criterion checklist. Fix-cycle cap embedded inline ("max 2 fix cycles"). PG-4 specifically reads three test-result files and emits a 4-criterion verdict — model pattern for hook-sync-and-matcher-fix final gate.

### 3g. Open Questions Section (lines 318-320)
Single section `### Open Questions Documented from Build Request` at the very bottom, after all other Task Log sections. Format:
```
- **Q1 — <question text>?** Default disposition: **<answer>** — <rationale>. **Escalation:** <condition under which to halt>
```
Used to document decisions deferred from the BUILD_REQUEST, with a clear default and an escalation trigger.

---

## 4. Patterns to AVOID (Anti-Examples Drawn from B5)

For the hook-sync-and-matcher-fix builder, the following patterns are FORBIDDEN by B5 / E2:

| Anti-pattern | Why forbidden | Correct alternative |
|--------------|---------------|---------------------|
| "Edit Makefile, install_hooks.py, and matcher" (single item) | Violates A3 — bulk operation | One item per file |
| "Read hooks-spec.md" (standalone, no output) | Violates B5 — context lost across batches | Embed read into the action item that needs it |
| "Verify all tests pass" (separate from the test run) | Violates C3 / I12 — verification must integrate | Use "ensuring…" clause inside the test-run item |
| "Update Makefile: <br>  - [ ] add target <br>  - [ ] document it" (nested) | Violates E1/E2 — no nested checkboxes | `**Step X.Y:** Update Makefile target` header, then two flat items |
| Parent checkbox before children | Violates E2 — summary in middle | Components first, summary item LAST |

---

## 5. Frontmatter Recommendation for hook-sync-and-matcher-fix

```yaml
id: "TASK-RF-20260517-213436"
title: "hook-sync-and-matcher-fix — Makefile verify-sync, hooks matcher patch, pytest coverage"
description: "Implement the 3-part hook-sync-and-matcher-fix release: (1) extend Makefile verify-sync target to cover hooks parity; (2) fix the install_hooks matcher to handle the missed edge case; (3) add pytest scenarios that lock in both the verify-sync behavior and the matcher fix. All three parts ship together and are gated by a single phase-gate + post-completion validation."
status: "🟡 To Do"
type: "🔧 Refactor"     # primary intent is hardening existing infra; "✨ Feature" only if matcher fix is a net-new capability — Refactor is the more defensible default
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: ""
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
related_docs:
- path: ".dev/releases/current/hook-sync-and-matcher-fix/<spec-file>.md"
  description: "Release spec defining the 3-part scope"
- path: "Makefile"
  description: "verify-sync target to extend"
- path: "src/superclaude/cli/install_hooks.py"   # confirm exact path with researcher-01
  description: "Hooks installer with matcher to patch"
- path: "tests/<hooks-test-path>/"               # confirm exact path with researcher-03
  description: "Pytest harness where new scenarios will be added"
tags:
- "hooks"
- "verify-sync"
- "matcher-fix"
- "makefile"
- "pytest"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
```

**Rationale for `type: "🔧 Refactor"`:** the verify-sync extension hardens an existing target, the matcher fix is a bug correction, and pytest scenarios lock down both. None of the three parts is a net-new user-facing feature. If the release-spec frames the matcher fix as enabling a new install scenario, switch to `✨ Feature` — but Refactor is the default per the release name's "fix" verb.

**Rationale for `task_type: "static"`:** all three parts (Makefile edit, matcher patch, test additions) are enumerable upfront from the spec + research findings. There is no dynamic discovery that produces a variable number of edits (contrast with track-3 which had 79 violations enumerated at execution time).

---

## 6. Execution Context Block Recommendation (per SKILL.md A.9, lines 878-974)

### 6a. AUTO Heuristic for This Release

The block emits when "≥3 distinct named source areas can be inferred from the research files." For hook-sync-and-matcher-fix, exactly **3 named areas** are present:
1. **Makefile verify-sync target** (Makefile area)
2. **hooks matcher and install script** (src/superclaude/cli/install_hooks area — name without paths)
3. **pytest test harness for hooks** (tests/cli/hooks area — name without paths)

The 3-area count crosses the AUTO threshold (≥3), so the block **MUST be emitted**.

### 6b. Recommended Block Content (full 3-bullet form)

```markdown
## Execution Context

<!-- OPTIONAL header — task-level rollup for executor reading aid. Per-item Context
fields below remain the authoritative file:line evidence venue. -->

- **References:** R-001: <GOAL verbatim from BUILD_REQUEST>; R-002: <WHY verbatim>; R-003: <related-doc 1 ID/path>; R-004: <related-doc 2 ID/path>
- **Source areas:** Makefile verify-sync target, hooks matcher and installer, pytest hooks test harness
- **Key constraints:** <verbatim from BUILD_REQUEST QA_GATE_REQUIREMENTS or VALIDATION_REQUIREMENTS — top 3 by priority>

---
```

### 6c. Critical Compliance Rules (R-033 / R-034 / R-035 / R-039)

- **Source areas bullet:** MUST satisfy `grep -cE "src/|/.*:[0-9]+"` returning **0**. The names "Makefile verify-sync target", "hooks matcher and installer", "pytest hooks test harness" are compliant (no `src/`, no `:NN`). Do NOT write "src/superclaude/cli/install_hooks.py:42" here — that belongs in per-item Context fields.
- **References bullet:** ALWAYS present (R-001 minimum from GOAL). Verbatim text from BUILD_REQUEST — strip only trailing whitespace.
- **Key constraints bullet:** 1–3 entries, verbatim from BUILD_REQUEST. Drop excess if >3 candidates; OMIT bullet if no constraints surface.
- **Header-wide guard (R-039):** after assembly, the entire block from `## Execution Context` to closing `---` must pass `grep -cE "src/|/.*:[0-9]+"` = 0. If any path leaks via verbatim GOAL/WHY/constraint text, rewrite the offending bullet ONCE; if it still hits, OMIT the block and annotate `header-leak-suppressed`.

### 6d. TB-Add-7 Re-Appearance Check

Every "Source areas:" entry MUST reappear in at least one item's per-item Context field (with file:line citations there). So:
- "Makefile verify-sync target" → must appear in the Makefile-edit item's Context, with `Makefile:<line>` citations
- "hooks matcher and installer" → must appear in the matcher-fix item's Context, with `src/superclaude/cli/install_hooks.py:<line>` citations
- "pytest hooks test harness" → must appear in the test-add item's Context, with `tests/<path>/test_*.py:<line>` citations

---

## 7. Recommended Phase Skeleton for hook-sync-and-matcher-fix

Drawn from template L7 "Common Phase Structures" + track-3 example. Suggested phase ordering (researcher-01/02/03 will confirm file inventory and exact step granularity):

| Phase | Purpose | L-pattern(s) |
|-------|---------|--------------|
| **Phase 1: Preparation** | Status → 🟠 Doing; mkdir phase-outputs; cut feature branch from master; confirm dev env (`make dev`, `uv run pytest --version`) | flat items |
| **Phase 2: Implement** | One item per file: (a) Makefile verify-sync edit; (b) install_hooks matcher patch; (c) new pytest scenario(s) — each scenario gets its own item per A3 if multiple | K1 file-by-file (one item per file/scenario) |
| **Phase Gate PG-2** | Spawn rf-qa (structural) on the three edits + Open Questions check | M1 (L6 aggregate → rf-qa spawn → L5 conditional, max 2 fix cycles per I16 task-integrity) |
| **Phase 3: Verification** | (a) Run `make verify-sync` (L3, tee to file); (b) Run `uv run pytest tests/<hooks-path>/ -v` scoped (L3); (c) Run full `uv run pytest` (L3); (d) Final verdict file (L4) | L3 × 3 + L4 |
| **Phase Gate PG-3** | Read the 3 capture files, emit `pg3-final-verdict.md` with PASS/FAIL per-criterion checklist | L4 + L5 |
| **Phase 4: Commit + PR** | git add specific files (per CLAUDE.md "Git Safety" rule — never `git add -A`); commit with conventional-commit message; `gh pr create` with heredoc body | flat items |
| **Post-Completion Actions** | I17-conformant: Glob output files, confirm tests pass, write Task Summary, update frontmatter to 🟢 Done | flat items |

---

## 8. Summary

**Template location:** `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md`
**PART 2 copy range:** lines 896-1197 (from `# [Task Title]` to end of file)
**Strip from output:** all `<!-- ╔═══ ORCHESTRATOR INSTRUCTION BLOCK … ═══╝ -->` blocks

**Canonical comparable example:** `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-track-3-20260517-032112/TASK-RF-track-3-20260517-032112.md` (5 phases + 2 phase-gates + 1 post-completion section, 320 lines, merged PR #39). Especially useful patterns: 3.c (per-file edit with embedded pytest), 3.d (full pytest with EXIT trap), 3.e (`make verify-sync` with tee + fallback), 3.f (PG-N verdict files), 3.g (Open Questions with default disposition).

**Critical mandatory rules:** A3 (granular), A4 (iterative), B2 (self-contained 6-element items), B3 (one paragraph), E1-E3 (flat checkboxes, summary last), I15-I17 (phase-gates + post-completion validation), I18 (testing item required for code-modifying tasks), L3 (test/execute pattern), M1 (phase-gate sequence).

**Execution Context block:** EMIT (3 source areas crosses AUTO threshold). Three bullets: References (verbatim, never blank), Source areas (3 named-without-paths entries), Key constraints (1–3 verbatim from BUILD_REQUEST). MUST satisfy `grep -cE "src/|/.*:[0-9]+"` = 0 over the whole block.

**Recommended frontmatter:** `type: 🔧 Refactor`, `task_type: static`, `priority: 🔼 High`, `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"`, tags `[hooks, verify-sync, matcher-fix, makefile, pytest]`.

**Recommended phase count:** 4 execution phases + 2 phase-gates + post-completion = ~6 logical sections.
