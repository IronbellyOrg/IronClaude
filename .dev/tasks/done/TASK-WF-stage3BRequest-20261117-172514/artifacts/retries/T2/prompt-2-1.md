20b754eb1c0dd9fa215ff9616c158ea57e03acb6
Review one task for spec compliance.

Task brief: ## Task 2: Sync the dev copies of the edited agent and record the final run

Depends on: Task 1

Run `make sync-dev` so `.claude/agents/reflect-reviewer.md` follows `src/superclaude/agents/reflect-reviewer.md`, then `make verify-sync`, then the four test files of Task 1 once more after this last edit. Write the pass counts and the `make verify-sync` result to `./artifacts/stage3b-final-run.md`. Do not stage anything under the project `.claude/` folder, and edit no retired carrier.

Acceptance criteria:
- `make verify-sync` passes.
- `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes, and `./artifacts/stage3b-final-run.md` holds the observed pass counts and the `make verify-sync` result.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`, and `git status --porcelain -- src plugins` lists none of the retired carriers (`src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md`) and lists only `src/superclaude/agents/reflect-reviewer.md` among `src` and `plugins` files.
Global constraints: ## Constraints

- This is stage 3b: it runs after the stage 3 package `TASK-WF-blockerStage3-20261116-030158` (in the done subfolder of the repository task folder, `FINAL: pass`) and before the held stage 4 package. The owner's go to run it is a chat message recorded in the stage ledger `stage-requests/README.md` of the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115`; no task here is an owner gate. The re-run of the five throwaway review runs against the fixed agent is read by the owner and is not a task of this package.
- Why this package exists: in the five throwaway review runs of 2026-11-17 the reflect reviewers' cards labelled two real blockers (findings M6 and B2) Medium. The agent grades only on its own HIGH, MEDIUM, LOW scale and holds no consequence rule (`.dev/throwaway-medium-runs-20261117/B/RUN-RECORD.md` lines 175 to 176 and `E/RUN-RECORD.md` line 69). Run B records that the orchestrator pasted the rule into the briefs; run E records that nothing was pasted and that where the reviewers got the blocking wording is unverified. Without a paste, a reviewer has only the agent's own scale.
- The three bullets S1, S2 and S3 are copied exactly as `canonical_rule_bullets()` in `tests/skills/test_review_severity_rule.py` returns them (the helper reads them from `src/superclaude/output-styles/pragmatic.md`); copy the text, never retype it. S4 and S5 are not copied: the agent's own new bullet replaces what S5 says for a HIGH, MEDIUM, LOW scale.
- Not edited here, recorded so the exclusions are decisions: `skills/sc-reflect-protocol` and its adversarial merge (whether the merged card needs the rule is not checked here); the Correctness gaps section, the Behavioral Mindset and the "Soften a real deviation to close enough" bullet of `reflect-reviewer.md`; `src/superclaude/agents/evidence-validator.md`; `src/superclaude/skills/sc-implement-protocol/refs/qa.md` and the own-scale primitives; `src/superclaude/cli/**/*.py`; the cap of 2 fix cycles; any plugin surface; the stale "ten-file set" wording in `docs/developer-guide/review-severity-rule.md` (lines 92 and 112). No new question is added to any command. No Jev call.
- Retired carriers are not edited: `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md`.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; do not stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked).
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Acceptance checks are by content and quote the sentence they protect; line numbers in a task body are hints, each place is re-read by its text before editing.
- Task-owned evidence goes under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says that `.dev/tasks/` is excluded from staging. Staging is not committing.
Start sha: 20b754eb1c0dd9fa215ff9616c158ea57e03acb6
Diff against the start snapshot: === new file (no earlier version in the start snapshot): .dev/tasks/to-do/TASK-WF-stage3BRequest-20261117-172514/artifacts/stage3b-final-run.md (shown with line numbers)
     1	# Stage 3b final run (2026-11-17)
     2	
     3	- `make sync-dev`: exit 0 (`./artifacts/t2-sync-dev.log`).
     4	- `make verify-sync`: exit 0, last line "All components in sync." (`./artifacts/t2-verify-sync.log`).
     5	- `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -q`: 82 passed (`./artifacts/t2-pytest-four-files.log`).
     6	- Files under the project `.claude/` folder in `git diff --cached --name-only`: 0.
     7	- Retired carriers (`src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md`) edited: 0.
     8	- `git status --porcelain -- src plugins` lists only `src/superclaude/agents/reflect-reviewer.md`.
