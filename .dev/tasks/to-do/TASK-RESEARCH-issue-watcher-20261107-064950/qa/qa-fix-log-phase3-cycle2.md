# Fix log: Phase 3 research gate, fix cycle 2

**Date:** 2026-11-07
**Agent:** rf-qa (fix_authorization: true)
**Inputs:** `qa/qa-consolidated-findings-phase3-cycle2.md` (1 blocking finding), `qa/qa-verification-phase3-content.md` (finding N1)
**Files edited:** research 01, 02, 03 (targeted Edit calls only). `research-notes.md` not touched.
**Status:** Complete

---

## Finding 1 (IMPORTANT, blocking): section 2c of file 02 states incompatible routing rules

Sources read this session for every added statement: `src/superclaude/skills/sc-issue-protocol/refs/claim.md` lines 1-60 (line 20 "No GitHub or ClickUp write happens before Wave 3"; line 41 assigned to another login -> STOP; line 42 assigned to the current login -> continue; line 47 Wave 3 `--add-assignee @me`); research 01 lines 38 (`E-TIER-UNAVAILABLE` stops before any GitHub write, issue stays unassigned), 150-165 and 172-173 (post-Wave-3 failure leaves the issue assigned to the own login, re-selected every cycle under candidate 1); research 02 lines 68-82; research 03 lines 134-139.

Edits made (all Edit calls, no rewrite):

1. `research/02-github-surface-and-cli-patterns.md` section 2c, "Single predicate" bullet (line 70): removed the sentence `"Skip assigned" therefore applies only to issues assigned to someone else, never to issues assigned to the workspace's own login.` and replaced it with a statement that the claim-stop pre-filter (claim.md:41-42) skips only issues assigned to someone else and is separate from a candidate's own selector: candidate 1 requires the own login, candidate 4 (no assignee) excludes every already-assigned issue, own login included; so the pre-filter is not identical to either candidate's filter. Cites `gh issue list --help` lines 48 and 50 (already read and cited earlier in the same section).
2. Same file, table row 4 (line 77): the "Role of the assignee check" cell now says the unassigned requirement is candidate 4's own selector, stricter than the claim-stop pre-filter, so the row and the line-70 sentence no longer read as contradictory.
3. Same file, "Consequence for the plan" bullet (old line 79) replaced by two sub-bullets (lines 80-81): candidate 1 (post-Wave-3 failure leaves the issue assigned to the own login with no claim comment, re-selected every cycle, retry cap needed, 01 line 173); candidate 4 (pre-Wave-3 failure such as `E-TIER-UNAVAILABLE`, 01 line 38 and claim.md:20, leaves the issue unassigned and re-selected every cycle, retry cap needed; a post-Wave-3 failure strands the issue because the candidate-4 selector excludes it, so the dispatch record is needed to notice and report the abandoned claim). Deleted the incorrect "the same rule seen from two sides" wording. Corrected the cross-reference "file 01 section 10 line 172" to line 173 (the cited sentence is at 01:173). The trailing owner-decision sentence (research-notes.md:108-112, [UNVERIFIED] tag kept) was split into its own bullet.
4. `research/01-claim-flow-and-session-launch.md` section 9 Key Takeaways, reconciliation pointer (line 165): dropped the "'skip assigned' applies only to issues assigned to someone else" tail and added the corrected wording (candidate 4 excludes every already-assigned issue; post-Wave-3 failure strands such an issue under candidate 4 but re-selects it under candidate 1, section 10 line 173; the claim-stop pre-filter, claim.md:41-42, is the claim's own rule and not identical to either filter).
5. `research/03-governance-and-security-surface.md` section 4.3 reconciliation pointer (line 139): same replacement, citing `claim.md:41-42`.

Verification of the fix:
- Grep over research 01-03 for `same rule seen|never to issues assigned|applies only to issues assigned|section 10 line 172` returns no match.
- Read back of 02 lines 68-83 after the edits shows line 70, row 4 (line 77) and the two candidate sub-bullets (lines 79-81) consistent: the pre-filter is "not assigned to someone else"; candidate 1 requires own login; candidate 4 requires no assignee.
- Structure intact: 02 still has its Status, Summary, Gaps and Key Takeaways headings (Grep count 10 for those headings); no heading was touched.

No new research agent was needed (the finding required no new investigation). No new [UNVERIFIED] item was introduced; the existing tags (multi-assignee behaviour, query form, whether a later decision names a candidate) are unchanged.

Not fixed (by instruction, minors stay notes): M-A to M-G of the cycle-1 content report.

