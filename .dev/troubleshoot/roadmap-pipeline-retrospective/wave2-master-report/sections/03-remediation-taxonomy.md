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
