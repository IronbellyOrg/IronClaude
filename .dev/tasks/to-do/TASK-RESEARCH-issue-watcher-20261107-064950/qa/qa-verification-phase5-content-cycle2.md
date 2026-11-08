# QA Report - Phase 5 Content Verification (report-qualitative, fix-cycle re-verification)

**Topic:** GitHub issue watcher research (issue 331), synthesis files after Phase 5 fix cycle 2
**Date:** 2026-11-07
**Phase:** report-qualitative (fix-cycle verification)
**Fix cycle:** Phase 5 fix cycle 2
**Fix authorization:** false (report only; no synthesis file modified)
**Status:** Complete
**Overall Verdict:** PASS (no blocking finding open; 5 minor notes)

---

## Check log (appended incrementally)

### Step 1: Inputs read
- Read task file line 269 (binding prompt), `qa/qa-consolidated-findings-phase5-cycle2.md` (1 blocking: truncation guard tested the jq-filtered page length), `qa/qa-fix-log-phase5-cycle2.md` (marks it FIXED, 8 edits in synth-04 only), the cycle-1 content report `qa/qa-verification-phase5-content.md` (VERDICT: FAIL, 1 blocking, 4 minor) and `research/research-notes.md` (binding addenda 1 and 2).
- No `## Inherited Structural Verdict` block was in the spawn prompt; the sibling `qa/qa-verification-phase5-structural-cycle2.md` was still a 318-byte stub when I started, so I relied on none of it and ran standalone.
- File state: `stat` shows synth-01 (09:22:11), synth-02 (09:22:12) and synth-03 (09:19:54) older than the cycle-1 content report (09:32:40); only synth-04 (09:33:59) changed in cycle 2. This matches the fix log (edit scope = synth-04 only). Cycle-1 results for synth-01..03 therefore still hold and I re-ran only grep-level checks on them.

### Step 2: Was the cycle-2 blocking finding addressed substantively? (synth-04, own reading of lines 170-300)
Finding: the full-page test ran on `--jq`-filtered data, so it could not fire and a short filtered page looked like the end of the list.
Each of the eight edits the fix log lists is present in the file at the line it names:
- Lines 194-195: `events-jq` is `{n: length, items: [...]}` and `marker-jq` is `{n: length, items: [... | .id]}`. I ran both filters in `jq 1.7` on sample raw pages: a raw page of 2 events with 1 label event gives `{"n":2,"items":[{"id":1,...}]}`; a raw page of 2 comments with one own marker gives `{"n":2,"items":[5]}`; an empty page gives `{"n":0,"items":[]}`. So `n` is the raw page length taken before any `select`, as claimed.
- Line 198: states the page-end test uses `n`, never `len(items)`, with the 100-events/40-label-events example. The cited precedent is real: `poll-augment-review.sh:69` is `count="$(jq 'length' "$_tmp/rest-page.json")"`, `:70` is `if [ "$count" -lt 100 ]; then completed=true; break; fi`, `:74` is `[ "$completed" = true ] || return 1`, `:47` the "fail incomplete at the cap, never silently truncate" comment, `:51` the 1000-page loop. All five read directly.
- Lines 190-191 (Returns column), 205 (step 4.2), 207 (step 4.4), 208 (step 4.5), 283 ("Truncated read") and 295 (step 6.1) all carry the same rule: continue while `n == 100`, stop with a complete list on `n < 100`, raise `E-GH-TRUNCATED` when page `max_pages` still has `n == 100`, for both `label_events` and `own_claim_comment_ids`; malformed output (not an object with integer `n` and list `items`) raises `E-GH-FAILED`.
- The fixtures are now RAW REST pages that hold fewer than 100 label events (for example 40), the unit `FakeRunner` and the PATH stub apply the received `--jq` string with `jq -c`, so a wrong filter fails a test. This answers the cycle-1 complaint that the fixture bypassed the filter. The new case "n == 100 with short filtered items followed by a page with n < 100 is read to the end" is the exact scenario the old guard got wrong.
- Wiring downstream is unchanged and still correct: `run_cycle` rows 5 and 6 (lines 232-233) map `E-GH-TRUNCATED` to `approval-unverifiable` / `claim-marker-unverifiable`; step 4.3 (line 206) says `is_approved` only ever sees a complete list.
- `grep "still full"` over `synthesis/` returns 0 in all four files.
Result: substantive, not cosmetic. The guard now tests the right quantity, the paging stop rule is stated, both reads are covered, and the tests can fail for the defect they target.

