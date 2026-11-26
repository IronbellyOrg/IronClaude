# Reviewer 1 brief (persona: analyzer; model class: opus; mode: pre)

Audit the plan at `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md` against the spec at `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/source.md`. Read-only. The plan is a proposal that has not been run.

## T1 card excerpt

```yaml
findings:
  - id: F1
    class: gap
    blocking: true
    claim: >-
      The plan never edits tests/skills/test_worker_contract.py, but Task 1 adds a new line to
      src/superclaude/skills/sc-issue-protocol/refs/claim.md that contains `gh api`. That test file scans every
      line under src/superclaude/skills, commands and agents for the pattern `gh pr` or `gh api` and fails
      `test_every_write_verb_hit_is_classified` for any line that has no entry in its WRITE_VERB_CLASSIFICATION
      table (keyed by path, verb and the exact stripped line). So after Task 1 that test fails, and Task 6's own
      acceptance criterion (the other readers still pass, including tests/skills/test_worker_contract.py) cannot be
      met without an edit that no task owns.
    evidence:
      - "tests/skills/test_worker_contract.py:1886-1890 (AUDIT_ROOTS = src/superclaude/skills, commands, agents)"
      - "tests/skills/test_worker_contract.py:1894-1897 (WRITE_VERB_RE matches `gh pr` and `gh api`)"
      - "tests/skills/test_worker_contract.py:1951-1958 (_check_all_classified fails on any unclassified hit)"
      - "tests/skills/test_worker_contract.py:3167-3168 (test_every_write_verb_hit_is_classified)"
      - "tests/skills/test_worker_contract.py:2953-2960 (an existing read-only entry for the claim.md line `runs gh issue view ... and gh api user`)"
      - "plan line 30 (Task 1 introduces the `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by` line)"
      - "plan line 91 (Task 6 acceptance names tests/skills/test_worker_contract.py as a reader that must still pass)"
    recommendation: >-
      Add to Task 6 (or a new task after Task 1) the edit of tests/skills/test_worker_contract.py: one new
      WRITE_VERB_CLASSIFICATION entry for the new claim.md line, category `read-only`, one-line reason that it is a
      GET of the issue's blocked-by list. Keep `gh api` out of the SKILL.md, command and guide wording so no other
      line needs an entry.
  - id: F2
    class: note
    blocking: false
    claim: >-
      The sources of the five inferred requirements (INF-001 to INF-005) all sit on one line of source.md, and the
      requirements about updating the protocol, command description, guide and tests come from the issue summary the
      source names (.dev/issues/848/issue-summary.md), not from source.md itself. The plan covers them (Tasks 2 to 6),
      so coverage is not a gap, but the coverage matrix proves only the five source.md rows.
    evidence:
      - "source.md:1"
      - "plan lines 39, 52, 62, 70, 82 (Tasks 2 to 6 headings)"
  - id: F3
    class: note
    blocking: false
    claim: >-
      Task 1 renumbers item 5 of Wave 2 to 6. A search of tests/ for the old item text ("Earlier claim or accuracy",
      "Already assigned to the current login") found no test that pins it, so the renumbering is low risk.
    evidence:
      - "src/superclaude/skills/sc-issue-protocol/refs/claim.md:36-44 (Wave 2 items 1 to 5)"
risk_register:
  - "A new `gh api` line without a classification entry fails test_worker_contract.py (F1)."
  - "Wave 2 now carries a network read before the first write; a blocker read failure is a continue, not a stop, per the source."
recommendations:
  - {id: R1, file: tests/skills/test_worker_contract.py, change: "add one read-only WRITE_VERB_CLASSIFICATION entry for the new claim.md Wave 2 line", verifier: "uv run pytest tests/skills/test_worker_contract.py -q passes after Task 1"}
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-25T20:14:20Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-848 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-848

### src/superclaude/skills/sc-issue-protocol/refs/claim.md:36-51

```markdown
## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)

Checked in this order; every STOP here makes no GitHub or ClickUp write (B9):

1. `is_pull_request` is true -> STOP `E-NOT-AN-ISSUE`: "#N is a pull request, not an issue; not claimed."
2. `state` is `CLOSED` -> STOP: "Issue #N is closed; not claimed."
3. Assigned to anyone other than the current login -> STOP: "Issue #N is assigned to @<login>; not claimed."
4. Already assigned to the current login -> continue (re-claim is allowed and idempotent).
5. Earlier claim or accuracy-check comment IDs present -> remember them; Wave 6 edits those comments instead of posting new ones (B9, D18).

## Wave 3: assign (orchestrator)

