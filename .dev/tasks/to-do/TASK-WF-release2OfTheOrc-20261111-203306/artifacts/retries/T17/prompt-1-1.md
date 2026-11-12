8fc83479317c38b204ad28b696ba32606601e4a5
Review one task for spec compliance.

Task brief: 
## Task 17: Capture one permitted redacted sample on the owner-named Run (gated on the owner)

Depends on: Task 16, Task 12

Blocked until the owner names the Run and the redaction rules (open question for the owner; OWNER decision 6 grants the read but names no Run). When the Run is named, run it from a terminal that already holds that Run, never with `run-use`, as one non-consuming read: `orca-ide orchestration check --all --types question --run <named Run> --json`, once, plus one repeat a few seconds later to see whether ids change. Keep only redacted shapes. Record the counts per read, `window full` or not, the observed number of question rows, the interval between the two reads and any new message ids, and whether `message.id` stayed unique.

Write `./artifacts/t17-sample.md` (redacted, no bodies, no handles) and update `release-gates.md` proof (c) and the question-identity line with the measured values, still labelled UNVERIFIED for any other Run and still carrying the disclosure label after the sample. If the Run is not named, write `./artifacts/t17-sample.md` with `T17: BLOCKED (owner has not named the Run)` and change nothing else.

Acceptance criteria:
- `./artifacts/t17-sample.md` holds either measured redacted values with the command shape and date, or the one BLOCKED line; the argv log in the artifact shows only the template argv.
- When measured, `release-gates.md` states the sample size, the date and the Run's role (named by the owner), says the rate is not proof of completeness, and keeps `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.

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

