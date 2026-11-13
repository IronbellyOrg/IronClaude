9ffb781e1bf132494df858fa119140ee62e41a34
Review one task for spec compliance.

Task brief: 
## Task 2: Update unverified-register.md with verified facts and gated risks

Depends on: Task 1

Edit `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md`: the section "Candidate message verb", the UNVERIFIED table and "Not established".

- Move to a new "Seen on probe Runs and the coordinator's own Run only" list: the message row keys and envelope (the probe shapes), `--types question` filtering server-side, `--all` newest first capped at 100 with no truncation field, `--peek` oldest first and hiding acked rows, `consumer_fenced` and `no_active_terminal` responses, `message.id` as a unique identity in probes.
- Keep as UNVERIFIED rows, each with a named verification task: Q-1 (unbound observer terminal that has a handle; Task 16), Q-2 (`run-use` on a live coordinator; never tested, forbidden for the observer, pinned by Task 6), message rate and identity on a Run other than the coordinator's own (Task 17), Q-3 (`ask` writes type `question`; not required by R2), whether `check --all` ever consumes when the reader is not the owner (Task 16), meaning of `delivered_at` always null.
- Rewrite the row "Proof (a) ... narrows" to the withdrawn wording and the row for decision 8 to "decided 2026-11-11: coordinator questions only (type `question`)".
- Note that `worker-list --help` lists a `--terminal-state` filter (REPORT section 5): still UNVERIFIED as behaviour.

Acceptance criteria:
- Every row naming Q-1, Q-2, Q-3, the message rate or the non-owner consumption question carries either a verification task number from this plan or the words `not tested; forbidden`.
- No row states proof (a) as outstanding in its old wording; the candidate verb line reads `check --all --types question --run <runId> --json`.
- The file still labels the snapshot schema PROPOSED and invents no Orca field.

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

Start sha: 9ffb781e1bf132494df858fa119140ee62e41a34
Diff against the start snapshot: 
diff --git a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
index 5666c65d4..c03147bcd 100644
--- a/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
+++ b/.dev/issues/409/bmad/spec-orca-observer/unverified-register.md
@@ -24,22 +24,38 @@ The MVP (R0, R1) needs exactly one live source.
 
 ## Candidate message verb (behind QUESTION-OBSERVATION only)
 
