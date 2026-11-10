# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 plus Round 2.5 invariant probe (Round 3 skipped: depth=standard)
- Convergence achieved: 96% (24 of 25 diff points)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (A = opus:architect, B = sonnet:refactorer, C = haiku:qa)
- Full statements on disk (this transcript summarizes and scores them; the files are the record): `debate/round1-A.md`, `debate/round1-B.md`, `debate/round1-C.md`, `debate/round2-A.md`, `debate/round2-B.md`, `debate/round2-C.md`; probe: `invariant-probe.md`
- Evidence introduced during the debate: `enrichment/evidence-attribution.md` (all), `enrichment/minor-byte-share.md` (all), B's per-run cycle-2 byte shares (round2-B section 3: flg-r1 33%, flg-r2 27%, trt-r1 10%, trt-r2 10% minor-only; controls cite almost no ids), A's review-2 origin count (round2-A section 3: 22 of 25 review-2 blocking findings on cycle-1-changed lines; B and C: a location tag, not a cause), C's parser traps (round2-C section 3: four severity formats, `MAJOR (FR-8 GAP)` graded minor, `non-blocking` contains `blocking`).

## Round 1: Advocate Statements

### Variant A Advocate (opus:architect)
Keep A's skeleton (one audit after cycle 2, before review 3, generic script does every edit and the verdict) but move the weight from reverts to deletion-shrinks of blocking fixes. Conceded: A-001 refutes the revert channel (about 4% of R3 blocking, not 15-30%); A-004 lowers growth gains; the N5 to N12 example is class C, not a deletion win; MAJOR downgrade-and-revert goes (X-002 to B). Revised prediction 2.7-3.2 and 26-28%.

