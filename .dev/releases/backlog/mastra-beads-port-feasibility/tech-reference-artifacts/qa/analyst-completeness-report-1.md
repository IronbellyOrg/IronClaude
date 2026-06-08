# Research Completeness Verification (Partition A of 2)

**Topic:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture — Technical Reference (adapted, design-reference)
**Date:** 2026-06-03
**Analyst:** rf-analyst (completeness-verification)
**Stance:** ADVERSARIAL — job is to find problems, not confirm things work
**Depth tier:** Heavyweight
**Code HEAD verified at:** `9e864860` (confirmed via `git rev-parse`)

**Files analyzed (10 assigned, all read in full):**
1. `research/00-evidence-index.md` (387 lines, 243 evidence rows) — the bridge artifact
2. `research/spot-01-pipeline.md` (148 lines, 80 claims)
3. `research/spot-02-roadmap-tasklist.md` (81 lines, 4 targets)
4. `TASK-RESEARCH-20260602-211124/research/01-pipeline-core-contracts.md` (259)
5. `…/02-roadmap-tasklist-pipelines.md` (307)
6. `…/03-sprint-execution-runtime.md` (259)
7. `…/04-cli-portify-prd-cleanup-audit-eval.md` (371)
8. `…/05-skills-agents-harness-reuse.md` (203)
9. `…/web-01-mastra-current-capabilities.md` (110)
10. `…/web-02-backlog-md-current-capabilities.md` (139)

**[PARTITION NOTE: This is Partition A of a 2-instance split. Cross-file checks (contradiction detection, coverage audit against full scope, built-vs-design demarcation completeness) are applied ONLY within this assigned subset. The companion files NOT in this partition — `spot-03-sprint.md`, `spot-04-harness.md`, research files `06-11`, and `web-03`/`web-04` — are out of scope here. Full cross-file analysis requires merging this report with Partition B. Several findings below depend on a file outside this partition (notably spot-03 resolving the `rerun-tasks` contradiction); I verified the underlying code claim directly via grep but flag the spot-check ownership boundary.]**

---

## Verdict: PASS WITH MINOR DEFECTS — 0 critical, 0 important, 4 minor gaps

The evidence base in this partition is exceptionally strong. Every `[CODE-VERIFIED]` claim I independently spot-tested resolves to a real `path:line` valid at HEAD `9e864860`. The built-vs-design demarcation is present and disciplined. The two in-partition spot-checks (pipeline, roadmap/tasklist) report 80/80 and 4/4 CONFIRMED with zero drift, and my independent re-verification of a sample of their anchors plus a sample of evidence-index rows that NO partition spot-check covered (subsystems 5.4/5.6/5.7-current-code) all held. No critical or important gap blocks synthesis. The 4 minor gaps are metadata/traceability hygiene that must still be fixed but do not undermine the evidence.

This partition does NOT independently clear the whole research gate — the `rerun-tasks` contradiction resolution and harness-count spot-check live in spot-03/spot-04 (Partition B). Final research-gate PASS requires the merged verdict.

---

## 1. Coverage Audit (against research-notes.md planned scope, within partition)

The research-notes.md EXISTING_FILES section enumerates the evidence base. For my partition, the relevant question is: does the evidence index map every needed subsystem to a source, and do the assigned source files cover the subsystems they own?

| Scope item (subsystem / notes plan) | Covered by (in partition) | Status |
|---|---|---|
| §5.1 Pipeline-core seam | evidence-index 5.1-01…44 ← research 01; spot-01 (80 claims) | COVERED |
| §5.2 Roadmap/tasklist | evidence-index 5.2-01…28 ← research 02; spot-02 (4 targets) | COVERED |
| §5.3 Sprint runtime | evidence-index 5.3-01…34 ← research 03 | COVERED (source); spot-check is spot-03 → **OUT OF PARTITION** |
| §5.4 Harness corpus | evidence-index 5.4-01…20 ← research 05 | COVERED (source); spot-check is spot-04 → **OUT OF PARTITION** |
| §5.5 Target data model | evidence-index 5.5-01…17 ← research 07 | PARTIAL — source file 07 **OUT OF PARTITION**; index rows present |
| §5.6 Adapter layer | evidence-index 5.6-01…27 ← research 04 | COVERED |
| §5.7 External substrate (Mastra) | evidence-index 5.7-01…10 ← web-01 | COVERED |
| §5.7 External substrate (Backlog.md) | evidence-index 5.7-11…18 ← web-02 | COVERED |
| §5.7 External substrate (Beads) | evidence-index 5.7-19…28 ← web-03 | PARTIAL — web-03 **OUT OF PARTITION** |
| §5.7 cross-cutting (06) | evidence-index 5.7-29…34 ← research 06 | PARTIAL — 06 **OUT OF PARTITION** |
| §5.8 Governance plane | evidence-index 5.8-01…13 ← web-04 | PARTIAL — web-04 **OUT OF PARTITION** |
| Cross-cutting XC-01…26 | evidence-index ← 06/08-11/DECISION/ROADMAP/RISK | PARTIAL — most sources **OUT OF PARTITION** |

