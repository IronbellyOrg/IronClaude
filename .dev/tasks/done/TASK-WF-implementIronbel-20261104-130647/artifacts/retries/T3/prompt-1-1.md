511d1613f5132780c1630910f26d78b168b7959a
Review one task for spec compliance.

Task brief: Task T3 of plan /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md (lines 69-82), verbatim:
## Task 3: Register the hook and add it to the installer list

Depends on: Task 1

In `src/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/hooks.json`, add one `PreToolUse` registration after the existing `Edit|Write` freshness entry: `{"matcher": "Bash", "hooks": [{"type": "command", "command": "~/.claude/hooks/block-bare-python.sh", "timeout": 3}]}`. Change nothing else in either file.

In `src/superclaude/cli/install_hooks.py`, add `"block-bare-python.sh"` to `_FRESHNESS_SCRIPTS` with a short comment (PreToolUse `Bash` UV-only gate, issue #357, fails open, blocks with exit 2), so `_copy_scripts` installs it to `~/.claude/hooks/` and `make verify-sync`'s installer-registration check stays green.

Run `make sync-dev` so `.claude/hooks/block-bare-python.sh` exists for development (not staged).

Acceptance criteria:
- Both `hooks.json` files parse with `jq .` and contain exactly one PreToolUse entry whose command is `~/.claude/hooks/block-bare-python.sh`, with matcher `Bash` and timeout 3; `git diff` of both files shows only that addition.
- `"block-bare-python.sh"` is in `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py`.
- `make verify-sync` exits 0; output saved to `./artifacts/t3-verify-sync.log`.

AC ids: T3.AC1 = plan line 80 (both hooks.json parse with jq, exactly one PreToolUse entry for block-bare-python.sh, matcher Bash, timeout 3; git diff shows only that addition); T3.AC2 = plan line 81 (block-bare-python.sh in _FRESHNESS_SCRIPTS); T3.AC3 = plan line 82 (make verify-sync exits 0; output in ./artifacts/t3-verify-sync.log).
Package root for ./artifacts/ paths: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647. Note: make sync-dev also wrote gitignored dev copies under .claude/ (not staged, per the constraints).

Global constraints: plan lines 17-26, verbatim:
## Constraints

- Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), "Proposed fix" and "Done when". Done when, verbatim: a PreToolUse `Bash` hook blocks a command that runs bare `python`, `python3`, `pip` or `pip3`, with a message naming `uv run python` and `jq`; it allows `uv run python`, `uv pip` and `uvx`, and does not block commands that only mention python in arguments, paths or quoted text; tests cover both the blocked and the allowed cases, including commands chained with `&&`, `;` and `|`; `superclaude install` installs and registers the hook, and it fires for subagent Bash calls; `read-parse.md:8` uses `uv run python`; a fresh session that tries `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` is blocked and pointed to `uv run python` or `jq`.
- Never run `superclaude install` (with or without `--force`) against the live `~/.claude`: other sessions are running. Installer checks use a temporary target path or a temporary HOME only. The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file and never writes to `~/.claude/settings.json` or `~/.claude/hooks/`.
- The hook script is bash plus `jq`, modelled on `src/superclaude/hooks/scripts/freshness-pre-edit.sh`: read the PreToolUse JSON from stdin with `jq`, block with a message on stderr and exit 2, allow with exit 0, never exit 1, and fail open (exit 0) when `jq` is missing, the input is not valid JSON, the tool is not `Bash`, or `tool_input.command` is absent or empty. The hook itself must not run Python.
- Scope of "bare": the command word's basename is exactly `python`, `python3`, `pip` or `pip3` (so `/usr/bin/python3` and `.venv/bin/python` count). Versioned names such as `python3.12` are not part of issue #357 and get no test either way.
- UV for every Python operation in this work (`uv run pytest`, `uv run ruff`); never bare `python`, `python3`, `pip` or `pip3`.
- `src/superclaude/` is the source of truth: run `make sync-dev` after changing hooks or skills, and never stage `.claude/` paths other than `.claude/settings.json`.
- `plugins/superclaude/hooks/hooks.json` already differs from `src/superclaude/hooks/hooks.json` in unrelated entries (ccsession, pragmatic-subagent, auggie matcher). Add only the new registration there; fixing that older drift is out of scope.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Staging is not committing.

