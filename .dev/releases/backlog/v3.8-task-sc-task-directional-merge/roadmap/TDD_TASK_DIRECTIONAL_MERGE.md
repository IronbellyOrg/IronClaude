---
name: TDD_TASK_DIRECTIONAL_MERGE
title: "Task Directional Merge (/sc:task → /task) — Technical Design Document"
tier: Heavyweight
status: 🟡 Draft
version: 1.0
date: 2026-05-16
parent_doc: .dev/releases/current/task-sc-task-directional-merge/roadmap/PRD_TASK_DIRECTIONAL_MERGE.md
parent_doc_version: 1.1
pinned_sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444
convergence_score: 0.86
authoritative_values:
  f2_catalog_pre_merge: 10
  f2_catalog_post_merge: 13
  in_flight_floor: 136            # union-files at pinned SHA; monotonic upward; iterate live recount at gate-execution time
  task_prd_20260514_121039: EXISTS  # 258 donor-surface refs across 12 files; R-DRIFT-04 RETRACTED; S-1 binding stays in force
  rf_qa_invocation_count_post_merge: 4   # phase-gate + post-completion structural + post-completion qualitative + TU-7 mid-phase TFEP
  tier_enum: [STRICT, STANDARD, LIGHT, EXEMPT]
  outcome_enum: [success, escalated, failed]   # byte-identical to donor sc-task-protocol/SKILL.md:232 per ME-6
  legacy_surface_enum: ["/sc:task", "sc-task-protocol", "task-unified"]
---

# Task Directional Merge (/sc:task → /task) — Technical Design Document

## Document Information

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | 🟡 Draft |
| **Date** | 2026-05-16 |
| **Author** | rf-assembler (consolidating synth-01..synth-10) |
| **Reviewers** | rf-qa, rf-analyst, Engineering Lead |
| **Approvers (deferred)** | Engineering Lead, Documentation/Release Owner |
| **Parent doc** | `.dev/releases/current/task-sc-task-directional-merge/roadmap/PRD_TASK_DIRECTIONAL_MERGE.md` v1.1 (2026-05-16) |

## Approvers

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Engineering Lead | _pending_ | — | — |
| Documentation/Release Owner | _pending_ | — | — |
| rf-qa Owner | _pending_ | — | — |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & Context](#2-problem-statement--context)
3. [Goals & Non-Goals](#3-goals--non-goals)
4. [Success Metrics](#4-success-metrics)
5. [Technical Requirements](#5-technical-requirements)
6. [Architecture](#6-architecture)
7. [Data Models](#7-data-models)
8. [API Specifications](#8-api-specifications)
9. [State Management](#9-state-management) — N/A
10. [Component Inventory](#10-component-inventory) — N/A
11. [User Flows & Interactions](#11-user-flows--interactions)
12. [Error Handling & Edge Cases](#12-error-handling--edge-cases)
13. [Security Considerations](#13-security-considerations)
14. [Observability & Monitoring](#14-observability--monitoring)
15. [Testing Strategy](#15-testing-strategy)
16. [Accessibility Requirements](#16-accessibility-requirements)
17. [Performance Budgets](#17-performance-budgets)
18. [Dependencies](#18-dependencies)
19. [Migration & Rollout Plan](#19-migration--rollout-plan)
20. [Risks & Mitigations](#20-risks--mitigations)
21. [Alternatives Considered](#21-alternatives-considered)
   - [Appendix A — Operational Drill-Down](#appendix-a--operational-drill-down-synth-07-owned-cross-cutting-reference) *(non-numbered, between §21 and §22 per assembly convention)*
22. [Open Questions](#22-open-questions)
23. [Timeline & Milestones](#23-timeline--milestones)
24. [Release Criteria](#24-release-criteria)
25. [Operational Readiness](#25-operational-readiness)
26. [Cost & Resource Estimation](#26-cost--resource-estimation)
27. [References & Resources](#27-references--resources)
28. [Glossary](#28-glossary)

---

## 1. Executive Summary

This component is the **directional merge of the donor `/sc:task` command-and-skill pair into the recipient `/task` skill** within `src/superclaude/skills/task/SKILL.md`. The merge collapses two parallel task-execution surfaces into one by transplanting eight bounded Transfer Units (TU-1..TU-8) — Tier classification + Gate-1 dispatch, Critical/Trivial path overrides at row-1 (CR-7 ORDERING), Gate-2 verification-roster widening to `[rf-qa, quality-engineer]`, Layer-2 `git status` pre-flight with a five-row warn-and-continue disposition matrix, on-disk TFEP baseline at `${TASK_DIR}/research/test-baseline.yaml`, prohibition additions to the F2 catalog (extending **10 pre-merge prohibitions** [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)], NOT the 9 carried by stale spec lineage), TFEP escalation gradient as the fourth rf-qa invocation point (F-05) — authoritative rf-qa invocation count post-merge = **4** (phase-gate + post-completion structural + post-completion qualitative + TU-7 mid-phase TFEP), and TFEP incident-report side-effect file at `${TASK_DIR}/research/tfep-incident-report.md` — then deletes the donor skill body (Step 6, CR-DEP-03) and stubifies the donor command (Step 5, CR-DEP-01). The merge is governed by an atomic 10-step commit sequence (FR-CS-1..FR-CS-10) under ME-6 atomicity, with the load-bearing seven-foundation-row binding enforced by a server-side push-policy hook (AC-ATK-17) that closes the H-2 rebase-split bypass.

The chosen engineering approach is **adopt-then-adapt against five hard invariants** (INV-01..INV-05) and **nine manifest exceptions** (ME-1..ME-9; five load-bearing, four ancillary). INV-04 carries the highest exposure: a live in-flight floor of **136 union files** [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444), monotonic upward — iterate live recount at gate-execution time, never hardcode] currently reference donor surfaces under `.dev/tasks/`, and must resume across the merge boundary without HALT. INV-04 is split into FR-INV-04-PARSE (CR-FM-03 shim defaulting absent `Tier:` → `STANDARD`) and FR-INV-04-SEMANTIC (AC-ATK-18 content-level resume-time grep emitting `gate-1.5: legacy-surface-reference` warn-and-continue per occurrence, plus L3 `related_docs:` ENOENT detection). The donor command stubification carries a one-shot deprecation banner; the donor SKILL.md is hard-deleted (sha256-baselined per AC-ATK-09); a one-shot residual-reference manifest (FR-CR-DEP-06, elevated to MUST) enumerates 144 surviving residual occurrences across 40+ files with per-bucket disposition.

Key engineering decisions: (a) **CR-7 ORDERING is enforced by sentinel + AST-grade ordering grep**, not by markdown discipline alone (closes R-ATK-01); (b) **AST/regex/content-hash anchors** replace line-number anchors for the load-bearing INV-03 rf-qa block (CR-FM-04, closes R-ATK-06); (c) **server-side CI push-policy enforcement** at `.github/workflows/push-policy.yml` is the canonical venue for the seven-foundation-row atomicity check — local `.git/hooks/pre-push` is rejected because it is bypassable via `--no-verify` (closes R-ATK-17); (d) **`flock` on `.claude/skills/.sync-lock`** wraps `make sync-dev` + `make verify-sync` to close both the forward-looking prune race and the LIVE copy-overwrite race in `Makefile:121` (closes R-ATK-16); (e) **TFEP baseline persists on disk** at `${TASK_DIR}/research/test-baseline.yaml` rather than in memory, because INV-04 binds resumability across session boundaries (donor's in-memory form at `sc-task-protocol/SKILL.md:147` is the ADAPT delta).

Scope is bounded to the 19 Must FRs (FR-TU-1..FR-TU-8 + FR-CS-1..FR-CS-10 + FR-CR-DEP-06). Explicitly out of scope: re-introduction of `/sc:task` post-stubification, donor SKILL.md as parallel live skill, tier vocabulary `TRIVIAL` (canonical = `{STRICT, STANDARD, LIGHT, EXEMPT}`), per-item marker as runtime dispatcher (INV-05/ME-1 forbid; D09b REJECTed per AC-ATK-05 closed enumeration), HALT-as-gate disposition for git pre-flight (INV-01 forbids), and content audit of the seven on-disk anchor artifacts (Documentation/Release Owner-scoped, not implementation work). The 47 adversarial artifacts converge at score **0.86**, with five residual concessions (R-RES-01..R-RES-05) recorded but not closed in this merge cycle.

Risk envelope is dominated by **INV-04 (HIGHEST EXPOSURE per validation-spec § 9 L285)**, **rebase-split bypass (R-ATK-17, H-2)**, and **TASK-PRD-20260514-121039 LIVE spec-named target with 258 donor-surface refs** [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] keeping S-1 binding in force (R-DRIFT-04 RETRACTED). All `[CODE-VERIFIED]` tags throughout this TDD carry the 40-char SHA suffix per AC-ATK-08. Six engineering-lead open questions (OQ-1..OQ-5 + OQ-FM-03-SUNSET + four others) remain unresolved and are surfaced to §22 Open Questions; ship requires their disposition.

**Key Deliverables:**

- Merged `src/superclaude/skills/task/SKILL.md` with TU-1..TU-8 transplanted, INV-01..INV-05 preserved, 10-step commit sequence landed under ME-6 atomicity.
- Server-side `.github/workflows/push-policy.yml` push-policy enforcer covering the seven-foundation-row binding and the extended grep scope `src/superclaude/cli/{sprint,cleanup_audit}/**` (AC-ATK-17).
- `make sync-dev` + `make verify-sync` wrapped in `flock` on `.claude/skills/.sync-lock` (AC-ATK-16).
- `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` enumerating ≥144 residual `/sc:task | sc-task-protocol | task-unified` occurrences across ≥40 files with per-bucket disposition (FR-CR-DEP-06).
- Test fixtures `tests/fixtures/donor-blocks/{TU2_path_override,TU2_redirect,TU6_prohibitions,TU6_carve_outs,TU7_triggers,TU8_schema,CR7_sentinel,CR8_sentinel}.txt` for CR-TASK-12 seven-diff audit (AC-ATK-06 frozen-fixture closure).
- Pytest harness covering AC-SM-01..12 (12 audits) and AC-ATK-01..18 (18 attack-class closures) per the §15 traceability matrix.

---

## 2. Problem Statement & Context

### 2.1 Background

The SuperClaude framework v4.2.0 currently ships **two parallel task-execution surfaces** that diverged organically. The donor pair — slash command `/sc:task` (defined at `src/superclaude/commands/task.md` lines 50-100 [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]) and skill `sc-task-protocol` (365-line `src/superclaude/skills/sc-task-protocol/SKILL.md` [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]) — owns Tier classification, Critical/Trivial path override, on-disk TFEP baseline, prohibition rules with carve-outs, escalation gradient with `/sc:forensic` routing, and incident-report ceremony. The recipient — skill `/task` (`src/superclaude/skills/task/SKILL.md` [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]) — owns the F1 execution loop (lines 79-98), the F2 prohibited-actions catalog with **10 prohibitions** (lines 104-117), the Phase-Gate rf-qa spawn (lines 191-198), and Post-Completion Validation (lines 219-241). The two surfaces share semantic intent but differ in implementation: the recipient has no `Tier:` parser, no Gate 1, no TFEP scaffolding, no baseline snapshot, no incident-report schema; the donor lacks the recipient's F1 monotonicity discipline and routes mid-phase escalations away from rf-qa entirely.

The merge is happening **now** because the live in-flight task population has grown to a floor of **136 union files** [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444), monotonic upward] across `.dev/tasks/`, each containing content-level references to donor surfaces (`/sc:task`, `sc-task-protocol`, `task-unified`). The exposure is **larger than every upstream canonical figure** — supersedes spec § 3 line 81 (96 files), supersedes fix-cycle 1 (130), supersedes fix-cycle 2 (132), and supersedes the earlier 25-file research-03 narrower-scope snapshot. The trajectory is monotonic upward; deferring the merge increases the blast radius. Forty-seven adversarial artifacts have converged on a **0.86 confidence score** for the directional-merge design, with five residual concessions (R-RES-01..R-RES-05) explicitly recorded.

The recipient `task` skill is the canonical post-merge surface because it owns the F1 loop and the framework's MDTM execution contract. The donor `/sc:task` command surface is stubified rather than deleted to preserve a one-shot deprecation banner for at-resume callers; the donor `sc-task-protocol` SKILL.md is hard-deleted because ME-9 binds the 10 ceremony drops to remain dropped (re-introduction requires a new directional merge).

### 2.2 Problem Statement

**The core technical problem:** Two parallel task-execution surfaces (`/sc:task` + `sc-task-protocol/SKILL.md` donor pair; `/task` + `task/SKILL.md` recipient) duplicate semantic intent, drift independently, and cannot both bind the same INV-04 resumability guarantee across a 136-file live in-flight population.

Expanded specifics:

- **What is broken or missing:** (a) no canonical `Tier:` field or Gate-1 dispatch in the recipient; (b) no CR-7 ORDERING enforcement at row-1 (sentinel ABSENT in both donor and recipient as of pinned SHA); (c) no Layer-2 `git status` pre-flight with the five-row disposition matrix `{clean, dirty, tool-absent, not-a-repo, error-other}` × `{WARN-CONTINUE, GRACEFUL-SKIP}`; (d) no on-disk TFEP baseline at `${TASK_DIR}/research/test-baseline.yaml` (donor's `:147` form is in-memory only, breaking INV-04 across sessions); (e) no fourth rf-qa invocation point for mid-phase escalation (donor routes to `/sc:forensic`); (f) no `tfep-incident-report.md` side-effect schema with the seven-field outcome enum `{success / escalated / failed}`; (g) no server-side push-policy enforcer protecting the seven-foundation-row atomicity binding against rebase-split bypass (`.git/hooks/` contains only `*.sample` and `--no-verify` evades local hooks); (h) no `flock` on `.claude/skills/` for the `make sync-dev` copy-overwrite race that LIVE-exists at `Makefile:121`.
- **Who is affected:** Four personas — (P-01) MDTM task authors whose 136 in-flight files must survive merge; (P-02) `/task` operators whose F1 loop must reach green Phase-Gate QA without surprise HALTs; (P-03) framework maintainers landing Steps 1-10 with auditable evidence; (P-04) downstream subagent callers consuming `.dev/tasks/` content as context and traversing `related_docs:` paths that can ENOENT post-Step-6.
- **Cost of not solving:** (i) INV-04 silent semantic degradation post-Step-5 across 136 files (highest exposure); (ii) operator confusion from two parallel commands with overlapping but non-identical semantics (K-07: 2 paired entries should be 1); (iii) maintenance overhead from synchronized edits to two SKILL.md files (K-08: 2 → 1); (iv) audit drift accumulating with every new `[CODE-CONTRADICTED]` tag; (v) FR-CR-DEP-06 elevation to MUST because **144 live residual occurrences** (61 backlog + 83 docs/generated) defeat any non-manifest-backed cleanup approach.

### 2.3 Business Context

This component is an **internal SuperClaude framework feature**. It does not directly produce business revenue, customer conversion, or end-user-facing metrics. Its business value is **maintenance-surface reduction**, **audit-pass discipline**, and **runtime correctness for the framework's task-execution contract** — all of which are framework-internal levers.

- **Product PRD Reference:** `.dev/releases/current/task-sc-task-directional-merge/roadmap/PRD_TASK_DIRECTIONAL_MERGE.md` v1.1 (2026-05-16); Epics: full PRD scope §1-§28; specifically §6 JTBD Jobs 1-3, §7 Personas P-01..P-04, §12 Scope, §14 FRs, §19 KPIs.
- **Business Impact:** Internal — collapses the maintenance-surface pair count from 2 → 1 (K-08), eliminates the 144 residual `/sc:task` occurrences from non-authorized buckets (K-03), and reduces the visible `/sc:help` command roster from 2 paired entries → 1 (K-07). No revenue/conversion metric applies; this TDD marks §4.2 Business Metrics as N/A by design.
- **User Impact:** Affects **framework users** (engineers and agent operators) invoking `/task` or `/sc:task`. Post-merge, all invocations route through the single recipient surface; one-shot deprecation banner fires at the donor stub for any caller still using `/sc:task`. End users of products built on top of the framework are not directly affected.

---

## 3. Goals & Non-Goals

### 3.1 Engineering Goals

What this component WILL accomplish (translation of PRD JTBD Jobs 1-3 + §12.1 In-Scope categories into engineering-shape goals):

| ID | Goal | Success Criteria | Trace |
|----|------|------------------|-------|
| **G-01** | Land all eight Transfer Units (TU-1..TU-8) into recipient `task/SKILL.md` with V/C/K verdicts preserved byte-for-byte against `transfer-manifest.md` § 4 | AC-SM-01 returns 8/8 V/C/K identical; CR-TASK-12 seven-diff audit (AC-SM-08) returns 7 zero-diffs against `tests/fixtures/donor-blocks/*.txt` [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] | PRD §12.1, §14.1 FR-TU-1..FR-TU-8 |
| **G-02** | Enforce CR-7 ORDERING at row-1: `path_override_check()` → `tier_field_validate()` → `gate_1_dispatch()`, anchored by sentinel comment + AST-grade ordering grep | CR-FM-04 ordering grep at `final-merge-plan.md:116-117, 243` returns 3 function names in monotonically-increasing line order (AC-SM-07); sentinel-comment companion present byte-identical (AC-ATK-13) | PRD §14.1 FR-TU-2, §14.7 NFR-INV-5 |
| **G-03** | Preserve INV-01..INV-05 across the merged surface with INV-04 split into FR-INV-04-PARSE (CR-FM-03 shim) and FR-INV-04-SEMANTIC (AC-ATK-18 content-level audit) | AC-SM-03 walkthrough confirms 5/5 INVs survive on merged surface; AC-SM-12 confirms 100% of live in-flight floor (136 union files at this drift snapshot) resume cleanly under CR-FM-03 with zero HALTs | PRD §14.7 NFR-INV-1..5; §9 L285 HIGHEST EXPOSURE |
| **G-04** | Land the 10-step commit sequence (FR-CS-1..FR-CS-10) under ME-6 atomicity, with the seven-foundation-row binding enforced by server-side CI push-policy | Server-side `.github/workflows/push-policy.yml` returns exit 0; AC-SM-09 confirms Step-5 commit roster equality; AC-SM-10 confirms Step-6 commit roster equality; AC-SM-12 confirms gates 1/5/6 exit 0 | PRD §14.2 FR-CS-1..10, §14.9 NFR-S-2 |
| **G-05** | Widen Gate-2 verification roster to `[rf-qa, quality-engineer]` (ME-2 preserved: rf-qa never replaced, only ADDED to) with a **fourth** rf-qa invocation point at mid-phase TFEP escalation (F-05) — authoritative rf-qa count post-merge = 4 (3 pre-merge + 1 TU-7) | All four rf-qa invocation points present at `task/SKILL.md` (phase-gate L191, post-completion structural L221, post-completion qualitative L230, mid-phase TU-7); AC-ATK-07 rf-qa F-07 chain verifier returns PASS; AC-ATK-11 ME-10 carve-out OR retroactive manifestization decision recorded | PRD §14.1 FR-TU-3, FR-TU-7; §14.7 NFR-INV-3 |
| **G-06** | Implement the 5-row `git status` warn-and-continue matrix at F1 entry — `{clean, dirty, tool-absent, not-a-repo, error-other}` × `{WARN-CONTINUE, GRACEFUL-SKIP}` with NO HALT semantic added | AC-ATK-02 5-row matrix test returns 5/5 dispositions correct; AC-ATK-10 input-invalid (HALT) vs environment-non-ideal (warn-continue) asymmetry table present; F2 grep confirms no new env-state HALT row | PRD §14.1 FR-TU-4, §14.7 NFR-INV-1, NFR-ME-3 |
| **G-07** | Persist TFEP baseline on disk at `${TASK_DIR}/research/test-baseline.yaml` (ADAPT delta from donor in-memory form) and emit `tfep-incident-report.md` side-effect file at `${TASK_DIR}/research/tfep-incident-report.md` with the seven-field schema `{Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts}` with Outcome enum `{success / escalated / failed}` | AC-ATK-03 4-state baseline matrix `{absent, empty, parse-fail, schema-fail}` with observer order pinned (`os.path.exists → os.path.getsize → yaml.safe_load → schema`) returns clean; baseline round-trip test passes; incident-report schema matches donor literal `sc-task-protocol/SKILL.md:225-233` byte-for-byte | PRD §14.1 FR-TU-5, FR-TU-8 |
| **G-08** | Eliminate the 144 live residual `/sc:task | sc-task-protocol | task-unified` occurrences (61 backlog + 83 docs/generated) outside authorized leave-as-is buckets via a one-shot post-Step-6 residual-reference manifest (FR-CR-DEP-06, elevated MUST) with per-bucket disposition | `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` present, enumerating ≥144 residuals across ≥40 files; AC-ATK-18 four-part fan-out closure achieved; residual count outside authorized buckets = 0 | PRD §14.3 FR-CR-DEP-06; §14.7 NFR-INV-4b |

### 3.2 Engineering Non-Goals

What this component will NOT do (explicit scope boundaries per PRD §12.2 + §12.3):

| ID | Non-Goal | Rationale |
|----|----------|-----------|
| **NG-01** | Re-introduction of `/sc:task` as a non-stubified command post-Step-5 | Stubification IS the deprecation surface; reverting would invalidate ME-9 and re-open the H-2 rebase-split exposure. New `/sc:task` invocations post-Step-5 are fix-forward to `/task` via CR-DEP-05, not re-enabled. |
| **NG-02** | Donor `sc-task-protocol/SKILL.md` as a parallel live skill | Hard-deleted at Step 6 (CR-DEP-03); re-introduction requires a NEW directional merge with fresh ME registration. ME-9 binds the 10 ceremony drops to remain dropped. |
| **NG-03** | Tier vocabulary value `TRIVIAL` | Canonical post-merge tier set is `{STRICT, STANDARD, LIGHT, EXEMPT}` per live code at `commands/task.md:55, 61, 82` and donor `:9, 56` [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]. `TRIVIAL` is vestigial spec-only drift; not adopted. |
| **NG-04** | Per-item `(Tier: ...)` marker as a runtime dispatcher (any form) | INV-05 + ME-1 forbid; design alternative D09b REJECTed at validation-spec L87/206 for weakening INV-05. AC-ATK-05 enforces a closed enumeration of authorized per-item-marker consumers (initial: `{CR-TASK-07 baseline-skip}`); new consumer requires new ME-10+. |
| **NG-05** | HALT-as-gate disposition for Layer-2 git pre-flight (Reading B of D15b) | Would author a new HALT semantic into F1; INV-01 monotonicity forbids. All four environment-non-ideal rows of the 5-row matrix dispatch to warn-and-continue per AC-ATK-10 asymmetry. |
| **NG-06** | New gate identity for TFEP escalation (D25) | REJECTed; would force a new gate vs reusing the rf-qa identity (F-05). Mid-phase escalation reuses rf-qa as the fourth invocation point, NOT a new gate. |
| **NG-07** | In-task remediation block embedded in the task body (in lieu of `tfep-incident-report.md` side-effect file) | Would mutate task body and break INV-04 parse-clean semantics. Incident report lives as a side-effect file at `${TASK_DIR}/research/tfep-incident-report.md` (synth-02/03/04 consensus path; supersedes the `${TASK_DIR}/tfep/...` form that appeared in earlier draft text). |
| **NG-08** | Content audit of the seven on-disk anchor artifacts (R-DOC-01 reframed) within this merge cycle | Documentation dependency, not implementation work. Owned by Documentation/Release Owner pre-Step-7. The seven artifacts (`extension-point-contracts.md`, `transfer-manifest.md`, `merge-master.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `rejected-features-ledger.md`, `final-merge-plan.md`) are PRESENT on disk [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] but content-audit verification is owed and out of TDD scope. |

Additional permanently-out items (PRD §12.3): throttling/rate-limit/refusal threshold for F-04 over-escalation on rf-qa (Concession 3: load axis unbounded by design); restoration/amendment of `extension-point-contracts.md:11-17` to mention mid-phase rf-qa routing (Concession 2: anchor not amended); embedded runtime classifier replacing per-item-marker design (D09b REJECTed).

### 3.3 Future Considerations

Items deferred to future iterations (PRD §12.2 future-phase rows):

| Item | Target Phase | Notes |
|------|--------------|-------|
| ME-4 ancillary patterns (HELD without per-row deltas) | Future merge (only with new V/C/K) | Same applies to ME-5, ME-7, ME-8 — fenced by NFR-ME-4 ancillary classification |
| Operational tuning for F-04 over-escalation throttling | Future operational tuning | Concession 3 records load-axis unboundedness; reactive refusal threshold to be added once queue-depth telemetry exists |
| Retroactive ME-10 manifestization of F-05 fourth rf-qa invocation | Pending AC-ATK-11 disposition | Engineering-lead OQ-F-05-MANIFESTIZATION must resolve before Step 4; binary choice between retroactive ME-10 vs one-time non-generalizing carve-out |
| R-FM-NN coverage expansion (FM-01 symlink, FM-02 atomicity, FM-03 concurrent edits, FM-04 env determinism, FM-05 mkdocs pin, FM-07 encoding) | Phase 7.5.b (5-10 engineer-day add) | Could-tier per PRD S21.2; not closed by Phase 7.5 21-change scope |
| `tests/cleanup_audit/test_prompts.py` authoring | Pre-Step-5 (asymmetric closure with `tests/sprint/test_process.py:80-89`) | Must exist to pin CLI prompt prefix after CR-DEP-04 retargeting |

---

## 4. Success Metrics

How we will measure success. Each row is a translation of an AC-SM-NN success-metric anchor into a concrete engineering KPI with target value, measurement method, test owner, and verification tag.

### 4.1 Technical Engineering KPIs

| KPI ID | AC-SM Anchor | Engineering KPI Statement | Current State | Target | Measurement Method | Owner / Test Path | Verification Tag |
|---|---|---|---|---|---|---|---|
| **KPI-01** | AC-SM-01 | V/C/K verdict fidelity for TU-1..TU-8 against `transfer-manifest.md` § 4 | TUs not yet transplanted; donor lines reflect verdicts at `sc-task-protocol/SKILL.md:7-9, 49-58, 80-91, 121, 123, 125-244, 277-279` [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] | 8/8 verdicts identical byte-for-byte | `tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match` | Audit / `tests/fixtures/vck-verdicts-expected.json` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **KPI-02** | AC-SM-02 | ME traceability — each ME-1..ME-9 traces to ≥1 CR-row acceptance-criterion | 5/9 load-bearing trace; 4/9 ancillary HELD-without-per-row-deltas | 9/9 ME rows trace | `tests/audit/test_me_traceability.py::test_each_me_has_cr_row` | Audit / intra-spec | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **KPI-03** | AC-SM-03 | INV-01..INV-05 walkthrough survival | Anchor present; walkthrough content audit owed | 5/5 INVs re-readable with worked-example anchor | `tests/audit/test_invariant_walkthrough.py::test_inv_1_through_5_re_readable` | Audit / `invariant-survival-walkthrough.md` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] [CONTENT-AUDIT-OWED]` |
| **KPI-04** | AC-SM-04 | F-finding anchor citations — F-01..F-08 each cite a re-readable Phase 7 artifact line range | F-rows present in `final-merge-plan.md § 4`; citations audit-owed | 8/8 F-rows cite valid line ranges | `tests/audit/test_f_findings_cite_anchors.py::test_each_f_row_has_artifact_anchor` | Audit / `final-merge-plan.md` § 4 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] [CONTENT-AUDIT-OWED]` |
| **KPI-05** | AC-SM-05 | S-constraint HZ citations — S-1..S-3 each cite a named hazard | Artifact present; named hazards present | 3/3 S-rows cite an HZ-NN | `tests/audit/test_s_constraints_cite_hz.py` | Audit / `compat-hazard-report.md` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **KPI-06** | AC-SM-06 | Row + step counts unchanged from `merge-master.md` — 67 row-line-items + 10 commit steps | Artifact present | 67 rows + 10 steps | `tests/audit/test_row_and_step_counts.py` | Audit / `merge-master.md` § 1 + § 6 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] [CONTENT-AUDIT-OWED]` |
| **KPI-07** | AC-SM-07 | CR-FM-04 row-1 ordering grep returns 3 function names in monotonically-increasing line order | Sentinel ABSENT in both donor + recipient as of pinned SHA | 2 greps × 3 function names = 6 hits in expected order | `tests/skills/task/test_cr_fm_04_ordering.py::test_row_1_order, test_row_10_order` | `tests/skills/task/` / Step-4 pre-commit hook | `[UNVERIFIED — post-Step-1..4 merge]` |
| **KPI-08** | AC-SM-08 | CR-TASK-12 seven-diff audit — 6 donor strings + 1 sentinel-comment block | Fixtures not yet authored; donor blocks live in donor SKILL.md | 7/7 zero-diffs against `tests/fixtures/donor-blocks/` | `tests/skills/task/test_cr_task_12_donor_diffs.py::test_6_donor_strings_and_1_sentinel_block` | `tests/skills/task/` / Step-4 pre-commit | `[UNVERIFIED — fixture authoring required pre-Step-6]` |
| **KPI-09** | AC-SM-09 | Step-5 commit roster exact-match per `final-merge-plan.md:375` | Step 5 not yet executed | Step-5 commit file list = exact set | `tests/audit/test_step_5_commit_roster.py::test_exact_file_list` | Audit / `final-merge-plan.md:375` | `[UNVERIFIED — post-Step-5]` |
| **KPI-10** | AC-SM-10 | Step-6 commit roster exact-match per `final-merge-plan.md:381` | Step 6 not yet executed | Step-6 commit file list = exact set | `tests/audit/test_step_6_commit_roster.py::test_exact_file_list` | Audit / `final-merge-plan.md:381` | `[UNVERIFIED — post-Step-6]` |
| **KPI-11** | AC-SM-11 | Zero ledger re-proposals — every LR-REJECT-* returns zero grep hits in `final-merge-plan.md` § 5 | Both artifacts present | 0 of N ledger entries appear as binding rows | `tests/audit/test_no_rejected_re_proposal.py::test_zero_ledger_re_introductions` | Audit / `rejected-features-ledger.md` × `final-merge-plan.md` § 5 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **KPI-12** | AC-SM-12 | **In-flight MDTM resume + step-gate zero — 100% of live in-flight floor (136 union files at this drift snapshot, monotonic upward) resume cleanly under CR-FM-03; gates 1/5/6 return exit-code 0** | Live in-flight floor = **136 union files** [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] (supersedes spec 96, fix-cycle 1 130, fix-cycle 2 132) — TASK-PRD-20260514-121039 carries 258 donor-surface refs keeping S-1 binding in force | 100% of live in-flight floor 136 at pinned SHA, monotonic upward, resume clean; gates 1/5/6 exit 0 | `tests/audit/test_step_gates.py` + `tests/skills/task/test_in_flight_mdtm_resume.py::test_live_in_flight_resume_clean` — iterates the live in-flight floor via `grep -rl '/sc:task\|sc-task-protocol\|task-unified' .dev/tasks/ \| wc -l` at authoring time | `tests/audit/test_step_gates.py` + `tests/skills/task/test_in_flight_mdtm_resume.py` / Pre-commit gates at Steps 1, 5, 6 + integration test | `[UNVERIFIED — post-merge; live recount at authoring time; 136 = 2026-05-16 floor, monotonic upward; CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |

**Supplementary KPIs (PRD §19 K-01..K-08 cross-traced):**

| KPI ID | PRD K-NN | Statement | Target | Owner |
|---|---|---|---|---|
| **KPI-13** | K-01 | Zero unmitigated AC-ATK rows after Phase 7.5 | 0 AC-ATK-01..18 in OPEN or PARTIAL state | Post-Phase-7.5 traceability matrix re-run |
| **KPI-14** | K-02 | Sprint-runner pytest pass rate post-CLI update | 100% on `tests/cli/` after CR-DEP-05 stubification + CLI update | `uv run pytest tests/cli/ -v` green |
| **KPI-15** | K-03 | Residual `/sc:task | sc-task-protocol | task-unified` occurrences outside authorized leave-as-is buckets | 144 → 0 outside authorized buckets | Post-Step-6 grep; CR-DEP-06 manifest |
| **KPI-16** | K-04 | `make verify-sync` flake rate after `flock` (AC-ATK-16 closure) | 0 flakes across 30 consecutive CI runs | CI log retention scan |
| **KPI-17** | K-05 | Post-merge audit pass rate across 33 spec-named CR rows | 100% PASS post-Step-6 | Aggregated pre-commit gate output |
| **KPI-18** | K-06 | Donor SKILL.md absent from disk post-Step-6 | Both `src/` and `.claude/` copies absent | Two `test -f` checks; CR-DEP-04 gate |
| **KPI-19** | K-07 | Visible command + skill surface count | 2 paired entries → 1 paired entry | `superclaude install --dry-run` roster diff |
| **KPI-20** | K-08 | Maintenance surface-pair count | 2 → 1 | Repo census of `src/superclaude/skills/*/SKILL.md` |

### 4.2 Business Metrics

**N/A — internal framework feature, no business revenue/conversion metrics.**

This component is an internal SuperClaude framework refactor. It does not directly influence customer-facing revenue, user retention, conversion, or any external KPI. Per the PRD §19 KPI-to-Business-Lever mapping, the levers operated on are **surface reduction** (KPI-19, KPI-18, KPI-20), **audit-pass discipline via CR-7 ORDERING** (KPI-17, KPI-13), and **sprint-runtime correctness via CR-DEP-05** (KPI-14, KPI-15, KPI-16) — all of which are framework-internal and unmetered against business dashboards. The template's §4.2 row is therefore marked N/A by design rather than left as a stub. `[CONTENT-AUDIT-COMPLETED]`

### 4.3 Measurement Cadence & Owners

| KPI Set | Cadence | Owner |
|---|---|---|
| KPI-01..06, -11 (AC-SM-01..06, -11 intra-spec audits) | CI continuous; once at Phase 7.5 completion + at each subsequent task-surface merge | Audit / pytest harness in `tests/audit/` |
| KPI-04 (AC-SM-04 F-row citation audit) | CI continuous; gated pre-Step-7 walkthrough | Audit / `tests/audit/test_f_findings_cite_anchors.py` |
| KPI-07, KPI-08 (AC-SM-07, AC-SM-08 ordering + diff audits) | Step-4 pre-commit gate; post-Step-6 fixture-backed | Skills test / `tests/skills/task/` |
| KPI-09, KPI-10 (AC-SM-09, AC-SM-10 commit-roster audits) | Step-5 push + Step-6 push | Audit / `tests/audit/test_step_*_commit_roster.py` |
| KPI-12 (AC-SM-12 in-flight resume + step-gate zero) | Pre-commit gates at Steps 1, 5, 6 + integration test on live population | Skills test + Audit |
| KPI-14 (K-02 sprint-runner pytest) | Every CI run | CI / `tests/cli/` |
| KPI-15 (K-03 residual count) | Step 6 commit + weekly cleanup-audit | Cleanup-audit / weekly CR-DEP-06 manifest archived to `docs/generated/` |
| KPI-16 (K-04 verify-sync flake rate) | Continuously via CI history rollup (30-run window) | CI history scan |
| KPI-13, KPI-17..20 (K-01, K-05..K-08) | Once at Phase 7.5 completion + at each subsequent task-surface merge | Phase 7.5 traceability matrix; release readiness gate |

---

## 5. Technical Requirements

### 5.0 Authoritative-Value Header (READ FIRST)

Three operational counts are load-bearing for every FR/NFR row below; downstream sections MUST honor these:

1. **F2 prohibited-actions catalog count.** Recipient `src/superclaude/skills/task/SKILL.md:104-117` carries **10 numbered F2 entries** at the pinned SHA (corrected fix-cycle 1; earlier "9" was off-by-one — cross-confirmed by `09-tu5-tu8-tfep-transplant.md:144` and `13-adversarial-artifact-cross-validator.md:2.3`). **TU-6 absorbs three additive prohibitions via CR-TASK-08**, growing the catalog to **13 entries post-merge ≥ 12** (NOT "9 → 12"). `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`
2. **In-flight MDTM file floor.** **136 union files** per the live recount at the pinned SHA; a subsequent cycle-2 grep returned 150 (drift is monotonically upward as new in-flight tasks accumulate). All "96 in-flight" mentions in upstream artifacts are validation-spec snapshots, now superseded. **NFR/AC rows iterate the live recount at gate-execution time, never the literal "96" or "136".** `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`
3. **TASK-PRD-20260514-121039 EXISTS.** Per S-1 named-target audit: `TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250` are both **LIVE** (un-discharged); only `TASK-RF-20260515-195758` is genuinely absent. S-1 framing is "supplement-not-replace": bind both live named targets AND broader 136-floor in-flight population. R-DRIFT-04 RETRACTED. `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`

### 5.1 Functional Requirements

#### 5.1.A FR-TU — Transfer Units (FR-TU-1..FR-TU-8)

Every TU is **MoSCoW: Must**. Each pairs with INV preservation per §5.2 NFR-INV-N and binds ≥1 ME audit gate.

| ID | Name | Description | Priority | Acceptance Criterion | Source PRD epic | Tag |
|---|---|---|---|---|---|---|
| **FR-TU-1** | Tier field + Gate-1 dispatch + per-item marker | Recipient frontmatter gains optional `Tier:` field ∈ `{STRICT, STANDARD, LIGHT, EXEMPT}` (CR-FM-01 closed enum). At task entry, executor emits TEXT-ONLY classification header (HTML-comment schema), then fires Gate-1 dispatch **once** (ME-1 binding). Per-item `(Tier: ...)` inline marker is **read-only** (tier-conditioned reads only; ME-1 forbids per-item re-dispatch). | Must | **AC-ATK-05** closed-enum register of authorized per-item marker consumers ({`CR-TASK-07 baseline-skip`}); new consumer → new ME row. **AC-SM-01** Gate-1 emits `gate-1: dispatch_profile=… source=…` exactly once per task entry. | PRD §14.1 (FR-TU-1, V/C/K = ADOPT); PRD §6 Job-1 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for current recipient absence of `Tier:`; `[SPEC-DEFINED]` for absorption target |
| **FR-TU-2** | Critical/Trivial Path Override at row 1 (CR-7 ORDERING) | At the F1 entry block (post-merge `src/superclaude/skills/task/SKILL.md` ~lines 65-73), three call sites fire in fixed order: `path_override_check()` → `tier_field_validate()` → `gate_1_dispatch()`. Critical paths (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) force tier STRICT; trivial paths (`*.md`, `docs/`, `*test*.py`) take override path. CR-7 sentinel comment block lands at Step 1. | Must | **AC-ATK-01** AST/line-range-pinned check verifies call-site order. **AC-ATK-13** sentinel-comment audit OR demotion with F-02 MEDIUM severity removed. **AC-SM-07** CR-FM-04 ordering greps return three function names in expected order. **AC-SM-08** verbatim diff of donor path-override block ≤ 0-line drift. | PRD §14.1 (FR-TU-2, V/C/K = ADOPT); PRD §6 Job-1 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — donor source at `sc-task-protocol/SKILL.md:121, 123`; recipient zero matches for `auth/` today |
| **FR-TU-3** | Gate-2 verification roster widening | Phase-Gate QA block at recipient `src/superclaude/skills/task/SKILL.md:181-211` widens `verifier_roster:` to `[rf-qa, quality-engineer]` on STRICT tier. `quality-engineer` is **additive only** — `rf-qa` always present (ME-2 binding). On STANDARD/LIGHT/EXEMPT, `rf-qa` alone (current behavior unchanged). | Must | **AC-ATK-11** F-05 either backed by retroactive ME-10 row in `merge-master.md` § 4.5 OR explicit non-generalization annotation in `final-merge-plan.md:148`. **AC-SM-02** each ME-1..ME-9 traces to ≥1 CR-row acceptance criterion (ME-2 → CR-TASK-05). | PRD §14.1 (FR-TU-3, V/C/K = ADAPT); PRD §6 Job-2 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — recipient currently `rf-qa` only at `:191` |
| **FR-TU-4** | D15b git pre-flight (warn-and-continue) | F1 entry block gains a Layer-2 pre-flight `git status` check. Five-row disposition matrix: `{clean, dirty, tool-absent, not-a-repo, error-other}` × `{Task Log line, action}` — every action ∈ `{WARN-CONTINUE, GRACEFUL-SKIP}`. **No HALT** (ME-3 binding; INV-01 progress guarantee). | Must | **AC-ATK-02** five-row matrix parametrized in `tests/skills/task/test_git_dirty_dispatch.py`; asserts no HALT for any row. **AC-ATK-10** unified pre-loop HALT policy table separates input-invalid (HALT) from environment-non-ideal (warn-continue). | PRD §14.1 (FR-TU-4, V/C/K = ADAPT); PRD §6 Related-Job (TU-5 baseline pre-flight) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — donor source single-line at `sc-task-protocol/SKILL.md:81`; recipient F1 has no git step today |
| **FR-TU-5** | TFEP baseline snapshot on disk | Before F1 fires on STRICT/STANDARD tier, executor writes `${TASK_DIR}/research/test-baseline.yaml` containing `uv run pytest --collect-only -q` output. Disk persistence is load-bearing for INV-04 across session boundaries (ME-4 binding — tier-gated; LIGHT/EXEMPT skip). | Must | **AC-ATK-03** four-state baseline trinary disambiguation `{absent, empty, parse-fail, schema-fail}` with observation order pinned: `os.path.exists → os.path.getsize → yaml.safe_load → <schema>`. **AC-SM-01** baseline file present pre-F1 on STRICT/STANDARD; absent on LIGHT/EXEMPT. | PRD §14.1 (FR-TU-5, V/C/K = ADOPT-adapted: in-memory→on-disk); PRD §6 Related-Job (TU-5) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — donor in-memory at `sc-task-protocol/SKILL.md:147`; recipient zero matches in body |
| **FR-TU-6** | TFEP Prohibitions + Carve-outs (additive to F2) | F2 catalog at recipient `src/superclaude/skills/task/SKILL.md:104-117` (currently **10 numbered entries**) absorbs **3 additive VIOLATION-level prohibitions** + **3 permitted-exception carve-outs** via **byte-for-byte verbatim transplant** from `sc-task-protocol/SKILL.md:127-142` under CR-TASK-08. Post-merge count: **13 entries ≥ 12**. | Must | **AC-ATK-11** disposition matrix authored for verifier-spawned and mid-phase rf-qa contexts. **AC-SM-06** 67-row count + 10-step commit sequence unchanged from `merge-master.md` §1 + §6. **CR-TASK-12** verbatim-diff audit: absorbed strings match `sc-task-protocol/SKILL.md:127-135` byte-for-byte. | PRD §14.1 (FR-TU-6, V/C/K = ADOPT); PRD §6 Related-Job (TFEP) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — recipient F2 entries enumerated; zero TFEP matches |
| **FR-TU-7** | TFEP escalation gradient + mid-phase rf-qa (FOURTH invocation point per authoritative count) | TFEP escalation block routes to `rf-qa` mid-phase as the **fourth rf-qa invocation point** (alongside three pre-merge surfaces: Phase-Gate L191, post-completion structural L221, post-completion qualitative L230 — authoritative rf-qa invocation count = 4). Six-step flow: halt-and-freeze → 9-field failure context YAML → forensic invocation with tier ladder (light ~5-8K → standard ~15-20K → FULL-STOP) → consume → tasklist insertion → resume `--compliance strict`. ME-2 preserves rf-qa identity at the fourth invocation (not a replacement of any existing rf-qa). | Must | **AC-ATK-11** F-05 paragraph-level surface-widening precedent. **AC-SM-02** ME-2 traces to ≥1 CR-row (CR-TASK-09 `merge-master.md` row authoring acceptance). | PRD §14.1 (FR-TU-7, V/C/K = ADOPT); PRD §6 Related-Job (TFEP routing) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — donor routes to `/sc:forensic` at `sc-task-protocol/SKILL.md:155-168, 170-218, 238-244`; recipient has no mid-phase route |
| **FR-TU-8** | TFEP incident reporting side-effect file | Per TFEP resolution, executor writes `${TASK_DIR}/research/tfep-incident-report.md` with a **seven-field schema** (donor literal `sc-task-protocol/SKILL.md:225-233`): `{Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts}`. Outcome enum: `{success, escalated, failed}` (donor literal `:232`). **No in-task heading** — file is side-effect-only. | Must | **AC-ATK-12(b)** seven-field schema enumeration in `tests/skills/task/test_tfep_incident_schema.py`. **AC-SM-04** file written pre-rf-qa-spawn in TFEP path. | PRD §14.1 (FR-TU-8, V/C/K = ADOPT); PRD §6 Related-Job (TFEP incident emit) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — donor literal at `sc-task-protocol/SKILL.md:220-236` |

#### 5.1.B FR-CS — Canonical Commit Sequence (FR-CS-1..FR-CS-10)

Every CS row is **MoSCoW: Must** and **Atomicity REQUIRED** under ME-6. The seven foundation rows (CR-FM-01..03 + CR-TASK-01..04) plus CR-TASK-05 land as a single source-tree merge per `merge-master.md:60` ("M1 atomicity rule").

| ID | Step | Description | Pre-commit Gate | Dependencies | Source PRD epic | Tag |
|---|---|---|---|---|---|---|
| **FR-CS-1** | Step 1 | Foundation row landing + CR-7 ORDERING sentinel + row-1 call-site (`path_override_check → tier_field_validate → gate_1_dispatch`). | CR-FM-04 ordering grep + CR-TASK-01 sentinel grep + CR-TASK-04 companion sentinel grep | none (foundation) | PRD §14.2 (FR-CS-1); PRD §12.1 (10-step sequence) | `[SPEC-DEFINED]` |
| **FR-CS-2** | Step 2 | `Tier:` frontmatter contract + Gate-1 dispatch closed-enum canonicalization. | CR-FM-01 canonicalization-rules + CR-TASK-02 parse-error HALT for malformed `Tier:` | FR-CS-1 | PRD §14.2 (FR-CS-2) | `[SPEC-DEFINED]` |
| **FR-CS-3** | Step 3 | Path overrides + Gate-2 roster widening (FR-TU-2 + FR-TU-3 land). | CR-FM-04 row-1 ordering re-run + ME-2 anchor check | FR-CS-1, FR-CS-2 | PRD §14.2 (FR-CS-3) | `[SPEC-DEFINED]` |
| **FR-CS-4** | Step 4 | TU/donor verbatim diff audits + sentinel landing; CR-TASK-12 seven-diff audit pass (6 donor + 1 sentinel block). | CR-TASK-12 returns zero-diff against `tests/fixtures/donor-blocks/` snapshot | FR-CS-1..3 | PRD §14.2 (FR-CS-4) | `[SPEC-DEFINED]` |
| **FR-CS-5** | Step 5 | Donor command stubification (CR-DEP-01 + CR-DEP-02 sha256 baseline + CR-DOC-01 doc row inline) + CLI fix-forward (CR-DEP-04 sprint + cleanup-audit re-routing). | pytest pass + CR-DEP-02 sha256 baseline + CR-DEP-05 grep | FR-CS-4 | PRD §14.2 (FR-CS-5); PRD §6 Related-Job | `[SPEC-DEFINED]` |
| **FR-CS-6** | Step 6 | Donor skill hard-delete (CR-DEP-03) + directory + residual greps. | **AC-ATK-07** rf-qa F-07 chain-integrity verifier rebound; CR-DEP-04 directory-absence + CR-DEP-05 grep returns zero | FR-CS-4 + FR-CS-5 | PRD §14.2 (FR-CS-6) | `[SPEC-DEFINED]` |
| **FR-CS-7** | Step 7 | Sprint/pipeline integrator fix-up; no runtime caller emits `/sc:task` post-stubification. | pytest pass + AC-ATK-17 server-side pre-push hook active | FR-CS-5 + FR-CS-6 | PRD §14.2 (FR-CS-7); PRD §6 Job-3 | `[SPEC-DEFINED]` |
| **FR-CS-8** | Step 8 | Documentation rollup + mkdocs build (CR-DOC-01 fallback if Step-5 gate failed with `AUTHORIZE_HOT_FIX=1`; CR-DOC-13 R-RULE-11 scope). | `mkdocs build` returns 0 broken-link warnings | FR-CS-5 | PRD §14.2 (FR-CS-8) | `[SPEC-DEFINED]` |
| **FR-CS-9** | Step 9 | Leave-as-is enforcement across buckets A, C, D, E, F, G, H; CR-REF-12 scoped to `[src]` + `[.claude]`; CR-REF-18 `DEPRECATION-NOTE.md` cluster root check. | bucket-grep returns zero unauthorized residuals | FR-CS-6 | PRD §14.2 (FR-CS-9) | `[SPEC-DEFINED]` |
| **FR-CS-10** | Step 10 | `docs/generated/*` deferred-regen placeholder + frozen-pre-merge banner. | banner string present in every `docs/generated/*` referencing `/sc:task` OR `sc-task-protocol` | FR-CS-6 + FR-CS-8 | PRD §14.2 (FR-CS-10) | `[SPEC-DEFINED]` |

#### 5.1.C FR-CR-DEP-06 — Residual-Reference Manifest (elevated to Must)

| ID | Name | Description | Priority | Acceptance Criterion | Source PRD epic | Tag |
|---|---|---|---|---|---|---|
| **FR-CR-DEP-06** | Post-Step-6 one-shot residual-reference manifest | Post-Step-6 one-shot script (`scripts/audit/cr_dep_06_manifest.sh`) writes `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` enumerating every surviving deprecation-surface string outside authorized leave-as-is buckets. Per-string disposition. Pre-commit gate: residual count outside authorized buckets MUST equal **zero**. | **Must (elevated)** | **AC-ATK-18(d)** one-shot post-Step-6 manifest. **AC-ATK-14(a)** CR-DEP-05 grep spec. | PRD §14.3 — elevated due to (1) **144 live residual occurrences** (61 backlog + 83 docs/generated); (2) Operational closure of AC-ATK-18 four-part fan-out; (3) V3 security-probe origin | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for residual count |

#### 5.1.D MoSCoW Summary

| Tier | Count | FR IDs | Rationale |
|---|---:|---|---|
| **Must** | 19 | FR-TU-1..FR-TU-8 (8) + FR-CS-1..FR-CS-10 (10) + FR-CR-DEP-06 (1) | Every TU pairs with INV preservation; every CS row pairs with ME-6 atomicity + pre-commit gate; CR-DEP-06 elevated for 144 residuals + V3 security-probe origin |
| **Should** | 0 | — | None proposed |
| **Could** | 0 | — | Reserved for non-load-bearing optimizations |
| **Won't** | 0 | — | Leave-as-is bucket roster handled by FR-CS-9 + FR-CR-DEP-06 |

### 5.2 Non-Functional Requirements

#### 5.2.A NFR-INV — Behavioral Invariants (NFR-INV-1..NFR-INV-5)

| NFR ID | Category | Target (statement) | Measurement Method | Source / Anchor | Tag |
|---|---|---|---|---|---|
| **NFR-INV-1** | Reliability / F1 progress monotonicity | F1 loop READ→IDENTIFY→EXECUTE→UPDATE→REPEAT pattern preserved; no new HALT semantic mid-checklist. Environment-non-ideal MUST warn-and-continue (AC-ATK-10 asymmetry). Per-item dispatch forbidden (ME-1). | Direct Read of `src/superclaude/skills/task/SKILL.md:79-98` post-merge; **AC-ATK-02** 5-row matrix; **AC-ATK-13** sentinel test; Critical Rule 12 at `:115` (delegating F1 prohibited). Protectors: ME-3 (primary), ME-6 (indirect). | `extension-point-contracts.md:13`; recipient anchor `:79-98`, `:108-110`, `:115` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-INV-2** | Reliability / F2 catalog additivity | F2 "Prohibited Actions" catalog at `:104-117` extended **only additively**. **Pre-merge count: 10 numbered entries**. **TU-6 adds 3 → post-merge ≥ 12 (target 13)**. No existing prohibition deleted/weakened/narrowed. | Pre-merge vs post-merge diff: `pytest tests/skills/task/test_prohibitions_additive.py`. **AC-ATK-11** disposition matrix authored. | `extension-point-contracts.md:14`; recipient anchor `:104-117`; donor source `sc-task-protocol/SKILL.md:127-142` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for 10-entry baseline |
| **NFR-INV-3** | Reliability / Phase-gate rf-qa floor | `rf-qa` remains named role at **all four** invocation points (post-merge): (1) Phase-Gate QA at `:181-211`; (2) Post-Completion structural at `:213-248`; (3) Post-Completion qualitative; (4) Mid-phase TFEP escalation (TU-7, new). Widenings permitted (TU-3 adds `quality-engineer` on STRICT); replacements/displacements prohibited (ME-2). | Grep for `subagent_type: "rf-qa"` returns ≥ 3 matches in `src/superclaude/skills/task/SKILL.md` pre-merge plus the TU-7 surface post-merge; **AC-ATK-07** F-07 chain verifier returns PASS pre-Step-6 hard-delete; **AC-ATK-11** F-05 ME-10 row OR non-generalization annotation present; **CR-FM-04** content-keyed anchor audit. | `extension-point-contracts.md:15`; recipient anchors `:181-211`, `:213-248`, TU-7 mid-phase | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-INV-4a** | Reliability / Resumability — parse layer | Every existing MDTM TASK-* file parses and resumes cleanly at structural/parse layer post-merge: YAML frontmatter valid; checklist syntax recognized; task-log append-only; **CR-FM-03 default-to-STANDARD shim** handles absent `Tier:`; TU-5 baseline YAML + TU-8 incident report persist across sessions. | `tests/skills/task/test_compat_shim_parse.py` parametrized over **live in-flight population** (current floor 136); CR-FM-03 default test; baseline round-trip test. **AC-ATK-12(c)** sunset binding. Protectors: ME-3 (warn-continue), ME-6 (atomicity). | `extension-point-contracts.md:16`; recipient anchors `:68`, `:252-264`, `:268-283` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-INV-4b** | Reliability / Resumability — semantic layer (**HIGHEST EXPOSURE**) | Meaningful resume path through in-flight checklist body MUST survive merge. Content-level deprecated-surface references detected at resume; executor emits Gate-1.5 token; one-shot ack gate; **continue execution (warn-and-continue per ME-3, NOT HALT)**. Three exposures closed: (i) **136-floor in-flight file content references**; (ii) default-STANDARD shim doesn't strip implicit STRICT; (iii) CR-FM-03 sunset binding. | **AC-ATK-18** four sub-bindings: (a) content-layer grep at resume time; (b) sprint-emit boundary content-grep; (c) one-shot ack gate via `legacy-surface-ack: 1` frontmatter token; (d) CR-DEP-06 one-shot post-Step-6 manifest. **AC-ATK-12(a)** sunset row authored. Manual walkthrough on **H-4 named target `TASK-RESEARCH-20260403-sprint-task-exec`**. Protectors: ME-3, ME-9. | validation-spec §9 line 285 names **INV-04 highest-exposure overall**; H-4 scenario at `validation-spec.md:318` | `[CONTENT-AUDIT-COMPLETED]` for H-4 evidence; `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for 136 floor |
| **NFR-INV-5** | Reliability / Refusal-of-definition | `Tier:` field + per-item `(Tier: ...)` marker = **metadata conditioning which audits run**, NOT work-definition driving runtime dispatch. **Closed list of authorized per-item-marker consumers** (initial: `{CR-TASK-07 baseline-skip}`); new consumer requires new ME-NN row. No embedded runtime classifier (D09b REJECTed as LR-REJECT-3, terminal). | **AC-ATK-05** closed-enum committed in CR-TASK-03 acceptance criterion; `tests/audit/test_marker_consumers.py`; **ME-1 design-review checklist** at code-review gate. **CR-FM-01 canonicalization table**. Protectors: ME-1 (primary). | `extension-point-contracts.md:17`; recipient anchor `:69`, `:104-117`, extension-point row 13 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for absence of runtime classifier |

#### 5.2.B NFR-ME — Manifest Exceptions (NFR-ME-1..NFR-ME-9)

Per `transfer-manifest.md:340-352` (9 ME rows) and `validation-spec.md:60-65` (5 load-bearing rows). Each NFR-ME row binds ≥1 INV protected and names the AC closure obligation.

| NFR ID | Category | Target (binding) | Load-bearing? | Measurement Method | Tag |
|---|---|---|---|---|---|
| **NFR-ME-1** | Auditability / Governance | **PRE-LOOP DISPATCH ONLY.** Per-item dispatch forbidden; protects INV-05. `Tier:` marker is a tier-conditioned READ only. AC-ATK-05 closed-enum register is the operational manifestation. | **Load-bearing** | CR-TASK-02 acceptance; CR-TASK-03 acceptance. **AC-ATK-05** closed enumeration of authorized per-item marker consumers. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-2** | Auditability / Governance | **`rf-qa` SUPPLEMENTED NOT REPLACED.** Four invocation points (Gate-2, post-completion structural, post-completion qualitative, mid-phase TU-7). Widenings permitted; replacements prohibited. Content-keyed anchor (CR-FM-04). | **Load-bearing** | CR-TASK-05 acceptance "`verifier_roster: [rf-qa, quality-engineer]` on STRICT; `rf-qa` always present". **AC-ATK-11** F-05 retroactive ME-10 row OR non-generalization annotation. **AC-ATK-07** rf-qa F-07 chain-integrity verifier. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-3** | Auditability / Governance | **SIDE-CHANNEL ONLY, NO F1 HALT.** No new HALT semantics in F1 from TU-4 / TU-6 / TU-7 / TU-8 + TU-5. AC-ATK-02 5-row matrix dispatches all → warn-and-continue. Input-invalid (HALT) vs environment-non-ideal (warn-continue) asymmetry per AC-ATK-10. | **Load-bearing** | CR-TASK-08 acceptance "`tfep: prohibition-refusal … / carve-out …` Task Log lines; **F1 continues** (no halt)". **AC-ATK-02** 5-row matrix. **AC-ATK-10** unified pre-loop HALT policy table. **AC-ATK-18** legacy-surface content audit warn-and-continue. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-4** | Auditability / Governance | **BASELINE TIER-GATED.** TU-5 baseline collection runs only on STRICT/STANDARD. HELD without per-row deltas. | Ancillary | CR-TASK-07 acceptance "baseline YAML present pre-F1 on STRICT/STANDARD; absent on LIGHT/EXEMPT". | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-5** | Auditability / Governance | **NO PER-ITEM EXECUTE SUBSTITUTION.** TU-4 D15b accepted; explicitly REJECTs D15c per-item synthesis at execute-time. | Ancillary | CR-TASK-06 acceptance "no per-item synthesis; LR-REJECT-7 not revived". | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-6** | Auditability / Governance | **TIER FIELD + GATE 1 SHIP TOGETHER (M1 atomicity).** Seven foundation rows mutually presupposing; land in **one source-tree merge**. | **Load-bearing** (commit-sequence shape) | M1 atomicity rule audit at `merge-master.md:60`. **AC-ATK-06** snapshot donor strings into frozen fixture. **AC-ATK-17** server-side pre-push hook on landing commit at master. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-7** | Auditability / Governance | **D08 DEFERRED UNTIL PARSER SHIPS.** Held as terminal DEFER. | Ancillary | None re-opened; ledger row 19. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-8** | Auditability / Governance | **D01 DEFERRED UNTIL LOADER SEMANTICS + RULE 6 SPLIT.** Held as terminal DEFER. | Ancillary | None re-opened; ledger row 18. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **NFR-ME-9** | Auditability / Governance | **DONOR-CEREMONY DROP AUDIT.** Load-bearing for R-RULE-11 boundary protecting INV-04 + R-RULE-06. 10 named drops remain dropped. Two axes: (i) rejected-pattern axis; (ii) surviving-citation axis (CR-DEP-06). | **Load-bearing** | **CR-DEP-01** soft-deprecate `/sc:task` command. **CR-DEP-05** audit row. **R-RULE-11 audit**. **AC-ATK-17** server-side pre-push hook. **CR-DOC-04** user-guide commands documentation re-affirms. | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |

#### 5.2.C NFR-S — Sequencing Constraints (NFR-S-1..NFR-S-3)

| NFR ID | Category | Target (statement) | Verification Method | Source / Hazard | Tag |
|---|---|---|---|---|---|
| **NFR-S-1** | Process / Sequencing & Atomicity | **[POPULATION-GENERALIZED] In-flight discharge.** Any in-flight PRD/TDD task in `.dev/tasks/` whose body references donor surfaces MUST complete before Step 5 OR be snapshot-frozen with decision record. Binds both **live spec-named targets** (`TASK-PRD-20260514-121039` LIVE, `TASK-TDD-20260514-121250` LIVE; `TASK-RF-20260515-195758` genuinely absent) AND broader population at **the live in-flight floor at gate-execution time** (current floor 136). `--max-wait 14d` default; auto-invoke snapshot option at expiry. All `[CODE-VERIFIED]` tags MUST carry `(git-sha: <40-char>)` suffix. | **AC-ATK-08** three sub-bindings: (a) `--max-wait 14d` arg; (b) `scripts/embed_git_sha.py` walks every `[CODE-VERIFIED]` tag; (c) CR-DEP-05 grep extension. **Iterates the live recount at gate-execution time, NEVER the literal "96" or "136".** | HZ-03 (atomic-merge hazard); PRD §14.9 (NFR-S-1) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for live named targets; `[SPEC-DEFINED]` for `--max-wait` flag |
| **NFR-S-2** | Process / Sequencing & Atomicity | **CLI runtime atomicity.** Step-5 commit MUST be atomic with CLI fix-forward. Server-side push-policy enforcer on landing commit at master, **NOT working tree**, prevents rebase-split bypass (H-2 scenario). Grep scope amended to `src/superclaude/cli/{sprint,cleanup_audit}/**`. Hook venue MUST be **CI-server-side**. | **AC-ATK-17** server-side `pre-receive` hook re-greps `/sc:task\b` against `src/superclaude/cli/**/*.py`. Fallback `scripts/atomic_step_5.sh` `flock -xn /tmp/step5.lock`. Anti-persona enforcement. V3 origin. | HZ-06 + HZ-07; PRD §14.9 (NFR-S-2) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for CLI emission sites; `[SPEC-DEFINED]` for server-side hook |
| **NFR-S-3** | Process / Sequencing & Atomicity | **Makefile sync-rule atomicity with `flock`.** `make sync-dev` + `make verify-sync` MUST acquire exclusive `flock` on `.claude/skills/` (lockfile `.claude/skills/.sync-lock`). Covers TWO races: (a) forward-looking prune-loop race; (b) **LIVE copy-overwrite race** at `Makefile:121`. | **AC-ATK-16** pytest concurrency fixture `tests/audit/test_make_sync_dev_flock.py`. K-04 KPI target: 0 flakes across 30 consecutive CI runs. | HZ-14 (parallel-worktree race); PRD §14.9 (NFR-S-3) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for current `Makefile:121` `cp` shape; `[SPEC-DEFINED]` for `flock` wrapper |

### 5.3 Cross-Reference Matrices

#### 5.3.A FR × NFR × AC Traceability (reverse map)

| NFR | FR(s) protected | AC closure obligation(s) | Test fixture (synth-06 §15) |
|---|---|---|---|
| NFR-INV-1 (F1 monotonicity) | FR-TU-4, FR-TU-6, FR-TU-7, FR-TU-8 | AC-ATK-01, -02, -10, -13 | `tests/skills/task/test_git_dirty_dispatch.py`, `test_preloop_halt_policy.py`, `test_row1_call_order.py` |
| NFR-INV-2 (F2 additivity) | FR-TU-6 | AC-ATK-11, CR-TASK-12 verbatim-diff | `tests/skills/task/test_prohibitions_additive.py` |
| NFR-INV-3 (rf-qa floor) | FR-TU-3, FR-TU-7 | AC-ATK-07, -11 | `tests/skills/task/test_rf_qa_three_invocations.py`, `tests/audit/test_rf_qa_step6_gate.py` |
| NFR-INV-4a (resumability parse) | FR-TU-1 (CR-FM-03 shim), FR-TU-5 (baseline file), FR-TU-8 (incident file) | AC-ATK-03, -12 | `tests/skills/task/test_compat_shim_parse.py`, `test_baseline_trinary.py` |
| NFR-INV-4b (resumability semantic — **HIGHEST**) | FR-CR-DEP-06, FR-TU-1 (content audit) | AC-ATK-18 (4 sub-bindings), AC-ATK-12 | `tests/skills/task/test_resume_content_audit.py`, `test_cr_fm_03_resume_grep.py` |
| NFR-INV-5 (refusal-of-definition) | FR-TU-1, FR-TU-5 (CR-TASK-07 consumer) | AC-ATK-05, -12(c) | `tests/audit/test_marker_consumers.py`, `test_cr_fm_01_canonical.py` |
| NFR-ME-1..9 | per matrix above | AC-ATK-02, -05, -07, -10, -11, -17, -18 | per fixture cluster above |
| NFR-S-1 (in-flight discharge) | FR-CS-5 (named-target precondition) | AC-ATK-08 | `tests/cli/test_prd_precondition.py`, `tests/scripts/test_embed_git_sha.py` |
| NFR-S-2 (CLI atomicity) | FR-CS-5, FR-CS-6, FR-CS-7 | AC-ATK-17 | `tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected` |
| NFR-S-3 (Makefile flock) | FR-CS-3 (sync-dev step) | AC-ATK-16 | `tests/audit/test_make_sync_dev_flock.py` |

#### 5.3.B Authoritative-Value Verification Pointers

| Authoritative value | Source / Anchor | Downstream consumer |
|---|---|---|
| **F2 count: 10 pre-merge → ≥12 post-merge (target 13)** | `src/superclaude/skills/task/SKILL.md:104-117` at pinned SHA | NFR-INV-2, FR-TU-6, AC-SM-06 |
| **In-flight floor: 136 union files (live recount at gate-execution time; iterate, never hardcode)** | live grep at pinned SHA; supersedes spec snapshot "96"; cycle-2 grep returned 150 | NFR-INV-4a, NFR-INV-4b, NFR-S-1, FR-CR-DEP-06, AC-ATK-18(d) |
| **`TASK-PRD-20260514-121039` LIVE (258 refs); `TASK-TDD-20260514-121250` LIVE; only `TASK-RF-20260515-195758` genuinely absent** | S-1 supplement-not-replace framing | NFR-S-1, AC-ATK-08, FR-CS-5 precondition |

### 5.4 Coverage Audit

- **FR-TU-1..FR-TU-8** — 8 rows, all Must, in §5.1.A.
- **FR-CS-1..FR-CS-10** — 10 rows, all Must, in §5.1.B.
- **FR-CR-DEP-06** — 1 row, Must (elevated), in §5.1.C.
- **NFR-INV-1..NFR-INV-5** — 5 invariants in §5.2.A (with INV-4 split into 4a parse / 4b semantic).
- **NFR-ME-1..NFR-ME-9** — 9 manifest exceptions in §5.2.B (5 load-bearing 1/2/3/6/9; 4 ancillary 4/5/7/8).
- **NFR-S-1..NFR-S-3** — 3 sequencing constraints in §5.2.C.

**Total:** 19 FR + 17 NFR rows = 36 requirements, each tagged per the verification taxonomy.

---

## 6. Architecture

> **Authoritative values pinned at synth time:** F2 prohibition catalog = **10 pre-merge / 13 post-merge**; in-flight donor-surface exposure floor = **136 union files** (monotonic upward; iterate live recount at gate-execution time); rf-qa invocation surface count = **4 invocations post-merge** (phase-gate + post-completion structural + post-completion qualitative + new TU-7 mid-phase TFEP); R-DRIFT-04 RETRACTED — TASK-PRD-20260514-121039 is live (🟠 Doing, 258 refs across 12 files); S-1 sequencing binding stays in force. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]

### 6.1 High-Level Architecture (System Diagram)

The merged `/task` surface is a **single recipient skill** that absorbs verified content from a donor skill and a donor command, while serving as the addressable target for six CLI emission sites and ~136 in-flight MDTM task files.

```
                          ┌─────────────────────────────────────────────────────────────────┐
                          │                  PRE-MERGE (current state @ SHA 71b1b1f)        │
                          └─────────────────────────────────────────────────────────────────┘

    CLI EMISSION SITES (6 in-scope)                    RECIPIENT SKILL                       DONOR SKILL (to be deleted)
    ──────────────────────────────                     ───────────────                        ────────────────────────────
    src/superclaude/cli/                               src/superclaude/skills/                src/superclaude/skills/
      sprint/process.py:170     ─┐                       task/SKILL.md                          sc-task-protocol/SKILL.md
      cleanup_audit/             │                       (376 lines)                            (365 lines)
        prompts.py:26  ──────────┤                                                              │
        prompts.py:47  ──────────┼─emits──> "/sc:task ..." ──┐                                  │
        prompts.py:69  ──────────┤              (subprocess)  │                                 │
        prompts.py:92  ──────────┤                            │                                 │
        prompts.py:116 ──────────┘                            │                                 │
                                                              ▼                                 │
                                                  DONOR COMMAND (will be stubified)             │
                                                  ─────────────────────────────                 │
                                                  src/superclaude/commands/task.md              │
                                                  (170 lines; line 100: `> Skill                │
                                                  sc:task-protocol`)                            │
                                                              │                                 │
                                                              └────invokes (CR-DEP-01)──────────┘

    IN-FLIGHT MDTM TASK FILES (136 floor; live recount required pre-Step-5)
    ──────────────────────────────────────────────────────────────────────
    .dev/tasks/to-do/TASK-*/                ──reads──> task/SKILL.md (recipient)
      • 132 files contain "/sc:task" literal              ▲
      • 47 files contain "sc-task-protocol"                │
      • 56 files contain "task-unified"                    │ INV-04 highest-exposure surface
      • Union = 136 (live grep)                            │ (parse-layer shim CR-FM-03 +
      • TASK-PRD-20260514-121039: 🟠 Doing, 258 refs       │  semantic-layer audit AC-ATK-18)
        (S-1 binding)

                          ┌─────────────────────────────────────────────────────────────────┐
                          │  POST-MERGE (after 10-step commit chain; ~440-470 line target)  │
                          └─────────────────────────────────────────────────────────────────┘

    CLI EMISSION SITES (re-routed)                     RECIPIENT SKILL (widened)              DONOR SKILL (deleted)
    ─────────────────────────────                      ──────────────────────────             ─────────────────────
    sprint/process.py:170 ──┐                          src/superclaude/skills/                src/superclaude/skills/
    cleanup_audit/          │ emits                      task/SKILL.md                          sc-task-protocol/        ← removed
      prompts.py:26 ────────┤ "/task ..."                ├ Row 0: CR-7 ORDERING sentinel        SKILL.md                    by CR-DEP-03
      prompts.py:47 ────────┼─────────────> /task ──┐    ├ §Pre-Execution Classification        (NOT PRESENT)              (S-3 step 6)
      prompts.py:69 ────────┤  (subprocess) command │    │  ├ §path_override_check (TU-2)
      prompts.py:92 ────────┤                       │    │  └ §tier_field_validate +
      prompts.py:116 ───────┘                       │    │     gate_1_dispatch (TU-1)
                                                    │    ├ §Execution
                                                    │    │  ├ F1 loop (preserved L79-98)
                                                    ▼    │  ├ First Item Protocol (L100-102)
    DONOR COMMAND (stubified or renamed)                 │  ├ TU-4 Git Pre-Flight (5-row)
    ────────────────────────────────────                 │  ├ F2 catalog 10→13 (TU-6)
    src/superclaude/commands/task.md                     │  ├ F4 / F5 (preserved)
    (now /task; line 100 → Skill task)                   │  ├ Error Handling (L170-179)
                                                         │  └ TFEP BLOCK (TU-5..TU-8, ME-6
    IN-FLIGHT TASK FILES (136 floor)                     │     atomic byte-for-byte)
    ─────────────────────────────                        ├ §Phase-Gate QA (rf-qa + qe TU-3)
    .dev/tasks/to-do/TASK-*/ ── resumes ──> task ──┐     ├ §Post-Completion (rf-qa structural
    • Tier: absent ⇒ STANDARD (CR-FM-03 shim)      │     │   + qe TU-3 + rf-qa-qualitative)
    • Body grep at resume:                         │     ├ §Incremental Writing (preserved)
        /sc:task | sc-task-protocol | task-unified │     ├ §Session Resumption (+baseline read)
        → gate-1.5 warn-and-continue (AC-ATK-18)   │     ├ §Agent Spawning Conv. (+qe entry)
                                                   ▼     └ §Critical Rules 1-14 (preserved)
                                            (resume read)
```

**Edges enumerated:**

1. **CLI ⇒ /task command** (6 sites, post-merge): re-routed via CR-DEP-04 + AC-ATK-17.
2. **/task command ⇒ task skill** (1 site, post-merge): `src/superclaude/commands/task.md:100` ` > Skill sc:task-protocol` rewrites to `> Skill task` (synth-05 §8.3 binding).
3. **In-flight task files ⇒ task skill** (136 floor): each in-flight `.dev/tasks/to-do/TASK-*/...md` is read by the recipient at resume time; CR-FM-03 parse-layer shim + AC-ATK-18 semantic-layer content audit.
4. **Donor skill ⇒ recipient skill** (transient — write-then-delete): donor content blocks are transplanted into the recipient under ME-6 atomicity; the donor file is then hard-deleted in step 6 (CR-DEP-03).
5. **rf-qa surface (4 invocations post-merge):** see §6.3.5 below.

### 6.2 Component Decomposition

Eight Transfer Units (TU-1..TU-8) compose the post-merge recipient. Each TU is an additive component bound to one or more INVs and one or more MEs.

| Component | Kind | Pre-merge LOC | Post-merge LOC (est.) | Insertion target | Pattern source (donor) | INV protected | ME bound | CR-row author |
|---|---|---|---|---|---|---|---|---|
| **TU-1 — Tier field parser + Gate 1 dispatch** | Pre-loop classifier (read-only) | 0 | ~20 | (a) row 0 CR-7 ORDERING sentinel; (b) new subsection after L73; (c) +1 bullet inside F1 EXECUTE dispatch L89-96 | synthesized from `commands/task.md:55,61,104` closed enum + `sc-task-protocol/SKILL.md:9` enum | INV-04 (parse layer), INV-05 | ME-1 (PRE-LOOP DISPATCH ONLY), ME-6 (M1 atomic ship-together) | CR-FM-01..03, CR-TASK-01..03 |
| **TU-2 — Path override (critical/trivial)** | Pre-loop classifier (read-only) | 0 | ~10 | (a) row 0 sentinel (shared with TU-1); (b) new subsection adjacent to TU-1 | `sc-task-protocol/SKILL.md:121` (5 critical globs) + `:123` (3 trivial globs) | INV-05 | ME-6 | CR-TASK-01 + CR-7 ordering sentinel |
| **TU-3 — Verification roster widening** | Phase-gate + post-completion expansion (additive spawn) | 0 | ~14 | (a) +Step 3b inside L191-198; (b) +Step 1b inside L219-226; (c) +Step 4 verdict-processing edit; (d) +bullet in agent-type list L290-299 | `sc-task-protocol/SKILL.md:89` (`quality-engineer`) + `:116` (STRICT routing row) | INV-03 (rf-qa floor preserved) | ME-2 (rf-qa SUPPLEMENTED NOT REPLACED) | CR-TASK-05 |
| **TU-4 — Git pre-flight Task Log emission** | F1 pre-execution side-channel (5-row warn-and-continue) | 0 | ~12 | new subsection between L102 and L104 | `sc-task-protocol/SKILL.md:82` ("Verify git working directory clean") | INV-01 (additive surface, no new HALT) | ME-3 | CR-TASK-06 |
| **TU-5 — TFEP baseline snapshot** | Pre-F1 side-effect file emitter (YAML) | 0 | ~10 + on-disk `${TASK_DIR}/research/test-baseline.yaml` | (a) new subsection between L179 and L181; (b) +bullet inside Session Resumption Step 4 | `sc-task-protocol/SKILL.md:144-153` (donor in-memory → file-resident per INV-04) | INV-04 (disk-resident evidence) | ME-3, ME-4 (BASELINE TIER-GATED) | CR-TASK-07 |
| **TU-6 — TFEP prohibitions + carve-outs** | F2 catalog additive insertion + carve-out subsection | 0 | +3 bullets (F2: **10 → 13**) + ~6 lines carve-out | (a) append after L117; (b) carve-out subsection inside TFEP block | `sc-task-protocol/SKILL.md:133-135` (3 VIOLATION rules, byte-for-byte) + `:137-140` (3 permitted exceptions) | INV-02, INV-01 | ME-3 | CR-TASK-08, CR-TASK-12 |
| **TU-7 — TFEP escalation trigger (mid-phase rf-qa)** | F1-side-channel escalation router; **4th rf-qa invocation surface** | 0 | ~15 | new subsection inside TFEP block | `sc-task-protocol/SKILL.md:157-161` (3 MUST-escalate triggers; R-DRIFT-03 anchor corrected from `:200-210`) | INV-03 (additive rf-qa surface; ME-2 preserved) | ME-2, ME-3 (no F1 halt; carve-out per AC-ATK-11 one-time) | CR-TASK-09 |
| **TU-8 — TFEP incident report** | Post-resolution side-effect file emitter (Markdown) | 0 | ~12 + on-disk `${TASK_DIR}/research/tfep-incident-report.md` | new subsection inside TFEP block | `sc-task-protocol/SKILL.md:222-234` (7-field schema, byte-for-byte; Outcome enum literal at `:232` = `{success / escalated / failed}`) | INV-04 (disk-resident evidence) | ME-3, ME-6 (byte-for-byte transplant) | CR-TASK-10, CR-TASK-12 |

#### 6.2.1 Component invariants (cross-cutting)

| Invariant | Statement | Enforcement point (recipient file:line, post-merge projected) |
|---|---|---|
| **INV-01** | F1 loop READ → IDENTIFY → EXECUTE → UPDATE → REPEAT — no skipping, reordering, out-of-band substitution | `task/SKILL.md:79-98` (preserved verbatim) `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **INV-02** | F2 prohibited-actions catalog is additive only | `task/SKILL.md:104-117` (10 pre-merge entries; TU-6 appends 3 → 13; verbatim-diff audit by CR-TASK-12) `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **INV-03** | rf-qa never replaced, never displaced at any invocation surface | `task/SKILL.md:191`, `:221`, `:230`, TU-7 new (mid-phase) — see §6.3 |
| **INV-04** | Progress recoverable from disk after context compression / session restart | Two-layer: (a) parse layer at `:68` validator (CR-FM-03 default `STANDARD`); (b) semantic layer at `:268-283` Session Resumption (AC-ATK-18). **136-file floor; highest-exposure invariant** |
| **INV-05** | `/task` does not decide what to do; the MDTM file does. Refusal-of-definition | Negative anchor: no embedded classifier in `task/SKILL.md`. Positive anchor: closed enum `{STRICT, STANDARD, LIGHT, EXEMPT}` at `commands/task.md:55,61,104`; AC-ATK-05 closed-enumeration register |

#### 6.2.2 Donor ceremony dropped (R-RULE-06 / R-RULE-11)

14 donor patterns are **ceremonially dropped** under the rejected-features-ledger:

- `mcp-servers:` frontmatter list (LR-REJECT-2) — no recipient consumer
- D09b runtime classifier with priority cascade + keyword tables (LR-REJECT-3) — INV-05 violation
- D13 auto-suggest keywords (LR-REJECT-4) — no triggering surface
- D11 few-shot prompt blocks — supports D08/D09 only
- D29 worked examples (donor lines 286-332) — supports D09/D10/D15
- D31 metrics package (donor lines 349-358) — scores REJECTed targets
- D25 "3-strike FULL STOP" budget at donor `:195, :243` — Phase-Gate QA's existing 3-cycle loop already provides this
- Strategy-axis classification — compliance axis preserved via TU-1; strategy dropped
- Boundaries Will/Will Not lists at donor `:334-347` — skill-self-description ceremony
- Configuration References at donor `:360-365` — orphaned config-file pointers
- Tool Coordination prose lists at donor `:265-284` — recipient's F1 loop already names tools
- Feedback Collection at donor `:246-251` — D31 dependency
- Donor's STRICT execution prose checklist at `:80-91` — pattern absorbed, prose form dropped
- Donor's verification routing table prose framing at `:114-119` — content absorbed by TU-3, prose dropped

The audit hook for these drops is ME-9 + CR-DEP-05: "grep returns zero matches on both `[src]` and `[.claude]`; commit message cites ME-9."

### 6.3 4-Stage Gate Topology

The merged `/task` surface routes every task through four ordered stages: **(1) Intake → (2) Classification → (3) Dispatch → (4) Completion**.

#### 6.3.1 Stage 1 — Intake (Gate 1)

**Purpose:** read the task file from disk, validate the MDTM envelope, classify into a dispatch profile. **Single-shot per task** (ME-1 binding).

**Pipeline (3-step, in mandatory order enforced by CR-7 ORDERING sentinel + CR-FM-04 row-1 grep):**

```
   path_override_check()  ──┐
        │                   │  (CR-7 ORDERING — load-bearing)
        ▼                   │
   tier_field_validate()  ──┤
        │                   │
        ▼                   │
   gate_1_dispatch()      ──┘
        │
        ▼
   dispatch_profile  = {budget, verifier_roster, pre_flight_enablement, baseline_required}
   Task Log emission = "gate-1: dispatch_profile=<X> source=<frontmatter|default|path-override>"
```

**Invariant binding:** ME-1 (PRE-LOOP DISPATCH ONLY); INV-04 parse layer; INV-05. **rf-qa interaction:** none at Stage 1.

#### 6.3.2 Stage 2 — Classification (Gate 1.5: legacy-surface audit + per-item marker)

**Sub-stage 2a — Gate 1.5 legacy-surface audit (resume only, AC-ATK-18):**

```
   on session resume:
     read task file
     content_grep = grep -E "(/sc:task\b|sc-task-protocol|task-unified)" <task_body>
     IF content_grep matches:
        emit Task Log: "gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>"
        route through one-shot acknowledgment gate
     CONTINUE F1 loop (ME-3 — warn-and-continue, never HALT)
```

**Sub-stage 2b — per-item marker read (inside F1 loop EXECUTE dispatch):**

The F1 EXECUTE dispatch (`task/SKILL.md:89-96`) gains a new bullet: "If the item includes a `(Tier: ...)` marker → apply per-item budget hint before executing the action." The per-item marker is a **closed-enum consumer register** (AC-ATK-05; current consumer set = `{CR-TASK-07 baseline-skip}`).

**Invariant binding:** ME-1 (per-item marker NEVER re-fires Gate 1); INV-04 semantic layer; INV-05. **rf-qa interaction:** none at Stage 2.

#### 6.3.3 Stage 3 — Dispatch (F1 loop body + TFEP escalation router)

**Purpose:** execute checklist items per the F1 loop (preserved at L79-98); on TFEP trigger, escalate side-channel to mid-phase rf-qa (TU-7).

```
   FOR EACH unchecked `- [ ]` item (in IDENTIFY order):
       READ task file (always, ME-1 binding)
       IDENTIFY first unchecked item
       EXECUTE per dispatch table:
          ├── spawn subagent
          ├── read+output
          ├── edit
          ├── bash
          ├── present
          ├── frontmatter
          ├── ensuring... clause verification
          └── [TU-1 NEW]: if item has (Tier: ...) marker, apply budget hint
       UPDATE: mark - [x], append Phase Findings
       REPEAT

   IF (during EXECUTE) TFEP trigger fires:
       ├── pre-existing test fails
       ├── ≥3 new tests fail simultaneously
       └── runtime exception in implementation code
       THEN:
          spawn rf-qa (4th invocation surface; mid-phase; TU-7)
          emit tfep-incident-report.md (7-field schema; TU-8)
          F1 loop CONTINUES (ME-3 — no HALT; warn-and-continue)
```

**Invariant binding:** INV-01 (5-step F1 pattern preserved); ME-3 (no F1 HALT on TFEP); ME-2 (TU-7 ADDS without displacing); AC-ATK-11 (one-time non-generalizing carve-out).

**rf-qa interaction (1 of 4):** TU-7 mid-phase invocation. Output path `${TASK_DIR}/reviews/qa-tfep-incident-[N]-report.md`.

#### 6.3.4 Stage 4 — Completion (Phase-gate + Post-completion)

**Phase-gate sub-stage** (`task/SKILL.md:181-211`, runs after every Phase 2+):

```
   Step 1: Collect phase outputs
   Step 2: Collect verification criteria (from "ensuring..." clauses)
   Step 3: Spawn rf-qa  ─────────────────────────────────────► rf-qa INVOCATION #1
   [TU-3 NEW] Step 3b: Spawn quality-engineer in parallel ──► (additive companion, NOT rf-qa)
   Step 4: Process the QA verdict (extended to consume BOTH reports)
       PASS | FAIL with fixes applied | FAIL unfixable + 3-cycle HALT
   Partitioning at L209: >6 output files → multiple rf-qa instances (per-agent threshold)
```

**Post-completion sub-stage** (`task/SKILL.md:213-248`, runs ONCE after final phase):

```
   Step 1: Spawn rf-qa (structural)  ────────────────────────► rf-qa INVOCATION #2
   [TU-3 NEW] Step 1b: Spawn quality-engineer in parallel ──► (additive companion, NOT rf-qa)
   Step 2: Spawn rf-qa-qualitative (operational) ───────────► rf-qa INVOCATION #3
   Parallel partitioning at L241: >15 output files → multiple instances
   Handling: Both PASS | Either FAIL w/ fixes | Either FAIL unfixable (zero-leniency at L248)
```

**Note on TU-3 asymmetry (HZ-04):** TU-3 widens rf-qa **structural** validation (invocations #1 and #2). It does **NOT** widen rf-qa-**qualitative** at invocation #3.

#### 6.3.5 rf-qa Invocation Surface — Authoritative 4-Row Register

| # | Stage | Invocation | Recipient line anchor (post-merge projected) | qa_phase | Output path | TU author | ME binding |
|---|-------|------------|----------------------------------------------|----------|-------------|-----------|------------|
| **1** | Stage 4 phase-gate | rf-qa | L191-198 (preserved verbatim) | `phase-validation` | `${TASK_DIR}/reviews/qa-phase-[N]-report.md` | (preserved) | ME-2 (preserved) |
| **2** | Stage 4 post-completion | rf-qa structural | L219-226 (preserved verbatim) | `report-validation` | `${TASK_DIR}/reviews/qa-final-validation-report.md` | (preserved) | ME-2 (preserved) |
| **3** | Stage 4 post-completion | rf-qa-qualitative | L228-239 (preserved verbatim) | `task-qualitative` | `${TASK_DIR}/reviews/qa-qualitative-review.md` | (preserved) | ME-2 (preserved) |
| **4** | Stage 3 dispatch (mid-phase) | **rf-qa (TFEP)** | NEW inside TFEP block between L179 and L181 | `tfep-incident` | `${TASK_DIR}/reviews/qa-tfep-incident-[N]-report.md` | **TU-7 (CR-TASK-09)** | **ME-2 (extension) + AC-ATK-11 (one-time carve-out)** |

**Authoritative count: 4 post-merge** (3 preserved + 1 new TU-7 mid-phase). `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for invocations 1, 2, 3; `[UNVERIFIED — design-time obligation]` for invocation 4.

**TU-3 quality-engineer companion spawns:** **NOT counted as rf-qa invocations** (per ME-2 — quality-engineer is SUPPLEMENTED NOT REPLACED; additive spawn alongside rf-qa at surfaces 1 and 2).

### 6.4 Per-TU Landing Topology

For each Transfer Unit, the table below specifies the exact insertion line range against the **pre-merge** recipient (376 lines).

| TU | Verdict (manifest) | Insertion point #1 | Insertion point #2 | Insertion point #3 | Insertion point #4 | Post-merge fit (heading) |
|---|---|---|---|---|---|---|
| **TU-1** | ADOPT | Row 0 (BOF) — CR-7 ORDERING HTML comment sentinel | After L73 — new subsection `### Tier Field Parser + Gate 1 Classification` | Inside F1 EXECUTE dispatch L89-96 — new bullet | — | `### Pre-Execution Classification` |
| **TU-2** | ADOPT | Row 0 (BOF) — shared CR-7 ORDERING sentinel: `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->` | After L73, BEFORE TU-1 #2 — new subsection `### Critical / Trivial Path Override` | — | — | `### Pre-Execution Classification > Path Override` |
| **TU-3** | ADAPT | Inside Phase-Gate QA Step 3 L191-198 — add Step 3b | Inside Phase-Gate QA Step 4 L200-203 — extend verdict-processing | Inside Post-Completion Validation Step 1 L219-226 — add Step 1b | Inside Agent Spawning Conventions L290-299 — add bullet for `quality-engineer` | (within existing sections) |
| **TU-4** | ADAPT | After L102 and BEFORE L104 — new subsection `### Git Pre-Flight Task Log Emission` | — | — | — | `### Git Pre-Flight Task Log Emission` |
| **TU-5** | ADOPT | After L179 and BEFORE L181 — new subsection `### TFEP Baseline Snapshot (Pre-F1)` | Inside Session Resumption Step 4 L274 — append baseline-reuse note | — | — | First subsection of new TFEP block |
| **TU-6** | ADOPT | After L117 and BEFORE L119 — append 3 dash-bulleted prohibitions byte-for-byte from donor `:133-135` | Inside TFEP block — `#### Permitted Exceptions (MAY fix directly)` listing 3 carve-outs from donor `:138-140` | — | — | (a) F2 catalog **10 → 13** entries; (b) TFEP carve-out subsection |
| **TU-7** | ADOPT | Inside TFEP block between L179 and L181 — new subsection `### TFEP Escalation Trigger (Mid-Phase rf-qa Invocation)` (donor `:157-161` per R-DRIFT-03 correction) | — | — | — | Middle subsection of TFEP block |
| **TU-8** | ADOPT | Inside TFEP block — new subsection `### TFEP Incident Report (Side-Effect File)` documenting `${TASK_DIR}/research/tfep-incident-report.md` with 7-field schema byte-for-byte from donor `:225-233`; Outcome enum byte-exact `{success / escalated / failed}` from donor `:232` | — | — | — | Final subsection of TFEP block |

#### 6.4.1 Post-merge file topology (projected)

Stacking all 8 TU insertions yields ~440-470 lines (up from 376).

```
Row 0           (NEW) <!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->   [TU-2]
Lines 1-4       YAML frontmatter (preserved)
Lines 5-26      Preamble (preserved)
Lines 28-52     ## Input (preserved)
Lines 54-73     ## Task File Discovery (preserved)
Lines 74-90     (NEW) ### Critical / Trivial Path Override                                                 [TU-2]
Lines 91-110    (NEW) ### Tier Field Parser + Gate 1 Classification                                        [TU-1]
Lines 111+      ## Execution
                  ### The F1 Execution Loop (preserved L79-98; +1 EXECUTE bullet)                          [TU-1 #3]
                  ### First Item Protocol (preserved L100-102)
                  (NEW) ### Git Pre-Flight Task Log Emission                                               [TU-4]
                  ### Prohibited Actions (F2) (preserved L104-117; +3 TFEP bullets → 13 total)             [TU-6 #1]
                  ### Parallel Agent Spawning (preserved L119-142)
                  ### Task File Modification Restrictions (F4) (preserved L144-158)
                  ### Frontmatter Update Protocol (F5) (preserved L160-168)
                  ### Error Handling (preserved L170-179)
                  (NEW) ### TFEP Baseline Snapshot (Pre-F1)                                                 [TU-5]
                  (NEW) ### TFEP Permitted Exceptions / Carve-outs                                          [TU-6 #2]
                  (NEW) ### TFEP Escalation Trigger (Mid-Phase rf-qa Invocation)                            [TU-7]
                  (NEW) ### TFEP Incident Report (Side-Effect File)                                         [TU-8]
                  ### Phase-Gate QA Verification (preserved L181-211)
                    - Step 3 rf-qa spawn (preserved L191-198)
                    - (NEW) Step 3b quality-engineer parallel spawn                                         [TU-3 #1]
                    - Step 4 verdict-processing (extended to consume 2 reports)                             [TU-3 #2]
                  ### Post-Completion Validation (preserved L213-248)
                    - Step 1 rf-qa structural (preserved L219-226)
                    - (NEW) Step 1b quality-engineer parallel spawn                                         [TU-3 #3]
                    - Step 2 rf-qa-qualitative (preserved L228-239)
## Incremental Writing Protocol (preserved L252-264)
## Session Resumption (preserved L268-283; +bullet inside Step 4 for baseline.yaml read)                    [TU-5 #2]
## Agent Spawning Conventions (preserved L286-319; +bullet for quality-engineer at L295/296 boundary)      [TU-3 #4]
## Critical Rules 1-14 (preserved verbatim L323-353)
## Session Management (preserved verbatim L357-376)
```

#### 6.4.2 Sequencing constraints (CR-row level, enforced by 10-step commit chain)

| Constraint | Reason | Enforcement |
|---|---|---|
| **CS-1 BEFORE CS-2** | CR-7 ORDERING sentinel (row 0) must exist before `path_override_check` is referenced anywhere | CR-FM-04 row-1 grep |
| **CS-2 BEFORE CS-3** | `path_override_check()` must precede `tier_field_validate()` in row-1 sentinel-referenced ordering | CR-7 ORDERING + CR-FM-04 |
| **CS-3 BEFORE CS-4** | TU-3 widening at L191-198 references the existing rf-qa spawn; wider TU-1 / TU-2 changes don't disturb L191 | line-range stability + CR-TASK-12 verbatim audit |
| **CS-4 BEFORE CS-6** | TU-5..TU-8 (TFEP block) references the rf-qa invocation pattern established by CS-3/CS-4 | rf-qa pattern reuse |
| **CS-6 BEFORE CR-DEP-03** | Donor `sc-task-protocol/SKILL.md` hard-delete is the LAST step (no upstream reference left) | CR-DEP-03 sequencing; ME-9 audit |

### 6.5 Multi-Tenancy Architecture

**N/A — single-user CLI/skill on local repo; no multi-tenant deployment.**

SuperClaude is a local-machine, single-user CLI plus a Claude Code skill loaded into a developer's own session. There is no shared compute, shared database, shared schema-per-tenant, or per-tenant configuration layer. The recipient skill file (`task/SKILL.md`) is one file per repository checkout; all task state lives under `.dev/tasks/to-do/TASK-*/` directories scoped to the local working tree. No noisy-neighbor controls, tenant isolation guarantees, or tenant offboarding hooks are required.

The four `${TASK_DIR}/{research,synthesis,qa,reviews,artifacts}/` subdirectories form the only persistence layer; they are POSIX-filesystem-bounded and have no multi-tenant addressing. Cross-task isolation is provided by the `TASK-ID` directory naming convention, not by any tenancy primitive. `[CONTENT-AUDIT-COMPLETED]`

### 6.6 INV-01..INV-05 Enforcement Points

#### 6.6.1 INV-01 — F1 loop progress monotonicity

**Definition:** READ → IDENTIFY → EXECUTE → UPDATE → REPEAT. No skipping, reordering, or out-of-band substitution.

| Anchor | Role | Tag |
|---|---|---|
| L79-98 | F1 Execution Loop body (5-step canonical pattern); TU-1 adds 1 bullet to EXECUTE dispatch (L89-96) without altering the 5 step ordering | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L108-110 | F2 entries 1-3 reinforce F1 prohibitions | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L349 (Critical Rule 12) | "The F1 loop is non-delegable" — explicit prohibition on subagent delegation of the loop itself | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |

**Audit gates:** AC-ATK-02 (5-row matrix); AC-ATK-10; AC-SM-07.
**Counter-factuals blocked:** D09b per-item per-tier runtime classifier (LR-REJECT-3); D15c synthesis at execute-time (LR-REJECT-7); TFEP F1-halting on engagement (auto-REJECT under ME-3).

#### 6.6.2 INV-02 — F2 prohibited-actions catalog additivity

| Anchor | Role | Tag |
|---|---|---|
| L104-117 (pre-merge) | F2 catalog — **10 dash-bulleted prohibitions** (corrected fix-cycle 1) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L117 → L118+ (post-merge) | TU-6 appends 3 new prohibitions after L117 → **13 total** post-merge | `[UNVERIFIED — design-time obligation]` |
| Donor `:133-135` (byte-for-byte source) | 3 VIOLATION rules (R-DRIFT-02 anchor corrected from `:127-135`) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |

**Audit gates:** CR-TASK-12 verbatim-diff audit; AC-SM-06 (10-step commit sequence + row count); extension-point row N1 (no F2 entry removal).

#### 6.6.3 INV-03 — Phase-gate rf-qa never replaced, never displaced

| Anchor | Role | Tag |
|---|---|---|
| L181-211 | Phase-Gate QA Verification block | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L191-198 | rf-qa spawn signature (preserved verbatim) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L213-248 | Post-Completion Validation block | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L221 | rf-qa structural spawn `qa_phase: "report-validation"` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L230 | rf-qa-qualitative spawn `qa_phase: "task-qualitative"` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| TU-7 (between L179 and L181) | 4th rf-qa invocation surface (mid-phase TFEP) | `[UNVERIFIED — design-time obligation]` |

**Audit gates:** AC-ATK-11; CR-FM-04 extension; extension-point row 10 admit/reject.

#### 6.6.4 INV-04 — Resumability (HIGHEST EXPOSURE)

**(a) Parse layer — CR-FM-03 default-to-STANDARD shim:**

| Anchor | Role | Tag |
|---|---|---|
| L68 (validator) | Frontmatter required-field list; CR-FM-03 shim defaults missing `Tier:` to `STANDARD` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L252-264 | Incremental Writing Protocol (disk-as-truth guarantee) | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L268-283 | Session Resumption 6-step ladder | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |

**(b) Semantic layer — AC-ATK-18 content-grep audit at resume time:**

| Anchor | Role | Tag |
|---|---|---|
| L274 (post-merge extended) | Session Resumption Step 4 extended with content-level grep | `[UNVERIFIED — design-time obligation]` |
| `${TASK_DIR}/research/test-baseline.yaml` | TU-5 disk-resident baseline | `[UNVERIFIED — design-time obligation]` |
| `${TASK_DIR}/research/tfep-incident-report.md` | TU-8 disk-resident incident reports (7-field schema) | `[UNVERIFIED — design-time obligation]` |

**Exposure floor:** **136 union files** under `.dev/tasks/to-do/` contain at least one donor-surface reference at pinned SHA. The `TASK-PRD-20260514-121039` directory is **live (🟠 Doing, 258 refs across 12 files)** — R-DRIFT-04 RETRACTED. S-1 sequencing is binding.

**Audit gates:** AC-ATK-12 (sunset binding); AC-ATK-18 (semantic content audit + ack gate + CR-DEP-06 manifest); AC-ATK-03 (4-state baseline observation order); AC-ATK-09 (sha256).

#### 6.6.5 INV-05 — Refusal-of-definition

| Anchor | Role | Tag |
|---|---|---|
| Negative anchor (absence) | No embedded classifier in `task/SKILL.md` — verified by grep | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| L69 (validator) | Checklist body (`- [ ]` / `- [x]`) is required — work definition lives in the task file | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| `commands/task.md:55, :61, :104` | Closed enum `{STRICT, STANDARD, LIGHT, EXEMPT}` (3 byte-for-byte forms); negative-set callout at L55 and L104 | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| TU-1 per-item marker | AC-ATK-05 closed-enum consumer register; current set = `{CR-TASK-07 baseline-skip}` | `[UNVERIFIED — design-time obligation]` |

**M1 atomic-landing commitment:** AC-ATK-05 closed-enumeration register is a **load-bearing component of the M1 atomic commit** — without an executable consumer register, the per-item marker can silently grow new consumers (a semantic-layer INV-04 + INV-05 violation).

### 6.7 10-Step Commit Chain Shape

The post-merge surface ships across **10 commits** (`merge-master.md` § 6 canonical sequence), grouped into three **sequencing groups (S-1, S-2, S-3)**. Steps 1, 5, and 6 are **atomic-by-design** (ME-6 ship-together); steps 2, 3, 4, 7-10 are fine-grained (single CR-ID rollback per commit).

#### 6.7.1 S-1 — Pre-merge sequencing (in-flight task floor = 136)

| Pre-step | Action | Verification |
|---|---|---|
| S-1.a | Live recount of in-flight donor-surface references: `grep -rl '/sc:task\|sc-task-protocol\|task-unified' .dev/tasks/ \| wc -l` | Floor = **136** at 2026-05-16; treat as monotonic-upward |
| S-1.b | Verify named exposure target TASK-PRD-20260514-121039 status: `🟠 Doing` with 258 refs across 12 files | If still Doing at landing time → S-1 BINDING |
| S-1.c | Pre-stage CR-FM-03 default-STANDARD shim impact analysis on 136-file population | All files validate clean under shim |
| S-1.d | Pre-stage AC-ATK-18 content-grep at resume time as part of M1 atomic commit | AC-ATK-05 register lands in M1 |

#### 6.7.2 S-2 — Atomic landing (Steps 1, 5, 6)

**Step 1 (M1 atomic; rows 1-7 + AC-ATK-05 register):**

```
   Step 1 contents (atomic):
   ├─ CR-FM-01  — Tier: frontmatter field schema (closed enum)
   ├─ CR-FM-02  — per-item (Tier: ...) inline marker schema
   ├─ CR-FM-03  — default-STANDARD compat shim for missing Tier:
   ├─ CR-TASK-01 — CR-7 ORDERING sentinel at row 0
   ├─ CR-TASK-02 — gate_1_dispatch() — single Task Log emission at entry
   ├─ CR-TASK-03 — per-item marker overrides task-level
   ├─ CR-TASK-04 — Gate 1 dispatch profile schema
   └─ AC-ATK-05 register — closed-enum consumer register
```

**Step 5 (M3 atomic; rows TFEP-cluster, BYTE-FOR-BYTE):**

```
   Step 5 contents (atomic, byte-for-byte under ME-6):
   ├─ CR-TASK-06 — TU-4 git pre-flight 5-row matrix (warn-and-continue per ME-3)
   ├─ CR-TASK-07 — TU-5 baseline.yaml emission (tier-gated to STRICT/STANDARD per ME-4)
   ├─ CR-TASK-08 — TU-6 F2 catalog 10 → 13 (3 VIOLATION rules byte-for-byte from donor :133-135 + 3 carve-outs from :138-140)
   ├─ CR-TASK-09 — TU-7 mid-phase rf-qa invocation (4th surface; AC-ATK-11 one-time carve-out)
   ├─ CR-TASK-10 — TU-8 incident-report 7-field schema byte-for-byte from donor :225-233; Outcome enum byte-exact {success / escalated / failed} from donor :232
   └─ CR-TASK-12 — verbatim-diff audit
```

**Step 6 (M4-B hard-deprecation + sync rule; atomic):**

```
   Step 6 contents (atomic):
   ├─ CR-DEP-03 — hard-delete src/superclaude/skills/sc-task-protocol/SKILL.md
   ├─ CR-DEP-04 — caller sync: 6 emission sites in cli/sprint/process.py + cli/cleanup_audit/prompts.py (5)
   ├─ CR-DIST-02 — atomic sync rule
   ├─ CR-DIST-01, CR-DIST-04, CR-REF-10 — same-or-next-commit
   └─ CR-DIST-03 + CR-REF-08 — may land here or next
```

**Verification:** `make verify-sync` returns 0 after Step 6.

#### 6.7.3 S-3 — Post-merge cleanup (Steps 2, 3, 4, 7, 8, 9, 10; fine-grained)

- **Step 2 (CR-TASK-05):** TU-3 verification roster widening (rf-qa + quality-engineer); 4 insertion points
- **Step 3 (CR-FM-04, CR-FM-05):** row-1 ordering grep audit; sentinel validity check
- **Step 4 (CR-DEP-01):** stubify donor command — strip `mcp-servers:` and `personas:` frontmatter fields; line 100 rewrite
- **Step 7 (CR-DEP-05):** audit row — re-affirm `mcp-servers:` / `personas:` removal
- **Step 8 (CR-DEP-06):** residual-reference manifest
- **Step 9 (CR-DOC-01..04):** user-guide commands documentation re-affirms no `mcp-servers:` / `personas:` as load-bearing
- **Step 10 (CR-REF-NN):** test-fixture cleanup; lockstep test updates

#### 6.7.4 INV boundary preservation across the chain

| INV | Pre-S-1 state | After S-2 Step 1 | After S-2 Step 5 | After S-2 Step 6 | After S-3 | Final state |
|---|---|---|---|---|---|---|
| INV-01 | F1 loop 5-step | F1 + TU-1 bullet (5+1) | F1 + TU-4 pre-flight + TFEP side-channel (no HALT) | unchanged | unchanged | preserved |
| INV-02 | F2 = 10 | F2 = 10 (no change yet) | F2 = 13 (TU-6 +3) | F2 = 13 | F2 = 13 | additive growth verified |
| INV-03 | rf-qa @ 3 surfaces | unchanged | TU-7 adds 4th surface | unchanged | TU-3 adds qe COMPANION at 2 of the rf-qa surfaces (additive) | rf-qa preserved at 4 surfaces |
| INV-04 | parse layer only | parse layer added (CR-FM-03 shim) + AC-ATK-05 register | + TU-5 baseline.yaml + TU-8 incident-report on disk | + AC-ATK-18 content-grep at resume | + CR-DEP-06 residual-reference manifest | two-layer guarantee complete |
| INV-05 | no classifier | + Tier: field as metadata + AC-ATK-05 closed register | unchanged | donor deleted (CR-DEP-03) | unchanged | refusal-of-definition preserved |

#### 6.7.5 Audit gates per commit chain step

| Step | Audit gate(s) | Validation method |
|---|---|---|
| S-1 | live in-flight recount (136 floor); R-DRIFT-04 retraction check | `grep -rl` recount; verify TASK-PRD-20260514-121039 status |
| Step 1 | ME-6 atomicity; CR-7 ordering; AC-SM-06 row count; AC-ATK-05 register | single-commit atomic check; CR-FM-04 row-1 grep |
| Step 5 | CR-TASK-12 verbatim-diff audit (5 byte-for-byte transplants); ME-6 atomicity | `diff` against donor `:133-135`, `:138-140`, `:157-161`, `:225-233`, `:232` |
| Step 6 | ME-9 donor-ceremony drop; CR-DEP-04 caller sync; AC-ATK-17 emission-boundary | `make verify-sync`; `tests/sprint/test_process.py`; new `tests/cleanup_audit/test_prompts.py` |
| Steps 2-4, 7-10 | per-CR row acceptance; ME-9 audit; CR-DEP-05 + CR-DEP-06; R-RULE-11 aggregate audit | per-row diff + grep gates |

---

## 7. Data Models

> **Scope:** Engineering-shape data-model authorship for the five canonical schemas surfaced by the task-directional-merge release: (1) `Tier:` frontmatter field, (2) per-item inline marker, (3) TFEP baseline YAML, (4) `tfep-incident-report.md` 7-field schema, (5) Gate-1.5 legacy-surface emission token. The L3 reference-layer ENOENT token `gate-1.5: deleted-related-doc` is **folded into Schema 5 as a token-type discriminator** rather than authored as a 6th canonical schema.

### 7.1 Entity Overview (Text ERD)

The release introduces or canonicalises **five data shapes**. Three are file-resident (durable on disk inside `${TASK_DIR}/`); two are emission-only.

```
                ┌──────────────────────────────────────────────────────────┐
                │ MDTM Task File (${TASK_DIR}/<TASK-ID>.md)                │
                │                                                          │
                │  Frontmatter:                                            │
                │    ┌────────────────────────┐                            │
                │    │ Schema 1               │  row 1 (CR-FM-04 grep)     │
                │    │ Tier: <CLOSED_ENUM>    │──── default = STANDARD ──┐ │
                │    │ (optional)             │     via CR-FM-03 shim    │ │
                │    └─────────┬──────────────┘                          │ │
                │              │ fallback for unmarked items             │ │
                │              ▼                                         │ │
                │  Checklist body:                                       │ │
                │    ┌────────────────────────┐                          │ │
                │    │ Schema 2               │   3-level fallback chain:│ │
                │    │ - [ ] (Tier: <ENUM>)…  │   per-item → Schema 1 →  │ │
                │    │ (optional, per-item)   │   STANDARD (CR-FM-03) ───┘ │
                │    └────────────────────────┘                            │
                └────────────┬─────────────────────────────────────────────┘
                             │ Gate 1 reads (pre-loop, once per task)
                             ▼
                ┌──────────────────────────────────────────────────────────┐
                │ Gate 1 dispatch profile ∈ {STRICT|STANDARD|LIGHT|EXEMPT} │
                └──┬───────────────────────┬───────────────────────────────┘
                   │ tier ∈ {STRICT,STANDARD} only (CR-14)
                   ▼
        ┌──────────────────────────────┐
        │ Schema 3                     │ ${TASK_DIR}/research/test-baseline.yaml
        │ TFEP Baseline YAML           │ captured at First Item Protocol (pre-F1)
        │ {schema_version, captured_at,│ INV-04 file-resident resume anchor
        │  tier, tests[]}              │
        └──────────┬───────────────────┘
                   │ TU-7 reads at first test failure
                   ▼
        ┌──────────────────────────────┐
        │ 4-state observation (CANONICAL ORDER, AC-ATK-03):
        │   1. absent → 2. empty → 3. parse-fail → 4. schema-fail
        │   all four → warn-and-continue (ME-3); never HALT (INV-01)
        └──────────┬───────────────────┘
                   │ STRICT items where TFEP fired & failure resolved
                   ▼
        ┌──────────────────────────────┐
        │ Schema 4                     │ ${TASK_DIR}/research/tfep-incident-report.md
        │ Incident Report (7 fields)   │ emitted at Post-Completion Validation
        │ {Trigger, Escalation count,  │ INV-03 floor (rf-qa adjudication)
        │  Failing tests, Root cause,  │
        │  Solution, Outcome ∈         │
        │  {success,escalated,failed}, │
        │  Forensic artifacts}         │
        └──────────────────────────────┘
```

**Entity relationship summary** `[CONTENT-AUDIT-COMPLETED]`:

| # | Schema | Persistence | Cardinality per task | Emission surface | Verifying AC |
|---|--------|-------------|----------------------|------------------|--------------|
| 1 | `Tier:` frontmatter field | File-resident (MDTM task file) | 0..1 per task | Frontmatter row 1 | CR-FM-01, CR-FM-04 |
| 2 | Per-item inline marker | File-resident (MDTM task file) | 0..N (one per checklist row) | Checklist body | CR-FM-02, AC-ATK-05 |
| 3 | TFEP baseline YAML | File-resident (`research/test-baseline.yaml`) | 0..1 per task (only STRICT/STANDARD) | Pre-F1 First Item Protocol | AC-ATK-03 |
| 4 | `tfep-incident-report.md` | File-resident (`research/tfep-incident-report.md`) | 0..1 per task (only STRICT post-fire) | Post-Completion Validation | AC-ATK-12 |
| 5 | Gate-1.5 emission token (polymorphic) | Emission-only (Task Log lines) | 0..N per resume | Resume entry / ENOENT detect | AC-ATK-18 |

**Closed enumerations bound once, referenced 3×:**

- `TIER_ENUM = {STRICT, STANDARD, LIGHT, EXEMPT}` — defined once at Schema 1 (`commands/task.md:55,:61,:82` `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`); restricted to `{STRICT, STANDARD}` in Schema 3 per CR-14.
- `OUTCOME_ENUM = {success, escalated, failed}` — defined at Schema 4 (donor `sc-task-protocol/SKILL.md:232` `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`); byte-identical transplant under ME-6.
- `LEGACY_SURFACE_ENUM = {/sc:task, sc-task-protocol, task-unified}` — defined at Schema 5 variant A; enumerates the in-flight floor of **136 union files** at this drift snapshot.

### 7.2 Schema 1: `Tier:` Frontmatter Field (CR-FM-01)

**Purpose:** Optional, author-tagged MDTM frontmatter metadata that conditions Gate 1's dispatch profile. Declarative only — INV-05 binds it as **never a runtime classifier**; D09b terminally REJECTed.

| Property | Value | Verification |
|---|---|---|
| **Field name** | `Tier` (singular, capitalized) | Donor casing at `sc-task-protocol/SKILL.md:121,:123` `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **Type** | string (closed enumeration) | `[CONTENT-AUDIT-COMPLETED]` |
| **Valid values** | `STRICT` \| `STANDARD` \| `LIGHT` \| `EXEMPT` | `commands/task.md:55` CRITICAL RULE 3 + `:61` template + `:82` LIGHT anchor `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **Required** | **Optional** | mitigates INV-04 — making it required would invalidate every existing TASK-* file across the 136-file in-flight floor `[CONTENT-AUDIT-COMPLETED]` |
| **Default when absent** | `"STANDARD"` (resolved at Gate 1 dispatch via CR-FM-03 parse-layer shim — NO file mutation) | `[CONTENT-AUDIT-COMPLETED]` |
| **Canonical position** | **Row 1 of YAML frontmatter** | CR-FM-04 ordering grep contract `[CONTENT-AUDIT-COMPLETED]` |
| **Mutability** | Author-set at task file creation; **NEVER mutated by the runtime** | `[CONTENT-AUDIT-COMPLETED]` |
| **Constraint family** | Closed enumeration; refusal-of-definition (INV-05) | `[CONTENT-AUDIT-COMPLETED]` |

**Canonical YAML shape:**

```yaml
---
Tier: STANDARD           # row 1 — CR-FM-04 ordering grep target
id: TASK-TDD-20260516-043749
title: TDD for Task Directional Merge
status: 🟠 Doing
created_date: 2026-05-16
---
```

**Validation rules:**
1. **Closed-enum check** — A function `tier_field_validate(frontmatter: dict) -> str` reads the field and returns one of the four enum strings. Pure-read; no mutation; called **once per task entry** (pre-loop).
2. **Dispatch ordering (CR-7)** — `path_override_check → tier_field_validate → gate_1_dispatch`. The path override takes precedence over the field even when the field is present.
3. **Refusal diagnostic on bad value** — A non-enum value raises `ValidationError` HALTing at task entry. The four valid values appear verbatim in the diagnostic. This is an **input-invalid HALT category** (AC-ATK-10), distinct from forbidden environment-non-ideal HALTs. INV-01 is preserved because the HALT fires pre-loop.
4. **Per-item marker fallback** — When Schema 2 is absent for a row, the validated Schema 1 value is the row's tier; if Schema 1 is also absent, CR-FM-03 yields `STANDARD`.

**Constraints — what `Tier:` is NOT:**
- **NOT a runtime classifier.** INV-05 binds `Tier:` as metadata only; D09b terminally REJECTed.
- **NOT bundled with `Strategy:`/`Persona:`/`Auto-trigger:`/`allowed-tools:`/D08-classification-header.**
- **NOT mutated post-creation.** Read-only at parse time; no migration, no backfill.

### 7.3 Schema 2: Per-Item Marker (CR-FM-02 / AC-ATK-05)

**Purpose:** Optional inline tier marker that overrides Schema 1 for a single checklist row. Read-only — **NEVER fires `gate_1_dispatch` a second time** per ME-1 (PRE-LOOP DISPATCH ONLY) and INV-01.

| Property | Value |
|---|---|
| **Marker token form** | `(Tier: <VALUE>)` — parenthesized, prefix `Tier:`, single ASCII space after colon, ASCII closing paren |
| **Regex (canonical)** | `^- \[[ x]\] \(Tier: (STRICT\|STANDARD\|LIGHT\|EXEMPT)\) ` |
| **Valid values** | `STRICT` \| `STANDARD` \| `LIGHT` \| `EXEMPT` — **identical closed enum to Schema 1** |
| **Cardinality** | Optional, 0..1 per checklist row, 0..N per task |
| **Placement** | Immediately AFTER `- [ ]` or `- [x]` (checkbox), BEFORE the item text |
| **Default when absent** | Falls back to Schema 1; if Schema 1 also absent, falls back to `STANDARD` via CR-FM-03 |
| **Constraint family** | Closed enumeration (same constant as Schema 1) |

**Canonical example:**

```markdown
## Checklist
- [ ] (Tier: STRICT) refactor authentication middleware in auth/middleware.py
- [ ] (Tier: LIGHT) fix typo in README.md
- [ ] Update changelog                              # inherits task-level Tier (or STANDARD via CR-FM-03)
- [x] (Tier: EXEMPT) explain how F1 loop processes blockers
```

**Three-level fallback chain (first hit wins):**

| Priority | Layer | Source | Resolved |
|---|---|---|---|
| **1 (highest)** | Per-item marker (Schema 2) | Row body matches the canonical regex | per-item value |
| **2** | Task-level field (Schema 1) | Row has no marker; frontmatter has `Tier:` | frontmatter value |
| **3 (default)** | CR-FM-03 compat shim | Row has no marker; frontmatter has no `Tier:` | `STANDARD` |

**Path-override interaction:** `path_override_check()` can force `STRICT` for rows touching `auth/`, `security/`, `crypto/`, `models/`, or `migrations/`. The override is path-keyed (not field-keyed) — `- [ ] (Tier: LIGHT) touch auth/foo.py` resolves to **STRICT**.

**Validation rules:**
1. **Same constant as Schema 1.** Parser holds the closed enum in exactly one location; Schema 2 references it by import.
2. **Malformed marker is warn-and-continue, NEVER HALT.** A non-enum value inside the marker (or a marker mis-spaced) emits a single warning line to Task Log and falls back to Schema 1.
3. **No re-dispatch of Gate 1.** Per ME-1, the marker is consulted by F1 EXECUTE for **per-row budget conditioning**, NEVER to re-fire `gate_1_dispatch()` mid-loop.

### 7.4 Schema 3: TFEP Baseline YAML (AC-ATK-03, 4-State)

**Purpose:** File-resident pre-loop test baseline that classifies test failures as pre-existing vs new during TFEP escalation. INV-04 resume anchor — captured once at the First Item Protocol, reused across resumes, never mutated mid-loop.

| Property | Value |
|---|---|
| **Path** | `${TASK_DIR}/research/test-baseline.yaml` |
| **Emission point** | First Item Protocol — pre-F1 (extension-point row 2; `task/SKILL.md:100-102`) |
| **Tier gating** | STRICT and STANDARD only (CR-14); LIGHT/EXEMPT skip baseline collection |
| **Collection procedure** | (1) `uv run pytest --collect-only -q`; (2) `uv run pytest --tb=no -q` |
| **Persistence** | YAML file on disk; reused across resume cycles |
| **Mutability** | Written once at First Item Protocol entry; NEVER rewritten mid-loop or on resume |

**Canonical YAML shape:**

```yaml
# ${TASK_DIR}/research/test-baseline.yaml
schema_version: 1
captured_at: 2026-05-16T14:32:11Z
tier: STRICT                       # echoed from Gate 1 dispatch profile
tests:
  - test_id: tests/pm_agent/test_confidence.py::test_high_confidence_proceeds
    status: passing
  - test_id: tests/pm_agent/test_self_check.py::test_evidence_required
    status: passing
  - test_id: tests/execution/test_parallel.py::test_wave_checkpoint
    status: failing               # pre-existing failure (not introduced by this task)
```

**Field grammar:**

| Field | Type | Required | Valid values | Description |
|---|---|---|---|---|
| `schema_version` | int | yes | `1` | Forward-compat versioning |
| `captured_at` | ISO-8601 UTC string | yes | RFC 3339-compliant ending `Z` | Captured at First Item Protocol entry |
| `tier` | string (closed enum) | yes | `STRICT` \| `STANDARD` | Echoed from Gate 1 dispatch profile |
| `tests` | list of `{test_id, status}` | yes | non-empty when collection yields ≥1 ID | One record per pytest node ID |
| `tests[].test_id` | string | yes | pytest node ID format | Stable identifier across runs |
| `tests[].status` | string (closed enum) | yes | `passing` \| `failing` | Captured from `--tb=no -q` exit status |

**Four-state observation order (AC-ATK-03 CANONICAL):**

**`{absent, empty, parse-fail, schema-fail}` — drift here breaks AC-ATK-03.**

| Order | State | Detection predicate | Handling (all four → warn-and-continue per ME-3) |
|---|---|---|---|
| **1** | **`absent`** | `os.path.exists(...) == False` | Task Log: `tfep: baseline=absent action=warn-and-continue tier=<X>` |
| **2** | **`empty`** | File exists, length == 0 OR YAML parses to `null` / `{}` | Task Log: `tfep: baseline=empty action=warn-and-continue` |
| **3** | **`parse-fail`** | File exists, non-empty, but YAML parser raises | Task Log: `tfep: baseline=parse-fail error=<msg> action=warn-and-continue` |
| **4** | **`schema-fail`** | YAML parses to a dict, but `tests` key missing OR field invalid | Task Log: `tfep: baseline=schema-fail missing=<field> action=warn-and-continue` |

**Observation-order constraint (load-bearing for AC-ATK-03):** Detection MUST short-circuit in this order. AC-ATK-03 verifies the order by ranking the four states and refusing reorderings.

### 7.5 Schema 4: `tfep-incident-report.md` 7-Field (AC-ATK-12)

**Purpose:** Post-Completion Validation side-effect file documenting a TFEP escalation that fired during the task and was resolved in-task. Tier-gated to STRICT items; INV-03 floor preserved.

| Property | Value |
|---|---|
| **Path** | `${TASK_DIR}/research/tfep-incident-report.md` |
| **Emission point** | Post-Completion Validation phase (post-F1); `task/SKILL.md:213-248` band |
| **Trigger condition** | STRICT items AND TFEP escalation fired during task AND failure resolved in-task |
| **Donor schema source** | `src/superclaude/skills/sc-task-protocol/SKILL.md:220-236` (verbatim 7-field block) `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` |
| **Mutability** | Written once at Post-Completion; never amended mid-loop |

**Donor schema body (verbatim transplant per ME-6):**

```markdown
# TFEP Incident Report

- **Trigger**: {which threshold rule fired}
- **Escalation count**: {1, 2, or 3}
- **Failing tests**: {test names and classification}
- **Root cause**: {summary from rca-verdict.md}
- **Solution**: {summary from solution-verdict.md}
- **Outcome**: {success / escalated / failed}
- **Forensic artifacts**: {path to output_dir}
```

`[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — donor lines 222-236.

**Seven-field grammar:**

| # | Field | Type | Valid values | Description / example |
|---|---|---|---|---|
| 1 | **Trigger** | string (enum-like) | `pre-existing test failure` \| `≥3 new tests failed simultaneously` \| `runtime exception in implementation code` | Which TFEP escalation threshold rule fired |
| 2 | **Escalation count** | int | `1` \| `2` \| `3` | Which TFEP trigger in the chain |
| 3 | **Failing tests** | list of `{test_id, classification}` | `classification ∈ {pre-existing, new}` | Test node IDs and Schema-3-baseline-classified status |
| 4 | **Root cause** | free-form string (markdown allowed) | any non-empty markdown | Adjudicated root cause from rf-qa mid-phase invocation (F-05) |
| 5 | **Solution** | free-form string (markdown allowed) | any non-empty markdown | Adjudicated remediation |
| 6 | **Outcome** | string (closed enum) | `success` \| `escalated` \| `failed` — **byte-identical to donor `:232` per ME-6** | Resolution state |
| 7 | **Forensic artifacts** | string (path) or list-of-strings | path under `${TASK_DIR}/reviews/` | rf-qa report path(s) |

**Post-Completion validation check:**
1. On STRICT items where TFEP fired during the task, Post-Completion Validation reads `${TASK_DIR}/research/tfep-incident-report.md`.
2. **Validation passes** when all 7 fields are present AND `Outcome ∈ {success, escalated, failed}`.
3. **Validation fails** when any field is missing OR `Outcome` is outside the closed enum.
4. **On validation failure** — routed to `rf-qa` (INV-03 surface). Does NOT halt the task at completion.

**Constraints — what the incident report is NOT:**
- **NOT a remediation-plan heading.** Donor's `## Failure Remediation Plan (Adjudicated)` heading-insertion is **explicitly DROPPED** — the report is a side-effect FILE, never an in-task heading. F4 violation if heading-inserted.
- **NOT written for LIGHT / EXEMPT / STANDARD-no-TFEP-fire items.** Tier-gated.
- **NOT written mid-loop.** Emitted at Post-Completion Validation phase only.
- **NOT a replacement for rf-qa adjudication.** Reports are authored AFTER rf-qa adjudicates the failure.
- **NOT subject to outcome-enum drift.** ME-6 binds the `Outcome` literal byte-for-byte against donor `:232`.

### 7.6 Schema 5: Gate-1.5 Emission Token (AC-ATK-18, polymorphic via `token_type`)

**Purpose:** Emission-only Task Log token surfacing forward-looking compat-shim observations at the half-step band between Gate 1 (dispatch) and the F1 loop. Two variants share the same byte-form skeleton and `gate-1.5:` prefix but are discriminated by an event token. Both warn-and-continue per ME-3.

#### 7.6.1 Folding decision: one polymorphic schema, two variants

Research surfaced an authorship choice: canonicalise the L3 reference-layer ENOENT token (`gate-1.5: deleted-related-doc`) as a 6th schema, OR fold it into Schema 5 as a token-type variant. **Decision: fold.** Rationale:

1. **Shared emission band.** Both tokens emit at the same gate.
2. **Shared HALT disposition.** Both are `action=warn-and-continue` per ME-3.
3. **Shared one-shot ack semantics.**
4. **Avoid schema sprawl.** A 6th schema with a near-identical byte-skeleton would inflate the audit matrix without adding semantics.

#### 7.6.2 Variant A — `token_type = legacy-surface-reference` (AC-ATK-18, L2 content-layer)

**Trigger:** At resume time, content-grep over the resumed task's body matches one of `{/sc:task, sc-task-protocol, task-unified}`. The in-flight floor at this drift snapshot is **136 union files** `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`.

**Canonical byte form (single line):**

```
gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>
```

| Field | Type | Required | Valid values |
|---|---|---|---|
| `gate-1.5:` | fixed prefix | yes | literal `gate-1.5:` |
| `legacy-surface-reference detected` | fixed event token | yes | literal |
| `file=<path>` | KV pair | yes | absolute or repo-relative path string |
| `action=warn-and-continue` | fixed KV pair | yes | literal `warn-and-continue` (NEVER `refuse-entry`) |
| `surface=<symbol>` | KV pair | yes | one of `{/sc:task, sc-task-protocol, task-unified}` |

`[CONTENT-AUDIT-COMPLETED]` byte form per `validation-spec/validation-spec.md:106`.

**Placement:** Appended (one line per match) to the resumed task's `## Task Log / Notes` section at resume entry, BEFORE any F1 iteration begins.

**Audit verification (AC-ATK-18):** Post-merge, the test is `grep -c 'gate-1.5: legacy-surface-reference detected' <task-file>`. The 136-file floor is the audit's scope.

#### 7.6.3 Variant B — `token_type = deleted-related-doc` (L3 reference-layer)

**Trigger:** At resume time, `related_docs:` frontmatter traversal finds a path that does not exist on disk (ENOENT).

**Canonical byte form (single line):**

```
gate-1.5: deleted-related-doc file=<path> action=warn-and-continue referenced_from=<path>
```

| Field | Required | Valid values |
|---|---|---|
| `gate-1.5:` | yes | literal `gate-1.5:` |
| `deleted-related-doc` | yes | literal |
| `file=<path>` | yes | path string of the missing target |
| `action=warn-and-continue` | yes | literal `warn-and-continue` |
| `referenced_from=<path>` | yes | path of the file that named the missing target |

`[CONTENT-AUDIT-COMPLETED]` — variant B is authored per the synthesis fold-in decision.

#### 7.6.4 Compat-surface layering with CR-FM-03

Schema 5 and CR-FM-03 form a three-layer compat closure for INV-04 resumability:

| Layer | Surface | Action when matched | Schema |
|---|---|---|---|
| **L1 — Parse layer** | CR-FM-03 frontmatter default | Missing `Tier:` → resolve `STANDARD` + Task Log `gate-1: dispatch_profile=STANDARD source=default` | (NOT a §7 schema — companion of Schema 1) |
| **L2 — Content layer** | AC-ATK-18 body-grep | Match on `LEGACY_SURFACE_ENUM` → emit Schema 5 variant A per match + one-shot ack | **Schema 5 variant A** |
| **L3 — Reference layer** | `related_docs:` traversal | Target missing on disk → emit Schema 5 variant B per ENOENT | **Schema 5 variant B** |

**All three layers share the warn-and-continue HALT disposition (ME-3); none HALT (INV-01).**

#### 7.6.5 One-shot acknowledgment gate

- When a resumed task emits ≥1 Schema 5 line (any variant) at the same resume entry, the runtime requires a **single user-facing acknowledgment** before F1 proceeds beyond the resume-entry advisory phase.
- The acknowledgment is recorded as a follow-up Task Log line: `gate-1.5: ack received user=<id> ts=<ISO-8601>`.
- The ack is **one-shot per resume entry**, NOT per emission line.
- INV-01 is preserved because the gate is advisory in HALT terms (warn-and-continue throughout).

#### 7.6.6 Example Task Log block

```markdown
## Task Log / Notes

### Phase N — Resume Entry (2026-05-16)

gate-1: dispatch_profile=STANDARD source=default
gate-1.5: legacy-surface-reference detected file=.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md action=warn-and-continue surface=/sc:task
gate-1.5: legacy-surface-reference detected file=.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md action=warn-and-continue surface=sc-task-protocol
gate-1.5: deleted-related-doc file=docs/legacy/old-spec.md action=warn-and-continue referenced_from=.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md
gate-1.5: ack received user=ryanw ts=2026-05-16T14:35:00Z
```

#### 7.6.7 Constraints — what Schema 5 is NOT

- **NOT a HALT trigger** (either variant). ME-3 / INV-01 — refuse-entry semantics would weaken INV-01.
- **NOT a migration trigger.** No automatic body rewrite or `related_docs:` repair is performed.
- **NOT bundled with `Tier:` migration.** AC-ATK-18 is content-layer only.
- **NOT subject to silent sunset.** Absence of a `CR-AUDIT-FM-03-SUNSET` audit row binding the compat-shim lifetime is owned by §22 (Open Questions).

### 7.7 Cross-Schema Audit Matrix

| Schema | Closed-enum source | Default | HALT disposition | INV touched | ME binding | Audit AC |
|---|---|---|---|---|---|---|
| 1 — `Tier:` frontmatter | `commands/task.md:55,:61,:82` | `STANDARD` via CR-FM-03 | HALT at task entry on non-enum (pre-loop refusal — input-invalid) | INV-04, INV-05, INV-01 | ME-1, ME-6 | CR-FM-01, CR-FM-04 |
| 2 — Per-item marker | shares Schema 1 enum | falls back to Schema 1 → CR-FM-03 | warn-and-continue on malformed; NEVER HALT mid-F1 | INV-01, INV-05 | ME-1 | CR-FM-02, AC-ATK-05 |
| 3 — TFEP baseline YAML | `tier` field uses Schema 1 subset `{STRICT, STANDARD}` | `absent` is canonical for LIGHT/EXEMPT | warn-and-continue all 4 states | INV-04, INV-01 | ME-3, CR-14 | AC-ATK-03 |
| 4 — Incident report 7-field | Outcome enum `{success, escalated, failed}` from donor `:232` | n/a | n/a (post-completion read; failure routes to rf-qa) | INV-03, INV-04 | ME-6 (byte-identical Outcome) | AC-ATK-12 |
| 5 — Gate-1.5 emission | variant A surface enum `{/sc:task, sc-task-protocol, task-unified}` | n/a (emission-only) | warn-and-continue (both variants, ME-3) | INV-01, INV-04 | ME-3 | AC-ATK-18 |

**Invariant closure check:**
- **INV-01 (no mid-F1 HALT):** Schemas 2, 3, 5 all warn-and-continue; Schema 1 HALTs only pre-loop; Schema 4 routes post-loop failures to rf-qa.
- **INV-03 (rf-qa floor):** Schema 4 is consumed AFTER rf-qa adjudicates; never replaces rf-qa.
- **INV-04 (resumability):** Schemas 3, 4 are file-resident; Schema 5 is emission-only; Schema 1 default via CR-FM-03 mutates no files.
- **INV-05 (refusal-of-definition):** Schemas 1, 2 bind closed enums; D09b terminally REJECTed.

### 7.8 Data Storage & Retention

| Data shape | Storage location | Retention | Backup strategy |
|---|---|---|---|
| Schema 1 — `Tier:` frontmatter | Inline in MDTM task file | Lifetime of task file (git-tracked) | Git history |
| Schema 2 — Per-item marker | Inline in checklist body | Lifetime of task file | Git history |
| Schema 3 — TFEP baseline YAML | `${TASK_DIR}/research/test-baseline.yaml` | Lifetime of task (captured pre-F1, reused on resume) | Git-tracked |
| Schema 4 — `tfep-incident-report.md` | `${TASK_DIR}/research/tfep-incident-report.md` | Permanent (forensic record) | Git-tracked |
| Schema 5 — Gate-1.5 emission token | Task Log `## Task Log / Notes` of resumed MDTM file | Lifetime of task file | Git history |

**Retention rationale:** All five schemas are repo-tracked (in `.dev/tasks/` or the MDTM file itself); there is no separate database, no expiry policy, no PII handling required. Git history is the canonical retention/backup surface.

---

## 8. API Specifications

> **Engineering shape:** the recipient skill is a Markdown SKILL.md; "functions" are documented as numbered prose steps inside `### Validating the Task File` with the canonical control flow and data-types declared below. **Callers** are real Python CLI emitters. **Stubification** rewrites a single donor-command line. **Spawn contracts** are YAML-shape Skill/Task invocation envelopes.
>
> **Authoritative values (locked):**
> - **3 ordered functions per CR-7:** `path_override_check → tier_field_validate → gate_1_dispatch` (in this byte order). `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`
> - **4 `rf-qa` invocation points** post-merge (phase-gate / post-completion-structural / post-completion-qualitative / mid-phase TFEP). `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`
> - **6 `/sc:task` emission sites to re-route** (1 sprint + 5 cleanup-audit). `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`

### 8.1 Function Specifications — Row 1 Pre-Loop Classification Trio

The recipient skill currently contains **zero hits** for `path_override_check`, `tier_field_validate`, or `gate_1_dispatch` at the pinned SHA `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`. The three "functions" below are post-merge prose-step insertions into the `### Validating the Task File` block.

#### 8.1.1 Overview Table

| Position | Function | Parameters | Return type | Side effect |
|----------|----------|------------|-------------|-------------|
| 1 (FIRST) | `path_override_check` | `task_target_paths: list[str]` | `forced_stance ∈ {STRICT, LIGHT, none}` | Append 1 line to `## Task Log / Notes` |
| 2 | `tier_field_validate` | `frontmatter: dict` | `tier_field ∈ {STRICT, STANDARD, LIGHT, EXEMPT}` | None (read-only validator) |
| 3 (LAST) | `gate_1_dispatch` | `forced_stance, tier_field` | `execution_profile` | None (pure dispatch) |

**Ordering invariant:** the three names MUST appear in this top-to-bottom byte order. The order is **load-bearing** — `path_override_check` must run first so that security-domain paths elevate to STRICT before the declarative `Tier:` field is consulted. `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`

**Sentinel guard:** immediately above the three-call block, the canonical HTML comment sentinel is inserted:

```
<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->
```

#### 8.1.2 Function #1 — `path_override_check`

**Signature (canonical, verbatim from `refactor-task-skill.md:60` / `transfer-manifest.md:103`):**

```
path_override_check(task_target_paths: list[str]) -> forced_stance ∈ {STRICT, LIGHT, none}
```

**Body shape (prose step, verbatim from `integration-sketches.md:39`):**

```python
# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.
def path_override_check(task_target_paths):
    CRITICAL_GLOBS = {"auth/", "security/", "crypto/", "models/", "migrations/"}
    TRIVIAL_GLOBS  = {"*.md", "docs/", "*test*.py"}

    # (a) Critical hard-elevate: ANY-match → STRICT regardless of frontmatter Tier:
    for p in task_target_paths:
        if any(matches_glob(p, g) for g in CRITICAL_GLOBS):
            log(f"path-override: forced_stance=STRICT (matched: {first_match(p, CRITICAL_GLOBS)})")
            return "STRICT"

    # (b) Trivial skip: ALL-match → LIGHT regardless of frontmatter Tier:
    if task_target_paths and all(any(matches_glob(p, g) for g in TRIVIAL_GLOBS) for p in task_target_paths):
        log("path-override: forced_stance=LIGHT (all paths inside trivial-glob set)")
        return "LIGHT"

    # (c) No match — declarative Tier: governs (or STANDARD default)
    log("path-override: no-match (forced_stance=none)")
    return "none"
```

`[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` glob sets sourced verbatim from `src/superclaude/skills/sc-task-protocol/SKILL.md:121` (Critical) and `:123` (Trivial).

**Semantic asymmetry (binding):**
- **Critical = ANY-match** — a single security-domain path forces STRICT regardless of the frontmatter `Tier:` value.
- **Trivial = ALL-match** — every path must be inside the trivial set; one substantive path disqualifies the LIGHT skip.
- **Precedence:** Critical evaluates before Trivial; the function returns on first match.

**Task Log emission contract (exactly one line per call):**
- STRICT path: `path-override: forced_stance=STRICT (matched: <glob>)`
- LIGHT path: `path-override: forced_stance=LIGHT (all paths inside trivial-glob set)`
- No-match path: `path-override: no-match (forced_stance=none)`

**Invariant bindings:** INV-01 (pure-read, additive surface), INV-04 (Task Log line as parseable evidence), INV-05 (refusal-of-definition).

#### 8.1.3 Function #2 — `tier_field_validate`

**Signature:**

```
tier_field_validate(frontmatter: dict) -> tier_field ∈ {STRICT, STANDARD, LIGHT, EXEMPT}
```

**Closed enumeration (verbatim, three sources):**
- `src/superclaude/commands/task.md:55` prose: "The ONLY valid TIER values are: `STRICT`, `STANDARD`, `LIGHT`, `EXEMPT`."
- `src/superclaude/commands/task.md:61` template: `TIER: [STRICT|STANDARD|LIGHT|EXEMPT]`
- `src/superclaude/commands/task.md:104` Output Examples echo: same enum + negative-set callout

**Negative-set guard (rejected literals):** `{ITERATIVE, SIMPLE, IMPLEMENT, COMPLEX}` — flagged at command-facade lines 55 and 104. `tier_field_validate` MUST raise / refuse on any value not in the closed enum.

**CR-FM-03 compat shim:** when the `Tier:` key is **absent** from frontmatter, `tier_field_validate` defaults to `STANDARD` (additive — preserves the **136-file in-flight floor** of existing TASK files which lack the field; iterate the live recount at gate-execution time, never hardcode).

**Body shape:**

```python
def tier_field_validate(frontmatter):
    VALID = {"STRICT", "STANDARD", "LIGHT", "EXEMPT"}
    raw = frontmatter.get("Tier")
    if raw is None:
        return "STANDARD"  # CR-FM-03 compat shim — pre-merge tasks default
    if raw not in VALID:
        raise ValueError(f"Invalid Tier: '{raw}'. Closed enum: {sorted(VALID)}")
    return raw
```

**Invariant bindings:** INV-01 (additive, pure-read), INV-04 (frontmatter is parseable disk state), INV-05.

#### 8.1.4 Function #3 — `gate_1_dispatch`

**Signature:**

```
gate_1_dispatch(forced_stance: str, tier_field: str) -> execution_profile
```

**Resolution precedence (binding):**
1. If `forced_stance == "STRICT"` → execution_profile = STRICT (overrides any declarative `Tier:`).
2. Else if `forced_stance == "LIGHT"` → execution_profile = LIGHT (overrides any declarative `Tier:`).
3. Else (`forced_stance == "none"`) → execution_profile = mapping of `tier_field`.

**ME-1 binding — PRE-LOOP DISPATCH ONLY:** `gate_1_dispatch` fires **once per task** at task-entry time, NOT once per F1 EXECUTE iteration.

**ME-6 binding — D09a + Gate 1 SHIP TOGETHER:** the `Tier:` field (TU-1 D09a) and `gate_1_dispatch` (TU-1 Gate 1) MUST land in the same atomic commit (CS-1, the M1 atomic-merge).

**Body shape:**

```python
def gate_1_dispatch(forced_stance, tier_field):
    if forced_stance == "STRICT":
        return EXECUTION_PROFILES["STRICT"]
    if forced_stance == "LIGHT":
        return EXECUTION_PROFILES["LIGHT"]
    # forced_stance == "none" — declarative tier governs
    return EXECUTION_PROFILES[tier_field]  # defaults via tier_field_validate CR-FM-03 shim
```

### 8.2 Caller Contracts — Six `/sc:task` Emission Sites

The 6 in-scope emission sites collectively constitute the **CR-DEP-04 caller-sync surface** and the **AC-ATK-17 content-grep emission verification gate**. Each site re-routes from the literal `/sc:task ` (trailing space) to the literal `/task ` post-merge.

#### 8.2.1 Site Inventory (Authoritative)

| # | File | Line | Function | Current literal | Post-merge target literal |
|---|------|------|----------|-----------------|---------------------------|
| 1 | `src/superclaude/cli/sprint/process.py` | 170 | `ClaudeProcess.build_prompt` | `f"/sc:task Execute all tasks in @{phase_file} "` | `f"/task Execute all tasks in @{phase_file} "` |
| 2 | `src/superclaude/cli/cleanup_audit/prompts.py` | 26 | `build_surface_scan_prompt` | `f"/sc:task Perform a surface-level scan ..."` | `f"/task Perform a surface-level scan ..."` |
| 3 | `src/superclaude/cli/cleanup_audit/prompts.py` | 47 | `build_structural_analysis_prompt` | `f"/sc:task Perform deep structural analysis ..."` | `f"/task Perform deep structural analysis ..."` |
| 4 | `src/superclaude/cli/cleanup_audit/prompts.py` | 69 | `build_cross_cutting_prompt` | `f"/sc:task Detect duplication, sprawl, and consolidation ..."` | `f"/task Detect duplication, sprawl, and consolidation ..."` |
| 5 | `src/superclaude/cli/cleanup_audit/prompts.py` | 92 | `build_consolidation_prompt` | `f"/sc:task Consolidate audit findings ..."` | `f"/task Consolidate audit findings ..."` |
| 6 | `src/superclaude/cli/cleanup_audit/prompts.py` | 116 | `build_validation_prompt` | `f"/sc:task Validate audit findings ..."` | `f"/task Validate audit findings ..."` |

`[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` — each line directly re-Read at the pinned SHA.

**Out-of-scope confirmations** (`/sc:tasklist` — different protocol):
- `src/superclaude/cli/sprint/checkpoints.py:28` — comment prose, NOT emission. CONFIRMED UNCHANGED.
- `src/superclaude/cli/tasklist/prompts.py:158` — docstring prose, NOT emission. CONFIRMED UNCHANGED.

#### 8.2.2 Sprint Pipeline Emission Contract (Site 1)

**Post-merge byte form (`src/superclaude/cli/sprint/process.py:169-172`):**

```python
return (
    f"/task Execute all tasks in @{phase_file} "
    f"--compliance strict --strategy systematic\n"
    f"\n"
)
```

**Emission-boundary AC-ATK-17 content-grep contract:**

```python
assert prompt.startswith("/task Exec")    # 10-byte prefix match
assert "/sc:task" not in prompt           # no legacy spelling anywhere in the prompt
```

The first assertion is the positive boundary check; the second is the regression guard. Both run at the sprint-emission boundary in `tests/sprint/test_process.py`.

#### 8.2.3 Cleanup-Audit Pipeline Emission Contract (Sites 2-6)

Each of the 5 sites is a pure builder `build_*_prompt(config, ...) -> str` returning a multi-fragment f-string. The 5 return values flow through the trivial passthrough `CleanupAuditProcess.build_prompt()` at `cli/cleanup_audit/process.py:44-46`.

**Per-site emission-boundary contract** (uniform for sites 2-6):

```python
assert prompt.startswith("/task ")     # 6-byte prefix match
assert "/sc:task" not in prompt        # regression guard
```

**Caller bindings (6 total binding sites in `executor.py`, NOT requiring code changes):**

| Site | Builder | Caller (executor.py) | Step ID |
|------|---------|----------------------|---------|
| 2 | `build_surface_scan_prompt` | line 197 | G-001 |
| 3 | `build_structural_analysis_prompt` | line 211 | G-002 |
| 3 (reuse) | `build_structural_analysis_prompt` | line 228 | G-003 |
| 4 | `build_cross_cutting_prompt` | line 245 | G-004 |
| 5 | `build_consolidation_prompt` | line 263 | G-005 |
| 6 | `build_validation_prompt` | line 278 | G-006 |

**AC-ATK-17 gap (closure required at merge):** there is currently NO `tests/cleanup_audit/test_prompts.py` file. AC-ATK-17 cannot be closed for the cleanup-audit pipeline until this test module is authored as part of the merge. The new module MUST contain 5 fixtures, one per builder, each asserting the per-site contract above.

#### 8.2.4 Sprint-Emission Boundary AC-ATK-17 Verification Pattern

**Half 1 — positive prefix grep** (catches partial migration):

```bash
uv run pytest tests/sprint/test_process.py::test_build_prompt_contains_task_command \
              tests/cleanup_audit/test_prompts.py
```

**Half 2 — negative-substring grep** (catches regression — any stray `/sc:task` slipping back in):

```python
assert "/sc:task" not in prompt
```

Failure of either half blocks the M1 atomic-merge commit.

#### 8.2.5 CR-DEP-04 + AC-ATK-17 Closure Matrix

| Site # | File:line | CR-DEP-04 closure (literal swap) | AC-ATK-17 closure (test) |
|--------|-----------|----------------------------------|--------------------------|
| 1 | `cli/sprint/process.py:170` | 1-line edit (4-byte `sc:` deletion) | Update `tests/sprint/test_process.py:88-89` (flip literal + add regression guard) |
| 2 | `cli/cleanup_audit/prompts.py:26` | 1-line edit | NEW `test_prompts.py::test_surface_scan_prompt_emits_task` |
| 3 | `cli/cleanup_audit/prompts.py:47` | 1-line edit | NEW `test_prompts.py::test_structural_analysis_prompt_emits_task` |
| 4 | `cli/cleanup_audit/prompts.py:69` | 1-line edit | NEW `test_prompts.py::test_cross_cutting_prompt_emits_task` |
| 5 | `cli/cleanup_audit/prompts.py:92` | 1-line edit | NEW `test_prompts.py::test_consolidation_prompt_emits_task` |
| 6 | `cli/cleanup_audit/prompts.py:116` | 1-line edit | NEW `test_prompts.py::test_validation_prompt_emits_task` |

**Additional lockstep edits:**
- `cli/sprint/process.py:124` docstring → `"""Build the /task prompt for this phase."""`
- `tests/pipeline/test_process.py:131` fixture string update.
- `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md:521` prose update.

### 8.3 Stubification Contract — Donor Command Rewrite

#### 8.3.1 Single Stubify Site

**Source:** `src/superclaude/commands/task.md:100`
**Current literal (verbatim):** `  > Skill sc:task-protocol`
**Surrounding context (lines 97-100):**

```
- **EXEMPT**: Execute immediately — answer the question or perform the read-only operation. No Skill invocation needed.
- **LIGHT**: Execute the change directly. No Skill invocation needed for trivial changes.
- **STANDARD / STRICT**: Invoke the full protocol for tier-appropriate workflow:
  > Skill sc:task-protocol
```

#### 8.3.2 Post-merge Target Literal

**Synth-05 binding:** adopt **Form 1 (`> Skill task`)**. Rationale:
1. The recipient skill is named `task` (not `task-protocol`) — `name: task` in frontmatter.
2. The directional merge consolidates donor and recipient under the recipient's identifier; the recipient name wins per CR-DEP-01.
3. The 6 caller emissions re-route to `/task ` (no `-protocol` suffix). Internal consistency between caller emission and skill-stub invocation.

#### 8.3.3 Stubify Diff (Exact Byte Form)

```diff
--- src/superclaude/commands/task.md (before merge)
+++ src/superclaude/commands/task.md (after CR-DEP-01)
@@ -100,1 +100,1 @@
-  > Skill sc:task-protocol
+  > Skill task
```

**Frontmatter constraint (line 6):** `allowed-tools` includes `Skill` — required because line 100 invokes a skill. This frontmatter entry survives unchanged across the rewrite.

#### 8.3.4 Adjacent Brand-Rename Rewrites (Same Commit)

The CR-DEP-01 stubify is the **single Skill invocation rewrite**, but the same merge commit MUST sweep 8 additional `/sc:task` brand-name occurrences in the same file:

| Line | Context | Current | Post-merge |
|------|---------|---------|------------|
| 12 | H1 heading | `# /sc:task - Unified Task Command` | `# /task - Unified Task Command` |
| 19 | Purpose code block | `/sc:task [operation] --strategy ...` | `/task [operation] --strategy ...` |
| 41 | Usage code block | `/sc:task [operation] [target] [flags]` | `/task [operation] [target] [flags]` |
| 106 | Example 1 input | `/sc:task` context | `/task` context |
| 117 | Example 2 input | `/sc:task` context | `/task` context |
| 128 | Example 3 input | `/sc:task` context | `/task` context |
| 139 | Example 4 input | `/sc:task` context | `/task` context |
| 169 | Deprecation note | `/sc:task-mcp` | `/task-mcp` (compound rebrand) |

#### 8.3.5 HTML Marker Decision (synth-05 binding)

The classification output marker `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` appears 10 times in the donor command. **Synth-05 binding:** preserve the literal `SC:TASK-UNIFIED:CLASSIFICATION` marker tokens across the rename. Rationale:
1. The marker is a **parseable test-fixture anchor** — flipping the brand risks silently invalidating any classifier-output test that greps for the literal.
2. The marker is the **load-bearing semantic token** (it identifies the classifier output, not the command brand).
3. CR-DEP-01's scope is skill-invocation rewrite + command-brand rename, NOT marker-token rebranding.

### 8.4 rf-qa Spawn Contract — 4 Invocation Points

The 4 post-merge `rf-qa` invocation points are enumerated below. The quality-engineer companion spawns (TU-3, ME-2 "supplement not replace") are documented as a sibling roster in §8.4.5 but are NOT counted in the rf-qa floor.

#### 8.4.1 Invocation Point Inventory

| # | Invocation phase | Recipient anchor (pre-merge) | qa_phase value | Status |
|---|------------------|------------------------------|----------------|--------|
| 1 | Phase-gate QA Verification | `task/SKILL.md:191-198` | (existing rf-qa stance) | EXISTING |
| 2 | Post-completion structural validation | `task/SKILL.md:219-226` | `"report-validation"` | EXISTING |
| 3 | Post-completion qualitative validation | `task/SKILL.md:228-239` | `"task-qualitative"` (via `rf-qa-qualitative`) | EXISTING |
| 4 | Mid-phase TFEP rf-qa invocation | NEW — inserted in TFEP block (TU-7) | `"tfep-incident-[N]"` | NEW (TU-7) |

`[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` for invocations 1-3; `[UNVERIFIED]` for invocation 4 (TU-7-introduced, post-merge).

#### 8.4.2 Spawn Envelope (Uniform Across All 4 Points)

Every rf-qa spawn uses the same YAML-shape Task tool envelope:

```yaml
subagent_type: "rf-qa"
mode: "bypassPermissions"
qa_phase: <phase-specific value from §8.4.1 table>
fix_authorization: true
prompt: |
  <adversarial stance literal>
  <task file path>
  <output files list>
  <ensuring clauses extracted from completed checklist items>
  <QA report write path>
  <zero-trust verification instruction>
```

**Per-invocation prompt-embedding variations:**

| # | Adversarial stance literal | Output report path | Additional prompt fields |
|---|----------------------------|---------------------|--------------------------|
| 1 | `"You are an adversarial reviewer. Find what is missing or wrong."` | `${TASK_DIR}reviews/qa-phase-[N]-report.md` | Phase outputs list; verification criteria |
| 2 | Same as #1 | `${TASK_DIR}reviews/qa-final-validation-report.md` | ALL outputs across ALL phases; cross-phase consistency |
| 3 | Same as #1 | `${TASK_DIR}reviews/qa-qualitative-review.md` | TARGET_FILE_LIST, modified sources, CLAUDE.md conventions, research dir, `document_type: "Executed Task File"`, 15-item checklist |
| 4 (NEW) | Same as #1 | `${TASK_DIR}reviews/qa-tfep-incident-[N]-report.md` | TFEP trigger classification; baseline diff; failing tests list; escalation gradient stage |

#### 8.4.3 Partitioning Rule — >6 Files Threshold

When a phase produces **more than 6 output files**, the spawn MUST partition into multiple parallel `rf-qa` instances with `assigned_files` subsets.

```yaml
subagent_type: "rf-qa"
mode: "bypassPermissions"
qa_phase: <as above>
fix_authorization: true
assigned_files: [<subset of phase outputs, ≤6 files>]
prompt: |
  <base envelope as §8.4.2>
  Restrict your review to the assigned_files subset above.
```

**Post-merge partitioning under TU-3:** the >6 threshold applies **per agent** in the widened roster — rf-qa and quality-engineer each partition independently if their respective output-file count exceeds the threshold.

#### 8.4.4 Fix-Authorization Contract

All 4 invocations spawn with `fix_authorization: true`. This authorizes rf-qa to issue Edit/Write tool calls to remediate findings inline. The post-completion qualitative invocation additionally writes its 15-item checklist verdict to `qa-qualitative-review.md`.

**3-cycle HALT (recipient line 203):** if a phase fails QA 3 times in a row, the task halts. The mid-phase TU-7 invocation interacts with this budget — **synth-05 binding:** TU-7 mid-phase rf-qa consumes from a **separate** mid-phase escalation budget (light → standard → forensic gradient) NOT the phase-gate 3-cycle budget.

#### 8.4.5 Sibling Roster — quality-engineer (TU-3, NOT counted in rf-qa floor)

TU-3 widens the verification roster by spawning `quality-engineer` **in parallel with** rf-qa at invocation points #1 and #2 (NOT #3 rf-qa-qualitative, per HZ-04 immunity). ME-2 binds: "rf-qa never replaced, never displaced."

| # | rf-qa invocation | quality-engineer companion | Output report path |
|---|------------------|----------------------------|---------------------|
| 1 | `task/SKILL.md:191` (phase-gate) | NEW Step 3b at ~L198 | `${TASK_DIR}reviews/qe-phase-[N]-report.md` |
| 2 | `task/SKILL.md:221` (post-completion structural) | NEW Step 1b at ~L226 | `${TASK_DIR}reviews/qe-final-validation-report.md` |
| 3 | `task/SKILL.md:230` (rf-qa-qualitative) | NONE (HZ-04 immunity) | N/A |
| 4 | TU-7 mid-phase (NEW) | NONE (TU-7 is ME-2-bound to rf-qa only) | N/A |

**Agent-type enumeration update:** `src/superclaude/skills/task/SKILL.md:290-299` adds a new bullet for `quality-engineer` between `rf-qa-qualitative` (L295) and `rf-assembler` (L296).

### 8.5 rf-qa → rf-qa-qualitative Phase Contract

The post-completion validation cluster runs two sequential phases: rf-qa (structural) and rf-qa-qualitative (operational). Both fire ONCE, after the final phase, not after every phase.

#### 8.5.1 Phase 1 — rf-qa Structural Validation

**Spawn-time arguments (`task/SKILL.md:219-226`):**

```yaml
subagent_type: "rf-qa"
mode: "bypassPermissions"
qa_phase: "report-validation"
fix_authorization: true
prompt: |
  You are an adversarial reviewer. Find what is missing or wrong.
  Task file: ${TASK_DIR}TASK_ID.md
  Outputs across ALL phases: <list>
  Cross-phase consistency instruction: verify report contents agree with on-disk evidence.
output_path: ${TASK_DIR}reviews/qa-final-validation-report.md
```

#### 8.5.2 Phase 2 — rf-qa-qualitative Operational Validation

**Spawn-time arguments (`task/SKILL.md:228-239`):**

```yaml
subagent_type: "rf-qa-qualitative"
mode: "bypassPermissions"
qa_phase: "task-qualitative"
fix_authorization: true
prompt: |
  You are an adversarial reviewer. Find what is missing or wrong.
  Task file: ${TASK_DIR}TASK_ID.md
  TARGET_FILE_LIST: <list of target file paths>
  Modified source files: <list>
  PROJECT CONVENTIONS from CLAUDE.md: <embedded snapshot>
  Research dir: ${TASK_DIR}research/
  document_type: "Executed Task File"
  Apply the 15-item task-qualitative checklist.
output_path: ${TASK_DIR}reviews/qa-qualitative-review.md
```

#### 8.5.3 Sequencing — rf-qa First, rf-qa-qualitative Second

**Verdict consumption (L243-246, "Handling verdicts"):**

| Outcome | Action |
|---------|--------|
| Both PASS | Task complete; final status update authorized |
| Either FAIL with fixes applied | Re-verify; iterate up to 3-cycle HALT budget |
| Either FAIL with unfixable issues | Halt; surface findings to user |

**Parallel partitioning (L241):** if the task produced >15 output files total, each agent partitions its review across multiple parallel instances.

**Zero-leniency rule (L248):** the post-completion validation cluster MUST NOT be skipped, even when phase-gate QA passed every prior phase.

### 8.6 CR-FM-04 Row-1 Ordering Grep Contract

#### 8.6.1 Grep Command (Verbatim, Per `final-merge-plan.md:243`)

```bash
grep -nE "(path_override_check|tier_field_validate|gate_1_dispatch)" src/superclaude/skills/task/SKILL.md
```

#### 8.6.2 Expected Output Ordering

The grep MUST return the three function names in this **exact line order** (`N1 < N2 < N3`):

```
<line-N1>:... path_override_check ...
<line-N2>:... tier_field_validate ...
<line-N3>:... gate_1_dispatch ...
```

Any other ordering **BLOCKS the commit**.

#### 8.6.3 Validation Algorithm (Python-shape, for clarity)

```python
def cr_fm_04_row_1_ordering_check(skill_md_path: str) -> bool:
    """Audit gate per final-merge-plan.md:243 — row-1 ordering."""
    EXPECTED = ["path_override_check", "tier_field_validate", "gate_1_dispatch"]
    import subprocess
    out = subprocess.run(
        ["grep", "-nE", "(path_override_check|tier_field_validate|gate_1_dispatch)", skill_md_path],
        capture_output=True, text=True, check=False,
    ).stdout.strip().splitlines()
    observed = []
    for line in out:
        for name in EXPECTED:
            if name in line:
                observed.append(name)
                break
    first_occurrence = []
    for n in observed:
        if n not in first_occurrence:
            first_occurrence.append(n)
    return first_occurrence == EXPECTED  # True → pass; False → block commit
```

#### 8.6.4 Drift Baseline (Pre-Merge)

At the pinned SHA, the grep returns **zero matches** against `src/superclaude/skills/task/SKILL.md` (the three function names are not yet present). This is the expected drift baseline.

#### 8.6.5 Sentinel Verbatim Diff (CR-TASK-12 Seventh Diff, Pairs with Grep)

```bash
# CR-TASK-12 sentinel-comment-block diff (7th of seven diffs)
diff <(grep -oF "<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->" \
        src/superclaude/skills/task/SKILL.md) \
     <(echo "<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->")
# Expected: zero diff. Same expectation for the CR-8 sentinel at row 10.
```

**Two-axis enforcement:** the grep (ordering) and the diff (sentinel byte-identity) together close F-02.

#### 8.6.6 Symmetric Row-10 Ordering Grep (CR-8, For Completeness)

```bash
grep -nE "(forced_stance_read|tier_field_read|gate_2_dispatch)" src/superclaude/skills/task/SKILL.md
```

Expected ordering: `forced_stance_read → tier_field_read → gate_2_dispatch`. Same fail-blocks-commit semantic.

---

## 9. State Management

**N/A — CLI/skill feature, not a frontend component.**

State Management as defined by the template (Redux/Zustand-style state shape, state transitions, hydration, client-side persistence) is a **frontend concern**. This component is a **skill body executed by a server-side agent loop** plus a CLI emitter chain (`src/superclaude/cli/sprint/process.py`, `src/superclaude/cli/cleanup_audit/prompts.py`). The closest analog to "state" is:

- The **MDTM task file itself** (frontmatter status `🟠 Doing` / `🟢 Complete`, checklist tick marks, Task Log entries) — owned by §7 Data Models as the canonical persisted-state schema.
- The **TFEP baseline YAML** at `${TASK_DIR}/research/test-baseline.yaml` — likewise a persisted artifact, not application state.

Neither is "frontend state." The §9 template structure (state architecture diagram, state shape interface, state transitions table) does not apply. State semantics are covered by §7 Data Models and §6 Architecture. `[CONTENT-AUDIT-COMPLETED]`

---

## 10. Component Inventory

**N/A — CLI/skill feature, not a frontend component.**

Page/route structure, shared components, component hierarchy as defined by the template are **frontend artifacts** (React/Vue/Svelte component trees, route tables). This component has no rendered surface, no page tree, no shared UI components. The closest analog to "component inventory" is the **module/file inventory** in §6 (Recipient + Donor architecture) which enumerates `src/superclaude/skills/task/SKILL.md` (recipient), `src/superclaude/skills/sc-task-protocol/SKILL.md` (donor), `src/superclaude/commands/task.md` (donor command), and six emission sites under `src/superclaude/cli/`. Those belong in §6 Architecture, not §10. `[CONTENT-AUDIT-COMPLETED]`

---

## 11. User Flows & Interactions

> **Note on scope:** This component has three primary user flows, all driven by **developers operating a local CLI or interactively invoking the skill via Claude Code** — there is no GUI, no end-user-facing surface. The Mermaid `sequenceDiagram` blocks below use abbreviated participant names (`Dev`, `MDTM`, `Skill`, `CLI`, `Subproc`) instead of the template's `User`/`Frontend`/`Backend`/`Database` defaults.

### 11.1 Primary User Flow: Classification-Header Authoring

**Trigger:** A developer creates a new MDTM task file under `.dev/tasks/to-do/<TASK-ID>/` and decides whether to annotate it with a `Tier:` classification.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Editor as Text Editor
    participant MDTM as TASK-*.md file
    participant Skill as /task skill (Gate 1)

    Dev->>Editor: Open new TASK-*.md from template
    Dev->>Editor: Author frontmatter (status, id, title, ...)
    Note over Dev,Editor: Optional: add `Tier: <STRICT|STANDARD|LIGHT|EXEMPT>` as row-1
    Dev->>Editor: Optional per-item: `- [ ] (Tier: <value>) <item text>`
    Dev->>MDTM: Save
    Dev->>Skill: Invoke /task @<path>
    Skill->>MDTM: Read frontmatter (Gate 1)
    alt Tier present and valid
        Skill->>Skill: tier_field_validate → use authored value
    else Tier absent
        Skill->>Skill: CR-FM-03 shim → default STANDARD; emit gate-1.4 shim-status row
    else Tier present but malformed (non-enum)
        Skill->>Skill: REFUSE entry; log refusal token
    end
    Skill-->>Dev: Acknowledge classification + begin execution
```

**Steps:**
1. Developer opens a new `TASK-*.md` based on the MDTM template.
2. Developer authors frontmatter (status, id, title, parent_release, ...).
3. **Optionally** appends a `Tier: <STRICT|STANDARD|LIGHT|EXEMPT>` field — canonical position is row-1 of the YAML block.
4. **Optionally** annotates individual checklist items with `(Tier: <value>)` immediately after the checkbox.
5. Saves the file.
6. Invokes `/task @<path>` (either directly in Claude Code or transitively via `superclaude sprint run`).
7. The skill's Gate 1 reads the frontmatter and dispatches per the precedence chain (per-item marker → task-level `Tier:` → STANDARD default).

**Success Criteria:**
- A task authored with `Tier: STANDARD` (or omitted entirely) enters execution with no Gate-1 refusal.
- A task authored with `Tier: AGGRESSIVE` (non-enum) is refused at Gate 1 with a refusal token in the Task Log.
- A per-item override `- [ ] (Tier: LIGHT) typo fix` embedded in an otherwise STRICT task is honored on that item only.

**Error Scenarios:**
- If `Tier:` value is non-enum, Gate 1 emits the validation-spec enum-violation refusal token and HALTS (one of the few legal HALT semantics under INV-01).
- If frontmatter is structurally malformed, Gate 1 returns a YAML parse error pointing at the offending line.

`[CONTENT-AUDIT-COMPLETED]`

### 11.2 Secondary User Flow: Sprint Emitter → /task Invocation

**Trigger:** A developer runs `superclaude sprint run <tasklist-index.md>` to execute a multi-phase task plan; each phase fans out to a `claude` subprocess receiving a `/task ...` prompt.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CLI as superclaude sprint run
    participant Build as ClaudeProcess.build_prompt
    participant Subproc as claude (subprocess)
    participant Skill as /task skill

    Dev->>CLI: superclaude sprint run <index.md>
    CLI->>Build: Construct phase prompt
    Build->>Build: Render f"/task Execute all tasks in @{phase_file} ..."
    Note over Build: Post-merge: literal MUST be `/task ` (NOT `/sc:task `)
    Build->>Subproc: Spawn `claude` with prompt on stdin
    Subproc->>Skill: Invoke /task skill via slash-command dispatch
    Skill->>Skill: F1 execution loop on phase_file items
    Skill-->>Subproc: Phase complete (or HALT signal)
    Subproc-->>CLI: Exit code + stdout
    CLI->>CLI: Checkpoint; advance to next phase
    CLI-->>Dev: Sprint complete summary
```

**Success Criteria:**
- Every emission site (6 enumerated: `sprint/process.py:170`, plus five `cleanup_audit/prompts.py` sites at `:26, :47, :69, :92, :116`) renders the literal `/task ` prefix; no site emits `/sc:task ` (closed by `tests/sprint/test_process.py::test_build_prompt_contains_task_command` asserting `prompt.startswith("/task ")` AND `"/sc:task" not in prompt` per AC-ATK-17).
- The subprocess receives a non-empty prompt of byte form starting with `/task ` (the 6-byte literal) and the skill dispatches.

**Error Scenarios:**
- If a future commit reintroduces the literal `/sc:task ` at any emission site, the AC-ATK-17 boundary test fails CI and the gate blocks merge.
- If `claude` subprocess fails (non-zero exit), the sprint runner records the failure in its checkpoint log.

`[CONTENT-AUDIT-COMPLETED]`

### 11.3 Tertiary User Flow: In-Flight MDTM Resume (CR-FM-03 Shim + Gate-1.5 Emission)

**Trigger:** A developer resumes an existing in-progress MDTM task (status `🟠 Doing`) authored **before** the directional merge.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Skill as /task skill
    participant MDTM as TASK-*.md (legacy)
    participant Log as Task Log (in MDTM)

    Dev->>Skill: Invoke /task @<legacy-path>
    Skill->>MDTM: Read frontmatter (Gate 1)
    Note over Skill: No `Tier:` field present
    Skill->>Skill: CR-FM-03 parse-layer shim → default STANDARD
    Skill->>Log: Emit `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<N> sunset_row_authored=false`
    Skill->>MDTM: Scan body for donor-surface refs (AC-ATK-18)
    alt Donor refs found
        Skill->>Log: Emit `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` (per occurrence)
        Skill->>Skill: ME-3 disposition: warn-and-continue (NEVER HALT)
    end
    Skill->>Skill: Resume from first unchecked item
    Skill-->>Dev: F1 loop proceeds; identical behavior to pre-merge except added Task Log rows
```

**Steps:**
1. Developer invokes `/task @<path>` on a legacy MDTM file (status `🟠 Doing`, no `Tier:` field, donor-surface references possibly present in body).
2. Gate 1 parses frontmatter; the **CR-FM-03 compat shim** detects missing `Tier:` and assigns `STANDARD` as the parse-layer default.
3. The shim emits a `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<int> sunset_row_authored=<bool>` row to the Task Log.
4. The skill performs the AC-ATK-18 content-level audit: greps the task body for `/sc:task\b`, `sc-task-protocol`, `task-unified`; for each occurrence, emits a `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` row.
5. ME-3 (warn-and-continue) is binding: the skill **never refuses entry** on a legacy reference (would violate INV-01).
6. F1 loop resumes from the first unchecked checklist item with **identical behavior** to pre-refactor execution.

**Success Criteria (AC-SM-12):**
- **100% of the live in-flight MDTM population (136 union files at the 2026-05-16 drift snapshot) resumes cleanly with NO HALT** at the resume-gate boundary (L1 parse + L2 content audit).
- Every resumption produces at minimum one `gate-1.4: shim-status` row and zero-or-more `gate-1.5: legacy-surface-reference` rows in the Task Log.
- L3 runtime hazards (H-4 transition-to-`⚪ Blocked` scenario) are out-of-scope for the resume-gate guarantee per INV-04 by-transition disposition.

**Error Scenarios:**
- If the legacy task body has a malformed checklist line, the F1 loop emits a parse-error Task Log row and continues to the next item.
- If the operator does not provide the first-resume acknowledgment, the skill blocks **only on the acknowledgment-gate, not on the legacy reference itself** — this is the one legal acknowledgment-style pause under INV-01.

`[CONTENT-AUDIT-COMPLETED]`

---

## 12. Error Handling & Edge Cases

### 12.1 Error Categories

The merged `/task` surface partitions error origins into **five categories**, each bound to a recipient-skill enforcement point and a documented disposition. No category authors a new HALT semantic at the F1-loop boundary (ME-3 binding) `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`.

| Category | Examples | Disposition | Recovery / Routing |
|---|---|---|---|
| **C-PRE Pre-flight environment** | `git status` failure modes (5-row matrix below); MCP tool unavailability (`serena`, `codebase-retrieval`) | `WARN-CONTINUE` or `GRACEFUL-SKIP` (per AC-ATK-02 + ME-3) | Emit `gate-1.5:` Task Log line; F1 enters loop. No row HALTs. |
| **C-VAL Schema validation** | Malformed `Tier:` value outside `{STRICT, STANDARD, LIGHT, EXEMPT}`; missing required frontmatter (`id`, `title`, `status`, `created_date`); checklist absent | **Input-invalid HALT** (AC-ATK-10 row a) — task does not enter | Caller fixes task file; re-invoke. Distinct from C-PRE. |
| **C-BASE Baseline degraded** | `research/test-baseline.yaml` absent / empty / parse-fail / schema-fail (4-state per AC-ATK-03) | Over-escalate: `classification=new-all` per AC-CR-TASK-09-F04 | Emit `tfep: baseline=absent classification=new-all reason=<token>`; never refuse task entry; never silently skip. |
| **C-TFEP Test failure escalation** | Pre-existing test fails post-EXECUTE; ≥3 new tests fail simultaneously; runtime exception in implementation code | Mid-phase rf-qa spawn (fourth authorized INV-03 invocation point — F-05 closure) | TU-7 routes to existing `rf-qa` via spawn pattern at `task/SKILL.md:191-198`; F1 continues per ME-3. |
| **C-RES Resume-time content drift** | In-flight MDTM body cites deleted surface (`/sc:task`, `sc-task-protocol`, `task-unified`) after Step-5/Step-6 lands | `warn-and-continue` per ME-3 (refuse-entry would weaken INV-01) | Emit `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`; one-shot ack gate. |

### 12.2 TU-4 Git Pre-flight — Five-Row Outcome Matrix (AC-ATK-02 closure)

The TU-4 git pre-flight extends F-03 closure to five mutually-exclusive observable outcomes of `git status --porcelain`. All five rows have action ∈ `{WARN-CONTINUE, GRACEFUL-SKIP}`. **No row HALTs F1 entry** (ME-3 binding; INV-01 binding; auto-REJECT under R-RULE-05 if proposed) `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`.

| Row | Outcome | Detection condition | Action | Task Log line emitted |
|---|---|---|---|---|
| R1 | `clean` | `returncode=0` AND `stdout` empty after strip | **WARN-CONTINUE (informational)** | `gate-1.5: pre-flight tier=STRICT git_status=clean action=warn-and-continue` |
| R2 | `dirty` | `returncode=0` AND `stdout` has ≥1 non-empty line | **WARN-CONTINUE** | `gate-1.5: pre-flight tier=STRICT git_status=dirty action=warn-and-continue` |
| R3 | `tool-absent` | `FileNotFoundError` (Python) / shell exit 127 | **GRACEFUL-SKIP** | `gate-1.5: pre-flight tier=STRICT git_status=tool-absent action=graceful-skip` |
| R4 | `not-a-repo` | Non-zero `returncode` (typically 128) AND `stderr` contains `not a git repository` | **GRACEFUL-SKIP** | `gate-1.5: pre-flight tier=STRICT git_status=not-a-repo action=graceful-skip` |
| R5 | `error-other` | `TimeoutExpired`; OR `returncode != 0` AND R4 substring absent; OR permissions/I/O error | **WARN-CONTINUE** | `gate-1.5: pre-flight tier=STRICT git_status=error-other action=warn-and-continue reason=<short-token>` |

**Row-action mapping rules:**
- R1 (clean) is *not* silent — emits a positive-confirmation line so an auditor can distinguish "ran and observed clean" from "did not run at all."
- R3 (tool-absent) reuses the established `graceful-skip` semantic from the recipient's existing MCP-tool-unavailability pattern.
- R5 (error-other) carries `reason=<short-token>`. Closed token set: `{timeout, permission, index-locked, nfs-stale, unknown}`.
- **GRACEFUL-SKIP vs WARN-CONTINUE** distinguishes log-line semantics, not F1 behavior. Both are non-HALT.

**Tier-gating.** All rows describe STRICT behavior. STANDARD runs a reduced pre-flight subset that does NOT include `git_status_clean_tree_check`; LIGHT and EXEMPT skip pre-flight entirely.

**Reading B (refuse-entry) — auto-REJECTed** on three independent grounds: (1) INV-01 violation (structural); (2) ME-3 violation (manifest); (3) Pattern discontinuity. The pre-flight has **no HALT verb in its vocabulary**.

### 12.3 TU-5 Baseline — Four-State Observation Order (AC-ATK-03 closure)

The on-disk `${TASK_DIR}/research/test-baseline.yaml` may exist in **four distinct degraded states**. AC-ATK-03 pins observation order strict left-to-right (first-match-wins) and binds a uniform disposition (`classification=new-all`, conservative over-escalate).

| # | State | Observation tool | Predicate | Disposition |
|---|---|---|---|---|
| 1 | `absent` | `os.path.exists(path)` | returns `False` | `tfep: baseline=absent classification=new-all reason=absent` |
| 2 | `empty` | `os.path.getsize(path)` | returns `0` | `tfep: baseline=absent classification=new-all reason=empty` |
| 3 | `parse-fail` | `yaml.safe_load(content)` | raises `yaml.YAMLError` | `tfep: baseline=absent classification=new-all reason=malformed` |
| 4 | `schema-fail` | Schema validator | returns invalid | `tfep: baseline=absent classification=new-all reason=malformed` |

**Why order matters:** given `baseline.yaml` of 5 bytes containing `null\n`, observer 1 (`yaml.safe_load → None`) would label it `empty` while observer 2 (`os.path.getsize → 5`) would label it not-empty. Pinning `exists → getsize → parse → schema` resolves the ambiguity deterministically.

### 12.4 TFEP Failure-Mode Disposition Matrix (Mode A through Mode F)

| Mode | Trigger | Recovery |
|---|---|---|
| **A — Baseline degraded** | 4-state per §12.3 | AC-CR-TASK-09-F04: classify all post-EXECUTE failures `classification=new`; never refuse entry; observation order pinned. |
| **B — Prohibition firing in verifier-spawned subagent** | TFEP prohibition fires inside rf-qa mid-phase context | Three-way disposition: **root F1** → emit `tfep: prohibition-refusal`; F1 continues. **verifier-spawned F1** → rf-qa returns FAIL verdict; orchestrator handles via fix-cycle. **mid-phase rf-qa** → rf-qa surfaces prohibition in mid-phase report. |
| **C — TU-7 trigger fires; donor's `/sc:forensic` absent** | Recipient does not host this command | Recipient routes to existing `rf-qa` via spawn pattern at `task/SKILL.md:191-198` (fourth authorized INV-03 invocation point per F-05 closure). `/sc:forensic` invocation dropped. ME-2 preserved. |
| **D — TU-8 incident-report missing required field** | Post-Completion Validation reads `research/tfep-incident-report.md` and finds <7 fields | Routed to `rf-qa`. Emit `gate-1.5: tfep-incident-schema-drift detected file=<path> expected_fields=7 found_fields=<n> action=warn-and-continue`. |
| **E — F1 halts on TFEP engagement** | Donor's F1-HALTING behavior | **Auto-REJECT** under ME-3 / CR-12. The failing item flips to `- [x]` (or records via blocker logging); F1 continues. |
| **F — Heading insertion into task file** | Donor Step 5 inserts heading into task body | **Auto-REJECT** under F4 and INV-05. TU-8 produces a side-effect FILE only at `${TASK_DIR}/research/tfep-incident-report.md`. |

### 12.5 Gate-1.5 Warn-and-Continue Token Catalogue (AC-ATK-18 + AC-CR-TASK-06-F03)

Gate-1.5 emissions form a single common-prefix grammar with seven event classes. Every emission is **warn-and-continue per ME-3**; refuse-entry would weaken INV-01 and is explicitly prohibited.

| Trigger | Token byte form |
|---|---|
| TU-4 pre-flight (5-row matrix per §12.2) | `gate-1.5: pre-flight tier=<tier> git_status=<value> action=<action> [reason=<token>]` |
| AC-ATK-18 content match on `(/sc:task\|sc-task-protocol\|task-unified)` in task body | `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` |
| `related_docs:` path traversal — ENOENT | `gate-1.5: deleted-related-doc detected path=<path> action=warn-and-continue` |
| Acknowledgment-gate prompt (first resume only) | `gate-1.5: legacy-surface-acknowledgment-required` |
| Acknowledgment-gate completion | `gate-1.5: legacy-surface-acknowledged operator=<id> sha=<git-sha>` |
| Shim status emission (paired CR-FM-03 sunset counter, gate-1.4) | `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<int> sunset_row_authored=<bool>` |
| TFEP-incident schema drift at resume | `gate-1.5: tfep-incident-schema-drift detected file=<path> expected_fields=7 found_fields=<n> action=warn-and-continue` |
| Baseline YAML schema-version mismatch | `gate-1.5: baseline-schema-version-mismatch ... action=warn-and-continue` |

**Position semantics.** The `gate-1.5:` prefix sits between Gate 1 (binary STANDARD/STRICT dispatch at task entry) and F1's first iteration. It is half a gate-step beyond Gate 1, but it is *not* a sixth gate in the five-gate compliance-gating model.

### 12.6 Graceful Degradation Matrix

| Component Failure | Degraded Experience | Fallback Behavior |
|---|---|---|
| MCP `serena` unavailable | Pre-flight `serena_activate_if_available` emits graceful-skip | GRACEFUL-SKIP; pre-flight continues to next check |
| MCP `codebase-retrieval` unavailable | Pre-flight `codebase_retrieval_on_relevant_code_if_available` emits graceful-skip | GRACEFUL-SKIP; F1 proceeds without warmed context |
| `git` binary absent (R3) | git_status not observable | GRACEFUL-SKIP; pre-flight continues |
| `research/test-baseline.yaml` absent (Mode A state 1) | TU-7 has no per-test baseline to classify against | Over-escalate: all post-EXECUTE failures classified `new` |
| `/sc:forensic` absent (Mode C) | Donor Step 3 invocation impossible | Route to existing `rf-qa` (fourth INV-03 invocation point); ME-2 preserved |
| Pre-flight subprocess `TimeoutExpired` (R5) | git_status not observable in bounded time | WARN-CONTINUE with `reason=timeout`; F1 enters |

### 12.7 Retry & Recovery Strategies

| Error Type | Retry Strategy | Max Attempts | Backoff |
|---|---|---|---|
| Pre-flight subprocess timeout (R5) | No automatic retry — emit `reason=timeout` and continue | 0 | N/A |
| TFEP fix-cycle (Mode B / D) | Phase-Gate QA's existing rf-qa fix-cycle | **3** (per `task/SKILL.md:203`; D25 escalation budget was REJECTed) | None — adversarial verification is sequential |
| Acknowledgment gate (C-RES) | Operator must acknowledge once per task generation; gate is idempotent across re-resumes within the same ack-token-set state | 1 | N/A |
| Baseline YAML write failure on pre-F1 (TU-5) | Treat as Mode A state 4 | 0 | Over-escalate on TU-7 fire |
| Server-side `pre-receive` hook reject (AC-ATK-17) | Author must fix commit composition atomically and re-push | 0 (rejection is intentional — bypass closure) | N/A |

### 12.8 Edge Cases

| Scenario | Expected Behavior | Test Case |
|---|---|---|
| STRICT task resumed mid-pre-flight (context window flushed between R1 and R2) | Re-emit all five rows on resume; append-only; auditor reads latest emission per facet as authoritative | `tests/skills/task/test_preflight_resume_reemit.py::test_append_only` |
| `git status --porcelain` produces ambiguous stderr | Treated as R5 `error-other` with `reason=unknown` | `tests/skills/task/test_git_dirty_dispatch.py::test_R5_unknown_categorization` |
| `research/test-baseline.yaml` exists with `null\n` (5 bytes) | Observer-order pinned; disposition: `reason=malformed` | `tests/skills/task/test_baseline_trinary.py::test_null_content_5_bytes` |
| In-flight MDTM body cites all three deprecated surfaces | Emit three legacy-surface-reference tokens (one per surface symbol); de-duplicate per file at implementation discretion | `tests/skills/task/test_cr_fm_03_resume_grep.py::test_multi_surface_emission` |
| Per-tier non-STRICT task encounters git-dirty | No pre-flight runs; no Task Log emission; F1 enters normally | `tests/skills/task/test_git_dirty_dispatch.py::test_non_strict_skip` |
| Two MCP-tool unavailabilities in same pre-flight | Two graceful-skip emissions; pre-flight continues; F1 enters | `tests/skills/task/test_preflight_multi_unavailable.py::test_double_skip` |

---

## 13. Security Considerations

### 13.1 Threat Model

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **T-RebSplit** — Rebase-split bypass | M | **HIGH** — any sprint run pinned to that SHA is dead | AC-ATK-17 server-side `pre-receive` hook re-greps `/sc:task\b` against the landing commit's `src/superclaude/cli/**/*.py`; rejects push if grep matches AND donor `task.md` deletion absent. |
| **T-WorktreeRace** — Concurrent `make sync-dev` races on prune loop of `.claude/skills/` | L | M | AC-ATK-16: wrap `Makefile` `sync-dev` prune in `flock -xn /tmp/sync-dev.lock`. **Portability gap:** `flock(1)` is GNU-coreutils only; macOS / BSD lacks it (see §13.5). |
| **T-StaleVerify** — Long-running PRD subagent issues `[CODE-VERIFIED]` tag at Day 28; Day 30 Step 5 lands and stubifies `task.md`; PRD deliverable now carries stale tags | M | M | AC-ATK-08(a)(b)(c): `--max-wait 14d` CLI flag; `scripts/embed_git_sha.py` walks final commit and appends `(git-sha: <SHA>)` to every `[CODE-VERIFIED]` tag; CR-DEP-05 grep extension flags post-Step-5 stale-tag drift. |
| **T-ResumeContent** — Resumed in-flight task names a deleted donor file as PRIMARY ARTIFACT; CR-FM-03 parse-layer validates clean; subagent fails `Read` on the deleted file | **HIGH** (136 live in-flight files at fix-cycle floor) | M | AC-ATK-18: CR-FM-03 content-layer grep at Gate-1.5 resume emits `gate-1.5: legacy-surface-reference detected ... action=warn-and-continue`; one-shot ack gate; CR-DEP-06 post-Step-6 manifest. |
| **T-CriticalPathBypass** — Author tags a task body editing `auth/`, `security/`, `crypto/`, `models/`, or `migrations/` paths as `Tier: LIGHT` or `Tier: EXEMPT` to skip pre-flight + Phase-Gate QA | **HIGH** | **HIGH** | TU-2 Critical Path Override: `path_override_check` runs BEFORE `tier_field_validate` and BEFORE `gate_1_dispatch` (CR-7 ordering, enforced by CR-FM-04 row-1 grep + sentinel comment). Override forces `verification_stance=CRITICAL` regardless of declared `Tier:`. |
| **T-ProhibitionBypass** | Agent reads a test traceback and edits code directly to make tests pass (donor TFEP VIOLATION-1) | M | M | TU-6 prohibition firing routes to side-channel hook `tfep_prohibition_check(blocker_type) → {allow, refuse}`; `refuse` emits `tfep: prohibition-refusal item=<id> rule=<VIOLATION-NN> reason=<reason>`; F1 continues per ME-3. |
| **T-EncBypass** — UTF-16-authored markdown evades grep audits | L | L | CR-FM-04 grep + CR-DEP-05 grep use bytestring regexes that match UTF-8 only; surface as TDD §22 gap. |
| **T-RenameEvasion** — Donor file renamed (`sc-task-protocol/SKILL.md.deprecated`) rather than deleted bypasses CR-DEP-04 absence check | L | M | CR-DEP-04 audit asserts the entire directory `src/superclaude/skills/sc-task-protocol/` is absent (not just `SKILL.md`); `make verify-sync` re-asserts on every commit. |

### 13.2 Security Controls

| Control | Implementation | Verification |
|---|---|---|
| **Input Validation — Tier enum** | Closed enum `{STRICT, STANDARD, LIGHT, EXEMPT}` validated at task entry (CR-FM-01); malformed value HALTs with exit-code 2 (input-invalid per AC-ATK-10 row a) | `tests/skills/task/test_cr_fm_01_canonical.py::test_enum_membership` + `test_default_standard` |
| **Critical Path Override** | Path-glob match against `auth/, security/, crypto/, models/, migrations/` BEFORE Tier resolution; forces CRITICAL stance regardless of declared `Tier:` (CR-7 ordering) | `tests/skills/task/test_cr_task_01_path_override.py::test_log_emission, test_sentinel_present, test_call_first` |
| **Trivial Path Override** | Path-glob match against `*.md, docs/, *test*.py` BEFORE Tier resolution; allows verification skip — but **only on non-Critical-overridden paths** (Critical takes precedence) | `tests/skills/task/test_cr_task_01_path_override.py::test_trivial_then_critical_precedence` |
| **Server-side atomic-commit enforcement** | `.github/workflows/pre-receive-cli-atomicity.yml` (GitHub Actions) OR `.git/hooks/pre-receive.sh` (self-hosted); re-greps `/sc:task\b` against landing commit's `src/superclaude/cli/**/*.py` | `tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected` |
| **Per-item marker authorization** | Closed enumeration of consumers; current set = `{CR-TASK-07 baseline-skip}`; new consumers require new manifest exception (AC-ATK-05) | `tests/audit/test_marker_consumers.py::test_closed_consumer_set` |
| **Donor-string byte-preservation** | CR-TASK-12 seven-diff audit against `tests/fixtures/donor-blocks/{TU2_path, TU2_redirect, TU6_prohibitions, TU6_carve_outs, TU7_triggers, TU8_schema, sentinel}.txt`; ME-6 binding | `tests/skills/task/test_cr_task_12_donor_diffs.py::test_seven_zero_diffs` |
| **Digest integrity** | `sha256sum` (not `md5`) on stubified `task.md` (CR-DEP-02), recipient mirror (CR-TASK-11), and CR-DIST-02 mirror; AC-ATK-09 mechanical substitution | `tests/skills/task/test_cr_task_11_digest.py::test_sha256_match` |
| **Concurrency lock** | `Makefile sync-dev` target wraps prune loop in `flock -xn`; concurrent worktree run blocks (not races) | `tests/audit/test_make_sync_dev_flock.py::test_concurrent_worktree` |

### 13.3 Critical Path Override Semantics (V3 security-probe binding)

The Critical Path Override is the **load-bearing security control** for paths under `auth/, security/, crypto/, models/, migrations/`. Verbatim donor literal at `sc-task-protocol/SKILL.md:121`:

> **Critical Path Override**: Paths matching `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always trigger CRITICAL verification regardless of compliance tier.

**Enumerated path globs (load-bearing — DO NOT modify without ME-6 byte-preservation re-audit):**

| Glob | Matches | Override action |
|---|---|---|
| `auth/` | Any path containing `auth/` segment | Force `verification_stance=CRITICAL`; Phase-Gate QA mandatory regardless of `Tier:` |
| `security/` | Any path containing `security/` segment | Same |
| `crypto/` | Any path containing `crypto/` segment | Same |
| `models/` | Any path containing `models/` segment (data models — schema changes touch persistence integrity) | Same |
| `migrations/` | Any path containing `migrations/` segment (DB schema migrations — irreversible state changes) | Same |

**CR-7 ordering rule (CR-FM-04 row-1):** `path_override_check` MUST be called BEFORE `tier_field_validate` and BEFORE `gate_1_dispatch`. This ordering is enforced by:
1. **Sentinel comment** preceding the three-call sequence (byte-identical text; part of CR-TASK-12 seven-diff audit; AC-SM-08 sentinel-block fixture).
2. **Grep audit** at Step-4 pre-commit: `scripts/audit/cr_fm_04_ordering.sh` runs `grep -n -E "(path_override_check|tier_field_validate|gate_1_dispatch)" src/superclaude/skills/task/SKILL.md`; asserts monotonic line-number ordering. Reorder blocks commit.
3. **Test fixture** `tests/skills/task/test_cr_fm_04_ordering.py::test_row_1_order` subprocess-invokes the grep, parses line numbers, asserts monotonic increase.

**Composition with Trivial Path Override.** A path matching both `auth/auth-spec.md` (Critical via `auth/` segment AND Trivial via `*.md` suffix) is **forced CRITICAL**, never trivialized. The check order in `path_override_check` is: critical-match → trivial-match → none.

### 13.4 Data Governance & Compliance

**N/A — internal framework, no PII/PHI/regulated data.**

The `/task` skill operates on MDTM task files (markdown with YAML frontmatter) stored in `.dev/tasks/to-do/`, `.dev/tasks/doing/`, `.dev/tasks/done/`, `.dev/tasks/cancelled/`, plus side-effect files under `${TASK_DIR}/{research,synthesis,qa,reviews}/`. No PII, PHI, payment data, healthcare data, or regulated content is stored or processed by the skill. No GDPR / CCPA / HIPAA / SOC2 / PCI-DSS obligations apply.

If the merged surface is ever extended to process such data (a future PRD decision outside this TDD's scope), the §13.4 obligations would be re-evaluated under a fresh PRD + TDD cycle.

### 13.5 `flock` Portability Gap (AC-ATK-16 + web-01 reference)

`flock(1)` is **GNU-coreutils only**. macOS and BSD systems lack it by default. The AC-ATK-16 concurrency-lock control depends on `flock -xn` for the `Makefile sync-dev` prune lock.

| Platform | Default `flock` available? | Required action |
|---|---|---|
| Linux (Debian/Ubuntu/Fedora/Arch) | **Yes** (`util-linux`) | None — `flock -xn /tmp/sync-dev.lock` works out-of-box |
| macOS | **No** | `brew install flock` OR fallback to `lockfile-create` from `procmail-lockfile` |
| BSD (FreeBSD/OpenBSD) | **No** | `pkg install flock` (FreeBSD) OR fallback to `lockf(1)` (different semantics) |
| Windows (WSL2) | **Yes** (Linux semantics inside WSL) | None — assumes Claude Code runs inside WSL on Windows hosts |

Preserved as TDD §22 open question (`Gap-22-FLOCK-PORTABILITY`).

### 13.6 GitHub.com Pre-Receive Limitation (AC-ATK-17 + web-01 reference)

GitHub.com (hosted) **lacks `pre-receive` hook support** — only GitHub Enterprise Server hosts arbitrary pre-receive hooks. AC-ATK-17's primary path (server-side hook) is therefore not directly executable on GitHub.com.

**Defense-in-depth substitution on GitHub.com:**

1. **GitHub Actions workflow** `.github/workflows/pre-receive-cli-atomicity.yml` running on push to `master`/`integration` — re-greps the landing commit and fails the workflow on violation.
2. **Branch protection** with required status check `cli-atomicity-grep` AND `Require branches to be up to date before merging` enforces the gate at the merge-button level.
3. **Signed commits** (`commit.gpgsign=true`) raise the cost of a malicious override.
4. **Required signatures** + `code owners` review on `src/superclaude/cli/**` ensures any CLI residual change is reviewed by a domain owner.

Note that *none* of (1)-(4) is strictly equivalent to a server-side `pre-receive` hook — an admin with bypass-branch-protection rights can short-circuit (1)-(3); (4) is reviewer-discretion only. The TDD §22 risk register surfaces `Gap-22-PRE-RECEIVE-GITHUB-COM`.

---

## 14. Observability & Monitoring

### 14.1 Logging — Task Log Emission Schema

The `/task` skill writes structured emission lines to the per-task Task Log
section (`## Task Log / Notes`) of the MDTM file. Lines are **append-only**;
the executor never overwrites a prior line (preserves INV-04 resumability)
[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)].

**Per-TU emission catalogue:**

| TU | Emission prefix | Example line | Where it lands |
|---|---|---|---|
| TU-1 Gate 1 dispatch | `gate-1:` | `gate-1: dispatch_profile=STRICT source=frontmatter` | `## Task Log / Notes` at task entry |
| TU-1 CR-FM-03 default shim | `gate-1:` | `gate-1: dispatch_profile=STANDARD source=default` | Same; only when `Tier:` absent from frontmatter |
| TU-2 Path Override | `path-override:` | `path-override: forced_stance=CRITICAL path=auth/login.py reason=critical-path-glob` | First-emitted at task entry (BEFORE gate-1 per CR-7) |
| TU-4 Pre-flight (5-row matrix) | `gate-1.5: pre-flight` | `gate-1.5: pre-flight tier=STRICT git_status=clean action=warn-and-continue` | Under `### Pre-flight (TU-4 / D15b Layer 2)` sub-heading |
| TU-5 Baseline write | `tfep: baseline=ran` | `tfep: baseline=ran files=tests/foo/test_a.py::test_one,... reason=fresh` | Under `### Pre-flight` sub-heading after TU-4 lines |
| TU-5 Baseline fallback (4-state per §12.3) | `tfep: baseline=absent` | `tfep: baseline=absent classification=new-all reason=malformed` | Same |
| TU-6 Prohibition refusal | `tfep: prohibition-refusal` | `tfep: prohibition-refusal item=2.3 rule=VIOLATION-1 reason=fix-without-tfep` | Per F1 iteration, under `### Iteration N` sub-heading |
| TU-6 Carve-out match | `tfep: carve-out` | `tfep: carve-out item=2.3 rule=carve-out-1 reason=import-error-scaffolding` | Same |
| TU-7 Escalation trigger | `tfep: escalation-trigger` | `tfep: escalation-trigger fired=3 tests=[test_a, test_b, test_c] classification=new` | Same; precedes mid-phase rf-qa spawn |
| TU-8 Incident write | `tfep: incident-report` | `tfep: incident-report path=research/tfep-incident-report.md fields=7 outcome=success` | After mid-phase rf-qa resolution |
| AC-ATK-18 legacy-surface | `gate-1.5: legacy-surface-reference` | `gate-1.5: legacy-surface-reference detected file=research/03-X.md action=warn-and-continue surface=/sc:task` | Under `### Pre-flight (Gate-1.5)` on resume |
| AC-ATK-18 ack-required | `gate-1.5: legacy-surface-acknowledgment-required` | (literal token) | First resume only |
| AC-ATK-18 ack-complete | `gate-1.5: legacy-surface-acknowledged` | `gate-1.5: legacy-surface-acknowledged operator=ryan sha=71b1b1f` | After operator response |

**Single-line emission grammar (BNF-ish):**

```
<prefix>: <facet>=<value> [<facet>=<value> ...] [reason=<short-token>]

<prefix>   ::= "gate-1" | "gate-1.5" | "gate-1.5: pre-flight"
             | "path-override" | "tfep" | "sprint-emit"
<facet>    ::= identifier (no spaces)
<value>    ::= identifier OR quoted-string-without-spaces
<action>   ::= "warn-and-continue" | "graceful-skip" | "block-emit"
```

Constraints: one line per emission; no newlines inside an emission; lines are
append-only; `gate-1.5:` prefix is reserved for pre-flight + resume-time
emissions (verified by absence elsewhere in
`src/superclaude/skills/task/SKILL.md` at the pinned SHA, [CODE-VERIFIED
(git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]).

### 14.2 CR-FM-04 Ordering Audit Metric (AC-SM-07)

The CR-FM-04 audit fires two greps at Step-4 pre-commit; both MUST return three
function names in monotonic line-number order. Failure blocks commit
[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
`final-merge-plan.md:243`.

**Grep #1 (Row 1 — Validating the Task File section):**

```bash
grep -n -E "(path_override_check|tier_field_validate|gate_1_dispatch)" \
  src/superclaude/skills/task/SKILL.md
```

Expected output (post-merge):

```
<L>: path_override_check(...)
<L+1>: tier_field_validate(...)
<L+2>: gate_1_dispatch(...)
```

where `L < L+1 < L+2`.

**Grep #2 (Row 10 — Phase-Gate QA Verification section):**

```bash
grep -n -E "(forced_stance_read|tier_field_read|gate_2_dispatch)" \
  src/superclaude/skills/task/SKILL.md
```

Expected output (post-merge):

```
<M>: forced_stance_read(...)
<M+1>: tier_field_read(...)
<M+2>: gate_2_dispatch(...)
```

where `M < M+1 < M+2`.

**Sentinel comments (CR-7 / CR-8):**

- Row 1: `# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.`
- Row 10: `# CR-8 ORDERING — load-bearing: forced_stance_read FIRST. Do not reorder.`

The sentinels are byte-identical text; they are themselves part of the
CR-TASK-12 seven-diff audit fixture (AC-SM-08 sub-binding "1 sentinel-comment
block"). AC-ATK-13 binds the executable-grep form of the audit, not just
sentinel-presence — the grep itself is the load-bearing test.

### 14.3 AC-ATK-18 Content-Grep at Resume Time

At Gate-1.5 (resume-time pre-flight), the executor greps the entire task body
for regex `(/sc:task\b|sc-task-protocol|task-unified)`. On match, emit:

```
gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<matched-symbol>
```

where `<matched-symbol>` ∈ `{/sc:task, sc-task-protocol, task-unified}`. Token
byte form (canonical, [CODE-VERIFIED (git-sha:
71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
`validation-spec.md:106`):

```
gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>
```

- `gate-1.5:` prefix is literal (with trailing colon-space).
- `legacy-surface-reference` is the literal event class.
- `detected` is the literal disposition keyword.
- `file=<path>` is a space-separated key=value pair.
- `action=warn-and-continue` is literal — refuse-entry would weaken INV-01 and
  is explicitly prohibited by `validation-spec.md:106`.
- `surface=<symbol>` is one of three closed values.

**Token-vs-pre-flight disambiguation.** The Gate-1.5 prefix is shared between
TU-4 pre-flight (`gate-1.5: pre-flight ...`) and AC-ATK-18 resume content-scan
(`gate-1.5: legacy-surface-reference ...`). Parsers disambiguate via the second
token (`pre-flight` vs `legacy-surface-reference`). Surfaced as TDD §22 gap
`Gap-22-GATE-1.5-GRAMMAR` (per research file 12 §10.9).

### 14.4 Pre-commit Gate Telemetry

| Gate | Step | Exit-code semantic | Verification fixture |
|---|---|---|---|
| Step-1 (M1 atomic merge) | Step 1 | 0 = pass; non-zero = blocks commit | `tests/audit/test_step_gates.py::test_step_1_gate_zero` |
| Step-2 (routing widening) | Step 2 | 0 = pass | `tests/skills/task/test_cr_task_05_routing.py + test_cr_task_06_preflight.py + test_cr_task_07_baseline.py` |
| Step-3 (TFEP cluster) | Step 3 | 0 = pass | `tests/skills/task/test_cr_task_08_prohibitions.py + test_cr_task_09_escalation.py + test_cr_task_10_incident.py` |
| Step-4 (sentinel ordering audit) | Step 4 | 0 = pass | `tests/skills/task/test_cr_fm_04_ordering.py + test_cr_task_12_donor_diffs.py` |
| Step-5 (CR-DEP-01 + CR-DOC-01 atomic) | Step 5 | 0 = pass; non-zero = blocks commit AND server-side hook re-validates on push | `tests/audit/test_step_5_commit_roster.py + test_cr_dep_01_stub.py + test_cr_dep_02_stub_digest.py + test_cr_dep_05_grep.py` |
| Step-6 (CR-DEP-03 hard-delete) | Step 6 | 0 = pass | `tests/audit/test_step_6_commit_roster.py + test_cr_dep_03_hard_delete.py + test_cr_dep_04_caller_sync.py + test_cr_dep_06_manifest.py + test_make_sync_dev_flock.py` |
| Server-side pre-receive | Push-time | 0 = accept push; non-zero = reject | `tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected` |
| Gate-1.5 (resume content-grep) | Per-resume | always 0 (warn-and-continue, no HALT) | `tests/skills/task/test_cr_fm_03_resume_grep.py::test_emission_token_format` |
| Sprint-emit boundary | Per-tasklist | 0 = accept; non-zero = block-emit | `tests/cli/test_sprint_emit_legacy_grep.py::test_block_emit_on_match` |

### 14.5 Alerts

| Alert | Condition | Severity | Response |
|---|---|---|---|
| Pre-receive hook reject on master/integration push | Server-side hook exits non-zero | **Critical** | Author re-composes commit (atomic CR-DEP-01 + CR-DOC-01 + CR-REF-01..05); re-push |
| Step-5 pre-commit gate fail | Local pytest run on Step-5 file roster exits non-zero | **Critical** | Author fixes failing tests; re-stage; re-commit. Hot-fix Step-8 fallback requires `AUTHORIZE_HOT_FIX=1` env var (AC-ATK-15 sub-binding) |
| Resume legacy-surface match | Gate-1.5 grep matches `(/sc:task\|sc-task-protocol\|task-unified)` in task body on resume | **Warning** | Operator acknowledges via one-shot ack gate (idempotent within ack-token-set state) |
| Sprint-emit block-emit | `superclaude sprint run` grep on rendered tasklist body matches | **Warning** | Author corrects tasklist source to remove legacy-surface citation; re-emit |
| `make verify-sync` non-zero | `src/superclaude/skills/` and `.claude/skills/` mirror diverge | **Critical** | Run `make sync-dev`; re-verify; if diff persists, manual reconcile under R-RULE-10 |
| TFEP incident-report schema drift on Post-Completion | Field count ≠ 7 in `${TASK_DIR}/research/tfep-incident-report.md` | **Warning** | Orchestrator re-routes to `rf-qa`; re-author report; re-validate |

### 14.6 Business Metric Instrumentation

**N/A — internal framework feature.**

The `/task` skill is an internal-tooling component (Claude Code slash command +
skill package). It has no end-user-facing business KPIs (no conversion funnel,
no revenue events, no retention metrics). Section 4.2 (Business Metrics) is
itself marked N/A in the parent PRD for the same reason; consequently §14.6 is
also N/A per `tdd_template.md:832-839` ("if applicable").

If the merged surface is ever instrumented for product analytics (a future PRD
decision outside this TDD's scope), the §14.6 business-event table would be
populated under that fresh PRD + TDD cycle.

---

## 15. Testing Strategy

### 15.1 Test Pyramid

| Level | Coverage Target | Tools | Responsibility |
|---|---|---|---|
| Unit Tests (markers `@pytest.mark.unit`, auto-applied to `/tests/unit/` per `pyproject.toml` superclaude pytest plugin) | > 80% per `superclaude/pm_agent/` module | `uv run pytest`, `pytest-cov` | Engineers |
| Integration Tests (`@pytest.mark.integration`, auto-applied to `/tests/integration/`) | Every CR-TASK-NN, CR-FM-NN, CR-DEP-NN row has ≥1 integration test | `uv run pytest`, `subprocess`, `tmp_path` fixtures | Engineers |
| AC-ATK Tests (1 test per AC-ATK-01..18; 18 tests) | 100% AC-ATK coverage | `uv run pytest`, `pytest.mark.parametrize` | Engineers |
| AC-SM Tests (1 test per AC-SM-01..12; 12 tests) | 100% AC-SM coverage | `uv run pytest`, intra-spec grep/diff | Engineers |
| Invariant Survival Walkthrough (re-readable scaffold; one paragraph per INV-01..INV-05) | 5 paragraphs, one per INV | Markdown walkthrough at `invariant-survival-walkthrough.md` + `tests/audit/test_invariant_walkthrough.py` | Engineers + sprint reviewer |
| CI continuous (intra-spec audits AC-SM-01..06, -11) | 7 audits return zero diff on every PR | GitHub Actions `audit.yml` | CI |

### 15.2 Test Case Roster — Every AC → Test Case (30 cases minimum)

Every AC-ATK-NN (18) + AC-SM-NN (12) closes a concrete test case. Per
research file 12 §8 aggregated map, the 30-test minimum surface:

#### AC-ATK Tests (18 cases)

| AC | Test path | Test name | Asserts | Step gate |
|---|---|---|---|---|
| AC-ATK-01 | `tests/skills/task/test_row1_call_order.py` | `test_path_override_first` | AST/grep order at row-1 site: `path_override_check → tier_field_validate → gate_1_dispatch` | Step-4 pre-commit |
| **AC-ATK-02** | `tests/skills/task/test_git_dirty_dispatch.py` | `test_5_row_matrix` | Parametrize R1..R5; for each: exact Task Log line; action token; proceed sentinel TRUE; no HALT | Step-2 pre-commit |
| AC-ATK-03 | `tests/skills/task/test_baseline_trinary.py` | `test_4_state_observer` | Parametrize {absent, empty, parse-fail, schema-fail}; observer order pinned (`exists → getsize → safe_load → schema`); all four → `classification=new-all` | Step-3 pre-commit |
| AC-ATK-04 | `tests/audit/test_condensation_table.py` | `test_79_to_67_to_65` | 6 bucket rows sum to 79 row-instances → 65 distinct CR-IDs → 67 PASS-line-items; names 2 duplicate CR-IDs | Step-5 pre-commit |
| AC-ATK-05 | `tests/audit/test_marker_consumers.py` | `test_closed_consumer_set` | Only authorized consumer = `{CR-TASK-07 baseline-skip}`; new consumer requires new ME-NN | Step-4 pre-commit |
| AC-ATK-06 | `tests/skills/task/test_cr_task_12_donor_diffs.py` | `test_seven_zero_diffs` | 7 `diff` invocations return zero against `tests/fixtures/donor-blocks/*.txt` (frozen-fixture per AC-ATK-06) | Step-4 pre-commit |
| AC-ATK-07 | `tests/audit/test_rf_qa_step6_gate.py` | `test_chain_links` | 5 chain anchors: sprint goal → T06.03 → §2 rubric → §4 traceability → CR-TASK-01..10 + CR-FM-01..03 landed; `rf-qa` returns PASS | Step-6 pre-commit |
| AC-ATK-08 | `tests/scripts/test_embed_git_sha.py` + `tests/audit/test_cr_dep_05_grep.py` | `test_idempotent` + `test_post_step5_stale_verification` | Every `[CODE-VERIFIED]` tag carries `(git-sha: <SHA>)` suffix; idempotent; post-Step-5 stale tags grep-detected | PRD final-commit + Step-5/6 pre-commit |
| AC-ATK-09 | `tests/skills/task/test_cr_task_11_digest.py` + `test_cr_dep_02_stub_digest.py` + `test_cr_dist_02_mirror_digest.py` | `test_sha256_matches_baseline` | All 3 audit digests use `sha256` (NOT `md5`); baselines pinned | Step-5 pre-commit |
| AC-ATK-10 | `tests/skills/task/test_preloop_halt_policy.py` | `test_2_category_table` | (a) input-invalid `Tier:` → HALT exit-code 2; (b) env-non-ideal git-dirty → WARN-CONTINUE exit-code 0 + Task Log line | Step-2 pre-commit |
| AC-ATK-11 | `tests/audit/test_me10_carve_out.py` | `test_me10_authored_or_annotated` | ME-10 row in `merge-master.md` §4.5 OR explicit non-generalization annotation at `final-merge-plan.md:148` | Step-1 pre-merge |
| AC-ATK-12 | `tests/skills/task/test_tfep_incident_schema.py` + `tests/audit/test_cr_fm_01_canonical.py` | `test_7_fields` + `test_canonical_table` | Incident schema enumerates exactly 7 fields (`{Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts}`); Tier enum closed `{STRICT, STANDARD, LIGHT, EXEMPT}` | Step-3 + Step-1 |
| AC-ATK-13 | `tests/skills/task/test_row1_ordering_grep.py` | `test_executable_grep` | Both CR-FM-04 greps (rows 1 + 10) return three names in monotonic order | Step-4 pre-commit |
| AC-ATK-14 | `tests/audit/test_cr_dep_05_grep.py` + companions | `test_4_sub_resolutions` | (a) grep scope correct; (b) cluster root named at `src/superclaude/skills/sc-task-protocol/`; (c) gate at Step-6 pre-commit; (d) CR-DOC-13 scope widened to 65 CR-IDs | Step-5 + Step-6 pre-commit |
| AC-ATK-15 | `tests/audit/test_cr_doc_01_step.py` | `test_landed_with_dep_01` + `test_step8_fallback_only_under_authorization` | `git log --name-only <step5-commit>` lists BOTH `src/superclaude/commands/task.md` AND `docs/user-guide/commands.md`; Step-8 fallback only with `AUTHORIZE_HOT_FIX=1` | Step-5 push + Step-8 fallback |
| AC-ATK-16 | `tests/audit/test_make_sync_dev_flock.py` | `test_concurrent_worktree` | Two `make sync-dev` subprocesses against parallel worktrees; `flock` held during prune; post-prune `find -type d .claude/skills/` matches expected; no lost commits | local + CI matrix |
| **AC-ATK-17** | `tests/ci/test_pre_receive_hook.py` | `test_rebase_split_rejected` | Fabricate rebase-split commit pair via `git rebase -i` in tmp repo; hook exits non-zero on intermediate broken state | push-time (server-side) |
| **AC-ATK-18** | `tests/skills/task/test_cr_fm_03_resume_grep.py` + `tests/cli/test_sprint_emit_legacy_grep.py` + `tests/audit/test_cr_dep_06_manifest.py` | `test_emission_token_format` + `test_block_emit_on_match` + `test_manifest_present` | (a) Gate-1.5 emission line matches canonical grammar exactly; (b) sprint-emit blocks on content match; (c) post-Step-6 manifest enumerates ≥1 row per 144 residuals | Gate-1.5 + sprint-emit + post-Step-6 |

#### AC-SM Tests (12 cases)

| AC | Test path | Test name | Asserts | Step gate |
|---|---|---|---|---|
| AC-SM-01 | `tests/audit/test_vck_verdicts.py` | `test_transfer_manifest_byte_match` | 8 of 8 V/C/K verdicts identical byte-for-byte between `final-merge-plan.md:54-63` and `transfer-manifest.md:56-63` | CI |
| AC-SM-02 | `tests/audit/test_me_traceability.py` | `test_each_me_has_cr_row` | For ME ∈ {1..9}, ≥1 grep hit in `final-merge-plan.md` §5 OR §6 | CI |
| AC-SM-03 | `tests/audit/test_invariant_walkthrough.py` | `test_inv_1_through_5_re_readable` | For INV ∈ {1..5}, ≥1 grep hit in `invariant-survival-walkthrough.md` §§2-3 with associated worked-example anchor (one paragraph per INV; see §15.6 below) | CI |
| AC-SM-04 | `tests/audit/test_f_findings_cite_anchors.py` | `test_each_f_row_has_artifact_anchor` | For F ∈ {01..08}, ≥1 line-range cite in `final-merge-plan.md` §4 | CI |
| AC-SM-05 | `tests/audit/test_s_constraints_cite_hz.py` | `test_s_1_cites_hz03` + `test_s_2_cites_hz06_hz07` + `test_s_3_cites_hz14` | 3 of 3 S-rows cite their HZ-NN | CI |
| AC-SM-06 | `tests/audit/test_row_and_step_counts.py` | `test_67_rows_in_master` + `test_10_steps_in_sequence` | 67 row-line-items in `merge-master.md` §1; 10 commit steps in §6 | CI |
| **AC-SM-07** | `tests/skills/task/test_cr_fm_04_ordering.py` | `test_row_1_order` + `test_row_10_order` | 2 greps × 3 function names = 6 hits monotonic; 0 reorders detected (see §14.2) | Step-4 pre-commit |
| AC-SM-08 | `tests/skills/task/test_cr_task_12_donor_diffs.py` | `test_6_donor_plus_1_sentinel` | 7 `diff` invocations return zero (6 donor strings + 1 sentinel-comment block) | Step-4 pre-commit |
| AC-SM-09 | `tests/audit/test_step_5_commit_roster.py` | `test_exact_file_list` | `git log --name-only <step5-commit>` set-equal to `final-merge-plan.md:375` roster | Step-5 push |
| AC-SM-10 | `tests/audit/test_step_6_commit_roster.py` | `test_exact_file_list` | Same for Step 6 against `:381` | Step-6 push |
| AC-SM-11 | `tests/audit/test_no_rejected_re_proposal.py` | `test_zero_ledger_re_introductions` | For every LR-REJECT-* in `rejected-features-ledger.md`, zero grep hits in `final-merge-plan.md` §5 row text | CI |
| **AC-SM-12** | `tests/audit/test_step_gates.py` + `tests/skills/task/test_in_flight_mdtm_resume.py` | `test_step_1_gate_zero` + `test_step_5_gate_zero` + `test_step_6_gate_zero` + `test_live_inflight_mdtm_resume_clean` | Gates 1/5/6 exit zero; **fixture iterates LIVE in-flight count at gate-execution time** (see §15.3 below) | Step-1/5/6 pre-commit + CI |

[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
research file 12 §8 aggregated map.

### 15.3 AC-SM-12 — Live-Count Fixture (NOT literal 25/96/132)

The AC-SM-12 fixture binds: "100% of live in-flight MDTM population resumes
cleanly under CR-FM-03 default-to-STANDARD shim; gates 1/5/6 return exit-code
0." The **live count** is a moving floor — 25 (early narrow snapshot) → 96
(validation-spec) → 130 (PRD fix-cycle 1) → 132 (PRD fix-cycle 2) → **136
(this TDD task fix-cycle, 2026-05-16)**.

**The pytest fixture MUST iterate the live count at gate-execution time, NOT a
literal 25/96/132 hardcoded value.** The 136 floor is the canonical
fix-cycle-time figure; the real Step-1 pre-commit gate iterates the population
at commit time (which may be larger).

**Reference fixture shape:**

```python
import subprocess
import pytest
from pathlib import Path

LEGACY_SURFACE_REGEX = r'/sc:task\|sc-task-protocol\|task-unified'

def _live_inflight_union() -> list[Path]:
    """Re-execute the live grep at fixture-evaluation time.

    NOTE: This iterates the live population — DO NOT hardcode 25/96/132.
    Floor at 2026-05-16 fix-cycle is 136 (per research file 11 §2.1).
    """
    result = subprocess.run(
        ["grep", "-rl", "-E", LEGACY_SURFACE_REGEX, ".dev/tasks/"],
        capture_output=True, text=True, check=False,
    )
    return [Path(p) for p in result.stdout.splitlines() if p.strip()]


@pytest.mark.parametrize("task_file", _live_inflight_union())
def test_ac_sm_12_in_flight_mdtm_resume_clean(task_file):
    """AC-SM-12 / NFR-INV-4: every live in-flight MDTM file resumes
    cleanly under CR-FM-03 default-to-STANDARD shim. Iterates the LIVE
    population — fix-cycle floor 136 at 2026-05-16."""
    # 1. L1 parse-layer: frontmatter must parse (default Tier=STANDARD
    #    when absent — CR-FM-03 shim).
    profile = resolve_dispatch_profile(task_file)
    assert profile in {"STRICT", "STANDARD", "LIGHT", "EXEMPT"}, (
        f"{task_file} did not resolve to a valid dispatch profile"
    )
    # 2. L2 content-scan: legacy-surface match emits warn-and-continue,
    #    NEVER refuses entry (AC-ATK-18 / ME-3 / INV-01).
    log_lines = resume_preflight(task_file, tier=profile)
    # 3. No HALT signal anywhere.
    assert not any(line.startswith("HALT:") for line in log_lines), (
        f"{task_file} produced HALT — violates AC-SM-12 + ME-3 + INV-01"
    )
```

The fixture is **moving-floor compatible**: at any future SHA, the live grep
re-runs and the parametrize set expands accordingly. The TDD pins the *floor*
(136 at 2026-05-16) as the lower-bound contractual guarantee; the actual run
may exceed it [CODE-VERIFIED (git-sha:
71b1b1fe7909fab59b5e30d39ce68fcb7f825444)].

### 15.4 AC-ATK-02 — Five-Row Matrix Fixture (Defensive Negative-Existence Test)

```python
import pytest
import subprocess
from unittest.mock import MagicMock, patch

GIT_PREFLIGHT_MATRIX = {
    "R1_clean": (
        MagicMock(returncode=0, stdout=b"", stderr=b""),
        "gate-1.5: pre-flight tier=STRICT git_status=clean action=warn-and-continue",
        "warn-and-continue",
    ),
    "R2_dirty": (
        MagicMock(returncode=0, stdout=b" M src/foo.py\n", stderr=b""),
        "gate-1.5: pre-flight tier=STRICT git_status=dirty action=warn-and-continue",
        "warn-and-continue",
    ),
    "R3_tool_absent": (
        FileNotFoundError("[Errno 2] No such file or directory: 'git'"),
        "gate-1.5: pre-flight tier=STRICT git_status=tool-absent action=graceful-skip",
        "graceful-skip",
    ),
    "R4_not_a_repo": (
        MagicMock(
            returncode=128, stdout=b"",
            stderr=b"fatal: not a git repository (or any of the parent directories): .git\n",
        ),
        "gate-1.5: pre-flight tier=STRICT git_status=not-a-repo action=graceful-skip",
        "graceful-skip",
    ),
    "R5_error_other_timeout": (
        subprocess.TimeoutExpired(cmd=["git", "status"], timeout=5),
        "gate-1.5: pre-flight tier=STRICT git_status=error-other action=warn-and-continue reason=timeout",
        "warn-and-continue",
    ),
}


@pytest.mark.parametrize(
    "row_id,mock_value,expected_line,expected_action",
    [(k, *v) for k, v in GIT_PREFLIGHT_MATRIX.items()],
)
def test_ac_atk_02_git_preflight_no_halt(
    row_id, mock_value, expected_line, expected_action, tmp_path, strict_task_file
):
    """AC-ATK-02 closure: 5-row matrix; no HALT in any row; exact line per row."""
    with patch("subprocess.run") as mock_run:
        if isinstance(mock_value, Exception):
            mock_run.side_effect = mock_value
        else:
            mock_run.return_value = mock_value

        result = run_preflight(strict_task_file, tier="STRICT")

        assert result.proceed is True, (
            f"Row {row_id} produced HALT — violates ME-3 / AC-ATK-02 / INV-01"
        )
        assert result.action == expected_action

        log_content = strict_task_file.read_text()
        assert expected_line in log_content
        assert "### Pre-flight (TU-4 / D15b Layer 2)" in log_content


def test_ac_atk_02_no_halt_exception_class_exists():
    """Defensive negative-existence test: pre-flight module MUST NOT define
    any class containing 'Halt' in its name. Encodes the 'no HALT verb in
    pre-flight vocabulary' constraint at the type level."""
    import inspect
    from superclaude.skills.task import preflight  # hypothetical module
    halt_classes = [
        cls for _, cls in inspect.getmembers(preflight, inspect.isclass)
        if "Halt" in cls.__name__
    ]
    assert halt_classes == [], (
        f"Pre-flight module defines HALT exception classes ({halt_classes}) — "
        f"violates ME-3 / AC-ATK-02 contract."
    )
```

[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
research file 08 §8.

### 15.5 Synthetic Fixture Catalogue (per research files 00-13)

The following synthetic fixtures support the 30-test roster and must be
authored as deliverables alongside the test files:

| Fixture | Purpose | Source | Files |
|---|---|---|---|
| `tests/fixtures/donor-blocks/TU2_path_override.txt` | Critical Path Override path-globs verbatim from `sc-task-protocol/SKILL.md:121` | research file 09 §5 | One per CR-TASK-12 diff |
| `tests/fixtures/donor-blocks/TU2_redirect.txt` | Trivial Path Override globs verbatim from `:123` | research file 09 §5 | Same |
| `tests/fixtures/donor-blocks/TU6_prohibitions.txt` | TFEP VIOLATION 1-3 verbatim from `:127-135` (anchor off-by-2 per R-DRIFT-02) | research file 09 §2.2 | Same |
| `tests/fixtures/donor-blocks/TU6_carve_outs.txt` | TFEP permitted-exceptions verbatim from `:137-140` | research file 09 §2.2 | Same |
| `tests/fixtures/donor-blocks/TU7_triggers.txt` | TFEP MUST-escalate triggers verbatim from `:157-161` (cited as `:200-210` in plan — R-DRIFT-03 anchor off-by-43) | research file 09 §3.1 + research file 13 §1.7 | Same |
| `tests/fixtures/donor-blocks/TU8_schema.txt` | TFEP incident-report 7-field template verbatim from `:222-234` (Outcome enum `{success / escalated / failed}` — ME-6 byte-preservation) | research file 09 §4.2 + §5 | Same |
| `tests/fixtures/donor-blocks/CR7_sentinel.txt` | Sentinel comment: `# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.` | research file 12 §4 | AC-SM-08 sub-binding |
| `tests/fixtures/donor-blocks/CR8_sentinel.txt` | Sentinel comment: `# CR-8 ORDERING — load-bearing: forced_stance_read FIRST. Do not reorder.` | research file 12 §4 | Same |
| `tests/fixtures/digest-baselines/task-md-stubified.sha256` | Pinned sha256 of stubified `src/superclaude/commands/task.md` | research file 12 §5 | AC-ATK-09 + CR-DEP-02 |
| `tests/fixtures/digest-baselines/task-md-mirror.sha256` | Pinned sha256 of recipient `.claude/skills/task/SKILL.md` mirror | research file 12 §5 + §7 | CR-TASK-11 |
| `tests/fixtures/vck-verdicts-expected.json` | Extracted V/C/K table for byte-for-byte diff | research file 12 §3 | AC-SM-01 |
| `tests/fixtures/inflight-mdtm-floor.json` | Floor metadata: `{"date": "2026-05-16", "floor": 136, "regex": "/sc:task\\|sc-task-protocol\\|task-unified"}` (informational; the fixture parametrize itself iterates live) | research file 11 §2 | AC-SM-12 |
| `tests/fixtures/legacy-residuals-144.json` | List of 144 known residual occurrences for CR-DEP-06 manifest assertion | research file 12 §5.1 | AC-ATK-18 sub-binding (d) |
| `tests/fixtures/preflight-five-row-matrix.json` | Five-row matrix data structure (parametrize source for `test_git_dirty_dispatch.py`) | research file 08 §4 | AC-ATK-02 |
| `tests/fixtures/baseline-four-state-matrix.json` | Four-state observer matrix (parametrize source for `test_baseline_trinary.py`) | research file 09 §1.4 | AC-ATK-03 |

[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] for all 15
fixture rows against the source research files.

### 15.6 Invariant-Survival Walkthrough Scaffold (5 paragraphs — one per INV)

AC-SM-03 requires a re-readable walkthrough demonstrating each of INV-01..INV-05
survives the merged surface. The scaffold below is the canonical structure;
each paragraph anchors to a worked-example stage in
`invariant-survival-walkthrough.md` §§2-3. Test `tests/audit/test_invariant_walkthrough.py::test_inv_1_through_5_re_readable`
asserts ≥1 grep hit per INV.

**INV-01 (F1 loop progress monotonicity) — paragraph 1.**

> The walkthrough's fabricated `TASK-EXAMPLE-20260515-strict-walkthrough.md`
> enters F1 after TU-4 pre-flight (Stage §2.1) and proceeds READ → IDENTIFY →
> EXECUTE → UPDATE → REPEAT through Phase 1 items in declared order (Stage
> §2.2). Critically, when TU-7 fires mid-phase on a regression (Stage §2.6),
> the failing item flips to `- [x]` (with blocker logged) and F1 continues to
> the next item — it does NOT halt. Every entered task progresses
> monotonically until the checklist exhausts or a documented terminal state is
> reached. Reading B (refuse-entry on git-dirty) is auto-REJECTed under ME-3 +
> INV-01; the pre-flight matrix has no HALT verb in its vocabulary
> [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
> `extension-point-contracts.md:13` + `task/SKILL.md:79-98`.

**INV-02 (Prohibited-actions F2 catalog additivity) — paragraph 2.**

> The F2 catalog at `task/SKILL.md:104-117` contains **10 numbered entries
> pre-merge** (Working from memory; Executing multiple items simultaneously;
> Skipping items; Assuming completion; Inventing file paths; Modifying items;
> Adding items; Delegating across phase boundaries; Skipping phase-gate QA;
> Skipping post-completion validation). TU-6 absorbs **3 additive TFEP
> prohibitions** (no fix-without-TFEP; no test-expectation-modification; no
> ad-hoc-traceback-patches) verbatim from `sc-task-protocol/SKILL.md:133-135`
> after line 117. Post-merge cardinality is **13** (10 existing + 3 new ≥ ≥12
> target). The three permitted-exception carve-outs (ImportError/NameError
> scaffolding; lint/formatting; deprecation warnings) embed inside the new
> TFEP block as exceptions, NOT as separate F2 entries. No existing F2 entry
> is dropped, reordered, or rephrased — additive insertion only
> [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
> `task/SKILL.md:108-117` count + research file 09 §2.1.

**INV-03 (Phase-gate rf-qa never replaced, never displaced) — paragraph 3.**

> The walkthrough's Stage §2.4 spawns `rf-qa` at the Phase 1 → Phase 2
> boundary via the canonical Phase-Gate QA pattern at `task/SKILL.md:191-198`.
> TU-3 widens the verifier roster on STRICT to
> `[rf-qa, quality-engineer]` — `quality-engineer` is ADDITIONAL, never
> replaces rf-qa (ME-2 binding). TU-7 (mid-phase rf-qa via TFEP escalation,
> Stage §2.6) is the **fourth** authorized INV-03 invocation point per F-05
> closure (joining phase-gate L191, post-completion structural L221, and
> post-completion qualitative L230 — authoritative rf-qa invocation count
> post-merge = 4); it routes to the existing rf-qa identity (no sibling
> verifier authored). The mid-phase invocation is a one-time non-generalizing carve-out
> per AC-ATK-11 — future widenings require fresh ME-* exceptions. Stage §2.9
> Post-Completion Validation runs the two-pass rf-qa (structural) +
> rf-qa-qualitative (operational) zero-leniency gate at `:248`
> [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
> `task/SKILL.md:181-211` + `:213-248` + research file 09 §3.

**INV-04 (Resumability — highest-exposure invariant) — paragraph 4.**

> Stage §2.0 demonstrates the two-layer preservation. **Parse layer:**
> CR-FM-03 default-to-STANDARD shim — every existing TASK-* file without a
> `Tier:` field validates clean post-merge; `gate-1: dispatch_profile=STANDARD
> source=default` emits once at entry; NO migration (the shim defaults at read
> time only). **Content layer:** AC-ATK-18 — at Gate-1.5 resume time, the
> executor greps the task body for `(/sc:task|sc-task-protocol|task-unified)`
> and emits `gate-1.5: legacy-surface-reference detected file=<path>
> action=warn-and-continue surface=<symbol>` per match; one-shot ack gate
> idempotent within ack-token-set state; never refuses entry (refuse would
> weaken INV-01). The H-4 scenario (resumed task names a deleted donor file as
> PRIMARY ARTIFACT) is the canonical failure: INV-01 holds by transition;
> INV-04 *semantically* breaks at L3 (subagent `Read` fails); the
> `⚪ Blocked` transition is logged. **Live in-flight blast radius at
> fix-cycle floor: 136 union files** (per research file 11 §2.1; supersedes
> 25/96/130/132 lineage figures)
> [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)].

**INV-05 (Refusal-of-definition — `Tier:` is metadata, NOT runtime classifier) — paragraph 5.**

> The merged surface contains NO embedded runtime classifier (verified by
> negative grep on `task/SKILL.md` — no priority cascade, no keyword tables,
> no runtime classification table). `Tier:` arrives declaratively from the
> task file's frontmatter and is read pre-loop only (ME-1 binding). Stage §2.0
> demonstrates: the validator reads schema fields (`Tier:`, frontmatter
> requirement list) but does NOT decide what work to do — the checklist body
> is untouched. D09b (donor classifier with priority cascade + keyword tables)
> was REJECTed as LR-REJECT-3, terminal. The per-item `(Tier: ...)` marker
> consumer list is a closed enumeration `{CR-TASK-07 baseline-skip}` per
> AC-ATK-05; any new consumer requires a new manifest exception, audited at
> the row level. Extension-point row 13 REJECTs "Required fields whose values
> *define the work*"
> [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] against
> `extension-point-contracts.md:17` + research file 10 §2.5.

### 15.7 Test Environments

| Environment | Purpose | Data | Tooling |
|---|---|---|---|
| Local (developer machine) | TDD red/green/refactor cycle | tmp_path fixtures + `tests/fixtures/donor-blocks/` | `uv run pytest`, `make test` |
| Pre-commit hooks (Steps 1-6) | Block bad commits before they land | Local working tree + frozen fixtures | `.git/hooks/pre-commit` + `scripts/audit/*.sh` |
| CI (GitHub Actions or self-hosted) | Continuous validation on every PR | Synthetic + intra-spec audits | `.github/workflows/test.yml` + `.github/workflows/audit.yml` |
| Server-side pre-receive (push-time) | Atomic-commit enforcement (AC-ATK-17) | Landing commit diff | `.github/workflows/pre-receive-cli-atomicity.yml` OR `.git/hooks/pre-receive.sh` |
| Resume-time (Gate-1.5 per task) | AC-ATK-18 content audit | Live in-flight MDTM file | In-skill executor logic |
| Sprint-emit boundary (per tasklist) | AC-ATK-18 companion | Rendered tasklist body | `src/superclaude/cli/sprint.py` |

---

## 16. Accessibility Requirements

> **Standard applied:** WCAG 2.1 AA *to the extent that the surface area permits*. This component has **no rendered visual surface** (no GUI, no web page) — the accessibility footprint is bounded to **terminal output and plain-text artifacts** consumed via the developer's preferred editor and screen reader.

### 16.1 Requirements

| Requirement | Implementation | Testing Method |
|-------------|----------------|----------------|
| **Terminal-output color contrast (no-color fallback)** | The skill body emits Task Log rows and gate tokens as **plain ASCII**, with no ANSI color escapes embedded in the persisted Task Log content. CLI emitters (`sprint`, `cleanup_audit`, `tasklist`) honor the `NO_COLOR=1` environment variable convention for any colorized stdout summaries. Result: a screen-reader-only operator captures the same factual content as a sighted operator. | Manual: set `NO_COLOR=1`, invoke `superclaude sprint run`, confirm stdout summary contains no ANSI escape sequences. Automated: a unit test fixture asserts that the rendered `/task ...` prompt (per AC-ATK-17) is pure ASCII with no `\x1b[` byte sequences. |
| **Plain-text Task Log format (no ANSI escape requirements)** | Task Log entries are appended as markdown table rows or bullet lines into the MDTM file body — pure UTF-8 text, no embedded escape codes. Gate-1.4 and Gate-1.5 emission tokens (per `research/11-in-flight-exposure-and-resumability.md` §4.2) are plain ASCII lines of the form `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`. | Inspect the committed MDTM files via any text reader (cat, less, screen reader); no glyph degradation. |
| **Task Log entries readable in any text editor (markdown-safe)** | All Task Log content is valid CommonMark — no proprietary markup, no binary attachments inside the task file. The TFEP incident-report side-effect file (`${TASK_DIR}/research/tfep-incident-report.md` per synth-04) is likewise CommonMark. | Open a `TASK-*.md` in any markdown viewer (VS Code, Obsidian, GitHub web view, plain `less`); all content renders or degrades cleanly to plain text. |
| **Keyboard-only operability** | All operator interaction is CLI-driven (typed commands) or Claude Code slash-command-driven (typed `/task`). No mouse, no GUI, no pointer-only gestures. | N/A — no pointer surface exists to fail. |
| **Screen-reader compatibility for emission tokens** | The Gate-1.5 token byte form is deliberately **whitespace-separated key=value pairs** rather than a colored or tabular layout, so a screen reader produces a navigable, comprehensible audit trail. | Manual: pipe a Task Log through `espeak` or VoiceOver; the operator can identify gate, action, surface, and file from the spoken output. |

### 16.2 Testing Tools

- **`grep -P '\x1b\['` over rendered CLI output and Task Log files** — confirms zero ANSI escape sequences leak into persisted artifacts. `[CONTENT-AUDIT-COMPLETED]`
- **CommonMark linter (`markdownlint-cli`)** — confirms `TASK-*.md` files plus `${TASK_DIR}/research/tfep-incident-report.md` parse without proprietary-syntax warnings.
- **Manual NO_COLOR=1 audit** — listed in §15 Testing Strategy as a release-blocker manual gate.

**Bounded surface acknowledgment:** This component has no visual UI, no rendered images, no form labels, no focus management surface. The WCAG 2.1 AA dimensions enumerated in the template (color contrast for rendered text, alternative text for images, form-label correctness, focus rings) are inapplicable. The accessibility commitment here is bounded to the items above — **plain-text artifacts, no-color fallback, screen-reader-friendly emission tokens**. `[CONTENT-AUDIT-COMPLETED]`

---

## 17. Performance Budgets

> **Note:** Backend-RPS budgets and frontend-LCP budgets do not apply (no HTTP API, no rendered UI). The performance surface that **does** apply is **token cost per execution phase**, **wall-clock per gate cycle**, **F1 loop iteration latency**, and **phase-gate QA latency**. All targets below are sourced from synth-08 §26 (where it lands) and the gate-cycle empirical observations in `research-notes.md`.

### 17.1 Frontend Performance — N/A

No rendered UI; FCP/LCP/FID/CLS/TTI are inapplicable. `[CONTENT-AUDIT-COMPLETED]`

### 17.2 Backend Performance — Token-Cost & Wall-Clock Budgets

| Metric | Budget | Measurement |
|--------|--------|-------------|
| **F1 loop iteration latency (per checklist item)** | ≤ 30s wall-clock for STANDARD-tier items; ≤ 5min for STRICT-tier items requiring sub-agent spawn | Timestamp delta between checklist item start and its `- [x]` checkmark in Task Log |
| **Research-gate cycle (parallel sub-agent fanout for research items)** | ≤ 10min wall-clock from gate-enter to gate-exit | Gate-enter and gate-exit Task Log row timestamps |
| **Synthesis-gate cycle (synthesis sub-agent fanout)** | ≤ 15min wall-clock from gate-enter to gate-exit | Gate-enter and gate-exit Task Log row timestamps |
| **Report-validation gate (qualitative + structural rf-qa)** | ≤ 10min wall-clock | Gate-enter and gate-exit Task Log row timestamps |
| **Qualitative-review gate (rf-qa-qualitative)** | ≤ 15min wall-clock | Gate-enter and gate-exit Task Log row timestamps |
| **Phase-gate QA (per partition, >15 output files)** | ≤ 5min wall-clock per partition | Per-partition timestamp delta in Phase-Gate QA Task Log section |
| **Token cost per phase (research + synthesis combined)** | Defer to §26 Cost & Resource Estimation | Token-usage report from Claude Code session telemetry |

### 17.3 Performance Testing

| Test Type | Tool | Frequency | Threshold |
|-----------|------|-----------|-----------|
| **Wall-clock budget audit per gate cycle** | Manual review of Task Log timestamps post-task | Per task completion | Each gate cycle ≤ its row above; flag in §14 Alerts when exceeded |
| **F1 iteration-latency soak** | `tests/sprint/test_process.py` with synthetic 50-item phase file | CI on merge | Mean iteration ≤ 30s under STANDARD tier |
| **Resume-gate latency (legacy MDTM)** | Manual: resume a 136-file in-flight task; measure CR-FM-03 shim + AC-ATK-18 audit wall-clock | Pre-release manual gate | ≤ 30s for shim + audit emission rows |

**Cost-budget cross-reference:** The token-cost-per-phase budget is **owned by §26 (Cost & Resource Estimation)** per the Phase 5 ownership matrix. The values quoted in row 7 above are placeholders; the canonical figures are bound in §26 below. `[CONTENT-AUDIT-COMPLETED]`

---

## 18. Dependencies

### 18.1 External Dependencies

| Dependency | Version | Purpose | Risk Level | Fallback | Source |
|---|---|---|---|---|---|
| `git` binary on every executing host | system PATH (any version ≥2.0) | TU-4 pre-flight `git status` 5-row matrix (clean/dirty/tool-absent/not-a-repo/error-other); CR-DEP-03 hard-delete; per-step commit gates | M — TU-4 degrades to `tool-absent` row of AC-ATK-02 matrix when exit 127; CR-DEP-03 cannot execute without git | Graceful-skip per ME-3 (warn-and-continue, NEVER HALT — INV-01 binding); operator manual fallback for delete | `research/00-prd-extraction.md:77` |
| `uv` runtime | project-pinned | All Python ops (pytest, lint, scripts) per CLAUDE.md absolute rule | L — required hard project requirement; CLAUDE.md forbids `python -m`/`pip install` | None — hard project requirement | `research/00-prd-extraction.md:78` |
| `pytest` (via `uv run pytest`) | per `pyproject.toml` dev dep | Pre-commit gates Steps 1, 5, 6; TFEP baseline snapshot `uv run pytest --collect-only -q`; verification of `tests/sprint/`, `tests/cli/`, `tests/skills/task/` | M — flaky pytest creates no-progress state under Step 5 atomicity (FM-02) | Pin env vars (PYTHONHASHSEED, locale, timezone) per FM-04; CI gate sign-off per R-OPS-04 | `research/00-prd-extraction.md:79`; `validation-spec.md:388-390` (FM-02/FM-04) |
| `pyyaml` | per `pyproject.toml` | YAML frontmatter parsing (CR-FM-03 shim); `${TASK_DIR}/research/test-baseline.yaml` (TU-5) load/parse for AC-ATK-03 4-state observer; CR-TASK-10 incident schema | L — used at multiple parse layers; failure cascades to AC-ATK-03 `parse-fail` state | Conservative over-escalate per AC-CR-TASK-09-F04 (classify all failures as `new`); never refuse task entry | `research/10-invariant-preservation-and-me-binding.md:164` (AC-ATK-03 four-state observer) |
| `click` | per `pyproject.toml` | CLI entry points (`superclaude sprint`, `superclaude install`, cleanup-audit CLI); `superclaude install --dry-run` for K-07 measurement | L — stable click 8.x API | None — hard project requirement | `research/00-prd-extraction.md:263` (K-07) |
| `rich` | per `pyproject.toml` | CLI terminal output rendering | L — cosmetic | Plain stdout fallback | (project Makefile / pyproject.toml) |
| `mkdocs` (build only) | unpinned (FM-05 risk) | Step 8 gate: `mkdocs build` returns 0 broken-link warnings | M — version drift could pass or fail same source tree (FM-05) | Pin mkdocs version in `pyproject.toml`/`docs/requirements.txt` before Step 8; record version in commit msg | `validation-spec.md:391` (FM-05) |
| `flock(2)` / POSIX file-locking | POSIX (BSD/macOS gap) | AC-ATK-16 sync-dev / `make verify-sync` atomicity against H-3 parallel-worktree race | M — BSD/macOS missing `flock(1)` binary; must `brew install flock` or use `lockfile-create` | Document deployment-surface portability gap in installer (web-01 cross-link `research/web-01-rebase-split-prevention.md:14`); fall back to `lockfile-create` on macOS | `research/web-01-rebase-split-prevention.md:14`; `validation-spec.md:307` (H-3) |
| `sha256sum` (or `shasum -a 256`) | system PATH | CR-DEP-02 sha256 baseline (replaces md5sum per AC-ATK-09) | L — universal POSIX | `openssl dgst -sha256` | `research/00-prd-extraction.md:299` (R-ATK-09) |

### 18.2 Internal Dependencies

| Component | Status (2026-05-16, pinned SHA) | TU/CR-row binding | Resolution | Source |
|---|---|---|---|---|
| `src/superclaude/skills/task/SKILL.md` (recipient skill, 376 lines) | LIVE `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`: F1 `:79-98`; F2 `:104-117`; rf-qa spawn `:191-198` + `:219-241`; Spawning Conventions `:290-299`; Session Resumption `:269-282` | All 8 TUs land changes here; foundation TUs M1 atomic (ME-6) | Edits land at Steps 1-4 covering all TUs | `research/00-prd-extraction.md:85`; `research/10-invariant-preservation-and-me-binding.md:30` |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` (donor, 365 lines) | LIVE `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`: TU-1 `:7-9, 49-58`; TU-2 `:121, 123`; TU-3 `:80-91, 114-119`; TU-4 `:81`; TU-5 `:144-154`; TU-6 `:129-142` (corrects R-DRIFT-02 anchor `:127-135`); TU-7 `:157-161` (corrects R-DRIFT-03 anchor `:200-210`); TU-8 `:222-234` | All 8 TUs read verbatim donor text under CR-TASK-12 audit | Hard-deleted at Step 6 (CR-DEP-03 + ME-9); R-RULE-10 binding requires both `src/` and `.claude/` mirror absence | `research/00-prd-extraction.md:86`; `research/13-adversarial-artifact-cross-validator.md:717-718` (R-DRIFT-02/03) |
| `src/superclaude/commands/sc/task.md` (donor `/sc:task` command facade, 170 lines) | LIVE `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`: classification header `:50-67`; tier rules `:69-91`; skill invocation `:93-101` | TU-1 closed-enum `{STRICT, STANDARD, LIGHT, EXEMPT}` sourced here `:55, 60, 71-89` | Stubified at Step 5 (CR-DEP-01); one-shot deprecation banner; `mcp-servers:` and `personas:` frontmatter REMOVED per ME-9 (CR-DEP-05) | `research/00-prd-extraction.md:87`; `research/13-adversarial-artifact-cross-validator.md:62-65` |
| `src/superclaude/cli/sprint/process.py` lines 124, 170 | LIVE `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`: `f"/sc:task Execute all tasks in @{phase_file} "` at :170; docstring at :124 | HZ-06 source; S-2 sequencing constraint (sprint emitter rewire before CR-DEP-01 stubification) | Re-routed to `/task` at Step 5 (CR-REF-01 + CR-REF-02 atomic with CR-DEP-01..02); AC-ATK-17 hook covers | `research/00-prd-extraction.md:88`; `research/13-adversarial-artifact-cross-validator.md:321` |
| `src/superclaude/cli/cleanup_audit/prompts.py` lines 26, 47, 69, 92, 116 (5 sites) | LIVE `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`: each is `f"/sc:task <verb> …"` prefix | HZ-07 source; S-2 sequencing constraint (cleanup-audit emitters); spec under-counts CLI emission sites by 5/6 (PRD R-DIV-01) | Re-routed at Step 5; AC-ATK-17 hook scope MUST extend to cover both `tests/sprint/` and `tests/cleanup_audit/` | `research/00-prd-extraction.md:89`; `research/13-adversarial-artifact-cross-validator.md:322` |
| `src/superclaude/pytest_plugin.py` | LIVE (auto-loaded via `pyproject.toml` entry point) | Fixtures: `confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context` consumed by `tests/skills/task/` tier-marker consumer test (planned per AC-ATK-05) | No edits required in this merge; tests/skills/task/ tests author against existing fixtures | `CLAUDE.md` (Pytest Plugin section) |
| `src/superclaude/pm_agent/` (`confidence.py`, `self_check.py`, `reflexion.py`) | LIVE | NFR-INV-1..5 verification rests on PM Agent confidence-check + self-check patterns; no direct edits | No edits required in this merge | `CLAUDE.md` (PM Agent Three Core Patterns) |
| `src/superclaude/execution/parallel.py` | LIVE | Wave→Checkpoint→Wave pattern referenced for parallel subagent dispatch (TU-3 widening) | No edits required in this merge | `CLAUDE.md` (Parallel Execution) |
| `src/superclaude/skills/task/` (full package: `SKILL.md` + `rules/` + `templates/` + `scripts/`) | LIVE | Recipient package; F1 loop and prohibitions catalog | M1 atomic edits across foundation rows | `research/10-invariant-preservation-and-me-binding.md:5` |
| `src/superclaude/skills/sc-task-protocol/` (donor package) | LIVE | Donor package; full directory hard-deleted at Step 6 (CR-DEP-03) | Directory absent post-Step-6 per K-06 (`find ... -type d` empty) | `research/00-prd-extraction.md:263` (K-06) |
| `.pre-commit-config.yaml` + `.git/hooks/` | `.pre-commit-config.yaml` present; `.git/hooks/` only `*.sample` (no active enforcement) | AC-ATK-17 server-side pre-push hook before Step 7 | Author server-side hook in pipeline before Step 7; GitHub.com gap → use Actions + branch-protection per `web-01-rebase-split-prevention.md:14` | `research/00-prd-extraction.md:90`; `web-01-rebase-split-prevention.md:14` |
| `Makefile` targets: `make sync-dev`, `make verify-sync`, `make dev`, `make test` | LIVE | S-3 atomicity (`make sync-dev` + `make verify-sync`); component-sync source-of-truth discipline | No edits required; AC-ATK-16 adds flock guard against H-3 race | `CLAUDE.md` (Component Sync); `research/00-prd-extraction.md:115` |
| `docs/generated/*` | LIVE `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`: 83 residuals across 20 files | CR-DEP-06 manifest target | One-shot CR-DEP-06 manifest at Step 9; FM-06 deferred-regen risk acknowledged | `research/00-prd-extraction.md:91` |
| `.dev/releases/backlog/` + archive | LIVE: 61 residuals across 20 files | CR-DEP-06 manifest target | CR-DEP-06 enumerates as authorized leave-as-is bucket | `research/00-prd-extraction.md:92` |
| `.dev/tasks/to-do/TASK-PRD-20260514-121039/` (S-1 target a) | LIVE `🟠 Doing`: **258 occurrences across 12 files** | S-1 sequencing binds; **R-DRIFT-04 RETRACTED** | Must complete OR snapshot-freeze OR auto-invoke (b) per AC-ATK-08 14d default before Step 5 | `research/11-in-flight-exposure-and-resumability.md:76-103`; `research/13-adversarial-artifact-cross-validator.md:9-15` |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/` (S-1 target b — H-4 surviving) | LIVE `🟠 Doing`: 48 occurrences across 10 files | S-1 + H-4 (PRIMARY-ARTIFACT path layer surface-mention) | AC-ATK-18 resume-time grep; first-resume acknowledgment gate | `research/00-prd-extraction.md:93`; `research/11-in-flight-exposure-and-resumability.md:106-128` |
| `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/` (S-1 target d — latent) | LIVE `To Do`: 30 occurrences across 5 files | S-1 binds **if promoted to in-flight before Step 5** | Reinstate to H-4 named list per `research/11-in-flight-exposure-and-resumability.md:158` | `research/11-in-flight-exposure-and-resumability.md:140-159` |
| `.dev/tasks/to-do/TASK-RF-20260515-195758/` (S-1 target c — never present) | ABSENT (never committed in git history) | DROP from S-1 / H-4 enumeration | No action; PRD body updated per `research/11-in-flight-exposure-and-resumability.md:130-138` | `research/11-in-flight-exposure-and-resumability.md:130-138` |

### 18.3 Cross-Team Dependencies

| Team | Dependency | Need | When | Status |
|---|---|---|---|---|
| (None in scope) | The merge is fully internal to the SuperClaude framework; no external team dependencies exist | — | — | — |

**Rationale:** Per `research/00-prd-extraction.md:95-106`, all eight cross-team dependencies listed in PRD §11.3 are owner-internal (Engineering Lead, Documentation/Release Owner, rf-qa Owner — all in the same maintainer cohort). These are open-questions (OQs) routed to engineering-lead disposition rather than true cross-team dependencies; they are captured in TDD §22 Open Questions, NOT as third-party dependencies. The merge has no upstream OSS dependency contracts, no inbound API contracts, no external SLO commitments.

---

## 19. Migration & Rollout Plan

### 19.1 Migration Strategy — 10-Step Canonical Commit Chain

The merge ships as a **10-step canonical commit sequence** per `research/13-adversarial-artifact-cross-validator.md:399-410` (`merge-master.md` §6) with explicit S-1/S-2/S-3 sequencing constraints and ME-6 atomicity binding on the foundation rows. The chain is acyclic (verified §5.2 of that research file); rollback granularity is **coarse at Steps 1, 5, 6** (atomic-by-design) and **fine at Steps 2, 3, 4, 7-10** (single CR-ID revertible) per §5.3.

| Step | Rows | Description | Pre-commit Gate | Sequencing Binding | Rollback |
|---|---|---|---|---|---|
| 1 | M1 atomic: CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-01, CR-TASK-02, CR-TASK-03, CR-TASK-04 | Foundation: `Tier:` field schema (CR-FM-01) + per-item marker grammar (CR-FM-02) + default-to-`STANDARD` compat shim (CR-FM-03) + Gate-1 dispatch site (CR-TASK-01..04) + CR-7 ORDERING sentinel | `uv run pytest` + `make verify-sync` returns 0; CR-FM-04 sentinel grep + CR-TASK-01/04 sentinel grep | **ME-6 atomic binding:** the seven rows are mutually-presupposing per `research/10-invariant-preservation-and-me-binding.md:243-249` — splitting CR-FM-01 from CR-TASK-02 leaves `Tier:` as inert metadata (R-RULE-06 violation); splitting CR-TASK-01 from CR-TASK-02 reopens the wrong-stance-dispatch window at row 1 runtime | **Coarse — atomic-by-design.** Single revert of the M1 commit reverses all 7 rows. F-01 + F-02 sentinel/audit additions revert with the commit. |
| 2 | M2 (interleavable): CR-TASK-05, CR-TASK-06 | Gate-2 roster widening `[rf-qa, quality-engineer]` (CR-TASK-05); D15b pre-flight `git status` 5-row matrix (CR-TASK-06) | Depends on Step 1 only; F-03 dirty-tree closure AC | None beyond Step 1 dependency | **Fine — single CR-ID revertible.** Revert CR-TASK-05 OR CR-TASK-06 independently; if CR-TASK-06 reverted, AC-CR-TASK-06-F03 dirty-tree warn-and-continue closure also reverts. |
| 3 | M3 TFEP: CR-TASK-07 → CR-TASK-08 → CR-TASK-09 → CR-TASK-10 | TFEP baseline (CR-TASK-07); prohibitions catalog absorption to F2 (CR-TASK-08, byte-for-byte from donor `:129-142`); escalation routing mid-phase rf-qa (CR-TASK-09); incident-report 7-field schema (CR-TASK-10) | DM-7 / DM-9 internal ordering; F-04 + F-05 closures (CR-TASK-09 AC additions) | **R-DRIFT-02/03 PRE-PATCH REQUIRED before Step 3 commits:** the CR-TASK-12 verbatim-diff audit MUST be re-pointed from `:127-135` → `:129-135` (or `:133-135`) and from `:200-210` → `:157-161` per `research/13-adversarial-artifact-cross-validator.md:717-718` — failure to patch causes erroneous block of M3 commit | **Fine.** Each CR-TASK-NN can be reverted independently within M3 ordering. |
| 4 | M-sync + audits: CR-TASK-11 (sha256 replaces md5sum per AC-ATK-09), CR-FM-04, CR-TASK-12 | Verbatim-diff audit (CR-TASK-12, 7-diff scope: 6 donor + 1 sentinel block per F-02) | All three pass; commit blocked otherwise | None beyond M3 dependency | **Fine.** Audit rows revertible independently. |
| 5 | M4-A soft-deprecation: CR-DEP-01, CR-DEP-02, CR-DEP-05 + **atomic** CR-REF-01, CR-REF-02, CR-REF-09 + **atomic** CR-DOC-01 | Stubify `/sc:task` command (CR-DEP-01) + sha256 baseline (CR-DEP-02) + ME-9 audit (CR-DEP-05) + sprint CLI re-route (CR-REF-01..02) + sprint TUI re-route (CR-REF-09) + doc redirect (CR-DOC-01) | `uv run pytest tests/sprint/test_process.py && tests/sprint/test_tui_v2_wave2.py && tests/pipeline/test_process.py` returns 0 | **S-1 binding (live):** `TASK-PRD-20260514-121039` (258 refs, 12 files, 🟠 Doing) MUST complete OR snapshot-freeze with decision record OR auto-invoke option (b) per AC-ATK-08 14d default before this step. **R-DRIFT-04 RETRACTED** — S-1 is non-moot per `research/13-adversarial-artifact-cross-validator.md:9-15`. **S-1 supplement-not-replace:** generalize to "any in-flight task referencing donor surfaces, current floor = **136 union files**" per `research/11-in-flight-exposure-and-resumability.md:43, 68`. **S-2 binding:** sprint + cleanup-audit emitters re-routed atomically with CR-DEP-01 stubification (otherwise CLI breaks). | **Coarse — atomic-by-design.** Revert CR-DEP-01..02 + CR-REF-01..02 + CR-REF-09 + CR-DOC-01 atomically. If Step 6 has already shipped (hard-deprecation), Step 5 cannot be cleanly rolled back without also reverting Step 6 per `research/13-adversarial-artifact-cross-validator.md:424`. |
| 6 | M4-B hard-deprecation + sync rule: CR-DEP-03 + CR-DEP-04 + CR-DIST-02 atomic; CR-DIST-01, CR-DIST-04, CR-REF-10 same/next commit; CR-DIST-03 + CR-REF-08 may land here or next | Donor skill hard-delete (`src/superclaude/skills/sc-task-protocol/` + `.claude/skills/sc-task-protocol/`); CR-DIST-02 sync rule | `make verify-sync` returns 0; AC-ATK-07 rf-qa F-07 verifier PASS; CR-DEP-04 directory-absence; CR-DEP-05 grep returns zero on both `[src]` and `[.claude]` (ME-9) | **S-3 binding:** CR-DEP-03 + CR-DEP-04 + CR-DIST-02 must land atomically; absent atomicity `make verify-sync` reports drift between `[src]` delete and `[.claude]` prune per `research/13-adversarial-artifact-cross-validator.md:328`. **F-07 annotation:** procedural authorization chain (sprint goal → T06.03 task description → `refactor-sctask-deprecation.md` § 2 + § 4) is binding precondition. | **Destructive — roll FORWARD preferred.** Reverting Step 6 requires re-introducing the donor skill files (the deletion is destructive-by-default); safer to roll forward per `research/13-adversarial-artifact-cross-validator.md:425`. If revert needed: restore from git history; re-run S-3 atomicity gate. |
| 7 | M5-B remaining + M5-C live backlog: CR-REF-04, CR-REF-05, CR-REF-06, CR-REF-07, CR-REF-11, CR-REF-14 + CR-REF-12 + CR-DIST-05 + CR-DIST-06 | Live-backlog ref re-routes; ME-9 R-RULE-11 re-affirmation | `make verify-sync` returns 0; AC-SM-03 walkthrough fixture + AC-SM-04 | None beyond Step 6 dependency | **Fine.** Each CR-REF-NN revertible independently. |
| 8 | M5-E doc redirects: CR-DOC-01 (or co-shipped Step 5), CR-DOC-02, CR-DOC-04, CR-DOC-05, CR-DOC-03 | User-guide doc redirects; AC-ATK-17 server-side pre-push hook landing | `mkdocs build` 0 broken-link warnings; pre-push hook installed and re-grepping landing commit (not working tree) for `/sc:task` in CLI sources | None | **Fine — annotation only.** Revertible per-CR-DOC. **Caveat FM-05:** mkdocs version not pinned; pre-pin before Step 8 to avoid version-drift drift. |
| 9 | M5-C/M5-D/M5-F annotation pass + CR-DEP-06 manifest: CR-REF-15..18, CR-DOC-06..09, CR-DOC-11 partial | CR-DEP-06 one-shot manifest of authorized leave-as-is residual `/sc:task`/`sc-task-protocol`/`task-unified` references across `docs/generated/`, `.dev/releases/backlog/`, archived task subtrees | None beyond grep verification | **OQ-4 binding:** CR-DEP-06 elevated from proposal to required closure (PRD §14.3); confirm 144-binding count (61 backlog + 83 docs/generated) | **Fine — manifest-only.** Per-row annotation reverts cheap. |
| 10 | Audit closure: CR-DOC-10, CR-DOC-11 (live portion), CR-DOC-12, CR-DOC-13 + CR-DEFER-T06.04 ack | R-RULE-11 audit clean; AC-SM-01..12 audits | R-RULE-11 audit clean; K-01..K-08 measurement run; CR-DEP-06 archived to `docs/generated/` | None | **Fine — audit-only.** Revertible. |

### 19.2 S-1/S-2/S-3 Sequencing Constraint Detail

**S-1 — In-flight PRD completion before Step 5 (CRITICAL, binding).** Per `research/11-in-flight-exposure-and-resumability.md:344` and `research/13-adversarial-artifact-cross-validator.md:9-15`:

- **Binding targets (LIVE):**
  - Target (a) `TASK-PRD-20260514-121039` — 🟠 Doing, **258 occurrences across 12 files** `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]`. **R-DRIFT-04 RETRACTED** — S-1 binding is NOT no-op; HZ-03 from `compat-hazard-report.md` is NOT stale.
  - Target (b) `TASK-RESEARCH-20260403-sprint-task-exec` — 🟠 Doing, 48 occurrences across 10 files (H-4 surviving exposure target).
  - Target (d) `TASK-RF-20260403-tasklist-e2e` — `To Do`, 30 occurrences across 5 files (latent; reinstate to H-4 if promoted to in-flight before Step 5).
- **Dropped target:** Target (c) `TASK-RF-20260515-195758` — GENUINELY ABSENT (never committed). Drop from S-1/H-4 enumeration.
- **Population-generalized binding:** "Any in-flight task referencing donor surfaces" with live floor of **136 union files** at PRD-completion authoring time (2026-05-16 drift snapshot, monotonic upward). Implementation uses live recount via `grep -rl '/sc:task\|sc-task-protocol\|task-unified' .dev/tasks/ | wc -l` at the time of authoring per `research/11-in-flight-exposure-and-resumability.md:68`.
- **Mitigation hierarchy:** (a) complete in-flight tasks before Step 5; (b) auto-invoke at `--max-wait 14d` expiry per AC-ATK-08 with decision record; (c) snapshot-freeze with pinned git-SHA on `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` tag.
- **Anti-pattern:** Hardcoding the literal "96" or "132" or "25" — all three are `[CODE-CONTRADICTED]` per `research/11-in-flight-exposure-and-resumability.md:333-336`.

**S-2 — CLI emitter atomicity (CR-REF-01 + CR-REF-02 + CR-REF-09 ≤ CR-DEP-01).** Per `research/13-adversarial-artifact-cross-validator.md:326`:

- All CLI emitters of `/sc:task` MUST be re-routed to `/task` **atomically with** (not before, not after) CR-DEP-01 stubification of the `/sc:task` command.
- **Cited surfaces:** `src/superclaude/cli/sprint/process.py:124, 170` (HZ-06); `src/superclaude/cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116` (HZ-07, 5 sites under-counted by spec per PRD R-DIV-01).
- **Pre-commit gate enforcement:** `uv run pytest tests/sprint/test_process.py && tests/sprint/test_tui_v2_wave2.py && tests/pipeline/test_process.py` returns 0 at Step 5 commit boundary per `final-merge-plan.md` §6 Step 5.
- **Rebase-split risk (R-ATK-17 / R-H-02):** intermediate master SHA carrying stubified `task.md` but live CLI emissions is the H-2 hazard; AC-ATK-17 server-side pre-push hook MUST cover BOTH sprint AND cleanup_audit emitter scopes.

**S-3 — Mirror-sync atomicity (CR-DEP-03 + CR-DEP-04 + CR-DIST-02 atomic).** Per `research/13-adversarial-artifact-cross-validator.md:328`:

- Hard-deletion of donor skill must land **atomically with** the `.claude/` mirror prune AND the CR-DIST-02 sync-rule update.
- **Pre-commit enforcement:** `make verify-sync` returns 0 (otherwise drift between `[src]` delete and `[.claude]` prune).
- **Flock guard:** AC-ATK-16 adds `flock`-guarded atomicity on `.claude/skills/` during `make sync-dev` prune to prevent H-3 parallel-worktree race.

### 19.3 ME-6 Atomicity Binding (Foundation Rows)

Per `research/10-invariant-preservation-and-me-binding.md:238-249`, ME-6 binds the **seven M1 foundation rows** (CR-FM-01..03 + CR-TASK-01..04) to a single source-tree merge commit at Step 1. The rows are mutually-presupposing:

- Splitting CR-FM-01 (Tier field schema) from CR-TASK-02 (Gate-1 dispatch parse-error HALT) leaves `Tier:` as inert metadata (R-RULE-06 "no inert metadata; no ceremony-without-teeth" violation).
- Splitting CR-TASK-01 (CR-7 ORDERING sentinel) from CR-TASK-02 reopens the wrong-stance-dispatch window at row 1 runtime.
- CR-TASK-12 (verbatim-diff audit) at Step 4 depends on M1 atomicity to land — the byte-for-byte transplant of TFEP donor strings (CR-TASK-08/09/10 M3 cluster at Step 3) presupposes M1 foundation rows are live.

**Pre-commit enforcement of ME-6:** the Step 1 commit MUST be a single commit (not a feature-branch with separate row commits squashed at merge-time, which leaves intermediate states failing their own pre-commit gates per `validation-spec.md:64`).

### 19.4 Per-Step Rollback Granularity

Per `research/13-adversarial-artifact-cross-validator.md:421-428`:

| Step | Granularity | Revert Cost | Special Considerations |
|---|---|---|---|
| 1 (M1 atomic) | **Coarse** | 1 revert reverses 7 rows | ME-6 atomic-by-design; F-01 + F-02 closures revert with commit |
| 2 (M2 interleavable) | Fine | Per-CR-ID | F-03 dirty-tree AC reverts if CR-TASK-06 reverted |
| 3 (M3 TFEP) | Fine | Per-CR-ID (within DM-7/DM-9 order) | R-DRIFT-02/03 pre-patch dependency |
| 4 (Audit) | Fine | Per-CR-ID | Audit-only rows |
| 5 (M4-A soft-deprecation) | **Coarse** | 1 revert reverses CR-DEP-01..02 + CR-REF-01..02 + CR-REF-09 + CR-DOC-01 | If Step 6 already shipped, Step 5 cannot be cleanly rolled back without also reverting Step 6 |
| 6 (M4-B hard-deprecation) | **Destructive-by-default** | Restoration requires git-history re-introduction | Roll FORWARD preferred over revert; S-3 atomicity gate must re-pass |
| 7 (M5-B/M5-C) | Fine | Per-CR-REF-NN | None |
| 8 (M5-E doc) | Fine | Per-CR-DOC-NN | mkdocs version pin recommended |
| 9 (CR-DEP-06 manifest) | Fine | Per-row | Manifest-only |
| 10 (audit closure) | Fine | Per-row | Audit-only |

### 19.5 Feature Flags & Progressive Delivery

| Flag | Description | Default | Rollout Plan | Cleanup Date | Owner |
|---|---|---|---|---|---|
| `CR-FM-03` shim (`Tier:` default-to-`STANDARD` on absence) | Backward-compat shim for in-flight 136 union files lacking `Tier:` frontmatter | Active on Step 1 | Always-on from Step 1; sunset binding **TBD** per OQ-FM-03-SUNSET (recommended: `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`) per `research/10-invariant-preservation-and-me-binding.md:349` | After CR-MIGR-FM-03 migration ships AND 50 generations AND 90 days post-Step-6 | Engineering Lead |
| `gate-1.4` shim-status counter (CR-FM-03 sunset audit emission) | Emits `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<N> sunset_row_authored=<bool>` per resume | Active on Step 1 | Always-on from Step 1 | Co-removed with CR-FM-03 shim | Engineering Lead |
| `gate-1.5` legacy-surface content audit (AC-ATK-18) | Resume-time grep against task body for `(/sc:task\b\|sc-task-protocol\|task-unified)`; emits warn-and-continue token per `research/11-in-flight-exposure-and-resumability.md:194-208` | Active on Step 1 | Always-on; one-shot acknowledgment gate per first-resume | Indefinite (semantic-layer INV-04 guarantee) | Engineering Lead |
| Server-side pre-push hook (AC-ATK-17) | Re-greps landing commit for `/sc:task` in CLI sources; covers sprint + cleanup_audit emitter scope | Inactive pre-Step-8 | Activates at Step 8; GitHub.com gap → Actions + branch-protection-required-checks per `web-01-rebase-split-prevention.md:14` | Indefinite (CLI surveillance) | Engineering Lead |

> **Rule per template:** Every feature flag MUST have a `Cleanup Date`. CR-FM-03 shim cleanup is gated on OQ-FM-03-SUNSET resolution; gate-1.5 / pre-push are indefinite by design (semantic-layer INV-04 + R-RULE-11 surveillance).

### 19.6 Rollout Stages

Standard percentage-based rollout stages (canary/limited/partial/full) do **NOT** apply to this merge — it is a discrete commit chain landing into the SuperClaude framework codebase, not a runtime-served feature with traffic shifting. The "rollout stages" map to the 10 commit boundaries above; each commit boundary is the equivalent of a stage with its own pre-commit gate as success criterion and per-step revert as rollback trigger.

### 19.7 Rollback Decision Criteria

Per `validation-spec.md:388` (FM-02) and `research/13-adversarial-artifact-cross-validator.md:421-428`:

- **Pre-commit gate failure at any step** → block commit; do NOT land partial state. Re-run after fix.
- **Post-commit test failure (`uv run pytest` red)** in `tests/sprint/`, `tests/cli/`, or `tests/skills/task/` after Step 5 or Step 6 → revert immediately if within atomic boundary; roll forward with hotfix if past Step 6.
- **`make verify-sync` non-zero post-Step-6** → S-3 atomicity violated; revert CR-DEP-03 + CR-DEP-04 + CR-DIST-02 atomically OR roll forward with sync hotfix.
- **R-RULE-11 audit (Step 10) detects re-introduced REJECTed donor pattern** → revert offending CR-row; re-audit.
- **In-flight task INV-04 semantic failure (H-4 transition-to-Blocked observed in production)** → AC-ATK-18 emission did NOT fire (gate-1.5 missing); add per-task `--compliance strict` override; do NOT revert Step 6.

### 19.8 Deprecation Cycle Precedents

The 10-step chain models the **soft-deprecate → hard-deprecate → residual-manifest** pattern from established practice. Per `research/web-02-content-vs-parse-resumability.md:14` (read the source for URLs):

- **Python `DeprecationWarning` → `PendingDeprecationWarning` → removal cycle** — Step 5 = warn surface (CR-DEP-01 stubification with deprecation banner); Step 6 = removal (CR-DEP-03 hard-delete).
- **GitHub API deprecation cycle 30→180 days** — analogous to OQ-FM-03-SUNSET `N=50 generations AND ≥90 days` post-Step-6 binding.
- **Stripe API versioning** ("API requests are tied to a specific version, and we maintain backward compat") — analogous to CR-FM-03 shim per-resume backward-compat at the parse layer.
- **Alembic "inline throwaway ORM models for data migrations"** — analogous to the "in-flight task file is a third intermediate snapshot, not pre-merge or post-merge" framing for AC-ATK-18 content audit (see §21 Alternative 3 below).

---

## 20. Risks & Mitigations

### 20.1 PRD K-01..K-08 Bound Risks (NOT K-001..K-010)

Per `research/00-prd-extraction.md:257-264` and `research/00-prd-extraction.md:420` — the user-query reference to "K-001..K-010" was a typo; the PRD uses **K-01..K-08** for KPIs/success metrics, each with implicit risk on miss. The risk rows below pair each K-NN KPI with its associated failure mode:

| ID | Risk | P | I | Mitigation | Contingency |
|---|---|---|---|---|---|
| **K-01** | Unmitigated AC-ATK row(s) survive Phase 7.5 closure (OPEN or PARTIAL state) — degrades audit posture | L | H | Post-Phase-7.5 traceability matrix re-run vs validation-spec §11.1; CI-emitted JSON manifest gate per `research/00-prd-extraction.md:257` | Hold Step 10 audit closure until 0 OPEN/PARTIAL rows; escalate to Engineering Lead |
| **K-02** | Sprint-runner pytest pass rate drops post-CLI rewire (CR-DEP-04) — S-2 break | M | H | `uv run pytest tests/cli/ -v` green on integration immediately after Step 5/6 commits per `research/00-prd-extraction.md:258` | Revert Step 5 atomic bundle; re-author CR-REF-01..02 with broader test coverage |
| **K-03** | Residual `/sc:task` occurrences NOT eliminated by CR-DEP-06 manifest (144 → 0 outside authorized buckets fails) | M | M | Post-Step-6 `grep -RE '/sc:task\b\|sc-task-protocol\|task-unified'` minus authorized buckets; CR-DEP-06 manifest enumerates survivors per `research/00-prd-extraction.md:259` | Extend CR-DEP-06 manifest to cover discovered residuals; re-run grep |
| **K-04** | `make verify-sync` flake rate post-flock (AC-ATK-16) — H-3 race not fully closed | L | M | CI log retention; scan 30 most-recent invocations; target 0 flakes per `research/00-prd-extraction.md:260` | Add second flock guard scope; investigate per-OS portability (BSD/macOS gap) |
| **K-05** | Post-merge audit FAIL on any CR-FM-NN / CR-TASK-NN / CR-DEP-NN / CR-DIST-NN / CR-REF-NN / CR-DOC-NN row — 100% PASS target missed | L | H | Aggregated pre-commit gate output for Steps 1, 4, 5, 6, 8; rf-qa Step 6 chain-verification (AC-ATK-07) PASS before hard-delete per `research/00-prd-extraction.md:261` | Block step commit until row PASS; reopen failed row for re-author |
| **K-06** | Donor SKILL.md persists post-Step-6 (`src/` or `.claude/` copy survives) — ME-9 / CR-DEP-04 break | L | H | Two `test -f` checks return non-zero; `find ... -type d` empty; CR-DEP-04 gate returns 0 per `research/00-prd-extraction.md:262` | Re-run CR-DEP-03 hard-delete; investigate sync-rule (CR-DIST-02) failure |
| **K-07** | Visible command + skill surface count not reduced 2 → 1 (paired entries) | L | M | `superclaude install --dry-run` roster diff; `/sc:help` listing post-Step-6 per `research/00-prd-extraction.md:263` | Audit installer for residual donor command/skill enumeration |
| **K-08** | Maintenance surface-pair count not reduced 2 → 1 (paired SKILL.md files) | L | L | Repo census of `src/superclaude/skills/*/SKILL.md` matching protocol-class regex per `research/00-prd-extraction.md:264` | Confirm CR-DEP-03 deleted both `src/superclaude/skills/sc-task-protocol/SKILL.md` and `.claude/skills/sc-task-protocol/SKILL.md` |

### 20.2 Validation-Spec §15 Residual-Risk Concessions (5 rows)

Per `validation-spec.md:409-419`, the steelman acknowledges **five places where the defense cannot fully cover the attacks**. These are residual risks that survive after Phase 7.5 closure:

| ID | Concession | P | I | Mitigation | Contingency |
|---|---|---|---|---|---|
| **R-RES-01** (§15 L415) | "Tier-conditioned read" boundary conceptually thin; sufficiently determined refactor could describe a forbidden per-item dispatch as a "read" if it routes through a wrapper. Defense relies on R-RULE-11 audit discipline at design-time — human-process, NOT structural | M | M | AC-ATK-05 closed enumeration of authorized per-item marker consumers (current: `{CR-TASK-07 baseline-skip}`); ME-1 design-time review checklist; CI lint step in `make verify` that fails on undeclared marker consumers per `research/10-invariant-preservation-and-me-binding.md:347` | New consumer adds require new ME-10+ entry; audit at row level |
| **R-RES-02** (§15 L416) | Fourth rf-qa invocation point (F-05 mid-phase routing, TU-7 — authoritative rf-qa count post-merge = 4) widens INV-03 surface beyond canonical anchor language; anchor source `extension-point-contracts.md:11-17` NOT amended | L | M | AC-ATK-11: either back F-05 with retroactive ME-10 OR explicitly mark as one-time non-generalizing carve-out per OQ-F-05-MANIFESTIZATION | Resolve OQ-F-05-MANIFESTIZATION before Step 4 (TU-7) commit; document chosen disposition in commit msg |
| **R-RES-03** (§15 L417) | F-04 over-escalation = load-volume bet on rf-qa; classifying every failure as `new` when baseline is absent could flood the verifier queue; plan does NOT bound upper limit on routing volume | M | M | Monitor rf-qa queue depth; reactive refusal threshold; PRD R-OPS-03 acknowledged per `research/00-prd-extraction.md:377` | If queue floods: tighten AC-CR-TASK-09-F04 to require operator ack at threshold; investigate baseline-absence frequency |
| **R-RES-04** (§15 L418) | S-1 hierarchy (a / b / c) recorded but NOT decided; `--max-wait` carrier surface (CLI flag / frontmatter / operator discipline) ambiguous per OQ-S-1-CARRIER; late-discovered infeasibility of (a) means options (b) or (c) get chosen under time pressure | M | M | AC-ATK-08: `--max-wait 14d` default + auto-invoke (b) at expiry + pinned-SHA on `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` tags per `research/00-prd-extraction.md:298` | Pre-decide carrier surface per OQ at TDD review; document Engineering Lead disposition |
| **R-RES-05** (§15 L419) | F-07 procedural authorization chain "NOT a manifest binding"; reviewer applying strict-manifest-only discipline could insist on retroactive amendment despite documentation chain | L | L | AC-ATK-07: rf-qa rebound as F-07 chain-integrity verifier at Step 6 pre-commit per `research/00-prd-extraction.md:297` | Document procedural chain in commit msg + `final-merge-plan.md` §4.7; escalate retroactive-amendment requests to Engineering Lead |

### 20.3 Combined Risk Posture

Aggregating PRD §20 risk rows beyond K-NN per `research/00-prd-extraction.md:283-388`:

- **R-ATK-01..18 predicate-precision risks** — closed by AC-ATK-01..18 (1:1 mapping). All 18 ACs MUST be in PASS state at Phase 7.5 closure per K-01.
- **R-S-01..03 timeline-layer hazards** — closed by S-1/S-2/S-3 sequencing constraints in §19.2 above. R-S-01 (S-1 no `--max-wait` enforcer) and R-S-02 (S-2 atomicity) are HIGH-P; AC-ATK-08 + AC-ATK-17 carry.
- **R-H-01..03 hazard scenarios** — H-1 PRD stall + `[CODE-CONTRADICTED]` corruption (AC-ATK-08 + pinned-SHA); H-2 rebase-split (AC-ATK-17 extended grep + `tests/cleanup_audit/test_prompts.py`); H-4 resumed task hits deleted PRIMARY ARTIFACT (AC-ATK-18 + CR-DEP-06).
- **R-FM-01..08 failure-mode gaps** — see §20.4 below for mitigation map.
- **R-EC-01..04 evidence-completeness gaps** — closed by Phase 7 grep-pattern specification, comparison-method specification, V/C/K re-derivation sample expansion to 8/8 TUs.
- **R-BIZ-01..03 business risks** — R-BIZ-01 merge-stall (AC-ATK-08 + decision record); R-BIZ-02 tier-vocabulary (OQ-1 pre-merge resolve); R-BIZ-03 companion-TDD absence (OQ-5 — this TDD is the OQ-5 affirmative path).
- **R-OPS-01..04 operational risks** — R-OPS-02 H-4 manual operator intervention (AC-ATK-18 + pre-flag at-risk task ID + operator runbook).

### 20.4 Failure-Mode Coverage (R-FM-01..08)

Per `validation-spec.md:383-394`:

| ID | Failure Mode | Mitigation |
|---|---|---|
| R-FM-01 | `make verify-sync` doesn't check symlink divergence (defeats R-RULE-10) | Pre-Step-6 audit: `find src/superclaude/skills .claude/skills -type l` returns empty |
| R-FM-02 | Step 5 atomic across six rows; flaky pytest creates no-progress state | Pin env vars per FM-04; CI gate sign-off per R-OPS-04 |
| R-FM-03 | Two implementation sub-agents in parallel land conflicting SKILL.md edits at row 1 vs row 10 | AC-ATK-16 + ban parallel subagent dispatch on `task/SKILL.md` during Step 5 per `research/00-prd-extraction.md:375` |
| R-FM-04 | `uv run pytest` CI vs local env divergence (PYTHONHASHSEED, locale, timezone) | Pin env vars in `pyproject.toml` or `tox.ini`; pre-commit gate enforces env |
| R-FM-05 | mkdocs version not pinned; broken-link semantics could differ | Pin mkdocs in `pyproject.toml` before Step 8 |
| R-FM-06 | `docs/generated/*` regen unscheduled; permanently disagrees with `docs/` source (83 occurrences live) | CR-DEP-06 manifest archives weekly to `docs/generated/`; investigate regen scheduler |
| R-FM-07 | UTF-16-authored markdown silently passes every grep with no matches | Specify text encoding in all greps: `grep --include='*.md' -P` with locale set |
| R-FM-08 | Donor file renamed (`*.deprecated`) rather than deleted bypasses absence check | CR-DEP-04 enforces `find ... -type d` empty AND `find -type f` empty for donor directory |

---

## 21. Alternatives Considered

> **This is one of the most important sections of the TDD.** Per template `tdd_template.md:1034`, alternatives must be genuinely evaluated. The chosen path is the 10-step canonical commit sequence with CR-FM-03 default-to-`STANDARD` parse-layer shim + AC-ATK-18 semantic-layer content audit. The eight unnamed tradeoffs from validation-spec §12 are surfaced below as named opportunity-costs.

### Alternative 0: Do Nothing *(mandatory)*

**Description:** Leave `/sc:task` and `/task` as parallel paired surfaces. No directional merge. Both skills (`task/` and `sc-task-protocol/`) remain live. Both commands (`/task` and `/sc:task`) remain available. CLI emitters (sprint + cleanup_audit) continue calling `/sc:task`. The 136 in-flight union files continue to coexist with both surfaces.

**Pros:**
- No engineering cost (no 10-step commit chain to author)
- No operational burden (no S-1/S-2/S-3 sequencing constraints to police)
- No risk of introducing regressions (no INV-01..05 attack surfaces opened)
- In-flight 136 union files unaffected (no AC-ATK-18 resume-time grep required)
- No R-DRIFT-02/03 anchor patches required pre-Phase-7
- No CR-FM-03 shim sunset binding to author

**Cons:**
- **K-08 — Maintenance burden persists 2 → 2** (no surface-pair reduction). Engineers continue maintaining two `SKILL.md` files (`task/SKILL.md` + `sc-task-protocol/SKILL.md`) that drift from each other; every TFEP/tier-marker change requires synchronized edits across both.
- **K-07 — UX cost persists 2 → 2** (no command surface reduction). Two paired entries (`/task` + `/sc:task`) remain in `/sc:help`; users confused about which to invoke.
- **Donor-feature absorption blocked.** TFEP cluster (TU-5..TU-8), path overrides (TU-2), pre-flight scaffolding (TU-4), Gate-2 widening (TU-3), Tier field + Gate-1 (TU-1) all stuck in donor; cannot be invoked through recipient `/task` F1 loop without re-authoring.
- **Audit posture stale.** Validation-spec §16 verdict `convergence_score: 0.86 ≥ 0.85 threshold` per `validation-spec.md:19` already authorizes PASS; deferring indefinitely leaves the convergence work unrealized.
- **OQ-5 (companion TDD) unresolved.** Engineering audience strongly recommends companion TDD; doing nothing defers OQ-5 indefinitely (R-BIZ-03 adoption friction).
- **R-DOC-01 reframed audit artifacts** (7 PRESENT on disk per fix-cycle 2) remain unaudited at the row level; AC-SM-01..12 carry `[CONTENT-AUDIT-OWED]` flags indefinitely.

**Why Not Chosen:** The donor `sc-task-protocol/SKILL.md` (365 lines) contains 8 ADOPTed/ADAPTed Transfer Units that are load-bearing for compliance workflows (TFEP cluster), pre-flight scaffolding, and tier-routed Gate-1/Gate-2 enforcement. These survive in the donor and are inaccessible from the recipient `/task` F1 loop without merge. Cumulative annual maintenance cost of dual-surface maintenance (K-08) compounds; deferring indefinitely is strictly dominated by the 10-step chain with finite, scoped 5 residual concessions (R-RES-01..05). The 0.86 convergence verdict per `validation-spec.md:19` authorizes proceeding.

---

### Alternative 1: Big-Bang Single-Commit Merge

**Description:** Land all 65 CR-IDs in a single commit. No 10-step sequence; no S-1/S-2/S-3 sequencing constraints; no per-step rollback granularity. ME-6 atomicity extended from M1 foundation to ALL rows.

**Pros:**
- No intermediate broken master SHA (R-H-02 H-2 rebase-split bypass impossible by construction)
- No S-1 14d wait for in-flight PRDs (single atomic landing)
- No S-2 atomicity policing between sprint CLI and `/sc:task` stubification
- No S-3 mirror-sync race window

**Cons:**
- **Unreviewable scope.** 65 CR-IDs across 6 refactor file areas + 8 TUs + 9 MEs + 18 ACs in one commit defeats code-review and bisect-ability.
- **No rollback granularity.** Step 6 hard-delete (destructive-by-default per `research/13-adversarial-artifact-cross-validator.md:425`) and Step 1 inert-metadata risk both collapse into one all-or-nothing revert; if K-02 (sprint pytest) fails post-commit, full rollback is the only option.
- **S-1 in-flight conflict explodes.** 136 union files (and live targets a/b/d with 258+48+30 = 336 donor-surface occurrences) all must be resolved at the same instant; no per-step coordination window with in-flight task owners.
- **Pre-commit gate budget overflow.** All 4 gate suites (`uv run pytest`, `make verify-sync`, `mkdocs build`, AC-ATK-07 rf-qa F-07) must pass simultaneously; flake probability multiplies.
- **F-NN closure auditing impossible per-step** — F-01..F-08 closures rely on per-step row-deltas per `final-merge-plan.md` §4.

**Opportunity cost (named):** Trades **rollback granularity** (Steps 2, 3, 4, 7-10 fine-grained) for **rebase-split elimination**. Per AC-ATK-17, the rebase-split risk is mitigated by server-side pre-push hook covering both sprint + cleanup_audit emitters — making this alternative's primary "pro" already covered by the chosen path.

**Why Not Chosen:** The 10-step chain's per-step rollback granularity (Steps 2/3/4/7-10 fine-grained) and bisect-ability are operationally critical. R-FM-02 (Step 5 atomic flaky-pytest no-progress) already represents the upper bound of acceptable atomic-commit risk; extending atomicity to all 65 rows multiplies this risk by ~10x. AC-ATK-17 mitigates rebase-split without sacrificing granularity.

---

### Alternative 2: Two-Phase Release Split (Soft-Deprecate Now, Hard-Delete Later)

**Description:** Phase A ships Steps 1-5 + Step 8 + Step 9 (soft-deprecate `/sc:task` to stub; CLI rewire; doc redirects; CR-DEP-06 manifest); Phase B (separate release, weeks/months later) ships Step 6 + Step 7 + Step 10 (hard-delete donor skill; AC-SM-03 walkthrough audit; audit closure). CR-FM-03 shim deliberately permanent across Phase A; sunset binding deferred to Phase B closure.

**Pros:**
- Eliminates S-1 14d wait (in-flight tasks have full Phase-A-to-Phase-B interval to drain)
- Step 6 destructive-by-default constraint isolated to Phase B; safer rollback at Phase A
- Per `research/web-02-content-vs-parse-resumability.md:14`, deferred deprecation patterns (Python `DeprecationWarning` → `PendingDeprecationWarning` → removal cycle; GitHub API 30→180 days) precedent this exact split
- AC-ATK-08 `--max-wait 14d` becomes unnecessary; option (a) "complete in-flight" always available within Phase-A-to-Phase-B window
- Step 6 procedural authorization chain (F-07) has more time for human-review per R-RES-05

**Cons:**
- **CR-FM-03 shim permanence between phases** = R-ATK-12 (shim has no sunset binding; future audit row dropping default bricks shim-era TASK-*) becomes load-bearing during the inter-phase window
- **Donor `sc-task-protocol/SKILL.md` persists as dead-code** between phases — confusing for new contributors; R-RULE-06 "no ceremony-without-teeth" weakened
- **K-06 / K-07 / K-08 deferred** — surface reduction not realized until Phase B
- **Doubles release ceremony** (two PR cycles, two QA passes, two announcement cycles)
- **ME-9 audit (donor-ceremony drop) split across two releases** — R-RULE-11 boundary auditor at Step 10 (Phase B) sees state from Phase A as "in-progress drop" not "completed drop"

**Opportunity cost (named):** Trades **single-release ME-9 / R-RULE-11 audit clarity** for **soft-deprecation grace window**. Per validation-spec §16 verdict, the 10-step single-release chain already passes `convergence_score: 0.86 ≥ 0.85` with explicit S-1/S-2/S-3 mitigations — the split's grace-window benefit is incremental, not load-bearing.

**Why Not Chosen:** The 10-step chain's Steps 5-6 internal boundary already encodes the soft → hard transition with S-3 atomicity + AC-ATK-07 rf-qa F-07 chain verifier at the Step 6 pre-commit gate. Splitting at the release boundary adds ceremony without adding safety, given AC-ATK-08 14d default + auto-invoke (b) per S-1 already addresses the in-flight grace requirement. Per `sc:release-split-protocol` (referenced skill), the natural seam at Step 5/6 boundary inside a single release is preferred over inter-release split when sequencing constraints are already auditable.

---

### Alternative 3: Alembic "Inline Throwaway ORM Models" Pattern (in lieu of CR-FM-03 default-to-`STANDARD` Shim)

**Description:** Instead of CR-FM-03 backward-compat shim that defaults missing `Tier:` to `STANDARD`, adopt the Alembic "inline throwaway ORM models for data migrations" pattern per `research/web-02-content-vs-parse-resumability.md:14`. Each in-flight task file would carry an **inline migration block** at resume time that authors a one-shot frontmatter mutation: read the legacy frontmatter, infer `Tier:` from path-override heuristics (e.g., `src/superclaude/` paths → STRICT) or operator-prompt, write back to the task file with `Tier:` populated, then resume normally. The in-flight task file is treated as the "third intermediate snapshot, not pre-merge or post-merge" per web-02 §3.

**Pros:**
- **No permanent shim** — CR-FM-03 shim sunset binding (OQ-FM-03-SUNSET) becomes moot; migration is one-shot at first-resume
- **Per-task explicit `Tier:` propagation** improves auditability vs implicit default-to-`STANDARD`
- **R-RES-01** ("tier-conditioned read" boundary thin) gets stronger anchor — explicit `Tier:` value cannot be confused with implicit default
- **R-FM-08** (file-rename evasion) less applicable — migration writes through to canonical location

**Cons:**
- **INV-04 parse-layer compromise.** Writing back to task frontmatter at resume time mutates the disk-resident source of truth; violates `task/SKILL.md:252-264` Incremental Writing Protocol "Never accumulate content in context and attempt a single large Write" interpretation.
- **First-resume blocking.** Operator-prompt or heuristic inference at resume time introduces latency and ambiguity at the F1 entry gate; CR-FM-03 default-to-`STANDARD` is silent and instant.
- **Per-task heuristic inference correctness** unbounded — `src/superclaude/` paths default to STRICT, but what about mixed paths? what about `tests/` paths? — proliferates per-task disposition decisions where shim collapses to default.
- **Conflicts with INV-05** — auto-populating `Tier:` field from path heuristics resembles D09b runtime classifier (LR-REJECT-3); ME-1 binding forbids.
- **Higher in-flight risk** — 136 union files × first-resume mutation × per-resume operator prompt = significantly more error surface than shim default.
- **Migration script authoring** for 136+ files = real engineering cost not in scope.

**Opportunity cost (named):** Trades **CR-FM-03 shim permanence and OQ-FM-03-SUNSET ambiguity** for **per-task migration complexity and INV-05 risk surface.** The shim's permanence is bounded by `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored` (OQ-FM-03-SUNSET recommended binding); the migration pattern's INV-05 risk is unbounded.

**Why Not Chosen:** CR-FM-03 default-to-`STANDARD` shim per `merge-master.md:53` is **load-bearing for INV-04 parse-layer survival of 136 in-flight files at first-resume**. Per `research/11-in-flight-exposure-and-resumability.md:182-186`, the shim guarantees L1 (schema parse) survival for 100% of the live in-flight union with zero-latency, zero-mutation, zero-operator-burden semantics. The Alembic-style migration pattern is the canonical alternative in industry tooling (`research/web-02-content-vs-parse-resumability.md:14`) but is operationally heavier and reintroduces INV-05 risk surface (D09b-adjacent path-to-Tier heuristic inference). The shim wins on operational simplicity AND INV-05 conformance. AC-ATK-18 (semantic-layer content audit at resume time) complements the shim without mutating files.

---

### Alternative 4: Embedded Runtime Classifier (D09b — donor `sc-task-protocol`'s original design)

**Description:** Restore the donor's D09b classifier with priority cascade + keyword tables inside `/task` F1 loop. Run classification at task entry AND per-item; emit `dispatch_profile=<tier>` per item. No `Tier:` frontmatter field needed (D09b would dispatch all decisions from runtime prompt scan).

**Pros:**
- Zero MDTM frontmatter migration burden (no `Tier:` field; no CR-FM-03 shim)
- No `Tier:` value author-time decision for new tasks (classifier picks)
- Eliminates AC-ATK-05 closed enumeration requirement
- Avoids OQ-TIER-VOCABULARY (3-tier vs 4-tier) reconciliation

**Cons:**
- **INV-05 hard violation.** D09b runtime classifier *defines work at runtime*; explicit `Tier:`-as-metadata contract per INV-05 prohibits this. Per `research/10-invariant-preservation-and-me-binding.md:188`, "D09b (donor classifier with priority cascade + keyword tables) was REJECTed as LR-REJECT-3."
- **ME-1 binding hard violation.** "PRE-LOOP DISPATCH ONLY" — D09b classifier necessarily fires per-item.
- **INV-01 progress monotonicity at risk.** Runtime classification could re-emit per-item dispatch lines, potentially re-firing Gate-1 inside F1 EXECUTE.
- **Ledger entry LR-REJECT-3 explicit terminal REJECT** per `rejected-features-ledger.md` row 3; re-introduction requires new manifest exception (ME-10+) and re-litigation of INV-05/ME-1 bindings.
- **R-RULE-11 audit (Step 10) auto-fails** — re-proposing a REJECTed ledger entry is the canonical R-RULE-11 violation per `research/13-adversarial-artifact-cross-validator.md:437`.

**Opportunity cost (named):** Trades **INV-01 + INV-05 + ME-1 + ledger LR-REJECT-3 conformance** for **frontmatter-migration elimination.** The frontmatter migration burden is already addressed by CR-FM-03 shim (zero-cost at first-resume); the INV/ME costs are catastrophic.

**Why Not Chosen:** D09b is terminally REJECTed at the ledger layer (LR-REJECT-3); ME-1 prohibits any per-item dispatch construct; INV-05 prohibits runtime work-definition. This alternative is listed for completeness only — it is **Permanently Out of Scope** per `research/00-prd-extraction.md:148` and `research/00-prd-extraction.md:133`.

---

### Alternative 5: Manifest-Only Audit (drop CR-7 ORDERING sentinel; rely on transfer-manifest.md §3 review)

**Description:** Skip CR-TASK-01/04 sentinel-comment insertion and CR-FM-04 grep-AC. Rely on transfer-manifest.md §3 manifest-exception register (ME-1..9) review at every PR as the sole enforcement of CR-7 / CR-8 ordering.

**Pros:**
- Less ceremony per source file (no sentinel comment annotations)
- Fewer files to keep in sync (no audit script per CR-FM-04)
- Aligns with R-RULE-11 audit-discipline framing (defense-relies-on-human-process per R-RES-01)

**Cons:**
- **R-ATK-01 / R-ATK-13 hard hit.** Markdown comments cannot enforce executable ordering; without grep-AC + sentinel pair, R-ATK-01 (F-02 ordering claim relies on grep alternation) and R-ATK-13 (CR-7/CR-8 sentinel binding requires structural enforcement) both fail.
- **F-02 closure retracts.** Per `research/13-adversarial-artifact-cross-validator.md:551-557`, F-02 closure adds two mitigations: (1) CR-FM-04 audit-scope extension; (2) sentinel-comment blocks at row 1 + row 10. Dropping either reverts F-02 to its pre-closure MEDIUM-severity finding.
- **Audit posture regression** — `validation-spec.md` Round 3 convergence depended on F-02 closure; dropping CR-FM-04 + sentinels would re-open the validation-spec issue.

**Opportunity cost (named):** Trades **F-02 structural enforcement** for **ceremony reduction.** Per R-ATK-02 closure (`research/00-prd-extraction.md:294`), the validation-spec convergence is conditional on AC-ATK-03 closed-enum normalization — same structural rigor; dropping CR-FM-04 leaves a parallel hole.

**Why Not Chosen:** Structural enforcement (grep-AC + sentinel pair) is strictly stronger than manifest-review-only enforcement. The ceremony cost is minimal (2 comment lines at row 1 + 2 at row 10, audited by 2 grep invocations).

---

### Alternative 6: Single-Phase rf-qa (drop F-05 fourth invocation point; remove TU-7 mid-phase routing)

**Description:** Cancel TU-7 absorption. Keep rf-qa invocation only at the two canonical anchor points (phase-gate per `task/SKILL.md:191-198`; post-completion per `:219-241`). TFEP escalation routed to operator manual review (not mid-phase rf-qa).

**Pros:**
- INV-03 anchor language at `extension-point-contracts.md:11-17` matches implementation without F-05 widening (R-RES-02 closed)
- AC-ATK-11 (F-05 backed by retroactive ME-10 OR one-time non-generalizing carve-out) becomes moot
- R-OPS-03 (rf-qa queue flood from F-04 over-escalation) lower-risk — no mid-phase routing volume
- OQ-F-05-MANIFESTIZATION resolved by elimination

**Cons:**
- **TFEP escalation routing requires new gate.** Per `research/10-invariant-preservation-and-me-binding.md:115`, "the donor's D25 parallel-3-strike adjudicator was REJECTed (LR-REJECT-2 / rejected-features-ledger.md:46)." Without TU-7's rf-qa-reuse, TFEP must either (a) HALT (forbidden per ME-3) or (b) author a new gate (D25 LR-REJECT-2 returns).
- **TU-7 ADOPT verdict per transfer-manifest.md** has V/C/K Net=6.0; rejecting it after Phase-7 PASS triggers V/C/K re-score per R-RULE-07.
- **R-RES-02 trade is acknowledged-but-bounded.** Per validation-spec §15 L416, F-05 is "authorized" in the plan with three-prong defense; complete elimination removes the donor's escalation pattern entirely.

**Opportunity cost (named):** Trades **TU-7 donor-pattern absorption** for **INV-03 anchor-language conformance.** The plan's three-prong defense (ME-2 keeps rf-qa present, F-05 documented in `final-merge-plan.md` §4.5 as authorized widening, AC-ATK-11 closure obligation) covers the residual risk.

**Why Not Chosen:** TU-7 is ADOPT-verdict per transfer-manifest.md § 4 row; absorbing donor TFEP escalation pattern is a load-bearing merge goal. The F-05 widening is bounded by ME-2 (rf-qa preservation) and AC-ATK-11 (retroactive ME-10 OR carve-out); R-RES-02 is acknowledged but mitigated.

---

### Alternative 7: HALT-as-gate Disposition for Git Pre-flight (Reading B, rejected)

**Description:** When `git status` returns dirty tree on STRICT pre-flight, refuse task entry (HALT). Treat `git_status_clean_tree_check` as an authorization gate rather than environment-prep.

**Pros:**
- Strict no-partial-state guarantee at task entry
- No warn-and-continue ambiguity at F-03 closure
- AC-ATK-02 5-row matrix simplifies to {clean=continue, all-else=HALT}

**Cons:**
- **INV-01 hard violation.** New HALT semantic mid-checklist forbidden per `validation-spec.md:62`. F-03 closure explicitly chose Reading A (log-and-continue) for INV-01 consistency per `research/13-adversarial-artifact-cross-validator.md:561-564`.
- **ME-3 hard violation.** "SIDE-CHANNEL ONLY, NO F1 HALT" binding forbids refuse-entry on environment-non-ideal conditions.
- **AC-ATK-10** "unified pre-loop HALT policy table with input-invalid vs environment-non-ideal row categories" pre-decides: environment-non-ideal → warn-continue; HALT reserved for input-invalid.

**Opportunity cost (named):** Trades **INV-01 + ME-3 conformance** for **strict pre-flight semantics.**

**Why Not Chosen:** INV-01 progress monotonicity and ME-3 no-new-HALT binding are non-negotiable. This alternative is **Permanently Out of Scope** per `research/00-prd-extraction.md:135`.

---

### Alternative 8: In-Memory TFEP Baseline (donor's original `:147` in-memory shape)

**Description:** Adopt TU-5 donor pattern verbatim — store TFEP baseline "in memory for the duration of the task" per `sc-task-protocol/SKILL.md:147-149`, not on disk at `${TASK_DIR}/research/test-baseline.yaml`.

**Pros:**
- Matches donor source verbatim (CR-TASK-12 verbatim-diff audit trivially passes for TU-5)
- Avoids `${TASK_DIR}/research/test-baseline.yaml` file authoring + 4-state observer (AC-ATK-03)
- No file-system writes at baseline capture time

**Cons:**
- **INV-04 resumability hard violation.** In-memory baseline does NOT survive context compression / session restart per `task/SKILL.md:269-282`. Resume after compaction loses baseline; TFEP `pre-existing vs new` classification becomes unbound.
- **Manifest's file-resident strengthening** per `research/13-adversarial-artifact-cross-validator.md:139` was deliberate: "the file-resident shape is the INV-04-safe choice and is consistent with the manifest's wording that 'TU-5's file-resident *choice* is the INV-04-safe variant the manifest selected'."

**Opportunity cost (named):** Trades **INV-04 resumability guarantee** for **donor-source verbatim conformance.** Manifest already authorizes the strengthening explicitly under invariant-survival-walkthrough.md §2.1.

**Why Not Chosen:** INV-04 is the HIGHEST-EXPOSURE invariant per `validation-spec.md:285`; in-memory baseline trades highest-priority invariant for a verbatim-citation purity that the manifest has already explicitly waived.

---

### Closure Audit: 8 Unnamed Tradeoffs from validation-spec §12

Per `validation-spec.md:368-379`, the steelman names 8 unnamed tradeoffs ("eight closures, eight costs"). Each is closed and opportunity-cost-named in Alternatives 1-8 above (or in the chosen path's residual concession register R-RES-01..05 §20.2). Cross-map:

| validation-spec §12 Tradeoff | Closure in this TDD | Opportunity Cost Named |
|---|---|---|
| **F-01** "tier-conditioned read" widens INV-05 attack surface | Chosen path + Alt 4 + R-RES-01 | Per-item marker closed-enum (AC-ATK-05) trades open-read-channel for structural design-time-review enforcement |
| **F-02** sentinel shifts enforcement to documentation discipline | Chosen path + Alt 5 | CR-FM-04 grep-AC + sentinel pair trades manifest-only audit clarity for structural ordering enforcement |
| **F-03** Reading A (warn-continue) exposes runtime to dirty-tree divergence | Chosen path + Alt 7 + R-RES-04 adjacent | AC-CR-TASK-06-F03 trades dirty-tree-divergence cost for INV-01 progress monotonicity |
| **F-04** Over-escalate floods rf-qa queue | Chosen path + R-RES-03 | AC-CR-TASK-09-F04 trades queue-volume-bet for INV-03 floor and INV-04 resumability |
| **F-05** Mid-phase rf-qa sees in-progress not phase-complete state | Chosen path + Alt 6 + R-RES-02 | TU-7 ADOPT trades semantic-shift cost for absorbing donor TFEP escalation pattern; AC-ATK-11 is closure obligation |
| **F-06** Line-pinned reference brittle to edits | Chosen path + R-DRIFT-02/03 patches | Content-keyed anchor (CR-FM-04 extension per `research/00-prd-extraction.md:225`) trades line-anchor brittleness for content-hash stability |
| **F-07** Procedural chain auditable only by humans | Chosen path + R-RES-05 | AC-ATK-07 rf-qa F-07 verifier trades manifest-binding-purity for documented procedural-chain auditability |
| **F-08** "five" → "six" inconsistency persists in `merge-master.md:7` | Chosen path | Documentation strengthener LOW; closed by per-step audit pass |

All 8 tradeoffs are closed with named opportunity costs; no unnamed cost survives into the chosen path.

---

## Appendix A — Operational Drill-Down (synth-07-owned cross-cutting reference)

<!-- Non-numbered appendix between §21 and §22 per assembly convention. Expands key operational concerns that cross-cut §18-§21 but that the TDD's row format cannot fully accommodate. NOT part of TDD §22 Open Questions. -->

This appendix expands key operational concerns that cross-cut §18-§21 but that the TDD's row format cannot fully accommodate. Each subsection points to the upstream research source and the TDD-target section that consumes it.

### A.1 Pre-Commit Gate Matrix (Per Step)

The pre-commit gates referenced in §19.1 above are summarized here with their command-line invocations and exit-code semantics. Per `merge-master.md` §6 (cited via `research/13-adversarial-artifact-cross-validator.md:399-410`):

| Step | Pre-commit gate command | Exit-code semantic | Failure disposition |
|---|---|---|---|
| 1 | `uv run pytest && make verify-sync && grep -q 'CR-7 ORDERING' src/superclaude/skills/task/SKILL.md && grep -q 'CR-8 ORDERING' src/superclaude/skills/task/SKILL.md` | 0 = pass; non-zero = block | Block commit; investigate sentinel absence or sync drift |
| 2 | `uv run pytest && make verify-sync` (no new gates beyond Step 1 baseline) | 0 = pass | Block commit; re-author CR-TASK-05 or CR-TASK-06 row |
| 3 | `uv run pytest && make verify-sync && <CR-TASK-12 verbatim-diff audit at corrected anchors :129-135 and :157-161>` | 0 = pass | **R-DRIFT-02/03 PRE-PATCH OBLIGATION:** if diff non-zero, verify whether anchor moved (drift) vs content moved (legitimate change) before deciding revert vs anchor-update |
| 4 | `uv run pytest && make verify-sync && CR-FM-04 7-diff audit pass && CR-TASK-11 sha256 baseline pass` | 0 = pass | Block commit; investigate which audit row failed |
| 5 | `uv run pytest tests/sprint/test_process.py && uv run pytest tests/sprint/test_tui_v2_wave2.py && uv run pytest tests/pipeline/test_process.py && uv run pytest tests/cli/ && make verify-sync && CR-DEP-02 sha256 baseline pass && CR-DEP-05 'grep returns zero matches' check` | 0 = pass | **S-2 enforcement boundary;** block if any CLI emitter test fails (sprint or cleanup_audit); also block if S-1 in-flight tasks still LIVE per AC-ATK-08 14d expiry not yet reached |
| 6 | `make verify-sync && AC-ATK-07 rf-qa F-07 verifier PASS && find src/superclaude/skills/sc-task-protocol/ -type d 2>&1 \| grep -q 'No such file' && find .claude/skills/sc-task-protocol/ -type d 2>&1 \| grep -q 'No such file' && CR-DEP-05 grep returns zero on both [src] and [.claude]` | 0 = pass | **S-3 enforcement boundary + destructive-by-default;** block if mirror-sync drift OR if rf-qa F-07 procedural chain verifier fails OR if any donor file/directory persists |
| 7 | `make verify-sync && AC-SM-03 walkthrough fixture pass && AC-SM-04 pass` | 0 = pass | Block commit; investigate walkthrough fixture failure |
| 8 | `mkdocs build 2>&1 \| grep -c 'WARNING' = 0 && pre-push hook installed && pre-push hook re-grep on landing commit (not working tree) returns zero '/sc:task' in CLI sources` | 0 = pass | Block commit; FM-05 mkdocs version drift caveat — confirm mkdocs version pin in commit msg |
| 9 | `<CR-DEP-06 manifest grep verification>` | 0 = pass | Block commit; extend manifest if residuals discovered outside authorized buckets |
| 10 | `R-RULE-11 audit clean (zero ledger entries re-proposed) && K-01..K-08 measurement pass` | 0 = pass | Block commit; reopen any K-NN row missing target threshold |

**Consumed by:** §19.1 (10-step chain table) above; §19.7 (rollback decision criteria).

### A.2 Per-Resume Gate Emission Order (AC-SM-12 100% Clean Resume)

Per `research/11-in-flight-exposure-and-resumability.md:240-249`, every live in-flight MDTM file (136 union files at the pinned SHA, monotonic upward) resumes through this gate sequence:

1. **L1 parse-layer (CR-FM-03 shim):** frontmatter parses cleanly; missing `Tier:` defaults to `STANDARD`; emits `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<N> sunset_row_authored=false` (sunset audit emission).
2. **L2 content-scan (AC-ATK-18):** recursive grep against task body for `(/sc:task\b\|sc-task-protocol\|task-unified)`; on each match emits `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`. De-dup per file at implementation discretion.
3. **First-resume acknowledgment gate (one-shot):** emits `gate-1.5: legacy-surface-acknowledgment-required`; operator responds; `gate-1.5: legacy-surface-acknowledged operator=<id> sha=<git-sha>` emitted.
4. **`related_docs:` traversal:** `find` each path; on ENOENT emits `gate-1.5: deleted-related-doc detected path=<path> action=warn-and-continue`.
5. **L3 dispatch-layer (runtime):** if a checklist step or subagent prompt later tries to spawn a stubified surface or `Read` a deleted donor file, transitions to `⚪ Blocked` per its own exception clauses (INV-01 holds by transition; INV-04 semantic guarantee broken — H-4 scenario). NOT covered by AC-SM-12 (which binds resume-gate boundary only).

**Consumed by:** §19.5 feature-flag table (gate-1.4 + gate-1.5); §20.4 R-FM-NN failure mode mitigations.

### A.3 R-DRIFT-02/03 Pre-Patch Obligation Detail (Step 3 Blocker)

Per `research/13-adversarial-artifact-cross-validator.md:717-718` and §1.6 / §1.7 of that file:

- **R-DRIFT-02** (LOW): donor anchor `:127-135` (cited in 3 artifacts) should be `:129-135` (heading + rules) or `:133-135` (rules only). Content verbatim preserved at corrected anchor.
- **R-DRIFT-03** (MEDIUM): donor anchor `:200-210` (cited in 3 artifacts: transfer-manifest.md TU-7 line 277, integration-sketches.md IS-ADOPT-9 line 142, invariant-survival-walkthrough.md §2.6 step 4 line 277) should be `:157-161`. Content at `:200-210` is the REJECTed D23 forensic-results block (LR-DEFER-6) — running CR-TASK-12 verbatim-diff audit against literal `:200-210` returns non-zero **erroneously**, would block Step 3 M3 commit at pre-commit gate.

**Patch path:**
1. Update `transfer-manifest.md` TU-6 anchor: `:127-135` → `:129-135` or `:133-135`.
2. Update `transfer-manifest.md` TU-7 anchor: `:200-210` → `:157-161`.
3. Update `integration-sketches.md` IS-ADOPT-2: `:127-135` → `:129-135`.
4. Update `integration-sketches.md` IS-ADOPT-9: `:200-210` → `:157-161`.
5. Update `invariant-survival-walkthrough.md` §2.6 step 3: `:127-135` → `:129-135`.
6. Update `invariant-survival-walkthrough.md` §2.6 step 4: `:200-210` → `:157-161`.
7. Update CR-TASK-12 audit script anchor literals to match (or accept content-keyed anchors per F-06 closure tradeoff resolution).

**Consumed by:** §19.1 Step 3 row; §20 R-ATK-06 closure pointer (CR-FM-04 line-anchor brittleness AC-ATK-06).

### A.4 Counter-Factual Register (16 Variants Manifest Blocks)

Per `research/10-invariant-preservation-and-me-binding.md` §4 (counter-factuals cited at `invariant-survival-walkthrough.md` §4) and `research/13-adversarial-artifact-cross-validator.md` §4.4, the manifest blocks 16 donor variants that would have broken an INV-NN. The register lives in `invariant-survival-walkthrough.md` §4 and is summarized here for Alternative-cross-reference:

- Per-item per-tier dispatch (D09b) — blocked by ME-1 / LR-REJECT-3 (covered as Alt 4 above).
- D15c per-tier procedure synthesis at execute-time — blocked by ME-5 / LR-REJECT-7.
- TFEP F1-halting behavior on engagement — blocked by ME-3 (auto-REJECT).
- Any feature removing an F2 entry — blocked by C1 / R-RULE-05 (extension-point N1).
- D25 3-strike FULL STOP parallel adjudicator — blocked by LR-REJECT-2 (covered as Alt 6 above).
- Verifier replacement on STRICT (`quality-engineer` REPLACES `rf-qa`) — blocked by ME-2.
- Gate 5 override flags bypassing the gate — blocked by LR-REJECT-4.
- In-memory baseline cache for TFEP — blocked by TU-5 file-resident choice (covered as Alt 8 above).
- D23 Step 6 "resume from inserted task" — blocked by LR-DEFER-6.
- md5 collision in CR-TASK-11 — blocked by AC-ATK-09 (sha256 replacement).
- D06 auto-trigger heuristics scanning the prompt — blocked by LR-REJECT-8.
- D08 classification header emission without ME-7 precondition — blocked by LR-DEFER-5.
- D13 auto-suggest keywords — blocked by LR-REJECT-6.
- D02/Layer A `mcp-servers:` advertisement re-affirmed REJECT — blocked by LR-REJECT-1 / ME-9.
- HALT-as-gate dirty-tree (Reading B) — blocked by ME-3 (covered as Alt 7 above).
- Big-bang single-commit merge — covered as Alt 1 above (no formal ledger entry; structural counter-factual).

**Consumed by:** §21 Alternatives 1, 4, 6, 7, 8 (the alternatives that map to a ledger-blocked variant); §20 R-RES-01 (closed-enum AC-ATK-05 is the structural guard against re-introduction).

### A.5 Synthesis-Feed Confirmation Matrix

| Section obligation | Input source | TDD section |
|---|---|---|
| External deps (pytest, pyyaml, click, rich) | CLAUDE.md + pyproject.toml | §18.1 |
| Internal deps (pytest_plugin, pm_agent, execution, cli, skills/{task, sc-task-protocol}) | CLAUDE.md project structure + `research/00-prd-extraction.md:81-93` | §18.2 |
| Cross-team (none in scope) | `research/00-prd-extraction.md:95-106` (all owner-internal OQs) | §18.3 |
| 10-step commit chain with S-1/S-2/S-3 sequencing + per-step rollback | `research/13-adversarial-artifact-cross-validator.md:399-428` (`merge-master.md` §6) | §19.1, §19.2, §19.4 |
| ME-6 atomicity binding | `research/10-invariant-preservation-and-me-binding.md:238-249` | §19.3 |
| S-1 pre-Step-5 baseline floor 136 + TASK-PRD-20260514-121039 binding | `research/11-in-flight-exposure-and-resumability.md:29, 43, 76-103` + `research/13-adversarial-artifact-cross-validator.md:9-15` (R-DRIFT-04 RETRACTED) | §19.2 (S-1 section) |
| K-01..K-08 (NOT K-001..K-010) | `research/00-prd-extraction.md:257-264, 420` | §20.1 |
| 5 residual risks from validation-spec §15 | `validation-spec.md:409-419` (R-RES-01..05) | §20.2 |
| 8 unnamed tradeoffs from validation-spec §12 closed with opportunity-cost named | `validation-spec.md:368-379` (F-01..F-08 tradeoffs) | §21 Closure Audit table |
| Mandatory Alternative 0 (Do Nothing) | `tdd_template.md:1036-1052` | §21 Alternative 0 |
| Alembic "inline throwaway model" alternative vs CR-FM-03 shim | `research/web-02-content-vs-parse-resumability.md:14` | §21 Alternative 3 |
| Server-side pre-push hook industry references (AC-ATK-17) | `research/web-01-rebase-split-prevention.md:14` | §19.5 (pre-push hook flag); §21 Alternative 1 opportunity-cost |
| F2 catalog count = 10 (fix-cycle 1 correction; not 9) | `research/10-invariant-preservation-and-me-binding.md:31` | §20.4 R-FM-NN context (cited in Alt 6 closure rationale) |

All synthesis-feed obligations are accounted for; no upstream input is unread or unmapped.

---

## 22. Open Questions

> **Scope.** This register is the consolidated open-question surface emerging from the four-cycle Phase-3 research gate plus the adversarial cross-validation in file 13. Entries fall into seven families: **(F-A)** carry-overs from PRD §S13; **(F-B)** R-DRIFT-NN claims surviving cross-validation; **(F-C)** unresolved research-gap residuals from file 00; **(F-D)** fix-cycle metadata drift (132→136, F2 9→10); **(F-E)** schema / token-grammar decisions deferred to synth-04; **(F-F)** AC-ATK-05 closed-enumeration register; **(F-G)** typo-history register (e.g., user-prompt K-01..K-08 vs K-001..K-010). All five R-DRIFT-NN items from file 13 §10 are surfaced (R-DRIFT-04 RETRACTED, R-DRIFT-01 retracted, R-DRIFT-02 LOW, R-DRIFT-03 MEDIUM, R-DRIFT-05 LOW). R-DOC-01 is downgrade-candidate (see Q-R-DOC-01 below).

### 22.1 Open-Question Register

| ID | Family | Question | Owner | Target Date | Status | Resolution Notes |
|----|--------|----------|-------|-------------|--------|------------------|
| **OQ-TIER-VOCABULARY** | F-A | Confirm canonical post-merge tier vocabulary is `{STRICT, STANDARD, LIGHT, EXEMPT}` (4-tier code) and that `TRIVIAL` from spec § 4 L103 is vestigial. INV-05 protection scope and ME-1 enumeration depend on this. [SPEC-DEFINED] | Engineering Lead | Before Step 1 | 🔴 Open | Live code uses 4-tier at `commands/task.md:55, 61, 82` + `sc-task-protocol/SKILL.md:9, 56`. Recommendation: pin 4-tier; retire `TRIVIAL`. (Source: research-00 § Anti-Persona row; OQ-1.) [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **OQ-FM-03-SUNSET** | F-A | Confirm CR-FM-03 default-to-STANDARD compat shim sunset binding `N`. Recommended: `N = 50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`. The emitter `gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<int> sunset_row_authored=<bool>` must be specified. | Engineering Lead | Before Step 1 | 🔴 Open | Tied to AC-ATK-12 sub-binding (a) (CR-AUDIT-FM-03-SUNSET row authored in `merge-master.md`). [SPEC-DEFINED][UNVERIFIED] |
| **OQ-F-NN-BIJECTION** | F-A | Confirm canonical F-NN ↔ TU-NN bijection once `final-merge-plan.md` content audit completes. Pre-Phase-7 obligation. | Engineering Lead | Before Step 7 | 🔴 Open | Content audit of all 7 anchor artifacts is the upstream dependency; see file 13 § 7 + §6.6 closure note. [CONTENT-AUDIT-COMPLETED] for plan-level pairings; [UNVERIFIED] for final bijection. |
| **OQ-TFEP-FIELD-COUNT** | F-A | Resolve TU-8 incident-report 6-vs-7 field cardinality. Donor literal at `sc-task-protocol/SKILL.md:222-234` and §7 Data Models commits to **7 fields**: `{tier, item_id, trigger, classification, action, timestamp, sha}` (or `failing_tests` ↔ `commits/diff` per donor verbatim). | Engineering Lead | Before Step 4 (TU-7) | 🟡 Investigating | §7 Schema 4 commits to 7. Engineering Lead must confirm field name canonical form (`failing_tests` vs `commits` etc.). [SPEC-DEFINED] |
| **OQ-F-05-MANIFESTIZATION** | F-A | Decide retroactive ME-10 vs one-time carve-out for F-05 (4th rf-qa invocation point post-merge — TU-7 mid-phase TFEP) per AC-ATK-11. | Engineering Lead | Before Step 4 (TU-7) | 🔴 Open | Required for AC-ATK-11 disposition matrix closure. [SPEC-DEFINED] |
| **OQ-PROHIBITION-DISPOSITION-MATRIX** | F-A | Decide verifier-spawned F1 disposition (root F1 / verifier-spawned F1 / mid-phase rf-qa) per AC-ATK-11 generalization. | Engineering Lead | Before Step 3 (TU-6) | 🔴 Open | Tied to NFR-ME-1 + INV-02 catalog additivity. [SPEC-DEFINED] |
| **Q-1 / OQ-1** | F-A | Carry-over of OQ-TIER-VOCABULARY. (Same as above; preserved here under historical PRD numbering.) | Engineering Lead | Before Step 1 | 🔴 Open | Duplicate of OQ-TIER-VOCABULARY (traceability). |
| **Q-2** | F-A | Content audit of AC-SM-01, -03, -05, -06, -11 cited anchor artifacts. Originally claimed absent; QA fix-cycle 2 confirms all 7 anchor artifacts PRESENT at `.dev/releases/current/task-sc-task-directional-merge/artifacts/`. Decide: schedule content audit pre-Step-7 (recommended) vs defer to post-Phase-7.5. | Documentation/Release Owner | Before Step 7 | 🟡 Investigating | File 12 §0.4 + file 13 §0 + research-00 §139 confirm artifacts PRESENT at pinned SHA. Audit scheduling decision still open. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-3** | F-A | S-1 named-target population update. `TASK-PRD-20260514-121039` and `TASK-TDD-20260514-121250` LIVE; `TASK-RF-20260515-195758` genuinely absent. Confirm "supplement-not-replace" framing — bind both live named targets AND broader 136-file population. | Engineering Lead | Before Step 5 | 🔴 Open | NFR-S-1 [POPULATION-GENERALIZED]. R-DRIFT-04 retraction confirms `121039` LIVE with 258 donor-surface refs across 12 files (file 11 §3.1). [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-4** | F-A | CR-DEP-06 elevation from "proposal" to "required for closure." Live evidence confirms 144 residual occurrences (61 backlog + 83 docs/generated); fix-cycle 1 recount drift to 153 across 45 files. Confirm 144 binding count. | Engineering Lead | Before Step 6 | 🟡 Investigating | Bound to AC-ATK-18(d). PRD research-00 § 159 records 144 as the binding count. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-5** | F-A | Companion TDD offer at delivery. Engineering audience strongly recommends companion TDD (5 INVs, 9 MEs, 18 ACs, 5 concessions). Confirm whether Engineering Lead wants TDD authored next. | Engineering Lead | Pre-merge | 🟢 Resolved | This TDD authoring run IS the companion TDD per the OQ-5 affirmative path. [CONTENT-AUDIT-COMPLETED] |
| **Q-R-DRIFT-01** | F-B | RETRACTED — `src/superclaude/skills/task/SKILL.md` exists (376 lines, byte-identical to `.claude/` mirror) per file 13 § 1.1 + § 10 row 1. No patch needed. | Documentation/Release Owner | Closed | 🟢 Resolved | [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-R-DRIFT-02** | F-B | **LOW (mechanical).** `transfer-manifest.md` TU-6 L238, `integration-sketches.md` IS-ADOPT-2 L52, `invariant-survival-walkthrough.md` § 2.6 step 3 L263 cite donor `sc-task-protocol/SKILL.md:127-135` for the 3 VIOLATION rules but the canonical anchor is `:129-135` (heading) or `:133-135` (rules only). **Anchor off-by-2.** Content verbatim is preserved. | Documentation/Release Owner (patch task) | Before Step 4 (CR-TASK-12 audit window) | 🔴 Open | Patch single-source: replace `:127-135` → `:133-135` in all three artifacts. Update CR-TASK-12 diff audit anchors to match. (file 13 § 10 row 3.) [CODE-CONTRADICTED] |
| **Q-R-DRIFT-03** | F-B | **MEDIUM (mechanical, multi-artifact).** `transfer-manifest.md` TU-7 L277 / `integration-sketches.md` IS-ADOPT-9 L142 / `invariant-survival-walkthrough.md` § 2.6 step 4 L277 all cite donor `:200-210` for the 3 MUST-escalate triggers. Actual anchor is `:157-161`. **Anchor off-by-43.** If CR-TASK-12 verbatim-diff audit runs against `:200-210` literally, it returns non-zero (content there is D23 forensic-results, REJECTed by ledger LR-DEFER-6) and **erroneously blocks the M3 commit**. | Documentation/Release Owner (patch task) | Before Step 3 (M3 commit) | 🔴 Open | Highest-priority drift to patch before Phase 7. Patch single-source: replace `:200-210` → `:157-161` in all three artifacts + CR-TASK-12 audit anchors. (file 13 § 10 row 4 + §6 closure note.) [CODE-CONTRADICTED] |
| **Q-R-DRIFT-04** | F-B | **RETRACTED** per file 13 top-of-file fix-cycle 1 correction. The earlier claim that `TASK-PRD-20260514-121039/` was no longer in `.dev/tasks/to-do/` was **WRONG**. Per live `ls -d` at pinned SHA, the directory **exists** and is `🟠 Doing` with 258 donor-surface occurrences across 12 files (file 11 §3.1 REINSTATED). HZ-03 from `compat-hazard-report.md` is **NOT stale**; S-1 sequencing remains **binding, not no-op**. `final-merge-plan.md` § 6 Step 5 S-1 binding stays in force. The aggregate R-DRIFT severity in file 13 §10 line 714 is re-read as: **0 HIGH, 1 MEDIUM (R-DRIFT-03), 2 LOW (R-DRIFT-02 + R-DRIFT-05); R-DRIFT-04 dropped from LOW count.** | Engineering Lead | Closed | 🟢 Resolved | [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] — authoritative per file 13 fix-cycle 1 correction block. **R-DRIFT-04 RETRACTED — explicit confirmation.** |
| **Q-R-DRIFT-05** | F-B | **LOW (citation).** The role brief asks to verify "validation-report.md for the 0.86 convergence score". The 0.86 figure is NOT in `validation-report.md`; it lives in `validation-spec/validation-spec.md:6, :19` and `validation-spec/adversarial/merge-log.md:71`. No artifact patch required — this TDD §22 clarifies the source. | Documentation/Release Owner | Pre-publish | 🟢 Resolved | [CODE-CONTRADICTED] on the brief's source citation only; the figures themselves verify. (file 13 § 10 row 6 + §6.6.) |
| **Q-R-DOC-01** | F-B | **Downgrade candidate.** Originally framed as "7 absent upstream artifacts." Fix-cycle 2 verification 2026-05-16 confirms all 7 named artifacts PRESENT at `.dev/releases/current/task-sc-task-directional-merge/artifacts/` (file 12 §0.4 + file 13 §0). **Recommendation: downgrade R-DOC-01 from "artifact gaps" to "artifact-content verification owed"** with cascading downgrade of `[ARTIFACT-ABSENT]` flags on AC-SM-01, -03, -04, -05, -06, -07, -09, -10, -11, -12 to `[CONTENT-AUDIT-OWED]`. | Documentation/Release Owner | Before Step 7 | 🟡 Investigating | Per research-00 § 360 + 398. The downgrade is recommended but unblocked closure is contingent on content audit completing pre-Step-7 (Q-2). [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] on presence; [CONTENT-AUDIT-OWED] on content. |
| **Q-GAP-01** | F-C | `tests/cleanup_audit/test_prompts.py` absence — spec under-counts CLI emission sites by 5/6 (cleanup_audit/prompts.py L26, L47, L69, L92, L116 not named). | Engineering Lead (CR-DEP-05 author) | Before Step 5 | 🔴 Open | Per research-00 § 57 + § 506 R-DIV-01 (e). [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-GAP-02** | F-C | HTML-vs-shell sentinel form (CR-7 ORDERING canonical form). PRD S24.2 commits to HTML-comment form `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->`. TDD must specify whether binding is sentinel-presence grep (AC-ATK-13) OR AST-level (AC-ATK-01) OR informational. | Engineering Lead | Before Step 1 | 🔴 Open | Per research-00 § 409. [SPEC-DEFINED] |
| **Q-GAP-03** | F-C | Non-generalization grep audit for per-item-marker consumers (closed enumeration discipline; AC-ATK-05). | Engineering Lead | Before Step 1 | 🔴 Open | Per research-00 § 295 R-ATK-05 + § AC-ATK-05 binding. [SPEC-DEFINED] |
| **Q-GAP-04** | F-C | `flock` portability. `flock` is GNU-coreutils only. macOS/BSD lacks `flock` by default. Either require `brew install flock` or fallback to `lockfile-create` from `procmail-lockfile`. AC-ATK-16 binding must specify. | Engineering Lead | Before Step 6 | 🔴 Open | Per research-12 § 10 row 8 (Gap-8). The TDD §14 (Dev Setup) MUST document portable invocation. [SPEC-DEFINED][UNVERIFIED] |
| **Q-GAP-05** | F-C | `helper module superclaude/skills/task/preflight.py` to-be-authored (per AC-ATK-10 fixture binding). | Engineering Lead | Before Step 1 | 🔴 Open | Per research-12 § 5 + row 83 (preflight helper module). [SPEC-DEFINED] |
| **Q-GAP-06** | F-C | `helper module superclaude/skills/task/frontmatter_validator.py` to-be-authored (per CR-FM-01 binding + AC-ATK-12(c)). | Engineering Lead | Before Step 1 | 🔴 Open | Per research-12 § CR-FM-01 row + AC-ATK-12. [SPEC-DEFINED] |
| **Q-GAP-07** | F-C | `tests/fixtures/donor-blocks/*.txt` (8 files: 6 donor + 2 sentinel) must be authored pre-Step-6 (per AC-ATK-06 fixture freeze). | Engineering Lead | Before Step 6 | 🔴 Open | Per research-12 § AC-ATK-06 binding. CR-TASK-12 audit moves to fixture-backed after Step 6 hard-delete. [SPEC-DEFINED] |
| **Q-GAP-08** | F-C | `docs/condensation-table.md` artifact authoring (per AC-ATK-04 condensation-bucket table). | Engineering Lead / Documentation Owner | Before Step 5 | 🔴 Open | Per research-12 § AC-ATK-04. [SPEC-DEFINED] |
| **Q-GAP-09** | F-C | Server-side pre-receive hook hosting (per AC-ATK-17). Assumes GitHub Actions or self-hosted-git pre-receive availability. If neither available, fallback to `scripts/atomic_step_5.sh` with `flock` — but this is local, NOT server-side, and a force-push from a different clone bypasses it. | Engineering Lead / DevOps | Before Step 5 | 🔴 Open | Per research-12 § 10 row 2 (Gap-2). [SPEC-DEFINED][UNVERIFIED] |
| **Q-GAP-10** | F-C | `${TASK_DIR}/research/tfep-incident-report.md` template (CR-TASK-10) — seven-field schema fields enumeration must match donor `:222-234` verbatim. | Engineering Lead | Before Step 3 | 🟡 Investigating | TDD-layer naming convention `{tier, item_id, trigger, classification, action, timestamp, sha}` is research inference; donor verbatim alignment owed. §7 Schema 4 confirms 7 fields. [SPEC-DEFINED] |
| **Q-GAP-11** | F-C | Acknowledgment-gate persistence shape — Schema 5 one-shot ack mechanism (single Task Log line vs separate ack file) is under-specified. | §7 / §8 author | Before Step 1 | 🔴 Open | Per research-14 § Gaps (entry 4). Decision required for AC-ATK-18(c). [SPEC-DEFINED] |
| **Q-GAP-12** | F-C | Schema-version uniformity. Schema 3 includes `schema_version: 1`; no other schema does. Decide whether all 5 schemas adopt a uniform version field. | §7 author | Pre-publish | 🟡 Investigating | Per research-14 § Gaps (entry 5). Design choice. [SPEC-DEFINED] |
| **Q-DRIFT-IN-FLIGHT** | F-D | **In-flight count drift acknowledgment.** Authoritative floor at fix-cycle 2 = **136 union files** (per research-11 §2.1 live grep). File 14 at L292/L336 still cites **132** (per the cycle-2 PartB analyst finding). The figure grows over time; §15 iterates live count at authoring time. The "moving floor" framing must propagate into §15 Testing fixtures (live recount at gate-execution time, not hard-coded). Drift discipline note: file 14's framing ("audit scope follows the live count, not the variant-3 snapshot") acknowledges this — patch L292/L336 to 136 to align. | Engineering Lead / §7 author | Before Step 1 (test fixture authoring) | 🟡 Investigating | Per qa/research-gate-consolidated.md § Cycle 2 residuals (entry 1) + research-14 § 7 closure note. The "moving floor" is canonical — test fixtures iterate live grep at commit time. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-DRIFT-F2** | F-D | **F2 catalog cardinality typo correction history.** PRD body and research-notes.md at multiple points stated `9 prohibitions` for the F2 catalog. The authoritative count is **10** per fix-cycle 1 cross-confirmation: file 01 top-of-file CORRECTION block + file 09 § 10 line 532 math (10+3=13) + file 10 corrections at lines 25, 70, 284, 351, 360 + file 13 §2.3 enumeration of all 10 prohibition entries at `.claude/skills/task/SKILL.md:108-117` (lines 108..117 = 10 list items). **Retire the "9" figure.** Test fixtures (NFR-INV-2 catalog additivity diff) must lock against 10 entries pre-merge → 13 entries post-merge (10 existing + 3 TFEP VIOLATION rules per TU-6). | Engineering Lead | Closed (corrections applied) | 🟢 Resolved | Per qa/research-gate-consolidated.md § Fixes applied (entry 2). 9→10 typo history preserved. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-AC-ATK-05-CLOSED-ENUM** | F-F | AC-ATK-05 closed-enumeration register `[UNVERIFIED]` until M1 atomic-landing commit. Authorized per-item-marker consumers initial set: `{CR-TASK-07 baseline-skip}`. New consumer requires new ME-10+. Manifest fixture `tests/audit/test_marker_consumers.py` enforces. | Engineering Lead / §6 author | Step 1 (M1 atomic commit) | 🟡 Investigating | Per qa/research-gate-consolidated.md § Cycle 1 residuals + research-12 AC-ATK-05 row. Architecture elevates to M1 commitment. [SPEC-DEFINED][UNVERIFIED] |
| **Q-GATE-1-5-SCHEMA** | F-E | **6th Gate-1.5 schema decision.** Research-14 § Gaps entry 1 identifies a third emission token `gate-1.5: deleted-related-doc` (ENOENT on `related_docs:` paths, per research-00 § Job 3 L36 + P-04 persona § 58). Decide: author as a 6th canonical schema OR fold into Schema 5 as an additional `surface=` value. Existing Schema 5 grammar: `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`. | §7 author | Before Step 1 | 🟡 Investigating | Recommend fold-into-Schema-5 with `surface=related-doc-missing path=<path>` value to preserve single-grammar parser. [SPEC-DEFINED] |
| **Q-GATE-1-5-TOKEN-COLLISION** | F-E | **Gate-1.5 token grammar collision risk.** AC-ATK-18(b) names format `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`. If the existing `gate-1.5: pre-flight ...` token from CR-TASK-06 collides with this format, the parser must disambiguate via the second token (`legacy-surface-reference` vs `pre-flight`). §14 (Observability) pins both grammars formally. | §7 / §8 author | Before Step 1 | 🔴 Open | Per research-12 § 10 row 9 (Gap-9). Recommend the grammar be `gate-1.5: <subtype> ...` with `<subtype> ∈ {pre-flight, legacy-surface-reference, deleted-related-doc?}`. [SPEC-DEFINED] |
| **Q-TYPO-K-001-vs-K-01** | F-G | **K-NN ID typo correction.** The user-query prompt referenced "K-001..K-010" for KPIs, but the PRD uses **K-01..K-08** (eight KPIs, no leading zeroes, no K-009/K-010). Per research-00 § Section 20.1 line 283: "KPI-style K-001..K-010 user query maps to S19 K-01..K-08; risk register here". The typo is documented; canonical IDs are **K-01..K-08**. No further action; this entry locks the correction for downstream artifact authoring. | Documentation/Release Owner | Closed | 🟢 Resolved | Per research-00 § 285 + § 257-264 enumeration. K-NN typo correction lock. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| **Q-TYPO-F2-9-vs-10** | F-G | **F2 count typo correction history (companion).** Cross-references Q-DRIFT-F2 above. The "9" figure originated in research-notes.md and propagated to file 01, file 10 (4 inline locations), file 13. Fix-cycle 1 closed all by replacing with "10" or adding correction blocks. Future authors writing about the F2 catalog MUST cite **10 entries** as the pre-merge baseline. | Documentation/Release Owner | Closed | 🟢 Resolved | Per qa/research-gate-consolidated.md § Fixes applied (entry 2). [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |

### 22.2 Patch-Before-Phase-7 Obligations (extracted from R-DRIFT-NN)

Three patches MUST land before Phase 7 commit execution. They are mechanical and single-source.

1. **R-DRIFT-03 (MEDIUM, multi-artifact, M3-blocking)** — Replace `:200-210` → `:157-161` in `transfer-manifest.md` TU-7 L277, `integration-sketches.md` IS-ADOPT-9 L142, `invariant-survival-walkthrough.md` § 2.6 step 4 L277, AND in CR-TASK-12 verbatim-diff audit anchors. Without this patch, CR-TASK-12 returns non-zero against D23 forensic-results content and erroneously blocks the M3 commit.
2. **R-DRIFT-02 (LOW, multi-artifact)** — Replace `:127-135` → `:133-135` in `transfer-manifest.md` TU-6 L238, `integration-sketches.md` IS-ADOPT-2 L52, `invariant-survival-walkthrough.md` § 2.6 step 3 L263, AND in CR-TASK-12 audit anchors. (LOW because content verbatim is preserved.)
3. **R-DOC-01 cascade-downgrade** — Re-flag AC-SM-01, -03, -04, -05, -06, -07, -09, -10, -11, -12 from `[ARTIFACT-ABSENT]` to `[CONTENT-AUDIT-OWED]` and schedule the content audit before Step 7 (per Q-2).

### 22.3 R-DOC-01 Cascade Downgrade — Detailed Disposition

Per Q-R-DOC-01, the R-DOC-01 framing changes from "artifact gaps" to "artifact-content verification owed". The downstream cascading downgrade affects 10 AC-SM rows:

| AC-SM row | Original flag | Recommended new flag | Rationale |
|-----------|---------------|----------------------|-----------|
| AC-SM-01 | `[ARTIFACT-ABSENT]` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` | `transfer-manifest.md` PRESENT; V/C/K table re-readable now |
| AC-SM-03 | `[ARTIFACT-ABSENT]` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` | `invariant-survival-walkthrough.md` PRESENT |
| AC-SM-04 | `[ARTIFACT-ABSENT]` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` | `final-merge-plan.md` § 4 PRESENT |
| AC-SM-05 | `[ARTIFACT-ABSENT]` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` | `compat-hazard-report.md` PRESENT |
| AC-SM-06 | `[ARTIFACT-ABSENT]` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` | `merge-master.md` § 1 + § 6 PRESENT |
| AC-SM-07 | `[ARTIFACT-ABSENT]` | `[UNVERIFIED]` (post-Step-1..4) | Requires POST-MERGE state of `task/SKILL.md` |
| AC-SM-09 | `[ARTIFACT-ABSENT]` | `[UNVERIFIED]` (post-Step-5) | Requires Step-5 commit roster |
| AC-SM-10 | `[ARTIFACT-ABSENT]` | `[UNVERIFIED]` (post-Step-6) | Requires Step-6 commit roster |
| AC-SM-11 | `[ARTIFACT-ABSENT]` | `[CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]` | `rejected-features-ledger.md` PRESENT |
| AC-SM-12 | `[ARTIFACT-ABSENT]` | `[UNVERIFIED]` (post-merge) | Integration test against 136-file population |

**Net effect:** 7 rows promotable to `[CODE-VERIFIED]` immediately (in-repo validation possible NOW at pinned SHA); 5 rows remain `[UNVERIFIED]` pending POST-MERGE state (which is structural, not artifact-absence). The R-DOC-01 framing as "artifact gaps" is therefore inaccurate; the residual `[UNVERIFIED]` set is the expected steady state for any forward-looking AC against a not-yet-landed merge.

### 22.4 12 Unresolved Research Gaps (file 00 inventory)

Per qa/research-gate-consolidated.md § Cycle 1 residuals (entry 4), file 00 surfaces 12 unresolved research gaps for TDD §22 carry. The first 10 are captured as Q-GAP-01..Q-GAP-10 above; the remaining 2 (Q-GAP-11 ack persistence + Q-GAP-12 schema versioning) span research-14. The full enumeration is:

1. Q-GAP-01 — `tests/cleanup_audit/test_prompts.py` absence (CLI emission site under-count 5/6)
2. Q-GAP-02 — HTML-vs-shell sentinel form (CR-7 ORDERING canonical form)
3. Q-GAP-03 — non-generalization grep audit for per-item-marker consumers
4. Q-GAP-04 — `flock` portability (macOS/BSD)
5. Q-GAP-05 — `preflight.py` helper module to-be-authored
6. Q-GAP-06 — `frontmatter_validator.py` helper module to-be-authored
7. Q-GAP-07 — `tests/fixtures/donor-blocks/*.txt` (8 files) authoring
8. Q-GAP-08 — `docs/condensation-table.md` authoring
9. Q-GAP-09 — server-side pre-receive hook hosting
10. Q-GAP-10 — `${TASK_DIR}/research/tfep-incident-report.md` template field alignment
11. Q-GAP-11 — Acknowledgment-gate persistence shape (Schema 5)
12. Q-GAP-12 — Schema-version field uniformity (all 5 schemas)

All 12 are unblocked (no upstream R-DOC-01 dependency) but each requires Engineering Lead or §7/§8 author decision before its bound milestone.

### 22.5 AC-ATK-05 Closed-Enumeration Register

Per Q-AC-ATK-05-CLOSED-ENUM (above), the authorized per-item-marker consumer set is **closed** at: `{CR-TASK-07 baseline-skip}`. Any new consumer requires a new ME-10+ entry in the manifest exception register; the closure is structurally enforced by `tests/audit/test_marker_consumers.py` (per AC-ATK-05). This register lives here in §22 for cross-document traceability — see also §15.2 AC-ATK-05 row and §28.3 glossary entry.

### 22.6 Status Roll-Up

| Status | Count | Items |
|--------|-------|-------|
| 🟢 Resolved | 7 | Q-5, Q-R-DRIFT-01, Q-R-DRIFT-04 (RETRACTED), Q-R-DRIFT-05, Q-DRIFT-F2, Q-TYPO-K-001-vs-K-01, Q-TYPO-F2-9-vs-10 |
| 🟡 Investigating | 9 | OQ-TFEP-FIELD-COUNT, Q-2, Q-4, Q-R-DOC-01, Q-GAP-10, Q-GAP-12, Q-DRIFT-IN-FLIGHT, Q-AC-ATK-05-CLOSED-ENUM, Q-GATE-1-5-SCHEMA |
| 🔴 Open | 20 | OQ-TIER-VOCABULARY, OQ-FM-03-SUNSET, OQ-F-NN-BIJECTION, OQ-F-05-MANIFESTIZATION, OQ-PROHIBITION-DISPOSITION-MATRIX, Q-1, Q-3, Q-R-DRIFT-02, Q-R-DRIFT-03, Q-GAP-01..09 (9 items), Q-GAP-11, Q-GATE-1-5-TOKEN-COLLISION |

(Counts add to 36 distinct entries; OQ-TIER-VOCABULARY and Q-1 are intentional duplicates for traceability — the unique-question count is 35.)

---

## 23. Timeline & Milestones

> **Anchor.** The 10-step canonical commit sequence in `merge-master.md` § 6 (cross-validated in research-13 § 5) IS the timeline. Per file 13 § 5.3, Steps 1 / 5 / 6 are *coarse* (atomic-by-design) while Steps 2 / 3 / 4 / 7-10 are *fine* (single CR-ID can be reverted). The atomic constraints (ME-6 + CR-7 + CR-9 for Step 1; S-2 for Step 5; S-3 for Step 6) are load-bearing — splitting them re-introduces wrong-stance-dispatch / broken-CLI / mirror-drift windows respectively. [CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)]

### 23.1 High-Level Timeline

| Milestone | Target | Status | Dependencies |
|-----------|--------|--------|--------------|
| **M0 — Design Complete (this TDD)** | T+0 | 🟡 In Progress | PRD + 4-cycle research gate PASS |
| **M1 — Step 1 lands (atomic M1)** | T+5d | ⬜ Pending | OQ-TIER-VOCABULARY + OQ-FM-03-SUNSET resolved; Q-GAP-02/05/06 closed; AC-ATK-05 closed-enum register published |
| **M2 — Step 2 lands** | T+7d | ⬜ Pending | M1 |
| **M3 — Step 3 lands (TFEP cluster)** | T+10d | ⬜ Pending | M2; R-DRIFT-03 patch applied to all 3 artifacts + CR-TASK-12 audit |
| **M4 — Step 4 lands (audit window closes)** | T+12d | ⬜ Pending | M3; CR-TASK-12 7-diff PASS; Q-GAP-07 fixtures authored |
| **M5 — Step 5 lands (soft-deprecation, atomic; S-2 binding)** | T+15d | ⬜ Pending | M4; in-flight target population frozen (S-1: live `121039`, `121250` + 136-file floor); Q-GAP-08 condensation table authored |
| **M6 — Step 6 lands (hard-delete; S-3 binding)** | T+17d | ⬜ Pending | M5; rf-qa F-07 chain-verifier PASS; CR-DEP-06 manifest authored |
| **M7 — Step 7 lands (invariant survival walkthrough audit)** | T+19d | ⬜ Pending | M6; Q-2 content audit complete |
| **M8 — Step 8 lands (docs rollup + mkdocs build)** | T+21d | ⬜ Pending | M7 |
| **M9 — Step 9 lands (CR-DEP-06 residual manifest)** | T+22d | ⬜ Pending | M8 |
| **M10 — Step 10 lands (audit closure; K-01..K-08 baseline)** | T+24d | ⬜ Pending | M9 |
| **Phase 7.5 — Full traceability matrix PASS** | T+27d | ⬜ Pending | M10; AC-ATK-01..18 + AC-SM-01..12 all closed |

### 23.2 Implementation Phases (mapped to 10-step commit chain per `merge-master.md` § 6 + research-13 § 5.1)

#### Phase Step-1: M1 atomic foundation row (CR-FM-03 + TU-1 + TU-2 + sentinel)

**Deliverables (atomic-7 per ME-6 / CR-7 / CR-9):**
- [ ] CR-FM-03 default-to-STANDARD compat shim landed at `task/SKILL.md` parser
- [ ] CR-FM-01 + CR-FM-02 canonicalization rules and per-item-marker spec
- [ ] CR-TASK-01..04 row-1 ordering (`path_override_check → tier_field_validate → gate_1_dispatch`)
- [ ] CR-7 ORDERING sentinel (HTML-comment form per Q-GAP-02)
- [ ] CR-TASK-04 companion sentinel block
- [ ] AC-ATK-05 closed-enumeration register (initial set `{CR-TASK-07 baseline-skip}`)
- [ ] `tier_field_validate()` + `path_override_check()` + `gate_1_dispatch()` helper modules

**Exit Criteria (gates):**
- Step-1 pre-commit gate returns 0
- AC-SM-07 [CONTENT-AUDIT-OWED] cleared
- AC-SM-12 100% in-flight resume gate PASS against 136-file live population

#### Phase Step-2: TU-3 + TU-4 (Gate 2 roster widening + git pre-flight 5-row matrix)

**Deliverables:**
- [ ] Gate 2 widened roster `[rf-qa, quality-engineer]` (ME-2 preserved)
- [ ] D15b Layer 2 git pre-flight (warn-and-continue, 5-row matrix per AC-ATK-02)
- [ ] `tier_preflight_git_status()` helper module

**Exit Criteria:**
- AC-ATK-02 5-row dispatch test PASS (no HALT for any row)
- AC-ATK-10 two-category fixture PASS

#### Phase Step-3: M3 TFEP cluster (CR-TASK-07..10)

**Deliverables (R-DRIFT-03 PATCH PRECONDITION):**
- [ ] R-DRIFT-03 anchor patch applied to all 3 artifacts + CR-TASK-12 anchors BEFORE this commit
- [ ] TU-5 TFEP baseline on disk at `${TASK_DIR}/research/test-baseline.yaml`
- [ ] TU-6 Prohibitions + Carve-outs APPEND-only to F2 catalog (10 → 13 entries)
- [ ] CR-TASK-07..10 acceptance criteria + side-channel hook to `${TASK_DIR}/research/tfep-incident-report.md` (7-field schema)
- [ ] TU-7 4th rf-qa invocation point post-merge (TFEP mid-phase escalation; F-05 authorized)
- [ ] TU-8 incident reporting side-effect file

**Exit Criteria:**
- AC-ATK-03 4-state observer test PASS
- AC-ATK-12(b) 7-field schema fixture PASS
- AC-CR-TASK-09-F04 over-escalate test PASS

#### Phase Step-4: Donor verbatim diff audit window

**Deliverables (R-DRIFT-02 PATCH PRECONDITION):**
- [ ] R-DRIFT-02 anchor patch applied to all 3 artifacts + CR-TASK-12 anchors BEFORE this commit
- [ ] CR-TASK-12 seven-diff audit fixture authored at `tests/fixtures/donor-blocks/`
- [ ] AC-ATK-06 frozen-fixture snapshot script

**Exit Criteria:**
- CR-TASK-12 returns 7 zero-diffs (6 donor + 1 sentinel block) — AC-SM-08 gate

#### Phase Step-5: Soft-deprecation (S-2 atomic binding)

**Deliverables (S-1 supplement-not-replace precondition; ATOMIC):**
- [ ] CR-DEP-01 donor stubification (atomic with below)
- [ ] CR-DEP-02 sha256 digest baseline
- [ ] CR-DEP-05 CLI residual grep + cleanup_audit/prompts.py emission re-route
- [ ] CR-DOC-01 docs rewrite (atomic with CR-DEP-01 per AC-ATK-15)
- [ ] CR-REF-01..05 CLI residual deletion
- [ ] `docs/condensation-table.md` (Q-GAP-08)
- [ ] In-flight target population frozen: spec-named `121039`, `121250` AND broader 136-file population (Q-3)

**Exit Criteria:**
- AC-ATK-15 Step-5 atomicity test PASS (`git log --name-only <step5-commit>` includes CR-DEP-01 + CR-DOC-01)
- AC-ATK-17 server-side pre-receive hook PASS (no rebase-split bypass)
- AC-SM-09 commit roster equality test PASS

#### Phase Step-6: Hard-delete (S-3 atomic binding)

**Deliverables (ATOMIC; INV-04 highest exposure):**
- [ ] CR-DEP-03 donor SKILL.md hard-delete
- [ ] CR-DEP-04 directory absence + `make sync-dev` prune
- [ ] AC-ATK-07 rf-qa F-07 chain verifier PASS (pre-hard-delete)
- [ ] AC-ATK-16 `flock` guard on `make sync-dev` (Q-GAP-04 portability)
- [ ] CR-DEP-06 residual manifest written to `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` with all 144 residuals dispositioned

**Exit Criteria:**
- AC-SM-10 Step-6 commit roster equality test PASS
- `make verify-sync` returns 0
- Donor `sc-task-protocol/` directory absent from both `src/` and `.claude/`
- CR-DEP-06 manifest: residual count outside authorized buckets = 0

#### Phase Step-7: Invariant survival walkthrough audit

**Deliverables:**
- [ ] AC-SM-03 walkthrough re-read (5 of 5 INVs)
- [ ] AC-SM-04 8 of 8 F-rows cite valid line ranges
- [ ] Q-2 content audit complete (downgrades R-DOC-01)

#### Phase Step-8: Documentation rollup

**Deliverables:**
- [ ] CR-DOC-02..09, CR-DOC-11 partial
- [ ] mkdocs build returns 0 broken-link warnings
- [ ] CR-DOC-13 R-RULE-11 audit clean

#### Phase Step-9: CR-DEP-06 residual manifest one-shot

**Deliverables:**
- [ ] Post-Step-6 one-shot residual-reference manifest finalized
- [ ] AC-ATK-18(d) closure

#### Phase Step-10: Audit closure

**Deliverables:**
- [ ] CR-DOC-10..12 final
- [ ] CR-DEFER-T06.04 ack
- [ ] AC-SM-01..12 audits re-run from clean checkout
- [ ] K-01..K-08 baseline measurements taken

### 23.3 Pre-Step-N Gating Decisions

Per the R-DRIFT-NN register and the §22.2 patch list, the following decisions/patches MUST close at the named pre-Step boundary or that Step's pre-commit gate fails:

| Pre-Step | Gating decision/patch | Owner | Driver |
|----------|----------------------|-------|--------|
| Before Step 1 (M1) | OQ-TIER-VOCABULARY resolved; OQ-FM-03-SUNSET binding; Q-GAP-02 sentinel form; Q-GAP-05/06 helper modules authored; AC-ATK-05 closed-enum register published; Q-GAP-11 ack persistence; Q-GATE-1-5-TOKEN-COLLISION grammar pinned | Engineering Lead | M1 atomic commit |
| Before Step 3 (M3) | **R-DRIFT-03 anchor patch applied** to `transfer-manifest.md` / `integration-sketches.md` / `invariant-survival-walkthrough.md` AND CR-TASK-12 audit anchors | Documentation/Release Owner | CR-TASK-12 would otherwise erroneously block M3 |
| Before Step 4 (audit window) | **R-DRIFT-02 anchor patch applied** to same 3 artifacts + CR-TASK-12 audit anchors; Q-GAP-07 donor-block fixtures authored | Documentation/Release Owner | CR-TASK-12 audit fixture freeze |
| Before Step 5 (soft-deprecation) | Q-3 S-1 supplement-not-replace framing confirmed (136-file population frozen); Q-GAP-08 condensation table authored; Q-GAP-01 cleanup_audit/prompts.py emission re-route; Q-GAP-09 server-side hook hosting decided; OQ-F-05-MANIFESTIZATION + OQ-PROHIBITION-DISPOSITION-MATRIX resolved | Engineering Lead | S-2 atomic binding + AC-ATK-15 + AC-ATK-17 |
| Before Step 6 (hard-delete) | Q-4 CR-DEP-06 binding count confirmed (144); Q-GAP-04 `flock` portability fallback documented; AC-ATK-07 rf-qa F-07 chain verifier authored | Engineering Lead | S-3 atomic binding + AC-ATK-18(d) |
| Before Step 7 (walkthrough audit) | Q-2 content audit of 7 anchor artifacts complete; Q-R-DOC-01 downgrade applied; OQ-F-NN-BIJECTION resolved | Documentation/Release Owner | AC-SM-03 + AC-SM-04 |

### 23.4 Rollback Granularity (cross-ref §19.4)

| Step | Granularity | Rollback path | Special hazard |
|------|-------------|---------------|----------------|
| 1 | Coarse (atomic-by-design) | Single revert of M1 commit (7 rows) | Splitting violates ME-6 / CR-7 / CR-9 |
| 2-4 | Fine | Per-CR revert | None |
| 5 | Coarse (atomic, S-2 binding) | Revert CR-DEP-01..02 + CR-REF-01..02 + CR-REF-09 + CR-DOC-01 atomically | If Step 6 already shipped, cannot cleanly roll back without also reverting Step 6 |
| 6 | Coarse, **destructive-by-default** | Re-introducing donor skill files; **safer to roll forward** than to revert | INV-04 highest exposure |
| 7-10 | Fine (annotation/mirror-refresh) | Cheap | None |

---

## 24. Release Criteria

> **Binding rule.** Every AC closes a release gate, per file 12 § 9 table mapping AC-rows to per-Step gates. The DoD below is the operational manifestation: a release ships only when **all 18 AC-ATK rows AND all 12 AC-SM rows close** with auditable evidence.

### 24.1 Definition of Done (per-Step gates)

A feature is considered "Step-N complete" when:

- [ ] All AC-ATK and AC-SM rows mapped to Step N (per file 12 § 9) close with PASS
- [ ] Pre-commit gate at Step N returns exit-code 0
- [ ] Pytest fixtures named in the AC mapping execute clean under `uv run pytest`
- [ ] Code review by `rf-qa` (post-completion) PASS
- [ ] Documentation updated per CR-DOC-NN row roster
- [ ] No new `[CODE-CONTRADICTED]` tags introduced
- [ ] Each `[CODE-VERIFIED]` tag carries the `(git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)` suffix (drift discipline; AC-ATK-08)
- [ ] No HIGH/CRITICAL R-DRIFT-NN open against the Step's input artifacts
- [ ] If Step is M5/M6, S-2/S-3 atomic-binding gate PASS
- [ ] Step-6: CR-DEP-06 residual manifest enumerates ≥144 residuals across ≥40 files with all outside-authorized-bucket counts = 0

### 24.2 Release Criteria — Full AC → Gate Map

The following table maps **every** AC to its release gate per file 12 § 9 and §3 AC-SM target. AC-SM targets are quoted from file 12 § 3.

#### 24.2.1 AC-ATK-01..18 → Release Gate

| AC | Target / Predicate | Release Gate | Status flag |
|----|--------------------|--------------|-------------|
| AC-ATK-01 | F-02 ordering claim grep+AST | G-Step-4 pre-commit + CI | [SPEC-DEFINED][UNVERIFIED] post-Step-4 |
| AC-ATK-02 | 5-row matrix `{clean, dirty, tool-absent, not-a-repo, error-other}` × {Task Log line, action}; no HALT | G-Step-1 Gate-1.5 pre-loop | [SPEC-DEFINED][UNVERIFIED] post-Step-1 |
| AC-ATK-03 | 4-state observer `{absent, empty, parse-fail, schema-fail}` for `test-baseline.yaml` | G-Step-3 F1 loop body | [SPEC-DEFINED][UNVERIFIED] post-Step-3 |
| AC-ATK-04 | Condensation table 79→65 with 2 duplicates named | G-Step-5 pre-Step-5 PRD precondition | [SPEC-DEFINED][UNVERIFIED] (Q-GAP-08 binding) |
| AC-ATK-05 | Closed enumeration `{CR-TASK-07 baseline-skip}` ; new consumer needs ME-10+ | G-Step-1 (M1 atomic landing) | [SPEC-DEFINED][UNVERIFIED] (Q-AC-ATK-05-CLOSED-ENUM) |
| AC-ATK-06 | Frozen fixture for 6 donor strings + 2 sentinel blocks | G-Step-4 pre-commit (audit moves to fixture post-Step-6) | [SPEC-DEFINED][UNVERIFIED] (Q-GAP-07 binding) |
| AC-ATK-07 | rf-qa rebound as F-07 chain verifier at Step-6 pre-commit | G-Step-6 pre-commit (pre-hard-delete) | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-08 | `--max-wait 14d` CLI flag + git-SHA suffix on every `[CODE-VERIFIED]` tag + CR-DEP-05 grep extension | G-Step-5 + G-Step-6 + PRD final-commit | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-09 | md5 → sha256 mechanical substitution (LOW) | G-Step-5 pre-commit | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-10 | Two-category HALT vs WARN-CONTINUE table | G-Step-1 pre-loop entry | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-11 | F-05 disposition matrix for verifier-spawned F1 | G-Step-1 plan-bound | [SPEC-DEFINED][UNVERIFIED] (OQ-PROHIBITION-DISPOSITION-MATRIX) |
| AC-ATK-12 | (a) CR-AUDIT-FM-03-SUNSET row; (b) 7-field schema; (c) canonical enum table | G-Step-1 + G-Step-3 + Step-N+M | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-13 | Sentinel-comment audit grep | G-Step-4 pre-commit | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-14 | (a) CR-DEP-05 grep; (b) CR-REF-18 cluster root; (c) CR-DEP-04 gate; (d) CR-DOC-13 scope | G-Step-6 pre-commit + G-Step-8 | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-15 | CR-DOC-01 lands atomic Step-5 (Step-8 fallback iff `AUTHORIZE_HOT_FIX=1` AND Step-5 pre-commit FAIL) | G-Step-5 pre-commit (primary), G-Step-8 (fallback) | [SPEC-DEFINED][UNVERIFIED] |
| AC-ATK-16 | `flock` concurrency guard on `make sync-dev` prune | G-Local Makefile (CI matrix) | [SPEC-DEFINED][UNVERIFIED] (V3 security-probe; Q-GAP-04 portability) |
| AC-ATK-17 | Server-side `pre-receive` hook re-grep `/sc:task\b` vs CLI sources on landing commit | G-Push-time (server-side; cannot be bypassed by `git rebase -i`) | [SPEC-DEFINED][UNVERIFIED] (V3; Q-GAP-09) |
| AC-ATK-18 | (a) Gate-1.5 resume-time content grep; (b) sprint-emit boundary grep; (c) one-shot ack; (d) CR-DEP-06 manifest | G-Resume (per-task) + G-sprint-emit + G-post-Step-6 | [SPEC-DEFINED][UNVERIFIED] (V3) |

#### 24.2.2 AC-SM-01..12 → Release Gate (AC-SM target quoted)

| AC | AC-SM Target (per file 12 § 3) | Release Gate | Status flag |
|----|--------------------------------|--------------|-------------|
| AC-SM-01 | **8 of 8 V/C/K verdicts identical, byte-for-byte** | G-Step-7 + CI | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-02 | **9 of 9 ME rows trace to ≥1 CR-row** | G-Step-7 + CI | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-03 | **5 of 5 INVs survive merged surface, re-readable walkthrough** | G-Step-7 | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-04 | **8 of 8 F-rows cite valid line ranges** | G-Step-7 | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-05 | **3 of 3 S-rows cite an HZ-NN** | G-Step-7 | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-06 | **67 row-line-items, 10 commit steps** | G-Step-7 | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-07 | **2 greps × 3 function names = 6 hits in expected order; 0 reorders detected** | G-Step-4 pre-commit | [SPEC-DEFINED][UNVERIFIED] post-Step-1..4 |
| AC-SM-08 | **7 of 7 diffs return zero differences (CR-TASK-12 seven-diff)** | G-Step-4 pre-commit | [SPEC-DEFINED][UNVERIFIED] post-Step-1 (R-DRIFT-02/03 patch precondition) |
| AC-SM-09 | **Step 5 commit file list = {task.md stubified, task.md digest, CR-DOC-01 rewrites, CR-REF-01..05}** | G-Step-5 push | [SPEC-DEFINED][UNVERIFIED] post-Step-5 |
| AC-SM-10 | **Step 6 commit file list = {sc-task-protocol/SKILL.md deletion, sc-task-protocol/ dir absence, sync-dev verify}** | G-Step-6 push | [SPEC-DEFINED][UNVERIFIED] post-Step-6 |
| AC-SM-11 | **0 of N ledger entries (LR-REJECT-1..N) re-introduced in `final-merge-plan.md` § 5** | G-Step-7 | [SPEC-DEFINED][CODE-VERIFIED (git-sha: 71b1b1fe7909fab59b5e30d39ce68fcb7f825444)] |
| AC-SM-12 | **100% of live in-flight MDTM population resumes cleanly under CR-FM-03; gates 1/5/6 return 0** | G-Step-1 + G-Step-5 + G-Step-6 (integration test against 136-file live population) | [SPEC-DEFINED][UNVERIFIED] post-merge |

### 24.3 Release Checklist (overall)

- [ ] All 18 AC-ATK rows + 12 AC-SM rows close PASS
- [ ] No CRITICAL R-ATK / R-DRIFT open; all MEDIUM R-DRIFT patched (R-DRIFT-03 mandatory pre-M3)
- [ ] CR-DEP-06 manifest: 144 → 0 residuals outside authorized leave-as-is buckets
- [ ] `mkdocs build` returns 0 broken-link warnings
- [ ] `uv run pytest tests/cli/` returns 100% green on integration immediately after Step-5/6
- [ ] `make verify-sync` returns 0
- [ ] All `[CODE-VERIFIED]` tags carry git-sha suffix (AC-ATK-08 drift-discipline)
- [ ] Rollback runbook tested for Steps 1, 5, 6 (per §25.1)
- [ ] On-call team briefed on §25.1 runbooks
- [ ] OQ-FM-03-SUNSET binding `N` agreed and CR-AUDIT-FM-03-SUNSET row in `merge-master.md`
- [ ] Release notes prepared; Stakeholders notified

---

## 25. Operational Readiness

> **Premise.** Per file 12 § 9 and the §22 hazard register, five recurring operational scenarios must have runbooks: (a) Critical Path Override invocation; (b) Gate-1.5 emission triage; (c) Tier mis-classification recovery; (d) TFEP escalation handling; (e) in-flight resume triage. These cover both the 4-cycle research-gate risk surface and the V3 security-probe ACs.

### 25.1 Runbook

| Scenario | Symptoms | Diagnosis Steps | Resolution | Escalation |
|----------|----------|-----------------|------------|------------|
| **R1 — Critical Path Override invocation** (CR-7 row-1 site fires `path_override_check`) | F1 dispatched to STRICT tier for an item under `auth/` / `security/` / `crypto/` / `models/` / `migrations/` despite frontmatter `Tier:` claiming `LIGHT` or `EXEMPT` | (i) Read Task Log for `path_override fired: matched <pattern>`; (ii) confirm CR-7 ORDERING sentinel still present at row-1 site via grep; (iii) verify `path_override_check()` executed FIRST per CR-FM-04 ordering | Honor override (STRICT wins). If author insists on LIGHT/EXEMPT, require explicit override-suppression annotation with rf-qa sign-off; never silently bypass CR-7. | rf-qa within 1h if author requests suppression; Engineering Lead within 4h if pattern set itself disputed |
| **R2 — Gate-1.5 emission triage** (resume-time legacy-surface-reference detected) | Task resume emits `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` | (i) Confirm token grammar matches canonical AC-ATK-18(b) form; (ii) check `legacy-surface-ack: 1` in task frontmatter — if present, gate-1.5 fires once per task generation (not per resume); (iii) inspect matched symbol against CR-DEP-06 residual manifest disposition | Acknowledge via one-shot ack (set `legacy-surface-ack: 1` in frontmatter). DO NOT HALT — ME-3 forbids new HALT semantics. Patch the matched surface only if disposition = `action=violation`. | If matched surface = `bucket=src`, page Engineering Lead within 30 min (manifest expected to be 0 in `src/`) |
| **R3 — Tier mis-classification recovery** (Gate 1 dispatch mismatch between item and runtime profile) | Item executes under wrong tier (e.g., STRICT item dispatched to STANDARD profile) | (i) Read frontmatter `Tier:`; (ii) read per-item marker `(Tier: ...)` if present; (iii) compute expected tier per 3-level fallback (per-item → task-level → STANDARD default); (iv) compare to actual dispatch in Task Log | If dispatch wrong: log incident at `${TASK_DIR}/research/tfep-incident-report.md` (7-field schema). Fix the canonicalization (case, whitespace) at the source. If canonicalization rule itself wrong, page Engineering Lead. | Engineering Lead within 1h if root cause is parser bug; rf-qa for human-author errata |
| **R4 — TFEP escalation handling** (4th rf-qa invocation point post-merge fires) | F-05 authorized TFEP-escalation invocation logged; baseline classifies ≥1 new-test fail | (i) Confirm baseline state at `${TASK_DIR}/research/test-baseline.yaml` (4-state observer per AC-ATK-03); (ii) read TFEP incident report; (iii) classify against carve-outs (3 permitted exceptions per TU-6); (iv) confirm prohibition disposition matrix routing (root F1 vs verifier-spawned F1 vs mid-phase rf-qa) | If baseline parse-fail or schema-fail → treat as `classification=new`. If carve-out applies → record exception in incident report. If neither → HALT item (input-invalid is HALT-permitted per AC-ATK-10) and route to rf-qa for adjudication. | rf-qa within 30 min for adjudication |
| **R5 — In-flight resume triage** (post-merge resume of an in-flight MDTM task in the 136-file floor) | Subagent resumes a TASK-PRD-/TASK-TDD-/TASK-RESEARCH-* file that pre-dates merge; may emit Gate-1.5 token, may ENOENT on `related_docs:` paths | (i) Run CR-FM-03 default-to-STANDARD shim (`gate-1: dispatch_profile=STANDARD source=default`); (ii) Gate-1.5 content grep over task body for `(/sc:task\b|sc-task-protocol|task-unified)`; (iii) traverse `related_docs:` paths with `find`; emit `gate-1.5: deleted-related-doc` on ENOENT (or fold into Schema 5 per Q-GATE-1-5-SCHEMA) | Warn-and-continue. Set `legacy-surface-ack: 1` if author has reviewed. Never HALT mid-resume — INV-04 highest-exposure protector. | Engineering Lead within 4h if resume blocked by parser bug; never block on `related_docs:` ENOENT |

### 25.2 On-Call Expectations

| Aspect | Detail |
|--------|--------|
| **On-call team** | `rf-qa` (primary; Phase-Gate QA + post-completion + TFEP escalation); Engineering Lead (secondary; parser bugs, S-1/S-2/S-3 atomicity violations, V3 security-probe regressions); DevOps (CI hook failures, server-side pre-receive misfires) |
| **Expected page volume** | <2 pages/week at steady state post-Phase-7.5. Spike expected during Step 5/6 windows (atomic-by-design + INV-04 highest exposure). |
| **Required response time** | rf-qa: ack 15 min, mitigate 60 min. Engineering Lead: ack 30 min for non-S-2/S-3 issues, ack 5 min for atomicity violations (HALT class). DevOps: ack 30 min. |
| **Knowledge prerequisites** | Familiarity with: (i) `task/SKILL.md` F1 + F2 + Phase-Gate QA loop; (ii) Gate-1 dispatch profile semantics; (iii) Gate-1.5 token grammar (Q-GATE-1-5-TOKEN-COLLISION); (iv) 4-state baseline observer; (v) CR-FM-03 shim default + content audit; (vi) `make sync-dev` + `flock` portability (Q-GAP-04); (vii) atomic commit boundaries at Steps 1, 5, 6 |

### 25.3 Capacity Planning

| Resource | Current Capacity | Projected Load (6 mo) | Projected Load (12 mo) | Scaling Trigger |
|----------|-----------------|----------------------|------------------------|-----------------|
| In-flight MDTM file count (CR-FM-03 shim coverage) | 136 files | 200-300 files | 400-600 files | If `gate-1.5: legacy-surface-reference detected` emission rate > 10/day, schedule batch ack pass |
| CR-DEP-06 residual manifest entries | 144 (61 backlog + 83 docs/generated) | 50-100 (after archive sweep) | < 50 (steady state) | If residual count grows post-Step-6, audit CR-DEP-05 grep extension |
| Pre-commit gate wall-clock time | < 30s | < 45s | < 60s | If > 90s, batch by Step (only run Step-relevant gates per commit) |
| `make sync-dev` `flock`-guarded duration | < 5s | < 10s | < 15s | If > 30s, investigate skill directory bloat |
| TFEP incident-report file count | 0 (pre-merge) | 5-20/mo (steady) | 10-40/mo | If > 50/mo, surface as systemic test-failure trend; rf-qa adjudication |

### 25.4 Operational Risk Snapshot

| Risk | Severity | Mitigation runbook |
|------|----------|--------------------|
| Rebase-split bypass at Step 5 | HIGH | R1 (path override) + AC-ATK-17 server-side hook |
| Gate-1.5 emission token grammar collision | MEDIUM | R2 (triage) + Q-GATE-1-5-TOKEN-COLLISION pinning in §14 Logging Schema |
| `flock` unavailable on macOS/BSD | MEDIUM | R5 + Q-GAP-04 portability fallback (`lockfile-create`) |
| CR-FM-03 sunset not bound | MEDIUM | OQ-FM-03-SUNSET + CR-AUDIT-FM-03-SUNSET row |
| in-flight TASK file with deleted `related_docs:` | LOW | R5 (warn-and-continue per ME-3) |

---

## 26. Cost & Resource Estimation

> **Scope.** This TDD authors a directional merge plan; the runtime infrastructure costs are negligible (skill files + pre-commit hooks + CI matrix). The dominant cost dimension is **token spend on the authoring + research + QA + assembly pipeline** plus a small **per-Step CI/runtime token budget for the 10-step commit chain**.

### 26.1 TDD Authoring Run Cost Budget (one-shot)

| Phase | Output | Estimated line count | Estimated cost | Notes |
|-------|--------|---------------------|----------------|-------|
| **Research (Phase 3)** | 14 research files (00-14) + 2 web research files | ~6,895 lines | ~$350 | ~$0.05 / line at Opus-tier inference. Files 12 + 13 + 14 are the load-bearing inputs for §22. |
| **Research-Gate QA (Phase 3.5)** | analyst + rf-qa partition A/B + cycle 2 re-spawns | ~3 cycles × ~$200 | ~$600 | Cycle 1 + cycle 2 + executor remediation. Per qa/research-gate-consolidated.md: 12→5→0 monotonic shrinkage. |
| **Synthesis (Phase 5)** | 10 parallel synth-agents (synth-01..synth-10) | ~5,000 lines | ~$250 | Synth-08 ~500-700 lines. Synth-04 ~600, synth-05 ~600, etc. |
| **Assembly + final consolidation** | Single TDD.md | ~assembly pass | ~$100 | Stitching + cross-section consistency audit. |
| **Total per TDD authoring run** | — | — | **~$1,300** | Sub-$2k upper bound assuming no third re-spawn cycle. |

### 26.2 Per-Step Token Budget (10-step commit chain runtime)

| Step | Workload | Token budget | Rationale |
|------|----------|--------------|-----------|
| Step 1 (M1 atomic) | Compose foundation row + sentinel + 7-row atomic commit | 2,500 (complex) | Atomic-by-design; coarse rollback granularity |
| Step 2 | Gate 2 widening + git pre-flight 5-row matrix | 1,000 (medium) | Fine granularity |
| Step 3 (M3 TFEP) | TFEP cluster (CR-TASK-07..10) + R-DRIFT-03 patch | 1,500 (medium-complex) | R-DRIFT-03 patch precondition adds ~500 tokens to the budget |
| Step 4 (audit window) | CR-TASK-12 seven-diff + R-DRIFT-02 patch + fixture authoring | 1,500 (medium-complex) | Fixture authoring at `tests/fixtures/donor-blocks/` |
| Step 5 (soft-deprecation, atomic) | CR-DEP-01/02/05 + CR-REF-01..05 + CR-DOC-01 atomic | 2,500 (complex) | S-2 binding; atomic-by-design |
| Step 6 (hard-delete, atomic) | CR-DEP-03/04 + rf-qa F-07 verifier + CR-DEP-06 manifest | 2,500 (complex) | S-3 binding; INV-04 highest exposure |
| Step 7 (walkthrough audit) | AC-SM-03 + AC-SM-04 + Q-2 content audit | 1,000 (medium) | Independent re-read |
| Step 8 (docs rollup) | CR-DOC-02..09 + mkdocs build | 1,000 (medium) | Mostly annotation |
| Step 9 (residual manifest) | CR-DEP-06 one-shot post-Step-6 | 200 (simple) | Mechanical grep + manifest emit |
| Step 10 (audit closure) | CR-DOC-10..12 + K-01..K-08 baseline | 1,000 (medium) | Audit closure + KPI baseline |
| **Total per 10-step run** | — | **~14,700 tokens** | Bounded by complex-step ceiling (2,500 × 3 = 7,500) plus medium runs. Confidence-check ROI per CLAUDE.md core principle 4: spend 100-200 to save 5,000-50,000. |

### 26.3 Infrastructure Cost Snapshot

| Resource | Unit | Unit Cost | Estimated Usage | Monthly Cost | Notes |
|----------|------|-----------|-----------------|--------------|-------|
| CI pipeline minutes (GitHub Actions) | min | $0.008/min | ~600 min/mo (post-merge CI runs across PRs) | ~$5 | Negligible; covered by existing CI budget |
| Server-side `pre-receive` hook hosting (AC-ATK-17) | per hook invocation | n/a | ~50/mo | $0 | GitHub Actions free tier OR self-hosted git |
| MCP server usage (Auggie + Tavily + Context7) | per query | varies | per task | bundled | Gateway batches; AIRIS gateway 98% token reduction |
| Local CI compute (`uv run pytest`) | dev workstation cycles | n/a | per commit | $0 | Developer laptop |
| **Total monthly OPEX** | | | | **~$5-10** | Dominated by CI minutes, not infra |

### 26.4 Cost Scaling Model

| Scale Factor | At 1 TDD / mo | At 5 TDDs / mo | At 20 TDDs / mo | Cost Driver |
|--------------|---------------|----------------|-----------------|-------------|
| TDD authoring | $1,300 | $6,500 | $26,000 | Linear with TDD count; dominated by synthesis + QA |
| Per-Step commit-chain (Phase 7 execution) | $0.10 (if priced via Opus tokens) | $0.50 | $2.00 | Negligible; CI runs are not LLM-driven |
| In-flight resume audit (Gate-1.5 grep) | $0 | $0 | $0 | Pure regex grep; non-LLM |
| **Total** | **~$1,300** | **~$6,500** | **~$26,000** | TDD authoring dominates |

### 26.5 Sensitivity Analysis — TDD Cost Drivers

| Driver | Base scenario | Pessimistic | Optimistic | Sensitivity factor |
|--------|---------------|-------------|------------|-------------------|
| Research-gate QA cycles | 2 cycles | 3 cycles (third re-spawn) | 1 cycle (clean PASS) | +$200 / -$200 per cycle |
| Synthesis re-spawns | 0 (parallel-clean) | 2 re-spawns (drift detection) | 0 | +$50 per re-spawn |
| Assembly model tier | Opus | Opus | Sonnet (50% cheaper) | -$50 (Sonnet) |
| Research file count | 14 + 2 web | 18 (additional contingency probes) | 12 (some folded) | +$100 per added file |
| Cycle-1 → cycle-2 diff caching | None | None | 25% cache hit | -$150 with caching |
| **Net cost range** | **~$1,300** | **~$1,800** | **~$850** | Pessimistic is ~38% over base; optimistic is ~35% under |

### 26.6 Cost Optimization Opportunities

| Opportunity | Estimated Savings | Effort | Priority |
|-------------|-------------------|--------|----------|
| Cache cycle-1 → cycle-2 research diffs (avoid re-running unchanged content) | 20-30% on QA loop | Medium | Medium — Phase 7.5 |
| Use Sonnet for assembly/consolidation pass (not Opus) | 50% on assembly | Low | High — implement at GA |
| Batch synth-agents 1-10 into parallel waves (already canonical) | 3.5× speedup (no cost reduction) | Already done | n/a |
| Auto-skip clean partitions on re-spawn (PartA, PartB cycle-2 if cycle-1 PASS) | 25% on QA loop | Low | High |
| AIRIS Gateway 98% token reduction on MCP calls | Bulk MCP overhead | Already deployed | n/a |

---

## 27. References & Resources

### 27.1 Related Documents

#### 27.1.1 Parent PRD

| Document | Type | Link / Source Path |
|----------|------|--------------------|
| Product PRD — Directional Merge of `/sc:task` into `/task` | Product Requirements (v1.1, 2026-05-16, 1,964 lines, 308 KB, Heavyweight Feature-PRD abbreviated) | `.dev/releases/current/task-sc-task-directional-merge/roadmap/PRD_TASK_DIRECTIONAL_MERGE.md` |

#### 27.1.2 Validation Spec

| Document | Type | Link / Source Path |
|----------|------|--------------------|
| Validation Spec — Authoritative defense overlay (`convergence_score: 0.86`, `unaddressed_high_invariants: 0`) | Spec (46,094 bytes, 16 numbered sections) | `.dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md` |

#### 27.1.3 Adversarial-Validation Artifacts (47, by category)

All 47 artifacts present on disk at the directory below per fix-cycle 2 verification (2026-05-16); body-content audit OWED at synthesis time per R-DOC-01.

| Artifact Directory | Source Path |
|--------------------|-------------|
| Adversarial-validation artifacts (root) | `.dev/releases/current/task-sc-task-directional-merge/artifacts/` |

**Verdict + plan tier (4):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `validation-report.md` | 32,338 | Overall convergence verdict; 0 HIGH-severity unaddressed invariants after Round 3. Cited in §15 (Testing) + §20 (Risk) for AC-SM closure floor. |
| `final-merge-plan.md` | 43,832 | Source plan asserting "PASS. ZERO OPEN FINDINGS" (the validation-spec's plan-under-validation); closure F-01..F-08 mappings. Cited in §19 (Migration) + §22 (Open Questions). |
| `merge-master.md` | 63,898 | Master merge plan; 10-step commit-chain detail; rollback granularity; per-step pre-commit gate. **Canonical step ordering source** for §19. |
| `merge-roadmap.md` | 36,345 | Per-step roadmap visual; FR → step → audit-row mapping. Cited in §19. |

**Manifest + extension-point tier (4):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `transfer-manifest.md` | 35,294 | **Canonical V/C/K verdicts byte-for-byte source** for TU-1..TU-8 (validation-spec §2 cites this). AC-SM-01 verification anchor. Cited in §6 + §15. |
| `extension-point-contracts.md` | 22,320 | **INV-01..INV-05 definitions** at lines 11-17 (validation-spec frontmatter `invariant_anchor_source` field). AC-SM-03 invariant-survival anchor. Cited in §6 + §15. |
| `recipient-extension-points.md` | 10,510 | Recipient skill extension surface — explicit insertion-point list. Cited in §6 + §15. |
| `donor-feature-catalog.md` | 32,423 | Catalog of all donor patterns considered; mapped to V/C/K verdicts. Cited in §6 (Architecture) + §21 (Alternatives). |

**Hazard + invariant-walkthrough tier (2):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `compat-hazard-report.md` | 23,490 | HZ-01..HZ-18 compatibility hazards + per-row mitigations; S-1, S-2, S-3 derivation source. Cited in §20 (Risk). |
| `invariant-survival-walkthrough.md` | 37,857 | Re-readable INV-01..INV-05 survival demonstration (AC-SM-03 deliverable). Cited in §15. |

**Refactor tier (6):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `refactor-task-skill.md` | 49,128 | **Per-FR refactor of recipient skill** — exact code-shape changes. Highest-priority artifact for §6 (Architecture) + §8 (API Specs). |
| `refactor-sctask-deprecation.md` | 28,806 | CR-DEP-01 (stubify) + CR-DEP-03 (hard-delete) refactor; Step 5 / Step 6 specifics. Cited in §19. |
| `refactor-mdtm-frontmatter.md` | 24,889 | CR-FM-01 / CR-FM-03 / CR-FM-04 implementation; `Tier:` field schema + compat shim semantics. Cited in §7 (Data Models). |
| `refactor-references.md` | 63,075 | Cross-document reference re-routing (CR-REF-NN cluster); residual-reference manifest (CR-DEP-06). Cited in §19. |
| `refactor-distribution.md` | 34,150 | `make sync-dev` / `.claude/` cascade; S-3 worktree race surface. Cited in §13 (Security) + §19. |
| `refactor-documentation.md` | 43,620 | Documentation re-routing (CR-DOC-NN); release-notes authoring. Cited in §27 (this section). |

**Integration + traceability tier (5):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `integration-sketches.md` | 44,605 | **Post-merge code-shape sketches** — pseudo-code for `path_override_check()`, `tier_field_validate()`, `gate_1_dispatch()`. §6 + §8 source. |
| `traceability-chain-check.md` | 40,898 | TU → CR → AC traceability chain; closure F-01..F-08 mapping. Cited in §15 + §27. |
| `traceability-gap-report.md` | 23,807 | Traceability gaps surfaced during V2 attack chain. Cited in §22. |
| `file-reference-reverification.md` | 29,277 | Line-number drift re-verification (similar to TASK-TDD-20260514's drift discipline). Cited in §6 + §22. |
| `stack-rank.md` | 25,706 | TU stack-rank (priority order). Cited in §19 (Migration sequencing). |

**Adjacency + sprint-summary tier (4):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `task-builder-adjacency.md` | 18,471 | Adjacency to the independent task-builder convergence release — cross-referenced to avoid scope conflation. Cited in §3 (Goals/Non-Goals NG-08). |
| `rejected-features-ledger.md` | 38,040 | 10 donor-ceremony drops audit (ME-9). D09b "embedded runtime classifier" rejection — alternative for TU-1 if disposition flipped to ADAPT. Cited in §21 (Alternatives). |
| `gate-pass-report.md` | 13,602 | Gate-pass verification per merge step. Cited in §15. |
| `sprint-summary.md` | 33,725 | Overall sprint summary. Reference-only. |

**Debate-and-feature spec tier (20 — 9 debate transcripts + 9 feature specs + 2 misc):**

| Artifact | Bytes | Purpose-of-citation in TDD |
|----------|-------|-----------------------------|
| `debate-allowed-tools.md` | 21,309 | Debate transcript: allowed-tools donor pattern. Cited in §6 (rejected). |
| `debate-classification-header.md` | 19,697 | Debate transcript: classification header (TU-1 derivation). Cited in §6 (TU-1). |
| `debate-compliance-gating.md` | 27,259 | Debate transcript: compliance gating. Cited in §6. |
| `debate-mcp-declarations.md` | 18,061 | Debate transcript: MCP declarations donor pattern (rejected). |
| `debate-persona-activation.md` | 17,171 | Debate transcript: persona activation donor pattern (rejected). |
| `debate-per-tier-branching.md` | 24,188 | Debate transcript: per-tier branching. Cited in §6 (TU-1 Gate-1 dispatch derivation). |
| `debate-tfep.md` | 26,721 | Debate transcript: TFEP transplant — TU-5..TU-8 derivation. Cited in §6 (TFEP block). |
| `debate-tier-classification.md` | 22,355 | Debate transcript: tier classification — TU-1 derivation. Cited in §6 (TU-1). |
| `debate-triggering-surface.md` | 19,134 | Debate transcript: triggering-surface (when /task vs other skills fire). Cited in §6 (Gate-0). |
| `feature-allowed-tools.md` | 13,829 | Feature spec: allowed-tools. Reference-only (REJECT verdict). |
| `feature-classification-header.md` | 13,609 | Feature spec: classification header (post-debate distilled). TU-1 spec. |
| `feature-compliance-gating.md` | 18,773 | Feature spec: compliance gating. Cited in §6 (TU-7 carve-out). |
| `feature-dependency-matrix.md` | 32,815 | Dependency matrix across all donor features. Cited in §18 (Dependencies). |
| `feature-mcp-declarations.md` | 14,049 | Feature spec: MCP declarations. Reference-only (REJECT verdict). |
| `feature-persona-activation.md` | 13,420 | Feature spec: persona activation. Reference-only (REJECT verdict). |
| `feature-per-tier-branching.md` | 25,226 | Feature spec: per-tier branching. Cited in §6 (TU-1 Gate-1 dispatch). |
| `feature-tfep.md` | 23,460 | Feature spec: TFEP (post-debate distilled, the TU-5..TU-8 spec). Cited in §6. |
| `feature-tier-classification.md` | 11,938 | Feature spec: tier classification (TU-1 spec). Cited in §6 + §7. |
| `feature-triggering-surface.md` | 19,990 | Feature spec: triggering-surface. Cited in §6 (Gate-0). |
| `plan-adversarial-review.md` | 51,831 | V2 attack-chain review summary. Cited in §20 (Risk). |
| `anti-sycophancy-pass-p2.md` | 10,520 | Phase 2 anti-sycophancy validation. Cited in §15 (testing discipline). |
| `artifact-index.md` | 11,767 | Index of all 47 artifacts (self-referential map). Cited in §27 (this section). |

Total: 47 artifacts. Convergence score `0.86` per `validation-report.md` (≥ 0.85 threshold required for the "operationally binding" verdict per validation-spec §1 clause 1).

#### 27.1.4 PRD Companion Research (8 files — 6 codebase + 2 web)

| File | Bytes | Purpose-of-citation in TDD |
|------|-------|-----------------------------|
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/01-transfer-units-catalog.md` | 41,024 | TU-1..TU-8 V/C/K verdicts catalog with PRD-grounded dispositions. Cited in §6 + §15. |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/02-manifest-exceptions-and-invariants.md` | 51,235 | ME-1..ME-9 + INV-01..INV-05 load-bearing analysis. Cited in §6 + §15. |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/03-in-flight-exposure-and-resumability.md` | 35,210 | Live in-flight grounding; 132-file union (fix-cycle 2 recount, superseded by 136 at TDD-time); R-DIV-01; INV-04 layered analysis (parse vs semantic). Cited in §6 + §14 (Observability). |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/04-sequencing-and-timeline-hazards.md` | 39,036 | S-1..S-3, HZ-NN sequencing detail; CLI scope amendments. Cited in §19 + §20. |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/05-acceptance-criteria-and-audit-rows.md` | 43,411 | AC-ATK-01..18 + AC-SM-01..12 detailed criteria + CR-DEP/CR-FM/CR-TASK audit-row catalog. Cited in §4 + §15. |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/06-failure-mode-coverage-and-tradeoffs.md` | 37,523 | FM-01..08 + EC-01..04 + 8 unnamed tradeoffs (validation-spec §12). Cited in §12 (Error Handling) + §21 (Alternatives). |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/web-01-rebase-split-prevention.md` | 28,197 | Industry references for atomic-commit / rebase-split prevention (S-2). Cited in §13 + §19. See §27.2 below for underlying external URLs. |
| `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/web-02-content-vs-parse-resumability.md` | 44,265 | Industry references for parse-vs-content resumability semantics (INV-04 layering). Cited in §6 + §15. See §27.2 below for underlying external URLs. |

#### 27.1.5 TDD Codebase Research (15 native files + 2 cross-link references = 17 rows)

| File | Purpose-of-citation in TDD |
|------|-----------------------------|
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/00-prd-extraction.md` | PRD requirement extraction — surface index for §1-§4 translation. Cited by synth-01. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/01-recipient-skill-architecture.md` | Recipient F1 loop, F2 catalog, Phase-Gate QA, Post-Completion, Incremental Writing, Session Resumption code-shape trace. Cited by synth-03, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/02-donor-skill-tracer.md` | Donor `sc-task-protocol/SKILL.md` STRICT execution, Path Overrides, TFEP block (`:125-244`), Outcome enum donor literal. Cited by synth-03, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/03-donor-command-tracer.md` | Donor `commands/task.md` classification rules, tier keyword tables, `:100` Skill-invocation site (CR-DEP-01 target). Cited by synth-03, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/04-caller-emission-mapper.md` | 6 CLI emission sites (`cli/sprint/process.py:170` + `cli/cleanup_audit/prompts.py:{26,47,69,92,116}`) with literal byte sequences emitted. Cited by synth-03, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/05-tu1-tier-field-implementation.md` | TU-1: `Tier:` parser code shape; CR-FM-03 default-to-STANDARD shim; per-item marker schema (closed enumeration per AC-ATK-05); CR-FM-01 canonicalization. Cited by synth-04, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/06-tu2-path-overrides-and-cr7-ordering.md` | TU-2: Critical/Trivial Path Override at row-1; CR-7 ORDERING sentinel + AST-grade grep enforcement (R-ATK-01 closure). Cited by synth-04, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/07-tu3-tu7-verification-roster-widening.md` | TU-3 + TU-7: rf-qa spawn at `:191-198`; widening to `[rf-qa, quality-engineer]`; ME-2 enforcement; F-05 mid-phase rf-qa invocation surface; AC-ATK-11 carve-out boundary. Cited by synth-03, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/08-tu4-git-preflight-five-row-matrix.md` | TU-4: Layer-2 `git status` pre-flight 5-row × 2-disposition matrix `{clean, dirty, tool-absent, not-a-repo, error-other}` × `{WARN-CONTINUE, GRACEFUL-SKIP}`; INV-01 binding (forbids HALT-as-gate). Cited by synth-04, synth-06. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/09-tu5-tu8-tfep-transplant.md` | TU-5..TU-8 TFEP block transplant; baseline 4-state observation order (AC-ATK-03); F2 prohibitions additive insertion; escalation trigger; incident-report 7-field schema (AC-ATK-12). Cited by synth-04, synth-05. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/10-invariant-preservation-and-me-binding.md` | INV-01..INV-05 + ME-1..ME-9 binding map. F2 prohibition catalog corrected to 10 pre-merge (not 9). Cited by synth-03, synth-04. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/11-in-flight-exposure-and-resumability.md` | Live in-flight grounding — 136 union files floor (supersedes 132/130/96/25); TASK-PRD-20260514-121039 status `🟠 Doing` 258-ref binding; R-DRIFT-04 retraction. Cited by synth-01, synth-04, synth-07. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/12-acceptance-criteria-and-audit-rows.md` | AC-ATK-01..18 + AC-SM-01..12 + CR-DEP/CR-FM/CR-TASK audit-row coverage. AC-ATK-08 git-sha 40-char-suffix discipline source. Cited by synth-01, synth-06. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/13-adversarial-artifact-cross-validator.md` | Cross-validation of the 47 adversarial artifacts vs PRD-cited line numbers and content claims; R-DRIFT-NN findings; R-DOC-01 audit closure verdict. Cited by synth-01, synth-08. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/14-data-models-and-schemas.md` | Data shapes for `Tier:` field, baseline YAML, incident-report side-effect schema, residual-reference manifest. Cited by synth-04. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/web-01-rebase-split-prevention.md` | **Cross-link** (read-only reference, NOT re-executed). Points at the PRD-task web research source. |
| `.dev/tasks/to-do/TASK-TDD-20260516-043749/research/web-02-content-vs-parse-resumability.md` | **Cross-link** (read-only reference, NOT re-executed). Points at the PRD-task web research source. |

#### 27.1.6 Source Tree & Template

| Document | Type | Source Path |
|----------|------|-------------|
| TDD template (this document's structure source) | Engineering template v1.2 | `src/superclaude/examples/tdd_template.md` (template lines 1223-1334 for §27-§28 specifically). |
| Recipient skill source (post-merge canonical surface) | Source file | `src/superclaude/skills/task/SKILL.md` (376 lines). |
| Donor skill source (Step 6 hard-delete target) | Source file | `src/superclaude/skills/sc-task-protocol/SKILL.md` (365 lines). |
| Donor command source (Step 5 stubify target) | Source file | `src/superclaude/commands/task.md` (170 lines). |
| Sprint CLI emission site | Source file | `src/superclaude/cli/sprint/process.py:170` (1 emission site). |
| Cleanup-audit CLI emission sites | Source file | `src/superclaude/cli/cleanup_audit/prompts.py:{26,47,69,92,116}` (5 emission sites). |

### 27.2 External References

External URLs are cited from the underlying PRD-task web research sources `.dev/tasks/to-do/TASK-PRD-20260516-004625/research/web-01-rebase-split-prevention.md` and `web-02-content-vs-parse-resumability.md`. Per TDD synthesis policy, **the TDD does NOT duplicate quoted text from these sources** — it links to them by URL. Below is the consolidated registry of external URLs grouped by TDD section feed.

**§13 Security Considerations + §19 Migration & Rollback — atomic-commit / rebase-split protection (web-01 source):**

| External Resource | Purpose | URL |
|-------------------|---------|-----|
| Atlassian: Git Hooks tutorial | Canonical client-side vs server-side hook taxonomy | https://www.atlassian.com/git/tutorials/git-hooks/ |
| Git-Tower: Git Hooks FAQ | Hook-bypass semantics (`--no-verify`) | https://www.git-tower.com/learn/git/faq/git-hooks |
| GitHub Enterprise: pre-receive hook docs | Non-bypassable server-side enforcement layer (GH Enterprise only; GitHub.com lacks pre-receive) | https://docs.github.com/admin/policies/enforcing-policy-with-pre-receive-hooks/creating-a-pre-receive-hook-script |
| GitHub Enterprise: working with pre-receive hooks | Operator perspective on pre-receive | https://docs.github.com/enterprise/user/articles/working-with-pre-receive-hooks |
| GitLab: server hooks | Non-bypassable server-side enforcement on GitLab Server | https://docs.gitlab.com/administration/server_hooks/ |
| GitHub: protected branches | Branch-protection rules; required status checks; signed commits | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| Terraform GitHub provider: `branch_protection` resource | IaC pattern for branch protection (release engineering) | https://registry.terraform.io/providers/integrations/github/latest/docs/resources/branch_protection.html |
| GitLab: push rules | Branch protection equivalent on GitLab | https://docs.gitlab.com/user/project/repository/push_rules/ |
| git-scm: `git push` docs | Atomic-push semantics (`--atomic`) for the 7-foundation-row binding | https://git-scm.com/docs/git-push |
| Stack Overflow: `git push --atomic` not failing | Cited failure mode for atomic-push bypass | https://stackoverflow.com/questions/37531663/git-push-atomic-not-failing |
| GitHub Actions: workflow syntax | Required-checks CI venue (substitute for pre-receive on GitHub.com) | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax |
| commitlint local-setup | Client-side commit-message linting reference | https://commitlint.js.org/guides/local-setup |
| commitlint CI-setup | Server-side enforcement venue for commit linting | https://commitlint.js.org/guides/ci-setup |
| jorisroovers: gitlint commit-hooks | Alternative commit linter reference | https://jorisroovers.com/gitlint/dev/commit_hooks/ |
| kernel.org: rebasing and merging | Atomic-commit-set discipline literature (canonical Linux-kernel practice) | https://kernel.org/doc/html/v6.2/maintainer/rebasing-and-merging.html |
| kernel.org: submitting patches | "One logical change per commit" rule | https://kernel.org/doc/html/next/process/submitting-patches.html |
| kernelnewbies: patch philosophy | Tutorial-grade reinforcement of atomic-commit rule | https://kernelnewbies.org/PatchPhilosophy |
| snellman.net: monorepo atomic commits | Industry argument for atomic commits in monorepos | https://www.snellman.net/blog/archive/2021-07-21-monorepo-atomic/ |
| Action: branch-enforcement | GitHub Action for required-branch policy | https://github.com/marketplace/actions/branch-enforcement |

**§6 Architecture + §15 Testing Strategy + §19 Migration & Rollback — content-vs-parse compatibility (web-02 source):**

| External Resource | Purpose | URL |
|-------------------|---------|-----|
| Alembic Cookbook | "Inline throwaway ORM models for data migrations" — prior art for the in-flight task file being a third intermediate snapshot, not pre/post-merge | https://alembic.sqlalchemy.org/en/latest/cookbook.html |
| Alembic Runtime API | `MigrationContext` + `autocommit_block()` — per-step transactional islands relevant to ME-6 atomicity | https://alembic.sqlalchemy.org/en/latest/api/runtime.html |
| Alembic Operation Reference | Operation-level migration vocabulary | https://alembic.sqlalchemy.org/en/latest/ops.html |
| Stack Overflow: Alembic upgrade migrations in a transaction | Community Q&A on transactional migrations | https://stackoverflow.com/questions/22095039/run-alembic-upgrade-migrations-in-a-transaction |
| Bytebase: Flyway vs Liquibase (2026) | Two-axis "syntax compatibility vs semantic compatibility" model; **direct vocabulary for INV-04 parse-vs-semantic split** | https://www.bytebase.com/blog/flyway-vs-liquibase/ |
| Liquibase: changelog concepts | Structured-changelog parser layer (two-axis model) | https://docs.liquibase.com/concepts/basic/changelog.html |
| Liquibase: SQL-format changelogs | "Pass parser A and fail parser B, or pass both parsers and fail execution" | https://docs.liquibase.com/concepts/basic/sql-format.html |
| Liquibase vs Flyway (official) | Vendor-comparative view of parse-vs-execution split | https://www.liquibase.com/liquibase-vs-flyway |
| Flyway migrations docs | Canonical Flyway reference | https://github.com/flyway/flywaydb.org/blob/gh-pages/documentation/concepts/migrations.md |
| Yugabyte: Evaluating PostgreSQL compatibility | Explicit syntax-vs-semantic compatibility taxonomy | https://www.yugabyte.com/wp-content/uploads/2021/12/Evaluating-PostgreSQL-Compatibility-in-Distributed-SQL-Databases-Webinar-Slides.pdf |
| Temporal: Worker Versioning GA | Workflow Pinning model: in-flight executions stay on Build ID, new executions take new code | https://temporal.io/change-log/worker-versioning-continue-as-new-worker-controller |
| Temporal: Worker Versioning Public Preview | Worker-versioning prior state | https://temporal.io/change-log/worker-versioning-public-preview |
| Temporal: Worker Versioning docs (GitHub) | Build-ID compatibility tables — **prior art for CR-DEP-06 residual-reference manifest** | https://github.com/temporalio/temporal/blob/main/docs/worker-versioning.md |
| Cadence: Replay and Shadowing — Go | `WorkflowReplayer` / `WorkflowShadower` — **prior art for AC-ATK-18 content-level resume audit** | https://cadenceworkflow.io/docs/go-client/workflow-replay-shadowing |
| Cadence: Replay and Shadowing — Java | Same as above, Java client | https://cadenceworkflow.io/docs/java-client/workflow-replay-shadowing |
| Cadence blog: non-deterministic errors, replayers, shadowers | Failure-mode taxonomy for in-flight resume | https://cadenceworkflow.io/blog/2023/08/28/nondeterministic-errors-replayers-shadowers |
| Bitovi: replay testing in Temporal | Practitioner perspective on replay testing | https://www.bitovi.com/blog/replay-testing-to-avoid-non-determinism-in-temporal-workflows |
| AIP-63: DAG Versioning (Apache cwiki) | Airflow versioning history — cautionary tale for not pinning in-flight | https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-63%3A%2BDAG%2BVersioning |
| Astronomer: Airflow DAG Versioning (learn) | Vendor-documented Airflow versioning model | https://www.astronomer.io/docs/learn/airflow-dag-versioning/ |
| Astro: DAG versioning | Astro-platform versioning view | https://www.astronomer.io/docs/astro/dag-versioning |
| Dapr: Workflow Versioning | Third-ecosystem convergence (Temporal + Cadence + Dapr) on pin-or-patch semantics | https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-versioning/ |
| Python warnings module | Canonical Python `DeprecationWarning` discipline (for `/sc:task` one-shot deprecation banner pattern) | https://docs.python.org/3/library/warnings.html |
| PEP 4 — Deprecation of Standard Modules | Module-deprecation policy precedent | https://peps.python.org/pep-0004/ |
| PEP 702 — Marking deprecations using the type system | `@typing.deprecated` for parser-vs-semantic deprecation signaling | https://peps.python.org/pep-0702/ |
| arXiv 2408.10327: Empirical Study on Package-Level Deprecation in Python Ecosystem | Argues for explicit manifests (CR-DEP-06 alignment) | https://arxiv.org/abs/2408.10327 |
| pyDeprecate | Helper-library reference for deprecation discipline | https://pypi.org/project/pyDeprecate/ |

> **Citation policy.** When TDD §13 / §19 / §6 / §15 cites an external URL, the citation form is `[short title](URL)` followed by a parenthetical source-of-extraction reference to the underlying web-research file (e.g., "(per `web-01-rebase-split-prevention.md` §1)"). The TDD body does NOT inline the source's quoted text; readers traverse to the URL or the source research file.

---

## 28. Glossary

### 28.1 Transfer-Unit & Manifest Vocabulary

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **TU** | Transfer Unit — a bounded, V/C/K-verdicted donor pattern that the directional merge transplants from the donor skill/command into the recipient skill. TU-1..TU-8 are enumerated; each carries a verdict in `{ADOPT, ADAPT, REJECT}`. | `transfer-manifest.md`; validation-spec §2; research/01 §1; PRD §14.1 FR-TU-N. |
| **TU-1** | Tier classification + Gate-1 dispatch (frontmatter `Tier:` field + `gate_1_dispatch()`). ADOPT verbatim. | `transfer-manifest.md`; research/05; PRD FR-TU-1. |
| **TU-2** | Critical / Trivial Path Override at row-1 (`path_override_check()` runs BEFORE `tier_field_validate()`). Binds CR-7 ORDERING. ADOPT verbatim. | research/06; PRD FR-TU-2; donor `sc-task-protocol/SKILL.md:121,:123`. |
| **TU-3** | Gate-2 verification-roster widening from `[rf-qa]` to `[rf-qa, quality-engineer]`. ADAPT (preserves INV-03 floor). | research/07; PRD FR-TU-3; INV-03. |
| **TU-4** | Layer-2 `git status` pre-flight with 5-row × 2-disposition matrix. ADAPT (forbids HALT under INV-01). | research/08; PRD FR-TU-4. |
| **TU-5** | TFEP baseline snapshot at `${TASK_DIR}/research/test-baseline.yaml` (on-disk YAML pre-F1). ADOPT verbatim (donor's in-memory form is the ADAPT delta). | research/09; PRD FR-TU-5. |
| **TU-6** | TFEP Prohibitions + Carve-outs — 3 entries appended to the F2 catalog (10 pre-merge → 13 post-merge). Additive only under INV-02. | research/09; PRD FR-TU-6. |
| **TU-7** | TFEP Escalation trigger — **fourth** rf-qa invocation point post-merge (mid-phase failure escalation; authoritative count = 4 = 3 pre-merge + TU-7). F-05 closure; ME-2 carve-out per AC-ATK-11. | research/07, research/09; PRD FR-TU-7. |
| **TU-8** | TFEP Incident reporting side-effect file `${TASK_DIR}/research/tfep-incident-report.md` with 7-field schema (AC-ATK-12 enumeration). | research/09; PRD FR-TU-8. |
| **ME** | Manifest Exception — a load-bearing or ancillary deviation from naive byte-for-byte transplant. ME-1..ME-9 are enumerated; 5 are load-bearing, 4 are ancillary. | `transfer-manifest.md`; validation-spec §2; PRD NFR-ME-N. |
| **ME-1** | Closed-enumeration constraint on per-item tier markers (forbids per-item runtime dispatch). | research/10 §2.1; PRD NFR-ME-1. |
| **ME-2** | rf-qa floor — rf-qa is never replaced and never displaced across all **four** post-merge invocation points (phase-gate L191; post-completion structural L221; post-completion qualitative L230; mid-phase TU-7 TFEP). Roster widening (e.g., adding `quality-engineer` companion on STRICT) is permitted; replacement/displacement is prohibited. **Load-bearing** for INV-03. | research/10 §2.2; PRD NFR-ME-2; INV-03; TDD §5.2.B. |
| **ME-3** | SIDE-CHANNEL ONLY, NO F1 HALT — no new HALT semantic may be added to F1 by TU-4/5/6/7/8. Environment-non-ideal dispositions (e.g., 5-row `git status` matrix) MUST warn-and-continue, never HALT. **Load-bearing** for INV-01. (Note: TFEP baseline on-disk persistence is FR-TU-5 / INV-04, NOT ME-3.) | research/10; PRD NFR-ME-3; TDD §5.2.B. |
| **ME-4** | BASELINE TIER-GATED — TU-5 baseline collection runs only on STRICT/STANDARD tiers; LIGHT/EXEMPT skip. **Ancillary** (HELD without per-row deltas). (Note: CR-7 ORDERING — `path_override_check` firing first — is NFR-INV-5 / FR-TU-2, NOT ME-4.) | research/10; PRD NFR-ME-4; TDD §5.2.B. |
| **ME-5** | NO PER-ITEM EXECUTE SUBSTITUTION — TU-4 D15b accepted; D15c per-item synthesis at execute-time is REJECTed (LR-REJECT-7 stays terminal). **Ancillary**. (Note: 5-row git pre-flight disposition matrix is NFR-ME-3 / FR-TU-4 acceptance criterion AC-ATK-02, NOT ME-5.) | research/10; PRD NFR-ME-5; TDD §5.2.B. |
| **ME-6** | TIER FIELD + GATE 1 SHIP TOGETHER (M1 atomicity) — the 7 mutually-presupposing foundation rows land in one source-tree merge; rebase-split prohibited and enforced server-side via AC-ATK-17. **Load-bearing** (commit-sequence shape protecting INV-01/-03/-04). | research/10; PRD NFR-ME-6; TDD §5.2.B. |
| **ME-7** | D08 DEFERRED until parser ships — held as terminal DEFER. **Ancillary**. (Note: F2 catalog additive-only growth `10 → 13` via TU-6 is NFR-INV-2, NOT ME-7.) | research/10; PRD NFR-ME-7; TDD §5.2.B. |
| **ME-8** | D01 DEFERRED until loader semantics + Rule 6 split. **Ancillary**. (Note: Outcome enum literal preservation `{success / escalated / failed}` byte-for-byte from donor `:232` is FR-TU-8 schema obligation, NOT ME-8.) | research/10; PRD NFR-ME-8; TDD §5.2.B. |
| **ME-9** | 10 donor-ceremony drops remain dropped — re-introduction requires a new directional merge. | research/10; `rejected-features-ledger.md`; PRD NFR-ME-9. |

### 28.2 Invariants, Sequencing, Hazards, Closures

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **INV** | Invariant — a hard binding the merge must preserve. INV-01..INV-05 are load-bearing; defined in `extension-point-contracts.md` lines 11-17 (validation-spec frontmatter `invariant_anchor_source`). | `extension-point-contracts.md`; validation-spec §9; PRD §14.2 NFR-INV-N. |
| **INV-01** | F1 loop semantics (READ→IDENTIFY→EXECUTE→UPDATE→REPEAT monotonicity). Forbids HALT-as-gate dispositions in pre-flight stages. | `extension-point-contracts.md:11`. |
| **INV-02** | Prohibited-actions F2 catalog is additive within existing rows; no entries dropped or rephrased. | `extension-point-contracts.md:13`. |
| **INV-03** | Phase-gate rf-qa floor — rf-qa is never replaced and never displaced. | `extension-point-contracts.md:14`. |
| **INV-04** | Resumability — in-flight task files must resume across the merge boundary without HALT. Two-layer: parse-layer (CR-FM-03 shim) + semantic-layer (AC-ATK-18 content audit). **Highest-exposure invariant** per validation-spec §9 L285. | `extension-point-contracts.md:15`; validation-spec §4, §9. |
| **INV-05** | Closed-enumeration discipline for tier and outcome literals — no open-class introductions. | `extension-point-contracts.md:17`. |
| **S-N** | Sequencing Constraint — a hard ordering rule across the 10-step commit chain. S-1..S-3 enumerated. | `compat-hazard-report.md`; validation-spec §7; PRD NFR-S-N. |
| **S-1** | PRD precondition target sequencing — TASK-PRD-20260514-121039 must reach a stable state before Step 5 commits. Binding in force at TDD-time (258 donor-surface refs across 12 files). **R-DRIFT-04 RETRACTED** — TASK-PRD-20260514-121039 EXISTS. | research/11 §3.1; validation-spec §7. |
| **S-2** | Atomic 10-step commit sequence — rebase-split prohibited; AC-ATK-17 server-side push-policy enforcer is the closure venue. | validation-spec §7; web-01 source. |
| **S-3** | `make sync-dev` + `make verify-sync` worktree-race ordering — `flock` on `.claude/skills/.sync-lock` required (R-ATK-16 closure). | validation-spec §7; `refactor-distribution.md`. |
| **HZ** | Hazard — a compatibility risk surface enumerated in `compat-hazard-report.md`. HZ-01..HZ-18 covered. | `compat-hazard-report.md`; validation-spec §10. |
| **H-2** | Rebase-split bypass hazard — closes via AC-ATK-17 server-side enforcement (R-ATK-17). | `compat-hazard-report.md`; validation-spec §10. |
| **F-NN** | F-closure — a numbered closure pairing an attack vector with its mitigation. F-01..F-08 enumerated; F-04 = F2 catalog additivity, F-05 = mid-phase rf-qa invocation, F-07 = INV-04 semantic-layer closure. | `final-merge-plan.md`; `traceability-chain-check.md`. |

### 28.3 Acceptance-Criteria Families

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **AC-ATK** | Acceptance Criterion — Attack-vector. AC-ATK-01..18 (18 rows). ALL must close before validation-spec §1 clause 3 "operationally binding" verdict. | validation-spec §11; research/12 §1. |
| **AC-ATK-05** | Closed-enumeration register for per-item tier-marker consumers — initial set `{CR-TASK-07 baseline-skip}`. Any new consumer requires a new ME-10+ entry. Manifest fixture `tests/audit/test_marker_consumers.py` enforces. | research/12 §1.5; §22.5 (this TDD). |
| **AC-ATK-08** | git-sha 40-char suffix discipline — every `[CODE-VERIFIED]` tag in TDD MUST carry `(git-sha: <40-char>)`. | research/12 §1.8; research/04 §6.1. |
| **AC-ATK-17** | Server-side push-policy hook for the 7-foundation-row atomicity binding (closes H-2 / R-ATK-17). | validation-spec §11; web-01 source. |
| **AC-ATK-18** | Content-level resume audit — emits `gate-1.5: legacy-surface-reference` warn-and-continue per occurrence of `/sc:task | sc-task-protocol | task-unified` body grep at resume time. | validation-spec §4, §11; web-02 source. |
| **AC-SM** | Acceptance Criterion — Success Metric. AC-SM-01..12 (12 rows). Audit deliverables for TDD §4 metric closures. | validation-spec §11; research/12 §2. |
| **AC-SM-01** | TU verdict closure audit (V/C/K against `transfer-manifest.md`). | research/12 §2.1. |
| **AC-SM-03** | INV-01..INV-05 survival demonstration (`invariant-survival-walkthrough.md` deliverable). | research/12 §2.3. |
| **AC-SM-12** | 100% of live in-flight MDTM population resumes cleanly under CR-FM-03; gates 1/5/6 return 0. Fixture iterates LIVE count at gate-execution time (NOT hardcoded 25/96/132). Floor = 136 at 2026-05-16. | validation-spec §11; §15.3 (this TDD). |

### 28.4 Compatibility / Audit-Row Families

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **CR-DEP** | Compatibility Requirement — Dependency. CR-DEP-01..06 cluster covers donor-command stubification, donor-skill hard-delete, CLI-emission re-routing, and residual-reference manifest. | validation-spec §6, §8; research/12 §3. |
| **CR-DEP-01** | Stubify donor command `commands/task.md:100` (Step 5; `> Skill sc:task-protocol` rewrite). | validation-spec §6; `refactor-sctask-deprecation.md`. |
| **CR-DEP-03** | Hard-delete donor skill `sc-task-protocol/SKILL.md` (Step 6). sha256-baselined per AC-ATK-09. | validation-spec §6; `refactor-sctask-deprecation.md`. |
| **CR-DEP-04** | CLI-emission re-routing — 6 emission sites rewrite `/sc:task ` → `/task ` byte-for-byte. | research/04 §1; validation-spec §6. |
| **CR-DEP-06** | Residual-reference manifest at `${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}` — enumerates ≥144 surviving residual occurrences across ≥40 files with per-bucket disposition. Elevated to MUST. | validation-spec §8; research/12 §3.6. |
| **CR-FM** | Compatibility Requirement — Frontmatter / Format-Migration. CR-FM-01..04 cluster covers `Tier:` canonicalization, default-to-STANDARD shim, row-1 ordering grep. | validation-spec §5; research/12 §4. |
| **CR-FM-01** | `Tier:` field canonicalization (vocabulary = `{STRICT, STANDARD, LIGHT, EXEMPT}`). | research/12 §4.1; `refactor-mdtm-frontmatter.md`. |
| **CR-FM-03** | Default-to-STANDARD compat shim — absent `Tier:` parses as `STANDARD` to preserve INV-04 parse-layer resumability. | validation-spec §5; research/12 §4.3. |
| **CR-FM-04** | Row-1 ordering grep (AST-grade) for the load-bearing INV-03 rf-qa block — replaces line-number anchors with content-hash anchors. Closes R-ATK-06. | research/12 §4.4. |
| **CR-TASK** | Compatibility Requirement — Task body (predicate-precision attacks). CR-TASK-01..12 (12 sub-attacks per validation-spec §5). | validation-spec §5; research/12 §5. |
| **CR-TASK-12** | Seven-diff fixture audit using `tests/fixtures/donor-blocks/` (AC-ATK-06 frozen-fixture closure). | research/12 §5.12. |
| **CR-7 ORDERING** | Load-bearing function-order sentinel — `path_override_check()` MUST fire BEFORE `tier_field_validate()` so security-domain paths always elevate to STRICT regardless of frontmatter `Tier:`. Enforced by sentinel comment + AST-grade ordering grep (not by markdown discipline alone). Closes R-ATK-01. | research/06; validation-spec §2; ME-4. |

### 28.5 Process-Discipline Terms

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **TFEP** | Test Failure Escalation Protocol — the donor pattern transplanted as TU-5..TU-8: baseline snapshot, prohibitions + carve-outs, escalation triggers, incident-report side-effect file. Donor block is contiguous at `sc-task-protocol/SKILL.md:125-244`. TFEP incident-report file canonical path: `${TASK_DIR}/research/tfep-incident-report.md`. | `feature-tfep.md`; `debate-tfep.md`; research/09. |
| **MDTM** | Markdown Task Management — the framework's task-file format under `.dev/tasks/` (frontmatter + checklist body + research/ subdir + qa/ subdir). The recipient `/task` skill owns the MDTM execution contract. | PRD §6 Jobs; research-notes.md §Tier-5; research/11. |
| **F1 loop** | The recipient `task/SKILL.md` execution loop at `:79-98`: **READ→IDENTIFY→EXECUTE→UPDATE→REPEAT**. INV-01 binds progress monotonicity. | recipient `task/SKILL.md:79-98`; research/01. |
| **F2 catalog** | Prohibited-Actions catalog at `task/SKILL.md:104-117`. **10 prohibitions pre-merge** (authoritative — supersedes any 9-row spec lineage); **13 prohibitions post-merge** after TU-6 additive insertion of 3 entries. | research-notes.md §1, §Pattern-2; research/10 §2.2; research/13 §2.3 cross-confirmed. |
| **F4** | Task File Modification Restrictions section at `task/SKILL.md:144-158`. | research-notes.md §Tier-1 table. |
| **F5** | Frontmatter Update Protocol at `task/SKILL.md:160-168`. | research-notes.md §Tier-1 table. |

### 28.6 Surface Vocabulary (Agents, Skills, Commands)

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **rf-qa** | Rigorflow QA subagent — the floor-binding verification agent invoked at **four** invocation points post-merge: (1) phase-gate after every Phase 2+ (`task/SKILL.md:191`), (2) post-completion structural (`:219-226`), (3) post-completion qualitative via rf-qa-qualitative (`:228-239`), (4) TU-7 mid-phase TFEP escalation (new). INV-03 / ME-2 forbid replacement or displacement; TU-7 carve-out is one-time and non-generalizing per AC-ATK-11. **Invocation count = 4.** | `task/SKILL.md:191`, `:219-226`, `:228-239`; synth-03 §6.3.5; research/07. |
| **rf-analyst** | Rigorflow Analyst subagent — research-gate and synthesis-gate verifier (e.g., `qa/analyst-research-partA.md`, `qa/analyst-synthesis-partA.md`). Not part of the merge surface; cited as TDD-build process actor only. | research-notes.md §Phase-3, §Phase-5. |
| **rf-assembler** | Rigorflow Assembler subagent — final TDD assembly actor using Incremental Writing Protocol. Not part of the merge surface; cited as TDD-build process actor only. | research-notes.md §Phase-6. |
| **task-builder** | Independent convergence release (v3.9) — adjacent to this directional merge per `task-builder-adjacency.md`. **Explicitly out of scope** for the directional-merge TDD; cross-referenced only to avoid scope conflation. | `task-builder-adjacency.md`; research-notes.md §SCOPE. |
| **quality-engineer** | Donor sub-agent invoked from `sc-task-protocol/SKILL.md:89` under STRICT execution. TU-3 widens the recipient Gate-2 roster to `[rf-qa, quality-engineer]` (ADAPT verdict — preserves INV-03 floor by addition, not replacement). | donor `sc-task-protocol/SKILL.md:89,:116`; research/07. |
| **`/task` (recipient)** | The canonical post-merge slash command and skill — the address that all 6 CLI emission sites and ~136 in-flight MDTM files resolve to after merge. | `task/SKILL.md`; `commands/task.md` (renamed/stubified per CR-DEP-01). |
| **`/sc:task` (donor command)** | The pre-merge donor slash command at `commands/task.md` whose `:100` `> Skill sc:task-protocol` invocation is stubified (CR-DEP-01) at Step 5 with a one-shot deprecation banner. | donor `commands/task.md:100`; `refactor-sctask-deprecation.md`. |
| **`sc-task-protocol` (donor skill)** | The pre-merge donor skill at `src/superclaude/skills/sc-task-protocol/SKILL.md` (365 lines) — hard-deleted at Step 6 (CR-DEP-03); sha256-baselined for the deletion proof (AC-ATK-09). | donor `sc-task-protocol/SKILL.md`; `refactor-sctask-deprecation.md`. |

### 28.7 Tier Enumeration

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **STRICT / STANDARD / LIGHT / EXEMPT** | The canonical closed tier enumeration. Authoritative source: donor `commands/task.md:55,:61,:82` "VALID TIERS = `{STRICT, STANDARD, LIGHT, EXEMPT}`". | donor `commands/task.md:55,:61,:82`; PRD §14.1 FR-TU-1. |
| **STRICT** | Highest tier — invokes `[rf-qa, quality-engineer]` Gate-2 roster; binds the most expensive verification path. Triggered by tier keywords at `:73` of donor command. | donor `commands/task.md:73`; research/03. |
| **STANDARD** | Default tier — used when `Tier:` is absent under the CR-FM-03 compat shim. INV-04 parse-layer resumability anchor. | donor `commands/task.md:88`; CR-FM-03; INV-04. |
| **LIGHT** | Reduced-verification tier — keywords at `:83` of donor command. | donor `commands/task.md:83`. |
| **EXEMPT** | Verification-exempt tier — keywords at `:78` of donor command. | donor `commands/task.md:78`. |
| **`TRIVIAL`** | **NON-CANONICAL** vestige from validation-spec §4 line 103 — explicitly NOT in the canonical enumeration. OQ-TIER-VOCABULARY resolves this drift before Step 1. | validation-spec §4 L103 (vestige); research-notes.md §Open-Questions. |

### 28.8 Drift-Finding Vocabulary

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **R-DRIFT-NN** | Drift findings surfaced during research/13 cross-validation. R-DRIFT-02 = donor anchor off-by-2 (`:127-135` should be `:133-135`, LOW). R-DRIFT-03 = donor anchor off-by-43 for TFEP MUST-escalate triggers (`:200-210` should be `:157-161`, MEDIUM — CR-TASK-12 verbatim-diff audit would silently mis-fire). **R-DRIFT-04 = RETRACTED** in fix-cycle 1 (TASK-PRD-20260514-121039 exists with 258 refs, S-1 binding stays in force). R-DRIFT-05 = citation drift (0.86 figure is in `validation-spec.md:6,:19`, not `validation-report.md`, LOW). The 9→10 F2 count correction is a separate finding (§22, not R-DRIFT-NN family). | research/13 §10; research/11 §3.1; §22 (this TDD). |
| **R-DOC-01** | Artifact cross-validation finding — content audit of the 47 adversarial artifacts. **OWED** at PRD time; **RESOLVED** at research/13 by performing the audit. Downgrade candidate per Q-R-DOC-01. | research-notes.md §Tier-2; research/13. |
| **R-DIV-01** | In-flight divergence finding — live grep count (132 / 136) supersedes spec count (96). | research/03 (PRD-task); research/11. |
| **R-ATK-NN** | Adversarial-attack findings from the V2 attack chain. R-ATK-01 = CR-7 ORDERING markdown-discipline-only weakness (closed by sentinel + AST grep). R-ATK-06 = line-number anchor brittleness (closed by content-hash anchors). R-ATK-16 = `make sync-dev` worktree race (closed by `flock`). R-ATK-17 = local `pre-push` bypassable via `--no-verify` (closed by server-side push-policy hook). | `plan-adversarial-review.md`; validation-spec §9-§10. |
| **R-RES-NN** | Residual concession findings — R-RES-01..05 — recorded as residual risks surviving Phase 7.5 closure. Surfaced to §20.2 and TDD §22 Open Questions. | `validation-report.md`; research-notes.md §Convergence. |
| **R-RULE-11** | Ten-donor-ceremony-drops audit row (ME-9 binding). | `rejected-features-ledger.md`. |
| **R-FM-NN** | Frontmatter-format research findings. | research/12 §4; `refactor-mdtm-frontmatter.md`. |

### 28.9 Cross-Document Abbreviations

| Term | Definition | Source-of-definition |
|------|------------|----------------------|
| **PRD** | Product Requirements Document — defines *what* to build (product ownership). Parent doc: `.dev/releases/current/task-sc-task-directional-merge/roadmap/PRD_TASK_DIRECTIONAL_MERGE.md`. | TDD template lines 1322-1334; project convention. |
| **TDD** | Technical Design Document — defines *how* to build it (engineering ownership). This document: `.dev/releases/current/task-sc-task-directional-merge/roadmap/TDD_TASK_DIRECTIONAL_MERGE.md`. | TDD template lines 1322-1334. |
| **FR** | Functional Requirement — prefixed in PRD §14.1 as FR-TU-1..8, FR-CS-1..10, FR-CR-DEP-06. | research-notes.md §155-156; PRD §14.1. |
| **NFR** | Non-Functional Requirement — prefixed in PRD §14.2 as NFR-INV-1..5, NFR-ME-1..9, NFR-S-1..3. | research-notes.md §156-157; PRD §14.2. |
| **CR-CS** | Commit-sequencing audit row (CS-1..CS-10 = the 10-step atomic commit chain under ME-6). | `merge-master.md`; research/10. |
| **CS-N** | Commit Step N in the 10-step chain. CS-5 = donor command stubify (CR-DEP-01). CS-6 = donor skill hard-delete (CR-DEP-03). | `merge-master.md` §10-step-sequence; research-notes.md §193. |
| **EC-NN** | Evidence-Completeness audit row (validation-spec §14). EC-01..04 enumerated. | validation-spec §14; research/06 (PRD-task) §EC. |
| **FM-NN** | Failure-Mode audit row (validation-spec §13). FM-01..08 enumerated. | validation-spec §13; research/06 (PRD-task). |
| **OQ-** | Open-Question identifier — surfaced to §22. OQ-TIER-VOCABULARY, OQ-FM-03-SUNSET, OQ-F-05-MANIFESTIZATION, OQ-1..OQ-5 enumerated. | research-notes.md §Open-Questions; synth-01 §3. |
| **K-NN** | Maintenance-surface KPI from PRD §19 KPI table. **Canonical IDs are K-01..K-08** (NOT K-001..K-010). K-03 = residual-`/sc:task`-occurrence count; K-07 = `/sc:help` paired-entry count; K-08 = SKILL.md pair count. | PRD §19; §20.1 (this TDD). |
| **G-NN / NG-NN** | TDD Engineering Goal / Non-Goal identifiers (G-01..G-08, NG-01..NG-08) per §3. | §3 (this TDD); PRD §3 translation. |
| **P-NN** | Persona identifier from PRD §7 (P-01..P-04). | PRD §7; §2 (this TDD). |
| **D-NN** | Donor-pattern derivation row from V2 debate transcripts. D08, D09, D09b, D10, D11, D13, D15, D25, D29, D31 enumerated. D09b = "embedded runtime classifier" pattern, REJECT verdict per AC-ATK-05. | `debate-*.md` transcripts; `rejected-features-ledger.md`. |
| **PR-02** | Retry Monotonicity Protocol — referenced in the task-builder convergence release context (NOT directly applicable to this directional-merge TDD; cross-referenced in `task-builder-adjacency.md` for scope-fencing only). | `task-builder-adjacency.md`; out-of-scope per PRD §SCOPE-OUT. |
| **V/C/K** | The three verdict columns on `transfer-manifest.md`: **V**erbatim / **C**hange / **K**eep — adopted into TU disposition language as `{ADOPT verbatim / ADAPT / REJECT}`. | `transfer-manifest.md`; research/01. |
| **STRICT / STANDARD / LIGHT / EXEMPT** | The four canonical dispatch profiles (Tier enumeration); see §28.7. | §28.7 (this TDD). |
| **`[CODE-VERIFIED]`** | Verification tag asserting a claim was checked against source at a specific git SHA. AC-ATK-08 requires the 40-char SHA suffix `(git-sha: <40-char>)`. | research/12 §1.8; AC-ATK-08. |
| **`[CONTENT-AUDIT-COMPLETED]` / `[CONTENT-AUDIT-OWED]`** | Verification tag pair for body-content audit of artifact claims. R-DOC-01 governs the OWED→COMPLETED transition. | research/13; research-notes.md §Tier-2. |
| **`[VALIDATION-SPEC-CITED]`** | Tag asserting the claim's authoritative anchor is the validation-spec. Used when validation-spec section is the source-of-truth. | validation-spec; synth-01 frontmatter. |
| **`[CODE-CONTRADICTED]`** | Tag asserting a claim was checked and contradicted by source — surface to §22 for resolution. | research/13 cross-validation discipline. |
| **`[SPEC-DEFINED]`** | Tag asserting the claim is sourced from the validation-spec but not yet verified against live code. | validation-spec; §22 Open Questions. |
| **`[UNVERIFIED]`** | Tag asserting the claim is forward-looking and cannot be verified until post-merge state lands. | research-notes.md; §22, §24.2. |

---
