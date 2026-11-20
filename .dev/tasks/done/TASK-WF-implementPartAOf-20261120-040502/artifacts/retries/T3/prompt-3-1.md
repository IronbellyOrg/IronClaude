814e1014433044c960a1d14676d831688c21e3e8
Review one task for spec compliance.

Task brief: Task 3: Document the file in the claim text and test the docs

Depends on: Task 1

In `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, in the Wave 8 paragraph that describes the launch JSON, add one sentence: the script also writes that same JSON, with `terminal`, `layers` and `release`, to `<D>/launch-result.json` for a `launched` and a `failed` result (never for `already_launched`; a later `failed` result replaces an earlier file), best-effort, so a script can read it instead of the agent's text; the file is separate from the pending record and the `launch` entry of `worktree.json`, which a refusal still does not write (this keeps the paragraph's "no agent and no launch record" wording true). In the same file, in the Wave 7 sentence that says the script never copies `worktree.json` into the worktree (line 104), make it say it never copies `launch-result.json` either. In `src/superclaude/skills/sc-issue-protocol/SKILL.md`, in the Return contract section next to the `enforcement_hook` and `launch_status` text, add one sentence naming `<D>/launch-result.json`, saying it holds the full launch JSON of a `launched` or `failed` launch (never of `already_launched`) and that the agent's printed text is not the machine record. In `src/superclaude/commands/issue.md` add `launch-result.json` (the full launch JSON of a launched or failed launch; never copied into the worktree; not written for `--pipeline none`) to the claim row of the file inventory (line 80). Add a test to `tests/skills/test_issue_protocol.py` beside `test_st9_final_output_lists_the_launch_results_and_every_launch_code` that asserts `launch-result.json` appears in `claim.md` and `SKILL.md`, and that in each the line naming it also contains `launched` and `failed`; add an assertion to `test_claim_outputs_and_examples_cover_the_new_flags` in `tests/commands/test_issue_command.py` (line 169) that the claim row names `launch-result.json`.

Acceptance criteria:
- T3.AC1: `claim.md`, `SKILL.md` and the claim row of `commands/issue.md` each name `launch-result.json`, and no distributable file names a `src/superclaude/` path for it (check with `grep -rn --include='*.md' --include='*.py' 'src/superclaude' src/superclaude/skills/sc-issue-protocol src/superclaude/commands/issue.md`, which must show no new line).
- T3.AC2: `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py` passes, including the new test and the new assertion, and `test_st9_final_output_lists_the_launch_results_and_every_launch_code` still passes.
Global constraints: Edit distributable files only under `src/superclaude/` and tests under `tests/`; then run `make sync-dev` and `make verify-sync`. The `.claude/` copies are never staged, and no installed primitive may name a `src/superclaude/` path. The file is best-effort: a failed write never changes the JSON the `launch` subcommand prints, and the existing launch JSON keys keep their names and values. Part B (session-gov.sh, observation runbook, superclaude install, live OB-H2 rerun) and a verbatim-print rule for the claiming agent are out of scope.
Start sha: 814e1014433044c960a1d14676d831688c21e3e8
Diff against the start snapshot: The change is in the worktree at /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Produce it with `git diff 814e1014433044c960a1d14676d831688c21e3e8 -- src tests` (changed files: src/superclaude/skills/sc-issue-protocol/refs/claim.md, src/superclaude/skills/sc-issue-protocol/SKILL.md, src/superclaude/commands/issue.md, tests/skills/test_issue_protocol.py, tests/commands/test_issue_command.py; no untracked product files). Codegraph context: index_state: fresh, checked_at: 2026-11-20T04:06:49Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-691-launch-result. Call codegraph only when index_state: fresh, never to widen scope.
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
