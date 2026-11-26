---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-designSpec-20261126-144507
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Build the offline harness for the Jev versus keyword table experiment (issue 611)

Source: ./source.md
Goal: A tested, offline measurement harness for the Jev versus keyword table comparison exists under `.dev/research/jev-vs-keyword-table-611/`, with the agreed decision rule recorded in its rule file and the gates that keep every live call closed until a person has frozen the corpus and given a go. No prompt is sent anywhere while building it.

## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, and set a fake key with `monkeypatch.setenv`. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need.
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file, and the scorer refuses to run while any field is `UNSET`: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid.
- Where the design says a dry run goes against the mock transport, the real client behaves differently: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. Tests that need the transport path pass `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by the gate: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.

## Phase 1: Foundation

## Task 1: Create the experiment folder, the test setup and the single question file

Create `.dev/research/jev-vs-keyword-table-611/questions.py`, `.dev/research/jev-vs-keyword-table-611/harness/__init__.py` (empty), `.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py`.

`questions.py` is the only place Jev question wording lives. It imports `choice` and `noul` from `jevlib.questions` and exposes `QSET_VERSION`, `TYPES = ("bug", "build", "performance", "deployment", "security", "test")` and `build_questions() -> dict` returning two questions: `problem_type`, a `choice` over the six types with a one-sentence plain definition per option (no positional option names such as `a` or `option1`, and no copy of the keyword cues in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` lines 152 to 159), and `any_type_fits`, a `noul` asking whether any of the six types fits the problem in `state["prompt"]`, with `true` and `false` criteria. No corpus prompt, label or corpus-derived example appears in the file.

`conftest.py` inserts `.dev/research/346-review-loop-experiments/p15/jev` and the experiment folder into `sys.path` (the same pattern as `p15/jev/tests/conftest.py`), provides an autouse fixture that fails any test that calls `socket.socket.connect`, and a fixture that sets a fake `JEV_API_KEY` with `monkeypatch.setenv`.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py -v` passes.
- `test_questions.py` shows that `jevlib.questions.build_request({"prompt": "x"}, build_questions())` succeeds, the choice has exactly the six type names, the noul has `true` and `false` criteria, and `request_sha256` is identical across two calls.
- A test shows the socket guard fails a test that tries to connect.
- `grep -n "keyword" .dev/research/jev-vs-keyword-table-611/questions.py` finds no copy of the table's cue words ("slow", "latency", "stack trace", "pytest").

## Task 2: Write the rule file and the loader

Depends on: Task 1

Create `.dev/research/jev-vs-keyword-table-611/decision-rule.md`, `.dev/research/jev-vs-keyword-table-611/harness/loader.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py`.

`decision-rule.md` starts with a front-matter block of plain `key: value` lines (stdlib parser, no nesting) holding: `status: AGREED`, `agreed_by`, `agreed_at: 2026-11-26`, `relayed_owner_words`, `alpha_inverse: 20`, `median_limit_s: 2`, `slowest_limit_s: 5`, `attempt_timeout_s: 10`, `median_population: answered_only`, `rerun_policy: one_per_prompt`, `p90_method: nearest_rank`, `spend_cap_usd: 1.0`, `noul_low: 0.3`, `noul_high: 0.7`, `noul_low_operator: UNSET`, `noul_high_operator: UNSET` and `unresolved_failure_invalid_count: UNSET`. Its body holds a section `## Agreement text (verbatim)` with the IronFlow reply of 2026-11-26 word for word as in the Constraints above, and a section `## Rule in words` restating the agreed rule from the Constraints.

