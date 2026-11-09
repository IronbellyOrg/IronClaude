# Position summary

C is the strongest safety and measurement contract for a genuinely terminal audit: it covers both fix cycles, preserves the raw review-3 result, and makes missing evidence a failed treatment rather than a hidden fallback. Its placement cannot improve the registered raw review-3 count, and the new attribution and byte-share evidence invalidate its optimistic numerical model. Choose C only for an explicitly approved terminal-cleanup experiment, not as a demonstrated convergence solution.

# Steelman

## A

A's strongest argument is that review 3 should inspect the document that ships, using the same measurement instrument as the controls. Its script-owned edits, all-or-nothing validation, preserved original command, and independent inspection of shrink text are valuable safeguards (A sections 3, 8, 14). Its emphasis on shrinking oversized blocking fixes is better directed than minor-only deletion: the attribution evidence identifies seven potentially avoidable blocking-fix findings, against only one blocking finding anchored on a minor fix (evidence-attribution.md, Totals and implied predictions).

## B

B's strongest argument is that the script should nominate obvious candidates while the model handles only necessity and severity judgments. Protecting every report-blocking hunk from whole reversion is safer than trusting an auditor's downgrade, and the report/apply consistency check and blind safety re-grade are useful falsifiers (B sections 7, 10, 14). The proposed no-model comparison is also valuable: it can show whether the extra reviewer earns its cost rather than assuming that it does (B sections 9.4, 14.1).

# Strengths claimed

1. C distinguishes a changed historical measurement from a new terminal judgment. It explicitly says "Never relabel the latter as review 3" and reports pre-cleanup and terminal growth separately (C sections 1, 11). This prevents a smaller final document or a downgraded terminal finding from being presented as a lower raw review-3 count.

2. C defines coverage by applied finding, not merely by a surviving hunk. Its replayed ledger includes both cycles and superseded contributions; missing attribution produces E-COVERAGE rather than an automatic deletion candidate (C section 4). This matters because minor-byte-share.md, Reading, says most minor fixes share a line with a blocking fix, and evidence-attribution.md, flg-r1, records bare numeric finding ids.

3. C specifies tests for failure boundaries that ordinary exact-string application does not cover: shared paragraphs, overwritten cycle-1 fixes, an invalid last row, stale hashes, CRLF and UTF-8, interrupted replacement, and missing receipts (C section 8). These are proposed acceptance tests, not executed results or proof of semantic safety.

4. C separates atomic replacement from recoverable completion. A durable intent precedes replacement, and resume reconciles exact old/new hashes before completing a receipt (C section 6). That handles the crash between target replacement and receipt writing, not only a process that finishes normally.

5. C requires evidence of one actual plugin Skill invocation and fails without it; a fake auditor only tests wiring (C sections 3, 8). This preserves the treatment being measured instead of letting an inline substitute mutate the target under the same experiment name.

6. C refuses to treat deletion as resolution by itself. A genuine blocker reverted without equivalent protection remains open; a requirement-to-result witness is required, and its truth remains a model judgment (C sections 6, 7). That is directly aligned with evidence-attribution.md, flg-r2, which classifies N12 as a necessary-blocking-fix defect and says dropping both defective halves reopens N5.

# Weaknesses identified in others

1. A overstates the evidence for its N5 deletion alternative. A section 2 claims deleting the proof claim would close N5 and avoid N12; evidence-attribution.md, flg-r2, explicitly reaches the contrary judgment. Neither reader's interpretation is mechanical proof, but the conflict defeats using this example as settled support for a predicted successful shrink.

2. A's final downgrade authority can conceal a real regression. A sections 8 and 9 remove validated-minor ids from the blocking set even if review 3 lists them open, while restored baseline spans become unchanged-origin notes. Independent review is therefore not a complete safety net for wrongly downgraded blocking fixes, as A itself admits in section 16.

3. B's claim that the mechanism "cannot corrupt the spec" is too strong (B section 1). Exact-string application prevents some mechanical errors, not a valid but incorrect shrink or an unstated dependency on reverted minor text; B section 15 acknowledges both. C's tests and preservation requirements make these risks explicit without claiming to prove them absent.

4. Both A and B assume that hunk attribution provides enough separation for useful deletion (A sections 3, 7; B sections 6, 7). minor-byte-share.md measures only 6% and 27% minor-only added characters across the two cycles of flg-r2, with most minor changes mixed into blocking lines. B's conservative keep rule helps safety but further limits deletion yield; neither design earns its central effect estimate from row counts.

5. A and B reinterpret "never re-reviewed" to mean that the audit table is not regraded, while review 3 still inspects kept and shrunk text (A section 3; B section 3.1). That is a defensible safety trade, but not the literal terminal property C preserves. This is a choice for the owner, not a constraint satisfied by changing its meaning.

