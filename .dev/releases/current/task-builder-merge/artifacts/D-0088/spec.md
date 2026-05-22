# D-0088 — T07.07 Spec: NFR-CONV.9 + NFR-CONV.2

**Task:** T07.07 (Phase 7 — M7)
**Roadmap items:** R-145 (NFR-CONV.9), R-146 (NFR-CONV.2)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STRICT
**Verification method:** Sub-agent (quality-engineer) + direct test execution
**Overall: PASS**

---

## 1. Scope

This deliverable lands the M7 audit artifacts for the two NFR rows
that anchor the zero-trust QA invariant and the determinism scope
split:

- **R-145 / NFR-CONV.9** — Zero-trust QA invariant verification via
  a two-part fixture:
  - **Part (a)** — a research-completeness verification report
    carrying exactly one MINOR-severity gap MUST FAIL the rf-qa
    gate (rule body at `src/superclaude/agents/rf-qa.md:144-145`:
    "Any gaps exist (CRITICAL, IMPORTANT, or MINOR) … ALL gaps must
    be resolved before proceeding — no severity level is exempt").
  - **Part (b)** — the FR-CONV.3 inherited-structural-verdict
    workflow MUST NOT mark any item VERIFIED unless the Self-Audit
    section carries ≥ 1 category-(b) independent semantic check
    (INV-019 floor).
- **R-146 / NFR-CONV.2** — A published documentation page
  enumerating the structural-vs-prose determinism boundary:
  structural fields byte-deterministic (NFR-CONV.1), research-prose
  nondeterminism acceptable, structural annotations embedded inside
  prose remain byte-equal across two runs of the same input.

The invariant anchor that both rows depend on is the verbatim PASS /
FAIL bullet pair in `src/superclaude/agents/rf-qa.md`. The roadmap
row pins them at `:141-142` (the baseline commit `fd41178`
location). The bullet content is byte-identical across all nine
intervening commits through HEAD; the line index has drifted to
`:144-145` because PR-03 (`dfae6cf`) added three earlier lines, but
the bytes are unchanged.

## 2. Deliverables

| Artifact | Path | Purpose |
|---|---|---|
| Test (NFR-CONV.9 two-part + NFR-CONV.2 doc enforcement) | `tests/audit/test_nfr_conv_9_zero_trust.py` | 35 assertions across 6 classes. |
| Fixture — Part (a) FAIL | `tests/audit/fixtures/nfr_conv_9/one_low_finding.md` | 1 MINOR gap → gate FAIL. |
| Fixture — Part (a) baseline | `tests/audit/fixtures/nfr_conv_9/zero_findings_baseline.md` | 0 gaps → gate PASS. |
| Fixture — Part (b) FAIL | `tests/audit/fixtures/nfr_conv_9/inherited_verdict_no_semantic.md` | VERIFIED + 0 category-(b) → inflation-positive. |
| Fixture — Part (b) baseline | `tests/audit/fixtures/nfr_conv_9/inherited_verdict_with_semantic.md` | VERIFIED + ≥1 category-(b) → not flagged. |
| Documentation — NFR-CONV.2 | `docs/reference/nfr-conv-2-prose-determinism.md` | Structural-vs-prose boundary enumerated. |
| Sub-agent verification report | `.dev/releases/current/task-builder-merge/artifacts/D-0088/sub-agent-report.md` | Quality-engineer audit (STRICT tier). |

## 3. Test design

`tests/audit/test_nfr_conv_9_zero_trust.py` contains six test
classes mirroring the acceptance shape:

1. `TestFixturesExist` — all four fixtures + the NFR-CONV.2 doc
   are present on disk.
2. `TestPassFailBulletsByteIdentical` — the verbatim PASS / FAIL
   bullet strings appear in both `src/` and `.claude/` rf-qa.md;
   they sit on consecutive lines; the `(CRITICAL, IMPORTANT, MINOR)`
   severity triple is intact; source and mirror are byte-equal.
3. `TestPartA_OneLowFindingFailsGate` — fixture carries exactly
   1 gap classified MINOR; the gate scorer returns FAIL; the
   fixture carries the self-documenting `NFR-CONV.9 part (a)`
   marker.
4. `TestPartA_ZeroFindingsBaselinePasses` — baseline twin with
   0 gaps PASSES, anchoring the positive arm.
5. `TestPartB_InheritedVerdictWithoutSemanticIsInflation` — the
   K-003 audit recipe (reused from `test_self_audit_inv_019.py` —
   `_self_audit_present`, `_count_category_b_bullets`,
   `_inflation_positive`) flags a VERIFIED-with-zero-category-(b)
   report as inflation-positive.
6. `TestPartB_InheritedVerdictWithSemanticIsClean` — positive twin
   with ≥1 category-(b) bullet is NOT flagged.
7. `TestStructuralAnnotationsByteEqualAcrossRuns` — each fixture
   read twice yields byte-identical bytes; the verdict scored
   from two reads of `one_low_finding.md` is byte-identical
   (`FAIL` in both runs).
8. `TestNfrConv2DocumentationPage` — the published doc names
   NFR-CONV.2, enumerates the structural side (byte-deterministic,
   axis labels, dedup-keys), enumerates the prose side
   (research-prose nondeterminism), cross-references rf-qa.md, and
   cites the M7-audit claim.

Detector reuse: the test imports `_self_audit_present`,
`_count_category_b_bullets`, `_inflation_positive` from
`tests/audit/test_self_audit_inv_019.py` so the two NFRs share one
source of detector truth (avoids drift).

## 4. Acceptance-criteria mapping (phase-7-tasklist.md L335-339)

| AC | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC1 | Both fixture parts pass per spec | **PASS** | 35/35 pytest assertions PASS (D-0088/evidence.md §3). |
| AC2 | Byte-diff of rf-qa.md PASS/FAIL definitions pre/post M5+M6 is zero | **PASS** | Cross-commit grep across `fd41178`, `db6166e` (post-M5), `87c8254` (post-M6), `HEAD` — content byte-identical (D-0088/evidence.md §4; sub-agent-report.md §2). |
| AC3 | NFR-CONV.2 doc exists with structural-vs-prose boundary enumerated | **PASS** | `docs/reference/nfr-conv-2-prose-determinism.md` §§2.1, 2.2, 3 enumerate the three boundary surfaces; sub-agent confirmed in §5. |
| AC4 | Sub-agent report confirms structural annotations within prose remain byte-equal across 2 runs | **PASS** | Quality-engineer report at `D-0088/sub-agent-report.md` §4 (md5 stable across reads). |

## 5. STRICT-tier compliance

- **Sub-Agent Delegation: Required** — quality-engineer spawned;
  report at `D-0088/sub-agent-report.md`; verdict PASS.
- **Fallback Allowed: No** — no fallback path used; all 35 test
  assertions PASS on first run after fixture asterisk fix.
- **MCP Requirements: Sequential, Serena** — verification chain
  followed the sequential decomposition (anchor → part (a) → part
  (b) → NFR-CONV.2 doc → cross-checks); Serena memory not modified
  (no new project facts that survive beyond the conversation).
- **Critical Path Override: No** — no override needed.

## 6. Rollback plan

If any acceptance criterion regresses post-merge:

1. Re-run `uv run pytest tests/audit/test_nfr_conv_9_zero_trust.py -v`
   to locate the failing class.
2. If `TestPassFailBulletsByteIdentical` fails → the rf-qa.md
   PASS/FAIL bullets drifted. Revert the offending rf-qa.md commit;
   NFR-CONV.9 invariant compromised at the anchor level.
3. If `TestPartA_*` fails → the rf-qa verdict rule changed shape;
   check rf-qa.md:144-145 for a content edit and the severity
   triple `(CRITICAL, IMPORTANT, MINOR)`.
4. If `TestPartB_*` fails → the K-003 audit recipe in
   `test_self_audit_inv_019.py` regressed; restore the detector to
   its T03.14 / D-0037 form.
5. If `TestNfrConv2DocumentationPage` fails → the doc page was
   edited; restore §§2.1, 2.2, 3, 6 to the boundary-enumerating
   shape.

## 7. Cross-references

- **NFR-CONV.9 roadmap row:** `roadmap.md:424` (R-145).
- **NFR-CONV.2 roadmap row:** `roadmap.md:425` (R-146).
- **Invariant anchor (PASS/FAIL bullets):** `src/superclaude/agents/rf-qa.md:144-145` (baseline `:141-142`).
- **Determinism scope split source:** `roadmap.md:28`, `roadmap.md:592`.
- **K-003 audit recipe (reused detectors):** `tests/audit/test_self_audit_inv_019.py` (D-0037).
- **Sibling tests:** `test_inherited_verdict_present.py` (D-0035), `test_nfr_conv_6_self_contained.py` (D-0086).
- **Downstream composite:** TEST-025 invariant preservation composite at T07.09 / D-0090 (will fold this fixture into the 5-invariant union check NFR-CONV.6..10).
- **Sub-agent report:** `.dev/releases/current/task-builder-merge/artifacts/D-0088/sub-agent-report.md`.
- **Evidence file:** `.dev/releases/current/task-builder-merge/artifacts/D-0088/evidence.md`.

**Reviewer sign-off:** NFR-CONV.9 two-part fixture lands; rf-qa.md
PASS/FAIL anchor byte-identical pre/post M5+M6; NFR-CONV.2
prose-determinism documentation page published with the
structural-vs-prose boundary enumerated; quality-engineer
sub-agent verdict PASS.
