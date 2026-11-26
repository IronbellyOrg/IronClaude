713b2663af957a3b43d567fbb3096732b6a6f611
Review one task for spec compliance.

Task brief: T1 = the whole document /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/DESIGN.md (call it R2/DESIGN.md; R2 is that folder's parent path above). Its acceptance criteria are section 6.5, with these ids: T1.AC1 = AC-1, T1.AC2 = AC-2, T1.AC3 = AC-3, T1.AC4 = AC-4, T1.AC5 = AC-5, T1.AC6 = AC-6, T1.AC7 = AC-7, T1.AC8 = AC-8, T1.AC9 = AC-9, T1.AC10 = AC-10, T1.AC11 = AC-2b. The delivered work is everything under R2 except DESIGN.md (bin/, py/, config/, spikes/, tests/, runs/, results/, scoring/, README.md, IMPLEMENTATION.md). IMPLEMENTATION.md is the implementer's own report: do not trust it, check each of its claims against the files and logs. Evidence you may read for the evidence-type criteria: R2/spikes/RESULTS.md, R2/spikes/out/**, R2/runs/smoke-*/**, R2/results/smoke-*.json, R2/config/manifest.json. You cannot run commands; judge test claims by reading the tests and the recorded results (the implementer reports 358 passed, 0 skipped, from `uv run pytest R2/tests -q`).
Global constraints: Created or edited only under R2/, .dev/implement/collab-r2-idle-shift-sweeper/, /tmp/evalsb-collab-r2/ and /tmp/collab-r2/; nothing under src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or another redesign's folder; nothing staged, committed or pushed. Python only through uv. Allowed models: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; claude-opus-5-5 only as the blind judge; never Qwen or glm; NOFALLBACK=1. At most 3 reviewer or judge model sessions at once. No full panel runs (Spike 4 included) by the implementer; every requirement or acceptance criterion not met must be listed with its reason in R2/IMPLEMENTATION.md.
Start sha: 713b2663af957a3b43d567fbb3096732b6a6f611
Diff against the start snapshot: Every file under R2 except DESIGN.md was created or changed after the start snapshot; read them with Read, Glob and Grep. Changes made in this resumed session: R2/py/audits.py (per-field ground-truth check, anchor overlap recorded as a note, path tokens removed from items and cmd, carry-over of sandbox verdicts when the sandbox is gone), R2/tests/test_audits.py (5 added tests), R2/spikes/RESULTS.md (appended lines), R2/spikes/out/s3/**, R2/runs/smoke-el2-*, smoke-hl2-*, R2/results/smoke-*.json (new smoke runs; the first two EL2 rows are kept as runs/smoke-el2-*.invalid-20261113T2250), R2/IMPLEMENTATION.md (rewritten). Codegraph context: index_state fresh, checked_at 2026-11-13T20:27:08Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel, projectPath the same; call codegraph only when index_state: fresh, never to widen scope. Shell scripts and Markdown are not indexed, so this review is on the Grep and Read floor.
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
