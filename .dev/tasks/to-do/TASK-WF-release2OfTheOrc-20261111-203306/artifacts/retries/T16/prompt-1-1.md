9533e0def3b58c5f7ab6ab2567b9c08693e7b4c6
Review one task for spec compliance.

Task brief: 
## Task 16: Verify Q-1 from a fresh plain terminal against the probe Run (gated)

Depends on: Task 2

Answer Q-1 (REPORT section 9) and the question whether `check --all` consumes when the reader is not the owner. The probe Runs `run_c1badaa6576b` (Run A) and `run_14cfcbd8edf2` (Run B) were created by the gate research worker as throwaways; use only them. The check needs a plain Orca terminal that has a handle and holds no Run, which the executor may not have: a coordinator must open one. Run only `orca-ide orchestration check --all --types question --run run_c1badaa6576b --json` from that terminal, once (no `--peek` form is needed); never plain `check`, `--ack`, `run-use` or any send. Then, from the owning terminal, read Run A once with `check --all` and compare ids and count before and after to see whether the reader changed anything.

Write `./artifacts/q1-result.md` with the command, date, redacted output shape, the observed error code or the row count, and one verdict line: `Q-1: PASS (an unbound terminal with a handle can read)`, `Q-1: FAIL (<error code>)` or `Q-1: BLOCKED (<reason, for example no plain terminal available>)`. Update the Q-1 row in `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md` with the verdict and the artifact name.

Acceptance criteria:
- `./artifacts/q1-result.md` exists and holds exactly one of the three verdict lines, with real command output shape for PASS and FAIL and a stated reason for BLOCKED; nothing is fabricated or assumed.
- The register row for Q-1 states the same verdict. No Orca command other than the non-consuming `check --all` forms on Run A or Run B was run, shown by the command list in the artifact.

Global constraints: 
## Constraints

- Shorthand. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. REPORT is the file `RESEARCH-REPORT-phase2-gate.md` in the folder `TASK-RESEARCH-phase2-gate-20261111-200400` under `.dev/tasks/` (the folder may sit in to-do or done); its recorded evidence is the `research/evidence/` folder next to it, files numbered 01 to 27. OWNER is `.dev/issues/409/owner-decisions-20261111.md`. "The probe shapes" are the recorded outputs in REPORT's evidence folder: envelope `{id, ok, result:{acknowledged, count, messages[], runId}, _meta}`; message row keys `id` (msg_...), `run_id`, `delivery_contract`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at`; error envelope `{ok:false, error:{code, message}}` with codes `consumer_fenced` (exit status 1) and `no_active_terminal`.
- Scope is release 2 only, as fixed by OWNER and REPORT sections 7 to 9. Decision 8: only messages of type `question`, labelled "coordinator questions", never "human". Decision 6: read permission for one named Run, `--types question`, never `run-use`. The owner has not yet named the Run (open question for the owner; Task 17 is blocked until they do).
- Fixed design basis, not reopened. One named Run only; no rotation across Runs; the observer runs where it already holds the Run. Every read passes `--types question`. Only `check --all` is used: `--peek` hides acked rows so it is not a source. Question identity is `message.id`, labelled UNVERIFIED for any Run other than the probe Runs and the coordinator's own Run; a worker `dispatchId` is never a question identity. The disclosure text, verbatim, is `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.
- UNVERIFIED facts that stay gated risks, each with a named verification task and never an assumption. Q-1: whether an observer terminal that has a handle but holds no Run can read (Task 16). Q-2: the effect of `run-use` on a live coordinator (not tested, forbidden for the observer; Task 6 pins `run-use` as a forbidden argv and Task 2 records Q-2 as never tested). Message rate on a Run other than the coordinator's own, and identity on real traffic (Task 17). Whether `ask` writes type `question` (Q-3) is recorded in the register as UNVERIFIED; no R2 behaviour depends on it because the label says "coordinator questions" and the observer lists type `question` rows however they were written.
- Safety. No consuming read (`check` without `--all` or `--peek`, `check --ack`), no `run-use`, `run-create`, `send`, `ask`, `reply` or `reset` against any Run except where a task names a throwaway probe Run and a non-consuming form. Raw Orca output is never logged, committed or exported; committed samples hold only redacted values (no terminal handle, token, credential or absolute path). Bodies of messages are received by the observer process (acquisition cannot be undone by dropping them at parse time), so the design never claims bodies were not acquired; it only does not keep or show them.
- Rules carried from release 1. UV only (`uv run pytest ...`). Python 3.10 compatible, no new dependency. A fact the source does not give is the `UNKNOWN` sentinel and renders as `unknown`; unknown is never 0, false, blank or `null`. Source loss never closes a question, lowers an open count or turns a value into `failed`. Every source string passes `sanitize` before it reaches the view model; strings render as literal text, never Rich markup; truncation uses cell width. Plan edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Out of scope: R3 links (QUESTION-LINK), `inbox`, closure evidence, history beyond the 100-row window, `--include-remote`, write-back, per-question selection and marking (the `m` key keeps its release 1 meaning), any message call other than the one template.
- Plan-author choices (PROPOSED, the owner may change them). The opt-in flag is `--questions`, valid only with `--run <runId>` and a live source. The message call budget is one call per cycle; when questions are on, worker-list paging is limited to 4 calls so the cycle total stays inside the 5-call cap. The panel shows `subject` and age only, never `body`. The reason column reads `reason unknown` because no verified reason field exists. Retention is in memory for the process, bounded at 1,000 records.
- Gate honesty. QUESTION-OBSERVATION is NOT passed as of this plan: proof (a) failed as worded, proof (b) is partly proven, proof (c) is unmeasured, non-consumption passed only as the Run's owner on a probe Run. The live question read is guarded by one constant that Task 18 may flip only against an owner-written record.

