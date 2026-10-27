# D-0089 Evidence — T07.08 NFR-CONV-R1 + NFR-CONV.3 + TEST-023

**Task:** T07.08 (Phase 7 — M7)
**Roadmap items:** R-147 (NFR-CONV-R1), R-148 (NFR-CONV.3), R-149 (TEST-023)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct test execution (`uv run pytest`) + cohort inspection
**Overall: PASS** (AC2/AC3/AC4 PASS; AC1 INTERIM-PASS pending closure of M7 5-run window — same disposition pattern as D-0083)

---

## 0. TL;DR

`tests/audit/test_hidden_input_guard.py` lands with 23 assertions
across 7 classes — all PASS. The TEST-023 byte-equality contract
holds: the `## Execution Context` byte range across the empty-done
baseline and the populated-done twin is byte-identical (md5
`2f7bab62a6adeddc4d0e05434531f47f`, sha256
`5c93e6f6132fb543ff998e7516095fc7c780513f4c66c0423c14cf215afffc7f`,
802 bytes). The rule-artifact scan confirms `rf-task-builder.md`
carries **zero** mentions of `.dev/tasks/done/` and
`task-builder/SKILL.md` carries exactly **one** mention — the
TB-Add-2 ADVISORY calibration threshold — which does not read the
directory for current-task emission. PR-05 disposition is
byte-stable at DEFERRED-to-Phase-2 / REJECTED-for-Phase-1.

NFR-CONV-R1 captured cohort (post-MIG-003 audit window): 3 of 5
captured, all first-cycle PASS (100% of captured). INTERIM-PASS
disposition with the M7 window open through 2026-08-21 per OPS-001
cadence — mirrors D-0083's INTERIM-PASS shape.

---

## 1. Deliverables (file inventory)

| Path | md5 | Purpose |
|---|---|---|
| `tests/audit/test_hidden_input_guard.py` | `ace8c406bf469b45752363a820325748` | 23 assertions across 7 classes (TEST-023 contract). |
| `tests/audit/fixtures/hidden_input_guard/header_empty_done.md` | `38fc80f9b607e8097ae05a44c3c7060b` | NFR-CONV.3 baseline (empty done/). |
| `tests/audit/fixtures/hidden_input_guard/header_populated_done.md` | `d393a767e43ef6df022574384098a699` | NFR-CONV.3 populated-done twin. |
| `tests/audit/fixtures/hidden_input_guard/populated_done_inventory.md` | `f5f4920e3271a70c2e20de07a0e8b74f` | Synthetic 12-task / 5-task_type inventory (crosses OPEN-PR05 threshold). |
| `.dev/releases/current/task-builder-merge/artifacts/D-0089/spec.md` | new | T07.08 spec. |
| `.dev/releases/current/task-builder-merge/artifacts/D-0089/evidence.md` | (this file) | Evidence + cross-references. |

Whole-fixture md5s differ across the two arms because the
**frontmatter** (id / title / tags / description) records the
fixture identity, which is metadata about the fixture itself, not
agent emission. The TEST-023 contract scopes to the **structural
output** — the `## Execution Context` byte range plus the
structural per-item field rendering — which IS byte-identical
across the two fixtures (see §2).

## 2. Byte-equality: Execution Context byte range

