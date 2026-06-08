# QA Report — Phase 3 Structural Gate (rf-qa, adversarial)

**Task:** TASK-RF-20260525-194356 · **Phase:** 3 (test coverage) · **Date:** 2026-06-03
**Agent:** rf-qa (sonnet), ADVERSARIAL STANCE, fix_authorization: true · **Persisted by:** task executor (rf-qa returned inline).

## VERDICT: PASS (after 1 fix cycle)

- Cycle 1: **FAIL** — 1 CRITICAL. rf-qa strengthened the discovery fixture with non-surfaces and exposed a real implementation bug: `discover_surfaces()` used `commands_dir.rglob("*")`, pulling in non-markdown files (`foo.txt`) and any file under `.claude/commands/**`.
- Resolution (executor contract decision): **command context surfaces are markdown** — `discover_surfaces` now globs `.claude/commands/**/*.md`, consistent with the existing `agents=*.md` and `skills=SKILL.md` filters and faithful to `.claude/commands/**` filtered to the context format. `init_lite.py:93-98` + docstring updated; discovery test updated to expect `.claude/commands/README.md` included (markdown) and `.claude/commands/sc/foo.txt` excluded.
- Cycle 2: **PASS** — 0 issues remaining; `62 passed in 0.29s`; no skipped tests.

## Resolved discovery contract (verified by direct CliRunner probe)

| Path | Discovered? |
|------|-------------|
| `.claude/commands/sc/foo.md` | ✅ included (markdown) |
| `.claude/commands/README.md` | ✅ included (markdown under commands) |
| `.claude/commands/sc/foo.txt` | ❌ excluded (non-markdown) |
| `.claude/skills/foo/SKILL.md` | ✅ included |
| `.claude/skills/foo/refs.md` | ❌ excluded (only SKILL.md) |
| `.claude/agents/foo.md` | ✅ included |
| `.claude/agents/foo.txt` | ❌ excluded (only *.md) |

## Verified criteria (17/17 PASS, highlights)

- Token estimate `ceil(bytes/4)` incl 0/non-multiples; thresholds incl exact 1000→medium, 4000→medium, 4001→high.
- Dry-run writes nothing incl no `.dev/superclaude/`; default writes marked report + no scaffold; scaffold exactly 2 files.
- `CLAUDE.md` byte preservation across dry-run/default/scaffold/force (parametrized); idempotency; help lists all 6 flags.
- No `.claude/` writes (absent + present cases); `--force` refuses markerless-outside AND all 6 protected context inputs (parametrized).
- Registration: `init-lite` in frozen roster; top-level help + flag help tests.
- F2 installer guard real & non-vacuous: protocol skills not command-backed; bare `sc-roadmap` maps; zero `sc-*-protocol` swept; end-to-end install keeps them standalone; would FAIL against the over-broad `-protocol`-stripping fix (rf-qa confirmed via scratch simulation — 17 skills would be swept).
- No skipped/placeholder/tautological tests.

## Issues remaining: 0
