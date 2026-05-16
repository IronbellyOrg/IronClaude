<!-- Variant: opus:architect — "surgical port-of-best-features; minimize blast radius; preserve /sc:task's current public surface" -->
<!-- Generated from FINAL-REPORT.md (11 sections) -->

# RELEASE SPEC — v3.75 RigorflowMerger / task-unified-v3 (Surgical Port Variant)

**Stance.** Surgically port the small, high-confidence set of historical `/sc:task-unified` strengths into the canonical `/sc:task` command, with the smallest possible diff against the v3.7 surface. No structural redesign. Treat `/sc:task` as a stable, mostly-correct command that needs targeted reinforcement, not a re-derivation.

**Source.** FINAL-REPORT.md (11 sections, including §10 Shared Assumptions and §11 TUI Improvement Bundle).

---

## 1. Release identity & scope

### 1.1 Name and version

- **Release ID:** `v3.75-RigorflowMerger-task-unified-v3`
- **Surface affected:** `/sc:task` (canonical), `sc-task-protocol` skill, `cli/sprint/` runtime, TUI rendering subsystem.
- **Predecessor:** v3.7-task-unified-v2 (R1 + R2 split, complete).
- **Public command name:** **`/sc:task` remains the only canonical surface** (v3.7 hard constraint, non-negotiable).

### 1.2 In-scope (this release)

The release executes a **minimum-viable adoption** of the FINAL-REPORT best-of-breed candidates, prioritizing low-blast-radius, additive changes:

**Task-side (TU-series, surface-preserving):**
- **TU-001** CRITICAL FAIL conditions for STRICT-tier tasks (3 conditions, programmatically enforced).
- **TU-003** Six universal quality principles published as a named NFR section in `sc-task-protocol/SKILL.md`.
- **TU-004** Deterministic BLOCKED state at confidence <0.70 (replaces soft prompt).
- **TU-007** Mandatory completion checklist (6 conditions enumerated and enforced).

**Task-side (deferred, but documented):**
- **TU-002** Output-type discrimination (`code|analysis|documentation|opinion`) — **DEFERRED** to a follow-on release. Routing-logic change is too invasive for a surgical port; needs Q3 precedence resolved first.
- **TU-005** Classification-logic consolidation — **DEFERRED** (Q12 resolution pending).
- **TU-006** Materialize missing skill sub-files — **DEFERRED** (bundle with TU-005).

**Sprint-side (SE-series, sibling release recommended):**
- **SE-001** Fail-closed gate evaluation (S, additive).
- **SE-004** `ExecutionMode` enum (S, additive).
- **SE-005** `GateFailureSeverity` enum (S, additive).
- **SE-002, SE-003** Per-task UID + sub-phase resume — **packaged together** as one shippable unit (M each, both touch prompt construction). Risk: regresses Wave-4 checkpoint heading parser (§9.7) if not tested. **Recommendation:** ship as part of this release only if the +3 Wave-4 parser tests pass; otherwise defer paired.
- **SE-006** Auto-diagnostic threshold — **DEFERRED**.

**TUI bundle (P-series, FINAL-REPORT §11):**
- Top-5 (P-05, P-02, P-03, P-07, P-01) ship as documented. Ship order: P-05 → P-02 → P-03+P-07 (combined PR) → P-01.

### 1.3 Out-of-scope (non-goals)

- **NG-1.** Reintroduce `/sc:task-unified` as a live command. **Hard constraint** from v3.7.
- **NG-2.** Resurrect `task-unified.md` or `sc-task-unified-protocol/` directories.
- **NG-3.** Replace IC's keyword-based tier classifier with semantic NLP.
- **NG-4.** Adopt LW's bash-orchestrator / Python-from-bash / multi-backup patterns.
- **NG-5.** Touch the lingering carry-overs (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel, `--caller task-unified`) — surgical variant **explicitly preserves** these until a dedicated cleanup release audits telemetry consumers (Q1, Q2, A-005 unresolved).
- **NG-6.** TypeScript plugin work (v5.0 scope).
- **NG-7 (surgical-specific).** Output-type axis (TU-002), classification-logic consolidation (TU-005), skill sub-file materialization (TU-006), auto-diagnostic threshold (SE-006). All deferred to dedicated follow-ons.

