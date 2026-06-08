## Failure Taxonomy

Categorical breakdown of documented failures across all 14 Wave 1 partitions (159 failure-class findings, with overlap into 61 remediations and 51 successes). Findings are grouped by failure-shape rather than partition; each class lists ≥2 representative citations using the `(A<N>:F-A<N>-<seq>)` format.

### Gate Bypass / Vacuous PASS

Gates emit PASS while doing zero or wrong work — wrong target directory, fallback-on-uncertainty, or `gate=None` in alternative execution paths.

- **Frequency:** ~16 findings across 7 partitions (A2b, A3, A4, A6, A9, A11, A12).
- **Severity:** HIGH — the pipeline's primary trust signal silently lies.
- **Pipeline step(s) affected:** wiring-verification, spec-fidelity (convergence), validate, anti-instinct.
- **Representative findings:**
  - (A2b:F-A2b-002) Wiring-verification ran against `config.output_dir.parent` (release markdown dir), reported `files_analyzed: 0`, gate vacuously PASSED.
  - (A4:F-A4-004) Same wrong-directory bug surfaced in v2.24.5 / v1.2.1 / v3.0 — fixed at executor.py:1019-1022 with `files_analyzed > 0` guard only post-v3.05.
  - (A4:F-A4-003) `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` at executor.py:2167 — convergence path has no external gate.
  - (A12:F-A12-13) Sprint reuses roadmap's ANTI_INSTINCT_GATE; vacuous-pass fallback at executor.py:828-830 makes it a no-op for code-change tasks.
  - (A9:F-A9-010) cleanup-audit wiring scanned `.dev/releases/complete` with `total_findings: 0`, PASS.

### Wired-but-Inert / Dead-Code-on-Production-Path

Component implemented and tested, but unreachable from the actual production entry point (`execute_sprint`, `_build_steps`, `run_portify`).

- **Frequency:** ~12 findings across 5 partitions (A2b, A3, A6, A10, A11).
- **Severity:** HIGH — gives false confidence that a feature shipped.
- **Pipeline step(s) affected:** anti-instinct, certify, wiring-verification, sprint integration, cli-portify execution.
- **Representative findings:**
  - (A2b:F-A2b-003) All four anti-instinct modules exist, ANTI_INSTINCT_GATE defined, but `execute_sprint()` never calls `execute_phase_tasks()`; T04 bridge SKIPPED.
  - (A11:F-A11-011) `build_certify_step()` at executor.py:1899 is unreferenced anywhere else — step 13 never executes; certification-report.md never emitted.
  - (A3:F-A3-13) `_resolve_wiring_mode()` defined at executor.py:420-446 but `run_post_task_wiring_hook()` read `config.wiring_gate_mode` directly — scope-based resolution never executed.
  - (A7:F-A7-06) cli-portify `_execute_step()` had no-op default; `run_portify()` never passed `step_runner`; 8 step modules orphaned.
  - (A10:F-A10-019) v3.66 certify step never wired into `_build_steps()`; pipeline silently ended at remediate.

### LLM-Output Format Brittleness (Preamble / Truncation / Frontmatter)

Deterministic parsers fail on semantically-valid but format-deviant LLM output: byte-0 frontmatter checks, single-stream stdout scans, two parsers disagreeing on validity.

- **Frequency:** ~10 findings across 4 partitions (A2a, A5, A7, A11).
- **Severity:** HIGH — single-step failure cascades to halt at 0.9⁸ = 43% all-pass probability.
- **Pipeline step(s) affected:** extract (every step using shared `_check_frontmatter`), spec-fidelity, all 9 LLM steps.
- **Representative findings:**
  - (A2a:F-A2a-001) `_check_frontmatter()` did byte-0 `lstrip().startswith("---")` — 1-line Claude preamble halted extract.
  - (A11:F-A11-010) Two frontmatter parsers (`_parse_frontmatter` byte-0; `_check_frontmatter` re.MULTILINE) disagree, producing non-deterministic semantic-check pass/fail.
  - (A11:F-A11-007) `claude --print --output-format text` caps at 64k-token fallback; file silently truncated; no `content_complete` check.
  - (A5:F-A5-002) `detect_prompt_too_long()` scanned only stdout NDJSON, missed stderr where "Prompt is too long" actually landed.
  - (A5:F-A5-008) `_EMBED_SIZE_LIMIT = 200 * 1024  # 100 KB` value/comment mismatch above kernel MAX_ARG_STRLEN — 72 KB dead zone.

