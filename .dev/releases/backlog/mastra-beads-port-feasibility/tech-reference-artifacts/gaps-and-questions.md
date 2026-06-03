# Gaps and Questions — TASK-TECHREF-20260603-021348

**Feature:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (Technical Reference)
**Date:** 2026-06-03
**HEAD:** 9e864860

This file consolidates findings from the Phase 3 (research-completeness) and Phase 5 (synthesis) QA gates. It is the carry-forward gap/guardrail log for synthesis and assembly.

---

## Research Gate (Phase 3) — MERGED VERDICT: PASS (after fix-cycle 1)

Combined per the BOTH-must-PASS rule: Partition A PASS + Partition B FAIL→fixed→PASS.

| Source report | Verdict | Issues |
|---|---|---|
| `qa/analyst-completeness-report-1.md` (Partition A) | PASS | 4 minor (cosmetic) |
| `qa/analyst-completeness-report-2.md` (Partition B) | PASS | 1 minor (cosmetic) |
| `qa/qa-research-gate-report-1.md` (Partition A) | PASS | 0 |
| `qa/qa-research-gate-report-2.md` (Partition B) | FAIL | 1 minor (spot-03 status line) |
| `qa/qa-research-gate-fixcycle-1.md` (re-verify) | **PASS** | 0 — failure set 2→0, no regressions |

### Issues found and resolved (fix-cycle 1)

| ID | Severity | Issue | Resolution |
|---|---|---|---|
| RG-1 | Minor | `spot-03-sprint.md:4` frontmatter "In Progress" vs body "Complete" | FIXED — status line → Complete (executor Edit) |
| RG-2 | Minor | `spot-01-pipeline.md:4` header "In Progress" vs footer "Complete" | FIXED — status line → Complete (executor Edit) |
| RG-3 | Non-issue | `analyst-completeness-report-2.md` appeared truncated to QA-B | RACE ARTIFACT — analyst finished after QA-B's read; final report is 172 lines, Verdict PASS. No action needed. |

### Minor cosmetic items carried forward (do NOT block synthesis; surface in §14 where relevant)

| ID | Item | Action for synthesis |
|---|---|---|
| RG-4 | Evidence-index line-count off-by-ones (e.g. `sc-task-protocol` 397→396) | Cosmetic; prefer spot-check `path:line` over prior research line counts where they differ |
| RG-5 | `_build_steps` docstring says "9-step" + duplicate "Step 8" comments (`roadmap/executor.py:1948,2140,2157`) | Surface in §14 as cosmetic code staleness (labels only; ordering unaffected) |
| RG-6 | Stale legacy `### Checkpoint:` refs in `sprint/process.py:188-195` + `commands.py:426` | Surface in §14 (numbered-checkpoint contract is canonical; pattern accepts both) |

---

## Synthesis Guardrails (carried into Phase 5 — derived from Phase 3 findings)

These are NOT gaps — they are confirmed facts the synthesis agents MUST honor so the document states the verified truth:

1. **`sprint rerun-tasks` is ABSENT at HEAD 9e864860.** The package is v4.2.0 here; the operator memory note `reference_sprint_rerun_tasks` anticipates an unmerged future v4.3.0. The tech reference MUST state ABSENT and name `verify-checkpoints` as the nearest extant recovery surface. Do NOT describe `rerun-tasks` as existing.
2. **`src/superclaude/` is the canonical source-of-truth**, not `plugins/superclaude/` (a divergent 30/20/1/6 mirror). All `[CODE-VERIFIED]` paths cite `src/superclaude/...`.
3. **All four stale/contradiction findings are CONFIRMED at HEAD** and must appear in §14: CERTIFY_GATE unwired (`gates.py:1324-1351`), wiring-verification grace=0 forces blocking (`models.py:232`+`executor.py:213-214`), Path A skips `_verify_checkpoints()` (`sprint/executor.py:1262-1301` vs `:1519`), stale `### Checkpoint:` references.
4. **Built-vs-design tag readiness CONFIRMED:** every claim in the evidence index has a determinable tag; no `[CODE-CONTRADICTED]` claim is presented as current fact; every `[CODE-VERIFIED]` cites a real `path:line` valid at HEAD.

---

## Synthesis Gate (Phase 5) — MERGED VERDICT: PASS (after fix-cycle 1)

| Source report | Verdict | Issues |
|---|---|---|
| `qa/analyst-synthesis-review-1.md` (synth-01..04) | FAIL | 2 important + 2 minor |
| `qa/analyst-synthesis-review-2.md` (synth-05..08) | PASS | 1 medium |
| `qa/qa-synthesis-gate-report-1.md` (synth-01..04) | PASS | 2 minor (fixed in-place) |
| `qa/qa-synthesis-gate-report-2.md` (synth-05..08) | PASS | 1 minor (fixed in-place) |
| `qa/qa-synthesis-gate-fixcycle-1.md` (re-verify) | **PASS** | 0 — 11/11 checks, no regressions |

### Issues found and resolved

| ID | Severity | Issue | Resolution (fix-cycle 1) |
|---|---|---|---|
| SG-1 | Important | synth-04 used un-whitelisted 4th tag `[DESIGN — NOT PROVIDED]` (§5.5/§5.8) — violates the exactly-one-of-3-tags contract | FIXED — normalized all 6 occurrences → `[DESIGN — UNBUILT]`; "NOT PROVIDED by any of Mastra/Backlog/Beads — must be built net-new" meaning preserved in prose (7×); legend confirmed 3 canonical tags |
| SG-2 | Medium | synth-06 §9.3/§10.4 stated a hallucinated Mastra version (`>=1.34.0` floor + "1.16.0 line") unsupported by any source | FIXED — replaced with source-grounded `@mastra/core 1.1.0+` (WorkspaceSandbox added in 1.1.0, `[EXTERNAL-VERIFIED]` web-01 L32); precise-latest marked `[DESIGN — UNVERIFIED]`/pin-at-adoption; all propagation sites reconciled; zero `1.34.0`/`1.16.0` remain |
| SG-3 | Minor | synth-02 + synth-03 stale "In Progress" status headers | FIXED in-place by QA-A (→ Complete) |
| SG-4 | Minor | synth-04 §5.7 folded two `[CODE-VERIFIED]` citations under a combined tag | FIXED — split; seam citations now standalone `[CODE-VERIFIED]` with path:line (`pipeline/process.py:73-147`, `sprint/config.py:379-384`) |
| SG-5 | Minor | synth-05/06/07 bare paths relative to `src/superclaude/cli/` could mis-resolve | FIXED in-place by QA-B (added path-root convention note) |

### Carry-forward for assembly (NOT a gap)

- **`[DESIGN — UNVERIFIED]` sub-variant:** synth-06 §11 (Performance) deliberately uses `[DESIGN — UNVERIFIED]` (distinct from `[DESIGN — UNBUILT]`) for "measurable-in-principle-but-not-yet-measured." Recognized + PASSED by analyst-review-2 and fix-cycle-1. The assembled document's §1 tag legend should ACKNOWLEDGE this §11-only sub-variant so a reader is not confused by an apparent 4th tag.
