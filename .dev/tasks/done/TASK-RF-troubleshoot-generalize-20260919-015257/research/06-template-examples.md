# Research 06: Template & Examples

**Track goal:** Implement §(d) R-01..R-19 of merged-report-v2.md (sc:troubleshoot generalization) in IronClaude.
**Scope:** Template 02 PART 1 + PART 2; prior task TASK-RF-troubleshoot-hardening-20260610-144537 as shape example; glance at other TASK-RF-* editing SKILL.md.
**Status:** Complete
**Date:** 2026-09-19

---

## 1. Template 02 PART 1 rules by ID

Source: `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1514 lines; PART 1 = lines 62-1130, PART 2 = lines 1156-1514).

### Section A: Core Principles (lines 84-144)

| ID | Name | Operative sentence (quoted) | Line |
|----|------|-----------------------------|------|
| A1 | Workflow Document Availability Check | "If workflow documents DO NOT EXIST: Omit all workflow-specific sections (marked with "WORKFLOW-DEPENDENT" below) ... Replace workflow references with direct user requirements" | 88-99 |
| A2 | Workflow Doc Deep Integration [WORKFLOW-DEPENDENT] | "Extract EVERY requirement, phase, step, and quality standard from the workflow" | 101-105 |
| **A3** | **Complete Granular Breakdown** | "Break down EVERY workflow phase into atomic, verifiable checklist items / Create individual checklist items for EVERY file, component, or iteration / NO high-level or bulk operations allowed - everything must be granular / Include exact file paths, specific requirements, and measurable outcomes" | 107-111 |
| **A4** | **Iterative Process Structure** | "For ANY process involving multiple items (files, components, etc.): Pre-enumerate ALL items to be processed in initial step; Create individual checklist item for each specific item; Require incremental updates after each item; Include consolidation step only after all items complete" — pattern: `Step X.1 enumerate` → `Step X.2 one item per [Item N]: [exact identifier] - [specific action] completed` → `Step X.3 consolidate` | 113-132 |
| A5 | Cross-Stage Integration [WORKFLOW-DEPENDENT] | "EVERY phase must explicitly specify inputs from previous stages" | 134-138 |
| A6 | Workflow Compliance Enforcement [WORKFLOW-DEPENDENT] | "Copy quality standards directly from workflow documents" | 140-144 |

Note for THIS task: no `.gfdoc/workflows/` governing doc exists → A1 rule 3 applies: omit WORKFLOW-DEPENDENT sections (A2, A5, A6, D1, D2); derive requirements from merged-report-v2.md §(d) R-01..R-19 directly.

### Section B: Self-Contained Checklist Items (lines 146-212)

| ID | Operative sentence | Line |
|----|--------------------|------|
| B1 | "any context loaded in batch 1 will NOT be available in batch 3+. Therefore, EVERY checklist item MUST be self-contained ... Standalone 'read context' items that don't produce actionable output are USELESS" | 150-156 |
| **B2** | EVERY item MUST include 6 elements: "1. **Context Reference with WHY** ... 2. **Action with WHY** ... 3. **Output Specification** - The exact output file name, location, what content to produce ... 4. **Integrated Verification** - An 'ensuring...' clause ... 5. **Evidence on Failure Only** - Log to task notes ONLY if unable to complete ... 6. **Explicit Completion Gate** - 'This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.'" | 158-164 |
| B3 | "Each checklist item should be written as ONE FULL PARAGRAPH (not multiple lines or bullets) that is verbose and explanatory." | 166-169 |
| B4 | Canonical example item (Read spec → Read pattern file → create output → ensuring clause → J1 blocker clause → "Once done, mark this item as complete.") | 171-174 |
| B5 | FORBIDDEN: standalone read items; missing context reference ("Update the configuration file ❌ WRONG - which file? what updates?"); multi-line/bulleted items; separate verification items; "Overly granular items (e.g., 'create directory' alone)"; "Separate REMINDER blocks between checklist items" | 180-199 |
| B6 | PREFERENTIAL: context source refs when reading source; output spec when producing a file | 201-203 |
| B7 | "7. QA process handles verification between batches (see I15-I16 for phase-gate rules) - do NOT create separate verification items" | 205-212 |

### Sections C-H (summary)

- C1-C4 (lines 214-246): outputs, success criteria, verification, completion all EMBEDDED in items; never separate sections. C4: "frontmatter update and task summary are the only Post-Completion Actions" beyond I17 validation items.
- D3 (line 285-288): "NO CHECKLIST ITEMS may appear before Phase 1 begins."
- E1-E4 (lines 290-404): flat checkboxes, `**Step X.Y:**` bold headers without checkboxes, summary checkboxes AFTER components, top-to-bottom only, no "see below"/"go back".
- F1 (410-419): READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. F2a (430-446): one item per loop; **parallel spawning exception** line 446: "When consecutive checklist items within the SAME phase spawn INDEPENDENT subagents ... the executor MAY spawn all such agents in parallel".
- F5 (463-467): frontmatter update protocol (Doing/Done/Blocked/updated_date).
- G1-G4 (470-484): headless agents don't auto-load framework rule files; embed conventions.
- H1-H3 (487-506): only specify tools when a SPECIFIC tool is required; embed inline ("use the Bash tool to run `npm test`").

### Section I (lines 508-839) — key rules

| ID | Operative sentence | Line |
|----|--------------------|------|
| I2 | "If a step could be interpreted multiple ways, it needs more detail" | 521-525 |
| I3 | "Explicitly state 'DO NOT attempt to complete entire files at once'" | 527-530 |
| I6 | task_type static vs dynamic; dynamic-content markers `<!-- DYNAMIC CONTENT START: [purpose] -->` | 542-571 |
| I11 | "Status update to '🟠 Doing' must be the first action in the task" | 604-606 |
| I12 | "Do NOT create separate 'verify the file' or 'confirm completion' checklist items" | 608-613 |
| I13 | Post-Completion Actions section mandatory; frontmatter + Execution Log entries | 615-620 |
| I15 | "Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint ... QA gates using only 1-2 agents are PROHIBITED. For FINAL DOCUMENT ... minimum is 6 agents (3 rf-qa + 3 rf-qa-qualitative). For INTERMEDIATE gates ... minimum is 5 agents". Full checkpoint = 7 parts: L6 aggregation → parallel lens spawns (`fix_authorization: false`) → consolidation → ONE fix agent (`fix_authorization: true`) → verification round (min 2) → L5 conditional → M4 if applicable. "Every QA gate step ... MUST be encoded as individual `- [ ]` checklist items". Each spawn item MUST include: agent type, lens, input files, output report path, `fix_authorization: false`, adversarial framing "Assume this document has at least N errors focused on your lens. Find them." | 634-650 |
| I16 | "Any issue of any severity (CRITICAL, IMPORTANT, or MINOR) results in FAIL." Max cycles table: research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3, source-fidelity 3. | 652-672 |
| I17 | Post-completion validation BEFORE frontmatter Done: (1) all items [x], (2) outputs exist via Glob, (3) blockers resolved, (4) "If the task modified source code: all relevant tests pass", (5) lens-based QA per M3 MANDATORY, (6) fidelity gate per M4 when applicable. | 674-685 |
| **I18** | "If a task creates or modifies source code files ... MUST include at least one testing checklist item. This item MUST: 1. Specify the test command (e.g., 'Run `uv run pytest tests/path/ -v`') 2. Define pass criteria 3. Specify where test results are captured (e.g., a test-results file in phase-outputs/) 4. Follow the self-contained item pattern from B2. For Template 02 tasks: use the L3 (Test/Execute) pattern" | 687-696 |
| **I19** | Lens minimums (FULL intensity). Final doc <500 lines: 3 rf-qa + 3 rf-qa-qual = 6; 500-1500: 8; 1500-3000: 10; >3000: 12. Structural lenses: template-conformance, internal-consistency, evidence-quality, completeness. Content lenses: actionability, numbers-metrics, crossref-chain, domain-accuracy. Adversarial N: "5 for <500 lines, 10 for 500-1500, 15 for 1500-3000, 20 for >3000". Intermediate gates: research-gate 5 (2 rf-analyst + 2 rf-qa + 1 rf-qa-qual); synthesis-gate 5; task-integrity 5 (2 rf-qa + 2 rf-qa-qual + 1 rf-analyst). | 698-742 |
| **I20** | Serialized Fix Authorization: "(1) Report phase: Spawn all lens-based QA agents in parallel with `fix_authorization: false` ... (2) Consolidation phase: ... `${TASK_DIR}qa/qa-consolidated-findings.md` ... (3) Fix phase: Spawn ONE rf-qa agent with `fix_authorization: true` ... (4) Verification phase: minimum 2 agents: 1 rf-qa + 1 rf-qa-qualitative ... (5) Cycle control ... Maximum cycles per I16". "Parallel fix authorization ... is PROHIBITED." | 744-756 |
| **I21** | Source-document fidelity gate MANDATORY for "Any task where the orchestrator reads source documents to produce output"; NOT required for "Pure transformation tasks" / "Configuration-only tasks". Checks: semantic coverage, detail preservation, cross-source contradiction, phantom coverage, operational completeness. Min 2 agents; partition 3-4 if sources >1000 lines. Runs AFTER M3. Report: `${TASK_DIR}qa/qa-source-fidelity-report.md`. | 758-787 |
| **I22** | QA intensity: **lite** = intermediate 2, final 3 (1 struct + 1 content + 1 domain), fidelity 1, 1 fix cycle, 1 verifier; **standard** = intermediate 3, final 7 (3 struct + 3 content + 1 domain), fidelity 2, 2 fix cycles, 2 verifiers, partition only >10 files; **full** = I19 tables. "Serialized fix protocol (I20) applies at ALL intensity levels." Double QA DISABLED at lite/standard. | 792-839 |

### Section J (lines 841-863) — Error Handling

J1 embedded clause (verbatim, must appear in every item): "If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete." J2: "Items are NEVER left unchecked". J3: only mark task Blocked if ALL remaining items blocked by the same issue.

### Section K (lines 865-898) — K1 file-by-file / K2 multi-item

K2 line 884-886: "The orchestrator agent creating this task file MUST identify and enumerate ALL items that need processing during task setup. The worker agent MUST NEVER dynamically add checklist items". Per-file pattern uses `#### File: [name] at [path]` header then ONE item (line 895-897).

