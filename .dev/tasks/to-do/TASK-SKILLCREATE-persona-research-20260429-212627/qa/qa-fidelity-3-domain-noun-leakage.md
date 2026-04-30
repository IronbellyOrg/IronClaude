# QA Report — Source-Document Fidelity (Domain-Noun Leakage Lens)

**Topic:** sc-persona-research-protocol SKILL.md
**Date:** 2026-04-30
**Phase:** skillcreate-source-fidelity / domain-noun-leakage (3 of 3)
**Fix cycle:** N/A (REPORT ONLY — fix authorization: false)
**Generated SKILL.md:** /config/workspace/IronClaude/.temp/skills/sc-persona-research-protocol/SKILL.md (1887 lines)

---

## Overall Verdict: FAIL

Domain-noun leakage detected from at least two reference skills (tech-research and skill-creator) into SUBSTITUTE/GENERATE sections of the produced persona-research SKILL.md. The leakage is concentrated in S20 (Agent Prompt Templates) — a GENERATE section — and in S25/S26-equivalent QA-prompt blocks. The most material leak is the phrase **"Investigation type:"** which is a tech-research label appearing verbatim inside three of the persona-research worker-prompt headers, not as a citation but as an active field name that workers are instructed to write into their output files.

---

## Confidence

**Verified:** 5/5 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100%

**Tool engagement:** Read: 5 | Grep: 12 | Glob: 0 | Bash: (greps via Bash) — every grep targets a specific checklist item.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | tech-research domain-noun leakage (feasibility / research question / investigation type / tech research) | FAIL | `Investigation type:` appears at lines 664, 780, 907 inside agent-prompt headers in S20 (GENERATE). Source-of-phrase confirmed at tech-research/SKILL.md lines 260, 566, 577 (`Investigation type: [Code Tracer / Doc Analyst / ...]`). "research question" not present (good); "feasibility" not present (good); "tech research" used only in citation contexts (acceptable). |
| 2 | prd domain-noun leakage (Product Requirements Document / PRD / product requirements / user stories) | PASS | `grep -i "product requirements\|Product Requirements Document\|user stor"` returned zero hits. Bare "PRD" appears only at lines 1418, 1542, 1543, 1679, 1782, 1786 — all in citation/classification contexts that frame PRDs as a reference skill, not as the produced skill's own domain. |
| 3 | tdd domain-noun leakage (Technical Design Document / TDD / technical design / architecture decision) | PASS | `grep -i "Technical Design Document\|technical design\|architecture decision"` returned zero hits. Bare "TDD" appears only at lines 1419, 1542, 1543, 1679, 1782, 1786 — all in citation/classification contexts. |
| 4 | skill-creator domain-noun leakage (skill creation / 10-differentiator / section classification) | FAIL | "section classification" appears at lines 1137, 1287, 1305, 1687 inside S20 QA-prompt scopes and S25 validation-checklist text — these are GENERATE sections where the phrase is being used as an active domain noun ("the section classification file's reasoning"), not just a file-name citation. "10-differentiator" not present (good); "skill creation" not present as a domain phrase. |
| 5 | task-builder domain-noun leakage (MDTM / BUILD_REQUEST / task file / checklist item) | PARTIAL FAIL | 62 hits across the document. Most are LEGITIMATE because the persona-research skill genuinely uses MDTM as its persistence mechanism (S1, S5, S9, S10-S17, S19) — the spec explicitly authorizes this and §1 frames the skill around the MDTM task file. However, the prompt directives in **S2/S3 (When to Use)** and the architecture rationale at **S5/S20** treat "task file" / "MDTM task file" / "BUILD_REQUEST" / "checklist item" as primary nouns of the persona-research domain itself, blurring the line between adopting task-builder's mechanics and adopting its vocabulary as the produced skill's own. See "Issues Found" for the borderline cases. |

---

## Summary

