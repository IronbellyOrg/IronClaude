# QA Report — Fix Verification (Qualitative), Gate 3 Fix Cycle 2

**Topic:** GitHub issue watcher research report (issue #331)
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative)
**Fix cycle:** 2
**Fix authorization:** false (report only)
**Status:** Complete (Overall Verdict: FAIL, 2 blocking findings, see the last line)

Inputs: qa-consolidated-findings-phase6-cycle2.md, qa-fix-log-phase6-cycle2.md, RESEARCH-REPORT-issue-watcher.md; cycle-1 reports qa-fix-verification-phase6.md and qa-fix-verification-qualitative.md.

---

## Checks (appended incrementally)

### C1. Owner decision wording (D1-D3, option A decided, claim-only, integer-only, Coder#477) - PASS

- Read report l.129-149 (1.1, 1.2), l.583, l.653-662 (3.4), l.1331-1337 (7.1), l.1411-1417 (7.7), l.1836-1843 (9.1).
- D1 "option A ... decided by the owner" (l.135, l.1335, l.1838); D2 claim-only (l.136, l.1839); D3 integer-only (l.137, l.1840); Coder#477 "unnecessary unless B or C is revisited" with the repo boundary (l.149, l.660, l.1413, l.1842).
- Grep "pending owner|owner decision pending|awaiting the owner": 0 hits. Grep "decided by the owner": 8 hits. Grep "Coder#477": 63 hits.
- The cycle-2 edits did not touch these passages (the fix log "Not changed" matches what I read). INTACT.

### C2. Is the dispatch-record state machine coherent (states, lease, cap order)? - PARTLY (see F1, F4, F5)

Read in full: Phase 5 intro (l.1646), step 5.1 (l.1650), step 5.2 (l.1651), the algorithm table (l.1657-1671), test scenarios (l.1699-1717), exit codes (l.1690-1695), G9 (l.691), SC-8 to SC-10 (l.628-630), Test plan summary (l.1748-1762), Q13 (l.1863).

