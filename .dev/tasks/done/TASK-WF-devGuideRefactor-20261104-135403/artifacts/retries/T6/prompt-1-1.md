bb2dec2fcf22d202e76368f8842ccd56d9c3c6e9
Review one task for spec compliance.

Task brief: T6 (AC ids in order of the "Acceptance criteria:" bullets: T6.AC1,T6.AC2,T6.AC3,T6.AC4). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 119-132:
## Task 6: Add Orca readiness to the development workflow and testing

Depends on: Task 1

In section 8 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, after reading `tests/skills/test_worker_contract.py` (the `AUDIT_ROOTS`, `WRITE_VERB_RE`, `WRITE_VERB_CLASSIFICATION`, `UNATTENDED_COMMANDS` definitions and the tests that use them):

- `### 8.3 Creating a New Component: Full Workflow`: inside the bash block, add a comment step between "2. Write the component" and "3. Sync to .claude/": decide worker eligibility (WC-2, section 7.6); if the command will accept `--unattended`, write its `## Unattended mode` section and add it to `UNATTENDED_COMMANDS`. Keep the block's comment style.
- `### 8.4 Testing Components`: add an "Orca readiness checks" list that opens with one sentence naming WC-2, WC-4 and WC-9 and linking to `#76-orca-orchestration-commands-as-workers`, then: run `uv run pytest tests/skills/test_worker_contract.py`; its write-verb audit scans the skills, commands and agents under `src/superclaude/` for `git add`, `commit`, `push`, `merge`, `stash`, `update-ref`, `worktree add` and `worktree remove` (also written with `-C <path>`), and for every `gh pr` and `gh api` line, reads included; each matching line needs an entry in `WRITE_VERB_CLASSIFICATION` with a category and a reason, and an entry whose line was edited or removed fails `test_classification_table_has_no_stale_entries`; a command given an `## Unattended mode` section must be added to `UNATTENDED_COMMANDS`, or `test_no_command_has_unattended_mode_section_after_p0` fails; and someone runs the command once without `--unattended` to confirm its prompts, outputs and outward defaults are unchanged.

Acceptance criteria:
- The 8.3 bash block has a comment naming `## Unattended mode`, `UNATTENDED_COMMANDS`, a WC rule ID and "section 7.6", placed before the `make sync-dev` line.
- 8.4's list opens with a sentence naming at least one WC rule ID and linking to `#76-orca-orchestration-commands-as-workers`.
- 8.4 names `tests/skills/test_worker_contract.py`, `WRITE_VERB_CLASSIFICATION`, `UNATTENDED_COMMANDS`, `test_classification_table_has_no_stale_entries` and `test_no_command_has_unattended_mode_section_after_p0`, and its verb list matches `WRITE_VERB_RE`; `grep -n` for each identifier and for `WRITE_VERB_RE` in `tests/skills/test_worker_contract.py` is saved to `./artifacts/t6-test-identifiers.txt`.
- 8.4 does not say the audit catches "any" git or gh write verb, and includes the check that behaviour without `--unattended` is unchanged.

Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md lines 17-34)
## Constraints