`loader.py` provides `sha256_file(path)`, `load_rule(path) -> dict` (refuses when a required key is missing, when `status` is not `AGREED`, when `agreed_by`, `agreed_at` or the verbatim agreement text is empty, and, when asked to prepare scoring, when any value is `UNSET`), `load_corpus(path)` and `load_table_answers(path)` (JSON lines). A corpus row has `id`, `text`, `source`, `retrieved_on`, `selection_reason`, `label` (one of the six types, `ambiguous` or `none-fit`), `label_basis`, `labeller`, `labelled_on` and `seen_by_table`. `load_corpus` rejects a missing public `source`, a duplicate `id`, the same `text` under two ids, a label outside the allowed set, a missing type among the six, no `ambiguous` row and no `none-fit` row, and runs `jevlib.manifest.privacy_violation` on each prompt with data class `public`, failing with the reason string and the prompt id (never the matched text).

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py -v` passes (requirement T-04 and the rule-file refusals of T-01).
- Tests show `load_rule` refuses `PROPOSED`, `PENDING`, an empty agreement text and a missing key, and refuses scoring while an `UNSET` value remains, while the file as committed loads with `UNSET` for exactly the three open fields.
- Tests show `load_corpus` rejects each case listed above, including a prompt containing a GitHub URL and one containing a home-directory path (the cases `jevlib.manifest.privacy_violation` refuses).
- `decision-rule.md` as committed contains the verbatim IronFlow agreement text and the relayed owner words marked as relayed.

## Phase 2: Scoring

## Task 3: Build the pure scoring functions

Depends on: Task 2

Create `.dev/research/jev-vs-keyword-table-611/harness/scorer.py` (first part) and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py`. Functions, all pure and stdlib only: `right(label, answer) -> bool` (answer `None` means unset); `sign_test_passes(b, c) -> bool` using `math.comb` and the integer test `20 * tail < 2 ** n` with `n = b + c` and `tail = sum(comb(n, k) for k in range(b, n + 1))`, reading the factor 20 from the rule's `alpha_inverse`; `jev_answer(noul_p, choice, rule) -> (answer, reason)` returning the type, or `None` with reason `none-fit` or `not-settled`, from `noul_low`, `noul_high` and the two operators (`lt`, `le`, `gt`, `ge`), refusing when an operator is `UNSET`; `median(values)` (even count: mean of the two middle values), `percentile_nearest_rank(values, 0.9)` (index `ceil(0.9 * n) - 1` of the sorted list) and `latency_stats(attempts, rule)` returning the median over the population `median_population` says, the slowest over all attempts with a timeout counted at `attempt_timeout_s`, and the 90th percentile.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py -v` passes.
- A test asserts `sign_test_passes` is True for 5-0, 7-1 and 9-2 and False for 4-0, 6-1, 8-2 and (0, 0), and asserts the smallest passing b for each c from 0 to 6 is 5, 7, 9, 10, 12, 13 and 15, and agrees with a reference loop for every b and c up to 30 (requirement T-12 and T-15).
- Tests cover Noul exactly at 0.3 and 0.7 and just either side of each, under every operator choice, and a refusal when an operator is `UNSET` (T-05).
- Tests cover `right` for a typed label, an `ambiguous` label and a `none-fit` label with an unset answer (T-07), and odd and even median counts, the nearest-rank 90th percentile, a timeout counted at 10 seconds in the slowest and left out of the median under `answered_only` (T-08).
- `scorer.py` contains no floating-point comparison at the 0.05 line.

## Task 4: Build the scoring pipeline, verdict and report

Depends on: Task 3

