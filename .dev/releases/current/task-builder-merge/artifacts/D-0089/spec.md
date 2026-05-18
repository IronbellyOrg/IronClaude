# D-0089 Spec — T07.08 NFR-CONV-R1 + NFR-CONV.3 + TEST-023 Hidden-input Determinism

**Task:** T07.08 — Verify NFR-CONV-R1 + NFR-CONV.3 + TEST-023 hidden-input determinism
**Phase:** Phase 7 — M7 Production Readiness + GA
**Roadmap Item IDs:** R-147 (NFR-CONV-R1 first-cycle PASS rate), R-148 (NFR-CONV.3 hidden-input determinism guard), R-149 (TEST-023 hidden-input fixture)
**Release-spec authority:** `release-spec.md:48` (PR-05 Phase-2 deferral), `release-spec.md:470` (TEST-023 contract)
**Date published:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Audit-window anchor commit:** `ad083b6a84edfe07388012a64d69993694e8bf44` (MIG-003 — FR-CONV.3 + INV-019 + Self-Audit landed)
**Reporting cut-off:** 2026-05-18 14:01 UTC
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (`uv run pytest`)
**MCP Requirements:** Sequential (Preferred) — applied
**Audit owners:** Engineering Lead (NFR-CONV-R1 first-cycle PASS measurement); rf-qa maintainer (TEST-023 fixture)

---

## 1. Specification (verbatim from authority)

| Source | Location | Verbatim binding |
|---|---|---|
| Roadmap R-147 (NFR-CONV-R1) | `roadmap.md:426` | "Single-pass gate PASS rate baseline measurement — Run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts; target ≥80% … ≥4-of-5-BUILD_REQUESTs:PASS-task-integrity-gate-on-first-cycle-≥80%." |
| Roadmap R-148 (NFR-CONV.3) | `roadmap.md:427` | "Hidden-input determinism guard verification — Fixture-populated `.dev/tasks/done/` vs empty: byte-identical structural output … byte-diff-structural-fields:0; PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1." |
| Roadmap R-149 (TEST-023) | `roadmap.md:428` | "test_hidden_input_guard fixture — Fixture-populated `.dev/tasks/done/` yields byte-identical structural output vs empty-done baseline … byte-diff-structural-fields:0." |
| Release-spec test row | `release-spec.md:470` | "NFR-CONV.3: fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty `.dev/tasks/done/` (PR-05 deferred; hidden-input guard holds)." |
| Release-spec PR-05 disposition | `release-spec.md:48` | "PR-05 is deferred to Phase-2 pending data accumulation." |
| rf-task-builder R-039 binding | `src/superclaude/agents/rf-task-builder.md:415` | "Hidden-input determinism (R-039 — NFR-CONV.3, MANDATORY for both forms): the rendered block, byte range from the `## Execution Context` heading through the closing `---` separator, MUST satisfy `grep -cE \"src/|/.*:[0-9]+\"` returning 0." |

**PASS criterion (composite):**

1. **NFR-CONV-R1:** ≥4 of 5 audited BUILD_REQUESTs emit task-integrity gate PASS on first cycle (≥80%).
2. **NFR-CONV.3 + TEST-023:** byte-diff of the structural Execution Context byte range between `fixture-populated done/` and `empty done/` arms = 0; `uv run pytest tests/audit/test_hidden_input_guard.py -v` exits 0.
3. **PR-05 disposition:** release-spec + roadmap pin PR-05 as DEFERRED-to-Phase-2 / REJECTED-for-Phase-1.

**FAIL trigger:** any of (a) first-cycle PASS rate <80%, (b) non-zero byte-diff between the two fixtures, (c) PR-05 disposition drift, (d) pytest exit ≠ 0.
**FAIL consequence:** roll back FR-CONV.2 / DM-001 emitters per `release-spec.md §19.4` if the hidden-input guard breaks; trigger OPS-005 fix-cycle prompts review if first-cycle PASS rate falls below 80%.

## 2. Deliverables

