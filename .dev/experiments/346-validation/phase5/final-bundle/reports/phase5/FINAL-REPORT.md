---
id: "ISSUE346-FINAL-COMPARISON"
title: "Review-loop convergence experiment"
description: "Measured effects, failed validity checks and limits of the issue 346 review-loop variants."
version: "1.0"
status: "reviewed-report; design and final assembly pending"
type: "reference"
created_date: "2026-11-09"
updated_date: "2026-11-09"
autogen: true
coordinator: "issue346 coordinator"
parent_doc: "../DECISIONS.md"
related_docs: ["first-run-fidelity-review.md", "repeat-plan.md"]
template_schema_doc: "~/.claude/templates/documents/supplemental_doc_template.md"
review_info:
  last_reviewed_by: "final-report-review, independent source-fidelity PASS"
  last_review_date: "2026-11-09"
---

# Review-loop convergence experiment

Back to [fixed experimental decisions](../DECISIONS.md).

> **WHAT:** Final comparison of the original incident, controlled PR 427 tests and five proposed variants.
> **WHY:** Distinguish lower review counts and smaller documents from evidence that defects actually converge.
> **HOW TO USE:** Read the conclusion and comparison first; treat refactor candidates as hypotheses, not proven fixes.

### Document Lifecycle Position
Standalone experimental reference. Design and implementation are separate deliverables.

### Tiered Usage
Standard supplemental report: five substantive sections, evidence appendix and explicit verification status.

## Document Information
| Field | Value |
|---|---|
| Document name | Review-loop convergence experiment |
| Type | Standard supplemental experimental report |
| Maintained by | Issue 346 coordinator |
| Last source refresh | 2026-11-09, original recorder comparisons, fixed decisions and independent first-run fidelity review |
| Measurement unit | One scenario; two control loops, two exact-427 loops, two flagged-427 loops, one completed loop for each of three proposed variants |
| Scientific conclusion | Convergence not proven; no validated winner |
| Calculation companion | `final-summary.json`, derived from nine original measurement files |
| Verification entry point | `final_report_check.py`; read-only by default, no model calls |
| Governing template | Installed supplemental document template, standard tier |

## Completeness Status
- [x] Conclusion, scope and fixed success conditions documented.
- [x] Measured comparisons, owner carry-forward and uncertain audit unions documented.
- [x] Mechanisms, invalid trials and incomplete builds distinguished.
- [x] Design candidates separated from established effects.
- [x] Coordinator deviation, polling stop and preservation limits documented.
- [x] Fresh independent review of this final report: PASS, no required changes. See [FINAL-REPORT-QA.md](FINAL-REPORT-QA.md).
- [ ] Fresh-session refactor design and independent final design review: pending.
- [ ] Final bundle manifest after all deliverables: pending.

| Contract element | Details |
|---|---|
| Dependencies | Fixed decisions, original measurement packages, first-run fidelity review |
| Inputs | Preserved specs, findings, dispositions, script results, session/model provenance |
| Downstream | Fresh refactor specification and owner decision; no implementation authorized here |
| Change impact | Any changed endpoint/count/source requires recomputing the companion and rechecking the affected claim |
| Review cadence | This experiment's closeout; no recurring polling |

The comparison report and numeric companion passed a fresh independent source-fidelity review. That approves their evidence fidelity, not experimental success or completion of the separate design and bundle deliverables. Pending deliverables are listed rather than represented by implementation stubs.

