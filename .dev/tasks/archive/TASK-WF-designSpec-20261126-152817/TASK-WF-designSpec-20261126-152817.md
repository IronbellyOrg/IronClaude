---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-designSpec-20261126-152817
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Build the offline harness for the Jev versus keyword table experiment (issue 611)

Source: ./source.md
Goal: A tested, offline measurement harness for the Jev versus keyword table comparison exists under `.dev/research/jev-vs-keyword-table-611/`, with the agreed decision rule recorded in its rule file and the gates that keep every live call closed until a person has frozen the corpus, the table answers and the rule, confirmed the price and given a go. No prompt is sent anywhere while building it. This plan is the rebuild after the pre-execution review; the decisions of "Revision 1" in `./source.md` bind it and win over sections 3 to 8 of the design where they differ.

## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, set a fake key with `monkeypatch.setenv`, and use a temporary experiment root for every file the gates, events, runner and scorer write. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need. The pull request that delivers this plan says `Refs #611` and lists parts B to E of section 8 of the design as left (Task 8 puts that sentence in the README).
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only, and only from its submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid. Gate 1 accepts `UNSET` and does not freeze the rule file's hash. The scorer, the `freeze-rule` command and Gate 2 refuse any `UNSET` value, and `freeze-rule` is the step that freezes the rule file's hash after the owner has filled the fields.
- The real client behaves differently from a mock-backed dry run: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. So the runner has two subcommands: `run` needs `--live`, both gates and the key; `rehearse` never posts and needs no gate and no key. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.

## Phase 1: Foundation

## Task 1: Record the baseline, create the test setup and the single question file

First, before creating any other file, run `git status --short` and save its output to `./artifacts/baseline-status.txt` in the package. Then create `.dev/research/jev-vs-keyword-table-611/questions.py`, `.dev/research/jev-vs-keyword-table-611/harness/__init__.py` (empty), `.dev/research/jev-vs-keyword-table-611/harness/tests/conftest.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py`.

`questions.py` is the only place Jev question wording lives. It imports `choice` and `noul` from `jevlib.questions` and exposes `QSET_VERSION`, `TYPES = ("bug", "build", "performance", "deployment", "security", "test")` and `build_questions() -> dict` returning two questions: `problem_type`, a `choice` over the six types with a one-sentence plain definition per option (no positional option names such as `a` or `option1`), and `any_type_fits`, a `noul` asking whether any of the six types fits the problem in `state["prompt"]`, with `true` and `false` criteria. No corpus prompt, label or corpus-derived example appears in the file, and it does not copy the table's cue phrases (the table is `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` lines 153 to 158).

`conftest.py` inserts `.dev/research/346-review-loop-experiments/p15/jev` and the experiment folder into `sys.path` (the same pattern as `p15/jev/tests/conftest.py`). It provides an autouse fixture that fails any test that calls `socket.socket.connect`, a fixture that sets a fake `JEV_API_KEY` with `monkeypatch.setenv`, and an autouse fixture that records the existence, size and modification time of the real experiment folder's `events.jsonl`, `manifest.json`, `ledger/spend.json` and `runs/` before each test and fails the test if any of them changed. The real folder is found from the conftest's own location, so this fixture needs no other module.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py -v` passes.
- `test_questions.py` shows that `jevlib.questions.build_request({"prompt": "x"}, build_questions())` succeeds, the choice has exactly the six type names, the noul has `true` and `false` criteria, and `request_sha256` is identical across two calls.
- A test shows the socket guard fails a test that tries to connect, and a test shows the real-state snapshot helper reports a change when a file in a temporary folder is edited.
- A test asserts that none of these cue phrases appears, ignoring case, in the text of `questions.py`: stack trace, NameError, undefined, tsc, compiled, lint, slow, latency, p99, too long to load, takes forever, hangs, container, env var, service won't start, CVE, vulnerab, pytest, jest, flake, intermittent, passing locally. The test names the words it exempts because they are type names or ordinary English: build, make, deploy, production, memory, leak, auth, token, exposed, null.
- `./artifacts/baseline-status.txt` exists and does not list `.dev/research/jev-vs-keyword-table-611`.

## Task 2: Write the rule file and the loader

Depends on: Task 1

Create `.dev/research/jev-vs-keyword-table-611/decision-rule.md`, `.dev/research/jev-vs-keyword-table-611/harness/loader.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py`.

`decision-rule.md` starts with a front-matter block of plain `key: value` lines (stdlib parser, no nesting) holding: `status: AGREED`, `agreed_by`, `agreed_at: 2026-11-26`, `relayed_owner_words`, `alpha_inverse: 20`, `median_limit_s: 2`, `slowest_limit_s: 5`, `attempt_timeout_s: 10`, `median_population: answered_only`, `rerun_policy: one_per_prompt`, `p90_method: nearest_rank`, `spend_cap_usd: 1.0`, `noul_low: 0.3`, `noul_high: 0.7`, `noul_low_operator: UNSET`, `noul_high_operator: UNSET` and `unresolved_failure_invalid_count: UNSET`. The valid operators are `lt` or `le` for the low edge and `gt` or `ge` for the high edge. Its body holds a section `## Agreement text (verbatim)` with the IronFlow reply of 2026-11-26 word for word as in the Constraints above, and a section `## Rule in words` restating the agreed rule from the Constraints.

