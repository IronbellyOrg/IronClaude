# QA Report — Phase 3 Research Gate, Fix Cycle 2 (Structural)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 2
**Fix authorization:** false (report only)
**Status:** Complete

---

## Overall Verdict: PASS (0 open blocking findings; 3 minor notes)

---

## Inputs

- Cycle-1 structural report: qa/qa-verification-phase3-structural.md
- Cycle-1 content report: qa/qa-verification-phase3-content.md
- Cycle-2 consolidated findings: qa/qa-consolidated-findings-phase3-cycle2.md
- Cycle-2 fix log: qa/qa-fix-log-phase3-cycle2.md
- Research files: research/

## Checks (appended incrementally below)

Inputs read in full this session: cycle-2 consolidated findings (1 blocking, 0 minor), cycle-2 fix log, both cycle-1 verification reports, research files 01 (290 lines), 02 (231), 03 (233), `refs/claim.md` lines 15-91, `research-notes.md` lines 83-113. Every source cited by the fix was re-read independently, not taken from the fix log.

### Check A: the one blocking finding of the cycle-2 consolidated list (section 2c of file 02 states incompatible routing rules) - RESOLVED

Sub-checks, each against the current file text:

- A1 (line 70, "Single predicate"): the sentence "never to issues assigned to the workspace's own login" is gone (Grep for `never to issues assigned|applies only to issues assigned|same rule seen|section 10 line 172` over research/0*.md: no hit in any of the three files). Line 70 now says the claim-stop pre-filter (claim.md:41-42) skips only issues assigned to someone else, that candidate 1's selector requires the own login, that candidate 4's selector (no assignee) separately excludes every already-assigned issue including the own login, and that the pre-filter is therefore not identical to either candidate's filter. This no longer conflicts with row 4. RESOLVED.
- A2 (table row 4, line 77): "The issue must be unassigned (candidate 4's own selector, stricter than the claim-stop pre-filter): skip anything already assigned, to the own login or another". Consistent with line 70 and with row 2/3 ("Pre-filter only: skip when assigned to another login; accept unassigned or own") and row 1 ("Required: the issue MUST be assigned to the own login"). The three rows plus line 70 now form one coherent statement. RESOLVED.
- A3 (retry-cap cause, lines 80-81): candidate 1 is tied to a failure after Wave 3 (`E-WORKER-NO-OUTPUT` or `E-POST-FAILED`) that leaves the issue assigned to the own login, re-selected every cycle, citing 01 line 173; I read 01:173 and it says exactly that for "a poller using candidate 1". Candidate 4 is tied to a failure BEFORE Wave 3 (`E-TIER-UNAVAILABLE`), citing 01 line 38 and `claim.md:20`; I read 01:38 (E-TIER-UNAVAILABLE stops before any GitHub write, issue stays unassigned) and claim.md:20 ("No GitHub or ClickUp write happens before Wave 3"): both match. The post-Wave-3 failure under candidate 4 is now stated correctly as stranded (excluded by the candidate-4 selector). The example `E-WORKER-NO-OUTPUT` is a valid post-Wave-3 case: claim.md:62 (Wave 4 worker returns no file, retry once, then STOP `E-WORKER-NO-OUTPUT`). RESOLVED.
- A4 ("the same rule seen from two sides"): deleted (Grep above: no hit). RESOLVED.
- A5 (pointer sentences): 01 line 165 and 03 line 139 were re-read; both now say candidate 1 selects assigned-to-me, candidate 4 selects unassigned and so excludes every already-assigned issue (own login included), the claim-stop pre-filter (claim.md:41-42) is the claim's own rule and not identical to either filter, and both point at 02 section 2c. 01:165 also carries "a post-Wave-3 failure strands such an issue under candidate 4 but re-selects it every cycle under candidate 1, section 10 line 173", which matches 02 lines 80-81 and 01:173. The quoted phrase in 03:139, "a rule that the issue must be assigned to its own login", is a substring of 03:192 (read). RESOLVED.
- Extra: the "file 01 section 10 line 172" cross-reference (a cycle-1 minor note) was corrected to line 173 as a side effect; the sentence is at 01:173 (read).

Result: finding 1 is resolved in substance, not cosmetically. PASS.

### Check B: no new blocking issue (false claim, contradiction, missing path, untagged doc claim, broken structure) introduced by the cycle-2 fixes - PASS