### Section L (lines 900-1025) — Handoff patterns

Handoff dir convention (908-916): `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/`.

| ID | When | Key rule | Line |
|----|------|----------|------|
| L1 Discovery | explore & produce structured findings | "The discovery file IS the deliverable." | 927-937 |
| L2 Build-from-Discovery | create output from discovery + source | "Always reference the discovery file path AND the source file path." | 939-949 |
| **L3 Test/Execute** | run command/test suite | "Always capture BOTH raw output AND a structured summary." Example: `pytest-output.txt` + `test-summary.md` (PASSED/FAILED, counts, failed-test table). Blocker clause distinguishes execution failure from test failure. | 951-961 |
| L4 Review/QA | assess output vs source | "The review must produce a structured verdict (PASS/FAIL) with specific findings." | 963-973 |
| **L5 Conditional-Action** | branch on result | "The item MUST handle BOTH branches (success AND failure) ... The output file is always created regardless" | 975-987 |
| L6 Aggregation | consolidate outputs | "Use Glob to find all relevant files ... Don't hardcode file lists" | 989-999 |
| L7 Selection guide | | Common structures (1013-1025): "Build → Test → Fix: Phase 2: K1/K2 (build items) → L3 (run tests) → L5 (conditional: fix or proceed)"; "Full Lifecycle with QA Gates: L1 → L2 → **M3 (QA Gate)** → L3 → L5 → L4 → L6 → **M3 (QA Gate)**" | 1001-1025 |

### Section M (lines 1027-1120) — Phase-gate composites

