311a6922cbefb8394402dcaa46919feced7b3c76
Review one task for spec compliance.

Task brief: 
## Task 3: Rewrite the R2 row and FR-17 wording in prd.md

Depends on: Task 1

Edit `.dev/issues/409/bmad/prd-orca-observer/prd.md`: the R2 row at line 106 (section 4 table, verify the line before editing), the Attention Ledger entry that names `OPEN HUMAN QUESTIONS` at line 106, FR-17 in section 5.10 (lines 243 to 253), and the open questions OQ-7 and the decision-8 mentions (lines near 425 and 471).

- R2 row: candidate verb `orca orchestration check --all --types question --run <runId> --json`; panel title "coordinator questions"; gate status "NOT passed" with the open items from Task 1; remove proofs (a)'s old wording and the rotation.
- FR-17: "After QUESTION-OBSERVATION passes, a supervisor can see every observed open coordinator question (message type `question`) of the one named Run, retained until explicit closure evidence"; keep the T10, T11, T12, T46 consequences; keep the disclosure label verbatim; state `m` leaves the question count unchanged and that questions are listed, not individually selectable, in R2.
- OQ-7 becomes "decided 2026-11-11 (OWNER): coordinator questions only".

Acceptance criteria:
- `grep -n "OPEN HUMAN QUESTIONS\|human question" .dev/issues/409/bmad/prd-orca-observer/prd.md` finds no line that describes the R2 panel title or FR-17 as "human"; any remaining "human" occurrence is quoted history (for example the R1 notice text `Human questions: source UNVERIFIED`).
- The R2 row names `--types question`, one named Run and the disclosure label verbatim.

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

Start sha: 311a6922cbefb8394402dcaa46919feced7b3c76
Diff against the start snapshot: 
diff --git a/.dev/issues/409/bmad/prd-orca-observer/prd.md b/.dev/issues/409/bmad/prd-orca-observer/prd.md
index 64bdb3422..5211c9c74 100644
--- a/.dev/issues/409/bmad/prd-orca-observer/prd.md
+++ b/.dev/issues/409/bmad/prd-orca-observer/prd.md
@@ -103,7 +103,7 @@ The owner chose a staged direction (binding): R1 = Signal Bridge's worker ledger
 | R0 Fixture replay | Ledger screen, inspector, text export at 160/116/80, sanitizer, cell-width truncation, NO_COLOR, ID-anchored selection, every fixture variant, the synthetic `base` variant in place of a recorded sample, which R1 records at the first permitted live read (release-gates.md:9); renders of A, B and C for review. Key-reader spike first. | None from Orca; offline only. Fixtures labelled SYNTHETIC; the PROPOSED schema is used only in fixture mode. | Open to start |
 | DIRECTION-SELECTED (gate only) | Nothing ships. | The owner's dated, owner-written selection record (date, option, decider, where the statement lives). Holds the defaults, post-link choice or explicit deferral, fallback date, stack confirmation, command name and confirmed production-integration reading. The owner has already confirmed the stack (owner-decisions-20261108.md item 5, 2026-11-08); whether that confirmation counts toward the selection record is OQ-1. | **NOT passed** |
 | R1 Live worker-list | COUNTS strip, freshness strip, worker ledger with verbatim `nextAction.kind`, `result.counts`, capped paging, stale handling, changes since last look, the selected view, the question-source notice, the JSON snapshot export. | DIRECTION-SELECTED passed, production integration permitted under the reading the owner confirms, a redacted golden sample of each of the four kinds, contract test T32. | Closed |
