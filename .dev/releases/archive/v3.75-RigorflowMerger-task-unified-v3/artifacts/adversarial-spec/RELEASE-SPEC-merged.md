<!-- Provenance: This document was produced by /sc:adversarial Mode B. -->
<!-- Base: Variant C (sonnet:analyzer — contingent decision-tree, combined score 0.890). -->
<!-- Overlays: Variant A (opus:architect — surgical) for preservation test, user-impact framing, no-new-flags stance. -->
<!-- Overlays: Variant B (opus:architect — full unification) for break-rejection criterion, deferred-risks distillation, three-release effort estimates, Annexes B+C as R3 reference. -->
<!-- Adversarial synthesis: §1.7 "Considered and not adopted"; INV-002 / INV-005 mitigation notes; §9 invariant-gate reference. -->
<!-- Convergence: 86.8% over 38 diff points (threshold 0.85). Status: CONVERGED. -->
<!-- Merge date: 2026-05-14 -->

# RELEASE SPEC — v3.75 RigorflowMerger / task-unified-v3 (Merged)

**Method.** This spec is produced by per-candidate decision-tree evaluation. For each FINAL-REPORT best-of-breed candidate, we evaluate against three dimensions — (coupling, behavioral break, investigation gate) — and route to one of six verdicts. The output is a ship list plus a structured deferral list with named gates. The decision rule is re-runnable for future merge proposals.

**Source.** FINAL-REPORT.md (11 sections, including §10 Shared Assumptions and §11 TUI Improvement Bundle). All decisions trace to FINAL-REPORT line references and to debate-transcript.md diff points.

<!-- Source: Base (original, modified) — TL;DR + decision-tree framing per Variant C; methodology paragraph polished per Change #12 -->

---

## 1. Release identity & scope

### 1.1 Name and version

