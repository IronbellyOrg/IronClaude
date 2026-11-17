<!-- Source: new text — merged per Change #M-00 -->
<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (run 2 report, RESEARCH-REPORT-review-panel-unification-run2.md) -->
<!-- Merge date: 2026-11-15 -->

# Technical Research Report: Unified Central Review Panel (merged from run 1 and run 2)

## Merge Notes

This document merges two research reports on the same question. Run 2's report (`RESEARCH-REPORT-review-panel-unification-run2.md`, 5,098 lines) is the base. Run 1's report (4,476 lines) contributes the blocks that carry the `R1-` id prefix. The merge followed `adversarial/refactor-plan.md` (changes M-00 to M-30) in the compare folder `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/`; Section 10.B lists every compare artifact.

**(a) Status: `partial`.** The compare debate examined 234 diff points (56 structural, 97 content, 63 contradictions, 18 promoted shared assumptions; `diff-analysis.md` Summary, `debate-points.md`).

| Measure | Value | Source |
|---|---|---|
| Points resolved (both advocates name the same winner, `Both (merge)` included) | 218 of 234 | `partials/scoring-matrix.md`, Convergence Assessment |
| Points both advocates call open (undecidable by the evidence; owner decision) | 6: X-040, X-056, X-058, C-060, X-041, X-057 | same |
| Points still split after Round 2 | 10: 3 real label disputes (C-005, C-076, X-051) and 7 artefacts of cluster inheritance (C-010, C-017, C-018, C-020, C-021, C-024, C-025) | same; `invariant-probe.md` R25-INV-004 |
| Strict convergence (resolved points only) | 93.2% (218 of 234); 95.7% if the 6 both-open points are counted as agreement; threshold 80% | `partials/matrix.json` (`strict` = 0.93162) |
| Points won (strict tally) | Variant 1 (run 1) 26, Variant 2 (run 2) 130, Both (merge) 62, Neither 0 | `partials/scoring-matrix.md` |
| Taxonomy coverage gate | PASS (L1 50 points, L2 126, L3 58, all addressed in both rounds) | same |
| Invariant probe gate | BLOCKS: 7 HIGH-severity UNADDRESSED invariants; status BLOCKED_BY_INVARIANTS; depth `standard` has no Round 3 | `invariant-probe.md` Summary |

