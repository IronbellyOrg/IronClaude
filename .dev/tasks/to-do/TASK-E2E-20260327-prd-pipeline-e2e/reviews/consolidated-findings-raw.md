# Consolidated Findings — TDD + PRD Pipeline Integration

**Date:** 2026-03-31
**Sources:** Adversarial QA Agent 1 (code, 15), Agent 2 (integration, 23), Agent 3 (fresh eyes, 10), Agent 4 (data flow, 10), Agent 5 (deep dive, 25), Agent 6 (edge cases, 16), TDD E2E follow-up, PRD E2E follow-up, Implementation task deferred items
**Deduplication:** Applied across all 6 agents — 99 raw findings → 72 unique (27 duplicates removed)

---

## FIX NOW — Code Bugs & Regressions

These are bugs in the current code that should be fixed before merging to master.

### C-01: DEVIATION_ANALYSIS_GATE field mismatch (one-line fix)
**Severity:** CRITICAL | **Sources:** Agent2 F-13, TDD E2E B-1
**File:** `src/superclaude/cli/roadmap/gates.py` L382, L1038, L539
**Bug:** `_no_ambiguous_deviations()` reads `ambiguous_deviations` but `required_frontmatter_fields` requires `ambiguous_count` and `_total_analyzed_consistent()` reads `ambiguous_count`. The gate can never pass — the LLM can't satisfy both field names.
**Fix:** Change `ambiguous_deviations` to `ambiguous_count` in `_no_ambiguous_deviations()` at L382.

### C-02: Anti-instinct gate blocks entire downstream pipeline
**Severity:** CRITICAL | **Sources:** Agent2 F-11/F-17/F-18, TDD E2E follow-up #1, PRD E2E follow-up #1
**Files:** `src/superclaude/cli/roadmap/gates.py`, `obligation_scanner.py`, `integration_contracts.py`
**Bug:** All 4 E2E runs fail at anti-instinct. The obligation scanner flags "skeleton" task descriptions as undischarged obligations (false positives). The contract checker uses broad patterns (`middleware`, `strategy`, `subscribe`) that match conceptual mentions, not actual dispatch tables. This blocks test-strategy, spec-fidelity, deviation-analysis, and the entire remediation/certification pipeline.
**Fix:** Change ANTI_INSTINCT_GATE to `gate_mode=GateMode.TRAILING` (like wiring-verification) so it reports findings without blocking. Then separately fix the false positive patterns in obligation_scanner and integration_contracts.

### C-03: Spec-fidelity dimensions 7-11 always emitted (regression for spec-only users)
**Severity:** IMPORTANT | **Sources:** Agent2 F-04/F-20
**File:** `src/superclaude/cli/roadmap/prompts.py` L587-591
**Bug:** TDD-specific fidelity dimensions (API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness) are ALWAYS in the prompt, even for spec-only runs. Pre-TDD, the prompt had 6 dimensions. Now it has 11+. For spec inputs without API/component sections, these dimensions generate noise or false deviations.
**Fix:** Make dimensions 7-11 conditional: add "If the source document does not contain this section, write 'N/A — section not present in source document' and do not flag deviations" to each TDD-specific dimension.

### C-04: Generate prompt ignores TDD extraction sections
**Severity:** CRITICAL | **Sources:** Agent2 F-15, Agent1 #3
**File:** `src/superclaude/cli/roadmap/prompts.py` L360-367
**Bug:** `build_generate_prompt()` has a comment saying TDD awareness is "deferred" but the function accepts `tdd_file` and embeds TDD content into the prompt. The LLM sees 14-section extraction but the prompt only describes 8 sections. The 6 TDD sections (Data Models, API Specs, Components, Testing, Migration, Operational) are available but not directed toward.
**Fix:** Add instruction: "When the extraction document contains additional sections beyond the standard 8 (Data Models and Interfaces, API Specifications, Component Inventory, Testing Strategy, Migration and Rollout Plan, Operational Readiness), address each in the roadmap with specific implementation phases, tasks, and milestones."

### C-05: Dead `tdd_file` parameter in 5 prompt builders
**Severity:** IMPORTANT | **Sources:** Agent1 #2-#6
**Files:** `src/superclaude/cli/roadmap/prompts.py` — `build_extract_prompt`, `build_extract_prompt_tdd`, `build_generate_prompt`, `build_score_prompt`, `build_test_strategy_prompt`, `build_spec_fidelity_prompt`
**Bug:** All 6 builders accept `tdd_file` parameter but only `prd_file` has conditional blocks. The `tdd_file` is embedded via `step.inputs` but the prompt gives zero instructions for using it. This wastes context window on every pipeline run.
**Fix:** Either (a) add TDD supplementary blocks to each builder (preferred for generate, test-strategy, spec-fidelity where TDD content is directly relevant), or (b) remove `tdd_file` from signatures and stop embedding it in `step.inputs` for builders where it adds no value.

### C-06: Merge prompt has no PRD/TDD awareness (absorbs S-03 merge portion)
**Severity:** IMPORTANT | **Sources:** Agent1 #17, Agent2 F-16, Implementation task deferred S-03
**File:** `src/superclaude/cli/roadmap/prompts.py` L505-534
**Bug:** `build_merge_prompt()` is the only builder with no `tdd_file` or `prd_file` parameter. The merge step produces the final `roadmap.md` without any supplementary context, but downstream steps (score, fidelity, test-strategy) validate it WITH PRD context. This creates an unfair validation gap. Also include TDD/PRD in merge step's `inputs` list so the LLM can read the source documents.
**Fix:** Add `tdd_file` and `prd_file` parameters with supplementary blocks instructing the merge to preserve business-value ordering and technical specificity from the variants. (Diff/debate P3 blocks are lower priority — tracked separately in S-01.)

### C-07: `_restore_from_state` mutates config directly instead of `dataclasses.replace`
**Severity:** IMPORTANT | **Sources:** Agent1 #8
**File:** `src/superclaude/cli/roadmap/executor.py` L1725, L1742, L1751, L1762
**Bug:** Direct assignment (`config.agents = restored`) instead of immutable `dataclasses.replace()`. Inconsistent with `_build_steps()` which correctly uses `replace()`.
**Fix:** Collect all overrides, apply via single `dataclasses.replace()` call, return new config.

### C-08: `_restore_from_state` missing TDD fallback
**Severity:** IMPORTANT | **Sources:** Agent1 #1
**File:** `src/superclaude/cli/roadmap/executor.py` L1744-1764
**Bug:** On `--resume`, the TDD fallback (use `spec_file` as TDD when `input_type==tdd` and `tdd_file` is null) exists in `tasklist/commands.py` but NOT in `_restore_from_state()`. Inconsistent auto-wire behavior between resume and tasklist.
**Fix:** Add the same `elif state.get("input_type") == "tdd"` fallback block.

### C-09: `read_state` doesn't validate JSON is a dict
**Severity:** MINOR | **Sources:** Agent1 #15
**File:** `src/superclaude/cli/roadmap/executor.py` (read_state function)
**Bug:** If `.roadmap-state.json` contains valid JSON that isn't a dict (array, string), `state.get()` calls crash with AttributeError.
**Fix:** Add `return data if isinstance(data, dict) else None` after `json.loads()`.

