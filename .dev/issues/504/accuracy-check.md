## Accuracy check for #504

**Verdict:** current

Checked against `origin/master` at ec259f1b718ccdb9f08bba0237bfa47b2b7601a2 (committed 2026-11-11T16:44:25Z, before the issue was opened at 19:28:40Z), and the pull requests merged since the issue was opened (0, list truncated: no). The local checkout (`495eb96d1`) is 49 commits behind `origin/master`; every path below exists in both, and all evidence is quoted from `origin/master` (`git show` / `git grep origin/master`).

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "`src/superclaude/commands/analyze.md` — `/sc:analyze` command definition" | still true | Exists on `origin/master` (125 lines). |
| 2 | "`src/superclaude/commands/design.md` — `/sc:design` command definition" | still true | Exists on `origin/master` (123 lines). |
| 3 | "`src/superclaude/commands/implement.md` — `/sc:implement` command definition" | still true | Exists (101 lines); `implement.md:79` invokes `Skill sc:implement-protocol`. |
| 4 | "`src/superclaude/commands/workflow.md` — `/sc:workflow` command definition" | still true | Exists (95 lines); `workflow.md:54` invokes `Skill sc:workflow-protocol`. |
| 5 | "`src/superclaude/skills/sc-implement-protocol/SKILL.md` — backing implementation protocol" | still true | Exists (178 lines). |
| 6 | "`src/superclaude/skills/sc-workflow-protocol/SKILL.md` — backing workflow protocol" | still true | Exists (78 lines). |
| 7 | "slash commands and their backing skills where present" (analyze and design have no backing skill) | still true | `git ls-tree origin/master src/superclaude/skills/` lists no `sc-analyze-protocol` or `sc-design-protocol`; `analyze.md` and `design.md` contain no `Skill` invocation (their only "skill" word is the report-directory rule at `analyze.md:97`, `design.md:96`). |
| 8 | "These commands and their backing skills do not currently use Codegraph" | still true | The only `codegraph` text in `analyze.md:97`, `design.md:96` and `workflow.md:71` is the `.codegraph/` report-directory exclusion, not tool use. `implement.md`, `sc-implement-protocol/` and `sc-workflow-protocol/` (SKILL.md and refs) have no `codegraph` match at all. |
| 9 | "the listed general-purpose agent files under `src/superclaude/agents/`: `system-architect.md`, `root-cause-analyst.md`, `refactoring-expert.md`, `security-engineer.md`, `performance-engineer.md`, `python-expert.md`, `backend-architect.md`, `quality-engineer.md`, `self-review.md`, `technical-writer.md`" | still true | All ten exist on `origin/master`. None of them mentions `codegraph` or `index_state`. |
| 10 | "use Codegraph only when the caller passes `index_state: fresh`" (shared agent rule) | still true (rule exists elsewhere, not in the listed agents) | The same rule already appears in `auggie-reviewer.md:79`, `reflect-reviewer.md:64`, `reuse-auditor.md:50`, `troubleshoot-analyst.md:27`, and in `core/CODEGRAPH.md:24` ("they call codegraph only when `index_state: fresh`"). |
| 11 | "`/sc:troubleshoot` or `/sc:reflect`, which already use Codegraph" | still true | `troubleshoot.md:3,6` and `reflect.md:6,144` list codegraph grounding and the `codegraph` MCP server; `sc-troubleshoot-protocol/SKILL.md:4` and `sc-reflect-protocol/SKILL.md:5` allow `mcp__codegraph__codegraph_status`. |
| 12 | "`~/.claude/CODEGRAPH.md` — Codegraph usage guide referenced by the existing protocols" | still true | Source is `src/superclaude/core/CODEGRAPH.md`; section "2. Readiness check (once per run)" at line 9, `index_state` classes at line 15. |
| 13 | "Add one Codegraph readiness check to each of the four slash-command workflows" (none exists yet) | still true | No readiness check text in any of the four commands or the two backing skills (see row 8). |

### Merged pull requests that touch this issue

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| None | No pull request was merged after the issue was opened (`scout.md`) | None | None |

<!-- sc:issue:accuracy-check -->
