# Reviewer 1 brief (persona: analyzer)

Audit ONLY: the plan .dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md against its spec .dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md (UC-1, pre-execution). Read both files. Return findings as YAML: a list of {id, severity: blocking|minor, category: coverage|ordering|acceptance|scope|risk|deviation, claim, evidence: [file:line], recommendation}. A finding is blocking only if following the plan as written gives a wrong or missing deliverable. Read-only: no Bash, no edits.

## T1 card excerpt

#### Analyzer section (root cause, ordering, deviations from the spec)

- A1 [ordering defect]: Task 5 requires `finalize` to write a `label-count critical+major` line "built by the same function as Task 6's `count`" (plan Task 5 body), but Task 6 (Depends on: Task 5) is where `count` is defined. Task 5 cannot meet its own acceptance criterion ("the computed block's label-count line counts a CRITICAL-labelled `late-found` claim") without code Task 6 owns. Fix: define the counting function in Task 5 and have Task 6 only add the `count` subcommand around it.
- A2 [documented deviation, Necessary]: source.md section 3.4 line 129 says `tests/recommend/test_routing_refresh.py` is "Run, do not edit"; plan Task 10 edits `_POST_REFRESH_ADDITIONS`. Justified in the plan by `tests/recommend/test_routing_refresh.py:648` (`assert shipped - _POST_REFRESH_ADDITIONS == active`), which a new command file breaks; source.md itself marked the count effect UNVERIFIED.
- A3 [documented deviation, Authorized by owner]: source.md section 3.1 says the variant is a "Copy of `spec-panel.md`"; plan Task 9 removes `## Unattended mode` per the owner ruling recorded in Constraints. `tests/skills/test_worker_contract.py:831-839` pins the exact command set with that section.
- A4 [scope]: owner decision on deferred/demoted/withdrawn findings is implemented as reporting only (Tasks 3, 5, 6); the verdict function of source.md section 2.4 step 9 is unchanged.

#### QA section (coverage and acceptance)

- Q1: Pass 1 found no labelled requirement IDs in source.md (no R-/REQ-/SPEC-/T- tokens), so coverage is Pass-2 inferred only: 34 rows, 31 matched by the deterministic containment rule, coverage_pct_union 0.9118 (artifacts/coverage-matrix.json).
- Q2: The 3 rows the mechanical rule left unmatched are lexical misses that the plan does cover in other words: INF-003 "FR-10 stays" (Task 9 says "FR-10 stays"), INF-009 `--rubric` and `--cap` (Task 3 lists both options), INF-034 `audit-sample` k = 5 (Task 6 `--owner-k 5`). Reviewer should confirm by reading.
- Q3 [gap candidate]: source.md section 4 line 163 says the measurement copy of the command "is built from the exact Arm B base file (472 lines, sha256[:12] `c8d80346a96c`) plus the section 3.1 edits". Plan Task 13 only documents this in INSTALL.md; no task produces that measurement copy file. Whether this is a plan gap or coordinator work is not stated by the spec.
- Q4 [risk]: Task 7 depends on files in a sibling checkout `exp346-ab-ctl-r1` whose exact paths the plan does not pin (it says "Locate the exact files with a read-only listing"); the task has a blocked path if they are absent.
- Q5: Every task has an `Acceptance criteria:` block with runnable checks (pytest commands, grep counts, git diff checks).


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
| INF-009 (121) | none | none | 0.25 |
| INF-010 (121) | Task 3 | containment | 0.857 |
| INF-013 (128) | Task 7 | containment | 0.8 |
| INF-014 (128) | Task 5 | containment | 0.762 |
| INF-025 (62) | Task 3 | containment | 0.95 |
| INF-026 (64) | Task 3 | containment | 0.667 |
| INF-027 (65) | Task 4 | containment | 0.96 |
| INF-028 (67) | Task 4 | containment | 1.0 |
| INF-029 (68) | Task 4 | containment | 0.667 |
| INF-030 (70) | Task 5 | containment | 1.0 |
| INF-031 (74) | Task 5 | containment | 0.933 |
| INF-032 (75) | Task 14 | containment | 0.818 |
| INF-033 (76) | Task 6 | containment | 0.905 |
| INF-034 (180) | none | none | 0.333 |
