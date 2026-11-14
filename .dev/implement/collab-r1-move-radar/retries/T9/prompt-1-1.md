6b2b9176432cbb554cb2f5543d5f969f5047bfca
Review one task for spec compliance.

Task brief: T9 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md sections 6.4 and 6.5 AC-3, AC-4, AC-5; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). The one-package smoke test (S3) of section 6.4 and its acceptance criteria.
T9.AC1: Smoke rows run (as far as Gate 0 allows) and each 6.4 condition is checked and recorded. Section 6.4: the smoke is `PANEL_COLLAB=1 bash tools/launch.sh el2 0 TASK-WF-designSpec-20261107-075614` and then the same with PANEL_COLLAB=0; it passes when all seven hold: (1) three reviewers with model_ok true and the observed model equal to the panel model; (2) dropped_lines 0 for every reviewer, or the re-ask ran and the remaining drops are recorded; (3) collab 1: hook_calls > 0 for all three, injections per rid <= k, no injection after GUARD, seal_t before first_delivery_t, leak lookup clean; collab 0: no settings/ directory, no msgs/, no --settings in any argv in meta.json; (4) superclaude review merge rc 0 and the merged report lists the three reviewer ids; (5) merged-anon.md passes the T-14 assertions, the judge wrote a parseable score.json under R1/scoring/, no new entry under A1DIR; (6) results/<row>.json validates against the section 5.4 shape, status incomplete being the only accepted reason for null sums; (7) git status --porcelain empty in the sandbox, candidate sha256 unchanged, cleanup-sessions.sh removed exactly the recorded session files. AC-3 asks for all 7 for collab 1 and collab 0; AC-4: T-10 passes and the collab-0 smoke row has 0 injections, no settings/ and no msgs/; AC-5: after AC-3, git status --porcelain in REPO shows changes only under R1/, nothing newer than manifest.json under A1DIR.
What the executor did (implementer claims, verify them): (a) the collab-0 smoke row el2-c0-r0 ran for real in R1: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/runs/el2-c0-r0/, results/el2-c0-r0.json. (b) The real collab-1 smoke could not run: launch.sh refuses it (exit 2) because Gate 0 needs Spike 4 (a values file per package, 3 full collab-0 rows per panel; the orchestrator forbids full panel runs) and S3; S3 was therefore NOT written as pass in spikes/gate0.json, which still says S3 missing, Spike 4 missing. (c) To exercise the collab-1 path with real models anyway, a PROVISIONAL collab-1 smoke ran in a scratch root /tmp/collab-r1/r1scratch with planning values and a hand-written gate file (built by /tmp/collab-r1/mkscratch.sh); its small evidence files were copied to .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/provisional-c1/. (d) The seven conditions were decided by /tmp/collab-r1/smokecheck.sh; outputs in .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-el2-c0-r0.tsv and check-provisional-el2-c1-r0.tsv.
Global constraints: Orchestrator constraints (global): create and edit files only under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/); do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or any other redesign's folder; do not stage, commit or push; python only through uv; models allowed muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7, Opus only as the blind judge, never Qwen or glm; NOFALLBACK=1; no full panel runs; at most 3 reviewer or judge sessions at once.
Start sha: 6b2b9176432cbb554cb2f5543d5f969f5047bfca
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-el2-c0-r0.tsv b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-el2-c0-r0.tsv
new file mode 100644
index 000000000..1ff7201f0
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-el2-c0-r0.tsv
@@ -0,0 +1,8 @@
+status=ok
+1	true	t2b-1:muse-ember-1.0:model_ok=true t3-1:gpt-6-luna:model_ok=true t4-1:gpt-6-luna:model_ok=true 
+2	true	 t2b-1:dropped=0,reask=5.491 t3-1:dropped=0,reask=null t4-1:dropped=0,reask=null
+3	true	settings_dir=no msgs_dir=no settings_in_argv=0
+4	true	merge_stdout_tail=viewer_id": "t3-1"     }    ]   }  ],  "decision": "PASS",  "new": [   "L1",   "L2"  ],  "refound": [],  "regressed": [],  "verdict": "PASS",  "warnings": [] } 
+5	true	anon_leak=0 score={"gt_covered_any":[],"wrong_blockers":0} a1_unchanged=yes
+6	true	status=incomplete found_14=null output_tokens=null
+7	true	git_clean=yes cand_sha_unchanged=true sessions=3 deleted=3 absent=0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-provisional-el2-c1-r0.tsv b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-provisional-el2-c1-r0.tsv
new file mode 100644
index 000000000..8d03b5f9d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/check-provisional-el2-c1-r0.tsv
@@ -0,0 +1,8 @@
+status=ok
+1	true	t2b-1:muse-ember-1.0:model_ok=true t3-1:gpt-6-luna:model_ok=true t4-1:gpt-6-luna:model_ok=true 
+2	true	 t2b-1:dropped=0,reask=null t3-1:dropped=0,reask=null t4-1:dropped=0,reask=null
+3	true	{"t2b-1":{"hook_calls":10,"inj":2,"k":2,"seal_t":1794611690863,"first":1794611690863},"t4-1":{"hook_calls":9,"inj":1,"k":2,"seal_t":1794611710445,"first":1794611710445},"t3-1":{"hook_calls":8,"inj":1,"k":2,"seal_t":1794611732535,"first":1794611732535}} leak_violations=0
+4	true	merge_stdout_tail=1"     }    ]   }  ],  "decision": "PASS",  "new": [   "L1",   "L2",   "L3",   "L4"  ],  "refound": [],  "regressed": [],  "verdict": "PASS",  "warnings": [] } 
+5	true	anon_leak=0 score={"gt_covered_any":["GT3","GT7"],"wrong_blockers":0} a1_unchanged=yes
+6	true	status=incomplete found_14=null output_tokens=null
+7	true	git_clean=yes cand_sha_unchanged=true sessions=3 deleted=3 absent=0

Codegraph context: index_state: fresh; checked_at: 2026-11-13T22:17:42Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. call codegraph only when index_state: fresh, never to widen scope. Q2b dependents: none outside the diff (shell, markdown and untracked test files are not indexed; Grep floor used).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): Evidence the reviewer may read (not part of the diff): .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/runs/el2-c0-r0/ (launch.log, run.json, TASK-WF-designSpec-20261107-075614/{status,collab.json,audit.json,reviews/*.meta.json,merged-1.md,label-key.json}), .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/results/el2-c0-r0.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/scoring/*/, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/ (checks, provisional-c1/ copies), /tmp/collab-r1/r1scratch/ (the provisional row in full), /tmp/collab-r1/smokecheck.sh, /tmp/collab-r1/mkscratch.sh, /tmp/collab-r1/a1-listing-before.txt (a listing hash of A1DIR taken before the smoke rows), the full test log /tmp/collab-r1/t7-pytest.log.


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