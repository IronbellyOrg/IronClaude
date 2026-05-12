# Research Notes: Update E2E Rerun Task File with QA Fixes and Auto-Detection

**Date:** 2026-04-02
**Scenario:** A (Explicit — existing task file, known changes, known sources)
**Depth Tier:** Deep (20+ files changed, multiple subsystems, major new feature)
**Track Count:** 1

---

## EXISTING_FILES

### Task File Being Updated
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` — 63 items, 11 phases, all checkboxes unchecked. Reset copy of TASK-E2E-20260327-prd-pipeline-e2e.

### Change Source Files
- `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` — Master QA findings (123 findings, 28 FIXED, ~21 BACKLOG)
- `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/RESUME-FINDINGS-REVIEW.md` — Session summary of all QA fix work done
- `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/TASK-RF-20260402-auto-detection.md` — Completed auto-detection task (25 items, 7 phases, status=done)

### Modified Pipeline Source Files (a9cf7ee..HEAD)
- `src/superclaude/cli/roadmap/executor.py` — +587 lines: detect_input_type() expanded with PRD scoring, new _route_input_files(), execute_roadmap() uses routing, EXTRACT_TDD_GATE imported
- `src/superclaude/cli/roadmap/commands.py` — +64/-: spec_file→input_files (nargs=-1), routing integration, new stderr format, --input-type includes "prd"
- `src/superclaude/cli/roadmap/gates.py` — +40 lines: EXTRACT_TDD_GATE (19 fields), DEVIATION_ANALYSIS_GATE, REMEDIATE_GATE
- `src/superclaude/cli/roadmap/prompts.py` — +12/-4: PRD authority language updated in extract and extract_tdd builders
- `src/superclaude/cli/roadmap/models.py` — +2/-1: input_type Literal now includes "prd"
- `src/superclaude/cli/tasklist/prompts.py` — +7 lines: TDD fidelity checks 4-5 (data models, API endpoints), PRD fidelity check 4 (priority ordering)

### New Test Files
- `tests/cli/test_tdd_extract_prompt.py` — 822 new lines: PRD detection, three-way boundary, multi-file routing, backward compat, override priority
- `tests/roadmap/test_prd_cli.py` — 97 lines
- `tests/roadmap/test_prd_prompts.py` — 254 lines
- `tests/roadmap/test_resume_restore.py` — 123 lines
- `tests/roadmap/test_spec_patch_cycle.py` — 48 lines
- `tests/tasklist/test_autowire.py` — 147 lines
- `tests/tasklist/test_prd_cli.py` — 41 lines
- `tests/tasklist/test_prd_prompts.py` — 105 lines

## PATTERNS_AND_CONVENTIONS

### E2E Task File Patterns (from original task)
- Each phase has a purpose block (> quoted)
- Items are self-contained with full bash commands
- Items write results to `phase-outputs/test-results/phase[N]-[slug].md`
- Phase summaries written to `phase-outputs/reports/[slug].md`
- Known Issues section documents expected failures
- Findings tables per phase in Task Log

### Change Impact Categories
1. **CLI behavior changes** — affect Phase 1 (CLI verification), Phase 3 (dry-run verification)
2. **Detection changes** — affect Phase 2 (PRD fixture detection check), Phase 3 (auto-detection checks)
3. **Gate changes** — affect Phase 4/5 (extraction gate verification), Phase 9 (pipeline comparison)
4. **Prompt changes** — affect Phase 4/5 (enrichment content checks)
5. **New feature** — multi-file CLI needs entirely new test items
6. **Tasklist changes** — affect Phase 6 (auto-wire), Phase 7 (validation enrichment)
7. **Known Issues resolved** — affect Known Issues section, Findings tables

## GAPS_AND_QUESTIONS

1. The existing task's Phase 1 item 1.3 checks for `--prd-file` and `--tdd-file` flags — these still exist but CLI help text changed. Need researcher to verify exact help output format.
2. The existing task's Phase 3 items use single-file `uv run superclaude roadmap run spec.md` — still valid but multi-file mode is new and untested by the task.
3. Existing task's Phase 4 item 4.2 checks for exactly 13 standard + 6 TDD frontmatter fields — now verified by EXTRACT_TDD_GATE; check if expected field list changed.
4. Existing task's "Known Issues" references anti-instinct halting — unclear if any QA fixes addressed this.
5. Need to check if `detect_input_type()` threshold changed from original >=5 referenced in task.
6. Auto-detection now has PRD scoring — task needs items to verify PRD fixture is NOT detected as PRD (it should be "spec" for the pipeline).
7. The multi-file `nargs=-1` CLI is a major new feature not covered by any existing items — needs a new phase or items.

## RECOMMENDED_OUTPUTS

| # | Researcher Topic | Output File | Scope |
|---|-----------------|-------------|-------|
| 01 | QA Fix Inventory | `research/01-qa-fix-inventory.md` | All 28 FIXED findings mapped to task file items they affect |
| 02 | Auto-Detection & Routing Changes | `research/02-auto-detection-changes.md` | Full _route_input_files(), PRD detection, nargs=-1, and their E2E implications |
| 03 | CLI & Gate Changes | `research/03-cli-gate-changes.md` | commands.py changes, EXTRACT_TDD_GATE, new stderr format, --input-type "prd" |
| 04 | Prompt & Tasklist Changes | `research/04-prompt-tasklist-changes.md` | All prompt builder updates, tasklist fidelity additions, authority language changes |
| 05 | Existing Task Item Mapping | `research/05-item-impact-mapping.md` | Map each of 63 items → which changes affect it, what needs updating |

## SUGGESTED_PHASES

### Researcher 1 — QA Fix Inventory
- **Topic type:** File Inventory + Doc Cross-Validator
- **Scope:** `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md`, `RESUME-FINDINGS-REVIEW.md`
- **Focus:** Catalog all 28 FIXED findings with: finding ID, what was fixed, which source files changed, what E2E behavior changed
- **Output:** `research/01-qa-fix-inventory.md`
- **Other researchers cover:** auto-detection (02), CLI/gates (03), prompts/tasklist (04), item mapping (05)

### Researcher 2 — Auto-Detection & Routing Changes
- **Topic type:** Data Flow Tracer + Integration Points
- **Scope:** `src/superclaude/cli/roadmap/executor.py` (detect_input_type, _route_input_files), `src/superclaude/cli/roadmap/commands.py` (nargs=-1, routing call), auto-detection task file
- **Focus:** Full behavioral specification of new multi-file CLI and routing. What E2E test items need to verify these new behaviors.
- **Output:** `research/02-auto-detection-changes.md`
- **Other researchers cover:** QA fixes (01), gates (03), prompts (04), item mapping (05)

### Researcher 3 — CLI & Gate Changes
- **Topic type:** Integration Points + Patterns
- **Scope:** `src/superclaude/cli/roadmap/commands.py`, `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/roadmap/models.py`
- **Focus:** New EXTRACT_TDD_GATE, DEVIATION_ANALYSIS_GATE/REMEDIATE_GATE imports, --input-type "prd" addition, stderr output format change, help text changes
- **Output:** `research/03-cli-gate-changes.md`
- **Other researchers cover:** QA fixes (01), auto-detection (02), prompts (04), item mapping (05)

### Researcher 4 — Prompt & Tasklist Changes
- **Topic type:** File Inventory + Patterns
- **Scope:** `src/superclaude/cli/roadmap/prompts.py`, `src/superclaude/cli/tasklist/prompts.py`, `src/superclaude/cli/tasklist/commands.py`
- **Focus:** PRD authority language change, new TDD fidelity checks 4-5, new PRD fidelity check 4, what E2E assertions these changes affect
- **Output:** `research/04-prompt-tasklist-changes.md`
- **Other researchers cover:** QA fixes (01), auto-detection (02), CLI/gates (03), item mapping (05)

### Researcher 5 — Existing Task Item Impact Mapping
- **Topic type:** Doc Cross-Validator
- **Scope:** `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` (all 63 items)
- **Focus:** Read every item, cross-reference against all known changes, produce per-item impact assessment: NO_CHANGE, UPDATE_NEEDED (with what), NEW_ITEM_NEEDED (with where)
- **Output:** `research/05-item-impact-mapping.md`
- **Other researchers cover:** QA fixes (01), auto-detection (02), CLI/gates (03), prompts (04)

## TEMPLATE_NOTES

- **Template:** 02 (complex) — the existing task file uses complex template patterns
- **Builder mode:** UPDATE (not new build) — builder receives existing task file + research and modifies it
- **Key constraint:** Must preserve existing item numbering where possible. New items appended at end of their phase.
- **MDTM rules:** A3 (granularity) already satisfied by existing items. Focus on A4 (iterative) for new multi-file test items.

## AMBIGUITIES_FOR_USER

None — intent is clear: update the existing 63-item task file to reflect QA fixes and auto-detection changes, adding new items for untested behaviors.

**Status:** Complete
