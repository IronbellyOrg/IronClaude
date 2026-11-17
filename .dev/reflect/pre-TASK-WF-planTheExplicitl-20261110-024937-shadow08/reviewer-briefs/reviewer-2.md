# Reviewer Brief 2 — persona: qa (model class: haiku, reviewer_id t4-1)

You are a Tier-2 reflection reviewer (UC-1, pre-execution coverage audit). Audit ONLY the evidence in this brief plus what you can Read/Grep from your grounding root (/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel). You are read-only: no edits, no writes, no shell execution. You own the acceptance-criteria and verification surface: are the ACs mechanically checkable, do the named tests actually pin the preserved wording, and are mirrors/verification steps complete?

## T1 card excerpt (verbatim from <output>/t1-card.md, qa slice)

- 4 inferred requirements; union coverage 4/4 mapped; unmapped union: [].
- Tasklist: 2 tasks. Task 1 AC1 qualitative ("clearly preserve..."), AC2 test-pass on tests/core/test_orca_session_launch_guidance.py. Task 2 updates hook script + plugins/ mirror + exact expected denial text in tests/hooks/test_require_orca_worktree_agent.py, adds focused assertions "where necessary", runs make sync-dev; AC runs three test files + make verify-sync, "or their actual failures are reported".
- T1 F1 (medium): Task 1's first AC has no grep-able form though tests/core/test_orca_session_launch_guidance.py:36 already asserts the banned phrase is absent and lines 24-35 assert each preserved phrase; the "three locations" vs "two files covered by the test" asymmetry means root CLAUDE.md:312 wording is AC-verified only by review, not by any test.
- T1 F2: hook scripts byte-identical today (sha256 79a22b... both sides); make sync-dev regenerates .claude/skills/ccsession-tag/README.md; verify-sync catches README drift.
- T1 F4 (low): Task 2's second AC pre-authorizes reporting failures instead of fixing them.

Calibrator-noted gaps you must adjudicate (from blind calibration, C=0.76):
- test lines 33-34 pin the person-opened and worker-ban phrases (card said 24-35, loose but covering).
- The negative-phrase assertion at line 36 sits inside the required loop (redundant but harmless).
- No test-gap finding for the hook-message text beyond a bare citation (hook script lines 352-356 unverified).
- F4 notes the weak pass gate but gives no concrete AC rewording.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:14:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### spec (whole body): .dev/tasks/done/TASK-WF-planTheExplicitl-20261110-024937/source.md:1

```text
Plan the explicitly requested narrow wording clarification for PR #449's phrase 'a coordinator under another orchestrator', preserving the existing worker-session fan-out ban and person-opened coordinator eligibility. Use .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md sections 7.4, 7.6 and 8. Address canonical guidance, hook message, required mirrors and affected tests only as necessary. This is a wording clarification, not implementation of a subordinate mode.
```

### plan Task 1 + Task 2 (verbatim): .dev/tasks/done/TASK-WF-planTheExplicitl-20261110-024937/TASK-WF-planTheExplicitl-20261110-024937.md:23-43 — read the tasklist file for the full text; both tasks' steps and ACs as quoted in the T1 card excerpt above.

### test: tests/core/test_orca_session_launch_guidance.py:10-36 (surface you own)

```python
ROOT = Path(__file__).resolve().parents[2] / "src" / "superclaude"
COPIES = ["core/CLAUDE.md", "skills/ccsession-tag/README.md"]
EXISTING_END = "commands' internal Agent-tool subagents.\n\n"
# per-copy guidance test asserts each required phrase, then:
        assert "coordinator under another orchestrator" not in section
        assert required in section, (relative, required)
```
Required phrases pinned include: "Every Orca worktree gets an agent", "never create a worktree for your own use", "owns its agent", "coordinator is person-opened", "authorize a supervised worker to create worktrees or dispatch workers".

### test: tests/hooks/test_require_orca_worktree_agent.py:35-36 (exact expected denial text)

```python
    "The eligible session that creates the worktree owns that agent.\n"
    "A supervised coordinator is person-opened; workers cannot create worktrees or dispatch workers.\n"
```

### source: hook denial message src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:352-356

```text
ORCA WORKTREE BLOCK: every Orca worktree gets an agent, and this command runs `orca worktree create` without `--agent`.
Use: orca worktree create --name <name> --agent claude --prompt "<task>"
[a 2-line explanation follows]
A supervised coordinator is person-opened; workers cannot create worktrees or dispatch workers.
Supervised workers use `orca orchestration worker-start`.
```
plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh is the byte-identical mirror (same sha256 today).

### source: root CLAUDE.md:312 (the untested third location)

```text
- **Every worktree gets an agent, and its creator owns it.** Because every worktree gets an agent, a bare `orca worktree create` is wrong: always pass `--agent claude --prompt "<task>"`, and never create a worktree for your own use. The eligible session that creates a worktree owns its agent(s). An Orca coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers. ...
```

## Coverage slice (rows you own)

| Requirement | Status per T1 card | Your question |
|-------------|--------------------|---------------|
| INF-003 guidance + hook message + mirrors + tests "only as necessary" | covered (tasklist:27,39,43) — calibrator: over-credited, hedged steps | For each of the four surfaces, is there an AC that mechanically fails if the step is skipped or botched? |
| Test-pin completeness (cross-cutting) | T1 F1: root CLAUDE.md untested; test covers only the two src copies | Would any wording regression in root CLAUDE.md or the hook message be caught by the named tests? |
| Verification honesty | T1 F4: "or their actual failures are reported" | Is a reported-failure escape hatch acceptable here, and what AC wording would make it airtight? |
