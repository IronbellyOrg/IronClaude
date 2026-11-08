651fb0e3be5e92da95891c886044a8dde836a78b
Review one task for spec compliance.

Task brief: ## Task 1: Replace the WC-10 closing sentence (C-1) and extend WC-11 (C-17)

In `src/superclaude/core/WORKER-CONTRACT.md` section 2, replace the last sentence of WC-10 ("The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late, and it acts only on Orca's stall proofs.") with the C-1 wording from design section 10.2: absence is never death; stop, retry or release only on Orca's stall proofs or the person's recorded stop under WC-6; absence past the deadline in "Liveness supervision" (section 4) authorizes only read-only probes, a typed nudge and a direct question to the worker, in that order; a worker that announced a long step with `expect_silence_min` gets no nudge or typed text before that window ends, while read-only probes still run. Append the C-17 sentence to WC-11: "The coordinator's liveness `stat` reads only the worker's own contract path and report directory." Add `RULE_PHRASES` pins in `tests/skills/test_worker_contract.py` for both.

Acceptance criteria (ids T1.AC1, T1.AC2, T1.AC3 in order):
- T1.AC1: WC-10 keeps its first three sentences unchanged and ends with the C-1 text; the old phrase "it acts only on Orca's stall proofs" is gone.
- T1.AC2: WC-11 ends with the C-17 sentence.
- T1.AC3: `RULE_PHRASES` gains a WC-10 absence pin (for example "never as death" and "authorizes only read-only probes, a typed nudge and a direct question") and a WC-11 liveness-stat pin; `uv run pytest tests/skills/test_worker_contract.py -q` passes.
Global constraints: ## Constraints

