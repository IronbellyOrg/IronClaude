# Reflect report: pre-execution review of the rebuilt Jev experiment build plan

```yaml
contract_version: 1.9.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.85
citations_total: 87
citations_revalidated: 87
citations_dropped: 2
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Plan under review: `.dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md` against its spec `source.md` in the same folder (its "Revision 1" section wins over sections 3 to 8). This is the review of the plan rebuilt after a first review (`.dev/reflect/pre-designSpec-20261126145044/REPORT.md`) found 2 Blocking and 12 Medium findings. Tier 2 ran: rule 4 of the tier rubric fired (three domains: code, tests, docs), the parse-density guard forbade a Tier 1 stop, and the Tier 1 card calibrated at C = 0.68. Three reviewers on different model classes reviewed the plan, each card was blind-calibrated (C = 0.83, 0.82, 0.89), and the cards were merged by a two-round debate with an invariant probe (base: card 1; convergence on the 21 diff points 1.00).

**Why partial:** the evidence validator dropped 2 of 87 citations (one in M-17, one in M-21), and two probe findings graded HIGH (INV-001, INV-002) were not debated and are carried as M-11 and M-12 (graded Medium by the grade rule). Departures from the pipeline are recorded in `adversarial/adversarial/base-selection.md` (a lighter qualitative layer) and `adversarial/adversarial/merge-log.md` (merge applied by script).

**Counts:** 3 Blocking, 11 Medium, 7 Note. Parsed coverage 14 of 14 (coverage_pct 1.0000); union coverage 49 of 58 (0.8448); structural-ambiguity density 0.1552.

## Findings

### M-1: Blocking (Decision) Task 6's acceptance bullet requires exactly one post for every systemic stop, including a missing key and a spent ledger, but `KeyMissing` is raised before the transport (zero posts) and `refused`/`budget_exhausted` is returned before the transport, and after the whole-run reservation a draw cannot run short, so `budget_exhausted` cannot occur inside `execute`.

- **Claim:** Task 6's acceptance bullet requires exactly one post for every systemic stop, including a missing key and a spent ledger, but `KeyMissing` is raised before the transport (zero posts) and `refused`/`budget_exhausted` is returned before the transport, and after the whole-run reservation a draw cannot run short, so `budget_exhausted` cannot occur inside `execute`.
- **Evidence:** plan:165; plan:152; client.py:113-137; budget.py:72-78.
- **Consequence:** the stated acceptance check cannot pass with the unchanged `jevlib`, so an implementer cannot satisfy Task 6 as written.
- **Fix:** in Task 6 state zero posts for a missing key, and one post for HTTP 401 and for a returned model other than the pin; replace the spent-ledger case by the `spend_bound` refusal (zero posts) or by a ledger the test changes during the run.
- **Raised by:** C-001

### M-2: Blocking (Missing) the spec requires that a person reads the six question definitions once before the freeze (source.md:142), and no task, README step or procedure carries it; the automated cue test is not the human reading, and `freeze-corpus` hashes `questions.py` and cannot be redone.

- **Claim:** the spec requires that a person reads the six question definitions once before the freeze (source.md:142), and no task, README step or procedure carries it; the automated cue test is not the human reading, and `freeze-corpus` hashes `questions.py` and cannot be redone.
- **Evidence:** source.md:142; plan:39-47; plan:201 (README order of work); plan:181-183 (Task 7). plan:101.
- **Consequence:** the question wording can be frozen with no human review, which the spec forbids.
- **Fix:** add the human reading as a README step before `gate.py freeze-corpus` and as a Task 8 criterion, and name it in Task 7's procedure.
- **Raised by:** C-005

### M-3: Blocking (Missing) the spec requires every `freeze-*` command to write only its own keys and never an existing key, but the plan states the refusal only for `freeze-corpus`; `freeze-table` and `freeze-rule` have none and the only test is a second `freeze-corpus`.

- **Claim:** the spec requires every `freeze-*` command to write only its own keys and never an existing key, but the plan states the refusal only for `freeze-corpus`; `freeze-table` and `freeze-rule` have none and the only test is a second `freeze-corpus`.
- **Evidence:** source.md:144; plan:101-104; plan:115.
- **Consequence:** a re-run of `freeze-table` or `freeze-rule` replaces a frozen hash and hides `table_answers_changed`.
- **Fix:** state the write-once refusal for all three freeze commands and add a test for `freeze-table` and `freeze-rule`.

Group B: Medium.
- **Raised by:** C-006

### M-4: Medium: the row format of `jev-rows.jsonl` and the `run-record.md` format are defined only in Task 6 but consumed by Task 5, which does not depend on Task 6 and is tested only on hand-built rows; no test scores rows written by `execute`.

- **Claim:** the row format of `jev-rows.jsonl` and the `run-record.md` format are defined only in Task 6 but consumed by Task 5, which does not depend on Task 6 and is tested only on hand-built rows; no test scores rows written by `execute`.
- **Evidence:** plan:123; plan:125; plan:129; plan:138; plan:155-156.
- **Consequence:** the scorer can pass every check while unable to read the runner's real rows.
- **Fix:** move the row and run-record format into Task 5 (or add `Depends on: Task 6`) and add a Task 6 or Task 5 test that scores rows written by `execute` with `MockTransport`.
- **Raised by:** C-002

### M-5: Medium: Gate 2's `spend_bound` needs the frozen prompts to build the whole-run estimate, but the plan says the gates never call the corpus loader and gives no source for the prompts; it also does not say how the ledger's remaining allowance is read, though `Budget.__init__` rewrites the ledger.

- **Claim:** Gate 2's `spend_bound` needs the frozen prompts to build the whole-run estimate, but the plan says the gates never call the corpus loader and gives no source for the prompts; it also does not say how the ledger's remaining allowance is read, though `Budget.__init__` rewrites the ledger.
- **Evidence:** plan:106; plan:108; plan:115; budget.py:20-28.
- **Consequence:** an implementer either calls the loader inside Gate 2 (breaking plan:115 and the no-environment-read claim) or leaves `spend_bound` unimplemented.
- **Fix:** state that Gate 2 reads corpus.jsonl as JSON lines, builds the requests and calls `spend.estimate_run_tokens` (or reads an estimate stored by `freeze-corpus`), and reads the ledger file as plain JSON without `Budget`.
- **Raised by:** C-003

### M-6: Medium: `execute` writes `run_end` also for a refusal before any post, and Gate 2's `prior_run` refuses forever once any `run_end` exists, so a run that posted nothing burns the go; an unset `TYPESAFE_API_KEY` is unspecified (assigning `None` into `os.environ` raises, and a key that is not copied raises `KeyMissing` after `first_request`); an unlisted exception such as a bad `JEV_API_URL` after the draw is also unspecified.

- **Claim:** `execute` writes `run_end` also for a refusal before any post, and Gate 2's `prior_run` refuses forever once any `run_end` exists, so a run that posted nothing burns the go; an unset `TYPESAFE_API_KEY` is unspecified (assigning `None` into `os.environ` raises, and a key that is not copied raises `KeyMissing` after `first_request`); an unlisted exception such as a bad `JEV_API_URL` after the draw is also unspecified.
- **Evidence:** plan:106; plan:152; plan:156; plan:159; client.py:133-135; client.py:150; source.md:149.
- **Consequence:** a fixable zero-post failure uses up the single allowed run.
- **Fix:** make `run` exit non-zero before any event or run folder when the key is absent, and state whether a zero-post `run_end` counts for `prior_run` and what `run_end` records on an unlisted exception.
- **Raised by:** C-004, INV-003

### M-7: Medium: the real-state fixture records only existence, size and modification time of `runs/` itself, so an edit of an existing nested file need not be seen, and `Paths(root=None)` defaults to the real folder so a test that omits the root writes to it; the fixture detects only after the fact.

- **Claim:** the real-state fixture records only existence, size and modification time of `runs/` itself, so an edit of an existing nested file need not be seen, and `Paths(root=None)` defaults to the real folder so a test that omits the root writes to it; the fixture detects only after the fact.
- **Evidence:** plan:41-46; plan:59; plan:117; source.md:150. plan:106.
- **Consequence:** A stray append to the real, append-only event log stays on disk after the test run (the fixture fails the test but cannot remove the line) and, for first_request, makes prior_run unpassable.
- **Fix:** make the snapshot cover existing descendant files by hash or size, and have `Paths` refuse the real folder inside tests (for example an environment-free guard in conftest).
- **Raised by:** C-007, INV-008

### M-8: Medium: the T-06 check for a twice-failed prompt does not say the label is `ambiguous` or `none-fit`, where an unset answer would count as right, so an implementation that turns an `error` into an unset answer passes with a typed label.

- **Claim:** the T-06 check for a twice-failed prompt does not say the label is `ambiguous` or `none-fit`, where an unset answer would count as right, so an implementation that turns an `error` into an unset answer passes with a typed label.
- **Evidence:** plan:77-78; plan:127; plan:138. plan:25; source.md:75.
- **Consequence:** a wrong scoring path can pass the check and change b and c.
- **Fix:** require a twice-failed prompt with an `ambiguous` or `none-fit` label to be scored not right and say `score()` bypasses `right` for `error` rows.
- **Raised by:** C-008

### M-9: Medium: `sign_test_passes(b, c)` is described as reading the factor 20 from the rule's `alpha_inverse` but has no rule parameter, and a reference-loop check cannot fail if it is the same formula.

- **Claim:** `sign_test_passes(b, c)` is described as reading the factor 20 from the rule's `alpha_inverse` but has no rule parameter, and a reference-loop check cannot fail if it is the same formula.
- **Evidence:** plan:79; plan:85; plan:137; source.md:113.
- **Consequence:** an implementer hard-codes 20 and a rescore under another `alpha_inverse` silently uses 20.
- **Fix:** give the function an `alpha_inverse` (or rule) parameter and pass stand-in values in the boundary tests.
- **Raised by:** C-009

### M-10: Medium: "answered" is not defined: the Constraints say the median is over each prompt's final answered attempt, Task 3 says the population `median_population` says, and neither says whether an `invalid` 200 response counts or whether an earlier answered attempt of a prompt counts.

- **Claim:** "answered" is not defined: the Constraints say the median is over each prompt's final answered attempt, Task 3 says the population `median_population` says, and neither says whether an `invalid` 200 response counts or whether an earlier answered attempt of a prompt counts.
- **Evidence:** plan:26; plan:81; source.md:78.
- **Consequence:** the T-08 test and the median cannot be pinned.
- **Fix:** define an answered attempt (for example status `ok`) and whether the population is all answered attempts or the last per prompt.
- **Raised by:** C-010

### M-11: Medium: `keyscan.py` reads the key only from `JEV_API_KEY` and prints SKIP with exit 2 when it is unset, while the plan's live key is `TYPESAFE_API_KEY`, copied into `JEV_API_KEY` only inside the runner process; the README keyscan step names no mapping and plan:171 tests only with `--fake`.

- **Claim:** `keyscan.py` reads the key only from `JEV_API_KEY` and prints SKIP with exit 2 when it is unset, while the plan's live key is `TYPESAFE_API_KEY`, copied into `JEV_API_KEY` only inside the runner process; the README keyscan step names no mapping and plan:171 tests only with `--fake`.
- **Evidence:** keyscan.py:80-83; plan:22; plan:159; plan:171; plan:201; SHARED-CONTRACT.md:147-148.
- **Consequence:** with only `TYPESAFE_API_KEY` sourced, the required post-run leak check cannot return OK.
- **Fix:** in the README step, source `TYPESAFE_API_KEY` and export it as `JEV_API_KEY` inside the same one subshell command for `keyscan.py`.
- **Raised by:** INV-001

### M-12: Medium: no task makes `gate.py`, `events.py`, `runner.py` and `scorer.py` importable when run as scripts: only `conftest.py` inserts `sys.path` (plan:41), existing scripts insert it themselves, and no acceptance check runs a CLI as a script or checks that the imported `jevlib` is the hashed one.

- **Claim:** no task makes `gate.py`, `events.py`, `runner.py` and `scorer.py` importable when run as scripts: only `conftest.py` inserts `sys.path` (plan:41), existing scripts insert it themselves, and no acceptance check runs a CLI as a script or checks that the imported `jevlib` is the hashed one.
- **Evidence:** plan:41; plan:59; plan:94; plan:105; plan:147; plan:201; probe.py:17.
- **Consequence:** the documented commands fail with an import error at first use.
- **Fix:** have each CLI module insert the `jevlib` folder and the experiment folder into `sys.path` as `probe.py` does, and add a test that runs each CLI with `--help` as a script.
- **Raised by:** INV-002

### M-13: Medium: `load_corpus` has refusals but `load_table_answers` has none and `freeze-table` only hashes, so a missing, duplicate or misspelled table row skews b and c.

- **Claim:** `load_corpus` has refusals but `load_table_answers` has none and `freeze-table` only hashes, so a missing, duplicate or misspelled table row skews b and c.
- **Evidence:** plan:62; plan:103.
- **Consequence:** wrong counts feed the sign test.
- **Fix:** have `freeze-table` (through `load_table_answers`) refuse ids that are not in the corpus, a corpus id with no row, duplicate rows and an answer outside the six types or null.
- **Raised by:** INV-009

### M-14: Medium: the procedure says the applier receives prompts only, but corpus.jsonl rows carry `label` and `label_basis` and no task produces a labels-free file.

- **Claim:** the procedure says the applier receives prompts only, but corpus.jsonl rows carry `label` and `label_basis` and no task produces a labels-free file.
- **Evidence:** plan:62; plan:183.
- **Consequence:** the applier is likely handed the full corpus and sees the labels.
- **Fix:** add a command or procedure step that writes a prompts-only file (ids and texts) for the applier.

Group C: Notes.
- **Raised by:** INV-010

### M-15: Note: the `exp` fixture is described as holding synthetic frozen files and a rule copy but not the code files and `jevlib` folder that `hash_code` and `record-tests` need.

- **Claim:** the `exp` fixture is described as holding synthetic frozen files and a rule copy but not the code files and `jevlib` folder that `hash_code` and `record-tests` need.
- **Evidence:** plan:59; plan:94; plan:105; plan:112.
- **Consequence:** found at the first test run.
- **Fix:** say the fixture supplies them.
- **Raised by:** C-011

### M-16: Note: three small points: the "31 importers" count at plan:173 does not match a grep (22 files with an import statement, 26 mention `jevlib`); the model check over the models returned by `ok` rows cannot fail because `validate_response` already rejects another model; `load_rule` does not say it converts numeric values, and `attempt_timeout_s` left as a string would break `min(C.ATTEMPT_TIMEOUT_S, ...)`.

- **Claim:** three small points: the "31 importers" count at plan:173 does not match a grep (22 files with an import statement, 26 mention `jevlib`); the model check over the models returned by `ok` rows cannot fail because `validate_response` already rejects another model; `load_rule` does not say it converts numeric values, and `attempt_timeout_s` left as a string would break `min(C.ATTEMPT_TIMEOUT_S, ...)`.
- **Evidence:** plan:129; plan:173; validate.py:32-33; client.py:158. plan:61; plan:149.
- **Consequence:** wording or a small implementation slip.
- **Fix:** correct or drop the count, drop the `ok`-rows check, state the number types.
- **Raised by:** C-012

### M-17: Note: Failed attempts that end `unavailable` (timeouts, 5xx) or as a non-200 `invalid` result are settled at 0 tokens, so 'both attempts counted against the cap' is true only of the drawn estimates; an `invalid` result from a 200 response is settled at its usage; with `MAX_RETRIES = 0` the rerun runs at once with no backoff, so transient 429 or 5xx failures become `error` rows.

- **Claim:** Failed attempts that end `unavailable` (timeouts, 5xx) or as a non-200 `invalid` result are settled at 0 tokens, so 'both attempts counted against the cap' is true only of the drawn estimates; an `invalid` result from a 200 response is settled at its usage; with `MAX_RETRIES = 0` the rerun runs at once with no backoff, so transient 429 or 5xx failures become `error` rows.
- **Evidence:** client.py:202; client.py:204; client.py:191-201; plan:27; plan:149; plan:164.
- **Consequence:** small; the whole-run reservation still bounds spend.
- **Fix:** state that the ledger records failed attempts at 0 and consider a short pause before the rerun.
- **Raised by:** INV-004, INV-005

### M-18: Note: `go` records only the rule hash and Gate 2 checks that events exist, not their order; the event log and manifest are not hashed and a person can edit them.

- **Claim:** `go` records only the rule hash and Gate 2 checks that events exist, not their order; the event log and manifest are not hashed and a person can edit them.
- **Evidence:** plan:98; plan:106.
- **Consequence:** a later price or table event is not bound to the go; the audit trail is advisory.
- **Fix:** record the price and table hashes in the go event, or accept and state the limit.
- **Raised by:** INV-006, INV-007

### M-19: Note: replacing prompts the privacy screen refuses (paths, GitHub URLs, emails) can thin out the stack-trace cues the table keys on.

- **Claim:** replacing prompts the privacy screen refuses (paths, GitHub URLs, emails) can thin out the stack-trace cues the table keys on.
- **Evidence:** manifest.py:13-22; plan:62; plan:183.
- **Consequence:** a possible bias in which prompts survive.
- **Fix:** have selection-criteria.md record how many prompts were replaced and why.
- **Raised by:** INV-011

### M-20: Note: the unresolved-failure limit says "above" but no boundary test fixes `>` against `>=`.

- **Claim:** the unresolved-failure limit says "above" but no boundary test fixes `>` against `>=`.
- **Evidence:** plan:29; plan:131; plan:137.
- **Consequence:** a verdict flip at the boundary.
- **Fix:** add a boundary test once the owner sets the count.
- **Raised by:** INV-012

### M-21: Note: Gate 1 does not freeze the rule hash and the go names a hash, not the values; output tokens are assumed free; the 10 s timeout applies per socket operation so a slow response can run longer.

- **Claim:** Gate 1 does not freeze the rule hash and the go names a hash, not the values; output tokens are assumed free; the 10 s timeout applies per socket operation so a slow response can run longer.
- **Evidence:** plan:29; plan:102; config.py:10; transport.py:29-34; plan:26. plan:98.
- **Consequence:** [INFERRED] small. (The per-socket-operation behaviour of urlopen's timeout is known from how urllib works; the cited lines show only that the timeout is passed on.)
- **Fix:** none needed beyond a note in the README.
- **Raised by:** INV-013, INV-014, INV-015

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Nothing under `src/` changes. | source.md:11 | none (containment 0.5) |
| INF-002 | Nothing here sends a prompt anywhere; | source.md:11 | none (containment 0.4) |
| INF-003 | Reuse by import. Write no new client. | source.md:17 | none (containment 0.4) |
| INF-004 | Build and test offline; the live run is a coordinator step. | source.md:18 | Task 8 (containment 0.71) |
| INF-005 | The runner sets `MAX_RETRIES = 0` and `ATTEMPT_TIMEOUT_S = 10.0` in its own process | source.md:19 | none (containment 0.38) |
| INF-006 | The runner copies it into `JEV_API_KEY` inside its own process only, never printed or written. | source.md:20 | none (containment 0.5) |
| INF-007 | A prompt that would be refused is replaced before freezing, never edited. | source.md:21 | Task 7 (containment 0.75) |
| INF-008 | The gate records the explicit command and its passing result. | source.md:24 | Task 6 (containment 0.67) |
| INF-009 | One cumulative spend ledger (the `Budget` file) across all run ids | source.md:41 | Task 6 (containment 0.9) |
| INF-010 | It refuses a corpus row without a public source, a duplicate id, or duplicate prompt text under two ids. | source.md:68 | Task 2 (containment 0.85) |
| INF-011 | The scorer refuses a rule file with a missing field or a status other than `AGREED`. | source.md:70 | Task 6 (containment 0.67) |
| INF-012 | The runner calls Gate 1 and Gate 2 before reading any environment variable. | source.md:72 | Task 6 (containment 0.8) |
| INF-013 | a typed label is right when the answer equals it; an `ambiguous` or `none-fit` label is right when the answer is unset. | source.md:75 | Task 3 (containment 0.75) |
| INF-014 | from the Noul probability and the band operators in the rule file gives a type, `unset:none-fit` or `unset:not-settled`. | source.md:77 | none (containment 0.45) |
| INF-015 | slowest over all attempts with a timeout counted at its value; 90th percentile by nearest rank | source.md:78 | Task 3 (containment 0.82) |
| INF-016 | `RUN_INVALID` makes no build or close decision on issue 612. | source.md:79 | Task 5 (containment 0.71) |
| INF-017 | Deterministic: same rows, same bytes. | source.md:80 | Task 5 (containment 1.0) |
| INF-018 | A twice-failed prompt is recorded as `error` and scored not right for Jev. | source.md:82 | none (containment 0.57) |
| INF-019 | It runs prompts one at a time, so the per-request spend bound is checked before each request and the whole-run estimate before the first. | source.md:82 | Task 6 (containment 0.79) |
| INF-020 | Append-only `events.jsonl` writer | source.md:84 | Task 4 (containment 0.67) |
| INF-021 | The price is the figure observed on the vendor models page on 2026-11-10 and must be re-confirmed by the coordinator before Gate 2. | source.md:88 | none (containment 0.5) |
| INF-022 | it must say `Refs #611` and list B to E as left | source.md:104 | Task 8 (containment 0.86) |
| INF-023 | What this is, how to run the offline tests, how the coordinator runs the live step, how to rescore | source.md:34 | Task 8 (containment 0.9) |
| INF-024 | The runner calls `Budget.reserve_phase(phase, whole_run_tokens)` before its first request | source.md:132 | Task 6 (containment 1.0) |
| INF-025 | It calls `Budget.release_phase(phase)` in a `finally` | source.md:132 | Task 6 (containment 0.8) |
| INF-026 | A run whose requests fit one by one but whose total does not is refused with zero posts. | source.md:132 | Task 4 (containment 0.75) |
| INF-027 | Gate 1 does not check for `UNSET`, as section 5 says. | source.md:134 | none (containment 0.57) |
| INF-028 | A separate command, `gate.py freeze-rule`, refuses while any value is `UNSET`, then records the rule file's hash in the manifest and writes the `rule_freeze` event. | source.md:134 | Task 4 (containment 0.82) |
| INF-029 | The runner stops the run, with no rerun, on the exceptions `KeyMissing` and `KeyRejected` | source.md:140 | Task 6 (containment 0.86) |
| INF-030 | The model-pin check applies only to `ok` results | source.md:140 | Task 6 (containment 1.0) |
| INF-031 | `runner.py run` needs `--live`, passing Gate 1 and Gate 2, and the key. | source.md:141 | Task 6 (containment 0.67) |
| INF-032 | `runner.py rehearse` never posts, needs no gate and no key | source.md:141 | Task 8 (containment 0.71) |
| INF-033 | A test in `test_questions.py` asserts that none of the table's distinctive cue phrases appears in `questions.py` | source.md:142 | Task 1 (containment 0.91) |
| INF-034 | Task 1 records `git status --short` to `./artifacts/baseline-status.txt` in the package before it creates anything. | source.md:143 | Task 1 (containment 0.73) |
| INF-035 | `gate.py` has the subcommands `freeze-corpus`, `gate1`, `freeze-table`, `freeze-rule`, `record-tests` and `gate2`. | source.md:144 | Task 4 (containment 0.88) |
| INF-036 | `record-tests` runs the recorded pytest command itself, refuses a non-zero exit or zero tests | source.md:144 | Task 4 (containment 0.91) |
| INF-037 | The runner writes `runs/<run-id>/run-record.md` at the end of every run, also after a stop. | source.md:145 | Task 6 (containment 0.91) |
| INF-038 | The scorer refuses to overwrite either file. | source.md:145 | Task 5 (containment 0.8) |
| INF-039 | The README has a "how to rescore" section and a criterion that checks it. | source.md:146 | Task 8 (containment 0.86) |
| INF-040 | and the sentence the pull request must carry: `Refs #611`, with parts B to E listed as left. | source.md:147 | Task 8 (containment 0.91) |
| INF-041 | If `p` is below the low edge by the low operator, the answer is unset with reason `none-fit`. | source.md:148 | Task 3 (containment 0.89) |
| INF-042 | Gate 2 refuses when any `first_request` or `run_end` event already exists; a go is therefore good for one run. | source.md:149 | Task 4 (containment 0.79) |
| INF-043 | An autouse fixture fails any test that changes the real `events.jsonl`, `ledger/spend.json`, `manifest.json` or `runs/`. | source.md:150 | Task 1 (containment 0.82) |
| INF-044 | Gate 2 refuses without a `price_confirmed` event. | source.md:151 | Task 6 (containment 1.0) |

