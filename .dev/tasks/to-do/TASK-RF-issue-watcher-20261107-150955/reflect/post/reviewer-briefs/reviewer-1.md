# Reviewer brief 1 (persona lens: analyzer / correctness of production logic)

## T1 card excerpt

(Verbatim slice of the Tier-1 card, "Root-cause and deviation register". It is the single-agent first pass: treat every row as an unverified claim, confirm or refute it from the real source.)

#### Root-cause and deviation register (card section)

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

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T04:40:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher

### src/superclaude/cli/issue_watch/cycle.py:663-760

```python
    def run(self) -> CycleResult:
        deps = self.deps
        try:
            if not deps.config.enabled and not self.dry_run:
                raise _Stop("not_enabled")
            try:
                self.approvers = validate_setup(deps.config)
            except ConfigError as exc:
                raise _Stop(exc.reason) from None
        except _Stop as stop:
            self._stopped(stop.reason)
            return self._conclude(locked=False)
        try:
            with deps.store.lock():
                self._locked_body()
                return self._conclude(locked=True)
        except LockHeld:
            self._stopped("lock_held")
        except LockError as exc:
            self._stopped(exc.reason)
        return self._conclude(locked=False)

    def _locked_body(self) -> None:
        try:
            self._steps()
        except _Stop as stop:
            self._stopped(stop.reason)
        self._commit()

    def _steps(self) -> None:
        if self.deps.store.disabled():
            raise _Stop("disabled")
        self._load()
        self._login_step()
        timeout = self.deadline.timeout_for(GIT_TIMEOUT_S)
        if timeout is None:
            # Gate C fix C-1: no time left is not a mismatch. The origin check is
            # a shared call, so design 8.5 gives exit 3 gh_timeout (no git call).
            raise _Stop("gh_timeout")
        if not self._origin_ok(timeout):
            raise _Stop("origin_mismatch")
        self._sweep()
        issues = self._discover()
        by_number = {i.number: i for i in issues}
        if self.dry_run:
            self.shadow, self.shadow_reset = record.load_dry_run(
                self.deps.store.state_dir
            )
            if self.shadow_reset:
                self._warn("dry_run_shadow_reset")
            considered = self.shadow.considered
        else:
            assert self.doc is not None
            considered = self.doc.considered
        order = predicates.eligibility_order(issues, considered)[:MAX_CANDIDATES]
        self._candidates(order, by_number)

    def _load(self) -> None:
        store = self.deps.store
        try:
            doc = store.load()
        except StoreError as exc:
            raise _Stop(exc.reason) from None
        self.doc = doc
        if not self.dry_run and getattr(store, "migrated", False):
            self._save()  # DF-17: only a real cycle saves the migrated store
        wait = doc.next_permitted_at
        if wait is not None and self.now() < wait:
            raise _Stop("rate_limited")

    def _login_step(self) -> None:
        cfg = self.deps.config
        capture = _LastResult(self.deps.runner)
        read = github.user(capture, self._tf_shared)
        if read.reason is not None:
            if read.kind == "rate_limited" and capture.last is not None:
                assert self.doc is not None
                when, reason = github.rate_limit_wait(capture.last, self.now())
                self._set(record.set_next_permitted(self.doc, when))
                raise _Stop(reason)
            raise _Stop(read.reason)
        who = read.value
        if _LOGIN.fullmatch(who.login) is None:  # type: ignore[union-attr]
            raise _Stop("login_invalid")
        self.login = who.login  # type: ignore[union-attr]
        self.account_id = who.account_id  # type: ignore[union-attr]
        if cfg.owner_account_id is not None and cfg.owner_account_id != who.account_id:  # type: ignore[union-attr]
            raise _Stop("account_id_mismatch")
        server = who.server_date  # type: ignore[union-attr]
        if server is not None:
            skew = abs((server - self.now()).total_seconds())
            self.clock_skew_s = int(round(skew))  # S 100: on the cycle line every cycle
            if skew > SKEW_WARN_S:  # only the warning line has a threshold
                self._warn("clock_skew", clock_skew_s=self.clock_skew_s)

    def _sweep(self) -> None:
        assert self.doc is not None
        doc, changed = record.sweep(self.doc, self.now())
```

### src/superclaude/cli/issue_watch/cycle.py:896-1075

