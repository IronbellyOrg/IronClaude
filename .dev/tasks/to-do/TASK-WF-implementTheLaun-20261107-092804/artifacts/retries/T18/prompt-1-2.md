2972aa6ec7b94a4518c3976bb881929401428f0b
Review one task for spec compliance.

Task brief: ## Task 18: Make the claim refuse a governed launch when the guard is not effective (IR-4)

Depends on: Task 13

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py replace the warning-only check enforcement_status() (which today only tests that ~/.claude/hooks/launch-level-guard.sh exists and is executable, and whose absence only adds W-ENFORCEMENT-ABSENT after the agent has already started) with the IR-4 check of design section 13, run before publish_pending() so a refused launch writes no pending record and starts no agent. The launch is refused, as a failed launch with the warning code W-ENFORCEMENT-ABSENT and a plain reason, unless all of these hold: jq is on PATH; the installed script exists, is executable and carries the line "# launch-level-guard-version: 1" (the version this plan ships, read from the installed file); the effective configuration enables both registrations, meaning the user settings file under the configured home holds the exact command ~/.claude/hooks/launch-level-guard.sh under UserPromptSubmit and under PreToolUse and neither that file nor the worktree's project settings files set disableAllHooks to true; and CLAUDE_CONFIG_DIR, when set, resolves to the same directory as the home .claude folder (otherwise the launch is refused, never inspecting one directory while another executes). "Registration enabled" also means the PreToolUse registration carries the matcher of design section 13 (so it fires for the governed tools) and the UserPromptSubmit registration has no matcher that prevents it from firing on a prompt; a registration that holds the command but cannot fire is refused. The preflight also checks the identity adapter's runtime prerequisites that design section 19.7 lists for a future governed launcher: uv on PATH, a Linux host with the process interfaces the adapter uses, and the launch-job-identity.sh registration on Bash PreToolUse. Put the new checks in cmd_launch after the already-launched and stale-prompt checks and before publish_pending, and state that order in a comment so the stale-prompt tests and la3 keep their meaning. The check never edits any configuration. The claim script cannot see the environment the launched agent runs in, so the refusal text says it verified the claim process only. A claim with --pipeline none is unaffected (it never reaches this script; test that at the claim-protocol level or by asserting the launch subcommand is not called). State in the task what the enforcement_hook result field means after the change (installed, missing or null today) and keep the ten-key return-contract test and SKILL.md in agreement. Update REMEDY["W-ENFORCEMENT-ABSENT"] to say the launch was refused and what to run (superclaude install, then claim again).

Update tests/skills/test_issue_orca_worktree.py: the two existing tests that expect W-ENFORCEMENT-ABSENT as a warning on a launched claim (around lines 1303 and 1324) now expect a refusal with no orca agent launch call and no pending file; add cases for each failing condition (no jq, script not executable, wrong version line, missing UserPromptSubmit registration, missing PreToolUse registration, disableAllHooks true in user settings and in the worktree project settings, CLAUDE_CONFIG_DIR elsewhere) and a passing case that proceeds to the launch.

Acceptance criteria:
- uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the updated and new cases.
- For every refusal case the fake orca records no agent launch call, the home directory has no pending/<nonce> file, and the claim output names the failed condition.
- With the guard installed, both registrations present and jq available, the launch proceeds exactly as before this task and records the launch entry.
- The check reads configuration files only; a test asserts the settings files are byte-identical before and after.
- launch_scene is migrated (a guard file with the version line and the executable bit, a settings.json with both registrations, a known jq, CLAUDE_CONFIG_DIR unset) and every test whose result changes is named in the task, including la2, la3, la6 and the tests at lines 1246, 1291, 1313 and the pr425 pair; the whole file passes with uv run pytest tests/skills/test_issue_orca_worktree.py -v.
- A registration that holds the guard command but whose matcher excludes the governed tools, and one under UserPromptSubmit with a matcher that prevents it from firing, are each refused by a test; a missing uv or a missing launch-job-identity.sh registration is refused by a test; none of these refusals writes a pending record or starts an agent.
- The refusal text for a stale installed guard names the command that actually replaces it (an existing installed script is skipped without force), not just superclaude install.

AC ids (source order):
T18.AC1: uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the updated and new cases.
T18.AC2: For every refusal case the fake orca records no agent launch call, the home directory has no pending/<nonce> file, and the claim output names the failed condition.
T18.AC3: With the guard installed, both registrations present and jq available, the launch proceeds exactly as before this task and records the launch entry.
T18.AC4: The check reads configuration files only; a test asserts the settings files are byte-identical before and after.
T18.AC5: launch_scene is migrated (a guard file with the version line and the executable bit, a settings.json with both registrations, a known jq, CLAUDE_CONFIG_DIR unset) and every test whose result changes is named in the task, including la2, la3, la6 and the tests at lines 1246, 1291, 1313 and the pr425 pair; the whole file passes with uv run pytest tests/skills/test_issue_orca_worktree.py -v.
T18.AC6: A registration that holds the guard command but whose matcher excludes the governed tools, and one under UserPromptSubmit with a matcher that prevents it from firing, are each refused by a test; a missing uv or a missing launch-job-identity.sh registration is refused by a test; none of these refusals writes a pending record or starts an agent.
T18.AC7: The refusal text for a stale installed guard names the command that actually replaces it (an existing installed script is skipped without force), not just superclaude install.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: 2972aa6ec7b94a4518c3976bb881929401428f0b
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log
new file mode 100644
index 00000000..867e77bb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log
@@ -0,0 +1,5 @@
+$ uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/skills/test_worker_contract.py -q  (after the fix pass)
+
+============================= 921 passed in 26.48s =============================
+$ make verify-sync
+exit=0
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index cb08de2c..635a7944 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -89,7 +89,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
 7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Then continue with Wave 7 and Wave 8. A STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. This skill never runs a step of `next-steps.md` (B2).
 8. **Wave 7, worktree.** `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` creates or reuses the worktree and copies `<D>` into it. Every failure is a warning: the claim `status` stays `success`.
