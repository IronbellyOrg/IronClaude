# QA Report — Task Integrity Check

**Topic:** Remediate validated PR #112 + #111 review findings R1-R5
**Date:** 2026-06-02
**Phase:** task-integrity
**Fix cycle:** N/A
**Task file:** TASK-RF-20260602-060714.md
**Template:** 02
**Fix authorization:** true

---

## Overall Verdict: PASS

The task file is structurally well-formed against template 02, evidence-based against real
source (every anchor re-verified by symbol/grep), correctly encodes all CRITICAL CORRECTNESS
constraints, and gates the R5 implementation subtree on an in-task decision artifact with a clean
DAG. No issues required in-place fixes.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | `id`, `title`, `status`, `created_date`/`updated_date`, `type`, `template_schema_doc`, `task_type`, `related_docs`, `tags` all present + non-empty (L2-52). `related_docs` lists design + 4 research + 2 QA gate reports with descriptions. |
| 2 | Mandatory sections present; NO items before Phase 1 (D3) | PASS | Pre-Phase-1 headers (Overview, Key Objectives, Prereqs, Execution Context, Detailed Task Instructions) contain NO `- [ ]`. First checkbox is L139 inside Phase 1. Key Objectives use numbered `1.`-`7.`, not checkboxes. |
| 3 | Items self-contained (context+action+output+verify+gate, B2) | PASS | Every `- [ ]` is a single paragraph carrying a Read/anchor step, an edit/run action, an output path, a "ensuring …" verification clause, and a completion gate ("mark this item complete"). Sampled 1.4, 4.1, 4.9, 5.3, 5.5, 5.8, 6.3. |
| 4 | Granularity — R5 md_ids blast radius each granular | PASS | R5 split into 15 items (4.1-4.15): contracts MD body (4.1), spec_parser dedup (4.2), structural_checkers canonicalizer (4.3), allowlist (4.4), then md_ids landed per-site: SpecIdRegistry field (4.5), union_of_known (4.6), to_dict (4.7), build_id_registry (4.8), gates sidecar read (4.9), schema-tests (4.10), conftest (4.11), oracle tests (4.12), fixture (4.13), test-run (4.14), arch_lint (4.15). One file-site per item. |
| 5 | Evidence-based; verified paths re-anchored by symbol | PASS | Items RE-ANCHOR by symbol (`class SpecIdRegistry`, `def union_of_known`, `def to_dict`, `def build_id_registry`, `_roadmap_ids_within_spec`, `def execute_roadmap`, `if config.dry_run:`, Rule-2 membership check) explicitly because line drift was noted. All anchors verified present in real source (see Correctness section). |
| 6 | No items on contradicted/unverified findings | PASS | Every cited fact reconciles with live source: gates.py fail-shut, contracts FR/NFR/SC/G/D-only, absent `non_ref` in structural_checkers, absent `_MD_TRAILING_D_RE` in spec_parser, 8-key sidecar schema, commit `861047c2` + 3 oracle test names all confirmed. |
| 7 | Open Questions documented | PASS | OQ block (L426-432): R5 path a-vs-b decided IN-TASK by Phase 2 reproduction; R5 path-b allowlist scope answered by `r5-scope-determination.md`; R3 optional/droppable. R1.3 signature-widening recorded as deferred follow-up (L438). |
| 8 | Phase deps logical; R5 impl gated on decision artifact; no circular | PASS | Phase 4 (every item) reads `r5-remediation-decision.md` first and skips on `decision: CLOSE`. Decision artifact written in Phase 3 (Step 3.1) from Phase 2 reproduction evidence. Phase 6 reads the Phase 1 baseline. No back-edges. |
| 9 | Reasonable item count for scope | PASS | 46 items across 6 phases + phase-gate + post-completion for a 5-finding remediation whose R5 path-b is a cross-cutting SoT migration. Proportionate. |
| TB-Add-1 | No TBD/TODO/FIXME; no title-only items | PASS | 0 `TBD`/`FIXME`. The only `TODO` occurrences are inside quoted strings citing the literal stale clause "the TODO comment below" (the R1 *target text*), not placeholder tokens. No title-only items. |
| TB-Add-2 | Item-count bounds (single-track ≥3/≤50) | PASS (ADVISORY) | 46 items, within bound. Advisory per uncalibrated-bounds rule. |
| TB-Add-3 | Blocked items reference blocking OQ/decision-artifact | PASS | Every Phase 4 item names `r5-remediation-decision.md` and its `decision:`/scope gate in its Context. R3 items (5.10-5.12) self-reference the optional/droppable status. |
| TB-Add-4 | Item-to-item deps form a DAG | PASS | Linear intra-phase ordering; cross-item references point only backward (Phase 4 → Phase 3 artifact; Phase 6 → Phase 1 baseline; 4.6-4.9 depend on 4.5 dataclass field). No cycle. |
| TB-Add-5 | XL/multi-file items split or justified | PASS | The largest natural blast radius (R5 md_ids) is split one-site-per-item (4.5-4.11). R2 split into reset (5.3), guard (5.4), test (5.5), run (5.6). |
| TB-Add-6 | Uniform Verify form / acceptance form | PASS | Every item uses the "ensuring …" verification clause + "Once done, mark this item as complete." gate consistently. |
| TB-Add-7 | Exec Context "Source areas" reappear in items; block has no file:line | PASS | Block (L121-128) has 0 `src/`/`:NN` refs (grep -c = 0). Each named source area (gates, executor, id_registry, spec_parser/structural_checkers, contracts, arch_lint, cleanup-audit script) reappears in ≥1 item Context. |
| TB-Add-8 | Per-item Context with code surface carries file:line OR evidence-absence | PASS | Items cite file + symbol anchors and research-doc section refs (which carry the file:line). New-file-creation items (4.13 fixture, discovery outputs) reference format conventions, not source lines — consistent with evidence-absence intent. |

