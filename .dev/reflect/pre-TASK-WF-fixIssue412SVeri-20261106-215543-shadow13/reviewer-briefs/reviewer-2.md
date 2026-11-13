# Reviewer brief 2 — persona: qa (model pin: claude-haiku-5-5, class haiku)

You are a read-only Tier-2 reviewer (qa lens: coverage, acceptance criteria, verification honesty)
auditing a workflow PLAN (UC-1 pre-execution audit) against its driving spec. The package is
archived (post-hoc vantage: audit the PLAN TEXT as the object, using the package's own evidence
logs as ground truth; discount "no before-state baseline" observations as audit vantage, not
executor defect). Audit only the material in this brief; you may Read/Grep inside the repository.
Never execute commands, never edit anything.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any
requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## T1 card excerpt

(qa slice: coverage verdict + AC evidence findings)

Coverage verdict: parsed coverage null (0 Pass-1 IDs; parsed-sparse). Union coverage 0.89 (8/9
inferred rows covered; INF-006 partial: the staging-discipline half of "canonical edits only then
make sync-dev and make verify-sync; never stage .claude mirrors, stage .dev/tasks" rides ungated
in Constraints bullet 3 with no AC; INF-007 (no commit/push/PR) likewise ungated).

T1-F1 [MINOR, missing-requirement] INF-006's staging half has no AC. Task 2 AC3 gates only the
sync half (make sync-dev + make verify-sync). Recurring class "constraints without matching AC do
not gate" (shadow04/06/08/10).

T1-F2 [MINOR, missing-requirement] INF-007 (no commit/push/PR/global install) has no AC. Post-hoc:
progress.md shows no commit token.

T1-F3 [MINOR, other] Post-hoc vantage: red/green evidence is package-internal (t1-tests.log 2
failed pre-edit; t2-tests.log 9 failed pre-fix, 157 passed after); the pre-fix tree no longer
exists at HEAD, so re-running the plan's checks today passes vacuously.

INF-005 evidence: red observed before both edits, green after; default-skip covered by
test_orca_skills tests; nonfatal absent/timeout covered by tests 373-392.

Best-practice grade 4/5. Calibrated confidence 0.80.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 characters). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md:1 (SPEC BODY, whole file)

```text
Fix issue #412's verified instruction-delivery gaps, not Orca shell behavior. Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance: new ccsession-backed Claude sessions use Claude (CLI), never New Terminal; programmatic creation uses the version-matched Orca agent launch or worktree create --agent, explicit terminal surface when CLI required. Reserve terminal create for shells. Preserve supervised worker-start/dispatch-preamble rules and internal Agent-tool subagents. Repair src/superclaude/cli/install_user_setup.py so install_user_setup(force=True) requests safe refresh even with existing Orca guides; ordinary nonforce setup still skips existing copies. Do not forward --force to Orca or overwrite edited guides; show meaningful skipped/warning output rather than claiming refresh succeeded. Add minimal regression checks in tests/cli/test_install_user_setup.py and tests/core/test_orca_session_launch_guidance.py with observed pre-fix failures, force propagation, default skip and nonfatal absent/failing Orca. Canonical edits only then make sync-dev and make verify-sync; never stage .claude mirrors, stage .dev/tasks. No commit/push/PR, global install or other repo edits. Issue412 already contains verified refresh-introducing PR245 and intentional Orca CLI-label PR29074, not shell-causation proof. Actual failing agent transcript and a historical New Terminal semantic-change PR remain unverified; preserve boundary. Current diagnosis independent validation returned partial with static findings verified; runtime cause UNDETERMINED. User explicitly authorizes execution after reading checked plan. Two-phase bounded plan, no verification-only task.
```

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md:17-24 (Constraints)

```markdown
## Constraints

- Fix only issue #412. Its existing issue body already references verified IronClaude refresh-introducing PR #245 and intentional Orca CLI-label PR #29074. Do not create another issue or claim that the label PR changed shell startup. Runtime incident causation remains UNDETERMINED; diagnostic closure remains advisory.
- No commit, push, PR, global install or other-repository mutation. Orca source/history stays read-only. No new dependency or launch wrapper.
- Canonical edits are under src/superclaude and tests. Run make sync-dev and make verify-sync after changes. Never stage generated .claude mirrors. Always stage .dev/tasks packages and artifacts.
- Supervised workers keep the dispatch preamble and worker-start authority. Internal Agent-tool subagents remain internal. Ordinary agent launch is not a substitute for supervised worker dispatch.
- IronClaude force means request Orca's normal safe installation. Never pass Orca --force, replace edited guides, change Claude executable settings or make plain shell terminals start an agent.
- Installed Orca help defines update behavior; existing owned unmodified copies may update, edited or foreign copies may be skipped. Meaningful installer output must remain visible. Do not treat a safe skip as proof that the guide refreshed.
```

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md:26-52 (Phases + ACs)