What now holds (traced state by state through steps 3, 6, 7, 11, 12):
- `pending`, `launched`, `unknown`: `wait` inside the lease (step 3 drops them with no `gh` call) and eligible after it (step 3 keeps them; step 7 gives `launch`, `retry-launch` or `abandon`). The unreachable branch of finding 1 is closed: a past-lease `launched` entry now reaches `may_dispatch`.
- `claimed` is set only in step 6 on an own marker; `claim.md:88` (read) is the claim comment ending in `<!-- sc:issue:claim -->`, Wave 6 item 2, the last write, so "marker exists means the claim ran to its end" holds. Step 3 drops `claimed` and `abandoned` always. Both terminal, as 5.1 says.
- `claim.md:20` (read): "No GitHub or ClickUp write happens before Wave 3". The code name `E-TIER-UNAVAILABLE` lives in `SKILL.md:62,130` and `refs/tiers.md:32` (read), not at `claim.md:20`; the citation supports the "writes nothing" half only (the fix log's example is right for the T3 spawn; see N3).
- Attempts arithmetic: step 11 writes `attempts + 1` before each launch; with `max_attempts` 3 a stranded claim is launched at attempts 1, 2, 3 and abandoned at the next past-lease look. The "Second cycle" row (second launch at attempts 2, abandoned after `max_attempts`, exit 3) matches.
- G9 (l.691), SC-10 (l.630), Phase 5 intro (l.1646), step 5.1, algorithm steps 3, 6, 7 and the tests (l.1702, 1703, 1707, 1708, 1709) state the same lease / retry / `claimed` rule. Grep for `marker-found` and `` `launched` `` shows no leftover of the old "write `launched` with marker-found" rule (hits l.691, 1650, 1661, 1664, 1665, 1670, 1701-1703, 1709 all consistent; l.1775 is the rollback row, consistent).

### C3. Cap order after the fix - FAIL (F1)

Algorithm step 3 (l.1661) now drops `claimed`, `abandoned` and in-lease `pending`/`launched`/`unknown` before it sorts and keeps `max_candidates`. That closes the handled-issue starvation the finding named. It does not close the same starvation for issues that stay in the discovery result and are never handled:
- The discovery query (l.1618) is `is:issue is:open status:Backlog label:<trigger> assignee:@me`. It carries no approval label; filter 2 (l.1608) is client side only. Every trigger-labelled, Backlog, assigned-to-me issue that is still waiting for approval (the normal intake state) is returned every cycle, has no dispatch entry, so step 3 never drops it, and it consumes one of the 10 candidate slots in steps 4 and 5 (a snapshot plus at least one events call) on every cycle forever.
- Candidates are sorted ascending (oldest first), so stale never-approved issues sit at the front. Ten of them hide every newer approved issue, which is exactly the "lowest-numbered 10 hide every new one" failure the step 3 text says it prevents (l.1661).
- The same happens to a past-lease `launched` entry whose issue is rejected in step 4, 5 or 8 (approval label removed after launch, a second assignee added): it is not terminal, step 7 is never reached, and it costs a slot every cycle. The new sentence "an entry past the lease costs at most one candidate slot before it becomes terminal ... or is retried" (l.1661) is therefore false for these entries.
- No test covers it: "Many already-handled candidates" (l.1709) uses only handled entries; "Cycle cap" (l.1705) is the launch cap. Grep for starv|max_candidates shows 4 hits (CycleConfig, step 3, options table, Q13) and no discussion of ineligible candidates.

### C4. Do the Phase 5/6 tests exercise the machine, including time past the lease? - PASS with F4 / N1

Checked row by row (l.1699-1717, 1729):
- "Second cycle": first cycle launches, second cycle inside the lease makes no `orca` call and reports `waiting`, the injected `now` is then advanced past the lease for the relaunch (attempts 2), and again to `abandoned` after `max_attempts` with exit 3; marker variant gives `claimed` and the next cycle drops it. Time past the lease is explicit, as the finding required.
- "Unknown outcome": inside the lease skipped; `now` advanced past it for `--retry-launch <id>` with the original argv from the stored `launch_cwd`; `cwd-changed` abandon covered.
- "Launch timeout": `unknown` with no id, exit 3, no call inside the lease, `abandoned` after it, never a call without `--retry-launch`.
- "Lost record" writes a `claimed` entry; "Many already-handled candidates" has three cases, case 3 (past-lease `launched` with a marker, becomes `claimed`, then consumes no slot) is the case the finding asked for.
- `now` is injected (`now: Callable[[], datetime]`, l.1651), so advancing time is possible without sleeping. e2e (l.1729) uses the real clock and tests only "no second `orca` line", which is inside the lease; consistent.
- `pending` after a crash and `failed` retry have no named scenario in the cycle list; the Test plan summary (l.1758) says `test_state.py` pins a "`may_dispatch` table", which is the only place they can be covered. Acceptable, noted as N2.
- Gap: no test that an entry rejected in step 4/5/8 while past the lease keeps costing a slot (F1), and no row for `abandon` being persisted (F4).

### C5. Injectable `which` lookup: consistent with the launch contract and the mocks? - FAIL (F2), rest PASS

Read step 3.4 (l.1592), 3.5 (l.1593), 3.6 (l.1594), 5.2 (l.1651), algorithm step 12 (l.1670), 6.1 and 6.2 (l.1728-1729), Test plan summary (l.1760). Verified against the source it mirrors: `install_user_setup.py:35` `_ORCA_CLIS = ("orca-ide", "orca")` and `:198-221` `_find_orca` (probe `skills list --json`, `orca-cli` topic, `continue` on `OSError`/`SubprocessError`/`ValueError`/`AttributeError`) - the report's description of the mirror is accurate. Host fact re-run with Bash `which -a`: `orca-ide` resolves to `/home/coder/.local/bin/orca-ide` (also `/usr/bin/orca-ide` and `/bin/orca-ide`, so the report's "lists" is a subset, harmless); `orca` resolves to `/home/coder/.config/orca/linux-orca-cli-shim/orca` and `/home/coder/.local/bin/orca`; `jq` is `/usr/bin/jq`.