`loader.py` provides:
- `Paths(root=None)`: every file location of the experiment from one root, which defaults to the experiment folder found from the module's own location. It gives `corpus`, `selection_criteria`, `labelling_record`, `questions_py`, `rule`, `table_answers`, `table_provenance`, `manifest`, `events`, `ledger`, `runs`, `report`, `decision_record` and `rescores`, plus `jevlib_dir` (the existing `jevlib` folder by default, overridable for tests), `code_files()` (`questions.py` and the `harness` modules `loader`, `spend`, `gate`, `events`, `scorer` and `runner`) and `jevlib_files()` (the `.py` files directly inside `jevlib_dir`, sorted by name, never a folder walk, so `__pycache__` is never hashed).
- `sha256_file(path)`, the only SHA-256 helper in the experiment.
- `load_rule(path, for_scoring=False)`: refuses when a required key is missing, when `status` is not `AGREED`, when `agreed_by`, `agreed_at` or the verbatim agreement text is empty, and, when `for_scoring` is true, when any value is `UNSET`. Without `for_scoring` an `UNSET` value loads as the string `UNSET`.
- `load_corpus(path)` and `load_table_answers(path)` (JSON lines). A corpus row has `id`, `text`, `source`, `retrieved_on`, `selection_reason`, `label` (one of the six types, `ambiguous` or `none-fit`), `label_basis`, `labeller`, `labelled_on` and `seen_by_table`. `load_corpus` rejects a missing public `source`, a duplicate `id`, the same `text` under two ids, a label outside the allowed set, a missing type among the six, no `ambiguous` row and no `none-fit` row, and runs `jevlib.manifest.privacy_violation` on each prompt with data class `public`, failing with the reason string and the prompt id (never the matched text).

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py -v` passes (requirement T-04 and the rule-file refusals of T-01).
- Tests show `load_rule` refuses `PROPOSED`, `PENDING`, an empty agreement text and a missing key, loads the file as committed with `UNSET` for exactly the three open fields, and refuses with `for_scoring=True` while an `UNSET` value remains.
- Tests show `load_corpus` rejects each case listed above, including a prompt containing a GitHub URL and one containing a home-directory path (the cases `jevlib.manifest.privacy_violation` refuses).
- Tests show `Paths` built on a temporary root gives only paths under that root (except `jevlib_dir`), and `jevlib_files()` lists only top-level `.py` names and omits a `__pycache__` folder.
- `decision-rule.md` as committed contains the verbatim IronFlow agreement text and the relayed owner words marked as relayed.

## Phase 2: Pure functions, events and gates

## Task 3: Build the pure scoring functions

Depends on: Task 2

Create `.dev/research/jev-vs-keyword-table-611/harness/scorer.py` (first part) and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py`. Functions, all pure and stdlib only:
- `right(label, answer) -> bool`; answer `None` means unset.
- `sign_test_passes(b, c) -> bool` using `math.comb` and the integer test `20 * tail < 2 ** n` with `n = b + c` and `tail = sum(comb(n, k) for k in range(b, n + 1))`, reading the factor 20 from the rule's `alpha_inverse`.
- `jev_answer(noul_p, choice, rule) -> (answer, reason)`. Here `noul_p` is the Noul value for `any_type_fits` (a high value means a type fits) and `choice` is the validated answer of `problem_type`. If `noul_p` is below the low edge by the low operator (`lt` means strictly below `noul_low`, `le` means at or below), the answer is `None` with reason `none-fit`. Else if `noul_p` is above the high edge by the high operator (`gt` strictly above `noul_high`, `ge` at or above), the answer is `choice`. Otherwise the answer is `None` with reason `not-settled`. It refuses when an operator is `UNSET` or not valid for its edge.
- `median(values)` (even count: mean of the two middle values; empty list: `None`), `percentile_nearest_rank(values, 0.9)` (index `ceil(0.9 * n) - 1` of the sorted list; empty list: `None`) and `latency_stats(attempts, rule)` returning the median over the population `median_population` says, the slowest over all attempts with a timeout counted at `attempt_timeout_s`, and the 90th percentile; each is `None` when no attempt qualifies.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py -v` passes.
- A test asserts `sign_test_passes` is True for 5-0, 7-1 and 9-2 and False for 4-0, 6-1, 8-2 and (0, 0), and asserts the smallest passing b for each c from 0 to 6 is 5, 7, 9, 10, 12, 13 and 15, and agrees with a reference loop for every b and c up to 30 (requirement T-12 and T-15).
- Tests give `jev_answer` these expected values for the four operator pairs (`lt` or `le` with `gt` or `ge`): a value just below 0.3 gives `none-fit`; exactly 0.3 gives `none-fit` under `le` and `not-settled` under `lt`; a value between the edges gives `not-settled`; exactly 0.7 gives the choice under `ge` and `not-settled` under `gt`; a value just above 0.7 gives the choice. A test shows the refusal for an `UNSET` operator and for `gt` on the low edge (T-05).
- Tests cover `right` for a typed label, an `ambiguous` label and a `none-fit` label with an unset answer (T-07), odd and even median counts, the nearest-rank 90th percentile, a timeout counted at 10 seconds in the slowest and left out of the median under `answered_only` (T-08), and `None` results for empty input.
- `scorer.py` contains no floating-point comparison at the 0.05 line.

## Task 4: Build the spend estimates, the event log and the gates

Depends on: Task 2

Create `.dev/research/jev-vs-keyword-table-611/harness/spend.py`, `.dev/research/jev-vs-keyword-table-611/harness/events.py`, `.dev/research/jev-vs-keyword-table-611/harness/gate.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py`, and add to `conftest.py` a fixture `exp(tmp_path)` that builds a `loader.Paths` on a temporary root populated with small synthetic frozen files and a copy of the rule file.

`spend.py` (pure; the only code that estimates spend): `estimate_request_tokens(req)` is `ceil(len(canonical_bytes(req)) / RESERVE_BYTES_PER_TOKEN)`, the formula `JevClient.ask` uses (from `jevlib.questions` and `jevlib.config`); `estimate_run_tokens(requests)` is the sum over every request times 2 for the one allowed rerun; `ceiling_tokens(cap_usd, price_usd_per_mtok)` is `int(cap_usd / price * 1e6)`; `worst_case_usd(tokens, price)`.

`events.py` appends one JSON line per event to the events file of `Paths` (sorted keys, a UTC timestamp, the event name, an evidence path and the evidence file's SHA-256 through `loader.sha256_file`, plus event-specific fields). It never rewrites or deletes a line. Events: `owner_input_received`, `freeze`, `rule_freeze`, `gate1`, `gate2`, `tests_passed`, `price_confirmed`, `lead_go`, `first_request`, `run_end`, `scoring`, `verdict`. It provides `append_event`, `read_events` and `latest`. Its command line has `owner-input --evidence PATH --note TEXT`, `price --usd-per-mtok VALUE --source TEXT` and `go --words TEXT`; `go` records the rule file's current SHA-256 in the `lead_go` event. Every command takes `--root`.

`gate.py` owns the manifest and the gates. Its command line has six subcommands, each taking `--root`:
- `freeze-corpus`: runs `loader.load_corpus` (so the privacy screen runs), refuses on any failure, and writes the manifest keys `corpus`, `selection_criteria`, `labelling_record`, `questions` and `model_pin` (the hashes and `jev-1.14.0`), then a `freeze` event. It refuses when the manifest already holds these keys.
- `gate1`: reads the manifest and checks, returning the failed checks by name: `rule_missing`, `rule_status`, `rule_provenance_empty` (who, when or words empty), `manifest_missing`, `hash_corpus`, `hash_selection_criteria`, `hash_labelling_record`, `hash_questions`. It accepts `UNSET` values and never writes the manifest. It writes a `gate1` event and exits non-zero on a failure.
- `freeze-table`: refuses unless every Gate 1 check passes now and the table answers file and the provenance file exist; writes the manifest keys `table_answers` and `table_provenance` and a `freeze` event.
- `freeze-rule`: loads the rule with `for_scoring=True` (refusing any `UNSET`), writes the manifest key `rule` and a `rule_freeze` event.
- `record-tests`: runs `uv run pytest <harness tests folder> -q` itself, refuses a non-zero exit or a count of zero, and writes a `tests_passed` event holding the command, the count and the SHA-256 of every file in `Paths.code_files()` and `Paths.jevlib_files()`. The function takes the runner of the command as a parameter so tests inject a fake.
- `gate2`: all Gate 1 checks plus `unset_value`, `rule_not_frozen`, `hash_rule`, `table_missing`, `table_provenance_missing`, `hash_table_answers`, `hash_table_provenance`, `tests_not_recorded`, `hash_code` (any code or `jevlib` file differs from the `tests_passed` event), `price_not_confirmed`, `spend_bound`, `go_missing`, `go_rule_hash` (the `lead_go` names a different rule hash than the current one) and `prior_run` (a `first_request` or `run_end` event already exists). `spend_bound` fails when `worst_case_usd` of the whole-run estimate at the confirmed price exceeds the rule's `spend_cap_usd`, or when the whole-run tokens exceed the ledger's remaining allowance. It writes a `gate2` event.

`gate1` and `gate2` hash files only and never call the corpus loader.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py -v` passes, using only the `exp` fixture's temporary root.
- Tests show Gate 1 refuses on `PROPOSED`, `PENDING`, an empty who, when or words, and a missing rule file, accepts a rule file with `UNSET` values, and either gate refuses on a hash mismatch for the corpus, questions, rule, table answers or any `jevlib` or code file (T-01 and T-02).
- Tests show Gate 2 refuses with no `lead_go` event, a `lead_go` naming an old rule hash, no `tests_passed` event, an `UNSET` value, no `rule_freeze`, no `price_confirmed`, and a `first_request` or `run_end` event already in the log (the second-run refusal), and passes on a complete synthetic setup (T-03).
- Tests show `spend_bound` fails when each request fits the ledger but the whole-run total does not, and when the worst-case dollars at a high confirmed price exceed the cap.
- Tests show the manifest bytes are unchanged after `gate1` and `gate2`, a second `freeze-corpus` is refused, `freeze-rule` refuses an `UNSET` value, `record-tests` refuses a failing or empty run (injected), and a test patches `loader.load_corpus` to raise and shows both gates still run.
- A test shows event lines are append-only and each carries a timestamp, an evidence path and a hash, that `go` writes the rule's current hash, and that the three `events.py` subcommands write their events.
- The real `events.jsonl`, `manifest.json` and ledger are unchanged by the test run (the autouse fixture of Task 1).

