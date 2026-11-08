---
claim_class: runtime_behavior
evidence_class: source_static   # I executed nothing; I read the code, tests, design, spec and decision register. The 2635-pass pytest run is the orchestrator's.
verdict_direction: AFFIRM       # AFFIRM = the safety-critical promises hold in the code as read; deviations are documentation or contract level. No HIGH finding.
self_reported_confidence: 0.72
---

## Root-cause and deviation register

Short paths: IW = src/superclaude/cli/issue_watch ; T = tests/issue_watch ; PKG = .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955 ; TL = PKG/TASK-RF-...md (tasklist) ; D = docs/designs/issue-watcher.md ; S = spec-final.md.

| id | category | location | what diverged | evidence | sev | authorizing artifact |
|---|---|---|---|---|---|---|
| C1a | Authorized expansion | IW/record.py:23-29 | record imports three predicates FUNCTIONS (format_utc, parse_utc, valid_issue_number) though D:239 says "types only" | TL:332 (Step 4.1a names the three); TL:998 PRE-11 logs the mismatch; T/test_module_boundaries.py:15-22,57-61 states the widened rule in its docstring | LOW | Step 4.1a (plan item), PRE-11. D:239 was never amended (doc drift) |
| C1b | Necessary deviation | IW/record.py:183,585,607; IW/predicates.py:57-67 | fourth function valid_operation_id added by fix B-10. B-10 calls it "within design 5.3", which is false for a function import | record.py:182 inline reason ("status prints this id inside a shell command"); predicates.py:60-62; launch may import only runner (D:240), so record cannot reuse launch's pattern | LOW | none; no AC contradicted. AC-25 passes only because the test rule was widened (test_module_boundaries.py:57-61) |
| C2 | Drift | IW/cli.py:319 (via cycle.py:29) | cli reaches predicates.format_utc through cycle's namespace; D:242 gives cli no predicates | TL:1046 item (3) records it as a "judgment call" only; the AST walker sees imports only (T/test_module_boundaries.py:72-75) | LOW | none. Disclosed in the log, not authorized |
| C3a | Necessary deviation | IW/predicates.py:57 vs IW/launch.py:36 (+127,274) | OPERATION_ID_PATTERN exists twice | predicates.py:60-62 gives the reason; T/test_launch.py:198-200 pins pattern and flags equal; LaunchOutcome.__post_init__ launch.py:251-259 re-checks | LOW | none needed. Fail-closed in both directions (see C3-dir) |
| C3b | Drift | predicates.py:20,54; launch.py:30,90; audit.py:203,236; record.py:132 and launch.py:33 (digit counts {0,8}) | the 999_999_999 bound has 3 named copies plus 2 digit-count encodings. Only audit is pinned (T/test_audit.py:484); launch vs predicates is NOT pinned (grep of T for MAX_ISSUE_NUMBER: only test_audit.py). The login regex is also duplicated (cycle.py:468, github.py:134) with no parity test | | LOW | none |
| C3-dir | (answer: is each divergence fail-closed?) | | Yes. launch bound > predicates: github.discover rejects the number first (github.py:828). launch bound < predicates: build_claim_prompt raises ValueError, so cycle._fail(prompt_invalid) (cycle.py:1024-1026), then 3 attempts, then abandoned. audit bound < predicates: ValueError in decision_line AFTER the launch, so a crash with pending on disk (see A5). Pattern split: ValueError, entry stays pending. None of these launches twice; the helper's MEDIUM overstates it | | | |
| C4a | Authorized expansion | IW/audit.py:81,82,98,99,101 | marker_unreadable, edits_unreadable, dry_run_shadow_reset, reset_refused, operator_reset: 5 names beyond the spec's 52 | count verified: 80 matching rows in audit.py minus 18 (_TYPES) minus 3 (_KEYS) = 59; S:332-358 lists 52 | LOW | DF-02, DF-03, DF-22, DF-57 (PKG/research/06-gap-fill-decisions.md lines 25, 26, 149, 191) |
| C4b | Necessary deviation | IW/audit.py:57,64; cycle.py:1134-1137; cli.py:123-129 | cycle_complete (exit 0) and cycle_crashed (exit 1) added by the executor at Gate C. A closed enum has no reason for a normal cycle or a crash. `once` can now exit 1, but D:114 lists once exits 0,2,3,4,5,6,7,75 | inline [PROPOSAL] comments at audit.py:55-56,62-63; runbook docs/designs/issue-watcher-setup.md:318,331,344 documents both; D never lists them | MEDIUM | none from the owner. Three sources now disagree (spec 52, design silent, runbook 59). Literal AC-17 ("exit codes match section 4") is arguably contradicted for exit 1 |
| C4c | Authorized omission + Drift | IW/cycle.py:635-641; audit.py:94 | `re-approved` is in the table. cycle.py DOES contain a branch that sets note="re-approved", but it is unreachable and has no cycle-level test. OQ-49 says "This task adds no code for it" | `_approve` is reached only for entries that are None, `failed` (record.fail 503-525 sets no approval ids) or an attempts_exhausted tombstone (also none). Every other state exits earlier (cycle.py:901-914), so e.approval_event_id is always None there. Grep: "re-approved" appears in T only in test_audit.py (93,156,165,248,327,800) | LOW | OQ-49 (TL:975) authorizes the omission of the S:272 behaviour; the dead branch itself is unauthorized |
| C5 | Necessary deviation | T/test_cli.py:967,1070 (NOT_ROOT used at 1259,1627,1653); test_record.py:739; test_cycle.py:735,4694 | skip/skipif although the plan forbids SKIP | disclosed TL:908 and TL:1050, graded minor. Root-guarded test functions = 6 (967,1259,1627,1653,735,739) plus 1 platform skip (4694) | LOW | none; no AC contradicted |
| C5-a | (answer to your question) | | As root they report SKIPPED; they cannot silently pass. What goes unproven as root: status exit 6 on unreadable store (cli.py:175-177), init-state/reset exit 6 on an unwritable dir, unreadable approvers file (cycle.py:325-328), unopenable lock (record.py:396-397). The foreign-owner lock and owner checks are monkeypatched and are not skipped (test_record.py:753-760, test_cycle.py:678-682) | | | |
| C6 | Drift (alt reading: Regression of NFR-014, behaviour-neutral) | IW/audit.py:395-397 via cli.py:79,127,219; IW/runner.py:89,110,120,129 | NFR-014 says every time read goes through the Clock (S:231). stderr_fallback reads the wall clock when ts is None; runner reads time.monotonic | audit.py:390-392 and the module header call it "a stamp, not a decision"; the only other wall-clock read is SystemClock (cycle.py:377,380); CommandResult.duration_s is never read (runner.py:35) | LOW | none. cli.py could pass cycle.SystemClock().now() |
| C7 | Drift (documentation) | TL:847,883,199..975 ("57"), 907, 1050 | stale statements in the executed task file: "13 fixtures" (19 on disk), template placeholder at 883, 57 vs 59 names, OQ-43/OQ-44 (3.10, markdownlint) said absent but found. Log line refs are stale too: log says test_cycle 4635, test_cli 889/992, real lines are 4694, 967/1070 | TL:905-908 and TL:1050 disclose most of it. Risk: a resumed Step 2.3/2.8 would re-pin 57 names against the 59-name test | LOW | disclosed, not authorized |
| C8a | Authorized | cycle.py:1010-1016 | dry-run skips re-read and Orca probe | D:362 says step 12 stops before find_orca and reports probe: skipped. OQ-39 (TL:969) covers only the decision-line reason, so cite D:362 | LOW | design 6.2 |
| C8b | Authorized | cycle.py:644-649,738-742 | Retry-After honoured only on G1 | DF-51 (06 line 185); D 598-602 (NOT read by me) | LOW | DF-51 |
| C8c | Authorized | launch.py:119-132 | FR-015 full retry argv | DF-50 X2; D:866 Q2 | LOW | DF-50 |
| C8d | Authorized | cycle.py:814-815 | FR-016 S1: any launch-step outcome halts the cycle | D:386-388 states it, including "after any launch-step outcome" | LOW | D 6.3, DF-50 |
| C8e | Authorized | T/test_cli_e2e.py:11-13 | NFR-008/AC-19 split | DF-55 (06 line 189) | LOW | DF-55 |
| C8f | Not a deviation | | NFR-012/AC-23 gate-only | AC-23's own text is "gates pass" (D:896) | n/a | |
| C8g | Authorized | launch.py:343-355; runner.py:70-72 | launch runs with cwd=worktree; Runner.run gained a cwd kwarg | DF-01 (06 line 24); D 625 | LOW | DF-01 |
| C9 | Grounding Gap, not a deviation | main.py:563-565 | all six Click symbols DEGRADE | verified against ~/.claude/skills/sc-reflect-protocol/refs/runtime-surface.md:40 (rule a, decorators), :41 (rule b, pyproject.toml:71), :42 (rule c, add_command), and §3 which forbids UNREACHED/Regression. T/test_cli_e2e.py:101-127 runs `python -m superclaude.cli.main issue-watch <verb>`, but only for once and init-state. status, check-config and reset run only through the group object (CliRunner) | LOW | oracle |
| C10 | Authorized | commit 26f551f4 | 379 files, parent == BASE e8db2fe6 (git). Visible groups: TASK-RF qa 109, phase-outputs 83, reflect 43, research 6; TASK-RESEARCH qa 58, phase-outputs 11, research 6, synthesis 4 (79 in the groups shown; the helper's 83 not fully re-counted) | project CLAUDE.md: ".dev/tasks/ Is Always Staged". `git status -- docs src tests` is clean, so docs/designs/issue-watcher.md in HEAD equals the tree. "Unchanged from the pre-task file" is UNVERIFIED (DF-07/DF-31 only) | LOW | CLAUDE.md rule. Residual: S (.dev/brainstorms/...) and .dev/issues/331 stay untracked while D/T/DF cite them |

Additional findings from my own pass (A1-A12; [INFERRED] where marked):

| id | category | location | finding | sev |
|---|---|---|---|---|
| A1 | Fail-open on skew (design-conformant) | IW/record.py:689-690,699-703 | The day cap is closed at `now` (D:500,505), so a consumed_at LATER than now is not counted. After a backward clock step (NTP step, VM restore) recent launches are undercounted and the cap of 6 can be exceeded. The only guard is a clock_skew warning at cycle.py:755-756, which stops nothing. Every other time rule fails closed on skew (backoff, lease, next_permitted_at) | MEDIUM [INFERRED impact] |
| A2 | see C4c | cycle.py:635-641 | dead branch | LOW |
| A3 | Reporting regression | record.py:423 vs 425-431; cycle.py:1255 | disabled() uses lexists (a dangling symlink counts) but disabled_since() uses os.stat, which follows the link. A dangling-symlink DISABLED stops cycles while `status` prints "disabled since: no". Any OSError other than FileNotFoundError escapes status_report uncaught. The kill switch itself is unaffected | LOW |
| A4 | Design limit | cycle.py:1033-1062 | DISABLED is checked once at 1033, then comes the origin git call (<=10 s, 1041-1045), then a durable write, then the spawn. A `touch DISABLED` in that window is not honoured. D:355 fixes this order, but a re-check between 1049 and 1052 is cheap and leaves no pending entry | LOW |
| A5 | Gap | cycle.py:685-690,1062-1106; cli.py:121-129 | `_locked_body` catches only `_Stop`. Any other exception after the spawn (decision-line build via audit.py:246-258 on a bad host token, audit.py:219-221,234; a ValueError from record.mark_*) skips `_commit`. The entry stays `pending`, is swept to pending_orphan, the operation_id and retry hint are lost, the exit is 1 cycle_crashed, and no audit.jsonl line is written. At-most-once holds (pinned by T/test_crash_injection.py:327-339) | LOW (observability, not safety) |
| A6 | Untested real-world risk [INFERRED] | runner.py:91-101,125-126 | subprocess.run(capture_output=True) waits on the stdout/stderr pipes. If `orca agent launch` leaves a background process holding them, communicate() blocks until the 120 s timeout, so every successful launch becomes `unknown` (launch.py:320-321, exit 7). PATH stubs exit at once and cannot show it. Only stderr is capped (runner.py:15,126); stdout is not | LOW |
| A7 | Hardening [INFERRED] | cycle.py:307-324 | The approvers file is the authorization allow-list. Owner and mode are checked on os.lstat(path); the later open uses O_NOFOLLOW but there is no fstat on the opened fd, and the parent directory mode is not checked. Exploiting it needs write access to the parent dir | LOW |
| A8 | Dead code | cycle.py:35 (MAX_LAUNCHES_PER_CYCLE, never used); record.py:748 (disabled_present, no production caller); cycle.py:1235,1244 + cli.py:173 (status_report's audit arg and an AuditLog built for nothing); runner.py:35 (duration_s). The one-launch rule is enforced only by the halt flag at cycle.py:814-815 | | LOW |
| A9 | Defense-in-depth | record.py:538-568 | S:272 says a fresh launch requires launches == 0. mark_pending checks state only. It is safe today because validate rejects failed+launches 1 (record.py:208) and `_examine` branches on state, but there is no explicit guard | LOW |
| A10 | Operational trap (fail-closed) [INFERRED] | predicates.py:205-209 | Same-second tie detection scans the WHOLE label history. If a human adds trigger and approval in one `gh issue edit` (same second), the issue is events_incomplete forever, and re-applying the approval label cannot clear the old tie. S:92 words the rule that way, so this is conformant, but the documented re-arm (S:94) does not rescue this case. Runbook setup.md:174 only says "wait a few seconds" | LOW-MEDIUM |
| A11 | Helper corrections | coverage-matrix.yaml, FR-027 note | It says the owner-check and unreadable-file cases are skipif root. Wrong: the owner check is monkeypatched and runs (test_cycle.py:678-682); only the unreadable-file case (735) skips. The "5 sites" count understates the number of skipped test functions (6, plus parametrization at 1627) | LOW |
| A12 | Reproducibility | S and .dev/issues/331 untracked | the authority chain cites S line numbers and DF ids, and S is not in the commit. CLAUDE.md only forces .dev/tasks, so this is not a rule breach | LOW |

Safety properties re-verified against code, no counterexample found:
- **Pending durable before spawn:** mark_pending (cycle.py:1060), then _save (1061: write_prepared_bytes fsyncs the file, atomic.py:28-32, then dir fsync at record.py:378; an OSError raises _Stop before 1062), then launch (1062). The C1-C5 tests are real (test_crash_injection.py:217-374).
- **Integer-only prompt:** build_claim_prompt (launch.py:84-92) uses `type(n) is int`; launch_argv re-checks PROMPT_PATTERN with fullmatch (launch.py:101-102); retry_argv validates the id (launch.py:127).
- **No GitHub write:** the argv builders at github.py:175-262 are GET or fixed GraphQL queries. No title or body is requested; the body is touched only through jq `contains`, which yields a boolean (github.py:61-65).
- **No shell:** runner.py:91-101 uses shell=False; cli.py uses shlex only to print.
- **Fail-closed reads:** _rest_read and _graphql_read return incomplete on page cap, repeated id or cursor, and an errors key (github.py:592-702). Marker, edits, events and project failures all skip. The approvers regex rejects any odd line (cycle.py:335).
- **Kill switch, day cap, deadline:** the kill switch is checked at start (cycle.py:693) and mid-cycle (1033). The day cap is checked before reads (917) and again after the re-read (1031). Deadline guards sit at 1017 and 1039-1049. The residual is that nothing checks after the pending save (ON-01).

## Coverage and acceptance

**Re-verified against code (Read).** All the FR/NFR implementation line ranges I spot-checked in coverage-matrix.yaml match:
- FR-010 cycle.py:1052-1062
- FR-011 960-997
- FR-012 launch.py:84-102
- FR-013 343-355
- FR-016 814-815
- FR-024 848-857, 917, 1031
- FR-025 1039-1049
- FR-028 644-649, 738-742
- FR-029 383-412
- NFR-009 github.py:437-463
- reachability RC-2 order

The IE-01 to IE-05 line and call-site numbers also match. One helper claim is corrected (A11).

**Not re-verified:**
- The "bites" judgments for tests I did not open. I read test_crash_injection.py 150-374, test_cycle.py 2895-2954, test_module_boundaries.py 1-100 and test_cli_e2e.py 1-135, plus grep-level checks elsewhere.
- The Python 3.10.20 run and the "4 environmental failures".
- DF-50 and DF-51 beyond the first ~400 characters.
- D 598-602.

**Strongest proofs:**
1. Crash injection C1-C5 with byte-level store comparison and rerun counts (test_crash_injection.py:217-374).
2. Pending-before-launch snapshot taken inside the launcher callback (test_cycle.py:2925-2954), plus the e2e stub snapshot (RC-2).
3. The AST import walker with negative self-tests (test_module_boundaries.py header).

**Weakest:**
- (a) Every gh and Orca reply shape is an `_assumed_shape` fixture; the live test is the real proof and has not run.
- (b) NFR-012/AC-23 rest on gate output only.
- (c) NFR-008/AC-19 are never chained end to end (DF-55).
- (d) NFR-014's clock half has no test (C6).
- (e) S:272 `re-approved` reporting is not delivered (OQ-49).
- (f) The root-skipped tests (C5).
- (g) The unbounded-pipe behaviour of a real Orca (A6).
- (h) The FR-009 marker-contract test is weak (matrix note).

**Not really proven:** NFR-014 (partial), NFR-008/AC-19 (split), NFR-012/AC-23 (gate), and the real-shape half of FR-002/005/006/007/009/013 until FU-1 and FU-3 run.

## Structural and tech-debt

- **Module boundaries:** cycle.py is 1369 lines (config, mountinfo parser, approvers, deadline, cycle, status and SLO in one module; fixed by NFR-014's module list). Two boundary leaks the walker cannot see: cli -> cycle.format_utc (cli.py:319) and cycle -> launch._ORCA_CLIS, a private name (cycle.py:1225-1230).
- **Duplication:**
  - OPERATION_ID_PATTERN x2.
  - The issue bound x3, plus 2 digit encodings.
  - The login regex x2 (cycle.py:468, github.py:134).
  - The UTC format string x3.
  - ENTRY_STATES x2 (pinned by literal in test_audit.py:473).
  - Exit constants in cli.py:34-38 vs REASON_TABLE (audit.stderr_fallback checks membership only, audit.py:393-401).
- **Dead code:** the A8 list.
- **Wall-clock reads:** audit.py:396 only, plus runner's monotonic. SystemClock is the one sanctioned reader.
- **Doc/code drift:** D:239 and D:242 (imports). D lacks cycle_complete, cycle_crashed and the once exit 1 (D:114). S has 52 names, the code 59, the runbook 59. The task file is stale (C7).
- **Risk register (blast radius):**
  - R1: real gh/Orca shapes differ from the fixtures. Every launch then stops loudly or reads wrongly (whole feature; gated by the live test).
  - R2: the A6 pipe hang makes all launches `unknown` (whole feature, fail-closed).
  - R3: A1 clock step, cap exceeded (bounded by human approvals).
  - R4: A5, lost operation_id (one issue).
  - R5: A10, one issue never launches.
  - R6: `reset --forfeit-guarantee` is the only path to a second launch (by design).
- **Untested invariants:**
  - launch bound == predicates bound
  - cycle._LOGIN == github._LOGIN_RE
  - a DISABLED re-check after the origin call
  - the day cap under a backward clock
  - an exception after the spawn (only launcher exceptions are tested, T/test_crash_injection.py:327)
  - `status` on a dangling DISABLED
  - the six root-skipped paths when run as root

## Recommendations

1. **T/test_launch.py:** add parity assertions that launch.MAX_ISSUE_NUMBER == predicates.MAX_ISSUE_NUMBER (and that PROMPT_PATTERN and record._DECIMAL_KEY accept exactly 1..MAX), and that cycle._LOGIN.pattern == github._LOGIN_RE.pattern. Verifier: `uv run pytest tests/issue_watch/test_launch.py tests/issue_watch/test_record.py -v`.
2. **docs/designs/issue-watcher.md:** amend the 5.3 rows for record (functions) and cli. List the 59-name table including cycle_complete and cycle_crashed. Add exit 1 to the `once` row (D:114). Verifier: T/test_module_boundaries.py plus a grep for the two names in the design. The owner must decide whether exit 1 is accepted (AC-17).
3. **IW/cli.py:319:** stop using cycle.format_utc. Use a public stamp helper, or amend D:242 to allow predicates for cli. Verifier: test_module_boundaries.py (add an attribute-access scan).
4. **IW/cycle.py around 1049-1052:** re-check d.store.disabled() just before mark_pending and raise _Stop("disabled_mid_cycle", stamp=True). Verifier: a new test in T/test_cycle.py using world.on("origin", ...) to create DISABLED, asserting no pending entry and zero launcher calls.
5. **IW/record.py:689-703:** count consumed times later than now as in-window (fail closed). This needs an owner decision because D:500 and D:505 pin the closed-at-now rule. Verifier: T/test_record.py day-cap tests plus a new "clock stepped back" case.
6. **IW/record.py:425-431:** use os.lstat in disabled_since and catch OSError. Verifier: a new T/test_cli.py status case with a dangling DISABLED symlink.
7. **IW/cycle.py:685-690:** after a spawn (launched_issue set or launcher called), commit the store in a finally block, and validate host in cli.build_deps. Verifier: a new T/test_crash_injection.py case with an exception raised from audit.decision_line after the launcher returned.
8. **IW/cycle.py:635-641 and T:** delete the dead re-approved branch, or implement it per the owner's choice on OQ-49 (spec-final.md:272). Verifier: a T/test_cycle.py case where a launched issue gets a newer approval event.
9. **Dead code:** delete or use IW/cycle.py:35, record.py:748 (plus its 3 test refs), cycle.py:1235 with cli.py:173, and runner.py:35. Verifier: `uv run ruff check` and the full tests/issue_watch run.
10. **Root skips:** in T/test_cli.py:967, 1259, 1627, 1653; test_record.py:739; and test_cycle.py:735, replace the root skipif with monkeypatched failures (os.open or os.replace raising PermissionError) so they run as root. Verifier: `uv run pytest tests/issue_watch -rs` as uid 0 in a container; expect 0 skipped.
11. **IW/cycle.py:307-324:** fstat the opened fd for owner and mode, and check the parent directory mode. Verifier: the T/test_cycle.py approvers table.
12. **cli.py:79,127,219 (callers of IW/audit.py:393-397):** pass ts=cycle.SystemClock().now(). Verifier: a grep for `datetime.now` in the package shows only SystemClock.
13. **IW/runner.py:91-101:** add a stub in T/test_runner.py that backgrounds a child holding stdout and assert the classification. Consider start_new_session=True with a process-group kill and a stdout cap. Verifier: that test plus the live Orca test (FU).
14. **PKG/TASK-RF-...md lines 847, 883, 199-975 ("57"), 907, 1050:** refresh the stale statements. Verifier: grep for "13 files", "57" and "Populated by Step 10.5".
15. **Owner decision:** track .dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md, or copy the cited rules into the design. Verifier: `git ls-files`.

Not verified: DF-50/DF-51 full text, D 598-602, real gh/Orca behaviour, the Python 3.10 run, and the unopened tests' bite claims. The same card went to team-lead via SendMessage.

| Status | Result |
|---|---|
| DONE | Card returned in the requested shape, 12 additional findings (A1-A12) plus the C1-C10 register |
| NEXT | Orchestrator persists the card and runs blind calibration; owner decisions on recommendations 2, 5 and 15 |
