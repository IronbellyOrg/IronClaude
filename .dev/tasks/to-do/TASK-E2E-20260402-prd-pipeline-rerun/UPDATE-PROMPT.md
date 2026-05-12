# Prompt: Update E2E Rerun Task File with QA Fixes

## Context

We recently completed a round of QA fixes to the PRD/TDD pipeline integration work. The task file at:

```
.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md
```

is a reset copy of the original E2E test task (`TASK-E2E-20260327-prd-pipeline-e2e`) with all 63 checkboxes cleared back to incomplete. **Before we execute this rerun, the task file needs to be updated to reflect the QA fixes that were made since the original run.**

## What You Need To Do

### Step 1: Discover What Changed

Find all QA-related code changes made since the original E2E run (completed ~2026-03-31). Focus on:

1. **Git history** — Run `git log --oneline --since="2026-03-31" -- src/superclaude/cli/` and `git log --oneline --since="2026-03-31" -- src/superclaude/skills/` to find recent commits touching pipeline code and skills.

2. **QA review files** — Check these locations for QA findings and fix documentation:
   - `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/` — adversarial QA agent reports
   - `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/phase-outputs/reports/follow-up-action-items.md`
   - `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/RESUME-FINDINGS-REVIEW.md`

3. **Diff the code** — Run `git diff <commit-before-qa>..HEAD -- src/superclaude/cli/` to see exactly what changed in the pipeline code.

4. **Known issues from original run** — The original task file's findings tables and "Known Issues" section documented these problems:
   - Anti-instinct gate halting both pipelines (pre-existing)
   - Fingerprint coverage regression (0.76 → 0.69) with PRD enrichment
   - Click stderr swallowing auto-detection messages
   - `detect_input_type()` threshold changes
   - Various gate mismatches (DEVIATION_ANALYSIS_GATE, TEST_STRATEGY_GATE)

### Step 2: Update the Task File

For each QA fix discovered:

1. **Update existing items** — If a fix changes expected behavior for an existing verification item, update that item's description. For example:
   - If the anti-instinct gate was fixed, update items 4.7, 5.5, etc. to expect PASS instead of expected failure
   - If `detect_input_type()` thresholds changed, update items that check auto-detection behavior
   - If new CLI flags were added/renamed, update the flag-check items in Phase 1 and Phase 3

2. **Update "Known Issues" section** — Mark fixed issues as resolved, add any new known issues

3. **Update "Open Questions" section** — Resolve questions that the QA fixes answered

4. **Insert new items** — If QA fixes introduced new behavior that the existing items don't cover, add new verification items in the appropriate phase. For example:
   - If a new gate was added, add items to verify it
   - If error handling was improved, add items to test the new error paths
   - If prompt builders were modified, add items to verify the new prompt content

5. **Update output directory references** — The new task uses `.dev/test-fixtures/results/test1-tdd-prd-rerun/` and `.dev/test-fixtures/results/test2-spec-prd-rerun/` (or similar) to avoid overwriting the original results. Update all output path references accordingly.

6. **Update the `estimated_items` count** in frontmatter if you added/removed items.

### Step 3: Document Changes

At the bottom of the task file, add a new section:

```markdown
### QA Fix Integration Notes (2026-04-02)

| Change | Source | Items Affected | Description |
|--------|--------|----------------|-------------|
| ... | commit abc123 | 4.7, 5.5 | Anti-instinct threshold adjusted |
| ... | QA review #7 | 3.4, NEW 3.6 | Redundancy guard message format changed |
```

### Step 4: Add Tasklist Generation Pipeline Testing

**CRITICAL NEW SCOPE**: The original task file notes that `superclaude tasklist generate` does NOT exist as a CLI command (it was inference-only via `/sc:tasklist`). However, our recent QA/implementation work may have introduced PRD/TDD enrichment into the tasklist generation pipeline. Check whether:

