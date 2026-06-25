---
id: "FR-RSR-TDD"
title: "sc:reflect UC-2 Runtime-Surface Reachability Escalation - Technical Design Document"
description: "Technical architecture, data models, and implementation details for the additive UC-2 runtime-surface reachability escalation in the sc-reflect-protocol skill (tagger + sweep + degrade-oracle + rootwalk + forbid-STOP pre-filter + §10.9 finding-modifier + contract 1.6.0)"
version: "1.0"
status: "🟡 Draft"
type: "📐 Technical Design Document"
priority: "🔥 Highest"
created_date: "2026-06-19"
updated_date: "2026-06-19"
assigned_to: "sc-reflect maintainers"
autogen: false
coordinator: "tech-lead"
parent_doc: ".dev/reflect-hardening/issue-1-uc2-reachability/spec.md"
feature_id: "FR-RSR"
spec_type: "new_feature"
complexity_score: "0.85"
complexity_class: "HIGH"
target_release: "4.4.0"
authors: ["user", "claude"]
quality_scores:
  clarity: ""
  completeness: ""
  testability: ""
  consistency: ""
  overall: ""
depends_on:
- "src/superclaude/skills/sc-reflect-protocol/SKILL.md (§5.3, §6.1, §9.1, §9.3, §9.4, §10, §17.7)"
- "src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md"
- "src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md"
- ".dev/eval-workspaces/sc-reflect/grader.py"
related_docs:
- ".dev/reflect-hardening/issue-1-uc2-reachability/spec.md"
- "src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md"
tags:
- technical-design-document
- skill-protocol
- architecture
- specifications
- reflect
- reachability
template_schema_doc: "src/superclaude/examples/tdd_template.md"
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
approvers:
  tech_lead: ""
  engineering_manager: ""
  architect: ""
  security: ""
---

# sc:reflect UC-2 Runtime-Surface Reachability Escalation — Technical Design Document (TDD)

## Document Information