### Step 3: Contradictions introduced by the fix (check b)
Traced the rule through every place in the four files that touches reads, caps or the unverifiable outcomes:
- Call table (synth-04:190-191), jq block (:194-195), rule paragraph (:198), filter 2 row (:177), step 4.2 (:205), step 4.3 (:206), step 4.4 (:207), step 4.5 (:208), `run_cycle` rows 5-6 (:232-233), "Truncated read" scenario (:283), step 6.1 (:295). All use the same quantity (`n`, raw page length), the same stop rule, the same error code and the same two mapped reasons. No place still tests the filtered length.
- synth-01, synth-02, synth-03 never describe a page cap or a full-page test (grep for `paginat|truncat|per_page|E-GH|max_pages|approval-unverifiable` over them: only `per_page` maxima in synth-02:213/241/242 and `--limit` in synth-03:87/427, all consistent with `per_page=100`). So Section 4 gaps (synth-02) and Section 7 (synth-03) cannot contradict Section 8 on this point, and the Section 4 / Section 7 / Section 8 chain on at-most-once ("pre-launch re-read", no post-write re-read) is untouched by cycle 2.
- Section 8 vs Section 9: `max_pages = 5` is tagged [PROPOSAL] with no `open:` marker, so the Section 9 rule "every `open:` item has a Q row" is not broken.
- Exit-code table (:261-264): a truncated read is a per-issue skip (exit 0). Consistent with row 5/6 ("rejects the issue" / "skips the issue").
- Pre-existing and explained, not a contradiction: synth-03:90 shows `str(int(number))` (the R01 §13 form) while synth-04 step 3.2 uses a stricter check and says so in its own text.

### Step 4: Recommendation, three questions, B and C, Coder#477, external findings (checks c and d), own reads
- Option A "decided by the owner": synth-03:77 ("Decided by the owner"), :353 ("decided by the owner (ADDENDUM 2)"), :7; synth-01:39 and :43; synth-04:7 ("Binding owner decision"), :399-405 (D1). `grep -i "pending owner"` over all four files: no match.
- Three issue questions: synth-01:21-25 table answers Action versus microservice (neither push design; B and C stay alternatives), workspace-to-account tie (own `gh` login; owner-equals-login stays [UNVERIFIED]) and the Coder-side listener (none under A; the poller is the whole component). Read directly.
- B and C scored and documented: synth-03:280-291 (40 cells, one rule at :278), Tally :295-300 (A 2, B 1, C 0, D 2; I re-counted the Meets labels in the table and they match), "Reading the scores" :304-307 and 7.2 rows :364, :366, :368 say plainly where B and C are structurally stronger and that the count is not a design-quality measure. Nine revisit conditions at synth-04:364-374 (count 9) and synth-03:329; synth-04:376 says option A stays and Coder#477 is unnecessary if none holds.
- Coder#477: synth-01:47-51 (boundary: listener, registration and transport live in the Coder repo; "Option A makes #477 unnecessary unless B or C is revisited"), synth-04:7, :353, :409 (D5), :103 (design-doc step 1.2).
- Integer-only rule: synth-01:41, synth-04:91 (D3), :113 (rule recorded in the doc), step 3.2 (:159), :407.
- External supplements, never overrides: synth-02:180, synth-03:24, synth-04:24 and :472. The one non-file fact in the fix path (oldest-first event order, synth-04:190) was confirmed in cycle 1 by a live read-only call and is labelled as such in the cell.

### Step 5: Sourcing and tag discipline of the added text; sections 1-10 intact
- New text cites `poll-augment-review.sh:47, :69-70, :74` (all read and true) and the plan's own logic. No research file cites those three lines (research/02 mentions the script at :105 and :107 only for the `--method GET` pattern), so they are direct repo reads, not research-file citations. That is a stronger source for a code claim and nothing is invented. Placeholders: grep for `TODO|TBD|FIXME|XXX|???` over `synthesis/`: no match.
- The fix introduced a tag `[DESIGN]` (synth-04:198, :208, :295). The tag key at synth-04:24 defines CODE-VERIFIED, CODE-CONTRADICTED, EXTERNAL-VERIFIED, UNVERIFIED, PROPOSAL and DERIVED only. `[DESIGN]` is undefined (minor note M1).
- Headings: synth-01 has `## 1.` and `## 2.`; synth-02 `## 3.`, `## 4.`, `## 5.`; synth-03 `## 6.` and `## 7.`; synth-04 `## 8.`, `## 9.`, `## 10.`. Sections 1-10 are present in order (line numbers in the table above from `grep -n "^## "`).