-9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook. The agent, not this skill, runs the steps. Every failure is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result, every warning with its remedy line), the return contract, and STOP.
+9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when it would not; otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook. The agent, not this skill, runs the steps. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result, every warning with its remedy line), the return contract, and STOP.
 
 ## Create mode
 
@@ -133,7 +133,7 @@ launch_warning: <W- code or null>
 enforcement_hook: installed | missing | null
 ```
 
-`launch_status` is `not_requested` for `--pipeline none` and when `worktree_status` is `failed`. `worktree_match_key` is `null` for a newly created worktree. `enforcement_hook` is `null` when no agent was requested or the launch was `already_launched`; otherwise it is `installed` or `missing`, also after a failed launch. The claim `status` stays `success` through any worktree or launch warning.
+`launch_status` is `not_requested` for `--pipeline none` and when `worktree_status` is `failed`. `worktree_match_key` is `null` for a newly created worktree. `enforcement_hook` reports the IR-4 preflight of the launch: `installed` means it passed (also when the launch then failed), `missing` means it failed and the launch was refused (`launch_status` `failed`, `launch_warning` `W-ENFORCEMENT-ABSENT`, no agent started), and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). The claim `status` stays `success` through any worktree or launch warning.
 
 On a STOP, also print the STOP code and its message.
 
@@ -147,7 +147,7 @@ On a STOP, also print the STOP code and its message.
 | `gh auth status` fails | STOP `E-GH-AUTH` |
 | `orca_worktree.py preflight` prints `ok: false` (Orca not installed, not running or not reachable) | STOP `E-ORCA-REQUIRED` with the script's `detail`, before any GitHub or ClickUp write |
 | Worktree step fails or needs attention (`W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-ORIGIN-BASE-STALE`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`) | Warning only: the claim `status` stays `success`; print the code with its remedy line from `refs/claim.md` |
-| Launch step fails or needs attention (`W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`) | Warning only: the claim `status` stays `success`; print the code with its remedy line from `refs/claim.md`; no launch is attempted for a failed worktree or for `--pipeline none` |
+| Launch step fails or needs attention (`W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`) | Warning only: the claim `status` stays `success`; print the code with its remedy line from `refs/claim.md`; no launch is attempted for a failed worktree or for `--pipeline none`. `W-ENFORCEMENT-ABSENT` means the launch was refused and no agent was started |
 | Issue closed | STOP, message "Issue #N is closed; not claimed.", no writes |
 | Assigned to someone else | STOP, message names the assignee, no writes |
 | Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 0c432a01..41cb3d94 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -116,13 +116,13 @@ Runs only when `--pipeline` is not `none` and the Wave 7 `status` is `created` o
 
 `uv run --no-project python "<skill base>/scripts/orca_worktree.py" launch --number <N> --source <D> --level <L> [--submit]`
 
-Read the one JSON object it prints: `status` (`launched`, `already_launched` or `failed`), `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook` and `hand_command`. The script starts one agent behind the ccsession shim in the worktree and records the level where the enforcement hook of issue 394 can read it. A `launch` entry in `<D>/worktree.json` makes it return `already_launched` without calling Orca. Every failure is a warning, never a STOP: the claim `status` stays `success`. Remedy lines of the launch codes:
+Read the one JSON object it prints: `status` (`launched`, `already_launched` or `failed`), `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook` and `hand_command`. Before anything else the script runs the IR-4 preflight, which reads files and the environment only and never edits configuration: `jq` and `uv` on `PATH`, a Linux host, `~/.claude/hooks/launch-level-guard.sh` installed, executable and at version 1, the guard registered on `UserPromptSubmit` and on `PreToolUse` for every governed tool in `$HOME/.claude/settings.json`, `launch-job-identity.sh` registered on Bash `PreToolUse`, no `disableAllHooks` in the user or worktree project settings, and `CLAUDE_CONFIG_DIR` unset or equal to `$HOME/.claude`. When any fails it refuses the launch: `status` `failed`, `warning` `W-ENFORCEMENT-ABSENT`, `enforcement_hook` `missing`, a `detail` naming each failed condition, no agent and no launch record. It verifies the claim process only, not the environment the agent will run in. When all pass (`enforcement_hook` `installed`), the script starts one agent behind the ccsession shim in the worktree and records the level where the enforcement hook of issue 394 can read it. A `launch` entry in `<D>/worktree.json` makes it return `already_launched` without calling Orca. Every failure is a warning, never a STOP: the claim `status` stays `success`. Remedy lines of the launch codes:
 
 | Code | Remedy line |
 |---|---|
 | `W-LAUNCH-FAILED` | re-run the claim; the hand command is printed for reference (an agent started by hand is not governed by the hook). When the `detail` says the worktree's `launch-prompt.md` is not the one rendered for this claim, no agent was started and no hand command is printed: make that file match `<D>/launch-prompt.md` first, a re-run alone fails again |
 | `W-LAUNCH-NOT-CCSESSION` | this agent is NOT behind the ccsession shim, or could not be verified; close it. Orca's Claude command must be the ccsession-orca wrapper |
-| `W-ENFORCEMENT-ABSENT` | the level is an instruction in the prompt only until the launch-level hook (#394) ships; do not use `full` or `--submit` on a real issue yet |
+| `W-ENFORCEMENT-ABSENT` | the launch was refused and no agent was started; fix each condition the `detail` names (most are fixed by running `superclaude install`; a stale installed guard or registration needs `superclaude install --force`), then claim the issue again |
 
 ## Final output (replaces "print the path and STOP")
 
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index f3cfe846..562ef754 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -37,7 +37,9 @@ with ``--level worktree`` is a bad argument (exit 2).
 
 ``launch --number <N> --source <D> --level worktree|full [--submit]`` starts one
 Claude Code agent in the worktree recorded in ``<D>/worktree.json``. It first
-publishes the launch record the enforcement hook reads
+runs the IR-4 preflight (jq, uv, Linux, the installed guard and its settings
+registrations; read only) and refuses the launch with ``W-ENFORCEMENT-ABSENT``
+when the guard would not be effective. It then publishes the launch record the enforcement hook reads
 (``$HOME/.claude/state/launch-level/pending/<nonce>``, one word), then runs
 ``orca agent launch --surface terminal`` with a prompt that starts with
 ``[sc-launch:v1:<nonce>]``, checks the agent's screen for the ccsession shim, and
@@ -709,20 +711,210 @@ REMEDY = {
         "close it. Orca's Claude command must be the ccsession-orca wrapper"
     ),
     "W-ENFORCEMENT-ABSENT": (
-        "the level is an instruction in the prompt only until the launch-level "
-        "hook (#394) ships; do not use full or --submit on a real issue yet"
+        "the launch was refused and no agent was started; fix each condition "
+        "named above (most are fixed by running superclaude install), then "
+        "claim the issue again"
     ),
 }
