# Diff Analysis: reflect UC-1 reviewer-card comparison

## Metadata
- Generated: 2026-11-06T22:16:00Z
- Variants compared: 3
  - Variant 1: reviewer-1-card.yaml (sonnet / analyzer), calibrated confidence 0.72
  - Variant 2: reviewer-2-card.yaml (haiku / qa), calibrated confidence 0.66
  - Variant 3: reviewer-3-card.yaml (opus / refactorer), calibrated confidence 0.68
- Input format warning: all three inputs are YAML, not markdown; compared as structured cards.
- Total differences found: 18
- Categories: structural (2), content (5), contradictions (2), unique (5), shared assumptions (4, of which 2 UNSTATED and promoted)
- Ground truth used for adjudication (read-only): plan `TASK-WF-fixIssue412SVeri-20261106-215543.md` (53 lines), `source.md:1`, `src/superclaude/cli/install_user_setup.py:230-263` and `:434-444`, `artifacts/orca-discovery.md`.
- Supplemental context (coordinator, not a new finding): `artifacts/core-install-grounding.yaml` records that `src/superclaude/cli/install_core.py:47-74` copies every top-level `src/superclaude/core/*.md` flat to `~/.claude/<name>` (re-read here: lines 57, 67, 74). The plan's Task 1 rule in `src/superclaude/core/CLAUDE.md` therefore lands in the globally loaded `~/.claude/CLAUDE.md` through the existing installer. Limit: nonforce runs skip existing destinations (line 69), and no global install was executed. This resolves the coverage analyst's "globally loaded" uncertainty (INF-002, F-3) at plan level; it does not change any card's finding.
- All three cards return PASS with zero blocking findings. They differ materially in minor notes (0, 2 and 3 for Variants 2, 3 and 1), so agreement on the top-level verdict is not treated as identity.
- Taxonomy tagging (priority L3 > L2 > L1, default L2): L1 surface = S-001, C-005; L2 structural = S-002, C-002, C-003, C-004, X-001, X-002; L3 state-mechanics = C-001, A-001, A-002. All three levels have coverage; no forced round.

## Structural Differences

| # | Area | Variant 1 (sonnet/analyzer) | Variant 2 (haiku/qa) | Variant 3 (opus/refactorer) | Severity | Level |
|---|------|------|------|------|----------|-------|
| S-001 | Finding container | 3 `minor_findings` (R1-1..R1-3), each with `plan_ref` and `verifier` | `minor_findings: []`; adds `semantic_requirements_audited/covered` counts (21/21) and a top-level `verifiers` list | 2 `minor_findings` (R3-1, R3-2), each with `evidence` and `verifier` | Low | L1 |
| S-002 | Evidence anchoring | Plan line ranges per finding plus an `original_source_ref`/`evidence_pathology` pair recording its own wrong helper range (113-119) | Evidence points only at the reviewer brief (`reviewer-briefs/reviewer-2.md:49-82`, `:137`), not at plan or code | Evidence points at code and test files (`install_user_setup.py:230-263`, `tests/core/test_codegraph_guide.py:137-174`) plus unverified search leads | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|-------|-----------|-----------|-----------|----------|-------|
| C-001 | Exit-0 safe skip with all three guides present | R1-2: "meaningful stdout/stderr and success-prefix handling are not precisely defined"; verifier mocks an exit-0 edited-copy skip with files present and asserts the visible skip text | No finding; self-audit says Task 2 covers "child output"; verifier list includes "output" | R3-2: child output must cover exit-0 safe skips, not only failures, with no keyword parser; verifier mocks exit 0 with three files present and stdout naming a skipped guide | Medium | L3 |
| C-002 | Where Task 1's routing and sync checks run | R1-1: they run in Task 2, so failures surface later; own note says not an omission | No finding | Self-audit: "Task 2 sync delivers its README edit" | Low | L2 |
| C-003 | Agent terminal surface versus New Terminal shell wording | R1-3: static wording could blur the two; verifier asserts terminal surface tied to agent creation and shell routes prohibited | Self-audit: Task 1 covers the global selection rule and shell distinction | Silent | Medium | L2 |
| C-004 | Wider regression for other tests reading core CLAUDE.md | Silent | Silent (Task 2 named tests deemed sufficient) | R3-1: one verified reader (`tests/core/test_codegraph_guide.py:137-174`) plus three unverified leads; include relevant core-doc tests in Task 2 regression evidence | Low | L2 |
| C-005 | Coverage claim | No count | Semantic 21/21 (reviewer judgment) | No count | Medium | L1 |

