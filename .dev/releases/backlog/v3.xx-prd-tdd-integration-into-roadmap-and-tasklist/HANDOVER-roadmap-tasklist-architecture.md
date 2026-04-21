# Handover: Roadmap & Tasklist Architecture Overhaul

**Date:** 2026-04-06
**Branch:** `feat/tdd-spec-merge`
**Status:** Research complete, implementation not started

---

## 1. Where We Are

### What prompted this work

The TDD + PRD integration exposed three structural failures in the roadmap/tasklist pipeline:

| Problem | Evidence | Root Cause |
|---------|----------|------------|
| 4.1x richer input produces 49% fewer tasks | TDD+PRD (1,282 lines) → 44 tasks; Spec (312 lines) → 87 tasks | Extraction compresses structured documents into ~50 entities |
| Large outputs truncate silently | TDD extraction produced 10/14 sections before cutting off | One-shot `claude --print` architecture — entire output in a single response |
| Output format varies wildly between runs | Spec input → table-based roadmap; TDD input → prose narrative | No output template — the LLM invents its own format each time |

### Prompt fixes already applied (partially)

Recent commits to `src/superclaude/cli/roadmap/prompts.py` added:
- Anti-consolidation language in `build_generate_prompt()` — "technical-layer phasing mandate" and "PRD prevented from changing phase count"
- TDD supplementary block improvements
- `--prd-file` supplementary input flag (`a9cf7ee`)

These were confirmed by the prior research agent which found 2 CODE-CONTRADICTED claims — the prompts have been substantially rewritten since the first tasklist-quality investigation.

### Test fixture results (most recent run: 2026-04-03)

Pipeline run with TDD+PRD input (`test-fix-tdd-prd`):

| Artifact | Result |
|----------|--------|
| `extraction.md` | 668 lines, 14 FR + 9 NFR, complexity 0.65 MEDIUM |
| `roadmap.md` | 347 lines, 5 phases, 60 numbered task rows (using IDs like DM-001, COMP-004, etc. — not R- prefixes), `total_task_rows: 60` in frontmatter matches actual count |
| `diff-analysis.md` | Produced |
| `debate-transcript.md` | Produced |
| `base-selection.md` | Produced |
| `anti-instinct-audit.md` | Produced |
| `test-strategy.md` | Produced |
| `spec-fidelity.md` | Produced |
| `wiring-verification.md` | Produced |

**Key observation:** The roadmap has 60 task rows — matching the frontmatter — which is an improvement over the prior run's 44. However, the spec baseline produces ~140 roadmap rows and 87 tasklist tasks from 312 lines of input. The TDD+PRD path with 4x richer input (1,282 lines) should produce significantly more tasks, not fewer. The pipeline ran to completion but the output still does not reflect the full granularity of the TDD input.

### TDD skill comparison work

We did a comparison review of the TDD skill output (Version A: new template, 3,781 lines vs Version B: old template, 2,777 lines). Key outcome:

- Version B (shorter, template-compliant) was judged stronger than Version A (longer, template-violating)
- The self-audit corrections doc (`TDD-comparison-review-CORRECTIONS.md`) established a principle: **more is not better in a TDD** — content must be at the right abstraction level
- Template adherence is a primary differentiator — ad-hoc sections that don't exist in the template should be flagged as deviations

### Test fixtures and comparison baselines

Three mock input documents are used for all pipeline testing:

| Input | Lines | Location |
|-------|-------|----------|
| TDD (User Auth) | 876 | `.dev/test-fixtures/test-tdd-user-auth.md` |
| PRD (User Auth) | 406 | `.dev/test-fixtures/test-prd-user-auth.md` |
| Spec (User Auth) | 312 | `.dev/test-fixtures/test-spec-user-auth.md` |

Two completed test runs serve as the comparison baselines:

**Spec baseline (original repo, `master` branch):**
- Results: `.dev/test-fixtures/results/test3-spec-baseline/`
- Roadmap: ~140 task content rows (in `| Task | Requirements Covered | Details |` format, no IDs), no `total_task_rows` in frontmatter, full pipeline including tasklist generation (5 phase files)
- Tasklist fidelity: `.dev/test-fixtures/results/test3-spec-baseline/tasklist-fidelity.md`
- Verdict: `.dev/test-fixtures/results/e2e-baseline-verdict.md`
- Prior research found this produced 87 tasks after tasklist expansion