Start sha: 9533e0def3b58c5f7ab6ab2567b9c08693e7b4c6
Diff against the start snapshot: 
diff --git a/.dev/issues/409/bmad/spec-orca-observer/release-gates.md b/.dev/issues/409/bmad/spec-orca-observer/release-gates.md
index 4121d67e8..f92243ca5 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/release-gates.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/release-gates.md
@@ -40,9 +40,9 @@ Until the owner confirms one in the selection record, the stricter reading appli
 Candidate verb: `orca orchestration check --all --types question --run <runId> --json`, for **one named Run**. A candidate, never an available source, until the open items at the end of this section are recorded. Read scope: one named Run, `--types question`, never run-use (the observer never runs `run-use`).
 
 - **Proof (a), withdrawn as worded (REPORT 2.1).** The old wording said that `--run` narrows `--all`; that claim is withdrawn. The read returns only the mailbox of the Run the caller is bound to. A caller bound to another Run is fenced: `{"ok":false,"error":{"code":"consumer_fenced", ...}}` with the message "This caller is bound to Run <A>, not Run <B>. Nothing changed." (exit status 1). So `--run` is a fence, not a filter. Basis: two-Run evidence on probe Run A (`run_c1badaa6576b`) and probe Run B (`run_14cfcbd8edf2`), 2026-11-11 (REPORT 2.1, evidence files 01, 02, 03, 04, 23). No row from the other Run ever appeared.