Consistent:
- Unit and cycle level: `resolve_orca`, `launch_claim` and `run_cycle` take `which`; tests pass `lambda name: "/fake/" + name` or a dict (l.1594), `FakeOrca` answers the probe and has `not_orca` and `probe_timeout` modes (l.1593), `timeout` mode times out the launch call only. The probe-timeout rule (probe `CommandError` disqualifies the candidate; never `unknown`) and the launch-timeout rule (`unknown`, no id) do not overlap, and SC-9 / the "Launch timeout" row still hold because the probe is a separate call before the launch.
- e2e level: PATH is set to the stub directory only, `orca-ide` is stubbed too, `jq` is resolved to an absolute path before PATH is replaced, each stub logs `$0`, and the assertion that probe and launch are logged under `orca-ide` proves the run went through a stub. The reason given (a real `orca-ide` is on the real PATH) is true on this host. `CliRunner` runs in process, so `shutil.which` reads the patched `os.environ["PATH"]` at call time and finds only the stubs. Sound.

Not consistent (F2): the Test plan summary row for `test_cli_once.py` (l.1760) says the CLI tests monkeypatch `shutil.which` "(a fake lookup, never the real PATH)". But `launch.py` and `cycle.py` declare `which: Callable[[str], str | None] = shutil.which` (l.1592, l.1651). A default argument is bound when the function is defined, so `monkeypatch.setattr(shutil, "which", fake)` never reaches it. I demonstrated this with `uv run --no-project python -I -c` (default-arg call returned `None` after `shutil.which` was replaced by a fake; an attribute lookup at call time returned `/fake/x`). The `once` verb calls `run_cycle` without `which` (l.1652 says nothing else), so in `test_cli_once.py` `resolve_orca` uses the real `shutil.which`: on a host without Orca (CI) it raises `E-ORCA-NOT-FOUND` and every launch-path assertion fails; on a host with Orca it reads the real PATH. This is the host-dependence that finding 2 (NEW-2) set out to remove, still present for one test file, and the summary row claims the opposite.

### C6. Contradictions introduced by the cycle-2 fixes against SC-9, SC-10, G9, Section 8 and the Section 3 criteria - PASS for the fixed text; wording notes N1, F3, F5

- SC-9 (l.629, read): unknown outcome and timeout never start a fresh launch; abandoned after the lease. `may_dispatch` and the "Launch timeout" row agree.
- SC-10 (l.630) and G9 (l.691): rewritten in this cycle, consistent with step 5.1 and steps 3, 6, 7.
- SC-8 (l.628) says "A second poll cycle with the same issue does not launch again" and step 6.4 item 6 (l.1731) "A second cycle on unchanged state starts no second session". With the now-reachable retry, a cycle after the lease does launch again (up to `max_attempts`). The next-cycle reading of SC-8 still holds, so I grade it as wording (F3), but the criterion is unqualified.
- Section 7 / 6 (read l.1331-1437, l.1010-1114): no sentence says a launched issue is never re-selected; R10 "exactly one session per issue" is scored Partly, which already covers the retry.
- Sections 4, 6, 7, 8 against each other: G9 / SC-10 / Phase 5 / Q13 (l.1863: "too short a lease can relaunch a running claim") agree on lease and retry. No new cross-section contradiction found.
- External findings still supplement only: Section 5 header (l.754) states no external finding overrides verified code, and none of the cycle-2 edits adds an external claim.

### C7. Recommendation, B and C scoring, three questions of issue #331 - PASS

