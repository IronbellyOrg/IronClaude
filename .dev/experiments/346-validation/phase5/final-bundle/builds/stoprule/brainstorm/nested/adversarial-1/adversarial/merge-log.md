# Merge Execution Log

## Metadata
- Base: Variant B (sonnet:analyzer), `variant-2-sonnet-analyzer.md` (Round 2 report-resident form)
- Executor: merge-executor agent
- Changes applied: 27 of 27 planned
- Status: partial (all changes applied; post-merge validation FAIL on one contradiction inherited from the plan, returned to the orchestrator)
- Timestamp: 2026-11-08T15:40:12Z
- Merged output: `/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/.dev/brainstorms/346-stoprule/nested/adversarial-1/merged-output.md`
- Convergence context: BLOCKED_BY_INVARIANTS (92%, 60 of 65 points). The merged spec states this in its status block (lines 8-10) and in section 7, and does not describe the design as converged. Open HIGH invariants carried: INV-009 (partly resolved; section 6.2 risk 12, section 7 question 2) and INV-029 (unresolved at n = 2; section 5.2 attribution paragraph, section 6.2 risk 18, section 7 question 5).

## Changes Applied

### Change 1: In-report storage, no scratch directory
- **Status**: Applied
- **Source**: Variant B Round 2 (R2-B §3.4); R2-A §1 B-1; R2-C §1 item 2, §3.3
- **Target**: Base §2.0 bullet 4, §2.1 Parts table, §2.3 S0, S3, S4, S9, §3.2 script writes, §6.2 risk 9, §7 Q4
- **Before**: Ledger in `/tmp/stoprule-XXXXXXXX/` (umask 077) with `ledger.jsonl`, `diff.json`, `grader-in-K.txt`, `grader-out-K.txt`; embedded at `finalize`; scratch removed by `finalize`.
- **After**: Report is the only file written; fenced ledger block from the first write; `begin` marker `<!-- stoprule begin review=N/3 spec=<12hex> baseline=<12hex|none> nonce=<16hex> -->`; diff recomputed per call; batch printed to stdout and passed inline; reply on stdin; `finalize` rewrites in place. C's recovery rule added to S0. Risk 9 rewritten ("no `/tmp` permission is assumed"); ctl-r1 `/tmp/ironclaude-batch.*` kept as history. `/tmp` half of Q4 deleted. INV-001 residual stated as §6.2 risk 11 (applied with Change 24).
- **Provenance tag**: `<!-- Source: Variant B Round 2 (debate-transcript R2-B §3.4 "In-report mode"), Base §2.0 bullet 4 → Target §2.0 bullet 4, Change #1, Disposition: modified ... -->`
- **Thresholds**: `umask 077` dropped-with-rationale (no scratch dir); sentinel `review=N/3`, `rubric=<12hex>`, `ledger=<12hex>` preserved-exact; "about 2-3k tokens" per printed batch preserved-exact in §6.1.
- **Dropped anchors**: `/tmp/stoprule-XXXXXXXX/`, `ledger.jsonl`, `diff.json`, `grader-in-K.txt`, `grader-out-K.txt` (Variant B; decision basis X-001 at 95%; replacement: fenced ledger block in the report). Base risk 9 sentence "a worker sandbox that blocks `/tmp` would break S0 (fail closed: exit 5 and the review stops)" (Variant B; no `/tmp` use remains; replacement: risk 9 in-report text).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: Prior lifecycle: freeze, prior-report check, baseline binding, adjudicated exit
- **Status**: Applied
- **Source**: Variant A §2.3 S1 (U-002), S3 guard (U-003), S4 freeze, §2.4 `spec_sha256` (U-009); Variant C §2.4 (R2-C §1 item 4)
- **Target**: Base §2.3 S0, S2, S3; §2.4; §3.2 failure table; sentinel
- **Before**: No freeze; priors re-graded; no prior-report check; no baseline binding; open prior counted only without a claim line.
- **After**: S0 runs `check` on P (exit 5 "prior-verdict-mismatch") and checks baseline sha256 against P's `spec=` (exit 5 "baseline is not the text review N-1 reviewed"); sentinel gains `spec=<12hex>`; S3 freeze with A's sentence verbatim; adjudicated exit to `withdrawn-audit`; B's `resolved_by` guard kept; `unresolved` in §2.4 counts frozen open/regressed priors.
- **Provenance tag**: `<!-- Source: Variant A §2.3 S1 (`verify-prior`, U-002) and §2.4 `spec_sha256` (U-009), Change #2, ... -->`, `<!-- Source: Variant A §2.3 S3 prior-status guard (U-003) and S4 freeze, Change #2 (a) ... -->`, `<!-- Source: Variant C §2.4 "explicit adjudicated exception" ... Change #2 (e) ... -->`
- **Thresholds**: exit 5 preserved-exact (extended messages); A's exit 5 `prior-verdict-mismatch` modified-with-rationale (merged into B's exit 5); A's exit 7 `spec-mismatch` modified-with-rationale (replaced by the `spec=` check under exit 5); 12-hex prefixes preserved-exact.
- **Dropped anchors**: base verdict comment "an open prior needs a claim line; without one it counts" (Variant B; decision basis: freeze makes every frozen open prior count; replacement: `p.frozen and p.status in ("open","regressed")`).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ❌ (see Post-Merge Validation: "cap-time audit pool" has no audit to feed)

