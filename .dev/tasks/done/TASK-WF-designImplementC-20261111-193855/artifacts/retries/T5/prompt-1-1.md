10dc8dedc603c9a122b7ef7195aeef3c9106194d
Review one task for spec compliance.

Task brief: ## Task 5: Carry the run state in the retry adviser prompts

Edit `src/superclaude/skills/sc-implement-protocol/refs/retry.md`. Wherever it writes the prompt for an `implement-retry-adviser` (the adviser spawns of escalations 1 to 3 and any adviser re-spawn), require the prompt to carry the four run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath` from the run's single readiness check. State that the adviser definition lists only Read, Grep and Glob and so has no codegraph tools: its prompt tells it to use Grep and Read and to treat the run state as context only. Add one sentence that the executor's own retry attempts run Q1a and Q2b of `SKILL.md` again, and that no ladder step, halt reason, ledger record or brief file format changes.

Acceptance criteria:
- `src/superclaude/skills/sc-implement-protocol/refs/retry.md` states that every adviser prompt carries `index_state`, `checked_at`, `worktree_root` and `projectPath`, and that the adviser has no codegraph tools and stays on Grep/Read.
- The halt table, the `retry` record format, the brief file layout and every `E-*` code in `refs/retry.md` are unchanged.
- Running `uv run pytest tests/skills/test_implement_retry_revert.py tests/skills/test_implement_retry_citation.py tests/skills/test_implement_saved_prompt_rule.py tests/skills/test_implement_adviser_family.py tests/skills/test_implement_severity_static.py tests/skills/test_review_severity_rule.py tests/commands/test_impact_command.py tests/commands/test_workflow_command.py` passes.

AC ids, in source order of the Acceptance criteria bullets: T5.AC1 (first bullet), T5.AC2 (second bullet), T5.AC3 (third bullet).
Global constraints: ## Constraints

- Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking, minor, note, the four checklist answers, the verdict order), retry ladder and managed-package rule of /sc:implement. Add no new `E-*` code.
- The reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` stays closed with exactly seven slots (task_brief, global_constraints, diff, start_sha, prior_findings, delta_diff, recheck_list); codegraph context reaches the reviewer only through the content of the existing `{diff}` slot.
- Graph notes never go into the ledger notes file (it would add a `notes@` token and change the inline-review rule); they go to one run file named `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`).
- Installed primitives never tell an agent to read a `src/superclaude/...` path; the usage guide is named only as `~/.claude/CODEGRAPH.md`.
- The tool allowlist names exact `mcp__codegraph__codegraph_<tool>` entries, never a wildcard. Never call `codegraph_explore`, `codegraph init`, `codegraph index`, `codegraph sync`, or CLI `codegraph status` while an init or index runs.
- Edit only `src/superclaude/commands/implement.md` and files under `src/superclaude/skills/sc-implement-protocol/`; do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, and do not stage `.claude/`.
Start sha: 10dc8dedc603c9a122b7ef7195aeef3c9106194d
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/retry.md b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
index 364ced00b..fab0c9e36 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -68,7 +68,7 @@ Procedure step 0 runs after every failed attempt from A2 to A5 (for A5, see Esca
 
 2. **Procedure step 2, the diff.** Write `attempt-<k>.diff` = `git -C "$top" diff --no-renames "$start" <checkpoint tree> -- <every path of the checkpoint tree's revert domain, each as ':(literal)<p>'>` (the domain of The revert, computed with the checkpoint tree in place of `now`). Kept so the adviser, which has no Bash, can read the failed change. Cap the file at 256 KiB and end a cut file with the line `[truncated at 256 KiB; the full change is in the checkpoint tree until the task completes]`. On resume it is rebuilt from the recorded sha.
 
-3. **Advisers.** Spawn **before** reverting so they can read the live failed tree (model choice: Model ladder). Spawn both in one message and save both answers only after both return; neither has Write, so neither sees the other's answer. Advisers and fixers get the finding lines verbatim, never a paraphrase, with regressions first. The parent saves each answer verbatim as `advice-<n>-a.md` and `advice-<n>-b.md`, with a header naming the ladder entry used. This matches the existing read-only-agent pattern, where the agent returns its report and the orchestrator writes it. The answer contains:
+3. **Advisers.** Spawn **before** reverting so they can read the live failed tree (model choice: Model ladder). Spawn both in one message and save both answers only after both return; neither has Write, so neither sees the other's answer. Advisers and fixers get the finding lines verbatim, never a paraphrase, with regressions first. Every adviser prompt also carries the four codegraph run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath` from the Wave 0 check (`SKILL.md`, Wave 0 step 9). The `implement-retry-adviser` definition lists only Read, Grep and Glob, so the adviser has no codegraph tools: its prompt says so, tells it to use Grep and Read, and to treat the run state as context only. The executor's own attempts run Q1a and Q2b of `SKILL.md` again; no ladder step, stop reason, ledger record or brief file format changes. The parent saves each answer verbatim as `advice-<n>-a.md` and `advice-<n>-b.md`, with a header naming the ladder entry used. This matches the existing read-only-agent pattern, where the agent returns its report and the orchestrator writes it. The answer contains:
    - `outcome: ready | dispute`. `dispute` when the AC is contradictory or infeasible, or a review finding is not supported by its own citations. A `dispute` counts as one only when it names a blocking finding of `review-<k>.md` or the AC itself. A dispute of a minor or note is written to the notes file as a dispute line in the format of "Notes file" in `refs/qa.md`, and the answer is treated as `ready` for the parent check.
    - For `ready`: one row per original `Ti.ACk`: why earlier attempts missed it, and the change to make. Every citation points to a file that survives the revert: `attempt-<k>.diff:<line>`, `review-<k>.md:<line>`, `extras-<k>.log:<line>`, or a source file unchanged since the task started (the parent checks this, below).
    - `differs-by:` the single decision that differs from every earlier approach.
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