-`orca orchestration check --all --run <runId> --json` is a candidate, never an available source, until three proofs are recorded (`release-gates.md`). Not used in R0 or R1: `check --peek`, the candidate `check --all`, `inbox`. Parsing an unknown row shape into "questions" would invent a contract.
+`check --all --types question --run <runId> --json`, for one named Run, is a candidate, never an available source, until the open items in `release-gates.md` (QUESTION-OBSERVATION: not passed) are recorded. Not used in R0 or R1: `check --peek`, the candidate `check --all`, `inbox`. Unfiltered `check --all` and `--peek` are not allowed in any R2 argv; plain `check`, `--ack` and `run-use` are never run.
+
+## Seen on probe Runs and the coordinator's own Run only
+
+Source: `RESEARCH-REPORT-phase2-gate.md` (REPORT, in `.dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/`, evidence files 01 to 27) and `.dev/issues/409/owner-decisions-20261111.md` (OWNER). Probe Runs A `run_c1badaa6576b` and B `run_14cfcbd8edf2`, 2026-11-11. These facts were observed there and nowhere else; they are not verified for any other Run.
+
+- Envelope `{id, ok, result:{acknowledged, count, messages[], runId}, _meta}`; message row keys `id` (`msg_...`), `run_id`, `delivery_contract`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at` (REPORT 2.2, evidence file 03).
+- `--types question` filters on the server side (REPORT, evidence file 24), and the 100-row cap applies after the type filter (OWNER, own Run: 41 rows).
+- `check --all` returns at most 100 rows, newest first, with no total, `hasMore` or truncation field (evidence file 14); `check --peek` returns the oldest 100 first and hides acknowledged rows (evidence files 12, 15). `--all` rows carry no read marker.
+- A read from a caller bound to another Run answers `{"ok":false,"error":{"code":"consumer_fenced", ...}}` (exit status 1, "Nothing changed"); a caller with no terminal identity answers `no_active_terminal` (evidence files 01, 17 to 19).
+- `message.id` was unique in the probe Runs (REPORT 2.2, G-8). It is not recorded for any other Run.
 
 ## UNVERIFIED
 
 | Item | How the MVP shows it |
 |---|---|
-| Message row fields and the inbox JSON shape; only an empty peek `result.{count,dispatchId,runId}` has been seen | Not parsed before QUESTION-OBSERVATION |
-| Meaning of `result.count` | No count is ever derived from it |
-| Proof (a) `--run` narrows `--all`; proof (b) which handle receives human-addressed messages and whether an unbound observer can read; proof (c) message rate | Gate stays closed |
-| Whether a `--types` value identifies a human question | Open owner decision 8 |
-| Message IDs, inbox lease fields, terminal-attribution fields | Required before the non-consumption test (T51) |
+| The inbox JSON shape (its rows add `read` and `sequence`, REPORT 2.2, evidence file 20); whether `inbox` reaches across Runs (REPORT Q-4) | `inbox` stays forbidden; not tested; forbidden |
+| Meaning of `result.count` (equals 100 for a 104-row Run, evidence file 14) | No count is ever derived from it |
+| Proof (a) as worded, "`--run` narrows `--all`": WITHDRAWN. `--run` is a fence, not a filter (`consumer_fenced`); see `release-gates.md` | Replaced by the one-named-Run rule |
+| Proof (b), a terminal that has a handle but holds no Run (Q-1) | UNTESTED, so UNVERIFIED (REPORT 2.1 could not make such a terminal; a caller with no terminal identity at all gets `no_active_terminal`); verification task: Task 16 (gated on a plain terminal supplied by the coordinator) |
+| Whether `check --all` ever consumes when the reader is not the Run's owner | UNVERIFIED; verification task: Task 16 (non-consumption is seen only as the owner on a probe Run) |
+| Effect of `run-use` on a live coordinator (Q-2) | not tested; forbidden for the observer: `run-use` is a forbidden argv (Task 6) |
+| Whether `ask` writes type `question` (Q-3) | UNVERIFIED; not tested; forbidden for the observer (`ask` is a forbidden verb, Task 6); no R2 behaviour depends on it |
+| Message rate on any Run, and `message.id` identity on real traffic, for the Run the owner names (the owner has not named it) | UNVERIFIED; verification task: Task 17 (gated on the owner); the label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` stays |
+| Meaning of `delivered_at`, which stayed `null` on every probe row even after a consuming read and acknowledgement (REPORT 2.2, evidence files 08, 11) | UNVERIFIED; the observer never reads it as closure |
+| What identifies a human question | Decided 2026-11-11 (OWNER, decision 8): coordinator questions only (type `question`); whether the coordinator agent or a person answers is not recorded by Orca |
+| Inbox lease fields, terminal-attribution fields | `inbox` and plain `check` are never run; not tested; forbidden |
 | Value set of `projection.nextAction.kind`, and whether any value means "a human must answer" | Raw string, never classified |
 | Whether `projection.stage.activity` or `.detail` carries question text; value sets of `stage.*` | Inspector only, sanitized, labelled `worker-reported`; `stage.detail`/`.activity` withheld from the R1 snapshot (`snapshot-export-schema.md`) |
 | Meaning of `projection.evidence.durable` beyond presence | Shown raw |
 | Whether `page.total` counts historical dispatches ("Showing 2 of 287 Dispatches" suggests it, not proven); semantics of `result.counts` | Labelled `reported T`, never "workers"; counts never summed |
-| Whether `worker-list` offers a state filter for active workers | INV-007 accepted risk, `not reobserved` |
+| Whether `worker-list` offers a state filter for active workers. `worker-list --help` lists a `--terminal-state <active\|reclaimable\|retained\|release_pending\|release_unknown\|released>` filter (REPORT 5, Orca 1.4.245-aidev02.9cfecdd30b2a); its behaviour was not run, so it is still UNVERIFIED (REPORT Q-6) | INV-007 accepted risk, `not reobserved` |
 | Clock and format of `liveness.observedAt` / `evidence.lastObservedAt` | No per-row STALE; plain age only |
 | Per-call timeout value | Measured at the first permitted live read (R0 makes no Orca calls); T5 uses a configured value |
 | Whether `terminalState` values `released` and `retained` mean historical | Only those two values are hidden behind `h`; absent or other values are shown raw and never counted active (`rendering-rules.md`) |


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
