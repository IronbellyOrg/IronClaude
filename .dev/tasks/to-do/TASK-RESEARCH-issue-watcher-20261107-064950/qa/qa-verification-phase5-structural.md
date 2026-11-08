# QA Report — Phase 5 Fix-Cycle Verification (structural)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** fix-cycle (verification of Phase 5 fixes)
**Fix authorization:** false (report only)
**Status:** Complete

---

## Checks (appended incrementally)

### Check 1 - Consolidated finding #1 (codebase-context.md correction not stated): RESOLVED

- Grep `codebase-context` over `synthesis/`: one hit each in synth-01 line 242, synth-02 line 138, synth-04 line 457.
- Read `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md:21`: the "CORRECTION (2026-11-07, research alignment check)" text is present and says what the three synthesis clauses say (ci.py imports only `re`, `.classifier`, `.models`; no `subprocess`).
- synth-01 line 242 and synth-04 line 457 also cite `research/research-notes.md` lines 30 and 37; verified against my Read of research-notes.md (line 30 = ci.py EXISTING_FILES row marked CORRECTED; line 37 = GitHub-access pattern marked CORRECTED).
- NOTE (minor): synth-02 line 138 says "corrected in `research/research-notes.md` (row G2)". research-notes.md has no row G2 (the correction is the EXISTING_FILES row at line 30). "G2" is the ci.py row of synth-02's own gap table (line 111). Label ambiguity only; the fact is true.

### Check 2 - Consolidated finding #3 ("post-write re-read" layer not in the algorithm): RESOLVED

- Grep `post-write` over `synthesis/`: hits only at synth-02 lines 116, 305, 407 and synth-04 lines 108, 213, each saying the post-write re-read belongs only to routing candidate 4 and is not built. None presents it as part of the plan.
- Read synth-04 Phase 5 `run_cycle` table (lines 222-238): 13 steps; step 8 (line 233) is "Final `snapshot` ... the pre-launch re-read and the only re-read in the cycle"; nothing re-reads after the launch. Consistent with step 1.7 (line 108) and the Phase 5 intro (line 213).
- Sources for the candidate-4 qualification verified: `research/web-02-coder-claude-dispatch-and-security.md:186` (read-after-write, [PROPOSAL]); `research/01-claim-flow-and-session-launch.md:157` ("Design suggestion ... UNVERIFIED, untested", `--add-assignee @me`). SC-13 exists at synth-02 line 60 (test asserts no write-shaped `gh` call by the poller).
- synth-03 lines 291 and 324 use "pre-launch re-read"; no residual "post-write" there.

### Check 3 - Consolidated finding #4 (events read page cap fails open): RESOLVED

- synth-04 step 4.2 (line 203): `label_events` and `own_claim_comment_ids` raise `CommandError("E-GH-TRUNCATED")` when page `max_pages` is reached and still full; never return a partial list. Step 4.3 (line 204): `is_approved` only gets a complete list; the cycle maps truncation to `rejected_by="approval-unverifiable"`. `run_cycle` rows 5 and 6 (lines 230-231) carry `approval-unverifiable` / `claim-marker-unverifiable`. Step 4.5 (line 206) adds the unit test; the Phase 5 test table (line 281) adds the cycle-level "Truncated read" test; the filter 2 table row (line 177) says the cap fails closed.
- Evidence re-run by me (read-only, explicit repo path): `gh api --method GET repos/IronbellyOrg/IronClaude/issues/331/events -F per_page=100 --jq '[.[0].created_at,.[-1].created_at,length]'` returned `["2026-10-30T14:39:35Z","2026-11-07T06:48:14Z",9]` (oldest first). Same call on `/comments` returned `["2026-11-07T06:48:11Z","2026-11-07T06:48:12Z"]` (ascending). Both order claims in synth-04 hold.
- Precedent verified by Bash `sed -n 44,56p` of `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`: line 46 "Explicit page numbers ...", line 47 "1000 pages per source; fail incomplete at the cap, never silently truncate", line 51 `for ((page=1; page<=1000; page++))`, lines 53-55 `--method GET -F per_page=100 -F page=...`. synth-04 cites `:47` and `:51` correctly.
- Truncation is a per-issue skip, not a cycle failure; the exit-code table (lines 255-262) is unaffected. No contradiction found.

### Check 4 - Consolidated finding #2 (Requirement Scoring convention): RESOLVED

Read synth-03 lines 276-310 in full.