## Phase 3: Scoring pipeline and runner

## Task 5: Build the scoring pipeline, verdict, report and decision record

Depends on: Task 3, Task 4

Extend `.dev/research/jev-vs-keyword-table-611/harness/scorer.py` and create `.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py`. Add `score(corpus, table_answers, jev_rows, rule, run_meta) -> dict`, `verdict(result, rule, run_meta) -> (state, reason)`, `render_report(result) -> str` and `render_decision_record(result, verdict, paths) -> str`, plus a command line `score --run-id ID [--root PATH]` and `score --run-id ID --rescore NAME --rule PATH`.

The result holds: per-arm correct count, accuracy over every frozen prompt (an error counts as not right and stays in the denominator), abstentions by reason, error counts; the paired breakdown (both right, only Jev, only table, neither); accuracy split into typed prompts and `ambiguous` or `none-fit` prompts, with a flag when a margin-test pass rests only on the second group; accuracy with and without prompts marked `seen_by_table`; the full disagreement list (prompt id, label, both answers, Jev probabilities, Noul value); cost; and the latency statistics from Task 3.

`run_meta` is built by the command from the events, the manifest and the run record, through functions of `events.py` and `gate.py`: whether each frozen file still matches the manifest, whether the `gate1` and `gate2` events exist, whether the table provenance file exists, the systemic stop reason from the `run_end` event, the models returned by `ok` rows, the number of `first_request` events and the count of unresolved failures.

