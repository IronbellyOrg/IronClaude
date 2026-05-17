# D-0024 — T02.10 Evidence: NFR-CONV.7 Evidence-bound Preservation

**Task:** T02.10 (Phase 2)
**Roadmap items:** R-046
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Summary

The M1 TEST-003 three-fixture triple (bare-path FAIL / file:line PASS
/ justified-absence PASS) has been re-run against three M2-style MDTM
fixtures that carry the FR-CONV.2 `## Execution Context` header. The
verdict matrix is byte-identical to the M1 baseline, TB-Add-8 error
citations continue to point at per-item Context fields rather than at
the header byte range, and the NFR-CONV.7 evidence-bound-item
invariant is preserved post-M2.

## 2. Artifacts landed

| Path | Role |
|---|---|
| `tests/audit/fixtures/execution_context/evidence_bound_bare_path.md` | M2 fixture (a) — bare module path in per-item Context (TB-Add-8 must FAIL) |
| `tests/audit/fixtures/execution_context/evidence_bound_file_line.md` | M2 fixture (b) — `file:line` citation in per-item Context (TB-Add-8 must PASS) |
| `tests/audit/fixtures/execution_context/evidence_bound_justified_absence.md` | M2 fixture (c) — `<!-- evidence-absence: ... -->` justification (TB-Add-8 must PASS) |
| `tests/audit/test_evidence_bound_tb_add_8.py` | TB-Add-8 verifier mirroring rf-qa.md:310; 10-case pytest suite |

Each fixture file independently satisfies the M2 header invariants
(begins with frontmatter, contains a `## Execution Context` block with
the three DM-001 labeled bullets, places the block between frontmatter
and the first `### TPP.TT` task) — verified by the
`test_all_fixtures_carry_m2_execution_context_header` precondition
test.

## 3. TB-Add-8 verifier implementation

The verifier in `test_evidence_bound_tb_add_8.py` re-implements the
TB-Add-8 rule from `src/superclaude/agents/rf-qa.md:310` as executable
Python:

| Step | Rule clause | Implementation |
|---|---|---|
| Header exemption | "the block itself MUST NOT contain specific path.py:NN references; per-item Context fields are the correct venue" | `_header_range()` skips lines between the `## Execution Context` heading and its closing `---` separator before TB-Add-8 enumerates Context paragraphs (`tests/audit/test_evidence_bound_tb_add_8.py:74-79`). |
| Per-item Context enumeration | "Every per-item Context field…" | `_iter_per_item_context()` extracts the `- **Context**: …` sub-bullet under each `- [ ] **N.M — …**` checklist entry (`tests/audit/test_evidence_bound_tb_add_8.py:85-122`). |
| Code-surface heuristic | "references a code surface (a function, class, module, config field, or specific file)" | `CODE_SURFACE_RE` — matches `src/…` module paths, `*.py` / `*.md` tokens, and backtick-wrapped `file:line` patterns (`tests/audit/test_evidence_bound_tb_add_8.py:35`). |
| FAIL discriminator | "MUST include at least one file:line citation OR a `<!-- evidence-absence: ... -->` justified-absence comment" | `FILE_LINE_RE` (`\S+\.\w+:\d+`) and `EVIDENCE_ABSENCE_RE` (`<!--\s*evidence-absence:`) — when neither matches, FAIL is emitted (`tests/audit/test_evidence_bound_tb_add_8.py:33-34, 125-167`). |
| Error citation | "Item X.Y Context references `[surface]` but contains no file:line citation and no evidence-absence justification" | Result carries `f"Item {item.item_id} Context (line {item.line_number})"` — line index is always outside the header range (`tests/audit/test_evidence_bound_tb_add_8.py:161-168`). |

## 4. Test execution

```
$ uv run pytest tests/audit/test_evidence_bound_tb_add_8.py -v
...
collected 10 items

tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_bare_path_fixture_exists PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_file_line_fixture_exists PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_justified_absence_fixture_exists PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_all_fixtures_carry_m2_execution_context_header PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_bare_path_fails_tb_add_8 PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_file_line_passes_tb_add_8 PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8ThreeFixtureTriple::test_justified_absence_passes_tb_add_8 PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8CitesPerItemContextNotHeader::test_bare_path_error_cites_per_item_context_line PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8CitesPerItemContextNotHeader::test_header_range_never_yields_tb_add_8_verdict PASSED
tests/audit/test_evidence_bound_tb_add_8.py::TestTBAdd8VerdictMatrixMatchesM1Baseline::test_verdict_matrix PASSED

============================== 10 passed in 0.03s ==============================
```

Exit code: 0.

## 5. Verdict matrix vs M1 baseline

