# QA Report - Phase 5 Synthesis Gate, Fix Cycle 2 (Structural)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** fix-cycle (synthesis-gate re-verification)
**Fix cycle:** 2
**Fix authorization:** false (report only)
**Status:** Complete

---

## Inputs read

- Cycle-1 reports `qa/qa-verification-phase5-structural.md` (VERDICT: PASS, 4 of 4 earlier blocking findings resolved) and `qa/qa-verification-phase5-content.md` (VERDICT: FAIL, 1 blocking finding: truncation guard tests the filtered page length).
- Cycle-2 consolidated findings `qa/qa-consolidated-findings-phase5-cycle2.md`: 1 blocking finding (IMPORTANT), 0 minor listed.
- Cycle-2 fix log `qa/qa-fix-log-phase5-cycle2.md`: claims 8 targeted edits, all in `synthesis/synth-04-plan-questions-evidence.md`.
- Re-read synth-04 lines 1-12, 160-300, 396-412 and the repo precedent `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh` lines 40-84.

## Checks (appended incrementally)

### Check 1 - Cycle-2 blocking finding #1 (truncation guard tested the filtered page length): RESOLVED

Finding asked for: return the raw page length with the filtered items; page while `n == 100`; raise `E-GH-TRUNCATED` when `n == 100` at `max_pages` for both `label_events` and `own_claim_comment_ids`; build test fixtures from raw pages with fewer than 100 label events.

Each element re-read in the file (line numbers as of this read):

- jq filters, lines 194-195: `events-jq : {n: length, items: [...]}` and `marker-jq : {n: length, items: [...]}`. `n` is taken on the raw array before any `select`. Valid jq object construction.
- Rule paragraph, line 198: page-end test uses `n`, never `len(items)`; gives the 100-events/40-label-events example.
- Calls table rows, lines 190-191: Returns column now says per page `{n, items}`.
- Step 4.2, line 205: loop reads page 1, 2, ...; stops with a complete list when `n < 100`; continues while `n == 100`; if page `max_pages` is read and `n` is still 100, both `label_events` and `own_claim_comment_ids` raise `CommandError("E-GH-TRUNCATED")`; never a partial list; an output that is not an object with an integer `n` and a list `items` raises `E-GH-FAILED`. Grep `still full` over `synthesis/`: no hit (the only remaining "full page" style wording is the explanation of why the filtered length cannot be used).
- Step 4.4, line 207: events and comments fixtures are RAW REST pages (before the jq filter).
- Step 4.5, line 208: truncation tests use raw pages of 100 events with 40 label events served through the real filter string as `{n: 100, items: [40 entries]}`; cases for both functions; a raw page with `n == 100` and fewer than 100 filtered items does NOT end the read; `n < 100` ends it. A test now exercises the filter, so a wrong filter fails a test.
- Step 6.1, line 295: the PATH stub pipes the raw fixture page through `jq -c "<filter>"` with the filter it receives, so the real filters run in the e2e tests.
- "Truncated read" scenario, line 283: raw pages of 100 with fewer than 100 label events for every page up to `max_pages` give `approval-unverifiable`; comments give `claim-marker-unverifiable`; a page with `n == 100` and short filtered items followed by `n < 100` is read to its end; a single `n < 100` page is decided normally.
- Downstream wiring unchanged and still consistent: run_cycle row 5 (line 232) maps `E-GH-TRUNCATED` to `approval-unverifiable`; row 6 (line 233) maps it to `claim-marker-unverifiable`; step 4.3 (line 206) says `is_approved` only gets a complete list; Filter 2 row (line 177) says reaching the cap fails closed.

Trace of the original defect case: a raw page of 100 events holding 40 label events now returns `{n: 100, items: [40]}`; the loop sees `n == 100`, continues, and at page 5 with `n == 100` raises `E-GH-TRUNCATED`. A raw page of 100 comments with 0 or 1 marker ids returns `{n: 100, items: [..]}` and behaves the same. A short raw page (`n < 100`) ends the read. The guard can now fire on real data.

