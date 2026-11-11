5feedca465f24c32f22bc35d800ae6951b16f80c
Review one task for spec compliance.

Task brief: ## Task 11: Sync the dev copies and confirm they match

Depends on: Task 10

Run `make sync-dev` then `make verify-sync` from the repository root; run the tests that cover agent files (find them with grep under tests/) with `uv run pytest`.

Acceptance criteria:
- `make verify-sync` passes, `grep -rn 'src/superclaude'` over the ten agent files shows no new hit, and the agent-file tests pass; evidence saved to ./artifacts/t11-verify.log.

AC ids: T11.AC1
Global constraints: ## Constraints

- Rule text, identical in the nine engineering agents: "For symbols, callers, callees and impact use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the caller's brief says `index_state: fresh` together with `checked_at`, `worktree_root` and the `projectPath` to pass on every call, and Read every row before citing it. Otherwise use Grep, Glob and Read, and say so in your reply." It is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md.
- These ten files declare no tools line and inherit all tools: do not add a tools line or restrict tools. Change nothing but the added rule.
- Do not reference src/superclaude/ paths inside an agent file; point at ~/.claude/CODEGRAPH.md.
- Do not edit src/superclaude/core/CODEGRAPH.md, the four agents that already carry the rule, any command or skill, or .claude/. No commit, no push.
Start sha: 5feedca465f24c32f22bc35d800ae6951b16f80c
Diff against the start snapshot: 
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
