# Reviewer 1 brief (analyzer lens)

This is a UC-1 pre-execution review: there is no diff. Audit the TASKLIST at `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md` against the SPEC (the design) at `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md`. A 'deviation' here is a place where the plan omits, contradicts, reorders or over-reaches the design, or would break an existing test or invariant. Map classes as: Authorized = plan goes beyond the design with a stated basis; Necessary = plan departs from the design for a stated, real constraint; Drift = plan omits or alters a design instruction with no rationale; Regression = plan step would break an existing test, invariant or documented rule. Ground every finding at file:line (plan lines or spec lines or repository files). Read the live repository only to verify a cited fact; do not modify anything.

Lens: Ordering, dependency and design-to-plan fidelity defects. Focus: does each task leave the existing suite green at its own end? Is every design instruction that must be printed or decided by the skill supplied with the data it needs from the script?

## T1 card excerpt

```yaml
  - id: F-1
    kind: plan-sequencing
    severity_proposed: IMPORTANT
    claim: >-
      Task 1 creates scripts/orca_worktree.py but its SKILL.md files-table row is only added in Task 4;
      Task 5 creates templates/launch-prompt.md but its row is only added in Task 7. The existing test
      requires every scripts/*.py and templates/*.md on disk to be named in SKILL.md, so the existing
      suite is red between those tasks.
    evidence:
      - "tests/skills/test_issue_protocol.py:131 def test_every_named_path_exists_and_every_file_is_named"
      - "tests/skills/test_issue_protocol.py:141 assert sorted(on_disk - named) == []"
      - "plan:30 Task 1 heading (creates the script); plan:86 Task 4 adds the script table row"
      - "plan:95 Task 5 heading (creates the template); plan:130 Task 7 adds the template table row"
    recommendation: "Add the SKILL.md files-table row for the script to Task 1 and for the template to Task 5, and keep Tasks 4 and 7 for the prose edits."
  - id: F-2
    kind: spec-ambiguity-inherited
    severity_proposed: IMPORTANT
    claim: >-
      The final output must print the 'untracked, do not stage' line only when no file under the
      worktree's .dev/issues/<N>/ is tracked, but the worktree subcommand's output schema
      {status, path, branch, match_key, warning, detail} has no field that tells the skill this, and
      all worktree git calls are reserved to the script. Task 2 (plan:57) skips tracked files and names them,
      but only as free text in `detail`, not as a field the skill can read. The plan (Task 2 and Task 4)
      copies the gap.
    evidence:
      - "plan:57 Task 2 copy rule (tracked files named, no machine-readable field)"
      - "source.md:177 worktree output schema"
      - "source.md:158 final-output item 2 (untracked line)"
      - "plan:84 Task 4 final-output text"
    recommendation: "Add a field (for example tracked_files: [..]) to the worktree JSON in Task 2 and have Task 4 print the line from it."
  - id: F-3
    kind: doc-staleness
    severity_proposed: MINOR
    claim: >-
      The frontmatter description of commands/issue.md and of SKILL.md both say the claim 'then stop(s)'.
      That becomes false after this change. Task 3 and Task 4/7 list body sections but not the frontmatter
      description line.
    evidence:
      - "src/superclaude/commands/issue.md:3"
      - "src/superclaude/skills/sc-issue-protocol/SKILL.md:3"
      - "source.md:303 (design names SKILL.md 'description'; source.md:302 for commands/issue.md omits it)"
    recommendation: "Name the frontmatter description in Task 3 (command) and Task 4 (skill)."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T06:36:50Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag projectPath=/home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:30-44

````markdown
## Task 1: Create scripts/orca_worktree.py with its shared helpers and the preflight subcommand

Create `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (Python standard library only, executable-style header like `clickup_claim.py` in the same folder) and `tests/skills/test_issue_orca_worktree.py`. Source: design sections 8 (intro) and 8.1.

The script uses `argparse` subparsers `preflight`, `worktree`, `prompt`, `launch` (the last three are added by later tasks; register only `preflight` now). It prints exactly one JSON object on stdout, exits 0 for every runtime outcome and 2 only for bad arguments (argparse default). A shared `run(argv, timeout)` helper runs a command without a shell, captures output, and returns a failed result (never raises) on timeout, nonzero exit or missing binary. Timeouts: 120 s default, 30 s for `preflight`, 15 s for each `orca terminal read`.

