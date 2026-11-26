# Issue 561 architecture analysis

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli/eval/commands.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/561/analyze`.

Static review at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, on 2026-11-24. This is the narrowest source file covering both rejected selections. Supporting reads cover the scratch-root guard and existing acceptance tests. The live issue and all three comments were read.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:04:53Z; degraded: graph:truncated. Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. The callee query returned 30 of 36 rows; no conclusion relies on missing rows. File layout, symbol outline, callers, callees and one-level impact were queried; cited findings were confirmed from source.

## Severity-rated findings
1. **Low: validation follows allocation.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/commands.py:1753-1780` creates the per-run directory and homes child before suite resolution at `:1785-1789` and eval-ID validation at `:1798-1810`. Immediate error exits do not remove these directories. This confirms the issue's core defect from present source, without running the harness.
2. **Low: acceptance tests miss the disk side effect.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/eval/test_eval_run.py:384-425` asserts the two rejection codes and messages but not absence of new output directories. Extending these existing tests is the smallest regression surface.

Safety constraint: scratch-root resolution precedes the first mkdir (`commands.py:1727-1753`), and runtime allowlist extension precedes homes creation (`:1765-1780`). `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/eval/config.py:238-248` rejects paths outside the allowed roots and bare allowed prefixes. These protections must remain before writes; the proposed ordering change does not authorize weakening them.

## Metrics and boundaries
One primary Python file; two rejection paths; two existing focused acceptance tests inspected. Supporting source: the scratch-root helper. Two confirmed low-severity findings; no source changes. No dynamic analysis, tests, model launches, installs, environment creation, cleanup, commits, staging or GitHub writes. Current runtime reproduction, historical probe artifacts and the latest remote default-branch file contents are UNVERIFIED. Source review is of the named local checkout, not an implied remote synchronization.

Historical context: merged PR #75 (`0365a055f93e5703d9251873c8422d86e47911b3`) documents allowlist ordering and command acceptance work; merged PR #68 (`dce3c3cb5b689cf47755f2f4f08c1b688a7054d7`) concerns earlier scratch-root fixes. Neither is a verified fix for issue #561. Explicit `"#561" in:body` PR search returned no results; broader numeric and defect-text searches were noisy and are not proof of exhaustive absence.

## Recommendations
Keep issue #561 open on Backlog at P3. The live 2026-11-18 owner-directed comment forbids implementation until the unused eval harness is used again. The likely repair is simple/S: move directory allocation after suite parsing and eval selection checks, then extend existing regression tests without weakening scratch validation, containment or coverage. This is a future repair description, not authorization or a repair performed here.

The parent issue #354 owner instruction explicitly requested filing leftover folders separately from the diagnostic defect (#560) and coverage-policy question (#562). Neither sibling must be solved to fix the allocation order. No verified implementation dependency or downstream issue blocked by #561 was found in those records.
