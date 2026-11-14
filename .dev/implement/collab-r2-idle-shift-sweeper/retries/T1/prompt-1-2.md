713b2663af957a3b43d567fbb3096732b6a6f611
Review one task for spec compliance.

Task brief: T1 = the whole document /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/DESIGN.md (call it R2/DESIGN.md; R2 is that folder's parent path above). Its acceptance criteria are section 6.5, with these ids: T1.AC1 = AC-1, T1.AC2 = AC-2, T1.AC3 = AC-3, T1.AC4 = AC-4, T1.AC5 = AC-5, T1.AC6 = AC-6, T1.AC7 = AC-7, T1.AC8 = AC-8, T1.AC9 = AC-9, T1.AC10 = AC-10, T1.AC11 = AC-2b. The delivered work is everything under R2 except DESIGN.md (bin/, py/, config/, spikes/, tests/, runs/, results/, scoring/, README.md, IMPLEMENTATION.md). IMPLEMENTATION.md is the implementer's own report: do not trust it, check each of its claims against the files and logs. Evidence you may read for the evidence-type criteria: R2/spikes/RESULTS.md, R2/spikes/out/**, R2/runs/smoke-*/**, R2/results/smoke-*.json, R2/config/manifest.json. You cannot run commands; judge test claims by reading the tests and the recorded results (the implementer reports 358 passed, 0 skipped, from `uv run pytest R2/tests -q`).
Global constraints: Created or edited only under R2/, .dev/implement/collab-r2-idle-shift-sweeper/, /tmp/evalsb-collab-r2/ and /tmp/collab-r2/; nothing under src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or another redesign's folder; nothing staged, committed or pushed. Python only through uv. Allowed models: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; claude-opus-5-5 only as the blind judge; never Qwen or glm; NOFALLBACK=1. At most 3 reviewer or judge model sessions at once. No full panel runs (Spike 4 included) by the implementer; every requirement or acceptance criterion not met must be listed with its reason in R2/IMPLEMENTATION.md.
Start sha: 713b2663af957a3b43d567fbb3096732b6a6f611
Diff against the start snapshot: Every file under R2 except DESIGN.md was created or changed after the start snapshot; read them with Read, Glob and Grep. Changes made in this resumed session: R2/py/audits.py (per-field ground-truth check, anchor overlap recorded as a note, path tokens removed from items and cmd, carry-over of sandbox verdicts when the sandbox is gone), R2/tests/test_audits.py (5 added tests), R2/spikes/RESULTS.md (appended lines), R2/spikes/out/s3/**, R2/runs/smoke-el2-*, smoke-hl2-*, R2/results/smoke-*.json (new smoke runs; the first two EL2 rows are kept as runs/smoke-el2-*.invalid-20261113T2250), R2/IMPLEMENTATION.md (rewritten). Codegraph context: index_state fresh, checked_at 2026-11-13T20:27:08Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel, projectPath the same; call codegraph only when index_state: fresh, never to widen scope. Shell scripts and Markdown are not indexed, so this review is on the Grep and Read floor.
Delta diff from the previous reviewed tree (empty on the first review):
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/IMPLEMENTATION.md b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/IMPLEMENTATION.md
index f7254b182..e99956f13 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/IMPLEMENTATION.md
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/IMPLEMENTATION.md
@@ -145,6 +145,8 @@ History of the EL2 pair, kept on disk as `runs/smoke-el2-*.invalid-20261113T2250
 | U-4 | AC-10 wording "a smoke run is never re-run to hide a breach" | Met for breaches, with a caveat. | The first EL2 iso run ended in `hang_kill` and INVALID and the pair was re-run. The INVALID rows are kept and reported above; the re-run was not made to hide an SLO breach but it is a re-run. |
 | U-5 | Lint of the shell scripts | Only `bash -n`. | `shellcheck` is not installed in this environment. |
 | U-6 | `tests/fixtures/` of the design tree | Folder exists, empty. | Fixtures are built in a temp directory by `conftest.py`; nothing reads a static fixture. |
+| U-7 | AC-6, literal text "no ground-truth substring on the board" | **Not met as written; met only under the narrowed audit.** The final `smoke-el2-collab/.../audit.json` says `ok: true` yet its `notes[]` records a 12-character ground-truth overlap in an anchor (`>/issue-fiel`, fact `f-2`), and `smoke-sl2-collab` records two (`` ` tests/skil`` ). The S3 PASS line therefore means "AC-6 under D-A1 to D-A2", not under DESIGN 2.8. | The audit was narrowed after it failed on chance overlaps with plan text and repo paths (section 5.3). Whether that narrowing is acceptable is the owner's call; the original rule is restored by reverting those two branches in `py/audits.py`, after which the two collab smoke packages (EL2, SL2) fail AC-6 again. |
+| U-8 | Scope of `/tmp` writes (orchestrator rule: only `/tmp/evalsb-collab-r2/` and `/tmp/collab-r2/`) | Two writes outside it remain. The hook temp files that were created under `/tmp/r2-rhook.*` and `/tmp/r2-hhook.*` were moved to `/tmp/collab-r2/` in this session (the smoke rows of this section ran with the earlier hooks, which removed those files after each call). Still outside: `/tmp/panel-probe` (an empty directory made by `spikes/reqs3-actrate.sh`, whose probe text names `ls /tmp/panel-probe` as DESIGN 6.3 prescribes) and `/tmp/collab-gateway.lock` (created by the `flock` commands the design and the orchestrator's launch recipe use). | Both paths are written literally in DESIGN.md. Nothing was deleted or moved out of `/tmp/panel-probe`. The `reqs3` spike was not re-run with a changed path, so its recorded rates still describe the script as it ran. |
 
 ### 5.2 Observations that bear on how the rows are read (not failures of an AC)
 
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/harvest-hook.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/harvest-hook.sh
index 612c4affd..feb0ba9a2 100755
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/harvest-hook.sh
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/harvest-hook.sh
@@ -75,7 +75,7 @@ main() {
   mlog "$("$JQ" -cn --argjson t "$(now_ms)" --arg r "$res" --arg m "$move" '{ev:"harvest",t:$t,move:$m,result:$r}')"
 }
 
-ERRF=$(mktemp /tmp/r2-hhook.XXXXXX 2>/dev/null || echo /dev/null)
+ERRF=$(mkdir -p /tmp/collab-r2 2>/dev/null; mktemp /tmp/collab-r2/r2-hhook.XXXXXX 2>/dev/null || echo /dev/null)
 ( main ) >/dev/null 2>"$ERRF"; RC=$?
 if [ $RC -ne 0 ]; then
   MSG=$(head -c 300 "$ERRF" 2>/dev/null | tr -cd 'A-Za-z0-9 ._:/=-')
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/receiver-hook.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/receiver-hook.sh
index 67f68e1cc..a56ac26f8 100755
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/receiver-hook.sh
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/bin/hooks/receiver-hook.sh
@@ -89,7 +89,7 @@ main() {
   done_call
 }
 
-ERRF=$(mktemp /tmp/r2-rhook.XXXXXX 2>/dev/null || echo /dev/null)
+ERRF=$(mkdir -p /tmp/collab-r2 2>/dev/null; mktemp /tmp/collab-r2/r2-rhook.XXXXXX 2>/dev/null || echo /dev/null)
 OUTPUT=$( (main) 2>"$ERRF" ); RC=$?
 if [ $RC -ne 0 ]; then
   MSG=$(head -c 300 "$ERRF" 2>/dev/null | tr -cd 'A-Za-z0-9 ._:/=-' )
Earlier blocking findings of this start (empty on the first review):
F1.1 sev=blocking trigger=B1 ac=T1.AC6 at=py/audits.py:149 anchor="no ground-truth substring on the board" chk=y,n,n,n family=audit-weakened fix=list AC-6 as met only under the narrowed audit in IMPLEMENTATION 5.1: audit narrowed after it failed; AC-6 literal text not met, IMPLEMENTATION lists the narrowing (D-A1/D-A2) but not AC-6 as unmet.
F2.1 sev=blocking trigger=B1 ac=T1.AC3 at=spikes/RESULTS.md:1 anchor="Every Gate 0 spike in 6.3 has a PASS line in `spikes/RESULTS.md` with an evidence path" chk=y,n,n,n family=spike4-missing fix=orchestrator runs spikes/spike4-values.sh per panel and re-pins config/manifest.json: no Spike 4 line; disclosed as U-1; implementer barred from full panel runs.
F3.1 sev=blocking trigger=B4 ac=scope at=bin/run-package.sh:74 anchor="At most 3 reviewer or judge model sessions at once." chk=n,n,n,y family=concurrency-cap fix=start the sweeper after one reviewer ends on SL2/HL2, or the owner rules the helper does not count: smoke-sl2-collab and smoke-hl2-collab ran 4 sessions at once; disclosed as U-2.
F4.1 sev=blocking trigger=B4 ac=scope at=spikes/reqs3-actrate.sh:12 anchor="Created or edited only under R2/, .dev/implement/collab-r2-idle-shift-sweeper/, /tmp/evalsb-collab-r2/ and /tmp/collab-r2/" chk=n,n,n,y family=tmp-scope fix=hook temp files to /tmp/collab-r2; document /tmp/panel-probe and /tmp/collab-gateway.lock: reqs3 spike mkdir /tmp/panel-probe (DESIGN 6.3 literal command); hooks mktemp under /tmp/r2-*.
Saved-probe re-check hit locations (may be empty):
probe re-check: py/audits.py (anchor branch and PATH_TOKEN) unchanged; IMPLEMENTATION.md U-7 and U-8 now exist; bin/hooks/receiver-hook.sh:92 and bin/hooks/harvest-hook.sh:78 mktemp under /tmp/collab-r2; spikes/reqs3-actrate.sh:12 still names /tmp/panel-probe.

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
