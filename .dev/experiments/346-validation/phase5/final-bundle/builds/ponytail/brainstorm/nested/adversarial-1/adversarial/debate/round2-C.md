# Round 2, advocate C, QA

## 1. Response to criticisms of C

1. **Placement cannot move raw review 3 (A and B).** Conceded. Run P for the registered endpoint; withdraw C's terminal placement from this experiment. P reviews audit-edited text, so it does not literally satisfy an unreviewed terminal edit. Record that trade explicitly, rather than claim both properties.
2. **Ledgers change Arm B's treatment and cost too much (A and B).** Conceded for P. My ledger solves historical coverage, but cycle-2 scope does not require that problem to be solved. Keep frozen baseline/current snapshots and the script's edit receipt, not reviser-authored ledgers or the proposed extra schema file.
3. **FR-8/FR-9 override and unreviewed edits are unsafe (A and B).** Conceded. No whole revert of report-blocking text, no override of protected categories, and no text change after review 3. Preserving an id does not prove that its required outcome survives a deletion.
4. **Growth prediction used row share (A and B).** Already withdrawn. Character additions, net byte savings and finding counts are three different quantities. None can substitute for another.
5. **Fail-closed plugin rule loses a replicate (A and B).** Separate product continuation from experiment validity. Plain 427 may finish safely after a plugin failure. That attempt still belongs in the failure accounting; it cannot count as a successful plugin treatment or disappear through replacement.
6. **B says C conceded its ledgers and plugin rule in round 1.** Too broad. Round 1 acknowledged ledger cost and retained the plugin integrity requirement. I now drop the ledger for P, but keep proof of an actual Skill invocation for the plugin-specific claim.

## 2. Updated assessment of A and B

A supplies the right placement, limited command change and emphasis on smaller blocking fixes. Its latest claim that deleting words cannot introduce an unchecked fact is false: removing a negation or qualifier can reverse or broaden a claim. Review 3 is a safeguard, not proof that deletion is harmless. Its 50% capture rate and reduced replacement-finding penalty remain assumptions.

B is now the closer implementation base: blocking protection, unknown-grade protection, consistency checks and fewer command surfaces. Its round-2 correction of the cumulative-baseline shortcut is important. Keep B's narrower safety claims, not its earlier guarantee that the spec cannot be corrupted. Reject B's original rule that check/apply failures are voided and rerun: those failures are measured reliability outcomes of this mechanism.

## 3. New evidence and checks of B's round-2 claims

Source roots: R = `/home/coder/workspaces/worktrees/IronClaude`; W = `R/bs346-ponytail`. Each run report below is under `R/<run>/.dev/orca-command-refactor/review/`; each saved spec is under that run's `specs/history/`.

1. **Four severity formats: confirmed.** `exp346-ab-flg-r1/spec-panel-round2.md`, Numbered findings, uses separate Severity and Grade cells; flg-r2 uses prose `CRITICAL, blocking`; trt-r1 uses `Severity MAJOR, blocking`; trt-r2 defines B/M and uses `MAJOR, B`. This needs four fixture families, not merely a search for severity words anywhere on a line. Citation text and recommendations can contain other grades.
2. **New parser trap within those formats.** flg-r1's R2-7 row says `MAJOR (FR-8 GAP)` in Severity but `minor` in Grade. A bare `blocking` search also matches `non-blocking`. Preserve claimed severity, explicit blocking status and protected-category status separately; conflicts or unknowns protect text. This is a concrete regression fixture, not hypothetical format drift.
3. **flg-r1 cycle 2 is attributable: confirmed in scope, not in percentage.** Its `spec-v3-after-round2.md` explicitly cites R2-1 through R2-4 in WC-4, WC-7 and acceptance steps, plus minor ids elsewhere. The first disposition's bare numbers do not invalidate cycle-2 mapping. I did not reproduce B's 33% share or five-untagged-hunk count.
4. **Controls cite no ids: literally false, operational warning sound.** ctl-r1's saved v3 has no matches for the examined finding-id forms. ctl-r2's saved v3 Decisions table contains F1, F2, F3, N1, N5 and N6, mostly as rationale references rather than comprehensive edit attribution. Do not turn incidental references into proof of coverage. B's own 29-of-30-unattributed result is compatible with this distinction; I did not reproduce that count.
5. **New measurement limitation.** `W/.dev/brainstorms/346-ponytail/enrichment/minor_share.py` counts character insertions/replacements after splitting lines. It neither measures UTF-8 net revert savings nor preserves newline accounting. Its id expression also cannot match R2-1 intact. B used an adaptation, so this does not refute B's measurements; it means the supplied helper cannot validate them unchanged. Measure actual proposed output bytes before forecasting savings.
6. **New static-test limitation.** `W/tests/skills/test_spec_panel_review_loop.py` names only the original source and plugin commands; its seven-bullet assertion will not automatically cover the variant. `W/tests/skills/test_review_severity_rule.py` scans tracked files, so an untracked new command can escape its broad phrase scan. Variant-specific direct-file tests are mandatory before promotion.

