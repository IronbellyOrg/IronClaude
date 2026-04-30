# QA Report — Skill-Create Source Fidelity (Reference-Skill Semantic Coverage Lens)

**Topic:** sc-persona-research-protocol SKILL.md fidelity vs. reference skills
**Date:** 2026-04-30
**Phase:** skillcreate-source-fidelity
**Lens:** reference-skill-semantic-coverage
**Fix cycle:** N/A (initial pass)
**Fix authorization:** false (REPORT ONLY)

**Generated SKILL.md:** `/config/workspace/IronClaude/.temp/skills/sc-persona-research-protocol/SKILL.md` (1887 lines)
**Reference skills inspected:**
- `/config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md` (1322 lines — canonical reference)
- `/config/workspace/IronClaude/.claude/skills/skill-creator/SKILL.md` (1522 lines)
- `/config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md` (1709 lines)
- `/config/workspace/IronClaude/.claude/skills/prd/SKILL.md` (454 lines)
- `/config/workspace/IronClaude/.claude/skills/tdd/SKILL.md` (421 lines)

**Reference analyses inspected:**
- `02-reference-tech-research.md` through `06-reference-tdd.md`
- `01-canonical-reference-summary.md` (29-section anchor table)
- `12-section-classification.md` (COPY/SUBSTITUTE/GENERATE classification per section)

---

## Overall Verdict: **FAIL**

