---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-release2OfTheOrc-20261111-203306
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Orca terminal observer, release 2 (coordinator questions list for one named Run)

Source: ./source.md
Goal: `superclaude observe --run <runId> --questions` shows a "coordinator questions" panel built only from `orca orchestration check --all --types question --run <runId> --json` on one named Run, with observer-side retention, the 100-row cap disclosure and honest unknowns; the gate text, tests and recorded samples match what was observed, and the live read stays switched off until the gate record is written by the owner.

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

## Phase 1: Rewrite the gate record to match the evidence

## Task 1: Rewrite the QUESTION-OBSERVATION gate in release-gates.md

Edit `.dev/issues/409/bmad/spec-orca-observer/release-gates.md`, section "QUESTION-OBSERVATION (before R2)" and the R2 row of the release table (REPORT section 8 item 8.1, Section 2.1 and 2.2).

- Replace proof (a) with: the read returns only the mailbox of the Run the caller is bound to, and a caller bound to another Run is fenced with `consumer_fenced` ("Nothing changed"); `--run` is a fence, not a filter, so "narrows `--all`" is withdrawn. Record the two-Run evidence (probe Run A and Run B, 2026-11-11) as the basis.
- Proof (b): record that messages land in the Run mailbox (`to_handle` `run:<id>`), that Orca has no human recipient field, that a caller with no terminal identity gets `no_active_terminal`, and that a terminal with a handle but no bound Run is UNTESTED (Q-1, Task 16).
- Proof (c): keep UNVERIFIED; record the measured facts only (100-row bound, `--all` newest first and `--peek` oldest first, about 0.2 s per call on a probe Run, no total or truncation field) and the coordinator's own-Run counts from OWNER (100 rows with 91 heartbeats unfiltered; 41 rows with `--types question`).
- Non-consumption (INV-022): record pass on a probe Run as the Run's owner for the visible effects tested, and that `--all` rows carry no read marker.
- Question identity: record `message.id` seen on probe and own-Run data, UNVERIFIED elsewhere.
- Owner inputs: record decisions 8 and 6 as given in OWNER (date 2026-11-11, decider the owner), the one-named-Run, `--types question` and never-`run-use` reading, and that the Run is not yet named.
- Remove rotation from R2 and state the budget: one message call per cycle.
- Keep the status line "QUESTION-OBSERVATION: not passed" and list what is still open (Q-1, message rate on a named Run, owner-written pass record).

Acceptance criteria:
- `grep -n "narrows" .dev/issues/409/bmad/spec-orca-observer/release-gates.md` finds no live claim that `--run` narrows `--all`; the file says `--run` is a fence and quotes `consumer_fenced`.
- The section contains the verbatim label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, the words `one named Run`, `--types question` and `never run-use`, and a status line that reads not passed.
- Every recorded fact cites REPORT or OWNER by name; nothing is stated as verified beyond what REPORT records.

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

## Task 3: Rewrite the R2 row and FR-17 wording in prd.md

Depends on: Task 1

Edit `.dev/issues/409/bmad/prd-orca-observer/prd.md`: the R2 row at line 106 (section 4 table, verify the line before editing), the Attention Ledger entry that names `OPEN HUMAN QUESTIONS` at line 106, FR-17 in section 5.10 (lines 243 to 253), and the open questions OQ-7 and the decision-8 mentions (lines near 425 and 471).

- R2 row: candidate verb `orca orchestration check --all --types question --run <runId> --json`; panel title "coordinator questions"; gate status "NOT passed" with the open items from Task 1; remove proofs (a)'s old wording and the rotation.
- FR-17: "After QUESTION-OBSERVATION passes, a supervisor can see every observed open coordinator question (message type `question`) of the one named Run, retained until explicit closure evidence"; keep the T10, T11, T12, T46 consequences; keep the disclosure label verbatim; state `m` leaves the question count unchanged and that questions are listed, not individually selectable, in R2.
- OQ-7 becomes "decided 2026-11-11 (OWNER): coordinator questions only".

Acceptance criteria:
- `grep -n "OPEN HUMAN QUESTIONS\|human question" .dev/issues/409/bmad/prd-orca-observer/prd.md` finds no line that describes the R2 panel title or FR-17 as "human"; any remaining "human" occurrence is quoted history (for example the R1 notice text `Human questions: source UNVERIFIED`).
- The R2 row names `--types question`, one named Run and the disclosure label verbatim.

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