- Edit only `src/superclaude/core/WORKER-CONTRACT.md` and `tests/skills/test_worker_contract.py`. No code beyond tests; nothing for the v2 monitor, adapters, hooks or dashboard.
- The contract has no other copy in the repo (no `plugins/superclaude/core/` copy, no level-table copy in `HOW-WE-WORK.md`), and `make sync-dev` / `make verify-sync` do not cover `core/`; both still run before the PR.
- Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines). One adaptation: C-2's "in the preamble command's payload or phase text" becomes "in the heartbeat's subject or phase text, or a `status` body line", because the heartbeat verb takes typed flags (`--type heartbeat --subject alive --task-id --dispatch-id --phase`) and has no custom payload field.
- Every new pin is a `RULE_PHRASES` entry `"<name>": (<ident or None>, [<phrases>])` whose phrases appear verbatim in the contract; when an ident is given, one contract line must hold both the ident and the first phrase. `test_contract_states_rule` and `test_rule_check_fails_when_rule_removed` then cover it with no new test function.
- Existing pins must keep passing: WC-10 ("at the cadence its preamble sets", "split into waits of at most 4 minutes"), WC-5, WC-7, WC-12, WC-3, WC-6, heartbeats, brief-layout, brief-template, and the guard-before-`Command:` check.
- Statements the design marks unverified are written as UNVERIFIED in the contract text, never as fact: what `check --wait` wakes on without `--types`; the cause of case 5, answers not seen (lead: `orca orchestration reply` stores type `status` with subject "Re: Question", so a narrow `--types` waiter may miss it); whether a permission-prompt or compact-thrashing attention category exists; what Claude Code does with text typed while a tool call runs; whether two consumers on one mailbox both get a batch.
- Owner decisions of 2026-11-07 are binding: never resend a mailbox copy of an answer; the worker confirms an answer with an ack; with no ack after 5 minutes and a probe that positively shows an empty idle prompt, the coordinator types ONE copy into the terminal; at 15 minutes it reports to the person. A person-directed cancellation with confirmed quiescence settles a live attempt; context exhaustion alone is not proof.
- `unverifiable` liveness is absence and never authorizes stop, abandon, retry or release.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Never stage `.claude/` mirrors.
- Evidence logs go under `./artifacts/`.
Start sha: 651fb0e3be5e92da95891c886044a8dde836a78b
Diff against the start snapshot:
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 1911c2bf..ac0cb9de 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -43,8 +43,8 @@ These rules bind a command run with `--unattended`. Without the flag a command b
   - The worker then reads coordinator follow-ups, refuses on a detached HEAD, the default branch or any path outside its report directory, `report_path`, `artifacts` and `.dev/tasks`, stages with `git add -- <paths>` plus `.dev/tasks`, commits with `git commit --only -- <paths>` and never `--no-verify`, never pushes, and gives the commit ID in its `worker_done` body; a refused or failed commit is reported as WC-5 states. A command's own commit step stays off under `--unattended`.
   - Outside that grant a worker never runs `git add` (including `git add .dev/tasks`), never commits, never moves HEAD and never touches a remote: the coordinator stages `.dev/tasks` (section 4). The skills that stage it themselves (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md`, `~/.claude/skills/sc-implement-protocol/refs/ledger.md`, `~/.claude/skills/sc-workflow-protocol/SKILL.md`, `~/.claude/skills/task/SKILL.md`) defer that staging under `--unattended`, and the MDTM CLI-mode `git add -A` (`~/.claude/skills/task-builder/SKILL.md`) is refused.
   - `/sc:implement`'s private-index snapshots, its `refs/superclaude/implement/` refs and its revert stay allowed. A worker that finds `index.lock` in its worktree reports `blocked` with the path.
-- **WC-10. Liveness during long waits.** The worker sends heartbeats at the cadence its preamble sets. A command step that blocks a single Bash call for longer than 4 minutes (a poll wait, a long eval) must be split into waits of at most 4 minutes so the session can heartbeat between them. A command's own Agent-tool fan-out (kept unchanged by WC-7) can hold the session longer than the cadence with no way to heartbeat; that gap is accepted, not required away, because commands may not call Orca and the subagents may not send lifecycle messages (WC-7). The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late, and it acts only on Orca's stall proofs.
-- **WC-11. Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes, and the coordinator gives every Task its own report directory; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. Workers share the feature worktree only when they write nothing but their own report directory, which goes under `.dev/`. A worker gets its own child worktree (section 4) when its brief grants local commits; when it runs `/sc:implement` and any other writer (another worker, the coordinator, the person, a taken-over terminal or a hook) may write outside `.dev/` in the same worktree during the run; when it is a parallel experiment to compare or discard; or when its command writes the user index.
+- **WC-10. Liveness during long waits.** The worker sends heartbeats at the cadence its preamble sets. A command step that blocks a single Bash call for longer than 4 minutes (a poll wait, a long eval) must be split into waits of at most 4 minutes so the session can heartbeat between them. A command's own Agent-tool fan-out (kept unchanged by WC-7) can hold the session longer than the cadence with no way to heartbeat; that gap is accepted, not required away, because commands may not call Orca and the subagents may not send lifecycle messages (WC-7). The coordinator therefore treats a missing heartbeat as absence, never as death: it stops, retries or releases a worker only on Orca's stall proofs or the person's recorded stop under WC-6. Absence past the deadline in "Liveness supervision" (section 4) authorizes only read-only probes, a typed nudge and a direct question to the worker, in that order. A worker that announced a long step with `expect_silence_min` gets no nudge or typed text before that window ends; read-only probes still run.
+- **WC-11. Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes, and the coordinator gives every Task its own report directory; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. Workers share the feature worktree only when they write nothing but their own report directory, which goes under `.dev/`. A worker gets its own child worktree (section 4) when its brief grants local commits; when it runs `/sc:implement` and any other writer (another worker, the coordinator, the person, a taken-over terminal or a hook) may write outside `.dev/` in the same worktree during the run; when it is a parallel experiment to compare or discard; or when its command writes the user index. The coordinator's liveness `stat` reads only the worker's own contract path and report directory.
 
 ## 3. Worker-session duties
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 3197395e..aa2bc692 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -226,6 +226,19 @@ RULE_PHRASES = {
     ),
     "fan-in-max": (None, ["maximum of 10 inputs"]),
     "fan-in-min": (None, ["at least 2 inputs are admitted"]),
+    "wc10-absence-not-death": (
+        None,
+        [
+            "never as death",
+            "authorizes only read-only probes, a typed nudge and a direct question",
+        ],
+    ),
+    "wc11-liveness-stat": (
+        None,
+        [
+            "The coordinator's liveness `stat` reads only the worker's own contract path and report directory",
+        ],
+    ),
     "brief-template": (
         None,
         [
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