`preflight` runs `orca status --json` and prints `{"ok": true}` only when the command exits 0 and the JSON has `ok: true` and `result.runtime.reachable: true`; otherwise `{"ok": false, "detail": "<first stderr line or why the JSON failed>"}`. A missing `orca` binary gives the same shape.

The test file builds the reusable fixtures for the whole feature: a fake `orca` script written to a temporary directory that logs every argv to a file and answers from per-test JSON, a temporary git repository with an `origin` remote, and a temporary `HOME`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k preflight` passes with cases PF-1 (ok: true) and PF-2 (not reachable, nonzero exit, invalid JSON, and no `orca` on `PATH` each give `ok: false` with a non-empty detail).
- A call with a bad subcommand or missing required argument exits 2.
- A hanging fake `orca` is cut by the timeout and reported as `ok: false`, not as a crash (the timeout is overridable in the test through an environment variable or function argument so the test runs in under 5 seconds).

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:78-92

````markdown
## Task 4: Add the Orca check and Wave 7 to the issue skill and claim ref

Depends on: Task 2

Edit `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `tests/skills/test_issue_protocol.py`. Source: design sections 7 (Wave 0, Wave 6, Wave 7), 10 and 11.

In `refs/claim.md` Wave 0 add a new step 3 after `gh auth status` and before the default-branch lookup: run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight`; `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`, before any GitHub or ClickUp write. Replace Wave 6 step 4 ("Print the `next-steps.md` path and STOP") with a hand-off: after both comments are posted, run Wave 7 (and Wave 8, added by a later task); any STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. Add Wave 7: run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>`, read its JSON, every failure is a warning and the claim `status` stays `success`; print the worktree path, status, match key, the "reused a worktree not created by /sc:issue" line for keys `basename` and `branch`, the "untracked, do not stage" line when no file under the worktree's `.dev/issues/<N>/` is tracked, "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive, and each warning with its remedy line from design section 11 (worktree codes).

In `SKILL.md`: add the `scripts/orca_worktree.py` row to the files table; update the claim-mode paragraph and claim step 1 (Wave 0 check) and step 7 (Wave 6 now continues to the worktree step); add `E-ORCA-REQUIRED` and the worktree warning codes to the error table; keep the file under 500 lines. Update `tests/skills/test_issue_protocol.py`: the files-table test accepts the new script, ST-5 (still five refs, script named and present), ST-6 (preflight in Wave 0 before Wave 1, Wave 7 after the Wave 6 posts).

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py` passes.
- `grep -n "src/superclaude" src/superclaude/skills/sc-issue-protocol/SKILL.md src/superclaude/skills/sc-issue-protocol/refs/claim.md` finds nothing.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` reports fewer than 500 lines.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:95-109

````markdown
## Task 5: Add the launch prompt template and the prompt subcommand

Depends on: Task 1

Create `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` and add the `prompt` subcommand to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; extend `tests/skills/test_issue_orca_worktree.py` and `tests/skills/test_issue_protocol.py`. Source: design sections 8.2 and 9.

The template has exactly four blocks, each opened by an HTML-comment marker line of the form `block:<name>` wrapped as shown in design section 9 (names `common`, `worktree`, `full`, `submit`), with the required statements of the design section 9 table: common (read `issue-summary.md` and `next-steps.md`; run each step by invoking its command through the Skill tool in this session, never by reading a command file and never inside a subagent; report a model-tier mismatch with the tier named in `next-steps.md`; never merge, never push to `master` or `main`); worktree (follow the steps up to the `Plan boundary` line; do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`; print the plan path and `Waiting for approval`, then wait; after a human replies `approved` or runs the printed implement command, run the remaining steps, still without commit, push or `/sc:pr-submit`); full (run every step through the last, leave changes in the working tree, stage nothing, finish by printing `git status --short`); submit (the owner asked for the commit and push by passing `--submit`; check that no PR is already open or merged for the branch; commit with a conventional-commit message staging `.dev/tasks` and the changed files, never `.claude/` and never `.dev/issues/`; push the current feature branch to `origin`, never `master`; run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`; never merge).

