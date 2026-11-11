f3f3d8441a9851f004032c066455a1a97cbaf5c9
Review one task for spec compliance.

Task brief: 
## Task 4: Update the R2 section of adapter-contract.md

Depends on: Task 1

Edit `.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md`: "Scope", "Argv allow-list" (forbidden set), "Bounds per cycle", "R2 onward" and the "Scope honesty" last bullet.

- Add the message template as exact argv: `(orca, "orchestration", "check", "--all", "--types", "question", "--run", runId, "--json")`, separate arguments, `runId` through the existing format check, only after the gate record exists.
- Add `run-use`, `run-create`, `send`, `ask`, `reply`, `reset` to the forbidden set; keep plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox` forbidden; `--peek` and an unfiltered `check --all` are not allowed in any argv.
- Replace the "Rotation set" bullet: one named Run, no rotation, the observer never binds to a Run (no `run-use`), it must run where it already holds the Run; remove `revisit ~Ns` and `read k of N Runs since start` for messages (the header reads `one Run only` plus the named Run).
- Budget: one message call per cycle, worker-list paging limited to 4 calls when questions are on (total at most 5).
- Parsing: message rows by field with the `UNKNOWN` sentinel; required `result.messages` as a JSON list; error envelopes `consumer_fenced` and `no_active_terminal` map to source codes `consumer-fenced` and `no-active-terminal` (cycle FAILED for the question source only; retained questions stay).
- Retention paragraph: keep the 1,000 bound and add: retention is keyed by Run plus `message.id`, a question absent from a later read is marked `no longer in source window` and never closed, and a read of exactly 100 rows is flagged `window full`.

Acceptance criteria:
- The file contains the exact message template, the six added forbidden verbs and the two error code mappings.
- No remaining text describes a rotation across Runs or `read k of N Runs since start` as a message-source behaviour.
- The acquisition-permission paragraph names decision 6 as granted for one named Run and says the Run must be named before the first call.

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

Start sha: f3f3d8441a9851f004032c066455a1a97cbaf5c9
Diff against the start snapshot: 
diff --git a/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md b/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
index efa4d1ef1..ac7b576b8 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
@@ -1,6 +1,6 @@
 # Adapter contract (smallest trustworthy read-only adapter)
 
-**Scope.** R0 runs nothing against Orca. R1 has one verb: `orca orchestration worker-list --json --limit 100`, with optional `--run <runId>` and `--cursor <c>`, plus the one-time binary discovery below (run once before the first cycle, at most one `skills list --json` probe per candidate, so at most two, and not among a cycle's 5 subprocesses). The candidate message verb (`release-gates.md`) enters the allow-list only after QUESTION-OBSERVATION passes.
+**Scope.** R0 runs nothing against Orca. R1 has one verb: `orca orchestration worker-list --json --limit 100`, with optional `--run <runId>` and `--cursor <c>`, plus the one-time binary discovery below (run once before the first cycle, at most one `skills list --json` probe per candidate, so at most two, and not among a cycle's 5 subprocesses). The one R2 message template (below, "Argv allow-list") is used only after the QUESTION-OBSERVATION gate record exists (`release-gates.md`; status: not passed as of 2026-11-11).
 
 ## Structure
 
@@ -12,9 +12,10 @@
 ## Argv allow-list
 
 - Argv is built from exact templates only. R1 template: `(orca, "orchestration", "worker-list", "--json", "--limit", "100")` plus optional `("--run", runId)` and optional `("--cursor", value)`. Discovery template (once per candidate, inside `_find_orca()`): `(<candidate binary>, "skills", "list", "--json")`. Calls use `subprocess.run` with a list, no shell.
+- **R2 message template (one only, behind the gate record):** `(orca, "orchestration", "check", "--all", "--types", "question", "--run", runId, "--json")`, every item a separate argument, `runId` through the existing format check, used only after the gate record exists. The allow decision is made on the whole argv, not on the token `check`. `--peek` and an unfiltered `check --all` (without `--types question` or without `--run`) are not allowed in any argv.
 - Following a cursor goes through a guard that marks the view PARTIAL when the per-cycle cap stops it.
 - `--include-remote` is not in the allow-list until R4.
-- **Forbidden set** (prefix-matched, never shrinks): plain `check` (without `--peek`/`--all`), `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, and any verb other than the two templates above.
+- **Forbidden set** (prefix-matched, never shrinks): plain `check`, `--ack`, `--wait`, `--retry-request`, `--peek`, `dispatch`, `inbox`, and the added `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, and any verb other than the templates above (worker-list, discovery, and the one R2 message template). `check` is allowed only as the verb of the exact R2 message template.
 - **Values:** `runId` gets a format check. The cursor is copied unchanged from `page.nextCursor`, bounded by bytes, passed as its own argument, never checked against an inferred grammar. Any value starting with `-` is rejected. A cursor rejected by this guard (leading `-`, over the byte bound, or containing NUL) stops paging for the cycle, and the cycle shows `PARTIAL (cursor rejected, page k)` (T32). V1's numeric bounds and regexes are PROPOSED, not verified Orca formats.
 - **Form:** flags and values are separate arguments; `--opt=value` only after Orca's parser support is recorded.
 - **Test seam:** the fake runner fails the test on any argv not in the allow-list.
@@ -27,7 +28,7 @@
 - After failures the interval backs off, up to 60 s.
 - Per-call timeout is measured at the first permitted live read (R0 makes no Orca calls), not guessed; UNVERIFIED until then. T5 injects a configured timeout into the fake runner.
 - STALE after 3 intervals (45 s) with no success, on a local monotonic clock.
-- Message calls per cycle: open parameter set by measurement; V3 default at most 1.
+- Message calls per cycle: exactly one (the R2 template), no paging. When questions are on, worker-list paging is limited to 4 calls, so the cycle total stays at most 5 (PROPOSED; one call is about 0.2 s on a probe Run, real traffic UNVERIFIED).
 - The poll runs in a daemon thread waiting on a `threading.Event`, mirroring `sprint/monitor.py` `OutputMonitor`. No LLM in the loop. The earlier 30 s cycle deadline is withdrawn.
 
 ## Parsing
@@ -37,6 +38,9 @@
 - Optional: `result.scope` (absent: `scope unknown`) and `page.total` (absent: `reported unknown`). V1 dissents that `page.total` should be required (`owner-decisions-and-risks.md`).
 - Rows are read field by field with absent-tolerant access; a missing key becomes `UNKNOWN`, a sentinel that is not `None`, 0 or `False`. Unknown extra keys are ignored and counted in the inspector (`n unrecognised keys`).
 
+- **Message rows (R2):** `result.messages` is required and must be a JSON list, else the question source is `FAILED (shape)`. Rows are read field by field with the `UNKNOWN` sentinel; a row that is not an object is counted and skipped; a row whose `type` is not `question`, or whose `run_id` differs from the requested Run, is dropped and counted as `contradictory rows ignored`. `body`, `payload` and `to_handle` are not kept.
+- **Error envelopes (R2):** `{ok:false, error:{code, message}}` is decoded whatever the exit status. `consumer_fenced` (exit status 1) maps to source code `consumer-fenced` and `no_active_terminal` to `no-active-terminal`. Either one fails the cycle for the question source only: the worker-list state is unchanged and the retained questions stay. Any other error code maps to `exit:<n>` or `json`.
+
 ## Identity, duplicates, order
 
 - Row identity = source namespace + `dispatchId`; rows from two hosts or Runs never merge. Each component keeps its own clock.
@@ -53,12 +57,12 @@
 
 ## R2 onward
 
-- **Question retention:** kept until closure evidence is seen; bounded at 1,000 records; eviction never lowers the open total; beyond the bound the count reads `unknown (retention exceeded)` with the retained count; overflow never shown as closed; oldest first.
-- **Rotation set:** permissioned scopes from the configured set, discovered non-historical worker scopes and scopes of retained questions, deduplicated. Scopes that do not fit one cycle rotate with `revisit ~Ns`. Empty set: `message source not read: no eligible scope; coverage unknown`.
-- **Acquisition permission (INV-017):** must cover the actual read scope before a message call, separately from display and export permission. Dropping a body at parse time cannot undo its receipt, so the design never claims unauthorized bodies were not acquired; if a narrow read cannot honour the permission the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.
+- **Question retention:** kept until closure evidence is seen; bounded at 1,000 records; eviction never lowers the open total; beyond the bound the count reads `unknown (retention exceeded)` with the retained count; overflow never shown as closed; oldest first. Retention is keyed by Run plus `message.id`. A question absent from a later successful read is marked `no longer in source window` and never closed. A read of exactly 100 rows is flagged `window full` (the source gives no total or truncation field).
+- **One named Run, no rotation:** R2 reads one named Run only. The observer never binds to a Run (it never runs `run-use`); it must run where it already holds the Run, because a caller bound to another Run is fenced (`consumer_fenced`) and a caller with no terminal identity gets `no_active_terminal`. The rotation set and the `revisit ~Ns` token are removed. For messages the header reads `one Run only` plus the named Run; `read k of N Runs since start` is not a message-source behaviour.
+- **Acquisition permission (INV-017):** decision 6 is granted for one named Run (OWNER, `owner-decisions-20261111.md`, 2026-11-11: one named Run, `--types question`, never `run-use`), and the Run must be named before the first call (the owner has not named it yet; no message call is made until then). Permission must cover the actual read scope before a message call, separately from display and export permission. Dropping a body at parse time cannot undo its receipt, so the design never claims bodies were not acquired, only that they are not kept or shown; if a narrow read cannot honour the permission the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.
 
 ## Accepted risks and scope honesty
 
 - **INV-007 (accepted risk):** rows seen this session that drop out stay listed as `not reobserved`; the strip discloses `oldest rows not read; long-running active workers may be among them`. Whether `worker-list` has a state filter is UNVERIFIED.
 - **A-008 (QUALIFY; V3 dissent REJECT):** caps are per observer process, and help and the inspector say so. No singleton lock, so several observers multiply load on Orca. Any restriction is open owner decision 9.
-- **Scope honesty:** `result.scope.source` (`flag`, `bound` or `all`, per help) is shown in the header; absent reads `scope unknown`; `bound` adds `one Run only`; the header shows `read k of N Runs since start`, where N is the number of Runs in the rotation set and reads `unknown` where no rotation set exists (CONTRADICTION with the B-view-only rendering rule; open question in `SPEC.md`).
+- **Scope honesty:** `result.scope.source` (`flag`, `bound` or `all`, per help) is shown in the header; absent reads `scope unknown`; `bound` adds `one Run only`. With R2 questions on, the header reads `one Run only` plus the named Run and carries no `read k of N Runs since start` for messages, because there is no rotation set (the placement of that token for worker reads stays an open question in `SPEC.md`).


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
