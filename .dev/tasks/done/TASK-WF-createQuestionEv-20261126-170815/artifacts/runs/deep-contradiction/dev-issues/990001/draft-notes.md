Proposed title: /sc:issue --create with an empty description: verify the reported crash and enforce the STOP rule

# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

- Codebase pass: codegraph and auggie tools were not available to this worker (no MCP tools in its toolset, and `~/.claude/CODEGRAPH.md` is absent), so the `/sc:analyze --depth deep` pass used Grep, Glob and Read only (source: this run).
- Environment line: the analysis host was Linux 6.8.0-149-generic, package version 6.1.0 (`pyproject.toml:7`), branch `qev-run`, commit `862384852` (source: `git rev-parse`, environment). The reporter's own environment is "Not known yet".
- Documented behaviour for an empty description is a STOP "--create needs a description" (`src/superclaude/commands/issue.md:56`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:156`). Added to Current Behavior and Expected Behavior.
- Only test of the rule asserts a phrase, not behaviour (`tests/commands/test_issue_command.py:191`); an empty description slugs to `untitled` (`tests/skills/test_issue_protocol.py:186-190`, `src/superclaude/skills/sc-issue-protocol/refs/create.md:3`). Added to Codebase Context and Root Cause lead.
- `refs/create.md` Wave 0 (lines 13-16) has no explicit empty-description check (source: Read of `refs/create.md`).
- Related issues: none, from the scout's two searches (`scout.md`).
- Priority Medium and the whole Fix approach and Test plan sections come from the pass (required plan sections).
- Assumption: the report is meant as a bug in the `/sc:issue --create` flow even though the named script does not exist; the issue is filed as filed (flags `bug` and `skill`).
- Assumption: Priority is Medium (degraded behaviour with a workaround) because the crash is unconfirmed; it becomes High if the crash is reproduced.
- Assumption: the likely real gap is that the empty-description STOP lives only in prose and the whitespace-only case is not named; the proposed Wave 0 check and tests follow from that.
- Assumption: the reproduction step `/sc:issue --create ""` is the literal reading of "when the description is empty"; the reporter's exact command is not known.
- Assumption: the fix target branch is `integration`, per the job's stated base branch and the repo's Git Workflow.
- The "[synthetic run marker: qev-deep-contradiction-185432]" text in `description.md` is not copied into the issue body.

## Contradictions

Question outcome (orchestrator): one question asked naming both items below; answer "keep my wording". Applied to issue-body.md: Bug Summary, Current Behavior, Expected Behavior and Root Cause Analysis now state the crash in `scripts/create_issue.py` as the user wrote it; Priority moved from Medium (assumption: crash unconfirmed) to High (a documented command fails). Title uses the user's wording. Codebase Context, Fix approach, Test plan and every New material item are unchanged.

- User-stated fact contradicted by verified code: "crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py`". Conflicting evidence: that file does not exist; `src/superclaude/skills/sc-issue-protocol/scripts/` holds only `clickup_claim.py`, `origin_repo.py` and `orca_worktree.py` (Glob of `src/superclaude/skills/sc-issue-protocol/**`), and `git log --all --diff-filter=D` finds no deleted `create_issue*` file; a repo-wide Grep for `create_issue` outside `.dev/` hits only `tests/hooks/test_launch_level_guard.py:3609`, an unrelated MCP tool name.
- User-stated fact contradicted by verified code: "`/sc:issue --create` crashes ... when the description is empty". Conflicting evidence: `src/superclaude/commands/issue.md:56` makes an empty `--create` description a STOP ("--create needs a description") before Activation, and `src/superclaude/skills/sc-issue-protocol/SKILL.md:156` repeats it; no code path that crashes on it was found (static read only, the behaviour was not run).
