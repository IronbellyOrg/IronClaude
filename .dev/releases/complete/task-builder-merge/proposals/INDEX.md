# Phase 3 — Proposal Index

Inverse-direction (sc:tasklist → task-builder) merge proposals. Each row anchors to FINAL-REPORT §5/§7 mechanism (P1-P5 / R1-R5) plus two CB-3-classified per-check additions.

## Compare line (consumed by Phase 4 sc:adversarial)

--compare /config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-01-execution-context-header.md,/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-02-retry-monotonicity-guards.md,/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-03-dnsp-synthetic-finding.md,/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-04-gate-results-passthrough.md,/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-05-tier-history-advisory.md,/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-06-structural-gate-additions.md,/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/proposals/PR-07-adversarial-category-naming.md

## Proposal summary

| proposal_id | case | slug | source mechanism (FINAL-REPORT) | complexity_estimate | expected_quality_gain |
|---|---|---|---|---|---|
| PR-01 | D | execution-context-header | §7-R2 Task Execution Context Block | ~25 lines | medium |
| PR-02 | D | retry-monotonicity-guards | §7-R4 Dual-Mode Patch Recovery (monotonicity + regression detection) | ~25 lines | medium-high |
| PR-03 | B | dnsp-synthetic-finding | §7-R1 DNSP for Validation Agents (39/50 — only ADOPT proposal) | ~20 lines | high |
| PR-04 | B | gate-results-passthrough | §7-R3 Quality Gate Evidence Passthrough | ~15 lines | medium |
| PR-05 | D | tier-history-advisory | §7-R5 Tier Calibration Advisory (advisory-only resolves §6.2 F4) | ~30 lines | medium |
| PR-06 | D | structural-gate-additions | 17-point gate per-check classification (CB-3) | ~20 lines | medium |
| PR-07 | D | adversarial-category-naming | 5-axis adversarial taxonomy (CB-3 naming-only overlay) | ~15 lines | medium |

## Case-distribution

- CASE-A (task-builder explicit + sc:tasklist disagrees → adopt task-builder): 0
- CASE-B (task-builder silent + clean additive): 2 (PR-03, PR-04)
- CASE-C (both silent): 0
- CASE-D (partial coverage both sides, synthesis): 5 (PR-01, PR-02, PR-05, PR-06, PR-07)

CASE-A/D proposals (5) appear as rows in `../conflict-register.md`.

## Invariant coverage per proposal

| proposal | self-contained-item | evidence-bound-item | persistent .dev/tasks/ | zero-trust QA | parallel research |
|---|---|---|---|---|---|
| PR-01 | untouched | PROTECTED (central) | untouched | untouched | untouched |
| PR-02 | untouched | untouched | untouched | PROTECTED (central, strengthened) | untouched |
| PR-03 | untouched | upheld | upheld | reinforced | upheld |
| PR-04 | untouched | upheld | upheld | reinforced | untouched |
| PR-05 | untouched | PROTECTED (central) | upheld and extended | untouched | untouched |
| PR-06 | reinforced | untouched | untouched | PROTECTED (central, strengthened) | untouched |
| PR-07 | untouched | untouched | untouched | PROTECTED (central, sharpened) | untouched |

## Direction-inversion summary

Per FINAL-REPORT §6.3, 4/5 RF→SC ports were over-engineered when the implementation was ported wholesale rather than the intent. Applying the inverse lens to SC→TB:

- **Lowest over-engineering risk:** PR-03 (paradigm-neutral DNSP, the only original ADOPT), PR-04 (operationalises existing rf-qa-qualitative.md:794 rule), PR-07 (naming-only overlay).
- **Medium risk:** PR-01 (header-only summary), PR-02 (stop-conditions only), PR-06 (per-check CB-3 classification limits scope).
- **Highest risk:** PR-05 (introduces feedback-pattern infrastructure with no existing consumer data — explicitly flagged as Phase-2/future-work; advisory-only framing protects against hidden-input regression analog to §6.2 F4).

All 7 proposals avoid: blanket determinism imposition (would violate parallel-research), atomic-write enforcement (would violate persistent .dev/tasks/ artifact), full R-###→T<PP>.<TT>→D-#### matrix as hard requirement (would violate BUILD_REQUEST input contract), orchestrator-does-not-apply-patches re-architecture (would violate the skill-orchestrates / agent-builds split at SKILL.md:80-82).
