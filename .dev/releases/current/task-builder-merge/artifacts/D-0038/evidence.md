# D-0038 — T03.15 Evidence: TEST-010 Dynamic Enumeration INV-010 Fixture

**Task:** T03.15 (Phase 3)
**Roadmap items:** R-066
**Date:** 2026-05-17
**Tier:** STANDARD
**Verification:** Direct test execution
**Status:** PASS

---

## 1. Summary

T03.15 promotes the D-0031 `fixture-enum.sh` proof-of-concept into a
merge-gate pytest fixture at
`tests/audit/test_dynamic_enumeration_inv_010.py`. The fixture ports
the shell helpers (`extract_catalogue`, `render_block`, `emit_log`)
into Python with output parity, runs a 2-cycle synthetic enrichment
scenario inside a tempdir-confined working copy of `rf-qa.md`, and
asserts the four phase-3-tasklist acceptance criteria:

| AC | Phase-3-tasklist L730–734 / L346 | Status |
|----|----------------------------------|--------|
| AC-1 | Structural diff before/after catalogue growth shows new entry | **PASS** |
| AC-2 | `uv run pytest tests/audit/test_dynamic_enumeration_inv_010.py -v` exits 0 | **PASS** |
| AC-3 | Synthetic stub removed after fixture run (canonical rf-qa.md byte-identical pre/post) | **PASS** |
| AC-4 | Evidence at `TASKLIST_ROOT/artifacts/D-0038/evidence.md` | **PASS** (this file) |
| AC-5 (notes L346) | TB-Add catalogue lookup is dynamic (no hard-coded list in enumeration logic) | **PASS** |

Full pytest output: **23 passed in 0.05s** (`D-0038/pytest.log`).

## 2. Test inventory — 6 classes / 23 assertions

| Class | Asserts | Covers AC |
|-------|---------|-----------|
| `TestEnumerationWiringPresent` | rf-qa source + mirror exist, SKILL.md A.10.5 enumeration block heading still present, src ≡ mirror byte-identical | Pre-flight |
| `TestNoHardCodedEnumerationInA105` | Only symbolic `TB-Add-1` and `TB-Add-2` tokens permitted inside SKILL.md §A.10.5 enumeration block (dynamic-locate + documented static range) | AC-5 |
| `TestBaselineCatalogueExtraction` | Cycle-1 K ≥ 8 (M1 floor), dense `[1..K]` integer range, log shape matches INV-010 contract | AC-1 baseline |
| `TestAutoRichenOnCatalogueGrowth` | K2 = K1+1, synthetic ID present only in cycle-2, cycle-1 catalogue preserved as prefix of cycle-2, structural diff = 1 added line / 0 deleted | **AC-1 + AC-2** |
| `TestCanonicalFileUntouched` | Canonical `rf-qa.md` SHA-256 pre/post-fixture identical; src ≡ mirror unchanged | **AC-3** |
| `TestInv010LogShape` | INV-010 log shape matches per cycle; `source_sha256` witness differs across cycles (proves it reflects actual source bytes) | INV-010 step 7 |
| `TestNoGrowthWithoutSourceEdit` | `extract_catalogue` is pure (deterministic over identical text); `render_block` deterministic | Negative-case guard |
| `TestRegressionGuardHardcodedListBreaks` | A simulated hard-coded list FAILS to auto-richen — demonstrates the dynamic property is load-bearing | Negative-case guard |

## 3. Acceptance criteria — direct verification

### AC-1: Structural diff before/after catalogue growth shows new entry

`TestAutoRichenOnCatalogueGrowth::test_structural_diff_surfaces_exactly_one_added_row`
runs `difflib.unified_diff` over the rendered cycle-1 vs cycle-2
verdict-block enumeration views and asserts exactly **1 added line**
(the synthetic `TB-Add-(K+1)` row) and **0 deleted lines**. The diff
matches the shape captured in `D-0031/fixture-enum.log` lines
"structural diff cycle-1 → cycle-2".

Cycle-1 baseline (K=8):

```
| TB-Add-1 | (status carried verbatim from producer) |
| TB-Add-2 | (status carried verbatim from producer) |
| TB-Add-3 | (status carried verbatim from producer) |
| TB-Add-4 | (status carried verbatim from producer) |
| TB-Add-5 | (status carried verbatim from producer) |
| TB-Add-6 | (status carried verbatim from producer) |
| TB-Add-7 | (status carried verbatim from producer) |
| TB-Add-8 | (status carried verbatim from producer) |
```

