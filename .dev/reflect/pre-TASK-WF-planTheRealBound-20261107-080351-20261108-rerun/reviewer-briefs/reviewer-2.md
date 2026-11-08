# Reviewer brief (UC-1, pre-execution)

You are a read-only reviewer. Audit the plan at `.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/TASK-WF-planTheRealBound-20261107-080351.md` against its spec `.dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md`. Question: can an executor following this plan produce a meaningful, honest binary B-CTX result? Read the plan fully yourself. Do not edit any file, run no shell. Cite only `file:line` you read, with a short quoted snippet; tag anything not read as [INFERRED]. Classify nothing as a deviation class (UC-1 has none); return findings with severity (HIGH/MEDIUM/LOW), the plan line, the evidence, and a recommendation, and an overall coverage and best-practice judgement.

Persona: qa. Focus on coverage of the spec requirements, acceptance criteria that are missing or uncheckable, the run budget arithmetic, the cleanup and accounting rules, and whether FAIL is honestly reachable and PASS honestly unreachable.

## T1 card excerpt

### Tier 1 coverage statement

INF-001 to INF-010 all covered (10 of 10). INF-006 "no exit-status file" is covered: the matrix miss was lexical (best Constraints, ratio 0.5); the plan's Task 1 heading (plan:29) and ledger (plan:31) provide the exit-status ledger and plan:34, :49, :71, :119 repeat it. The gap list F2.1 to F2.6 is mapped in Task 8 at plan:118: F2.1 and F2.2 need observed evidence, F2.3 and F2.6 can be superseded, F2.4's boot-identity point is superseded by helper:234, F2.5 is closed by the ledger.

### Tier 1 new defects

| id | severity | plan_line | evidence | recommendation |
|---|---|---|---|---|
| N-1 | Medium | plan:22, :31, :66, :119 | ledger is one line per run with the case id; Task 8 counts lines with real_claude true, at most twelve; Task 4 has four shapes in three Claude runs, so one line per shape with real_claude true gives 1+4+4+4 = 13; no run-id field although plan:117 references records by run id | add claude_run_id and a claude_started boolean (true only on the line that starts a Claude process); count distinct started runs; each shape line carries its claude_run_id |
| N-2 | Medium | plan:31, :49, :55, :66 | Tasks 3 and 4 both say "the run group of Task 1" and depend only on Task 2; a Task 4 timeout sweep (cwd under the fixture) can kill Task 3's survivor | one group per task; tear each down at its own task end |
| N-3 | Medium | plan:31 | "per-case cleanup never signals a surviving job" versus "Timeout and teardown also sweep /proc ... and stop each"; a timeout in the resume or fork run would kill the old child and mislabel fork and /clear as "job did not survive" | the timeout sweep must exempt processes registered as surviving; only explicit teardown stops them; label a runner-caused stop distinctly |
| N-4 | Medium | plan:22, :55 | "--max-budget-usd ... (only works with --print)" per claude --help, but the pty /clear run is interactive; live_probe.py:228-255 argv carries --disable-slash-commands which would likely disable /clear [INFERRED]; fresh HOME may show onboarding dialogs [INFERRED] | add an explicit exception for the interactive run (bounded timeout, single scripted turn, no --disable-slash-commands, stated cost bound); "cannot be driven within budget" is the unavailable branch |
| N-5 | Low-Medium | plan:55 | the old child is "a bounded sleep" with no duration; it must outlive the kill, resume, fork and pty runs | state a minimum lifetime (for example 900 s); teardown stops it early |
| N-6 | Low | plan:31, :55 | the kill targets the runner's child handle pid; if claude is a launcher shim the real process could survive [INFERRED]; no check that the first Claude process actually exited | add an AC checking via /proc that no Claude process of the first run remains after the kill |
| N-7 | Low | plan:22, :66 | the four-shapes-in-three-sessions grouping appears only in Constraints; Task 4 does not say how the supervisor-killed shape finds and kills its own supervisor inside one governed command (helper:292 makes the supervisor its own kernel session leader) | put the shape-to-run table and the kill method in Task 4 |
| N-8 | Low | plan:117, :90 | launch-wrapper, Git/hook-tree, auto-mode and decisive rows are limited to observed or unavailable, but Task 6 evidence for wrapper and Git/hook tree is controlled; auto mode has no run and the CLI has --permission-mode, so "unavailable" cannot name a genuinely missing interface (plan:23) | allow controlled for wrapper and Git/hook-tree rows; for auto mode add "not run (budget)" counted as an evidence gap |
| N-9 | Low | plan:31, :44 | preflight flags unspecified; with --tools Bash as in live_probe.py:237-240 the tool list would falsely show subagent and Monitor as not offered | the preflight uses the default tool set |
| N-10 | Low | plan:101, :105 | deep-chain control gives no depth | require depth greater than 64 and bound it for pid limits |
| N-11 | Low | plan:25, :31, :121 | Task 8 compares "git status and diff checksums" of the blocked package while .dev/tasks is staged throughout | use a content hash such as git diff HEAD -- <pkg> or a tree hash, not unstaged status |
| N-12 | Medium (value risk) | plan:22, :31 | the executor runs inside Claude Code so CLAUDECODE is set; a refused nested launch makes the whole real-Claude half unavailable and the report an empty FAIL [INFERRED] | add a Task 1 precondition: run /sc:implement from a terminal that is not a Claude session; unset nothing |
| N-13 | Low | plan:95 | "the only hook installed" needs a script that ignores *.sample files | state the rule |
| N-14 | Info | plan:120 | PASS is unreachable by construction; the binary line carries no information and the two gap lists do the real work | optional: report the contract result and the evidence result separately |

