# QA Source Fidelity - Final experiment report

- **Topic:** Independent source verification of the issue 346 final experiment report
- **Date:** 2026-11-09
- **Phase:** source-fidelity
- **Fix cycle:** 0 / 2

## Sources Reviewed

| Source Doc | Assigned Section Range | Line Count |
|------------|--------------------------|------------|
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/FINAL-REPORT.md | Whole report | 259 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/final-summary.json | Whole companion | 189 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/final_report_check.py | Whole checker; default read-only execution | 127 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md | Whole fixed decision log | 74 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md | Whole controlled comparison | 47 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md | Whole flagged comparison | 42 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/first-run-fidelity-review.md | Whole independent review, including original FAIL and uncertainty notes | 66 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/repeat-plan.md | Whole corrected plan | 28 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-diffgate/.dev/experiments/346-validation/phase5/diffgate/comparison.md | Whole original comparison | 105 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-diffgate/.dev/experiments/346-validation/phase5/diffgate/metrics.json | Whole original metrics | 119 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-diffgate/.dev/experiments/346-validation/phase5/diffgate/validity.md | Whole original validity record | 104 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail/.dev/experiments/346-validation/phase5/ponytail/comparison.md | Whole original comparison | 76 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail/.dev/experiments/346-validation/phase5/ponytail/metrics.json | Whole original metrics | 232 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail/.dev/experiments/346-validation/phase5/ponytail/validity.md | Whole original validity record | 94 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger/.dev/experiments/346-validation/phase5/ledger/comparison.md | Whole original comparison | 88 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger/.dev/experiments/346-validation/phase5/ledger/metrics.json | Whole original metrics | 247 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger/.dev/experiments/346-validation/phase5/ledger/validity.md | Whole original validity record | 90 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-ab-ctl-r1/.dev/experiments/346-validation/phase4/ctl-r1/metrics.json | Read lines 79-133, 215-234, 354-373, 415-474; all source bytes hashed by checker | 598 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-ab-ctl-r2/.dev/experiments/346-validation/phase4/ctl-r2/metrics.json | Read lines 135-152, 434-451, 729-746, 788-805, 900-939; all source bytes hashed by checker | 1449 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-ab-trt-r1/.dev/experiments/346-validation/phase4/trt-r1/metrics.json | Whole original metrics | 232 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-ab-trt-r2/.dev/experiments/346-validation/phase4/trt-r2/metrics.json | Whole original metrics, including distinct all_findings field | 259 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/experiments/346-validation/phase4/flg-r1/metrics.json | Read lines 127-151, 353-377, 588-622, 675-686; all source bytes hashed by checker | 1470 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/experiments/346-validation/phase4/flg-r2/metrics.json | Read lines 220-258, 332-356, 472-498, 537-550; all source bytes hashed by checker | 1175 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/coordinator-log.md | Whole build record, scoped tests, incomplete minfix and disk-write gap | 52 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/s1v-log.md | Whole live-run and pause log | 113 |
| /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/progress.md | Whole authoritative acceptance ledger | 23 |
| /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/review-5.md | Whole final acceptance review | 14 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/final-bundle/runtime/s1v/stoprule-r1-integrity.txt | Whole saved mismatch output | 1 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/final-bundle/runtime/s1v/last-stoprule-T05.json | Whole failed completion receipt | 1 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/final-bundle/runtime/s1v/driver-stoprule.log | Whole saved driver log | 24 |
| /home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py | Read lines 1750-1849, transcript extraction and matching | 100 read (partial) |
| /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py | Read lines 860-911, spec write followed by later unhandled log/state writes | 52 read (partial) |
| /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail/.dev/experiments/346-validation/phase5/ponytail/reviews/installed/fix_audit.py | Read lines 992-1096, original measured verdict function | 105 read (partial) |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/baseline-metrics.json | Read lines 1-50, historical measured-loop definition and later constrained-stage distinction | 50 read (partial) |

Additional sources read in full:

| Source Doc | Assigned Section Range | Line Count |
|------------|--------------------------|------------|
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/install-log.md | Earlier additive installation record, not current machine-state proof | 22 |
| /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/final-bundle/SNAPSHOT-STATE.txt | Current preservation caveat and pending final inventory | 3 |

## Per-Source Fidelity