## Task 5: Update acceptance-tests.md and rendering-rules.md for the one-Run panel

Depends on: Task 4

Edit `.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md` (rows T19, T46, T47, T51, and AC-6 line) and `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` (lines about `OPEN HUMAN QUESTIONS`, `SEEN IS NOT RESOLVED`, `RETAIN CONTEXT`, rotation and the empty rotation set).

- T19 (no longer a placeholder): the question panel title contains `at most 100 rows per read, not 100 questions` and `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.
- T51 (no longer a placeholder): fake-runner quiet-scope test using the probe shapes (Task 15), covering only the visible effects tested.
- T46, T47: reword for one Run; T47 keeps the pre-gate and flag-off wording.
- Add new tests: T52 `consumer_fenced` and `no_active_terminal` render and keep retained questions; T53 the exact message argv and forbidden set; T54 the 100-row cap fixture shows `window full`; T55 the four recorded samples of the message read; T56 live `--questions` refused while the gate guard is off. Give each its AC mapping.
- rendering-rules.md: panel title `COORDINATOR QUESTIONS`, line `one Run only: <runId>`, per-question line (age, subject, `reason unknown`), `closed by evidence: unavailable`, `retention reset at HH:MM; questions observed before this start are not retained`; delete the rotation lines and the empty-rotation-set note.

Acceptance criteria:
- Each of T19, T46, T47, T51 to T56 has a one-sentence pass condition that matches the tests built in Tasks 6 to 15.
- `grep -n "revisit\|empty rotation\|OPEN HUMAN" .dev/issues/409/bmad/spec-orca-observer/rendering-rules.md .dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md` finds nothing that is still live behaviour.

## Phase 2: The read-only message adapter

## Task 6: Add the question template, forbidden verbs and error codes to adapter.py

Depends on: Task 4

Edit `src/superclaude/cli/observe/adapter.py` and `tests/observe/conftest.py` and add tests to `tests/observe/test_adapter.py`.

- Add `QUESTION_TEMPLATE = ("orchestration", "check", "--all", "--types", "question")` plus `--run <runId>` then `--json`; extend `FORBIDDEN_PREFIXES` with `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`; the existing `check` prefix stays forbidden except for exactly this template (the allow decision is made on the whole argv, not the token). `--peek` and a `check --all` without `--types question` or without `--run` stay refused.
- Extend `assert_allowed`, `_option_positions` and `build_argv` (new `build_question_argv(orca, run_id)`) so the run id passes `check_run_id`.
- Add `LiveSource.read_questions(clock, budget_deadline, run_id)`: one call, no paging, same timeout and output-cap handling; returns a `SourceResult` whose single page is the decoded envelope. When the decoded stdout is an object with `ok` false, map `error.code` `consumer_fenced` to source code `consumer-fenced` and `no_active_terminal` to `no-active-terminal` (add both to `CODES`), whatever the exit status; any other error code maps to `exit:<n>` or `json` as today. Diagnostics stay sanitized and under 2 KiB.
- Update `argv_allowed` in `tests/observe/conftest.py` to accept the question template and nothing else new.

Acceptance criteria:
- `uv run pytest tests/observe/test_adapter.py -v` passes with new tests: the fake runner receives exactly the template argv with `--run run_14cfcbd8edf2`-style ids; each of `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, `inbox`, plain `check`, `check --peek`, `check --all` without `--types question`, the template without `--run`, a run id starting with `-` and a malformed run id raises `ArgvRejected` before the runner is called.
- A fake runner returning the recorded `consumer_fenced` error envelope (exit 1) yields `FAILED` with code `consumer-fenced`; one returning `no_active_terminal` yields `FAILED` with code `no-active-terminal`; both leave the argv log with exactly one message call.
- A static test shows `--ack`, `--wait`, `--retry-request`, `--peek` and `run-use` appear in adapter.py only inside the forbidden set.

## Task 7: Parse question rows in parse.py

Depends on: Task 6

Edit `src/superclaude/cli/observe/parse.py` and add tests to `tests/observe/test_parse.py`. First open REPORT's evidence files 03, 14 and 24 and use their real key names; invent no key.

