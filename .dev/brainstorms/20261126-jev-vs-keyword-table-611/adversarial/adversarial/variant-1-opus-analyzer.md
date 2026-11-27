---
title: "Requirements: Jev versus the keyword table on about 30 labelled public prompts (#611)"
type: spec
---

# Requirements: Jev versus the keyword table (#611)

## 1. Purpose and scope

Measure whether Jev (TypeSafe, pinned `jev-1.14.0`) picks the `/sc:troubleshoot` problem type more accurately than the Wave 0 keyword table, on about 30 frozen, human-labelled public prompts, so that issue 612 is built or closed as not justified. Label leakage, small-sample noise, failure handling and table-arm provenance are requirements, not notes.

In scope: corpus, labels, question file, scoring rule, offline scorer and tests, one gated live run, report, decision record. Out of scope: a production preflight command or hook, gateway rewrite, depth or scope comparison, private repositories (issue 552), any change under `src/`, any edit to the table.

Baseline: `origin/integration` at `37765a800d0b232cc231cf58b796fec23b26f8a8`; table file blob `76bcb3d94182371250ffe99a7b60b9124b05c368` (Wave 0, `SKILL.md` lines 152 to 159).

## 2. Functional requirements

**Corpus and labels**

- FR-001: Each of about 30 prompts records id, verbatim text, public source link or repository path, retrieval date and selection reason. A prompt without public provenance is rejected.
- FR-002: The corpus covers all six types plus at least one ambiguous and one none-fit case. Selection criteria are written before either arm classifies any prompt, so selection cannot follow arm outcomes.
- FR-003: Each prompt has one label (one of the six types, `ambiguous`, or `none-fit`) and a one-line labelling basis drawn from the problem's actual nature (for example its public fix), not from which keywords appear, so labels do not encode the table's own rule.
- FR-004: The labeller has seen no table or Jev answer for the corpus. Labeller role and labelling date are recorded.
- FR-005: A prompt that also appears in `tests/troubleshoot/`, the skill text, or the #871 verification observations is flagged `seen-by-table`. Both arms' accuracy is reported with and without them.
- FR-006: Labels freeze before either arm runs; the corpus file's SHA-256 goes in the gate record (Section 4).

**Question file**

- FR-007: All Jev wording (the Choice over `bug`, `build`, `performance`, `deployment`, `security`, `test`, and the companion Noul asking whether any type fits) lives in one hashed file containing no corpus prompt, label or corpus-derived example.

**Table arm**

