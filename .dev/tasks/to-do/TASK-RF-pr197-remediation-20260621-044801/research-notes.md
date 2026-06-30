# Research Notes: Remediate PR #197 review findings

**Date:** 2026-06-21
**Scenario:** A (explicit — every change is grounded in the review + remediation spec)
**Depth Tier:** Quick
**Track Count:** 1
**Status:** Complete

> The authoritative "research" for this build is the code review and the remediation
> spec, both of which cite verified file:line evidence on the PR branch
> `feat/rf-harness-sync` (head `a3f3f0cb`):
> - Review: `.dev/reviews/pr-197-20260620223934/REVIEW.md`
> - Spec:   `.dev/reviews/pr-197-20260620223934/remediation-spec.md`
> - Audit:  `.dev/reviews/pr-197-20260620223934/audit.log`

---

## EXISTING_FILES

**R1 — Tavily rename (8 agent files, `src/superclaude/agents/`):**
- `rf-analyst.md` — frontmatter `tools:` lines 13-14 + body refs (`mcp__tavily__tavily_search`/`_extract`)
- `rf-assembler.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-task-builder.md`,
  `rf-task-executor.md`, `rf-task-researcher.md`, `rf-team-lead.md` — same pattern.
- CANONICAL (do-not-touch reference): `deep-research.md:6-7` uses `mcp__tavily__tavily-search` / `…-extract` (hyphen). Live session tool ids are hyphen.

**R2/R4/R5 — `src/superclaude/skills/task-builder/SKILL.md`:**
- L1668, L2218, L2370 — the "Nested-subagent and Skill-tool-in-subagent capability are confirmed" assertion (R2).
- `#6 --cli` input definition (R2 disclosure site).
- L2276 — "accepted-and-ignored per §4.2 clause 4" dangling ref (R5); the clauses live in the unnumbered note at ~L2246-2248.
- Rule 20 two-arm structure; `reflect_post_mode` frontmatter key (R4 bifurcation).

**R3 — `src/superclaude/cli/reflect/runner.py` + `tests/cli/reflect/`:**
- `_build_prompt()` directive at L367-380 (`return command + inline_directive`).
- `tests/cli/reflect/` unchanged by the PR; `test_no_nesting_guard.py` guards only the wrapper branch.

## PATTERNS_AND_CONVENTIONS
- Source-of-truth: edit `src/superclaude/…`, then `make sync-dev` + `make verify-sync`. NEVER stage `.claude/`.
- Python: `uv run pytest`, `uv run ruff format --check src/ tests/` (CI runs format check separately).
- Apply on branch `feat/rf-harness-sync` in an isolated worktree under `.dev/worktrees/`.

## GAPS_AND_QUESTIONS
- HD-1 (R2b): default-mode resolution (keep+cite / invert-to-cli / mark-experimental) is RyanW's design decision — MUST halt, not auto-default.

## RECOMMENDED_OUTPUTS
- One MDTM task file, Template 02, with per-finding phases (R1 mechanical revert, R2 disclosure+HALT, R3 test+doc, R4 doc table, R5 ref fix), each with make sync-dev/verify-sync + (for R3) pytest verification.

## SUGGESTED_PHASES
- Phase 1: worktree setup. Phase 2: R1 (8 agents, one item per file). Phase 3: R3 (runner test+doc). Phase 4: R2a disclosure + R2b/HD-1 human-decision HALT item. Phase 5: R4+R5 task-builder doc fixes. Phase 6: sync + lint + test validation. Phase 7: completion.

## TEMPLATE_NOTES
- Template 02 (multi-phase, has discovery/verification). Quick tier (small, fully-specified). R6 OUT OF SCOPE.

## AMBIGUITIES_FOR_USER
- HD-1 is the only genuine human-decision point; encode as a `needs_human_decision` item that writes PENDING and HALTS (per project rule: human-decision items must HALT, never auto-default).
