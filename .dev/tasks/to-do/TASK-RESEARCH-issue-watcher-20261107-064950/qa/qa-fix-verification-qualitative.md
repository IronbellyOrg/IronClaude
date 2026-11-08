# QA Report: Phase 6 fix verification (report-qualitative, fix-cycle 1)

**Topic:** GitHub issue watcher research report (issue #331)
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative)
**Fix cycle:** 1
**Report under review:** RESEARCH-REPORT-issue-watcher.md
**Fix log:** qa/qa-fix-log-phase6.md (override of qa-fix-log.md)
**Fix authorization:** false (report only)
**Status:** Complete (see the Status line at the end; verdict FAIL, one blocking finding)

---

## Method

Read the whole report (about 2,174 lines) end to end, the consolidated findings (12 blocking) and the fix log (qa-fix-log-phase6.md). Then independently checked the cited sources the fixes rely on (listed per check). No inherited structural verdict was supplied in the spawn prompt, so standalone behaviour applies (no reliance on any rf-qa PASS).

## Check log (appended incrementally)

### C1. Source claims introduced by the fixes (verified against source, not the fix log)

| Claim in the report | Source read | Result |
|---|---|---|
| `install_user_setup.py:198-263`: `_find_orca` proves a candidate is Orca (probe `skills list --json`, needs the `orca-cli` topic); GNOME screen reader warning; `_ORCA_CLIS = ("orca-ide","orca")` at l.35; `_orca_timeout` l.224-227; `install_orca_skills` l.230-263 | Read install_user_setup.py l.28-39 and l.195-270 | TRUE. Line numbers, timeout=10, probe argv, docstring quote and the topic check all match. |
| "No Python code under src/superclaude runs `orca agent launch`; the only Python `orca` calls are `skills list` and `skills install`" (2.3, 2.5, G1, G3) | Grep over src/superclaude *.py for quoted `orca`/`orca-ide`, `shutil.which("orca`, orca+subprocess | TRUE (only hit is `_ORCA_CLIS` at install_user_setup.py:35). A grep for a Python `gh` call found none, so the unchanged "no Python gh wrapper" claim still holds. |
| `.github/workflows/test.yml:32-38` runs `make sync-dev` before pytest because audit tests assert parity with the gitignored `.claude/` mirrors; pytest line at `:46-47` | Read test.yml l.10-54 | TRUE (step "Sync src/superclaude/ -> .claude/ mirrors" l.32-38; pytest command l.46-47). |
| `.claude/skills` and `.claude/commands` do not exist in this worktree | `ls` | TRUE (only agent-memory, cache, settings.json exist). |
| Makefile `sync-dev` l.109, `verify-sync` l.166; `.claude/*` gitignored (`.gitignore:127`) | Grep Makefile, .gitignore | TRUE. |
| `gh issue list --help` (gh 2.103.3) lists `issueType` and `projectItems` | Ran `gh issue list --help`, `gh --version` | TRUE. Former CONTRADICTION (a) is resolved correctly: 2.3, 5.5 and A.1 item 5 now agree. |
| gh source: `Issue.ExportData` exports body/title/number/repository/url; `ProjectItem.ExportData` exports id/title/body/type (`queries.go` l.558-566, 673-678) | `gh api --method GET repos/cli/cli/contents/pkg/cmd/project/shared/queries/queries.go` (read-only), printed l.550-570, 665-682 | TRUE. The leak the finding named is real and the mandatory `--jq` projection is the right fix. |
| Orca retry rule quoted verbatim in 2.2, Phase 3 table, Q3 | Grep `specs/agent-launch.js` l.27 | TRUE, verbatim. (I did not run bare `orca`: on Linux it can be the GNOME screen reader.) |
| 5.15 source note: web-02 J3 has six items at `:309-314`; web-01 14.5 event-time / change-history / shared-ledger bullets at `:178, :181, :182` | Read both research files at those lines | TRUE. |