Start sha: 511d1613f5132780c1630910f26d78b168b7959a
Diff against the start snapshot:
diff --git a/plugins/superclaude/hooks/hooks.json b/plugins/superclaude/hooks/hooks.json
index 9005de0e..dc14a2e9 100644
--- a/plugins/superclaude/hooks/hooks.json
+++ b/plugins/superclaude/hooks/hooks.json
@@ -52,6 +52,16 @@
             "timeout": 1
           }
         ]
+      },
+      {
+        "matcher": "Bash",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/block-bare-python.sh",
+            "timeout": 3
+          }
+        ]
       }
     ],
     "PostToolUse": [
diff --git a/src/superclaude/cli/install_hooks.py b/src/superclaude/cli/install_hooks.py
index a49d20b1..0a904fdf 100644
--- a/src/superclaude/cli/install_hooks.py
+++ b/src/superclaude/cli/install_hooks.py
@@ -79,6 +79,10 @@ _FRESHNESS_SCRIPTS = [
     # SessionStart (startup) hook: starts one detached `codegraph init --yes` in a
     # git checkout that has no .codegraph/codegraph.db. Fail-open, silent, exit 0.
     "codegraph-session-start.sh",
+    # PreToolUse(Bash) UV-only gate (issue #357): blocks a command that runs bare
+    # python/python3/pip/pip3 with exit 2 and a message naming `uv run python`
+    # and `jq`; fails open (exit 0) on anything it cannot judge, including no jq.
+    "block-bare-python.sh",
 ]
 _LEGACY_SCRIPTS = ["session-init.sh"]
 
diff --git a/src/superclaude/hooks/hooks.json b/src/superclaude/hooks/hooks.json
index 53bb29f0..c43c92a8 100644
--- a/src/superclaude/hooks/hooks.json
+++ b/src/superclaude/hooks/hooks.json
@@ -82,6 +82,16 @@
             "timeout": 1
           }
         ]
