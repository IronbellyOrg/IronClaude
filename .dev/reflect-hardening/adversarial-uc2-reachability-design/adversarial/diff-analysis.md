# Diff Analysis: Canonical UC-2 Reachability Design (B vs C vs Coexist)

## Metadata
- Generated: 2026-06-20 ~06:10 UTC
- Variants compared: 3 (C-canonical, B-canonical, Coexist)
- Source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/tasklist-overlap-conflict-matrix-fr-rh2-vs-uc2.md`
- Total differences found: 7 structural/content + 4 contradictions + 3 unique + 3 shared assumptions
- Reasoning mode: in-context (fallback_mode=true), single-evaluator with adversarial steelman + Round 2.5 invariant probe

## Structural / Content Differences

| # | Topic | B (runtime-surface) | C (contracted-sink gate) | Severity |
|---|---|---|---|---|
| C-001 | Detection target | Code-symbol reachability — is the surface *wired*? | Runtime side-effect — did a real boot *observe the contracted sink*? | High (different capabilities, not redundant) |
| C-002 | Precision vs recall | High recall, lower precision (dynamic dispatch/reflection confound) | High precision, lower recall (only `@sink`-annotated contracts) | High |
| C-003 | Strongest verdict | DEGRADE / UNREACHED modifier; **does not force Tier 2** | **Regression** via real-boot-only proof | High |
| C-004 | Contract bump | 6 §9.1 `runtime_surface_*` fields → 1.6.0 | 7 R7 `reachability_*` fields → 1.6.0 | High (version collision) |
| C-005 | New ledger | `runtime-surface-ledger.yaml` | `reachability_ledger_path` | Medium |
| C-006 | Eval namespace | `uc2-surface-*`, ids 37-41 | `uc2-reachability-*`, ids unspecified | Medium (shared evals.json) |
| C-007 | Maturity today | Skill + evals only | Skill + wrapper + docs + bounded cost + PRE reflect coverage 1.0 | Medium |

## Contradictions

| # | Point of conflict | B position | C position | Impact |
|---|---|---|---|---|
| X-001 | Who owns `1.6.0` | B's additive bump from 1.5.0 | C's additive bump from 1.5.0 | High — only one can be "the" 1.6.0 additive bump |
| X-002 | Same SKILL.md stable-contract / §10.9 / §9.1 sections | B edits from 1.5.0 baseline | C edits from 1.5.0 baseline | High — independent edits to one location |
| X-003 | `deviation-taxonomy.md` mapping | UNREACHED-by-evidence | real-boot-only Regression / blocking-sink unproven | Medium — coexists only with a precedence rule |
| X-004 | C-040 leakage guard | B *is* `runtime_surface_*`/UNREACHED | C asserts their *absence* | High — mutually exclusive as written |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | C | Real-boot-only Regression proof bar (gate-grade precision) | High |
| U-002 | B | Broad unwired-surface recall incl. un-annotated symbols | Medium |
| U-003 | C | Full operator surface shipped now (wrapper/docs/bounded cost/PRE reflect) | High |

## Shared Assumptions (UNSTATED → promoted)

| A-NNN | Assumption | Source agreement | Status |
|---|---|---|---|
| A-001 | "UC-2 reachability" is ONE feature that one task must own | Both tasks named uc2-reachability and both bump the same contract | **CONTRADICTED** — they are two different detectors; the name collision masks complementary scope |
| A-002 | A new stable contract field is required to expose the signal | Both add stable §9.1/R7 fields | **UNSTATED** — B's advisory signal could be *telemetry*, needing no stable field / no bump |
| A-003 | Exactly one minor version (1.6.0) is available for this work | Both target 1.6.0 | **UNSTATED** — sequential minors (1.6.0, 1.7.0) are available and cheaper than a union |

## Summary
- Highest-severity items: C-001, C-002, C-003, C-004, X-001, X-002, X-004, A-001.
- A-001 (CONTRADICTED) reframes the entire debate: this is **not** "pick one feature, discard the other" — it is "two complementary detectors colliding on packaging (version, file ownership, eval namespace)."