Precedent citations verified by my own Read of `poll-augment-review.sh`: `:47` ("fail incomplete at the cap, never silently truncate"), `:51` (`for ((page=1; page<=1000; page++))`), `:53-55` (`--method GET -F per_page=100 -F page=...`), `:69` (`count="$(jq 'length' "$_tmp/rest-page.json")"`), `:70` (`if [ "$count" -lt 100 ]; then completed=true; break; fi`), `:74` (`[ "$completed" = true ] || return 1`). All six cited lines say what synth-04 says. The raw-count precedent is real.

Result: RESOLVED. The guard now works as the finding specified, in every place the finding named.

### Check 2 - No new blocking issue introduced by the cycle-2 fixes: PASS

- Scope of edits: `stat` mtimes: synth-01, synth-02, synth-03 (09:19 to 09:22) are older than the cycle-2 consolidated findings (09:32:59); synth-04 was modified 09:33:59, the fix log 09:34:32; all research files and research-notes.md are 07:34 to 08:50. Only synth-04 changed in this cycle; no research file was edited.
- Fabrication: every new statement is either a code line I read (`poll-augment-review.sh:47,51,53-55,69,70,74`), or the logic of the plan itself, marked [DESIGN] or [PROPOSAL] in the text (lines 198, 205, 208, 295). No external or doc-only claim was added. The one oldest-first claim in the Calls table (line 190) is the cycle-1 observation, already re-run in cycle 1.
- Doc-only claims in Sections 2, 6, 7, 8: none added.
- Table structure: awk pipe count per row (escaped pipes and code spans removed) over synth-04 lines 167-300: all rows of each table have equal counts (7-column filter table rows 174-180; 5-column rows 184-191, 202-208, 217-222, 293-299; 4-column rows 226-240, 246-255; 3-column rows 259-264, 268-284). The edited rows 190, 191, 205, 207, 208, 283, 295 are in the consistent groups. No broken table.
- Placeholders: Grep `TBD|TODO|FIXME|pending owner|owner decision pending|undecided` over `synthesis/`: no match.
- Hallucinated paths: the only new path is `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, which exists (read). New code names `E-GH-TRUNCATED`, `E-GH-FAILED`, `label_events`, `own_claim_comment_ids`, `max_pages` are plan symbols (NEW files), consistent across lines 177, 190-191, 205-206, 208, 232-233, 283. Grep for `max_pages|TRUNCATED` in synth-01, 02, 03: no hit, so no other section describes the old rule.
- Earlier resolved findings did not regress: synth-04 still has the codebase-context correction (line 459, row C4), the "post-write" mentions only as "candidate 4 only, not built" (lines 108, 215), and run_cycle row 8 as the only re-read (line 235). Regression check: no item that passed in cycle 1 fails now.
- Internal consistency of the new rule: step 4.2 (read while `n == 100`, raise at `max_pages` with `n == 100`), step 4.5 (tests), "Truncated read" scenario and step 6.1 (stub) describe the same rule. Edge case: a list of exactly `100 * max_pages` items raises truncation instead of completing; that fails closed, which is the intended direction.

### Check 3 - Four files still cover Sections 1-10 in order: PASS

Heading Grep over `synthesis/`: synth-01 `## 1. Problem Statement` (17), `## 2. Current State Analysis` (55); synth-02 `## 3. Target State` (13), `## 4. Gap Analysis` (102), `## 5. External Research Findings` (178); synth-03 `## 6. Options Analysis` (28), `## 7. Recommendation` (349); synth-04 `## 8. Implementation Plan` (28), `## 9. Open Questions` (397), `## 10. Evidence Trail` (470). Same headings and order as cycle 1; synth-04 heading lines moved by +2 because of the added text.

### Check 4 - Newly added claims trace to a source: PASS (with minor note)

- `poll-augment-review.sh:69-70` and `:74` are new citations. They trace to code I read, not to a research file. Research file `research/02-github-surface-and-cli-patterns.md:105` cites the same script (lines 53-55) so the script is part of the researched surface; the fix agent's instruction said "backed by a research file", and these two citations come from reading the script itself. The statements are true and code-verified, so under the severity rule this is a citation-source note, not a defect (minor note M1).
- All other new text is plan design logic marked [DESIGN] or [PROPOSAL].