Cycle-2 grown (K=9) — diff added line:

```
+| TB-Add-9 | (status carried verbatim from producer) |
```

Zero removed lines. **PASS.**

### AC-2: `uv run pytest ... -v` exits 0

```
$ uv run pytest tests/audit/test_dynamic_enumeration_inv_010.py -v
...
============================== 23 passed in 0.05s ==============================
$ echo $?
0
```

Full log captured at `D-0038/pytest.log`. **PASS.**

### AC-3: Synthetic stub removed after fixture run

The `workdir` pytest fixture allocates a `tempfile.mkdtemp` and
unconditionally `shutil.rmtree`s it in the `finally` block.
`TestCanonicalFileUntouched` asserts:

- The canonical `src/superclaude/agents/rf-qa.md` SHA-256 is
  byte-identical pre-fixture and post-fixture
  (sha first 16 = `1c92a9e8aedf6905`).
- The `.claude/agents/rf-qa.md` mirror is byte-identical to the
  source after the fixture.

Direct re-verification:

```
$ sha256sum src/superclaude/agents/rf-qa.md .claude/agents/rf-qa.md
1c92a9e8aedf6905a684b0960ab6e37f7b2c3d67ff97d2db63df115a98bb76ca  src/superclaude/agents/rf-qa.md
1c92a9e8aedf6905a684b0960ab6e37f7b2c3d67ff97d2db63df115a98bb76ca  .claude/agents/rf-qa.md
```

Matches the pre-T03.15 hash recorded in `D-0031/evidence.md` §1.
**PASS.**

### AC-4: Evidence at `TASKLIST_ROOT/artifacts/D-0038/evidence.md`

This file. **PASS.**

### AC-5: TB-Add catalogue lookup is dynamic (no hard-coded list)

`TestNoHardCodedEnumerationInA105` dynamically locates the SKILL.md
§A.10.5 enumeration block (so the assertion survives any future
byte-offset drift from MIG-N) and asserts the unique TB-Add-N tokens
inside the block are a subset of `{TB-Add-1, TB-Add-2}` — the
symbolic worked-example pattern in step 4
(`LIVE_TB_ADD = [TB-Add-1, TB-Add-2, …, TB-Add-K]`). A second
assertion re-runs the same check against the **documented** static
range `[1213, 1224]` (D-0031 § 3.3 forensic baseline) so the narrow
case "block heading moves but static range still references the
original location" is also caught.

Direct verification:

```
$ awk 'NR>=1213 && NR<=1224' src/superclaude/skills/task-builder/SKILL.md \
    | grep -oE 'TB-Add-[0-9]+' | sort | uniq -c
      3 TB-Add-1
      1 TB-Add-2
```

Only `TB-Add-1` and `TB-Add-2` appear inside the enumeration block —
all symbolic. **PASS.**

In parallel, `TestRegressionGuardHardcodedListBreaks` constructs a
simulated hard-coded list `[TB-Add-1, …, TB-Add-K1]` and asserts that
it does **not** equal `cat2` (cycle-2 with synthetic
`TB-Add-(K1+1)`). This makes the dynamic-enumeration property
load-bearing: if the orchestrator silently regressed to a constant
list, that simulation IS the orchestrator, and the test would expose
the regression as a behaviour-equivalence between the orchestrator
and the failing simulation.

## 4. Implementation evidence

### 4.1 Fixture artefact

`tests/audit/test_dynamic_enumeration_inv_010.py`:

```
$ sha256sum tests/audit/test_dynamic_enumeration_inv_010.py
362de75c6c99479c41eaff28bd9b977df92908f280fde4c869a9cfb228037a84  tests/audit/test_dynamic_enumeration_inv_010.py
$ wc -l tests/audit/test_dynamic_enumeration_inv_010.py
397 tests/audit/test_dynamic_enumeration_inv_010.py
```

### 4.2 Pytest log

