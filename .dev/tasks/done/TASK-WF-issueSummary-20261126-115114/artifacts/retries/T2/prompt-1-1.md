040c4dd6d555e11688c7ca4f2c6031571f76f04f
Review one task for spec compliance.

Task brief: Task 2: Record the manual acceptance results required by the issue

Depends on: Task 1

Deliver the manual acceptance evidence required by ./source.md and issue 610. Exercise the updated troubleshooting skill through a fresh headless session (claude --print --output-format stream-json --verbose --no-session-persistence --max-budget-usd, with --plugin-dir pointing at a temporary plugin under ./artifacts/). MF-1: that plugin, for example named issue610-check, holds .claude-plugin/plugin.json and a byte-identical copy of the Task 1 skill directory as skills/sc-troubleshoot-protocol/; it is verification evidence, not a shipped plugin, and the user-wide installation is not touched. MF-1: the child must call the Skill tool for issue610-check:sc-troubleshoot-protocol on the exact input "ccsession is taking too long to load", with no --type, run all of Wave 0 including creating the real audit file, emit the Wave 0 completion line and stop there; the launch prompt must not state the expected type. Retain under ./artifacts/ the stream transcript with the Skill tool call and consumed path, sha256 of the plugin copy and of the checkout skill, the audit header and the completion line. MF-1: label the run a namespaced checkout-skill, Wave 0-only run, not proof that the default /sc:troubleshoot name resolves to the changed copy or that diagnostic agents ran; a source-text assertion or table reading is not runtime evidence. Also check "takes forever", "hangs" and ambiguous "leak" wording against the updated Wave 0 instructions and distinguish these bounded classification checks from a full diagnostic run. Use the existing audit/evidence formats rather than adding product logic. Run the related existing tests under tests/troubleshoot/ and retain their observed result. Post the exact sample's observed type and the leak rationale as an issue comment on IronbellyOrg/IronClaude issue 610, with the source change and verification result; do not stage .dev/issues/.

Acceptance criteria:
- The exact sample run, with no --type override, shows an actual Skill tool call for the plugin copy in the transcript, a real audit file, and the child's own Wave 0 complete: type=performance with a matching audit header. Evidence, consumed path and hashes are under ./artifacts/. A failed load, missing audit file or static table comparison is not a pass (MF-1).
- Bounded checks record performance for "takes forever" and "hangs"; an ambiguous leak report remains unset and does not exclude security. State their scope honestly, without claiming all specialist agents ran.
- Related tests under tests/troubleshoot/ have an observed result recorded under ./artifacts/. A failure is investigated and reported, not hidden or called a pass.
- A comment on https://github.com/IronbellyOrg/IronClaude/issues/610 records the exact sample's observed result, leak rationale, and successful synchronization check. Its comment URL is retained under ./artifacts/.

AC ids:
T2.AC1: The exact sample run, with no --type override, shows an actual Skill tool call for the plugin copy in the transcript, a real audit file, and the child's own Wave 0 complete: type=performance with a matching audit header. Evidence, consumed path and hashes are under ./artifacts/. A failed load, missing audit file or static table comparison is not a pass (MF-1).
T2.AC2: Bounded checks record performance for "takes forever" and "hangs"; an ambiguous leak report remains unset and does not exclude security. State their scope honestly, without claiming all specialist agents ran.
T2.AC3: Related tests under tests/troubleshoot/ have an observed result recorded under ./artifacts/. A failure is investigated and reported, not hidden or called a pass.
T2.AC4: A comment on https://github.com/IronbellyOrg/IronClaude/issues/610 records the exact sample's observed result, leak rationale, and successful synchronization check. Its comment URL is retained under ./artifacts/.
Global constraints: 

- Follow ./source.md and the original acceptance criteria of issue 610. Nothing to decide: build what the issue asks for, within its own scope.
- No Jev call, preflight component, gateway change, or changes to other keyword rows beyond the leak decision. Do not redesign the classifier or force Tier 2 escalation.
- Edit canonical source only. Generated .claude/ copies are never staged; .dev/issues/ is not staged. Stage .dev/tasks/, including its artifacts. Commit, push and pull request work remain outside this plan and follow the story's later steps.
- Add or extend a test only if existing repository coverage tests this table; otherwise preserve manual evidence instead of inventing a new matcher or test system.
- Do not change the installed user-wide skill just to make a check pass. The manual run must consume the changed checkout skill, not silently exercise the old installed row.


Start sha: 040c4dd6d555e11688c7ca4f2c6031571f76f04f
Diff against the start snapshot: 
Task-owned artifacts to Read: .dev/tasks/to-do/TASK-WF-issueSummary-20261126-115114/artifacts (exclude retries). For Task1 read sync-dev.log, verify-sync.log and coverage-inspection.txt. For Task2 read manual-evidence.txt, classification stream/audit and pytest.log plus issue-comment.url. New evidence files absent from snapshot are included in full by Reading these actual paths.
Codegraph context: index_state:stale checked_at:2026-11-26T11:57:10Z worktree_root/projectPath:/home/coder/workspaces/worktrees/IronClaude/issue-610. call codegraph only when index_state: fresh, never to widen scope. Q2b used Grep/Read; command and Wave3 lenses unchanged, install/contract tests depend on canonical skill.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