1. **`superclaude tasklist generate` now exists** — Run `uv run superclaude tasklist generate --help 2>&1`. As of this writing it does NOT exist yet. If it still doesn't exist, check whether the `build_tasklist_generate_prompt` function has been updated to accept/use PRD and TDD files (it was confirmed to exist in Phase 7 item 7.5 of the original run).

2. **If `tasklist generate` CLI now exists** — Add a new Phase (Phase 7b or extend Phase 7) with items to:
   - Run `uv run superclaude tasklist generate` with `--prd-file` and `--tdd-file` flags on both Test 1 and Test 2 output directories
   - Verify generated tasklists include PRD/TDD enrichment content
   - Compare enriched generated tasklists vs non-enriched baselines
   - Test auto-wire from `.roadmap-state.json` for generation (same pattern as validation auto-wire in Phase 6)

3. **If `tasklist generate` CLI still doesn't exist but `build_tasklist_generate_prompt` was updated** — Update Phase 7 item 7.5 to verify the updated prompt function signatures and PRD/TDD block content. Add items to test all enrichment scenarios (none, TDD-only, PRD-only, both) with updated assertions.

4. **Update the "Known Limitation" sections** — The task file currently says "There is NO `superclaude tasklist generate` CLI command" in two places (line 86 and Phase 7 header). Update or remove these limitations if the CLI now exists. Update the Deferred Work Items table accordingly.

5. **Build request reference** — A detailed build request for `tasklist generate` CLI exists at `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/BUILD-REQUEST-tasklist-generate-cli.md`. Review it for context on what was planned.

### Step 5: Add Spec-Only Baseline Comparison (Quality Improvement Assessment)

**NEW SCOPE**: The original task file compares PRD-enriched outputs against their PRD-less counterparts (TDD+PRD vs TDD-only, spec+PRD vs spec-only). But it does NOT include a comparison that answers the key question: **"Is the output from the PRD/TDD-updated roadmap pipeline objectively better than what the original spec-only pipeline produced?"**

Add items (in Phase 8 or a new Phase 8b) to perform this quality comparison:

1. **Retrieve or reference the original spec-only baseline** — Check if Test 3 results exist at `.dev/test-fixtures/results/test3-spec-baseline/`. If not, note that the baseline test (`BUILD-REQUEST-baseline-repo.md`) has not been executed yet and this comparison is blocked until it is.

2. **If baseline exists, compare output quality** — For each major artifact (extraction.md, roadmap.md, spec-fidelity.md, test-strategy.md):
   - **Coverage**: Does the TDD+PRD version cover more requirements, more components, more scenarios?
   - **Specificity**: Does the TDD+PRD version produce more concrete milestones, more specific acceptance criteria?
   - **Business alignment**: Does the PRD enrichment produce roadmaps that better reflect business priorities, personas, and success metrics?
   - **Completeness**: Count sections, requirements traced, risks identified, test scenarios generated
   - Write a quality delta report with quantitative metrics (section counts, requirement counts, identifier coverage) and qualitative assessment

3. **Cross-pipeline quality matrix** — Build a matrix comparing all pipeline variants:

| Metric | Spec-Only (baseline) | Spec+PRD | TDD-Only | TDD+PRD |
|--------|---------------------|----------|----------|---------|
| Extraction sections | | | | |
| Requirements traced | | | | |
| Fingerprint coverage | | | | |
| Roadmap milestones | | | | |
| Persona references | | | | |
| Business metrics | | | | |
| Compliance items | | | | |

This matrix is the definitive evidence that PRD/TDD integration improves pipeline output quality.

## Important Rules

- Do NOT check any boxes — this is a prep step, not execution
- Do NOT delete existing items unless they are truly obsolete — prefer updating descriptions
- Keep item numbering stable where possible (existing items keep their numbers)
- New items should be inserted at the end of their phase with the next sequential number
- All pipeline commands must use `uv run superclaude` (never bare `superclaude`)
- Output paths in the new task should reference `TASK-E2E-20260402-prd-pipeline-rerun` not the old task ID
