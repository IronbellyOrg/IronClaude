# Reviewer brief 1 — persona: analyzer (model pin: claude-sonnet-5-5, class sonnet)

You are a read-only Tier-2 reviewer (analyzer lens) auditing a workflow PLAN (UC-1 pre-execution
audit) against its driving spec. The package is archived (post-hoc vantage: the work already ran;
audit the PLAN TEXT as the object, using the package's own evidence logs as ground truth, and
discount "no before-state baseline" observations as audit vantage, not executor defect). Audit
only the material in this brief; you may Read/Grep inside the repository. Never execute commands,
never edit anything.

## T1 card excerpt

(analyzer slice: deviation/root-cause findings + rubric inputs)

mode: pre | spec: source.md (1 paragraph, 0 labeled IDs) | tasklist: 2 tasks, 2 phases
rubric_inputs: S_scope=2 (tasklist items) | S_domains=3 (core docs, skill README, cli code + tests) | S_dev_density_union=0.11 (1 partial of 9 inferred)

T1-F1 [MINOR, missing-requirement] INF-006's staging half has no AC.
Constraint bullet 3 ("Never stage generated .claude mirrors. Always stage .dev/tasks packages and
artifacts") is carried by no task acceptance criterion; only the sync half (make sync-dev +
verify-sync) is gated by Task 2 AC3. Recurring plan-defect class "constraints without matching AC
do not gate" (shadow04/06/08/10). Post-hoc evidence (progress.md ARCHIVE token, no commit) shows
the executor complied, so this is a plan-text gap, not an execution defect.

T1-F2 [MINOR, missing-requirement] INF-007 (no commit/push/PR/global install) likewise has no AC.
Same shape as T1-F1; process constraint ungated by any criterion.

T1-F4 [advisory, other] Root project CLAUDE.md carries a divergent third copy outside plan scope
(zero mechanical coverage, but the spec never asked for it).

Coverage verdict: parsed null (parsed-sparse); union 0.89 (8/9 covered, INF-006 partial).
Best-practice grade 4/5. Self-assessed 0.90.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 characters). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md:1 (SPEC, whole file)

```text
Fix issue #412's verified instruction-delivery gaps, not Orca shell behavior. Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance: new ccsession-backed Claude sessions use Claude (CLI), never New Terminal; programmatic creation uses the version-matched Orca agent launch or worktree create --agent, explicit terminal surface when CLI required. Reserve terminal create for shells. Preserve supervised worker-start/dispatch-preamble rules and internal Agent-tool subagents. Repair src/superclaude/cli/install_user_setup.py so install_user_setup(force=True) requests safe refresh even with existing Orca guides; ordinary nonforce setup still skips existing copies. Do not forward --force to Orca or overwrite edited guides; show meaningful skipped/warning output rather than claiming refresh succeeded. Add minimal regression checks in tests/cli/test_install_user_setup.py and tests/core/test_orca_session_launch_guidance.py with observed pre-fix failures, force propagation, default skip and nonfatal absent/failing Orca. Canonical edits only then make sync-dev and make verify-sync; never stage .claude mirrors, stage .dev/tasks. No commit/push/PR, global install or other repo edits. Issue412 already contains verified refresh-introducing PR245 and intentional Orca CLI-label PR29074, not shell-causation proof. Actual failing agent transcript and a historical New Terminal semantic-change PR remain unverified; preserve boundary. Current diagnosis independent validation returned partial with static findings verified; runtime cause UNDETERMINED. User explicitly authorizes execution after reading checked plan. Two-phase bounded plan, no verification-only task.
```

### src/superclaude/core/CLAUDE.md:45-53

```markdown
### Orca session launches

For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**.
Load the version-matched `orca-cli` guide before choosing commands. Use `agent launch`
in an existing worktree or `worktree create --agent` for a new checkout; request
`--surface terminal` when a CLI session is required. `terminal create` is for shells,
not agent sessions. The Claude command must be configured as `ccsession-orca` to use ccsession.
For supervised workers, keep `worker-start` and the dispatch preamble authoritative;
this rule does not replace supervised dispatch or commands' internal Agent-tool subagents.
```

### src/superclaude/skills/ccsession-tag/README.md:228-245

```markdown
### Orca session launches

For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**.
Load the version-matched `orca-cli` guide before choosing commands. Use `agent launch`
in an existing worktree or `worktree create --agent` for a new checkout; request
`--surface terminal` when a CLI session is required. `terminal create` is for shells,
not agent sessions. This requires the `ccsession-orca` Claude command configuration above;
choosing an agent does not configure ccsession automatically.
For supervised workers, keep `worker-start` and the dispatch preamble authoritative;
this rule does not replace supervised dispatch or commands' internal Agent-tool subagents.

Every Orca worktree gets an agent: create it with `worktree create --agent` (supervised workers
use `worker-start`, and a supervised worker follows its worker contract, which forbids it from
creating worktrees), and never create a worktree for your own use. The eligible session that
creates a worktree owns its agent(s). A supervised orchestrator's coordinator is person-opened;
ownership does not
authorize a supervised worker to create worktrees or dispatch workers. A hook blocks
`orca worktree create` without `--agent`.
```

### src/superclaude/cli/install_user_setup.py:279-312

```python
def install_orca_skills(
    home: Path | None = None, deadline: float | None = None, force: bool = False
) -> Tuple[bool, str]:
    """Request Orca's safe guide install/refresh; never force-replace edited guides."""
    home = Path.home() if home is None else Path(home)
    skills_dir = home / ".claude" / "skills"
    if not force and all(
        (skills_dir / name / "SKILL.md").exists() for name in _ORCA_SKILLS
    ):
        return True, "✅ Orca skills: already installed"
    orca = _find_orca()
    if orca is None:
        return True, "⏭️  Orca skills: Orca CLI not found; skipped"
    command = [orca, "skills", "install", "--agent", "claude-code"]
    for name in _ORCA_SKILLS:
        command += ["--skill", name]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=_orca_timeout(deadline),
            stdin=subprocess.DEVNULL,
        )
```

## Coverage slice

| Requirement (inferred) | Matched to | Status | Grounding |
|---|---|---|---|
| INF-001 explicit CLI-vs-New-Terminal rule in both surfaces | Task 1 AC1 | covered | core/CLAUDE.md:45-51; README:228-235 |
| INF-002 preserve worker-start/preamble + internal subagents | Task 1 AC2 | covered | core/CLAUDE.md:52-53; README:236-237 |
| INF-003 force=True requests safe refresh with existing guides; nonforce skips | Task 2 AC1 | covered | install_user_setup.py:285,505; test:313-370 |