-| R2 Attention Ledger (B) | `OPEN HUMAN QUESTIONS` with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown". | QUESTION-OBSERVATION on the candidate verb `orca orchestration check --all --run <runId> --json`, which is a candidate, never an available source, until every proof is recorded: (a) `--run` narrows `--all`, with samples from at least 2 Runs; (b) which handle receives human-addressed messages and whether an unbound observer can read; (c) measured message rate; non-consumption test (INV-022, T51), where help text and an empty peek `count` cannot clear the gate; a verified source-scoped question identity (a worker `dispatchId` is never a question's identity); open owner decisions 8 and 6; message-call budget inside the 5-call cap. All proofs UNVERIFIED. | Closed |
+| R2 Attention Ledger (B) | `COORDINATOR QUESTIONS` for one named Run (messages of type `question` only), with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". One Run only, no rotation. | QUESTION-OBSERVATION: **NOT passed**. Candidate verb, never an available source until the open items are recorded: `orca orchestration check --all --types question --run <runId> --json` for one named Run, never `run-use`, one message call per cycle inside the 5-call cap. Open items (`release-gates.md`): Q-1 (an observer terminal with a handle but no Run, UNVERIFIED), the message rate and identity on the Run the owner names (the owner has not named it), and the owner's written pass record. Seen on probe Runs only: the read returns only the bound Run's mailbox (`consumer_fenced` for another Run), and non-consumption as the Run's owner for the visible effects tested (INV-022, T51). Question identity is `message.id`, a worker `dispatchId` is never a question's identity. Owner decisions 8 and 6 decided 2026-11-11 (coordinator questions only; one named Run, `--types question`, never `run-use`). | Closed |
 | R3 Decision Desk (C) | For the selected question, affected sessions with worker-list evidence. | QUESTION-LINK: authoritative mapping from IDs in a message to `dispatchId`/`worktreeId`, verified on this host first; optional owner re-confirm of the post-link default (B or C). No named decider beyond that. | Closed |
 | R4 Remote fleet | `--include-remote` rows grouped by `projection.host.id`. | Cross-host ownership joins. Not established. | Closed |
 | Later | Closure evidence (`closed by evidence`), history beyond the 100-row window, admission and verification, cost, deep links. | Each needs its own feed; none established. | Closed |
@@ -242,14 +242,14 @@ Consequences (testable):
 
 ### 5.10 F-Attention Attention Ledger (CAP-11, R2; gated by QUESTION-OBSERVATION)
 
-**FR-17.** After QUESTION-OBSERVATION passes, a supervisor can see every observed open human question retained until explicit closure evidence; seen is not resolved.
+**FR-17.** After QUESTION-OBSERVATION passes, a supervisor can see every observed open coordinator question (message type `question`) of the one named Run, retained until explicit closure evidence; seen is not resolved. Questions are listed, not individually selectable, in R2; `m` leaves the question count unchanged (it marks worker rows only).
 Consequences (testable):
 - `m` on every item leaves the open count unchanged (T10).
 - `source-loss` keeps the open count and every retained item (T11); an item missing next cycle stays, marked `no longer in source window` (T12).
 - At 1,001 retained questions, eviction does not lower the open total (T46).
 - The panel is labelled "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost" and discloses the 100-row source window; the label stays after the gate passes, because a measured rate does not prove completeness (CAP-11; release-gates.md).
-- Each item states why it matters (issue 409 AC 2, "explains why they matter", I:78, I:19). `[ASSUMPTION]` (A7) The reason is a sourced field shown verbatim, or `reason unknown` when the source carries none; the observer never writes a reason of its own. Which message field carries it depends on OQ-7 (what identifies a human question); message fields are UNVERIFIED (U1). The spec carries reasons only as a field of attention items (acceptance-tests.md AC-3); no spec test pins it; test ID not assigned.
-- T19 and T51 are placeholders, skipped until the gate. T51 is the quiet-scope non-consumption test (INV-022).
+- Each item states why it matters (issue 409 AC 2, "explains why they matter", I:78, I:19). `[ASSUMPTION]` (A7) The reason is a sourced field shown verbatim, or `reason unknown` when the source carries none; the observer never writes a reason of its own. No verified message field carries a reason, so R2 shows `reason unknown` (PROPOSED); what identifies a question is decided (OQ-7, 2026-11-11: type `question`); message row keys were seen on probe Runs only and stay UNVERIFIED for other Runs (U1). The spec carries reasons only as a field of attention items (acceptance-tests.md AC-3); no spec test pins it; test ID not assigned.
+- T19 and T51 are tests in R2 (fake-runner and recorded-sample tests; T52 to T56 are added in `acceptance-tests.md`); the live question read stays refused until the gate passes (T56). T51 is the quiet-scope non-consumption test (INV-022); its pass covers only the visible effects tested, as the Run's owner on a probe Run.
 - Nothing in this FR ships in R1. Message rows are not parsed before the gate.
 
 ### 5.11 F-Desk Decision Desk (CAP-12, R3; gated by QUESTION-LINK)
