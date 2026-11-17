# Reviewer brief 3 — persona: refactorer (model pin: claude-opus-5-5, class opus)

You are a read-only Tier-2 reviewer (refactorer lens: structure, duplication, drift between copies)
auditing a workflow PLAN (UC-1 pre-execution audit) against its driving spec. The package is
archived (post-hoc vantage: audit the PLAN TEXT as the object, using the package's own evidence
logs as ground truth; discount "no before-state baseline" observations as audit vantage, not
executor defect). Audit only the material in this brief; you may Read/Grep inside the repository.
Never execute commands, never edit anything.

## T1 card excerpt

(refactorer slice: structure + copy-drift findings)

vantage: post-hoc — package already archived under .dev/tasks/done/; ACs verified against
package-internal evidence (t1/t2-tests.log, sync.log, final-review.md)

T1-F4 [advisory, other] Guidance-test coverage is exactly the spec's two named surfaces; the root
project CLAUDE.md carries a divergent third copy outside plan scope.
tests/core/test_orca_session_launch_guidance.py COPIES = core/CLAUDE.md + ccsession README, which
is exactly what the spec names. Root CLAUDE.md:307+ carries its own worktree-agent rule with
divergent wording ("An Orca coordinator is person-opened" vs core's "A supervised orchestrator's
coordinator is person-opened") and zero mechanical coverage here — but the spec never asked for it.

Structure notes: two-phase bounded plan; Task 2 depends on Task 1; both instruction surfaces
(core/CLAUDE.md:45-53 and README:228-245) carry the same section heading and near-identical body,
pinned identical by test_appended_paragraph_is_identical_in_both_copies. Best-practice grade 4/5.
Calibrated confidence 0.80.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 characters). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md:1 (SPEC, whole file)

```text
Fix issue #412's verified instruction-delivery gaps, not Orca shell behavior. Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance: new ccsession-backed Claude sessions use Claude (CLI), never New Terminal; programmatic creation uses the version-matched Orca agent launch or worktree create --agent, explicit terminal surface when CLI required. Reserve terminal create for shells. Preserve supervised worker-start/dispatch-preamble rules and internal Agent-tool subagents. Repair src/superclaude/cli/install_user_setup.py so install_user_setup(force=True) requests safe refresh even with existing Orca guides; ordinary nonforce setup still skips existing copies. Do not forward --force to Orca or overwrite edited guides; show meaningful skipped/warning output rather than claiming refresh succeeded. Add minimal regression checks in tests/cli/test_install_user_setup.py and tests/core/test_orca_session_launch_guidance.py with observed pre-fix failures, force propagation, default skip and nonfatal absent/failing Orca. Canonical edits only then make sync-dev and make verify-sync; never stage .claude mirrors, stage .dev/tasks. No commit/push/PR, global install or other repo edits. Issue412 already contains verified refresh-introducing PR245 and intentional Orca CLI-label PR29074, not shell-causation proof. Actual failing agent transcript and a historical New Terminal semantic-change PR remain unverified; preserve boundary. Current diagnosis independent validation returned partial with static findings verified; runtime cause UNDETERMINED. User explicitly authorizes execution after reading checked plan. Two-phase bounded plan, no verification-only task.
```

### src/superclaude/core/CLAUDE.md:45-63 (guidance copy A)

```markdown
### Orca session launches

For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**.
Load the version-matched `orca-cli` guide before choosing commands. Use `agent launch`
in an existing worktree or `worktree create --agent` for a new checkout; request
`--surface terminal` when a CLI session is required. `terminal create` is for shells,
not agent sessions. The Claude command must be configured as `ccsession-orca` to use ccsession.
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

### src/superclaude/skills/ccsession-tag/README.md:228-245 (guidance copy B)

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

### CLAUDE.md:307-312 (root project copy, divergent, OUTSIDE plan scope)

```markdown
**ABSOLUTE RULE — every project worktree is created through Orca and lives at Orca's default worktree location.**
Create it with `orca worktree create --name <name> --agent claude --prompt "<task>"`, adding `--repo <selector>`,
`--base-branch <ref>`, and `--parent-worktree <selector>` or `--no-parent` as needed. Orca places it at its default
worktree location, outside the main checkout; `orca worktree current --json` (from inside it) and `orca worktree list` show the real path.

- **Every worktree gets an agent, and its creator owns it.** ... An Orca coordinator is person-opened;
ownership does not authorize a supervised worker to create worktrees or dispatch workers. ...
```

### src/superclaude/cli/install_user_setup.py:279-294 + 313-327 (the repaired helper)

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
    ...
    installed = [n for n in _ORCA_SKILLS if (skills_dir / n / "SKILL.md").exists()]
    if result.returncode != 0 or len(installed) != len(_ORCA_SKILLS):
        message = (
            f"⚠️  Orca skills: install request failed or incomplete "
            f"({len(installed)}/{len(_ORCA_SKILLS)} files present); "
            f"rerun `{orca} skills install`"
        )
    else:
        message = (
            "✅ Orca skills: install request completed (see Orca output for any skips)"
        )
    details = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    return True, "\n".join(part for part in (message, details) if part)
```

### src/superclaude/cli/install_user_setup.py:498-508 (the caller propagation)

```python
def install_user_setup(force: bool = False) -> Tuple[bool, str]:
    """Run every user-setup step; returns combined success and messages."""
    deadline = time.monotonic() + _NETWORK_BUDGET
    results = [
        install_rules(force=force),
        install_output_styles(force=force),
        apply_settings_defaults(),
        install_orca_skills(deadline=deadline, force=force),
        install_plugins(deadline=deadline),
    ]
    return all(ok for ok, _ in results), "\n".join(msg for _, msg in results)
```

### tests/core/test_orca_session_launch_guidance.py:40-62 (copy-identity pin)

```python
def _appended_paragraph(relative: str) -> str:
    text = (ROOT / relative).read_text()
    start = text.index("### Orca session launches")
    after = text[start:].split(EXISTING_END, 1)[1]
    return after.split("\n\n", 1)[0]

@pytest.mark.parametrize("relative", COPIES)
def test_appended_paragraph_names_the_owner_roles_and_no_source_path(
    relative: str,
) -> None:
    paragraph = _appended_paragraph(relative)
    assert paragraph.startswith("Every Orca worktree gets an agent")
    assert "orchestrator" in paragraph and "coordinator" in paragraph
    assert "A hook blocks `orca worktree create` without `--agent`" in " ".join(
        paragraph.split()
    )
    assert "src/superclaude/" not in paragraph

def test_appended_paragraph_is_identical_in_both_copies() -> None:
    first, second = (_appended_paragraph(relative) for relative in COPIES)
    assert first == second
```

## Coverage slice

| Requirement (inferred) | Matched to | Status | Grounding |
|---|---|---|---|
| INF-001 explicit CLI rule in core/CLAUDE.md + README (both copies) | Task 1 AC1 | covered | core/CLAUDE.md:45-51; README:228-235 |
| INF-002 preserve worker-start/preamble + internal subagents | Task 1 AC2 | covered | both copies lines 52-53/236-237; test pins |
| INF-009 two-phase bounded plan | Plan structure | covered | tasklist:26,39,43 |