### Check 5 - Binding addenda in research-notes.md (ADDENDUM 2): PASS

- Option A "decided by the owner": Grep count of `decided by the owner|Decided by the owner|Binding owner decision`: synth-01 2, synth-02 1, synth-03 3, synth-04 2. synth-04 line 7 ("Binding owner decision (ADDENDUM 2 ...): Q1 = option A") and 9.1 D1 (line 403 area). Grep `pending owner|owner decision pending|undecided`: no match.
- B and C scored and documented with revisit conditions: unchanged from cycle 1 (synth-03 scoring table, Options Comparison, revisit conditions); synth-04 lines 351-352 and the nine revisit conditions table; cycle-2 edit did not touch synth-03.
- Coder#477 with repo boundary and "unnecessary unless B or C is revisited": synth-04 line 7, 95, 103, 351-353, 376, 409 (D5), 482; Grep `unnecessary` finds hits in all four files (8, 3, 5, 3 occurrences in synth-02, 01, 04, 03 respectively, all four files non-zero).
- Integer-only rule: Grep `integer` hits in all four files (synth-02 18, synth-04 22, synth-01 14, synth-03 15); synth-04 D3 (line 91), rule paragraph (line 113), step 3.2 (line 159), step 3.6 (line 163), and the step 4.2 `type(n) is int` check.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | synth-04 line 198 and step 4.2 (line 205) | New citations `poll-augment-review.sh:69-70` and `:74` come from reading the script, not from a research file (the fix prompt asked for research-file backing). Statements are true | None needed; optionally add the script to the Section 10 evidence trail |
| 2 | MINOR | synth-04 step 4.5 (line 208) | The unit-level `FakeRunner` helper now runs the `jq` binary on raw fixtures, but only the e2e stub tests have a `shutil.which("jq")` skip (step 6.1) and open question Q32 covers `jq` for the PATH stub only. `gh --jq` is gh's built-in engine, not the `jq` binary, so a filter could behave slightly differently | Extend Q32 or step 4.5 to say the unit tests need `jq` too, and skip likewise |
| 3 | MINOR | synth-04 line 195 (`marker-jq`) | `.body | contains(...)` errors on a null body in jq. REST issue comments carry a string body, so this is robustness only | Optionally write `(.body // "")` |

No blocking finding is open. Minor notes are not rechecked.

## Summary

- Blocking findings listed in the cycle-2 consolidated findings: 1 of 1 resolved.
- New blocking findings introduced by the cycle-2 fixes: 0.
- Regression of earlier resolved findings: none.
- Minor notes: 3 (above); the cycle-1 minor notes stay notes.
- Checks passed: 5 of 5 (Checks 1 to 5 above).
- Critical issues: 0. Issues fixed in-place: 0 (report only; no file but this report was written).

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (12 items: jq filters; step 4.2 rule; step 4.4 and 4.5 fixtures and tests; "Truncated read" scenario and step 6.1 stub; downstream run_cycle and step 4.3 wiring; six precedent line citations; scope of edits by mtime; table structure; no fabrication, placeholder or hallucinated path; Sections 1-10 order; earlier fixes not regressed; binding addenda).
**Tool engagement:** Read: 8 | Grep: 7 (two further Grep calls failed with `EACCES ... posix_spawn 'rg'` and were redone with Bash `grep`, which is why Bash is counted) | Glob: 1 | Bash: 4 (read-only: `stat`, `awk` column count, `sed`/`grep` reads; no write, no network, no web research, so no tavily or fallback calls). Read + Grep + Glob = 16 >= 12 items.

## Recommendations

- Proceed: the cycle-2 fix resolves the one blocking finding and adds no blocking issue. Minor notes 1 to 3 are optional wording or robustness fixes for whoever assembles the report.

VERDICT: PASS

Status: Complete

## QA Complete