=== new file (no earlier version in the start snapshot): .dev/tasks/to-do/TASK-WF-stage3BRequest-20261117-172514/artifacts/t2-sync-dev.log (shown with line numbers)
     1	🔄 Syncing src/superclaude/ → .claude/ for local development...
     2	✅ Sync complete.
     3	   Skills:    40 directories
     4	   Agents:    48 files
     5	   Commands:  47 files
     6	   Hooks:     17 files
     7	   Templates: 52 files
=== new file (no earlier version in the start snapshot): .dev/tasks/to-do/TASK-WF-stage3BRequest-20261117-172514/artifacts/t2-verify-sync.log (shown with line numbers)
   185	  ✅ documents/release-spec-template.md
   186	  ✅ documents/supplemental_doc_template.md
   187	  ✅ documents/technical_reference_template.md
   188	  ✅ documents/readme_template.md
   189	  ✅ modularization-template-review/qa-fix-summary_template.md
   190	  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
   191	  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
   192	  ✅ modularization-template-review/research-notes_template.md
   193	  ✅ modularization-template-review/synthetic-dnsp-finding.contract
   194	  ✅ modularization-template-review/INDEX.md
   195	  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
   196	  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
   197	  ✅ modularization-template-review/track-scope-map_template.md
   198	  ✅ modularization-template-review/claim-evidence-matrix_template.md
   199	  ✅ modularization-template-review/qa-inventory_report_template.md
   200	  ✅ modularization-template-review/analyst-coverage-matrix_template.md
   201	  ✅ modularization-template-review/codebase-research_template.md
   202	  ✅ modularization-template-review/analyst-completeness_report_template.md
   203	  ✅ modularization-template-review/analyst-gap-analysis_template.md
   204	  ✅ modularization-template-review/qa-lens_report_template.md
   205	  ✅ modularization-template-review/qa-consolidated-findings_template.md
   206	  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
   207	  ✅ modularization-template-review/qa-research-gap_report_template.md
   208	  ✅ modularization-template-review/qa-research-evidence_report_template.md
   209	  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
   210	  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
   211	  ✅ modularization-template-review/analyst-cross-validation_report_template.md
   212	  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
   213	  ✅ modularization-template-review/pipeline-complete_report_template.md
   214	  ✅ modularization-template-review/qa-source-fidelity_template.md
   215	  ✅ modularization-template-review/qa-research-depth_report_template.md
   216	  ✅ modularization-template-review/web-research_template.md
   217	
   218	=== Installer Registration ===
   219	  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
   220	
   221	=== Hooks Cross-Consistency ===
   222	  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
   223	
   224	✅ All components in sync.
=== new file (no earlier version in the start snapshot): .dev/tasks/to-do/TASK-WF-stage3BRequest-20261117-172514/artifacts/t2-pytest-four-files.log (shown with line numbers)
     1	..................................                                       [100%]
     2	
     3	============================== 82 passed in 3.35s ==============================

Codegraph context
index_state: fresh
checked_at: 2026-11-17T17:34:18Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none; this task changes no symbol. make sync-dev writes only the gitignored .claude/ copies. Current state to check against the acceptance criteria: git status --porcelain -- src plugins lists only src/superclaude/agents/reflect-reviewer.md (a Task 1 file); git diff --cached --name-only lists no .claude/ path (the orchestrator ran both and recorded 0). The diff above shows only evidence files; you may read the live repo and the logs under the package ./artifacts/ (the package folder is .dev/tasks/to-do/TASK-WF-stage3BRequest-20261117-172514/; its retries folder is off limits).
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