**TDD+PRD (new repo, `feat/tdd-spec-merge` branch):**
- Latest results: `.dev/test-fixtures/results/test-fix-tdd-prd/` (post-prompt-fix run)
- Prior results: `.dev/test-fixtures/results/test1-tdd-prd-v2/` (pre-prompt-fix run, 3 phase tasklist files)
- Roadmap: 60 numbered task rows (in `| # | ID | Task | Description | Depends On | Acceptance Criteria |` format), `total_task_rows: 60` in frontmatter, 5 phases
- Quality comparison: `.dev/test-fixtures/results/quality-comparison-prd-tdd-vs-spec.md`
- Prior research found this produced 44 tasks after tasklist expansion

**The core metric:** Spec (312 lines) → 87 tasklist tasks (from ~140 roadmap rows). TDD+PRD (1,282 lines) → 44 tasklist tasks (from 60 roadmap rows). A 4:1 input richness ratio produces a 0.5:1 output ratio — the pipeline regresses with richer input. The TDD+PRD roadmap rows are individually more detailed (6 columns with acceptance criteria vs 3 columns without), but the total coverage is far lower than the input warrants.

**Note on counting:** The two roadmaps use different table formats (spec has unnamed rows, TDD+PRD has numbered/ID'd rows). Direct row counts are not apples-to-apples. The tasklist task count (87 vs 44) is the more reliable comparison because the tasklist generator normalizes format.

**After any changes to prompts, templates, or pipeline architecture, both test paths MUST be re-run:**
1. `superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md` — spec baseline
2. `superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md` — TDD+PRD path

Then compare: task row counts, phase counts, granularity of individual tasks, and whether the TDD+PRD roadmap reflects the full depth of the 876-line TDD. The spec roadmap is the quality floor — the TDD+PRD roadmap should be significantly more detailed, not less.

### Deep research completed

A full pipeline investigation was completed on 2026-04-04:
- **Report:** `.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` (863 lines)
- **Research artifacts:** 8 codebase + 2 web research files, 6 synthesis files, 11 QA reports
- **All at:** `.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/`

---

## 2. What We Learned (Key Research Findings)

### The pipeline (12 steps)

```
CLI → detect_input_type() → _route_input_files() → _build_steps() → execute_pipeline()
     ↓
     extract → generate-A ↘
                           → diff → debate → score → merge → anti-instinct
               generate-B ↗                                     ↓
                                            test-strategy → spec-fidelity
                                                               ↓
                                            wiring-verification → deviation-analysis → remediate
```

- 8 steps are LLM-based (subprocess via ClaudeProcess), 4 are deterministic Python
- Only 1 parallel group: generate-A + generate-B (dual-architect adversarial)
- `build_certify_step()` is confirmed dead code — defined but never called

### Extraction is never bypassed

Every pipeline run passes through extraction as step 1, regardless of input type. When input is a TDD, it still gets summarized into extraction output. The generate step then receives BOTH the extraction AND the original TDD — but anchors on the extraction's compressed output.

### One-shot is a quality problem, not just a token problem

The token limits are not the bottleneck (Opus: 128k output tokens, Sonnet/Haiku: 64k). There's also a reported 64k non-streaming fallback cap in `--print` mode (sourced from a GitHub issue — not independently verified, flagged as Q-17 in the research open questions). But **the real problem is that one-shotting hundreds or thousands of lines of structured output produces dramatically worse results than incremental writing**, regardless of whether you hit a token limit.

When an LLM generates a 300-line roadmap in a single response:
- It makes structural decisions early that paint it into corners for later sections
- It loses coherence across sections — Phase 5 may contradict Phase 1
- It collapses granularity under attention pressure — "implementing 8 API endpoints" becomes a single task row instead of 8
- It cannot self-correct — if it realizes Phase 3 is wrong, it can't go back and fix Phase 1
- Format drift accumulates — table columns that were correct in row 5 may lose a column by row 50

Incremental writing (section by section via Write/Edit tools) solves all of these:
- Each section gets the LLM's full attention
- The LLM can read what it already wrote before continuing
- Format is enforced by the template skeleton that was created first
- Self-correction is possible — read Phase 1 output before writing Phase 2

**The subprocess already has `--tools default` and `--dangerously-skip-permissions`** — it CAN use Write/Edit tools right now. Sprint already does this pattern. Switching to tool-use file writing requires only prompt changes, not flag changes.

### No output template

- Roadmap: no template. Output format described inline in prompt strings. `build_generate_prompt()` says "task rows" but never defines columns.
- Tasklist: generation is skill-only (`/sc:tasklist`). The CLI only validates. `build_tasklist_generate_prompt()` is dead code.
- Meanwhile, TDD/PRD/Spec all have templates in `src/superclaude/examples/`.

### Prompts are where granularity dies

| Prompt | Granularity Impact |
|--------|--------------------|
| `build_extract_prompt` / `build_extract_prompt_tdd` | **Destroys** — tables/code → prose sections |
| `build_generate_prompt` | **Reduces** — no task table schema, no minimum counts |
| `build_merge_prompt` | **Destroys** — missing ID preservation, no `_INTEGRATION_ENUMERATION_BLOCK`, no granularity floor |
| `build_diff_prompt` | **Reduces** — discards areas of agreement |
| `build_debate_prompt` | Neutral |
| `build_score_prompt` | Neutral |

### Gate change impact

| Risk Level | Gates |
|------------|-------|
| Will break | EXTRACT, EXTRACT_TDD, TEST_STRATEGY, SPEC_FIDELITY, MERGE |
| May break | GENERATE_A, GENERATE_B, DIFF, DEBATE |
| Immune | ANTI_INSTINCT, WIRING, DEVIATION_ANALYSIS, REMEDIATE, SCORE |

Also found: latent frontmatter parser bug (two parsers with conflicting behavior) and field name mismatch in DEVIATION_ANALYSIS_GATE.

---

## 3. The Vision (What We Want)

The core idea you described is right and the research validates it:

**Roadmap should be template-driven and input-proportional.** The pipeline should:

1. **Create the output file first** from a template (skeleton with section headers, table schemas, frontmatter)
2. **Fill it in incrementally** using the input document directly — not through a lossy extraction intermediary
3. **Scale output proportionally to input** — a short spec produces a short roadmap; a 3,000-line TDD produces a very detailed roadmap with hundreds of task rows
4. **Not care what the input is** — the extraction step should NOT try to find specific section headers. Feed it anything (spec, TDD, PRD, a napkin sketch) and it uses that content to its fullest extent to fill the template

This means:
- **Extraction changes role:** Instead of "summarize into a normalized format," it becomes "read the input, understand its structure, extract metadata" — a thin metadata layer, not a content transformation
- **Template is the output contract:** The roadmap template defines what a roadmap looks like (sections, table schemas, required fields). The LLM's job is to populate the template, not invent the format
- **Incremental writing via tool-use:** The subprocess writes to the output file section by section using Write/Edit tools (the Sprint pattern), not one-shot stdout

---

## 4. What's Left To Do

### Phase 1: Immediate prompt fixes (LOW effort, HIGH impact)

These address the 5 highest-impact gaps without architectural changes:

| # | Fix | File | What to do |
|---|-----|------|-----------|
| 1 | Fix PRD suppression in tasklist | `tasklist/prompts.py:221-223` | Remove the block that strips PRD content from tasklist validation input |
| 2 | Add task table schema to generate prompt | `roadmap/prompts.py` (`build_generate_prompt`) | Define explicit columns: ID, Phase, Task, Component, Dependencies, Acceptance Criteria, Effort, Priority |
| 3 | Add ID preservation to merge prompt | `roadmap/prompts.py` (`build_merge_prompt`) | Add `_INTEGRATION_ENUMERATION_BLOCK` and "Preserve ALL IDs" instruction |
| 4 | Add granularity floor | `roadmap/prompts.py` (`build_generate_prompt`) | "The number of task rows MUST be proportional to input detail. A 200+ entity TDD should produce 100+ task rows." |
| 5 | Tighten SKILL.md merge directives | `skills/sc-tasklist-protocol/SKILL.md` | Change "may merge", "may group" to "MUST NOT merge", "MUST NOT group" |

**Decision gate after Phase 1:** Run the TDD+PRD test fixture again. If task count is still below 70, proceed to Phase 2.

### Phase 2: Create output templates (MEDIUM effort)

| Template | Location | What it defines |
|----------|----------|-----------------|
| Roadmap output template | `src/superclaude/examples/roadmap_template.md` | PART 1 (instructions in HTML comment) + PART 2 (output skeleton): frontmatter schema, Executive Summary, Phase sections with task tables (columns defined), Risk section, Open Questions, Evidence Trail |
| Tasklist index template | `src/superclaude/examples/tasklist_index_template.md` | Index structure with phase references, traceability matrix, coverage summary |
| Tasklist phase template | `src/superclaude/examples/tasklist_phase_template.md` | Phase file structure with task format, tier classification, deliverable registry |

Design patterns from existing templates:
- Use PART 1/PART 2 pattern from MDTM templates (instructions in HTML comment, output skeleton below)
- Use `{{SC_PLACEHOLDER:*}}` sentinels from Release Spec template (enables automated completeness validation via `grep -c`)
- Tables as primary enforcement — every row must populate every column, preventing granularity collapse

### Phase 3: Implement incremental writing (MEDIUM effort)

| # | Change | File |
|---|--------|------|
| 1 | Add `tool_write_mode` flag to ClaudeProcess | `pipeline/process.py` |
| 2 | Modify `roadmap_run_step()` to detect tool-write output | `roadmap/executor.py` |
| 3 | Update all 10 prompt builders to instruct "Write to output file using Write tool, section by section" | `roadmap/prompts.py` |
| 4 | Add template loading utility | `roadmap/templates.py` (new) |
| 5 | Register templates in package data | `pyproject.toml` |

The prompt change is the big one: instead of "produce this output," each prompt says "read the template at [path], then fill in each section by writing to [output path] using the Write tool."

### Phase 4: Replace extraction with metadata-only pass (MEDIUM effort)

**This is the key architectural change:** Extraction stops being a content transformation and becomes a thin metadata layer:
- Input type detection (already exists: `detect_input_type()`)
- Complexity scoring (already exists in extraction output)
- Domain detection (already exists)
- Section inventory (what's in the input, at what depth)
- Entity count estimate (how many task rows to expect)

The generate step then receives:
1. The full original input document (TDD, PRD, spec — whatever it is)
2. The metadata stub from extraction (not the summarized content)
3. The output template to fill

This means the LLM works directly from the source document at full granularity.

### Phase 5: Update gates (LOW-MEDIUM effort)

- EXTRACT gate: accept `"bypass-tdd"` extraction mode for metadata-only extraction
- GENERATE gates: add minimum task row count check, add sentinel validation (`{{SC_PLACEHOLDER}}` completeness)
- MERGE gate: add ID preservation check
- New gates may be needed for template completeness validation

### Phase 6: Tasklist pipeline (MEDIUM effort)

- Add `tasklist generate` CLI subcommand (currently skill-only)
- Or: enhance the skill to use templates and incremental writing
- Fix the PRD suppression bug
- Add anti-consolidation guards

### Phase 7: Testing

- Unit tests for templates, bypass logic, gates, prompts
- Integration tests: spec-only, TDD-only, TDD+PRD, tasklist-generate
- Regression: ensure spec input continues working as before
- **Key test fixture:** Re-run the TDD+PRD pipeline after each phase and count task rows

---

## 5. Artifacts & References

### Research artifacts
```
.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/
├── RESEARCH-REPORT-roadmap-tasklist-overhaul.md   # 846-line final report
├── TASK-RESEARCH-20260404-roadmap-tasklist-overhaul.md  # Task file (Done)
├── gaps-and-questions.md                           # Compiled gaps
├── research/
│   ├── 01-pipeline-step-map.md                    # 12-step pipeline trace
│   ├── 02-input-routing.md                        # Input classification mechanics
│   ├── 03-prompt-architecture.md                  # Per-prompt granularity analysis
│   ├── 04-claude-process-output.md                # ClaudeProcess + incremental feasibility
│   ├── 05-gate-architecture.md                    # 15 gates, 31 checkers, migration risk
│   ├── 06-tasklist-pipeline.md                    # Tasklist CLI vs skill analysis
│   ├── 07-template-patterns.md                    # Template design patterns
│   ├── 08-prior-research-context.md               # Validated prior findings
│   ├── web-01-claude-cli-output.md                # Claude CLI output modes + token limits
│   └── web-02-incremental-generation.md           # Incremental LLM generation patterns
├── synthesis/ (6 files)
└── qa/ (8 reports)
```

### Prior research
```
.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/
├── RESEARCH-REPORT-tasklist-quality.md             # First investigation
├── reviews/pipeline-trace-investigation.md         # Pipeline granularity trace
└── reviews/r-item-collapse-investigation.md        # R-item 1:1 mapping proof
```

### Test fixtures
```
.dev/test-fixtures/results/test-fix-tdd-prd/        # Most recent pipeline run
├── extraction.md                                    # 668 lines
├── roadmap.md                                       # 347 lines, 5 phases, 60 claimed / 7 actual R-items
└── (9 more pipeline step outputs)
```

### Issue docs
```
.dev/tasks/to-do/ISSUE-pipeline-one-shot-output.md  # One-shot architecture issue
.dev/tasks/to-do/TDD-comparison-review.md            # TDD skill comparison
.dev/tasks/to-do/TDD-comparison-review-CORRECTIONS.md # Self-audit corrections
```

### Key source files
```
src/superclaude/cli/roadmap/prompts.py      # 942 lines — ALL prompt builders
src/superclaude/cli/roadmap/executor.py     # 2,897 lines — pipeline orchestration
src/superclaude/cli/roadmap/gates.py        # 1,139 lines — 15 gates, 31 checkers
src/superclaude/cli/pipeline/process.py     # 202 lines — ClaudeProcess wrapper
src/superclaude/cli/tasklist/prompts.py     # 237 lines — tasklist prompts
```

---

## 6. Roadmap Validation Doesn't Validate Against Input

### Current state

`superclaude roadmap validate` runs a reflect + adversarial-merge pipeline. It reads exactly 3 files:
- `roadmap.md`
- `test-strategy.md`
- `extraction.md`

(Hardcoded at `validate_executor.py:35` as `_REQUIRED_INPUTS`)

The reflect prompt (`validate_prompts.py:15-74`) checks 7 dimensions:
1. Schema (YAML frontmatter present)
2. Structure (DAG acyclic, no duplicate IDs, heading hierarchy)
3. Traceability (deliverables ↔ requirements)
4. Cross-file consistency (test-strategy refs match roadmap)
5. Parseability (content parseable by `sc:tasklist`)
6. Interleave (test activities not back-loaded)
7. Decomposition (compound deliverables flagged)

### What's wrong

**It never reads the original input.** The validation checks the roadmap against itself and the extraction — but extraction IS the lossy intermediary that destroyed granularity. Validating against extraction just confirms the roadmap is consistent with its own compressed summary.

The validation should compare roadmap output against the actual input (TDD, PRD, spec) to answer:
- Does the roadmap cover everything in the input document?
- Are there input requirements with no corresponding roadmap tasks?
- Is the roadmap proportional to the input detail?
- Did the pipeline drop or merge entities from the input?

**It doesn't read TDD or PRD.** Even when the pipeline had TDD/PRD as supplementary inputs, the validation step never sees them. The `.roadmap-state.json` records TDD/PRD paths but `validate_executor.py` ignores them.

**It's regex-on-headers, not semantic.** The structural checks (DAG acyclic, heading hierarchy, no duplicate IDs) are useful but insufficient. A roadmap could have perfect structure and still miss half the input requirements.

### What needs to change

| Change | What it does |
|--------|-------------|
| Add input files to validation | `_REQUIRED_INPUTS` should include the original spec/TDD/PRD, read from `.roadmap-state.json` |
| Add coverage dimension | New validation dimension: "Coverage — every requirement/entity in the input has a corresponding roadmap task" |
| Add proportionality check | New dimension: "Proportionality — roadmap task count is proportional to input complexity and detail level" |
| Make reflect prompt input-aware | `build_reflect_prompt()` should receive the original input file(s) alongside roadmap/extraction/test-strategy |
| Support all input types | Validation must work for spec, TDD, PRD, and TDD+PRD inputs — not just spec |

---

## 7. Sprint Task Execution Pipeline Issues

A separate deep research investigation was completed on the sprint pipeline:
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md`

This found 10 confirmed gaps (3 CRITICAL, 4 HIGH, 3 MEDIUM) plus ~1,262 lines of dead code that was purpose-built for the target state but never wired. The key issues that need to be addressed:

### 7.1 Limited Handover Prompt (CRITICAL — G-01)

The sprint executor has two paths:
- **Path A (per-task):** Sends a **3-line prompt** — task ID, phase file path, description. No behavioral instructions, no compliance tier, no scope boundary, no result file contract.
- **Path B (whole-phase):** Sends a rich ~40-line prompt with `/sc:task-unified`, Sprint Context, Execution Rules, scope boundary.

**Path A is the standard path** for all protocol-generated phase files (they always contain `### T<PP>.<TT>` headings). Path B is effectively unreachable for well-formed tasklist output.

This means production sprint runs always use the impoverished 3-line prompt.

**Fix:** `_run_task_subprocess()` at `executor.py:1053` needs a `build_task_prompt()` that mirrors Path B's structure, including `/sc:task-unified` invocation, Sprint Context, Execution Rules, scope boundary ("After completing this task, STOP"), and result file instructions.

### 7.2 No Intra-Task QA / Semantic Verification (CRITICAL — G-02, G-03)

Task pass/fail is determined solely by subprocess exit code (`0=PASS`, else `FAIL`). There is no evaluation of whether the task accomplished its stated objective.

The two existing post-task hooks don't help:
- **Wiring gate:** Scans entire codebase for structural issues — not task-aware
- **Anti-instinct gate:** Checks roadmap-specific YAML frontmatter — passes vacuously for sprint tasks because they produce code, not markdown with that frontmatter

`TaskEntry` has no `acceptance_criteria` field. Neither the parser (`parse_tasklist`) nor any hook consumes acceptance criteria.

**Fix:** Add a third post-task hook (`run_post_task_verification_hook`) that reads the task output and evaluates it against the task's acceptance criteria. Since criteria are natural language, this likely requires an LLM-based evaluation subprocess.

### 7.3 In-Memory Phase Tracking — No Crash Recovery (HIGH — G-06)

All `TaskResult` objects live in-memory only within `execute_phase_tasks()`. No task-level events are written to JSONL. If the process crashes mid-phase, ALL intra-phase progress is lost — resume re-executes the entire phase.

| State | Persisted? |
|-------|-----------|
| Phase completion events | Yes (JSONL) |
| Individual TaskResult objects | **No** (in-memory list) |
| TurnLedger state | **No** (in-memory) |
| Which task last completed | **No** (no checkpoint) |

Dead code exists for this: `build_resume_output()` (models.py:633) generates `--resume <task_id>` commands, `aggregate_task_results()` (executor.py:298) produces per-task reports — but neither is called.

**Fix:** Write `task_start` and `task_complete` events to JSONL as they occur. Add checkpoint files per task. Wire `build_resume_output()` and add `--resume-from <task_id>` CLI flag.

### 7.4 Tasklist Generation Format & Template (relates to Section 4)

Tasklist generation is entirely inference-driven via SKILL.md — no output template, no structural enforcement beyond the skill's inline instructions. The CLI has no `tasklist generate` subcommand.

The phase file format (task headings, tier classification, deliverable registries) is prescribed in SKILL.md Section 4.5 but never validated against a template. Format correctness depends entirely on the LLM following instructions.

### 7.5 Output File Collision (HIGH — G-07)

All tasks in a phase write to the same `config.output_file(phase)`. Each task overwrites the previous task's output. Only the last task's artifacts survive on disk.

**Fix:** Task-scoped output paths, e.g., `config.task_output_file(phase, task_id)`.

### 7.6 No Completion Overrun Detection (implicit in G-04)

Per-task prompts contain no scope boundary instruction. Workers have no instruction to stop after task completion. They may drift into subsequent tasks, modify unrelated files, or continue indefinitely until `--max-turns` is exhausted.

Path B includes explicit "After completing this task, STOP" instructions. Path A does not.

**Fix:** Include scope enforcement in the enriched prompt: explicit stop instruction, result file contract, and `EXIT_RECOMMENDATION: CONTINUE/HALT` signal.

### 7.7 Dead Code Inventory (Purpose-Built, Never Wired)

~1,262 lines across 10 components were built for the target state but have zero callers:

| Component | Location | Purpose |
|-----------|----------|---------|
| `build_task_context()` | process.py:245 | Cross-task context injection |
| `get_git_diff_context()` | process.py:310 | Git diff for context |
| `compress_context_summary()` | process.py:335 | Token-budget truncation |
| `setup_isolation()` + `IsolationLayers` | executor.py:108-184 | 4-layer subprocess isolation |
| `build_resume_output()` | models.py:633 | Task-level resume commands |
| `aggregate_task_results()` | executor.py:298 | Per-task report generation |
| `attempt_remediation()` | pipeline/trailing_gate.py:359 | Retry-once gate remediation |
| `execution/` package (4 modules) | execution/*.py | Reflect-Plan-Execute-Correct |

### 7.8 Sprint Research Recommended Approach

The report recommends **Option B (Moderate)** — 3-5 days effort:
1. Enrich Path A prompt to match Path B quality
2. Fix output file collision with per-task paths
3. Wire `build_task_context()` for cross-task context
4. Add third post-task verification hook (structural, not yet LLM-based)
5. Add per-task JSONL logging

With a path to Option C (acceptance criteria gate + PM agent + checkpoint/resume) once Option B is validated.

---

## 8. Pre-Existing Repo Issues (69 findings, deferred)

An adversarial QA pass (14 agents, 7 rounds) was run during the TDD+PRD integration work. It surfaced 69 pre-existing issues in the IronClaude codebase that are **not caused by the TDD/PRD changes** — they existed before. These were separated from TDD/PRD-specific findings during interactive review and deferred while the architectural work was prioritized.

**Full details with file paths, line numbers, code context, impact analysis, and fix suggestions:**
`.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/pre-existing-findings.md`

**Raw agent reports (14 files):**
`.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent*.md`

**Consolidated raw findings:**
`.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings-raw.md`

### Summary: 11 CRITICAL, 30 IMPORTANT, 27 MINOR, 1 META

### CRITICAL (11)

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-01 | DEVIATION_ANALYSIS_GATE `ambiguous_count` vs `ambiguous_deviations` field mismatch — gate can never pass | Yes — one-line rename |
| C-02 | Anti-instinct gate blocks entire downstream pipeline — obligation scanner false positives on "skeleton" descriptions | Yes — change to TRAILING mode |
| C-14 | Complexity scoring formula not implemented in CLI — skill defines formulas but CLI delegates to LLM freeform | No |
| C-15 | No integration tests for full pipeline data flow for any path | No — new test suite |
| C-22 | spec_parser requirement ID regex silently drops compound IDs (FR-AUTH-001, FR-AUTH.1) | No — regex update |
| C-23 | certify_prompts parser regex rejects all structural checker finding IDs | No — regex update |
| C-24 | DIMENSION_SECTION_MAP hardcoded to release-spec numbering — breaks for TDD | No — conditional map |
| C-46 | _restore_from_state assigns unvalidated state values — malformed state crashes pipeline | No — type validation |
| C-79 | Semantic layer call-site passes wrong argument types (dead code path) | Yes — fix args |
| C-80 | _frontmatter_values_non_empty checks ALL fields, not just required — flags optional empty fields as failures | Yes — filter to required |
| C-81 | _parse_frontmatter drops YAML list continuation lines — multi-line lists silently truncated | No — parser fix |

### IMPORTANT (30)

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-07 | _restore_from_state mutates config directly instead of dataclasses.replace | No |
| C-09 | read_state doesn't validate JSON is a dict — non-dict crashes | Yes |
| C-13 | Extraction sections mismatch — CLI has 6 steps, skill layer has 7 | No |
| C-26 | Score step prompt exceeds _EMBED_SIZE_LIMIT with real data — warning only | No |
| C-28 | _embed_inputs no handling for empty or binary files — crashes on read | Yes |
| C-29 | _save_state writes only after all steps complete — mid-pipeline crash loses all progress | No |
| C-30 | Fingerprint extraction ignores file paths, API endpoints, data model field names | No |
| C-37 | Validation sub-pipeline structural checks only — no source document comparison | By design |
| C-38 | Remediation sub-pipeline works from deviation report — no direct source file access | By design |
| C-39 | Convergence fidelity checker scans hardcoded `src/superclaude` path | No |
| C-40 | Obligation scanner position calculation matches wrong section | No |
| C-41 | Integration contract coverage has no per-contract filtering | No |
| C-42 | Obligation scanner discharge check uses substring matching — false positives | No |
| C-43 | Convergence regression handler is a no-op stub | No |
| C-44 | _write_convergence_report hardcodes medium/low counts to 0 | Yes |
| C-45 | Registry not saved on early convergence exit | No |
| C-51 | spec_patch.py doesn't handle TDD/PRD file references | By design |
| C-52 | _check_cross_file_coherence removes from list during iteration — undefined behavior | Yes |
| C-57 | Prompt injection via malicious PRD/TDD content — raw embedding is pre-existing | Design decision |
| C-63 | Frontmatter regex rejects hyphenated field names | No |
| C-64 | Frontmatter regex breaks on blank lines within frontmatter | No |
| C-66 | pyproject force-include may double files in wheel | No — audit |
| C-68 | Makefile paths with spaces break | Yes |
| C-69 | TaskStatus enum collision/inconsistency | No — audit |
| C-82 | sys.path pollution in main.py | Yes |
| C-83 | _embed_inputs raises unhandled FileNotFoundError | Yes |
| C-95 | fidelity_checker.py scans only Python files — misses non-Python deliverables | No |
| C-96 | fidelity_checker partial-match marks found=True, swallows gaps | No |
| C-107 | remediate_parser overlay regexes hardcode column count | No |
| C-108 | _cross_refs_resolve gate check always returns True — never validates | Yes |

### MINOR (27)

| # | Finding | Quick Fix? |
|---|---------|-----------|
| C-10 | Step numbering comment error | Yes |
| C-33 | _FINDING_COUNTER dead global state | Yes |
| C-47 | Duplicate _embed_inputs and _sanitize_output implementations (roadmap + validate) | No |
| C-48 | _extract_by_section heading level calculation wrong | No |
| C-49 | spec_structural_audit divides by zero on empty spec | Yes |
| C-54 | _embed_inputs crashes on UTF-16 encoded files | Yes |
| C-56 | No lock mechanism on .roadmap-state.json for concurrent runs | Doc only |
| C-58 | --agents with empty string crashes | Yes |
| C-65 | Frontmatter regex false positives on `---` in content body | No |
| C-67 | Makefile .DS_Store causes false sync drift | Yes |
| C-70 | Parallel executor prints to stdout instead of stderr | Yes |
| C-71 | Doctor command missing pipeline health checks | No |
| C-72 | Dead deprecation shim | Yes |
| C-73 | Confidence checker mutates input dict | Yes |
| C-74 | Reflexion creates directories on init (side effect in constructor) | Yes |
| C-76 | Bare f-string prefixes with no interpolation | Yes |
| C-77 | Cross-module import of private _OUTPUT_FORMAT_BLOCK | No — design |
| C-78 | Redundant Path() wrapping on values already typed as Path | Yes |
| C-85 | Fidelity batch scripts hardcode container path | No |
| C-86 | prd/tdd skills lack sc- prefix, bypass duplicate skill filter | Yes |
| C-97 | fidelity_checker _STOP_WORDS contains "sets" but not "set" | Yes |
| C-99 | _derive_fidelity_status uses string search instead of YAML parsing | No |
| C-100 | Sprint executor doesn't read .roadmap-state.json — can't inherit pipeline state | No |
| C-106 | _extract_field regex may capture trailing content beyond field value | No |
| C-110 | Gate failure messages lack actual values — just say "field missing" | No |
| C-120 | TDD SKILL.md QA checklist item 13 references wrong synthesis file | Yes |
| C-121 | Obligation scanner lowercases component names — loses case for matching | Yes |

### Overlap with architecture workstreams

Several pre-existing findings directly relate to the roadmap/tasklist and sprint issues documented in Sections 6-7:

| Finding | Overlap |
|---------|---------|
| C-01 | Same as gap M-7 (gate field mismatch) — found independently by architecture research |
| C-02 | Relates to sprint G-02 (vacuous anti-instinct gate) |
| C-29 | Relates to one-shot/crash-recovery architecture issues (Section 3) |
| C-37 | Exactly what Section 6 flags — validation does structural checks only, no source comparison |
| C-80, C-81 | Same frontmatter parser bug family found by gate architecture research |
| C-108 | `_cross_refs_resolve` always returns True — a validation gate that never validates |

### Quick-fix triage

Of the 69 findings, **24 are marked "Quick Fix? Yes"** — these are one-line renames, guard clauses, try/except wrappers, and dead code removal. They could be addressed in a dedicated cleanup sprint without touching the architecture.

---

## 9. Recommended Execution Order

Two workstreams, partially parallelizable:

### Workstream A: Roadmap & Tasklist Architecture (from Section 4)

```
A1: Prompt fixes — task table schema, ID preservation, PRD suppression (1-2 days)
    ↓ decision gate: run test fixture, count task rows
A2: Output templates — roadmap + tasklist templates (2-3 days)
A3: Incremental writing — tool-use mode, section-by-section (2-3 days)
A4: Metadata-only extraction — bypass extraction for TDD/PRD (1-2 days)
A5: Gate updates — accept new format, add sentinel checks (1 day)
A6: Validation overhaul — input-aware, coverage + proportionality dimensions (2-3 days)
A7: Tasklist updates — templates, CLI generate subcommand (1-2 days)
```

### Workstream B: Sprint Task Execution (from Section 7)

```
B1: Enrich Path A prompt — build_task_prompt() matching Path B quality (1-2 days)
B2: Fix output file collision — per-task output paths (0.5 day)
B3: Wire build_task_context() — cross-task context injection (1 day)
B4: Per-task JSONL logging — task_start/task_complete events (1 day)
B5: Post-task verification hook — structural gate, scope enforcement (2-3 days)
B6: Task-level checkpoint/resume — checkpoint files + --resume-from flag (2-3 days)
```

### Dependencies

- A1 is independent — start immediately
- A2-A4 can partially overlap
- A5 depends on A2-A3 (output format must be defined)
- A6 depends on A2 (validation needs to know what the template looks like)
- B1-B2 are independent — can start in parallel with A1
- B3 depends on B2 (need per-task output files to build context from)
- B4-B5 can parallel with B3
- B6 depends on B4 (needs JSONL events for resume logic)

### Priority order if doing one thing at a time

1. **A1** (prompt fixes) — highest impact, lowest effort
2. **B1+B2** (sprint prompt + output collision) — unblocks everything else in sprint
3. **A2** (output templates) — foundational for all architectural changes
4. **B4** (task logging) — cheap, enables crash forensics immediately
5. **A3** (incremental writing) — the architectural shift
6. **A6** (validation overhaul) — must happen before declaring the pipeline reliable
7. **A4** (metadata-only extraction) — extraction bypass
8. **B5** (verification hook) — intra-task QA
9. **B3+B6** (context + resume) — polish

---

## 10. Research Artifacts Index

| Report | Location | Date | Status |
|--------|----------|------|--------|
| Roadmap/Tasklist Architecture | `.dev/tasks/to-do/TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` | 2026-04-04 | Complete |
| Sprint Task Execution | `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md` | 2026-04-03 | Complete |
| Tasklist Quality (prior) | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/RESEARCH-REPORT-tasklist-quality.md` | 2026-04-03 | Complete |
| One-Shot Output Issue | `.dev/tasks/to-do/ISSUE-pipeline-one-shot-output.md` | 2026-04-03 | Open |
| TDD Comparison Review | `.dev/tasks/to-do/TDD-comparison-review.md` | 2026-04-04 | Complete |
| TDD Comparison Corrections | `.dev/tasks/to-do/TDD-comparison-review-CORRECTIONS.md` | 2026-04-04 | Complete |