```python
    def _examine(self, c: _Cand) -> tuple[str, str | None]:
        """Steps 10 and 11 for one candidate: ``(reason, entry state or None)``."""
        d, cfg = self.deps, self.deps.config
        e = c.entry
        state = e.state if e is not None else None
        if state in ("claimed", "pending"):
            raise _Skip("already_dispatched")
        if e is not None and (
            state in ("launched", "unknown")
            or (state == "abandoned" and e.pending_at is not None)
        ):
            markers = self._val(
                github.marker_comments(d.runner, self.budget, c.n, self._tf)
            )
            if self._hit(markers, e.pending_at, None):
                return self._claim(c, None)  # T-10
            raise _Skip("already_dispatched")
        if state == "abandoned":  # an attempts_exhausted tombstone
            return self._reclaim(c, "already_dispatched")
        if e is not None and not record.backoff_elapsed(e, self.now()):
            return self._reclaim(c, "in_backoff")  # OQ-36
        if self._day_cap_reached():
            raise _Skip("day_cap")
        owned, why = predicates.is_intended_owner(c.issue.assignees, self.login or "")
        if not owned:
            raise _Skip(why or "assigned_other")
        markers = self._val(
            github.marker_comments(d.runner, self.budget, c.n, self._tf)
        )
        events = self._val(github.events(d.runner, self.budget, c.n, self._tf))
        approval = self._approve(c, events)
        if self._hit(markers, None, approval.approved_at):
            return self._claim(c, approval)  # T-11, T-12
        edits = self._val(github.edits(d.runner, self.budget, c.n, self._tf))
        why = predicates.unchanged_since(
            approval.approved_at,  # type: ignore[arg-type]
            edits,  # type: ignore[arg-type]
            events,  # type: ignore[arg-type]
            own_login=self.login or "",
        )
        if why is not None:
            raise _Skip(why)
        items = self._val(github.project_items(d.runner, self.budget, c.n, self._tf))
        why = predicates.project_check(items, cfg.project_id)  # type: ignore[arg-type]
        if why is not None:
            raise _Skip(why)
        return self._launch(c, approval)

    # -- step 12: the launch steps ---------------------------------------------

    def _rv(self, read: github.Read) -> object:
        """A re-read result: the value, or the skip, the stop or the transient."""
        if read.reason is None:
            return read.value
        if read.kind == "rate_limited":
            raise self._rate_stop()
        if read.kind == "scope_missing":
            raise _Stop("project_read_failed")
        if read.kind == "budget_exhausted":
            raise _Skip("budget_exhausted")
        if read.kind in ("timeout", "transient"):
            raise _Transient
        raise _Skip("revalidation_failed")

    def _revalidate(self, c: _Cand) -> None:
        """FR-011: G7, G3' and G6' with the 3 reserved calls."""
        d, cfg = self.deps, self.deps.config
        snap: predicates.IssueSnapshot = self._rv(  # type: ignore[assignment]
            github.reread(d.runner, self.budget, c.n, self._tf)
        )
        if (
            snap.state.lower() != "open"
            or cfg.trigger_label not in snap.labels
            or cfg.approval_label not in snap.labels
        ):
            raise _Skip("revalidation_failed")
        owned, why = predicates.is_intended_owner(snap.assignees, self.login or "")
        if not owned:
            raise _Skip(why or "assigned_other")
        assert self.doc is not None and c.approval is not None
        events = self._rv(
            github.events(d.runner, self.budget, c.n, self._tf, reserved=True)
        )
        again = predicates.approval_of(
            events,  # type: ignore[arg-type]
            labels_now=snap.labels,
            trigger_label=cfg.trigger_label,
            approval_label=cfg.approval_label,
            approvers=self.approvers,
            store_created_at=self.doc.created_at,
        )
        # A voided approval, or a newer approval event (edits are not re-read), fails.
        if (
            not again.approved
            or again.approval_event_id != c.approval.approval_event_id
        ):
            raise _Skip("revalidation_failed")
        items = self._rv(
            github.project_items(d.runner, self.budget, c.n, self._tf, reserved=True)
        )
        if predicates.project_check(items, cfg.project_id) is not None:  # type: ignore[arg-type]
            raise _Skip("revalidation_failed")

    def _fail(self, c: _Cand, reason: str) -> tuple[str, str]:
        assert self.doc is not None
        self._set(record.fail(self.doc, c.n, reason, self.now()))
        self._cond(reason)  # exit 7, also when the third failure abandons it
        entry = self.doc.entries[c.n]
        shown = entry.last_reason if entry.state == "abandoned" else reason
        return shown or reason, entry.state

    def _launch(self, c: _Cand, approval: ApprovalResult) -> tuple[str, str | None]:
        d, cfg = self.deps, self.deps.config
        c.launching = True
        if self.dry_run:  # no probe, no Orca call, nothing written (FR-019, OQ-39)
            assert self.shadow is not None
            self.would_launch = c.n
            self.shadow = replace(
                self.shadow, shadow_launches=(*self.shadow.shadow_launches, self.now())
            )
            return "launched", None
        timeout = self.deadline.timeout_for(PROBE_TIMEOUT_S)
        if timeout is None:
            raise _Skip("budget_exhausted")
        orca = launch.find_orca(d.runner, which=d.which, timeout=timeout)
        if orca is None:
            raise _Stop("orca_not_found", stamp=True)
        try:
            prompt = launch.build_claim_prompt(c.n)
        except ValueError:
            return self._fail(c, "prompt_invalid")
        try:
            self._revalidate(c)
        except _Transient:
            return self._fail(c, "revalidation_transient")
        if self._day_cap_reached():
            raise _Skip("day_cap")
        if d.store.disabled():
            raise _Stop("disabled_mid_cycle", stamp=True)
        # Gate C fix C-1 (design 647-649): when the 120 s cut-off has passed or
        # fewer than 5 s are left, no git call starts and the step ends with no
        # entry and a budget_exhausted decision line. origin_mismatch (exit 2)
        # is only for a git call that ran and failed.
        if not self.deadline.launch_allowed():
            raise _Skip("budget_exhausted")
        origin_timeout = self.deadline.timeout_for(GIT_TIMEOUT_S)
        if origin_timeout is None:
            raise _Skip("budget_exhausted")
        if not self._origin_ok(origin_timeout):
            raise _Stop("origin_mismatch", stamp=True)
        # Gate C cycle 2 (N-1): the git call may itself have crossed the cut-off,
        # so the launch must not start after it (design 647).
        if not self.deadline.launch_allowed():
            raise _Skip("budget_exhausted")
        assert self.doc is not None and self.login is not None
        assert self.account_id is not None
        ctx = record.PendingContext(
            approver_id=approval.approver_id,  # type: ignore[arg-type]
            approval_event_id=approval.approval_event_id,  # type: ignore[arg-type]
            approved_at=approval.approved_at,  # type: ignore[arg-type]
            launch_cwd=str(cfg.worktree),
            launch_login=self.login,
            launch_account_id=self.account_id,
        )
        self._set(record.mark_pending(self.doc, c.n, ctx, self.now()))
        self._save()  # FR-010: durable before the launch call
        outcome = d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)
        now = self.now()
        if outcome.kind == "launched":
            op = outcome.operation_id or ""
            self._set(record.mark_launched(self.doc, c.n, op, now))
            self.launched_issue = c.n
            return "launched", "launched"
        if outcome.kind == "unknown":
            self._set(record.mark_unknown(self.doc, c.n, outcome.operation_id, now))
            self._cond("launch_unknown")
            return "launch_unknown", "unknown"
        self._set(record.mark_spawn_error(self.doc, c.n, now))
        self._cond("spawn_error")
        return "spawn_error", "abandoned"
```

### src/superclaude/cli/issue_watch/cycle.py:1079-1174

```python
    def _commit(self) -> None:
        """Step 13 and 14: the one final write (the store, or the dry-run shadow)."""
        if self.stop_reason == "state_dir_unwritable":
            return
        try:
            if self.dry_run:
                self._commit_shadow()
            else:
                self._commit_store()
        except OSError:
            self._stopped("state_dir_unwritable")

    def _commit_store(self) -> None:
        doc = self.doc
        if doc is None:
            return
        now = self.now()
        changed = self.dirty
        if self.examined and self.discovered is not None:
            numbers = [i.number for i in self.discovered]
            doc = record.set_considered(doc, self.examined, numbers, now)
            changed = True
        if self.stop_reason is None and self._exit() == 0:
            doc = record.set_last_completed(doc, now)  # step 14
            changed = True
        if changed:
            self.doc = record.prune_consumed_log(doc, now)
            self.deps.store.save(self.doc)
            self.dirty = False

    def _commit_shadow(self) -> None:
        shadow = self.shadow
        if shadow is None or self.discovered is None:
            return
        launched = self.would_launch is not None
        if not (self.examined or launched or self.shadow_reset):
            return
        now = self.now()
        keep = {i.number for i in self.discovered}
        considered = {n: t for n, t in shadow.considered.items() if n in keep}
        considered.update((n, now) for n in self.examined if n in keep)
        cutoff = now - record.DAY_CAP_WINDOW
        launches = tuple(t for t in shadow.shadow_launches if t > cutoff)
        record.save_dry_run(
            self.deps.store.state_dir,
            record.DryRunDoc(considered=considered, shadow_launches=launches),
        )

    def _cycle_reason(self, exit_code: int) -> str:
        if exit_code != 0:
            for reason, code in self.conds:
                if code == exit_code:
                    return reason
        if self.stop_reason is not None:
            return self.stop_reason
        # [PROPOSAL] (Gate C fix C-2, executor decision): a cycle that ran to its
        # end names the cycle-kind reason cycle_complete (exit 0). A skip or entry
        # reason belongs to a decision line, never to this cycle line (DF-41).
        return "cycle_complete"

    def _conclude(self, locked: bool) -> CycleResult:
        """Step 15: decision lines, then the cycle line."""
        exit_code = self._exit()
        reason = self._cycle_reason(exit_code)
        cycle = audit.cycle_line(
            ts=self._ts(),
            host=self.deps.host,
            login=self.login,
            cycle_id=self.cycle_id,
            dry_run=self.dry_run,
            exit_code=exit_code,
            reason=reason,
            gh_calls=self.budget.total,
            duration_ms=int(self.deadline.elapsed() * 1000),
            discovery_count=self.discovery_count,
            clock_skew_s=self.clock_skew_s,
        )
        lines = (*self.lines, cycle)
        try:
            if self.stop_reason == "state_dir_unwritable":
                raise OSError("state_dir_unwritable")  # stderr only (FR-020)
            if locked:
                self.deps.audit.rotate_if_needed()
            for ln in lines:
                self.deps.audit.append(ln)
        except OSError:
            audit.stderr_fallback(reason, exit_code, ts=self._ts(), host=self.deps.host)
        return CycleResult(
            exit_code=exit_code,
            reason=reason,
            cycle_id=self.cycle_id,
            launched_issue=self.launched_issue,
            would_launch=self.would_launch,
            probe="skipped" if self.would_launch is not None else None,
            lines=lines,
        )
```

