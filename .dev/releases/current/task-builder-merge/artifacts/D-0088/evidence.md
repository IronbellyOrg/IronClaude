# D-0088 — T07.07 Evidence: NFR-CONV.9 + NFR-CONV.2

**Task:** T07.07 (Phase 7 — M7)
**Roadmap items:** R-145 (NFR-CONV.9), R-146 (NFR-CONV.2)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STRICT
**Verification method:** Sub-agent (quality-engineer) + direct test execution (`uv run pytest`)
**Overall: PASS** (4/4 acceptance criteria met)

---

## 0. TL;DR

NFR-CONV.9 two-part fixture lands. The 1-LOW-finding fixture FAILs
the rf-qa research-completeness gate; the inherited-verdict /
zero-semantic-check fixture is flagged inflation-positive by the
K-003 audit recipe. NFR-CONV.2 documentation page is published
with the structural-vs-prose boundary enumerated.

The invariant anchor — verbatim PASS / FAIL definitions in
`src/superclaude/agents/rf-qa.md` — is byte-identical from the
baseline commit (`fd41178`, pre-FR-CONV.*) through post-M5
(`db6166e`), post-M6 (`87c8254`), and HEAD. The line index drifted
from `:141-142` to `:144-145` because PR-03 added three earlier
lines; the *bytes* of each line are unchanged.

Quality-engineer sub-agent (STRICT-tier required) audited the
deliverable independently and returned Verdict: PASS — see
`sub-agent-report.md`.

---

## 1. Deliverables (file inventory)

| Path | SHA-256 hint | Purpose |
|---|---|---|
| `tests/audit/test_nfr_conv_9_zero_trust.py` | new | 35 assertions across 6 classes verifying the two-part fixture + invariant anchor + doc presence. |
| `tests/audit/fixtures/nfr_conv_9/one_low_finding.md` | new | NFR-CONV.9 part (a) FAIL fixture — 1 MINOR gap. |
| `tests/audit/fixtures/nfr_conv_9/zero_findings_baseline.md` | new | Part (a) positive twin — 0 gaps. |
| `tests/audit/fixtures/nfr_conv_9/inherited_verdict_no_semantic.md` | new | Part (b) FAIL fixture — VERIFIED + 0 category-(b). |
| `tests/audit/fixtures/nfr_conv_9/inherited_verdict_with_semantic.md` | new | Part (b) positive twin — VERIFIED + ≥1 category-(b). |
| `docs/reference/nfr-conv-2-prose-determinism.md` | new | NFR-CONV.2 boundary documentation page. |
| `.dev/releases/current/task-builder-merge/artifacts/D-0088/spec.md` | new | T07.07 spec (this deliverable). |
| `.dev/releases/current/task-builder-merge/artifacts/D-0088/sub-agent-report.md` | new | STRICT-tier sub-agent verification report. |
| `.dev/releases/current/task-builder-merge/artifacts/D-0088/evidence.md` | (this file) | Evidence + cross-references. |

## 2. Acceptance-criteria mapping (phase-7-tasklist.md L335-339)

| AC | Criterion | Status | Evidence § |
|----|-----------|--------|------------|
| AC1 | Both fixture parts pass per spec | **PASS** | §3 (pytest run, 35/35 assertions PASS) |
| AC2 | Byte-diff of rf-qa.md PASS/FAIL definitions pre/post M5+M6 is zero | **PASS** | §4 (cross-commit md5 + grep) |
| AC3 | NFR-CONV.2 documentation page exists with structural-vs-prose boundary enumerated | **PASS** | §5 (doc surface enumeration); sub-agent §5 |
| AC4 | Sub-agent report confirms structural annotations within prose remain byte-equal across 2 runs | **PASS** | §6 (test class + md5); sub-agent §4 |

## 3. Test execution