- Add a frozen `Question` dataclass: `qid` (the `message.id`), `run_id`, `namespace`, `from_handle`, `subject`, `priority`, `thread_id`, `created_at` (text) and `created_epoch` (parsed with `parse_timestamp`, else unknown), every field `UNKNOWN` when absent. `body`, `payload` and `to_handle` are not kept.
- Add `parse_questions(page, namespace, cycle)` returning rows plus counts: required `result.messages` a JSON list (else `ShapeError`, same rule as `parse_page`); a row that is not an object is counted and skipped; a row whose `type` is not `question`, or whose `run_id` differs from the requested Run, is dropped and counted as `contradictory rows ignored`; a row with no `id` has no identity, is flagged `identity unknown`, is not retained; duplicate ids in one read are counted. All strings pass `sanitize`.
- Identity is Run plus `message.id`; never a `dispatchId`.

Acceptance criteria:
- `uv run pytest tests/observe/test_parse.py -v` passes with new tests built from the probe shapes: a 2-row envelope parses to 2 `Question` rows; `result.messages` missing, `null` or not a list raises `ShapeError`; a status-type row and a wrong-Run row are dropped and counted; absent `subject` reads `UNKNOWN`; `[bold]` in a subject stays literal text; no parsed object has a `body` attribute.
- A deep-nesting or injection subject (CSI, OSC 8, U+202E) leaves no ESC, C1 or Cf character in the parsed value.

## Phase 3: Retention and collector integration

## Task 8: Build the question retention store in questions.py

Depends on: Task 7

Create `src/superclaude/cli/observe/questions.py` and `tests/observe/test_questions.py` (SPECDIR `adapter-contract.md` "R2 onward" as rewritten by Task 4; PRD FR-17).

- A pure store, no I/O: `merge_questions(previous, parsed_rows, cycle, window_full, source_ok)` returns a new immutable state. Keyed by (Run, `qid`). Each record keeps `first_seen_cycle`, `last_seen_cycle`, `in_window` and the `Question` fields.
- A question seen before and absent from a later successful read stays and is marked `no longer in source window`. A failed question read changes nothing. Nothing is ever marked closed: closure evidence is `unavailable (no source)`.
- Bound 1,000 records; when exceeded the oldest-created record is evicted, an `evicted` counter grows, the open total never goes down, and `open_total_text` reads `unknown (retention exceeded)` with the retained count shown. Order is oldest created first, unknown created time last.
- `window_full` is true when one read returned exactly 100 messages; it is carried in the state for the disclosure.

Acceptance criteria:
- `uv run pytest tests/observe/test_questions.py -v` passes: T46 (1,001 distinct questions keep the open total from falling and show `unknown (retention exceeded)` with 1,000 retained); T11 (a failed read keeps every record); T12 (a question missing from the next successful read stays, marked `no longer in source window`); a handled question that Orca still returns is listed again as open (no read marker exists), asserted by a test that names this limit.
- Two Runs' questions with the same `qid` stay two records (key includes the Run).

## Task 9: Wire the question read into the collector

Depends on: Task 6, Task 8

Edit `src/superclaude/cli/observe/collector.py` and add tests to `tests/observe/test_collector.py`.

- `CycleSource` gains `read_questions(clock, budget_deadline, run_id)`; `FixtureSource` returns a `FAILED` result with code `not-found`-style `no-question-fixture` unless a question fixture is supplied (fixture questions are synthetic and labelled so).
- `Collector.__init__` takes `questions: bool = False`. When true and a `run_id` is set, each cycle reads worker-list with a 4-call page cap (`LiveSource.read_pages` gets `max_calls`), then makes exactly one `read_questions` call inside the same cycle budget and merges the result with the store from Task 8. `CycleResult` gains optional fields with defaults (`questions`, `question_state`, `question_code`, `question_last_success_mono`), so existing callers and tests are unchanged.
- A failed question read never changes the worker-list state, the backoff or the retained records; a failed worker-list read never discards retained questions.

Acceptance criteria:
- `uv run pytest tests/observe/test_collector.py -v` passes, including: with questions on, one cycle logs worker-list calls plus exactly one message call and never more than 5 subprocesses (a fake worker-list that always says `hasMore` stops at 4 pages, plus 1 message call); with questions off the argv log is unchanged from release 1 (still 5 pages possible, T4 intact).
- A `consumer-fenced` question reply leaves the ledger `OK` and sets `question_state` to `FAILED` with the code; a later good read recovers.
- The message call is skipped, with `question_code` `overrun`, when the cycle budget is already spent.

## Phase 4: Display, export and command line

## Task 10: Add the coordinator questions panel to view.py and render.py

Depends on: Task 8, Task 9

