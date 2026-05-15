<!-- Variant: sonnet:analyzer — "contingent / decision-tree approach; identify which sub-features merge cleanly vs. which require versioned deprecation" -->
<!-- Generated from FINAL-REPORT.md (11 sections) -->

# RELEASE SPEC — v3.75 RigorflowMerger / task-unified-v3 (Contingent Decision-Tree Variant)

**Stance.** Reject the binary "surgical vs. structural" framing. Each FINAL-REPORT candidate has its own merge profile — some are clean adoptions, others require versioned deprecation, others should be deferred entirely. Build the release spec from a per-candidate decision tree applied to the full §6 slate. Document the **decision rule** alongside every verdict so subsequent releases can re-evaluate as conditions change.

**Source.** FINAL-REPORT.md (11 sections, including §10 Shared Assumptions and §11 TUI Improvement Bundle).

**Method.** For each candidate, evaluate against three decision dimensions:
1. **Coupling** — how many other candidates/files does it touch?
2. **Behavioral break** — does it change existing observable behavior?
3. **Investigation gate** — does it depend on resolving a FINAL-REPORT Q-NNN or A-NNN?

Verdicts: **ADOPT** (clean), **ADOPT-WITH-DEPRECATION** (behavioral break needs runway), **DEFER-GATED** (blocked on investigation), **DEFER-COUPLED** (depends on a deferred sibling), **REJECT** (anti-goal).

---

## 1. Release identity & scope

### 1.1 Name and version

- **Release ID:** `v3.75-RigorflowMerger-task-unified-v3`
- **Version bump:** `version: "2.0.0"` → `version: "2.2.0"` (minor bump because behavioral changes exist but are gated; major bump deferred to whichever release ships the Q1/Q2 renames).
- **Surface affected:** `/sc:task` command file, `sc-task-protocol` skill, `cli/sprint/` runtime, TUI rendering — but **per-candidate** based on the decision tree below.

### 1.2 Per-candidate decision tree

The release ships the candidates from §1.4 only. Below is the full decision matrix.

| Candidate | Coupling | Break? | Gate | Verdict | Rationale |
|-----------|---------:|:------:|:----:|---------|-----------|
| TU-001 (CRITICAL FAIL) | LOW | Yes (STRICT only) | None | **ADOPT-WITH-DEPRECATION** | Affects STRICT completion criterion; behavioral break must be announced. Additive surface. |
| TU-002 (output-type axis) | HIGH | Yes (routing) | **Q3** (precedence rule) | **DEFER-GATED** | Q3 recommendation exists ((a) modifier) but is `[inference]`; need confirmation. High coupling (touches ORCHESTRATOR + task.md + skill + tasklist-protocol). |
| TU-003 (six principles) | LOW | No | None | **ADOPT** | NFR addition; no flag or behavior change. R4 L77: "agent instruction addition; no code changes." |
| TU-004 (BLOCKED state) | MEDIUM | Yes (header schema) | **Q5** + **Q6** | **ADOPT-WITH-DEPRECATION** | Q5 & Q6 recommendations exist and are sound; behavioral break (soft prompt → hard block) must have user-facing announcement + override path. |
| TU-005 (SoT YAML) | HIGH | No (internal) | **Q7** + **Q12** | **DEFER-COUPLED** | Touches 4 files; FINAL-REPORT §6.1 already recommends DEFER. Coupled to TU-006. |
| TU-006 (skill sub-files) | MEDIUM | No | **Q7** + **Q8** | **DEFER-COUPLED** | Bundles naturally with TU-005. Worth its own release. |
| TU-007 (completion checklist) | LOW | Yes (TFEP gate) | **A-004** (six-condition list verification) | **ADOPT-WITH-INVESTIGATION** | Six conditions are `[inference]` per FINAL-REPORT §6.1; must verify against LW source pre-merge but verification is a one-time task, not a release blocker. |
| SE-001 (fail-closed gate) | LOW | Yes (sprint side) | None | **ADOPT** | R3 L34 "Low. Edge case for empty output files." Tightens; no new surface. |
| SE-002 (per-task UID) | MEDIUM | Yes (result files) | **Q10** (migration) | **ADOPT-WITH-DEPRECATION** | Q10 recommends graceful fallback (option a) — migration path is clean. Couples to SE-003 (must ship paired). |
| SE-003 (sub-phase resume) | MEDIUM | Yes (prompt) | **RK-15** (Wave-4 parser) | **ADOPT-WITH-DEPRECATION** | Must re-run Wave-4 parser tests pre-merge per RK-15. Couples to SE-002. |
| SE-004 (ExecutionMode) | LOW | No | None | **ADOPT** | Enum addition; no behavior change. |
| SE-005 (GateFailureSeverity) | LOW | No | **Q9** (scope) | **ADOPT** | Q9 (c) (map TFEP → Sev) is the right scope; reporting-taxonomy-only. |
| SE-006 (auto-diagnostic threshold) | MEDIUM | Yes (new path) | **RK-OOS-3** (diagnostic-chain hardening) | **DEFER-GATED** | Diagnostic chain robustness to sprint-context input is an OOS issue from FINAL-REPORT §7.1. Ship SE-006 only after diagnostic chain is hardened. |
| Q1 (sentinel rename) | LOW | Yes (string) | **A-005** | **DEFER-GATED** | A-005 investigation (forensic consumer audit) is unresolved. Cannot rename without confirming no consumer pattern-matches the literal. |
| Q2 (forensic-caller rename) | LOW | Yes (string) | **A-005** | **DEFER-GATED** | Same A-005 gate as Q1. |
| TUI P-01 (OutputMonitor wiring) | HIGH | No | **INV-001/005** | **ADOPT-WITH-MITIGATION** | Mandatory test `test_monitor_reset_between_tasks.py` (FINAL-REPORT §11.3). |
| TUI P-02, P-03, P-05, P-07 | LOW-MED | No-Low | None | **ADOPT** | Per FINAL-REPORT §11 top-5 selection. |

