### Deviation R-1: A launch can start after the 120 s cutoff.

- **Location:** `src/superclaude/cli/issue_watch/cycle.py:1060-1062`, `src/superclaude/cli/issue_watch/cycle.py:1048`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-007, C-014
- **Evidence:**
  - `src/superclaude/cli/issue_watch/cycle.py:1048-1049` - last check: if not self.deadline.launch_allowed(), raise _Skip budget_exhausted
  - `src/superclaude/cli/issue_watch/cycle.py:1060` - self._set(record.mark_pending(self.doc, c.n, ctx, self.now()))
  - `src/superclaude/cli/issue_watch/cycle.py:1061` - self._save() with the comment FR-010: durable before the launch call
  - `src/superclaude/cli/issue_watch/cycle.py:1062` - outcome = d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S), no cutoff check between 1061 and 1062
  - `src/superclaude/cli/issue_watch/cycle.py:410-412` - launch_allowed returns self.elapsed() <= LAUNCH_CUTOFF_S
  - `docs/designs/issue-watcher.md:647` - Orca launch not started when elapsed() > 120; the step ends with no entry and no reason other than a budget_exhausted decision line
  - `docs/designs/issue-watcher.md:892` - AC-19: no launch starts after 120 s
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:901` - Gate C: the fix of the deadline exit code let a launch start after the 120 s cut-off; fixed in cycle 2 (the git-call window only)
- **Classification:** regression (severity LOW, blocking: YES)
- **Classification rationale:** Design :647 "not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line"; AC-19 (design :892) "no launch starts after 120 s".
- **Debate outcome:** X-007 merged (confidence 0.85): variant-2 finding, LOW severity from variant-1 and variant-3, blocking flag from variant-2 and variant-3. V2 HIGH and calibrator MEDIUM rejected (see rejected_claims).
- **Default remediation:** src/superclaude/cli/issue_watch/cycle.py - Capture the document before mark_pending, re-check launch_allowed() after self._save(), and if the cutoff has passed restore and save the captured document and raise _Skip("budget_exhausted") (see late_launch_ruling). Verifier: New tests/issue_watch/test_cycle.py case whose clock passes 120 s inside store.save: asserts no launcher call, the document restored, and a budget_exhausted decision line.

### Deviation R-2: `once` can exit 1 (cycle_crashed), an exit code the design does not list for the verb.

- **Location:** `src/superclaude/cli/issue_watch/cli.py:35`, `src/superclaude/cli/issue_watch/cli.py:123-129`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-001, C-001
- **Evidence:**
  - `src/superclaude/cli/issue_watch/cli.py:35` - _EXIT_CRASH = 1 with the comment [PROPOSAL] C-3
  - `src/superclaude/cli/issue_watch/cli.py:123-129` - crash path calls audit.stderr_fallback(cycle_crashed, _EXIT_CRASH), then sys.exit(_EXIT_CRASH)
  - `docs/designs/issue-watcher.md:114` - once exit codes: 0, 2, 3, 4, 5, 6, 7, 75
  - `docs/designs/issue-watcher.md:890` - AC-17: each verb exit codes match section 4
- **Classification:** regression (severity LOW, blocking: no)
- **Classification rationale:** Design :114 `once` exits "0, 2, 3, 4, 5, 6, 7, 75"; AC-17 (design :890) "Each verb's exit codes match section 4". The [PROPOSAL] comment at cli.py:35 is not authority.
- **Debate outcome:** X-001 won by variant-2 and variant-3 (confidence 0.85); variant-1 Necessary rejected (A-002).
- **Default remediation:** docs/designs/issue-watcher.md (:114 and section 4.3); spec reason table - Add exit 1 (cycle_crashed) as an amended exit; behaviour stays. Verifier: tests/issue_watch/test_cli.py:630 (crash exit) unchanged and passing

### Deviation R-3: The reason table has 59 names (cycle_complete and cycle_crashed added), not the 57 the task and DF-41 fix, so audit.R...

- **Location:** `src/superclaude/cli/issue_watch/audit.py:55-57`, `src/superclaude/cli/issue_watch/audit.py:62-64`, `src/superclaude/cli/issue_watch/cycle.py:1134-1137`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-002, X-010, C-002, C-003
- **Evidence:**
  - `src/superclaude/cli/issue_watch/audit.py:55-57` - cycle_crashed mapped to (cycle, 1) with a [PROPOSAL] comment
  - `src/superclaude/cli/issue_watch/audit.py:62-64` - cycle_complete mapped to (cycle, 0) with a [PROPOSAL] comment
  - `src/superclaude/cli/issue_watch/cycle.py:1134-1137` - [PROPOSAL] comment and return cycle_complete
  - `tests/issue_watch/test_audit.py:214-220` - test_reasons_pin_59_names asserts 59 names
  - `docs/designs/issue-watcher-setup.md:344` - the audit log accepts only the 59 names
  - `docs/designs/issue-watcher.md:718` - audit.REASONS is a frozenset equal to the spec reason table
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:199` - Ensuring the table has exactly 57 entries (52 spec rows plus five proposals)
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:175` - DF-41: the 52 spec rows plus five named proposals; test_audit.py listed with 57 names
- **Classification:** regression (severity LOW, blocking: no)
- **Classification rationale:** Design :718 "`audit.REASONS` is a `frozenset` equal to the spec's reason table"; task :199 "exactly 57 entries"; DF-41 (DF register :175) names 57.
- **Debate outcome:** X-002 won by variant-2 and variant-3 (0.80), variant-1 MEDIUM rejected; X-010 won by variant-2 and variant-3 (0.80) and folded into this row.
- **Default remediation:** docs/designs/issue-watcher.md:718; task:199; DF register DF-41; spec reason table - Record 59 names, including cycle_complete and cycle_crashed. Verifier: tests/issue_watch/test_audit.py:215-219 (pins 59)

### Deviation R-4: record.py imports the function valid_operation_id from predicates, which neither the design import rule (types only) ...

- **Location:** `src/superclaude/cli/issue_watch/record.py:23-29`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-003, C-005
- **Evidence:**
  - `src/superclaude/cli/issue_watch/record.py:23-29` - imports ApprovalResult, format_utc, parse_utc, valid_issue_number, valid_operation_id from superclaude.cli.issue_watch.predicates
  - `src/superclaude/cli/issue_watch/record.py:183` - _opt(raw[operation_id], valid_operation_id) is the use site
  - `docs/designs/issue-watcher.md:239` - record may import predicates (types only)
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332` - allowed imports from predicates: parse_utc, format_utc, valid_issue_number
  - `tests/issue_watch/test_module_boundaries.py:20-21` - docstring says record imports three functions and one type (miscount, C-038)
  - `tests/issue_watch/test_module_boundaries.py:57-61` - record Rule allows the predicates sibling with no name limit
  - `src/superclaude/cli/issue_watch/launch.py:36` - OPERATION_ID_PATTERN local copy, the precedent for a local copy
