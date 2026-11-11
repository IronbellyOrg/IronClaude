a297a78f9baa19177f2f8735cf2ad11d046b8cb5
Review one task for spec compliance.

Task brief: ## Task 2: Add the codegraph section to the command file workflow.md

Depends on: Task 1

Edit `src/superclaude/commands/workflow.md` as specified in `./source.md` section 3.1, keeping the frontmatter (including `mcp-servers: []`), the options table, the Activation section and the `## Unattended mode` section unchanged. Add one sentence to Behavioral Summary (one codegraph readiness check per run, owned by the protocol; a fresh index grounds the plan and the pre-check, otherwise Grep/Read with a recorded note). Add a short `## Codegraph grounding` section before `## Unattended mode` that states the single readiness rule and points to `~/.claude/CODEGRAPH.md` section 2, carries the tool-to-step table (Wave 1, Wave 2, Wave 4 pre-check, matching Task 1), the fallback rule (any state other than `fresh`, or a failing lookup, means Grep/Glob/Read plus the matching `graph:*` token in `<pkg>/artifacts/codegraph-grounding.md`, never a STOP or gate), the `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switch (`graph:disabled`), and that `--unattended` applies the same rules with no gate and no person-mode flag. Extend the `Will:` line in Boundaries with grounding the plan in the real code through codegraph when the index is fresh; leave `Will Not:` unchanged.

Acceptance criteria:
- [T2.AC1] `src/superclaude/commands/workflow.md` states exactly one codegraph readiness check per run and lists which codegraph tool serves which step, consistent with the SKILL.md table from Task 1.
- [T2.AC2] The file states codegraph is used only when `index_state` is `fresh`, otherwise Grep/Glob/Read with a recorded note, and never halts.
- [T2.AC3] `mcp-servers: []`, `Skill sc:workflow-protocol`, every flag row, the banned-flag line and the `## Unattended mode` section are byte-identical to the version before the edit (`git diff src/superclaude/commands/workflow.md` shows only added lines plus the one changed Boundaries `Will:` line).
- [T2.AC4] `grep -n 'src/superclaude' src/superclaude/commands/workflow.md` prints no new read-instruction line.
- [T2.AC5] `uv run pytest tests/commands/test_workflow_command.py tests/skills/test_worker_contract.py -k "not plugin_mirror"` passes.


Global constraints: 
- Edit only `src/superclaude/skills/sc-workflow-protocol/SKILL.md`, `src/superclaude/commands/workflow.md` and, because `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` pins them byte for byte, the two matching files under `plugins/superclaude/`. Do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or any file another session owns.
- Cite only the installed guide `~/.claude/CODEGRAPH.md`; add no instruction that tells an agent to read a `src/superclaude/...` path.
- Keep `mcp-servers: []` and `Skill sc:workflow-protocol` in the command file, the template reference `refs/00_mdtm_template_simple_task.md` in SKILL.md, the Wave 3, 4, 5 order, and the `## Unattended mode` section and `refs/return-contract.md` wording that `tests/skills/test_worker_contract.py` parses.
- No commit, no push, no pull request, no `git add` of any `.claude/` path.


Start sha: a297a78f9baa19177f2f8735cf2ad11d046b8cb5
Diff against the start snapshot:
diff --git a/src/superclaude/commands/workflow.md b/src/superclaude/commands/workflow.md
index d7deb2033..c70d6074c 100644
--- a/src/superclaude/commands/workflow.md
+++ b/src/superclaude/commands/workflow.md
@@ -47,6 +47,7 @@ Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and t
 ## Behavioral Summary
 
 Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves. Final generation step (after the gate, before any handoff): advisory `/sc:reflect --mode pre` of the plan against the source; its report path/status is printed and recorded in `return-contract.yaml`.
+The protocol runs one codegraph readiness check per run: a fresh index grounds the plan and that pre-check in the real code, otherwise Grep/Read do and the fallback is recorded.
 
 ## Activation
 
@@ -63,6 +64,19 @@ The full behavioral specification is in `~/.claude/skills/sc-workflow-protocol/S
 /sc:workflow "add logout to the header" --handoff none
 ```
 
+## Codegraph grounding
+
+One codegraph readiness check per run, owned by the protocol (`~/.claude/CODEGRAPH.md` section 2, run at the start of Wave 1); this command never repeats it. Codegraph is used only when `index_state` is `fresh`. In any other state, or when a lookup fails, Grep, Glob and Read do the same job and the matching `graph:*` token is recorded in `<pkg>/artifacts/codegraph-grounding.md`. It never stops the run, fails the gate or changes the package status. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` is honoured (`graph:disabled`).
+
+| Step | Codegraph tool when fresh | Floor |
+|------|---------------------------|-------|
+| Wave 1, step 0 | `codegraph_status` (the readiness check) | guarded CLI `status`, else the floor |
+| Wave 1 | `codegraph_search`, `codegraph_node` with `symbolsOnly:true`: resolve the files and symbols the source names | Glob, Grep, Read |
+| Wave 2 | `codegraph_node` with `includeCode:true`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`: name real callers and dependents in tasks and acceptance criteria, order and size tasks by blast radius | Grep with a word-boundary pattern, then Read |
+| Wave 4 pre-check | the same lookups, read-only | the same floor |
+
+Under `--unattended` the same rules apply; no gate and no person-mode flag is added. The protocol (`~/.claude/skills/sc-workflow-protocol/SKILL.md`) holds the details.
+
 ## Unattended mode
 
 The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:workflow` resolves itself.
@@ -77,7 +91,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 
 ## Boundaries
 
-**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`.
+**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh.
 
 **Will Not:** mutate product code; edit the plan from reflect findings; emit `tasklist-index.md`; run `superclaude roadmap`.
 

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
