9e83e1e98bec90d57fa2a925fa0bf92ecae216ee
Review one task for spec compliance.

Task brief: ## Task 5: Implement `fix_audit.py verdict` with the still-open count

Depends on: Task 4

Add the `verdict --dir D --report R3 [--report-rule 427|any-severity]` subcommand (default `427`) as ./source.md section 2.7 items 1-6 state: `closed` from `D/closed-minor.txt` (empty when the audit was skipped, stopped or not triggered); `prior_open` = rows of review 3's resolution table with status `open` or `regressed` whose id R2 graded blocking; `new_blocking` = review-3 new findings graded blocking with the same tolerant parse (unknown counts as blocking); `open` = `prior_open` + `new_blocking`; a closed id listed open prints `closed-minor, listed open: <id>`; a closed id that review 3 grades blocking prints `consistency: DISAGREE` and forces FAIL in both modes; in `427` mode a report last line that disagrees with the computed one prints `consistency: DISAGREE` and the stricter line wins; in `any-severity` mode the report's own last line is printed as `t09-verdict:`; an unparseable table exits 2 with `verdict: FAIL`; any `consistency: DISAGREE` (a disagreeing verdict, ./source.md section 3.3 "verdict unparseable or inconsistent"; plan amendment F-04) also exits 2 with last line `verdict: FAIL`. The script never turns a FAIL into a PASS.

Owner decision (Constraints): also compute and print, in `D/final-verdict.md`:
- `held open (deferred or demoted): <id label, ...>` = every id in `closed-minor.txt` plus every id logged `DOWNGRADE` in `D/check.log`, each with its review-2 severity label from `D/state.json`;
- `review-3 new critical+major: <n>` = review-3 new findings labelled CRITICAL or MAJOR;
- `review-3 critical+major (owner count, held findings included): <n>` = that number plus the held ids whose review-2 label is CRITICAL or MAJOR.
`closed-minor` ids are printed as `closed-minor (deferred, counted open in the owner count): <ids>`.

Write `D/final-verdict.md` with the lines `open blocking: <ids or none>`, the `closed-minor` line above, `downgrades logged: <ids>`, the two held/count lines above, `audit: <state>`, the review-3 report's own last line, any `consistency:` line, and last line `verdict: PASS` (open is empty and no DISAGREE forced FAIL) or `verdict: FAIL`.

Extend `tests/skills/test_fix_audit_script.py` with the "verdict" bullet of ./source.md section 3.5 and the owner-count cases.

Acceptance criteria:
- `uv run pytest tests/skills/test_fix_audit_script.py -q` passes, with tests for: a report whose own line is FAIL never yields a final PASS; open and regressed prior findings that R2 graded blocking stay in `open blocking`; a listed-open row for an R2-minor id does not count, and a closed one prints `closed-minor, listed open: <id>`; a closed id graded blocking by review 3 gives `consistency: DISAGREE`, exit code 2 and `verdict: FAIL`; an unparseable table exits 2 with last line `verdict: FAIL`; in `427` mode a disagreeing report line gives `consistency: DISAGREE`, exit code 2 and the stricter line; in `any-severity` mode the report line appears as `t09-verdict:`.
- Owner-count tests: a reverted finding labelled MAJOR in R2 raises `review-3 critical+major (owner count, held findings included)` by 1 over `review-3 new critical+major`; a `DOWNGRADE` id labelled CRITICAL raises it by 1; a reverted id labelled MINOR does not raise it; with the audit skipped both numbers are equal.
- The last line of `D/final-verdict.md` is always exactly `verdict: PASS` or `verdict: FAIL`.

AC ids: T5.AC1,T5.AC2,T5.AC3 (in the order of the Acceptance criteria bullets). Repo root: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail. Package root (what ./ means in this brief): /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547.
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
Start sha: 9e83e1e98bec90d57fa2a925fa0bf92ecae216ee
Diff against the start snapshot: saved byte for byte (git diff 9e83e1e98bec90d57fa2a925fa0bf92ecae216ee over the touched files src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py, tests/skills/test_fix_audit_script.py, plus full contents of untracked touched files) at /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/diffs/T5-r1-1.diff; read that whole file, and the live files it names
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
