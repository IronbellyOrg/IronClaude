# Refactoring Plan

## Overview
- Base variant: Variant 2 (variant-2-original.md, fix-2)
- Incorporated variants: Variant 1 (fix-1), Variant 3 (fix-3)
- Planned changes: 7
- Rejected changes: 3
- Overall risk: Low (text proposal; no code executed)
- Review: auto-approved 2026-11-08T02:16Z (non-interactive)

## Planned Changes

### Change 1 — Closing command: `--all` inside guards (replace list-and-handle)
- Source: Variant 1 "Proposed change" step 1; Variant 3 bullet
- Target: base "Proposed change" step 1 sentence
- Approach: replace
- New sentence (both installed copies): "A `worktree create` without `--agent` also opens a plain first terminal. If you will work in that new checkout from your current session, close it right after the create with `orca terminal close --worktree path:<path> --all`, only when you created it with no setup script (`--setup skip` or none configured) and have started nothing in it; never run this on a worktree you did not just create. To hand work to a new Claude session, use `worktree create --agent` instead of a bare create; `/sc:issue` and supervised workers keep their own launch steps."
- Rationale: debate C-002 / X-001 (2/3, 70%); one command; ownership by stored worktree id (A-003 ACCEPT, worktree-pty-collection.ts:14-30). V2 dissent recorded in the merged output's Risks.
- Risk: Medium (modifies the base's core mechanism)

### Change 2 — Keep and tighten guards
- Source: base (V2) guards; V3 "before anything is started there"
- Target: same sentence (folded into Change 1 wording)
- Approach: restructure
- Rationale: C-003 unanimous (90%); X-004 unanimous (95%)
- Risk: Low

### Change 3 — Hand-off routing and exemptions
- Source: Variant 1 (U-002), Variant 3 (U-007)
- Target: same sentence (folded into Change 1 wording) and the project bullet
- Approach: insert
- Rationale: C-004 (2/3, 75%); core/CLAUDE.md:49; D2/FO-18; WORKER-CONTRACT.md:62
- Risk: Low

### Change 4 — Delivery: reinstall
- Source: Variant 1 step 3
- Target: base step 3 (after `make sync-dev`, `make verify-sync`)
- Approach: append: "After the change is merged (or with an editable install), run `superclaude update`; plain `superclaude install` keeps the existing ~/.claude/CLAUDE.md (install_core.py:70-72)."
- Rationale: C-005 unanimous (90%); N12 (installed copy has 0 matches)
- Risk: Low

### Change 5 — Project rule placement
- Source: Variant 3 (U-006)
- Target: base step 2 (project bullet)
- Approach: replace: one bullet after CLAUDE.md:310 with the same command and guards (short form), and one comment line in the example block at :318-324 showing the close after the create.
- Rationale: C-001 unanimous, X-002 unanimous; agents copy the example (V3 strength 1)
- Risk: Low

### Change 6 — Tests
- Source: Variant 1 test; Variant 3 test; base test run list
- Target: base "Test plan"
- Approach: replace: in tests/core/test_orca_session_launch_guidance.py add pinned phrases "`orca terminal close --worktree`" and "worktree you did not just create" for both copies (12 existing phrases unchanged); add a small test asserting the project CLAUDE.md worktree section contains `orca terminal close --worktree`; drop the base's `"--all" not in section` assertion (X-003). Run `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/skills/test_issue_orca_worktree.py -v` (last file unchanged and passing).
- Rationale: C-006 (2/3, 75%); X-003 unanimous (100%)
- Risk: Low

### Change 7 — Document A-001 and residual risks
- Source: all advocates (A-001 QUALIFY, A-002 QUALIFY)
- Target: base "Risks"
- Approach: append: (a) opening the worktree in the Orca UI re-seeds a shell (worktree-activation.ts:275) — user-driven, acceptable; (b) default tabs configured for a repo start in the background and would also be closed by `--all` (startup.ts:187-201) — not covered by the setup-script guard; (c) compliance is unproven (A-002); (d) V2 dissent: a single-handle close bounds damage if the guards are misjudged.
- Rationale: A-001/A-002 unanimous QUALIFY; X-004
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|---|---|---|
| C-001 | V1: no project CLAUDE.md change | Unanimous for core + project (C-001, X-002) |
| C-001 | V3: project only | Misses Coder/IronOrca creates (N12); unanimous against |
| C-006 | V2: `"--all" not in section` | Contradicts merged text (X-003) |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Medium | Wrong guard judgment could close a default tab | revert the sentence |
| 2-7 | Low | Text and tests | `git revert` |

## Review Status
- Approval: auto-approved
- Timestamp: 2026-11-08T02:16Z