### LLM Non-Determinism / Sycophantic Convergence

LLM-driven gates and scoring produce different verdicts on identical inputs; "convergence" reflects agreement among remaining points, not coverage of all assumptions.

- **Frequency:** ~9 findings across 5 partitions (A1b, A4, A8, A9, A10).
- **Severity:** MEDIUM-HIGH — workarounds (5-vote consensus) are expensive, deterministic alternatives still incomplete.
- **Pipeline step(s) affected:** spec-fidelity, debate, score, validate.
- **Representative findings:**
  - (A4:F-A4-005) v3.0 spec-fidelity run 5 times, 4 distinct deviation counts (3H/9M/5L … 1H/6M/3L), Run 4 regenerated roadmap from scratch losing prior edits.
  - (A8:F-A8-006) Risk R1 (sycophantic convergence) Medium-High in v1.7 risk assessment, mitigations encoded in prompts only; no telemetry for Round-1 agreement detection.
  - (A4:F-A4-016) 5-vote statistical consensus introduced as bypass for non-deterministic spec-fidelity; expensive workaround.
  - (A1b:F-A1b-002) Composite-score deltas >0.75 on 7 of 17 proposals in adversarial scoring debate; 1-pt nominal-scale slop produces rank-flips.
  - (A8:F-A8-012) "Quantitative" RC/IC/SR/DC/SC scores are LLM-judged despite R2 mitigation specifying deterministic grep/regex.

### Spec → Roadmap Fidelity Drift (Generator Invents Structure)

Roadmap generator restructures phases, renumbers requirement IDs, fabricates FR/NFR IDs not in spec, drops contracts — all caught only by downstream spec-fidelity gate.

- **Frequency:** ~14 findings across 7 partitions (A1a, A1b, A3, A5, A7, A9, A10).
- **Severity:** HIGH — most frequent halt cause across the cli-portify arc (3 of 5 generations).
- **Pipeline step(s) affected:** generate-opus-architect, generate-sonnet-architect, merge, spec-fidelity.
- **Representative findings:**
  - (A1b:F-A1b-004) v2.22 had 15 deviations (3H/7M/5L): wrong module names, 4-phase spec → 7-phase roadmap, fabricated FR-001..FR-032 IDs never defined in spec.
  - (A7:F-A7-05) v2.24 halted at spec-fidelity with `high_severity_count: 3`; DEV-001 was "architecturally superior to spec" but no allowlist mechanism existed.
  - (A3:F-A3-16) Goal-1a, NFR-001 fabricated for tabular formatting; `_cross_refs_resolve` does not detect IDs absent from source spec.
  - (A5:F-A5-009) Roadmap renumbered SC-006 differently from spec §9, introduced SC-009b not in spec, referenced non-existent FR-008.
  - (A1b:F-A1b-005) v2.22 Phase 7 tasklist used D-0042..D-0050 instead of D-0035..D-0043 (context-window overflow caused ID drift).

### Spec-Fidelity Chain Has No Terminal Link to Code

Spec→Roadmap and Roadmap→Tasklist gates exist; no gate verifies implementation matches spec contracts (AST inspection, field names, importable callables).

- **Frequency:** ~8 findings across 4 partitions (A2b, A3, A4, A11).
- **Severity:** HIGH — root cause of cli-portify no-op shipping with `outcome: SUCCESS` and "72% complete with 3 CRITICAL bugs" v3.1 false-clean.
- **Pipeline step(s) affected:** spec-fidelity, wiring-verification, certify (when wired).
- **Representative findings:**
  - (A2b:F-A2b-004) v3.1 ValidationReport "CLEAN — 0 findings" same day gap analysis found 3 CRITICAL bugs; spec-fidelity compares roadmap-vs-spec, never implementation-vs-spec.
  - (A3:F-A3-15) v3.2 KPI field-name divergence (`wiring_net_cost` etc.) accumulated unchecked; pipeline ends at roadmap approval.
  - (A3:F-A3-17) cli-portify forensic — Link 3 (Tasklist→Code fidelity) does not exist; pipeline silently "succeeded" against nonexistent inputs.
  - (A4:F-A4-013) v3.05 shipped 3 runtime crash bugs (B1-B3) — `DeviationRegistry.load_or_create()` arg count, dict vs dataclass — no gate imports code and calls it.

