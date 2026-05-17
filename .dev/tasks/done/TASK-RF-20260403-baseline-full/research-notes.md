# Research Notes: Baseline Full Pipeline E2E (Roadmap + Tasklist)

**Date:** 2026-04-03
**Scenario:** A (explicit BUILD_REQUEST with detailed phases, commands, verification)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

### Already Complete (from prior TASK-RF-20260402-baseline-repo)
- `.dev/test-fixtures/results/test3-spec-baseline/` — 9 roadmap artifacts already exist from prior baseline run
  - extraction.md, roadmap.md, roadmap-opus-architect.md, roadmap-haiku-architect.md
  - diff-analysis.md, debate-transcript.md, base-selection.md
  - anti-instinct-audit.md, wiring-verification.md
- `.dev/test-fixtures/results/comparison-test2-vs-test3.md` — Roadmap comparison already done
- `.dev/test-fixtures/results/full-artifact-comparison.md` — Three-test comparison already done

### Test Fixtures (verified)
- `.dev/test-fixtures/test-spec-user-auth.md` — 312 lines, spec fixture (DO NOT recreate)

### Comparison Targets
- `.dev/test-fixtures/results/test2-spec-modified/` — Test 2 spec-only output (9 artifacts)
- `.dev/test-fixtures/results/test2-spec-prd/` — Test 2 spec+PRD output (includes tasklist-fidelity.md)
- `.dev/test-fixtures/results/test1-tdd-modified/` — Test 1 TDD output (9 artifacts)
- `.dev/test-fixtures/results/test1-tdd-prd/` — Test 1 TDD+PRD output (includes tasklist-fidelity.md)

### Baseline Capabilities (verified via git show master:)
- `src/superclaude/cli/tasklist/commands.py` — has `validate` subcommand, NO `generate`
- `src/superclaude/cli/tasklist/executor.py` — exists on master
- `.claude/skills/sc-tasklist-protocol/` — exists on master (SKILL.md + rules/ + templates/)
- Baseline `tasklist validate` has NO --tdd-file or --prd-file flags

### Worktree Status
- Worktree was removed after prior baseline run — needs to be recreated
- Master branch at commit 4e0c621

## PATTERNS_AND_CONVENTIONS

### Tasklist Generation
- No `superclaude tasklist generate` CLI command exists (on master or feature branch)
- `/sc:tasklist` skill exists on master — can generate tasklist via Claude inference
- The skill takes a roadmap path and optional --spec flag
- Output: tasklist-index.md + phase-N-tasklist.md files

### Tasklist Validation
- `superclaude tasklist validate <output-dir>` exists on master
- Baseline validate has NO --tdd-file or --prd-file flags
- Produces tasklist-fidelity.md report
- Known issue: crashes on directories without proper roadmap.md

### Key Differences: Baseline vs Modified
- Baseline: no TDD/PRD enrichment, no Supplementary sections in fidelity report
- Modified: TDD adds 5 supplementary checks, PRD adds 4 supplementary checks
- This is what we're measuring

## GAPS_AND_QUESTIONS

1. Can `/sc:tasklist` actually be invoked in the worktree? It requires Claude Code session context — the worktree is just a git checkout, not a separate Claude session. The skill would need to be invoked from within the worktree directory.
2. Does the baseline `tasklist validate` work with the roadmap output we already have? It may crash if the roadmap was halted at anti-instinct (known issue).
3. The BUILD_REQUEST says Phases 1-2 overlap with the prior task — can we skip the roadmap run since results already exist and just recreate the worktree for tasklist operations?
4. Phase 7 comparison requires enriched tasklist results from the other E2E run (BUILD-REQUEST-e2e-full-pipeline-with-tasklist.md) — do those results exist yet?

## RECOMMENDED_OUTPUTS

| # | Topic | Output File |
|---|-------|-------------|
| 01 | Existing results inventory | `research/01-existing-results-inventory.md` |
| 02 | Baseline tasklist capabilities | `research/02-baseline-tasklist-capabilities.md` |
| 03 | Enriched results availability | `research/03-enriched-results-check.md` |
| 04 | Template rules | `research/04-template-rules.md` |

## SUGGESTED_PHASES

### Researcher 1 — File Inventory (Existing Results)
- **Topic type:** File Inventory
- **Scope:** `.dev/test-fixtures/results/` — all test output directories
- **Focus:** What exists from prior runs, what's missing (tasklist artifacts), what comparison targets are available
- **Output:** `research/01-existing-results-inventory.md`

### Researcher 2 — Integration Points (Baseline Tasklist)
- **Topic type:** Integration Points
- **Scope:** `src/superclaude/cli/tasklist/` on master, `.claude/skills/sc-tasklist-protocol/` on master
- **Focus:** How tasklist generation and validation work in the baseline. Can /sc:tasklist be invoked in a worktree? What does tasklist validate need? What output does it produce?
- **Output:** `research/02-baseline-tasklist-capabilities.md`

### Researcher 3 — File Inventory (Enriched Results)
- **Topic type:** File Inventory
- **Scope:** `.dev/test-fixtures/results/test1-tdd-prd/` and `.dev/test-fixtures/results/test2-spec-prd/`
- **Focus:** What enriched tasklist results exist for comparison. Do tasklist-fidelity.md files exist? Do tasklist-index.md files exist?
- **Output:** `research/03-enriched-results-check.md`

### Researcher 4 — Template & Examples
- **Topic type:** Template & Examples
- **Scope:** MDTM template 02, existing task folder examples
- **Focus:** Template rules for complex task files
- **Output:** `research/04-template-rules.md`

## TEMPLATE_NOTES

**Template:** 02 (Complex) — worktree setup, pipeline execution, tasklist generation via skill, validation, cross-repo comparison
**Tier:** Standard
**QA Gate Requirements:** FINAL_ONLY — focus on pipeline behavior, not report quality (per BUILD_REQUEST QA guidance)
**Testing Requirements:** NONE — this IS the test
**Validation Requirements:** Pipeline artifacts produced; tasklist generated if possible; comparison report written

## AMBIGUITIES_FOR_USER

None — the BUILD_REQUEST is clear. The key uncertainty (whether baseline has tasklist generation) is handled by the conditional Phase 3 logic in the BUILD_REQUEST.

**Status:** Complete
