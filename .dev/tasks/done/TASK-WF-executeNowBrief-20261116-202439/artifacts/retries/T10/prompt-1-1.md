da7febe1d0d070ec09a74c6ec15a00ecda21ef54
Review one task for spec compliance.

Task brief: ## Task 10: State that QUESTION-OBSERVATION passed on 2026-11-12 where it still says not passed (D2)

Depends on: Task 4

Change the QUESTION-OBSERVATION status wording only, so each place says the gate passed on 2026-11-12 on the terms of the owner-written record `.dev/issues/409/owner-pass-record-20261112.md` (cite that path): `.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 106 and 491; `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md` line 27; `.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md` lines 3 and 62 (line 62 also says the owner has not named the Run; the owner record names `run_93bfa00cae2b`); `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` line 89; and in `src/superclaude/cli/observe/commands.py` the comment above `QUESTION_GATE_PASSED` (:63-66; keep the strings `release-gates.md` and `Task 18` in it, because `tests/observe/test_commands.py:750` asserts both appear in the file text), the HELP text (:86-88, "off until the owner records that QUESTION-OBSERVATION passed") and the `--questions` option help (:452-453, "refused until QUESTION-OBSERVATION has passed"). Do not edit `QUESTION_GATE_TEXT` (pinned), any DIRECTION-SELECTED line, `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` (lines 12 and 38 are already correct) or the untracked `handoff-mvp-brainstorm.md`. Keep the disclosure label and the sentence that the observer never runs run-use in the help text.

Acceptance criteria:
- Grep for `NOT passed`, `not passed` and `has not passed` near QUESTION-OBSERVATION in the files above finds no live claim that the gate has not passed; the refusal text `question read not enabled: QUESTION-OBSERVATION has not passed` in `QUESTION_GATE_TEXT` is unchanged.
- `uv run pytest tests/observe/test_commands.py tests/observe/test_registration.py -q` passes, including the tests that read the help text (`never runs run-use`, the disclosure label, `one named Run`) and the guard test that requires `release-gates.md` and `Task 18` in the source text.
- No other line of these files changes (`git diff` is limited to the status wording); the full gate passes with the passed count unchanged.
Global constraints: 
- Shorthand. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. The debate's final list and its row text are copied into `./source.md`; each task below restates what it needs.
- Scope is these eleven rows only. No commit, no push, no pull request. Every other row of the debate (KEEP, owner decisions, low confidence) is out of scope.
- Never touch: the sanitizer (`PKG/sanitize.py` and its use), the argv allow-list and forbidden verbs in `PKG/adapter.py`, process-group kill and output caps, terminal restore on exit and signals, the rule that message bodies, payload and `to_handle` are never kept, snapshot redaction, the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, `QUESTION_GATE_TEXT` in `PKG/commands.py` (pinned by `TESTS/test_commands.py`), any DIRECTION-SELECTED line, and any file git does not track (for example `.dev/issues/409/handoff-mvp-brainstorm.md`).
- Line numbers in the tasks were read live on 2026-11-16 at HEAD f104ca51a and are leads only: re-grep every target right before editing, because other sessions share the worktree.
- Gate for every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and `uv run ruff check src/superclaude/cli/observe tests/observe` is clean. The baseline is 694 passed; the passed count falls only by the test functions a task deliberately deletes, and the task states the number it expects and the number it got. UV only; never bare python or pip. A failing gate is reported as a finding and never loosened to pass.
- Edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Whole-package checks, applied by the final review and not tasks of their own: Task 1 first saves `git status --short` to `./artifacts/baseline-status.txt`; at the end `git status --short` differs from that baseline only by the files these tasks name, `.dev/issues/409/` and this package; the full gate passes with the passed count equal to 694 minus the test cases the tasks removed (9 in Task 1 and 1 in Task 9, so 684, unless Task 6 had to remove an aggregate-only test); and `grep -rn "run-use" src/superclaude/cli/observe/` shows `run-use` only in the forbidden set in `PKG/adapter.py` and in the help text that says the observer never runs it.
- Names, not line numbers, wherever a check or a document points at code, because earlier tasks shift line numbers (for example `_question_refusal` in `PKG/commands.py`). A Grep check below means uses of the named symbol, not test function names that merely contain the word (`tests/observe/test_questions.py:50` and `tests/observe/test_view.py:174` keep such names).
- Labels. T5, T7, T8 and T9 in task titles are the debate's row names; the spec test ids in Task 12 are written "spec test T7", "T17", "T45" and "T50".
- Facts the debate found false in the earlier proposal, not to be repeated: the R1 test ranges were too wide, R3 must not drop the five parsed row fields, T9 keeps the `test_render.py` copy and deletes the `test_terminal.py` copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches owner decisions 6 and 8 only.
Start sha: da7febe1d0d070ec09a74c6ec15a00ecda21ef54
Diff against the start snapshot: diff --git a/.dev/issues/409/bmad/prd-orca-observer/prd.md b/.dev/issues/409/bmad/prd-orca-observer/prd.md
index af2092608..c7889fef3 100644
--- a/.dev/issues/409/bmad/prd-orca-observer/prd.md
+++ b/.dev/issues/409/bmad/prd-orca-observer/prd.md
@@ -105,3 +105,3 @@ The owner chose a staged direction (binding): R1 = Signal Bridge's worker ledger
 | R1 Live worker-list | COUNTS strip, freshness strip, worker ledger with verbatim `nextAction.kind`, `result.counts`, capped paging, stale handling, changes since last look, the selected view, the question-source notice, the JSON snapshot export. | DIRECTION-SELECTED passed, production integration permitted under the reading the owner confirms, a redacted golden sample of each of the four kinds, contract test T32. | Closed |
-| R2 Attention Ledger (B) | `COORDINATOR QUESTIONS` for one named Run (messages of type `question` only), with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". One Run only, no rotation. | QUESTION-OBSERVATION: **NOT passed**. Candidate verb, never an available source until the open items are recorded: `orca orchestration check --all --types question --run <runId> --json` for one named Run, never `run-use`, one message call per cycle inside the 5-call cap. Open items (`release-gates.md`): Q-1 (an observer terminal with a handle but no Run, UNVERIFIED), the message rate and identity on the Run the owner names (the owner has not named it), and the owner's written pass record. Seen on probe Runs only: the read returns only the bound Run's mailbox (`consumer_fenced` for another Run), and non-consumption as the Run's owner for the visible effects tested (INV-022, T51). Question identity is `message.id`, a worker `dispatchId` is never a question's identity. Owner decisions 8 and 6 decided 2026-11-11 (coordinator questions only; one named Run, `--types question`, never `run-use`). | Closed |
+| R2 Attention Ledger (B) | `COORDINATOR QUESTIONS` for one named Run (messages of type `question` only), with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". One Run only, no rotation. | QUESTION-OBSERVATION: **passed 2026-11-12** on the terms of the owner-written record `.dev/issues/409/owner-pass-record-20261112.md`. Candidate verb, read only while that record stands: `orca orchestration check --all --types question --run <runId> --json` for one named Run, never `run-use`, one message call per cycle inside the 5-call cap. Still open after the pass (`release-gates.md`): Q-1 is answered FAIL (an observer terminal that holds no Run cannot read; accepted in the owner record), and the message rate and identity on real traffic are unmeasured. The Run is `run_93bfa00cae2b`, named in the owner record. Seen on probe Runs only: the read returns only the bound Run's mailbox (`consumer_fenced` for another Run), and non-consumption as the Run's owner for the visible effects tested (INV-022, T51). Question identity is `message.id`, a worker `dispatchId` is never a question's identity. Owner decisions 8 and 6 decided 2026-11-11 (coordinator questions only; one named Run, `--types question`, never `run-use`). | Closed |
 | R3 Decision Desk (C) | For the selected question, affected sessions with worker-list evidence. | QUESTION-LINK: authoritative mapping from IDs in a message to `dispatchId`/`worktreeId`, verified on this host first; optional owner re-confirm of the post-link default (B or C). No named decider beyond that. | Closed |
@@ -490,3 +490,3 @@ The source table has no ids; U1-U19 are extractor row numbers.
 | U2 | Meaning of `result.count` | No count is ever derived from it |
-| U3 | QUESTION-OBSERVATION open items: Q-1, message rate and identity on the named Run, the owner's written pass record (proof (a) as first worded is withdrawn, `release-gates.md`) | Gate stays closed (NOT passed) |
+| U3 | QUESTION-OBSERVATION open items after the pass: Q-1 (answered FAIL), message rate and identity on real traffic (proof (a) as first worded is withdrawn, `release-gates.md`) | Gate passed 2026-11-12 on the owner-written record `.dev/issues/409/owner-pass-record-20261112.md`; these items stay open |
 | U4 | Whether the coordinator agent or a person answers a `question` row (Orca has no human recipient field) | Decided 2026-11-11 (OQ-7): the list reads "coordinator questions" |
diff --git a/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md b/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
index ac7b576b8..99aec3bd5 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
@@ -2,3 +2,3 @@
 
-**Scope.** R0 runs nothing against Orca. R1 has one verb: `orca orchestration worker-list --json --limit 100`, with optional `--run <runId>` and `--cursor <c>`, plus the one-time binary discovery below (run once before the first cycle, at most one `skills list --json` probe per candidate, so at most two, and not among a cycle's 5 subprocesses). The one R2 message template (below, "Argv allow-list") is used only after the QUESTION-OBSERVATION gate record exists (`release-gates.md`; status: not passed as of 2026-11-11).
+**Scope.** R0 runs nothing against Orca. R1 has one verb: `orca orchestration worker-list --json --limit 100`, with optional `--run <runId>` and `--cursor <c>`, plus the one-time binary discovery below (run once before the first cycle, at most one `skills list --json` probe per candidate, so at most two, and not among a cycle's 5 subprocesses). The one R2 message template (below, "Argv allow-list") is used only while the QUESTION-OBSERVATION gate record exists (`release-gates.md`; passed 2026-11-12, owner record `.dev/issues/409/owner-pass-record-20261112.md`).
 
@@ -61,3 +61,3 @@
 - **One named Run, no rotation:** R2 reads one named Run only. The observer never binds to a Run (it never runs `run-use`); it must run where it already holds the Run, because a caller bound to another Run is fenced (`consumer_fenced`) and a caller with no terminal identity gets `no_active_terminal`. The rotation set and the `revisit ~Ns` token are removed. For messages the header reads `one Run only` plus the named Run; `read k of N Runs since start` is not a message-source behaviour.
-- **Acquisition permission (INV-017):** decision 6 is granted for one named Run (OWNER, `owner-decisions-20261111.md`, 2026-11-11: one named Run, `--types question`, never `run-use`), and the Run must be named before the first call (the owner has not named it yet; no message call is made until then). Permission must cover the actual read scope before a message call, separately from display and export permission. Dropping a body at parse time cannot undo its receipt, so the design never claims bodies were not acquired, only that they are not kept or shown; if a narrow read cannot honour the permission the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.
+- **Acquisition permission (INV-017):** decision 6 is granted for one named Run (OWNER, `owner-decisions-20261111.md`, 2026-11-11: one named Run, `--types question`, never `run-use`), and the Run must be named before the first call (the owner record names `run_93bfa00cae2b`, the coordinator's own Run, which the observer terminal already holds). Permission must cover the actual read scope before a message call, separately from display and export permission. Dropping a body at parse time cannot undo its receipt, so the design never claims bodies were not acquired, only that they are not kept or shown; if a narrow read cannot honour the permission the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.
 
diff --git a/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md b/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md
index 9943778f8..c0e189804 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md
@@ -88,3 +88,3 @@ The first observation in a process is the baseline; a restart discloses that a n
 | Plain `check`, `--ack`, `--wait`, `--retry-request` | Plain `check` and `--ack` consume a delivery; `--wait` is a listener on the bound Run's FIFO. Forbidden set never shrinks (`adapter-contract.md`). |
-| Parsing `check --peek/--all` or `inbox --json` rows before QUESTION-OBSERVATION | Row fields UNVERIFIED; `check --all --types question --run <runId> --json` is the one candidate verb, behind the gate (status: not passed). |
+| Parsing `check --peek/--all` or `inbox --json` rows before QUESTION-OBSERVATION | Row fields UNVERIFIED; `check --all --types question --run <runId> --json` is the one candidate verb, behind the gate (status: passed 2026-11-12, owner record `.dev/issues/409/owner-pass-record-20261112.md`). |
 | Live question age, requester, owner | They exist only in message rows; `lastObservedAt` is an observation time, not a question open time. |
diff --git a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
index 0db2e5882..a2f28d999 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
@@ -26,3 +26,3 @@ The MVP (R0, R1) needs exactly one live source.
 
-`check --all --types question --run <runId> --json`, for one named Run, is a candidate, never an available source, until the open items in `release-gates.md` (QUESTION-OBSERVATION: not passed) are recorded. Not used in R0 or R1: `check --peek`, the candidate `check --all`, `inbox`. Unfiltered `check --all` and `--peek` are not allowed in any R2 argv; plain `check`, `--ack` and `run-use` are never run.
+`check --all --types question --run <runId> --json`, for one named Run, is an available source only under the owner-written record `.dev/issues/409/owner-pass-record-20261112.md` (QUESTION-OBSERVATION: passed 2026-11-12; the open items in `release-gates.md` stay open). Not used in R0 or R1: `check --peek`, the candidate `check --all`, `inbox`. Unfiltered `check --all` and `--peek` are not allowed in any R2 argv; plain `check`, `--ack` and `run-use` are never run.
 
diff --git a/src/superclaude/cli/observe/commands.py b/src/superclaude/cli/observe/commands.py
index 0490ecc9b..b8fbcd27f 100644
--- a/src/superclaude/cli/observe/commands.py
+++ b/src/superclaude/cli/observe/commands.py
@@ -62,6 +62,6 @@ WIDTHS = ("160", "116", "80")
 
-# The live coordinator-questions read is guarded by this one constant. It stays False until
-# the owner has given a record that QUESTION-OBSERVATION passed (release-gates.md, "Agents
-# cite the owner's statement"); plan Task 18 flips it only against that
-# record, cited by path. While False, ``--questions`` makes no Orca call, not even discovery.
+# The live coordinator-questions read is guarded by this one constant. It is True because
+# the owner gave a record that QUESTION-OBSERVATION passed (release-gates.md, "Agents
+# cite the owner's statement"); plan Task 18 flipped it only against that
+# record, cited by path. When False, ``--questions`` makes no Orca call, not even discovery.
 QUESTION_GATE_PASSED = True  # owner record: .dev/issues/409/owner-pass-record-20261112.md
@@ -86,4 +86,5 @@ observers running at once multiply the load on Orca.
 
-Coordinator questions (--questions, off until the owner records that QUESTION-OBSERVATION
-passed): with --run <runId> the observer lists the messages of type question of that one
+Coordinator questions (--questions; QUESTION-OBSERVATION passed on 2026-11-12, owner
+record .dev/issues/409/owner-pass-record-20261112.md): with --run <runId> the observer
+lists the messages of type question of that one
 named Run, from one read per cycle. Run it from the terminal that already holds the Run: the
@@ -451,3 +452,4 @@ def _check_run(
     help="List the coordinator questions (message type question) of the one Run named by "
-    "--run. Needs --run and a live source; refused until QUESTION-OBSERVATION has passed.",
+    "--run. Needs --run and a live source; QUESTION-OBSERVATION passed on 2026-11-12 "
+    "(owner record .dev/issues/409/owner-pass-record-20261112.md).",
 )
Evidence this task produced (machine output of the gate, file /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/artifacts/t10-gate.log):
== grep (each pattern expected to match nothing)
== pytest
.                                                                        [100%]

============================= 684 passed in 22.75s =============================
== ruff
All checks passed!
== remaining 'not passed' wording near QUESTION-OBSERVATION in the task's files (expect only QUESTION_GATE_TEXT at commands.py)
src/superclaude/cli/observe/commands.py:69:    "question read not enabled: QUESTION-OBSERVATION has not passed"  # PROPOSED wording
.dev/issues/409/bmad/prd-orca-observer/prd.md:464:1. **Visual direction (DIRECTION-SELECTED).** Dated, owner-written selection record (never an agent): (a) default while no question rows exi
== guard-test strings still in commands.py
64:# the owner gave a record that QUESTION-OBSERVATION passed (release-gates.md, "Agents
65:# cite the owner's statement"); plan Task 18 flipped it only against that
== help tests

============================== 40 passed in 1.69s ==============================
== files changed
 tests/observe/test_fixtures.py                     | 14 ++++++--
 tests/observe/test_golden_contract.py              |  5 ---
 tests/observe/test_question_quiet_scope.py         | 14 --------
 tests/observe/test_questions.py                    |  4 +--
 tests/observe/test_render.py                       |  7 +---
 tests/observe/test_snapshot_schema.py              | 17 +++++-----
 tests/observe/test_terminal.py                     | 35 +-------------------
 23 files changed, 61 insertions(+), 214 deletions(-)
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
