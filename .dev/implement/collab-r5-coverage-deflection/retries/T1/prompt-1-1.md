aa2f2bcedc445dfaf6828eb0fb408e1f3871ba2b
Review one task for spec compliance.

Task brief: T1 = implement the design in /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection/DESIGN.md (read it all; call that folder R5 and the repository root REPO = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel). Its acceptance criteria are DESIGN section 6.5, numbered here T1.AC1 to T1.AC10 for AC-1 to AC-10 (read the exact AC text in DESIGN.md lines 551-564). T1.AC11 (from the orchestrator's instruction to the executor): the executor rewrote R5/IMPLEMENTATION.md so that it is TRUE: what was built (file list), how to run one panel on all three packages (exact command for each of ember + 2x luna, sonnet + 2x luna and haiku + 2x luna, plus PANEL_COLLAB=0), test results with counts, spike and smoke results, and every requirement or acceptance criterion that is not met, with the reason. The executor reports AC-4 and AC-5 as NOT MET and the other ACs as MET (AC-2 and AC-8 with qualifications). Your job is to check those claims against live files, not to accept them. Allowed evidence: files under R5, REPO, /tmp, and read-only commands (grep, jq, sha256sum, git status/diff/ls-tree, bash R5/bin/pins-check.sh). You may run the AC-1 pytest command (DESIGN.md line 555, about 100 s, it calls no model). Do NOT run any model, launch.sh, spike script or judge, and do not write or edit any file.
Global constraints: (1) create and edit files ONLY under R5, .dev/implement/collab-r5-coverage-deflection/, and scratch under /tmp/evalsb-collab-r5/ and /tmp/collab-r5/; do not edit src/, tests/ (the repo-root tests folder), .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder; do not stage, commit or push; (2) Python only through uv; (3) models allowed: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus (claude-opus-5-5) only as the blind judge; never Qwen or glm; NOFALLBACK=1; at most 3 reviewer or judge model sessions at once; (4) no full panel runs (the orchestrator runs those); (5) DESIGN.md section 0.3 and its Non-goals: nothing is written to REPO/src/ or EVAL.
Start sha: aa2f2bcedc445dfaf6828eb0fb408e1f3871ba2b
Diff against the start snapshot: The start snapshot (a git tree) holds only 11 files under R5 (.build-start, DESIGN.md, design-report/*, implement-report/session.*). Everything else under R5 (about 600 files: bin/, lib/r5/, config/, tests/, spikes/, runs/, scoring/, results/, ruff.toml, IMPLEMENTATION.md) is new and untracked, so a plain `git diff` is almost empty; review by reading the files named in R5/IMPLEMENTATION.md section 1 and the evidence it cites (spikes/NOTES.md, results/, runs/*/launch.json, tests/last-run.txt). Use `git ls-tree -r --name-only aa2f2bcedc445dfaf6828eb0fb408e1f3871ba2b -- <R5>` to see what was there at the start. Codegraph context: index_state fresh, checked_at 2026-11-13T20:27:01Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel, projectPath the same; call codegraph only when index_state: fresh, never to widen scope.
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