Edit `src/superclaude/cli/observe/view.py`, `src/superclaude/cli/observe/render.py` and add tests to `tests/observe/test_view.py` and `tests/observe/test_render.py` (rendering rules as rewritten by Task 5).

- With questions on, `build_view` adds a question section: title `COORDINATOR QUESTIONS`, line `one Run only: <runId>`, the disclosure `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost`, the counts line `observed open: n | closed by evidence: unavailable (no source)`, one line per question oldest first (age, sanitized subject, `reason unknown`), windowed with `x/y shown` when the height cannot hold them, and `window full: older questions may be missing` when exactly 100 rows came back.
- States in plain words: never read yet (`question read pending`), `FAILED (consumer-fenced)` and `FAILED (no-active-terminal)` with the sentence `this terminal does not hold the named Run; the observer never binds to a Run`, STALE after 45 s without a good question read (monotonic clock), and an empty good read reads `no observed questions in this source window; not proof none exist`, never `no questions`.
- The header cell `MESSAGES_CELL` reads `coordinator questions: one Run, last read <age> ago` when on; with questions off it keeps `messages UNVERIFIED (not read)`. `GAP_NOTICE` is replaced by the panel only when questions are on and the source has read once; otherwise it stays (T9, T47). The ledger title stays `worker-reported, not questions`.
- Header and panel stay at or under the terminal width at 160, 116 and 80 columns; the too-small diagnostic (T49) still carries a question-source line.
- The `m` key keeps marking worker rows only; it never changes the question count.

Acceptance criteria:
- `uv run pytest tests/observe/test_view.py tests/observe/test_render.py -v` passes with new tests: T19 title text present; T47 with questions off is byte-identical to release 1 output; T10 `m` on every worker row leaves `observed open` unchanged; T12 and T11 render the retained and `no longer in source window` lines; an empty good read never contains the words `no questions`; every screen line has `cell_len <= W` at 160, 116 and 80; a subject with `[bold]` renders literally; the fenced state names the sentence above.
- With retention exceeded the count reads `unknown (retention exceeded)` and shows the retained count.

## Task 11: Add the question group to the snapshot export

Depends on: Task 10

Edit `src/superclaude/cli/observe/export.py`, `src/superclaude/cli/observe/snapshot.schema.json` and add tests to `tests/observe/test_snapshot_schema.py` and `tests/observe/test_export.py`.

- Add an optional `questions` object to the snapshot when questions are on: `runId`, `state`, `code`, `observedOpen` (number or the string `UNKNOWN`), `windowFull`, `retained`, `evicted`, `closureEvidence` fixed to `unavailable`, and per question only `id`, `createdAt`, `ageSeconds`, `inWindow`. No subject, body, handle or payload is exported. The record text export (`e`, `--once`) carries the same lines as the screen.
- Keep `schemaVersion` 1 if the schema accepts the optional group; otherwise record the change in the schema file and the test (the existing test rejects an unknown major).

Acceptance criteria:
- `uv run pytest tests/observe/test_snapshot_schema.py tests/observe/test_export.py -v` passes: a snapshot with questions on validates; one with questions off is byte-identical to release 1; a test asserts the exported JSON holds no `subject`, `body`, `from_handle` or `payload` key anywhere; missing values are the string `UNKNOWN`.
- The record export contains no ESC byte and the full question ids.

## Task 12: Add the `--questions` flag and the gate guard to commands.py

Depends on: Task 9, Task 10

Edit `src/superclaude/cli/observe/commands.py` and add tests to `tests/observe/test_commands.py` and `tests/observe/test_registration.py`.

- Add option `--questions` (flag). It requires `--run <runId>` (checked with `check_run_id`) and a live source; with `--fixture`, without `--run`, or with a malformed run id the command exits non-zero with a plain message and runs no Orca call.
- Add one module constant `QUESTION_GATE_PASSED = False` with a comment naming `release-gates.md` and Task 18. While False, `--questions` exits non-zero with `question read not enabled: QUESTION-OBSERVATION has not passed` and makes no Orca call, not even discovery.
- Pass `questions=True` into the `Collector` only past the guard. Update `HELP` with: the one-named-Run rule, "run it from the terminal that already holds the Run; the observer never runs run-use", the disclosure label, and "message bodies are received by this process; subjects are shown, bodies are not kept".