The generated SKILL.md preserves the **broad structural shell** of the canonical tech-research reference (Two-stage A/B execution, Stage A.1-A.8 sub-steps, F1 execution loop, parallel spawning protocol, Incremental File Writing Protocol, Documentation Staleness Protocol, ADVERSARIAL STANCE, VERDICTS blocks, 3-tier depth table, agent type roster, mandatory research notes file, A.5 sufficiency gate, A.6 template triage, BUILD_REQUEST scaffold, Validation Checklist, Critical Rules, Session Management, Research Quality Signals). For pattern-level coverage (the prompt's checklist item 1), the skill PASSES.

However, **multiple non-trivial fidelity violations** exist on:
- detail preservation (item 2),
- template compliance / canonical section ordering (item 3),
- domain-noun leakage (item 4),
- and one phantom-coverage violation (item 5).

Verdict overall: **FAIL** — at least **6 fidelity violations** require remediation before this SKILL.md can claim faithful inheritance from the reference skills.

---

## Confidence

**Verified:** 5/5 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
**Tool engagement:** Read: 8 | Grep (via Read scan): integrated | Glob: 0 | Bash: 2

Each of the 5 prompt-level checklist items was verified against either the generated SKILL.md byte content (Read with offset/limit) or the cited reference skill, and findings cite specific line references on both sides.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Semantic coverage of reference-skill patterns | **PASS** | Two-stage A/B (gen lines 192-227 vs tech-research lines 134-153), F1 execution loop READ→IDENTIFY→EXECUTE→UPDATE→REPEAT (gen 537-553 vs TR 463-553), Parallel Spawning (gen 566-579 vs TR 488-505), Incremental File Writing Protocol (gen multiple sites incl. 657-675, 773-792 vs TR 570-590), Documentation Staleness Protocol (gen 677-708, 803-820 vs TR 601-628), ADVERSARIAL STANCE (gen 683, 822, 947, 1144 etc. vs TR 760, 776, 865), VERDICTS PASS/FAIL (gen 702-708, 873-878, 1147-1149 etc. vs TR 755-757, 800-802, 847-849), Depth Tiers 3-row table (gen 149-153 vs TR 95-99), 6-mandatory-categories Research Notes (gen 348-391 vs TR 231-271), A.5 sufficiency gate w/ max-2-rounds (gen 393-415 vs TR 273-294), A.6 Template Triage (gen 417-433 vs TR 296-312), BUILD_REQUEST scaffold (gen 441-510 vs TR 314-448). Patterns are present, not just mentioned. |
| 2 | Detail preservation (line ranges + verbatim protocol blocks + naming/path conventions) | **FAIL** | See Issues 2A, 2B, 2C below. |
| 3 | Template compliance (canonical section ordering) | **FAIL** | See Issue 3 below. |
| 4 | Domain-noun leakage (no tech-research / prd / tdd / skill-creator / task-builder leakage into SUBSTITUTE/GENERATE sections) | **FAIL** | See Issue 4 below. |
| 5 | Phantom coverage (claimed pattern → empty implementation) | **FAIL** | See Issue 5 below. |

## Summary
- Checks passed: 1 / 5
- Checks failed: 4
- Critical issues: 2
- Important issues: 3
- Minor issues: 1

---

## Issues Found

### Issue 1 — Section §21.1 (29-section "logical schema") names DO NOT match the actual SKILL.md headers OR the canonical reference

**Severity:** CRITICAL
**Lens item:** 3 (Template Compliance) + 5 (Phantom Coverage)
**Location:** `SKILL.md` lines 1449-1483 (the §21.1 fenced "29-section" reference schema inside Output Structure)

The §21.1 fenced schema lists logical section names that do NOT match (a) the actual `## ` headers in this SKILL.md, (b) the canonical 29-section spine inferred from tech-research, NOR (c) the section-classification file (`research/12-section-classification.md`).

Examples of mismatch:

| §21.1 logical label (gen 1454-1483) | Actual `## ` header in this SKILL.md | Tech-research canonical (research file 01) |
|---|---|---|
| `## 2. When to Use This Skill` | (no such header) | "Overview + How-it-works" (S2) |
| `## 3. When NOT to Use This Skill` | (no such header) | "Why This Process Works" (S3) |
| `## 4. Skill Triggers` | (no such header) | "Variable Reference" — sub-section of S3 |
| `## 5. Input` | `## Input` (line 55) — matches | "Input" (S5) |
| `## 8. Variable Reference` | `### Variable Reference` (line 33, sub of Why) | S4 (per canonical summary) |
| `## 10. Stage A — Task File Construction (overview)` | `## Stage A: Scope Discovery & Task File Creation` (line 230) | "Execution Overview" (S10) |
| `## 11. A.1 Confirm Task ID & Output Path` | `### A.1: Check for Existing Task File` (line 232) | "Stage A header" (S11) |
| `## 12. A.2 Conduct Codebase Research` | `### A.2: Parse & Triage the Input` (line 246) | "A.1 Check for Existing Task File" (S12) |
| `## 13. A.3 Perform Scope Discovery` | `### A.3: Perform Scope Discovery` (line 290) | "A.2 Parse & Triage" (S13) |
| `## 19. Stage B — Delegate to /sc:task-unified` | `## Stage B: Task File Execution` (line 535) | "Stage B Task File Execution" (S19) |

This means the **logical schema in §21.1 fabricates section names** (e.g., "When to Use This Skill", "When NOT to Use This Skill", "Skill Triggers", "Confirm Task ID & Output Path", "Conduct Codebase Research", "Plan Phases & Items", "Stage A Output", "Delegate to /sc:task-unified") that **do not exist in this skill, do not match the canonical reference, and do not match the section-classification file** (which uses the tech-research-aligned spine: S2 Overview, S3 Why-this-works, S4 Variable Reference, S5 Input, S10 Execution Overview, S11 Stage A header, S12 A.1 Check for Existing Task File, etc.).

This is BOTH a phantom-coverage violation (claims a 29-section structure but the schema lists fabricated names) AND a template-compliance violation (the canonical spine has been altered without justification).

**Required fix:** Replace the §21.1 fenced schema with names that match (a) the actual `## ` headers in this document AND (b) the canonical mapping in `research/12-section-classification.md` (which classifies sections per the tech-research spine).

---

### Issue 2A — `## 19. Stage B — Delegate to /sc:task-unified` is a hallucinated section name

**Severity:** CRITICAL
**Lens item:** 4 (Domain-noun leakage) + 5 (Phantom coverage)
**Location:** `SKILL.md` line 1472

The §21.1 schema names section 19 as `## 19. Stage B — Delegate to /sc:task-unified`. This conflicts with the actual Stage B implementation in this SKILL.md (lines 535-625), which is **NOT** a `/sc:task-unified` delegation pattern — it is the **inline F1 execution loop** READ→IDENTIFY→EXECUTE→UPDATE→REPEAT pattern (line 542). The reference (tech-research) Stage B is also the inline F1 loop, not a delegation pattern.

The string "/sc:task-unified" appears NOWHERE else in the live skill content (only in §21.1's hallucinated label). This is a leaked external naming convention that does not match either the persona-research domain or the canonical reference.

**Required fix:** Either (a) remove the `— Delegate to /sc:task-unified` suffix from §21.1, or (b) replace with the canonical Stage B label "Stage B: Task File Execution".

---

### Issue 2B — A.7/A.8 step numbering mismatch between SKILL.md and §21.1 schema

**Severity:** IMPORTANT
**Lens item:** 2 (Detail preservation) + 3 (Template compliance)
**Location:** `SKILL.md` §21.1 schema (lines 1454-1483) vs. actual headers (lines 230-531)

The §21.1 schema lists Stage A as having sections `A.1 Confirm Task ID & Output Path`, `A.2 Conduct Codebase Research`, `A.3 Perform Scope Discovery`, `A.4 Categorize Research`, `A.5 Determine Output Strategy`, `A.6 Plan Phases & Items`, `A.7 Build Task File via task-builder`, then `Stage A Output` (S18).

The ACTUAL Stage A in this SKILL.md has sub-steps:
- `A.1: Check for Existing Task File` (line 232)
- `A.2: Parse & Triage the Input` (line 246)
- `A.3: Perform Scope Discovery` (line 290)
- `A.4: Write Research Notes File (MANDATORY)` (line 342)
- `A.5: Review Research Sufficiency (MANDATORY GATE)` (line 393)
- `A.6: Template Triage` (line 417)
- `A.7: Build the Task File` (line 435)
- `A.8: Receive & Verify the Task File` (line 516)

These two A-step lists do not match. The actual implementation correctly mirrors the canonical tech-research A.1-A.8 sequence (per `01-canonical-reference-summary.md` lines 18-28). The fabricated §21.1 schema is the broken artifact.

**Required fix:** Remove the §21.1 fenced schema OR replace it with the actual heading list that matches lines 232-516 of this SKILL.md (and tech-research lines 156-461).

---

### Issue 2C — Variable Reference promoted to top-level S8 in §21.1 but rendered as a subsection in actual document

**Severity:** MINOR
**Lens item:** 3 (Template compliance)
**Location:** `SKILL.md` line 33 (actual `### Variable Reference`) vs. §21.1 line 1461 (`## 8. Variable Reference`)

In this SKILL.md the Variable Reference is rendered at line 33 as `### Variable Reference` — a subsection nested inside `## Why This Process Works`. The §21.1 schema lists it as a top-level `## 8. Variable Reference`. The canonical reference (tech-research) renders it as a subsection of "Why This Process Works" (per `01-canonical-reference-summary.md` line 12) — so the actual rendering is faithful, but the schema misclassifies it.

**Required fix:** Update §21.1 to mark Variable Reference as a sub-section of S3 (Why This Process Works), or align the actual document to promote it to a top-level header (preferred per canonical summary line 12 which classifies it as S4 — but a sub-section of S3 in tech-research practice).

---

### Issue 3 — Verbatim protocol blocks present but with non-trivial wording deltas

**Severity:** IMPORTANT
**Lens item:** 2 (Detail preservation — verbatim block fidelity)
**Location:** Multiple agent prompts in S20

Per canonical summary lines 47-50, the following blocks are required to be **byte-copy verbatim** when included:
- Incremental File Writing Protocol (tech-research lines 570-590)
- Documentation Staleness Protocol (tech-research lines 601-628)
- ADVERSARIAL STANCE phrasing
- VERDICTS PASS/FAIL phrasing

The generated SKILL.md DOES include these blocks but with localized wording substitutions:

1. **Incremental File Writing Protocol** at gen lines 657-675 (Identity Verifier) drops the canonical step-2 phrase "As you investigate each **file, component, or logical unit**" and substitutes "As you investigate each **disambiguation signal**". This is a domain-appropriate substitution, but per canonical summary line 47, the protocol is supposed to be byte-copy verbatim — the substitution is acceptable for the loop-body phrase but the surrounding scaffolding (steps 1, 3, 4) is faithful.

2. **Documentation Staleness Protocol** at gen lines 803-820 (Archetype-Driven Worker) significantly **rewrites the protocol** rather than copying verbatim. The canonical (tech-research lines 601-628) has 4 numbered items (Services/components, Pipelines/call chains, File paths, API endpoints). The generated rewrite has 4 different items (Firm/role described in source, Deal-history claims, Quotes (FR-7), Thesis statements). The 3-tag system `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` is replaced with `[MULTI-SOURCE-VERIFIED]`/`[SOURCE-CONTRADICTED]`/`[UNVERIFIED]`. This is a domain rewrite, not a byte-copy.

   The Identity Verifier (gen 677-682) uses yet another variant tagging: `[SOURCE-VERIFIED]`/`[SOURCE-CONTRADICTED]`/`[UNVERIFIED]`. Three different tag systems within the same document.

**Severity rationale:** Per `01-canonical-reference-summary.md` line 47, these are "byte-copy boilerplate". A domain-specific rewrite is acceptable IF the reference analysis explicitly classifies the section as SUBSTITUTE/GENERATE — and `12-section-classification.md` does classify S20 as GENERATE. So the rewrite itself is permitted by classification, but the inconsistency (3 different `[*-VERIFIED]` tag schemes within S20) is a detail-preservation issue. Mark as IMPORTANT (not CRITICAL) because the classification permits domain rewrites.

**Required fix:** Standardize the source-provenance tag system to a single scheme (e.g., always `[MULTI-SOURCE-VERIFIED]`/`[SOURCE-CONTRADICTED]`/`[UNVERIFIED]`) across all S20 prompts. Either keep the canonical 3-tag scheme verbatim from tech-research or document the chosen domain-specific scheme in S26 Content Rules.

---

### Issue 4 — Domain-noun leakage: `/sc:task-unified` and `tech-research` in SUBSTITUTE/GENERATE sections

**Severity:** IMPORTANT
**Lens item:** 4 (Domain-noun leakage)
**Locations:**

(a) `SKILL.md` line 1472 — `## 19. Stage B — Delegate to /sc:task-unified`. The token `/sc:task-unified` is a leaked external command name (it refers to a SuperClaude protocol, not the persona-research domain or the canonical RF tech-research reference). Per the spawn-prompt guidance ("No tech-research/prd/tdd/task-builder/skill-creator domain nouns leaked into SUBSTITUTE/GENERATE sections"), this is leakage. (Same as Issue 2A from a different angle.)

(b) `SKILL.md` line 1535 — Synthesis Mapping Table row reads:
> `S20 Agent Prompt Templates | spec §5 architecture + §9.2 model-tiering + §5.2 worker contract (files 07, 08) | GENERATE (6 domain agents + 6 lens QA + 3 source-fidelity)`
This is fine (an explicit mapping row). However at line 1126:
> `Reference template: [reference path — e.g., the 29-section structure from /config/workspace/IronClaude/.dev/releases/current/skill-creator/]`
This embeds a `skill-creator` path inside the Lens QA prompt body. Acceptable as a reference (per spawn-prompt note: "A reference to ... inside a citation ... is intentional"), but the prompt also names the Lens-QA artifact under inspection as "the produced SKILL.md (when this skill is being used to generate another skill)" (line 1120). This implies the persona-research skill is being conflated with skill-creator's workload — a reference-skill domain leak rather than a citation.

(c) `SKILL.md` line 1535 (and 1532, 1538) — multiple Synthesis Mapping rows reference "tech-research S6 boilerplate", "tech-research S26", "tech-research S28 boilerplate", "tech-research S29". These are intentional citations of source provenance and are permitted by the spawn-prompt guidance, BUT the same rows treat the persona-research domain as an inheritor of those tech-research sections. The classification (SUBSTITUTE) supports this, so these citations are NOT leakage. NO FIX NEEDED for these.

(d) `SKILL.md` line 1679 — VALIDATION_REQUIREMENT CROSS_VALIDATION reads:
> `SUBSTITUTE-classified sections contain no leftover tech-research / skill-creator / prd / tdd domain nouns.`
This is a **meta-check rule**, not leakage — it explicitly defines the rule that other sections must satisfy. Acceptable.

(e) `SKILL.md` line 1786 (Critical Rule 13) — `If tech-research/SKILL.md, skill-creator/SKILL.md, task-builder/SKILL.md, prd/SKILL.md, or tdd/SKILL.md is missing, halt`. This rule presumes these reference paths must exist for the skill TO RUN at runtime. This is incorrect — the reference skills are needed during **skill generation**, not during a runtime persona-research run. Per Section §21 the runtime artifacts (dossiers, persona TOML, archetype YAMLs) do not depend on the reference skills. This rule has leaked from a meta-context (skill-creator's generation pipeline) into the runtime Critical Rules. **This is a true leakage.**

**Required fix:**
- (a) Remove `/sc:task-unified` from §21.1 (covered by Issue 2A).
- (b) Audit the Lens QA prompt at lines 1117-1152 to clarify whether it inspects (a) generated-skill output, or (b) persona-research runtime artifacts. The current prompt text conflates both.
- (e) Either remove Critical Rule 13 OR move it into a "Skill Generation Rules" subsection that is clearly out of scope for runtime persona-research runs.

---

### Issue 5 — Phantom coverage: §27 Critical Rules claims "Rules 1-9 are universal protocol (boilerplate from tech-research / skill-creator); Rules 10-22 are skill-creator template-discipline rules" but several rules are only partially implemented

**Severity:** IMPORTANT
**Lens item:** 5 (Phantom coverage) + 4 (Domain-noun leakage)
**Location:** `SKILL.md` lines 1758-1820

The introductory sentence at line 1760 categorizes 28 Critical Rules into three buckets:
- Rules 1-9: universal boilerplate (from tech-research / skill-creator)
- Rules 10-22: skill-creator template-discipline rules
- Rules 23-28: persona-research domain rules

Issues:

(a) **Rule 18** (line 1796) reads:
> `Spec partitioning when input >1000 lines. The persona-research-skill-spec.md is 993 lines, but combined with the 2088-line developer guide far exceeds the partitioning threshold. Phase 2b spawned 3 spec analyst agents (Part 1, Part 2, Part 3); Phase 2c spawned 2 guide analyst agents.`

This rule documents the **skill-generation** context (Phase 2b/2c references) but is presented as a runtime "Critical Rule". It's a phantom rule for runtime persona-research execution — it has no applicability to a runtime run. This rule belongs in skill-creator's documentation OR a "Skill Generation Notes" appendix, not in this skill's runtime Critical Rules.

(b) **Rule 11** (line 1782): `COPY/SUBSTITUTE/GENERATE discipline. Every section in the SKILL.md must have a documented classification (see file 12-section-classification.md produced by Phase 2d). A section presented as COPY but with non-trivial content drift is a violation.` Same problem — this is a generation-time rule, not a runtime rule. The file `12-section-classification.md` exists in the TASK directory used to GENERATE this skill, not in the runtime persona-research task directory.

(c) **Rule 12** (line 1784): "Section count is exactly 29." This is a generation-time invariant.

(d) **Rule 13** (line 1786): Reference skill paths must exist before Phase 2 — same generation-time leak (also flagged as Issue 4(e)).

(e) **Rule 16** (line 1792): "Verbatim protocol blocks. S19 Stage B must contain the Incremental File Writing Protocol, Documentation Staleness Protocol, ADVERSARIAL STANCE, and VERDICTS blocks byte-verbatim from tech-research." — generation-time invariant. (Note: also flagged separately in Issue 3 because the rule is asserted but Issue 3 shows it is not actually held byte-verbatim across all S20 prompts.)

(f) **Rule 18 of S27** (re. spec partitioning) makes an unverifiable claim: "The persona-research-skill-spec.md is 993 lines". This is a one-time-context-of-generation fact frozen into a Critical Rule. It is not a rule — it is a footnote. Phantom.

**Required fix:** Move generation-time rules (Rules 11, 12, 13, 16, 18) into a separate "Skill Generation Provenance" appendix OR clearly demarcate "Rules 10-22 are skill-creator template-discipline rules — applied during this skill's GENERATION, not its runtime" so the runtime reader is not confused into thinking these rules govern persona-research executions.

---

## Issues Found Summary Table

| # | Severity | Location (gen line) | Issue | Lens item |
|---|----------|---------------------|-------|-----------|
| 1 | CRITICAL | §21.1 lines 1449-1483 | 29-section logical schema lists fabricated section names that don't match actual headers OR canonical reference OR classification file | 3, 5 |
| 2A | CRITICAL | §21.1 line 1472 | `Stage B — Delegate to /sc:task-unified` — hallucinated and inconsistent with actual Stage B (which is inline F1 loop) | 4, 5 |
| 2B | IMPORTANT | §21.1 lines 1454-1483 | A.1-A.7 step labels in §21.1 do not match the actual A.1-A.8 in this document (or canonical) | 2, 3 |
| 2C | MINOR | §21.1 line 1461 | Variable Reference promoted to top-level S8 in schema but rendered as `### Variable Reference` sub-section of S3 in actual doc | 3 |
| 3 | IMPORTANT | S20 prompts (multiple) | Three different `[*-VERIFIED]` provenance tag schemes across S20 (`[SOURCE-VERIFIED]`, `[MULTI-SOURCE-VERIFIED]`, `[CODE-VERIFIED]`); Documentation Staleness Protocol rewritten rather than byte-copied | 2 |
| 4 | IMPORTANT | Rule 13 line 1786; Lens-QA prompt 1126 | `/sc:task-unified`, generation-time-only references leaked into runtime sections | 4 |
| 5 | IMPORTANT | §27 Rules 11/12/13/16/18 | Generation-time-only rules embedded as runtime Critical Rules — phantom coverage of "runtime invariants" | 4, 5 |

---

## Actions Taken

None — fix authorization is **false** for this report. Issues are documented for the orchestrator/user to remediate.

---

## Recommendations

**Before marking this skill as production-ready, the following must be resolved:**

1. **Replace the §21.1 fenced "29-section" schema** (gen lines 1449-1483) with an accurate header list that matches both this SKILL.md's actual `## ` headers AND the section-classification file (`research/12-section-classification.md`). Resolves Issues 1, 2A, 2B, 2C.
2. **Standardize source-provenance tags across S20 prompts** to a single scheme (recommend `[MULTI-SOURCE-VERIFIED]`/`[SOURCE-CONTRADICTED]`/`[UNVERIFIED]` since persona-research is sourcing from web docs, not codebase). Document the choice in S26. Resolves Issue 3.
3. **Demarcate generation-time rules from runtime rules** in §27. Either move Rules 11, 12, 13, 16, 18 into a "Skill Generation Provenance" appendix OR add a clear sub-header `### 27.B Skill Generation Rules (apply only during this skill's generation, not during runtime persona-research)`. Resolves Issues 4(e) and 5.
4. **Audit the Lens QA prompts at lines 1117-1316** for context-conflation: each prompt should clearly state whether it inspects (a) the generated SKILL.md (skill-creation context), or (b) runtime persona-research artifacts (dossier, persona TOML, archetype YAML). The current text mixes both. Resolves Issue 4(b).
5. **Cross-reference Issue 3 with the QA-evidence-quality lens (Lens 3)** to ensure that the inconsistent provenance tag schemes are surfaced there as well — this is a multi-lens finding.

After these fixes, re-run this Reference-Skill Semantic Coverage lens. If it passes, proceed to Source-Fidelity 2 of 3 (Spec FR Coverage).

## QA Complete

**[PARTITION NOTE: This is a single-instance lens (no `assigned_files` partition). All 5 reference skills + the generated SKILL.md were inspected within this report.]**
