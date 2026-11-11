efba21196835b598e92352b9048f095870185cd1
Review one task for spec compliance.

Task brief: ## Task 2: Add frontmatter, pointer and the one readiness check to the protocol skill

Edit `src/superclaude/skills/sc-implement-protocol/SKILL.md`. Extend the `allowed-tools` line (currently `Read, Grep, Glob, Edit, Write, Bash, Task, Skill`) by appending the exact entries `mcp__codegraph__codegraph_status`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_callees`, `mcp__codegraph__codegraph_impact` (the set `src/superclaude/skills/sc-reflect-protocol/SKILL.md` allows for codegraph). After the frontmatter add an HTML comment block headed `Extended metadata (for documentation, not parsed):` with `mcp-servers: [codegraph]`, as the reflect and troubleshoot protocol skills do. After the intro paragraph add one line: codegraph usage rules are in `~/.claude/CODEGRAPH.md`, read once per run. In Wave 0 add a step 9 after the existing step 8 (optional auggie) that runs the `~/.claude/CODEGRAPH.md` section 2 readiness check exactly once per run, before the first Q0, and keeps the result as the run state: `index_state`, `access`, `checked_at`, `worktree_root`, `projectPath`. The step also states: a resume is a new run with its own single check; there is no second check after the first product write, the state stays as recorded at `checked_at`, and graph rows about files this run changed are leads confirmed by Grep/Read; a later codegraph call that reports not indexed, foreign index or an error adds the matching token and keeps the rest of the run on the floor without a re-check; an `index_state` other than `fresh`, or `access: none`, means no codegraph call this run and the matching closed-list `graph:*` token; print one line `codegraph: index_state=<state> access=<access> checked_at=<ts>` (plus the token when degraded); write the state and every token to `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`), appending one line per later token; the check never halts the run and adds no STOP code. State that the existing `sc:impact-protocol` delegations at Q1 and Q6 are unchanged and run their own readiness inside that skill, which this protocol does not count as a second check of its own.

Acceptance criteria:
- The `allowed-tools` line of `src/superclaude/skills/sc-implement-protocol/SKILL.md` still lists `Read, Grep, Glob, Edit, Write, Bash, Task, Skill` and adds exactly the six `mcp__codegraph__codegraph_*` names above, with no wildcard; the file's frontmatter still parses.
- The extended-metadata comment lists `mcp-servers: [codegraph]` and the file points to `~/.claude/CODEGRAPH.md` without a `src/superclaude` read path.
- Wave 0 step 9 states one readiness check per run, the five run-state fields, the no-re-check-after-write rule, the not-fresh behaviour with a `graph:*` token, the `codegraph.md` record location for legacy and managed runs, and that it never halts; the STOP table has no new row.


AC ids, in source order of the Acceptance criteria bullets: T2.AC1 (first bullet), T2.AC2 (second bullet), T2.AC3 (third bullet).
Global constraints: ## Constraints

- Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking, minor, note, the four checklist answers, the verdict order), retry ladder and managed-package rule of /sc:implement. Add no new `E-*` code.
- The reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` stays closed with exactly seven slots (task_brief, global_constraints, diff, start_sha, prior_findings, delta_diff, recheck_list); codegraph context reaches the reviewer only through the content of the existing `{diff}` slot.
- Graph notes never go into the ledger notes file (it would add a `notes@` token and change the inline-review rule); they go to one run file named `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`).
- Installed primitives never tell an agent to read a `src/superclaude/...` path; the usage guide is named only as `~/.claude/CODEGRAPH.md`.
- The tool allowlist names exact `mcp__codegraph__codegraph_<tool>` entries, never a wildcard. Never call `codegraph_explore`, `codegraph init`, `codegraph index`, `codegraph sync`, or CLI `codegraph status` while an init or index runs.
- Edit only `src/superclaude/commands/implement.md` and files under `src/superclaude/skills/sc-implement-protocol/`; do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, and do not stage `.claude/`.
Start sha: efba21196835b598e92352b9048f095870185cd1
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/SKILL.md b/src/superclaude/skills/sc-implement-protocol/SKILL.md
index bc52429fd..f7d6b68de 100644
--- a/src/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -1,13 +1,19 @@
 ---
 name: sc:implement-protocol
 description: "Middleweight spec executor; spec/PRD/tasklist, informal notes, or inline prompt; per-task spec-compliance QA; one-file ledger"
-allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, Skill
+allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, Skill, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
 ---
 
+<!-- Extended metadata (for documentation, not parsed):
+mcp-servers: [codegraph]
+-->
+
 # /sc:implement protocol
 
 Middleweight executor. Source is a spec/PRD/tasklist path, an informal notes file, or an inline prompt. Walk enumerable tasks (informal/prompt → one task). After each task, spec-compliance QA against **that task's** AC + parent spec + instructions. Lint/tests are extras, never the verdict. One markdown ledger.
 
+Codegraph usage rules (readiness check, closed `graph:*` token list, call-site procedure) are in `~/.claude/CODEGRAPH.md`; read it once per run.
+
 Load `refs/qa.md` for Q3–Q5. Load `refs/ledger.md` for ledger I/O and resume. Also load `refs/retry.md` when A2 (the Q5 fix pass) still fails review, or when resume finds a `retry` or `halt` record in the ledger. Do not load reflect-protocol. Do not invoke `/task`, `/sc:task`, or `sc:task-protocol`.
 
 **Managed packages.** If Wave 0 step 3 finds a `workflow-plan/1.2` plan (a workflow-owned `TASK-WF-*` package), also load `refs/managed-workspace.md`: it replaces the ledger location, resume dispatch, whole-list review and completion rules for that run only. Every other source runs the legacy rules below, unchanged.
@@ -65,6 +71,12 @@ E-LEGACY copy: `Removed flags: --type/--framework/--safe/--with-tests. Pass a sp
 6. Open or create ledger (header first, before any product edit). Resume per `refs/ledger.md`. Truncated last line → `E-LEDGER-CORRUPT`.
 7. If N≥20 print **once**: `N tasks; compaction likely; ledger is the source of resume.` Do not STOP. Do not split.
 8. Optional auggie before significant edits; unavailability is a warning, not a STOP.
+9. **Codegraph readiness: exactly one check per run**, after step 8 and before the first Q0. Run the `~/.claude/CODEGRAPH.md` section 2 check once and keep the result as the **run state**: `index_state`, `access`, `checked_at`, `worktree_root`, `projectPath`.
+   - A resume is a new run and does its own single check. There is no second check after the first product write: the state stays as recorded at `checked_at`, and graph rows about files this run changed are leads, confirmed by Grep/Read before they are cited or drive an edit. A later codegraph call that reports not indexed, foreign index or an error adds the matching `graph:*` token and keeps the rest of the run on the Grep/Read floor, with no re-check.
+   - `index_state` other than `fresh`, or `access: none`: no codegraph call this run; the floor (Grep, Glob, Read) serves every step below; add the matching token from the closed list in `~/.claude/CODEGRAPH.md` section 3.
+   - Print one line: `codegraph: index_state=<state> access=<access> checked_at=<ts>`, plus the token when degraded.
+   - Record the run state and every `graph:*` token in `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`; managed `<pkg>/artifacts/codegraph.md`), appending one line per later token. This file is not the ledger and not a task notes file: it adds no `notes@` token and changes no inline-review rule.
+   - The check never halts the run, never changes a verdict and adds no STOP code. The existing `sc:impact-protocol` delegations at Q1 and Q6 are unchanged: they run their own readiness inside that skill, and this protocol does not count that as a second check of its own.
 
 ### Enumerable tasks
 
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
