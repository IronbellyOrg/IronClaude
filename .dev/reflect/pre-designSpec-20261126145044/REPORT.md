# Reflect report: pre-execution review of the Jev experiment build plan

```yaml
contract_version: 1.9.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.79
citations_total: 113
citations_revalidated: 113
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Plan under review: `.dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md` against its spec `source.md` in the same folder. Tier 2 ran: rule 4 of the tier rubric fired (the plan touches three domains: code, tests, docs) and the parse-density guard also forbade a Tier 1 stop. Three reviewers on different model classes reviewed the plan, each card was blind-calibrated (C = 0.77, 0.79, 0.82), and the cards were merged by `sc-adversarial-protocol` (base: card 1; convergence on the 28 diff points 1.00; invariant gate blocked, so the status is partial).

**Why partial:** one citation was dropped by the evidence validator (M-3, a line range that does not carry the claim), and four high-severity gaps raised by the invariant probe were not debated (they are carried as findings M-1, M-2, M-12 and M-13).

**Counts:** 2 Blocking, 12 Medium, 6 Note. Parsed coverage 14 of 14 (coverage_pct 1.0000); union coverage 33 of 37 (0.8919); structural-ambiguity density 0.1081.

## Findings

### M-1: Blocking (Missing) The design requires the whole-run spend estimate before the first request, but no task performs it: Tasks 5 and 6 guard each request on its own and check the ledger cumulatively, and Gate 2's 'verified per-request spend bound' has no stated inputs or formula, so its check cannot be written to fail.

- **Claim:** The design requires the whole-run spend estimate before the first request, but no task performs it: Tasks 5 and 6 guard each request on its own and check the ledger cumulatively, and Gate 2's 'verified per-request spend bound' has no stated inputs or formula, so its check cannot be written to fail. Budget.reserve_phase already provides the whole-run check; once it is added, an unspent reservation must be released with release_phase in a finally, or it stays counted in the shared ledger and reservations under the same phase name pile up across run ids.
- **Evidence:** card 1 F-5: source.md:72,82; plan:103,119,124; card 2 F-4: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/source.md:82; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:103; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:119-124; card 3 F-2: source.md:82; TASK-WF-designSpec-20261126-144507.md:119,124; jevlib/budget.py:63-70; probe INV-006: budget.py:54, budget.py:69-70, budget.py:98-100
- **Consequence:** T-09 can pass without the whole-run preflight, so a run whose individual requests fit but whose total estimate exceeds the remaining allowance is not refused before any post.
- **Fix:** In Task 6 of TASK-WF-designSpec-20261126-144507.md, add a Budget.reserve_phase whole-run check before the first request, released with release_phase in a finally, plus a test for it, and define the Gate 2 bound's inputs (token ceiling against the largest request).
- **Raised by:** cards 1, 2, 3; merges C-001, INV-006

### M-2: Blocking (Decision) The plan's Gate 1 refuses any UNSET value, stricter than the design, which ties UNSET only to the scorer; the committed rule file has three UNSET fields, so Gate 1 cannot pass and the table answers, allowed only after Gate 1, wait on Noul-band and failure-count fields the table never uses.

- **Claim:** The plan's Gate 1 refuses any UNSET value, stricter than the design, which ties UNSET only to the scorer; the committed rule file has three UNSET fields, so Gate 1 cannot pass and the table answers, allowed only after Gate 1, wait on Noul-band and failure-count fields the table never uses. The fix cannot be made alone: the rule file is hashed at freeze, so filling the UNSET fields later changes a frozen hash (RUN_INVALID, or a Gate 2 mismatch unless a re-hash is defined), and dropping UNSET from Gate 1 also drops it from Gate 2, which adds to Gate 1's checks. A decision between the two options is needed.
- **Evidence:** card 1 F-8: plan:61,103; source.md:70,72; probe INV-001: plan:103, plan:107, plan:84; probe INV-013: variant-1-original.md:45, plan:29, plan:103
- **Consequence:** As written, the table answers are blocked; fixed by dropping UNSET alone, the live run either can never be scored or must be scored after the rule was changed.
- **Fix:** In TASK-WF-designSpec-20261126-144507.md, record the decision on Gate 1's UNSET check: either keep the stricter Gate 1 as a stated decision and define a re-freeze of the rule-file hash for when the UNSET fields are filled, or drop UNSET from Gate 1 and keep it explicitly in the scorer and Gate 2.
- **Raised by:** cards 1; merges C-008, INV-001, INV-013

### M-3: Medium: Task 6 says BudgetExhausted and model_mismatch stop the run and that any non-ok status gets one rerun, but the stop signals are returned results, not exceptions: ask() catches BudgetExhausted and returns refused/budget_exhausted, model_mismatch arrives as invalid/model_mismatch, and a dry run returns refused/dry_run, so the rerun rule would rerun them before any stop.

- **Claim:** Task 6 says BudgetExhausted and model_mismatch stop the run and that any non-ok status gets one rerun, but the stop signals are returned results, not exceptions: ask() catches BudgetExhausted and returns refused/budget_exhausted, model_mismatch arrives as invalid/model_mismatch, and a dry run returns refused/dry_run, so the rerun rule would rerun them before any stop. plan:125 already requires the stops, so the defect is the sentence at plan:119. Sub-point: every non-ok result carries model=None, so comparing the model in jev-rows with the pin turns any timeout into RUN_INVALID.
- **Evidence:** card 1 F-3: jevlib/client.py:114-117, 103-108, 128-131; plan:117-119; card 2 F-2: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:119; .dev/research/346-review-loop-experiments/p15/jev/jevlib/client.py:114-117; card 3 F-1: TASK-WF-designSpec-20261126-144507.md:119; jevlib/client.py:114-117, 127-131, 170-174; jevlib/validate.py:32-33; probe INV-004: client.py:86, client.py:174, plan:84, plan:119
- **Consequence:** An exhausted budget is rerun and recorded as a prompt error instead of stopping the run, and a single timeout can invalidate the whole run.
- **Fix:** In Task 6 of TASK-WF-designSpec-20261126-144507.md (plan:119), check Result.status and error before any rerun so refused/budget_exhausted and invalid/model_mismatch stop the run with no rerun and refused/dry_run is not rerun, and apply the model-pin check only to ok results.
- **Raised by:** cards 1, 2, 3; merges C-002, INV-004

### M-4: Medium: Task 6 says the CLI refuses to start unless --live is given and, two sentences later, that without --live it runs a dry run; it does not say whether a dry run needs the gates.

- **Claim:** Task 6 says the CLI refuses to start unless --live is given and, two sentences later, that without --live it runs a dry run; it does not say whether a dry run needs the gates. The plan documents why live=False is used (plan:30), while the design wants a dry run against the mock transport, and live=False returns refused/dry_run for every prompt before any transport call.
- **Evidence:** card 1 F-4: plan:119; jevlib/client.py:128-131; card 2 F-3: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/source.md:82; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:30; .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:119; .dev/research/346-review-loop-experiments/p15/jev/jevlib/client.py:127-131; card 3 F-10: TASK-WF-designSpec-20261126-144507.md:119; source.md:82
- **Consequence:** An implementer cannot tell how a run without --live behaves or whether it must pass the gates, and a live=False dry run produces only refusals rather than exercising responses.
- **Fix:** In Task 6 of TASK-WF-designSpec-20261126-144507.md, state the dry-run entry rule once (live=False as plan:30 explains, or live=True with the injected MockTransport and a fake key) and whether a dry run checks the gates.
- **Raised by:** cards 1, 2, 3; merges C-003

### M-5: Medium: Task 1's acceptance check `grep -n "keyword" questions.py` is meant to prove no copy of the table's cue words, but it searches for the literal word 'keyword', not the cues ('slow', 'latency', 'stack trace', 'pytest'): a questions.py that copies every cue passes it, and a harmless comment containing 'keyword' fails it.

- **Claim:** Task 1's acceptance check `grep -n "keyword" questions.py` is meant to prove no copy of the table's cue words, but it searches for the literal word 'keyword', not the cues ('slow', 'latency', 'stack trace', 'pytest'): a questions.py that copies every cue passes it, and a harmless comment containing 'keyword' fails it. The required type names build and deployment themselves contain cues from the table. A strict cue-word grep has its own cost: option names and plain definitions naturally use cue words ('build', 'deploy', 'slow', 'auth'), so it pushes the wording of questions.py into awkward phrasing, which biases the comparison against it.
- **Evidence:** card 1 F-1: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:47 (cues at src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:153-158); card 3 F-8: TASK-WF-designSpec-20261126-144507.md:39,47; SKILL.md:154,156; probe INV-007: SKILL.md:154-157, plan:39
- **Consequence:** The Task 1 check neither proves nor disproves that the table's cues were copied, and a strict replacement would distort the question wording.
- **Fix:** In Task 1 of TASK-WF-designSpec-20261126-144507.md, replace the 'keyword' grep with a grep for the cue tokens (for example -Ei "slow|latency|p99|stack trace|pytest|flake|CVE|vulnerab") and exempt the option names build and deployment.
- **Raised by:** cards 1, 3; merges C-005, INV-007

### M-6: Medium: Task 8's final check says `git status --short` shows changes only under the experiment folder 'and the package folder'.

- **Claim:** Task 8's final check says `git status --short` shows changes only under the experiment folder 'and the package folder'. The tree already has untracked .dev/brainstorms/, .dev/issues/611/, .dev/reflect/ and the plan folder under .dev/tasks/, which sit outside both, and 'the package folder' is not defined anywhere, so the check cannot pass as written.
- **Evidence:** card 1 F-2: plan:159; card 3 F-5: TASK-WF-designSpec-20261126-144507.md:159; session git status snapshot
- **Consequence:** Task 8's acceptance check fails even on a correct implementation.
- **Fix:** In Task 8 of TASK-WF-designSpec-20261126-144507.md, measure the `git status --short` check against a baseline status taken when the plan began, or scope it to paths added since then.
- **Raised by:** cards 1, 3; merges C-006

### M-7: Medium: No step or gate.py subcommand writes the manifest at freeze time; the gate 'writes and checks' the manifest itself, so its hash checks can compare against values it just wrote.

- **Claim:** No step or gate.py subcommand writes the manifest at freeze time; the gate 'writes and checks' the manifest itself, so its hash checks can compare against values it just wrote. Task 5 defines a CLI only for events.py (record-tests, record-go), no command records owner_input_received, freeze or rule_freeze, and record-tests is an attestation unless it runs pytest. The tests_passed event carries one evidence hash, but Gate 2 checks it against several current files. The manifest holds the table-answers hash, which does not exist at Gate 1, and how it is written later is not stated. Task 8 asks the README to name gate.py subcommands 'as built in Tasks 4 to 6' that no task defines. The score command's reading of Task 5's events is also unstated (the remaining part of C-012).
- **Evidence:** card 1 F-6: plan:101-103,156; card 3 F-3: TASK-WF-designSpec-20261126-144507.md:101,103,156; source.md:49-56; card 3 F-6 (folded part of C-012): TASK-WF-designSpec-20261126-144507.md:82,84,97
- **Consequence:** The gates' hash checks can pass against values the gate itself just wrote, and the freeze events and Task 8's README list have no command behind them.
- **Fix:** In Task 5 of TASK-WF-designSpec-20261126-144507.md, define the gate.py CLI with a freeze/manifest subcommand and the commands that record owner_input_received, freeze and rule_freeze, record the code hashes in tests_passed, and state when and how the manifest's table-answers hash is written.
- **Raised by:** cards 1, 3; merges C-007

### M-8: Medium: The design lists runs/<run-id>/run-record.md, but no task creates it.

- **Claim:** The design lists runs/<run-id>/run-record.md, but no task creates it. The plan also moves report.md under runs/<run-id>/ and turns decision-record.md into a hand-written template, while the design has the scorer produce both.
- **Evidence:** card 3 F-9: source.md:42,44; TASK-WF-designSpec-20261126-144507.md:84,151
- **Consequence:** run-record.md is never produced, and report.md and decision-record.md end up with different paths or authors than the design names.
- **Fix:** In Tasks 4 and 8 of TASK-WF-designSpec-20261126-144507.md, add the step that creates runs/<run-id>/run-record.md and settle the path and the writer of report.md and decision-record.md.
- **Raised by:** cards 3; merges C-009

### M-9: Medium: The design gives the README the job 'how to rescore', but Task 8's README contents and its acceptance criteria leave it out.

- **Claim:** The design gives the README the job 'how to rescore', but Task 8's README contents and its acceptance criteria leave it out.
- **Evidence:** card 3 F-4: source.md:34; TASK-WF-designSpec-20261126-144507.md:153,156-157
- **Consequence:** The README can ship without rescore instructions and no acceptance check catches it.
- **Fix:** In Task 8 of TASK-WF-designSpec-20261126-144507.md, add a README 'how to rescore' section and an acceptance criterion for it.
- **Raised by:** cards 3; merges C-010

### M-10: Medium: The design (section 8) says the story's pull request 'must say `Refs #611` and list B to E as left'.

