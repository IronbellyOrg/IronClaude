# QA Report — Research Gate (Partition B)

**Topic:** Mastra/Beads port feasibility — tech-reference research gate
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A (first pass)
**Partition:** B of [M]

> [PARTITION NOTE: Cross-file checks (contradictions, cross-references, scope coverage) limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

**Reason:** One gap found (Minor severity). Per Heavyweight research-gate rules, any gap of any severity = FAIL. The gap is trivially fixable (one frontmatter line) and the underlying research is otherwise of uniformly strong quality.

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep/Bash: 10 | Glob: 0 | (web research: none required — all external claims verified against the research files' own URL citations, which are present and well-formed)

---

## HEAD context

- HEAD at verification: `9e8648603636d6b9f8fab9e261e583d0de849f34` (matches the HEAD declared in both spot-checks). Package version `4.2.0` (pyproject.toml:7).

---

## Items Reviewed (10-item Research Gate checklist + additional mandated checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all have Status: Complete + Summary | **FAIL** | All 10 files present. 8/10 prior files + spot-04 have `Status: Complete` and a Summary. **spot-03-sprint.md has a Status inconsistency: frontmatter L4 `**Status:** In Progress` vs body L55 `## Status: Complete`** (grep confirmed: only those two Status lines). The canonical frontmatter field says In Progress → this fails the "each has Status: Complete" check. |
| 2 | Evidence density | PASS | spot-03: all 6 delta rows + resolution carry `path:line @ HEAD` citations. spot-04: every count cites `git ls-files`/`find`/`diff -qr`. Files 06/07/08/09/11 are CODE-VERIFIED-dense (06: 31 CV, 08: 37 CV, 09: 33 CV). All cited paths exist (verified existence of executor.py, checkpoints.py, process.py, commands.py, commands/, agents/, skills/, hooks.json, core/, plugins/, retrospective.py). Density: Dense. |
| 3 | Scope coverage | PASS (subset) | Both assigned spot-check domains covered (sprint runtime+checkpoint+rerun; harness corpus+SoT). Prior files 06–11 + web-03/04 each cover their planned domain. [PARTITION NOTE: full EXISTING_FILES coverage audit requires merging Partition A.] |
| 4 | Documentation cross-validation tags | PASS | Every doc-sourced claim in 06/07/08/09/11 carries `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]`. Independently re-verified a sample of CODE-VERIFIED/CODE-CONTRADICTED claims at HEAD (main.py:410/418/422/426 registers cleanup-audit/cli-portify/prd/eval, no root pipeline; PipelineConfig has allow_cosmetic_remediation+cosmetic_remediator at models.py:233-234; build_command delivers prompt via stdin not -p at process.py:76,142). All confirmed. |
| 5 | Contradiction resolution | PASS | Two intra-subset contradictions, both surfaced/resolved (not stale): (a) file 06 "only seed-brief.md under feasibility dir" vs file 08 — file 08 L34/L101 explicitly flags 06's inventory as stale/incomplete and lists corrections → surfaced, remediated. (b) `rerun-tasks` — see additional check below; ABSENT, unambiguous. |
| 6 | Gap severity | **1 gap (Minor)** | The spot-03 Status inconsistency. Will not cause synthesis to hallucinate (content is unambiguously complete), but per gate rules ALL gaps = FAIL. Must be fixed. |
| 7 | Depth appropriateness (Heavyweight/Deep) | PASS | FEASIBILITY-STUDY traces complete data flows end-to-end (Section 2 sprint Path A/B execution flow with file:line; Section 8 phased roadmap with code+URL evidence binding). spot-03 traces the per-task vs freeform branch flow. |
| 8 | Integration point coverage | PASS | Orchestration↔runtime seam (`ClaudeProcess`, shared pipeline), src↔plugins SoT, checkpoint parser↔prompt surfaces, Backlog↔Beads ownership split all documented. |
| 9 | Pattern documentation | PASS | Checkpoint contract dual-shape pattern, Path A/B routing, gate blocking-vs-trailing, stable-ID contract all documented with citations. |
| 10 | Incremental writing compliance | PASS | spot files show delta-row → resolution → summary growth structure (not one-shot perfection); prior files show iterative gap-fill structure. New/untracked files (expected for in-flight research). |
| A1 | Stale/contradiction findings confirmed at HEAD, ready for Section 14 | PASS | Path A `_verify_checkpoints()` gap (executor.py:1301 continue; sole call :1519 in Path B), dual-shape `CHECKPOINT_HEADING_PATTERN` (checkpoints.py:30-33), stale `### Checkpoint:` text (process.py:189/195, commands.py:426) — ALL independently confirmed at HEAD. Ready to surface. |
| A2 | `sprint rerun-tasks` contradiction DEFINITIVELY RESOLVED as ABSENT | PASS | Independently confirmed: tree-wide grep `rerun-tasks\|rerun_tasks\|rerun_task` over src/ → rc=1 (zero matches). Sprint group registers exactly 6 subcommands (run/attach/status/logs/kill/verify-checkpoints at commands.py:71/293/305/317/342/360); no `def rerun`. Package v4.2.0. spot-03 §(c) reaches a binary ABSENT verdict; operator-memory v4.3.0 note reconciled as not-reachable-from-this-commit. Unambiguous. |
| A3 | Every DESIGN claim traces to study/research (not code-backed); every EXTERNAL claim cites URL | PASS | DECISION-SUMMARY (L5 "adds no claims beyond the study"), ROADMAP (L4 source=FEASIBILITY §8), RISK-REGISTER (L4 source=FEASIBILITY §4/6/7/9) all cite the study as source. Code-backed claims (42/39/24 corpus, ClaudeProcess seam, Path-A gap) carry file:line and were independently verified at HEAD. External claims (Beads/Dolt churn #4259/#3870/#3400/#3583, Mastra EE) trace to web-03/web-04 URLs. FEASIBILITY §8.0 "Authority order" explicitly separates codebase-SoT (file:line) from external (URL), keeps `[UNVERIFIED]` as `[UNVERIFIED]`. web-03 has 26 URLs + full Sources list; web-04 has 19 URLs. |

---

## Summary

- Checks passed: 12 / 13 (10 standard + 3 additional mandated)
- Checks failed: 1 (item 1, file inventory — driven by the spot-03 Status inconsistency; item 6 records it as the gap)
- Critical issues: 0
- Important issues: 0
- Minor issues: 1
- Issues fixed in-place: 0 (this gate is report-only; no fix_authorization granted in spawn)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `.dev/tasks/to-do/TASK-TECHREF-20260603-021348/research/spot-03-sprint.md:4` | Frontmatter declares `**Status:** In Progress` while the body terminator (L55) declares `## Status: Complete`. The canonical frontmatter status field is stale. A research file the gate consumes must report `Status: Complete` in its frontmatter. Content is substantively complete (binary verdicts on all 3 claims + full Summary), so this is cosmetic — but any gap of any severity = FAIL at the Heavyweight gate. | Edit `spot-03-sprint.md` line 4 from `**Status:** In Progress` to `**Status:** Complete` to match the body terminator. No content change needed. After fix, re-run a one-line grep to confirm both Status markers read Complete. |

## Cross-check against analyst report

The analyst report `analyst-completeness-report-2.md` exists (created 02:58, after my initial inventory pass) and was read and cross-checked. Independent agreement on all substantive findings:

- Analyst independently flagged the same spot-03 Status inconsistency (its Checklist 4 nit) — I confirmed it independently via grep. Concur: Minor gap = FAIL.
- Analyst's HEAD re-verification of all spot-03/spot-04 claims, the `rerun-tasks` ABSENT resolution, and the file-06-vs-08 surfaced contradiction all match my own independent checks.

**Caveat on the analyst report itself (process observation, not a research-file gap):** the analyst report is truncated/incomplete — it ends at L121 mid-document, never fills its `## Verdict: PENDING (filled at end)` (L14), and its `CHECKLIST 3 — DESIGN deliverable traceability` promises "(Detailed in the DESIGN section below after reading the four deliverables)" (L83) but no such DESIGN section was written. The analyst's DESIGN-traceability conclusion is therefore absent from its own output. This does NOT affect my verdict — I performed the full DESIGN traceability check (A3 above) independently and it PASSES — but the orchestrator should be aware the analyst's A3 coverage is missing and rely on this QA report's A3 row for that dimension. Recommend the orchestrator confirm the analyst either completes its report or that Partition B's DESIGN-traceability is considered covered by this QA report.

## Actions Taken

None. Spawn did not grant `fix_authorization` for this research-gate phase; this report is documentation-only. The single Minor issue requires one one-line Edit by the orchestrator or a gap-fill agent before synthesis proceeds.

## Recommendations

1. **Required before PASS:** Fix issue #1 (spot-03 frontmatter Status line). One-line Edit, no content change.
2. After the fix, this partition is otherwise green: all stale/contradiction findings are confirmed at HEAD and ready to surface in Section 14; the `rerun-tasks` contradiction is definitively ABSENT; DESIGN claims are study-traceable and external claims are URL-cited.
3. Orchestrator: note the analyst report's truncation (missing verdict + missing DESIGN-traceability section). Treat A3 (DESIGN traceability) as covered by THIS report, not the analyst's.
4. [PARTITION NOTE] Merge with Partition A before the final gate decision. Full cross-file contradiction/coverage audit spans both partitions.

## QA Complete