Each quote was checked mechanically as a verbatim substring of its cited line at extraction; none was dropped. The unmatched rows (INF-001, INF-002, INF-003, INF-005, INF-006, INF-014, INF-018, INF-021, INF-027) are carried in substance by the plan's Constraints and by Tasks 3, 4 and 6, as the reviewers confirmed; the word-overlap rule alone did not match them.

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 87` = 0.01

## Recommendations

### Recommendation R-1: Fix Task 6's stop and missing-key criteria

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Task 6 (plan:165, 152, 159))
- **Change:** State zero posts for a missing key and one post for HTTP 401 and a wrong model; replace the spent-ledger case by the `spend_bound` refusal; make `run` exit non-zero before any event or run folder when `TYPESAFE_API_KEY` is absent; say whether a zero-post `run_end` counts for `prior_run`.
- **Verifier:** Task 6's acceptance bullets name the post counts per signal and a test shows no event line is written when the key is absent.
- **Linked findings:** M-1, M-6
- **Priority:** P0

### Recommendation R-2: Add the human reading of the six definitions

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Tasks 7 and 8 (plan:181-183, 201))
- **Change:** Add the person's reading of the six question definitions before `gate.py freeze-corpus` to Task 7's procedure and to the README order of work, with a criterion that checks it.
- **Verifier:** Grep the README and Task 7 for the step before `freeze-corpus`.
- **Linked findings:** M-2
- **Priority:** P0

### Recommendation R-3: Make every freeze command write-once and validate the table answers

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Task 4 (plan:101-104, 115))
- **Change:** State the refusal to replace an existing manifest key for `freeze-table` and `freeze-rule` as for `freeze-corpus`, add tests, and have `freeze-table` refuse ids not in the corpus, missing or duplicate rows and answers outside the six types or null.
- **Verifier:** Tests name a second `freeze-table`, a second `freeze-rule` and each bad table row.
- **Linked findings:** M-3, M-13
- **Priority:** P0

### Recommendation R-4: Define the row format and Gate 2's spend input once

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Tasks 4, 5, 6 (plan:106, 108, 123-129, 155-156))
- **Change:** Move the `jev-rows.jsonl` and `run-record.md` formats into Task 5 (or make Task 5 depend on Task 6) with a test that scores rows written by `execute`; state that Gate 2 reads corpus.jsonl as JSON lines (or a stored estimate) and the ledger as plain JSON.
- **Verifier:** Task 5 lists the row fields and a test names `execute` rows; the gate2 description names its spend input.
- **Linked findings:** M-4, M-5
- **Priority:** P1

### Recommendation R-5: Make the live commands runnable and checkable

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Tasks 4, 6, 8 (plan:41, 94, 147, 201))
- **Change:** Have each CLI insert the `jevlib` and experiment folders into `sys.path`, add a `--help` as a script test, and give the README keyscan step the `TYPESAFE_API_KEY` to `JEV_API_KEY` mapping inside one subshell command.
- **Verifier:** A test runs each CLI as a script; the README step names the mapping.
- **Linked findings:** M-11, M-12
- **Priority:** P1

### Recommendation R-6: Tighten test isolation

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Tasks 1 and 4 (plan:41-46, 59, 94))
- **Change:** Make the real-state snapshot cover existing descendant files, make `Paths` refuse the real folder under tests, and say the `exp` fixture supplies code files and a `jevlib` folder.
- **Verifier:** A test edits an existing nested file in a temporary real-folder stand-in and the fixture fails.
- **Linked findings:** M-7, M-15
- **Priority:** P1

### Recommendation R-7: Pin the scoring details

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Tasks 3 and 5 (plan:25, 77-85, 127, 138))
- **Change:** Give `sign_test_passes` an `alpha_inverse` parameter, define an answered attempt, and require a twice-failed `ambiguous` or `none-fit` prompt to be scored not right through a path that bypasses `right`.
- **Verifier:** Boundary tests pass stand-in `alpha_inverse` values and a T-06 case with an `ambiguous` label.
- **Linked findings:** M-8, M-9, M-10
- **Priority:** P1

### Recommendation R-8: Give the table applier a prompts-only file and clean the notes

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md (Task 7 and the plan text)
- **Change:** Add a step that writes a prompts-only file for the applier; correct the importer count, number types, ledger-at-zero wording and the note-level points.
- **Verifier:** Task 7 names the file and its fields; re-read the cited plan lines after the edit.
- **Linked findings:** M-14, M-16 to M-21
- **Priority:** P2