- **Claim:** The design (section 8) says the story's pull request 'must say `Refs #611` and list B to E as left'. No task covers it, and the coverage script's match of INF-022 to Task 3 is spurious.
- **Evidence:** card 1 F-9: source.md:104; plan (no task mentions Refs); card 3 coverage_assessment: source.md:104
- **Consequence:** The pull request can omit the required reference and the list of what is left.
- **Fix:** In Task 8 of TASK-WF-designSpec-20261126-144507.md, or a hand-off step, add the pull-request body wording: `Refs #611`, with B to E listed as left.
- **Raised by:** cards 1, 3; merges C-011

### M-11: Medium: jev_answer is described only as using 'the two operators (lt, le, gt, ge)'; the plan does not say which band side yields a type, none-fit or not-settled, which operators are valid for the low and high edges, or which choice is used, so the 'every operator choice' test T-05 has no stated expected values.

- **Claim:** jev_answer is described only as using 'the two operators (lt, le, gt, ge)'; the plan does not say which band side yields a type, none-fit or not-settled, which operators are valid for the low and high edges, or which choice is used, so the 'every operator choice' test T-05 has no stated expected values.
- **Evidence:** card 1 F-7: plan:71,76; source.md:77
- **Consequence:** T-05 cannot be written to fail on a wrong band mapping.
- **Fix:** In TASK-WF-designSpec-20261126-144507.md, state the jev_answer band mapping so each T-05 boundary test has an expected value.
- **Raised by:** cards 1; merges C-014