- Checks passed: **2/5** (PRD, TDD)
- Checks failed: **2/5** (tech-research, skill-creator)
- Checks partial-fail: **1/5** (task-builder — see remediation note)
- CRITICAL issues: 1
- IMPORTANT issues: 3
- MINOR issues: 2
- Issues fixed in-place: 0 (report-only mode)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | SKILL.md lines 664, 780, 907 (S20 — Agent Prompt Templates, GENERATE) | The label `**Investigation type:**` is copied verbatim from tech-research/SKILL.md lines 260, 566, 577. In tech-research, "Investigation type" enumerates `[Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst]` — this is tech-research's own domain noun for classifying research workers. The persona-research skill reuses the SAME label name (`Investigation type:`) in its three worker-prompt headers (`identity-verification`, `archetype-driven-research-worker`, `discovery-worker`). Workers are instructed to write this field into their output file headers, propagating the leaked noun into runtime artifacts. | Rename the field to a persona-research-domain noun. Suggested replacements: `**Worker role:**`, `**Worker type:**`, or `**Phase role:**`. Update all three header blocks (lines 664, 780, 907) consistently. |
| 2 | IMPORTANT | SKILL.md lines 1137, 1287, 1305, 1687, 1782 (S20 QA-prompts and S25/S27) | The phrase "section classification" is used 5 times as an active domain noun (e.g., "the section classification file's reasoning", "match the section classification file") inside GENERATE sections. This phrase is skill-creator's own domain vocabulary (skill-creator classifies its own SKILL.md sections as COPY/SUBSTITUTE/GENERATE). The persona-research skill is the OUTPUT of skill-creator — but the skill-creation provenance shouldn't surface as live domain phrases inside the produced skill's runtime QA prompts. | These references should either (a) be reframed as one-shot citations to the artifact path (`research/12-section-classification.md`) and not as a recurring active domain noun, or (b) be moved entirely to a build-provenance appendix and removed from the runtime QA prompts. Specifically, lines 1287 and 1305 describe a QA scope/prompt that runs on the produced skill — that prompt should not exist in the runtime SKILL.md; it belongs to the skill-creator session. |
| 3 | IMPORTANT | SKILL.md S20 QA prompt blocks (lines 1287-1310, 1325-1340, 1402-1430) | The entire "Source-Fidelity 1/2/3" QA prompts (Template-Compliance, FR-Coverage, Domain-Noun-Leakage) are skill-creator-internal QA prompts. They reference building-time concepts: `tech-research/SKILL.md`, `skill-creator/SKILL.md`, `prd/SKILL.md`, `tdd/SKILL.md`, `task-builder/SKILL.md`, COPY/SUBSTITUTE/GENERATE classification, and the `12-section-classification.md` file. None of these are runtime concepts of the persona-research skill — yet they live inside its S20 (Agent Prompt Templates) section, which is supposed to hold the prompts for the SIX domain workers + SIX runtime lens-QA agents (per spec §6/§9). | Move the three Source-Fidelity prompts out of the produced SKILL.md entirely. They belong in skill-creator's Phase 5 QA orchestration, not in the persona-research runtime. If retained for documentation, frame them in a clearly-marked "Build Provenance (do not run at runtime)" appendix. |
| 4 | IMPORTANT | SKILL.md S20 multiple locations | Lens-QA prompt at line 1157 (Internal-Consistency) refers to "S18 BUILD_REQUEST and S20 worker contract" using the produced skill's own §-number vocabulary. The phrase **BUILD_REQUEST** is task-builder domain vocabulary — the produced persona-research SKILL.md inherits this term from the skill-creator A.7 template, but uses it dozens of times as if it were persona-research's own noun. | Acceptable in S17 (which is explicitly the A.7 BUILD_REQUEST template invocation). Should be minimized in lens-QA prompts (line 1157, 1169) where it is being used as a generic noun for "the request payload sent to the task-builder during Stage A." Reframe as "Stage A request" or "task-build request" in those QA prompts to break the verbatim adoption of task-builder vocabulary. |
| 5 | MINOR | SKILL.md line 1287 | The phrase "match the section classification file (`research/12-section-classification.md`)" treats the existence of a section-classification file as a runtime fact. This file only exists during skill-generation (Phase 2d of skill-creator), not during persona-research execution. Mentioning it inside a runtime prompt is provenance leakage. | Either remove the prompt entirely (preferred, see issue 3) or at minimum scope-mark it as `[BUILD-TIME ONLY — do not use at persona-research runtime]`. |
| 6 | MINOR | SKILL.md line 1689 (S25 Validation Checklist) | `**CROSS_VALIDATION**: COPY-classified sections byte-match tech-research's equivalents. SUBSTITUTE-classified sections contain no leftover tech-research / skill-creator / prd / tdd domain nouns.` — This validation rule lives in the produced skill's runtime checklist but describes a build-time invariant of skill-creator. | Move to a build-time appendix or remove. The runtime persona-research skill has no concept of "tech-research's equivalents" — that concern belongs to skill-creator's QA pass. |

