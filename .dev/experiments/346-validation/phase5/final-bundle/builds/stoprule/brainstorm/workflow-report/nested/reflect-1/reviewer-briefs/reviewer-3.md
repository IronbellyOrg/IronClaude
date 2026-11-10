# Reviewer 3 brief (persona: refactorer)

Audit ONLY: the plan .dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md against its spec .dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md (UC-1, pre-execution). Read both files. Return findings as YAML: a list of {id, severity: blocking|minor, category: coverage|ordering|acceptance|scope|risk|deviation, claim, evidence: [file:line], recommendation}. A finding is blocking only if following the plan as written gives a wrong or missing deliverable. Read-only: no Bash, no edits.

## T1 card excerpt

#### Refactorer section (structure, size, reuse)

- R1: The script grows across Tasks 3 to 6 in one file `scripts/stoprule.py`; each task extends the same test file `tests/skills/test_stoprule_script.py`. Reasonable split for review, but every later task re-runs the whole test file, so a failing earlier case blocks later tasks.
- R2: Test conventions reuse `tests/skills/test_issue_repo_resolution.py` (importlib + subprocess) rather than inventing a harness: reuse, good.

- R1: The script grows across Tasks 3 to 6 in one file `scripts/stoprule.py`; each task extends the same test file `tests/skills/test_stoprule_script.py`. Reasonable split for review, but every later task re-runs the whole test file, so a failing earlier case blocks later tasks.
- R2: Test conventions reuse `tests/skills/test_issue_repo_resolution.py` (importlib + subprocess) rather than inventing a harness: reuse, good.
- R3: Agent frontmatter reuses the `confidence-calibrator` pattern (`src/superclaude/agents/confidence-calibrator.md:1-9`).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T18:22:46Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule projectPath=/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule

### src/superclaude/commands/spec-panel.md:256-264
```markdown
## Review Loop

1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review.
2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open).
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review.
5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking.
```

### tests/skills/test_worker_contract.py:831-839
```python
def _check_no_unattended_sections() -> None:
    have = sorted(
        p.stem
        for p in Path(_THIS.COMMANDS_DIR).glob("*.md")
        if re.search(r"^## Unattended mode\s*$", p.read_text(encoding="utf-8"), re.M)
    )
    assert set(have) == set(UNATTENDED_COMMANDS), (
        f"unexpected `## Unattended mode` sections: {have}"
    )
```

### tests/recommend/test_routing_refresh.py:646-648
```python
    assert (len(active), len(names - active)) == (43, 4)
    shipped = {p.stem for p in _COMMANDS.glob("*.md") if p.name != "README.md"}
    assert shipped - _POST_REFRESH_ADDITIONS == active
```

## Coverage slice

| Requirement | Tasks | Method | Ratio |
|---|---|---|---|
| INF-001 (104) | Task 9 | containment | 0.9 |
| INF-002 (104) | Task 9 | containment | 1.0 |
| INF-003 (105) | none | none | 0.571 |
| INF-004 (106) | Task 9 | containment | 0.692 |
| INF-005 (115) | Task 9 | containment | 0.667 |
| INF-006 (118) | Task 8 | containment | 0.931 |
| INF-007 (119) | Task 1 | containment | 0.833 |
| INF-008 (120) | Task 1 | containment | 0.75 |
| INF-011 (124) | Task 2 | containment | 0.929 |
| INF-012 (127) | Task 10 | containment | 0.833 |
| INF-015 (129) | Task 10 | containment | 1.0 |
| INF-016 (132) | Task 11 | containment | 0.8 |
| INF-017 (132) | Constraints | containment | 0.8 |
| INF-018 (132) | Task 12 | containment | 1.0 |
| INF-019 (135) | Constraints | containment | 1.0 |
| INF-020 (148) | Task 13 | containment | 1.0 |
| INF-021 (150) | Task 14 | containment | 0.9 |
| INF-022 (163) | Task 13 | containment | 0.81 |
| INF-023 (163) | Task 13 | containment | 0.6 |
| INF-024 (165) | Task 13 | containment | 0.8 |
