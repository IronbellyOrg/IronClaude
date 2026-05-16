# Synthesis 09 — TDD §27 References & Resources + §28 Glossary

**Status:** Complete
**Date:** 2026-05-14
**Source inputs:** 00-prd-extraction.md, 01-task-builder-skill-architecture.md, 02-sc-tasklist-source-mechanisms.md, web-01-adversarial-taxonomies.md, web-02-monotonicity-patterns.md

---

## §27 References & Resources

### §27.1 Related Documents

| Document | Type | Link |
|---|---|---|
| Product PRD | Product Requirements | `.dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md` |
| Release Spec | Spec | `.dev/releases/current/task-builder-merge/release-spec.md` |
| Conflict Register | Spec | `.dev/releases/current/task-builder-merge/conflict-register.md` |
| Merge Log | Spec | `.dev/releases/current/task-builder-merge/adversarial/merge-log.md` |
| Per-Proposal Verdicts | Spec | `.dev/releases/current/task-builder-merge/adversarial/per-proposal-verdicts.md` |
| Invariant Probe | Spec | `.dev/releases/current/task-builder-merge/adversarial/invariant-probe.md` |
| Refactor Plan | Spec | `.dev/releases/current/task-builder-merge/adversarial/refactor-plan.md` |
| Reflection Task | Spec | `.dev/releases/current/task-builder-merge/reflection/reflect-task.md` |
| Gate Report (Phase 5.2 PASS) | QA | `.dev/releases/current/task-builder-merge/reflection/gate-report.md` |
| Upstream FINAL-REPORT (v3.8) | Spec | `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md` |
| Research notes (this TDD) | Internal | `.dev/tasks/to-do/TASK-TDD-20260514-121250/research-notes.md` |
| TDD Template | Engineering | `src/superclaude/examples/tdd_template.md` |
| PRD Template | Product | `src/superclaude/examples/prd_template.md` |

### §27.2 Source Code Targets