Read Section 6.0-6.1 (l.1010-1114), Requirement Scoring, Tally, Options Comparison (l.1256-1307), Revisit conditions (l.1309-1327), Section 7 (l.1331-1437). Recommendation is option A "decided by the owner" (l.1335); B and C are scored on the same rule (A 2 Meets, B 1, C 0, D 2, with the "does not credit" caveats l.1282-1290) and keep nine revisit conditions (l.1313-1323, repeated at l.1797-1807); Q-a, Q-b, Q-c are answered for A (l.1108-1112); the three questions of issue #331 are answered in the table at l.115-121; Coder#477 is a sibling dependency in the Coder repo that A makes unnecessary unless B or C is revisited (l.149, l.1413, l.1809).

### C8. Residual wording and carried points

- SC-8 / step 6.4 item 6 / G7 target (F3), `abandon` persistence (F4), `pending` after a crash versus SC-9 (F5), and notes N1 to N6 are listed in the Issues table.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cycle-2 finding 1 (NEW-1 / B1: unreachable `launched` branch) resolved substantively | PASS | Step 3 keeps past-lease `launched`/`pending`/`unknown`; step 6 sets `claimed`; step 7 reaches `may_dispatch`; tests l.1702, 1707-1709 advance `now` past the lease. Read l.1646-1671, 1699-1717 |
| 2 | Cycle-2 finding 2 (NEW-2: `resolve_orca` vs PATH stubs) resolved everywhere | FAIL | Resolved for unit, cycle, e2e; not for `test_cli_once.py` (l.1760): patching `shutil.which` cannot reach a def-time default (demonstrated with `uv run python -I -c`). F2 |
| 3 | State machine internally coherent (states, transitions, attempts, terminal states) | PASS | Traced every state through steps 3, 6, 7, 11, 12 (C2). Minor: `abandon` write not in step 7 (F4), `pending` rule (F5) |
| 4 | Cap order coherent (cap after local skip, no starvation) | FAIL | Handled issues no longer starve; ineligible-but-unterminated issues (unapproved, rejected after launch) still fill the 10 slots; the new "at most one slot" bound (l.1661) is false for them. F1 |
| 5 | Phase 5/6 tests exercise the machine, including time advanced past the lease | PASS | Rows l.1702, 1707, 1708, 1709 advance the injected `now`; `now` is a callable (l.1651); `pending`/`failed` only via the `may_dispatch` table (N2) |
| 6 | Injectable `which` consistent with the launch contract and the mocks (unit, cycle, e2e) | PASS | l.1592-1594, 1651, 1670, 1728-1729 read; `_ORCA_CLIS` and `_find_orca` read in source; `which -a` re-run |
| 7 | No contradiction with SC-9, SC-10, G9 | PASS | l.629, 630, 691 read against step 5.1 and the algorithm |
| 8 | Section 3 wording vs retry after lease (SC-8, criterion 6, G7 target) | PASS (note) | Next-cycle reading holds; unqualified wording recorded as F3 (MINOR) |
| 9 | Sections 4, 6, 7, 8 do not contradict each other after the fixes | PASS | l.691, 1025, 1304, 1374, 1646, 1863 read; consistent |
| 10 | Recommendation = option A decided by the owner; three questions answered; B/C scored with revisit conditions; Coder#477 statement; D1-D3, claim-only, integer-only intact | PASS | C1, C7 |
| 11 | External findings supplement and never override verified code | PASS | l.754; no external claim added in cycle 2 |
| 12 | Source claims added by the fixes are true | PASS (note) | `claim.md:20`, `:88`, `install_user_setup.py:35`, `:198-221`, `which -a` all verified; N3 on T2/T1 timing |

## Summary
- Checks passed: 10 / 12
- Checks failed: 2 (rows 2 and 4)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 2 (F1, F2)
- Minor findings recorded as notes: F3, F4, F5, N1-N6
- Issues fixed in-place: 0 (report only)

## Issues Found