```markdown
## Phase 1: Explicit session selection

## Task 1: Add canonical launch instructions and a regression check

Inputs: the explicit launch requirement in source.md, src/superclaude/core/CLAUDE.md, src/superclaude/skills/ccsession-tag/README.md, and the current installed orca-cli guide. Add a concise global selection rule and matching launcher README passage. Add tests/core/test_orca_session_launch_guidance.py using existing pytest static-document conventions. Test the absence before editing the two instruction files, then apply the instructions. Preserve Settings > Agents > Claude > Command configuration of ccsession-orca and distinguish a Claude CLI agent from an ordinary shell.

Outputs: the two canonical instruction files and runnable guidance checks; save observed failing/passing output under ./artifacts/t1-tests.log. No runtime Orca change is authorized.

Acceptance criteria:
- Both instruction surfaces explicitly distinguish Claude (CLI) for ccsession-backed Claude sessions from New Terminal and terminal create for shells, and identify agent launch and worktree create --agent as programmatic agent creation routes after loading the version-matched Orca guide. Explicit terminal surface is named only when a CLI session is required.
- Both surfaces preserve supervised worker-start/preamble authority and internal Agent-tool subagents. README retains the ccsession-orca executable configuration prerequisite rather than claiming every agent launch automatically uses ccsession.
- The new guidance tests are observed failing against the original instruction files and passing after the bounded edit. They check the shell/CLI distinction and supervised/internal-agent boundaries, not UI runtime success. Evidence records that scope honestly.

## Phase 2: Safe guide refresh

## Task 2: Propagate forced setup refresh with regression checks

Depends on: Task 1

Inputs: source.md's safe-refresh requirement, src/superclaude/cli/install_user_setup.py helper and caller, tests/cli/test_install_user_setup.py, and installed orca-ide skills install --help. Add a backward-compatible force argument to install_orca_skills and pass the enclosing install_user_setup force intent. Existing files may short-circuit only when force is false. A forced request uses the normal safe Orca install command, without external --force. Preserve the current executable identification, deadline, absent/failed-Orca nonfatal behavior and three-skill list. Relay meaningful Orca stdout/stderr so edited/foreign guide skips cannot be hidden by an unconditional success summary; reuse existing result fields without a new parser. Add minimal tests for helper refresh, top-level propagation, safe default skip, surfaced skip/failure output and nonfatal absence/failure with existing guides.

Outputs: the canonical helper/caller and matching tests; observed red/green and wider regression output under ./artifacts/t2-tests.log. Run synchronization and record its output in ./artifacts/sync.log as part of delivering the changed skill README, without staging mirrors.

Acceptance criteria:
- A forced user-setup request reaches normal Orca guide installation even with all three files present, and top-level force propagation is covered. Nonforce repeated setup still skips existing guides with no Orca calls. The external command never gains --force and existing edited-guide contents are not rewritten by IronClaude.
- Absent Orca, timeout, nonzero installation result or incomplete installation remains nonfatal and accurately reported. Meaningful skipped/warning output from Orca is surfaced, including when files already exist; tests cover those cases without network or global writes.
- New refresh regression checks fail before the implementation and pass afterwards. The related installer tests, tests/unit/test_cli_install.py, guidance tests and tests/core/test_claude_md_routing_block.py pass. Ruff on changed Python files and make sync-dev plus make verify-sync succeed. Logs distinguish mocked installer checks from actual Orca dry-run evidence; no live guide refresh or UI reproduction is claimed.
```

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/artifacts/t1-tests.log:1-13 (observed red/green, Task 1)

```text
Observed tool-output excerpts, not a UI reproduction.

Before instruction edits:
$ uv run pytest tests/core/test_orca_session_launch_guidance.py -q
exit 1; collected 2 items; 2 failed in 0.16s.
Both source surfaces raised ValueError: substring not found at text.index("### Orca session launches").

After instruction edits:
$ uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/core/test_codegraph_guide.py -q
exit 0; collected 23 items; 23 passed in 0.33s.
New static checks: 2 passed. Existing routing/guide checks: 21 passed.

These tests pin the installed wording, shell versus CLI distinction, configured ccsession-orca prerequisite and supervised/internal-agent boundaries. They do not prove historical incident causation or all Orca UI routes.
```

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/artifacts/t2-tests.log:60-88 (observed red/green, Task 2)

```text
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_preserves_edits_and_reports_output[0-Skipped edited guide--True]
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_preserves_edits_and_reports_output[0--Skipped foreign guide-True]
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_preserves_edits_and_reports_output[0---True]
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_preserves_edits_and_reports_output[1-partial output-installation failed-True]
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_preserves_edits_and_reports_output[0---False]
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_absent_or_timeout_is_nonfatal[False]
FAILED tests/cli/test_install_user_setup.py::test_orca_forced_refresh_absent_or_timeout_is_nonfatal[True]
FAILED tests/cli/test_install_user_setup.py::test_user_setup_passes_force_to_orca_without_skipping_plugins[False]
FAILED tests/cli/test_install_user_setup.py::test_user_setup_passes_force_to_orca_without_skipping_plugins[True]
======================= 9 failed, 29 deselected in 0.47s =======================
...
============================= 157 passed in 0.83s ==============================
```