### C2. The 12 blocking findings, one by one (substantive or cosmetic?)

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| 1 | Three CONTRADICTION blocks | RESOLVED, substantive | Grep for `CONTRADICTION` = 0 hits. (a) 2.3 l.336, 5.5 l.808, A.1 item 5 l.2009 now agree and are code-verified. (b) 5.1 row 3 (l.764) and 5.13 OIDC row (l.895) now say "option B ... not option C"; lettering note at l.909; 4.4 row l.743 and 9.3 C10 record the mapping. Remaining "C-lite" hits (l.743, 764, 1050) are explanatory mappings of the web files' naming. (c) One authoritative nine-condition list (Section 6 table l.1313-1323), 5.15 (l.956-966), 7.8, and Section 8 (l.1797-1807) carry the same nine numbers; item 9 is honestly marked "derived from G19, no research source". Minor: 5.15 items 2, 4, 6 are paraphrases of the Section 6 wording (5.15 item 2 says "many workspaces polling with their own login", Section 6 says "share one login"), although 5.15 says it is "the same list". |
| 2 | False "no Python calls orca" | RESOLVED, substantive | Verified in C1. Corrected in 2.3 (l.341), 2.5 (l.513), G1 (l.683), G3 (l.685). Plan now carries `resolve_orca` (step 3.4, l.1592), contract row 1 uses `<orca>` (l.1573), `FakeOrca` answers the probe and has a `not_orca` mode (l.1593), tests cover prefer-`orca-ide`, skip non-JSON, raise `E-ORCA-NOT-FOUND` (l.1594), e2e stub answers the probe (l.1728, 1729). Gap: see N1 (no `shutil.which` seam; probe timeout classification). |
| 3 | Q1-Q3 vs D1-D3 collision | RESOLVED, substantive | Grep `\bQ[123]\b` leaves only open-question uses (step 1.10, `open: Qn` flags, Section 9.2 rows, A.2 local numbering with its own disclaimer at l.1995). 1.1 has an explicit label rule (l.139). 8.4 and 9.1 use D1-D3. Minor: see N4. |
| 4 | Phase 4 read rules contradict | RESOLVED, substantive | One rule stated once at l.1613 (four clauses); `gh api --method GET user -q .login` (l.1617); SC-7 (l.627) and SC-13 (l.633) reworded (`--method GET` required and allowed, POST/PATCH/PUT/DELETE forbidden); step 1.5 (l.1537), test 4.5 (l.1639), stub rule 6.1 (l.1728), 6.2 (l.1729), 6.4 criterion 3 (l.1731) and the checklist (l.1820) all state the same two exempt calls. No residual disagreement found. |
| 5 | Issue title/body reach the poller | RESOLVED, substantive | Verified against gh source (C1). Discovery argv carries a mandatory `--jq` projection to `{number, repository, status}` (l.1618); SC-5 (l.625), D3 row (l.1522), Phase 4 goal (l.1600), 7.3 "Fields read" (l.1362), checklist (l.1818) and test 4.5 (hostile `title`/`body` fixture, l.1639) agree. JSON key names stay [PROPOSAL] and open under Q8 (honest). See N7. |
| 6 | Candidate cap starves new issues | PARTLY RESOLVED, and the fix introduced a new contradiction | `is:open` added (l.1618); cap now applied after local skips (algorithm step 3, l.1661); test "Many already-handled candidates" added (l.1709); `marker-found` recording added (step 6, l.1664). But the new unconditional drop of every `launched` entry contradicts `may_dispatch`, the "Second cycle" test, the stranded-claim handling and G9/SC-10. See B1 below. |
| 7 | Launch timeout leads to duplicate session | RESOLVED for the timeout path, substantive; the `unknown`-with-id retry is entangled with B1 | `E-TIMEOUT` maps to `unknown` with no id (step 3.4, l.1592); `may_dispatch` never launches fresh after `unknown` (l.1650); `launch_cwd` stored (l.1650), `cwd-changed` abandon, `build_runners(worktree)` binds `cwd` (l.1652), `run_command(cwd=...)` (l.1556); SC-9 (l.629), Q3 (l.1853, verbatim rule verified) and the "Launch timeout" test (l.1708) agree, and the rule text matches `specs/agent-launch.js:27`. Residual: step 3 skips `unknown` inside the lease, so "next cycle's argv contains --retry-launch" in the "Unknown outcome" test (l.1707) only holds if the test advances time past the lease; the spec does not say so (part of B1). |
| 8 | Phase 6 gate list would fail | RESOLVED, substantive | Step 6.5 (l.1732) runs `make sync-dev` first, `uv run pytest`, then `make verify-sync`, cites `test.yml:32-38` and `:46-47` (both verified), states the mirror output is never staged (matches `.gitignore:127` and the project CLAUDE.md rule). SC-16 (l.636), 7.6 "Checks to pass" (l.1407), step 1.9 (l.1541) and the checklist (l.1823) match. The unverified "31 test files" count was dropped (Grep: 0 hits), which is the honest choice. |
| 9 | Orphaned gap G15 | RESOLVED, substantive | Step 1.6 (l.1538) now states the basis (approver's label is the authorization, the claim's writes are the full extent), Q36 added (l.1886), G15 Notes (l.697), Section 10 R03 row (l.1970) and A.3 (l.2124) point to step 1.6 and Q36. |
| 10 | Wrong cross-references in Section 8 | RESOLVED, substantive | Step 1.5 points to the Phase 4 preamble table (exists, l.1603-1611), 1.8 to the Phase 3 contract table (l.1571-1585), 1.9 to the "On failure or skip" column and exit-code table (exist, l.1657-1695) and says openly that Phase 5 has no Scenario/Behavior table. Step 7.6 now has 11 items; step 1.10 says "eleven" and lists 12 Q numbers; I mapped item to Q one by one (1:Q1,Q2; 2:Q3; 3:Q8; 4:Q7; 5:Q6; 6:Q15; 7:Q11; 8:Q17; 9:Q5; 10:Q13; 11:Q18) and the set matches exactly. Q13 and Q18 point at items 10 and 11. |
| 11 | False carry claim | RESOLVED, substantive | Q34 (ClickUp identity vs `gh` login) and Q35 (minimum `gh` scopes) exist (l.1884-1885) with sources; Section 5 intro (l.754) now says only what is true; A.1 item 21 (l.2025) points to Q34. |
| 12 | Idempotency key inconsistency | RESOLVED, substantive | One rule: record keyed by (repository, issue number), approval event id as attribute (step 5.1 l.1650, algorithm step 11 l.1669, 5.12 l.881, Section 10 l.1987); the (repository, issue, approval event id) key is the push-contract key only (5.15 l.935, 5.16 l.984, R10 for B l.1271). All consistent. Note that the `re-approved` detection depends on B1 (it is unreachable for a `launched` entry). |

