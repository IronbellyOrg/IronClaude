# Reviewer 1 brief (persona: analyzer, model class: sonnet)

## T1 card excerpt

```yaml
grounding:
  verification_run:
    ruff_check_touched_files: {exit: 0, result: "All checks passed!"}
    pytest_scoped: {exit: 0, result: "1788 passed in 6.39s", scope: "tests/sweep, tests/commands/test_sweep_command.py, tests/skills/test_worker_contract.py, tests/core/test_how_we_work_routing_table.py, tests/recommend/test_routing_refresh.py"}
    real_entrypoint: {cmd: "uv run superclaude sweep --help and sweep run --help", exit: 0, result: "subcommand `run` listed with options --run --window --root --output"}
    recheck_of_logged_env_failures: "tests/cli/eval/test_claude_process_adapter.py two ruff tests fail with '.venv/bin/python: No module named ruff' (not in the diff); tests/hooks/test_launch_level_guard.py speed tests pass on isolated re-run (6 passed)"
  runtime_surface: "click group `sweep_group` (src/superclaude/cli/sweep/commands.py:214-216), command `run` (commands.py:219-245), deferred import (src/superclaude/cli/main.py:567) and registration `main.add_command(sweep_group, name=\"sweep\")` (src/superclaude/cli/main.py:569), console script superclaude -> cli.main:main: all hit the decorator/registry/packaging degrade oracle -> runtime_surface_degraded=true, unreached=0"
  reuse_sweep: "12 candidates, 0 confident duplicates; 3 maybe-related advisory (_git mirrors reflect/config.py:64, _publish idiom has copies at sprint/recovery.py:433 and install_ccsession.py:83, parse_time mirrors swarm/tui.py:125); neighbour search degraded (auggie unavailable)"
  tasklist_state: "355 checklist items; 353 ticked; unticked are 14.48 (this audit) and 14.49 (set status Done)"
  coverage: "all 50 diff files map to tasklist items (36 by literal path, 14 captured fixtures by the glob in item 7.16, tasklist line 1280): effective unmapped hunks 0, S_dev_density 0.0"
  S_scope: 50
  S_domains: 4          # code, tests, docs, config

  - id: DC-1
    claim: "Classification Rule 5 (`working`) is inert and the agent-wait branch of Rule 4(a) can never match on live data: probes.parse_worker_show never reads agentWait (src/superclaude/cli/sweep/probes.py:432-434) and _rule_working returns None unconditionally (src/superclaude/cli/sweep/classify.py:251-257). SPEC FR-006 says each class name is reached at least once."
    authorization: "Owner decision 'All 3 approved' 2026-11-12 (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md) edited DESIGN line 491 (docs/designs/orchestrator-mode.md:491) so Rule 5 stays inert until open item 6 closes (DESIGN open item 6 at docs/designs/orchestrator-mode.md:997). DESIGN section 13 got no new deviation row (docs/designs/orchestrator-mode.md:840 still says Total: 10 deviations)."
    proposed_class: authorized_expansion   # for Rule 5; the agent-wait feed of 4(a) is necessary (documented inline probes.py:432-434)
    residual: "the report footnote SP24_LINE (src/superclaude/cli/sweep/report.py:42-45) names only stalled and fenced, so `working: 0` carries no caveat"
    confidence: 0.80

  - id: DC-2
    claim: "A worker-list row whose dispatchId is missing or not a string yields only a source row, never a session row (src/superclaude/cli/sweep/probes.py:1105-1119). The FR-010 origin guard reads only the source rows named `orca worker-list <run>` and `orca task-list <run>` (src/superclaude/cli/sweep/classify.py:690-694), so the dropped-row source row `orca worker-list <run> row <i>` does not make the guard fail. Under join path B any non-ready Dispatch row already makes earlier_pane true (classify.py:739), so the effect is confined to a Run whose rows ALL lack a valid id. No test covers it; no recorded decision authorizes it. SPEC FR-005 says the sweep lists every Orca Dispatch row."
    proposed_class: drift
    severity: low
    confidence: 0.60

  - id: DC-3
    claim: "SPEC section 8 (merged-requirements.md:286) says both seams run `subprocess.Popen`, read in chunks and kill the child once output exceeds 8 MiB; the code uses subprocess.run(capture_output=True) and tests the limit only after the child exits (src/superclaude/cli/sweep/probes.py:257-263 with the check at :270; :308-310 with the check at :315). DESIGN names only the result (docs/designs/orchestrator-mode.md:386) and has no deviation row. Observable result is the same for output that ends inside the 10 s timeout."
    proposed_class: drift          # a reviewer may argue regression against SPEC section 8 text; no acceptance criterion fails
    severity: low
    confidence: 0.55

  - id: DC-9
    claim: "Code adds items DESIGN 7.2 does not list (ContractRecord.mtime, OrcaObservation.agent_wait_since reserved, SessionRow.freshness_age_s, four constants in models.py), backward-compatible signature changes (share_shows(runs, wanted=None), optional root params) and a third per-Run source row `orca task-list --ready <run>` (probes.py:1033, :1054; DESIGN 7.4 names two per Run, docs/designs/orchestrator-mode.md:597). Task logged these as MINOR FIN-F10..F12."
    proposed_class: necessary_deviation
    confidence: 0.65

  - id: DC-12
    claim: "(added after calibration, from the calibrator's note) `_git` raises GitCallFailed(f\"output over {OUTPUT_LIMIT} bytes\") (src/superclaude/cli/sweep/probes.py:316), which prints `output over 8388608 bytes`, while SPEC section 8 (.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:286) says the worktree status is unread with the reason `output over 8 MiB`; `_orca` does print MiB (src/superclaude/cli/sweep/probes.py:271-273)."
    proposed_class: drift          # wording of one reason string; check whether any test or DESIGN line pins it
    severity: low
    confidence: 0.60
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T19:25:01Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode

### src/superclaude/cli/sweep/probes.py:252-322

```python
def _orca(*args: str, timeout: float) -> OrcaResult:
    """Run one allowlisted Orca read and classify the result once (SPEC section 8)."""
    check_orca_argv(tuple(args))  # ValueError before any process starts
    binary = orca_binary()
    try:
        proc = subprocess.run(
            [binary, *args],
            capture_output=True,
            timeout=timeout,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return OrcaResult("unavailable", None, f"timeout after {timeout:g} s")
    except FileNotFoundError:
        return OrcaResult("unavailable", None, f"binary not found: {binary}")
    except OSError as exc:
        return OrcaResult("unavailable", None, f"could not start {binary}: {exc}")
    if len(proc.stdout) + len(proc.stderr) > OUTPUT_LIMIT:
        return OrcaResult(
            "call_failed", None, f"output over {OUTPUT_LIMIT // _MIB} MiB"
        )
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace").strip()
    parsed = _json_or_none(out)
    error = parsed.get("error") if isinstance(parsed, dict) else None
    code = error.get("code") if isinstance(error, dict) else None
    first_err = err.splitlines()[0].strip() if err else ""
    # The marker counts only as the error code or the whole first stderr line.
    if code == "runtime_unavailable" or first_err == "runtime_unavailable":
        return OrcaResult("unavailable", None, "runtime_unavailable")
    if proc.returncode != 0:
        return OrcaResult(
            "call_failed", None, f"orca call failed (exit {proc.returncode})"
        )
    if tuple(args) == ("orchestration", "run-current"):
        return _run_current_result(out)
    if (
        isinstance(parsed, dict)
        and parsed.get("ok") is True
        and isinstance(parsed.get("result"), dict)
    ):
        return OrcaResult("ok", parsed["result"], None)
    return OrcaResult("call_failed", None, "orca call failed (invalid response)")


def _git(cwd: Path, *args: str, timeout: float) -> str:
    """Run the allowed git call in ``cwd`` and return its stdout as text.

    The argv always starts ``git --no-optional-locks -C <cwd>`` and the child runs with
    ``GIT_OPTIONAL_LOCKS=0``, so a caller cannot build a git argv without them.
    """
    check_git_args(args)
    argv = ["git", "--no-optional-locks", "-C", str(cwd), *args]
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    try:
        proc = subprocess.run(
            argv, capture_output=True, timeout=timeout, check=False, env=env
        )
    except subprocess.TimeoutExpired as exc:
        raise GitCallFailed(f"timeout after {timeout:g} s") from exc
    except OSError as exc:
        raise GitCallFailed(f"could not start git: {exc}") from exc
    if len(proc.stdout) + len(proc.stderr) > OUTPUT_LIMIT:
        raise GitCallFailed(f"output over {OUTPUT_LIMIT} bytes")
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip().splitlines()
        raise GitCallFailed(
            f"git exited {proc.returncode}" + (f": {detail[0]}" if detail else "")
        )
    return proc.stdout.decode("utf-8", "replace")
```

### src/superclaude/cli/sweep/probes.py:422-465

```python
def parse_worker_show(
    run: str, list_row: object, show: object | None
) -> OrcaObservation:
    """Build one observation from a ``worker-list`` row and its ``worker-show`` result.

    Never raises. The show value wins for every field both return. Fields that only the
    show returns stay None when there is no show, so such a row prints could not
    determine (WC-10) and counts toward ``bound_reached``.
    """
    dispatch = _text(_first(_get(list_row, "dispatchId"), _get(show, "dispatch", "id")))
    # No agentWait field is read: its live name was not captured (step 1.0a, open item 6),
    # so ``agent_wait``, ``agent_wait_present`` and ``agent_wait_since`` keep their model
    # defaults until a read-only capture records the names.
    return OrcaObservation(
        dispatch=dispatch or "",
        run=run,
        session_join=_text(_get(show, "dispatch", "assigneeHandle")),
        dispatch_started=parse_time(_get(show, "dispatch", "dispatchedAt")),
        dispatch_ended=parse_time(_get(show, "dispatch", "completedAt")),
        dispatch_status=_text(_get(show, "dispatch", "status")),
        liveness_verdict=_text(_get(show, "projection", "liveness", "verdict")),
        status=_text(_get(show, "dispatch", "status")),
        outcome=_text(_get(show, "projection", "outcome")),
        parent=_text(
            _first(
                _get(show, "projection", "parent"),
                _get(list_row, "projection", "parent"),
            )
        ),
        worktree_path=_text(_get(show, "terminal", "worktreePath")),
        terminal_state=_text(
            _first(
                _get(show, "projection", "resource", "terminalState"),
                _get(list_row, "terminalState"),
                _get(list_row, "projection", "resource", "terminalState"),
            )
        ),
        next_action=_text(
            _first(
                _get(show, "projection", "nextAction", "kind"),
                _get(list_row, "projection", "nextAction", "kind"),
            )
        ),
    )
```

### src/superclaude/cli/sweep/probes.py:1091-1146

```python
def _run_rows(
    run: str,
    workers: list[dict],
    ready_tasks: list[dict],
    tasks_by_id: dict[str, dict],
    budget: Budget,
    state: _OrcaState,
    sources: list[SourceCoverage],
) -> list[OrcaObservation]:
    raws: dict[str, list[dict]] = {}
    for row in workers:
        raws.setdefault(str(row.get("dispatchId")), []).append(row)
    shows: dict[str, object | None] = {}
    rows: list[OrcaObservation] = []
    for index, row in enumerate(workers):
        dispatch = row.get("dispatchId")
        if not isinstance(dispatch, str) or not re.fullmatch(DISPATCH_ID_RE, dispatch):
            # An id the allowlist would refuse is never put into an argv.
            name = f"orca worker-list {run} row {index}"
            sources.append(
                SourceCoverage(
                    name, "unscanned", None, "row without a valid Dispatch id"
                )
            )
            if isinstance(dispatch, str) and dispatch:
                rows.append(
                    _with_task(parse_worker_show(run, row, None), row, tasks_by_id)
                )
            continue
        disagree = any(r != raws[dispatch][0] for r in raws[dispatch])
        if disagree:
            # Duplicate rows that differ are kept apart; no show is used to pick one.
            obs = replace(
                parse_worker_show(run, row, None),
                dispatch_status=_text(row.get("dispatchStatus")),
            )
            rows.append(_with_task(obs, row, tasks_by_id))
            continue
        show = shows.get(dispatch)
        if dispatch not in shows:
            show = _show(dispatch, run, budget, state, sources)
            shows[dispatch] = show
        rows.append(_with_task(parse_worker_show(run, row, show), row, tasks_by_id))
    known = {r.get("taskId") for r in workers}
    for task in ready_tasks:
        task_id = task.get("id")
        if isinstance(task_id, str) and task_id not in known:
            rows.append(
                OrcaObservation(
                    dispatch=task_id,
                    run=run,
                    status="ready",
                    task_spec_text=_text(task.get("spec")),
                )
            )
    return rows
```

### src/superclaude/cli/sweep/classify.py:226-257

```python
def _rule_waiting_signal(row: SessionRow, ctx: SweepContext) -> Classification | None:
    orca, contract = row.orca, row.contract
    if orca is not None and orca.agent_wait is not None:
        since = orca.agent_wait_since  # reserved: set by nothing yet (open item 6)
        notes: tuple[str, ...] = ()
        evidence = "agent_wait is non-null (worker-show agentWait)"
        if since is not None and since > ctx.now:
            notes = (NOTE_FUTURE,)
        elif since is not None:
            evidence += f"; waiting since {since.isoformat()}"
        return _classification(C_WAITING, "waiting_signal", evidence, "a", notes)
    if contract is not None and contract.worker_status == "failed":
        codes = _freeze_codes(contract)
        if codes:
            evidence = (
                "frozen plan: contract worker_status failed with STOP code "
                + ", ".join(codes)
            )
            return _classification(C_WAITING, "waiting_signal", evidence, "b")
    if orca is not None and orca.status == "ready":
        evidence = "ready Task: creator not observable; needs ownership review"
        return _classification(C_WAITING, "waiting_signal", evidence, "b")
    return None


def _rule_working(row: SessionRow, ctx: SweepContext) -> Classification | None:
    # Rule 5 cannot match in Phase 1 (DESIGN open item 6): the live names of the
    # ``agentWait`` field and of the ``live`` and ``in_progress`` values were never
    # captured, so a row that would reach it falls to the fallback. Once a read-only
    # capture records them, restore the four conditions of DESIGN 7.2 (SP-24):
    # liveness_verdict "live", status "in_progress", agent_wait_present True, agent_wait None.
    return None
```

### src/superclaude/cli/sweep/classify.py:676-740

```python


def _origin_unknown(inp: SweepInput, ctx: SweepContext) -> tuple[str, ...]:
    """The five list-incomplete cases (SPEC FR-010 and R3-B3), in note order."""
    source = {s.name: s for s in inp.sources}
    notes: list[str] = []
    if not inp.orca_available:
        notes.append(NOTE_ORIGIN_UNAVAILABLE)
    if inp.truncated:
        notes.append(NOTE_ORIGIN_TRUNCATED)
    if inp.orca_available:
        runs_seen = {o.run for o in inp.orca_rows}
        failed = unconfirmed = False
        for run in ctx.runs:
            listing = source.get(f"orca worker-list {run}")
            if listing is not None and listing.unscanned is not None:
                failed = True
                continue
            tasks = source.get(f"orca task-list {run}")
            if (
                run not in runs_seen
                and tasks is not None
                and tasks.unscanned is not None
            ):
                unconfirmed = True
        if failed:
            notes.append(NOTE_ORIGIN_CALL_FAILED)
        if unconfirmed:
            notes.append(NOTE_ORIGIN_RUN_NOT_CONFIRMED)
    tabs = source.get("ccsession orca-tabs")
    if tabs is not None and tabs.unscanned is not None:
        notes.append(NOTE_ORIGIN_TAB_MAP)
    return tuple(notes)


@dataclass(frozen=True)
class _Guard:
    origin: tuple[str, ...]
    unobservable: bool  # first case: a scoped Dispatch row has no session_join
    no_join: bool  # second case: workers returned, no transcript joined
    unmatched: bool  # third case (path B): a session_join matches no tab-map entry
    earlier_pane: bool  # fourth case (path B): a scoped Dispatch row exists

    @property
    def failed(self) -> bool:
        return self.unobservable or self.no_join or self.unmatched or self.earlier_pane


def _guard(
    inp: SweepInput, ctx: SweepContext, rows: list[OrcaObservation], j: _Joins
) -> _Guard:
    keys = {k for e in inp.tab_map for k in _entry_keys(e)}
    path_b = JOIN_PATH == "B"
    # A ready Task has no Dispatch, so it is not a scoped Dispatch row (FR-010 cases).
    rows = [r for r in rows if r.status != "ready"]
    return _Guard(
        origin=_origin_unknown(inp, ctx),
        unobservable=any(r.session_join is None for r in rows),
        no_join=bool(rows) and not j.joined,
        unmatched=path_b
        and any(
            r.session_join is not None and r.session_join not in keys for r in rows
        ),
        earlier_pane=path_b and bool(rows),
    )
```

### .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:99-104

```markdown
| FR-005 | The sweep lists every Orca Task/Dispatch row of the selected Runs, every worktree under the tree, and every person-started session (FR-010). Totals that cannot be known are shown as lower bounds, and visible, historical and omitted counts must reconcile. [V3:114, V3:299; Change 11] Reconciliation [SP-05]: `summary.total` = `summary.visible` + `summary.historical`. `summary.bound_reached` counts rows included in `visible` that were not enriched. Rows never discovered are not counted, and when any list is truncated or unscanned, `summary.total_is_lower_bound` is true. Session rows go to JSON `rows`; worktrees go to JSON `worktrees` (section 5.2). | Fixture with 3 workers, 2 worktrees, 1 person session yields 4 entries in JSON `rows` and 2 entries in JSON `worktrees`; the report's Sessions heading reads `(4/4)` and its Worktrees section has 2 rows. [SP-05] |
| FR-006 | Each session row gets exactly one class from section 7, chosen by the ordered rule table. | Parametrized test, one case per section 7 rule (REPORT rules 1-7 plus idle and person session (active) [SP-14]); each class name is reached at least once. |
| FR-007 | `classify` receives a `SweepContext` holding `now`, `window` and `window_start` (GQ-103(2)). | A row whose `last_activity` (section 7 source rule [SP-15]) is 5 h old is idle-eligible only when window is under 5 h; same row, window 6 h, is not idle. A fixture whose last JSONL record carries a timestamp older than the file's `st_mtime` uses the record's timestamp and names that source in `evidence`. [SP-15] |
| FR-008 | "Could not determine" is its own class, never folded into stalled or idle; `unverifiable`, a late heartbeat, a stale `liveStatus` or a missing row give it (WC-10, `WORKER-CONTRACT.md:45`). | Fixtures for each of the four inputs give `could not determine`, never `stalled (proved)`. |
| FR-009 | Stalled (proved) only from Orca's own exit proof with no `worker_done` and no fencing evidence; with fencing evidence unreadable rule 2 declines and attaches the note; the row is classified by later rules, and by the fallback if none matches (REPORT step 1.3 rules 2, 3; GQ-84). [V3R3:53; INV-007; Change 6] | Two cases, neither using a blocked contract [Conv:326; Change 6]: (1) an exited row with unreadable fencing evidence and a `guard refused:` body classifies as finished (rule 6) and carries the note `Orca: exited; fenced evidence not readable`; (2) an exited row with unreadable fencing evidence and nothing else classifies as could not determine through rule 9 (the fallback) [SP-14] and carries the same note. |
| FR-010 | A person-started session is a transcript under a scanned root's project key that the ccsession tab map joins to no Orca row; one with no activity inside the window goes to Historical sessions (GQ-108). Represent `person_started` as True, False or None. A positive transcript-to-worker join makes it False. Only when every scoped Run's worker list is complete, no relevant list or join is unscanned or truncated, and the tab map is read and the join completed may an unjoined transcript be True. Otherwise it is None. None never becomes idle or Historical; an origin-unknown transcript is could not determine, with an explicit reason such as Orca unavailable, worker list truncated, worker list call failed or tab map unreadable. Idle requires True and the existing readability and activity-window conditions. [V3R3:33; INV-003; Change 5] The C-014 full-page lower-bound note and this completeness guard apply together; counting only discovered rows does not establish a complete negative join. [V3R3:55; INV-009] Other Runs [SP-29]: a transcript that the tab map marks as an Orca worker session (any Run), or whose session id appears in any Orca row returned by `worker-list` for any Run, is never True. If the tab map records the Run id and it is outside the scope, the row is `person_started` False with note `worker of Run <id>, outside scope` and is not classified further. The tab map fields that carry this are UNVERIFIED until `/sc:design` reads the ccsession tab map format. The join key and the empty or stale tab map rule are in section 7 (SessionRow, `row_id`) [SP-16]. A transcript must be readable to count; an unknown timestamp is never idle; open Tasks, explicit waits and unread-report candidates are exempt from the activity window and never go to Historical. [V3:93, V3:2 [line cut for the brief; re-Read the file]
```

### .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:283-297

```markdown

- `_orca` runs `[<binary>, *args]`, where `<binary>` is `ORCA_CLI_COMMAND` if set, else `orca-ide`. This is a deliberate safety deviation from orca-cli SKILL.md:27, which selects bare `orca` inside Orca-managed terminals; the sweep cannot reliably tell it is in one, and bare `orca` outside one starts the GNOME screen reader (SKILL.md:24-26). The resolved binary name is recorded in the report header (section 9). [V1R3:48, V2R3:49; INV-017; Change 9]
- `_git(cwd, *args) -> str` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]` itself and passes `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. A caller passes only the subcommand, so no call site can omit the flag. This is the first item built and the first test written (GQ-103(1)).
- Both check the argv against the allowlist before running, then run it with `subprocess.Popen` (stdout and stderr piped, decoded as UTF-8) and read the output in chunks until the process exits or the per-call timeout passes; a nonzero exit or a timeout raises, as `check=True` would. Once the combined output exceeds 8 MiB, reading stops, the process is killed, and the result is `call_failed` with reason `output over 8 MiB` (for `_git`, that worktree's status is unread with the same reason). An argv outside the allowlist raises `ValueError` (exit 1, a bug, not a source loss). [Change 24 for the timeout; SP-28]
- Orca result classes [V3R3:32; INV-002; Change 4]: Classify each `_orca` result once as `ok`, `no_binding`, `unavailable` or `call_failed`. First apply the unavailable checks: launch `OSError`, call timeout (except the budget-cut case below), or the `runtime_unavailable` marker. The marker counts only as the captured error field value (for example a JSON `error.code` equal to `runtime_unavailable`; UNVERIFIED shape until step 1.0a) or as the whole first line of stderr; the same text inside any other JSON string field, such as `body_text`, is ignored. [SP-07] AC: a zero-exit `worker-show` body whose `body_text` quotes `runtime_unavailable` is classified `ok`, and `orca_available` stays true; a stderr whose later line, not the first, holds the marker is not unavailable for that reason. [SP-07] Also treat nonzero exit or invalid response on the first Orca call as unavailable. Stop further Orca calls after unavailable. A later nonzero exit or invalid response without those unavailable signals is `call_failed`: mark that source or row unscanned, preserve its failure reason, leave dependent evidence unknown, and continue independent reads within budget. Invalid response includes empty or unparseable stdout and JSON that cannot establish the operation's captured success or no-binding shape. `no_binding` applies only to zero-exit `run-current` with the captured explicit no-binding shape, never to an empty body, arbitrary null or a missing field guessed to mean no binding. Those shapes remain UNVERIFIED until step 1.0a. `ok` requires the captured success shape. Use `orca call failed (exit <n>)` for nonzero exit and `orca call failed (invalid response)` for response failure, retaining the actual exit separately. An earlier successful call plus a later `call_failed` does not prov [line cut for the brief; re-Read the file]
- Step 1.0a capture is a precondition for the result parser, because `ok` and `no_binding` require captured shapes. [Conv:273; Change 4]
- A launch failure because the binary is missing is an `unavailable` result with reason `binary not found: orca-ide` (or the `ORCA_CLI_COMMAND` value). [Change 9]
- A `Budget` object (50 `worker-show`, 90 s total) is passed into `collect`, never global, so tests set it per case. Each call's timeout is the lesser of 10 s and the remaining total budget. [V3:124-125, V3:137; Change 24]
- Budget scope [SP-10]: every `_git` call has a 10 s timeout and counts against the same 90 s total. Disk reads are bounded by the byte limits and are not timed. The cap of 50 `worker-show` calls is split evenly across the selected Runs, with the remainder to the first Run; a Run's unused share passes to the next Run. `bound_reached` is the count of rows that needed a `worker-show` call and did not get one; the cap line prints only when it is at least 1.
- Budget exhaustion [SP-08]: a call whose timeout was cut below 10 s by the remaining budget, and that times out, is `call_failed` with reason `unscanned: time budget reached (90 s)`, never `unavailable`; `orca_available` stays true. No call starts when less than 1 s of budget remains; the sources and rows it would have read get the same reason. Rows denied a `worker-show` call by the cap of 50 get `unscanned: show cap reached (50)`. AC: with 88.5 s used, the next call gets a 1.5 s timeout and times out; `orca_available` is true and the row carries the time-budget reason. With 89.5 s used, no further call starts and the remaining rows carry the same reason.
- Byte limits (proposed; rationale required before release) [SP-28]:
  - A transcript tail read of the last 256 KiB is the normal case, not a limit hit: drop bytes up to and including the first newline, decode as UTF-8 with `errors="replace"`, and parse the remaining complete lines.
  - A contract or ledger read is a hit when the file size is greater than 1 MiB; a file of exactly 1 MiB is not a hit. A contract hit marks that contract unscanned with reason `over 1 MiB`. A ledger hit is not unscanned: the ledger is read as its first 512 KiB and its last 512 KiB (split proposed), and the tail is searched for a `FINAL:` line.
  - Subprocess output over 8 MiB is handled by the seams as stated above.
  - AC: fixtures at limit minus 1, at the limit and at limit plus 1 for each of the three limits.
```

### docs/designs/orchestrator-mode.md:484-492

```markdown
| 7 | `idle` | idle |
| 8 | `person_active` | person session (active) |
| 9 | `fallback` | could not determine |

Rule conditions are the SPEC table text. Three readings are fixed here:

- Rule 1 notes (M6): a decline under `ask the coordinator` on a live unsettled row adds the note `blocked contract under ask the coordinator; may be re-running`; a decline with `gate_policy` None on a live row adds the same note; a contract with no Orca row declines with `blocked contract; Orca state not observed` unless a Ruling halt matches.
- Rule 5 (SP-24), one condition per line: `liveness_verdict == "live"`; `status == "in_progress"`; `agent_wait_present is True`; `agent_wait is None`. All four must hold once the names are known. Until step 1.0a item 4 records them (open item 6) Rule 5 is inert: it returns None and a row that would reach it falls to the fallback, and these four conditions are kept in `classify.py` as the text to restore. Field sources (the `worker-show` field names, the `live` and `in_progress` values and the `agentWait` key are NOT yet captured, UNVERIFIED): `liveness_verdict`, `status`, `agentWait` presence and value would come from `worker-show`; `worker_done_seen` is None on every live row; `fenced_evidence` is `unreadable` on every live row (SPEC line 231).
- Age (SP-26, D5): a `last_activity` or waiting timestamp later than `now` is unknown age, adds note `timestamp in the future`, and never satisfies rule 7.
```

### docs/designs/orchestrator-mode.md:596-598

```markdown

Every Run in `ctx.runs` has its own source row named `orca worker-list <run>` and another named `orca task-list <run>` (the `task-list --run <run>` call); `orca` there is the literal word, not `$ORCA_CLI_COMMAND`. A `call_failed` result sets the row's `unscanned` reason (for example `orca call failed (exit 1)`), and a Run whose call was never started because the time budget ran out gets `unscanned: time budget reached (90 s)` on the row. `collect` sets `truncated` when a Run's `worker-list` returns `WORKER_LIST_PAGE` (100) rows. The tab-map folder has the row `ccsession orca-tabs`. The list-incomplete rule of section 7.2 reads these rows.

```

### docs/designs/orchestrator-mode.md:823-840

```markdown
## 13. Deviations from SPEC

A deviation is a place where this design states something the SPEC text does not say, or says differently. Each one comes from the PANEL, FIXREVIEW or the design review (`docs/designs/orchestrator-mode-review-1.md`) and is applied in the section named. D-numbers here are this design's own; they are not the owner decision D3 that `WORKER-CONTRACT.md` line 23 mentions (quoted in section 8).

| ID | SPEC text | Design | Source | Section |
|---|---|---|---|---|
| D1 | Module table line 199: `report.py` holds `write_report(text, output_dir, now) -> Path`, the package's only write; line 200: `commands.py` calls `write_report`; section 11 line 448 names `OSError` in `write_report` | No `write_report`. The one write is `commands._publish`; `os` joins the `commands.py` may-import list; `report.py` is pure as a whole | SP-20 | 3.1, 4 |
| D2 | Section 11 line 453: a killed process may leave a report file without the `Report complete` footer; G-1 (lines 637-645) leaves the exit-1 disk state open | Temp file, `fsync`, then `os.link` as the commit point; no report name ever holds partial bytes; the exit-1 rule of section 3.4 is added to SPEC section 5.3 | G-1, PANEL lines 289-296 | 3.2 to 3.4 |
| D3 | FR-002 and FR-019 message `Orca unavailable; no Run binding could be established: pass --run <id>` | `Orca unavailable (<reason>); no Run binding could be established: pass --run <id>`, with the `OrcaResult.reason` in the parentheses | SP-21 | 5 |
| D4 | No cell length limit | `report.cell` cuts a Markdown table cell at 200 characters ending `...`; JSON values are never cut | SP-23 | 7.1, 7.5 |
| D5 | Age has no rule for a timestamp after `now` | A future timestamp is unknown age, adds note `timestamp in the future`, and never satisfies rule 7 (idle) | SP-26 | 7.2 |
| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-16, with master's cadence "at most once every 5 minutes" (contract line 110) in place of "It sweeps on every wake"; `/sc:sweep` stated as an added read beside the unchanged line 110 sweep (not a replacement, not a second pass, no heartbeat update, no `--agent-wait` listing), with a sentence that its own reads are not L1 probes and do not count against the L1 cap; and one sentence appended: the coordinator records each admission or rejection in its run notes; `/sc:sweep` does not observe them. No new pin | SP-27 | 8 |
| D7 | Rule 5 at line 253 reads only "`live`, `in_progress`, `agent_wait_present` and null"; the report says nothing about classes Phase 1 cannot observe | Rule 5 restated as four conditions, one per line, with each field source; the report adds the footnote that stalled and fenced are not observed in Phase 1 and a zero count does not mean none occurred | SP-24 | 7.2, 7.5 |
| D8 | Branch header case at line 335: `ahead N` gives `unpushed N` (a count) | `unpushed` is `bool \| None` as SPEC line 240 types it, with `upstream_note` carrying `ahead N` and the other notes; JSON `unpushed` is never a count | M7 | 2.2, 7.2, 7.4 |
| D9 | FR-010 and SP-29 (line 104): a transcript that the tab map marks as an Orca worker session (any Run), or whose session id appears in any Orca row of any Run, is never True | A worker is a transcript joined to a Dispatch row of a scoped Run (path A or B). A tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs`, so person sessions started through `ccsession` in Orca panes are never idle or Historical in Phase 1. Under path A only, a transcript with no tab-map entry and no scoped join may be True when the guard holds, so a worker of an unscoped Run that has no entry can be True. Every True reached this way carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and in the JSON `notes`, so such a session is never shown as person-started without a note. Under path B the guard has four join-incomplete cases; the fourth (an earlier session of a reused pane has no entry) makes every unjoined no-entry transcript None, and a path-B join also needs the Dispatch row's time window, a transcript whose tail is complete and, when several rows match one pane session, exactly one window holding it. D9 as first written covers only True becoming None. Two residual path-B cases are new and need the same owner sign-off, which is still pending: a window with no end (a row still `pending` or `dispatched`) has no upper bound, so a person's later session in that pane, started after the worker died, joins the row as False and is shown as `orca:<dispatch>`, not as a person session; and a live session that serves two Dispatches joins the older row only, while the newer row is could not determine. Reason: the ccsession file cannot tell a worker pane from a person pane and holds no Run id, i [line cut for the brief; re-Read the file]
| D10 | NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619: `worktree ps` never carries `--agent-wait` | `worktree ps --agent-wait` (with and without `--json`) is allowed; `FORBIDDEN_TOKENS` holds only `--include-remote`; the NFR-014 exact-set pin covers ten templates, not eight | Owner decision R5, 2026-11-08: "Allow it, no conditions needed." | 2.2, 4, 7.3, 11, 12, 15.1 |

Total: 10 deviations.
```

## Coverage slice

| Diff file | Hunks | Tasklist items naming the path | Status |
|---|---|---|---|
| src/superclaude/cli/sweep/__init__.py | 1 | ['8.2', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19', '8.20'] | mapped (literal path) |
| src/superclaude/cli/sweep/classify.py | 1 | ['8.4', '10.2', '14.49'] | mapped (literal path) |
| src/superclaude/cli/sweep/commands.py | 1 | ['9.1', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10', '9.11'] | mapped (literal path) |
| src/superclaude/cli/sweep/models.py | 1 | ['8.3', '10.2', '14.49'] | mapped (literal path) |
| src/superclaude/cli/sweep/probes.py | 1 | ['8.5', '8.10', '9.3', '9.7', '9.12', '10.2', '10.3', '14.49'] | mapped (literal path) |
| src/superclaude/cli/sweep/report.py | 1 | ['8.12', '10.5', '14.49'] | mapped (literal path) |
| tests/sweep/conftest.py | 1 | ['8.8', '8.11', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19'] | mapped (literal path) |
| tests/sweep/test_classify.py | 1 | ['2.5', '3.2', '4.3', '10.2', '14.49'] | mapped (literal path) |
| tests/sweep/test_cli_contract.py | 1 | ['10.7', '14.49'] | mapped (literal path) |
| tests/sweep/test_cli_registration.py | 1 | ['10.6'] | mapped (literal path) |
| tests/sweep/test_probes_allowlist.py | 1 | ['2.5', '10.3', '14.49'] | mapped (literal path) |
| tests/sweep/test_readonly.py | 1 | ['8.9', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19', '8.20'] | mapped (literal path) |
| tests/sweep/test_report.py | 1 | ['10.5', '14.49'] | mapped (literal path) |

Rows are file-level (the mapping is per file, not per hunk).
