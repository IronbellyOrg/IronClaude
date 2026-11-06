# Diff Analysis: spec Comparison

## Metadata

- Generated: 2026-11-05T19:58:00Z
- Variants compared: 2 (variant-1-opus-scribe, variant-2-sonnet-analyzer)
- Total differences found: 16 diff points (structural 3, content 8, contradictions 2) plus unique contributions 8 and shared assumptions 3
- Categories: structural (3), content (8), contradictions (2), unique (8), shared assumptions (3)
- Taxonomy tags (L1 surface, L2 structural, L3 state mechanics) are given per diff point; each level has at least one point.

## Structural Differences

| # | Area | Variant 1 (opus scribe) | Variant 2 (sonnet analyzer) | Severity | Level |
|---|---|---|---|---|---|
| S-001 | Section order | Purpose and sources, pattern, requirements, examples, decisions table, risks | Problem and root cause, pattern, requirements grouped under Retries / Nested / Child worktrees, examples, risks | Low | L2 |
| S-002 | Open-question answers | A table of four decisions with reasons | One paragraph inside the pattern section | Low | L1 |
| S-003 | Requirement grouping | Flat list FR-001 to FR-011 | FR-001 to FR-016 in topic sections | Low | L2 |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity | Level |
|---|---|---|---|---|---|
| C-001 | Directory shape and root | `.dev/orca/<runStamp>-<runSlug>/<command>-<subject>-<attempt>/` (new root, one folder per run) | `.dev/<command>/<subject>-<n>/` (the contract's worked example, generalized) | High | L2 |
| C-002 | Date in the name | Once, on the run folder (UTC stamp) | None; git history and the contract carry time | Medium | L1 |
| C-003 | Names across child worktrees and merge-back | Same relative part in every worktree (FR-010); merge-back not discussed | Relative path unique across worktrees (FR-002); merge-back of child report folders stated as undecided (FR-016) | Medium | L2 |
| C-004 | Simultaneous dispatch and parallel siblings | Names assigned from the coordinator's placement map (FR-003); sibling subjects shown only in examples | Same mechanism (FR-003) plus an explicit rule that fan-out siblings differ in subject, not in attempt number (FR-004) | Medium | L3 |
| C-005 | Retry circuit breaker | Only the attempt number changes between retries, so the coordinator can strip it and compare (FR-005) | The path appears exactly once on the command line so one token is stripped (FR-011) | Low | L3 |
| C-006 | Subject style | camelCase, at most 16 characters, `A-Za-z0-9-` (FR-007) | lowercase kebab, at most 24 characters, `[a-z0-9-]`; warns about trailing digits (risk 3) | Medium | L1 |
| C-007 | Fixed per-check names in the P1 live plan | `-1` suffix from the first run (FR-011) | Same advice, filed as a risk and left to a plan edit (risk 1) | Low | L1 |
| C-008 | Reuse of a directory | Never written again after a Task ends (FR-004) | Same, with one stated exception: a re-invocation inside the same Task after `ask` keeps the directory (FR-013) | Medium | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Level |
|---|---|---|---|---|---|
| X-001 | Choice of root against folders other tools already own | Introduces `.dev/orca/` and says it is new and unverified (R4) | Per-command roots `.dev/<command>/`; `.dev/README.md:63` (read in this run's grep output) names `.dev/implement/` as the home of implement ledgers and `.dev/workflow/<slug>/` as the legacy workflow plan path, and `src/superclaude/commands/reflect.md:101` uses `.dev/reflect/`, so commands `implement`, `workflow` and `reflect` would put report folders next to, or inside, those tool-owned folders. Variant 2 does not mention this. | High | L2 |
| X-002 | "Never written again" against the WC-3 re-run | FR-004 reads as an absolute rule for the directory | FR-013 states the one case where the same directory is rewritten (same Task, after an answer) | Low | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | Run-level folder with a coordinator-chosen stamp groups one run and separates runs without counter recovery | High |
| U-002 | 1 | One audit line per name in the run notes, with an example line (FR-009) | Medium |
| U-003 | 1 | Decisions table answering each open question of the seed brief | Medium |
| U-004 | 2 | Root-cause framing: collisions are caught late by the command's refusal, so the coordinator must be the only source of the name | Medium |
| U-005 | 2 | Explicit WC-3 exception (directory reused inside one Task) | High |
| U-006 | 2 | Brief-guard refusals consume attempts, 3 attempts maximum (FR-012) | Medium |
| U-007 | 2 | Trailing digits in a subject make the attempt number ambiguous (risk 3) | Medium |
| U-008 | 2 | Merge-back of child report folders is undecided (FR-016) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status | Level |
|---|---|---|---|---|---|---|
| A-001 | The coordinator's placement map (and attempt counter) is the only uniqueness mechanism and stays correct for the whole run | Both: names come from the coordinator before dispatch | STATED (V1 R1 and R2, V2 risk 2) | High | Not promoted | L3 |
| A-002 | The chosen root does not clash with folders other tools already write under `.dev/` (`implement`, `workflow`, `reflect`, `brainstorms`, `tasks`) | Both: reports go under `.dev/` (WC-11) | UNSTATED (V1 R4 only says "UNVERIFIED"; V2 silent) | High | Promoted [SHARED-ASSUMPTION] | L2 |
| A-003 | After a coordinator loses its notes, the highest attempt number can be recovered by listing directories | V2 FR-005 and risk 2; V1 FR-006 relies on a contract file existing | CONTRADICTED by V1 R1: a guard-refused attempt runs nothing and leaves no directory | Medium | Promoted [SHARED-ASSUMPTION] | L3 |

## Summary

- Total structural differences: 3
- Total content differences: 8
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 1, STATED: 1, CONTRADICTED: 1)
- Total debate diff points (S + C + X + A): 16
- Taxonomy coverage: L1 = S-002, C-002, C-006, C-007; L2 = S-001, S-003, C-001, C-003, X-001, A-002; L3 = C-004, C-005, C-008, X-002, A-001, A-003
- Highest-severity items: C-001, X-001, A-001, A-002