- One rule: the "Scoring convention" paragraph (line 278) defines Meets / Partly / Does not meet once, for all four options and all ten requirements, and states the exclusions (Coder#477 listener and registry, a GitHub App, a hosted service, a new org secret or token-scope grant, any [UNVERIFIED] fact or open rule in the cell). "(design level)" no longer appears (Grep for `design level|design-level` over synth-03: only the rule sentence at line 278 that forbids it, and lines 306 and 368 do not use it as a rating).
- Recomputed tally from the cells I read (lines 282-291). Meets cells: R1 = A, B, D (C is Partly); R8 = A, D (B, C Partly); every cell of R2, R3, R4, R5, R6, R7, R9, R10 = Partly for all four options. So A = 2 (R1, R8), B = 1 (R1), C = 0, D = 2 (R1, R8). Row sums of the Tally table (lines 295-300): A 2+8+0, B 1+9+0, C 0+10+0, D 2+8+0, each 10. The Tally table matches the recomputation exactly. The table itself has 5 cells in each of the 12 rows (awk pipe count 6 per row).
- Every place the tally is quoted: synth-03 line 302 (no numbers, caveat only), line 306 ("A and D have 2 Meets (R1, R8), B has 1 (R1) and C has 0"), line 368 ("A and D count 2 Meets, B 1 and C 0"). All three agree with the table. Grep for `Meets|tally|Tally|raw count|score above` over synth-01, synth-02 and synth-04 returns no match, and a Grep for `scor|rating|Partly` there finds only references to "scored in Section 6" without numbers (synth-02 lines 7, 82, 86, 152, 174; synth-04 none). So the old tally (A 2, B 5, C 6, D 3) survives nowhere (Grep for `B 5|C 6|D 3|design level` over synth-03 returned only lines that are the new text). The lead's wording "quoted in synth-02/03/04": only synth-03 quotes numbers; synth-02 and synth-04 quote none, so there is nothing stale to reconcile.
- Cell basis for the re-scored cells traces to research: `research/web-01-github-events-projects-and-limits.md:188` (`projects_v2_item` is an organization webhook event needing an App with org Projects read), `:189` (`GITHUB_TOKEN` has no projects permission), `:219` (Gaps item 7, org token policies UNVERIFIED); Coder#477 "not known yet" is in research-notes.md line 102. No new fact was added by the re-scoring.
- Rule applied without cell-level exceptions: each Meets cell (A R1, A R8, B R1, D R1, D R8) names no unbuilt outside-repo dependency and no [UNVERIFIED] item in the cell; every Partly cell names the unbuilt, unverified or open item that caused it (checked all 40 cells). The label-setup lines count as in-repo mechanism by the rule's own list, which is why A R1 is Meets while R3 (a token-scope grant) is Partly; that distinction is stated, not hidden.
- Tilt check (did the new scoring tilt the Recommendation by assertion?): No. 7.1 (line 353) states the recommendation as "decided by the owner (ADDENDUM 2)" and rests on that. 7.2 (line 359) says it "states the trade-offs, including where A scores lower". The rationale rows name the structural reasons for A (no listener, no inbound port, no registry, Effort M) and a separate row (line 364) says B and C are structurally stronger on R2, R9 and R10 and latency, which the count hides. Line 368 says the count rates only what exists today, is not a measure of design quality, and that the decision rests on the removed listener, port and registry. The fix log (line 107) openly records that the rule was the one the consolidated findings proposed. The shift of the ranking from B/C ahead (old 5 and 6) to A/D ahead (2) follows from applying the stated rule to the 11 cells the earlier QA agents flagged as inconsistent, not from text asserting A is best.
- NOTE (minor, not blocking): the rule measures "buildable with no dependency outside this repo" more than requirement satisfaction, so it structurally favours any in-repo option. This is disclosed three times (lines 278, 302, 368). Also line 278 says cells "rate each design on what exists today" while allowing Meets for "the option's own described in-repo mechanism" (not built either); wording only.

### Check 5 - No new blocking issue introduced by the fixes: PASS

- Fabrication: every new claim traces. Candidate-4 qualification: `web-02...:186`, `01-claim-flow...:157` (read). Events order on issue #331: observed by the fix agent and re-run by me (result above). Page-cap precedent: `poll-augment-review.sh:46-47,51` (read). `codebase-context.md:21` (read). Re-scored cells: W01 lines 188, 189, 219 (read).
- Doc-only claims in Sections 2, 6, 7, 8: none added. The new Section 8 text is a design rule marked [PROPOSAL] plus code-verified precedent.
- Table structure: the four edited places keep their column counts. awk column check over the four files flagged only synth-03 line 148 and synth-02 lines 118, 264, 273, 359, none of which the fixes edited (the fixes edited synth-02 lines 116, 138, 305, 407, and synth-03 lines 278-310, 324, 363-368). They are bare `|` characters inside code spans (for example `repository|issue_number|approval_event_id` at synth-03 line 148, `gh project|projectV2|graphql` at synth-02 line 118). Pre-existing, cosmetic rendering note, not recheckable under the severity rule.
- Missing sections or placeholders: none. Grep for `TBD|TODO|FIXME|pending owner|undecided` over `synthesis/` found only the words "placeholder" (label-name placeholders, the `{owner}` placeholder) and "not decided" (synth-03 line 220, hosting not decided in any research file; synth-01 line 400), all legitimate.
- Hallucinated paths: the only new paths are `poll-augment-review.sh` (exists, read) and `enrichment/codebase-context.md` (exists, read).
- Scope of edits: mtimes (`stat`) show all seven research files, research-notes.md and gaps-and-questions.md older (07:34 to 08:50) than the consolidated findings (09:16); synth-01..04 modified 09:19 to 09:22; fix log 09:23. Only synthesis files changed in this cycle.

### Check 6 - Four files still cover Sections 1-10 in order: PASS

Heading Grep: synth-01 `## 1. Problem Statement` (line 17), `## 2. Current State Analysis` (line 55). synth-02 `## 3. Target State` (13), `## 4. Gap Analysis` (102), `## 5. External Research Findings` (178). synth-03 `## 6. Options Analysis` (28), `## 7. Recommendation` (349). synth-04 `## 8. Implementation Plan` (28), `## 9. Open Questions` (395), `## 10. Evidence Trail` (468). Order and coverage intact.

### Check 7 - Binding addenda in research-notes.md (ADDENDUM 2): PASS

- Option A labelled "decided by the owner": synth-03 line 77 (heading), line 353, line 7; synth-01 line 39; synth-04 line 7 and 9.1. Grep for `pending owner|owner decision pending` over `synthesis/`: no match.
- B and C scored: synth-03 Requirement Scoring table columns B and C (lines 282-291), Options Comparison (lines 314-327), Revisit conditions (lines 329-345).
- Coder#477 with its repo boundary and the "A makes it unnecessary unless B or C is revisited" statement: synth-01 line 50-51, synth-02 line 7 and G18 row (line 127), synth-03 7.7 (line 431) and line 7, synth-04 D5 (line 407) and follow-up table (line 351). Grep `unnecessary` finds it in all four files.
- Integer-only rule stated: synth-01 Q3 row (line 41), synth-03 7.3 Prompt row (line 379), synth-04 D3 (line 91, 405), step 3.2 and the rule paragraph under Phase 1 (line 113).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | synth-02 line 138 | "research/research-notes.md (row G2)": research-notes.md has no row G2 (the correction is the ci.py EXISTING_FILES row, line 30) | Say "EXISTING_FILES row for `ci.py`" |
| 2 | MINOR | synth-04 step 4.2 (line 203) | "the events and comments lists come back oldest first" is stated without a source for the comments half (events half cites the #331 observation, line 190). True when I re-ran it | Add "observed on issue #331, 2026-11-07" to the comments half |
| 3 | MINOR | synth-03 line 278 / lines 302, 368 | Scoring rule favours in-repo mechanisms by construction; wording "what exists today" vs "described in-repo mechanism" is slightly loose. Disclosed in the text | None needed |
| 4 | MINOR | synth-03 line 148; synth-02 lines 118, 264, 273, 359 | Bare `|` inside code spans in table cells breaks the cell split in GFM; pre-existing, not touched by the fixes | Escape as `\|` |
| 5 | MINOR | synth-04 steps 4.2 and 5.2 | A permanently truncated issue (more than 500 events) is skipped every cycle with exit 0; visible only in the audit line | Optional: count `approval-unverifiable` in the exit code |

No blocking finding is open.

## Summary

- Previously blocking findings: 4 of 4 resolved (consolidated #1, #2, #3, #4).
- New blocking findings introduced by the fixes: 0.
- Minor notes: 5 (not rechecked in later rounds).
- Requirement Scoring: one rule, recomputed tally A 2, B 1, C 0, D 2 matches the table and every quotation (synth-03 lines 302, 306, 368); synth-02 and synth-04 quote no tally; no tilt by assertion.
- Checks passed: 7 of 7 (Checks 1 to 7 above).

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (15 items: 4 resolved findings, no-new-blocking, section order, 4 addenda items, 4 scoring-consistency items (single rule, recomputed tally, every quotation, no tilt)).
**Tool engagement:** Read: 14 | Grep: 11 | Glob: 1 | Bash: 4 (including two read-only `gh api --method GET repos/IronbellyOrg/IronClaude/issues/331/{events,comments}` calls, no write, no web research, so no tavily or fallback calls)

## Recommendations

- Proceed to the next gate. Minor notes 1 and 2 are optional wording fixes for whoever assembles the report.

VERDICT: PASS

Status: Complete

## QA Complete

