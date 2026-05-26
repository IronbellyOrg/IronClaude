# D-0051 — T04.13 Spec: COMP-001-M4 SKILL.md task-qualitative prompt axis directive

**Task:** T04.13 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-083
**Date:** 2026-05-17
**Tier:** STANDARD
**Confidence:** [████████--] 85%

---

## 1. Scope

Add axis-annotation directive at `src/superclaude/skills/task-builder/SKILL.md` inside the Task-Qualitative QA prompt (block A.10.5). Directive instructs the spawned `rf-qa-qualitative` agent to annotate every task-qualitative Items-Reviewed row with one value drawn from the canonical `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` vocabulary.

## 2. Edit-Site Governance Contract

**File:** `src/superclaude/skills/task-builder/SKILL.md`
**Block:** `### A.10.5: Task File Qualitative Validation` → `**QA prompt:**` fenced block → `INSTRUCTIONS:` clause.
**Planned location (roadmap):** ~line 961 in the pre-M3 numbering.
**Actual location (post-M3):** lines 1158–1170 — M3 (FR-CONV.3 Inherited Structural Verdict) and the R-038/R-039 Execution Context header rules inserted ~200 lines above this block, shifting the directive down. The roadmap line `961` predates these landings; the line-number tolerance `[958, 964]` cannot be satisfied literally and is documented as planned-vs-actual drift below (§4).

## 3. Directive Content (post-edit, lines 1158–1170)

```
Apply the 5 Adversarial Axes (PR-07) as a sharpening overlay across all
15 checks: drift, contradictions, omissions, weakened-criteria,
invented-content. Every task-qualitative row's Axis column carries
exactly one value from the canonical vocabulary `{AX-1, AX-2, AX-3,
AX-4, AX-5, none}` — FAIL rows MUST carry the most-specific firing
axis (AX-1..AX-5); PASS rows that surfaced no axis finding carry
`none` (positive statement that all five axes were applied and none
fired, NOT an N/A escape). `N/A`/`n/a`/`—`/blank in the Axis column
is forbidden for task-qualitative phase. The drift axis (AX-1)
requires a BUILD_REQUEST.GOAL verbatim baseline; if no GOAL verbatim
is reachable, emit the literal `drift-axis-inactive` annotation in
the Summary block (not as an Axis-column cell value) and proceed with
the other four axes (AX-2..AX-5).
```

## 4. Planned-vs-Actual Line-Number Drift

| Field | Roadmap (R-083) | Phase-4 tasklist (T04.13) | Actual (post-edit, 2026-05-17) |
|---|---|---|---|
| Reference line | 961 | ~961, tolerance [958, 964] | 1158–1170 |
| Driver of drift | — | — | M3 FR-CONV.3 Inherited Structural Verdict (PR-04) + R-038/R-039 Execution Context header rules inserted upstream |

The phase-task tolerance window `[958, 964]` is a roadmap-time estimate that did not account for the ~200-line M3 insertion that landed before M4. The substantive intent of R-083 — "axis-annotation directive in the Task-Qualitative QA prompt referencing the canonical `{AX-1..AX-5, none}` vocabulary" — is satisfied; the literal line-number tolerance is documented as expected drift in the M3→M4 sequence.

## 5. Mirror Parity

`.claude/skills/task-builder/SKILL.md` synced from `src/` via `make sync-dev`; `make verify-sync` PASS (zero diff between source-of-truth and mirror).

## 6. Rollback Path

Restore the prior directive text (commit immediately preceding this edit) at `src/superclaude/skills/task-builder/SKILL.md` lines 1158–1170 and re-run `make sync-dev` + `make verify-sync`. The edit is contained to a single fenced-block INSTRUCTIONS clause; no surrounding logic or code paths are touched.