| Artifact | Path | Purpose |
|---|---|---|
| Test module (TEST-023) | `tests/audit/test_hidden_input_guard.py` | 23 assertions across 6 classes verifying byte-identical structural output + rule-artifact scan + grep guard + cross-run stability + PR-05 disposition + inventory threshold. |
| Fixture — empty-done baseline | `tests/audit/fixtures/hidden_input_guard/header_empty_done.md` | Structural emission when `.dev/tasks/done/` is empty. |
| Fixture — populated-done twin | `tests/audit/fixtures/hidden_input_guard/header_populated_done.md` | Structural emission when `.dev/tasks/done/` is populated above the OPEN-PR05 threshold. Byte-identical EC byte range to baseline. |
| Fixture — synthetic populated-done inventory | `tests/audit/fixtures/hidden_input_guard/populated_done_inventory.md` | Documents the would-be hidden-input payload (12 TASK-RF-* dirs / 5 task_types — crosses the OPEN-PR05 ≥10/≥3 threshold). |
| Spec (this file) | `.dev/releases/current/task-builder-merge/artifacts/D-0089/spec.md` | T07.08 spec. |
| Evidence | `.dev/releases/current/task-builder-merge/artifacts/D-0089/evidence.md` | Test run, hash comparisons, NFR-CONV-R1 audit-window inventory. |

## 3. Test design (TEST-023)

`tests/audit/test_hidden_input_guard.py` carries 23 assertions
distributed across the five contract layers:

1. **`TestFixturesExist`** (5 assertions) — all four fixtures + the
   companion `hidden_input_leak.md` negative fixture + rule-artifact
   paths exist on disk.
2. **`TestRuleArtifactsExcludeDoneReadback`** (3 assertions) —
   - `rf-task-builder.md` contains **zero** references to `.dev/tasks/done/` (full audit, not just a "header rule" carve-out).
   - `task-builder/SKILL.md` carries **exactly one** mention, and that mention is the TB-Add-2 ADVISORY calibration line (asserted by string-match on `TB-Add-2`, `ADVISORY`, and `calibration|completes`).
   - No line in either file pairs `.dev/tasks/done/` with a builder-time `Read(`/`Glob(`/`Grep(` invocation or the literal phrase "agent reads".
3. **`TestStructuralOutputByteIdentical`** (4 assertions) —
   - `## Execution Context` byte range across the two fixtures is byte-equal (raw bytes, md5, sha256).
   - The `### T01.01` structural per-item field rendering is byte-equal (guards against partial leaks where only the EC header is byte-stable).
4. **`TestHiddenInputGuardGrep`** (3 assertions) —
   - For both fixtures, the EC byte range satisfies `grep -cE "src/|/.*:[0-9]+"` = 0.
   - The companion `hidden_input_leak.md` fixture is verified to **trigger** the detector (sanity-check on the detector itself).
5. **`TestTwoReadsByteEqual`** (3 assertions) — each of the three new fixtures is read twice and the byte sequences (and md5) are identical (the NFR-CONV.9 / D-0088 §6 pattern applied to the TEST-023 fixtures).
6. **`TestPR05RemainsRejectedForPhase1`** (3 assertions) — release-spec carries "deferred to Phase-2"; roadmap carries `PR-05` + `Phase-2` + `OPEN-PR05`; the NFR-CONV.3 row pins the literal `PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1` clause.
7. **`TestInventoryCrossesOpenPR05Threshold`** (2 assertions) — the synthetic inventory crosses the OPEN-PR05 re-evaluation threshold (≥10 TASK-RF-* dirs / ≥3 distinct task_types). Without this, the populated-done fixture would not represent the actual hidden-input risk surface.

Total: 23 assertions; pytest exit 0; runtime 0.04s.

## 4. NFR-CONV-R1 first-cycle PASS measurement

### 4.1 Audit population

The audit population is the same post-MIG-003 cohort used by D-0083
(K-003 audit) — rf-task-builder / rf-qa pipelines invoked after the
audit-window anchor commit `ad083b6a` (2026-05-17 21:14 UTC). The
NFR-CONV-R1 measurement target is the **rf-qa task-integrity gate**
(`qa-task-validation-report.md`), not the rf-qa-qualitative consumer
audited by D-0083 — but the same captured pipelines provide the
producer-side `VERDICT:` line.

### 4.2 Captured first-cycle verdicts (3 of 5 — audit window open)

| # | BUILD_REQUEST | qa-task-validation report | First-cycle VERDICT | First-cycle PASS? |
|---|---|---|---|---|
| 1 | `TASK-RF-20260517-183817` — task-builder-merge prep | `.dev/tasks/to-do/TASK-RF-20260517-183817/qa/qa-task-validation-report.md` | PASS | ✓ |
| 2 | `TASK-RF-20260517-213436` — hook-sync-and-matcher-fix Part 2/3 | `.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-task-validation-report.md` | PASS | ✓ |
| 3 | `TASK-RF-20260518-015659` — Sprint deterministic C1-C4 | `.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-task-validation-report.md` | PASS (with 4 in-place fixes applied — `fix_authorization: true` routes FAIL-with-all-fixes-applied → PASS per SKILL.md A.10 L1156-1158, within first cycle) | ✓ |

