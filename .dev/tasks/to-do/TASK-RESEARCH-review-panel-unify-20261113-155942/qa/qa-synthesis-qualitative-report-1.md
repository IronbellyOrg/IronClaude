# QA Report - Synthesis Gate, Synthesis-Coherence Lens (Partition 1 of 2)

**Topic:** Unified Review Panel investigation (E1 reflect Tier 2, E2 tasklist review-panel study at 4a22d74, E3 #346 review loop)
**Date:** 2026-11-14
**Phase:** synthesis-gate (task-qualitative family; lens: synthesis-coherence)
**Fix cycle:** N/A (review 1)
**Assigned files:** synth-01-problem-current-state.md, synth-02-target-gaps.md, synth-03-external-findings.md, synth-04-options-conflicts.md

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Repository root: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`. TASK_DIR = `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/`. `fix_authorization: false` (no file modified except this report). No `## Inherited Structural Verdict` block was supplied, so this review ran in standalone mode.

## Overall Verdict: FAIL

Six blocking findings (1 CRITICAL, 5 IMPORTANT) are open; details in "Findings". The four adversarial write-backs (C03, C05, C13, C14) were checked against their debate outputs and follow from them, and the four debates' open HIGH invariants are stated as open in the text (not defects, per executor note 2). The FAIL comes from the C14 recount claim (executor note 3) still being stated as measured fact in synth-01, synth-02 and synth-04, plus five other coherence defects.

## Lens results (the seven requested evaluations)

| # | Evaluation | Result | Evidence |
|---|---|---|---|
| L1 | Findings build logically: Section 2 to Sections 3-4 to Section 6 | FAIL | Chain holds for D1-D16, BL, MS, ENS rows (synth-02 4.3 counts re-derived by grep: 144 rows, Critical 15 / Important 65 / Minor 64, tracks M1 56 / M2 20 / M3 18 / M4 16 / none 34, all match). Breaks at C14: the Section 2 / Section 4 claim that Tier 2 is driven by the parsed-sparse flag (synth-01:73, synth-02 DOC-59) is carried into synth-04 as the premise of Option B, then refuted by the C14 debate inside the same section (F1, F2, F3). |
| L2 | Conclusions proportionate to evidence; weak evidence hedged | FAIL | AI-labelled cluster precision (0.84/0.95) hedged everywhere checked (synth-01:68, synth-02 D6, SC-6, synth-04 C-12). Bundle "no valid-success verdict" hedged (synth-01 2.3, synth-04 C-05, C-13, C-20). E2 non-significant panel differences hedged in synth-01:104 and the C-14 E2 row. Not proportionate: C-04 `DECIDED-BY-EVIDENCE` rests on one uncorrected p-value (F5); C-05 Option E uses a cluster_agreement figure the synthesis itself calls uninformative (F4). |
| L3 | Research-file contradictions resolved or noted | PASS with notes | synth-01 2.6 table (11 rows) and synth-02 4.1 (15 rows) resolve or flag each contradiction found; the 37-vs-38 test-file count is explicitly left open (synth-02 DOC-43, 4.1 #6). Exceptions are in F4 and minor notes M1, M3, M4. |
| L4 | Options genuinely distinct | FAIL (overall design level only) | Conflict-level options (C01-C20) are distinct. The three whole-design options in 6.X are not: synth-04 states "Option A is the first stage of Option B (B starts from A's code)" and recommends "build toward Option B through Option A" (F6). |
| L5 | Overlap matrix judges by meaning, not name | PASS with notes | 18 rows; calibration (row 7) is judged "partly" because confidence and a binary blocking decision are different questions; manifest row 13 maps E3's ledger rounds by function, not by name. Name or location based cells: row 8 "same code: yes: panel.py" while E2 bypassed it, row 18 "partly: one tests/review directory" (M6). |
| L6 | Debate results written into synth-04 follow from debate outputs | PASS | Checked each of C03, C05, C13, C14 against `adversarial/return-contract.yaml` (and `base-selection.md` for C05): winners, scores (0.917/0.880; 0.9091/0.8810; 0.9804/0.9724; 0.9256/0.9194), tiebreak counts (10-0, 6-2, 14-10, 6-4), convergence (0.86, 0.909, 0.89, 0.80), unresolved diff-point ids, and HIGH invariant lists all match; open HIGH invariants are stated as open. One C13 code claim re-read at source: `ledger.py:350-360` `defer` does set `verdict, decision = "PASS", "PASS"` when `brief_ids` empties. |
| L7 | External research used as context, never overriding code | PASS | synth-03 states the rule at lines 6 and 10 and tags every item `[E]/[A]/[S]/[2]/[V]/[U]`; synth-04 always labels web items `External context [web]` and no decision rests on them alone. Minor: M2. |

## Findings

Blocking findings (CRITICAL and IMPORTANT):

| # | Severity | Synth file | Section | Finding | Proposed remedy |
|---|---|---|---|---|---|
| F1 | CRITICAL | synth-04 | 6 C-14 (lines 926, 941, 944, 952, 954) and C-10 evidence (line 691) | The older claim is stated as measured fact while the same section's debate write-back (line 956) says it is overstated. Line 926 (Option B pros): "Acts on the measured driver of Tier 2 spend (35 of 39 parsed-sparse)". Line 941 (Option C cons): "Pays Tier 2 on 38 of 39 plans for an input-format reason, not plan risk". Line 944 (Evidence): "Tier 2 cost is almost always paid and mostly for an input-format reason: ... 35 by the parsed-sparse pre-filter ... with the same conclusion". Line 952 (Status): "the cost side favours fixing the rubric first". Line 691 (C-10 Evidence): "Parsed-sparse escalation sends nearly every workflow plan to Tier 2". Line 956 then reports the debate recount: flag set in 35 of 39 non-shadow runs, "decisive in 0 for certain, at most 1", and calls A's "35 of 39 escalate because of the flag" and B's "1 certain, at most 5" both overstated (matches `panel-size-cost/adversarial/return-contract.yaml` `orchestrator_notes.escalation_figure_after_check`). I also recounted the 39 files `.dev/reflect/pre-*/artifacts/tier_decision.yaml` (non-shadow) by shell: `selected_tier` 2 in 38 and 1 in 1; `coverage_degraded` starts with `parsed-sparse` in 35 (34 of the 38 Tier 2 runs, plus the one Tier 1 run). The premise of Option B ("fix the rubric first" cuts Tier 2 spend) is therefore not supported, yet it remains the stated reason for the recommended resolution. synth-05 line 284 already lists this sentence as "synth-04 C-14 Option B pros ... superseded ... not carried as a current fact", so synth-04 is the stale file. | Rewrite lines 926, 941, 944, 952 and 691 to say: flag set in 35 of 39 runs (34 of 38 Tier 2 runs), decisive in at most 1; the flag is not shown to be the driver; the cost lever of Option B is unproven. Make the C-14 recommended resolution lead with what the debate actually supports (A-min as owner-gated D-1, H-A measurement, Phase 1 conditional) and drop "cost side favours fixing the rubric first" from the Status. |
| F2 | IMPORTANT | synth-01 | 2.1 "Current measurements" table, row "Tier 2 is the typical path" (line 73) | States "38 of 39 non-shadow `pre-*` runs selected tier 2; 35 of them through the parsed-sparse pre-filter" with strength "measured census". Two defects: the count is wrong (34 of the 38 Tier 2 runs carry the flag; 35 is the count over all 39 runs, one Tier 1 run included, per my shell recount), and "through the pre-filter" presents the flag as the route Tier 2 was selected by, which the C14 recount refutes (decisive in at most 1). | Replace with: "38 of 39 selected Tier 2; the parsed-sparse flag was set in 35 of 39 (34 of 38 Tier 2 runs) and was decisive in at most 1 (C14 recount); flag set is not the reason Tier 2 was chosen." |
| F3 | IMPORTANT | synth-02 | 4 gap table, DOC-59 (line 245) | "Superseded by the 2026-11-13 recount: 38 of 39, 35 (same conclusion). Use 38 of 39 and 35." The recount did not keep the conclusion: synth-06 V-673 and V-316 (same corpus) say the "driven by the flag" claim is not used, and synth-05 line 284 says the same. A reader who follows DOC-59 re-imports the refuted claim. | Replace "(same conclusion)" with "(count changed; the 'driven by the flag' conclusion is withdrawn: flag set in 35 of 39, decisive in at most 1)". |
| F4 | IMPORTANT | synth-04 | 6 C-05 Option E cons (line 368) and Evidence (line 375); also C-11 count in line 754 | Uses "`cluster_agreement` 1.0 in 10 of 11" and "convergence 1.0 in 9 of 14 ... equal to `cluster_agreement` in several, so it carried no information beyond the script" to argue the debate adds nothing. The synthesis itself (synth-01 line 72, synth-02 DOC-19 and 4.1 #10, from GQ C-05) says `cluster_agreement` 1.000 is mostly the no-blocking-cluster branch (`cluster.py:407-408`): 11 of 14 runs have no blocking cluster, two are null, one (shadow09) is 0.9328. If the cluster number is a degenerate 1.0, equality with convergence 1.0 shows nothing about debate versus script. The "10 of 11" and the "11 of 14 / 2 null / 1 real" figures are never reconciled. C-11 (line 754) words it correctly ("the data cannot show the debate adds information ... nor that the script is as good"); C-05 does not. | In C-05 Option E cons and Evidence, restate as "uninformative either way (cluster_agreement is mostly the no-blocking-cluster default)" and cite the corrected population from DOC-19; reconcile or drop "10 of 11". |
| F5 | IMPORTANT | synth-04 | 6 C-04 Status (line 286) and Recommended resolution (line 288); same evidence in synth-02 D11 | C-04 is labelled `DECIDED-BY-EVIDENCE`, and the case for "intended replicas" rests on E2's one surviving doubling effect: second luna, control found +0.83, Welch p 0.004, permutation p 0.048, n=4-6, baseline all zeros. synth-01 line 94 records that the study ran 28 uncorrected p-values, and E2's own text says only "these survive". At 28 tests one or two p below 0.05 are expected by chance, and the p 0.048 value is the one the replica feature leans on. synth-04's own evidence rule (line 7) says doc-sourced E2 numbers are "supporting evidence only, never the sole basis of a decision". The silent re-admission removal is correctly code-verified (D11); the replica capability is not. | Split the C-04 decision: "remove silent re-admission" stays DECIDED-BY-EVIDENCE (code, reproduced run); "declared replicas" is a design option, stated as resting on one uncorrected p-value (0.048 of 28 tests) pending replication. Carry the multiplicity caveat from synth-01 into C-04 and synth-02 D11. |
| F6 | IMPORTANT | synth-04 | 6.X "Assessment summary" (line 1439) and Option B text (lines 1404-1416) | The summary says "no part of Option B depends on the open conflicts except which decider (C05) and which ledger rounds model (C13) the registry carries". That is contradicted inside the section: Option B contains "launch adapters per environment", while C-03 (open, O-2) resolves to anthropic-only class launch and explicitly does not adopt gateway launch entries; C-09 says "the adapter default per consumer follows the C03 decision"; the default reviewer count in the templates the registry carries depends on C-14 (D-1 open). The same summary says "Option A is the first stage of Option B", so options A and B are nested stages of one approach, leaving two real alternatives (unify on v2 versus adapters only), not three. | Correct the dependency sentence to list C03, C05, C13 and C14 (and O-2); state in the 6.X heading that A and B are stages of one unification path and C is the only alternative, or add a distinct whole-design alternative (for example a master-ledger-as-core option from E3) so the comparison table compares real alternatives. |

Minor notes (never fail the review; not rechecked):

| # | Severity | Synth file | Section | Note | Proposed remedy |
|---|---|---|---|---|---|
| M1 | MINOR | synth-02 vs synth-03 | 3.1 row "Severity interchange" vs 5.2.1 | synth-02 says SARIF `level` has "three buckets (error, warning, note)"; synth-03 (same source) says four values including `none` for non-fail kinds. | Say "three buckets for fail results (plus `none`)". |
| M2 | MINOR | synth-02, synth-04 | 3.1 row "Union vs weighted voting"; C-05 evidence line 376 | The 82.7% recall / 85.0% FPR / 37.7% / 35.3% figures are quoted without the synth-03 tag "[S] search snippet; exact numbers MEDIUM confidence until extracted". | Carry the snippet-only hedge. |
| M3 | MINOR | synth-01, 02, 04 | 2.5; ENS rows; C-09, C-11, C-17 | `ensemble.py` provenance tag differs: "E1-adjacent master baseline" (synth-01), "[E1]" (synth-02), E3 column (synth-04). It predates all three efforts (PRs #213 #214 #220 #329). | Use one label such as "master baseline (none of E1-E3)". |
| M4 | MINOR | synth-01 | 2.2 (line 86) | "about 106 scored reviewer runs" and "156 of 665 valid-era runs" use different units: R11 line 143 says 106 are panel runs (76 source-era + 30 pre-source), 665 are individual reviewer runs. | Label 106 as "panel runs". |
| M5 | MINOR | synth-01, synth-04 | 2.1 line 71; C-20 | The EV-1 comparison "8 of 13 = 0.615 versus legacy 3 of 39 = 0.077" omits the OPEN-02 caveat (legacy side may not treat unparseable contracts as failures; unchecked). The Stage 2 FAIL itself stands (13 of 20 runs). | Cross-reference OPEN-02. |
| M6 | MINOR | synth-01 | 2.6 matrix rows 8 and 18, "Reading the matrix" | "Same code? yes: panel.py" (E2 bypassed it) and "partly: one tests/review directory" are location or name based. | Mark E2 "no" for row 8 and row 18 "no shared code". |
| M7 | MINOR | synth-04 | C-06 Status | `DECIDED-BY-EVIDENCE` for Option B rests on code mismatch and low cost; no evidence shows calibration adds value (association only: mean 0.80 vs 0.66; placebo warning at `confidence-calibrator.md:159`). | Say "decided on design grounds; value unmeasured". |
| M8 | MINOR | synth-04 | C-05 | Only Option A and Option D were debated (conflict-index.md); B, C, E were not, and base-selection.md:145 notes only 8 of 33 points produced a one-sided winner. The text reports the narrow margin and 3/5 vs 1/5 correctness, but not these two facts. | Add one sentence each. |
| M9 | MINOR | synth-01 | 1 (line 33) | "94 open rows, none Critical" sits beside 15 Critical rows in synth-02; synth-02 4.1 #15 explains the two scales, synth-01 does not point to it. | Add a pointer. |
| M10 | MINOR | synth-04 | C-14 Evidence (line 945), Option A pros | "no recall gain ... matches the three-reviewer ones" is read from non-significant n=4-6 results without the "underpowered" caveat used in synth-01:104. | Add the caveat. |
| M11 | MINOR | synth-01 | 1 (line 30) | "49 blocking findings lost at merge by length limits": 48 were length rejections and 1 was refs (stated correctly at line 110 and in C-02). | "48 by length limits and 1 by refs". |
| M12 | MINOR | synth-04 | 6.D rows D3, D14 | D3 recommends "at least two valid blocks for PASS" while synth-02 SC-3 calls the value an owner decision (G-20); D14 (Critical, unwired) is marked "Decided" though the listed conflicts decide design, not wiring. | Mark D3 value as provisional; mark D14 "design decided, wiring open (M3)". |

## Executor-note checks

| Note | Result | Evidence |
|---|---|---|
| (2) Debates C03, C05, C13, C14 ended `partial` with unaddressed HIGH invariants | Stated as open in the text; not counted as defects | synth-04 lines 226, 382, 891, 956 list the invariant ids, unresolved diff points and residual risks; counts match each `return-contract.yaml` (C03: 2 HIGH, 4 unresolved; C05: 11 HIGH, 3 unresolved; C13: 10 HIGH, 4 unresolved; C14: 3 HIGH, 6 unresolved). |
| (3) 35-of-39 "driven by the flag" claim | FAIL: presented as measured fact in 3 of my 4 files | F1 (synth-04, five locations), F2 (synth-01:73), F3 (synth-02 DOC-59). synth-04 line 956 and the debate output state the corrected figure, so the file contradicts itself. |
| (4) `[CONTRADICTION]` on PENDING / exit 12 in synth-05 | Not in my partition | Not assessed here. |
| (5) E2 only at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 | PASS | `git cat-file -t 4a22d742...` returns `commit`; every E2 cite in synth-01 to synth-04 uses `4a22d742` or the full sha (grep of all 7+ hex tokens in synth-01 shows no other E2 commit; synth-02 K-11 and synth-04 header restate it). E2 file:line cites I re-read at that commit (`run-reviewer.sh:51,55-58,69-71,76,87`; `final-table.py:44,48`; `judge-one.sh:21`; `COMBO-REPORT.md:291-292,298,373,501`) match the text. |

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` was supplied; standalone mode.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was provided, so nothing was skipped on reliance. I did rely on the executor's statement that all seven synthesis files exist (confirmed by `ls`, all seven present) and on the executor notes (2) to (5) as context only.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Tier-2 / parsed-sparse recount, independent of the debate script: shell count over `.dev/reflect/pre-*/artifacts/tier_decision.yaml` (excluding shadow dirs) gave 39 files, `selected_tier` 2 = 38 and 1 = 1, flag `parsed-sparse*` = 35 in total (34 of the 38 Tier 2 runs). This confirmed the debate figure and showed synth-01:73's "35 of them" is miscounted (basis of F1, F2).
- Debate write-back fidelity: read all four `return-contract.yaml` files and `who-judges-blocking/adversarial/base-selection.md:138-159`; compared score, margin, tiebreak, convergence, unresolved ids and invariant ids to synth-04 lines 226, 382, 891, 956 (L6 PASS). Grepped the C05 transcript for "fail-closed" and "add recall" (X-001, X-006 confirm synth-04's "overturned" sentence) and the C13 probe for the `defer`/empty-block invariants.
- Code claims re-read at source: `findings_v2.py:105-109,159-163`; `contract.py:376-382`; `panel.py:534-544,484-495`; `runner.py:536-546`; `ensemble.py:771-775`; `findings.py:102-119`; `ledger.py:148-158,252-259,272-275,350-360`. All match the cited behaviour.
- Count integrity of synth-02 4.2: grep over the gap-table rows reproduced 144 rows, Critical 15, Important 65, Minor 64, and tracks 56/20/18/16/34.
- E2 harness cites re-read with `git show 4a22d742:` (see executor note 5 row).
- Source of the stale claim traced: `research/11-evaluation-evidence.md:421` and `:461` ("same conclusion, newer numbers") are where the older claim entered; synth-05:284 and synth-06 V-316/V-366/V-673 already correct it, which shows synth-01, -02 and -04 are the files left behind.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (7 lens evaluations, each with tool evidence listed above; 4 PASS or PASS-with-notes, 3 FAIL).
- **Tool engagement:** Read: 26 | Grep: 16 | Glob: 0 | Bash: 8 (Read+Grep+Glob = 42, above the 7 lens items).
- Not independently re-derived (outside what could be checked here, no effect on the verdict): E2 raw `score.json` aggregates (the synthesis itself marks them doc-sourced, G-82), the remaining ~200 file:line cites in synth-02 rows beyond the spot checks above, and every web source (no external lookup was needed; web findings were read as reported by `research/web-0N-*.md`, so no Tavily or fallback calls were made).

## Recommendations

1. Fix F1 to F3 first: they are one error in three files (the refuted "driven by the flag" claim). Use the debate wording from synth-04 line 956.
2. Fix F4 (C-05 Option E cluster_agreement), F5 (C-04 replica evidence) and F6 (6.X dependency sentence and nested options).
3. Apply the minor notes only where cheap; they are not rechecked.
4. Re-run this partition review after the fixes (cycle 1 of at most 2).

## Verdict

**VERDICT: FAIL** (6 blocking findings open: F1 CRITICAL; F2, F3, F4, F5, F6 IMPORTANT. 12 minor notes.)

## QA Complete

