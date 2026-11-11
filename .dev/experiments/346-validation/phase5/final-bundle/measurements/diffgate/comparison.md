# S1 diffgate measurement comparison

## DRAFT per-round comparison
Measurement only. There is **no success verdict for the variant**. Counts below keep the original critical-plus-major severity proxy separate from new findings, carried open findings, script-confirmed blockers and the independent audit. Source of every numeric comparison: `metrics.json`; copied read-only comparator inputs: `reviews/comparators/` and `reviews/provenance/phase2/S1/baseline-metrics.json`.

### Original counting rule, unchanged

| Run | Review | New numbered findings | New CRITICAL+MAJOR proxy | Report blocking grade | MINOR severity labels |
|---|---|---:|---:|---:|---:|
| Historical original | 1 | 24 | 18 | not separately graded | 6 |
| Historical original | 2 | 13 | 10 | not separately graded | 3 |
| Historical original | 3 | 14 | 8 | not separately graded | 6 |
| Control replicate 1 | 1 | 19 | 11 | 11 | 8 |
| Control replicate 1 | 2 | 15 | 9 | 9 | 6 |
| Control replicate 1 | 3 | 11 | 8 | 8 | 3 |
| Control replicate 2 | 1 | 21 | 12 | 12 | 9 |
| Control replicate 2 | 2 | 17 | 7 | 7 | 10 |
| Control replicate 2 | 3 | 7 | 4 | 4 | 3 |
| Arm B replicate 1 | 1 | 22 | 16 | 11 | 6 |
| Arm B replicate 1 | 2 | 12 | 5 | 4 | 7 |
| Arm B replicate 1 | 3 | 10 | 6 | 4 | 4 |
| Arm B replicate 2 | 1 | 22 | 17 | 13 | 5 |
| Arm B replicate 2 | 2 | 11 | 6 | 6 | 5 |
| Arm B replicate 2 | 3 | 4 | 1 | 1 | 3 |
| Diffgate, single run | 1 | 13 | 7 | 7 | 6 |
| Diffgate, single run | 2 | 5 | 2 new, plus 1 open prior | 3 including prior | 3 new |
| Diffgate, single run | 3 | 3 | 2 | 2 | 1 new |

Arm B means the earlier 427 command with re-review/baseline flags added by the experiment; it is not this variant. Its non-blocking grade may include MAJOR labels, so severity proxy and blocking are not interchangeable. Historical MINOR values are taken from the baseline splits, not inferred by applying present grading.

### Additional counts, not substituted into the old proxy

| Review | New total | New proxy | Unresolved prior proxy | Current open proxy | Script confirmed blockers | Script `proxy_all` | Cumulative owner-counted deferred/demoted/withdrawn proxy |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 13 | 7 | 0 | 7 | 7 | 7 | 0 |
| 2 | 5 | 2 | 1 | 3 | 3 | 3 | 0 |
| 3 | 3 | 2 | 0 | 2 | 2 | 2 | 0 |

The second review leaves the retry-directory finding open (R1.3), separately from its five new findings. The third resolves all three prior blockers and raises two new blockers plus one new minor. Citation rows that duplicate numbered findings are not counted twice. Script acceptance `clean` means machine-format acceptance, not a clean specification PASS. Every final review ends `verdict: FAIL`, including review 3 at the cap.

### Document size at matched points

| Run | Original bytes | After first fix bytes | After second fix / review-3 bytes | Growth after two fixes |
|---|---:|---:|---:|---:|
| Historical original | 57763 | 82643 | 92194 | 59.6% |
| Control replicate 1 | 57763 | 71528 | 91102 | 57.72% |
| Control replicate 2 | 57763 | 76214 | 97814 | 69.30% |
| Arm B replicate 1 | 57763 | 67886 | 73807 | 27.78% |
| Arm B replicate 2 | 57763 | 70255 | 76328 | 32.14% |
| Diffgate, frozen snapshots | 57763 | 62054 | 63717 | 10.307636% |

