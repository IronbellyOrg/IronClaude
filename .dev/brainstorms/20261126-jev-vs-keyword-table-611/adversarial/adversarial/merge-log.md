# Merge Log

- Base: Variant A (`blind/variant-A.md`)
- Plan: `refactor-plan.md`, 27 changes plus the "Changes NOT Being Made" table; plan status auto-approved (non-interactive run), 2026-11-26T14:40:00+00:00
- Sources: Variant B (`blind/variant-B.md`), Variant C (`blind/variant-C.md`), `invariant-probe.md`, `.dev/issues/611/issue-summary.md` (sections "Proposal received", "This agent's answer", "Decision rule as it stands")
- Output: `../merged-output.md` (the brainstorm's `adversarial/merged-output.md`)
- Merge date: 2026-11-26

## Input note

The seed brief was not at the stated path `adversarial/seed-brief.md`. The only seed brief in the brainstorm folder is `20261126-jev-vs-keyword-table-611/seed-brief.md`, one level up; that file was used.

## Id map (old Base id to merged id)

- FR: A FR-001 to FR-011 keep their ids; new FR-012 (table answers); A FR-012 to FR-022 become FR-013 to FR-023; new FR-024 (rescore); A FR-023 becomes FR-025; A FR-024 becomes FR-026.
- NFR: A NFR-001 stays NFR-001; new NFR-002 (ledger); A NFR-002 to NFR-005 become NFR-003 to NFR-006; new NFR-007 and NFR-008 (Variant B NFR-010, NFR-011).
- Tests: A T-01, T-02 keep ids (T-01 rewritten); new T-03 (Variant B T-04) and T-04 (Variant B T-01); A T-03 to T-10 become T-05 to T-12; new T-13 (Changes #20, #24) and T-14 (Variant B T-11, T-12).
- Files: Base `scoring-rule.md` and the gate-record role of `decision-rule.md` merge into one rule file `decision-rule.md`; gate results move to `events.jsonl`; hashes move to `manifest.json`.

## Per-change status

| # | Status | Before (Base) | After (merged) |
|---|---|---|---|
| 1 | applied | Section 5: `.dev/experiments/611-jev-vs-keyword-table/`, name to be confirmed | Section 5: `.dev/research/jev-vs-keyword-table-611/`, with the `.dev/README.md` reason |
| 2 | applied | FR-016: "This spec requires no retries in the scored run" | FR-017: one rerun per failed prompt, never a whole-run rerun, every attempt logged and counted, failed attempt visible; FR-014 makes each attempt a row |
| 3 | applied | Band operators and error treatment in the spec and `scoring-rule.md` | `decision-rule.md` holds band operators, error and rerun treatment, latency, margin test, validity; scorer has no default (FR-015, FR-019, section 4.1); Base error text is the content |
| 4 | applied | Section 4: margin and median PENDING, no rule content | Section 4.2: the proposed rule exactly as Change #4 lists it, marked PROPOSED, relayed and not the owner's words, no value decided, gates closed until AGREED with who and when |
| 5 | applied | FR-019: median and slowest over all attempts and over successes | FR-020: decision figures from the rule file, Base's two bases reported beside them, 90th percentile, local versus remote labels; twice-failed median left open (section 8) |
| 6 | applied | One gate record with six items | Gate 1 (section 4.3, before table or Jev) and Gate 2 (section 4.4, before first live call) |
| 7 | applied | No event log | Section 4.5 `events.jsonl`, append-only, each event linked to evidence, first request references the manifest |
| 8 | applied | No timing rule for table answers | FR-012: table answers after Gate 1, all stored before any Jev call |
| 9 | applied | FR-002 coverage stated, not checked | FR-002: scorer's corpus check fails on missing type, no ambiguous, no none-fit, duplicate id, missing provenance; T-04 |
| 10 | applied | NFR-005 single scored run only | FR-024 non-decisional offline rescore; NFR-006 append-only run ids; T-14 |
| 11 | applied | NFR-001: worst-case of one more call | NFR-001: verified per-request upper bound (reruns included), stop if no bound, whole-run estimate as second check, one call at a time, no liability reservation |
| 12 | applied | NFR-003: refuse-to-write only | NFR-004: layers (a) refuse to write, (b) redact and folder scan, (c) minimise |
| 13 | applied | T-01 to T-10 with no requirement cites | T-01 to T-14, each citing its FR, NFR or section; Variant B tests merged. Change #24 lists no tests by name, so T-13 was written to cover its three conditions |
| 14 | applied | Flat NFR list; risks as bullets | NFRs grouped under Cost, Privacy and key secrecy, Reproducibility, Maintainability; risks as a table. The Maintainability group takes Variant B NFR-010 and NFR-011 as NFR-007 and NFR-008 |
| 15 | applied | FR-023: `JEV_BEATS_TABLE`, `JEV_DOES_NOT_BEAT_TABLE`, `RUN_INVALID` | FR-025: `JEV_BEATS_TABLE`, `NOT_CLEARLY`, `RUN_INVALID` with a reason field; Base invalid reasons kept in section 4.7 |
| 16 | applied | Gate item 6: restatement confirmed by the lead | Section 4.1 item 3 and Gate 1 item 2: verbatim words beside the machine reading; unclear unit, denominator or tie fails Gate 1 and goes back to the owner |
| 17 | applied | FR-001: provenance only | FR-001: public sources and achieved counts per label listed before the freeze; shortfall reported to the lead, never padded |
| 18 | applied | FR-024: record to coordinator, no GitHub write | FR-026: posts nothing; record carries exact text and target issues 611, 609, 612; coordinator's text and links added afterwards |
| 19 | applied | No rule on who sets the rule status | Section 4.1 items 1 and 2: who agreed, verbatim words, date; refuse non-AGREED; relayed words recorded as relayed; Gate 2 item 7: lead's go naming the rule hash, quoted in the event log |
| 20 | applied | Table answers not hashed | FR-012 and NFR-005: hashed at storage, checked before scoring; change after first Jev result is `RUN_INVALID` (section 4.7) |
| 21 | applied | NFR-004 hashes the runner only | NFR-005: scorer and runner hashes and commit in the manifest, folder committed, `uv run pytest <path> -v` result recorded before Gate 2; Gate 2 item 3 |
| 22 | applied | FR-011: applier blind to labels and Jev | FR-011: prompts only, different person or session from the labeller, AI session told to follow the prose, cue record kept |
| 23 | applied | FR-003: basis from the problem's nature | FR-003: ambiguous and none-fit basis written before any arm and not from the table's two-row rule; split accuracy; flag a pass resting only on that group |
| 24 | applied | `RUN_INVALID` for frozen-file change, cap stop, missing gate, missing provenance | Section 4.7 adds key rejected, returned model id differs, unresolved failures over a rule-file count (no number set); no build or close decision on 612 |
| 25 | applied | NFR-005: "a rerun needs a reason" (whole-run meaning) | NFR-002 one experiment-wide ledger across run ids; NFR-006 "rerun" means one per prompt, a new run needs a reason written first |
| 26 | applied | Duplicate ids only; band operators in the scoring rule; even-count median unstated | FR-002 same-text check; FR-015 operators before AGREED; section 4.1 item 7 and FR-020 one median population, even-count median, 90th-percentile method; FR-006 achieved count and new freeze on a swap |
| 27 | applied | FR-005 split; no gate-input status; old open questions | FR-005 kept; section 4.6 status table, all not yet passed on 2026-11-26; section 8 updated as planned |

"Changes NOT Being Made" table: honoured. No outstanding-liability reservation (C-007); the 10 s imputation is an open item only (C-003); "no retries" dropped (X-001); rescoring is non-decisional only (U-007); numbered layout kept (S-001); `research/` folder used (C-009).

## Edits made outside the 27 changes

1. Section 1 states the lead's decision already typed in (about 30 public prompts to TypeSafe on `TYPESAFE_API_KEY`, 1 dollar cap, public prompts only, key never printed or stored) and says it opens no gate. Reason: the orchestrator's hard rule (b) and the seed brief's "Known Context". Wording from Variant B section 1 and Variant C "Purpose and scope". Base gate item 4 (sending approval word for word) is kept as Gate 2 item 6.
2. Section 8: the Base question "Whether `RUN_INVALID` leaves issue 612 open or closes it" was removed, because Change #24 answers it (no build or close decision). The Base latency-basis question was folded into the latency item. Flagged for the orchestrator.
3. NFR-007: Variant B's "the three frozen files" became "the frozen files", because the merged spec freezes four (corpus, question file, rule file, table answers).
4. Section 7 mitigation references were renumbered. "Owner fixes the margin before the run" became "the margin test is fixed in the AGREED rule file before Gate 1", to match Change #19.
5. Section 5 names the ledger file `spend-ledger.jsonl`. Change #25 requires the ledger but names no file.

## Post-merge validation

**Heading hierarchy: pass.** One H1. Sections 1 to 8 are H2s in the Base order. H3s appear only under section 4 (4.1 to 4.7). No level is skipped.

**Internal references: pass.** FR-001 to FR-026, NFR-001 to NFR-008 and T-01 to T-14 are each defined once, with no gaps. Every FR, NFR and T id used in the text is defined. Every section reference (1, 4, 4.1 to 4.7, 5, 8) exists. Every "Gate 1 item n" (1, 4), "Gate 2 item n" (1 to 5, 7) and "section 4.1 item n" (1, 2, 3, 7) exists. NFR-010, NFR-011, T-12 and "section 3, 5, 7" in provenance comments are Variant B ids, named as such, not internal references.

**Hard rule (a): pass.** The 2 s, 5 s and 10 s values and the 0.05-equivalent integer test appear only inside the section 4.2 PROPOSED block. Section 4 opens with "This spec sets no value for the margin or the latency limits". Tests use stand-in values.

**New contradictions introduced: none found.** Pairs checked:
- FR-013 (another model name makes that row an `error`) against section 4.7 (a differing returned model id makes the run `RUN_INVALID`). Compatible: the row is an error and the run is invalid.
- FR-019 (an unresolved error stays in the accuracy denominator) against the proposed median over final answered attempts. These are different populations by design. The open item is in section 8.
- NFR-006 ("first complete run is scored") against FR-017 (rerun within the run). Compatible because "rerun" is defined per prompt.
- Gate 1 before table application against FR-002, FR-006 (selection and freeze before either arm). Same order.

**Watch items for the orchestrator (not contradictions inside the merged spec):**
- The source proposal's verdict line (issue-summary.md, "Anything else is 'not clearly'") maps an invalid run to "not clearly". The merged spec maps it to `RUN_INVALID` (Changes #15, #24). Change #4 does not carry that line into section 4.2, so the spec is consistent. Whoever marks the rule AGREED should know the two differ.
- The seed brief's success criterion says the margin and latency come "from" the owner. Per Change #19, the spec records who agreed and marks relayed words as relayed. It does not restrict who may mark AGREED. Whether a relayed proposal meets the seed brief's criterion is not settled by the spec.
- `events.jsonl` (section 4.5) has no dedicated test. The plan names none, and the Variant C test for event ordering is not part of Change #13's sources.

## Summary

- Planned: 27. Applied: 27. Partial: 0. Skipped: 0.
- Outside-plan edits: 5, listed above with reasons. Each is a consistency or orchestrator-directed edit.
- Merged spec size: 5,633 words by `wc -w`, provenance comments included. That is above the plan's estimate of about 4,000 words, which did not count the comments.
- Gate status recorded in the spec: closed. The rule is PROPOSED, and no gate input has passed as of 2026-11-26.