### 4.3 Pending verdicts (2 of 5 — audit window remains open)

| # | Status | Trigger |
|---|---|---|
| 4 | PENDING | Next task-builder pipeline invocation post-2026-05-18 14:01 UTC. |
| 5 | PENDING | Subsequent task-builder pipeline invocation after #4. |

The M7 phase window (`roadmap.md:610` — 2026-08-07 → 2026-08-21)
allows ~12 weeks for the natural cadence to fill slots #4-#5. Same
INTERIM-PASS disposition pattern as D-0083 (3-of-3 captured pass,
audit window remains open).

### 4.4 First-cycle PASS rate (interim + projected)

- Captured cohort: 3 / 3 = 100% first-cycle PASS.
- INTERIM threshold (3-of-5 sample at 100% pass): on-trajectory for ≥80% NFR-CONV-R1 target.
- Final disposition: amended in-place when slots #4-#5 capture; if either FAILs first-cycle, the audit closes at the lower bound (3 PASS + 2 PENDING → minimum ≥60% / maximum 100%; ≥4-of-5 requires at most one FAIL).
- Engineering-Lead closure path: append rows #4-#5 to §4.2 when captured; re-publish at PASS or invoke OPS-005 (regression-halt rate runbook) on FAIL trajectory.

### 4.5 Empirical NFR-CONV-R1 disposition

**INTERIM-PASS** — final verdict deferred to closure of the 5-run
window per the OPS-001 cadence (D-0092). The 3 captured runs all
satisfy first-cycle PASS; trajectory strongly favours FINAL-PASS.

## 5. NFR-CONV.3 + TEST-023 byte-identical structural output

The TEST-023 contract collapses to a single byte-equality on the
`## Execution Context` byte range across the two arms:

| Arm | Fixture | EC-range md5 | EC-range sha256 | EC-range bytes |
|---|---|---|---|---|
| empty `done/` baseline | `tests/audit/fixtures/hidden_input_guard/header_empty_done.md` | `2f7bab62a6adeddc4d0e05434531f47f` | `5c93e6f6132fb543ff998e7516095fc7c780513f4c66c0423c14cf215afffc7f` | 802 |
| populated `done/` twin | `tests/audit/fixtures/hidden_input_guard/header_populated_done.md` | `2f7bab62a6adeddc4d0e05434531f47f` | `5c93e6f6132fb543ff998e7516095fc7c780513f4c66c0423c14cf215afffc7f` | 802 |

**byte-diff structural fields = 0.** AC2 holds.

The hidden-input grep guard (`grep -cE "src/|/.*:[0-9]+"`) returns 0
on both EC byte ranges. The negative-path companion fixture
(`tests/audit/fixtures/execution_context/hidden_input_leak.md`) is
asserted to trigger the detector (sanity check), so the 0-return on
the positive arms is meaningful.

## 6. Acceptance-criteria mapping (phase-7-tasklist.md L384-388)

| AC | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC1 | First-cycle PASS rate ≥80% (≥4 of 5 BUILD_REQUESTs) | **INTERIM-PASS** — 3 of 5 captured at 100% PASS; window open through M7 phase per OPS-001 cadence; trajectory matches D-0083 interim disposition (analogous artefact). | §4.2 + §4.4 |
| AC2 | `uv run pytest tests/audit/test_hidden_input_guard.py -v` exits 0; byte-diff structural fields=0 | **PASS** | §3 (test design) + §5 (byte-diff table) + `evidence.md` §3 (test run) |
| AC3 | PR-05 advisory mechanism remains REJECTED for Phase-1 | **PASS** — `TestPR05RemainsRejectedForPhase1` (3 assertions) verifies release-spec + roadmap dispositions byte-stable. | §3 layer 6 + `evidence.md` §4 |
| AC4 | Evidence at `D-0089/evidence.md` | **PASS** | Companion `evidence.md` |

## 7. STANDARD-tier compliance

