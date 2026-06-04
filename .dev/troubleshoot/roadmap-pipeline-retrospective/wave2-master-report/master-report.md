# Roadmap Pipeline Retrospective — Master Report

**Generated:** 2026-05-31
**Source:** 14 partition retrospectives synthesizing 64 releases (`.dev/releases/complete/`) + 77 tasks (`.dev/tasks/done/`)
**Wave-1 totals:** 262 findings — 159 failures, 61 remediations, 51 successes, 113 brittleness drivers identified
**Driver question:** *What recurring failures in the roadmap pipeline reveal architectural flaws so deep that targeted patches will keep losing — and what would a ground-up rewrite or refactor have to look like to make the brittleness go away permanently?*

---

## Executive Summary

The retrospective produces one architectural conclusion that the evidence chain forces: **the roadmap pipeline is brittle by substrate, not by bug**. Five deep structural flaws (Section 6) account for the overwhelming majority of failures across 9 release generations, and four of the five are classified INHERENT — they cannot be fixed without changing the pipeline's interchange primitives. The pipeline has grown monotonically from 9 steps (v4) → 11 (v2.22) → 13 (v5) → 14 (current) because each new failure class triggers a new validator rather than a constraint on the generator that produced it. The validator/generator asymmetry (Flaw 2) guarantees the next failure shape will arrive faster than the next validator can be authored, which is the operational signature of substrate-level brittleness.

**The three most-confident recurrence patterns** (Section 4) carry this thesis on their own:

1. **Spec-fidelity gate (~12 fix attempts across 8 partitions, A1a→A12).** Every redesign — LLM-only → 5-vote consensus → deterministic structural checkers → convergence engine → DeviationRegistry → canonicalizing comparator — closed the *previous* failure shape by adding machinery *around* the comparator. (A12:F-A12-03) names this the "multi-release harden-orchestration-around-broken-comparator" anti-pattern explicitly.

2. **"Written but not wired" (~8 attempts, A2b→A12).** Every release ships infrastructure (`TurnLedger`, `_resolve_wiring_mode()`, `build_certify_step()`, `tasklist generate` CLI subcommand, `_format_wiring_failure()`) that production entry points never reach. The pipeline has no terminal verification link from Tasklist → Code; spec-fidelity validates *roadmap-against-spec*, never *implementation-against-spec*.

3. **Roadmap fabricates / renumbers identifiers (~7 attempts, A1b→A12).** Roadmaps invent FR/NFR/SC/D-### identifiers absent from the spec on every release with >5 requirements, because the LLM's tabular-formatting bias produces IDs to fill columns and no gate enforces "every roadmap ID ∈ spec ID set ∪ accepted deviations". Each fix is per-instance; none install a bidirectional registry.