### C-10: Step numbering comment error
**Severity:** MINOR | **Sources:** Agent1 #9, Agent2 F-22
**File:** `src/superclaude/cli/roadmap/executor.py` L1003
**Fix:** Change `# Step 8: Spec Fidelity` to `# Step 9: Spec Fidelity`.

### C-11: Stale "deferred" comment in generate prompt
**Severity:** MINOR | **Sources:** Agent2 F-21
**File:** `src/superclaude/cli/roadmap/prompts.py` L360-367
**Fix:** Update comment to reflect PRD block was added; TDD-specific section awareness still deferred.

---

## FIX NOW — Skill/CLI Consistency

### C-12: Detection rule divergence between CLI and skill layer
**Severity:** CRITICAL | **Sources:** Agent1 #11-#13, Agent2 F-01
**Files:** `scoring.md` L7-12, `extraction-pipeline.md` L143-148, `spec-panel.md` L32
**Bug:** Skill docs describe simple 3-condition OR rule. CLI uses weighted scoring with threshold ≥5. A document meeting only one skill condition may not meet the CLI threshold.
**Fix:** Update all 3 skill docs to describe the actual weighted scoring algorithm with threshold ≥5.

### C-13: Extraction sections mismatch (6 CLI vs 7 skill steps)
**Severity:** IMPORTANT | **Sources:** Agent2 F-02
**Files:** `prompts.py` vs `extraction-pipeline.md`
**Bug:** CLI has 6 TDD sections. Skill has 7 steps (includes `release_criteria` Step 11 with no CLI equivalent).
**Fix:** Either add `## Release Criteria` to `build_extract_prompt_tdd()` or remove Step 11 from skill.

### C-14: TDD complexity scoring formula not implemented in CLI
**Severity:** CRITICAL | **Sources:** Agent2 F-03
**Files:** `scoring.md` L70-108 vs CLI code
**Bug:** Skill defines a deterministic 7-factor formula. CLI delegates complexity to the LLM with no programmatic implementation. Downstream consumers may assume deterministic scoring.
**Fix:** Either implement the formula in post-extraction processing, or document explicitly that CLI scoring is LLM-delegated and the skill formula is advisory.

---

## FIX NOW — Test Gaps

### C-15: No integration tests for full data flow
**Severity:** CRITICAL | **Sources:** Agent2 F-05
**Fix:** Create integration tests covering detect→extract→gate→state→auto-wire flow.

### C-16: No tests for `build_extract_prompt_tdd` with `prd_file`
**Severity:** IMPORTANT | **Sources:** Agent2 F-06
**Fix:** Add prd_file parameter tests to `test_tdd_extract_prompt.py`.

### C-17: No tests for old-schema state file backward compat
**Severity:** IMPORTANT | **Sources:** Agent2 F-07
**Fix:** Add test with minimal state file (no tdd_file/prd_file/input_type fields).

### C-18: No explicit detection threshold boundary tests
**Severity:** MINOR | **Sources:** Agent2 F-10
**Fix:** Add tests at score=4 (spec) and score=5 (tdd) with different signal combinations.

---

## FIX NOW — Edge Cases

### C-19: No content validation on `--prd-file` / `--tdd-file` (absorbs S-01, S-02)
**Severity:** IMPORTANT | **Sources:** Agent2 F-08, Implementation task deferred S-01/S-02
**Bug:** `--prd-file` and `--tdd-file` accept any file that exists (Click `exists=True`). No validation that the file is actually a PRD or TDD. A user passing `--prd-file my-tdd.md` gets TDD content injected as "PRD context." The PRD blocks reference specific PRD sections (S5, S6, S7, S12, S17, S19) that won't exist in a TDD, causing garbage enrichment.
**Fix:** Add lightweight content checks at pipeline start: for `--prd-file`, check for PRD markers ("User Personas", "Success Metrics", "Product Requirements") in first 1000 bytes. For `--tdd-file`, check for TDD markers ("Technical Design Document", numbered sections). Emit warning if markers absent.

### C-20: Same file for `--tdd-file` and `--prd-file` not caught
**Severity:** MINOR | **Sources:** Agent2 F-09
**Fix:** Add duplicate-file check with warning.

### C-21: Domain keyword dictionary count note missing
**Severity:** MINOR | **Sources:** Agent1 #16
**Fix:** Add note in scoring.md explaining 5 vs 7 denominator relationship.

---

## TRULY DEFER — Requires Separate Extensive Work

### D-01: `superclaude tasklist generate` CLI
**Sources:** Agent2 F-14, PRD E2E follow-up, TDD E2E follow-up
**Why defer:** Requires new CLI command, executor, gates, state management — estimated 620-880 lines across 7-8 files. BUILD-REQUEST already written at `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/BUILD-REQUEST-tasklist-generate-cli.md`.
**Impact of deferral:** Full pipeline chain incomplete. Tasklist validation enrichment untestable E2E.

### D-02: Fingerprint threshold calibration
**Sources:** Agent2 F-19, PRD E2E fingerprint regression
**Why defer:** Needs empirical calibration across multiple pipeline runs. The 0.7 threshold is arbitrary. Need N>1 runs to establish variance bands.
**Impact of deferral:** TDD+PRD pipelines may intermittently fail fingerprint check.

---

## SHOULD DO SOON — High-Priority Additions

### S-01: P3 supplementary blocks for diff/debate (NOT merge — merge is C-06)
**Sources:** Implementation task deferred items, Agent1 #17
**What:** PRD/TDD blocks for diff and debate builders. Merge is already tracked as C-06 (Fix Now). Diff and debate have diminishing PRD/TDD returns.
**Priority:** LOW — merge (C-06) is the critical one; diff/debate are optional.

NOTE: S-01/S-02 (PRD/TDD structure validation) were duplicates of C-19 (no content validation on flags) — consolidated into C-19. S-03 (merge prompt) was duplicate of C-06 — only diff/debate portion remains here as S-01.

---

## Summary Counts

| Category | Count |
|----------|-------|
| Fix Now — Code Bugs | 11 (C-01 through C-11) |
| Fix Now — Skill/CLI Consistency | 3 (C-12 through C-14) |
| Fix Now — Test Gaps | 4 (C-15 through C-18) |
| Fix Now — Edge Cases | 3 (C-19 through C-21) |
| **Total Fix Now** | **21** |
| Truly Defer | 2 (D-01, D-02) |
| Should Do Soon | 3 (S-01 through S-03) |
| **Grand Total** | **26** |

## Priority Order for Fixes

1. **C-01** (deviation gate field mismatch) — one-line fix, unblocks deviation analysis
2. **C-02** (anti-instinct TRAILING mode) — one-line fix, unblocks test-strategy + spec-fidelity + remediation
3. **C-04** (generate prompt TDD awareness) — high-value prompt addition
4. **C-03** (fidelity dims 7-11 conditional) — prevents spec-path regression
5. **C-05** (dead tdd_file params) — either add blocks or remove dead params
6. **C-06** (merge prompt PRD/TDD) — closes the validation gap
7. **C-12** (detection rule alignment) — 3 skill doc updates
8. **C-14** (scoring formula documentation) — clarify contract
9. **C-15** (integration tests) — prevents regression in all above
10. All remaining items

