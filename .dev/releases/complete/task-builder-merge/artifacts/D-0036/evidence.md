# D-0036 — T03.13 Evidence: TEST-008 Inherited Verdict Freshness (INV-002) 2-Cycle Fixture

**Task:** T03.13 (Phase 3)
**Roadmap items:** R-064
**Date:** 2026-05-17
**Status:** PASS
**Fixture:** `tests/audit/test_inherited_verdict_freshness_inv_002.py`
**Pytest log:** `D-0036/pytest.log` (24 tests, all PASSED, 0.87s)
**Byte-diff artifact:** `D-0036/byte-diff.txt`

---

## 1. Acceptance Criteria Verification

Acceptance criteria copied from `phase-3-tasklist.md` L636-640:

| AC | Criterion | Result |
|---|---|---|
| AC-1 | `uv run pytest tests/audit/test_inherited_verdict_freshness_inv_002.py -v` exits 0 | **PASS** — see §2 (`24 passed in 0.87s`) |
| AC-2 | 2-cycle byte-diff shows cycle-2 verdict in cycle-2 spawn prompt | **PASS** — see §3 + `D-0036/byte-diff.txt` (cycle-2 PASS row in unified-diff `+` additions) |
| AC-3 | Stale cycle-1 verdict NOT present in cycle-2 spawn | **PASS** — see §3 (`TestFreshnessTwoCycleSpawnPrompt::test_cycle2_prompt_does_not_contain_cycle1_fail_row` green; cycle-1 FAIL row in `-` removals) |
| AC-4 | Evidence at `TASKLIST_ROOT/artifacts/D-0036/evidence.md` | **PASS** — this file |

---

## 2. Pytest Run (live)

```
$ uv run pytest tests/audit/test_inherited_verdict_freshness_inv_002.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0 -- /config/workspace/IronClaude/.venv/bin/python
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collecting ... collected 24 items

tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessProcedureWiredInSkill::test_fix_cycle_header_present_in_source PASSED       [  4%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessProcedureWiredInSkill::test_fix_cycle_header_present_in_mirror PASSED       [  8%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessProcedureWiredInSkill::test_skill_source_mirror_byte_identical PASSED       [ 12%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessProcedureWiredInSkill::test_seven_step_procedure_present PASSED             [ 16%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessProcedureWiredInSkill::test_inv002_log_format_specified PASSED              [ 20%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessProcedureWiredInSkill::test_test_008_cross_reference_present PASSED         [ 25%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessTwoCycleSpawnPrompt::test_cycle2_prompt_contains_cycle2_pass_row PASSED     [ 29%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessTwoCycleSpawnPrompt::test_cycle2_prompt_does_not_contain_cycle1_fail_row PASSED [ 33%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessTwoCycleSpawnPrompt::test_cycle1_prompt_contains_cycle1_fail_row PASSED     [ 37%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessTwoCycleSpawnPrompt::test_cycle1_prompt_does_not_contain_cycle2_pass_row PASSED [ 41%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessTwoCycleSpawnPrompt::test_block_sha_changes_between_cycles PASSED           [ 45%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessTwoCycleSpawnPrompt::test_producer_witness_changes_between_cycles PASSED    [ 50%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessByteDiff::test_full_prompts_differ PASSED                                   [ 54%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessByteDiff::test_verdict_table_region_differs PASSED                          [ 58%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessByteDiff::test_byte_diff_surfaces_cycle2_pass_row PASSED                    [ 62%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessByteDiff::test_diff_line_count_nonzero PASSED                               [ 66%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessLogLine::test_cycle1_log_matches_format PASSED                              [ 70%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessLogLine::test_cycle2_log_matches_format PASSED                              [ 75%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessLogLine::test_cycle2_log_sha_matches_block PASSED                           [ 79%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessLogLine::test_cycle_logs_distinct PASSED                                    [ 83%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessStaleVerdictRejection::test_no_contradiction_under_genuine_change PASSED    [ 87%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessStaleVerdictRejection::test_contradiction_signature_synthesisable PASSED    [ 91%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessStaleVerdictRejection::test_no_op_signature_allowed PASSED                  [ 95%]
tests/audit/test_inherited_verdict_freshness_inv_002.py::TestFreshnessLedgerUpdate::test_ledger_entry_moves_to_cycle2_sha PASSED                  [100%]

============================== 24 passed in 0.87s ==============================
```