### src/superclaude/cli/issue_watch/record.py:370-419

```python
    def save(self, doc: StoreDoc) -> None:
        """Write ``doc`` atomically, force mode 0600, then fsync ``state_dir``."""
        from superclaude.cli.swarm.atomic import write_prepared_bytes  # C18

        text = json.dumps(_to_raw(doc), sort_keys=True, indent=2, ensure_ascii=True)
        path = self.state_dir / STORE_FILE
        write_prepared_bytes(path, text.encode() + b"\n")
        os.chmod(path, 0o600)
        _fsync_dir(self.state_dir)

    @contextmanager
    def lock(self) -> Iterator[None]:
        """Hold an exclusive ``flock`` on ``state_dir/lock`` (design section 7.6).

        Raises ``LockError("lock_missing")``, ``LockError("lock_invalid")`` or
        ``LockHeld``. The lock is released and its descriptor closed in a
        ``finally``, so a ``SystemExit`` passing through the ``with`` leaves the
        lock free for the next run (DF-15).
        """
        import fcntl  # not at module level: importing the package must work off Linux

        path = self.state_dir / LOCK_FILE
        try:
            fd = os.open(path, os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC)
        except FileNotFoundError:
            raise LockError("lock_missing") from None
        except OSError:  # a directory, a symlink (ELOOP), no permission, ...
            raise LockError("lock_invalid") from None
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid():
                raise LockError("lock_invalid")
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise LockHeld() from None
            try:
                try:
                    ps = os.stat(path, follow_symlinks=False)
                except FileNotFoundError:
                    raise LockHeld() from None
                if (ps.st_dev, ps.st_ino) != (st.st_dev, st.st_ino):
                    raise LockHeld()
                if os.fstat(fd).st_nlink == 0:
                    raise LockHeld()
                yield
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
```

### src/superclaude/cli/issue_watch/record.py:503-651

```python
def fail(doc: StoreDoc, n: int, reason: str, now: datetime) -> StoreDoc:
    """T-1 and T-3 (plus DF-43): record a pre-pending failure of issue ``n``.

    Allowed from no entry and from ``failed``; ``attempts`` grows by one and at
    ``MAX_ATTEMPTS`` the entry becomes ``abandoned`` ``attempts_exhausted``.
    ``reason`` must be ``prompt_invalid`` or ``revalidation_transient``.
    """
    state = _state_of(doc, n)
    if reason not in _FAIL_REASONS or state not in (None, "failed"):
        raise _refuse(n, state, reason)
    entry = doc.entries.get(n) or _new_entry(n, "failed", now)
    attempts = entry.attempts + 1
    exhausted = attempts >= MAX_ATTEMPTS
    return _with_entry(
        doc,
        replace(
            entry,
            state="abandoned" if exhausted else "failed",
            attempts=attempts,
            updated_at=now,
            last_reason="attempts_exhausted" if exhausted else reason,
        ),
    )


def backoff_elapsed(entry: Entry, now: datetime) -> bool:
    """T-2: True when a ``failed`` entry may be examined again.

    Elapsed iff ``now >= updated_at + BACKOFF`` and ``attempts < MAX_ATTEMPTS``.
    """
    if entry.state != "failed":
        raise _refuse(entry.issue, entry.state, "backoff_elapsed")
    return entry.attempts < MAX_ATTEMPTS and now >= entry.updated_at + BACKOFF


def mark_pending(doc: StoreDoc, n: int, ctx: PendingContext, now: datetime) -> StoreDoc:
    """T-4: write ``pending`` for issue ``n`` (from no entry or ``failed``).

    Sets ``launches`` 1, ``consumed_at`` and ``pending_at`` to ``now`` and the
    six ``PendingContext`` fields; ``attempts`` and ``created_at`` are kept.
    """
    state = _state_of(doc, n)
    if state not in (None, "failed"):
        raise _refuse(n, state, "pending")
    _check_approval(ctx.approver_id, ctx.approval_event_id, ctx.approved_at)
    if not isinstance(ctx.launch_cwd, str) or not os.path.isabs(ctx.launch_cwd):
        raise ValueError("launch_cwd must be an absolute path")
    if not isinstance(ctx.launch_login, str) or not ctx.launch_login:
        raise ValueError("launch_login must be a non-empty string")
    if not _positive_id(ctx.launch_account_id):
        raise ValueError("launch_account_id must be a positive integer")
    entry = doc.entries.get(n) or _new_entry(n, "pending", now)
    return _with_entry(
        doc,
        replace(
            entry,
            state="pending",
            launches=1,
            consumed_at=now,
            pending_at=now,
            updated_at=now,
            # No reason in the closed table names a pending write.
            last_reason=None,
            **asdict(ctx),
        ),
    )


def _pending_to(
    doc: StoreDoc, n: int, trigger: str, now: datetime, **fields: object
) -> StoreDoc:
    entry = doc.entries.get(n)
    if entry is None or entry.state != "pending":
        raise _refuse(n, _state_of(doc, n), trigger)
    return _with_entry(doc, replace(entry, updated_at=now, **fields))


def mark_launched(doc: StoreDoc, n: int, operation_id: str, now: datetime) -> StoreDoc:
    """T-5: ``pending`` to ``launched`` with a safe ``operation_id``.

    The id must match ``OPERATION_ID_PATTERN`` (design 9.2); ``ValueError`` else.
    """
    if not valid_operation_id(operation_id):
        raise ValueError("operation_id must match the operation-id pattern")
    return _pending_to(
        doc,
        n,
        "launched",
        now,
        state="launched",
        operation_id=operation_id,
        lease_expires_at=now + LEASE,
        last_reason="launched",
    )


def mark_unknown(
    doc: StoreDoc, n: int, operation_id: str | None, now: datetime
) -> StoreDoc:
    """T-6: ``pending`` to ``unknown``; keeps an ``operation_id`` if Orca gave one.

    ``operation_id`` must be None or match ``OPERATION_ID_PATTERN``; anything
    else raises ``ValueError`` (a saved store must always load again).
    """
    if operation_id is not None and not valid_operation_id(operation_id):
        raise ValueError("operation_id must be None or match the operation-id pattern")
    return _pending_to(
        doc,
        n,
        "launch_unknown",
        now,
        state="unknown",
        operation_id=operation_id,
        last_reason="launch_unknown",
    )


def mark_spawn_error(doc: StoreDoc, n: int, now: datetime) -> StoreDoc:
    """T-7: ``pending`` to ``abandoned`` ``spawn_error`` (OSError before the child)."""
    return _pending_to(
        doc, n, "spawn_error", now, state="abandoned", last_reason="spawn_error"
    )


def sweep(doc: StoreDoc, now: datetime) -> tuple[StoreDoc, list[Entry]]:
    """T-8 and T-9: abandon orphaned ``pending`` and lease-expired ``launched``.

    Every ``pending`` entry becomes ``abandoned`` ``pending_orphan``; every
    ``launched`` entry with ``now >= lease_expires_at`` (or no lease) becomes
    ``abandoned`` ``claim_not_observed``. Returns the new document and the
    changed entries in issue order, so a dry-run can report without saving.
    """
    changed: list[Entry] = []
    for n in sorted(doc.entries):
        entry = doc.entries[n]
        if entry.state == "pending":
            reason = "pending_orphan"
        elif entry.state == "launched" and (
            entry.lease_expires_at is None or now >= entry.lease_expires_at
        ):
            reason = "claim_not_observed"
        else:
            continue
        changed.append(
            replace(entry, state="abandoned", updated_at=now, last_reason=reason)
        )
    entries = dict(doc.entries)
    entries.update((e.issue, e) for e in changed)
    return replace(doc, entries=entries), changed
```