+# IR-4: what the claim checks before a governed launch. It reads files and the
+# environment only and never edits any configuration.
+GUARD_COMMAND = "~/.claude/hooks/launch-level-guard.sh"
+IDENTITY_COMMAND = "~/.claude/hooks/launch-job-identity.sh"
+GUARD_VERSION_LINE = "# launch-level-guard-version: 1"
+GOVERNED_TOOLS = (
+    "Bash",
+    "Skill",
+    "Agent",
+    "Task",
+    "Edit",
+    "Write",
+    "NotebookEdit",
+    "Monitor",
+    "Workflow",
+    "RemoteTrigger",
+    "SendMessage",
+    "CronCreate",
+    "CronDelete",
+    "ScheduleWakeup",
+    # The mcp__ branch of the design matcher: a registration without it misses these.
+    "mcp__x__merge_pull_request",
+    "mcp__x__push_files",
+    "mcp__x__create_or_update_file",
+)
+FIRE_ALWAYS = (None, "", "*")
+LINUX_FILES = ("/proc/self/stat", "/proc/sys/kernel/random/boot_id")
+PR_GET_CHILD_SUBREAPER = 37  # linux/prctl.h
+
+
+def process_interface_gaps() -> list[str]:
+    """The process interfaces of the job identity hook that this host lacks.
+
+    Read-only probes on the claim process itself: the /proc files, pidfd_open of
+    its own pid, and the query form of the child-subreaper call.
+    """
+    if not sys.platform.startswith("linux"):
+        return [f"sys.platform is {sys.platform}, not Linux"]
+    gaps = [p for p in LINUX_FILES if not os.path.exists(p)]
+    try:
+        import ctypes
+
+        libc = ctypes.CDLL(None, use_errno=True)
+    except OSError:
+        return gaps + ["pidfd_open", "prctl(PR_GET_CHILD_SUBREAPER)"]
+    try:
+        # libc, like the hook: some UV Python builds omit os.pidfd_open.
+        fd = libc.pidfd_open(os.getpid(), 0)
+        if fd < 0:
+            gaps.append("pidfd_open")
+        else:
+            os.close(fd)
+    except AttributeError:
+        gaps.append("pidfd_open")
+    try:
+        flag = ctypes.c_int()
+        if libc.prctl(PR_GET_CHILD_SUBREAPER, ctypes.byref(flag), 0, 0, 0) != 0:
+            gaps.append("prctl(PR_GET_CHILD_SUBREAPER)")
+    except AttributeError:
+        gaps.append("prctl(PR_GET_CHILD_SUBREAPER)")
+    return gaps
 
 
 def home_dir() -> Path:
     return Path(os.environ.get("HOME") or Path.home())
 
 
