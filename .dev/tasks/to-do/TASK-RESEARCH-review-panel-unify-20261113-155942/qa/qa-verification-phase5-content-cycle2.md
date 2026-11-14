# QA Report: Phase 5 Synthesis Gate, Content Verification (fix cycle 2)

**Topic:** unified Review Panel investigation, synthesis-gate fixes
**Date:** 2026-11-14
**Phase:** synthesis-gate (verification, qualitative)
**Fix cycle:** 2
**Fix authorization:** false (report only)

**Inputs read:** `qa/qa-consolidated-findings-phase5.md` (`## Cycle 2`: P5-B9-r, P5-B10-r, P5-B14-r, P5-B23-r), `qa/qa-fix-log-phase5.md` (`## Cycle 2`), all seven `synthesis/synth-*.md`, the cycle-1 report `qa/qa-verification-phase5-content.md`, and the source `reviews/adversarial/panel-size-cost/proposal-merged.md` (:30-:110). The cycle-2 edits were also read as a word-level `git diff -U0 --word-diff=porcelain -- synthesis` (staged cycle-1 state against the working tree), so every changed phrase is known.

## Overall Verdict: PASS

All four cycle-2 findings are resolved in substance. No blocking defect was found. Five minor notes are listed and are not rechecked. The cycle-2 edit set is narrow: 23 changed lines in synth-01, 02, 04, 05, 06; no edit touches the C-14 text, Section 9.5 or any debate winner.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No sentence in synth-01..07 presents intended `replicas` as a decided, evidence-backed requirement | PASS | `grep -i replica` over all seven files, then every long hit expanded with `grep -o` so no "Omitted long matching line" stayed unread. Hits classified in the table "Replica hits" below. The decided part is stated as "per-slot distinctness and no silent re-admission" everywhere it is stated: synth-04 index :18, C-04 Status :286 and resolution :288, D11 row :1366; synth-05 :29, :41, :149, :232; synth-06 V-033 :63, V-075 :105, V-143 :173, V-198 :228, V-497 :527, M1-09 :742; synth-02 SC-17 :68, D11 :119, MS-06 :153; synth-07 Q-16 :32. |
| 2 | No sentence in synth-04..06 says B or the architecture depends only on decided conflicts; C03, C05, C13, C14 all named | PASS | synth-05 Rationale 2 (:27) now reads "B depends on the four debate-resolved (`partial`) conflicts ... launch adapters and class-launch grammar depend on C-03 (owner item O-2), the decider on C-05, the round model on C-13, and the template and reviewer-count defaults on C-14 (Decision D-1) ... leaves all four as declared hooks or owner-gated items". Rationale 4 (:29) heading is "Decided conflicts are built as written; the four debate-resolved ones are staged behind hooks, gates or owner items" and ends "the architecture is not independent of them (Rationale 2)". Equals synth-04 6.X (:1439), the synth-05 risk table (:63-:66) and Rationale 6 (:31, "blocked on C-03"). Searches for `only decided`, `depend only`, `does not depend`, `No part of B`, `independent of`, `regardless of`, `not blocked by`, `unblocked`, `no dependency on` find no remaining claim (synth-04 :1434 is about production callers, synth-06 :488 is the PR-review consumer; neither is the claim). |
| 3 | No sentence says the code merge writer ends EV-1's self-attestation; EV-1 stays an on-disk presence check (Q-56) | PASS | `grep -i 'self-attest\|stops being\|ends the self\|no longer self'`: synth-01 :80 and synth-02 MS-12 :159 state the current gap; synth-04 :712, :720 and synth-06 V-271 :301 say "narrows ... EV-1 stays an on-disk presence check (Q-56)"; synth-05 :160 and synth-06 M2-02 :762 say EV-1 "remains an on-disk presence check"; synth-07 Q-56 :257 asks what closes the gap. synth-06 :774 "stops being a false green" is the tasklist post gate, a different subject. All `EV-1` mentions were read; see minor note N-4 on SC-16 wording. |
| 4a | Cycle-1 fix held: C-14 wording agrees with `proposal-merged.md` and the recount | PASS | synth-04 :897, :917, :926, :941, :944, :952-:956, synth-05 :18, :31, :51, synth-06 M2-07 :767 re-read. Against proposal-merged.md: pre-filter "Unchanged ... CI-1, reopened only by the recorded keys" (:38, :48); Step A/B/C staging (:45-:47); Step A key names `matching_rows`, `calibrated_C_t1`, `S_domains_basis`, `tier_without_flag`, `sparse_flag_decisive`, `escalation_path` (:83-:88) equal the list in M2-07 and synth-05 :31; telemetry keys `reviewers_requested/resolved/source` (:89); three pinned arms (:107); cap 3 and D-1 owner-gated (:33-:34). The recount (flag set 35 of 39, 34 of 38 Tier 2, decisive 0 for certain and at most 1, 29 of 34 with row 4, 5 or 6) is identical in synth-04, 05, 06, 07. Search for `driven by`, `fix the rubric`, `37 of 38`, `37/38`, `cost lever`, `input format`: every remaining hit is a quote marked superseded, the Option B label (the debate's own name), or a Reason cell that carries the correction. The cycle-2 diff contains no C-14 edit. |
| 4b | Cycle-1 fix held: Section 9.5 (Q-47 to Q-57) | PASS | synth-07 :242-:258 re-read; all eleven rows present, each tied to a `proposal-merged.md`; Q-56 matches the corrected C-11 Option A wording. Not touched by the cycle-2 diff. |
| 4c | Cycle-1 fix held: C-04 split | PASS | The split is now carried in every place the cycle-1 report listed plus the ones the cycle-2 grep added (check 1). "28 uncorrected p-values" is backed by synth-01 :94. |
| 4d | Table integrity (P5-B14-r) | PASS | synth-01 :260 and synth-04 :769 now use `\|` inside the code spans. Re-ran an awk column-count scan (unescaped pipes only, code fences skipped, header column count against every row of each table): synth-01 to synth-07 all `bad=0`. |
| 5 | No debate winner overturned; four debates still `partial` | PASS | synth-04 index rows C03 (winner A, partial, INV-013 and INV-009), C05 (winner B by tiebreaker, 11 HIGH), C13 (winner B narrowly, 10 HIGH), C14 (winner B by tiebreaker, 3 HIGH) all still "UNDECIDED-BY-EVIDENCE, resolved by adversarial debate". synth-05 :63-:66 and synth-07 Q-57 (:258) carry the same status and counts. The D11 row (:1366) and index C04 row changed only the C-04 wording. |
| 6 | Section 8 not a roadmap; no `/sc:workflow` use | PASS | synth-06 :3, :7, :9, :725: no dates, sprints, ordering commitments, `/sc:workflow` plan; step ids carry no order. A search for sprint, week, milestone, ETA, `/sc:workflow`, `sc:implement`, `/roadmap` over all seven files finds only scope disclaimers, descriptions of an existing skill as a consumer (V-149, V-441, V-542, M3 goal :774) and quoted hand-off items. No cycle-2 edit adds sequencing. |

### Replica hits (check 1)

| Where | Reading | Verdict |
|---|---|---|
| synth-04 :18 index C04 | "Declared per-slot distinctness and no silent re-admission (decided); intended replicas an optional design option resting on one uncorrected E2 p-value" | decided part separated |
| synth-04 :262-:266 Option text; :280, :286, :288 | Option names and the C-04 body; :286 states the split and "one of 28 uncorrected p-values"; :288 "optional slot field (design option ...; no replica is enabled by default)" | caveated (note N-2) |
| synth-04 :1366 D11 row | "(decided); intended replicas recorded as an optional design option" | caveated |
| synth-04 :218, :898, :945; synth-01 :34, :100, :104, :115; synth-06 V-014, V-030, V-035, V-084, V-086, V-094, V-190 | "replicated" or "replicates" meaning repeat runs of an E2 panel, or the conflict statement "strict distinctness versus replicated same-model panels" | not the design field |
| synth-05 :29, :41, :101, :149, :232 | decided = distinctness policy and no re-admission; `replicas` = "optional", "design option, not a decided one", "no replica is enabled by default", "only if the `replicas` option is adopted" | caveated |
| synth-02 :38, :68 (SC-17), :119 (D11), :153 (MS-06) | "optional replicas", "if that design option is adopted (C-04: one uncorrected E2 p-value)", "a hypothesis for replication, not a basis for the design" | caveated |
| synth-06 V-033 :63, V-075 :105, V-124 :154, V-143 :173, V-198 :228, V-207 :237, V-490 :520, V-497 :527, V-499 :529, M1-09 :742 | each says "design option" or "optional ... C-04"; V-033 now reads "the only support for the optional `replicas` field, one of 28 uncorrected p-values" | caveated |
| synth-07 Q-16 :32 | "'declared replicas', a design option that rests on one uncorrected E2 p-value (second luna) until replicated" | caveated |

## Per-finding result (cycle 2)

| ID | Result | Evidence |
|----|--------|----------|
| P5-B9-r | resolved | Index row C04 (synth-04 :18) and V-033, V-075, V-143, V-198 carry the split. The fix agent also found and caveated the further hits the finding did not list (synth-04 D11 row :1366; synth-05 diagram :101, :149, :232; synth-02 :38, SC-17, MS-06; synth-06 V-124, V-207, V-490, V-499, M1-09). V-033 replaces "drives" with "the only support for the optional `replicas` field, one of 28 uncorrected p-values". The decided policy is not weakened: "no silent re-admission" stays decided by code evidence (D11, `panel.py:536-543`). |
| P5-B10-r | resolved | synth-05 :27 and :29 as quoted in check 2; consistent with synth-04 :1439, synth-05 :31 and the risk table. The Rationale 4 heading change is proportionate: it keeps "decided conflicts are built as written" and adds the staging of the four partial ones. |
| P5-B14-r | resolved | Check 4d. |
| P5-B23-r | resolved | synth-04 :720 Pros cell "narrows the self-attested EV-1 (it stays an on-disk presence check, Q-56)" now agrees with :712; synth-06 V-271 reads "narrows the self-attestation but EV-1 stays an on-disk presence check (Q-56)". |

## Summary
- Checks passed: 10 / 10 (items 1, 2, 3, 4a to 4d, 5, 6)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Synth file | Finding | Evidence |
|---|----------|-----------|---------|----------|
| none | n/a | n/a | No blocking finding. | Checks 1 to 6 above. |

## Minor notes (not blocking, not rechecked)

| # | Synth file | Note |
|---|-----------|------|
| N-1 | synth-02 :163 (MS-16) | "Class-disjointness forbids E2's useful second luna" calls the second luna useful with no caveat. It has no `replica` word, so the cycle-2 grep did not reach it. It states E2's finding, not a requirement, and the same file caveats it at :119 and :153; add "(one uncorrected p-value)" if the file is edited again. |
| N-2 | synth-04 :288 | "choose strict for reflect finders and allow replicas for evaluation panels" sits inside a resolution that already says "design option ... no replica is enabled by default"; read together it is an option, not a requirement. |
| N-3 | synth-06 V-231 (:261) | "recorded as a requirement of the replicated design" is ambiguous (the replicated benchmark runs, not the `replicas` field); it does not present the field as decided. |
| N-4 | synth-02 SC-16 (:67), MS-12 target (:159); synth-06 V-279, V-655 | Say EV-1 "reads a verdict file written by the merge step itself, not by the orchestrator". This names the writer, not a stronger check, and M2-02, synth-05 :160 and Q-56 carry the presence-only caveat; adding "(presence check only, Q-56)" would remove any doubt. |
| N-5 | synth-04 :1439 | Lists C04 among "Decided by evidence" without the split; synth-05 Rationale 4 carries the split for the same list. |

The cycle-1 minor notes (synth-02 :263 "37 vs 38", recount date wording, garbled sentence at synth-04 :368, C13 "empty block", Q-31 and Q-32 phrasing, `cluster_v2` range, V-399 wording) were not rechecked, as the instructions say.

## Actions Taken
None. Fix authorization was false; no file except this report was edited.

## Inherited Structural Verdict: Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was in the spawn prompt; standalone mode applied. The structural parts (table column counts) were re-run directly.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. The fix log's own claims (column scan "0 bad rows", grep results for `replica`, `self-attested`, `stops being`, "Only decided") were treated as claims and re-run.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Fix-log claim that every `replica` hit was read: re-ran the grep, expanded all eleven "Omitted long matching line" hits with `grep -o` (synth-01 :34, :115; synth-02 :119, :153; synth-04 :286, :288, :898, :1366; synth-05 :29, :149; synth-06 :742) and searched for replica synonyms that do not contain the word (`second luna`, `intended repeat`, `doubling effect`, `luna twice`, `2x luna`); this found N-1, which the fix log's search could not.
- Fix-log claim "no other sentence makes the claim" for B depends only on decided conflicts: ran a wider search (`independent of`, `regardless of`, `not blocked by`, `unblocked`, `no dependency on`) and read synth-05 :18-:66 in full against synth-04 :1439.
- Fix-log claim that EV-1 is never said to stop being self-attested: read every `EV-1` mention in the seven files (about 60 lines) and Q-56 in synth-07; found the SC-16 wording (N-4).
- Column-count claim: re-ran my own awk scan over all seven files (bad=0) and printed synth-01 :260 and synth-04 :769 to see the escapes.
- C-14 non-regression: Read synth-04 :893-:958 and `proposal-merged.md` :30-:110 and compared the key names, staging, arms and recount; read the word-level cycle-2 diff to confirm no C-14 or 9.5 line changed.
- Winners and status: printed the C03, C05, C13, C14 index rows of synth-04 and compared with synth-05 :63-:66 and synth-07 :258.

## Recommendations
- Proceed. The synthesis gate may close. Optionally fold notes N-1, N-4 into the next edit of those files; they need no fix pass.

## Confidence
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement (approximate counts):** Read: 9 | Grep: 8 | Glob: 1 | Bash: 7 (Read + Grep + Glob = 18 against 10 checklist items and 4 per-finding rows)
- Unchecked items: none. Unverifiable items: none. No web research was needed, so no Tavily call was made.

## QA Complete
