8446c587969d893ff1e7fa21c254546fec5814a9
Review one task for spec compliance.

Task brief: ## Task 2: Implement `fix_audit.py prepare`

Depends on: Task 1

Create `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py` with an `argparse` CLI and the `prepare --baseline B --current S --report R [--dispositions DISP] --out D` subcommand, as ./source.md sections 2.2 (trigger rule), 2.3 item 1 and 3.3 (row `prepare`) state:
- Trigger check: a line of R starts with `review: 2 of 3` (trailing text allowed) and R's last non-empty line is `verdict: FAIL`; the diff of B to S ignoring whitespace-only lines is not empty; S and B are readable. Otherwise write `D/state.json` with `audit: not-triggered(<reason>)`, change nothing else, exit 0.
- sha256 of S and B into `D/state.json`; copy S byte-for-byte to `D/current-before-audit.md`.
- Hunks: line-level `difflib` diff of B to S ignoring whitespace-only lines; hunk ids `H1..Hn`; per hunk the lines in S and in B and bytes added and removed.
- Ids R defines: ids R grades as its own new findings or citation notes; ids R only restates in its prior-findings status table (for example `| F16 | no | open |`) are listed separately as prior-only.
- Ids a hunk cites: whole-word tokens matching `[A-Z][A-Z0-9]*(-[A-Z0-9]+)*[0-9]`, ranges such as `N1-N11` expanded to members first, counted as the multiset difference of current lines over baseline lines.
- Grades: tolerant per-line parse of the four formats (`| MAJOR | blocking |`, `CRITICAL, blocking`, `Severity MAJOR, blocking`, `MAJOR, B` with a key); `non-blocking` is not blocking; a conflicting or unknown grade counts as blocking; record both the severity label (CRITICAL, MAJOR, MINOR or unknown) and the blocking flag per id, because Task 5 needs the label.
- Protection (plan amendment, reflect finding F-02 / recommendation R-002): record a per-id `protected` flag in `D/state.json`, true when the id's severity label is CRITICAL or its grade line in R carries the token `FR-8` or `FR-9` (for example `MAJOR (FR-8 GAP)`), regardless of the blocking flag (./source.md section 3.3 K6 and section 3.5 "grade parse"). A hunk citing a protected id is `blocking-involved`.
- Classes `minor-only`, `blocking-involved`, `foreign-id`, `unattributed` by the rule of ./source.md section 2.3 item 1 "Class", including the disposition `Where` single-line overlap (for example `SPEC':63`) and "no `--dispositions` file means no hunk is `minor-only`"; id-shaped tokens R neither defines nor lists are ignored.
- Skip guard: more than half the hunks `unattributed` writes `audit: skipped(ids not citable)` to `D/state.json` and stops.
- Writes `D/fix-list.md` (hunk table: id, lines in S, lines in B, bytes added and removed, ids cited, grade, class), `D/state.json` (paths, sha256s, ids with label, blocking flag and `protected` flag, prior-only ids, trigger result, audit state) and `D/brief.md` (Task 1's brief with the placeholders replaced by the real paths). The brief is located relative to the script (`../refs/auditor-brief.md`), never through a `src/superclaude` path.
- Exit codes: 0 ok or not-triggered or skipped, 1 on an unreadable input after the trigger check.

Create `tests/skills/test_fix_audit_script.py` with `tmp_path` fixtures covering the "hunks", "id rule", "grade parse" and "classes and guard" bullets of ./source.md section 3.5, plus the Task 1 brief comparison. Load the script by path (`importlib.util.spec_from_file_location`) or run it with `subprocess` and `sys.executable`, as `tests/skills/test_workflow_archive.py` does for `archive_workspace.py`.

Acceptance criteria:
- `uv run pytest tests/skills/test_fix_audit_script.py -q` passes, with at least one test each for: empty and whitespace-only diffs (not triggered, nothing but `state.json` written); insert, delete and replace hunks; ids `N12`, `C9`, `R2-1`, `C-R3-15` matched and bare numbers and partial words not matched; a range `N1-N11` expanded; an id present in the baseline lines is context, not a citation; an id only in R's prior-findings table is not R-defined and makes a hunk citing it `foreign-id`; each of the four grade formats; `non-blocking` read as minor; an unknown or conflicting grade read as blocking; a `MAJOR (FR-8 GAP)` finding graded minor is recorded `protected: true` and a hunk citing it is `blocking-involved`, not `minor-only`; a CRITICAL id is recorded `protected: true`; the four classes on one mixed fixture; a minor-only hunk containing a disposition line of a blocking id becomes `blocking-involved`; no dispositions file gives no `minor-only` hunk; skip guard below, at and above 50% unattributed (at exactly 50% it does not skip); `D/brief.md` contains no `<D>`, `<R>`, `<DISP>`, `<B>` or `<S>` placeholder.
- `D/current-before-audit.md` is byte-identical to S after `prepare` (asserted with `filecmp.cmp(..., shallow=False)`).
- `fix_audit.py` imports only standard-library modules (a test parses its imports with `ast` and checks them against an allowlist).

AC ids: T2.AC1,T2.AC2,T2.AC3 (in the order of the Acceptance criteria bullets). Repo root: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail. Package root (what ./ means in this brief): /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547.
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
Start sha: 8446c587969d893ff1e7fa21c254546fec5814a9
Diff against the start snapshot: saved byte for byte (git diff 8446c587969d893ff1e7fa21c254546fec5814a9 over the touched files src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py, tests/skills/test_fix_audit_script.py, plus full contents of untracked touched files) at /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/diffs/T2-r1-1.diff; read that whole file, and the live files it names
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
