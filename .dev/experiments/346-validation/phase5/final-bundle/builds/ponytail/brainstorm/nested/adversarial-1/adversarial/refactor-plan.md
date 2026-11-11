# Refactoring Plan

## Overview
- Base variant: B (variant-2-sonnet-refactorer.md), combined score 0.967
- Incorporated: A (variant-1-opus-architect.md), C (variant-3-haiku-qa.md), debate rounds 1-2, invariant probe
- Planned changes: 21
- Overall risk: Medium (changes 9-16 alter safety rules of the base)
- Output: `../merged-output.md` (a design spec), plus `merge-log.md`

## Planned Changes

### Debate-agreed changes (1-8)
1. **Drop the revert channel from every review-3 forecast.** Source: diff A-001, all advocates. Target: B s1, s9, s11, s14.2. Replace with the corrected forecasts of change 14. Risk Low.
2. **Remove `--apply-audit` and the `plan` subcommand.** Source: round2-B O4 and 1.3. Target: B s1, s3.3, s3.4, s6, s10, s12. Consent is choosing the variant plus owner approval of the editing contract recorded before S1 (round2-C O4). The row builder is a function inside `apply`. Risk Low.
3. **Separate heading.** Source: C s9, round2-C O5 (S-001). The variant keeps the 427 `## Review Loop` with exactly its seven bullets byte-identical; the audit lives in a new `## Fix Audit (review 3 only)` section placed right after it. No bullet 8. Risk Low.
4. **Brief stored once, copied by script.** Source: A s5, S-002. `sc-fix-audit/refs/auditor-brief.md`; `prepare` fills the placeholders and writes `D/brief.md`; the session passes that file's text unchanged. Risk Low.
5. **Auditor isolation and fallback labels.** Source: A s6, C-006. Header lines `auditor: ponytail-review|inline-rubric` and `auditor-isolation: subagent|in-session`. Risk Low.
6. **Upgrades logged, ignored.** Source: A K9. A validated `blocking` on a report-minor id is logged `UPGRADE <id>` and never enters the verdict. Risk Low.
7. **Shrink rule: delete words or restore the aligned baseline span** (round2-B O2, round2-C O2). Exact token identity and order, no case or punctuation folding. Risk Medium; tightened by changes 12 and 13.
8. **Naming and accounting.** Source: C s1, s11, round2-C O5. Never call a post-audit number "review 3". Report raw review-3 proxy, review-3 blocking, pre-audit growth and post-audit growth as separate numbers. Plugin-absent or inline-rubric runs finish as plain 427 but are not valid plugin-treatment replicates and stay in all-attempt accounting; check failure, apply STOP and skip guard are outcomes, not grounds to void. Risk Low.

### Invariant-probe fixes, HIGH (9-16)
9. **INV-005 review 3 unprimed.** The auditor subagent writes `D/audit.md` itself and returns only `done`. The review-3 session never reads `audit.md`, `apply-log.md` or `brief.md`; it reads only each script's exit code and one summary line (`APPLY_OK reverted=n shrunk=n` or `APPLY_STOP`). Review 3 needs no audit content: the audit can close only report-minor ids, which never appear in review 3's prior-blocking table. Residual risk (prose): the session knows an audit ran. Measurement check: the transcript shows no Read of those files before the report is written.
10. **INV-007 unattributed hunks are kept.** A hunk citing no id is never whole-reverted; the auditor may propose a deletion row for it, under the same rules as a blocking hunk. Drop B's unattributed-to-revert default, including from `--auto-minor`.
11. **INV-008 cross-check against the disposition.** Before any whole revert, `prepare` reads the cycle-2 disposition file named by `--dispositions` (default: `disposition-round2.md` beside the R2 report, if present) and every line range its `Where` column gives for an R2 blocking id; a hunk overlapping any of them is reclassed `blocking-involved`. No disposition file found: no hunk is whole-reverted (all become `blocking-involved`), and `audit.md` records `dispositions: none`.
12. **INV-009 delete-only keyed on the hunk.** Any row inside a hunk classed `blocking-involved` or `unattributed` may only delete words; restore rows are allowed only in `minor-only` hunks.
13. **INV-010 deletions touch only cycle-2 added words.** `check` computes a word diff of the row's span against the aligned baseline span and rejects any row that removes a baseline token or a context token. A row may remove only words the cycle-2 fix added.
14. **INV-018 corrected forecasts.** Class-A credit is 0 on the Arm B base (its only class-A critical+major finding, flg-r1 R3-7, sits on an FR-8-tagged row the protection rule never reverts). Arm B class B is 2 findings, both in flg-r1, so the audit can lower the mean by at most 1.0. Forecast P: 3.5 minus 0.35 to 0.5 (class B 1.0 per run times 35-50% nominated before review 3) plus 0.15 to 0.25 replacement and regression findings = about 3.2 (range 2.8 to 3.6); the bar of 3 needs at least 50% capture and no replacements. (a): about 3.1; (b): about 3.5. Growth: P 27%, (a) 26%, (b) 26%. 427-only base (5.5): P about 5.1.
15. **INV-032 gate readouts.** Pre-register logged readouts G1-G6: G1 audit fired (and with which auditor); G2 rows nominated, each matched afterwards against review-3 anchors in the paired review (change 16); G3 rows applied and SKIPped; G4 audit-caused review-3 findings (quoting an audited span); G5 all-grade review-3 total; G6 critical+major and blocking. A miss is traced to the first gate that failed. Falsifier from the probe: all-grade review-3 totals stay level while changed lines fall.
16. **INV-033 paired measurement.** In each replicate, run one extra independent review 3 (same command, same flags, separate session, outside the loop, not shipped, not used for the verdict) on the kept pre-audit copy `D/current-before-audit.md`. Report the paired difference (audited review 3 minus pre-audit review 3) as the audit effect, beside the comparison with historical Arm B.

