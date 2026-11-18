329f052078ce2471d376d3077cd06ee5ca1860ce
Review one task for spec compliance.

Task brief: ## Task 1: Replace the Feature, simple row in the chain table
In `src/superclaude/skills/sc-issue-protocol/refs/chains.md`, change only the table row that starts `| Feature, simple |`. Keep its tier line `/model claude-gw-tier2`. Replace its chain cell with two steps in the row's existing `<br>` style: the first runs `/sc:workflow <S> --depth quick --handoff none` (`<S>` is the issue-summary path the file already defines), the second runs `/sc:implement <plan path printed by step 1>`. Under `Notes:` add one bullet saying the simple feature row has no brainstorm step because the issue summary already states the requirements, so it plans directly from it. Leave the other five rows and the paragraph about handoff flags unchanged.
Acceptance criteria (ids):
T1.AC1: The `Feature, simple` row contains no `/sc:brainstorm` and exactly the two commands above; the other five rows are byte-identical to before.
T1.AC2: Because the first `/sc:implement` step is now step 2, the plan boundary for this row is `after step 1`, and the `Plan boundary` rule in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5 step 3) still reads correctly.
T1.AC3: Every flag in the new commands exists in the workflow and implement command files, so `test_every_chain_flag_exists_in_its_command` in `tests/skills/test_issue_protocol.py` still passes.
Global constraints: ## Constraints
- Edit only source files: `src/superclaude/...`, `tests/...`, `docs/...` and the one mirror file `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Never edit or stage anything under `.claude/`; Task 10 regenerates those copies with `make sync-dev`.
- The default level applies to a bare `--claim`. The issue watcher always passes `--pipeline none` (`build_claim_prompt` in `src/superclaude/cli/issue_watch/launch.py`, pinned by `tests/issue_watch/test_launch.py`). Do not edit either file and do not add any human-versus-agent detection.
- The default level does not authorize a commit, a push or a pull request: `E-SUBMIT-NEEDS-FULL` keeps its meaning, so a `--submit` with no `--pipeline` still stops and `--submit` needs an explicit `--pipeline full` (the design record `docs/designs/sc-issue-claim-pipeline-flag.md` line 85 already says so).
- No file under `src/superclaude/skills/sc-issue-protocol/` and not `src/superclaude/commands/issue.md` may contain the text `src/superclaude/` (`tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files` and `tests/commands/test_issue_command.py::test_no_source_tree_path` forbid it): in those files cite code by file name, never by its `src/superclaude/` path.
- New lines in command and skill files must not contain `git add`, `git commit`, `git push`, `git merge`, `gh pr` or `gh api`: `tests/skills/test_worker_contract.py` audits those verbs line by line.
- Leave the ship-gate sentences (OB-H1, OB-H2, OB-H3) and the `--pipeline none` coordinator-handoff paragraph exactly as written. The worktree `claim-handoff-planb` edits the same files (`issue.md`, `SKILL.md`, `refs/claim.md`, `HOW-WE-WORK.md`), so keep every edit narrow and rebase onto `origin/master` before any pull request.
- Out of scope: `/tech-research`, `/task-builder` and `/task` handling, the complex bug row, model tiers, `orca_worktree.py`, every other chain row, and the command version (it stays 1.1.0, which `tests/commands/test_issue_command.py` pins).
- Also out of scope, recorded on purpose: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` lines 17-19 (the coordinator path keeps its brainstorm step for simple work); the owner-run bare launch prompts in `docs/designs/issue-watcher-setup.md` lines 616-619 (a launch with them now starts at `full`; update them before reuse if a claim-only capture is wanted); and the dated records `docs/designs/issue-watcher.md` lines 41 and 48 and `docs/designs/issue-watcher-setup.md` line 575.
- Known risk, not fixed here: a person's bare `/sc:issue --claim <N>` on an issue that a coordinator already owns reuses its worktree and starts a second agent, now at `full`, because only the claim's own launch step writes the launch record (`cmd_pending` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` writes only a pending record). Do not claim such an issue without `--pipeline none`.
Start sha: 329f052078ce2471d376d3077cd06ee5ca1860ce
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/refs/chains.md b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
index 59b51b1fe..6cff1eeb3 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/chains.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
@@ -8,7 +8,7 @@ These are the default rows passed to `/sc:recommend` as the suggested route. `/s
 
 | Type / complexity | Tier line | Chain |
 |---|---|---|
-| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:brainstorm "<topic> @<S>" --depth quick` (no `--handoff`)<br>2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`<br>3. `/sc:implement <plan path printed by step 2>` |
+| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:workflow <S> --depth quick --handoff none`<br>2. `/sc:implement <plan path printed by step 1>` |
 | Feature, medium | `/model claude-gw-tier1b` | 1. `/sc:brainstorm "<topic> @<S>" --blind`<br>2. `/sc:design <brainstorm dir>/merged-requirements.md --type <architecture\|api\|component\|database> --format spec`<br>3. `/sc:workflow <design doc> --depth standard --handoff none`<br>4. `/sc:implement <plan path>` |
 | Feature, complex | `/model claude-gw-tier1b` | 1. `/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind`<br>2. `/sc:design <merged-requirements.md> --type <...> --format spec`<br>3. `/sc:workflow <design doc> --depth deep --handoff none`<br>4. `/sc:implement <plan path>` |
 | Bug, simple | `/model claude-gw-tier2` | 1. `/sc:troubleshoot "<symptom>" --depth quick --context <S> --scope <scope>`<br>2. `/sc:implement <REPORT.md path printed by step 1>` |
@@ -20,6 +20,7 @@ Notes:
 - `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
 - The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. In a ccsession tier workspace the launcher sets each `ANTHROPIC_DEFAULT_*_MODEL` for a tier the owner may use, so those aliases map to the `tier1a`, `tier1b` and `tier2` picker ids (`claude-gw-` prefix); an alias for a tier the owner may not use keeps its inherited value, and outside a tier workspace the aliases keep Claude Code's meaning (`docs/reference/model-aliases.md`). The session tier itself is pinned by the `/model` line (default D25).
 - `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.
+- The simple feature row has no brainstorm step: the issue summary already states the requirements, so the row plans directly from it with `/sc:workflow`.
 
 No brainstorm step carries a handoff flag: the tasklist handoff feeds `/sc:tasklist`, not `/sc:workflow`, and the design handoff only prints a suggestion (B11), so `/sc:workflow` and `/sc:design` run as their own steps.
 


Codegraph context
index_state: fresh
checked_at: 2026-11-18T05:09:43Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the task changes Markdown or test text, not code symbols; no dependents outside the touched set were listed.

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