### M-12: Medium: The gates do not close live calls after the first run: lead_go can be reused, and no gate refuses when a first_request or run_end event already exists, so a rerun of the whole run, which the agreed rule forbids, and picking the better of two runs stay open.

- **Claim:** The gates do not close live calls after the first run: lead_go can be reused, and no gate refuses when a first_request or run_end event already exists, so a rerun of the whole run, which the agreed rule forbids, and picking the better of two runs stay open.
- **Evidence:** probe INV-002: plan:27, plan:103, plan:124
- **Consequence:** A second live run, and keeping the better of two runs, stay possible despite the agreed no-rerun rule.
- **Fix:** In the gate rules of TASK-WF-designSpec-20261126-144507.md (plan:103), make Gate 2 refuse when a first_request or run_end event already exists and make a lead_go usable for one run only.
- **Raised by:** cards ; merges INV-002

### M-13: Medium: Tests are isolated only from the network and the key.

- **Claim:** Tests are isolated only from the network and the key. events.jsonl, ledger/spend.json and runs/ are fixed paths, so a gate or events test could append tests_passed or lead_go to the real log; that log is append-only, so the lines cannot be removed, and Gate 2 could pass with no real go.
- **Evidence:** probe INV-003: plan:19, plan:101, plan:119
- **Consequence:** A test run can leave a permanent false tests_passed or lead_go line that lets Gate 2 pass without a real go.
- **Fix:** In TASK-WF-designSpec-20261126-144507.md, require the gate, events and runner tests to use temporary paths for events.jsonl, ledger/spend.json and runs/.
- **Raised by:** cards ; merges INV-003

