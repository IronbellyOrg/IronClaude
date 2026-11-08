# QA Report - Phase 3 Fix Cycle Verification (structural)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** verification of Phase 3 fixes
**Fix authorization:** false (report only)
**Status:** Complete

---

## Progress log (appended incrementally)

Inputs read in full this session: `qa/qa-consolidated-findings-phase3.md` (3 blocking: #1, #2, #3; 9 minor), `qa/qa-fix-log-phase3.md`, research files 01 (290 lines), 02 (228), 03 (233). Every source cited by the fixes was re-read independently (not taken from the fix log).

## Check A1: blocking finding #1 (routing/dedupe contradiction, files 02/01/03) - RESOLVED

Evidence:
- File 02 line 57 now says skip only issues assigned to a login other than the own login, with an amendment note; line 63 (Key Takeaways 2b) is narrowed the same way. Grep for "already have an assignee" / "skip issues that already" over research/0*.md: the only hits are 02 line 57 (inside the amendment note quoting the old text) and 02 line 67 (the 2c narrative quoting it). No unqualified "skip assigned" statement remains.
- New section 2c (02 lines 65-80) states one predicate, maps all four of file 01's routing candidates (table at 01 line 148, candidate 1 at 01 line 150, candidate 4 at 01 line 153) to a selection rule, and tags GitHub multi-assignee behaviour and the query form [UNVERIFIED]. Reconciles with 01 line 165 and 03 line 139 (pointer bullets present, same wording of the predicate). 03 line 134 (assignee row) and 03 line 192 ("must be assigned to its own login") are explained by the 03 line 139 pointer.
- Cited sources re-read: `src/superclaude/skills/sc-issue-protocol/refs/claim.md` lines 41 (assigned to another login -> STOP), 42 (own login -> continue, idempotent), 47 (`--add-assignee @me`): match. `gh issue list --help` (run this session, grep -n): line 20 `--assignee`, line 48 `--assignee "@me"` example, line 50 `no:assignee` search example: match the 2c table. `research-notes.md` lines 108-112 (ADDENDUM 2, option A, 5-minute own-login polling, no routing candidate named): match.
- Result: files 01, 02, 03 no longer contradict each other on this point. PASS.

## Check A2: blocking finding #2 (where the poller runs / dispatch record) - RESOLVED as a recorded, tagged gap

Evidence:
- File 01: Key Takeaways sentence at line 130 carries an [UNVERIFIED] tag naming scheduler availability, survival across autostop/restart and durable state, and points to Gaps item 9; Gaps and Questions item 9 exists at line 267, tagged [UNVERIFIED], covering (a) scheduler, (b) survival across autostop/restart, (c) durable state location, (d) a stopped workspace not polling, assigned to web-02 and the live plan phase.
- File 03: section 5 line 150 carries the [UNVERIFIED] tag and points to item 15; Gaps item 15 exists at line 222, tagged [UNVERIFIED], same four unknowns plus the consequence for the section 7 at-most-once/audit properties, assigned to web-02 and the live plan.
- Cited sources re-read: `research-notes.md:85` (web-02 row names "autostop"): match. `src/superclaude/core/WORKER-CONTRACT.md:61` (WC-13, worker never calls `agent launch`): match. `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/agent-launch.js:23-35` (capabilities check, `incompatible_runtime`, `callAgentLaunch` against a running runtime client): match.
- The proposed fix asked for exactly this (gap entry, [UNVERIFIED] tags, assignment to web-02 and the live plan); nothing in the repo can close it. PASS.

## Check A3: blocking finding #3 (`CCSESSION_PERMISSIONS=default` treated as deciding bypass vs stall) - RESOLVED

Evidence:
- File 03 line 67 (ccsession row): amendment present, cites README:534-535 and ccsession:141, Orca config, Orca code lines, and tags whether `orca agent launch` applies `agentDefaultArgs` as [UNVERIFIED]. Line 70 (section 2.3 first bullet): rewritten, states `CCSESSION_PERMISSIONS=default` does not by itself produce a stall. Line 77 (section 2.3 Key Takeaways): rewritten, says it is not a sufficient mitigation alone. Line 212 (Gaps item 5): rewritten to name three inputs. Line 233 (Summary): parenthetical added. File 01 line 190 (section 11 Interactivity): reconciliation sentence added and consistent with file 03.
- Cited sources re-read: `src/superclaude/skills/ccsession-tag/README.md:534` says "flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply" and line 535 says a non-empty `CC_CLAUDE_FLAGS` replaces the flags: match. `src/superclaude/skills/ccsession-tag/ccsession` lines 136-141: `default)` branch gives only `--allowedTools=Grep`, and `CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:-$_cc_default_flags}"` at line 141: match. `/home/coder/.config/orca/profiles/local-default/orca-data.json` (grep -o): `"agentDefaultArgs":{"claude":"--dangerously-skip-permissions",...}` and `"agentCmdOverrides":{}`: match. `/opt/Orca/resources/app.asar.unpacked/out/shared/agent-launch-profile.js:12-14` (userArgs falls back to `settings.agentDefaultArgs[agent]`, then YOLO args when nothing typed) and `.../shared/tui-agent-permissions.js:16` (`claude: '--dangerously-skip-permissions'`): match.
- Remaining grep over research/0*.md for "stalled (default mode)" and every `CCSESSION_PERMISSIONS=default` occurrence (01:190, 03:67, 70, 77, 212, 233): every occurrence carries the corrected reading. PASS.

## Check B: no new blocking issue introduced by the fixes - PASS

- False claims: every added statement was traced to a source above; none is contradicted. The added 2c table's claims about candidates 1-4 match file 01 lines 148-155 as re-read.
- Untagged doc claims: the added unknowns (Coder scheduler, autostop survival, durable state, `agentDefaultArgs` on `orca agent launch`, GitHub multi-assignee behaviour) are all tagged [UNVERIFIED].
- Broken structure: no heading was removed or reordered; section 2c sits between 2b and section 3 in file 02; new Gaps items 01:9 and 03:15 are numbered in sequence after 01:8 and 03:14. Cross-references resolve (01:130 -> item 9 at 01:267; 03:150 -> item 15 at 03:222; 02:80 pointers present at 01:165 and 03:139).
- `research/research-notes.md` md5 now `d2671ff214db5ce006c8a5f46e99896b`, identical to the value in the fix log (unchanged, as required).
- Line counts now 01: 290, 02: 228, 03: 233 (`wc -l`), matching the fix log.

## Check C: required structure per research file - PASS

| File | Status: Complete | Summary | Gaps and Questions | Key Takeaways |
|---|---|---|---|---|
| 01 | line 4 | line 287 | line 256 | plain "Key Takeaways" blocks after each section (e.g. lines 29, 47, 66, 78, 97, 111, 127, 161, 176, 198, 240, 252); same format as before the fixes |
| 02 | line 4 | line 226 | line 207 | headings at lines 26, 48, 61, 123, 155, 168, 189, 203 |
| 03 | line 4 | line 231 | line 204 | headings at lines 41, 75, 105, 141, 156, 181, 197 |

## Check D: every newly added claim cites an existing file and line - PASS (with minor notes)

All new citations (claim.md:41/42/47, README:534-535, ccsession:136-141, orca-data.json keys, agent-launch-profile.js:12-14, tui-agent-permissions.js:16, research-notes.md:85 and 108-112, WORKER-CONTRACT.md:61, handler agent-launch.js:23-35, `gh issue list --help` lines 20/48/50, and the internal file 01/02/03 line anchors) were re-read and resolve as described.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR (note) | 02 line 79 | Cites "file 01 section 10 line 172" for "a claim that fails after Wave 3 leaves the issue assigned to the own login"; that sentence is at 01 line 173 (172 is the preceding at-most-once bullet). Moved line number on a true claim. | none required |
| 2 | MINOR (note) | 02 line 43 | Calls the `gh issue list --json issueType` field name unverified; `gh issue list --help` (run this session) lists `issueType` among the JSON fields and a `--type` flag. The sentence is tagged unverified, so it is not a false claim. Pre-existing, not introduced by the fixes. | none required |

No blocking issue found.

## Summary
- Checks passed: 6 / 6 (A1, A2, A3, B, C, D)
- Checks failed: 0
- Blocking issues open: 0
- Minor notes: 2 (not rechecked in later rounds)
- Issues fixed in-place: 0 (fix authorization false)

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 15 | Grep: 4 | Glob: 1 | Bash: 2 (each call targeted a specific check above; Read+Grep+Glob = 20 >= 6 checks)

**Self-audit:** a "0 blocking" result is backed by independent re-reads of eleven cited sources, a repo-wide grep for the residual wrong phrasings, an md5 check of `research-notes.md`, and line-anchored confirmation of each added cross-reference. I looked for new defects (broken anchors, untagged claims, structural loss) and found only the two off-by-one or stale-tag notes above.

VERDICT: PASS

Status: Complete

## QA Complete

