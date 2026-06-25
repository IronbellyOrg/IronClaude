# Phase 7 (Cross-Cutting) — Consolidated QA Findings (Cycle 1)

**Generated:** 2026-06-19 (Step 7.G8). Six lens reports consolidated (de-collided `qa/qa-p7-*.md` paths).

## Per-lens verdicts

| Lens | Agent | Verdict | Issues |
|------|-------|---------|--------|
| behavior-preserving-edit | rf-qa | PASS | 0 (§49-57 byte-identical to pin; no flag/algorithm/gate change) |
| HALT-discipline / Open-Question integrity | rf-qa | PASS | 1 obs (stale OQ line-numbers, non-blocking) |
| evidence-quality / hygiene-test-coverage | rf-qa | PASS | 2 MINOR (test hardening) |
| actionability / clarity | rf-qa-qualitative | **FAIL** | 2 IMPORTANT, 2 MINOR |
| scope-discipline / no-overreach | rf-qa-qualitative | PASS | 0 |
| domain-accuracy vs research/07/08 + spec | rf-qa-qualitative | PASS | 0 |

## CONSOLIDATED VERDICT: **FAIL**

The §49-57 edit is byte-identical to the authorized research/07 §2b pin (behavior-preserving + domain-accuracy
both PASS). The actionability lens found that the pin PROSE itself has clarity gaps in how it relates to the
existing `--spec`/`--tdd-file`/`--prd-file` flag vocabulary and the 3-tier spec resolution. These are
behavior-preserving clarity fixes (naming flags that already exist, a section-ref correction) — they do NOT
change any flag/algorithm/gate, so the behavior-preserving property is retained.

## Deduplicated issue list

| ID | Severity | Lens | Location | Issue | Required fix |
|----|----------|------|----------|-------|--------------|
| C7-01 | IMPORTANT | actionability I-1 | SKILL.md §49-65 | Flag-vocabulary collision: the contract + `argument-hint` name only `--spec`, but the cited enrichment sites use `--tdd-file`/`--prd-file` (and §4.1a treats `--spec` as a TDD path). The contract never states how the three flag names relate → reads as contradicting AC #4. | Name all three supplementary-input flags in the contract: "(`--spec <spec-path>`, or the explicit `--tdd-file`/`--prd-file` flags, or auto-wired TDD/PRD paths from `.roadmap-state.json`...)". This only NAMES existing flags — no behavior change. |
| C7-02 | IMPORTANT | actionability I-2 | SKILL.md §49-65 | The contract presents spec resolution as 2-state (TDD/PRD present, or roadmap-alone), but the cited Stage-10.5 resolution order is 3-tier ending in "the roadmap itself, always present" — the roadmap-as-final-spec-fallback path is hidden. | Add a brief clause: the roadmap is ALWAYS the final spec-resolution fallback (explicit `--spec` → auto-wired TDD/PRD → the roadmap itself), so a task always has a spec source. |
| C7-03 | MINOR | actionability I-3 | SKILL.md §49-65 (`(§10.5)`) | Dangling ref `(§10.5)` — there is no `§10.5` heading; the section is "Stage 10.5". | Change `(§10.5)` → `(Stage 10.5)`. |
| C7-04 | MINOR | actionability I-4 | SKILL.md §49-65 | Silent on TDD-vs-PRD precedence that §3.x defines, implying false symmetry. | Add a short note that TDD-vs-PRD precedence is per §3.x (or drop the implied symmetry); low priority. |
| C7-05 | MINOR | evidence-quality G-1 | test_sc_task_naming | The positive `"sc:task" in text` is substring-vacuous (the `sc:tasklist` skill name satisfies it even with all real `sc:task` delegations removed). | Assert a real delegate form, e.g. `sc:task --compliance strict`, so the positive half is non-vacuous. |
| C7-06 | MINOR | evidence-quality G-2 | test_no_stale_tokens_in_tasklist_source | A NEW bare `StageError` mention (disclaimer intact) would pass; only operative forms are gated. | Add `assert text.count("StageError") == 1` so a second `StageError` token is caught. |

## Fix scope for Step 7.G9

- SKILL.md §49-65 clarity fixes C7-01..C7-04: name the three supplementary flags; add the roadmap-final-fallback
  clause; `(§10.5)`→`(Stage 10.5)`; (optionally) the TDD-vs-PRD precedence note. All behavior-preserving (no
  flag/algorithm/emitter/gate change — only naming existing flags + ref/clarity). The bullet list stays verbatim;
  the removal path is NOT applied.
- Test hardening C7-05/C7-06 in `tests/tasklist/test_tasklist_cli.py` `TestCrossCuttingHygiene`.
- After fixes: `make sync-dev` + `make verify-sync` + `uv run pytest tests/tasklist/ -v`. Keep all green.
- IMPORTANT: re-read post-fix SKILL.md; keep the existing PASS asserts green; new asserts byte-match source.