`verdict` returns `JEV_BEATS_TABLE`, `NOT_CLEARLY` or `RUN_INVALID` with a reason as the Constraints say. The `RUN_INVALID` reasons are `frozen_file_changed`, `table_answers_changed`, `stopped_before_all_prompts`, `key_rejected`, `model_mismatch`, `unresolved_failures_above_limit`, `gate_result_missing`, `table_provenance_missing`, `second_live_run` and `no_answered_prompts`.

The command loads the rule with `for_scoring=True` and exits with a refusal, and no verdict, while any value is `UNSET`. It writes `report.md` and `decision-record.md` at the experiment root, for every verdict, and appends `scoring` and `verdict` events; it refuses to overwrite either file. `render_decision_record` lists the verdict, the rule file's hash, the report path, the exact text to post on issues 611, 609 and 612, and an empty section "Posted text and links" for the coordinator to fill; for `RUN_INVALID` it states that issue 612 stays undecided, and it states that the build and close decision on issue 612 is made only from a valid run. `render_report` is deterministic: the same inputs give identical bytes. A rescore under another rule file writes `rescores/NAME/report.md`, labelled non-decisional, appends no event and never changes the root files.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py -v` passes, using a temporary root for every file it writes.
- Tests check each verdict state is reached from synthetic inputs, with boundary cases on both sides of the margin test and both latency limits using stand-in rule values (T-12), and each `RUN_INVALID` reason, including `no_answered_prompts` for a run with no answered prompt (T-13).
- Tests check the paired breakdown and disagreement list against hand-built rows (T-11), the typed versus `ambiguous` or `none-fit` split and its flag, and a twice-failed prompt scored not right and kept in the denominator (T-06).
- A test shows two calls to `render_report` give byte-identical output, a rescore writes only under `rescores/` and leaves the root report unchanged, and a second `score` run refuses to overwrite the root report (T-14).
- A test shows the command exits with a refusal and writes no verdict while the rule has an `UNSET` value, and that the decision record names the three issues, the rule hash and the 612 statement for each of the three verdicts.
- No stand-in value from a test appears in `decision-rule.md`.

