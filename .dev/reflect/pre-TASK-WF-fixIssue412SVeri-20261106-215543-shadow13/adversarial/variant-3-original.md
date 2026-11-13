# Reviewer 3 card — refactorer lens (UC-1 pre-execution plan audit, post-hoc vantage)

Plan: .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md
Spec: .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md
Evidence used: artifacts/t1-tests.log, artifacts/t2-tests.log; current src/superclaude/core/CLAUDE.md:45-61, src/superclaude/skills/ccsession-tag/README.md:228-245, src/superclaude/cli/install_user_setup.py:279-327.

Context for F1: the spec asks for "matching" README guidance. Task 1's checks only require the same items to appear in each copy; nothing compares the two copies. The plan's original guidance test had 2 items, one per copy (t1-tests.log:5,11), and checked text fragments copy by copy. The delivered first paragraphs already differ on the ccsession-orca sentence: core/CLAUDE.md:51 versus README.md:234-235. The identical-paragraph check in the test file covers only the later "Every Orca worktree" paragraph, which this plan did not add.

Context for F2: install_orca_skills (install_user_setup.py:279-327) has no code that writes to guide files, and the tests replace Orca with a stub. So "edited-guide contents are not rewritten by IronClaude" cannot fail. The spec's "do not overwrite edited guides" is really enforced only by the "no --force" check.

Out of scope (agreeing with T1-F4): the third, differently worded copy in the root CLAUDE.md. The spec never names it, so it is not counted as a plan failure.

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The spec asks for README guidance that matches core/CLAUDE.md, but Task 1's criteria only list items each copy must contain and never compare the copies, so the shared guidance can drift; the delivered copies already differ on the ccsession-orca sentence.","refs":["INF-001"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md","line_start":1,"line_end":1,"quote":"Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance"},{"role":"plan","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md","line_start":35,"line_end":36,"quote":"Both instruction surfaces explicitly distinguish Claude (CLI) for ccsession-backed Claude sessions from New Terminal"}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"The Task 2 clause 'existing edited-guide contents are not rewritten by IronClaude' cannot fail: install_orca_skills never writes guide files and the tests stub out Orca, so only the no---force check actually enforces the spec's do-not-overwrite rule.","refs":[],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md","line_start":1,"line_end":1,"quote":"Do not forward --force to Orca or overwrite edited guides"},{"role":"plan","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md","line_start":50,"line_end":50,"quote":"The external command never gains --force and existing edited-guide contents are not rewritten by IronClaude."}]}
```

Confirmed coverage: the plan includes the spec's two phases (guidance, then forced refresh), the before-fix test failures, force propagation, the default skip when guides exist, Orca being absent or failing without stopping setup, and the sync and staging steps.

reviewer_model_self_report: claude-gw-tier1a (I was pinned as claude-opus-5-5 but am actually running as claude-gw-tier1a)