### M-14: Medium: The spend ceiling comes from jevlib's price constant: budget.py copies that price when it is imported, jevlib is read-only, and no task feeds a re-confirmed price into the ceiling, so the cap is not shown to hold after the price is re-confirmed.

- **Claim:** The spend ceiling comes from jevlib's price constant: budget.py copies that price when it is imported, jevlib is read-only, and no task feeds a re-confirmed price into the ceiling, so the cap is not shown to hold after the price is re-confirmed.
- **Evidence:** probe INV-005: config.py:10, budget.py:8, budget.py:15-16, plan:119, plan:153
- **Consequence:** If the re-confirmed price differs from the constant, the cap is computed on the old price.
- **Fix:** In Tasks 6 and 8 of TASK-WF-designSpec-20261126-144507.md, add a step that feeds the re-confirmed price into the spend ceiling instead of relying on jevlib's import-time price constant.
- **Raised by:** cards ; merges INV-005

### M-15: Note: The key-scan test T-10 scans only the run folder; events.jsonl, the ledger and the manifest are unscanned, and events.py has no redaction, unlike Journal.

- **Claim:** The key-scan test T-10 scans only the run folder; events.jsonl, the ledger and the manifest are unscanned, and events.py has no redaction, unlike Journal.
- **Evidence:** probe INV-009: plan:126, plan:101, journal.py:27
- **Consequence:** [INFERRED] T-10 can pass while the key is written to an unscanned file. (The cited lines show the key scan runs on the run folder; they do not show that events.jsonl, the ledger or the manifest are left unscanned, so this stays a Note.)
- **Fix:** In TASK-WF-designSpec-20261126-144507.md, extend T-10's key scan to events.jsonl, the ledger and the manifest.
- **Raised by:** cards ; merges INV-009