**Within-partition finding:** Every subsystem the assigned source files own (5.1, 5.2, 5.4-source, 5.6, 5.7-Mastra, 5.7-Backlog) is covered, and the evidence index maps each to a named source. No scope item that this partition is responsible for is missing from the index. The PARTIAL rows are not gaps — they are sourced from files Partition B holds; the index rows for them exist and are internally consistent, but I cannot verify their source fidelity here. The merge step must confirm Partition B validated 07, 06, 08-11, web-03, web-04.

**No coverage GAP found within partition.**

## 2. Evidence Quality (file:line density)

| Research file | Evidenced claims | Unsupported claims | Quality rating |
|---|---|---|---|
| 00-evidence-index.md | 243/243 rows carry source file + (where applicable) `path:line` + tag | 0 (synthesis-only rows explicitly tagged `(synthesis)`) | Strong |
| spot-01-pipeline.md | 80/80 claims carry research-loc + current-code-loc + status | 0 | Strong |
| spot-02-roadmap-tasklist.md | 4/4 targets carry def + wired + coercion `path:line` | 0 | Strong |
| 01-pipeline-core-contracts.md | dense `path:line` throughout; every claim anchored | 0 | Strong |
| 02-roadmap-tasklist-pipelines.md | dense absolute-path `path:line`; gate-by-gate anchors | 0 | Strong |
| 03-sprint-execution-runtime.md | dense `path:line`; Path A/B divergence anchored | 0 | Strong |
| 04-cli-portify-prd-cleanup-audit-eval.md | dense `path:line` across 5 surfaces | 0 | Strong |
| 05-skills-agents-harness-reuse.md | dense; tables cite `path:line`; counts cited | 0 | Strong |
| web-01-mastra | URL provenance per finding; Tavily/Context7 tagged | 0 (vendor claims flagged as vendor) | Strong (external) |
| web-02-backlog-md | URL provenance per finding incl. raw GitHub source files | 0 | Strong (external) |

