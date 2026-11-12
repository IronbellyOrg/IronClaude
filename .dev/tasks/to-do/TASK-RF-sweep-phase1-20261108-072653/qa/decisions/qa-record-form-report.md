# QA Report - Record-form lens (item 7.22)

**Reviewer:** rf-qa (report-only, fix_authorization: false)
**Date:** 2026-11-12
**Phase:** decisions gate, record-form lens
**Base path:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` (shortened to `PKG/` below)

## Checks

| Check | Description | Result |
|-------|-------------|--------|
| C1 | OQ-1 file: `needs_human_decision: false`, `status: RESOLVED`, no recommendation line, filled four decision lines quoting "Allow it, no conditions needed." | PASS |
| C2 | OQ-2 file: `needs_human_decision: true`, `status:`, question and options quoted, recommendation ends "This recommendation does NOT authorize adoption.", blocked steps, four decision lines | PASS |
| C3 | OQ-3 file: same parts as C2 | PASS |
| C4 | OQ-4 file: same parts as C2 | PASS |
| C5 | OQ-5 file: same parts as C2 | PASS |
| C6 | OQ-6 file: same parts as C2, with the no-recommendation sentence instead of a recommendation line | PASS |
| C7 | OQ-7 file: same parts as C2 | PASS |
| C8 | OQ-8 file: `needs_human_decision: true`, `status:`, request quoted, blocked steps, `Run id:` / `Given by:` / `Source:` filled, record says the Run holds at least one Dispatch row | PASS (MINOR note M1) |
| C9 | OQ-17 file (exists, folder listing): same parts as C2 | PASS |
| C10 | No OQ-18 file exists (so no OQ-18 row is owed) | PASS |
| C11 | `owner-decisions.md` has seven decision rows OQ-1 to OQ-7 | PASS |
| C12 | `owner-decisions.md` has one extra row for each resolved OQ-17 / OQ-18 file that exists (OQ-17 exists and is RESOLVED, so eight rows are owed) | FAIL |
| C13 | `owner-decisions.md` APPROVED table present, 13 rows, each cell identical to `.dev/orca-command-refactor/decisions/APPROVED.md` at the cited line | PASS |
| C14 | Owner quotes and `file:lines` ranges in `owner-decisions.md` rows 1-7 match the record files | PASS |
| C15 | OQ-6 record versus the narrow style override: record unchanged, `pragmatic.md:22` carries the scoped exception, no contradiction outside the override | PASS |

## Evidence by check

- C1: `PKG/phase-outputs/plans/OQ-1-agent-wait-decision.md:4-5` (`needs_human_decision: false`, `status: RESOLVED`), `:19-22` (OPERATOR DECISION, Chosen, Decided by, Decision source), quote at `:22`. The whole file (42 lines read) has no recommendation sentence.
- C2: `OQ-2-GQ-10-report-location-decision.md:2-3`, quoted question `:10`, options `:16-19`, recommendation `:23`, blocked work `:25-29`, decision lines `:33-36`.
- C3: `OQ-3-GQ-11-rule-id-decision.md:2-3`, question `:10`, options `:18-20`, recommendation `:26`, blocked `:28-32`, decision lines `:36-39`.
- C4: `OQ-4-GQ-35-409-pin-decision.md:2-3`, question `:10-16`, options `:24`, recommendation `:32`, blocked `:34-36`, decision lines `:40-43`.
- C5: `OQ-5-GQ-61-window-decision.md:2-3`, question `:10`, options `:16-19`, recommendation `:25`, blocked `:27-29`, decision lines `:33-36`.
- C6: `OQ-6-GQ-63-done-next-decision.md:2-3`, question `:10`, options `:16-18`, `## No recommendation` `:22-24` ending "does NOT authorize adoption.", blocked `:26-28`, decision lines `:32-35`.
- C7: `OQ-7-D9-signoff-decision.md:2-3`, question `:10-14`, options `:22-28`, recommendation `:32`, blocked `:34-36`, decision lines `:40-43`.
- C8: `OQ-8-run-id-decision.md:2-3`, request quoted `:10-16`, blocked `:20-22`, `Run id:` `:26`, `Dispatch rows: 5` `:27`, `Given by:` `:28`, `Source:` `:29`.
- C9: `OQ-17-cursor-template-decision.md:2-3`, question `:10-18`, options `:22-25`, recommendation `:29`, blocked `:31-33`, decision lines `:37-40`.
- C10: Glob of `PKG/phase-outputs/plans/OQ-*` returned nine files (OQ-1 to OQ-8 and OQ-17); no OQ-18.
- C11: `PKG/artifacts/owner-decisions.md:9-15` are seven rows: OQ-1, OQ-2, OQ-3, OQ-4, OQ-5, OQ-6, OQ-7.
- C12: see finding F1.
- C13: compared `owner-decisions.md:41-53` to `APPROVED.md` lines 10, 11, 12, 13, 20, 25, 29, 30, 35, 36, 47, 71, 90 (D3, D4, D5, GIT, L3, CR-01, PATHS, UPSTREAM, B1, B1-N1, S4, G1, F1). The decision cells match; the bracketed re-anchor notes in rows D4, GIT and UPSTREAM are additions to the last column only.
- C14: owner quotes match their records (OQ-2 `:36`, OQ-3 `:39`, OQ-4 `:43`, OQ-5 `:36`, OQ-6 `:35`, OQ-7 `:43`, OQ-1 `:22`); the cited `:lines` ranges point at the four decision lines in every record.
- C15: `OQ-6-GQ-63-done-next-decision.md:12` states the old "no exceptions" wording as history, and the prompt names that as the pre-7.10 anchor. `src/superclaude/output-styles/pragmatic.md:22` now holds "The only exception is the sweep chat-summary exception". `step-7.10-style-exception.md:33` says the OQ-6 record is "unchanged". `owner-decisions.md:19-33` keeps decision, revision and execution permission apart.