- M1 (1033-1044): DEPRECATED single-agent; "New task files MUST NOT use M1".
- M2 (1046-1056) applicability table, row **Code-modifying tasks**: "After implementation phase and before testing phase (if testing is separate), or after combined implement+test phase | M3 lens-based (minimum 6 agents per I19). Fidelity gate only if code was derived from spec documents" (line 1051).
- **M3** (1058-1095): Step 1 L6 aggregate → Step 2 structural rf-qa PARALLEL (report `${TASK_DIR}qa/qa-structural-[lens]-report.md`) → Step 3 content rf-qa-qualitative PARALLEL (`qa-content-[lens]-report.md`) → Step 4 domain lenses → Step 5 consolidate `qa-consolidated-findings.md` → Step 6 ONE fix agent → Step 7 verification 2 agents (`qa-verification-structural-report.md`, `qa-verification-content-report.md`) → Step 8 L5 conditional. "The orchestrator MUST NOT collapse multiple steps into a single item" (1095).
- **M4** (1097-1120): fidelity gate after M3; Step 1 identify sources explicitly; Step 2 fidelity agents parallel (`qa-source-fidelity-report-[N].md`); Step 3 cross-source contradiction agent (if multiple sources); Step 4 consolidate `qa-fidelity-consolidated-findings.md`; Step 5 ONE fix agent; Step 6 verification 2 agents.

## 2. PART 2 structure (lines 1156-1514)

### Frontmatter fields (lines 1-60)

`id` (format `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS`), `title`, `description`, `version`, `status` (🟡 To Do), `type` (enum line 8; use "✨ Feature" or "⚙️ Process Improvement"), `priority`, `created_date`, `updated_date`, `assigned_to`, `autogen`, `autogen_method`, `coordinator: orchestrator`, `parent_doc`, `parent_task`, `depends_on` (list), `spec_path` (line 23: "driving spec/PRD/TDD path; populated by task-builder (A.2)"), `reflect_pre` block (lines 24-30: verdict/coverage_pct/depth/tcs/report/reviewed_at — "populated by task-builder at A.10.7"), `reflect_post` (line 31, executor fills), `related_docs` (path+description list), `related_prd`, `related_tdd`, `tags`, `template_schema_doc`, `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason`, `ai_model`, `model_settings`, `review_info` block, `task_type: static` (line 59).

### Required body sections IN ORDER

1. `# [Task Title]` (1156)
2. `## Task Overview` (1158)
3. `## Key Objectives` — numbered bold objectives (1162-1168)
4. `## Prerequisites & Dependencies` → `### Parent Task & Dependencies` + `### Previous Stage Outputs (MANDATORY INPUTS)` — "INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE" (1170-1190)
5. `## Execution Context` (1192-1230) — **builder MUST populate** (line 1194): `### References` (`- [Doc](path): purpose`), `### Source Areas` (`- \`path/\`: what/why`), `### Key Constraints` (QA intensity, scope limits, prohibitions), `### Handoff File Convention` (fixed text, phase-outputs subdirs), `### Frontmatter Update Protocol` (fixed text).
6. `## Detailed Task Instructions` (1232) — orchestrator instruction block comment (1234-1288) MUST be removed from output.
7. `### Phase 1: Preparation and Setup` (1290) — Step 1.1 status update item (verbatim at 1322), Step 1.2 create handoff dirs (1325), `### Task-Specific Context Files` informational list (1327-1336).
8. `### Phase 2: [Main Execution]` (1338) — Steps 2.1-2.4 placeholder items (L1/L2/L3/L5).
9. `### Phase Gate: Quality Verification (M3 Lens-Based QA)` (1364-1401) — Steps PG.1 aggregate, PG.2 structural (4 items), PG.3 content (4 items), PG.4 consolidate + fix (2 items), PG.5 verification (3 items incl. L5 conditional), PG.6 fidelity (7 items, if applicable).
10. `### Phase [N]: Testing & Verification` (1403-1409) — I18 L3 item; "remove this entire section if the task is documentation-only".
11. `### Phase 3: [Review and Quality Assessment]` (1411-1420) — L4 review + L6 aggregate.
12. `## Post-Completion Actions` (1422-1440), order: (a) Glob-verify outputs, (b) run test suite if source modified, (c) POST-COMPLETION lens-based QA placeholder — "orchestrator MUST expand into per-agent items following Steps PG.2-PG.5", (d) POST-COMPLETION fidelity placeholder (PG.6 pattern, or "Fidelity gate not applicable — [reason]"), (e) Task Summary, (f) frontmatter → 🟢 Done + Execution Log entry.
13. `## Task Log / Notes 📋` (1442-1514): `### Task Summary` (template block), `### Execution Log` (`**[YYYY-MM-DD HH:MM]** - action`), `### Phase 1 - [Name] Findings`, `### Phase 2 - [Name] Findings` (blocker template: Blocker Reason / Attempted / Required to Unblock), `### Phase 3 - Findings`, `### Phase Gate Findings`, `### Follow-Up Items Identified`, `### Deviations from Process`.

## 3. Prior task file as shape example

Source A: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/TASK-RF-troubleshoot-hardening-20260610-144537.md` (474 lines, 52 items; markdown-only: 4 edits + 5 new refs, no pytest).
Source B (for test-file + SKILL.md + sync patterns): `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-fr-drs-runtime-surface-20260622-000600/TASK-RF-fr-drs-runtime-surface-20260622-000600.md` (113 items; code + 20+ test functions + SKILL.md edits + per-phase M3 gates).

### 3.1 Frontmatter (Source A lines 1-55)

- `id`, `title`, `description` (line 4 — 2-sentence description ends with the file count + validation surface: "Edits 4 source-of-truth markdown files and creates 5 new ref files (all under src/superclaude/), then validates via sync/verify-sync/markdownlint").
- `type: "🔧 Refactor"` (line 7 — NB: not in the template enum at template line 8; this task should use "✨ Feature" or "⚙️ Process Improvement").
- `assigned_to: "rf-task-executor"` (line 11). `spec_path` set (line 18). `reflect_pre` block has an extra `run_id: ""` field (line 24) not in the template. `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` (line 41). `task_type: static` (line 54).
- `related_docs` lists the spec + the `research/` directory (lines 28-32).

### 3.2 Phase structure (Source A, headers at lines 156-378)

```
Phase 1: Preparation, G1 Acknowledgement, and Discovery   (1.1 status, 1.2 dirs, 1.3 approval ack, 1.4 insertion-anchor inventory)
Phase 2: Build — Create 5 New Refs and Edit 4 Source Files (2.1-2.5 new refs; 2.6-2.7 command; 2.8a/2.8b/2.9/2.10/2.11a/2.11b/2.11c SKILL.md; 2.12-2.13 report-template; 2.14 remediation-handoff)
Phase 3: Validation (sync / verify-sync / markdownlint / staging discipline)  (3.1-3.4)
Phase 4: Final QA Gate (M3 Lens-Based QA — full intensity)  (4.1 aggregate; 4.2-4.5 four rf-qa; 4.6-4.9 four rf-qa-qual; 4.10 consolidate; 4.11 fix; 4.12-4.13 verify; 4.14 loop-control)
Phase 5: Source-Fidelity Gate (M4 — spec → output)  (5.1-5.2 fidelity agents; 5.3 consolidate; 5.4 fix; 5.5a verify; 5.5b re-fix; 5.5c loop-control)
Post-Completion Actions (6 items)
Task Log / Notes (Task Summary, Execution Log, Phase 1-5 Findings, Follow-Up, Deviations, Open Questions)
```

Also present: an `## Open Questions` section between Execution Context and Detailed Task Instructions (lines 148-152) — NOT in the template but used to park ratified decisions; Step 1.3 references it.