| Fixture | M1 expected verdict | M2 observed verdict | Drift |
|---|---|---|---|
| `evidence_bound_bare_path.md` (a) — bare path | FAIL | **FAIL** | none |
| `evidence_bound_file_line.md` (b) — `file:line` | PASS | **PASS** | none |
| `evidence_bound_justified_absence.md` (c) — justified absence | PASS | **PASS** | none |

The matrix is byte-identical to the M1 baseline declared in
`.dev/releases/current/task-builder-merge/roadmap.compressed.md:85`
("bare-src/foo:FAIL; src/foo:42:PASS; justified-absence:PASS") and in
`.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.compressed.md:355`.
Validated by `TestTBAdd8VerdictMatrixMatchesM1Baseline::test_verdict_matrix`
(asserting `{bare_path: FAIL, file_line: PASS, justified_absence: PASS}`
verbatim).

## 6. Citation-scope invariant

Two tests structurally PROVE TB-Add-8 cites per-item Context fields,
not the M2 header:

1. `test_bare_path_error_cites_per_item_context_line` — for the
   bare-path fixture, every FAIL result carries
   `cited_location = "Item 1.1 Context (line N)"`, and the line index N
   is asserted to fall OUTSIDE the `## Execution Context` header range
   `[start, end]`.
2. `test_header_range_never_yields_tb_add_8_verdict` — across all three
   fixtures, the verifier is asserted to never produce a Context
   verdict (PASS or FAIL) whose line index sits inside the header
   range. The header is structurally exempt by design (NFR-CONV.3
   hidden-input determinism).

This satisfies the rf-qa.md:310 invariant: *"per-item Context fields
are the correct venue for file:line citations"*.

## 7. NFR-CONV.7 preservation report

| Invariant clause (roadmap.compressed.md:157) | Status post-M2 | Evidence |
|---|---|---|
| Per-item Context fields MUST retain `file:line` citations | **PRESERVED** | `evidence_bound_file_line.md` PASSes against M2 header — § 5 |
| OR `<!-- evidence-absence: ... -->` justified-absence comments | **PRESERVED** | `evidence_bound_justified_absence.md` PASSes against M2 header — § 5 |
| Three-fixture-triple: bare-FAILS, file:line-PASSES, justified-absence-PASSES | **PRESERVED** | Matrix byte-identical to M1 baseline — § 5 |
| Integration with TB-Add-8 verified | **VERIFIED** | 10 tests / 10 PASS — § 4 |
| Validated by TB-Add-8 from M1 | **CONFIRMED** | Verifier mirrors rf-qa.md:310 verbatim — § 3 |
| Header introduction does not relocate evidence binding | **CONFIRMED** | `test_header_range_never_yields_tb_add_8_verdict` — § 6 |

**Verdict: NFR-CONV.7 preserved post-M2.** The FR-CONV.2 `## Execution
Context` header (introduced by tasks T02.01-T02.09) is fully
orthogonal to TB-Add-8's per-item Context enforcement: the header
range is structurally exempt from the file:line scan; per-item Context
paragraphs continue to require either a `file:line` citation or an
`<!-- evidence-absence: ... -->` justification; and the bare-path
FAIL verdict still triggers with an error citation that names the
per-item Context line, not the header.

## 8. Acceptance-criteria mapping

| AC | Criterion | Status | Evidence |
|---|---|---|---|
| AC1 | TEST-003 triple re-run produces FAIL/PASS/PASS verdicts unchanged from M1 | **PASS** | § 5 — matrix byte-identical; § 4 — 10/10 tests green |
| AC2 | TB-Add-8 error citations refer to per-item Context fields, not the header | **PASS** | § 6 — two structural tests; `test_bare_path_error_cites_per_item_context_line` + `test_header_range_never_yields_tb_add_8_verdict` |
| AC3 | NFR-CONV.7 preservation report written to `TASKLIST_ROOT/artifacts/D-0024/evidence.md` | **PASS** | This file |
| AC4 | Per-item Context fields retain `file:line` form post-M2 | **PASS** | § 7 — file:line and justified-absence branches both preserved |

## 9. Dependencies satisfied

- T02.09 (D-0023) PASS — TEST-004..006 fixtures committed (M2 header
  structure frozen for fixture authoring).
- Phase 1 TB-Add-8 rule landings — `rf-qa.md:310`, `SKILL.md:1073`,
  `SKILL.md:1826` all present in source-of-truth.

## 10. Unblocks

- T02.11 — MIG-002 PR-01 landing migration.
- T02.12 — Phase 2 end checkpoint (CP-P02-END).

## 11. Verdict

**PASS** — All 4 acceptance criteria satisfied; 10/10 tests green;
TB-Add-8 verdict matrix preserved byte-identically against M2-generated
MDTM; NFR-CONV.7 evidence-bound-item invariant confirmed preserved.
