# QA Report: Phase 6 Source-Fidelity Verification, Content

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks
**Date:** 2026-10-24
**Task step:** 6.31 (independent content fidelity verification)
**Phase:** fidelity (content lens), after fidelity fix cycle 1 of 2
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Report under review:** `R/RESEARCH-REPORT-review-loops.md`, 1,313 lines, sha256 `a94475caee954ae9942c4b4e8d609e4fc4bfb898fa134026045c78657f18ccf2` (re-measured at the start of this step; it matches the fix log's after-hash).
**Mode:** report-only, `fix_authorization: false`. No file was edited and no Git command was run. The parent session log `dfade920-…jsonl` was not opened. The other primary logs were read only by record number.
**Templates read first:** `/config/.claude/skills/tech-research/SKILL.md:1153-1194` (fidelity prompt and checklist); `/config/.claude/skills/task/SKILL.md:466-506` (Standard QA Report Output Format).
**Known and not counted:** J1, the stale status lines at Report:5, :1238 and :1290 (they were :5, :1235 and :1287 before the 3-line growth). The user accepted them.
**User decisions applied as given:** F-05 "Keep, disclosed"; F-02 "Disclosure only" (task log entry `[2026-10-24T06:32Z]`, `R/TASK-RESEARCH-review-loops-20261023-032537.md:683`).

---

## Overall Verdict

Verdict: FAIL

The fixes correct the ten original defects as written. Checking them against primary sources turned up four new fidelity defects: 2 IMPORTANT and 2 MINOR. Fixing any of the four changes no rank or ranked cause. One previously PASS claim-to-source link regressed: P3-C11. It broke because the fixer inserted lines into case file 04, which shifted the line numbers the report cites in that file.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Governing templates read before review | PASS | tech-research SKILL `:1153-1194`; task SKILL `:466-506` |
| 2 | Report identity | PASS | `sha256sum` gives `a94475ca…7ccf2`; `wc -l` gives 1,313 |
| 3 | F-01: replay-row plan versions | PASS | Report:846 matches the case's version table (`research/01-session-ac2cd1fd.md` hash table: v1 `ebc03d45…`, v2 Session:544 `d3a12ef9…`, v3 Session:841 `cbfb606a…`) and its correction B (150 was blocked at 151; retry 163/164 applied). v3 is the version checked by the targeted review at 874 (`research/01:75-80`) |
| 4 | F-02: requested criterion quoted, substitution disclosed, not presented as pre-authorized | PASS for the quotations and the honesty of the disclosure; FAIL on rule attribution (N-04) | `BUILD-REQUEST.md:12` ("ranked most to least likely") and `:34` are quoted exactly at Report:88 and :716. Report:88 says "No user authorization for that substitution was on record when the ranking was made", then gives the 06:32Z acceptance, which matches task log `:683` |
| 5 | F-03: who decided the Phase 5 review skip | PASS | Report:10 matches task log `:645` (user said "keep the phase 5 review if valuable"; the parent judged it duplicative) and `phase-outputs/plans/synthesis-gate-decision.md:65` |
| 6 | F-04: coverage pointers and the no-review v4 edit | PASS for the pointers; FAIL on the agency wording at 858 (N-03) | Option A Support (Report:523, validation after fetch, over-credited matrix), Gap row 1 (:343), Option B Risk (:559, blocked 150/151) and 2.7 (:291) exist as claimed. Orca records 885 and 889 match (raw text read) |
| 7 | F-05: disclosure of the case-03 Coder Git reads | PASS for the case-03 content; FAIL on completeness (N-01) | `research/03-session-6f744b87.md:121-131` ("I independently read both Git blobs"); the tree comparison at `:212-250`. Report:8, :324 and :904 say "no authorization on record" and only then give the 2026-10-24 acceptance, so they do not read as pre-authorized |
| 8 | F-06: same reviewer | PASS | `research/screening-recovery-source.txt:76` ("Same reviewer returns `compliant`"); the case table rows for 204, 222 and 234 |
| 9 | F-07: the 16/2 count survived debate | PASS for the wording; FAIL on the marker's evidence links (N-02) | CI `REPORT.md:21` ("fixes 16 of the 18 cycle-0 findings in full and the other 2 in part"); `round2-v1.md` R1-3 concession (boundary file "not an M-10 requirement … optional hardening"), "V2's 'not_ready' is the correct label", and the X-001 row. Case 04 (now `:148`): reviewer 1 conceded in the second debate |
| 10 | F-08: monitor skill-load time | PASS | Monitor log timestamps: record 14 19:29:17.282Z; 40 19:29:22.409Z; 42 19:29:22.708Z; 58 19:29:28.357Z |
| 11 | F-09: historical `ledger.md` bytes | PASS | Re-run here: record 874 (20:34:06.655Z) holds the installed `ledger.md` at startLine 1, numLines 243, totalLines 243, content sha256 `bd66451d93910c97aac0b20a4d1c2f35b0452c96cbda24567cb731f09ceddeb8`. A diff against today's installed copy differs only at line 3 (the staging sentence). The "timing evidence" label is kept (Report:580, :582) |
| 12 | F-10: provenance class of the scope files | PASS | `scope-rules.md:11` ("Main additionally directly read the four sources"); rule-map record 79 opens with a status table, not the `# Research: Review and retry rule map` title; `scope-02/04/05.md:8,11` read "No producer-written report is claimed" and point to their captures |
| 13 | Ranked causes and the non-consensus order V1 > V3 > V2 > V5 > V4 | PASS | `ADV/debate-transcript.md:477-484`, as read: V3 above V2 3 of 5 and V4 above V5 3 of 5. Report 7.1 (:677-681) and 7.2 (:687-701) agree: V1 first 5 of 5; V3 > V2 3 of 5; V4 > V5 3 of 5, with the displayed V5 > V4 on the 2-of-5 side (:701, :706). Report:718 says writing scores are not likelihood (V1 had the lowest writing score) |
| 14 | Uncertainty statements | PASS | The installer's identity is still unknown (Report:229, :744, :947); the final CI partial pair is still unrecoverable (:254); the Coder-read tool is not recorded (:8); the link to the 20:29:54Z install stays timing evidence (:580) |
| 15 | Historical versus current-rule distinctions | PASS | 2.3 and 7.5 are unchanged; Report:580 separates the loaded bytes from the current copy and dates the line-3 change against 2.3's mtime row (:208) |
| 16 | Controls and their limits | PASS | Section 2.2 controls (:174-183), the Opposition rows (:524, :551, :605, :629) and the 7.7 control placements (:780-787) all keep their limits. No patch touched them |
| 17 | No new unsupported generalization in the 25 patched regions | PASS, except N-01, N-03 and N-04 | All patched regions were read in context (:8, :10, :88-90, :165, :167, :168, :254, :271, :274, :324, :349, :382, :580, :614, :716, :768, :846, :904, :1240, :1245-1246, :1259) |
| 18 | Matching changes in synth-01, synth-02 and synth-04 | PASS | Old wording ("intermediate “16 fixed", "second reviewer had") found 0 times in all three; the requested-criterion text appears in synth-01 and synth-04; the marker is in synth-01 and in `gaps-and-questions.md:37` |
| 19 | Regression check of the cycle-0 PASS set | FAIL | P3-C11 regressed through N-02. The other identities listed under PASS/FAIL set history still hold |
| 20 | Search for other Phase 2 Git object reads (honesty of "two disclosed sets") | FAIL | Found an undisclosed case-06 tree read: `research/06-session-0690ee9f.md:94,292-293` (N-01). Cases 02, 04 and 05 mention Git only as subject matter |

## Summary

- Checks passed: 13 of 20. Failed: 7 (items 4, 6, 7, 9, 17, 19 and 20). Item 17 is not a separate defect; it records where N-01, N-03 and N-04 sit.
- Issues: **4 (CRITICAL 0, IMPORTANT 2, MINOR 2)**. Issues fixed in place: 0 (report-only).
- Rank impact: no required fix changes a rank, the displayed order or a pair tally. The only rank-relevant choice is under N-01: whether to keep the case-06 evidence. That is a user decision, like F-05.
- Regression: P3-C11 (PASS at cycle 0, FAIL now), caused by N-02.
- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 20 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 10, all read-only: two batched inspection scripts in a private `/tmp` directory that was removed afterward, one `uv run --no-project python` reader for record 874, and single `sed`/`grep`/`wc`/`sha256sum` calls. No web research was done, so Tavily was not needed.

## Issues Found

| ID | Severity | Location path:line | Issue | Primary evidence | Required fix |
|---|---|---|---|---|---|
| N-01 | IMPORTANT | `R/RESEARCH-REPORT-review-loops.md:904` ("None was performed here, except two disclosed sets of read-only Git reads"); `:8` and `:324` (only two departures disclosed). Dependent claims: `:170`, `:346`, `:604` | **Inaccurate denial, the same class as F-05.** During Phase 2, the case-06 analyst also read Git objects: "I independently confirmed its historical content using preserved Git tree `7ac64e6a91f624362b19daf46ea9544ad8a4edcd`, rather than today's changed README", and "Checked historical source through preserved Git objects … performed read-only … Git object inspection". The report relies on that read for the claim that the temporary lint proof became a README separator citation (:604 Option D Support, :346 Gap row, :170). No authorization is on record. The 06:32Z user decision was asked on F-05, which named only the case-03 objects (`qa/qa-fidelity-consolidated-findings.md:80`), so it cannot be assumed to cover this read. | `research/06-session-0690ee9f.md:94`, `:292-293`; task log `:683`; `grep` for `7ac64e6a` finds it nowhere in the report, the deck, the synthesis files or any fidelity QA record | At :8, :324 and :904, disclose a third departure: the case-06 analyst read preserved Git tree `7ac64e6a91f624362b19daf46ea9544ad8a4edcd` and other "preserved Git objects" during Phase 2 to confirm README line 161's historical content (`research/06-session-0690ee9f.md:94,292-293`). Say these were read-only, with no authorization on record, and that the source names neither the tool nor the repository at those lines. Change "two disclosed sets" to three. Do not say the 06:32Z acceptance covers this read: keeping or removing it is a user decision. Disclosure has no rank impact. Removing the evidence would weaken the initial-credential support for V4 (Option D), so it would need the same handling as F-05 decision 1 |
| N-02 | IMPORTANT | `R/research/04-session-43582de1.md` (lines 119-121 and 298-299 inserted at Step 6.29). The cited anchors broke at `R/RESEARCH-REPORT-review-loops.md:254` (`:130`, `:143`, `:145`, `:294`, `:361`), `:349` (`:240`, `:244`, `:361`), `:848` (`:470-471`), `:951` (`:593`), and the ranges at `:151`, `:168`, `:281`. Also `R/gaps-and-questions.md:37` and the matching rows in synth-01 and synth-02 | **The case-file insertions shifted every case-04 anchor after line 118: by +3 lines, and by +5 after line 297.** The case file grew from 610 to 615 lines. As a result, the new contradiction row's evidence "M-05 partial at `:130`, M-18 partly corrected at `:143`" now points at M-02 "Addressed in plan text" and M-15 "Addressed as specified". `:145` is M-17. `:294` is a path line. `:361`, `:470` and `:593` are blank, and `:471` is a table header. Report:848 "SHA-256 values … still match `research/04-session-43582de1.md:470-471`" now cites the wrong lines; the hashes are at `:475-476`. The fix log's "addition-only … no existing case text is changed" (`qa/qa-fidelity-fix-log.md:43,346`) is literally true but missed this side effect | `wc -l` gives 615. Current anchors: M-05 `:133`, M-18 `:146`, reviewer-1 concession `:148`, verdict-counts sentence `:297`, "The final report repeats" `:366`, hashes `:475-476`, source frames `:598`, every-note-applied claim `:243`, "ready with notes" `:247` | Revert the two Step 6.29 insertions in `research/04-session-43582de1.md` (current lines 119-121 and 298-299), so the file returns to its pre-fix sha256 `661d0604423bc9f68b38f1cf9e752c43b70968cf8d5701d928cf167a66cd0de7`. Keep the `[CONTRADICTION: …]` marker in Report 2.5 and `gaps-and-questions.md:37`, the fallback the consolidation allowed (`qa/qa-fidelity-consolidated-findings.md:72`). Record the reversal in the cycle-2 fix log. Every existing citation is then correct again without other edits. The alternative, renumbering every case-04 citation in the report, synthesis, gap register, deck and QA records, touches far more files and is not recommended. No rank impact |
| N-03 | MINOR | `R/RESEARCH-REPORT-review-loops.md:165` ("narrowed at the user's instruction to two items (raw 858)"; the transition list has no 856); `:271` ("the user-directed two-item targeted review (raw 858)"); the same text in synth-01 (patches S1-02 and S1-07) | **The F-04 fix introduced a distortion of who decided.** The case says the orchestrator proposed the narrowing and the user accepted it: "At Session:821 and :856, the orchestrator argued for reviewing only the two blocking fixes, citing the repeated cost … The user explicitly accepted that narrowed review at :858". Raw 856 ends "Recommended action: have one fresh reviewer check only N-01 and N-12 against plan v3 … instead of a third full review". Raw 858 is the user typing that sentence back verbatim. The report describes the parallel 885/889 pair as a recommendation followed by an authorization, but presents 858 as user-originated | `research/01-session-ac2cd1fd.md:77-78,305`; Orca log records 856 and 858 (858 at 2026-10-22T15:54:59.545Z) | Report:165: "narrowed to two items on the orchestrator's recommendation (raw 821, 856), which the user adopted at raw 858", and add "→ recommendation 856 → user authorization 858" to the transition list. Report:271: replace "user-directed" with "orchestrator-recommended, user-authorized (raw 856, 858)". Apply the same wording in synth-01. No rank impact |
| N-04 | MINOR | `R/RESEARCH-REPORT-review-loops.md:88` ("It therefore promoted rule A-001, under which explanatory reach across contexts counts first and direct evidence … second (`diff-analysis.md:64,69`; Section 6.0)"); the same sentence in synth-01 (patch S1-01) | **The F-02 disclosure attributes the content of the rule to the wrong source.** The diff analysis promoted A-001 only as an OPEN shared assumption: "OPEN: each advocate must ACCEPT, REJECT or QUALIFY and give a comparison rule". Its impact note warns: "Strong narrow evidence for two unchanged blockers is not automatically less likely than broader evidence". The reach-first rule came from the advocates in Round 1 (`debate-transcript.md:47,65,143,182,196`) and Round 2 (`:277,316,356,397,438`). In Round 2, V2-V5 described it as "not population likelihood" or "not measured likelihood". As written, the disclosure the user accepted credits the diff analysis with a criterion it did not set, and leaves out its caution | `reviews/adversarial/adversarial/diff-analysis.md:64,69`; `debate-transcript.md` lines above | Rewrite as follows: the diff analysis promoted A-001 as an open point requiring a shared comparison rule, noting that narrow evidence is "not automatically less likely" (`:64,69`); in Rounds 1-2 the advocates answered with explanatory reach first and direct transition evidence second, and V2-V5 described it as not likelihood (`debate-transcript.md:47,65,143,182,196,277,316,356,397,438`; Section 6.0). Make the same change in synth-01. Report:716 ("The debate adopted A-001's explanatory-reach rule") is already accurate. No rank impact |

## PASS/FAIL set history

**Cycle 0** (`qa/qa-fidelity-consolidated-findings.md:195-208`): |F_0| = 10 (F-01 to F-10). 84 PASS identities frozen.

**Cycle 1, content lens (this report):**

| Cycle-0 item | Cycle-1 status | Basis |
|---|---|---|
| F-01 | PASS | Item 3 |
| F-02 | PASS (disclosure present and honest) | Item 4; the new attribution defect is N-04 |
| F-03 | PASS | Item 5 |
| F-04 | PASS (pointers) | Item 6; the new agency defect is N-03 |
| F-05 | FAIL at the same sentence (Report:904): the case-03 reads are now disclosed, but the sentence is still an inaccurate denial | N-01 |
| F-06 | PASS | Item 8 |
| F-07 | FAIL as applied: the wording is correct, but the marker row's case-04 citations are broken | N-02 |
| F-08 | PASS | Item 10 |
| F-09 | PASS | Item 11 (hash re-run) |
| F-10 | PASS | Item 12 |

- **F_1 (deduplicated): {N-01 (same sentence as F-05), N-02 (covers F-07's marker evidence), N-03, N-04}. |F_1| = 4**, below |F_0| = 10.
- **Regression:** P3-C11 (Q7 post-window ledger; plan hashes) was PASS at cycle 0 and is FAIL now. The report's links for it (Report:848 `:470-471`, Report:951 `:593`) now land on blank lines and a table header. The plan hashes themselves still match at case 04 `:475-476`. This is a regression under Step 6.32's guard and it takes precedence over the monotonicity check.
- **Cycle-0 PASS identities re-checked directly against primary sources this cycle, all still PASS:** P1-S1 (records 856, 858, 874, 885 and 889 with their timestamps), P1-S3 (the version-hash table), P1-S7 (orders at 477-484), P1-C5 (the 946 disclosure at `research/01:86`), P2-V8 (204/222/234 same reviewer), P3-C4 (debate changed the verdict; round2-v1 concessions), P3-C5 (`REPORT.md:21-25`: 5 medium, 11 low, 0 high), P4-H6 (records 874/884 after 20:29:54Z; 2.3 unchanged), XS-R1 (Report:253, 13/3 versus 14/2).
- **Relied on, not re-checked individually:** the remaining cycle-0 PASS identities. Basis: they sit in report regions that no patch touched (`qa/qa-fidelity-fix-log.md:344-349`, a replayed patch set), and my full read found no semantic conflict with them. The structural verifier (Step 6.30) owns the full recheck.

## Actions Taken

None. Report-only; no file was edited.

## Recommendations

- Step 6.32: record FAIL at fidelity cycle 1 and the P3-C11 regression. Halt or continue according to the regression guard's rule. If cycle 2 is allowed, one serialized fixer should apply N-01 to N-04, with N-02 first (revert the case-04 insertions), because it restores the citations N-01's fix may also rely on.
- N-01 needs a user decision, as F-05 did. The disclosure is required either way. Whether to keep the case-06 Git-tree evidence is the user's choice.
- After the fixes, re-verify the case-04 hash `661d0604…` and re-check P3-C11 and the 2.5 contradiction row against case 04 `:130`, `:143`, `:145`, `:294`, `:361`.

## Self-Audit

**(a) Reliance list (cycle-0 PASS items not re-checked structurally):**
- Relied on the 84 cycle-0 PASS identities in unpatched regions, except the nine re-checked above. The basis is the fix log's patch replay and parent application record (`qa/qa-fidelity-fix-log.md:363-373`).

**(b) Independent semantic checks (my own tool work, beyond what earlier reviewers did):**
- Recomputed the record-874 `ledger.md` hash and diff with a read-only Python reader, matching `bd66451d…` with a line-3-only difference.
- Read Orca raw records 856, 858, 885 and 889; this found N-03.
- Searched all six case files for analyst Git reads; this found the case-06 tree read (N-01), which none of the five cycle-0 reviews found.
- Read the case-04 anchors after the patch (`wc -l` 615; `sed` of the cited lines); this found N-02 and the P3-C11 regression.
- Checked A-001's origin in `diff-analysis.md:64,69` against the debate transcript's A-001 responses; this found N-04.

## QA Complete

**Verdict: FAIL.** The ten cycle-0 defects are corrected as written. The fix cycle introduced four new fidelity defects (2 IMPORTANT, 2 MINOR) and one regression (P3-C11). None of them changes the ranking V1 > V3 > V2 > V5 > V4 or its tallies.

| Status | Result |
|---|---|
| DONE | Verified F-01 to F-10 against primary records, including a re-run of the record-874 hash (`bd66451d…`) and the monitor timestamps. |
| DONE | Found N-01: an undisclosed Phase 2 Git-tree read by the case-06 analyst (`research/06-session-0690ee9f.md:94,292-293`) contradicts "two disclosed sets" at Report:904. |
| DONE | Found N-02: the case-04 erratum insertions shifted the cited lines, breaking the 2.5 contradiction evidence and regressing P3-C11. Also found N-03 (who narrowed the review at 858) and N-04 (where rule A-001's content came from). |
| NEXT | Step 6.32: record FAIL and the P3-C11 regression, then apply the regression-guard rule. |
| NEXT | User decision on N-01: keep or remove the case-06 Git-tree evidence (disclosure is required either way). |