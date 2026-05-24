---
id: "PRD-TASK-DIRECTIONAL-MERGE"
title: "Task Directional Merge (/sc:task → /task) - Product Requirements Document (PRD)"
description: "Feature PRD for the directional merge of the donor /sc:task skill into the recipient /task skill, preserving INV-01..INV-05 under 9 manifest exceptions and an 8-Transfer-Unit transfer plan."
version: "1.0"
status: "🟡 Draft"
type: "📋 Product Requirements"
priority: "🔥 Highest"
created_date: "2026-05-16"
updated_date: "2026-05-16"
assigned_to: "product-team"
autogen: false
autogen_method: ""
coordinator: "product-manager"
parent_task: ""
depends_on:
- ".dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md"
- "src/superclaude/examples/prd_template.md"
related_docs:
- "src/superclaude/skills/task/SKILL.md"
- "src/superclaude/skills/sc-task-protocol/SKILL.md"
- "src/superclaude/commands/task.md"
tags:
- prd
- requirements
- feature-prd
- task-merge
- sc-task
- task
- directional-merge
- adversarial-validation
template_schema_doc: "src/superclaude/examples/prd_template.md"
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: "static"
---

# Task Directional Merge (/sc:task → /task) - Product Requirements Document (PRD)

> **WHAT:** This Feature PRD defines the requirements, scope, invariants, sequencing constraints, acceptance criteria, and KPIs for the directional merge of the donor `/sc:task` skill into the recipient `/task` skill, folding 8 Transfer Units under 9 manifest exceptions while preserving 5 load-bearing invariants (INV-01..INV-05).
> **WHY:** Two task-execution skills coexist in the framework with overlapping but non-identical surfaces. The donor must be folded into the recipient atomically (ME-6 single-PR landing) without breaking in-flight MDTM resumability or the rf-qa structural floor, closing the post-adversarial-validation phase of the validation-spec (V1 steelman + V2 attack chain + V3 security-probe converged).
> **HOW TO USE:** Engineering, QA, and release teams reference this PRD throughout the merge implementation, validation, and rollout lifecycle. Pair this PRD with the validation-spec for adversarial-validation provenance and with the forthcoming TDD for implementation architecture.

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| **Requirements** | **This PRD** | **Product** | **🟡 Draft** |
| Design | TDD (TBD) | Engineering | Not yet started |
| Implementation | Tech Reference (TBD) | Engineering | Not yet started |

### Tiered Usage

| Tier | When to Use | Sections to Skip |
|------|-------------|------------------|
| **Lightweight** | Single-feature PRD, <10 sections | Value Proposition Canvas, Customer Journey Map, API Contract Examples, Appendices, Document History (first version) |
| **Standard** | Multi-feature product, most PRDs | None — complete all sections |
| **Heavyweight** | Platform PRD, 28 sections, cross-team | None — complete all sections (this PRD is Heavyweight, Feature-PRD-abbreviated) |

---

## Document Information

| Field | Value |
|-------|-------|
| **Product Name** | Task Directional Merge (/sc:task → /task) |
| **Product Type** | Feature PRD |
| **Product Owner** | TBD |
| **Engineering Lead** | TBD |
| **Design Lead** | N/A (CLI/skill feature; no visual design) |
| **Maintained By** | TBD |
| **Stakeholders** | TBD (framework users, sprint executor, cleanup-audit, in-flight MDTM authors) |
| **Status** | 🟡 Draft |
| **Target Release** | TBD |
| **Last Updated** | 2026-05-16 |
| **Last Verified** | 2026-05-16 against current working tree (live grep, fix-cycle 1) |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | TBD | __________ | TBD |
| Engineering Lead | TBD | __________ | TBD |
| Design Lead | N/A | __________ | N/A |
| Executive Sponsor | TBD | __________ | TBD |

---

## Completeness Status

**Completeness Checklist:**
- [x] Section 1: Executive Summary — Complete
- [x] Sections 2-5: Problem, Background, Vision, Business Context — Complete (S5 abbreviated; refers to Platform PRD)
- [x] Sections 6-9: JTBD, Personas, Value Proposition, Competitive Analysis — S6/S7 Complete; S8 abbreviated (refers to Platform PRD); S9 marked N/A (Feature PRD)
- [x] Sections 10-13: Assumptions, Dependencies, Scope, Open Questions — Complete
- [x] Sections 14-15: Technical Requirements, Technology Stack — Complete
- [x] Sections 16-18: UX, Legal/Compliance, Business Requirements — S16.2 only (Feature-PRD abbreviation); S17/S18 reference Platform PRD
- [x] Sections 19-20: Success Metrics, Risk Analysis — Complete
- [x] Section 21: Implementation Plan (Epics/Stories, Product Reqs, Phasing, DoD, Timeline) — Complete
- [x] Sections 22-25: Customer Journey, Error Handling, Design, API Contracts — Complete
- [x] Sections 26-28: Contributors, Related Resources, Maintenance & Ownership — Complete

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | validation-spec.md (`.dev/releases/current/task-sc-task-directional-merge/validation-spec/`), donor and recipient SKILL.md files, donor and recipient command files, sprint executor (`src/superclaude/cli/sprint/process.py`), cleanup-audit prompts (`src/superclaude/cli/cleanup_audit/prompts.py`) |
| **Upstream** | Feeds from: validation-spec V1 steelman + V2 attack chain + V3 security-probe convergence; research notes (research-notes.md); 6 research files; 2 web research files |
| **Downstream** | Feeds to: TDD (TBD), Tech Reference (TBD), 10-step commit chain implementation, AC-ATK and AC-SM verification tickets |
| **Change Impact** | Notify: framework users, sprint executor users, cleanup-audit users, in-flight MDTM authors, rf-qa team |
| **Review Cadence** | TBD |
| **Living Document** | This PRD evolves as merge implementation and post-merge audits reveal new findings — see Document History for change log |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Background & Strategic Fit](#3-background--strategic-fit)
4. [Product Vision](#4-product-vision)
5. [Business Context](#5-business-context)
6. [Jobs To Be Done (JTBD)](#6-jobs-to-be-done-jtbd)
7. [User Personas](#7-user-personas)
8. [Value Proposition Canvas](#8-value-proposition-canvas)
9. [Competitive Analysis](#9-competitive-analysis)
10. [Assumptions & Constraints](#10-assumptions--constraints)
11. [Dependencies](#11-dependencies)
12. [Scope Definition](#12-scope-definition)
13. [Open Questions](#13-open-questions)
14. [Technical Requirements](#14-technical-requirements)
15. [Technology Stack](#15-technology-stack)
16. [User Experience Requirements](#16-user-experience-requirements)
17. [Legal & Compliance Requirements](#17-legal--compliance-requirements)
18. [Business Requirements](#18-business-requirements)
19. [Success Metrics & Measurement](#19-success-metrics--measurement)
20. [Risk Analysis](#20-risk-analysis)
21. [Implementation Plan](#21-implementation-plan)
22. [Customer Journey Map](#22-customer-journey-map)
23. [Error Handling & Edge Cases](#23-error-handling--edge-cases)
24. [User Interaction & Design](#24-user-interaction--design)
25. [API Contract Examples](#25-api-contract-examples)
26. [Contributors & Collaboration](#26-contributors--collaboration)
27. [Related Resources](#27-related-resources)
28. [Maintenance & Ownership](#28-maintenance--ownership)

---

## 1. Executive Summary

The `/sc:task` → `/task` directional merge folds the donor skill `src/superclaude/skills/sc-task-protocol/SKILL.md` (365 lines, currently invoked by the `/sc:task` command per `src/superclaude/commands/task.md:100`) `[CODE-VERIFIED]` into the recipient skill `src/superclaude/skills/task/SKILL.md` (F1 loop at `:79-98`; F2 prohibitions at `:104-117`; phase-gate rf-qa at `:191-198`) `[CODE-VERIFIED]`. The merge transfers 8 Transfer Units (TU-1..TU-8) covering tier classification, path overrides, verification roster widening, git pre-flight, TFEP baseline, TFEP prohibitions, mid-phase rf-qa escalation, and incident reporting, while preserving 5 load-bearing invariants (INV-01..INV-05) under 9 manifest exceptions (ME-1..ME-9) `[VALIDATION-SPEC-CITED][UNVERIFIED]`. The merge is sequenced as a 10-step commit chain with three named sequencing constraints (S-1..S-3) and is governed by 18 adversarial-validation acceptance criteria (AC-ATK-01..AC-ATK-18) plus 6 success-metric acceptance criteria (AC-SM-01..AC-SM-12, subset cited) `[VALIDATION-SPEC-CITED][UNVERIFIED]`.

Resumability of in-flight MDTM tasks is the highest-exposure surface. Validation spec § 9 line 285 capitalizes "HIGHEST EXPOSURE" on INV-04 `[VALIDATION-SPEC-CITED][UNVERIFIED]`. Live grep re-run on 2026-05-16 at fix-cycle 2 QA time (`rg -l "/sc:task|sc-task-protocol|task-unified" .dev/tasks/ | wc -l`) returns **132 union files** (canonical, all `.dev/tasks/` including this PRD's own subtree; supersedes the 130 figure that fix-cycle 1 recorded earlier the same day — population is dynamic; the earlier research-03 § 6 snapshot of 25 union files reflected a narrower subset and an earlier morning grep — all three numbers stand at their respective snapshot times) `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`. Against the validation-spec's 2026-05-15 snapshot of **96 union files**, live exposure has GROWN, not shrunk; the spec figure is divergent in direction as well as magnitude `[CODE-CONTRADICTED]`. The surviving named-exposure target `TASK-RESEARCH-20260403-sprint-task-exec` (status `🟠 Doing`) carries **48 `/sc:task|sc-task-protocol|task-unified` occurrences across 10 files** in research/synthesis/qa under that subtree (`rg -c` summed over the subtree on 2026-05-16) `[CODE-VERIFIED 2026-05-16]`. CR-FM-03 (compatibility shim defaulting absent `Tier:` to STANDARD) covers parse-level resumability; AC-ATK-18 (resume-time content grep with warn-and-continue disposition per ME-3) closes the semantic-level gap.

The merge converges with the 7 foundation rows under ME-6 atomicity (single-PR landing). Two anchor artifacts cited by the validation spec — `extension-point-contracts.md:11-17` (INV definitions) and `transfer-manifest.md § 4` (V/C/K verdicts byte-for-byte source) — were originally claimed absent from the working tree but are **PRESENT on disk** at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` per fix-cycle 2 verification 2026-05-16 `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; **content audit owed** to confirm artifact bodies match PRD claims (R-DOC-01 reframed). Every claim sourced solely to those anchors is tagged `[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]` throughout this PRD pending the content audit.

**Key Success Metrics:**
- INV-01..INV-05 survive the merged surface, demonstrated by a re-readable invariant-survival walkthrough (AC-SM-03) `[VALIDATION-SPEC-CITED][UNVERIFIED]`.
- All eight V/C/K verdicts (TU-1..TU-8) match the transfer manifest byte-for-byte (AC-SM-01) `[VALIDATION-SPEC-CITED][UNVERIFIED]`.
- CR-FM-04 ordering greps return three function names (`path_override_check`, `tier_field_validate`, `gate_1_dispatch`) in expected order against `src/superclaude/skills/task/SKILL.md` (AC-SM-07) `[VALIDATION-SPEC-CITED][UNVERIFIED]`.
- 100% of the live in-flight MDTM file population (132 files referencing donor surfaces as of 2026-05-16 live recount; population is dynamic and re-baselined at Step 5 pre-commit per S-1) resume cleanly under CR-FM-03 with warn-and-continue Gate-1.5 emission per AC-ATK-18 (no HALT; no silent semantic degradation undetected) — verified against the surviving named-exposure target `TASK-RESEARCH-20260403-sprint-task-exec` (48 occurrences across 10 files, 2026-05-16) `[CODE-VERIFIED 2026-05-16]`.

---

---

## 2. Problem Statement

### 2.1 The Core Problem

**Two task-execution skills coexist in the framework with overlapping but non-identical surfaces; the donor surface must be folded into the recipient without breaking in-flight resumability or the five load-bearing invariants.**

The recipient skill `src/superclaude/skills/task/SKILL.md` carries the canonical F1 execution loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT at `:79-98`), the F2 prohibition catalog (`:104-117`, 9 numbered prohibitions), and two rf-qa invocation points (Phase-Gate QA at `:191-198`; Post-Completion Validation at `:219-241`) `[CODE-VERIFIED]`. The donor skill `src/superclaude/skills/sc-task-protocol/SKILL.md` carries an MDTM frontmatter `Tier:` classifier (donor `:7-9`, `:49-58`), critical/trivial path overrides (donor `:121, 123`), a STRICT verification roster naming `quality-engineer` (donor `:80-91`, `:114-119`, `:277-279`), a git pre-flight (donor `:81`), and the contiguous Test Failure Escalation Protocol block at donor `:125-244` `[CODE-VERIFIED]`. Today, the `/sc:task` command file (`src/superclaude/commands/task.md:100`) invokes the donor skill `[CODE-VERIFIED]`. The merge stubifies `/sc:task` (CR-DEP-01), hard-deletes the donor skill (CR-DEP-03), retargets all callers to `/task` invoking the recipient skill, and folds donor content into the recipient via 8 named Transfer Units.

Affected: framework users who author and execute MDTM tasks via `/task` or `/sc:task`; in-flight task subtrees referencing donor surfaces (132 union files live on 2026-05-16 fix-cycle 2 QA recount per `rg -l "/sc:task|sc-task-protocol|task-unified" .dev/tasks/ | wc -l`; supersedes the 130 figure used elsewhere in this PRD which reflected the earlier fix-cycle 1 recount; supersedes the earlier 25-file research-03 narrower-scope snapshot; the surviving exposure target `TASK-RESEARCH-20260403-sprint-task-exec` carries 48 donor-surface occurrences across 10 files in subtree per fix-cycle 1 verification); the sprint executor pipeline that currently emits `/sc:task` from `src/superclaude/cli/sprint/process.py:170` (builder defined at `:124`) and from `src/superclaude/cli/cleanup_audit/prompts.py` at lines 26, 47, 69, 92, 116 `[CODE-VERIFIED 2026-05-16]`.

Impact of not solving: the donor surface persists as a parallel skill with overlapping semantics and divergent verification rosters; rf-qa floor (INV-03) is anchored at two points in the recipient and at zero points in the donor (donor TFEP escalates to `/sc:forensic`, not rf-qa) `[CODE-VERIFIED]`; ME-2 (rf-qa never replaced, never displaced) cannot be enforced uniformly; the framework continues to emit a deprecated surface from sprint and cleanup-audit pipelines; in-flight tasks referencing `/sc:task` continue to consume a skill whose intended successor (rf-qa-anchored, tier-classified, TFEP-equipped) is the recipient `/task`.

Barriers today: no `Tier:` frontmatter parser exists in the recipient `[CODE-VERIFIED]`; the canonical post-merge call ordering (`path_override_check` → `tier_field_validate` → `gate_1_dispatch`) is **not yet expressed in either donor or recipient SKILL.md** — neither file contains the literal strings `path_override_check`, `tier_field_validate`, `gate_1_dispatch`, or the CR-7 ORDERING sentinel `[CODE-VERIFIED]`; `.git/hooks/` contains only `*.sample` files (no active pre-commit / pre-push enforcement) `[CODE-VERIFIED]`; the rebase-split bypass (Scenario H-2) permits intermediate commits between Step 1 stubification and Step 6 donor-deletion to land where `/sc:task` is stubified but `sprint/process.py` and `cleanup_audit/prompts.py` still emit it `[CODE-VERIFIED]`.

### 2.2 Why This Feature is Required

The merge is the post-adversarial-validation closure of validation-spec.md, which converged a V1 steelman, a V2 attack chain, and a V3 security-probe pass into a 12-section spec (§§ 1–15) that names 8 TUs, 9 MEs, 5 INVs, 3 sequencing constraints, a 10-step commit sequence, 18 AC-ATK rows, and 12+ AC-SM rows, and explicitly concedes 5 residual risks in § 15 `[VALIDATION-SPEC-CITED][UNVERIFIED]`. The feature is critical to the framework for the following reasons:

| Driver | Evidence | INV / ME / Closure tie |
|---|---|---|
| **Tier classification must become a first-class frontmatter contract.** | Donor `commands/task.md:50-67` defines a TEXT-ONLY classification header schema with values `{STRICT, STANDARD, LIGHT, EXEMPT}`; donor `commands/task.md:69-91` provides priority-ordered keyword tables `[CODE-VERIFIED]`. Recipient `task/SKILL.md` carries no `Tier:` mention `[CODE-VERIFIED]`. | TU-1 closes via ADOPT verdict; INV-05 (refusal-of-definition) bound by ME-1 audit gate. |
| **Critical/trivial path override semantics must precede tier dispatch.** | Donor `sc-task-protocol/SKILL.md:121, 123` defines override paths (`auth/`, `security/`, `crypto/`, `models/`, `migrations/` → CRITICAL; `*.md`, `docs/`, `*test*.py` → skip) `[CODE-VERIFIED]`. Recipient mentions `auth/` zero times `[CODE-VERIFIED]`. Wrong-order risk: validation-spec § 10 Scenario A documents the `tier_field_validate(); path_override_check(); gate_1_dispatch()` bait `[VALIDATION-SPEC-CITED][UNVERIFIED]`. | TU-2 closes via ADOPT; F-02 sentinel + row-1 ordering grep; CR-7 ORDERING sentinel to be authored at Step 1. |
| **Verification roster must widen to `[rf-qa, quality-engineer]` without displacing rf-qa.** | Donor STRICT execution at `sc-task-protocol/SKILL.md:80-91, 114-119, 277-279` spawns `quality-engineer` only `[CODE-VERIFIED]`. Recipient phase-gate QA at `task/SKILL.md:191-198` spawns `rf-qa` only `[CODE-VERIFIED]`. Direct ADOPT would violate ME-2. | TU-3 closes via ADAPT verdict; ME-2 (rf-qa never replaced, never displaced) binds the widening. |
| **STRICT tier must capture a git working-tree pre-flight as warn-and-continue, not a HALT.** | Donor `sc-task-protocol/SKILL.md:81` is the single-line "Verify git working directory clean (git status)" pre-flight `[CODE-VERIFIED]`. Recipient F1 loop at `task/SKILL.md:79-98` has no git status step `[CODE-VERIFIED]`. New HALT semantics would violate INV-01. | TU-4 closes via ADAPT (re-frame as Task Log emission); ME-3 forbids new HALT; AC-ATK-02 binds 5-row matrix {clean, dirty, tool-absent, not-a-repo, error-other}. |
| **TFEP baseline must persist across session boundaries on disk.** | Donor `sc-task-protocol/SKILL.md:144-154` stores baseline in memory `[CODE-VERIFIED]`. In-memory baseline breaks INV-04 across resumption. Recipient creates `research/`, `synthesis/`, `qa/`, `reviews/` subfolders per `task/SKILL.md:205, 274` `[CODE-VERIFIED]` — the natural home for on-disk baseline YAML. | TU-5 closes via ADOPT adapted to on-disk YAML at `${TASK_DIR}/research/test-baseline.yaml`; INV-04 (resumability) bound. |
| **TFEP VIOLATION-level prohibitions must reinforce F2 additively.** | Donor `sc-task-protocol/SKILL.md:129-142` adds 3 prohibitions + 3 carve-outs `[CODE-VERIFIED]`. Recipient F2 catalog at `task/SKILL.md:104-117` has zero matches for "TFEP", "test failure", "Ad-hoc fixes" `[CODE-VERIFIED]`. | TU-6 closes via ADOPT; INV-02 (F2 catalog additive within existing semantic categories). |
| **TFEP escalation must route mid-phase to rf-qa (not `/sc:forensic`).** | Donor `sc-task-protocol/SKILL.md:170-218` escalates to `/sc:forensic` `[CODE-VERIFIED]`. Recipient has no mid-phase rf-qa invocation point `[CODE-VERIFIED]`. F-05 authorization is three-prong (existing identity + existing spawn pattern + named by TU-7) — but anchor `extension-point-contracts.md:11-17` was not amended `[VALIDATION-SPEC-CITED][UNVERIFIED]`. | TU-7 closes via ADOPT with F-05 three-prong defense; INV-03 surface widened from 2 to 3 invocation points (Concession 2 of § 15). |
| **TFEP incident reports must survive session boundaries as a side-effect file.** | Donor `sc-task-protocol/SKILL.md:220-236` defines `tfep-incident-report.md` with 7 visible fields (Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts) `[CODE-VERIFIED]`. Validation-spec § 5.8 calls it "seven-field schema" `[VALIDATION-SPEC-CITED][UNVERIFIED]` — donor count of 7 reconciles with spec count of 7; the prior research-notes "6 vs 7" ambiguity is resolved against the live donor file at `:227-233`. | TU-8 closes via ADOPT; INV-04 (resumability via parse-clean side-effect file); AC-ATK-12 binds enumeration. |
| **In-flight resumability must hold semantically, not just at parse-level.** | 132 live in-flight files (canonical live recount 2026-05-16, fix-cycle 1 re-grep across `.dev/tasks/`) carry no `Tier:` field and route through CR-FM-03 default to STANDARD `[CODE-VERIFIED 2026-05-16]`. The surviving named-exposure target `TASK-RESEARCH-20260403-sprint-task-exec` (status `🟠 Doing`) holds 48 donor-surface content references across 10 files in its subtree `[CODE-VERIFIED 2026-05-16]`. CR-FM-03 (parse-layer) cannot see content references. | INV-04 split into parse-level + semantic-level; AC-ATK-18 (resume-time grep) closes the semantic gap. |

### 2.3 Reference to Platform Context

This is a Feature PRD; market sizing and platform-level value proposition are out of scope per the FEATURE-PRD abbreviation discipline. The platform-level context for SuperClaude (the SuperClaude_Framework Python package per `src/superclaude/`) lives in the platform PRD and is referenced rather than restated here.

---

## 3. Background & Strategic Fit

### 3.1 Why Now?

The feature is required now because three adversarial-validation outputs are ready and a fourth (the validation-spec itself) names enablers and dependencies that are either present or explicitly bounded by Open Questions. Platform market trends and revenue projections are out of scope for this Feature PRD.

| # | Enabler / Trend | Status (2026-05-16) | Bound by |
|---|---|---|---|
| 1 | **Validation-spec § 1–15 converged.** V1 (steelman) + V2 (attack chain) + V3 (security-probe) merged into single spec with 8 TUs, 9 MEs, 5 INVs, 3 S-Ns, 18 AC-ATK, 12+ AC-SM | `[VALIDATION-SPEC-CITED][UNVERIFIED]` — spec body present at `.dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md`; named anchor artifacts (`extension-point-contracts.md`, `transfer-manifest.md`, etc.) present on disk; content audit owed per R-DOC-01 | This PRD's S13 Open Questions for anchor recovery; S20 Risk Analysis R-DOC-01 |
| 2 | **Recipient skill carries 2 of 3 required rf-qa invocation points.** Phase-Gate at `task/SKILL.md:191-198`; Post-Completion at `:219-241` `[CODE-VERIFIED]` | Two anchors live; third (TU-7 mid-phase escalation) is the new authoring at Step 4 | ME-2 (rf-qa never replaced); F-05 three-prong defense (Concession 2 of § 15) |
| 3 | **Donor command file `commands/task.md` already carries the tier classification schema.** Lines 50-67 (TEXT-ONLY classification header) and 69-91 (priority-ordered tier rules) `[CODE-VERIFIED]` | Tier vocabulary canonical: `{STRICT, STANDARD, LIGHT, EXEMPT}` per donor `commands/task.md:55, 61` and donor SKILL.md `:9, 56` `[CODE-VERIFIED]`. Validation-spec § 4 line 103 references 3-tier `{STRICT, STANDARD, TRIVIAL}` `[VALIDATION-SPEC-CITED][UNVERIFIED]` — surfaced as Open Question OQ-TIER-VOCABULARY | OQ-TIER-VOCABULARY in S13 |
| 4 | **In-flight exposure blast radius has grown vs the spec snapshot and remains dynamic.** Live count 132 union files across `.dev/tasks/` on 2026-05-16 (fix-cycle 1 re-grep) vs. validation-spec 96 — direction inverted from the earlier 25-file research-03 figure; spec figure now under-counts live exposure `[CODE-CONTRADICTED 2026-05-16]`. The surviving named-exposure target `TASK-RESEARCH-20260403-sprint-task-exec` (48 occurrences across 10 files) remains concrete and groundable for AC-ATK-18 testing `[CODE-VERIFIED 2026-05-16]` | Blast radius is dynamic; CR-DEP-06 residual-reference manifest required to enumerate the population at Step 5 pre-commit; backlog (61) + `docs/generated/` (83) residuals still in scope `[CODE-VERIFIED]` |

### 3.2 How This Fits Framework Objectives

- **Convergence with the 7 foundation rows.** ME-6 atomicity binds the merge to a single-PR landing such that intermediate states cannot fail their own pre-commit gates `[VALIDATION-SPEC-CITED][UNVERIFIED]`. Aligns with project convention `master ← integration ← feature/*` in CLAUDE.md `[CODE-VERIFIED]`.
- **Single source of truth for task-execution semantics.** Folding donor into recipient eliminates parallel skills; preserves the recipient's F1 + F2 + rf-qa architecture; transfers donor's tier classifier and TFEP into the recipient under invariant-preserving verdicts (ADOPT for TU-1/TU-2/TU-6/TU-7/TU-8; ADAPT for TU-3/TU-4/TU-5).
- **rf-qa as the structural floor.** Every roster widening is permitted only because ME-2 keeps rf-qa present. Mid-phase TU-7 invocation reuses the existing `task/SKILL.md:191-198` spawn pattern.

### 3.3 Strategic Bets

| # | Bet | Hypothesis being tested | Concession (§ 15) tied |
|---|---|---|---|
| 1 | **Markdown sentinel comments + CR-FM-04 grep enforce row-1 ordering.** | Combined parse-level grep + design-time review is sufficient to guarantee runtime call-site order without an AST-level check `[VALIDATION-SPEC-CITED][UNVERIFIED]` | Concession (none direct — AC-ATK-13 escalation if grep proves insufficient) |
| 2 | **CR-FM-03 default-to-STANDARD shim survives in-flight resumption without an authored sunset.** | 100% of the live in-flight population route through the shim (research-time 25-file figure was a narrower-scope snapshot; live canonical figure is 132 at 2026-05-16 fix-cycle 2 / 130 at fix-cycle 1); any future migration row will be authored before the shim's default behavior is dropped `[CODE-VERIFIED]` | Concession 5 indirect via INV-04 (F-07 chain is procedural); AC-ATK-12 binds sunset |
| 3 | **Over-escalating on missing/empty/malformed TFEP baseline does not flood rf-qa.** | rf-qa verifier capacity exceeds the expected escalation volume; no rate-limit / refusal threshold required `[VALIDATION-SPEC-CITED][UNVERIFIED]` | Concession 3 (F-04 over-escalation unbounded on load); no AC closes load axis |
| 4 | **Mid-phase rf-qa adjudication on in-flight state is a sound semantic extension.** | rf-qa designed to verify completed work generalizes to adjudicating in-flight escalations without invariant erosion `[VALIDATION-SPEC-CITED][UNVERIFIED]` | Concession 2 (F-05 widens INV-03 beyond canonical anchor); AC-ATK-11 closes via retroactive ME-10 or one-time carve-out |

---

## 4. Product Vision

**"A single `/task` skill that classifies, dispatches, verifies, and escalates MDTM task execution with rf-qa as the structural floor — INV-01..INV-05 preserved verbatim, the donor surface removed, and every in-flight task resuming cleanly under a content-aware compatibility shim."**

When the merge succeeds, the framework runs `/task` as the canonical task-execution invocation. The recipient skill at `src/superclaude/skills/task/SKILL.md` carries the tier classification frontmatter contract (TU-1), the path-override-first row-1 call ordering (TU-2 with CR-7 ORDERING sentinel), the widened verification roster `[rf-qa, quality-engineer]` (TU-3, ME-2 preserved), the warn-and-continue git pre-flight (TU-4, ME-3 honored), the on-disk TFEP baseline at `${TASK_DIR}/research/test-baseline.yaml` (TU-5, INV-04 bound), the TFEP VIOLATION-level prohibitions additively appended to the F2 catalog (TU-6, INV-02 honored), the mid-phase rf-qa escalation as the third invocation point (TU-7, F-05 authorized), and the `tfep-incident-report.md` side-effect file (TU-8, INV-04 parse-clean). The donor `src/superclaude/skills/sc-task-protocol/SKILL.md` is hard-deleted; the `/sc:task` command is stubified with a one-shot deprecation banner; `src/superclaude/cli/sprint/process.py:170` (builder defined at `:124`) and `src/superclaude/cli/cleanup_audit/prompts.py` (lines 26, 47, 69, 92, 116) emit `/task` instead of `/sc:task` `[CODE-VERIFIED 2026-05-16]`. CR-FM-03 defaults every existing in-flight TASK-* file's absent `Tier:` to STANDARD; AC-ATK-18 emits a Gate-1.5 warn-and-continue line on every resume that surfaces deprecated-surface content references. The live in-flight population of 132 union files referencing donor surfaces across `.dev/tasks/` (2026-05-16 fix-cycle 2 recount; supersedes the 25-file research-03 snapshot used in early drafts) resumes cleanly. The 7-foundation-row commit chain lands atomically under ME-6, and the rebase-split bypass is closed by AC-ATK-17 (server-side pre-push hook).

---

## 5. Business Context

> **Feature-PRD abbreviation:** Section 5 is abbreviated for Feature PRD. Full business context (market positioning, revenue, competitive landscape) lives in the **Platform PRD** for SuperClaude_Framework. This section captures only Feature-PRD-relevant business framing.

### 5.1 Business Drivers (Feature-Local)

| Driver | Tie to Feature | Reference |
|--------|----------------|-----------|
| **Single source of truth for task-execution semantics** — eliminate parallel `/sc:task` + `/task` skills | Folds donor into recipient atomically (ME-6); reduces framework maintenance surface | See S3 "How This Fits Framework Objectives" |
| **rf-qa as structural floor (uniform enforcement)** | Pre-merge: rf-qa floor (INV-03) enforced unevenly across donor + recipient; post-merge: single skill carries ME-2 binding | INV-03; F-05 three-prong defense for TU-7 |
| **Closure of post-adversarial-validation phase** | V1 steelman + V2 attack chain + V3 security-probe converged into validation-spec; this PRD is the closure-phase requirements document | validation-spec.md sections 1–15 |
| **In-flight resumability protection** | 132 live in-flight files; named target `TASK-RESEARCH-20260403-sprint-task-exec` carries 48 donor-surface references; INV-04 is the highest-exposure invariant | INV-04; AC-ATK-18 |

### 5.2 Platform-PRD Reference

For the broader product strategy, revenue assumptions, ecosystem positioning, and stakeholder map at the SuperClaude_Framework platform level, refer to the **Platform PRD** (TBD location; not yet published). This Feature PRD does **not** restate platform-level market sizing, TAM/SAM/SOM, or platform-wide competitive positioning per the FEATURE-PRD abbreviation discipline.

---

## 6. Jobs To Be Done (JTBD)

> Format: When [situation], I want to [motivation], so I can [expected outcome].

### 6.1 Primary Jobs

**Job 1: Classify a task before any skill body runs**

- **When**: I (the user or harness) invoke `/task <task-file-path>` against a pre-authored MDTM task file
- **I want to**: have the command emit a TEXT-ONLY classification header (TU-1) with `Tier:` ∈ `{STRICT, STANDARD, LIGHT, EXEMPT}` per the priority-ordered keyword rules in `commands/task.md:69-91` `[CODE-VERIFIED]`, with `path_override_check()` evaluated first at row 1, then `tier_field_validate()`, then `gate_1_dispatch()` (CR-7 ORDERING)
- **So I can**: route the task to the correct verification roster and audit set without re-classifying inside the skill body (INV-05 preserved; ME-1 audit gate enforces "tier-conditioned reads only")
- **Current alternatives**: The donor `/sc:task` command file at `src/superclaude/commands/task.md:50-67` already emits the classification header `[CODE-VERIFIED]`; the recipient `/task` does not
- **Pain with alternatives**: Two parallel commands with overlapping but non-identical classification surfaces; the recipient skill has no `Tier:` parser and no row-1 ordering grep; CR-7 ORDERING sentinel is **absent from both donor and recipient SKILL.md** `[CODE-VERIFIED]`

**Job 2: Verify completed work with rf-qa as the structural floor**

- **When**: I reach a phase gate, post-completion validation, or a TFEP escalation trigger during execution
- **I want to**: spawn rf-qa (always) plus `quality-engineer` (for STRICT only) via the existing `task/SKILL.md:191-198` spawn pattern `[CODE-VERIFIED]`, with rf-qa never replaced or displaced (ME-2)
- **So I can**: trust that every verification path passes through the rf-qa identity, that roster widenings (TU-3, TU-7) are additive not substitutive, and that the third invocation point (mid-phase TFEP per TU-7) reuses the same identity and spawn pattern (F-05 three-prong defense)
- **Current alternatives**: Today the recipient has only two rf-qa invocation points (`:191-198` and `:219-241`) `[CODE-VERIFIED]`; donor TFEP escalates to `/sc:forensic`, not rf-qa, at donor `:191-218` `[CODE-VERIFIED]`
- **Pain with alternatives**: Mid-phase escalation routes around rf-qa; INV-03 floor is at 2 invocation points where the merged design requires 3; ME-2 cannot be enforced uniformly across the donor surface

**Job 3: Resume an in-flight MDTM task post-merge without surprise**

- **When**: I (or a subagent) resume an existing in-flight MDTM task (e.g., `TASK-RESEARCH-20260403-sprint-task-exec`, status `🟠 Doing`, 48 donor-surface references across 10 files in its subtree `[CODE-VERIFIED 2026-05-16]`) after the merge has landed
- **I want to**: have CR-FM-03 default the absent `Tier:` to STANDARD (parse-level), have AC-ATK-18 emit a Gate-1.5 warn-and-continue Task Log line on every detected deprecated-surface content reference (semantic-level), and have all `related_docs:` paths verified by `find` with `gate-1.5: deleted-related-doc detected path=<path>` emission for any ENOENT (L3-level)
- **So I can**: keep INV-04 (resumability) honored at all three layers — L1 parse, L2 semantic, L3 execution — without any HALT (ME-3 forbids new HALT semantics in F1) and without silent semantic degradation
- **Current alternatives**: Today no Tier shim, no resume-time content grep, no `related_docs:` traversal exists `[CODE-VERIFIED]`. Resumption parses clean but post-CR-DEP-03 (donor hard-delete) a subagent acting on `/sc:task` content reference hits a stubified surface (silent degradation) or the deleted donor SKILL.md (FileNotFoundError → ⚪ Blocked transition; INV-01 holds by transition, INV-04 *technically* satisfied but meaningful resume path dead)
- **Pain with alternatives**: Highest-exposure invariant (§ 9 INV-04 row "HIGHEST EXPOSURE") `[VALIDATION-SPEC-CITED][UNVERIFIED]`. 132 live `.dev/tasks/` files at risk (2026-05-16 fix-cycle 2 recount; supersedes 130 fix-cycle 1 figure — population dynamic); 144 residual `/sc:task` occurrences outside the in-flight slice; the surviving named-exposure target alone (`TASK-RESEARCH-20260403-sprint-task-exec`) carries 48 donor-surface content references across 10 files

### 6.2 Related Jobs

| Job | Frequency | Importance | Satisfaction with Current Solutions |
|-----|-----------|------------|-------------------------------------|
| **Run TFEP baseline capture before implementation begins** (TU-5; on-disk YAML at `${TASK_DIR}/research/test-baseline.yaml`) | Once per STRICT/STANDARD task | Critical (INV-04 bound) | Low — donor stores in-memory only; breaks INV-04 across resumption |
| **Detect TFEP escalation triggers and route mid-phase to rf-qa** (TU-7; F-05 third invocation point) | Per failing-test event | High (INV-03 widened) | None — donor routes to `/sc:forensic`; recipient has no mid-phase route |
| **Emit `tfep-incident-report.md` side-effect file after each TFEP resolution** (TU-8) | Per TFEP resolution | High (INV-04 parse-clean) | None in recipient; donor has the schema |
| **Enforce 10-step commit sequence atomically under ME-6** | Once at merge landing | Critical (ME-6 + 7-foundation-row mutual-presupposition) | Low — `.git/hooks/` contains only `*.sample` files; no active pre-push enforcement `[CODE-VERIFIED]` |
| **Re-route sprint executor + cleanup-audit emitters from `/sc:task` to `/task`** (CR-DEP-04, AC-ATK-17 server-side pre-push) | Once at Step 5 | Critical (M1 atomicity) | None — both emitters are live as of 2026-05-16 |
| **Verify INV-01..INV-05 survival on the merged surface** (AC-SM-03 invariant-survival walkthrough) | Once at Step 7 | Critical | None — anchor artifact `invariant-survival-walkthrough.md` is present on disk; content audit owed per R-DOC-01 |



## 7. User Personas

### 7.1 Primary Persona: TBD — MDTM Task Author

| Attribute | Details |
|-----------|---------|
| **Role** | Engineer or PM authoring MDTM task files (`TASK-PRD-*`, `TASK-RESEARCH-*`, `TASK-RF-*`) under `.dev/tasks/to-do/` |
| **Demographics** | Mid-to-senior contributor; reads/writes Markdown + YAML frontmatter daily; familiar with `/sc:*` slash-command surfaces (`/sc:task`, `/sc:tasklist`, `/sc:roadmap`) |
| **Goals** | (a) Produce task files that the recipient skill (`task/SKILL.md`) consumes cleanly post-merge; (b) keep in-flight tasks resumable across the merge boundary; (c) avoid authoring content that breaks on Step 5 stubification or Step 6 hard-delete |
| **Pain Points** | (i) 132 in-flight tasks reference `/sc:task`, `sc-task-protocol`, or `task-unified` and must survive the merge (2026-05-16 fix-cycle 2 live recount; supersedes earlier 25-file research-03 snapshot); (ii) no `Tier:` field exists today, so every in-flight file resumes through the unauthored CR-FM-03 shim default; (iii) tier vocabulary drift (`TRIVIAL` in research-notes vs canonical `LIGHT` in `commands/task.md:55, 61, 82`) creates classification ambiguity |
| **Technical Proficiency** | High — comfortable with shell, git, YAML; routinely runs `grep -R` audits |
| **Authority** | Influences task scope and frontmatter conventions; does NOT own framework rollout decisions |
| **Success Metrics** | Authored task resumes post-merge under correct tier; zero `[CODE-CONTRADICTED]` tags raised against their citations; resume-time grep (AC-ATK-18) emits no `legacy-surface-reference` warnings on subsequent re-grep |

**Quote:** "I have a `🟠 Doing` task with 43 `/sc:task` mentions across 9 files in my research subtree — I need to know whether resuming it post-merge silently degrades or loudly warns me before I touch anything."

**A Day in Their Life:** Opens an in-flight task at `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/`, runs `grep -R /sc:task` to enumerate exposure, expects a `Tier:` field validation and a Gate 1.5 emission listing surface-reference warnings before any subagent spawns.

---

### 7.2 Primary Persona: TBD — Sprint Executor (`/task` Operator)

| Attribute | Details |
|-----------|---------|
| **Role** | Engineer or agent operator who invokes `/task <file>` (post-merge) or `/sc:task <file>` (pre-merge) and drives the F1 execution loop |
| **Demographics** | Daily user of the recipient skill (`task/SKILL.md`) F1 loop at `src/superclaude/skills/task/SKILL.md:79-98`; familiar with Phase-Gate QA (`:181-211`) and Post-Completion Validation (`:219-241`) |
| **Goals** | (a) Reach a green Phase-Gate QA and Post-Completion Validation across STRICT, STANDARD, LIGHT, and EXEMPT tiers; (b) keep F1 progress monotonic — no surprise HALTs on dirty git, missing baselines, or warn-and-continue surface references; (c) escalate test failures via TFEP rather than ad-hoc patches |
| **Pain Points** | (i) Today the recipient skill has NO `Tier:` field, NO Gate 1 dispatch, NO TFEP, NO baseline snapshot — every STRICT obligation is implicit; (ii) Phase-Gate QA spawns `rf-qa` only (`task/SKILL.md:191`); STRICT contexts need `quality-engineer` co-spawn without displacing rf-qa (ME-2); (iii) `git status` pre-flight failure modes (clean / dirty / tool-absent / not-a-repo / error-other) have no defined disposition table |
| **Technical Proficiency** | High — debugs subagent transcripts, reads QA reports at `${TASK_DIR}/reviews/qa-phase-[N]-report.md`, traces F1 step transitions |
| **Authority** | Owns runtime decisions inside a single task execution; does NOT own framework releases |
| **Success Metrics** | F1 loop completes without unauthorized HALTs; all three rf-qa invocation points (phase-gate, post-completion, mid-phase TFEP) fire under the right preconditions; TFEP escalation budget ladder (~5-8K → ~15-20K → FULL STOP) tracks correctly across retries |

**Quote:** "When `git status` returns exit 127 because `git` isn't installed in the CI image, I need to know it's a warn-and-continue, not a HALT — and the disposition table needs to say so explicitly."

**A Day in Their Life:** Invokes `/task .dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/...`; reads the Step 0 classification header; expects path-override-check FIRST, then tier-field-validate, then gate-1-dispatch (canonical CR-7 ORDERING); spawns rf-qa for Phase-Gate QA and `quality-engineer` for STRICT context.

---

### 7.3 Primary Persona: TBD — Framework Maintainer (Merge Driver)

| Attribute | Details |
|-----------|---------|
| **Role** | Engineer landing the `/sc:task → /task` directional merge across Steps 1-10 (donor body absorbed into recipient skill; donor surface stubified at Step 5; donor file hard-deleted at Step 6; CR-DEP-06 residual manifest emitted post-Step-6) |
| **Demographics** | Owns `src/superclaude/` source-of-truth files; runs `make sync-dev`, `make verify-sync`, the cleanup-audit CLI, and the sprint-runner CLI; reviews `.dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md` |
| **Goals** | (a) Land Steps 1-10 without violating INV-01..INV-05 or ME-1..ME-9; (b) close AC-ATK-01..18 and AC-SM-01..12 with auditable evidence; (c) reconcile spec-cited named targets against live ground truth (two of three are live; one is genuinely absent — research-03's "stale" framing was itself stale at synthesis time); (d) ship CR-DEP-05 (CLI fix-forward) and CR-DEP-06 (residual-reference manifest) at the right phase boundaries |
| **Pain Points** | (i) Of the spec-named in-flight targets, `TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250` are LIVE on disk per 2026-05-16 fix-cycle 1 verification (`find .dev/tasks -iname '*121039*'` and `'*121250*'` both return matches) `[CODE-VERIFIED 2026-05-16]`, while `TASK-RF-20260515-195758` is genuinely absent; `TASK-RF-20260403-tasklist-e2e` exists but has zero `/sc:task` refs; S-1 has unsatisfied preconditions on the live named targets PLUS the broader 132-file in-flight population referencing donor surfaces; (ii) the validation spec under-counts CLI emission sites by 5/6 — `cleanup_audit/prompts.py` emits `/sc:task` at lines 26, 47, 69, 92, 116 and is NOT named in spec § 7.2; (iii) no `flock` discipline in `Makefile`, no `.git/hooks/` active hooks, no `.github/workflows/` push-policy — every § 7 mitigation is a greenfield addition |
| **Technical Proficiency** | High — reads/writes Makefile, drafts pre-commit / pre-push CI policy, audits `[CODE-VERIFIED]` tags against pinned SHAs |
| **Authority** | Owns merge phasing decisions, sentinel-comment authoring (CR-7 ORDERING), and shim sunset binding (CR-FM-03 / CR-MIGR-FM-03) |
| **Success Metrics** | Steps 1-10 land in order with each AC-ATK / AC-SM row green; CR-DEP-06 manifest enumerates ≥144 residual occurrences across ≥40 files with per-bucket disposition; no transient broken master SHA (HZ-06 / HZ-07 closed via AC-ATK-17 server-side hook) |

**Quote:** "If a rebase-split lands a SHA where `/sc:task` is stubified in `task.md` but still emitted from `sprint/process.py` and `cleanup_audit/prompts.py`, every sprint run pinned to that SHA dies — I need a CI check that fails the push, not a pre-commit hook the operator can `--no-verify` around."

**A Day in Their Life:** Drafts the CR-7 ORDERING sentinel for `task/SKILL.md` row 1; runs `grep -E '/sc:task\b' src/superclaude/cli/{sprint,cleanup_audit}/` and confirms 6 true-positive emission sites; authors `.github/workflows/push-policy.yml` enforcing AC-ATK-17 on landing commits.

---

### 7.4 Secondary Persona: TBD — Downstream Task-Runner (Subagent Caller)

| Attribute | Details |
|-----------|---------|
| **Role** | Subagent or human operator consuming `.dev/tasks/` content as context — e.g., reading research/synthesis prose, traversing `related_docs:` frontmatter, spawning child subagents from checklist items |
| **Demographics** | Indirect consumer — does not author tasks but reads them; commonly spawned by the sprint runner (`src/superclaude/cli/sprint/process.py:170`) or cleanup-audit passes (`src/superclaude/cli/cleanup_audit/prompts.py:26..116`) |
| **Goals** | (a) Receive context that points only at live (non-stubified, non-deleted) artifacts; (b) get a one-shot acknowledgment-gate warning when a resumed task's content references a deprecated surface; (c) never silently hit FileNotFoundError on a `Read` of `sc-task-protocol/SKILL.md` post-Step-6 |
| **Pain Points** | (i) L1 schema-parse holds for all 132 in-flight files (2026-05-16 fix-cycle 2 live recount; 130 live at fix-cycle 1 — population dynamic) but L2 (semantic content) and L3 (execution / dispatch) do not — a subagent acting on a `synth-05-implementation-plan.md` line that says "spawn `/sc:task` for the deferred regenerator audit" silently degrades post-Step-5; (ii) `related_docs:` paths can ENOENT post-Step-6 with no pre-flight detection; (iii) the spec's H-4 literal-PRIMARY-ARTIFACT phrasing does not match live evidence — the actual exposure shape in `TASK-RESEARCH-20260403-sprint-task-exec` is surface-mention (48 occurrences across 10 files in subtree, 2026-05-16), not literal-path |
| **Technical Proficiency** | Variable — may be human reviewer or automated subagent; reliable on file paths and grep, less reliable on intent inference |
| **Authority** | None — observes and acts on task content as given |
| **Success Metrics** | Resume-time grep emits `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` for every match; `find`-traversal over `related_docs:` emits `gate-1.5: deleted-related-doc detected path=<path>` on ENOENT; no silent degradation |

**Quote:** "I was reading `synth-05-implementation-plan.md` and it told me to spawn `/sc:task` for a deferred audit — three months from now, post-Step-5, that's a no-op the operator will never see unless someone surfaces it on first resume."

---

### 7.5 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|--------------|----------------|
| **Casual reader of `docs/generated/` or `.dev/releases/backlog/`** | These surfaces carry 144+ residual `/sc:task` occurrences (CR-DEP-06 manifest scope). LEAVE-AS-IS dispositions are enumerated for audit, not migration — a casual reader is not the migration audience and the manifest is not addressed to them. |
| **Author of new `/sc:task` invocations post-Step-5** | After Step 5 stubification, the runtime surface is no-op or warn. New invocations are explicitly out-of-scope and must be CR-DEP-05 fix-forward (`/task` invocation) instead. |
| **Operator using `git rebase -i` to split Step 5 across multiple commits without server-side enforcement** | The H-2 scenario (AC-ATK-17) explicitly targets this workflow. Bypass via `git commit --no-verify` is the exact failure mode the closure obligation forbids — operators relying on per-developer hooks are not the audience; server-side CI is the structural barrier. |
| **External consumer expecting `TRIVIAL` as a tier value** | Canonical tier set is `{STRICT, STANDARD, LIGHT, EXEMPT}` per `commands/task.md:55, 61, 82`. `TRIVIAL` is a vestigial term not present in live code; consumers expecting it will fail validation. |

---

---

## 8. Value Proposition Canvas

> **Feature-PRD abbreviation:** Section 8 is abbreviated per FEATURE-PRD discipline. The platform-level Value Proposition Canvas (customer jobs, pains, gains; products, pain relievers, gain creators) lives in the **Platform PRD** for SuperClaude_Framework and is referenced rather than restated here.

### 8.1 Feature-Local Value Brief

| Aspect | Detail |
|--------|--------|
| **Customer Jobs** | Classify, dispatch, verify, and escalate MDTM task execution under a single canonical surface (`/task`) — see S6 JTBD |
| **Customer Pains** | Two parallel skills with divergent verification rosters; in-flight tasks at risk of silent semantic degradation; rebase-split bypass enables transient broken master SHA |
| **Customer Gains** | Single source of truth for task execution; rf-qa as the structural floor at all three invocation points; CR-FM-03 + AC-ATK-18 make resume warnings observable |
| **Products & Services** | Recipient `/task` skill with TU-1..TU-8 absorbed; stubified `/sc:task`; CR-DEP-06 residual-reference manifest |
| **Pain Relievers** | Tier classifier + row-1 ordering grep (TU-1/TU-2); on-disk TFEP baseline (TU-5); seven-field incident report (TU-8); resume-time grep + acknowledgment gate (AC-ATK-18) |
| **Gain Creators** | Atomic single-PR landing (ME-6); server-side push-policy hook (AC-ATK-17); `flock` discipline on `sync-dev` (AC-ATK-16) |

For the platform-level VPC, refer to the Platform PRD.

---

## 9. Competitive Analysis

> **N/A — Feature PRD.** Competitive analysis is out of scope for a Feature PRD because the directional merge is an internal framework consolidation, not a market-facing product comparison. The competitive landscape for SuperClaude_Framework at the platform level (vs. other agentic frameworks, vs. other slash-command/skill ecosystems) lives in the **Platform PRD** for SuperClaude_Framework.
>
> **Rationale:** This feature has no direct external competitor; it is a unification of two internal skills (`/sc:task` donor + `/task` recipient). No comparison matrix, no feature parity table, and no win-loss analysis applies at this scope. Per the FEATURE-PRD abbreviation discipline, this section is marked N/A and not populated.

---

## 10. Assumptions & Constraints

> Validation-spec § 15 names 5 residual-risk concessions where the steelman explicitly acknowledges the defense cannot fully cover the attacks. These are reflected verbatim as assumptions TA-1, TA-2, TA-3, BA-2, and TA-5 below, with traceability to the source line and the closure obligation (AC) where one exists `[VALIDATION-SPEC-CITED][UNVERIFIED]`.

### 10.1 Technical Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| TA-1 | **"Tier-conditioned read" boundary is conceptually thin but holds via ME-1 design-time review.** (§ 15 Concession 1, validation-spec.md:415) `[VALIDATION-SPEC-CITED][UNVERIFIED]` A sufficiently determined refactor could describe a forbidden per-item dispatch as a "read" if it routes through a wrapper. Defense relies on R-RULE-11 audit discipline at design-time — human-process, not structural. | INV-05 (refusal-of-definition) erodes; per-item marker becomes runtime classifier; F1 progress monotonicity (INV-01 via D09b indirect) degrades | AC-ATK-05 (closed enumeration of authorized per-item marker consumers; new consumers require new manifest exception); design-time review by ME-1 audit gate |
| TA-2 | **Third rf-qa invocation point (TU-7 / F-05) widens INV-03 surface beyond the canonical anchor language.** (§ 15 Concession 2, validation-spec.md:416) `[VALIDATION-SPEC-CITED][UNVERIFIED]` Anchor source `extension-point-contracts.md:11-17` was not amended to mention mid-phase routing; authorization lives in this plan, not in the anchor. **Anchor file itself is present on disk; content audit owed per R-DOC-01.** | Future reviewer applying strict-anchor-only discipline treats mid-phase invocation as out-of-scope; paragraph-level surface-widening precedent established procedurally lower-cost than authoring a manifest exception | AC-ATK-11 (F-05 either backed by retroactive ME-10 OR explicitly marked as one-time non-generalizing carve-out); Open Question for engineering lead in S13 |
| TA-3 | **F-04 over-escalation on missing/empty/malformed TFEP baseline is a load-volume bet on rf-qa.** (§ 15 Concession 3, validation-spec.md:417) `[VALIDATION-SPEC-CITED][UNVERIFIED]` Plan does not bound upper limit on this routing volume; rf-qa capacity > escalation volume is unaudited. | rf-qa verifier queue floods; classification=`new` for every failure under absent/empty/malformed baseline produces noisier escalation queue without throttling | § 12 F-04 closure tradeoff (line 375) explicitly notes "Plan notes 'possibly-noisier escalation queue' but does not specify when 'noisy' becomes a refusal trigger" — no AC closes the load axis; left as TBD operational metric |
| TA-4 | **CR-FM-03 default-to-STANDARD shim has no sunset binding today.** (Validation-spec § 4 line 104, exposure #3) `[VALIDATION-SPEC-CITED][UNVERIFIED]` 100% of live in-flight files route through the shim per research-03 § 5 (research-time 25-file figure was a narrower-scope snapshot; live canonical figure is 132 at 2026-05-16 fix-cycle 2 / 130 at fix-cycle 1 — population dynamic) `[CODE-VERIFIED]`. A future audit row dropping the default-fall-through bricks every TASK-* authored under the shim. | All live files (132 at fix-cycle 2; population dynamic) simultaneously transition from "resumable" to "input-invalid → HALT per AC-ATK-10" if sunset is dropped without migration row | AC-ATK-12 (bind CR-FM-03 shim lifetime; sunset audit row CR-AUDIT-FM-03-SUNSET); Open Question OQ-FM-03-SUNSET in S13 (recommended `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`) |
| TA-5 | **F-07 procedural authorization chain is "not a manifest binding."** (§ 15 Concession 5, validation-spec.md:419) `[VALIDATION-SPEC-CITED][UNVERIFIED]` A reviewer reading only the `transfer-manifest.md` (present on disk; content audit owed per R-DOC-01) would see only the deletion, not the F-07 authorization. | Future reviewer applying strict-manifest-only discipline could insist on retroactive amendment despite the chain being documented in this plan | AC-ATK-07 (rebind rf-qa as F-07 chain-integrity verifier, spawning at Step 6 pre-commit); chain remains procedural rather than declared in manifest |
| TA-6 | **CR-7 ORDERING sentinel is a markdown comment, not an executable enforcement.** (Validation-spec § 5.1, lines 116-120) `[VALIDATION-SPEC-CITED][UNVERIFIED]` CR-FM-04 grep checks for the comment string's presence, not for any operational effect. | If SKILL.md is auto-generated by any future tool, sentinel comments could be stripped without triggering grep (§ 12 second bullet); ordering remains procedural | AC-ATK-01 (replace F-02 alternation grep with line-range-pinned or AST-level check); AC-ATK-13 (either move CR-7/CR-8 ordering into executable artifact OR downgrade sentinel claim from "binding" to "informational") |
| TA-7 | **Tier vocabulary is `{STRICT, STANDARD, LIGHT, EXEMPT}` per live code, not 3-tier `{STRICT, STANDARD, TRIVIAL}` per validation-spec § 4 line 103.** Canonical per `commands/task.md:55, 61` and `sc-task-protocol/SKILL.md:9, 56` `[CODE-VERIFIED]`. `TRIVIAL` is not in live code; any spec instance is vestigial. | Tier classifier author at Step 1 codifies wrong enum set; CR-FM-01 canonicalization table mis-anchored | OQ-TIER-VOCABULARY in S13 for engineering-lead confirmation |

### 10.2 Business Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | The framework operates with a single canonical task-execution skill; parallel skills (donor + recipient) are a transient state | Donor surface persists as parallel skill indefinitely; rf-qa floor enforced unevenly | CR-DEP-03 hard-deletes donor SKILL.md at Step 6 under ME-9 audit gate |
| BA-2 | **S-1 mitigation hierarchy is recorded but not decided.** (§ 15 Concession 4, validation-spec.md:418) `[VALIDATION-SPEC-CITED][UNVERIFIED]` Source plan line 325 leaves the choice (a/b/c) "at Phase 7 execution time"; late-discovered infeasibility of (a) means (b) or (c) get chosen under time pressure. **Named precondition target `TASK-PRD-20260514-121039` EXISTS** on disk (created 2026-05-16 01:37 per `find .dev/tasks -iname '*121039*'`) `[CODE-VERIFIED 2026-05-16]`; companion `TASK-TDD-20260514-121250` also EXISTS `[CODE-VERIFIED 2026-05-16]`; `TASK-RF-20260515-195758` is genuinely absent (find returns zero matches) `[CODE-VERIFIED 2026-05-16]`. The spec citation is therefore PARTIALLY current — two of three named targets are live and have unsatisfied S-1 preconditions; only one is genuinely absent. Critically, the in-flight PRD population is dynamic: this PRD (`TASK-PRD-20260516-004625`) is itself a new in-flight task referencing donor surfaces; live recount returns 132 union files across `.dev/tasks/`, so the S-1 generalization must bind the broader population in addition to the named targets, not in place of them. | Time-pressured choice between (b) and (c) when 14d deadline fires across multiple live in-flight tasks; named targets are live with un-discharged S-1 obligations; new tasks (including this one) compound the population continuously | AC-ATK-08 (V3-enhanced S-1: `--max-wait` 14d default + auto-invoke option (b) + pinned git-SHA + CR-DEP-05 grep extension); recommended PRD framing: S-1 binds **both the named targets `TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250` (live) AND any other in-flight PRD/TDD task referencing donor surfaces** — supplement, not replace, the named-target list |
| BA-3 | The 10 donor-ceremony drops are correctly enumerated by ME-9 against the absent `transfer-manifest.md` `[VALIDATION-SPEC-CITED][UNVERIFIED]` | A future contributor re-introduces a donor-ceremony pattern without re-litigating its rejection | ME-9 audit gate at Step 5; CR-DEP-06 one-shot residual-reference manifest (AC-ATK-18 companion) |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | Users / harnesses invoke `/task` after stubification of `/sc:task` (CR-DEP-01); stub emits one-shot deprecation banner pointing to `/task` | Users continue invoking `/sc:task` despite stub; deprecation goes unnoticed | CR-DEP-01 stub body + one-shot banner; AC-SM-08 returns 7 zero-diff invocations |
| UA-2 | Users tolerate Gate-1.5 warn-and-continue Task Log emissions on resume of pre-merge in-flight tasks (AC-ATK-18); first-resume-only confirmation gate prevents fatigue | Operators dismiss Gate-1.5 warnings; semantic-level deprecated-surface references go unactioned | Resume-fatigue prevention via one-shot acknowledgment gate per research-03 § 3 closure-obligation table |
| UA-3 | Subagents reading research/synthesis prose containing `/sc:task` symbol references degrade gracefully (no HALT) and emit Gate-1.5 lines per ME-3 | Subagent silently spawns stubified `/sc:task` and proceeds with degraded semantics | AC-ATK-18 resume-time grep covers (a) task body, (b) synthesis/research/qa siblings, (c) `find`-traversal of `related_docs:` paths |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Technology** | All Python operations use UV per CLAUDE.md `[CODE-VERIFIED]`; never `python -m` or bare `pip` | Hook implementations, audit scripts (CR-FM-04 grep, AC-ATK-18 resume-time grep) MUST use `uv run` or be pure shell | Encode UV-only discipline in any new audit row |
| **Technology** | Source of truth is `src/superclaude/`; `.claude/` is dev copy synced via `make sync-dev` per CLAUDE.md `[CODE-VERIFIED]` | All TU authoring edits land in `src/superclaude/skills/task/SKILL.md`; `make sync-dev` runs before commit; `make verify-sync` runs as a step-level gate | Add `make verify-sync` check to Step 7 commit-gate suite |
| **Architecture** | F1 loop semantics (INV-01) forbid new HALT semantics in F1; blockers are logged and the loop advances per `task/SKILL.md:170-179` `[CODE-VERIFIED]` | TU-4 (git pre-flight) MUST be warn-and-continue, not HALT; AC-ATK-18 resume-time grep MUST be warn-and-continue, not HALT | ME-3 audit gate at Step 1 |
| **Architecture** | F2 prohibitions catalog (INV-02) is additive within existing semantic categories; no deletion or weakening per `task/SKILL.md:104-117` `[CODE-VERIFIED]` | TU-6 TFEP prohibitions appended; AC-ATK-11 generalization required for verifier-spawned / mid-phase rf-qa context disposition | Step 1 + Step 4 author additively; CR-FM-04 grep verifies catalog row count monotonic-increasing |
| **Architecture** | rf-qa floor (INV-03) requires rf-qa presence at all three invocation points; ME-2 forbids replacement or displacement | TU-3 widening to `[rf-qa, quality-engineer]` MUST keep rf-qa; TU-7 mid-phase routing MUST reuse rf-qa identity and `task/SKILL.md:191-198` spawn pattern | F-05 three-prong defense; AC-ATK-07 + AC-ATK-11 |
| **Resumability** | Every existing TASK-* file MUST parse and resume cleanly under the merged surface (INV-04) | CR-FM-03 shim covers parse-level; AC-ATK-18 covers semantic-level; baseline YAML (TU-5) + incident report (TU-8) survive session boundaries | 100% of the live 132-file in-flight population (2026-05-16 fix-cycle 1 recount) validated against the surviving named-exposure target (`TASK-RESEARCH-20260403-sprint-task-exec`, 48 occurrences across 10 files) |
| **Timeline** | ME-6 (M1 atomicity) binds the 7 foundation rows to a single-PR landing under `.pre-commit-config.yaml` enforcement; rebase-split bypass is open today (`.git/hooks/` contains only `*.sample` files) `[CODE-VERIFIED]` | Intermediate commits between Step 1 stubification and Step 6 hard-delete must not land where `sprint/process.py:169` or `cleanup_audit/prompts.py:{26,47,69,92,116}` still emit `/sc:task` `[CODE-VERIFIED]` | AC-ATK-17 server-side pre-push hook covering both emitters; CR-DEP-04 |
| **Documentation** | Anchor artifacts cited by validation-spec (`extension-point-contracts.md:11-17`, `transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `rejected-features-ledger.md`, `final-merge-plan.md`) — originally claimed absent — are **PRESENT** on disk at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` per fix-cycle 2 verification 2026-05-16 `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`. Content audit owed (does artifact body match PRD claims?). | AC-SM-01 (V/C/K byte-for-byte), AC-SM-03 (invariant-survival walkthrough), AC-SM-04 (Phase 7 artifact line ranges), AC-SM-05 (HZ-NN hazard pairing), AC-SM-06 (row-count / step-count), AC-SM-11 (rejected-ledger CR-IDs) — verification now possible against on-disk artifacts; content audit required before claims can be re-classified from `[UNVERIFIED]` to verified. | R-DOC-01 risk row in S20 (reclassified to content-audit-owed); follow-up audit plan in S13 Open Questions; PRD body still carries `[VALIDATION-SPEC-CITED][UNVERIFIED]` flag pending the audit. |
| **Resource** | F-NN ↔ TU-NN bijection is non-obvious; canonical mapping lives in absent `final-merge-plan.md` | Cross-references to F-01..F-08 in this PRD use the most defensible local-evidence reading per research-01 Gaps #1, #3, #6 | Open Question in S13 for engineering lead to confirm bijection from recovered `final-merge-plan.md` |

---

## 11. Dependencies

### 11.1 External Dependencies

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| **`git` binary on every executing host** | CLI tool | OS / packaging | Medium — TU-4 git pre-flight degrades to `tool-absent` row of AC-ATK-02 5-row matrix when `git` exits 127 `[VALIDATION-SPEC-CITED][UNVERIFIED]` | Graceful-skip per ME-3 (warn-continue); never HALT |
| **`uv` runtime for Python operations** | CLI tool | Astral / project pin | Low — required by CLAUDE.md `[CODE-VERIFIED]` for all Python ops (`uv run pytest`, audit scripts) | Already a hard project requirement; no contingency |
| **MDTM task files conforming to the YAML frontmatter contract** (`id`, `title`, `status`, `created_date` per `task/SKILL.md:65-73` `[CODE-VERIFIED]`; post-merge: optional `Tier:`) | Data format | Task authors | Low at parse-level (CR-FM-03 defaults absent `Tier:`); higher at semantic-level (content references to deprecated surfaces) | CR-FM-03 shim + AC-ATK-18 resume-time grep |

### 11.2 Internal Dependencies

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| **`src/superclaude/skills/task/SKILL.md`** (recipient skill, F1 + F2 + rf-qa anchors) | Skill source | Framework team | Live `[CODE-VERIFIED]`: F1 loop at `:79-98`; F2 prohibitions at `:104-117`; Phase-Gate rf-qa at `:191-198`; Post-Completion rf-qa at `:219-241`; Agent Spawning Conventions at `:290-299`; Session Resumption at `:269-282` | Edits land at Step 1 (TU-1/TU-2 frontmatter + row-1 ordering); Step 2 (TU-3 + TU-4); Step 3 (TU-5 + TU-6); Step 4 (TU-7 + TU-8) |
| **`src/superclaude/skills/sc-task-protocol/SKILL.md`** (donor skill, 365 lines) | Skill source | Framework team | Live `[CODE-VERIFIED]`: TU-1 contribution at `:7-9, 49-58`; TU-2 contribution at `:121, 123`; TU-3 contribution at `:80-91, 114-119, 277-279`; TU-4 contribution at `:81`; TU-5..TU-8 contiguous block at `:125-244` | Hard-deleted at Step 6 under CR-DEP-03 and ME-9 audit |
| **`src/superclaude/commands/task.md`** (donor `/sc:task` command file) | Command source | Framework team | Live `[CODE-VERIFIED]`: classification header at `:50-67`; tier rules at `:69-91`; skill invocation at `:100` (currently `> Skill sc:task-protocol`) | Stubified at Step 1 under CR-DEP-01; one-shot deprecation banner; flips to `/task` invocation per CR-DEP-01 |
| **`src/superclaude/cli/sprint/process.py:169`** (sprint executor `/sc:task` emitter) | Caller | Framework team | Live `[CODE-VERIFIED]` per research-02 Stale Documentation Found #7 | Re-routed to `/task` at Step 5 under CR-DEP-04; AC-ATK-17 server-side pre-push hook covers |
| **`src/superclaude/cli/cleanup_audit/prompts.py`** (cleanup-audit `/sc:task` emitter, 5 occurrences at lines 26, 47, 69, 92, 116) | Caller | Framework team | Live `[CODE-VERIFIED]` per research-02 Stale Documentation Found #7 | Re-routed to `/task` at Step 5; AC-ATK-17 server-side pre-push hook scope MUST extend to include this file |
| **`.pre-commit-config.yaml` + `.git/hooks/`** | Gate infrastructure | Framework team | `.pre-commit-config.yaml` present; `.git/hooks/` contains only `*.sample` files per research-02 ME-6 row `[CODE-VERIFIED]` — no active pre-commit / pre-push enforcement | AC-ATK-17 authors a server-side pre-push hook covering both sprint and cleanup-audit emitters before Step 7 lands |
| **`docs/generated/*`** (83 residual `/sc:task` occurrences across 20 files) | Generated docs | Pipeline output | Live `[CODE-VERIFIED]` per research-02 ME-9 row and research-03 § 1 | CR-DEP-06 one-shot residual-reference manifest (AC-ATK-18 companion) covers this surface |
| **`.dev/releases/backlog/` + archive** (61 residual `/sc:task` occurrences across 20 files) | Backlog docs | Framework team | Live `[CODE-VERIFIED]` per research-02 ME-9 row | CR-DEP-06 |
| **`.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/`** (surviving in-flight H-4 exposure target, 48 donor-surface occurrences across 10 files in subtree, status `🟠 Doing`) | In-flight task subtree | Task owner | Live `[CODE-VERIFIED 2026-05-16]` per fix-cycle 1 re-grep (`rg -c "/sc:task|sc-task-protocol|task-unified" <subtree>`); supersedes research-03 § 4 stale count | AC-ATK-18 resume-time grep; first-resume-only acknowledgment gate |

### 11.3 Cross-Team Dependencies

| Team | Dependency | What We Need | When Needed | Status |
|------|------------|--------------|-------------|--------|
| Engineering Lead | OQ-FM-03-SUNSET decision (CR-FM-03 shim sunset binding `N`) | Confirmation of `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored` (recommendation from research-03 § 5) or alternative | Before Step 1 (CR-FM-03 authored) | TBD |
| Engineering Lead | OQ-TIER-VOCABULARY (3-tier vs 4-tier reconciliation) | Confirmation that canonical post-merge tier set is `{STRICT, STANDARD, LIGHT, EXEMPT}` per live code (research-01 Gap #6, research-02 Question #1) | Before Step 1 | TBD |
| Engineering Lead | OQ-F-NN-BIJECTION (F-NN ↔ TU-NN mapping) | Confirmation of canonical pairings (research-01 Gaps #1, #3) once `final-merge-plan.md` is recovered | Before Step 7 (AC-SM-04 Phase 7 artifact line ranges) | TBD |
| Engineering Lead | OQ-TFEP-FIELD-COUNT (TU-8 incident report 6 vs 7 fields) | Confirmation of canonical field enumeration (research-01 Gap #2) | Before Step 4 (TU-8 authoring) | TBD |
| Engineering Lead | OQ-F-05-MANIFESTIZATION (retroactive ME-10 vs one-time carve-out) | Decision per AC-ATK-11 (research-02 Question #2) | Before Step 4 (TU-7 / mid-phase rf-qa) | TBD |
| Engineering Lead | OQ-PROHIBITION-DISPOSITION-MATRIX (verifier-spawned F1 disposition) | Decision per AC-ATK-11 generalization (research-02 Question #4) | Before Step 3 (TU-6 prohibitions) | TBD |
| Documentation / Release Owner | Content audit of cited anchor artifacts (R-DOC-01 reframed) | Confirm on-disk content of all seven artifacts present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` (`extension-point-contracts.md`, `transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `rejected-features-ledger.md`, `final-merge-plan.md`) matches PRD claims; surface any drift as per-row R-DRIFT-NN findings | Before Step 7 invariant-survival walkthrough | TBD |
| rf-qa Owner | Acceptance of third invocation point (TU-7) and load implications of F-04 over-escalation (Concession 3) | Confirmation that rf-qa capacity exceeds expected mid-phase escalation volume; no rate-limit required | Before Step 4 | TBD |

---

## 12. Scope Definition

### 12.1 In Scope (Phase 1 / Merge MVP)

| Category | Included | Notes |
|----------|----------|-------|
| **8 Transfer Units (TU-1..TU-8)** | TU-1 `Tier:` field + Gate 1 + per-item marker (ADOPT); TU-2 Critical/Trivial Path Override + CR-7 ORDERING (ADOPT); TU-3 Gate 2 Verification roster widening to `[rf-qa, quality-engineer]` (ADAPT, ME-2 preserved); TU-4 D15b Layer 2 git pre-flight as warn-and-continue (ADAPT, ME-3 honored); TU-5 TFEP baseline snapshot on disk at `${TASK_DIR}/research/test-baseline.yaml` (ADOPT adapted); TU-6 TFEP Prohibitions + Carve-outs additive to F2 (ADOPT); TU-7 TFEP Escalation trigger as 3rd rf-qa invocation point (ADOPT, F-05 authorized); TU-8 TFEP Incident reporting `tfep-incident-report.md` side-effect file (ADOPT) | Each TU has V/C/K verdict per validation-spec § 2 lines 49-56 `[VALIDATION-SPEC-CITED][UNVERIFIED]`; INV(s) protected and alternative-that-would-weaken-INV documented in research-01 |
| **9 Manifest Exceptions (ME-1..ME-9)** | ME-1 per-item dispatch forbidden (load-bearing for INV-05); ME-2 rf-qa never replaced/displaced (load-bearing for INV-03); ME-3 no new HALT semantics in F1 (load-bearing for INV-01); ME-4..5/7/8 held without per-row deltas (ancillary, referenced for fence); ME-6 M1 atomicity (load-bearing for 7-foundation-row commit shape); ME-9 donor-ceremony drop audit (load-bearing for R-RULE-11 boundary) | Five load-bearing (1, 2, 3, 6, 9); four ancillary (4, 5, 7, 8) per research-02 Section A summary. Ancillary set is referenced as fence; no per-row deltas authored |
| **5 Load-bearing Invariants (INV-01..INV-05)** | INV-01 F1 loop semantics (progress monotonicity); INV-02 Prohibited-actions F2 (additive within existing catalog); INV-03 Phase-gate rf-qa (never replaced, never displaced); INV-04 Resumability (highest exposure per § 9 line 285); INV-05 Refusal-of-definition (`Tier:` is metadata, not work-definition) | INV-04 carries the highest DoD weight; split into FR-INV-04-PARSE (CR-FM-03 shim) and FR-INV-04-SEMANTIC (AC-ATK-18 resume-time grep) per research-03 § 3 |
| **3 Sequencing Constraints (S-1, S-2, S-3)** | S-1: the spec-named targets `TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250` (both live on disk per fix-cycle 1 verification) AND any other in-flight PRD/TDD task referencing donor surfaces must complete before Step 5 (generalized to cover the live in-flight population of 132 union files referencing donor surfaces; `TASK-RF-20260515-195758` is genuinely absent); S-2: sprint executor + cleanup-audit emitters re-routed before Step 6 hard-delete; S-3: 7-foundation-row mutual-presupposition (ME-6 atomicity) | S-1 generalization supplements the named targets — does not replace them. Per fix-cycle 1 (2026-05-16): named targets 121039/121250 live `[CODE-VERIFIED]`; broader population at 132 union files `[CODE-VERIFIED]`; AC-ATK-08 `--max-wait` 14d default + auto-invoke option (b) + pinned git-SHA |
| **10-step commit sequence** | Step 1 (CR-FM-03 shim + TU-1 + TU-2 + CR-7 ORDERING sentinel); Step 2 (TU-3 + TU-4 + AC-ATK-02 5-row matrix); Step 3 (TU-5 + TU-6); Step 4 (TU-7 + TU-8 + AC-ATK-11 disposition); Step 5 (CR-DEP-04 caller re-routing — sprint/process.py:169 + cleanup_audit/prompts.py); Step 6 (CR-DEP-01 stubify `/sc:task` + CR-DEP-03 hard-delete donor SKILL.md + ME-9 audit); Step 7 (AC-SM-03 invariant-survival walkthrough + AC-SM-04 Phase 7 artifact line ranges); Step 8 (AC-ATK-17 server-side pre-push hook covering both emitters); Step 9 (CR-DEP-06 residual-reference manifest); Step 10 (AC-SM-01..12 conformance audits) | Step ordering is the canonical 10-step commit sequence inferable from validation-spec § 6 / § 8 sections per the absent `merge-master.md § 1` `[VALIDATION-SPEC-CITED][UNVERIFIED]`. ME-6 binds atomicity across the 7 foundation rows of this sequence |
| **18 AC-ATK closure obligations** | AC-ATK-01 (line-range-pinned or AST-level ordering check); AC-ATK-02 (5-row git_status matrix); AC-ATK-03 (baseline trinary → 4 states); AC-ATK-05 (closed enumeration of per-item marker consumers); AC-ATK-07 (rebind rf-qa as F-07 chain-integrity verifier); AC-ATK-08 (V3-enhanced S-1 with 14d deadline); AC-ATK-10 (unified pre-loop HALT policy table); AC-ATK-11 (F-05 retroactive ME-10 OR one-time carve-out); AC-ATK-12 (CR-FM-03 sunset + 7-field enumeration + CR-FM-01 canonicalization); AC-ATK-13 (CR-7/CR-8 ordering executable artifact OR downgrade sentinel); AC-ATK-17 (server-side pre-push hook covering sprint + cleanup-audit); AC-ATK-18 (resume-time content grep + Gate-1.5 emission + first-resume acknowledgment) + AC-ATK-04, 06, 09, 14, 15, 16 from validation-spec § 11.1 `[VALIDATION-SPEC-CITED][UNVERIFIED]` | Per research-02 Summary: AC-ATK-05, 07, 11, 12, 18 + CR-DEP-06 are the closure obligations the PRD must surface in S13 and S21 |
| **6 AC-SM success-metric closures (subset cited)** | AC-SM-01 (V/C/K table byte-for-byte conformance); AC-SM-02 (ME-1..ME-9 traceability); AC-SM-03 (invariant-survival walkthrough); AC-SM-04 (Phase 7 artifact line ranges); AC-SM-07 (CR-FM-04 ordering greps return three function names in expected order against `[src] skills/task/SKILL.md`); AC-SM-08 (CR-TASK-12 returns 7 zero-diff invocations: 6 donor strings + 1 sentinel-comment block) | Full set is AC-SM-01..12 per validation-spec § 11 `[VALIDATION-SPEC-CITED][UNVERIFIED]`; six are explicitly cited in research-01 + research-02 |
| **18+6 closure gap closure** | The 18 AC-ATK + 6 AC-SM (cited subset) above form the closure-gap audit envelope. CR-DEP-06 (residual-reference manifest) is the operational companion to ME-9 / AC-ATK-18 per research-02 ME-9 row | All gaps tracked in S13 Open Questions; resolution required before AC-SM-03 invariant-survival walkthrough lands at Step 7 |

### 12.2 Out of Scope (Phase 1 / Merge MVP)

| Item | Reason | Target Phase |
|------|--------|--------------|
| ❌ **10 donor-ceremony drops** | Named in absent `transfer-manifest.md` per research-02 ME-9 row `[VALIDATION-SPEC-CITED][UNVERIFIED]`. Drops remain dropped; ME-9 is the audit hook at the Step 5 commit. The 10 patterns are not re-introduced and not re-litigated within this merge. | Permanently out (re-introduction requires a new manifest exception) |
| ❌ **ME-4 ancillary donor patterns (HELD without per-row deltas)** | Ancillary per research-02 Section A summary; not attached to any F-01..F-08 finding. Fenced by ME-4 against re-opening. Specific patterns require content audit against on-disk `transfer-manifest.md § 4` (artifact present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/`; content audit owed per reframed R-DOC-01) `[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]` | Future merge (only if a new V/C/K verdict adopts the pattern) |
| ❌ **ME-5 ancillary donor patterns (HELD without per-row deltas)** | Same as ME-4 — ancillary, fenced against re-opening; source artifact present on disk, content audit owed | Future merge |
| ❌ **ME-7 ancillary donor patterns (HELD without per-row deltas)** | Same as ME-4 / ME-5 | Future merge |
| ❌ **ME-8 ancillary donor patterns (HELD without per-row deltas)** | Same as ME-4 / ME-5 / ME-7 | Future merge |
| ❌ **Embedded runtime classifier replacing per-item marker design** | D09b REJECTed at validation-spec source line 87 / 206 `[VALIDATION-SPEC-CITED][UNVERIFIED]`; weakens INV-05 by turning the per-item marker into a runtime dispatcher per research-01 TU-1 row | Permanently out |
| ❌ **In-task remediation block in lieu of `tfep-incident-report.md` side-effect file** | Breaks INV-04 (mutates task body) per research-01 TU-8 row | Permanently out |
| ❌ **HALT-as-gate disposition for git pre-flight (Reading B)** | Authors new HALT semantic that INV-01 forbids per ME-3; rejected in favor of warn-and-continue (Reading A) per research-01 TU-4 row | Permanently out |
| ❌ **New gate for TFEP escalation (D25)** | REJECTed; forces new gate vs reusing rf-qa identity per research-01 TU-7 row | Permanently out |
| ❌ **Throttling / rate-limit / refusal threshold for F-04 over-escalation on rf-qa** | § 12 F-04 closure tradeoff line 375 explicitly notes "Plan notes 'possibly-noisier escalation queue' but does not specify when 'noisy' becomes a refusal trigger" `[VALIDATION-SPEC-CITED][UNVERIFIED]`. Load axis is unbounded by design (Concession 3) | Future operational tuning (post-merge) |
| ❌ **Restoration / amendment of `extension-point-contracts.md:11-17`** to mention mid-phase rf-qa routing | Anchor source not amended per Concession 2; F-05 authorization lives in plan, not in anchor `[VALIDATION-SPEC-CITED][UNVERIFIED]` | Future if AC-ATK-11 selects retroactive ME-10 path |
| ❌ **Content audit of cited anchor artifacts (R-DOC-01 reframed)** within this merge | The 7 cited artifacts (`extension-point-contracts.md`, `transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `rejected-features-ledger.md`, `final-merge-plan.md`) are PRESENT on disk at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; the content audit cross-checking PRD claims against artifact bodies is a documentation dependency, not implementation work | Pre-Step-7 — content audit owned by Documentation / Release Owner per S11 cross-team table |

### 12.3 Permanently Out of Scope

| Item | Reason |
|------|--------|
| ❌ **Re-introduction of `/sc:task` as a non-stubified command** | Stubification (CR-DEP-01) is the merge's deprecation surface; re-instating the full command would require a new framework decision and would invalidate ME-9 |
| ❌ **Donor `sc-task-protocol/SKILL.md` as a parallel live skill** | Hard-deleted under CR-DEP-03 at Step 6; ME-9 audit gate documents the deletion; re-introduction requires a new directional merge proposal |
| ❌ **Tier vocabulary `TRIVIAL`** | Not in live code; canonical set is `{STRICT, STANDARD, LIGHT, EXEMPT}` per `commands/task.md:55, 61` and donor SKILL.md `:9, 56` `[CODE-VERIFIED]`. Validation-spec § 4 line 103 reference is vestigial |
| ❌ **Per-item marker as runtime dispatcher (any form)** | INV-05 + ME-1 forbid; D09b REJECTed; closure obligation AC-ATK-05 binds future contributors via closed enumeration |

---

## 13. Open Questions

> Per template: question tracking table. Owner=TBD, Status=Open, Resolution=TBD for all
> items below pending engineering-lead disposition. Status legend retained from template
> (🔴 Urgent / 🟡 Researching / 🟢 Resolved); all entries currently `🔴 Open`.

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| 1 | **Tier vocabulary reconciliation.** Spec § 4 line 103 uses a 3-tier set `{STRICT, STANDARD, TRIVIAL}` ("Default-STANDARD strips implicit STRICT"); live code in `src/superclaude/commands/task.md:50-67` and `src/superclaude/skills/sc-task-protocol/SKILL.md:9` uses a 4-tier set `{STRICT, STANDARD, LIGHT, EXEMPT}`. Canonical post-merge set = **code (4-tier)**. Confirm with engineering lead. INV-05 protection scope and ME-1 audit-gate enumeration depend on this. (Cross-ref research-02 § B INV-05 evidence; research-02 Stale Documentation Found #5.) | TBD | TBD | 🔴 Open | TBD |
| 2 | **AC-SM-01, AC-SM-03, AC-SM-05, AC-SM-06, AC-SM-11 — content audit required (re-evaluated 2026-05-16 fix-cycle 2).** The originally-claimed absence of the anchor files (`transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `extension-point-contracts.md`, `invariant-survival-walkthrough.md`) was a stale claim — all five files DO EXIST at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` per QA fix-cycle 2 verification 2026-05-16. The directory was reported as "does not exist" in earlier research, but at PRD-validation time it contains all named artifacts plus more (`rejected-features-ledger.md`, `final-merge-plan.md`, `donor-feature-catalog.md`, etc.). What remains owed: a CONTENT AUDIT comparing PRD claims against artifact bodies (byte-for-byte for AC-SM-01; structural conformance for AC-SM-03, -05, -06, -11). Decide: schedule content audit pre-Step-7 (recommended) vs defer to post-Phase-7.5. (Cross-ref research-02 Gap #1–#3; research-06 § 2 EC-03 + EC-04 artifact-block; superseded portion: "directory does not exist" claim.) | TBD | TBD | 🔴 Open | TBD |
| 3 | **S-1 named-target population update.** Spec § 3 line 86 names `TASK-PRD-20260514-121039` as the S-1 precondition target with 149+ `/sc:task` refs. **Fix-cycle 1 verification 2026-05-16:** the named target `TASK-PRD-20260514-121039` EXISTS on disk (created 2026-05-16 01:37; `find .dev/tasks -iname '*121039*'` returns a match) `[CODE-VERIFIED 2026-05-16]`; companion `TASK-TDD-20260514-121250` ALSO exists `[CODE-VERIFIED 2026-05-16]`; only `TASK-RF-20260515-195758` is genuinely absent. The earlier research-04 § 1.1 "task does not exist" assertion was a research-time snapshot that became stale at synthesis time. Generalization adopted in this PRD: **"the live spec-named targets AND any other in-flight PRD/TDD task referencing donor surfaces (`/sc:task`, `sc-task-protocol/`) must complete before Step 5, OR be explicitly snapshot-frozen with a decision record"** — supplement, not replace. Live in-flight population is 132 union files across `.dev/tasks/` (2026-05-16 fix-cycle 1 recount). Confirm the supplement-not-replace framing is acceptable. (Cross-ref research-04 § 1.1, § 1.4 [research-time, now superseded]; fix-cycle 1 verification 2026-05-16.) | TBD | TBD | 🔴 Open | TBD |
| 4 | **CR-DEP-06 elevation from "proposal" to "required for closure."** Validation-spec § 8 frames CR-DEP-06 as a proposal; live evidence (research-notes DIVERGENCE_FLAGS authority) confirms **144 residual `/sc:task` occurrences outside CR-DEP-05 scope** (61 in `.dev/releases/backlog/` + archive across 20 files; 83 in `docs/generated/` across 20 files); live recount on 2026-05-16 shows drift to 153 across 45 files. Confirm 144 residual scope (61 backlog + 83 docs/generated) is accepted as the binding count for the CR-DEP-06 manifest, and confirm CR-DEP-06 elevation to **REQUIRED**. (Cross-ref research-04 § 5; research-02 ME-9 evidence.) | TBD | TBD | 🔴 Open | TBD |
| 5 | **Companion TDD offer at delivery.** Engineering audience (multiple invariants, manifest exceptions, atomic commit sequence, five-row HALT matrix, server-side hook semantics, `flock` discipline) strongly recommends a companion Technical Design Document accompanying this PRD. Confirm whether engineering lead wants a TDD authored next, or whether the PRD's S14/S15/S21 sections suffice. | TBD | TBD | 🔴 Open | TBD |

---

---

## 14. Technical Requirements

This section contains the full Functional Requirements (FR) catalog and the Non-Functional Requirements (NFR) catalog for the directional merge. Functional rows (FR-TU-NN, FR-CS-NN, FR-CR-DEP-06) enumerate the eight Transfer Units (TU-1..TU-8) and the ten-step canonical commit sequence (CS-1..CS-10). Non-functional rows (NFR-INV-NN, NFR-ME-NN, NFR-S-NN) bind the five load-bearing invariants, nine manifest exceptions, and three sequencing constraints. Every row carries an MoSCoW priority and traces to at least one validation-spec or research citation.

### 14.1 Functional Requirements — Transfer Units (FR-TU-1..FR-TU-8)

One FR per Transfer Unit. Each row cites the recipient target `file:line`, the donor source `file:line`, the V/C/K verdict from validation-spec § 2, and the paired AC-ATK / AC-SM rows from § 11.

| FR ID | Title | Description | Priority (MoSCoW) | Acceptance Criteria mapping | Source citation |
|---|---|---|---|---|---|
| **FR-TU-1** | Frontmatter `Tier:` field + Gate 1 dispatch + per-item marker | Introduce frontmatter `Tier:` field on MDTM task files with values `{STRICT, STANDARD, LIGHT, EXEMPT}`; author Gate 1 dispatch step in recipient `task/SKILL.md` that reads `Tier:` BEFORE F1 loop entry; permit per-item `(Tier: X)` marker for tier-conditioned reads. Classification performed by `/sc:task` command file as TEXT-ONLY first output (HTML-comment header schema). V/C/K = **ADOPT** (§ 2 line 49). Closure pairs with F-01 (per-item marker as ME-1-bound tier-conditioned read). | Must | AC-ATK-05 (closed enumeration of authorized per-item marker consumers; current = `{CR-TASK-07 baseline-skip}`); AC-SM-01 (V/C/K row matches `transfer-manifest.md` § 4 byte-for-byte) `[CONTENT-AUDIT-OWED]` | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:7-9, 49-58` `[CODE-VERIFIED]`; `src/superclaude/commands/task.md:50-67, 69-91` `[CODE-VERIFIED]`. Recipient target: `src/superclaude/skills/task/SKILL.md` frontmatter (currently `:1-4` lists only `name`/`description` `[CODE-VERIFIED]`) + new Gate-1 dispatch section before F1 loop `:79-98` `[CODE-VERIFIED]`. Spec: § 2 line 49; § 5.3 lines 130–134; § 11.1 line 334. |
| **FR-TU-2** | Critical / Trivial Path Override at row 1 (CR-7 ORDERING) | Author "row 1" section in `task/SKILL.md` placing `path_override_check()` FIRST, then `tier_field_validate()`, then `gate_1_dispatch()`. Critical override (paths matching `auth/`, `security/`, `crypto/`, `models/`, `migrations/`) elevates to STRICT regardless of classified tier; Trivial override (`*.md`, `docs/`, `*test*.py`) permits skip. Author CR-7 ORDERING sentinel comment (confirmed **absent in both donor and recipient SKILL.md** as of 2026-05-16). V/C/K = **ADOPT** (§ 2 line 50). Closure pairs with F-02 (row-1 ordering grep). | Must | AC-ATK-01 (replace alternation grep with AST-level / line-range-pinned check); AC-ATK-13 (move sentinel into executable artifact OR downgrade to informational); AC-SM-07 (CR-FM-04 ordering grep returns three function names in expected order) `[CONTENT-AUDIT-OWED cascading]`; AC-SM-08 (CR-TASK-12 returns 7 zero-diff invocations) | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:121, 123` `[CODE-VERIFIED]`. Recipient target: `src/superclaude/skills/task/SKILL.md` (no analog today — zero matches for `auth/` in body `[CODE-VERIFIED]`). Sentinel absent in both files `[CODE-VERIFIED]`. Spec: § 2 line 50; § 5.1 lines 116–120; § 10 Scenario A line 296; § 11.1 lines 330, 342. |
| **FR-TU-3** | Gate 2 verification roster widening to `[rf-qa, quality-engineer]` | Widen STRICT-tier verification agent roster from rf-qa-only to `[rf-qa, quality-engineer]`. quality-engineer is **added to**, never replaces, rf-qa (ME-2 binding). Update Phase-Gate QA at `task/SKILL.md:181-211` and Agent Spawning Conventions at `:290-299`. V/C/K = **ADAPT** (§ 2 line 51) — synthesizes donor (quality-engineer) + recipient (rf-qa). Closure pairs with F-03-roster (Gate 2 widening; F-NN bijection ambiguous per R-DOC-01 — see catalog 01 Gaps #1, #3). | Must | AC-ATK-11 (F-05 retroactive ME-10 or non-generalization annotation — bounds precedent surface that this FR widens); AC-SM-02 (ME-2 traceability to CR-row) | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:80-91, 114-119, 277-279` `[CODE-VERIFIED]`. Recipient: `src/superclaude/skills/task/SKILL.md:181-211` (currently spawns `rf-qa` only at `:191`) `[CODE-VERIFIED]`; `:290-299` lists `rf-qa` at `:294`, omits `quality-engineer` `[CODE-VERIFIED]`. Spec: § 2 line 51; § 9 INV-03 row line 284; § 15 residual #2 line 416. |
| **FR-TU-4** | D15b Layer 2 pre-flight `git status` (warn-and-continue) | Author pre-loop pre-flight step that runs `git status` at STRICT entry and emits a Task Log line per AC-ATK-02 five-state matrix `{clean, dirty, tool-absent, not-a-repo, error-other}` with disposition `{WARN-CONTINUE, GRACEFUL-SKIP}` — **no HALT** (preserves INV-01 / ME-3). V/C/K = **ADAPT** (§ 2 line 52) — re-framed from gate to Task Log emission. Closure pairs with F-03 (dirty-tree warn-and-continue). | Must | AC-ATK-02 (five-row exit-code matrix bound to CR-TASK-06); AC-ATK-10 (unified pre-loop HALT policy: input-invalid vs environment-non-ideal); AC-SM-04 (F-NN cites Phase 7 artifact line range) `[CONTENT-AUDIT-OWED cascading]` | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:81` (single-line STRICT Execution step 2) `[CODE-VERIFIED]`. Recipient: F1 loop at `task/SKILL.md:79-98` has no git-status step today `[CODE-VERIFIED]`. Spec: § 2 line 52; § 5.4 lines 136–140; § 5.2 lines 122–128; § 10 Scenario B line 298; § 11.1 lines 331, 339. |
| **FR-TU-5** | TFEP baseline snapshot on disk at `research/test-baseline.yaml` | Author pre-F1 step that captures existing test files/function names via `uv run pytest --collect-only -q` (or directory listing) and **writes YAML to `${TASK_DIR}/research/test-baseline.yaml`**. Disk persistence is load-bearing for INV-04 resumability (donor's in-memory baseline would break across session boundaries). Baseline drives MUST-escalate vs MAY-fix-directly classification in TFEP. V/C/K = **ADOPT (adapted: in-memory → on-disk)** (§ 2 line 53). Closure pairs with F-04 (over-escalate on missing/empty/malformed baseline; classification=new). | Must | AC-ATK-03 (disambiguate baseline trinary into four states `{absent, empty, parse-fail, schema-fail}` with observation order pinned `os.path.exists → os.path.getsize → yaml.safe_load → <schema>`); AC-SM-01 (V/C/K row match) `[CONTENT-AUDIT-OWED]` | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:144-154` (in-memory store at `:147`) `[CODE-VERIFIED]`. Recipient: no `test-baseline` / `baseline` strings in body today `[CODE-VERIFIED]`; `research/` subfolder convention exists at `task/SKILL.md:205, 274` `[CODE-VERIFIED]`. Spec: § 2 line 53; § 4 lines 100–104; § 5.5 lines 142–146; § 10 Scenario C line 300; § 11.1 line 332. |
| **FR-TU-6** | TFEP Prohibition Rules + Permitted Exceptions (additive to F2) | **Append** three VIOLATION-level prohibition rules to the existing recipient F2 Prohibited Actions catalog at `task/SKILL.md:104-117` (additive, never substitutive — preserves INV-02): (1) MUST NOT fix code in response to test failures without TFEP workflow; (2) MUST NOT modify test expectations without adversarial validation; (3) Ad-hoc patches from test output are PROHIBITED. Permitted Exceptions carve-outs: ImportError/NameError in test scaffolding; lint/format failures; deprecation warnings. Disposition matrix MUST cover `{root F1, verifier-spawned F1, mid-phase rf-qa}` contexts per § 5.6. V/C/K = **ADOPT** (§ 2 line 54). Closure pairs with F-06 (per catalog 01 Gap #1 F-NN bijection caveat). | Must | AC-ATK-11 (generalization — F-05 ME-10 backing OR non-generalization carve-out — absorbs CR-TASK-08 prohibition-disposition gap per § 5.6 line 152); AC-SM-02 (ME-2 / INV-02 anchor) | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:129-142` `[CODE-VERIFIED]`. Recipient: F2 catalog at `task/SKILL.md:104-117` contains 9 prohibitions today; zero matches for "TFEP" / "test failure" / "Ad-hoc fixes" `[CODE-VERIFIED]`. Spec: § 2 line 54; § 5.6 lines 148–152; § 9 INV-02 row line 283; § 11.1 line 340. |
| **FR-TU-7** | TFEP escalation gradient + mid-phase rf-qa (third rf-qa invocation point) | Author TFEP escalation trigger detection (MUST-escalate: pre-existing test fails / 3+ new tests fail / runtime exceptions) and 6-step execution flow (halt-and-freeze → 9-field failure context YAML → forensic invocation with tier ladder light/standard/FULL-STOP → consume results → tasklist insertion with "Failure Remediation Plan (Adjudicated)" heading inserted BEFORE test/verification tasks → resume with `--compliance strict`). Routes to rf-qa as the **third** invocation point (in addition to phase-gate QA at `task/SKILL.md:191-198` and post-completion validation at `:219-241`). F-05 three-prong defense: (a) routes to existing rf-qa identity; (b) reuses existing spawn pattern; (c) named by TU-7. V/C/K = **ADOPT** (§ 2 line 55). Closure pairs with F-05 (authorized INV-03 surface extension). | Must | AC-ATK-11 (F-05 backed by retroactive ME-10 OR explicit non-generalization carve-out — bounds paragraph-level surface-widening precedent); AC-SM-02 (ME-2 rf-qa-never-replaced anchor) | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:155-168, 170-218, 238-244` `[CODE-VERIFIED]`. Recipient: today exactly two rf-qa invocation points at `task/SKILL.md:191-198` and `:219-241` `[CODE-VERIFIED]`; TU-7 adds the third. Spec: § 2 line 55; § 5.7 lines 154–158; § 12 fifth bullet line 376; § 15 residual #2 line 416; § 11.1 line 340. |
| **FR-TU-8** | TFEP incident reporting (side-effect file, no in-task heading) | Author side-effect file emission step that writes `tfep-incident-report.md` after each TFEP resolution (success or escalation). **Seven-field schema** (unenumerated in spec — see catalog 01 Gap #2; AC-ATK-12(b) requires enumeration): Trigger / Escalation count / Failing tests / Root cause / Solution / Outcome / Forensic artifacts. File is committed to git alongside other forensic artifacts. **No in-task heading inserted** — heading mutation would break INV-04. Likely path: `${TASK_DIR}/tfep/` or alongside existing QA reports at `${TASK_DIR}reviews/` (assembler decision). V/C/K = **ADOPT** (§ 2 line 56). Closure pairs with F-08 (mechanical count correction, per catalog 01 Gap #1). | Must | AC-ATK-12(b) (enumerate seven incident-report field names + types, bind in CR-FM-04); AC-SM-04 (F-NN Phase-7 artifact line range) `[CONTENT-AUDIT-OWED cascading]` | Donor: `src/superclaude/skills/sc-task-protocol/SKILL.md:220-236` `[CODE-VERIFIED]`. Recipient: side-effect files exist at `${TASK_DIR}reviews/qa-phase-[N]-report.md` referenced at `task/SKILL.md:196, 205, 226, 239` `[CODE-VERIFIED]`; `tfep-incident-report.md` joins this set. Spec: § 2 line 56; § 5.8 lines 160–164; § 9 INV-04 row line 285; § 11.1 line 341; § 12 eighth bullet line 379. |

**FR-TU summary.** Each FR-TU-N is a **Must** because (a) every TU pairs with one or more invariants `INV-01..INV-05` whose preservation is the deprecation-merge's correctness contract, and (b) every TU is verbatim-bound by the validation-spec § 2 verdict table (lines 49–56). Dropping any FR-TU-N would either reintroduce a REJECTed alternative (D09b for FR-TU-1; in-memory baseline for FR-TU-5; in-task remediation block for FR-TU-8) or fail an invariant-survival check (FR-TU-2 INV-01 row-1 ordering; FR-TU-3 INV-03 ME-2; FR-TU-4 INV-01 monotonicity; FR-TU-6 INV-02 catalog discipline; FR-TU-7 INV-03 widening surface).

---

### 14.2 Functional Requirements — Canonical Commit Sequence (FR-CS-1..FR-CS-10)

One FR per merge-step commit. Each row names the pre-commit gate(s), upstream/downstream dependencies, and the atomicity requirement. Step numbering follows validation-spec § 1 line 31 ("the 10-step canonical sequence") and § 6 step rosters. The exact row-roster per step lives in absent `merge-master.md` § 6 (R-DOC-01) — flagged `[CONTENT-AUDIT-OWED cascading]` on AC-SM-09, -10 verification.

| FR ID | Title | Description | Priority (MoSCoW) | Acceptance Criteria mapping | Source citation |
|---|---|---|---|---|---|
| **FR-CS-1** | Step 1 commit — Foundation row landing + CR-7 ORDERING sentinel authoring | Land the seven mutually-presupposing foundation rows (ME-6 "M1 atomicity" group) including authoring CR-7 ORDERING sentinel + row-1 call site (`path_override_check → tier_field_validate → gate_1_dispatch`) in `task/SKILL.md`. **Pre-commit gate: CR-FM-04 ordering grep (returns three function names in expected order) + CR-TASK-01 sentinel grep + CR-TASK-04 companion sentinel grep**. Dependencies: none (foundation). **Atomicity: REQUIRED** — landing rows in separate commits leaves intermediate states that fail their own pre-commit gates (§ 1 line 64 ME-6 load-bearing). | Must | AC-SM-07 (ordering grep returns three function names) `[CONTENT-AUDIT-OWED cascading]`; AC-SM-12 (Step 1 pre-commit gate returns 0) `[CONTENT-AUDIT-OWED cascading]`; AC-ATK-01 (AST-level ordering check); AC-ATK-13 (sentinel executable or downgrade) | Spec: § 1 lines 31, 64; § 5.1 lines 116–120; § 11.2 line 359 AC-SM-07; § 11.2 line 364 AC-SM-12. Target: `src/superclaude/skills/task/SKILL.md` (new row-1 site). |
| **FR-CS-2** | Step 2 commit — Tier classification + Gate 1 dispatch | Land `Tier:` frontmatter contract + Gate 1 dispatch step in `task/SKILL.md`; align `commands/task.md` classification header schema (already at `:50-67, 69-91`). **Pre-commit gate: CR-FM-01 canonicalization-rules check (Tier enum) + CR-TASK-02 parse-error HALT for malformed `Tier:`**. Dependencies: FR-CS-1 (row-1 site must exist before Gate 1 reads from it). Atomicity: REQUIRED — partial landing leaves dispatch reading non-existent fields. | Must | AC-ATK-10 (unified pre-loop HALT policy — input-invalid HALT row covers CR-TASK-02); AC-ATK-12(c) (CR-FM-01 canonicalization table); AC-SM-06 (10-step sequence unchanged) `[CONTENT-AUDIT-OWED]` | Spec: § 5.2 lines 122–128; § 5.3 lines 130–134; § 11.1 lines 339, 341; § 11.2 line 358 AC-SM-06. Target: `src/superclaude/skills/task/SKILL.md` frontmatter + Gate 1 section. |
| **FR-CS-3** | Step 3 commit — Path overrides + Gate 2 roster widening | Land Critical/Trivial Path Override mechanism (FR-TU-2) and widen Phase-Gate QA roster to `[rf-qa, quality-engineer]` (FR-TU-3). **Pre-commit gate: CR-FM-04 row-1 ordering grep re-run + ME-2 anchor check (rf-qa present at all invocation points)**. Dependencies: FR-CS-1 (sentinel + row-1 site), FR-CS-2 (tier dispatch exists for override-vs-dispatch interaction). Atomicity: REQUIRED — partial roster widening violates ME-2 (rf-qa never replaced). | Must | AC-ATK-01 (call-site ordering check); AC-ATK-11 (F-05 carve-out frames the widening surface); AC-SM-02 (ME-2 traceability) | Spec: § 2 lines 50–51; § 9 INV-03 row line 284; § 11.1 lines 330, 340; § 11.2 line 354 AC-SM-02. Target: `task/SKILL.md:181-211, 290-299`. |
| **FR-CS-4** | Step 4 commit — TU/donor verbatim diff audits + sentinel landing | Land CR-TASK-12 seven-diff audit pass (six donor-string verbatim diffs + one sentinel-comment block diff) against `src/superclaude/skills/sc-task-protocol/SKILL.md` while donor still exists. **Pre-commit gate: CR-TASK-12 seven-diff audit returns zero-diff**. Dependencies: FR-CS-1..3 (donor strings must be reflected in recipient before audit fires). Atomicity: REQUIRED — gate intent is single-shot pre-CR-DEP-03 (donor hard-delete) snapshot per AC-ATK-06; rebase-split would void the audit window. | Must | AC-SM-08 (CR-TASK-12 returns 7 zero-diff invocations: 6 donor strings + 1 sentinel-comment block) — **validatable in-repo post-Step-1**; AC-ATK-06 (snapshot donor strings into frozen fixture before Step 6 OR mark CR-TASK-12 Step-4-only with successor-audit obligation) | Spec: § 5.10 lines 172–176; § 7.1 line 268; § 10 Scenario D line 302; § 11.1 line 335; § 11.2 line 360 AC-SM-08. Target: pre-commit script + `tests/fixtures/donor-blocks/` (proposed by AC-ATK-06 option (a)). |
| **FR-CS-5** | Step 5 commit — Donor command stubification (CR-DEP-01 + CR-DEP-02 + CR-DOC-01) | Stubify donor command `src/superclaude/commands/task.md` (body → deprecation stub) per CR-DEP-01; emit **sha256** digest per CR-DEP-02 (AC-ATK-09 mechanical substitution; **NOT md5sum**); land CR-DOC-01 documentation row inline (primary location). S-1 pre-condition: any in-flight PRD referencing donor surfaces (e.g., the generalized form of `TASK-PRD-20260514-121039`) must complete OR S-1 `--max-wait 14d` snapshot auto-invokes. **Pre-commit gate: pytest pass + CR-DEP-02 sha256 baseline + CR-DEP-05 grep (residual `/sc:task` scoped per AC-ATK-14(a)) + CR-AUDIT-FM-03-SUNSET binding check**. Dependencies: FR-CS-4 (audit window must close pre-stubification). Atomicity: REQUIRED — rebase-split is the documented Scenario H-2 INV-S-2 breach (sprint/process.py emitter desync from stubified surface). | Must | AC-ATK-08 (S-1 `--max-wait 14d` + pinned git-SHA at every `[CODE-VERIFIED]` tag + CR-DEP-05 extension to post-Step-5 docs); AC-ATK-09 (sha256 replacement for CR-DEP-02 — LOW severity mechanical); AC-ATK-15 (CR-DOC-01 Step 5 primary, Step 8 fallback only on gate failure + hot-fix auth); AC-SM-09 (Step 5 commit contains exactly rows named at source line 375) `[CONTENT-AUDIT-OWED cascading]`; AC-SM-12 (Step 5 pre-commit gate returns 0) `[CONTENT-AUDIT-OWED cascading]` | Spec: § 3 line 86; § 6.1 line 184; § 6.6 lines 214–218; § 7.1 lines 244, 248–250; § 10 Scenarios F line 306, H-1 line 312, H-2 line 314; § 11.1 lines 337–338, 344, 347. Target: `src/superclaude/commands/task.md` (stubified). |
| **FR-CS-6** | Step 6 commit — Donor skill hard-delete (CR-DEP-03) + directory + residual greps | Hard-delete donor `src/superclaude/skills/sc-task-protocol/SKILL.md` (+ `__init__.py`) per CR-DEP-03. **Pre-commit gate: AC-ATK-07 rf-qa verifier role (rebound to verify F-07 procedural authorization chain: sprint goal → T06.03 → § 2 rubric → § 4 traceability → structural precondition) + CR-DEP-04 directory-absence check (`find -type d` per AC-ATK-14(c)) + CR-DEP-05 grep with extension/excluded-path/hidden-dir scope per AC-ATK-14(a)**. Dependencies: FR-CS-4 (CR-TASK-12 audit closed) + FR-CS-5 (command stub already landed). Atomicity: REQUIRED — split between hard-delete and directory removal exposes Scenario D (CR-TASK-12 re-fire against missing donor) breaking INV-01. | Must | AC-ATK-07 (rf-qa F-07 verifier spawned at Step 6 pre-commit; PASS before hard-delete); AC-ATK-14(a)(c) (CR-DEP-05 grep scope, CR-DEP-04 gate point); AC-SM-10 (Step 6 commit contains exactly rows named at source line 381) `[CONTENT-AUDIT-OWED cascading]`; AC-SM-12 (Step 6 pre-commit gate returns 0) `[CONTENT-AUDIT-OWED cascading]` | Spec: § 3 line 86; § 6.1 lines 184–188; § 6.3 lines 196–200; § 8 line 264; § 10 H-4 line 318; § 11.1 lines 336, 343; § 11.2 lines 362, 364. Target: hard-delete `src/superclaude/skills/sc-task-protocol/`. |
| **FR-CS-7** | Step 7 commit — Sprint / pipeline integrator fix-up | Land sprint / pipeline / CLI integrator code adjustments so that no runtime caller emits `/sc:task` after Step 5 stubification. Includes Scenario H-2 mitigation surface (`sprint/process.py` emitter alignment with stubified surface). **Pre-commit gate: pytest pass + AC-ATK-17 server-side pre-push hook re-grep of `/sc:task\b` against `src/superclaude/cli/` on landing commit (rejects push if grep matches AND donor body not also deleted)**. Dependencies: FR-CS-5 + FR-CS-6 (stubification + hard-delete must precede integrator fix-up to expose call sites). Atomicity: REQUIRED — partial integrator update is the running-broken-state attractor that AC-ATK-17 defeats. | Must | AC-ATK-17 (server-side pre-push hook on landing commit — V3 security-probe origin); AC-SM-12 (pre-commit gates Steps 1/5/6 return 0; Step 7 by extension) `[CONTENT-AUDIT-OWED cascading]` | Spec: § 10 Scenario H-2 line 314; § 11.1 line 346. Target: `src/superclaude/cli/`, `src/superclaude/execution/` (consumer surfaces). |
| **FR-CS-8** | Step 8 commit — Documentation rollup + mkdocs build | Land documentation rollup: any CR-DOC-01 fallback (only if Step 5 pre-commit gate failed AND hot-fix authorized per AC-ATK-15); CR-DOC-13 R-RULE-11 final audit row with scope decision per AC-ATK-14(d) (rename to scoped doc-only audit OR widen to 65 CR-IDs). **Pre-commit gate: `mkdocs build` returns 0 broken-link warnings** (FM-05 caveat: mkdocs version pinning per § 13 line 391). Dependencies: FR-CS-5 (CR-DOC-01 primary lands at Step 5; Step 8 only fallback). Atomicity: REQUIRED — split between rollup and mkdocs validation could land orphan doc references. | Must | AC-ATK-15 (Step 5 / Step 8 disambiguation); AC-ATK-14(d) (CR-DOC-13 rename vs widen-to-65); AC-SM-06 (10-step sequence unchanged) `[CONTENT-AUDIT-OWED]` | Spec: § 6.6 lines 214–218; § 6.7 lines 220–224; § 13 FM-05 line 391; § 11.1 lines 343–344; § 11.2 line 358 AC-SM-06. Target: `docs/` source tree + mkdocs config. |
| **FR-CS-9** | Step 9 commit — Leave-as-is enforcement across bucket roster (A, C, D, E, F, G, H) | Apply leave-as-is enforcement across the named CR-REF buckets: `CR-REF-BUCKET-{A, C, D, E, F, G, H}` — bucket B explicitly omitted from § 8 line 269 (intentional or typo flagged in synthesis 05 Gap #5, surfaced to S13 Open Questions). CR-REF-12 grep scoped to `[src]` and `[.claude]` (NOT to `.dev/releases/backlog/` or `docs/generated/*`). CR-REF-18 `DEPRECATION-NOTE.md` existence check at cluster root (path resolved per AC-ATK-14(b)). **Pre-commit gate: bucket-grep returns zero unauthorized residuals; cluster-root path resolved**. Dependencies: FR-CS-6 (donor hard-deleted before residual sweep). Atomicity: REQUIRED — bucket sub-rows are co-presupposing; partial enforcement leaves one bucket unscrubbed. | Must | AC-ATK-14(b) (CR-REF-18 cluster root path); AC-SM-06 (step roster unchanged) `[CONTENT-AUDIT-OWED]` | Spec: § 6.8 lines 226–230; § 8 lines 262–272 (buckets at line 269); § 11.1 line 343. Target: bucket-archive subtrees + cluster-root `DEPRECATION-NOTE.md`. |
| **FR-CS-10** | Step 10 commit — Deferred regenerator placeholder + frozen-pre-merge banner | Land `docs/generated/*` deferred-regeneration placeholder with frozen-pre-merge banner explicitly marking generated docs as describing `/sc:task` as a frozen pre-merge surface (mitigates § 13 FM-06 line 392 — if next regenerator run never schedules, `docs/generated/*` would permanently disagree with `docs/`). **Pre-commit gate: banner string present in every `docs/generated/*` file referencing `/sc:task` OR `sc-task-protocol`**. Dependencies: FR-CS-6 + FR-CS-8 (hard-delete + mkdocs validate must precede banner landing). Atomicity: REQUIRED — partial banner landing exposes the FM-06 footgun on bucket-sampled regen runs. | Must | AC-ATK-18(b)(c) (gate-1.5 emission + one-shot acknowledgment gate cover content-level resume; banner is the visible artifact); AC-SM-06 (10-step sequence unchanged) `[CONTENT-AUDIT-OWED]` | Spec: § 7.1 line 244; § 7.3 line 270; § 13 FM-06 line 392; § 11.1 line 347. Target: `docs/generated/*` (banner injection script). |

**FR-CS atomicity rationale (load-bearing).** Every FR-CS-N is **Must** with **atomicity REQUIRED** because validation-spec § 1 line 64 names **ME-6 M1 atomicity** as load-bearing: "The seven foundation rows are mutually-presupposing; landing them in separate commits leaves intermediate states that fail their own pre-commit gates." Scenarios D (line 302), F (306), H-1 (312), H-2 (314), H-4 (318) document the concrete invariant breaches that non-atomic landing produces. The 10-step ordering is **not** decorative — the dependency chain `FR-CS-4 → FR-CS-5 → FR-CS-6 → FR-CS-7` is the central correctness invariant of the deprecation merge.

**Step roster verification gap (R-DOC-01).** AC-SM-09 ("Step 5 commit contains exactly the rows named at source line 375") and AC-SM-10 ("Step 6 commit … line 381") both anchor in absent `final-merge-plan.md` and absent `merge-master.md § 6`. The FR-CS-N descriptions above cite the **named** rows from the validation spec; the exact roster per step is flagged `[CONTENT-AUDIT-OWED cascading]` and surfaced to **S13 Open Questions** per synthesis 05 Gap #12.

---

### 14.3 Functional Requirement — CR-DEP-06 Elevated to Must

**FR-CR-DEP-06** is the elevation of the previously-proposed Step-8/post-Step-6 audit row to a **required** functional requirement, justified by the live-grep evidence of **144 residual `/sc:task` occurrences** in the working tree (per research-notes ARTIFACT_GAPS). Without CR-DEP-06 the merge ships with an unaudited residual-reference surface across the leave-as-is buckets (`.dev/releases/backlog/`, bucket archives, `docs/generated/*`).

| FR ID | Title | Description | Priority (MoSCoW) | Acceptance Criteria mapping | Source citation |
|---|---|---|---|---|---|
| **FR-CR-DEP-06** | Post-Step-6 one-shot residual-reference manifest (elevated to Must per 144 occurrences) | Author a one-shot post-Step-6 grep that produces a **structured manifest** of every surviving `/sc:task` / `sc-task-protocol` / `task-unified` reference outside the authorized leave-as-is buckets, with **per-string disposition** (e.g., `bucket=archive action=leave-as-is`, `bucket=docs-generated action=banner-required`, `bucket=src action=violation`). Manifest written to `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}`. **Pre-commit gate (one-shot, post-FR-CS-6/FR-CS-9): residual count outside authorized buckets MUST equal zero; otherwise gate fails with violation list.** Authorized leave-as-is buckets enumerated at § 8 line 269 (A, C, D, E, F, G, H — bucket B omission resolved in S13 Open Questions). Atomicity: REQUIRED — single commit landing the manifest + gate disposition; partial landing allows residuals to ride into Step 10. | **Must (elevated)** | AC-ATK-18(d) (CR-DEP-06 one-shot post-Step-6 grep emitting structured manifest of every surviving residual outside authorized leave-as-is buckets); AC-ATK-14(a) (CR-DEP-05 grep scope flags — companion); AC-ATK-18(a)(b)(c) (CR-FM-03 content-level resume grep + gate-1.5 emission + one-shot ack gate — content-side enforcement complementary to manifest-side) | Spec: § 8 lines 262–272 (named bucket roster at 269); § 11.1 line 347 AC-ATK-18(d) "author CR-DEP-06 — one-shot post-Step-6 grep emitting structured manifest of every surviving residual outside authorized leave-as-is buckets"; § 16 line 431. Live evidence: research-notes ARTIFACT_GAPS records **144 residual `/sc:task` occurrences** in the working tree (verified by live grep at synthesis time). Target: new pre-commit gate script + `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}`. |

**Elevation justification (PRD-level).**

1. **Quantitative trigger.** Validation-spec § 7.3 line 270 flags `docs/generated/*` as a deferred-regen risk; § 8 line 269 names seven authorized leave-as-is buckets. Live grep records **144 occurrences** — an order of magnitude larger than the 25-MDTM-file in-flight set referenced in FR-CS-7 / FR-TU residual scope. Without CR-DEP-06 the deprecation surface persists silently across release artifacts. Severity is therefore not LOW (unlike AC-ATK-09 mechanical sha256).
2. **Operational closure.** AC-ATK-18 introduces CR-DEP-06 in § 11.1 line 347 as the **fourth** sub-binding of an already-Must AC (`(d)` of the four-part AC-ATK-18). Promoting the sub-binding to a numbered FR removes the readability hazard of multi-sub-obligation ACs (per synthesis 05 § "Cross-cutting AC-ATK fan-out" line 305–309).
3. **V3 security-probe origin.** AC-ATK-18 is V3 (security-probe origin per synthesis 05 line 70 tally; one of three V3-origin ACs alongside -16 flock discipline and -17 server-side pre-push). Elevating CR-DEP-06 to Must aligns PRD priority with the adversarial-validation severity surfaced by the V3 probe.
4. **R-DOC-01 independence.** Unlike many AC-SM rows, CR-DEP-06 is **validatable in-repo**: the grep can run today against the current working tree (`grep -rn '/sc:task\b\|sc-task-protocol\|task-unified' .` outside authorized buckets) without depending on a content audit of the upstream artifacts. This makes the FR low-risk to scope and high-yield to ship.

---

### 14.4 MoSCoW Summary

| MoSCoW tier | FR count | FR IDs | Justification |
|---|---:|---|---|
| **Must** | 19 | FR-TU-1..FR-TU-8 (8) + FR-CS-1..FR-CS-10 (10) + FR-CR-DEP-06 (1) | Every TU pairs with an INV-NN preservation contract (§§ 2, 9, 11); every CS-step pairs with ME-6 atomicity + named pre-commit gate; CR-DEP-06 elevation justified by 144 live residuals + V3 security-probe origin. Dropping any **Must** row reintroduces a REJECTed alternative or fails a falsifiable acceptance criterion in § 11. |
| **Should** | 0 | — | None proposed in this synthesis. Candidates for downstream PRD revision (out of scope here): AC-ATK-12 sub-binding decomposition into three sub-FRs (CR-FM-03 sunset; CR-TASK-10 seven-field enumeration; CR-FM-01 canonicalization table); AC-ATK-14 sub-binding decomposition into four sub-FRs (CR-DEP-05 grep scope; CR-REF-18 cluster root; CR-DEP-04 gate point; CR-DOC-13 scope companion). Flagged for synth-07 Risks (R-FAN-OUT). |
| **Could** | 0 | — | Reserved for non-load-bearing optimizations (none surfaced in research catalogs 01 / 05). |
| **Won't** | 0 | — | The validation spec § 6 / § 8 leave-as-is bucket roster constitutes an implicit "won't" for bucket-internal rewriting (handled by FR-CS-9 + FR-CR-DEP-06 disposition rather than as a separate FR negative). No further "won't" needed. |

**Total: 19 Must, 0 Should, 0 Could, 0 Won't.**

---

### 14.5 Citation Provenance Summary

- **Donor surfaces cited** (every FR-TU-N): `src/superclaude/skills/sc-task-protocol/SKILL.md` `[CODE-VERIFIED]` end-to-end.
- **Recipient surfaces cited** (every FR-TU-N): `src/superclaude/skills/task/SKILL.md` `[CODE-VERIFIED]` end-to-end for current-state anchors (e.g., `:79-98` F1 loop, `:104-117` F2 catalog, `:181-211` Phase-Gate QA, `:191-198` rf-qa spawn, `:219-241` post-completion validation, `:290-299` agent spawning).
- **Validation-spec sections cited** (every FR): §§ 1 (closure clauses), 2 (V/C/K verdict table lines 49–56), 5 (predicate-attack subsections 5.1–5.10), 6 (commit-sequence step rosters 6.1–6.8), 7 (rebase / generated-doc hazards), 8 (bucket roster + CR-DEP-06 proposal lines 262–272), 9 (INV walkthroughs), 10 (Scenarios A–H), 11.1 (AC-ATK-01..18), 11.2 (AC-SM-01..12), 12 (closure tradeoffs), 13 (FM-05/06 timing hazards), 15 (residual risks), 16 (recommendation lines 427–437).
- **Absent-artifact dependencies surfaced** (R-DOC-01): AC-SM-01, -03, -05, -06, -11 explicitly `[CONTENT-AUDIT-OWED]`; AC-SM-04, -07, -09, -10, -12 cascading via absent `final-merge-plan.md`. Flagged across FR-TU-1, FR-TU-2, FR-TU-3, FR-TU-4, FR-TU-5, FR-TU-8, FR-CS-1, FR-CS-2, FR-CS-5, FR-CS-6, FR-CS-7, FR-CS-8, FR-CS-9, FR-CS-10. Resolution lives in **S13 Open Questions** + **synth-07 Risks**.

---

---

### 14.7 NFR — Invariants (NFR-INV-1..NFR-INV-5)

**Category basis:** All five rows are categorized as **Reliability / Behavioral Invariant** — they bind runtime semantics of the merged `/task` skill that downstream implementers MUST preserve verbatim per validation-spec § 2 "defense overlay" framing. INV-04 is additionally categorized as **Reliability / Backward Compatibility** because its resumability guarantee crosses session boundaries and binds the in-flight task population.

INV-04 carries a **two-row treatment** distinguishing parse-level from semantic-level resumability per task instruction; the NFR ID remains `NFR-INV-4` with two sub-rows `NFR-INV-4a` (parse) and `NFR-INV-4b` (semantic), reflecting the parse-vs-semantic structure of validation-spec § 4 and research-02 § B INV-04 row.

| NFR ID | Category | Statement | Verification Method | Source |
|---|---|---|---|---|
| **NFR-INV-1** | Reliability / Behavioral Invariant (F1 progress monotonicity) | The F1 execution loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT) MUST make monotonic progress across checked items. No closure, audit, or extension introduced by this merge may add a new HALT semantic that pauses the loop mid-checklist. Blockers are logged and the loop advances. The environment-non-ideal class (e.g. `git_status` not clean, `git` tool absent, directory not a git repo, `git status` errors) MUST be treated as warn-and-continue, NOT HALT (input-invalid asymmetry per AC-ATK-10). | (1) Direct Read of `src/superclaude/skills/task/SKILL.md` F1 loop region (currently lines 79-98) confirms no HALT semantic added; (2) `make sync-dev && make verify-sync` passes; (3) AC-ATK-02 five-row `git_status` matrix test fires warn-and-continue for {tool-absent, not-a-repo, error-other} states and HALT for none; (4) AC-ATK-13 sentinel-comment ordering test confirms F-02 markdown sentinels do not constrain runtime ordering; (5) F2 prohibitions catalog grep confirms no environment-state-triggered HALT clause introduced. | Validation-spec § 2 line 53 (INV-01); validation-spec § 5.4 (F-03 closure) and § 5.1 (F-02 closure); research-02 § B INV-01 row [CODE-VERIFIED against `task/SKILL.md:79-98` + `:104-117`]; **[VALIDATION-SPEC-CITED][UNVERIFIED]** for the underlying anchor `extension-point-contracts.md:11-17` per R-DOC-01. **Load-bearing protectors:** ME-3 (primary), ME-6 (indirect via commit-shape). **Closure obligations:** AC-ATK-01, AC-ATK-02, AC-ATK-10, AC-ATK-13. |
| **NFR-INV-2** | Reliability / Behavioral Invariant (F2 catalog additivity) | The F2 "Prohibited Actions" catalog in the merged `task/SKILL.md` MUST be extended only additively. No existing prohibition (working from memory, multi-item parallelism, skipping items, assuming completion, inventing file paths, modifying items, adding items, delegating across phase boundaries, skipping phase-gate QA / post-completion validation) may be deleted, weakened, or rewritten in a way that narrows its semantic scope. New prohibitions introduced by TU-6 / TFEP integration MUST fit within the existing semantic category structure. Disposition of an F2 prohibition firing inside a verifier-spawned F1 (mid-phase rf-qa context per F-05 / TU-7) MUST be bound by a prohibition-disposition matrix; the matrix MUST cover {root F1, verifier-spawned F1, mid-phase rf-qa context} at minimum. | (1) Diff `src/superclaude/skills/task/SKILL.md` F2 region pre-merge vs post-merge: every pre-merge bullet present verbatim post-merge (additive-only check); (2) TU-6 / TFEP-additions are demonstrably new bullets, not edits to existing ones; (3) AC-ATK-11 prohibition-disposition matrix authored and committed alongside the merge; (4) `make verify-sync` passes; (5) `tests/skills/task/test_prohibitions_additive.py` (to be authored) asserts every pre-merge F2 bullet appears in the post-merge file by substring match. | Validation-spec § 2 line 54 (INV-02); validation-spec § 5.6 (verifier-spawned F1 disposition gap); research-02 § B INV-02 row [CODE-VERIFIED against `task/SKILL.md:104-117` and donor `sc-task-protocol/SKILL.md:129-142`]. **Load-bearing protectors:** Catalog-additivity is self-enforcing at parse-level (grep / diff). **Closure obligations:** AC-ATK-11 (nested-F1 disposition matrix). |
| **NFR-INV-3** | Reliability / Behavioral Invariant (Phase-gate rf-qa floor) | The `rf-qa` agent MUST remain the named role at every phase-gate verification point in the merged surface. Three invocation points MUST be preserved: (i) Gate 2 verification roster, (ii) post-completion structural validation, (iii) mid-phase escalation (TU-7 / F-05 third invocation). Roster widenings (adding companion agents) are permitted; replacements or displacements are prohibited. The rf-qa spawn block MUST be anchored such that formatting edits that shift line ranges do not silently break the parse-level reference; the anchor MUST be content-keyed (e.g. heading-keyed, block-tag-keyed, or symbol-keyed), NOT line-number-keyed. | (1) Direct Read of `task/SKILL.md` confirms `subagent_type: 'rf-qa'` literal present at all three invocation points post-merge; (2) AC-ATK-07 names rf-qa as F-07 chain-integrity verifier at Step 6 pre-commit; (3) AC-ATK-11 binds the F-05 widening as either retroactive ME-10 or one-time non-generalizing carve-out; (4) CR-FM-04 line-anchor audit fires if the rf-qa spawn block region drifts beyond a content-keyed anchor; (5) `tests/skills/task/test_rf_qa_invocation_points.py` (to be authored) asserts three distinct rf-qa spawn sites by content match, not line number. | Validation-spec § 2 line 51-52 + 55 (INV-03); validation-spec § 5.7 (F-05 paragraph-level surface-widening precedent); research-02 § B INV-03 row [CODE-VERIFIED for two invocation points at `task/SKILL.md:191-198` and `:219-226`; mid-phase invocation is post-merge target — donor `sc-task-protocol/SKILL.md:170-218` currently routes to `/sc:forensic`, retargeted to rf-qa by F-05]. **Load-bearing protectors:** ME-2 (primary), ME-9 (F-07 chain integrity). **V3 augmentation:** line-anchor brittleness call-out → CR-FM-04. **Closure obligations:** AC-ATK-07, AC-ATK-11. |
| **NFR-INV-4a** | Reliability / Backward Compatibility (Resumability — parse level) | Every existing MDTM TASK-* file in `.dev/tasks/` MUST continue to parse and resume cleanly after the merge at the **structural / parse layer**: YAML frontmatter remains valid; checklist syntax (`- [ ]`, `- [x]`, `- [-]`, `- [!]`, `- [?]`) remains recognized by the F1 loop; task-log append-only schema is unchanged; the CR-FM-03 compatibility shim defaults absent `Tier:` frontmatter to `STANDARD` (per the post-merge canonical tier vocabulary — open question per synth-01 on whether canonical set is 3-tier `{STRICT, STANDARD, TRIVIAL}` or 4-tier `{STRICT, STANDARD, LIGHT, EXEMPT}`); TU-5 baseline YAML and TU-8 incident-report artifacts persist across session boundaries. Parse-level success is necessary but NOT sufficient for semantic resumability — see NFR-INV-4b. | (1) `tests/skills/task/test_compat_shim_parse.py` (to be authored) iterates every TASK-* file under `.dev/tasks/` and asserts: YAML loads, checklist regex matches at least one item, task-log section appends rather than overwrites; (2) CR-FM-03 shim defaults absent `Tier:` to `STANDARD` (assertion case for files with no Tier field); (3) Manual resumption walkthrough on TASK-RESEARCH-20260403-sprint-task-exec (48 donor-surface refs across 10 files in subtree, 2026-05-16 fix-cycle 1 live recount, status Doing) reads cleanly under merged skill; (4) `tests/skills/task/test_baseline_persistence.py` (to be authored) round-trips TU-5 baseline YAML and TU-8 incident-report fixtures across simulated session boundary. | Validation-spec § 2 line 50 + § 4 lines 94-109 (INV-04 parse-level dimension); validation-spec § 5.5 (TU-5 baseline) and § 5.8 (TU-8 incident); research-02 § B INV-04 row, parse layer [CODE-VERIFIED for F1 loop content-blindness at `task/SKILL.md:79-98, 269-282`; CR-FM-03 shim itself NOT yet present in `task/SKILL.md` — post-merge TU-1 addition]. **Load-bearing protectors:** ME-3 (warn-continue at resume), ME-6 (atomicity prevents intermediate broken state). **Closure obligations:** AC-ATK-12 (CR-FM-03 sunset binding). |
| **NFR-INV-4b** | Reliability / Backward Compatibility (Resumability — semantic level) | The **meaningful resume path** through every in-flight TASK-* file's checklist body MUST survive the merge — i.e. parse-level success per NFR-INV-4a is not sufficient if the resumed task's next actionable step references a deprecated surface (`/sc:task`, `sc-task-protocol/SKILL.md`, `task-unified`) that has been stubified (CR-DEP-01) or deleted (CR-DEP-03). The merged surface MUST detect content-level deprecated-surface references at resume time, emit a warn-and-continue marker (NOT HALT per ME-3), require one-shot acknowledgement in the task log by the resuming subagent, and continue execution. Three specific semantic exposures MUST be closed: (i) content-level deprecated-surface refs in the live in-flight population (currently 132 union files across `.dev/tasks/` per 2026-05-16 fix-cycle 2 live recount — 130 live at fix-cycle 1; population dynamic; the spec's § 3 line 81 figure of 96 is now an UNDER-count, not an over-count — population has grown); (ii) default-`STANDARD` shim MUST NOT silently strip implicit-STRICT obligations from pre-`Tier:` checklists; (iii) the CR-FM-03 shim MUST have an explicit sunset binding (a future audit row dropping the default fall-through cannot brick shim-era TASK-* files without notice). | (1) AC-ATK-18 content-level audit runs at resume time: `grep -E "/sc:task\b\|sc-task-protocol\|task-unified"` against task body; warn-and-continue with one-shot ack gate; (2) CR-DEP-06 residual-reference manifest produced at Step 6 post-commit covers `.dev/tasks/to-do/`, `.dev/releases/backlog/`, `docs/generated/` (per research-04 § 5.4); (3) Manual resumption walkthrough on TASK-RESEARCH-20260403-sprint-task-exec exercises the content-level audit and confirms ack gate fires; (4) AC-ATK-12 binds CR-FM-03 sunset (e.g. "at least N task generations or until explicit migration row lands" — N to be specified per S13 Open Question); (5) `tests/skills/task/test_resume_content_audit.py` (to be authored) asserts content-level grep fires on a fixture task containing `/sc:task` in checklist body. | Validation-spec § 4 lines 94-109 (parse-vs-semantic distinction — the load-bearing structural argument); validation-spec § 9 line 285 ("**HIGHEST EXPOSURE:** 96 in-flight files..." — spec figure 96 now divergent in DIRECTION as well as magnitude; live count is 132 per 2026-05-16 fix-cycle 2 (130 at fix-cycle 1; population dynamic); semantic exposure pattern unchanged but blast radius LARGER, not smaller); validation-spec § 10 H-4 (resumed-task hits deleted PRIMARY ARTIFACT); research-02 § B INV-04 row, semantic layer; research-04 § 4 H-4 row and § 5 CR-DEP-06 elevation. **Load-bearing protectors:** ME-3 (warn-continue dispatch), ME-9 (residual-reference visibility). **V3 augmentation:** 96-file empirical exposure (figure DIVERGENT; population has grown to 132 at fix-cycle 2 / 130 at fix-cycle 1 — population dynamic; pattern stands) → AC-ATK-18 + CR-DEP-06 elevation from "proposed" to **REQUIRED**. **Closure obligations:** AC-ATK-12, AC-ATK-18, CR-DEP-06. |
| **NFR-INV-5** | Reliability / Behavioral Invariant (Refusal-of-definition for `Tier:`) | The `Tier:` field on a task file (frontmatter level) and any per-item `(Tier: ...)` marker on a checklist item MUST be treated as **metadata that conditions which audits run**, NOT as **work-definition that drives runtime dispatch**. The per-item marker is a tier-conditioned **read**, not a runtime classifier. The merged surface MUST enumerate a closed list of authorized per-item-marker consumers (initial set: `{CR-TASK-07 baseline-skip}`); any new consumer requires a new manifest exception (ME-10+) referencing this NFR. The parse-level canonicalization rules (e.g. case-normalization, whitespace, accepted value set) for the `Tier:` field MUST be specified by CR-FM-01 before the post-merge feature ships. | (1) AC-ATK-05 closed-enum authorized-consumer list authored and committed in `task/SKILL.md` or an adjacent rules file; (2) ME-1 audit fires (design-time review checklist row) on any proposed new per-item-marker consumer; (3) CR-FM-01 canonicalization rules table committed with explicit `{case-normalization, whitespace handling, accepted-value-set}` columns; (4) `tests/skills/task/test_tier_marker_consumers.py` (to be authored) asserts the post-merge code reads the marker only from the enumerated consumer call-sites; (5) Tier vocabulary canonical-set decision recorded in S13 Open Questions (synth-01 cross-reference) and reflected in CR-FM-01 accepted-value-set. | Validation-spec § 2 line 49 (INV-05); validation-spec § 5.3 (per-item marker consumer list open) + § 9 line 286 (CR-FM-01 normalization unspecified); research-02 § B INV-05 row [feature surface NOT yet present in `task/SKILL.md`; donor `commands/task.md:50-67` uses 4-tier `{STRICT, STANDARD, LIGHT, EXEMPT}` while validation-spec § 4 line 103 references 3-tier `{STRICT, STANDARD, TRIVIAL}` — Tier vocabulary reconciliation open question]. **Load-bearing protectors:** ME-1 (primary). **V3 augmentation:** closed-enum consumer list → AC-ATK-05. **Closure obligations:** AC-ATK-05, AC-ATK-12 (CR-FM-01 normalization). |

**INV NFR cross-reference summary:**

- **NFR-INV-4 carries the spec's "HIGHEST EXPOSURE" annotation** (validation-spec § 9 line 285) and is the only INV with a parse-vs-semantic split treatment. The split is load-bearing for the merge's correctness story: NFR-INV-4a covers what the CR-FM-03 shim can mechanically guarantee (structural parsing); NFR-INV-4b covers the residual semantic exposure that CR-FM-03 cannot see (content-level deprecated-surface references). All other INVs are single-row.
- **NFR-INV-1, NFR-INV-3, NFR-INV-4b** carry V3 (security-probe) augmentations per validation-spec § 9 INV rows 282, 284, 285 respectively. NFR-INV-2 and NFR-INV-5 carry no V3 augmentation row in § 9 but rest on V3 contributions in § 5.6 (NFR-INV-2 nested-F1 disposition) and § 5.3 + § 9 line 286 (NFR-INV-5 closed-enum + canonicalization).
- **NFR-INV-4b's divergent-figure note:** the spec-quoted 96-file count is now an UNDER-count — the live 2026-05-16 fix-cycle 1 recount is **132 union files** referencing donor surfaces across `.dev/tasks/`, against the earlier (and itself stale at synthesis time) 25-file research-03 narrower-scope figure. Blast radius has GROWN, not shrunk; direction of divergence is inverted vs the original synthesis narrative. The **semantic exposure pattern is unchanged**. PRD S20 Risk Analysis MUST surface this as R-DIV-01 with the corrected direction.

---

### 14.8 NFR — Manifest Exceptions (NFR-ME-1..NFR-ME-9)

**Category basis:** All nine rows are categorized as **Auditability / Governance** — manifest exceptions are audit gates that bind downstream contributors' design discretion. The "Source" column flags load-bearing status per research-02 § A summary table and names the closure clause each ME leans on. Ancillary MEs (4, 5, 7, 8) are included for catalog completeness per task instruction "one NFR per manifest exception"; their statement clauses are deliberately minimal because they fence donor patterns no F-01..F-08 finding re-opened.

| NFR ID | Category | Statement | Verification Method | Source |
|---|---|---|---|---|
| **NFR-ME-1** | Auditability / Governance (Per-item dispatch forbidden — Load-bearing for NFR-INV-5) | ME-1 MUST be enforced at design-review time: no closure, audit extension, or surface widening introduced by this merge may cause a per-item `(Tier: ...)` marker on a checklist item to become a runtime classifier or dispatcher. The marker is a **tier-conditioned read**, not a tier-conditioned dispatch. ME-1 covers both (i) direct dispatch (a switch on the marker value at a runtime call-site) and (ii) wrapper-routed dispatch (a function that reads the marker and routes based on its value — semantically a dispatcher even if parse-level a "read"). The authorized-consumer enumeration in NFR-INV-5 / AC-ATK-05 is the operational manifestation of ME-1. | (1) Design-review checklist row in PRD S21 (Implementation Plan) explicitly names ME-1 audit; (2) AC-ATK-05 closed-enum authorized-consumer list passes review; (3) Code-review grep for new per-item marker consumers against the AC-ATK-05 enumeration; (4) Any new consumer rejected at review unless accompanied by a new manifest exception (ME-10+). | Validation-spec § 2 line 60 (ME-1 load-bearing for INV-05; D09b indirect link to INV-01); validation-spec § 5.3 (CR-TASK-03 predicate-precision attack); research-02 § A ME-1 row. **Load-bearing status:** Load-bearing. **Closure clause leaned on:** F-01 "tier-conditioned reads only" disposition (validation-spec § 5.3 line 132). **Concession 1 (validation-spec § 15 line 415):** "Tier-conditioned read" boundary is conceptually thin; ME-1 relies on human-process design-time review, not structural runtime guard. |
| **NFR-ME-2** | Auditability / Governance (rf-qa never replaced / never displaced — Load-bearing for NFR-INV-3) | ME-2 MUST be enforced at the three rf-qa invocation points: (i) Gate 2 verification roster, (ii) post-completion structural validation, (iii) mid-phase escalation (TU-7 / F-05 third invocation). Roster widenings (companion agents added alongside rf-qa) are permitted. Replacements (substituting another agent for rf-qa) and displacements (moving rf-qa out of any of the three positions) are prohibited. The rf-qa spawn block MUST be anchored by a content-keyed reference (CR-FM-04), not by line number, to survive formatting edits. | (1) `tests/skills/task/test_rf_qa_invocation_points.py` (to be authored) asserts three distinct rf-qa spawn sites in the merged `task/SKILL.md` by content match; (2) CR-FM-04 line-anchor audit fires if the rf-qa spawn block region drifts beyond its content-keyed anchor; (3) Design-review checklist row in PRD S21 explicitly names ME-2 audit at any rf-qa-touching change; (4) AC-ATK-11 binds the F-05 widening as either retroactive ME-10 or one-time non-generalizing carve-out — surfaced as S13 Open Question. | Validation-spec § 2 line 61 (ME-2 floor for INV-03); validation-spec § 5.7 (F-05 paragraph-level surface-widening precedent); validation-spec § 9 INV-03 row line 284 (V3 augmentation: line-anchor brittleness → CR-FM-04); research-02 § A ME-2 row [CODE-VERIFIED for two of three invocation points at `task/SKILL.md:191-198` and `:219-226`; mid-phase route is post-merge target]. **Load-bearing status:** Load-bearing. **V3 augmentation:** Yes (line-anchor brittleness → CR-FM-04). **Closure clause leaned on:** F-05 "authorized widening" (validation-spec § 5.7 line 156). **Concession 2 (validation-spec § 15 line 416):** F-05 widens INV-03 surface beyond canonical anchor; anchor file absent locally per R-DOC-01. |
| **NFR-ME-3** | Auditability / Governance (No new HALT semantics in F1 — Load-bearing for NFR-INV-1) | ME-3 MUST be enforced at every F1-loop-touching change: no closure, audit, or extension may add a new HALT condition to the F1 loop tied to environment state. The five-state `git_status` matrix {clean, dirty, tool-absent, not-a-repo, error-other} (AC-ATK-02) MUST be specified such that {dirty, tool-absent, not-a-repo, error-other} all dispatch to warn-and-continue, NOT HALT. The input-invalid (HALT-permitted) vs environment-non-ideal (warn-continue-required) asymmetry distinction (AC-ATK-10) MUST be documented in the merged surface. ME-3 also binds the resume-time content audit per NFR-INV-4b: deprecated-surface content matches dispatch to warn-and-continue + one-shot ack, NOT HALT. | (1) `tests/skills/task/test_git_status_five_row_matrix.py` (to be authored) asserts each of the five `git_status` states dispatches per AC-ATK-02; (2) Code-review grep for any new `HALT`-equivalent disposition keyed off environment state; (3) AC-ATK-10 input-invalid-vs-environment-non-ideal asymmetry documented in the merged `task/SKILL.md` error-handling region; (4) Resume-time content audit per AC-ATK-18 dispatches warn-and-continue on deprecated-surface match. | Validation-spec § 2 line 62 (ME-3 load-bearing for INV-01); validation-spec § 4 line 106 (AC-ATK-18 resume-time content audit MUST be warn-and-continue per ME-3); validation-spec § 5.4 (F-03 dirty-tree-only — three other states unspecified pre-V3); validation-spec § 9 INV-01 row line 282 (V3 augmentation: 5-row matrix → AC-ATK-02); research-02 § A ME-3 row [CODE-VERIFIED for current ME-3 honor at `task/SKILL.md:104-117` (no env-state HALT) and `:170-179` (graceful-skip error handling); git-status pre-flight itself is post-merge TU-4 addition]. **Load-bearing status:** Load-bearing. **V3 augmentation:** Yes (5-row matrix → AC-ATK-02). **Closure clause leaned on:** F-03 dirty-tree warn-continue (validation-spec § 5.4 line 137). |
| **NFR-ME-4** | Auditability / Governance (HELD without per-row deltas — Ancillary) | ME-4 fences ancillary donor patterns that no F-01..F-08 finding re-opened during the merge analysis. No closure clause is leaned on directly; ME-4's role is to prevent the bucket-condensation arithmetic (validation-spec § 6.4 line 203, 79 → 65) from silently eliding ancillary patterns under "no per-row delta" framing. ME-4-fenced patterns MUST be enumerated in `transfer-manifest.md § 4` (currently present on disk; content audit owed per R-DOC-01) before the merge ships; until then the specific patterns ME-4 fences cannot be cited against the live donor file. | (1) `transfer-manifest.md § 4` ME-4 row enumerates the specific ancillary patterns fenced; (2) Design-review checklist row in PRD S21 confirms ME-4 enumeration matches research-02 § A ME-4 row once `transfer-manifest.md` is recovered or reconstructed; (3) Bucket-condensation arithmetic audit (against CR-DEP attacks per validation-spec § 6.4) confirms 79 → 65 reduction does not silently elide ME-4-fenced patterns. | Validation-spec § 2 line 63 (ME-4 ancillary collective with ME-5, ME-7, ME-8); validation-spec § 6.4 (bucket-condensation attack); research-02 § A ME-4 row. **Load-bearing status:** Ancillary — no closure clause leaned on; included for catalog completeness per task instruction. **Staleness:** [VALIDATION-SPEC-CITED][UNVERIFIED] — anchor source `transfer-manifest.md § 4` present on disk; content audit owed per R-DOC-01. |
| **NFR-ME-5** | Auditability / Governance (HELD without per-row deltas — Ancillary) | ME-5 fences ancillary donor patterns identically to ME-4 (collective treatment per validation-spec § 2 line 63). Same enumeration / verification obligation as NFR-ME-4 applies. ME-5's specific fenced patterns are named only in absent `transfer-manifest.md § 4`; until that artifact is recovered or reconstructed, the row stands as a catalog placeholder. | Same as NFR-ME-4: `transfer-manifest.md § 4` ME-5 row enumeration; design-review checklist confirmation; bucket-condensation arithmetic audit. | Validation-spec § 2 line 63 (collective with ME-4, ME-7, ME-8); research-02 § A ME-5 row. **Load-bearing status:** Ancillary — no closure clause leaned on; included for catalog completeness. **Staleness:** [VALIDATION-SPEC-CITED][UNVERIFIED]. |
| **NFR-ME-6** | Auditability / Governance (M1 atomicity — Load-bearing for commit-sequence shape protecting NFR-INV-1 / -3 / -4) | ME-6 MUST be enforced at commit time AND at push time: the seven foundation-row commits (validation-spec source-plan obligation #3) are mutually presupposing; landing them in separate commits leaves intermediate states that fail their own pre-commit gates and break either F1 progress (NFR-INV-1), rf-qa presence (NFR-INV-3), or resumability (NFR-INV-4). ME-6 is therefore atomicity at two layers: (i) commit-time pre-commit hook enforces gates per-commit; (ii) push-time server-side hook (AC-ATK-17) enforces the same gates on the landing commit at `master`, not on the working tree, preventing rebase-split bypass (`git rebase -i` permits commit-split; intermediate state passes commit-time pre-commit; push lands intermediate broken SHA). | (1) Existing `.pre-commit-config.yaml` continues to run pre-commit gates per-commit; (2) New `.github/workflows/push-policy.yml` (AC-ATK-17 implementation) re-runs the same gates on the landing commit at server side and rejects the push if the M1 atomicity contract is violated; (3) Test: rebase-split a foundation-row commit locally, push, confirm CI rejects; (4) `git diff origin/master..HEAD -- 'src/superclaude/cli/**' \| xargs grep -lE '/sc:task\b' \| grep -v '/sc:tasklist'` returns empty on landing commit. | Validation-spec § 2 line 64 (ME-6 load-bearing for foundation-row atomicity); validation-spec § 7.2 (Scenario H-2 rebase-split bypass — operational attack on ME-6); research-02 § A ME-6 row [CODE-VERIFIED: `.git/hooks/` contains only `*.sample` files; `.pre-commit-config.yaml` is commit-stage only per line 92 `default_stages: [commit]`; rebase-split bypass surface confirmed open]. **Load-bearing status:** Load-bearing (commit-sequence shape, indirect for INV-01 / -03 / -04). **V3 augmentation:** Yes (§ 7.2 H-2 → AC-ATK-17). **Closure clause leaned on:** Source-plan obligation #3 (atomic-commit). **Closure obligation:** AC-ATK-17 (server-side pre-push hook). |
| **NFR-ME-7** | Auditability / Governance (HELD without per-row deltas — Ancillary) | ME-7 fences ancillary donor patterns identically to ME-4 / ME-5 (collective treatment). Same enumeration / verification obligation as NFR-ME-4 applies. Specific fenced patterns named only in absent `transfer-manifest.md § 4`. | Same as NFR-ME-4. | Validation-spec § 2 line 63 (collective with ME-4, ME-5, ME-8); research-02 § A ME-7 row. **Load-bearing status:** Ancillary — no closure clause leaned on; included for catalog completeness. **Staleness:** [VALIDATION-SPEC-CITED][UNVERIFIED]. |
| **NFR-ME-8** | Auditability / Governance (HELD without per-row deltas — Ancillary) | ME-8 fences ancillary donor patterns identically to ME-4 / ME-5 / ME-7 (collective treatment). Same enumeration / verification obligation as NFR-ME-4 applies. Specific fenced patterns named only in absent `transfer-manifest.md § 4`. | Same as NFR-ME-4. | Validation-spec § 2 line 63 (collective with ME-4, ME-5, ME-7); research-02 § A ME-8 row. **Load-bearing status:** Ancillary — no closure clause leaned on; included for catalog completeness. **Staleness:** [VALIDATION-SPEC-CITED][UNVERIFIED]. |
| **NFR-ME-9** | Auditability / Governance (Donor-ceremony drop audit — Load-bearing for R-RULE-11 boundary protecting NFR-INV-4) | ME-9 MUST be enforced at the Step 5 commit (donor-body deletion) AND at the Step 6 post-commit residual-reference probe (CR-DEP-06): the 10 named donor-ceremony drops MUST remain dropped; no future contributor may silently re-introduce a donor-ceremony pattern without re-litigating its rejection in the manifest. The audit operates on two axes: (i) rejected-pattern axis (the 10 drops named in `transfer-manifest.md` — currently present on disk; content audit owed per R-DOC-01); (ii) surviving-citation axis (CR-DEP-06 residual-reference manifest across `.dev/releases/backlog/`, `docs/generated/`, `.dev/tasks/to-do/` — required for closure per research-04 § 5). rf-qa MUST be rebound at Step 6 pre-commit as F-07 chain-integrity verifier per AC-ATK-07. | (1) AC-ATK-07 names rf-qa as F-07 chain-integrity verifier at Step 6 pre-commit; (2) CR-DEP-06 residual-reference manifest produced at Step 6 post-commit with per-string disposition (LEAVE-AS-IS for backlog/generated docs, enumerate-per-task for `.dev/tasks/to-do/`, CR-DEP-05 fix-forward for `src/superclaude/cli/cleanup_audit/`); (3) Manifest scope per research-04 § 5.4; (4) `transfer-manifest.md` (when recovered or reconstructed) enumerates the 10 donor-ceremony drops; (5) Periodic re-grep against the manifest detects any silent re-introduction. | Validation-spec § 2 line 65 (ME-9 load-bearing for R-RULE-11); validation-spec § 6.1 (CR-DEP-03 attack on F-07 procedural authorization chain); validation-spec § 8 (CR-DEP-06 proposal — **elevated to REQUIRED** per research-04 § 5); research-02 § A ME-9 row [CODE-VERIFIED for residual-reference surface: 144 (task-brief authority) or 153 (live 2026-05-16 recount) `/sc:task` occurrences outside CR-DEP-05 scope]. **Load-bearing status:** Load-bearing (for R-RULE-11 boundary; indirect for INV-04). **V3 augmentation:** Yes (§ 8 → CR-DEP-06 / AC-ATK-18 companion). **Closure clause leaned on:** Source-plan Step 5 / Step 6 disposition (validation-spec § 6.1 line 184). **Closure obligations:** AC-ATK-07, AC-ATK-18 (CR-DEP-06 companion). **Concession 5 (validation-spec § 15 line 419):** F-07 chain is "not a manifest binding" — chain remains procedural; reviewer reading only `transfer-manifest.md` would not see the F-07 authorization. |

**ME NFR cross-reference summary:**

- **Load-bearing MEs (5 of 9):** NFR-ME-1, NFR-ME-2, NFR-ME-3, NFR-ME-6, NFR-ME-9. These rows carry stronger Definition-of-Done weight: each names a specific closure clause leaned on, a V3-augmentation flag where applicable, and an AC-ATK closure obligation. Downstream implementers MUST preserve these verbatim per validation-spec § 2 "defense overlay" framing.
- **Ancillary MEs (4 of 9):** NFR-ME-4, NFR-ME-5, NFR-ME-7, NFR-ME-8. These rows are catalog placeholders; their specific fenced patterns are named only in absent `transfer-manifest.md § 4` (R-DOC-01) and cannot be enumerated against the current donor file. The rows exist to prevent the bucket-condensation arithmetic from silently eliding them.
- **MEs with V3 augmentation:** NFR-ME-2, NFR-ME-3, NFR-ME-6, NFR-ME-9 (four of five load-bearing). NFR-ME-1 is V1/V2-sourced; V3 hardens it via § 5.3 predicate-precision attack.
- **Cross-INV protection map:** ME-1 → INV-05; ME-2 → INV-03; ME-3 → INV-01 (primary), INV-04 (Scenario B indirect); ME-6 → INV-01 / -03 / -04 (indirect via commit-shape); ME-9 → INV-04 (indirect via R-RULE-11).

---

### 14.9 NFR — Sequencing Constraints (NFR-S-1..NFR-S-3)

**Category basis:** All three rows are categorized as **Process / Sequencing & Atomicity** — sequencing constraints bind the operational ordering and atomicity properties of the merge timeline (Phase 5 commits, Phase 7.5 patch sprint, post-Step-6 residual sweep). Each row maps to a `compat-hazard-report.md` HZ-NN row that is currently `[VALIDATION-SPEC-CITED][UNVERIFIED]` (the report itself is present on disk; content audit owed per R-DOC-01); the operational mechanisms are independently verifiable from live evidence.

NFR-S-1 is **generalized** per task instruction to cover the live population: the validation-spec line 240 named target `TASK-PRD-20260514-121039` EXISTS in the working tree on 2026-05-16 (per fix-cycle 1 verification, `find .dev/tasks -iname '*121039*'` returns a match created 01:37 same date); its companion `TASK-TDD-20260514-121250` also EXISTS. The research-04 § 1.1 claim of zero matches was correct at research time but stale by synthesis time. Only `TASK-RF-20260515-195758` is genuinely absent. The generalization binds the constraint to **both the live named targets AND any other in-flight PRD/TDD task referencing donor surfaces** — supplement, not replace. The disposition MUST be surfaced as a `[POPULATION-GENERALIZED]` flag in S13 Open Questions per synth-01 cross-reference (re-named from `[STALE-CITATION-GENERALIZED]` because the named targets are partially current).

| NFR ID | Category | Statement | Verification Method | Source |
|---|---|---|---|---|
| **NFR-S-1** | Process / Sequencing & Atomicity (in-flight PRD precondition — **generalized**) | **[POPULATION-GENERALIZED]** — Any in-flight PRD/TDD task in `.dev/tasks/` whose body contains references to donor surfaces (`/sc:task`, `sc-task-protocol/`, `task-unified`) MUST complete before Step 5 of the merge (donor-body deletion), OR be explicitly snapshot-frozen with a decision record. The constraint binds **the live spec-named targets** (`TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250`, both verified present 2026-05-16 fix-cycle 1) **AND** any other in-flight PRD/TDD task referencing donor surfaces — supplement, not replace. `TASK-RF-20260515-195758` is genuinely absent. Live population is 132 union files across `.dev/tasks/` (2026-05-16). A `--max-wait 14d` default applies to each in-flight PRD/TDD: if the wait expires, the operator MAY auto-invoke "option (b)" (snapshot-freeze the in-flight task's `[CODE-VERIFIED]` tags at the SHA at expiry and proceed with merge). All `[CODE-VERIFIED]` tags written into research / synthesis / PRD files MUST carry a `(git-sha: <40-char>)` suffix to permit post-merge verification against the recorded SHA. The carrier surface for `--max-wait` is an Open Question per synth-01 (S13): candidates are (a) CLI flag on a future merge-orchestrator command, (b) task-frontmatter convention with watchdog, (c) operator-discipline-only. | (1) Pre-Step-5 grep `rg -l "/sc:task|sc-task-protocol|task-unified" .dev/tasks/to-do/ | grep -E 'TASK-(PRD|TDD)-'` enumerates the in-flight PRD/TDD population (live: includes 121039, 121250, and this PRD's own ID 20260516-004625); each must be "completed" or "snapshot-frozen with decision record" before Step 5 commit; (2) Snapshot-freeze decision records live as `.dev/releases/current/task-sc-task-directional-merge/decisions/SNAPSHOT-<task-id>.md` (or equivalent); (3) `[CODE-VERIFIED]` tag audit: grep research / synthesis / PRD body for `[CODE-VERIFIED]` and confirm an accompanying `(git-sha: ...)` suffix (or near-by SHA citation); (4) `--max-wait 14d` watchdog (per chosen carrier surface) fires at expiry; (5) CR-DEP-05 grep extension flags any post-Step-5 doc asserting verification against the stubified body without a pinned SHA. | Validation-spec line 240 (named target `TASK-PRD-20260514-121039` **live as of 2026-05-16 fix-cycle 1** — citation is partially current); validation-spec line 242-244 (S-1 mitigation text: `--max-wait` 14d default + auto-invoke option (b) + pinned git-SHA at every `[CODE-VERIFIED]` tag + CR-DEP-05 grep extension); validation-spec § 11.1 AC-ATK-08; research-04 § 1.1-1.4 (research-time absence claim — superseded). **Hazard mapped:** HZ-03 [VALIDATION-SPEC-CITED][UNVERIFIED] — `compat-hazard-report.md` present on disk; content audit owed per R-DOC-01. **Closure obligation:** AC-ATK-08. **Generalization flag:** [POPULATION-GENERALIZED] — synth-01 cross-reference for S13 Open Questions. **Concession 4 (validation-spec § 15 line 418):** S-1 mitigation hierarchy (a / b / c) is recorded but not decided; AC-ATK-08 deadline adds discipline but choice between (b) and (c) remains time-pressured at expiry. |
| **NFR-S-2** | Process / Sequencing & Atomicity (CLI runtime atomicity) | The commit that lands Step 5 of the merge (donor-body deletion in `sc-task-protocol/SKILL.md`) MUST be atomic with the commit that lands the CLI fix-forward (stubification / replacement of `/sc:task` emissions in `src/superclaude/cli/`). A server-side push-policy enforcer (AC-ATK-17) MUST re-run the atomicity check on the **landing commit at `master`**, NOT on the developer's working tree, to prevent `git rebase -i` from splitting Step 5 into intermediate SHAs where `task.md` is stubified but CLI sources still emit `/sc:task`. The grep target scope is `src/superclaude/cli/{sprint,cleanup_audit}/**` — the spec-original scope of `src/superclaude/cli/` named only `sprint/process.py` (line 170) but live evidence (research-04 § 2.2 + § 8) confirms `src/superclaude/cli/cleanup_audit/prompts.py` emits `/sc:task` at lines 26, 47, 69, 92, 116 (5 additional sites — 83% of CLI-layer exposure). The grep pattern MUST use word-boundary `/sc:task\b` to exclude `/sc:tasklist` substring false positives at `sprint/checkpoints.py:28` and `tasklist/prompts.py:158`. The hook venue MUST be CI-server-side (recommended: `.github/workflows/push-policy.yml`), NOT `.git/hooks/pre-push` (per-developer, bypassable via `git commit --no-verify` or local hook absence). | (1) `.github/workflows/push-policy.yml` (or equivalent CI check) authored and committed; check fires on every push (not only on PR merge) so bypass-resistance is structural; (2) Hook predicate: `git diff --name-only origin/master..HEAD -- 'src/superclaude/cli/**' \| xargs grep -lE '/sc:task\b' 2>/dev/null \| grep -v -- '/sc:tasklist'` returns empty on the landing commit OR the same commit also deletes the donor `task.md` body AND the recipient `task/SKILL.md` contains the absorbed TU-1..TU-8 markers; (3) Test fixture: synthetic rebase-split intermediate SHA pushed to a test branch → CI rejects; (4) Existing `tests/sprint/test_process.py:80-89` continues to assert post-stubification CLI prompt prefix; analogous `tests/cleanup_audit/test_prompts.py` SHOULD be authored (S13 Open Question per research-04 Q-4). | Validation-spec § 7.2 (Scenario H-2 / rebase-split bypass mechanism); validation-spec § 11.1 AC-ATK-17 (line 346 — server-side pre-push hook on landing commit); research-04 § 2.1-2.5 + § 6.2 + § 8 (fresh discovery of cleanup_audit emission sites). **Hazard mapped:** HZ-06 + HZ-07 [VALIDATION-SPEC-CITED][UNVERIFIED] — `compat-hazard-report.md` present on disk; content audit owed per R-DOC-01; mechanism independently verified from `.git/hooks/`, `.pre-commit-config.yaml:92`, `src/superclaude/cli/{sprint,cleanup_audit}/`. **Closure obligation:** AC-ATK-17. **Scope amendment:** [DIVERGENT vs spec] — research-04 § 2.5 + § 8 amends grep scope to `src/superclaude/cli/{sprint,cleanup_audit}/**`; PRD R-DIV-02 risk row. **V3 augmentation:** Yes (§ 7.2 H-2 mechanism + AC-ATK-17 server-side enforcement). |
| **NFR-S-3** | Process / Sequencing & Atomicity (Makefile sync-rule atomicity with flock) | `make sync-dev` and `make verify-sync` MUST acquire an exclusive `flock` on `.claude/skills/` (recommended lock-file: `.claude/skills/.sync-lock`, in-tree per research-04 Q-5) before iterating skill directories, and MUST release on exit. The `flock` discipline covers TWO races: (a) the **forward-looking prune-loop race** named in validation-spec § 7.3 — current `Makefile:108-151` `sync-dev` is copy-forward-only and does NOT yet prune (per research-04 § 3.2-3.3, [DIVERGENT] vs spec assumption); AC-ATK-16 `flock` MUST land BEFORE any future prune-semantics refactor; AND (b) the **live copy-overwrite race** — Session A's `cp` at `Makefile:121` can overwrite Session B's in-progress edit in a parallel worktree (authorized by `CLAUDE.md:194-205`); spec does not name this race but it is live in current code and MUST be covered by the same `flock`. A post-prune `find -type d` diff against an expected-set manifest (generated at the start of `sync-dev` from `src/superclaude/skills/*/`) MUST fail loud if directories present in `.claude/skills/*/` are absent from the expected set (or vice versa) — gated on prune-semantics existing; until then the diff serves as a copy-side drift detector. | (1) `Makefile:108-151` `sync-dev` and `Makefile:154-242` `verify-sync` wrap their respective loops in `flock -x .claude/skills/.sync-lock <command>`; (2) Parallel-worktree stress test: Session A `make sync-dev` and Session B simultaneous edit to `.claude/skills/<some-name>/SKILL.md` — Session B's edit survives or the operation blocks; (3) Post-prune dir-diff step at end of `sync-dev` compares `find .claude/skills/ -type d -mindepth 1 -maxdepth 1` against an expected-set manifest generated at start; (4) Documentation note in `Makefile` header or `CLAUDE.md` records "current sync semantics are copy-forward-only; prune semantics are a Phase 7.5 forward-looking change gated on `flock` discipline landing first." | Validation-spec § 7.3 (Scenario H-3 mechanism — forward-looking per research-04 § 3.2-3.3); validation-spec § 11.1 AC-ATK-16 (line 345 — `flock` discipline + post-prune dir-diff); research-04 § 3.1-3.4 + § 6.3. **Hazard mapped:** HZ-14 [VALIDATION-SPEC-CITED][UNVERIFIED] — `compat-hazard-report.md` present on disk; content audit owed per R-DOC-01; mechanism partially refined per research-04 § 3.3 (copy-overwrite race is live; prune race is forward-looking). **Closure obligation:** AC-ATK-16. **Scope refinement:** [DIVERGENT vs spec, forward-looking framing] — current `sync-dev` is copy-forward-only; PRD MUST document this explicitly; spec mitigation extended to cover live copy-overwrite race in addition to the named prune race. **V3 augmentation:** Implicit via § 7.3 / AC-ATK-16 authorship. |

**S NFR cross-reference summary:**

- **NFR-S-1 is generalized** per task instruction; the citation `TASK-PRD-20260514-121039` (validation-spec line 240) is now confirmed **partially current** (target exists on disk per 2026-05-16 fix-cycle 1) and surfaced as `[POPULATION-GENERALIZED]` for synth-01 inclusion in S13 Open Questions. The constraint binds **the live spec-named targets AND any other in-flight PRD/TDD task referencing donor surfaces** — supplement, not replace.
- **NFR-S-2 carries a fresh-discovery scope amendment** ([DIVERGENT vs spec]): `src/superclaude/cli/cleanup_audit/prompts.py` emits `/sc:task` 5 times (lines 26, 47, 69, 92, 116) and is not named in the validation spec. The spec's CLI scope is under-counted by 5/6 (83% of emission sites). PRD R-DIV-02 captures this; AC-ATK-17 grep scope MUST be amended to `src/superclaude/cli/{sprint,cleanup_audit}/**`.
- **NFR-S-3 carries a forward-looking framing refinement** ([DIVERGENT vs spec]): current `Makefile:108-151` `sync-dev` is copy-forward-only; the prune-loop race the spec attacks is forward-looking, but a copy-overwrite race is live and unaddressed by the spec mitigation as originally written. `flock` discipline MUST cover both.
- **All three S-rows are bound to `compat-hazard-report.md` HZ-NN rows** (HZ-03, HZ-06+HZ-07, HZ-14 respectively); the report is present on disk at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; rows are tagged `[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]` and rolled up under PRD R-DOC-01 (reframed: content audit owed against on-disk artifact bodies).

---

### 14.10 NFR Cross-References and MoSCoW Summary

### D.1 Cross-references TO this synthesis

- **synth-01 (Open Questions / S13):** receives `[STALE-CITATION-GENERALIZED]` flag for NFR-S-1; also receives the four S-1 Open Questions from research-04 § 1.4 (naming generalization, `--max-wait` carrier surface, pinned-SHA discipline, auto-invoke option (b) ambiguity), the Tier vocabulary reconciliation question (3-tier vs 4-tier — relevant to NFR-INV-5), the CR-FM-03 sunset condition question (relevant to NFR-INV-4b), the F-05 authorization manifestization question (relevant to NFR-INV-3 / NFR-ME-2), and the verifier-spawned F1 disposition question (relevant to NFR-INV-2).
- **synth-07 (Risk Analysis / S20):** receives R-DOC-01 (reframed at fix-cycle 2 — `extension-point-contracts.md`, `transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md` all PRESENT on disk at `.dev/releases/current/task-sc-task-directional-merge/artifacts/`; content audit owed), R-DIV-01 (96-file figure stale; live count is 132 union files at fix-cycle 2 / 130 at fix-cycle 1; the earlier research-03 25-file figure was a narrower-scope research-time snapshot), R-DIV-02 (CLI scope under-counted by 5/6); receives the five § 15 residual-risk concessions cross-referenced to anchor-dependent rows (Concessions 1 & 5 → R-DOC-01, Concessions 2 / 3 / 4 → AC-ATK closures).
- **synth-08 (Acceptance Criteria / S13 + Implementation Plan / S21):** receives AC-ATK-02 (5-row git_status matrix → NFR-ME-3), AC-ATK-05 (closed-enum per-item-marker consumers → NFR-INV-5 / NFR-ME-1), AC-ATK-07 (rf-qa as F-07 chain-integrity verifier → NFR-ME-9), AC-ATK-08 (S-1 enhancement → NFR-S-1), AC-ATK-10 (input-invalid-vs-environment-non-ideal asymmetry → NFR-INV-1 / NFR-ME-3), AC-ATK-11 (F-05 retroactive ME-10 vs one-time carve-out → NFR-INV-3 / NFR-ME-2 + nested-F1 disposition matrix → NFR-INV-2), AC-ATK-12 (CR-FM-03 sunset + CR-FM-01 canonicalization → NFR-INV-4b / NFR-INV-5), AC-ATK-13 (F-02 sentinel-comment ordering → NFR-INV-1), AC-ATK-16 (`flock` discipline → NFR-S-3), AC-ATK-17 (server-side pre-push hook → NFR-S-2 / NFR-ME-6), AC-ATK-18 (resume-time content-level audit + CR-DEP-06 manifest → NFR-INV-4b / NFR-ME-9).

### D.2 Priority (MoSCoW) and Definition-of-Done weight by NFR family

Per Synthesis Quality Review criterion 6, every NFR row carries a MoSCoW priority. The DoD weight column is retained as a sub-prioritization within the Must tier (where applicable) — MoSCoW answers "is this in scope for Phase 7.5" while DoD weight answers "how much closure rigor does this row demand inside Phase 7.5."

| Family | Priority (MoSCoW) | DoD weight | Rationale |
|---|---|---|---|
| NFR-INV-4b (semantic resumability) | **Must** | HIGHEST | Validation-spec § 9 line 285 "HIGHEST EXPOSURE" annotation; AC-ATK-18 + CR-DEP-06 elevation; live in-flight exposure target TASK-RESEARCH-20260403-sprint-task-exec (48 donor-surface refs across 10 files in subtree, 2026-05-16 fix-cycle 1 live recount, status Doing). |
| NFR-INV-1, NFR-INV-3 (F1 progress, rf-qa floor) | **Must** | HIGH | Code-verifiable in current `task/SKILL.md`; closure obligations have explicit ACs (AC-ATK-02 / -10 / -13 for INV-01; AC-ATK-07 / -11 for INV-03). Load-bearing for merge correctness. |
| NFR-INV-4a (parse resumability) | **Must** | HIGH | Mechanically testable via fixture iteration; CR-FM-03 shim is the foundation that NFR-INV-4b sits atop. Foundation-row for resumability. |
| NFR-INV-2 (F2 catalog additivity) | **Must** | MEDIUM-HIGH | Self-enforcing at parse-level (diff); semantic wrinkle is nested-F1 disposition matrix (AC-ATK-11). Catalog-additivity is contract; Must-do. |
| NFR-INV-5 (refusal-of-definition) | **Must** | MEDIUM-HIGH | Protects a feature surface not yet in code; binds post-merge design intent; AC-ATK-05 closed-enum is operationally critical. Must-do to prevent per-item dispatch creep. |
| NFR-ME-1, -2, -3, -6, -9 (load-bearing MEs) | **Must** | HIGH | Each anchors an INV or commit-shape; closure obligations bound by AC-ATKs above. Load-bearing — Must-do. |
| NFR-ME-4, -5, -7, -8 (ancillary MEs) | **Should** | LOW-MEDIUM | Catalog placeholders pending `transfer-manifest.md` recovery; included for catalog completeness. Not Must (no closure clause leans on them); not Could (deliberate fence against bucket-condensation arithmetic). Should-do if `transfer-manifest.md` recovers in time; otherwise carry as placeholder rows. |
| NFR-S-1 (generalized in-flight PRD/TDD precondition) | **Must** | HIGH | Two named targets (`TASK-PRD-20260514-121039`, `TASK-TDD-20260514-121250`) live on disk plus this PRD itself plus the broader 132-file in-flight population; H-1 scenario condition is live for multiple tasks; Must-do precondition for Step 5. |
| NFR-S-2 (CLI runtime atomicity) | **Must** | **CRITICAL** | H-2 scenario is the most concrete operational hazard; six emission sites; no server-side hook today; bypass-resistant CI check is the structural barrier. Highest within-Must DoD weight. |
| NFR-S-3 (Makefile sync-rule atomicity) | **Should** | MEDIUM | Forward-looking for prune-loop race (no prune semantics today); live for copy-overwrite race; `flock` discipline is small lift but ordering-critical (must precede prune-semantics refactor). Should-do for Phase 7.5; promotion to Must triggers when a prune-semantics refactor is scoped. |

**Per-NFR MoSCoW assignment table (companion to §A/§B/§C row tables; assembler MAY ingest this as the Priority (MoSCoW) column when consolidating into PRD §14):**

| NFR ID | Priority (MoSCoW) | Reason |
|---|---|---|
| NFR-INV-1 | Must | F1 progress monotonicity invariant — contractual |
| NFR-INV-2 | Must | F2 catalog additivity invariant — contractual |
| NFR-INV-3 | Must | rf-qa floor invariant — contractual |
| NFR-INV-4a | Must | Parse-level resumability — foundation for 4b |
| NFR-INV-4b | Must | Semantic resumability — HIGHEST EXPOSURE per § 9 line 285 |
| NFR-INV-5 | Must | Refusal-of-definition for `Tier:` — contractual |
| NFR-ME-1 | Must | Load-bearing for INV-05 |
| NFR-ME-2 | Must | Load-bearing for INV-03 |
| NFR-ME-3 | Must | Load-bearing for INV-01 |
| NFR-ME-4 | Should | Ancillary catalog placeholder (no closure clause leaned on; pending `transfer-manifest.md` recovery) |
| NFR-ME-5 | Should | Ancillary catalog placeholder |
| NFR-ME-6 | Must | Load-bearing for commit-sequence shape (INV-01/-03/-04) |
| NFR-ME-7 | Should | Ancillary catalog placeholder |
| NFR-ME-8 | Should | Ancillary catalog placeholder |
| NFR-ME-9 | Must | Load-bearing for R-RULE-11 boundary (indirect INV-04) |
| NFR-S-1 | Must | Live in-flight PRD/TDD precondition — H-1 condition live across multiple tasks |
| NFR-S-2 | Must | CLI runtime atomicity — H-2 most concrete hazard, CRITICAL DoD weight |
| NFR-S-3 | Should | Makefile sync-rule atomicity — forward-looking prune race; live copy-overwrite race; promotion to Must triggers when prune semantics scoped |

**MoSCoW distribution:** Must = 13 (NFR-INV-1, -2, -3, -4a, -4b, -5; NFR-ME-1, -2, -3, -6, -9; NFR-S-1, NFR-S-2 — counting INV-4 split as two sub-rows); Should = 5 (NFR-ME-4, -5, -7, -8; NFR-S-3); Could = 0; Won't = 0. Justification for Could/Won't being empty: every NFR in this synthesis pairs with either an invariant whose preservation is contractual (Must) or with a fenced ancillary pattern preserved for catalog completeness (Should). No NFR row in scope is a nice-to-have or a deliberately deferred surface; deferred items live in synth-08 S21 Could/Won't backlog instead. The four ancillary ME rows are Should rather than Must because their statement clauses are deliberately minimal (no closure clause leaned on per validation-spec § 2 line 63 collective ancillary treatment); the NFR-S-3 row is Should rather than Must because the named prune-loop race is forward-looking (current `sync-dev` is copy-forward-only per research-04 § 3.2-3.3).

### D.3 Stale-citation and divergence flags applied in this synthesis

| Flag | Rows affected | Disposition |
|---|---|---|
| `[POPULATION-GENERALIZED]` | NFR-S-1 | Generalize to live named targets (`TASK-PRD-20260514-121039` + `TASK-TDD-20260514-121250` both verified present 2026-05-16) PLUS the broader 132-file in-flight population; surface in S13 Open Questions via synth-01. |
| `[VALIDATION-SPEC-CITED][UNVERIFIED]` | NFR-INV-1..5 (anchor); NFR-ME-4, -5, -7, -8 (transfer-manifest); NFR-S-1, -2, -3 (compat-hazard-report HZ-NN) | Roll up to R-DOC-01 in S20 Risk Analysis per synth-07. |
| `[DIVERGENT]` (live evidence contradicts spec) | NFR-INV-4b (96 → 132 union files — UNDER-count, direction inverted from synthesis-time figure); NFR-S-2 (CLI scope under-counted by 5/6); NFR-S-3 (sync-dev is copy-forward-only, not prune-and-replace) | Roll up to R-DIV-01 (file-count drift; direction corrected to GROWTH) and R-DIV-02 (CLI scope amendment) in S20 per synth-07; NFR-S-3 framed as forward-looking refinement. |
| `[CODE-VERIFIED]` | NFR-INV-1 (`task/SKILL.md:79-98` + `:104-117`); NFR-INV-2 (`task/SKILL.md:104-117`); NFR-INV-3 (`task/SKILL.md:191-198` + `:219-226`); NFR-INV-4a (F1 parse-blindness at `:79-98, 269-282`); NFR-ME-6 (`.git/hooks/` sample-only + `.pre-commit-config.yaml:92` commit-stage); NFR-S-2 (CLI emission sites); NFR-S-3 (`Makefile:108-242` no `flock`, copy-forward-only) | Standard tag; no roll-up required. |

---

---

## 15. Technology Stack

### 15.1 Stack-of-record (only what touches the merge)

Per S15 template (`src/superclaude/examples/prd_template.md:640-669`), the merge has no backend / frontend / infrastructure tiers in the traditional product sense — it is a textual / file-layout refactor of MDTM artefacts plus a small CLI / Makefile / hook surface. The table below is scoped to **components that the merge actually touches**.

| Layer | Technology | Version | Notes / Evidence |
|---|---|---|---|
| Authoring runtime | Python | ≥ 3.10 | Project requirement; `make dev` editable install. UV is the only sanctioned invocation per `CLAUDE.md`. |
| Skill / task substrate | MDTM (YAML frontmatter + Markdown body) | n/a (in-repo convention) | TU-1 introduces `Tier:` field in frontmatter. `src/superclaude/skills/task/SKILL.md:1-4` `[CODE-VERIFIED]` (frontmatter lists `name` + `description` only — no `Tier:`); `:65-73` `[CODE-VERIFIED]` ("Validating the Task File" requires `id`, `title`, `status`, `created_date`, no `Tier:`). |
| Sprint CLI runtime | Python module `src/superclaude/cli/sprint/` | live | Emits `/sc:task` prompt at `src/superclaude/cli/sprint/process.py:170` `[CODE-VERIFIED]`. Pinned by `tests/sprint/test_process.py:80-89` (`prompt.startswith("/sc:task ")`) `[CODE-VERIFIED]`. Step-5 stubification flips this to `/task ...`. |
| Cleanup-audit CLI runtime | Python module `src/superclaude/cli/cleanup_audit/` | live | **Fresh discovery (research 04 §2.5, §8)**: emits `/sc:task` 5× at `src/superclaude/cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116` `[CODE-VERIFIED]` — **NOT named in `validation-spec.md` § 7.2**. PRD scope amendment required (R-DIV-02). |
| Test framework | pytest (auto-loaded via `superclaude` plugin entry-point) | ≥ 7.0.0 | TU-5 baseline collection candidate per donor `src/superclaude/skills/sc-task-protocol/SKILL.md:146` `[CODE-VERIFIED]` (`uv run pytest --collect-only -q`). |
| Sync / dev-mirror build | GNU make | n/a | `Makefile:108-151` (`sync-dev`) and `Makefile:154-247` (`verify-sync`) `[CODE-VERIFIED]`. Currently **copy-forward-only**; no `flock`; no prune step. AC-ATK-16 surface. |
| Pre-commit hook framework | `pre-commit` | per `.pre-commit-config.yaml` | `default_stages: [commit]` at `.pre-commit-config.yaml:92` `[CODE-VERIFIED]`; **no pre-push stage** (`grep -in 'pre-push\|prepush' .pre-commit-config.yaml` returns empty). |
| Git hooks (active) | none | n/a | `find .git/hooks/ -type f ! -name '*.sample'` returns empty; only 14 `*.sample` files `[CODE-VERIFIED]` (verified 2026-05-16). AC-ATK-17 venue must be authored. |
| Lock primitive (planned) | `flock(1)` (util-linux) | system | Not present anywhere in `Makefile` today (`grep -n flock Makefile` empty) `[CODE-VERIFIED]`. AC-ATK-16 addition: `flock -x .claude/skills/.sync-lock <cmd>`. |
| Audit-grep primitive | `grep -E` (POSIX) and/or `rg` (ripgrep) | system | All CR-FM-NN sentinel / ordering greps use POSIX ERE with word-boundary `\b`. `rg` is the developer-preferred runtime for `.dev/tasks/` corpus scans (research 03 §1 invocation). |
| Push-policy enforcer (planned) | GitHub Actions workflow `.github/workflows/push-policy.yml` | greenfield | Authored at Phase 7.5 per AC-ATK-17 plan (research 04 §6.2 + §7). Runs on every push, not just PR-merge, to defeat rebase-split bypass (H-2). |

### 15.2 Surfaces explicitly out of scope for this PRD

| Surface | Why out of scope |
|---|---|
| Backend services, databases, caches, queues | None exist — the merge is a textual / file-layout refactor. |
| Frontend frameworks, UI tooling | No UI surface; see S24. |
| Container / orchestration / monitoring | The merge changes no deployment topology. |
| Tier-renames inside `src/superclaude/commands/task.md` body line ranges other than `:50-67, 69-91, 93-100` | Out of TU-1..TU-8 catalog; tracked separately as CR-DEP-01 stubification target (research 01 Gaps #7). |

---

### 15.3 Impacted Surfaces (Cross-Cut)

Key impacted files (also enumerated under S14 FR rows and S24 design map):

- `src/superclaude/skills/task/SKILL.md` (recipient — TU-1..TU-8 absorbed)
- `src/superclaude/skills/sc-task-protocol/SKILL.md` (donor — stubified Step 5; hard-deleted Step 6)
- `src/superclaude/commands/task.md` (command file — stubified)
- `src/superclaude/cli/sprint/process.py:169-170` (sprint emitter — re-routed)
- `src/superclaude/cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116` (cleanup-audit emitters — re-routed; AC-ATK-17 grep scope MUST cover this file)
- `Makefile:108-247` (sync-dev / verify-sync — `flock` discipline AC-ATK-16)
- `.github/workflows/push-policy.yml` (greenfield — AC-ATK-17 server-side hook)

---



---

> **Feature-PRD abbreviation:** Section 16 is abbreviated per FEATURE-PRD discipline — only Section 16.2 (Core User Flows) is fully populated. Section 16.1 (Onboarding), 16.3 (Accessibility), and 16.4 (Localization) are marked N/A with rationale per template SCOPE NOTE for Feature PRDs. Platform-level UX requirements live in the Platform PRD.

## 16. User Experience Requirements

### 16.1 Onboarding Experience — N/A

**Rationale.** This release is a directional merge of an internal skill / command pipeline. No new end-user product surface ships; no first-run flow exists. Onboarding metrics (time-to-onboarding, activation rate) are platform-level concerns owned by the SuperClaude framework PRD, not by this merge. Per the prd_template S16 SCOPE NOTE, feature-PRDs reference the Platform PRD for onboarding rather than restate it.

### 16.2 Core User Flows

Five flows are load-bearing for this merge. Each maps to verifiable post-merge behavior in `src/superclaude/skills/task/SKILL.md` and/or `src/superclaude/commands/task.md`. Citations are to research-01 (transfer-units catalog) and research-03 (in-flight exposure).

| Flow | Steps | Success Criteria |
|------|-------|------------------|
| **F-16.2.1 — Tier classification UX** | 1. Operator invokes `/task <file>` (post-merge name). 2. Command file emits the MANDATORY FIRST OUTPUT classification header (TEXT-ONLY, HTML-comment schema, one of `{STRICT, STANDARD, LIGHT, EXEMPT}`) BEFORE skill invocation. 3. Command file reads frontmatter `Tier:` field (CR-FM-03 default-fall-through to STANDARD if absent — see CR-FM-03 sunset binding in S23). 4. `path_override_check()` evaluates FIRST (row 1 ordering per CR-7 ORDERING sentinel; `auth/`, `security/`, `crypto/`, `models/`, `migrations/` → CRITICAL; `*.md`, `docs/`, `*test*.py` → trivial skip). 5. `tier_field_validate()` runs. 6. `gate_1_dispatch()` routes to STRICT / STANDARD / LIGHT / EXEMPT execution path. | Header appears as first output; tier value is one of the canonical four; path-override-bound tier supersedes frontmatter tier; F1 loop entered with correct routing. Verified by F-02 grep at row 1 ordering and AC-SM-08 zero-diff invocation count. (research-01 TU-1, TU-2.) |
| **F-16.2.2 — F1 loop transparency** | 1. F1 executor reads task file. 2. Pre-loop steps emit visible Task Log lines: `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<N> sunset_row_authored=<bool>` and `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` (the latter only if AC-ATK-18 resume-time grep matches). 3. Pre-F1 `git status` emits a Task Log line bound to one of five dispositions `{clean, dirty, tool-absent, not-a-repo, error-other}` per CR-TASK-06, each mapped to `{WARN-CONTINUE, GRACEFUL-SKIP}` — never HALT. 4. STRICT entry writes baseline snapshot to `${TASK_DIR}/research/test-baseline.yaml` (on-disk; survives session boundary). 5. F1 iterates: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. Each phase boundary emits a checkpoint line. 6. On test failure inside STRICT/STANDARD: TFEP escalation trigger detection per S23 below. | Every gate decision is visible in the Task Log; no silent state mutation; baseline YAML exists on disk before first execution step; INV-01 monotonicity preserved (no in-flight HALT). (research-01 TU-1, TU-4, TU-5; research-03 §3.) |
| **F-16.2.3 — Resumability behavior** | 1. Resumed-task author opens an in-flight task (e.g., one of the 132 live union files referencing donor surfaces — 2026-05-16 fix-cycle 1 live recount of `.dev/tasks/`, `rg -l "/sc:task|sc-task-protocol|task-unified" .dev/tasks/ | wc -l`; supersedes earlier 25-file research-03 §6 narrower-scope snapshot). 2. Skill performs L1 schema-parse: frontmatter parses; `Tier:` field absent → CR-FM-03 shim assigns STANDARD. 3. L2 semantic-content scan: AC-ATK-18 resume-time grep runs recursively over (a) task body, (b) `research/`, `synthesis/`, `qa/` siblings in subtree, (c) `find`-traversal of paths named in `related_docs:` frontmatter. Matches on `(/sc:task\b\|sc-task-protocol\|task-unified)` emit `gate-1.5: legacy-surface-reference detected`. 4. Operator sees one-shot acknowledgment gate (first-resume-only confirmation; subsequent resumes do not re-prompt unless task content changes). 5. Disposition: WARN-CONTINUE only — never HALT (ME-3, INV-01). 6. L3 execution: if a subagent later attempts `Read` on a deleted donor path or spawns a `/sc:task` invocation, the F1 loop transitions the task to `⚪ Blocked` per its own exception clauses (INV-01 holds by transition; INV-04 semantic guarantee broken — see S23 H-4 row). | All 132 live in-flight files parse cleanly at L1; resume-time grep correctly surfaces the surviving named-exposure target (`TASK-RESEARCH-20260403-sprint-task-exec` with **48 donor-surface occurrences across 10 files** in subtree, 2026-05-16 fix-cycle 1 recount); acknowledgment gate is one-shot per file; no false-HALTs. (research-03 §3, §4, §6 [research-time]; fix-cycle 1 live recount 2026-05-16.) |
| **F-16.2.4 — Deprecation messaging on stubified `/sc:task` invocation** | 1. Post-Step-5 (CR-DEP-01 stubification), an operator or subagent invokes `/sc:task <file>` against the now-stubified command surface. 2. The stub does NOT execute the F1 loop. 3. The stub emits a deprecation message (suggested text below) directing the caller to the canonical `/task` surface and to CR-FM-03 for tier-field migration. 4. The stub exits cleanly (no error code; warn-and-continue semantics so any tooling that scrapes for an exit status sees success). 5. Post-Step-6 (CR-DEP-03 hard-delete), the same invocation hits a missing file; behavior depends on the shell / harness layer and is out-of-scope for the stub itself, but the residual-reference manifest from CR-DEP-06 should have already eliminated all known call sites. | Deprecation message is emitted exactly once per invocation; canonical text is stable across stub lifetime; no false-positive HALT; CR-FM-03 shim sunset audit row (CR-AUDIT-FM-03-SUNSET) is referenced in the message for forward-looking guidance. (research-01 TU-1; research-03 §5.) |
| **F-16.2.5 — Incident-report file format** | 1. F1 executor encounters a TFEP escalation trigger (per S23 below). 2. After resolution (success OR escalation-exhausted FULL STOP), the executor writes a side-effect file `tfep-incident-report.md` to a stable location (recommended: `${TASK_DIR}/tfep/tfep-incident-report.md` to parallel `${TASK_DIR}/reviews/qa-phase-[N]-report.md`; final location bound by post-merge assembler decision). 3. File contains the seven-field schema enumerated below. 4. The incident report is committed to git alongside other forensic artifacts. 5. No in-task heading is inserted into the parent TASK-* file (INV-04 — would mutate task body). | The file exists on disk after TFEP completion; the seven fields are all present and non-empty; the file survives session boundaries; downstream tools parsing `${TASK_DIR}` see the new artifact at a stable path; INV-04 holds. (research-01 TU-8.) |

#### 16.2.4 — Suggested deprecation message text

The stubified `/sc:task` surface should emit a message with this shape (operator may adjust verbatim wording during Step 5 authoring, but the seven-element structure is load-bearing for AC-ATK-18 detection):

> ```
> [DEPRECATED] /sc:task has been merged into /task as of <Step-5-merge-date>.
>
> What to do:
>   - Invoke /task <task-file> instead. The behavior is equivalent for
>     STANDARD/STRICT tiers; LIGHT and EXEMPT tiers follow the canonical
>     vocabulary {STRICT, STANDARD, LIGHT, EXEMPT}.
>   - Existing MDTM task files without a `Tier:` frontmatter field will
>     default-classify to STANDARD via the CR-FM-03 compatibility shim
>     (sunset binding: CR-AUDIT-FM-03-SUNSET — see release notes).
>   - For residual references in synthesis/research prose, see the
>     CR-DEP-06 residual-reference manifest.
>
> Reference: src/superclaude/skills/task/SKILL.md and src/superclaude/commands/task.md.
> No action will be taken by this stub. Exit: 0.
> ```

Seven load-bearing elements: (1) `[DEPRECATED]` prefix, (2) merge-date placeholder, (3) replacement invocation guidance, (4) canonical tier vocabulary statement, (5) CR-FM-03 default-fall-through behavior, (6) CR-FM-03 sunset binding pointer, (7) CR-DEP-06 residual-reference manifest pointer. Exit code 0 is mandatory (warn-and-continue per ME-3).

#### 16.2.5 — Incident-report seven-field schema

Per TU-8 (research-01) and AC-ATK-12 enumeration obligation:

| # | Field | Purpose | Example value |
|---|---|---|---|
| 1 | **Trigger** | Which TFEP escalation trigger fired (one of: pre-existing test fails, 3+ new tests fail, runtime exception in implementation code, escalation gradient bullet) | `pre-existing-test-failure: tests/pm_agent/test_confidence.py::test_assess_high` |
| 2 | **Escalation count** | Which rung of the gradient was reached (1 = tier-light triage ~5–8K tokens; 2 = tier-standard ~15–20K tokens; 3 = FULL STOP) | `2` |
| 3 | **Failing tests** | Full list of failing test names + pre-existing-vs-new classification (driven by `${TASK_DIR}/research/test-baseline.yaml`) | `tests/pm_agent/test_confidence.py::test_assess_high (pre-existing)` |
| 4 | **Root cause** | Single-sentence summary from forensic subagent; cites the file:line of the underlying defect | `confidence.py:142 returns 0.65 when context lacks 'has_official_docs'` |
| 5 | **Solution** | What was changed (commit SHA + file list) OR "no change — test expectations were wrong" if adversarial outcome was `failed` (test_is_wrong case rolled into the donor `failed` enum value) | `commit abc1234; src/superclaude/pm_agent/confidence.py` |
| 6 | **Outcome** | One of `{success / escalated / failed}` — donor-verbatim enum from `src/superclaude/skills/sc-task-protocol/SKILL.md:232` `[CODE-VERIFIED 2026-05-16 fix-cycle 1]`. Fix-cycle 1 finding: earlier synth-06 enum `{resolved, escalated-FULL-STOP, test_is_wrong-presented-to-user}` drifted from donor; corrected to donor literal. Operator UI MAY render long-form glosses but persisted value MUST be the donor literal. | `success` |
| 7 | **Forensic artifacts** | Paths to forensic subagent prompts, traceback dumps, adversarial-validation reports (anything the subagent emitted) | `${TASK_DIR}/tfep/forensic-prompt-1.md; ${TASK_DIR}/tfep/traceback-1.log` |

**Open Question (Q-S13).** Per research-01 Gap #2, the spec line counts a "seven-field schema" and the donor literal at `sc-task-protocol/SKILL.md:225-233` lists 7 bullet rows (one per field: Trigger / Escalation count / Failing tests / Root cause / Solution / Outcome / Forensic artifacts) — verified 2026-05-16 QA pass. The file-header line `# TFEP Incident Report` at line 225 is NOT counted. AC-ATK-12 mandates a definitive enumeration; the table above adopts the donor-aligned 7-field reading. Engineering lead to confirm at PRD assembly.

### 16.3 Accessibility Requirements — N/A

**Rationale.** No human-facing GUI / web / native UI ships. The merge operator and resumed-task author interact via terminal text output (Task Log lines, stub deprecation messages, F1 checkpoint markers). WCAG / screen-reader / color-contrast standards apply to visual UIs and are not relevant to text-only command output. Standard terminal-accessibility patterns (no required color encoding, no required cursor positioning, no required ANSI escape interpretation) are followed by default because Task Log lines are plain-text emissions parseable by any line-buffered consumer.

### 16.4 Localization Requirements — N/A

**Rationale.** All artifacts in this merge (SKILL.md files, command files, MDTM task files, incident-report schema, deprecation messages, audit-row identifiers like CR-FM-03 / CR-DEP-01 / AC-ATK-18) are English-only and operate inside the SuperClaude developer-tooling layer. Localization is not in scope for v4.x; if introduced at v5.x or later it will be owned by the Platform PRD per template SCOPE NOTE.

---

---

## 17. Legal & Compliance Requirements

> **Feature-PRD abbreviation.** Regulatory framework (GDPR, CCPA, SOC 2), corporate data-handling posture, and terms-of-service / privacy-policy artifacts live in the SuperClaude **Platform PRD**. This S17 covers only the **feature-specific data handling** introduced by the merge.

### 17.1 Feature-Specific Data Handling

The directional merge introduces exactly one new on-disk data file: the **`tfep-incident-report.md` file format**, written by CR-TASK-10 (F1 loop-body incident emit) at the per-task task-files directory. Schema is intentionally minimal.

**Schema — seven fields (AC-ATK-12(b) closure obligation; donor-aligned per `src/superclaude/skills/sc-task-protocol/SKILL.md:227-233` `[CODE-VERIFIED]`):**

| Field | Type | Purpose |
|---|---|---|
| `Trigger` | string (one-line) | Which TFEP escalation trigger fired (e.g. "pre-existing test failure", "3+ new tests fail", "runtime exception in implementation code", "escalation gradient threshold crossed") |
| `Escalation count` | integer (1..3) | Donor escalation ladder rung: 1=tier-light triage, 2=tier-standard, 3=FULL STOP (donor `:238-244`) |
| `Failing tests` | newline-delimited list | Pytest nodeids that triggered the incident, with pre-existing-vs-new classification driven by `${TASK_DIR}/research/test-baseline.yaml` |
| `Root cause` | multi-line | Forensic analysis from Step 3 invocation; must reference baseline-snapshot classification |
| `Solution` | string | Remediation plan synthesized in Step 5 ("Failure Remediation Plan (Adjudicated)" heading per donor `:207-212`) |
| `Outcome` | enum `{success / escalated / failed}` (donor-verbatim per `src/superclaude/skills/sc-task-protocol/SKILL.md:232` `[CODE-VERIFIED 2026-05-16 fix-cycle 1]`) | Matches Step 4 (donor `:200-205`) status-branching outcome. Fix-cycle 1 correction: earlier synth-08 enum `{resolved, escalated-to-FULL-STOP, deferred-with-decision-record}` drifted from donor literal; normalized to donor form. Operator UI MAY render long-form glosses (`success` → "resolved", `escalated` → "escalated to FULL STOP", `failed` → "failed / deferred with decision record"); persisted value MUST be donor literal. |
| `Forensic artifacts` | newline-delimited list of paths | At minimum the forensic invocation's structured-output file and any test-rerun logs |

**Status:** Schema field-names enumerated per **AC-ATK-12(b)** closure obligation (validation-spec § 11.1 line 341). Aligned verbatim with donor literal at `src/superclaude/skills/sc-task-protocol/SKILL.md:227-233` (seven bullet rows), Outcome enum aligned to donor literal at `:232`. Cross-section consistency: matches synth-05 §25.2 and synth-06 §F-16.2.5 schema enumeration (all three normalized to donor enum at fix-cycle 1 2026-05-16). `[SPEC-DEFINED][CODE-VERIFIED]`

### 17.2 No PII Statement

The `tfep-incident-report.md` schema contains **no personally identifiable information (PII)** by construction. Field types are explicitly bounded to (a) machine timestamps, (b) MDTM task identifiers (synthetic), (c) F1 step names from a fixed enum, (d) incident-class enums, (e) framework-internal evidence pointers, and (f) framework-internal log references. No user names, email addresses, IP addresses, hostnames, or free-form user-supplied content are collected. The file lives entirely in the per-task `.dev/tasks/` tree on the developer's local workstation; nothing is transmitted off-device.

### 17.3 Platform Context Cross-Reference

For the platform-wide privacy posture, retention policy, regulatory mapping, and corporate compliance program, see the SuperClaude **Platform PRD § 17**. This Feature PRD inherits the platform's no-PII / local-only data posture and adds the `tfep-incident-report.md` schema as the sole feature-specific data artifact.

---

---

## 18. Business Requirements

> **Feature-PRD abbreviation.** Monetization strategy, go-to-market plan, support tiering, and pricing live in the SuperClaude **Platform PRD § 18**. This S18 records only the **Phase 7.5 patch-sprint engineering effort cost** introduced by the merge's predicate-precision closure work.

### 18.1 Phase 7.5 Patch-Sprint Effort Cost

Validation-spec § 16 line 435 enumerates the Phase 7.5 patch sprint as **21 changes**:

| Bucket | Count | Items |
|---:|---:|---|
| AC-ATK gap-closure rows | 18 | AC-ATK-01..18 (predicate-precision + V3 security-probe overlay) |
| Proposed audit row | 1 | CR-DEP-06 (post-Step-6 residual-reference manifest) |
| Sequencing-constraint additions | 2 | S-4 PRD timeout (`--max-wait` 14d default per AC-ATK-08); S-5 rebase-ban (server-side pre-push hook per AC-ATK-17) |
| **Total** | **21** | — |

### 18.2 Rough Engineering-Effort Estimate (ranges)

These are coarse engineer-day ranges intended for capacity planning only. Detailed RICE scoring lives in § 21.2; the timeline lives in § 21.5.

| Workstream | Effort range (engineer-days) | Notes |
|---|---:|---|
| AC-ATK mechanical (-09 sha256 swap; -03/-10 table authoring; -04 condensation table) | 2–4 | Largely mechanical; substitution + re-baseline |
| AC-ATK predicate-precision (-01, -02, -05, -06, -07, -11, -12, -13, -14, -15) | 6–10 | Spec / audit-row / fixture authoring + small Python/CLI hooks |
| AC-ATK V3 security-probe (-16 flock + dir-diff; -17 pre-push hook; -18 CR-FM-03 content audit + CR-DEP-06 manifest + gate-1.5) | 4–7 | New scripts + CI integration |
| AC-ATK V3-augmented (-08 `--max-wait` + pinned-SHA + grep extension) | 1–2 | Argument plumbing + commit-time SHA capture |
| CR-DEP-06 manifest emitter | 1–2 | One-shot Python script + manifest schema |
| S-4 PRD timeout (encompassed by AC-ATK-08) | 0.5 | Plumbing only |
| S-5 rebase-ban server-side hook (encompassed by AC-ATK-17) | 1–2 | Pre-push hook + CI mirror |
| **Subtotal — implementation** | **15.5–27.5** | — |
| Reviewer adversarial pass + rf-qa spawning per Step 6 (AC-ATK-07) | 2–4 | Includes pre-commit gate authoring |
| Documentation + sync + verify-sync runs | 1–2 | Per CLAUDE.md component-sync discipline |
| **Total Phase 7.5 patch-sprint** | **18.5–33.5 engineer-days** | Range reflects estimation uncertainty, not a commitment |

**Note on residuals.** Per research-06 § 5, the 21-change Phase 7.5 scope **does not close** the FM-NN class (FM-01, -02, -03, -04, -05, -07 fully open; FM-06, -08 partial), EC-01, or § 12 tradeoffs F-01/F-04/F-06/F-08. These are surfaced as accepted residuals in S10 Assumptions and S20 Risk Register. Expanding the patch sprint to absorb them (Phase 7.5.b) would add an estimated 5–10 engineer-days; this expansion is an open question for the engineering lead (see synth-07).

### 18.3 Platform Context Cross-Reference

For monetization model, customer-acquisition strategy, support tiering, and revenue targets, see the SuperClaude **Platform PRD § 18**. This Feature PRD inherits the platform's OSS-with-optional-paid-tier model; the directional merge is a maintenance investment chargeable to the platform's framework-quality budget line.

---

---

## 19. Success Metrics & Measurement

This section is written in full because all KPIs below are **feature-specific** to the `/sc:task` → `/task` directional merge. Each KPI is anchored to an AC-ATK / AC-SM / CR-DEP / verify-sync / audit-outcome citation in the validation-spec and research inputs. KPI categories follow the prd_template.md S19 convention (Product / Business / Technical).

### 19.1 KPI Table

| # | Category | KPI | Target | Measurement Method |
|---|---|---|---|---|
| K-01 | Technical (audit) | Zero unmitigated AC-ATK after Phase 7.5 | 0 AC-ATK-01..18 rows in `OPEN` or `PARTIAL` state | Post-Phase-7.5 traceability matrix re-run against validation-spec § 11.1; CI-emitted JSON manifest of AC-ATK closure status per row |
| K-02 | Technical (runtime) | Sprint-runner pytest pass rate post-CLI update | 100% pass on `tests/cli/` after CR-DEP-05 stubification + CLI update lands | `uv run pytest tests/cli/ -v` green on integration branch immediately after Step 5 / Step 6 commits |
| K-03 | Technical (surface) | Residual `/sc:task` occurrences eliminated by CR-DEP-06 | 144 residual occurrences (research-notes baseline) → 0 outside authorized leave-as-is buckets | Post-Step-6 grep: `grep -RE '/sc:task\b\|sc-task-protocol\|task-unified' --include='*.md' --include='*.py' --include='*.yaml'` against the working tree minus authorized buckets (`.dev/releases/backlog/`, archived bucket subtrees, `docs/generated/*` with deferred-regen note); CR-DEP-06 manifest must enumerate every survivor with disposition |
| K-04 | Technical (operations) | `make verify-sync` flake rate after `flock` discipline lands (AC-ATK-16) | 0 flakes across 30 consecutive CI runs | CI run log retention: scan 30 most-recent `make verify-sync` invocations on integration branch; count non-deterministic failures attributable to worktree race |
| K-05 | Technical (audit) | Post-merge audit pass rate (CR-FM-NN + CR-TASK-NN + CR-DEP-NN + CR-DIST-NN + CR-REF-NN + CR-DOC-NN) | 100% PASS across all 33 spec-named CR rows post-Step-6 | Aggregated pre-commit gate output for Steps 1, 4, 5, 6, 8; rf-qa Step 6 chain-verification report (AC-ATK-07) returns PASS before hard-delete commit |
| K-06 | Product (surface) | Donor SKILL.md absent from disk post Step 6 (CR-DEP-03 + CR-DEP-04) | `src/superclaude/skills/sc-task-protocol/SKILL.md` and `.claude/skills/sc-task-protocol/SKILL.md` both absent; donor directory absent | Two `test -f` checks return non-zero; `find src/superclaude/skills/sc-task-protocol .claude/skills/sc-task-protocol -type d` returns empty; CR-DEP-04 directory-absence gate returns 0 |
| K-07 | Product (UX) | Visible command + skill surface count | 2 paired entries (`/sc:task` + `sc-task-protocol`; `/task` + `task`) → 1 paired entry (`/task` + `task`) | `superclaude install --dry-run` skill+command roster diff; user-facing `/sc:help` listing after Step 6 |
| K-08 | Business (maintenance) | Maintenance surface-pair count (paired `SKILL.md` files needing synchronized edits) | 2 → 1 | Repo-level census of `src/superclaude/skills/*/SKILL.md` matching the protocol-class regex; expected delta -1 after Step 6 |

### 19.2 KPI-to-Business-Lever Mapping

Cross-mapping back to the three S5 business levers:

| S5 Lever | Primary KPI | Secondary KPI |
|---|---|---|
| Surface reduction | K-07 (visible surface count) | K-06 (donor absent); K-08 (maintenance surface) |
| Audit-pass discipline via CR-7 ORDERING | K-05 (audit pass rate) | K-01 (zero unmitigated AC-ATK) |
| Sprint-runtime correctness via CR-DEP-05 stubification | K-02 (sprint-runner pytest) | K-03 (residual occurrences); K-04 (verify-sync flake rate) |

### 19.3 Measurement Cadence

- **K-01, K-05, K-06, K-07, K-08:** measured once at Phase 7.5 completion (release-criteria gate) and re-measured at each subsequent integration-branch merge that touches the task surface.
- **K-02:** measured on every CI run; reported in PR status checks.
- **K-03:** measured at Step 6 commit (initial) and at every weekly `cleanup-audit` invocation thereafter; CR-DEP-06 manifest archived per-week to `docs/generated/`.
- **K-04:** measured continuously via CI history rollup (30-run window).

### 19.4 Out-of-Scope KPIs

The following are explicitly **not** Feature-PRD KPIs (they live in Platform PRD): user-adoption rate of `/task` post-merge, DAU/MAU, monetization conversion, NPS. The directional merge is a maintenance investment whose KPIs are technical and discipline-oriented; user-adoption is a platform-level concern.

---

---

## 20. Risk Analysis

> Per template: technical, business, and operational risk matrices with mitigation and
> contingency columns. All owner cells = TBD pending engineering-lead assignment. Verbatim
> preservation applied to § 12 unnamed-tradeoff phrasing (R-TRADE-01..08) and § 15
> residual-risk concessions (R-RES-01..05) per spec source comment (validation-spec.md:411).

### 20.1 Technical Risks

> Predicate-precision gaps (R-ATK-01..18 = one risk per AC-ATK-01..18), timeline-layer
> hazards (R-S-01..03 + R-H-01..03), failure-mode coverage gaps (R-FM-01..08),
> evidence-completeness audit gaps (R-EC-01..04), artifact-gap and divergence risks
> (R-DOC-01, R-DIV-01).

#### 20.1.a Predicate-Precision Gaps — R-ATK-01..R-ATK-18 (one risk per AC-ATK-NN)

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-ATK-01** | F-02 ordering claim relies on grep alternation that does not enforce executable order (validation-spec § 5.1). Future formatting commit could shift sentinel comment without violating any grep, breaking parse-vs-semantic linkage. | M | M | Land **AC-ATK-01** — line-range-pinned check (or AST-level callgraph assertion); document sentinel discipline in CR-7/CR-8. | Treat F-02 ordering as informational only (per AC-ATK-13 downgrade option); annotate in CR-7. | TBD |
| **R-ATK-02** | F-03 binds only `git_status=dirty`; three other failure modes (tool-absent / not-a-repo / hang / error-other) are unspecified, allowing implementer divergence (warn-continue vs HALT) that breaks INV-01 or INV-04 (Scenario B). | M | H | Land **AC-ATK-02** — five-row matrix `{clean, dirty, tool-absent, not-a-repo, error-other}` with explicit dispositions per row. | If matrix cannot be authored pre-Phase-7.5, ship F-03 with explicit fail-loud on unmatched states; defer to first patch sprint. | TBD |
| **R-ATK-03** | CR-FM-NN family lacks closed-enum normalization rules (validation-spec § 9 INV-05 row). `Tier: STRICT` vs `tier: strict` vs `TIER:STRICT` produce non-deterministic parse outcomes. | M | M | Land **AC-ATK-03** — pin closed-enum normalization rules in CR-FM-01 (case, whitespace, alias handling). | Specify ASCII-upper canonical form in PRD § 25 examples; reject all variants. | TBD |
| **R-ATK-04** | Bucket-condensation arithmetic 79 → 65 is asserted without an enumerated bucket table (validation-spec § 6.4); ME-4/5/7/8 ancillary patterns could be elided rather than dropped. | M | M | Land **AC-ATK-04** — 79 → 65 condensation table with 2 duplicate CR-IDs explicitly enumerated. | Re-derive bucket table from `transfer-manifest.md` once recovered (depends on R-DOC-01). | TBD |
| **R-ATK-05** | ME-1 per-item-dispatch refusal is design-time-only (no runtime guard); a wrapper that "reads" the per-item marker and dispatches based on its value is semantically a dispatcher but parse-level a "read" (validation-spec § 5.3 + § 15 concession #1). | M | H | Land **AC-ATK-05** — closed enumeration of authorized per-item marker consumers (current = `{CR-TASK-07 baseline-skip}`); any new consumer requires a new manifest exception. | Accept as design-time residual per § 15 #1; rely on R-RULE-11 review discipline. | TBD |
| **R-ATK-06** | CR-FM-04 line-anchor `SKILL.md:191-198` is brittle to formatting edits (validation-spec § 9 INV-03 V3 augmentation); a one-line insertion above the spawn block silently breaks the citation while the semantic rf-qa guarantee holds. | M | M | Land **AC-ATK-06** — convert line-anchor to AST/regex anchor against the spawn-block content, not its line number. | Convert anchor to a content-hash check; bind to pre-commit hook. | TBD |
| **R-ATK-07** | F-07 procedural-chain authorization for donor-ceremony drop (CR-DEP-03) has no verifier role; auditable only by humans reading linked docs (validation-spec § 12 F-07 + § 15 concession #5). | M | H | Land **AC-ATK-07** — rebind `rf-qa` as F-07 chain-integrity verifier; spawn at Step 6 pre-commit. | Treat F-07 chain as procedural-only documented residual per § 15 #5; rely on human review. | TBD |
| **R-ATK-08** | S-1 `--max-wait` hierarchy was undecided in original spec; carrier surface (CLI flag vs frontmatter vs operator discipline) ambiguous (validation-spec § 15 #4 + § 7.1). | M | M | Land **AC-ATK-08** — `--max-wait 14d` default + auto-invoke option (b) + pinned git-SHA at every `[CODE-VERIFIED]` tag + CR-DEP-05 grep extension. Decide carrier surface in PRD § 14 (recommendation: task-frontmatter `max-wait: 14d` with watchdog). | If `--max-wait` enforcer cannot land in Phase 7.5, document as operator discipline only in PRD § 28. | TBD |
| **R-ATK-09** | Hash-equivalence audits (`md5sum`) are not collision-resistant; sufficiently determined adversary can craft drift that passes md5 check (research-06 § 1 FM-01 context). | L | M | Land **AC-ATK-09** — replace `md5sum` with `sha256sum` across audit grammar. | Document md5 as known-weak; require independent dual-hash check until swap lands. | TBD |
| **R-ATK-10** | F-03 dirty-tree closure does not distinguish input-invalid (HALT allowed) from environment-non-ideal (warn-continue required), risking divergent implementer interpretation (validation-spec § 9 INV-01 V3 augmentation). | M | H | Land **AC-ATK-10** — unified pre-loop HALT policy table with input-invalid vs environment-non-ideal rows. | Default all unclear cases to warn-continue (preserves INV-01); escalate to engineering lead. | TBD |
| **R-ATK-11** | F-05 third rf-qa invocation point widens INV-03 surface beyond canonical anchor language; authorization lives in plan, not in anchor (validation-spec § 5.7 + § 15 concession #2). Future TU-style merges could cite F-05 as precedent. | M | H | Land **AC-ATK-11** — either retroactive ME-10 binding F-05 in manifest, OR explicit one-time non-generalizing carve-out. F2 prohibition disposition matrix across `{root F1, verifier-spawned F1, mid-phase rf-qa context}`. | Treat F-05 as one-time non-generalizing; document explicitly in CR-7 to block precedent claims. | TBD |
| **R-ATK-12** | CR-FM-03 compatibility shim has no sunset binding; a future audit row dropping the default-fall-through bricks every shim-era TASK-* file (validation-spec § 4 + INV-04 evidence). | M | H | Land **AC-ATK-12** — bind CR-FM-03 lifetime to "at least N task generations or until an explicit migration row lands"; pin N. | Pin N=3 as recommendation in PRD § 14; defer to first migration-planning sprint. | TBD |
| **R-ATK-13** | CR-7/CR-8 sentinel-comment claim is "binding" but markdown comments cannot enforce executable ordering (validation-spec § 5.1 + § 12 F-02). | M | M | Land **AC-ATK-13** — downgrade CR-7/CR-8 sentinel claim from "binding" to "informational" OR move enforcement to an executable artifact (test or audit script). | Accept toolchain-coupling cost (§ 12 F-02); document explicitly in CR-7. | TBD |
| **R-ATK-14** | Bucket-condensation table enumeration does not surface 2 duplicate CR-IDs explicitly (extends R-ATK-04). | L | M | Land **AC-ATK-14** — surface the 2 duplicate CR-IDs in the condensation table; pin canonical disposition. | Document duplicates in PRD § 25 examples; require manual review at Step 5. | TBD |
| **R-ATK-15** | CR-DOC-01 placement ambiguity (Step 5 atomic vs Step 8 mkdocs gate) could cause atomicity violation if doc lands in wrong step (validation-spec § 14 EC-02 context). | M | M | Land **AC-ATK-15** — disambiguate CR-DOC-01 placement (Step 5 vs Step 8) with explicit decision rationale; pin rollback policy. | Default to Step 8 placement; require explicit operator confirmation if Step 5 chosen. | TBD |
| **R-ATK-16** | `flock` discipline on `.claude/skills/` during `make sync-dev` prune missing; parallel-worktree race risks Session B uncommitted-work loss (research-04 § 3, H-3). | M | M | Land **AC-ATK-16** — `flock -x .claude/skills/.sync-lock` wrappers around `sync-dev` loops (Makefile:111-124) and `verify-sync` loops (Makefile:159-183); post-prune `find -type d` dir-diff. Extend to cover **copy-overwrite race** (current copy-forward-only `sync-dev` has live overwrite race even without prune). | Document current sync as "copy-forward-only"; require `flock` to land before any prune-semantics refactor. | TBD |
| **R-ATK-17** | Rebase-split bypass produces transient master SHA where `/sc:task` is stubified in `task.md` but still emitted live from CLI sources; any sprint run pinned to that SHA dies (research-04 § 2, H-2). | M | H | Land **AC-ATK-17** — server-side pre-push hook (or CI check) re-grepping landing commit (not working tree) for `/sc:task\b` in CLI sources. **Grep scope MUST include both `src/superclaude/cli/sprint/process.py` (1 emission) AND `src/superclaude/cli/cleanup_audit/prompts.py` (5 emissions at lines 26, 47, 69, 92, 116)** — fresh discovery per research-04 § 2.5. Exclude `/sc:tasklist` substring false-positives. | Author `.github/workflows/push-policy.yml` CI check; require bypass-resistance (run on push, not PR-merge); reject `--no-verify` pattern. | TBD |
| **R-ATK-18** | INV-04 resumability has highest exposure — **132 in-flight MDTM files** (live recount 2026-05-16 fix-cycle 1; spec asserts 96 — spec is now an UNDER-count, direction inverted from earlier research-03 25-file figure) contain content-level deprecated-surface references CR-FM-03 does not see; CR-FM-03 sees parse-layer only (research-04 § 4, H-4). | M | H | Land **AC-ATK-18** — extend CR-FM-03 with content-level audit at resume time (`grep -E "(/sc:task\b|sc-task-protocol\|task-unified)"` against task body); warn-and-continue HALT disposition per ME-3; one-shot ack gate; pair with CR-DEP-06 residual-reference manifest. | If content-level audit cannot land at resume, document at-risk task IDs (`TASK-RESEARCH-20260403-sprint-task-exec` confirmed) in PRD § 20.3; manual operator audit. | TBD |

#### 20.1.b Timeline-Layer Hazards — R-S-01..R-S-03 + R-H-01..R-H-03

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-S-01** | S-1 in-flight PRD/TDD precondition: no `--max-wait` enforcer exists in code; named targets `TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250` both **live on disk** per 2026-05-16 fix-cycle 1 (constraint binds them in addition to the broader 132-file in-flight population referencing donor surfaces). Without enforcer, in-flight PRDs/TDDs touching donor surfaces can stall Step 5 indefinitely. | H | M | AC-ATK-08 (`--max-wait 14d` + auto-invoke (b)); task-frontmatter convention `max-wait: 14d` with watchdog; pinned-SHA discipline on `[CODE-VERIFIED]` tags. | Operator discipline only until enforcer ships; weekly review of in-flight PRD/TDD set against donor-surface grep. | TBD |
| **R-S-02** | S-2 CLI runtime atomicity: no active git hooks (`.git/hooks/` contains only `*.sample`); no `.pre-commit-config.yaml` pre-push stage (commit-stage only at line 92); no `.github/workflows/` push-policy. `git rebase -i` + commit-split path is wide open. CLI scope per spec under-counts emission sites by 5/6 (83%) — fresh discovery `cleanup_audit/prompts.py`. | H | H | AC-ATK-17 with **extended grep scope** to `src/superclaude/cli/{sprint,cleanup_audit}/**`; word-boundary regex `/sc:task\b`; server-side CI check (not per-developer hook). | If hook cannot land in Phase 7.5, require manual two-reviewer attestation on every push touching CLI sources during merge window. | TBD |
| **R-S-03** | S-3 Makefile sync atomicity: no `flock` discipline; no post-prune dir-diff; CLAUDE.md authorizes parallel worktrees. Current `sync-dev` is copy-forward-only — H-3 prune-race is **forward-looking** but copy-overwrite race is **live**. | M | M | AC-ATK-16 with **scope extension** to cover copy-overwrite race in current code (not only forward-looking prune race). Document current semantics as "copy-forward-only" in PRD § 14. | Single-session sync discipline during merge window; pause parallel worktrees during `make sync-dev` runs. | TBD |
| **R-H-01** | H-1 PRD stalls 30+ days; merge bypassed via S-1 option (b); remaining subagent emits `[CODE-CONTRADICTED]` tags; deliverable corrupted. **Live exposure:** at least three in-flight PRD/TDD tasks touching donor surfaces (`TASK-PRD-20260514-121039` live, `TASK-TDD-20260514-121250` live, this PRD `TASK-PRD-20260516-004625`) plus the broader 132-file population (130 live at fix-cycle 1; 132 at fix-cycle 2 — population dynamic) — H-1 scenario condition is live across multiple tasks. | M | H | AC-ATK-08 + pinned-SHA discipline on `[CODE-VERIFIED]` tags (PRD adds TFEP-class convention: `(git-sha: <40-char>)` suffix on all verification tags). | Snapshot-freeze in-flight PRDs/TDDs at `(git-sha)` of S-1 max-wait expiry; deferred re-read post-merge. | TBD |
| **R-H-02** | H-2 rebase-split intermediate SHA carries stubified `/sc:task` in `task.md` but live emission in `sprint/process.py:170` + `cleanup_audit/prompts.py:26,47,69,92,116`. Six emission sites; spec names one. Any sprint run pinned to the intermediate SHA dies. | M | H | AC-ATK-17 with extended grep scope (per R-S-02); test-coverage parity gap (`tests/cleanup_audit/test_prompts.py` does not exist) authored. | If hook absent, ban `git rebase -i` during merge window via documented policy (S-5 rebase-ban per validation-spec L435). | TBD |
| **R-H-03** | H-4 resumed task hits deleted PRIMARY ARTIFACT (`sc-task-protocol/SKILL.md` named in subagent prompt); CR-FM-03 validates clean but resume path fails on `Read`. Live concrete target: `TASK-RESEARCH-20260403-sprint-task-exec` (**48 donor-surface occurrences across 10 files** in subtree, status 🟠 Doing — verified 2026-05-16 fix-cycle 1 via `rg -c "/sc:task|sc-task-protocol|task-unified" <subtree>` summed). | H | H | AC-ATK-18 content-level resume-time audit + one-shot ack gate + CR-DEP-06 manifest. Scope manifest to `.dev/tasks/to-do/` (132 union files per 2026-05-16 fix-cycle 1 live recount). | Manual operator review of in-flight tasks before merge; freeze named at-risk task IDs with explicit decision record. | TBD |

#### 20.1.c § 12 Unnamed Tradeoffs — R-TRADE-01..R-TRADE-08 (verbatim phrasing preserved)

> Per spec § 12 lines 372–379 `[SPEC-VERIFIED]`. Verbatim cost phrasing preserved per
> spec source comment L411 ("preserved verbatim with attribution"). Each tradeoff is a
> cost the source plan does not name, paired with the closure that produces it.

| ID | Description (verbatim where in quotes) | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-TRADE-01** | **F-01 closure tradeoff** (spec L372): "Naming the consumption shape 'tier-conditioned read' widens INV-05 attack surface by making 'read' semantically open-ended. Cost of closing F-01 is implicit grant of unbounded read channel." | M | H | None direct; couples to § 15 concession #1 (R-RES-01). AC-ATK-05 closed-enum partial. | Accept as design-time residual; rely on R-RULE-11 review discipline. | TBD |
| **R-TRADE-02** | **F-02 closure tradeoff** (spec L373): "Two greps + sentinel comment shifts enforcement from structural ordering to documentation discipline. If SKILL.md is auto-generated by any future tool, sentinel comments could be stripped without triggering grep — because function names remain in source order. Coupling between audit tool and source-file editing toolchain is unbound." | M | M | AC-ATK-01 + AC-ATK-13 partial (toolchain-coupling cost survives). | Ban auto-generation of SKILL.md; require manual edit discipline. | TBD |
| **R-TRADE-03** | **F-03 closure tradeoff** (spec L374): "Reading A (warn-and-continue) preserves INV-01 but exposes the runtime to dirty-tree-induced behavior divergence in downstream commits. A warned-and-continued dirty tree could land partial state into the merge sequence." | M | M | AC-ATK-02 + AC-ATK-10 partial (warn-and-continue residual by design). | Accept residual; document dirty-tree behavior in operator runbook. | TBD |
| **R-TRADE-04** | **F-04 closure tradeoff** (spec L375): "Over-escalate floods the rf-qa queue. Plan notes 'possibly-noisier escalation queue' but does not specify when 'noisy' becomes a refusal trigger." | M | M | None; couples to § 15 concession #3 (R-RES-03). | Monitor rf-qa queue depth; introduce refusal threshold reactively. | TBD |
| **R-TRADE-05** | **F-05 closure tradeoff** (spec L376): "Mid-phase rf-qa routing means the verifier sees in-progress state instead of phase-complete state. Reuses spawn pattern but does not address the semantic shift: rf-qa was designed to verify completed work, not adjudicate in-flight escalations." | M | H | AC-ATK-11 structural (semantic-shift cost survives); couples to § 15 #2 (R-RES-02). | Document semantic-shift in rf-qa skill rules; train rf-qa for in-flight adjudication mode. | TBD |
| **R-TRADE-06** | **F-06 closure tradeoff** (spec L377): "Citing `extension-point-contracts.md:11-17` means line-pinned reference is brittle to any edit. Formatting commit adding one line above the anchor block silently breaks the citation." | M | M | None direct (no AC closure). Anchor file present on disk; content audit owed per reframed R-DOC-01 (line-pinning fragility persists). | Convert all spec citations from line-pinned to content-pinned (regex / hash) post-content-audit. | TBD |
| **R-TRADE-07** | **F-07 closure tradeoff** (spec L378): "Procedural authorization without verifier role means chain is auditable only by humans reading linked docs. Automation cannot enforce it. CR-DEP-03's irreversibility (hard-delete) compounds the cost." | M | H | AC-ATK-07 partial (auditability cost closed; irreversibility cost survives); couples to § 15 #5 (R-RES-05). | Accept residual; CR-DEP-03 step gated behind verifier sign-off. | TBD |
| **R-TRADE-08** | **F-08 closure tradeoff** (spec L379): "Correcting 'five' to 'six' is mechanical, but does not audit downstream references to 'five' in other Phase 6 artifacts (`merge-master.md:7` still says 'five'). Inconsistency persists in chain of trust." | L | M | None direct. `merge-master.md` present on disk; content audit owed per reframed R-DOC-01. | Add Phase-6-artifact downstream cross-grep for "five"→"six" propagation post-content-audit. | TBD |

#### 20.1.d FM-NN Failure-Mode Coverage Gaps — R-FM-01..R-FM-08

> Per spec § 13 lines 387–394 `[SPEC-VERIFIED]`. Orthogonal to HZ-01..HZ-18 row-level
> hazards. Phase 7.5 patch scope (21 changes per spec L435) does **NOT** include FM
> mitigations; six of eight are fully open.

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-FM-01** | **Filesystem / symlink defeat** (spec L387): `make verify-sync` returns 0 on successful sync but does not check for symlink divergence between `[src]` and `[.claude]`. If `[.claude]` is symlinked to `[src]` (defeats R-RULE-10), md5sum/sha256sum/content checks pass trivially. | L | H | No AC closure. Add Phase-7.5.b story: `find .claude/skills -type l` stat check + fail-loud on any symlink. | Document `verify-sync` known limitation; require manual `find` audit pre-merge. | TBD |
| **R-FM-02** | **Atomicity / rollback** (spec L388): Step 5 atomic across six rows. If any pytest invocation flakes intermittently, atomicity guarantee creates a no-progress state where commit cannot land but soft-deprecation has been authored locally. Rollback policy unspecified. | M | M | AC-ATK-15 partial (placement only). Add explicit rollback policy: `git checkout HEAD -- <files>` discard-local on Step 5 pre-commit failure. | Manual operator rollback; document retry budget (recommendation: 3 retries before HALT). | TBD |
| **R-FM-03** | **Concurrent edits** (spec L389): Two implementation sub-agents running in parallel could land conflicting edits to SKILL.md at row 1 vs row 10. Atomic-merge obligation is at commit level, not edit level. Distinct from H-3 (worktree race) — this is same-file in-tree concurrent edits. | M | M | No AC closure. Author file-level lock convention for SKILL.md edits during merge; consider Edit-tool serialization. | Single-executor discipline during Step 5; ban parallel subagent dispatch on `task/SKILL.md`. | TBD |
| **R-FM-04** | **CI / local env determinism** (spec L390): `uv run pytest` on local machine and on CI may surface different results if env vars differ (`PYTHONHASHSEED`, locale, timezone). Pre-commit gate does not pin env. | M | M | No AC closure. Phase-7.5.b story: `pytest --strict-markers` + env-pin (`PYTHONHASHSEED=0`, `LC_ALL=C`, `TZ=UTC`) in `pyproject.toml` or CI image. | Document known env divergence; require dual-run (local + CI) attestation pre-merge. | TBD |
| **R-FM-05** | **mkdocs build version drift** (spec L391): Step 8 gate is `mkdocs build` returns 0 broken-link warnings. mkdocs version not pinned. Version upgrade changing broken-link semantics could pass or fail same source tree. | L | M | No AC closure. Pin mkdocs version in `pyproject.toml`; use version-stamped CI image. | Document version dependency; freeze mkdocs version for duration of merge window. | TBD |
| **R-FM-06** | **Deferred regen scheduling** (spec L392): Step 10 commits with `docs/generated/*: refresh deferred to next regenerator run.` Next regenerator run unscheduled. If it never runs, `docs/generated/*` permanently disagrees with `docs/` source. 83 occurrences live. | M | M | CR-DEP-06 + AC-ATK-18 partial (detection only, not remediation). Schedule binding: assign regenerator-run authority to framework-maintenance team with defined cadence (PRD § 28). | Manual regenerator invocation as part of weekly framework-maintenance ritual. | TBD |
| **R-FM-07** | **Encoding audit defeat** (spec L393): None of the greps specify text encoding. UTF-16-authored markdown silently passes every grep with no matches. Adversarial-or-accidental UTF-16 in recipient surface evades the entire grep-based audit class. | L | H | No AC closure. Phase-7.5.b story: `file -i` pre-grep encoding check, or `iconv` normalization step in audit grammar. | Document UTF-8-only authoring discipline; require encoding attestation pre-merge. | TBD |
| **R-FM-08** | **File-rename evasion** (spec L394): Hard-deletion at CR-DEP-03 is procedural. If donor file renamed (e.g., `*.deprecated`) rather than deleted, absence check passes but file persists. R-RULE-11 violation indirect. | L | H | AC-ATK-07 partial (chain verifier added; filesystem state still open). Phase-7.5.b story: `git diff --diff-filter=D` assertion on Step 6 commit verifying donor inode is deleted, not renamed. | Manual `find` audit of donor paths pre-merge; reject any `*.deprecated` artifact in commit diff. | TBD |

#### 20.1.e Evidence-Completeness Audit Gaps — R-EC-01..R-EC-04

> Per spec § 14 lines 402–405 `[SPEC-VERIFIED]`. Audits the **source plan's** § 9
> validation hooks (cites lines inside the absent `merge-master.md` /
> `final-merge-plan.md` — `[VALIDATION-SPEC-CITED][UNVERIFIED]` throughout).

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-EC-01** | Plan's § 9 hook (source L447): "Grepping § 4 for each F-01..F-08 disposition." Grep pattern unspecified. Reviewer using `grep -n "F-0"` vs `grep -n "F-01"` vs `grep -n "F-[0-9][0-9]"` gets different results. Two reviewers can sign off on different audit outputs of the same artifact. | M | M | No AC closure. PRD § 25 (API Contract Examples) codifies canonical pattern: `grep -nE '^[[:space:]]*F-0[1-8][^0-9]'` or equivalent. | Manual two-reviewer pattern-attestation on each grep. | TBD |
| **R-EC-02** | Plan's § 9 hook (source L449): "Confirming § 5 carries the same 67 row-line-items as merge-master.md § 1." Comparison method unspecified — diff, manual count, hash? With four declared row-deltas, any naive textual diff is non-zero by design. | M | M | AC-ATK-04 + AC-SM-06 partial (arithmetic only). Specify comparison method explicitly in PRD § 25 (recommendation: structured diff per CR-ID, not textual diff). | Manual count-based audit; document method in PRD § 21. | TBD |
| **R-EC-03** | Plan's § 9 hook (source L450): "V/C/K verdicts carried forward unchanged." Carry-forward asserted; no audit step re-derives V/C/K. R-RULE-07 requires re-scoring on drift; plan claims zero drift but no-drift claim itself unaudited (circularity). | M | H | AC-SM-01 intent (byte-for-byte against `transfer-manifest.md` § 4) — **GATED on R-DOC-01 content audit** (artifact present on disk; cross-check owed). | Conduct content audit of `transfer-manifest.md` (now present) as Phase-7.5 prerequisite, then execute AC-SM-01 in full. | TBD |
| **R-EC-04** | Plan's § 9 hook (source L452): "the reviewer recomputes a sample of the no-drift V/C/K assessments by picking 3 TUs." 3-of-8 = 37.5% sample. Cannot rule out single drifted TU among unsampled five. | M | M | AC-SM-01 in full (not sample) — **GATED on R-DOC-01 content audit** (artifact present on disk; cross-check owed). | Full 8-of-8 cross-check post-content-audit; reject any sample-based attestation. | TBD |

#### 20.1.f Artifact-Gap and Divergence Risks — R-DOC-01, R-DIV-01

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-DOC-01** | **ARTIFACT_GAPS — superseded by fix-cycle 2 QA verification 2026-05-16.** The originally-claimed "7 absent upstream artifacts" narrative was DRAFTED on the assumption that `.dev/releases/current/task-sc-task-directional-merge/artifacts/` did not exist. **Fix-cycle 2 verification (2026-05-16, report-validation phase) confirms that all seven named artifacts ARE PRESENT on disk**: (1) `extension-point-contracts.md`, (2) `transfer-manifest.md`, (3) `merge-master.md`, (4) `compat-hazard-report.md`, (5) `invariant-survival-walkthrough.md`, (6) `final-merge-plan.md`, and (7) `rejected-features-ledger.md` all exist at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`. The risk row is RECLASSIFIED from "artifact gaps" to "artifact-content verification still owed": each AC-SM row originally flagged `[CONTENT-AUDIT-OWED]` (AC-SM-01, -03, -05, -06, -11) must now be re-evaluated by reading the on-disk artifact and confirming byte-for-byte / structural conformance. Cascading `[CONTENT-AUDIT-OWED]` tags on AC-SM-04, -07, -09, -10, -12 against the now-present `final-merge-plan.md` should likewise be re-evaluated. The PRD body still carries the original `[VALIDATION-SPEC-CITED][UNVERIFIED][CONTENT-AUDIT-OWED]` tags pending a follow-up content audit; the tag SEMANTICS are unchanged (verification still owed) but the BASIS has flipped from "cannot read" to "must read". | M (reduced from H) | M (reduced from H) | **PRIMARY** — Conduct artifact content audit (read each of the 7 artifacts; confirm cited line ranges and content match PRD claims). Update AC-SM verdict per row. Open Question #2 reframed: not "recover vs re-derive" but "schedule content audit and reconcile any drift." Until content audit completes, the `[VALIDATION-SPEC-CITED][UNVERIFIED]` tag remains in place. | If content audit surfaces drift between artifact body and PRD claims, treat as a per-row finding (R-DRIFT-NN); do not block Phase 7.5 on resolution unless the drift invalidates a load-bearing claim. | TBD |
| **R-DIV-01** | **DIVERGENCE_FLAGS — direction-corrected at fix-cycle 1.** Spec assertions vs live evidence on 2026-05-16 fix-cycle 1: (a) S-1 named-target population: `TASK-PRD-20260514-121039` **EXISTS** (created 2026-05-16 01:37) `[CODE-VERIFIED]`; `TASK-TDD-20260514-121250` **EXISTS** `[CODE-VERIFIED]`; only `TASK-RF-20260515-195758` is genuinely absent — earlier research-04 § 1.1 "all stale" framing was itself stale at synthesis time, now corrected to "named targets partially current"; (b) Spec § 3 line 81 asserts 96 in-flight MDTM task files; **live count is 132** union files at fix-cycle 2 (`rg -l "/sc:task|sc-task-protocol|task-unified" .dev/tasks/ | wc -l`; 130 live at fix-cycle 1 — population dynamic) — H-4 blast radius is LARGER than spec assumes, not smaller; earlier research-03 25-file figure reflected a narrower subset/morning grep that became stale within hours; (c) Donor F-05 mid-phase route currently goes to `/sc:forensic` (donor `sc-task-protocol/SKILL.md:191-218`), NOT to rf-qa — F-05 retargets at merge; (d) Tier vocabulary divergence (3-tier spec vs 4-tier code per Open Question #1); (e) CLI scope under-counts emission sites by 5/6 (83%) — `cleanup_audit/prompts.py` not named (fresh discovery). | H | M | Bind S-1 to live named targets + broader 132-file population (Open Question #3, supplement-not-replace; population dynamic — 130 at fix-cycle 1, 132 at fix-cycle 2); adopt live-recount scope as Step-5-pre-commit recount target; retarget F-05 explicitly in CR-7; reconcile tier vocab (Open Question #1); extend AC-ATK-17 grep scope. | If divergences accumulate further, re-run research probe at Step 5 pre-commit; gate Phase 7.5 on fresh divergence count ≤ current. | TBD |

---

### 20.2 Business Risks

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-BIZ-01** | Merge stalls indefinitely due to in-flight PRD soft-blocks (S-1 generalization); blocks downstream consumers of unified `/task` interface; ship-window slips. | M | H | AC-ATK-08 (`--max-wait 14d` default + auto-invoke (b)); explicit decision record on in-flight PRD freeze. | Escalate ship-window slip to stakeholder review; partial-ship `/task` with banner noting `/sc:task` deprecation pending. | TBD |
| **R-BIZ-02** | Tier vocabulary inconsistency (3-tier spec vs 4-tier code) confuses downstream skill authors; introduces classification ambiguity into post-merge tier audits; rework cost. | M | M | Resolve Open Question #1 pre-merge; pin canonical 4-tier set `{STRICT, STANDARD, LIGHT, EXEMPT}` in PRD § 14 and propagate to all spec citations. | If reconciliation delayed, ship with both vocabularies documented + migration note; deprecate 3-tier post-merge. | TBD |
| **R-BIZ-03** | Adoption friction from companion-TDD absence: engineering audience cannot consume PRD alone for implementation (5 load-bearing INVs, 5 MEs, 18 AC-ATKs, 8 FMs, 4 ECs, 8 tradeoffs, 5 concessions — high cognitive load without architectural overlay). | M | M | Resolve Open Question #5 in favor of authoring companion TDD; offer at delivery. | If TDD declined, expand PRD § 14 and § 21 with TDD-equivalent depth; risk PRD length bloat. | TBD |

---

### 20.3 Operational Risks

| ID | Description | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-OPS-01** | Parallel-worktree session conflicts during merge window: CLAUDE.md authorizes parallel `git worktree` sessions, but no `flock` on `.claude/skills/` and no file-level lock on `task/SKILL.md` (FM-03 + S-3). Loss of in-progress work from Session B. | M | M | AC-ATK-16 with copy-overwrite-race extension; single-session sync discipline during merge window; ban parallel subagent dispatch on `task/SKILL.md` during Step 5. | Manual operator coordination; pause parallel worktrees during merge window. | TBD |
| **R-OPS-02** | At-risk in-flight task `TASK-RESEARCH-20260403-sprint-task-exec` (48 donor-surface refs across 10 files in subtree, status 🟠 Doing — verified 2026-05-16 fix-cycle 1 via `rg -c "/sc:task|sc-task-protocol|task-unified" <subtree>` summed) hits H-4 resumed-task scenario post-merge; manual operator intervention required. | H | M | AC-ATK-18 content-level audit + one-shot ack gate; pre-flag at-risk task ID in PRD § 20 and operator runbook. | Manual operator review pre-merge; explicit decision record on freeze/reroute/migrate disposition for this task. | TBD |
| **R-OPS-03** | rf-qa queue flood from F-04 over-escalation (verbatim § 15 concession #3): unbounded routing volume could starve rf-qa for legitimate phase-gate verifications. | M | M | None direct. Monitor rf-qa queue depth as operational metric; introduce refusal threshold reactively post-flood detection. | Manual triage of rf-qa queue; escalate severe floods to engineering lead for ad-hoc throttling. | TBD |
| **R-OPS-04** | Five-row HALT matrix (AC-ATK-02) authoring delay forces ship with implicit divergence between implementers on `git_status` failure modes. | L | H | Land AC-ATK-02 in Phase 7.5 with explicit author owner; gate Phase 7.5 sign-off on matrix completion. | If matrix delayed, default all unmatched git_status states to fail-loud (HALT); operator training on three-of-five missing dispositions. | TBD |

---

### § 15 Residual-Risk Concessions — R-RES-01..R-RES-05 (verbatim from V1 steelman)

> Per spec § 15 lines 415–419 `[SPEC-VERIFIED]`. Source comment L411: "Source: V1 § 6
> (5 honest concessions; preserved verbatim with attribution)". These are accepted
> residuals at the operational level. Concession #4 is closed via AC-ATK-08; the other
> four (#1, #2, #3, #5) survive Phase 7.5 by design.

| ID | Concession (verbatim from spec § 15) | Probability | Impact | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|
| **R-RES-01** | **(spec L415, Concession #1):** "The 'tier-conditioned read' boundary is conceptually thin. Plan acknowledges this (source line 97) and bounds with ME-1 + acceptance-criterion language, but a sufficiently determined refactor could describe a forbidden per-item dispatch as a 'read' if it routes through a wrapper. Defense relies on R-RULE-11 audit discipline at design-time — human-process, not structural." | M | H | ME-1 + AC-ATK-05 closed-enum; design-time R-RULE-11 review discipline. **Remains accepted residual per § 15.** | Add structural runtime guard (out-of-scope for Phase 7.5); escalate to engineering lead if wrapper-dispatch pattern observed in code review. | TBD |
| **R-RES-02** | **(spec L416, Concession #2):** "The third rf-qa invocation point (F-05) widens INV-03's surface beyond the canonical anchor language. Plan calls this 'authorized' and documents three-prong defense, but anchor source (`extension-point-contracts.md:11-17`) was not amended to mention mid-phase routing. Authorization lives in this plan, not in the anchor." | M | H | AC-ATK-11 (retroactive ME-10 OR one-time non-generalizing carve-out). Anchor file present on disk (R-DOC-01 reframed); content audit needed before concession can be falsified. | Treat F-05 as one-time non-generalizing; block precedent claims by future TU-style merges in CR-7. | TBD |
| **R-RES-03** | **(spec L417, Concession #3):** "F-04 over-escalation is a load-volume bet on rf-qa. Classifying every failure as `new` when baseline is absent could flood the verifier queue. Plan does not bound upper limit on this routing volume." | M | M | None direct. § 12 F-04 tradeoff noted; no AC closes load axis. **Remains accepted residual per § 15.** | Monitor rf-qa queue depth (R-OPS-03); introduce refusal threshold reactively. | TBD |
| **R-RES-04** | **(spec L418, Concession #4):** "S-1's mitigation hierarchy (a / b / c) is recorded but not decided. Source line 325 leaves the choice 'at Phase 7 execution time.' Late-discovered infeasibility of (a) means options (b) or (c) get chosen under time pressure." | M | M | **CLOSED via AC-ATK-08** — `--max-wait 14d` default + auto-invoke option (b). Choice still time-pressured at deadline expiry. | If 14d expires under time pressure with option (a) infeasible, default to (b) snapshot-freeze; defer option (c) to post-merge decision. | TBD |
| **R-RES-05** | **(spec L419, Concession #5):** "The procedural authorization chain (F-07) is 'not a manifest binding.' Source line 186 explicitly says so. Future reviewer applying strict-manifest-only discipline could insist on retroactive amendment despite the chain being documented." | M | H | AC-ATK-07 adds verifier role (rf-qa); chain itself remains procedural. `transfer-manifest.md` present on disk (R-DOC-01 reframed); content audit owed. **Remains accepted residual per § 15.** | Retroactively manifest-bind F-07 in a future audit cycle if strict-manifest-only reviewer challenges it; document explicitly in CR-7. | TBD |

---

---

## 21. Implementation Plan

### 21.1 Epics, Features & Stories

> See Section 7 (Personas) for the persona index and synthesis-02 cross-walk for the full 28-story enumeration with AC mapping (E-1..E-8 epics; US-E1.1..US-E8.4 stories). The epic and story table below is the canonical implementation-plan view.


Persona cross-reference: see **synth-02 (Personas & JTBD)** for full Persona definitions (Framework Maintainer, Task Author, Reviewer/rf-qa, In-flight Task Resumer, Sprint CLI Operator). Epic ownership and JTBD anchors below reference those personas without restating them.

**Epic E-01 — Donor surface stubification & deletion (10-step canonical commit sequence)**

Primary persona: Framework Maintainer (synth-02 P-01). JTBD anchor: synth-02 JTBD-01 (collapse two parallel surfaces to one) and JTBD-04 (remove donor source-of-truth ambiguity).

| Story ID | Story | AC anchors | Step |
|---|---|---|---|
| S-E01-01 | Step 1: Land CR-TASK-12 seven-diff baseline against still-present donor | AC-SM-08 | 1 |
| S-E01-02 | Step 4: Land CR-7 + CR-8 sentinel comments (or AST-level replacement per AC-ATK-13) | AC-ATK-01, AC-ATK-13 | 4 |
| S-E01-03 | Step 5: Stubify donor `/sc:task` command + author CR-DOC-01 doc row + emit sha256 digests | AC-ATK-09, AC-ATK-15, AC-SM-09 | 5 |
| S-E01-04 | Step 6: Hard-delete donor `sc-task-protocol/SKILL.md` + `__init__.py` + directory under rf-qa verifier chain | AC-ATK-07, AC-SM-10, K-06 | 6 |
| S-E01-05 | Steps 8–10: mkdocs build + deferred-regen note + leave-as-is enforcement | AC-SM-12 (gate at Step 8); CR-REF buckets A, C, D, E, F, G, H | 8, 9, 10 |

**Epic E-02 — Predicate-precision acceptance-criteria closure (Phase 7.5)**

Primary persona: Reviewer / rf-qa (synth-02 P-03). JTBD anchor: synth-02 JTBD-03 (audit-binding closure of falsifiable gaps).

| Story ID | Story | AC anchors |
|---|---|---|
| S-E02-01 | AC-ATK-01..04 predicate-precision authoring (alternation-grep replacement, git-status matrix, baseline four-state, 79→65 condensation table) | AC-ATK-01, -02, -03, -04 |
| S-E02-02 | AC-ATK-05..08 consumer enumeration, snapshot fixture, verifier role, S-1 timeout | AC-ATK-05, -06, -07, -08 |
| S-E02-03 | AC-ATK-09..12 sha256 substitution, HALT-policy table, F-05 ME-10 binding, fan-out (sunset/seven-fields/canonicalization) | AC-ATK-09, -10, -11, -12 |
| S-E02-04 | AC-ATK-13..15 sentinel disambiguation, CR-DEP-05 scope + CR-REF-18 root + CR-DEP-04 gate + CR-DOC-13 R-RULE-11 disposition, CR-DOC-01 Step 5/8 disambiguation | AC-ATK-13, -14, -15 |

**Epic E-03 — V3 security-probe overlay (Phase 7.5 — security)**

Primary persona: Framework Maintainer + Reviewer (synth-02 P-01, P-03). JTBD anchor: synth-02 JTBD-05 (close adversarial timeline-layer attacks).

| Story ID | Story | AC anchors |
|---|---|---|
| S-E03-01 | AC-ATK-16: `flock` discipline + post-prune dir-diff for `make sync-dev` | AC-ATK-16 |
| S-E03-02 | AC-ATK-17: server-side pre-push hook re-grepping landing commit for `/sc:task` in CLI sources | AC-ATK-17 |
| S-E03-03 | AC-ATK-18: CR-FM-03 content-level resume grep + gate-1.5 emission + one-shot ack gate + CR-DEP-06 residual manifest | AC-ATK-18 |

**Epic E-04 — Sequencing-constraint additions (Phase 7.5 — sequencing)**

Primary persona: Framework Maintainer (synth-02 P-01). JTBD anchor: synth-02 JTBD-02 (sprint-runtime correctness).

| Story ID | Story | AC anchors |
|---|---|---|
| S-E04-01 | S-4: PRD `--max-wait` 14d default + auto-invoke option (b) + pinned git-SHA at every `[CODE-VERIFIED]` tag | AC-ATK-08 |
| S-E04-02 | S-5: Rebase-ban via server-side pre-push hook (encompassed by AC-ATK-17 server-side check) | AC-ATK-17 |

**Epic E-05 — In-flight task resumability (continuous; spans Step 6 → ongoing)**

Primary persona: In-flight Task Resumer (synth-02 P-04). JTBD anchor: synth-02 JTBD-06 (resumed tasks survive donor deletion).

| Story ID | Story | AC anchors |
|---|---|---|
| S-E05-01 | CR-FM-03 parse-layer shim: default `Tier:` to STANDARD when absent | CR-FM-03 parse-layer |
| S-E05-02 | CR-FM-03 content-layer resume grep + gate-1.5 warn-and-continue per AC-ATK-18(a)(b)(c) | AC-ATK-18(a), (b), (c) |
| S-E05-03 | CR-DEP-06 weekly one-shot manifest emit + archive to `docs/generated/` | AC-ATK-18(d), K-03 |

### 21.2 Product Requirements — MoSCoW × RICE Matrix

MoSCoW prioritization (Must / Should / Could / Won't) applied at the **epic + story** level. RICE = Reach × Impact × Confidence / Effort (effort in engineer-days, rough order from § 18.2).

| Story | MoSCoW | Reach (R, 1–5) | Impact (I, 0.25/0.5/1/2/3) | Confidence (C, % → 0.0–1.0) | Effort (E, eng-days) | RICE = R·I·C / E |
|---|---|---:|---:|---:|---:|---:|
| S-E01-01 (Step 1 baseline) | **Must** | 5 | 2 | 0.9 | 0.5 | 18.0 |
| S-E01-02 (Step 4 sentinel/AST) | **Must** | 5 | 2 | 0.85 | 1.0 | 8.5 |
| S-E01-03 (Step 5 stubify + doc + sha256) | **Must** | 5 | 3 | 0.85 | 2.0 | 6.4 |
| S-E01-04 (Step 6 hard-delete + rf-qa) | **Must** | 5 | 3 | 0.8 | 2.0 | 6.0 |
| S-E01-05 (Steps 8–10) | **Must** | 4 | 1 | 0.85 | 1.5 | 2.3 |
| S-E02-01 (AC-ATK-01..04) | **Must** | 4 | 2 | 0.85 | 3.0 | 2.3 |
| S-E02-02 (AC-ATK-05..08) | **Must** | 4 | 2 | 0.8 | 3.0 | 2.1 |
| S-E02-03 (AC-ATK-09..12) | **Must** | 4 | 2 | 0.9 | 2.5 | 2.9 |
| S-E02-04 (AC-ATK-13..15) | **Must** | 4 | 1.5 | 0.8 | 2.0 | 2.4 |
| S-E03-01 (AC-ATK-16 flock) | **Should** | 3 | 1 | 0.75 | 1.5 | 1.5 |
| S-E03-02 (AC-ATK-17 pre-push) | **Should** | 3 | 2 | 0.7 | 2.0 | 2.1 |
| S-E03-03 (AC-ATK-18 + CR-DEP-06) | **Must** | 5 | 2 | 0.8 | 2.5 | 3.2 |
| S-E04-01 (S-4 PRD `--max-wait`) | **Should** | 3 | 1 | 0.85 | 0.5 | 5.1 |
| S-E04-02 (S-5 rebase-ban) | encompassed by S-E03-02 | — | — | — | — | — |
| S-E05-01 (CR-FM-03 parse shim) | **Must** | 5 | 2 | 0.95 | 0.5 | 19.0 |
| S-E05-02 (CR-FM-03 content gate-1.5) | **Must** | 5 | 2 | 0.85 | 1.0 | 8.5 |
| S-E05-03 (CR-DEP-06 weekly emit) | **Should** | 3 | 1 | 0.85 | 1.0 | 2.6 |

**Could-tier** (deferred to Phase 7.5.b if scope expanded): FM-NN mitigation stories (FM-01 symlink, FM-02 atomicity rollback, FM-03 parallel edits, FM-04 env determinism, FM-05 mkdocs pin, FM-07 encoding).

**Won't-tier (Phase 7.5)**: full Phase-6-artifact downstream cross-grep for F-08 "five"→"six" propagation; full V/C/K re-derivation for EC-03/EC-04 absent R-DOC-01 artifact recovery.

### 21.3 Implementation Phasing

Phasing follows the validation-spec's **10-step canonical commit sequence** (research-notes) for the merge proper, with **Phase 7.5 patch sprint** treated as a separate epic that runs in parallel post-Step-1 and converges before Step 6.

#### Phase A — Merge Proper (10-step canonical commit sequence)

| Step | Commit | Story | Gate |
|---|---|---|---|
| 1 | Land CR-TASK-12 baseline against still-present donor | S-E01-01 | AC-SM-08 (7 zero-diff invocations) |
| 2 | (research-implicit baseline) | — | — |
| 3 | (research-implicit baseline) | — | — |
| 4 | Land CR-7 + CR-8 sentinel / AST replacement | S-E01-02 | AC-ATK-01, AC-ATK-13 |
| 5 | Stubify `/sc:task` + author CR-DOC-01 doc row + emit sha256 | S-E01-03 | AC-ATK-09, AC-ATK-15, AC-SM-09, AC-SM-12 (gate at line 377) |
| 6 | Hard-delete donor SKILL.md + directory + `__init__.py` under rf-qa chain | S-E01-04 | AC-ATK-07, AC-SM-10, AC-SM-12 (gate at line 387), CR-DEP-04 |
| 7 | (post-Step-6 cleanup + sync) | — | `make verify-sync` (AC-ATK-16 `flock` discipline) |
| 8 | mkdocs build gate + CR-DOC-01 Step-8 fallback if Step-5 failed | S-E01-05 (a) | `mkdocs build` returns 0 broken-link warnings |
| 9 | Leave-as-is enforcement (CR-REF buckets A, C, D, E, F, G, H) | S-E01-05 (b) | CR-REF-12 grep |
| 10 | Deferred regen note for `docs/generated/*` | S-E01-05 (c) | CR-DEP-06 manifest archived |

#### Phase B — Phase 7.5 Patch Sprint (separate epic)

Phase 7.5 = **21 changes**: AC-ATK-01..18 + CR-DEP-06 + S-4 PRD timeout + S-5 rebase-ban (validation-spec § 16 line 435). Runs in parallel with Phase A from immediately after Step 1; **must converge before Step 6 hard-delete** so AC-ATK-07 verifier chain has the full predicate-precision set to verify against.

| Phase 7.5 stream | Stories | Convergence gate |
|---|---|---|
| Predicate-precision authoring | S-E02-01..04 | rf-qa Step 6 pre-commit chain returns PASS |
| V3 security-probe overlay | S-E03-01..03 | pre-push hook live on integration branch; flock landed in `make sync-dev`; CR-DEP-06 manifest emitter live |
| Sequencing-constraint additions | S-E04-01 (S-4); S-E04-02 encompassed by S-E03-02 | S-1 hierarchy (a) auto-invokes at 14d cap; rebase-ban server-side reject works on test push |

#### Phase C — In-flight Task Resumability (continuous post-Step-6)

| Story | Cadence |
|---|---|
| S-E05-01 (CR-FM-03 parse-layer shim) | Lands with Step 5 (default `Tier:` to STANDARD) |
| S-E05-02 (CR-FM-03 content gate-1.5) | Lands with Step 6 (resumed-task body grep) |
| S-E05-03 (CR-DEP-06 weekly emit) | Weekly post-Step-6; archived to `docs/generated/` per FM-06 disposition |

### 21.4 Release Criteria & Definition of Done

The release ships when **all** of the following are true:

#### 21.4.1 AC-ATK-01..18 Satisfied (all required; no [UNVERIFIED] exemptions)

| AC ID | DoD line | Status convention |
|---|---|---|
| **AC-ATK-01** | F-02 alternation-grep replaced by line-range-pinned `sed -n` + AST parse fixture for row-1 site `path_override_check → tier_field_validate → gate_1_dispatch` | required |
| **AC-ATK-02** | Five-row `git status` matrix (clean / dirty / tool-absent / not-a-repo / error-other) bound to CR-TASK-06; subprocess wrapper covers five exit-code regimes | required |
| **AC-ATK-03** | Baseline four-state table (absent / empty / parse-fail / schema-fail) with observation order pinned (`os.path.exists` → `os.path.getsize` → `yaml.safe_load` → schema) | required |
| **AC-ATK-04** | 79 → 65 condensation table authored (14+2+5+39+6+13 → 65); two duplicate CR-IDs in 67-row PASS roll-up named; PASS-verdict assignment stated | required |
| **AC-ATK-05** | Closed enumeration of authorized per-item marker consumers (`{CR-TASK-07 baseline-skip}`); future-expansion gate fires on unaudited consumer | required |
| **AC-ATK-06** | Donor strings snapshotted into `tests/fixtures/donor-blocks/` OR CR-TASK-12 marked Step-4-only with successor audit | required |
| **AC-ATK-07** | rf-qa verifier role rebound; spawned at Step 6 pre-commit; returns PASS before hard-delete commit | required |
| **AC-ATK-08** | `--max-wait` 14d default with auto-invoke option (b); pinned git-SHA at every `[CODE-VERIFIED]` tag in PRD final commit; CR-DEP-05 grep extends to post-Step-5 `[CODE-VERIFIED]` assertions against stubified body | required |
| **AC-ATK-09** | sha256sum substituted for md5sum in CR-TASK-11, CR-DEP-02, CR-DIST-02; expected digests re-baselined | required (LOW severity, mechanical) |
| **AC-ATK-10** | Unified pre-loop HALT policy table with input-invalid (HALT) vs environment-non-ideal (WARN-CONTINUE) rows | required |
| **AC-ATK-11** | F-05 either backed by retroactive ME-10 OR explicitly marked as one-time non-generalizing carve-out in source plan | required |
| **AC-ATK-12** | (a) CR-AUDIT-FM-03-SUNSET row authored; (b) seven-field `tfep-incident-report.md` schema enumerated (per S17.1); (c) CR-FM-01 canonicalization-rules table tabulated | required (three sub-bindings) |
| **AC-ATK-13** | CR-7 / CR-8 ordering either moved to executable artifact (pytest fixture / YAML schema / JSON manifest) OR sentinel claim downgraded from "binding" to "informational" with F-02 MEDIUM-severity closure removed | required |
| **AC-ATK-14** | (a) CR-DEP-05 grep scope specified (`find`/`grep` with extension + excluded-path flags); (b) CR-REF-18 cluster root path named; (c) CR-DEP-04 Step 6 pre-commit gate point fixed; (d) CR-DOC-13 R-RULE-11 scope decided (rename vs widen-to-65) | required (four sub-bindings) |
| **AC-ATK-15** | CR-DOC-01 lands Step 5 by default; Step 8 fallback only if Step 5 pre-commit gate fails AND hot-fix authorized | required |
| **AC-ATK-16** | `flock` discipline wraps prune loop on `.claude/skills/`; post-prune `find -type d` diff against expected directory set returns empty | required (V3 security-probe) |
| **AC-ATK-17** | Server-side pre-push hook re-greps `/sc:task\b` against `src/superclaude/cli/` on landing commit; rejects push if grep matches AND donor `task.md` body not deleted in same commit | required (V3 security-probe) |
| **AC-ATK-18** | (a) CR-FM-03 content-level resume grep `(/sc:task\b\|sc-task-protocol\|task-unified)`; (b) `gate-1.5: legacy-surface-reference detected ... action=warn-and-continue` emitted on match; (c) one-shot acknowledgment gate; (d) CR-DEP-06 post-Step-6 grep emitting structured manifest of every surviving residual outside authorized buckets | required (four sub-bindings; V3 security-probe) |

#### 21.4.2 AC-SM-01..12 Satisfied where artifact present; [UNVERIFIED] flags on artifact-absent rows

| AC ID | DoD line | Status |
|---|---|---|
| **AC-SM-01** | All eight V/C/K verdicts (TU-1..TU-8) match `transfer-manifest.md` § 4 byte-for-byte | **[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]** — `transfer-manifest.md` present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; byte-for-byte cross-check against PRD claims still owed (R-DOC-01 reframed) |
| **AC-SM-02** | Each ME-1..ME-9 traces to ≥1 CR-row acceptance-criterion or sequencing constraint via cross-grep against validation-spec §§ 5, 6 | required (intra-spec; validatable in-repo) |
| **AC-SM-03** | `invariant-survival-walkthrough.md` worked example demonstrates INV-01..INV-05 survive on the merged surface | **[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]** — walkthrough present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; invariant-survival cross-check against on-disk content still owed (R-DOC-01 reframed) |
| **AC-SM-04** | F-01..F-08 each cite a re-readable Phase 7 artifact line range | [VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED] — cascading on `final-merge-plan.md` (present on disk; line-range cross-check still owed) |
| **AC-SM-05** | S-1..S-3 each cite a named hazard (HZ-NN) in `compat-hazard-report.md` | **[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]** — `compat-hazard-report.md` present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; HZ-NN citation cross-check against on-disk content still owed (R-DOC-01 reframed) |
| **AC-SM-06** | 67-row count and 10-step commit sequence unchanged from `merge-master.md` § 1 + § 6 | **[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]** — `merge-master.md` present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; 67-row / 10-step cross-check against on-disk content still owed (R-DOC-01 reframed) |
| **AC-SM-07** | CR-FM-04 ordering greps return three function names in expected order against post-merge `task/SKILL.md` row-1 site | [VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED] — cascading on `final-merge-plan.md` source anchors (artifact present on disk; cross-check still owed) |
| **AC-SM-08** | CR-TASK-12 returns 7 zero-diff invocations (6 donor strings + 1 sentinel-comment block) | required (validatable post-Step-1) |
| **AC-SM-09** | Step 5 commit contains exactly the rows named at source line 375 of `final-merge-plan.md` | [VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED] — cascading (artifact present on disk; row-roster cross-check at line 375 still owed) |
| **AC-SM-10** | Step 6 commit contains exactly the rows named at source line 381 of `final-merge-plan.md` | [VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED] — cascading (artifact present on disk; row-roster cross-check at line 381 still owed) |
| **AC-SM-11** | Zero ledger entries from `rejected-features-ledger.md` re-proposed across the 65 distinct CR-IDs | **[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]** — `rejected-features-ledger.md` present at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` `[CODE-VERIFIED 2026-05-16 fix-cycle 2]`; re-proposal cross-check across 65 CR-IDs still owed (R-DOC-01 reframed) |
| **AC-SM-12** | Pre-commit gates for Steps 1, 5, 6 all return 0 on clean checkout | [VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED] — gate definitions cascade on `final-merge-plan.md` (present on disk; content audit owed); partial validation possible if gates are reconstructed in-repo |

**[CONTENT-AUDIT-OWED] disposition (fix-cycle 2 reframe).** AC-SM-01, -03, -05, -06, -11 are flagged `[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]` per the reframed R-DOC-01 (the original user-brief load-bearing five). All seven cited artifacts (`extension-point-contracts.md`, `transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `final-merge-plan.md`, `rejected-features-ledger.md`) were verified PRESENT on disk at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` on 2026-05-16 (fix-cycle 2). AC-SM-04, -07, -09, -10, -12 cascade on `final-merge-plan.md` and inherit the same status. AC-SM-02 and AC-SM-08 remain the only AC-SM rows fully validatable in-repo today. Release ships with these flags in place; disposition is no longer "retrieve vs relax vs defer" but rather "schedule the content audit and reconcile any drift discovered against on-disk artifact bodies" — the S13 Open Question Q-2 is reframed accordingly.

#### 21.4.3 Additional DoD Conditions

- All 21 Phase 7.5 changes (AC-ATK-01..18 + CR-DEP-06 + S-4 + S-5) landed on integration branch.
- `make verify-sync` green across 30-run window (K-04).
- Donor SKILL.md absent from disk post Step 6 (K-06); donor directory absent.
- 144 residual `/sc:task` occurrences eliminated or accounted for in CR-DEP-06 manifest (K-03).
- Sprint-runner pytest pass green post-CLI update (K-02).
- rf-qa Step 6 pre-commit chain PASS report archived alongside Step 6 commit.

### 21.5 Timeline & Milestones (ASCII)

Assumes a 4-week Phase 7.5 patch sprint running in parallel with the merge proper. Engineer-day ranges from § 18.2 fit a 1-engineer cadence at 4 days/week.

```
Week                W1            W2            W3            W4            W5
                    |-------------|-------------|-------------|-------------|-------------|
Phase A (merge)
  Step 1 baseline   |█|
  Step 4 sentinel   |  |██|
  Step 5 stubify    |        |████|
  Step 6 hard-del   |             |████|  ← rf-qa converges here
  Steps 7–8 sync    |                  |██|
  Step 9 leave-as-is|                     |██|
  Step 10 regen-def |                        |█|

Phase B (Phase 7.5)
  AC-ATK-01..04     |████|
  AC-ATK-05..08     |  |██████|
  AC-ATK-09..12     |       |██████|
  AC-ATK-13..15     |             |████|
  AC-ATK-16 flock   |                  |██|   ← lands before Step 7 sync
  AC-ATK-17 pre-push|                  |███|  ← lands before Step 6 push
  AC-ATK-18 + CR-DEP-06 |          |██████|   ← lands before Step 6 verifier
  S-4 --max-wait    |       |█|
  S-5 rebase-ban    |                  |███|  (encompassed by AC-ATK-17)

Phase C (resumability — continuous)
  S-E05-01 parse shim    (with Step 5)         |█|
  S-E05-02 content gate-1.5 (with Step 6)              |██|
  S-E05-03 weekly emit   (post-Step-6)                              |█|→ ongoing

MILESTONES
  M1: Step 1 baseline commit                  W1
  M2: Phase 7.5 predicate-precision converged W3 (gate for Step 6)
  M3: Step 5 stubify + sha256 + doc           W3
  M4: Step 6 hard-delete + rf-qa PASS         W4  ← release-candidate
  M5: Step 10 regen note + CR-DEP-06 manifest W4
  M6: Release ship (DoD § 21.4 all green)     W5
```

**Critical-path notes.**
- M2 (Phase 7.5 predicate-precision converged) is the gating milestone for M4 (Step 6). AC-ATK-07's rf-qa verifier role needs the full AC-ATK-01..15 set to verify against.
- AC-ATK-17 (server-side pre-push hook) must land before M4 because rebase-ban enforcement is server-side; without it, S-5 has no enforcement surface.
- AC-ATK-16 (flock) must land before Phase A's Step 7 sync step; otherwise, M4-to-M5 sync runs risk worktree race (K-04 degradation).
- AC-ATK-18 + CR-DEP-06 manifest emitter must land before M4 because Step 6 hard-delete fixes the residual-reference universe; the manifest must be emittable immediately post-delete.

---

---

## 22. Customer Journey Map

Two journeys are material: the **merge operator** executing the 10-step commit sequence (the primary actor), and the **resumed-task author** returning to an in-flight task post-merge (the secondary actor whose experience binds INV-04).

### 22.1 Journey Stages — Merge Operator (10-step commit sequence)

The 10-step sequence is the canonical execution order for the directional merge. Steps 5 and 6 are the moments of truth (see S22.3). Stage names below adapt the template's product-journey stages to the engineering-execution context — the mapping is one journey per step, then aggregated into the template's awareness/engagement/retention skeleton where the mapping holds.

| Stage | User Goal | Actions | Touchpoints | Emotions | Pain Points | Opportunities |
|-------|-----------|---------|-------------|----------|-------------|---------------|
| **Step 1 — Author CR-7 ORDERING sentinel + row-1 ordering** | Establish load-bearing `path_override_check() FIRST` ordering in post-merge `task/SKILL.md`; emit the canonical sentinel comment | Edit `src/superclaude/skills/task/SKILL.md` (source of truth); add CR-7 ORDERING comment; place `path_override_check()` at row 1; run `make sync-dev`; verify F-02 grep | `task/SKILL.md`; `make sync-dev`; F-02 grep script | Cautious — the sentinel is markdown-comment-only and is brittle to auto-generation (per validation-spec §12 second bullet, research-01 TU-2) | Sentinel can be stripped silently by any future auto-gen tool; markdown comments are not load-bearing to any interpreter | AC-ATK-01 hardens this to AST-level or line-pinned check; AC-ATK-13 considers downgrading "binding" claim to "informational" |
| **Step 2 — Widen Gate 2 roster to `[rf-qa, quality-engineer]`** | STRICT tier spawns quality-engineer ADDITIONALLY to rf-qa (never replacing); ME-2 floor preserved | Edit Phase-Gate QA section (`task/SKILL.md:181-211`) and Agent Spawning Conventions (`:290-299`); add `quality-engineer` to the catalog; ensure rf-qa remains present | `task/SKILL.md`; rf-qa agent definition; quality-engineer agent definition | Confident — donor already names quality-engineer; recipient already names rf-qa; the widening is the synthesis | None significant if ME-2 holds; risk if any audit row drops rf-qa | AC-SM-02 trace ME-2 anchoring to TU-3 row |
| **Step 3 — Author git pre-flight (TU-4) as warn-and-continue Task Log line** | Pre-F1 `git status` emission; never HALT | Author Task Log step at F1 entry; bind five `git status` dispositions per CR-TASK-06; map each to `{WARN-CONTINUE, GRACEFUL-SKIP}` | `task/SKILL.md`; AC-ATK-02 five-row matrix; AC-ATK-10 unified pre-loop HALT policy table | Careful — must avoid authoring new HALT semantics that INV-01 forbids | Asymmetry with input-invalid HALT category (AC-ATK-10 disambiguation — see S23) | AC-ATK-02 five-row matrix locks the disposition table |
| **Step 4 — Author baseline-snapshot step (TU-5) writing YAML to disk** | `${TASK_DIR}/research/test-baseline.yaml` written pre-F1; survives session boundary | Author pre-F1 baseline step; invoke `uv run pytest --collect-only -q` or equivalent; persist as YAML; bind four on-disk states `{absent, empty, parse-fail, schema-fail}` per AC-ATK-03 | `${TASK_DIR}/research/`; pytest collect-only output; AC-ATK-03 disambiguation | Cautious — `null` YAML disambiguation (research-01 Gap #2; spec §10 Scenario C) | Trinary collapse `{absent, empty, malformed}` is ambiguous at observer-order layer | AC-ATK-03 four-state disambiguation pins observer order |
| **★ Step 5 — Stubify `/sc:task` (CR-DEP-01)** | `commands/sc/task.md` and `commands/task.md` deprecation surfaces emit canonical message; F1 loop NOT executed | Replace command body with the seven-element deprecation message (F-16.2.4 text); set exit 0; ensure CR-FM-03 default-fall-through is still active for any tool that bypasses the stub | `commands/sc/task.md`; `commands/task.md`; CR-DEP-06 residual-reference manifest | **Apprehensive — this is the moment in-flight tasks first see the deprecation.** Operator must validate the manifest grep covers all live union files (132 at 2026-05-16 fix-cycle 2; 130 at fix-cycle 1; population dynamic — research-03 §6's earlier 25-file figure was a narrower-scope snapshot at research-time) | If the deprecation message text drifts from the canonical seven elements, AC-ATK-18 grep may miss it; if CR-DEP-06 manifest is incomplete, residual `/sc:task` invocations in `.dev/releases/backlog/` (61) or `docs/generated/` (83) silently degrade | **MOMENT OF TRUTH 1 (S22.3).** Stubification is reversible; failure rolls back via `git revert` |
| **★★ Step 6 — Hard-delete donor `sc-task-protocol/` (CR-DEP-03)** | Donor SKILL.md removed from filesystem; recipient `task/` is sole skill | `git rm -r src/superclaude/skills/sc-task-protocol/`; run `make sync-dev`; run `make verify-sync` | Filesystem; git; CR-DEP-06 manifest | **Highest tension of the sequence — this is irreversible without git revert.** Any in-flight subagent prompt that `Read`s `src/superclaude/skills/sc-task-protocol/SKILL.md` will FileNotFoundError post-delete | H-4 scenario (research-03 §4): `TASK-RESEARCH-20260403-sprint-task-exec` may have subagent prompts that resolve to deleted paths; INV-04 semantic guarantee can break here | **MOMENT OF TRUTH 2 (S22.3).** CR-DEP-06 manifest must have been validated complete before this step; rollback is `git revert` but emotional cost is high |
| **Step 7 — Author CR-FM-03 compat shim audit row** | Frontmatter shim default-fall-through to STANDARD documented; CR-AUDIT-FM-03-SUNSET row authored with binding `N` | Edit audit-row registry; bind sunset condition per Q-S13 OQ-FM-03-SUNSET (recommended: `N=50 generations AND ≥90 days AND CR-MIGR-FM-03 authored`) | Audit-row registry; CR-MIGR-FM-03 forward stub | Methodical — this is bookkeeping but load-bearing for downstream sunset behavior | Sunset value of `N` is unbound today (research-03 §5); engineering lead confirmation required | OQ-FM-03-SUNSET resolution before Step 7 lands |
| **Step 8 — TFEP transfer (TU-5..TU-8)** | Donor §4.5 TFEP block (sc-task-protocol/SKILL.md:125-244) transferred into recipient; mid-phase rf-qa invocation added as third invocation point; incident-report seven-field schema authored | Author TFEP prohibitions catalog (additive to F2), escalation trigger detection, execution flow (6 steps), incident-report schema | `task/SKILL.md`; F-05 three-prong defense citation; AC-ATK-11, AC-ATK-12 | Confident — the donor block is contiguous and well-shaped; the F-05 three-prong defense is the load-bearing INV-03 widening (research-01 TU-7) | Precedent risk: F-05 establishes paragraph-level surface-widening precedent (validation-spec §5.7); future widenings may invoke the same pattern | AC-ATK-11 binds F-05 as one-time non-generalizing carve-out |
| **Step 9 — `make sync-dev` + `make verify-sync`** | `.claude/skills/task/` and `.claude/commands/task.md` reflect `src/superclaude/` source of truth | Run sync; verify zero-diff | `make` targets; `.claude/` mirror | Routine | None expected if Steps 1-8 were clean | Sync hooks confirm source-of-truth discipline |
| **Step 10 — Post-merge audit + downstream consumer notification** | All AC-SM rows pass; CR-DEP-06 residual-reference manifest published; H-4 case study (`TASK-RESEARCH-20260403-sprint-task-exec`) operator-notified for resume-time acknowledgment | Run AC-SM verification suite; publish manifest; notify owners of the live union files (132 at 2026-05-16 fix-cycle 2; population dynamic; research-03 §6's earlier 25-file figure was a narrower-scope snapshot at research-time) | AC-SM-01..12; CR-DEP-06; in-flight task owners | Relief mixed with watchfulness — the merge has landed but the shim is now load-bearing for 100% of the in-flight surface (research-03 §5) | If any residual `/sc:task` reference in `.dev/releases/backlog/` (61 files) or `docs/generated/` (83 files) blows up downstream, blast radius is large | Forward-looking `gate-1.4: shim-status` emission provides operator visibility into sunset countdown |

### 22.2 Journey Stages — Resumed-Task Author

Applies to the engineer (or agent) who opens an in-flight task post-merge. The 132 live union files referencing donor surfaces (2026-05-16 fix-cycle 1 live recount, `rg -l ... .dev/tasks/ | wc -l`; supersedes earlier research-03 §6 narrower 25-file snapshot) are the canonical population; the surviving named-exposure target `TASK-RESEARCH-20260403-sprint-task-exec` (**48 donor-surface occurrences across 10 files** in subtree, 2026-05-16 fix-cycle 1) is the binding case study.

| Stage | User Goal | Actions | Touchpoints | Emotions | Pain Points | Opportunities |
|-------|-----------|---------|-------------|----------|-------------|---------------|
| **Awareness** | Discover that the merge has landed and the task may reference deprecated surfaces | Read release notes; see CR-DEP-06 manifest notification; observe one of the live union files in their queue (132 at 2026-05-16 fix-cycle 2; population dynamic; research-03 §6's earlier 25-file figure was a narrower-scope snapshot at research-time) | Release notes; CR-DEP-06 manifest; team channel | Mild concern — "is my task affected?" | If no proactive notification, author may not know until L2 grep fires at resume | Step 10 proactive notification eliminates this gap |
| **Consideration** | Decide whether to resume the task as-is, rewrite the affected prose, or close + re-author | Cross-reference task's `/sc:task` occurrence count against CR-DEP-06 manifest; read research-03 §3 layer table | Task subtree; manifest; INV-04 layer table | Cautious analytical — wants to understand L1/L2/L3 exposure | If the layer table is opaque, author may overestimate or underestimate risk | F-16.2.3 transparency: AC-ATK-18 grep surfaces exactly which files contain which symbols |
| **Acquisition** | Invoke `/task <file>` (post-merge invocation) | `/task` (NOT `/sc:task` — the latter is stubified post-Step-5) | Post-merge command surface | Routine if AC-ATK-18 message is clear; confused if author still types `/sc:task` | If author types `/sc:task`, they see the deprecation message (F-16.2.4); behavior is graceful but adds a step | Deprecation message's seven elements teach the canonical replacement |
| **Onboarding (L1 parse)** | Skill validates frontmatter and assigns tier (CR-FM-03 default → STANDARD if no `Tier:` field) | Skill loads task file; emits `gate-1.4: shim-status` line | Skill output; Task Log | Trust — file parses; STANDARD is reasonable default | If CR-FM-03 sunset has fired (post-Q-S13 resolution), missing `Tier:` becomes input-invalid HALT (AC-ATK-10) — author must add field | OQ-FM-03-SUNSET resolution publishes the deadline forward |
| **First Value (L2 semantic scan)** | AC-ATK-18 resume-time grep runs; warns on any matched deprecation surface | Skill emits `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` for each match (recursive over task subtree + `related_docs:` find-traversal) | Task Log; one-shot acknowledgment gate | If surviving named-exposure target (48 donor-surface occurrences across 10 files in subtree, 2026-05-16 fix-cycle 1): mild fatigue but warn-and-continue dispatch is correct | Resume-fatigue if every resume re-prompts; one-shot gate (F-16.2.3 step 4) addresses this | Author can use the grep output as a worklist for incremental cleanup |
| **Engagement (L3 execution)** | F1 loop iterates checklist items; subagents fire only when an item requires them | Standard F1 progression; if a subagent prompt references a deleted donor path, `Read` raises and the F1 transitions task to `⚪ Blocked` per INV-01 | F1 loop; subagent spawn pattern; `⚪ Blocked` status | Risk of frustration if a subagent fails mid-loop | H-4 scenario: irrecoverable failure path if `related_docs:` references a deleted donor file and the subagent prompt names it explicitly | F-16.2.3 step 3(c) catches this at resume time, BEFORE the F1 transitions; provides actionable pre-flight |
| **Retention** | Task completes (or is intentionally re-scoped after AC-ATK-18 surfaced issues); incident report emitted if TFEP fired | Standard completion path; possible `tfep-incident-report.md` emission | TFEP incident report (F-16.2.5); QA reports; done/ move | Confidence restored; learns the canonical post-merge workflow | If author closed task without addressing flagged surfaces, residual-reference manifest will reflect this | Post-merge audit (Step 10) catches incomplete cleanups |
| **Advocacy** | Author recommends the AC-ATK-18 / CR-FM-03 / Tier-field discipline to teammates; contributes to roadmap residual cleanups | Reviews CR-DEP-06 manifest; closes any of the live union files they own (132 at 2026-05-16 fix-cycle 2; population dynamic; research-03 §6's earlier 25-file figure was a narrower-scope snapshot at research-time) | Manifest; PR reviews | Positive — saw the system handle deprecation gracefully | None significant | Builds organizational muscle for the next directional merge |

### 22.3 Moments of Truth

| Moment | Description | Success Criteria | Failure Recovery |
|--------|-------------|------------------|------------------|
| **MoT-1 — Step 5 stubification** | The instant `/sc:task` stops executing the F1 loop and starts emitting the canonical seven-element deprecation message instead. First time the post-merge contract is visible to external callers. | All in-flight invocations during the stubification window receive the deprecation message (no silent no-op, no error code, no HALT). CR-DEP-06 residual-reference manifest is published and validated complete BEFORE the commit lands. F-16.2.4 seven elements are all present in the stub body. | `git revert` the stubification commit; restore the donor command body; re-author message after validating CR-DEP-06 completeness. Low cost — stubification is a single file change. |
| **MoT-2 — Step 6 hard-delete of donor `sc-task-protocol/`** | The instant the donor skill directory is removed from the filesystem. Irreversible without `git revert`. Any in-flight subagent prompt that resolves `Read('.../sc-task-protocol/SKILL.md')` now raises FileNotFoundError. | All known references in CR-DEP-06 manifest have been validated; `TASK-RESEARCH-20260403-sprint-task-exec` operator has been notified; `make verify-sync` returns clean post-delete; no AC-SM row fails. INV-01 holds by transition for any task that hits H-4 (task goes to `⚪ Blocked`, not crashed). | `git revert` the delete commit; restore donor SKILL.md; re-validate CR-DEP-06 with stricter grep including `related_docs:` find-traversal; retry. Higher emotional cost than MoT-1 because reverting a delete is psychologically harder than reverting a body change. |
| **MoT-3 — First resume of `TASK-RESEARCH-20260403-sprint-task-exec` post-Step-6** | The binding H-4 case (research-03 §4). Surviving named-exposure target with **48 donor-surface occurrences across 10 files** in subtree (research / synthesis / qa) per 2026-05-16 fix-cycle 1 recount. First real-world test of AC-ATK-18 + INV-04 semantic guarantee. | AC-ATK-18 resume-time grep surfaces all 10 files; `gate-1.5` Task Log lines fire for each; one-shot acknowledgment gate appears; operator confirms; F1 enters with STANDARD tier (CR-FM-03 default). Task either resumes or transitions to `⚪ Blocked` cleanly. No FileNotFoundError reaches the operator without a `gate-1.5` having warned first. | If the grep misses a file, treat as a manifest gap and back-fill; if a subagent crashes on a missing donor path that the grep DID surface, the warn-continue disposition was honored — operator addresses the prose. If a subagent crashes on a path the grep did NOT surface, this is an AC-ATK-18 scope gap (recommended scope per research-03 §4: task body + subtree siblings + `related_docs:` find-traversal). |

---

---

## 23. Error Handling & Edge Cases

### 23.1 Error Categories

| Category | Examples | User Experience | Recovery |
|----------|----------|-----------------|----------|
| **Validation Errors (input-invalid, HALT per AC-ATK-10)** | (a) `Tier:` field present but value not in `{STRICT, STANDARD, LIGHT, EXEMPT}`; (b) frontmatter missing required field (`id`, `title`, `status`, `created_date`); (c) post-CR-FM-03-sunset task file with no `Tier:` field; (d) classification header emitted with invalid tier or in wrong format | HALT before F1 entry; explicit error message naming the field and the allowed values; task NOT transitioned (operator must fix and re-invoke) | Operator edits frontmatter; re-invokes `/task <file>`. No partial state to clean up — HALT is pre-loop. |
| **Environment-Non-Ideal Errors (warn-and-continue per AC-ATK-10)** | (a) `git status` returns dirty tree (CR-TASK-06 disposition: `dirty` → WARN-CONTINUE); (b) `git status` returns tool-absent / not-a-repo / error-other (CR-TASK-06 dispositions per spec §10 Scenario B); (c) baseline YAML absent / empty / parse-fail / schema-fail (AC-ATK-03 four-state); (d) AC-ATK-18 resume-time grep matches a deprecation surface in task subtree or `related_docs:` find | Task Log line emitted (`gate-1.4` / `gate-1.5` / pre-F1 git-status line); F1 proceeds without HALT; INV-01 monotonicity preserved | None required — the warn-and-continue disposition is the recovery. Operator may address the warning at their pace; subsequent resumes do not re-prompt (one-shot acknowledgment for `gate-1.5`). |
| **TFEP Escalation Triggers (research-01 TU-7)** | (a) Pre-existing test fails (per baseline classification); (b) 3+ new tests fail; (c) runtime exception in implementation code; (d) escalation gradient hits: repeated failure, multi-file blast radius, low-confidence root cause, unresolved adversarial outcome, second failed retest, cross-domain regression | F1 halts the current item, freezes state, constructs 9-field failure context YAML, invokes forensic subagent (third rf-qa invocation point — F-05 authorized); resolution either resumes F1 with adjudicated remediation plan or escalates to FULL STOP after three rungs of the budget ladder (~5–8K → ~15–20K → FULL STOP) | TFEP execution flow's 6 steps handle this end-to-end. After resolution (success or escalation), `tfep-incident-report.md` is written per F-16.2.5. F1 resumes with `--compliance strict`; re-runs test suite; loops or succeeds. |
| **L3 Integration Errors (post-Step-6 deleted-donor reference)** | (a) Subagent prompt names `src/superclaude/skills/sc-task-protocol/SKILL.md` as `Read` target (FileNotFoundError); (b) Bash step invokes `/sc:task ...` (hits stubified surface, gets deprecation message + exit 0 — handled gracefully if invoker checks output, undefined if invoker assumed F1 execution); (c) `related_docs:` frontmatter cites a deleted donor path | F1 transitions task to `⚪ Blocked` per its own exception clauses; INV-01 holds by transition; the `⚪ Blocked` transition is visible in the task file's frontmatter; operator sees a stop-state but not a crash | Operator edits the offending subagent prompt / Bash step / `related_docs:` entry to remove the deleted-donor reference; re-invokes `/task`. AC-ATK-18 pre-flight grep should have surfaced this at L2 — if not, this is a scope gap to back-fill per research-03 §4. |
| **Timeout / Resource Errors** | (a) Forensic subagent exceeds TFEP escalation budget (3rd rung → FULL STOP); (b) baseline pytest collect-only hangs; (c) AC-ATK-18 recursive grep timeout on a large `related_docs:` traversal | TFEP FULL STOP emits `tfep-incident-report.md` with `Outcome: escalated` (donor literal per `sc-task-protocol/SKILL.md:232` `[CODE-VERIFIED]`); operator notified via task status transition; F1 does not proceed | Operator reviews incident report; chooses to manually resolve, re-scope the task, or escalate further. No autonomous retry — FULL STOP is terminal. |

#### 23.1 Detail — AC-ATK-10 Disambiguation (input-invalid HALT vs environment-non-ideal WARN-CONTINUE)

Per validation-spec §5.2 (lines 122-128) and research-01 TU-4: the dispositions for pre-loop checks fall into two distinct categories with different HALT semantics. The disambiguation is load-bearing because INV-01 forbids new HALT semantics in the F1 loop, so any HALT must be pre-loop AND must be classified as input-invalid (not environment-non-ideal).

| Class | Disposition | Examples | INV protected |
|---|---|---|---|
| **input-invalid** | HALT (pre-loop only; NEVER inside F1) | Invalid `Tier:` enum value; malformed frontmatter; missing required field; post-sunset missing `Tier:` field | INV-05 (refusal-of-definition — invalid input is not a work-definition the agent must accept); INV-01 (HALT is pre-loop, not in-loop) |
| **environment-non-ideal** | WARN-CONTINUE (Task Log emission; F1 proceeds) | Dirty git tree; tool-absent (`git` not installed, exit 127); not-a-repo; baseline YAML absent/empty/parse-fail/schema-fail; AC-ATK-18 legacy-surface-reference match | INV-01 (no new HALT semantics introduced); ME-3 (refuse-entry would weaken INV-01) |

**Operator-facing rule.** If you can fix it by editing the task file → input-invalid → HALT, fix file, re-invoke. If you can fix it by changing the environment OR if it's a documentation surface that doesn't block correctness → environment-non-ideal → WARN-CONTINUE, F1 proceeds, you address the warning at your pace.

### 23.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| **INV-04 parse-vs-semantic boundary (research-03 §3)** | An in-flight task file parses cleanly at L1 (frontmatter valid; CR-FM-03 default → STANDARD) but contains `/sc:task` references in its checklist / prose / synthesis siblings. L1 says "INV-04 holds." L2 grep says "deprecation surfaces present, warn-and-continue." L3 execution may fail on a subagent `Read`. **All three layers can return different verdicts for the same file.** PRD MUST split INV-04 into FR-INV-04-PARSE (L1 — mechanical, holds for all 132 live files per 2026-05-16 fix-cycle 2; 130 live at fix-cycle 1 — population dynamic) and FR-INV-04-SEMANTIC (L2+L3 — requires AC-ATK-18). | Take `TASK-RESEARCH-20260403-sprint-task-exec` (canonical case: **48 donor-surface occurrences across 10 files** in subtree, 2026-05-16 fix-cycle 1, status `🟠 Doing`). Verify: (a) frontmatter parses; (b) AC-ATK-18 grep matches all 10 files; (c) one-shot `gate-1.5` acknowledgment appears on first resume; (d) F1 enters with STANDARD; (e) if a subagent later fails on a deleted donor path, task transitions to `⚪ Blocked`. All five behaviors must hold in sequence. |
| **CR-7 ORDERING sentinel stripped by auto-gen** | If a future tool auto-regenerates `task/SKILL.md`, the canonical sentinel — an **HTML comment** `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->` (form unified with synth-05 §24.2 / §25.1.2 at fix-cycle 1 2026-05-16; HTML-comment form chosen because it does not render in Markdown views and serves as an out-of-band machine-grep anchor) — may be stripped silently (validation-spec §12 second bullet). The F-02 alternation grep would still pass against the function names if their order is preserved, but the sentinel-presence grep `grep -n '<!-- CR-7 ORDERING' src/superclaude/skills/task/SKILL.md` would fail. | Run `make sync-dev` followed by the canonical sentinel grep `grep -n '<!-- CR-7 ORDERING' src/superclaude/skills/task/SKILL.md` (matches synth-05 §25.1.2 audit grep verbatim). Verify match. Then simulate auto-gen (e.g., a hypothetical regenerator that strips top-level comments) and verify the grep correctly reports MISSING. AC-ATK-01 hardens to AST-level check; AC-ATK-13 considers downgrading "binding" to "informational" if AST check is too brittle. |
| **TU-7 mid-phase rf-qa invocation precedent risk (F-05 closure)** | The third rf-qa invocation point (mid-phase, triggered by TFEP) reuses rf-qa identity, uses the existing spawn pattern at `task/SKILL.md:191-198`, and is named by TU-7. The F-05 three-prong defense authorizes this widening but ALSO establishes a paragraph-level surface-widening precedent procedurally cheaper than authoring a manifest exception. Future widenings may invoke the same pattern with weaker justification. | Verify post-merge: (a) rf-qa is spawned at all three invocation points (phase-gate QA, post-completion validation, mid-phase TFEP); (b) ME-2 floor holds — rf-qa is never replaced by quality-engineer in any invocation; (c) AC-ATK-11 marks F-05 as one-time non-generalizing carve-out OR retroactive ME-10 backing exists; (d) no fourth rf-qa invocation point is silently added without invoking AC-ATK-11 again. |
| **Baseline YAML `null` content (spec §10 Scenario C)** | A `${TASK_DIR}/research/test-baseline.yaml` file containing 5 bytes (`null\n`) parses to a Python `None`. Observer 1 (`yaml.safe_load`) calls it `empty`. Observer 2 (`os.path.getsize`) calls it not-empty (5 bytes). AC-ATK-03 four-state disambiguation `{absent, empty, parse-fail, schema-fail}` requires observer order to be pinned: load FIRST, size as tiebreaker. Disposition for all four states: classification=new (over-escalate per F-04 closure). | Write 5-byte file with literal `null\n`. Run baseline detector. Verify it reports `empty` (not `parse-fail`). Verify F1 classifies subsequent test failures as `new` (over-escalate path). Verify no rf-qa overload alarm fires until queue-saturation threshold. |
| **`git status` exit 127 (tool-absent, spec §10 Scenario B)** | CI worker image has `git` removed. Pre-F1 `git status` exits 127. CR-TASK-06 disposition: `tool-absent` → WARN-CONTINUE (per AC-ATK-02 five-row matrix). F1 proceeds without baseline cleanliness check. | Run pre-F1 in a container with `which git` returning nothing. Verify Task Log line `pre-flight: git-status tool-absent action=warn-and-continue` emitted. Verify F1 proceeds. Verify NO HALT. |
| **CR-FM-03 shim sunset binding** | Per Q-S13 OQ-FM-03-SUNSET (research-03 §5): the shim must have a binding sunset condition. Recommended: `N=50 task generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 row authored`. Pre-sunset: missing `Tier:` → STANDARD (warn). Post-sunset: missing `Tier:` → input-invalid HALT (per AC-ATK-10). The audit row CR-AUDIT-FM-03-SUNSET emits at every resume: `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<int> sunset_row_authored=<bool>`. | Pre-sunset: open in-flight task with no `Tier:`. Verify warn-and-continue. Open 50th post-merge new task. Verify `gate-1.4` reports `generations_remaining=0`. Author CR-MIGR-FM-03 row. Reopen old task with no `Tier:`. Verify input-invalid HALT message. |
| **CR-DEP-06 residual-reference manifest gap** | After CR-DEP-06 manifest is published, a downstream consumer in `.dev/releases/backlog/` (61 residual `/sc:task` occurrences) or `docs/generated/` (83 residual occurrences) may still reference the deprecated surface. The manifest exists to enumerate these explicitly so they are not surprises post-Step-6. | Run `grep -R -c "/sc:task\b" .dev/releases/backlog/ docs/generated/` post-Step-10. Verify count matches manifest entries. If not, manifest has a gap and must be back-filled before any further downstream cleanup commits land. |

### 23.3 Graceful Degradation

| Component Failure | Degraded Experience | User Communication |
|-------------------|--------------------|--------------------|
| **CR-7 ORDERING sentinel missing** | `path_override_check()` may still be at row 1 (function-order grep passes), but the load-bearing comment that documents the ordering is gone. Behavior is correct as long as function order is preserved. | F-02 grep reports `sentinel missing; function order verified`. Operator restores sentinel from canonical text. |
| **CR-FM-03 shim active but sunset value unbound (pre-Q-S13 resolution)** | Tasks without `Tier:` field default to STANDARD indefinitely. No data loss. No incorrect routing for the STANDARD-classified work. Open question is forward-looking sunset, not current behavior. | `gate-1.4: shim-status sunset_row_authored=false generations_remaining=unbound`. Operator escalates Q-S13 to engineering lead. |
| **AC-ATK-18 grep scope incomplete (e.g., misses `related_docs:` traversal)** | L2 detection passes for task body but not for path-level PRIMARY ARTIFACTS named in `related_docs:`. L3 may then surface the failure as a FileNotFoundError mid-F1. Task transitions to `⚪ Blocked` (INV-01 holds by transition). | Operator sees `⚪ Blocked` status with no prior `gate-1.5` warning — this is a scope gap. AC-ATK-18 scope is updated to include `related_docs:` find-traversal per research-03 §4 recommendation. |
| **TFEP forensic subagent unavailable** | Mid-phase rf-qa cannot be spawned. TFEP execution flow Step 3 fails. F1 cannot adjudicate the failure autonomously. | Task transitions to `⚪ Blocked`. `tfep-incident-report.md` written with `Outcome: escalated` (donor literal per `sc-task-protocol/SKILL.md:232` `[CODE-VERIFIED]`) plus a free-form annotation `Reason: forensic-unavailable`. Operator manually resolves. |
| **Deprecation stub message text drifts** | If the seven-element canonical text is edited away from its locked form, AC-ATK-18 detection becomes less reliable (downstream tooling expecting specific phrases may miss matches). Behavior is functionally degraded but not broken. | Step-10 audit catches drift; operator restores canonical text per F-16.2.4. |
| **Hard-delete (Step 6) leaves orphan references in `.claude/`** | If `make sync-dev` was not run after Step 6, `.claude/skills/sc-task-protocol/` may persist as an orphan despite being removed from `src/superclaude/`. The orphan is read by Claude Code at session start and would resurrect the donor surface at runtime. | `make verify-sync` returns non-zero with the orphan listed. Operator runs `make sync-dev` (or manually `rm -rf .claude/skills/sc-task-protocol/`) and re-verifies. |

---

---

## 24. User Interaction & Design

Per S24 template (`src/superclaude/examples/prd_template.md:1104-1128`), this PRD has **no UI / no wireframes / no design system / no prototypes**. The artefact is a Markdown file (`src/superclaude/skills/task/SKILL.md`) whose post-merge structure is the design that must be specified. This section describes the structural design only — the line-level authoring instructions for Step 1 belong to the implementation plan (synth-08).

### 24.1 Top-of-file ordering contract (row 1)

The post-merge recipient SKILL.md MUST establish a "row 1" structural anchor that pins the F1 loop dispatch ordering. Three call-site names are introduced (none of which exist as defined functions in the current donor or recipient SKILL.md or in `src/superclaude/commands/task.md` — verified end-to-end; research 01 Gaps #5):

| Order | Call-site | Purpose | INV protected |
|---|---|---|---|
| 1 | `path_override_check()` | Apply TU-2 Critical Path Override (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) and Trivial Path Override (`*.md`, `docs/`, `*test*.py`) before any tier resolution. Donor source: `src/superclaude/skills/sc-task-protocol/SKILL.md:121, 123` `[CODE-VERIFIED]`. | INV-05 (refusal-of-definition: override is a routing read, not a re-definition); INV-01 (F1 loop semantics preserved — override decided pre-loop). |
| 2 | `tier_field_validate()` | Read the frontmatter `Tier:` field (TU-1) and assert membership in `{STRICT, STANDARD, LIGHT, EXEMPT}` (canonical tier set per `src/superclaude/commands/task.md:55, 61` `[CODE-VERIFIED]`). On absent `Tier:`, default-classify via the CR-FM-03 compatibility shim. | INV-04 (resumability — pre-merge files without `Tier:` still parse); INV-05. |
| 3 | `gate_1_dispatch()` | Route to the per-tier execution path (STRICT / STANDARD / LIGHT / EXEMPT). This is where the donor's `src/superclaude/skills/sc-task-protocol/SKILL.md:80-91` STRICT checklist is absorbed. | INV-01 (no new HALT introduced); INV-03 (Phase-gate rf-qa floor preserved). |

**Wrong-order bait scenario.** `validation-spec.md:296` (Scenario A) shows `tier_field_validate(); path_override_check(); gate_1_dispatch()` as the failing case — `tier_field_validate` races ahead and resolves a tier the path override would have superseded. The CR-7 ORDERING sentinel below is the structural guard against this.

### 24.2 CR-7 ORDERING sentinel (authored at Step 1)

**Sentinel literal:**

```
<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->
```

| Property | Value / Evidence |
|---|---|
| Current existence | **Absent from both donor and recipient SKILL.md** as of 2026-05-16 (verified end-to-end; research 01 Gaps #4). |
| Author event | Step 1 of the directional merge — pre-flight to all other TU absorption. |
| Location | Immediately above the row-1 `path_override_check()` reference in the post-merge `src/superclaude/skills/task/SKILL.md`. |
| Audit binding | CR-FM-04 ordering grep returns the three function names in expected order against `src/superclaude/skills/task/SKILL.md` (AC-SM-07, `validation-spec.md:359`). CR-TASK-12 returns 7 zero-diff invocations (AC-SM-08, `validation-spec.md:360`). |
| Spec attack to address | `validation-spec.md:116-120` § 5.1 — "markdown comments are not load-bearing to any interpreter — they are documentation. The 'ordering' is procedural, not enforced." Mitigation: AC-ATK-01 (line-range-pinned or AST-level check) and AC-ATK-13 (downgrade sentinel claim from 'binding' to 'informational' OR move into executable artifact) — addressed in Phase 7.5 audit-row design. |
| Secondary attack | `validation-spec.md:373` § 12 second bullet — "If SKILL.md is auto-generated by any future tool, sentinel comments could be stripped without triggering grep." Mitigation: CR-FM-04 line-range pinning. |

### 24.3 F1 loop dispatch — post-merge call ordering

The recipient F1 loop today (`src/superclaude/skills/task/SKILL.md:79-98` `[CODE-VERIFIED]`) contains only READ/IDENTIFY/EXECUTE/UPDATE/REPEAT — no tier-dispatch step, no path-override step, no `git status` step. Post-merge the loop entry is preceded by the three-call dispatch row described in §24.1.

| Phase | Step | Source-of-truth |
|---|---|---|
| Pre-F1 (added) | (a) Read frontmatter; (b) CR-7 ORDERING sentinel marker; (c) `path_override_check()` (TU-2); (d) `tier_field_validate()` (TU-1); (e) `gate_1_dispatch()` (TU-1 / TU-3 / TU-4); (f) TU-5 baseline snapshot write; (g) TU-4 `git status` Task Log emission (warn-and-continue, NOT HALT per ME-3 / AC-ATK-02). | Authored at Step 1. |
| F1 loop (preserved) | READ → IDENTIFY → EXECUTE → UPDATE → REPEAT, unchanged structurally to preserve INV-01 (progress monotonicity). Per-item `(Tier: X)` markers (TU-1) read only — never dispatch. | `src/superclaude/skills/task/SKILL.md:79-98` `[CODE-VERIFIED]`. |
| Phase-gate QA (widened) | Spawn `rf-qa` (preserved by ME-2) + `quality-engineer` for STRICT tier (TU-3 widening). | Recipient `src/superclaude/skills/task/SKILL.md:191-198` `[CODE-VERIFIED]` (currently rf-qa only). |
| Post-completion validation | `rf-qa` structural + `rf-qa-qualitative` operational. Unchanged. | Recipient `src/superclaude/skills/task/SKILL.md:219-241` `[CODE-VERIFIED]`. |
| Mid-phase rf-qa (TU-7, F-05 authorized widening) | THIRD rf-qa invocation point, triggered by TFEP escalation gradient. Routes to existing rf-qa identity (preserves ME-2); reuses spawn pattern from `:191-198` (F-05 three-prong defense per `validation-spec.md:154-158` § 5.7). | Authored at Step 1 alongside TU-5..TU-8 TFEP block. |

### 24.4 TFEP baseline-snapshot adaptation (TU-5: in-memory → on-disk)

Donor (`src/superclaude/skills/sc-task-protocol/SKILL.md:144-154` `[CODE-VERIFIED]`) specifies an **in-memory** baseline. Validation-spec § 2 line 53 / § 4 lines 100-104 require **adaptation to on-disk YAML** at `${TASK_DIR}/research/test-baseline.yaml`, written pre-F1, because in-memory baseline breaks INV-04 across resumption.

| Aspect | Donor (in-memory) | Post-merge (on-disk) | INV / rationale |
|---|---|---|---|
| Storage medium | In-process variable for task duration (donor `src/superclaude/skills/sc-task-protocol/SKILL.md:147`: "Store this baseline in memory for the duration of the task") `[CODE-VERIFIED]` | YAML file at `${TASK_DIR}/research/test-baseline.yaml` | INV-04 — disk persistence survives session boundaries / Claude restarts / `--continue` re-entry. |
| Capture timing | Pre-implementation, at task start | Pre-F1, after Phase-1 directory creation (`research/`, `synthesis/`, `qa/`, `reviews/` per `src/superclaude/skills/task/SKILL.md:205, 274` `[CODE-VERIFIED]`) | INV-03 (Phase-gate rf-qa floor — baseline enables the pre-existing vs new classification rf-qa relies on). |
| Trinary states (F-04 closure) | "pre-existing vs new" (binary, in-memory) | Three on-disk states {`absent`, `empty`, `malformed`} all classified to `new` per F-04 — but spec § 5.5 attacks the collapse: a `null\n` body is `empty` to `yaml.safe_load` but not-empty to `os.path.getsize`. | AC-ATK-03 (`validation-spec.md:332`) disambiguates to four states {`absent`, `empty`, `parse-fail`, `schema-fail`} with observation order pinned. |
| Classification driver | MUST-escalate vs MAY-fix-directly (donor `src/superclaude/skills/sc-task-protocol/SKILL.md:153`) | Same predicate; reads from the on-disk YAML at every resume. | TU-5 closure preserves donor semantics; only the storage medium changes. |
| Failure-floor | None | Over-escalate on absent / empty / malformed; F-04 closure per `validation-spec.md:32, 142-146` | Spec § 12 fourth bullet (line 375): "Over-escalate floods the rf-qa queue" — acknowledged residual; AC-ATK-03 disambiguation is the lever. |

### 24.5 In-scope file design impact (post-merge structural map)

| File | Role | Change |
|---|---|---|
| `src/superclaude/skills/task/SKILL.md` | Recipient (canonical post-merge) | Authored to receive TU-1..TU-8 + CR-7 ORDERING sentinel + row-1 dispatch + on-disk baseline + tfep-incident-report side-effect. |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | Donor | Stubified at Step 5 (CR-DEP-01); hard-deleted at Step 6 (CR-DEP-03). |
| `src/superclaude/commands/task.md` | Recipient command | `name:` flips role per CR-DEP-01 (research 01 Gaps #7); `src/superclaude/commands/task.md:100` `Skill sc:task-protocol` line flips to invoke the post-merge `task` skill. Classification header schema at `:50-67` and tier rules at `:69-91` are preserved verbatim. |
| `src/superclaude/cli/sprint/process.py` | Sprint CLI runtime | `:170` `/sc:task` emission flips to `/task` per Step-5. Test pin at `tests/sprint/test_process.py:80-89` must be updated in same commit. |
| `src/superclaude/cli/cleanup_audit/prompts.py` | Cleanup-audit CLI runtime | **Fresh discovery (research 04 §2.5, §8)**: 5 `/sc:task` emissions at `:26, 47, 69, 92, 116` `[CODE-VERIFIED]`. CR-DEP-01 scope MUST include this file. R-DIV-02 risk applies. |

---

---

## 25. API Contract Examples

Per S25 template (`src/superclaude/examples/prd_template.md:1131-1169`), this PRD has no HTTP API. The contracts that bind the merge are **(a) audit-grep command lines**, **(b) the `tfep-incident-report.md` 7-field markdown schema**, and **(c) the `research/test-baseline.yaml` schema**. Each is treated below as a contract example with request / success / failure framings.

### 25.1 CR-FM-NN audit grep commands

These are the structural enforcement commands the post-merge audit row catalog (CR-FM-01..CR-FM-04 and friends) executes. Each is bound to a specific AC-SM-NN success-measure row in `validation-spec.md` § 11.

#### 25.1.1 CR-FM-04 — row-1 ordering grep (CR-7 ORDERING sentinel + three call-sites)

**Command:**

```bash
# Bound to AC-SM-07 (validation-spec.md:359) and AC-SM-08 (validation-spec.md:360).
# Verifies three call-site names appear in canonical order in the recipient SKILL.md.

grep -nE 'path_override_check\(\)|tier_field_validate\(\)|gate_1_dispatch\(\)' \
  src/superclaude/skills/task/SKILL.md
```

**Success (post-Step-1):**

```
NN:    path_override_check()         # row 1, immediately under CR-7 ORDERING sentinel
NN:    tier_field_validate()         # row 2
NN:    gate_1_dispatch()             # row 3
```

**Failure (wrong-order bait — `validation-spec.md:296` Scenario A):**

```
NN:    tier_field_validate()         # WRONG — would resolve a tier the path override should supersede
NN:    path_override_check()
NN:    gate_1_dispatch()
```

Disposition: REJECT push (AC-ATK-17 hook fires); CR-7 ORDERING sentinel grep also fails.

#### 25.1.2 CR-7 sentinel literal grep

**Command:**

```bash
grep -n '<!-- CR-7 ORDERING' src/superclaude/skills/task/SKILL.md
```

**Success:**

```
NN:<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->
```

**Failure:** empty → push rejected. (Mitigation for spec § 12 attack: a future SKILL.md auto-generator that strips the comment would also fail CR-FM-04 ordering grep because the comment anchors the line-range pin.)

#### 25.1.3 CR-DEP-05 / AC-ATK-17 server-side `/sc:task` re-grep (extended scope)

**Command (PRD-amended scope — research 04 §2.5 / §6.2):**

```bash
# Runs on push against the landing commit, not the working tree.
# MUST include cleanup_audit/ (fresh discovery; spec only named sprint/).
# MUST exclude /sc:tasklist substring false positives via word boundary.

git diff --name-only origin/master..HEAD -- 'src/superclaude/cli/**' | \
  xargs grep -nE '/sc:task\b' 2>/dev/null | \
  grep -v -- '/sc:tasklist'
```

**Success (post-Step-5):** empty.

**Failure (rebase-split bypass / H-2):**

```
src/superclaude/cli/sprint/process.py:170:        f"/sc:task Execute all tasks in @{phase_file} "
src/superclaude/cli/cleanup_audit/prompts.py:26:        f"/sc:task Perform a surface-level scan ..."
src/superclaude/cli/cleanup_audit/prompts.py:47:        f"/sc:task Perform deep structural analysis ..."
src/superclaude/cli/cleanup_audit/prompts.py:69:        f"/sc:task Detect duplication, sprawl ..."
src/superclaude/cli/cleanup_audit/prompts.py:92:        f"/sc:task Consolidate audit findings ..."
src/superclaude/cli/cleanup_audit/prompts.py:116:        f"/sc:task Validate audit findings ..."
```

Disposition: REJECT the push unless the same commit also deletes the donor `task.md` body AND the recipient `task/SKILL.md` contains the absorbed TU-1..TU-8 markers (research 04 §6.2 third clause).

#### 25.1.4 CR-DEP-06 / AC-ATK-18 residual-reference manifest grep

**Command:**

```bash
# Post-Step-6 one-shot. Emits structured manifest with per-bucket disposition.
# Scope buckets per research 04 §5.4:

grep -rln '/sc:task\b\|sc-task-protocol\|task-unified' \
  .dev/releases/backlog/ \
  docs/generated/ \
  .dev/tasks/to-do/ \
  | grep -v -- '/sc:tasklist'
```

**Success (manifest emitted, no surprises):** count matches expected bucket totals (`.dev/releases/backlog/` 61 occurrences / 20 files; `docs/generated/` 83 occurrences / 20 files = **144 baseline residual** outside CR-DEP-05 scope per research-notes DIVERGENCE_FLAGS; `.dev/tasks/to-do/` live canonical figure is **132 union files** at 2026-05-16 fix-cycle 2 — 130 at fix-cycle 1; population dynamic; synth-07 §13 Q#4's earlier 25-file figure was a narrower-scope research-time snapshot; cross-section consistent with synth-08 K-03 modulo recount). Live recount on 2026-05-16 shows drift (per synth-07 Q#4: 153 across 45 files); CR-DEP-06 manifest must reconcile baseline-vs-live delta at emission time.

**Failure:** any path inside `src/superclaude/cli/` returns matches — that bucket is CR-DEP-05 fix-forward scope, NOT manifest LEAVE-AS-IS. Manifest rejects with a `CR-DEP-05 leakage` error.

#### 25.1.5 AC-ATK-18 resume-time content grep (per-resume gate-1.5)

**Command (invoked at task resume on the task subtree + `related_docs:` paths — research 03 §3, §4):**

```bash
TASK_DIR=".dev/tasks/to-do/${TASK_ID}"
grep -REn '/sc:task\b|sc-task-protocol|task-unified' "${TASK_DIR}" \
  | grep -v -- '/sc:tasklist'

# Plus: traverse related_docs frontmatter array; emit gate-1.5 for ENOENT.
```

**Success:** empty AND every `related_docs:` path resolves.

**Failure (warn-and-continue, NOT HALT — preserves ME-3 / INV-01):**

```
gate-1.5: legacy-surface-reference detected file=research/03-worker-session-governance.md action=warn-and-continue surface=/sc:task
gate-1.5: deleted-related-doc detected path=src/superclaude/skills/sc-task-protocol/SKILL.md
```

One-shot acknowledgment gate: first resume only (research 03 §3).

### 25.2 `tfep-incident-report.md` — 7-field schema (TU-8 / AC-ATK-12 binding)

The donor literal at `src/superclaude/skills/sc-task-protocol/SKILL.md:225-233` `[CODE-VERIFIED]` lists seven bullet rows (file-header `# TFEP Incident Report` at line 225, then seven `- **Field**:` rows at lines 227-233). Validation-spec § 5.8 (line 162) names a "seven-field schema." AC-ATK-12 (`validation-spec.md:341`) requires the seven fields be **enumerated** to close the spec attack ("the seven field names are not enumerated; a resumed task that reads an older incident file with a different field count sees undefined behavior"). The interpretation gap is surfaced in research 01 Gaps #2 and is bound here.

**File location:** `${TASK_DIR}/tfep/tfep-incident-report.md` (sibling of `qa/`, parallel to the QA report convention at `src/superclaude/skills/task/SKILL.md:196, 205, 226, 239` `[CODE-VERIFIED]`). Committed to git per donor `src/superclaude/skills/sc-task-protocol/SKILL.md:236`. INV-04 binding: side-effect file survives session boundaries, no in-task heading inserted (heading would mutate task body and risk INV-04 per research 01 TU-8).

**Schema (seven fields, AC-ATK-12 enumerated):**

```markdown
# TFEP Incident Report

**Trigger:** <one-line description of which TFEP escalation trigger fired (e.g. "pre-existing test failure", "3+ new tests fail", "runtime exception in implementation code", or "escalation gradient threshold crossed")>

**Escalation count:** <integer 1..3 corresponding to the donor escalation ladder at src/superclaude/skills/sc-task-protocol/SKILL.md:238-244 — tier-light triage / tier-standard / FULL STOP>

**Failing tests:** <newline-delimited list of pytest nodeids (e.g. tests/sprint/test_process.py::test_prompt_prefix) that triggered the incident>

**Root cause:** <multi-line analysis from forensic invocation Step 3 (donor src/superclaude/skills/sc-task-protocol/SKILL.md:191-198) — must reference baseline-snapshot classification (pre-existing vs new) from research/test-baseline.yaml>

**Solution:** <description of remediation plan synthesized in Step 5 ("Failure Remediation Plan (Adjudicated)" heading per donor :207-212), inserted BEFORE test/verification tasks in the parent task's checklist>

**Outcome:** <one of `{success / escalated / failed}` — donor-verbatim enum from `src/superclaude/skills/sc-task-protocol/SKILL.md:232` `[CODE-VERIFIED 2026-05-16 fix-cycle 1]`; matches Step 4 (donor :200-205) status-branching outcome. The earlier synth-05 enum `{resolved, escalated-to-FULL-STOP, deferred-with-decision-record}` was a fix-cycle 1 finding — drift from donor literal — and has been corrected to the verbatim donor form. Operator-facing UI MAY render the donor enum with longer-form glosses (e.g., `success` → "resolved", `escalated` → "escalated to FULL STOP", `failed` → "failed / deferred-with-decision-record") but the persisted enum value MUST be the donor literal.>

**Forensic artifacts:** <newline-delimited list of paths to forensic output files; MUST include at least the forensic invocation's structured-output file and any test-rerun logs>
```

**Field count:** seven, matching `validation-spec.md:162` and closing AC-ATK-12.

**Schema-violation handling at resume:** Per research 01 TU-8 paired AC-ATK-12 and research 03 §3 INV-04 layer split — a resumed task that reads an older incident file (e.g. pre-AC-ATK-12 six-field shape) MUST emit `gate-1.5: tfep-incident-schema-drift detected file=<path> expected_fields=7 found_fields=<n> action=warn-and-continue` rather than HALT (preserves ME-3 / INV-01).

### 25.3 `research/test-baseline.yaml` — baseline schema (TU-5 on-disk adaptation)

**File location:** `${TASK_DIR}/research/test-baseline.yaml` (per `src/superclaude/skills/task/SKILL.md:205, 274` `research/` directory convention `[CODE-VERIFIED]`).

**Capture command (donor `src/superclaude/skills/sc-task-protocol/SKILL.md:146` `[CODE-VERIFIED]`):**

```bash
uv run pytest --collect-only -q  > research/test-baseline.raw.txt
# Then parse to YAML below.
```

**Schema:**

```yaml
# research/test-baseline.yaml
# TFEP baseline snapshot (TU-5). Written PRE-F1 per validation-spec § 2 line 53.
# INV-04 binding: persistence across session boundaries.

schema_version: 1                          # increment on field shape change
captured_at: "2026-05-16T00:00:00Z"        # ISO 8601 UTC
captured_by_sha: "<40-char git SHA>"       # repo HEAD at capture
captured_by_command: "uv run pytest --collect-only -q"

baseline:
  test_files:                              # list of paths relative to repo root
    - tests/sprint/test_process.py
    - tests/cleanup_audit/test_prompts.py  # planned, research 04 Q-4
    - tests/pm_agent/test_confidence.py
  test_nodeids:                            # full pytest nodeids
    - tests/sprint/test_process.py::test_prompt_prefix
    - tests/sprint/test_process.py::test_emission_target

# Classification predicate (donor src/superclaude/skills/sc-task-protocol/SKILL.md:148-152):
#   - A failing test whose nodeid appears in `baseline.test_nodeids` is PRE-EXISTING
#     → MUST-escalate via TFEP.
#   - A failing test whose nodeid is NOT in `baseline.test_nodeids` is NEW
#     → MAY-fix-directly within the carve-out catalog (donor :137-140).

# F-04 closure / AC-ATK-03 four-state observation order (validation-spec.md:332):
#   absent      → classification=new (over-escalate; see § 12 fourth bullet residual)
#   empty       → classification=new (size == 0 by os.path.getsize)
#   parse-fail  → classification=new (yaml.safe_load raises YAMLError)
#   schema-fail → classification=new (yaml parses but `baseline` key missing or wrong type)
# Observer order is pinned: getsize → safe_load → schema-shape — to prevent the
# `null\n` ambiguity called out in validation-spec.md:300 Scenario C.
```

**Resume-time read contract:** every F1 entry re-reads `research/test-baseline.yaml`; never trusts in-process memo. This is the load-bearing TU-5 adaptation — donor in-memory storage breaks INV-04, on-disk YAML preserves it.

---

---

## 26. Contributors & Collaboration

> Per FEATURE-PRD discipline, contributor names are TBD. The roles below name the responsibility, not specific individuals.

### 26.1 Contributors

| Role | Name | Responsibility | Contact |
|------|------|----------------|---------|
| Product Owner | TBD | Owns this PRD, scope decisions, stakeholder alignment | TBD |
| Engineering Lead | TBD | Owns implementation across the 10-step commit sequence + Phase 7.5 patch sprint | TBD |
| QA / rf-qa Lead | TBD | Owns rf-qa identity and floor (INV-03); confirms ME-2 across three invocation points | TBD |
| Documentation / Release Owner | TBD | Owns content audit of cited anchor artifacts (R-DOC-01 reframed — artifacts present on disk; cross-check owed) and release-notes authoring | TBD |
| Framework Maintainer | TBD | Owns `src/superclaude/` source-of-truth and `make sync-dev` / `make verify-sync` discipline | TBD |
| Sprint / Cleanup-Audit CLI Owner | TBD | Owns sprint executor and cleanup-audit CLI emitter re-routing (CR-DEP-04, AC-ATK-17) | TBD |

### 26.2 Review & Approval Process

- **Reviewers (open Open Questions):** Engineering Lead (Open Questions Q-1..Q-5 in S13).
- **Approvers:** Product Owner, Engineering Lead, Executive Sponsor (see Document Approval table at top).
- **Cadence:** TBD; recommended review at each merge step (Steps 1, 4, 5, 6) and at Phase 7.5 convergence.

### 26.3 Collaboration Conventions

- All edits land in `src/superclaude/` (source of truth); `make sync-dev` cascades to `.claude/`.
- All `[CODE-VERIFIED]` tags MUST carry a `(git-sha: <40-char>)` suffix per AC-ATK-08 amendment (research-04 § 6.1).
- Open Questions in S13 are resolved by Engineering Lead before the dependent merge step (e.g., OQ-TIER-VOCABULARY before Step 1; OQ-FM-03-SUNSET before Step 7; OQ-F-NN-BIJECTION before Step 7 invariant-survival walkthrough).

---

## 27. Related Resources

### 27.1 Primary Source Documents

- **Validation Spec.** `.dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md` — V1 steelman + V2 attack chain + V3 security-probe converged (sections 1–15).
- **PRD Template.** `src/superclaude/examples/prd_template.md` — template followed by this PRD (Heavyweight tier, Feature-PRD abbreviated).
- **Recipient Skill.** `src/superclaude/skills/task/SKILL.md` — canonical post-merge surface; F1 loop at `:79-98`; F2 prohibitions at `:104-117`; Phase-Gate rf-qa at `:191-198`; Post-Completion rf-qa at `:219-241`.
- **Donor Skill.** `src/superclaude/skills/sc-task-protocol/SKILL.md` — to be stubified (Step 5) and hard-deleted (Step 6); TFEP block at `:125-244`.
- **Donor Command File.** `src/superclaude/commands/task.md` — classification header at `:50-67`; tier rules at `:69-91`.

### 27.2 Research Inputs

- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/01-transfer-units-catalog.md` (TU-1..TU-8)
- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/02-manifest-exceptions-and-invariants.md` (ME-1..ME-9, INV-01..INV-05)
- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/03-in-flight-exposure-and-resumability.md` (live in-flight grounding, R-DIV-01)
- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/04-sequencing-and-timeline-hazards.md` (S-1..S-3, HZ-NN)
- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/05-acceptance-criteria-and-audit-rows.md` (AC-ATK-01..18, AC-SM-01..12)
- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/06-failure-mode-coverage-and-tradeoffs.md` (FM-01..08, EC-01..04, tradeoffs)
- Web research files (2 files) for adversarial-validation pattern references.

### 27.3 Project Context

- `CLAUDE.md` — UV-only Python operations; component sync discipline; `src/superclaude/` source-of-truth.
- `Makefile` — sync-dev, verify-sync, test, lint targets.

### 27.4 External References

- N/A — this is an internal framework merge; no external dependencies beyond `git`, `uv`, and the Python toolchain pinned in `pyproject.toml`.

---

## 28. Maintenance & Ownership

### 28.1 Document Ownership

- **Owner:** TBD (Product Owner).
- **Backup Owner:** TBD (Engineering Lead).
- **Update Cadence:** Per merge step convergence; major revisions at Step 5 (CR-DEP-01 stubification) and Step 6 (CR-DEP-03 hard-delete).
- **Living Document Status:** This PRD evolves as merge implementation and post-merge audits surface new findings.

### 28.2 Living Document Process

- All updates land in `src/superclaude/...` or in this PRD file directly; updates to `[CODE-VERIFIED]` tags require a fresh git-SHA suffix per AC-ATK-08 amendment.
- Open Questions in S13 are resolved by Engineering Lead and the resolution is recorded in Document History (S28.4).
- Acceptance criteria flagged `[VALIDATION-SPEC-CITED][UNVERIFIED][CONTENT-AUDIT-OWED]` are revisited at every artifact-recovery event (R-DOC-01).

### 28.3 Long-term Maintenance

- **Post-merge (Steps 7-10):** `make verify-sync` runs on every commit; CR-DEP-06 residual-reference manifest is regenerated weekly; CR-FM-03 shim sunset audit row (`CR-AUDIT-FM-03-SUNSET`) emits on every resumed task.
- **Sunset binding:** CR-FM-03 sunsets at `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 row authored` (recommended; subject to OQ-FM-03-SUNSET confirmation).
- **AC-SM content-audit resolution (reframed at fix-cycle 2):** AC-SM-01, -03, -05, -06, -11 remain `[VALIDATION-SPEC-CITED][CONTENT-AUDIT-OWED]` until the named anchor artifacts (`transfer-manifest.md`, `extension-point-contracts.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `rejected-features-ledger.md`, `final-merge-plan.md`) — all confirmed PRESENT on disk at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` per fix-cycle 2 verification — are content-audited against the PRD claims, with any drift surfaced as per-row R-DRIFT-NN findings.

### 28.4 Document History

> See **Document History** section below for the chronological change log.

---

## Appendices

### Appendix A — Glossary

| Term | Definition |
|------|------------|
| **TU** | Transfer Unit. A named donor-pattern absorbed into the recipient skill under a V/C/K (Verbatim / Calibrated / Killed) verdict. 8 TUs total (TU-1..TU-8). |
| **ME** | Manifest Exception. An audit gate that binds a specific invariant or pattern from being silently dropped or modified. 9 MEs total; 5 load-bearing, 4 ancillary. |
| **INV** | Load-bearing Invariant. A semantic guarantee the recipient skill MUST preserve verbatim across the merge. 5 INVs total (INV-01..INV-05). |
| **S-N** | Sequencing Constraint. A timeline-layer constraint binding the merge ordering or atomicity. 3 S-Ns total (S-1, S-2, S-3). |
| **H-N** | Compatibility Hazard. A named scenario from `compat-hazard-report.md` that the merge must address (H-1..H-4, HZ-NN row family). |
| **FM** | Failure Mode. A spec § 13 failure-mode coverage row (FM-01..FM-08). |
| **EC** | Evidence-Completeness audit gap (EC-01..EC-04 per spec § 14). |
| **AC-ATK** | Adversarial-validation Acceptance Criterion. Closure obligations from V2 attack chain + V3 security-probe; 18 rows (AC-ATK-01..18). |
| **AC-SM** | Success-Metric Acceptance Criterion. Verification rows for invariants and audit chains; 12 rows (AC-SM-01..12). |
| **CR-DEP-N** | Deprecation Audit Row. Audit rows enforcing donor-surface deprecation (CR-DEP-01 stubify; CR-DEP-03 hard-delete; CR-DEP-04 sync; CR-DEP-05 caller re-routing; CR-DEP-06 residual-reference manifest). |
| **CR-FM-N** | Frontmatter / Format-Migration Audit Row. CR-FM-01 (Tier canonicalization); CR-FM-03 (default-to-STANDARD shim); CR-FM-04 (row-1 ordering grep). |
| **CR-7 ORDERING sentinel** | Markdown comment immediately above row 1 in `task/SKILL.md`. Canonical form: `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->` |
| **TFEP** | Test Failure Escalation Protocol. Donor §4.5 block (`sc-task-protocol/SKILL.md:125-244`) absorbed as TU-5..TU-8. |
| **MDTM** | Markdown-Driven Task Management. Task file format with YAML frontmatter + Markdown checklist body. |
| **F1 loop** | The canonical execution loop in `task/SKILL.md:79-98`: READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. |
| **F2 catalog** | Prohibited Actions catalog in `task/SKILL.md:104-117`. Additive-only per INV-02. |
| **rf-qa** | The verification agent identity that anchors INV-03 floor. Spawned at three invocation points post-merge. |
| **STRICT / STANDARD / LIGHT / EXEMPT** | Canonical tier vocabulary per `commands/task.md:55, 61, 82` `[CODE-VERIFIED]`. `TRIVIAL` from validation-spec § 4 line 103 is vestigial. |

### Appendix B — Acronyms

| Acronym | Expansion |
|---------|-----------|
| PRD | Product Requirements Document |
| TDD | Technical Design Document |
| QA | Quality Assurance |
| CR | Change Row (audit row) |
| CR-DEP | Deprecation audit row |
| CR-FM | Frontmatter / Format-Migration audit row |
| CR-TASK | Task-class audit row |
| CR-REF | Reference-class audit row |
| CR-DOC | Documentation audit row |
| CR-DIST | Distribution audit row |
| F-NN | Finding (V/C/K verdict from validation-spec § 2) |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| INV | Invariant |
| ME | Manifest Exception |
| TU | Transfer Unit |
| YAML | YAML Ain't Markup Language |
| UV | UV Python package manager (Astral) |
| CI | Continuous Integration |
| SHA | Git commit SHA-1 hash |

### Appendix C — Document Provenance

This PRD was synthesized from the following inputs (read in this order):

**Validation Spec:**
- `.dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md` (sections 1–15)

**Research Notes:**
- `.dev/tasks/to-do/TASK-PRD-20260516-004625/research-notes.md` (preliminary findings; superseded by per-topic research files)

**Research Files (6 files):**
- `01-transfer-units-catalog.md` (TU-1..TU-8 V/C/K verdicts)
- `02-manifest-exceptions-and-invariants.md` (ME-1..ME-9, INV-01..INV-05)
- `03-in-flight-exposure-and-resumability.md` (live in-flight grounding, INV-04 layers)
- `04-sequencing-and-timeline-hazards.md` (S-1..S-3, HZ-NN, CLI scope amendments)
- `05-acceptance-criteria-and-audit-rows.md` (AC-ATK-01..18, AC-SM-01..12)
- `06-failure-mode-coverage-and-tradeoffs.md` (FM-01..08, EC-01..04, tradeoffs)

**Web Research Files (2 files):**
- Adversarial-validation pattern references (web research files for V2/V3 framing)
- Industry references for atomicity, server-side hooks, and `flock` discipline

**Synthesis Files (8 files — assembled into this PRD):**
- `synth-01-overview-goals-non-goals.md` (S1, S2, S3, S4, S6, S10, S11, S12)
- `synth-02-personas-and-stories.md` (S7, S21.1)
- `synth-03-functional-requirements.md` (S14 FR portion: FR-TU-1..8, FR-CS-1..10, FR-CR-DEP-06)
- `synth-04-non-functional-requirements.md` (S14 NFR portion: NFR-INV-1..5, NFR-ME-1..9, NFR-S-1..3)
- `synth-05-architecture-and-impact.md` (S15, S24, S25)
- `synth-06-ux-and-impacted-flows.md` (S16.2, S22, S23)
- `synth-07-risks-and-mitigations.md` (S13, S20)
- `synth-08-acceptance-criteria-kpis-cost.md` (S5, S17, S18, S19, S21)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-16 | rf-assembler (synthesis from 8 component files) | Initial draft. Assembled from 8 synthesis files covering S1-S28 plus appendices. Heavyweight tier, Feature-PRD abbreviated (S5/S8/S17/S18 reference Platform PRD; S9 marked N/A; S16 only S16.2 populated). AC-SM-01, -03, -05, -06, -11 carry `[VALIDATION-SPEC-CITED][UNVERIFIED][CONTENT-AUDIT-OWED]` flags per R-DOC-01. Tier vocabulary canonical = `{STRICT, STANDARD, LIGHT, EXEMPT}` with reconciliation surfaced as Open Question in S13. S-1 framing: supplement-not-replace — binds both the live named targets (`TASK-PRD-20260514-121039`, `TASK-TDD-20260514-121250`, both verified present 2026-05-16) AND the broader live in-flight population (132 union files referencing donor surfaces across `.dev/tasks/`). `TASK-RF-20260515-195758` is genuinely absent. CR-DEP-06 ELEVATED to required (FR-CR-DEP-06 in S14). `cleanup_audit/prompts.py` lines 26, 47, 69, 92, 116 included in S15 impacted surfaces and AC-ATK-17 scope. TFEP Outcome enum donor literal: `{success / escalated / failed}`. CR-7 ORDERING sentinel canonical form: HTML comment `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->`. |
| 1.1 | 2026-05-16 | TBD (QA fix-cycle sweep) | QA report-validation fix-cycles 1+2: R-DOC-01 reclassified (artifacts present, content audit owed); AC-SM cascade tags downgraded from `[ARTIFACT-ABSENT]` to `[CONTENT-AUDIT-OWED]`; live count updated 130 → 132; residual stale "25 live" sites reframed as research-time snapshots. |

---

**END OF DOCUMENT**