+      },
+      {
+        "matcher": "Bash",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/block-bare-python.sh",
+            "timeout": 3
+          }
+        ]
       }
     ],
     "PostToolUse": [
=== new file: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/t3-verify-sync.log (full contents)
     1	🔍 Verifying src/superclaude/ ↔ .claude/ sync...
     2	
     3	=== Skills ===
     4	  ✅ ccsession-tag
     5	  ✅ confidence-check
     6	  ✅ operational-guide
     7	  ✅ prd
     8	  ✅ readme
     9	  ✅ roadmap
    10	  ✅ sc-adversarial-protocol
    11	  ✅ sc-auggie-review-protocol
    12	  ✅ sc-bare-review
    13	  ✅ sc-brainstorm-protocol
    14	  ✅ sc-cleanup-audit-protocol
    15	  ✅ sc-cli-eval-protocol
    16	  ✅ sc-cli-portify-protocol
    17	  ✅ sc-crash-recovery
    18	  ✅ sc-graph-protocol
    19	  ✅ sc-impact-protocol
    20	  ✅ sc-implement-protocol
    21	  ✅ sc-init-lite-protocol
    22	  ✅ sc-pm-protocol
    23	  ✅ sc-post-release-protocol
    24	  ✅ sc-pr-submit-protocol
    25	  ✅ sc-recommend
    26	  ✅ sc-reflect-protocol
    27	  ✅ sc-release-split-protocol
    28	  ✅ sc-review-translation-protocol
    29	  ✅ sc-roadmap-protocol
    30	  ✅ sc-swarm-wizard-protocol
    31	  ✅ sc-task-protocol
    32	  ✅ sc-tasklist-protocol
    33	  ✅ sc-troubleshoot-protocol
    34	  ✅ sc-validate-roadmap-protocol
    35	  ✅ sc-validate-tests-protocol
    36	  ✅ sc-workflow-protocol
    37	  ✅ task-builder
    38	  ✅ task
    39	  ✅ tdd
    40	  ✅ tech-reference
    41	  ✅ tech-research
    42	
    43	=== Agents ===
    44	  ✅ audit-analyzer.md
    45	  ✅ audit-comparator.md
    46	  ✅ audit-consolidator.md
    47	  ✅ audit-scanner.md
    48	  ✅ audit-validator.md
    49	  ✅ auggie-reviewer.md
    50	  ✅ backend-architect.md
    51	  ✅ business-panel-experts.md
    52	  ✅ confidence-calibrator.md
    53	  ✅ debate-orchestrator.md
    54	  ✅ deep-research-agent.md
    55	  ✅ deep-research.md
    56	  ✅ devops-architect.md
    57	  ✅ eval-docs-loader.md
    58	  ✅ eval-run-reporter.md
    59	  ✅ eval-suite-author.md
    60	  ✅ evidence-validator.md
    61	  ✅ frontend-architect.md
    62	  ✅ implement-retry-adviser.md
    63	  ✅ learning-guide.md
    64	  ✅ merge-executor.md
    65	  ✅ performance-engineer.md
    66	  ✅ pm-agent.md
    67	  ✅ python-expert.md
    68	  ✅ quality-engineer.md
    69	  ✅ refactoring-expert.md
    70	  ✅ reflect-reviewer.md
    71	  ✅ repo-index.md
    72	  ✅ requirements-analyst.md
    73	  ✅ reuse-auditor.md
    74	  ✅ rf-analyst.md
    75	  ✅ rf-assembler.md
    76	  ✅ rf-qa-qualitative.md
    77	  ✅ rf-qa.md
    78	  ✅ rf-task-builder.md
    79	  ✅ rf-task-executor.md
    80	  ✅ rf-task-researcher.md
    81	  ✅ rf-team-lead.md
    82	  ✅ root-cause-analyst.md
    83	  ✅ security-engineer.md
    84	  ✅ self-review.md
    85	  ✅ socratic-mentor.md
    86	  ✅ system-architect.md
    87	  ✅ technical-writer.md
    88	  ✅ troubleshoot-analyst.md
    89	
    90	=== Commands ===
    91	  ✅ adversarial.md
    92	  ✅ agent.md
    93	  ✅ analyze.md
    94	  ✅ auggie-review.md
    95	  ✅ brainstorm.md
    96	  ✅ build.md
    97	  ✅ business-panel.md
    98	  ✅ cleanup-audit.md
    99	  ✅ cleanup.md
   100	  ✅ cli-eval.md
   101	  ✅ cli-portify.md
   102	  ✅ design.md
   103	  ✅ document.md
   104	  ✅ explain.md
   105	  ✅ git.md
   106	  ✅ graph.md
   107	  ✅ help.md
   108	  ✅ impact.md
   109	  ✅ implement.md
   110	  ✅ improve.md
   111	  ✅ index-repo.md
   112	  ✅ index.md
   113	  ✅ init-lite.md
   114	  ✅ load.md
   115	  ✅ pm.md
   116	  ✅ post-release.md
   117	  ✅ pr-submit.md
   118	  ✅ recommend.md
   119	  ✅ reflect.md
   120	  ✅ release-split.md
   121	  ✅ research.md
   122	  ✅ review-translation.md
   123	  ✅ roadmap.md
   124	  ✅ save.md
   125	  ✅ spawn.md
   126	  ✅ spec-panel.md
   127	  ✅ swarm-wizard.md
   128	  ✅ task.md
   129	  ✅ tasklist.md
   130	  ✅ tdd.md
   131	  ✅ test.md
   132	  ✅ troubleshoot.md
   133	  ✅ validate-roadmap.md
   134	  ✅ validate-tests.md
   135	  ✅ workflow.md
   136	
   137	=== Hooks ===
   138	  ✅ auggie-flag-clear.sh
   139	  ✅ block-bare-python.sh
   140	  ✅ codegraph-session-start.sh
   141	  ✅ freshness-file-changed.sh
   142	  ✅ freshness-post-read.sh
   143	  ✅ freshness-pre-edit.sh
   144	  ✅ freshness-session-start.sh
   145	  ✅ freshness-subagent-start.sh
   146	  ✅ freshness-subagent-stop.sh
   147	  ✅ freshness-user-prompt.sh
   148	  ✅ reject-workspace-writes.sh
   149	  ✅ sc-recommend-phase0.sh
   150	  ✅ pragmatic-subagent.js
   151	
   152	=== Templates ===
   153	  ✅ workflow/05_prd_template.md
   154	  ✅ workflow/03_project_plan_template.md
   155	  ✅ workflow/03_component_authoring_template.md
   156	  ✅ workflow/00_mdtm_template_simple_task.md
   157	  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
   158	  ✅ workflow/06_architecture_proposal_template.md
   159	  ✅ workflow/02_mdtm_template_complex_task.md
   160	  ✅ workflow/04_feature_brief_template.md
   161	  ✅ workflow/changelog_template.md
   162	  ✅ workflow/01_mdtm_template_generic_task.md
   163	  ✅ workflow/99_mdtm_template_generic_task_old.md
   164	  ✅ documents/prd_template.md
   165	  ✅ documents/operational_guide_template.md
   166	  ✅ documents/GFxAI_Master_Documentation_Template.md
   167	  ✅ documents/tdd_template.md
   168	  ✅ documents/agent_template_analysis.md
   169	  ✅ documents/supplemental-doc-creation-checklist.md
   170	  ✅ documents/agent_template_qa.md
   171	  ✅ documents/skill_template.md
   172	  ✅ documents/roadmap_template.md
   173	  ✅ documents/agent_template_worker.md
   174	  ✅ documents/release-spec-template.md
   175	  ✅ documents/supplemental_doc_template.md
   176	  ✅ documents/technical_reference_template.md
   177	  ✅ documents/readme_template.md
   178	  ✅ modularization-template-review/qa-fix-summary_template.md
   179	  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
   180	  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
   181	  ✅ modularization-template-review/research-notes_template.md
   182	  ✅ modularization-template-review/synthetic-dnsp-finding.contract
   183	  ✅ modularization-template-review/INDEX.md
   184	  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
   185	  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
   186	  ✅ modularization-template-review/track-scope-map_template.md
   187	  ✅ modularization-template-review/claim-evidence-matrix_template.md
   188	  ✅ modularization-template-review/qa-inventory_report_template.md
   189	  ✅ modularization-template-review/analyst-coverage-matrix_template.md
   190	  ✅ modularization-template-review/codebase-research_template.md
   191	  ✅ modularization-template-review/analyst-completeness_report_template.md
   192	  ✅ modularization-template-review/analyst-gap-analysis_template.md
   193	  ✅ modularization-template-review/qa-lens_report_template.md
   194	  ✅ modularization-template-review/qa-consolidated-findings_template.md
   195	  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
   196	  ✅ modularization-template-review/qa-research-gap_report_template.md
   197	  ✅ modularization-template-review/qa-research-evidence_report_template.md
   198	  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
   199	  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
   200	  ✅ modularization-template-review/analyst-cross-validation_report_template.md
   201	  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
   202	  ✅ modularization-template-review/pipeline-complete_report_template.md
   203	  ✅ modularization-template-review/qa-source-fidelity_template.md
   204	  ✅ modularization-template-review/qa-research-depth_report_template.md
   205	  ✅ modularization-template-review/web-research_template.md
   206	
   207	=== Installer Registration ===
   208	  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
   209	
   210	=== Hooks Cross-Consistency ===
   211	  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
   212	
   213	✅ All components in sync.
   214	verify-sync rc=0

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
