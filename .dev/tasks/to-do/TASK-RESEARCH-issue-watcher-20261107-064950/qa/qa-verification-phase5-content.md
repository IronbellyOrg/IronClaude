# QA Report - Phase 5 Content Verification (report-qualitative, fix-cycle re-verification)

**Topic:** GitHub issue watcher research (issue 331), synthesis files after the Phase 5 fix cycle
**Date:** 2026-11-07
**Phase:** report-qualitative (fix-cycle verification)
**Fix cycle:** Phase 5 fix cycle 1
**Fix authorization:** false (report only; no synthesis file modified)
**Status:** Complete
**Overall Verdict:** FAIL (1 blocking finding; see Issues Found)

---

## Check log (appended incrementally)

### Step 1: Inputs read
- Read task file line 265 (binding prompt), `qa/qa-consolidated-findings-phase5.md` (4 blocking: #1 codebase-context ci.py clause, #2 scoring convention, #3 "post-write re-read", #4 page cap fails open), `qa/qa-fix-log-phase5.md` (all four marked FIXED).
- Read `synthesis/synth-03-options-recommendation.md` lines 1-540 in full (all of sections 6 and 7, scoring, tally, revisit table, coverage, carried items).

### Step 2: synth-03 re-scoring (finding #2) - cell-by-cell audit (own reading of lines 278-310)
Rule as written (line 278): Meets only if satisfied today or by the option's own in-repo mechanism, with no dependency on anything unbuilt outside this repo (Coder#477 listener/registry, GitHub App, hosted service, new org secret or token-scope grant) and no [UNVERIFIED]/open rule in the cell; else Partly; Does not meet only if the mechanism cannot satisfy it.
Tally recomputed from the 40 cell labels in the table (lines 282-291): A Meets = R1, R8 (2); B Meets = R1 (1); C Meets = none (0); D Meets = R1, R8 (2); no Does-not-meet anywhere. This matches the Tally table (lines 295-300) exactly. Fix log claims (A 2, B 1, C 0, D 2) match.
Uniformity of the rule across options:
- R3: A, B, C, D all Partly, each for a missing token, secret or scope grant. Uniform.
- R4: all four Partly (unverified server-side filter, or unbuilt App). Uniform.
- R2: all four Partly (no allow-list exists, location open, GAPS 14). Uniform; B and C are no longer credited "at design level".
- R9, R10: all four Partly. Uniform label; the reasons differ (A: no central trail / no atomic exclusion; B, C: unbuilt receiver/service).
- R1: A, B, D Meets (in-repo label-setup lines count as in-repo mechanism per the rule text); C Partly (needs the unbuilt service). Consistent with the rule.
- R8: A and D Meets (no inbound surface exists); B and C Partly (listener unbuilt, mTLS/header [UNVERIFIED]). Consistent.
Minor note M-A: the line between "label-setup lines count as in-repo mechanism" (R1 Meets for A, B, D although the label does not exist) and "a per-developer `gh auth refresh -s read:project` stays Partly" is drawn by the rule's explicit list (token-scope grant, new org secret = outside the repo), so it is consistent, but a reader may find it thin.
Minor note M-B: line 306 says A "cannot close" R2 by setup because every poller holds its own allow-list copy (W02 J3 item 3), while 7.9 item 2 leaves the allow-list location open (repo file, org team, CODEOWNERS-like). An allow-list read from one repo file or org team would give A one copy. Sourced from W02, so a note, not a blocker.
Result: one rule applied to all 40 cells and the tally follows from the cells. It is not tilted toward A: A only ties D at 2 and is 1 and 2 above B and C because B and C depend on unbuilt external components, which lines 302 and 368 state explicitly.
Minor note M-C: the A cell for R9 (line 290) still opens with "no record of the poller's own decision", but synth-04 step 5.3 and run_cycle row 13 (lines 219 and 238) emit one JSON audit line per decision and the dispatch record stores approver and approval event id. The label stays Partly (no central trail; stdout persistence depends on the Coder scheduler), but the first clause is stale against the plan.

### Step 3: B and C structurally stronger on R2, R9, R10 vs decided Recommendation A (synth-03 lines 302-310, 349-368, 329-345)
- Line 306 states that under the one rule A and D have 2 Meets, B 1, C 0, and that "the count does not show three properties in which B and C are structurally stronger than A if their unbuilt component is built: R2, R9 and R10", mapped to revisit conditions 3 and 4 (lines 337-338). Line 364 (7.2 row "Where B and C are structurally stronger than A") repeats R2, R9, R10, latency and stopped-workspace. Line 368 ("What the score does and does not say") says the count rates only what exists today, does not credit B or C for the central allow-list, audit trail and decision point, and that the owner's decision rests on removing the listener, inbound port and registry.
- This does not contradict the decided Recommendation A: 7.1 (line 353) says "decided by the owner (ADDENDUM 2)", the recommendation does not claim A wins on the score, and 7.2 says "including where A scores lower". The tally note (line 302) says the count "is not a measure of design quality". PASS on this point. The text is honest in both directions: it does not hide that the re-score now ranks A at or above B and C, and it names why (unbuilt components), and it names the three properties the count cannot show.
- No "pending owner decision" text anywhere in synthesis (grep for "pending owner" over synth-01..04 returned no match). Option A is labelled "Decided by the owner" / "decided by the owner" in synth-03 lines 77 and 353 (line 7 says "Binding owner decision"); synth-01 line 39; synth-04 line 7 ("Binding owner decision") and 9.1 D1 (line 403).

### Step 6: Finding #4 (approval check on partial data) - fix is present but does not work as specified
What was verified true: (1) the live read-only calls I re-ran on 2026-11-07 (`gh api --method GET repos/IronbellyOrg/IronClaude/issues/331/events -F per_page=100 --jq '[.[0].created_at,.[-1].created_at,length]'`) returned `["2026-10-30T14:39:35Z","2026-11-07T06:48:14Z",9]` and the same on `/comments` returned `["2026-11-07T06:48:11Z","2026-11-07T06:48:12Z",2]`: both lists are oldest first, so a page cap drops the newest entries, as the fix log says. (2) `poll-augment-review.sh:46-47` holds the comment "Explicit page numbers ..." and "fail incomplete at the cap, never silently truncate"; `:51` is `for ((page=1; page<=1000; page++))`; the cited precedent is real. (3) The fail-closed rule appears at step 4.2 (line 203), step 4.3 (line 204), step 4.5 (line 206), the Filter 2 row (line 177), the Calls table (line 190), `run_cycle` rows 5 and 6 (lines 230-231) and the "Truncated read" scenario (line 281). The wiring between the files is consistent (no contradiction among synth-02 Section 4, synth-03 Section 7 and synth-04 Section 8; synth-02 and synth-03 never describe a page cap).

What is wrong (new blocking defect in the fix): step 4.2 detects truncation by "page `max_pages` is reached and is still full (100 items)". But the calls that produce each page project the data inside `gh` before the code sees it: `events-jq` (line 194) is `[.[] | select(.event=="labeled" or .event=="unlabeled") | {...}]` and `marker-jq` (line 195) returns only matching comment ids, and the plan says "only ids leave it" (line 198). A raw page of 100 events that holds, say, 40 label events comes back as a 40-element list; a raw page of 100 comments comes back with 0 or 1 ids. The "is it a full page" test therefore never fires in real use (the comments case can never reach 100), and the rule that ends paging (a short page) cannot be told from a full page either, so the loop can stop at page 1 on a busy issue and return a partial list without any error. That is exactly the fail-open behaviour finding #4 asked to remove, and the repo's own precedent counts raw items per page (`poll-augment-review.sh` fetches the raw page, then counts). The "Truncated read" test (line 281) feeds a fixture of 100 label events per page, which bypasses the jq, so it would pass while real behaviour stays unsafe.
Required fix (synth-04 only, small): make each page call return the raw page length together with the projection (for example `--jq '{n: length, items: [...]}'`), define the loop as "continue while n == 100; if n == 100 at page `max_pages`, raise `E-GH-TRUNCATED`", apply it to both `label_events` and `own_claim_comment_ids`, and make the Truncated read fixtures use raw pages whose label-event or marker content is under 100 (for example a raw page of 100 events with 10 label events must still raise at the cap).

### Step 7: Checks (c) and (d) of the prompt, and cross-file consistency
- (c) three issue questions: synth-01 lines 21-27 table answers Microservice vs Action (A, neither push design), workspace-to-account tie (own `gh` login, owner-equals-login unverified) and the Coder-side listener (none under A; the poller is the whole component). synth-03 6.1 lines 126-132 repeat Q-a, Q-b, Q-c for A, and 6.2, 6.3, 6.4 answer them for B, C, D. Still answered.
- (c) B and C remain scored (synth-03 lines 282-291, Tally 295-300), documented (6.2, 6.3) and carry nine revisit conditions (lines 329-345; synth-04 lines 360-372 repeats the same nine; 7.8 says "nine"). Coder#477 is stated as a sibling dependency in the Coder repo that A makes unnecessary unless B or C is revisited: synth-03 line 7 and 7.7 (line 431), synth-01 line 51, synth-02 SC-15 (line 62), synth-04 lines 7, 351, 407.
- (d) external supplements, never overrides: synth-02 line 180 ("The codebase is the source of truth: no external finding below overrides verified code behavior"), synth-03 line 24, synth-04 line 24. The only fix-cycle fact that came from outside the files (oldest-first event order) is a live read-only call that I re-ran, not a web finding.
- Cross-file wording: the "nine revisit conditions" count agrees in synth-02 (line 408), synth-03 (7.8), synth-04 (9.1 D6). The earlier minor note that synth-02 lists different conditions stays a note.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Finding #1 (codebase-context ci.py clause) addressed substantively in synth-01, 02, 04 | PASS | Step 4: clause present at synth-01:242, synth-02:138, synth-04:457; cited lines 21, 30, 37 read and say what is claimed |
| 2 | Finding #2: one scoring rule, applied to every cell of all four options | PASS | Step 2: rule at synth-03:278; R2, R3, R4, R9, R10 Partly for all four; R1 and R8 follow the rule's in-repo / unbuilt-dependency test |
| 3 | Re-scored tally follows from the cells; old tally not quoted anywhere | PASS | Own recount from lines 282-291 gives A 2, B 1, C 0, D 2 = lines 295-300; grep for tally, Meets, "design level" in synth-01/02/04 returns no match; synth-03 line 278 mentions "design level" only to say it is no longer credited |
| 4 | Text still conveys B and C structurally stronger on R2, R9, R10 without contradicting decided A | PASS | Step 3: lines 302, 306, 364, 368 plus revisit conditions 3 and 4; 7.1 keeps "decided by the owner" |
| 5 | Finding #3: "post-write re-read" removed as a built layer; algorithm, step 1.7, intro and Section 4 agree | PASS | Step 5: only five "candidate 4 only / not built" mentions remain; run_cycle row 8 is the only re-read; sources at web-02:186 and R01:157 read |
| 6 | Finding #4: approval check fails closed when the events read hits the page cap | FAIL | Step 6: the full-page test counts jq-projected items, so it cannot fire in real use and paging can stop on a short filtered page; truncation test uses a fixture that bypasses the jq |
| 7 | Fixes introduced no contradiction between Section 4 gaps (synth-02), Section 7 (synth-03) and Section 8 (synth-04) | PASS | Step 5 and 7: G7, 5.12 rows, 7.4, step 1.7, Phase 5 intro, run_cycle all use "pre-launch re-read"; no section mentions a page cap except synth-04. Only defect is internal to synth-04 (check 6) |
| 8 | Recommendation is A "decided by the owner", never "pending owner decision" | PASS | grep "pending owner" over synth-01..04: no match; labels at synth-03:77, :353; synth-01:39; synth-04:403 |
| 9 | Recommendation still answers the three issue questions | PASS | Step 7: synth-01:21-27; synth-03:126-132 and Q-a/b/c tables for B, C, D |
| 10 | B and C still scored and documented with revisit conditions; Coder#477 sibling dependency made unnecessary by A unless B or C revisited | PASS | Step 7: synth-03:282-291, 329-345, 431; synth-04:351, 360-374, 407 |
| 11 | External findings supplement and never override verified code | PASS | Step 7: synth-02:180, synth-03:24, synth-04:24; oldest-first order checked by a live call, not a web claim |
| 12 | Fix log claims match the files (cells changed, lines named, tally) | PASS with caveat | Cells, tally, quoted lines and `post-write` grep results all match; the log's statement that finding 4 is "FIXED" is not borne out (check 6) |

## Summary
- Checks passed: 11 / 12
- Checks failed: 1 (check 6)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 1
- Issues fixed in-place: 0 (report only; no synthesis file modified)
- Confidence: Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this measures evidence coverage; the verdict is FAIL because one verified check failed)
- Tool engagement: Read: 11 | Grep: 6 | Glob: 0 | Bash: 9 (Read + Grep + Glob = 17 >= 12 items)
- Web research: none performed (no Tavily or WebFetch call; the only network calls were two read-only `gh api --method GET repos/IronbellyOrg/IronClaude/issues/331/...` reads)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT (blocking) | synth-04 Phase 4: Calls table lines 190-191, `events-jq`/`marker-jq` lines 194-195, step 4.2 line 203, test line 281 | The truncation guard of fix #4 tests "page still full (100 items)" on data that `--jq` has already filtered to label events or comment ids. The guard cannot fire for real data, the paging stop rule is unstated and a short filtered page looks like the end of the list, so the approval check and the claim-marker check can still decide on partial data. The test fixture bypasses the jq and would pass anyway | Return the raw page length from each call (for example `{n: length, items: [...]}`), page while `n == 100`, raise `E-GH-TRUNCATED` when `n == 100` at `max_pages`, for both `label_events` and `own_claim_comment_ids`; change the "Truncated read" and step 4.5 fixtures to raw pages of 100 that hold fewer than 100 label events or markers |
| 2 | MINOR | synth-03:290 | R9 cell for A says "no record of the poller's own decision"; the plan (synth-04:219, :238) emits an audit line per decision | Reword to "decision lines go to stdout and the dispatch record; no central trail" |
| 3 | MINOR | synth-03:306 vs 7.9 item 2 | "A cannot close R2 by setup" sits beside an open allow-list location (a repo file or org team would be one copy) | Say "unless the allow-list is a single shared file or team" |
| 4 | MINOR | synth-02:138 | Cites "research-notes.md (row G2)"; no such row label exists (synth-01 and synth-04 correctly cite lines 30 and 37) | Replace with "EXISTING_FILES row, line 30" |
| 5 | MINOR | synth-03:278 rule | Label setup counts as in-repo (R1 Meets) while a per-developer scope grant is outside the repo (R3 Partly); consistent by the rule's list but thin | Add one sentence saying why |

