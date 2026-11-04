# Issue #302 handoff: 01 design report

- Task: task_9d8f851e0be6 (dispatch ctx_88bb0f27ecf8)
- Branch: ironbelly/feat-sc-issue-command
- Scope: written design for `/sc:issue` only. No source under `src/` or `tests/` was edited.

## 1. Design document path

`docs/designs/sc-issue-command.md` (produced through `/sc:design sc-issue-command --type component --format spec`; `docs/designs/` is the repo's existing design folder).

## 2. Inputs read

- Issue #302 body and all three comments (`gh issue view 302 --repo IronbellyOrg/IronClaude --json title,body,comments`). Nothing was posted to the issue.
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, all 2062 lines.
- Installed command files `~/.claude/commands/sc/{brainstorm,design,workflow,implement,troubleshoot,analyze,recommend,pr-submit,adversarial}.md`.
- GFxAI templates `IronbellyGroup/GFxAI:.dev/proj_mgmt/clickup-integration/templates/ISSUE_TEMPLATE/{bug_report,feature_request}.md` and its ClickUp `.env.example` (read only, via `gh api`).
- Claude Code subagent docs (`https://code.claude.com/docs/en/sub-agents`) for model pinning; ClickUp v2 reference via Context7 for the task-list and update-task endpoints.
- Repo facts: tier table `src/superclaude/skills/ccsession-tag/ccsession-models.json` (tiers `tier0`, `tier1a`, `tier1b`, `tier2`, `tier3`, `tier4`); env `ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-5.3`; repo labels (GitHub defaults only); `tests/cli/test_issue_body_templates.py`; `tests/core/test_how_we_work_routing_table.py`; `src/superclaude/core/HOW-WE-WORK.md` "Other commands" table.

## 3. Flags cited in the design, verified against the real command files

| Command | Flags verified (file) |
|---|---|
| `/sc:brainstorm` | `--depth quick|deep`, `--research deep`, `--codebase`, `--blind`, `--handoff` (default `none`; `design` text-only; `tasklist` feeds `sc-tasklist-protocol`), `--models` (aliases only), `@path` topic (`brainstorm.md`) |
| `/sc:design` | `--type architecture|api|component|database`, `--format spec` (`design.md`) |
| `/sc:workflow` | `--depth quick|standard|deep`, `--handoff none` (`workflow.md`) |
| `/sc:implement` | `<path>` (`implement.md`) |
| `/sc:troubleshoot` | `--depth quick|deep`, `--fix`, `--context <path>`, `--scope <path>`; quick+fix STOP; deep needs 10+ words or `--scope` (`troubleshoot.md`) |
| `/sc:analyze` | `--depth quick|deep` only (`analyze.md`) |
| `/sc:recommend` | goal text; `Skill sc-recommend` (`recommend.md`) |
| `/sc:adversarial` | `--compare a,b`, `--depth quick` (`adversarial.md`) |
| `/sc:pr-submit` | `--monitor 3`, `--head`, `--title`, `--body` (`pr-submit.md`) |
| `/task` | the `task` skill, `<task file>` (`~/.claude/skills/task/`) |
| `gh` | `issue edit --add-assignee @me`, `issue create --title --body-file --label`, `issue comment --body-file`, `issue view --json`, `label list --json`, all with `--repo` (`--help` output) |

## 4. Defaults chosen by this design (no open questions left)

All 27 (D1 to D27) are in section 18 of the design, each marked as a design default with its reason. The ones the coordinator most needs to see:

- **D2 ClickUp match:** the issue URL in the task description or a custom field first, then `#<N>` as a whole token in the title; exactly one match or no assignment.
- **D3 tier map:** T3 `claude-gw-tier3`, T2 `claude-gw-tier2`, T1 `claude-gw-tier1a` (`claude-gw-tier1` does not exist).
- **D4:** no alias fallback when a picker ID is not served; STOP `E-TIER-UNAVAILABLE`.
- **D5 rubric:** simple up to 4 h, medium over 4 to 16 h, complex over 16 h or cross-subsystem or security/migration.
- **D6:** next-step tier simple -> T2, medium/complex -> T1 (replaces the issue body's T0 rows, per the owner's T1/T2 comment).
- **D7:** the complex-feature chain also runs `/sc:design` as its own step.
- **D13:** deep create with all flags = two variants debated by `/sc:adversarial --compare ... --depth quick`.
- **D14:** create prompts the user only when new material or a contradiction is found; never a routine preview.
- **D16:** labels from the fixed set that are missing in the repo are skipped and reported; never created.
- **D24:** the command never stages or commits `.dev/issues/`.
- **D25:** every brainstorm step passes `--models opus,sonnet` so no proposal runs on the `haiku` alias (`glm-5.3` here).
- **D26:** the command and skill say their templates replace core rule 10's templates for `/sc:issue --create`; rule 10 is not edited.

Model pinning (binding, verified): the Agent tool's `model` parameter takes only aliases and overrides frontmatter, and `haiku` maps to `glm-5.3` here, so each worker pins its picker ID in agent frontmatter and the skill never passes `model`.

## 5. Corrections to the issue text

- `--handoff tasklist` / `--handoff design` replaced per the owner's pipeline fix; the same fix is applied to the complex-feature path (D7).
- `---research deep` typo -> `--research deep`.
- T0 rows replaced by T1/T2 (owner comment).
- `/sc:analyze` has no `standard` depth: standard runs it with no `--depth`.
- Existing test `test_no_issue_skill_or_command_added` forbids an issue command and skill; the design replaces it.

## 6. Review and what is left

**Independent review:** a separate reviewer agent checked the design against the issue, the installed command files and the repo tests.
- Round 1: FAIL with 2 blocking findings, both fixed. (1) Adding `issue.md` would break `tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory`, so that test is now in the change list (`"issue"` goes into `_POST_REFRESH_ADDITIONS`). (2) The brainstorm steps used the default `--models opus,sonnet,haiku`, which puts a proposal on `glm-5.3`; every brainstorm row now passes `--models opus,sonnet` (D25). All 5 minor findings were fixed too.
- Round 2: PASS. Its one new minor finding (no test pinned D26) is fixed in the section 16 command-test row.

**Left (not in this task):**
1. Run `/sc:workflow docs/designs/sc-issue-command.md --depth standard --handoff none`, read the plan, then `/sc:implement <printed plan path>`.
2. Implementation-time checks the design already schedules: one smoke spawn per worker agent to confirm the picker ID is served, and one manual ClickUp claim against a test task.
3. Stage `.dev/tasks/issue-302-handoff/` per the always-staged rule when committing. This task committed nothing.

Files created by this task: `docs/designs/sc-issue-command.md` and this report. No file under `src/` or `tests/` was changed.
