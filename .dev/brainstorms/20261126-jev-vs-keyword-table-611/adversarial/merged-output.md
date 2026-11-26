---
title: "Requirements: Jev versus the keyword table on about 30 labelled public prompts (#611)"
type: spec
---

<!--
Provenance
- Base: Variant A (adversarial/blind/variant-A.md), combined score 0.9833
- Merged from: Variant B (adversarial/blind/variant-B.md) and Variant C (adversarial/blind/variant-C.md)
- Context for Changes #4 and #19 to #27: adversarial/invariant-probe.md; .dev/issues/611/issue-summary.md sections "Proposal received", "This agent's answer" and "Decision rule as it stands"
- Plan: adversarial/refactor-plan.md, 27 planned changes plus the "Changes NOT Being Made" table; plan status auto-approved (non-interactive run), 2026-11-26T14:40:00+00:00
- Merge date: 2026-11-26
- A, B and C are neutral variant labels.
-->

# Requirements: Jev versus the keyword table (#611)

## 1. Purpose and scope

<!-- Source: Base (original, modified) - "scoring rule" becomes "rule file" (Change #3); adds the lead's decision already typed in, as an input (seed brief "Known Context"; wording from Variant B section 1 and Variant C "Purpose and scope") -->

Measure whether Jev (TypeSafe, pinned `jev-1.14.0`) picks the `/sc:troubleshoot` problem type more accurately than the Wave 0 keyword table, on about 30 frozen, human-labelled public prompts, so that issue 612 is built or closed as not justified. Label leakage, small-sample noise, failure handling and table-arm provenance are requirements, not notes.

In scope: corpus, labels, question file, rule file, offline scorer and tests, one gated live run, report, decision record. Out of scope: a production preflight command or hook, gateway rewrite, depth or scope comparison, private repositories (issue 552), any change under `src/`, any edit to the table.

Decided by the lead on 2026-11-26 (an input, not an option): send about 30 public prompts to TypeSafe on the `TYPESAFE_API_KEY` key, with a 1 dollar spend cap, public prompts only. The key is never printed or stored. That decision does not set the margin Jev must win by or the acceptable median latency, and it does not open either gate in section 4.

Baseline: `origin/integration` at `37765a800d0b232cc231cf58b796fec23b26f8a8`; table file blob `76bcb3d94182371250ffe99a7b60b9124b05c368` (Wave 0, `SKILL.md` lines 152 to 159).

## 2. Functional requirements

<!-- Source: Base (original, modified) - ids renumbered FR-001 to FR-026 after new FR-012 (Change #8) and FR-024 (Change #10); old-to-new map in merge-log.md -->

**Corpus and labels**

<!-- Source: Base (original, modified) - FR-001 adds the source list and shortfall rule (Variant C FR-001, merged per Change #17); FR-002 adds the scorer's corpus check (Variant B FR-002, FR-003, merged per Change #9) and the same-text check (invariant probe INV-008, merged per Change #26) -->

- FR-001: Each of about 30 prompts records id, verbatim text, public source link or repository path, retrieval date and selection reason. A prompt without public provenance is rejected. Before the freeze, the public sources searched and the achieved count per label are listed; a shortfall in `ambiguous` or `none-fit` cases is reported to the lead and is never padded.
- FR-002: The corpus covers all six types plus at least one ambiguous and one none-fit case. Selection criteria are written before either arm classifies any prompt, so selection cannot follow arm outcomes. The offline scorer's corpus check fails on a missing type, no `ambiguous` entry, no `none-fit` entry, a duplicate id, the same prompt text under two ids, or a missing provenance.

<!-- Source: Base (original, modified) - FR-003 adds the basis rule for ambiguous and none-fit labels and the split report (invariant probe INV-014, merged per Change #23) -->

- FR-003: Each prompt has one label (one of the six types, `ambiguous`, or `none-fit`) and a one-line labelling basis drawn from the problem's actual nature (for example its public fix), not from which keywords appear, so labels do not encode the table's own rule. For an `ambiguous` or `none-fit` label, the basis is written before any arm runs and is not taken from the table's own rule for cues from two or more rows (FR-010). The report gives each arm's accuracy separately for typed prompts and for `ambiguous` or `none-fit` prompts, and flags a margin-test pass that rests only on the second group.

<!-- Source: Base (original) - FR-004 and FR-005 unchanged; FR-005 kept as reported both ways per Change #27 (INV-016) -->

- FR-004: The labeller has seen no table or Jev answer for the corpus. Labeller role and labelling date are recorded.
- FR-005: A prompt that also appears in `tests/troubleshoot/`, the skill text, or the #871 verification observations is flagged `seen-by-table`. Both arms' accuracy is reported with and without them.

<!-- Source: Base (original, modified) - hash moves from the gate record to `manifest.json` (Change #21); achieved count and new-freeze-on-swap from invariant probe INV-011, merged per Change #26 -->

- FR-006: Labels freeze before either arm runs; the corpus file's SHA-256 goes in `manifest.json` (NFR-005). The achieved prompt count is recorded at the freeze. A prompt swapped after table answers exist forces a new freeze.

**Question file**

<!-- Source: Base (original) -->

- FR-007: All Jev wording (the Choice over `bug`, `build`, `performance`, `deployment`, `security`, `test`, and the companion Noul asking whether any type fits) lives in one hashed file containing no corpus prompt, label or corpus-derived example.

**Table arm**

<!-- Source: Base (original) - FR-008 to FR-010 unchanged -->

- FR-008: The table is applied as written: keyword and structural cues, ambiguity leaves the type unset, "leak" stays in both performance and security. No first-match parser, normalisation or added inference.
- FR-009: The method (a person reading the prose table, or execution of the skill's Wave 0) is recorded before application. Execution records the exact skill copy path, revision, blob and evidence of which copy ran. Manual application is labelled manual, not runtime evidence.
- FR-010: A written procedure states, before application, how "no cue matched" and "cues from two or more rows" resolve, consistent with the ambiguity rule.

<!-- Source: Base (original, modified) - FR-011 separates applier from labeller and adds the AI-session instruction (invariant probe INV-013, merged per Change #22) -->

- FR-011: The table applier is given the prompts only, never the labels or Jev answers, and is a different person or session from the labeller. If an AI session applies the table, it is told to follow the prose as written. The applier records, per prompt, the cues and rows matched, and that cue record is kept.

<!-- Source: Variant B FR-009 and section 4 gate step 4 - merged per Change #8; hash and freeze from invariant probe INV-002, merged per Change #20 -->

- FR-012: Table answers are produced only after Gate 1 passes (section 4.3), and all of them are stored in `table-answers.jsonl` before any Jev call. The file is hashed into `manifest.json` when stored, and the hash is checked before scoring; a change to it after the first Jev result makes the run `RUN_INVALID` (section 4.7).

**Jev arm**

<!-- Source: Base (original, modified) - FR-013 renumbered from FR-012 unchanged; FR-014 records every attempt (Variant B FR-016, Variant C FR-006, merged per Change #2); FR-015 reads the band from the rule file (Variant B FR-011, merged per Change #3; operators before AGREED per Change #26, INV-009); FR-016 renumbered from FR-015 unchanged -->

- FR-013: One request per prompt, the same prompt bytes the table arm received, model `jev-1.14.0` named explicitly. A response naming any other model is an error.
- FR-014: Each attempt, a rerun included, is its own row recording attempt number, Choice answer, probability of every returned answer, Noul value, client latency (monotonic clock, send to full response), cost and status.
- FR-015: Noul above the not-settled band: type is the Choice answer. Below it: unset, reason `none-fit`. Inside it: unset, reason `not-settled`. The rule file (`decision-rule.md`, section 4.1) states the band with explicit operators at 0.3 and 0.7 before it is marked `AGREED`. The scorer reads the band from the rule file and has no built-in default.
- FR-016: A transport error, timeout, malformed body, missing Choice or Noul, Choice outside the six values, or wrong model is status `error`, never mapped to "no", `none-fit` or abstention.

<!-- Source: Base (original, modified) - "no retries in the scored run" replaced by the pre-written rerun policy (Variant B FR-016, Variant C FR-006, merged per Change #2); policy lives in the rule file per Change #3 -->

- FR-017: The rerun policy and the per-call timeout are written in the rule file before it is marked `AGREED`. The policy: a failed prompt gets one rerun, never a rerun of the whole run; every attempt is logged and counts against the cap (NFR-001); the failed attempt stays visible in the rows and the report. A prompt is scored on its final attempt. A prompt whose rerun also fails has an unresolved error (FR-019).

**Scoring and report**

<!-- Source: Base (original, modified) - FR-018 renumbered from FR-017 unchanged; FR-019 makes the Base error text the rule-file content (Variant B FR-012, merged per Change #3) -->

- FR-018: Correct means a typed label matched by the same type, or an `ambiguous` or `none-fit` label matched by an unset type. Unset on a typed label is incorrect and counted as an abstention.
- FR-019: The accuracy denominator is every prompt in the frozen corpus. The rule file states the error treatment and the scorer takes it from there, with this content: an unresolved error is not right and stays in the denominator. Errors are also reported as a count and rate, with first-attempt failures and reruns shown.

<!-- Source: Base (original, modified) - FR-020 keeps the Base's two latency bases, aligns the decision figures to the rule file, adds the 90th percentile and local-versus-remote labels (Variant C FR-008, merged per Change #5); one median population and method from invariant probe INV-010, merged per Change #26 -->

- FR-020: Per arm: correct count, accuracy, abstentions by reason, errors. For Jev also: total cost, and latency as follows. (a) The decision figures are computed exactly as the rule file defines them (section 4.1 item 7); the rule file names one population for the decision median, the median of an even count, and the 90th-percentile method. (b) Reported beside them, the median and slowest latency over all attempted calls (failures at measured or timeout time) and over successful calls. (c) The 90th percentile. Table-arm timing and cost are labelled local and Jev's remote; unmeasured latency is never shown as zero. The median treatment of a prompt that fails twice is open (section 8).

<!-- Source: Base (original) - FR-021 to FR-023 renumbered from FR-020 to FR-022 unchanged -->

- FR-021: Paired breakdown: prompts both arms got right, only Jev, only the table, neither, showing how many prompts any difference rests on.
- FR-022: Every disagreement is listed with prompt id, label, both answers, Jev probabilities and Noul.
- FR-023: All aggregates are recomputed by the scorer from retained rows; none is hand-entered.

<!-- Source: Variant B FR-018, NFR-008 and T-12 - merged per Change #10; non-decisional label per Change #10 and the "Changes NOT Being Made" row U-007 -->

- FR-024: The scorer can rescore any stored run offline under another rule file. A rescore writes a new, separately named report labelled non-decisional, never edits the original files, and never replaces the original verdict.

**Decision**

<!-- Source: Base (original, modified) - FR-025 uses three verdict states (Variant C, debate C-002, merged per Change #15); FR-026 adds the exact-text handoff and the coordinator's links afterwards (Variant C FR-010, merged per Change #18) -->

- FR-025: The verdict is computed mechanically (section 4.7) as one of three states: `JEV_BEATS_TABLE`; `NOT_CLEARLY` (a valid run where the rule is not met); or `RUN_INVALID`, with a reason field naming the condition that made it invalid.
- FR-026: This work posts nothing to GitHub. The decision record (verdict, inputs, hashes, report path) goes to the coordinator and carries the exact text to post and the target issues (611, 609 and 612). The coordinator's posted text and links are added to the decision record afterwards.

## 3. Non-functional requirements

<!-- Source: Base (original, modified) - grouped under Cost, Privacy and key secrecy, Reproducibility and Maintainability (Variant B section 3, merged per Change #14); ids renumbered NFR-001 to NFR-008 -->

**Cost**

<!-- Source: Base (original, modified) - NFR-001 per-request bound from Variant C "Cost cap" and whole-run check from Variant B NFR-002, merged per Change #11 (no concurrent-request reservation, per "Changes NOT Being Made" row C-007); NFR-002 from invariant probe INV-004 and INV-005, merged per Change #25 -->

- NFR-001 Spend cap: total spend at or under 1 dollar (the lead's cap, section 1). Calls are sent one at a time. Before each request, a rerun included, the runner checks that a verified upper bound of that request's cost plus spend so far fits within the cap; if no bound can be shown, it stops before sending and records the stop. As a second check, before the first call the runner computes the worst-case spend of the whole run, reruns included, and refuses to start if it exceeds the cap. Price is checked at execution time; the issue's 0.00004 dollars per call is an estimate, not a verified bound.
- NFR-002 One ledger: one cumulative spend ledger covers the whole experiment and carries across run ids, so the cap applies to the experiment, not to each run. Spend from a stopped or interrupted run stays in the ledger.

**Privacy and key secrecy**

<!-- Source: Base (original, modified) - NFR-003 renumbered from NFR-002, with the new-freeze cross-reference (Change #26, INV-011) -->

- NFR-003 Privacy: public prompts only. A prompt containing a credential-shaped string or personal data is excluded and replaced, not edited, so both arms see verbatim public text. A replacement after table answers exist forces a new freeze (FR-006).

<!-- Source: Base (original, modified) - NFR-004 renumbered from NFR-003; layer (a) Base, layer (b) Variant B NFR-004 to NFR-006, layer (c) Variant C "Key secrecy", merged per Change #12 -->

- NFR-004 Key secrecy: `TYPESAFE_API_KEY` is read from the environment only inside the runner process, at call time, held in memory, and sent only in the request's authorization header. Three layers apply:
  - (a) Refuse to write: the key is never printed, logged, written to a file, passed on a command line, or put in issue or pull request text. The runner refuses to write any artifact containing the key value.
  - (b) Redact and scan: error text and any stored response text pass through a redaction step before storage. After the run, an offline check scans every file in the experiment folder for the key, using the runner's in-memory value and a pattern, never by printing the key, and fails on a match. No shell history, command echo or debug trace holds the key.
  - (c) Minimise: artifacts record only whether a credential was available, never any part of it. Offline tests never read the real environment or the key.

**Reproducibility**

<!-- Source: Base (original, modified) - NFR-005 renumbered from NFR-004; manifest from Variant B NFR-007; table-answer hash per Change #20 (INV-002); scorer and runner pin, commit and recorded test command per Change #21 (INV-003) -->

- NFR-005 Pinned inputs: `manifest.json`, written before the first live call, holds the baseline revision and table blob; the SHA-256 of the corpus, the question file, the rule file, `table-answers.jsonl` (FR-012), the scorer and the runner; and the git commit in which the scorer and runner were committed. The experiment folder is committed before the run. The test command `uv run pytest <path> -v`, with the path to the folder's tests, and its passing result are recorded before Gate 2, because tests under `.dev/` are not collected by the repository's normal test run. Each run record holds the requested pin and returned model id, the timestamp of the first call, and the manifest's hash. The scorer is deterministic.

<!-- Source: Base (original, modified) - NFR-006 renumbered from NFR-005; "rerun" defined per Change #25 (INV-005); append-only run ids from Variant B NFR-008, merged per Change #10; rerun wording aligned per Change #2 -->

- NFR-006 Single scored run: the first complete run is scored. In this spec "rerun" means only the one rerun of a failed prompt (FR-017). A whole new run needs a reason written before it starts, gets a new run id, and draws on the same ledger (NFR-002). Result files are append-only per run id and nothing is overwritten. Every run is reported; no best-of-N selection.

**Maintainability**

<!-- Source: Variant B NFR-010 and NFR-011 - merged per Change #14 (Maintainability group); "the three frozen files" became "the frozen files" because the merged spec freezes four -->

- NFR-007 Small code: one runner, one scorer, and one shared loader for the frozen files; no abstraction beyond that.
- NFR-008 One job per file: each file in the folder has one job (section 5), so a reader can re-judge the decision from the folder alone, without the chat history.

## 4. Run gate and decision rule

<!-- Source: Base (original, modified) - the single gate is replaced by two gates (Variant C "Run gate and decision rule" and Variant B section 4 gate order, merged per Change #6); rule file per Change #3; proposed rule per Change #4 -->

No prompt goes to TypeSafe, and the table is not applied, until the gates below pass. Both gates stay closed until `decision-rule.md` is marked `AGREED` with who agreed and when. This spec sets no value for the margin or the latency limits.

### 4.1 The rule file

<!-- Source: Variant B FR-011, FR-012 and NFR-007 - merged per Change #3; status and acceptance fields from invariant probe INV-001, merged per Change #19; words kept beside the machine reading from Variant C "Run gate and decision rule" and Base section 4 item 6, merged per Change #16; required contents per Change #26 (INV-009, INV-010) and Change #24 (INV-017) -->

`decision-rule.md` is the single rule file. It is frozen and hashed into the manifest (NFR-005). The scorer reads every rule value from it and has no built-in default. It holds:

1. Status: `PROPOSED` or `AGREED`. The scorer and both gates refuse any status other than `AGREED`.
2. For `AGREED`: who agreed, their words verbatim, and the date and time. Words relayed on another person's behalf are recorded as relayed, with who relayed them; a relayed proposal is not the owner's words.
3. The margin test and the latency limits, each as the verbatim words received, kept beside the machine-readable comparison the scorer applies, with the lead's confirmation that the reading means exactly the words. If the words leave the unit (count of prompts or share), the denominator or tie handling unclear, Gate 1 fails, the question goes back to the owner, and the answer is recorded word for word.
4. The definition of right (FR-018).
5. The Noul band with explicit operators at 0.3 and 0.7 (FR-015).
6. The error and rerun treatment and the per-call timeout (FR-017, FR-019).
7. How latency is measured: the one population the decision median is taken over, the median of an even count, and the 90th-percentile method (FR-020).
8. The validity conditions for `RUN_INVALID` (section 4.7), including the count of unresolved failures above which a run is invalid. This spec sets no number for that count.

### 4.2 Proposed rule content (status: PROPOSED)

<!-- Source: .dev/issues/611/issue-summary.md "Decision rule as it stands", read with "Proposal received" and "This agent's answer" - merged per Change #4; provenance wording per Change #19 (INV-001) -->

> **PROPOSED, not agreed.** This block records a proposal so the rule file has content to accept or replace. It was relayed on 2026-11-26 by another session on the owner's behalf; it is not the owner's own words, and the lead may replace it at any time by typing the owner's own words. This spec names no value below as decided. The gates stay closed until `decision-rule.md` is marked `AGREED` with who agreed and when.

Proposed content:

- Right: a typed label is right when the answer is the same type; an `ambiguous` or `none-fit` label is right when the answer is unset. The same holds for both arms.
- Margin: an exact one-sided sign test on the prompts where only one arm is right. With b the prompts only Jev gets right and c the prompts only the table gets right (FR-021), the tail count is the sum of C(b+c, k) for k from b to b+c. Jev passes the margin test when 20 times the tail count is below 2 to the power b+c, computed in integer arithmetic.
- Latency: a median of 2 seconds or less over each prompt's final answered attempt; a slowest call of 5 seconds or less over all attempts, a call that times out counting at its timeout value; a per-call timeout of 10 seconds; the 90th percentile reported.
- Jev must pass both the margin test and the latency limits.

Not in the proposal, and required in the rule file before it can be marked `AGREED` (section 4.1): the Noul band operators at 0.3 and 0.7, the even-count median and 90th-percentile method, and the unresolved-failure count for `RUN_INVALID`. The median treatment of a prompt that fails twice is an open question (section 8).

### 4.3 Gate 1: before the table is applied or any Jev call

<!-- Source: Variant C "Run gate and decision rule" and Variant B section 4 gate order - merged per Change #6; verbatim words and unclear-unit rule per Change #16; AGREED fields per Change #19; Base section 4 items 3, 5 and 6 kept -->

All must hold, checked by code:

1. `decision-rule.md` exists, its status is `AGREED`, and it records who agreed, their verbatim words, and the date and time (section 4.1 items 1 and 2).
2. The margin and latency words are recorded verbatim beside their machine reading and confirmed by the lead, and nothing about unit, denominator or tie handling is unclear (section 4.1 item 3).
3. The rule file states every item in section 4.1.
4. Corpus and labels are frozen (FR-006), the corpus check passes (FR-002), and the corpus, question file and rule file hashes in the manifest match the files on disk.

### 4.4 Gate 2: before the first live call

<!-- Source: Variant B section 4 gate steps 4 and 5 and Variant C "Run gate and decision rule" - merged per Change #6; lead's go per Change #19 (INV-001); pinned and tested scorer per Change #21 (INV-003); Base section 4 item 4 and the runner refusal kept -->

All must hold, checked by code, after Gate 1:

1. Gate 1 still holds and its hashes still match the files on disk.
2. All table answers are stored and hashed (FR-012).
3. The scorer and runner are pinned and their tests pass (NFR-005).
4. The spend bound is verified: the whole-run worst case fits the cap, and the price used for the per-request bound was checked at execution time (NFR-001).
5. The response contract is checked: the fields FR-014 needs and the returned model id are confirmed at execution time, not assumed from earlier work.
6. The lead's sending decision (section 1) is recorded word for word, with when it was recorded and who typed it.
7. The lead has typed an explicit go in the terminal naming the rule file's hash, and the go is quoted in the event log (section 4.5).

The runner opens no network connection unless both gates pass and the gate timestamps precede the run. Otherwise it exits with a named refusal and sends nothing.

### 4.5 Gate result and event log

<!-- Source: Variant C FR-003 and FR-009 - merged per Change #7 -->

`events.jsonl` is append-only. Each event has a timestamp and a link to its evidence (file and hash): owner input received, corpus and label freeze, rule freeze, each gate result (pass or fail, with the failing item named), the lead's go (quoted), first request, run end or stop, scoring, and verdict. The first-request event references the manifest by hash, so a reader can establish the order without trusting a later narrative.

### 4.6 Gate inputs and their status

<!-- Source: invariant probe INV-018 - merged per Change #27 -->

The gate results in `events.jsonl` show each gate input as passed, with its evidence, or list it as not yet passed. As of 2026-11-26 none has passed:

| Gate input | Status on 2026-11-26 |
|---|---|
| Rule file `AGREED` (Gate 1 item 1) | Not yet passed: the rule is PROPOSED (section 4.2) |
| Corpus and labels frozen (Gate 1 item 4) | Not yet passed: no corpus or labels exist |
| Table method and answers (FR-009, Gate 2 item 2) | Not yet passed: the method is open (section 8) |
| Scorer and runner pinned and tested (Gate 2 item 3) | Not yet passed: no passing test result is recorded |
| Spend bound and price (Gate 2 item 4) | Not yet passed: the price is unverified |
| Response contract (Gate 2 item 5) | Not yet passed: unverified |
| Lead's go (Gate 2 item 7) | Not yet passed |

### 4.7 Decision rule and verdict

<!-- Source: Base (original, modified) - three verdict states (Variant C, debate C-002, merged per Change #15); Base RUN_INVALID reasons kept and extended per Change #20 (INV-002) and Change #24 (INV-017); rescore rule per Change #10 -->

Fixed before the run and not changed after results are seen:

- `RUN_INVALID`, with the reason recorded, if any of these holds: a frozen file changed after hashing, including `table-answers.jsonl` changed after the first Jev result; the run stopped at the cap before all prompts; a gate condition was missing; the table provenance record (FR-009) is absent; the key was rejected; a returned model id differs from the pin; or unresolved failures exceed the count the rule file states.
- Else `JEV_BEATS_TABLE` only if Jev passes both the margin test and the latency limits as the `AGREED` rule file states them.
- Else `NOT_CLEARLY`.

`RUN_INVALID` is not a result for either arm: no build or close decision on issue 612 is made from it. A rescore under another rule file (FR-024) is non-decisional and never replaces the verdict.

## 5. Artifacts under `.dev/`

<!-- Source: Base (original, modified) - folder name from Variant B section 5, merged per Change #1; `decision-rule.md` is the rule file and absorbs the Base `scoring-rule.md` and gate record (Change #3); `manifest.json` per Changes #20 and #21 (Variant B NFR-007); `events.jsonl` per Change #7; spend ledger per Change #25; append-only runs and rescores per Change #10; commit before the run per Change #21 -->

Folder: `.dev/research/jev-vs-keyword-table-611/` (`.dev/README.md` lists `research/` and not `experiments/`):

- `corpus.jsonl` (prompts, provenance, labels, basis, flags), `selection-criteria.md` (criteria, public sources searched, achieved count per label, FR-001), `labelling-record.md`
- `questions.md` (the single question file)
- `decision-rule.md` (the rule file, section 4.1)
- `manifest.json` (hashes and commit, NFR-005)
- `events.jsonl` (gate results and event log, section 4.5)
- `spend-ledger.jsonl` (the experiment's cumulative spend, NFR-002)
- `table-procedure.md`, `table-provenance.md` (method and per-prompt cue record, FR-009, FR-011), `table-answers.jsonl` (FR-012)
- runner and scorer code with `tests/` beside them
- `runs/<run-id>/jev-rows.jsonl`, `runs/<run-id>/run-record.md` (append-only per run id, NFR-006)
- `report.md`, `decision-record.md`; a rescore writes a new, separately named report labelled non-decisional (FR-024)

The folder is committed before the run (NFR-005). No file under `src/` changes; no file holds the key.

## 6. Test obligations (offline, no live API)

<!-- Source: Base (original, modified) - each test cites the requirement it checks (Variant B T-01 to T-13, merged per Change #13); T-13 covers Change #24 and Change #20; test command per Change #21; ids renumbered T-01 to T-14 -->

Tests run with `uv run pytest <path> -v` (NFR-005) against a fake client and hand-built fixtures. Any network attempt fails the test, and no test reads the real environment or `TYPESAFE_API_KEY` (NFR-004). Fixture rule files use stand-in values that are clearly not real owner values.

- T-01 (section 4.1; Gate 1 item 1): Gate 1 refuses when `decision-rule.md` is missing, its status is anything other than `AGREED` (including `PROPOSED` and `PENDING`), or who agreed, their words or the date is empty.
- T-02 (FR-006, FR-012, NFR-005; Gate 1 item 4, Gate 2 item 1): either gate refuses on any hash mismatch for the corpus, question file, rule file, table answers, scorer or runner.
- T-03 (section 4.4): with either gate failing, or with no lead's go naming the rule file's hash, the runner's HTTP function is never called (stubs that raise).
- T-04 (FR-002): the corpus check rejects a missing provenance, a missing type, no `ambiguous` entry, no `none-fit` entry, a duplicate id, and the same text under two ids.
- T-05 (FR-015): Noul exactly at 0.3 and 0.7, and just either side of each, maps as the rule file states, under each operator choice it can state; a rule file without the band is refused.
- T-06 (FR-016, FR-017, FR-019): each FR-016 failure kind becomes `error`, never `none-fit` or abstention; a failed attempt and its rerun both stay in the rows; a prompt whose rerun also fails is scored not right and stays in the denominator.
- T-07 (FR-018, FR-003): a unique performance cue, an ambiguous "leak" prompt and a none-fit prompt score correctly against their labels, for both arms alike; accuracy is split into typed and `ambiguous` or `none-fit` prompts, and a margin-test pass resting only on the second group is flagged.
- T-08 (FR-020): synthetic latencies give the expected median (odd and even counts), slowest and 90th-percentile values over the populations the rule file states, with and without failures, a timeout counting at its value.
- T-09 (NFR-001, NFR-002): the cost guard stops before a request, a rerun included, whose upper bound would pass the cap, and stops when no bound can be shown; a worst-case whole-run estimate over the cap refuses to start; the ledger carries spend from one run id to the next.
- T-10 (NFR-004): a fake key never appears in any written artifact or captured output; error text containing the fake key is redacted before storage; the folder scan flags a planted fake key in a fixture file.
- T-11 (FR-021, FR-022): the paired breakdown and the disagreement list match hand-built rows.
- T-12 (FR-025, section 4.7): each verdict state is reached from synthetic inputs, with boundary cases on both sides of the margin test and the latency limits, using stand-in rule values. The margin test is also checked against exact integer cases, with b the prompts only Jev gets right and c the prompts only the table gets right: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 FAILS (the tail is 56 of 1024, above 0.05), 9-2 passes, and b+c = 0 is "not clearly". A float computation must not be used at the 0.05 line. <!-- Source: Base (original, modified) - added after the 8-2 example in the relayed proposal was found to contradict its own formula (p 0.0547) -->
- T-15 (FR-021, FR-022): the smallest passing b for each c from 0 to 6 is 5, 7, 9, 10, 12, 13 and 15, and the scorer's pass or fail agrees with these cut-offs for every b and c up to 30.
- T-13 (section 4.7, FR-012, FR-013): a rejected key, a returned model id that differs from the pin, unresolved failures above the rule file's count, and a change to `table-answers.jsonl` after the first Jev result each give `RUN_INVALID` with that reason and no build or close decision.
- T-14 (FR-023, FR-024, NFR-005): the same rows and rule file give a byte-identical report twice; a rescore under a second rule file writes a new report labelled non-decisional and leaves the original files and verdict unchanged.

## 7. Risks and mitigations

<!-- Source: Base (original, modified) - laid out as a table (Variant B section 7, merged per Change #14); mitigation references renumbered and pointed at the merged requirements -->

| Risk | Mitigation |
|---|---|
| Labels written by reading keywords mirror the table | FR-003 basis, including the rule for `ambiguous` and `none-fit` labels; FR-004 blindness |
| Table tuned on some corpus prompts inflates its score | FR-005 flag and split report |
| On about 30 prompts a few prompts decide the outcome | FR-021 paired breakdown; the margin test is fixed in the `AGREED` rule file before Gate 1 (section 4) |
| Manual table application drifts toward the label | FR-010 procedure; FR-011 applier given the prompts only, separate from the labeller, per-row cues |
| Skill execution runs a stale copy | FR-009 copy path and execution evidence |
| Failures counted as "no" make Jev look cautious | FR-016, FR-019, T-06 |
| Retries or reruns until results look good | FR-017 one rerun per prompt; NFR-006 |
| Rule edited after results | Manifest hashes (NFR-005) and the event log (section 4.5) |
| Key leaks via logs, or price differs from quote | NFR-004, T-10, NFR-001 guard |

## 8. Open questions

<!-- Source: Base (original, modified) - updated per Change #27: the folder-name and retry questions removed; median treatment of a twice-failed prompt, unresolved-failure count, Noul boundary operators, table method and applier, and who labels added; margin and latency items point at the PROPOSED rule (Change #4); the RUN_INVALID-and-612 question removed because Change #24 answers it -->

- The margin Jev must win by: a proposal is recorded in section 4.2 as PROPOSED. It is not decided, and the gates stay closed until the rule file is `AGREED` with who agreed and when.
- The acceptable median latency and the slowest-call limit, and the basis each is measured on: a proposal is recorded in section 4.2 as PROPOSED. Not decided.
- Noul boundary operators: whether 0.3 and 0.7 themselves count as not settled. The proposal does not state them; the rule file must, before it is `AGREED`.
- Median treatment of a prompt whose first attempt and rerun both fail: the proposed median covers final answered attempts only, so such a prompt falls outside it. Counting it at its timeout value was raised as a new proposal and is not agreed.
- The count of unresolved failures above which a run is `RUN_INVALID` (section 4.7): no number is set here; the rule file must state it before it is `AGREED`.
- Whether the owner accepts FR-019 (an unresolved error counts as not right and stays in the denominator).
- Table method and applier: manual application or skill execution (FR-009), and which person or session applies the table (FR-011).
- Who labels (FR-004), and what the lead decides if the public sources fall short of `ambiguous` or `none-fit` cases (FR-001).
- Whether the runner is a repository script or a manual sequence under NFR-004.