| Field | Value |
|-------|-------|
| **Component Name** | sc:reflect UC-2 Runtime-Surface Reachability Escalation (FR-RSR) |
| **Component Type** | Skill protocol (inference-mediated Markdown behavioral spec + supporting `refs/` + eval suite) |
| **Tech Lead** | sc-reflect maintainers |
| **Engineering Team** | SuperClaude framework |
| **Maintained By** | sc-reflect-protocol owners |
| **Target Release** | 4.4.0 |
| **Last Verified** | 2026-06-19 against `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (~1850 lines) and the spec at `.dev/reflect-hardening/issue-1-uc2-reachability/spec.md` |
| **Status** | Draft |

### Approvers

| Role | Name | Status | Date |
|------|------|--------|------|
| Tech Lead | | ⬜ Pending | |
| Engineering Manager | | ⬜ Pending | |
| Architect | | ⬜ Pending | |
| Security | | ⬜ Pending | |

---

## Completeness Status

**Completeness Checklist:**

- [x] Section 1: Executive Summary — Complete
- [x] Section 2: Problem Statement & Context — Complete
- [x] Section 3: Goals & Non-Goals — Complete
- [x] Section 4: Success Metrics — Complete
- [x] Section 5: Technical Requirements — Complete
- [x] Section 6: Architecture — Complete
- [x] Section 7: Data Models — Complete
- [x] Section 8: API Specifications — Complete (skill-contract surface; no HTTP API)
- [x] Section 9: State Management — N/A (stateless review pass; documented)
- [x] Section 10: Component Inventory — N/A (no frontend; documented)
- [x] Section 11: User Flows & Interactions — Complete
- [x] Section 12: Error Handling & Edge Cases — Complete
- [x] Section 13: Security Considerations — Complete
- [x] Section 14: Observability & Monitoring — Complete
- [x] Section 15: Testing Strategy — Complete
- [x] Section 16: Accessibility Requirements — N/A (documented)
- [x] Section 17: Performance Budgets — Complete
- [x] Section 18: Dependencies — Complete
- [x] Section 19: Migration & Rollout Plan — Complete
- [x] Section 20: Risks & Mitigations — Complete
- [x] Section 21: Alternatives Considered — Complete
- [x] Section 22: Open Questions — Complete
- [x] Section 23: Timeline & Milestones — Complete
- [x] Section 24: Release Criteria — Complete
- [x] Section 25: Operational Readiness — Complete
- [x] Section 26: Cost & Resource Estimation — Complete (token cost)
- [x] Section 27: References & Resources — Complete
- [x] Section 28: Glossary — Complete

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | `sc-reflect-protocol/SKILL.md` §5.3/§6.1/§9.1/§9.3/§9.4/§10/§17.7; `refs/reviewer-spec.md`; `refs/deviation-taxonomy.md`; `.dev/eval-workspaces/sc-reflect/grader.py` |
| **Upstream** | Feeds from: release spec `issue-1-uc2-reachability/spec.md` (FR-RSR.1–10) |
| **Downstream** | Feeds to: `sc:roadmap` / `sc:tasklist` (themes T1–T5, §10 of spec), implementation, eval suite |
| **Change Impact** | Notify: sprint consumer (`executor.py` TurnLedger), `sc-troubleshoot-protocol` Wave 6, `sc-task-protocol` end-of-task hook |
| **Review Cadence** | As-needed (per skill release) |

---

## 1. Executive Summary

`sc:reflect` UC-2 (post-execution audit) shipped a **PASS on an unreachable feature**: every leaf
mechanism existed, every unit test was green, yet nothing was wired into the production
entrypoint. The requirement "user can reach `/ai` and invoke Spawn" (FR-S9-04) was graded PASS
at Tier 1 citing only the gate source plus its unit tests, while the implementing symbol's only
referrers lived in test files and doc-comments. This is a **structural blind spot** spanning four
mutually-reinforcing planes of the protocol (STOP rubric, evidence chain, coverage algorithm,
deviation taxonomy), not a one-off misjudgement.

This TDD specifies an **additive, LLM-free, fail-loud** reachability-escalation capability for UC-2
that gathers the reachability signal the protocol already fetches-and-discards, classifies it
along the existing 4-class taxonomy by evidence (no 5th class), and gates it through the proven
table-wide forbid-STOP pre-filter shape. The design is anchored on two non-negotiable invariants
the implementer must not relax:

1. **The tagger is symbol-anchored, NOT requirement-anchored.** It keys off the diff hunk's
   resolved symbol kind (Wave-1A), never a requirement id that may not yet be mapped (Wave-1B).
   Requirement-anchoring would resurrect the original clean-pass bug via a wave-ordering quirk.
2. **The degrade oracle defaults all dynamic / registry / decorator / reflection / packaging-entrypoint
   wiring to DEGRADE → §10.6 Grounding Gap, NEVER to a blocking Regression.** Reachability is
   semi-decidable; the asymmetric cost of a false `UNREACHED → Regression` (it triggers a TurnLedger
   rollback in the sprint consumer) makes loud-degrade the only sound default.

Scope is **one SKILL.md** (six surgical edits), **one new `refs/runtime-surface.md`** (the source of
truth for all code-free behavior), **two existing refs** touched, and **eval coverage** (one active
headline case + four MAIN companions). The contract bumps `1.5.0 → 1.6.0` (additive minor). No
existing field is renamed, removed, retyped, or re-semanticized. Source of truth is
`src/superclaude/` only; UV for any Python (grader) work.

---

## 2. Problem Statement & Context

### 2.1 Background

`sc-reflect-protocol` is a tiered, evidence-grounded reflection skill. UC-2 (`--mode post`) audits
completed agent work for 100% adherence and classifies every divergence under a 4-class deviation
taxonomy (§10: Authorized / Necessary / Drift / Regression). Tier 1 is a fast single-agent grounded
pass; the §5.3 decision rubric (SKILL.md:386–402) decides whether to STOP at Tier 1 or escalate to
the Tier-2 heterogeneous reviewer ensemble.

### 2.2 Problem Statement

The protocol cannot detect a **complete-but-unintegrated feature**. Four load-bearing facts
(adversarially confirmed at ~88% confidence in the spec) each independently fail, and fail in a
mutually-reinforcing way:

1. **The STOP rubric has no row for it.** §5.3 row 1 (SKILL.md:390) STOPs on
   `C ≥ 0.90 ∧ S_scope ≤ 5 ∧ S_domains == 1 ∧ S_dev_density ≤ 0.05 ∧ coverage_pct ≥ floor` — exactly
   the signature of a small, clean, additive, well-tested but unwired leaf. The only structural
   escalation rows are 3 (Regression, SKILL.md:392) and 3a (Reuse-Miss, SKILL.md:393); there is **no row**
   for "claimed user surface with no production caller."
2. **The reachability signal is gathered, then discarded.** §6.1 Wave-1A step 4
   (`find_referencing_symbols include_info:true`, SKILL.md:463) runs already, but only "for downstream
   impact + signatures." It never partitions referrers into production-vs-test/comment.
3. **Coverage maps mapping, not reachability.** `refs/coverage-mapping.md` proves requirement → task/diff
   mapping. An additive diff contradicts no mapping → clean STOP. Reachability is not in its value space.
4. **The taxonomy is the sink, and it has no class.** §10.3 Drift (SKILL.md:937) needs an *unmapped hunk*;
   §10.4 Regression (SKILL.md:952) needs a *contradicted criterion*. Additive-only unwired code triggers
   neither, so even a gathered signal has nowhere to be filed.

### 2.3 Business Context (engineering risk framing)

**Framing correction (load-bearing for the whole design).** Production reachability is **semi-decidable**:
static analysis cannot *prove* reachability under dynamic dispatch, plugin/registry wiring, reflection,
and `console_scripts`-style entrypoints. This feature specifies a **zero-production-referrer ESCALATION**,
not a reachability *proof*. The single biggest implementation risk is a fix bolted onto
`find_referencing_symbols` that **silently no-ops** on `backend: none` and on dynamic/registry entrypoints —
**including this very repository's own** `[project.scripts]` (`pyproject.toml:67–69`:
`superclaude = "superclaude.cli.main:main"`, `ic = "superclaude.cli.ic:main"`) — which have **zero static
callers**. A naive referrer-only sweep would false-flag idiomatic console_scripts wiring as UNREACHED.
The escalation MUST fail loud to a Grounding Gap on every uncertainty, and MUST never silently downgrade
a real finding nor silently PASS an unwired one.

---

## 3. Goals & Non-Goals

### 3.1 Goals

- **G1** — Gather the discarded reachability signal in UC-2 Wave-1A via a deterministic (LLM-free) tagger
  and a production-caller sweep that extends the existing `find_referencing_symbols` call.
- **G2** — Classify each UNREACHED finding onto the existing 4-class taxonomy by evidence (Reuse-Miss-style
  finding-modifier), introducing **no 5th deviation class** and **no new counter** (consistent with
  §17.7 Kill List item 6, SKILL.md:1799).
- **G3** — Gate via a **table-wide forbid-STOP pre-filter** (`surface_unreached`) that cannot be shadowed
  by §5.3's first-match-wins row 1.
- **G4** — Fail loud on every reachability uncertainty: dynamic/registry/decorator/reflection/packaging
  wiring, unknown language, comment-ambiguity, and backend loss all DEGRADE → §10.6 Grounding Gap, never
  a blocking Regression and never a silent PASS.
- **G5** — Surface the signal additively: six §9.1 contract fields + a `runtime-surface-ledger.yaml`
  artifact; `contract_version` 1.5.0 → 1.6.0; reviewer-brief routing of the ledger as a grounding-hunk ref.
- **G6** — Make the fix **falsifiable** with real fixtures: one active headline eval (FAIL pre-change /
  PASS post-change) + four MAIN companions.

### 3.2 Non-Goals

- **NG1** — UC-1 (pre-execution) reachability. The reachable surface lives in UC-2 diff hunks, not a
  UC-1 tasklist. UC-1 emits only the additive inert defaults.
- **NG2** — Whole-program call-graph construction or any reachability *proof* (semi-decidable; explicitly
  rejected — see §21 Alternative 1).
- **NG3** — Cross-language entrypoint resolution beyond the deterministic degrade-oracle table. Unknown
  languages DEGRADE; they are not analyzed.
- **NG4** — Any change to UC-1 coverage semantics, the §10 4-class taxonomy **count**, or the
  exit-code-sourced `verification_regressions_detected` field.
- **NG5** — Auto-remediation of UNREACHED findings. Reflect AUTHORS, never runs `/task` — the §"Will Not"
  invariant (SKILL.md:1700) is preserved.

### 3.3 Future Considerations

- OQ-RSR.4 — whether `runtime_surface_*` should feed `S_dev_density` as a parallel up-weight (deferred;
  v1 routes via the forbid-STOP pre-filter only).
- OQ-RSR.5 — whether a TurnLedger rollback is the right sprint-consumer action for an UNREACHED-contradiction
  Regression (v1 accepts the §10.9 by-evidence routing; revisit on iteration-2 false-fire telemetry).
- Extending the language→(test-marker, comment-syntax) and degrade-oracle tables beyond py/rust/ts/js/go
  (OQ-RSR.2): new rows are additive; unknown languages DEGRADE until added.

---

## 4. Success Metrics

### 4.1 Technical Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Headline eval `uc2-unwired-surface-passes` | FAILs against pre-change skill, PASSes against post-change skill | `grader.py` `regex_absent` + `yaml_field` |
| False `UNREACHED → Regression` on idiomatic wiring | 0 across the companion suite | NFR-RSR.3 / `uc2-surface-dynamic-dispatch` |
| Added cost on non-surface diffs | 0 extra MCP/tool calls (`runtime_surface_sweep_ran == false`) | NFR-RSR.1 |
| Determinism | byte-identical `runtime-surface-ledger.yaml` across two runs of the same fixture | NFR-RSR.2 |
| Contract compatibility | all pre-1.6.0 fields keep name/type/semantics; `make verify-sync` clean | NFR-RSR.4/5 |
| Count invariant | `len(unreached_surfaces) == runtime_surface_unreached` for every run | FR-RSR.2 / eval |

### 4.2 Business Metrics

Not directly instrumented (internal developer-tooling skill). The proxy business metric is **escaped
unreachable-feature defects** caught at reflection time instead of in production — the motivating
FR-S9-04 incident is the canonical example the headline eval re-enacts (§2.3 worked scenario in spec).

---

## 5. Technical Requirements

### 5.1 Functional Requirements

The ten functional requirements are specified verbatim in the spec (`spec.md` §3). This TDD restates
their engineering contract and binds each to its modification site.

| FR | Title | Primary site | Design section |
|----|-------|--------------|----------------|
| FR-RSR.1 | Deterministic runtime-surface tagger (symbol-anchored) | SKILL.md §6.1 new step **4b'** | §6.4 D1, §7.1 |
| FR-RSR.2 | Production-caller reachability sweep (extends step 4) | SKILL.md §6.1 new step **4b** | §6.4 D3, §7.1 |
| FR-RSR.3 | Degrade oracle (concrete deterministic table) | `refs/runtime-surface.md` | §6.4 D2, §7.1 |
| FR-RSR.4 | Entrypoint-rootwalk (dead-caller false-negative guard) | `refs/runtime-surface.md` | §6.4 D4, §11.1 |
| FR-RSR.5 | Table-wide forbid-STOP pre-filter `surface_unreached` | SKILL.md §5.3 + precedence ¶ | §6.4 D5, §11.1 |
| FR-RSR.6 | §10.9 UNREACHED finding-modifier (by evidence, no 5th class) | SKILL.md new §10.9 | §6.4 D6, §11.1 |
| FR-RSR.7 | Six additive contract fields + ledger; `contract_version` 1.6.0 | SKILL.md §9.1/§9.3 | §7, §8 |
| FR-RSR.8 | Fail-open on backend/tool unavailability | SKILL.md §6.5/§0.5d consumers | §12.3 |
| FR-RSR.9 | Reviewer-brief ledger routing (preserve "exactly three sections") | `refs/reviewer-spec.md` | §8.4, §11.1 |
| FR-RSR.10 | Eval coverage (fail-before / pass-after, real fixtures) | `.dev/eval-workspaces/sc-reflect/` | §15 |

**FR-RSR.1 — symbol-anchored tagger (the load-bearing invariant).** The tagger keys off the **diff
hunk's symbol** resolved in Wave 1A (`get_symbols_overview` / `find_symbol`, SKILL.md:459,461), NOT off a
requirement id. The requirement id is an *attribute* attached when the UC-2 inline Wave-1B
tasklist-vs-diff map is available; when a surface hunk has no mapped requirement, the tagger still tags
the **symbol** with `requirement_id: null` and the sweep runs regardless. Reachability must not depend on
a requirement mapping built later in the wave order, or an ordering quirk would emit `[]` by sequencing
and resurrect the original clean-pass bug. A `requirement_id: null` UNREACHED finding maps to §10.3 Drift
(unmapped) by FR-RSR.6, never silently dropped. Kind-resolution failure (parse failure / `backend: none`)
routes the hunk to DEGRADE, never silent-skip.

**FR-RSR.3 — degrade oracle (the asymmetric-cost default).** The oracle maps wiring idioms that static
referrer analysis cannot resolve to **DEGRADE → §10.6 Grounding Gap, NEVER a blocking Regression**. It MUST
cover, at minimum, four categories with deterministic match predicates: (a) decorator routes
(`@app.route`, `@click.*` / Typer command decorators); (b) packaging entrypoints
(`[project.scripts]` / `[project.entry-points.*]` and equivalents); (c) registry / DI / string-dispatch
wiring; (d) reflection / dynamic import. The oracle **default** for any reachability uncertainty is DEGRADE.

### 5.2 Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-RSR.1 | Zero added cost on non-surface diffs | 0 extra MCP/tool calls beyond the existing Wave-1A chain when `runtime_surface_requirements == []` | `runtime_surface_sweep_ran == false` ⇒ no `runtime-surface:*` audit rows; positive-control companion |
| NFR-RSR.2 | Determinism of tagging + matching | Identical `(diff + allowlist)` → identical `runtime_surface_requirements` + ledger statuses | Re-run fixture twice; assert byte-identical ledger (LLM-free path) |
| NFR-RSR.3 | No false `UNREACHED → Regression` on idiomatic wiring | 0 Regression increments from `[project.scripts]`/decorator/registry wiring | `uc2-surface-dynamic-dispatch` asserts `runtime_surface_degraded: true` AND `deviation_count_by_class.regression` unchanged |
| NFR-RSR.4 | Additive contract compatibility | All pre-1.6.0 fields keep name/type/semantics; read-and-ignore forward-compat | `make verify-sync` + unchanged-fields grader assertion |
| NFR-RSR.5 | Source-of-truth + sync discipline | Edit only `src/superclaude/`; `make sync-dev` → `make verify-sync` clean; UV-only | CI `make verify-sync`; no `.claude/` mirror staged |
| NFR-RSR.6 | Fail-open availability | Backend/tool loss never STOPs and never silent-PASSes a tagged surface | `uc2-surface-degraded-backend` asserts Grounding Gap + skill-continues + no clean PASS |

---

## 6. Architecture

### 6.1 High-Level Architecture

The feature is a **read-only enrichment of the UC-2 Wave-1A grounding chain** plus three downstream
consumers of the signal it produces. It introduces no new agent, no new wave, no new CLI flag, and no
mutation outside `<output>/`. The capability is gathered along the **gather → gate → classify → surface**
spine, mirroring the four planes the blind spot spans:

```
UC-2 post-execution audit
        │