---

## ROUND 2 FINDINGS (Agents 3 & 4)

### FIX NOW — Pre-Existing Bugs Exposed by TDD/PRD Work

### C-22: spec_parser requirement ID regex silently drops compound IDs
**Severity:** CRITICAL | **Source:** Agent3 E-01
**File:** `src/superclaude/cli/roadmap/spec_parser.py`
**Bug:** Regex patterns `FR-\d+` and `NFR-\d+` only match simple format (FR-001). All three test fixtures use compound IDs: `FR-AUTH-001` (TDD), `FR-AUTH.1` (spec), `NFR-AUTH.1` (spec). The parser extracts ZERO requirement IDs from real documents. The `check_signatures` phantom-ID detector runs against an empty spec ID set, flagging every roadmap reference as a phantom.
**Fix:** Update regex to handle compound formats: `FR-[A-Z]+-\d+`, `FR-[A-Z]+\.\d+`, etc.

### C-23: certify_prompts parser regex rejects all structural checker finding IDs
**Severity:** CRITICAL | **Source:** Agent3 E-02
**File:** `src/superclaude/cli/roadmap/certify_prompts.py`
**Bug:** Parser regex `F-\d+` expects finding IDs like `F-001` but structural checkers produce IDs in `dimension-type-hash` format. Certification always reports 0 findings verified, causing unconditional failure.
**Fix:** Update regex to match actual finding ID format.

### C-24: DIMENSION_SECTION_MAP hardcoded to release-spec numbering
**Severity:** CRITICAL | **Source:** Agent3 E-03
**File:** `src/superclaude/cli/roadmap/structural_checkers.py`
**Bug:** Section mapping (Section 3 = FRs, Section 4 = Data Models) matches release-spec template only. TDD uses different numbering (Section 5 = Requirements, Section 7 = Data Models). Structural checkers receive empty section lists for TDD input, producing false negatives — silently missing structural issues.
**Fix:** Make section mapping conditional on input type or detect section numbers from the actual document headings.

### FIX NOW — Data Flow Issues

### C-25: _embed_inputs labels files by path only — no semantic role markers
**Severity:** IMPORTANT | **Source:** Agent4 DF-02
**File:** `src/superclaude/cli/roadmap/executor.py` (_embed_inputs function)
**Bug:** When multiple files are embedded (spec + TDD + PRD), they're labeled only by filesystem path. The LLM must infer which is the primary input vs supplementary PRD vs supplementary TDD from the path name alone. No "## Primary Input" / "## Supplementary PRD Context" markers.
**Fix:** Add semantic role labels to embedded content: `## Primary Input: {filename}`, `## Supplementary PRD Context: {filename}`, etc.

### C-26: Score step prompt exceeds _EMBED_SIZE_LIMIT with real test data
**Severity:** IMPORTANT | **Source:** Agent4 DF-03
**File:** `src/superclaude/cli/roadmap/executor.py`
**Bug:** With real fixtures (TDD 876 lines + PRD 406 lines + debate + variants), the score step prompt exceeds the `_EMBED_SIZE_LIMIT` of 120KB. The warning is emitted ("composed prompt exceeds 102400 bytes; embedding inline anyway") but execution continues. On Linux where `MAX_ARG_STRLEN` = 128KB per argument, this could cause subprocess failure.
**Fix:** Implement file-based input fallback (`--file` flag) when prompt exceeds size limit, or reduce what's embedded in the score step.

### C-27: --resume with --prd-file doesn't override state-restored prd_file
**Severity:** IMPORTANT | **Source:** Agent4 DF-05
**File:** `src/superclaude/cli/roadmap/executor.py` (_restore_from_state)
**Bug:** On `--resume`, `_restore_from_state()` writes `config.prd_file = prd_path` from state. If the user also passes `--prd-file different.md` on the resume command, the explicit flag should take precedence but the restoration happens after config construction — potentially overwriting the explicit flag.
**Fix:** Add precedence check: only restore from state when the config field is None (explicit flag not provided).

### C-28: _embed_inputs no handling for empty or binary files
**Severity:** MINOR | **Source:** Agent4 DF-04
**File:** `src/superclaude/cli/roadmap/executor.py`
**Bug:** If `--prd-file` points to an empty file (0 bytes) or a binary file, `_embed_inputs` reads and embeds it without any check. An empty file wastes a labeled section; a binary file corrupts the prompt.
**Fix:** Skip files with 0 bytes (with warning). Validate content is valid UTF-8 before embedding.

### C-29: _save_state writes only after all steps complete
**Severity:** MINOR | **Source:** Agent4 DF-06
**File:** `src/superclaude/cli/roadmap/executor.py`
**Bug:** State is written once after the pipeline finishes (or fails). If the process is killed mid-pipeline, no state file exists and `--resume` can't recover. Each step's output files exist on disk but there's no state tracking of which passed.
**Fix:** Write state incrementally after each step completes (or at minimum after each gate passes).

### FIX NOW — Fixture & Test Issues