6. B's suggested cumulative-baseline shortcut does not replace historical attribution (B sections 3.2, 16 Q3). Comparing original and final snapshots cannot by itself recover overwritten intermediate fixes or distinguish cycle-qualified ids; C's snapshots and replayed ledger address that missing test surface (C section 4).

# Concessions

1. C's primary cannot lower raw review-3 findings because it runs after that report is written. A and B have the superior placement if improving that registered endpoint is mandatory. C section 11 correctly requires reporting failure for that objective even if terminal cleanup helps.

2. C's section-10 planning model used the 9/15 minor row share as exposure and assumed a 20% terminal reduction. Withdraw the resulting terminal-blocking 2.0 and growth 24% point predictions: evidence-attribution.md finds only 1/28 blocking findings on minor-fix anchors, and minor-byte-share.md rejects using row share as removable hunk share. The raw 3.5 unchanged prediction is a timing consequence, not an estimated cleanup effect.

3. The byte-share evidence counts added characters, not a universally measured UTF-8 byte rate. Its approximate 32.1% to 27.8% growth illustration concerns whole-line minor-only reverts across both cycles of one run; it is not a forecast for C's sentence-level ledger workflow.

4. C's terminal edits lack an independent in-loop semantic check. A preservation witness can be false, and passing schema and recovery tests cannot establish that required behavior survives. B's blocking-revert ban is the safer default until the owner explicitly accepts a different terminal severity policy.

5. C adds ledger work, snapshots, schema handling and recovery complexity to both revisers and the coordinator (C sections 12, 13). There is no evidence yet that saved document text justifies that maintenance cost or that a real plugin obeys the requested structured output.

6. C's separate heading preserves the seven-bullet shape, not identical overall behavior: terminal cleanup and terminal grading are explicit exceptions. C section 9 must not be used to claim unchanged 427 semantics, and its proposed plugin mirror should remain contingent on verified distribution requirements rather than assumed necessary work.

# Shared-assumption responses

A-001: REJECT. A material blocking-count reduction from minor-only reverts is unsupported: evidence-attribution.md estimates about 0.17 fewer blocking findings per run, before replacement findings or restored defects.
A-002: QUALIFY. Inline-id mapping is evidenced for flg-r2, not all runs; bare numeric ids and shared lines require verified coverage or an explicit attribution ledger, not presumed mapping.
A-003: QUALIFY. Nested plugin access remains unverified; require a disposable live Skill-call receipt before treating a run as the intended treatment (C sections 3, 8).
A-004: REJECT. Whole-line hunks do not reliably separate minor and blocking contributions; the measured minor-only shares are 6% and 27% in the one measured run (minor-byte-share.md).
A-005: QUALIFY. Concrete wrong outcomes support the strict grading rule, but do not authorize silent override of protected categories or guarantee any downgrade; raw labels and blocking status remain separate (C section 7; evidence-attribution.md, flg-r1).

# Per-point positions

X-001: C is superior for literal terminality: one audit after review 3 actually has no subsequent in-loop review of its edits; its safety cost must remain explicit (C sections 1, 13).
X-002: merge: use B's ban on whole reversion of report-blocking fixes by default, retaining C's separate terminal grades and preservation records; any authority to override protected grades needs an explicit owner decision.
X-003: C is superior for treatment integrity: missing plugin or missing actual invocation means no edits and an incomplete treatment, not a substitute rubric counted as equivalent (C section 3).
X-004: C is superior in measurement honesty: it explicitly fails the raw-count objective rather than replacing it with terminal blocking; A and B are correct that only pre-review intervention can affect that report.
X-005: merge: reject all three reduction models based on minor-fix prevalence, measure actual attribution and retained outcomes, and investigate blocking-fix shrink separately; the attribution evidence supports no large minor-revert effect.
X-006: C is superior for complete historical coverage: a command-name substitution cannot supply missing cycle ledgers and intermediate snapshots; record that instrumentation as treatment cost rather than claiming an unchanged brief.
C-001: merge: use C after review 3 only for an approved terminal-cleanup endpoint; if raw review-3 improvement is non-negotiable, use B's pre-review placement and explicitly concede that audit edits are reviewed.
C-002: C is superior for the stated all-fixes audit: both cycles and superseded findings receive a row; cycle-2-only designs leave known earlier work unaudited (C section 4).
C-003: C is superior for attributable coverage: replayed edit ledgers catch missing and overwritten contributions; hunk ids alone cannot resolve the mixed-line and numeric-id evidence.
C-004: merge: retain C's exact ancestor restoration, grouped dependencies and preservation witnesses, but adopt B's protected-blocking whole-revert ban until separate override authority is approved.
C-009: C is superior for traceability: immutable raw verdict plus a separately named terminal result avoids rewriting history, with every open id covered and audit errors counted separately from spec blockers (C section 7).
C-011: merge: retain C's unchanged raw endpoint and failure declaration, withdraw its terminal point predictions and A/B's unsupported reductions, and treat attribution-based shrink opportunities as hypotheses rather than guaranteed successes.