**Independent verification (adversarial sample of CODE-VERIFIED rows NOT covered by any partition spot-check):**
- 5.4-13 `hooks.json:1-95` → file is exactly 95 lines; SessionStart/SubagentStart/SubagentStop all present. ✓
- 5.4-16 / notes harness counts "42 commands / 39 agents / 24 skills" → `42 / 39 / 24` exact at HEAD. ✓
- 5.4-14 / XC-07 `core/MCP.md:269-304` → file is exactly 304 lines (XC-07's correction of 305→304 is valid; 269-305 would over-run). ✓
- 5.6-02 `cli_portify/executor.py:105` → `STEP_REGISTRY` defined there. ✓
- 5.6-04 `cli_portify/executor.py:283-372` → `return-contract.yaml` emitted at line 369. ✓
- 5.6-14 `cleanup_audit/executor.py:187-287` → G-001…G-006 all present. ✓
- 5.6-20 `eval/retry.py:92-165` → `class RetryOncePolicy` at 93, `MCP-flaky` tag at 44 (within ±1). ✓
- 5.2-10 / 5.7 sample → `CERTIFY_GATE` at `gates.py:1324`; `grace_period: int = 0` at `models.py:232`; coercion at `executor.py:212-214`. ✓

Zero fabrication detected. Zero unsupported architectural claims. Evidence quality is **Strong** across the partition.

## 3. Documentation Staleness — verification-tag discipline

The driving requirement: every doc-sourced architectural claim must carry `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` (research-file scheme) and, for the tech-ref demarcation, every index row must carry `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]`.

| Stale/contradicted claim (in partition) | Source | Tag present? | Status |
|---|---|---|---|
| `TrailingGateResult` shape spec-deviation (old `(passed,evaluation_ms,gate_name)` vs current) | research 01:113,247; index 5.1-30 | `[STALE DOC][CODE-CONTRADICTED]` / index `(doc-contradicted)` | OK |
| Roadmap "gate on ORIGINAL output" comment vs `.compressed.md` sidecar | research 01:188,248; index 5.1-44 | `[STALE DOC][CODE-CONTRADICTED]` / `(doc-contradicted)` | OK |
| Sprint TUI / deep-dive line-count drift (816/264/1850 → 2148/571) | research 01:249-250 | `[STALE DOC][CODE-CONTRADICTED]` | OK |
| Global "no MCP integration" CLI claim | research 01:251 | `[UNVERIFIED]` | OK (correctly scoped, not over-claimed) |
| `_get_all_step_ids` line drift 2281-2300 → 2283-2302 | research 02:296; index 5.2-27 | `[STALE DOC]` / `(doc-stale)` | OK |
| roadmap.md flag table omits `prd` | research 02:298; index 5.2-28 | `[STALE DOC]` / `(doc-stale)` | OK |
| roadmap skill lists `certify` as wired CLI step (it is not) | research 02:236,297; index 5.2-10 | `[CODE-CONTRADICTED]` / `(defined-only)` | OK |
| cli_portify resume.py legacy step names vs STEP_REGISTRY | research 04:52,346,356; index 5.6-08 | `[CODE-CONTRADICTED]` / `(contradicted)` | OK |
| cleanup_audit docstring claims ThreadPoolExecutor; runs sequentially | research 04:146,349,355; index 5.6-15 | `[CODE-CONTRADICTED]` / `(contradicted)` | OK |
| eval retry-once "future work" comment vs wired policy | research 04:350,358; index 5.6-26 | `[CODE-CONTRADICTED]` / `(doc-stale)` | OK |
| commands/agents README incomplete (5/3 listed vs 42/39 actual) | research 05:197-198; index 5.4-19 | `[STALE DOC]` / `(doc-stale)` | OK |
| SoT conflict `src/` vs `plugins/` | research 05:188,199; index 5.4-18 | `[CODE-CONTRADICTED]` / `(contradicted)` | OK |
| Mastra vendor-maturity / EE-license claims | web-01 §6,§9; index 5.7-06,5.7-09 | `[EXTERNAL-VERIFIED] (vendor/key risk)` | OK |
| Backlog.md MCP "75+ tools" older claim corrected to MVP | web-02 §5; index 5.7-14 | `[EXTERNAL-VERIFIED]` | OK |
| Backlog.md seed-brief BACK-407 unconfirmed (BACK-408 found) | web-02 §9 | `[UNVERIFIED — could not confirm]` | OK |

**Adversarial check for the most dangerous failure mode — a `[CODE-CONTRADICTED]` claim presented as current fact:** none found in partition. Every contradiction is explicitly carried as a contradiction with both the stale version AND the current code reality, and the index routes each to §14 (tech-debt) or §5.x rather than presenting it as architecture. The `certify` defined-only / `wiring grace=0→blocking` / `deviation-classifier UNCLASSIFIED` items are correctly flagged "preserve, do not normalize" per the framing rule.

**No staleness FLAG within partition.** Tag discipline is complete for all doc-sourced and external claims in the assigned files.

## 4. Completeness (per-file status / structure)

| File | Status field | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 00-evidence-index.md | Complete | Y (Summary + tag/row distribution) | N/A (index, not investigation) | Y (4 load-bearing facts) | Complete |
| spot-01-pipeline.md | **In Progress (line 4) / Complete (line 147)** — INCONSISTENT | Y | N/A (delta) | N/A | Complete-body, **defective header** → MINOR-1 |
| spot-02-roadmap-tasklist.md | Complete | Y | N/A (delta) | N/A | Complete |
| 01-pipeline-core-contracts.md | Complete | Y | Y (6 items) | Y (per-section) | Complete |
| 02-roadmap-tasklist-pipelines.md | Complete | Y | Y (6 items) | Y | Complete |
| 03-sprint-execution-runtime.md | Complete | Y | Y (7 items) | Y | Complete |
| 04-cli-portify-prd-cleanup-audit-eval.md | Complete | Y | Y (6 items) | Y | Complete |
| 05-skills-agents-harness-reuse.md | Complete | Y | Y (6 items) | Y | Complete |
| web-01-mastra | Complete | Y | Y (Limitations/Open Questions) | Y | Complete |
| web-02-backlog-md | Complete | Y | Y (implicit in findings) | Y | Complete |

All investigation files have Status: Complete, a Summary, a Gaps/Questions section, and Key Takeaways. The sole completeness defect is the spot-01 header/footer status mismatch (body is unambiguously complete: 80/80 claims verified, summary present). → **MINOR-1**.

## 5. Contradiction Detection (within partition)

I checked for cross-file contradictions among the assigned files, and between the evidence index and its in-partition source files.

**Internal consistency (index vs sources):** Sampled — 5.1 rows match research 01 exactly; 5.2 rows match research 02; 5.6 rows match research 04; 5.7 Mastra/Backlog rows match web-01/web-02. No divergence found between an index row and its cited source within the partition.

**Spot-check vs source-file consistency:** spot-01 confirms research 01's anchors (80/80, ±0-2 line drift, explicitly reconciled). spot-02 confirms research 02's four high-risk targets (4/4). No contradiction between spot-check and the research it audits.

**One cross-partition contradiction surfaces here but is OWNED by Partition B:** Research file 03 (sprint, in my partition as a *source*) and evidence-index XC-09 assert "no `sprint rerun-tasks`." The project memory `reference_sprint_rerun_tasks` claims it shipped v4.3.0. The notes explicitly route resolution to **spot-03 (Agent 2.4), which is NOT in my partition.** I verified the code side directly: `grep -rn "rerun-tasks\|rerun_tasks" src/superclaude/` returns **zero matches at HEAD 9e864860**. So the research/index claim is CORRECT at HEAD and the memory is stale. This is not a contradiction *within the evidence* — it is evidence-vs-stale-memory, correctly resolved in favor of code. **Flagged for merge:** confirm spot-03 reached the same conclusion and that no synthesis agent imports the stale "rerun-tasks exists" memory. → tracked as a cross-partition merge note, not a partition gap.

**No unresolved contradiction within the partition's evidence.**

## 6. Cross-Reference Check (within partition)

The strongest cross-cutting concern in this partition is the `ClaudeProcess` / `StepRunner` seam, which appears in multiple files and must be consistent:
- research 01 (5.1-13, 5.1-24): `StepRunner` protocol + `ClaudeProcess` as the replace point. ✓
- research 02 (5.2-01, 5.2-02): roadmap and tasklist both route through `execute_pipeline` + `ClaudeProcess`. ✓ (consistent with 01)
- research 03 (5.3-13): sprint `ClaudeProcess` subclasses the pipeline `ClaudeProcess`. ✓ (consistent)
- research 04 (5.6 portify/prd/cleanup): all extend the shared `ClaudeProcess`. ✓ (consistent)
- spot-01 §"single runtime seam" explicitly reconciles the cross-reference: the seam is single *within the pipeline package*, and sprint's subclass is a consumer-side instantiation, not a second seam. ✓ Well-handled — the one place a naive reader could see a contradiction ("is there one seam or many?") is pre-empted.

The `.compressed.md` sidecar gate-target rule cross-references correctly between executor (5.1-12) and trailing_gate (5.1-32) and the stale roadmap comment (5.1-44). The `grace_period=0→BLOCKING` rule cross-references between pipeline (5.1-17), roadmap wiring (5.2-12), and sprint wiring-mode mapping (research 01:170). All consistent.

**No broken cross-reference within partition.**

## 7. Built-vs-Design Demarcation Readiness (additional mandated check)

This is the single most important integrity control for an unbuilt-architecture reference. Three sub-checks:

**(a) Every claim destined for the document has a determinable tag.** PASS within partition. All 243 index rows carry exactly one of `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` (with sub-qualifiers like `(doc-contradicted)`, `(absence)`, `(synthesis)`, `(risk)`). I found no untagged row. The tag legend is defined in research-notes.md CRITICAL FRAMING and instantiated per-row.

**(b) Every `[CODE-VERIFIED]` claim has a real `path:line` confirmed valid at HEAD `9e864860`.** PASS within partition, by two independent channels:
- In-partition spot-checks: spot-01 confirms 80/80 pipeline anchors; spot-02 confirms 4/4 roadmap/tasklist high-risk anchors. Both report ±0-2 line drift only, zero NOT-FOUND.
- My independent adversarial sample of CODE-VERIFIED rows that NO partition spot-check touched (5.4-13, 5.4-14, 5.4-16, 5.6-02, 5.6-04, 5.6-14, 5.6-20) — all resolved at HEAD. See §2.
- **Caveat:** 5.3 (sprint) CODE-VERIFIED rows are anchored to research 03 but their dedicated re-verification is spot-03 (Partition B). I did NOT independently re-anchor all 34 sprint rows; I rely on the merge to confirm spot-03 cleared them. The notes' design intends spot-03 to be that channel.

**(c) No claim is untraceable to a source.** PASS within partition. Every row names a source research file; synthesis/inference rows are explicitly labeled `(synthesis)` and traced to the originating research file's synthesis section, not to phantom code. The `[DESIGN — UNBUILT]` rows (5.5-12,13,14; 5.6-27; XC-04,10,11-16) correctly trace to FEASIBILITY-STUDY/DECISION/ROADMAP — though those design-source documents are themselves OUT OF PARTITION, so I verify the *tagging discipline* is correct, not the design-source fidelity (Partition B / source files own that).

**Demarcation readiness verdict for partition: READY.** The discipline is uniform and the dangerous mode (a `[DESIGN]` claim masquerading as built, or a `[CODE-VERIFIED]` claim with a dead anchor) is absent in the assigned files.

## 8. Depth Assessment

**Expected depth:** Heavyweight (8 cross-cutting subsystems, 20+ source files, 3 external tools, governance plane; target 1,200-1,800 line document).

**Actual depth achieved (in-partition evidence):** Exceeds the bar. The evidence base provides data-flow traces (consumer mapping in research 01; Path A/B divergence in 03; QA/fix-loop and fan-out mechanics in 04), integration-point mapping (StepRunner seam, the 4 adapter contracts referenced from 5.5/5.6, the MCP/governance boundary), and pattern analysis (fan-out→consolidate→verify; strangler-fig; artifact-first prompt contracts). The spot-checks add HEAD-validity at symbol/line granularity — stronger than typical Standard-tier file-level understanding.

**Missing depth elements (in-partition):** None that block synthesis. The only depth I could not assess from this partition is sprint runtime spot-validation (spot-03) and harness-count spot-validation (spot-04) — both exist (confirmed via `ls`) but belong to Partition B.

## 9. Compiled Gaps

### Critical Gaps (block synthesis)
None.

### Important Gaps (affect quality)
None within partition.

### Minor Gaps (must still be fixed)

- **MINOR-1 — spot-01 header status inconsistency.** `spot-01-pipeline.md` line 4 reads `**Status:** In Progress` while line 147 reads `**Status: Complete**`. The body is unambiguously complete (80/80 verified). **Remediation:** change line 4 to `**Status:** Complete` for consistency. (Hygiene only; does not affect evidence.)

- **MINOR-2 — sc-task-protocol line-count off-by-one.** Evidence-index 5.4-04 cites `sc-task-protocol/SKILL.md` and research 05 table lists it as 397 lines; actual is 396 at HEAD. Trivial drift, but since the framing demands HEAD-accurate counts, **Remediation:** correct 397→396 if this count is reproduced in the document (or simply do not reproduce raw line counts for instruction files in the tech-ref body).

- **MINOR-3 — partition cross-file dependencies not independently re-verified here.** Subsystems 5.3 (sprint), and the `[DESIGN]`/`[EXTERNAL]` rows sourced from 06/07/08-11/web-03/web-04 are tagged and internally consistent in the index but their source-fidelity validation lives in Partition B. **Remediation (merge step):** confirm Partition B PASSed those source files and their spot-checks (spot-03, spot-04) before declaring an overall research-gate PASS. This is a structural consequence of partitioning, not a defect in the evidence.

- **MINOR-4 — stale-memory guardrail for synthesis.** The `rerun-tasks` finding is correct at HEAD (verified: zero matches in `src/superclaude/`), but the project memory `reference_sprint_rerun_tasks` asserts the opposite. **Remediation:** synthesis agents (esp. §9-11 / §14) must cite XC-09 / spot-03, NOT the memory; add an explicit "do not claim `sprint rerun-tasks` as a current capability" note to the synthesis brief so no agent silently re-imports the stale memory.

## 10. Recommendations

1. **Proceed to synthesis.** This partition's evidence clears the research gate on its own scope: 0 critical / 0 important gaps, demarcation READY, evidence quality Strong, every tested CODE-VERIFIED anchor valid at HEAD `9e864860`.
2. **Fix MINOR-1 and MINOR-2** (trivial header/count edits) before assembly — they would otherwise become visible inaccuracies in a document whose entire premise is HEAD-accurate built-vs-design demarcation.
3. **Gate the overall research PASS on the merge** of this report with Partition B. Specifically require Partition B to have validated: spot-03 (sprint, incl. the `rerun-tasks` resolution and Path-A `_verify_checkpoints()` gap), spot-04 (harness counts 42/39/24 — which I independently confirmed correct), and source files 06/07/08-11/web-03/web-04.
4. **Carry MINOR-4 into the synthesis brief** as a hard guardrail so the stale `rerun-tasks` memory cannot leak into the document.
5. **Preserve, do not normalize** the flagged code-realities (CERTIFY_GATE defined-only, wiring grace=0→blocking, deviation classifier UNCLASSIFIED, Path-A isolation/checkpoint gaps) — the evidence correctly marks these for §14; synthesis must keep them as design-debt, not silently "fix" them in prose.

---

*End of Partition A completeness verification. Merge with Partition B for the full research-gate verdict.*