### src/superclaude/cli/issue_watch/predicates.py:162-312

```python
def is_intended_owner(
    assignees: Iterable[str], own_login: str
) -> tuple[bool, str | None]:
    """Return ``(True, None)`` only when the assignee set is exactly {own login}.

    Otherwise the skip reason is ``unassigned`` (empty set) or ``assigned_other``.
    """
    names = set(assignees)
    if names == {own_login}:
        return True, None
    if not names:
        return False, "unassigned"
    return False, "assigned_other"


def _not_approved(reason: str) -> ApprovalResult:
    return ApprovalResult(False, reason, None, None, None)


def _second(value: datetime) -> datetime:
    return value.replace(microsecond=0)


def approval_of(
    events: Iterable[LabelEvent],
    *,
    labels_now: Collection[str],
    trigger_label: str,
    approval_label: str,
    approvers: Collection[int],
    store_created_at: datetime,
) -> ApprovalResult:
    """Apply spec Section 3 "Approved by a human" checks (a) to (e).

    ``events`` must be the complete event history; absent evidence never
    counts as positive.
    """
    ordered = sorted(events, key=lambda e: (e.created_at, e.id))
    appr_on = [e for e in ordered if e.event == "labeled" and e.label == approval_label]
    appr_off = [
        e for e in ordered if e.event == "unlabeled" and e.label == approval_label
    ]
    trig_on = [e for e in ordered if e.event == "labeled" and e.label == trigger_label]
    on_seconds = {_second(e.created_at) for e in appr_on}
    if on_seconds & {_second(e.created_at) for e in appr_off} or on_seconds & {
        _second(e.created_at) for e in trig_on
    }:
        return _not_approved("events_incomplete")
    if approval_label not in labels_now or not appr_on:
        return _not_approved("not_approved")
    approval = appr_on[-1]
    key = (approval.created_at, approval.id)
    if any((e.created_at, e.id) > key for e in appr_off):
        return _not_approved("not_approved")
    if (
        approval.actor_type != "User"
        or approval.actor_login is None
        or approval.actor_login.endswith("[bot]")
        or type(approval.actor_id) is not int
        or approval.actor_id not in approvers
    ):
        return _not_approved("not_approved")
    # OQ-38: no trigger `labeled` event means check (c) cannot pass; this also
    # covers an absent trigger label (absent evidence never counts as positive).
    if not trig_on:
        return _not_approved("events_incomplete")
    if approval.created_at <= trig_on[-1].created_at:
        return _not_approved("approval_before_trigger")
    if approval.created_at <= store_created_at:
        return _not_approved("approval_before_init")
    return ApprovalResult(
        True, None, approval.actor_id, approval.id, approval.created_at
    )


def unchanged_since(
    approved_at: datetime,
    edits: EditEvidence,
    events: Iterable[LabelEvent],
    *,
    own_login: str,
) -> str | None:
    """Return ``edited_after_approval`` unless everything predates ``approved_at``.

    Checks the issue body, every comment not authored by ``own_login`` and
    every ``renamed`` event; an equal timestamp counts as changed (OQ-37).
    """
    times: list[datetime | None] = [
        edits.issue_created_at,
        edits.issue_last_edited_at,
    ]
    for comment in edits.comments:
        if comment.author_login != own_login:
            times += [comment.created_at, comment.last_edited_at]
    times += [e.created_at for e in events if e.event == "renamed"]
    if any(t is not None and t >= approved_at for t in times):
        return "edited_after_approval"
    return None


def project_check(items: Iterable[ProjectItem], project_id: str) -> str | None:
    """Return ``project_mismatch`` unless exactly one live item is in Backlog.

    The item must be non-archived, in ``project_id`` and have Status
    ``Backlog``.
    """
    matching = [i for i in items if not i.is_archived and i.project_id == project_id]
    if len(matching) == 1 and matching[0].status_name == "Backlog":
        return None
    return "project_mismatch"


def marker_time(marker: MarkerEvidence) -> datetime:
    """Return the later of the marker comment's creation and update (DF-16)."""
    return max(marker.created_at, marker.updated_at)


def marker_in_window(
    marker: MarkerEvidence,
    *,
    own_login: str,
    pending_at: datetime | None,
    approved_at: datetime | None,
) -> bool:
    """Return True for an own-login claim marker inside the claim window.

    With ``pending_at`` set the marker counts at or after ``pending_at`` minus
    ``SKEW_TOLERANCE_S``; otherwise only strictly after ``approved_at``.
    """
    if not marker.marker or marker.login != own_login:
        return False
    when = marker_time(marker)
    if pending_at is not None:
        return when >= pending_at - timedelta(seconds=SKEW_TOLERANCE_S)
    return approved_at is not None and when > approved_at


def eligibility_order(
    discovered: Iterable[DiscoveredIssue], considered: Mapping[int, datetime]
) -> list[int]:
    """Order issue numbers: never-examined first by number, then oldest examined.

    Examined issues sort by ``considered[n]`` with ties by number; the
    ``max_candidates`` cap is applied by the cycle.
    """
    numbers = [issue.number for issue in discovered]
    fresh = sorted(n for n in numbers if n not in considered)
    seen = sorted(
        (n for n in numbers if n in considered), key=lambda n: (considered[n], n)
    )
    return fresh + seen
```

