581eee20e6eff280e1326645bbc2aa81e08a52cb
Review one task for spec compliance.

Task brief: T1 (the whole source, persisted at /home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/source.md). T1.AC1 is the source text itself: "Reference our research and design material from pr697.  spawn parallel agents for each section in major design feature laid out in issue 655.  where direct conflict exists with our current plan except the current plan and reject 655.   build a list of the remaining design features that are current plan does not cover.  organize those remaining features into either features that belong to the tui dashboard, the watcher, or the coordinator.  then make three separate issues one for the next release of the coordinator with all features from our list, an issue for the ty bat dashboard with the features from the list and finally an issue for the observer.   populate the issue with any research or debate results from our documents in PR 697.   each issue should also have links to the other issues and a brief Review of all of the issues together to determine any dependencies or relationships between the individual features and the order in which the issues should be completed." Interpretations the orchestrator applied and records here so you can judge them: "except the current plan and reject 655" is read as "accept the current plan and reject 655"; "our documents in PR 697" is read as the unification folder /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/ (PR 697 itself is a closed revert PR that holds only code); "the observer" is read as the watcher (the third of the three groups named in the prompt); "ty bat" is read as TUI.
Global constraints: none stated in the source. Project rules that apply to GitHub work: every gh call passes --repo IronbellyOrg/IronClaude; nothing is filed on any other repository.
Start sha: 581eee20e6eff280e1326645bbc2aa81e08a52cb
Diff against the start snapshot: The task writes no tracked repository file. Its product is local analysis files plus three GitHub issue bodies that are drafted but NOT yet posted. Touched files, all new and untracked (read their full contents; there is no git diff):
- /home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/sections/section-01.md to section-14.md: one file per section of the Proposed Solution of issue 655; each feature has a status COVERED, CONFLICT or NOT-COVERED against the current plan (SPEC.md, DECISIONS.md and debate verdicts under /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/), a component for NOT-COVERED rows, and evidence quotes. Written by 14 parallel analyst agents.
- /home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/aggregate/rows.json: the merged parse of all rows (488 rows: 248 COVERED, 124 CONFLICT, 116 NOT-COVERED).
- /home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/aggregate/review.md: the shared "Review of the three issues together" (relationships and order).
- /home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/issues/coordinator.md, watcher.md, dashboard.md (with a .title file each): the three drafted issue bodies, built by script from rows.json using the item groups in /tmp/impl-agg/groups.json (115 NOT-COVERED rows grouped into items C1-C27, W1-W15, D1-D4; row S10-F60 is excluded on purpose because its analyst wrote "not a product feature"). The placeholders {{I_COORD}}, {{I_WATCH}} and {{I_DASH}} are replaced by the real issue numbers when the issues are posted, after the issues exist, so their absence of real numbers now is expected. The three issues are filed with the project's backlog template (sections: What was tried, Relevant files and links, Done when, Pick-up note).
Codegraph context: index_state: fresh, checked_at: 2026-11-21T14:20:46Z, worktree_root: /home/coder/workspaces/IronClaude, projectPath: /home/coder/workspaces/IronClaude. Call codegraph only when index_state: fresh, never to widen scope. Q2b: no code symbol was defined, changed or removed, so there are no dependents to list.
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