### 3.3 How multi-file markdown edits were encoded

**Granularity = one item per insertion point, NOT per file.** SKILL.md (one file) got 7 items: 2.8a, 2.8b, 2.9, 2.10, 2.11a, 2.11b, 2.11c (lines 222-248). Each item edits exactly ONE seam (table append / new section at `---` seam / registry rows / gate block / precondition line / Will-Not bullet). Phase 2 preamble line 178 makes it explicit: "Each item creates or edits exactly ONE file (or ONE insertion point). DO NOT batch."

**Per-file grouping** uses the K1 `#### File: <name> (EDIT|NEW — role) at <path>` header (lines 180, 186, 210, 220, 250, 260), then `**Step 2.N:**` sub-headers, one item each.

**Anchor phrasing = TEXT, not line numbers.** Line 178: "Anchor every Edit on exact current TEXT from the discovery inventory at `.../phase-outputs/discovery/insertion-anchors.md`, NOT on absolute line numbers." Key Constraints line 118: "Anchor every Edit on exact TEXT, not absolute line numbers (line numbers in research are off-by-one trailing-newline artifacts — see GF-1)." Every build item: "section refs are authoritative; line numbers approximate — anchor on heading text".

**Discovery step 1.4 (line 174) builds the anchor inventory FIRST**, quoting the exact `old_string` per seam: "one `###` subsection per edit-target file, each recording the EXACT current `old_string` text anchor (quoted verbatim) for every insertion/append point that the Phase 2 edit items will need ... and the 5 new-ref target paths are confirmed ABSENT (record 'ABSENT — safe to create')".

**Chained edits to the same table reference the prior step's output as the new anchor** — Step 2.8b line 228: "read the discovery inventory ... to confirm the rows appended in Step 2.8a are now the last rows of the `## Output Contract` table ... append, immediately after the Step 2.8a rows".

**Column-shape guard embedded** — Step 2.8a line 224: "**COLUMN MODEL (CRITICAL):** the live `## Output Contract` table is a **3-column** table ... Do NOT add a 4th column (... MD056 column-count violation)".

**Fence-integrity guard embedded** — Step 2.12 line 254: "written as plain markdown inside the four-backtick fence with NO nested three-backtick fence, the four-backtick fence still closes correctly after the edit".

**Verbatim-preservation baseline pattern** (Source B, Step 4.1 line 466): capture load-bearing sentences to `phase-outputs/discovery/preserve-baseline.md` BEFORE editing; each subsequent edit item says "P6/P7 are byte-intact against `.../preserve-baseline.md`"; Step 4.6 (line 486) byte-compares after.

### 3.4 Representative items (verbatim)

**(a) Registry-table append item — Source A Step 2.10, line 236:**

> - [ ] Read the discovery inventory at `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/phase-outputs/discovery/insertion-anchors.md` for the exact current last row of the `## Refs` registry table (the `refs/diagnosability-audit.md` row is the last current row) and the table format, and read the refs-registry convention in `01-skill-structure-inventory.md` at `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/research/01-skill-structure-inventory.md` §5 (table header `| File | When loaded |`, one row per ref), then edit `SKILL.md` at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` to append 5 new rows to the `## Refs` registry table immediately after the last current ref row, one per new ref — `` | `refs/pipeline-hardening-closure.md` | Wave 4.5 (pipeline-hardening mode) | ``, [...] — ensuring each row matches the existing 2-column `| File | When loaded |` format with backticked relative `refs/<name>.md` paths, the table remains valid, and the "Do not pre-load" closing line stays intact, with no fabricated ref names. If unable to complete due to missing anchors or file access issues, log the specific blocker using the templated format in the `### Phase 2 - Build Findings` section of the `## Task Log / Notes` at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**(b) `make sync-dev` item — Source A Step 3.1, line 272:**

> - [ ] Use the Bash tool to run the command `make sync-dev 2>&1` to mirror the edited and newly-created `src/superclaude/...` files (...) into the `.claude/` tree, because the new refs auto-mirror per the Makefile and the verify-sync gate requires the mirror to match; capture the complete output to the file `sync-dev-output.txt` at `.../phase-outputs/test-results/sync-dev-output.txt` preserving the exact output, then write a one-line PASS/FAIL summary (PASS if the command exits 0 with no error) to `sync-dev-summary.md` at `.../phase-outputs/test-results/sync-dev-summary.md`, ensuring the summary accurately reflects the raw output with no fabricated result. Do NOT stage any `.claude/` paths as part of this step — `make sync-dev` only refreshes the working tree mirror. If the command fails to execute (e.g., missing `make` target), log the specific blocker [...] then mark this item complete. Once done, mark this item as complete.

**`make verify-sync` item — Source A Step 3.2, line 276** — PASS criterion is literal: "PASS REQUIRES the output to contain the literal string `✅ All components in sync.`", with an embedded one-retry branch: "IF the output does NOT contain `✅ All components in sync.`, re-run `make sync-dev` once and re-run `make verify-sync`".

**Staging-discipline item — Source A Step 3.4, line 284:** `git status --porcelain | grep '^[AM].*\.claude/' || echo "CLEAN: no .claude staged"` → verdict file in `plans/`; "never use `git add -f` on any `.claude/` path".

**(c) pytest L3 item — Source B Step 1.20, line 260:**

