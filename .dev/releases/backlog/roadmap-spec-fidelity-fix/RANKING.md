# Solution Ranking — Roadmap Spec-Fidelity Convergence Fix

**Source failure**: `.dev/releases/current/task-builder-merge/roadmap/spec-fidelity.md`
**Ranking date**: 2026-05-15
**Method**: 6-way adversarial debate per `sc-adversarial-protocol`. Each Sx solution was independently attacked, refactored, and scored by a `root-cause-analyst` agent; results synthesized in `adversarial/`.

## Ground-Truth Failure Decomposition

10 ACTIVE HIGHs after 3 convergence runs, all with `files_affected=[]`:

| Category | Count | Examples | Status |
|----------|-------|----------|--------|
| Parser noise (URL fragments, brace, line-ref) | 4 | `docs/grouping-algorithm`, `src/x.py:88\`` | Not real defects |
| Legit manifest gaps | 2 | `prd_template.md`, `tdd_template.md` | Real defects in the roadmap |
| NFR soft findings | 4 | `encryption`, `hash`, `<1%`, `<2%` | Overclassified as HIGH |

## Final Ranking

| Rank | Solution | Composite | Standalone conf | Combined conf | Verdict |
|------|----------|-----------|-----------------|---------------|---------|
| 1 | **S2** — Route findings + actionable fix_guidance | **9.2 / 10** | 78 | 88 | **REQUIRED** — load-bearing root-cause fix |
| 2 | **S1** — Sanitize file-path extraction | **7.2 / 10** | 12 | 86 | **REQUIRED** — eliminates 4/10 HIGHs cheaply |
| 3 | **S5** — Context-aware NFR severity | **6.6 / 10** | 70 | 88 | **REQUIRED** — eliminates 4/10 HIGHs via demotion |
| 4 | S6 — MANUAL_TRIAGE halt | 4.6 / 10 | 70 | 88 | Deferred — safety net, not required if top-3 converge |
| 5 | S3 — Tiered diff relaxation | 3.1 / 10 | 72 | 78 | Deferred — wrong failure shape; defensive future feature |
| 6 | S4 — Budget overhaul | 2.8 / 10 | 25 | 70 | Deferred — falsified its own premise; observability only |

### Scoring weights
- Failure-shape match (30%) — does it address the documented failure pattern?
- Root-cause coverage (30%) — how many of the 10 HIGHs does it resolve?
- Implementation risk (20%, inverted) — LOC, blast radius, regression potential
- Combined synergy (20%) — does it amplify the other top fixes?

### Per-axis scoring (out of 10)

| Soln | Failure-shape | Root-cause | Impl risk (inv) | Synergy | Composite |
|------|---------------|-----------|-----------------|---------|-----------|
| S1 | 8 | 4 | 9 | 9 | 7.2 |
| S2 | 10 | 10 | 6 | 10 | 9.2 |
| S3 | 3 | 0 | 6 | 5 | 3.1 |
| S4 | 2 | 0 | 7 | 4 | 2.8 |
| S5 | 8 | 4 | 7 | 8 | 6.6 |
| S6 | 6 | 0 | 7 | 7 | 4.6 |

## Why Top 3 Together Resolve the Failure

After applying S1 + S2 + S5:
- **S1** drops 4 phantom HIGHs at extraction (0 work for downstream).
- **S5** demotes 4 NFR-soft HIGHs to MEDIUM (the spec-fidelity gate is HIGH-only — they no longer block).
- **S2** gives the remaining 2 legitimate HIGHs (`prd_template.md`, `tdd_template.md`) a `files_affected=[roadmap.md]` target *plus* templated `fix_guidance` that tells the agent: *"Add a row referencing `src/superclaude/examples/prd_template.md` to the File Manifest section of the roadmap. Do not modify other rows."*

That guidance produces small additive edits that stay well under the 30% diff threshold. The 3-run convergence loop should reach 0 active HIGHs in Run 1 or Run 2.

## What the Ranking Does NOT Promise

- If the spec is genuinely missing `prd_template.md` / `tdd_template.md` references that the roadmap *should* surface, applying S2 will create roadmap rows for real files — that's correct behavior. But if you decide those template files shouldn't be in the manifest, the spec needs editing, not the roadmap. That's a human decision.
- If a future spec produces a different *kind* of phantom (e.g., S1's URL-precedence heuristic fails on some unusual cell content), S1 will need extending. The current ranking optimizes for *this* failure, not all possible failures.
- S3 and S6 retain defensive value. Re-promote them if the next failure pattern is "agents produce correctly-routed but oversized patches" (→ S3) or "checker bugs continue to generate unfixable findings" (→ S6).

## Backup / Workaround Path

If implementing the top-3 fixes still doesn't unblock the pipeline, see `BACKUP-WORKAROUND.md`. Short version: run with `--allow-regeneration --max-runs 5` to brute-force past the gate and accept a draft tasklist for manual triage, while a proper fix is investigated.

## Artifacts
- Adversarial process: `adversarial/{diff-analysis,debate-transcript,base-selection,refactor-plan,merge-log,merged-solution,invariant-probe}.md`
- Per-solution debate transcripts: `agent-reports/Sx-debate.md`
- Refactored solutions: `solutions/Sx-*.md`
- Implementation tasklist: `TASKLIST.md`
