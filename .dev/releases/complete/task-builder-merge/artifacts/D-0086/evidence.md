# D-0086 — T07.04 Evidence: NFR-CONV.6 Self-Contained-Item Fixture

**Task:** T07.04 (Phase 7 — M7)
**Roadmap items:** R-143
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct test execution (`uv run pytest`)
**Overall: PASS** (5/5 acceptance criteria met)

---

## 0. TL;DR

NFR-CONV.6 self-contained-item invariant holds. The composite fixture
exercises the Q-DM-1 resolved 5-field per-item schema —
`{Context, Action, Output, Verification, Completion gate}` — in two
variants:

- **Full-fields variant** (`tests/audit/fixtures/nfr_conv_6/full_fields.md`)
  — every checklist item populates all five fields. TB-Add-1..8 catalogue
  emits **PASS** for every check.
- **Field-stripped variant** (`tests/audit/fixtures/nfr_conv_6/stripped.md`)
  — item `1.1` has the `**Output**` field deliberately removed. TB-Add-1
  **FAILs** with both the item-ID (`1.1`) and the missing field label
  (`Output`) named in the error message.

The fixture's schema reference is machine-checked against the production
TB-Add-1 rule body at `src/superclaude/agents/rf-qa.md:296`: if the rule
text drifts away from `{Context, Action, Output, Verification,
Completion-gate}` the test fails before any verdict assertion is run.

---

## 1. Q-DM-1 resolution binding

The Q-DM-1 schema contradiction (PRD §25.4 declared
`{Description, Context, Acceptance, Confidence, Verification}` while the
SKILL.md source carried `{Context, Action, Output, Verification,
Completion gate}`) was resolved in favour of preserving the existing
SKILL.md schema. The resolution is recorded in the production rule
body for TB-Add-1 at `src/superclaude/agents/rf-qa.md:296`:

> No checklist item contains the literal tokens `TBD`, `TODO`, or
> `FIXME` in its description or body, and no item is title-only (it
> MUST have a Context, Action, Output, Verification, and
> Completion-gate body).

The fixture's frontmatter `related_docs` block cites this resolution
verbatim. The test `TestQDm1SchemaCrossCheck::test_rf_qa_schema_matches_expected`
re-parses the rule body and asserts the field-set is byte-identical to
the expected `SCHEMA_FIELDS` tuple. The hyphen variant `Completion-gate`
in the production rule is normalised to the rendered Markdown label
`Completion gate` used by the fixture; the test exposes any further
drift immediately.

## 2. Fixture inventory

| Variant | Path | Items | Intent |
|---|---|---|---|
| Full-fields | `tests/audit/fixtures/nfr_conv_6/full_fields.md` | 3 | Every item carries `{Context, Action, Output, Verification, Completion gate}`; no placeholder tokens; per-item Context fields cite file:line. |
| Field-stripped | `tests/audit/fixtures/nfr_conv_6/stripped.md` | 3 | Item `1.1` omits the `**Output**` field; items `1.2`/`1.3` remain fully populated. |

Both fixtures share the same `## Execution Context` header with three
named source areas (`rf-qa agent prompt`, `task-builder skill body`,
`MDTM output structure template`) so TB-Add-7 cross-validates the same
header-to-item drift surface on both inputs.

## 3. Test inventory

`tests/audit/test_nfr_conv_6_self_contained.py` ships 4 test classes:

1. `TestFixturesExist` — both fixture files present on disk.
2. `TestQDm1SchemaCrossCheck` — production TB-Add-1 rule body matches the
   `{Context, Action, Output, Verification, Completion gate}` field-set
   (`rf-qa.md:296`); both fixtures declare the schema in their bodies.