### C3. Cross-section consistency after the fixes (Sections 4, 6, 7, 8 and the success criteria)

Result: one blocking contradiction (B1), introduced by the fix to finding 6. Everything else I traced agrees.

**B1 (blocking, IMPORTANT, axis: contradictions). The new candidate-cap order makes the retry state machine unreachable.**

- Algorithm step 3 (report l.1661) now says: drop "every number whose local entry is `launched`, `abandoned`, or `pending`/`unknown` still inside the lease" before the cap. `launched` and `abandoned` are dropped with no lease condition.
- Step 5.1 `may_dispatch` (l.1650) says: "`pending` and `launched` give `wait` until `now - last_at >= lease`, then `launch` while `attempts < max_attempts`, else `abandon`". A `launched` entry never reaches `may_dispatch` (step 7) because step 3 already removed it, so the "after the lease, launch again / abandon" branch for `launched` is dead.
- Test "Second cycle" (l.1702) asserts "after the lease and with no marker: exactly one retry; after `max_attempts`: `abandoned`, reported, exit 3". With step 3 as written the `launched` entry is skipped forever, so no retry and no `abandoned` can occur. That test cannot pass against the stated algorithm.
- The Phase 5 intro (l.1646) says a claim that fails after Wave 3 "is selected again every cycle; the attempt cap and an 'abandoned' report handle it". Under step 3 it is never selected again and never reported as abandoned. The same holds for the common case `E-TIER-UNAVAILABLE` (session launched, claim stopped at Wave 1, no marker): it is now silently dropped, where before the fix it was retried up to `max_attempts` and then reported.
- This also breaks the Section 4 target of G9 ("a stranded claim is noticed", l.691) and SC-10 (l.630), and makes the `re-approved` audit reason (step 5.1 / step 11) unreachable for `launched` issues.
- The `marker-found` entries added by step 6 (recorded as `launched`, attempts 0) are the reason the author made `launched` an unconditional drop; but the correct way to get "terminal skip" for those is a distinct terminal state (for example `claimed`), not making every `launched` entry terminal.
- Secondary effect of the same step: `unknown` inside the lease is dropped, so the "Unknown outcome" test (l.1707: "next cycle's `orca` argv contains `--retry-launch <id>`") only holds if time is advanced past the 60-minute lease; the test text does not say so.
- Required fix: drop `launched` (and `pending`/`unknown`) only while `now - last_at < lease`; drop `abandoned` and a new terminal `claimed` state (written for `marker-found`) unconditionally; state in the "Unknown outcome" test that `now` is advanced past the lease (or that `retry-launch` is allowed inside the lease, and change step 3 and `may_dispatch` to say so); then the "Second cycle" and "Many already-handled candidates" tests (which must also cover a `launched` entry older than the lease) are consistent with the algorithm.