### tests/core/test_orca_session_launch_guidance.py:7-37 (the AC3 checker)

```python
ROOT = Path(__file__).resolve().parents[2] / "src" / "superclaude"
COPIES = ["core/CLAUDE.md", "skills/ccsession-tag/README.md"]
EXISTING_END = "commands' internal Agent-tool subagents.\n\n"

@pytest.mark.parametrize("relative", COPIES)
def test_orca_session_launch_guidance(relative: str) -> None:
    text = (ROOT / relative).read_text()
    start = text.index("### Orca session launches")
    section = text[start:].split("\n## ", 1)[0]
    for required in (
        "Claude (CLI)",
        "never **New Terminal**",
        "`terminal create` is for shells",
        "version-matched `orca-cli` guide",
        "`agent launch`",
        "`worktree create --agent`",
        "`--surface terminal`",
        "ccsession-orca",
        "supervised workers",
        "`worker-start`",
        "dispatch preamble",
        "internal Agent-tool subagents",
        "Every Orca worktree gets an agent",
        "never create a worktree for your own use",
        "owns its agent",
        "coordinator is person-opened",
        "authorize a supervised worker to create worktrees or dispatch workers",
    ):
        assert "coordinator under another orchestrator" not in section
        assert required in section, (relative, required)
```

### tests/cli/test_install_user_setup.py:313-392 (forced-refresh checks)

```python
@pytest.mark.parametrize(
    "returncode,stdout,stderr,present",
    [
        (0, "Skipped edited guide", "", True),
        (0, "", "Skipped foreign guide", True),
        (0, "", "", True),
        (1, "partial output", "installation failed", True),
        (0, "", "", False),
    ],
)
def test_orca_forced_refresh_preserves_edits_and_reports_output(
    tmp_path: Path, monkeypatch, returncode: int, stdout: str, stderr: str, present: bool,
) -> None:
    paths = [
        tmp_path / ".claude/skills" / name / "SKILL.md" for name in setup._ORCA_SKILLS
    ]
    if present:
        for path in paths:
            path.parent.mkdir(parents=True)
            path.write_text("user edited")
    calls = []
    monkeypatch.setattr(setup, "_find_orca", lambda: "/bin/orca-ide")

    def fake_run(command, **kwargs):
        calls.append(command)
        assert kwargs["stdin"] == subprocess.DEVNULL
        assert 0 < kwargs["timeout"] <= setup._ORCA_TIMEOUT
        return subprocess.CompletedProcess(command, returncode, stdout, stderr)

    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    ok, message = setup.install_orca_skills(tmp_path, None, force=True)
    assert ok
    assert len(calls) == 1
    assert calls[0][:5] == ["/bin/orca-ide", "skills", "install", "--agent", "claude-code"]
    assert calls[0].count("--skill") == 3
    assert "--force" not in calls[0]
    assert "already installed" not in message
    assert "refreshed" not in message.lower()
    for output in (stdout, stderr):
        if output:
            assert output in message
    if returncode or not present:
        assert message.startswith("⚠️  Orca skills")
    if present:
        assert all(path.read_text() == "user edited" for path in paths)
    else:
        assert not any(path.exists() for path in paths)

@pytest.mark.parametrize("available", [False, True])
def test_orca_forced_refresh_absent_or_timeout_is_nonfatal(
    tmp_path: Path, monkeypatch, available: bool
) -> None:
    for name in setup._ORCA_SKILLS:
        path = tmp_path / ".claude/skills" / name / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("existing")
    monkeypatch.setattr(
        setup, "_find_orca", lambda: "/bin/orca-ide" if available else None
    )
    def fail_run(command, **_kwargs):
        raise subprocess.TimeoutExpired(command, setup._ORCA_TIMEOUT)
    monkeypatch.setattr(setup.subprocess, "run", fail_run)
    ok, message = setup.install_orca_skills(home=tmp_path, force=True)
    assert ok
    assert "already installed" not in message
    assert ("not installed" if available else "not found") in message
```

## Coverage slice

| Requirement (inferred) | Matched to | Status | Grounding |
|---|---|---|---|
| INF-004 no --force forwarded, no overwrite, output relayed, no false success | Task 2 AC1 + AC2 | covered | install_user_setup.py:292-294,313-327; test:339-368 |
| INF-005 regression checks: observed pre-fix failures, propagation, default skip, nonfatal | Task 1 AC3 + Task 2 AC3 | covered | t1-tests.log:3-13; t2-tests.log:60-88; test:373-392 |
| INF-006 canonical edits + sync-dev + verify-sync + staging discipline | Task 2 AC3 (sync half only) | partial | sync.log tail; staging half ungated |
| INF-007 no commit/push/PR/global install | Constraints bullet 2 (no AC) | partial | progress.md (no commit token) |
| INF-008 evidence-boundary honesty (no shell-causation claim) | Task 1 AC3 + Constraints bullet 1 | covered | t1-tests.log:13; final-review.md T1.AC1 |
