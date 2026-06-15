# Refactoring Plan

## Overview

- **Base variant**: Solution 2 (Prompt-side path pinning)
- **Incorporated variants**: Solution 1 (backstop recovery), Solution 3 (truncation guard + capture/cwd as deferred follow-ups)
- **Planned changes**: 6 incorporated + 3 explicit deferrals + 1 drop
- **Overall risk**: Low–Medium (hotfix scope is prompt edits + one hardened function; the high-risk items are deferred)
- **Review status**: Auto-approved (non-interactive)

## Planned Changes

### Change #1 — Base: `_artifact_path_for_step` helper + path pinning (Solution 2 §1-2)
- **Source**: Base, Solution 2 §1-2
- **Target**: `prompts.py` (new helper ~line 53; edits to the 4 un-pinned builders)
- **Integration**: replace
- **Rationale**: removes the prompt ambiguity that is the REPORT root cause; debate C-001/C-003 winner (82%/78%)
- **Risk**: Low (additive prompt text + read-only mirror helper)

### Change #2 — Backstop: hardened `_resolve_step_content` (Solution 1 §1-3)
- **Source**: Solution 1 §1 (pattern map), §3 (pattern-aware search)
- **Target**: `executor.py` `_resolve_step_content` (~266-365)
- **Integration**: replace exact-name rglob with pattern-aware search; keep `_STEP_ARTIFACT_FILES` + special cases (`build-task-file`, `assembly`) untouched
- **Rationale**: defense-in-depth for agent non-compliance (X-003); REPORT 2+1 recommendation
- **Risk**: Medium (widens search — see Change #4 constraints)

### Change #3 — Deterministic tiebreak `_pick_best_candidate` (Solution 1 §4, U-001)
- **Source**: Solution 1 §4
- **Target**: `executor.py` (new helper)
- **Integration**: replace current `len(content) > len(best_content)` "largest wins" (executor.py:360)
- **Rationale**: **INV-006** — current source picks largest, not freshest; a stale longer file from a prior run silently wins. Tiebreak order: in-preferred-root (task_dir) → freshness (mtime) → content length → path specificity
- **Risk**: Low (deterministic, unit-testable)

### Change #4 — Bounded WHERE search roots + symlink containment (Solution 1 §2, U-002, INV-005)
- **Source**: Solution 1 §2 + traversal guard
- **Target**: `executor.py` `_resolve_step_content`
- **Integration**: add `parsed-request.json` WHERE dirs as roots, but **bounded** — reject dirs outside repo root via `realpath` containment (not just `relative_to`), reject symlinks, preserve the existing anti-widening intent at executor.py:290-292
- **Rationale**: targets the observed `.dev/specs/` miss; INV-005 warns naive widening reverses a hard-won narrowing against sibling-dir stale matches
- **Risk**: Medium (mitigated by containment + tiebreak)

### Change #5 — Truncation-detection semantic check (Solution 3, U-005)
- **Source**: Solution 3 §Gate Criteria Adjustments
- **Target**: `gates.py` (optional semantic check)
- **Integration**: append (`[TRUNCATED`, trailing `...`)
- **Rationale**: cheap guard against silently-incomplete content; harmless to existing gates
- **Risk**: Low

### Change #6 — Preserve `output_text`↔`gate_content` split (INV-010)
- **Source**: invariant probe
- **Target**: `executor.py` (assertion / comment guarding the existing split at ~609/613/618)
- **Rationale**: INV-010 — `_determine_status` sentinel detection reads NDJSON `output_text`; the gate reads disk `gate_content`. The merge must NOT collapse these or sentinel detection silently loses its input
- **Risk**: Low (documents/locks an existing-correct invariant)

## Changes NOT Being Made (considered and rejected)

- **Solution 3 result-event capture as the hotfix mechanism (C-002)**: rejected. Grep-confirmed unimplemented (`_extract_text_from_stream_json` has no `result` branch, INV-008); core contract unverified; HIGH blast radius across 15 steps; token-truncation risk for the 800-line assembly PRD. **Deferred** behind `capture_mode` (default legacy) pending CLI verification.
- **Solution 3 blanket cwd=task_dir (U-004/C-004)**: rejected for the hotfix. **INV-011 (HIGH)** — task_dir is a `.dev/tasks/` leaf; cwd there breaks scope-discovery/investigation codebase reads → degraded scope-discovery → thin research-notes → *causes* the STRICT gate to fail. **Deferred** until paired with an explicit absolute repo-root injection for input reads. Item 1's absolute output-path pinning already delivers the contamination benefit without this risk (INV-003).
- **Frontmatter prompt-mandate (naive consensus item 5)**: dropped. **INV-001** — the research-notes prompt already emits `[Date,Scenario,Tier]` (prompts.py:224-228), and the PRD `_evaluate_gate` never reads `required_frontmatter_fields` (dead constraint). The real load-bearing STRICT criteria are min_lines + the 2 semantic-section checks.
- **Solution 1 standalone (no pinning)**: rejected. Leaves contamination live (REPORT R2) and institutionalizes reading the agent's pollution out of `.dev/specs/`.

## Risk Summary

| Change | Risk | Rollback |
|--------|------|----------|
| #1 path pinning | Low | revert prompt strings |
| #2 backstop search | Medium | revert `_resolve_step_content` |
| #3 tiebreak | Low | revert `_pick_best_candidate` |
| #4 bounded WHERE | Medium | drop WHERE roots, keep task_dir+parent |
| #5 truncation check | Low | remove semantic check |
| #6 split guard | Low | comment only |

## Sufficiency Note (INV-002, scoped)

The merged fix guarantees the gate **evaluates the agent's real document** instead of NDJSON commentary. It does **not** guarantee the agent *authored* ≥100 lines + all 7 sections + detailed phases — that is correctly the STRICT gate's decision (a genuinely thin doc *should* HALT). Reproduction evidence (REPORT: real 197-line doc) indicates content was not the problem in the observed failure. Content-completeness is out of scope for a capture fix; the existing semantic checks enforce it.