Wave 1A (§6.1) ── existing grounding chain (steps 1..7', SKILL.md:457-478) ───────────────┐
        │                                                                                  │
        ├── [NEW step 4b'] TAGGER  (FR-RSR.1): per diff hunk, symbol kind + surface         │
        │        allowlist → runtime_surface_requirements:[ids]  (LLM-free; emits []        │
        │        and runtime_surface_sweep_ran:false on non-surface diffs → zero cost)      │
        │                                                                                   │
        └── step 4 find_referencing_symbols (already runs, SKILL.md:463) ───────────────────┤
                 │                                                                           │
                 ├── [NEW step 4b] SWEEP (FR-RSR.2): partition referrers prod-vs-(test|       │
                 │     comment) via lang→(marker,syntax) table; reduce edges→symbol verdict   │
                 │       ├── ≥1 prod referrer ................................ REACHED         │
                 │       ├── 0 prod referrers ∧ rootwalk hit (FR-RSR.4) ...... REACHED         │
                 │       ├── 0 prod referrers ∧ rootwalk complete, no hit .... UNREACHED       │
                 │       └── oracle row | unknown-lang | comment-ambiguous |                   │
                 │             partial rootwalk | backend loss (FR-RSR.3/4/8) .. DEGRADE       │
                 │                                                                             │
                 └── writes <output>/artifacts/runtime-surface-ledger.yaml (per-edge) ────────┘
        │
        ▼
Wave 2 (§5.3 rubric): [NEW] table-wide forbid-STOP pre-filter `surface_unreached` (FR-RSR.5)
        │   runtime_surface_unreached ≥ 1 → NO STOP row may fire → route Tier 2
        │   (pins --tier 1 / --depth quick override → loud WARN + status:partial)
        ▼
Wave 5 synthesis: [NEW] §10.9 finding-modifier maps each UNREACHED by evidence (FR-RSR.6)
        │   contradiction → Regression (deviation_count_by_class.regression ONLY)
        │   unmapped     → Drift
        │   degraded/ambiguous → §10.6 Grounding Gap (needs_human_decision, status:partial)
        ▼
Contract: +6 runtime_surface_* fields, contract_version 1.6.0 (FR-RSR.7)
Reviewer brief (T2 only): ledger routed as a `## Grounding hunks` entry (FR-RSR.9 — 3-section invariant intact)
```

### 6.2 Component Diagram

```
                 §1B coverage hunk→requirement map  (optional attribute only — never gates the sweep)
                              │
                FR-RSR.1 TAGGER (Wave-1A, UC-2, symbol-anchored)
                              │ runtime_surface_requirements:[ids]  (requirement_id may be null)
                              ▼
   §6.1 step 4 find_referencing_symbols ──► FR-RSR.2 SWEEP (edge producer)
                              │                    │
                              │            ┌───────┴────────┐
                              │     FR-RSR.3 ORACLE   FR-RSR.4 ROOTWALK
                              │       (degrade table)  (entrypoint roots; full-enum gate)
                              │            └───────┬────────┘
                              ▼                    ▼
                     runtime-surface-ledger.yaml (status per edge → reduced per-symbol verdict)
                              │
            ┌─────────────────┼──────────────────────────┐
            ▼                 ▼                           ▼
  FR-RSR.5 §5.3 pre-filter  FR-RSR.6 §10.9 modifier   FR-RSR.7 contract 1.6.0
  (forbid-STOP → T2)        (Regression|Drift|Gap)    (+6 fields, +ledger path)
                              │
                              ▼ (T2 only)
                     FR-RSR.9 reviewer-brief grounding-hunk ref (qa persona)
                              │
                              ▼
                  FR-RSR.8 fail-open on backend/tool loss (§6.5, §0.5d)
```

### 6.3 System Boundaries

- **In-skill, read-only:** the tagger, sweep, oracle, and rootwalk all execute inside Wave 1A, which is
  one of the read-only review waves (Waves 0–6; SKILL.md:161,176). The sweep writes only to
  `<output>/artifacts/`. No repository state is mutated. Wave 7 (the sole mutation wave) is untouched.
- **Determinism boundary:** the tagger and the referrer-partition matching are 100% LLM-free. The only
  model-mediated surface remains the existing Wave-5 synthesis (which the §10.9 modifier feeds, not
  replaces).
- **Consumers:** the §5.3 rubric (gate), the §10.9 modifier (classify), the §9.1 contract + §9.3
  consumer map + `refs/reviewer-spec.md` (surface). The downstream sprint consumer
  (`executor.py` TurnLedger, SKILL.md:858) reads `deviation_count_by_class.regression` — unchanged in
  name, type, and meaning; only a new *evidence source* can now move its value.

### 6.4 Key Design Decisions

| # | Decision | Choice | Rationale (grounded) |
|---|----------|--------|----------------------|
| **D1** | Where the tagger runs + what it keys off | §6.1 **Wave-1A (UC-2)**, keyed off **diff-hunk symbol kind** (symbol-anchored) | Coverage Pass-1 is UC-1 / Wave-1B; the reachable surface lives in **UC-2 diff hunks** (SKILL.md:455). Requirement-anchoring would depend on a Wave-1B mapping built later → ordering quirk emits `[]` → original bug returns. Symbol-anchoring resolves the spec's Wave-1A/1B sequencing hazard. |
| **D2** | Reachability vs escalation | **Zero-production-referrer ESCALATION**, not a proof | Static reachability is **semi-decidable**; a "proof" would over-claim (silent PASS on dynamic wiring) or over-block (false Regression on idiomatic registry wiring). |
| **D3** | Sweep mechanism | **Extend** the existing `find_referencing_symbols` call (SKILL.md:463) | The referrer set is *already fetched* and discarded; partitioning it is a filter, not a new tool — avoids agent-coordination cost and inherits §6.5 fail-open. |
| **D4** | Dead-production-caller false-negative | v1 **REQUIRES** an entrypoint-rootwalk before any UNREACHED | A symbol called only by *other unreached production code* reads REACHED on a referrer-only check; the rootwalk anchors REACHED to an actual entrypoint root. Partial enumeration = incompleteness → DEGRADE. |
| **D5** | Dynamic/registry/decorator wiring | **DEFAULT degrade → §10.6 Grounding Gap**, never blocking Regression | A false `UNREACHED → Regression` triggers unconditional T2+T3 + a TurnLedger rollback in the sprint consumer — net-negative if it false-fires on `@app.route` / `[project.scripts]` / registry wiring. Degrade is the asymmetric-cost-correct default. |
| **D6** | Escalation shape | **Table-wide forbid-STOP pre-filter**, not a plain §5.3 row | §5.3 is first-match-wins (SKILL.md:386); a plain row is shadowed by row 1's earlier STOP. A pre-filter (the proven `coverage_degraded` shape, SKILL.md:402) forbids ALL STOP rows when set. |
| **D7** | Taxonomy sink | **§10.8 Reuse-Miss-style finding modifier**, NO 5th class | §17.7 Kill List item 6 (SKILL.md:1799) rejected a 5th class for structural cleanliness; §10.8 (SKILL.md:1014) is the established "maps onto the 4 by evidence" pattern. |
| **D8** | Regression counter hygiene | Increment **ONLY** `deviation_count_by_class.regression` | `verification_regressions_detected` is **exit-code-sourced** (§10.4 / step 5.5, SKILL.md:708,959). An UNREACHED contradiction is evidence-sourced; conflating them corrupts the verified-regression count. |
| **D9** | Contract bump | **1.5.0 → 1.6.0** (additive minor) | All six new fields are additive; existing fields keep semantics; §9.4 minor rules (SKILL.md:877) + read-and-ignore forward-compat apply. |
| **D10** | Eval placement | One falsifier promoted to `active` + four companions in **MAIN** `evals/` | Skeleton falsifier cases pass *vacuously* (structural-contract-only, README dual-state lifecycle). Positive/negative companions must FAIL pre-change / PASS post-change against real fixtures — that is MAIN-case (`regex_absent`/`yaml_field`) behavior. |
| **D11** | Degrade-only runs do NOT force T2 | Pre-filter trigger is `runtime_surface_unreached ≥ 1`, not `runtime_surface_degraded` | A degrade-only run already files a §10.6 Grounding Gap that independently forces `status: partial` + `needs_human_decision`; it must not pay the asymmetric T2 cost for a "could not decide" finding. |
| **D12** | Downstream rollback coupling (Newman) | **ACCEPT** that an UNREACHED-contradiction Regression triggers the sprint consumer's TurnLedger rollback (§9.3, SKILL.md:858) | Routing UNREACHED-contradiction → `deviation_count_by_class.regression` is the D7/§10.9 by-evidence design, and the sprint consumer already rolls back on `regression`. An unwired user-facing surface is exactly the "should not have shipped" state rollback exists for. The coupling is intentional and stated; OQ-RSR.5 (§22) tracks revisiting it if iteration-2 false-fire telemetry appears. Alternatives (a separate non-rollback "unreached" signal; suppressing rollback) were rejected as they fork the established by-evidence routing. |

### 6.5 Multi-Tenancy Architecture

N/A — single-user developer-tooling skill; no tenancy model.

---

## 7. Data Models

### 7.1 Data Entities

**(a) Additive §9.1 stable-contract fields** (UC-2; inert defaults on UC-1 / non-surface). Appended to
the §9.1 block (SKILL.md:689–708 region, "UC-2 specific"); `contract_version` bumps to `"1.6.0"`.

```python
# contract_version: "1.6.0"   # 1.5.0 + ADDITIVE ONLY (no rename/remove/retype/semantic change)

runtime_surface_requirements: list[str]   # FR-RSR.1: requirement ids tagged user-reachable surface; [] when none
runtime_surface_sweep_ran: bool           # FR-RSR.2: true only when ≥1 tagged surface triggered the sweep (UC-2)
runtime_surface_ledger_path: str | None   # FR-RSR.2: abs path to <output>/artifacts/runtime-surface-ledger.yaml; null when sweep did not run
runtime_surface_unreached: int            # FR-RSR.2/6: count of SYMBOLS (reduced verdict) that are UNREACHED — drives the §5.3 pre-filter
runtime_surface_degraded: bool            # FR-RSR.3/8: true when ≥1 SYMBOL reduced to DEGRADE (oracle / unknown-lang / backend) → Grounding Gap
unreached_surfaces: list[UnreachedSurface]  # FR-RSR.6: per-UNREACHED detail; [] when none

class UnreachedSurface(TypedDict):
    requirement_id: str | None            # reachability requirement (e.g. "FR-S9-04"); null when surface hunk had no mapped requirement
    symbol: str                           # symbol name-path with zero surviving production referrers
    mapped_class: Literal["regression", "drift", "grounding_gap"]   # §10.9 by-evidence mapping
    evidence_ref: str                     # resolves to the ledger row for regression/drift; to grounding-gaps.yaml for grounding_gap
                                          # (same value space, repointed by mapped_class) — re-Read by Wave-5 evidence-validator.
```

**(b) `runtime-surface-ledger.yaml`** — one row per evaluated edge (FR-RSR.2):

```python
class RuntimeSurfaceLedgerRow(TypedDict):
    requirement_id: str | None            # null permitted (symbol-anchored, FR-RSR.1)
    symbol: str                           # tagged surface symbol name-path
    edge: str                             # "<symbol> -> <referrer-or-entrypoint-root>"
    status: Literal["REACHED", "UNREACHED", "DEGRADE"]
    production_referrers: list[str]       # surviving non-test/non-comment referrer file:line refs ([] for UNREACHED)
    evidence_ref: str                     # file:line / artifact ref backing the verdict (re-Read by evidence-validator)
```

**Count semantics (the edge-vs-symbol invariant).** The ledger is **per-edge**, but every *count* the
contract and gate consume is **per-symbol**, computed by reducing a symbol's edges to a single verdict
under the precedence:

```
DEGRADE-on-any-incompleteness  >  UNREACHED  >  REACHED
```

A symbol is REACHED if **any** edge is REACHED; UNREACHED only if **all** edges are non-REACHED and none
degraded; DEGRADE if **any** edge degraded. Therefore `runtime_surface_unreached` counts **symbols** (never
edges), and `len(unreached_surfaces) == runtime_surface_unreached` is an invariant asserted by an eval
(`yaml_field`). A single symbol with N test-only referrers contributes N ledger rows but exactly 1 to
`runtime_surface_unreached`.

> **Spec-override annotations (traceability).** Two field definitions here resolve internal inconsistencies in
> the driving spec, choosing the spec's own authoritative *prose* over its §4.5 code-comment:
> (1) `runtime_surface_unreached` / `runtime_surface_degraded` count **symbols** (reduced per-symbol verdict),
> correcting the spec §4.5 comment's "edges" wording per the FR-RSR.2 count-semantics prose (`spec.md:296–313`,
> which makes `len(unreached_surfaces) == runtime_surface_unreached` an invariant); (2) `requirement_id` is
> `str | None` in both `UnreachedSurface` and `RuntimeSurfaceLedgerRow`, correcting the spec §4.5 TypedDicts'
> `str` per the symbol-anchored FR-RSR.1 mandate (a surface hunk with no mapped requirement is tagged
> `requirement_id: null`). The spec was updated to match in the same remediation pass, so spec and TDD now agree.

**Write-ordering for `grounding_gap` evidence_ref.** The ledger is written at **Wave 1A** (sweep);
`grounding-gaps.yaml` rows are written at **Wave 5** (synthesis, §10.6). A `mapped_class: grounding_gap`
`evidence_ref` is **forward-declared at sweep time and RESOLVED at synthesis** — the contract field is
finalized in Wave 5, after both artifacts exist. Regression/drift `evidence_ref`s point at the
Wave-1A ledger row directly.

### 7.2 Data Flow

1. **Tagger (Wave 1A, step 4b')** consumes diff hunks + resolved symbol kinds (`get_symbols_overview`/
   `find_symbol`) + the surface allowlist → produces `runtime_surface_requirements` (+ symbol→requirement_id
   attribute map, requirement_id nullable).
2. **Sweep (Wave 1A, step 4b)** consumes the tagged symbols + the `find_referencing_symbols` referrer set
   + the lang→(marker,syntax) table + the oracle + the rootwalk → produces `runtime-surface-ledger.yaml`
   (per-edge) → reduced to per-symbol counts (`runtime_surface_unreached`, `runtime_surface_degraded`).
3. **Gate (Wave 2)** consumes `runtime_surface_unreached` → forbid-STOP pre-filter decision →
   `tier_decision.yaml` records `surface_unreached` reason.
4. **Modifier (Wave 5)** consumes ledger statuses + contradiction/mapping evidence → `mapped_class` per
   UNREACHED → increments `deviation_count_by_class.regression` (contradiction) or files Drift / §10.6 Gap.
5. **Surface** — contract fields finalized; ledger routed to the qa-persona reviewer brief (T2 only).

### 7.3 Data Storage

All artifacts are per-run files under `<output>/artifacts/` (the default output dir is
`.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`, SKILL.md:76). No database, no persistent store. Serena
memory is untouched by this feature. The `<output>` path is forbidden from resolving under
`.claude/skills|agents|commands/` (existing §3.3 hard STOP, SKILL.md:111).

---

## 8. API Specifications

### 8.1 API Overview

There is **no HTTP API**. The "API" surface of this feature is (1) the **CLI flag interaction** (no new
flags — see §8.2) and (2) the **return-contract** (the six additive fields — see §7.1). This section
documents both as the skill's external contract.

### 8.2 Endpoint Details (CLI flag interaction)

The feature adds **no new CLI flags**. It activates automatically inside UC-2 (`--mode post`) and is
governed by existing pins:

| Option | Type | Default | Behavior with this feature |
|--------|------|---------|----------------------------|
| `--mode post` | enum | (mode-selected) | UC-2; the only mode in which the tagger + sweep run (FR-RSR.1). |
| `--tier 1` | pin | unset | Overrides the `surface_unreached` forbid-STOP pre-filter; emits a loud WARN naming the flag and forces `status: partial` (FR-RSR.5). |
| `--depth quick` | pin | unset | Same override semantics as `--tier 1` against the pre-filter (FR-RSR.5). |
| `--no-mcp` / `backend: none` | flag/env | unset | Degrades the Serena backend; the sweep fails open to a §10.6 Grounding Gap (FR-RSR.8), never STOP. |

### 8.3 Error Response Format (contract degradation signals)

The feature never raises; it degrades. Degradation is surfaced via:

- `runtime_surface_degraded: true` + a §10.6 Grounding Gap row (`needs_human_decision: true`,
  `status: partial`).
- `degraded_components += "runtime-surface:backend_unavailable"` (FR-RSR.8) appended to the existing
  telemetry list (SKILL.md:815).
- The §5.3 pre-filter override WARN (when a pin forces past `surface_unreached`).

### 8.4 API Governance & Versioning

**Contract bump 1.5.0 → 1.6.0 (additive minor, §9.4).** Per the §9.4 versioning rule (SKILL.md:877), a minor
bump is "purely additive — new top-level field(s), no existing field renamed/removed/retyped, no semantic
change." All six new fields are additive. The one existing load-bearing field whose *value* can now move is
`deviation_count_by_class.regression` (sprint consumer, SKILL.md:858) — but its **semantics are unchanged**
("a regression occurred"); FR-RSR.6 only adds a new evidence *source* (an UNREACHED contradiction) feeding
the same field with the same meaning. This is not a rename/removal/retype/semantic-change, so it remains a
minor bump. `verification_regressions_detected` is explicitly NOT touched (stays exit-code-sourced).

**§9.3 Consumer Field Map.** One new **advisory** UC-2 consumer row documents the six fields as non-gating
for every existing consumer (read-and-ignore forward-compat). No existing consumer's load-bearing row gains
a field, so the §9.3 field-deletion guard (SKILL.md:868) is not triggered.

**FR-RSR.9 reviewer-brief routing — "exactly three sections" invariant.** The ledger is routed into the T2
reviewer brief as a **grounding-hunk artifact-ref** under the existing `## Grounding hunks` H2 section
(`refs/reviewer-spec.md:31`), filtered to the **qa**-persona reviewer (who owns the coverage/acceptance
surface). It is an entry under that section — **NOT a fourth top-level section**. This mirrors the existing
FR-4 verify-log routing pattern (`refs/reviewer-spec.md:43`), which already preserves the three-section
invariant. The artifact ref is byte-preserved so the Wave-5 evidence-validator can re-Read it.

---

## 9. State Management

N/A — sc:reflect is a stateless batch review pass; the feature holds no client/UI state. The only
"state" is the per-run artifact set under `<output>/` (§7.3), which is write-once per run.

---

## 10. Component Inventory

N/A — no frontend / no React components. The "components" of this feature are the Markdown skill edits and
one new `refs/` file, enumerated in §6 and §18.2.

---

## 11. User Flows & Interactions

### 11.1 Primary User Flow: Unwired user surface is escalated instead of clean-passed (the FR-S9-04 case)

This is the motivating incident, traced before/after. (Spec §2.3 Gherkin.)

```gherkin
Scenario: Unwired user surface is escalated instead of clean-passed
  GIVEN a UC-2 audit of a diff implementing FR-S9-04 ("user can reach /ai and invoke Spawn")
    AND the Spawn handler symbol is touched by a diff hunk whose kind/decorator matches the surface allowlist
    AND every referrer of the Spawn handler resolves to a test file or a doc-comment
    AND no [project.scripts]/route/registry entrypoint root reaches the Spawn handler

  # --- BEFORE (pre-change skill) ---
  WHEN reflect runs Wave 1A
   THEN no reachability signal is produced (find_referencing_symbols result discarded)
    AND C >= 0.90, S_scope <= 5, S_domains == 1, S_dev_density <= 0.05, coverage_pct >= floor
    AND §5.3 row 1 fires -> STOP at Tier 1
    AND status: success, deviation_count_by_class.regression == 0     # the defect: clean PASS

  # --- AFTER (post-change skill) ---
  WHEN reflect runs Wave 1A with the tagger + sweep
   THEN runtime_surface_requirements == ["FR-S9-04"]                  # TAGGER (symbol-anchored)
    AND the Spawn handler reduces to UNREACHED (test/comment-only referrers, no root)  # SWEEP+ROOTWALK
    AND runtime_surface_unreached == 1 AND len(unreached_surfaces) == 1
    AND §5.3 forbid-STOP pre-filter `surface_unreached` blocks row 1 -> route Tier 2   # FR-RSR.5
    AND §10.9 maps the contradicted criterion to Regression: deviation_count_by_class.regression == 1  # FR-RSR.6
    AND verification_regressions_detected is UNCHANGED (evidence-sourced, not exit-sourced)
    AND status != success; the finding ships in the deviation register
```

### 11.2 Secondary User Flow: Idiomatic dynamic wiring degrades loud, never false-Regression

```gherkin
Scenario: Idiomatic [project.scripts] wiring degrades loud, never false-Regression
  GIVEN a UC-2 audit of a diff adding a CLI command wired via [project.scripts]
        (e.g. `ic = superclaude.cli.ic:main`) with zero static callers
  WHEN reflect runs the tagger + sweep
   THEN the command symbol is tagged (surface allowlist match)
    AND the degrade oracle (FR-RSR.3) matches the [project.scripts] row -> status: DEGRADE
    AND runtime_surface_degraded == true AND runtime_surface_unreached == 0
    AND a §10.6 Grounding Gap row is filed (needs_human_decision: true, status: partial)
    AND deviation_count_by_class.regression is UNCHANGED (NO false Regression)   # NFR-RSR.3
    AND the forbid-STOP pre-filter does NOT force Tier 2 (degrade-only; FR-RSR.5 / D11)
```

---

## 12. Error Handling & Edge Cases

### 12.1 Error Categories

| Category | Trigger | Handling |
|----------|---------|----------|
| Kind-resolution failure | `get_symbols_overview`/`find_symbol` cannot resolve a hunk's symbol kind (parse failure / `backend: none`) | Hunk routes to **DEGRADE** (Grounding Gap), never silent-skip (FR-RSR.1) |
| Dynamic/registry/decorator/reflection wiring | Oracle row match | **DEGRADE → §10.6 Grounding Gap**, never Regression (FR-RSR.3) |
| Unknown language / comment-ambiguous referrer | No lang-table row, or comment classification ambiguous | **DEGRADE**, never "treat as production" (FR-RSR.2) |
| Partial rootwalk | Any root errors/skips, or depth bound hit before resolution | **DEGRADE**, never UNREACHED (FR-RSR.4) |
| Backend / tool loss | `backend: none`, Serena unavailable, `find_referencing_symbols` fails, §0.5d reports chain degraded | **DEGRADE** + `degraded_components += "runtime-surface:backend_unavailable"`; skill continues (FR-RSR.8) |

### 12.2 Edge Cases

- **Surface hunk with no mapped requirement** → tagged with `requirement_id: null`; sweep runs; UNREACHED
  maps to §10.3 Drift (unmapped), never dropped by missing-id (FR-RSR.1).
- **Symbol with N test-only referrers** → N ledger rows, 1 contribution to `runtime_surface_unreached`
  (count invariant, §7.1).
- **Inline test modules** (`#[cfg(test)]`, in-file `Test*`) → counted as test, not production; lang-table
  must catch in-file markers, not only path-based test detection (FR-RSR.2).
- **Symbol called only by other unreached production code** → referrer-only check would read REACHED; the
  mandatory rootwalk (FR-RSR.4) catches the dead-production-caller false-negative.
- **Non-surface diff** → `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, zero added
  cost (NFR-RSR.1).
- **UNREACHED that is both contradiction AND unmapped** → **Regression** wins (contradiction precedence,
  mirroring §10.5 "rationale does not override a contradiction", SKILL.md:982).

### 12.3 Graceful Degradation (fail-open, the doctrine)

The feature inherits the §6.5 fail-open policy (SKILL.md:563–565): "The protocol must never abort because
Serena is unavailable." Every uncertainty resolves to **DEGRADE → §10.6 Grounding Gap**, which independently
forces `status: partial` + `needs_human_decision: true` (SKILL.md:1002–1006). The asymmetric-cost default is:
when in doubt, DEGRADE — never silent-PASS an untested surface, never silent-Regression a real finding. The
three-branch §10.9 mapping is **totally ordered**: evaluate DEGRADE first (no decided verdict → Grounding
Gap), else contradiction → Regression, else → Drift.

### 12.4 Retry & Recovery Strategies

No retry logic is added by this feature. A `find_referencing_symbols` failure mid-sweep degrades **that
edge** to Grounding Gap (records `degraded_components`) and the sweep continues over remaining edges. There
is no global abort. (The existing §6.1 step-5.5 flaky-retry logic, SKILL.md:971, is unrelated and untouched.)

---

## 13. Security Considerations

### 13.1 Threat Model

The feature is **read-only** and operates on the user's own repository under an existing skill. The relevant
"security" concerns are integrity/correctness, not external attack surface:

- **Silent no-op (the primary threat).** A sweep that silently no-ops on `backend: none` or dynamic wiring
  would reproduce the original blind spot — an integrity failure that ships unreachable features as PASS.
  Mitigated by the fail-loud doctrine (FR-RSR.3/8) and the `uc2-surface-degraded-backend` /
  `uc2-surface-dynamic-dispatch` companions.
- **False-Regression rollback amplification.** A false `UNREACHED → Regression` triggers a TurnLedger
  rollback in the sprint consumer — a destructive downstream side-effect. Mitigated by D5/D8/NFR-RSR.3.

### 13.2 Security Controls

- **No new write paths.** Sweep writes only under `<output>/artifacts/`; the §3.3 hard-STOP forbidding
  `<output>` under `.claude/skills|agents|commands/` (SKILL.md:111) still applies.
- **No shell execution added.** The feature uses only the existing read-only Serena symbol tools
  (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`). It does NOT touch the §6.1.1
  `execute_shell_command` verification triangle.
- **CLAUDE.md SoT discipline.** Edits land only in `src/superclaude/`; `.claude/` mirrors are never staged.

### 13.3 Sensitive Data Handling

No credentials, PII, or secrets. The ledger contains only symbol name-paths and `file:line` refs from the
repository under audit.

### 13.4 Data Governance & Compliance

N/A — local developer tooling; no regulated data.

---

## 14. Observability & Monitoring

### 14.1 Logging

Each new Wave-1A step emits **one `audit.log` row** per the §4 per-step convention (SKILL.md:127):
`{wave: 1, step: 4b'|4b, timestamp, outcome: ok|warn|fail|skip, evidence_ref}`. On a non-surface diff,
`runtime_surface_sweep_ran: false` ⇒ **no** `runtime-surface:*` audit rows (NFR-RSR.1).

### 14.2 Metrics (contract + telemetry fields)

| Field | Block | Meaning |
|-------|-------|---------|
| `runtime_surface_sweep_ran` | §9.1 stable | sweep fired (≥1 tagged surface) |
| `runtime_surface_unreached` | §9.1 stable | per-symbol UNREACHED count (drives the gate) |
| `runtime_surface_degraded` | §9.1 stable | ≥1 edge degraded |
| `runtime_surface_ledger_path` | §9.1 stable | abs path to the ledger artifact |
| `degraded_components += "runtime-surface:backend_unavailable"` | §9.2 telemetry | backend/tool loss (FR-RSR.8) |
| `tier_decision.yaml` `surface_unreached` reason | §5.4 artifact | forced-T2 audit visibility |

### 14.3 Tracing

The per-edge ledger **is** the trace: each row's `edge` + `status` + `evidence_ref` lets an operator
reconstruct exactly why a symbol reduced to REACHED / UNREACHED / DEGRADE.

### 14.4 Alerts

No automated alerting (interactive/CI skill). The "alert" channels are: the loud WARN on a pin override,
the `status: partial` forcing, and the eval-suite failure in CI.

### 14.5 Dashboards / 14.6 Business Metric Instrumentation

N/A — eval `grading.json` / `metrics.json` aggregation is the only dashboarding surface, inherited
unchanged.

---

## 15. Testing Strategy

### 15.1 Test Pyramid

Tests are **eval-driven** via `.dev/eval-workspaces/sc-reflect/` + `grader.py`. The grader provides the
assertion types this feature uses (verified present): `regex_absent` (grader.py:162),
`regex_present` (grader.py:152), `yaml_field` (grader.py:336), `falsifier_skeleton_present`
(grader.py:270/405). One **active** headline case with real fixtures + four **MAIN** companions + the two
**existing falsifier skeletons** remaining green.

### 15.2 Test Cases

| Case (dir under `evals/`) | Type | Validates | Assertions |
|---------------------------|------|-----------|------------|
| `uc2-unwired-surface-passes` (**active**, real fixtures) | integration | FR-RSR.1/2/5/6 end-to-end: unwired surface → escalation, no clean PASS | `regex_absent` on a clean-pass marker; `yaml_field` `runtime_surface_unreached ≥ 1`; **FAIL pre-change / PASS post-change** |
| `uc2-surface-positive-control` | unit | FR-RSR.2/4: genuinely-wired surface → REACHED, no escalation, no sweep cost on non-surface | `yaml_field` `runtime_surface_unreached == 0`; NFR-RSR.1 no-sweep assert |
| `uc2-surface-dynamic-dispatch` | unit | FR-RSR.3: `[project.scripts]`/decorator/registry → DEGRADE, never Regression | `yaml_field` `runtime_surface_degraded: true`; assert `deviation_count_by_class.regression` unchanged (NFR-RSR.3) |
| `uc2-surface-degraded-backend` | unit | FR-RSR.8: `backend: none` → Grounding Gap, no STOP | `yaml_field` `runtime_surface_degraded: true`; skill-continues; `regex_absent` clean-pass |
| `uc2-surface-test-only-ref` | unit | FR-RSR.2: referrers only in tests/comments/inline-test → UNREACHED | `yaml_field` `runtime_surface_unreached ≥ 1`; count invariant `len(unreached_surfaces) == runtime_surface_unreached` |
| `T2-converges-on-wrong`, `T2-judge-class-collision` (existing skeletons) | falsifier | regression-guard: must still pass `falsifier_skeleton_present` | unchanged |

**Count-invariant coverage.** At least one companion asserts `len(unreached_surfaces) == runtime_surface_unreached`
via `yaml_field` (FR-RSR.10 acceptance criterion).

### 15.3 Test Environments

UV-only for grader work (`uv run python .dev/eval-workspaces/sc-reflect/grader.py ...`). The eval runner
executes reflect against fixtures; the headline case runs against **both** the pre-change skill snapshot
(`skill-snapshot/reflect-v1.md`) and the post-change SKILL.md to prove fail-before / pass-after. Real
fixtures are mandatory — skeletons pass vacuously (`falsifier_skeleton_present` only checks structural
contract; README dual-state lifecycle).

---

## 16. Accessibility Requirements

N/A — CLI/skill protocol; no UI surface.

---

## 17. Performance Budgets

### 17.1 / 17.2 Cost Budgets

| Path | Budget | Source |
|------|--------|--------|
| Non-surface UC-2 diff | **0** extra MCP/tool calls beyond the existing Wave-1A chain | NFR-RSR.1 |
| Surface diff | The sweep **reuses** the already-fetched `find_referencing_symbols` result (SKILL.md:463) — no new referrer-fetch tool call; partition + reduce is in-context computation | D3 |
| Rootwalk | Bounded by OQ-RSR.3 depth bound (mirror the §4.0 link-following depth=1 convention) — partial enumeration DEGRADEs rather than recursing unbounded | FR-RSR.4 |
| UC-1 run | 0 — tagger never runs in `--mode pre` | FR-RSR.1 |

The feature does not change the §15 token cost bands; it adds in-context filtering, not new agent fan-out.

### 17.3 Performance Testing

NFR-RSR.2 determinism is performance-adjacent: re-run the headline fixture twice and assert a byte-identical
ledger (proves the LLM-free path).

---

## 18. Dependencies

### 18.1 External Dependencies

None added. Uses only existing Serena MCP read-only symbol tools already in `allowed-tools` (SKILL.md:5):
`mcp__serena__get_symbols_overview`, `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`.

### 18.2 Internal Dependencies (modified + new files)

**New files:**

| File | Purpose |
|------|---------|
| `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` | **Source of truth** for the tagger allowlist, the language→(test-marker, comment-syntax) table, the degrade-oracle table, the rootwalk algorithm, and the `runtime-surface-ledger.yaml` schema |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-unwired-surface-passes/` (+ fixtures) | Headline active eval (FAIL pre / PASS post) |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-positive-control/` (+ fixtures) | Genuinely-wired → REACHED |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-dynamic-dispatch/` (+ fixtures) | Registry/decorator/`[project.scripts]` → Grounding Gap, never Regression |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-degraded-backend/` (+ fixtures) | `backend: none` → Grounding Gap, no STOP |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-test-only-ref/` (+ fixtures) | Tests/comments-only referrers → UNREACHED |
| `<output>/artifacts/runtime-surface-ledger.yaml` (**runtime artifact, per-run** — not a source file) | Per-edge reachability ledger written by the FR-RSR.2 sweep at Wave 1A; schema = `RuntimeSurfaceLedgerRow` (§7.1). Listed for implementer-checklist completeness; produced at runtime, never committed |

**Modified files:**

| File | Change |
|------|--------|
| `SKILL.md` §6.1 | Add Wave-1A steps **4b'** (tagger) and **4b** (sweep) extending step 4; UC-2-only, fail-open, one `audit.log` row each |
| `SKILL.md` §5.3 + pre-filter precedence ¶ (SKILL.md:402) | Add `surface_unreached` to the table-wide forbid-STOP pre-filter set |
| `SKILL.md` §5.4 `tier_decision.yaml` | Record `surface_unreached` as a forced-T2 reason |
| `SKILL.md` §10 (new §10.9) | Add UNREACHED finding-modifier mapping onto the 4 classes by evidence; no 5th class |
| `SKILL.md` §9.1 stable contract | Add 6 additive fields; bump `contract_version` 1.5.0 → 1.6.0 |
| `SKILL.md` §9.3 Consumer Field Map | Add one advisory UC-2 consumer row (non-gating) |
| `refs/reviewer-spec.md` | Add FR-RSR.9 ledger grounding-hunk entry (qa persona); preserve "exactly three sections" |
| `refs/deviation-taxonomy.md` | Cross-reference the §10.9 UNREACHED-by-evidence mapping |
| `.dev/eval-workspaces/sc-reflect/grader.py` | Ensure `regex_absent` / `yaml_field` cover the new fields (extend only if needed) |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/…` | Promote/author the relevant active companion per FR-RSR.10. **Primary** placement of the headline + 4 companions is MAIN `evals/` (above); this row records the spec §4.2 falsifier-suite touch — the two pre-existing skeletons (`T2-converges-on-wrong`, `T2-judge-class-collision`) remain green and unmodified |

### 18.3 Infrastructure Dependencies

`make sync-dev` + `make verify-sync` (sync `src/` → `.claude/`); UV toolchain for grader. No CI infra change.

---

## 19. Migration & Rollout Plan

### 19.1 Migration Strategy

Pure **additive minor** — no migration. Existing consumers read-and-ignore the six new fields (§9.4
forward-compat). UC-1 and non-surface UC-2 runs emit inert defaults, so existing behavior is byte-stable
on those paths.

### 19.2 Feature Flags & Progressive Delivery

No runtime flag. The capability is governed by existing pins (`--tier 1` / `--depth quick` override the
pre-filter; `--no-mcp` degrades the backend). The eval headline case is the progressive-delivery gate: it
must FAIL on the pre-change snapshot before the post-change skill is allowed to ship.

### 19.3 Rollout Stages (implementation order)

Per spec §4.6 (dependency-ordered):

1. `refs/runtime-surface.md` — author allowlist + lang table + oracle table + rootwalk + ledger schema
   (critical-path predecessor for everything).
2. SKILL.md §6.1 steps 4b' + 4b (tagger + sweep) **‖** §9.1 +6 fields + `contract_version` 1.6.0
   (parallelizable — contract is additive, no dependency on sweep internals).
3. SKILL.md §5.3 forbid-STOP pre-filter + §5.4 (reads `runtime_surface_unreached`).
4. SKILL.md §10.9 finding-modifier + `deviation-taxonomy.md` xref (consumes ledger status).
5. `refs/reviewer-spec.md` ledger grounding-hunk ref (parallel with 3,4).
6. §9.3 consumer-field-map advisory row.
7. Eval cases (1 active headline + 4 MAIN companions) + grader assertions.
8. `make sync-dev && make verify-sync`.

### 19.4 Rollback Procedure

Revert the SKILL.md + `refs/` edits and re-run `make sync-dev && make verify-sync`. Because the change is
additive and gated behind UC-2 surface detection, rollback restores exact prior behavior. The contract
version reverts 1.6.0 → 1.5.0; consumers that opted into the new fields simply stop seeing them (they were
advisory).

---

## 20. Risks & Mitigations

| Risk | Prob. | Impact | Mitigation |
|------|-------|--------|------------|
| Sweep silently no-ops on `backend: none` / dynamic wiring → reproduces the original blind spot | High | High | FR-RSR.3 oracle defaults uncertainty to **DEGRADE → Grounding Gap** (fail loud); FR-RSR.8 asserts no silent PASS; `uc2-surface-dynamic-dispatch` + `uc2-surface-degraded-backend` encode it |
| False `UNREACHED → Regression` on idiomatic `[project.scripts]`/decorator wiring triggers unconditional T2+T3 + TurnLedger rollback | Medium | High | Degrade oracle never maps wiring to Regression (NFR-RSR.3); dead-caller false-negative covered by mandatory FR-RSR.4 rootwalk; companion asserts zero Regression increment |
| Plain §5.3 row shadowed by first-match-wins row 1 → escalation never fires | Medium | High | FR-RSR.5 uses a **table-wide forbid-STOP pre-filter** (proven `coverage_degraded` shape), not a row |
| Conflating UNREACHED Regression with verified-regression count corrupts `verification_regressions_detected` | Medium | Medium | FR-RSR.6 increments **only** `deviation_count_by_class.regression`; grader asserts `verification_regressions_detected` unchanged |
| Skeleton eval cases pass vacuously → fix looks tested but isn't | Medium | High | FR-RSR.10 ships the headline case `status: active` with real fixtures + fail-before/pass-after; companions in MAIN `evals/`, not skeleton falsifier-suite |
| Reviewer brief gains a 4th section → breaks `reviewer-spec.md` invariant | Low | Medium | FR-RSR.9 routes the ledger as a grounding-hunk **entry** under existing `## Grounding hunks`, asserted by the three-section invariant |
| Unknown-language test/comment detection misfires → real test referrer counted as production | Medium | Medium | Lang→(marker,syntax) table; unknown language / comment-ambiguous → DEGRADE, never "treat as production" |
| **Tagger keyed off requirement id instead of symbol** (the sequencing hazard) → ordering quirk emits `[]` → original bug returns | Medium | High | **Symbol-anchored design (D1/FR-RSR.1)** — the tagger keys off the Wave-1A resolved symbol; requirement id is an optional attribute, never a gate |

---

## 21. Alternatives Considered

### Alternative 0: Do Nothing (mandatory)

Leave UC-2 unable to detect complete-but-unintegrated features. **Rejected** — the motivating FR-S9-04
incident shipped an unreachable user-facing feature with a "100% adherence" PASS; the blind spot is
structural and will recur on every additive, well-tested, unwired leaf.

### Alternative 1: Static reachability *proof* (whole-program call graph)

Build a real call graph and *prove* reachability. **Rejected** — reachability is **semi-decidable** under
dynamic dispatch, plugin/registry wiring, reflection, and `console_scripts`. A proof would either over-claim
(silent PASS on dynamic wiring) or over-block (false Regression on idiomatic registry wiring). Escalation +
loud degrade is the only sound posture (spec §2.1; this TDD D2).

### Alternative 2: New standalone reachability agent + a 5th deviation class

Add a dedicated reachability agent writing into a new `unreached` taxonomy class. **Rejected** on two
counts: (1) the referrer set is *already fetched and discarded* (SKILL.md:463) — partitioning it is a filter,
not a new agent; a new agent adds coordination cost and breaks fail-open inheritance (D3). (2) §17.7 Kill
List item 6 (SKILL.md:1799) explicitly rejected a 5th deviation class for structural cleanliness; the §10.8
Reuse-Miss finding-modifier is the established "map onto the 4 by evidence" pattern (D7).

### Alternative 3: Plain inserted §5.3 row (instead of a pre-filter)

Insert a new escalation row into §5.3. **Rejected** — §5.3 is first-match-wins (SKILL.md:386); a plain row
is shadowed by row 1's earlier STOP on the exact unwired-leaf signature. The table-wide forbid-STOP
pre-filter (`coverage_degraded` shape, SKILL.md:402) is the only shape that forbids ALL STOP rows when set
(D6).

---

## 22. Open Questions

| ID | Question | Impact | Resolution target |
|----|----------|--------|-------------------|
| OQ-RSR.1 | Final surface-keyword/decorator allowlist contents (per-language) | Medium — under-broad misses surfaces; over-broad adds cost | Enumerate in `refs/runtime-surface.md`; validate against companion fixtures |
| OQ-RSR.2 | Exact lang→(test-marker, comment-syntax) table rows beyond py/rust/ts | Medium — unknown languages DEGRADE (safe) but coverage matters | Author py/rust/ts/js/go rows in v1; others DEGRADE until added |
| OQ-RSR.3 | Rootwalk depth bound for entrypoint reachability | Low — too-shallow over-DEGRADEs (safe) | Pick a bounded depth (mirror §4.0 link-following depth=1) in `runtime-surface.md` |
| OQ-RSR.4 | Whether `runtime_surface_*` should feed `S_dev_density` as a parallel up-weight | Low — additive enrichment, not gating | Defer; v1 routes via the forbid-STOP pre-filter only |
| OQ-RSR.5 | Is a TurnLedger rollback the right sprint-consumer action for an UNREACHED-contradiction Regression? | Medium — rollback is heavy; but unwired user surface is "should not ship" | v1 accepts §10.9 by-evidence routing; revisit on iteration-2 false-fire telemetry |

---

## 23. Timeline & Milestones

### 23.1 High-Level Timeline

Single coordinated skill change; milestones map to the §19.3 rollout stages (spec §4.6 implementation
order). No multi-sprint timeline — this is one bounded skill-hardening unit.

### 23.2 Implementation Phases

| Phase | Theme (spec §10) | FRs | Gate |
|-------|------------------|-----|------|
| P1 | **Source of truth** | `refs/runtime-surface.md` | allowlist + tables + rootwalk + ledger schema authored |
| P2 | **Gather** | FR-RSR.1, FR-RSR.2, FR-RSR.3, FR-RSR.4 | tagger + sweep + oracle + rootwalk land; UNREACHED only emittable after FR-RSR.3/4 |
| P3 | **Gate** | FR-RSR.5 | forbid-STOP pre-filter routes T2; `tier_decision.yaml` reason recorded |
| P4 | **Classify** | FR-RSR.6 | §10.9 modifier maps by evidence; regression counter hygiene (D8) |
| P5 | **Surface** | FR-RSR.7, FR-RSR.9 | contract 1.6.0 + ledger + reviewer-brief ref; three-section invariant intact |
| P6 | **Falsify** | FR-RSR.10 | active headline FAILs pre / PASSes post; companions green; existing falsifiers green |

**Blocker ordering:** FR-RSR.3 (oracle) and FR-RSR.4 (rootwalk) are the highest-risk tasks and MUST land
before any UNREACHED verdict is emittable (gate them as blockers of FR-RSR.2's UNREACHED path). The contract
task (FR-RSR.7) is parallelizable with the sweep task. The eval task (FR-RSR.10) is terminal — the headline
case is the acceptance gate.

---

## 24. Release Criteria

### 24.1 Definition of Done

- [ ] `refs/runtime-surface.md` authored: allowlist (OQ-RSR.1), lang→(marker,syntax) table (OQ-RSR.2),
      degrade-oracle table covering categories (a)–(d), rootwalk algorithm with depth bound (OQ-RSR.3),
      ledger schema.
- [ ] SKILL.md §6.1 steps 4b' (symbol-anchored tagger) + 4b (sweep) added; both UC-2-only, fail-open, one
      `audit.log` row each.
- [ ] SKILL.md §5.3 `surface_unreached` added to the table-wide forbid-STOP pre-filter set + §5.4 reason.
- [ ] SKILL.md §10.9 finding-modifier added (by-evidence mapping; **no** 5th class; **no** new counter).
- [ ] SKILL.md §9.1 six additive fields + `contract_version: "1.6.0"`; §9.3 advisory consumer row.
- [ ] `refs/reviewer-spec.md` ledger grounding-hunk entry (qa persona); three-section invariant holds.
- [ ] `refs/deviation-taxonomy.md` cross-references §10.9.
- [ ] Eval: `uc2-unwired-surface-passes` (active, real fixtures) FAILs pre-change / PASSes post-change;
      four MAIN companions present; `len(unreached_surfaces) == runtime_surface_unreached` asserted;
      existing `T2-converges-on-wrong` / `T2-judge-class-collision` skeletons still pass.
- [ ] `make sync-dev` → `make verify-sync` clean; no `.claude/` mirror staged; UV-only for grader.

### 24.2 Release Checklist

- [ ] `make verify-sync` green (NFR-RSR.5).
- [ ] Unchanged-fields grader assertion confirms all pre-1.6.0 fields intact (NFR-RSR.4).
- [ ] `uc2-surface-dynamic-dispatch` asserts zero `deviation_count_by_class.regression` increment (NFR-RSR.3).
- [ ] `verification_regressions_detected` never incremented by a reachability finding (D8 grader assertion).
- [ ] Determinism: byte-identical ledger across two runs (NFR-RSR.2).

---

## 25. Operational Readiness

### 25.1 Runbook

- **A reachability finding fired unexpectedly:** inspect `<output>/artifacts/runtime-surface-ledger.yaml`;
  each row's `edge` + `status` + `evidence_ref` explains the verdict. A DEGRADE row carries a §10.6
  Grounding Gap (needs human decision) — resolve by confirming the wiring idiom and, if a real entrypoint
  exists, extend the oracle/rootwalk table in `refs/runtime-surface.md`.
- **Idiomatic wiring false-flagged as UNREACHED:** this is a defect — the oracle should have DEGRADEd it.
  Add the wiring idiom as an oracle row (FR-RSR.3) and add a companion fixture.
- **Override the escalation:** `--tier 1` or `--depth quick` proceeds at the pinned tier with a loud WARN
  and `status: partial`.

### 25.2 On-Call Expectations

N/A — developer-tooling skill; no production on-call. CI eval failure is the only operational signal.

### 25.3 Capacity Planning

N/A — no runtime capacity; the only "capacity" is the per-run token budget, unchanged (§17).

---

## 26. Cost & Resource Estimation

The only cost is **token cost**, and the feature is designed to add **zero** on the common path:

- Non-surface UC-2 diff and all UC-1 runs: 0 added MCP/tool calls (NFR-RSR.1).
- Surface diff: the sweep reuses the already-fetched referrer set (SKILL.md:463) — partition/reduce is
  in-context, no new fetch. The rootwalk is depth-bounded (OQ-RSR.3).
- The asymmetric cost the design optimizes is **downstream**: a false `UNREACHED → Regression` would cost a
  full T2+T3 cycle plus a TurnLedger rollback; the degrade-default (D5) avoids paying it on idiomatic wiring.

---

## 27. References & Resources

### 27.1 Related Documents

| Document | Relevance |
|----------|-----------|
| `.dev/reflect-hardening/issue-1-uc2-reachability/spec.md` | Parent spec (FR-RSR.1–10, NFRs, risks) |
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §5.3, §6.1, §9.1, §9.3, §9.4, §10, §17.7 | Primary modification target; the four structural facts the fix addresses |
| `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md` | Establishes that coverage proves mapping, not reachability (fact 3) |
| `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | The contradiction-anchored taxonomy that is the missing sink (fact 4); §10.9 xref target |
| `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | "Exactly three sections" invariant (lines 23, 43, 45, 47) the ledger-routing FR must preserve (FR-RSR.9) |
| `.dev/eval-workspaces/sc-reflect/grader.py` | `regex_absent` (162), `yaml_field` (336), `falsifier_skeleton_present` (270/405) assertion types |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` | Dual-state skeleton/active lifecycle the eval FR follows |
| `pyproject.toml` (`[project.scripts]`: `superclaude`, `ic`; lines 67–69) | Concrete in-repo registry entrypoints the degrade oracle MUST NOT false-flag (FR-RSR.3) |

### 27.2 External References

- Mehta (Towards AI, Mar 2026) — single-agent self-review representational bias (SKILL.md:29).
- Khan et al. ICML 2024 Oral; Kenton NeurIPS 2024 — weak-judge-strong-debaters (SKILL.md §11.4).

---

## 28. Glossary

| Term | Definition |
|------|-----------|
| **User-reachable surface** | A symbol constituting a user-facing entry to a feature (CLI command, HTTP route handler, registered command) — what a reachability requirement like "user can reach X" refers to. |
| **Production referrer** | A referrer of a symbol that is NOT in a test file, doc-comment, or inline test module (`#[cfg(test)]`, in-file `Test*`). |
| **UNREACHED** | A tagged surface symbol with zero surviving production referrers AND not reachable from any entrypoint root (FR-RSR.2/4). |
| **DEGRADE** | A reachability verdict the sweep could not soundly decide (dynamic/registry/decorator/reflection wiring, unknown language, backend loss) → routed to §10.6 Grounding Gap, never a blocking class. |
| **Entrypoint-rootwalk** | Enumeration of project entrypoint roots (`[project.scripts]`, app mounts, command registries) to confirm reachability when direct production referrers are absent (FR-RSR.4). Partial enumeration = incompleteness → DEGRADE. |
| **Forbid-STOP pre-filter** | A table-wide §5.3 flag (`surface_unreached`, like `coverage_degraded`) that forbids ALL STOP rows when set, forcing Tier 2 — not a first-match-wins row. |
| **Finding-modifier** | A §10.8-style mechanism mapping a finding onto the existing 4-class taxonomy by evidence — NO 5th class, NO new counter. |
| **Symbol-anchored (vs requirement-anchored)** | The tagger keys off the diff hunk's resolved symbol (Wave 1A), not a requirement id (Wave 1B); requirement id is an optional attribute. Prevents the wave-ordering quirk that would resurrect the clean-pass bug. |
| **Edge vs symbol count** | The ledger is per-edge; all contract/gate counts are per-symbol, reduced under `DEGRADE > UNREACHED > REACHED`. `len(unreached_surfaces) == runtime_surface_unreached` is invariant. |

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-06-19 | user, claude | Initial TDD authored from `issue-1-uc2-reachability/spec.md`, grounded in `sc-reflect-protocol/SKILL.md` (§5.3/§6.1/§9.1/§9.3/§9.4/§10/§17.7), `refs/reviewer-spec.md`, `refs/deviation-taxonomy.md`, the falsifier suite, `grader.py`, and `pyproject.toml` `[project.scripts]`. |
