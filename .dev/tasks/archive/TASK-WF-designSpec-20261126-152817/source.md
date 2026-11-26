# Design: Jev versus the keyword table experiment (issue 611)

Grounding: index_state: fresh (codegraph_status, checked_at 2026-11-26T14:41:18Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/issue-611, 0 changes since index). The tools used were `codegraph_status` only. The code this design builds on is under `.dev/research/`, so it was read directly with Read and Glob/Grep (the floor); no graph row is cited.

Type: architecture. Format: spec. Source requirements: `.dev/brainstorms/20261126-jev-vs-keyword-table-611/merged-requirements.md` (status partial). Story summary: `.dev/issues/611/issue-summary.md`.

**Update, 2026-11-26 after the requirements were written:** the decision rule that `merged-requirements.md` calls PROPOSED is now AGREED (the IronFlow session and the build agent, relayed by the lead; see "Agreement received" in `.dev/issues/611/issue-summary.md`). Where this design and `merged-requirements.md` differ on the rule's status or on the median population, this design and the issue summary win. The agreement does not open the live run: the gates in section 5 still apply.

## 1. What this designs

A small, offline-testable measurement harness and a frozen on-disk record for one experiment: does Jev (TypeSafe `jev-1.14.0`) beat the Wave 0 keyword table of `/sc:troubleshoot` at choosing one of six problem types on about 30 labelled public prompts. Nothing under `src/` changes. Nothing here sends a prompt anywhere; the design separates building the harness (offline, mock transport) from running it live (a coordinator action behind two gates).

## 2. Findings that shape the design (read from the repository)

| # | Finding | Source | Effect on the design |
|---|---|---|---|
| F1 | A stdlib-only Jev client already exists: `JevClient.ask(state, questions, case_id, qset_version, data_classes, purpose)`, `Budget` (locked spend ledger with reservations), `Journal` (never writes headers, redacts the key), `validate_response` (pins `jev-1.14.0`, checks answers and probabilities), `MockTransport`, `privacy_violation`, and `keyscan.py` | `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` | Reuse by import. Write no new client. |
| F2 | Binding rule J2 of that work: implementer sessions never hold the key or call the live API; a coordinator-run script loads the key inside one subshell command only, and `keyscan.py` runs after every live run | `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` lines 145 to 165 | Build and test offline; the live run is a coordinator step. This work follows J2. |
| F3 | The client retries once by itself (`MAX_RETRIES = 1`, 2 s backoff, 20 s attempt timeout) | `jevlib/config.py` lines 15 to 18; `client.py` lines 191 to 203 | The experiment's rule is one logged rerun per prompt counted against the cap. The runner sets `MAX_RETRIES = 0` and `ATTEMPT_TIMEOUT_S = 10.0` in its own process (the client reads these as `config` attributes at call time) and does the single rerun itself. |
| F4 | The client reads the key from `JEV_API_KEY`, not `TYPESAFE_API_KEY` | `jevlib/config.py` line 9 | The decision names `TYPESAFE_API_KEY`. The runner copies it into `JEV_API_KEY` inside its own process only, never printed or written. Whether the live route is the vendor URL (default) or the gateway (`JEV_API_URL`) is an open question; the ops guide says workspaces may reach only the gateway. |
| F5 | `privacy_violation` refuses a request containing an email, `/home/`, a GitHub URL, the owner or upstream organisation names, a token shape or the key | `jevlib/manifest.py` lines 12 to 38 | Public prompts are screened offline at corpus freeze with the same function. A prompt that would be refused is replaced before freezing, never edited. A `refused` result at run time is an error. |
| F6 | Observed Jev cost and latency in the earlier probe: about 0.00005 dollars and 160 to 380 ms per call; price 0.042 dollars per million input tokens | `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md` line 54 | 30 prompts cost well under 1 cent. The 1 dollar cap will not bind; its job is to stop a runaway. The proposed 2 s and 5 s limits sit far above the probe, but the probe is not this experiment's evidence. |
| F7 | Experiments live under `.dev/research/` | `.dev/README.md` lines 23 and 38 | Folder: `.dev/research/jev-vs-keyword-table-611/`. |
| F8 | The repository's pytest `testpaths` is `tests`; tests under `.dev/` are not collected by a plain `pytest` | `pyproject.toml` lines 107 to 108 | The gate records the explicit command and its passing result. |