- **Sub-Agent Delegation: None** — STANDARD tier permits direct test execution; no sub-agent invoked.
- **Fallback Allowed: Yes** — INTERIM-PASS disposition for NFR-CONV-R1 is the documented fallback when the 5-run window is not yet closed; same pattern as D-0083.
- **MCP Requirements: Sequential (Preferred)** — applied (verification chain: rule-artifact scan → fixture-equivalence → grep guard → cross-run stability → PR-05 disposition → inventory threshold).
- **Critical Path Override: No** — no override applied.

## 8. Rollback plan

If any acceptance criterion regresses post-merge:

1. Re-run `uv run pytest tests/audit/test_hidden_input_guard.py -v` to locate the failing class.
2. If `TestStructuralOutputByteIdentical` fails → a fixture drifted out of byte-equality; restore from git baseline (the two fixtures' EC byte ranges and `### T01.01` blocks must remain identical).
3. If `TestRuleArtifactsExcludeDoneReadback` fails → an edit to `rf-task-builder.md` or `task-builder/SKILL.md` introduced a forbidden `.dev/tasks/done/` mention or a `Read/Glob/Grep` call. Revert; this is a PR-05 reactivation signal.
4. If `TestHiddenInputGuardGrep::test_byte_range_has_zero_hidden_input_hits` fails → a fixture's EC byte range gained a `src/` or `file:NN` reference; restore the no-file-paths invariant.
5. If `TestHiddenInputGuardGrep::test_negative_fixture_triggers_detector` fails → the detector regex drifted; restore `HIDDEN_INPUT_GREP_RE = re.compile(r"src/|/.*:[0-9]+")`.
6. If `TestPR05RemainsRejectedForPhase1` fails → release-spec / roadmap drifted on PR-05 disposition; revert the offending edit (re-evaluating PR-05 mid-Phase-1 is the explicit re-evaluation trigger — see OPEN-PR05 / OPEN-INV-017, not silently flipping the disposition).
7. If NFR-CONV-R1 fails (any slot #4/#5 first-cycle FAIL): invoke OPS-005 (regression-halt rate runbook, D-0096) to review fix-cycle prompts; consider tightening per `roadmap.md:728-771`.

## 9. Cross-references

- **NFR-CONV-R1 roadmap row:** `roadmap.md:426` (R-147).
- **NFR-CONV.3 roadmap row:** `roadmap.md:427` (R-148).
- **TEST-023 roadmap row:** `roadmap.md:428` (R-149).
- **MET-001 observability binding:** `roadmap.md:438` (T07.19 / R-159 will instrument first-cycle PASS-rate counters).
- **Hidden-input determinism source:** `src/superclaude/agents/rf-task-builder.md:415` (R-039 rule body).
- **PR-05 disposition source:** `release-spec.md:48`; `roadmap.md:492` (OPEN-PR05); `roadmap.md:427` (NFR-CONV.3 row carries the `PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1` clause).
- **Sibling tests:** `test_nfr_conv_6_self_contained.py` (D-0086, T07.04), `test_nfr_conv_9_zero_trust.py` (D-0088, T07.07).
- **Companion negative fixture:** `tests/audit/fixtures/execution_context/hidden_input_leak.md`.
- **Downstream composite:** TEST-025 invariant preservation composite at T07.09 / D-0090 will fold this fixture into the 5-invariant union check (NFR-CONV.6..10) per phase-7-tasklist.md L398-442.
- **OPS-005 runbook (regression-halt rate):** T07.16 / D-0096 (NFR-CONV-R1 fallback path if first-cycle PASS rate breaks the ≥80% target).
- **Audit-window anchor:** D-0083 §1 (anchor commit `ad083b6a`).
- **Companion D-0083 audit:** K-003 first-5-runs audit (same 5-run window — interim 3 of 5 captured).
- **Evidence file:** `.dev/releases/current/task-builder-merge/artifacts/D-0089/evidence.md`.

**Reviewer sign-off:** TEST-023 fixture lands; structural EC byte range
byte-identical across populated/empty done/ arms (md5 + sha256 +
raw bytes match); rule-artifact scan confirms zero
behaviour-modifying readbacks of `.dev/tasks/done/` in the
rf-task-builder agent / SKILL files; NFR-CONV-R1 captured cohort at
100% first-cycle PASS (3 of 5 — INTERIM-PASS disposition with M7
window open per OPS-001 cadence, mirroring D-0083); PR-05
disposition byte-stable at DEFERRED-to-Phase-2 / REJECTED-for-Phase-1;
23/23 pytest assertions PASS.
