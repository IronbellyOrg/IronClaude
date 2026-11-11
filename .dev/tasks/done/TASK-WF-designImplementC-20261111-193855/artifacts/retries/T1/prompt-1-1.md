4323e33a77f71a38ec771e1c8d49b402fcd66822
Review one task for spec compliance.

Task brief: ## Task 1: Add the codegraph section to the implement command file

Edit `src/superclaude/commands/implement.md`. In the frontmatter add the line `mcp-servers: [codegraph]` after `complexity: standard`. Add a short `## Codegraph` section before `## Boundaries`. It states: the protocol runs exactly one codegraph readiness check per run (Wave 0 of the protocol skill, rules in `~/.claude/CODEGRAPH.md`); codegraph is used only when `index_state` is `fresh`, for pre-edit context (definitions, callers, impact of the symbols a task touches) and for the per-task check that the change reached every dependent; otherwise the run continues on Grep/Read and records a `graph:*` note in `codegraph.md`; codegraph never causes a STOP. Under `**Will Not:**` in Boundaries add a bullet: run `codegraph init`, `codegraph index` or `codegraph sync`. Do not change any flag, option row, STOP behaviour or the Activation block.

Acceptance criteria:
- `src/superclaude/commands/implement.md` frontmatter contains `mcp-servers: [codegraph]` and still parses as YAML with the original `name`, `description`, `category`, `complexity` and `argument-hint` values unchanged.
- The `## Codegraph` section names one readiness check per run, the fresh-only rule, the Grep/Read floor with a recorded `graph:*` note, and that it never STOPs; it points to `~/.claude/CODEGRAPH.md` and contains no `src/superclaude` path.
- The Boundaries `Will Not` list names `codegraph init`, `index` and `sync`; the Options table, Usage block and Activation block are byte-identical to before.


AC ids, in source order of the Acceptance criteria bullets: T1.AC1 (first bullet), T1.AC2 (second bullet), T1.AC3 (third bullet).
Global constraints: ## Constraints

- Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking, minor, note, the four checklist answers, the verdict order), retry ladder and managed-package rule of /sc:implement. Add no new `E-*` code.
- The reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` stays closed with exactly seven slots (task_brief, global_constraints, diff, start_sha, prior_findings, delta_diff, recheck_list); codegraph context reaches the reviewer only through the content of the existing `{diff}` slot.
- Graph notes never go into the ledger notes file (it would add a `notes@` token and change the inline-review rule); they go to one run file named `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`).
- Installed primitives never tell an agent to read a `src/superclaude/...` path; the usage guide is named only as `~/.claude/CODEGRAPH.md`.
- The tool allowlist names exact `mcp__codegraph__codegraph_<tool>` entries, never a wildcard. Never call `codegraph_explore`, `codegraph init`, `codegraph index`, `codegraph sync`, or CLI `codegraph status` while an init or index runs.
- Edit only `src/superclaude/commands/implement.md` and files under `src/superclaude/skills/sc-implement-protocol/`; do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, and do not stage `.claude/`.
Start sha: 4323e33a77f71a38ec771e1c8d49b402fcd66822
Diff against the start snapshot: diff --git a/src/superclaude/commands/implement.md b/src/superclaude/commands/implement.md
index 7b6fe6b31..883ce4d26 100644
--- a/src/superclaude/commands/implement.md
+++ b/src/superclaude/commands/implement.md
@@ -3,6 +3,7 @@ name: implement
 description: "Middleweight spec executor — walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger"
 category: workflow
 complexity: standard
+mcp-servers: [codegraph]
 argument-hint: "<path-or-prompt> [--resume] [--ledger <path>] [--skip-final-review]"
 ---
 
@@ -82,11 +83,16 @@ Do NOT proceed with protocol execution using only this command file.
 The full behavioral specification is in the protocol skill at
 `~/.claude/skills/sc-implement-protocol/SKILL.md`.
 
+## Codegraph
+
+The protocol skill runs exactly one codegraph readiness check per run (Wave 0; rules in `~/.claude/CODEGRAPH.md`). Only when `index_state` is `fresh` does the run use codegraph, for pre-edit context (definitions, callers and impact of the symbols a task touches) and for the per-task check that the change reached every dependent. Otherwise the run continues on Grep/Read and records a `graph:*` note in `codegraph.md` next to the ledger. Codegraph never causes a STOP.
+
 ## Boundaries
 
 **Will Not:**
 
 - Invent scope beyond the given source
+- Run `codegraph init`, `codegraph index` or `codegraph sync`
 - Treat a bare `/sc:implement` with no path and no prompt as a source
 - Treat lint or tests as the pass/fail
 - Invoke `/task` or `/sc:task`
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
