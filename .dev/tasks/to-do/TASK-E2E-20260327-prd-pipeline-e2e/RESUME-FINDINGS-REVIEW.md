# Resume Prompt: TDD/PRD Findings Review

## What We're Doing

We are going through the consolidated findings report at `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` one finding at a time, interactively deciding whether to fix now, backlog, or recategorize each one.

The findings are organized into two sections:
1. **TDD/PRD issues** — caused by our TDD and PRD integration work
2. **Pre-existing issues** — existed before our changes

We are working through the TDD/PRD issues first, all severities (CRITICAL, IMPORTANT, MINOR).

## Work Method

For each finding:
1. You explain what the issue is with FULL context (file, line numbers, what the code does, what's wrong, what the impact is)
2. I decide: fix now, backlog, or recategorize
3. If fix now: you make the code change, verify tests pass, and mark it FIXED in the consolidated findings file
4. If backlog: you mark it as BACKLOG in the findings file
5. If recategorize (e.g., move from TDD/PRD to pre-existing): you move it

## What's Done So Far

### TDD/PRD CRITICALs (5 total):
- **C-04**: FIXED — Added standard body section descriptions + TDD supplementary block to `build_generate_prompt`
- **C-12**: FIXED — Updated 3 skill docs (scoring.md, extraction-pipeline.md, spec-panel.md) to match CLI weighted scoring algorithm
- **C-14**: MOVED to pre-existing — complexity scoring formula never implemented in CLI for ANY path (spec or TDD). Noted: should be implemented for both.
- **C-15**: MOVED to pre-existing — no integration tests for ANY path. Noted: should add for all paths.
- **C-62**: FIXED (earlier) — input_type "auto" written to state file. Fixed by resolving in execute_roadmap() before _build_steps().

### TDD/PRD IMPORTANTs (25 total, 15 FIXED, 10 BACKLOG):
- **C-03**: FIXED — Made spec-fidelity dims 7-11 conditional on tdd_file.
- **C-05**: FIXED — Added TDD supplementary blocks to all 4 remaining prompt builders.
- **C-06**: FIXED — Added tdd_file/prd_file to build_merge_prompt + executor merge step.
- **C-08**: FIXED — Added TDD fallback in _restore_from_state (spec_file as TDD when input_type=tdd).
- **C-16**: FIXED — Added 10 tests for PRD in extract/merge prompts.
- **C-17**: FIXED — Added 2 backward-compat tests for old-schema state files.
- **C-27**: FIXED — Added --prd-file CLI override of state-restored prd_file.
- **C-50**: FIXED — Added log.info for tdd_file, prd_file, and input_type resolution.
- **C-61**: FIXED — Clarified TDD template sentinel about complexity fields.
- **C-84**: FIXED — Removed dead auto-detection from _build_steps.
- **C-91**: FIXED — Added input_type restoration in _restore_from_state.
- **C-111**: FIXED — Moved redundancy guard to execute_roadmap (state now saves correctly).
- BACKLOG: C-19, C-25, C-34, C-35, C-37, C-38, C-51, C-53, C-55, C-57, C-117

### TDD/PRD MINORs (20 total, 8 FIXED, 2 NOT ISSUES, 10 BACKLOG):
- **C-18**: FIXED — Added 4 detection threshold boundary tests (score 0/4/5/6).
- **C-20**: FIXED — Same-file guard for --tdd-file and --prd-file.
- **C-75**: FIXED — Fixed wrong PRD section refs (S7/S22 → S12/S22).
- **C-88**: FIXED — Expanded CLI help text for --tdd-file and --prd-file.
- **C-93**: FIXED — Updated test docstring for comparison dimensions count.
- **C-103**: FIXED — Added borderline warning for scores 3-6.
- **C-113**: FIXED — Removed effective_input_type alias, uses config.input_type directly.
- **C-11**: NOT FOUND — no "deferred" text in prompts.py.
- **C-119**: NOT AN ISSUE — ordering is correct (only 1 builder uses _INTEGRATION_ENUMERATION_BLOCK).
- BACKLOG: C-13, C-21, C-31, C-32, C-59, C-60, C-87, C-89, C-98, C-104, C-105

### Deferred (not changing):
D-01 (tasklist generate CLI), D-02 (fingerprint calibration), S-01 (diff/debate blocks)

## Status: TDD/PRD findings complete. Pre-existing findings remain to review.

## Code Changes Made During This Session

1. `src/superclaude/cli/roadmap/prompts.py` — Major changes:
   - Added 8 standard body section descriptions to `build_generate_prompt` (always present)
   - Added TDD supplementary block to `build_generate_prompt` (conditional on tdd_file)
   - Made fidelity dims 7-11 conditional on tdd_file in `build_spec_fidelity_prompt`
   - Added TDD supplementary blocks to `build_extract_prompt`, `build_extract_prompt_tdd`, `build_score_prompt`, `build_test_strategy_prompt`
   - All 6 builders now have both TDD and PRD conditional blocks

2. `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` — Updated TDD detection rule to match CLI weighted scoring
3. `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` — Same detection rule update
4. `src/superclaude/commands/spec-panel.md` — Same detection rule update
5. `.claude/` copies synced via `make sync-dev`

## Earlier Code Changes (from QA rounds):
- `src/superclaude/cli/roadmap/executor.py` — input_type resolution moved to execute_roadmap() + resume path
- `src/superclaude/cli/tasklist/commands.py` — TDD auto-wire fallback (spec_file when input_type=tdd)
- `tests/roadmap/test_validate_cli.py` — Updated test for resolved input_type

## How to Resume

1. Read the consolidated findings file: `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md`
2. Find C-06 in the TDD/PRD IMPORTANT section — that's where we left off
3. Present the finding with full context (what the code does, what's wrong, impact)
4. Wait for my decision
5. Continue through the remaining IMPORTANTs, then MINORs

## Key Files

- Findings: `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md`
- Raw history: `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings-raw.md`
- Agent reports: `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/adversarial-qa-agent*.md`
- Prompts code: `src/superclaude/cli/roadmap/prompts.py`
- Executor code: `src/superclaude/cli/roadmap/executor.py`
- Tasklist commands: `src/superclaude/cli/tasklist/commands.py`

## Critical Rules
- `uv run superclaude` for all pipeline runs (not bare `superclaude`)
- `make sync-dev` after editing any skill/command files in `src/superclaude/`
- Run `uv run pytest tests/cli/test_tdd_extract_prompt.py tests/roadmap/ tests/tasklist/ -v --tb=short` after code changes