- **Classification:** regression (severity LOW, blocking: no)
- **Classification rationale:** Design :239 `record` may import `predicates` "(types only, ...)"; task :332 lists only `parse_utc`, `format_utc`, `valid_issue_number`.
- **Debate outcome:** X-003 merged (0.85) and split: Authorized for the three functions and ApprovalResult (A-1), Regression LOW for valid_operation_id (this row). C-038 folded into this row.
- **Default remediation:** task:332 and design :239, or src/superclaude/cli/issue_watch/record.py; tests/issue_watch/test_module_boundaries.py:20-21 - Either amend task :332 and design :239 to name valid_operation_id, or give record.py a local copy as launch.py:36 does; fix the miscounted docstring at test_module_boundaries.py:20-21 (C-038). Verifier: tests/issue_watch/test_module_boundaries.py:57-61

### Deviation R-5: Five test sites use skipif or pytest.skip, which the task forbids;

- **Location:** `tests/issue_watch/test_cli.py:967`, `tests/issue_watch/test_cli.py:1070`, `tests/issue_watch/test_record.py:739`, `tests/issue_watch/test_cycle.py:735`, `tests/issue_watch/test_cycle.py:4694`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-006, C-013
- **Evidence:**
  - `tests/issue_watch/test_cli.py:967` - skipif when os.geteuid() == 0 (root reads any file)
  - `tests/issue_watch/test_cli.py:1070` - NOT_ROOT = pytest.mark.skipif when os.geteuid() == 0
  - `tests/issue_watch/test_record.py:739` - skipif when os.geteuid() == 0
  - `tests/issue_watch/test_cycle.py:735` - skipif when os.geteuid() == 0
  - `tests/issue_watch/test_cycle.py:4694` - pytest.skip: /proc/self/mountinfo exists on Linux only
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:188` - No test may use pytest.skip, skipif or xfail, because gates G-1 and G-3 require zero skipped tests
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:908` - pytest.skip/skipif still appears in five test sites; nothing was skipped in any recorded run (graded minor)
- **Classification:** regression (severity MEDIUM, blocking: no)
- **Classification rationale:** Task :188 "No test may use `pytest.skip`, `skipif` or `xfail`, because gates G-1 and G-3 require zero skipped tests." (graded minor at task :908)
- **Debate outcome:** X-006 merged (0.80): variant-2 class with the non-blocking ruling of variant-1 and variant-3.
- **Default remediation:** tests/issue_watch/test_cli.py, tests/issue_watch/test_record.py, tests/issue_watch/test_cycle.py - Replace the root-only skipif marks with checks that hold for root and non-root, and give test_cycle.py:4694 a stubbed mountinfo text instead of reading /proc/self/mountinfo. Verifier: uv run pytest tests/issue_watch -rs reports 0 skipped