## Table of Contents
1. [Conclusion and scope](#1-conclusion-and-scope)
2. [Measured comparison](#2-measured-comparison)
3. [What the variants do and miss](#3-what-the-variants-do-and-miss)
4. [Refactor candidates and constraints](#4-refactor-candidates-and-constraints)
5. [Validity, execution and remaining work](#5-validity-execution-and-remaining-work)

## 1. Conclusion and scope
**PR 427 is not proven to make review loops converge. None of the completed, measured loops reached a clean PASS. None of the five proposed variants has a valid, repeated convergence result.** Smaller documents are the strongest observed improvement, not proof that the remaining defects disappeared.

The controlled comparison used two pre-427 runs and two runs with the exact 427 command. The last-review CRITICAL+MAJOR label count averaged 6 before 427 and 5.5 with it; the required maximum was 3. Document growth fell from about 63.5% to 29.7%, but the defect-count condition and variation condition failed. The literal installation-stability check also failed during the treatment window, although delivered reviews were traced to the intended command text. The separate two-run test with 427's re-review flags averaged 3.5 last-review labels, still above 3, and its improvement was smaller than the observed between-run variation. Sources: [controlled comparison](../phase4/AB-REPORT.md), [flagged comparison](../phase4/ARMB-REPORT.md), and [fixed decisions](../DECISIONS.md), controlled-test and flagged-test sections.

Of the proposed variants, diffgate has the largest measured reduction in document growth: 10.31% versus the fixed control mean of 63.51%. Its final restricted review still found two blockers, and a separate full-document audit found four MAJOR findings. Ponytail's final restricted review listed no new CRITICAL+MAJOR findings, but the reviewer changed models, the verdict parser failed, and the owner's broader counting rule retains one earlier MAJOR-labelled note conservatively. Ledger's restricted final review listed three new MAJOR findings, with three prior MAJOR labels unresolved; its separate sweep found nine MAJOR findings. These are observations from one completed loop each, not a ranking of established defect-removal effectiveness.

### Scope and method

The initial search produced five candidate incidents. Session logs were chosen over tasklists because they retained the actual review/revise instructions and byte-identical starting documents. The tasklist search was cheaper but lacked several original briefs. Only one incident used the changed review command: the Orca worker-contract specification. The other four used different review tools, so their analyses establish limited reach, not successful replays. The decision log narrowed live testing to this one scenario; this report does not describe five scenarios as tested.

The starting specification was 57,763 bytes. Replays used the original source checkout at commit `2cb683f5c1f0dfbd3c5f169a8b64a432931f718e` and an untracked input overlay, rather than a later checkout containing the finished answer. Each completed loop had three reviews and two fix cycles. A later full-document audit or ledger sweep was a separate measurement, not a fourth fix/re-review cycle.

The experiment's term **significant** means its predeclared practical screen: final counts at most half the control mean, growth at most 70% of control mean, improvement exceeding the larger within-arm spread, every treatment replicate better than every control replicate, and required validity checks satisfied. It is not a statistical significance test or a confidence interval. The strict success conditions were not met.

## 2. Measured comparison
### Counts and size at matched endpoints

**Label proxy** means the number of newly numbered findings labelled CRITICAL or MAJOR in that review. It is not a verified blocker count. Prior unresolved findings, deferred findings and later audits are separate measures. Original reports and machine snapshots remain in the per-variant evidence packages.

| Run | Completed loops | New CRITICAL+MAJOR labels, reviews 1 / 2 / 3 | Final bytes | Growth from 57,763 bytes | Final report / loop outcome |
|---|---:|---|---:|---:|---|
| Historical incident | 1 | 18 / 10 / 8 | 92,194 | 59.61% | No clean pass |
| Pre-427 control 1 | 1 | 11 / 9 / 8 | 91,102 | 57.72% | FAIL |
| Pre-427 control 2 | 1 | 12 / 7 / 4 | 97,814 | 69.34% by bytes | FAIL |
| Exact 427, no added flags, replicate 1 | 1 | 9 / 5 / 6 | 71,113 | 23.11% | FAIL |
| Exact 427, no added flags, replicate 2 | 1 | 9 / 7 / 5 | 78,715 | 36.27% | FAIL |
| 427 with re-review flags, replicate 1 | 1 | 16 / 5 / 6 | 73,807 | 27.78% | FAIL |
| 427 with re-review flags, replicate 2 | 1 | 17 / 6 / 1 | 76,328 | 32.14% | FAIL |
| Diffgate | 1 | 7 / 2 / 2 | 63,717, frozen snapshot | 10.31% | FAIL, cap escalation |
| Ponytail | 1 | 9 / 7 / 0 | 70,488, after audit | 22.03% | FAIL; automated verdict parser failed |
| Ledger | 1 | 13 / 9 / 3 | 70,565 | 22.16% | ESCALATE; sweep FAIL |
| Stoprule | 0 completed loops | Review 1 only; 6 machine-confirmed blockers from 8 sealed claims | No two-fix endpoint | Not measured | Invalid provenance check; stopped |
| Minfix | 0 | Not measured | No runnable command | Not measured | Build halted |

Sources: [controlled comparison](../phase4/AB-REPORT.md), [flagged comparison](../phase4/ARMB-REPORT.md), `final-bundle/measurements/{diffgate,ponytail,ledger}/comparison.md` and their original `metrics.json` files. The 427 flag run's first final review has six MAJOR labels but four blocking grades, demonstrating why the two measures must not be substituted for one another.

### What remains open beyond the new-label count

| Measure | Diffgate | Ponytail | Ledger |
|---|---|---|---|
| New final-review label proxy | 2 | 0 | 3 |
| Unresolved prior CRITICAL+MAJOR labels at final review | 0 | 0 within the stated final-review resolution table | 3 |
| Final script/report blockers | 2 | 0 by independent reading, not the failed parser | 3 in-scope script rows |
| Cumulative deferred/demoted/withdrawn CRITICAL+MAJOR labels | 0 | Conservatively 1, possible 0-1 interpretation of partially rejected N1 | 3 loop deferrals; 12 including 9 sweep rows |
| Loop-only new plus unresolved label rows | 2 | 0, plus conservative owner carry-forward 1 | 6; five distinct mechanisms under the recorder's merge rule |
| Additional full-document check | 4 MAJOR findings | None | 12 findings: 9 MAJOR, 3 MINOR |
| Audit-augmented CRITICAL+MAJOR union | Recorder point 6; plausible 5-6 with independent review's overlap concern | Unknown, not zero | Recorder point 13, bounds 11-14 |

The union is an interpretive deduplication, not an independently validated severity count. Diffgate's recorder treats all four audit findings as distinct from its two endpoint blockers. The independent measurement reviewer identified a plausible shared retry-relocation mechanism, so this report retains 5-6 rather than treating six as exact. Ledger's script headline is 15: three in-scope unverified rows plus nine sweep MAJOR rows plus three outside-scope MAJOR rows. It duplicates at least one sweep/loop finding and a parent/child residual. Neither 15 nor the union 13 should replace the original new-label proxy 3.

**Controls did not receive these post-loop full-document audits.** Comparing their new-label mean of 6 with diffgate's or ledger's augmented union would change the measurement instrument. Conversely, ignoring the audits would overstate how close the whole document was to clean. Ponytail's zero is an unaudited, restricted-review zero and its final report still says FAIL.

### Fixed thresholds, without moving the bar

- Fixed reference values used in the screen: control mean final proxy 6, count limit 3; control mean growth 63.51%, growth limit 44.457%.
- Byte-derived control growth is about 63.527%, making the corresponding limit about 44.469%. The rounded original reports used 69.30% for control 2 rather than its byte-derived 69.337%. This rounding does not change any result; the registered rounded limit is retained.
- Exact 427 without added flags: final-label mean 5.5 and improvement 0.5, versus control spread 4. Neither count nor spread condition holds.
- 427 with flags: mean 3.5, improvement 2.5, larger proxy spread 5. Neither condition holds. Growth passes the magnitude screen in both replicates.
- Diffgate: new-label improvement 4 equals, but does not exceed, control spread 4. Its own spread is unknown. Growth reduction is large descriptively, but final FAIL, restricted coverage and validity failures prevent a convergence claim.
- Ponytail: the numerical count reduction is larger than control spread, but its only final review changed models and its own spread is unknown. The same-model validity condition fails.
- Ledger: new-label improvement 3 is smaller than control spread 4. Counting loop-only unresolved labels gives 6, not 3. Its model change and restricted coverage are additional failures.

The three variant growth percentages were below both control growth percentages. That supports an observed size reduction under these workflows. It does not establish a repeatable treatment effect, a clean specification, or which single mechanism caused the reduction.

## 3. What the variants do and miss
### Diffgate: smaller controlled edit surface, not a clean whole document

The prototype computes a diff-based re-review surface and checks machine-readable finding anchors and reviser fix maps. Revisions must map to accepted blocking findings. In the measured run, the document grew by 4,291 bytes in the first fix and 1,663 in the second. All three frozen versions had 285 newline characters; added content was inside long existing lines, so line counts alone hide growth.

The last review examined a narrow computed surface, about 2% of the document, rather than a fresh whole-document panel. That and the blocking-only revision scope plausibly restrain expansion, but the experiment did not separate their effects. The frozen audit's four MAJOR findings include problems at both changed and original anchors. A changed anchor proves neither causation nor that the same defect was previously closed. The source package's causal-origin groupings are interpretive, not an ablation result. See `final-bundle/measurements/diffgate/comparison.md`, scope, size and audit sections.

### Ponytail: a real audit, but only 91 bytes removed

The requested audit ran once after fix cycle 2 and before review 3. It invoked the ponytail review skill and examined the severity and necessity of fixes. The script retained all seven blocking fixes, reverted one MINOR template expansion and shortened one repeated citation clause. The endpoint changed from 70,579 to 70,488 bytes: 91 bytes saved, only 0.1575 percentage points of cumulative growth. Growth was already about 22.19% before the audit. The lower total growth cannot therefore be credited mainly to those two audit edits.

The first revision acted on seven MINOR-labelled findings and the second on eight; after the audit reversal, fourteen such fixes remained, with one citation shortened. This contrasts with diffgate's narrower blocking-owned revision scope. It is a plausible design opportunity, not evidence that an arbitrary budget would safely remove those edits.

The final review resolved seven tracked blockers and reported no new numbered findings, but still ended FAIL for a carried MINOR under the preserved original brief. Its orphan reference to `R3-N1` is unresolved report inconsistency, not an extra confirmed blocker or a reason to silently claim PASS. The verdict script failed because the prose-first resolution table did not yield parsed prior-status rows; it also treated citation rows as blockers. The recorded automatic zero is invalid. `fix_audit.py`'s `cmd_verdict` explicitly adds an unparseable condition when no prior rows are parsed. The recorder independently counted report text instead of repairing the format or parser mid-run.

### Ledger: accounting works; restricted verification misses substantive residuals

The prototype keeps finding rows in a script-owned ledger, verifies existing rows during later reviews and checks new defects in changed hunks. One separate blinded sweep follows the capped loop. The script closed the loop with three open blocking rows and ESCALATE, not PASS. It stored outside-scope MAJOR labels and sweep rows as deferred; the owner's rule keeps them visible.

The later sweep found nine MAJOR findings. Several challenged text associated with rows the loop had marked verified. This shows why row closure and a bounded review surface cannot by themselves establish correctness of the document. It does not establish a universally superior sweep instrument: the sweep saw revision tags, had no corresponding control sweep, and the loop's final reviewer changed models. See `final-bundle/measurements/ledger/comparison.md`, separate-count and mismatch sections.

### Stoprule: implemented prototype, invalid live trial

The build completed and the first live review sealed eight claims; the grader classified six as blocking and two as minor. The report checker accepted the format. The mandatory transcript-integrity verifier then failed because the actual grader replies arrived as asynchronous completion notices while its extractor recognizes Agent/Task tool-result records. The source's `transcript_blocks` and `cmd_verify_transcript` implement that extraction boundary. The trial was invalidated and no reviser was launched. This is a transport/provenance failure, not evidence for or against reduced defects. No parser patch or weakened gate was used to recover an apparent success.

### Minfix: proposed mechanism, incomplete build

The budget-based fix limiter never reached a runnable experiment command. Its managed progress ledger completes only tasks 1 and 2; task 3 halted after the retry ladder and again after operator review. The remaining blocker concerned line-break restoration moving an in-budget appended sentence into a separate paragraph. The recorded 84 passing tests did not establish acceptance of the failed task. Tasks 4-8, including the command and experiment packaging, were not built. Predictions in the brainstorm specification are not measured results.

Historical build checks for the other four prototypes passed their scoped new tests, but these are not live convergence tests. Build completion, evidence-package quality, experimental validity, and a clean review outcome are four different claims. This report does not promote one into another.

## 4. Refactor candidates and constraints
**Do not ship a combined variant as a proven convergence fix.** The justified next deliverable is a small refactor specification that distinguishes observed size restraint from hypotheses requiring validation.

| Candidate | Evidence supporting consideration | What is not established | Design constraint |
|---|---|---|---|
| Limit revisions to confirmed blocking defects and explicitly authorized edits | Largest observed size restraint came from diffgate's constrained surface and fix ownership; base 427 also reduced growth | Which of diff enforcement, fewer minor edits or run variation caused the effect | Reuse 427's existing scope rule; do not add arbitrary word budgets as if validated |
| Track finding identity, disposition and changed anchors mechanically | Diffgate fix maps and ledger retained traceable rows and exposed count differences | Mechanical bookkeeping alone does not validate a finding or a fix | Stable identities, explicit unresolved/deferred counts, immutable snapshots; uncertain matches stay uncertain |
| Audit severity and necessity before the final review | Ponytail's audit actually ran and removed two small surplus edits while retaining blocking fixes | No causal effect on final defect count; only 91 bytes removed; final model changed | Optional bounded audit, explicit edit consent, preserve changes and rollback evidence; never silently demote blockers |
| Keep an honest final coverage statement | Diffgate audit and ledger sweep found defects outside the restricted last-review view | No matched control audit, so no comparable full-document improvement estimate | Scope-local pass must not imply whole-document safety; any separate audit is separately labelled and cannot create a new endless loop |
| Make parsing and provenance fail closed | Ponytail's parser and stoprule's transcript checks failed on real outputs | Fixes to those tools have not been built or validated in this work | Do not turn unparseable output into zero findings, or accept unlinked grader answers |

These are components of an **unvalidated design hypothesis**, not an instruction to merge all four scripts. Prefer the existing review-loop contract and the fewest additional mechanisms needed for provenance and honest counting. Do not finish minfix, repair stoprule, add an ablation arm, or run further experiments under this report's authority.

The refactor specification must retain:

1. At most three reviews and two fix cycles, with escalation rather than PASS when genuine blockers remain.
2. Separate minor notes from blockers without concealing MAJOR labels, disputed findings, deferrals, withdrawals or severity changes in experimental accounting.
3. A final review of prior blocking fixes plus the declared changed surface; disclose unreviewed coverage and dependencies.
4. Explicit ownership and authorization for any scripted edit or revert; preserve failed-attempt evidence and recovery snapshots.
5. Recorded command version, actual reviewer model, input hashes and scope so a future controlled test can distinguish the treatment from environment drift.
6. No assertion that line changes alone prove fix-induced causation.

A future validation plan, not executed here, should compare the same measurement instrument in every arm, preserve actual model continuity, validate real asynchronous transcript transport before the run, and include owner carry-forward counts. Full-document audits must either be matched across all arms or remain separate safety observations. Any new experimental run requires authorization; this report does not lower the original success bar.

## 5. Validity, execution and remaining work
### Experimental limitations

- **Single scenario.** The five incident analyses did not become five tested scenarios. Four incidents were outside the changed command's reach. The historical original also lacked later global review rules, so historical improvement alone cannot be attributed to PR 427.
- **Small samples and no valid variant repeats.** Controls and each original 427 arm had two loops; each measured proposed variant had one. The four later exploratory sessions completed only first reviews. They supply no final-loop endpoint, spread estimate or repeatability evidence.
- **Model continuity failed.** Ponytail's final-review session changed from requested `claude-opus-5-5` to recorded `gpt-6.1-sol`; ledger's final review and part of its second revision also used `gpt-6.1-sol`. Diffgate's replacement audit used changed model routing. Launch-request metadata is not actual per-response model evidence.
- **Review coverage changed.** Diffgate and ledger restricted new-finding checks to a computed/changed surface. Ponytail inherited changed-lines-only re-review. Lower visible counts may reflect limited search rather than fewer whole-document defects.
- **Environment and ownership drift.** Phase 5 had the finished WORKER-CONTRACT file available, unlike the isolated control arms. Answer exposure occurred in diffgate. Its live target was later externally replaced; the preserved history snapshot salvages size/count measurement, not untouched-trial validity. Variant installation watches did not continuously cover the first runs.
- **Counting and automation limits.** CRITICAL+MAJOR labels are a proxy, not a fresh severity validation. The ponytail parser's printed zero is unusable. Ledger's raw headline double-counts some mechanisms. Audit unions have uncertain overlaps and unmatched control instruments.
- **Interruption and cost limits.** Rate-limit failures and retries were extensive; elapsed time is not active reasoning time. Logged tokens across changed providers are not equivalent billed cost. The first-run recorders separate recoverable tools/tokens and interruption windows; this report does not invent a single cross-provider efficiency score.
- **Safety gap in audit application.** The build log records that ponytail's script can write the spec before writing later audit log files; a subsequent disk error may leave the edit applied. The prototype therefore must not be described as guaranteeing unchanged input on every failure. This is a logged product gap, not a repair delivered here.

### Coordinator deviation and correction

The owner requested two further runs for **significant deltas**. The coordinator instead selected diffgate and ponytail from weaker magnitude screens and called that authorized. That was incorrect: diffgate did not exceed control variation, and ponytail's only trial had failed model continuity. A fresh independent review verified the first-run measurements but returned FAIL on the authorization claim. Its original FAIL is preserved in [first-run-fidelity-review.md](first-run-fidelity-review.md); the [repeat plan](repeat-plan.md) was corrected, not rewritten as though the mistake never happened.

Four exploratory first-review reports were already delivered when the drivers were stopped. One diffgate revision had automatically launched; it was paused before any edits. All four source specs were checked against the original hash and remained unchanged. The preserved `final-bundle/confirmations/` folders contain those incomplete observations. They are not additional completed replicates. No authorization to resume them has been inferred from subsequent reporting instructions.

Repeated scheduled checks and rate-limit retries then failed to produce the final report. On the owner's instruction, polling, the router and completion waits were stopped. The blocked report worker produced no report; it was cancelled before direct authorship began. This report was written directly in the coordinating session on 2026-11-09. No schedule or experiment was restarted to write it.

### Deliverable and repository state

- **Written:** this final comparison, the calculation/source-hash companion `final-summary.json`, and the preserved first-run evidence packages. Their quality status is separate from experimental success.
- **Not established:** a winning convergence fix, a valid repeated proposed-variant effect, or a causal benefit from the ponytail audit.
- **Separate remaining deliverable:** a fresh-session `/sc:design` refactor specification grounded in this report, followed by independent final review of the report/design and a final bundle inventory. Until those exist, the overall requested program is not complete.
- **No commits or pushes in this reporting step.** Variant build worktrees contain staged task packages and uncommitted product changes; experiment evidence is separately preserved. Do not stage generated `.claude/` mirrors or project-root `artifacts/`. Required `.dev/tasks/` packages remain subject to the repository's always-stage rule.
- Additive experimental commands were installed earlier under separate names. This report does not uninstall them, restore a different machine state or authorize publication. The earlier machine-wide changes and restoration history are in `install-log.md`, the decision log and phase-4 install-watch evidence; current machine configuration is not inferred from old hashes.

Final assembly must retain all failed/invalid attempts, source reports, intermediate reviews and the corrected authorization record. It must regenerate the bundle checksum inventory after all deliverables are present. A valid checksum establishes byte preservation, not truth of the contents.

## Appendices
### Evidence and provenance
The report and `final-summary.json` are the canonical synthesis and numeric companion. The evidence bundle contains frozen copies, not independently rewritten conclusions. Worktree paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/`.

| Evidence | Location | Use |
|---|---|---|
| Fixed decisions and scope changes | `exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md` | Method selection, one-scenario scope, success bar, owner counting rule |
| Historical replay definitions and source overlay | `exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/` | Original instructions, starting document and counting definitions |
| Six controlled/flagged original measurements | `exp346-ab-<ctl-r1,ctl-r2,trt-r1,trt-r2,flg-r1,flg-r2>/.dev/experiments/346-validation/phase4/<name>/metrics.json` | Counts, matched bytes and comparator validity |
| Three proposed-variant measurements | `exp346-v-<diffgate,ponytail,ledger>/.dev/experiments/346-validation/phase5/<variant>/` | Metrics, validity, comparisons and copied source reports |
| First-run independent verification | [first-run-fidelity-review.md](first-run-fidelity-review.md) | Verified measurements, authorization finding and uncertainty notes |
| Build outcomes and scoped test evidence | [coordinator-log.md](coordinator-log.md) | Four completed prototypes and minfix halt; historical test results, not new test passes |
| Live trial, parser and transcript failures | [s1v-log.md](s1v-log.md) and `final-bundle/runtime/` | Stoprule invalidation, ponytail parser failure, interruptions and exact task receipts |
| Minfix task acceptance ledger | `bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/progress.md` | Two complete tasks, task 3 halt, no finished command |
| Installed experimental-file hashes | [install-log.md](install-log.md) | Earlier additive install and recorded command precedence |
| Paused exploratory first reviews | `final-bundle/confirmations/` | Incomplete observations only; no additional fixed endpoints |
| Original build snapshots and staged patches | `final-bundle/builds/` | Product source, task packages, worktree status and patch copies |

Original input SHA256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.

Frozen measured endpoints:

- Diffgate: `75a628e35b00eb23bde80d0190f6cf735f3b298c8f3b228caf05f65ee094ac9a`, 63,717 bytes. Use history version 3, not the externally rewritten live target.
- Ponytail after audit: `2d74ef94e35ad1f5762ec1e118aec05de6759321cf3bdfff852ab653ebff0509`, 70,488 bytes.
- Ledger: `030b7a941cd3498bf3c568232ae039ba2e267bd99c86417708f47add4d6a4e0c`, 70,565 bytes.

`final_report_check.py` recomputes nine source-file hashes, per-round label arrays, byte-growth arithmetic and fixed control counts; it also checks this report for unresolved placeholders and broken local Markdown links. This mechanical check is evidence consistency, not an independent substantive review or a new convergence test. It does not establish that every raw finding is correct.

The old bundle `SHA256SUMS` describes an earlier preservation snapshot and must not be used as a claim that later additions were inventoried. `SNAPSHOT-STATE.txt` discloses that limitation. A new complete inventory follows final assembly; all intermediate reports and failures remain retained.

## Document History
| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-11-09 | Coordinator | Initial direct synthesis from preserved measurements; independent final review pending. |

> **See also:** [first-run measurement review](first-run-fidelity-review.md), [corrected repeat plan](repeat-plan.md), [Arm B report](../phase4/ARMB-REPORT.md).