### 1.3 Verdict summary

- **ADOPT (clean):** TU-003, SE-001, SE-004, SE-005, TUI P-02/P-03/P-05/P-07 — **8 candidates**.
- **ADOPT-WITH-DEPRECATION:** TU-001, TU-004, SE-002, SE-003 — **4 candidates** (paired SE-002/003).
- **ADOPT-WITH-INVESTIGATION:** TU-007 — **1 candidate** (one-time pre-merge investigation).
- **ADOPT-WITH-MITIGATION:** TUI P-01 — **1 candidate** (mandatory test added).
- **DEFER-GATED:** TU-002 (Q3), SE-006 (RK-OOS-3), Q1 (A-005), Q2 (A-005) — **4 candidates**, each blocked on a documented investigation.
- **DEFER-COUPLED:** TU-005, TU-006 — **2 candidates**, ship together as their own follow-on release.

### 1.4 In-scope (this release)

The contingent variant ships:

**Task-side rigor (R1 of release split):**
- TU-001 (with deprecation announcement).
- TU-003.
- TU-004 (with deprecation announcement).
- TU-007 (after the six-condition LW-source verification).

**Sprint-side runtime (R2 of release split):**
- SE-001.
- SE-002 + SE-003 (paired; gated on Wave-4 parser).
- SE-004.
- SE-005.

**TUI bundle (R2):**
- P-05, P-02, P-03, P-07, P-01 (with mandatory `test_monitor_reset_between_tasks.py`).

**Audit log infrastructure (Q11):**
- ADOPT now (powers TU-001 audit trail + TU-004 BLOCKED override audit + future Q1/Q2 telemetry investigation).

**Migration guide infrastructure:**
- A new `docs/migration/v3.75.md` documents every ADOPT-WITH-DEPRECATION behavior change with a recommended user action.

### 1.5 Out-of-scope (deferred, gated, or rejected)

**Deferred to next release** (DEFER-COUPLED bundle):
- TU-002 (output-type axis) — pending Q3 confirmation.
- TU-005 (SoT YAML).
- TU-006 (skill sub-files).
- Q1 (sentinel rename) — pending A-005.
- Q2 (forensic-caller rename) — pending A-005.

**Deferred to a later release** (DEFER-GATED, single-issue blockers):
- SE-006 (auto-diagnostic threshold) — pending diagnostic-chain hardening per RK-OOS-3.

**Rejected** (anti-goals, per FINAL-REPORT §1.2 + §6.4):
- NG-1: Reintroduce `/sc:task-unified` as live command.
- NG-2: Resurrect `task-unified.md` / `sc-task-unified-protocol/`.
- NG-3: Semantic NLP classifier.
- NG-4: LW bash-orchestrator / Python-from-bash patterns.

### 1.6 Release-split outcome

The decision tree naturally produces a **two-release plan** identical in shape to the surgical variant's R1+R2, plus a **third future release** for the deferred bundle:

- **R1 (this release, task-surface):** ADOPT + ADOPT-WITH-DEPRECATION task-side: TU-001, TU-003, TU-004, TU-007.
- **R2 (this release, sprint+TUI):** ADOPT + ADOPT-WITH-DEPRECATION sprint-side: SE-001, SE-002+SE-003 (paired), SE-004, SE-005 + TUI top-5.
- **R3 (future, gated):** TU-002, TU-005, TU-006, Q1, Q2 — pending Q3/A-005/Q7/Q12 resolutions.
- **R4 (later, single-issue):** SE-006 — pending RK-OOS-3.

