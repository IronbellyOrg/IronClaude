# Follow-Up Action Items -- E2E PRD Pipeline Verification

**Date:** 2026-04-02
**Task:** TASK-E2E-20260402-prd-pipeline-rerun
**Branch:** feat/tdd-spec-merge

This document is self-contained for a future developer who has not seen these test runs.

---

## 1. Bugs Found

### BUG-1: `tasklist validate` crashes without roadmap.md (Phase 6, Item 6.5)

- **Severity:** IMPORTANT
- **Description:** Running `uv run superclaude tasklist validate` on a directory that lacks `roadmap.md` produces a Python traceback (FileNotFoundError) instead of a graceful error message.
- **Root Cause Hypothesis:** The `tasklist validate` executor assumes `roadmap.md` exists in the target directory and does not check for its absence before attempting to read it.
- **File to Investigate:** `src/superclaude/cli/tasklist/executor.py` -- the function that resolves roadmap.md path.
- **Status:** Pre-existing bug, not caused by auto-wire changes. Confirmed in this E2E run.

### BUG-2: Baseline overwrites enriched fidelity output (Phase 7, Items 7.1-7.2)

- **Severity:** IMPORTANT (test infrastructure)
- **Description:** Running `tasklist validate` twice on the same output directory overwrites the previous `tasklist-fidelity.md` file. Items 7.1 (enriched) and 7.2 (baseline) both wrote to the same file, destroying the enriched output.
- **Root Cause Hypothesis:** The fidelity output path is deterministic based on the output directory, with no option to specify a custom output filename.
- **File to Investigate:** `src/superclaude/cli/tasklist/executor.py` -- output path construction.
- **Status:** Design limitation. Workaround: use `tee` to capture output or copy the file before re-running.

### BUG-3: LLM does not generate Supplementary PRD section when no tasklist exists (Phase 7, Item 7.4)

- **Severity:** IMPORTANT
- **Description:** When running `tasklist validate` on spec+PRD output with `--prd-file`, the fidelity report does not include a "Supplementary PRD Validation" section. The LLM appears to gate supplementary checks on whether a tasklist exists to validate against.
- **Root Cause Hypothesis:** The prompt instructs the LLM to check persona/metric/scope coverage in the tasklist, but when no tasklist exists, the LLM skips the entire supplementary section rather than reporting "cannot validate -- no tasklist."
- **File to Investigate:** `src/superclaude/cli/tasklist/prompts.py` -- `build_tasklist_fidelity_prompt()` -- the PRD supplementary block wording.
- **Status:** Observed. May be fixable by adding explicit instructions to always emit the section header with a "no tasklist" note.

### BUG-4: Phase 7 QA found fabricated severity ratings (Phase 7, Item 7.6)

- **Severity:** IMPORTANT (process)
- **Description:** The initial Phase 7 comparison and summary files contained fabricated MEDIUM/LOW severity ratings for supplementary items. The actual fidelity report does not assign individual severity ratings to supplementary checks -- only DEV-001 (missing tasklist) has an explicit HIGH severity.
- **Root Cause:** Executor hallucinated severity ratings that were not present in the source fidelity report. QA gate caught and corrected.
- **Status:** RESOLVED. Files rewritten with accurate content.

---

## 2. Known Issues Confirmed

| Issue | First Observed | Confirmed In This Run | Notes |
|-------|---------------|----------------------|-------|
| Anti-instinct gate blocks all pipelines (uncovered_contracts too strict) | 2026-03-27 | Yes -- all 4 runs FAIL | Roadmaps do not wire all integration contracts (middleware_chain, strategy_pattern) |
| Anti-instinct undischarged_obligations (TDD path) | 2026-03-27 | Yes -- reduced from 5 to 1 with PRD | PRD context helps reduce skeleton placeholders |
| Click stderr swallowed in dry-run | 2026-03-27 | Yes | Detection messages not captured by tee pipeline |
| `uv run superclaude` required (pipx binary is older) | 2026-03-27 | Yes | Dev-installed editable package has all changes |

---

## 3. PRD Enrichment Assessment

**Goal:** Add business context (personas, metrics, compliance) to pipeline outputs without breaking existing functionality.

**Result: ACHIEVED.**

| Aspect | Assessment | Evidence |
|--------|-----------|----------|
| Compliance requirements injected | HIGH VALUE | GDPR/SOC2 appear in all enriched outputs (0 to 7-16 mentions); 4-5 additional NFRs |
| Persona-driven constraints added | HIGH VALUE | Alex/Jordan/Sam personas inject user-centric requirements; 5-9 mentions in roadmaps (varies by path) |
| Business metrics added | HIGH VALUE | $2.4M revenue, conversion >60%, session >30min as success criteria |
| Risk inventory expanded | HIGH VALUE | Doubles from 3 to 7 in both paths (adoption, breach, compliance, email delivery risks) |
| Structural integrity preserved | CONFIRMED | Identical frontmatter field counts and section counts between enriched and non-enriched |
| TDD isolation preserved | CONFIRMED | Zero cross-contamination in all spec-path outputs |
| No regressions | CONFIRMED | Fingerprint regression from prior run (0.69) partially recovered to 0.73 |