> - [ ] Use the Bash tool to run `uv run pytest tests/cli/reflect/test_runtime_surface.py -v --cov=superclaude.cli.reflect.runtime_surface --cov-report=term-missing` (UV-only; never bare `python -m`/`pytest`) and capture the complete output, then run `uv run ruff format --check src/... tests/...` (SCOPED to the changed files only — NOT a repo-wide run [...]) and capture its output, then write the raw combined output to `phase1-unit-results.txt` at `.../phase-outputs/test-results/phase1-unit-results.txt` and a structured summary `phase1-unit-summary.md` at `.../phase-outputs/test-results/phase1-unit-summary.md` containing: overall pytest result (PASSED/FAILED), tests passed/failed/skipped, the coverage % [...], the ruff format --check result (clean/needs-format), and a table of any failures (Test Name, Error Type, Brief Message). Ensuring the summary reflects the raw output with no fabricated results [...]. If the test command fails to execute (execution failure, not test failures), log the specific blocker [...] then mark this item complete. Once done, mark this item as complete.

Followed by an L5 assess item (Step 1.21, line 264) with explicit IF PASSED → `plans/phase1-verdict.md` / IF FAILED → root-cause from raw output → fix → re-run → record.

**(d) Test-file creation item — Source B Step 1.14, line 236 (pattern for the 20 new test files):**

> - [ ] Read research file `07-test-patterns-and-verification.md` at `.../research/07-test-patterns-and-verification.md` §1.3-§1.5 + §2.1 to extract the house test idioms (`from __future__ import annotations` header; `-> None` on every test fn; ONE named `def test_<scenario>()` per case; NO `@pytest.mark.parametrize` [...]), then read the implemented units in `src/...` to get the exact signatures, then create the unit-test file `test_runtime_surface.py` at `tests/cli/reflect/test_runtime_surface.py` with the import header (...) and three named test functions: `test_tag_surfaces_*` (...), `test_find_referrers_*` (...), `test_partition_referrers_*` (...). Ensuring every test fn is annotated `-> None` with a one-line docstring naming the unit/AC, [...] assertions match the implemented behavior with no fabrication, and no placeholder remains. If unable to complete, log the specific blocker [...]. Once done, mark this item as complete.

Note the `xfail` convention (Source B Step 1.17, line 248) when a test is authored before the code it exercises lands: "mark it `@pytest.mark.xfail(reason="...")` with a comment, to be un-xfailed in Phase 2".

### 3.5 QA-gate items — lens prompts and agent counts

Phase 4 preamble (Source A line 288) states the sizing decision in prose: "The reviewed output set is the 9 changed source files (4 edits + 5 new refs), totaling 500-1500 changed lines → per I19/I22 full intensity, this gate uses 4 rf-qa structural lens agents + 4 rf-qa-qualitative content lens agents (8 total), all spawned with `fix_authorization: false`, then serialized fix (one fixer, I20), then a verification round; max 3 fix-verify cycles [...]. Adversarial framing N = 10 (500-1500 line tier)."

Lens choice was DOMAIN-ADAPTED, not the stock 8: structural = template-conformance, internal-consistency, markdownlint-compliance, cross-reference-integrity (Steps 4.2-4.5); content = spec-fidelity, completeness-vs-spec-§7, command-thinness/acceptance-#1, blocking-rule-accuracy (Steps 4.6-4.9).

**Lens spawn item verbatim — Source A Step 4.2, line 296:**

> - [ ] Spawn an `rf-qa` subagent with `fix_authorization: false` and an ADVERSARIAL STANCE, assigning ONLY the **template-conformance** structural lens, with this embedded prompt: "Assume the 9 changed troubleshoot-hardening source files listed in the QA input manifest at `.../phase-outputs/reports/qa-input-manifest.md` have at least 10 template-conformance errors. Find them. Read all 9 files and verify: [lens-specific checklist ...]. Report-only — do NOT modify any file." and direct the agent to write its findings to `qa-structural-template-conformance-report.md` at `.../qa/qa-structural-template-conformance-report.md` with a binary PASS/FAIL verdict (FAIL on ANY issue of any severity) and a per-issue list (file, location, severity, expected vs actual), ensuring the report is evidence-based against the actual files. If the agent cannot run, log the blocker [...] then mark this item complete. Once done, mark this item as complete.

Shape of every lens item: agent type → `fix_authorization: false` → ONE lens → quoted prompt with "Assume ... at least N ... errors. Find them." + lens checklist + "Report-only" → report path under `${TASK_DIR}qa/` → binary verdict + per-issue list → J1 clause → gate.

**Consolidate (Step 4.10, line 328):** Glob `qa/qa-structural-*-report.md` + `qa/qa-content-*-report.md` → `qa/qa-consolidated-findings.md`, deduped with originating lens, "consolidated verdict that is FAIL if ANY agent reported ANY issue of any severity"; records missing lenses if <8 found.

**Fix agent (Step 4.11, line 332):** L5 branch — IF PASS write no-op `qa/qa-fix-applied.md`; IF FAIL spawn ONE `rf-qa` with `fix_authorization: true`, "apply ALL consolidated fixes to the affected SOURCE files under `src/superclaude/...` ONLY (NEVER the `.claude/` mirror), then re-run `make sync-dev`" — re-sync after fix is embedded in the fixer item.

**Verification (Steps 4.12-4.13, lines 336-340):** 1 rf-qa + 1 rf-qa-qualitative, each prompt: read consolidated findings + fix summary, re-inspect, confirm (a) addressed (b) no new issues (c) integrity → `qa/qa-verification-structural-report.md` / `qa-verification-content-report.md`.

**Loop control (Step 4.14, line 344):** IF BOTH PASS → `qa/qa-m3-gate-verdict.md`; IF EITHER FAIL → repeat 4.10-4.13, cycle counter in verdict file, MAX 3; exhausted → HALT + record in Task Log.

**M4 fidelity (Phase 5, lines 346-376):** 2 fidelity agents partitioned by spec section (5.1 "spec §4/§6/§8 + report/hub", 5.2 "spec §7 H1/H2/H3/H4 cards + gate refs"), consolidate → ONE fix → 2 verifiers → 5.5b "consolidate verification reports and spawn ONE serialized re-fix agent if needed" → 5.5c loop control (max 3), exhausted issues appended to `### Open Questions` "NEVER deleting existing entries".