### C-30: Fingerprint extraction ignores file paths, API endpoints, data model field names
**Severity:** IMPORTANT | **Source:** Agent3 E-04
**File:** `src/superclaude/cli/roadmap/fingerprint.py`
**Bug:** Fingerprint extraction only captures backtick-delimited identifiers ≥4 chars, `def/class` in code blocks, and ALL_CAPS constants. It misses: API endpoint paths (`/auth/login`), data model field names without backticks (`email`, `displayName`), TypeScript interface names in ```ts blocks. For TDD input with rich API specs and data models, this limits fingerprint coverage.
**Fix:** Extend extraction to include URL path patterns and interface/type names from fenced code blocks.

### C-31: Test fixture TDD has inconsistent data model field naming
**Severity:** MINOR | **Source:** Agent3 E-09
**File:** `.dev/test-fixtures/test-tdd-user-auth.md`
**Bug:** TypeScript interface `UserProfile` uses `displayName` but the field table below it may use `display_name`. Inconsistent casing between code and table.
**Fix:** Align field names between code blocks and tables.

### C-32: Test fixtures have conflicting architecture (Redis in TDD, not in spec)
**Severity:** MINOR | **Source:** Agent3 E-10
**Files:** `.dev/test-fixtures/test-tdd-user-auth.md`, `.dev/test-fixtures/test-spec-user-auth.md`
**Bug:** TDD mentions Redis for token storage; spec doesn't mention Redis. Cross-test comparisons may attribute this difference to TDD/spec divergence rather than fixture inconsistency.
**Fix:** Either add Redis to spec fixture or document the intentional scope difference.

### C-33: _FINDING_COUNTER dead global state
**Severity:** MINOR | **Source:** Agent3 E-08
**File:** (location TBD — Agent3 referenced it but didn't specify file)
**Bug:** A global `_FINDING_COUNTER` variable is declared but never incremented or used.
**Fix:** Remove dead code.

### C-34: Tests use toy data that can't catch prompt size issues
**Severity:** IMPORTANT | **Source:** Agent4 DF-10
**Files:** `tests/roadmap/`, `tests/tasklist/`
**Bug:** All unit tests create 1-line dummy Path files. They verify prompt string content but can never catch size-related issues (C-26). A test with a real 800-line TDD fixture would catch the _EMBED_SIZE_LIMIT warning.
**Fix:** Add at least one test that uses realistic file sizes and verifies the prompt stays within limits.

### C-35: PRD prompt section numbers don't match PRD fixture headings
**Severity:** IMPORTANT | **Source:** Agent3 E-11, Agent4 DF-08
**Files:** `src/superclaude/cli/roadmap/prompts.py` (PRD blocks), `.dev/test-fixtures/test-prd-user-auth.md`
**Bug:** PRD supplementary blocks reference S7 (User Personas), S12 (Scope Definition), S17 (Legal & Compliance), S19 (Success Metrics). The PRD fixture uses descriptive headings without section numbers. The LLM infers correctly from heading names, but if a PRD uses different heading names (e.g., "Target Users" instead of "User Personas"), the mapping breaks silently.
**Fix:** Add heading name hints alongside section numbers in prompts: "User Personas section (S7, typically titled 'User Personas' or 'Target Users')".

### C-36: Branch has uncommitted distributable changes
**Severity:** IMPORTANT | **Source:** Agent3 E-06
**Bug:** `make verify-sync` still shows drift. The branch has modifications to distributable files that haven't been committed. Risk of losing work.
**Fix:** Run `make sync-dev`, commit all changes to `feat/tdd-spec-merge`.

---

## UPDATED SUMMARY

| Category | Prior (Agents 1-2) | New (Agents 3-4) | Total |
|----------|-------------------|-------------------|-------|
| Fix Now — Code Bugs | 11 | 8 | 19 |
| Fix Now — Skill/CLI Consistency | 3 | 0 | 3 |
| Fix Now — Test Gaps | 4 | 2 | 6 |
| Fix Now — Edge Cases | 3 | 0 | 3 |
| Fix Now — Fixture Issues | 0 | 2 | 2 |
| Fix Now — Data Flow | 0 | 3 | 3 |
| **Total Fix Now** | **21** | **15** | **36** |
| Truly Defer | 2 | 0 | 2 |
| Should Do Soon | 3 | 0 | 3 |
| **Grand Total** | **26** | **15** | **41** |

## UPDATED PRIORITY ORDER

1. **C-01** (deviation gate field mismatch) — one-line fix
2. **C-02** (anti-instinct TRAILING mode) — one-line fix, unblocks entire downstream
3. **C-22** (spec_parser compound ID regex) — pre-existing, affects all real documents
4. **C-23** (certify parser regex) — pre-existing, blocks certification
5. **C-24** (DIMENSION_SECTION_MAP for TDD) — pre-existing, structural checkers blind to TDD
6. **C-04** (generate prompt TDD awareness) — high-value prompt fix
7. **C-03** (fidelity dims 7-11 conditional) — spec-path regression
8. **C-25** (embed semantic role markers) — improves LLM accuracy
9. **C-26** (score step size limit) — Linux deployment blocker
10. **C-36** (commit changes) — risk of work loss
11. **C-05/C-06** (dead params, merge prompt) — cleanup + quality
12. **C-12/C-14** (skill alignment, scoring docs) — consistency
13. **C-15/C-34** (integration tests, realistic test sizes) — regression prevention
14. All remaining items

---

## ROUND 3 FINDINGS (Agents 5 & 6)

### FIX NOW — Sub-Pipeline TDD/PRD Blindness

### C-37: Validation sub-pipeline has zero TDD/PRD awareness
**Severity:** IMPORTANT | **Source:** Agent5 E-01
**Files:** `src/superclaude/cli/roadmap/validate_executor.py`, `validate_prompts.py`, `validate_gates.py`
**Bug:** The `superclaude roadmap validate` sub-pipeline runs structural checks on the roadmap but has no knowledge of TDD/PRD supplementary files. It can't validate TDD-specific roadmap content or PRD-driven prioritization.
**Fix:** Pass tdd_file/prd_file through validate executor to prompts where relevant.

### C-38: Remediation sub-pipeline has zero TDD/PRD awareness
**Severity:** IMPORTANT | **Source:** Agent5 E-02
**Files:** `src/superclaude/cli/roadmap/remediate.py`, `remediate_executor.py`, `remediate_prompts.py`
**Bug:** Remediation generates a tasklist from structural findings but doesn't know about TDD/PRD. Remediation tasks won't reference TDD components or PRD business context.
**Fix:** Pass supplementary file context to remediation prompt builder.

### C-39: convergence fidelity checker scans hardcoded `src/superclaude` path
**Severity:** IMPORTANT | **Source:** Agent5 E-03
**File:** `src/superclaude/cli/roadmap/convergence.py`
**Bug:** The convergence engine's fidelity checker appears to hardcode a scan path that may not apply to all projects.
**Fix:** Make scan path configurable or derive from config.

### FIX NOW — Scanner & Checker Bugs

### C-40: Obligation scanner position calculation matches wrong section
**Severity:** IMPORTANT | **Source:** Agent5 E-04
**File:** `src/superclaude/cli/roadmap/obligation_scanner.py`
**Bug:** `_get_absolute_position` uses `content.find(section_text)` which returns the FIRST occurrence. If the same text appears in multiple sections, it attributes the obligation to the wrong phase.
**Fix:** Use section-aware position lookup that respects heading boundaries.

### C-41: Integration contract coverage has no per-contract filtering
**Severity:** IMPORTANT | **Source:** Agent5 E-05
**File:** `src/superclaude/cli/roadmap/integration_contracts.py`
**Bug:** `check_roadmap_coverage` matches ANY wiring task pattern to ANY contract. A wiring task for contract A could satisfy the coverage check for contract B.
**Fix:** Add contract-specific matching that ties wiring tasks to their specific dispatch patterns.

### C-42: Obligation scanner discharge check uses substring matching
**Severity:** IMPORTANT | **Source:** Agent5 E-13
**File:** `src/superclaude/cli/roadmap/obligation_scanner.py`
**Bug:** `_has_discharge` checks if a component name is a substring of discharge text. "Auth" would match "AuthService" AND "AuthorizationManager" AND "authentication" — producing false discharge matches.
**Fix:** Use word-boundary matching for component names.

### FIX NOW — Convergence Engine Issues

### C-43: Convergence regression handler is a no-op stub
**Severity:** IMPORTANT | **Source:** Agent5 E-06
**File:** `src/superclaude/cli/roadmap/convergence.py`
**Bug:** The regression handler copies the registry but does not re-run checkers after remediation. Regressions introduced by remediation go undetected.
**Fix:** Re-run structural checkers after remediation to catch regressions.

### C-44: _write_convergence_report hardcodes medium/low counts to 0
**Severity:** IMPORTANT | **Source:** Agent5 E-10
**File:** `src/superclaude/cli/roadmap/convergence.py`
**Bug:** The convergence report always shows medium_severity_count=0, low_severity_count=0 regardless of actual findings.
**Fix:** Compute counts from actual findings.

### C-45: Registry not saved on early convergence exit
**Severity:** IMPORTANT | **Source:** Agent5 E-24
**File:** `src/superclaude/cli/roadmap/convergence.py`
**Bug:** If convergence exits early (budget exceeded, max iterations), the deviation registry's budget snapshot is not flushed before write.
**Fix:** Flush registry before any exit path.

### FIX NOW — _restore_from_state Issues

### C-46: _restore_from_state assigns unvalidated state values to typed fields
**Severity:** CRITICAL | **Source:** Agent5 E-07
**File:** `src/superclaude/cli/roadmap/executor.py`
**Bug:** State file values are assigned directly to config fields without type validation. If state file has `depth: 42` (not a valid Literal), the config accepts it. If `agents` is malformed, the list comprehension may crash.
**Fix:** Validate state values against expected types before assignment.

### FIX NOW — Code Quality Issues

### C-47: Duplicate _embed_inputs and _sanitize_output implementations
**Severity:** MINOR | **Source:** Agent5 E-08
**File:** Multiple executor files
**Bug:** The same utility functions are reimplemented across executor files rather than shared.
**Fix:** Extract to a shared utility module.

### C-48: _extract_by_section heading level calculation wrong
**Severity:** MINOR | **Source:** Agent5 E-19
**Bug:** The heading level calculation for section extraction produces incorrect results for certain heading patterns.
**Fix:** Review and fix heading level logic.

### C-49: spec_structural_audit divides by zero
**Severity:** MINOR | **Source:** Agent5 E-21
**File:** `src/superclaude/cli/roadmap/spec_structural_audit.py`
**Bug:** `check_extraction_adequacy` divides by `total_structural_indicators` which can be 0.
**Fix:** Guard against zero division.

### C-50: No logging of TDD/PRD decisions
**Severity:** IMPORTANT | **Source:** Agent5 E-20
**File:** `src/superclaude/cli/roadmap/executor.py`
**Bug:** Auto-detection result, PRD enrichment activation, TDD fallback, and redundancy guard are not logged at INFO level. Users can't debug pipeline behavior from logs.
**Fix:** Add `_log.info()` calls for each TDD/PRD decision point.

### C-51: spec_patch.py doesn't handle TDD/PRD file references
**Severity:** IMPORTANT | **Source:** Agent5 E-09
**File:** `src/superclaude/cli/roadmap/spec_patch.py`
**Bug:** The spec patching system that applies remediation fixes back to the source document doesn't know about TDD/PRD file references in the state file.
**Fix:** Pass supplementary file context through spec patch workflow.

### C-52: _check_cross_file_coherence removes from list during iteration
**Severity:** IMPORTANT | **Source:** Agent5 E-18
**File:** `src/superclaude/cli/roadmap/remediate_executor.py`
**Bug:** Modifying a list while iterating over it can skip items or crash.
**Fix:** Iterate over a copy or collect items to remove and apply after iteration.

### FIX NOW — Edge Cases (Agent 6)

### C-53: No validation of --input-type vs actual file content
**Severity:** IMPORTANT | **Source:** Agent6 E-02
**File:** `src/superclaude/cli/roadmap/commands.py`
**Bug:** `--input-type tdd` on a spec file forces TDD extraction on spec content. The existing warning only checks for "Technical Design Document" in first 500 bytes — a spec that happens to mention TDD won't be caught. No warning for `--input-type spec` on a TDD file.
**Fix:** Warn when forced input type contradicts auto-detection result.

### C-54: _embed_inputs crashes on UTF-16 encoded files
**Severity:** MINOR | **Source:** Agent6 E-03
**Bug:** Files encoded as UTF-16 crash during read. Only UTF-8 is handled.
**Fix:** Add encoding detection or try/except with fallback.

### C-55: Passing PRD as primary input silently misclassifies
**Severity:** IMPORTANT | **Source:** Agent6 E-04
**Bug:** `superclaude roadmap run prd.md` runs the PRD through spec extraction (auto-detects as "spec"). No warning that the input is a PRD, not a spec/TDD. The extraction will be poor quality since PRD content doesn't match spec extraction patterns.
**Fix:** Add PRD detection signal (check for "Product Requirements" type field) and warn.

### C-56: No lock mechanism on .roadmap-state.json for concurrent runs
**Severity:** MINOR | **Source:** Agent6 E-06
**Bug:** Two concurrent pipeline runs to the same output directory can corrupt the state file. `_save_state` uses atomic rename but two writers racing can still lose data.
**Fix:** Add advisory file lock or document that concurrent runs to the same directory are unsupported.

### C-57: Prompt injection via malicious PRD/TDD content
**Severity:** IMPORTANT | **Source:** Agent6 E-07
**Bug:** File content is embedded raw into prompts via `_embed_inputs`. A malicious PRD/TDD could contain "IGNORE ALL PREVIOUS INSTRUCTIONS" or similar prompt injection. No sanitization of embedded content.
**Fix:** Add content sanitization or document the trust model (supplementary files are trusted inputs).

### C-58: --agents with empty string crashes
**Severity:** MINOR | **Source:** Agent6 E-09
**Bug:** `--agents ""` causes IndexError during agent spec parsing.
**Fix:** Validate non-empty before parsing.

### C-59: spec_type enum divergence between templates
**Severity:** MINOR | **Source:** Agent6 E-12
**Files:** TDD template, release-spec-template
**Bug:** The `spec_type` enum values may differ between the two templates.
**Fix:** Verify both templates use the same enum values.

### C-60: Guardrail "do NOT treat PRD as hard requirements" may be ineffective
**Severity:** MINOR | **Source:** Agent6 E-15
**Bug:** LLMs may not reliably follow negative instructions. The guardrail could be ignored, causing PRD narrative to be treated as engineering requirements.
**Fix:** Document as known limitation. Consider positive framing: "Use PRD content ONLY to inform prioritization and acceptance criteria, not as implementation requirements."

### C-61: TDD template sentinel says complexity fields "may remain empty" but pipeline expects them
**Severity:** IMPORTANT | **Source:** Agent6 E-16
**File:** `src/superclaude/examples/tdd_template.md`
**Bug:** The sentinel self-check says `complexity_score` and `complexity_class` "may remain empty (computed by sc:roadmap)". But the EXTRACT_GATE requires `complexity_class` to be LOW/MEDIUM/HIGH. If a user leaves them empty as instructed, the pipeline fills them during extraction — but if the extraction LLM also leaves them empty, the gate fails.
**Fix:** Clarify: "may remain empty in the template — the pipeline's extraction step will compute these values."

---

## FINAL UPDATED SUMMARY

| Category | Rounds 1-2 | Round 3 | Total |
|----------|-----------|---------|-------|
| Fix Now — Code Bugs | 19 | 12 | 31 |
| Fix Now — Skill/CLI Consistency | 3 | 0 | 3 |
| Fix Now — Test Gaps | 6 | 0 | 6 |
| Fix Now — Edge Cases | 3 | 6 | 9 |
| Fix Now — Sub-Pipeline Blindness | 0 | 3 | 3 |
| Fix Now — Convergence Engine | 0 | 3 | 3 |
| Fix Now — Fixture Issues | 2 | 0 | 2 |
| Fix Now — Data Flow | 3 | 0 | 3 |
| **Total Fix Now** | **36** | **25** | **61** |
| Truly Defer | 2 | 0 | 2 |
| Should Do Soon | 3 | 0 | 3 |
| **Grand Total** | **41** | **31** | **72** |

Note: Some Round 3 Agent 5/6 findings were duplicates of existing items (6 from Agent 6, 4 from Agent 5 = 10 duplicates removed from the 41 raw findings).

---

## ROUND 4 FINDINGS (Agents 7 & 8) — 20 new unique

### FIXED DURING QA

### C-62: input_type "auto" still written to state file (prior fix was incomplete)
**Severity:** CRITICAL | **Source:** Agent8 M-01
**Bug:** Our Round 2 fix at `_build_steps` line 859 created a LOCAL config via `dataclasses.replace` — the caller (`execute_roadmap`) still had `input_type="auto"` when it called `_save_state`. The fix was scoped to the wrong function.
**Fix applied:** Moved resolution to `execute_roadmap()` BEFORE `_build_steps()` call (both main and resume paths). Updated `test_auto_invoke_after_success` to expect resolved input_type="spec". All tests pass.

### FIX NOW — YAML/Frontmatter Parsing

### C-63: Frontmatter regex rejects hyphenated field names
**Severity:** IMPORTANT | **Source:** Agent7
**Bug:** Pipeline frontmatter parser may reject `high-severity-count` (hyphens) vs expected `high_severity_count` (underscores).
**Fix:** Normalize field names or accept both.

### C-64: Frontmatter regex breaks on blank lines within frontmatter
**Severity:** IMPORTANT | **Source:** Agent7
**Bug:** Blank line before closing `---` may split parse incorrectly.
**Fix:** Make parser tolerant of blank lines within frontmatter.

### C-65: Frontmatter regex false positives on `---` in content
**Severity:** MINOR | **Source:** Agent7
**Bug:** Horizontal rules (`---`) in markdown body misinterpreted as frontmatter delimiters.
**Fix:** Only match `---` at file start for opening delimiter.

### FIX NOW — Build/Package

### C-66: pyproject force-include may double files in wheel
**Severity:** IMPORTANT | **Source:** Agent7
**Fix:** Audit force-include paths for overlap.

### C-67: Makefile .DS_Store causes false sync drift
**Severity:** MINOR | **Source:** Agent7
**Fix:** Exclude .DS_Store from diff.

### C-68: Makefile paths with spaces break
**Severity:** IMPORTANT | **Source:** Agent7
**Fix:** Quote all path references.

### FIX NOW — Code Quality

### C-69: TaskStatus enum collision/inconsistency
**Severity:** IMPORTANT | **Source:** Agent7
**Fix:** Audit enum values.

### C-70: Parallel executor prints to stdout
**Severity:** MINOR | **Source:** Agent7
**Fix:** Use stderr or logging.

### C-71: Doctor missing pipeline health checks
**Severity:** MINOR | **Source:** Agent7
**Fix:** Add TDD/PRD flag checks.

### C-72: Dead deprecation shim
**Severity:** MINOR | **Source:** Agent7
**Fix:** Remove.

### C-73: Confidence checker mutates input
**Severity:** MINOR | **Source:** Agent7
**Fix:** Copy before mutation.

### C-74: Reflexion creates directories on init
**Severity:** MINOR | **Source:** Agent7
**Fix:** Lazy creation.

### FIX NOW — Prompt Quality

### C-75: build_tasklist_generate_prompt references wrong PRD sections for acceptance scenarios
**Severity:** MINOR | **Source:** Agent8 M-02
**Fix:** Correct S7/S22 references to S14/S21.

### C-76: Bare f-string prefixes with no interpolation
**Severity:** MINOR | **Source:** Agent8 M-05/M-06
**Fix:** Remove unnecessary f-string prefixes.

### C-77: Cross-module import of private _OUTPUT_FORMAT_BLOCK
**Severity:** MINOR | **Source:** Agent8 M-09
**Fix:** Make public or move to shared module.

### C-78: Redundant Path() wrapping
**Severity:** MINOR | **Source:** Agent8 M-03/M-04
**Fix:** Remove redundant wrapping.

---

---

## ROUND 5 FINDINGS (Agents 9 & 10) — 11 new unique

### FIX NOW — Gate & Parser Bugs (CRITICAL)

### C-79: Semantic layer call-site passes wrong argument types
**Severity:** CRITICAL | **Source:** Agent9
**File:** `src/superclaude/cli/roadmap/executor.py` L671-677 vs `semantic_layer.py` L377-384
**Bug:** `run_semantic_layer` is called with `spec_path=str(...)` and `roadmap_path=str(...)` but the function signature expects `spec_sections: list[Any]` and `roadmap_sections: list[Any]`. TypeError is swallowed by `except Exception`. The semantic layer NEVER actually executes.
**Fix:** Fix the call-site to pass correct argument types, or fix the function signature.

### C-80: _frontmatter_values_non_empty checks ALL fields, not just required ones
**Severity:** CRITICAL | **Source:** Agent9
**File:** `src/superclaude/cli/roadmap/gates.py` L110-118
**Bug:** The semantic check iterates over ALL frontmatter fields and fails if ANY has an empty value — including optional fields like `pipeline_diagnostics`. This causes spurious gate failures when the LLM produces optional empty fields alongside required non-empty fields.
**Fix:** Only check fields listed in `required_frontmatter_fields`, not all parsed fields.

### C-81: _parse_frontmatter drops YAML list continuation lines
**Severity:** CRITICAL | **Source:** Agent9
**File:** `src/superclaude/cli/roadmap/gates.py` L147-168
**Bug:** The hand-rolled YAML parser treats everything as strings. YAML lists like `domains_detected: [backend, security]` on one line work, but block-style lists (multi-line with `- item`) have continuation lines dropped. `domains_detected` could appear missing even when present in block format.
**Fix:** Use a proper YAML parser (`yaml.safe_load`) or handle block-style lists in the hand-rolled parser.

### FIX NOW — Code Issues

### C-82: sys.path pollution in main.py
**Severity:** IMPORTANT | **Source:** Agent9 I-02
**File:** `src/superclaude/cli/main.py` L13
**Bug:** Unconditional `sys.path.insert(0, ...)` at import time pollutes sys.path for every CLI invocation.
**Fix:** Guard with `if ... not in sys.path` or remove if unnecessary.

### C-83: _embed_inputs raises unhandled FileNotFoundError
**Severity:** IMPORTANT | **Source:** Agent9 I-03
**File:** `src/superclaude/cli/roadmap/executor.py` L134-147
**Bug:** If any input file in the `inputs` list doesn't exist (deleted between step construction and execution), `_embed_inputs` raises unhandled FileNotFoundError with no graceful recovery.
**Fix:** Add try/except with descriptive error message identifying which input file is missing.

### C-84: Double auto-detection still exists (shadow in _build_steps)
**Severity:** IMPORTANT | **Source:** Agent9 I-01
**File:** `src/superclaude/cli/roadmap/executor.py` L853-859
**Bug:** After our C-62 fix, `execute_roadmap` resolves input_type before calling `_build_steps`. But `_build_steps` still has its own resolution code at L853-859 that creates a local `config = dataclasses.replace(...)`. This is now a no-op (input_type is already resolved) but the dead code is confusing and the local `config` shadows the parameter.
**Fix:** Remove the resolution code from `_build_steps` since it's now done in `execute_roadmap`. Keep only the redundancy guard.

### FIX NOW — Minor Issues

### C-85: Fidelity batch scripts hardcode container path
**Severity:** MINOR | **Source:** Agent9 M-01
**Bug:** Container-specific path `/config/workspace/` hardcoded in batch scripts.
**Fix:** Make configurable.

### C-86: prd/tdd skills lack sc- prefix, bypass duplicate filter
**Severity:** MINOR | **Source:** Agent9 M-02
**Bug:** Skills named `prd` and `tdd` (not `sc-prd`, `sc-tdd`) bypass the install duplicate-checking filter.
**Fix:** Either rename to `sc-prd`/`sc-tdd` or update the filter.

### C-87: Section notation ambiguity (S vs §) in tasklist prompts
**Severity:** MINOR | **Source:** Agent10
**File:** `src/superclaude/cli/tasklist/prompts.py` L180-194
**Bug:** `build_tasklist_generate_prompt` uses `S7, S8` prefix while `build_tasklist_fidelity_prompt` uses `§15, §19`. When both TDD and PRD are present, `S7` is ambiguous — TDD S7 = Data Models, PRD S7 = User Personas.
**Fix:** Adopt `§` notation for TDD sections consistently, or use full heading names.

### C-88: Minimal CLI help text for --tdd-file and --prd-file
**Severity:** MINOR | **Source:** Agent10
**File:** `src/superclaude/cli/roadmap/commands.py` L112-122
**Bug:** Help strings don't explain which pipeline steps are affected, redundancy guard, or auto-wire behavior.
**Fix:** Expand help text with usage examples.

### C-89: No user-facing documentation for three-way flag interaction
**Severity:** MINOR | **Source:** Agent10
**Bug:** No docs explain how `--input-type`, `--tdd-file`, and `--prd-file` interact together.
**Fix:** Add usage guide or expand --help.

---

## GRAND TOTAL (5 rounds, 10 agents)

| Round | Agents | Raw Findings | Duplicates | New Unique | Running Total |
|-------|--------|-------------|------------|------------|---------------|
| 1 | 1, 2 | 38 | 17 | 26 | 26 |
| 2 | 3, 4 | 20 | 5 | 15 | 41 |
| 3 | 5, 6 | 41 | 10 | 31 | 72 |
| 4 | 7, 8 | 27 | 7 | 20 | 92 |
| 5 | 9, 10 | 12 | 1 | 11 | 103 |
| dedup pass | — | — | 2 | -2 | 101 |
| **Total** | **10** | **138** | **42** | **101** | **101** |

**Deduplicated items:**
- S-01/S-02 (PRD/TDD structure validation) merged into C-19 (no content validation on flags)
- S-03 merge portion merged into C-06 (merge prompt no PRD/TDD). Only diff/debate remains as S-01.

**After round 5: 101 unique findings**

---

## ROUND 6 FINDINGS (Agents 11 & 12) — 15 new unique (5 duplicates removed from 20 raw)

**Duplicates removed:** C-90 (=C-06 merge), C-92 (=C-84 double detect), C-94 (=S-01 diff/debate), C-102 (=C-62 input_type, state file from pre-fix E2E run), C-109 (=C-83 FileNotFoundError)

### TDD/PRD Findings (7)

### C-91: _restore_from_state doesn't restore input_type on --resume
**Severity:** IMPORTANT | **Tag:** [TDD/PRD] | **Source:** Agent11
**File:** `src/superclaude/cli/roadmap/executor.py` (_restore_from_state)
**Bug:** On `--resume`, `_restore_from_state` restores `agents`, `depth`, `tdd_file`, `prd_file` from state — but NOT `input_type`. The config retains whatever `input_type` was passed on the resume command (likely "auto"), which triggers re-detection. If the resolved type differs between original and resume (unlikely but possible if file changed), behavior is inconsistent.
**Fix:** Restore `input_type` from state alongside other fields.

### C-93: Test docstring claims "5 comparison dimensions" but prompt has 11+
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent11
**Bug:** Test documentation/docstrings reference the pre-TDD dimension count (5-6) but the fidelity prompt now has 11 standard + 4 PRD conditional dimensions.
**Fix:** Update test docstrings to reflect current dimension count.

### C-98: build_extract_prompt and build_extract_prompt_tdd have identical PRD blocks
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent11
**Bug:** Both extractors have the same 5-check PRD supplementary block. The TDD extractor could have a lighter PRD block (TDD already has technical content that overlaps with some PRD checks). Having them identical isn't wrong but may produce redundant extraction when TDD already covers compliance/scope.
**Fix:** Document as intentional, or tailor the TDD extractor's PRD block to avoid overlap.

### C-103: Minimal TDDs below detection threshold produce no borderline warning
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent12
**Bug:** A TDD that scores 3-4 (below ≥5 threshold) is silently classified as "spec." No warning that the document was close to the TDD threshold. User has no way to know auto-detection almost chose TDD.
**Fix:** Log a warning when score is between 3-4: "Document scored N (threshold 5) — classified as spec but has some TDD characteristics. Use --input-type tdd to force TDD extraction."

### C-104: Tasklist fidelity doesn't validate S5-derived priority ordering
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent12
**Bug:** The PRD fidelity block checks persona coverage, success metrics, and acceptance scenarios — but doesn't validate that the tasklist respects business priority ordering from PRD S5 (Business Context).
**Fix:** Add priority ordering check to PRD fidelity block.

### C-105: Tasklist fidelity doesn't validate S8/S7 enrichment completeness
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent12
**Bug:** The fidelity block doesn't verify that enrichment from S8 (Value Proposition) and S7 (User Personas) is actually reflected in task descriptions — only checks presence of persona references, not quality.
**Fix:** Add quality check or document as out-of-scope for automated validation.

### Pre-Existing Findings (8)

### C-95: fidelity_checker.py scans only Python files
**Severity:** IMPORTANT | **Tag:** [PRE-EXISTING] | **Source:** Agent11
**File:** `src/superclaude/cli/roadmap/fidelity_checker.py`
**Bug:** File scanning only covers `.py` files. Projects with JS/TS/Go/Rust code have their implementation files invisible to fidelity checking.
**Fix:** Extend to common language extensions or make configurable.

### C-96: fidelity_checker partial-match marks found=True, swallows gaps
**Severity:** IMPORTANT | **Tag:** [PRE-EXISTING] | **Source:** Agent11
**Bug:** A partial match on a requirement ID marks the entire requirement as found, hiding actual coverage gaps.
**Fix:** Distinguish partial vs full matches; flag partial as warnings.

### C-97: fidelity_checker _STOP_WORDS contains "sets" but not "set"
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent11
**Fix:** Add "set" to stop words.

### C-99: _derive_fidelity_status uses string search instead of YAML parsing
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent11
**Fix:** Use proper YAML parsing for status derivation.

### C-100: Sprint executor doesn't read .roadmap-state.json
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent11
**Bug:** Sprint runner doesn't know about the roadmap state file. It can't leverage input_type, tdd_file, or prd_file information during sprint execution.
**Fix:** Document as future enhancement or pass state context to sprint phases.

### C-106: _extract_field regex may capture trailing content
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent12
**Fix:** Tighten regex to stop at line boundary.

### C-107: remediate_parser overlay regexes hardcode column count
**Severity:** IMPORTANT | **Tag:** [PRE-EXISTING] | **Source:** Agent12
**Fix:** Make column count dynamic.

### C-108: _cross_refs_resolve gate check always returns True
**Severity:** IMPORTANT | **Tag:** [PRE-EXISTING] | **Source:** Agent12
**Bug:** The cross-reference resolution check is registered as a semantic check but always returns True — it's a no-op.
**Fix:** Either implement the check or remove it from the gate.

### C-110: Gate failure messages lack actual values
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent12
**Bug:** When a gate fails, the error message says what was expected but not what was actually found.
**Fix:** Include actual values in failure messages.

---

## GRAND TOTAL (6 rounds, 12 agents)

| Round | Agents | Raw | Dupes | New Unique | Running Total |
|-------|--------|-----|-------|------------|---------------|
| 1 | 1, 2 | 38 | 17 | 26 | 26 |
| 2 | 3, 4 | 20 | 5 | 15 | 41 |
| 3 | 5, 6 | 41 | 10 | 31 | 72 |
| 4 | 7, 8 | 27 | 7 | 20 | 92 |
| 5 | 9, 10 | 12 | 1 | 11 | 103 |
| dedup | — | — | 2 | -2 | 101 |
| 6 | 11, 12 | 20 | 5 | 15 | 116 |
| **Total** | **12** | **158** | **47** | **116** | **116** |

**Round 6 breakdown: 7 TDD/PRD + 8 pre-existing = 15 new**

**Final count: 116 unique findings**
- Truly Defer: 2 (D-01, D-02)
- Should Do Soon: 1 (S-01)
- Fix Now: 110
- Fixed During QA: 3

**Fixes applied during QA rounds:** 4 code changes (input_type resolution x2, auto-wire TDD fallback, test update).

---

## ROUND 7 FINDINGS (Agents 13 & 14) — 7 new unique (1 duplicate removed from 8 raw)

**Duplicate removed:** C-118 (obligation scanner position) = C-40

### TDD/PRD (4)

### C-111: Redundancy guard nullifies tdd_file in local config only — state file saves the un-nulled value
**Severity:** IMPORTANT | **Tag:** [TDD/PRD] | **Source:** Agent14
**File:** `src/superclaude/cli/roadmap/executor.py` (_build_steps redundancy guard)
**Bug:** The redundancy guard at line 862 does `config = dataclasses.replace(config, tdd_file=None)` — but this is LOCAL to `_build_steps`. The caller's config still has the original `tdd_file`. `_save_state` writes the un-nulled `tdd_file` to state. On resume or auto-wire, the "ignored" tdd_file reappears. Same class of bug as C-62 (local config not propagated).
**Fix:** Move the redundancy guard to `execute_roadmap()` alongside the input_type resolution, before `_build_steps()`.

### C-113: effective_input_type becomes pointless alias after C-84 fix
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent14
**Bug:** If C-84 is fixed (remove dead auto-detection from _build_steps since execute_roadmap resolves it), `effective_input_type` becomes just an alias for `config.input_type`. The variable adds confusion.
**Fix:** When fixing C-84, also rename or remove `effective_input_type` — just use `config.input_type` directly.

### C-117: EXTRACT_GATE does not validate TDD-specific frontmatter fields
**Severity:** IMPORTANT | **Tag:** [TDD/PRD] | **Source:** Agent13
**File:** `src/superclaude/cli/roadmap/gates.py` L765
**Bug:** `build_extract_prompt_tdd()` instructs the LLM to produce 6 additional fields (data_models_identified, api_surfaces_identified, etc.) but EXTRACT_GATE only requires the standard 13. TDD extractions that omit these fields pass silently. Downstream scoring uses `api_surface` and `data_model_complexity` which may be missing.
**Fix:** Create a conditional TDD_EXTRACT_GATE with the 6 additional required fields, selected in `_build_steps` based on input_type.

### C-119: PRD block and _INTEGRATION_ENUMERATION_BLOCK ordering inconsistent between builders
**Severity:** MINOR | **Tag:** [TDD/PRD] | **Source:** Agent13
**File:** `src/superclaude/cli/roadmap/prompts.py`
**Bug:** In `build_generate_prompt`, the PRD block is inserted before `_INTEGRATION_ENUMERATION_BLOCK`. In `build_spec_fidelity_prompt`, the PRD block is inserted after the integration dimensions. Inconsistent ordering could affect LLM output quality.
**Fix:** Standardize: PRD block always BEFORE output format blocks.

### Pre-Existing (2)

### C-120: TDD SKILL.md QA checklist item 13 references wrong synthesis file
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent13
**File:** `.claude/skills/tdd/SKILL.md`
**Bug:** QA checklist item 13 references `synth-04` for FR traceability but FRs live in `synth-02`.
**Fix:** Correct reference.

### C-121: obligation_scanner lowercases component names at extraction
**Severity:** MINOR | **Tag:** [PRE-EXISTING] | **Source:** Agent13
**File:** `src/superclaude/cli/roadmap/obligation_scanner.py` L222
**Bug:** Component names lowercased during extraction. Reports show `authservice` instead of `AuthService`, reducing diagnostic clarity.
**Fix:** Preserve original casing; lowercase only for matching.

### Meta (1)

### C-112: Consolidated report summary counts inconsistent
**Severity:** MINOR | **Tag:** [META] | **Source:** Agent14
**Fix:** Reconcile summary tables (multiple running totals from different rounds don't add up cleanly).

---

## GRAND TOTAL (7 rounds, 14 agents)

| Round | Agents | Raw | Dupes | New | Running |
|-------|--------|-----|-------|-----|---------|
| 1 | 1, 2 | 38 | 17 | 26 | 26 |
| 2 | 3, 4 | 20 | 5 | 15 | 41 |
| 3 | 5, 6 | 41 | 10 | 31 | 72 |
| 4 | 7, 8 | 27 | 7 | 20 | 92 |
| 5 | 9, 10 | 12 | 1 | 11 | 103 |
| dedup | — | — | 2 | -2 | 101 |
| 6 | 11, 12 | 20 | 5 | 15 | 116 |
| 7 | 13, 14 | 8 | 1 | 7 | 123 |
| **Total** | **14** | **166** | **48** | **123** | **123** |

**Round 7: 4 TDD/PRD + 2 pre-existing + 1 meta = 7 new**
**Raw findings dropped to 8 — lowest of any round. Approaching zero.**

Agent 14 explicitly stated: "Diminishing returns are clear — further passes are unlikely to yield significant findings."