3. `TestFullFieldsAllPass` — full-fields variant produces PASS for every
   TB-Add-1..8 check (aggregate-PASS plus the stronger "no FAIL emitted
   on any individual check" assertion).
4. `TestStrippedFailsTBAdd1` — stripped variant emits a TB-Add-1 FAIL
   that names both item `1.1` and field `Output`; items `1.2`/`1.3`
   continue to PASS TB-Add-1; TB-Add-2..7 remain PASS overall.

## 4. Acceptance-criteria mapping (phase-7-tasklist.md L186-191)

| AC | Criterion | Status | Evidence § |
|----|-----------|--------|------------|
| AC1 | `uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -v` exits 0 | **PASS** | §5 |
| AC2 | Full-fields variant passes all 8 TB-Add checks | **PASS** | §3 (`TestFullFieldsAllPass`), §5 |
| AC3 | One-field-stripped variant fails TB-Add-1 with named field-ID | **PASS** | §3 (`TestStrippedFailsTBAdd1::test_tb_add_1_fails_with_item_and_field`), §5 |
| AC4 | Fixture's schema reference matches the recorded Q-DM-1 resolution artifact (machine-checkable) | **PASS** | §1, §3 (`TestQDm1SchemaCrossCheck`), §5 |
| AC5 | Evidence at `TASKLIST_ROOT/artifacts/D-0086/evidence.md` | **PASS** (this file) | — |

## 5. Test run output

```bash
$ uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
SuperClaude: 4.2.0
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 10 items

tests/audit/test_nfr_conv_6_self_contained.py::TestFixturesExist::test_full_fields_fixture_exists PASSED [ 10%]
tests/audit/test_nfr_conv_6_self_contained.py::TestFixturesExist::test_stripped_fixture_exists PASSED [ 20%]
tests/audit/test_nfr_conv_6_self_contained.py::TestQDm1SchemaCrossCheck::test_rf_qa_schema_matches_expected PASSED [ 30%]
tests/audit/test_nfr_conv_6_self_contained.py::TestQDm1SchemaCrossCheck::test_full_fields_fixture_declares_schema PASSED [ 40%]
tests/audit/test_nfr_conv_6_self_contained.py::TestQDm1SchemaCrossCheck::test_stripped_fixture_declares_schema_intent PASSED [ 50%]
tests/audit/test_nfr_conv_6_self_contained.py::TestFullFieldsAllPass::test_aggregate_pass PASSED [ 60%]
tests/audit/test_nfr_conv_6_self_contained.py::TestFullFieldsAllPass::test_no_check_emits_fail PASSED [ 70%]
tests/audit/test_nfr_conv_6_self_contained.py::TestStrippedFailsTBAdd1::test_tb_add_1_fails_with_item_and_field PASSED [ 80%]
tests/audit/test_nfr_conv_6_self_contained.py::TestStrippedFailsTBAdd1::test_other_items_pass_tb_add_1 PASSED [ 90%]
tests/audit/test_nfr_conv_6_self_contained.py::TestStrippedFailsTBAdd1::test_tb_add_2_through_8_unaffected_for_intact_items PASSED [100%]

============================== 10 passed in 0.03s ==============================
```

Exit code: `0`. All 10 assertions PASS.

## 6. Failure-mode reproducibility

The negative-path semantics (`Output` field stripped) are reproducible
by hand:

```bash
$ grep -n '**Output**' tests/audit/fixtures/nfr_conv_6/stripped.md
# (Item 1.1 omits the Output bullet; items 1.2 and 1.3 carry it.)
$ grep -n '**Output**' tests/audit/fixtures/nfr_conv_6/full_fields.md
# (All three items carry the Output bullet.)
```

The TB-Add-1 checker in `tests/audit/test_nfr_conv_6_self_contained.py`
parses each `- [ ] **N.M — title**` bullet, captures its `**Field**:`
sub-bullets, and reports a FAIL whose detail names the item-ID and the
missing-field list. Restoring the `**Output**` bullet to item `1.1`
flips the verdict to PASS.

## 7. Cross-references

- **NFR-CONV.6 roadmap row:** §M7 row R-143 — "synthetic fixture with
  all 5 fields populated PASSES all 8 TB-Add checks; same fixture with
  one field stripped FAILS TB-Add-1".
- **Q-DM-1 resolution anchor:** `src/superclaude/agents/rf-qa.md:296`
  (TB-Add-1 rule body listing the 5 field names).
- **SKILL.md mirror:** `src/superclaude/skills/task-builder/SKILL.md:1134`
  (TB-Add-1 catalogue entry).
- **Companion fixture pattern:** `tests/audit/test_evidence_bound_tb_add_8.py`
  + `tests/audit/fixtures/execution_context/evidence_bound_*.md` (the
  three-fixture triple used by NFR-CONV.7 / T02.10 / D-0024).
- **Cross-cutting composite (downstream):** TEST-025 invariant
  preservation composite at T07.09 / D-0090 will fold this fixture
  into the 5-invariant union check (NFR-CONV.6..10).

**Reviewer sign-off:** NFR-CONV.6 self-contained-item invariant fixture
landed; full-fields → 8/8 PASS; stripped → TB-Add-1 FAIL with item-ID
and field-ID named; schema reference machine-checked against the
recorded Q-DM-1 resolution.
