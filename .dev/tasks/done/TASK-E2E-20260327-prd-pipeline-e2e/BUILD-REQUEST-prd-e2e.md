# BUILD REQUEST: E2E Test Task — PRD + TDD + Spec Pipeline Integration

## GOAL

Build an MDTM task file that E2E tests the full pipeline after PRD integration is complete. This task must verify that TDD still works, spec still works, PRD enrichment works on top of both, auto-wire works, and tasklist generation enrichment works.

## HOW TO BUILD THIS TASK — READ THESE TWO FILES

### Source 1: The existing E2E test task (CLONE THIS, UNCHECK ALL BOXES)

**File:** `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/TASK-E2E-20260326-modified-repo.md`

This is a completed 42-item, 7-phase E2E test task that tests TDD and spec paths. **You MUST:**

1. Read this file in full
2. Copy its entire structure into the new task file
3. Change every `- [x]` to `- [ ]` (uncheck all boxes — we're re-running everything)
4. Modify existing items to ALSO check for PRD-related behavior (see Source 2 below)
5. Add new items and phases for PRD-specific test scenarios that didn't exist before

The existing phases and what to do with each:

| Existing Phase | Items | What to Do |
|---------------|-------|------------|
| Phase 1: Preparation (3 items) | 1.1-1.3 | Keep. Add items to verify `--prd-file` and `--tdd-file` flags exist on CLI. |
| Phase 2: Create Test Fixtures (4 items) | 2.1-2.4 | Keep TDD + spec fixture creation. ADD new items to create a PRD fixture (`test-prd-user-auth.md`) for the same "User Authentication Service" feature. |
| Phase 3: Dry-Run Verification (4 items) | 3.1-3.4 | Keep TDD + spec dry-runs. ADD dry-runs with `--prd-file` flag. ADD dry-run testing the redundancy guard (`--tdd-file` when primary is TDD). |
| Phase 4: Test 1 — Full TDD Pipeline (12 items) | 4.1-4.10 | Modify the pipeline command to include `--prd-file`. Keep ALL existing artifact verification items. ADD PRD-specific checks to each artifact (persona refs in extraction, business value in roadmap, new state file fields, fidelity dimensions 12-15, test-strategy PRD checks). Change output dir to `test1-tdd-prd/`. |
| Phase 5: Test 2 — Full Spec Pipeline (8 items) | 5.1-5.8 | Same modification — add `--prd-file` to the command. Keep ALL existing TDD-leak checks. ADD PRD enrichment checks. Verify state file has `prd_file` but `tdd_file` is null. Change output dir to `test2-spec-prd/`. |
| Phase 6: Comparison Analysis (5 items) | 6.1-6.5 | Keep extraction comparison and TDD leak checks. ADD comparisons against PRIOR E2E results (TDD+PRD vs TDD-only, spec+PRD vs spec-only). |
| Phase 7: Completion (3 items) | 7.1-7.3 | Keep deliverable checks and follow-up items. |

### Source 2: The PRD implementation task (DERIVE NEW TEST ITEMS FROM THIS)

**File:** `.dev/tasks/to-do/TASK-RF-20260327-prd-pipeline/TASK-RF-20260327-prd-pipeline.md`

This is a 61-item, 10-phase implementation task that adds PRD support. **Read it in full** and use each implementation phase to know what NEW test items to add:

| Implementation Phase | What It Implements | New Test Items to Add |
|---------------------|-------------------|----------------------|
| Phase 2 (items 2.1-2.6): `--prd-file` on roadmap CLI | CLI flag, model field, executor wiring | Phase 1: verify `--prd-file` on `roadmap run --help`. Phase 3: dry-run with `--prd-file`. Phase 4: pipeline run with `--prd-file` flag. |
| Phase 3 (items 3.1-3.5): `--prd-file` on tasklist CLI | CLI flag, model field, executor wiring | Phase 1: verify `--prd-file` on `tasklist validate --help`. New phase: tasklist validate with auto-wired PRD. |
| Phase 4 (items 4.1-4.8b): PRD blocks in 7 prompt builders | Supplementary PRD context in extraction, generate, fidelity, test-strategy, score, tasklist fidelity | Phase 4: check PRD content in extraction.md (personas, metrics, compliance). Phase 4: check PRD influence in roadmap (business value ordering). Check fidelity dimensions 12-15. Check test-strategy PRD items. |
| Phase 5 (items 5.1-5.4): TDD extract PRD block + P3 stubs | PRD block in `build_extract_prompt_tdd`, param stubs | Phase 4: TDD extraction should have PRD supplementary content alongside TDD content. |
| Phase 6 (items 6.1-6.5): Fix dead `tdd_file` in roadmap | `--tdd-file` flag on roadmap, redundancy guard | Phase 1: verify `--tdd-file` on `roadmap run --help`. Phase 3: dry-run testing redundancy guard. New item: test `--tdd-file` with spec primary input. |
| Phase 7 (items 7.1-7.5): Skill/reference layer | extraction-pipeline.md, scoring.md, SKILL.md, spec-panel.md | Phase 1 or new phase: `make verify-sync` confirms skill layer synced. |
| Phase 8 (items 8.1-8.5): Auto-wire from `.roadmap-state.json` | State stores tdd_file/prd_file/input_type, tasklist reads them | **NEW PHASE: Auto-Wire Testing.** Run tasklist validate WITHOUT explicit flags. Verify auto-wire messages. Verify both TDD and PRD supplementary validation present. Test precedence (explicit overrides auto-wire). Test missing file graceful degradation. |
| Phase 9 (items 9.1-9.4): Tasklist generation enrichment | Generation prompt reads TDD/PRD for richer tasks | **NEW PHASE: Generation Enrichment Testing.** Generate tasklist WITH auto-wired TDD+PRD. Generate baseline WITHOUT. Compare: enriched should have named test cases, persona refs, API details, rollback procedures. Baseline should lack all of these. |
| Phase 10 (items 10.1-10.12): Unit testing | Pytest coverage | Not relevant to E2E — unit tests already run in implementation task. |

### NEW PHASES TO ADD (not in the existing E2E task)

**New Phase: Auto-Wire from `.roadmap-state.json`** (~6 items)
- Run `uv run superclaude tasklist validate` on Test 1 output dir WITHOUT `--tdd-file` or `--prd-file`
- Verify auto-wire info messages emitted for both files
- Verify tasklist fidelity output includes BOTH TDD and PRD supplementary validation
- Test explicit flag overrides auto-wire
- Test graceful degradation when auto-wired file path doesn't exist on disk

**New Phase: Tasklist Generation Enrichment** (~6 items)
- Generate tasklist from Test 1 roadmap WITH auto-wired TDD+PRD source documents
- Generate tasklist from same roadmap WITHOUT any supplementary files (baseline)
- Side-by-side comparison: enriched should have specific names/values from TDD (§7 data models, §8 API endpoints, §10 components, §15 test cases, §19 rollback steps) and from PRD (persona names, metric targets, acceptance scenarios)
- Baseline should have none of these specific references

**New Phase: Cross-Run Comparison** (~7 items)
- Compare new Test 1 (TDD+PRD) vs prior Test 1 (TDD-only) at `.dev/test-fixtures/results/test1-tdd-modified/` — did PRD enrichment add value?
- Compare new Test 2 (spec+PRD) vs prior Test 2 (spec-only) at `.dev/test-fixtures/results/test2-spec-modified/` — did PRD enrichment add value without breaking isolation?
- Cross-contamination matrix: PRD content should appear in extraction/roadmap but NOT introduce TDD sections into spec path
- Run rf-qa-qualitative comparing enriched vs non-enriched
- Write verification report at `.dev/test-fixtures/results/verification-report-prd-integration.md`

## FIXTURES

### Existing (reuse as-is)
- `.dev/test-fixtures/test-tdd-user-auth.md` — TDD fixture (already populated, 1000+ lines)
- `.dev/test-fixtures/test-spec-user-auth.md` — Spec fixture (already populated)

### New (create during Phase 2)
- `.dev/test-fixtures/test-prd-user-auth.md` — PRD for "User Authentication Service" that is the PRODUCT-LEVEL PRECURSOR to the TDD. Same feature, same FRs/NFRs, but written from PM perspective. Must include:
  - Personas with names and goals (end user, admin, API consumer)
  - JTBD and business rationale
  - Success metrics with specific targets (registration rate, login latency p95, session duration)
  - User journeys (signup → verify → login → profile → reset → logout)
  - Scope boundaries (auth service IN, RBAC OUT)
  - Compliance/legal (GDPR, SOC2)
  - Acceptance scenarios (happy path + edge cases)
  - Must NOT trigger TDD auto-detection

### Prior results (read-only comparison data)
- `.dev/test-fixtures/results/test1-tdd-modified/` — TDD-only pipeline output
- `.dev/test-fixtures/results/test2-spec-modified/` — spec-only pipeline output
- `.dev/test-fixtures/results/verification-report-modified-repo.md` — prior verification report
- `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/reviews/qa-qualitative-tdd-vs-spec.md` — prior qualitative QA

### New output directories
- `.dev/test-fixtures/results/test1-tdd-prd/` — TDD+PRD pipeline output
- `.dev/test-fixtures/results/test2-spec-prd/` — spec+PRD pipeline output

## PREREQUISITES

- Implementation task `TASK-RF-20260327-prd-pipeline` must be COMPLETE before execution
- `uv run superclaude roadmap run --help` must show `--prd-file` and `--tdd-file`
- `uv run superclaude tasklist validate --help` must show `--prd-file`
- All unit tests passing (`uv run pytest tests/`)

## TEMPLATE

02 (complex)

## CRITICAL RULES

1. **Every item B2 self-contained** — full context, exact commands, exact file paths, exact verification criteria
2. **Phase-gate QA mandatory after Phase 2+** — spawn rf-qa after every phase
3. **`uv run superclaude` always** — never bare `superclaude`
4. **Pipeline timeout 3600000ms** — runs take 30-60 minutes
5. **Incremental writing** — Write (header) then Edit (append). Never accumulate and single-write.
6. **Prior results are READ-ONLY** — `test1-tdd-modified/` and `test2-spec-modified/` are reference data. New output goes to `test1-tdd-prd/` and `test2-spec-prd/`.
7. **PRD fixture must read like a PM wrote it** — personas with names, "As a [user]..." stories, metric targets, not engineering language
