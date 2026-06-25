# Phase 3 (P1) — Consolidated QA Findings (Cycle 1)

**Generated:** 2026-06-19 (Step 3.G8). Six lens reports consolidated, deduplicated.

## Per-lens verdicts

| Lens | Agent | Verdict | Issues |
|------|-------|---------|--------|
| contract-reuse fidelity | rf-qa | PASS | 0 (2 non-blocking INFO) |
| internal-consistency / mirror-sync | rf-qa | PASS | 2 MINOR (hint-text desync) |
| evidence-quality / test-coverage | rf-qa | PASS | 5 MINOR + 1 LOW (test hardening) |
| determinism / no-inference | rf-qa-qualitative | **FAIL** | 3 CRITICAL, 2 IMPORTANT, 1 MINOR |
| surface-placement / no-conflation w/ P5 | rf-qa-qualitative | PASS | 0 |
| domain-accuracy | rf-qa-qualitative | PASS | 0 |

## CONSOLIDATED VERDICT: **FAIL**

(Determinism lens FAILed with 3 CRITICAL no-inference/non-determinism defects; mirror-sync + evidence-quality noted MINOR items.)

## Deduplicated issue list

| ID | Severity | Lens | Location | Issue | Required fix |
|----|----------|------|----------|-------|--------------|
| C3-01 | CRITICAL | determinism | SKILL.md block shape (`References:` line) | Block shape lists `References:` as "roadmap item ID(s) / **GOAL-derived refs**", but §4.1d defines only `R-###` roadmap refs and the Input Contract (`:49`) is "exactly one input: the roadmap text" — there is NO GOAL input to this generator (GOAL is a task-builder/BUILD_REQUEST concept). Internal contradiction + no-inference violation + beyond R-4. | Strike "/ GOAL-derived refs" from the block-shape `References:` line so it is exactly the resolved `R-###` roadmap reference(s) per §4.1d. |
| C3-02 | CRITICAL | determinism | SKILL.md §4.1d + block (`Source areas:`) | No deterministic predicate for what qualifies as a "named source area", nor ordering/de-dup. Classifying roadmap prose as module/subsystem = inference (forbidden). Two generators → different bytes. | Pin a deterministic extraction rule: "list, in roadmap appearance order, only literal noun phrases the roadmap explicitly tags as a module/subsystem/component (e.g. a backticked name or explicit 'module:'/'component:' label); do not classify free prose; de-dup case-insensitively, preserve first-appearance order." |
| C3-03 | CRITICAL | determinism | SKILL.md §4.1d + block (`Key constraints:`) | "**top** 1-3 invariants" presupposes an undefined ranking; the >3-invariants case is unhandled; §4.1d ("carries 1-3") and the shape ("top 1-3") disagree. Non-deterministic; unbacked by R-4. | Replace with: "list the first 1-3 stated invariants in roadmap appearance order; if the item states >3, take the first 3 in appearance order; if 0, omit the field." Reconcile both phrasings to this rule. |
| C3-04 | IMPORTANT | determinism | SKILL.md §4.1d | The three emission forms (full / References-only / Key-constraints-present) are prose-only, not an exhaustive mutually-exclusive branch table. | Add a decision table: (≥1 ref, 0 areas, 0 invariants)→References-only; (≥1 ref, ≥1 area, 0 invariants)→References+Source areas; (≥1 ref, 1-3 invariants)→full; (0 resolvable refs)→omit block. |
| C3-05 | IMPORTANT | determinism | SKILL.md block header ("per-item Context") | The header defers "specific paths belong in per-item Context, never the block header" — but the tasklist generator's task format has NO "per-item Context" sub-block (that is a task-builder concept). Dangling reference / scope-creep risk. | Drop the "belong in per-item Context" clause; replace with "specific paths are never emitted by this generator (roadmap-text-only input)." |
| C3-06 | MINOR | determinism | SKILL.md §4.1d (:218 vs :220 vs :224) | Input set described inconsistently (refs only / refs+source-areas / roadmap text). | State the canonical input set once: "{resolved R-### refs, roadmap-supplied named source areas, roadmap-stated invariants}, all extracted from the roadmap text; nothing else." |
| C3-07 | MINOR | mirror-sync | phase-template.md Source-areas hint | Hint text "listed when present" differs from SKILL.md "listed when the roadmap supplies them". | Make the phase-template hint text byte-identical to SKILL.md (after C3-02/C3-03 land, re-sync both). |
| C3-08 | MINOR | mirror-sync | phase-template.md Key-constraints hint | Hint text "omitted when none" differs from SKILL.md "omitted when the roadmap supplies none". | Make byte-identical to SKILL.md. |
| C3-09 | MINOR | evidence-quality | test (mirror test) | The mirror test omits the no-Ensuring / single-source-of-truth parity asserts that the block-shape test has. | Add `assert "NO `Ensuring:` clause" in text` parity (if present in mirror) — or note the mirror's shorter form. Low priority. |
| C3-10 | MINOR | evidence-quality | test (R-2 lock) | No `assert "## Execution Context" not in index_template_text` to lock R-2 body-not-index placement (the `index_template_text` fixture exists but is unused). | Add `assert "## Execution Context" not in index_template_text` to the P1 test class (uses the existing fixture; locks R-2). |

## Fix scope for Step 3.G9

- SKILL.md determinism fixes C3-01..C3-06 (strike GOAL-derived; pin Source areas + Key constraints extraction;
  add form-selection branch table; drop per-item Context; canonical input set) — all within P1 scope
  (determinism is a core P1/R-4/NFR requirement). NO new surface; block stays in the task body.
- phase-template.md mirror re-sync C3-07/C3-08 (byte-identical hint text after the SKILL.md edits).
- Test hardening C3-09/C3-10 in `tests/tasklist/test_tasklist_cli.py` `TestP1ContextArmedSteps`.
- After fixes: `make sync-dev` + `make verify-sync` + `uv run pytest tests/tasklist/ -v` (stay green).
- IMPORTANT: keep the C3-09/C3-10 test assertions consistent with the actual post-fix SKILL.md prose
  (re-read the edited source before authoring asserts; match arrow/byte-for-byte).
