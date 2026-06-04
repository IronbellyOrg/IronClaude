# QA Report — Phase 2 Structural Gate (rf-qa, adversarial)

**Task:** TASK-RF-20260525-194356 · **Phase:** 2 (CLI/command/skill/installer) · **Date:** 2026-06-03
**Agent:** rf-qa (sonnet), ADVERSARIAL STANCE, fix_authorization: true
**Report persisted by:** task executor (rf-qa returned findings inline; harness blocked its own .md write).

## VERDICT: PASS (after 1 in-place fix)

- Issues found: 1 · fixed: 1 · remaining: 0
- 19/19 acceptance criteria verified with file:line + runtime evidence.

## Issue & fix

| # | Sev | Location | Issue | Fix |
|---|-----|----------|-------|-----|
| 1 | IMPORTANT | `src/superclaude/cli/init_lite.py` `--context-optimized` option | CLI accepted `superclaude init-lite` WITHOUT the mandatory `--context-optimized` flag, drifting from the command contract (flags table marks it Required: Yes). | Added `required=True` to the Click option. Re-verified: bare `init-lite` exits 2; `init-lite --context-optimized --dry-run` exits 0. |

## Verified criteria (highlights, all PASS)

- `discover_surfaces` returns ONLY the 6 allowed surface classes; excludes non-SKILL.md skill files and non-.md agent files (`init_lite.py:80-108`).
- `estimate_tokens` = `(b+3)//4` with zero guard; runtime `5→2`, `4001→1001` (`:45-49`).
- `classify_weight` boundaries correct: `999→low`, `1000→medium`, `4000→medium`, `4001→high` (`:52-61`).
- `--dry-run` returns before any write; `.dev/superclaude/` not created (`:314-318`, runtime `dev_exists False`).
- Default writes only the marked report; `--scaffold` creates exactly the 2 allowed files (`:238-252,320-326`).
- `_is_protected_context_path` + `_write_report` refuse writes to `CLAUDE.md`/`.mcp.json`/`.claude/**` under all flags incl. `--force`; runtime force attempts exited 1 and preserved bytes (`:194-221`).
- `--force` markerless overwrite gated on `_is_init_lite_owned` (under `.dev/superclaude/`); markerless-outside refused (`:111-122,223-232`).
- `main.py` additive registration intact; `init-lite --help` exit 0, all 6 flags, in top-level help (`main.py:428-430`).
- `install_skills.py` git diff = comments/docstrings only; `_has_corresponding_command` still strips only `sc-`; `sc-roadmap/reflect/task/init-lite-protocol` all return False (standalone); bare `sc-roadmap` returns True.
- 17 `sc-*-protocol` skill dirs present incl. `sc-init-lite-protocol`.
- `init-lite.md` = thin dispatcher, mandatory `Skill sc:init-lite-protocol` activation, forbids command-only execution, 6 flags.
- `SKILL.md` frontmatter complete; `allowed-tools` excludes `Edit`; "invoked only by /sc:init-lite".
- No TODO/FIXME/TBD/placeholder in any Phase 2 file; `ruff check` → All checks passed.
- `git status` shows only `src/` changes; no `.claude/` paths.

## Recommendation
Proceed to Phase 3. Add a Phase-3 test locking the fixed required-flag behavior (bare `init-lite` → exit 2; `--context-optimized --dry-run` → exit 0, no writes).