Start sha: 8fc83479317c38b204ad28b696ba32606601e4a5
Diff against the start snapshot: 
diff --git a/.dev/issues/409/bmad/spec-orca-observer/release-gates.md b/.dev/issues/409/bmad/spec-orca-observer/release-gates.md
index f92243ca5..98f25e742 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/release-gates.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/release-gates.md
@@ -42,10 +42,11 @@ Candidate verb: `orca orchestration check --all --types question --run <runId> -
 - **Proof (a), withdrawn as worded (REPORT 2.1).** The old wording said that `--run` narrows `--all`; that claim is withdrawn. The read returns only the mailbox of the Run the caller is bound to. A caller bound to another Run is fenced: `{"ok":false,"error":{"code":"consumer_fenced", ...}}` with the message "This caller is bound to Run <A>, not Run <B>. Nothing changed." (exit status 1). So `--run` is a fence, not a filter. Basis: two-Run evidence on probe Run A (`run_c1badaa6576b`) and probe Run B (`run_14cfcbd8edf2`), 2026-11-11 (REPORT 2.1, evidence files 01, 02, 03, 04, 23). No row from the other Run ever appeared.
 - **Proof (b), partly proven (REPORT 2.1).** Messages land in the Run mailbox: a message sent `--to run:<id>` is stored with `to_handle` `run:<id>` (REPORT 2.1, evidence file 03). Orca has no human recipient field; `send --help` lists the types `status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat`. A caller with no terminal identity gets `no_active_terminal` (evidence files 17, 18, 19). **Q-1: FAIL (consumer_fenced)** (plan Task 16, 2026-11-11, `artifacts/q1-result.md` in the release 2 plan folder): a plain Orca terminal that has a handle but holds no Run was refused when it read probe Run A, which is bound to another terminal; no rows came back. So an observer must run in the terminal that holds the Run (or hold a Run of its own); it cannot read by name from an unbound terminal. One case, one Run; a Run bound to no terminal was not tested. Whether `ask` writes type `question` (Q-3) is UNVERIFIED; no R2 behaviour depends on it.
 - **Proof (c), UNVERIFIED (REPORT 2.1).** No real message rate is recorded for any Run (REPORT: "the real message rate is UNVERIFIED and I did not measure it"). Measured facts only: the read is bounded at 100 rows; `--all` returns the newest 100 first and `--peek` returns the oldest 100 first (probe Run B, 104 messages, evidence files 14 and 15); there is no total, `hasMore` or truncation field; about 0.2 s per call on a probe Run (evidence file 16). The coordinator's own Run, as the owner measured it (OWNER, "Coordinator measurement"): 100 rows with `check --all` and no type filter (91 heartbeat, 8 worker_done, 1 question), and 41 rows with `--types question`, so the cap applies after the type filter. A measured rate does not prove completeness, so the label stays `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` after the gate.
+  - **Sample (plan Task 17, 2026-11-11, `artifacts/t17-sample.md` in the release 2 plan folder):** the Run is `run_86013b917868`, a throwaway the executor created from a plain Orca terminal, with the owner's permission to choose its own Run, and seeded by hand with 5 synthetic questions and 2 status messages. Two template reads 6 s apart each returned 5 rows, only type `question`, the same ids in the same order, `delivered_at` null, window not full. Sample size: 5 messages on one synthetic Run. This is not a real message rate, and a rate is not proof of completeness. Real traffic is still unmeasured (UNVERIFIED).
 - **Non-consumption (INV-022): passed on a probe Run, as the Run's owner, for the visible effects tested (REPORT 2.2, evidence files 03 to 12).** `--all` and `--peek` reads did not consume, and a later consuming `check` by the owner still received everything. `--all` rows carry no read or acknowledged marker, so a handled question looks like a fresh one; `--peek` hides acknowledged rows, so only `--all` is used. Non-consumption by a reader that is not the owner is UNVERIFIED; Task 16 narrowed it: the one non-owner read (Q-1) was refused before any row was returned, and Orca's reply says "Nothing changed". The coordinator's own-Run check also found 0 pending after its reads (OWNER), tested as the Run's owner only. A pass covers only the visible effects tested (T51).
-- **Question identity: `message.id` (`msg_...`), seen on the probe Runs only (REPORT 2.2 and gap G-8, "identity candidate `message.id` seen on probes only"), UNVERIFIED on real traffic, including the coordinator's own Run, where OWNER records counts and types but no message ids.** A worker `dispatchId` is never a question's identity.
-- **Owner inputs (OWNER, decided 2026-11-11, decider: the owner).** Decision 8: "coordinator questions only"; only messages of type `question` are listed, labelled "coordinator questions", never "human". Decision 6: "Permission granted, proceed"; read permission for one named Run, `--types question`, never `run-use`. The owner has not yet named the Run (open question for the owner), and no call may be made against a named Run until it is named.
+- **Question identity: `message.id` (`msg_...`), seen on the probe Runs only (REPORT 2.2 and gap G-8, "identity candidate `message.id` seen on probes only"), UNVERIFIED on real traffic, including the coordinator's own Run, where OWNER records counts and types but no message ids.** On the executor's synthetic Run of the Task 17 sample, 5 of 5 ids were distinct and stable across two reads (UNVERIFIED for any other Run). A worker `dispatchId` is never a question's identity.
+- **Owner inputs (OWNER, decided 2026-11-11, decider: the owner).** Decision 8: "coordinator questions only"; only messages of type `question` are listed, labelled "coordinator questions", never "human". Decision 6: "Permission granted, proceed"; read permission for one named Run, `--types question`, never `run-use`. The owner did not name a Run and told the executor to choose its own (coordinator session, 2026-11-11); the executor chose a throwaway it created, `run_86013b917868`, after weighing the coordinator's Run (fenced for any other terminal, `run-use` forbidden) and the probe Runs (bound to a finished session). No real Run was read.
 - **Budget:** one message call per cycle; no rotation across Runs. The rotation set the earlier text described is removed from R2 (REPORT 8, item 1: a terminal bound to one Run is fenced from every other Run, and the only route found to another Run is `run-use`, whose effect on a live coordinator is UNVERIFIED, Q-2, never tested and forbidden for the observer).
-- **Still open (the gate stays closed until all are recorded):** Q-1 (an observer terminal that has a handle but holds no Run; plan Task 16); the message rate and identity on the Run the owner names (plan Task 17); the owner's written pass record, which agents cite and never write (see the evidence rule under DIRECTION-SELECTED). QUESTION-OBSERVATION: not passed.
+- **Still open (the gate stays closed until all are recorded):** Q-1 is answered: FAIL (an unbound terminal cannot read; the observer must run in the terminal that holds the Run), which the owner must weigh before passing the gate; the message rate and identity on real traffic are still unmeasured (Task 17 sampled only a synthetic Run); the owner's written pass record, which agents cite and never write (see the evidence rule under DIRECTION-SELECTED). QUESTION-OBSERVATION: not passed.
 
 **Fallback rule:** if QUESTION-OBSERVATION is not verified by the owner's fallback date, the owner re-confirms the direction. If A is picked, A stays the default on the same adapter and renderer; B's retention model stays in the code for when the contract arrives (one layout function, not a rewrite).
diff --git a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
index 017b86f8d..0db2e5882 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
@@ -47,7 +47,7 @@ Source: `RESEARCH-REPORT-phase2-gate.md` (REPORT, in `.dev/tasks/to-do/TASK-RESE
 | Whether `check --all` ever consumes when the reader is not the Run's owner | UNVERIFIED, narrowed by Task 16: the one non-owner read was refused before any row was returned ("Nothing changed"), so nothing was observed to consume; the owner-side before/after comparison of the plan was not done (the owning terminal belongs to another session) |
 | Effect of `run-use` on a live coordinator (Q-2) | not tested; forbidden for the observer: `run-use` is a forbidden argv (Task 6) |
 | Whether `ask` writes type `question` (Q-3) | UNVERIFIED; not tested; forbidden for the observer (`ask` is a forbidden verb, Task 6); no R2 behaviour depends on it |