### Invariant-probe fixes, MEDIUM (17-21)
17. **INV-002 baseline check.** `prepare` records the baseline sha; the experiment pre-registers that it equals the coordinator's saved `spec-v2-after-round1.md`; a mismatch is recorded as wrong input (void for comparison).
18. **INV-006 bullet-4 conflict.** The Fix Audit section states that, in the variant only, the scripted audit edit is the single exception to bullet 4's "writes no revised specification"; review 3 itself still writes no revised specification.
19. **INV-011 early PASS.** Pre-register: a replicate whose review 2 ends `verdict: PASS` has no cycle 2 and no audit; it counts as a clean pass in fewer rounds (the D10/D11 bar's own alternative) and is reported as audit-not-triggered.
20. **INV-017, 019, 020 metric definitions.** Report both the critical+major proxy and 427 blocking; define the proxy as the recorder's existing count of new review-3 findings, and separately report reopened (`open` or `regressed`) prior findings; state that the audit lowers the proxy only when a finding disappears, never by regrading.
21. **INV-030 substitution only in the review-3 brief.** Reviews 1 and 2 and both reviser briefs keep `/sc:spec-panel`, so they stay byte-identical to Arm B; the one-line substitution is made in the review-3 brief only.

### Post-debate correction found by the orchestrator (22), overrides the in-run placement of changes 2, 9, 18, 21
22. **The audit is its own step, not part of the review-3 run.** Evidence: the S1 review-3 brief `exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/templates/T09-R3-reviewer.TEMPLATE.txt` line 1 says "Ownership: write ONLY that file; do not edit the spec", and 427 bullet 7 lets a brief narrow scope, so an audit inside the review-3 run may neither write `fix-audit/` nor edit the spec. No variant or advocate read T09. New shape:
    - The variant command gains a mode: `/sc:spec-panel-ponytail @<spec> --fix-audit --re-review <R2 report> --baseline <copy before cycle 2>`. It runs only the audit (prepare, ponytail-review in this session, check, apply) and writes `fix-audit/` beside the R2 report; it writes no review report. Invoking `--fix-audit` is the consent for the one scripted edit (C6). Without `--fix-audit` the variant behaves exactly like `/sc:spec-panel`.
    - The coordinator runs it once, after the cycle-2 reviser and before review 3, as its own Task (own session). Review 3 is then run as before (in the experiment, T09 verbatim with plain `/sc:spec-panel`).
    - Consequences: the auditor is a fresh top-level session, so no subagent is needed (A-003 reduces to "a top-level worker can load a plugin skill", which the round-3 report observed for command skills); review 3 never sees audit content (INV-005 solved by session boundary, not prose); the bullet-4 conflict (INV-006) disappears because the review run writes nothing new; change 21 becomes "no review brief changes at all".
    - The experiment brief change is one inserted Task (T08a), not a substitution: its single command line is the `--fix-audit` invocation above with the S1 paths. State plainly that a pure one-line name substitution in T09 cannot work.
    - Verdict: `fix_audit.py verdict` runs after review 3 (coordinator or recorder), reads review 3's report and the audit files, and prints the open blocking list and PASS/FAIL under 427 grading; it never creates a PASS or lowers a FAIL. T09's own "any finding of any severity is FAIL" line stays in the brief and is reported separately.
    - Paired measurement (change 16) becomes a fork: after the cycle-2 reviser, copy the loop folder to a sibling worktree; run T08a plus T09 in one, T09 alone in the other. The difference isolates the audit from the review-1/review-2 path spread (Arm B 6 vs 1).

## Changes NOT Being Made
| Diff point | Non-base approach | Reason |
|---|---|---|
| C-001 (C) | terminal audit after review 3 | cannot move the registered metric; ships unread edits (round1-C concession 1); kept in the spec as the rejected reading "P-post" with its prediction |
| C-002 (C) | both cycles in one audit | cycle-1 minor-only text is 6% of cycle-1 added bytes; report 2 has no cycle-1 grades (round2-B 1.5); covered instead by placement (a) |
| C-003 (C) | reviser-written edit ledgers | change the treatment and cost more than they save (round2-C 1.2) |
| C-004 (A) | downgrade-and-revert of MAJOR fixes | blocking reverts reopen findings (evidence-attribution caveat); all three adopted B's ban |
| C-004 (C) | FR-8/FR-9 override | contradicts 427 bullet 2 |
| C-007 (C) | fail closed with no fallback | product keeps working; validity handled by change 8 |
| C-005 (A) | deletion-only shrinks | cannot express trt-r1 R3-4 "keep v2 wording"; restore allowed only in minor-only hunks (change 12) |
| U-001 (A) | N5 deletion as the showcase | judged class C by the evidence reader; kept only as an example of an untested deletion |

Anchor-level rule: A's anchors kept (K4 lock, REVERT_SHARED, one-owner table, cost figures, Q1-Q7); C's anchors kept (edge-case list in full, E-codes renamed to plain statuses, run-validity rules); none silently dropped.

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 9 | Medium | prose rule; priming not fully removed | paired review (16) measures it |
| 10-13 | Medium | fewer rows pass, lower yield | yield is a G3 readout |
| 14 | Low | forecasts drop below the bar's comfort | none needed; honest |
| 16 | Low | one extra session per replicate | optional only if budget is cut, then stated |

## Review Status
- Approval: auto-approved (unattended)
- Timestamp: 2026-11-08T15:05:00Z