**Decision verdict — REWRITE.** Four of five flaws are INHERENT (Flaws 1, 2, 3, 5 in whole; Flaw 4's silent-skip half), and three of those four scope to *cross-cutting state* — the artifact-centric gate model (Flaw 1), markdown-frontmatter state (Flaw 3), and the missing contract-schema layer (Flaw 5) — none of which are subsystem boundaries that can be replaced independently. A REWRITE should preserve the working mechanisms (adversarial debate per Section 4's #18 RESOLVED-FOR-NOW pattern, the v3.05 deterministic structural-checker layer) but invert the substrate: typed cross-step state (sidecar JSON + dataclass), tool-write structured-output enforcement at every LLM step, a code-reaching terminal fidelity link (Tasklist → AST), and a central contract registry with bidirectional drift detection in CI.

The user's currently-blocking failure (anti-instinct halts on the MultiModelSwarm roadmap due to `stub`-as-component-name false positives at lines 207/211/213) is a *direct manifestation* of Flaw 2: a deterministic regex gate operating on LLM-generated text with no allowlist escape valve. Section 4 row #6 documents 4 prior remediations of this exact class. Per the verdict, patching this instance individually will *not* prevent the next.

---

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
## Remediation Taxonomy

This section groups the ~61 remediations recorded in Wave 1 by the *shape* of the fix attempted — not by the bug or the pipeline step, but by the structural move the engineer made. Each shape is followed by a status breakdown:

- **Stuck** = remediation that landed in artifact (spec, tasklist, prompt) but the underlying class of bug is "Still possible today" per Auggie evidence, or the recommendation never landed in code.
- **Regressed** = remediation that landed and then re-broke at a later release.
- **Superseded** = the remediation was replaced by a deeper, structurally different fix in a later release.

Counts span all 14 partitions. Findings tagged REMEDIATION or "FAILURE → REMEDIATION" were assigned to exactly one shape based on the dominant fix move.

---

### Add a downstream validator / new pipeline step

A new gate, step, or validator was appended downstream of an existing failing surface, leaving the original generator untouched.

- **Count:** 14 attempts
- **Stuck:** 9 — **Regressed:** 1 — **Superseded:** 3
- **Representative findings:**
  - `(A1b:F-A1b-003)` v2.20 produced 14 validation findings with no automated path to "findings fixed" → v2.22 added `remediate` (Step 10) + `certify` (Step 11) bringing pipeline count to 11. Shipped; outcome: pipeline keeps growing in step count (v4=9 → v2.22=11 → v5=13), each addition increasing coupling. Superseded by v5's `deviation-analysis` and convergence wrapper.
  - `(A1b:F-A1b-006)` v2.24-cli-portify spec-fidelity halted with futile-by-construction retry → v5 added `annotate-deviations` and `deviation-analysis` steps with 4-class taxonomy (SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED). Stuck at structural level: generator/validator asymmetry persists — validators are deterministic, generators are not, so every new failure class produces a new validator.
  - `(A4:F-A4-001)` `superclaude roadmap validate` introduced 7-dimension post-pipeline reflection (schema/structure/traceability/cross-file/interleave/decomposition/parseability). Stuck because gate is warn-not-fail by design `(A4:F-A4-002, F-A4-022)`.
  - `(A12:F-A12-13)` Sprint reuses roadmap's `ANTI_INSTINCT_GATE` despite contract mismatch; documented Path B (new third hook) but never shipped.

### Add a deterministic regex / structural check to replace LLM judgment

A pure-Python check (regex, set-difference, count check) was added in place of an LLM-judged predicate.

- **Count:** 9 attempts
- **Stuck:** 4 — **Regressed:** 3 — **Superseded:** 2
- **Representative findings:**
  - `(A2b:F-A2b-001)` Anti-instinct V2-A obligation scanner shipped as pure-regex by *deliberate design contract* ("zero LLM calls" elevated to spec property). Regressed: F-A11-002 (`\bStrategy\b` matched section headings), F-A11-003 (`\bhardcoded\b` matched descriptive prose), F-A12-04 (`DISPATCH` over-capture). Each regression patched with narrower regex; underlying brittleness (no syntactic context) remains by design.
  - `(A1a:F-A1a-007)` v2.0 quality-engineer caught duplicate step numbering manually in Phase 4 — same defect recurred in Phase 7 because no structural lint was added. Stuck.
  - `(A11:F-A11-009)` DEVIATION_ANALYSIS_GATE field-name mismatch (`ambiguous_count` vs `ambiguous_deviations`) annotated as pre-existing bug in `gates.py:18` but never fixed. Stuck (acknowledged unfixed).

### Add canonicalization at the comparator seam

Both sides of a comparison were normalized (case, ID format, whitespace, hyphenation) before set-difference. The dominant fix shape in late-arc spec-fidelity work.

- **Count:** 4 attempts
- **Stuck:** 1 — **Regressed:** 1 — **Superseded:** 0
- **Representative findings:**
  - `(A12:F-A12-01)` TUIBBS phantom_id 54-finding flatline: `_canonicalize_requirement_id` helper added to `structural_checkers.py`; both spec and roadmap normalized before set-diff; MEDIUM `id_schema_drift` emitted when canonical forms match but surface forms differ. Shipped, deterministic.
  - `(A12:F-A12-06, F-A12-07)` PR #86 introduced `mechanism_signature` without explicit canonicalization invariants → `_canonicalize_identifiers(text) -> frozenset[str]` added with 3-invariant docstring; Layer 3 case-insensitivity (`window_text.upper()`) enforced. Regressed once mid-cycle (hyphen-pattern matched prose kebab-case `class-priority`), fixed via digit-lookahead `(?=\S*\d)`. Stuck pattern: no project convention forces canonicalization at *every* extractor/comparator seam.

### Split LLM judgment across N voters / multi-agent adversarial pass

The same LLM check was run N times (or by N differently-prompted/differently-sized agents) and votes aggregated.

- **Count:** 8 attempts
- **Stuck:** 2 — **Regressed:** 0 — **Superseded:** 2
- **Representative findings:**
  - `(A4:F-A4-005, F-A4-016)` v3.0 unified-audit-gating could not pass its own spec-fidelity gate in 4 successive runs; solution: 5-vote consensus, majority severity wins, 1-2/5 findings classified NOISE. Worked for v3.0; expensive (5× gate cost); superseded by v3.05's structural-checker + convergence engine.
  - `(A5:F-A5-007)` v3.7 TurnLedger single-agent validation initially scored 100%; adversarial cross-validation (Claude + GPT + Kimi + Sonnet) corrected D1 to 88% and surfaced 10 HIGH coverage findings + 2 spec-roadmap CONFLICTS missed by both primary passes.
  - `(A8:F-A8-008)` Adversarial scoring debate Round 1 found 7 proposals with composite-score deltas >0.75 between Agent A and Agent B; debate methodology converged them. Mechanism works on meta-level but only because orchestrator gated on composite-delta — same-model sycophancy `(A8:F-A8-006)` remains structurally unverified.

### Move check to earlier stage / preflight gate

A failing condition was diagnosed pre-execution (Phase 0, preflight, baseline capture) rather than caught post-failure.

- **Count:** 6 attempts
- **Stuck:** 3 — **Regressed:** 0 — **Superseded:** 1
- **Representative findings:**
  - `(A5:F-A5-001)` Recursive `claude` subprocess deadlock (857s, exit 143, zero phases completed) → `execute_preflight_phases()` classifies phases via `execution_mode` annotation and runs EXEMPT-tier shell phases via `subprocess.run()` before the LLM loop begins. Shipped; gate is annotation-driven so unannotated phases can still deadlock.
  - `(A1b:F-A1b-008)` v2.25 spec carried 10 OQs at brainstorm, 8 at spec → roadmap Phase 0 ("Pre-Implementation Decisions") added as mandatory gate. Pattern looks sound but is process discipline, not pipeline enforcement.
  - `(A2a:F-A2a-001, F-A2a-003)` Compound-reliability framing (P(all 8 pass) = 0.9⁸ = 43%) justified shared-substrate fixes for byte-0 frontmatter parser and obligation scanner. Stuck: spec Section 8 explicitly defers protocol-parity audit across 6 remaining roadmap steps.

### Hoist shared constant / vocabulary into single source of truth

A duplicated definition (vocabulary list, threshold, frontmatter shape) was promoted to a single module with import-based consumers.

- **Count:** 5 attempts
- **Stuck:** 2 — **Regressed:** 1 — **Superseded:** 0
- **Representative findings:**
  - `(A2a:F-A2a-003)` Obligation-vocab false-positive (100% rate on legitimate planning vocabulary) → `src/superclaude/cli/vocabulary.py` created as single source: 11 SCAFFOLD_TERMS, 9 DISCHARGE_TERMS, 16-entry PREFERRED_ALTERNATIVES, `build_prompt_constraint_block()`. Both scanner and prompt builders import from it. Identity check via test.
  - `(A2a:F-A2a-010)` Sanitizer scope decision: roadmap-executor-local, NOT shared. Parallels obligation-vocab elevation to `cli/` (not `cli/roadmap/`) — opposite scoping choice. Stuck if sprint/other commands hit the same preamble pattern.

### Add structural template / tool-write mode to constrain LLM output

Instead of free-form prose, the LLM was forced to write into a template via tool_use writes, with `_validate_merge_completeness` enforcing section-by-section.

- **Count:** 3 attempts
- **Stuck:** 1 — **Regressed:** 0 — **Superseded:** 0
- **Representative findings:**
  - `(A8:F-A8-015)` R3 merge corruption (LLM turn-budget truncating 200-400 line artifacts mid-sequence) → `tool_write_mode=_roadmap_template is not None` + `template_path=_roadmap_template` + `_validate_merge_completeness` in MERGE_GATE. Confirmed working in v2.09 post-merge validation (PASS across structural integrity, internal references, contradiction re-scan).
  - `(A11:F-A11-007)` One-shot stdout capture hits 64k-token fallback cap with no truncation detection across all 9 LLM steps. Stuck: overhaul research §8 Phases 1-2 plan template-driven tool-use writing for *every* step; not executed.

### Externalize state via fixture / failure-injection harness

A test surface was created by externalizing the contract (return-contract YAML, fixture directory, `--resume-from` flag) so failure paths become deterministically reproducible.

- **Count:** 4 attempts
- **Stuck:** 1 — **Regressed:** 0 — **Superseded:** 0
- **Representative findings:**
  - `(A1a:F-A1a-008)` v2.02 shipped at 21/28 (75%) on QA scorecard, below 22/28 threshold → `fix-tasklist.md` 12-task remediation built `pipeline_diagnostics` block + `--resume-from` flag with 5 DC fixture directories (DC-1 missing fields through DC-5 fallback mode). All 12 tasks EXECUTED COMPLETE; +7 score impact projected.
  - `(A5:F-A5-005)` Hash-mismatch on documentation-only spec edits triggered full 28-min pipeline re-run → `accept-spec-change` CLI command + evidence gate requiring `dev-*-accepted-deviation.md` with `disposition: ACCEPTED` + recursion guard (max 1 cycle).

### Convergence-engine wrapper (loop with budget, mutate inputs between attempts)

Instead of binary halt, wrap the failing step in a multi-iteration loop with TurnLedger budget, registry-tracked findings, and inter-iteration state mutation.

- **Count:** 3 attempts
- **Stuck:** 2 — **Regressed:** 0 — **Superseded:** 0
- **Representative findings:**
  - `(A7:F-A7-18)` Across v2.15 → v2.24.1, spec-fidelity halt-and-die was binary; v2.25 wrapped in `_run_convergence_spec_fidelity()` max_runs=3. Live but `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` `(A4:F-A4-003)` — convergence runs ship without external format-validating gate. Stuck.
  - `(A12:F-A12-02)` Convergence loop's binary `active_highs == 0` predicate has no MANUAL_TRIAGE escape; halt formatter at `convergence.py:653-668` emits TurnLedger numbers leading operators to misread structural defects as budget exhaustion. S6 (MANUAL_TRIAGE) deferred from backlog.

### Manual override / hand-classification / authored-deviation declaration

When a scanner or gate failed, the operator declared the answer by hand (manual contracts, PRE_APPROVED rows, accepted-deviation records, `manual_declaration: true` flags).

- **Count:** 7 attempts
- **Stuck:** 5 — **Regressed:** 2 — **Superseded:** 0
- **Representative findings:**
  - `(A7:F-A7-05)` v2.24 spec-fidelity halted on 3 HIGH; one was an architecture-superiority-over-spec deviation. Side-channel `dev-001-accepted-deviation.md` (28KB) documented why DEV-001 is correct and spec should change. No machine-readable allowlist exists; gate still counts DEV-001 as HIGH on every re-run. Recurred in F-A7-07 v2.24.1.
  - `(A10:F-A10-008)` task-builder-merge anti-instinct auto-detection returned 0 contracts; manual override declared 7 IC contracts. Audit passes only because human did the work the scanner was supposed to do.
  - `(A10:F-A10-011, F-A10-012)` 2 PRE_APPROVED templates + 4 INTENTIONAL portfolio NFRs flagged as deviations *every release*; manual classification each release; no scope-boundary semantics in spec-fidelity layer.

### Wire previously-defined-but-dead code into production entry point

A function existed, had tests, had a hook — but the production caller never invoked it. Remediation = add the call site.

- **Count:** 4 attempts
- **Stuck:** 2 — **Regressed:** 0 — **Superseded:** 0
- **Representative findings:**
  - `(A2b:F-A2b-003)` Anti-instinct gate complete but `execute_sprint()` never calls `execute_phase_tasks()` (production used per-phase subprocess); v3.1 gap-remediation T04 (the critical bridge) SKIPPED. Eventually closed in `(A3:F-A3-12)` v3.2 — `run_post_phase_wiring_hook` wired at sprint/executor.py:1289.
  - `(A3:F-A3-13)` `_resolve_wiring_mode()` written but `run_post_task_wiring_hook()` read `config.wiring_gate_mode` directly. One-line fix; closed.
  - `(A11:F-A11-011)` `build_certify_step()` defined at `executor.py:1899`, never invoked. Stuck. v3.66 phase-2-certify-wiring tasklist tracked the fix `(A10:F-A10-019)` but verification not confirmed.

### Add structural lint / CI enforcement of architecture policy

Make a previously-instructional rule machine-enforced via Makefile target + CI workflow + PreToolUse hook.

- **Count:** 4 attempts
- **Stuck:** 2 — **Regressed:** 0 — **Superseded:** 0
- **Representative findings:**
  - `(A3:F-A3-05)` `make lint-architecture` made command-skill linkage, size warnings, naming consistency, and sync integrity CI-enforced. 6 of 10 checks implemented; 4 unimplemented (BUG-006).
  - `(A10:F-A10-005, F-A10-006, F-A10-007)` skill-creator plugin wrote ~100 eval artifacts into `.claude/skills/` violating governance; verify-sync existed but no CI invoked it; error message misled authors to wrong fix. Five-layer remediation: `.dev/README.md` documentation + Makefile context-aware message + CI wiring of verify-sync + `*-workspace` suffix blocklist + PreToolUse hook + CLAUDE.md override. Tracked in 5-phase tasklist, validation report 14/14 RESOLVED.

### Re-frame failed RCA / corrective root-cause analysis

A prior remediation effort misframed the bug; corrective RCA traced the true cause and either invalidated the original fix or re-pointed it.

- **Count:** 3 attempts
- **Stuck:** 1 — **Regressed:** 0 — **Superseded:** 1
- **Representative findings:**
  - `(A12:F-A12-03)` Multi-release "harden orchestration around comparator" anti-pattern — every prior spec-fidelity remediation (DeviationRegistry, TurnLedger, monotonic-progress, regression detection, S1/S2/S5) hardened the loop without touching the broken `phantom_ids = roadmap_ids - spec_ids` comparator. F-A12-01 was the first comparator-side fix.
  - `(A12:F-A12-12)` Tasklist generation "collapse" (87 spec-only vs 44 TDD+PRD tasks) framed as PRD suppression / merge directive defects across multiple research files; deep-dive `r-item-collapse-investigation.md` proved 1:1:1 R-item → task mapping in both cases. Actual driver: roadmap *format* (table-row dense vs delivery-milestone narrative). Reframed as design intent.

---

**Cross-shape observations** (not findings; synthesis):

- The 14 shapes are *not* equally durable. Shapes that mutate the producer ("canonicalize at the seam," "hoist shared vocabulary," "structural template") show low recurrence; shapes that add downstream consumers ("new validator," "manual override," "convergence wrapper") accumulate technical debt — every release adds infrastructure, none removes.
- "Stuck" outcomes cluster around two shapes: (a) downstream validators with no enforcement (warn-not-fail) and (b) manual overrides for scanner failures. Both leave the original generator/scanner unchanged.
- The single most-recurring class of "Regressed" remediation is regex-based deterministic checks — the v2-A "zero LLM calls" design contract `(A2b:F-A2b-001)` is downstream-fragile by construction.
## Recurrence Matrix

Failures appearing in ≥2 partitions, sorted by Times-fixed DESC. A "fix attempt" is any cited remediation, accepted deviation, or local workaround associated with the failure class — irrespective of whether the structural pattern was eliminated. Verdict reflects whether the *failure class* remains structurally possible per the latest partition-cited Auggie check, not whether a specific instance was closed.

| # | Failure (short name) | Partitions | First seen (oldest partition) | Last seen (newest) | Times "fixed" | Verdict | Evidence (≥2 finding citations) |
|---|---|---|---|---|---|---|---|
| 1 | Spec-fidelity LLM-only / non-deterministic / phantom-ID gate (high_severity_count binary halt; LLM-judged severity; no programmatic spec↔roadmap ID cross-ref) | A1a, A1b, A4, A7, A9, A10, A11, A12 | A1a (v2.0 C1/C2 spec-panel) | A12 (TUIBBS v1-MVP D-family canonicalizer) | ~12 | RECURRENT | (A4:F-A4-005), (A4:F-A4-006), (A7:F-A7-04), (A7:F-A7-05), (A7:F-A7-07), (A1b:F-A1b-004), (A9:F-A9-006), (A10:F-A10-022), (A12:F-A12-01), (A12:F-A12-03), (A11:F-A11-009) |
| 2 | Gate / step "written but not wired" — function defined, never invoked from production path (cert step, `_resolve_wiring_mode`, `_format_wiring_failure`, T04 sprint bridge, `tasklist generate` CLI subcommand) | A2b, A3, A4, A10, A11, A12 | A2b (v3.1 T04/T05 skipped) | A12 (`_format_wiring_failure` stub) | ~8 | RECURRENT | (A2b:F-A2b-003), (A3:F-A3-12), (A3:F-A3-13), (A10:F-A10-019), (A11:F-A11-011), (A11:F-A11-021), (A12:F-A12-14) |
| 3 | Wiring-verification gate scans wrong directory or empty target, silently PASSes with 0 findings | A2b, A4, A6, A9 | A2b (v3.1 release-dir target) | A6 (cliEval 7 orphan modules, soft mode) | ~5 | PARTIALLY-RESOLVED (specific src/superclaude default landed; structural "must verify target non-empty" invariant not codified) | (A2b:F-A2b-002), (A4:F-A4-004), (A4:F-A4-021), (A6:F-A6-010), (A9:F-A9-010) |
| 4 | Roadmap fabricates/renumbers FR/NFR/SC/D-### identifiers absent from spec; no bidirectional ID registry | A1b, A3, A4, A5, A7, A12 | A1b (v2.22 invented FR-001..FR-032) | A12 (D01..D54 canonical drift) | ~7 | RECURRENT | (A1b:F-A1b-004), (A3:F-A3-16), (A4:F-A4-006), (A5:F-A5-009), (A7:F-A7-15), (A12:F-A12-01) |
| 5 | Phase restructure / module-layout deviation between architect output and spec (architects optimise execution units; spec optimises logical decomposition) | A1b, A3, A7, A10 | A1b (v2.22 4 spec phases → 7 roadmap phases) | A10 (cross-framework Phase 0 added) | ~5 | RECURRENT | (A1b:F-A1b-004), (A7:F-A7-04), (A7:F-A7-05), (A7:F-A7-07), (A7:F-A7-16), (A10:F-A10-022) |
| 6 | Anti-instinct false-positive on legitimate vocabulary (scaffold-as-noun, "Strategy" headings, "hardcoded" config descriptors); gate hard-halts entire pipeline | A2a, A2b, A6, A10, A11 | A2a (v.2.17 obligation-vocab) | A11 (TDD+PRD 4-way matrix) | ~4 | RECURRENT | (A2a:F-A2a-003), (A2b:F-A2b-001), (A2b:F-A2b-006), (A6:F-A6-014), (A10:F-A10-008), (A11:F-A11-001), (A11:F-A11-002), (A11:F-A11-003) |
| 7 | Convergence-threshold drift / advisory-not-enforcing (gate validates score parses; releases ship at 0.72 below 0.80; sibling skills use 0.6/0.5 vs 0.7/0.5) | A1b, A8, A9, A10 | A1b (v.2.11 1-pt nominal-scale slop) | A10 (release-split 0.7/0.5 vs roadmap 0.6/0.5) | ~3 | RECURRENT | (A1b:F-A1b-002), (A8:F-A8-002), (A9:F-A9-007), (A10:F-A10-003) |
| 8 | `_cross_refs_resolve` / cross-reference gate always-True stub | A4, A9, A11 | A9 (v2.20 "too fragile for now") | A11 (C-108 still BACKLOG) | 2 | RECURRENT | (A9:F-A9-005), (A11:F-A11-031), (A4:F-A4-010) |
| 9 | Retry without input mutation — identical prompt re-run produces identical output, exhausts retry budget | A1b, A11, A12 | A1b (v2.24 cli-portify spec-fidelity halt) | A12 (D-family flatline 58→54→54 over 3 runs) | 3 | RECURRENT | (A1b:F-A1b-006), (A11:F-A11-017), (A12:F-A12-02) |
| 10 | Generator/validator asymmetry; validators deterministic, generators non-deterministic; every fix adds a downstream validator, none constrain generator | A1b, A2a, A4, A12 | A1b (Phase 7 ID drift caught post-hoc) | A12 (multi-release "harden orchestration around comparator") | ~4 | RECURRENT | (A1b:F-A1b-005), (A2a:F-A2a-005), (A2a:F-A2a-007), (A4:F-A4-012), (A12:F-A12-03) |
| 11 | Skill / SKILL.md drift from CLI (waves vs 14 step IDs; flag mismatches; schema drift between protocol refs and CLI prompts) | A2a, A9 | A2a (v.2.17 schema drift §8 deferred audit) | A9 (roadmap-cli-skill-converge 17-flag mismatch) | 2 | RECURRENT (round closed; no automated `--help`↔doc gate) | (A2a:F-A2a-002), (A9:F-A9-003), (A9:F-A9-004), (A9:F-A9-008), (A9:F-A9-020) |
| 12 | Validation/spec-fidelity declared CLEAN/PASS while implementation incomplete or production-path unreachable (gate validates report frontmatter, not behavior) | A2b, A3, A4 | A2b (v3.1 8 sub-agents CLEAN with 3 CRITICAL bugs) | A4 (v3.05 5 BLOCKING + tasklist_ready:false ships) | 2 | RECURRENT | (A2b:F-A2b-004), (A2b:F-A2b-007), (A3:F-A3-15), (A4:F-A4-022) |
| 13 | Frontmatter / preamble parser brittleness (byte-0 strict vs MULTILINE; LLM preamble breaks STRICT gates; two parsers disagree) | A2a, A4, A11 | A2a (v.2.17 _check_frontmatter byte-0) | A11 (`_parse_frontmatter` vs `_check_frontmatter` conflict still live) | 2 | PARTIALLY-RESOLVED (sanitizer + regex tolerance landed; duplicate parsers with conflicting semantics persist) | (A2a:F-A2a-001), (A2a:F-A2a-009), (A4:F-A4-010), (A11:F-A11-010) |
| 14 | Verification / Wave-3 / certify tasks silently skipped — pipeline does not gate on verification completion | A2b, A3, A4, A11 | A2b (v3.1 T11-T14 skipped) | A11 (certify still dead code) | 1 | RECURRENT | (A2b:F-A2b-003), (A3:F-A3-19), (A4:F-A4-013), (A11:F-A11-011) |
| 15 | Adversarial findings dropped silently at merge (~10-15%); no completeness invariant tying debate transcript items to merged roadmap | A8, A9 | A8 (v2.09 R3 mitigation) | A9 (v2.07/v2.13/v2.20 cited recurrence) | 1 | RECURRENT | (A8:F-A8-005), (A8:F-A8-016), (A9:F-A9-011), (A9:F-A9-012) |
| 16 | Telemetry/text-regex against structured stream-json (PARTIAL→PASS promotion, files_changed=0, last_task_id="", phase-name leading dash) | A6 (cross-cuts A1a, A11) | A6 (v2.07 P0 IMP-001) | A6 (cliEval May-21) | 0 | RECURRENT | (A6:F-A6-001), (A6:F-A6-002), (A6:F-A6-003), (A6:F-A6-004), (A6:F-A6-007) |
| 17 | Context-window exhaustion / sprint phase OOM / max-turns budget collapse (exit -9, "Prompt is too long", first-run-fails-resume-passes) | A1a, A5, A6, A7 | A1a (v2.02 Phase 2 exit -9 silent) | A6/A7 (cliEval Phase 5 / v2.25 Phase 3 crash) | 1 | RECURRENT | (A1a:F-A1a-009), (A5:F-A5-002), (A6:F-A6-006), (A7:F-A7-09) |
| 18 | Subprocess `--file` flag broken (cloud-download, not local injector); inline embedding now mandatory | A3, A7, A8 | A3 (v2.13 D3 0-byte outputs) | A8 (file-passing-debate 95% confidence) | 1 | RESOLVED-FOR-NOW (`_embed_inputs` permanent; `--file` cannot regress without deleting comment) | (A3:F-A3-10), (A7:F-A7-12), (A8:F-A8-001) |
| 19 | Spec-fidelity / deviation classifier produces UNCLASSIFIED, hex stable_ids, or false-positives forcing manual triage every release (portfolio NFRs, template files, malformed tokens) | A6, A10 | A6 (cliEval 20 false-positives, 100% NO_ACTION) | A10 (v3.66 14 UNCLASSIFIED hex IDs) | 1 | RECURRENT | (A6:F-A6-008), (A6:F-A6-009), (A10:F-A10-010), (A10:F-A10-011), (A10:F-A10-012), (A10:F-A10-018) |
| 20 | One-shot stdout / 64k token cap / no truncation detection / no template enforcement → 49% fewer tasks on TDD+PRD vs spec-only | A11, A12 | A11 (TASK-RF-quality-comparison) | A12 (corrected RCA: format artifact + no phase-count floor) | 0 | RECURRENT | (A11:F-A11-005), (A11:F-A11-006), (A11:F-A11-007), (A11:F-A11-019), (A11:F-A11-020), (A12:F-A12-12) |
| 21 | Sprint executor ignores task dependencies; reuses roadmap gates vacuously; no feedback loop back to roadmap | A6, A11, A12 | A6 (no PARTIAL state) | A12 (sprint reuses ANTI_INSTINCT_GATE vacuously) | 0 | RECURRENT | (A6:F-A6-001), (A11:F-A11-023), (A11:F-A11-024), (A12:F-A12-13) |
| 22 | "Silent skip on uncertainty" institutionalised as design (`--no-codebase`, `--no-validate`, MEDIUM-non-blocking, fail-open ambiguous=found, false-negative-preferred) | A2a, A4, A9 | A2a (Stage 9 deviation: Edit-tool over strict compliance) | A9 (v2.21 brainstorm "if uncertain do NOT trigger") | 0 | RECURRENT | (A2a:F-A2a-008), (A4:F-A4-012), (A9:F-A9-002), (A9:F-A9-009), (A9:F-A9-013), (A9:F-A9-018) |

### Top 3 most-retried failures — what their persistence reveals

**#1 Spec-fidelity gate (≈12 attempts across 8 partitions).** The fidelity check has been redesigned more times than any other gate — LLM-only → 5-vote consensus (v3.0) → structural deterministic checkers (v3.05) → convergence engine with TurnLedger budget (v3.05/v5) → DeviationRegistry with classification taxonomy (v2.26) → canonicalising comparator with id_schema_drift demotion (v3.7+, A12). Each redesign closed the *previous* failure shape (binary halt without remediation; non-deterministic 5-run regeneration; phantom-ID HIGH on D01-vs-D1 drift) by adding machinery *around* the comparator. (A12:F-A12-03) names this the "multi-release harden-orchestration-around-broken-comparator" anti-pattern explicitly: every release until A12 wrapped DeviationRegistry, TurnLedger, monotonic-progress, regression-detection, parser sanitization and route_findings around the same `phantom_ids = roadmap_ids - spec_ids` set-difference, leaving the comparator untouched. The persistence reveals that *the gate's job is structurally hard* — it has to reconcile (a) LLMs that legitimately improve on input specs, (b) extractor leniency vs comparator strictness, (c) binary-pass predicates that can't represent "structurally unfixable", and (d) severity classification entrusted to the LLM under audit. Each fix is correct for the shape it caught and irrelevant for the next shape.

**#2 "Written but not wired" (≈8 attempts).** This pattern is the canonical "anti-instinct gate's own bug" — every remediation that builds infrastructure objects, hooks, and helpers without verifying the production entry-point reaches them. v3.1 shipped `TurnLedger` / `ShadowGateMetrics` / `DeferredRemediationLog` / `SprintGatePolicy` complete with tests, while `execute_sprint()` never instantiated any of them (A2b:F-A2b-003); v3.2 shipped `_resolve_wiring_mode()` and `run_post_phase_wiring_hook()` defined but unwired (A3:F-A3-12, A3:F-A3-13); v3.66 shipped `build_certify_step()` with no orchestration call so the pipeline ends at remediate (A10:F-A10-019, A11:F-A11-011); cli-portify shipped `step_runner` parameter never provided in production (A3:F-A3-17); `tasklist generate` CLI subcommand has a prompt builder but no Click command (A11:F-A11-021); `_format_wiring_failure()` debits remediation budget without invoking a subprocess (A12:F-A12-14). What this reveals: the pipeline has *no terminal verification link* from Tasklist→Code. Spec-Fidelity validates roadmap-against-spec, Wiring-Verification scans markdown (until A4:F-A4-004 was fixed), and the Verification wave (T17-T22) is silently skippable (A3:F-A3-19, A4:F-A4-013). Until a smoke test imports each new wiring path and calls it with minimal inputs, every release can ship infrastructure that is dead in production while passing every artifact-shape gate.

**#3 Roadmap fabricates / renumbers identifiers (≈7 attempts).** Roadmaps invent FR-001..FR-032 / NFR-001..NFR-014 (A1b:F-A1b-004), `Goal-1a` / `NFR-001` not in spec (A3:F-A3-16), SC-009b / FR-008 (A5:F-A5-009), D01..D54 vs spec D1/D3/D5 (A12:F-A12-01) — every release with non-trivial requirement decomposition does this. Each remediation is per-instance: add a Traceability Matrix, mark severity LOW, declare an accepted deviation, canonicalise the comparator. None install a bidirectional spec↔roadmap ID registry with deterministic cross-reference. (A3:F-A3-16) and (A11:F-A11-022) both call this out: `_cross_refs_resolve` validates that referenced IDs resolve to something but does not detect fabricated IDs that don't exist in source spec, and the generation-time LLM independently re-derives R-items at validation-time with no shared registry. The persistence reveals that the LLM's tabular-formatting bias produces IDs to fill columns, and the gates accept any ID-shaped token as long as it doesn't break shape constraints. Until the extract step emits a spec-derived ID set and the merge gate enforces "every roadmap ID ∈ spec ID set ∪ accepted-deviations", this failure class will recur on every release with >5 requirements.
## Pipeline-step Heat Map

The table below maps each of the 14 named pipeline steps to its retrospective footprint across the 14 partition reports. Counts are derived by tagging every Wave 1 finding (262 total) to the `Pipeline step` field declared in the finding header; findings tagged `OTHER` are excluded from per-step rows (they account for the bulk of the missing 159+61+51 = 271 ≠ 262 reconciliation: a small number of findings span two steps and are credited to the most-proximate one). Risk verdicts reflect whether the *structural* failure mode is still reachable in the current `src/superclaude/cli/roadmap/` tree per inline Auggie checks across the partitions, not whether the specific historical incident recurs.

| Step | Failures | Remediations | Successes | Current-codebase risk verdict | Representative finding |
|---|---|---|---|---|---|
| extract | 9 | 3 | 2 | **HIGH** — byte-0 frontmatter parser still co-exists with MULTILINE variant; preamble contamination class still reachable; PRD-only input still silently misclassified; one-shot stdout capture still truncates at 64k with no completeness check (A2a:F-A2a-001, A11:F-A11-007, A11:F-A11-010, A11:F-A11-018) | Preamble contamination halts pipeline at step 1/8 with zero tolerance — `lstrip().startswith("---")` gate rejects valid extraction with 1-line preamble (A2a:F-A2a-001); v2.15 cli-portify pipeline halted on identical class (A7:F-A7-01) |
| generate-opus-architect | 6 | 4 | 3 | **MED** — IDs/phase-counts still freely reinvented at generation; no template-driven structure; merge prompt missing the ID-preservation clause that generate carries; but `_embed_inputs` + tool-write mode close the largest historical class (A11:F-A11-008, A1b:F-A1b-005, A7:F-A7-16) | Context-window overflow caused Phase 7 ID drift (D-0042..D-0050 instead of D-0035..D-0043, references to non-existent R-055/056/057) — generator silently produced it; validator caught post-hoc (A1b:F-A1b-005) |
| generate-sonnet-architect | 5 | 3 | 2 | **MED** — Haiku/Sonnet variant exhibits retry instability on enriched PRD context; validator definitional disagreements ship as WARNING only; convergence-score below threshold ships as PASS because gate only checks float range (A11:F-A11-016, A10:F-A10-027, A9:F-A9-007) | TDD+PRD haiku-architect needed 2 attempts where the other 3 runs needed 1 — model-capacity ceiling under enriched-prompt sizes; no per-model prompt-size budgeting (A11:F-A11-016) |
| diff | 2 | 1 | 3 | **MED** — diff-only architecture is structurally unable to surface shared assumptions across variants (Replay-Guard-Bypass and Index-Tracking-Stall escaped this way in v0.04); AD-2 shared-assumption extraction designed but orchestration wiring not enforced (A8:F-A8-003, A8:F-A8-004) | "When all variants share an assumption (explicitly or implicitly), that assumption receives zero scrutiny regardless of how critical it is" — two real production bugs escaped via shared blind spot (A8:F-A8-003) |
| debate | 7 | 4 | 5 | **HIGH** — no convergence-gate between debate and merge (80% threshold is advisory); same-family validator-on-generator pairing is structural; sycophancy detector exists only as documentation; 0.72 convergence routinely ships as PASS (A8:F-A8-002, A8:F-A8-006, A9:F-A9-007, A1b:F-A1b-002) | v2.20 shipped at convergence 0.72 with 4 unresolved disagreements at round 3; `_convergence_score_valid()` only checks the value parses as float in [0.0, 1.0] (A9:F-A9-007); composite-score 1-pt slop produces rank-flips (A1b:F-A1b-002) |
| score | 3 | 3 | 3 | **MED** — "quantitative" RC/IC/SR/DC/SC metrics still LLM-judged rather than deterministic regex (R2 mitigation never landed in code); convergence threshold drift across sibling skills (release-split used 0.7/0.5, sc:roadmap uses 0.6/0.5) (A8:F-A8-012, A10:F-A10-003, A1b:F-A1b-002) | R2 mitigation was "use deterministic grep/regex for quantitative layer (no LLM judgment)"; current `build_score_prompt` delegates to a Claude subprocess — round-coarse outputs (0.95, 0.85, 1.00) consistent with LLM-coarse not regex-counted (A8:F-A8-012) |
| merge | 12 | 6 | 4 | **HIGH** — `_cross_refs_resolve()` known-broken stub still returns True; FR/NFR/SC IDs invented without traceability table (recurrent across v2.23/v2.24.1/v3.2); ~10–15% of adversarial findings drop silently with no completeness check; ID preservation clause omitted from merge prompt (A9:F-A9-005, A7:F-A7-15, A9:F-A9-011, A11:F-A11-008) | `_cross_refs_resolve()` "always returns True; the cross-reference check is non-enforcing — `# Don't fail on this — it's too fragile for now`" (A9:F-A9-005); ~85–90% adversarial incorporation rate observed across v2.07/v2.13/v2.20 (A9:F-A9-011) |
| anti-instinct | 14 | 8 | 2 | **HIGH** — pure-regex by *design contract* (zero LLM calls); hard-zero AND-composition (undischarged_obligations==0 AND uncovered_contracts==0 AND fingerprint_coverage>=0.7) halts every enriched run; vacuous-pass surface when reused by sprint pipeline; multi-release "harden orchestration around comparator" anti-pattern (A2b:F-A2b-001, A11:F-A11-001, A12:F-A12-13, A11:F-A11-046) | Every TDD/PRD enriched pipeline halts here — TDD-only 5 undischarged + 4 uncovered + 0.76; TDD+PRD 1+4+0.73; Spec-only 0+3+0.72; Spec+PRD 0+3+0.67 — ALL FAIL (A11:F-A11-001); design-philosophy states "LLM-on-LLM review shares the same blindspots" (A2b:F-A2b-001) |
| wiring-verification | 9 | 4 | 3 | **MED** — original `source_dir` bug (gate scanned release artifact dir, 0 files, silent PASS) is FIXED in current code (A4:F-A4-004); but soft-mode default still produces noise (7 orphan-module findings non-blocking, A6:F-A6-010); AST-only analysis still misses dynamic imports (cliEval false positives); `_format_wiring_failure()` debits budget without invoking remediation subprocess (A4:F-A4-004, A6:F-A6-010, A12:F-A12-14) | Gate scanned `.dev/releases/complete/` markdown instead of `src/` Python; analyzed 10 markdown files, found 0 findings, silently PASSed; subsequent fix landed `files_analyzed > 0` guard (A4:F-A4-004); `_format_wiring_failure()` builds prompt + debits budget + reruns recheck with no subprocess between (A12:F-A12-14) |
| test-strategy | 1 | 0 | 2 | **LOW** — when reached, the step produces structurally sound artifacts threading convergence-failure metadata into downstream (test-strategy.md records partial-status); but most enriched runs never reach it because anti-instinct halts upstream (A8:F-A8-010, A11:F-A11-001) | Test-strategy YAML frontmatter correctly threaded `Adversarial convergence: 79% (PARTIAL). Unresolved: X-002 M5 dependency model (62% confidence)` from upstream debate stall (A8:F-A8-010) |
| spec-fidelity | 18 | 11 | 6 | **HIGH** — hard-fails on `high_severity_count==0` with no allowlist mechanism for architecture-superior-to-spec deviations; LLM-driven severity classification has documented non-determinism (5 runs / 4 distinct counts on same input); D-family ID-schema asymmetric extractor/comparator was the canonical multi-release failure; MEDIUM-non-blocking policy lets cross-cutting infrastructure ship deferred (A7:F-A7-05, A4:F-A4-005, A12:F-A12-01, A9:F-A9-009) | 5 spec-fidelity runs on identical input produced 3H/9M/5L → 3H/8M/5L → 1H/6M/3L → 3H/8M/4L (roadmap regenerated from scratch mid-loop) → 0H/7M/3L (A4:F-A4-005); TUIBBS v1-MVP 54 phantom_id HIGHs from `\bD-?\d+\b` lenient extractor vs strict comparator (A12:F-A12-01) |
| deviation-analysis | 4 | 2 | 1 | **HIGH** — field-name mismatch `ambiguous_count` vs `ambiguous_deviations` in gate code (annotated as known bug but unfixed); cliEval ran with placeholder classifier producing 100% false positives, requiring manual triage; portfolio-NFRs and template files re-flagged every release (A11:F-A11-009, A6:F-A6-008, A10:F-A10-011, A10:F-A10-012) | DEVIATION_ANALYSIS_GATE requires frontmatter `ambiguous_count` but semantic check reads `ambiguous_deviations` — field name mismatch, "Pre-existing bug" annotated in code at gates.py:18 yet still unfixed (A11:F-A11-009); cliEval emitted 20 deviations, all 20 resolved as NO_ACTION via manual triage (A6:F-A6-008) |
| remediate | 7 | 5 | 1 | **MED** — convergence-engine wraps with max_runs=3 (good); but identical-prompt-on-retry pattern means structurally-unfixable findings burn budget then halt; receiver-only wiring pattern routinely leaves config-threading half-done; 30% per-patch diff guard makes correct fixes unreachable when they exceed budget (A1b:F-A1b-006, A12:F-A12-01, A5:F-A5-003, A12:F-A12-02) | v2.24 spec-fidelity exhausted 2-attempt retry budget with identical inputs producing identical outputs — drove entire v5 pipeline rebuild (A1b:F-A1b-006); convergence binary pass predicate + no MANUAL_TRIAGE escape leads operators to misread structural defect as budget exhaustion (A12:F-A12-02) |
| certify | 3 | 0 | 0 | **HIGH** — `build_certify_step()` defined but never invoked; pipeline silently ends at remediate; certify_prompts parser uses wrong finding-format regex (academic until certify is wired); CERTIFY_GATE never runs in normal pipeline flow (A11:F-A11-011, A10:F-A10-019, A11:F-A11-034) | "A 13th step (certify) has a builder function `build_certify_step()` at executor.py:1259, but is never called — confirmed dead code" (A11:F-A11-011); v3.66 `_build_steps()` ends at remediate; no `step.id == "certify"` dispatch (A10:F-A10-019) |

### Hot-spot identification

Three steps stand out as the highest-risk hot spots when failure-count, remediation-count, and current-codebase-risk verdict are weighted together:

**1. spec-fidelity (18 failures, HIGH risk).** Highest single failure count in the table and the highest-frequency *recurring* halt across the v2.x → v3.x arc. The hot-spot character is structural rather than incidental: the gate's `high_severity_count == 0` predicate has no allowlist for architecture-superior-to-spec deviations (A7:F-A7-05, F-A7-07), the LLM-driven classification is empirically non-deterministic (5 runs / 4 distinct counts in A4:F-A4-005), and the canonical multi-release anti-pattern of "harden orchestration around the broken comparator" (A12:F-A12-03) means each new release ships a *new* failure shape (DeviationRegistry, TurnLedger, monotonic-progress, regression detection, S1 parser-sanitization, S2 route_findings, S5 NFR-severity demotion) without ever fixing the deterministic primitive (`phantom_ids = roadmap_ids - spec_ids` asymmetric set difference). The TUIBBS v1-MVP D-family canonicalization (A12:F-A12-01) is the first comparator-side fix; analogous asymmetries in function-signature, param-type, and dispatch-family comparators have not been audited.

**2. anti-instinct (14 failures, HIGH risk).** The single highest-frequency *terminal* halt across the entire E2E run corpus: every TDD/PRD-enriched pipeline halted here, none reached spec-fidelity (A11:F-A11-001). The hot-spot driver is encoded in the v3.1 unified spec as a *design contract* ("zero LLM calls is the defining property") not as drift — adversarial variants offering relational context (V3 coherence-graph, V5 mechanism taxonomy) were merge-rejected on latency/cost grounds (A2b:F-A2b-006). Three independent failure modes compound: (a) pure word-boundary regex over-matching section headings like "Testing Strategy" / "Migration Strategy" (A11:F-A11-002); (b) `\bhardcoded\b` flagging descriptive config values like `bcryptjs cost factor (12)` (A11:F-A11-003); (c) fingerprint coverage regression when PRD enrichment substitutes business synonyms (AUTH_SERVICE_ENABLED, RBAC, CSRF) for technical identifiers (A11:F-A11-001). Hard-zero AND-composition of three counters with no `--allow-anti-instinct-warnings` escape valve means any one false positive halts the entire downstream pipeline.

**3. merge (12 failures, HIGH risk).** Highest concentration of *silent* failure modes — gates that pass while genuinely-broken state ships downstream. `_cross_refs_resolve()` returns True unconditionally with a `# Don't fail on this — it's too fragile for now` comment shipped to production (A9:F-A9-005, A11:F-A11-031). Adversarial findings drop at a documented ~10–15% rate with no completeness check (A9:F-A9-011, cited consistently across v2.07/v2.13/v2.20 retrospectives). FR/NFR/SC identifiers are invented for tabular formatting convenience without traceability tables (A7:F-A7-15, recurrent across v2.23/v2.24.1/v3.2). The merge prompt was extended with TDD/PRD blocks but the ID-preservation constraint that `build_generate_prompt` carries was not propagated (A11:F-A11-008). The pattern is the same shape as the spec-fidelity hot spot: protective machinery added around a primitive that is itself broken or under-specified, so each new release surfaces a new manifestation.

**Cross-hot-spot dependency note.** spec-fidelity + anti-instinct + merge collectively cover 44 of 159 failures (28%) and 25 of 61 remediations (41%); they sit at consecutive points in the dependency chain (merge → anti-instinct → spec-fidelity), so a failure at any one cascades. The structural pattern across all three is identical: deterministic gate logic operating on LLM-generated text, with no allowlist/escape valve when the deterministic logic disagrees with substantively-correct content. The remaining HIGH-risk verdicts (extract, debate, deviation-analysis, certify) are second-tier hot spots — extract and debate because the architectures (byte-0 parser, diff-only analysis) embed the same brittleness pattern at upstream stages, deviation-analysis because of the annotated-but-unfixed field-name mismatch and placeholder-classifier history, and certify because the entire step is dead code with no pipeline run currently exercising it (A11:F-A11-011, A10:F-A10-019).
## Architectural-flaw Thesis

Across 14 partitions and 262 findings, the pipeline's failures cluster into five deep structural flaws — not bugs or oversights, but design properties baked into the architecture's primitives. Each is evidenced by independent occurrences across multiple unrelated releases, demonstrating that the same shape recurs as a *consequence of the design*, not as residual defect work.

### Flaw 1: Artifact-Centric Gate Model With No Code-Reaching Terminal Link

**Flaw statement:** Every pipeline gate consumes a markdown artifact and validates its frontmatter / structure / count fields; no gate inspects whether the code those artifacts claim to describe is actually reachable from production entry points, so "written but not wired" is the default outcome rather than the exception.

**Evidence chain:** The v3.1 anti-instinct gate built TurnLedger, ShadowGateMetrics, DeferredRemediationLog, and four detection modules complete with tests — but `execute_sprint()` never called `execute_phase_tasks()`, leaving every object dead in production while validation reported CLEAN with 0 findings (A2b:F-A2b-003, A2b:F-A2b-004). The v3.2 fidelity refactor wrote `_resolve_wiring_mode()` and `run_post_phase_wiring_hook()` but never wired the call sites; spec-fidelity passed because it compared roadmap-vs-spec, not implementation-vs-spec (A3:F-A3-12, A3:F-A3-13, A3:F-A3-15). The cli-portify executor raced through 12 steps in milliseconds emitting `outcome: SUCCESS` against eight orphaned step modules because no gate verified `STEP_DISPATCH` resolved to live callables (A3:F-A3-17, A7:F-A7-06). The v3.66 certify step has a complete `build_certify_step()` plus `generate_certification_report()` formatter but no orchestration call — pipelines silently end at remediate (A10:F-A10-019, A11:F-A11-011). The wiring-verification gate itself scanned `.dev/releases/complete/` (markdown artifacts) instead of `src/`, emitting 0 findings against 10 markdown files in v2.24.5, unified-audit-gating-v1.2.1, v3.0, and v3.1 before the `files_analyzed > 0` guard was finally added (A2b:F-A2b-002, A4:F-A4-004, A4:F-A4-021, A6:F-A6-010).

**Classification:** INHERENT — the gate signature `(content: str) -> bool` or `(file: Path, criteria) -> tuple[bool, str|None]` cannot be extended to AST-level call-graph verification without rewriting every gate's contract and the executor's dispatch model.

**Cost of leaving unaddressed:** Every release re-pays the manual cost of post-hoc gap analysis (the v3.1 + v3.2 retrospectives each consumed full QA reflection cycles to surface ~3-5 CRITICAL bugs that 8 validator agents had marked CLEAN); estimated 30-50% of remediation token spend goes to bugs that an integration-smoke gate would have caught pre-merge.

**First-principles cause:** The fidelity loop terminates at roadmap approval because the pipeline was conceived as a *document-generation* pipeline (spec→roadmap→tasklist) where every step's output is markdown. Code-artifact verification was never in the abstraction — Tasklist→Code is the missing Link 3 of the fidelity chain, and there is no place in the gate model to insert it.

### Flaw 2: Generator/Validator Asymmetry With No Generator-Side Constraints

**Flaw statement:** Validators are deterministic Python (parsers, schema checks, counts); generators are non-deterministic LLM subprocesses with no structural rule pinning ID preservation, phase-count stability, or contract-preservation across the architect→debate→merge chain, so the pipeline grows a new validator for every drift class while the generator's open-ended failure surface keeps expanding.

**Evidence chain:** Roadmap generators fabricate FR-NNN/NFR-NNN/SC-NNN identifiers the spec never defines, recurring across v2.22 (DEV-010 invented FR-001..FR-032 and NFR-001..NFR-014, A1b:F-A1b-004), v3.2 (Goal-1a/NFR-001 invention, A3:F-A3-16), v2.23 and v2.24.1 (renumbered IDs without traceability tables, A7:F-A7-15), v2.20 cleanup-audit and cross-framework-deep-analysis (DEV-002 OQ-001..OQ-008 invented, A10:F-A10-022), and the cliEval deviation analyzer producing phantom IDs `D-1, D12, D3, D5, D6` against a roadmap defining only `D-5` and `D-8` (A6:F-A6-008). Architects re-decompose spec phases for execution-coherence reasons (v2.24 18-module restructure superior-to-spec, A7:F-A7-05; v2.24.1 7→5 phase consolidation dropping `config.py`, A7:F-A7-07; v3.66 Phase 3 compound tasks + Phase 5 bundling, A10:F-A10-028). Context-window pressure produces silent Phase 7 ID drift (D-0042..D-0050 instead of D-0035..D-0043 in v2.22, A1b:F-A1b-005). Each failure class triggers a new downstream validator (spec-fidelity, deviation-analysis, structural_checkers, convergence engine, fidelity_checker, traceability matrix) but no constraint is ever added to the generator prompt itself.

**Classification:** INHERENT — generator-side constraints would require structured-output enforcement (tool-write mode + templates with required-field schemas) at every LLM step; the current `_embed_inputs()` + raw stdout capture cannot enforce structural invariants without architectural change to `ClaudeProcess`.

**Cost of leaving unaddressed:** Pipeline step count grows monotonically (v4=9 steps → v2.22=11 → v5=13 → current=14) because every new failure class adds a step rather than constraining the generator; remediation cost scales linearly with step count.

**First-principles cause:** The pipeline architecture treats the LLM as a black-box producer and inserts Python validators as the only line of defense. Validators can only catch failure classes someone has named after observing them; the generator's failure surface is open-ended by construction.

### Flaw 3: Cross-Step State Lives in Markdown Frontmatter, Coupling Every Gate to LLM-Reported Counts

**Flaw statement:** Pipeline state, fidelity counts, severity classifications, and gate-pass signals all flow through markdown frontmatter that the LLM both produces and self-reports, so every gate that blocks on `high_severity_count == 0` or `convergence_score >= 0.8` is trusting the same agent it is meant to police.

**Evidence chain:** Spec-fidelity gate ran 5 times against identical inputs in v3.0 and produced 4 distinct deviation counts; Run 4 silently regenerated the roadmap from scratch, losing all Runs 1-3 edits (A4:F-A4-005). The 5-vote statistical consensus harness (A4:F-A4-016) was bolted on to compensate at 5x the gate cost. Convergence thresholds are advisory floats: `_convergence_score_valid()` checks only `[0.0, 1.0]` parseability, so v2.13 and v2.20 both shipped at 0.72 below the documented 0.85 high-confidence threshold (A4:F-A4-008, A9:F-A9-007), and skill-side prose thresholds (`≥0.6 PASS`) have no CLI gate enforcement (A9:F-A9-004). Severity classifications are LLM-self-reported: cleanup-audit-v2 shipped with `high_severity_count: 0` despite DEV-004/DEV-005 being cross-cutting infrastructure deferred to Phase 4 that materially blocked Phase 1-3 execution (A9:F-A9-009); SC-NNN namespace collision was downgraded to MEDIUM and shipped (A4:F-A4-020); v3.66 emitted 14 UNCLASSIFIED findings with hex stable_ids instead of gate-required `DEV-N` because `_run_deviation_analysis` populated records without running classification (A10:F-A10-018). The `ambiguous_count` vs `ambiguous_deviations` frontmatter-field-name mismatch in DEVIATION_ANALYSIS_GATE means the semantic check effectively cannot fire (A11:F-A11-009). Two frontmatter parsers (`_parse_frontmatter` byte-0-only and `_check_frontmatter` re.MULTILINE) disagree about valid input (A11:F-A11-010).

**Classification:** INHERENT — the state-in-markdown architecture is the substrate of every pipeline handoff; replacing it requires a typed state model (dataclass + sidecar JSON) at every step.

**Cost of leaving unaddressed:** LLM gate non-determinism makes single-pass releases unreproducible; adversarial mode (the only structural counter) is opt-in and only catches half the false-negative surface (A4:F-A4-009 forward-trace pass coexists with backward-trace fail).

**First-principles cause:** Markdown was chosen as the universal interchange format because it is human-readable and LLM-emittable. Type safety became the parser's job, and the parser is itself an LLM-instructed prompt.

### Flaw 4: Retry Without Input Mutation + Silent-Skip As Default Failure Mode

**Flaw statement:** When a gate fails, the executor re-runs the same prompt against the same unchanged inputs (futile by construction), and when an upstream signal is ambiguous the system defaults to silent skip rather than loud rejection — combining to make degradation indistinguishable from success.

**Evidence chain:** v2.24-cli-portify halted at spec-fidelity after exhausting its 2-attempt retry budget producing identical output because retry re-runs the same prompt against unchanged `roadmap.md` (A1b:F-A1b-006); this single incident drove the entire v5 pipeline redesign with three new steps. v2.20 merge step's duplicate-headings gate failed then "PASSED on resume" not by deterministic regeneration but by LLM non-determinism on the same prompt (A11:F-A11-017). The cross-framework Phase 2 sub-agent emitted 870KB single-Write looking like a stall to the event-counting detector and exited with no remediation (A10:F-A10-023). Silent-skip is institutionalized as design intent: `/sc:brainstorm` smart-detection explicitly says "If uncertain, do NOT trigger. False negatives preferred over token waste" (A9:F-A9-002); `_cross_refs_resolve()` shipped as `return True` with a "too fragile for now" comment that stayed live for releases (A9:F-A9-005, A11:F-A11-031); `fidelity_checker.py:287-303` fails open with `found=True` for any FR whose names cannot be extracted (A4:F-A4-012); the validate gate emits BLOCKING findings while parent pipeline returns exit 0 by design (A4:F-A4-002, A4:F-A4-022); MEDIUM-severity is non-blocking even when it encodes cross-cutting infrastructure deferred (A9:F-A9-009); cliEval `.roadmap-state.json` shows `fidelity_status: pass` coexisting with `validation.status: fail` after manual triage closed the gate (A6:F-A6-013); spec-format auto-detection falls back to roadmap-only generation with a warning that downstream consumers never see (A2a:F-A2a-006).

**Classification:** PATCH-FIXABLE for retry-with-mutation (v2.26 v5 pipeline added deviation-class injection on retry); INHERENT for silent-skip discipline because it is encoded across dozens of explicit policy decisions that would require architectural inversion to "loud rejection by default."

**Cost of leaving unaddressed:** Operators cannot tell from `.roadmap-state.json` or exit codes whether a release actually shipped vs limped through with manual triage; every release re-pays the cost of distinguishing "real PASS" from "silent skip" via human review.

**First-principles cause:** Retry was modeled on transient LLM failures (rate limits, timeouts) not on deterministic-input failures; silent-skip emerged as the token-economy optimization when "every gate halts the pipeline" felt operationally worse than "gates produce advisory reports."

### Flaw 5: No Cross-Skill / Cross-Step Contract Schema Or Source-Of-Truth Authority

**Flaw statement:** Producers and consumers of artifacts evolve independently — there is no schema validation between skill outputs, no enforcement that consumers must read all producer fields, no central registry of identifiers, gate names, or threshold constants, so drift between every coupled pair (CLI↔skill, generator↔validator, spec↔roadmap, roadmap↔code) recurs at every release boundary.

**Evidence chain:** Skill/command CLI drift produced 17 flag mismatches in v2.20-WorkflowEvolution → roadmap-cli-skill-converge (6 inference-only flags in `roadmap.md`, 11 CLI-only flags missing from docs, plus 5 waves documented vs 14 CLI steps shipped — A9:F-A9-003, A9:F-A9-004). Schema drift in extraction collapsed the 17+ field protocol-side contract to a 3-field CLI prompt that the gate adapted to (A2a:F-A2a-002, A9:F-A9-008). Cross-skill contract violations: release-split's Mode B consumer enumerated 4 of 9 fields sc:adversarial returned, dropping `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method` with no schema validation (A10:F-A10-004); convergence thresholds drifted across sibling skills (sc:release-split 0.7/0.5 vs sc:roadmap 0.6/0.5 — A10:F-A10-003); `--generate split-proposal` was invented as an unrecognized adversarial artifact type (A10:F-A10-002). Asymmetric extractor/comparator pairs: spec_parser leniently matched `D1` and `D01` while structural_checkers strict-set-differenced producing 54 phantom_id HIGHs (A12:F-A12-01), and the same pattern recurred in PR #86 mechanism_signature missing canonicalization invariants (A12:F-A12-06). v3.1 anti-instinct's variant V3 (coherence graph) and V5 (mechanism taxonomy) were merge-rejected on cost grounds, leaving the gate with no relational context — producing the predictable false positives on "Testing Strategy" headings (A2b:F-A2b-006, A11:F-A11-002). Eval workspaces drifted from SKILL.md contracts: sc-reflect's 14 promotion fixtures invented an 8-field schema contradicting the 11-field §14.5.6 contract (A12:F-A12-09); skill-creator wrote 100 eval artifacts to `.claude/skills/` against CLAUDE.md project rules because no PreToolUse hook existed (A10:F-A10-005).

**Classification:** PATCH-FIXABLE per coupling — but the meta-flaw (absence of a contract-enforcement layer) is INHERENT because dozens of coupling points exist, each currently coordinated only via prose and `make verify-sync` (which is opt-in and produced misleading error messages — A10:F-A10-006, A10:F-A10-007).

**Cost of leaving unaddressed:** Every release with non-trivial scope manually triages contract drift; the convergence release closed *one round* of CLI↔skill drift but the structural condition recreates drift the next time CLI flags evolve.

**First-principles cause:** Skills, commands, agents, gates, and CLI commands were authored as parallel surfaces with overlapping but independent vocabulary. No SoT layer was ever designated for cross-cutting concerns (identifiers, thresholds, gate names, return contracts), and drift detection was deferred to humans reading prose.

---

**Verdict: REWRITE**

The decision rule resolves to REWRITE: four of five flaws are classified INHERENT (Flaws 1, 2, 3, 5 in whole; Flaw 4's silent-skip half), and three of those four scope to *cross-cutting state* — the artifact-centric gate model (Flaw 1) is the substrate every gate inherits, markdown-frontmatter state (Flaw 3) flows through every step, and the missing contract-schema layer (Flaw 5) couples every producer/consumer pair. These are not subsystem boundaries one could replace independently — they are the pipeline's interchange substrate. Patches will continue addressing each new failure shape one validator at a time (the documented v4→v2.22→v5→current trajectory: 9→11→13→14 steps), but the generator/validator asymmetry guarantees new shapes will arrive faster than validators can be authored. A REWRITE should preserve the adversarial-debate mechanism (Pattern P3 in A8 — it actually works) and the deterministic structural-checker layer (v3.05), but invert the substrate: typed cross-step state (sidecar JSON + dataclass), tool-write structured-output enforcement at every LLM step, a code-reaching terminal fidelity link (Tasklist→AST), and a central contract registry with bidirectional drift detection in CI. The v2.13 lesson — don't extract until semantic overlap forces the abstraction — applies inversely here: the recurring failure across every retrospective forces the abstraction now.
## Bibliography

### Partition reports (14)

- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A1a-roadmap-core-older.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A1b-roadmap-core-newer.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A2a-reliability-precursors.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A2b-anti-instinct-gate.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A3-architecture-refactor.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A4-validation-gates.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A5-halt-preflight.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A6-tasklist-sprint.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A7-cli-portify.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A8-adversarial-specpanel.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A9-brainstorm-convergence.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A10-release-split-misc.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A11-e2e-research-tasks.md`
- `.dev/troubleshoot/roadmap-pipeline-retrospective/wave1-partition-reports/A12-fidelity-reflect-cliEval.md`

### Source artifacts cited

Paths below are grouped by parent release directory (under `.dev/releases/complete/`) and by other top-level locations. Within a group, artifacts are listed alphabetically. Where a partition report cited only a bare filename, the canonical containing directory has been inferred from the partition's scope and is grouped accordingly.

#### `.dev/releases/complete/v1.4-roadmap-gen/`

- `v1.4-roadmap-gen/FILE-STATUS-ANALYSIS.md`
- `v1.4-roadmap-gen/SPEC-IMPROVEMENT-PROPOSALS.md`
- `v1.4-roadmap-gen/archive/ibopencode-source/` (directory)
- `v1.4-roadmap-gen/claude-code-proposals-framework.md`
- `v1.4-roadmap-gen/claude-code-proposals-opencode.md`
- `v1.4-roadmap-gen/workflow-superclaude-refactoring.md`

#### `.dev/releases/complete/v2.0-roadmap-v2/`

- `v2.0-roadmap-v2/COMMIT-LOG.md`
- `v2.0-roadmap-v2/SC-ROADMAP-V2-SPEC.md`
- `v2.0-roadmap-v2/spec-panel-roadmap-v2-review.md`

#### `.dev/releases/complete/v2.01-Architecture-Refactor/`

- `v2.01-Architecture-Refactor/spec-planning/extract-root-cause-analysis.md`

#### `.dev/releases/complete/v2.02-Roadmap-v3/`

- `v2.02-Roadmap-v3/execution-log.md`
- `v2.02-Roadmap-v3/fix-tasklist.md`
- `v2.02-Roadmap-v3/prereq-validation.md`
- `v2.02-Roadmap-v3/probe-results.md`

#### `.dev/releases/complete/v2.05-sprint-cli-specification/`

- `v2.05-sprint-cli-specification/tasklist/tasklist.md`

#### `.dev/releases/complete/v2.07-tasklist-v1/`

- `v2.07-tasklist-v1/adversarial/strategy1-stage-gated-contract/adversarial-final-report.md`
- `v2.07-tasklist-v1/final-unified-refactor-plan.md`
- `v2.07-tasklist-v1/sprint-process-improvement-v2.07-retrospective.md`
- `v2.07-tasklist-v1/tasklist-quality-comparison-v2.08.md`
- `v2.07-tasklist-v1/tasklist-upgrade-review.md`

#### `.dev/releases/complete/v2.09-adversarial-v2/`

- `v2.09-adversarial-v2/adversarial/file-passing-debate/debate-transcript.md`

#### `.dev/releases/complete/v2.10-spec-panel-v2/`

- `v2.10-spec-panel-v2/process-improvement/cross-cutting-analysis.md`

#### `.dev/releases/complete/v.2.11-roadmap-v4/`

- `v.2.11-roadmap-v4/brainstorm-roadmap.md`

#### `.dev/releases/complete/v2.13-CLIRunner-PipelineUnification/`

- `v2.13-CLIRunner-PipelineUnification/CLIRunner-benchmark/adversarial-output/merged-analysis.md`
- `v2.13-CLIRunner-PipelineUnification/merged-pipeline-decision.md`

#### `.dev/releases/complete/v2.15-cli-portify/`

- `v2.15-cli-portify/adversarial/invariant-probe.md`
- `v2.15-cli-portify/adversarial/refactor-plan.md`
- `v2.15-cli-portify/session-findings-merged.md`

#### `.dev/releases/complete/v.2.17-roadmap-reliability/`

- `v.2.17-roadmap-reliability/roadmap-extract-failure-2.md`
- `v.2.17-roadmap-reliability/roadmap-extract-failure-context.md`
- `v.2.17-roadmap-reliability/spec-roadmap-pipeline-reliability.md`

#### `.dev/releases/complete/v2.18-cli-portify-v2/`

- `v2.18-cli-portify-v2/base-selection.md`
- `v2.18-cli-portify-v2/execution-log.md`
- `v2.18-cli-portify-v2/PlanningArtifacts/cli-portify-executor-noop-forensic-report.md`
- `v2.18-cli-portify-v2/roadmap.md`

#### `.dev/releases/complete/v2.19-roadmap-validate/`

- `v2.19-roadmap-validate/debate-transcript.md`
- `v2.19-roadmap-validate/spec-roadmap-validate.md`

#### `.dev/releases/complete/v2.20-WorkflowEvolution/`

- `v2.20-WorkflowEvolution/adversarial-forensic-validation/forensic-foundation-validated.md`
- `v2.20-WorkflowEvolution/adversarial/refactor-plan.md`
- `v2.20-WorkflowEvolution/Archive/forensic-diagnostic-report.md`
- `v2.20-WorkflowEvolution/Archive/spec-fidelity-gap-analysis-merged.md`
- `v2.20-WorkflowEvolution/Archive/workflow-failure-theories.md`
- `v2.20-WorkflowEvolution/diff-analysis.md`
- `v2.20-WorkflowEvolution/extraction.md`
- `v2.20-WorkflowEvolution/roadmap.md`

#### `.dev/releases/complete/v2.21-sc-brainstorm-auggie/`

- `v2.21-sc-brainstorm-auggie/design-spec.md`
- `v2.21-sc-brainstorm-auggie/tasklist.md`

#### `.dev/releases/complete/v2.22-RoadmapRemediate/`

- `v2.22-RoadmapRemediate/spec-fidelity.md`
- `v2.22-RoadmapRemediate/spec-roadmap-remediate.md`

#### `.dev/releases/complete/v2.23-cli-portify-v3/` (and `v2.23/`)

- `v2.23-cli-portify-v3/reflect-merged.md`
- `v2.23-cli-portify-v3/spec-cli-portify-workflow-evolution.md`
- `v2.23-cli-portify-v3/spec-fidelity.md`
- `v2.23/spec-fidelity.md`

#### `.dev/releases/complete/v2.24-cli-portify-cli-v4/` (and `v2.24/`)

- `v2.24-cli-portify-cli-v4/dev-001-accepted-deviation.md`
- `v2.24-cli-portify-cli-v4/panel-report.md`
- `v2.24-cli-portify-cli-v4/spec-fidelity.md`
- `v2.24-cli-portify-cli-v4/troubleshoot-agent1-artifacts.md`
- `v2.24/dev-001-accepted-deviation.md`

#### `.dev/releases/complete/v2.24.1-cli-portify-cli-v5/` (and `v2.24.1/`)

- `v2.24.1-cli-portify-cli-v5/brainstorm-approach-a.md`
- `v2.24.1-cli-portify-cli-v5/brainstorm-approach-b.md`
- `v2.24.1-cli-portify-cli-v5/context-overview.md`
- `v2.24.1-cli-portify-cli-v5/debate-transcript.md`
- `v2.24.1-cli-portify-cli-v5/scoring-matrix.md`
- `v2.24.1-cli-portify-cli-v5/spec-fidelity.md`
- `v2.24.1-cli-portify-cli-v5/wiring-verification.md`
- `v2.24.1-cli-portify-cli-v5/workflow_gate-remediation-phase0-decisions.md`
- `v2.24.1-cli-portify-cli-v5/workflow_portify-roadmap-corrections.md`
- `v2.24.1/spec-fidelity.md`

#### `.dev/releases/complete/v2.24.2-Accept-Spec-Change/`

- `v2.24.2-Accept-Spec-Change/design-accept-spec-change.md`
- `v2.24.2-Accept-Spec-Change/release-spec-accept-spec-change.md`
- `v2.24.2-Accept-Spec-Change/tasklist-index.md`

#### `.dev/releases/complete/v2.24.5-SpecFidelity/`

- `v2.24.5-SpecFidelity/spec-fidelity.md`
- `v2.24.5-SpecFidelity/validation/PatchChecklist.md`
- `v2.24.5-SpecFidelity/wiring-verification.md`

#### `.dev/releases/complete/v2.25-cli-portify-cli/`

- `v2.25-cli-portify-cli/execution-log.md`
- `v2.25-cli-portify-cli/oq-resolutions.md`
- `v2.25-cli-portify-cli/results/phase-3-diagnostic.md`
- `v2.25-cli-portify-cli/results/phase-3-result.md`
- `v2.25-cli-portify-cli/resume-tasklist.md`
- `v2.25-cli-portify-cli/roadmap.md`

#### `.dev/releases/complete/v2.25.5-PreFlightExecutor/`

- `v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/fix-plan-high.md`
- `v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/spec-fidelity.md`
- `v2.25.5-PreFlightExecutor/sprint-preflight-executor-spec.md`

#### `.dev/releases/complete/v2.25.7-Phase8HaltFix/`

- `v2.25.7-Phase8HaltFix/phase8-partial-task-remediation-tasklist.md`
- `v2.25.7-Phase8HaltFix/Phase8-SprintContext-cross-spec-overlap-analysis-adversarial/cross-spec-overlap-validation.md`
- `v2.25.7-Phase8HaltFix/v2.25.1-arg-too-long-spec.md`
- `v2.25.7-Phase8HaltFix/v2.25.7-phase8-sprint-context-resilience-prd.md`

#### `.dev/releases/complete/v2.26-roadmap-v5/`

- `v2.26-roadmap-v5/adversarial-accept-spec-change-placement.md`
- `v2.26-roadmap-v5/roadmap.md`
- `v2.26-roadmap-v5/v2.25-spec-merged.md`

#### `.dev/releases/complete/v3.0_unified-audit-gating/`

- `v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md`
- `v3.0_unified-audit-gating/fidelity-consensus.md`
- `v3.0_unified-audit-gating/fidelity-remediation-log.md`
- `v3.0_unified-audit-gating/release-split/fidelity-audit.md`
- `v3.0_unified-audit-gating/wiring-verification.md`

#### `.dev/releases/complete/v3.05_DeterministicFidelityGates/`

- `v3.05_DeterministicFidelityGates/spec-fidelity.md`
- `v3.05_DeterministicFidelityGates/v3.05/execution-qa-reflection.md`
- `v3.05_DeterministicFidelityGates/v3.05/pipeline-weakness-analysis.md`
- `v3.05_DeterministicFidelityGates/v3.05/roadmap-gap-analysis-merged.md`
- `v3.05_DeterministicFidelityGates/validate/validation-report.md`
- `v3.05_DeterministicFidelityGates/wiring-verification.md`

#### `.dev/releases/complete/v3.1_Anti-instincts__/`

- `v3.1/execution-qa-reflection.md`
- `v3.1/gap-remediation-reflection.md`
- `v3.1/pipeline-weakness-analysis.md`
- `v3.1/roadmap-gap-analysis-merged.md`
- (and `v3.1`/`v3.2` reflection / pipeline-weakness families cited in A2b)

#### `.dev/releases/complete/v3.2_fidelity-refactor___/`

- `v3.2_fidelity-refactor___/debate-transcript.md`
- `v3.2/execution-qa-reflection.md`
- `v3.2/pipeline-weakness-analysis.md`
- `v3.2/roadmap-gap-analysis-merged.md`

#### `.dev/releases/complete/v3.65-prd-refactor/`

- `v3.65-prd-refactor/anti-instinct-audit.md`
- `v3.65-prd-refactor/spec-drift-analysis-b942d50.md`
- `v3.65-prd-refactor/tfep-run-1/rca-verdict.md`
- `v3.65-prd-refactor/tfep-run-1/tfep-incident-report.md`
- `v3.65-prd-refactor/tfep-run-2/rca-verdict.md`
- `v3.65-prd-refactor/workflow-gate-fix.md`

#### `.dev/releases/complete/v3.66-tdd-skill-refactor-v2/`

- `v3.66-tdd-skill-refactor-v2/spec-deviations.md`
- `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-1-deviation-analysis.md`
- `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-2-certify-wiring.md`
- `v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/phase-3-hardening-verification.md`
- `v3.66-tdd-skill-refactor-v2/tasklist-spec-fidelity-bugfix.md`
- `v3.66-tdd-skill-refactor-v2/validate/validation-report.md`

#### `.dev/releases/complete/v3.7-turnledger-integration/`

- `v3.7-turnledger-integration/v3.3-wiring-verification-final.md`
- `v3.7-turnledger-integration/v3.7-TurnLedger-Validation/remediation-tasklist.md`
- `v3.7-turnledger-integration/validation-comparison/merged-consolidated-report.md`

#### `.dev/releases/complete/v.1.06-CleanupAudit/`

- `v.1.06-CleanupAudit/research/refactor-plan.md`
- `v.1.06-CleanupAudit/sc-cleanup-audit-roadmap.md`

#### `.dev/releases/complete/unified-audit-gating-v1.2.1/` and `unified-audit-gating-v2/`

- `unified-audit-gating-v1.2.1/wiring-verification.md`
- `unified-audit-gating-v2/spec-fidelity.md`

#### `.dev/releases/complete/cleanup-audit-v2-UNIFIED-SPEC/`

- `cleanup-audit-v2-UNIFIED-SPEC/adversarial/debate-transcript.md`
- `cleanup-audit-v2-UNIFIED-SPEC/adversarial/diff-analysis.md`
- `cleanup-audit-v2-UNIFIED-SPEC/adversarial/refactor-plan.md`
- `cleanup-audit-v2-UNIFIED-SPEC.md`
- `cleanup-audit-v2-UNIFIED-SPEC/extraction.md`
- `cleanup-audit-v2-UNIFIED-SPEC/spec-fidelity.md`
- `cleanup-audit-v2-UNIFIED-SPEC/wiring-verification.md`

#### `.dev/releases/complete/cliEval/`

- `cliEval/anti-instinct-audit.md`
- `cliEval/base-selection.md`
- `cliEval/deviation-triage.md`
- `cliEval/diff-analysis.md`
- `cliEval/execution-log.jsonl`
- `cliEval/execution-log.md`
- `cliEval/remediate-roadmap.md`
- `cliEval/remediation-tasklist.md`
- `cliEval/.roadmap-state.json`
- `cliEval/spec-deviations.md`
- `cliEval/spec-fidelity.md`
- `cliEval/tasklist-index.md`
- `cliEval/wiring-verification.md`

#### `.dev/releases/complete/cross-framework-deep-analysis/`

- `cross-framework-deep-analysis/results/phase-2-diagnostic.md`
- `cross-framework-deep-analysis/spec-fidelity.md`

#### `.dev/releases/complete/release-split/` and `release-split-workspace-rca/`

- `release-split/release-split-agents-refactor-plan.md`
- `release-split-workspace-rca/rca-2-eval-harness.md`
- `release-split-workspace-rca/rca-3-naming-convention.md`

#### `.dev/releases/complete/roadmap-cli-skill-converge/`

- `roadmap-cli-skill-converge/checkpoints/CP-P04-END.md`
- `roadmap-cli-skill-converge/checkpoints/CP-P05-END.md`
- `roadmap-cli-skill-converge/design-decision.md`
- `roadmap-cli-skill-converge/manifest.json`
- `roadmap-cli-skill-converge/release-scope.md`
- `roadmap-cli-skill-converge/solutions.md`
- `roadmap-cli-skill-converge/verification.md`

#### `.dev/releases/complete/task-builder-merge/`

- `task-builder-merge/anti-instinct-audit.md`
- `task-builder-merge/spec-deviations.md`

#### `.dev/releases/complete/obligation-vocab-alignment/`

- `obligation-vocab-alignment/design.md`

#### `.dev/releases/complete/reflect-path-regression/`

- `reflect-path-regression/tasklist/tasklist-index.md`

#### `.dev/releases/complete/sc-reflect-rescrutiny/`

- `sc-reflect-rescrutiny-design.md`
- `sc-reflect-rescrutiny-workflow.md`

#### `.dev/releases/complete/sc-tasklist-command-spec/`

- `sc-tasklist-command-spec-v1.0.md`

#### `.dev/tasks/done/` — TASK-E2E / TASK-RF / TASK-RESEARCH bundles

- `TASK-E2E-20260327-prd-pipeline-e2e/phase-outputs/test-results/phase4-anti-instinct.md`
- `TASK-E2E-20260327-prd-pipeline-e2e/reviews/consolidated-findings.md`
- `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md`
- `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md`
- `TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-anti-instinct-4way.md`
- `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-REPORT-anti-instinct-gate-failure.md`
- `TASK-RESEARCH-20260403-anti-instinct/RESEARCH-PROMPT-anti-instinct-gate-failure.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/research/02-merged-fix-spec.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/research/03-roadmap-phases.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/research/04-post-task-verification-gates.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/research/05-restrictions-doc-context.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/research/06-invariant-probe.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/research/07-historical-context.md`
- `TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md`
- `TASK-RESEARCH-20260403-tasklist-quality/reviews/pipeline-trace-investigation.md`
- `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-PROMPT-roadmap-tasklist-architecture-overhaul.md`
- `TASK-RESEARCH-20260404-roadmap-tasklist-overhaul/RESEARCH-REPORT-roadmap-tasklist-overhaul.md`
- `TASK-RF-20260326-e2e-modified/phase-outputs/test-results/phase4-anti-instinct.md`
- `TASK-RF-20260326-e2e-modified/reviews/qa-qualitative-tdd-vs-spec.md`
- `TASK-RF-20260402-baseline-repo/phase-outputs/test-results/execution-summary.md`
- `TASK-RF-20260403-quality-comparison/phase-outputs/reports/qualitative-assessment.md`
- `TASK-RF-20260403-quality-comparison/phase-outputs/reports/quality-matrix.md`
- `TASK-RF-20260518-181333/TASK-RF-20260518-181333.md`
- `TASK-RF-20260518-cliEval-P4-wire-and-ship/TASK-RF-20260518-cliEval-P4-wire-and-ship.md`
- `TASK-RF-20260524-issue-60-ruff-debt/TASK-RF-20260524-issue-60-ruff-debt.md`
- `TASK-RF-20260525-150000/TASK-RF-20260525-150000.md`
- `TASK-RF-20260525-150000/phase-outputs/plans/phase4-fix-plan.md`
- `TASK-RF-20260525-150000/qa/qa-qualitative-review.md`
- `TASK-RF-20260526-102600/TASK-RF-20260526-102600.md`
- `TASK-RF-20260526-102600/phase-outputs/grep-audit/pr86-prA-grep-audit.md`
- `TASK-RF-20260526-102600/qa/final-qa-gate-cycle-1.md`
- `TASK-RF-20260527-043715-sc-reflect-rebuild/phase-outputs/reviews/phase7-rf-qa-qualitative-final.md`
- `TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/01-troubleshoot-report.md`

#### `.dev/` — top-level scaffolding

- `.dev/README.md`
- `.dev/eval-workspaces/` (directory)
- `.dev/research/` (directory)

#### `src/superclaude/cli/` — Python pipeline executors and helpers

- `src/superclaude/cli/main.py`
- `src/superclaude/cli/vocabulary.py`
- `src/superclaude/cli/cli_portify/steps/__init__.py`
- `src/superclaude/cli/roadmap/commands.py`
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/gates.py`
- `src/superclaude/cli/roadmap/prompts.py`
- `src/superclaude/cli/roadmap/structural_checkers.py`
- `src/superclaude/cli/tasklist/commands.py`
- `src/superclaude/cli/sprint/executor.py`
- `src/superclaude/cli/sprint/monitor.py`
- `src/superclaude/cli/sprint/process.py`

(Bare-name citations resolving into the cli tree: `adversarial_runner.py`, `audit/wiring_gate.py`, `certify_executor.py`, `certify_gates.py`, `config.py`, `contract.py`, `convergence.py`, `diagnostics.py`, `executor.py`, `fidelity_checker.py`, `finding_parser.py`, `fingerprint.py`, `gates.py`, `integration_contracts.py`, `logging_.py`, `monitor.py`, `obligation_scanner.py`, `pipeline/gates.py`, `pipeline/process.py`, `pipeline/trailing_gate.py`, `prompts.py`, `remediate_executor.py`, `remediate_parser.py`, `resume.py`, `spec_patch.py`, `spec_structural_audit.py`, `state.json`, `structural_checkers.py`, `trailing_gate.py`, `tui.py`, `validate_config.py`, `validate_executor.py`, `validate_gates.py`, `validate_prompts.py`, `vocabulary.py`, `wiring_analyzer.py`.)

#### `src/superclaude/commands/` and `src/superclaude/examples/`

- `src/superclaude/commands/brainstorm.md`
- `src/superclaude/commands/reflect.md`
- `src/superclaude/examples/prd_template.md`

#### `tests/` — pytest suite citations

- `tests/roadmap/test_cli_contract.py`
- `tests/roadmap/test_executor.py`
- `tests/roadmap/test_file_passing.py`
- `tests/roadmap/test_obligation_scanner_meta_context.py`

#### `.claude/` and `.github/` configuration

- `.claude/commands/sc/reflect.md`
- `.claude/settings.json`
- `.github/workflows/quick-check.yml`
- `.github/workflows/publish-pypi.yml`
- `.github/workflows/pull-sync-framework.yml`
- `.github/workflows/test.yml`

#### Top-level repo files

- `pyproject.toml`

#### Sub-skill / sub-command artifacts cited by short name

The following short-name artifacts appear repeatedly across partitions, typically as inputs / outputs of pipeline steps (extraction, adversarial, validate, spec-fidelity, wiring-verification, reflect, brainstorm, anti-instinct, halt-preflight). They resolve within the release directories listed above. Listed here for completeness:

- Pipeline outputs: `extraction.md`, `extraction-pipeline.md`, `extract-root-cause-analysis.md`, `roadmap.md`, `roadmap-extract-failure-2.md`, `roadmap-extract-failure-context.md`, `roadmap-pipeline-deep-trace.md`, `.roadmap-state.json`, `roadmap/executor.py`, `roadmap/gates.py`
- Adversarial / debate: `adversarial.md`, `adversarial/debate-transcript.md`, `adversarial-scoring-debate.md`, `adversarial-accept-spec-change-placement.md`, `debate-transcript.md`, `merge-log.md`, `merged-analysis.md`, `merged-spec.md`, `oq-resolutions.md`, `scoring-matrix.md`, `scoring.md`
- Validate / fidelity / wiring: `validation-report.md`, `ValidationReport.md`, `validation/validation-report.md`, `validation/ValidationReport.md`, `validate/merged-validation-report.md`, `validate/reflect-merged.md`, `validate/reflect-opus-architect.md`, `validate-roadmap.md`, `validate-tests.md`, `validation-immediate.md`, `spec-fidelity.md`, `spec-fidelity-gap-analysis-merged.md`, `spec-refactor-plan-merged.md`, `tasklist-fidelity.md`, `wiring-verification.md`, `wiring_analyzer.py`, `fidelity-consensus.md`
- Reflect / brainstorm: `reflect.md`, `reflect-merged.md`, `reflect-haiku-architect.md`, `brainstorm-approach-a.md`, `brainstorm-approach-b.md`, `brainstorm-immediate-amendments.md`, `brainstorm-reference.md`, `brainstorm-roadmap.md`, `analysis-protocol.md`
- Anti-instinct / gate: `anti-instinct-audit.md`, `anti-instincts-gate-unified.md`, `tfep-run-1/rca-verdict.md`
- Tasklist / sprint: `tasklist.md`, `tasklist-index.md`, `tasklist-insertion.md`, `tasklist-longterm-amendments.md`, `tasklist-shortterm-amendments.md`, `tasklist-spec-fidelity-bugfix.md`, `tasklist-upgrade-review.md`, `tasklist/prompts.py`, `tasklist/results/phase-3-result.md`, `tasklist/results/phase-4-result.md`, `tasklist/tasklist.md`, `resume-tasklist.md`, `remediation-tasklist.md`, `remediate-roadmap.md`, `phase-7-tasklist.md`, `phase-N-tasklist.md`, `phase8-partial-task-remediation-tasklist.md`, `phase-3-hardening-verification.md`, `gap-remediation-tasklist.md`, `epics.md`
- CLI-portify forensics: `cli-portify-executor-noop-forensic-report.md`, `PlanningArtifacts/cli-portify-executor-noop-forensic-report.md`, `portify-release-spec.md`, `workflow_portify-roadmap-corrections.md`, `workflow_gate-remediation-phase0-decisions.md`, `workflow_gate-system-remediation-4phases.md`, `workflow_sc-roadmap-refactor.md`, `workflow_spec-fidelity-fixes.md`, `workflow.md`, `workflow-meta-context-fix.md`, `workflow-failure-theories.md`, `workflow-superclaude-refactoring.md`, `spec-cli-portify-workflow-evolution.md`
- Misc reviews / QA / RCAs: `00-consolidated-findings.md`, `07-historical-context.md`, `approved-immediate.md`, `backward-compat-regression-report.md`, `baseline-failures.json`, `benchmark.json`, `branch-baseline.md`, `certification-report.md`, `cleanup-audit.md`, `context-overview.md`, `cross-cutting-analysis.md`, `design-decision.md`, `design.md`, `design-spec.md`, `dev-001-accepted-deviation.md`, `diff-analysis.md`, `eval_metadata.json`, `evals.json`, `execution-log.md`, `execution-qa-reflection.md`, `FILE-STATUS-ANALYSIS.md`, `final-unified-refactor-plan.md`, `fix-plan-high.md`, `fix-tasklist.md`, `forensic-foundation-validated.md`, `grading.json`, `handoff.json`, `-longterm.md`, `merged-pipeline-decision.md`, `panel-report.md`, `PatchChecklist.md`, `pipeline-weakness-analysis.md`, `pm.md`, `process-improvement/cross-cutting-analysis.md`, `qa-deep-dive-root-cause.md`, `qa/final-qa-gate-cycle-1.md`, `qa/qa-qualitative-review.md`, `rca-3-naming-convention.md`, `recommend.md`, `refactor-plan.md`, `release-spec.md`, `return-contract.yaml`, `review-translation.md`, `reviews/qa-deep-dive-root-cause.md`, `reviews/r-item-collapse-investigation.md`, `r-item-collapse-investigation.md`, `SKILL.md`, `solutions.md`, `spec-panel.md`, `task-unified.md`, `tdd_template.md`, `test_cli_contract.py`, `test_executor.py`, `test-strategy.md`, `tfep-run-1/rca-verdict.md`, `upgrade.md`, `phase-outputs/grep-audit/pr86-prA-grep-audit.md`, `phase-outputs/plans/phase4-fix-plan.md`, `phase-outputs/reports/change-report.md`, `phase-outputs/reports/issue-60-evidence-report.md`, `phase-outputs/reports/live-tuibbs-verification.md`, `phase-outputs/reports/phase-10-stale-branch-cleanup.md`, `phase-outputs/test-results/roadmap-suite-full.md`, `results/phase-1..5-result.md`, `results/phase-2-diagnostic.md`, `results/phase-4-result.md`, `results/phase-5-result.md`, `commands.py`, `commands/roadmap.md`, `refs/extraction-pipeline.md`, `refs/templates.md`, `sc-roadmap-protocol/refs/templates.md`, `SC-ROADMAP-V2-SPEC.md`, `spec-roadmap-pipeline-reliability.md`, `spec-roadmap-remediate.md`, `spec-roadmap-validate.md`, `sprint-preflight-executor-spec.md`, `checkpoints/CP-P04-END.md`, `CP-P04-END.md`, `CP-P05-END.md`