**What was missing:**
- PRD fidelity dimensions 12-15 could not be validated (anti-instinct halt prevents spec-fidelity from running).
- LLM sometimes skips supplementary PRD validation section when no tasklist exists.

---

## 4. Auto-Wire Assessment

**Goal:** Enable `tasklist validate` to automatically discover TDD and PRD files from `.roadmap-state.json` without requiring explicit CLI flags.

**Result: ACHIEVED (4/5 scenarios PASS).**

| Capability | Status | Evidence |
|-----------|--------|----------|
| Basic auto-wire (both files) | WORKS | 6.1: Both tdd_file and prd_file auto-wired |
| input_type restoration | WORKS | C-91 fix: input_type correctly restored as "tdd" from state |
| Explicit flag override | WORKS | C-27 fix: explicit --prd-file suppresses auto-wire |
| Graceful degradation (missing file) | WORKS | 6.4: WARNING emitted, command continues |
| Missing state file | FAILS | 6.5: Python traceback (pre-existing bug) |

**Gaps:** The crash on missing roadmap.md (BUG-1) should be fixed with a proper error message.

---

## 5. Validation Enrichment Assessment

**Goal:** Add TDD and PRD supplementary validation checks to tasklist fidelity reports.

**Result: PARTIALLY ACHIEVED.**

| Capability | Status | Evidence |
|-----------|--------|----------|
| TDD supplementary checks (5 items) | WORKS | 7.1: S15, S19, S10, S7, S8 checks present |
| PRD supplementary checks (4 items) | WORKS | 7.1: S7, S19, S12/S22, S5 checks present |
| Generate prompt function (4 scenarios) | WORKS | 7.5: no_supplements, tdd_only, prd_only, both -- all pass |
| PRD-only enrichment on spec path | PARTIAL | 7.4: CLI ran successfully but LLM did not generate PRD section |

**Gaps:**
- No `superclaude tasklist generate` CLI command exists. Generation enrichment is untestable E2E. The `build_tasklist_generate_prompt` function is implemented but has no CLI entry point.
- LLM behavior is inconsistent: generates supplementary sections when a tasklist deviation exists (7.1) but skips them when no tasklist exists (7.4).

---

## 6. Deferred Work

| Item | Description | Priority | Source |
|------|-------------|----------|--------|
| DW-1 | Anti-instinct synonym-aware fingerprint matching | HIGH | Phase 9 recommendation: PRD synonyms reduce fingerprint coverage |
| DW-2 | `superclaude tasklist generate` CLI command | MEDIUM | Phase 7 limitation: generation enrichment untestable E2E |
| DW-3 | Graceful error for missing roadmap.md in tasklist validate | MEDIUM | BUG-1 from Phase 6 |
| DW-4 | PRD fidelity dimensions 12-15 E2E validation | LOW | Blocked by anti-instinct halt; requires anti-instinct fix first |
| DW-5 | Custom fidelity output filename for tasklist validate | LOW | BUG-2: baseline overwrites enriched output |
| DW-6 | Prompt wording for supplementary PRD section (always emit header) | LOW | BUG-3: LLM skips section when no tasklist |
| DW-7 | Investigate haiku-architect retry instability with large PRD context | LOW | Phase 9: TDD+PRD required attempt 2 |
| DW-8 | CLI `--input-type prd` choice (internal routing only, not exposed) | DEFERRED | Design decision: PRD detection is auto-only |

---

## 7. Recommended Next Steps (Prioritized)

1. **[HIGH] Fix anti-instinct gate strictness.** The uncovered_contracts check blocks all 4 pipelines. Consider: (a) implementing synonym-aware fingerprint matching (DW-1), (b) reducing the uncovered_contracts threshold, or (c) treating uncovered contracts as warnings rather than failures. This is the single biggest pipeline blocker.

2. **[HIGH] Fix tasklist validate crash on missing roadmap.md (BUG-1, DW-3).** Add a file-existence check before attempting to read roadmap.md. Emit a clear error message like "No roadmap.md found in {directory}. Run `superclaude roadmap run` first."

3. **[MEDIUM] Build `superclaude tasklist generate` CLI (DW-2).** The `build_tasklist_generate_prompt` function is implemented and tested (4/4 scenarios pass). It needs a CLI entry point to enable E2E testing of generation enrichment.

4. **[MEDIUM] Re-run E2E after anti-instinct fix.** Once the anti-instinct gate is resolved, re-run to validate: (a) spec-fidelity dimensions 12-15 (criterion 4), (b) test-strategy step completion, (c) full pipeline end-to-end. This will close the last SKIPPED criterion.

5. **[LOW] Improve supplementary section prompt wording (DW-6).** Update `build_tasklist_fidelity_prompt()` to instruct the LLM to always emit supplementary section headers even when no tasklist exists, with a note like "Cannot validate -- no tasklist found."

6. **[LOW] Add custom output filename option to tasklist validate (DW-5).** Allow `--output-file` flag to prevent overwriting when running multiple validation passes on the same directory.

7. **[LOW] Investigate haiku-architect retry with large PRD context (DW-7).** Monitor whether the retry pattern becomes frequent with PRD enrichment. If so, consider truncating extraction context for smaller models.