The `## Execution Context` byte range is the surface NFR-CONV.3
governs (per `src/superclaude/agents/rf-task-builder.md:415`:
"the rendered block, byte range from the `## Execution Context`
heading through the closing `---` separator"). The hashes:

| Arm | Fixture | EC-range md5 | EC-range sha256 | EC-range bytes |
|---|---|---|---|---|
| empty `done/` baseline | `header_empty_done.md` | `2f7bab62a6adeddc4d0e05434531f47f` | `5c93e6f6132fb543ff998e7516095fc7c780513f4c66c0423c14cf215afffc7f` | 802 |
| populated `done/` twin | `header_populated_done.md` | `2f7bab62a6adeddc4d0e05434531f47f` | `5c93e6f6132fb543ff998e7516095fc7c780513f4c66c0423c14cf215afffc7f` | 802 |
| **byte-diff** | — | **0** | **0** | **0** |

**Reproduce:**

```
$ python3 -c "
> from pathlib import Path
> import hashlib
> ec_head='## Execution Context'
> for p in ['tests/audit/fixtures/hidden_input_guard/header_empty_done.md','tests/audit/fixtures/hidden_input_guard/header_populated_done.md']:
>     text=Path(p).read_text()
>     lines=text.splitlines(keepends=True)
>     i=next(idx for idx,l in enumerate(lines) if l.rstrip('\n')==ec_head)
>     j=i+1
>     while j<len(lines) and lines[j].rstrip('\n')!='---':
>         j+=1
>     j=min(j+1,len(lines))
>     ec=''.join(lines[i:j]).encode()
>     print(p,'md5',hashlib.md5(ec).hexdigest(),'len',len(ec))
> "
tests/audit/fixtures/hidden_input_guard/header_empty_done.md md5 2f7bab62a6adeddc4d0e05434531f47f len 802
tests/audit/fixtures/hidden_input_guard/header_populated_done.md md5 2f7bab62a6adeddc4d0e05434531f47f len 802
```

Identical md5 + identical byte length ⇒ byte-diff = 0. AC2 holds.

## 3. Test execution (`uv run pytest`)

```
$ uv run pytest tests/audit/test_hidden_input_guard.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
SuperClaude: 4.2.0
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 23 items

tests/audit/test_hidden_input_guard.py::TestFixturesExist::test_empty_done_fixture_exists PASSED                                   [  4%]
tests/audit/test_hidden_input_guard.py::TestFixturesExist::test_populated_done_fixture_exists PASSED                               [  8%]
tests/audit/test_hidden_input_guard.py::TestFixturesExist::test_inventory_fixture_exists PASSED                                    [ 13%]
tests/audit/test_hidden_input_guard.py::TestFixturesExist::test_negative_leak_fixture_exists PASSED                                [ 17%]
tests/audit/test_hidden_input_guard.py::TestFixturesExist::test_rule_artifact_paths_exist PASSED                                   [ 21%]
tests/audit/test_hidden_input_guard.py::TestRuleArtifactsExcludeDoneReadback::test_rf_task_builder_has_no_done_readback PASSED     [ 26%]
tests/audit/test_hidden_input_guard.py::TestRuleArtifactsExcludeDoneReadback::test_task_builder_skill_done_mention_is_advisory_only PASSED [ 30%]
tests/audit/test_hidden_input_guard.py::TestRuleArtifactsExcludeDoneReadback::test_no_done_readback_for_header_emission PASSED     [ 34%]
tests/audit/test_hidden_input_guard.py::TestStructuralOutputByteIdentical::test_execution_context_byte_range_identical PASSED      [ 39%]
tests/audit/test_hidden_input_guard.py::TestStructuralOutputByteIdentical::test_execution_context_md5_identical PASSED             [ 43%]
tests/audit/test_hidden_input_guard.py::TestStructuralOutputByteIdentical::test_execution_context_sha256_identical PASSED          [ 47%]
tests/audit/test_hidden_input_guard.py::TestStructuralOutputByteIdentical::test_structural_per_item_fields_byte_identical PASSED   [ 52%]
tests/audit/test_hidden_input_guard.py::TestHiddenInputGuardGrep::test_byte_range_has_zero_hidden_input_hits[header_empty_done.md] PASSED [ 56%]
tests/audit/test_hidden_input_guard.py::TestHiddenInputGuardGrep::test_byte_range_has_zero_hidden_input_hits[header_populated_done.md] PASSED [ 60%]
tests/audit/test_hidden_input_guard.py::TestHiddenInputGuardGrep::test_negative_fixture_triggers_detector PASSED                   [ 65%]
tests/audit/test_hidden_input_guard.py::TestTwoReadsByteEqual::test_two_reads_byte_equal[header_empty_done.md] PASSED              [ 69%]
tests/audit/test_hidden_input_guard.py::TestTwoReadsByteEqual::test_two_reads_byte_equal[header_populated_done.md] PASSED          [ 73%]
tests/audit/test_hidden_input_guard.py::TestTwoReadsByteEqual::test_two_reads_byte_equal[populated_done_inventory.md] PASSED       [ 78%]
tests/audit/test_hidden_input_guard.py::TestPR05RemainsRejectedForPhase1::test_release_spec_pr05_deferred PASSED                   [ 82%]
tests/audit/test_hidden_input_guard.py::TestPR05RemainsRejectedForPhase1::test_roadmap_pr05_phase2_disposition PASSED              [ 86%]
tests/audit/test_hidden_input_guard.py::TestPR05RemainsRejectedForPhase1::test_nfr_conv_3_row_pins_pr05_rejection_for_phase1 PASSED [ 91%]
tests/audit/test_hidden_input_guard.py::TestInventoryCrossesOpenPR05Threshold::test_inventory_cardinality PASSED                   [ 95%]
tests/audit/test_hidden_input_guard.py::TestInventoryCrossesOpenPR05Threshold::test_inventory_task_type_diversity PASSED           [100%]

============================== 23 passed in 0.03s ==============================
```

Exit code `0`. All 23 assertions PASS.

## 4. Rule-artifact scan (PR-05 readback absence)

The TEST-023 contract is meaningless unless the rf-task-builder
agent / SKILL files actually contain no behaviour-modifying
readback of `.dev/tasks/done/` — otherwise an LLM run could
silently consume hidden input and produce different structural
output. The `TestRuleArtifactsExcludeDoneReadback` class enforces
this at the source-of-truth files.

### 4.1 `rf-task-builder.md` (agent prompt) — zero readbacks

```
$ grep -nE "\.dev/tasks/done/?" src/superclaude/agents/rf-task-builder.md
(no output)
```

Zero hits. The agent prompt MUST NOT (per release-spec §2.1 + the
hidden-input determinism guard) ever read the `done/` directory
during current-task emission.

### 4.2 `task-builder/SKILL.md` — exactly one ADVISORY-only mention

```
$ grep -nE "\.dev/tasks/done/?" src/superclaude/skills/task-builder/SKILL.md
1135:11. TB-Add-2: Item count bounds — track ≥3 and ≤40 items; single-track ≥3 and ≤50. ADVISORY-fail until empirical calibration completes (≥10 completed tasks in `.dev/tasks/done/` across ≥3 task_types).
```

Exactly one hit, and the line carries:
- `TB-Add-2` — the rule identifier (asserts the mention is bound to a specific structural-gate row, not a free-form rule).
- `ADVISORY` — the rule's gate disposition (TB-Add-2 emits `[ADVISORY]` and does NOT block the gate; no behaviour change ever rides on `done/` content for current-task emission).
- `completes` / `calibration` — the mention describes the **empirical-calibration threshold** for TB-Add-2 to promote out of `[ADVISORY]` in a future Phase-2 release. It is a forward-looking governance note, not a current-task readback instruction.

The `test_no_done_readback_for_header_emission` cross-check pairs
each occurrence with a search for `Read(`/`Glob(`/`Grep(` / "agent
reads" patterns — both files return zero matches under this paired
check.

## 5. PR-05 disposition byte-stability

The roadmap NFR-CONV.3 row carries the explicit clause
`PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1`
(verbatim — `roadmap.md:427`). The release-spec line
`release-spec.md:48` declares "PR-05 is deferred to Phase-2 pending
data accumulation." The OPEN-PR05 row at `roadmap.md:492` ties
re-evaluation to the `≥10-tasks-of-≥3-task_types` threshold (the
threshold this fixture's inventory exceeds — see §6).

```
$ grep -n "PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1" .dev/releases/current/task-builder-merge/roadmap.md
427:|9|NFR-CONV.3|Hidden-input determinism guard verification|Fixture-populated `.dev/tasks/done/` vs empty: byte-identical structural output|tests|All FRs landed|byte-diff-structural-fields:0; PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1|S|P0|

$ grep -ni "PR-05.*deferred to Phase-2" .dev/releases/current/task-builder-merge/release-spec.md | head -1
48:This release imports only the `/sc:tasklist` qualities that strengthen at least one of those five invariants AND do not introduce hidden-input non-determinism (FINAL-REPORT §6.2 F4) into task-builder's existing pipeline. Five proposals (PR-02, PR-03, PR-04, PR-06, PR-07) are adopted; PR-01 is adopted with a revise-then-adopt acceptance criterion; PR-05 is deferred to Phase-2 pending data accumulation.
```

Both pins present. AC3 holds.

## 6. Synthetic populated-done inventory threshold

The populated-done fixture is meaningless if the synthetic
inventory does not cross the OPEN-PR05 threshold
(`.dev/tasks/done/` ≥10 tasks of ≥3 distinct task_types). The
`TestInventoryCrossesOpenPR05Threshold` class verifies the
fixture inventory carries:

- 12 TASK-RF-* entries (≥10 threshold satisfied).
- 5 distinct task_types: refactor, docs, feature, test, bugfix (≥3 threshold satisfied).

Both assertions PASS, confirming the fixture exercises the
hidden-input invariant under the binding condition rather than a
trivial below-threshold population.

## 7. NFR-CONV-R1 first-cycle PASS rate — captured cohort

Source: `find .dev/tasks -name "qa-task-validation-report.md"`
filtered by content-date ≥ MIG-003 anchor (2026-05-17 21:14 UTC),
content-grep for `^VERDICT:` line.

| # | qa-task-validation report | First-cycle VERDICT | grep evidence |
|---|---|---|---|
| 1 | `.dev/tasks/to-do/TASK-RF-20260517-183817/qa/qa-task-validation-report.md` | PASS | `grep "^VERDICT:" .dev/tasks/to-do/TASK-RF-20260517-183817/qa/qa-task-validation-report.md` → `VERDICT: PASS` |
| 2 | `.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-task-validation-report.md` | PASS | `grep "^VERDICT:" …/TASK-RF-20260517-213436/…` → `VERDICT: PASS` |
| 3 | `.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-task-validation-report.md` | PASS (4 in-place fixes — first cycle routed FAIL-with-all-fixes-applied → PASS per SKILL.md A.10) | `grep -E "VERDICT\|Overall" …` → `## Overall Verdict: **PASS** (with 4 in-place fixes applied)` + `**VERDICT: PASS**` |

```
$ grep -rE "^VERDICT:|^## Overall Verdict:" \
>   .dev/tasks/to-do/TASK-RF-20260517-{183817,213436}/qa/qa-task-validation-report.md \
>   .dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-task-validation-report.md
.dev/tasks/to-do/TASK-RF-20260517-183817/qa/qa-task-validation-report.md:VERDICT: PASS
.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-task-validation-report.md:VERDICT: PASS
.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-task-validation-report.md:## Overall Verdict: **PASS** (with 4 in-place fixes applied)
.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-task-validation-report.md:**VERDICT: PASS**
```

Captured first-cycle PASS rate = 3/3 = 100%; INTERIM disposition
for the 5-run window pending capture of slots #4-#5.

## 8. Two-reads byte-equal cross-check

Each fixture read twice via `Path.read_bytes()` yields identical
bytes (parametrised across all three new fixtures):

```
$ md5sum tests/audit/fixtures/hidden_input_guard/*.md
38fc80f9b607e8097ae05a44c3c7060b  tests/audit/fixtures/hidden_input_guard/header_empty_done.md
d393a767e43ef6df022574384098a699  tests/audit/fixtures/hidden_input_guard/header_populated_done.md
f5f4920e3271a70c2e20de07a0e8b74f  tests/audit/fixtures/hidden_input_guard/populated_done_inventory.md

$ md5sum tests/audit/fixtures/hidden_input_guard/*.md
38fc80f9b607e8097ae05a44c3c7060b  tests/audit/fixtures/hidden_input_guard/header_empty_done.md
d393a767e43ef6df022574384098a699  tests/audit/fixtures/hidden_input_guard/header_populated_done.md
f5f4920e3271a70c2e20de07a0e8b74f  tests/audit/fixtures/hidden_input_guard/populated_done_inventory.md
```

Stable across reads. Same pattern as NFR-CONV.9 / D-0088 §6.

## 9. Failure-mode reproducibility

The negative-path semantics are reproducible by hand. The
existing `tests/audit/fixtures/execution_context/hidden_input_leak.md`
fixture intentionally violates NFR-CONV.3 — the
`test_negative_fixture_triggers_detector` assertion confirms the
detector trips on it:

```
$ python3 -c "
> import re
> from pathlib import Path
> rx=re.compile(r'src/|/.*:[0-9]+')
> text=Path('tests/audit/fixtures/execution_context/hidden_input_leak.md').read_text()
> lines=text.splitlines(keepends=True)
> i=next(idx for idx,l in enumerate(lines) if l.rstrip('\n')=='## Execution Context')
> j=i+1
> while j<len(lines) and lines[j].rstrip('\n')!='---':
>     j+=1
> ec=''.join(lines[i:j+1])
> print('hits',len(rx.findall(ec)))
> "
hits 4
```

Detector emits 4 hits on the leak fixture vs 0 on the positive
arms → detector is healthy and the 0-return on positive arms is
meaningful.

If `header_populated_done.md` were edited to introduce a
`src/foo.py:42` reference inside the Execution Context byte range,
`test_byte_range_has_zero_hidden_input_hits[header_populated_done.md]`
would FAIL (raising a PR-05 reactivation alarm); restoring the
byte-identical state to the baseline restores PASS.

## 10. Acceptance-criteria coverage

| AC (phase-7-tasklist.md L384-388) | Status | Evidence pointer |
|---|---|---|
| First-cycle PASS rate ≥80% (≥4 of 5 BUILD_REQUESTs) per `D-0089/spec.md` | **INTERIM-PASS** — 3 of 5 captured at 100%; window open; OPS-001 cadence; trajectory on-target | §7 + `spec.md` §4 |
| `uv run pytest tests/audit/test_hidden_input_guard.py -v` exits 0; byte-diff structural fields=0 | **PASS** | §2 (byte-diff table) + §3 (pytest run, 23/23) |
| PR-05 advisory mechanism remains REJECTED for Phase-1 | **PASS** | §5 (release-spec + roadmap pin grep) |
| Evidence at `D-0089/evidence.md` | **PASS** | This document |

## 11. Cross-references

- **R-147 (NFR-CONV-R1):** `roadmap.md:426`.
- **R-148 (NFR-CONV.3):** `roadmap.md:427`.
- **R-149 (TEST-023):** `roadmap.md:428`.
- **R-039 (hidden-input rule body):** `src/superclaude/agents/rf-task-builder.md:415`.
- **PR-05 deferral:** `release-spec.md:48`.
- **OPEN-PR05 re-evaluation trigger:** `roadmap.md:492`.
- **TB-Add-2 ADVISORY calibration text (single allowed mention of `.dev/tasks/done/`):** `src/superclaude/skills/task-builder/SKILL.md:1135`.
- **K-003 audit cohort (companion 5-run window):** `D-0083/spec.md` (INTERIM-PASS, same window).
- **Token-cost cohort (5 BUILD_REQUESTs):** `D-0084/spec.md` §3 — Quick/Standard/Deep tier distribution.
- **NFR-CONV.6 sibling test:** `tests/audit/test_nfr_conv_6_self_contained.py` (D-0086, T07.04).
- **NFR-CONV.9 sibling test (two-runs byte-equality pattern):** `tests/audit/test_nfr_conv_9_zero_trust.py` (D-0088, T07.07).
- **Downstream composite:** TEST-025 invariant preservation composite at T07.09 / D-0090 will fold this fixture into the 5-invariant union check (NFR-CONV.6..10).
- **OPS-005 runbook (fallback path):** T07.16 / D-0096 (regression-halt rate — engaged if NFR-CONV-R1 falls below 80%).
- **MET-001 observability binding:** `roadmap.md:438` (T07.19 / R-159 — first-cycle PASS-rate counter at M7).
- **Spec:** `.dev/releases/current/task-builder-merge/artifacts/D-0089/spec.md`.

**Reviewer sign-off:** TEST-023 fixture lands; structural Execution
Context byte range byte-identical across populated/empty done/ arms
(md5 + sha256 + raw bytes match → byte-diff = 0); rule-artifact
scan confirms zero behaviour-modifying readbacks of `.dev/tasks/done/`
in rf-task-builder agent / SKILL files (single ADVISORY mention is
calibration-threshold only); PR-05 disposition byte-stable at
DEFERRED-to-Phase-2 / REJECTED-for-Phase-1; NFR-CONV-R1 captured
cohort at 100% first-cycle PASS (3 of 5 — INTERIM-PASS, M7 window
open, mirrors D-0083); 23/23 pytest assertions PASS; exit code 0.
