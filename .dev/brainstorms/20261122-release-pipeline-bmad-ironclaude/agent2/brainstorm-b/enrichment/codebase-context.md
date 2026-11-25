# Codebase context (Wave 2A, quality_tier: primary for the augment scan, plus direct reads)

Gathered 2026-11-22. Tool: `mcp__litellm__augment_code-augment_code_search` (pushed master only) plus direct Read and Grep of installed files. No `/sc:analyze` call, so no nested analyze directory exists.

## Verified facts

1. BMAD story template (`/home/coder/workspaces/IronClaude/.claude/skills/bmad-create-story/template.md`): sections Story, Acceptance Criteria (numbered list "1. ..."), Tasks / Subtasks (checkboxes "Task 1 (AC: #)"), Dev Notes (architecture patterns, source tree to touch, testing standards, Project Structure Notes, References with source paths), Dev Agent Record (model, debug log, completion notes, file list). Status line `ready-for-dev`. Matches the topic file.
2. BMAD `bmad-create-story` SKILL.md states: "ZERO USER INTERVENTION" except story selection or missing docs; exhaustive analysis of PRD, architecture, UX, epics; uses subagents when available; goal is to stop LLM developer mistakes. So the story is already an LLM-researched artifact; a second LLM spec pass overlaps with it.
3. `/home/coder/.claude/skills/sc-issue-protocol/refs/chains.md` (installed, current): Feature simple = `/sc:workflow <summary> --depth quick --handoff none` then `/sc:implement` (NO brainstorm: "the issue summary already states the requirements"). Feature medium = `/sc:brainstorm "<topic> @<S>" --blind`, `/sc:design`, `/sc:workflow --depth standard`, `/sc:implement`. Feature complex = brainstorm `--depth deep --research deep --codebase --blind`, design, workflow `--depth deep`, implement. Bug simple = troubleshoot quick then implement. The older design doc `docs/designs/sc-issue-command.md` shows a brainstorm step for simple features; the installed chains.md is the current route and matches the topic file.
4. The existing IronClaude precedent therefore already encodes a conditional rule keyed on complexity: brainstorm only from medium upward, and the issue's own text is the spec for simple work.
5. `/sc:brainstorm --unattended` (command file `~/.claude/commands/sc/brainstorm.md`): refuses `--interactive`; skips research-deep; nested adversarial call runs `--unattended`; Wave 3 delegates to `sc-adversarial-protocol` Mode B with `--generate spec`; convergence below 0.50 fails, 0.50 to 0.65 is partial. Token pre-flight estimate for quick depth is about 80K tokens per proposal (2 proposals about 160K to 210K).
6. `/sc:adversarial` produces 6 artifacts per run (diff analysis, debate transcript, base selection, refactor plan, merge log, merged output). Its command file lists `--compare a.md,b.md` as Mode A and has an Unattended mode that accepts `--output`.
7. `/sc:implement` qualifies acceptance criteria per task and ids them `T<i>.AC<k>`; it requires an `AC:` / `Acceptance:` / `Acceptance criteria` / `Done when` block on each item (`~/.claude/skills/sc-implement-protocol/SKILL.md` line 98 and `refs/retry.md` lines 114 to 119). A BMAD story id such as AC 3 therefore needs an explicit mapping to the `T<i>.AC<k>` ids the executor writes.
8. `/sc:spec-panel` has a Review Loop section (`~/.claude/commands/sc/spec-panel.md` line 256); the topic says it is capped at 2 fix cycles (not re-verified here).

## Not verified

- How often BMAD Dev Notes are stale against current code (no data exists).
- Actual model-call counts of one `/sc:adversarial` run at quick depth (counts below in the debate are estimates from the protocol text, to be measured in the trial).