### 1.4 Release-split recommendation

Per §9.3 (Q8 commitment), this release **should be split** at the natural seam between task-surface (TU-series) and sprint-runtime (SE-series + TUI). The surgical variant **adopts** the split recommendation:

- **R1 (task-surface):** TU-001, TU-003, TU-004, TU-007.
- **R2 (sprint + TUI):** SE-001, SE-002+SE-003 (paired), SE-004, SE-005 + TUI top-5.

R2 depends on R1 only insofar as TU-001's CRITICAL FAIL semantics may be referenced by SE-001's fail-closed gate; otherwise sibling. R1 can ship independently and is the lower-blast-radius candidate.

---

## 2. Surface contract (what stays, what changes, what is added)

### 2.1 Stays (no change)

The full public surface of `/sc:task` as documented in FINAL-REPORT §4 is preserved verbatim:

- Command path: `src/superclaude/commands/task.md` + `.claude/commands/sc/task.md` (synced).
- Metadata: `name: task`, `category: special`, `complexity: advanced`, `version: "2.0.0"` (bumped to `"2.1.0"` by this release).
- All 8 flags: `--strategy, --compliance, --verify, --skip-compliance, --force-strict, --parallel, --delegate, --no-escalation`.
- Strategy axis: `systematic, agile, enterprise, auto`.
- Compliance tier axis: `strict, standard, light, exempt, auto`.
- Verification axis: `critical, standard, skip, auto`.
- Five-step decision tree at `core/ORCHESTRATOR.md:151-213`.
- Critical-path overrides (`auth/, security/, crypto/, models/, migrations/`) and trivial-path overrides (`*.md, docs/, *test*.py`).
- All four example invocations at `task.md:106-148`.
- The lingering `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header sentinel **preserved verbatim** (DEFER decision per Q1).
- `--caller task-unified` forensic invocation string **preserved verbatim** (DEFER per Q2).

### 2.2 Changes (modified behavior, same surface)

- **TU-004 (BLOCKED state).** `task.md:91` low-confidence rule replaced. Today: "prompt user with `--compliance [tier]` override hint." New: **deterministic BLOCKED state**. Behavior:
  - When `confidence < 0.70`: emit classification header with `TIER: BLOCKED`, `CONFIDENCE: <computed>`, `KEYWORDS: <split-keywords>`, `RATIONALE: split between <tier-A> and <tier-B>`, then **halt** execution.
  - User must re-invoke with explicit `--compliance <tier> --reason "..."` to proceed.
  - **Override path:** Per Q6 resolution (debate concession), `--skip-compliance --reason "..."` may override BLOCKED. Audit log entry written on each use.
- **TU-007 (completion checklist).** `think_about_whether_you_are_done` invocation in `sc-task-protocol/SKILL.md` becomes a hard gate; cannot return `complete` until all six conditions are met (see §3.3).

### 2.3 Additions (new behavior, additive surface)

- **TU-001 (CRITICAL FAIL).** New `CriticalFailCondition` dataclass added to skill internals. Three STRICT-tier conditions are encoded:
  1. Sequential or Serena MCP unavailable → unconditional FAIL.
  2. Output file absent after `max_turns` → unconditional FAIL.
  3. Classification header absent in STRICT-tier task output → unconditional FAIL.
  - Applies to **STRICT only**; STANDARD/LIGHT/EXEMPT exit before the check (per RK-09 mitigation).
- **TU-003 (six principles).** A new "Quality Principles NFR" section in `sc-task-protocol/SKILL.md` enumerates: Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy. Per Q14 resolution: **both prompt and checklist** (prompt drives agent behavior; checklist artifact provides audit trail).
- **Audit log infrastructure (new).** A single append-only log line (one per STRICT task) capturing tier, confidence, override flags used. Powers Q11 telemetry for `--skip-compliance` usage tracking.

### 2.4 Sprint-side additions (R2 sibling release)

- **SE-001.** `gate_passed()` returns `(False, 'empty output file')` on inconclusive-completion or empty output. Tighten existing behavior; edge case only.
- **SE-002.** `task_uid: str` field; format `f'{phase_id}-{task_index:04d}'`.
- **SE-003.** On `--start N`, re-enter at first task with `status != DONE` (not at task 0). Graceful fallback to full-phase restart when UIDs absent (Q10 resolution).
- **SE-004.** `ExecutionMode` enum: `NORMAL, INCOMPLETE_RESUME, CORRECTION`.
- **SE-005.** `GateFailureSeverity` enum: `SEV1_BLOCK, SEV2_CYCLE, SEV3_ADVISORY`. Mapping per Q9 resolution: **map** existing TFEP severities to Sev (no operational change; reporting taxonomy only).

---

## 3. Protocol changes (sc-task-protocol skill)

### 3.1 Where the edits land

All task-side protocol changes are confined to **`src/superclaude/skills/sc-task-protocol/SKILL.md`**. No new sub-directories created (TU-006 deferred).

### 3.2 CRITICAL FAIL semantics (TU-001)

New section inserted between current §3 (MCP requirements) and §4 (tool coordination):

```
### CRITICAL FAIL conditions (STRICT only)

