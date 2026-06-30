# Handoff: Git cleanup session — untangle the staged blob on `docs/octocode-integration-investigation-backlog`

## Mission

The working branch has accumulated **one undifferentiated 46-file staged index** that conflates four unrelated concerns, plus ~20 untracked `.dev/` directories. **Nothing is committed** (`HEAD` = `e6d75415`). Your job: turn this into a clean series of intentional, individually-passing commits, then triage the untracked sprawl.

## Ground truth (verified 2026-06-04, re-verify before acting)

- `HEAD` = `e6d75415` — no commits landed this session.
- Working tree: **0 unstaged** files; everything is in the index (46 staged).
- All prior commit attempts failed on a pre-commit **markdownlint MD040** error.

### The staged blob = 4 concerns

| # | Concern | Files | Notes |
|---|---------|-------|-------|
| 1 | Octocode backlog removal | 29 staged deletions under `.dev/releases/backlog/octocode-integration-investigation/` | This branch's stated purpose |
| 2 | init-lite feature | `src/superclaude/cli/init_lite.py` (A), `cli/main.py` (M), `cli/install_skills.py` (M), `commands/init-lite.md` (A), `skills/sc-init-lite-protocol/SKILL.md` (A), `tests/cli/test_init_lite.py` (A), `tests/cli/test_cli_registration.py` (M), `tests/unit/test_cli_install.py` (M) | Verified clean by `/sc:reflect` — see `REPORT.md` in this dir. 101 tests pass. |
| 3 | TASK-RF-20260525-194356 promotion | 7 staged renames `to-do/ → done/` | The archival of concern #2's task |
| 4 | fingerprint exclusions | `cli/roadmap/fingerprint.py` (M), `tests/roadmap/test_fingerprint.py` (M) | Belongs to TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531; continuation of commit #88. 39 tests pass. |

### Untracked `.dev/` sprawl (NOT staged — second triage bucket)

`.dev/reflect/` (5 run dirs), `.dev/releases/Current/`, `.dev/releases/backlog/{SprintGranularResume,TaskQAComparison,sprint-cli-architecture-brainstorm,sprint-multiagent-handoff}/`, `.dev/reviews/pr123-remediation-brief.md`, `.dev/tasks/done/TASK-RF-20260525-194356/{phase-outputs,reviews}/`, `.dev/tasks/to-do/{TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531,TASK-PR111-HISTORY-SURGERY-20260602,TASK-RESEARCH-20260602-211124,TASK-TECHREF-20260603-021348}/`, `.dev/troubleshoot/{...}/`, `scripts/githubhttps.sh`.

## HARD BLOCKER — fix first, before any commit

`src/superclaude/commands/init-lite.md:22` — the Usage fenced block opens with a bare ` ``` ` (no language) → MD040. Fix in the **source-of-truth** file:

- Change the opening fence at line ~21 from ` ``` ` to ` ```text `.
- Then run `make sync-dev` (it's a synced `commands/` artifact).
- Run markdownlint to confirm there are no FURTHER violations (the hook stops at the first): `uv run pre-commit run markdownlint --all-files` or commit-by-commit and read failures.

**Do NOT** use `git commit --no-verify`, `mdformat`, `sed`, or any pivot to escape the hook — fix the markdown properly (see memory `feedback_no_strategy_pivot_to_avoid_hooks`).

## ABSOLUTE guardrails (CLAUDE.md — non-negotiable)

1. **UV only** — `uv run pytest`, never `python -m` / bare `pip`.
2. **Never stage `.claude/` paths** except `.claude/settings.json`. If `git add` ever needs `-f` on a `.claude/` path, STOP — move the change to `src/superclaude/` and `make sync-dev`. `.claude/{skills,commands,agents}` are gitignored sync output.
3. **Source-of-truth**: edit `src/superclaude/`, then `make sync-dev`, then `make verify-sync` (must exit 0) before committing.
4. **PR target = fork**: if you open a PR, `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> ...`. NEVER bare `gh pr create` (defaults to upstream `SuperClaude-Org`). Verify the returned URL is `IronbellyOrg/IronClaude`.
5. **No multi-line paste-ready commands** if you hand commands back to the operator — single-line only (their terminal can't paste heredocs/continuations).

## Recommended plan

### Step 0 — reset to a clean index (non-destructive; keeps working tree)

```
git reset
```

This unstages all 46 files (files stay on disk) so you can build intentional commits. `git mv` renames re-detect automatically at commit time.

### Step 1 — fix the MD040 blocker + sync + verify

Edit `src/superclaude/commands/init-lite.md` fence → `make sync-dev` → `make verify-sync` (exit 0).

### Step 2 — build commits in this order (each must pass pre-commit independently)

- **Commit A — octocode removal** (29 deletions):
  `git add -A .dev/releases/backlog/octocode-integration-investigation && git commit -m "docs(backlog): remove octocode-integration-investigation backlog"`
- **Commit B — init-lite feature** (8 files, incl. the MD040 fix + synced mirror — but NEVER stage `.claude/`; stage only `src/` + `tests/`):
  stage `src/superclaude/cli/init_lite.py src/superclaude/cli/main.py src/superclaude/cli/install_skills.py src/superclaude/commands/init-lite.md src/superclaude/skills/sc-init-lite-protocol tests/cli/test_init_lite.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py` → commit `feat(cli): add superclaude init-lite --context-optimized`
- **Commit C — archive completed task** (7 renames):
  `git add -A .dev/tasks && git commit -m "chore(tasks): archive TASK-RF-20260525-194356 (init-lite) to done"`
- **Commit D — fingerprint exclusions** (2 files):
  `git add src/superclaude/cli/roadmap/fingerprint.py tests/roadmap/test_fingerprint.py && git commit -m "chore(roadmap): exclude HTML/WILL/UNADDRESSED from anti-instinct fingerprint extraction"`

(B+C may be combined if you prefer feature+archive in one commit. A and D are independent.)

### Step 3 — triage untracked `.dev/` sprawl

For each untracked dir/file: decide commit / leave-untracked / delete. Many `.dev/reflect/`, `.dev/troubleshoot/` dirs are scratch run-artifacts — check `.gitignore` first (`git check-ignore <path>`). `scripts/githubhttps.sh` is code — review and commit or remove. Do NOT bulk `git add -A` the whole tree.

### Step 4 — verify

`uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py tests/roadmap/test_fingerprint.py -q` (expect 101 passed) and `make verify-sync` (exit 0).

## Open decision for the operator

This branch (`docs/octocode-integration-investigation-backlog`) now carries a **feature** (init-lite) on a `docs/` branch. Consider whether the init-lite commit(s) should be cherry-picked onto a `feat/init-lite` branch for a clean fork PR, vs. left here. Surface this; don't decide unilaterally.