Extend `.dev/research/jev-vs-keyword-table-611/harness/scorer.py` and create `.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py`. Add `score(corpus, table_answers, jev_rows, rule, run_meta) -> dict`, `verdict(result, rule, run_meta) -> (state, reason)` and `render_report(result) -> str`, plus a command line `score` that reads the experiment folder and writes `runs/<run-id>/report.md` and a decision record input. The result holds: per-arm correct count, accuracy over every frozen prompt (an error counts as not right and stays in the denominator), abstentions by reason, error counts; the paired breakdown (both right, only Jev, only table, neither); accuracy split into typed prompts and `ambiguous` or `none-fit` prompts, with a flag when a margin-test pass rests only on the second group; accuracy with and without prompts marked `seen_by_table`; the full disagreement list (prompt id, label, both answers, Jev probabilities, Noul value); cost; and the latency statistics from Task 3. `verdict` returns `JEV_BEATS_TABLE`, `NOT_CLEARLY` or `RUN_INVALID` with a reason as the Constraints say, and `RUN_INVALID` reasons include: a frozen file or the table answers changed after hashing, a stop at the cap before all prompts, a rejected key, a returned model id other than `jev-1.14.0`, unresolved failures above `unresolved_failure_invalid_count`, a missing gate result, and missing table provenance. `render_report` is deterministic: the same inputs give identical bytes. A rescore under a second rule file writes a new report labelled non-decisional and never changes the original files or verdict.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py -v` passes.
- Tests check each verdict state is reached from synthetic inputs, with boundary cases on both sides of the margin test and the latency limits using stand-in rule values (T-12), and each `RUN_INVALID` reason (T-13).
- Tests check the paired breakdown and disagreement list against hand-built rows (T-11), the typed versus `ambiguous` or `none-fit` split and the flag, and a twice-failed prompt scored not right and kept in the denominator (T-06).
- A test shows two calls to `render_report` give byte-identical output and a rescore leaves the original report file unchanged (T-14).
- No stand-in value from a test appears in `decision-rule.md`.

## Phase 3: Gates and audit trail

## Task 5: Build the event log, the manifest and the two gates

Depends on: Task 2, Task 4

Create `.dev/research/jev-vs-keyword-table-611/harness/events.py`, `.dev/research/jev-vs-keyword-table-611/harness/gate.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py`.

`events.py` appends one JSON line per event to `events.jsonl` (sorted keys, a UTC timestamp, the event name, an evidence path and the evidence file's SHA-256). Events: `owner_input_received`, `freeze`, `rule_freeze`, `gate1`, `gate2`, `tests_passed` (with the command and the number of tests), `lead_go` (with the rule file's SHA-256 and the lead's words), `first_request`, `run_end`, `scoring`, `verdict`. Its command line has `record-tests` and `record-go`. It never rewrites or deletes a line.

`gate.py` writes and checks `manifest.json` (SHA-256 of the corpus, `questions.py`, the rule file, the table answers, `harness/scorer.py`, `harness/runner.py`, `harness/loader.py`, `harness/gate.py`, `harness/events.py`, and the `jevlib` files under `.dev/research/346-review-loop-experiments/p15/jev/jevlib/`, plus the pinned model id). `gate1(paths)` returns the failed checks by name: rule file loads and is `AGREED` with who, when and words, no `UNSET` value, corpus and label hashes match the manifest. `gate2(paths)` adds: table answers present with a recorded procedure and provenance and a matching hash, the scorer, runner and `jevlib` hashes match, a `tests_passed` event whose hashes match the current files, a per-request spend bound that fits the cap, and a `lead_go` event naming the rule file's current SHA-256. Each gate writes its result as an event.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py -v` passes.
- Tests show Gate 1 refuses on `PROPOSED`, `PENDING`, an empty who, when or words, an `UNSET` value, and a missing rule file (T-01), and either gate refuses on any hash mismatch for the corpus, questions, rule, table answers, scorer, runner or `jevlib` (T-02).
- Tests show Gate 2 refuses with no `lead_go` event, a `lead_go` naming an old rule hash, and no `tests_passed` event (T-03).
- A test shows `events.jsonl` lines are append-only and each carries a timestamp, an evidence path and a hash.

## Phase 4: Runner

## Task 6: Build the runner on `JevClient`

Depends on: Task 1, Task 2, Task 5

Create `.dev/research/jev-vs-keyword-table-611/harness/runner.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py`. The runner imports `JevClient`, `Budget`, `Journal`, `UrllibTransport`, `TransportTimeout` and `TransportError` from `jevlib` and the questions from `questions.py`. It sets `jevlib.config.MAX_RETRIES = 0` and `jevlib.config.ATTEMPT_TIMEOUT_S` to the rule's `attempt_timeout_s` inside its own process only (tests restore both with `monkeypatch`). It wraps the transport in a small timing class that records `time.monotonic()` around each `post` and whether it timed out, because `Result.latency_ms` also counts local work.

