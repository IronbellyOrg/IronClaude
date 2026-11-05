e39a3a458bb2c14a77712141e5f0812dbbaf0f36
Review one task for spec compliance.

Task brief: ## Task 5: Add `tests/skills/test_worker_contract.py` for the contract's rules

Depends on: Task 3

Create `tests/skills/test_worker_contract.py`. It reads the contract from a module-level path constant (default `src/superclaude/core/WORKER-CONTRACT.md`) that tests can monkeypatch. For each rule `./source.md` section 2.1 assigns to the file, it asserts the phrase recorded for that rule in `./artifacts/t1-rule-phrases.md`. Copy the phrases into the test as data; the test must not read the artifact. Each phrase carries the rule's meaning, not only its label:
- each WC identifier from Tasks 1 and 2 with its rule's recorded phrase;
- the four refusal conditions, the three exact reason texts and the case-3 `guard refused:` prefix;
- the never-as-worker list (all seven commands);
- the nested propagation rule;
- the WC-4 missing-directory error text;
- the WC-5 outcome mapping and its P0 override;
- the section 2.3 rule that dependents are created only after their inputs settle;
- the fan-in caps "maximum of 10 inputs" and "at least 2 inputs are admitted";
- the guard line, and that it comes before the first `Command:` line of the brief template.

If Task 3 added `plugins/superclaude/core/WORKER-CONTRACT.md`, the test also asserts that this copy is byte-identical to `src/superclaude/core/WORKER-CONTRACT.md`. Follow the pattern of `test_plugin_mirror_matches_src` in `tests/commands/test_workflow_command.py`.

It also asserts that no file in `src/superclaude/commands/` has an `## Unattended mode` section, because no command accepts `--unattended` after P0 (`./source.md` section 6 table, P0 row); later phases extend this list.

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.
- A negative check makes the matching assertion fail for each rule removed from a `tmp_path` copy of `WORKER-CONTRACT.md` that the path constant is monkeypatched to. The negative check is run by a test in the same file or recorded in `./artifacts/t5-negative-check.txt`, and no scratch file is written under `src/superclaude/`.

AC ids, in the order of the Acceptance criteria bullets: T5.AC1, T5.AC2.
Package root (resolves ./artifacts/ and ./source.md): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232
Global constraints: ## Constraints

