039276ff7288e6f0a5e0afcb0d518a366881d8ae
Review one task for spec compliance.

Task brief:  Add the assume-blind question rule

Extend the Decision requests section in `src/superclaude/output-styles/pragmatic.md` with one concise bullet covering questions as well as decisions and approvals. Assume the user has none of the session context. Before asking, explain context, implications and risks in roughly one line each. Link an already-existing file with more detail when one exists; forbid creating a file solely to link it and require saying when no existing detail file exists. Follow ./source.md, What the issue asks for; the optional core-rule mirror is deliberately omitted because this is a Pragmatic-only requirement.

Acceptance criteria:
- T1.AC1: A single new bullet in Decision requests explicitly covers every question or decision request, assumes no prior session context, and requires context, implications and risks before asking in roughly one line each.
- T1.AC2: That bullet requires a path or link to an existing detail file when available, explicitly forbids making a file just to link, and says to state when no existing file has more detail.
- T1.AC3: Existing EXACTLY ONE question, self-sufficient-option, answer-line and no-manufactured-choice text remains unchanged and in its original order. No other production file changes.
- T1.AC4: Review the rule against a sample approval request with an existing detail file and a sample question without one, recording the examples and assessment in the task's existing review evidence. This is a wording check, not proof of live model compliance.


Global constraints: 

- Change only the canonical Pragmatic style and its focused content/delivery tests; leave core RULES, worker communications, AskUserQuestion, installer behavior and Makefile behavior unchanged.
- Do not generate or curate detail files merely to provide a link. Never change the real user's home configuration; installation checks use temporary homes.
- Preserve all existing decision-request, answer-line and general response-format rules unchanged. Required question context is useful information, not filler prohibited by the no-preamble rule.
- Work on the existing feature branch against integration. Stage `.dev/tasks/` including evidence, but never stage `.dev/issues/`, generated `.claude/` mirrors or project-root `artifacts/`.
- Decided for this work: Nothing to decide: build what the issue asks for, within its own scope.


Start sha: 039276ff7288e6f0a5e0afcb0d518a366881d8ae
Diff against the start snapshot: diff --git a/src/superclaude/output-styles/pragmatic.md b/src/superclaude/output-styles/pragmatic.md
index ad14f3dbe..54b1e35be 100644
--- a/src/superclaude/output-styles/pragmatic.md
+++ b/src/superclaude/output-styles/pragmatic.md
@@ -51,6 +51,7 @@ This applies to ALL message types: status, narration, next steps, tables, and qu
 
 #### Decision requests
 
+- Before every question or decision request (including approval), assume the user is coming in blind, with none of the session's context. Give the context, implications and risks in roughly one line each before asking; this is necessary context, not filler. Link an existing file with more detail when available. Never create a file just to link it. If no existing file has the detail, say so plainly.
 - Never ask what can be self-answered. Three-way gate before surfacing anything: (a) answer findable in the artifacts/code/own capability: resolve it and report, never ask; (b) genuinely the user's decision (taste, scope, priorities, destructive or outward actions): ask EXACTLY ONE clear plain-English question with a recommendation; (c) neither (speculative, non-actionable): do not raise it.
 - No hedging: no half-formed "one nuance worth flagging" offers that are neither a committed action nor a clear question.
 - Present decisions ONE at a time, never as a batched table of terms. Each option must be self-sufficient: define the term, state concretely what each value would DO and why it matters, give an example, and include a recommendation.

Full new evidence file .dev/tasks/to-do/TASK-WF-issueSummary-20261126-044758/artifacts/T1-review.md:
start=039276ff7288e6f0a5e0afcb0d518a366881d8ae tree=pending

T1.AC1: {{RF_PLACEHOLDER:ac1}}
T1.AC2: {{RF_PLACEHOLDER:ac2}}
T1.AC3: {{RF_PLACEHOLDER:ac3}}
T1.AC4: {{RF_PLACEHOLDER:ac4}}

## Sample approval with existing detail

Illustrative wording only, not an actual approval request or authorization:

Context: The proposed question rule is described in the existing [implementation plan](../TASK-WF-issueSummary-20261126-044758.md).
Implications: Approving it would let implementation add context before questions without changing who decides.
Risk: Static wording checks cannot guarantee every future response follows the rule.
Do you approve that scope? I recommend yes because it addresses the missing context without changing other behavior.
Yes: implementation proceeds within the plan. No: implementation stays paused.

## Sample question without existing detail

Illustrative preference question, not a real decision needed for this task:

Context: A hypothetical personal notification can appear each morning or only after a failure; no existing file has more detail about this preference.
Implications: A morning notification gives a daily reminder; failure-only notifications stay quiet unless something needs attention.
Risk: Daily reminders can become noise; failure-only notifications provide no routine reassurance.
Which notification schedule do you prefer? I recommend failure-only so each notification is actionable.
Morning: you receive a daily reminder even when nothing fails. Failure-only: you hear only when a failure needs attention.

## Sample assessment

Both samples put context, implications and risk before exactly one question, provide a recommendation, and state the effect of each answer. The approval links the already-existing plan; the preference sample explicitly states the lack of an existing detail file and creates none. These samples exercise the requested wording only. They do not establish live model compliance. Independent task QA fills the AC marks above.

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:40:07Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-758
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-758
call codegraph only when index_state: fresh, never to widen scope
Grep/Read floor: style consumers are the existing style-content and installer tests; hook reads the whole installed style. No symbol signatures changed.
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
