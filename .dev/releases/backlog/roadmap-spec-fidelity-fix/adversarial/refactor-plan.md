# Refactor Plan — Merging Top 3 (S2 + S1 + S5) into a Unified Fix

## Overview
- Base variant: **S2** (highest combined score, addresses load-bearing root cause)
- Incorporated variants: **S1** (regex sanitization), **S5** (context-aware NFR severity)
- Excluded variants: S3, S4, S6 (defensive/cosmetic; defer)
- Change count: 3 sequential changes (S1 → S2 → S5)
- Overall risk: **Medium** (touches Finding dataclass, parser, NFR checker)

## Planned Changes

### Change 1 (from S1): Sanitize file-path extraction
- **Source variant**: S1
- **Target location**: `src/superclaude/cli/roadmap/spec_parser.py` (`extract_file_paths_from_tables` ~line 407; `extract_file_paths` ~line 397)
- **Integration approach**: Add `_looks_like_file_path(candidate, cell, start)` helper applying 5 structural-token reject rules; wire as final filter in both extractors.
- **Rationale**: Eliminates 4 of 10 phantom HIGHs at source. **Must merge first** — without this, Change 2 will route phantom findings to the roadmap, creating real defects from imaginary ones.
- **Risk level**: Low (additive helper, surgical filter)

### Change 2 (from S2): Route findings + actionable fix_guidance
- **Source variant**: S2
- **Target location**:
  - `src/superclaude/cli/roadmap/structural_checkers.py` (extend `_make_finding` signature, add `MISMATCH_FILE_ROUTING` table, thread `roadmap_path` into all checkers)
  - `src/superclaude/cli/roadmap/semantic_layer.py:514` (parallel `Finding()` call)
  - `src/superclaude/cli/roadmap/remediate_prompts.py` (templated `fix_guidance` per mismatch_type; additive-edit Constraint line)
  - `src/superclaude/cli/roadmap/models.py` (add `deviation_class` field for AMBIGUOUS routing)
- **Integration approach**: Foundational schema change first, then per-checker threading, then prompt template.
- **Rationale**: Without targets + actionable guidance, agents will keep rewriting whole sections regardless of any other fix.
- **Risk level**: Medium (Finding contract widened; multi-file blast radius; existing tests must update)

### Change 3 (from S5): Context-aware NFR severity
- **Source variant**: S5
- **Target location**: `src/superclaude/cli/roadmap/structural_checkers.py` (`check_nfrs` ~line 518; `_section_text` ~line 159 — DO NOT call it for the NFR loops anymore; new `_classify_nfr_severity` helper)
- **Integration approach**: Replace `spec_nfr_text = _section_text(spec_sections)` blob with per-section iteration that preserves `heading_path`; emit MEDIUM unless heading contains strong-NFR tokens (`security|critical|must|shall|p0|nfr-|compliance|encryption|audit`); optional YAML allowlist with `PRE_APPROVED` deviation_class.
- **Rationale**: 4 of the remaining 6 HIGHs (after Change 1) are NFR softs. The gate is HIGH-only — demoting them to MEDIUM removes them from convergence blockers without hiding them from the report.
- **Risk level**: Medium (per-section refactor changes finding determinism; must sort by `(heading_path, term)` for stable IDs)

## Changes NOT Being Made (rejected alternatives)

### S3 — Tiered diff-size relaxation
- **Rejected because**: Addresses the 71.3% rejection *symptom*, not the cause. Once Change 2 routes findings to the right file, the diff stays small. S3 stays in backlog as defensive future work.
- **Debate evidence**: X-001 resolved in favor of S2's "symptom not cause" thesis at 88% confidence.

### S4 — Budget overhaul
- **Rejected because**: S4's own refactor falsified the budget-too-small premise. `available=35` = `61 - 46 + 20` (post-credit) is correct. The observability improvements (dual snapshots, refund-on-rollback) are valuable but not failure-blocking; defer to follow-up.
- **Debate evidence**: X-002 unanimous (100% confidence).

### S6 — MANUAL_TRIAGE halt
- **Rejected because**: Safety net that's not needed if S1+S2+S5 converge. Adds new finding status + downstream consumer updates + CLI flag — non-trivial blast radius for a defensive feature. Reconsider if the next CLI re-run still fails.
- **Debate evidence**: C-006 won by S6 at 85% confidence but only conditionally on convergence still failing.

## Risk Summary

| Change | Risk | Impact if it breaks | Rollback |
|--------|------|---------------------|----------|
| 1 (S1) | Low | Legit paths get filtered (e.g., `scripts/build`) — false negatives in manifest scan | Revert helper; ~30 LOC |
| 2 (S2) | Medium | Finding emission breaks if checkers miss the new parameter; remediation prompts misformat | Field has `default_factory=list`; backward compatible at dataclass level. Prompt templates have fallback to current generic guidance. |
| 3 (S5) | Medium | Stable IDs change → existing registries see all findings as "new" | Add registry-migration shim: if same dimension+location+mismatch_type with old severity HIGH appears as MEDIUM, treat as continuation. |

## Review Status
Auto-approved (non-interactive mode).