Per prompt, in corpus order and one at a time: build the state `{"prompt": text}`, call `client.ask(state, build_questions(), case_id=<prompt id>, qset_version=QSET_VERSION, data_classes=["public"], purpose="issue611")`, and on any status other than `ok` make exactly one more call for that prompt (a new logical call id). Every attempt is journaled to `runs/<run-id>/journal.jsonl` and drawn from one cumulative `Budget` at `ledger/spend.json` with `ceiling_usd=1.0` and `ceiling_input_tokens=int(1.0 / PRICE_USD_PER_MTOK_INPUT * 1e6)`. Each prompt writes one row to `runs/<run-id>/jev-rows.jsonl` with the attempts (status, error, measured latency, timed-out flag), final status, the choice and its probabilities, the Noul value and the returned model. `KeyMissing`, `KeyRejected`, a `model_mismatch` error and `BudgetExhausted` stop the run and are recorded as systemic reasons for `RUN_INVALID`. The command line refuses to start unless `--live` is given, `gate1` and `gate2` both pass, and the key is present; it checks the gates before reading any environment variable. With no `--live` it runs the client with `live=False`, which builds, screens and budgets each request and calls no transport. When `--live` is given it copies `TYPESAFE_API_KEY` into `JEV_API_KEY` in memory and prints nothing about the key.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py -v` passes using `MockTransport` and `fake_answer` only.
- Tests show a failed first attempt gets exactly one rerun, both attempts appear in the journal and the ledger, and a prompt that fails twice is recorded as `error` (T-06); the client never retries by itself (the mock sees exactly two posts for a twice-failed prompt).
- Tests show the cost guard stops before a request whose estimate would pass the ceiling, and that spend carries across two run ids through the one ledger (T-09).
- Tests show a rejected key (HTTP 401), a returned model id other than `jev-1.14.0` and a spent ledger each stop the run with a systemic reason (T-13), and that the gates are checked before any environment read (the stubbed environment accessor is never called when a gate fails; T-03).
- A test sets a fake key, runs the runner against a mock whose error text contains that key, then runs `keyscan.py --fake <value>` on the run folder with explicit paths and sees `KEYSCAN OK` and no occurrence of the value in any written file (T-10).
- `runner.py` contains no reference to a real endpoint other than `jevlib.config.api_url()`.

## Phase 5: Procedures for the steps that need a person

## Task 7: Write the table procedure and the corpus and provenance templates

Depends on: Task 2

Create `.dev/research/jev-vs-keyword-table-611/table/table-procedure.md`, `.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`, `.dev/research/jev-vs-keyword-table-611/corpus/selection-criteria.md` and `.dev/research/jev-vs-keyword-table-611/corpus/labelling-record.md`.

`table-procedure.md` states how the Wave 0 table in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` lines 152 to 159 is applied as written: the six cue rows quoted from those lines, "no cue matched" gives an unset answer, cues from two or more rows give an unset answer, "leak" stays in both performance and security, no first-match parser and no extra inference. It requires the applier to receive prompts only, never the labels or any Jev answer, to be a different person or session from the labeller, to record per prompt the cues and rows matched, and to store all answers before any Jev call and only after Gate 1 passes. It defines the `table-answers.jsonl` row (`prompt_id`, `answer` or null, `cues`, `rows`, `method`). `table-provenance.md` is a form to fill: method (a person reading the prose, or executing the skill), the source revision (the commit and the blob of the table file at the time), who applied it, the date, and, for a skill execution, evidence of which copy ran (the lesson recorded in `docs/memory/reflect/deviation-patterns-issue-610.md`). `selection-criteria.md` is a form for the public sources listed before any arm runs, the counts per label, any shortfall reported rather than padded, and the rule that a prompt the privacy screen would refuse is replaced, never edited. `labelling-record.md` is a form for the named labeller, the date, the labelling instructions, and the basis for each label, with the rule that the basis for an `ambiguous` or `none-fit` label is written before any arm runs and is not taken from the table's own two-row rule.

Acceptance criteria:
- Each of the four files exists, states at its top that it is a form or procedure to be completed by a person or session and is not evidence, and has no filled-in prompt, label or answer.
- `table-procedure.md` quotes the six cue rows exactly as they stand in `SKILL.md` lines 152 to 159 (checked by comparing the quoted text to those lines).
- `table-procedure.md` names `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl` and its row fields, and states the Gate 1 ordering and the prompts-only rule.
- The files contain no real prompt text and no key.

## Phase 6: Hand-off documentation

## Task 8: Write the README and the decision-record template

Depends on: Task 5, Task 6, Task 7

Create `.dev/research/jev-vs-keyword-table-611/README.md` and `.dev/research/jev-vs-keyword-table-611/decision-record.md` (a template).

`README.md` explains: what the experiment decides and what it does not; the folder layout of the design (one job per file); the offline test command; the order of work (rule AGREED, corpus and labels frozen, Gate 1, table answers, harness tests recorded with `events.py record-tests`, lead's go recorded with `events.py record-go`, Gate 2, the coordinator's live run, `keyscan.py` with explicit paths and the real key sourced inside one subshell command only as rule J2 describes, scoring, decision record); the open items (Noul band operators, the failure count, who labels, who applies the table, the live route through the vendor URL or the gateway because the ops guide `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md` says the vendor key is held by the gateway, the price to re-confirm before Gate 2); and the rule that an implementer session never calls the live API. `decision-record.md` is a template listing the verdict, the rule file's hash, the report path, the exact text to post on issues 611, 609 and 612, and the posted text and links to be added by the coordinator afterwards; it states that `RUN_INVALID` leaves issue 612 undecided.

Acceptance criteria:
- `README.md` contains the exact test command `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v` and the live-run steps in the order above, and names each command line (`gate.py`, `runner.py`, `events.py`, `scorer.py`) with its subcommands as built in Tasks 4 to 6.
- `README.md` names every open item above and says which person or session answers each.
- `decision-record.md` has fields for the verdict states `JEV_BEATS_TABLE`, `NOT_CLEARLY` and `RUN_INVALID` and states that the build and close decision on issue 612 is made only from a valid run.
- Running the full test command from the repository root passes with all tests from Tasks 1 to 6, and `git status --short` shows changes only under `.dev/research/jev-vs-keyword-table-611/` and the package folder.