- False claims: every statement added in cycle 2 was traced: claim.md:20, :41, :42, :47, :62 (read); 01:38, 01:173, 01:155 (read); `gh issue list --help` run this session: line 20 `-a, --assignee string`, line 48 `$ gh issue list --assignee "@me"`, line 50 `$ gh issue list --search "error no:assignee sort:created-asc"` (matches the "lines 48 and 50" cite in 02:70, 75, 77); `research-notes.md:108-112` (ADDENDUM 2: option A, 5-minute polling with the workspace's own `gh` login, claim-only, integer-only; no routing candidate named): matches 02:82. None is contradicted.
- Cross-file contradictions: the routing/dedupe rule now reads the same in 02 (lines 70-83), 01 (lines 150, 153, 165, 173) and 03 (lines 134, 139, 192). The 02 Key Takeaways (2b) line 63 ("skip only issues assigned to someone else ... must not skip issues assigned to its own login when routing is by assignee") is the claim-stop pre-filter and is consistent with line 70.
- Untagged doc claims: no new doc-sourced claim was added without a tag; the tags that already existed in section 2c (multi-assignee behaviour on GitHub at row 4, whether a later decision names a candidate at line 82) are still present. The fix introduced no new unverified item.
- Broken structure: no heading removed or reordered; line counts 01: 290, 02: 231, 03: 233 (`wc -l`), matching the expected +3 lines in 02 (one bullet replaced by a header bullet plus two sub-bullets, plus the owner-decision sentence split into its own bullet at line 82); 01 and 03 unchanged in length (single-bullet replacement).
- Internal anchors in 02 2c resolve: "01 section 9, table at line 148" (01:148 is the candidate table header, read), "01 line 150/155", "03 line 134" (03:134 is the assignee row, read).

### Check C: every research file still has Status: Complete, Summary, Gaps and Questions and Key Takeaways - PASS

Grep for `^#{1,3} (Summary|Gaps and Questions|Key Takeaways)|^Key Takeaways|^Status: Complete` over research/0*.md:

| File | Status: Complete | Key Takeaways | Gaps and Questions | Summary |
|---|---|---|---|---|
| 01 | line 4 | plain "Key Takeaways" blocks at lines 29, 47, 66, 78, 97, 111, 127, 161, 176, 198, 240, 252 | line 256 | line 287 |
| 02 | line 4 | `### Key Takeaways` at 26, 48, 61 (2b), 126, 158, 171, 192, 206 | line 210 | line 229 |
| 03 | line 4 | `### Key Takeaways` at 41, 75, 105, 141, 156, 181, 197 | line 204 | line 231 |

All present, same format as before the fix. (Section 2c of file 02 has no Key Takeaways block of its own; it had none when cycle 1 passed it and the file as a whole carries them, so this is a minor note only.)

### Check D: every newly added claim cites an existing file and line - PASS

Cited and re-read this session: `claim.md:20`, `:41`, `:42`, `:47`, `:62`; `01-claim-flow-and-session-launch.md:38`, `:148`, `:150`, `:155`, `:165`, `:173`; `03-governance-and-security-surface.md:134`, `:139`, `:192`; `research-notes.md:108-112`; `gh issue list --help` lines 48 and 50. Every cite resolves to the content described. The replaced cross-reference "01 section 10 line 172" no longer exists (Grep: no hit); the correct line 173 is used.

### Check E: `research/research-notes.md` untouched - PASS

`md5sum` = `d2671ff214db5ce006c8a5f46e99896b`, identical to the value recorded in both cycle-1 verification reports and the cycle-1 fix log. The cycle-2 fix log also states it was not touched.

### Check F: halt-guard statements in the cycle-2 consolidated findings - PASS

The consolidated file says no regression (the three original blocking findings are confirmed resolved: cycle-1 structural report checks A1-A3 and cycle-1 content report steps 2-3 both say RESOLVED; I found no re-opening of any of them in the current text: the permission-mode wording in 03:67/70/77/212/233 and 01:190 and the poller-host [UNVERIFIED] gaps 01 item 9 (line 267) and 03 item 15 (line 222) are all intact) and open blocking 3 before, 1 now, so |F| shrank. Both statements match the evidence I read.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (note) | `research/02-github-surface-and-cli-patterns.md` line 70 | The bullet is titled "Single predicate the evidence supports" and opens "the poller must skip an issue assigned to a login OTHER than its own", then says the predicate is not identical to either candidate's filter. Readable and not contradictory, but the title promises one rule while the text describes a claim-stop pre-filter plus per-candidate selectors | none required |
| 2 | MINOR (note) | `research/02-github-surface-and-cli-patterns.md` section 2c | No `Key Takeaways` block for section 2c, and the numbered Gaps list (item 10 covers race behaviour only) does not list the two inline [UNVERIFIED] items of 2c (multi-assignee behaviour, query form); they remain visible inline | none required |
| 3 | MINOR (note) | `research/02-github-surface-and-cli-patterns.md` line 43 | Pre-existing carried note: `issueType` is listed as unverified although `gh issue list --help` lists it among JSON fields | none required |

No blocking issue found. Previously open blocking findings: 1 (cycle-2 consolidated finding 1), now resolved. New blocking findings: 0.

## Summary

- Checks passed: 6 / 6 (A, B, C, D, E, F; A has five sub-checks A1-A5, all passed)
- Checks failed: 0
- Blocking issues open: 0
- Minor notes: 3 (not rechecked in later rounds)
- Issues fixed in-place: 0 (fix authorization false)

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 11 | Grep: 2 | Glob: 1 | Bash: 1 (each call targeted a specific check above; Read+Grep+Glob = 14 >= 6 checks). Web research: none (tavily_search: 0 | tavily_extract: 0 | fallback: 0).

**Self-audit:** a "0 blocking" result is backed by independent re-reads of the five claim.md lines and six file-01 lines the fix cites, a live `gh issue list --help` check of the two help-text cites, a repo-wide Grep proving the three wrong phrasings are gone, a heading Grep for the required structure, an md5 and `wc -l` check, and a row-by-row logical walk of the 2c table against file 01 candidates 1 and 4 and against 01:173 (the walk is what exposed the cycle-1 defect, and this time it finds the table, line 70, lines 80-81 and both pointers consistent). I looked for new defects (a wrong failure-stage for the candidate-4 example, an example error code that fires before Wave 3 under candidate 1, broken anchors, structure loss) and found only the minor notes above.

UNCHECKED items: none. UNVERIFIABLE items: none.

VERDICT: PASS

Status: Complete

## QA Complete