- Only one delivery file changes: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`. Do not edit `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, or any command, skill, agent or test file, and add no new test file. Scripts and evidence go under this package's `./artifacts/`.
- Allowed sources. Worker behaviour: `src/superclaude/core/WORKER-CONTRACT.md` (the authority), the "Orca coordination" section at the end of `src/superclaude/core/HOW-WE-WORK.md`, and `~/.claude/skills/orchestration/SKILL.md` (a discovery stub). Rollout phases (section 6), coordinator-only reasons (section 4) and SA-1 to SA-6 (section 5): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, and every sentence taken from it carries a label such as "per the rollout plan". Test behaviour: `tests/skills/test_worker_contract.py`. Per-command facts in 3.2: `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md` or the contract's ready table.
- The guide summarizes contract rules in its own words and points to `~/.claude/WORKER-CONTRACT.md`. It never reproduces the contract's guard line, brief template, coordinator section or the WC-4 error string.
- One home: the never-as-worker list, the person-mode flags, the WC-10 wait limit in minutes, the `worker_status` values with the full WC-4 status mapping, and the description of the WC-4 report-directory error are written out only in 7.6; elsewhere a touchpoint refers to them by rule ID or "section 7.6".
- Pointer rule (source "Pointer rule for touchpoints"): in prose, tables and list items outside code fences, a touchpoint that refers to a 7.6 topic names its rule ID or "section 7.6" and links to `#76-orca-orchestration-commands-as-workers`; this covers the Context Loading sentence, 3.1, 3.2, 3.6, 4.2, 5.9, 5.10, 8.4, 9.1, 9.3, 9.7 and the Appendix E rows. Inside a code fence (the Installation Locations block, the 8.3 bash block, the Appendix A and B templates) it names the rule ID and "section 7.6" as plain text. The table-of-contents entry carries the link only. Appendix A's `## Return Contract` note points only to section 5.9 and names no rule. Appendix D rows carry paths only.
- WC-4 two-case rule. In prose that explains the worker contract file (7.6 and 5.9) both cases are stated in full: a command that already writes `return-contract.yaml` in the report directory itself keeps every existing field, including its own `status`, and adds the worker fields beside them; a command whose own contract lives elsewhere leaves that file unchanged, and the worker contract at `<report-dir>/return-contract.yaml` lists it in `artifacts`. Elsewhere (5.10, 9.3, 9.7, the glossary) a line naming "the WC-4 two-case rule" with a link to 7.6 or 5.9 is enough. No line states the first case without its condition.
- Report directory flag. Wherever the guide lists or defines `--report-dir` (7.6, 3.1, Appendix B, the glossary) it says: a command uses its own directory-valued `--output` or `--output-dir` as the report directory; `--report-dir` is for a command without such a flag, or for a brief that does not pass that flag; passing both, or neither, is refused before any work (WC-4).
- Rule anchors. WC-8 is cited only for a command calling `worker-start`, `dispatch` or `task-create`. "Commands contain no Orca calls" is cited to the contract's opening. "No `orca` or `orca-ide` command anywhere, and no need for Orca to be installed" is cited as "per the rollout plan, SA-2". Agent rules cite WC-7 and WC-8, never WC-13. WC-7 is a worker-session duty.
- Nobody is asked. No new sentence says or implies that a worker session, a command or an agent asks the person or the user under `--unattended`. Under `--unattended` nothing asks the person (WC-2); only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-3). Every added line containing "the person", "the user" or "a person" states that nothing asks them; other new text uses other words (for example "someone" or "a human").
- Skills and agents under a command: the guide presents as its own authoring convention, not as a contract rule, that they follow the command's `## Unattended mode` section (WC-2) and, for a skill's own contract file, the WC-4 two-case rule.
- Every mention of the brief guard says it applies from P1.
- Rollout state as on disk: at P0 no command accepts `--unattended` or `--report-dir`; `tests/skills/test_worker_contract.py` holds `UNATTENDED_COMMANDS: frozenset = frozenset()`. Without `--unattended` every command behaves as it does today.
- New and edited text is plain English and contains no em dash and no en dash, including new checklist items (no dash after the bold label). Existing ones in untouched lines stay.
- When the guide tells an agent or primitive to read a file, it uses the installed path (`~/.claude/WORKER-CONTRACT.md`, `~/.claude/HOW-WE-WORK.md`, `~/.claude/skills/orchestration/SKILL.md`). A `src/superclaude/...` path appears only where the guide describes this repository's own source layout or a maintainer step (the Installation Locations block, 7.6's maintainer edit, 8.4's audit scope, the Appendix D path table), as the guide's "Path rules for primitives" subsection allows.
- Unrelated stale content stays untouched (the stray `p` before the H1 on line 1, the `/sc:task-unified` examples, the 3.4 performance profiles, the nested fences outside Appendix B). Record such findings in the task's evidence notes.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