### Anti-Instinct Regex False Positives (Vocabulary Collision)

Pure word-boundary regex matches scaffold/strategy/hardcoded vocabulary in legitimate non-obligation contexts (section headings, descriptive nouns, parenthetical labels).

- **Frequency:** ~7 findings across 4 partitions (A2a, A2b, A6, A11).
- **Severity:** HIGH — single point of pipeline failure (every enriched run halted).
- **Pipeline step(s) affected:** anti-instinct.
- **Representative findings:**
  - (A11:F-A11-001) Anti-instinct halted every enriched TDD/PRD pipeline run; 4-way matrix all FAIL with mixed `undischarged + uncovered + fp_coverage<0.7`.
  - (A11:F-A11-002) Bare `\bStrategy\b` matched section headings "Testing Strategy" / "Migration Strategy" — IC-001/002/006/007 false positives.
  - (A2a:F-A2a-003) `Scaffold` as imperative table-cell verb + `scaffolding` as parenthetical phase label both flagged HIGH; required vocabulary.py module to align scanner + prompt.
  - (A2b:F-A2b-001) V2-A obligation scanner shipped as pure-regex by deliberate design ("zero LLM calls") — false-positive surface is baked into design contract.

### Telemetry / Result-Parser Brittleness

Phase status, files_changed, last_task_id, phase_name extracted via text-regex against stream-json output; signals silently lost or misattributed.

- **Frequency:** ~7 findings across 2 partitions (A6, primarily; A5).
- **Severity:** MEDIUM — operationally confusing; PARTIAL silently promoted to PASS.
- **Pipeline step(s) affected:** sprint executor, sprint monitor.
- **Representative findings:**
  - (A6:F-A6-001) `_determine_phase_status()` checks `EXIT_RECOMMENDATION: CONTINUE` before `status: PARTIAL` — PARTIAL silently promoted to PASS; "telemetry lie."
  - (A6:F-A6-002) `FILES_CHANGED_PATTERN` regex looks for prose but stream-json emits structured `tool_use` events; every phase records `files_changed: 0`.
  - (A6:F-A6-003) `last_task_id` greedy regex matched cross-phase backreferences; cliEval records empty string after format change.
  - (A6:F-A6-007) Phase name extracted with leading "- " dash artifact from table-cell parsing instead of `# Phase N -- <Name>` heading.

### Retry / Convergence Logic Without Input Mutation

Retry re-runs identical prompt against identical inputs; convergence binary pass with no MANUAL_TRIAGE escape; budget debited for work that never happens.

- **Frequency:** ~8 findings across 5 partitions (A1b, A3, A11, A12).
- **Severity:** HIGH — exhausts budget on unfixable findings; misleads operators about cause.
- **Pipeline step(s) affected:** spec-fidelity (convergence), remediate, debate.
- **Representative findings:**
  - (A1b:F-A1b-006) v2.24-cli-portify halted at spec-fidelity after 2 identical-output retry attempts; motivated v5 pipeline rebuild with 4-class deviation taxonomy.
  - (A12:F-A12-02) Convergence binary pass predicate (`active_highs == 0`) with TurnLedger budget fields in halt message — operators mistake structural defect for budget exhaustion.
  - (A3:F-A3-18) v3.2 BLOCKING wiring mode debited TurnLedger budget for non-existent remediation; `_format_wiring_failure()`, `_recheck_wiring()` absent until T06/T07/T08.
  - (A12:F-A12-14) `_format_wiring_failure()` returns prompt string but never invokes subprocess; recheck necessarily reproduces same failure.

### Cross-Skill Contract Drift (Producer/Consumer Mismatch)