-def enforcement_status() -> str:
-    """``installed`` when the hook script exists and is executable, else ``missing``."""
-    hook = home_dir() / HOOK_SCRIPT
-    return "installed" if hook.is_file() and os.access(hook, os.X_OK) else "missing"
+def read_settings(path: Path, required: bool) -> tuple[dict, str | None]:
+    """The settings object at ``path`` and why it could not be used, else None."""
+    try:
+        data = json.loads(path.read_text(encoding="utf-8"))
+    except FileNotFoundError:
+        return (
+            {},
+            f"{path} does not exist (run superclaude install)" if required else None,
+        )
+    except (OSError, ValueError) as exc:
+        return {}, f"{path} cannot be read as JSON: {exc} (fix that file)"
+    if not isinstance(data, dict):
+        return {}, f"{path} is not a JSON object (fix that file)"
+    return data, None
+
+
+def matchers_for(settings: dict, event: str, command: str) -> list[object]:
+    """The matcher of every ``event`` registration that holds ``command``."""
+    hooks = settings.get("hooks")
+    groups = hooks.get(event) if isinstance(hooks, dict) else None
+    found: list[object] = []
+    for group in groups if isinstance(groups, list) else []:
+        inner = group.get("hooks") if isinstance(group, dict) else None
+        if isinstance(inner, list) and any(
+            isinstance(h, dict) and h.get("command") == command for h in inner
+        ):
+            found.append(group.get("matcher"))
+    return found
+
+
+def fires_for(matcher: object, tool: str) -> bool:
+    if matcher in FIRE_ALWAYS:
+        return True
+    if not isinstance(matcher, str):
+        return False
+    try:
+        return re.search(matcher, tool) is not None
+    except re.error:
+        return False
+
+
+def enforcement_preflight(wt: str) -> list[str]:
+    """IR-4: every reason the launch-level guard would not be effective; [] if none.
+
+    Only the claim process is seen: its HOME, PATH and environment, and the
+    settings files on disk. The agent Orca starts may run with another one.
+    """
+    home = home_dir()
+    stale = "run superclaude install --force to replace it"
+    restale = "run superclaude install --force to replace the registration"
+    failures: list[str] = []
+    for tool in ("jq", "uv"):
+        if shutil.which(tool) is None:
+            failures.append(f"{tool} is not on PATH (install {tool})")
+    gaps = process_interface_gaps()
+    if gaps:
+        failures.append(
+            "this host lacks "
+            + ", ".join(gaps)
+            + ", which the job identity hook needs (governed launches are Linux only)"
+        )
+    script = home / HOOK_SCRIPT
+    if not script.is_file():
+        failures.append(f"{script} is not installed (run superclaude install)")
+    else:
+        if not os.access(script, os.X_OK):
+            failures.append(f"{script} is installed but not executable ({stale})")
+        try:
+            lines = script.read_text(encoding="utf-8", errors="replace").splitlines()
+        except OSError as exc:
+            lines, why = [], f"cannot be read: {exc}"
+        else:
+            why = f"lacks the line '{GUARD_VERSION_LINE}'"
+        if GUARD_VERSION_LINE not in (line.rstrip() for line in lines):
+            failures.append(f"{script} is installed but stale: it {why} ({stale})")
+    config = os.environ.get("CLAUDE_CONFIG_DIR")
+    if config and os.path.realpath(os.path.expanduser(config)) != os.path.realpath(
+        home / ".claude"
+    ):
+        failures.append(
+            f"CLAUDE_CONFIG_DIR is {config}, not {home / '.claude'}, so the user "
+            "settings checked here may not be the ones Claude Code loads (unset it "
+            "or point it at $HOME/.claude)"
+        )
+    user_path = home / ".claude" / "settings.json"
+    user, user_why = read_settings(user_path, required=True)
+    failures += [user_why] if user_why else []
+    files = [(user_path, user)]
+    for name in ("settings.json", "settings.local.json"):
+        path = Path(wt) / ".claude" / name
+        data, why = read_settings(path, required=False)
+        failures += [why] if why else []
+        files.append((path, data))
+    for path, data in files:
+        if data.get("disableAllHooks") is True:
+            failures.append(
+                f"{path} sets disableAllHooks to true, so no hook runs (remove that "
+                "setting; the claim never edits it)"
+            )
+    if not user_why:
+        prompt = matchers_for(user, "UserPromptSubmit", GUARD_COMMAND)
+        if not prompt:
+            failures.append(
+                f"{user_path} has no UserPromptSubmit registration of "
+                f"{GUARD_COMMAND} (run superclaude install)"
+            )
+        elif not any(m in FIRE_ALWAYS or m == ".*" for m in prompt):
+            failures.append(
+                f"the UserPromptSubmit registration of {GUARD_COMMAND} in {user_path} "
+                f"has a matcher that may stop it firing ({restale})"
+            )
+        tools = matchers_for(user, "PreToolUse", GUARD_COMMAND)
+        missed = [t for t in GOVERNED_TOOLS if not any(fires_for(m, t) for m in tools)]
+        if not tools:
+            failures.append(
+                f"{user_path} has no PreToolUse registration of {GUARD_COMMAND} "
+                "(run superclaude install)"
+            )
+        elif missed:
+            failures.append(
+                f"the PreToolUse registration of {GUARD_COMMAND} in {user_path} "
+                f"does not fire for {', '.join(missed)} ({restale})"
+            )
+        identity = matchers_for(user, "PreToolUse", IDENTITY_COMMAND)
+        if not any(fires_for(m, "Bash") for m in identity):
+            failures.append(
+                f"{user_path} has no PreToolUse registration of {IDENTITY_COMMAND} "
+                "that fires for Bash (run superclaude install"
+                + (", with --force" if identity else "")
+                + ")"
+            )
+    return failures
 
 
 def publish_pending(word: str) -> tuple[str, Path]:
@@ -934,7 +1126,30 @@ def cmd_launch(args: argparse.Namespace) -> int:
     stale = stale_prompt(source, Path(wt), number)
     if stale:
         return emit(launch_result("failed", [(failed, stale)]))
-    hook = enforcement_status()
+    # Order: the already-launched and stale-prompt checks above come first, the
+    # IR-4 preflight next, and only then publish_pending, so a refusal leaves no
+    # launch record and starts no agent. enforcement_hook in the result means:
+    # "installed" the preflight passed, "missing" it failed and the launch was
+    # refused, null (the launch_result default) no preflight ran.
+    absent = enforcement_preflight(wt)
+    if absent:
+        return emit(
+            launch_result(
+                "failed",
+                [
+                    (
+                        "W-ENFORCEMENT-ABSENT",
+                        "the launch-level guard would not be effective: "
+                        + "; ".join(absent)
+                        + ". This check verified the claim process only (its "
+                        "HOME, PATH, environment and the settings files on "
+                        "disk), not the environment the agent would run in",
+                    )
+                ],
+                enforcement_hook="missing",
+            )
+        )
+    hook = "installed"
     notes: list[tuple[str, str]] = []
     word = "full-submit" if args.submit else args.level
     try:
@@ -983,10 +1198,6 @@ def cmd_launch(args: argparse.Namespace) -> int:
                 else "the launch result named no terminal",
             )
         )
-    if hook == "missing":
-        notes.append(
-            ("W-ENFORCEMENT-ABSENT", "the launch-level hook script is not installed")
-        )
     at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
     unrecorded = ""
     problems = record_launch(source, args.level, args.submit, at, wt, number)
diff --git a/tests/skills/test_issue_orca_worktree.py b/tests/skills/test_issue_orca_worktree.py
index 4c9f374d..cdeffc78 100644
--- a/tests/skills/test_issue_orca_worktree.py
+++ b/tests/skills/test_issue_orca_worktree.py
@@ -10,6 +10,7 @@ from __future__ import annotations
 import json
 import os
 import re
+import shutil
 import stat
 import subprocess
 import sys
@@ -79,6 +80,23 @@ class FakeOrca:
         exe = self.bin / "orca"
         exe.write_text(FAKE_ORCA.format(python=sys.executable))
         exe.chmod(0o755)