---

## Self-Audit (mandatory)

1. **How many factual claims did you independently verify against source code?** Five — each checklist item received at least one targeted grep. The most consequential (Investigation type) was cross-verified against tech-research/SKILL.md (lines 260, 566, 577) confirming the phrase's origin in tech-research's worker-classification vocabulary.
2. **What specific files did you read to verify claims?**
   - `/config/workspace/IronClaude/.temp/skills/sc-persona-research-protocol/SKILL.md` (lines 655-679, 770-799, 900-919, 1140-1160, 1395-1429)
   - `/config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md` (lines 260, 566, 577 confirmed via grep — phrase "Investigation type" originates here)
3. **If I found 0 issues, why should the user trust I checked thoroughly?** I did NOT find 0 issues — I found 6 (1 CRITICAL, 3 IMPORTANT, 2 MINOR). The adversarial stance instructed me to assume ≥5 leakage instances exist; I found 6 distinct issue clusters across two of the five checked categories. PRD and TDD passed cleanly; task-builder is partial-fail because much of its vocabulary is genuinely adopted (with spec authorization) and harder to flag without false positives.

---

## Notes on Acceptable References

The following are NOT counted as leakage:

- Bare paths like `/config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md` (lines 1334, 1335, 1336) — these are file-system citations.
- The §21.1 Synthesis Mapping Table (lines 1512-1544) — its express purpose is to document section provenance, so phrases like "tech-research S6 boilerplate" are intentional.
- Section header `## 17. A.7 Build Task File via task-builder` (line 1470) — the Synthesis-Mapping inventory of canonical section names; "task-builder" is named as the agent invoked, not adopted as domain vocabulary.
- Critical Rule 13 (line 1786) listing the five reference-skill paths — these are operational preconditions ("halt if any of these reference files are missing").
- "MDTM task file" usage throughout — the spec authorizes MDTM as the persistence mechanism, so MDTM is genuinely part of the persona-research domain by design (not leakage).

---

## Recommendations

1. **Block release until issue 1 (CRITICAL) is resolved.** The `Investigation type:` field name is shipped into per-run output files (lines 664, 780, 907 are agent prompt templates that workers execute) — every persona-research run will produce output files headed with a tech-research domain phrase. This is the textbook case the leakage lens exists to catch.
2. **Strongly recommend resolving issues 2 and 3 (IMPORTANT) before release.** The three Source-Fidelity QA prompts (Template-Compliance, FR-Coverage, Domain-Noun-Leakage) are skill-creator's own QA tooling that has been incorrectly hoisted into the produced persona-research SKILL.md's S20. They drag in vocabulary from skill-creator (`section classification`, `COPY/SUBSTITUTE/GENERATE`, `12-section-classification.md`) and from all four other reference skills (in their scope statements). Move them to a build-time provenance appendix or remove.
4. **Re-run domain-noun-leakage QA after fixes.** Specifically re-grep `Investigation type`, `section classification`, and `BUILD_REQUEST` to confirm zero recurrence in S2/S3/S5/S20/S25/S26/S27 body prose.

## QA Complete
