7987ab62e0024258b9bd4ad4197ddcc89dbbee48
Review one task for spec compliance.

Task brief: ## Task 9: Write the design note

Depends on: Task 8

Create `docs/designs/spec-panel-ponytail.md`: ./source.md cut to its decisions (sections 2.1, 2.2 table, 2.6, 2.7 summary, 2.8 recommendation, 3.1 file list, 4), the four owner decisions, the Unattended-mode deviation and the 472-line base (owner correction) from Constraints, the owner count of Task 5, the install steps (pointing to `.dev/brainstorms/346-ponytail/INSTALL.md`), and the inserted T08a command line of ./source.md section 4.

Acceptance criteria:
- The file exists and contains the literals `/sc:spec-panel-ponytail`, `--fix-audit`, `sc-fix-audit`, `fix_audit.py verdict`, `owner count`, the T08a command line exactly as in ./source.md section 4, a sentence stating the variant omits `## Unattended mode` and why, and the string `spec-panel-post427-95f2c6e4.md` naming the 472-line base.
- `uv run pytest tests/docs -q` passes.

AC ids: T9.AC1,T9.AC2 (in the order of the Acceptance criteria bullets). Repo root: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail. Package root (what ./ means in this brief): /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547.
Global constraints: ## Constraints

- Scope is ./source.md section 3 "Exact changes" and section 4 "Variant command name and install note" only. Section 5 (running the S1 experiment, replicates, paired fork, blind re-grade) and section 6 are not built by this plan; only the brief template and the recorder's verdict line from section 4 are delivered.
- Owner decision (overrides ./source.md): the success measure counts findings that the new script defers, demotes or withdraws as still open. A finding whose fix the audit reverted (an id in `closed-minor.txt`) or that the audit logged `DOWNGRADE` stays in the review-3 critical+major count when review 2 labelled it CRITICAL or MAJOR. The `verdict` subcommand reports this count (Task 5); nothing in the script lowers it.
- Owner decision: the S1 review-3 brief (T09) is not edited, including its "any finding of any severity is FAIL" line.
- Owner decision: the `--fix-audit` flag in the brief is the explicit consent for the one scripted edit or revert that `apply` makes (resolves ./source.md section 7 question 4; `apply` stays inside the `--fix-audit` run).
- Owner decision: the audit runs after the cycle-2 fixes and before review 3 (placement P of ./source.md section 2.8; resolves section 7 question 1).
- `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md`, `tests/skills/test_spec_panel_review_loop.py`, `src/superclaude/output-styles/pragmatic.md` and `src/superclaude/skills/sc-implement-protocol/refs/qa.md` are not changed (./source.md section 3.1, row "Not changed").
- Deviation from ./source.md section 3.1 row 1, confirmed by owner ruling (coordinator message msg_7b27feaade5e, 2026-11-08): the current `spec-panel.md` (486 lines) carries a `## Unattended mode` section (lines 451-462, added by commit 2327fbd3 after the 427 Review Loop). A copy that keeps it fails `tests/skills/test_worker_contract.py` (`_check_no_unattended_sections` requires the set of commands with that section to equal the P1 plus P2 list) and makes the brief guard of `~/.claude/WORKER-CONTRACT.md` (case 1) refuse the T08a command line, which carries no `--unattended`. The variant therefore omits the `## Unattended mode` section as one more enumerated difference, and does not support `--unattended`. Everything else is a byte copy.
- Owner correction (coordinator message msg_1125a0eb124a, 2026-11-08; supersedes the base named above): the variant's base is the 472-line Arm B file, byte for byte: `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/inputs/tool-text/spec-panel-post427-95f2c6e4.md` (read-only; sha256 `c8d80346a96cb528fce6cff3bcadfed5bc95d1eee48dea0ac275404314b8df2f`). It equals the current `src/superclaude/commands/spec-panel.md` without three spans: the second Usage line (the one advertising `--unattended`), the sentence "When `--target-release <release>` is passed ..." in Behavioral Flow, and the `## Unattended mode` section. Because the experiment folder is outside the repo, Task 7 copies this base byte for byte into `tests/skills/fixtures/spec-panel-post427-base.md` (a test fixture, not installed) and every drift test compares against that fixture. `src/superclaude/commands/spec-panel.md` is not changed. Wherever a task below says "copy of `src/superclaude/commands/spec-panel.md`" or "the base", it means this 472-line base.
- A new command also breaks `tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory` (`shipped - _POST_REFRESH_ADDITIONS == active`); Task 7 adds `spec-panel-ponytail` to `_POST_REFRESH_ADDITIONS` (line 33). No routing-guide row is added (./source.md section 3.1).
- No plugin mirror: `plugins/superclaude/skills/` mirrors only four skills and `tests/commands/test_routing_plugin_parity.py` checks only the four commands the commands README lists, so neither the new command nor the new skill gets a `plugins/superclaude/` copy.
- No installed primitive (the command, `SKILL.md`, the brief) contains the string `src/superclaude`; installed lookups name `~/.claude/skills/sc-fix-audit/` first, then the project `.claude/skills/sc-fix-audit/` (project CLAUDE.md rule).
- Python runs only through `uv run`. `fix_audit.py` uses the standard library only (`argparse`, `difflib`, `hashlib`, `json`, `os`, `re`, `pathlib`, plus `tempfile`/`sys` if needed).
- After editing primitives run `make sync-dev` and `make verify-sync`. Never stage anything under `.claude/` except `.claude/settings.json`; never use `git add -f`. `.dev/tasks` is always staged. Staging is not committing; no commit, push or PR is part of this plan.
- Never write to `~/.claude/`, other worktrees or the experiment folders; installing is described in INSTALL.md, not performed.
Start sha: 7987ab62e0024258b9bd4ad4197ddcc89dbbee48
Diff against the start snapshot: saved byte for byte (git diff 7987ab62e0024258b9bd4ad4197ddcc89dbbee48 over the touched files docs/designs/spec-panel-ponytail.md, plus full contents of untracked touched files) at /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/diffs/T9-r3-1.diff; read that whole file, and the live files it names
Delta diff from the previous reviewed tree (empty on the first review): saved byte for byte (git diff f45b735179daa0fc17e0bcad216762cadc9333b3 bdc2fbe11dfccc1459353bd531c5cb65a1288e56 over the touched files; f45b735179daa0fc17e0bcad216762cadc9333b3 is the failed attempt-2 checkpoint, the note was reverted to absent and rewritten from brief 3) at /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/diffs/T9-delta-a2-to-r3-1.diff
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=scope at=docs/designs/spec-panel-ponytail.md:30 anchor=src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:653 chk=n,y,n,n family=doc-claim-vs-code fix=narrow the sentence to ids review 2 graded blocking first=A1 origin=new: the note says a validated-minor grade on an id that is blocking or protected is logged DOWNGRADE; the script logs DOWNGRADE only when ids[rid]["blocking"] is true (fix_audit.py:653), so a protected id graded non-blocking gets no DOWNGRADE line and never enters the held list (fix_audit.py:1020). The "never closed" half is true (K6 at :678, classify at :293).
F2.1 sev=blocking trigger=B2 ac=scope at=docs/designs/spec-panel-ponytail.md:31 anchor=src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:898 chk=n,y,n,n family=doc-claim-vs-code fix=narrow the sentence to "every check failure, apply stop, or failed spec write leaves the specification byte-identical to `current-before-audit.md`" (or make apply restore the spec when writing apply-log.md or closed-minor.txt fails) first=A1 origin=late: the note says every failure path leaves the spec byte-identical. But apply replaces the spec at :877 and only then writes apply-log.md at :898 and closed-minor.txt at :899-901, with no handler. If either write raises OSError (for example a full disk or a fix-audit/ folder that cannot be written), the spec stays edited, apply-log.md is missing, and state.json still says "checked". A rerun then fails K1 at :586 and records skipped(check failed) while the spec stays edited. The source design makes the same claim (source.md:47), so the gap is real but only shows up on an input/output error.
Saved-probe re-check hit locations (may be empty): probe-1-1 (DOWNGRADE):
30:- A finding review 2 graded blocking, or protected (CRITICAL, FR-8, FR-9), is never closed by the audit. A validated-minor grade on an id review 2 graded blocking is logged `DOWNGRADE <id>` only; a protected id that review 2 did not grade blocking gets no `DOWNGRADE` line.
44:Owner decision: findings that the script defers (reverted, listed in `closed-minor.txt`) or demotes (logged `DOWNGRADE`) stay open in the success measure. `final-verdict.md` prints `held open (deferred or demoted): ...`, `review-3 new critical+major: <n>` and `review-3 critical+major (owner count
probe-2-1 (failure-path wording):
34:  - An exact-once or overlap failure prints `APPLY_STOP: nothing written` and the specification is not written.
35:  - If the specification write or its read-back fails, the script tries to copy `current-before-audit.md` back over the specification, then prints `APPLY_STOP: nothing written (write failed: ...)`.
80:In S1 a pure one-line name substitution does not work, so the briefs T05-T09 stay byte-identical and one Task T08a is inserted between T08 (cycle-2 reviser) and T09 (review 3). Its single command line is:

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
