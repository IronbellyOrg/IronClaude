# Summary: #289 Focused architecture analysis

<!-- Structure: ~/.claude/skills/sc-issue-protocol/templates/issue-summary.md, adapted to the analyze command's report requirements. -->

- Target: src/superclaude/core/HOW-WE-WORK.md
- Command: /sc:analyze src/superclaude/core/HOW-WE-WORK.md --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/289/analyze
- Scope: Static documentation architecture and issue-specific supporting sources; no source edits or dynamic analysis.

## What the issue asks for

Issue #289 requests an installed, tested worktree-and-branch policy and updated onboarding guidance. Its 2026-11-17 review predates the merged cleanup implementation in PR #711. This quick analysis checks the guide against the five questions; it does not run cleanup or implement policy.

## Relevant files and systems (cheatsheet)

Repository root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/`. Paths below are root-relative.

| Path or system | Why it matters |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md` | The 363-line Markdown target, read in full in bounded pieces. |
| `src/superclaude/core/WORKER-CONTRACT.md` | Existing placement and deletion protections used by the guide. |
| `src/superclaude/commands/worktrees.md`; `scripts/worktree_cleanup.py` | Already-built cleanup and evidence-saving implementation. |
| `tests/core/` | Existing ownership/registration checks; searched for the missing policy rules. |
| `docs/onboarding/ironclaude-onboarding.html` | Required acceptance surface still advertises unfinished work. |

## Analysis

### Prioritized findings

1. **Medium: general creation/reuse and naming policy is missing.** The complete guide has specialized Orca placement rules at `src/superclaude/core/HOW-WE-WORK.md:352-362` and restart guidance at `:210-221`, but not the owner's general new-work/reuse rule or under-25-character metadata-plus-description convention. Consequence: installed projects cannot use this guide to decide whether to reuse a worktree or how to name new work consistently. Existing claim-specific reuse (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:384-422`) and `issue-{number}` naming (`:695-708`) are useful prior art, not complete general policy.
2. **Medium: the onboarding acceptance criterion is still unmet.** `docs/onboarding/ironclaude-onboarding.html:515-523` still says the protocol is being worked out. Existing ownership tests at `tests/core/test_claude_md_worktree_rule.py:14-39` are not tests of the missing shared policy. Consequence: closing #289 now would leave a required training surface unfinished.
3. **Informational: avoid duplicating the cleanup engine.** The guide's `:299` entry now explicitly answers #289 item 4. PR #711 (merged 2026-11-22, commit `6b17a7449f9400a9acc4140d6ce48dec93a9de8e`) added guarded cleanup and raw `.dev/` preservation. `scripts/worktree_cleanup.py:2251-2271` writes provenance/checksums, not extracted lessons. Decide separately whether the earlier lesson-extraction proposal remains wanted. This is not evidence the raw archive is missing.
4. **Informational: installed-project cleanup has a stated boundary.** `src/superclaude/commands/worktrees.md:43-45` refuses execution outside an IronClaude checkout containing the script. A general installed-project guide must explain that boundary or point to the proper maintained implementation; it must not claim the installed slash command alone supplies cleanup everywhere.

### Metrics and domain limits

- Primary target: 1 Markdown file, 363 lines; read in full in chunks of at most 80 lines.
- Architecture findings: 2 Medium documentation/acceptance gaps; 2 informational scope/reuse observations. These are review judgments, not runtime defects or measured quality scores.
- Five decision areas: location is covered, safe cleanup and raw evidence preservation are substantially covered, general session allocation and naming are incomplete; semantic lesson extraction remains an owner-scope question.
- No source change, code execution, cleanup run, dependency audit, security scan, performance benchmark or test-suite run was performed. Security/performance conclusions are not established by this documentation-only quick analysis.
- GitHub issue/PR reads and native searches supported the review. Augment's first lookup failed because its default `main` branch does not exist; repeating it explicitly on `master` succeeded. No broad absence claim relies on the semantic search.

### Recommendations

Keep #289 open with a narrower remainder: document the general new-work/reuse policy, agree a concrete naming format, add policy tests, and update the onboarding card. Reference PR #711 for cleanup and the evidence destination instead of implementing a second cleanup tool. Treat lesson extraction as a separate unresolved scope choice. Explain that the existing cleanup command requires an IronClaude checkout and that its daily automation is not enabled by the checked-in definition.

### Codegraph

Codegraph: index_state=fresh, checked_at=2026-11-23T22:44:07Z; degraded: graph:empty

The readiness check found 0 added, 0 modified and 0 removed files. The target is Markdown, which this index does not parse: the core directory listing returned only `__init__.py`, and the target outline returned no indexed file. Graph call paths and symbol impact are not applicable to this prose target; findings use direct Reads and Grep instead. No index was initialized or changed.
