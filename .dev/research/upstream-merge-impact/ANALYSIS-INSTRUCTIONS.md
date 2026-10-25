# Upstream change impact: analysis contract

## Scope and safety

Repository: /config/workspace/IronClaude/.dev/worktrees/ci-followup. Snapshot HEAD: 053b75664c8979bf223b8040f68310dce882d05b. Date: 2026-10-23. Window: 2025-10-23 through 2026-10-23 inclusive, UTC committer timestamp; preserve author dates and identify any discrepancy.

Read-only investigation. Write ONLY inside .dev/research/upstream-merge-impact/, and only your assigned report and uniquely named supporting evidence. Do not fetch, stage, commit, revert, alter index, create worktrees, install, sync, run tests that create state outside this directory, or update memories. Do not invoke nested agents. Do not change source or mirrors. Use UV for Python, with UV_CACHE_DIR inside the authorized directory and `uv run --no-project --no-managed-python` to avoid project synchronization.

## Required procedure

Read src/superclaude/commands/analyze.md and follow its Discover, Scan, Evaluate, Recommend, Report flow with --focus architecture --depth deep over EVERY path changed by your assigned commits. Invoke Skill sc:analyze if available, passing the assigned paths and these flags; respect this research-only scope and output destination. The command file names no separate protocol skill. Read inventory.json and units.json in this directory for full hashes and exact changed paths. The changed paths are historical: map deletions and moved files to current consumers, not merely their old names.

Read governing template src/superclaude/templates/modularization-template-review/codebase-research_template.md. Before investigating findings create your report with its header and full Findings/Gaps/Key Takeaways skeleton and explicit RF_PLACEHOLDER markers, then populate incrementally. Use the template's [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED] tags. Adapt Findings with subsections for the questions below. Preserve all evidence artifacts.

## Questions to answer for EACH commit and coherent subchange

1. What changed, using actual parent-to-commit patches (first-parent net patch for merge commits), not commit subjects alone? Separate added behavior, deleted behavior, metadata, and formatting.
2. What currently depends on it: code, imports, tests, documentation, installed skills/agents/commands, CLI, packaging, plugin distribution, CI? Trace entry point to implementation and consumer. Distinguish real runtime dependencies from prose references and unused historical surfaces.
3. Which later fork-owned commits built on, replaced, removed, or corrected it? Cite representative full or short hashes plus exact source evidence. Use ancestry/history, not date alone. A commit touched later does not alone prove a functional dependency.
4. Does reversing the change apply cleanly at snapshot HEAD? Central reverse-checks.json records `git apply --reverse --check` against current tracked checkout without writes. This is a strict patch check, NOT a true git revert simulation. Report its exact return code and conflicts and explicitly label actual Git three-way revert behavior UNVERIFIED unless separately proved without mutating .git or source. Never run a real revert, even --no-commit, in this worktree. A failed strict check does not prove a three-way revert must conflict. Partial/renamed/deleted paths and merge mainline requirements must be explicit.
5. What breaks, is lost, must be rewritten, or is already superseded if reversed? Include fork's own work accidentally removed by whole-commit reversion. Distinguish present findings from conditional predictions and do not claim tests ran.
6. Verdict keep|revert|partial, severity and risk, recommended narrow boundaries, estimated effort with clearly labeled judgment and assumptions. Assess every included commit explicitly even if grouped. Do not make an unverified claim the basis of a recommendation.

## Evidence and completeness

Cite live source file:line for claims, after Read of exact lines. Historical evidence must be distinguished as `<sha>:<path>:<line>` and may be materialized under your supporting-evidence subdirectory for stable readable citations. Git-derived facts should cite inventory.json, units.json, reverse-checks.json, or your saved command output with line numbers. Do not fabricate current paths for removed files. Full path lists belong in the report or linked manifest; account for EVERY changed file, including non-code paths, classify them by consequence, and mark anything not inspected UNVERIFIED. If using codebase graph tools, check_index_coverage on relied-on files and use direct source fallback for gaps. Use Auggie for cross-cutting discovery, then verify live source. No external web research is necessary for repository history analysis.

Provide a commit decision ledger, source evidence, changed-path coverage, later fork dependencies, reverse applicability, loss/rewrite cost, reversal prerequisites/order, and explicit unverified gaps. Do not conflate clean patch reversal with safe removal. Other units share files; identify cross-unit prerequisites without analyzing their commits redundantly.

## Return contract

Write the complete report to .dev/research/upstream-merge-impact/<your-unit-id>.md. Return ONLY that path, no report body. Stop when written. The parent will independently review the on-disk artifact.