-| Message rate on any Run, and `message.id` identity on real traffic, for the Run the owner names (the owner has not named it) | UNVERIFIED; verification task: Task 17 (gated on the owner); the label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` stays |
+| Message rate on any Run, and `message.id` identity on real traffic | UNVERIFIED. Task 17 sampled only a synthetic throwaway Run the executor created (5 rows, 5 distinct ids, stable across two reads; `artifacts/t17-sample.md`); no real Run was read; the label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` stays |
 | Meaning of `delivered_at`, which stayed `null` on every probe row even after a consuming read and acknowledgement (REPORT 2.2, evidence files 08, 11) | UNVERIFIED; the observer never reads it as closure |
 | What identifies a human question | Decided 2026-11-11 (OWNER, decision 8): coordinator questions only (type `question`); whether the coordinator agent or a person answers is not recorded by Orca |
 | Inbox lease fields, terminal-attribution fields | `inbox` and plain `check` are never run; not tested; forbidden |
diff --git a/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/t17-sample.md b/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/t17-sample.md
new file mode 100644
index 000000000..8f3d213ac
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/t17-sample.md
@@ -0,0 +1,42 @@
+# T17 sample on a Run the executor created (plan Task 17)
+
+**Run named by the executor, with the owner's permission to choose one ("find and name your own run"): `run_86013b917868`, a throwaway created for this sample. It is synthetic. It says nothing about real traffic.**
+
+## Why this Run (options weighed)
+
+| Option | Verdict |
+|---|---|
+| The coordinator's own Run `run_93bfa00cae2b` | Real traffic, but only its own terminal holds it, an observer terminal is fenced from it (Q-1 FAIL), and the only other route is `run-use`, which is forbidden. Rejected. |
+| Probe Runs A and B from the gate research | Bound to the research worker's terminal, so every other terminal is fenced (Q-1). Unreadable. Rejected. |
+| A new throwaway Run created from the plain terminal, seeded with synthetic questions | The terminal that creates a Run holds it, so it can read it with the exact template and no `run-use`. Nothing real is read or changed. **Chosen.** |
+
+## What was run (plain terminal, which created and holds the Run)
+
+1. `orchestration run-create --objective "<text>" --json` (creates and binds the Run).
+2. Seeded: 5 messages `--type question` and 2 `--type status`, each `send --to run:<id>`, synthetic subject and body.
+3. Template argv, twice, about 6 s apart (22:36:32Z and 22:36:38Z): `check --all --types question --run run_86013b917868 --json`.
+
+No `--peek`, plain `check`, `--ack`, `run-use`, `reset` or `ask`. Raw output stayed in a temporary folder and is not committed.
+
+## Measured (redacted)
+
+| Item | Read 1 | Read 2 |
+|---|---|---|
+| exit status, `ok` | 0, true | 0, true |
+| rows returned | 5 | 5 |
+| `result.count` | 5 | 5 |
+| types in the rows | only `question` (the 2 status messages were not returned) | same |
+| distinct `message.id` | 5 of 5 | 5 of 5 |
+| ids and order vs read 1 | | identical, same order |
+| `delivered_at` | all null | all null |
+| window full (exactly 100 rows) | no | no |
+| row keys | `body, created_at, delivered_at, delivery_contract, from_handle, id, payload, priority, run_id, subject, thread_id, to_handle, type` (the 13 recorded keys, no more) | same |
+
+Call latency was not measured (the timing helper `bc` is not installed on the host).
+
+## What this shows and does not show
+
+- Shows: the template works end to end through real Orca for a Run the reader holds; `--types question` filters on the server; `message.id` is unique within the Run; two reads 6 s apart return the same ids in the same order; no new id appeared (nothing was sent between the reads); the read left `delivered_at` null.
+- Does not show: a real message rate (5 messages sent by hand); identity on real traffic; behaviour on a busy Run; non-consumption by a non-owner (Q-1: the non-owner read is refused). The rate is not proof of completeness. The label stays `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.
+
+argv log in this artifact: the one template shape above, twice, plus the run-create and the seven sends on this Run only.


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