## Task 6: Build the runner on `JevClient`

Depends on: Task 1, Task 2, Task 4

Create `.dev/research/jev-vs-keyword-table-611/harness/runner.py` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py`. The runner imports `JevClient`, `KeyMissing` and `KeyRejected` from `jevlib.client`, `Budget` and `BudgetExhausted` from `jevlib.budget`, `Journal` from `jevlib.journal`, `UrllibTransport`, `TransportTimeout` and `TransportError` from `jevlib.transport`, and `jevlib.config` as a module; the questions come from `questions.py`.

A context manager `limits(rule)` sets `config.MAX_RETRIES = 0` and `config.ATTEMPT_TIMEOUT_S` to the rule's `attempt_timeout_s` and restores both in a `finally`. A small timing class wraps the transport and records `time.monotonic()` around each `post` and whether it timed out, because `Result.latency_ms` also counts local work.

A core function `execute(paths, rule, corpus, run_id, transport, price)` runs one live run with the gates already checked by its caller, so tests can call it twice against one temporary ledger. Its steps are, in order:
- Compute the whole-run estimate with `spend.estimate_run_tokens` over the requests built from the frozen prompts, build the `Budget` at the ledger of `Paths` with `ceiling_usd` from the rule's `spend_cap_usd` and `ceiling_input_tokens` from `spend.ceiling_tokens` at the confirmed price, and call `budget.reserve_phase(phase, whole_run_tokens)` with `phase` equal to `issue611-<run_id>`, the same string given to `JevClient`. A `BudgetExhausted` there ends the run before any post with the reason `spend_bound`. The reservation is released with `budget.release_phase(phase)` in a `finally`.
- Append the `first_request` event, then handle prompts in corpus order, one at a time: build the state `{"prompt": text}` and call `client.ask(state, build_questions(), case_id=<prompt id>, qset_version=QSET_VERSION, data_classes=["public"], purpose="issue611")`.
- Stop the run with no rerun, and record the systemic reason, on the exceptions `KeyMissing` and `KeyRejected`, on a result with status `refused` and error `budget_exhausted`, on status `invalid` with error `model_mismatch`, and on status `refused` with error `dry_run`. On any other non-`ok` result make exactly one more `ask` for that prompt (a new logical call id). A second non-`ok` result makes the prompt an `error`. The model-pin check applies only to `ok` results, since every non-`ok` result has `model` of `None`.
- Every attempt is journaled to `runs/<run-id>/journal.jsonl` and drawn from the one cumulative ledger. Each prompt writes one row to `runs/<run-id>/jev-rows.jsonl` with the attempts (status, error, measured latency, timed-out flag), the final status, the choice and its probabilities, the Noul value and the returned model.
- At the end, also after a stop, write `runs/<run-id>/run-record.md` (run id, start and end in UTC, the stop reason or `completed`, the counts of prompts, attempts, `ok` and `error`, the ledger state, the models returned, the confirmed price, the rule's hash, and the SHA-256 of the rows and journal files) and append the `run_end` event. Neither file holds the key.

The command line has two subcommands, each taking `--root`:
- `run --run-id ID --live`: refuses to start (exit 2, nothing read) without `--live` or when `runs/<run-id>` exists. It then checks Gate 1 and Gate 2 and reads no environment variable before both pass. Only then does it read `TYPESAFE_API_KEY`, copy it into `JEV_API_KEY` in memory, load the corpus, read the latest `price_confirmed` event and call `execute`. It prints nothing about the key.
- `rehearse --out DIR`: never posts, needs no gate and no key, and refuses a `DIR` inside the experiment's `ledger/` or `runs/` folders. It runs the client with `live=False` against a throwaway ledger in `DIR`, so every request ends `refused`/`dry_run` before any transport call, and prints the prompt count and the whole-run estimate. It writes nothing to the events file, the real ledger or `runs/`.

Acceptance criteria:
- `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py -v` passes using `MockTransport`, `fake_answer` and a temporary root only.
- Tests show a failed first attempt gets exactly one rerun, both attempts appear in the journal and the ledger, and a prompt that fails twice is recorded as `error` (T-06); the mock sees exactly two posts for a twice-failed prompt, so the client never retries by itself.
- Tests show each systemic signal ends the run with its reason and exactly one post for that prompt: an HTTP 401 (`KeyRejected`), a missing key (`KeyMissing`), a returned model id other than `jev-1.14.0`, and a spent ledger (`refused`/`budget_exhausted`); and a timeout is rerun and is not a stop (T-13).
- Tests show a ledger where every request fits but the whole-run estimate does not gives zero posts, a `run_end` event with reason `spend_bound` and an empty `reserved` map afterwards; that a completed run also leaves `reserved` empty; and that spend carries across two run ids through the one ledger (T-09).
- Tests show a confirmed price higher than the jevlib constant lowers the token ceiling passed to `Budget`.
- Tests show that with an `os.environ` replaced by a recorder, a failing gate leaves `TYPESAFE_API_KEY`, `JEV_API_KEY` and `JEV_API_URL` unread (which also covers the direct read inside `privacy_violation`), and that `run` without `--live` exits 2 before checking any gate (T-03).
- A test shows `limits(rule)` restores `config.MAX_RETRIES` to 1 and `config.ATTEMPT_TIMEOUT_S` to 20.0 on exit, also after an exception.
- A test shows `rehearse` calls a transport that fails on any call zero times, leaves the real events file, ledger and `runs/` unchanged, and refuses a `DIR` under `ledger/`.
- A test sets a fake key, runs `execute` against a mock whose error text contains that key, then runs `keyscan.py --fake <value>` with explicit paths on the run folder, `events.jsonl`, `manifest.json` and the ledger and sees `KEYSCAN OK` and no occurrence of the value in any written file (T-10).
- `run-record.md` exists after a completed run and after a stopped run, and `runner.py` contains no `http://` or `https://` literal (the endpoint comes from `jevlib.config.api_url()`).
- No file under the `jevlib` folder is changed; its 31 importers (the experiments under `p15` and later folders) are untouched.