### src/superclaude/cli/issue_watch/github.py:376-463

```python
RATE_LIMIT_MAX_WAIT_S = 3600
"""Longest wait taken from a header; anything else clamps to this (FR-028)."""


def _g1_header(result: CommandResult, name: str) -> str | None:
    """Return header ``name`` of a G1 (``--include``) result, else None."""
    if "--include" not in result.argv:
        return None
    split = _split_include(result.stdout)
    return None if split is None else split[0].get(name)


def _header_int(result: CommandResult, name: str) -> int | None:
    """Return a G1 header as a non-negative ``int``, or None when unparseable."""
    value = _g1_header(result, name)
    if value is None or not re.fullmatch(r"[0-9]+", value):
        return None
    return int(value)


def retry_after(result: CommandResult) -> int | None:
    """Return the ``Retry-After`` seconds of a G1 result, or None when absent."""
    return _header_int(result, "retry-after")


def date_header(result: CommandResult) -> datetime | None:
    """Return the G1 ``Date`` header as an aware time, or None when unparseable.

    An unparseable ``Date`` skips the skew check (DF-35).
    """
    value = _g1_header(result, "date")
    if value is None:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if parsed is None:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def rate_limit_wait(result: CommandResult, now: datetime) -> tuple[datetime, str]:
    """Return ``(next_permitted_at, reason)`` for a rate-limited result.

    ``Retry-After`` in 1..3600 s wins; else an ``x-ratelimit-reset`` epoch later
    than ``now`` by at most 3600 s; else now + 3600 s, ``rate_limit_clamped``.
    ``now`` must be timezone-aware.
    """
    seconds = retry_after(result)
    if seconds is not None and 0 < seconds <= RATE_LIMIT_MAX_WAIT_S:
        return now + timedelta(seconds=seconds), "rate_limited"
    reset = _header_int(result, "x-ratelimit-reset")
    if reset is not None and 0 < reset - now.timestamp() <= RATE_LIMIT_MAX_WAIT_S:
        return datetime.fromtimestamp(reset, tz=timezone.utc), "rate_limited"
    return now + timedelta(seconds=RATE_LIMIT_MAX_WAIT_S), "rate_limit_clamped"


# --- call budget (NFR-009) and read results ----------------------------------


class CallBudget:
    """Counts one cycle's ``gh`` calls against ``CALL_CAP`` (NFR-009).

    Per-issue calls share ``CALL_CAP``; the last ``RESERVED_CALLS`` of them are
    kept for the FR-011 re-read. Shared calls (G1, G2) are counted apart.
    """

    def __init__(self) -> None:
        self.calls = 0
        self.shared_calls = 0

    def spend(self, reserved: bool = False) -> bool:
        """Count one per-issue call; False (nothing counted) when it would breach."""
        cap = CALL_CAP if reserved else CALL_CAP - RESERVED_CALLS
        if self.calls >= cap:
            return False
        self.calls += 1
        return True

    def spend_shared(self) -> None:
        """Count one shared call; shared calls are never refused."""
        self.shared_calls += 1

    @property
    def total(self) -> int:
        """Every call counted this cycle, the ``gh_calls`` audit value."""
        return self.calls + self.shared_calls
```

### src/superclaude/cli/issue_watch/github.py:557-628

```python
def _call(
    runner: Runner,
    budget: CallBudget | None,
    timeout_for: Callable[[], float | None],
    argv: list[str],
    *,
    reserved: bool = False,
    include_headers: bool = False,
) -> Reply | None:
    """Spend one call, then run ``argv``; None when no call may start.

    ``budget`` is None for the shared calls G1 and G2, which the cycle counts
    with ``CallBudget.spend_shared``.
    """
    timeout = timeout_for()
    if timeout is None:
        return None
    if budget is not None and not budget.spend(reserved):
        return None
    result = runner.run(argv, timeout)
    return classify(result, include_headers=include_headers)


def _failed(reply: Reply, reason: str) -> Read:
    return Read(None, reason, reply.kind, retry_after(reply.result))


def _shared_failed(reply: Reply) -> Read:
    return _failed(reply, _SHARED_REASONS.get(reply.kind, "gh_auth_failed"))


_NO_CALL = Read(None, "budget_exhausted", "budget_exhausted")
_SHARED_NO_CALL = Read(None, "gh_timeout", "timeout")


def _rest_read(
    runner: Runner,
    budget: CallBudget,
    timeout_for: Callable[[], float | None],
    argv_for_page: Callable[[int], list[str]],
    parse: Callable[[dict], object | None],
    unreadable: str,
    incomplete: str,
    reserved: bool,
) -> Read:
    """Page a G3 or G4 read (design 8.2 table, DF-19); ``parse`` None drops an item."""
    values: list[object] = []
    seen: set[int] = set()
    for page in range(1, PAGE_CAP + 1):
        reply = _call(
            runner, budget, timeout_for, argv_for_page(page), reserved=reserved
        )
        if reply is None:
            return _NO_CALL
        if reply.kind != "ok":
            return _failed(reply, unreadable)
        try:
            items = _list(reply.payload)
            _check(len(items) <= PAGE_SIZE)
            for item in items:
                item_id = _pos_int(_obj(item).get("id"))
                if item_id in seen:
                    return Read(None, incomplete, "incomplete")
                seen.add(item_id)
                parsed = parse(item)
                if parsed is not None:
                    values.append(parsed)
        except _Malformed:
            return Read(None, unreadable, "non_json")
        if len(items) < PAGE_SIZE:
            return Read(tuple(values))
    return Read(None, incomplete, "incomplete")
```

### src/superclaude/cli/issue_watch/github.py:784-842