```
$ uv run pytest tests/audit/test_nfr_conv_9_zero_trust.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
SuperClaude: 4.2.0
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 35 items

tests/audit/test_nfr_conv_9_zero_trust.py::TestFixturesExist::test_one_low_finding_fixture_exists PASSED                          [  2%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestFixturesExist::test_zero_findings_baseline_fixture_exists PASSED                  [  5%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestFixturesExist::test_inherited_verdict_no_semantic_fixture_exists PASSED           [  8%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestFixturesExist::test_inherited_verdict_with_semantic_fixture_exists PASSED         [ 11%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestFixturesExist::test_nfr_conv_2_doc_published PASSED                               [ 14%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_pass_bullet_present_in_source PASSED           [ 17%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_fail_bullet_present_in_source PASSED           [ 20%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_pass_bullet_present_in_mirror PASSED           [ 22%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_fail_bullet_present_in_mirror PASSED           [ 25%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_severity_triple_intact PASSED                  [ 28%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_source_and_mirror_byte_identical PASSED        [ 31%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_pass_and_fail_bullets_are_adjacent PASSED      [ 34%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartA_OneLowFindingFailsGate::test_fixture_contains_one_minor_gap PASSED          [ 37%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartA_OneLowFindingFailsGate::test_gate_returns_fail PASSED                       [ 40%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartA_OneLowFindingFailsGate::test_fixture_is_self_documenting PASSED             [ 42%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartA_ZeroFindingsBaselinePasses::test_fixture_contains_zero_gaps PASSED          [ 45%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartA_ZeroFindingsBaselinePasses::test_gate_returns_pass PASSED                   [ 48%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithoutSemanticIsInflation::test_self_audit_heading_present PASSED [ 51%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithoutSemanticIsInflation::test_report_claims_verified_items PASSED [ 54%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithoutSemanticIsInflation::test_zero_category_b_bullets PASSED [ 57%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithoutSemanticIsInflation::test_audit_recipe_flags_inflation PASSED [ 60%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithoutSemanticIsInflation::test_negative_marker_present PASSED [ 62%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithSemanticIsClean::test_self_audit_heading_present PASSED [ 65%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithSemanticIsClean::test_at_least_one_category_b PASSED    [ 68%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestPartB_InheritedVerdictWithSemanticIsClean::test_audit_recipe_does_not_flag PASSED [ 71%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestStructuralAnnotationsByteEqualAcrossRuns::test_two_reads_byte_equal[one_low_finding.md] PASSED [ 74%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestStructuralAnnotationsByteEqualAcrossRuns::test_two_reads_byte_equal[zero_findings_baseline.md] PASSED [ 77%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestStructuralAnnotationsByteEqualAcrossRuns::test_two_reads_byte_equal[inherited_verdict_no_semantic.md] PASSED [ 80%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestStructuralAnnotationsByteEqualAcrossRuns::test_two_reads_byte_equal[inherited_verdict_with_semantic.md] PASSED [ 82%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestStructuralAnnotationsByteEqualAcrossRuns::test_structural_annotations_extractable PASSED [ 85%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestNfrConv2DocumentationPage::test_doc_names_nfr_conv_2 PASSED                       [ 88%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestNfrConv2DocumentationPage::test_doc_enumerates_structural_side PASSED             [ 91%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestNfrConv2DocumentationPage::test_doc_enumerates_prose_side PASSED                  [ 94%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestNfrConv2DocumentationPage::test_doc_cross_references_rf_qa_pass_fail PASSED       [ 97%]
tests/audit/test_nfr_conv_9_zero_trust.py::TestNfrConv2DocumentationPage::test_doc_references_m7_audit PASSED                    [100%]

============================== 35 passed in 0.04s ==============================
```

Exit code: `0`. All 35 assertions PASS.

## 4. Invariant anchor: rf-qa.md PASS/FAIL byte-equality across milestones

Per AC2: "Byte-diff of rf-qa.md:141-142 PASS/FAIL definitions
pre/post M5+M6 is zero." The roadmap anchored these at lines
`141-142` in the pre-FR-CONV.* baseline (`fd41178`). After PR-03
(`dfae6cf`) added three earlier lines, they sit at `:144-145` in
HEAD. The *content* of each bullet is byte-identical across all
milestones:

```
$ for ref in fd41178 db6166e 87c8254 HEAD; do
>   git show $ref:src/superclaude/agents/rf-qa.md | grep -nE '^- \*\*(PASS|FAIL)\*\*'
> done
=== fd41178 (baseline, pre-FR-CONV.*) ===
141:- **PASS** — All checks pass, no gaps of any severity. Green light for synthesis.
142:- **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). List each gap with a specific remediation action. ALL gaps must be resolved before proceeding — no severity level is exempt.
=== db6166e (post-M5) ===
144:- **PASS** — All checks pass, no gaps of any severity. Green light for synthesis.
145:- **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). List each gap with a specific remediation action. ALL gaps must be resolved before proceeding — no severity level is exempt.
=== 87c8254 (post-M6) ===
144:- **PASS** — All checks pass, no gaps of any severity. Green light for synthesis.
145:- **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). List each gap with a specific remediation action. ALL gaps must be resolved before proceeding — no severity level is exempt.
=== HEAD ===
144:- **PASS** — All checks pass, no gaps of any severity. Green light for synthesis.
145:- **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). List each gap with a specific remediation action. ALL gaps must be resolved before proceeding — no severity level is exempt.
```

md5 of each bullet text across the four refs:

| ref | PASS md5 | FAIL md5 |
|---|---|---|
| `fd41178` (baseline) | `705536d8a8ec67fef6e56f74fb5093fb` | `d959dffa6d80319d6215470b43288884` |
| `db6166e` (post-M5) | `705536d8a8ec67fef6e56f74fb5093fb` | `d959dffa6d80319d6215470b43288884` |
| `87c8254` (post-M6) | `705536d8a8ec67fef6e56f74fb5093fb` | `d959dffa6d80319d6215470b43288884` |
| `HEAD` | `705536d8a8ec67fef6e56f74fb5093fb` | `d959dffa6d80319d6215470b43288884` |

Byte-diff = 0 across all four refs. AC2 holds.

src↔mirror parity confirmed:

```
$ diff src/superclaude/agents/rf-qa.md .claude/agents/rf-qa.md && echo "SYNC OK"
SYNC OK
```

## 5. NFR-CONV.2 documentation surface enumeration

`docs/reference/nfr-conv-2-prose-determinism.md` (~140 lines, 6
sections) carries:

- **§1 Why a determinism boundary exists** — frames the two-axis
  split (structural fields byte-deterministic vs LLM-prose
  nondeterminism acceptable) and cites the roadmap REJECTED
  alternatives (full byte-determinism, zero-determinism).
- **§2.1 Structural fields (byte-deterministic — NFR-CONV.1)** —
  11-row table enumerating item identifiers, schema field names,
  verdict labels, severity labels, Self-Audit heading,
  Inherited-Verdict block header, axis (PR-07) labels, dedup-key
  strings, finding counts, reliance bullets, independent-semantic-check
  labels.
- **§2.2 Research-driven prose (nondeterminism acceptable —
  NFR-CONV.2)** — 6-row table enumerating item `Why` wording,
  item `Notes`, research-file Summary prose, gap-description
  prose, Self-Audit category-(b) bullet content, Issues Found
  body.
- **§3 Structural annotations embedded inside prose** — 6-row
  table covering the boundary case (axis labels, finding counts,
  dedup-keys, verdict labels, severity labels, `file:line`
  citations) with byte-equal requirements.
- **§4 Determinism contracts the boundary preserves** — 7-row
  table linking each contract to its source row and the holding
  fixture.
- **§5 What this boundary excludes** — clarifies negative scope.
- **§6 Cross-references** — pointers back to PRD anchor, roadmap
  rows, invariant anchor, Self-Audit floor, fixtures, downstream
  composite.

AC3 holds: the documentation page exists and the structural-vs-prose
boundary is enumerated three ways (structural fields, prose
surfaces, structural annotations embedded in prose).

## 6. Structural-annotations byte-equal across 2 runs