No dependency cycle: Task 1 to Task 2, then Tasks 3 and 4 to Task 7, then Task 8; Tasks 5 and 6 hang off Task 1.

## Grounding hunks

codegraph run state: index_state=n/a checked_at=2026-11-08T02:02:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans projectPath=/home/coder/workspaces/worktrees/IronClaude/finish-leftover-implement-plans (not applicable: inputs are plan, design, shell+python helper, fixture, test; use Grep/Read)

### src/superclaude/hooks/scripts/launch-job-identity.sh:3-20

```bash
# prepare SESSION COMMAND [TOOL_USE_ID] prints a single-use token; run TOKEN
# waits for the main bash AND ordinary non-zombie descendants, returning bash's
# status. identify [PID] prints governed/ordinary/unknown, never command text.
# Release is deletion of sessions/SESSION; malformed live state is unknown.
# shortcut: deliberate setsid/daemonization escapes selection; upgrade to OS
# containment if hostile isolation is required. Killing the supervisor leaves
# unknown stale state, not trusted human identity. Monitor/pipelines unsupported.
# With no arguments, adapt documented PreToolUse Bash JSON on stdin only.
# The hook emits execute SESSION TOOL_ID_OR_EMPTY COMMAND, never a ticket.
# Accepted execution creates and immediately consumes one private request.
# Unverifiable/oversized envelopes are unsupported, not proof of human identity.
# updatedInput replaces the WHOLE input; omit permissionDecision so ordinary
# permission checks still apply. Other hooks' rewrite ordering is unspecified.
# Each call uses a fresh bash: cd is local, and completion waits for ordinary
# background descendants. Always use an explicit cwd/cd in each governed call;
# persistent Claude Bash cwd tracking and live auto-mode rewrites need Task4.
# Missing ordinary state must not require UV or create any launch state.
if [[ $# == 0 || ( $# == 1 && $1 == hook ) ]]; then
```

### src/superclaude/hooks/scripts/launch-job-identity.sh:215-242

```python
def identify(pid):
    root = None
    jobs = None
    try:
        _, sid, _ = proc(pid)
        try:
            root = store()
            jobs = subdir(root, 'jobs')
            raw = read_file(jobs, str(sid) + '.json')
        except FileNotFoundError:
            return {'status': 'ordinary'}
        value = json.loads(raw)
        if not isinstance(value, dict) or set(value) != {'pid', 'start', 'boot', 'kernel_sid', 'session_id'}:
            raise ValueError('invalid record')
        if type(value['pid']) is not int or value['pid'] != sid or type(value['kernel_sid']) is not int or value['kernel_sid'] != sid:
            raise ValueError('invalid supervisor')
        if type(value['start']) is not int or not valid_id(value['session_id']):
            raise ValueError('invalid identity')
        state, actual_sid, start = proc(value['pid'])
        if state == 'Z' or actual_sid != sid or start != value['start'] or boot() != value['boot']:
            raise ValueError('stale supervisor')
        if os.stat('/proc/%d' % sid).st_uid != os.geteuid():
            raise ValueError('foreign supervisor')
        try:
            governed(root, value['session_id'])
        except FileNotFoundError:
            return {'status': 'ordinary', 'reason': 'released'}
        return {'status': 'governed', 'session_id': value['session_id']}
```

### src/superclaude/hooks/scripts/launch-job-identity.sh:322-345