| Source | Semantic Coverage | Detail Preservation | Phantom-Coverage Check | Operational Completeness | Verdict |
|--------|---------------------|------------------------|---------------------------|------------------------------|---------|
| Fixed decisions and phase-4 comparison reports | The final report preserves the one-scenario scope and failed joint success screen. | Means 6, 5.5 and 3.5 and spreads 4 and 5 match; registered rounded growth is distinguished from byte-derived growth. | No statistical significance, causal proof or successful convergence is claimed. | Installation instability, failed count condition and incomplete repetitions are disclosed. | PASS |
| Three original variant comparison reports and first-run fidelity review | New label proxies, blockers, unresolved prior labels, owner carry-forward and audit unions remain separate. | Diffgate 2 with uncertain union 5-6; ponytail 0 with conservative carry 1 and 91-byte audit saving; ledger 3 new, 3 prior, union 13 (11-14) match. | Package-quality PASS is not promoted into experimental success. | Restricted coverage, model changes, invalid parser zero, exposure and target replacement remain explicit. | PASS |
| Corrected repeat plan | The unsupported repeat authorization is acknowledged as a coordinator deviation. | Four first reviews and a paused revision are not counted as completed replicates. | Historical proposed steps are not called authorized execution. | Design and manifest remain expressly pending; no false completion claim. | PASS |
| Original nine metrics files and final-summary.json | All nine per-round proxy arrays and endpoint bytes match the original measurement files, not just bundled copies. | Control endpoints 91,102 and 97,814; exact-427 71,113 and 78,715; flagged-427 73,807 and 76,328; variants 63,717, 70,488 and 70,565. Growth arithmetic and conservative endpoint details agree. | The diffgate 5-6 bound is explicitly attributed to the independent review rather than falsely presented as the recorder's original exact 6. | Summary distinguishes failed/unbuilt variants and paused exploratory runs. | PASS |
| Minfix progress ledger and final task-3 review | Only tasks 1 and 2 are complete; task 3 halted twice. | The final review records 84 tests passing while the in-budget appended-sentence acceptance condition fails. | Passing tests are not called task acceptance or a runnable command. | Tasks 4-8 remain unbuilt in both source and report. | PASS |
| Stoprule run log, integrity output, failed receipt and transcript extraction source | Eight claims, six confirmed, two minor, format accepted, provenance mismatch and failed settlement agree. | The extractor only matches saved replies against Agent/Task tool-result text. | A failed first review is not promoted into a completed convergence loop; no reviser is claimed. | Failure is preserved without a product patch or relaxed gate. | PASS |
| Ponytail audit application and verdict source | Specification write precedes later log/state writes; the separate verdict function rejects missing parsed prior rows. | Source corroborates both the disk-error safety gap and parser mechanism in the report. | The invalid automatic zero is rejected; independent reading is not called an automated pass. | No guarantee of unchanged input after every failure is made. | PASS |
| final_report_check.py | Narrow evidence-consistency checks, not full semantic verification. | Explicit trt-r2 adapter reads all_findings; the other arms use findings_total. Nine hashes and numerical extraction are recomputed; several interpretive endpoint details are constants. | Token-presence assertions are only substring checks, not proof that the surrounding prose is true. The report expressly says the mechanical check is not independent substantive review. | This review observed one default read-only run exiting successfully; no --write, experiment, install or source mutation. | PASS |

## Overall Verdict: PASS

This is a source-fidelity PASS for the final comparison and numeric companion, not a finding that any treatment converged, any prototype is safe to ship, or the overall requested program is complete. No blocking false statement, arithmetic/source mismatch or missing required limit was found in the reviewed comparison. The design, final design review and complete final checksum inventory are honestly pending and are not grounds for failing this report.

## Issues Found

| # | Severity | Source | Issue | Required Fix |
|---|----------|--------|-------|---------------|

No blocking or minor report changes required. The original first-run authorization FAIL remains valid historical evidence, and the final report acknowledges rather than erases it.

## QA Complete

**Self-Audit:** Began by trying to disprove the flattering count reductions and the apparent zero. Read all three original variant comparisons, metrics and validity records; checked all six comparator files directly at the count/endpoint fields (whole treatment files, bounded control/flag ranges); independently followed the label/blocker distinction, unresolved prior rows, owner carry-forward, uncertain unions and unmatched audit instruments. The recorder's diffgate union 6 and the independent review's plausible 5-6 are both preserved; ledger's 15-row script headline is not mistaken for its new-label proxy 3 or union 13 (11-14). Ponytail's parser zero is rejected, its conservative carry 1 and orphan candidate remain visible, and its 91-byte audit effect is not credited with the much larger earlier growth restraint. The historical table is a matched three-review endpoint, not an assertion that its later constrained one-line review never passed.

Checked the fixed screen rather than substituting a weaker selection rule: diffgate's count improvement 4 only equals the control spread 4; flagged 427 improves by 2.5 against spread 5; exact 427 improves by 0.5 against spread 4. The final report does not claim statistical significance, matched full-document audit improvement or a valid repeated proposed-variant effect. It preserves the corrected authorization hold and treats the four exploratory first reviews as incomplete, not additional completed loops. The minfix ledger and final task-3 review show failed acceptance despite 84 tests passing; stoprule's original integrity mismatch output and failed receipt show an invalid first review with no reviser. Build-test passes are not convergence results.

Read the actual ponytail write ordering and original verdict function, and the stoprule transcript extraction boundary. The final report accurately discloses that a later disk/log error can leave a ponytail spec edit applied. The original ponytail recorder additionally lacks a whole-machine filesystem-write audit; no such audit was performed here, and bounded hashes/transcript observations are not treated as proof against arbitrary external writes. Earlier installation hashes are historical records, not current configuration claims. The stale bundle inventory is explicitly pending, not falsely certified.

Inspected the full checker before execution. Its explicit per-arm adapter correctly handles trt-r2's original all_findings field. Some endpoint interpretations are hard-coded, and the report prose checks are substring/link/placeholder checks, so this PASS depends on the independent source readings above, not those assertions alone. The checker-development schema failure described in the review brief is not experimental convergence evidence. This review itself observed one additional read-only run, with no --write, returning: `PASS: 9 source measurements, endpoint arithmetic, numeric assertions, local report links and no placeholders`.

**Limits and retained negative evidence:** Did not regrade controls, conduct another substantive specification review, rerun builds or experiments, inspect live orchestration state, verify every raw session record anew, regenerate the final inventory or change any install. Historical polling/worker cancellation statements are coordinator-recorded history, not a new live-process audit. The initial Edit of this QA stub was rejected by the freshness hook; a tracked Read followed by the same bounded Edit succeeded. No bypass or source modification was used. Only this agreed QA file was written, incrementally from the governing template. All intermediate evidence was left intact. No commits, pushes or publication.

VERDICT: PASS