Start sha: bb2dec2fcf22d202e76368f8842ccd56d9c3c6e9
Diff against the start snapshot: (git diff bb2dec2fcf22d202e76368f8842ccd56d9c3c6e9 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 9b030a79..5f74bf05 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -1112,6 +1112,10 @@ touch src/superclaude/skills/sc-my-skill/refs/scoring.md
 
 # 2. Write the component (see templates in Section 10)
 
+# 2a. Decide worker eligibility (WC-2, section 7.6)
+#    If the command will accept --unattended, write its ## Unattended mode section
+#    and add its name to UNATTENDED_COMMANDS in tests/skills/test_worker_contract.py
+
 # 3. Sync to .claude/ for testing
 make sync-dev
 
@@ -1152,6 +1156,14 @@ git commit -m "feat: add /sc:my-command with agent and skill"
 - Adversarial integration tests: End-to-end with real variant files
 - Edge case tests: Empty inputs, single file, maximum file count
 
+**Orca readiness checks** (for a command that will run as an Orca worker). These checks relate to WC-2, WC-4 and WC-9 ([section 7.6](#76-orca-orchestration-commands-as-workers)):
+
+- Run `uv run pytest tests/skills/test_worker_contract.py`.
+- Its write-verb audit scans the skills, commands and agents under `src/superclaude/` (`AUDIT_ROOTS`) for `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` and `git worktree remove` (also written as `git -C <path> <verb>`), and for every `gh pr` and `gh api` line, reads included.
+- Each matching line needs an entry in `WRITE_VERB_CLASSIFICATION` with a category and a reason. An entry whose line was edited or removed fails `test_classification_table_has_no_stale_entries`.
+- A command given an `## Unattended mode` section must be added to `UNATTENDED_COMMANDS`, or `test_no_command_has_unattended_mode_section_after_p0` fails.
+- Someone runs the command once without `--unattended` to confirm that its prompts, outputs and outward defaults are unchanged.
+
 ### 8.5 Plugin Build Workflow (Future)
 
 The plugin system is planned for v5.0. When available:

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t6-test-identifiers.txt ===
# T6 test identifiers in tests/skills/test_worker_contract.py
$ grep -n 'AUDIT_ROOTS' tests/skills/test_worker_contract.py (first 3)
346:AUDIT_ROOTS = (
386:    for root in map(Path, _THIS.AUDIT_ROOTS):
565:    monkeypatch.setattr(_THIS, "AUDIT_ROOTS", (tmp_path / "skills",))
$ grep -n 'WRITE_VERB_RE' tests/skills/test_worker_contract.py (first 3)
354:WRITE_VERB_RE = re.compile(
395:                found = WRITE_VERB_RE.findall(line)
546:    assert not WRITE_VERB_RE.search("git merge-base master HEAD")
$ grep -n 'WRITE_VERB_CLASSIFICATION' tests/skills/test_worker_contract.py (first 3)
410:        - set(WRITE_VERB_CLASSIFICATION)
418:WRITE_VERB_CLASSIFICATION = {
527:    stale = sorted(set(WRITE_VERB_CLASSIFICATION) - live)
$ grep -n 'UNATTENDED_COMMANDS' tests/skills/test_worker_contract.py (first 3)
203:UNATTENDED_COMMANDS: frozenset = frozenset()
250:    assert set(have) == set(UNATTENDED_COMMANDS), f"unexpected `## Unattended mode` sections: {have}"
$ grep -n 'test_classification_table_has_no_stale_entries' tests/skills/test_worker_contract.py (first 3)
525:def test_classification_table_has_no_stale_entries():
$ grep -n 'test_no_command_has_unattended_mode_section_after_p0' tests/skills/test_worker_contract.py (first 3)
269:def test_no_command_has_unattended_mode_section_after_p0():
# WRITE_VERB_RE definition
357-range: WRITE_VERB_RE = re.compile(
357-range:     r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))"
357-range:     r"|gh\s+(?:pr|api))(?![\w-])"
357-range: )

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