```python
        while True:
            while True:
                try:
                    child, code = os.waitpid(-1, os.WNOHANG)
                except ChildProcessError:
                    break
                if child == 0:
                    break
                if child == shell:
                    status = os.waitstatus_to_exitcode(code)
            live = members(sid)
            if pending:
                forward(live, sid, pending.pop(0))
                deadline = time.monotonic() + 1 if deadline is None else deadline
            if deadline is not None and time.monotonic() >= deadline:
                forward(live, sid, signal.SIGKILL)
            if status is not None and not live:
                return status if status >= 0 else 128 - status
            time.sleep(0.03)
    finally:
        # Only this job's session is ever signalled, including error cleanup.
        try:
            forward(members(sid), sid, signal.SIGKILL)
            # Reap even children that became zombies during the final scan.
```

### src/superclaude/hooks/scripts/launch-job-identity.sh:384-392

```python
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
            def relay(signum, frame):
                try:
                    os.kill(child, signum)
                except ProcessLookupError:
                    pass
            signal.signal(sig, relay)
        signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
        _, code = os.waitpid(child, 0)
```

### tests/hooks/fixtures/launch_level/live_probe.py:228-255

```python
            argv = [
                cli,
                "--print",
                "--setting-sources",
                "",
                "--settings",
                str(settings),
                "--session-id",
                sid,
                "--tools",
                "Bash",
                "--allowedTools",
                "Bash",
                "--permission-mode",
                "dontAsk",
                "--strict-mcp-config",
                "--mcp-config",
                '{"mcpServers":{}}',
                "--max-budget-usd",
                "0.25",
                "--output-format",
                "stream-json",
                "--include-hook-events",
                "--verbose",
                "--no-session-persistence",
                "--disable-slash-commands",
                "--no-chrome",
                prompt,
```

### docs/designs/sc-issue-launch-level-hook.md:504-506

```markdown
**OB-CTX / B-CTX completion evidence (not observed here):** a log-only probe must capture the actual main/subagent/nested/background Bash/Monitor-to-Git and hook process trees, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, launch wrapper, process exit/PID reuse, resume in a new process, /clear/fork, and release while a job remains alive. Establish the needed ancestry bound from that evidence, with an explicit exhaustion rule. In particular, prove how an ordinary new session in a reused Claude process and an old governed background child can be distinguished at the same time. Kernel ancestry alone may not supply that distinction. No single PID-label lookup is accepted as a solution to it.

**Current full-enforcement verdict:** B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**. The owner authorized the new scoped integration; its per-job selector and isolated live Bash evidence are described in §19.7. That is not a retroactive PASS for the old controller-ancestry probe or for unobserved `/clear`, resume, Monitor, nested-subagent and auto-mode variants. Existing claim code still has no pipeline-launch implementation. Keep production activation conditional on the actual supported execution surfaces and their required observations, without a root service or weakening human isolation. O-22/O-21/O-13 are not reopened.
```

### docs/designs/sc-issue-launch-level-hook.md:553-565