**Everything else traced and consistent:**

- SC-9, 2.2 "Key findings", Phase 3 "Lost reply" row, step 3.4, step 5.1, the "Launch timeout" test, Q3 and 7.6 poller rules all agree that a timeout is `unknown`, never `failed`, never a fresh launch, and is abandoned after the lease for inspection.
- SC-5, SC-4, D3 row (8.4), 7.3 "Fields read", Phase 4 goal and call table, test 4.5 and the checklist agree on the `--json number,labels,assignees,state` + `--jq` projections.
- SC-7, SC-13, Phase 4 read rule, step 1.5, 6.1 stub rule, 6.2, 6.4 criterion 3 and the checklist agree on the two exempt calls and `--method GET`.
- SC-16, 6.5, 7.6, 1.9 and the checklist agree on the `make sync-dev` / `uv run pytest` / `make verify-sync` order.
- Requirement Scoring tally recomputed from the cells: A 2/8/0, B 1/9/0, C 0/10/0, D 2/8/0, which matches the Tally table.
- The recommendation (Section 7.2) still rests on the scoring rule and states where A scores lower.

### C4. Owner decision wording and recommendation (task checks c and d)

Compared the report against the binding source, `research/research-notes.md` ADDENDUM 2 (lines 108-112, read in full).

- Decision text intact. D1 in 1.1 (l.135) and 9.1 (l.1838) reproduces the owner's sentence word for word ("each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim via `orca agent launch`; no listener, no inbound port, no address registry"). Claim-only (D2) and integer-only (D3) match. The repo-side deliverable (design doc, tested poller with mock `gh` and mock `orca agent launch`, nothing run live, label setup instructions) matches l.141, 1337, 1841.
- Coder#477 statement intact: "filed assuming a push design; option A makes #477 unnecessary unless B or C is revisited" appears in 1.2 (l.149), 3.4 (l.660), 4.1 G18 (l.700), 7.7 (l.1411), 9.1 D5 (l.1842), the Section 8 follow-up table (l.1786) and the closing sentence of the revisit table (l.1325). It is stated as a sibling dependency in the Coder repo (7.7), consistent with the task wording.
- Recommendation is labelled "decided by the owner" (7.1 l.1335, 6.1 title l.1057, 1.1 l.135). Grep for `pending owner` = 0 hits. The three issue questions are still answered (1.1 table l.117-121; 6.1 "Answers to the three issue questions" l.1106-1112).
- B and C remain scored (R1-R10 table, Tally, Options Comparison), documented (6.2, 6.3) and tied to nine revisit conditions with sources (l.1309-1327, 5.15, 7.8, Section 8 table).
- External findings supplement, never override: Section 5 intro (l.754) says the codebase is the source of truth and no external finding overrides verified code; 4.4 resolves every web-versus-code or web-versus-web disagreement in favour of the stronger or primary source; 5.9 explicitly limits the `claude -p` finding to documentation level. The fix-added gh-source reading (`cli/cli` queries.go) is itself marked as read on 2026-11-07 and used only to justify a protective `--jq`, not to override code.

### C5. New minor findings (notes only, not rechecked in later rounds)