### Step 6: Residual weaknesses looked for in the fix (none blocking)
- jq availability: step 4.5 (:208) now has the UNIT `FakeRunner` shell out to `jq -c`, and the "Truncated read" scenario depends on it. Step 6.1 (:295) and Q32 (:449) only say the E2E tests skip when `jq` is absent, and Q32 rates the whole topic Low. So on a host without `jq` the unit tests would fail instead of skipping, and acceptance criterion 10 (:298, pytest passes) would not hold there. `jq` exists here (`/usr/bin/jq`, 1.7) and existing PATH-stub tests already depend on it (`tests/pr_submit/test_cosmos_poll.py:106,116`), so the risk is small. The fix is one sentence in step 4.5 and Q32. Minor note M2.
- Engine mismatch: `gh --jq` runs gojq while the tests run the `jq` binary. Both implement the used subset (`length`, `select`, `contains`, object construction) the same way; I ran the two filters in jq 1.7 only. Minor note M3.
- Exactly 500 items: if a list has exactly `max_pages * 100` entries, page 5 has `n == 100` and the code raises `E-GH-TRUNCATED` although the list is complete. This is the safe direction (fail closed) and is not stated. Minor note M4.
- Acceptance criteria (:298) have no explicit line for "an unreadable or truncated approval or marker read selects nothing"; criterion 4 covers it only by implication. Minor note M5.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | (a) Cycle-2 blocking finding (truncation guard on filtered length) addressed substantively | PASS | Step 2: `events-jq`/`marker-jq` return `{n, items}` (synth-04:194-195); page-end test on `n` (:198, :205); `E-GH-TRUNCATED` at `max_pages` with `n == 100` for both reads; malformed output raises `E-GH-FAILED` |
| 2 | Precedent citations in the fix are real | PASS | Step 2: `poll-augment-review.sh:47, :51, :69, :70, :74` read directly and say what synth-04:190/198/205 claim |
| 3 | The new jq filters behave as claimed | PASS | Step 2: both filters executed in jq 1.7 on sample raw pages: `{"n":2,"items":[...1 label event...]}`, `{"n":2,"items":[5]}`, `{"n":0,"items":[]}` |
| 4 | Tests/fixtures can now fail for the defect (they exercise the filter, not bypass it) | PASS | Step 2: raw fixtures (:207), raw pages of 100 with 40 label events through the real filter (:208, :283, :295), plus the "n == 100 but short items, then n < 100" case |
| 5 | No contradiction introduced between Section 4 gaps, Section 7 recommendation and Section 8 plan, or inside Section 8 | PASS | Step 3: 11 places in synth-04 use one rule; synth-01..03 contain no page-cap statement and were not edited in cycle 2 (mtimes) |
| 6 | Recommendation is option A "decided by the owner", never "pending owner decision" | PASS | Step 4: synth-03:77, :353; synth-01:39; synth-04:7, :399-405; grep "pending owner" = 0 matches |
| 7 | Recommendation still answers the three issue questions | PASS | Step 4: synth-01:21-25 read directly |
| 8 | B and C scored and documented with revisit conditions; Coder#477 sibling dependency with repo boundary and "A makes it unnecessary unless B or C is revisited" | PASS | Step 4: synth-03:280-300, 304-307, 364-368; nine conditions synth-04:364-374; Coder#477 synth-01:47-51, synth-04:7, :353, :376, :409 |
| 9 | External findings supplement and never override verified code | PASS | Step 4: synth-02:180, synth-03:24, synth-04:24, :472; the one non-file fact (oldest-first order) is labelled as a live read-only call |
| 10 | Added text is sourced, tagged and free of placeholders | PASS (with note M1) | Step 5: direct repo reads only, grep for TODO/TBD/FIXME = 0; `[DESIGN]` is not in the tag key (minor) |
| 11 | Sections 1-10 present in order across the four files | PASS | Step 5: heading grep, synth-01 (1, 2), synth-02 (3, 4, 5), synth-03 (6, 7), synth-04 (8, 9, 10) |
| 12 | Fix log claims match the files | PASS | Step 2: all eight edits found at the lines the log names; `still full` = 0 hits in all four files; unchanged items (run_cycle rows 5-6 mapping, `max_pages = 5` [PROPOSAL]) confirmed unchanged in meaning |