How the 10 split points are read in this document (refactor-plan rule 4). C-005, C-076 and X-051 are a dispute about labels only: the run 1 advocate holds BOTH (run 1's superset core kept as the documented one-engine target), the run 2 advocate holds "Variant 2 governing, run 1 detail carried" (`partials/r2-advocate-V1.md:167`; `partials/r2-advocate-V2.md:176`). Both positions are stated where the core shape is discussed (3.6, 7.4). The other 7 are artefacts of `partials/r2-state.json`, where points inherited a cluster label: C-017 and C-025 are Variant 2 for both advocates (`partials/r1-advocate-V1.md:253-254`); for C-010, C-018, C-020, C-021 and C-024 the run 1 advocate's actual position is "V1 on the post gate (C-084, X-043, X-054), BOTH on the rest" (`partials/r2-advocate-V1.md:116`), not a per-point Variant 1 verdict (R25-INV-004; fault-finder correction 14). The consensus summary's figure "224 of 234" counts the 6 both-open points as resolved; 218 is the resolved count (R25-INV-016).

A further read-only check made for this merge found the same inheritance effect on four points that the matrix records as Variant 2. C-056 (calibration) and S-039 (run 1's defect-to-test table) are Variant 1 in both advocates' Round 1 exception lists (`partials/r1-advocate-V1.md:248, 261`; `partials/r1-advocate-V2.md:275, 278`). C-053 (invalid-block policy) and C-065 (per-lens blocking predicate) are Variant 1 in the run 1 advocate's exception list (`partials/r1-advocate-V1.md:247, 249`) and Variant 2 by cluster inheritance for the run 2 advocate. `partials/r2-state.json` has no point entry for any of the four. The counts in the table above are the matrix's and are not re-tallied here; 6.13.0 states the advocates' positions on C-053, C-056 and C-065, and run 1's defect-to-test table (S-039) is carried in 6.13.

The base was chosen by the debate tiebreaker: the combined scores were run 1 0.8845 and run 2 0.8620, a margin of 2.5% (below the 5% threshold), and at tiebreaker level 1 run 2 won 130 of 234 points against run 1's 26 (`base-selection.md`, Combined Scoring).

**(b) What is in this document and how to read it.**

- Base text (run 2) keeps its section numbers, its ids and its line-number citations. Each block carries an HTML comment naming its source: `Base (original)`, `Base (original, modified) — <reason>` for an in-place correction, `Variant 1, Section <n> (lines a-b) — merged per Change #<M-nn>` for a carried run 1 block, or `new text — merged per Change #<M-nn>` for text written by the merge.
- Run 1 blocks are added as numbered subsections at the end of the section they belong to: 2.10 (current state), 3.6 (target state), 4.7 and 4.8 (gap rows; contradictions and track coverage), 5.6 (external findings), 6.13 (conflict blocks, with the disposition table 6.13.0 at its head), 7.4 (run 1 recommendation and architecture, the recorded one-engine alternative), 8.3 to 8.8 (value inventory, migration content, no-regression gates, persisted-format rules, branch-structure constraint, risk inputs and checklist), 9.11 (open questions) and 10.A (evidence trail). Run 1's own section numbers appear in carried headings as `R1 n.m`.
- Where a carried run 1 block and the base disagree, the base governs unless a verified fact says otherwise; each such case is a row of Appendix C. Section 7.0.2 records which of run 2's 15 adjudicated outcomes the compare debate left unchanged and which it changed or reopened.
- New material from the compare: 7.0.2 (status of the 15 outcomes), 9.12 (open items raised by the compare debate), 10.B (compare artifacts), Appendix C (contradiction register, all 63 X rows), Appendix D (the 32-row invariant probe), Appendix E (corrections applied, and counts with units) and Appendix F (provenance index).

**(c) Owner decisions already made (context, not findings).**

- The shared core lives in `src/superclaude/cli/review/`, with thin modules.
- Branch names use the form `feat_review-panel/<name>` (the git-ref constraint that follows from this is in 8.7).
- Stacked pull requests are a matter for the later plan.
- The newer commits of the tasklist branch (newest `e2f2ac268`) are folded in later; neither report read them.
- Pull requests go only to `IronbellyOrg/IronClaude`, through `/sc:pr-submit --monitor 3`.

**(d) Id rule.**

- Ids that exist in the base (run 2) are written without a prefix.
- Every id inside a block carried from run 1 carries the prefix `R1-`, for example `R1-D6`, `R1-C-17`, `R1-ENS-1`, `R1-INV-014`, `R1-G2`, `R1-M1-08`, `R1-V-001`. The prefixed families are run 1's debate-row ids (`R1-C13-22`), its own debate diff-point ids (`R1-C-nnn`, `R1-X-nnn`, `R1-S-nnn`, `R1-A-nnn`, `R1-U-nnn`; run 2 and the compare use the same shapes for other points), constraints and conflict shorthand (`R1-C1`..`R1-C14`, `R1-C01`..`R1-C20`), conflicts `R1-C-nn`, questions `R1-Q-nn`, owner items `R1-O-n`, `R1-OD-n`, hypotheses `R1-H-A`..`R1-H-C` and `R1-Hn`, web files `R1-W01`..`R1-W04`, defects `R1-Dn`, `R1-D-nn` and run 1's "Decision D-1" (`R1-D-1`; run 2's D-1 is a defect), log ids `R1-G-nn`, gates `R1-Gn` and `R1-G-all`, `R1-G-bench`, `R1-G-exit`, `R1-G-new`, `R1-G-pr`, `R1-G-replay`, `R1-G-skills`, `R1-G-sync`, gap rows `R1-BL-nn`, `R1-MS-nn`, `R1-ENS-n`, `R1-DOC-nn`, `R1-OPEN-nn`, success criteria `R1-SC-n`, constraints `R1-K-n`, migration steps `R1-M1-nn`..`R1-M4-nn`, tracks `R1-M1`..`R1-M4` (run 2's M1-M10 are moves), scope slices `R1-S00`..`R1-S05` (run 2's S02 is another folder), `R1-F-n`, inventory rows `R1-V-nnn`, exposures `R1-Xn`, `R1-A-nn`, invariants `R1-INV-nnn`, research files `R1-Rnn` and conditional items `R1-CI-n`.
- A range whose two ends belong to one family is written with both ends prefixed, for example `R1-D1..R1-D16`.
- Run 1's closed items (its list in 9.11, every `GQ C-nn` or `GQ:C-nn` reference and every `C-nn` after the words "closed item") are renamed `R1-CLS-nn`, so a closed item is never read as a run 1 conflict `R1-C-nn`. The backticked `GQ:C-01` to `GQ:C-25` at V1:3107 is a code span and stays as written.
- `R1-Rnn` with nn from 01 to 13 is a run 1 research file (R01 to R13); `R1-Rnn` with nn above 13 is a run 1 debate risk id (for example `R1-R21`). Run 2's R01 to R18 are other files. A bare `R1` to `R9` (no hyphen) inside carried text is an anonymised reviewer id, never a provenance mark.
- Not prefixed: ids inside backticks, URLs and file:line citations; `C3` at V1:169 (a combo run); the probe labels `M1`-`M4` at V1:2704, 2729 and 2761. In 9.11, `R1-Gn` means gap row n and `R1-C1`..`R1-C3` mean closure-effort classes (V1:4126).
- Inside a carried `R1-` block, a bare short label that this rule does not list (for example the V1-V4 `panel verify` checks, T1/T2, the S1-S5 rf-qa sections, the F2/F3 audit rows, the A-1/A-4 audit checks, the K1-K4 MR kernel layers, the B-1..B-4 stages, the M5-M12 probe labels, the P3-B1 QA ids) keeps run 1's meaning and is not a base id.
- Under each carried run 1 legend (V1:108-129, 483-492, 4126) one line says: "In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule)".
- Compare ids: three-digit `C-`, `X-`, `S-`, `A-` and `U-` ids in new text (these Merge Notes, lead sentences, notes and Appendices C to F) are ids of the compare's `diff-analysis.md` (for example C-084, X-043). The exception is base text inside V2:3509-3525 and V2:3586-3670, where three-digit ids are points of run 2's own debates. Two-digit `C-01`..`C-15` and `X-13`..`X-15` are run 2's debate slots.
- Invariants found by the compare fault-finder are cited `R25-INV-nnn` (`invariant-probe.md`); they are not the debate-local INV ids of either report.

**Citation form.** In new text (these Merge Notes, lead sentences, notes and Appendices C to F), `V1:<n>` means line n of run 1's report (byte-identical copy `adversarial/variant-1-original.md`) and `V2:<n>` means line n of run 2's report (byte-identical copy `adversarial/variant-2-original.md`); `V2:<n>` refers to the base as it was before the merge, not to this file. Carried blocks keep their own line citations into the repository, which are unchanged.

**(e) E2 evidence pins.** Run 2 reads the E2 branch at `6c0984326cbb8fb06c4a36065de58b171d3f8175`; run 1 read it at `4a22d74213f93837d00c2c314075dd967b9a98e3`, four commits earlier (`git rev-list --count 4a22d74..6c09843` = 4). Commit `e2f2ac268` (2026-11-14 19:19 UTC) is 7 commits after `6c09843` (`git rev-list --count 6c09843..e2f2ac268` = 7); neither report read it, and by owner decision it is folded in later. The E2 files the two reports cite were not changed by those 7 commits (fault-finder notes section 1, row 4; for `audit2.py` and `combos/SPEC.md` re-checked by this merge with `git diff --name-only 6c09843 e2f2ac268`, empty).

**(f) HEAD and line numbers.** The code is identical at `792cf8c52` (run 1's HEAD), `50d4d2b9d` (run 2's HEAD) and `ad8f57560` (HEAD of `ironbelly/shadow-runs` at the merge) for `src`, `tests` and `scripts` (`git diff --stat` empty for both pairs). Line numbers in this document are valid at `ad8f57560`. A later plan must re-check every cited line at the base it cuts its branches from: `origin/master` (`d4d1662a8`) has moved and sits 3 commits past the merge-base `d2d8a2d16` (Baseline and Conventions, merge addendum; R25-INV-001).

**(g) Open items that block a `converged` status.** The 7 HIGH UNADDRESSED invariants of the compare probe are carried as open items, not as settled, in Section 9.12: R25-INV-003 (ledger version skew), R25-INV-006 (read-only mechanism leaves MCP servers available), R25-INV-018 (gate set and gate cross-references), R25-INV-024 (cascade of the clustering trigger T-c), R25-INV-027 (run 1 migration steps that conflict with the adopted design), R25-INV-028 (five outcomes changed or reopened without a new debate) and R25-INV-029 (trigger T-c already met by an agreed fact unless the owner accepts the v1 over-merge). Appendix D lists all 32 probe rows.

**(h) Scope.** This document adds no roadmap, no branch plan, no pull-request plan and no schedule. Run 1's migration steps, gates and risk rows are carried as content; where carried run 1 text uses ordering words, they are run 1's recommendation, not an order of work in this document.