| # | Severity | Blocking | Location | Issue | Required Fix |
|---|----------|----------|----------|-------|-------------|
| F1 | IMPORTANT | yes | Phase 5 algorithm step 3 (l.1661), step 5.1 (l.1650), discovery query (l.1618), tests (l.1709) | The cap-order fix covers handled issues only. Issues that stay in the discovery result and are never terminal (trigger label + assigned to me + Backlog, but not yet approved, or rejected in step 4, 5 or 8 after a launch) have no entry that step 3 can drop, are examined every cycle and fill the 10 slots, oldest first. Ten stale unapproved issues hide every newer approved one: the failure the step 3 text says it prevents. The added sentence "costs at most one candidate slot before it becomes terminal ... or is retried" is false for them, and no test covers them. | Pick one and say it in step 3: (a) add the approval label to the server-side query (`label:<approval>`), leaving only the approver-actor check client side; or (b) record a short-lived `rejected` skip (reason, until `now + lease`) so rejected numbers are dropped before the cap; or (c) apply `max_candidates` to examined-and-not-rejected issues and bound the cost by a call budget. Correct the "Bound" sentence. Add a test row: more than `max_candidates` unapproved lower-numbered issues plus one approved issue; the approved one is launched in the same cycle. |
| F2 | IMPORTANT | yes | Test plan summary row `test_cli_once.py` (l.1760); signatures at l.1592 and l.1651; `once` verb (l.1652) | The row says the CLI tests monkeypatch `shutil.which` ("a fake lookup, never the real PATH"). `resolve_orca`, `launch_claim` and `run_cycle` bind `which=shutil.which` as a default argument at definition time, so patching `shutil.which` later has no effect (demonstrated). `once` calls `run_cycle` without `which`, so `test_cli_once.py` uses the real lookup: it raises `E-ORCA-NOT-FOUND` on a host without Orca and reads the real PATH on a host with it. This is the NEW-2 host-dependence the cycle-2 fix claimed to remove. | Either make `commands.py` pass `which=shutil.which` at call time (module attribute looked up when `once` runs) and say so in step 5.3, or declare the defaults as `None` and resolve `shutil.which` inside the function; or make the CLI tests set PATH to a stub directory with `orca-ide` and `orca` stubs as step 6.1 does. Correct the l.1760 row to the mechanism actually used. |
| F3 | MINOR | no | SC-8 (l.628), step 6.4 item 6 (l.1731), G7 target (l.689), summary row `test_cycle.py` "no relaunch" (l.1759) | Unqualified "does not launch again" / "no second session" / "at most one session per workspace per issue"; after the lease a second launch is the designed retry (up to `max_attempts`). | Add "inside the lease" to SC-8 and criterion 6 and say "at most `max_attempts` launches, one per lease" in G7 |
| F4 | MINOR | no | Algorithm step 7 (l.1665) | `abandon` is "reported" but the write of the `abandoned` state is not stated, although step 3 and the "Second cycle" and "Launch timeout" rows rely on a persisted terminal `abandoned` (and dry-run behaviour is unstated). | Add "set the entry to `abandoned` (not in dry-run)" to step 7 |
| F5 | MINOR | no | `may_dispatch` `pending` rule (l.1650) | A crashed `pending` entry is relaunched fresh after the lease, while a timed-out launch (same epistemic state: reply lost, no id) is abandoned for a person (SC-9). Carried from cycle 1 as a minor note; not rechecked. | State the reason or treat `pending` like `unknown` without id |
| N1 | MINOR | no | cycle-1 notes | Unescaped pipes in code spans, `str(int(number))` wording vs the stricter validator (l.1361 vs l.1590), `D1..` default-ID collision, `-L 100` truncation: carried, not rechecked. | none |
| N2 | MINOR | no | Phase 5 scenario list | `pending`-after-crash and `failed`-retry/abandon have no named scenario; only the `test_state.py` "`may_dispatch` table" (l.1758) can cover them. | List the table rows |
| N3 | MINOR | no | l.225, 650, 703, 1044 | "`E-TIER-UNAVAILABLE` at Wave 1, before any GitHub write" holds for the T3 spawn only; T2/T1 workers are spawned in Wave 4 (`claim.md:54`, `refs/tiers.md:11-15`, read), after assignment and ClickUp. The plan's behaviour (lease, retry, cap) covers both cases. | Say "Wave 1 (T3) or Wave 4 (T2/T1)" |
| N4 | MINOR | no | Step 4.5 (l.1639) vs Q32 (l.1882) | Unit-level `FakeRunner` applies the `--jq` filter with `jq -c`, so unit tests need `jq`, but Q32 and step 6.1 say only the e2e tests skip without it. | Skip or declare the dependency for the unit helper |
| N5 | MINOR | no | Step 6.2 (l.1729) | `--worktree-path tmp_path/"checkout"` must exist: `subprocess.run(cwd=...)` on a missing directory raises `FileNotFoundError`, which `run_command` maps to `E-TOOL-MISSING`. | Create the directory in the test setup |
| N6 | MINOR | no | Exit code 3 (l.1695) vs step 3 reporting (l.1661) | Step 3 reports dropped `abandoned` entries every cycle; "an issue was abandoned" could keep exit 3 on every later cycle. | Say "newly abandoned in this cycle" |

