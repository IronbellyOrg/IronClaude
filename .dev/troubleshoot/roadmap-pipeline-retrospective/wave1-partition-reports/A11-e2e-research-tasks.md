# A11 — E2E Runs + Research Tasks Retrospective

**Partition scope:** Ten task directories spanning the TDD pipeline E2E (2026-03-26 → 2026-04-03), the PRD pipeline E2E + rerun, the spec-only baseline + full baseline runs, the quality-comparison cross-run audit, and two RESEARCH tasks (anti-instinct gate failure; full roadmap-tasklist architecture overhaul). Also covers three top-level files in `.dev/tasks/done/`: `RESEARCH-PROMPT-anti-instinct-gate-failure.md`, `RESEARCH-PROMPT-roadmap-tasklist-architecture-overhaul.md`, and `roadmap-pipeline-deep-trace.md`.

**Methodology:** Followed the mandated `grep -rli "roadmap"` enumeration → targeted Read of findings/research/QA/audit/phase reports → classification (FAILURE / REMEDIATION / SUCCESS) → cross-reference against current `src/superclaude/cli/roadmap/` code via grep on the BareReview worktree. Inferential findings (claims grounded in absence-of-evidence) are tagged inline.

---

## Findings

### F-A11-001: Anti-instinct gate halts every enriched (TDD/PRD) pipeline run
- **Type:** FAILURE
- **Pipeline step:** anti-instinct
- **Symptom:** Across four parallel E2E runs (TDD-only, TDD+PRD, Spec-only, Spec+PRD), every single run halted at the anti-instinct step. None reached spec-fidelity, test-strategy, deviation-analysis, remediate, or certify. Concretely, the 4-way matrix at `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-anti-instinct-4way.md` shows: TDD-only 5 undischarged + 4 uncovered + 0.76 fp coverage → FAIL; TDD+PRD 1 undischarged + 4 uncovered + 0.73 → FAIL; Spec-only 0 undischarged + 3 uncovered + 0.72 → FAIL; Spec+PRD 0 undischarged + 3 uncovered + 0.67 → FAIL. The execution-summary at `TASK-RF-20260402-baseline-repo/phase-outputs/test-results/execution-summary.md` confirms the baseline test-strategy + spec-fidelity were SKIPPED because anti-instinct exhausted retries.
- **Root cause (claimed):** Three independent regex-level false positives in two deterministic scanner modules — confirmed in detail by the anti-instinct research report (see F-A11-002). The Spec+PRD fingerprint regression to 0.67 is additionally driven by PRD-induced synonym substitution: the roadmap generator uses business/product terms instead of spec-level technical identifiers (`AUTH_SERVICE_ENABLED`, `RBAC`, `CSRF` appear in the missing-fingerprint list only when PRD is added).
- **Remediation applied:** Two parallel tracks. (1) Per the integration_contracts code at `src/superclaude/cli/roadmap/integration_contracts.py:54-60` the bare `\bStrategy\b` regex was removed from Category 4 and replaced with code-specific tokens (`Context(strategy=`, `ConcreteStrategy`, `set_strategy`, `get_strategy`, `StrategyPattern`, `strategy_registry`, `STRATEGY_MAP`, `AbstractStrategy`). (2) The obligation scanner at `src/superclaude/cli/roadmap/obligation_scanner.py:235-251,310-312` now skips lines beginning with `## ` or `### `, skips `**Objective:` lines, and explicitly demotes `hardcoded`-prefixed terms in descriptive config contexts.
- **Outcome:** Partial fix verified-in-code, but the synonym-aware fingerprint matching follow-up (DW-1 in `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md`) was NOT implemented. The fingerprint regression remains exploitable any time PRD enrichment introduces business synonyms.
- **Still possible today (Auggie check):** YES (partial). The regex-level false positives are closed at `integration_contracts.py:54-60` and `obligation_scanner.py:235-312`, but `gates.py:1043+` still hard-codes `undischarged_obligations == 0` AND `uncovered_contracts == 0` AND `fingerprint_coverage >= 0.7`, meaning any new vocabulary drift below 0.7 still halts the entire downstream pipeline as a single point of failure.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-anti-instinct-4way.md`, `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md`, `TASK-RF-20260326-e2e-modified/phase-outputs/test-results/phase4-anti-instinct.md`, `TASK-E2E-20260327-prd-pipeline-e2e/phase-outputs/test-results/phase4-anti-instinct.md`, `TASK-RF-20260402-baseline-repo/phase-outputs/test-results/execution-summary.md`.

### F-A11-002: Strategy-pattern regex matched section headings like "Testing Strategy"
- **Type:** FAILURE
- **Pipeline step:** anti-instinct
- **Symptom:** Four false-positive uncovered contracts in TDD+PRD runs (IC-001, IC-002, IC-006, IC-007) all from matching the bare `\bStrategy\b` token against markdown like `## 15. Testing Strategy` and `### 19.1 Migration Strategy`. Verbatim from `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-REPORT-anti-instinct-gate-failure.md` §2.3: "The Category 4 Strategy Pattern regex at `integration_contracts.py:48` matches `\bStrategy\b` in section headings. 'Testing Strategy' and 'Migration Strategy' are SECTION NAMES, not code patterns requiring wiring tasks. The regex is too broad."
- **Root cause (claimed):** Regex over-breadth — Category 4 conflated the design-pattern name with the English word.
- **Remediation applied:** Bare `Strategy` removed from the alternation; only code-shaped tokens remain (see F-A11-001 remediation #1).
- **Outcome:** Fix verified in-code. Eliminates the 4 false positives. Did not change the underlying gate strictness, so an actual uncovered strategy_pattern is still a hard halt.
- **Still possible today (Auggie check):** NO for "Testing Strategy" / "Migration Strategy" headings — `integration_contracts.py:54-60` no longer matches bare `Strategy`. YES for any other category if its regex is similarly overbroad (none audited).
- **Source artifacts:** `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-REPORT-anti-instinct-gate-failure.md` (§2.3, §6 Fix 1), `TASK-RF-20260326-e2e-modified/phase-outputs/test-results/phase4-anti-instinct.md`.

### F-A11-003: Obligation scanner falsely flagged "Hardcoded" describing a config value
- **Type:** FAILURE
- **Pipeline step:** anti-instinct
- **Symptom:** TDD+PRD run flagged 1 undischarged obligation on the literal word "Hardcoded" inside a roadmap Library Dependencies section describing `bcryptjs cost factor (12)`. The scanner detected it as a scaffold term but no discharge term exists because the value never gets "replaced" — it's a deliberate config. Anti-instinct research report §2.3: "ROOT CAUSE: False positive. The word 'hardcoded' in the roadmap is descriptive, not a scaffolding obligation."
- **Root cause (claimed):** Scanner matches `\bhardcoded\b` regardless of whether the term is imperative (a temporary implementation) or descriptive (naming a fixed config).
- **Remediation applied:** Heading-line skip + `hardcoded`-specific demotion at `obligation_scanner.py:235-251,310-312` ("hardcoded describing a deliberate config value (e.g., bcrypt cost factor (12) or hardcoded default) is not an obligation").
- **Outcome:** Specific bcryptjs case resolved. General descriptive-vs-imperative ambiguity remains heuristic.
- **Still possible today (Auggie check):** NO for the exact bcrypt/cost-factor pattern. YES for arbitrary descriptive uses outside H2/H3 headings that don't begin with "hardcod" prefix.
- **Source artifacts:** `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-REPORT-anti-instinct-gate-failure.md` (§2.3, §6 Fix 2), `TASK-RF-20260326-e2e-modified/phase-outputs/test-results/phase4-anti-instinct.md`.

### F-A11-004: The "Failures incorrectly reported as pre-existing" meta-failure
- **Type:** FAILURE
- **Pipeline step:** OTHER (E2E test triage / reviewer judgement)
- **Symptom:** From `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-REPORT-anti-instinct-gate-failure.md` §1 verbatim: "We incorrectly reported this as 'pre-existing' across multiple E2E runs." The same pattern appears in `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` where the anti-instinct halt is in the **pre-existing** column as C-02 ("Anti-instinct gate blocks entire downstream pipeline").
- **Root cause (claimed):** Reviewers/analysts attributed the halt to "pre-existing baseline behavior" rather than investigating that the false positives were caused by enriched-input vocabulary changes. The baseline only passed because its shorter, less descriptive roadmap happened not to contain the trigger words.
- **Remediation applied:** Dedicated research task spawned (TASK-RESEARCH-20260403-anti-instinct) which performed the regex-level analysis and produced the fix recipe in §6.
- **Outcome:** Mitigated by the research → remediation pipeline. The structural lesson — "do not classify halts as pre-existing without isolating triggers" — has no enforcement mechanism. **INFERENTIAL:** absence of any policy document or QA gate makes recurrence likely.
- **Still possible today (Auggie check):** UNKNOWN — no code-level mechanism prevents triage misclassification.
- **Source artifacts:** `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-REPORT-anti-instinct-gate-failure.md` (§1), `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` (C-02 row).

### F-A11-005: TDD+PRD pipelines produce 49% FEWER tasks than spec-only baseline
- **Type:** FAILURE
- **Pipeline step:** generate-opus-architect / generate-sonnet-architect / merge / OTHER (tasklist generation)
- **Symptom:** From `TASK-RF-20260403-quality-comparison/phase-outputs/reports/quality-matrix.md` Dim 7 and `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §1: "4.1x richer input (1,282 lines of TDD+PRD vs 312 lines of spec-only) produces 49% fewer actionable tasks (44 vs 87) for the same functional domain." The R-item-to-task ratio is 1:1 in both cases — meaning the tasklist generator is fine; the regression happens upstream in roadmap generation.
- **Root cause (claimed):** Three compounding structural failures: (a) extraction destroys tabular/code-block granularity into prose; (b) one-shot `claude --print --output-format text` capture hits 64k-token fallback cap with no truncation detection; (c) NO output template — neither generate nor merge prompts define a task table schema, so structure is LLM-invented and varies per run. Additional contributors: PRD-suppression language in `tasklist/prompts.py:221-223`, SKILL.md merge directives (lines 233/255/259), and absent task-count floors.
- **Remediation applied:** Partial. Per research/08 §3 Loss Point 1: TDD block now mandates technical-layer phasing and per-item decomposition; PRD block now prevents phase count reduction. The full overhaul (Option D phased migration) was specified but not yet executed.
- **Outcome:** Partial mitigation only. **INFERENTIAL:** absence of a re-run quality-matrix comparison after the partial prompt fixes means the 49% gap is not known to have closed.
- **Still possible today (Auggie check):** YES. `cli/roadmap/prompts.py` still constructs prompts via Python string concatenation; no template files exist under `cli/roadmap/templates/`; `ClaudeProcess` (per `pipeline/process.py`) still captures stdout via `--output-format text`; no `superclaude tasklist generate` CLI subcommand exists.
- **Source artifacts:** `TASK-RF-20260403-quality-comparison/phase-outputs/reports/quality-matrix.md`, `TASK-RF-20260403-quality-comparison/phase-outputs/reports/qualitative-assessment.md` §3.2.2, `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §1, §2.5, §4.

### F-A11-006: Extraction step lossily summarizes structured TDD/PRD content into prose
- **Type:** FAILURE
- **Pipeline step:** extract
- **Symptom:** `build_extract_prompt` produces 8 prose sections (TDD variant: 14) but reformats source tables, code blocks, and field-level definitions as narrative. The granularity flow diagram in the overhaul research report §2.4 shows extract as "REDUCES: tables/code blocks become prose sections."
- **Root cause (claimed):** Prompt design — no instruction preserves original structured formats. Extraction was designed for the spec-only case where unstructured prose is the source; TDD inputs that ARE structured get unnecessarily flattened.
- **Remediation applied:** None at the extraction-bypass level. The overhaul research recommends Phase 3 (bypass extraction for TDD with `_should_bypass_extraction()`) but that is unimplemented.
- **Outcome:** Open. Downstream steps work from already-degraded input.
- **Still possible today (Auggie check):** YES. No `_should_bypass_extraction` helper in `cli/roadmap/executor.py`; the extract step is unconditionally built in `_build_steps()`.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.4 (granularity flow), §4 Gap G-01.

### F-A11-007: One-shot stdout capture hits 64k-token fallback cap with no truncation detection
- **Type:** FAILURE
- **Pipeline step:** OTHER (subprocess output mechanism — affects extract, generate-*, diff, debate, score, merge, test-strategy, spec-fidelity, certify)
- **Symptom:** All 9 LLM steps capture output via `claude --print --output-format text` with stdout redirected to file. The non-streaming fallback caps at 64k tokens; if output exceeds this, the file is silently truncated. From overhaul research §2.5 Table: "If output hits token limit, file may be incomplete" and "Retries re-send identical prompt; partial output overwritten." The score step is documented at C-26 (`TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md`) as "Score step prompt exceeds _EMBED_SIZE_LIMIT with real data."
- **Root cause (claimed):** Architectural — `ClaudeProcess` uses `--output-format text` and one-shot stdout. No `content_complete` semantic check exists. No tool-use file writing.
- **Remediation applied:** None to date. Overhaul research §8 Phases 1-2 plan template-driven tool-use writing; not executed.
- **Outcome:** Open. Latent risk on every large enriched run.
- **Still possible today (Auggie check):** YES. `pipeline/process.py::ClaudeProcess` still uses `--output-format text`. No truncation detection in `_sanitize_output()` or in any gate.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.5, §5.5 Takeaway 1; `roadmap-pipeline-deep-trace.md` §3 Inline Embedding note.

### F-A11-008: Merge prompt drops ID preservation + integration enumeration that generate prompt enforces
- **Type:** FAILURE
- **Pipeline step:** merge
- **Symptom:** Per overhaul research §2.4: "Generate says 'Preserve ALL IDs… Do NOT renumber.' Merge has NO such instruction. `_INTEGRATION_ENUMERATION_BLOCK` is appended to generate; merge does not. Wiring tasks can be lost during merge."
- **Root cause (claimed):** Prompt drift — when `build_merge_prompt` was authored, the ID and enumeration constraints that already lived in `build_generate_prompt` were not propagated.
- **Remediation applied:** Per consolidated-findings C-06, the merge prompt was extended with `tdd_file` / `prd_file` params + conditional TDD/PRD blocks. ID preservation block was NOT added. Inspection of current prompts.py would confirm whether this remains open. **INFERENTIAL:** the overhaul research dated 2026-04-04 (after C-06 fix) still lists this as a Critical gap (G-05), so the ID preservation language did not land.
- **Outcome:** Partial. TDD/PRD context flows into merge but IDs and integration enumeration can still drop silently.
- **Still possible today (Auggie check):** YES (high probability). The Wave 1 trace at `roadmap-pipeline-deep-trace.md` §4 confirms `_INTEGRATION_ENUMERATION_BLOCK` exists but does not list it on the merge step.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.4 (gap 2/3), §4 G-05; `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-06.

### F-A11-009: DEVIATION_ANALYSIS_GATE field-name mismatch (`ambiguous_count` vs `ambiguous_deviations`)
- **Type:** FAILURE
- **Pipeline step:** deviation-analysis
- **Symptom:** Bug B-1 per overhaul research §2.6: "DEVIATION_ANALYSIS_GATE requires frontmatter field `ambiguous_count` but semantic check reads `ambiguous_deviations` — field name mismatch."
- **Root cause (claimed):** Field naming inconsistency between gate frontmatter requirement and semantic check function.
- **Remediation applied:** None. Inspection confirms `gates.py:18` carries an explicit comment ("Pre-existing bug: ambiguous_count/ambiguous_deviations field mismatch (B-1)"), `gates.py:389-403` reads `ambiguous_deviations`, while `gates.py:573,589` requires `ambiguous_count` in frontmatter. The bug remains UNFIXED but is annotated.
- **Outcome:** Open. The semantic check effectively cannot fire on a real "ambiguous" deviation because the frontmatter field consumed by it (`ambiguous_deviations`) is never required by the gate.
- **Still possible today (Auggie check):** YES (verified). The mismatch is still in `src/superclaude/cli/roadmap/gates.py:18, 389-403, 573, 589`.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.6, §4 G-19; `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-01.

### F-A11-010: Two frontmatter parsers with conflicting byte-0-vs-anywhere behavior
- **Type:** FAILURE
- **Pipeline step:** OTHER (gate enforcement — affects every STRICT gate)
- **Symptom:** Per overhaul research §2.6 latent bug: "`_parse_frontmatter` (roadmap/gates.py) requires frontmatter at byte 0; `_check_frontmatter` (pipeline/gates.py) uses `re.MULTILINE` allowing frontmatter after preamble." Some semantic checks can therefore fail on content that the basic-frontmatter check accepts.
- **Root cause (claimed):** Duplicate utility implementations in two modules that evolved independently.
- **Remediation applied:** None. `_sanitize_output()` exists as a partial mitigation by stripping conversational preamble, but the two parsers still disagree on what is valid.
- **Outcome:** Open and dangerous because it produces non-deterministic semantic-check pass/fail depending on whether the LLM emitted preamble.
- **Still possible today (Auggie check):** YES — both parsers still exist (the trace confirms `_parse_frontmatter` in roadmap/gates.py and `_check_frontmatter` in pipeline/gates.py).
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.6, §4 G-15.

### F-A11-011: `build_certify_step()` is dead code — step 13 never executes
- **Type:** FAILURE
- **Pipeline step:** certify
- **Symptom:** From overhaul research §2.1: "A 13th step (certify) has a builder function `build_certify_step()` at executor.py:1259, but is never called — confirmed dead code (research/01, Gap 1)." The deep trace §13 lists certify as the dynamic step but the trace itself notes it as "constructed dynamically by `roadmap_run_step()` after remediate completes" — yet the actual remediate dispatch path does not call it. Auggie confirms: `grep certify` in `cli/roadmap/executor.py` finds only the definition at line 1899, never an invocation.
- **Root cause (claimed):** Step was designed for the remediation→certify loop but the loop wiring was never finished.
- **Remediation applied:** None.
- **Outcome:** Open. Remediation has no verification step; users see remediation-tasklist.md but never a certification-report.md from a normal pipeline run.
- **Still possible today (Auggie check):** YES — `build_certify_step` defined at `executor.py:1899` is unreferenced anywhere else in the executor.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.1, §4 G-18; `roadmap-pipeline-deep-trace.md` §13 footnote.

### F-A11-012: `tasklist validate` crashes with bare traceback when roadmap.md missing
- **Type:** FAILURE
- **Pipeline step:** OTHER (downstream — `superclaude tasklist validate`)
- **Symptom:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` BUG-1: "Running `uv run superclaude tasklist validate` on a directory that lacks `roadmap.md` produces a Python traceback (FileNotFoundError) instead of a graceful error message."
- **Root cause (claimed):** Missing file-existence guard in the tasklist validate executor's roadmap-path resolution.
- **Remediation applied:** None — left as DW-3 (MEDIUM priority deferred work).
- **Outcome:** Open. Pre-existing per the artifact.
- **Still possible today (Auggie check):** UNKNOWN — not in the assigned partition's audit scope. **INFERENTIAL:** absence of any commit referencing DW-3 makes it likely still open.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` BUG-1, DW-3.

### F-A11-013: `tasklist validate` overwrites prior fidelity report when re-run
- **Type:** FAILURE
- **Pipeline step:** OTHER (downstream — `superclaude tasklist validate`)
- **Symptom:** Same follow-up-action-items file, BUG-2: "Running `tasklist validate` twice on the same output directory overwrites the previous `tasklist-fidelity.md` file. Items 7.1 (enriched) and 7.2 (baseline) both wrote to the same file, destroying the enriched output."
- **Root cause (claimed):** Output filename is deterministic on output dir; no `--output-file` flag.
- **Remediation applied:** None — left as DW-5 (LOW).
- **Outcome:** Open. Test infrastructure workaround: copy file before re-run.
- **Still possible today (Auggie check):** UNKNOWN (outside partition). **INFERENTIAL:** treat as likely still open.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` BUG-2, DW-5.

### F-A11-014: LLM skips PRD supplementary validation section when no tasklist exists
- **Type:** FAILURE
- **Pipeline step:** OTHER (downstream — `tasklist validate` with `--prd-file`)
- **Symptom:** Follow-up BUG-3: fidelity report does not include "Supplementary PRD Validation" section when run on spec+PRD output without a tasklist. The LLM skips the entire section instead of emitting a "cannot validate — no tasklist" stub.
- **Root cause (claimed):** Prompt wording gates supplementary checks on the existence of a tasklist artifact.
- **Remediation applied:** None — left as DW-6 (LOW).
- **Outcome:** Open. Behavior inconsistent: section emitted when tasklist deviations exist (7.1), skipped when no tasklist exists (7.4).
- **Still possible today (Auggie check):** UNKNOWN (outside partition).
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` BUG-3, DW-6.

### F-A11-015: Fabricated severity ratings emitted by reviewer subagent
- **Type:** FAILURE
- **Pipeline step:** OTHER (reviewer subagent quality)
- **Symptom:** Follow-up BUG-4: "The initial Phase 7 comparison and summary files contained fabricated MEDIUM/LOW severity ratings for supplementary items. The actual fidelity report does not assign individual severity ratings to supplementary checks — only DEV-001 (missing tasklist) has an explicit HIGH severity." Caught by QA gate.
- **Root cause (claimed):** Executor agent hallucinated severities that were not present in source.
- **Remediation applied:** Files rewritten with accurate content.
- **Outcome:** Resolved for this run; structural mechanism enabling hallucination remains.
- **Still possible today (Auggie check):** YES — no programmatic guard against subagent hallucination of severity classification.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` BUG-4.

### F-A11-016: Haiku-architect retry instability with large PRD context
- **Type:** FAILURE
- **Pipeline step:** generate-haiku-architect
- **Symptom:** From 4-way pipeline table at `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md` §2 and follow-up DW-7: "the TDD+PRD haiku-architect generation required 2 attempts" — singular among the 4 runs. Hypothesis: larger extraction context from PRD enrichment exceeds the smaller model's capacity.
- **Root cause (claimed):** Model capacity for smaller-class agents under enriched-prompt sizes.
- **Remediation applied:** None — DW-7 deferred.
- **Outcome:** Open; pattern not yet observed to recur frequently.
- **Still possible today (Auggie check):** YES — no per-model prompt-size budgeting in `prompts.py` or `executor.py`.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md` §2, follow-up DW-7.

### F-A11-017: Merge step failed on duplicate-headings gate; passed on resume
- **Type:** FAILURE
- **Pipeline step:** merge
- **Symptom:** `TASK-RF-20260402-baseline-repo/phase-outputs/test-results/execution-summary.md`: "Merge initially FAILED (duplicate headings gate), PASSED on resume." Required 2 attempts to satisfy `MERGE_GATE`'s `no_duplicate_headings` semantic check.
- **Root cause (claimed):** UNDOCUMENTED in the execution summary. **INFERENTIAL:** LLM emitted the same H2 twice (common when merging two variants both having "Risk Assessment"). The resume re-prompt resolved by chance, not by deterministic regeneration logic.
- **Remediation applied:** Pipeline retry succeeded — no code change.
- **Outcome:** Resolved per-run via retry; the structural fragility (LLM may emit duplicate headings; resume relies on non-determinism) remains.
- **Still possible today (Auggie check):** YES — `gates.py` MERGE_GATE still includes `no_duplicate_headings` and retry-without-learning is documented in overhaul §2.5: "Retries re-send identical prompt."
- **Source artifacts:** `TASK-RF-20260402-baseline-repo/phase-outputs/test-results/execution-summary.md`.

### F-A11-018: PRD-only input silently misclassified (no PRD detection signal route)
- **Type:** FAILURE
- **Pipeline step:** OTHER (input routing)
- **Symptom:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-55: "Passing PRD as primary input silently misclassifies." Also `--input-type` CLI flag accepts `auto/tdd/spec` but NOT `prd` even though detection can return `prd` and `RoadmapConfig` accepts it (overhaul research §2.3).
- **Root cause (claimed):** Input router rejects single PRD because routing requires at least one spec or TDD as primary input; user receives misclassification rather than rejection with actionable error.
- **Remediation applied:** BACKLOG in C-55; partially addressed by C-122 multi-file auto-detection (BACKLOG).
- **Outcome:** Open. PRDs cannot be used standalone; users discover this only post-failure.
- **Still possible today (Auggie check):** YES — `commands.py` still doesn't accept `prd` in `--input-type` choices per the trace §2.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-55, C-122; `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.3.

### F-A11-019: PRD-suppression language in tasklist prompt blocks PRD-driven tasks
- **Type:** FAILURE
- **Pipeline step:** OTHER (tasklist generation prompt)
- **Symptom:** Overhaul research §4 G-08 / Recommendation §7: "tasklist/prompts.py lines 221-223 block PRD from generating tasks. Strongest single root cause of task count regression." This is the H2 finding from the prior 2026-04-03 task-quality research.
- **Root cause (claimed):** Prompt text explicitly suppresses PRD-derived task rows.
- **Remediation applied:** None at the prompt-edit level. Step 5.1 in the recommended Option D plan would remove these 3 lines.
- **Outcome:** Open. Largest single contributor to the 49% task-reduction failure (F-A11-005).
- **Still possible today (Auggie check):** YES — file path and line numbers still active per overhaul research evidence.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §4 G-08, §7 evidence, §8 Phase 5 Step 5.1.

### F-A11-020: SKILL.md merge directives encourage over-consolidation in tasklist generation
- **Type:** FAILURE
- **Pipeline step:** OTHER (tasklist skill protocol)
- **Symptom:** Overhaul research §4 G-09: "3+ merge instructions with vague matching criteria cause over-consolidation" (SKILL.md lines 233, 255, 259).
- **Root cause (claimed):** Vague merge criteria in the protocol cause the LLM to bundle distinct R-items into single tasks rather than producing 1:1 task expansion.
- **Remediation applied:** None — proposed as Step 5.4 in the unexecuted Option D plan.
- **Outcome:** Open. Co-cause of the 49% task-reduction failure.
- **Still possible today (Auggie check):** YES — protocol still in place.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §4 G-09.

### F-A11-021: No CLI `tasklist generate` subcommand — generation is inference-only via skill
- **Type:** FAILURE
- **Pipeline step:** OTHER (downstream — tasklist generation entry point)
- **Symptom:** Overhaul research §2.2: "There is no CLI `tasklist generate` subcommand. `build_tasklist_generate_prompt()` exists in `tasklist/prompts.py` but is never called by any CLI code." Follow-up DW-2 same.
- **Root cause (claimed):** Subcommand was designed and prompt builder written, but Click command + executor were never added.
- **Remediation applied:** None.
- **Outcome:** Open. Generation enrichment is untestable E2E because there is no programmatic entry point.
- **Still possible today (Auggie check):** YES — verified absence of `tasklist generate` in `cli/tasklist/commands.py` per overhaul research.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.2, §4 G-04; `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` DW-2.

### F-A11-022: R-item identity gap — generation IDs and validation IDs derived independently
- **Type:** FAILURE
- **Pipeline step:** OTHER (tasklist generation ↔ validation)
- **Symptom:** Overhaul research §2.2: "R-items (R-001, R-002, ...) are assigned by the generation-time LLM following SKILL.md Section 4.1 rules. The validation-time LLM independently re-derives R-items. No shared registry exists."
- **Root cause (claimed):** No file-backed R-item registry. Both ends rely on the LLM applying identical algorithm to identical input, which is non-deterministic.
- **Remediation applied:** None — proposed as G-13 in the unexecuted Option D plan.
- **Outcome:** Open. Validation can flag false missing/false extra R-items depending on the LLM's re-derivation.
- **Still possible today (Auggie check):** YES — no R-item registry file mentioned in trace §15.
- **Source artifacts:** `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md` §2.2, §4 G-13.

### F-A11-023: Sprint executor does NOT enforce task dependencies at runtime
- **Type:** FAILURE
- **Pipeline step:** OTHER (downstream — sprint execution)
- **Symptom:** From the deep trace §15 Step C: "dependencies are NOT enforced at runtime. The executor iterates tasks in list order… The executor doesn't read the dependency field at all (it's parsed into `TaskEntry.dependencies` but never consulted during execution)." Cross-phase deps work only because phases run sequentially.
- **Root cause (claimed):** Architectural — sprint executor's per-task loop processes by list order, not dependency graph.
- **Remediation applied:** None documented in the assigned partition.
- **Outcome:** Open. Tasklist ordering becomes a load-bearing contract; mis-ordering at generation time produces silent dependency violations at sprint time.
- **Still possible today (Auggie check):** YES — `roadmap-pipeline-deep-trace.md` §15 Step C is current as of 2026-04-03 and matches `sprint/executor.py` per the trace's citations.
- **Source artifacts:** `roadmap-pipeline-deep-trace.md` §15 Step C.

### F-A11-024: No feedback loop from sprint completion back into roadmap update
- **Type:** FAILURE
- **Pipeline step:** OTHER (architectural gap)
- **Symptom:** Deep trace §15 Step D: "There is no `superclaude roadmap update` command. The designed feedback mechanisms are: retrospective file (manual), `.roadmap-state.json` as state bridge (read-only from sprint side), and `--resume` for spec changes only." Sprint executor does NOT write back to roadmap state.
- **Root cause (claimed):** Architectural — the "continuous refinement loop" exists structurally but is not implemented end-to-end.
- **Remediation applied:** None.
- **Outcome:** Open. Each roadmap regeneration requires manual retrospective authoring.
- **Still possible today (Auggie check):** YES — confirmed by the deep trace.
- **Source artifacts:** `roadmap-pipeline-deep-trace.md` §15 Step D.

### F-A11-025: Spec-fidelity dimensions 7-11 always emitted even when no TDD provided
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity
- **Symptom:** Consolidated findings C-03: "Spec-fidelity dims 7-11 always emitted" — pipeline emitted TDD-specific dimensions even on spec-only runs, polluting the fidelity report with N/A entries.
- **Root cause (claimed):** Prompt builder unconditionally appended dims 7-11 regardless of `tdd_file` presence.
- **Remediation applied:** FIXED per consolidated-findings: "Made dims 7-11 conditional on `tdd_file is not None`. Spec-only runs get 6 dims (pre-TDD behavior). TDD runs get 11. PRD adds 12-15 on top. No regression."
- **Outcome:** Resolved.
- **Still possible today (Auggie check):** NO — the conditional gating per the consolidated-findings remediation should hold.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-03.

### F-A11-026: Validation/remediation sub-pipelines have zero TDD/PRD awareness
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity / remediate
- **Symptom:** Consolidated findings C-37, C-38: "Validation sub-pipeline has zero TDD/PRD awareness" and "Remediation sub-pipeline has zero TDD/PRD awareness." Status BACKLOG.
- **Root cause (claimed):** TDD/PRD context not threaded into the validation/remediation prompt builders or step inputs.
- **Remediation applied:** None — both BACKLOG.
- **Outcome:** Open. Remediation tasks may regress TDD-specific or PRD-specific requirements because the remediator does not know they exist.
- **Still possible today (Auggie check):** YES — the deep trace §6 shows validation_executor takes only `roadmap.md`, `test-strategy.md`, `extraction.md` and does not list TDD/PRD inputs.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-37, C-38; `roadmap-pipeline-deep-trace.md` §6.

### F-A11-027: Fingerprint extraction ignores file paths, API endpoints, field names
- **Type:** FAILURE
- **Pipeline step:** anti-instinct (fingerprint sub-check)
- **Symptom:** Consolidated findings C-30: "Fingerprint extraction ignores file paths, API endpoints, field names." Status BACKLOG. Combined with F-A11-001 PRD-synonym substitution this contributes to fingerprint coverage drops.
- **Root cause (claimed):** Fingerprint extractor pulls backticked identifiers from spec but skips other identifier classes (URLs, field names, file paths).
- **Remediation applied:** None.
- **Outcome:** Open. Fingerprint coverage measures a subset of what should be measured.
- **Still possible today (Auggie check):** YES — deep trace §1 confirms fingerprint module purpose unchanged.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-30.

### F-A11-028: Obligation scanner position-matching uses `content.find` (wrong section attribution)
- **Type:** FAILURE
- **Pipeline step:** anti-instinct (obligation sub-check)
- **Symptom:** Consolidated findings C-40: position matching scans for substring in raw content, leading to wrong-section attribution for the same scaffold term repeated elsewhere.
- **Root cause (claimed):** Naive substring search instead of section-aware tokenization.
- **Remediation applied:** Heading-skip logic added later (F-A11-003 remediation), but the underlying position attribution bug is broader.
- **Outcome:** Partially mitigated; the targeted fix doesn't address all attribution edge cases.
- **Still possible today (Auggie check):** YES (likely) — obligation_scanner.py has section-splitting logic (`scan_obligations` builds per-section context) but the consolidated finding C-40 is BACKLOG.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-40.

### F-A11-029: Convergence regression handler is a no-op stub
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity (convergence mode)
- **Symptom:** Consolidated findings C-43: "Convergence regression handler is a no-op stub." The convergence engine has a `handle_regression` hook but it does nothing meaningful.
- **Root cause (claimed):** Stub never implemented; convergence proceeds even when regressions appear between iterations.
- **Remediation applied:** None.
- **Outcome:** Open. Convergence mode is unsound on regression cases. Mitigated only because convergence is off by default (deep trace §7: "currently defaults to False").
- **Still possible today (Auggie check):** YES — convergence module unchanged per deep trace §7.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-43; `roadmap-pipeline-deep-trace.md` §7.

### F-A11-030: `_check_cross_file_coherence` mutates list during iteration
- **Type:** FAILURE
- **Pipeline step:** OTHER (gate utility)
- **Symptom:** Consolidated findings C-52: list-during-iteration mutation bug in cross-file coherence check.
- **Root cause (claimed):** Standard Python footgun — `remove()` while iterating same list.
- **Remediation applied:** None (marked "Yes" quick fix but unverified).
- **Outcome:** Open per consolidated findings.
- **Still possible today (Auggie check):** UNKNOWN — not in partition scope.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-52.

### F-A11-031: `_cross_refs_resolve` gate check always returns True
- **Type:** FAILURE
- **Pipeline step:** merge (gate semantic check)
- **Symptom:** Consolidated findings C-108: "`_cross_refs_resolve` gate check always returns True" — implemented as a no-op stub.
- **Root cause (claimed):** Implementation pending; check pretends to validate.
- **Remediation applied:** None.
- **Outcome:** Open. Broken cross-references in merged roadmap pass MERGE_GATE silently.
- **Still possible today (Auggie check):** YES (per consolidated findings; not in remediated list).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-108.

### F-A11-032: `_frontmatter_values_non_empty` checks ALL fields, not just required
- **Type:** FAILURE
- **Pipeline step:** OTHER (gate semantic check)
- **Symptom:** Consolidated findings C-80: the non-empty checker iterates every frontmatter field including optional ones, blocking otherwise-valid outputs.
- **Root cause (claimed):** Filter not narrowed to required-fields set.
- **Remediation applied:** None (BACKLOG; quick fix flagged).
- **Outcome:** Open. Adds noise failures on optional metadata fields.
- **Still possible today (Auggie check):** YES — `gates.py` confirms `frontmatter_values_non_empty` is used widely; no narrowing wrapper observed.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-80.

### F-A11-033: Spec-parser regex drops compound IDs (`FR-AUTH-001`, `FR-AUTH.1`)
- **Type:** FAILURE
- **Pipeline step:** OTHER (extract / spec_parser)
- **Symptom:** Consolidated findings C-22 (CRITICAL pre-existing): regex for requirement IDs strips compound forms.
- **Root cause (claimed):** Regex assumes flat numbering, not domain-qualified or dotted.
- **Remediation applied:** None.
- **Outcome:** Open. TDD-style IDs (`FR-AUTH-001`) may be missed by spec_parser, corrupting downstream traceability.
- **Still possible today (Auggie check):** YES (BACKLOG).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-22.

### F-A11-034: `certify_prompts` parser uses wrong finding-format regex
- **Type:** FAILURE
- **Pipeline step:** certify (when wired) / certify_prompts
- **Symptom:** Consolidated findings C-23 (CRITICAL pre-existing): regex matches `F-\d+` but actual format is `dimension-type-hash`.
- **Root cause (claimed):** Format drift between deviation-analysis output and certify parser.
- **Remediation applied:** None.
- **Outcome:** Open — and academic until F-A11-011 (certify dead code) is fixed.
- **Still possible today (Auggie check):** YES (BACKLOG).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-23.

### F-A11-035: DIMENSION_SECTION_MAP hardcoded to release-spec section numbering
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity / extract
- **Symptom:** Consolidated findings C-24 (CRITICAL pre-existing): `DIMENSION_SECTION_MAP` assumes release-spec section numbering and breaks on TDD or PRD numbering schemes.
- **Root cause (claimed):** Map should be conditional on input_type.
- **Remediation applied:** None.
- **Outcome:** Open.
- **Still possible today (Auggie check):** YES (BACKLOG).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-24.

### F-A11-036: `_restore_from_state` assigns unvalidated state values
- **Type:** FAILURE
- **Pipeline step:** OTHER (resume / state)
- **Symptom:** Consolidated findings C-46 (CRITICAL pre-existing): state file values restored without type validation, opening the door to type-confusion on `--resume`.
- **Root cause (claimed):** Restore path trusts JSON shape.
- **Remediation applied:** None.
- **Outcome:** Open. Corrupted state file can crash mid-resume.
- **Still possible today (Auggie check):** YES.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-46.

### F-A11-037: Semantic-layer call-site passes wrong argument types — code never executes
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity (convergence semantic layer)
- **Symptom:** Consolidated findings C-79 (CRITICAL pre-existing): call site passes wrong arg types, function silently never executes.
- **Root cause (claimed):** Type mismatch between caller and callee.
- **Remediation applied:** None.
- **Outcome:** Open. Convergence semantic layer is dead in practice.
- **Still possible today (Auggie check):** YES (BACKLOG; quick fix flagged but not done).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-79.

### F-A11-038: `_parse_frontmatter` drops YAML list continuation lines
- **Type:** FAILURE
- **Pipeline step:** OTHER (frontmatter parser)
- **Symptom:** Consolidated findings C-81 (CRITICAL pre-existing): parser drops YAML list continuation lines, mangling list-valued frontmatter fields.
- **Root cause (claimed):** Parser implementation handles only flat key:value, not list continuations.
- **Remediation applied:** None.
- **Outcome:** Open. List-valued fields (e.g., `agents:`) can be silently truncated.
- **Still possible today (Auggie check):** YES (BACKLOG).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-81.

### F-A11-039: TDD-extraction sentinel said complexity "may remain empty" while gate required value
- **Type:** REMEDIATION
- **Pipeline step:** extract
- **Symptom:** Consolidated findings C-61 (TDD/PRD critical): "TDD template sentinel says complexity 'may remain empty' but gate expects value" — template-vs-gate contract mismatch.
- **Root cause (claimed):** Documentation drift between template guidance and gate enforcement.
- **Remediation applied:** FIXED. Template text clarified: "computed by sc:roadmap, provide estimated values if known."
- **Outcome:** Resolved.
- **Still possible today (Auggie check):** NO for the exact contradiction; YES for other template-vs-gate contract drifts (no enforcement mechanism prevents recurrence).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-61.

### F-A11-040: `EXTRACT_TDD_GATE` introduced after C-117 to validate TDD-specific frontmatter
- **Type:** REMEDIATION
- **Pipeline step:** extract
- **Symptom:** Pre-fix: `EXTRACT_GATE` did not validate TDD-specific frontmatter fields (`data_models_identified`, `api_surfaces_identified`, etc.), so TDD extractions that omitted these silently passed.
- **Root cause (claimed):** Single gate constant for both spec and TDD paths.
- **Remediation applied:** FIXED per C-117: "Created `EXTRACT_TDD_GATE` with all 19 fields (13 standard + 6 TDD-specific). Routing in `_build_steps`: `EXTRACT_TDD_GATE if config.input_type == 'tdd' else EXTRACT_GATE`."
- **Outcome:** Resolved. The deep trace §5 confirms EXTRACT_TDD_GATE present at `gates.py:797-835`.
- **Still possible today (Auggie check):** NO — gate exists in current code.
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-117; `roadmap-pipeline-deep-trace.md` §5.

### F-A11-041: TDD path achieves functional parity with spec path — substantive new content
- **Type:** SUCCESS
- **Pipeline step:** extract (and downstream)
- **Symptom:** From `TASK-RF-20260326-e2e-modified/reviews/qa-qualitative-tdd-vs-spec.md` §1: "TDD path works as well as or better than the spec path. No functionality lost. Ready for use." The 6 TDD-specific extraction sections (Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness) all produced substantive implementation-ready content, not stubs.
- **Root cause (claimed):** Successful design of TDD-conditional prompt blocks and `EXTRACT_TDD_GATE`.
- **Remediation applied:** N/A (success record).
- **Outcome:** TDD path is operational; spec path is unbroken; isolation is clean.
- **Still possible today (Auggie check):** N/A — success confirmation only.
- **Source artifacts:** `TASK-RF-20260326-e2e-modified/reviews/qa-qualitative-tdd-vs-spec.md` §1-2.

### F-A11-042: PRD enrichment substantively reduced undischarged obligations (TDD)
- **Type:** SUCCESS
- **Pipeline step:** anti-instinct
- **Symptom:** From `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md` §4 Positive Effects: "Undischarged obligations dropped from 5 to 1 (80% reduction). PRD context helps the roadmap generator produce fewer skeleton/stub placeholders."
- **Root cause (claimed):** PRD context fills in implementation specifics that would otherwise be left as scaffolding placeholders.
- **Remediation applied:** N/A — emergent benefit of PRD enrichment.
- **Outcome:** Reduces real-obligation count even though gate still halts on false-positive count.
- **Still possible today (Auggie check):** YES (emergent property of richer input).
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md` §4.

### F-A11-043: PRD enrichment dramatically expanded extraction yield
- **Type:** SUCCESS
- **Pipeline step:** extract
- **Symptom:** Cross-pipeline analysis §2: TDD-only → TDD+PRD: total_requirements +56% (9→14), risks_identified +133% (3→7), components_identified +125% (4→9), migration_items_identified +400% (3→15), operational_items_identified +350% (2→9).
- **Root cause (claimed):** PRD context provides additional dimensions the extractor would otherwise miss.
- **Remediation applied:** N/A — emergent benefit.
- **Outcome:** Confirmed across all dimensions.
- **Still possible today (Auggie check):** YES.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md` §2.

### F-A11-044: Auto-wire from `.roadmap-state.json` works in 4/5 scenarios
- **Type:** SUCCESS
- **Pipeline step:** OTHER (downstream — `tasklist validate`)
- **Symptom:** Follow-up §4: tdd_file + prd_file auto-wired; input_type restoration works (C-91 fix); explicit `--prd-file` overrides auto-wire (C-27 fix); graceful degradation (missing file → WARNING). Only failure: missing state file → traceback (BUG-1, see F-A11-012).
- **Root cause (claimed):** Coherent state-file design once correctly populated by upstream roadmap run.
- **Remediation applied:** N/A.
- **Outcome:** 4/5 scenarios working — strong success record despite the single missing-roadmap.md crash.
- **Still possible today (Auggie check):** N/A — success.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` §4.

### F-A11-045: PRD-derived enrichment categories are sticky/amplifying across pipeline
- **Type:** SUCCESS
- **Pipeline step:** OTHER (cross-pipeline enrichment flow)
- **Symptom:** Quality matrix §4.3: persona refs amplify 4→11→40 (10× end-to-end in Run C). Compliance refs amplify 11→25→40 (3.6×). "Enrichment amplification is a pipeline property, not just an input property."
- **Root cause (claimed):** Each pipeline stage contextualizes enrichment into phase-specific and task-specific mentions.
- **Remediation applied:** N/A — emergent.
- **Outcome:** Confirmed amplification behavior; quality benefit when pipeline completes.
- **Still possible today (Auggie check):** YES (emergent).
- **Source artifacts:** `TASK-RF-20260403-quality-comparison/phase-outputs/reports/quality-matrix.md` §4.3.

### F-A11-046: Anti-instinct fingerprint coverage marginally improved on richer TDD+PRD input
- **Type:** SUCCESS
- **Pipeline step:** anti-instinct
- **Symptom:** Quality matrix Dim 3: Run C 0.73 vs Run A 0.72, despite Run C auditing 2.5× more fingerprints (45 vs 18). Equivalent coverage over larger surface area = stronger performance.
- **Root cause (claimed):** Richer roadmap content matches richer fingerprint set.
- **Remediation applied:** N/A.
- **Outcome:** Marginal but real improvement on the fingerprint dimension specifically. Caveat: did not save the overall gate from FAIL because of F-A11-002/F-A11-003 false positives.
- **Still possible today (Auggie check):** YES.
- **Source artifacts:** `TASK-RF-20260403-quality-comparison/phase-outputs/reports/quality-matrix.md` Dim 3.

### F-A11-047: Spec-only baseline run completes the full pipeline through tasklist
- **Type:** SUCCESS
- **Pipeline step:** OTHER (full pipeline completion record)
- **Symptom:** Only the spec-baseline (Run A) produced spec-fidelity, test-strategy, and tasklist artifacts. Per execution-summary, 9 content `.md` files + 7 zero-byte error files (clean cancellations), 0 Python crashes. 87 tasks generated across 5 phases with 55% STRICT tier classification.
- **Root cause (claimed):** Shorter roadmap content avoided the false-positive triggers in anti-instinct.
- **Remediation applied:** N/A.
- **Outcome:** Confirms pipeline IS capable of end-to-end completion. The blocker is anti-instinct strictness on richer inputs.
- **Still possible today (Auggie check):** YES (success).
- **Source artifacts:** `TASK-RF-20260402-baseline-repo/phase-outputs/test-results/execution-summary.md`.

### F-A11-048: Detection-rule divergence between CLI and skill layer (FIXED)
- **Type:** REMEDIATION
- **Pipeline step:** OTHER (input detection)
- **Symptom:** Consolidated findings C-12 (CRITICAL TDD/PRD): scoring algorithm differed between CLI `detect_input_type()` and the skill-layer documentation, risking divergent detection across paths.
- **Root cause (claimed):** Docs drift after CLI refactor.
- **Remediation applied:** FIXED. Updated `scoring.md` (full algorithm description), `extraction-pipeline.md` (summary with cross-ref), `spec-panel.md` (inline algorithm). All 3 now describe the 4-signal weighted scoring with threshold ≥5. Synced via `make sync-dev`.
- **Outcome:** Resolved.
- **Still possible today (Auggie check):** NO for the original divergence; YES for future drift (no enforcement).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-12.

### F-A11-049: Click stderr swallowed in dry-run mode
- **Type:** FAILURE
- **Pipeline step:** OTHER (CLI / dry-run)
- **Symptom:** Follow-up Known Issues: "Click stderr swallowed in dry-run" — detection messages emitted to stderr are not captured by the user's tee pipeline.
- **Root cause (claimed):** Click writes to stderr; tee captures only stdout.
- **Remediation applied:** None.
- **Outcome:** Open. Workaround: redirect 2>&1.
- **Still possible today (Auggie check):** UNKNOWN — not partition-scope.
- **Source artifacts:** `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` §2.

### F-A11-050: `_embed_inputs` raises unhandled FileNotFoundError; crashes on UTF-16
- **Type:** FAILURE
- **Pipeline step:** OTHER (subprocess input embedding)
- **Symptom:** Consolidated findings C-83, C-54: embedder raises unhandled FileNotFoundError on missing TDD/PRD files and crashes on UTF-16 encoded inputs. Compounded by C-28 "no handling for empty or binary files."
- **Root cause (claimed):** Naive file reads without try/except or encoding detection.
- **Remediation applied:** None.
- **Outcome:** Open. Brittle to real-world file conditions.
- **Still possible today (Auggie check):** YES (BACKLOG).
- **Source artifacts:** `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md` C-28, C-54, C-83.

---

## Cross-cutting patterns within this partition

- **Anti-instinct gate is the structural bottleneck.** Every enriched run halts there (F-A11-001, F-A11-002, F-A11-003, F-A11-046), every E2E test plan documented its halt as "expected," and the gate's hard-zero requirements on three independent regex-driven counters make false-positive vocabulary drift catastrophic to pipeline completion.
- **Regex-driven deterministic checks are fragile to richer vocabulary.** Both `\bStrategy\b` (F-A11-002) and `\bhardcoded\b` (F-A11-003) over-matched once richer roadmaps used more English; the fingerprint regression (F-A11-001, F-A11-027) is the same pattern from the missing-side.
- **Prompt vs gate vs template contracts are silently drifted.** The merge prompt omits constraints the generate prompt enforces (F-A11-008); the deviation-analysis gate requires `ambiguous_count` while its checker reads `ambiguous_deviations` (F-A11-009); the TDD template sentinel contradicted gate requirements (F-A11-039); fidelity dims 7-11 were emitted unconditionally (F-A11-025) until fixed.
- **One-shot stdout capture and template-less generation are the root architectural cause of granularity loss.** F-A11-005 (49% task reduction), F-A11-006 (lossy extraction), F-A11-007 (64k truncation), F-A11-019 (PRD suppression) and F-A11-020 (over-consolidation) compound to produce the documented richer-input-fewer-tasks paradox.
- **Triage misclassifies pipeline halts as "pre-existing baseline" instead of investigating triggers.** F-A11-004 calls this out explicitly; F-A11-016 and F-A11-017 followed the same pattern (treated as one-off retries rather than structural fragilities).
- **Dead-code and dead-stub patterns weaken several gates.** F-A11-011 (certify step builder unwired), F-A11-029 (convergence regression handler), F-A11-031 (cross-refs always True), F-A11-037 (semantic-layer call-site type-mismatched) all create the illusion of validation where none happens.
- **Sprint, tasklist, and roadmap feedback loops are unclosed.** F-A11-021 (no `tasklist generate` CLI), F-A11-022 (no R-item registry), F-A11-023 (sprint ignores dependencies), F-A11-024 (no roadmap-update from sprint outcomes) together leave the downstream side of the pipeline structurally incomplete.

## Brittleness drivers identified

- **Single point of failure on a single deterministic gate.** The anti-instinct gate uses AND-composition of three hard-zero checks driven by line-by-line regex; any one false positive halts the entire downstream pipeline with no escape valve (e.g., no `--allow-anti-instinct-warnings`, no TRAILING mode for anti-instinct).
- **No template layer to enforce structure.** Roadmap and tasklist generation rely on inline Python string composition + LLM "remember the schema" prompting; no template files exist, so structure is LLM-invented and varies per run / per agent persona.
- **One-shot subprocess capture with no completeness check.** `ClaudeProcess` uses `--print --output-format text`, no `content_complete` semantic check, no truncation detection, no continuation logic; combined with the non-streaming 64k fallback cap this is a silent-failure surface.
- **Frontmatter-parser duplication with conflicting semantics.** Two parsers (`_parse_frontmatter` byte-0, `_check_frontmatter` MULTILINE) coexist; semantic checks can fail on content the basic frontmatter check accepts.
- **Field-name and contract drift between gates / prompts / templates.** No registry binds the frontmatter field names that gates require to the names the checkers read or the names prompts instruct the LLM to emit; drift (`ambiguous_count`/`ambiguous_deviations`, dims 7-11 unconditional, TDD sentinel complexity) is invisible until E2E reveals it.
- **Retry-without-learning.** When a step fails its gate, the executor re-sends the identical prompt; partial output is overwritten with no diff. F-A11-017 succeeded by luck.
- **Sprint executor is dependency-blind.** Tasklist ordering becomes a load-bearing contract because `TaskEntry.dependencies` is parsed but never consulted.
- **No bidirectional state.** `.roadmap-state.json` is read by tasklist/auto-wire but never written back from sprint; the "continuous refinement" loop is structurally unimplemented.
- **No mechanism to prevent triage misclassification.** No policy gate, no checklist, no reviewer-pairing rule that forces "if a halt is described as pre-existing, isolate the trigger before accepting the classification."
- **Auto-detection chains lack rejection paths.** PRD-only input is silently misclassified rather than rejected with an actionable error; `--input-type` choices don't include `prd` even though detection can return it; missing roadmap.md crashes `tasklist validate` rather than emitting a graceful diagnostic.