## Findings

### F1 - BLOCKING - `owner-decisions.md` has no row for the resolved OQ-17 decision

- Evidence: `PKG/artifacts/owner-decisions.md:5` ("Decisions (seven rows)") and `:9-15` hold rows OQ-1 to OQ-7 only. `PKG/phase-outputs/plans/OQ-17-cursor-template-decision.md:3` is `status: RESOLVED` and `:37-40` hold a filled decision (Chosen: refuse the cursor command, allowlist stays at 10; Decided by Ryan Wiancko, owner, 2026-11-11; owner words "Keep the 10 commands (Recommended)"). `PKG/phase-outputs/discovery/1.0a-facts.md:56` also records the OQ-17 answer. File times: `owner-decisions.md` was last written 2026-11-11 20:51; the OQ-17 file was last written 2026-11-11 22:28.
- What is wrong: this lens requires seven rows plus one row for each resolved OQ-17 or OQ-18 file that exists. OQ-17 exists and is resolved, so eight rows are owed and seven are present. `owner-decisions.md:55` still says OQ-17 is "Still open and not recorded here as decisions ... (only if step 1.0a fires them)", which is now false. The file went stale when item 7.17 fired the OQ-17 branch after item 7.13 had compiled it. The mechanical check C5 in `decisions-mechanical.md` only tests that the file is non-empty, so it did not catch this.
- Smallest fix: append one OQ-17 row to the decisions table in the same seven-column shape (ID `OQ-17 (cursor template)`; option chosen: refuse, keep the allowlist at exactly 10 templates; owner's words: "Keep the 10 commands (Recommended)"; decider: Ryan Wiancko, owner, 2026-11-11; source: `PKG/phase-outputs/plans/OQ-17-cursor-template-decision.md:37-40`; unblocks: item 7.17 and, with it, step 1.2 onward including the 8.10 and 10.3 template count). Then change the heading at `:5` to "eight rows", and rewrite `:55` to say OQ-17 is resolved (row added) and OQ-18 does not exist. Then re-run the row count.

### M1 - MINOR - OQ-8 has no options section

- Evidence: `OQ-8-run-id-decision.md:8-22`. The file is a request, not a choice between options, so there are none to quote. The lens exempts only the recommendation line for OQ-8. The options the owner was offered are summarized in the `Source:` line (`:29`).
- Fix (optional): none needed.

### M2 - MINOR - OQ-1 status lines sit in a yaml code block

- Evidence: `OQ-1-agent-wait-decision.md:3-6` puts `needs_human_decision` and `status` inside a fenced block rather than front matter. The values are correct. Noted only because the other eight files use front matter.
- Fix (optional): none needed.

## Not checked (outside this lens)

`readonly-probe.md`, `pr422-409-check.md`, `1.0a-facts.md` content beyond the OQ-17 branch, `tests/sweep/fixtures/`, the DESIGN edits, the revision files and the `chat-output-exception` content were not audited for correctness here. They belong to other lenses.

## Summary

- Checks passed: 14 / 15
- Checks failed: 1 (C12)
- BLOCKING findings: 1 (F1). MINOR notes: 2 (M1, M2).
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 14 | Grep: 4 | Glob: 3 | Bash: 1

Verdict: FAIL
Blocking count: 1