### M-16: Note: Task 6 says the runner imports JevClient, Budget, Journal, UrllibTransport, TransportTimeout and TransportError 'from jevlib', but jevlib/__init__.py re-exports only MODEL, API_URL and KEY_ENV, so the imports must come from its submodules; KeyMissing and KeyRejected are also missing from the import list.

- **Claim:** Task 6 says the runner imports JevClient, Budget, Journal, UrllibTransport, TransportTimeout and TransportError 'from jevlib', but jevlib/__init__.py re-exports only MODEL, API_URL and KEY_ENV, so the imports must come from its submodules; KeyMissing and KeyRejected are also missing from the import list.
- **Evidence:** card 1 F-3: jevlib/__init__.py:5; plan:117-119; card 2 F-1: .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md:117; .dev/research/346-review-loop-experiments/p15/jev/jevlib/__init__.py:5; card 3 F-11: jevlib/__init__.py:5; TASK-WF-designSpec-20261126-144507.md:117
- **Consequence:** Wording only; read literally, `from jevlib import ...` fails before the runner tests can run.
- **Fix:** In Task 6 of TASK-WF-designSpec-20261126-144507.md, name the defining jevlib submodule for each import and add KeyMissing and KeyRejected to the list.
- **Raised by:** cards 1, 2, 3; merges C-004

### M-17: Note: The design says the loader owns hashing, but the plan has events.py and gate.py compute SHA-256 without requiring loader.sha256_file.

- **Claim:** The design says the loader owns hashing, but the plan has events.py and gate.py compute SHA-256 without requiring loader.sha256_file. The card's second point, reusing jevlib.Journal for events.py, was withdrawn in the debate.
- **Evidence:** card 3 F-7: source.md:68; TASK-WF-designSpec-20261126-144507.md:101,103
- **Consequence:** Duplicate hashing code that can drift from the loader's.
- **Fix:** In Task 5 of TASK-WF-designSpec-20261126-144507.md, have events.py and gate.py hash files with loader.sha256_file.
- **Raised by:** cards 3; merges C-013

### M-18: Note: 'Six cue rows .

- **Claim:** 'Six cue rows ... SKILL.md lines 152 to 159' is imprecise: the rows are lines 153 to 158, line 152 is the step heading and line 159 is the ambiguity rule.
- **Evidence:** card 1 F-10: SKILL.md:152-159; plan:137,141
- **Consequence:** Wording only; a reader may count the heading and the ambiguity rule as cue rows.
- **Fix:** In TASK-WF-designSpec-20261126-144507.md (plan:137,141), cite SKILL.md lines 153 to 158 for the cue rows and line 159 for the ambiguity rule.
- **Raised by:** cards 1; merges C-015

### M-19: Note: Edge cases are not bounded: if no prompt is answered, the median and nearest-rank calculations run on an empty list; 'the jevlib files' is undefined; and a folder walk would hash __pycache__, which git ignores.

