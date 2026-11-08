# QA Report — Phase 3 Content Verification (report-qualitative, fix-cycle)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative lens on research files 01, 02, 03)
**Fix cycle:** 1
**Fix authorization:** false (report only)
**Status:** Complete

---

## Progress log (appended incrementally)

### Step 1 - inputs read
- Read in full: consolidated findings (12 findings, 3 blocking: #1 routing/dedupe contradiction, #2 poller host/state gap, #3 CCSESSION_PERMISSIONS claim), fix log, research files 01/02/03 (post-fix), research-notes.md, and the three source gate reports (qualitative F1/F2, evidence B1, analyst PASS) to check that no blocking item was dropped during consolidation.
- Consolidation fidelity: qualitative F1 -> consolidated #1; qualitative F2 -> #2; evidence B1 -> #3; analyst had 0 blocking. Qualitative M1-M5 and evidence m1-m3 map to minors #4-#11. No blocking item was downgraded or lost. VERIFIED.
- `md5sum research-notes.md` = d2671ff214db5ce006c8a5f46e99896b, identical to the fix log's before/after value (Bash, this session). VERIFIED.

### Step 2 - blocking finding #3 (CCSESSION_PERMISSIONS) re-verified against sources: RESOLVED
- `ccsession:119-141` read: default flags `--dangerously-skip-permissions --allowedTools=Grep`; `CCSESSION_PERMISSIONS=default` gives `--allowedTools=Grep`; `CC_CLAUDE_FLAGS` replaces the default. Matches file 03 s2.2.
- `ccsession-tag/README.md:534` read: "flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply"; `:535` CC_CLAUDE_FLAGS replaces flags. Matches the amended file 03 text.
- `orca-data.json` (grep): `agentDefaultArgs.claude` = `--dangerously-skip-permissions`; `agentCmdOverrides` = `{}`. Matches file 01 s11 and file 03 s2.2.
- `/opt/Orca/.../shared/agent-launch-profile.js` (userArgs = input.userArgs ?? settings.agentDefaultArgs[agent] ?? YOLO fallback when nothing typed) and `tui-agent-permissions.js:16` (`claude: '--dangerously-skip-permissions'`). Matches the cited lines.
- All four places named by the finding (s2.2 row, s2.3 bullet, s2.3 takeaway, Gap 5) plus the Summary and file 01 s11 now agree. Substantive, not cosmetic. The un-traced step (does the `orca agent launch` route use the profile) is honestly tagged [UNVERIFIED].

### Step 3 - blocking finding #2 (poller host and dispatch record): RESOLVED as a recorded gap, one follow-up
- File 01 s7 takeaway now carries an [UNVERIFIED] tag; new Gap 9 (01 line 267) and Gap 15 (03 line 222) list scheduler availability, survival across autostop/restart, durable state location and a stopped workspace not polling. File 03 s5 (line 150) carries the same tag. Grep for cron|systemd|shell loop|user loop|autostop over 01-03 shows every remaining assertion sits next to the tag. Honest: both gaps say no Coder documentation was checked.
- Follow-up (minor, see M-A): the gaps assign the question to web-02, but web-02's spawn prompt (task file line 229) only asks for autostop/autostart "for a watcher that must reach a stopped workspace" plus `coder_script` cron/run_on_start. It does not ask whether a poller process survives a stop, or where durable state lives. The assignment is therefore only partly backed by an actual task.

### Step 4 - blocking finding #1 (routing/dedupe contradiction): original contradiction resolved, but the new section 2c contradicts itself (NEW BLOCKING N1)
- Source facts re-read: `refs/claim.md:41-42,47` (stop on a different assignee; continue and idempotent for the own login; Wave 3 `--add-assignee @me`). `gh issue list --help` run this session shows `--assignee`, `--type`, JSON fields incl. `issueType`/`projectItems`, example `--assignee "@me"` at help line 48 and `no:assignee` at line 50 (matches 02 s2c). `research-notes.md:108-112` read: ADDENDUM 2 says each workspace polls every 5 minutes with its own `gh` login and names no routing candidate (matches 02 s2c).
- Cross-file pointers verified present: 01 line 165, 02 section 2c (lines 65-80), 03 line 139; line anchors cited in 2c (01 line 148/150/155, 03 line 134) are correct.
- The three-way contradiction of the original finding (02 "skip assigned" vs 01/03 "select assigned to me") is gone: the single predicate is "skip an issue assigned to a login other than the own login", and the per-candidate table is consistent with claim.md:41-42.
- BUT the reconciling section is not internally consistent:
  - 02 line 70 says "'Skip assigned' therefore applies only to issues assigned to someone else, never to issues assigned to the workspace's own login." A shorter form ("skip assigned applies only to issues assigned to someone else", without the word "never") is repeated as the pointer at 01 line 165 and 03 line 139.
  - 02 line 77 (table row 4, candidate 4) says "The issue must be unassigned; skip anything already assigned, to the own login or another."
  - These two statements cannot both be the rule for candidate 4: "never skip own-login-assigned" versus "skip anything already assigned, to the own login".
  - 02 line 79 then says that under candidate 4 the dispatch record carries the retry cap because "a claim that fails after Wave 3 leaves the issue assigned to the own login (file 01 section 10 line 172)". Under candidate 4 the selector is "no assignee", so an issue left assigned to the own login after a Wave 3+ failure is never selected again: it is stranded, not retried. File 01 line 173 (the cited passage) says the re-select-every-cycle consequence applies to "a poller using candidate 1". The cause named for candidate 4's retry cap is therefore wrong; the true candidate-4 cause is a pre-Wave-3 failure (for example `E-TIER-UNAVAILABLE`, 01 line 38), and the stranded post-Wave-3 case is not mentioned at all.
  - 02 line 79 also calls "skip assigned" and "select assigned to me" "the same rule seen from two sides" under candidate 1. They are not the same: skipping others' issues admits unassigned ones; selecting own-assigned excludes them.
- This is new content added by the fix, in the exact section whose purpose is to give one unambiguous rule, and a synthesis reader who takes the one-line pointer sentence (repeated in 01 and 03) will get the wrong rule for candidate 4. Graded IMPORTANT (blocking) under Critical Rule 6 (contradictions are never minor).

### Step 5 - cross-file contradiction scan after the fixes (check b)
- Permission posture: 01 line 190, 03 lines 67/70/77/212/233 now agree (bypass comes from ccsession default, `CC_CLAUDE_FLAGS`, or Orca's `agentDefaultArgs`; `CCSESSION_PERMISSIONS=default` alone is not sufficient). No contradiction.
- Poller host: 01 lines 130/267 and 03 lines 150/222 carry the same [UNVERIFIED] list (a)-(d). No contradiction.
- Routing/dedupe: contradiction between files removed; internal contradiction inside 02 s2c remains (N1).
- Known pre-existing items re-seen and left as notes (not introduced by the fixes): 03 Gap 4 still treats `--prefill` as open although 01 s12 shows `delivery: 'submit'` (request.js:63-64 re-checked this session: `{ prompt: { text: prompt, delivery: 'submit' } }`); 03 line 192 says duplicate launches are "not harmful" while 01 line 159 and 177 say concurrent same-login runs both post new comments.

### Step 6 - proportionality, tagging and gap honesty (checks c, d)
- Section 2c is about 16 lines for a 3-way contradiction; every claim carries a claim.md or help-text citation or an [UNVERIFIED] tag (multi-assignee behaviour, exact query form, whether a later owner decision names a candidate). Proportionate.
- Fix 3 adds Orca-code claims with file:line (re-read, correct) and tags the one untraced link [UNVERIFIED]. Proportionate. Summary-level sentences (03 line 77 and 233) restate "Orca's default flag still applies" without the [UNVERIFIED] hedge of s2.2/s2.3 (note M-B).
- Gap lists: 01 Gap 9 and 03 Gap 15 are honest ("no Coder documentation checked"). 02's Gaps list was not extended for the new inline [UNVERIFIED] items of s2c (multi-assignee, query form); they remain visible inline (note M-F).
- research-notes.md untouched (md5 above). The fix log's line-count claims (01 288->290, 02 211->228, 03 231->233) are consistent with what Read shows.

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | (a) Blocking #1 (routing/dedupe contradiction) addressed substantively | PASS | 02 s2b amended (lines 57, 63), new s2c, pointers at 01:165 and 03:139; claim.md:41-42,47 and `gh issue list --help` re-checked; the original 02-vs-01/03 contradiction is gone |
| 2 | (a) Blocking #2 (poller host/state gap) addressed substantively | PASS | [UNVERIFIED] tags at 01 s7 / 03 s5; new Gap 9 (01:267) and Gap 15 (03:222); grep over 01-03 shows no untagged cron/systemd assertion. Follow-up M-A on web-02 prompt |
| 3 | (a) Blocking #3 (CCSESSION_PERMISSIONS) addressed substantively | PASS | ccsession:136-141, README:534-535, orca-data.json, agent-launch-profile.js, tui-agent-permissions.js:16 all re-read; four named places plus Summary and 01 s11 agree |
| 4 | (a) No blocking finding lost in consolidation | PASS | Qualitative F1/F2 and evidence B1 map to consolidated #1/#2/#3; analyst had none; minors M1-M5/m1-m3 map to #4-#11 |
| 5 | (b) Fixes introduced no contradiction between or within the research files | FAIL | N1: 02 line 70 ("never ... own login") vs 02 line 77 (candidate 4 "skip anything already assigned, to the own login"); 02 line 79 attributes candidate-4's retry cap to a post-Wave-3 failure that candidate 4 never re-selects (01:173 says that consequence belongs to candidate 1) |
| 6 | (c) Added content proportionate to evidence | PASS | s2c, Gap 9/15, 03 amendments each cite file:line or carry [UNVERIFIED] |
| 7 | (c) Doc-sourced claims remain tagged | PASS (note M-B) | README:534 claim is cited and the untraced `orca agent launch` link is tagged in s2.2/s2.3; the Summary/Key Takeaway lines drop the hedge |
| 8 | (d) Gaps sections remain honest | PASS (notes M-A, M-F) | Gap 9 and Gap 15 state that no Coder documentation was checked; no gap was closed without evidence |
| 9 | research-notes.md not edited | PASS | md5 d2671ff214db5ce006c8a5f46e99896b before and after |
| 10 | Cross-file anchors cited by the fixes are correct | PASS (note M-E) | 01:148/150/155 and 03:134 correct; "01 section 10 line 172" is line 173 after the fix shifted the file (moved line on a true claim) |

## Summary
- Checks passed: 9 / 10
- Checks failed: 1 (check 5)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 1 (N1)
- Issues fixed in-place: 0 (report only)
- Blocking findings from the consolidated list: 3 of 3 resolved (#1 resolved in substance, #2, #3). One new blocking finding introduced by the #1 fix.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N1 | IMPORTANT (blocking, new) | `research/02-github-surface-and-cli-patterns.md` lines 70, 77, 79 (and the one-line pointers at `research/01-...md:165`, `research/03-...md:139`) | Section 2c, written to give one rule, says "skip assigned" applies "never to issues assigned to the workspace's own login" (line 70) while its own candidate-4 row says to skip anything already assigned "to the own login or another" (line 77). Line 79 also says candidate 4's dispatch record carries a retry cap because a claim that fails after Wave 3 leaves the issue assigned to the own login; under candidate 4 such an issue is never re-selected (stranded), and 01:173 ties the re-select-every-cycle effect to candidate 1. Line 79 also calls "skip assigned" and "select assigned to me" the same rule from two sides, which they are not (one admits unassigned issues) | In 02 s2c: (1) in line 70 separate the two things: "the claim-stop pre-filter skips only issues assigned to a login other than the own login; candidate 4's selector (no assignee) separately excludes every assigned issue, including own-login ones"; (2) in line 79 replace the Wave-3 parenthetical with the true cause for candidate 4 (a failure before Wave 3 such as `E-TIER-UNAVAILABLE`, 01:38, leaves the issue unassigned and re-selected every cycle) and add that a failure after Wave 3 strands the issue (assigned to the own login, no claim comment, never re-selected under candidate 4; re-selected every cycle under candidate 1, 01:173); (3) delete or correct "the same rule seen from two sides"; (4) align the pointer sentences at 01:165 and 03:139 to the corrected wording. Tag nothing new beyond what is already [UNVERIFIED] |

### Minor notes (never fail the review, not rechecked later)
| # | Location | Note |
|---|----------|------|
| M-A | task file line 229 (web-02 prompt) vs 01 Gap 9 / 03 Gap 15 | The gaps are assigned to web-02, but its prompt asks only about autostop "for a watcher that must reach a stopped workspace" and `coder_script` cron/run_on_start. Add "does a poller process survive stop/start and where does durable state live" to the web-02 prompt so the assignment is real |
| M-B | 03 lines 77 and 233 | Summary-level sentences say Orca's default `--dangerously-skip-permissions` "still applies" under `CCSESSION_PERMISSIONS=default` without the [UNVERIFIED] qualifier that the `orca agent launch` route was not traced (s2.2, s2.3). Locally Orca runs plain `claude` (`agentCmdOverrides` is `{}`), so ccsession is not even in the local path |
| M-C | 03 line 192 vs 01 lines 159 and 177 | 03 says duplicate launches are "not harmful because of the idempotent re-claim"; 01 says concurrent runs by one login both post new comments. Pre-existing, complementary but overstated in 03 |
| M-D | `qa/analyst-completeness-report.md` Important gap 2 (and consolidated finding #12's "compiled into gaps-and-questions.md") | The analyst's compiled gap still reads "stalled in default mode, unrestricted under ccsession's bypass default", the wording finding #3 corrected. Whoever compiles gaps-and-questions.md must take the permission wording from 03 Gap 5, not from the analyst list |
| M-E | 02 line 43 and Gap 2 | `gh issue list --help` (run this session) lists JSON field `issueType`, `projectItems`, and a `--type name` flag, so the "unverified field name" caveat can be closed. Cross-reference "01 section 10 line 172" in 02 s2c is line 173 |
| M-F | 02 Gaps list | The new inline [UNVERIFIED] items in s2c (GitHub multi-assignee behaviour, exact query form) are not in the numbered Gaps list. 02 line 224 still says `feature_request.yml` has Orca placeholders (known minor, false) |
| M-G | known carried minors | 03 Gap 4 (`--prefill` open) vs 01 s12 (`delivery: 'submit'`, re-checked); 01 Gap 6 (tests do not pin the stop text; Grep of `test_issue*.py` shows no hit); off-by-one line-count headings |

## Actions Taken
None (fix_authorization: false). Only this report was written.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was supplied in the prompt, so standalone behaviour applied. Reliance list below is therefore limited to the earlier gate reports' read-only observations that I did not repeat.

## Self-Audit

**(a) Reliance list - rf-qa / earlier-gate PASS items skipped for structural re-check:**
- Relied on the evidence gate's citation sweep (about 300 file:line anchors in 01/02/03, `qa/qa-research-evidence-report.md`) for anchors I did not touch; I re-read only the anchors that the fixes added or changed.
- Relied on the analyst's coverage matrix (`qa/analyst-completeness-report.md` Checklist 1) for scope coverage; the fixes add no new scope.
- Did not read `qa/qa-verification-phase3-structural.md` (the sibling structural check of this same cycle); structure is out of this report's lens.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Permission-mode claim after fix 3 -- verified by Read `ccsession:110-155` (lines 136-141), Read `ccsession-tag/README.md:532-535`, Bash grep of `orca-data.json` (`agentDefaultArgs.claude`, `agentCmdOverrides:{}`), Bash sed of `/opt/Orca/.../agent-launch-profile.js` and `tui-agent-permissions.js:16`.
- Routing rule after fix 1 -- verified by Read `refs/claim.md:10-55` (lines 41, 42, 47), Bash `gh issue list --help` (lines 48, 50, `--assignee`, `--type`, `issueType`), Read `research-notes.md:99-112`, then a logical walk of every row of 02 s2c against 01 s9/s10 (found N1).
- Poller-host gap after fix 2 -- verified by Grep for cron|systemd|shell loop|user loop|autostop across 01-03, Bash `sed`/`grep` of the task file's web-02 prompt (line 229) to test whether the assignment is backed by a task (found M-A).
- Consolidation fidelity -- verified by Read of all three source gate reports against the consolidated table.
- Live-state claims touched by the security reading -- Bash `gh repo view` (PUBLIC, not private, fork), `gh api .../collaborators` (1 admin, 2 maintain, 8 read), `gh label list` (9 defaults), Grep `request.js` (`delivery: 'submit'`), Grep `WORKER-CONTRACT.md` (lines 11, 23, 39, 40, 61, 93, 112). All matched.

If I had reported 0 issues the user should not have trusted it: the one blocking defect (N1) only appears when the rows of the new table are compared against the sentence that summarises them and against file 01 line 173, which is a logical check no citation sweep would catch.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 12 | Glob: 1 | Bash: 5 (all read-only: md5sum, ls, wc, sed, grep, `gh` help/api/view/label list)
**Web research:** none performed. tavily_search: 0 | tavily_extract: 0 | fallback: 0.
Tool calls (27) exceed the checklist items (10), so the minimum-engagement rule is met.
UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations
1. Fix N1 in `research/02-github-surface-and-cli-patterns.md` (lines 70 and 79) and align the two pointer sentences (`01:165`, `03:139`). This is a four-sentence edit; it needs no new research.
2. Then run one targeted re-review limited to N1 (this was review 2 of at most 3).
3. Carry M-A into the web-02 prompt and M-D into the gaps compilation, in the same pass; neither blocks.

## QA Complete

VERDICT: FAIL