+        # Known jq and uv stubs (the IR-4 preflight only looks them up on PATH).
+        self.tools = root / "tool-bin"
+        self.tools.mkdir()
+        for name in ("jq", "uv"):
+            stub = self.tools / name
+            stub.write_text("#!/bin/sh\nexit 0\n")
+            stub.chmod(0o755)
+
+    def path_without(self, *names: str) -> str:
+        """A PATH holding orca, git and the tool stubs, minus ``names``."""
+        bare = self.bin.parent / ("bare-" + "-".join(names))
+        bare.mkdir()
+        (bare / "git").symlink_to(shutil.which("git"))
+        for stub in self.tools.iterdir():
+            if stub.name not in names:
+                (bare / stub.name).symlink_to(stub)
+        return f"{self.bin}{os.pathsep}{bare}"
 
     def respond(self, key: str, *responses: dict) -> None:
         """Set the answers for one orca subcommand (``status``, ``worktree-list``...)."""
@@ -101,7 +119,8 @@ class FakeOrca:
 
     def env(self, **extra: str) -> dict[str, str]:
         env = dict(os.environ)
-        env["PATH"] = f"{self.bin}{os.pathsep}{env['PATH']}"
+        env["PATH"] = os.pathsep.join([str(self.bin), str(self.tools), env["PATH"]])
+        env.pop("CLAUDE_CONFIG_DIR", None)
         env["FAKE_ORCA_DIR"] = str(self.dir)
         env["HOME"] = str(self.home)
         # Hermetic git: the script's own git calls ignore the user's config.