```python
def user(runner: Runner, timeout_for: Callable[[], float | None]) -> Read:
    """G1: a ``Login`` (own login, account id, ``Date`` header) (FR-002).

    The login regex and the ``owner_account_id`` compare are the cycle's.
    """
    reply = _call(runner, None, timeout_for, argv_user(), include_headers=True)
    if reply is None:
        return _SHARED_NO_CALL
    if reply.kind != "ok":
        return _shared_failed(reply)
    try:
        d = _obj(reply.payload)
        value = Login(
            _text(d.get("login")), _pos_int(d.get("id")), date_header(reply.result)
        )
    except _Malformed:
        return Read(None, "gh_non_json", "non_json")
    return Read(value)


def discover(
    runner: Runner, trigger: str, login: str, timeout_for: Callable[[], float | None]
) -> Read:
    """G2: a tuple of ``DiscoveredIssue`` (FR-003, FR-004).

    ``DISCOVERY_BOUND`` or more results give ``truncated``, a repeated number
    ``discovery_duplicate`` and any malformed element ``non_json``. Raises
    ``ValueError`` before any call for a ``trigger`` or ``login`` that is unsafe
    as a command-line value (the cycle checks both first).
    """
    reply = _call(runner, None, timeout_for, argv_discover(trigger, login))
    if reply is None:
        return _SHARED_NO_CALL
    if reply.kind != "ok":
        return _shared_failed(reply)
    issues: list[DiscoveredIssue] = []
    seen: set[int] = set()
    try:
        items = _list(reply.payload)
        if len(items) >= DISCOVERY_BOUND:
            return Read(None, "truncated", "truncated")
        for item in items:
            d = _obj(item)
            number = _pos_int(d.get("number"))
            _check(valid_issue_number(number))
            if number in seen:
                return Read(None, "discovery_duplicate", "discovery_duplicate")
            seen.add(number)
            issues.append(
                DiscoveredIssue(
                    number=number,
                    labels=_names(d.get("labels"), "name"),
                    assignees=_names(d.get("assignees"), "login"),
                    state=_text(d.get("state")),
                )
            )
    except _Malformed:
        return Read(None, "gh_non_json", "non_json")
    return Read(tuple(issues))
```

### src/superclaude/cli/issue_watch/launch.py:84-132

```python
def build_claim_prompt(n: object) -> str:
    """Return ``/sc:issue --claim <n>`` for an ``int`` in 1..999999999.

    A ``bool``, a ``str``, a ``float`` or an out-of-range ``int`` raises
    ``ValueError`` (FR-012, design 9.3).
    """
    if type(n) is not int or not 1 <= n <= MAX_ISSUE_NUMBER:
        raise ValueError("issue number must be an int in 1..999999999")
    return f"/sc:issue --claim {n}"


def launch_argv(orca: str, worktree: Path | str, prompt: str) -> list[str]:
    """Return the 12-element ``orca agent launch`` argv (FR-013, design 8.4).

    Raises ``ValueError`` when ``prompt`` is not a string ``build_claim_prompt``
    could have returned, so no other text can reach ``--prompt``.
    """
    if not isinstance(prompt, str) or not PROMPT_PATTERN.fullmatch(prompt):
        raise ValueError("prompt must come from build_claim_prompt")
    return [
        orca,
        "agent",
        "launch",
        "--agent",
        ORCA_AGENT,
        "--worktree",
        "path:" + str(worktree),
        "--surface",
        "terminal",
        "--prompt",
        prompt,
        "--json",
    ]


def retry_argv(
    orca: str, worktree: Path | str, prompt: str, operation_id: str
) -> list[str]:
    """Return ``launch_argv`` with ``--retry-launch <id>`` before ``--json`` (D 741).

    Raises ``ValueError`` when ``operation_id`` fails ``OPERATION_ID_PATTERN``,
    because ``status`` prints this argv as a shell command.
    """
    if not isinstance(operation_id, str) or not OPERATION_ID_PATTERN.fullmatch(
        operation_id
    ):
        raise ValueError("operation_id fails the operation-id pattern")
    argv = launch_argv(orca, worktree, prompt)
    return [*argv[:-1], "--retry-launch", operation_id, argv[-1]]
```

### src/superclaude/cli/issue_watch/launch.py:311-355

```python
def outcome_of(result: CommandResult) -> LaunchOutcome:
    """Map one launch ``CommandResult`` to a ``LaunchOutcome`` (design 629-634).

    Anything short of exit 0 with a JSON object carrying a valid operation id is
    ``unknown``; the ``agent_session_operation_unknown`` text anywhere in stdout
    or stderr is ``unknown`` even when an id is present (OQ-40).
    """
    if result.spawn_error is not None:
        return LaunchOutcome("spawn_error", None, "spawn_error")
    if result.timed_out:
        return _unknown(result, "timeout")
    if OP_UNKNOWN_TEXT in result.stdout or OP_UNKNOWN_TEXT in result.stderr:
        return _unknown(result, "op_unknown")
    if result.returncode != 0:
        return _unknown(result, "exit_nonzero")
    reply = _json_object(result.stdout)
    if reply is None:
        return _unknown(result, "non_json")
    hit, value = _first_hit(reply)
    if not hit:
        return _unknown(result, "no_operation_id")
    if not isinstance(value, str) or not _valid_id(value):
        return _unknown(result, "operation_id_invalid")
    return LaunchOutcome("launched", value, "ok")


class OrcaLauncher:
    """The real ``Launcher``: runs ``launch_argv`` through the runner in the worktree."""

    def __init__(self, runner: Runner) -> None:
        self._runner = runner

    def launch(
        self, orca: str, worktree: Path, prompt: str, timeout: float
    ) -> LaunchOutcome:
        """Run the launch argv with ``cwd=worktree`` and map the reply.

        The only call in the package that passes ``cwd`` (DF-01, design 625), so
        an operator retry from ``launch_cwd`` matches Orca's rule. Raises
        ``ValueError`` for a prompt ``build_claim_prompt`` could not have built
        or a timeout that is not a positive number.
        """
        argv = launch_argv(orca, worktree, prompt)
        seconds = _check_timeout(timeout)
        return outcome_of(self._runner.run(argv, seconds, cwd=str(worktree)))
```

## Coverage slice

Rows for reviewer 1 (analyzer): functional requirements FR-001..FR-029 from artifacts/coverage-matrix.yaml lines 199-352 (verbatim; the helper that built them is NOT trusted, re-verify the ones you rely on).