## Actions Taken
None (fix authorization false). No file other than this report was written. The report `RESEARCH-REPORT-issue-watcher.md` was not modified.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

The spawn prompt carried no `## Inherited Structural Verdict` section, so this review ran in standalone mode. The structural cycle-2 report (`qa-fix-verification-cycle2.md`) exists in the same folder; I did not read it and rely on nothing from it.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited PASS items were relied on.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- `claimed` means "claim ran to its last write" - verified by Read of `claim.md:82-90` (Wave 6 item 2, claim comment with `<!-- sc:issue:claim -->`, is the last write before the final print).
- "`E-TIER-UNAVAILABLE` writes nothing (`claim.md:20`)" - Read of `claim.md:20` and `refs/tiers.md:11-15,32-40` and grep of `SKILL.md`: true for the T3 spawn, not for T2/T1 (N3).
- `resolve_orca` mirrors `_find_orca` - Read of `install_user_setup.py:198-221` and Grep of `_ORCA_CLIS` (`:35`): accurate.
- Host fact "both candidate names resolve on the real PATH" - Bash `which -a orca-ide`, `which -a orca`, `which -a jq`: confirmed (and `orca-ide` also at `/usr/bin`, `/bin`).
- `monkeypatch` of `shutil.which` versus a default-argument binding - executed `uv run --no-project python -I -c` demonstration: the default-bound call returned `None` after `shutil.which` was replaced (basis of F2).
- Cap starvation (F1) - Read of the discovery query (l.1618), the five-filter table (l.1608) and the algorithm; Grep for `starv|max_candidates` (4 hits, none about ineligible candidates).
- State-by-state trace of `may_dispatch` against steps 3, 6, 7, 11, 12 and each test row (C2, C4).

## Confidence and tool engagement

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (the percentage measures completed verification of the 12 checks, not a pass; 2 checks verified as FAIL)
- **Tool engagement:** Read: 16 | Grep: 12 | Glob: 1 | Bash: 3 (`wc`, `which -a`, `uv run python -I -c` demonstration) - well above 12 checklist items
- Web research: none performed (all claims are repo-local or host-local), so no Tavily/fallback record is needed.

## Recommendations
- Fix F1 and F2 in the report (two targeted edits in Phase 5 / Test plan summary), then this is a fix-cycle-2 outcome: per the review loop rule (at most 2 fix cycles, 3 reviews) there is no cycle 3. The task file says to HALT and escalate to the user with these two open blocking findings; the user decides whether to accept them as plan notes or to have them edited without a further review.
- F3 to F5 and N1 to N6 stay notes.

## QA Complete

Status: Complete

VERDICT: FAIL