- **Release ID:** `v3.75-RigorflowMerger-task-unified-v3`
- **Version bump:** `version: "2.0.0"` → `version: "2.2.0"`. Minor bump signals "behavioral changes are present but gated by runway." (3.0.0 considered and rejected per Rejection #3 in refactor-plan.md — major bump premature when v3.75's actual breaks are limited migration-guide-addressable runways.)
- **Surface affected:** `/sc:task` command file, `sc-task-protocol` skill, `cli/sprint/` runtime, TUI rendering — but **per-candidate** based on the decision tree below.

### 1.2 In-scope (TL;DR + per-candidate decision tree)

**TL;DR (ships in v3.75):**
- Task-side: TU-001, TU-003, TU-004, TU-007.
- Sprint-side: SE-001, SE-002+SE-003 paired, SE-004, SE-005.
- TUI bundle: top-5 (P-05, P-02, P-03, P-07, P-01) in ship order.
- Audit log infrastructure (Q11).

**Deferred to R3 (future structural-consolidation release):** TU-002, TU-005, TU-006, Q1, Q2.
**Deferred to R4 (later, single-issue):** SE-006.

**Per-candidate decision tree (full):**

| Candidate | Coupling | Break? | Gate | Verdict | Rationale |
|-----------|---------:|:------:|:----:|---------|-----------|
| TU-001 (CRITICAL FAIL) | LOW | Yes (STRICT only) | None | **ADOPT-WITH-DEPRECATION** | STRICT-only additive enforcement; migration guide entry. |
| TU-002 (output-type axis) | HIGH | Yes (routing) | **Q3** (precedence) | **DEFER-COUPLED with R3** | Q3 precedence rule + TU-005 SoT must land together. Annex B preserves the design. |
| TU-003 (six principles) | LOW | No | None | **ADOPT** | NFR addition; no flag or behavior change. R4 L77: "agent instruction addition; no code changes." |
| TU-004 (BLOCKED state) | MEDIUM | Yes (header schema) | **Q5** + **Q6** | **ADOPT-WITH-DEPRECATION** | Q5 & Q6 recommendations adopted (CLI prompt + inline header; `--skip-compliance --reason "..."` override). |
| TU-005 (SoT YAML) | HIGH | No (internal) | **Q7** + **Q12** | **DEFER-COUPLED with R3** | Bundled with TU-006 and TU-002. Annex B preserves YAML schema. |
| TU-006 (skill sub-files) | MEDIUM | No | **Q7** + **Q8** | **DEFER-COUPLED with R3** | Bundles naturally with TU-005. Annex C preserves directory tree. |
| TU-007 (completion checklist) | LOW | Yes (TFEP gate) | **A-004** (six-condition list verification) | **ADOPT-WITH-INVESTIGATION** | Pre-merge LW-source verification produces canonical list; parameterized tests handle any count. |
| SE-001 (fail-closed gate) | LOW | Yes (sprint side) | None | **ADOPT** | R3 L34 "Low. Edge case for empty output files." |
| SE-002 (per-task UID) | MEDIUM | Yes (result files) | **Q10** (migration) | **ADOPT-WITH-DEPRECATION** | Graceful fallback per Q10 (a). Paired with SE-003. |
| SE-003 (sub-phase resume) | MEDIUM | Yes (prompt) | **RK-15** (Wave-4 parser) | **ADOPT-WITH-DEPRECATION** | Must re-run Wave-4 parser tests pre-merge. Paired with SE-002. |
| SE-004 (ExecutionMode) | LOW | No | None | **ADOPT** | Enum addition; no behavior change. |
| SE-005 (GateFailureSeverity) | LOW | No | **Q9** (scope) | **ADOPT** | Q9 (c) (map TFEP → Sev) — reporting taxonomy only. |
| SE-006 (auto-diagnostic threshold) | MEDIUM | Yes (new path) | **RK-OOS-3** (diagnostic-chain hardening) | **DEFER-GATED to R4** | Ship after diagnostic chain hardened. |
| Q1 (sentinel rename) | LOW | Yes (string) | **A-005** | **DEFER-GATED to R3** | A-005 forensic-consumer investigation must complete. |
| Q2 (forensic-caller rename) | LOW | Yes (string) | **A-005** | **DEFER-GATED to R3** | Same A-005 gate as Q1. |
| TUI P-01 (OutputMonitor wiring) | HIGH | No | **INV-001/005** | **ADOPT-WITH-MITIGATION** | Mandatory test `test_monitor_reset_between_tasks.py` (FINAL-REPORT §11.3). |
| TUI P-02, P-03, P-05, P-07 | LOW-MED | No-Low | None | **ADOPT** | Per FINAL-REPORT §11 top-5. |

### 1.3 Verdict counts

- ADOPT (clean): **8** — TU-003, SE-001, SE-004, SE-005, TUI P-02/P-03/P-05/P-07.
- ADOPT-WITH-DEPRECATION: **4** — TU-001, TU-004, SE-002, SE-003.
- ADOPT-WITH-INVESTIGATION: **1** — TU-007.
- ADOPT-WITH-MITIGATION: **1** — TUI P-01.
- DEFER-COUPLED (to R3): **3** — TU-002, TU-005, TU-006.
- DEFER-GATED: **3** — Q1, Q2 (to R3 on A-005), SE-006 (to R4 on RK-OOS-3).

### 1.4 Out-of-scope (non-goals, hard constraints from v3.7)

- **NG-1.** Reintroduce `/sc:task-unified` as a live command. **v3.7 hard constraint.**
- **NG-2.** Resurrect `task-unified.md` or `sc-task-unified-protocol/` directories.
- **NG-3.** Replace IC's keyword-based classifier with semantic NLP.
- **NG-4.** Adopt LW's bash-orchestrator / Python-from-bash / multi-backup patterns.
- **NG-5.** TypeScript plugin work (v5.0 scope).

### 1.5 Release-split outcome

Per FINAL-REPORT §9.3 (Q8 commitment): **YES, apply the release-split protocol**. The decision tree produces:

- **R1 (this release, task-surface):** TU-001, TU-003, TU-004, TU-007 (post-verification).
- **R2 (this release, sprint-runtime + TUI; sibling to R1):** SE-001, SE-002+SE-003 paired, SE-004, SE-005 + TUI top-5.
- **R3 (future, structural-consolidation; target within 2 release cycles, i.e., by v3.85 or v3.9):** TU-002, TU-005, TU-006, Q1, Q2 — once Q3 confirmed and A-005 investigation complete.
- **R4 (later, single-issue; target after RK-OOS-3 clears; no later than v3.9):** SE-006.

R1 ⊥ R2 (siblings; can ship in parallel). R3 depends on investigations clearing. R4 depends on RK-OOS-3 clearing. Target windows are **soft** (not SLAs); they constrain "future" from being "any time" to "within ~6-12 months."

### 1.6 Considered and not adopted (transparency)

The adversarial review considered an alternative full-slate position (all TU-001..007 + SE-001..006 + Q1+Q2 renamed with shim + new `--output-type` flag + 3.0.0 major version bump) and rejected it. Specifically:

- **Full TU-002 + TU-005 + TU-006 in v3.75:** Rejected on X-001..X-003 consensus (80% confidence). Combined complexity exceeds the convergence margin's risk budget. Annex B (YAML schema) and Annex C (sub-file tree) preserve B's concrete designs for R3 release-planning.
- **Q1 + Q2 renames with telemetry-compat shim in v3.75:** Rejected on X-002 consensus (80% confidence). A-005 forensic-consumer investigation is unresolved; defer until cleared.
- **New `--output-type {auto|override}` CLI flag:** Rejected on C-012/X-005 consensus (80% confidence). Flag surface stays at 8.
- **3.0.0 major version bump:** Rejected on C-013 (60% confidence). v3.75's actual breaks are limited migration-guide-addressable runways; 3.0.0 belongs with R3.
- **SE-006 auto-diagnostic threshold:** Rejected on X-006 consensus (80% confidence). RK-OOS-3 (diagnostic-chain hardening) unresolved.

The full-slate position is preserved in this artifact as a documented alternative for future re-evaluation. If A-005, Q3, and RK-OOS-3 all clear, the decision tree should be re-run and R3 (plus R4) can ship the deferred candidates.

<!-- Source: Variant C (base) for §1.1-§1.5; Change #10 (Considered and not adopted §1.6); Change #11 (R3 narrative with B effort estimates: R1 3-5 days, R2 7-10 days, R3 5-7 days) -->

---

## 2. Surface contract (per-candidate)

### 2.1 Stays unchanged

- Command name `/sc:task`.
- All **8 CLI flags** (no new flag this release): `--strategy, --compliance, --verify, --skip-compliance, --force-strict, --parallel, --delegate, --no-escalation`.
- Strategy axis (`systematic, agile, enterprise, auto`).
- Compliance tier values (`strict, standard, light, exempt`).
- Verification axis (`critical, standard, skip, auto`).
- Carry-over strings (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->`, `--caller task-unified`) — preserved verbatim because Q1/Q2 are DEFER-GATED on A-005.

### 2.2 Changes (per-candidate, with runway label)

| Candidate | Change | Behavioral break | User-visible? | Runway |
|-----------|--------|------------------|---------------|--------|
| TU-001 | STRICT tasks unconditionally FAIL on (a) MCP missing, (b) empty output, (c) missing header. | Yes (STRICT only). | Yes. | Migration guide entry; no shim needed. |
| TU-004 | Low-confidence soft prompt becomes deterministic BLOCKED state. Header TIER enum extends to include `BLOCKED`. | Yes (5-10% of `--compliance auto` users, `[inference]`). | Yes (clearer error message; explicit re-invocation required). | Migration guide entry; `--skip-compliance --reason "..."` is the documented override. |
| TU-007 | Completion checklist becomes a hard gate (canonical condition count from LW-source verification). | Yes (STRICT/STANDARD tasks returning `complete` despite gaps now block). | Yes (more diagnostic information). | Migration guide entry; net positive expected. |
| SE-001 | Empty output → `(False, 'empty output file')` instead of soft PASS. | Yes (sprint runs relying on inconclusive PASS will fail). | Yes (sprint owners see new failures). | Migration guide entry. |
| SE-002+SE-003 | Per-task UID + sub-phase resume. Result file format extended (additional `task_uid` field). | No (additive; graceful fallback per Q10 (a)). | Only when resuming; faster when UIDs present. | None needed (fallback covers legacy). |
| Q1 / Q2 (DEFERRED) | n/a — explicitly preserved verbatim. | n/a | n/a | n/a |

### 2.3 Additions (no break, additive)

- TU-001 `CriticalFailCondition` dataclass.
- TU-003 NFR section + checklist + prompt binding (Q14 (c) both).
- TU-004 `TIER: BLOCKED` value in header schema (additive enumeration).
- SE-004 `ExecutionMode` enum.
- SE-005 `GateFailureSeverity` enum (Q9 (c) map TFEP → Sev).
- Audit log infrastructure (Q11 (a)) — `audit.py` module with daily-rotated JSONL.
- TUI P-series fixes (P-01 mandatory test ships alongside it).

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

  Completion checklist (NEW, gated on LW-source verification):
+   Canonical condition count before `complete` status (TU-007)

  Sprint runtime (R2):
+   ExecutionMode enum, GateFailureSeverity enum, task_uid field, sub-phase resume
+   Fail-closed empty-output gate

  TUI (R2):
+   Spinner on RUNNING (P-05), elapsed-since-phase-start Duration (P-02),
+   width-aware truncation (P-03+P-07), OutputMonitor wired into per-task path (P-01)

  Carry-overs (DEFERRED to R3):
    SC:TASK-UNIFIED:CLASSIFICATION sentinel — preserved verbatim
    --caller task-unified — preserved verbatim
```

<!-- Source: Variant C (base) — §2.1-§2.4 retained; "no new flags" stance reinforced per Change #3 -->

---

## 3. Protocol changes (sc-task-protocol skill)

### 3.1 Scope of edits

All task-side protocol changes are confined to **`src/superclaude/skills/sc-task-protocol/SKILL.md`** plus new sibling `audit.py`. **No sub-directory restructure** (TU-006 deferred to R3; Annex C preserves the future layout).

### 3.2 New sections added to SKILL.md

In order of insertion:

1. **§2.5 CRITICAL FAIL conditions (TU-001)** — between current §2 (entry rule) and §3 (MCP requirements).
2. **§3.5 Quality Principles NFR (TU-003)** — at end of current §3.
3. **§8 Mandatory completion checklist (TU-007)** — new top-level section.

Sections renumbered as needed.

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

Decision rule for future additions: any new condition must be deterministic,
applicable only to STRICT, and have a non-recoverable failure mode.

Implementation: CriticalFailCondition dataclass in audit.py:
  @dataclass
  class CriticalFailCondition:
      condition_type: str
      description: str
      always_blocks: bool = True
```

### 3.4 Quality Principles NFR (TU-003)

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

Enforcement: prompt + checklist (Q14 (c) both).
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

Release-boundary note (INV-002 mitigation): Tasks initiated before TU-004
deployment continue under their original classification. The BLOCKED state
applies only to tasks initiated after deployment. No in-flight reclassification
occurs.
```

### 3.6 Completion checklist (TU-007) — ADOPT-WITH-INVESTIGATION

```
### Mandatory completion checklist (TU-007)

Before any task may return `complete`, the canonical condition set must be met.

KNOWN GAP: The condition list is `[inference]` per FINAL-REPORT §6.1 — R2 L85
does not enumerate the conditions verbatim. The implementation phase must
consult the original LW source and verify the canonical list before merge.
The condition list below is a working placeholder, not a final list.

Working placeholder (subject to LW-source verification):
1. All affected files have been identified and updated.
2. All tests pass (or manual verification documented for STANDARD/LIGHT).
3. No pre-existing test failures introduced.
4. No new contradictions or invariants violated.
5. Adversarial verification (STRICT) returned a non-FAIL verdict.
6. think_about_whether_you_are_done confirms completion.

Pre-merge gate: The LW-source-verification investigation completes and either
(a) confirms this list matches the original, or (b) supplies the canonical list,
which replaces this one. NO MERGE until this investigation is complete.

Test approach (V-C §5.3 parameterized): tests/skills/test_task_completion_checklist.py
parameterizes over the canonical list. If the canonical list has 5 / 6 / 7 / 8
conditions, the test suite handles it without re-architecting.
```

### 3.7 Audit log infrastructure (Q11)

New file: `src/superclaude/skills/sc-task-protocol/audit.py`.

The audit log serves three downstream goals:
1. TU-001 audit trail.
2. TU-004 BLOCKED override audit (per Q6 (c)).
3. Q11 `--skip-compliance` metering.

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

**Concurrency contract (INV-005 mitigation):** Audit log writes within a single task lifecycle MUST be serialized through a single writer. Ordering is preserved per-task, not globally. Implementation: `audit.py` uses a per-task write lock; cross-task ordering is timestamp-based but not strictly serial.

<!-- Source: Variant C (base) — §3.1-§3.7 retained verbatim from C; INV-002 mitigation appended to §3.5 per Change #8; INV-005 contract appended to §3.7 per Change #9 -->

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
| TU-007 completion checklist (post-LW-verification) | INTRODUCED | n/a |
| Q1 sentinel rename | **NOT INTRODUCED** (DEFER-GATED on A-005) | R3 with shim |
| Q2 forensic-caller rename | **NOT INTRODUCED** (DEFER-GATED on A-005) | R3 with shim |

### 4.3 Future R3 deprecation policy (informational, for R3 planning)

When R3 ships Q1/Q2 renames and the TU-002/005/006 bundle, the deprecation runway pattern is:

- **R3 v1:** Emit new strings + accept both old and new in parsers (compat shim).
- **R3 v2 (or v3.8):** Remove old strings from parsers.

R3 inherits Annex B (YAML schema) and Annex C (sub-file tree) as starting designs.

### 4.4 Break-rejection criterion

A proposed behavioral break is **rejected** (not adopted-with-deprecation) if any of:

1. It cannot be made backward-compatible via a 1-release shim.
2. Its migration cost on the most-affected user cohort exceeds 1 hour of work.
3. It depends on an unresolved investigation (DEFER-GATED in the decision-tree).

The criterion applies to candidate evaluation in this release **and** future releases. It is intended as a stable test that distinguishes ADOPT-WITH-DEPRECATION from DEFER-GATED.

<!-- Source: Variant C (base) — §4.1-§4.3 retained from C; §4.4 break-rejection criterion adopted from Variant B per Change #4 -->

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

### 5.2.5 Canonical-form-agnostic sentinel preservation (Q1/Q2 DEFER lock)

- `tests/skills/test_classification_sentinel_canonical.py`
  - `test_sentinel_present_and_canonical`:
    ```python
    def test_sentinel_present_and_canonical():
        """Asserts the sentinel exists; canonical form read from SoT constant."""
        sentinel = read_canonical_sentinel_const()
        assert sentinel in classification_header_output()
        assert sentinel.startswith("<!-- ")
        assert sentinel.endswith("-->")
    ```
- `tests/skills/test_tfep_caller_canonical.py`
  - `test_caller_string_is_canonical`:
    ```python
    def test_caller_string_is_canonical():
        """Asserts the forensic caller string matches the canonical form."""
        caller = read_canonical_caller_const()
        assert f"--caller {caller}" in tfep_forensic_invocation_string()
    ```

**Rationale:** These tests encode the v3.75 DEFER decision in CI without asserting the literal `task-unified` substring. When R3 renames Q1/Q2, only the `SoT` constants update; the tests remain valid. Prevents accidental removal of the carry-overs in v3.75; survives the eventual rename in R3.

### 5.3 ADOPT-WITH-INVESTIGATION (TU-007)

The pre-merge investigation is the test:
- **Investigation:** Verify the completion-checklist conditions against the original LW source.
- **Artifact:** `docs/tu-007-completion-checklist-verification.md` documenting the LW source citation and the canonical condition list.
- **Test:**
  - `tests/skills/test_task_completion_checklist.py`
    - One parameterized test per condition, parameter list from `docs/tu-007-completion-checklist-verification.md`.
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
  - `test_audit_log_per_task_writes_serialized` (INV-005)

### 5.6 Regression tests

From v3.7-task-unified-v2 (FINAL-REPORT §9.5):
- Sprint full run: **921 passed, 57 failed baseline** — new failures must be net-new.
- TUI Waves 1-2 + tmux + summarizer + retrospective: **125/125 pass.**
- `test_process.py::TestClaudeProcess`: **16/16** including `test_build_prompt_contains_task_command`.
- `TEST-SPEC.md:34-80`: no `/sc:task-unified` strings.
- Wave-4 checkpoint heading parser: **+3 tests must pass** (RK-15).

### 5.7 Coverage target

- **80% line coverage** on all new code (TU-001, TU-003, TU-004, TU-007, audit.py, SE-001..005).
- **100% on `audit.py`** (security-sensitive write path).
- **No coverage requirement** on canonical-form-agnostic preservation tests (existence checks).

<!-- Source: Variant C (base) — §5.1-§5.7 retained; §5.2.5 canonical-form-agnostic preservation test pattern adopted from Variant A R2 concession per Change #1 -->

---

## 6. Backward compatibility & risk

### 6.1 Compat guarantees

- **Command name `/sc:task`** — unchanged.
- **CLI flag count: 8 flags. No new flags added this release.** (TU-002's `--output-type` is deferred to R3 per Change #3 / Rejection #2.)
- **Classification header schema** — extended (BLOCKED added) but not changed for existing tiers.
- **Skill file structure** — unchanged (no sub-directories; TU-006 deferred to R3; Annex C preserves the future layout).
- **Carry-over telemetry strings** — preserved verbatim in their current form.

### 6.2 Behavioral breaks (with migration-guide pointer)

| Item | Migration guide entry |
|------|------------------------|
| TU-001 (STRICT empty output → FAIL) | docs/migration/v3.75.md#tu-001 |
| TU-001 (STRICT missing header → FAIL) | docs/migration/v3.75.md#tu-001 |
| TU-004 (low-confidence BLOCKED) | docs/migration/v3.75.md#tu-004 |
| TU-007 (completion checklist) | docs/migration/v3.75.md#tu-007 |
| SE-001 (empty output gate) | docs/migration/v3.75.md#se-001 |
| SE-002+SE-003 (UID + resume) | docs/migration/v3.75.md#se-002-se-003 (graceful-fallback note) |

### 6.3 New risks introduced by this release

| ID | Risk | Sev | Like | Mitigation |
|----|------|-----|------|------------|
| RK-NEW-1 | TU-004 BLOCKED adds `BLOCKED` to TIER enum — downstream parsers may not handle it. | Medium | Low | Add `BLOCKED` to all known parsers; grep `STRICT\|STANDARD\|LIGHT\|EXEMPT` regex; update each. |
| RK-NEW-2 | TU-001 #3 (missing classification header) may false-positive during early-development sessions. | Low | Medium | STRICT only; document workaround `--skip-compliance --reason "header-development"`. |
| RK-NEW-3 | TU-007 condition list is `[inference]`; implementation may discover a different canonical list. | Medium | Medium | Parameterized tests handle any count; investigation outcome dictates final list. |
| RK-NEW-4 | Q11 audit log adds an I/O write path; could be I/O-sensitive in tight loops. | Low | Low | Append-only JSONL; per-task lock (INV-005); benchmark in pre-merge perf gate. |
| RK-NEW-5 | DEFER-COUPLED / DEFER-GATED candidates may become permanently deferred if their gating investigations aren't funded. | Medium | Medium | Backlog tasks committed for A-005, Q3 confirmation, RK-OOS-3 (§9 acceptance criterion). Soft target windows for R3 and R4. |

#### Risks for deferred R3 work (informational; not in v3.75 scope)

These risks are carried from Variant B's analysis as a starting inventory for R3 planning. They DO NOT apply to v3.75.

| ID | Risk | Mitigation (for R3) |
|----|------|---------------------|
| RK-R3-1 (was RK-U-1) | TU-002 routing reclassifies historically-STRICT doc tasks to lower scrutiny. | Stage rollout behind `--output-type auto` default; emit before/after tier in header. |
| RK-R3-2 (was RK-U-2) | YAML SoT (TU-005) adds load-time dependency; malformed YAML → every invocation fails. | CI YAML schema validation; frozen baseline; `make verify-sync` checks round-trip. |
| RK-R3-3 (was RK-U-3) | Q1/Q2 partial unification if A-005 finds a hidden consumer. | A-005 investigation is pre-merge blocker for Q1/Q2 only; rest of R3 unaffected. |
| RK-R3-4 (was RK-U-4) | TU-006 sub-file materialization expands CI sync surface. | Update `make sync-dev` allowlist; add `test_verify_sync_handles_subfiles`. |
| RK-R3-5 (was RK-U-5) | Widened STRICT keyword set may spike STRICT classifications by 15-30% `[inference]`. | 1-week soft-launch window with MIGRATION: warning; full enforcement after window. |
| RK-R3-6 (was RK-U-6) | TU-002 + TU-005 + TU-006 PR ordering creates merge conflicts. | Sequential 3-PR delivery: TU-006 → TU-005 → TU-002. |

All FINAL-REPORT §7 risks (RK-01..RK-18, RK-OOS-1..3, RK-TUI-01..05) inherited.

### 6.4 Inherited risks (FINAL-REPORT §7, summarized)

Applies without modification:
- **RK-05** Classification logic duplication / drift — acknowledged but unresolved this release (TU-005 deferred to R3).
- **RK-10** Naming-artifact telemetry-compat — explicitly preserved verbatim (Q1/Q2 deferred to R3).
- **RK-15, RK-16** Wave-4 parser regression + unvalidated live sprint execution — prerequisites for shipping SE-002+SE-003 (paired) and the R2 sprint-side bundle.

### 6.5 User-facing impact summary

| Change | What users see | Mitigation |
|--------|----------------|------------|
| TU-004 BLOCKED | Tasks with ambiguous keyword classification (~5-10% of historical traffic, `[inference]`) will halt where they previously auto-classified. | Release notes call this out; `--compliance auto` users see the change first. Clear error message points to `--compliance <tier> --reason "..."` or `--skip-compliance --reason "..."`. |
| TU-001 STRICT output absent | STRICT tasks that previously completed with empty output (likely buggy completions) will now FAIL. | Expected net positive; users with legitimate "no-output" STRICT tasks should reclassify to EXEMPT. |
| TU-007 completion checklist | STRICT/STANDARD tasks that previously returned `complete` despite gaps will now block. | Expected net positive; document the canonical condition list in release notes. |
| SE-001 empty output gate | Sprint runs that previously soft-passed on empty output will now fail-closed. | Sprint owners should expect 1-2 new failures per phase during the first week; classify each as pre-existing or net-new. |

<!-- Source: Variant C (base) — §6.1-§6.4 retained from C; §6.3 deferred-R3 sub-table adopted from Variant B (RK-U-1..6 → RK-R3-1..6) per Change #7; §6.5 user-facing impact summary adopted from Variant A §6.2 pattern per Change #2; "no new flags" assertion in §6.1 per Change #3 -->

---

## 7. Release split (Q8 commitment, §9.3)

### 7.1 Four-stage plan (2 immediate + 2 future)

**R1: Task-surface rigor (this release)**
- TU-001, TU-003, TU-004, TU-007 (post-verification).
- Audit log infrastructure.
- Migration guide.
- Canonical-form-agnostic preservation tests.
- **Effort:** ~3-5 dev-days `[inference]` (sum of 1×M + 3×S).

**R2: Sprint-runtime + TUI (this release, sibling to R1)**
- SE-001, SE-002+SE-003 (paired, conditional on Wave-4 parser passing), SE-004, SE-005.
- TUI top-5 in ship order (P-05 → P-02 → P-03+P-07 → P-01).
- **Effort:** ~7-10 dev-days `[inference]`.

**R3: Structural-consolidation release (future)**
- TU-002 (output-type axis using Annex B detection rules + gate tables).
- TU-005 (SoT YAML using Annex B schema).
- TU-006 (skill sub-files using Annex C tree).
- Q1 (sentinel rename) — post-A-005.
- Q2 (forensic-caller rename) — post-A-005.
- **Effort:** ~5-7 dev-days `[inference]`.
- **Target window:** within 2 release cycles of v3.75 (i.e., by v3.85 or v3.9).

**R4: SE-006 (later)**
- Auto-diagnostic threshold flag.
- **Effort:** ~1-2 dev-days `[inference]`.
- **Target window:** after RK-OOS-3 (diagnostic-chain hardening) clears; no later than v3.9.

**Total effort for v3.75 (R1+R2):** ~10-15 dev-days. Compatible with one sprint. `[inference]`

### 7.2 Why this shape

- **R1 ⊥ R2** sibling structure mirrors v3.7's R1+R2 split (FINAL-REPORT §9.3 reference). Different reviewer pools, different blast radii, different test surfaces.
- **R3 is explicitly planned** with named investigation prerequisites (A-005, Q3) and a soft target window. Not punted.
- **R4 is a single-candidate release** because SE-006 isn't naturally bundled with R3.
- **R3 dependencies on R1 and R2:** TU-002's gate tables reference TU-001's CRITICAL FAIL hooks; TU-002 routing may consult the audit log from R1. SE-006's auto-diagnostic threshold depends on R2's SE-001..005 surfaces being stable.

### 7.3 Release-split protocol invocation

Per Q8 + FINAL-REPORT §9.3: **invoke `sc-release-split-protocol`** to verify the R1+R2 split for this release. **Adopt the protocol's recommendation** even if it differs from this proposal.

If the protocol suggests a different split shape (e.g., single combined release):
- Re-evaluate each ADOPT-WITH-DEPRECATION verdict against the new shape.
- DEFER-COUPLED and DEFER-GATED verdicts are unaffected (they depend on investigations, not split shape).
- TUI top-5 ship order is unaffected.

<!-- Source: Variant C (base) — §7.1 release-plan retained from C with target windows; effort estimates merged from Variant B's §7.1 per Change #11 (3-release narrative); §7.2-§7.3 retained from C -->

---

## 8. Open questions (FINAL-REPORT §8 resolution + gating investigations)

### 8.1 FINAL-REPORT §8 resolution status in this release

| Q | Recommendation | Status |
|---|----------------|--------|
| Q1 | DEFER-GATED to R3 on A-005 | **(c) DEFERRED**; future R3 with shim |
| Q2 | DEFER-GATED to R3 on A-005 | **(c) DEFERRED**; future R3 |
| Q3 | (a) modifier | **GATE for TU-002**; resolve in R3 release-planning |
| Q4 | (a)+(c) filename + override flag | **NOT APPLICABLE this release** (TU-002 deferred) |
| Q5 | (a)+(b) CLI prompt + inline header | **(a)+(b) ADOPTED** (§3.5) |
| Q6 | (c) yes with `--reason` + audit log | **(c) ADOPTED** (§3.5 + §3.7) |
| Q7 | (a) SoT | **GATE for TU-005**; R3 |
| Q8 | YES, apply split | **ADOPTED with R1+R2 immediate + R3+R4 future plan** (§7) |
| Q9 | (c) map TFEP → Sev | **(c) ADOPTED** (§2.3 SE-005) |
| Q10 | (a) graceful fallback | **(a) ADOPTED** (§2.2 SE-003) |
| Q11 | (a) add metering now | **(a) ADOPTED** (§3.7 audit log) |
| Q12 | (c) | **GATE for TU-005**; R3 |
| Q13 | (c) `--checkpoint-gate-mode` + live-run | **ACKNOWLEDGED**; live-run is soft prereq for R2 |
| Q14 | (c) both prompt + checklist | **(c) ADOPTED** (§3.4 + §3.7) |

### 8.2 Newly opened (gating conditions)

These investigations / clearances must complete before the deferred candidates can ship:

- **A-005 investigation** — enumerate `/sc:forensic` consumers of `--caller task-unified` and the `SC:TASK-UNIFIED:CLASSIFICATION` sentinel. **Owner:** backlog. **Gates:** Q1, Q2 (both R3).
- **Q3 confirmation** — confirm the output-type-tier precedence rule (recommendation (a) modifier). One release-planning meeting. **Gates:** TU-002 (R3).
- **RK-OOS-3 clearance** — `run_diagnostic_chain()` hardened to sprint-context input. **Gates:** SE-006 (R4).
- **TU-007 LW-source verification** — confirm the completion-checklist canonical condition list. **Pre-merge blocker for THIS release** (not deferred).

### 8.3 Decision-rule rationale

The decision rule applied to produce §1.2:

> Ship a candidate if and only if:
> - Coupling is LOW or MEDIUM, AND
> - Behavioral break is either absent OR addressable via deprecation runway / migration guide, AND
> - Investigation gate is either absent OR will be cleared pre-merge.

Otherwise: DEFER (gated, coupled, or planned-future-release).

Re-running this rule with updated conditions (A-005 cleared, Q3 confirmed, RK-OOS-3 closed) will reshape the verdict matrix and unlock the deferred candidates for R3 / R4 inclusion.

The break-rejection criterion (§4.4) distinguishes ADOPT-WITH-DEPRECATION from REJECT within the decision tree.

<!-- Source: Variant C (base) — §8.1-§8.3 retained verbatim from C; resolution table reflects merged release decisions -->

---

## 9. Acceptance criteria

This release ships when:

1. **All §5.1 + §5.2 + §5.2.5 + §5.5 + §5.6 tests pass.**
2. **§5.3 TU-007 LW-source verification complete** (`docs/tu-007-completion-checklist-verification.md` published; parameterized tests pass against canonical condition list).
3. **Regression baselines green:** 921 sprint pass / 57 fail baseline; 125/125 TUI; 16/16 ClaudeProcess; +3 Wave-4 parser; TEST-SPEC.md:34-80 (no `/sc:task-unified` in build_prompt).
4. **Migration guide published** (`docs/migration/v3.75.md`) with one entry per ADOPT-WITH-DEPRECATION candidate.
5. **Release notes** cover:
   - Behavioral changes (TU-001, TU-004, TU-007, SE-001).
   - Migration guide pointer.
   - User-facing impact summary (§6.5).
   - Carry-over preservation explanation (DEFER-GATED on A-005).
   - R3 + R4 future-release plan with named investigations and target windows.
6. **Audit log infrastructure deployed** and capturing every classification + override + escape-hatch use.
7. **Backlog tasks created** for:
   - A-005 forensic-consumer investigation.
   - Q3 output-type-precedence confirmation.
   - RK-OOS-3 diagnostic-chain hardening.
8. **R2 sprint+TUI (if shipped paired with R1):**
   - Wave-4 parser tests pass (+3 mandatory per RK-15).
   - `test_monitor_reset_between_tasks.py` passes (P-01 mitigation).
   - SE-002+SE-003 paired PR is single artifact.
9. **Convergence and invariant gates:** Adversarial pipeline at convergence 86.8% (CONVERGED). Invariant probe: 0 HIGH-severity UNADDRESSED. See `artifacts/adversarial-spec/adversarial/invariant-probe.md` for full findings.

<!-- Source: Variant C (base) — §9 retained from C; item 9 invariant-gate reference added per Change #14 -->

---

## 10. Coverage notes

- **All 11 FINAL-REPORT sections incorporated:**
  - §1 Scope (→ §1 here, with per-candidate verdict matrix).
  - §2 Sources (referenced throughout; specific citations in §3.x test list).
  - §3 task-unified inventory (→ §1.2 verdict-matrix rows TU-NNN; Annex B + Annex C preserve deferred-candidate designs).
  - §4 /sc:task inventory (preserved in §2.1, §2.2; surface diff in §2.4).
  - §5 Overlap matrix (drove §1.2 ADOPT/DEFER classification for ALL O1-O47 rows).
  - §6 Best-of-breed candidates (full slate evaluated in §1.2 decision tree).
  - §7 Risks (inherited in §6.4; new RK-NEW-1..5; deferred-R3 inventory in §6.3 sub-table).
  - §8 Open questions (full resolution table in §8.1; gating investigations in §8.2).
  - §9 Prior-art constraints (hard constraints in §4.1; non-goals in §1.4).
  - §10 Shared assumptions (A-005 promoted to gating investigation in §8.2; A-001..A-004 acknowledged).
  - §11 TUI bundle (→ §1.2 verdict rows for P-01..P-07; §5.4 mandatory tests).
- **Hard constraint compliance:** `/sc:task` only canonical command name (§4.1); N1-N12 green (§5.6 baseline); carry-overs preserved verbatim until A-005 clears (§5.2.5 canonical-form-agnostic tests); no `task-unified` reintroduction.
- **`[inference]` callouts:** All FINAL-REPORT `[inference]` tags propagated:
  - TU-007 condition list is `[inference]` until LW-source verification completes (§3.6 KNOWN GAP).
  - TU-004 behavioral break impact (5-10% estimate in §6.5).
  - Effort labels in §7 (FINAL-REPORT §10 A-003 inheritance).
  - R3+R4 target windows are soft, not SLAs (§7.1).
  - RK-R3-5 telemetry-spike 15-30% estimate (§6.3, from Variant B's RK-U-5).

**Variant signature:** Per-candidate decision tree with three dimensions and six verdict types. Mixed ADOPT / ADOPT-WITH-DEPRECATION / ADOPT-WITH-INVESTIGATION / ADOPT-WITH-MITIGATION / DEFER-COUPLED / DEFER-GATED. Two-release immediate (R1+R2) + R3 (deferred bundle with target window) + R4 (SE-006). Q1/Q2 deferred on A-005. TU-007 LW-source-verification is a pre-merge gate. Carry-overs preserved with canonical-form-agnostic tests. Break-rejection criterion documented. Annex B and Annex C preserve B's full YAML schema and sub-file tree as R3 reference content.

<!-- Source: Variant C (base) — §10 coverage notes retained from C with merged-spec provenance summary -->

---

## Annex B — R3 reference: `config/tier-keywords.yaml` schema (future, NOT shipped in v3.75)

**This annex documents the proposed schema for R3 (TU-005 single source of truth). It is NOT shipped in v3.75. It is preserved here so R3 release-planning can reference it directly.**

```yaml
tiers:
  STRICT:
    weight: 0.4
    keywords:
      - security
      - authentication
      - authorization
      - database
      - migration
      - refactor
      - breaking change
      - encrypt
      - token
      - session
      - oauth
      # Reconciled from sc-tasklist-protocol (Q12 (a) widen):
      - password
      - credential
      - secret
      - jwt
      - transaction
      - query
    compound_phrases:
      - "fix security"
      - "add authentication"
      - "update database"
      - "change api"
    boosters:
      files_gt_2: 0.3
      paths_match: ["auth/", "security/", "crypto/"]
      path_boost: 0.4
    critical_path_override: ["auth/", "security/", "crypto/", "models/", "migrations/"]

  STANDARD:
    weight: 0.2
    keywords: [implement, add, create, update, fix, build, modify, change]
    # Q12 (a) widen:
    additional_keywords: [remove, delete, deprecate]

  LIGHT:
    weight: 0.3
    keywords: [typo, comment, whitespace, lint, docstring, formatting, spacing, minor]
    compound_phrases:
      - "quick fix"
      - "minor change"
      - "fix typo"
      - "refactor comment"
      # Q12 (a) widen:
      - "small update"
      - "update comment"
      - "fix spacing"
      - "fix lint"
      - "rename variable"
    boosters:
      files_eq_1: 0.1
      lines_le_50: 0.05

  EXEMPT:
    weight: 0.4
    keywords: [explain, search, commit, push, plan, discuss, brainstorm, what, how, why]
    boosters:
      is_read_only: 0.4
      is_git_operation: 0.5
      all_doc_files: 0.5
    path_overrides:
      docs: 0.5
      md_only: 0.5

  BLOCKED:
    # Synthetic tier emitted only by TU-004 deterministic block.
    # No keyword set; produced when max(tier_scores) confidence < 0.70

priority_order: [STRICT, EXEMPT, LIGHT, STANDARD]

compound_match_boost: 0.15

confidence_thresholds:
  block_below: 0.70
  reduce_if_top_two_within: 0.1  # -0.15
  boost_compound: 0.15
  reduce_no_keywords: 0.30
  cap_max: 0.95

output_types:
  # TU-002 (R3) detection rules
  code:
    detection: [code_change, src_path]
    gates: [compile, test_required, lint]
  analysis:
    detection: [filename_contains: "comparison|analysis|report"]
    gates: [evidence_citation_required, no_lint]
  documentation:
    detection: [all_md, docs_path]
    gates: [structure_check_only, no_code_test]
  opinion:
    detection: [filename_contains: "recommendation|opinion|verdict", flag: "--output-type opinion"]
    gates: [cev_structure_required, no_automated_verification]
```

When R3 ships, all four consumers (`task.md`, `ORCHESTRATOR.md`, `sc-tasklist-protocol/SKILL.md`, `sc-tasklist-protocol/rules/tier-classification.md`) load this YAML at startup. `make sync-dev` includes the YAML in the sync target.

<!-- Source: Variant B §3.3 (full YAML schema, ~50 lines) — preserved as R3 reference per Change #5 -->

---

## Annex C — R3 reference: `sc-task-protocol/` skill sub-file layout (future, NOT shipped in v3.75)

**This annex documents the proposed directory tree for R3 (TU-006 sub-file materialization). It is NOT shipped in v3.75. It is preserved here so R3 release-planning can reference it directly.**

```
src/superclaude/skills/sc-task-protocol/
├── SKILL.md                         # Top-level protocol (R1 edits remain valid)
├── __init__.py
├── audit.py                         # R1 audit log infrastructure (already shipped)
├── refs/
│   ├── tier-classification.md       # Mirror of canonical tier logic (sourced from config/)
│   ├── output-type-detection.md     # TU-002 detection rules
│   └── critical-fail-conditions.md  # TU-001 condition catalog
├── rules/
│   ├── tier-keywords.yaml -> ../config/tier-keywords.yaml (symlink)
│   ├── critical-fail-rules.md       # TU-001 gate evaluator rules
│   ├── quality-principles.md        # TU-003 NFR text
│   └── completion-checklist.md      # TU-007 canonical condition list
├── templates/
│   ├── classification-header.md.tmpl
│   ├── blocked-header.md.tmpl
│   └── completion-report.md.tmpl
├── config/
│   └── tier-keywords.yaml           # TU-005 single source of truth (Annex B)
└── scripts/
    └── validate_classification.py   # CI helper
```

After this restructure, the `SKILL.md:359-365` references (currently broken per R7 §5 item 2) all resolve.

R3 PR ordering (per RK-R3-6 mitigation): **TU-006 → TU-005 → TU-002.** Sequential PRs avoid merge conflicts.

<!-- Source: Variant B §3.1 (full directory tree) — preserved as R3 reference per Change #6 -->

---

<!-- End of merged RELEASE-SPEC. -->
<!-- Convergence: 86.8% over 38 diff points. Status: CONVERGED. -->
<!-- Invariant probe: 0 HIGH-severity UNADDRESSED. -->
<!-- Base: Variant C. Overlays: Variant A (preservation test + user-impact framing + no-new-flags). Variant B (break-rejection criterion + deferred-risks + Annexes B+C). -->
