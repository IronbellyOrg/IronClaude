# /sc:recommend output for #315

- Recorded: 2026-11-05T03:06:59Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/315. Type: bug. Complexity: complex. Summary: .dev/issues/315/issue-summary.md. The owner already approved the design in the issue comments, so only a checked written plan and its execution are needed; IronClaude part only. Suggested route: default row "Bug, complex" (troubleshoot --depth deep --fix, then /task).

The block below is the skill's output, copied verbatim.

````text
Goal: Fix issue #315 (agent-launched Claude sessions stop at the ccsession session name question) in the IronClaude part only (ccsession and ccsession-orca, with tests), from a design the owner already approved.

Level: 3 (follow a checked implementation plan) - guide section 3.4 (ordinary planned fix) with 3.3, row `bug` branch 3b

Changes files: yes. Step 1 writes a plan package under .dev/tasks/to-do/; step 3 edits src/superclaude/skills/ccsession-tag/ and tests/unit/. No commit, push or PR.

Run these in order:

1. /sc:workflow "Fix GitHub issue #315, IronClaude part only: agent-launched Claude sessions stop at the ccsession session name question. Implement the owner-approved plan (issue comments of 2026-11-03 and 2026-11-04, owner takeover 2026-11-05) in src/superclaude/skills/ccsession-tag/ccsession and ccsession-orca: one naming-question rule, unique auto-name, 30-second timer on every question, Ctrl+C cancels back to the shell, and keep the PR 355 tab reopen ahead of the question. Update README.md, CHANGELOG.md and docs/testing/v5.0.0/user/D08-ccsession.md, and the tests in tests/unit/test_ccsession_tag.py and tests/unit/test_ccsession_tiers.py, with real runs in a throwaway HOME. Read first: .dev/issues/315/issue-summary.md, .dev/issues/315/accuracy-check.md, .dev/issues/315/analysis/analyze-ccsession-tag.md. Build on master, never on origin/clayphi/433-ccsession-orca-resume. Out of scope: the Coder repo." --depth standard --handoff none
2. Read the actual printed plan .dev/tasks/to-do/<id>/<id>.md and its advisory check result; resolve gaps before step 3.
3. Only because execution was requested: /sc:implement <actual printed plan path>

Notes:
- The accuracy check and the analysis already diagnose the bug and the owner approved the design, so no /sc:troubleshoot run is added ("Do not diagnose again merely to obtain planning").
- The default row (/sc:troubleshoot --depth deep --fix, then /task) was not used: explicit deep plus fix couples to MDTM, and MDTM needs explicit selection or an exceptional machinery need, neither of which applies here.
- Two plan questions are still open and must be settled before step 1 so the plan can state them: (a) no-prompt worker paths (worker-start, agent launch without a prompt); (b) whether Claude Agent Teams goes through ccsession.
- Resume an interrupted step 3 by running the same /sc:implement command again.

Sources verified:
- src/superclaude/core/HOW-WE-WORK.md (routing table, row `bug`; level table; sections 3.3, 3.4)
- /home/coder/.claude/commands/sc/workflow.md (Read; flags --depth standard, --handoff none verified)
- /home/coder/.claude/commands/sc/implement.md (Read; positional plan path verified)
- /home/coder/.claude/skills/sc-workflow-protocol/SKILL.md (exists; depth values verified)
- /home/coder/.claude/skills/sc-implement-protocol/SKILL.md (exists)
- auggie semantic rank: skipped (matched row)
````