## Phase 4: Procedures and hand-off

## Task 7: Write the table procedure and the corpus and provenance templates

Depends on: Task 4

Create `.dev/research/jev-vs-keyword-table-611/table/table-procedure.md`, `.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`, `.dev/research/jev-vs-keyword-table-611/corpus/selection-criteria.md` and `.dev/research/jev-vs-keyword-table-611/corpus/labelling-record.md`.

`table-procedure.md` states how the Wave 0 table in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` is applied as written: the six cue rows quoted from lines 153 to 158 and the ambiguity rule of line 159, "no cue matched" gives an unset answer, cues from two or more rows give an unset answer, "leak" stays in both performance and security, no first-match parser and no extra inference. It requires the applier to receive prompts only, never the labels or any Jev answer, to be a different person or session from the labeller, to record per prompt the cues and rows matched, and to store all answers before any Jev call and only after `gate.py gate1` passes. It defines the `table-answers.jsonl` row (`prompt_id`, `answer` or null, `cues`, `rows`, `method`) and ends with the command `gate.py freeze-table`. `table-provenance.md` is a form to fill: method (a person reading the prose, or executing the skill), the source revision (the commit and the blob of the table file at the time), who applied it, the date, and, for a skill execution, evidence of which copy ran (the lesson recorded in `docs/memory/reflect/deviation-patterns-issue-610.md`). `selection-criteria.md` is a form for the public sources listed before any arm runs, the counts per label, any shortfall reported rather than padded, and the rule that a prompt the privacy screen would refuse is replaced, never edited. `labelling-record.md` is a form for the named labeller, the date, the labelling instructions, and the basis for each label, with the rule that the basis for an `ambiguous` or `none-fit` label is written before any arm runs and is not taken from the table's own two-row rule.

Acceptance criteria:
- Each of the four files exists, states at its top that it is a form or procedure to be completed by a person or session and is not evidence, and has no filled-in prompt, label or answer.
- `table-procedure.md` quotes the six cue rows exactly as they stand in lines 153 to 158 of `SKILL.md` and the ambiguity rule of line 159 (checked by comparing the quoted text to those lines).
- `table-procedure.md` names `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl` and its row fields, states the Gate 1 ordering and the prompts-only rule, and names `gate.py gate1` and `gate.py freeze-table`.
- The files contain no real prompt text and no key.

## Task 8: Write the README

Depends on: Task 5, Task 6, Task 7

Create `.dev/research/jev-vs-keyword-table-611/README.md` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py`.