```yaml
requirements:
  # ---------------------------------------------------------------- FR
  - id: FR-001
    status: covered
    impl: ["IW/cycle.py:663-720 _Cycle.run/_steps (enabled+approvers, lock, DISABLED, next_permitted_at, G1, origin, sweep, discovery, candidates)"]
    tests: ["T/test_cycle.py:1283 (gh_argvs == [user, discover]; call order gh,git,gh; one cycle line)", "T/test_cli_e2e.py:299 (real process, PATH stubs)"]
    bites: "yes: asserts exact argv list and order, so any extra or reordered call fails"
  - id: FR-002
    status: covered
    impl: ["IW/cycle.py:733-756 _login_step", "IW/github.py:784-801 user"]
    tests: ["T/test_cycle.py:1314 (exit 3, no further call)", "T/test_cycle.py:1330 (account_id_mismatch exit 2)", "T/test_cycle.py:1357 (bad_login! exit 3, no discovery)", "T/test_security_invariants.py:605 (hostile logins; argvs == [gh api user --include])"]
    bites: yes
  - id: FR-003
    status: covered
    impl: ["IW/github.py:180-198 argv_discover (-L 100, no title/body)", "IW/cycle.py:775-789 _discover (warn at >=80)"]
    tests: ["T/test_github.py:126 (literal argv)", "T/test_cycle.py:1671,1683 (79 no warning, 80 warning)", "T/test_security_invariants.py:637 (allowed forms)", "T/test_no_text.py:816"]
    bites: yes
  - id: FR-004
    status: covered
    impl: ["IW/github.py:804-842 discover (len>=100 truncated; repeated number discovery_duplicate)", "IW/cycle.py:780-783"]
    tests: ["T/test_github.py:1271,1279", "T/test_cycle.py:1625 (99 proceeds), 1640 (>=100 exit 4), 1658 (duplicate exit 4)"]
    bites: yes (99 vs 100 boundary both tested)
  - id: FR-005
    status: covered
    impl: ["IW/predicates.py:185-234 approval_of ((a) to (e), allow-list, [bot], User type, trigger order, store created_at)"]
    tests: ["T/test_predicates.py:108,147,153,165,198,206,228,234,241,273,278,283", "T/test_cycle.py:2461 (each skip row through a whole cycle)"]
    bites: yes (table-driven, includes bool actor id and exact-equal timestamps)
  - id: FR-006
    status: covered
    impl: ["IW/predicates.py:199-215 (latest labeled wins; unlabeled after voids)", "IW/github.py:592-628 _rest_read (repeated id => events_incomplete)"]
    tests: ["T/test_predicates.py:153,165,171", "T/test_github.py:738,750,760 (repeated id, page cap)", "T/test_cycle.py:2461"]
    bites: yes
  - id: FR-007
    status: covered
    impl: ["IW/predicates.py:262-271 project_check", "IW/github.py:907 project_items, 88-103 PROJECT_ITEMS_QUERY", "IW/cycle.py:823-824 (scope_missing => project_read_failed), 938-941"]
    tests: ["T/test_predicates.py:460,477,482", "T/test_cycle.py:2493 (issue 8 unreadable, 9 still launches)", "T/test_cycle.py:4436,1575 (missing scope => exit 3, no decision line)", "T/test_github.py:1137,1148"]
    bites: yes
  - id: FR-008
    status: covered
    impl: ["IW/predicates.py:162-174 is_intended_owner", "IW/cycle.py:919-921 and 972-974 (re-read)"]
    tests: ["T/test_predicates.py:440", "T/test_cycle.py:3215 (re-read {own, other} => assigned_other)", "T/test_security_invariants.py:567"]
    bites: yes
  - id: FR-009
    status: covered
    impl: ["IW/predicates.py:14 CLAIM_MARKER, 274-296 marker_in_window (300 s skew floor)", "IW/github.py:61-65 MARKER_JQ (boolean projection)", "IW/cycle.py:877-894 _claim/_reclaim, 903-912, 927-928"]
    tests: ["T/test_predicates.py:521-563", "T/test_cycle.py:2690,2724,2754,2778,2802,2827", "T/test_marker_contract.py:28 (marker in refs/claim.md and templates/claim-comment.md)"]
    bites: yes
    note: "T/test_marker_contract.py:51 only asserts CLAIM_MARKER in MARKER_JQ (weak, but MARKER_JQ is built from the constant)"
  - id: FR-010
    status: covered
    impl: ["IW/cycle.py:1052-1062 (mark_pending, _save, then launcher.launch)", "IW/record.py:538-568 mark_pending"]
    tests: ["T/test_cycle.py:2925 (launcher callback reads dispatch.json: state pending, launches 1, consumed_at set)", "T/test_cycle.py:4449 (failed pending save => no launch, exit 6)", "T/test_crash_injection.py:287 (C3)"]
    bites: yes (moving the write after launch fails 2925)
  - id: FR-011
    status: covered
    impl: ["IW/cycle.py:960-997 _revalidate, 946-958 _rv, 1027-1030", "IW/github.py:934 reread (REREAD_JQ), reserved calls 437-463"]
    tests: ["T/test_cycle.py:3181 (closed/labels gone), 3215, 3231 (transient => failed, launches 0, attempts 1), 3261, 3275, 3314, 3334, 3349, 3369 (budget), 2565 (pending swept)"]
    bites: yes
  - id: FR-012
    status: covered
    impl: ["IW/launch.py:84-92 build_claim_prompt (type(n) is int, 1..999999999), 101-102 launch_argv guard"]
    tests: ["T/test_launch.py:41-69 (9 ok; '9', True, 0, -1, 10**9, 9.0, False raise; bounds 1 and 999999999)", "T/test_security_invariants.py:451 (property over ~1600 draws, regex match on every recorded prompt, full cycles for bounds)"]
    bites: yes (bool rejected via type() check, covered by True and False params)
  - id: FR-013
    status: covered
    impl: ["IW/launch.py:95-116 launch_argv (12 elements), 163-188 find_orca, 343-355 OrcaLauncher (cwd=worktree, DF-01 departure)", "IW/cycle.py:1017-1022 (probe, orca_not_found exit 2)"]
    tests: ["T/test_launch.py:75 (12-element literal), 225-346 (probe)", "T/test_find_orca_parity.py:145-270", "T/test_cycle.py:3088,3109 (probe failure => exit 2, no entry), 1477 (bad worktree before any gh)"]
    bites: yes
    note: "relative-path worktree rejected in load_config (T/test_cycle.py:323 table), not in a dedicated cycle test"
  - id: FR-014
    status: covered
    impl: ["IW/cycle.py:1007-1075 _launch (probe, prompt, re-read, day cap, DISABLED, deadline, origin, pending, spawn)", "IW/launch.py:311-334 outcome_of", "IW/record.py:503-525 fail, 580-624 mark_*"]
    tests: ["T/test_cycle.py:2925 (_LAUNCH_TRACE order), 3032 (6 unknown outcomes: timeout, non-json, nonzero, no id, empty id, op_unknown => exit 7, launches 1), 3065 (spawn_error), 3122 (prompt ValueError => failed launches 0)", "T/test_launch.py:596-700"]
    bites: yes
  - id: FR-015
    status: covered
    impl: ["IW/launch.py:119-132 retry_argv (full argv with --retry-launch before --json)", "IW/cycle.py:1271-1288 status retry list", "IW/cli.py:158-161"]
    tests: ["T/test_launch.py:152,178,185", "T/test_cycle.py:2536 (no orca argv for launched/unknown/spawn_error entry)", "T/test_cli.py:842,885 (only unknown with id and cwd)"]
    bites: yes
    note: "implements the FULL argv form (C20, owner question Q2), not FR-015's short form: authorized departure. T/test_cli.py:862 builds its expected text with production retry_argv (independently pinned by test_launch.py:152)"
  - id: FR-016
    status: covered
    impl: ["IW/cycle.py:34-35,717 (MAX_CANDIDATES 10), 797-798 and 814-815 (halt after first launch-step outcome, S1)", "IW/github.py:46-49 CALL_CAP/RESERVED_CALLS"]
    tests: ["T/test_cycle.py:3495 (15 skipping issues: k=8, 9 and 10 unstamped; next cycle starts with never-examined)", "T/test_cycle.py:3534 (15 eligible: exactly 1 launch, later issues neither read nor stamped)", "T/test_cycle.py:3145,4653,4668"]
    bites: yes (_touched(world) == {1} fails if the halt is removed)
    note: "S1 reading (owner Q1, DF-50): any launch-step outcome including a skip at the launch step stops the cycle"
  - id: FR-017
    status: covered
    impl: ["IW/record.py:380-419 FileStore.lock (O_NOFOLLOW, S_ISREG, owner, LOCK_NB, inode and nlink recheck)"]
    tests: ["T/test_concurrency.py:146 (two real processes, one launch, 0 and 75), 215,230,243,255", "T/test_record.py:703-849 (753 foreign owner)", "T/test_cycle.py:1385"]
    bites: yes
  - id: FR-018
    status: covered
    impl: ["IW/record.py:421-423 disabled (lexists)", "IW/cycle.py:693-694, 1033-1034 (disabled_mid_cycle), 1101 (no health refresh)"]
    tests: ["T/test_cycle.py:1430 (disabled: zero calls, no stamp)", "T/test_cycle.py:3417,3449 (created after discovery, no pending, exit 0, stamp unchanged)"]
    bites: yes
  - id: FR-019
    status: covered
    impl: ["IW/cycle.py:707-713, 1010-1016, 1109-1125 (shadow commit)", "IW/record.py:805-865 dry-run file"]
    tests: ["T/test_cycle.py:3685 (zero orca calls, store bytes identical, exact trace, shadow file)", "T/test_cycle.py:3659,3739,3747,3773,3827,3845,3860,3873"]
    bites: yes
    note: "dry-run skips the FR-011 re-read and the probe (design reading OQ-39); FR-019 wording 'performs all reads' is narrowed accordingly"
  - id: FR-020
    status: covered
    impl: ["IW/audit.py:123-157 AuditLog.append/rotate_if_needed, 159-197 closed key and type schema, 381-404 stderr_fallback", "IW/cycle.py:1139-1174 _conclude"]
    tests: ["T/test_cycle.py:2017 (exits 0,2,3,4,5,6,7,75: one cycle line, cycle line last, one decision per issue)", "T/test_cycle.py:1403,1417,4533", "T/test_audit.py:490,524 (one os.write),559,580 (4 rotated files),662,674"]
    bites: yes
  - id: FR-021
    status: covered
    impl: ["IW/cycle.py:1233-1298 status_report (read-only, no lock)", "IW/cli.py:164-182"]
    tests: ["T/test_cli.py:785,842,885,927 (900 vs 901 s),938,988 (mtimes unchanged, no audit file)", "T/test_cycle.py:1430,3449 (health stamp rules)"]
    bites: yes
  - id: FR-022
    status: covered
    impl: ["IW/cycle.py:472-497 _Skip/_Stop, 817-827 _val"]
    tests: ["T/test_cycle.py:1584 (9 shared failures => zero launches)", "T/test_cycle.py:1602,2493 (per-issue failure skips only that issue)"]
    bites: yes
  - id: FR-023
    status: covered
    impl: ["IW/predicates.py:299-312 eligibility_order", "IW/record.py:738-745 set_considered", "IW/cycle.py:812-813 (budget_exhausted not stamped), 1097-1100"]
    tests: ["T/test_cycle.py:3584 (order 9,7,8 and 9,8,7; pruning), 3602,3615,3644,3659", "T/test_predicates.py:576,583,590"]
    bites: yes
  - id: FR-024
    status: covered
    impl: ["IW/record.py:538-568 (consumed_at), 689-703 day_cap_count (half-open), 706-720 reset_entry", "IW/cycle.py:848-857, 917-918, 1031-1032 (checked before reads and again after the re-read)"]
    tests: ["T/test_cycle.py:2645 (6 in window => day_cap, zero reads), 2662 (exactly 24 h old not counted), 2673 (consumed_log counts)", "T/test_record.py:1444,1451,1460,1581,1606", "T/test_cli.py:1439 (count unchanged after reset)"]
    bites: yes
  - id: FR-025
    status: covered
    impl: ["IW/launch.py:200-236 parse_origin/check_origin (lower-cased compare)", "IW/cycle.py:651-659, 697-703, 1039-1049 (second check not cached)"]
    tests: ["T/test_cycle.py:1498 (4 failure modes, exit 2 before discovery)", "T/test_cycle.py:3464 (origin changed before pending => exit 2, no entry, 2 origin calls)", "T/test_origin_parity.py:90", "T/test_launch.py:373-518"]
    bites: yes
  - id: FR-026
    status: covered
    impl: ["IW/cli.py:94-348 (once, status, check-config, init-state, reset)", "IW/record.py:706-726, 753-802"]
    tests: ["T/test_cli.py:1213,1234,1406,1439,1488,1536,351,988", "T/test_record.py:1316,1659,1675"]
    bites: yes
  - id: FR-027
    status: covered
    impl: ["IW/cycle.py:195-283 load_config, 298-342 validate_approvers, 352-358 validate_setup, 666-671"]
    tests: ["T/test_cycle.py:98-800 (config and approvers tables: mode, owner, empty, login in place of id)", "T/test_cycle.py:1446 (not_enabled: zero calls), 1462 (dry-run ignores enabled), 1477", "T/test_cli.py:351"]
    bites: yes
    note: "owner-check and unreadable-file cases are skipif root (test_cycle.py:735): silent skip when the suite runs as root"
  - id: FR-028
    status: covered
    impl: ["IW/github.py:376-431 rate_limit_wait", "IW/cycle.py:644-649 _rate_stop (always 3600 s), 729-731 (window check), 738-742 (G1 uses header)"]
    tests: ["T/test_cycle.py:1751 (Retry-After 120, block 60 s later, zero calls), 1782 (half-open end), 1812 (1,3600,3601,86400,0,'soon',None), 1835 (every non-G1 call clamps 3600), 1851,1863", "T/test_cli.py:1488 (reset --rate-limit)"]
    bites: yes
    note: "AUTHORIZED NARROWING (DF-51, design D 598-602): Retry-After and x-ratelimit-reset are honoured only on G1 (the one call run with --include); every other rate-limit reply stores now+3600 with reason rate_limit_clamped. FR-028 prose says 'from Retry-After or the reset header' generally."
  - id: FR-029
    status: covered
    impl: ["IW/cycle.py:383-412 Deadline (240 s, 5 s floor, 120 s cutoff), 1017-1049", "IW/github.py:557-577 _call (timeout None => no call)"]
    tests: ["T/test_cycle.py:931-1043", "T/test_cycle.py:1897,1907,1917 (236 s: no gh, record written),1939,1951,1964 (121 s: no launch),1982 (120 s exactly still launches, full 120 s timeout)", "T/test_cycle.py:4286-4394 (C-1, N-1 fixes)", "T/test_github.py:1998,2009"]
    bites: yes
```