-- **Proof (b), partly proven (REPORT 2.1).** Messages land in the Run mailbox: a message sent `--to run:<id>` is stored with `to_handle` `run:<id>` (REPORT 2.1, evidence file 03). Orca has no human recipient field; `send --help` lists the types `status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat`. A caller with no terminal identity gets `no_active_terminal` (evidence files 17, 18, 19). A terminal that has a handle but holds no Run is **UNTESTED** and stays UNVERIFIED (Q-1, plan Task 16). Whether `ask` writes type `question` (Q-3) is UNVERIFIED; no R2 behaviour depends on it.
+- **Proof (b), partly proven (REPORT 2.1).** Messages land in the Run mailbox: a message sent `--to run:<id>` is stored with `to_handle` `run:<id>` (REPORT 2.1, evidence file 03). Orca has no human recipient field; `send --help` lists the types `status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat`. A caller with no terminal identity gets `no_active_terminal` (evidence files 17, 18, 19). **Q-1: FAIL (consumer_fenced)** (plan Task 16, 2026-11-11, `artifacts/q1-result.md` in the release 2 plan folder): a plain Orca terminal that has a handle but holds no Run was refused when it read probe Run A, which is bound to another terminal; no rows came back. So an observer must run in the terminal that holds the Run (or hold a Run of its own); it cannot read by name from an unbound terminal. One case, one Run; a Run bound to no terminal was not tested. Whether `ask` writes type `question` (Q-3) is UNVERIFIED; no R2 behaviour depends on it.
 - **Proof (c), UNVERIFIED (REPORT 2.1).** No real message rate is recorded for any Run (REPORT: "the real message rate is UNVERIFIED and I did not measure it"). Measured facts only: the read is bounded at 100 rows; `--all` returns the newest 100 first and `--peek` returns the oldest 100 first (probe Run B, 104 messages, evidence files 14 and 15); there is no total, `hasMore` or truncation field; about 0.2 s per call on a probe Run (evidence file 16). The coordinator's own Run, as the owner measured it (OWNER, "Coordinator measurement"): 100 rows with `check --all` and no type filter (91 heartbeat, 8 worker_done, 1 question), and 41 rows with `--types question`, so the cap applies after the type filter. A measured rate does not prove completeness, so the label stays `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` after the gate.
-- **Non-consumption (INV-022): passed on a probe Run, as the Run's owner, for the visible effects tested (REPORT 2.2, evidence files 03 to 12).** `--all` and `--peek` reads did not consume, and a later consuming `check` by the owner still received everything. `--all` rows carry no read or acknowledged marker, so a handled question looks like a fresh one; `--peek` hides acknowledged rows, so only `--all` is used. Non-consumption by a reader that is not the owner is UNVERIFIED (Q-1). The coordinator's own-Run check also found 0 pending after its reads (OWNER), tested as the Run's owner only. A pass covers only the visible effects tested (T51).
+- **Non-consumption (INV-022): passed on a probe Run, as the Run's owner, for the visible effects tested (REPORT 2.2, evidence files 03 to 12).** `--all` and `--peek` reads did not consume, and a later consuming `check` by the owner still received everything. `--all` rows carry no read or acknowledged marker, so a handled question looks like a fresh one; `--peek` hides acknowledged rows, so only `--all` is used. Non-consumption by a reader that is not the owner is UNVERIFIED; Task 16 narrowed it: the one non-owner read (Q-1) was refused before any row was returned, and Orca's reply says "Nothing changed". The coordinator's own-Run check also found 0 pending after its reads (OWNER), tested as the Run's owner only. A pass covers only the visible effects tested (T51).
 - **Question identity: `message.id` (`msg_...`), seen on the probe Runs only (REPORT 2.2 and gap G-8, "identity candidate `message.id` seen on probes only"), UNVERIFIED on real traffic, including the coordinator's own Run, where OWNER records counts and types but no message ids.** A worker `dispatchId` is never a question's identity.
 - **Owner inputs (OWNER, decided 2026-11-11, decider: the owner).** Decision 8: "coordinator questions only"; only messages of type `question` are listed, labelled "coordinator questions", never "human". Decision 6: "Permission granted, proceed"; read permission for one named Run, `--types question`, never `run-use`. The owner has not yet named the Run (open question for the owner), and no call may be made against a named Run until it is named.
 - **Budget:** one message call per cycle; no rotation across Runs. The rotation set the earlier text described is removed from R2 (REPORT 8, item 1: a terminal bound to one Run is fenced from every other Run, and the only route found to another Run is `run-use`, whose effect on a live coordinator is UNVERIFIED, Q-2, never tested and forbidden for the observer).