- This is the static plan of Phase P0 (`./source.md` section 6, last paragraph: each phase's plan has a static part and a live part). It covers AC-0.1, AC-0.2, AC-0.3, AC-0.7 and AC-0.9 (section 7.3), and the common checks AC-C1, AC-C2, AC-C3, AC-C5 and AC-C6 (section 7.1). AC-C4 is checked on the index at the end of this plan and again by the coordinator at commit time. The live checks (AC-0.4, AC-0.5, AC-0.6) and the P0 phase report belong to the P0 live plan, which is written after this plan's checks pass. AC-0.8 is a P1 check (section 7.3). Phases P1-P4 get their own plans later; they are not dropped.
- No task in this plan commits, installs into `~/.claude`, starts an Orca worker or asks the owner a question. Between this plan and the live plan, the coordinator session asks the owner, commits and runs `uv run superclaude install --force`, as `./source.md` section 7.2 states, outside any plan run. `/sc:implement` may not prompt the user outside its halt paths (`./source.md` section 6, last paragraph).
- P0 edits no command file, no `SKILL.md` and no agent file (`./source.md` section 6, P0 row: "no command edits"). The only file this plan writes inside a skill package (`src/superclaude/skills/` or `plugins/superclaude/skills/`) is the byte-for-byte copy of `HOW-WE-WORK.md` at `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` that Task 4 makes. `tests/skills/test_worker_contract.py` is a test file, not a skill package. The `.claude/` copies that `make sync-dev` writes are sync output. No command gains `--unattended` or an `## Unattended mode` section in P0 (section 6, table "Which commands accept `--unattended`", P0 row: none).
- `WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 say and adds no rule the spec lacks. The one exception is the brief template, which also carries the section 3.1 "Brief must pass" flags and the section 6 phase markers (`--report-dir` marked "from P1"). For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats), the contract states only the IronClaude-specific rule and points to the dispatch preamble for Orca verb syntax and heartbeat cadence, never copying them (section 2.1, "Contract file"). These duties are not copied in full. Task 5 pins them by the short phrases that Tasks 1 and 2 record. This no-copy rule does not cover the coordinator's brief template, whose guard line and `worker_done` text are copied word for word from section 2.3 "Brief layout".
- `WORKER-CONTRACT.md` and the new `HOW-WE-WORK.md` section are installed files, so they use installed paths only (`~/.claude/...`). They copy none of the spec's evidence ids (`CAPS:`, `INV-`, `EVIDENCE.md:`) and no `src/superclaude/...` or other repo-path citations (repo `CLAUDE.md`, "Never Hardcode `src/superclaude/` Paths in Installed Primitives"). Where a rule needs to cite a skill file (for example `ledger.md:71` or `refs/retry.md:498` in the section 2.3 resume check), the citation is rewritten as an installed path, such as `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.
- `src/superclaude/` is the source of truth. After editing it, run `make sync-dev`; never stage `.claude/` paths other than `.claude/settings.json` (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"). `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- No command, skill or agent file may name `orca` or `orca-ide` verbs (`./source.md` SA-2, AC-C1). Only `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`, and their plugin copies, may describe the coordinator side.
- Every git and GitHub outward action targets `IronbellyOrg/IronClaude` only; SuperClaude upstream is never pushed to or interacted with (`./source.md` section 2.3, "Git and GitHub ownership"). This plan pushes nothing and opens no PR.
- Orca checks in this plan are read-only: no Orca command that starts, sends or creates anything is run.
- Use `uv run` for all Python.
Start sha: e39a3a458bb2c14a77712141e5f0812dbbaf0f36
Diff against the start snapshot: Files present in the start tree (diff against the start tree):
```diff
```
New untracked files written by this task (absent from the start tree; the whole file is the diff, Read each in full from disk):
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/skills/test_worker_contract.py
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t5-test-run.txt

Delta diff from the previous reviewed tree (empty on the first review): ```diff
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index fb4eef34..f083cb10 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -60,6 +60,13 @@ RULE_PHRASES = {
         ["(case 3) the command is on the never-as-worker list; the body still starts `guard refused:`"],
     ),
     "brief-guard-prefix": (None, ["a body starting `guard refused:`"]),
+    "never-as-worker": (
+        "**Never-as-worker list**",
+        [
+            "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "
+            "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"
+        ],
+    ),
     "nested-propagation": (
         None,
         [
diff --git a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t5-test-run.txt b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t5-test-run.txt
index a86d265d..7ac461d1 100644
--- a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t5-test-run.txt
+++ b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t5-test-run.txt
@@ -1,5 +1,5 @@
 $ uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider
-============================== 89 passed in 0.15s ==============================
+============================== 91 passed in 0.14s ==============================
 rc=0
 $ uv run pytest tests/skills/test_worker_contract.py -v -p no:cacheprovider -k "fails" (negative checks)
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-10] PASSED [  2%]
@@ -13,30 +13,31 @@ tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-4-missing-directory-error] PASSED [ 18%]
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-5] PASSED [ 20%]
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-5-P0-override] PASSED [ 22%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-6] PASSED [ 25%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-7] PASSED [ 27%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-8] PASSED [ 29%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-9] PASSED [ 31%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-contents] PASSED [ 33%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-case-1] PASSED [ 35%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-case-2] PASSED [ 37%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-case-3] PASSED [ 39%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-copies-disagree] PASSED [ 41%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-prefix] PASSED [ 43%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-scope] PASSED [ 45%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-layout] PASSED [ 47%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-template] PASSED [ 50%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[dependents-after-settle] PASSED [ 52%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[fan-in-max] PASSED [ 54%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[fan-in-min] PASSED [ 56%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[flag-parse-rule] PASSED [ 58%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[git-github-ownership] PASSED [ 60%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[heartbeats] PASSED [ 62%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[implement-stop] PASSED [ 64%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[nested-propagation] PASSED [ 66%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[person-mode-refusal] PASSED [ 68%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[read-before-depend] PASSED [ 70%]
-tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[report-directory] PASSED [ 72%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-6] PASSED [ 24%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-7] PASSED [ 26%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-8] PASSED [ 28%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[WC-9] PASSED [ 30%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-contents] PASSED [ 32%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-case-1] PASSED [ 34%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-case-2] PASSED [ 36%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-case-3] PASSED [ 38%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-copies-disagree] PASSED [ 40%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-prefix] PASSED [ 42%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-guard-scope] PASSED [ 44%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-layout] PASSED [ 46%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[brief-template] PASSED [ 48%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[dependents-after-settle] PASSED [ 51%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[fan-in-max] PASSED [ 53%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[fan-in-min] PASSED [ 55%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[flag-parse-rule] PASSED [ 57%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[git-github-ownership] PASSED [ 59%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[heartbeats] PASSED [ 61%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[implement-stop] PASSED [ 63%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[nested-propagation] PASSED [ 65%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[never-as-worker] PASSED [ 67%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[person-mode-refusal] PASSED [ 69%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[read-before-depend] PASSED [ 71%]
+tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[report-directory] PASSED [ 73%]
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[unattended-mode] PASSED [ 75%]
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[worker-run] PASSED [ 77%]
 tests/skills/test_worker_contract.py::test_rule_check_fails_when_rule_removed[worktrees] PASSED [ 79%]
@@ -50,7 +51,7 @@ tests/skills/test_worker_contract.py::test_never_as_worker_check_fails_when_comm
 tests/skills/test_worker_contract.py::test_guard_order_check_fails_when_guard_follows_command PASSED [ 95%]
 tests/skills/test_worker_contract.py::test_guard_order_check_fails_when_guard_line_removed PASSED [ 97%]
 tests/skills/test_worker_contract.py::test_unattended_section_check_fails_on_unlisted_command PASSED [100%]
-====================== 48 passed, 41 deselected in 0.12s =======================
+====================== 49 passed, 42 deselected in 0.12s =======================
 rc=0
 $ git status --short src/superclaude
  M src/superclaude/cli/install_core.py
```
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/tests/skills/test_worker_contract.py:215 anchor="it asserts the phrase recorded for that rule in `./artifacts/t1-rule-phrases.md`" chk=n,n,n,y family=phrase-coverage fix=add a "never-as-worker" entry to RULE_PHRASES with the recorded phrase "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers" (artifact t1-rule-phrases.md:23), or extend _check_never_as_worker to assert the D3 qualifier covers="Each phrase carries the rule's meaning, not only its label" first=A1 origin=new: The never-as-worker rule is the only rule whose recorded phrase is not in the test's data. `_check_never_as_worker` checks only that the seven command names appear on the list line, so the condition that keeps `/sc:pr-submit` on the list (the D3 answer) is not pinned. I tested this on a copy under /tmp: I replaced "while the answer to decision D3 keeps it off workers" with "always" in the contract and all 8 never-as-worker tests still passed. Every other recorded phrase in t1-rule-phrases.md, 70 in all, is copied into RULE_PHRASES or GUARD_LINE.
Saved-probe re-check hit locations (may be empty): tests/skills/test_worker_contract.py:67
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md:23
src/superclaude/core/WORKER-CONTRACT.md:23

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
