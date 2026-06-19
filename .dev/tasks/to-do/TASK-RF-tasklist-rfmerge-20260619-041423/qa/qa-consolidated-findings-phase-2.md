# Phase 2 (P4) — Consolidated QA Findings (Cycle 1)

**Generated:** 2026-06-19 (Step 2.G8). Six lens reports consolidated, deduplicated.

## Per-lens verdicts

| Lens | Agent | Verdict | Issues |
|------|-------|---------|--------|
| template-conformance / diff-discipline | rf-qa | PASS | 0 |
| internal-consistency | rf-qa | PASS | 0 |
| evidence-quality / test-coverage | rf-qa | PASS (w/ 4 MINOR coverage gaps) | 4 MINOR |
| actionability | rf-qa-qualitative | **FAIL** | 2 CRITICAL, 3 IMPORTANT, 1 MINOR |
| scope-discipline / no-overreach | rf-qa-qualitative | PASS | 0 |
| domain-accuracy | rf-qa-qualitative | PASS | 0 (2 MINOR notes were upstream research/08 stale anchors, NOT impl defects) |

## CONSOLIDATED VERDICT: **FAIL**

(FAIL if ANY agent reported ANY issue of any severity. The actionability lens FAILed with
2 CRITICAL determinism gaps; the evidence-quality lens noted 4 MINOR test-coverage gaps.)

## Deduplicated issue list

| ID | Severity | Lens(es) | Location | Issue | Required fix |
|----|----------|----------|----------|-------|--------------|
| C2-01 | CRITICAL | actionability | SKILL.md gate-results prose (`<check description>`) | The PASS line `CHECK <n> PASS: <check description>` never pins WHICH string fills `<check description>`. Checks 1-12 are prose sentences (1138-1154); checks 13-20 are terse table rows (1178-1185). A generator must guess full-sentence vs first-clause vs table-cell → different bytes for the same all-pass gate. Breaks determinism (FR-RFMERGE.4 / R-5 byte-reproducibility goal). | Pin the exact source string per check — e.g. "use the verbatim leading clause (text up to the first colon) of each numbered check / the table Check-column cell". |
| C2-02 | CRITICAL | actionability | SKILL.md gate-results prose (`<offending task/file>`) | The FAIL line `CHECK <n> FAIL: <offending task/file>` gives no rule for multi-offender checks (10 duplicate D-####, 15 circular dep chain, 13 task-count): one vs all, ordering, delimiter. | Specify cardinality + delimiter, e.g. "name the first offending identifier in document order; if multiple, comma-separate in ascending T<PP>.<TT> / D-#### order". |
| C2-03 | IMPORTANT | actionability | SKILL.md gate-results prose (`GATE: FAIL (<n> failing)`) | Ambiguous whether the serialized file records the pre-fix failures or the final post-fix all-pass state ("the gate that just ran"). | State explicitly: "serialize the FINAL gate state after all fixes — in practice always `GATE: PASS (20/20)` since no output is written while any check fails (the check-1-20 gate line above)." |
| C2-04 | IMPORTANT | actionability | SKILL.md gate-results prose vs Stage-8 mkdir | Stage-6 now creates `TASKLIST_ROOT/validation/` ("moves its creation earlier") but Stage 8 still says `mkdir -p`; and nothing guarantees gate-results.txt EXISTS before Stage 7 reads it. | Add ordering assertion: "gate-results.txt MUST exist before Stage 7 spawns any agent." Note the Stage-8 `mkdir -p` remains safe/idempotent. |
| C2-05 | IMPORTANT | actionability | SKILL.md Stage-7 payload bullets ("The contents of …") | Unclear whether the orchestrator Reads the file and inlines its text, or passes a path the sub-agent must resolve. Blockquote says "you receive the contents" (implies inlined). | Make explicit: "the orchestrator Reads gate-results.txt and inlines its full text into each spawn payload." |
| C2-06 | MINOR | actionability | SKILL.md gate-results prose (numeric order note) | Ordering deterministic but per-line content not (depends on C2-01). | Auto-resolves once C2-01 is fixed; no standalone change. |
| C2-07 | MINOR | evidence-quality (G1) | test_tasklist_cli.py test | Single `... in text` assert doesn't distinguish the Stage-6 emit from the Stage-7 mentions; AC#6 same-path contract weakly pinned. | Assert the path occurs ≥4× (or in both the Gate-Results subsection AND the Stage-7 payload). |
| C2-08 | MINOR | evidence-quality (G2) | test_tasklist_cli.py test | The `NOT JSON` / plain-text directive (AC#2) is unasserted. | Add `assert "NOT JSON" in text` (or `"plain UTF-8 text" in text`). |
| C2-09 | MINOR | evidence-quality (G3) | test_tasklist_cli.py test | No test guard against re-introducing `Stage 6.5` / `generation-evidence.json`. | Add `assert "generation-evidence" not in text` and `assert "Stage 6.5" not in text`. |
| C2-10 | MINOR | evidence-quality (G4) | test_tasklist_cli.py test | `numeric order 1→20` / one-line-per-check ordering directive unasserted. | Optionally assert `"numeric order 1→20" in text`. |

## Fix scope for Step 2.G9

- SKILL.md prose clarifications C2-01..C2-05 (C2-06 auto-resolves with C2-01) — all bounded
  determinism/wiring clarifications within P4 scope; NO new surface (no Stage 6.5, no JSON, no
  prompts.py edit). Then re-run `make sync-dev` + `make verify-sync`.
- Test hardening C2-07..C2-10 in `tests/tasklist/test_tasklist_cli.py` `TestP4EvidenceAnchoredValidation`.
- After fixes, re-run `uv run pytest tests/tasklist/ -v` to confirm still-green.
