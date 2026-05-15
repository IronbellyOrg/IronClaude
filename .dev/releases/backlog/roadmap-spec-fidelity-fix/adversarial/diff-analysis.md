# Diff Analysis — 6 Spec-Fidelity Fix Candidates

## Metadata
- Generated: 2026-05-15T14:07:00Z
- Variants compared: 6 (S1–S6, all post-adversarial-refactor)
- Total differences found: 19
- Categories: structural (3), content (8), contradictions (2), unique (4), shared assumptions (2)
- Source-of-truth failure: `.dev/releases/current/task-builder-merge/roadmap/spec-fidelity.md`
  - 10 ACTIVE HIGHs after 3 convergence runs
  - All findings have `files_affected=[]`
  - Patches against `TDD_TASK_BUILDER_CONVERGENCE.md` rejected at 71.3% / 38.1%
  - HIGH composition: 4 parser-noise, 2 legit manifest gaps, 4 NFR soft findings

## Structural Differences

| # | Area | Variants taking each position | Severity |
|---|------|-------------------------------|----------|
| S-001 | Primary target file | S1 → `spec_parser.py`; S2 → `structural_checkers.py` + `remediate_prompts.py`; S3 → `convergence.py` + `executor.py`; S4 → `convergence.py` + `remediate_executor.py`; S5 → `structural_checkers.py` (check_nfrs); S6 → `convergence.py` + `models.py` | Low |
| S-002 | Adds CLI flags | S3 (`--convergence-tier-relax`, `--convergence-deletion-guard`), S6 (`--triage-allow dim:class`); S1/S2/S5/S4 → none | Medium |
| S-003 | Changes Finding dataclass / status enum | S2 (extends `_make_finding` to accept `files_affected`); S6 (adds `MANUAL_TRIAGE` status); S1/S3/S4/S5 → no schema change | Medium |

## Content Differences

| # | Topic | S1 | S2 | S3 | S4 | S5 | S6 |
|---|-------|----|----|----|----|----|----|
| C-001 | Targets parser-noise HIGHs (4/10) | YES (load-bearing) | indirect | no | no | no | indirect (skip) |
| C-002 | Targets NFR-soft HIGHs (4/10) | no | indirect | no | no | YES (load-bearing) | indirect (skip) |
| C-003 | Targets legit manifest gaps (2/10) | no (correctly preserves) | YES (gives them a remediation target) | no | no | no | indirect (skip) |
| C-004 | Fixes agent-edits-wrong-file (71.3% root cause) | partial (removes phantoms agents tried to fix) | YES (routes to roadmap.md) | partial (relaxes guard) | no | no | no |
| C-005 | Adds actionable `fix_guidance` to agent prompts | no | YES (per-mismatch templates) | no | no | no | no |
| C-006 | Adds escape hatch on irrecoverable failure | no | no | no | no | no | YES (MANUAL_TRIAGE halt) |
| C-007 | Improves diagnostics / observability | no | no | YES (telemetry on regen policy) | YES (dual snapshots) | no | YES (runbook output) |
| C-008 | Changes convergence budget math | no | no | no | YES (refund-on-rollback, constant rename) | no | no |

## Contradictions

| # | Point of conflict | Position A | Position B | Impact |
|---|-------------------|-----------|-----------|--------|
| X-001 | Whether 30% diff threshold is the root cause | S3: YES — relaxing it unblocks Run 2/3 | S2/S1: NO — agents only hit 30% because they edit the wrong file; route correctly and the threshold is fine | High — drives whether to ship S3 |
| X-002 | Whether `STD_CONVERGENCE_BUDGET=46` is too small | S4 (v1): YES, raise to 100 | S4 (refactored after debate): NO, math is correct — `available=35` is post-credit, budget is not the binding constraint | High — falsified by S4's own debate |

## Unique Contributions

| # | Source | Contribution | Value |
|---|--------|--------------|-------|
| U-001 | S2 | Per-mismatch `fix_guidance` templates that tell the agent *what to edit* | High — without this, even correct routing produces wholesale rewrites |
| U-002 | S5 | Per-section iteration in `check_nfrs` preserving `heading_path` for context-aware severity | High — currently dropped by `_section_text` join |
| U-003 | S3 | Deletion-attack defence (`is_likely_deletion_fix` heading/anchor count check) | Medium — relevant only after relaxing threshold |
| U-004 | S6 | Default-deny allowlist + proof-of-life check (`remediated_this_run > 0`) preventing skip-everything attack | Medium — closes the obvious workaround abuse path |

## Shared Assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|-----------|------------------|--------|--------|
| A-001 | The remediation agent will not improve without better prompts | All solutions implicitly assume the agent's behavior is fixed and the system around it must adapt | Medium — could be addressed by improving agent reasoning but that's out of scope | UNSTATED |
| A-002 | The spec (TDD) is immutable input; only the roadmap is editable | S2 makes this explicit; S1/S3/S4/S5/S6 implicitly assume the same | High — load-bearing for routing | UNSTATED |

## Summary

- Total structural differences: 3
- Total content differences: 8
- Total contradictions: 2 (one self-falsified during debate)
- Total unique contributions: 4
- Shared assumptions surfaced: 2 (both UNSTATED, both promoted)
- Highest-severity items: X-001, X-002, U-001, U-002, A-002