@@ -994,7 +1013,13 @@ PROMPT_RE = re.compile(
 def launch_scene(
     fake: FakeOrca, git_repo: Path, issue_dir: Path, *, hook: str | None = "exec"
 ) -> Path:
-    """A real worktree with a guarded record, an Orca that launches and a hook."""
+    """A real worktree with a guarded record, an Orca that launches and the guard.
+
+    ``hook="exec"`` installs what the IR-4 preflight needs: the versioned,
+    executable guard and a user settings.json holding the shipped hooks.json
+    registrations (both guard entries and the identity entry). ``"plain"`` is
+    the same without the executable bit; ``None`` creates nothing in HOME.
+    """
     wt = add_worktree(git_repo, "issue-302", "ironbelly/issue-302")
     (issue_dir / "worktree.json").write_text(
         json.dumps({"path": str(wt), "status": "created"})
@@ -1008,11 +1033,21 @@ def launch_scene(
     if hook:
         script = fake.home / ".claude" / "hooks" / "launch-level-guard.sh"
         script.parent.mkdir(parents=True)
-        script.write_text("#!/bin/sh\n")
+        script.write_text("#!/bin/sh\n# launch-level-guard-version: 1\n")
         script.chmod(0o755 if hook == "exec" else 0o644)
+        user_settings(fake).write_text(HOOKS_JSON.read_text())
     return wt
 
 
+HOOKS_JSON = REPO_ROOT / "src/superclaude/hooks/hooks.json"
+GUARD = "~/.claude/hooks/launch-level-guard.sh"
+IDENTITY = "~/.claude/hooks/launch-job-identity.sh"
+
+
+def user_settings(fake: FakeOrca) -> Path:
+    return fake.home / ".claude" / "settings.json"
+
+
 def run_launch(
     fake: FakeOrca,
     git_repo: Path,
@@ -1159,8 +1194,8 @@ def test_la3_launch_failure_removes_the_record_and_prints_a_hand_command(
 def test_la3_launch_with_an_unwritable_record_store_makes_no_launch_call(
     fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
 ) -> None:
-    launch_scene(fake_orca, git_repo, issue_dir, hook=None)
-    (fake_orca.home / ".claude").write_text("a file where the store should be\n")
+    launch_scene(fake_orca, git_repo, issue_dir)  # the IR-4 preflight passes
+    (fake_orca.home / ".claude/state").write_text("a file where the store should be\n")
     data = run_launch(fake_orca, git_repo, issue_dir)
     assert data["status"] == "failed" and data["warning"] == "W-LAUNCH-FAILED"
     assert "launch record" in data["detail"]
@@ -1292,36 +1327,271 @@ def test_la5_launch_handle_is_found_anywhere_in_the_result(
     assert orca_calls(fake_orca, "terminal", "read")[0][3] == "term_deep"
 
 
+def assert_refused(fake: FakeOrca, data: dict, *names: str) -> None:
+    """An IR-4 refusal: no agent, no launch record, and the condition is named."""
+    assert data["status"] == "failed" and data["warning"] == "W-ENFORCEMENT-ABSENT"
+    assert data["enforcement_hook"] == "missing" and data["hand_command"] is None
+    assert data["terminal"] is None and data["launched_at"] is None
+    assert "verified the claim process only" in data["detail"]
+    assert "superclaude install" in data["detail"]  # the REMEDY text
+    for name in names:
+        assert name in data["detail"], (name, data["detail"])
+    assert launch_calls(fake) == [] and orca_calls(fake, "terminal", "read") == []
+    assert not (fake.home / ".claude/state").exists()  # so no pending/<nonce>
+
+
 @pytest.mark.parametrize("hook", [None, "plain"], ids=["absent", "not-executable"])
-def test_la6_launch_without_an_executable_hook_warns_and_still_launches(
+def test_la6_launch_without_an_executable_hook_is_refused(
     fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, hook: str | None
 ) -> None:
     launch_scene(fake_orca, git_repo, issue_dir, hook=hook)
     data = run_launch(fake_orca, git_repo, issue_dir)
-    assert data["status"] == "launched"
-    assert data["enforcement_hook"] == "missing"
-    assert data["warning"] == "W-ENFORCEMENT-ABSENT"
-    assert "#394" in data["detail"]
-    assert len(launch_calls(fake_orca)) == 1
+    assert_refused(
+        fake_orca, data, "not installed" if hook is None else "not executable"
+    )
+    assert "launch" not in json.loads((issue_dir / "worktree.json").read_text())
 
 
+@pytest.mark.parametrize(
+    "env",
+    [{}, {"CLAUDE_CONFIG_DIR": "same"}],
+    ids=["default", "config-dir-same"],
+)
 def test_la6_launch_with_the_hook_installed_has_no_warning(
-    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
+    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, env: dict
 ) -> None:
     launch_scene(fake_orca, git_repo, issue_dir)
-    data = run_launch(fake_orca, git_repo, issue_dir)
+    if env:
+        env = {"CLAUDE_CONFIG_DIR": str(fake_orca.home / ".claude") + "/"}
+    before = user_settings(fake_orca).read_bytes()
+    data = run_launch(fake_orca, git_repo, issue_dir, **env)
+    assert data["status"] == "launched"
     assert data["enforcement_hook"] == "installed" and data["warning"] is None
     assert len(launch_calls(fake_orca)) == 1
+    assert user_settings(fake_orca).read_bytes() == before
 
 
-def test_la6_launch_two_warnings_put_the_shim_one_first(
+def test_la6_launch_refusal_comes_before_any_shim_check(
     fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
 ) -> None:
     launch_scene(fake_orca, git_repo, issue_dir, hook=None)
     fake_orca.respond("terminal-read", {"stdout": SCREEN_PLAIN})
     data = run_launch(fake_orca, git_repo, issue_dir)
-    assert data["warning"] == "W-LAUNCH-NOT-CCSESSION"
-    assert "also W-ENFORCEMENT-ABSENT" in data["detail"]
+    assert_refused(fake_orca, data)
+    assert "W-LAUNCH-NOT-CCSESSION" not in data["detail"]
+
+
+# --- IR-4 preflight: one refusal per failing condition ------------------------
+
+
+def edit_settings(path: Path, change) -> None:
+    data = json.loads(path.read_text()) if path.exists() else {}
+    change(data)
+    path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(json.dumps(data, indent=2))
+
+
+def drop(event: str, command: str):
+    def change(data: dict) -> None:
+        data["hooks"][event] = [
+            g
+            for g in data["hooks"][event]
+            if not any(h["command"] == command for h in g["hooks"])
+        ]
+
+    return change
+
+
+def set_matcher(event: str, command: str, matcher: str):
+    def change(data: dict) -> None:
+        for group in data["hooks"][event]:
+            if any(h["command"] == command for h in group["hooks"]):
+                group["matcher"] = matcher
+
+    return change
+
+
+def disable_hooks(data: dict) -> None:
+    data["disableAllHooks"] = True
+
+
+def guard_script(fake: FakeOrca) -> Path:
+    return fake.home / ".claude/hooks/launch-level-guard.sh"
+
+
+# Each case: what to break (given the fake and the worktree; returns extra env)
+# and the text the refusal must contain to name that condition.
+IR4_CASES = {
+    "no-jq": (
+        lambda f, wt: {"PATH": f.path_without("jq")},
+        ["jq is not on PATH"],
+    ),
+    "no-uv": (
+        lambda f, wt: {"PATH": f.path_without("uv")},
+        ["uv is not on PATH"],
+    ),
+    "script-not-executable": (
+        lambda f, wt: guard_script(f).chmod(0o644),
+        ["not executable", "superclaude install --force"],
+    ),
+    "wrong-version-line": (
+        lambda f, wt: guard_script(f).write_text(
+            "#!/bin/sh\n# launch-level-guard-version: 0\n"
+        ),
+        ["launch-level-guard-version: 1", "stale", "superclaude install --force"],
+    ),
+    "no-user-prompt-registration": (
+        lambda f, wt: edit_settings(user_settings(f), drop("UserPromptSubmit", GUARD)),
+        [f"no UserPromptSubmit registration of {GUARD}"],
+    ),
+    "no-pretooluse-registration": (
+        lambda f, wt: edit_settings(user_settings(f), drop("PreToolUse", GUARD)),
+        [f"no PreToolUse registration of {GUARD}"],
+    ),
+    "matcher-excludes-governed-tools": (
+        lambda f, wt: edit_settings(
+            user_settings(f), set_matcher("PreToolUse", GUARD, "^(Bash|Edit|Write)$")
+        ),
+        ["does not fire for Skill, Agent, Task", "ScheduleWakeup"],
+    ),
+    # The design matcher minus its mcp__ branch: the plain tools fire, the
+    # GitHub write tools of an MCP server do not.
+    "matcher-without-mcp-branch": (
+        lambda f, wt: edit_settings(
+            user_settings(f),
+            set_matcher(
+                "PreToolUse",
+                GUARD,
+                "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow"
+                "|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$",
+            ),
+        ),
+        ["does not fire for mcp__x__merge_pull_request", "mcp__x__push_files"],
+    ),
+    "user-prompt-matcher-cannot-fire": (
+        lambda f, wt: edit_settings(
+            user_settings(f), set_matcher("UserPromptSubmit", GUARD, "never")
+        ),
+        ["UserPromptSubmit registration", "may stop it firing"],
+    ),
+    "disable-all-hooks-user": (
+        lambda f, wt: edit_settings(user_settings(f), disable_hooks),
+        ["settings.json sets disableAllHooks"],
+    ),
+    "disable-all-hooks-project": (
+        lambda f, wt: edit_settings(wt / ".claude/settings.json", disable_hooks),
+        [".claude/settings.json sets disableAllHooks"],
+    ),
+    "disable-all-hooks-project-local": (
+        lambda f, wt: edit_settings(wt / ".claude/settings.local.json", disable_hooks),
+        ["settings.local.json sets disableAllHooks"],
+    ),
+    "config-dir-elsewhere": (
+        lambda f, wt: {"CLAUDE_CONFIG_DIR": str(f.home / "other-claude")},
+        ["CLAUDE_CONFIG_DIR is", "unset it"],
+    ),
+    "no-identity-registration": (
+        lambda f, wt: edit_settings(user_settings(f), drop("PreToolUse", IDENTITY)),
+        [f"no PreToolUse registration of {IDENTITY} that fires for Bash"],
+    ),
+}
+
+
+@pytest.mark.parametrize("case", sorted(IR4_CASES))
+def test_ir4_each_failing_condition_refuses_the_launch(
+    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, case: str
+) -> None:
+    wt = launch_scene(fake_orca, git_repo, issue_dir)
+    breaker, names = IR4_CASES[case]
+    env = breaker(fake_orca, wt)
+    env = env if isinstance(env, dict) else {}
+    files = [user_settings(fake_orca)] + [
+        wt / ".claude" / n for n in ("settings.json", "settings.local.json")
+    ]
+    before = {p: p.read_bytes() for p in files if p.exists()}
+    data = run_launch(fake_orca, git_repo, issue_dir, **env)
+    assert_refused(fake_orca, data, *names)
+    if "disable-all-hooks-project" in case:
+        assert str(wt) in data["detail"]
+    # The check never edits configuration.
+    assert {p: p.read_bytes() for p in files if p.exists()} == before
+    assert "launch" not in json.loads((issue_dir / "worktree.json").read_text())
+
+
+def test_ir4_stale_registrations_name_the_force_flag(
+    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
+) -> None:
+    launch_scene(fake_orca, git_repo, issue_dir)
+    edit_settings(user_settings(fake_orca), set_matcher("PreToolUse", GUARD, "Bash"))
+    data = run_launch(fake_orca, git_repo, issue_dir)
+    assert_refused(
+        fake_orca, data, "run superclaude install --force to replace the registration"
+    )
+
+
+def test_ir4_non_linux_host_is_refused(
+    monkeypatch: pytest.MonkeyPatch,
+    fake_orca: FakeOrca,
+    git_repo: Path,
+    issue_dir: Path,
+) -> None:
+    import importlib.util
+
+    wt = launch_scene(fake_orca, git_repo, issue_dir)
+    spec = importlib.util.spec_from_file_location("orca_worktree_ir4", SCRIPT)
+    module = importlib.util.module_from_spec(spec)
+    monkeypatch.setitem(sys.modules, spec.name, module)  # dataclasses need it
+    spec.loader.exec_module(module)
+    for key, value in fake_orca.env().items():
+        monkeypatch.setenv(key, value)
+    assert module.enforcement_preflight(str(wt)) == []
+    monkeypatch.setattr(module.sys, "platform", "darwin")
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "not Linux" in reason and "job identity hook needs" in reason
+
+    # The process interfaces the identity hook uses are probed on the claim
+    # process itself, read-only: pidfd_open and the child-subreaper query.
+    monkeypatch.undo()
+    for key, value in fake_orca.env().items():
+        monkeypatch.setenv(key, value)
+
+    import ctypes
+
+    class FakeLibc:
+        def __init__(self, pidfd: int, prctl: int) -> None:
+            self.pidfd, self.prctl_result = pidfd, prctl
+
+        def pidfd_open(self, pid: int, flags: int) -> int:
+            return self.pidfd
+
+        def prctl(self, *_args) -> int:
+            return self.prctl_result
+
+    real_cdll = ctypes.CDLL
+    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: FakeLibc(-1, 0))
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "lacks pidfd_open" in reason and "prctl" not in reason
+    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: FakeLibc(-1, -1))
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "pidfd_open, prctl(PR_GET_CHILD_SUBREAPER)" in reason
+    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: object())  # no symbols
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "pidfd_open, prctl(PR_GET_CHILD_SUBREAPER)" in reason
+    monkeypatch.setattr(ctypes, "CDLL", real_cdll)
+    assert module.enforcement_preflight(str(wt)) == []
+
+
+def test_ir4_pipeline_none_never_reaches_the_preflight(
+    fake_orca: FakeOrca, issue_dir: Path
+) -> None:
+    # Nothing is installed in HOME; --level none is still a bad argument (exit 2),
+    # and the claim runs Wave 8 only when --pipeline is not none.
+    args = ["--number", "302", "--source", str(issue_dir), "--level", "none"]
+    proc = run_script("launch", *args, env=fake_orca.env())
+    assert proc.returncode == 2 and "W-ENFORCEMENT-ABSENT" not in proc.stdout
+    assert fake_orca.calls() == [] and not (fake_orca.home / ".claude").exists()
+    claim = (SCRIPT.parents[1] / "refs/claim.md").read_text()
+    assert "Runs only when `--pipeline` is not `none`" in claim
 
 
 def test_la7_launch_without_a_usable_worktree_record_calls_nothing(

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log
index dae3211a..867e77bb 100644
--- a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t18-test.log
@@ -1,22 +1,5 @@
-$ uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/skills/test_worker_contract.py -q
-........................................................................ [ 90%]
-........................................................................ [ 98%]
-..................                                                       [100%]
+$ uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/skills/test_worker_contract.py -q  (after the fix pass)
 
-============================= 920 passed in 24.83s =============================
-$ make sync-dev
-   Skills:    39 directories
-   Agents:    48 files
-   Commands:  46 files
-   Hooks:     15 files
-   Templates: 52 files
+============================= 921 passed in 26.48s =============================
 $ make verify-sync
-
-=== Hooks Cross-Consistency ===
-  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
-
-✅ All components in sync.
-verify-sync exit=0
-$ ruff check / ruff format --check (changed Python files)
-All checks passed!
-2 files already formatted
+exit=0
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index bac19653..562ef754 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -734,10 +734,49 @@ GOVERNED_TOOLS = (
     "RemoteTrigger",
     "SendMessage",
     "CronCreate",
+    "CronDelete",
     "ScheduleWakeup",
+    # The mcp__ branch of the design matcher: a registration without it misses these.
+    "mcp__x__merge_pull_request",
+    "mcp__x__push_files",
+    "mcp__x__create_or_update_file",
 )
 FIRE_ALWAYS = (None, "", "*")
 LINUX_FILES = ("/proc/self/stat", "/proc/sys/kernel/random/boot_id")
+PR_GET_CHILD_SUBREAPER = 37  # linux/prctl.h
+
+
+def process_interface_gaps() -> list[str]:
+    """The process interfaces of the job identity hook that this host lacks.
+
+    Read-only probes on the claim process itself: the /proc files, pidfd_open of
+    its own pid, and the query form of the child-subreaper call.
+    """
+    if not sys.platform.startswith("linux"):
+        return [f"sys.platform is {sys.platform}, not Linux"]
+    gaps = [p for p in LINUX_FILES if not os.path.exists(p)]
+    try:
+        import ctypes
+
+        libc = ctypes.CDLL(None, use_errno=True)
+    except OSError:
+        return gaps + ["pidfd_open", "prctl(PR_GET_CHILD_SUBREAPER)"]
+    try:
+        # libc, like the hook: some UV Python builds omit os.pidfd_open.
+        fd = libc.pidfd_open(os.getpid(), 0)
+        if fd < 0:
+            gaps.append("pidfd_open")
+        else:
+            os.close(fd)
+    except AttributeError:
+        gaps.append("pidfd_open")
+    try:
+        flag = ctypes.c_int()
+        if libc.prctl(PR_GET_CHILD_SUBREAPER, ctypes.byref(flag), 0, 0, 0) != 0:
+            gaps.append("prctl(PR_GET_CHILD_SUBREAPER)")
+    except AttributeError:
+        gaps.append("prctl(PR_GET_CHILD_SUBREAPER)")
+    return gaps
 
 
 def home_dir() -> Path:
@@ -798,12 +837,11 @@ def enforcement_preflight(wt: str) -> list[str]:
     for tool in ("jq", "uv"):
         if shutil.which(tool) is None:
             failures.append(f"{tool} is not on PATH (install {tool})")
-    if not sys.platform.startswith("linux") or not all(
-        os.path.exists(p) for p in LINUX_FILES
-    ):
+    gaps = process_interface_gaps()
+    if gaps:
         failures.append(
-            "this host is not Linux with "
-            + " and ".join(LINUX_FILES)
+            "this host lacks "
+            + ", ".join(gaps)
             + ", which the job identity hook needs (governed launches are Linux only)"
         )
     script = home / HOOK_SCRIPT
diff --git a/tests/skills/test_issue_orca_worktree.py b/tests/skills/test_issue_orca_worktree.py
index d17c6690..cdeffc78 100644
--- a/tests/skills/test_issue_orca_worktree.py
+++ b/tests/skills/test_issue_orca_worktree.py
@@ -1454,6 +1454,20 @@ IR4_CASES = {
         ),
         ["does not fire for Skill, Agent, Task", "ScheduleWakeup"],
     ),
+    # The design matcher minus its mcp__ branch: the plain tools fire, the
+    # GitHub write tools of an MCP server do not.
+    "matcher-without-mcp-branch": (
+        lambda f, wt: edit_settings(
+            user_settings(f),
+            set_matcher(
+                "PreToolUse",
+                GUARD,
+                "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow"
+                "|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$",
+            ),
+        ),
+        ["does not fire for mcp__x__merge_pull_request", "mcp__x__push_files"],
+    ),
     "user-prompt-matcher-cannot-fire": (
         lambda f, wt: edit_settings(
             user_settings(f), set_matcher("UserPromptSubmit", GUARD, "never")
@@ -1533,7 +1547,38 @@ def test_ir4_non_linux_host_is_refused(
     assert module.enforcement_preflight(str(wt)) == []
     monkeypatch.setattr(module.sys, "platform", "darwin")
     (reason,) = module.enforcement_preflight(str(wt))
-    assert "not Linux" in reason and "/proc/self/stat" in reason
+    assert "not Linux" in reason and "job identity hook needs" in reason
+
+    # The process interfaces the identity hook uses are probed on the claim
+    # process itself, read-only: pidfd_open and the child-subreaper query.
+    monkeypatch.undo()
+    for key, value in fake_orca.env().items():
+        monkeypatch.setenv(key, value)
+
+    import ctypes
+
+    class FakeLibc:
+        def __init__(self, pidfd: int, prctl: int) -> None:
+            self.pidfd, self.prctl_result = pidfd, prctl
+
+        def pidfd_open(self, pid: int, flags: int) -> int:
+            return self.pidfd
+
+        def prctl(self, *_args) -> int:
+            return self.prctl_result
+
+    real_cdll = ctypes.CDLL
+    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: FakeLibc(-1, 0))
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "lacks pidfd_open" in reason and "prctl" not in reason
+    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: FakeLibc(-1, -1))
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "pidfd_open, prctl(PR_GET_CHILD_SUBREAPER)" in reason
+    monkeypatch.setattr(ctypes, "CDLL", lambda *a, **k: object())  # no symbols
+    (reason,) = module.enforcement_preflight(str(wt))
+    assert "pidfd_open, prctl(PR_GET_CHILD_SUBREAPER)" in reason
+    monkeypatch.setattr(ctypes, "CDLL", real_cdll)
+    assert module.enforcement_preflight(str(wt)) == []
 
 
 def test_ir4_pipeline_none_never_reaches_the_preflight(

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T18.AC6 at=src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:724 anchor="the matcher of design section 13 (so it fires for the governed tools)" chk=y,y,n,n family=matcher-coverage fix=add mcp__ merge/push names and CronDelete to the governed-tool probe list so a registration without the design's mcp__ branch is refused covers="the matcher of design section 13 (so it fires for the governed tools)" first=A1 origin=new: a PreToolUse matcher equal to the design matcher minus its mcp__ branch was accepted although the guard governs mcp__ merge and push tools.
F2 sev=blocking trigger=B1 ac=scope at=src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:740 anchor="a Linux host with the process interfaces the adapter uses" chk=y,n,n,n family=runtime-prereq fix=add read-only probes for pidfd_open and the child-subreaper query covers="a Linux host with the process interfaces the adapter uses" first=A1 origin=new: the preflight tested only two /proc files, but design 19.7 names the pidfd and subreaper interfaces the adapter needs.

Saved-probe re-check hit locations (may be empty): 740:    "mcp__x__merge_pull_request",
741:    "mcp__x__push_files",
742:    "mcp__x__create_or_update_file",
749:def process_interface_gaps() -> list[str]:
766:        fd = libc.pidfd_open(os.getpid(), 0)


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