- **Claim:** Edge cases are not bounded: if no prompt is answered, the median and nearest-rank calculations run on an empty list; 'the jevlib files' is undefined; and a folder walk would hash __pycache__, which git ignores.
- **Evidence:** probe INV-010: plan:71, plan:77, plan:103, .gitignore:2
- **Consequence:** The statistics can fail on an empty run, and a hash can change with compiled-file caches.
- **Fix:** In TASK-WF-designSpec-20261126-144507.md, state the result of the median and nearest-rank statistics on an empty list, list the jevlib files to hash, and exclude __pycache__ from hashing.
- **Raised by:** cards ; merges INV-010

### M-20: Note: The 'gates before any environment read' test can miss a read: load_corpus calls privacy_violation, which reads os.environ directly, so a stubbed environment accessor never sees that read.

- **Claim:** The 'gates before any environment read' test can miss a read: load_corpus calls privacy_violation, which reads os.environ directly, so a stubbed environment accessor never sees that read.
- **Evidence:** probe INV-011: plan:57, plan:125, manifest.py:35
- **Consequence:** The test can pass while an environment read happens before the gates.
- **Fix:** In TASK-WF-designSpec-20261126-144507.md, make the 'gates before any environment read' test cover privacy_violation's direct os.environ read in load_corpus.
- **Raised by:** cards ; merges INV-011

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Nothing under `src/` changes. | source.md:11 | none (containment 0.5) |
| INF-002 | Nothing here sends a prompt anywhere; | source.md:11 | none (containment 0.5) |
| INF-003 | Reuse by import. Write no new client. | source.md:17 | none (containment 0.4) |
| INF-004 | Build and test offline; the live run is a coordinator step. | source.md:18 | Task 8 (containment 0.86) |
| INF-005 | The runner sets `MAX_RETRIES = 0` and `ATTEMPT_TIMEOUT_S = 10.0` in its own process | source.md:19 | Task 6 (containment 1.0) |
| INF-006 | The runner copies it into `JEV_API_KEY` inside its own process only, never printed or written. | source.md:20 | Task 6 (containment 0.86) |
| INF-007 | A prompt that would be refused is replaced before freezing, never edited. | source.md:21 | Task 7 (containment 0.67) |
| INF-008 | The gate records the explicit command and its passing result. | source.md:24 | Task 6 (containment 0.83) |
| INF-009 | One cumulative spend ledger (the `Budget` file) across all run ids | source.md:41 | Task 6 (containment 1.0) |
| INF-010 | It refuses a corpus row without a public source, a duplicate id, or duplicate prompt text under two ids. | source.md:68 | Task 2 (containment 0.92) |
| INF-011 | The scorer refuses a rule file with a missing field or a status other than `AGREED`. | source.md:70 | Task 2 (containment 0.75) |
| INF-012 | The runner calls Gate 1 and Gate 2 before reading any environment variable. | source.md:72 | Task 6 (containment 1.0) |
| INF-013 | a typed label is right when the answer equals it; an `ambiguous` or `none-fit` label is right when the answer is unset. | source.md:75 | Task 3 (containment 0.89) |
| INF-014 | from the Noul probability and the band operators in the rule file gives a type, `unset:none-fit` or `unset:not-settled`. | source.md:77 | Task 3 (containment 0.67) |
| INF-015 | slowest over all attempts with a timeout counted at its value; 90th percentile by nearest rank | source.md:78 | Task 3 (containment 0.9) |
| INF-016 | `RUN_INVALID` makes no build or close decision on issue 612. | source.md:79 | Task 8 (containment 0.86) |
| INF-017 | Deterministic: same rows, same bytes. | source.md:80 | Task 4 (containment 1.0) |
| INF-018 | A twice-failed prompt is recorded as `error` and scored not right for Jev. | source.md:82 | Task 4 (containment 0.88) |
| INF-019 | It runs prompts one at a time, so the per-request spend bound is checked before each request and the whole-run estimate before the first. | source.md:82 | Task 6 (containment 0.79) |
| INF-020 | Append-only `events.jsonl` writer | source.md:84 | Task 5 (containment 0.75) |
| INF-021 | The price is the figure observed on the vendor models page on 2026-11-10 and must be re-confirmed by the coordinator before Gate 2. | source.md:88 | none (containment 0.43) |
| INF-022 | it must say `Refs #611` and list B to E as left | source.md:104 | Task 3 (containment 0.6) |
| INF-023 | What this is, how to run the offline tests, how the coordinator runs the live step, how to rescore | source.md:34 | Task 8 (containment 0.6) |

