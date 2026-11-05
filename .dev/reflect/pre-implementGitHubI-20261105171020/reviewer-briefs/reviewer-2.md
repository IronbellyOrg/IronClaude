## T1 card excerpt

Persona: qa (coverage, acceptance and testability lens). Your model class: haiku. You are reviewing a PLAN before anyone builds it (pre-execution). Audit only what this brief supplies plus what you can Read, Grep and Glob. Run no commands and edit nothing.

What is under review
- Spec (the user's decision, one line, reproduced in the grounding hunks): .dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/source.md
- Plan (9 tasks, 4 phases): .dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/TASK-WF-implementGitHubI-20261105-170815.md

Tier 1 coverage matrix (verbatim from t1-card.md). Parsed requirements: 0. Inferred rows are quote-pinned to source.md:1. Deterministic matching ran over the Task sections only.

| Row | Quote | Best task | Ratio | Result |
|---|---|---|---|---|
| INF-001 | a new explicit opt-in environment variable CCSESSION_PERMISSIONS=default | Task 1 | 0.6667 | containment |
| INF-002 | When set, ccsession adds no permission-bypass flag (no --dangerously-skip-permissions) on all six launch lines while keeping shim and tier-model routing | Task 1 | 0.6923 | containment |
| INF-003 | when unset, behavior is unchanged for everyone | Task 9 | 0.75 | containment |
| INF-004 | Do NOT change how an empty CC_CLAUDE_FLAGS is handled (the :- default stays) | none | 0.5714 | none |
| INF-005 | Tests must fail on the old code: set -> no bypass flag and shim/model routing kept; unset -> unchanged | Task 1 | 1.0 | containment |
| INF-006 | Document the variable where ccsession's other variables are documented | Task 7 | 1.0 | containment |
| INF-007 | Unblocks Coder PR 458 | none | 0.25 | none |

Numbers: coverage_pct_union = 0.7143; unmapped_requirements_union = [INF-004, INF-007]. The plan carries INF-007 as a Constraints delivery note (a pull-request description item), and INF-004 in the second Constraints bullet and Tasks 1 and 4.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

Your job: find defects in the PLAN's acceptance criteria and test design. Look for: an acceptance criterion that cannot be observed or would pass for the wrong reason; a test the plan describes that would pass on the old launcher (so it does not prove the change); a missing case (every one of the six launch lines, the opt-in with a profile, the opt-in through ccsession-orca print mode, tier mode, unset, empty variable, bad value); a doc or changelog claim that the tests in Tasks 1 to 3 do not back; a requirement of the spec that no task delivers. Assume mistakes exist.

Classify every divergence between the plan and the spec using: Authorized expansion, Necessary deviation, Drift, Regression (a plan step that contradicts the spec or an existing guarantee). Report only what you can ground with a `file:line`.

Return, as your final message, a YAML document with: `verdict` (PASS or FAIL for "plan is safe to approve as written"), `self_confidence` (0.0 to 1.0), and `findings`, a list of items each with `id`, `claim`, `evidence` (file:line list), `class`, `severity` (blocking or minor), `plan_ref` (Task N or Constraints), `recommended_change`. Add `not_checked` listing what you could not verify.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T17:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/ic-issue-390 projectPath=/home/coder/workspaces/worktrees/IronClaude/ic-issue-390

### .dev/tasks/to-do/TASK-WF-implementGitHubI-20261105-170815/source.md:1-1

```text
Implement GitHub issue 390 as described in .dev/issues/390/issue-summary.md. Chosen design (decided by the user): option B, a new explicit opt-in environment variable CCSESSION_PERMISSIONS=default. When set, ccsession adds no permission-bypass flag (no --dangerously-skip-permissions) on all six launch lines while keeping shim and tier-model routing; when unset, behavior is unchanged for everyone. Do NOT change how an empty CC_CLAUDE_FLAGS is handled (the :- default stays). Tests must fail on the old code: set -> no bypass flag and shim/model routing kept; unset -> unchanged. Document the variable where ccsession's other variables are documented. Unblocks Coder PR 458.
```

### tests/unit/test_ccsession_tag.py:1251-1256

```python
    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
    stdout, _ = _label_launch(tmp_path, transcript=transcript, args=args)
    launched = json.loads(stdout.strip().splitlines()[-1])
    assert launched[:2] == ["--dangerously-skip-permissions", "--allowedTools=Grep"]
    assert ("--model" in launched) == ("--profile" in args)
    assert ("--resume" in launched) == transcript
```

### tests/unit/test_ccsession_tag.py:1470-1489

```python
def _orca_no_tty(tmp_path: Path, *args: str, **extra: str) -> tuple[str, dict]:
    result = subprocess.run(
        [str(ORCA), *args],
        env=_orca_env(tmp_path, **extra),
        cwd=tmp_path / "work",
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=60,
        check=True,
    )
    return result.stdout + result.stderr, json.loads(
        (tmp_path / "record.json").read_text()
    )


def _assert_through_shim(record: dict) -> None:
    assert record["base_url"] == "http://127.0.0.1:4555"
    # One credential reaches Claude Code, never both.
    assert record["set"] == {"ANTHROPIC_API_KEY": False, "ANTHROPIC_AUTH_TOKEN": True}
```

### tests/unit/test_ccsession_tiers.py:301-319

```python
def _launch(
    tmp_path: Path, *args: str, defaults: str | None = TIER_BLOCK, **extra: str
):
    """Run ccsession with a fake claude and a fake running shim; return (rc, out, err, seen)."""
    env = _launch_env(tmp_path, defaults, **extra)
    proc = subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    seen = (
        json.loads((tmp_path / "seen.json").read_text())
        if (tmp_path / "seen.json").exists()
        else None
    )
    return proc.returncode, proc.stdout, proc.stderr, seen
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 variable defined | Task 4 | covered | plan Task 4 |
| INF-002 all six launch lines, shim and tier routing kept | Tasks 1, 2, 3, 4 | covered | plan Tasks 1 to 3 acceptance |
| INF-003 unset unchanged | Tasks 1 to 3 | covered | tests/unit/test_ccsession_tag.py:1251-1256 |
| INF-004 empty CC_CLAUDE_FLAGS unchanged | Task 1, Task 4 | matcher: none; judgment: covered | plan Constraints bullet 2 |
| INF-005 tests fail on old code | Tasks 1 to 3 | covered | red logs under ./artifacts/ |
| INF-006 documentation | Tasks 5 to 8 | covered | README table |
| INF-007 PR description | Constraints delivery note | matcher: none | plan Constraints |
