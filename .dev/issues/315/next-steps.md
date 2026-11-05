/model claude-gw-tier1a

# Next steps for #315

Run these in your own session, in order. `/sc:issue` does not run them.

0. Before step 1, settle the two plan questions the owner left open, and put the answers into the step 1 prompt: (a) the no-prompt worker paths (`orca orchestration worker-start --agent claude`, `orca agent launch` without a prompt): orchestrators always pass the task or a name, with "a typed line that cannot be a session name is the first message to Claude" as a safety net; (b) Claude Agent Teams: route it through ccsession, or keep it as the one exception.
1. `/sc:workflow "Fix GitHub issue #315, IronClaude part only: agent-launched Claude sessions stop at the ccsession session name question. Implement the owner-approved plan (issue comments of 2026-11-03 and 2026-11-04, owner takeover 2026-11-05) in src/superclaude/skills/ccsession-tag/ccsession and ccsession-orca: one naming-question rule, unique auto-name, 30-second timer on every question, Ctrl+C cancels back to the shell, and keep the PR 355 tab reopen ahead of the question. Update README.md, CHANGELOG.md and docs/testing/v5.0.0/user/D08-ccsession.md, and the tests in tests/unit/test_ccsession_tag.py and tests/unit/test_ccsession_tiers.py, with real runs in a throwaway HOME. Read first: .dev/issues/315/issue-summary.md, .dev/issues/315/accuracy-check.md, .dev/issues/315/analysis/analyze-ccsession-tag.md. Build on master, never on origin/clayphi/433-ccsession-orca-resume. Out of scope: the Coder repo." --depth standard --handoff none`
   - Input: `@.dev/issues/315/issue-summary.md`
2. Read the plan printed by step 1 (`.dev/tasks/to-do/<id>/<id>.md`) and its advisory check result; resolve gaps before step 3.
3. `/sc:implement .dev/tasks/to-do/<id>/<id>.md` (use the plan path printed by step 1)

- Effort estimate: 24 hours
- Default row not used: Bug, complex (`/sc:troubleshoot --depth deep --fix`, then `/task`). The accuracy check and analysis already diagnose the bug and the owner approved the design, and `--depth deep --fix` couples to the MDTM task-file route, which needs explicit selection or an exceptional machinery need; the ordinary route is `/sc:workflow` then `/sc:implement`.
