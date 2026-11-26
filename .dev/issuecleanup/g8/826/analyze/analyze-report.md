# /sc:analyze report: issue 826 area (architecture, quick)

Target: docs/developer-guide/release-procedure.md, src/superclaude/skills/sc-post-release-protocol
Codegraph: index_state=not_checked (docs and markdown are not indexed; Grep/Read floor used), checked_at=2026-11-25T00:57:50Z; degraded: graph:disabled-by-scope (markdown only)

## Findings
1. HIGH: docs/developer-guide/release-procedure.md still names master as the base: line 59 (`--base master`), line 71 (G2 `--branch master`), line 88 (tag rule "later master commit"), line 22, line 3. Same on origin/integration (local ref 4e35750e7, after PR 824 merged).
2. HIGH (architecture): src/superclaude/skills/sc-post-release-protocol/SKILL.md:91 checks `git merge-base --is-ancestor <tag> <default-branch>` with the default branch auto-detected. The default is now integration. Under the chosen rule (merge commit into master, tag on that merge commit) the tag commit is not an ancestor of integration until master is merged back, so the check reports a false release-integrity finding.
3. MEDIUM: CLAUDE.md "Branch structure" and step 4 (lines 290, 297 on origin/integration) already say integration then master, but give no release-PR commands.
4. LOW: impact.md:23, auggie-review.md:37 and :113 use origin/master in diff examples.
5. MEDIUM: no test targets post-release base-branch logic (only tests/skills/test_worker_contract.py:2371-2384 and a routing-table name check).