Source B variant: per-PHASE M3 gates (Phase 1 Gate 8 agents, Phase 2/3 Gates 6 agents, Phase 4 Gate 6 + M4), i.e. "Full Lifecycle with QA Gates" from L7 line 1025, with `**Step PG1.2:** Spawn structural lens agents (PARALLEL, `fix_authorization: false`)` headers grouping 3-4 items each (Source B lines 266-306).

### 3.6 Final phase ordering (Source A Post-Completion, lines 378-390)

1. Glob-verify all expected source files + QA verdict files exist (line 380).
2. Testing statement — here "TESTING_REQUIREMENTS is NONE ... record in the Task Log that the validation surface is `make sync-dev` + `make verify-sync` + markdownlint" (line 382). For THIS task this becomes: re-run `uv run pytest tests/troubleshoot/ -v` (I17 item 4).
3. Re-confirm M3 + M4 gate verdict files show PASS — "This item satisfies I17 items 5-6 (the Phase 4 M3 gate IS the post-completion lens-based QA on the final output state, and the Phase 5 M4 gate IS the post-completion source-fidelity gate)" (line 384). This is how the task avoided duplicating the 8+2 agents in Post-Completion: the final-phase gates were placed AFTER all edits + validation, so they already review final state.
4. Task Summary (line 386).
5. POST-reflect gate as PENULTIMATE item (line 388): `/sc:reflect --mode post --remediate --diff <BASE> --tasklist <task file> --spec <spec> --depth deep --executor-model <EXECUTOR_CLASS>`, `<BASE>` = `git merge-base HEAD origin/master`, "before running the gate, run `git add -A` so newly-created untracked refs are captured in the diff surface", record `{verdict, run_id, report}` into frontmatter `reflect_post`.
6. Frontmatter → 🟢 Done + Execution Log entry (line 390).

## 4. Pitfalls for THIS goal (11 markdown edits w/ line-shifting insertions + 20 new test files + fixtures)

| # | Pitfall | Template rule violated | Mitigation (from prior tasks) |
|---|---------|------------------------|-------------------------------|
| P1 | Batch item "apply R-01 to SKILL.md, hypothesis-card-template.md, and confidence-calibrator.md" (one R-item spanning 3 files) | A3 line 110 "NO high-level or bulk operations"; A4 line 116 one item per item | One item per (file × insertion seam). R-items that touch 3 files → 3 items. Files touched by 3 R-items (G2 `hypothesis-card-template.md` R-01/R-07/R-09; G3 `diagnosability-audit.md` R-03/R-06/R-15) → one item per seam, ordered bottom-up within the file, each anchored on the prior step's resulting text (Source A 2.8a→2.8b chain). |
| P2 | Anchoring Edits on spec line numbers (`SKILL.md:439`) that shift after the first insertion (research-notes G1) | B5 line 187 "Missing context reference (no source of truth)"; I2 line 522 | Step 1.x discovery item builds `phase-outputs/discovery/insertion-anchors.md` with verbatim `old_string` per seam (Source A 1.4 line 174); every edit item says "anchor on heading/sentence TEXT, NOT absolute line numbers". Sequence same-file edits bottom-up (Wave 5 → Wave 4.5 → Wave 3 → Wave 1.7 → 1.6 → 1 → wave map) so earlier anchors are not shifted — or rely solely on text anchors, but state the order anyway. |
| P3 | Item edits SKILL.md and also runs `make sync-dev` in the same item, or forgets sync entirely | A3 granularity; project rule "src → sync-dev → .claude" | Separate L3 items for `make sync-dev` (raw output + PASS/FAIL summary) and `make verify-sync` (PASS iff literal `✅ All components in sync.`), plus the staging-discipline grep item (Source A 3.1-3.4). Fix agents must "re-run `make sync-dev`" after applying fixes (Source A 4.11). |
| P4 | Missing per-edit "ensuring..." verification (table column counts, fence integrity, verbatim preservation) | B2 element 4 line 162; I12 line 608 | Embed shape guards: "exactly N cells matching existing column count (MD056)", "four-backtick fence still closes", "P-sentences byte-intact against `preserve-baseline.md`" (Source A 2.8a/2.12; Source B 4.1/4.6). For R-17 HC-rename: ensuring clause must list every `H0`..`H5` token site that must be renamed AND confirm output-contract field names unchanged. |
| P5 | Creating 20 test files as one item "create all R-19 tests" or 20 items with no fixture content | A3/A4; B5 line 188 "what methods? from where?" | One item per test file (or per fixture-set + test-file pair), each naming the exact test function names, the assertion text quoted from R-14 (A1-A10 / C1-C8), the fixture paths under `tests/troubleshoot/fixtures/{io,nonio,regression-sysbox}/`, pos+neg expectations, and house idioms (`from __future__ import annotations`, `REPO_ROOT = Path(__file__).resolve().parents[2]`, `-> None`, docstring cites R-item) — Source B 1.14-1.18 shape. Fixtures that a test depends on must be created in the SAME item or an EARLIER item (E3 top-to-bottom). |
| P6 | Tests written BEFORE the markdown edits they assert on → red suite mid-task | E3 sequential order; L3 pass criteria | Either (a) edits phase precedes tests phase and pytest item runs after both, or (b) use the `@pytest.mark.xfail(reason=...)` + un-xfail item convention (Source B 1.17 line 248). Prefer (a). |
| P7 | Existing `test_hardening_h0..h4.py` / `test_hardening_output_contract.py` / `test_hardening_verdict.py` break on R-16 enum + R-17 rename (G5/G6) and no item updates them | I18 line 696 "no regressions"; I17 item 4 | Dedicated items (one per existing test file) BEFORE the full-suite L3 run; L5 assess item handles FAIL → root cause → fix → re-run. Record the A1 ambiguity decision in `## Open Questions`. |
| P8 | Single `uv run pytest` item with no raw-output capture or pass criterion | I18 items 1-3 line 689-691; L3 line 955 "capture BOTH raw output AND a structured summary" | Copy Source B 1.20 shape: `uv run pytest tests/troubleshoot/ -v` → `test-results/pytest-output.txt` + `test-summary.md` (PASSED/FAILED, counts, failed-test table) → L5 verdict item. Add `make lint` / `uv run ruff format --check` SCOPED to new test files. |
| P9 | Skipping the M4 fidelity gate because "it's code" | I21 line 770 "Any task where the orchestrator reads source documents to produce output"; M2 line 1051 "Fidelity gate only if code was derived from spec documents" — here EVERYTHING derives from merged-report-v2.md §(d) | Include M4 with ≥2 agents partitioned by R-item range (e.g. R-01..R-09 / R-10..R-19), each reading the spec range + ALL changed files; ordering after M3 (Source A Phase 5). Spec is >1000 lines? If §(d) alone ~500 lines, 2 agents suffice; if the whole v2 doc is the source, partition 3-4 (I21 line 783). |
| P10 | Under-sizing the M3 gate: 11 edited md files + 20 test files + fixtures ≈ well over 500 changed lines | I19 line 707-710; I22 full = I19 | State the tier in the gate preamble (Source A line 288). Likely 500-1500 → 4+4 = 8 agents, N=10; if >1500 → 5+5 = 10, N=15. Add domain lenses: `hc-rename-completeness` (R-17), `enum-consistency` (R-16 fifth value across SKILL/refs/tests), `test-to-R-item traceability` (R-19). |
| P11 | Collapsing consolidate + fix + verify into one QA item | M3 line 1095 "MUST NOT collapse multiple steps into a single item"; I20 line 756 | One `- [ ]` per agent spawn, per consolidation, per verification, per loop-control (Source A 4.10-4.14). |
| P12 | Leaving the Post-Completion `[PLACEHOLDER ...]` lens/fidelity items from PART 2 lines 1434-1436 unexpanded | I17 items 5-6 | Either expand into per-agent items OR do what Source A did (line 384): place M3 + M4 as the LAST execution phases after all edits/tests/validation, and make the Post-Completion item a re-confirmation that reads `qa/qa-m3-gate-verdict.md` + `qa/qa-m4-gate-verdict.md`, stating explicitly "This item satisfies I17 items 5-6". |
| P13 | Item edits `.claude/skills/...` mirror or tells the executor to `git add -f` | CLAUDE.md ABSOLUTE RULE; Key Constraints Source A line 116 | Every edit item: "ONLY `src/` is edited (NEVER `.claude/`)"; staging grep item; fixer item forbids mirror edits. |
| P14 | Item order violates E3 (e.g. "update the Refs table" before "create `refs/primitive-differential.md`", or a test item referencing a fixture created later) | E3 lines 366-381 | New ref (R-05) created BEFORE the SKILL.md registry-row item; fixtures BEFORE the tests that read them; rename items (R-17) BEFORE the test-update items that assert the new names. |
| P15 | `type:` frontmatter uses a value outside the template enum (Source A used "🔧 Refactor") | template line 8 enum | Use "✨ Feature" (new protocol behaviour + tests). |