The following conditions cause unconditional FAIL and block task completion:

1. **MCP unavailability.** If Sequential or Serena is unreachable at task entry, FAIL.
2. **Empty output.** If output file is absent after max_turns, FAIL.
3. **Missing classification header.** If the STRICT task's first output line is not the classification sentinel, FAIL.

Each condition is enforced by the skill's gate evaluator, not the agent's discretion.
The gate evaluator runs after every turn for condition 1, after final turn for conditions 2-3.
```

### 3.3 Mandatory completion checklist (TU-007)

The six conditions (per FINAL-REPORT §3.4 known-gap note: must consult LW original; the surgical variant publishes a placeholder list and **requires** the implementation phase to confirm against the LW source before merge):

1. All affected files have been identified and updated.
2. All tests pass (or manual verification documented for STANDARD/LIGHT).
3. No pre-existing test failures introduced.
4. No new contradictions or invariants violated.
5. Adversarial verification (STRICT only) has returned a non-FAIL verdict.
6. `think_about_whether_you_are_done` confirms completion.

Block `complete` status until all 6 are met. Implementation note: this list is **`[inference]`** until R2 L85 is verified against the original LW source — known gap from FINAL-REPORT §6.1 TU-007.

### 3.4 Quality Principles NFR section (TU-003)

A new top-level NFR section in `sc-task-protocol/SKILL.md`, placed before TFEP:

```
### Quality Principles (Universal NFR baseline)

All STANDARD and STRICT task verification must enforce these six principles:

1. **Verifiability.** Every claim must cite file:line evidence.
2. **Completeness.** Acceptance criteria are explicit and verified.
3. **Correctness.** Implementation matches stated specification intent.
4. **Consistency.** No internal contradictions.
5. **Clarity.** Statements are unambiguous and actionable.
6. **Anti-Sycophancy.** Verification verdict is independent of the implementer's
   stated confidence. The verification agent treats high stated confidence as
   neutral evidence, not as license to lower scrutiny.

Verification agents bind each principle to a specific check step. Each MET verdict
cites the principle and the supporting evidence.
```

### 3.5 BLOCKED state (TU-004)

In `task.md` (the command file, not the skill), at the existing `confidence < 0.70` branch:

- **Old:** "prompt user with `--compliance [tier]` override hint."
- **New:** "Emit classification header with `TIER: BLOCKED`, `CONFIDENCE: <computed>`, `KEYWORDS: <split-keywords>`, `OVERRIDE: false`, `RATIONALE: split between <tier-A> and <tier-B>`. **Halt.** User must re-invoke with explicit `--compliance <tier> --reason '...'` or `--skip-compliance --reason '...'` to proceed."

The classification header schema gains `TIER: BLOCKED` as a fifth valid value. The header validator must be updated (otherwise header check fails — risk RK-NEW-1, see §6).

---

## 4. Naming & deprecation (Q1/Q2 policy)

### 4.1 Hard constraints (non-negotiable, from v3.7)

- **`/sc:task` is the only canonical command name.** No new `/sc:task-unified` command, no aliasing, no parallel file at `commands/task-unified.md`.
- **N1-N12 rename map** (v3.7) remains green. CI `TEST-SPEC.md:34-80` must continue to pass.
- **No duplicate `name:` declarations** across `commands/`.

### 4.2 Carry-over artifacts (DEFER decision)

The surgical variant **explicitly preserves**:
- `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header sentinel at `task.md:50-67`.
- `--caller task-unified` in TFEP forensic invocation at `SKILL.md:191-197`.