`prompt --template <path> --level worktree|full [--submit] --number <N> --out <file>` keeps `common` plus the level block (plus `submit` with `--submit`), drops every other block and all marker lines, replaces `<N>`, writes `--out` and prints `{"status": "written", "path": "<out>"}`. `--submit` with `--level worktree` exits 2.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k prompt` passes with PR-1 to PR-4 (levels keep only their own block, `--submit` adds the submit block, `--submit` with `worktree` exits 2, the rendered `full` output and the `common` block hold none of `/sc:pr-submit`, `git push`, `git commit`, `--monitor`).
- `tests/skills/test_issue_protocol.py` has ST-8: the template has exactly the four blocks, only the `submit` block contains `/sc:pr-submit --monitor 3`, `git push` and the commit instruction, and only the `worktree` block also contains those tokens (as a prohibition).
- The rendered `worktree` output contains the line telling the agent not to run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:122-136

````markdown
## Task 7: Add Wave 5 additions, Wave 8, the Plan boundary line and the claim return contract

Depends on: Task 4, Task 5, Task 6

Edit `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `tests/skills/test_issue_protocol.py`. Source: design sections 7 (Wave 5 additions, Wave 8, final output), 10 and 11.

In `templates/next-steps.md` add the line `Plan boundary: after step <K>` under the title. In `refs/claim.md` Wave 5 add: the skill sets `<K>` to the number of the last step before the first step whose command is `/sc:implement` or `/task` (the line reads `Plan boundary: before step 1` when the first step is the implementation step; `--pipeline full` ignores it); for any `--pipeline` value other than `none`, run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --out "<D>/launch-prompt.md"` before Wave 7 so the copy carries it. Add Wave 8: runs only when `--pipeline` is not `none` and Wave 7 status is `created` or `reused`; run `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`; never attempted for a `failed` worktree; failures are warnings and the claim stays `success`. Replace the Wave 6 hand-off with the final output of design section 7 (next-steps path, worktree line, launch result lines for launched, already_launched and none, every warning with its remedy line from design section 11 including the three launch codes, then the return contract).

In `SKILL.md`: add the `templates/launch-prompt.md` row to the files table; replace the claim-mode return contract with the ten fields of design section 10 (`pipeline_level`, `submit`, `worktree_status`, `worktree_path`, `worktree_branch`, `worktree_match_key`, `worktree_warning`, `launch_status`, `launch_warning`, `enforcement_hook`), create mode unchanged; add `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `E-CLAIM-ONLY-FLAG` and `E-SUBMIT-NEEDS-FULL` to the error table; update the Will and Will Not lists to match the command file (the skill itself still runs no next-step command; the launched agent does; nothing merges). Add tests ST-4 (no forbidden Orca flag in skill, refs, command or script outside the launch call), ST-7 (`Plan boundary` in the template and the `<K>` rule in the ref), ST-9 (Wave 8 skipped for `none`, prompt file written before Wave 7), ST-10 (the ten contract fields), ST-11 part one (no `src/superclaude/` path in any file of the skill).