## 5. Recommended phase skeleton for this task

Consistent with L7 "Full Lifecycle with QA Gates" (template line 1025) and Source A's build → validate → M3 → M4 → post-completion ordering. Every `- [ ]` follows B2 (context+why → action+why → output → ensuring → J1 blocker clause → "Once done, mark this item as complete.").

```
Phase 1: Preparation and Discovery
  1.1 status → 🟠 Doing + Execution Log entry (template line 1322 verbatim)
  1.2 create phase-outputs/{discovery,test-results,reviews,plans,reports}/ + qa/
  1.3 [L1] baseline check: git branch = feature/troubleshoot-generalize (create from master if absent), `make verify-sync` clean on baseline (research-notes G7) → discovery/baseline.md
  1.4 [L1] insertion-anchor inventory: for all 11 edit targets (SKILL.md, 7 refs, 2 agents, command), quote verbatim old_string per seam per R-item; confirm refs/primitive-differential.md ABSENT; confirm tests/troubleshoot/fixtures/ ABSENT → discovery/insertion-anchors.md
  1.5 [L1] preserve-baseline: verbatim capture of sentences that must survive (output-contract field names for R-17, existing 4 enum tokens context for R-16, fixtures 1-9 of calibrator-eval-cases) → discovery/preserve-baseline.md
  1.6 [L1] existing-test impact inventory: grep tests/troubleshoot/*.py for H0..H5 tokens and the 4-token enum; list every assertion that R-16/R-17 will break → discovery/test-impact.md  (G5/G6)

Phase 2: Build — new ref + 11 markdown edits (one item per file × seam; bottom-up within each file)
  #### File: refs/primitive-differential.md (NEW — R-05)         2.1
  #### File: SKILL.md (EDIT)  — bottom-up:                        2.2 Refs table row (R-05) → 2.3 cost profile/Will-Not (if any) → 2.4 Wave 5 (R-10/R-13 hooks) → 2.5 Wave 4.5 HC rename (R-17) → 2.6 Wave 4 (R-14 wiring) → 2.7 Wave 3 (R-02/R-05/R-08/...) → 2.8 Wave 1.7 → 2.9 Wave 1.6 → 2.10 Wave 1 (R-01) → 2.11 wave map
  #### File: refs/hypothesis-card-template.md — bottom-up:         2.12 filling rule :91 → 2.13 Falsification :80-82 (R-07) → 2.14 "If I'm wrong" → 2.15 claim classes / runs-in (R-01) / behaviour-definition (R-09)
  #### File: refs/diagnosability-audit.md — bottom-up:             2.16 hard constraints → 2.17 complexity signal (R-15) → 2.18 S14 + falsifier columns (R-03/R-06) → 2.19 task type 5
  #### File: refs/triage-checklist.md                              2.20 refuse clause → 2.21 evidence bullet → 2.22 cause-class row (R-15)
  #### File: refs/escalation-rubric.md                             2.23 rule (R-08)
  #### File: refs/hardening-output-contract.md                     2.24 latch → 2.25 enum `blocked-on-authorization` (R-16)
  #### File: refs/report-template.md                               2.26 rendering rules (R-13) → 2.27 Diagnosis-section rule (R-10)
  #### File: refs/calibrator-eval-cases.md                         2.28 (if edited by R-19 test-12 note)
  #### File: agents/confidence-calibrator.md                       2.29 Will-Not/Notes → 2.30 Stage-2 trace row → 2.31 step 5b C1-C8 → 2.32 inputs card_mtime (R-14)
  #### File: agents/evidence-validator.md                          2.33 status → 2.34 output Structural assertions table → 2.35 responsibility 2b A1-A10 → 2.36 inputs (R-14)
  #### File: commands/troubleshoot.md                              2.37 :103 Bash bullet → 2.38 :69 on-return sentence (R-18)
  2.39 [L3] `make sync-dev` → test-results/sync-dev-output.txt + summary
  2.40 [L3] `make verify-sync` (PASS iff `✅ All components in sync.`) → test-results/verify-sync-*
  2.41 [L5] byte-compare preserve-baseline + assess sync → plans/phase2-verdict.md

Phase 2 Gate: M3 lens QA on the 12 changed markdown files (full intensity; state tier + N in preamble)
  PG2.1 [L6] aggregate → reports/qa-input-manifest-md.md
  PG2.2 rf-qa ×4: template-conformance, internal-consistency, cross-reference-integrity, hc-rename-completeness (domain)
  PG2.3 rf-qa-qualitative ×4: spec-fidelity, completeness-vs-R-01..R-19, enum-consistency (domain), actionability
  PG2.4 consolidate → qa/qa-consolidated-findings-md.md ; ONE fix agent (fix_authorization: true; src/ only; re-run make sync-dev)
  PG2.5 verify ×2 → loop control (max 3)

Phase 3: Tests — fixtures + 20 test files + existing-test updates (one item per file)
  3.1 fixtures MANIFEST + tests/troubleshoot/fixtures/{io,nonio}/ minimal pos/neg files (one item per fixture group, content quoted from R-14 assertion text)
  3.2 fixtures/regression-sysbox/ vendored byte copies + sha256 MANIFEST (A2)
  3.3-3.21 one item per new test file test_r19_<nn>_<name>.py (function names, docstring citing R-item, assertion, fixture paths, house idioms)
  3.22 test 12 non-regression over calibrator fixtures 1-9 (`tests/troubleshoot/test_calibrator_eval_cases.py`)
  3.23-3.2x one item per EXISTING test file needing R-16/R-17 updates (from discovery/test-impact.md)
  3.30 [L3] `uv run pytest tests/troubleshoot/ -v` → test-results/pytest-output.txt + test-summary.md ; `uv run ruff format --check` + `make lint` scoped to new/changed .py
  3.31 [L5] assess → plans/phase3-verdict.md (FAIL → root cause → fix → re-run; record)
  3.32 [L3] staging-discipline grep (no .claude/ staged; only src/ + tests/)

Phase 3 Gate: M3 lens QA on tests (6 agents min: 3 rf-qa + 3 rf-qa-qual incl. test-to-R-item traceability domain lens) → consolidate → ONE fix → verify ×2 → loop

Phase 4: M4 Source-Fidelity Gate (spec → output)
  4.1 fidelity agent 1: v2 §(d) R-01..R-09 + all changed files
  4.2 fidelity agent 2: v2 §(d) R-10..R-19 + rescore table + all changed files (+ 4.3 cross-source agent vs spec-panel-critique.md if treated as 2nd source)
  4.4 consolidate → 4.5 ONE fix (re-run sync-dev + pytest after fix) → 4.6 verify ×2 → 4.7 loop control (max 3; exhausted → Open Questions, never delete)

Post-Completion Actions
  - Glob-verify all 12 md + 1 new ref + 20 tests + fixtures + qa verdict files
  - re-run `uv run pytest tests/troubleshoot/ -v` + `make verify-sync` on final state (I17 item 4)
  - re-confirm qa-m3 (both gates) + qa-m4 verdict files PASS — "satisfies I17 items 5-6"
  - Task Summary
  - POST-reflect (penultimate): `/sc:reflect --mode post --remediate --diff $(git merge-base HEAD origin/master) --tasklist <this> --spec <merged-report-v2.md> --depth deep`; `git add -A` first (src/ + tests/ only — NOT .claude/); record reflect_post
  - frontmatter → 🟢 Done + Execution Log

Task Log / Notes: Task Summary, Execution Log, Phase 1-4 Findings, Phase Gate Findings, Follow-Up, Deviations, Open Questions (A1 rename-tests decision, A2 fixture authoring, G7 baseline verify-sync state)
```