The `TestStructuralAnnotationsByteEqualAcrossRuns` class
parametrises across all four fixtures and asserts two
`Path.read_bytes()` calls return identical bytes; the
`test_structural_annotations_extractable` test runs the verdict
scorer over two reads and asserts both runs produce `FAIL`.

Manual md5 spot-check (from sub-agent report §4):

```
$ md5sum tests/audit/fixtures/nfr_conv_9/one_low_finding.md
81807a5d4b2694d36d6193d1206ebf2d  …
$ md5sum tests/audit/fixtures/nfr_conv_9/one_low_finding.md
81807a5d4b2694d36d6193d1206ebf2d  …
```

AC4 holds.

## 7. Sub-agent verification (STRICT-tier requirement)

Sub-agent type: `quality-engineer`. Report path:
`.dev/releases/current/task-builder-merge/artifacts/D-0088/sub-agent-report.md`.
Verdict: **PASS**.

Sub-agent independently executed all seven checks (test run,
cross-commit byte-equality, src↔mirror parity, two-run byte
equality, doc-surface enumeration, fixture intent spot-check,
detector reuse audit) and found no defects.

## 8. Failure-mode reproducibility

The negative-path semantics of each fixture are reproducible by
hand:

```
$ grep -nE '\| GAP \|' tests/audit/fixtures/nfr_conv_9/one_low_finding.md
25:| 6 | Gap severity | GAP | MINOR | One naming-convention note in `auth-middleware.md` could be tightened (`session_id` vs `sessionId`). …

$ grep -c 'verified by' tests/audit/fixtures/nfr_conv_9/inherited_verdict_no_semantic.md
0
$ grep -c 'verified by' tests/audit/fixtures/nfr_conv_9/inherited_verdict_with_semantic.md
2
```

Removing the gap row from `one_low_finding.md` flips the gate
verdict to PASS (breaks NFR-CONV.9 part (a)); adding a
`verified by …` bullet to `inherited_verdict_no_semantic.md`'s
category-(b) section flips it to non-inflation (breaks NFR-CONV.9
part (b)). Both negative fixtures carry the explicit
`INV-019 violation` / `NFR-CONV.9 part (a)` self-documenting
markers to prevent accidental "fixing".

## 9. Cross-references

- **NFR-CONV.9 roadmap row:** `roadmap.md:424` (R-145).
- **NFR-CONV.2 roadmap row:** `roadmap.md:425` (R-146).
- **Invariant anchor:** `src/superclaude/agents/rf-qa.md:144-145`
  (baseline `:141-142` — content byte-identical across all M1..M6
  commits).
- **rf-qa-qualitative INV-019 schema:** `src/superclaude/agents/rf-qa-qualitative.md:823-889`
  + `:893-964` (T03.04 / T03.10).
- **K-003 audit recipe source:** `tests/audit/test_self_audit_inv_019.py`
  (D-0037 — detectors `_self_audit_present`, `_count_category_b_bullets`,
  `_inflation_positive` reused by D-0088).
- **NFR-CONV.2 doc:** `docs/reference/nfr-conv-2-prose-determinism.md`.
- **Companion fixture pattern:** `tests/audit/test_nfr_conv_6_self_contained.py`
  (D-0086 / T07.04) — same shape (positive-and-negative twin variants).
- **Downstream composite:** TEST-025 invariant preservation composite
  at T07.09 / D-0090 will fold this fixture into the 5-invariant union
  check (NFR-CONV.6..10).
- **Sub-agent report:** `.dev/releases/current/task-builder-merge/artifacts/D-0088/sub-agent-report.md`.
- **Spec:** `.dev/releases/current/task-builder-merge/artifacts/D-0088/spec.md`.

**Reviewer sign-off:** NFR-CONV.9 zero-trust QA invariant fixture
PASS; FR-CONV.3 inherited-verdict guard PASS; NFR-CONV.2
documentation page published with structural-vs-prose boundary
enumerated; rf-qa.md PASS/FAIL anchor byte-identical pre/post
M5+M6; STRICT-tier sub-agent (quality-engineer) verdict PASS.
