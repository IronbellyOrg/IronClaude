# QA Report - Phase 3 Content Verification (fix cycle 2)

**Topic:** GitHub issue watcher research (Phase 3 research gate, content quality after fix cycle 2)
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 2
**Fix authorization:** false (report only)
**Status:** Complete

---

## Inputs

- Cycle-2 consolidated findings: qa/qa-consolidated-findings-phase3-cycle2.md
- Cycle-2 fix log: qa/qa-fix-log-phase3-cycle2.md
- Research files: research/01-claim-flow-and-session-launch.md, research/02-github-surface-and-cli-patterns.md, research/03-governance-and-security-surface.md

## Checks (appended incrementally below)

### Step 1 - inputs read (all in full)
- Read the cycle-2 consolidated findings (1 blocking: N1, section 2c of file 02 self-contradiction), the cycle-2 fix log (5 edits), the cycle-1 content report (N1 text and minor notes M-A..M-G), research 01 (290 lines), 02 (231 lines), 03 (233 lines), `refs/claim.md` lines 1-91, `research-notes.md` lines 95-113.
- `md5sum research-notes.md` = d2671ff214db5ce006c8a5f46e99896b (Bash, this session), identical to the value in the cycle-1 content report: research-notes.md untouched by cycle 2.

### Step 2 - check (a): N1 resolved substantively, not cosmetically
- Cycle-1 N1 had four defects. Re-read each against the current text of 02:
  1. Line 70 vs row 4 (line 77) contradiction. Now line 70 separates the claim-stop pre-filter ("skip an issue assigned to someone else", claim.md:41-42) from each candidate's own selector (candidate 1 = own login, candidate 4 = no assignee, excludes own login too) and says the pre-filter is "not identical to either candidate's filter". Row 4 (line 77) now says the unassigned requirement is "candidate 4's own selector, stricter than the claim-stop pre-filter". Rows 1, 2/3, 4 and line 70 are mutually consistent. RESOLVED.
  2. Wrong cause for candidate 4's retry cap. Lines 80-81 now split by candidate. Candidate 1: post-Wave-3 failure leaves the issue assigned to the own login, re-selected every cycle (cites 01:173; 01:173 does say "A poller using candidate 1 would select it again every cycle"). Candidate 4: pre-Wave-3 failure (E-TIER-UNAVAILABLE, 01:38; claim.md:20 "No GitHub or ClickUp write happens before Wave 3") leaves it unassigned and re-selected; post-Wave-3 failure strands it (selector excludes it) so the dispatch record is needed to notice it. Each cited line re-read and matches (01:38, 01:173, claim.md:20, SKILL.md:130-135 error table). RESOLVED.
  3. "the same rule seen from two sides" deleted. Grep over 01-03 for `same rule seen|never to issues assigned|applies only to issues assigned|section 10 line 172|skip assigned|Skip assigned` = no match. RESOLVED.
  4. Pointers. 01:165 and 03:139 both now state: candidate 4 excludes every already-assigned issue; the claim-stop pre-filter is the claim's own rule and not identical to either filter; 01:165 adds the stranded-vs-re-selected contrast with the right anchor (section 10 line 173). 03:139 quotes "a rule that the issue must be assigned to its own login" from its own section 7 row (03:192): that phrase exists verbatim. RESOLVED.
- Citations added by the fix re-verified by tool: `gh issue list --help` (run this session, `cat -n`) line 48 = `$ gh issue list --assignee "@me"`, line 50 = `$ gh issue list --search "error no:assignee sort:created-asc"` (matches 02:70, 02:75, 02:77). `research-notes.md:108-112` = ADDENDUM 2: "each workspace polls GitHub every 5 minutes with its own `gh` login ... via `orca agent launch`", names no routing candidate (matches 02:82). `claim.md:41,42,47` and `:20` read.
- Verdict for (a): the one blocking finding is addressed with a content rewrite plus aligned pointers. PASS.