Execution Context / Key Constraints to state (mirroring Source A lines 113-120): QA intensity = full; edit ONLY `src/` + `tests/`, never `.claude/`; anchor on TEXT not line numbers, same-file edits bottom-up; UV only; feature branch `feature/troubleshoot-generalize`, PR `--repo IronbellyOrg/IronClaude`; spec = merged-report-v2.md §(d) is the fidelity source; output-contract field names unchanged under R-17.

---

**Status:** Complete

## Summary

1. Template 02 PART 1 rules extracted by ID with line cites: A3 (line 107-111, no bulk ops), A4 (113-132, enumerate → one item each → consolidate), B2 six-element item pattern (158-164), L1-L6 (927-999), M3 (1058-1095), M4 (1097-1120), I15-I22 (634-839).
2. PART 2 section order and frontmatter documented (lines 1-60, 1156-1514); Execution Context (1192-1230) is a mandatory builder-populated block; Post-Completion has two `[PLACEHOLDER]` QA items (1434-1436) that must be expanded or satisfied by final-phase gates.
3. Prior task TASK-RF-troubleshoot-hardening encodes markdown edits as one item per file × insertion seam (SKILL.md = 7 items), anchors on verbatim TEXT captured in a Step 1.4 discovery inventory, chains same-table edits via the prior step's rows, and runs sync-dev / verify-sync / lint / staging-grep as separate L3 items; QA lens items embed a quoted adversarial prompt + report path + `fix_authorization: false`; TASK-RF-fr-drs-runtime-surface supplies the test-file-creation and `uv run pytest` L3/L5 item shapes.
4. 15 pitfalls listed for this goal — chiefly batch multi-file items, line-number anchors, missing per-edit shape guards, unsized M3 gate, skipped M4, un-updated existing hardening tests (G5/G6), and E3 ordering (new ref before registry row; fixtures before tests; rename before test updates).
5. Recommended skeleton: Phase 1 discovery (anchors, preserve-baseline, test-impact) → Phase 2 bottom-up markdown build + sync → M3 gate → Phase 3 fixtures + 20 tests + existing-test updates + pytest/lint → M3 gate → Phase 4 M4 fidelity (spec partitioned R-01..09 / R-10..19) → Post-Completion with POST-reflect penultimate.