### Deviation R-6: The operation-unknown marker is searched only in stderr already cut to 500 bytes, so a marker after byte 500 is misse...

- **Location:** `src/superclaude/cli/issue_watch/runner.py:57-64`, `src/superclaude/cli/issue_watch/runner.py:126`, `src/superclaude/cli/issue_watch/launch.py:322`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-026
- **Evidence:**
  - `src/superclaude/cli/issue_watch/runner.py:15` - STDERR_CAP_BYTES = 500
  - `src/superclaude/cli/issue_watch/runner.py:57-64` - _cap_stderr cuts text to STDERR_CAP_BYTES UTF-8 bytes
  - `src/superclaude/cli/issue_watch/runner.py:126` - stderr=_cap_stderr(proc.stderr) in the returned CommandResult
  - `src/superclaude/cli/issue_watch/launch.py:322` - OP_UNKNOWN_TEXT checked in result.stdout or result.stderr (the capped text)
  - `docs/designs/issue-watcher.md:634` - agent_session_operation_unknown anywhere in stdout or stderr maps to unknown
- **Classification:** regression (severity LOW, blocking: no)
- **Classification rationale:** Design :634 "`agent_session_operation_unknown` anywhere in stdout or stderr" maps to `unknown`.
- **Debate outcome:** C-026 won by variant-2 and variant-3 (0.70): Regression.
- **Default remediation:** src/superclaude/cli/issue_watch/runner.py, src/superclaude/cli/issue_watch/launch.py - Detect the operation-unknown marker on the full stderr before the 500-byte cap is applied (runner.py:15). Verifier: New launch test with the marker after byte 500, expecting unknown

### Deviation R-7: status drops an unknown entry with an operation id from the retry list when its retry argv cannot be built;

- **Location:** `src/superclaude/cli/issue_watch/cycle.py:1271`, `src/superclaude/cli/issue_watch/cycle.py:1279-1280`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-036
- **Evidence:**
  - `src/superclaude/cli/issue_watch/cycle.py:1271` - retry only when entry.state == unknown and entry.operation_id and entry.launch_cwd
  - `src/superclaude/cli/issue_watch/cycle.py:1279-1280` - except ValueError: continue (the entry is dropped)
  - `src/superclaude/cli/issue_watch/record.py:182-184` - operation_id validated with valid_operation_id; launch_cwd must be absolute when present
  - `src/superclaude/cli/issue_watch/record.py:548` - mark_pending requires an absolute launch_cwd
  - `docs/designs/issue-watcher.md:739` - retry lists unknown entries with an operation_id
