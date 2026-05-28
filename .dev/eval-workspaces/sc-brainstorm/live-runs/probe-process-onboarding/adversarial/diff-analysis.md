# Diff Analysis: Onboarding Workflow Specification Comparison

## Metadata

- Generated: 2026-05-25T19:32:00Z
- Variants compared: 2
- Variant 1: `variant-1-opus-scribe.md` (opus:scribe — curated documentation spine)
- Variant 2: `variant-2-sonnet-analyzer.md` (sonnet:analyzer — root-cause-driven interventions)
- Total differences found: 19
- Categories: structural (4), content (7), contradictions (2), unique (4), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Taxonomy |
|---|---|---|---|---|---|
| S-001 | Top-level organization | 7 sections (Proposal Summary, FRs, NFRs, Artifacts, Adoption Path, Success Metrics, Open Risks) | 7 sections (Root-Cause Diagnosis, Targeted Interventions, FRs, Falsification Plan, Not-Doing, Success Metrics, Open Assumptions) | Medium | L2 |
| S-002 | Opening framing | Proposal-first (declares the artifact set up front) | Diagnosis-first (causes precede interventions) | Low | L1 |
| S-003 | Requirement decomposition depth | 10 FRs + 8 NFRs (18 total) | 7 FRs (no separate NFR layer) | Medium | L2 |
| S-004 | Falsification surface | Embedded in Success Metrics (M-001…M-006) | Dedicated §4 with per-intervention checks AND embedded in FRs (each FR ends with "Falsifiable: …") | Medium | L3 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity | Taxonomy |
|---|---|---|---|---|---|
| C-001 | Document layout | 4 short guides under `docs/contributing/` (`01-setup.md`, `02-mental-model.md`, `03-first-pr.md`, `04-troubleshooting.md`) + rewritten `CONTRIBUTING.md` | Single `docs/contributor-guide.md` consolidating all topics; existing `CONTRIBUTING.md` retained as CI-hygiene doc | High | L2 |
| C-002 | Make target naming + semantics | `make onboard-check` — verification gate run by CI on PRs touching onboarding surface | `make onboard` — contributor-facing happy-path runner with pass/fail summary + next-steps message | Medium | L3 |
| C-003 | Treatment of existing stale docs | Not addressed (no mention of `docs/developer-guide/` content) | Diagnosed as RC-1 (highest-leverage root cause); explicit deletion/replacement required (FR-001 with grep check) | High | L3 |
| C-004 | Worked example specificity | "Typo fix in a skill `SKILL.md`" — abstract category | Two concrete candidates named: "Change description of `python-expert` agent" or "Add assertion to `tests/pm_agent/test_confidence.py`" | Low | L1 |
| C-005 | Audience targeting | Explicit audience tag header on every guide: `**Audience:** X \| **Time:** Y \| **Prereqs:** Z` | No audience tags; single contributor audience implied | Medium | L2 |
| C-006 | Rejected alternatives section | §7 inline (linear-vs-contextual, setup-vs-concepts, CLI, sandbox, skill, ceremony) — addresses every seed-brief open question | §5 "What We Are NOT Doing" — covers CLI, skill, sandbox, contextual paths, SoT rearchitecture — overlaps but cites different rationales | Medium | L2 |
| C-007 | Baseline measurement | Compares against "30-day baseline" (assumed implicit) | Explicit pre-merge baseline capture: (a) setup-blocked issue count, (b) `.claude/` violation PR count, (c) clean-clone-to-verify wall time | Medium | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Taxonomy |
|---|---|---|---|---|---|
| X-001 | Where the contributor guide lives | `docs/contributing/` directory with 4 files (FR-003) | `docs/contributor-guide.md` single file (FR-002) | Medium — design choice, not logically incompatible | L2 |
| X-002 | Make target name | `make onboard-check` (FR-005) | `make onboard` (FR-003) | Low — naming choice; semantics differ but reconcilable (could have both, or unify) | L1 |

(Neither contradiction is a hard logical conflict; both reflect different design choices that the refactor plan must adjudicate.)

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Two-click rule (FR-004): every confusion point reachable in ≤2 clicks from README, single authoritative paragraph each, no duplication | High |
| U-002 | V1 | `superclaude doctor` integration (FR-009): troubleshooting prefers programmatic doctor checks over prose | Medium |
| U-003 | V1 | Single-line command discipline (NFR-007) explicitly tied to user's terminal constraint (no heredocs/continuations) | Medium |
| U-004 | V1 | Maintainer-DM-as-doc-bug rule (§7 residual): "if a question is asked twice, the doc has failed" — converts DMs into improvement signal | High |
| U-005 | V1 | Brevity caps as enforceable checks (NFR-001 + M-005: `wc -l` gate) | Medium |
| U-006 | V2 | Stale-docs-as-RC-1 diagnosis (entirely absent from V1) — identifies active misinformation in `docs/developer-guide/` as the highest-priority issue | High |
| U-007 | V2 | Causes-vs-Symptoms table — explicit mapping of observed friction to root cause; structures intervention reasoning | High |
| U-008 | V2 | Per-FR inline grep falsification (each FR ends with a concrete grep/timing check) | High |
| U-009 | V2 | Explicit baseline measurement plan (pre-merge data capture for later A/B) | Medium |
| U-010 | V2 | Open Assumptions section (§7) with named A1–A5 — surfaces what could invalidate the intervention | Medium |

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Status |
|---|---|---|---|---|
| A-001 | A Makefile target is the right delivery primitive for the green-bar moment (vs. shell script / Docker / CLI subcommand) | Both propose a Make target (just differ on name) | UNSTATED | Promoted [SHARED-ASSUMPTION] L3 |
| A-002 | A single linear onboarding path is sufficient for the current contributor mix | V1 explicitly chooses linear-with-contextual-depth; V2 explicitly defers contextual paths | STATED (V2) / IMPLIED (V1) | Promoted [SHARED-ASSUMPTION] L2 |
| A-003 | Markdown-in-repo (vs CLI/skill/sandbox) is the correct delivery surface | Both reject identical alternatives | STATED | Not promoted (both state it) |
| A-004 | README is the canonical discovery entry point | Both wire onboarding entry via README pointer | UNSTATED | Promoted [SHARED-ASSUMPTION] L2 |

(Promoted assumptions are included in convergence denominator per AD-2.)

## Summary

- Total structural differences: 4
- Total content differences: 7
- Total contradictions: 2 (both soft / design-choice)
- Total unique contributions: 10 (V1: 5, V2: 5)
- Total shared assumptions promoted: 3 (UNSTATED)
- Highest-severity items: C-001 (document layout), C-003 (stale docs), U-006 (stale-doc gap in V1), U-008 (falsification discipline)

**Total diff points for convergence calculation:** 4 + 7 + 2 + 3 (promoted A-NNN) = **16**

**Taxonomy coverage:** L1 = 3 points (S-002, C-002, C-004, X-002), L2 = 7 points (S-001, S-003, C-001, C-005, C-006, X-001, A-002, A-004), L3 = 6 points (S-004, C-002, C-003, C-007, A-001 + falsification surface) — all three levels covered. No forced round required.
