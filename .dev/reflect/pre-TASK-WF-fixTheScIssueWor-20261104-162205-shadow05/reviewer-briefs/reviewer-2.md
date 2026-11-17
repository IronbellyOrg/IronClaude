# Reviewer brief 2 (persona: qa, model class: haiku, slot t4)

Audit target: UC-1 pre-execution coverage audit. Spec = source.md (one sentence). Tasklist = TASK-WF-fixTheScIssueWor-20261104-162205.md, archived package under .dev/tasks/done/. Repo: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel. You own the coverage/acceptance/verification surface.

## T1 card excerpt

(qa slice — coverage and evidence findings)

Union coverage matrix (two-pass extraction: Pass 1 regex found zero labeled IDs; Pass 2 inferred 3 rows, each quote-pinned to source.md:1): INF-001 (Rules rule) → Task 2, INF-002 (regression test) → Task 1, INF-003 (file scope) → Tasks 1-2. coverage_pct_union = 1.0, unmapped = []. coverage_pct (parsed-only) = null; coverage_degraded: parsed-sparse.

F3 (INFO, Grounded): Red-first evidence is real: t1-red.log tail shows 4 failed (3 worker tests + spawn-rule test), rc=1. Green evidence on file: t3-green.log, t3-verify-sync.log; progress.md FINAL: pass. SKILL.md at 193 lines (< 500 constraint).

F4 (INFO, Grounded): Spec→tasklist coverage is complete on the union set; no missing requirement.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:57Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### source.md:1-1 (SPEC BODY, whole file — D13 hunk)

```markdown
Fix the /sc:issue worker agents so they always write their files: add to each issue-worker-t*.md Rules section a rule that the files they write under .dev/issues/ are input files for the orchestrator's next tool calls (gh --body-file posts, /sc:recommend), not report files, so the general harness note against writing report .md files does not apply to them, and returning the content as text instead is a failure (E-WORKER-NO-OUTPUT). Add a regression test in tests/skills/test_issue_worker_agents.py that every issue-worker agent file carries that rule. Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py
```

### TASK-WF tasklist:38-54 (Phase 1 / Task 1: the regression tests + red-first AC)

```markdown
## Task 1: Add the tool-input rule tests to tests/skills/test_issue_worker_agents.py

Add to `tests/skills/test_issue_worker_agents.py`:

- module constants holding the exact early-section heading, the early-section paragraph, the Rules bullet and the SKILL.md line from the Constraints (byte-identical), plus a `SKILL` path constant for `src/superclaude/skills/sc-issue-protocol/SKILL.md`;
- a helper `tool_input_rule_problems(text)` that returns a list of problems for an agent file text: the heading missing, the heading not before `## Jobs for this tier`, the paragraph not appearing exactly once directly under that heading, any of the files `scout.md`, `accuracy-check.md`, `summary.md`, `analysis/`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md` missing from the paragraph, or the Rules bullet not appearing exactly once inside the `## Rules` section;
- a test parametrized over `sorted(WORKERS)` asserting `tool_input_rule_problems` returns `[]` for each agent file;
- a negative test parametrized over `sorted(WORKERS)` that writes a `tmp_path` copy of the agent file with the early section and the Rules bullet removed (the pre-fix text) and asserts the helper reports problems for it;
- a test asserting the "Workers and the spawn rule" section of SKILL.md (from its heading to the next `## ` heading) contains the SKILL.md line exactly once, and a negative test that a `tmp_path` copy of SKILL.md with that line removed fails the same check.

Before Tasks 2 and 3, run the new positive tests against the current, unedited files and save the output with its exit code to `./artifacts/t1-red.log`.

Acceptance criteria:
- The constants, the helper and the four new tests exist in `tests/skills/test_issue_worker_agents.py`; no existing test is changed.
- `./artifacts/t1-red.log` shows the agent positive test failing for all three agent files and the SKILL.md positive test failing, with a non-zero exit code recorded: proof the tests fail on the old text.
```

### TASK-WF artifacts/t1-red.log:90 (red-first evidence, tail)

```text
FAILED tests/skills/test_issue_worker_agents.py::test_spawn_rule_restates_tool_inputs - assert 0 == 1
======================= 4 failed, 39 deselected in 0.20s ========================
rc=1
```

### TASK-WF progress.md (implement ledger, whole)

```markdown
T1: complete verdict=compliant ac=T1.AC1,T1.AC2 evidence=T1.AC1@tests/skills/test_issue_worker_agents.py:253,T1.AC1@./artifacts/t1-diff.patch:5,T1.AC2@./artifacts/t1-red.log:90
T2: complete verdict=compliant ac=T2.AC1,T2.AC2 evidence=T2.AC1@src/superclaude/agents/issue-worker-t1.md:13,...,T2.AC2@./artifacts/t2-green.log:75
T3: complete verdict=compliant ac=T3.AC1,T3.AC2,T3.AC3 evidence=T3.AC1@src/superclaude/skills/sc-issue-protocol/SKILL.md:66,T3.AC2@./artifacts/t3-green.log:130,T3.AC3@./artifacts/t3-verify-sync.log:218
FINAL: pass evidence=src/superclaude/agents/issue-worker-t1.md:13,... state=8cd053528d4a9b29942417ed4f2b46d585863aab374fe71794648923fffe9112
```

### tests/skills/test_issue_worker_agents.py:298-321 (the implemented tests)

```python
@pytest.mark.parametrize("name", sorted(WORKERS))
def test_worker_states_its_files_are_tool_inputs(name):
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    assert tool_input_rule_problems(text) == []


@pytest.mark.parametrize("name", sorted(WORKERS))
def test_tool_input_check_fails_on_pre_fix_text(name, tmp_path):
    """Negative case: a temporary copy without the section and bullet fails."""
    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    block = f"{_TOOL_INPUT_HEADING}\n\n{_TOOL_INPUT_PARAGRAPH}\n\n"
    assert text.count(block) == 1
    ...


def test_spawn_rule_restates_tool_inputs():
    lines = spawn_rule_lines(SKILL.read_text(encoding="utf-8"))
    assert lines.count(_SPAWN_PROMPT_LINE) == 1
```

## Coverage slice

| Requirement row | Assigned | Match | Grounding |
|---|---|---|---|
| INF-001: Rules rule in each worker file | reviewer-1, reviewer-2 | containment | tasklist:58-62 |
| INF-002: regression test | reviewer-2 | containment | tasklist:38-50 |
| INF-003: file scope | reviewer-1 | containment | tasklist:42, tasklist:62 |