- **Classification:** regression (severity LOW (effectively unreachable), blocking: no)
- **Classification rationale:** Design :739 `retry` lists "`unknown` entries with an `operation_id`".
- **Debate outcome:** C-036 won by variant-2 and variant-3 (0.70): Regression, effectively unreachable.
- **Default remediation:** src/superclaude/cli/issue_watch/cycle.py - When an unknown entry with an id has no usable retry argv, print it with a warning instead of dropping it. Verifier: New tests/issue_watch/test_cycle.py case

### Deviation D-1: The setup guide and design 10.2 misstate two verb facts: setup :53 leaves reset out of the Linux-only verbs although ...

- **Location:** `docs/designs/issue-watcher-setup.md:53`, `docs/designs/issue-watcher-setup.md:432`, `docs/designs/issue-watcher.md:726`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-034
- **Evidence:**
  - `docs/designs/issue-watcher-setup.md:53` - Linux-only list names once, check-config and init-state (no reset)
  - `docs/designs/issue-watcher-setup.md:432` - status exits 0, 1, 6
  - `docs/designs/issue-watcher.md:726` - status exits 0, 1, 6 (no 2)
  - `docs/designs/issue-watcher.md:115` - status exits 0, 1, 2, 6
  - `src/superclaude/cli/issue_watch/cli.py:169` - status calls _load_config(config_path, platform=False); a config error exits 2 through cli.py:84-91 and cli.py:77-81
  - `src/superclaude/cli/issue_watch/cli.py:314` - reset calls _load_config(config_path), which runs check_platform (cli.py:84-91, platform defaults to true)
- **Classification:** drift (severity LOW, blocking: no)
- **Classification rationale:** Rationale: the docs disagree with design :115 (status 0, 1, 2, 6), cli.py:169 (exit 2) and cli.py:314 (reset runs the platform check).
- **Debate outcome:** C-034 won by all three variants (0.85): Drift.
- **Default remediation:** docs/designs/issue-watcher-setup.md:53, :432; docs/designs/issue-watcher.md:726 - Add reset at setup :53; add exit 2 at setup :432 and design :726. Verifier: Re-read against cli.py:169 and cli.py:314

### Deviation D-2: cli.py stamps the reset line with cycle.format_utc, a predicates function re-exported through cycle;

- **Location:** `src/superclaude/cli/issue_watch/cli.py:319`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-006
- **Evidence:**
  - `src/superclaude/cli/issue_watch/cli.py:319` - ts: cycle.format_utc(now)
  - `docs/designs/issue-watcher.md:242` - cli may import cycle, record, audit, launch, runner
- **Classification:** drift (severity LOW, blocking: no)
- **Classification rationale:** Rationale: cycle.format_utc is re-exported from predicates; design :242 does not list predicates for cli.
- **Debate outcome:** C-006 won by variant-1 and variant-3: Drift.
- **Default remediation:** docs/designs/issue-watcher.md:242, or src/superclaude/cli/issue_watch/cycle.py - Amend design :242 to note the transitive use, or give cycle a public stamp helper. Verifier: tests/issue_watch/test_module_boundaries.py

### Deviation D-3: cycle.py keeps its own copies of the login pattern and the UTC timestamp format although design :241 lets it import g...

- **Location:** `src/superclaude/cli/issue_watch/cycle.py:468`, `src/superclaude/cli/issue_watch/cycle.py:76`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-008, C-009
- **Evidence:**
  - `src/superclaude/cli/issue_watch/cycle.py:468` - _LOGIN = re.compile with the pattern [A-Za-z0-9][A-Za-z0-9-]{0,38}
  - `src/superclaude/cli/issue_watch/github.py:134` - _LOGIN_RE = re.compile with the same pattern
  - `src/superclaude/cli/issue_watch/cycle.py:76` - _UTC_TS_FORMAT = %Y-%m-%dT%H:%M:%SZ
  - `docs/designs/issue-watcher.md:241` - cycle may import runner, github, predicates, record, launch, audit
- **Classification:** drift (severity LOW, blocking: no)
- **Classification rationale:** Rationale: they copy github.py:134 `_LOGIN_RE` and the predicates format; design :241 allows the imports.
- **Debate outcome:** C-008 won by variant-1 and variant-3; C-009 won by variant-3: Drift for the cycle copy.
- **Default remediation:** src/superclaude/cli/issue_watch/cycle.py - Use the github and predicates values. Verifier: The existing login and timestamp tests in tests/issue_watch/test_cycle.py

