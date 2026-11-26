# Diff Analysis: requirements spec comparison

## Metadata

- Generated: 2026-11-26T14:15:00+00:00
- Variants compared: 3 (blind labels A, B, C; files under `blind/`)
- Source: `.dev/brainstorms/20261126-jev-vs-keyword-table-611/seed-brief.md`
- Total differences found: 22
- Categories: structural (3), content (10), contradictions (2), unique (9), shared assumptions (5 promoted)
- Blind check: no model or persona name appears in the blind copies (the one grep hit on the word "superclaude" is a file path).

Variant key: A = numbered FR-001 to FR-024, 10 tests (T-01 to T-10), tables; B = numbered FR-001 to FR-018, 13 tests, one-job-per-file folder; C = bold-titled FR-001 to FR-010, tests as bullets without IDs.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | Section numbering and NFR layout | Numbered sections 1 to 8; NFR as NFR-001 to NFR-005 | Numbered 1 to 8; NFR grouped under Cost, Privacy and key secrecy, Reproducibility, Maintainability | Unnumbered headings; NFR as four bold bullets | Low |
| S-002 | Risks presentation | Two-column table | Two-column table | One prose paragraph | Low |
| S-003 | Test obligation traceability | T-01 to T-10 each tied to behaviour | T-01 to T-13, each cites the FR it checks | Seven unnumbered bullets, no FR links | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|---|---|---|---|---|
| C-001 | How labels avoid copying the table's own rule | Label basis drawn from the problem's real nature (for example its public fix), not from keywords; labeller sees no arm output (FR-003, FR-004) | Labeller and date recorded; no rule about how the basis is chosen (FR-001) | Named human labeller, written instructions, rationale for hard cases (FR-002) | Medium |
| C-002 | Verdict names and states | `JEV_BEATS_TABLE`, `JEV_DOES_NOT_BEAT_TABLE`, `RUN_INVALID` | `jev-clearly-beats-table`, `not-clearly`, `run-incomplete` | "clearly beats" or inconclusive for an incomplete or invalid run; no fixed names | Low |
| C-003 | Basis of the latency number in the decision rule | Median over all attempted calls (failures at measured or timeout time); also reported over successful calls | "Median latency within Input B"; basis not stated | Latency calculation is left to the frozen rule | Medium |
| C-004 | What the run gate checks | Record exists, both numbers present and not PENDING, lead confirms a restatement of both as comparisons, hashes match, timestamps precede the run | Rule file filled, bounds, error and retry treatment stated, hashes match manifest, table answers already stored, worst-case spend passes | Verbatim inputs, confirmed interpretation, frozen labels and rule, digests, order, public-only review, model pin, budget safeguard; pass or fail result persisted | Medium |
| C-005 | Who decides how an error call counts in accuracy | Spec decides: an error is not correct and stays in the denominator (FR-018) | Rule file decides before scoring; scorer has no default (FR-012) | Pre-run document decides (FR-006) | Medium |
| C-006 | Retry policy | No retries in the scored run | No automatic retry; optional policy written in the rule file, each retry counts against the cap | Retry policy documented before the run; retries separately visible and counted against the cap | Low |
| C-007 | Spend guard shape | Before each call, spend so far plus worst case of one more call must fit the cap | Worst case for the whole run computed before the first call, plus a stop before the cap | Spend plus reserved outstanding liability plus an upper bound for the request; stop if it cannot be bounded | Medium |
| C-008 | Key secrecy controls | Runner refuses to write any artifact holding the key; fake-key test | Redaction before storage; post-run scan of the whole folder for the key | Only a "credential available" status is recorded; key never in arguments, logs, errors or request dumps | Low |
| C-009 | Experiment folder name | `.dev/experiments/611-jev-vs-keyword-table/` | `.dev/research/jev-vs-keyword-table-611/` | Left open | Low |
| C-010 | How the owner's two numbers are turned into a rule | Lead confirms the restatement means exactly the verbatim text; unclear unit or tie handling goes back to the owner | Unit is whatever the owner's words say; recorded in the rule file | Verbatim text kept beside a machine-readable reading; ambiguous, unitless or contradictory input blocks the gate | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|---|---|---|---|---|
| X-001 | Whether a retry may happen in the scored run | "This spec requires no retries in the scored run" | No automatic retry; a retry policy is allowed if written before the run | Retries allowed if documented, visible and counted | Medium |
| X-002 | Whether the spec itself may fix how errors score | Yes, fixes it, then asks the owner to accept it as an open question | No, the scorer must take it from the rule file with no built-in default | No, a pre-run document must set it | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | Flag any prompt that also appears in `tests/troubleshoot/`, the skill text or the #871 observations as `seen-by-table`, and report accuracy with and without those prompts | High |
| U-002 | A | Paired breakdown: both right, only Jev, only table, neither, so the reader sees how many prompts a difference rests on | Medium |
| U-003 | A | Verdict `RUN_INVALID` when a frozen file changed, the run stopped at the cap, a gate condition was missing, or table provenance is absent | Medium |
| U-004 | A | Table applier is blind to labels and Jev answers and records the cues and rows matched for each prompt; written rule for "no cue matched" and "cues from two rows" | High |
| U-005 | B | Table answers are all stored before any Jev call is made | High |
| U-006 | B | Scorer checks the corpus (all six types, one ambiguous, one none-fit, no duplicate ids, provenance present) and fails on a gap | Medium |
| U-007 | B | Append-only run ids, offline re-scoring under a different rule file, one README | Medium |
| U-008 | C | Dated event log: owner input received, freeze, rule freeze, gate approval, first request, run end, scoring, verdict, each linked to evidence | High |
| U-009 | C | Record the exact text posted to issues 611, 609 and 612 and their links; mark local table cost and timing apart from remote call measurements | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Enough real public `/sc:troubleshoot` prompts exist to build about 30, including real ambiguous and none-fit cases, and a public source can be named for each | All three require public provenance and coverage; none says where such prompts come from | High: without a source the corpus step cannot finish | UNSTATED, promoted |
| A-002 | TypeSafe accepts a Choice and a Noul in one request and returns a probability for every answer, a cost, and a model id that confirms `jev-1.14.0` | All three build a per-prompt record from those fields | High: the record schema fails if any field is missing | UNSTATED, promoted (state mechanics: response contract) |
| A-003 | One human's label is the ground truth; no second labeller is needed | All three treat the label as the answer key | Medium | UNSTATED, promoted |
| A-004 | Latency measured from this workspace's network is a fair stand-in for the latency a real pre-step would see | All three compare a measured median with the owner's number | Medium | UNSTATED, promoted |
| A-005 | Scorer and runner code kept under `.dev/` will be tested by someone: the repository's normal test run may not collect tests there | A and B put code and tests beside the data; C says offline scoring code is required | Medium: tests nobody runs prove nothing | UNSTATED, promoted |

## Summary

- Total structural differences: 3
- Total content differences: 10
- Total contradictions: 2
- Total unique contributions: 9
- Total shared assumptions surfaced: 5 (UNSTATED: 5, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: U-001, U-004, U-005, U-008, A-001, A-002
- Diff points counted for convergence: S 3 + C 10 + X 2 + A 5 = 20

Taxonomy tags (one per point): L1 surface: S-001, S-002, C-002, C-009. L2 structural: S-003, C-001, C-003, C-004, C-010, U-001 to U-009 (as unique items, not scored). L3 state mechanics: C-005, C-006, C-007, C-008, X-001, X-002, A-002. Points A-001, A-003, A-004, A-005 are tagged L2.

Similarity check: not triggered. The variants differ on well over 10% of comparable points.