| # | Note | Where | Axis |
|---|---|---|---|
| N1 | `resolve_orca` calls `shutil.which` directly (step 3.4), which is not injectable, so the unit tests specified in 3.6 (prefers `orca-ide`, skips non-JSON, happy path in `test_cycle.py`) have no seam to make a candidate resolve on a CI host without Orca; the plan should say `which` is a parameter or is monkeypatched. Also a probe that times out inside `resolve_orca` would arrive as `CommandError("E-TIMEOUT")` and be classified `unknown` by the launch rule, although no launch started (`_find_orca` simply tries the next candidate). Safe direction (no duplicate session) but a 60-minute stall. | l.1592, 1594 | AX-3 |
| N2 | Discovery reads `-L 100` and the `--jq` projection drops `totalCount`, so truncation of the discovery result is not detected, unlike the events and comments reads. Handled issues stay in Backlog assigned to the login until a person moves them, so they can in time crowd the first 100 results. | l.1618, 1619 | AX-3 |
| N3 | The PATH stub of 6.1 pipes `gh api ... --jq` through `jq` but does not mention doing the same for `gh project item-list --jq`; the Project-mode e2e path needs it, or the projected shape the parser expects is never produced. | l.1728 | AX-3 |
| N4 | The owner's own labels in ADDENDUM 2 are Q1/Q2/Q3; the report now uses D1/D2/D3 and removed the "Q1 =" aliases, so a reader checking the source cannot map them from the report. One mapping line in 1.1 would restore traceability. 9.1 also extends the D series to D6 (deliverable, Coder#477, alternatives), and step 1.9 plans a design-doc "Defaults table with IDs `D1..`", which reuses the D label. | l.139, 1541, 1836-1843 | AX-2 |
| N5 | SC-4, 6.1 step 6 and 7.3 still say `str(int(number))`; step 3.2 deliberately uses the stricter `type(number) is int` plus a regex. Same effect, different wording. | l.624, 1070, 1361 vs 1590 | AX-2 |
| N6 | 5.15 says it "repeats the same nine items with the same numbers" but items 2, 4 and 6 are paraphrases of the Section 6 wording (item 2: "many workspaces polling with their own login" versus "share one login"). | l.959-963 vs 1316-1320 | AX-2 |
| N7 | 6.1 step 3 describes candidate reads as `number,labels,assignees,state` only and does not mention the Project call and its `--jq` projection (the 8.2 diagram and Phase 4 do). | l.1067 | AX-3 |

None of N1 to N7 changes a recommendation or makes a plan step wrong on its own; they are listed for the next editor.

## Items Reviewed (summary)

| # | Check | Result |
|---|---|---|
| 1 | Finding 1: CONTRADICTION blocks resolved substantively | PASS |
| 2 | Finding 2: `orca` claim corrected, `resolve_orca` carried into plan (source read) | PASS |
| 3 | Finding 3: D1-D3 relabelling complete | PASS |
| 4 | Finding 4: one consistent read rule | PASS |
| 5 | Finding 5: `--jq` projection, title/body never reach the poller (gh source read) | PASS |
| 6 | Finding 6: candidate cap order and `is:open` | FAIL (B1: fix contradicts `may_dispatch`, the "Second cycle" test, G9/SC-10) |
| 7 | Finding 7: timeout is `unknown`, same-cwd retry, Q3 corrected | PASS for the timeout path; the `unknown`-with-id retry timing is part of B1 |
| 8 | Finding 8: sync-dev gate order (test.yml:32-38 read) | PASS |
| 9 | Finding 9: G15 basis and Q36 | PASS |
| 10 | Finding 10: Section 8 cross-references | PASS |
| 11 | Finding 11: carry claim, Q34 and Q35 | PASS |
| 12 | Finding 12: idempotency key rule | PASS |
| 13 | No new contradictions between Sections 4, 6, 7, 8 and the success criteria | FAIL (B1) |
| 14 | Owner decision wording intact; recommendation "decided by the owner"; three questions answered; B/C scored with revisit conditions; Coder#477 sibling dependency | PASS |
| 15 | External findings supplement and never override code | PASS |

## Summary

- Checks passed: 13 / 15
- Checks failed: 2 (both caused by the single issue B1)
- Critical issues: 0
- Blocking (IMPORTANT) issues open: 1 (B1)
- New minor notes: 7 (N1 to N7, not rechecked later)
- Issues fixed in place: 0 (report-only review)

