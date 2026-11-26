965c61228949cfb55d679604e496bca4019aa702
Review one task for spec compliance.

Task brief: Task 1: Extend the performance row and explain leak ambiguity

In src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md, Wave 0 step 2, append the exact phrases "too long to load", "takes forever" and "hangs" to the existing performance row. Retain "leak" in both existing rows and add a short rationale next to the ambiguity rule: a leak may mean resource leakage or disclosure, so an ambiguous report must remain untyped rather than silently discard security candidates. Keep the existing command and Wave 3 specialist selection unchanged. Inspect existing coverage under tests/ before deciding whether its conditional test requirement applies. Run make sync-dev and make verify-sync after the edit; record their actual outcomes under ./artifacts/ without staging generated mirrors.

Acceptance criteria:
- The performance row contains all three new phrases and keeps its existing cues.
- Both leak listings remain; the written reason preserves the existing leave-type-unset ambiguity rule, including security candidates for Tier 2. Other keyword rows and escalation behavior are unchanged.
- The command src/superclaude/commands/troubleshoot.md still supports auto-detection and explicit --type; Wave 3 still uses performance-engineer and root-cause-analyst for performance, and security-engineer for security. No command-file change is required.
- Coverage inspection records where it searched and what it found. Existing phrase/table coverage is extended only if found; otherwise no new test framework is introduced.
- make sync-dev and make verify-sync run after the edit, and verify-sync exits zero. Their output is retained in ./artifacts/; only canonical source and task-package evidence are staged.

AC ids:
T1.AC1: The performance row contains all three new phrases and keeps its existing cues.
T1.AC2: Both leak listings remain; the written reason preserves the existing leave-type-unset ambiguity rule, including security candidates for Tier 2. Other keyword rows and escalation behavior are unchanged.
T1.AC3: The command src/superclaude/commands/troubleshoot.md still supports auto-detection and explicit --type; Wave 3 still uses performance-engineer and root-cause-analyst for performance, and security-engineer for security. No command-file change is required.
T1.AC4: Coverage inspection records where it searched and what it found. Existing phrase/table coverage is extended only if found; otherwise no new test framework is introduced.
T1.AC5: make sync-dev and make verify-sync run after the edit, and verify-sync exits zero. Their output is retained in ./artifacts/; only canonical source and task-package evidence are staged.
Global constraints: 

- Follow ./source.md and the original acceptance criteria of issue 610. Nothing to decide: build what the issue asks for, within its own scope.
- No Jev call, preflight component, gateway change, or changes to other keyword rows beyond the leak decision. Do not redesign the classifier or force Tier 2 escalation.
- Edit canonical source only. Generated .claude/ copies are never staged; .dev/issues/ is not staged. Stage .dev/tasks/, including its artifacts. Commit, push and pull request work remain outside this plan and follow the story's later steps.
- Add or extend a test only if existing repository coverage tests this table; otherwise preserve manual evidence instead of inventing a new matcher or test system.
- Do not change the installed user-wide skill just to make a check pass. The manual run must consume the changed checkout skill, not silently exercise the old installed row.


Start sha: 965c61228949cfb55d679604e496bca4019aa702
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md b/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
index d7f0a1aed..76bcb3d94 100644
--- a/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
@@ -152,11 +152,11 @@ Each wave has explicit entry/exit criteria. Refs are loaded per-wave, never pre-
 2. Auto-detect `--type` if not provided. Use keyword + structural cues from the issue description:
    - Stack trace, exception name, `undefined`/`null`/`NameError` → `bug`
    - "tsc", "ts(", "compiled", "lint", "build", `make`, CI log fragments → `build`
-   - "slow", "latency", "p99", "memory", "leak", profiler output → `performance`
+   - "slow", "latency", "p99", "memory", "leak", "too long to load", "takes forever", "hangs", profiler output → `performance`
    - "production", "deploy", "container", "env var", "service won't start" → `deployment`
    - "auth", "token", "leak", "exposed", "CVE", "vulnerab" → `security`
    - "pytest", "jest", "flake", "intermittent", "passing locally" → `test`
-   - On ambiguity, leave `--type` unset and treat all agent specialties as candidates for Tier 2.
+   - On ambiguity, leave `--type` unset and treat all agent specialties as candidates for Tier 2. Keep "leak" in both rows: it can mean resource leakage or sensitive-data disclosure, so ambiguous leak reports must not discard security candidates.
 3. Resolve `--scope` to a concrete path/symbol. If given, narrow auggie/codegraph queries and Grep/Read lookups to that target.
 4. Compute output slug: `<type-or-untyped>-<first-5-words-of-issue-or-scope>-<YYYYMMDDHHMMSS>` and create `<output-dir>/`.
 5. Open audit log; emit machine-readable header:

Task-owned artifacts to Read: .dev/tasks/to-do/TASK-WF-issueSummary-20261126-115114/artifacts (exclude retries). For Task1 read sync-dev.log, verify-sync.log and coverage-inspection.txt. For Task2 read manual-evidence.txt, classification stream/audit and pytest.log plus issue-comment.url. New evidence files absent from snapshot are included in full by Reading these actual paths.
Codegraph context: index_state:stale checked_at:2026-11-26T11:57:10Z worktree_root/projectPath:/home/coder/workspaces/worktrees/IronClaude/issue-610. call codegraph only when index_state: fresh, never to widen scope. Q2b used Grep/Read; command and Wave3 lenses unchanged, install/contract tests depend on canonical skill.
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
