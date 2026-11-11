2055043ac2b0735ac8724aa1569f18e90d79b107
Review one task for spec compliance.

Task brief: ## Task 3: Add the pre-edit context step and the dependents step to the Q loop

Depends on: Task 2

In `src/superclaude/skills/sc-implement-protocol/SKILL.md` add two steps to the Q0-Q8 loop block, keeping the existing step numbering and text of Q0 to Q8 otherwise intact, and add a short tool-to-step table. Q1a (before the Q1 edits): when the run state is `index_state: fresh` and `access: mcp`, for up to 5 symbols the task names or touches, locate with `codegraph_search`, read the definition with `codegraph_node {symbol, file, includeCode:true}` (file outline with `codegraph_node {file, symbolsOnly:true}`), and find who depends on it with `codegraph_callers` and `codegraph_impact` at depth 1; every call passes the run state's `projectPath`. The Grep for the definition, Read of the range, word-boundary Grep for references and Read of each call site stay as the floor and run whenever the run state is not fresh; Read before every Edit regardless; the Q1 rename/delete/signature `sc:impact-protocol` step stays as it is. Q2b (after the Q2 diff, before Q3): for up to 5 symbols whose definition, signature or behaviour the diff changed, query `codegraph_callers`, `codegraph_impact` at depth 1 and, when the change moved a call, `codegraph_callees`, and list the dependents whose file is not in the task's touched set; floor is Grep `\b<symbol>\b` plus Read of the hits. Rules for both steps: each row is confirmed by Grep plus Read of the call site before it is cited or drives an edit (the CS1 to CS5 procedure of `~/.claude/CODEGRAPH.md` section 5); at most 5 rows per symbol and 20 per run; an empty graph answer is never read as "no dependents"; a truncated list is re-queried once, then `graph:truncated` is recorded; rows about files this run changed are leads. The Q2b list is context for the reviewer, placed in the `{diff}` slot content (Task 4); it becomes a finding only through the existing four-question checklist, never edits files and never widens the touched set. The Q5 fix pass and any retry attempt run Q1a and Q2b again for the symbols they touch.

Acceptance criteria:
- `src/superclaude/skills/sc-implement-protocol/SKILL.md` contains a `Q1a` step before `Q1` and a `Q2b` step between `Q2` and `Q3`, naming `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_impact` and (for Q2b) `codegraph_callees`, each tied to its step, with the Grep/Read floor stated for each; the original text of Q0 to Q8 is otherwise unchanged.
- Both steps say codegraph runs only when the run state is `index_state: fresh`; otherwise Grep/Read runs and a `graph:*` line is appended to `codegraph.md`; neither step can halt the run or change a verdict.
- The 5-symbol, 5-rows-per-symbol and 20-rows-per-run caps, the confirm-by-Grep-and-Read rule and the "empty is not absence" rule appear in the skill text.


AC ids, in source order of the Acceptance criteria bullets: T3.AC1 (first bullet), T3.AC2 (second bullet), T3.AC3 (third bullet).
Global constraints: ## Constraints

- Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking, minor, note, the four checklist answers, the verdict order), retry ladder and managed-package rule of /sc:implement. Add no new `E-*` code.
- The reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` stays closed with exactly seven slots (task_brief, global_constraints, diff, start_sha, prior_findings, delta_diff, recheck_list); codegraph context reaches the reviewer only through the content of the existing `{diff}` slot.
- Graph notes never go into the ledger notes file (it would add a `notes@` token and change the inline-review rule); they go to one run file named `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`).
- Installed primitives never tell an agent to read a `src/superclaude/...` path; the usage guide is named only as `~/.claude/CODEGRAPH.md`.
- The tool allowlist names exact `mcp__codegraph__codegraph_<tool>` entries, never a wildcard. Never call `codegraph_explore`, `codegraph init`, `codegraph index`, `codegraph sync`, or CLI `codegraph status` while an init or index runs.
- Edit only `src/superclaude/commands/implement.md` and files under `src/superclaude/skills/sc-implement-protocol/`; do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, and do not stage `.claude/`.
Start sha: 2055043ac2b0735ac8724aa1569f18e90d79b107
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/SKILL.md b/src/superclaude/skills/sc-implement-protocol/SKILL.md
index f7d6b68de..e16a23b8b 100644
--- a/src/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -127,6 +127,7 @@ Q0 START   If AC QUALIFY fails → E-NO-AC (do not reach Q1).
            If write-tree fails, `start=$(git rev-parse HEAD 2>/dev/null)` (HEAD is already a ref). If that fails, `nogit`. Write the start line once with that 40-hex (or `nogit`).
            On task `complete`, delete the Q0 pin `git update-ref -d "refs/superclaude/implement/<slug>/T<id>"` and the task's checkpoint refs (`refs/retry.md`); keep its sweep refs. The final summary lists each kept sweep ref with one `git update-ref -d <ref>` line for the operator. The task's reviewed-tree refs `retry/T<rid>/r<k>-<j>` (`refs/qa.md`) are deleted at `complete` once `first=` and `origin=` are written; sweep refs are kept.
            Read Ti text + AC ids + global constraints.
+Q1a CONTEXT Before the first edit, load context for up to 5 symbols the task names or touches. Run state `index_state: fresh` and `access: mcp` (Wave 0 step 9): `codegraph_search` to locate each, `codegraph_node {symbol, file, includeCode:true}` for its definition (`codegraph_node {file, symbolsOnly:true}` for a file outline), `codegraph_callers` and `codegraph_impact` at depth 1 for who depends on it; every call passes the run state's `projectPath`. Floor, always the fallback and always the Read before an Edit: Grep for the definition, Read the range, Grep `\b<symbol>\b` for references, Read each call site. Not fresh → floor only, and append the `graph:*` line to `codegraph.md`. Context only: it never widens the task, changes the AC, changes a verdict or halts.
 Q1 EXEC    Implement only that task. Touched files = paths this task created or modified via Write, Edit, or Bash (product paths, not the ledger).
            A drive-by file not implied by the AC is blocking only when a confirmed `quoted-constraint-breach` or `harmful-effect` applies; otherwise it is a minor that stays in `files=` and goes to notes.
            Rename, delete or signature-change task: before the first edit, for each symbol it renames, deletes or re-signs, invoke
@@ -135,6 +136,7 @@ Q1 EXEC    Implement only that task. Touched files = paths this task created or
 Q2 DIFF    `git diff "$start"` (tree-ish vs worktree — not `..WORKTREE`, which is not a Git revision).
            Scope to Ti touched files when possible. This is the increment since Q0, including uncommitted prior-task files only if they were edited again.
            Untracked files in the touched set are part of the review package: if the path exists in `$start`, diff vs `git show "$start:<path>"`; else include full new-file contents (`git diff --no-index -- /dev/null <file>` or Read). Do not `git add` to the user index for this snapshot (that is not the `.dev/tasks/` rule: `.dev/tasks/` is always staged, `git add .dev/tasks`). An empty `git diff` with new untracked writes is not `cannot-verify`.
+Q2b DEPENDENTS For up to 5 symbols whose definition, signature or behaviour the diff changed, list the dependents whose file is not in the task's touched set. Run state fresh: `codegraph_callers`, `codegraph_impact` at depth 1 and, when the change moved a call, `codegraph_callees` (rows about files this run changed are leads). Floor: Grep `\b<symbol>\b` over the repo and Read the hits. Not fresh → floor only, and append the `graph:*` line to `codegraph.md`; Q2b never halts the run and never changes a verdict. The list goes into the `{diff}` slot content with the run state (`refs/qa.md`); it is context for the reviewer, never an edit, never a wider touched set, and a finding only through the existing four-question checklist.
 Q3 REVIEW  Load refs/qa.md. Reviewer (not the implementer voice) fills:
              - For each Ti.ACk: met | unmet + citation
              - finding lines with the four checklist answers and one anchor per `yes` (`refs/qa.md`)
@@ -149,6 +151,20 @@ Q8 NEXT    Only if complete (compliant, or non-compliant plus operator Ruling).
 
 A 1-task source still runs Q0–Q8 once (inline). Skip the end-of-list second pass.
 
+### Codegraph by step
+
+Codegraph runs only when the Wave 0 run state is `index_state: fresh` with `access: mcp`; every step keeps its Grep/Read floor, which also runs whenever codegraph is not used. The Q5 fix pass and each retry attempt repeat Q1a and Q2b for the symbols they touch.
+
+| Step | Job | Codegraph tools | Floor |
+|---|---|---|---|
+| Wave 0 step 9 | the one readiness check | `codegraph_status` (CLI form per `~/.claude/CODEGRAPH.md`) | none needed: record the `graph:*` token |
+| Q1a | definitions, callers, blast radius before the edit | `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_impact` | Grep, Read |
+| Q1 rename/delete/signature | dependent counts | `sc:impact-protocol`, unchanged | its own floor |
+| Q2b | did the change reach every dependent | `codegraph_callers`, `codegraph_impact`, `codegraph_callees` | Grep `\b<symbol>\b`, Read |
+| Q6 advisory tests | test list | `sc:impact-protocol`, unchanged | extras run as before |
+
+Rules for every row: confirm each row by Grep plus Read of the call site before it is cited or drives an edit (the CS1 to CS5 procedure of `~/.claude/CODEGRAPH.md` section 5); at most 5 rows per symbol and 20 per run; an empty graph answer is never read as "no dependents"; a truncated list is re-queried once with a higher limit, then `graph:truncated` is recorded. Never call `codegraph_explore`, `codegraph init`, `codegraph index` or `codegraph sync`.
+
 ### Extras (after verdict, never the gate)
 
 Detect in repo root, run what exists, skip the rest. Do not install tools. No extras flag.
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