Variant increases: 4291 bytes in fix 1 (7.428631%), 1663 in fix 2 (2.679924% of version 2), 5954 cumulatively. All three snapshots contain 285 newline-terminated lines, so line growth is 0%; much content was added within existing long table rows. The endpoint is the verified version-3 history snapshot, not the externally rewritten live file. No third revision ran.

### Fix-origin split and resource accounting

Baseline-style analyst grouping for new findings: second review, 2 strict / 3 partial / 0 pre-existing out of 5 (strict share 0.4; strict+partial 1.0); third review, 2 strict / 1 partial / 0 pre-existing out of 3 (strict share 0.666667; strict+partial 1.0). Reasons and IDs are in each round's `M3` in `metrics.json`. In particular, the report itself says the final P0 step-4 failure predates the last revision in substance, despite its changed anchor; it is partial, not automatically strict. Historical original review 2 reports all 13 introduced or exposed, while review 3 has 10 strict / 3 partial / 1 pre-existing out of 14. These are report/analyst groupings, not empirical causal attribution. Raw machine changed/unchanged labels are retained separately: 4/1 at review 2 and 3/0 at review 3. No new finding is on wholly untouched text without a stated changed dependency.

The five loop dispatches total 186 tools and 207181 output tokens, with 32.894467 summed dispatch-window wall minutes and no observed terminal rate-limit error inside those windows. These figures exclude coordinator shell work, the failed audit, replacement audit, and later user-owned work in the first-review session. `validity.md` and `reviews/session-metrics.json` retain uncached/cache inputs, whole-session totals, interruption windows and existing audit-helper costs separately.

## Last-round arithmetic against fixed thresholds
The fixed control mean is **6** last-review proxy findings and **63.51%** growth. The corresponding numeric limits are **3** proxy findings (6 x 0.5) and **44.457%** growth (63.51 x 0.7). The growth limit deliberately uses the supplied rounded comparator mean, not a newly substituted denominator.

- Original-counting endpoint proxy: **2**, which is 4 below the control mean (66.666667% lower) and numerically at or below 3. Adding the owner-required cumulative deferred/demoted/withdrawn proxy count of 0 leaves 2.
- Frozen document growth: **10.307636%**, numerically below 44.457% by 34.149364 percentage points; below control mean by 53.202364 points (83.770058% lower relative growth).
- Earlier Arm B last-review proxies are **6** and **1**, mean **3.5**; growth mean is **29.96%**. These are comparator numbers, not repeat measurements by this recorder.
- Independent-audit union is **6**, equal to the control mean and above the proxy limit by **3**. That union is NOT the historical new-findings proxy: comparing it directly with unaudited controls is apples-to-oranges, so it is shown alongside rather than replacing the old metric.

**No convergence and no success conclusion.** Review 3 still ends FAIL. One variant run cannot establish between-replicate robustness, the variant's replicate spread, superiority of variance, or the all-replicates conditions. The existing control proxy spread is 4 and growth spread 11.58 points; Arm B proxy spread is 5, but no within-variant spread exists to compare with them.

## Independent audit overlap and owner-adjusted open counts
Only `reviews/blindness-audit-frozen.md` supplies final independent-audit findings. Recount: **4 distinct findings, all blocking MAJOR, no CRITICAL or MINOR**. Two compare at changed anchors and two at original anchors; repeated guard-table attacks do not add more findings. `reviews/blindness-audit.md` is preserved as failed mixed-target evidence, excluded from counts.

Deduplication was performed BEFORE adding audit counts. Compare concrete failure mechanisms/outcomes with both endpoint blockers, not merely section numbers:

| Frozen audit finding | Relation to endpoint missing-resume blocker (R3.1) | Relation to endpoint P0-field assertion blocker (R3.2) | Classification |
|---|---|---|---|
| 1: early all-command phase promise before gate/safety delivery | Different rollout eligibility, not retry resume | Later-phase conversion timing, not P0 report-field access | Original anchor |
| 2: tasklist child reflect call lacks mandatory report directory | Different child argument rejection, before child audit | Missing child argument, not existing-report schema | Changed callee anchor, unchanged caller |
| 3: blanket blocked gate test rejects safe-default completion | Different acceptance outcome, no retry | P2 safe-default branch, not P0 schema assertion | Original anchor |
| 4: archived report pointers still name reused output paths | Non-resumable output archival/pointer misattribution, not an explicit-resume command lacking a resume flag | Different operation and wrong outcome | Changed retry-procedure anchor |