Discrepancy to surface: the ops guide says the vendor key is held only by the gateway, while the decision says to use the `TYPESAFE_API_KEY` key. If that key is not present in the coordinator's shell, the live step cannot run; that is a blocker for the coordinator, not for the build.

## 3. Folder layout (one job per file)

`.dev/research/jev-vs-keyword-table-611/`

| Path | Job |
|---|---|
| `README.md` | What this is, how to run the offline tests, how the coordinator runs the live step, how to rescore |
| `corpus/selection-criteria.md`, `corpus/labelling-record.md`, `corpus/corpus.jsonl` | Public sources and selection criteria; labeller, date and basis for each label; the frozen prompts with provenance and labels |
| `questions.py` | The only copy of Jev question wording, built with `jevlib.questions.choice` and `noul` |
| `decision-rule.md` | Rule file: status, who agreed and when, verbatim owner words, and every policy value (no defaults) |
| `table/table-procedure.md`, `table/table-provenance.md`, `table/table-answers.jsonl` | How "no cue" and "two rows" resolve; method and revision; one answer per prompt with cues matched |
| `harness/loader.py`, `gate.py`, `scorer.py`, `runner.py`, `events.py` | Small modules, each one job (section 5) |
| `harness/tests/` | Offline tests with a mock transport and a socket guard |
| `ledger/spend.json` | One cumulative spend ledger (the `Budget` file) across all run ids |
| `runs/<run-id>/jev-rows.jsonl`, `journal.jsonl`, `run-record.md` | Append-only per run |
| `events.jsonl`, `manifest.json` | Dated event log; hashes and pins |
| `report.md`, `decision-record.md` | Produced by the scorer after a valid run |

## 4. Data flow

```
corpus selection --(privacy_violation screen)--> corpus.jsonl --label (human, blind to arms)--> labels frozen
        |                                                                          |
        v                                                                          v
   Gate 1 (rule AGREED, hashes, verbatim words)  -------------------------------> manifest.json
        |
        +--> table applier (prompts only, never labels) --> table-answers.jsonl --hash--> manifest
        |
   Gate 2 (table hashed, scorer+runner+jevlib hashes, tests passed, spend bound, lead's go)
        |
        v
   runner --(JevClient, MAX_RETRIES=0, 10 s)--> Jev            (coordinator-run subshell, key in memory only)
        |           \--> journal.jsonl, ledger/spend.json, events.jsonl
        v
   jev-rows.jsonl --> scorer(rows, table-answers, corpus, decision-rule) --> report.md + verdict
                                                              keyscan after the run
```

## 5. Components

**loader.py.** Reads the frozen files, computes SHA-256 per file, and returns typed rows. It owns hashing so no other module hashes. It refuses a corpus row without a public source, a duplicate id, or duplicate prompt text under two ids.

**decision-rule.md fields (no defaults anywhere).** `status` (`PROPOSED` | `AGREED`), `agreed_by`, `agreed_words`, `agreed_at`; the margin test (`sign_test`, alpha 0.05, one-sided); `noul_band` with operators at 0.3 and 0.7; `unresolved_failure_invalid_count`; `median_population` (`answered_only` | `include_timeouts_at_cap`); `median_limit_s`, `slowest_limit_s`, `attempt_timeout_s`; `rerun_policy` (one per prompt). The scorer refuses a rule file with a missing field or a status other than `AGREED`. Initial content is the agreed rule of 2026-11-26 (sign test; median 2 s or less; slowest 5 s or less; 10 s timeout; one rerun per prompt; `median_population: answered_only`), with `status: AGREED`, `agreed_by: the IronFlow session and the build agent`, the verbatim agreement text, and Clay's relayed words ("you and the agent debate whats correct way to handle this and do it") recorded as relayed, not typed by Clay. The fields the agreement left open (`noul_band` operators, `unresolved_failure_invalid_count`) are written with the marker `UNSET`, and the scorer refuses to run while any field is `UNSET`.