Acceptance criteria:
- `uv run pytest tests/observe/test_commands.py tests/observe/test_registration.py -v` passes: T56 (guard False: exit non-zero, empty argv log); with the constant monkeypatched True, `--run run_14cfcbd8edf2 --questions --once` through the fake runner logs worker-list calls plus one template message call and prints the panel; `--questions` without `--run`, with `--fixture`, and with `--run -x` are refused with no Orca call; the `--help` text contains `never runs run-use`.

## Phase 5: Recorded samples and the required tests

## Task 13: Record the four redacted message-read samples and pin them in contract tests

Depends on: Task 9, Task 10

Create `src/superclaude/cli/observe/fixtures/golden-question-success.json`, `golden-question-missing.json`, `golden-question-stale.json`, `golden-question-contradictory.json` and extend `tests/observe/test_golden_contract.py` and `tests/observe/test_fixtures.py` (data-gate rule in `release-gates.md`: four kinds, each pinned in a contract test). Build them from the already recorded probe outputs in REPORT's evidence folder (success from files 03 and 24; missing from file 03 with `messages` removed and from the `no_active_terminal` file 17; contradictory from a success envelope carrying a status-type row and a row from another Run, and from the `consumer_fenced` file 01 read by a bound Run; stale from the success envelope replayed after the clock advances beyond 45 s). Do not make any new Orca call. Redact before saving: replace `from_handle`, `to_handle`, Run ids and message ids with synthetic stable values, remove `body`, keep key names and types. Mirror how the existing four `golden-*` worker-list samples are loaded and tested in `tests/observe/test_golden_contract.py`, and write `./artifacts/t13-redaction.md` listing each field replaced.

Acceptance criteria:
- `uv run pytest tests/observe/test_golden_contract.py tests/observe/test_fixtures.py -v` passes: success parses to the expected question count and ids; missing gives `FAILED (shape)` or `no-active-terminal` with retained questions kept; stale shows `STALE` after the monotonic clock passes 45 s with the questions kept; contradictory rows are dropped and counted and `consumer-fenced` is shown.
- The sensitive-string scan used by `test_fixtures.py` (`SENSITIVE`) finds no `term_` handle, token, credential or absolute path in the four files.

## Task 14: Build the 100-row cap fixture and its test

Depends on: Task 10

Create `tests/observe/test_question_cap.py` and the fixture builder `make_question_rows(n)` in `tests/observe/conftest.py`, with a recorded-shape fixture `src/superclaude/cli/observe/fixtures/question-cap-100.json` of exactly 100 redacted `question` rows, newest first, shaped like REPORT evidence file 14 (the 104-message probe Run read: exactly 100 rows, the 4 oldest silently missing, no total or truncation field).

Acceptance criteria:
- `uv run pytest tests/observe/test_question_cap.py -v` passes: a 100-row reply sets `window full` and the panel shows `window full: older questions may be missing` and the disclosure label; a 99-row reply does not; two cycles where the second returns a window that has moved on (newest 100 only) keep the dropped questions retained as `no longer in source window` and the open total does not fall; the panel never prints a total taken from `result.count`.
- The test asserts that no argv in the log contains `--peek` and that every message argv has `--types question`.

## Task 15: Build the T51 quiet-scope non-consumption test

Depends on: Task 6, Task 9

Create `tests/observe/test_question_quiet_scope.py` (T51, `acceptance-tests.md` as rewritten by Task 5; INV-022). It uses a stateful fake Orca backend over the probe shapes (REPORT section 2.2 steps 1 to 9, evidence files 03 to 12): the fake keeps a mailbox of question rows and a `delivered_at`/ack state, answers only the question template, and fails the test if any argv could consume (`check` without `--all`, `--ack`, `--wait`).

- Step one establishes readable identity: the test asserts every returned row has a `msg_` id, a Run id and a created time before any comparison.
- Then repeated reads on a quiet scope (no sender writes between reads): before-and-after readings through the observer return identical question ids, identical order and an unchanged fake mailbox state (no delivery or ack field changed).
- The test docstring and a final assertion message state that a pass covers only the visible effects tested, as the owner as Run owner on a probe Run, and does not show non-consumption by a non-owner reader (Q-1).

Acceptance criteria:
- `uv run pytest tests/observe/test_question_quiet_scope.py -v` passes; a deliberately consuming fake (mailbox changes on read) makes a companion test fail, proving the test can detect consumption.
- The test file contains no `--peek`, `--ack` or `run-use` argv apart from the assertions that forbid them.

## Phase 6: Gated verification and enabling the live read

