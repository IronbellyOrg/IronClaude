---
type: spec
topic: "Jev vs the keyword table on about 30 labelled public prompts (issue 611)"
variant: 2
status: draft
---

# Requirements: Jev vs keyword table experiment (issue 611)

## 1. Purpose and scope

Decide, from a measurement, whether Jev (TypeSafe model `jev-1.14.0`) clearly beats the prose keyword table in Wave 0 of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` at picking one of six problem types (`bug`, `build`, `performance`, `deployment`, `security`, `test`). The verdict decides issue 612: build the Jev preflight classifier, or close it as not justified. The verdict is recorded on issues 611 and 609, and issue 612 is updated.

The experiment is built to be rerun, re-scored and re-read later. Everything that defines it (corpus, labels, question wording, decision rule) is a frozen file with a recorded hash. Everything it produces (per-prompt records, report, decision) is a file that can be rescored offline without a live call.

In scope: a corpus of about 30 public prompts, one question file, one decision-rule file, a small live runner, a small offline scorer with tests, a results file, a report and a decision record.

Out of scope: a production preflight command or hook, a gateway rewrite, depth or scope comparison, private repositories (issue 552), any edit to the table, any change under `src/`.

Already decided by the lead on 2026-11-26 (inputs, not options): send about 30 PUBLIC prompts to TypeSafe using the `TYPESAFE_API_KEY` environment variable; spend cap of 1 dollar; public prompts only; the key is never printed or stored.

Baseline: `origin/integration` at `37765a800d0b232cc231cf58b796fec23b26f8a8`; table file blob `76bcb3d94182371250ffe99a7b60b9124b05c368`.

## 2. Functional requirements

Corpus
- FR-001. A single corpus file holds about 30 prompts. Each entry has: id, prompt text, label (one of the six types, or `ambiguous`, or `none-fit`), labeller, label date, and public provenance (a URL or a citation that a third party can open).
- FR-002. The corpus covers all six types at least once, and includes at least one `ambiguous` and at least one `none-fit` entry. The offline scorer checks this and fails on a gap.
- FR-003. Any entry without recorded public provenance is rejected by the scorer's corpus check. No private-repository text may appear.
- FR-004. The corpus file and its labels are frozen before either arm runs. Freezing means a SHA-256 hash recorded in `manifest.json`; any later change to the file makes the gate (FR-014) fail.

Question file
- FR-005. One question file holds all Jev wording: the Choice question over the six types and the companion Noul question asking whether any type fits. No question text is hard-coded in the runner or the scorer.
- FR-006. The question file records the pinned model `jev-1.14.0`. An alias is rejected by the runner.
- FR-007. Each prompt costs one request carrying both questions (one Choice, one Noul).

Table arm
- FR-008. The table arm is applied as written, with its structural cues and ambiguity rule preserved ("unset when unclear"; "leak" deliberately in both performance and security). It is not replaced by a first-match parser or a better classifier.
- FR-009. Each table answer records its method (a person reading the prose table, or running the skill's Wave 0), who or what produced it, and the date. All table answers are written to the results file before any Jev call is made.

Jev arm and scoring rules
- FR-010. Per prompt, the Jev record stores: the Choice answer, its probability, the Noul value, latency in milliseconds, call status, and the raw response body with request headers excluded.
- FR-011. A Noul value strictly between the lower and upper bounds set in the decision-rule file means "not settled" and the type is left unset. The decision-rule file states, before scoring, the treatment of values at exactly the bounds. The scorer takes these from the rule file and has no built-in default.
- FR-012. A failed call is stored as status `error`. It is never converted to "no" or to "unset". The decision-rule file states, before scoring, how an `error` counts in the accuracy denominator and in the abstention rate. The scorer takes this from the rule file.
- FR-013. The scorer produces, for both arms: accuracy, abstention rate, cost, median latency, slowest latency, and the list of disagreements between the arms (prompt id, label, table answer, Jev answer).

Run gate
- FR-014. The live runner refuses to start unless the gate in section 4 passes. The gate check is a separate function that runs before the runner reads the environment variable.
- FR-015. The runner stops before a call that could take cumulative spend over 1 dollar. The stop is recorded in the results file with the cumulative cost at that point.
- FR-016. The runner makes no automatic retry. A failed call is recorded and the run continues. If a retry policy is wanted, it is written in the decision-rule file before the run and each retry counts against the cap.

Decision
- FR-017. The verdict is computed by the scorer from the results file and the decision-rule file, and written to the decision record. The verdict is one of: `jev-clearly-beats-table`, `not-clearly`, or `run-incomplete`. No human edit of the numbers is allowed between scorer output and decision record.
- FR-018. The scorer can re-score any stored results file offline, with a different rule file, for later review. A re-score writes a new report and never edits the original.

## 3. Non-functional requirements

Cost
- NFR-001. Total spend is at or under 1 dollar. The issue quotes about 0.00004 dollars per call; the runner records per-call cost from the response where given, and from the quoted rate otherwise, labelled as an estimate.
- NFR-002. The runner computes the worst-case spend for the whole run before the first call and refuses to start if that figure is over the cap.

Privacy and key secrecy
- NFR-003. Only public prompts are sent. The corpus check (FR-003) is the control.
- NFR-004. The key is read from `TYPESAFE_API_KEY` only at call time, held in memory, and sent only in the request authorization header. It is never printed, logged, written to any file, placed in an error message, a result record, a pull request text or an issue comment.
- NFR-005. Error text and raw responses are passed through a redaction step before storage. After the run, an offline check scans every file in the experiment folder for the key's presence and fails on a match. This is checked with the runner's own in-memory value and a pattern, never by printing the key.
- NFR-006. The experiment writes no shell history, command echo or debug trace containing the key. Run commands never put the key on a command line.

Reproducibility
- NFR-007. `manifest.json` records: hashes of the corpus, question file and decision-rule file; the pinned model; baseline revision and table blob; scorer version (git commit); run id; run start and end time (UTC); and the table method (FR-009).
- NFR-008. Result files are append-only per run id. A rerun gets a new run id and a new results file. Nothing is overwritten.
- NFR-009. The scorer uses only the standard library, is deterministic (no clock, no randomness, no network), and runs through `uv run`.

Maintainability
- NFR-010. The code is small: one runner, one scorer, one shared loader for the three frozen files. It has no abstraction beyond that.
- NFR-011. Each file in the folder has one job (section 5), so a reader can re-judge the decision from the folder alone, without the chat history.

## 4. Run gate and decision rule

Two required inputs are PENDING from the owner and have no default and no suggested value:

- Input A: the margin Jev must win by.
- Input B: the acceptable median latency for a pre-step.

Both must be typed in by the owner, recorded word for word (the owner's exact words, the lead who typed them, date and time) in the decision-rule file before the first live call. Neither is inferred from the corpus size, from the disagreement count, or from any prior result. The unit of Input A (count of prompts or share) is whatever the owner's words say.

Gate (all must be true, checked by code, in this order, before the runner reads the environment variable):

1. The decision-rule file has Input A and Input B filled with the owner's recorded words, a typed-in date, and no `PENDING` marker.
2. The decision-rule file also states the Noul bound treatment (FR-011), the `error` treatment (FR-012) and the retry policy (FR-016), and carries a date.
3. The corpus, question file and decision-rule file hashes match `manifest.json`, and the manifest was written before any results file exists.
4. All table answers (FR-009) are already stored.
5. The worst-case spend check (NFR-002) passes.

Decision rule (fixed before the run, not changed after seeing results): Jev "clearly beats" the table only if both hold: (a) its accuracy exceeds the table's by at least Input A, measured as the owner worded it; and (b) its median latency is within Input B. Any other complete outcome is `not-clearly`. If the run stopped early (cap, repeated errors, key failure), the verdict is `run-incomplete` and no build decision is made from it. A changed rule means a new dated rule file and a new run id; the old rule file is kept.

If the gate fails, the runner exits with the failed check named and makes no network call.

## 5. Artifacts and where they live under .dev/

Proposed folder (name to be confirmed, see section 8): `.dev/research/jev-vs-keyword-table-611/`.

| File | Job |
|---|---|
| `README.md` | One page: what this is, how to rerun, how to rescore |
| `corpus.jsonl` | Frozen prompts, labels, provenance (FR-001 to FR-004) |
| `questions.md` | The only copy of Jev question wording and the pinned model (FR-005, FR-006) |
| `decision-rule.md` | Inputs A and B in the owner's words, Noul bounds, error treatment, retry policy, dates |
| `manifest.json` | Hashes, baseline revision, table blob, scorer version, run ids (NFR-007) |
| `table-answers.jsonl` | Table arm answers with method and provenance (FR-009) |
| `runs/<run-id>/results.jsonl` | One line per prompt: label, table answer, Jev answer, probability, Noul, latency, status, cost, raw body (FR-010) |
| `runs/<run-id>/report.md` | Aggregate numbers and disagreements (FR-013) |
| `decision.md` | Verdict, the rule it was computed from, links to the issue 611, 609 and 612 updates |
| `scorer/` | `score.py`, `load.py` and the runner `run_live.py` |
| `scorer/tests/` | Offline tests (section 6) |

No file is written under `src/`. The folder is under `.dev/`, so the repository rule that `.dev/tasks/` is staged does not apply to it; whether this folder is committed is an open question (section 8). Raw responses are stored only after redaction (NFR-005).

## 6. Test obligations (offline, no live API)

All tests run with `uv run pytest <scorer/tests path> -v`, use fixture files made by hand, and fail if any socket is opened (the network is blocked in the test setup). No test reads `TYPESAFE_API_KEY`.

- T-01. Corpus check: rejects a missing provenance, a missing type, no `ambiguous` entry, no `none-fit` entry, a duplicate id (FR-001 to FR-003).
- T-02. Hash check: a changed corpus, question or rule file fails the gate (FR-004, gate step 3).
- T-03. Gate: a rule file with `PENDING` in Input A or Input B fails; a rule file with both filled and the other required fields passes. The test uses placeholder words that are clearly not real owner values.
- T-04. Gate order: with the gate failing, the runner's environment read and its HTTP function are never called (use stubs that raise).
- T-05. Noul scoring: values below, inside and above the bounds, and at each bound under each treatment the rule file can state (FR-011).
- T-06. `error` scoring: an error is never counted as "no" or "unset"; both treatments the rule file can state are covered (FR-012).
- T-07. Aggregates: accuracy, abstention, median and slowest latency, disagreements, on a hand-computed fixture of known answers (FR-013).
- T-08. Verdict: boundary cases on both sides of Input A and Input B, using stand-in numbers in the fixture, and `run-incomplete` (FR-017).
- T-09. Spend stop: a stubbed transport with rising costs stops before the cap and records the stop (FR-015). A cap-exceeding worst-case estimate refuses to start (NFR-002).
- T-10. Key secrecy: a stubbed transport whose error text contains a fake key string; assert the stored record and any printed output do not contain it; the folder scan (NFR-005) flags a planted fake key in a fixture file.
- T-11. Determinism: the same results and rule file give a byte-identical report on two runs; the scorer imports nothing outside the standard library (NFR-009).
- T-12. Rescore: scoring a stored results file under a second rule file leaves the original files unchanged (FR-018).
- T-13. Alias: a question file naming a model other than `jev-1.14.0` is rejected (FR-006).

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Owner numbers are late, so the run stalls | The gate is a hard stop; all offline work (corpus, labels, table arm, scorer, tests) can finish first |
| Margin chosen after seeing results | Rule file is dated and hashed before the first call; the manifest is written before any results file exists |
| About 30 prompts make differences small | The report shows counts beside shares; the rule is the owner's; `not-clearly` is a valid result |
| Label bias (one person labels, then judges the arms) | Labels are frozen first and record the labeller; the table arm is produced before any Jev result is seen |
| Table arm quietly improved by the reader | FR-008 and FR-009 record method and keep the ambiguity rule; the table blob hash is in the manifest |
| Key leaks through error text or a trace | Redaction before storage, folder scan, no key on any command line (NFR-004 to NFR-006) |
| Service changes or model is retired between run and review | Raw bodies and the pinned model are stored; a later reader can rescore and see the run's date |
| Spend overrun from loops or retries | No automatic retry, a worst-case check before start, and a stop before the cap |
| Folder becomes a pile of one-off scripts | One loader, one scorer, one runner; one file per job (NFR-010, NFR-011) |

## 8. Open questions

1. Input A (the margin Jev must win by): PENDING from the owner. No value is assumed.
2. Input B (the acceptable median latency): PENDING from the owner. No value is assumed.
3. Treatment of Noul values at exactly the lower and upper bounds, the Noul bounds themselves as the issue states them (0.3 and 0.7), and how an `error` counts against accuracy and abstention: to be written in the rule file before scoring.
4. How the table arm is applied: a person reading the prose table, or running the skill's Wave 0. This decides what FR-009 records as provenance (see `docs/memory/reflect/deviation-patterns-issue-610.md`).
5. How the prompts are sourced and who labels them; how ambiguous and none-fit entries are chosen; whether a second labeller checks.
6. Experiment folder name: `.dev/research/jev-vs-keyword-table-611/` is proposed. Whether the folder is committed with the pull request, and whether the scorer tests should also be collected by the repository's normal test run, need a decision.
7. Whether the live call is a script in the repository (as specified here) or a manual sequence. A script is proposed because it makes the cap, the gate and the key handling checkable.
8. Whether a retry policy is wanted at all (FR-016 defaults to none).