### Variant B Advocate (sonnet:refactorer)
Script-first, fail-open, model only for severity and necessity. Strengths: worst case is plain 427; script never creates a PASS or lowers a FAIL; one-line brief change; most mechanical checks; `--auto-minor` ablation and blind re-grade as falsifiers. Conceded: forecast withdrawn (2.4 to about 3.3); m = 0.35 to 0.27; shrink check blocked sentence-level minor trims; unattributed-default-revert is a hazard; no in-session fallback (adopt A's).

### Variant C Advocate (haiku:qa)
Strongest safety and measurement contract for a terminal audit (both cycles, raw result kept, missing evidence fails the treatment). Conceded: the terminal placement cannot move the registered raw review-3 count; its point predictions are withdrawn; ledgers cost more than they save; B's blocking-revert ban is the safer default.

## Round 2: Rebuttals

### Variant A Advocate
Kept all round-1 concessions; adopted B's blocking-revert ban, `open-blocking:` line, fail-open guard and Q2-before-Q1. New: 22 of 25 review-2 blocking findings on cycle-1-changed lines; 7 of 7 class B and about 10 of 12 class C anchor on cycle-2 fixes; 0.46 R3 B+C findings per cycle-2 blocking fix. Positions: O1 run P now, (a) pre-registered; O2 deletion-only shrinks; O3 cycle 2 only. Prediction P 2.9 / 26%, (a) 2.7 / 23%, (b) 3.4 / 26%.

### Variant B Advocate
Dropped `--apply-audit`, folded `plan` into `apply`, narrowed the safety claim, withdrew the cumulative-baseline shortcut. Measured cycle-2 minor-only shares for four 427 runs (33/27/10/10%) and four severity formats. Checked A's items: 1 holds as a count but not as a cause, 2 holds, 3 weak as a rate, 4 mostly holds (one case needs a baseline restore). Positions: O1 P now, (a) on an anchor readout; O2 delete words or restore the baseline span; O3 cycle 2; O4 no consent flag. Prediction P 3.1 / 27%, (a) 3.0 / 26%, (b) 3.4 / 26%.

### Variant C Advocate
Withdrew the terminal placement and ledgers for P; kept proof of a real Skill call for plugin claims. Confirmed the four formats and added parser traps; corrected "controls cite no ids" (ctl-r2 cites some ids as rationale); noted `minor_share.py`'s regex misses `R2-1` and the severity-rule test scans tracked files only. Positions: O1 P with a cause-based trigger for (a); O2 B's rule with aligned spans and token-exact deletion; O3 cycle 2; O4 name substitution plus recorded owner approval; O5 minimum test list and run-validity rules. Prediction P 3.3 / 27%, (a) 3.2 / 26%, (b) 3.5 / 27%.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L2 | C (separate `## Fix Audit` heading, Review Loop keeps seven bullets) | 60% | only C argued it (round2-C O5); A and B took no position; unresolved by agreement |
| S-002 | L2 | merge A+B | 80% | B's `refs/auditor-brief.md` file, A's rule that a script copies it so no model writes the brief |
| S-003 | L2 | B | 85% | markdown table plus one fenced JSON block of edit rows; C dropped its schema file (round2-C 1.2) |
| S-004 | L2 | B (minus `plan`) | 80% | B round2 1.3; A round2 2 |
| C-001 | L3 | A and B (before review 3) | 95% | C conceded (round1-C concession 1, round2-C 1.1) |
| C-002 | L3 | A and B (cycle 2) | 90% | 7 of 7 class B on cycle-2 fixes; cycle-1 minor-only hunks 6% of added bytes |
| C-003 | L3 | merge B+C | 90% | diff hunks with B's classes; model-written exact rows inside mixed hunks; no reviser ledger |
| C-004 | L3 | B | 95% | all three adopt "no whole revert of report-blocking text" |
| C-005 | L3 | B (delete or aligned baseline restore) | 70% | B and C over A's deletion-only; trt-r1 R3-4 needs a restore |
| C-006 | L2 | A (fresh subagent with `auditor-isolation` fallback label) | 75% | B adopted it (round1-B concession 5) |
| C-007 | L3 | merge | 85% | product continues as plain 427, run void as plugin treatment, kept in all-attempt accounting |
| C-008 | L2 | merge A+C | 80% | pure name substitution; owner approval of the editing contract recorded before S1 |
| C-009 | L3 | merge B+A+C | 90% | script cannot create PASS or lower FAIL; `open-blocking:` line cross-checked with tables; raw and post-audit numbers named separately |
| C-010 | L2 | A and B | 90% | one-line name substitution keeps Arm B comparable |
| C-011 | L2 | merge | 85% | all revised to 2.9-3.3 and 26-27% for P |
| X-001 | L3 | merge | 85% | P chosen; "review 3 reads the shrunk text" recorded as the owner's call |
| X-002 | L3 | B | 95% | unanimous by round 2 |
| X-003 | L2 | merge | 85% | see C-007 |
| X-004 | L2 | all (no) | 100% | all three state it |
| X-005 | L3 | merge (drop revert channel from R3 forecasts) | 95% | A-001 evidence |
| X-006 | L2 | A and B | 85% | C conceded ledgers for P |
| A-001 | L3 | REJECT (all) | 95% | 1 of 28 |
| A-002 | L3 | QUALIFY (all) | 85% | tolerant parse, fail-open guard |
| A-003 | L2 | QUALIFY (all) | 85% | smoke probe before S1 |
| A-004 | L3 | REJECT (all) | 95% | 6% and 27% |

Taxonomy coverage: L1 0 points by auto-tag (no surface-level differences of substance; naming of the raw versus post-audit metric is the closest and is scored under C-009), L2 11, L3 14. The L1 gap is noted; a forced round was not run because no L1 diff point exists in diff-analysis.md to debate (all differences there are structural or state-level).

## Convergence Assessment
- Points resolved: 24 of 25
- Alignment: 96%
- Threshold: 75%
- Status: BLOCKED_BY_INVARIANTS after Round 2.5 (`invariant-probe.md`: 33 items, 18 UNADDRESSED, 8 HIGH: INV-005, 007, 008, 009, 010, 018, 032, 033)
- Unresolved points: S-001
- Resolution (no Round 3 at depth standard): every HIGH item's "Required fix" is adopted as a planned change in `refactor-plan.md` (changes 9-16) and applied by the merge; the MEDIUM items INV-002, 006, 011, 017, 019, 020, 030 are adopted as changes 17-21. The merge log records each. The gate is cleared by plan, not by debate agreement, so the return contract reports `status: partial` with this note rather than claiming debate convergence on those items.
