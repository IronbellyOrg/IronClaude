# Synthesis Quality Review (Partition 1 of synthesis set)

**Analysis type:** synthesis-review
**Date:** 2026-06-02
**Reviewer:** rf-analyst (adversarial stance)
**Task:** TASK-RESEARCH-20260602-211124 — Mastra + Backlog.md + Beads port feasibility
**Files reviewed:** 3 (assigned subset)

- `synthesis/synth-01-problem-current-state.md` (Report Sections 1-2)
- `synthesis/synth-02-target-gaps.md` (Report Sections 3-4)
- `synthesis/synth-03-external-findings.md` (Report Section 5)

**Report Structure reference applied:** `TASK-RESEARCH-20260602-211124.md` L907-917.
**Checklist applied:** 9-item Synthesis Quality Review Checklist (task file L919-928), plus the partition-specific extras: external claims carry source URLs + uncertainty tags; Beads-Dolt / Mastra-EE / Backlog-MCP corrections preserved.

> **[PARTITION NOTE]** Cross-file checks (checklist #7 — gaps in S4 ↔ later sections) are limited to the assigned subset (S1-S5). S4 gaps that should be addressed in Sections 6-9 (Options/Recommendation/Implementation/Open-Questions) live in synth-04/05/06, which are outside this partition. Full S4↔S6-9 consistency requires merging this report with the partition covering synth-04/05/06.

---

## Per-File Verdicts

| File | Sections | Verdict |
|------|----------|---------|
| synth-01-problem-current-state.md | 1 Problem Statement, 2 Current State | PASS |
| synth-02-target-gaps.md | 3 Target State, 4 Gap Analysis | PASS (fix §4.6 count label) |
| synth-03-external-findings.md | 5 External Research Findings | PASS |

---

## Overall Verdict: PASS (with 1 Low-severity defect to fix)

All nine checklist items pass on substance. Claim-tracing of a representative sample (runtime seam, trailing-gate advisory semantics, R11 guardrails, ownership split, Beads-Dolt / Mastra-EE / Backlog-MCP corrections) confirmed every sampled claim traces to an authorized research input with correct verification tags and no fabrication. The three mandated external corrections are all preserved and correctly attributed.

One genuine internal-consistency defect was found: a severity roll-up **count label** in synth-02 §4.6 says "High (8)" but enumerates 9 items. This is cosmetic (the item list and the 17-gap total are both correct), so it does not block the gate, but it MUST be fixed for the assembled report to be internally consistent.

A second, non-blocking observation (not a defect): the single most load-bearing structural claim in S5 — the `@mastra/acp` `AcpAgent` seam replacement (M3) — rests on the older enrichment seed (`research-deep.md`), not the fresh web-01 research. synth-03 discloses and tags this correctly, so it passes, but it is called out below so the downstream Options/Recommendation synthesis treats the ACP seam as seed-sourced-and-unverified, not fresh-confirmed.

---

## Checklist Results (9 items, applied across all 3 files)

| # | Check | Result | Evidence / Notes |
|---|-------|--------|------------------|
| 1 | Section headers match Report Structure (task file L907-917) | PASS | synth-01 → `## 1. Problem Statement`, `## 2. Current State Analysis`, `## Current-State Summary`. synth-02 → `## Section 3 — Target State`, `## Section 4 — Gap Analysis`. synth-03 → `## 5.x …` covering all five Section-5 sub-areas (Mastra/Backlog/Beads/MCP-governance/Summary). All map 1:1 to the reference's Sections 1, 2, 3, 4, 5. |
| 2 | Table column structures correct | PASS | S4 gap table uses the exact required `Gap / Current State / Target State / Severity / Notes` columns (synth-02 §4.1-4.4). S5 finding tables use `# / Finding / Rating / Relationship / Source` (synth-03), satisfying "findings with URLs, relevance, relationship to codebase." Current-state contract/behavior tables in synth-01 are well-formed. One numeric inconsistency in a roll-up *count label* (not a column-structure problem) — see Issue 1. |
| 3 | No fabrication beyond research files | PASS | Sampled claims all trace: (a) synth-01 ClaudeProcess `claude --print --verbose … --output-format <fmt>`, stdin/`MAX_ARG_STRLEN`, timeout=124 → R01 L75-91; (b) trailing-gate "advisory/warn-only, does not alter StepResult" → R01 L45/L49 (`executor.py:175-187`); (c) R11 guardrails RG-M3/RG-I4/RG-I5/RG-M2 → R11 L15-18, L51-54, L109-158; (d) synth-03 "Steve Yegge's org" (BD1), `@mastra/acp`/`AcpAgent` (M3), "EE bespoke license NOT Elastic/BSL" (M10) → `research-deep.md` L112, L13/L22, L9/L18 — `research-deep.md` is an authorized synth-03 input per task file Step 5.3, so these are sourced, not invented. No fabricated file paths or invented claims found in the sample. |
| 4 | Findings cite actual evidence (paths / URLs) | PASS | Current-state cells cite `file:line` ranges carried from research (e.g. `models.py:212-235`, `process.py:73-95`, `convergence.py:90-668`). External findings cite source URLs (`mastra.ai/docs/...`, `github.com/MrLesk/Backlog.md`, `github.com/gastownhall/beads`, `modelcontextprotocol.io/...`, `scalekit.com`, `finops.org`) plus `[research-deep.md]` / `[tavily]` provenance. Verified URLs against web-01/02/03/04 source tables; representative URLs present in the underlying research. |
| 5 | Options/gaps consistency where applicable | PASS (N/A for Options) | Options Analysis (Section 6) is out of this partition's scope. The applicable analog — gap inventory consistency — holds: §4.5 Required-Coverage Cross-Check maps every task-brief minimum gap to a G-row, and §4.6 buckets all 17 gaps by severity. The two distinct candidate directions ("port" vs the live "do not port / keep Python harness") are both preserved as live (synth-01 §1.1, synth-03 §5.5 net posture), satisfying the seed-brief requirement that "do not port" remain a live outcome. |
| 6 | Actionable specificity | PASS | Gap "Notes" cells carry actionable, source-anchored direction (e.g. G10 "emit numbered checkpoint task entries with `Checkpoint Report Path:`, not sibling sections"; G9 "drive `bd … --json`, never read `.beads/issues.jsonl`"; G7 "Mastra EE OR a separate auth layer + new governance/control-plane"). No generic "build a service" filler. Full Implementation Plan specificity (Section 8) is out of partition scope. |
| 7 | Cross-references consistent | PASS (within partition) | Severity buckets in §4.6 match each row's own Severity column (spot-checked G3/G4/G6/G7=Critical, G12/G15/G16=Medium, G17=Low — all consistent). §4.5 coverage map references resolve to real G-rows. S5 seed-correction callouts (Beads-Dolt, Mastra-EE, BACK-407, Backlog↔Beads, MCP-not-governance) are consistent with the corresponding S4 rows (G9, G7, G14, G8). **One count-label inconsistency** (Issue 1). S4↔S6-9 cross-refs deferred per Partition Note. |
| 8 | No doc-only claims in Current State (S2) | PASS | synth-01 §2 opens with an explicit guardrail (L74-77): only `[CODE-VERIFIED]` findings appear as current-state facts. Every §2 doc-sourced or contradicted item is quarantined into a "Current-state caveats carried as risks (not facts)" block (§2.2, §2.3, §2.4, §2.5) rather than stated as architecture — e.g. `CERTIFY_GATE` defined-not-wired, the documented "4-layer isolation" not active, `cli_portify` legacy step-name drift `[CODE-CONTRADICTED]`, `/sc:forensic` no matching command. No untagged doc-only claim found in the current-state body. |
| 9 | Stale-doc / CODE-CONTRADICTED surfaced (not omitted) | PASS | All known `[CODE-CONTRADICTED]` / stale items surface: in synth-01 as risk caveats (certify-not-wired, isolation-not-active, cli_portify/cleanup_audit drift, `/sc:forensic`, plugin-mirror SoT conflict RG-I4); in synth-02 S4 as gaps (G10 checkpoint contract, G11 certify defined-only, G12 wiring trailing-vs-blocking + compressed-sidecar comment contradiction, G15 SoT mirror drift, G16 `/sc:forensic` + `rerun-tasks` exclusion); in synth-03 as four explicit Seed-Correction callouts + a fifth structural correction. The `reference_sprint_rerun_tasks` project-memory tension (memory claims a v4.3.0 verb; this research did not find it) is correctly handled in G16 as unverified-pending-broader-search, matching R11 L113/L141. |

---

## Partition-Specific External-Claims Checks

| Check | Result | Evidence / Notes |
|-------|--------|------------------|
| External claims carry source URLs | PASS | Every S5 finding row has a Source column with a URL or `[research-deep.md]` provenance; §3 target-stack cells and §4 target-state cells cite `web-0N §url`. |
| External claims carry uncertainty tags | PASS | synth-03 §5.1.3 carries an explicit "UNVERIFIED / needs hands-on validation" block (workflow replay/idempotency, `@mastra/acp` Apache-vs-ee, `max_turns`/permission parity, Cursor/Gemini/Copilot via AcpAgent, hook parity). M13/M14 rated MEDIUM with version-UNVERIFIED notes. synth-02 carries `[UNVERIFIED external]` on all Stack-D capability/ownership assumptions (§3.4, CON-1..CON-7). No external claim is stated as code-fact. |
| **Beads = Dolt-first correction preserved** | PASS | synth-03 §5.3.2 dedicated Seed-Correction box: "Beads uses Dolt ONLY … classic SQLite+JSONL removed … `.beads/issues.jsonl` export/interop ONLY … drive `bd … --json`, never read JSONL." Traces to web-03 §7 (L54-59) + research-deep.md L115. Mirrored in synth-02 G9 ("Corrects the seed brief") and the §5.5 corrections table. CONTRADICTED status correctly relationship-tagged. |
| **Mastra EE licensing correction preserved** | PASS | synth-03 M10/M11/M12 + §5.1.2 Seed-Correction box: production RBAC/SSO/FGA is EE-gated (bespoke commercial license, NOT Elastic/BSL); Apache path = SimpleAuth + DIY tenant scoping. Traces to web-01 §6 (L51-56) for the EE-gating and research-deep.md L9/L18 for the "NOT Elastic/BSL" specificity. Mirrored in synth-02 CON-2, G7, and §5.5 corrections table. |
| **Backlog.md MCP / BACK-407 correction preserved** | PASS | synth-03 §5.2.3 dedicated BACK-407 box: BACK-407 status UNVERIFIED (BACK-408 found instead); MCP is an MVP stdio surface; `additionalProperties:false` rejects arbitrary metadata; decisions CLI-only in MVP; probe live before relying. Traces to web-02 (B6/B7/B8/B12). Mirrored in synth-02 CON-3, CON-4, G14, and §5.5 corrections table. Fresh research correctly governs over the seed per stated authority rule 2. |
| Authority rule (codebase governs external) honored | PASS | synth-03 §5.0 ground rules + §5.5 authority reminder both state external research does not override verified code; discrepancies noted explicitly. synth-02 citation conventions keep current-state cells on code research and target cells on web URLs. |

---

## Issues Requiring Fixes

| # | File | Check | Severity | Issue | Required Fix |
|---|------|-------|----------|-------|--------------|
| 1 | synth-02-target-gaps.md §4.6 (L137) | #7 / #2 | **Low** | Severity roll-up label reads **"High (8):"** but enumerates **9** items (G1, G2, G5, G8, G9, G10, G11, G13, G14). The item list and the 17-gap total (4 Critical + 9 High + 3 Medium + 1 Low = 17 = G1-G17) are both correct; only the parenthetical count is wrong. | Change `**High (8):**` to `**High (9):**` on L137. No other edit needed — the enumerated list is complete and correct. |

---

## Non-Blocking Observations (not gate failures)

| # | File | Observation | Why it matters downstream |
|---|------|-------------|---------------------------|
| A | synth-03 M3 (ACP seam) | The decisive "structural replacement for `ClaudeProcess`" (`@mastra/acp` `AcpAgent`) is sourced from the older enrichment seed `research-deep.md`, NOT from the fresh web-01 research, which covers `WorkspaceSandbox` but not ACP. synth-03 rates M3 "HIGH/Extends" and discloses the seed provenance + UNVERIFIED sub-items (license, `max_turns`/permission parity), so it PASSES. | The Options/Recommendation synthesis (Section 6-7) should treat the ACP seam as seed-asserted-and-unproven, not fresh-confirmed, and should keep the "verify `max_turns`/permission/model parity" spike as a go/no-go gate. Do not upgrade M3 to "fresh-verified" during assembly. |
| B | synth-03 reading guide (rule 2) | The guide states fresh web research supersedes the seed where they differ. For M3/M10 the seed is the *sole* source (fresh research is silent, not contradictory), so "supersedes" does not down-weight them — correct handling, but worth noting the seed remains load-bearing for the seam claim and the EE "NOT Elastic/BSL" specificity. | Assembly should not silently drop seed-only claims on the assumption that "fresh supersedes." Where fresh research is silent, the seed claim stands but retains its original `[research-deep.md]` provenance and uncertainty. |
| C | Cross-partition (deferred) | synth-02 S4 gaps are inputs to Sections 6-9, which live in synth-04/05/06 (other partition). This review cannot confirm that every Critical/High gap (esp. G3/G4/G6/G7) is actually addressed in the Options/Recommendation/Implementation/Open-Questions sections. | The merge step / the partition reviewing synth-04/05/06 MUST verify S4↔S6-9 closure: every Critical gap should map to an option trade-off, a recommendation rationale, an implementation step, or an open question. |

---

## Summary

- Files reviewed: 3 (synth-01, synth-02, synth-03)
- Files passed: 3
- Files failed: 0
- Blocking issues: 0
- Non-blocking issues to fix before assembly: 1 (Low — synth-02 §4.6 count label "8"→"9")
- Non-blocking observations: 3 (A: ACP seam is seed-sourced; B: seed-only claims must survive "fresh supersedes"; C: S4↔S6-9 closure deferred to other partition)
- External corrections preserved: 3/3 (Beads-Dolt, Mastra-EE, Backlog-MCP/BACK-407) + the fifth MCP-not-governance structural correction
- Fabrication: none detected in the traced sample
- Doc-only-in-current-state violations: none
- Stale-doc / CODE-CONTRADICTED omissions: none

**Gate result: PASS.** The one Low-severity count-label defect should be corrected by the synthesis owner before final report assembly, but it does not block the synthesis quality gate.

---

**Status:** Complete