## 4. Positions on the open points

### O1. Placement to run
Winner: merge: P now, with B's evidence-led follow-up and a stronger cause check.

Pre-register (a), but trigger it only when at least a third of leftover critical+major findings, pooled across valid P replicates, are independently attributed to cycle-1 changes that a smaller cycle-1 fix plausibly could have avoided. Use the attribution file's distinctions, not origin=changed alone; older text on a touched line does not qualify. Zero leftovers means no trigger, and unresolved attribution cannot establish it. A mean above 3 still means the success bar failed, but does not identify which follow-up to run. The one-third threshold is a planning choice, not a measured optimum. Any follow-up is exploratory, not a rescue of P's original result.

### O2. Shrink rule
Winner: merge: B's deletion or exact ancestor restoration, with aligned spans and blocking protection.

Allow exact deletion of words or restoration of the corresponding span from the frozen cycle-2 baseline. An arbitrary substring found elsewhere in that baseline is not an ancestor and must fail. Restoration is a revert even when labelled shrink, so it cannot bypass the report-blocking or protected-category ban; such rows may only delete while retaining blocking attribution elsewhere in the hunk. Minor ids may disappear only with recorded minor-revert approval. Use exact token identity and order, not case/punctuation folding that could admit a changed literal, operator or negation. Neither permitted operation proves semantic preservation; retain review 3 and the blind safety check.

### O3. Scope
Winner: A and B, cycle 2 only for P.

All seven class-B anchors in `enrichment/evidence-attribution.md` concern cycle-2 fixes. That supports the bounded pilot, not a claim that earlier work is safe or fully audited. Baseline replacement alone cannot widen scope because report 2 does not supply all cycle-1 grades. Keep unknown, foreign and individually unattributed text unless attribution is established; the majority-unattributed skip guard is not permission to delete the remaining unknown hunks. Under (a), each audit uses its own cycle's baseline and report.

### O4. Consent
Winner: merge: A's name substitution, conditional on explicit owner approval of the variant's editing contract.

Selecting the documented editing variant can express consent for one bounded scripted application; a second flag adds no meaningful protection if the coordinator inserts it automatically. But this debate is not user authorization, and a review-only command cannot silently acquire permission through an internal rename. Before S1, record owner approval of that contract, target and scope. Without it, do not mutate. Preserve the original command and disclose the variant's editing behavior in its usage and boundaries. No new consent flag is needed for this approved pilot.

### O5. Minimum tests and run validity
Winner: merge: C's failure-boundary tests, B's consistency checks and explicit assigned-arm accounting.

These are proposed acceptance tests, not executed results. The minimum is the following parameterized suite; none requires a full historical ledger.

**Script unit tests**
- Hunk construction: empty and whitespace-only diffs, insert/delete/replace, the four hunk classes, numeric and hyphenated ids, whole-token boundaries, ids surviving only in old text, and incidental rationale references.
- Grade parsing: all four real formats, B/M key, multiline records, non-blocking MAJOR, FR-8 conflict, unknown grade, duplicate/conflicting id definitions and quoted severity words. Ambiguity protects, never enables a revert.
- Coverage: missing/duplicate/foreign rows, invalid enums, empty audit with nonempty diff, shared blocking/minor hunk and conflicting verdicts. Test the majority-unattributed boundary below, at and above 50%; individually unknown text stays protected.
- Edit policy: blocking whole-revert rejection, N5-style required-outcome regression fixture, exact deletion, aligned ancestor restore, rejection of a baseline span from elsewhere, retained blocking ids outside the edited clause, and approved minor-id removal. Semantic safety still needs live review.
- Exact application: absent/repeated/empty old span, overlapping rows, cascading replacements, out-of-scope edits, invalid last row and stale inputs all leave target bytes unchanged. Safe SKIP never closes an unapplied finding; one id across several hunks closes only after every required revert succeeds.
- Bytes and recovery: UTF-8, CRLF, trailing newline, JSON escaping, symlink/path rejection, same-target concurrency, atomic replacement failure and interruption before/after replacement and receipt. Retry uses recorded before/after hashes, never merely finding new text somewhere; no double application or PASS without a consistent receipt.
- Verdict: raw report FAIL cannot become PASS, open/regressed blockers survive, missing/duplicate machine lines and report/table/apply disagreement fail closed, upgrades remain visible, and audit errors are distinct from document blockers.

