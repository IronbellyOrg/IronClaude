# PR #197 Remediation — Validation Verdict

**Worktree:** `.dev/worktrees/pr197-remediation` (branch `feat/rf-harness-sync`, base `a3f3f0cb`)
**Scope:** 11 tracked files modified + 1 new test = 12 in-scope files. No out-of-scope changes.

| Item | Applied / Halted | Acceptance Check | Result |
|------|------------------|------------------|--------|
| **R1** (HIGH) | Applied | `mcp__tavily__tavily_(search\|extract)` in agents/ → 0 matches; hyphen form in all 8; `deep-research.md` untouched | ✅ PASS |
| **R2a** (HIGH) | Applied | 0 bare "capability are confirmed"; 3 disclosure sites; `#6 --cli` + Rule 20 disclosed | ✅ PASS |
| **R2b / HD-1** (HIGH) | **HALTED (PENDING)** | PENDING record written; `--cli` default NOT flipped; O4 floors NOT edited | ⏸️ PENDING by design |
| **R3** (MEDIUM) | Applied | new `test_inline_directive.py` (3 tests) pass; EV-1 comment at runner.py:371 | ✅ PASS |
| **R3+ (new finding)** | Applied | pre-existing `test_no_nesting_guard` failure fixed (banned token `subagent`→`subagent_type`+`Agent(`) | ✅ PASS |
| **R4** (MEDIUM) | Applied | Mode Bifurcation Table + key-presence rule + checklist ref present | ✅ PASS |
| **R5** (LOW) | Applied | 0 dangling `§4.2 clause 4`; 2 spec_path skill-vs-CLI qualifiers | ✅ PASS |

## Gates
- `make sync-dev` + `make verify-sync`: ✅ clean (src/ ↔ .claude/ in sync)
- `ruff format --check` (3 in-scope Python files): ✅ already formatted
- `uv run pytest tests/cli/reflect/`: ✅ 81 passed, 1 xpassed, 0 failed

## HD-1 preservation
HD-1 remains **PENDING** — the `--cli` default was NOT flipped and O4 depth floors were NOT
edited. Record: `phase-outputs/plans/HD-1-default-mode-decision.md`. This is the correct
terminal state and does NOT block the mechanical work.

## Out-of-scope flag (for maintainer)
Full-tree `ruff format --check src/ tests/` reports 106 files "would reformat" — a likely ruff
version mismatch (worktree .venv vs CI). Reverted, NOT fixed here. Verify CI's pinned ruff.

## OVERALL (mechanical R1/R2a/R3/R4/R5): ✅ PASS  |  HD-1: ⏸️ PENDING (by design)