**Rationale:** Q1 and Q2 are blocking-flagged but **deferable**. The surgical variant takes the conservative path:
- Neither extract identifies a downstream consumer (A-005 unresolved).
- Renaming without audit risks regressing telemetry consumers that may pattern-match on the strings.
- A dedicated cleanup release (paired with TU-005 + TU-006) is the right venue.

The release notes for v3.75 **must** include a "Known telemetry-compat carry-overs" subsection naming both strings, citing R7 §5 item 1 and R8 §6 item 2, and noting the deferred cleanup release.

### 4.3 Header schema update (additive)

The classification header schema is **extended** (not changed) to include `BLOCKED` as a valid TIER value:

```
TIER: [STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED]
```

All other fields and the sentinel comments are unchanged.

### 4.4 Deprecation surface

**Nothing is deprecated in this release.** All existing flags, behaviors, and APIs remain available. The surgical variant deliberately avoids deprecation announcements:

- TU-004's BLOCKED state is a **behavior change at the existing branch**, not a flag deprecation.
- TU-001's CRITICAL FAIL is **additive enforcement**, not a removal of existing gates.
- TU-003 and TU-007 are **new NFR sections / hard gates**, not deprecations.

If future releases (TU-002, TU-005, TU-006, Q1/Q2 cleanup) introduce deprecations, those releases own the deprecation policy.

---

## 5. Test strategy

### 5.1 New tests (required for merge)

**TU-001 (CRITICAL FAIL):**
- `tests/skills/test_task_protocol_critical_fail.py`
  - `test_strict_blocks_on_sequential_unavailable`
  - `test_strict_blocks_on_serena_unavailable`
  - `test_strict_blocks_on_empty_output_after_max_turns`
  - `test_strict_blocks_on_missing_classification_header`
  - `test_exempt_skips_critical_fail_check` (RK-09 mitigation)
  - `test_standard_does_not_apply_output_absent_critical_fail` (RK-09 nuance)

**TU-004 (BLOCKED state):**
- `tests/commands/test_task_blocked_state.py`
  - `test_low_confidence_produces_blocked_header`
  - `test_blocked_header_contains_computed_tier_competing_tier_keywords`
  - `test_skip_compliance_with_reason_overrides_blocked` (Q6 resolution)
  - `test_skip_compliance_without_reason_fails`
  - `test_force_strict_with_reason_overrides_blocked`

**TU-007 (completion checklist):**
- `tests/skills/test_task_completion_checklist.py`
  - Six tests, one per condition: `test_completion_blocks_when_<condition_N>_unmet`.

**TU-003 (quality principles):**
- `tests/skills/test_quality_principles_nfr.py`
  - `test_skill_md_contains_six_principles_section`
  - `test_each_principle_appears_in_verification_check_list`

### 5.2 Regression tests (must remain green)

From v3.7-task-unified-v2 (FINAL-REPORT §9.5):
- `tests/sprint/` full run: **921 passed, 57 failed baseline** — new failures must be net-new, not regressions of previously-passing tests.
- TUI Waves 1-2 + tmux + summarizer + retrospective: **125/125 pass.**
- `test_process.py::TestClaudeProcess`: **16/16** including `test_build_prompt_contains_task_command`.
- `TEST-SPEC.md:34-80`: no `/sc:task-unified` strings in `ClaudeProcess.build_prompt` output.
- Wave-4 checkpoint heading parser tests (HANDOVER `:253-304`): **+3 tests must pass** (RK-15 from FINAL-REPORT §7).

### 5.3 Telemetry-compat tests (Q1/Q2 carry-over preservation)