R1 ⊥ R2 (siblings; can ship in parallel). R3 depends on investigations clearing. R4 depends on RK-OOS-3 clearing.

---

## 2. Surface contract (per-candidate, with decision rule)

### 2.1 Stays unchanged

- Command name `/sc:task`.
- All 8 CLI flags.
- Strategy / compliance / verify axes.
- Carry-over strings (`SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) — preserved because Q1/Q2 are DEFER-GATED on A-005.

### 2.2 Changes (per-candidate, with deprecation runway label)

| Candidate | Change | Behavioral break | User-visible? | Runway |
|-----------|--------|------------------|---------------|--------|
| TU-001 | STRICT tasks unconditionally FAIL on (a) MCP missing, (b) empty output, (c) missing header. | Yes (STRICT tasks that previously completed-empty will now FAIL). | Yes (STRICT users see new FAIL conditions in error messages). | Migration guide entry; no shim needed (additive enforcement). |
| TU-004 | Low-confidence soft prompt becomes deterministic BLOCKED state. Header schema gains `BLOCKED` value. | Yes (5-10% of `--compliance auto` users, `[inference]`). | Yes (clearer error message; explicit re-invocation required). | Migration guide entry; `--skip-compliance --reason "..."` is the documented escape hatch. |
| TU-007 | Completion checklist becomes a hard gate (six conditions before `complete`). | Yes (STRICT/STANDARD tasks that returned `complete` despite gaps now block). | Yes (more diagnostic information). | Migration guide entry; net positive expected. |
| SE-001 | Empty output → `(False, 'empty output file')` instead of soft PASS. | Yes (sprint runs that relied on inconclusive PASS will now fail). | Yes (sprint owners see new failures). | Migration guide entry. |
| SE-002+SE-003 | Per-task UID + sub-phase resume. Result file format extended (additional `task_uid` field). | No (additive field; graceful fallback to full-phase restart per Q10 (a)). | Visible only when resuming (`--start N`); faster resumes when UIDs present. | None needed (graceful fallback covers legacy). |
| Q1/Q2 (DEFERRED) | n/a — explicitly preserved verbatim in this release. | n/a | n/a | n/a |

### 2.3 Additions (no break, additive)

- TU-001 `CriticalFailCondition` dataclass.
- TU-003 NFR section + checklist + prompt binding (Q14 (c) both).
- TU-004 `TIER: BLOCKED` value in header schema (additive enumeration).
- SE-004 `ExecutionMode` enum.
- SE-005 `GateFailureSeverity` enum (Q9 (c) map TFEP → Sev).
- Audit log infrastructure (Q11 (a)).
- TUI P-series fixes (additive; no behavior break, all renderer-only except P-01 which is a structural change in executor.py).

### 2.4 Surface diff (compact)

```diff
  CLI flags (8 total, unchanged):
    --strategy, --compliance, --verify, --skip-compliance,
    --force-strict, --parallel, --delegate, --no-escalation

  Classification header TIER values:
-   [STRICT|STANDARD|LIGHT|EXEMPT]
+   [STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED]

  CRITICAL FAIL conditions (NEW for STRICT):
+   1. MCP unavailable → FAIL
+   2. Empty output after max_turns → FAIL (STRICT only)
+   3. Missing classification header → FAIL (STRICT only)

  Quality Principles NFR (NEW):
+   Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy

  Completion checklist (NEW, gated):
+   6 conditions before `complete` status (TU-007; LW source verification required)

  Sprint runtime (R2):
+   ExecutionMode enum, GateFailureSeverity enum, task_uid field, sub-phase resume
+   Fail-closed empty-output gate

  TUI (R2):
+   Spinner on RUNNING (P-05), elapsed-since-phase-start Duration (P-02),
+   width-aware truncation (P-03+P-07), OutputMonitor wired into per-task path (P-01)

  Carry-overs (DEFERRED to R3):
    SC:TASK-UNIFIED:CLASSIFICATION sentinel — preserved
    --caller task-unified — preserved
```

---

## 3. Protocol changes (sc-task-protocol skill)

### 3.1 Scope of edits

The contingent variant **does not** restructure the skill into sub-directories (TU-006 deferred). All task-side protocol edits land in `src/superclaude/skills/sc-task-protocol/SKILL.md` plus new sibling `audit.py`.

### 3.2 New sections added to SKILL.md

In order of insertion:

1. **§2.5 CRITICAL FAIL conditions (TU-001)** — between current §2 (entry rule) and §3 (MCP requirements).
2. **§3.5 Quality Principles NFR (TU-003)** — at end of current §3.
3. **§8 Mandatory completion checklist (TU-007)** — new top-level section.

(Sections renumbered as needed.)

### 3.3 CRITICAL FAIL semantics (TU-001)

```
### CRITICAL FAIL conditions (STRICT only)

The following conditions cause unconditional FAIL and block task completion.
Applies to STRICT tier only. STANDARD/LIGHT/EXEMPT exit before evaluation.

| Condition | When checked | Always blocks? |
|-----------|--------------|----------------|
| Sequential or Serena MCP unavailable | task entry, after each turn | Yes |
| Output file absent after max_turns | after final turn | Yes |
| Classification header absent | after first turn | Yes |

Decision rule for additions: any new condition must be deterministic, applicable
only to STRICT, and have a non-recoverable failure mode (no soft degradation).

Implementation: CriticalFailCondition dataclass in audit.py:
  @dataclass
  class CriticalFailCondition:
      condition_type: str
      description: str
      always_blocks: bool = True
```

### 3.4 Quality Principles NFR (TU-003)

Verbatim text from FINAL-REPORT §3.4 / R4 L70:

```
### Quality Principles (Universal NFR)

All STANDARD and STRICT verification must enforce these six principles.
Each MET verdict by the verification agent must cite the principle and
specific evidence (file:line citation, quote, or check result).

1. Verifiability — every claim cites file:line evidence.
2. Completeness — acceptance criteria explicit and verified.
3. Correctness — implementation matches stated specification intent.
4. Consistency — no internal contradictions.
5. Clarity — statements unambiguous and actionable.
6. Anti-Sycophancy — verdict independent of implementer's stated confidence.

Enforcement: prompt + checklist (Q14 (c)).
- The verification agent's prompt names the six principles.
- The verification artifact contains a checklist; each principle row carries
  a citation field. Audit log captures the checklist completeness.
```

### 3.5 BLOCKED state (TU-004)

```
### Confidence threshold (TU-004)

When the classifier's max_tier_score confidence < 0.70:
  - DO NOT auto-classify.
  - Emit classification header with:
      TIER: BLOCKED
      CONFIDENCE: <computed>
      KEYWORDS: <comma-separated split-keywords>
      OVERRIDE: false
      RATIONALE: split between <tier-A> (<score-A>) and <tier-B> (<score-B>)
  - Halt execution. Do not invoke Skill sc:task-protocol.
  - User must re-invoke with --compliance <tier> --reason "..." OR
    --skip-compliance --reason "..." to proceed.

Override semantics (Q6 (c)):
  - --compliance <tier> --reason "..." bypasses BLOCKED with explicit tier.
  - --skip-compliance --reason "..." bypasses tier check entirely.
  - --force-strict --reason "..." forces STRICT regardless.
  - Each override path writes an audit log entry.
```

### 3.6 Completion checklist (TU-007)

```
### Mandatory completion checklist (TU-007)

Before any task may return `complete`, the following six conditions must be met.

KNOWN GAP: This list is `[inference]` per FINAL-REPORT §6.1 — R2 L85 does not
enumerate the six conditions verbatim. The implementation must consult the
original LW source and verify the list before merge. The six conditions below
are a working list, not a final list.

1. All affected files have been identified and updated.
2. All tests pass (or manual verification documented for STANDARD/LIGHT).
3. No pre-existing test failures introduced.
4. No new contradictions or invariants violated.
5. Adversarial verification (STRICT) returned a non-FAIL verdict.
6. think_about_whether_you_are_done confirms completion.

Pre-merge gate: the LW-source-verification investigation completes and either
(a) confirms this list matches the original, or (b) supplies the canonical list,
which replaces this one. NO MERGE until this investigation is complete.
```

### 3.7 Audit log infrastructure (Q11)

New file: `src/superclaude/skills/sc-task-protocol/audit.py`.

Per FINAL-REPORT §6.1 + Q11 + the contingent variant's decision rule: ship audit log infrastructure **now** because it serves three downstream goals:
1. TU-001 audit trail.
2. TU-004 override audit (per Q6 (c)).
3. Future A-005 investigation telemetry — if Q1/Q2 renames eventually proceed, having an audit log on `--caller task-unified` usage would have de-risked the rename.

Schema (per entry, JSONL):
```json
{
  "ts": "ISO-8601",
  "task_id": "uuid",
  "tier": "STRICT|STANDARD|LIGHT|EXEMPT|BLOCKED",
  "confidence": 0.85,
  "user_override_tier": null,
  "skip_compliance": false,
  "force_strict": false,
  "reason": null,
  "critical_fail": null
}
```

Persisted to `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`. Append-only; daily rotation.

---

## 4. Naming & deprecation (per-candidate)

### 4.1 Hard constraints (non-negotiable)

- `/sc:task` is the only canonical command name.
- N1-N12 rename map (v3.7) remains green.
- `TEST-SPEC.md:34-80` continues to pass.
- No duplicate `name:` declarations in `commands/`.

### 4.2 Per-deprecation runway

| Item | Action this release | Future release |
|------|---------------------|-----------------|
| TU-001 CRITICAL FAIL on empty STRICT output | INTRODUCED; migration guide entry | n/a (new behavior) |
| TU-001 CRITICAL FAIL on missing STRICT header | INTRODUCED; migration guide entry | n/a |
| TU-004 BLOCKED state replaces soft prompt | INTRODUCED; migration guide entry | n/a |
| TU-004 `BLOCKED` value in header TIER enum | ADDITIVE; downstream parsers updated | n/a |
| TU-007 completion checklist | INTRODUCED (after LW-source verification) | n/a |
| Q1 sentinel rename | **NOT INTRODUCED** (DEFER-GATED on A-005) | Future R3 release with shim |
| Q2 forensic-caller rename | **NOT INTRODUCED** (DEFER-GATED on A-005) | Future R3 release with shim |

### 4.3 Decision rules for future cleanup release

When the deferred bundle (R3) eventually ships, the contingent variant's recommendations are:

- **Q1, Q2:** Rename **with telemetry-compat shim** for one release cycle (R3.v1: emit new + accept both; R3.v2: remove old). This matches the unification variant's runway proposal.
- **TU-005:** Adopt option (c) (SoT YAML) per Q7/Q12 recommendations.
- **TU-006:** Adopt option (a) per Q7 recommendation. Bundle with TU-005.
- **TU-002:** Adopt option (a) modifier per Q3 recommendation.

These recommendations are **non-binding** on R3 because the conditions may change between this release and R3 (A-005 investigation outcome, telemetry data from this release's audit log, etc.).

---

## 5. Test strategy (per-candidate)

### 5.1 ADOPT (clean) tests

**TU-003 (six principles):**
- `tests/skills/test_quality_principles_nfr.py`
  - `test_skill_md_contains_six_principles_section`
  - `test_each_principle_appears_in_verification_checklist`

**SE-001:**
- `tests/sprint/test_gate_passed_empty_output.py::test_empty_output_returns_false`.

**SE-004:**
- `tests/sprint/test_execution_mode_enum.py::test_three_values_present`.

**SE-005:**
- `tests/sprint/test_gate_failure_severity_enum.py::test_three_values_present`.
- `tests/sprint/test_severity_maps_to_tfep.py::test_tfep_unchanged_operationally`.

**TUI P-02/P-03/P-05/P-07:**
- Smoke tests per FINAL-REPORT §11.5.
- P-03 INV-004 downstream-consumer audit log (15-min pre-merge grep, documented in PR).

### 5.2 ADOPT-WITH-DEPRECATION tests

**TU-001 (CRITICAL FAIL):**
- `tests/skills/test_task_protocol_critical_fail.py`
  - `test_strict_blocks_on_sequential_unavailable`
  - `test_strict_blocks_on_serena_unavailable`
  - `test_strict_blocks_on_empty_output_after_max_turns`
  - `test_strict_blocks_on_missing_classification_header`
  - `test_exempt_skips_critical_fail_check` (RK-09)
  - `test_standard_does_not_apply_empty_output_check` (RK-09)
  - `test_critical_fail_writes_audit_log_entry`

**TU-004 (BLOCKED):**
- `tests/commands/test_task_blocked_state.py`
  - `test_low_confidence_produces_blocked_header`
  - `test_blocked_header_contains_computed_tier_competing_tier_keywords`
  - `test_skip_compliance_with_reason_overrides_blocked` (Q6 (c))
  - `test_skip_compliance_without_reason_fails`
  - `test_blocked_writes_audit_log_entry`

**SE-002 + SE-003 (paired):**
- `tests/sprint/test_task_uid.py::test_uid_stable_across_sessions`.
- `tests/sprint/test_subphase_resume.py::test_resume_from_first_undone_task`.
- `tests/sprint/test_subphase_resume.py::test_graceful_fallback_when_uids_absent` (Q10 (a)).
- **MANDATORY:** Re-run Wave-4 checkpoint heading parser tests (+3 tests). Non-negotiable per RK-15.

### 5.3 ADOPT-WITH-INVESTIGATION (TU-007)

The pre-merge investigation is the test:
- **Investigation:** Verify the six-condition completion checklist against the original LW source.
- **Artifact:** `docs/tu-007-completion-checklist-verification.md` documenting the LW source citation and the canonical six-condition list.
- **Test:**
  - `tests/skills/test_task_completion_checklist.py`
    - One parameterized test per condition, where the parameter list comes from `docs/tu-007-completion-checklist-verification.md`. If the verification doc supplies 6 conditions, 6 tests run; if 7, 7 tests run.
- **Pre-merge gate:** Investigation completes and the parameterized tests pass.

### 5.4 ADOPT-WITH-MITIGATION (TUI P-01)

Per FINAL-REPORT §11.3:
- **MANDATORY:** `tests/sprint/test_monitor_reset_between_tasks.py`
  - `test_events_received_equals_6_after_two_3_event_tasks_with_reset`
  - `test_last_read_pos_correct_after_reset`
- **MANDATORY:** `OutputMonitor.reset_for_next_task()` public method exists and is idempotent.
- **MANDATORY:** P-01 shipped LAST in the TUI sequence (after P-05, P-02, P-03+P-07).

### 5.5 Audit log infrastructure tests

- `tests/skills/test_audit_log.py`
  - `test_audit_log_append_only`
  - `test_audit_log_jsonl_format`
  - `test_audit_log_rotates_daily`
  - `test_audit_log_captures_skip_compliance_reason`
  - `test_audit_log_captures_blocked_overrides`

### 5.6 Regression tests

Same baseline as both other variants (FINAL-REPORT §9.5):
- Sprint full run: 921 passed, 57 failed baseline.
- TUI Waves 1-2 + tmux + summarizer + retrospective: 125/125.
- `test_process.py::TestClaudeProcess`: 16/16.
- `TEST-SPEC.md:34-80`: no `/sc:task-unified` strings.
- Wave-4 checkpoint heading parser: +3.

Plus the contingent-variant invariant:
- The `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` carry-over remains in the emitted classification header (DEFERRED rename).
- `--caller task-unified` remains in the TFEP forensic invocation (DEFERRED rename).

### 5.7 Coverage target

- **80% line coverage** on all new code (TU-001, TU-003, TU-004, TU-007, audit.py, SE-001..005).
- **100% on `audit.py`** (security-sensitive write path; mirrors unification variant's reasoning).
- **No coverage requirement** on carry-over preservation (existence tests only).

---

## 6. Backward compatibility & risk

### 6.1 Compat guarantees

- **Command name `/sc:task`** — unchanged.
- **All 8 CLI flags** — unchanged (no new flags this release; `--output-type` deferred with TU-002).
- **Classification header schema** — extended (BLOCKED added) but not changed for existing tiers.
- **Skill file structure** — unchanged (no sub-directories; TU-006 deferred).
- **Carry-over telemetry strings** — preserved verbatim.

### 6.2 Behavioral breaks (with migration-guide pointer)

| Item | Migration guide entry |
|------|------------------------|
| TU-001 (STRICT empty output → FAIL) | docs/migration/v3.75.md#tu-001 |
| TU-001 (STRICT missing header → FAIL) | docs/migration/v3.75.md#tu-001 |
| TU-004 (low-confidence BLOCKED) | docs/migration/v3.75.md#tu-004 |
| TU-007 (completion checklist) | docs/migration/v3.75.md#tu-007 |
| SE-001 (empty output gate) | docs/migration/v3.75.md#se-001 |
| SE-002+SE-003 (UID + resume) | docs/migration/v3.75.md#se-002-se-003 (with graceful-fallback note) |

### 6.3 New risks introduced by this release

Same as surgical variant §6.3 plus:

| ID | Risk | Sev | Like | Mitigation |
|----|------|-----|------|------------|
| RK-C-1 | TU-007 LW-source-verification investigation could uncover a 7- or 8-condition canonical list. | Low | Medium | Parameterized tests handle any count; investigation outcome dictates final list. |
| RK-C-2 | DEFER-GATED candidates (TU-002, Q1, Q2, SE-006) become permanently deferred if their gating investigations are never funded. | Medium | Medium | The contingent variant **commits** to a follow-on release (R3) for the DEFER-COUPLED + DEFER-GATED bundle. The investigation tasks (A-005, Q3 confirmation, RK-OOS-3) are added to backlog with explicit owners. |
| RK-C-3 | Multiple deprecation announcements in one release (TU-001 + TU-004 + TU-007 + SE-001 + SE-002/003) may overwhelm users. | Low | High | Single consolidated `docs/migration/v3.75.md` document. Release notes lead with the migration guide pointer. |
| RK-C-4 | Audit log infrastructure ships in R1; performance impact untested on hot path. | Low | Low | Mirror unification variant: append-only JSON, benchmark in pre-merge perf gate. |

All FINAL-REPORT §7 risks (RK-01..RK-18, RK-OOS-1..3, RK-TUI-01..05) inherited.

### 6.4 Risk-budget reasoning

The contingent variant accepts:
- **More risk** than surgical (TU-007 LW-source-verification, audit log infrastructure shipped now, paired SE-002+SE-003).
- **Less risk** than unification (no TU-002 routing change, no TU-005/TU-006 SoT consolidation, no Q1/Q2 renames).

Decision rule: ship every candidate whose decision dimensions clear (low-or-medium coupling, deprecation-runway-addressable break, and no unresolved gate). DEFER everything else with explicit gating conditions documented.

---

## 7. Release split (Q8 commitment, §9.3)

### 7.1 Two-release proposal (immediate) + future release plan

**R1: Task-surface rigor (this release)**
- TU-001, TU-003, TU-004, TU-007 (post-verification).
- Audit log infrastructure.
- Migration guide.

**R2: Sprint-runtime + TUI (this release, sibling to R1)**
- SE-001, SE-002+SE-003 (paired, conditional on Wave-4 parser), SE-004, SE-005.
- TUI top-5 in ship order (P-05 → P-02 → P-03+P-07 → P-01).

**R3: Deferred structural release (future)**
- TU-002, TU-005, TU-006, Q1, Q2 — once Q3 confirmed and A-005 investigation complete.

**R4: SE-006 (later)**
- Once RK-OOS-3 (diagnostic-chain hardening) closes.

### 7.2 Why this split shape

- **R1 ⊥ R2** sibling structure mirrors v3.7's R1+R2 split (FINAL-REPORT §9.3 reference). Different reviewer pools, different blast radii, different test surfaces.
- **R3 is explicitly planned**, not just punted. The contingent variant **commits** to R3 by adding backlog tasks for A-005, Q3 confirmation, and the Q1/Q2 cleanup PRs.
- **R4 is a single-candidate release** because SE-006 is the only DEFER-GATED candidate that isn't naturally bundled with R3.

### 7.3 Release-split protocol invocation

Per Q8 + FINAL-REPORT §9.3: **invoke `sc-release-split-protocol`** to verify the R1+R2 split for this release. Per the contingent variant's decision rule: **adopt the protocol's recommendation** even if it differs from this proposal.

If the protocol suggests a different split shape (e.g., single combined release):
- Re-evaluate each ADOPT-WITH-DEPRECATION verdict against the new shape.
- DEFER-GATED verdicts are unaffected (they depend on investigations, not split shape).
- TUI top-5 ship order is unaffected.

---

## 8. Open questions (carried from FINAL-REPORT §8, plus contingent-specific gates)

### 8.1 FINAL-REPORT §8 resolution status in this release

| Q | Recommendation | Status this release | Status this variant |
|---|----------------|---------------------|---------------------|
| Q1 | DEFER | DEFERRED | **DEFER-GATED on A-005**; future R3 with shim |
| Q2 | DEFER | DEFERRED | **DEFER-GATED on A-005**; future R3 |
| Q3 | (a) modifier | DEFERRED (TU-002 not adopted) | **GATE for TU-002**; must confirm Q3 (a) before TU-002 ships |
| Q4 | (a)+(c) | NOT APPLICABLE | n/a (TU-002 deferred) |
| Q5 | (a)+(b) | ADOPTED in §3.5 | **(a)+(b) ADOPTED** |
| Q6 | (c) | ADOPTED in §3.5 | **(c) ADOPTED** |
| Q7 | (a) SoT | DEFERRED (TU-005) | **GATE for TU-005**; ship in R3 |
| Q8 | YES, split | ADOPTED (§7) | **ADOPTED with 2-release immediate + R3+R4 future plan** |
| Q9 | (c) map | ADOPTED in §2.3 | **(c) ADOPTED** |
| Q10 | (a) fallback | ADOPTED in §2.2 / §5.2 | **(a) ADOPTED** |
| Q11 | (a) meter | ADOPTED in §3.7 | **(a) ADOPTED** (audit log) |
| Q12 | (c) | DEFERRED (TU-005) | **GATE for TU-005** |
| Q13 | (c) | ACKNOWLEDGED | **soft prereq for R2** |
| Q14 | (c) both | ADOPTED in §3.4 | **(c) ADOPTED** |

### 8.2 Newly opened (gating conditions)

These investigations / clearances must complete before the DEFER-GATED candidates can ship:

- **A-005 investigation** — enumerate `/sc:forensic` consumers of `--caller task-unified` and the `SC:TASK-UNIFIED:CLASSIFICATION` sentinel. **Owner:** backlog. **Gates:** Q1, Q2.
- **Q3 confirmation** — confirm the output-type-tier precedence rule (recommendation (a) modifier). Could be a one-meeting decision; not a long investigation. **Gates:** TU-002.
- **RK-OOS-3 clearance** — `run_diagnostic_chain()` hardened to sprint-context input. **Gates:** SE-006.
- **TU-007 LW-source verification** — confirm the six-condition completion checklist. **Pre-merge blocker for THIS release** (not deferred).

### 8.3 Decision-rule rationale

The contingent variant's decision rule:

> Ship a candidate if and only if:
> - Coupling is LOW or MEDIUM, AND
> - Behavioral break is either absent OR addressable via deprecation runway / migration guide, AND
> - Investigation gate is either absent OR will be cleared pre-merge.

Otherwise: DEFER (gated, coupled, or deferred-with-explicit-future-release).

This rule produces the candidate distribution in §1.3. Re-running the rule with updated conditions (e.g., A-005 investigation complete) will reshape the verdict matrix and the next release's scope.

---

## 9. Acceptance criteria

This release ships when:

1. **All §5.1 + §5.2 + §5.4 + §5.5 + §5.6 tests pass.**
2. **TU-007 LW-source verification complete** (`docs/tu-007-completion-checklist-verification.md` published).
3. **Regression baselines green** (921 / 125 / 16 / +3 Wave-4 / TEST-SPEC.md:34-80).
4. **Migration guide published** (`docs/migration/v3.75.md`) with one entry per ADOPT-WITH-DEPRECATION candidate.
5. **Release notes** cover:
   - Behavioral changes (TU-001, TU-004, TU-007, SE-001).
   - Migration guide pointer.
   - Carry-over preservation explanation (DEFER-GATED on A-005).
   - DEFER-GATED future-release plan (R3 + R4) with named investigations.
6. **Audit log infrastructure deployed.**
7. **Backlog tasks created** for:
   - A-005 forensic-consumer investigation.
   - Q3 output-type-precedence confirmation.
   - RK-OOS-3 diagnostic-chain hardening.
8. **If R2 (sprint+TUI) ships paired with R1:**
   - Wave-4 parser tests pass.
   - `test_monitor_reset_between_tasks.py` passes (P-01 mitigation).
   - SE-002+SE-003 paired PR is single artifact.

---

## 10. Coverage notes

- **All 11 FINAL-REPORT sections incorporated:**
  - §1 Scope (→ §1 here, with per-candidate verdict matrix).
  - §2 Sources (referenced throughout; specific citation in §3.x).
  - §3 task-unified inventory (→ §1.2 verdict-matrix rows TU-NNN).
  - §4 /sc:task inventory (preserved in §2.1, §2.2; surface diff in §2.4).
  - §5 Overlap matrix (drove §1.2 ADOPT/DEFER classification for ALL O1-O47 rows).
  - §6 Best-of-breed candidates (full slate evaluated in §1.2 decision tree).
  - §7 Risks (inherited in §6.4; plus new RK-C-1..4).
  - §8 Open questions (full resolution table in §8; new gating conditions in §8.2).
  - §9 Prior-art constraints (hard constraints in §4.1; non-goals in §1.5).
  - §10 Shared assumptions (A-005 promoted to gating investigation in §8.2; A-001..A-004 acknowledged but not promoted).
  - §11 TUI bundle (→ §1.2 verdict rows for P-01..P-07; §5.4 mandatory tests).
- **Hard constraint compliance:** `/sc:task` only canonical command name; N1-N12 green; carry-overs preserved verbatim until A-005 clears; no `task-unified` reintroduction.
- **`[inference]` callouts:** All FINAL-REPORT `[inference]` tags propagated. Specific to this variant:
  - TU-007 six-condition list is `[inference]` until verification completes (§3.6 KNOWN GAP).
  - TU-004 behavioral break impact estimate (§6.3 RK-C-3 high-likelihood claim).
  - R3+R4 timeline implicit; no SLA given.

**Variant signature:** Per-candidate decision tree with explicit dimensions (coupling, break, gate). Mixed ADOPT / ADOPT-WITH-DEPRECATION / ADOPT-WITH-INVESTIGATION / ADOPT-WITH-MITIGATION / DEFER-GATED / DEFER-COUPLED. Two-release immediate (R1+R2). Future R3 (deferred bundle) and R4 (SE-006) explicitly planned, not punted. Q1/Q2 deferred on A-005. TU-007 LW-source-verification is a pre-merge gate.
