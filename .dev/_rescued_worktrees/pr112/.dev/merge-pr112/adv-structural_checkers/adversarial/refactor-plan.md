# Refactoring Plan: structural_checkers.py Merge Resolution

## Overview
- Base variant: V3 (proposed-resolution) = ours' code body + enriched comments
- Incorporated variants: V2 (theirs) — TASK-RF provenance only
- Change count: 3 (all comment-only)
- Overall risk: **Low** (zero executable-code change vs the converged port both branches produced)

## Planned Changes
(These are already applied in the `.resolved` file; documented here for transparency.)

### Change #1 — Hunk 1 (MD-canon comment)
- Source: V1 rich comment + V2 TASK-RF reference
- Target: `_canonicalize_requirement_id`, MD-family comment block
- Integration approach: keep V1 text, append `; see also TASK-RF-20260531-044100 design D2`
- Rationale: preserves arch-lint Rule 2 rationale (C-001 winner V3, 95%) + adds design-doc traceability
- Risk: Low (comment only)

### Change #2 — Hunk 2 (non-references anchor comment)
- Source: V1 PR#111 provenance + V2 TASK-RF reference
- Target: `_EXPLICIT_NON_REFS_ANCHOR_RE` comment
- Integration approach: `Ported from PR #111 (861047c2) design D3; see also TASK-RF-20260531-044100 design D3.`
- Rationale: C-002 winner V3 (95%); V2 advocate conceded its foreign-repo absolute path is rot
- Risk: Low

### Change #3 — Hunk 3 (D3 allowlist comment in check_signatures)
- Source: V1 PR#111 provenance + V2 TASK-RF reference
- Target: `check_signatures`, non_ref_allowlist comment
- Integration approach: `Ported from PR #111 (861047c2) design D3; see also TASK-RF-20260531-044100 design D3.`
- Rationale: C-003 winner V3 (90%); additive
- Risk: Low

## Changes NOT Being Made
- **U-001 rejected**: V2's `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md L665` absolute path. Rationale: targets a different repository; unresolvable in IronClaude-RoadmapRewrite; would be dead reference rot on day one. Unanimous reject (95%).
- **Local `import re` inside `_canonicalize_requirement_id` NOT removed**: redundant given module-level `import re`, but present identically in BOTH ours and theirs. Removing it is a cleanup that exceeds conflict-resolution scope and is not load-bearing. Left as-is.
- **C-004 duplicate-comment**: NOT introduced. By building from the clean OURS stage, the single "We also track source family" block is retained; the git-auto-merge duplicate is structurally avoided (no action needed).

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 #2 #3 | Low | comment text only | revert to V1 comment verbatim |
| Reject U-001 | Low | removes a dead path | n/a |

## Review Status
Auto-approved (non-interactive). Depth=quick.