Each quote was checked mechanically as a verbatim substring of its cited line at extraction; none was dropped. The four unmatched rows (INF-001, INF-002, INF-003, INF-021) are covered in substance by the plan's Constraints and by Tasks 6 and 8, as the reviewers confirmed; the word-overlap rule alone did not match them.

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 113` = 0.01

## Recommendations

### Recommendation R-1: Add to Task 6 (and the Task 5 Gate 2 check) a whole-run spend estimate before th

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Add to Task 6 (and the Task 5 Gate 2 check) a whole-run spend estimate before the first request, using `reserve_phase` and releasing it in a `finally` with `release_phase`; define the inputs of Gate 2's spend bound.
- **Verifier:** Task 6 and Task 5 name `reserve_phase`, `release_phase` and the bound's inputs; a test shows zero posts when only the total estimate exceeds the ceiling.
- **Linked findings:** M-1
- **Priority:** P0

### Recommendation R-2: Decide Gate 1's `UNSET` rule

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Decide Gate 1's `UNSET` rule: keep it and define how the rule file is re-frozen when the open fields are set, or drop it from Gate 1 and keep it in the scorer and Gate 2.
- **Verifier:** Task 2 and Task 5 state the choice and the re-freeze step; the Gate 1 test matches it.
- **Linked findings:** M-2
- **Priority:** P0

### Recommendation R-3: Rewrite the Task 6 stop and rerun sentences

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Rewrite the Task 6 stop and rerun sentences: stop with no rerun on `refused`/`budget_exhausted`, `invalid`/`model_mismatch` and `dry_run`; state one dry-run rule; import from the jevlib submodules; do not treat a timeout as a wrong model.
- **Verifier:** Task 6 names those status and error pairs and the submodule imports; the acceptance tests drive each stop.
- **Linked findings:** M-3, M-4, M-16
- **Priority:** P1

### Recommendation R-4: Fix Task 1's check to grep for the real cue words

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Fix Task 1's check to grep for the real cue words, exempting the option names; fix Task 8's `git status` check to compare with a baseline.
- **Verifier:** Task 1 and Task 8 acceptance bullets name the cue list, the exemption and the baseline.
- **Linked findings:** M-5, M-6
- **Priority:** P1

### Recommendation R-5: Define the `gate.py` commands (freeze

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Define the `gate.py` commands (freeze, manifest, gates), the freeze events, the `tests_passed` hashes and when the manifest is rewritten; add the band mapping for `jev_answer`.
- **Verifier:** Task 5 and Task 3 name the commands and the mapping; each boundary test states its expected value.
- **Linked findings:** M-7, M-11
- **Priority:** P1

### Recommendation R-6: Add `run-record.md`

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Add `run-record.md`, the README rescore section and the pull-request wording to Tasks 6 and 8, and settle where `report.md` and `decision-record.md` live.
- **Verifier:** Task 8's README criteria name rescore, `run-record.md` and the PR wording.
- **Linked findings:** M-8, M-9, M-10
- **Priority:** P1

### Recommendation R-7: Add test isolation (temporary paths for `events.jsonl`

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Add test isolation (temporary paths for `events.jsonl`, the ledger and runs), a refusal of a second live run, and a way to feed a re-confirmed price into the cap.
- **Verifier:** Tasks 5 and 6 require temporary paths; a test shows Gate 2 refuses when a `first_request` event already exists.
- **Linked findings:** M-12, M-13, M-14
- **Priority:** P1

### Recommendation R-8: Clean up the notes

- **File:** .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- **Change:** Clean up the notes: cite cue rows as lines 153 to 158, prefer `loader.sha256_file`, scan the event log and ledger for the key, and handle empty statistics.
- **Verifier:** Re-read the cited plan lines after the edit.
- **Linked findings:** M-15 to M-20
- **Priority:** P2
