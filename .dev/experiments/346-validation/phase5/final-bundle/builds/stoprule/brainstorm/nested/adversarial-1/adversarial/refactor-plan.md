# Refactoring Plan: Merge into Base (Variant B)

## Overview

- Base: Variant B (sonnet:analyzer), `variant-2-sonnet-analyzer.md`, in its Round 2 report-resident form (R2-B §3.4). Selected at a combined score of 0.900 against A 0.886 and C 0.818, with the debate-performance tiebreaker (`base-selection.md`).
- Incorporating strengths from: Variant A (opus:architect) and Variant C (haiku:devops).
- Planned changes: 27.
- Risk level: Medium overall. Changes 1, 9, 13, 15 and 17-21 restructure measured behaviour. The rest are additive or local.
- Convergence context: BLOCKED_BY_INVARIANTS at 92% (60 of 65 points). The 8 HIGH UNADDRESSED invariants (INV-008, INV-009, INV-012, INV-014, INV-015, INV-017, INV-029, INV-030) each have a planned change below. Six are resolved in the merged text. INV-009 is partly resolved, with a stated residual risk and an open question. INV-029 cannot be resolved at n = 2 without an extra arm, so it is a stated residual risk and an open question, with an optional ablation arm.
- Merge rules applied: concrete anchors are carried verbatim unless a row says otherwise (debate-protocol Step 4 items 6-7). Where base and non-base express the same rule, the more concrete version is kept. Governance additions from A and C wrap B's anchors; they do not replace them with summaries.
- Path keys used below: `B §x` = base section; `A §x`, `C §x` = non-base sections; `R2-A/B/C` = Round 2 rebuttals in `debate-transcript.md`; `INV-NNN` = `invariant-probe.md`.

## Merged Spec Skeleton (8 required sections)

The merged spec keeps exactly these 8 H2 sections, in this order. The merge executor must not add, drop or reorder H2 sections.

| # | Section (merged) | Required content | Built from |
|---|---|---|---|
| 1 | Problem and evidence | At most 5 lines | Change 27 |
| 2 | Mechanism | Steps in order (S0-S10 renumbered as needed) and the finding-ledger schema | B §2.0-2.7 with Changes 1-13, 15, 16 |
| 3 | Exact changes | File by file: command, skill (`SKILL.md`, `refs/rubric.md`, `refs/canaries.json`, `scripts/stoprule.py`), agent `finding-grader.md`, 2 test files, design doc | B §3 with Changes 3, 5, 11, 12, 22 |
| 4 | Variant command name and install note | `/sc:spec-panel-stoprule`, install contract, the one-line brief substitution (`perl` line plus `grep -c` check), coordinator placeholder fill | B §4 with Changes 15, 22 |
| 5 | Measurement plan | Predicted numbers for BOTH the pre-registered recorder proxy and the script's confirmed-blocking count, bar (c) spread logic, falsifiers | B §5 with Changes 14, 17-21 |
| 6 | Risks, costs, how it can make the loop worse | Cost table, risk list, removed/left causes | B §6 with Changes 23, 24 |
| 7 | Open questions | Updated list | B §7 with Change 25 |
| 8 | Reuse by other review commands | Reuse table | B §8 with Change 26 |

## HIGH Invariant Resolution Map

| INV | Severity | Planned change(s) | Disposition in the merged spec |
|---|---|---|---|
| INV-008 | HIGH | 8 | Resolved: a claim still failing the form rule after the one repair is `minor-form` (never `incomplete`), is listed in the escalation, and is in the PASS-time audit pool. Only an uncovered hunk gives `incomplete`. Residual stated: a pure omission with no quotable promise stays `minor-form`. |
| INV-009 | HIGH | 12 | Partly resolved: the raw grader reply is embedded verbatim with its hash, and a recorder step checks it against the Agent tool result in the worker transcript. Residual stated: inside one session the reviewer can still alter a reply; if the transcript is unavailable the run reports `grader-integrity: unverified`. Open question 2. |
| INV-012 | HIGH | 7, 15 | Resolved: the coordinator keeps the D11 step order and fills the T08 range from the script's brief; with zero confirmed ids it fills `NONE` and the brief says "make no spec edit". Carried priors get display ids inside the range. Pre-registered as a placeholder-value change. |
| INV-014 | HIGH | 18 | Resolved: bar (c) is computed (effect = 6.0 - arm mean must exceed max(4, own spread), equivalent to r1 + r2 <= 3). The merged spec states that the committed point prediction (3, 1) does NOT meet (c), and gives P(c) about 0.27. |
| INV-015 | HIGH | 4, 17 | Resolved: the pre-registered bar (a) reads the recorder proxy (CRITICAL+MAJOR by the reviewer's `claimed` label on new R3 findings). The script count is a separate, newly pre-registered metric. Nothing makes labels follow computed statuses. |
| INV-017 | HIGH | 16, 19 | Resolved: bar (a)'s "clean pass" branch reads `brief_pass` (script PASS and zero findings of any severity). `script_pass` is reported separately. The post-PASS path under the fixed DAG is defined. |
| INV-029 | HIGH | 21 | Not resolvable at n = 2 without an extra arm. Stated residual risk: the result can show "stoprule arm vs control", not "mechanism vs co-riding levers". Optional ablation arm with its falsifying condition. Open question 5. |
| INV-030 | HIGH | 20 | Resolved: new falsifier F1b (filter-only) fires if M1 <= 3 in both replicates while the M1c probe mean is above 3.0. The merged spec states it is expected to fire (about 0.7) under B's M1c prediction of 4.5. |

MEDIUM UNADDRESSED warnings handled on the way: INV-001 (Change 1, residual), INV-002 (2), INV-003 (2), INV-004 (13), INV-006 (15), INV-007 (8), INV-010 (16), INV-016 (17), INV-019 (14), INV-020 (24), INV-021 (9), INV-024 (15), INV-025 (21), INV-026 (24). LOW: INV-018 (23), INV-023 (24).

## Planned Changes

### Change 1: In-report storage, no scratch directory (from B Round 2, with A's and C's concessions)

- **Source**: R2-B §3.4 ("In-report mode"); R2-A §1 B-1; R2-C §1 item 2 and §3.3.
- **Target**: Base §2.0 bullet 4, §2.1 Parts table (Scratch dir row), §2.3 S0, S3, S4, S9, §6.2 risk 9, §7 Q4 (restructure).
- **Rationale**: X-001 went to B in both rounds at 95%. The saved T07 says "write ONLY your output file; ... no edits to the spec or any other file", and B itself concedes its `/tmp` scratch is outside that letter (R2-B §3.4).
- **Integration point**: Delete the Scratch dir row and every `/tmp/stoprule-XXXXXXXX/` reference. The ledger is a fenced block inside the stub report from the first write. `begin` writes, as the report's first lines, a marker `<!-- stoprule begin review=N/3 spec=<12hex> baseline=<12hex|none> nonce=<16hex> -->`. The script recomputes the diff from report, spec and baseline on each call (no `diff.json`). `grade-prep` prints the batch to stdout; the parent puts it inline in the Agent prompt; the reply goes back on stdin to `apply-grades`, which appends it to the ledger block (see Change 12). `finalize` rewrites the report in place. Replace risk 9 with: "The report is the only file written; no `/tmp` permission is assumed." Delete the `/tmp` half of Q4. Add C's recovery rule to §2.3 S0: a report whose ledger block has no valid seal at `finalize` is an incomplete run, never a PASS; the coordinator stops and does not silently re-dispatch under a fresh count. Residual (INV-001, C-032 unresolved): a re-dispatched reviewer that re-stubs the report overwrites the `begin` marker. The coordinator log, not the report, is then the only record that the slot was used; state this in §6.2.
- **Risk**: Medium. It changes where every subcommand reads and writes. A crash during an in-place rewrite can leave no valid seal (R2-C §3.3); fail-closed handling is stated, and no durability claim is made.
- **Concrete anchors preserved**: report is the only repository file written; sealed ledger in a fenced block; sentinel comment; `finalize` and `check`; the brief text "write ONLY your output file" quoted as the reason; precedent "ctl-r1 R3 ran ... a private `/tmp/ironclaude-batch.*` dir" kept as history in §6.2.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | `umask 077` on the scratch dir | dropped-with-rationale: there is no scratch dir |
| B | sentinel fields `review=N/3`, `rubric=<12hex>`, `ledger=<12hex>` | preserved-exact |
| R2-B | "about 2-3k tokens" extra per printed batch | preserved-exact (moved to the §6.1 cost note, Change 23) |
| C | 13 files per round under `.spec-panel-stoprule/<run-id>/` | dropped-with-rationale: X-001 at 95% |

### Change 2: Prior lifecycle: freeze, prior-report check, baseline binding, adjudicated exit (from A, C)

- **Source**: A §2.3 S1 (`verify-prior`, U-002), S3 prior-status guard (U-003), S4 freeze; A §2.4 `spec_sha256` (U-009); C §2.4 "explicit adjudicated exception" (R2-C §1 item 4).
- **Target**: Base §2.3 S0, S2, S3; §2.4 verdict function; §3.2 SKILL.md failure table (insert and modify).
- **Rationale**: X-003 to A, unanimous at 95% (B concession 5 named its own hole: a claim citing a prior could be graded `blocking:false`). U-002 adopted by all three R2 merge lists. INV-002 and INV-003 (MEDIUM) are closed here.
- **Integration point**: (a) S3: a prior that was `confirmed` in review N-1 and is still `open` or `regressed` is not put in any grader batch; its status is frozen. (b) S0: `begin` runs `check` on the prior report first; a mismatch between the prior's last line and its recomputed verdict exits 5 (A's "prior-verdict-mismatch", same meaning). (c) S0: `begin` checks sha256 of `--baseline` against the `spec=` hash recorded in the prior report's sentinel; a mismatch exits 5 with "baseline is not the text review N-1 reviewed" (INV-002). The sentinel gains `spec=<12hex>`. (d) B's existing guard stays: `resolved_by` must sit inside changed tokens, else the status is forced `open`. (e) Adjudicated exit (INV-003): a frozen id the reviser rejected with a cited reason in `disposition-round2.md` goes into the PASS-time and cap-time audit pool; an auditor `real:false` sets it `withdrawn-audit`, which no longer counts. No other path unfreezes it.
- **Risk**: Medium. It modifies `compute_verdict` and `grade-prep`; fixtures for each path are required (Change 22 tests).
- **Concrete anchors preserved**: A's freeze sentence "their status is frozen, so a grade cannot oscillate between rounds"; exit 5 for bullet 1 conditions; B's `resolved_by` rule; A's "never fall back to a first review (427 bullet 1 rule)".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | exit 5 (stop, bullet 1 conditions) | preserved-exact; also used for prior-verdict and baseline mismatches |
| A | exit 5 `prior-verdict-mismatch` | modified-with-rationale: merged into B's exit 5 with a distinct message, since B's exit set is the base |
| A | exit 7 `spec-mismatch` | modified-with-rationale: replaced by the `spec=` sentinel hash check under exit 5; the report, not a findings file, now binds the spec |
| B | 12-hex prefixes in the sentinel | preserved-exact |