Consumer reads subset of producer's return-contract fields; convergence thresholds differ across sibling skills; CLI flags mismatch skill prose.

- **Frequency:** ~9 findings across 4 partitions (A9, A10, A11, A12).
- **Severity:** MEDIUM — silently drops observability signals; documentation drift.
- **Pipeline step(s) affected:** debate, merge, OTHER (skill/CLI surface).
- **Representative findings:**
  - (A10:F-A10-004) Release-split consumed 4 of 9 adversarial return fields, missing `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method`.
  - (A9:F-A9-003) `commands/roadmap.md` had 6 inference-only flags CLI doesn't implement; CLI exposed 11 flags command file didn't document — 17 mismatches.
  - (A10:F-A10-003) Convergence thresholds drifted (release-split 0.7/0.5 vs sc:roadmap 0.6/0.5) — no centralized policy.
  - (A9:F-A9-004) Skill described 5 waves; CLI ships 14 named steps — 6 step names absent from SKILL.md entirely.

### Severity-Calibration Failures (Gate Underclassification)

LLM-self-reported severity allows MEDIUM/LOW classification of structurally critical issues (ID namespace collisions, sequencing defects, fabricated IDs); HIGH-only blocking lets them through.

- **Frequency:** ~6 findings across 4 partitions (A4, A9, A10, A11).
- **Severity:** MEDIUM — gates pass with substantive defects undetected.
- **Pipeline step(s) affected:** spec-fidelity, deviation-analysis.
- **Representative findings:**
  - (A4:F-A4-020) SC-NNN reused for safety constraints AND release criteria — ID collision rated MEDIUM, non-blocking.
  - (A9:F-A9-009) cleanup-audit-v2 passed with 5 MEDIUMs including DEV-004 "Subagent failure handling deferred to Phase 4 but must be operational from Phase 1" — sequencing gap classified MEDIUM.
  - (A11:F-A11-009) DEVIATION_ANALYSIS_GATE field-name mismatch (`ambiguous_count` vs `ambiguous_deviations`) at gates.py:18, 389-403, 573, 589 — semantic check can never fire.

### Single-Agent Validation Overstates Coverage

Primary agents mark items COVERED that adversarial cross-validation shows MISSING or CONFLICTING; "validation theater" when same prompt runs on different models.

- **Frequency:** ~5 findings across 3 partitions (A2b, A5, A9).
- **Severity:** HIGH — false-clean signal would have masked CRITICAL bugs indefinitely.
- **Pipeline step(s) affected:** debate, spec-fidelity, validate.
- **Representative findings:**
  - (A5:F-A5-007) v3.7 TurnLedger D1 initially scored 100% (25/25); adversarial cross-validation (Claude + GPT + Kimi + Sonnet) corrected to 88%, surfaced 4 MISSING FRs + 2 CONFLICTS.
  - (A2b:F-A2b-004) 8 validator sub-agents across 4 phases all PASS / CLEAN with 0 findings while implementation 72% complete with 3 CRITICAL bugs.
  - (A9:F-A9-006) `build_reflect_prompt` accepts 3 params NEVER interpolated into prompt — multi-agent validation in v2.19 ran identical prompts on different models ("multi-model labeling theater").

### Plugin / Convention Override Without Mechanical Enforcement

External plugin (skill-creator) or default behavior (gh pr create) overrides project conventions because only instructional text — not hooks/gates — enforces them.

- **Frequency:** ~3 findings across 2 partitions (A10, A12).
- **Severity:** MEDIUM — caught post-hoc; required new hook layer.
- **Pipeline step(s) affected:** OTHER (governance, release engineering).
- **Representative findings:**
  - (A10:F-A10-005) skill-creator wrote ~100 eval artifacts to `.claude/skills/sc-release-split-protocol-workspace/` instead of `.dev/eval-workspaces/`; CLAUDE.md rule was instructional, no PreToolUse hook existed.
  - (A10:F-A10-007) `make verify-sync` existed in Makefile but no CI workflow invoked it — mechanical detection without invocation is decorative.
  - (A12:F-A12-08) Step 1.3 assumed `integration` branch from upstream CLAUDE.md convention; fork has only `master`. No static check pre-execution.

