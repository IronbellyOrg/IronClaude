db8f96b0454c910410ee2a14ae727982d082a134
Review one task for spec compliance.

Task brief: Task 7 of the plan /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md ("## Task 7: Record the built behaviour in the gate, spec, architecture and register files", read that section). Acceptance criteria, ids T7.AC1 to T7.AC3 in source order, are the three "Acceptance criteria:" bullets of Task 7 in that order (read them there).
Global constraints: the plan's "## Constraints" and "## Out of scope" content in the plan file above (read that section).
Start sha: db8f96b0454c910410ee2a14ae727982d082a134
Diff against the start snapshot: the full diff of the spec files under .dev/issues/409/bmad/spec-orca-observer/ is in the file /tmp/impl-T7-diff.patch (read it). Note the diff includes spec edits made by Tasks 1 to 6 only if they happened after the start snapshot; Task 7's own edits are release-gates.md, SPEC.md, ARCHITECTURE-SPINE.md and unverified-register.md; for the acceptance-tests.md check, verify by reading the test files under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/ named in rows T57 to T66 of .dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md. The full suite result to verify yourself: `uv run pytest tests/observe -q` (expect 762 passed), `uv run ruff check src/superclaude/cli/observe tests/observe` and `uv run ruff format --check src/superclaude/cli/observe tests/observe`. Codegraph context: index_state: fresh; checked_at: 2026-11-17T07:27:40Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp. Call codegraph only when index_state: fresh, never to widen scope. Dependents: documents only, no code symbol changed in this task.
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