### Change 3: FR-8/FR-9 source edit, bullet 2 replaced, FR-10 kept
- **Status**: Applied
- **Source**: Variant A §3.1 item 4; R2-A §3.4; R2-B §1 A-3, §3.3; R2-C §3.2
- **Target**: Base §3.1 first bullet; §7 Q5
- **Before**: "FR-8/FR-9 stay in the file; Review Loop bullet 2 is what overrides their 'MAJOR minimum'".
- **After**: FR-8/FR-9 in the copy read "generates a finding; it is blocking only under rubric B1-B3 of the Review Loop, otherwise minor"; anchors `spec-panel.md:259`, `:328-329`, `:330`, "MAJOR severity minimum" kept; FR-10 unchanged; bullet 2 sentence "an FR-8/FR-9 row is a candidate ... not an automatic MAJOR" kept; Q5 (now Q9) restated.
- **Provenance tag**: `<!-- Source: Variant A §3.1 item 4 (R2-A §3.4), Change #3, Disposition: modified ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: Reviewer label kept for reporting only; every form-valid claim graded
- **Status**: Applied
- **Source**: Variant A §2.4 `claimed`; R2-A §1 B-2; R2-B §1 A-4; R2-C §1 item 13
- **Target**: Base §2.2, S1, S8, S9 `label_mismatch`, §5.3 M1b row; consequential: §2.7 severity row, §3.2 "do not" list
- **Before**: No label in schema; claims only for candidate blockers; M1b predicted 3.0 "by construction".
- **After**: `"claimed":"critical|major|minor"` on every claim; "appears in the schema only as `claimed`, which no computation reads"; A's "CRITICAL and MAJOR labels are kept for reporting only"; S1 one claim per labelled finding; S8 prose may carry severity words, never a verdict; `label_mismatch` informational only; M1b row deleted. Consequential edits found by the contradiction re-scan: §2.7 severity row "REMOVED as a label" became "REMOVED as a gate" with the label stated as the M0 proxy; §3.2 "no severity words before `status`" now names the `claimed` exception.
- **Provenance tag**: `<!-- Source: Variant A §2.4 `claimed` field (R2-A §1 B-2), Change #4, ... -->`
- **Thresholds**: B M1b 3.0 dropped-with-rationale (not independent); A proxy mean 4 preserved-exact (Change 17).
- **Dropped anchors**: base S8 "Non-blocking observations stay in the prose as notes without severity words" (Variant B; contradicts the recorder's need for labels; replacement: S8 sentence allowing the reviewer's severity words, never a verdict).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: Skill activation line and fail-closed missing skill
- **Status**: Applied
- **Source**: Variant A §3.1 item 3; Variant C §3 (`E-SKILL-MISSING`)
- **Target**: Base §3.1 first bullet (activation line) and fallback sentence
- **Before**: Fallback ran the 427 loop with `stoprule: missing`.
- **After**: `> Skill sc:spec-panel-stoprule-protocol` under the title (`install_skills.py:30-32`); missing at both installed and project `.claude/` copies stops with `E-SKILL-MISSING`.
- **Provenance tag**: `<!-- Source: Variant C §3 (`E-SKILL-MISSING`), Base §3.1 fallback sentence → Target §3.1, Change #5, ... -->`
- **Dropped anchors**: `stoprule: missing` header marker (Variant B; X-013 at 95%; replacement: `E-SKILL-MISSING`).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: No in-loop cap lift, parent-run lineage
- **Status**: Applied
- **Source**: Variant C §2.5; R2-B §1 A-1
- **Target**: Base §2.5 (f), (g)
- **Before**: (g) "authorize one extra cycle limited to the ids in (b) (the user lifts the cap, the loop never does)".
- **After**: (g) accept with known issues, or start a new user-authorized run recording `ledger=` as `parent=`; "The loop never lifts its own cap." (f) adds "This command will not run review 4." Canonical cap sentence and exit 4 unchanged.
- **Provenance tag**: `<!-- Source: Variant C §2.5 last paragraph (R2-B §1 A-1), Base §2.5 (g) → Target §2.5 (g), Change #6, ... -->`
- **Thresholds**: 2 fix cycles / 3 reviews preserved-exact; exit 4 preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: Binary verdict with FAIL reason codes
- **Status**: Applied
- **Source**: Variant C §6; R2-B §1 C-1; R2-A §1 C-1; R2-C §1 item 5
- **Target**: Base §2.4, S5, S9 sentinel, §3.2 failure table, §5.2
- **Before**: FAIL with no reason; no rule kept unconfirmed claims out of the brief.
- **After**: reason set `confirmed`, `unresolved-prior`, `incomplete`; sentinel `reason=...` and `pre_audit=PASS|FAIL`; only `confirmed` and `unresolved-prior` ids enter the brief; `incomplete`-only gives the "make no spec edit" brief; §5.2 admission rule "more than one `incomplete` review" invalidates the replicate.
- **Provenance tag**: `<!-- Source: Variant C §6 failure table semantics with A and B rules ..., Change #7, Disposition: merged-from-multiple ... -->`
- **Thresholds**: "more than one" incomplete review preserved-exact; "two failures" leave claims `unconfirmed` preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: Form rule settled, one repair, omission quoting, post-repair fate
- **Status**: Applied
- **Source**: Variant A §2.3 S3; Base §2.3 S2; Variant C §2.3 omission sentence
- **Target**: Base §2.3 S2, §2.6 row 2, §3.2 rubric B1, §6.2 risk 2
- **Before**: whitespace-normalised substring, <= 300 characters; fate after repair `minor-form` only in the §2.6 table.
- **After**: normalised substring, >= 20 non-space and <= 300 characters, normalisation rule with A's shortcut note; non-unique quote repairable (exit 3); post-repair failure is `minor-form`, listed in Computed result and Escalation, in the PASS-time audit pool, never `incomplete`; only an uncovered hunk gives `incomplete`; rubric B1 gains C's omission line; risk 2 residual added.
- **Provenance tag**: `<!-- Source: Variant A §2.3 S3 ... + Base §2.3 S2 ..., Change #8 (a)-(b), Disposition: merged-from-multiple ... -->`, `<!-- Source: orchestrator decision in refactor-plan Change #8 (d) resolving INV-008 ... -->`
- **Thresholds**: quote >= 20 non-space preserved-exact; <= 300 preserved-exact; span <= 120 preserved-exact; outcome >= 8 words preserved-exact; A outcome >= 40 characters dropped-with-rationale; evidence within 3 lines preserved-exact; 1 repair preserved-exact; C raw line span dropped-with-rationale.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Ratchet by changed-line overlap, prior-link hash rule, Q2 advisory
- **Status**: Applied
- **Source**: Variant A §2.3 S3; Variant C §2.4 step 2 (U-027); R2-B §1 A-5
- **Target**: Base S2 anchor sentence, S5 final-status rule, §2.6 row 3, §3.1 bullet 5, §3.2 rubric Q2, §5.1 (R3-8 row and a note), §7 Q1; consequential: §3.4 ratchet test
- **Before**: `span_novel=false` and no prior gives `late-found`; Q2 `same` demotes.
- **After**: late-found unless an anchor line is in the `difflib` changed-line set (whitespace-only ignored, +/-1 around pure deletions) or a valid prior link (identical outcome hash and identical quote hash or changed anchor); one prior per claim, duplicates `duplicate-of:<id>`; `span_novel` printed as data; Q2 recorded, never demotes; bullet 5 reads "must quote a line changed by the last fix or cite a valid open prior id"; Q1 closed; §5.1 replay flagged for re-run.
- **Provenance tag**: `<!-- Source: Variant A §2.3 S3 (`difflib` changed lines, +/-1 around pure deletions) + Variant C §2.4 step 2 ..., Change #9, Disposition: modified ... -->`
- **Thresholds**: +/-1 preserved-exact; 4.3 of 8 and 0.85 of 1 preserved-exact as pre-merge replay, flagged; 4.6-5.0 of 8 (R2-B) preserved-exact; about 4-5 (R2-A) preserved-exact; R3-8 p about 0.7 modified-with-rationale (re-derived by replay gate); 89% / 100% preserved-exact.
- **Dropped anchors**: base test "span present in baseline -> `late-found`" (Variant B; rule replaced; replacement: "no anchor line in the changed-line set and no valid prior -> `late-found`" plus prior-link tests). Base Q1 argument text (Variant B; closed; key facts kept in the "Closed by the debate" note).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: Late-found claims graded in the same batch
- **Status**: Applied
- **Source**: Variant C §2.4 step 3
- **Target**: Base S3
- **Before**: only eligible claims batched.
- **After**: every form-valid claim batched, late-found included; `late_grade` shown in Escalation (d) and "PASS with known debt"; never changes the verdict; extra batch in the same Agent message.
- **Provenance tag**: `<!-- Source: Variant C §2.4 step 3, Change #10, Disposition: modified ... -->`
- **Thresholds**: at most 6 claims plus 2 canaries preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Grader primitive: pinned model, `same-class` flag, grade mode only
- **Status**: Applied
- **Source**: Variant A §3.5, §2.6 bullet 3; R2-B §1 A-6, §4 X-016; R2-C §1 item 9
- **Target**: Base §2.0 bullet 2, §2.1 Agent row, S4, §3.3; consequential: §2.6 grader row, S9 sentinel
- **Before**: cross-class rule by prose; `grade` and `audit` modes; grader reads a batch file.
- **After**: pinned `model: sonnet`; sentinel `grader_model=<model>[,same-class]`; grade mode only; "Read no file"; frontmatter kept (`tools: Read`, `maxTurns: 10`, `permissionMode: plan`, `category: quality`); `tools:` emptiness left to section 7 question 1. §2.6 row "Grader really is a different class" rewritten to the pinned-model form (found by the contradiction re-scan).
- **Provenance tag**: `<!-- Source: Variant A §3.5, §2.6 bullet 3 ..., Change #11, Disposition: modified ... -->`
- **Thresholds**: `maxTurns: 10` preserved-exact; `why` at most 25 words preserved-exact; auditor `model: opus` dropped-with-rationale.
- **Dropped anchors**: "opus if the reviewer is a sonnet-class model; the command says 'a class different from your own'" (Variant B; X-016 at 95%; replacement: pinned model plus `same-class` record). `audit` mode reply `{"cid":"C3","real":true,...}` and hunk-probe reply (Variant B; auditor is a separate call, Change 13).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: Grader reply integrity check
- **Status**: Applied
- **Source**: INV-009; Base §2.1 saved replies; Variant C §2.6; Variant A §2.3 S5
- **Target**: Base §2.2, S5, §2.6 row 4, new recorder step after S10, §5.2 M8, §3.2 function list, §6.2 risk 12 (with Change 24), §7 Q2 (with Change 25)
- **Before**: replies saved byte for byte to `grader-out-K.txt`.
- **After**: `grade-raw{batch,sha256,text}` appended before parsing; `check` re-parses, exit 6 on difference; `verify-transcript` prints `grader-integrity: verified|mismatch|unverified`; M8 with `mismatch` voiding the replicate; residual stated.
- **Provenance tag**: `<!-- Source: INV-009 (invariant-probe) using Base §2.1 saved-reply idea, Variant C §2.6 raw-response persistence and Variant A §2.3 S5, Change #12, ... partly resolved -->`
- **Thresholds**: exit 6 preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 13: Audit restructure
- **Status**: Applied
- **Source**: Base S6-S7; Variant A §2.6, §5; Variant C §5; R2-A §5 item 4 / A-008; R2-B §1 A-6, A-7
- **Target**: Base §2.0 bullet 3, S3 seed, S6-S7, new offline-audit bullet, §3.2 seed sentence, §5.2 M4, §7 Q2; consequential: §6.2 risk 4, §3.2 function list
- **Before**: auditor = `finding-grader` audit mode with 15 spec lines; FAIL path samples up to 3 demotions plus a hunk in the run; seed `sha256(sealed ledger)[:8]`.
- **After**: in-run audit only at a PASS candidate by a fresh general-purpose auditor with the full spec over all demotions plus 2 hunks; reinstatement gives `confirmed-audit` and a recomputed FAIL; auditor unavailable gives FAIL `incomplete`; no FAIL-path in-run audit; offline two-sided stratified sample (25% nonblocking min 2, 25% confirmed min 2, 25% `resolved` priors min 2, all claimed-critical demotions); seed `sha256(nonce || review || ledger)`; owner labels 5 (k = 5); Q2 closed. Risk 4's "all but 3 per review" rewritten (found by the contradiction re-scan).
- **Provenance tag**: `<!-- Source: Variant A §2.6 (fresh full-spec auditor) + Base §2.3 S6-S7 + Variant C §5 ..., Change #13, ... -->`
- **Thresholds**: PASS candidate all demotions plus 2 hunks preserved-exact; FAIL-path up to 3 plus 1 modified-with-rationale (moved offline); 15 lines modified-with-rationale (full spec); A's k = 3 dropped-with-rationale; owner spot-check of 5 preserved-exact; C 25% min 2 (two strata) preserved-exact; `resolved` priors 25% min 2 new; seed modified-with-rationale.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ❌ (see Post-Merge Validation)