**Static variant-command tests**
- Original source and plugin commands remain byte-identical to frozen baselines. Removing only enumerated variant additions and identity changes reproduces the source command; do not weaken existing tests.
- Pin unchanged seven bullets, severity model, precedence and cap. Put audit instructions under a separate heading; assert exactly one pre-review-3 trigger, cycle-2 scope, no review 4, no third fix cycle and no after-review-3 edits.
- Pin actual named Skill invocation, fresh auditor, literal brief transfer, script-only writes, consent contract, installed/project lookup order, explicit fallback label and unchanged raw metric names. Scan new files directly, not only tracked-file enumeration.
- Pin unchanged Arm B briefs except the registered command-name substitution and allowed variant behavior. A fake-auditor wiring fixture tests ordering and failure continuation; a separate live nested Skill-call smoke test is required before S1.

**S1 run-validity rules**
- Freeze initial bytes/hash, source inventories, model/settings, command/helper/plugin versions, briefs, placement and metric definitions before both replicates. Record every started attempt and every replacement. Use actual byte counts and frozen raw review-3 reports; publish pre/post-audit growth, blocking and critical+major separately.
- Void causal comparison for wrong initial input, changed model/briefs, answer exposure, uncontrolled external writes, missing evidence that prevents reconstruction, cap breach or wrong placement. Keep the void attempt and reason visible. Do not tune between replicates; a repair starts a new versioned experiment.
- Plugin absent, failed actual invocation or inline fallback means no valid plugin-treatment replicate, even if plain 427 finishes. Retain it in all-attempt reliability reporting; any replacement follows a fixed pre-registered policy, not a search for two successful runs.
- With correct inputs and invocation, malformed audit output, check failure, apply STOP, unattributed skip, safe no-op, regression, FAIL or poor metrics are outcomes, not grounds to void. Count assigned-arm results and separately show completed-treatment results. Unknown coverage or report integrity cannot earn PASS.
- Verify review 3 inspected the exact post-audit hash. Early ordinary termination is recorded, never forced to cycle 2; if raw R3 is absent, do not invent zero or silently drop it. Report the registered two-cycle comparison as incomplete unless an early-stop rule was fixed beforehand.
- Strict success retains mean critical+major at most 3, growth at most 44.4%, the registered per-replicate/control and spread conditions, and no confirmed audit-caused required-outcome regression. Blind safety re-grading is outside the loop and cannot trigger another repair or rewrite the raw result.

## 5. Final predicted numbers on the Arm B base

Predictions are planning judgments, not confidence intervals or observed effects. P means the merged pre-review-3 design; (a) audits each cycle; (b) follows the round-2 convention of triage before the first fix only. No forecast earns a clean PASS claim.

| Placement | Review-3 critical+major mean | Growth after two cycles |
|---|---:|---:|
| P | 3.3 | 27% |
| (a) | 3.2 | 26% |
| (b) | 3.5 | 27% |

- P: 3.5 minus 0.4 of the Arm B class-B opportunity plus 0.2 replacement/regression findings = 3.3; growth 30 minus 2.5 net minor-revert points minus 0.5 shrink points = 27%. No class-A credit until protected-category and hunk eligibility are verified.
- (a): P minus an assumed 0.1 indirect R3 benefit = 3.2; 27 minus an assumed 1.0 net cycle-1 saving = 26%. The cycle-1 avoidable share and replacement-review-2 burden remain unmeasured.
- (b): 3.5 minus zero demonstrated cycle-1 minor-anchor benefit = 3.5; 30 minus an assumed 3.0 growth points from not writing minor fixes = 27%. Prevented minor bytes and downstream dependencies are unmeasured.

Not checked: implementation, executed tests, full hunk recounts or live plugin access. Main risk: valid exact deletions can still break required behavior, while two replicates cannot separate small forecast differences from noise.
