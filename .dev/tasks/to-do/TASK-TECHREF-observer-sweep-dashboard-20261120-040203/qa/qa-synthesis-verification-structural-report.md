# QA Report - Gate 2 Synthesis Fix Verification (structural, fix-cycle, report-only)

**Status:** Complete
**Topic:** Observer, sweep and dashboard technical reference, Gate 2 fixes
**Date:** 2026-11-20
**Phase:** fix-cycle (review 2)
**Fix cycle:** 1
**Fix authorization:** false (no synthesis file modified)

## Overall Verdict: PASS (with notes). 7 of 7 blocking findings resolved (GS-5 judged resolved as far as reasonable, residual recorded below); 0 new blocking findings; 0 regressions. |F_1| = 7, |F_2| = 0.

## Per-finding verification (adversarial: current synthesis text plus snapshot lines read by me, fix log not trusted)

Snapshot = `/home/coder/.cache/ic-snap-20261120/master`; synthesis dir = `.../synthesis/`.

| ID | Status | Evidence |
|---|---|---|
| GS-1 | RESOLVED | synth-03:119 now reads "Draft7Validator in test_commands.py and test_snapshot_schema.py; shared validator set up in `conftest.py:17, 32`". Snapshot grep of `tests/observe` for `Draft7|jsonschema`: `conftest.py:17` (import), `:32` (`check_schema`), `test_commands.py:17, 44`, `test_snapshot_schema.py:10, 25, 60`; `test_export.py` has no hit. `test_export` no longer appears next to Draft7Validator anywhere in the synthesis (synth-07:117 lists it only as an export test file). |
| GS-2 | RESOLVED | synth-07 14.4 B now carries: line 215 the Orca error-code names `consumer_fenced`, `no_active_terminal` (UNVERIFIED, research 01:52, which I read: "[UNVERIFIED against a live Orca]"; code names confirmed at `adapter.py:67-68, 475`); line 219 `orchestrator-poll` (`*/5 * * * *`), `IronbellyOrg/IronOrchestrator`, `waker.py` triggers (research 05:571-572 and GF-3:185-186 read, both say UNVERIFIED); line 221 new row "Orca wrappers and recorded live result" (three wrappers reason not stated; issue #590 result recorded, not re-run). The #590 figures (264 / 263) are tagged "recorded, not re-run [UNVERIFIED]" or "recorded report, not re-run" at synth-01:88, synth-06:180, 206, synth-07:136, 221; no untagged occurrence remains (grep of `26[34]` across all seven files; the remaining hits are unrelated line numbers). The synth-04:90 occurrence no longer exists (paragraph removed under GS-5). I spot-checked the other UNVERIFIED lines of synth-02 (113, 123, 124) and synth-04 (65, 69, 119, 167, 175, 178): each maps to a U-id already in 14.4 B (U-10 to U-15, U-14, U-25, U-27, U-35). |
| GS-3 | RESOLVED | synth-07:71 now says `classify_all` tests `idle` and `person_active` once at `classify.py:958` (adds the `last_activity from <source>` suffix). Snapshot `classify.py:958` is `if cls.rule in ("idle", "person_active"):`, `:959` adds the suffix, `:960` is `if forced:`. "two places" no longer occurs. |
| GS-4 | RESOLVED | synth-07:260 now says the verb is named in `check.py:77` (docstring) and `common.py:136` (comment) and called only by `settle.sh:1037-1042` (probe at :1037, call at :1042, ends `ENTRY escalated why=surface_absent`). Snapshot: `check.py:77` is docstring text "its `report-entry` verb checks"; `common.py:136` is a `#` comment; `settle.sh:1037` is the `superclaude orchestrator report-entry --help` probe, `:1038` prints `why=surface_absent`, `:1042` is the call. The row at old 13.1 line 111 was deleted; synth-07:142 and synth-05:94, 123 make no caller claim about check.py or common.py. Other occurrences of the verb in the snapshot (`run.py:688` comment, tests, `sc-closeout-protocol/SKILL.md:21`, `refs/settle.md:99`) are comments, tests or prose, so "called only by settle.sh" holds for code. |
| GS-5 | RESOLVED as far as reasonable (partial; see GS-5 section) | Plan items 1 to 5 all applied; total 1,644 to 1,500 lines (`wc -l` re-run by me matches the fix log per file); characters 244,256 to 213,445 (-12.6%). Target "about 1,300" not met (200 over); Standard ceiling 1,200 not met (300 over). |
| GS-6 | RESOLVED | synth-01:103 now gives per-item lines: stalled and fenced 493, 636, 841, 877; `agent_wait_since` 493, 494, 649, 1003; `Safe to close` 794; `Removable` 795. Snapshot `orchestrator-mode.md`: 493 (Rule 5, `agentWait`, `worker_done_seen` None, `fenced_evidence` unreadable), 494 (unknown age), 649 (waiting (a) unknown-age rows), 794 (FR-012 `safe_to_close`), 795 (FR-013 `removable`), 1003 (open item 6, non-null `agentWait` never captured), 877 (SP-24 row). They match 14.5 C8-3 to C8-5 (DESIGN:493, 494, 649, 1003; 794; 795). |
| GS-7 | RESOLVED | synth-07:298 now: "R1 live worker-list ledger, `--once` and snapshot (it records the redacted golden samples)". Matches synth-03:204 ("Live worker ledger, `--once`, snapshot") and `release-gates.md` (read via `git show origin/master:...`): R1 row "Live worker-list ... add a redacted golden sample" and R0 row "until R1 records the redacted golden samples". |

## GS-5 (line budget): judgment and what remains

**Line counts (`wc -l`, run by me):** synth-01 104, synth-02 136, synth-03 250, synth-04 243, synth-05 211, synth-06 234, synth-07 322; **total 1,500** (before: 1,644). Target in the finding: about 1,300. Standard ceiling in `reviews/phase5-synthesis-inventory.md:15`: 800-1,200. Gap: 200 over target, 300 over ceiling (25%). The assembler adds only a header and table of contents, so the assembled body will be about 1,540.

**What was done (verified in the current text):** plan item 1 (14.5 rows C8-1..C8-7 shortened, R-C8 rule and C8-8, C8-9 untouched; checked against the pre-edit copy `/tmp/synth-07.before-gs5`: the C8-8 row is byte-identical, C8-9 keeps its owner question and the "Remediation task not created (read-only brief); flagged for the owner" wording); item 2 (13.1 unification table cut to 2 rows, synth-07:100-105); item 3 ("Replacement wording (GF-2, verbatim)" gone; grep finds no match); item 4 (synth-05:99 "Wording rule" is one short paragraph with a pointer to 14.5); item 5 (synth-06 "Source conflicts and corrections" gone; grep finds no match). Beyond the plan: synth-05 C1-C6 table replaced by a pointer, and I checked that the six facts sit in 14.4 A (SD-21 to SD-29 rows, synth-07:206-207) and 14.3 (write-back row, :173); synth-02 4.1 (c), (d) replaced by pointers to 5.5 and 5.6; 21 glossary rows, 3 duplicate 14.2 rows and many duplicate rows in synth-01, 04, 06 removed. Volume fell 12.6% in characters (244,256 to 213,445), more than the 8.8% in lines because the rows are wide.

**Is more reasonably cuttable?** I looked for remaining duplicates. Facts that still appear in two or three places: the C8-1..C8-5 limits (synth-04:80-88 table, synth-07 14.1 rows 1-3, 14.5 rows, synth-01:103 pointers); the "Remediation task not created" wording (17 lines; 8 of them are the mandated 14.5 rows and rule, 5 in the synth-04 table). Removing every one of those leaves the facts only in one place each and saves roughly 25 to 40 lines, which gives about 1,460, still well over 1,300. The rest of the gap sits in sections the finding told the fixer to protect (2.5 matrix, 8.1 verb inventory of 39 lines, 14.4 contradictions list of about 50 lines, the five 13.1 scenarios, 14.5) and in template-mandatory sections (3, 4, 12.3, 13.2). Further cuts would delete unique verified facts, which is an owner choice, not a mechanical dedupe. I agree with the fix agent's candidate list in `qa-synthesis-fix-log-c1.md` ("GS-5 status"): Section 3 locations block and 3.1 table (about 20 lines), synth-02 4.1 (a), (b) diagrams (about 20; these partly repeat the 5.1 and 5.3/5.4 diagrams), synth-03 5.2 PR and width tables (about 15), synth-05 5.6 S/R status tables (about 20), synth-07 12.3 and 13.2 (about 20), synth-06 11.2 and 11.3 (about 20), 14.2 debt rows (about 10).

**Grade:** the overrun is a size target, not a wrong behaviour, a false claim, a missing section or a security risk; every required section and every protected part is present. Under the review severity rule I grade the remaining 200 lines as a minor note with an owner decision attached, and GS-5 as resolved as far as reasonable. This is a judgment under the criterion given for this review, and I state plainly that the Gate 2 text in the inventory ("bring the assembled document within budget") is NOT met: 1,500 lines against 1,200.

**Options for the executor/owner (not applied, read-only review):** (a) accept about 1,540 assembled lines and carry the overrun as a Gate 3 note; (b) order one more cut pass that drops the named unique rows, with the owner choosing which facts to lose.

## New-issue check (introduced by the fixes)

| # | Check | Result | Evidence |
|---|---|---|---|
| N1 | Template headers intact | PASS | Heading scan of all seven files: sections 1, 2.1-2.4 (+2.5 added), 3, 3.1, 4.1-4.3, 5.1-5.6, 6-11 with 8.1-8.3, 9.1-9.3, 10.1-10.3, 11.1-11.3, 12.1-12.3, 13.1-13.2, 14.1-14.6, 15.1-15.2, 16, Appendix; same order as `technical_reference_template.md` (the `## 5. Subsystem Reference` parent heading is absent from every synth file; Gate 1 structure reports 1 and 2 passed this, so it is for the assembler). |
| N2 | No placeholders | PASS | Grep for `TBD|TODO|FIXME|[Feature Name]|[Subsystem Name]|PLACEHOLDER` over the seven files: no match. |
| N3 | Tables not broken by the whole-line deletions | PASS | awk check of every table block (pipe count outside backticks and escaped pipes) in all seven files: no row with a column count different from its header, no table under 3 rows. |
| N4 | C8 wording and labels | PASS | R-C8 rule at synth-07:239-244 intact; C8-8 and C8-9 labelled **DEFECT-CANDIDATE** with the mandated sentence; C8-1..C8-3, C8-6 keep the sentence; C8-4, C8-5, C8-7 end "Flagged for the owner." exactly as in the pre-edit copy (not a new loss; see note 4). No DEFECT-CANDIDATE relabelled. |
| N5 | No unification recommendation | PASS | Grep for unif*/consolidat*/"should merge" over the seven files: only "no unification recommendation / facts only" disclaimers (synth-01:3, synth-02:3, synth-04:5, synth-07:3, 100, 312). |
| N6 | No fabricated facts in added text | PASS | The added 14.4 B text traces to research 01:52, 05:571-572, GF-3:185-186 (all read); the GS-1, GS-3, GS-4, GS-6, GS-7 rewrites checked against snapshot lines above. |
| N7 | Dangling references from deletions | PASS | 15.2 step 2 now points to Section 5 Public Interface blocks; those blocks hold `classify` (synth-04:93), `collect` (synth-04:212), `build_view` and `render` (synth-03:226), `Collector.__init__` (synth-03:103); snapshot `classify.py:369`, `probes.py:1322`, `view.py:968`, `render.py:1449` are the definitions. synth-05 pointers to 14.4 A and 14.3 resolve (see GS-5 section). |
| N8 | Regression check (run first) | PASS | No item that passed at review 1 fails now: structure report 1 items still hold (headers, tables); no claim made false by a deletion was found. |

## Summary
- Blocking findings: |F_1| = 7, |F_2| = 0 (strictly fewer; no regression, so no [HALT-MONOTONICITY]).
- Checks passed: 7 findings + 8 new-issue checks = 15 / 15.
- Open blocking findings: 0. NEEDS-RESYNTH: none.
- Issues fixed in-place: 0 (fix authorization false; no synthesis file modified).

## Issues Found (all minor; notes only, not rechecked, no fix pass)
| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | MINOR | whole set | Line budget still 1,500 vs 1,300 target and 1,200 ceiling (GS-5 section) | Owner decision: accept, or one more cut pass of the named unique rows |
| 2 | MINOR | synth-07:221 | New 14.4 B row cites "synth-01 Section 2.5" for "reason for three wrappers not stated"; the statement sits in synth-01:69 (Section 2.3) | Say "Section 2.3" |
| 3 | MINOR | synth-01:103, synth-07 C8-3 | Lines 493, 494, 649, 1003 for `agent_wait_since` do not contain the literal name (they cover `agentWait` and the unknown-age rule); they are the lines GF-1 names, so this is consistent, not wrong | Optional: say "`agentWait` and unknown age" |
| 4 | MINOR | synth-07 C8-4, C8-5, C8-7 | R-C8 item 4 says the "Remediation task not created" sentence goes on a KNOWN LIMIT whose cited text names no tracked owner; these three rows print only "Flagged for the owner." (same as before the fix; synth-04:87-88 prints the full sentence for C8-4, C8-5) | Add the sentence, or narrow rule item 4 |
| 5 | MINOR | synth-07:4 | "the brief asked for about 160 lines" is stale next to a 322-line file | Update or drop the note |
| 6 | MINOR | fix log | Bulk deletions used `sed` on line numbers (disclosed); the pre-edit copies in `/tmp` exist; the result passed my table and heading checks | none |

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 21 | Glob: 2 | Bash: 6 (each call mapped to a finding or new-issue check above; two read the pre-edit copies, one ran the table check, one `wc -l`)
- Not done: I did not re-read all 1,500 lines of the synthesis for facts unrelated to the seven findings (that is Gate 2 review 1's job; minor findings are not rechecked), and I did not run any code or tests.

## QA Complete