### Change 14: One audit falsifier with a stated share and a minimum sample
- **Status**: Applied
- **Source**: Variant A §5 falsifier 3; Base §5.4 F2; Variant C §5; R2-C §3.4
- **Target**: Base §5.4 F2, §5.2 M4, §5.3 new row
- **Before**: F2 contested/sampled >= 25% over >= 8.
- **After**: F2 = offline demotion error rate > 20% over >= 8 audited demotions, else NOT ESTABLISHED; rollout bar <= 10%, zero missed CRITICAL, >= 20 audited true blockers, about 14% bound for 0 of 20; §5.3 row predicted 10-15%; A's error-rate definition kept.
- **Provenance tag**: inline in F2 text "(Change #14)"; §5.3 row "(Change #14, from A)"; §5.4 section tag
- **Thresholds**: 20% preserved-exact; 10-15% preserved-exact; >= 8 preserved-exact; 25% modified-with-rationale (one number with the success share); C 10% / 20 / zero CRITICAL preserved-exact (rollout); 14% preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 15: Reviser routing: stable ids, display range, `NONE` rule, disposition check
- **Status**: Applied
- **Source**: R2-A §3.1; R2-B §1 A-9; R2-C §3.1; Variant C §2.5 (U-024)
- **Target**: Base §3.1 bullet 6, S9 brief, §4 new paragraph, §5.2 M5, §5.3 arithmetic (restatement), §3.2 function list
- **Before**: brief from confirmed findings only; coordinator fill undefined.
- **After**: stable ledger ids; D1..Dk display ids (new confirmed first, then frozen priors) with a mapping table; coordinator fills `{{R2_FIRST_ID}}-{{R2_LAST_ID}}` and `{{R2_CITATION_COUNT}}`, `NONE` and `0` when empty; D11 step order unchanged; T08 reading flagged to section 7 question 3; `check-disposition` feeds M5 and F6, never rejects; "the reviser reads the report, not the command" kept.
- **Provenance tag**: `<!-- Source: R2-A §3.1 (placeholder fill) + R2-C §3.1 ... Change #15 (b)-(d), Disposition: merged-from-multiple ... -->`
- **Thresholds**: F6 2 or more ids per cycle preserved-exact; "15 of 15, 9 minor" modified-with-rationale to "15 rows: 11 findings plus 4 citation rows, 9 minor" (§1 and §5.3 arithmetic); C's HALT dropped-with-rationale.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 16: Verdict precedence and the brief-verdict line
- **Status**: Applied
- **Source**: R2-A §3.6; R2-B §3.2; R2-C §3.5
- **Target**: Base §3.1 bullet 3, S9 refusal rule, sentinel
- **Before**: refusal of any hand-typed verdict; no place for the brief's verdict.
- **After**: coordinator and metrics read only the last line; `brief-verdict:` prose line allowed; `finalize` computes `brief=PASS|FAIL` covariate; precedence question carried to section 7 question 4 (Change 25).
- **Provenance tag**: `<!-- Source: R2-A §3.6 + R2-B §3.2 + R2-C §3.5, Change #16, Disposition: merged-from-multiple ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 17: Two counts, both pre-registered, with predictions
- **Status**: Applied
- **Source**: Variant A §5; Base §5.2 M1, §5.3; R2-B §3.1; `FLG2/metrics.json` via INV-015
- **Target**: Base §5.2 metric list, §5.3 table and derivation
- **Before**: M1 script count as headline; M1b label proxy.
- **After**: M0 = recorder proxy over new R3 findings by `claimed` CRITICAL/MAJOR (pre-registered bar (a)); M1 = script `confirmed` plus frozen `unresolved-prior` (new, pre-registered); opposite-direction note; §5.3 rows M0 (r1 5 (4-7), r2 3 (1-4), mean 4.0, about 0.2) and M1 (r1 3, r2 1, mean 2.0, each 1-5, about 0.5); M0 derivation added; B's arithmetic kept.
- **Provenance tag**: `<!-- Source: Variant A §5 metrics table + Base §5.2 M1 + R2-B §3.1 + `FLG2/metrics.json` ..., Change #17 ... -->`, `<!-- Source: Variant A §5 prediction table ..., Change #17 ... -->`
- **Thresholds**: bar <= 3 in both and control 6.0 preserved-exact; A mean 4 preserved-exact; B M1 values preserved-exact; 0.55-0.85, 2.8, 0.76 preserved-exact; A's r1 3 / r2 1 at about 60% dropped-with-rationale; C's 2 and 3 dropped-with-rationale; M0 prediction new; M1b dropped.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 18: Bar (c) spread logic and its predicted outcome
- **Status**: Applied
- **Source**: D10/D11 bar (c) via INV-014; ARMB-REPORT; Variant C §5; Base §5.3
- **Target**: Base §5.3 (new paragraph), §5.4 (new F0)
- **Before**: bar (c) not stated.
- **After**: effect = 6.0 - mean > max(4, |r1 - r2|), equivalent to r1 + r2 <= 3; point prediction (3, 1) NOT MET; P = 0.41 before and about 0.27 after discount; M0 (5, 3) not met, about 0.1; F0 added.
- **Provenance tag**: `<!-- Source: D10/D11 bar (c) via INV-014 + Variant C §5 ... Change #18, Disposition: new (derived) ... -->`
- **Thresholds**: control spread 4 and Arm B spread 5 preserved-exact; derived r1 + r2 <= 3 new; 0.27 / 0.41 / 0.1 new (labelled); 0.5 / 0.76 preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 19: What PASS means, and the path after an early PASS
- **Status**: Applied
- **Source**: D10/D11 bar (a) via INV-017; Variant C §5; Base §5.3 M7
- **Target**: Base §5.2 M7, §2.3 S0, §5.3 M7 rows
- **Before**: M7 "PASS reached and at which review"; post-PASS path undefined.
- **After**: `script_pass` and `brief_pass`; bar (a) clean-PASS reads `brief_pass`; S0 accepts a prior PASS as a confirmation review with the `NONE` brief; growth reported at PASS review and R3; predictions about 0.2 and about 0.05.
- **Provenance tag**: `<!-- Source: INV-017 + Variant C §5 (early stopping) + Base §5.3 M7, Change #19 (b), Disposition: new -->`
- **Thresholds**: PASS about 0.2 preserved-exact (as `script_pass`); `brief_pass` about 0.05 new.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 20: Falsifier set, the M1c quality bar, and growth
- **Status**: Applied
- **Source**: Base §5.4 F1-F7, §5.2/5.3 M1c and growth; Variant A §5 falsifiers 4-6; R2-B §3.1; INV-028, INV-030
- **Target**: Base §5.3 M1c and M2 rows (plus an R1 row for F8), §5.4; consequential: §6.2 risk 8 ("F1" now "F1a, F1b")
- **Before**: F1-F7; M1c bar "no worse than 6.0".
- **After**: F0, F1a, F1b (filter-only, about 0.7), F2, F3, F4 (with A falsifier 6), F5 (with INV-028 note), F6, F7, F8, F9; M1c quality bar <= 3.0 with 6.0 kept as no-harm floor; growth 20% (12-30%) or 25-30% without the fill; R1 confirmed 5-8 (of 9-17 proxy) row.
- **Provenance tag**: `<!-- Source: Base §5.4 F1-F7 + Variant A §5 falsifiers 4-6 + INV-030, Change #20, ... -->`
- **Thresholds**: F1 >= 4 / >= 5.5 preserved-exact; M1c 4.5 (2-7), 6.0, about 0.8 preserved-exact; M1c <= 3.0 and about 0.7 new; F3 3, F5 30%, F6 2, F7 25 min preserved-exact; A falsifiers 4 and 5 preserved-exact; A R1 5-8 preserved-exact; growth 20% / 22% / 18% / 12-30% / about 0.9 preserved-exact; 25-30% preserved-exact; A 22% (16-28%) and C 22/28% dropped-with-rationale; 44.4%, 63.5%, 29.7%, 30.0% preserved-exact; INV-028 values preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 21: Attribution; optional ablation arm
- **Status**: Applied
- **Source**: INV-029, INV-025; R2-A §3.1; Variant C §5
- **Target**: Base §5.2 (new paragraph), §6.2 (new risk 18), §7 (question 5, with Change 25)
- **Before**: no attribution statement.
- **After**: "What this design can attribute (INV-029, open)" paragraph; Arm B bar (c) unreachable; ablation arm `spec-panel-stoprule-noscript`, 2 replicates, about 10 sessions, falsifying condition M0 <= 3; risk 18.
- **Provenance tag**: `<!-- Source: INV-029 and INV-025 (invariant-probe) + R2-A §3.1 + Variant C §5 ..., Change #21, Disposition: new ... -->`
- **Thresholds**: Arm B mean 3.5, spread 5 preserved-exact; ablation 2 replicates, about 10 sessions new (labelled estimate).
- **Note**: risk numbered 18 so that Change 24 can append items 11-17 as the plan specifies.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 22: Install contract and tests
- **Status**: Applied
- **Source**: Variant A §4, §3.6; Variant C §4 steps 2, 4, 5, 7; R2-B §1 C-3, §3.5
- **Target**: Base §4 install paragraphs, §3.4 tests
- **Before**: skill/agent install UNVERIFIED; manual route copied command first; no absence check.
- **After**: `install_skills.py:100-104` and `:13-21` sentence; `test ! -e` on 3 destinations; agent and skill copied before the command; load receipt; per-round hash recheck (exit 5); tests: computed diff, activation line, `_has_corresponding_command(...) is False`, fixtures for Changes 2, 7, 8, 9, 12, 13, 15.
- **Provenance tag**: `<!-- Source: Variant A §4 (`install_skills.py:100-104`), Change #22 (a), ... -->`, `<!-- Source: Base §4 (original, modified) + Variant C §4 steps 2, 4, 5, 7, Change #22 (b)-(d), ... -->`, `<!-- Source: Variant A §3.6, Change #22 (e), Disposition: preserved-exact -->`
- **Thresholds**: 472 lines, `c8d80346a96c` preserved-exact; 14 lines preserved-exact; 3 installed items preserved-exact; A 486-line base and C 2 surfaces dropped-with-rationale.
- **Dropped anchors**: "the same behaviour for skills and agents is UNVERIFIED, so the experiment uses the manual route" (Variant B; replaced by the `install_skills.py:100-104` sentence per the plan).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 23: Cost table re-estimated
- **Status**: Applied
- **Source**: Base §6.1; R2-B §1 A-7; Variant A §6.2; Variant C §6; INV-018
- **Target**: Base §6.1 table and break-even sentence
- **Before**: 9-11 Bash, 2-4 agent calls per review; 27-33 and 6-12 per loop.
- **After**: 7-9 Bash per review, 21-27 per loop; grader calls ceil(claims/6): 3-4 at R1, 1-2 at R2/R3, 5-9 per loop; auditor 0-1 per loop; recorder `verify-transcript` 1 per review; sessions +1 probe per replicate, +10 for the ablation arm; 2-3k per printed batch; break-even sentence updated.
- **Provenance tag**: `<!-- Source: Base §6.1 (original, modified) + R2-B §1 A-7 + INV-018, Change #23, ... -->`
- **Thresholds**: 9-11 / 27-33 modified-with-rationale; 2-4 / 6-12 (median 8) modified-with-rationale; R2-B 3-7 modified-with-rationale; A and C figures dropped-with-rationale; 3-5 / 9-15, 6-10 min / 18-30 min, 30-40k / 90-120k, 2-3k, F7 25 min preserved-exact.
- **Dropped anchors**: Write/Edit row item "saved grader replies" (Variant B; no saved files in in-report mode; replacement: "ledger lines, repair edit").
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 24: Risk list additions
- **Status**: Applied
- **Source**: INV-001, INV-009, INV-020, INV-023, INV-025, INV-026; R2-C §3.3, §3.5; Variant C §2.4 step 5
- **Target**: Base §6.2 items 11-17 (item 9 already modified under Change 1); §3.3 agent body (inert-data line)
- **Before**: items 1-10.
- **After**: items 11 (re-dispatch overwrites the marker), 12 (grader reply transcription), 13 (empty diff, R1 coverage off), 14 (canary recognition), 15 (FR edit moves the M0 labels), 16 (outcome wording), 17 (instruction authority, quotes as inert data); C's inert-data line also placed in the grader body.
- **Provenance tag**: `<!-- Source: invariant-probe INV-001, INV-009, INV-020, INV-023, INV-025, INV-026 + R2-C §3.3, §3.5 + Variant C §2.4 step 5, Change #24 (items 11-17), Disposition: new -->`
- **Thresholds**: 3 of 8 late-found all real preserved-exact; 6 installed files, 2 test files, 380-line script preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 25: Open questions updated
- **Status**: Applied
- **Source**: Base §7; Variant A §7 Q1; R2-C §3.1, §3.5; INV-009, INV-029
- **Target**: Base §7
- **Before**: 9 questions (Q1 ratchet, Q2 audit promotion, Q4 including `/tmp`).
- **After**: new 1-6 (empty `tools:`, transcript availability, T08 reading, instruction precedence, ablation arm, `minor-form` omissions), then base Q3, Q4 first half, Q5 (as modified), Q6, Q7, Q8, Q9 as 7-13; a convergence note naming questions 2 and 5 as the open HIGH invariants; closed questions listed in one "Closed by the debate" line.
- **Provenance tag**: `<!-- Source: Base §7 (original, modified) + Variant A §7 Q1 + R2-C §3.1, §3.5 + INV-009, INV-029, Change #25, ... -->`
- **Thresholds**: per-claim grading about 6-10 calls per review preserved-exact; "14 more lines" and `spec-panel-review-loop.md:154` preserved-exact.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 26: Reuse section: implement row
- **Status**: Applied
- **Source**: Variant A §8 implement row
- **Target**: Base §8 `/sc:implement` final review row
- **Before**: "The ratchet idea and `escalation` format only".
- **After**: "**Do not reuse the stop rule.** `qa.md` derives severity from checklist answers with a parent Read-back (`qa.md:37-97`) and keeps `late` blockers blocking (`qa.md:167`)." Other rows and the `--rubric`/`--cap` sentence unchanged; `qa.md:79` kept in the row's second column.
- **Provenance tag**: `<!-- Source: Base §8 (original); `/sc:implement` final review row from Variant A §8 implement row, Change #26, ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 27: Section 1 cut to at most 5 lines
- **Status**: Applied
- **Source**: Base §1 points 1-5
- **Target**: Base §1
- **Before**: 5 numbered items, about 15 wrapped lines.
- **After**: 5 single-line bullets with the plan's numbers.
- **Provenance tag**: `<!-- Source: Base §1 points 1-5 (original, modified) + seed brief, Change #27, ... -->`
- **Thresholds**: 8/4 (6.0), 6/5, 6/1 (3.5); 63.5 / 29.7 / 30.0% preserved-exact; 5 of 8 / 3 preserved-exact; 89% / 100% preserved-exact; 15 of 15, 9 minor modified-with-rationale (15 rows = 11 findings + 4 citations).
- **Dropped anchors** (compression, Variant B, decision basis: plan requirement of at most 5 lines; replacement: none unless noted): `spec-panel-round3.md:179-189` (the §5.1 table keeps `:181-189`); "Part 1, lines 21-31"; R3 id lists "R3-1, 2, 3, 5, 6" and "R3-4, 8, 9" (kept as §5.1 table rows); flg-r2 N12 sentence (kept in §5.1); "427 fixed growth, not convergence"; "seven prose bullets"; base point 5 summary of the mechanism (covered by §2.0).
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ one H1, eight H2 sections numbered 1-8 in the required order, H3 subsections unchanged in number and order (2.0-2.7, 3.1-3.6, 5.1-5.4, 6.1-6.2).
- Section ordering: ✅ matches the plan's Merged Spec Skeleton; no H2 added, dropped or reordered.
- Document flow: ✅ provenance header (Section 6 format) at the top; every H3 section and every incorporated block carries a `<!-- Source: ... -->` tag; one stray duplicate table header in §6.1 was removed during the merge.

