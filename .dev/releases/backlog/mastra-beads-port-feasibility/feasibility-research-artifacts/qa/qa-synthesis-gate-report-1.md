# QA Report — Synthesis Gate (Partition 1 of N)

**Topic:** Mastra + Backlog.md + Beads port feasibility (Stack D)
**Date:** 2026-06-02
**Phase:** synthesis-gate
**Fix cycle:** N/A
**Assigned files:**
- `synthesis/synth-01-problem-current-state.md` (Report Sections 1-2)
- `synthesis/synth-02-target-gaps.md` (Report Sections 3-4)
- `synthesis/synth-03-external-findings.md` (Report Section 5)

[PARTITION NOTE: Cross-file checks (consistency, cross-references) limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: PASS

All 12 synthesis-gate checks pass (with items 5 and 6 correctly N/A for this partition — see Items Reviewed). No fabrications, no hallucinated file paths, no placeholders, no doc-only architecture leakage. Every sampled claim traced to a research file and/or was independently re-verified against live source code. **Zero fixes were required** — the partition is clean on independent adversarial re-verification.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match Report Structure | PASS | synth-01 = "1. Problem Statement" + "2. Current State Analysis"; synth-02 = "Section 3 — Target State" + "Section 4 — Gap Analysis"; synth-03 = "5.x External Research Findings". Match template at `tech-research/SKILL.md:986-995` (S1 Problem, S2 Current State, S3 Target, S4 Gap, S5 External). |
| 2 | Table column structures correct | PASS | synth-02 Gap Analysis tables use `Gap / Current State / Target State / Severity / Notes` — exact match to `SKILL.md:989`. synth-03 finding tables use `# / Finding / Rating / Relationship / Source` (appropriate for external research). All tables well-formed. |
| 3 | No fabrication (≥5 claims/file traced) | PASS | **synth-01 (8 sampled):** `claude --print --verbose` build_command (process.py:73-95 ✓), PipelineConfig `--dangerously-skip-permissions` (models.py:212-235 ✓), gate tiers EXEMPT/LIGHT/STANDARD/STRICT (gates.py:28-76 ✓), 7 registered CLI commands (main.py:402-426 ✓), sprint prompt `/sc:task` not `/sc:task-unified` (sprint/process.py:170 ✓), diagnostic_chain static f-string Markdown not LLM (diagnostic_chain.py:71-90 ✓), eval per-eval HOME mkdtemp (isolation.py:456 ✓), prd ThreadPool max 10 = NFR-PRD.7 (prd/executor.py:929-939 ✓). **synth-02 (6 sampled):** certify defined-only/not-wired (build_certify_step only at executor.py:1899, never called; traces to research 02 lines 90,146-149 ✓), convergence.py 90-668 within 778-line file ✓, sprint dependency regex parsed (config.py:374-384 ✓), G16 sprint rerun-tasks absent ✓, checkpoint parser dual-form (sprint/checkpoints.py:18-33 ✓). **synth-03 (7 sampled):** all external M/B/BD/G findings trace to web-01/02/03/04 (EE license + AcpAgent → web-01:51-96; Dolt-first + JSONL-export-only + v1.0.5 "do not upgrade" → web-03:54-70; BACK-407 unverified/BACK-408 found + additionalProperties:false + #588 → web-02:33-107). No claim lacked a traceable source. |
| 4 | Evidence citations use actual file paths | PASS | All current-state cells cite `file:lines` with `RNN §` provenance; external cells cite source URLs. No vague "the system handles X" phrasing. Spot-checked paths all resolve. |
| 5 | Options analysis present where applicable | N/A (PASS) | Options Analysis = Report Section 6, owned by a different partition. synth-02 explicitly defers it (line 147: "go/no-go/hybrid scoring, the port matrix... belong to Sections 6-7"). No misplaced/empty option section in this partition. |
| 6 | Implementation specificity where applicable | N/A (PASS) | Implementation Plan = Report Section 8, owned by a different partition. Correctly deferred. No generic implementation steps present in S1-S5 scope. |
| 7 | Cross-section consistency (within partition) | PASS | Verified the highest-risk potential contradiction: synth-03 M1 frames `sprint rerun-tasks ≈ resume-from-step` as an EXTERNAL target analogy, while synth-02 G16 + synth-01 §2.3 flag the verb as ABSENT in current source. Confirmed `sprint/commands.py` has only run/attach/status/logs/kill/verify-checkpoints — verb genuinely absent. The current-vs-target framing is correctly bounded by synth-03's authority reminder (line 204); not a contradiction. |
| 8 | No doc-only claims in Section 2 (Current State) | PASS | synth-01 Section 2 explicitly restricts current-state facts to `[CODE-VERIFIED]` (lines 74-77); `[UNVERIFIED external]` / `[CODE-CONTRADICTED]` quarantined into scope notes and "carried as risks (not facts)" callouts. Grep for doc-only assertion patterns ("according to docs", "the documentation says", "per the README") returned zero hits in synth-01. |
| 9 | Stale docs surfaced in Sections 4/9 | PASS | synth-02 Section 4 surfaces 6 `[CODE-CONTRADICTED]`/stale findings: G10 (legacy checkpoint sibling-section drift), G11 (certify defined-only stale doc), G12 (compressed-sidecar comment contradiction), G15 (plugin-mirror SoT conflict), G16 (`/sc:forensic` + rerun-tasks). Stale items correctly land in Gap Analysis, not buried. |
| 10 | Content-rules compliance (tables over prose, no code repro) | PASS | synth-02/03 are fully table-driven (0 code fences). synth-01 has 3 fenced blocks — all are ASCII architecture/flow diagrams (system topology, roadmap step order, sprint two-path), NOT source-code reproductions. Compliant with Content Rules. |
| 11 | All expected sections have content (no placeholders) | PASS | Grep for TODO/TBD/FIXME/XXX/placeholder/lorem/TKTK across all 3 files = zero hits. Every section is populated; both synth-01 and synth-02 carry "Status: Complete". |
| 12 | No hallucinated file paths | PASS | All cited source paths verified to exist: pipeline/process.py, pipeline/gates.py, pipeline/models.py, roadmap/convergence.py (778 ln), sprint/config.py, sprint/executor.py (2148 ln), eval/isolation.py (747 ln), sprint/logging_.py, sprint/checkpoints.py (408 ln), sprint/diagnostics.py, audit/tool_orchestrator.py, prd/executor.py. (Note: `checkpoints.py` lives under `sprint/`, which the synthesis cites correctly in sprint context — no directory mismatch in the synthesis.) All web research files (web-01..04) and seed-brief.md exist. |

## Summary
- Checks passed: 12 / 12 (items 5, 6 N/A-by-scope, treated as PASS)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Issues Found

None. Independent adversarial re-verification of a representative sample (21 claims across the 3 files, plus full structural/placeholder/path scans) found every claim faithful to its cited research file and/or live source. The synthesis is notably disciplined: current-state facts are quarantined to `[CODE-VERIFIED]`, external claims carry `[UNVERIFIED external]` tags, stale docs are surfaced as gaps rather than normalized away, and the four seed corrections (Beads Dolt-first, Mastra EE-gated RBAC, Backlog.md MVP MCP / BACK-407 unverified, immature Backlog↔Beads integration) all trace to the fresh web research.

## Actions Taken

None — no fixes were necessary. (fix_authorization was true; no edits applied because no defects were found.)

## Adversarial Self-Audit

A 0-issue verdict is treated with suspicion per protocol. Justification that this is genuine, not under-checking:
- The two highest-risk fabrication candidates were probed hardest and both held: (a) the "certify defined-only / not-wired" claim was traced through the actual `_build_steps` body confirming `build_certify_step` is never called despite the `# Step 12 ... constructed dynamically` comment; (b) the `sprint rerun-tasks` current-vs-target framing was cross-checked against live `sprint/commands.py` AND against project memory `reference_sprint_rerun_tasks` (which claims a v4.3.0 verb) — the synthesis correctly takes the conservative "not found in current source" posture.
- Tool-call count (Read+Grep+Bash) exceeds checklist item count, satisfying the engagement minimum.
- Residual risk: claims NOT in the sample (~80% of cells) were not individually traced; given the 100% pass rate on a 21-claim adversarial sample concentrated on the riskiest cells, confidence in the unsampled remainder is high but not absolute.

## Confidence

**Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
- confidence = 12 / (12 - 0) * 100 = 100.0%
- Eligible for PASS: confidence ≥ 95% AND unchecked == 0. Met.

**Tool engagement:** Read: 5 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 8 (each running targeted grep/sed/find against specific cited claims; tavily/web fallback: 0 — no external lookup required, all claims verifiable against local research files + source)

## Recommendations
- Green light to proceed for this partition (S1-S5). The merged synthesis-gate verdict still depends on other partitions covering Sections 6-10 (Options, Recommendation, Implementation Plan, Open Questions, Evidence Trail) — items 5/6 (options/implementation specificity) MUST be enforced there, since they were N/A-by-scope here.
- At assembly time, confirm synth-03 M1's external `rerun-tasks` analogy is not silently promoted into a current-state or implementation assertion (it is correctly external here; preserve that boundary downstream).

## QA Complete

VERDICT: PASS