Full log captured at `D-0036/pytest.log`.

---

## 3. 2-Cycle Byte-Diff Demonstration

The fixture writes two consecutive synthetic `qa-task-validation-report.md`
artifacts (TB-Add-3 FAIL → PASS), runs the SKILL.md §A.10.5 fix-cycle
re-entry procedure (steps 1-5 + step 7) on each, and compares the two
assembled spawn prompts. Captured byte-diff (also at `D-0036/byte-diff.txt`):

```
cycle1_block_sha16 = 708b81303f70b8e6
cycle2_block_sha16 = b2619c23c8b4680a

--- cycle-1 spawn prompt
+++ cycle-2 spawn prompt
@@ -16,7 +16,7 @@
 |----------|----------------------------------------|---------|----------------------------------------|
 | TB-Add-1 | Placeholder scan (no TBD/TODO/FIXME)   | PASS    | clean                                  |
 | TB-Add-2 | Item count bounds                      | PASS    | 28 items, within bounds                |
-| TB-Add-3 | Clarification adjacency                | FAIL    | items 4, 7 missing Open-Question refs  |
+| TB-Add-3 | Clarification adjacency                | PASS    | items 4, 7 now reference OQ-1/OQ-2     |
 | TB-Add-4 | Circular dependency detection          | PASS    | DAG verified                           |
 | TB-Add-5 | Granularity / XL splitting             | PASS    | no XL items                            |
```

Reading the diff:
- `+ | TB-Add-3 | … | PASS | …` — the cycle-2 verdict landed in the cycle-2 spawn prompt (AC-2 satisfied).
- `- | TB-Add-3 | … | FAIL | …` — the cycle-1 stale verdict is absent from the cycle-2 prompt (AC-3 satisfied).
- `block_sha256` short-form moves from `708b81303f70b8e6` → `b2619c23c8b4680a` between cycles, confirming the re-extract + re-assemble pipeline ran end-to-end (defense-in-depth ledger advance).

---

## 4. Test Inventory (24 tests across 5 classes)

| Test class | # | Role |
|---|---|---|
| `TestFreshnessProcedureWiredInSkill` | 6 | Static SKILL.md guards: fix-cycle header present in src + mirror, byte-identical, 7-step procedure named, INV-002 log token present, TEST-008/T03.13 cross-reference. |
| `TestFreshnessTwoCycleSpawnPrompt` | 6 | Cycle-2 contains cycle-2 PASS row; cycle-2 does NOT contain cycle-1 FAIL row; cycle-1 symmetric anchors; block_sha + producer_sha both move across cycles. |
| `TestFreshnessByteDiff` | 4 | Full prompts differ; verdict-table region differs; unified-diff additions include cycle-2 PASS row and removals include cycle-1 FAIL row; ndiff line count > 0. |
| `TestFreshnessLogLine` | 4 | Step-7 log lines for both cycles parse against the documented format regex; cycle-2 log block_sha matches the recomputed block sha; cycle-1 and cycle-2 logs distinct. |
| `TestFreshnessStaleVerdictRejection` | 3 | Step-6 contradiction detector: no false-positive on genuine change; contradiction signature synthesisable; no-op signature allowed. |
| `TestFreshnessLedgerUpdate` | 1 | `last_injected_verdict_sha256` ledger advances to cycle-2 block_sha after cycle 2. |

24 tests, 24 PASS, 0 fail, 0 skip.

---

## 5. Mapping to SKILL.md §A.10.5 Procedure

Per D-0030 §2, the orchestrator's fix-cycle re-entry procedure has 7 steps.
The fixture exercises each step's observable surface:

