# Adversarial Validation: Architecture vs Requirements — Diff Analysis

## Metadata
- Generated: 2026-03-19
- Mode: VALIDATION (Architecture=CLAIM, Requirements=AUTHORITY)
- Artifact A: `architecture-design.md` v1.0.0
- Artifact B: `deterministic-fidelity-gate-requirements.md` v1.0.0
- Axes analyzed: 6
- Total findings: 22
- Depth: deep
- Convergence target: 0.90
- Focus: fr-nfr-coverage, data-flow, convergence, remediation, module-gaps, migration

## Structural Differences

| # | Area | Architecture (A) | Requirements (B) | Severity |
|---|------|-----------------|-------------------|----------|
| S-001 | Status vocabulary | Uses ACTIVE/FIXED/FAILED/SKIPPED (4 statuses) | Specifies FIXED/SKIPPED/FAILED only (3 statuses) | Medium |
| S-002 | Severity rule count | 17 rules across 5 checkers | 15 rows in FR-3 table | Low |
| S-003 | Debate assignment | Semantic HIGHs=lightweight, Regression=full /sc:adversarial | Resolved Q#2: Regression=lightweight, Semantic=full | High |
| S-004 | Module change scope | Section 2.3 lists prompts.py as UNCHANGED | Phase 5 removes build_spec_fidelity_prompt from prompts.py | Medium |

## Content Differences

| # | Topic | Architecture Approach | Requirements Approach | Severity |
|---|-------|----------------------|----------------------|----------|
| C-001 | FR-2 table extraction | No dedicated table extraction field in SpecData; tables parsed from section content | "Extracts markdown tables by section (keyed by heading path)" as explicit AC | Medium |
| C-002 | FR-2 code block extraction | Only Python function signatures extracted from fenced blocks | "Extracts fenced code blocks with language annotation" (generic) | Medium |
| C-003 | Boundary between structural/semantic | Implicit per-dimension (~55-85% estimates) | "Checkers handle 55-85% structurally" — boundary undefined | Medium |
| C-004 | Monotonic progress | Detection only (triggers regression handling) | "Each run must have ≤ HIGHs than previous run" (enforcement) | Low |
| C-005 | Rollback scope | Per-file: all patches rolled back if any patch in that file fails | "Rollback is per-file (not all-or-nothing)" — file-level, not patch-level | Low |

## Contradictions

| # | Point of Conflict | Architecture Position | Requirements Position | Impact |
|---|-------------------|----------------------|----------------------|--------|
| X-001 | Debate variant assignment | Sec 4.3: semantic HIGHs → lightweight debate; Sec 4.5.1: regression → full /sc:adversarial | Resolved Q#2: regression = lighter-weight; full adversarial reserved for FR-4 semantic HIGH | High — opposite assignment of lightweight vs full debate |
| X-002 | prompts.py change status | Sec 2.3: prompts.py is UNCHANGED | Phase 5 item 12: Remove build_spec_fidelity_prompt from prompts.py | Medium — internal contradiction within architecture |
| X-003 | NFR-4 frozen claim | Sec 10: "Frozen dataclasses; no shared state" | SpecData has mutable dict fields despite frozen=True | Medium — misleading compliance claim |

## Unique Contributions (Architecture Only)

| # | Contribution | Value Assessment |
|---|-------------|-----------------|
| U-001 | CrossReference dataclass for bidirectional section linking | High — enables resolved Q#5 supplementary sections |
| U-002 | ThresholdExpression with operator/value/unit parsing | High — enables NFR numeric comparison |
| U-003 | ConvergenceResult dataclass with progress_log | Medium — good observability |
| U-004 | Confirmation threshold (≥2/3 agents) for regression findings | Medium — adds audit quality |

## Shared Assumptions

| # | Assumption | Classification | Impact |
|---|-----------|---------------|--------|
| A-001 | Roadmap files are valid markdown parseable by regex | UNSTATED | Medium — malformed markdown could crash parsers |
| A-002 | ClaudeProcess is available for semantic layer and debate | UNSTATED | High — no fallback if ClaudeProcess unavailable |
| A-003 | Git worktrees work in the deployment environment | UNSTATED | Medium — container/CI environments may not support worktrees |
| A-004 | Output directory is writable and has sufficient disk space | UNSTATED | Low — standard assumption |

## Summary
- Total structural differences: 4
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-003, X-001 (debate assignment contradiction)