Thus **overlap = 0**, and **deduplicated union = 2 + 4 - 0 = 6**. Published bounds are the same, overlap [0,0], union [6,6], because no unresolved duplicate remains under this mechanism/outcome rule. The full pairwise rationale is also recorded in `metrics.json.independent_audit.overlap_checks`. Similar underlying sections and shared ancestral finding chains do not make these the same endpoint defect.

No critical/major finding was cumulatively deferred, demoted or withdrawn in any loop round, so the owner's adjustment adds **0**. Declined minor notes are separately visible and are not relabelled as critical/major. A changed anchor alone proves neither that the loop closed this exact audit defect earlier nor that a revision caused it; no such claim is made.

## What could not be measured
Continuous installation/WORKER-CONTRACT stability during this run is unknown: the supplied watcher ended before it began. Exact exclusive work time and pre-terminal-error API waiting are unknown; error-to-next-response gaps are reported instead. Coordinator-shell token costs cannot be assigned reliably from the shared coordinator session. A single replicate cannot supply between-replicate robustness or a variance estimate. These are explicit unknowns, not zero-valued measurements; see `metrics.json.not_recoverable` and `validity.md`.

## Limitations (at most eight)
1. **One variant replicate only:** no evidence for between-replicate robustness or variance superiority, and no all-replicates success decision.
2. **Scope differs:** computed-surface re-review and blocking-owned revisions exclude work that full-document/all-confirmed-findings comparators allowed. Lower growth does not isolate the computed-diff mechanism.
3. **Known answer-key exposure:** round-1 reviewer/reviser inspected master contract implementation. WORKER-CONTRACT is present for phase 5, unlike the isolated phase-4 comparators; explicit read covariates are retained.
4. **Installation monitoring gap:** phase-4 watcher has no coverage over phase 5. Matching installed and loaded command bodies is point evidence, not continuous stability proof.
5. **External target replacement:** live-target isolation fails. Frozen, hash-verified history salvages endpoint measurement, not untouched-run validity; the partial mixed audit is excluded.
6. **Replacement audit differs:** fresh frozen input brief and Arm B alias after a failed audit, plus actual gpt-6.1-sol messages after rate-limit/model-selection interruption. It is not a same-model, uninterrupted continuation.
7. **Metric meanings differ:** severity proxy, script-confirmed blockers, cumulative owner adjustment, audit union, changed anchors and strict/partial origin are separate. Audit union against unaudited controls and changed=>caused conversions would be apples-to-oranges.
8. **Resource boundaries differ:** session reuse, coordinator-shell script work, excluded failed audit, separate audit helper and unrecoverable waiting prevent simple total-cost attribution. The five core loop windows themselves show no terminal rate-limit failure.

## Self-Audit
Recounted numbered report rows and machine FINDING rows independently, checked their IDs/severity against machine results, and kept the second review's one open prior separate. Recomputed all snapshot byte/line growth and threshold arithmetic, matched copied comparator values without regrading, verified actual Skill calls/loaded command bodies and per-step model windows, checked disposition duplication and cumulative owner adjustments, and compared all four audit mechanisms with both endpoint blockers before adding counts. Preserved the failed partial audit without using it as final evidence.

The runnable consistency check, `reviews/package_check.py`, verifies source-copy hashes, unchanged loop/frozen source hashes, source/session pointers, reports versus checked snapshots plus closing blocks, counts, scope anchors, all token classes, delivered briefs, exact growth and threshold arithmetic. Its machine result is `reviews/package-check.json`. No unresolved package finding remained; this self-check does not constitute another independent model review or specification fix pass. Unknowns remain explicitly unknown rather than being invented, and no treatment-success verdict is made.

## Evidence-package quality verdict
**PASS** (evidence-package quality only, not variant success or experimental-validity approval).