### Asymmetric Extractor/Comparator (Canonicalization Missing)

Lenient extractor produces tokens that strict downstream comparator rejects (D1 vs D01; bare `Strategy` vs `\bStrategy\b` headings; hyphenated FR-S10-02 vs word-boundary split).

- **Frequency:** ~4 findings across 1 partition (A12), but pattern generalizes.
- **Severity:** HIGH — convergence loop cannot reduce findings the comparator structurally cannot accept.
- **Pipeline step(s) affected:** spec-fidelity (structural_checkers), anti-instinct (integration_contracts).
- **Representative findings:**
  - (A12:F-A12-01) TUIBBS v1-MVP: 54 phantom_id HIGHs; spec `D1, D3, D5` vs roadmap `D01..D54`; `_canonicalize_requirement_id` helper added post-hoc.
  - (A12:F-A12-06) PR #86 `mechanism_signature` shipped without canonicalization invariants; hyphenated `FR-S10-02` dropped by `\b` word-boundary; required `_canonicalize_identifiers` helper.

### Process / Discipline Erosion (Verification Tier Skipped)

Verification tasks (T17-T22, T07/T11) marked SKIPPED while implementation tasks complete; no pipeline gate halts release on that basis; honor-system compliance.

- **Frequency:** ~4 findings across 2 partitions (A3, A4).
- **Severity:** MEDIUM — regressions become invisible until production failure.
- **Pipeline step(s) affected:** test-strategy, certify, OTHER (sprint discipline).
- **Representative findings:**
  - (A3:F-A3-19) v3.2 shipped with 6 of 6 verification tasks (T17-T22) SKIPPED; overall FAIL verdict but release shipped.
  - (A4:F-A4-013) v3.05 Wave 3 (T07 integration smoke test, T11 E2E tests) NOT EXECUTED; crash bugs fixed, recurrence prevention layer never built.

### Cross-Phase Contract & Phase Restructuring Drift

Spec names a contract (return type, sentinel, telemetry boolean) propagated to only one phase's body; roadmap restructures phases dropping spec's parallelization guidance; SKILL.md merge directives over-consolidate.

- **Frequency:** ~7 findings across 4 partitions (A5, A7, A10, A11).
- **Severity:** MEDIUM-HIGH — silent contract violations between phases; 49% task-count regression on TDD+PRD inputs.
- **Pipeline step(s) affected:** generate, merge, tasklist generation.
- **Representative findings:**
  - (A11:F-A11-005) 4.1× richer TDD+PRD input produces 49% FEWER actionable tasks (44 vs 87) — extraction destroys tabular granularity, no output template, PRD-suppression at tasklist/prompts.py:221-223.
  - (A5:F-A5-004) Phase 1 specified `_write_preliminary_result()` without `-> bool` return type; Phase 2's `_wrote_preliminary` telemetry depends on it; implementer producing `-> None` silently breaks Phase 2.
  - (A7:F-A7-07) v2.24.1 — spec defined 7 implementation phases; roadmap consolidated to 5, losing "Phases 1-2 can run in parallel" guidance; omitted `config.py` entirely (DEV-002).
  - (A10:F-A10-020) SKILL.md lines 233/255/259 — 3+ merge instructions with vague matching criteria cause over-consolidation.

---

**Summary counts:** 16 classes covering ~129 distinct failure findings (some findings appear in multiple classes due to compound causation, e.g., F-A11-001 spans anti-instinct regex + gate bypass). The remaining ~30 failure findings are partition-specific instances of the above classes (e.g., F-A10-011/012 portfolio-NFR carryover false positives are instances of "Severity-Calibration Failures").

**Top-3 severity-weighted classes (by frequency × HIGH severity × cross-partition reach):**
1. **Spec → Roadmap Fidelity Drift** — most frequent halt cause across the entire arc; recurs in every release with non-trivial generator surface.
2. **Wired-but-Inert / Dead-Code-on-Production-Path** — produces false confidence at release time; only caught by post-hoc gap analysis.
3. **Gate Bypass / Vacuous PASS** — undermines every other gate's trustworthiness; same wrong-target-dir bug recurred across 3 releases before fix landed.