### Step 3 - check (b): contradictions introduced between or within the three files
- Routing/dedupe rule across 01:150-165, 02:57-83 and 03:134-139: the three files now agree on one claim-stop predicate (skip only issues assigned to someone else, claim.md:41-42), on candidate 1 = own login and candidate 4 = unassigned, and on the failure consequence per candidate (re-selected under candidate 1 after a post-Wave-3 failure; stranded under candidate 4 after a post-Wave-3 failure; re-selected under candidate 4 after a pre-Wave-3 failure, matching 01:38). No contradiction found. PASS.
- 01:38 says that after E-TIER-UNAVAILABLE "the poller would then see the issue still unassigned and could re-dispatch it every cycle". This holds only for selectors that admit unassigned issues (candidate 4, 2, 3), not candidate 1; 02:81 now states it per candidate. 01:38 is therefore compatible, though it does not name the candidate (note M-H below).
- Pre-existing items re-seen, unchanged by cycle 2, carried as notes (cycle-1 M-C, M-G): 03:192 "Duplicate launches are wasteful but not harmful because of the idempotent re-claim" versus 01:159 and 01:177 (same-login concurrent runs both post new comments and a second login double-assigns). 02:220 (Gap 10) proposes a "local state file" while 01:159 says the dispatch record "must then be on GitHub, not local" (conditional on same-login multi-workspace polling) and 01:178 says it must survive a restart (note M-I).
- Within-2c walk (the cycle-1 failure mode): line 70 (pre-filter vs selectors) -> table rows 1-4 (lines 75-77) -> lines 80-81 (per-candidate consequence) -> line 82 (owner decision) -> line 83 (pointers). Each sentence was checked against the others and against claim.md:20, :41, :42, :47; no sentence contradicts another. The row 2/3 cell ("skip when assigned to another login; accept unassigned or own") is the pre-filter, consistent with line 70. PASS.
- Structure intact: Grep count of `^(## |### |Status:)` lines = 30 (03), 28 (02), 17 (01); 02 still has Status: Complete, Key Takeaways (7 blocks), `## Gaps and Questions`, `## Summary`; line counts (wc -l, this session) 290 / 231 / 233 for 01 / 02 / 03, i.e. 01 and 03 have the same length as after cycle 1 (cycle 2 replaced lines in place there; the cycle-2 fix log gives no line counts, so I compared with the cycle-1 report's 290 and 233 only); research-notes.md untouched.

### Step 4 - checks (c) and (d): proportionality, tagging, gap honesty
- Proportionality: the cycle-2 change is about 6 sentences in 02 (lines 70, 77, 79-81) plus one pointer sentence each in 01 and 03. Every added statement cites a line I re-read (claim.md:20/41/42/47, 01:38, 01:173, gh help lines 48/50) or restates an existing derived item. No new speculation. PASS.
- Tagging: the three pre-existing [UNVERIFIED] items in 2c survive (multi-assignee behaviour on GitHub, row 4; exact query form, row 4; whether a later owner decision names a candidate, line 82). The new "stranded" conclusion at 02:81 is derived reasoning from the cited selector and claim lines; 01:173 tags the matching retry-cap statement "[Derived]" but 02:81 does not (note M-J). Doc-sourced claims touched in cycle 2: none beyond help text, which was run, not read from docs. PASS.
- Gaps honesty: no gap was closed or removed by cycle 2 (no Gaps list was edited). 02's numbered Gaps list still lacks the 2c-inline unknowns and the open routing-candidate choice (note M-K), unchanged from cycle 1 M-F. 01 Gap 9 and 03 Gap 15 (poller host) are unchanged and still say no Coder documentation was checked. PASS.

### Step 5 - independent spot-verification of claims outside the cycle-2 diff (INV-019 semantic checks)
Chosen because a stale or false claim in these would mislead the plan and the cycle-1 reports checked only some of them:
- `main.py` registrations: Grep `add_command\(` = 11 hits at lines 521, 525, 529, 533, 537, 541, 545, 549, 553, 557, 561; `cli_portify_group` has no `name=` (line 537); `init_lite_command` is registered with `name="init-lite"` (557). Matches 02 s4.1 (blocks 519-561, 11 registrations, swarm 547-549, reflect 559-561).
- `.github/workflows` (ls): README.md, boundary-guard.yml, contract3-generator-constraint-lint.yml, test.yml = 4 files; `test.yml:3-8` = on/push/pull_request/workflow_dispatch with branches [master, integration]. Matches 02 s1 (no schedule trigger in test.yml).
- `detection._fetch_payload` at `src/superclaude/pr_submit/detection.py:273-275` returns `{"reviews": [], "comments": []}` with the comment block at 268-270. Matches 02 s3.1 exactly.
- `src/superclaude/hooks/hooks.json:96-105` registers `~/.claude/hooks/launch-job-identity.sh`, matcher Bash, timeout 5 (Grep -B/-A). Matches 03 s2.1.
- `origin_repo.py`: `_NUMBER` at line 74, `check_claim` at 102, `read_origin` at 156, `main` at 177. Matches 01 s5 and 02 s2b.
- `tests/cli/test_cli_registration.py:29` "The set is intentionally a frozen snapshot" and no `swarm`/`reflect` hit in the file (Grep for `swarm|reflect` returned only the comment and a loop line, no set member). Matches 02 s4.3 [CODE-CONTRADICTED].
- Live state (Bash, read-only): `gh label list --repo IronbellyOrg/IronClaude` = the 9 defaults (bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix); `gh repo view` = visibility PUBLIC, isFork true. Matches 02 s2 and 03 s3.3 / Stale Documentation (project CLAUDE.md says "private fork").
- SKILL.md error table lines 130-135 (Grep): E-TIER-UNAVAILABLE (130), E-WORKER-NO-OUTPUT (131), E-ASSIGN-FAILED (132, "before ClickUp and before any comment"), E-POST-FAILED (135). Supports 01:38/01:173 and shows the E-ASSIGN-FAILED omission in note M-J.
- Result: 0 false claims found in this sample of 8 independent claim groups.

---

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | (a) N1 defect 1: line 70 vs row 4 contradiction removed | PASS | 02:70, 02:77 re-read; pre-filter vs selector split; gh help lines 48/50 run |
| 2 | (a) N1 defect 2: candidate-4 retry-cap cause corrected | PASS | 02:80-81 vs 01:38, 01:173, claim.md:20, SKILL.md:130-135 |
| 3 | (a) N1 defect 3: "same rule seen from two sides" removed | PASS | Grep over 01-03: no match for stale phrases |
| 4 | (a) N1 defect 4: pointers at 01:165 and 03:139 aligned | PASS | both re-read; anchors 01:173, 03:192 verified |
| 5 | (b) No contradiction between 01, 02, 03 on routing/dedupe after the fix | PASS | 01:150-165, 02:57-83, 03:134-139 compared sentence by sentence |
| 6 | (b) No contradiction inside 02 section 2c | PASS | line-by-line walk, Step 3 |
| 7 | (c) Added content proportionate; every addition cites a line that exists | PASS | Step 4; note M-J on one untagged derivation |
| 8 | (c) Doc-sourced claims remain tagged | PASS | three [UNVERIFIED] tags in 2c survive; none added or dropped |
| 9 | (d) Gaps sections remain honest | PASS (note M-K) | no Gaps list edited; poller-host gaps unchanged |
| 10 | Structure and research-notes.md intact | PASS | headings counted, wc -l, md5 d2671ff2... |
| 11 | Independent spot-verification outside the diff | PASS | 8 claim groups re-checked against source and live GitHub state |

## Summary
- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Blocking (IMPORTANT) issues: 0
- Issues fixed in-place: 0 (report only)
- Blocking findings from the cycle-2 consolidated list: 1 of 1 resolved (N1). No new blocking finding introduced by cycle 2.
- Issue count trend: cycle 1 left 1 blocking; cycle 2 leaves 0. No systemic growth.

## Issues Found
No CRITICAL or IMPORTANT issues. Minor notes only (never fail the review, not rechecked later):

| # | Severity | Location | Note |
|---|----------|----------|------|
| M-H | MINOR | 01:38 | Says the issue "could" be re-dispatched every cycle after E-TIER-UNAVAILABLE without naming the candidate; true only for selectors that admit unassigned issues (02:81 states it correctly). |
| M-I | MINOR | 02:220 (Gap 10) vs 01:159 | Gap 10 suggests a "local state file"; 01:159 says the dispatch record must be on GitHub, not local, if one person runs several workspaces. Pre-existing; 03 Gap 11 leaves the choice open. The design phase must settle it. |
| M-J | MINOR | 02:81 | The before/after-Wave-3 split is by example. E-ASSIGN-FAILED (Wave 3 step 1; claim.md:47, SKILL.md:85/132) also leaves the issue unassigned and re-selected under candidate 4, and E-WORKER-NO-OUTPUT can occur at Wave 1 (before the assignment) as well as Wave 4. The "stranded" conclusion is derived but not tagged [Derived] as 01:173 is. |
| M-K | MINOR | 02 Gaps list | The routing-candidate choice is an open owner decision stated only inline (02:82, 01 s9, 03 s4.3), and the 2c-inline [UNVERIFIED] items are not numbered gaps (cycle-1 M-F, unchanged). |
| M-L | MINOR | 01:162 | "the only candidate that needs no new label" is ambiguous: candidate 1's own command at 01:150 includes `--label <trigger>`, a new label under every candidate. Means "no new routing label". |
| M-A..M-G | MINOR | carried from cycle 1 | web-02 prompt scope (M-A), summary-level permission wording (M-B), 03:192 "not harmful" vs 01:159/177 (M-C), analyst gap wording (M-D), moved line anchors and the `issueType` caveat at 02:43 (M-E), 02 Gaps and Orca placeholder line (M-F), 03 Gap 4 `--prefill` vs 01 s12 `delivery: 'submit'` (M-G). Left as notes by the severity rule. |

## Actions Taken
None (fix_authorization: false). Only this report was written.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was supplied in the prompt (standalone behaviour).

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- Relied on the cycle-1 structural report (`qa-verification-phase3-structural.md`, VERDICT: PASS) for anchors the cycle-2 diff did not touch (the roughly 300 file:line citations swept in the evidence gate). I did not read the cycle-2 structural report, which runs in parallel with this one.
- Relied on the cycle-1 content report for the confirmed resolution of the original three blocking findings (routing contradiction between files, poller-host gap, CCSESSION_PERMISSIONS wording). I did not re-trace the Orca `agent-launch-profile.js` / `tui-agent-permissions.js` lines.

**(b) Independent semantic checks (>=1 required, INV-019):**
- N1 resolution -- verified by Read of 02 lines 57-83, 01 lines 38, 148-173, 03 lines 134-139 and 192, `claim.md:1-91`, Bash `gh issue list --help | cat -n` (lines 48, 50), Read `research-notes.md:95-113`, and a sentence-by-sentence consistency walk (Steps 2 and 3).
- Failure-mode claim for candidate 4 -- verified by Grep of `SKILL.md` error table (lines 130-135) against claim.md Wave order, which exposed the E-ASSIGN-FAILED omission (M-J).
- Eight claim groups outside the cycle-2 diff -- verified by Grep on `main.py`, `test.yml`, `detection.py`, `hooks.json`, `origin_repo.py`, `tests/cli/test_cli_registration.py`, and Bash `gh label list` / `gh repo view` / `ls .github/workflows` (Step 5). All matched.
- Cross-file contradiction scan -- Grep over 01-03 for pre-filter / unassigned / no assignee / not assigned phrases, then Read of each hit in context (found M-H, M-I; confirmed no routing contradiction).

If I had reported 0 findings the user should not have trusted it. The residual defects (M-H to M-L) only show up when a failure case is walked through the claim waves against the error table, which a citation sweep does not do. None is blocking: each is a wording, tagging or completeness gap on a claim whose substance is correct or explicitly deferred to the design.

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 10 | Glob: 1 | Bash: 3 (all read-only: gh help, md5sum/wc/grep, gh label list / gh repo view / ls)
**Web research:** none performed. tavily_search: 0 | tavily_extract: 0 | fallback: 0.
Tool calls (Read + Grep + Glob = 20) exceed the 11 checklist items, so the minimum-engagement rule is met.
UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations
1. Gate 1 content verification may proceed on the cycle-2 result: no open blocking finding.
2. Carry M-A to M-L into the design/plan phase as notes. The two worth settling there: where the dispatch record lives (M-I, tied to Gap 9 / Gap 15) and which routing candidate the owner picks (M-K).

## QA Complete

Status: Complete

VERDICT: PASS