### Change 3: FR-8/FR-9 source edit, bullet 2 replaced, FR-10 kept (from A)

- **Source**: A §3.1 item 4; R2-A §3.4; R2-B §1 A-3 and §3.3; R2-C §3.2.
- **Target**: Base §3.1 first bullet (replace the sentence "FR-8/FR-9 stay in the file; Review Loop bullet 2 is what overrides their 'MAJOR minimum'") and §3.1 bullet 2 text; §7 Q5 (modify).
- **Rationale**: X-005 to A, unanimous at 95%. `spec-panel.md:259` says "CRITICAL and FR-8/FR-9 findings are blocking"; `:328-329` hold "MAJOR severity minimum". FR-10 (`:330`) feeds the seven-column table that `sc:adversarial` AD-1 consumes (R2-C §3.2).
- **Integration point**: In the variant copy, FR-8 and FR-9 read: "generates a finding; it is blocking only under rubric B1-B3 of the Review Loop, otherwise minor" (A's wording with B's rubric ids). FR-10 unchanged. B's bullet 2 keeps its sentence "an FR-8/FR-9 row is a candidate that must pass the same test, not an automatic MAJOR". Q5 becomes: "the shared `spec-panel.md` is not edited; adopting this FR-8/FR-9 text there is a product decision after the measurement".
- **Risk**: Low. It edits only the copy. The confound it creates on the label proxy is handled in Change 21 (INV-025).
- **Concrete anchors preserved**: `spec-panel.md:259`, `:328-329`, `:330`; "MAJOR severity minimum"; FR-10 text verbatim; `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` checks in B §3.4.
- **Threshold preservation**: no numeric threshold in the touched text. Line anchors 259, 328-329 and 330: preserved-exact.

### Change 4: Reviewer label kept for reporting only; every form-valid claim is graded (from A)

- **Source**: A §2.4 `claimed` field; R2-A §1 B-2; R2-B §1 A-4; R2-C §1 item 13.
- **Target**: Base §2.2 schema (insert field), §2.3 S1 and S8 (modify), S9 `label_mismatch` (modify), §5.3 M1b row (replace).
- **Rationale**: X-006 to B (no label gates grading), with A's reporting-only label, unanimous at 95%. INV-015: the pre-registered metric is the recorder's label proxy, so the label must exist and must stay independent of the computed status.
- **Integration point**: Add `"claimed":"critical|major|minor"` to every `claim` line. State in §2.2: "No computation reads `claimed`; it exists only for the recorder proxy." S1: the reviewer writes one `claim` line per finding it would label critical, major or minor (not only candidate blockers), so a minor-labelled finding with a quote and outcome is still graded. S8: the prose may carry the reviewer's own severity words for each finding (needed by the recorder), but never a verdict. S9 `label_mismatch` is informational only and never edits a label. Delete M1b's "report labels follow computed statuses by construction" and its predicted 3.0 (replaced by the proxy prediction in Change 17).
- **Risk**: Medium. It raises grader volume (more claims per batch); Change 23 re-estimates the cost.
- **Concrete anchors preserved**: B's sentence "A reviewer-written severity word appears nowhere in the schema" is modified to "... appears in the schema only as `claimed`, which no computation reads"; A's "CRITICAL and MAJOR labels are kept for reporting only".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | M1b predicted 3.0 | dropped-with-rationale: it was 3.0 only "by construction"; the independent proxy prediction replaces it (Change 17) |
| A | proxy predicted mean 4 | preserved-exact (Change 17) |

### Change 5: Skill activation line and fail-closed missing skill (from A and C)

- **Source**: A §3.1 item 3 (`> Skill sc:spec-panel-stoprule-protocol`); C §3 (`E-SKILL-MISSING`).
- **Target**: Base §3.1 bullet 8 and the sentence "Fallback if the skill folder is missing ..." (replace).
- **Rationale**: X-013 to C, unanimous at 95%; S-008 to C at 95%. B's fallback produces a 427 run under the treatment name; with n = 2 one such run is half the arm (R1-A weakness 2).
- **Integration point**: Under the command title add the line `> Skill sc:spec-panel-stoprule-protocol` (the activation form `install_skills.py:30-32` recognises). Replace the fallback sentence with: "If the skill is missing at both `~/.claude/skills/sc-spec-panel-stoprule-protocol/` and `.claude/skills/sc-spec-panel-stoprule-protocol/`, stop with `E-SKILL-MISSING`; never run the 427 loop under this name."
- **Risk**: Low. Additive line plus one replaced sentence.
- **Concrete anchors preserved**: skill name `sc-spec-panel-stoprule-protocol`; `install_skills.py:30-32`; C's code `E-SKILL-MISSING`; the dual-surface lookup order (installed copy, then project `.claude/` copy) per the repo rule.
- **Threshold preservation**: no numeric threshold touched.

### Change 6: Cap and escalation choices: no in-loop cap lift, parent-run lineage (from C)

- **Source**: C §2.5 last paragraph; R2-B §1 A-1.
- **Target**: Base §2.5 item (g) (replace) and item (f) (modify).
- **Rationale**: X-012 to C, unanimous at 95%. B's (g) contradicts its own `begin` exit 4.
- **Integration point**: (g) becomes: "the two decisions only the user can take: accept the spec with (b) recorded as known issues, or start a new user-authorized run that records this run's sentinel `ledger=` hash as `parent=` in its first sentinel. The loop never lifts its own cap." (f) keeps its list and adds A's fixed sentence: "This command will not run review 4."
- **Risk**: Low.
- **Concrete anchors preserved**: canonical sentence `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` (bullet 4 and the Escalation footer); `begin` exit 4; escalation items (a)-(f) unchanged.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| seed / B / A / C | 2 fix cycles, 3 reviews | preserved-exact |
| B | exit 4 HALT at cap | preserved-exact |

### Change 7: Binary verdict with FAIL reason codes; unconfirmed never reaches the reviser (from C semantics, A and B rules)

- **Source**: C §6 failure table (infrastructure failure is not a defect); R2-B §1 C-1; R2-A §1 C-1; R2-C §1 item 5.
- **Target**: Base §2.4 verdict function, §2.3 S5 and S9, §3.2 SKILL.md failure table, sentinel (modify).
- **Rationale**: X-002 to B at 80% and C-028 to B at 80%, with A's rule identical in effect. A-007 qualified by all three (85%). INV-011 (ADDRESSED) depends on this rule being written down.
- **Integration point**: `compute_verdict` returns `FAIL` with a reason set: `confirmed` (any confirmed claim), `unresolved-prior` (a frozen open/regressed prior), `incomplete` (any `unconfirmed` claim or an uncovered hunk after the repair). The sentinel gains `reason=confirmed,unresolved-prior,incomplete` (the ones present) and `pre_audit=PASS|FAIL` (Change 13). Only `confirmed` and `unresolved-prior` ids enter the Reviser brief. An `incomplete`-only FAIL produces the brief "No confirmed blocking findings: make no spec edit" (Change 15). §5.2 adds: "A replicate with more than one `incomplete` review is invalid for M1; report results for clean runs and for all admitted runs."
- **Risk**: Medium. It changes how FAIL is consumed downstream.
- **Concrete anchors preserved**: B's "a missing grade, an uncovered hunk or an unresolved prior is also FAIL, so silence never passes"; B's `grader: unavailable` marker; B's `unconfirmed=f` sentinel field.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| A, B (R2) | "more than one" incomplete review invalidates the replicate | preserved-exact |
| B | "two failures" of a batch leave claims `unconfirmed` | preserved-exact |

### Change 8: Form rule settled, one repair, omission quoting, post-repair fate (from A, B, C)