`README.md` explains:
- what the experiment decides and what it does not;
- the folder layout of the design (one job per file, including `spend.py`);
- the offline test command;
- the order of work, with the command of each step: rule AGREED, corpus and labels frozen with `gate.py freeze-corpus`, `gate.py gate1`, the table answers and `gate.py freeze-table`, the owner's answers to the open rule fields recorded with `events.py owner-input`, `gate.py freeze-rule`, the re-confirmed price recorded with `events.py price`, the harness tests recorded with `gate.py record-tests`, the lead's go recorded with `events.py go`, `gate.py gate2`, `runner.py rehearse`, the coordinator's live `runner.py run --live` with `keyscan.py` run with explicit paths and the real key sourced inside one subshell command only as rule J2 describes, and `scorer.py score`;
- how to rescore: `scorer.py score --run-id ID --rescore NAME --rule PATH` writes only under `rescores/NAME/`, is labelled non-decisional and never changes the root report, the decision record or an event;
- the open items and who answers each: the Noul band operators, the unresolved-failure count, who labels, who applies the table, the live route through the vendor URL or the gateway (the ops guide `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md` says the vendor key is held by the gateway), the price to re-confirm before Gate 2, and where the prompts come from;
- a "Delivery status" section listing parts A to E of section 8 of the design, who does each and whether it is done, and the sentence the pull request must carry: `Refs #611`, with parts B to E listed as left;
- the rule that an implementer session never calls the live API.

`test_readme.py` reads the subcommand names from the argument parsers of `gate.py`, `events.py`, `runner.py` and `scorer.py` and checks that each appears in the README next to its script name.

Acceptance criteria:
- `README.md` contains the exact test command `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v` and the live-run steps in the order above, and `test_readme.py` passes, showing every subcommand of the four command lines is named in the README.
- `README.md` has a "how to rescore" section, a "Delivery status" section with the `Refs #611` sentence and the list of parts B to E, and names every open item above with the person or session that answers it.
- Running the full test command from the repository root passes with all tests from Tasks 1 to 8.
- `git status --short` with every entry under `.dev/research/jev-vs-keyword-table-611/` removed equals `./artifacts/baseline-status.txt`, and no path under `src/`, `tests/`, `.claude/` or `.dev/research/346-review-loop-experiments/` appears in `git status --short`.