1. `gh issue edit <N> --repo <R> --add-assignee @me`. Failure -> STOP `E-ASSIGN-FAILED`; ClickUp is not touched and no comment is posted.
2. Run the ClickUp script and write its stdout to `<D>/clickup.json`:
   `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`
   Every outcome it prints (`assigned`, `already_assigned`, `skipped`, `not_found`, `ambiguous`, `error`) is non-fatal and is reported in the claim comment. `error` with reason `page_cap` means the search reached `CLICKUP_MAX_PAGES` before the last page, so nothing was assigned; the claim comment says so and names the remedy (raise `CLICKUP_MAX_PAGES` or set `CLICKUP_LIST_IDS`). Exit 2 means the skill passed bad arguments: STOP and print the script's usage message; the GitHub assignment stays. Never print, echo or inline `CLICKUP_API_TOKEN`.
```

### src/superclaude/skills/sc-issue-protocol/refs/claim.md:149-149

```markdown
4. Every warning, the worktree one first (print the Wave 7 `warning` as `worktree_warning: <code>`, so an unattended run shows it): the code, its `detail`, and its remedy line from the two tables above. For `W-LAUNCH-FAILED`, also print the launch JSON's `hand_command` when it is not null (the remedy line promises it), and tell the user that an agent started by hand is not governed by the enforcement hook.
```

### src/superclaude/skills/sc-issue-protocol/SKILL.md:86-86

```markdown
3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6.
```

### src/superclaude/skills/sc-issue-protocol/SKILL.md:163-165

```markdown
| Issue closed | STOP, message "Issue #N is closed; not claimed.", no writes |
| Assigned to someone else | STOP, message names the assignee, no writes |
| Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |
```

### src/superclaude/commands/issue.md:16-16

```markdown
- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. With no `--pipeline` the claim picks `worktree` or `full` from the issue (the rule is in the skill, `refs/claim.md`). Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
```

### src/superclaude/core/HOW-WE-WORK.md:296-296

```markdown
| `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (with no `--pipeline` the level is picked from the issue: `full` for a bug or a simple or medium feature of 16 hours or less, `worktree` for a complex feature, one over 16 hours or one it cannot classify; `full`: implement, with no commit or push; `worktree`: plan, then wait for approval; `--submit` with `full`: also commit, push and open a PR; `none`: no worktree and no agent, you run the steps yourself) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with an issue type, the Complexity field and a mode label. Both post directly to GitHub and write `.dev/issues/`. |
```

### tests/skills/test_worker_contract.py:1886-1897

```python
AUDIT_ROOTS = (
    _REPO / "src" / "superclaude" / "skills",
    _REPO / "src" / "superclaude" / "commands",
    _REPO / "src" / "superclaude" / "agents",
)

# Whole words, not followed by a word character or "-", so `git merge-base`
# is not `git merge`. `git -C <path> <verb>` counts as `git <verb>`.
WRITE_VERB_RE = re.compile(
    r"\b(?:git(?:\s+-C\s+\S+)?\s+(?:add|commit|push|merge|stash|update-ref|worktree\s+(?:add|remove))"
    r"|gh\s+(?:pr|api))(?![\w-])"
)
```

### tests/skills/test_worker_contract.py:1951-1958

```python
def _check_all_classified() -> None:
    missing = sorted(
        {(path, verb, line) for path, verb, line, _ in _scan_write_verbs()}
        - set(WRITE_VERB_CLASSIFICATION)
    )
    assert not missing, "unclassified git/gh write-verb hits:\n" + "\n".join(
        f"{p} [{v}] {ln[:120]}" for p, v, ln in missing
    )
```

### tests/skills/test_worker_contract.py:2953-2960

```python
    (
        "src/superclaude/skills/sc-issue-protocol/refs/claim.md",
        "gh api",
        "- runs `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`;",
    ): (
        "read-only",
        "a read: gh issue view, gh pr list or a GET gh api user call",
    ),
```

### tests/skills/test_worker_contract.py:3167-3176

```python
def test_every_write_verb_hit_is_classified():
    _check_all_classified()


def test_classification_table_has_no_stale_entries():
    live = {(path, verb, line) for path, verb, line, _ in _scan_write_verbs()}
    stale = sorted(set(WRITE_VERB_CLASSIFICATION) - live)
    assert not stale, "classified lines no longer present:\n" + "\n".join(
        f"{p} [{v}] {ln[:120]}" for p, v, ln in stale
    )
```

### tests/skills/test_issue_protocol.py:237-241

```python
def _wave(text: str, number: int) -> str:
    """The text of `## Wave <number>` up to the next `## ` heading."""
    match = re.search(rf"^## Wave {number}\b.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"refs/claim.md has no Wave {number}"
    return match.group(0)
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 add the blocked-by check | F1,F3 | covered by Task 1 and Task 2 | .dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:28-48 |
| INF-002 read blocked_by in Wave 2 before Wave 3 | F1,F3 | covered by Task 1 | .dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:28-37 |
| INF-003 stop with E-BLOCKED naming each open blocker | F1 | covered by Task 1 | .dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:28-37 |
| INF-004 continue as today when none or all closed | F1 | covered by Task 1 | .dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:28-37 |
| INF-005 continue and say so when the list cannot be read | F1,F2 | covered by Task 2 | .dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:39-48 |