Minor notes are not rechecked and never fail a review. The pre-existing minor findings of the Phase 5 reports (M1-M13, M1-M6, M-1-M-4) were not re-reviewed.

## Actions Taken
None. Fix authorization is false; no synthesis file was modified. The only file written is this report. The two `gh api` calls were read-only GETs pinned to `repos/IronbellyOrg/IronClaude/`.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` block was in the spawn prompt (it pointed me to the consolidated findings, the fix log and the synthesis files), so I ran standalone and relied on no rf-qa PASS item. `qa/qa-verification-phase5-structural.md` was 297 bytes and still being written when I started; I did not use it.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied; fix-log statements were treated as claims to test, not as evidence.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Tally recount - recounted 40 cells in synth-03:282-291 and got A 2, B 1, C 0, D 2, matching lines 295-300 and the fix log.
- Rule uniformity - compared the R1-R10 rows across A, B, C, D against the rule at synth-03:278.
- Citation reads - read `codebase-context.md:21`, `research-notes.md:30,37`, `web-02:186`, `01-claim-flow:157`, `poll-augment-review.sh:44-56` (Bash sed) and confirmed each says what the synthesis cites.
- Live API check - re-ran two read-only `gh api` GETs on issue #331 (events: 9 items, oldest 2026-10-30, newest 2026-11-07; comments: 2 items ascending), which confirms the oldest-first premise.
- Plan trace of fix #4 - read synth-04 lines 167-283 and traced a raw page of 100 events through `events-jq` to the "still full" test; this found the defect in check 6, which no rf-qa PASS could have shown.

1. Factual claims independently verified: about 45 (cell labels, tallies, line citations, grep counts, API order).
2. Files read: synth-03 (all), synth-04 lines 28-127, 167-283, 340-467, synth-01 lines 17-45 and 242 context, synth-02 lines 62, 116, 138, 161-183, 305, 407; the consolidated findings; the fix log; the five cited source lines.
3. This review did not find 0 issues: it found one blocking defect and four minor notes.
4. No web research was performed, so no Tavily versus fallback decision arose.

## Recommendations
- Apply the Issue 1 fix in synth-04 only (about four sentences and two fixture descriptions), then run one more review limited to that fix. This is fix cycle 1 of at most 2, so one more fix cycle remains.
- Optionally apply the four minor wording notes in the same edit; they do not gate the verdict.

## QA Complete

VERDICT: FAIL


### Step 4: Finding #1 (codebase-context.md ci.py clause) - verified
- synth-01 line 242: clause present, cites `codebase-context.md` line 21 and `research-notes.md` lines 30 and 37.
- synth-02 line 138 (row G29 Notes): clause present, cites `codebase-context.md` line 21.
- synth-04 line 457 (row C4): clause present, cites `codebase-context.md` line 21 and `research-notes.md` lines 30, 37.
- Own read of the cited sources: `.dev/brainstorms/.../enrichment/codebase-context.md:21` begins "CORRECTION (2026-11-07, research alignment check): ... ci.py is NOT a gh subprocess wrapper"; `research/research-notes.md:30` and `:37` carry the CORRECTED ci.py text. All three cited lines say what the synthesis says. Addressed substantively.
- Minor note M-D: synth-02 line 138 points to "research-notes.md (row G2)"; research-notes.md has no row labelled G2 (grep for the token returned nothing), while synth-01 and synth-04 correctly say lines 30 and 37. Wrong row label, not a wrong fact.

### Step 5: Finding #3 ("post-write re-read") - verified
- Grep of `post-write` over synthesis returns only the five "belongs only to candidate 4 / not built" statements: synth-02 lines 116, 305, 407; synth-04 lines 108, 213. synth-03 contains none; its comparison and R10 cell say "pre-launch re-read" (lines 291, 324).
- synth-04 `run_cycle` table (lines 225-238) has no step after the launch; row 8 (line 233) is the "pre-launch re-read and the only re-read in the cycle". Step 1.7 (line 108) and the Phase 5 intro (line 213) agree with the table, and both cite SC-13 (poller never writes). The cited sources exist: `research/web-02-coder-claude-dispatch-and-security.md:186` is the "post-write check ... read-after-write ... [PROPOSAL]" bullet; `research/01-claim-flow-and-session-launch.md:157` is the "poller-side reservation ... UNVERIFIED" suggestion. Addressed substantively; no residual contradiction among Section 4 (synth-02 G7), Section 7 (synth-03 7.4 optional reservation for candidate 4) and Section 8.