- **Source**: A §2.3 S3 (quote >= 20 non-space chars, normalised); B §2.3 S2 (<= 300, span <= 120, outcome >= 8 words, one repair); C §2.3 ("For an omission, quote the requirement or guard whose promised behavior is incomplete").
- **Target**: Base §2.3 S2, §2.6 table row 2, §3.2 rubric B1 note, §6.2 risk 2 (modify and insert).
- **Rationale**: X-014 to B (one repair) at 95%. C-009 is unresolved (50%); INV-007 asks for one rule; INV-008 (HIGH) shows A R2 and B disagree on what a claim that still fails after the repair becomes.
- **Integration point**: (a) Quote rule: after normalisation, `quote` must be a substring of the spec, at least 20 non-space characters and at most 300 characters. Normalisation = collapse whitespace runs, strip backticks and `**`, map curly quotes to straight quotes (shortcut comment: "markdown tables and wrapped cells are not normalised; upgrade if `quote-not-found` dominates the audit"). (b) If the quote occurs more than once, the claim is repairable (exit 3): extend it until it is unique. (c) Rubric B1 gains C's omission sentence. (d) Fate after the one repair: a claim that still fails is `minor-form`. It is listed in the Computed result and the Escalation, and it is in the PASS-time audit pool (Change 13). It never makes the verdict `incomplete`. Only an uncovered hunk after the repair is `incomplete`. (e) §6.2 risk 2 keeps B's text and adds the residual: "a pure omission that has no quotable promise stays `minor-form`; the audit row `minor-form judged real` measures how often".
- **Risk**: Medium. Adding the 20-character floor can demote short real quotes; the audit row measures it.
- **Concrete anchors preserved**: B's `span` (defective words) field; exit 3 "repairable once"; "the second `seal` is final (`repair_used` recorded)"; A's shortcut note "the quote match is a whitespace-normalised substring search, not fuzzy".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| A | quote >= 20 non-space characters | preserved-exact |
| B | quote <= 300 characters | preserved-exact |
| B | span <= 120 characters | preserved-exact |
| B | outcome >= 8 words | preserved-exact |
| A | outcome >= 40 characters | dropped-with-rationale: B's 8-word floor is the base rule for the same check; keeping both adds a second gate with no debate support |
| B | evidence `text` within 3 lines of `line` | preserved-exact |
| B | 1 repair (exit 3 once) | preserved-exact |
| C | exact quote at a declared raw line span | dropped-with-rationale: C conceded the run tree that carried raw spans; normalised substring is the A/B rule |

### Change 9: Ratchet by changed-line overlap, prior-link hash rule, Q2 advisory (from A and C)