Note on C-005: the deterministic lexical containment for this run is 13/21 = 0.6190. Shared plan Constraints (lines 19-24) are outside the matcher. Variant 2's semantic 21/21 is reviewer judgment and is not substituted for the lexical figure anywhere in this pipeline.

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact | Level |
|---|-------------------|-----------|-----------|-----------|--------|-------|
| X-001 | Does the plan forbid New Terminal for ccsession sessions, or only distinguish? | Limitation: reviewer wording says the AC forbids New Terminal, while the literal AC says "distinguish" | Treats Task 1 as covering the shell distinction fully | No position | Medium | L2 |
| X-002 | Is the success/skip output behaviour precisely specified? | Not precisely defined (R1-2) | Fully covered; zero minor findings | Needs exit-0 skip coverage made explicit (R3-2) | Medium | L2 |

Ground truth for X-001: plan line 35 says "explicitly distinguish Claude (CLI) ... from New Terminal and terminal create for shells". `source.md:1` says "use Claude (CLI), never New Terminal". Plan line 30 (Task 1 Inputs) takes "the explicit launch requirement in source.md" as input. The prohibition therefore reaches Task 1 through its Inputs; the AC wording is weaker than the source.

Ground truth for X-002: plan line 45 requires relaying meaningful stdout/stderr "so edited/foreign guide skips cannot be hidden by an unconditional success summary"; plan line 51 requires surfacing skipped/warning output "including when files already exist"; plan line 24 forbids treating a safe skip as proof of refresh. The requirement exists; what is unspecified is the exact test fixture for an exit-0 skip.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | R1-1: run routing and sync checks after Task 1 to surface failures earlier, without changing required scope | Low |
| U-002 | Variant 1 | R1-3: verifier tying the terminal surface to agent creation and prohibiting shell routes for ccsession sessions | Medium |
| U-003 | Variant 2 | Explicit preservation checklist (backward compatibility, executable identification, deadline, three-skill list) and separation of mocked checks from live refresh/UI reproduction | Medium |
| U-004 | Variant 3 | R3-1: other tests read core CLAUDE.md (one verified file, three unverified leads) | Low |
| U-005 | Variant 3 | R3-2: "no keyword parser needed", matching plan line 45 "reuse existing result fields without a new parser" | Medium |

## Shared Assumptions

| # | Assumption | Classification | Promoted | Evidence |
|---|------------|----------------|----------|----------|
| A-001 | Orca's normal `skills install` (no `--force`) can skip an edited or foreign guide and still exit 0, so the exit code alone cannot signal a skip | UNSTATED (no card states the exit-code semantics; Variants 1 and 3 build verifiers on it; Variant 2 does not address it) | Yes | `artifacts/orca-discovery.md` (skipped folders are warnings; only exit 1 is failure); plan line 24 |
| A-002 | With all three SKILL.md files present before the call, the post-call presence check (`install_user_setup.py:257-258`) is trivially satisfied, so a success message after a forced run cannot prove a refresh | UNSTATED (no card names the mechanism; Variant 3 implies it via "no refresh-success claim") | Yes | `install_user_setup.py:236-237`, `:257-263`; plan line 24 |
| A-003 | The verdict concerns the plan only; no card claims runtime causation, test execution or installation | STATED (all three `limitations`; plan line 19) | No | Cards' limitations; plan line 19 |
| A-004 | Adding an optional `force` argument keeps existing callers compatible | STATED (Variant 2 and Variant 3 self-audits; plan line 45 "backward-compatible") | No | Plan line 45; `install_user_setup.py:441` |

## Summary
- Total structural differences: 2
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 5
- Shared assumptions: 4 (UNSTATED promoted: A-001, A-002)
- Scored diff points for convergence: S (2) + C (5) + X (2) + promoted A (2) = 11
- Highest-severity items: C-001, C-003, C-005, X-001, X-002, S-002, A-001, A-002 (all Medium; no High)
- Citation pathologies excluded from final citations: Variant 1 `install_user_setup.py:113-119` (actual helper is 230-263; 113-119 lies inside `install_rules`); Variant 3 brief-local "plan lines 81-82" (actual plan has 53 lines; the corresponding text is plan lines 45-51).