@@ -422,7 +422,7 @@ Recorded dissents (owner-decisions-and-risks.md): `page.total` required (V1) ver
 - **OQ-4.** Fallback date for QUESTION-OBSERVATION?
 - **OQ-5.** Sample capture and acquisition permission for live reads (open owner decision 6)?
 - **OQ-6.** Message-content exposure (open owner decision 7)?
-- **OQ-7.** What identifies a human question (open owner decision 8)?
+- **OQ-7.** Decided 2026-11-11 (OWNER, `owner-decisions-20261111.md`): coordinator questions only (message type `question`); the list is not labelled "human".
 - **OQ-8.** Multi-observer restriction (open owner decision 9)?
 - **OQ-9.** Licence opinion before any Go screen reads the snapshot?
 - **OQ-10.** Does TUIBBS become the staff platform?
@@ -468,7 +468,7 @@ The recommendations are the spec's, recorded for the owner. None is a decision.
 5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option. (OQ-4)
 6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, with the owner setting redaction rules. Unblocks B's headline panel. (OQ-5)
 7. **Message-content exposure.** What may be displayed and what exported, kept as separate permissions; no recommendation beyond that. (OQ-6)
-8. **Question-type choices.** What makes a message a "human question", which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference. (OQ-7)
+8. **Question-type choices.** Decided 2026-11-11: coordinator questions only, messages of type `question`, never inferred from text (OWNER, `owner-decisions-20261111.md`). (OQ-7)
 9. **Multi-observer restriction.** Caps are per process, no singleton. Recommend disclosure only. (OQ-8)
 10. **Still open from owner-decisions-20261108.md:** write-back stage (summary decision 3), TUIBBS licence opinion (decision 4), TUIBBS as staff platform (decision 5). (OQ-11, OQ-9, OQ-10)
 
@@ -488,8 +488,8 @@ The source table has no ids; U1-U19 are extractor row numbers.
 |---|---|---|
 | U1 | Message row fields and the inbox JSON shape; only an empty peek `result.{count,dispatchId,runId}` has been seen | Not parsed before QUESTION-OBSERVATION |
 | U2 | Meaning of `result.count` | No count is ever derived from it |
-| U3 | QUESTION-OBSERVATION proofs (a), (b), (c) | Gate stays closed |
-| U4 | Whether a `--types` value identifies a human question | Open owner decision 8 (OQ-7) |
+| U3 | QUESTION-OBSERVATION open items: Q-1, message rate and identity on the named Run, the owner's written pass record (proof (a) as first worded is withdrawn, `release-gates.md`) | Gate stays closed (NOT passed) |
+| U4 | Whether the coordinator agent or a person answers a `question` row (Orca has no human recipient field) | Decided 2026-11-11 (OQ-7): the list reads "coordinator questions" |
 | U5 | Message IDs, inbox lease fields, terminal-attribution fields | Required before T51 |
 | U6 | Value set of `projection.nextAction.kind`, and whether any value means "a human must answer" | Raw string, never classified |
 | U7 | Whether `projection.stage.activity` or `.detail` carries question text; value sets of `stage.*` | Inspector only, sanitized, labelled `worker-reported`; withheld from the R1 snapshot |


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
