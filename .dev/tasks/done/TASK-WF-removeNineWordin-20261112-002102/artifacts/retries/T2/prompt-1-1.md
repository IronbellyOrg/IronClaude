648df04e7e22b5f7e92b3769fe8f94fa43881ca6
Review one task for spec compliance.

Task brief: ## Task 2: Mirror the guide into plugins/superclaude/core/CODEGRAPH.md

Depends on: Task 1

Copy `src/superclaude/core/CODEGRAPH.md` byte for byte to `plugins/superclaude/core/CODEGRAPH.md`, because `test_plugin_copy_is_byte_identical` in `tests/core/test_codegraph_guide.py` pins them identical.

Acceptance criteria:
- `cmp src/superclaude/core/CODEGRAPH.md plugins/superclaude/core/CODEGRAPH.md` prints nothing.

AC ids:
T2.AC1: `cmp src/superclaude/core/CODEGRAPH.md plugins/superclaude/core/CODEGRAPH.md` prints nothing.
Global constraints: - Edit only `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md`, `src/superclaude/core/CODEGRAPH.md`, `plugins/superclaude/core/CODEGRAPH.md` (a test pins it byte-identical to the source), `tests/skills/test_codegraph_adoption.py` and `tests/core/test_codegraph_guide.py`. The plugin twins of analyze.md and design.md already differ from the source (no codegraph text, `mcp-servers: []`) and no test pins them, so they stay untouched. `scripts/eval_workflow_vs_task_builder.py` pins skill tool lists, which this plan does not change, so it stays untouched unless a test run shows otherwise.
- Do not change behaviour, flags, the one-check-per-run rule, the fresh-and-`access: mcp` rule, the Grep/Read floor or the never-halt rule. Every fix is a clause or one sentence.
- `src/superclaude/core/CODEGRAPH.md` is shared by every primitive: additive clarifications only; it stays at 120 lines or fewer, names no `src/superclaude/` path, adds no `graph:*` token outside the closed list of its section 3 (which already holds `graph:empty` and `graph:truncated`), and names `explore` and the mutating verbs only in its Never section. Each phrase changed is grepped across `src/superclaude` first so no other primitive contradicts it.
- Reference the smoke report only through `./source.md`; never add a `src/superclaude` read path to an installed primitive. Never stage `.claude/`; no commit, no push, no PR.
- All nine report quotes were re-verified against the worktree before planning: the quotes sit at the stated lines of analyze.md (30, 32, 36, 63, 67), design.md (55, 57, 61, 65, 74) and CODEGRAPH.md (13, 22, 50, 74). None is rebutted.
Start sha: 648df04e7e22b5f7e92b3769fe8f94fa43881ca6
Diff against the start snapshot: 

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