Of the 12 original blocking findings, 11 were fixed substantively (not cosmetically), including every one the spawn prompt named: the launch-timeout `unknown` state and same-cwd retry, the `--jq` projection, the sync-dev gate order, the `resolve_orca` screen-reader check, the D1-D3 relabelling and the idempotency-key rule. The candidate-cap fix (finding 6) was done in a way that broke the retry state machine it sits next to.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| B1 | IMPORTANT (blocking) | Report l.1661 (algorithm step 3), l.1650 (`may_dispatch`), l.1664 (step 6), l.1702 and l.1707 (tests), l.1646 (Phase 5 intro), G9/SC-10 | Step 3 drops every `launched` and `abandoned` entry unconditionally, so `may_dispatch`'s "launched, after the lease, launch again or abandon" branch is dead, the "Second cycle" test cannot pass, stranded claims (including `E-TIER-UNAVAILABLE`) are never retried or reported, and `re-approved` is unreachable for `launched`. `unknown` inside the lease is also dropped, which the "Unknown outcome" test does not account for. | Drop `launched`/`pending`/`unknown` only while `now - last_at < lease`; add a terminal `claimed` state for `marker-found` entries and drop it and `abandoned` unconditionally; make `may_dispatch` and step 3 say the same thing; state in the "Unknown outcome" test that `now` is advanced past the lease (or allow `retry-launch` inside the lease and say so); extend "Many already-handled candidates" with a `launched` entry older than the lease. |

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No `## Inherited Structural Verdict` was supplied, so I did not skip any structural check on the strength of an rf-qa PASS; I also did not rely on the fix log's own statements (every fix-log claim I report as true was re-read in the report or in source).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Fix-log claim "`install_user_setup.py:198-263` precedent" re-verified by Read of the file (l.28-39, l.195-270): numbers, timeout, probe and docstring all match.
- Fix-log claim "`test.yml:32-38` runs sync-dev before pytest" re-verified by Read (l.10-54) plus `ls .claude` (mirrors absent) and Makefile/.gitignore Grep.
- Fix-log claim "gh item export carries title and body" re-verified by `gh api --method GET` on `cli/cli` queries.go and reading l.550-570, 665-682.
- Orca retry rule re-verified by Grep of `specs/agent-launch.js:27`.
- Fix-log claim "`issueType`/`projectItems` listed by gh issue list" re-verified by running `gh issue list --help`.
- Absolute claims added by the fix ("the only Python `orca` calls", "no Python `gh` call") re-verified by Grep over `src/superclaude`.
- Fix 5.15 source citations (web-02 `:309-314`, web-01 `:178,:181,:182`) re-verified by Read.
- The cap-order fix (finding 6) was traced through `may_dispatch`, the algorithm table, the Phase 5 intro and every scenario test; this is where B1 was found. The fix log says nothing about this interaction.
- Owner decision wording compared against `research/research-notes.md` lines 108-112.

**Tavily / web research:** none performed; every external-looking fact checked was either a local file or a read-only `gh` call against `cli/cli` (the upstream SuperClaude repo was never touched).

## Confidence Gate

- Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (PASS-eligible on coverage; the verdict is FAIL because of the open blocking finding B1, not because of coverage).
- Tool engagement: Read: 24 | Grep: 9 | Glob: 1 | Bash: 4 (all read-only: `ls`, `gh issue list --help`, `gh --version`, `gh api --method GET`, `sed`). Read+Grep+Glob (34) is at least the 15 checks.
- Not verified and not asserted: the count of test files that reference the `.claude/` mirrors (the fix log correctly dropped it); the real JSON key names of `gh project item-list` (open under Q8); live behaviour of `orca agent launch` (no live run is allowed).

## Recommendations

1. Fix B1 in the Phase 5 text only (algorithm step 3, `may_dispatch`, step 6 state, the three affected tests); no other section needs to change. This is the only open blocking finding, so one more fix pass and one more review (cycle 2 of 2) should close the gate.
2. Optionally fold N1 (the `shutil.which` seam and probe-timeout classification) and N2 (discovery truncation) into the same edit, since they touch the same plan steps; they are notes and are not required.

VERDICT: FAIL

Status: Complete

## QA Complete