- **Source**: A §2.3 S3 (`difflib`, whitespace-only ignored, +/-1 line around pure deletions); C §2.4 step 2 (U-027); R2-B §1 A-5 (Q2 no longer demotes).
- **Target**: Base §2.3 S2 anchor sentence, S5 final-status rule, §2.6 row 3, §3.1 bullet 5, §3.2 rubric Q2 line, §7 Q1 (replace and modify).
- **Rationale**: C-010 to A at 60%: A's overlap is the more conservative demoter, and B's own replay shows span novelty demotes real late defects R3-4 and R3-9 (B §5.1, B open Q1). All three adopt the prior-link hash rule. INV-021 (MEDIUM) is closed here.
- **Integration point**: (a) S2: a claim in review 2 or 3 is `late-found` unless any anchor line of its quote is in the changed-line set (computed by `difflib` from baseline to spec, ignoring whitespace-only changes, plus the line before and after each pure deletion), or its `prior` is a valid link. (b) A `prior` link is valid only if the id was confirmed-open in review N-1 and has an identical outcome hash and either an identical quote hash or a changed-line anchor (C's rule). (c) One `prior` per claim; when two or more claims link to the same prior, they count once in M1 (as the prior), and the extra claims are reported as `duplicate-of:<id>`. (d) `span_novel` is still computed and printed as data. (e) Q2 is still asked in the batch and recorded, but it never demotes. Delete "`blocking:true` with `q2=same` and no `prior` gives `late-found`" from S5. (f) Bullet 5 of the command reads "... must quote a line changed by the last fix or cite a valid open prior id ...". (g) Q1 is closed: "Decided: changed-line overlap (A); span novelty is reported, not used to demote."
- **Risk**: High. It changes which R3 claims survive and so moves M1. The replay gate (B §5.1) must be re-run with this rule before any live run.
- **Concrete anchors preserved**: B's 5.1 table rows (R3-1 to R3-9) and its "3 of 8 in baseline" fact; B's `ratchet=off` on review 1 and when `--baseline` is missing; A's "+-1 around deletions" comment in `changed_lines`.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| A | +/-1 line around pure deletions | preserved-exact |
| B | replay result 4.3 of 8 (ctl-r1), 0.85 of 1 (flg-r2) | preserved-exact as the pre-merge replay; flagged for re-run under the overlap rule |
| R2-B | updated ctl-r1 survivors 4.6-5.0 of 8 (Q2 advisory) | preserved-exact |
| R2-A | hand replay about 4-5 on ctl-r1 | preserved-exact |
| B | R3-8 "p about 0.7" Q2 demotion, expected 0.2 | modified-with-rationale: Q2 no longer demotes, so R3-8's expected value is re-derived by the replay gate |
| seed | 89% (R2) and 100% (R3) of new findings `origin=changed` | preserved-exact |

### Change 10: Late-found claims graded in the same batch for the escalation (from C)

- **Source**: C §2.4 step 3.
- **Target**: Base §2.3 S3 (modify "Claims still eligible go into batches").
- **Rationale**: X-004 moved to C in all three Round 2 statements (95%); C-011 to C at 90%.
- **Integration point**: S3 puts every form-valid claim into the batches, including `late-found` ones. A late-found claim's grade is recorded as `late_grade` and shown in the Escalation item (d) and in "PASS with known debt". It never changes the verdict. If adding late-found claims pushes the claim count past one batch, the extra batch is added in the same Agent message (cost in Change 23).
- **Risk**: Low. Additive; verdict unaffected.
- **Concrete anchors preserved**: B's Escalation (d) label "real or not, not looped on"; "PASS with known debt".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | at most 6 claims per batch plus 2 canaries | preserved-exact |

### Change 11: Grader primitive: pinned model, `same-class` flag, grade mode only (from A)

- **Source**: A §3.5, §2.6 bullet 3; R2-B §1 A-6 and §4 X-016; R2-C §1 item 9.
- **Target**: Base §2.0 bullet 2, §2.1 Agent row, §2.3 S4, §3.3 (modify).
- **Rationale**: X-016 to A, unanimous at 95%; S-004 to A at 95%. B's cross-class rule is prose B admits it cannot check (B risk 5).
- **Integration point**: `finding-grader` keeps B's frontmatter (`tools: Read`, `model: sonnet`, `maxTurns: 10`, `permissionMode: plan`, `category: quality`). Delete "opus if the reviewer is a sonnet-class model; the command says 'a class different from your own'" and the `audit` mode. Add: "The sentinel records `grader_model=<frontmatter model>`; if the session model is the same class it records `same-class`." The batch arrives inline in the prompt (Change 1), so the body says "Read no file". Whether `tools:` may be empty stays an open question (A §7 Q1).
- **Risk**: Low.
- **Concrete anchors preserved**: agent name `finding-grader`; JSON reply shape `{"cid":"C3","blocking":true,"q2":"different","why":"..."}`; "facts marked `verified` are true, facts marked `unverified` are the reviewer's assertion".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B / A | `maxTurns: 10` | preserved-exact |
| B | `why` at most 25 words | preserved-exact |
| B | auditor `model: opus` in `audit` mode | dropped-with-rationale: the auditor is a separate fresh call (Change 13) |

### Change 12: Grader reply integrity check (new, from the invariant probe; uses B's saved-reply idea and C's raw-response persistence)

- **Source**: INV-009; B §2.1 (`grader-out-K.txt` saved byte for byte); C §2.6 (`grader-response.json` raw decisions); A §2.3 S5 ("The skill writes the reply verbatim").
- **Target**: Base §2.2 (new ledger line kind), §2.3 S5, §2.6 table row 4, §6.2 (new risk), §7 (new question).
- **Rationale**: In in-report mode the reviewer session carries the batch to the grader and the reply back. The script cannot tell a grader reply from reviewer-typed text, and canaries check the grader, not the transcription (INV-009, HIGH).
- **Integration point**: (a) `apply-grades` appends a `{"k":"grade-raw","batch":K,"sha256":"<hex>","text":"<reply verbatim>"}` line before parsing. `check` re-parses every `grade-raw` and fails (exit 6) if a parsed grade differs. (b) New recorder step, outside the loop: `stoprule.py verify-transcript --report R --transcript <worker session .jsonl>` confirms that each `grade-raw` text appears verbatim as an Agent tool result in that session's transcript, and prints `grader-integrity: verified|mismatch|unverified`. (c) §5.2 adds M8 `grader-integrity`, and a `mismatch` voids the replicate. (d) §6.2 residual: "inside one session the reviewer can still alter a reply before `apply-grades`; only the transcript check detects it, and only when the transcript is available."
- **Risk**: Medium. The transcript format and its availability to the recorder are UNVERIFIED (open question 2).
- **Concrete anchors preserved**: B's "The parent saves each reply byte for byte"; B 2.6 row "Blocking confirmed by an independent judge | Agent call (prose instruction) + script validation of the reply".
- **Threshold preservation**: no numeric threshold touched; exit 6 (tamper) preserved-exact.

### Change 13: Audit restructure: PASS-time all-demotion audit by a separate auditor, offline two-sided sample, nonce seed (from A, B, C)

- **Source**: B §2.3 S6-S7 (PASS candidate: all demotions plus 2 hunks); A §2.6 (fresh general-purpose auditor with the full spec; reinstatement recomputes FAIL); C §5 (two-sided stratified offline sample, inclusion probabilities, claimed-critical demotions); A §5 (owner spot-check of 5); R2-A §5 item 4 / A-008 (nonce seed); R2-B §1 A-7 (FAIL-path audit offline).
- **Target**: Base §2.0 bullet 3, §2.3 S6-S7, §3.2 seed sentence, §5.2 M4, §7 Q2 (restructure).
- **Rationale**: X-007 to A at 75% (B: "equal in effect to A"); C-013 to B at 85%; C-014 to A at 85%; A-006 and A-008 qualified with these conditions (75%, 85%). INV-004 (MEDIUM): reviewer `resolved` statuses were in no audit pool.
- **Integration point**: (a) In-run audit only at a PASS candidate: one fresh general-purpose Agent call with the session model, given the full spec at this review, the claim text and the rubric, and no grader reason. It re-judges ALL demotions in the review (`minor`, `late-found`, `minor-form`) plus 2 unclaimed hunks (seeded). Any `real:true` on a demotion sets `confirmed-audit`, and `finalize` recomputes FAIL. The sentinel records `pre_audit=PASS`. If the auditor is unavailable, the verdict is FAIL with reason `incomplete` (no reviser dispatch). (b) FAIL path: no in-run audit. (c) Offline, after both replicates: a two-sided stratified sample with recorded inclusion probabilities: 25% of nonblocking dispositions (min 2, at least 1 per nonempty stratum: grader-minor, minor-form, late-found), 25% of confirmed blockers (min 2), 25% of reviewer-`resolved` priors (min 2, new for INV-004), and all claimed-critical demotions as a separate nonrandom stratum. (d) Seed for every sample and shuffle is `sha256(nonce || review || ledger)`; `begin` writes the 16-hex nonce at review 1, before any finding exists. (e) The owner labels 5 sampled items independently, agreements included, and the report gives auditor-owner agreement as its own number. (f) Q2 of §7 is closed: "Decided: a FAIL-path disagreement is listed in the Escalation (c) and the offline report; it never changes a FAIL verdict."
- **Risk**: High. It changes when a PASS can stand and adds an agent call at every PASS candidate.
- **Concrete anchors preserved**: B's "a contested one blocks the PASS"; B's counts `sampled` and `contested` in the sentinel; C's "This estimates accuracy among reported findings, not recall of unreported defects"; A's "a false FAIL is cheaper than a false PASS" stance.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | PASS candidate: all demotions plus 2 hunks | preserved-exact |
| B | FAIL candidate: up to 3 demotions plus 1 hunk, in-run | modified-with-rationale: moved offline (R2-B §1 A-7); it cannot change a FAIL verdict |
| B | auditor sees 15 lines around the quote | modified-with-rationale: replaced by the full spec (R2-B §1 A-6 concedes 15 lines miss cross-references) |
| A | k = 3 demotions at PASS | dropped-with-rationale: replaced by all demotions; A risk 1 says k = 3 misses a 1-in-5 error rate about half the time |
| A | owner spot-check of 5, picked with k = 5 | preserved-exact |
| C | 25% of nonblocking dispositions, min 2 | preserved-exact |
| C | 25% of confirmed blockers, min 2 | preserved-exact |
| new (INV-004) | 25% of `resolved` priors, min 2 | new, mirrors C's rate |
| B | seed `sha256(sealed ledger)[:8]` | modified-with-rationale: the nonce makes the seed unsteerable by reviewer content (A-008) |

### Change 14: One audit falsifier with a stated share and a minimum sample (from A, B, C)

- **Source**: A §5 falsifier 3 (<= 20%); B §5.4 F2 (>= 25% over >= 8); C §5 (<= 10% over >= 20, zero missed CRITICAL); R2-C §3.4 (0 errors in 20 bounds the rate only near 14%).
- **Target**: Base §5.4 F2 (replace), §5.2 M4 (modify), §5.3 (add a row).
- **Rationale**: Success criterion 4 requires "a stated share". C-015 is unresolved (50%) and INV-019 (MEDIUM) notes three thresholds with no choice. Concrete-over-generic keeps all three numbers, each in one role.
- **Integration point**: (a) F2 (experiment falsifier and success-criterion share): offline audited demotion error rate > 20% over all demotions in both replicates, evaluated only if at least 8 demotions were audited; below 8 the criterion is reported NOT ESTABLISHED, not passed. (b) Rollout bar, stated as later work, not S1: <= 10% of audited true blockers demoted and zero missed CRITICAL, over at least 20 audited true blockers; add C's note that 0 of 20 gives a one-sided 95% upper bound of about 14%. (c) §5.3 row: demotion error rate predicted 10-15% (A).
- **Risk**: Low.
- **Concrete anchors preserved**: A's definition "Error rate = auditor `blocking` / demotions"; C's "zero missed CRITICAL".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| A | <= 20% demotion error rate | preserved-exact (success share and F2 threshold) |
| A | predicted 10-15% | preserved-exact |
| B | >= 8 sampled demotions | preserved-exact (minimum sample) |
| B | contested >= 25% rejects the grader | modified-with-rationale: replaced by 20% so the success share and the falsifier are one number; a 20-25% band where neither fires would leave criterion 4 undecided |
| C | <= 10%, >= 20 audited true blockers, zero missed CRITICAL | preserved-exact as the post-S1 rollout bar |
| R2-C | about 14% upper bound for 0 of 20 | preserved-exact |

### Change 15: Reviser routing: stable ids, display range, `NONE` rule, citation rows, disposition check (from A Round 2 and C)

- **Source**: R2-A §3.1 (placeholder fill); R2-B §1 A-9; R2-C §3.1 (stable ids, citation rows); C §2.5 (U-024, fix-to-id map).
- **Target**: Base §3.1 bullet 6, §2.3 S9 Reviser brief, §4 (new paragraph after the substitution), §5.2 M5 (modify).
- **Rationale**: X-011 to A, unanimous at 90%; C-018 to A at 85%. The T08 template fills "findings {{R2_FIRST_ID}}-{{R2_LAST_ID}}" itself (flg-r2 filled N1-N11 while the report's brief named N1-N6). INV-012 (HIGH), INV-006 and INV-024 (MEDIUM).
- **Integration point**: (a) Ledger ids never change. `finalize` assigns display ids D1..Dk contiguously to every item in the Reviser brief: new `confirmed` claims first, then frozen carried priors. The brief prints a `display -> ledger id` table. (b) §4 adds the coordinator rule: fill `{{R2_FIRST_ID}}-{{R2_LAST_ID}}` with `D1-Dk` from the report's Reviser brief, and `{{R2_CITATION_COUNT}}` with the number of confirmed claims of rubric kind (b). With zero such items, fill `NONE` and `0`; the report's brief then reads "No confirmed blocking findings: make no spec edit; write `disposition-round2.md` with one row `NONE`". The step order (D11) is unchanged: T08 is still dispatched. This is a change of placeholder values, which the validity check records as listed substitutions; the pre-registration lists it as part of the treatment. (c) T08 still demands "one row per finding and per overstated citation". The reviser writes rows for the listed range; citation notes from T09 step 2 that are not confirmed kind-(b) claims are not passed. Whether this reading of T08 is approved is open question 3. (d) `stoprule.py check-disposition --report R --disposition D` lists applied ids outside D1..Dk. It feeds M5 and F6 and never rejects a submission.
- **Risk**: High. It changes what the coordinator types into the reviser brief; a wrong fill routes the reviser to the wrong set.
- **Concrete anchors preserved**: T08 placeholders `{{R2_FIRST_ID}}`, `{{R2_LAST_ID}}`, `{{R2_CITATION_COUNT}}`; B's brief fields (id, quote, outcome, sites); B's "revise only the quoted text and the listed `sites`"; 427 bullet 6 "the reviser reads the report, not the command" (`spec-panel.md:263`).
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | F6: 2 or more applied ids per cycle outside the brief | preserved-exact |
| seed / B | Arm B applied 15 of 15, 9 minor | modified-with-rationale: restated as "15 rows: 11 findings plus 4 citation rows, 9 of them minor" per B's concession 9 |
| C | unknown or nonblocking ids reject the submission (HALT) | dropped-with-rationale: T08 requires citation rows outside the blocking set (R2-C §3.1); rejection would HALT compliant revisers |

### Change 16: Verdict precedence and the brief-verdict line (from A Round 2 and C)

- **Source**: R2-A §3.6; R2-B §3.2; R2-C §3.5.
- **Target**: Base §3.1 bullet 3, §2.3 S9 refusal rule, sentinel, §7 (new question).
- **Rationale**: The saved T07 and T09 say "any finding of any severity is FAIL"; flg-r2 R3 wrote both verdicts (`spec-panel-round3.md:15,170`). INV-010 (MEDIUM) and part of INV-017 (HIGH).
- **Integration point**: (a) Bullet 3 adds: "The coordinator and every metric read only the last line `verdict: PASS|FAIL` written by `finalize`." (b) The reviewer may record the brief's rule in prose on a line starting `brief-verdict: PASS|FAIL`. `finalize` refuses only lines starting `verdict:`. (c) `finalize` computes `brief_verdict` itself (FAIL if any finding of any severity exists) and writes `brief=PASS|FAIL` into the sentinel as a covariate. (d) Open question 4: the worker still holds two instructions on a minors-only report; owner approval of precedence is required before admission (R2-C §3.5).
- **Risk**: Low.
- **Concrete anchors preserved**: B's "a hand-typed verdict line fails `check`"; the last-line format `verdict: PASS` / `verdict: FAIL`.
- **Threshold preservation**: no numeric threshold touched.

### Change 17: Two counts, both pre-registered, with predictions for both (from A, B; INV-015, INV-016)

- **Source**: A §5 metrics table and prediction table (proxy mean 4); B §5.2 M1, §5.3; R2-B §3.1; `FLG2/metrics.json` counting rule (via INV-015).
- **Target**: Base §5.2 metric list and §5.3 prediction table (restructure).
- **Rationale**: INV-015 (HIGH): D10/D11 bar (a) is the recorder proxy, "CRITICAL + MAJOR by severity label ..., independent of the blocking grade", over new numbered R3 findings. Swapping it for M1 would change the metric after the bar was set. INV-016 (MEDIUM): the two sets differ.
- **Integration point**: §5.2 defines: **M0 (pre-registered bar (a))** = the recorder proxy, the count of new numbered R3 findings whose `claimed` label is CRITICAL or MAJOR, carried priors excluded, computed by the D10/D11 recorder method unchanged. **M1 (new, pre-registered before the first run)** = sentinel `confirmed` plus frozen `unresolved-prior` at R3; late-found, minor, minor-form and demoted items excluded. The text states that M0 and M1 can move in opposite directions on one report. §5.3 predictions (judgement, labelled):

| Metric | Control mean | Arm B | Predicted, merged variant | Bar | Chance |
|---|---|---|---|---|---|
| M0 R3 proxy (pre-registered) | 6.0 | 6 / 1, mean 3.5 | r1 5 (range 4-7), r2 3 (1-4), mean 4.0 | <= 3 in both, or a clean PASS earlier | about 0.2 |
| M1 R3 confirmed (script) | n/a | blocking 4 / 1 | r1 3, r2 1, mean 2.0 (each 1-5) | <= 3 in both | about 0.5 |

  Derivation for M0: the merged variant leaves labels to the reviewer, so the proxy starts at Arm B's 6 and 1. The FR-8/FR-9 edit (Change 3) and the rubric's "never a reason" list remove some upward labels, about 1 per control-like run. A's committed mean of 4 ("labels still drift") is kept. Derivation for M1: B's arithmetic (4 x 0.7 = 2.8, 1 x 0.85 = 0.9) is kept.
- **Risk**: High. It decides which number the success claim rests on.
- **Concrete anchors preserved**: all seed figures (control 8/4, mean 6.0; 427 6/5; 427+flags 6/1, mean 3.5); flg-r1 proxy 6 against blocking 4; B's M1 definition text.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| seed | bar <= 3 in both replicates, control mean 6.0 | preserved-exact |
| A | proxy predicted mean 4 | preserved-exact |
| B | M1 r1 3, r2 1, mean 2.0, each 1-5, chance about 0.5 | preserved-exact |
| B | survival 0.55 (ctl-r1 style) to 0.85 (flg-r2 style); 4 x 0.7 = 2.8; 1 - 0.7^4 = 0.76 | preserved-exact |
| A | r1 = 3, r2 = 1, confidence about 60% | dropped-with-rationale: withdrawn by A (R2-A §5 (d)); B's identical point values carry the prediction |
| C | R3 confirmed 2 and 3, mean 2.5 | dropped-with-rationale: withdrawn by C (R2-C §1 item 11) |
| new | M0 r1 5 (4-7), r2 3 (1-4), chance about 0.2 | new, judgement, labelled |
| B | M1b 3.0 | dropped-with-rationale: Change 4 |

### Change 18: Bar (c) spread logic and its predicted outcome (INV-014)

- **Source**: D10/D11 bar (c) (via INV-014); `ARMB-REPORT.md` (Arm B "NOT MET"); B §5.3 survival model.
- **Target**: Base §5.3 (new paragraph after the table), §5.4 (new falsifier F0).
- **Rationale**: INV-014 (HIGH): bar (c) requires the effect to exceed the larger within-arm spread. The control spread is 4 (ctl-r1 8, ctl-r2 4). C alone mentions this rule (C §5 "Require the effect to exceed the larger within-arm spread"); A and B omit it.
- **Integration point**: §5.3 adds: "Bar (c): effect = 6.0 - arm mean must exceed max(4, |r1 - r2|). With whole-number counts this holds exactly when r1 + r2 <= 3. It is evaluated on M0 (the pre-registered metric) and reported on M1. The committed M1 point prediction (3, 1) gives an effect of 4.0, which does not exceed 4: bar (c) is NOT MET at the point estimate, the same failure Arm B had (effect 2.5 against spreads of 4 and 5). Under B's survival model, P(r1 + r2 <= 3) = 0.41 (r1 ~ Bin(4, 0.7), r2 ~ Bern(0.85)); with B's discount for 6-proxy reviews (0.5 / 0.76) it is about 0.27. On M0, the predicted (5, 3) does not meet (c); chance about 0.1." §5.4 adds F0: "bar (c) NOT MET on M0 means the pre-registered bar fails, whatever M1 shows."
- **Risk**: Medium. It makes the stated success odds visibly lower.
- **Concrete anchors preserved**: control replicates 8 and 4; Arm B spread 5; "effect 2.5 against spreads of 4 (control) and 5 (Arm B): NOT MET".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| D10/D11 (via INV-014) | control spread 4; Arm B spread 5 | preserved-exact |
| new | arm mean < 2.0, i.e. r1 + r2 <= 3 | new, derived |
| new | P(c) on M1 about 0.27 (0.41 before discount); on M0 about 0.1 | new, orchestrator arithmetic on B's model, labelled judgement |
| B | discount ratio 0.5 / 0.76 | preserved-exact |

### Change 19: What PASS means, and the path after an early PASS (INV-017)

- **Source**: D10/D11 bar (a) "a clean pass in fewer rounds" (via INV-017); C §5 ("PASS before R3 counts as early stopping ... report growth at stop"); B §5.3 M7.
- **Target**: Base §5.2 M7 (modify), §2.3 S0 (insert), §5.3 M7 row.
- **Rationale**: INV-017 (HIGH): control and 427 runs could not pass while any minor existed, so a script PASS at R1 or R2 would meet bar (a) by a definition no comparator ran under. The fixed DAG still dispatches R2-revise and R3 after an R2 PASS.
- **Integration point**: (a) M7 splits into `script_pass` (last line PASS) and `brief_pass` (script PASS and zero findings of any severity in that review, the comparator's definition). Bar (a)'s clean-PASS branch reads `brief_pass` only. (b) S0: `begin` accepts a prior PASS and sets N = prior N + 1. The review runs as a post-PASS confirmation review; its R3 counts are recorded as usual. The fix cycle between them is the `NONE` brief from Change 15, so the spec does not change. (c) Growth is reported at the PASS review and at R3. (d) Predictions: `script_pass` about 0.2 per replicate (B); `brief_pass` about 0.05 per replicate (no run of any arm produced zero findings; judgement).
- **Risk**: Medium.
- **Concrete anchors preserved**: "Clean pass reached: no" in all A/B runs (via INV-017); B's M7 "PASS reached and at which review".
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | PASS about 0.2 per replicate | preserved-exact (as `script_pass`) |
| new | `brief_pass` about 0.05 per replicate | new, judgement, labelled |

### Change 20: Falsifier set, the M1c quality bar, and growth (from A, B; INV-030)

- **Source**: B §5.4 F1-F7, §5.2 M1c, §5.3 M1c row and growth row; A §5 falsifiers 4-6 and growth prediction; R2-B §3.1 (growth 25-30% without the placeholder fix); C §5 growth prediction.
- **Target**: Base §5.3 M1c and M2 rows, §5.4 (restructure).
- **Rationale**: INV-030 (HIGH): late-found rules and demotions can bring M1 to 3 or below while the spec is unchanged; B's own M1c prediction is 4.5, "not distinguishable from 427", and F1 fires only when M1 >= 4 AND M1c >= 5.5. C-024 to B at 75%. INV-028 (ADDRESSED) shows all four 427-base replicates already met the growth bar (23.1, 36.3, 27.8, 32.1%).
- **Integration point**: §5.4 becomes:
  - F0 bar (c) not met on M0 (Change 18).
  - F1a (B's F1, unchanged): M1 >= 4 in either replicate and M1c mean >= 5.5: no convergence gain over 427.
  - F1b (new, filter-only): M1 <= 3 in both replicates while the M1c mean is above 3.0. The claim "the spec got better" is void; report "converged by filtering". Predicted to fire: about 0.7 (B's M1c 4.5, range 2-7; judgement).
  - F2 (Change 14).
  - F3 (B, unchanged): a review ends PASS and the probe finds 3 or more claims meeting B1-B3.
  - F4 (B, extended with A falsifier 6): fewer than all reviews carry a sentinel with `check` exit 0, or re-running `check` on any saved report gives a different last line.
  - F5 (B, unchanged): growth above 30% in either replicate. Note that the 427 base already meets 44.4% (INV-028), so growth is not evidence for the mechanism.
  - F6 (B, unchanged), F7 (B, unchanged).
  - F8 (A falsifier 5, evasion): at R1, M1 below 3, or more than half of claims labelled CRITICAL/MAJOR end `minor-form`.
  - F9 (A falsifier 4, problem moved): M1 <= 3 while M0 >= 6 and the offline audit rates at least half of R3 demoted plus late-found claims as real.
  - M1c keeps "no worse than 6.0" as a no-harm floor; the quality bar for the "better spec" claim is M1c mean <= 3.0.
  - M2 growth prediction: 20% (r1 22%, r2 18%; range 12-30%) with the placeholder fill working; 25-30% if the reviser ignores the range (R2-B §3.1). Chance <= 44.4%: about 0.9.
- **Risk**: Medium. More falsifiers make a clean positive result rarer, which is the intended direction.
- **Concrete anchors preserved**: B's M1c definition ("one unmodified 427 `/sc:spec-panel` review ... of the spec after fix cycle 2, counted with the old method"); +1 probe session per replicate.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | F1: M1 >= 4 and M1c >= 5.5 | preserved-exact (F1a) |
| B | M1c predicted 4.5 (2-7), bar "no worse than 6.0", chance about 0.8 | preserved-exact; 6.0 kept as no-harm floor |
| new | M1c quality bar <= 3.0; F1b chance about 0.7 | new, labelled judgement |
| B | F3: 3 or more claims | preserved-exact |
| B | F5: growth > 30% | preserved-exact |
| B | F6: 2 or more ids per cycle | preserved-exact |
| B | F7: > 25 min per review | preserved-exact |
| A | falsifier 5: R1 confirmed < 3, or more than half of CRITICAL/MAJOR claims fail form | preserved-exact (F8) |
| A | falsifier 4: R3 confirmed <= 3, proxy >= 6, auditor rates at least half real | preserved-exact (F9) |
| A | R1 confirmed predicted 5-8 (of 9-17 proxy) | preserved-exact (§5.3 row for F8) |
| B | growth 20% (r1 22%, r2 18%; 12-30%), chance about 0.9 | preserved-exact |
| R2-B | growth 25-30% without the placeholder fix | preserved-exact |
| A | growth mean 22% (16-28%) | dropped-with-rationale: inside B's range; B's derivation (weighted applied volume) is the base |
| C | growth 22% and 28%, mean 25% | dropped-with-rationale: withdrawn by C (R2-C §1 item 11) |
| seed | growth bar <= 44.4%; control 63.5%; 427 29.7%; 427+flags 30.0% | preserved-exact |
| INV-028 | 23.1, 36.3, 27.8, 32.1% | preserved-exact |

### Change 21: Attribution: what the result can and cannot show; optional ablation arm (INV-029, INV-025)

- **Source**: INV-029 and INV-025; R2-A §3.1 (placeholder fill "must be stated as part of the treatment"); C §5 ("Use supplied control metrics as historical comparators").
- **Target**: Base §5.2 (new paragraph "What this design can attribute"), §6.2 (new risk), §7 (new question).
- **Rationale**: The merged variant runs on the Arm B base with Arm B briefs. Arm B alone already produced proxy 6 and 1 (mean 3.5, spread 5). Three levers ride with the script: the placeholder fill (Change 15), the FR-8/FR-9 text edit (Change 3) and the flags. With n = 2 the experiment cannot separate them.
- **Integration point**: (a) §5.2 states: "The pre-registered comparison is against control (6.0). A result of 3 or less shows the treatment bundle beat control. It does not show the script and grader caused it. Against Arm B (mean 3.5, spread 5), bar (c) cannot be met by any result, since the effect would have to exceed 5 from a mean of 3.5." (b) Optional ablation arm, owner-authorized: `spec-panel-stoprule-noscript` = the merged command text with the FR-8/FR-9 edit and the placeholder fill, and no script, grader or audit. 2 replicates, same briefs. Falsifying condition: if either ablation replicate has M0 <= 3, the mechanism is not shown to be what achieved the result. (c) §6.2 adds the residual risk; §7 adds open question 5 on authorizing the ablation arm.
- **Risk**: Low. Text only; the ablation arm is optional and costs about 10 extra sessions (2 loops x 5 sessions).
- **Concrete anchors preserved**: Arm B proxy 6 and 1, mean 3.5, spread 5; control mean 6.0.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| INV-029 | Arm B mean 3.5, spread 5 | preserved-exact |
| new | ablation: 2 replicates, about 10 sessions | new, labelled estimate |

### Change 22: Install contract and tests (from A and C)

- **Source**: A §4 (plain install, `install_skills.py:100-104`), A §3.6 (computed-diff drift test, `_has_corresponding_command` test); C §4 steps 2, 4, 5, 7 (absence check, skill first and command last, fresh-worker load receipt, per-round hash recheck); R2-B §1 C-3 and §3.5.
- **Target**: Base §4 install paragraphs (modify), §3.4 tests (append).
- **Rationale**: X-008 to A at 95%; C-019 to A at 85%; S-011 and C-022 to A (90%, 70%). INV-005 (ADDRESSED) relies on the per-round recheck.
- **Integration point**: (a) Replace "the same behaviour for skills and agents is UNVERIFIED, so the experiment uses the manual route" with: "`install_skills.py:100-104` skips an existing skill without `--force`, and the `-protocol` name installs standalone (`install_skills.py:13-21`), so a plain `uv run superclaude install` without `--force` installs all three items. The manual route stays only for the experiment's no-clobber record." (b) Manual route: `test ! -e` on each of the 3 destinations first; copy the agent and the skill before the command; then `sha256sum -c /tmp/spec-panel.before`. (c) A fresh worker's first report records the loaded command and skill hashes (C step 5). (d) `begin` checks the installed command, skill and rubric hashes against the sentinel of review 1; drift exits 5. (e) Tests added to §3.4: A's computed diff of the variant against `spec-panel.md` outside the replaced blocks; `install_skills._has_corresponding_command("sc-spec-panel-stoprule-protocol") is False`; fixtures for Changes 2, 7, 8, 9, 12, 13 and 15 (freeze, reason codes, post-repair `minor-form`, overlap ratchet and prior-link hash, `grade-raw` mismatch, PASS-time reinstatement, display-id mapping and the `NONE` brief).
- **Risk**: Low.
- **Concrete anchors preserved**: `install_commands.py:56-80`; B's `sha256sum ~/.claude/commands/sc/spec-panel.md > /tmp/spec-panel.before` line; B's "Never pass `--force`"; B's run-do-not-edit list of 4 test files; the measurement copy from the 472-line Arm B file, sha256[:12] `c8d80346a96c`.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | 472 lines, sha256[:12] `c8d80346a96c` | preserved-exact |
| A | 486-line master copy as the measured base | dropped-with-rationale: X-009 to B at 95%; the repo copy may still follow master (B Q8) |
| B | master adds 14 lines (`## Unattended mode`) | preserved-exact |
| B | 3 installed items | preserved-exact |
| C | 2 installed surfaces (no agent) | dropped-with-rationale: the agent is a declared primitive (S-004) |

### Change 23: Cost table re-estimated for the merged design (C-025, INV-018)

- **Source**: B §6.1; R2-B §1 A-7 (3-7 agent calls per loop); A §6.2 (2-3); C §6 (6 above baseline); INV-018 (R1 had 22 and 22 findings in Arm B).
- **Target**: Base §6.1 table (replace values) and break-even sentence.
- **Rationale**: C-025 is unresolved (50%). Grading every form-valid claim (Change 4) plus late-found claims (Change 10) at a batch limit of 6 means 3-4 batches at R1 alone, which no variant's estimate covers.
- **Integration point**: New §6.1 rows (estimates, UNVERIFIED until M6 measures them): grader calls per review = ceil(form-valid claims / 6): 3-4 at R1 (16-22 findings), 1-2 at R2 and R3; auditor calls 0-1 per loop (PASS candidate only); per loop 5-9 grader calls plus 0-1 audit. Bash calls per review: `begin`, `seal` 1-2, `grade-prep`, `apply-grades` 1-2, `status`, `finalize`, `check` = 7-9; per loop 21-27. Wall time: B's 6-10 min per review and 18-30 min per loop kept. Tokens: B's 90-120k per loop plus about 2-3k per printed batch (Change 1). Sessions: 0 extra in the loop; +1 probe session per replicate; +10 if the ablation arm runs (Change 21). Recorder: one `verify-transcript` call per review (Change 12).
- **Risk**: Low.
- **Concrete anchors preserved**: B's cost categories and the break-even sentence.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | 9-11 Bash calls per review, 27-33 per loop | modified-with-rationale: 7-9 and 21-27, since the in-run audit runs only at a PASS candidate |
| B | 2-4 agent calls per review, 6-12 per loop (median 8) | modified-with-rationale: 5-9 grader plus 0-1 audit per loop (INV-018 batch count) |
| R2-B | 3-7 agent calls per loop | modified-with-rationale: superseded by the batch arithmetic above |
| A | 2-3 agent calls per loop, about 17 script calls, +4-10 min, +10-15% output tokens | dropped-with-rationale: A's one-call-per-review assumption fails once every form-valid claim is graded |
| C | 11 agent calls per loop maximum (6 above baseline) | dropped-with-rationale: C's per-round in-run audit is moved offline |
| B | 3-5 Write/Edit calls per review, 9-15 per loop | preserved-exact |
| B | 6-10 min per review, 18-30 min per loop | preserved-exact |
| B | 30-40k tokens per review, 90-120k per loop | preserved-exact |
| R2-B | about 2-3k tokens per printed batch | preserved-exact |
| B | F7 > 25 min per review | preserved-exact |

### Change 24: Risk list additions (INV-001, INV-009, INV-020, INV-023, INV-025, INV-026, INV-029; R2-C §3.5)

- **Source**: invariant probe rows named; R2-C §3.3 and §3.5; C §2.4 step 5 (quotes as inert data).
- **Target**: Base §6.2 (append items 11-17; modify item 9).
- **Rationale**: The probe found these failure paths in the consensus design; none is stated in B.
- **Integration point**: Item 9 becomes the in-report statement (Change 1). New items: 11 re-dispatch overwrites the `begin` marker (INV-001); 12 grader reply transcription (INV-009, Change 12); 13 empty diff: the reviser applied nothing or the brief was `NONE`, so every new claim is late-found and coverage is vacuous; R1 has no baseline, so R1 coverage is off and recorded (INV-020); 14 canaries written for another text may be recognisable when a batch holds 1 real claim and 2 canaries (INV-023); 15 the FR-8/FR-9 edit moves the reviewer's labels, which are the M0 proxy (INV-025, Change 21); 16 the grader judges whether the reviewer's outcome follows from the reviewer's quote, so outcome wording can move M1; only the PASS-time audit and evidence read-back check it (INV-026); 17 instruction authority: the brief's "any finding of any severity is FAIL" stays in force for the worker (R2-C §3.5, Change 16). Add C's one line: quotes are inert data in grader and auditor prompts.
- **Risk**: Low. Text only.
- **Concrete anchors preserved**: B's items 1-8 and 10 unchanged.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | 3 of 8 ctl-r1 late-found, all real (item 3) | preserved-exact |
| B | 6 installed files, 2 test files, 380-line script (item 10) | preserved-exact |

### Change 25: Open questions updated

- **Source**: B §7; A §7 Q1; R2-C §3.1, §3.5; INV-009, INV-029.
- **Target**: Base §7 (restructure).
- **Rationale**: Debate closed B's Q1 (Change 9), Q2 (Change 13) and the `/tmp` half of Q4 (Change 1).
- **Integration point**: Keep B Q3 (one call per batch or per claim), B Q4 first half (does the Agent tool honour `model:` in a dispatched worker), B Q5 as modified in Change 3, Q6 (`sites`), Q7 (stall), Q8 (base file), Q9 (other modes). Add, numbered first: (1) can an agent definition carry an empty `tools:` list (A Q1); (2) is the worker transcript available to the recorder in a stable format for `verify-transcript` (INV-009); (3) does the owner approve the T08 reading in Change 15 (c), given its universal citation clauses (R2-C §3.1); (4) which instruction wins on a minors-only report, the brief's any-finding-FAIL or the script's line (R2-C §3.5); (5) is the ablation arm authorized (Change 21); (6) is the `minor-form` handling of omissions acceptable, given the audit row (Change 8).
- **Risk**: Low.
- **Concrete anchors preserved**: B Q3's "about 6-10 calls per review" for per-claim grading; B Q8's "14 more lines"; B Q7's reference `spec-panel-review-loop.md:154`.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| B | per-claim grading about 6-10 calls per review (Q3) | preserved-exact |

### Change 26: Reuse section: implement row (from A)

- **Source**: A §8 implement row.
- **Target**: Base §8 table, `/sc:implement` final review row (replace "The ratchet idea and `escalation` format only").
- **Rationale**: X-017 to A, unanimous at 95%; C-027 to A at 95%.
- **Integration point**: The row reads: "**Do not reuse the stop rule.** `qa.md` derives severity from checklist answers with a parent Read-back (`qa.md:37-97`) and keeps `late` blockers blocking (`qa.md:167`)." Keep B's "borrowed back" row and the `/sc:reflect` and rf-qa rows unchanged.
- **Risk**: Low.
- **Concrete anchors preserved**: `qa.md:37-97`, `qa.md:167`, `qa.md:79`; B's `--rubric` and `--cap` reuse sentence.
- **Threshold preservation**: no numeric threshold touched.

### Change 27: Section 1 cut to at most 5 lines

- **Source**: Base §1 points 1-5; requirement (c) of this plan.
- **Target**: Base §1 (replace).
- **Rationale**: The merged spec must keep section 1 at 5 lines or fewer. B's §1 is 5 numbered items but runs to about 15 wrapped lines.
- **Integration point**: Five single-line bullets: (1) S1 R3 proxy control 8/4 (mean 6.0), 427 6/5, 427+flags 6/1 (mean 3.5); growth 63.5% / 29.7% / 30.0%; no run passed. (2) ctl-r1 R3: 5 of 8 blockers on fix-written text, 3 on baseline text (R3-8 "present in the round-2 input"); 89% (R2) and 100% (R3) of new 427 findings `origin=changed`. (3) Labels drift up: FR-8/FR-9 force GAP rows to MAJOR (`spec-panel.md:328-329`), disagreements resolved to MAJOR. (4) Revisers applied 15 rows (11 findings, 4 citations; 9 minor) because the brief said "apply confirmed findings". (5) The verdict and the cap are prose; nothing computes "blocking" or ends the loop.
- **Risk**: Low.
- **Concrete anchors preserved**: every number in the five bullets above, verbatim from the seed brief and B §1.
- **Threshold preservation**:

| Source variant | Value | Disposition |
|---|---|---|
| seed / B | 8/4 (6.0), 6/5, 6/1 (3.5); 63.5 / 29.7 / 30.0% | preserved-exact |
| B | 5 of 8 on fix-written text, 3 on baseline | preserved-exact |
| seed | 89% / 100% `origin=changed` | preserved-exact |
| B | 15 of 15, 9 minor | modified-with-rationale: restated as 15 rows = 11 findings + 4 citation rows (B concession 9) |

## Base Weaknesses Addressed

| # | Issue in base (B) | Better variant | Fix approach | Change |
|---|---|---|---|---|
| 1 | `/tmp` scratch is outside the brief's "no edits to ... any other file" | B Round 2 (in-report mode), A and C concessions | Ledger inside the report from the first write; no scratch | 1 |
| 2 | A claim citing a prior can be graded `blocking:false` and drop a confirmed prior (B concession 5) | A | Freeze carried confirmed blockers | 2 |
| 3 | FR-8/FR-9 "MAJOR severity minimum" left beside bullet 2 | A | Edit the FR text in the copy; keep FR-10 | 3 |
| 4 | Option (g) lifts the cap with no mechanism | C | New run with a parent id | 6 |
| 5 | Missing skill falls back to a 427 run under the variant name | C | `E-SKILL-MISSING` | 5 |
| 6 | Q2 is a judged lateness gate that B's own Q1 argues against | A (overlap) | Q2 advisory; overlap ratchet | 9 |
| 7 | The auditor is the grader agent in another mode, with 15 lines of context | A, C | Separate fresh auditor with the full spec | 13 |
| 8 | FAIL mixes defects, coverage gaps and outages; an empty Reviser brief is undefined (B concession 8) | C | Reason codes; `incomplete`-only dispatches no edits; `NONE` brief | 7, 15 |
| 9 | Cross-class grader rule is unenforceable prose | A | Pinned model, `same-class` flag | 11 |
| 10 | "Notes are not instructions" does not reach the reviser, who reads the T08 range | A (Round 2 template evidence) | Display range filled by the coordinator | 15 |
| 11 | M1b follows computed statuses by construction, so the proxy loses independence | A | Reporting-only `claimed` label; M0 independent | 4, 17 |
| 12 | Skill install marked UNVERIFIED; no absence check; command published before its dependencies | A, C | Plain install; `test ! -e`; skill and agent first | 22 |
| 13 | No guard against drift of the copied command | A | Computed-diff test | 22 |
| 14 | Reuse row keeps "the ratchet idea" while late blockers block | A | "Do not reuse the stop rule" | 26 |
| 15 | Per-review FAIL-path audit costs calls and cannot change a FAIL | B Round 2, A | Move it offline | 13, 23 |

## Changes NOT Being Made (with rationale)

### Approach-level decisions where the base (or another variant) was kept

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| X-001, S-006 | A: loop directory with `findings-r<N>.json`, ledgers, cards, verdict files; C: `.spec-panel-stoprule/<run-id>/` with 13 files per round | B wins unanimously (95%); the saved T07 allows only the report, and the reviewer obeys that over the command (R2-A §3.2). |
| S-002, C-003 | A: 9 subcommands S0-S7; C: 6 operations over a state machine | Base vote B (65%); B's set plus `check` at `begin` gives A's `verify-prior` in a few lines (R2-B §5). |
| C-006, C-007 | A: shuffled cards with quote/outcome/example, one call per review | B wins at 70% and 65%; B's evidence entries marked verified/unverified carry cross-file defects, which C concedes quote-only grading misses (R2-C §1 item 12). |
| X-002, X-007, S-010 | C: ERROR and audit HOLD as terminal states outside PASS/FAIL | The brief demands "a binary PASS or FAIL verdict" (T07); C withdrew the third state (R2-C §1 items 5-6). C's meaning is kept as reason codes (Change 7). |
| X-003 | C: re-grade every carried blocker each round | A's freeze wins unanimously (95%); C concedes "convergence by attrition" (R2-C §1 item 4). |
| X-005 | C: override the FR-10 synthesis gate | A wins unanimously after C's own evidence that FR-10 feeds the AD-1 table (R2-C §3.2). |
| X-010 | C: variant persists its own baselines | B wins unanimously (95%); persistence needs repository writes the brief forbids (R2-C §1 item 2). |
| X-011, C-018 | C: separate `fix-packet.md`; rejected submission HALTs | A wins unanimously (90%); the reviser reads the report and T08's range (R2-A §3.1); HALT on nonblocking ids would reject the citation rows T08 requires (R2-C §3.1). |
| X-014 | C: no automatic retry; malformed output is ERROR | B wins unanimously (95%); C concedes (R2-C §1 item 7). |
| C-016 | A: separate `escalation.md`; C: `escalation.json` and `.md` | The report is the only file written (X-001); B's in-report Escalation section is kept, with A's fixed sentence added (Change 6). |
| C-032 (unresolved) | C: exclusive lock, fsync plus atomic rename, durable slot reservation, late-response quarantine | A and B never adopted it and C itself defers the durability stack to an enterprise pilot (R2-C §1 item 8). Only the fail-closed recovery rule and the `begin` marker are taken (Change 1); the overwrite residual is stated. |
| C-020 (unresolved) | C: quarantine rollback runbook | Not adopted: the three installed paths are additive and reinstallable from `src/`; only C argued it (R2-C §5 item 2). B's "delete the three installed paths" stays, after active writers stop. |
| U-001 | A: `## Rubric (frozen)` pasted byte for byte into every report, exit 6 if not | B's rubric sha in the sentinel plus the per-round hash check (Change 22) gives the same freeze with less reviewer text; no Round 2 advocate asked for the paste. |
| U-005 | A: `--severity-map` extension point | B's reuse unit is the script with `--rubric` and `--cap`; with labels reporting-only (Change 4) a label map has nothing to gate. |
| U-013 | B: `span_novel` as the late-found test | Replaced as a demoter by A's overlap (Change 9, 60%); still computed and printed. |
| U-022, U-023, U-029 | C: locks, deadlines (92-minute loop), SLOs | Out of scale for an n = 2 screen; C concedes and defers them (R2-C §1 item 8). |
| U-025 (part) | C: staged no-clobber publication with a manifest and quarantine | The absence check, skill-first order, load receipt and per-round recheck are taken (Change 22); the manifest and quarantine are not, as for C-020. |
| U-028 (part) | C: restrictive permissions, 30-day retention, no quote text in logs | S1 is a repository spec, not private data; only "quotes are inert data" is taken (Change 24). |

### Anchor-level omissions (non-base anchors not carried into the merged spec)

| Source variant | Anchor type | Anchor text or id | Reason for omission | Debate evidence |
|---|---|---|---|---|
| A | threshold | outcome >= 40 characters (S3) | B's outcome >= 8 words is the base check for the same field; two floors add a gate no one argued for | C-009 unresolved; R2-A and R2-B silent on it |
| A | threshold | k = 3 PASS-time audit sample | Replaced by all demotions at a PASS candidate | R2-A §1 B-4 ("the merge audits all demotions") |
| A | prediction | R3 confirmed r1 = 3, r2 = 1, confidence about 60% | Withdrawn by its author; B's identical point values carry it | R2-A §5 (d) |
| A | prediction | growth mean 22% (16-28%) | Inside B's 12-30% range; B's derivation is the base | C-023 to B at 95% |
| A | cost figures | 2-3 agent calls per loop, about 17 script calls, +4-10 min, +10-15% output tokens | A's one-call-per-review assumption fails once every form-valid claim is graded | INV-018; C-025 unresolved |
| A | named file | `refs/grader-brief.md` | The grader prompt is B's agent body plus the inline batch | S-003 to B at 70% |
| A | named files | `findings-r<N>.json`, `ledger-r<N>.json`, `cards-r<N>.md`, `grades-r<N>.txt`, `verdict-r<N>.json`, `rubric.sha256`, `escalation.md` | Report is the only file written | X-001 at 95% |
| A | named agent | `stoprule-grader` | Same frontmatter adopted under B's name `finding-grader` | C-005 to A at 85% (pinning, not the name) |
| A | exit codes | 2 usage, 7 spec-mismatch, 8 schema-invalid, 9 loop-exists | B's exit set (3, 4, 5, 6) is the base; the spec binding moves to the sentinel `spec=` hash under exit 5 (Change 2); a re-used report already carries a sentinel, so exit 9's case is caught by `begin` | C-003 to B at 65% |
| A | named system | 486-line master copy as the measured base | Measurement uses the 472-line Arm B file | X-009 at 95% |
| A | constraint | "reviser briefs are untouched" (section 4) | False under the T08 template; replaced by the placeholder-fill rule | R2-A §3.1 (A's own concession) |
| B | threshold | contested >= 25% over >= 8 (F2) | Replaced by A's 20% so the success share and the falsifier are one number; B's >= 8 minimum is kept | Change 14; INV-019 |
| B | threshold | FAIL path: up to 3 demotions + 1 hunk in-run | Moved offline | R2-B §1 A-7 |
| B | threshold | auditor context of 15 spec lines | Full spec | R2-B §1 A-6 |
| B | prediction | M1b 3.0 | Not independent by construction | R2-B §1 A-4; INV-015 |
| B | named system | `/tmp/stoprule-XXXXXXXX/` with `ledger.jsonl`, `diff.json`, `grader-in-K.txt`, `grader-out-K.txt`, `umask 077` | No scratch directory | R2-B §3.4 |
| B | rule | grader Q2 `same` demotes to `late-found` | Q2 is advisory | R2-B §1 A-5 |
| B | rule | `finding-grader` `audit` mode with `model: opus` | Separate auditor call | R2-B §1 A-6 |
| B | rule | option (g) "authorize one extra cycle"; 427 fallback with `stoprule: missing` | Contradicted by B's own exit 4; contaminates the arm | R2-B §1 A-1, A-2 |
| C | threshold | budgets reviewer 15 / grader 3 / audit 5 / helper 1 / fix 10 min; loop 92 min | No measured baseline; C withdraws them for S1 | R2-C §1 item 8 |
| C | threshold | SLOs: 100% reproducibility, 100% graded batches, >= 95% rounds within 24 min | S1 cannot show SLOs (C section 6) | R2-C §1 item 8 |
| C | threshold | 30-day retention | Owner-controlled; not needed for S1 | R2-C §1 item 8 |
| C | threshold | more than 100 findings or 1 MiB input gives ERROR | No envelope file exists in in-report mode; the batch limit of 6 bounds grader input | X-001; S-006 |
| C | prediction | R3 confirmed 2 and 3 (mean 2.5); growth 22% and 28% (mean 25%) | Withdrawn by C | R2-C §1 item 11 |
| C | cost figures | 11 agent calls per loop maximum, 6 above baseline; 5-7 helper calls per review | In-run audit is PASS-only; costs re-derived (Change 23) | R2-B §1 A-7 |
| C | named files | `manifest.json`, `state.json`, `events.jsonl`, `round-N/` (13 files), `fix-packet.md`, `disposition.json`, `escalation.json` | Report is the only file written | X-001 at 95%; X-011 at 90% |
| C | named file | `refs/rubric.txt` `stoprule-v1` text (CRITICAL as data loss, credential exposure, privileged action, outage) | B's rubric kind (e) "a step that loses data or takes an unsafe action" and its CRITICAL line cover the same ground | S-009 to B at 60% |
| C | exit codes | 0 PASS, 1 FAIL, 2 ERROR, 3 audit HOLD | Binary verdict with reason codes | S-010 to B at 90% |
| C | rule | grader classifies `critical|major|minor`; final class is the grader's | B's boolean `blocking` with labels reporting-only | C-030 to B at 90% |
| C | rule | human adjudicates every audit disagreement before delivery | No human inside the S1 loop; reinstatement recomputes FAIL | R2-C §1 item 6 |
| C | named skill | `sc-spec-panel-stoprule` (no suffix) | Removed by the installer (`install_skills.py:88-98`) | S-005 at 95%; R2-C §1 item 1 |

### Unresolved diff points carried as open items

C-009 is settled by Change 8, C-015 by Change 14 and C-025 by Change 23, each as an orchestrator decision recorded with its rationale (the debate did not settle them). C-020 and C-032 stay as stated in the table above.

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Every subcommand misreads the report; a crash mid-rewrite leaves no seal and the review is incomplete | Revert to base §2.0-2.3 scratch layout (and accept the X-001 brief conflict) |
| 2 | Medium | A wrong freeze keeps a false blocker open to R3; a wrong baseline check stops valid runs | Revert S0/S3 to base; keep B's `resolved_by` guard |
| 3 | Low | Reviewer still floors GAP rows to MAJOR if the copy edit is missed | Revert §3.1 to base sentence |
| 4 | Medium | More claims per batch; cost rises (Change 23) | Restrict `claim` lines to candidate blockers as in base S1 |
| 5 | Low | A missing skill stops the run instead of degrading | Restore base fallback sentence |
| 6 | Low | None beyond wording | Restore base (g) |
| 7 | Medium | Downstream consumers misread reason codes | Drop `reason=` from the sentinel; verdict line unchanged |
| 8 | Medium | The 20-character floor demotes short real quotes | Remove the floor; keep B's rule |
| 9 | High | Survivor count at R3 moves; predictions shift | Re-run the replay gate; revert to `span_novel` if overlap misclassifies |
| 10 | Low | Extra grader batch | Remove late-found from batches |
| 11 | Low | Grader model not honoured in a worker (B Q4) | Record observed model; no rollback needed |
| 12 | Medium | Transcript unavailable; integrity unverified | Report `grader-integrity: unverified`; keep `grade-raw` lines |
| 13 | High | PASS-time audit adds a call and can turn PASS to FAIL wrongly | Revert to base S6-S7 audit; keep the nonce seed |
| 14 | Low | Too few demotions to evaluate F2 | Reported NOT ESTABLISHED by design |
| 15 | High | Coordinator mis-fills the T08 range and routes the wrong set | Revert to the coordinator's 427 fill; record the change as a deviation |
| 16 | Low | Reviewer writes `verdict:` in prose and `finalize` refuses | Reviewer repairs to `brief-verdict:` in the same review |
| 17 | High | Success claim read on the wrong metric | None: the pre-registration fixes M0 before the first run |
| 18 | Medium | None in mechanics; lower stated odds | Text only |
| 19 | Medium | Early PASS mis-credited to bar (a) | Text only; `brief_pass` recomputable from the ledger |
| 20 | Medium | More falsifiers; a positive result is rarer | Text only |
| 21 | Low | Ablation not authorized; attribution stays open | Text only |
| 22 | Low | Install step order wrong; command visible before skill | `test ! -e` stops the copy; remove the three paths |
| 23 | Low | Estimates wrong | M6 measures actual costs |
| 24 | Low | None | Text only |
| 25 | Low | None | Text only |
| 26 | Low | None | Restore base row |
| 27 | Low | A number lost in compression | Every number is listed in Change 27's preservation table |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T15:55:00Z
- Note for the merge executor: convergence is BLOCKED_BY_INVARIANTS. The merged spec must carry the HIGH Invariant Resolution Map dispositions in its sections 5, 6 and 7, and must not describe the design as converged.