```markdown
**Permission boundary:** PreToolUse creates no launch ticket. It emits a shell-quoted invocation of `execute SESSION TOOL_ID_OR_EMPTY COMMAND`. Only when normal permission evaluation allows that invocation to start does `execute` create and immediately consume its private single-use request through the runner. A denied or canceled-before-start rewrite creates no request to replay. The standalone launcher interfaces `prepare SESSION COMMAND [TOOL_USE_ID]` and `run TOKEN` remain explicit caller APIs, not proof that a person approved a command.

**Job lifetime:** each supervisor owns a separate Linux process session, records its actual kernel session/PID/start ticks/boot identity and immutable originating logical session, and waits for the main shell plus ordinary live descendants in that kernel session. The subreaper retains/reaps ordinary orphan descendants after an intermediate shell exits. The main shell's stdout, stderr, stdin, environment, initial cwd and exit status are preserved. A new ordinary tool event from the same controller is not assigned to the old job. The supervisor remains live while ordinary background descendants remain; command completion therefore waits for them deliberately.

**Selector contract:** `identify [PID]` inspects actual kernel process-session membership and validates a live supervisor's PID/start/boot identity plus the origin's current governed record. It emits `governed` with the original session ID, `ordinary` for no registered job or explicit release, and `unknown` for malformed/stale/unreadable registered identity. `unknown` is not a trusted-human verdict. Deleting the origin's level record releases its live jobs without changing another session. Starting a new logical session does not relabel an old job. State location is the configured HOME's launch-level store; callers must preserve that execution context. Arbitrary state relocation or hostile same-user modification is not an isolation guarantee.

**Known execution changes:** wrapped commands run in a fresh Bash shell. An internal `cd` does not persist to later Bash tool calls; use an explicit working directory in each governed call. This adapter is not a transparent replacement for every interactive Bash workflow. Deliberate `setsid`/daemonization escapes kernel-session selection; supervisor killing leaves stale/unknown state for surviving registered jobs. Monitor, other shell tools, remote jobs and unmatched execution mechanisms are not silently supported. No universal hostile-agent protection is claimed.

**Runtime preflight:** UV, the supported Linux process/pidfd/subreaper interfaces, Bash and valid private state must exist for governed execution. With UV absent, jq may establish an exact positively bound session and block it plainly; ordinary unbound calls remain silent. If neither runtime nor parser can establish binding, adaptation is unavailable with no rewrite, not proven human identity or active protection. The future governed launcher must check these prerequisites instead of advertising protection on a host that cannot adapt its jobs.

**Observed versus simulated:** isolated actual CLI PreToolUse/PostToolUse records show one governed call rewritten without a permission-approval decision and reporting the same origin UUID from the executed selector; its ordinary counterpart is not rewritten and reports ordinary. Both actual CLI runs exited 0. The managed identity package `TASK-WF-authorizedNarrow-20261106-214325` retains the redacted `artifacts/live-harness-events.jsonl`. Controlled subprocess tests exercise old-background/new-ordinary overlap, release, stale process data, quoting, startup failure and signal behavior; they are not observations of real `/clear` or resume. Actual persistent-cwd tracking, background scheduling, `/clear`, resume, Monitor, auto mode, concurrent-hook composition and nested-subagent payload variants remain unobserved unless later evidence explicitly adds them.

**Next integration:** a future claim launcher must create the private governed level record for the actual logical session, validate effective adapter/runtime availability and install the separately designed production pre-push policy. That policy may use this selector only on the tested local Bash surface; it must retain an explicit unsupported path for unknown or unadapted execution. This increment does not implement the claim pipeline, the full text classifier, automatic session binding from a claim marker or the production pre-push install/release policy. The earlier blocked workflow remains historical and immutable, not retroactively compliant.
```

### .dev/tasks/to-do/TASK-WF-planTheRealBound-20261107-080351/source.md:1-1 (spec body, whole file)

```text
Plan the real bounded observation run that the blocked package .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206 (its Task 1, the B-CTX feasibility gate) never completed. Use docs/designs/sc-issue-launch-level-hook.md section 19 (especially 19.1 and 19.7, the identity integration in PR #414 and the done package .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325) as the authoritative design, and the operator review findings F2.1 to F2.6 in .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/retries/T1/review-2.md as the gap list: unobserved real cases (ordinary Claude session in the same worktree, /clear, resume into a new process, detached or reparented job, same-worktree human terminal, Monitor and nested subagent), boot identity not compared in the selector, no release with a live child, no exit-status file, and the unmeasured ancestry bound. Plan only observation evidence and the report with a binary result; no production hook, no real protected-branch push, no change to global Claude settings, no commit or push. Do not modify the blocked package -210206. --depth standard --handoff none

```


## Coverage slice

| Requirement | Quote (source.md:1) | Match | Ratio |
|---|---|---|---|
| INF-001 | Plan the real bounded observation run that the blocked package .dev/tasks/to-do/TASK-WF-im | containment (Constraints) | 0.722 |
| INF-002 | Use docs/designs/sc-issue-launch-level-hook.md section 19 (especially 19.1 and 19.7, the i | containment (Constraints) | 0.75 |
| INF-003 | unobserved real cases (ordinary Claude session in the same worktree, /clear, resume into a | containment (T8) | 0.9 |
| INF-004 | boot identity not compared in the selector | containment (T8) | 1.0 |
| INF-005 | no release with a live child | containment (T5) | 1.0 |
| INF-006 | no exit-status file | none (Constraints) | 0.5 |
| INF-007 | the unmeasured ancestry bound | containment (T7) | 0.667 |
| INF-008 | Plan only observation evidence and the report with a binary result | containment (T8) | 0.833 |
| INF-009 | no production hook, no real protected-branch push, no change to global Claude settings, no | containment (Constraints) | 0.8 |
| INF-010 | Do not modify the blocked package -210206. | containment (Constraints) | 0.75 |

Note: INF-006 ('no exit-status file') is a lexical miss of the deterministic rule; confirm or refute against plan Task 1.