### Internal References
- Total references checked: 39 occurrences of `section N[.N]` with optional `question`, `risk`, `bullet` or `S` suffix
- Resolved: 39 (section 7 questions 1-5 and 8; section 6.2 risks 2, 12, 18; sections 1, 2.3, 2.3 S2, 2.4, 3.1, 3.1 bullet 6, 4, 5, 5.2, 6; "section 11" refers to `docs/designs/spec-panel-review-loop.md`, an external file)
- Broken: 0. A stale "F1" in §6.2 risk 8 was updated to "F1a, F1b".

### Threshold Preservation
- Every threshold in the plan's preservation tables is present with its exact value or carries a disposition recorded above (grep check over about 95 anchor values: all present).

### Dropped-Anchor Audit
- All dropped, paraphrased or rewritten anchors are listed under their change above with source variant, change number, decision basis and replacement. The plan's own "Anchor-level omissions" table covers the non-base anchors not carried.

### Contradiction Re-Scan
- New contradictions introduced: 1 (inherited from the plan; not resolvable by the executor without a strategy decision)
- Details:
  1. Cap-time audit has no mechanism. Change 2 (e) puts reviser-rejected frozen ids into "the PASS-time and cap-time audit pool" (§2.3 S3), and Change 13 (f) lists a FAIL-path disagreement "in the Escalation (c)". Change 13 (b) removes every in-run audit on the FAIL path (§2.3 S6-S7 "FAIL candidate: no in-run audit"), and the offline sample runs after both replicates, after the review 3 Escalation is written. So no audit exists at the cap to feed the pool, and Escalation (c) ("contested demotions the auditor judged real") can only be empty at review 3. Returned to the orchestrator: either define a cap-time audit (for example, the PASS-time auditor also runs at a review 3 FAIL over the frozen rejected ids), or restate 2 (e) and 13 (f) as offline-only. The executor applied the plan text as written and did not choose.
- Contradictions found and fixed during the merge (consequential wording, logged under their changes): §2.6 grader-class row vs Change 11; §2.7 severity row vs Changes 4 and 17; §3.2 "no severity words before `status`" vs Change 4; §6.2 risk 4 "all but 3 per review" vs Change 13; §6.2 risk 8 "F1" vs Change 20.

## Summary
- Total changes planned: 27
- Successfully applied: 27
- Failed: 0
- Skipped: 0
- Post-merge validation: FAIL (one plan-inherited contradiction: the cap-time audit pool and Escalation (c) have no FAIL-path audit to feed them; all other checks pass)
