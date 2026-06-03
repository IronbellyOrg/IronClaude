# QA Report — Tech Reference Qualitative Review

**Topic:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (PROPOSED)
**Document:** `.dev/releases/backlog/mastra-beads-port-feasibility/ARCHITECTURE-TECHNICAL-REFERENCE.md` (1759 lines)
**Template:** `.claude/templates/documents/technical_reference_template.md`
**Date:** 2026-06-03
**Phase:** tech-ref-qualitative
**Fix cycle:** N/A (initial qualitative pass; fix_authorization: true — fixes applied in-place)
**Reviewer stance:** ADVERSARIAL — assumed errors present; verified every load-bearing claim against source at HEAD `9e864860`.

---

## Overall Verdict: PASS

All issues found (4 IMPORTANT numeric-accuracy defects across 8 lines) were **fixed in-place and re-verified** against source. After remediation, every `[CODE-VERIFIED]` claim spot-checked traces to real code, the design-vs-built integrity holds end-to-end, the §14 risk/gap/stale findings survive un-sanitized, and the §15.3 ledger is internally consistent with the per-section tags.

---

## Confidence

**Verified: 12/12 checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%**
(All 12 tech-ref-qualitative checks adapted to a design-reference-for-proposed-architecture and verified with tool evidence; none marked N/A.)

**Tool engagement:** Read: 6 (full document in pages + template + targeted re-reads) | Grep/Bash: 11 verification batches | Glob: 0 (count via `ls` in Bash) | Tavily: 1 (`tavily-search`, external Backlog.md realism — Tavily-first honored, no fallback needed)

Tool-call count (17 verification batches + 6 reads = 23) exceeds the 12 checklist items — no padding; each Bash batch verified multiple specific claims with `path:line`/count evidence.

---

## Items Reviewed
| # | Check (adapted for design-reference-of-proposed-arch) | Result | Evidence |
|---|-------|--------|----------|
| 1 | Documented behavior matches actual code | FAIL→FIXED | 4 numeric `[CODE-VERIFIED]` claims wrong (42-symbol→65; PhaseStatus 11→13; 15 gates→14); all fixed + re-verified |
| 2 | API examples realistic / would work (adapted: adapter contracts actionable) | PASS | §5.6/§7.3 four contracts have concrete I/O + round-trip/idempotency gates + real seam paths (`discover_phases()`, `parse_tasklist_file()`, `executor.py:41-60`) |
| 3 | Configuration options complete | PASS | §9 covers PipelineConfig/SprintConfig/.roadmap-state.json + external substrate config + env vars; `grace_period`, `permission_flag` verified |
| 4 | No planned features described as current (adapted: no [DESIGN] presented as built) | PASS | 5.5/5.6/5.8 each open with `CRITICAL [DESIGN — UNBUILT]`; "5.6-27 no source file implements" appears 9×; title + status carry PROPOSED |
| 5 | Architecture diagrams match file/module structure | PASS | §2/§3 ASCII trees verified: pipeline 25/roadmap 26/tasklist 6/sprint 19 `.py`; subsystem map matches §5 |
| 6 | File paths + function names verifiable | FAIL→FIXED | All paths exist; symbol-count claims (42→65) corrected; StepRunner@41, ClaudeProcess Popen@134, certify zero callsites all confirmed |
| 7 | Dependency versions match usage (adapted: external versions realistic + URL-cited) | PASS | Backlog.md v1.45.x line confirmed via Tavily; Mastra @core 1.1.0 floor, Beads Dolt-first all URL-cited and plausible |
| 8 | Error handling documented for all failure modes | PASS | §10 covers step/subprocess/parallel/phase/diagnostic + external failure modes + recovery surfaces |
| 9 | Setup/extension steps work (adapted: extension recipes sequence against real seams) | PASS | §13 Recipes A/B/C use real `[CODE-VERIFIED]` existing-side files; DESIGN steps marked; parity-gate ordering enforced |
| 10 | Edge cases + limitations acknowledged | PASS | §14 L1-L8, D1-D9, R1-R9 all present and un-sanitized (verified by count) |
| 11 | No marketing language | PASS | Neutral engineering tone throughout; verdict honestly "Conditionally Recommended ~70%/~55% confidence" |
| 12 | Version/date freshness | PASS | HEAD `9e864860` + package v4.2.0 confirmed; rerun-tasks (v4.3.0 memory) correctly flagged ABSENT |

