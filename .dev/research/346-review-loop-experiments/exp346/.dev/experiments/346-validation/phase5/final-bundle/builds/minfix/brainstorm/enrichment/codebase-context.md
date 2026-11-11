# Codebase context (Wave 2A, quality_tier: fallback_1)

Source: native Grep/Glob/Read in worktree bs346-minfix (origin/master 0423fe5f). `mcp__auggie__codebase-retrieval` is not available in this session; codegraph was not used (the hits below are direct file reads).

## Loop contract the variant builds on
- `src/superclaude/commands/spec-panel.md:256-264` `## Review Loop`, 7 one-line bullets: Mode, Grading, Verdict, Cap, Re-review output, Reviser contract (bullet 6, line 263), Precedence. Usage line 22 carries `[--re-review <prior-findings-file> --baseline <saved-copy>]`.
- Bullet 6 today: Reviser brief above `verdict:`, lists blocking ids, "revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after".
- `docs/designs/spec-panel-review-loop.md:73` rejected a size limit: "a limit conflicts with FR-8/FR-9 gap-filling, and nothing could check it from text". `:19` lists "a size limit on revisions" as out of scope. `:143`: "The tests prove the text is present ... not that a reviewer obeys it."
- FR-8/FR-9 (`spec-panel.md:328-329`) force MAJOR on GAP rows and blank behaviour cells; 427 bullet 2 keeps them blocking.
- Pinned by `tests/skills/test_spec_panel_review_loop.py` (T1-T10, parametrized over `src/` and `plugins/` copies) and `tests/skills/test_review_severity_rule.py` (cap text, any-severity phrase bans).

## Where a checker can live (existing patterns)
- Skill-bundled stdlib scripts run from the installed path: `uv run --no-project python "<skill base>/scripts/origin_repo.py"` (`src/superclaude/skills/sc-issue-protocol/SKILL.md:72,84`); other examples `sc-implement-protocol/scripts/archive_workspace.py`, `sc-crash-recovery/scripts/parse_session_log.py`. Installed copy exists at `~/.claude/skills/sc-implement-protocol/scripts/archive_workspace.py`. This pattern works in any project (no package import) and in the S1 experiment worktrees, whose repo base (2cb683f5) predates any new package code.
- Package CLI: `src/superclaude/cli/main.py:521-565` registers click groups (sprint, roadmap, reflect, eval, swarm, ...). `superclaude` 5.0.0 is on PATH at `~/.local/bin/superclaude` (pipx-style install), so a new subcommand reaches workers only after a reinstall of the package; an experiment cannot add it additively.
- Only `src/superclaude/cli/eval/expect.py` imports `difflib` today; stdlib `difflib.SequenceMatcher` on sentence lists is available without a dependency.
- Install: `src/superclaude/cli/install_commands.py` copies every `src/superclaude/commands/*.md` into `~/.claude/commands/sc/`, skipping existing files unless `--force` (lines 60-90 show the result messages). A new `spec-panel-minfix.md` installs as `/sc:spec-panel-minfix` beside the original without touching it.
- Project rule: installed primitives never cite `src/superclaude/` paths; dual-surface lookup (`~/.claude/skills/...` first, then project `.claude/skills/...`) pinned by `tests/skills/test_primitive_dual_surface_lookup.py`.

## Later adopters (reach)
- `/sc:reflect` (CLI wrapper `src/superclaude/cli/reflect/`), rf-qa Fix Cycle (`src/superclaude/agents/rf-qa.md:379-416`, 2-cycle cap), `/sc:implement` QA (`~/.claude/skills/sc-implement-protocol/refs/qa.md`: reviewer "may not widen the AC"; delta-diff re-review). A stdlib checker keyed on (baseline, revised, ledger) is document-agnostic, so each could call it after its reviser step.
- Example of the growth pattern the checker targets inside the framework itself: `src/superclaude/agents/rf-qa.md:82` is one bullet carrying a dozen named invariants (R-113 to R-126, INV-012, INV-021) added across fix cycles.