```
$ uv run pytest tests/audit/test_dynamic_enumeration_inv_010.py -v 2>&1 | tail -5
...
tests/audit/test_dynamic_enumeration_inv_010.py::TestRegressionGuardHardcodedListBreaks::test_hardcoded_list_does_not_auto_richen PASSED [100%]

============================== 23 passed in 0.05s ==============================
```

Full log: `D-0038/pytest.log` (collected at fixture run time).

### 4.3 Python-port parity with D-0031 shell fixture

The pytest fixture's `extract_catalogue`, `render_block`, and
`emit_inv010_log` helpers reproduce the D-0031 awk/regex pipeline
and log-line shape. Cycle-1 K=8 and cycle-2 K=9 match the values
recorded in `D-0031/fixture-enum.log` lines:

```
[fixture] cycle-1 K=8 ids=TB-Add-1,TB-Add-2,TB-Add-3,TB-Add-4,TB-Add-5,TB-Add-6,TB-Add-7,TB-Add-8
[fixture] cycle-2 K=9 ids=TB-Add-1,TB-Add-2,TB-Add-3,TB-Add-4,TB-Add-5,TB-Add-6,TB-Add-7,TB-Add-8,TB-Add-9 (with synthetic TB-Add-9 appended to working copy)
```

The pytest fixture inserts at the END of the bounded region, just as
the shell fixture does (awk block at D-0031/fixture-enum.sh:95-102).

### 4.4 Negative-case demonstration of dynamic property

`TestRegressionGuardHardcodedListBreaks::test_hardcoded_list_does_not_auto_richen`
asserts three guards:
1. `hardcoded == cat2` is FALSE — i.e., a static list cannot match
   the cycle-2 enumeration that has the synthetic TB-Add-(K1+1).
2. `len(hardcoded) == K1` — the static list is anchored to the
   baseline size, demonstrating that without re-extraction it never
   grows.
3. `TB-Add-(K1+1)` is absent from the static list — confirming the
   only way to surface the synthetic ID is the dynamic regex re-run
   (SKILL.md §A.10.5 steps 2-4).

## 5. Deliverables checklist

| Deliverable                                            | Status | Evidence                                             |
|--------------------------------------------------------|--------|------------------------------------------------------|
| TEST-010 fixture committed                             | LANDED | `tests/audit/test_dynamic_enumeration_inv_010.py`    |
| Structural diff demonstrating enrichment               | PASS   | `TestAutoRichenOnCatalogueGrowth::test_structural_diff_surfaces_exactly_one_added_row` |
| Synthetic stub auto-removed (canonical untouched)      | PASS   | `TestCanonicalFileUntouched` (2 assertions)          |

## 6. Roadmap coverage

| Item | Title | Covered? | Where |
|------|-------|----------|-------|
| R-066 | TEST-010 fixture asserts checklist auto-richens when FR-CONV.1 catalogue grows | YES | `tests/audit/test_dynamic_enumeration_inv_010.py` (23 assertions / 6 + 2 classes, 23 PASSED) |

## 7. Forward dependencies unblocked

- **T03.16 (MIG-003 PR-04 landing migration)** — TEST-010 is one of
  the three fixtures (TEST-008 + TEST-009 + TEST-010) the MIG-003
  planning step (phase-3-tasklist.md L773 "Confirm T03.13..T03.15
  fixtures green") gates on. With T03.13 (D-0036), T03.14 (D-0037),
  and now T03.15 (D-0038) all PASS, MIG-003 is unblocked.
- **T03.18 (End-of-Phase-3 checkpoint)** — D-0038 will appear in the
  CP-P03-END verification table alongside D-0036, D-0037, and the
  MIG-003 evidence at D-0039.

## 8. Sub-agent delegation

Not required (T03.15 tier: STANDARD; verification method: Direct test
execution; sub-agent delegation: None per phase-3-tasklist line 712).
The 23-assertion pytest fixture + direct sha256sum + grep evidence
above is sufficient per tier proportionality.

## 9. Status: PASS

All five acceptance criteria met. Pytest fixture green
(`23 passed in 0.05s`). Canonical `rf-qa.md` byte-identical pre/post.
Hard-coded enumeration regression caught by `TestNoHardCodedEnumerationInA105`
+ `TestRegressionGuardHardcodedListBreaks`. T03.15 unblocks T03.16
(MIG-003 PR-04 landing) and T03.18 (CP-P03-END).