### Deviation D-4: audit.stderr_fallback reads the wall clock when no ts is passed, against the rule that audit never reads the clock;

- **Location:** `src/superclaude/cli/issue_watch/audit.py:395-397`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-012
- **Evidence:**
  - `src/superclaude/cli/issue_watch/audit.py:395-397` - if ts is None: now = datetime.datetime.now(datetime.timezone.utc); ts = now.strftime(_UTC_TS_FORMAT)
  - `src/superclaude/cli/issue_watch/audit.py:390-391` - docstring: ts and host default to the current UTC time and socket.gethostname() (a stamp, not a decision)
- **Classification:** drift (severity LOW, blocking: no)
- **Classification rationale:** Rationale: wall clock; the docstring says "a stamp, not a decision".
- **Debate outcome:** C-012 won by variant-1 and variant-3; split into D-4 (Drift) and A-2 (Authorized).
- **Default remediation:** src/superclaude/cli/issue_watch/audit.py and its callers - Pass ts where the caller holds the cycle clock. Verifier: The test_audit.py fallback cases

### Deviation N-1: Leaf modules keep local copies of shared constants and helpers (issue bound, operation-id pattern, directory fsync, t...

- **Location:** `src/superclaude/cli/issue_watch/audit.py:203`, `src/superclaude/cli/issue_watch/launch.py:30`, `src/superclaude/cli/issue_watch/launch.py:36`, `src/superclaude/cli/issue_watch/record.py:310-315`, `src/superclaude/cli/issue_watch/audit.py:110-115`, `src/superclaude/cli/issue_watch/audit.py:200`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-004, C-007, C-010, C-011, C-009
- **Evidence:**
  - `src/superclaude/cli/issue_watch/audit.py:203` - _MAX_ISSUE = 999_999_999, the same bound as predicates.MAX_ISSUE_NUMBER
  - `src/superclaude/cli/issue_watch/launch.py:30` - MAX_ISSUE_NUMBER = 999_999_999
  - `src/superclaude/cli/issue_watch/launch.py:36` - OPERATION_ID_PATTERN = re.compile(^[A-Za-z0-9._:-]{1,128}$)
  - `src/superclaude/cli/issue_watch/record.py:310-315` - _fsync_dir: os.open O_RDONLY | O_DIRECTORY, os.fsync, os.close in finally
  - `src/superclaude/cli/issue_watch/audit.py:110-115` - _fsync_dir: the same four-line helper (CORRECTED from plan audit.py:204-206)
  - `src/superclaude/cli/issue_watch/audit.py:200` - _UTC_TS_FORMAT = %Y-%m-%dT%H:%M:%SZ (the C-009 audit copy)
  - `docs/designs/issue-watcher.md:237` - audit imports nothing from the package
  - `docs/designs/issue-watcher.md:240` - launch imports runner and _ORCA_CLIS only
- **Classification:** necessary (severity LOW, blocking: no)
- **Classification rationale:** Design :237 and :240 force the copies.
- **Debate outcome:** X-004 won by all three variants (0.90): Necessary. C-010 from variant-1, C-011 and C-009 from variant-3.
- **Default remediation:** none (document only).

### Deviation N-2: The day-cap test bounds the second day at 6 launches, following the module constant.

- **Location:** `tests/issue_watch/test_cycle.py:4150-4154`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-030
- **Evidence:**
  - `tests/issue_watch/test_cycle.py:4150-4154` - comment on the 6-per-24h cap and second_day = min(count - capped, 6)
  - `src/superclaude/cli/issue_watch/cycle.py:36` - DAY_CAP = 6
- **Classification:** necessary (severity LOW, blocking: no)
- **Classification rationale:** Rationale: cycle.py:36 DAY_CAP = 6.
- **Debate outcome:** C-030 won by variant-2: Necessary.
- **Default remediation:** none (document only).

### Deviation N-3: status picks the retry Orca name by reading launch._ORCA_CLIS instead of importing install_user_setup directly.

