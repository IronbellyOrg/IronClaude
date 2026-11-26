---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-issueSummary-20261126-044758
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Make Pragmatic questions understandable without session context

Source: ./source.md
Goal: Every Pragmatic question or decision request gives concise context, implications and risk, links existing detail only, and preserves the existing question rules.

## Constraints

- Change only the canonical Pragmatic style and its focused content/delivery tests; leave core RULES, worker communications, AskUserQuestion, installer behavior and Makefile behavior unchanged.
- Do not generate or curate detail files merely to provide a link. Never change the real user's home configuration; installation checks use temporary homes.
- Preserve all existing decision-request, answer-line and general response-format rules unchanged. Required question context is useful information, not filler prohibited by the no-preamble rule.
- Work on the existing feature branch against integration. Stage `.dev/tasks/` including evidence, but never stage `.dev/issues/`, generated `.claude/` mirrors or project-root `artifacts/`.
- Decided for this work: Nothing to decide: build what the issue asks for, within its own scope.

## Phase 1: Extend the user-facing guidance

## Task 1: Add the assume-blind question rule

Extend the Decision requests section in `src/superclaude/output-styles/pragmatic.md` with one concise bullet covering questions as well as decisions and approvals. Assume the user has none of the session context. Before asking, explain context, implications and risks in roughly one line each. Link an already-existing file with more detail when one exists; forbid creating a file solely to link it and require saying when no existing detail file exists. Follow ./source.md, What the issue asks for; the optional core-rule mirror is deliberately omitted because this is a Pragmatic-only requirement.

Acceptance criteria:
- A single new bullet in Decision requests explicitly covers every question or decision request, assumes no prior session context, and requires context, implications and risks before asking in roughly one line each.
- That bullet requires a path or link to an existing detail file when available, explicitly forbids making a file just to link, and says to state when no existing file has more detail.
- Existing EXACTLY ONE question, self-sufficient-option, answer-line and no-manufactured-choice text remains unchanged and in its original order. No other production file changes.
- Review the rule against a sample approval request with an existing detail file and a sample question without one, recording the examples and assessment in the task's existing review evidence. This is a wording check, not proof of live model compliance.

## Phase 2: Guard the rule and its delivery

## Task 2: Extend content and installation regression coverage

Depends on: Task 1

Extend `tests/commands/test_pragmatic_plain_english.py` using its existing literal/section/order pattern to guard the new rule and preserve earlier question rules. Strengthen `tests/cli/test_install_user_setup.py:test_output_style_installs` to compare installed Pragmatic bytes to the canonical source through `install_output_styles(home=tmp_path)`. Reuse the keep/forced-refresh/backup checks already in `tests/cli/test_install_keep.py`, rather than adding duplicate cases. Installer functions and callers remain unchanged.

Acceptance criteria:
- Focused content tests fail if the new rule disappears, moves outside Decision requests, duplicates, or loses any required context/implications/risk, existing-file-only, no-file-creation or missing-detail behavior. They also guard the original one-question, self-sufficient-option and answer-lines requirements and their order.
- The isolated-home installer test verifies byte-for-byte equality with canonical pragmatic.md, not just its header; no network or real-home writes are needed. Existing keep and forced-refresh/backup tests pass unchanged.
- Run `uv run pytest tests/commands/test_pragmatic_plain_english.py tests/cli/test_install_user_setup.py tests/cli/test_install_keep.py tests/commands/test_sweep_command.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_rule.py -v`, then `uv run pytest`, `make lint`, `make sync-dev` and `make verify-sync`; retain observed outputs under ./artifacts/. Report any unrelated failures accurately rather than changing unrelated code or claiming a pass.
- Treat sync verification as a separate regression check, not output-style delivery proof. State that static content, installation and sample review do not guarantee live model responses obey the rule.