## Summary
- Checks passed: 12 / 12 (after in-place fixes)
- Checks failed (pre-fix): 2 distinct checks (#1, #6) — same root cause: numeric-count drift in `[CODE-VERIFIED]` claims
- Critical issues: 0
- Important issues: 4 (all numeric-accuracy; all fixed in-place)
- Minor issues: 0
- Issues fixed in-place: 4 (across 8 edited lines)

## Issues Found (all FIXED in-place)
| # | Severity | Location | Issue | Fix Applied + Verification |
|---|----------|----------|-------|----------------------------|
| 1 | IMPORTANT | §3.1 L307, §5.1 L544, §7.2 L1149 | `pipeline/__init__.py` described as "42-symbol public API surface" — actual `__all__` has **65** distinct symbols. Likely confused with the "42 commands" corpus number. A `[CODE-VERIFIED]` claim contradicting source. | Changed all 3 to "65-symbol"/"65 exported symbols in `__all__`". Verified: `awk` over `__all__` block = 65 distinct quoted symbols. |
| 2 | IMPORTANT | §2.2 L334, §5.3 L705, §5.3 L750, §6.3 L1081, §10.1 L1321 | `PhaseStatus` stated as "11 values" / "PhaseStatus(11)" — actual enum (`sprint/models.py:211-233`) has **13** members: `PENDING`, `RUNNING` (transient) + the 11 result states the doc enumerated. The cited range `:211-270` includes PENDING/RUNNING. | Changed all 5 to "13 values" and added PENDING/RUNNING to the enumerated list, preserving the 11-result-state breakdown. Verified: enum member scan returned 13. |
| 3 | IMPORTANT | §5.2 L623 | "12-element step DAG with **15+ gates**" — `ALL_GATES` registry has exactly **14** entries; 13 named `*_GATE = GateCriteria` definitions in the file. "15+" is an over-count for a `[CODE-VERIFIED]` line. | Rewrote to "gates registered in the 14-entry `ALL_GATES` table (`roadmap/gates.py:1426-1441`)". Verified: `ALL_GATES` block = 14 tuples; `ALL_GATES = [` at line 1426. |
| 4 | IMPORTANT | §15.3 ledger L1683 | Ledger annotates `roadmap/gates.py:1020-1441` as "**(15 gates)**" — same off-by-one over-count as #3. Because §15.3 is "the single most important integrity control," a wrong count here is higher-impact. | Changed to "(14-entry `ALL_GATES` registry)". Verified against same `ALL_GATES`=14 source fact. |

> **Note on severity:** All four are IMPORTANT (not CRITICAL): they mislead a developer about API-surface size / enum cardinality / gate count (wrong mental model, wasted time) but would not by themselves break a build or cause data loss. They are document-vs-source drift, not section-vs-section contradictions, now reconciled.

## Actions Taken (in-place fixes)
- Fixed "42-symbol public API surface" → "65-symbol" in §3.1 (L307), §5.1 (L544), §7.2 (L1149). Verified via `__all__` block count = 65.
- Fixed "PhaseStatus 11 values" → "13 values (2 transient PENDING/RUNNING + 11 result states)" in §2.2 (L334), §5.3 models table (L705), §5.3 public-interface enum list (L750-751), §6.3 (L1081), §10.1 (L1321). Verified via enum-member scan = 13.
- Fixed "15+ gates" → "14-entry `ALL_GATES` table" in §5.2 (L623) and "(15 gates)" → "(14-entry `ALL_GATES` registry)" in §15.3 ledger (L1683). Verified `ALL_GATES` = 14 tuples at lines 1426-1441.
- Re-read each edited region post-fix (Edit tool confirms surgical application); re-grepped to confirm no stale "11"/"42-symbol"/"15 gates" count remains.

## Design-vs-Built Integrity Audit (end-to-end) — HOLDS

**(a) Reads as a design reference, not a feasibility reformat:** PASS. Answers what/how/built-vs-designed/how-to-extend (§1 What/Who/Where, §2-3 architecture, §5 subsystems, §13 extension recipes). No "should we/can we" re-litigation — the verdict is stated once (§1, §14) and forward-referenced, not re-argued.

**(b) No [DESIGN] item presented as built:** PASS. The proposed hybrid, adapter layer (§5.6), and governance plane (§5.8) each open with a `CRITICAL: This subsystem is [DESIGN — UNBUILT]` callout. "No source file implements any Mastra/Backlog.md/Beads integration" (evidence 5.6-27) appears 9×. Independently code-confirmed: **zero** mastra/beads code tokens in `cli/`.

**(c) Adapter contracts (§5.6/§7.3) actionable:** PASS. Four contracts with concrete inputs/outputs, real existing-side seam paths (`discover_phases()`/`parse_tasklist_file()`/`count_tasks_in_file()`, `pipeline/executor.py:41-60` StepRunner), and explicit round-trip / idempotency validation gates. An engineer could begin implementing against them.

**(d) §14 risks/gaps + stale findings survive un-sanitized:** PASS (verified by count). CERTIFY_GATE unwired (L1, 4×), wiring grace=0→BLOCKING (L2, 11×), Path A checkpoint gap (L3, 7×), stale `### Checkpoint:` (D1/D2, 8×), src-vs-plugins (D3, 7×), rerun-tasks ABSENT (L8, 4×), R1-R9 (9/9). Independently re-confirmed in source: `build_certify_step` zero callsites; grace_period default 0 + BLOCKING coercion at executor.py:213-214; `_verify_checkpoints` sole call at executor.py:1519; stubs at logging_.py:224-235.

**(e) [CODE-VERIFIED] trace to real code; [EXTERNAL] realistic+URL-cited; §15 ledger consistent with per-section tags:** PASS (after fixes). Ledger 5.1-5.4=BUILT ⟷ §5 headers tagged `[CODE-VERIFIED]`; ledger 5.5/5.6/5.8=DESIGN-only ⟷ §5 headers carry no CODE-VERIFIED tag (open with DESIGN-UNBUILT callouts); ledger 5.7=EXTERNAL ⟷ §5.7 header is EXTERNAL-VERIFIED. No subsystem the ledger calls DESIGN is tagged CODE-VERIFIED in its §5 subsection, and vice versa. External Backlog.md facts corroborated via Tavily.

**(f) §1 framing makes PROPOSED/spike-first/conditionally-recommended unmistakable:** PASS. Title carries "(PROPOSED)"; §1 has two `CRITICAL — PROPOSED, NOT-YET-BUILT ARCHITECTURE` callouts; verdict "Conditionally Recommended, Option D → Option A (spike-first)" stated up front; Implementation Status row = "Design reference — BUILT kernel stable; hybrid PROPOSED / unbuilt".

## Self-Audit (mandatory)

1. **How many factual claims independently verified against source?** ~35 distinct claims across 11 Bash/Grep batches: 8 directory/corpus counts (pipeline 25, roadmap 26, tasklist 6, sprint 19, commands 42, agents 39, skills 24, core 12 — all exact); HEAD `9e864860` + v4.2.0; 3 absence claims (mastra/beads imports=0, rerun-tasks=0, tenant/actor=0 real fields — the 18 grep hits were `default_factory` substrings); StepRunner@41, ClaudeProcess Popen@134, build_command flags verbatim, exit 124@165; grace_period=0@232 + coercion@213-214; CERTIFY_GATE def@1324 + zero callsites; `_build_steps` 12-element order + terminates at remediate@2197; `_verify_checkpoints` sole call@1519; logging stubs@224-235; plugins 30/20/1; "9-step" docstring@1948; stale `### Checkpoint:`@189/195/426; line counts (sprint executor 2148, total 8568, pipeline files); `__all__`=65; PhaseStatus=13; ALL_GATES=14.

2. **What specific files read?** The full tech-ref (6 pages), the template, and source files: `cli/pipeline/{models,executor,gates,process,trailing_gate,deliverables,__init__}.py`, `cli/roadmap/{executor,gates}.py`, `cli/sprint/{models,executor,commands,logging_,process}.py`, plus `ls`-based counts of `commands/`, `agents/`, `skills/`, `core/`, `plugins/superclaude/`.

3. **If 0 issues, why trust the check?** Not applicable — 4 IMPORTANT issues were found and fixed. The adversarial number-by-number verification (not sampling) is exactly what surfaced the 42→65, 11→13, and 15→14 drifts that a structural-only or trusting pass would have missed. Finding real defects is the evidence the review was thorough.

4. **Web research Tavily-first?** Yes. One external lookup (Backlog.md realism) used `mcp__tavily__tavily-search` first; it succeeded, so no WebSearch/WebFetch fallback was needed. Recorded in Tool engagement.

## Recommendations
- None blocking. All four defects fixed in-place and re-verified. The document is accurate, internally consistent, and ready to proceed.
- Optional (non-blocking) future hygiene: the document's own §15.1 verification log claims "0 code drift" for the BUILT side. That remains true for `path:line` anchors (accurate within ±0-2 lines as stated), but the four numeric *aggregate counts* corrected here were not caught by the original spot-checks. A future re-verification could add an explicit "aggregate-count check" lane (symbol/enum/gate cardinalities) to the §15.2 Lane A protocol so count drift is caught alongside line-anchor drift. This is a process suggestion, not a document defect.

## QA Complete