To prevent accidental regression of the carry-over decision:
- `tests/commands/test_classification_header_sentinel_preserved.py`
  - `test_classification_sentinel_contains_task_unified_string` (asserts the carry-over remains).
- `tests/skills/test_tfep_caller_string_preserved.py`
  - `test_forensic_caller_is_task_unified` (asserts the carry-over remains until cleanup release).

These tests **document** the carry-over decision in executable form. They MUST be updated if/when Q1/Q2 are resolved in a future release.

### 5.4 Sprint-side tests (R2 sibling release)

**SE-001:**
- `tests/sprint/test_gate_passed_empty_output.py::test_empty_output_returns_false`.

**SE-002 + SE-003 (paired):**
- `tests/sprint/test_task_uid_generation.py::test_uid_stable_across_sessions`.
- `tests/sprint/test_subphase_resume.py::test_resume_from_first_undone_task`.
- `tests/sprint/test_subphase_resume.py::test_graceful_fallback_when_uids_absent` (Q10 resolution).
- **CRITICAL:** Re-run Wave-4 checkpoint heading parser tests (+3 tests) — non-negotiable per RK-15.

**SE-004, SE-005:**
- Enum-existence + value-set tests.

### 5.5 TUI tests (P-series, from FINAL-REPORT §11.5)

Per FINAL-REPORT §11.3 mandatory mitigations:

- `tests/sprint/test_monitor_reset_between_tasks.py` (P-01 INV-001/005, MANDATORY).
- TUI smoke tests per §11.5 acceptance criteria — manual but documented as part of release acceptance.
- P-03 INV-004 downstream-consumer audit (15-min grep audit, pre-merge requirement).

### 5.6 Coverage target

- **80% line coverage** on new code introduced by TU-001, TU-003, TU-004, TU-007.
- **No coverage requirement** on the carry-over preservation tests (they are existence checks).

---

## 6. Backward compatibility & risk

### 6.1 Compat guarantees