## Summary

- Checks passed: 18 / 18 (9 numbered + 8 TB-Add + correctness sweep)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

---

## CRITICAL CORRECTNESS CHECKS (verified against real source)

| Constraint | Result | Evidence |
|---|--------|----------|
| R2 reset is resume-aware (does NOT break `--resume`/`_apply_resume`) | PASS | Step 5.3 explicitly forbids a blind `set_id_registry_sidecar_path(None)` because `_apply_resume` may skip extract, and mandates reset-only-when-extract-runs OR re-derive-from-existing-sidecar. Verified in source: `execute_roadmap` (L3399) runs dry-run guard (L3492) → `if resume: _apply_resume(...)` → `# Execute pipeline` (L3538). Resume genuinely runs between the proposed insertion point and `execute_pipeline`. |
| R2 does NOT change `Callable[[str], bool\|str]` signature | PASS | Steps 4.9, 5.3, 5.4 all state the signature is unchanged (R1.3 territory). Source: signature documented gates.py L1033; `def _roadmap_ids_within_spec(content: str) -> bool \| str:` L1052 (content-only). |
| R2 preserves fail-shut at gates.py:1069-1074 | PASS | Steps 4.9 + 5.3 cite "preserve fail-shut EXACTLY (around L1069-1074)". Source: `if _id_registry_sidecar_path is None: return ("Contract #9 … not registered")` + OSError/JSONDecode/TypeError branches all return failure strings (verified L1069-1100). |
| R2 regression = two sequential calls in ONE test body (autouse fixture hazard) | PASS | Step 5.5 explicitly: "the regression MUST exercise TWO sequential runs in ONE test body where the reset does NOT fire between them" and cites autouse `_isolate_gates_state`. Source: `@pytest.fixture(autouse=True) def _isolate_gates_state()` at L57-58 of test_spec_roadmap_id_containment.py — confirmed it would mask a two-function test. |
| R4 runs make sync-dev + verify-sync, stages ONLY src/ | PASS | Step 5.8 runs both and reinforces the ABSOLUTE RULE: never `git add`/`-f` any `.claude/{skills,...}` path; only `src/` side staged. Step 5.7 edits the `src/superclaude/skills/...` script. |
| R5 path-b MD body sourced from contracts.ID_PATTERNS SoT (never inlined) | PASS | Step 4.1 adds anchor-free `r"M\d+-D-?\d+"` to `ID_PATTERNS`, ordered BEFORE `D`; Steps 4.2/4.3 explicitly say MD is auto-derived via the dict-comprehension (not re-inlined); 4.15 runs arch_lint to prove no consumer inlined it. Source: contracts FR/NFR/SC/G/D-only confirmed; anchor-free convention confirmed (contracts L58-62). |
| R5 md_ids lands in lockstep across all registry/sidecar/schema sites | PASS | 4.5 field → 4.6 union_of_known → 4.7 to_dict (write) → 4.8 build_id_registry → 4.9 gates read → 4.10 schema tests → 4.11 conftest. Source: all 7 sites confirmed (id_registry dataclass, union, to_dict; gates reconstruction L1089-1099; schema test 8-key set L207-217; round-trip L248-257; conftest fixture L53). |
| Final phase has lint-architecture + verify-sync + targeted pytest + parent-baseline delta | PASS | Phase 6: 6.1 `make lint-architecture` (exit 0), 6.2 `make verify-sync`, 6.3 full `uv run pytest` + `final-baseline-delta.md` vs Phase-1 baseline. Plus per-surface pytest in 4.14/5.6/5.2 and post-completion regression run. |

