REMOVE THE "ANY ISSUE OF ANY SEVERITY FAILS" RULE AND CAP REVIEW LOOPS AT 2 ROUNDS (USER DECISION, 5.0.0 RELEASE BLOCKER)

USER DECISION (2026-10-31, verbatim): "Any severity fail rule: after review fails on minor, note them and proceed, do not recheck do not fail. Remove any severity rule. Limit review loops to 2."
Coordinator detail: when a review loop reaches its 2-round cap and BLOCKING (non-minor) findings are still open, stop and escalate to the user with the open findings; never pass them silently and never start a third round.

WHY
The QA-loop investigation (/home/coder/workspaces/IronClaude/.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md, sections 4 and 5, recommendation 1 "bundle A") found the longest loops (7 and 8 rounds, minor findings from round 3 on) came from "any finding of any severity means FAIL" rules with no round cap, outside /sc:implement.

TARGET
- Worktree: /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule, branch fix/review-severity-rule from origin/master AFTER PRs #337 and #338 merged (already created for you, no upstream set). Work from its root.
- Known hits on master (git grep -n -i -E 'any (issue|finding|gap)s? of any severity|any severity' -- src plugins commands agents CLAUDE.md): src/superclaude/output-styles/pragmatic.md:225 (and the lines around it: "a 'minor issues still pass' allowance is PROHIBITED", zero-finding-is-suspect stays); src/superclaude/agents/rf-qa.md:171; src/superclaude/agents/rf-qa-qualitative.md (8 PASS lines); src/superclaude/templates/documents/agent_template_qa.md:156; src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:643; 02_mdtm_template_complex_task.md:654-656; src/superclaude/skills/tech-reference/SKILL.md:536. Search more widely yourself too: other wordings ("zero tolerance", "any finding", "minor issues still pass", "must FAIL", "re-run QA until", "until PASS", unbounded fix-and-recheck loops, review loop counts > 2 such as rf-qa's 3-fix-cycle cap at rf-qa.md:390-391 and the MDTM templates' fix cycles), every tracked twin (plugins/superclaude/**, root commands/ and agents/ copies), and any ad hoc orchestrator review prompts in skills.

CHANGE
1. INVENTORY: write .dev/review-severity-rule/inventory.md listing every rule that (a) fails a review on a minor/low/cosmetic finding, (b) re-checks minor findings, or (c) allows more than 2 review rounds or has no cap; with file:line and the replacement wording you will use.
2. NEW RULE (one wording, reused everywhere; the output style holds the canonical text and others match it):
   - Findings are graded blocking (a real defect: wrong behaviour, false claim, missing required deliverable, security or data-loss risk) or minor (cosmetic, wording, formatting, citation format, nit, style, a moved line number on a true claim).
   - Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. They are not rechecked in later rounds and never trigger a fix pass on their own.
   - Only blocking findings produce FAIL.
   - A review loop (review, fix, re-review) runs at most 2 rounds. If blocking findings remain after round 2, stop and escalate to the user with the open findings; do not run a third round and do not pass them.
   - Keep the binary PASS/FAIL verdict, the adversarial stance and the zero-finding Self-Audit.
3. /sc:implement and /sc:workflow: their own severity models (#297, #338) already make minors non-failing; align them with the 2-round cap only where they currently allow more than 2 review rounds per task or per plan check, and keep their escalation path (retry adviser, halt) as the at-cap escalation. Read src/superclaude/skills/sc-implement-protocol/refs/qa.md and refs/retry.md first; if lowering their ladder to 2 rounds changes a saved-prompt or FINAL migration contract, escalate to the coordinator before changing it.
4. PLAN: this touches many files, so write a plan first: `/sc:workflow "<this task, citing FINDINGS.md and the inventory>" --depth standard --handoff none`, then `/sc:implement <printed plan path>`.
5. TESTS: add static tests (for example tests/skills/test_review_severity_rule.py) that fail if any "any severity ... FAIL" wording reappears anywhere in src/, plugins/, commands/ or agents/, that the canonical minor-findings and 2-round-cap text is present in the output style and each edited QA agent/template, and that src and plugin twins match. Update existing tests that pinned the old wording (grep tests/ for "any severity" and pragmatic.md:225; the #338 pins P1-P4 in tests/skills/test_implement_severity_static.py reference pragmatic.md:225, so update them to the new text rather than deleting them). Run the named tests plus every test that reads the edited files, make verify-sync, make lint (install dev deps with `uv pip install -e ".[dev]"` if ruff is missing). Never the full suite or tests/cli/eval/ as a directory.
6. COMMIT AND PR: commit by exact paths (stage .dev/tasks and .dev/review-severity-rule; never .claude/ except settings.json), conventional messages with your session's attribution line, `git push -u origin fix/review-severity-rule`. CLAUDE.md pre-PR checks, then `/sc:pr-submit --monitor 3 --head fix/review-severity-rule --title "fix(qa): minor findings never fail a review; cap review loops at 2 rounds" --body "<plain-text summary citing the user decision and FINDINGS.md>"`. Confirm the URL is on IronbellyOrg/IronClaude. Add a CHANGELOG.md Unreleased entry.

CONSTRAINTS
- Do not run superclaude install or edit ~/.claude. Never hardcode src/superclaude/ paths in installed primitives. Never push to master or upstream. Do not merge. Do not touch other worktrees or terminals.
- Apply the new rule to your own run: minor findings from your plan's reviewers are noted, not fixed in extra rounds.

OBSERVABLE ACCEPTANCE
- `git grep -n -i 'any severity' -- src plugins commands agents` returns no rule that fails reviews on minor findings; the new tests pass; verify-sync and lint pass; PR open on IronbellyOrg/IronClaude with CI green and no unresolved thread of medium or higher.
- worker_done gives the PR URL, final head SHA, the inventory path, the canonical rule text with its file:line, every file changed, and checks run with results.