**gate.py.** `gate1(paths) -> GateResult` and `gate2(paths) -> GateResult`, each returning the failed checks by name. Gate 1: rule file present, status `AGREED`, who and when and words non-empty, labels and corpus hashes match the manifest. Gate 2: table answers present and hashed, scorer, runner and the jevlib files hashed and matching, the recorded test run passing, a verified per-request spend bound, and a go from the lead recorded in `events.jsonl` that names the rule file's hash. A gate result is written to `events.jsonl`. The runner calls Gate 1 and Gate 2 before reading any environment variable.

**scorer.py.**
- `right(label, answer)`: a typed label is right when the answer equals it; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms.
- `sign_test_passes(b, c)`: `n = b + c`; `tail = sum(comb(n, k) for k in range(b, n + 1))`; pass when `20 * tail < 2 ** n`. Integer arithmetic only. Checked cases: 5-0 pass, 4-0 fail, 7-1 pass, 6-1 fail, 8-2 fail, 9-2 pass, b+c = 0 not clearly.
- `jev_answer(row, rule)`: from the Noul probability and the band operators in the rule file gives a type, `unset:none-fit` or `unset:not-settled`.
- Latency: per attempt time from send to full response; median over the population `median_population` says; slowest over all attempts with a timeout counted at its value; 90th percentile by nearest rank (`sorted[ceil(0.9 n) - 1]`); even-count median is the mean of the two middle values.
- `verdict(...)`: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold; `NOT_CLEARLY` for a valid run that does not; `RUN_INVALID` with a reason otherwise (changed frozen file or table answers, spend stop before all prompts, key rejected, returned model id other than the pin, unresolved failures above the rule file's count, missing gate result, missing table provenance). `RUN_INVALID` makes no build or close decision on issue 612.
- Outputs: paired breakdown (both right, only Jev, only table, neither), typed versus ambiguous or none-fit accuracy, seen-by-table split, disagreement list, abstentions by reason, error counts. Deterministic: same rows, same bytes.

**runner.py.** Per prompt: build one request (Choice question over the six types plus a Noul question "does any type fit"), call `JevClient.ask` with `data_classes=["public"]`, and on a status other than `ok` do exactly one rerun with a new logical call id. Both attempts are journaled and charged to the ledger. A twice-failed prompt is recorded as `error` and scored not right for Jev. `KeyMissing` and `KeyRejected` stop the run as `RUN_INVALID`; a `model_mismatch` result is also systemic. It wraps the transport to time each post with the monotonic clock. It refuses to start without `--live`, both gate results and the key in the environment; with no `--live` it is a dry run against the mock transport. It runs prompts one at a time, so the per-request spend bound is checked before each request and the whole-run estimate before the first.

**events.py.** Append-only `events.jsonl` writer: owner input received, freeze, rule freeze, each gate result, first request, run end, scoring, verdict, each linked to its evidence file and hash.

## 6. Cost arithmetic

At 0.042 dollars per million input tokens, 1 dollar is about 23.8 million input tokens. A request is the prompt plus fixed question wording, assumed well under 2,000 tokens; 30 prompts with a rerun for each would be at most 120,000 tokens, about 0.005 dollars. These are estimates; the ledger records actual usage from each response. The price is the figure observed on the vendor models page on 2026-11-10 and must be re-confirmed by the coordinator before Gate 2.

## 7. Test design (offline; mock transport; socket guard)

Run command, recorded in the gate: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. A `conftest.py` inserts the p15 `jev` folder in `sys.path` (the same pattern as `p15/jev/tests/conftest.py`) and installs a guard that fails a test on any socket connection. Each test cites its requirement: gates refuse on PROPOSED, PENDING, missing words or hash mismatch (T-01 to T-03); corpus checks and privacy screen (T-04); band boundaries at 0.3 and 0.7 (T-05); failure kinds, rerun and twice-failed scoring (T-06); right and typed-versus-ambiguous accuracy (T-07); latency statistics (T-08); cost guard and ledger carry-over (T-09); key never in any artifact, with `keyscan.py --fake` (T-10); paired breakdown (T-11); verdict branches and the sign-test integer cases (T-12, T-15); invalid reasons (T-13); determinism and non-decisional rescore (T-14).

## 8. Delivery split (what a plan can finish and what waits for a person)

| Part | Who | Can finish in the build? |
|---|---|---|
| A. Harness: loader, gate, scorer, runner, events, tests, the rule file with the AGREED rule, README | Implementer, offline | Yes |
| B. Corpus and labels: about 30 public prompts, provenance, human labels, label basis, freeze | A named human labeller (an AI session may collect candidates and run the privacy screen) | No, waits for a person |
| C. Table answers | A separate session or person given prompts only | After Gate 1 (rule AGREED), so no |
| D. Live run, keyscan, scoring, report | Coordinator, after Gate 2 and the lead's go | No |
| E. Issue updates on 611, 609, 612 | Coordinator | No |

So the story's pull request can deliver part A and the templates; it must say `Refs #611` and list B to E as left, unless the lead supplies the labeller and the numbers are AGREED.

## 9. Alternatives considered

| Choice | Chosen | Rejected | Why |
|---|---|---|---|
| Client | Import `jevlib` | Write a new client | Tested, stdlib-only, pins the model, journals without headers, has a budget ledger |
| Retries | Runner-level single rerun, client retries off | Keep the client's own retry | Two retry layers would hide attempts and break the cap accounting |
| Verdict names | `JEV_BEATS_TABLE`, `NOT_CLEARLY`, `RUN_INVALID` | Two states | An invalid run must not close issue 612 |
| Policy values | Rule-file fields with no defaults | Constants in code | The owner or delegate sets them; the scorer must not invent them |
| Folder | `.dev/research/jev-vs-keyword-table-611/` | `.dev/experiments/` | The README lists `research/` and not `experiments/` |

## 10. Open items (need an answer, none invented here)

1. RESOLVED 2026-11-26: margin and latency are AGREED (sign test; median 2 s or less; slowest 5 s or less; 10 s timeout).
2. RESOLVED 2026-11-26: median population is `answered_only`; a timeout counts at its value in the slowest.
3. Count of unresolved failures that makes a run invalid (field `unresolved_failure_invalid_count`, UNSET).
4. Noul band operators at exactly 0.3 and 0.7.
5. Who labels, and who applies the table.
6. Live route: vendor URL with `TYPESAFE_API_KEY`, or the gateway.
7. Where the prompts come from (A-001): candidate public sources are not yet identified.

## Revision 1 (2026-11-26): rebuilt after the pre-execution review

The review of the first plan (report `.dev/reflect/pre-designSpec-20261126145044/REPORT.md`) found 2 blocking findings and 12 medium findings. The route rule chose `regenerate` because 12 is above the medium limit of 9. This section lists what the rebuilt plan must fix and must not repeat. Sections 1 to 10 above are unchanged; where this section differs from sections 3 to 8, this section wins. Each decision below was checked against the `jevlib` code it touches.

### Blocking findings to fix

**M-1 (Missing): no whole-run spend estimate before the first request, and Gate 2's spend bound had no inputs.** Decision: a new module `harness/spend.py` (one job: token estimates and the token ceiling) holds three pure functions. The per-request estimate is `ceil(len(canonical request bytes) / RESERVE_BYTES_PER_TOKEN)`, the formula `JevClient.ask` uses. The whole-run estimate is the sum of the per-request estimates over every frozen prompt, times 2 for the one allowed rerun. The token ceiling is `int(cap_usd / price_usd_per_mtok * 1e6)`. The runner calls `Budget.reserve_phase(phase, whole_run_tokens)` before its first request, where `phase` is `issue611-<run-id>` and is the same string it gives `JevClient`, because `Budget.draw` only draws from a reservation of the client's own phase. It calls `Budget.release_phase(phase)` in a `finally`, so an unspent reservation never stays counted in the shared ledger. Gate 2's spend bound has two inputs and two limits: the whole-run worst-case dollars at the confirmed price must be at most the rule file's `spend_cap_usd`, and the whole-run tokens must fit the ledger's remaining allowance. A run whose requests fit one by one but whose total does not is refused with zero posts.

**M-2 (Decision): Gate 1 refused any `UNSET` value.** Decision: Gate 1 does not check for `UNSET`, as section 5 says. Gate 1 checks the rule file is present, `AGREED`, with who, when and words non-empty, and that the corpus-side hashes match the manifest. The rule file's own hash is not frozen at Gate 1, so the owner can fill the three open fields after Gate 1 without breaking a frozen hash. A separate command, `gate.py freeze-rule`, refuses while any value is `UNSET`, then records the rule file's hash in the manifest and writes the `rule_freeze` event. The lead's go names that hash. Gate 2 refuses an `UNSET` value, a current rule hash that differs from the frozen one, and a go that names a different hash. The table answers do not wait for the open fields, because only Gate 1 gates them.

### Medium findings the plan must not repeat

| ID | Defect not to repeat | Decision |
|---|---|---|
| M-3 | The stop signals were described as exceptions and any non-ok result was rerun. In fact `ask` returns `refused` with error `budget_exhausted` and `invalid` with error `model_mismatch` as results, and only `KeyMissing` and `KeyRejected` are raised. | The runner stops the run, with no rerun, on the exceptions `KeyMissing` and `KeyRejected`, on a result `refused`/`budget_exhausted`, on `invalid`/`model_mismatch` and on `refused`/`dry_run`. Any other non-ok result gets exactly one rerun. The model-pin check applies only to `ok` results, because every non-ok result has `model` of `None` and a timeout must not look like a wrong model. |
| M-4 | One sentence said the runner refuses to start without `--live` and another said it runs a dry run without it. | Two subcommands. `runner.py run` needs `--live`, passing Gate 1 and Gate 2, and the key. `runner.py rehearse` never posts, needs no gate and no key, uses a throwaway ledger outside the experiment's `ledger/` and `runs/` folders, runs the client with `live=False` (so every request ends `refused`/`dry_run` before any transport call), and prints the prompt count and the whole-run estimate. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`. |
| M-5 | The check `grep keyword` could not detect the table's cue words. | A test in `test_questions.py` asserts that none of the table's distinctive cue phrases appears in `questions.py`: stack trace, NameError, undefined, tsc, compiled, lint, slow, latency, p99, too long to load, takes forever, hangs, container, env var, service won't start, CVE, vulnerab, pytest, jest, flake, intermittent, passing locally. Words that are the type names or ordinary English (build, make, deploy, production, memory, leak, auth, token, exposed, null) are exempt, so the definitions can be written in plain words. A person also reads the six definitions once before the freeze. |
| M-6 | A `git status --short` check could not pass because other untracked work folders exist. | Task 1 records `git status --short` to `./artifacts/baseline-status.txt` in the package before it creates anything. The final check removes every entry under the experiment folder from the current status and requires the rest to equal the baseline. |
| M-7 | No command wrote the manifest, the freeze events or the test record; the gate could write the hashes it then checked. | `gate.py` has the subcommands `freeze-corpus`, `gate1`, `freeze-table`, `freeze-rule`, `record-tests` and `gate2`. Only the three `freeze-*` subcommands write the manifest, each its own keys and never an existing key; `gate1` and `gate2` only read it. `record-tests` runs the recorded pytest command itself, refuses a non-zero exit or zero tests, and writes a `tests_passed` event holding the command, the test count and the SHA-256 of every code file and every `jevlib` file; Gate 2 compares those to the current files. `events.py` has the subcommands `owner-input`, `price` and `go`. The scorer's `score` command reads the events and the manifest through functions in `events.py` and `gate.py`. |
| M-8 | `run-record.md` had no task, and the paths and writers of `report.md` and `decision-record.md` differed from the design. | The runner writes `runs/<run-id>/run-record.md` at the end of every run, also after a stop. The scorer writes `report.md` and `decision-record.md` at the experiment root, as section 3 says, for every verdict; for `RUN_INVALID` the record says issue 612 stays undecided. The scorer refuses to overwrite either file. A rescore under another rule file writes `rescores/<name>/report.md` and never touches the root files. |
| M-9 | The README lacked the job "how to rescore". | The README has a "how to rescore" section and a criterion that checks it. |
| M-10 | Nothing covered the pull request wording. | The README has a "Delivery status" section listing parts A to E of section 8 with who does each and whether it is done, and the sentence the pull request must carry: `Refs #611`, with parts B to E listed as left. |
| M-11 | The `jev_answer` mapping was undefined, so the band tests had no expected values. | Let `p` be the Noul value for "does any type fit" (`true` means a type fits) and `choice` the validated answer of `problem_type`. The low operator is `lt` or `le` and the high operator is `gt` or `ge`. If `p` is below the low edge by the low operator, the answer is unset with reason `none-fit`. Else if `p` is above the high edge by the high operator, the answer is `choice` (the validator already guarantees it is the highest probability). Otherwise the answer is unset with reason `not-settled`. This reading follows the design's sentence that the band gives a type, `unset:none-fit` or `unset:not-settled`. |
| M-12 | Nothing stopped a second live run or a reused go. | Gate 2 refuses when any `first_request` or `run_end` event already exists; a go is therefore good for one run. The runner refuses a run id whose folder exists. |
| M-13 | Tests used fixed paths, so a test could append a false `tests_passed` or `lead_go` line to the real, append-only event log. | `loader.Paths(root)` gives every file location from one root. Gate, events, runner and scorer functions take `Paths`, and their tests pass a temporary root. An autouse fixture fails any test that changes the real `events.jsonl`, `ledger/spend.json`, `manifest.json` or `runs/`. |
| M-14 | The spend ceiling used `jevlib`'s import-time price and nothing fed a re-confirmed price into it. | The coordinator records the re-confirmed price with `events.py price --usd-per-mtok <value> --source <text>`. Gate 2 refuses without a `price_confirmed` event. The runner builds its `Budget` with `ceiling_usd` from the rule and `ceiling_input_tokens` from `spend.py` at the confirmed price. `Budget` enforces both limits, so a higher confirmed price makes the token ceiling bind. |

### Notes folded in

`events.py` and `gate.py` hash files only through `loader.sha256_file`. The cue rows of the table are lines 153 to 158 of the troubleshoot skill and the ambiguity rule is line 159. The key scan covers `events.jsonl`, `manifest.json`, the ledger and the run folder. Imports come from the `jevlib` submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`. The jevlib files to hash are the `.py` files directly in the `jevlib` folder, listed by name and never by a folder walk, so `__pycache__` is never hashed. The median and nearest-rank statistics of an empty list are `None`, and a run with no answered prompt is `RUN_INVALID`. The test that the gates run before any environment read replaces `os.environ` with a recorder and asserts that none of `TYPESAFE_API_KEY`, `JEV_API_KEY` or `JEV_API_URL` was read, which also covers the direct read inside `privacy_violation`; `gate1` and `gate2` hash files only and never call the corpus loader.

Task order changes: the events, spend and gates come before the scoring pipeline, because the pipeline's verdict reads their formats.