## Task 16: Verify Q-1 from a fresh plain terminal against the probe Run (gated)

Depends on: Task 2

Answer Q-1 (REPORT section 9) and the question whether `check --all` consumes when the reader is not the owner. The probe Runs `run_c1badaa6576b` (Run A) and `run_14cfcbd8edf2` (Run B) were created by the gate research worker as throwaways; use only them. The check needs a plain Orca terminal that has a handle and holds no Run, which the executor may not have: a coordinator must open one. Run only `orca-ide orchestration check --all --types question --run run_c1badaa6576b --json` from that terminal, once (no `--peek` form is needed); never plain `check`, `--ack`, `run-use` or any send. Then, from the owning terminal, read Run A once with `check --all` and compare ids and count before and after to see whether the reader changed anything.

Write `./artifacts/q1-result.md` with the command, date, redacted output shape, the observed error code or the row count, and one verdict line: `Q-1: PASS (an unbound terminal with a handle can read)`, `Q-1: FAIL (<error code>)` or `Q-1: BLOCKED (<reason, for example no plain terminal available>)`. Update the Q-1 row in `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md` with the verdict and the artifact name.

Acceptance criteria:
- `./artifacts/q1-result.md` exists and holds exactly one of the three verdict lines, with real command output shape for PASS and FAIL and a stated reason for BLOCKED; nothing is fabricated or assumed.
- The register row for Q-1 states the same verdict. No Orca command other than the non-consuming `check --all` forms on Run A or Run B was run, shown by the command list in the artifact.

## Task 17: Capture one permitted redacted sample on the owner-named Run (gated on the owner)

Depends on: Task 16, Task 12

Blocked until the owner names the Run and the redaction rules (open question for the owner; OWNER decision 6 grants the read but names no Run). When the Run is named, run it from a terminal that already holds that Run, never with `run-use`, as one non-consuming read: `orca-ide orchestration check --all --types question --run <named Run> --json`, once, plus one repeat a few seconds later to see whether ids change. Keep only redacted shapes. Record the counts per read, `window full` or not, the observed number of question rows, the interval between the two reads and any new message ids, and whether `message.id` stayed unique.

Write `./artifacts/t17-sample.md` (redacted, no bodies, no handles) and update `release-gates.md` proof (c) and the question-identity line with the measured values, still labelled UNVERIFIED for any other Run and still carrying the disclosure label after the sample. If the Run is not named, write `./artifacts/t17-sample.md` with `T17: BLOCKED (owner has not named the Run)` and change nothing else.

Acceptance criteria:
- `./artifacts/t17-sample.md` holds either measured redacted values with the command shape and date, or the one BLOCKED line; the argv log in the artifact shows only the template argv.
- When measured, `release-gates.md` states the sample size, the date and the Run's role (named by the owner), says the rate is not proof of completeness, and keeps `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.

## Task 18: Record the gate outcome and, only against an owner-written pass record, enable the live read

Depends on: Task 12, Task 13, Task 14, Task 15, Task 16, Task 17

Edit `src/superclaude/cli/observe/commands.py` constant `QUESTION_GATE_PASSED` and `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` status line, and add a test to `tests/observe/test_commands.py`. Agents cite the owner's statement, never write it (release-gates.md).

- Flip `QUESTION_GATE_PASSED` to True only if `release-gates.md` or a dated owner decisions file under `.dev/issues/409/` contains an owner-written record that QUESTION-OBSERVATION passed with the open items of Task 1 resolved (Q-1 verdict recorded, sample recorded, owner decisions 8 and 6 recorded); cite that record by path in the commit-ready change description of the task log. Otherwise leave the constant False, set the `release-gates.md` status line to `not passed` with the list of open items and the fallback-date rule, and end the task as BLOCKED with the reason.
- If Q-1 is FAIL or BLOCKED, or the Run was never named, the observer keeps its guard and the owner re-confirms direction at the fallback date (release-gates.md fallback rule); no code path bypasses the guard.

Acceptance criteria:
- `uv run pytest tests/observe -q` passes in full, the guard test of Task 12 is updated to the constant's current value, and the argv log of every test shows only the worker-list template, the discovery probe and the question template.
- Either the constant is True with the owner's record cited by path, or it is False with the status line and BLOCKED reason; no state where the constant is True without a cited owner-written record.
- `grep -rn "run-use" src/superclaude/cli/observe/` shows `run-use` only in the forbidden set and in help text saying the observer never runs it.
