# QA Report — Synthesis Gate

**Topic:** Mastra + Backlog.md + Beads Hybrid Orchestration Architecture — Technical Reference
**Date:** 2026-06-03
**Phase:** synthesis-gate
**Fix cycle:** N/A (cycle 1)
**Fix authorization:** true (issues fixed in-place)
**Assigned files:** synth-01-overview-architecture.md, synth-02-directory-dataflow.md, synth-03-subsystems-existing.md, synth-04-subsystems-target.md
**Code baseline:** HEAD `9e864860` (confirmed via `git rev-parse --short HEAD`)

---

## Overall Verdict: PASS

2 issues found, both MINOR, both fixed in-place. No fabrication, no doc-only architecture claims, no hallucinated BUILT paths, no `[DESIGN]`-as-built. Built-vs-design demarcation is rigorous and the PROPOSED framing + tag legend is present in §1.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match template | PASS | Template §1 Overview / §2 Architecture / §3 Directory Structure / §4 Data Flow / §5 Subsystem Reference (template L149-328). synth-01 uses "## 1. Overview", "## 2. Architecture" + 2.1/2.2/2.3 matching template L165-191. synth-02 uses "## 3. Directory Structure" (3.1/3.2/3.3) + "## 4. Data Flow" (4.1/4.2/4.3) matching template L203-261. synth-03/04 use "### 5.N [Subsystem]" with Purpose/Key Files/How It Works/Dependencies/Consumers/Conventions per template L279-317 / L676-685. |
| 2 | Table column structures correct | PASS | Subsystem Map (synth-01 §2.2) + Key Design Decisions (§2.3) follow template L177-190. Data Sources / Data Transformations (synth-02 §4.2/4.3) match template L250-261. Dependencies/Consumers tables match template L303-311. A Tag column is added to every table — additive, structure preserved. |
| 3 | No fabrication (every fact traces to research) | PASS | Sampled ~25 claims across all 4 files; each cites an evidence-index row (5.x-NN / XC-NN) or spot-check (spot-01..04). Independently re-verified a sample against HEAD: Popen@process.py:134, StepRunner@executor.py:41-60, gate tiers@gates.py:20+, `_verify_checkpoints` single call@executor.py:1519, CERTIFY build_certify_step/check_certify_resume def-only (no callsites), grace_period=0@models.py:232, harness counts 42/39/24, decompose_deliverables@deliverables.py:146, DECISION-SUMMARY verdict. No untraceable claim found. |
| 4 | Evidence cites actual file paths (not vague) | PASS | All BUILT claims carry `path:line` (e.g. `pipeline/executor.py:41-60`, `sprint/executor.py:1519`). Proposed-layer modules use design paths (`adapters/backlog/import_tasklist.*`) explicitly tagged `[DESIGN — UNBUILT]`. External claims cite source URLs (synth-04 §5.7/§5.8). |
| 5 | Options analysis quality | N/A (§6, out of scope) | Options Analysis is template §6 (synth-05/06/07). synth-01 §2.3 references Option D→A + FEASIBILITY-STUDY §6.1/§6.2/§7.2; verified those headers exist in the source doc. |
| 6 | Implementation/extension specificity | PASS (in-scope) | Extension Guide is §13 (out of scope). In-scope adapter contracts (synth-04 §5.6, synth-02 §3.2/§4.3) are specific: named modules, directions, round-trip validation contracts, mapped to concrete current models (`StepStatus`/`TaskStatus`/`GateOutcome`@`pipeline/models.py:40-67`). No generic "create a service" placeholders. |
| 7 | Cross-section consistency | PASS | Seam (`StepRunner`/`ClaudeProcess`) described identically in synth-01 §2.1/§2.3, synth-02 §4.1 hop (F), synth-03 §5.1, synth-04 §5.6. Subsystem numbering 5.1-5.8 consistent across synth-01 §2.2 map and synth-03/04 bodies. Ownership split (Backlog=prose/Beads=graph/Mastra=run) identical in synth-01 §2.1, synth-02 §4.1, synth-04 §5.5. No contradictions. |
| 8 | No doc-only claims in Architecture | PASS | Every BUILT architecture claim in synth-01 §2, synth-03 §5.1-5.3 is code-traced with `path:line`, not doc-sourced. External capability claims (synth-04 §5.7) correctly segregated under `[EXTERNAL-VERIFIED]`, NOT presented as SuperClaude architecture. |
| 9 | Stale/contradicted discrepancies surfaced | PASS | Stale docs carried forward as flagged facts: roadmap "gates run on ORIGINAL output" CODE-CONTRADICTED (synth-03 §5.1, 5.1-44); README stale counts (synth-04 §5.4); checkpoint legacy/numbered drift (synth-04 §5.5); cli_portify/cleanup_audit drift (synth-04 §5.6). All marked "carry forward, not silently fix". |
| 10 | Content-rules compliance | PASS | Tables-over-prose throughout. No full source reproductions (only signature sketches in "Public Interface" code blocks, permitted by template L294-299). ASCII diagrams for architecture (synth-01 §2.1, synth-02 §3/§4.1). Statistics stated once (synth-01 §1). Evidence cited inline. |
| 11 | All sections have content (no placeholders) | FIXED | All in-scope sections §1-§5.8 fully populated; no `[bracketed placeholder]` tokens remain. **Issue:** synth-02 + synth-03 carried stale `Status: In Progress` headers contradicting `Status: Complete` footers — fixed in-place (Issues #1, #2). |
| 12 | No hallucinated file paths (BUILT paths exist) | PASS | `src/superclaude/cli/{pipeline,roadmap,tasklist,sprint}` all exist. Every sampled BUILT `path:line` resolves at HEAD `9e864860`. Proposed `adapters/` tree correctly does NOT exist (`ls adapters/` → No such file) and is uniformly `[DESIGN — UNBUILT]` — intended state, not hallucination. |

## Built-vs-Design Enforcement (additional gate)

| Check | Result | Evidence |
|-------|--------|----------|
| Every claim has exactly one tag | PASS | Each fact carries one of `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` / `[DESIGN — NOT PROVIDED]`. Mixed subsystems (5.5, 5.6) split per-row (current=`[CODE-VERIFIED]`, target=`[DESIGN]`) rather than double-tagging one claim. No untagged architecture claims found. |
| No `[DESIGN]` presented as built | PASS | All adapter/Mastra/Backlog/Beads integration uniformly tagged design/external. synth-01 §1 + synth-02 L17 + synth-03 L8 + synth-04 §5.5/5.6/5.8 all carry explicit "does not exist in the repository today" CRITICAL banners citing 5.6-27. |
| `[CODE-VERIFIED]` cites real path:line valid at HEAD 9e864860 | PASS | Independently re-read 9 distinct citations (listed in item 3). All resolved. HEAD confirmed `9e864860`. CERTIFY unwired + rerun-tasks ABSENT claims independently reproduced via grep (zero callsites / zero matches). |
| `[EXTERNAL-VERIFIED]` cites URLs | PASS | synth-04 §5.7 (Mastra/Backlog/Beads capability tables) and §5.8 (governance) carry source URLs per row (mastra.ai/docs, github.com/MrLesk/Backlog.md, github.com/gastownhall/beads, modelcontextprotocol.io). |
| §1 has PROPOSED framing + tag legend | PASS | synth-01 §1 opens with "CRITICAL — PROPOSED, NOT-YET-BUILT ARCHITECTURE" banner (L16) and §1.1 Tag Legend table (L26-34) defining all three tags with evidence basis. |

## Summary

- Checks passed: 16 / 17 (1 FIXED). 0 remaining failures.
- Checks failed (unresolved): 0
- Critical issues: 0
- Issues fixed in-place: 2 (both MINOR)

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | MINOR | synth-02 L5 | Header `**Status:** In Progress` contradicts footer L264 `**Status: Complete**`. A synthesis file labelled in-progress signals incomplete work to the assembly phase. | Set header status to Complete (footer is authoritative; file content is fully populated). | FIXED in-place |
| 2 | MINOR | synth-03 L10 | Header `**Status: In progress**` contradicts footer L266 `**Status: Complete**`. Same stale-header inconsistency. | Set header status to Complete. | FIXED in-place |

## Actions Taken

- Fixed synth-02 header `Status: In Progress` → `Status: Complete` (Edit). Verified: file content is fully populated through §4.3 with a "Status: Complete" footer; the header was the only stale token.
- Fixed synth-03 header `Status: In progress` → `Status: Complete` (Edit). Verified: file content fully populated through §5.3 Conventions with "Status: Complete" footer.
- No fabrication, hallucinated path, doc-only architecture claim, or design-as-built mistagging required correction — none were found.

## Confidence Gate

- **Confidence:** Verified: 16/16 | Unverifiable: 1 (item 5 N/A — §6 out of scope) | Unchecked: 0 | Confidence: 100.0% (16/(17-1))
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 6 (each Bash batched multiple grep/sed/ls verifications mapping to specific checklist items: HEAD+models+executor, Popen+gates+checkpoint+rerun, CERTIFY+subcommands+counts, cli-dirs+adapters+support-docs, DECISION+FEASIBILITY headers, core-CLAUDE+deliverables+grace_period). No web research performed (no external claim required live re-fetch — synth-04 URLs were treated as `[EXTERNAL-VERIFIED]` provenance, consistent with source-truth-first; spot-checking external URLs is the report-validation phase's job, not synthesis-gate).
- No UNCHECKED items. Item 5 UNVERIFIABLE blocker: Options Analysis (§6) is owned by synth-05/06/07, outside this partition's assigned files.

## Recommendations

- Green light to proceed to assembly (Phase 6) for the §1-§5.8 fragments. Both fixes applied; no blockers remain.
- Carry the flagged stale-doc / drift / unwired-gate items (5.1-44, CERTIFY unwired, WIRING blocking, deviation classifier UNCLASSIFIED, Path-A checkpoint skip, README stale counts, checkpoint drift) into template §14 (Known Limitations & Technical Debt) during assembly — synth files correctly route them there.
- At report-validation phase, spot-check a sample of the `[EXTERNAL-VERIFIED]` URLs (Tavily-first) since those were not live-fetched at synthesis-gate.

## QA Complete
