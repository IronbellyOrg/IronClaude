# QA Report - Fix Verification, Gate 3 (Phase 6), Fix Cycle 2

**Topic:** GitHub issue watcher research report (issue #331)
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 2
**Fix authorization:** false (report only)
**Status:** Complete

Name overrides applied (per the dispatching message): cycle-1 reports are `qa/qa-fix-verification-phase6.md` and `qa/qa-fix-verification-qualitative.md`; the cycle-2 fix log is `qa/qa-fix-log-phase6-cycle2.md`; the cycle-2 findings are `qa/qa-consolidated-findings-phase6-cycle2.md`. This file is written at the primary path (no hook block on the path itself; one freshness hook asked for a Read first, which was done).

Report under test: `RESEARCH-REPORT-issue-watcher.md` (mtime 2026-11-07 10:22:58; fix log mtime 10:23:40; the report was not modified after the fix log was written). Line numbers below are from a Read of that state.

---

## Section A. Blocking finding 1 (NEW-1 / B1): launched-entry retry branch unreachable

Test applied: the state machine must say one thing in the Phase 5 intro, `may_dispatch`, steps 3, 6 and 7, the test scenarios, G9 and SC-10.

| # | Location (report line) | What it says now | Consistent? |
|---|---|---|---|
| A1 | Phase 5 intro, l.1646 | Dispatch record skips a stranded issue while the lease runs, then retries it; attempt cap and an `abandoned` report end the retries; an own marker makes it `claimed` and it is never launched again (points to the state table in step 5.1) | PASS |
| A2 | `DispatchEntry.state`, l.1650 | Literal now has six states including the new terminal `claimed` | PASS |
| A3 | `may_dispatch`, l.1650 | One wait window: `pending`/`launched`/`unknown` give `wait` while `now - last_at < lease`, eligible after it; after the lease `pending`/`launched` give `launch` (attempts < max) else `abandon`; `unknown`+id gives `retry-launch` (cwd must match, else `abandon` `cwd-changed`); `unknown` without id waits then `abandon`, never `launch`; `failed` gives `launch`/`abandon`; `abandoned` and `claimed` give `wait` (terminal). States that step 3 and step 7 apply the same table | PASS |
| A4 | Step 3, l.1661 | Drops `claimed` and `abandoned` always, `pending`/`launched`/`unknown` only while `now - last_at < lease`; a past-lease entry is explicitly NOT dropped and stays a candidate; the cap applies after the local skip; bound stated (one slot before the entry is terminal or retried). The previously unreachable branch is now reachable | PASS |
| A5 | Step 6, l.1664 | Marker found (and not dry-run) sets the entry to `claimed` (`marker-found`), new entry attempts 0 or existing attempts kept, whatever state; a marker ends any retry | PASS |
| A6 | Step 7, l.1665 | States what reaches `may_dispatch`: new, `failed`, or `pending`/`launched`/`unknown` past the lease; matches steps 3 and 5.1 | PASS |
| A7 | `CycleReport`, l.1651 | `claimed: list[int]` added next to `waiting`, `abandoned`; matches step 3 "reported as `claimed`, `abandoned` or `waiting`" | PASS |
| A8 | Test "Second cycle", l.1702 | `launched` entry: inside lease no call and `waiting`; past lease (now advanced) exactly one `launch`, attempts 2; at `max_attempts` `abandoned`, exit 3; marker variant gives `claimed` and step-3 drop next cycle. Matches A3-A5 | PASS |
| A9 | Test "Lost record", l.1703 | Empty store plus marker: no launch, `claimed` entry with `marker-found`. Matches A5 | PASS |
| A10 | Test "Unknown outcome", l.1707 | Inside lease `waiting`; time advanced explicitly past the lease before the `--retry-launch` assertion; `cwd-changed` case. Matches A3 (the cycle-1 gap that time was not advanced is closed) | PASS |
| A11 | Test "Launch timeout", l.1708 | `unknown` no id; inside lease no call; past lease `abandoned`, never a launch. Matches A3 | PASS |
| A12 | Test "Many already-handled candidates", l.1709 | Case 1 (`claimed`/`abandoned`/in-lease `launched` dropped before the cap), case 2 (marker only: recorded `claimed`, dropped next cycle), case 3 (past-lease `launched` plus marker: examined once, becomes `claimed`, consumes no slot afterwards). Matches A4 and A5 | PASS |
| A13 | G9 last cell, l.691 | "a `launched` entry is skipped only inside the lease, then retried or reported `abandoned` unless the claim marker exists (then `claimed`)"; refers to step 5.1 | PASS |
| A14 | SC-10, l.630 | "skipped inside the lease, then retried until the retry cap and reported `abandoned`; an issue with an own claim marker becomes `claimed` and is never retried" | PASS |
| A15 | Other mentions (Grep over the whole report for `launched`, `lease`, `abandon`: l.629, 882, 885, 1428, 1541, 1695, 1855, 1863, 1987, 2051) | None contradicts the table (l.629 "abandoned after the lease for a person to inspect" is the `unknown` case) | PASS |

Source citations behind finding 1, re-read: `claim.md:88` (claim comment ending with `<!-- sc:issue:claim -->` is Wave 6 item 2, the last write) holds; `claim.md:20` says "No GitHub or ClickUp write happens before Wave 3" and supports the "writes nothing" half of the claim; the name `E-TIER-UNAVAILABLE` itself is defined in `sc-issue-protocol/SKILL.md:62,130` and `refs/tiers.md:32`, not at `claim.md:20` (see note N2).

**Result for finding 1: RESOLVED.** The state machine is consistent across all eight places; the previously unreachable retry/abandon branch is now reachable and tested.

## Section B. Blocking finding 2 (NEW-2): `resolve_orca` and the PATH-stub tests

| # | Location (report line) | What it says now | Result |
|---|---|---|---|
| B1 | Step 3.4, l.1592 | `resolve_orca(orca, *, which=shutil.which, names=("orca-ide","orca"))`: the lookup function and the candidate names are parameters, so tests never read the real `PATH`. A `CommandError` from the probe (`E-TIMEOUT`, `E-TOOL-MISSING`) disqualifies that candidate and the loop continues; none found raises `E-ORCA-NOT-FOUND`; a probe timeout is never mapped to `unknown` | PASS |
| B2 | Step 3.4, l.1592 | `launch_claim(..., which=shutil.which)` passes `which` to `resolve_orca`; the launch-timeout rule (`unknown`) is limited to the launch call, not the probe | PASS |
| B3 | Step 5.2, l.1651 and algorithm step 12, l.1670 | `run_cycle(..., which=shutil.which)` and step 12 calls `launch_claim(..., which=which)`; the plumbing is complete from cycle to probe | PASS |
| B4 | Step 3.5, l.1593 | `FakeOrca` answers the probe with `{"topics":[{"name":"orca-cli"}]}`, has `not_orca` and a new `probe_timeout` mode; `timeout` mode times out the launch call only | PASS |
| B5 | Step 3.6, l.1594 | `resolve_orca` is always tested with a fake `which`; cases: accept, skip non-JSON/non-zero, skip probe timeout (next candidate or `E-ORCA-NOT-FOUND`, never `unknown`), prefer `orca-ide`, none qualifies; `launch_claim` probe timeout gives `failed`, launch timeout gives `unknown`. This also covers the cycle-1 verifier note N1 | PASS |
| B6 | Step 6.1, l.1728 | `install_stubs` writes `gh`, `git`, `orca` and `orca-ide` (same script); the fixture sets `PATH` to the stub directory only (explicitly not the `make_repos` prefix form); stubs use absolute `#!/bin/bash` and an absolute `jq` resolved before `PATH` is replaced | PASS |
| B7 | Step 6.2, l.1729 | e2e runs with the default `which` against the restricted `PATH`, so `orca-ide` is tried first and resolves to its stub; each stub logs its program name (`$0` basename); the test asserts probe and launch are logged under `orca-ide` | PASS |
| B8 | Test plan summary, l.1760 | `test_cli_once.py` is listed as monkeypatching `build_runners` and `shutil.which` (see note N1 on how that is wired) | PASS with note |

Host fact re-run by me: `which -a orca-ide` printed `/home/coder/.local/bin/orca-ide` (also `/usr/bin/orca-ide` and `/bin/orca-ide`); `which -a orca` printed `/home/coder/.config/orca/linux-orca-cli-shim/orca` and `/home/coder/.local/bin/orca`. This matches l.1592 (the report lists a subset of the `orca-ide` hits, which is accurate for the point made).

Precedent citations re-read in `src/superclaude/cli/install_user_setup.py`: `_find_orca` at l.198-221 (verified), `_ORCA_CLIS = ("orca-ide", "orca")` at l.35 (Grep), `except (OSError, subprocess.SubprocessError, ValueError, AttributeError): continue` at l.217-218 (verified), probe `["skills","list","--json"]` and the `orca-cli` topic test at l.209-219 (verified). The report's mirror of that logic is accurate.

Reachability reasoning: with `PATH` equal to the stub directory, `shutil.which("orca-ide")` can only return the stub; the `gh`, `git`, `orca`, `orca-ide` argv[0] values in the report are bare names or the stub path, so no real Orca binary can be probed or launched in the e2e tests. The unit and cycle tests inject `which` and the runner. Both halves of the "nothing runs live" rule (l.1466) now hold.

**Result for finding 2: RESOLVED.**

## Section C. New blocking issues introduced by the cycle-2 fixes

| # | Check | Result | Evidence |
|---|---|---|---|
| C1 | Broken tables (row column counts) | PASS with note N3 | Rows edited in cycle 2 were counted with awk: l.1593 and l.1594 have the normal 4 separators; l.1592 and l.1651 each carry one extra unescaped pipe from `Callable[[str], str | None]` (Grep `[^\\]\| None` hits l.1592 and l.1651). This is the same defect class that both cycle-1 reports and the cycle-2 findings file (l.12) already graded minor (17 such hits exist in the report, 259 to 1879, most older than cycle 2). Graded minor for consistency; raw Markdown text is complete and correct |
| C2 | `[CONTRADICTION` tokens | PASS | Grep for `CONTRADICTION` (case-insensitive) hits only the heading "4.4 Contradictions ...", the prose rows at l.743, 909, 1046, 1900-1901, 2031 and `[CODE-CONTRADICTED]` tags; no `[CONTRADICTION` token |
| C3 | Placeholders (`TBD`, `TODO`, `FIXME`, lorem) | PASS | Same Grep: no hit other than the word "placeholder" in ordinary prose at l.333 and "names are placeholders" in Phase 7 |
| C4 | Section order | PASS | Grep of `^#{1,3} ` shows `## 1.` to `## 10.` in order (l.102, 153, 575, 675, 752, 990, 1331, 1441, 1830, 1906) and `## Appendix A.` at l.1993; no heading was added, renamed or moved |
| C5 | Table of Contents | PASS | Read of l.10-99: every ToC entry matches a heading in the Grep output (sections 1-10, subsections, Phase 1-7, Test plan summary, Rollback, Follow-up, Integration Checklist, Appendix A.1-A.3). The fix log says no heading changed; confirmed |
| C6 | Binding addenda | PASS | l.1057 heading "Option A ... Decided by the owner (ADDENDUM 2)"; l.1335 "Option A ... decided by the owner"; Grep for "pending owner decision" and "owner has not decided" returns nothing; B and C have their own sections (l.1116, 1168), "Requirement Scoring" (l.1256), "Options Comparison" (l.1292) and "Revisit conditions for options B and C" (l.1309); l.1413 states Coder#477 is a sibling dependency in the Coder repo, that option A makes it unnecessary unless B or C is revisited, and that its listener, registration and transport live in the Coder repo; integer-only rule is D3 (l.1522, 1590, 1754) |
| C7 | False claims in the text added by cycle 2 | PASS with note N2 | Verified against source: `_find_orca` and `_ORCA_CLIS` (above), `claim.md:88`, `claim.md:20`, host `which -a` output. The only imprecision is the `E-TIER-UNAVAILABLE`/`claim.md:20` pairing (N2) |
| C8 | Fix log matches the report | PASS | Every change the log lists was found in the report at the lines cited in Sections A and B (state `claimed`, `CycleReport.claimed`, step 3/6/7 wording, tests, G9, SC-10, `resolve_orca` parameters, `probe_timeout`, `orca-ide` stub, PATH restricted); the log's "no heading changed" matches C4 and C5 |

**Result: no new blocking issue found.**

## Notes (MINOR; not rechecked in later rounds)

| # | Location | Note |
|---|---|---|
| N1 | Test plan summary l.1760; step 3.4 l.1592; step 5.2 l.1651 | `which=shutil.which` is a default argument, bound when the function is defined. `monkeypatch.setattr(shutil, "which", fake)` in `test_cli_once.py` therefore does not change that default. The verb (step 5.3, l.1652) does not say it passes `which` explicitly. When the implementer wires the verb, it should pass `which=shutil.which` evaluated at call time (or the test should patch the name in `commands.py`), otherwise `test_cli_once.py` depends on the host's real `PATH`. The e2e test is unaffected because it restricts `PATH` |
| N2 | l.691, l.1646, l.1650 | `E-TIER-UNAVAILABLE` is cited to `claim.md:20`; that line only says no write happens before Wave 3. The error name is defined in `sc-issue-protocol/SKILL.md:62,130` and `refs/tiers.md:32`. The claim made (it writes nothing) is true |
| N3 | l.1592 and l.1651 | One unescaped pipe in `Callable[[str], str | None]` splits the table cell in GFM renderers and would hide the rest of the Details cell in rendered view. Escape as `str \| None` |
| N4 | Step 5.1 and algorithm step 7 (l.1650, l.1665) | Step 7 says `abandon (reported)` but does not say the entry is written as `abandoned`. The tests (l.1702, 1708) and the step-3 bound say the entry becomes `abandoned`, so the behavior is pinned; adding "and write `abandoned`" to step 7 would remove the ambiguity |
| N5 | Carried from cycle 1, not rechecked | Other unescaped pipes in code spans, `str(int(number))` wording, `D1..` ID collisions, `pending` wording versus "never retry as a fresh launch", `-L 100` truncation |

## Summary

- Blocking findings in the cycle-2 consolidated findings: 2. Resolved: 2. Still open: 0. New blocking: 0.
- Checks: Section A 15, Section B 8, Section C 8 = 31 total; passed 31 (three with minor notes); failed 0.
- Critical issues: 0. Important issues: 0. Minor notes: 5 (N1 to N5).
- Monotonicity (cycle 1 to cycle 2): open blocking findings 2 before this fix, 0 now; no regression of a previously resolved item (findings 1 to 5 and 7 to 12 of cycle 1 were not re-opened; the cycle-2 edits touch only Phase 3, Phase 5, Phase 6, G9 and SC-10 and the checks in Section C found nothing broken elsewhere).
- Fix cycle count: 2 (third review). No open blocking findings, so no escalation is needed.

**Confidence:** Verified: 31/31 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 15 | Grep: 9 | Glob: 1 | Bash: 2 (one `which -a` host check, one `stat`/`awk` pipe-count check, both read-only). No web research performed.

Adversarial self-audit: I looked for state-machine gaps (dropped-before-cap, reachability of each `may_dispatch` branch, who writes `abandoned`, whether `failed` needs a lease), for a way the e2e test could still reach a real Orca (default-argument binding, PATH prefix versus replace, candidate names), and for table damage in the edited rows. The findings that survived are the minor notes above; none changes behavior, makes a claim false, or removes a deliverable.

VERDICT: PASS

**Status:** Complete

## QA Complete