- FR-008: The table is applied as written: keyword and structural cues, ambiguity leaves the type unset, "leak" stays in both performance and security. No first-match parser, normalisation or added inference.
- FR-009: The method (a person reading the prose table, or execution of the skill's Wave 0) is recorded before application. Execution records the exact skill copy path, revision, blob and evidence of which copy ran. Manual application is labelled manual, not runtime evidence.
- FR-010: A written procedure states, before application, how "no cue matched" and "cues from two or more rows" resolve, consistent with the ambiguity rule.
- FR-011: The table applier is blind to labels and Jev answers and records, per prompt, the cues and rows matched.

**Jev arm**

- FR-012: One request per prompt, the same prompt bytes the table arm received, model `jev-1.14.0` named explicitly. A response naming any other model is an error.
- FR-013: Each row records Choice answer, probability of every returned answer, Noul value, client latency (monotonic clock, send to full response), cost and status.
- FR-014: Noul above the not-settled band: type is the Choice answer. Below it: unset, reason `none-fit`. Inside it: unset, reason `not-settled`. The scoring rule states the band with explicit operators at 0.3 and 0.7, fixed before the run.
- FR-015: A transport error, timeout, malformed body, missing Choice or Noul, Choice outside the six values, or wrong model is status `error`, never mapped to "no", `none-fit` or abstention.
- FR-016: Retry policy and per-call timeout are fixed in the run record before the run. This spec requires no retries in the scored run.

**Scoring and report**

- FR-017: Correct means a typed label matched by the same type, or an `ambiguous` or `none-fit` label matched by an unset type. Unset on a typed label is incorrect and counted as an abstention.
- FR-018: The accuracy denominator is every prompt in the frozen corpus. Jev errors count as not correct and are also reported as a count and rate.
- FR-019: Per arm: correct count, accuracy, abstentions by reason, errors. For Jev also: total cost, and median and slowest latency over all attempted calls (failures at measured or timeout time) and over successful calls.
- FR-020: Paired breakdown: prompts both arms got right, only Jev, only the table, neither, showing how many prompts any difference rests on.
- FR-021: Every disagreement is listed with prompt id, label, both answers, Jev probabilities and Noul.
- FR-022: All aggregates are recomputed by the scorer from retained rows; none is hand-entered.

**Decision**

- FR-023: The verdict is computed mechanically (Section 4) as `JEV_BEATS_TABLE`, `JEV_DOES_NOT_BEAT_TABLE` or `RUN_INVALID`.
- FR-024: The decision record (verdict, inputs, hashes, report path) goes to the coordinator for issues 611, 609 and 612. This work makes no GitHub write.

## 3. Non-functional requirements

- NFR-001 Cost: total spend at or under 1 dollar. Before each call the runner checks that spend so far plus the worst-case cost of one more call stays within the cap; otherwise it stops and records the stop. Price is checked at execution time; the issue's 0.00004 dollars per call is an estimate.
- NFR-002 Privacy: public prompts only. A prompt containing a credential-shaped string or personal data is excluded and replaced, not edited, so both arms see verbatim public text.
- NFR-003 Key secrecy: `TYPESAFE_API_KEY` is read from the environment only inside the runner process. It is never printed, logged, written to a file, passed on a command line, or put in issue or pull request text. The runner refuses to write any artifact containing the key value.
- NFR-004 Reproducibility: the run record holds baseline revision and blob, hashes of corpus, question file, scoring rule and runner, the requested pin and returned model id, and timestamps of the gate record and first call. The scorer is deterministic.
- NFR-005 Single scored run: the first complete run is scored. A rerun needs a reason recorded before it starts, and every run is reported; no best-of-N selection.

## 4. Run gate and decision rule

The gate record must hold, before the first live call:

1. The margin Jev must win by, word for word as the lead typed it from the owner. Required input; now PENDING.
2. The acceptable median latency, word for word as the lead typed it from the owner. Required input; now PENDING.
3. When each was recorded and who typed it.
4. The owner's sending approval (public prompts, `TYPESAFE_API_KEY`, 1 dollar cap), word for word.
5. SHA-256 of corpus, question file and scoring rule.
6. A restatement of items 1 and 2 as comparisons the scorer applies, confirmed by the lead as meaning exactly the verbatim text. If the verbatim text leaves the unit (count of prompts or share), denominator, or tie handling unclear, the lead gets the owner's clarification and records it word for word.

The runner opens no network connection unless the gate record exists, items 1 and 2 are present and neither empty nor `PENDING`, item 6 is confirmed, the hashes match the files on disk, and the gate timestamps precede the run. Otherwise it exits with a named refusal and sends nothing.

Decision rule, fixed before the run and not changed after results are seen:

- `RUN_INVALID` if a frozen file changed after hashing, the run stopped at the cap before all prompts, a gate condition was missing, or the table provenance record (FR-009) is absent.
- Else `JEV_BEATS_TABLE` only if Jev's correct count exceeds the table's by the recorded margin **and** Jev's median latency over all attempted calls meets the recorded acceptable median.
- Else `JEV_DOES_NOT_BEAT_TABLE`.

`RUN_INVALID` is not a positive result, so issue 612 is not built on it.

## 5. Artifacts under `.dev/`

Proposed folder `.dev/experiments/611-jev-vs-keyword-table/` (name to be confirmed):

- `corpus.jsonl` (prompts, provenance, labels, basis, flags), `selection-criteria.md`, `labelling-record.md`
- `questions.md` (the single question file), `scoring-rule.md`
- `table-procedure.md`, `table-provenance.md`, `table-answers.jsonl`
- `decision-rule.md` (the gate record)
- runner and scorer code with `tests/` beside them
- `runs/<run-id>/jev-rows.jsonl`, `runs/<run-id>/run-record.md`
- `report.md`, `decision-record.md`

No file under `src/` changes; no file holds the key.

## 6. Test obligations (offline, no live API)

Tests run with `uv run pytest` against a fake client; any network attempt fails the test.

- T-01: gate refuses when the record is missing or either required input is empty or `PENDING`.
- T-02: gate refuses on any hash mismatch.
- T-03: Noul exactly at 0.3 and 0.7, and just either side of each, maps as the scoring rule states.
- T-04: each FR-015 failure kind becomes `error`, never `none-fit` or abstention, and stays in the denominator.
- T-05: a unique performance cue, an ambiguous "leak" prompt and a none-fit prompt score correctly against their labels.
- T-06: synthetic latencies give the expected median (odd and even counts) and slowest values, with and without failures.
- T-07: the cost guard stops before a call that would pass the cap.
- T-08: a fake key never appears in any written artifact or captured output.
- T-09: paired breakdown and disagreement list match hand-built rows.
- T-10: each verdict branch, including `RUN_INVALID`, is reached from synthetic inputs.

## 7. Risks and mitigations

- Labels written by reading keywords mirror the table: FR-003 basis, FR-004 blindness.
- Table tuned on some corpus prompts inflates its score: FR-005 flag and split report.
- On about 30 prompts a few prompts decide the outcome: FR-020 paired breakdown; owner fixes the margin before the run.
- Manual table application drifts toward the label: FR-010, FR-011 procedure, blindness, per-row cues.
- Skill execution runs a stale copy: FR-009 copy path and execution evidence.
- Failures counted as "no" make Jev look cautious: FR-015, FR-018, T-04.
- Retries or reruns until results look good: FR-016, NFR-005.
- Rule edited after results: gate-record hashes and timestamps.
- Key leaks via logs, or price differs from quote: NFR-003, T-08, NFR-001 guard.

## 8. Open questions

- The margin Jev must win by: PENDING from the owner; required gate input.
- The acceptable median latency: PENDING from the owner; required gate input.
- Whether 0.3 and 0.7 themselves count as not settled.
- Whether the owner accepts FR-018 (errors count as not correct) and FR-016 (no retries).
- Whether the latency check uses all attempted calls (this spec) or successful calls only.
- Table method: manual application or skill execution; and whether labeller and table applier must be different people.
- Whether `RUN_INVALID` leaves issue 612 open or closes it.
- Final folder name, and whether the runner is a repository script or a manual sequence under NFR-003.