## Summary
- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Blocking (IMPORTANT) issues: 0 (the one blocking cycle-1 finding is resolved; no new blocking finding)
- Minor notes: 5 (M1-M5, not rechecked in later rounds, never fail the review)
- Issues fixed in-place: 0 (report only; no synthesis file modified)
- Confidence: Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 12 | Grep: 12 | Glob: 0 | Bash: 6 (Read + Grep + Glob = 24 >= 12 items)
- Web research: none performed (no Tavily, WebSearch or WebFetch call; no external lookup was needed; the only non-local action was running `jq` on inline samples)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| M1 | MINOR | synth-04:198, :208, :295 vs the tag key at :24 | `[DESIGN]` tag is used but not defined in the key (key lists CODE-VERIFIED, CODE-CONTRADICTED, EXTERNAL-VERIFIED, UNVERIFIED, PROPOSAL, DERIVED) | Add `[DESIGN]` (logic of the plan itself) to the key, or use [PROPOSAL] |
| M2 | MINOR | synth-04:208 (step 4.5), :283, :295, Q32 :449 | Unit-level `FakeRunner` now needs the `jq` binary; only the E2E tests have a skip rule and Q32 mentions only E2E | Add "skip when `shutil.which("jq")` is None" (or fail with a clear message) to step 4.5 and extend Q32 to the unit tests |
| M3 | MINOR | synth-04:208, :295 | Tests run the `jq` binary while `gh --jq` runs gojq | One sentence noting the engines and that the live test (checklist item 3 or 7) should confirm the `{n, items}` output once |
| M4 | MINOR | synth-04:205 | A complete list of exactly `max_pages * 100` items raises `E-GH-TRUNCATED` (page 5 has `n == 100`); safe direction, unstated | State it next to `max_pages = 5` |
| M5 | MINOR | synth-04:298 (criteria) | No acceptance criterion names the fail-closed truncation behavior | Add: "a truncated approval or claim-marker read selects no issue and starts no session" |

The cycle-1 minor notes (synth-03:290 R9 wording, synth-03:306 R2 wording, synth-02:138 "row G2" label, synth-03:278 rule sentence) and the Phase 5 notes M1-M13 are unchanged notes and were not rechecked.

## Actions Taken
None. Fix authorization is false; no synthesis file was modified. The only file written is this report.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` block was in the spawn prompt, and the sibling cycle-2 structural report was an unfinished 318-byte stub, so I ran standalone and relied on no rf-qa PASS item.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied. The fix log's statements ("FIXED", line numbers, grep results) were treated as claims to test, not as evidence. The unchanged state of synth-01..03 was established by `stat` mtimes, not by trusting the log.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Filter semantics - executed `events-jq` and `marker-jq` in jq 1.7 on raw sample pages (Bash) and confirmed `n` is the raw length and `items` the filtered list; this is the behavior the whole fix rests on and no document read could show it.
- Guard-can-fire trace - traced a raw page of 100 events holding 40 label events through the new call, step 4.2 and the "Truncated read" row; the old guard read 40 items as the list end, the new one reads `n == 100` and continues.
- Precedent lines - read `poll-augment-review.sh:36-85` and matched `:47`, `:51`, `:69-70`, `:74` to the claims in synth-04:190/198/205.
- Counts - recounted the Meets labels in the scoring table (A 2, B 1, C 0, D 2) against the Tally; counted nine revisit conditions in synth-04:364-374.
- Cross-file sweep - grepped all four files for the superseded phrase (`still full`: 0), pagination/cap/error-code tokens, "pending owner", Coder#477, placeholders.

1. Factual claims independently verified: about 40 (eight fix locations, five script lines, three jq outputs, tally, nine conditions, section headings, mtimes, decision labels).
2. Files read: synth-04 lines 1-554 in full, synth-01:17-52, synth-03:276-308 and :349-371, `poll-augment-review.sh:36-85`, the consolidated findings, the fix log, the cycle-1 content report, `research-notes.md`; grep passes over all four synthesis files and `research/`.
3. This review did not find 0 issues: it found no blocking issue and five minor notes. The user can trust the PASS because the fix's central claim (the guard now fires on real data) was tested by running the filters, not only by reading the text, and because every cross-file claim was re-grepped in this session.
4. No web research was performed, so no Tavily versus fallback decision arose.

## Recommendations
- Proceed. The cycle-2 blocking finding is resolved and no new blocking finding was introduced. This was the third review of Gate 2 (cycle 1 content FAIL, cycle 2 content PASS); no further fix cycle is needed.
- Optional, no gate: apply M1-M5 as one-sentence edits in synth-04 when the report is assembled.

## QA Complete

VERDICT: PASS