| File | Lines | Purpose | FR(s) modifying |
|---|---|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` | 1709 | Generation orchestration; A.1–A.11 pipeline; 4-stage gate topology | FR-CONV.1, FR-CONV.2, FR-CONV.3, FR-CONV.4, FR-CONV.5, FR-CONV.6 |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 1390 | Intent-port source (NOT modified by this release) | None |
| `src/superclaude/agents/rf-qa.md` | 432 | 4 QA phases + partition protocol | FR-CONV.1, FR-CONV.5, FR-CONV.6 |
| `src/superclaude/agents/rf-qa-qualitative.md` | 794 | 7 QA phases incl. task-qualitative | FR-CONV.3, FR-CONV.4, FR-CONV.6 |
| `src/superclaude/agents/rf-analyst.md` | 349 | Partition + completeness/synthesis review | FR-CONV.6 |
| `src/superclaude/agents/rf-task-builder.md` | 493 | BUILD_REQUEST → MDTM transformation | FR-CONV.5 |
| `src/superclaude/agents/rf-team-lead.md` | 431 | Project-mode orchestrator; escalation at line 417 (NO DRIFT) | None (preserved by FR-CONV.6 Negative Criterion) |

> **Drift note:** PRD cites `rf-team-lead.md:417` for the "3 fix cycles per phase" rule. This was sed-verified against current source (`research/07-rf-team-lead-escalation.md` §2, §9): line 417 is verbatim `- **Fix Cycles**: ... (max 3 cycles per phase). If max cycles exhausted, HALT and ask user ...`. **Drift = 0 lines** — the PRD citation is exactly correct as of 2026-05-14. (The task brief's earlier hypothesis that the anchor had drifted to line 414 was disproven: line 414 is the unrelated `- **Direct pipeline invocation**:` bullet. SC-6 confirms 417 correct.)

### §27.3 External References (prior art for §6.4 + §21)

All URLs accessed **2026-05-14**.

**From web-01 — Adversarial-axis taxonomies + multi-stage QA gate patterns:**

| Source | Purpose | Citation (URL) |
|---|---|---|
| Travassos et al. 2001 — SRS Inspection Taxonomy (via systematic review "Defect Types and Software Inspection Techniques") | Prior art for classical adversarial-review axes (Omission, Inconsistency, Incorrect Fact, Ambiguity, Extraneous Information) — most direct prior art for the {omissions, contradictions} pair | https://thescipub.com/pdf/jcssp.2017.470.495.pdf |
| ACM Computing Surveys 2024 — "A Survey on Hallucination in LLMs" | Prior art for the "invented-content" axis (factuality vs faithfulness taxonomy; instruction/context/logical inconsistency) | https://dl.acm.org/doi/10.1145/3703155 |
| "Large Language Models Hallucination: A Comprehensive Survey" (arXiv 2510.06265) | Prior art for the "drift" axis — "faithfulness hallucination occurs when the generated output drifts from the original input or context" | https://arxiv.org/html/2510.06265v2 |
| LayerLens 2025 — "LLM Hallucination Detection in Production" | Prior art for "Citation Drift" and "Fabrication" — drift + invented-content axes in LLM-assisted spec generation | https://layerlens.ai/blog/llm-hallucination-detection-in-production |
| Fagan inspection (Wikipedia) — IBM 1976 | Foundational inspection-process literature; major-vs-minor defect categorization; evidence-based independent re-derivation | https://en.wikipedia.org/wiki/Fagan_inspection |
| "Refute-or-Promote" (arXiv 2604.19049, 2026) | Prior art for the 4-stage fail-closed gate topology + inherited-verdict pattern + empirical-gate-defeats-rubber-stamp evidence (OpenSSL/Bleichenbacher consensus-false-positive case study) | https://arxiv.org/html/2604.19049v1 |
| IEEE Std 830-1998 / IEEE Std 1233-1998 — SRS quality attributes | Prior art for spec-quality dimensions (Internal Consistency, Completeness as primary SRS qualities) | http://www.math.uaa.alaska.edu/~afkjm/cs401/IEEE830.pdf · https://ranger.uta.edu/~huber/cse4316/Docs/IEEEStd1233-1998.pdf |
| Wiegers' canonical SRS review checklist | Supporting prior art for omissions/contradictions axes ("Is any necessary information missing?", "Do any requirements conflict?") | https://www.cs.toronto.edu/~sme/CSC340F/2005/assignments/inspections/reqts_checklist.pdf |
| Cooper's Stage-Gate® model + SonarQube / Dynatrace / Perforce Quality Gates | Prior art for fail-closed multi-stage gate semantics ("any gap = FAIL") | https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/ · https://www.dynatrace.com/news/blog/what-are-quality-gates-how-to-use-quality-gates-with-dynatrace/ |

**From web-02 — Monotonicity guards + dedup-key strategies:**

| Source | Purpose | Citation (URL) |
|---|---|---|
| "Widening and narrowing operators for abstract interpretation" + "Efficiently intertwining widening and narrowing" | Prior art for the monotonicity guard — `\|F_{n+1}\| >= \|F_n\|` is structurally a widening termination operator forcing fixpoint convergence | https://www.sciencedirect.com/science/article/pii/S1477842410000254 · https://www.sciencedirect.com/science/article/pii/S0167642315004165 |
| "A minimalistic look at widening operators" (arXiv 0902.3722) | Supporting formalization of widening sequences for termination | https://arxiv.org/abs/0902.3722 |
| Sentry event fingerprinting | Prior art for dedup-key composition — tuple-of-stable-attributes with priority cascade (stack trace > exception > message) | https://sentry.zendesk.com/hc/en-us/articles/26184711712155 |
| Rollbar grouping algorithm + best practices | Prior art for dedup-key stability-over-precision (excludes line numbers "because they can change due to unrelated edits"); over-grouping vs under-grouping tradeoff | https://docs.rollbar.com/docs/grouping-algorithm · https://docs.rollbar.com/docs/error-grouping-best-practices |
| BugSnag error grouping | Prior art for custom-grouping-hash composition | https://docs.bugsnag.com/product/error-grouping/ |
| Self-Refine (Madaan et al. 2023, arXiv 2303.17651) | Prior art for the QA fix-cycle as iterative generate/critique/refine; v3.9 adds the missing principled stop condition | https://arxiv.org/abs/2303.17651 |
| Reflexion (Shinn et al.) + Reflexion wiki | Prior art for the "no-improvement / lack-of-improvement" stop condition | https://openreview.net/pdf?id=vAElhFcKW6 · https://aiwiki.ai/wiki/reflexion |
| Self-Refine prompting guide (sureprompts.com) | Prior art enumerating 4 termination conditions (fixed iterations, PASS verdict, no-improvement detector, external validator) | https://sureprompts.com/blog/self-refine-prompting-guide |
| "Self-Contrast: Better Reflection Through Inconsistent Solving Perspectives" (arXiv 2401.02009) | Prior art for local-minimum oscillation — empirically validates the v3.8 F2 oscillation pattern (21 retry files / 18 batches) | https://arxiv.org/abs/2401.02009 |
| Zeller & Hildebrandt — "Simplifying and Isolating Failure-Inducing Input" (ddmin, IEEE TSE 2002) | Prior art for regression-before-monotonicity precedence — failure-preservation invariant must hold before set reduction | https://homes.cs.washington.edu/~mernst/teaching/6.893/readings/zeller-tse.pdf |
| Gaffer "flip rate" + Chromium CI flaky-vs-fault study (arXiv 2302.10594) | Prior art for PASS@N → FAIL@N+1 regression detection and the flake-vs-regression disambiguation problem INV-012 sidesteps semantically | https://gaffer.sh/solutions/flaky-test-detection/ · https://arxiv.org/abs/2302.10594 |
| "Satisfiability Solvers are Static Analysers" + CDCL (Wikipedia) | Prior art for dedup-key persistence across fix-cycles ≈ learned-clause persistence across CDCL restarts | https://www.kroening.com/papers/sas2012.pdf · https://en.wikipedia.org/wiki/Conflict-driven_clause_learning |

> **Codebase remains source of truth:** No external source contradicts the verified code in `sc-tasklist-protocol/SKILL.md` or `rf-qa-qualitative.md`. External prior art is supportive context for §6.4 and §21 narrative — validating, not authoritative. Prefer paraphrase-with-citation over direct quotation, since surveyed sources do not use the v3.9 vocabulary (`\|F_n\|`, dedup-key, escalation ladder).

---

## §28 Glossary

| Term | Definition |
|---|---|
| **A-002** | Strictly-additive governance rule: every FR adds content; no existing item is renamed or removed. |
| **A.1–A.11** | The 11 stages of the task-builder skill's pipeline: Check-Existing → Parse-Triage → Scope-Discovery → Write-Notes → Sufficiency-Gate → Template-Triage → Build → Verify → Task-Integrity → Task-Qualitative → Present. |
| **anti-inflation rule** | `rf-qa-qualitative.md:766-775`: "NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION." Prior art: Refute-or-Promote (arXiv 2604.19049), Fagan inspection. |
| **B2 self-contained pattern** | MDTM checklist-item rule: each item is one paragraph containing context + action + output + verification (no nested bullets). |
| **BUILD_REQUEST** | The structured prompt the task-builder skill passes to rf-task-builder; defined at `SKILL.md:1409-1485`. |
| **CASE A/B/C/D** | G6 four-case conflict-rule classifications: A = both have mechanism, conflicting; B = sc-tasklist has, task-builder silent; C = sc-tasklist silent, task-builder has; D = both have, related but non-conflicting. |
| **CB-3** | Per-check classification rule: when bulk-import would conflate applicable and inapplicable mechanisms, classify per-check rather than bulk-porting. |
| **dedup-key** | INV-012 composition identity: the tuple `(assigned_files_range, escalation_ladder_exhaust_point)` for synthetic-dnsp findings. Prior art: Sentry/Rollbar/BugSnag fingerprinting. |
| **DNSP** | "Does Not Serialize Parallel cohort" — FR-CONV.6's synthetic finding mechanism, emitted on per-partition escalation-ladder exhaust. |
| **drift-axis-inactive** | Annotation rule in FR-CONV.4: when no MDTM item restates `BUILD_REQUEST.GOAL`, the drift axis emits this annotation instead of a finding. |
| **`F_n`** | The set of FAIL-verdict items at fix-cycle N, with dedup-key as identity (FR-CONV.5). |
| **FR-CONV.1..6** | The 6 functional requirements of the Task-Builder Convergence v3.9 release (Structural Gate Additions, Execution Context header, Inherited Structural Verdict, Five Adversarial Axes, Retry Monotonicity, DNSP synthetic-finding). |
| **G6 four-case rule** | Authoritative conflict-resolution rule for sc-tasklist ↔ task-builder mechanism conflicts (release-spec.md Appendix D). |
| **INV-002, INV-010, INV-012, INV-015, INV-019, INV-021** | MEDIUM-severity invariant-probe findings from adversarial-debate Phase 4. |
| **K-001..K-010** | The 10 risk entries from PRD §20. |
| **MDTM** | Markdown Driven Task Management — the task-file format generated by rf-task-builder. |
| **NFR-CONV.1..10** | Non-functional requirements; NFR-CONV.6..10 are the invariant-preservation NFRs. |
| **OPEN-PR05, OPEN-INV-006, OPEN-INV-017, OPEN-INV-018, OPEN-X-002, OPEN-TOKEN** | The 6 Open Questions from PRD §13. |
| **PR-01..PR-07** | The 7 proposals from the adversarial debate; PR-01/PR-02/PR-06/PR-07 are CASE-D, PR-03/PR-04 are CASE-B, PR-05 is DEFERRED. |
| **rf-qa** | The structural QA agent: 4 phases (research-gate, synthesis-gate, report-validation, task-integrity). |
| **rf-qa-qualitative** | The content QA agent: 7 phases including task-qualitative (15-item checklist + Self-Audit). |
| **rf-analyst** | The completeness-verification + synthesis-review agent. |
| **rf-task-builder** | The subagent that emits MDTM task files from a BUILD_REQUEST. |
| **rf-team-lead** | The project-mode orchestrator; its line-417 "3 fix cycles per phase" rule is preserved by FR-CONV.6 (NO DRIFT). |
| **Self-Audit** | INV-019 mandate: rf-qa-qualitative output must list ≥1 semantic check performed beyond inherited PASS verdicts. |
| **TB-Add-1..8** | The 8 structural checks added to rf-qa's task-integrity gate by FR-CONV.1 (placeholder scan, item-count bounds, clarification adjacency, circular-dependency DAG check, granularity check, confidence/verification format, Execution-Context cross-validation, per-item file:line citation). |
| **synthetic-dnsp** | The 5-field HIGH-severity finding emitted on per-partition escalation-ladder exhaust (FR-CONV.6). |
| **task-qualitative** | rf-qa-qualitative's phase at lines 508-583 — the FR-CONV.4 5-axis adversarial overlay landing site. |
| **tdd-qualitative** | rf-qa-qualitative's phase at lines 244-308 — the Phase-6 gate that validates THIS TDD. |
| **X-001, X-002, X-003, X-004** | Rejected design alternatives documented in PRD §2.2 / Alternatives Considered. |
| **`[HALT-MONOTONICITY]`** | FR-CONV.5 halt signal raised when `\|F_{n+1}\| >= \|F_n\|` (failure-set fails to strictly shrink). Prior art: abstract-interpretation widening operators. |
| **`[HALT-REGRESSION]`** | FR-CONV.5 halt signal raised when an item that PASSed at cycle N FAILs at cycle N+1. Regression detection runs before the monotonicity check. Prior art: ddmin failure-preservation, CI/CD pass-to-fail transition semantics. |

---

**Status:** Complete