- **All existing invocations of `/sc:task` continue to work identically** EXCEPT in the narrow band of low-confidence (<0.70) classifications, which now BLOCK instead of soft-prompt.
- The CLI flag surface is **unchanged**: no flags added, no flags removed.
- The classification header schema is **extended** (BLOCKED added) but not changed for existing tiers.
- The skill file structure is **unchanged**: still just `SKILL.md` + `__init__.py`.
- The carry-over telemetry strings (`SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) are **preserved verbatim**.

### 6.2 Behavior changes that may surprise users

| Change | What users see | Mitigation |
|--------|----------------|------------|
| TU-004 BLOCKED | Tasks with ambiguous keyword classification (~5-10% of historical traffic, `[inference]`) will halt where they previously auto-classified. | Release notes call this out; `--compliance auto` users see the change first. Provide a clear error message pointing to `--compliance <tier> --reason "..."`. |
| TU-001 STRICT-only output absent | STRICT tasks that previously completed with empty output (likely buggy completions) will now FAIL. | Expected to be net positive; users with legitimate "no-output" STRICT tasks should reclassify to EXEMPT. |
| TU-007 completion checklist | STRICT/STANDARD tasks that previously returned `complete` despite gaps will now block. | Expected to be net positive; document the six conditions in release notes. |

### 6.3 New risks introduced by this release

| ID | Risk | Sev | Like | Mitigation |
|----|------|-----|------|------------|
| RK-NEW-1 | TU-004 BLOCKED adds `BLOCKED` to classification header TIER enum — downstream parsers may not handle it. | Medium | Low | Add `BLOCKED` to all known parsers (search `src/superclaude/` for `STRICT|STANDARD|LIGHT|EXEMPT` regex). |
| RK-NEW-2 | TU-001 #3 (missing classification header) may false-positive during early-development sessions where header generation is in flux. | Low | Medium | Apply to STRICT only; document workaround as `--skip-compliance --reason "header-development"`. |
| RK-NEW-3 | TU-007 6-condition list is `[inference]` (per FINAL-REPORT §6.1 known gap) — implementation phase may discover a different canonical list in original LW source. | Medium | Medium | Confirm 6 conditions against LW original before merge; do NOT ship until confirmed. Tag implementation task as blocked-on-source-verification. |
| RK-NEW-4 | Q11 telemetry on `--skip-compliance` usage adds an audit-log write path; could be I/O-sensitive in tight loops. | Low | Low | Append-only JSON log; benchmark in pre-merge perf gate. |

All FINAL-REPORT §7 risks (RK-01 through RK-18 + RK-OOS-1..3 + RK-TUI-01..05) remain applicable to this release; the surgical variant adds the four above.

### 6.4 Inherited risks (FINAL-REPORT §7, summarized)

The surgical variant adopts FINAL-REPORT §7 risks **without modification**, especially:
- **RK-05** Classification logic duplication / drift — **acknowledged but unresolved** in this release (TU-005 deferred).
- **RK-10** Naming-artifact telemetry-compat — **acknowledged and explicitly preserved** in this release (Q1/Q2 deferred).
- **RK-15, RK-16** Wave-4 parser regression + unvalidated live sprint execution — **prerequisites** for shipping SE-002+SE-003 (paired).

---

## 7. Release split (Q8 commitment, §9.3)

### 7.1 Recommended split

**R1: Task-surface (this release, immediate):**
- TU-001, TU-003, TU-004, TU-007.
- Audit log infrastructure for Q11.
- Telemetry-compat preservation tests for Q1/Q2 carry-overs.
- All new tests from §5.1 + §5.2.

**Effort:** ~3-5 dev-days (sum of 1×M + 3×S = 1-3 + 1.5 = 2.5-4.5 days; round to 3-5). `[inference]`

**R2: Sprint-runtime + TUI (sibling release, can ship in parallel or after R1):**
- SE-001, SE-002+SE-003 (paired, conditional on Wave-4 parser tests passing), SE-004, SE-005.
- TUI top-5 (P-05, P-02, P-03+P-07, P-01) in ship order.

**Effort:** ~5-7 dev-days. `[inference]`

**Total effort if both ship in v3.75:** ~8-12 dev-days. Compatible with one sprint. `[inference]`

### 7.2 R1 → R2 dependencies

R2 depends on R1 **only** in one narrow place:
- SE-001's fail-closed gate may **reference** TU-001's CRITICAL FAIL semantics for consistent vocabulary. The reference is documentation-only; the implementations are independent.

Other than that, R1 and R2 are siblings, not sequential.

### 7.3 Why this is the surgical seam

- **Different reviewer pools.** Task-surface changes need protocol-skill expertise; sprint-runtime needs CLI / subprocess expertise.
- **Different blast radii.** Task-surface affects every `/sc:task` invocation; sprint-runtime affects only `superclaude sprint run`.
- **Different test surfaces.** Task-surface tests live in `tests/skills/` and `tests/commands/`; sprint-runtime tests live in `tests/sprint/`.
- **Different validation prerequisites.** Sprint-runtime depends on RK-16 (live sprint execution validation, currently OPEN) being addressed; task-surface does not.

The release-split protocol (`sc-release-split-protocol`) should be applied to verify these seams. `[inference]`

### 7.4 What does NOT split

Q1/Q2 cleanup (Q1 sentinel rename + Q2 forensic-caller rename) does **not** belong in either R1 or R2 of this release. It is **its own future release** alongside TU-005 + TU-006, gated on the A-005 audit (enumerate `/sc:forensic` consumers of `--caller task-unified`).

---

## 8. Open questions (carried from FINAL-REPORT §8)

The surgical variant adopts FINAL-REPORT §8 resolutions and confirms:

| Q | Recommendation | Status in this release |
|---|----------------|------------------------|
| Q1 (sentinel rename) | DEFER to cleanup release | DEFERRED (preserved verbatim) |
| Q2 (forensic-caller rename) | DEFER to cleanup release | DEFERRED (preserved verbatim) |
| Q3 (output-type precedence) | (a) modifier — tier → output-type | NOT APPLICABLE (TU-002 deferred) |
| Q4 (output-type=opinion detection) | (a)+(c) filename + override flag | NOT APPLICABLE |
| Q5 (BLOCKED message format) | (a)+(b) CLI prompt + inline header | **(a)+(b) adopted** (§3.5) |
| Q6 (override BLOCKED via flag) | (c) yes with `--reason` + audit log | **(c) adopted** (§2.2, §3.5) |
| Q7 (`config/tier-keywords.yaml`) | (a) create SoT — DEFERRED | DEFERRED (TU-005/TU-006 release) |
| Q8 (release split) | YES, apply protocol | **ADOPTED** (§7) |
| Q9 (severity-enum scope) | (c) map TFEP → Sev | **(c) adopted** (§2.4) |
| Q10 (legacy result file migration) | (a) graceful fallback | **(a) adopted** (§2.4 SE-003) |
| Q11 (`--skip-compliance` metering) | (a) add metering now | **(a) adopted** (§2.3 audit log) |
| Q12 (keyword reconciliation) | (c) TU-005 SoT — DEFERRED | DEFERRED |
| Q13 (v3.7 follow-ups) | (c) `--checkpoint-gate-mode` + live-run | **ACKNOWLEDGED**; live-run is soft prereq for R2 |
| Q14 (six-principles enforcement) | (c) both prompt + checklist | **(c) adopted** (§3.4) |

**Remaining open (not blocking, but flagged):**
- **A-005** Enumerate `/sc:forensic` consumers of `--caller task-unified`. Recommendation: add as a dedicated investigation task in the cleanup release.
- **TU-007 six-condition list** Verify against original LW source before merge.

---

## 9. Acceptance criteria

This release ships when:

1. **All new tests in §5.1 pass.**
2. **All regression tests in §5.2 remain green** (921 passed sprint baseline, 125/125 TUI, 16/16 ClaudeProcess, +3 Wave-4 parser).
3. **TU-007 six-condition list verified** against original LW source. `[inference]` Known gap from FINAL-REPORT §6.1.
4. **Audit log infrastructure deployed** and capturing `--skip-compliance` usage.
5. **Carry-over preservation tests** (§5.3) green.
6. **Release notes** include:
   - "Behavior changes that may surprise users" section (per §6.2).
   - "Known telemetry-compat carry-overs" section naming `SC:TASK-UNIFIED:CLASSIFICATION` and `--caller task-unified`.
   - Pointers to the eventual TU-005/TU-006/Q1/Q2 cleanup release for users wanting to track the carry-over removal.
7. **If R2 (sprint-side) is bundled:** Wave-4 parser tests pass; SE-002+SE-003 paired PR includes the 3 mandatory tests.
8. **If TUI bundle is included:** P-01 ships only after P-05/P-02/P-03+P-07 (per §11 ship order); `test_monitor_reset_between_tasks.py` passes.

---

## 10. Coverage notes

- **All 11 FINAL-REPORT sections incorporated:** §1 Scope (mapped to §1 here), §2 Sources (referenced throughout), §3 task-unified inventory (covered in §2.2/§3.x), §4 /sc:task inventory (preserved in §2.1), §5 Overlap matrix (driven §1.2 in/out scope decisions), §6 Best-of-breed (mapped to §2.3/§2.4/§3.x), §7 Risks (mapped to §6), §8 Open questions (mapped to §8), §9 Prior-art constraints (mapped to §4 + §7), §10 Shared assumptions (A-005 carried to §8 known-open), §11 TUI bundle (mapped to §5.5 + §6.3 RK-TUI carry).
- **Hard constraint compliance:** `/sc:task` is the only canonical command name (§4.1); N1-N12 rename map green (§5.2); carry-overs preserved (§4.2); no `name: task-unified` reintroduced (§1.3 NG-1).
- **`[inference]` callouts:** Effort labels in §7 (FINAL-REPORT §10 A-003); TU-007 six-condition list (FINAL-REPORT §6.1 + A-004); Q11 metering pairing with TU-001 (FINAL-REPORT §6 + §8 Q11); behavior-change traffic estimate in §6.2.

**Variant signature:** Surgical port-of-best-features. Smallest diff against `/sc:task`. Carry-overs preserved. TU-002/TU-005/TU-006 explicitly deferred. R1 task-surface ships immediately; R2 sprint+TUI ships as sibling. Zero breaking changes.
