# QA Report: Phase 5 Synthesis Gate, Content Verification (fix cycle 1)

**Topic:** unified Review Panel investigation, synthesis-gate fixes
**Date:** 2026-11-14
**Phase:** synthesis-gate (verification, qualitative)
**Fix cycle:** 1
**Fix authorization:** false (report only)

**Inputs read:** `qa/qa-consolidated-findings-phase5.md` (25 blocking findings P5-B1 to P5-B25), `qa/qa-fix-log-phase5.md` (25 rows, all "fixed"), all seven `synthesis/synth-*.md`, and the sources they rest on: `reviews/adversarial/panel-size-cost/proposal-merged.md` and `adversarial/return-contract.yaml`, `reviews/adversarial/ledger-model/adversarial/invariant-probe.md` and `proposal-merged.md`, `reviews/adversarial/who-judges-blocking/proposal-merged.md`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md` headings, `tests/cli/reflect/test_shadow_skill_contract.py`, `research/05` and `research/08`.

## Overall Verdict: FAIL

21 of the 25 fixes hold in substance. Four are incomplete: the defect a finding named is still present in a place the fix did not reach (P5-B9, P5-B10, P5-B14, P5-B23). They are 4 IMPORTANT findings, 0 CRITICAL, listed under "Issues Found". All four are small edits. No debate winner was overturned, the four debates still read `partial`, Section 8 is still not a roadmap, and no `/sc:workflow` use was added.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Each fixed finding resolved in substance, not only wording | FAIL | 21 of 25 resolved (table "Per-finding result" below). P5-B9, P5-B10, P5-B14, P5-B23 resolved at the named location only: Issues 1 to 4. |
| b | Synthesis still builds logically from current state to conflicts to architecture to migration plan | PASS | synth-01 :73 now gives counts only; synth-04 C-14 (:897-:956), synth-05 Rationale 6 (:31) and C-14 row (:51), synth-06 M2-07 (:767) and synth-07 Q-47 to Q-50 tell one story. Section 9.5 rows resolve to Section 7 and 8 items. The one cross-file break in the chain is Issue 2. |
| c | Conclusions proportionate to evidence; debate winners not overturned | PASS | C03 winner A, C05 winner B (Option D), C13 winner B narrowly, C14 winner B by tiebreaker are unchanged in the synth-04 index (:17, :19, :27, :28), its four Adversarial result blocks (C-05 :382, C-14 :956), synth-05 risk table (:63-:66) and synth-07 debate table (:323-:326). The C14 "fix the rubric first" wording is dropped because the debate's own merged proposal drops it (proposal-merged.md :38, :48, :346). |
| d | Section 8 still a value-capture and migration plan, not a roadmap | PASS | synth-06 :9, :725 (step ids carry no order, date or sprint), :952 (branch options commit to no order). A search of synth-06 for sprint, week, milestone, ETA finds only those disclaimers; the `sc:workflow` hits describe the existing skill as a consumer or restate the scope rule. |
| 1 | C-14 wording in synth-04, synth-05 Rationale 6 and C-14 row, synth-06 M2-07 and V-366/V-405/V-518/V-557 agrees with the merged C14 proposal and the recount | PASS | Pre-filter unchanged unless the Step A keys show it decisive (CI-1): synth-04 :954, synth-05 :31 and :51, synth-06 :767, :396, :548, :587 against proposal-merged.md :38, :48, :346, :350. D-1 owner-gated (proposal :226-:228). Step A key names in M2-07 and synth-05 :31 equal proposal-merged.md :83-:89 exactly; check script name equals :99; the CI-1 trigger "at least three runs" equals :350; the three pinned arms equal :107. Recount (flag set 35 of 39, 34 of 38 Tier 2 runs, decisive 0 for certain and at most 1, 29 of 34 with row 4, 5 or 6) equals `return-contract.yaml` `escalation_figure_after_check`. A search of synth-01..07 for `driven by`, `fix the rubric`, `input format`, `cost lever`, `37 of 38`, `37/38`: every remaining hit is recount wording, a quote marked superseded, or a source claim in a row whose Reason cell carries the correction. |
| 2 | synth-07 Section 9 states the open decisions of the four partial debates and no longer shows as open what Sections 6 to 8 decide | PASS (note N-6) | Section 9.5 (:242-:258): Q-47 D-1, Q-48 task-builder POST gate, Q-49 tripwire numbers, Q-50 H-A owner and count-rule parameters, Q-51 C05 replay threshold and owner decisions, Q-52 C13 OD-1 to OD-11 incl. OD-6 and OD-8, Q-53 C03 flip shape and the undebated INV-009 engine-mode split, Q-54 verdict-vocabulary `[CONTRADICTION]`, Q-55 brainstorm hand-off, Q-56 EV-1 residual, Q-57 HIGH invariants. OD names and numbers equal `ledger-model/proposal-merged.md` :614-:624; owner-decision numbers 1 to 8 equal `panel-size-cost/proposal-merged.md` :519-:526; D-1 conditions 1 to 8 equal :240-:247. The 9.1 index lists Q-45 to Q-57 once each (:114-:126). Q-13, Q-16, Q-17, Q-19, Q-20, Q-22, Q-23 are relabelled "decided in synth-04 C-NN, owner confirmation only" with the residual open part; Q-30 is marked partly decided by M2-01. |
| 3 | C-04 split (silent re-admission removal decided, declared replicas a design option) carried consistently into synth-02 D11, synth-05 and synth-06 | FAIL | Carried in synth-04 C-04 Status (:286) and resolution (:288), synth-02 D11 (:119), synth-05 :41 and :149, synth-06 M1-09 (:742) and V-497 (:527), synth-07 Q-16 (:32). Not carried in the synth-04 index row C04 (:18) and synth-06 V-033, V-075, V-143, V-198: Issue 1. |
| 4 | No debate winner overturned | PASS | See check c. |
| 5 | Four debates still `partial` with HIGH invariants open | PASS | synth-04 index (:17, :19, :27, :28), synth-05 :59-:66 (2, 11, 10, 3 HIGH), synth-06 :11, synth-07 :319, :323-:326 and Q-57; the counts equal the return contracts and merged proposals read above. |
| 6 | Section 8 is a value-capture and migration plan; report free of `/sc:workflow` use | PASS | See check d; synth-07 :5 and synth-06 :3, :9 state the scope. |

## Per-finding result (P5-B1 to P5-B25)

| ID | Result | Evidence |
|----|--------|----------|
| P5-B1 | resolved | synth-04 :897, :917, :926, :941, :944, :952, :954, :956 carry the recount wording; "measured driver", "input-format reason" and "same conclusion" are gone; synth-05 :292 lists the corrected sentences. |
| P5-B2 | resolved | synth-04 :691 reads 38 of 39 selected Tier 2, flag set in 35 of 39, "not shown to be the cause". |
| P5-B3 | resolved | synth-01 :73 gives counts only; Strength cell "measured census of counts; cause not established". |
| P5-B4 | resolved | synth-02 :240 (DOC-59) and :273 (row 16 added to 4.1). |
| P5-B5 | resolved | synth-03 :168, :205, :215 equal research/05 :155-:157 (legacy 0 of 689, shadow 142 of 142). |
| P5-B6 | resolved | synth-02 Section 4 has no blank line between :107 and :252; a column-count scan of all seven files finds no bad row in synth-02. |
| P5-B7 | resolved | synth-01 :33 states the scale and points to synth-02 4.1 row 15 (:272). |
| P5-B8 | resolved | synth-04 :368 and :375: equality of convergence and `cluster_agreement` is "uninformative either way"; 11 of 14, two null, shadow09 0.9328 equal synth-01 :72. |
| P5-B9 | partial | Issue 1. |
| P5-B10 | partial | synth-04 :1439 is fixed (lists C03, C05, C13, C14; A and B as stages of one path, C the alternative). synth-05 :27 still carries the sentence the finding called false: Issue 2. |
| P5-B11 | resolved | synth-06 M1-07 (:740), V-118, V-431, V-432 use the probe numbering (`invariant-probe.md` :9-:18: INV-006 second revise, INV-008 spanless row). |
| P5-B12 | resolved | Re-ran `uv run pytest --collect-only -qq -p no:cacheprovider`: `tests/cli/reflect` 353; the G9 command with four `--ignore` flags 271; the four G8 files 82; 38 `test_*.py` files. G9 (:938), V-558, V-612 match; V-054 matches research/08 :307 (59 and 57). Stale residue: note N-1. |
| P5-B13 | resolved | synth-06 :435 Reason cell carries the recount. |
| P5-B14 | partial | synth-06 is clean (scan: 0 bad rows). Two rows of the same class remain in synth-01 and synth-04; the fix log records them and does not fix them: Issue 4. |
| P5-B15 | resolved | See check 2; the Inputs line (synth-07 :7) names `reviews/adversarial/`; synth-05 :295 and synth-06 :991, :1010 point to Section 9.5. |
| P5-B16 | resolved | See check 2. |
| P5-B17 | resolved | synth-07 :291-:301 has no "planned"; :317-:326 debate table; :328-:340 QA rows; :4 date. |
| P5-B18 | resolved | synth-07 :229 (D-59) and :54 (Q-38) carry the recount, no causal claim. |
| P5-B19 | resolved | See check 1. |
| P5-B20 | resolved | synth-06 :739 (M1-06) has `ledger.py:191,199,207-238` and recompute-on-re-find; G1 (:930) and G2 (:931) carry `test_review_findings.py:235-317` and `test_review_ledger.py:139-150` with replacement assertions (marked proposed). |
| P5-B21 | resolved | SKILL.md headings: 4.3a :309-:350 (so :344 and :346 are inside), section 8 :677-:717 (:714 outside), 17.6 :1920-:1963 (:1955 and :1958 outside); the C6 allowed list is 3.1, 4.3a, 5.4, 9.2 (`test_shadow_skill_contract.py` :65). M2-02 (:762), M2-09 (:769), G8 (:937) and synth-05 :260 now say so. |
| P5-B22 | resolved | synth-05 :110 (diagram), :160 and :161 split the generic core part from the named reflect module part; M2-02 keeps the writer module-side. |
| P5-B23 | partial | synth-05 :160, synth-06 M2-02 and Q-56 are correct; synth-04 C-11 Option A Pros (:720) still claims the fix: Issue 3. |
| P5-B24 | resolved | synth-06 V-415, V-416, V-420, V-426 are now "Round model (ledger), deferred to O-1" with the not-read reason (research/scope/05 :184); synth-07 Q-01 and Q-34 list the unread scripts and design docs. |
| P5-B25 | resolved | synth-06 :741 (M1-08) is shadow-only with promotion conditional on O-1 (M1-18); MS-19 and G-91 appear only in M1-18 (:751); V-155, V-421, synth-05 :158 and synth-07 Q-01 agree. |

## Summary
- Checks passed: 8 / 10 (checks a and 3 fail)
- Checks failed: 2
- Critical issues: 0
- Important issues: 4
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Synth file | Finding | Evidence |
|---|----------|-----------|---------|----------|
| 1 | IMPORTANT | synth-04 (index row C04); synth-06 (V-033, V-075, V-143, V-198) | The C-04 split (P5-B9) reached the C-04 body, synth-02 D11, synth-05, synth-06 M1-09 and V-497, and synth-07 Q-16, but not the places a reader meets first. The synth-04 conflict index row C04 still reads Status "DECIDED-BY-EVIDENCE" and resolution "Declared per-slot distinctness policy with recorded intended replicas; no silent re-admission", while the C-04 body calls the replicas a design option resting on one uncorrected p-value. synth-06 V-033 says the one-p-value effect "drives declared per-slot distinctness with `replicas` (C-04)"; V-075, V-143 and V-198 list `replicas` as part of the C-04 decision with no caveat. Required fix: index row: "Declared per-slot distinctness and no silent re-admission (decided); intended replicas an optional design option resting on one uncorrected E2 p-value"; V-033 Reason: replace "drives" with "is the only support for the optional `replicas` field, one of 28 uncorrected p-values"; add "(replicas: design option)" to V-075, V-143, V-198. | synth-04 :18 against :286 and :288; synth-06 :63, :105, :173, :228 against :527 and :742. |
| 2 | IMPORTANT | synth-05 (Rationale 2) | P5-B10 was fixed in synth-04 :1439 only. synth-05 :27 repeats the sentence the finding called false: "No part of B depends on the four open conflicts except which decider (C-05) and which round model (C-13)". synth-04 6.X (named binding for synth-05, and synth-05 :22 says "nothing below overrides it") now says B depends on C03 (launch adapters, O-2), C05, C13 and C14 (template and reviewer-count defaults, D-1). synth-05's own Rationale 6 (:31, "blocked on C-03") and risk table (:63, :66) also treat C03 and C14 as open prerequisites. Required fix: rewrite :27 to list C03, C05, C13 and C14 and say which the architecture leaves as declared hooks. | synth-05 :27 against synth-04 :1439 and synth-05 :31, :63, :66. |
| 3 | IMPORTANT | synth-04 (C-11 Option A, Pros) | P5-B23 removed "EV-1 stops being self-attested" from the How-it-works text, but the Pros cell of the same option still says Option A "fixes three unparseable shadow contracts and the self-attested EV-1". Line :712 of the same option says the writer "narrows the self-attestation but EV-1 remains an on-disk presence check" and points to Q-56; synth-05 :160 and synth-06 M2-02 say the same. A contradiction inside one option and the unsupported claim the finding asked to remove. Required fix: Pros cell: "fixes three unparseable shadow contracts and narrows the self-attested EV-1 (it stays an on-disk presence check, Q-56)". | synth-04 :720 against :712. |
| 4 | IMPORTANT | synth-01, synth-04 | Same defect class as P5-B14 (unescaped pipe characters inside code spans split a table row), found by the fix agent, recorded in the fix log as not fixed, still present: synth-01 :260 (row "Fingerprint", 11 cells under a 4-column header: `v1|section|refs`, `v2|role|path|section|refs|class`) and synth-04 :769 (C-12 position table, row E1, 8 cells under a 3-column header: `v2|role|path||refs|class`). The E1 position, its Evidence cell and the fingerprint comparison render in the wrong columns. A column-count scan of all seven files finds exactly these two bad rows. Required fix: escape each pipe inside those code spans as `\|`. | Scan: synth-01 :260 (11 vs 4), synth-04 :769 (8 vs 3); `qa-fix-log-phase5.md` :57. |

## Minor notes (not blocking, not rechecked)

| # | Where | Note |
|---|-------|------|
| N-1 | synth-02 :263 (4.1 row 6) | Still says "the 37 vs 38 file count stays unresolved"; synth-06 V-612 and G9 now resolve it (38 files, confirmed by collection). |
| N-2 | synth-02 :240 and synth-04 :897 | Call the recount "2026-11-13"; synth-04 :944 says 2026-11-14; `recount_tier_decision.py` was written 2026-11-14 00:05. |
| N-3 | synth-04 :368 | The sentence "whether that equals `cluster_agreement` shows nothing either way" is garbled; the meaning is correct. |
| N-4 | synth-06 :970 | Lists "empty block counted as valid review" among the ten HIGH invariants; the probe names it only as falsifier F5 of INV-010 (`invariant-probe.md` :18). |
| N-5 | synth-06 V-271 (:301) | "EV-1 is still self-attested ... the merge step writes the verdict file with its own `merge_method`" reads as if the writer ends the self-attestation; same point as Issue 3. |
| N-6 | synth-07 Q-31 (G-13), Q-32 (G-56, G-16) | Still phrased as owner decisions although synth-04 C-11 and C-02 decide them; compatible with "owner confirmation only" but not relabelled like the eight rows of P5-B16. |

## Actions Taken
None. Fix authorization was false; no file except this report was edited. The only command that runs repository code was `uv run pytest --collect-only -qq -p no:cacheprovider` (collection only, pytest cache disabled).

## Inherited Structural Verdict: Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was in the spawn prompt, so no rf-qa PASS was relied on; standalone mode applied. The structural parts (table integrity, test counts, section boundaries) were re-checked directly.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. The prompt carried no inherited verdict; the fix log's own "Verification performed" table (:44-:51) was treated as a claim and re-run: pytest collection counts (353, 271, 82, 38 files), the column-count scan over all seven files, the SKILL.md heading boundaries, the E2 commit hash set (16 full-hash hits, one short-hash form, all the same commit).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Fix-log claim "fixed" for P5-B10 tested against the sibling file: read synth-04 :1439 (fixed) and synth-05 :27 (same false sentence) with Read.
- Fix-log claim "removed from synth-05 and synth-04 C-11" for P5-B23 tested: Read synth-04 :701-:724 found the Pros cell at :720 still claiming the fix.
- Fix-log claim of C-04 consistency tested: Grep for `replica` across all synth files (43 hits) and a row-by-row read of synth-06 :63, :105, :173, :228, :237 against :527 and :742; read synth-04 index :18.
- Step A key names, D-1 conditions, owner-decision numbers, OD-1 to OD-11 names, INV-001 to INV-010 text compared with `proposal-merged.md` :83-:99, :226-:247, :519-:526, `ledger-model/proposal-merged.md` :614-:624 and `invariant-probe.md` :9-:18 (Read).
- C6 section claims in M2-02, M2-09, G8 and synth-05 :260 tested against `grep -nE '^#{1,4} '` of SKILL.md and `test_shadow_skill_contract.py` :65.
- Fix agent's two logged-but-unfixed rows re-found independently with a column-count scan (awk) and Read of synth-01 :255-:262 and synth-04 :764-:770.

## Recommendations
- One more fix pass (cycle 2) over four small edits: synth-04 :18, :720, :769; synth-01 :260; synth-05 :27; synth-06 :63, :105, :173, :228. After the pass, re-run the column-count scan over all seven files and a search for `replica` and "self-attested".
- Do not change any debate winner or any C-14 wording; the rest of the fixes should stay as they are.

## Confidence
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (all 10 checks were verified; two of them verified as FAIL)
- **Tool engagement (approximate counts):** Read: 27 | Grep: 12 | Glob: 0 | Bash: 16 (Read + Grep + Glob = 39 against 10 checklist items and 25 per-finding rows)
- Unchecked items: none. Unverifiable items: none. No web research was needed, so no Tavily call was made.

## QA Complete