- **Location:** `src/superclaude/cli/issue_watch/cycle.py:1225-1230`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-033
- **Evidence:**
  - `src/superclaude/cli/issue_watch/cycle.py:1225-1230` - _retry_orca returns the first launch._ORCA_CLIS name which resolves, else the first name
  - `src/superclaude/cli/issue_watch/launch.py:22` - from superclaude.cli.install_user_setup import _ORCA_CLIS
  - `docs/designs/issue-watcher.md:240` - launch imports runner and _ORCA_CLIS only
- **Classification:** necessary (severity LOW, blocking: no)
- **Classification rationale:** Rationale: reads launch._ORCA_CLIS (design :240).
- **Debate outcome:** C-033 won by variant-3: Necessary.
- **Default remediation:** none (document only).

### Deviation A-1: record.py imports parse_utc, format_utc, valid_issue_number and the type ApprovalResult from predicates.

- **Location:** `src/superclaude/cli/issue_watch/record.py:23-29`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-003, C-005
- **Evidence:**
  - `src/superclaude/cli/issue_watch/record.py:23-29` - imports ApprovalResult, format_utc, parse_utc, valid_issue_number (and valid_operation_id, see R-4)
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332` - allowed imports from predicates: parse_utc, format_utc, valid_issue_number
  - `docs/designs/issue-watcher.md:239` - record may import predicates (types only)
- **Classification:** authorized (severity n/a, blocking: no)
- **Classification rationale:** Task :332; design :239.
- **Debate outcome:** X-003 merged (0.85) and split; this is the Authorized part.
- **Default remediation:** none (document only).

### Deviation A-2: runner.py reads time.monotonic() to measure duration_s around the child.

- **Location:** `src/superclaude/cli/issue_watch/runner.py:89`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** X-005, C-012
- **Evidence:**
  - `src/superclaude/cli/issue_watch/runner.py:89` - start = time.monotonic()
  - `src/superclaude/cli/issue_watch/runner.py:35` - duration_s: float
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:193` - measures duration_s with time.monotonic() around the child only; it is never used for a decision
- **Classification:** authorized (severity n/a, blocking: no)
- **Classification rationale:** Task :193.
- **Debate outcome:** X-005 won by all three variants (0.85): Authorized.
- **Default remediation:** none (document only).

### Deviation A-3: The reason table carries the five proposed reasons the task names (marker_unreadable, edits_unreadable, operator_rese...

- **Location:** ~~dropped~~ (C-0113)
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-004
- **Evidence:**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:199` - plus the two proposals marker_unreadable and edits_unreadable; dry_run_shadow_reset (DF-22); reset_refused (DF-57); operator_reset (DF-03)
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:175` - DF-41 names the same five proposals
- **Classification:** authorized (severity n/a, blocking: no)
- **Classification rationale:** Task :199 five proposed reasons.
- **Debate outcome:** C-004 won by variant-1: Authorized.
- **Default remediation:** none (document only).

### Deviation A-4: The full suite depends on gh and runs in CI only.

- **Location:** `gh dependency`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-031
- **Evidence:**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:28` - DF-05: CI-only full suite
- **Classification:** authorized (severity n/a, blocking: no)
- **Classification rationale:** DF-05 (DF register :28).
- **Debate outcome:** C-031 won by variant-2: Authorized.
- **Default remediation:** none (document only).

### Deviation A-5: The issue-watch group is registered on the main CLI after line 561.

- **Location:** `src/superclaude/cli/main.py:563-565`
- **Mapped tasklist item:** see Per-Task Verdicts
- **Source ids:** C-032
- **Evidence:**
  - `src/superclaude/cli/main.py:563` - from superclaude.cli.issue_watch.cli import issue_watch_group
  - `src/superclaude/cli/main.py:565` - main.add_command(issue_watch_group, name=issue-watch)
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:156` - DF-29 row: main.py registration after line 561 (CORRECTED from plan DF register :208; :208 is the P7 phase row that references DF-29)
- **Classification:** authorized (severity n/a, blocking: no)
- **Classification rationale:** DF-29 (DF register :156; the plan cites :208, the P7 phase row that references DF-29).
- **Debate outcome:** C-032 won by variant-3: Authorized. Variant-3 path src/superclaude/main.py corrected to src/superclaude/cli/main.py.
- **Default remediation:** none (document only).