| Step | SKILL.md anchor | Surface exercised by TEST-008 |
|---|---|---|
| 1. Discard cached state | `SKILL.md:1204` | Each cycle re-reads from disk via `producer.read_text(...)`; no `span1` reuse in cycle 2. |
| 2. Re-stat + re-sha256 producer | `SKILL.md:1205` | `test_producer_witness_changes_between_cycles` asserts `p1_sha != p2_sha`. |
| 3. Re-extract "Items Reviewed" span contiguously | `SKILL.md:1206` | `extract_items_reviewed_span()` ported verbatim; `test_block_sha_changes_between_cycles` confirms the span differs. |
| 4. Re-enumerate TB-Add-* catalogue (INV-010) | `SKILL.md:1207` | Out of scope for TEST-008 — covered by TEST-010 / T03.15. |
| 5. Re-assemble and re-splice | `SKILL.md:1208` | `assemble_spawn_prompt()` rebuilds the prompt per cycle; verdict-table region differs (`test_verdict_table_region_differs`). |
| 6. Stale-verdict-rejection (defense-in-depth) | `SKILL.md:1209` | `TestFreshnessStaleVerdictRejection` exercises the contradiction-detector formula on synthetic witnesses; `test_no_contradiction_under_genuine_change` proves no false-positive on the happy path. |
| 7. Log the re-extract | `SKILL.md:1210` | `LOG_RE` regex matches the documented log-line format; `test_cycle2_log_sha_matches_block` cross-checks the witness fields. |

---

## 6. Companion Shell Fixture Parity

`D-0030/fixture-2cycle.sh` (T03.05 demonstration evidence) asserts four
properties: (a) cycle-2 spawn carries cycle-2 verdict, (b) no cycle-1 stale
row in cycle-2 spawn, (c) non-zero byte-diff at verdict-table region, (d)
step-7 log line emitted with witness fields. TEST-008 (this fixture)
reproduces each property in pytest form:

| Shell PASS | TEST-008 equivalent |
|---|---|
| `(a)` cycle-2 spawn carries cycle-2 verdict | `test_cycle2_prompt_contains_cycle2_pass_row` |
| `(b)` cycle-2 does NOT contain cycle-1 stale row | `test_cycle2_prompt_does_not_contain_cycle1_fail_row` |
| `(c)` byte-diff non-zero at verdict-table region | `test_byte_diff_surfaces_cycle2_pass_row` + `test_diff_line_count_nonzero` + `test_verdict_table_region_differs` |
| `(d)` step-7 log line with witnesses | `TestFreshnessLogLine` (4 tests) |

TEST-008 additionally adds static-procedure guards (`TestFreshnessProcedureWiredInSkill`, 6 tests) so accidental regression of the SKILL.md A.10.5 procedure block is caught by the merge-gate, not deferred to a runtime spawn.

---

## 7. Dependency Confirmation

T03.13 depends on T03.05 (D-0030, INV-002 freshness rule wired) and T03.12
(CP-P03-T07-T11 mid-phase checkpoint).

- **T03.05 / D-0030:** SKILL.md §A.10.5 fix-cycle re-entry block landed at L1202-1212 (7-step procedure + cross-reference to TEST-008). Confirmed by `TestFreshnessProcedureWiredInSkill::test_seven_step_procedure_present`.
- **T03.12 / CP-P03-T07-T11:** Mid-phase checkpoint `status: PASS`, explicitly unblocks T03.13 (CP-P03-T07-T11 §8). All prerequisites satisfied.

---

## 8. Phase-3 Sequencing Note

TEST-008 (D-0036, freshness) is the second of three fixture commits gated
by CP-P03-T07-T11 → CP-P03-END. TEST-007 (D-0035, presence) landed at
T03.11; TEST-009 (D-0037, self-audit) and TEST-010 (D-0038, dynamic
enumeration) follow at T03.14 and T03.15. The fixture trio collectively
satisfies the M3 Exit Condition "spawn prompt carries verdict table
byte-for-byte; on fix-cycle re-run orchestrator re-injects NEW cycle-N
verdict; rf-qa-qualitative output contains Self-Audit with ≥1 semantic
check" (phase-3-tasklist L3).

---

## 9. Artifacts Produced by T03.13

| File | Purpose |
|---|---|
| `tests/audit/test_inherited_verdict_freshness_inv_002.py` | TEST-008 fixture (24 tests, 5 classes) |
| `D-0036/evidence.md` | This file |
| `D-0036/pytest.log` | Captured pytest -v output (24 PASSED) |
| `D-0036/byte-diff.txt` | Unified diff of cycle-1 vs cycle-2 spawn prompts at the verdict-table region |

**T03.13 status: PASS.**