Acceptance criteria:
- `uv run pytest tests/skills tests/commands` passes.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` reports fewer than 500 lines.
- `grep -rn "src/superclaude" src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol` finds nothing.

````

### tests/skills/test_issue_protocol.py:125-145

````python
    assert "\nname: sc:issue-protocol\n" in head + "\n"
    assert f"\nallowed-tools: {ALLOWED_TOOLS}" in head
    assert "\ndescription: " in head
    assert len(text.splitlines()) < 500


def test_every_named_path_exists_and_every_file_is_named():
    text = _text(SKILL)
    named = set(_SKILL_PATH.findall(text))
    on_disk = {
        str(p.relative_to(SKILL_DIR))
        for pattern in ("refs/*.md", "templates/*.md", "scripts/*.py")
        for p in SKILL_DIR.glob(pattern)
    }
    assert on_disk, "the skill package has files"
    assert sorted(n for n in named if not (SKILL_DIR / n).is_file()) == []
    assert sorted(on_disk - named) == []


@pytest.mark.parametrize(
    "path", [SKILL, *sorted(REFS.glob("*.md"))], ids=lambda p: p.name
````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:156-161

````markdown

1. The `next-steps.md` path, then `Worktree: <wt>` (status, `match_key`; on key `basename` or `branch` the line "reused a worktree not created by /sc:issue").
2. The "untracked, do not stage" line (MR 2.4) when it applies, and "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive (MR 5 step 2).
3. Launch result: `launched` -> "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." (`full` -> "It runs every step and stops after implementation." `full --submit` -> "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges.") `already_launched` -> "agent already launched at <time>; remove the `launch` entry of <D>/worktree.json to launch again". `none` -> "No agent launched. Open <wt> and run .dev/issues/<N>/next-steps.md there."
4. Every warning with its remedy line (section 11), the worktree warning first.
5. The return contract (section 10) and STOP. The claim `status` stays `success` through any Wave 7 or Wave 8 failure: the assignment and comments cannot be undone (AD 4.5, FR-10, FR-29).
````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:175-177

````markdown
### 8.3 `worktree`

Arguments `--repo <R> --number <N> --base origin/<B> --source <D>`. Output `{status, path, branch, match_key, warning, detail}` with `status` `created | reused | failed`. The algorithm is MR section 5 with AD section 4 applied; commands are MR section 4 exactly, each with a 120 s timeout:
````

### src/superclaude/commands/issue.md:1-20

````markdown
---
name: issue
description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then stop) or create a templated issue with labels from a fixed set"
category: workflow
complexity: advanced
mcp-servers: [auggie, codegraph]
personas: [analyzer]
argument-hint: "--claim <number|url> | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
---

# /sc:issue: GitHub Issue Claim and Create

Two modes on the repository that `origin` points at:

- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then stops. It never runs the next-step commands.
- `--create` turns a description into a GitHub issue built from one of four templates, with labels from a fixed set. GitHub only: no ClickUp task.

Both modes post directly to GitHub; nothing is shown for approval first.

For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.
````

## Coverage slice

| Requirement | Spec line | Status | Matched task | Ratio | Quote |
|---|---|---|---|---|---|
| INF-017 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:138 | covered | Task 4 (best Task 4) | 1.0 | `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`. |
| INF-018 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:144 | covered | Task 5 (best Task 5) | 0.75 | `next-steps.md` gets its `Plan boundary: after step <K>` line (FR-26). |
| INF-019 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:145 | covered | Task 7 (best Task 7) | 1.0 | It is written before Wave 7 so the copy carries it. |
| INF-020 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:147 | covered | Task 4 (best Task 4) | 0.833 | Wave 7 runs only after both comments are posted. |
| INF-021 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:153 | covered | Task 7 (best Task 7) | 0.8 | Runs when `<L>` is not `none` and Wave 7 `status` is `created` or `reused` (FR-21) |
| INF-022 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:161 | covered | Task 4 (best Task 4) | 0.889 | The claim `status` stays `success` through any Wave 7 or Wave 8 failure |
| INF-023 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:165 | covered | Task 1 (best Task 1) | 1.0 | One JSON object on stdout. Exit 0 for every runtime outcome; exit 2 only for bad arguments (argparse). |
| INF-024 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:165 | covered | Task 1 (best Task 1) | 0.857 | Every subprocess runs without a shell, with a timeout (120 s; `preflight` 30 s; each `terminal read` 15 s) and captured output. |
| INF-025 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:169 | covered | Task 1 (best Task 1) | 1.0 | `{"ok": true}` when it exits 0, prints JSON with `ok: true` and `result.runtime.reachable: true` |
| INF-026 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:173 | covered | Task 1 (best Task 1) | 0.714 | `--submit` with `--level worktree` is bad arguments (exit 2). |
| INF-039 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:228 | covered | Task 5 (best Task 5) | 0.923 | The `full` and `common` blocks never contain the tokens `/sc:pr-submit`, `git push`, `git commit` or `--monitor` |
| INF-040 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:256 | covered | Task 7 (best Task 7) | 0.857 | `launch_status` is `not_requested` for `none` and when Wave 7 `failed`. |
| INF-042 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:287 | covered | Task 4 (best Task 4) | 0.625 | Nothing under `.claude/` is edited or staged; `make sync-dev` produces it. |
| INF-044 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:303 | covered | Task 4 (best Task 4) | 1.0 | Stays under 500 lines. |