diff --git a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
index c03147bcd..017b86f8d 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
@@ -43,8 +43,8 @@ Source: `RESEARCH-REPORT-phase2-gate.md` (REPORT, in `.dev/tasks/to-do/TASK-RESE
 | The inbox JSON shape (its rows add `read` and `sequence`, REPORT 2.2, evidence file 20); whether `inbox` reaches across Runs (REPORT Q-4) | `inbox` stays forbidden; not tested; forbidden |
 | Meaning of `result.count` (equals 100 for a 104-row Run, evidence file 14) | No count is ever derived from it |
 | Proof (a) as worded, "`--run` narrows `--all`": WITHDRAWN. `--run` is a fence, not a filter (`consumer_fenced`); see `release-gates.md` | Replaced by the one-named-Run rule |
-| Proof (b), a terminal that has a handle but holds no Run (Q-1) | UNTESTED, so UNVERIFIED (REPORT 2.1 could not make such a terminal; a caller with no terminal identity at all gets `no_active_terminal`); verification task: Task 16 (gated on a plain terminal supplied by the coordinator) |
-| Whether `check --all` ever consumes when the reader is not the Run's owner | UNVERIFIED; verification task: Task 16 (non-consumption is seen only as the owner on a probe Run) |
+| Proof (b), a terminal that has a handle but holds no Run (Q-1) | **Q-1: FAIL (consumer_fenced)**, tested 2026-11-11 from a plain Orca terminal against probe Run A: the read is refused, no rows (`artifacts/q1-result.md` of the release 2 plan folder, Task 16). One case, one Run; a Run bound to no terminal was not tested. A caller with no terminal identity at all gets `no_active_terminal` (REPORT 2.1) |
+| Whether `check --all` ever consumes when the reader is not the Run's owner | UNVERIFIED, narrowed by Task 16: the one non-owner read was refused before any row was returned ("Nothing changed"), so nothing was observed to consume; the owner-side before/after comparison of the plan was not done (the owning terminal belongs to another session) |
 | Effect of `run-use` on a live coordinator (Q-2) | not tested; forbidden for the observer: `run-use` is a forbidden argv (Task 6) |
 | Whether `ask` writes type `question` (Q-3) | UNVERIFIED; not tested; forbidden for the observer (`ask` is a forbidden verb, Task 6); no R2 behaviour depends on it |
 | Message rate on any Run, and `message.id` identity on real traffic, for the Run the owner names (the owner has not named it) | UNVERIFIED; verification task: Task 17 (gated on the owner); the label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` stays |
diff --git a/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/q1-result.md b/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/q1-result.md
new file mode 100644
index 000000000..1fe71c280
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/q1-result.md
@@ -0,0 +1,28 @@
+# Q-1 result (plan Task 16)
+
+**Q-1: FAIL (consumer_fenced)**
+
+Date: 2026-11-11 (22:3x UTC). Run read: probe Run A, `run_c1badaa6576b`, created by the gate research worker as a throwaway.
+
+## What was run
+
+A plain Orca terminal spawned by the owner for this test: it has a terminal handle (`ORCA_TERMINAL_HANDLE` is set) and holds no Run. From that terminal, once:
+
+```
+orca orchestration check --all --types question --run run_c1badaa6576b --json
+```
+
+(`orca`, not `orca-ide`: inside an Orca terminal `orca` is the Orca CLI.) No `--peek`, plain `check`, `--ack`, `run-use` or send was run against Run A. The other commands of this task ran only against the Run the executor created itself (see `t17-sample.md`).
+
+## Observed (redacted shape)
+
+Exit status 1; stdout one JSON envelope: `{"ok": false, "error": {"code": "consumer_fenced", "message": "This caller is not bound to Run run_c1badaa6576b, which is bound to <a terminal handle, redacted>. Nothing changed."}}`. No `result`, no rows.
+
+## Meaning
+
+- An observer terminal that has a handle but holds no Run cannot read a Run that is bound to another terminal. It is fenced, the same code the gate research saw for a caller bound to a different Run. So an observer must run in the terminal that holds the Run, or hold a Run of its own; there is no read-by-name from an unbound terminal. This is one case, one Run: Orca may behave differently for a Run that is bound to no terminal (not tested).
+- Whether `check --all` ever consumes when the reader is not the owner: **not observed.** The only non-owner read was refused before any row was returned, and Orca's own message says "Nothing changed". The second step of the plan (read Run A once from the owning terminal and compare ids and count before and after) was not done: the owning terminal belongs to the research session and was not touched. This question stays UNVERIFIED, now narrowed: a non-owner read returns nothing at all.
+
+## Commands run in this task (all of them)
+
+1. `check --all --types question --run run_c1badaa6576b --json` from the plain terminal (above).


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