### Source anchors re-verified (S1/S3 freshness compliance)

- `id_registry.py` stale clause "R0.3 will hoist the patterns … the TODO comment below tracks that migration" — present verbatim (L22-24 region); contradicted by `from superclaude.contracts import ID_PATTERNS as _ID_PATTERNS` present below. R1 target real.
- `contracts/__init__.py` `ID_PATTERNS: Final[dict[str,str]]` = FR/NFR/SC/G/D only, no MD; anchor-free convention documented. R5 premise real.
- `structural_checkers.py`: `check_signatures` L402, `_canonicalize_requirement_id` L295, **0** `non_ref` matches → allowlist genuinely absent (R5 path-b allowlist port justified).
- `spec_parser.py`: `_REQUIREMENT_PATTERNS` L329, `extract_requirement_ids` L335, no `_MD_TRAILING_D_RE` → must be added (4.2 justified).
- Commit `861047c2` exists; `test_phantom_id_honors_explicit_non_references_for_milestone_d_ids`, `test_phantom_id_backward_compatible_without_explicit_non_references`, `test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d`, and `_write_md_fixture_with_allowlist` all present there (4.12 port targets real). Current `test_structural_checkers.py` has `_write_id_fixture` (L316) in `class TestSignaturesChecker` (L255) — reuse claim for tests 2/3 valid.
- Sidecar schema: `test_registry_sidecar_schema_stable` 8-key `expected_keys` (L207-217) and `test_sidecar_schema_round_trip` 8-key reconstruction (L248-257) confirmed — both must gain `md_ids` → 9 keys (4.10 correct; note round-trip uses direct subscript so adding `md_ids` to to_dict requires the matching reconstruction update, which 4.10 mandates).

## Observations (non-blocking, no fix required)

1. **Step 4.10 round-trip subtlety (informational).** `test_sidecar_schema_round_trip` reconstructs with direct `payload["fr_ids"]` subscripts (not `.get`). Once `to_dict()` emits `md_ids` (4.7), the stable-schema test fails first on the key-set assertion; 4.10 correctly updates BOTH tests. The item already covers this — noted only to confirm the executor will not be surprised.
2. **Step 5.4 path-identity guard is correctly marked secondary/droppable** with an explicit "do not force it into R1.3 envelope territory" escape, matching the design doc's defense-in-depth-but-(1)-at-minimum framing.
3. **Phase-gate fix-cycle cap is 2** (Step PG.3, "MAXIMUM of 2 fix cycles … per I16") with the regression→monotonicity→hard-cap HALT precedence encoded verbatim — consistent with the task-integrity convention.

## Actions Taken

None. No issues found that required in-place fixes. (Adversarial sweep: every CRITICAL constraint and every cited anchor was independently re-verified against live source via grep/sed; the task file did not over-claim or fabricate any path, line, symbol, or commit.)

## Confidence Gate

- **Confidence:** Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 8 | Glob: 0 | Bash: 8 (each call mapped to a specific check/anchor)
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations

- Proceed to execution (`/task <path>`). The R5 decision MUST be made from the Phase 2 reproduction evidence at runtime — it is correctly NOT pre-decided in the task file.
- During execution, the only residual judgement call is Step 5.4 (path-identity guard): accept the item's built-in "skip cleanly rather than force R1.3 signature widening" branch if it cannot be done additively.

## QA Complete

VERDICT: PASS
