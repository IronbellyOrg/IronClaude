---
title: Independent verification of the /sc:issue implementation (GitHub issue #302)
task_id: task_0aabbab7531c
dispatch_id: ctx_1d41d511b89e
branch: ironbelly/feat-sc-issue-command
base_commit: 119622e3
date: 2026-11-04
role: independent verifier (did not write the code; read-only)
verdict: FAIL
blocking_findings: 1
---

# Verification report: /sc:issue (issue #302)

Structure follows the task brief's OBSERVABLE ACCEPTANCE list (no registered template exists for this report type).

## 1. Suite results

Run by me in this worktree on 2026-11-04 (HEAD `119622e3` plus the uncommitted change).

| Command | Exit code | Result | Log |
|---|---|---|---|
| `uv run pytest -q -p no:cacheprovider` (full suite) | 0 | 14830 passed, 0 failed, 136 skipped, 0 errors, 2 xpassed, 32 warnings, 461.60 s | `.dev/tasks/issue-302-handoff/verify/full-pytest.log` |
| `make lint` | 0 | `All checks passed!` (architecture policy PASS with 5 warnings) | `.dev/tasks/issue-302-handoff/verify/lint.log` |
| `make verify-sync` | 0 | `All components in sync.` | `.dev/tasks/issue-302-handoff/verify/verify-sync.log` |

Comparison with the implementer's claim (14830 passed / 136 skipped / 0 failed): **identical** counts (the implementer also reported 2 xpassed).

Side effect: the full suite rewrote the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (549 lines changed, the known behaviour of `tests/cli/eval/test_perf_home_setup.py`). It was unmodified before my run, so I restored it with `git restore`; the working tree is back to its pre-run state.

## 2. Design section 20 acceptance criteria

Checked against the code and tests on disk, not against the implementer's artifacts. "Runbook step" refers to the "Post-restart runbook" at the end of `.dev/tasks/done/TASK-WF-scIssueCommand-20261104-064713/artifacts/t17-acceptance.md` (lines 19-40); every pending-live item below is listed there.

| # | Criterion (design `docs/designs/sc-issue-command.md:467-475`) | Status | Evidence |
|---|---|---|---|
| 1 | Claim on an open, unassigned issue: T3 first; assigned; seven files; two marked comments; stops | pending-live (runbook step 5) | Static support verified: T3 spawned in Wave 1 after Wave 0 (`src/superclaude/skills/sc-issue-protocol/SKILL.md:80-81`, `refs/claim.md:22-31`); assign `refs/claim.md:47`; seven files named in `SKILL.md:81-86` and `refs/claim.md:30,48-49,57-59,78-79,88`; markers pinned by `tests/skills/test_issue_protocol.py:160-162`; stop `refs/claim.md:80,90`. Note: Wave 0 makes one orchestrator GitHub read (`gh repo view`) before the T3 spawn, finding m1 |
| 2 | Re-claim edits both comments; comment count does not grow | pending-live (runbook step 5) | Static support verified: earlier IDs found by marker and author, ID taken from `#issuecomment-` (`refs/claim.md:29`), PATCH by ID (`refs/claim.md:84-88`) |
| 3 | Closed or assigned-to-someone-else stops with the stated message, no write | pending-live (runbook step 5) | Static support verified: ordered checks before any write (`refs/claim.md:35-43`; "No GitHub or ClickUp write happens before Wave 3", `refs/claim.md:20`) |
| 4 | Foreign-repo claim URL stops with `E-FOREIGN-REPO`; no `gh` call without `--repo` | verified (static/unit); live run pending-live (runbook step 4) | `check_claim` compares owner and repo as whole segments, case-insensitive (`scripts/origin_repo.py:102-153`); Wave 0 calls it with exit 3 mapped to `E-FOREIGN-REPO` (`SKILL.md:80`, `refs/claim.md:13-15`); tests `tests/skills/test_issue_repo_resolution.py:126-133,173-194,197-215,218-234`. Clause 2: every `gh issue/pr/label` mention carries `--repo` (`tests/skills/test_issue_protocol.py:223-225`, `tests/skills/test_issue_worker_agents.py:108-112`); my grep of every `gh` mention in the command, skill and agents found only these other forms: `gh auth status`, `gh repo view <R>` (positional repo, `refs/claim.md:17`) and `gh api user` / `gh api ... repos/<R>/...` |
| 5 | Token unset: claim completes, comment says skipped; token + linked task: user assigned | pending-live (runbook steps 3 and 5) | Script behaviour verified by unit tests: `no_token` skip with zero requests (`tests/skills/test_clickup_claim.py:177-182`), link match and PUT body `{"assignees": {"add": [id]}}` (`tests/skills/test_clickup_claim.py:196-213,275-282`); skip is non-fatal (`refs/claim.md:50`) and reported via `templates/claim-comment.md:3` |
| 6 | Create at each depth: template headings, only existing fixed-set labels, one marked pushback at standard/deep, no ClickUp | pending-live (runbook step 6) | Static support verified: headings in order (`tests/skills/test_issue_protocol.py:172-174`), label intersection and no creation (`refs/create.md:65`, `refs/labels.md:15-20`), pushback with marker (`refs/create.md:68`, `templates/create-review-comment.md:10`), no ClickUp (`refs/create.md:9,69`) |
| 7 | Each worker pins its picker ID, the skill never passes `model` (static); smoke per worker | static half verified; smoke pending-live (runbook step 2) | `model:` at `src/superclaude/agents/issue-worker-t3.md:6`, `-t2.md:6`, `-t1.md:6`; pinned by `tests/skills/test_issue_worker_agents.py:62-74`; spawn rule `SKILL.md:54,150`. My grep of the skill found no Agent call carrying `model`; the static test only checks that the prohibition text is present (finding m4) |
| 8 | `next-steps.md` uses only section 19 commands and flags, starts with `/model`, no brainstorm handoff | static half verified; live half pending-live (runbook step 5) | `templates/next-steps.md:1` is the `/model` line; chain rows `refs/chains.md:11-16`. I checked every flag in those rows against the installed `~/.claude/commands/sc/{brainstorm,workflow,design,troubleshoot,implement}.md` option tables and usage lines: all exist with the values used (`--depth quick/deep`, `--research deep`, `--codebase`, `--blind`, `--models`, `--handoff none`, `--type`, `--format spec`, `--fix`, `--context`, `--scope`). No `--handoff tasklist/design` (`tests/skills/test_issue_protocol.py:205-214`) |
| 9 | `make verify-sync` passes; section 16 tests pass; `tests/core tests/commands` pass; no new path-grep hit | verified | My runs: section 1. Path grep: zero text hits in `commands/issue.md`, `skills/sc-issue-protocol/`, `agents/issue-worker-t*.md` (only gitignored `scripts/__pycache__/*.pyc` binaries match, the same as the existing `sc-implement-protocol/scripts/__pycache__`) |

## 3. Coordinator constraints C1 to C3

| Constraint | Result | Evidence |
|---|---|---|
| C1: workers carry no `permissionMode`; a test asserts it | met | Frontmatter of `src/superclaude/agents/issue-worker-t{1,2,3}.md:1-7` has `name`, `description`, `category`, `tools`, `model` only; `tests/skills/test_issue_worker_agents.py:85-90` asserts the key and the word are absent |
| C2: deterministic `E-FOREIGN-REPO` URL-versus-origin check with the six required test cases; no live claim or create | met | Check: `scripts/origin_repo.py:102-153`. Cases in `tests/skills/test_issue_repo_resolution.py`: foreign owner `:176`; same owner, different repo `:177`; repo-name prefix `:178-179` (plus owner-name prefix `:180`); `/pull/` URL `:197-215`; trailing slash, fragment, query `:159-161`; digits in owner or repo `:218-234`. No live run: the only `gh issue create` / `gh label create` strings in the package logs are test names (`artifacts/t14-full-pytest.log:9185` and copies); no `.dev/issues/<N>/` claim directory exists (only `.dev/issues/433/`, from the Coder #433 ccsession work); issue #302 still has exactly 3 comments and none carries an `sc:issue` marker; the last #302 timeline event (reassignment at 2026-11-04T06:29:11Z) predates the implement dispatch (13:25 UTC, `artifacts/coordinator-constraints.md:3`); the one issue the gh account created today (#357, 13:01Z) has no `sc:issue` marker and no template prefix |
| C3: live checks recorded pending with a runbook | met | `artifacts/t17-acceptance.md:9-16` marks items 1-3, 5, 6 and the live halves of 4, 7, 8 pending; the runbook (`:19-40`) lists worker smoke spawns, the ClickUp smoke claim, the live foreign-repo claim, live claims and the three creates, with commands and the variables to export |

## 4. Repo rules

| Rule | Result | Evidence |
|---|---|---|
| No hardcoded `src/superclaude/` path in installed primitives | pass | `grep -rn 'src/superclaude' src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol src/superclaude/agents/issue-worker-t*.md`: no text hit; only the two gitignored `scripts/__pycache__/*.cpython-311.pyc` binaries match (compiled-path metadata from the test imports; `.gitignore:2`; the installer and `make sync-dev` skip `__pycache__`) |
| Dual-surface lookup | **fail** (one lookup, two files) | Agents and templates name both surfaces (`issue-worker-t*.md:26-28`; `SKILL.md:22,62`; `refs/claim.md:7`). But `issue-worker-t1.md:17` and `issue-worker-t2.md:17` tell the worker to apply "the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`" with no project `.claude/` copy. Finding B1 |
| Every `gh` call passes `--repo <origin repo>` | pass | Every `gh issue`, `gh pr`, `gh label` mention carries `--repo <R>` (tests above plus my grep); `gh api` paths are `user` or `repos/<R>/...`; `gh repo view <R>` names the repo positionally; `gh auth status` takes no repo |
| Nothing under `.claude/` staged | pass | `git diff --cached --name-only` lists only `.dev/` paths |
| `src/` and `.claude/` copies in sync | pass | `make verify-sync` rc=0 (`verify/verify-sync.log`); `diff -rq` of the skill, command and three agents: identical except `src/.../scripts/__pycache__` (excluded by the sync check, `Makefile:178`) |
| `HOW-WE-WORK.md` byte copy | pass | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`: identical |

## 5. Findings

### Blocking

| ID | Severity | Location | Evidence | Suggested fix |
|---|---|---|---|---|
| B1 | blocking | `src/superclaude/agents/issue-worker-t1.md:17`, `src/superclaude/agents/issue-worker-t2.md:17` | Both workers are told to compute the effort estimate (B3) "using the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`", naming only the installed copy. The project `CLAUDE.md` dual-surface rule (and design section 15's path rule, `docs/designs/sc-issue-command.md:366`) requires a lookup of another installed primitive to name the project `.claude/` copy too. Failure scenario, observed now: in this dev checkout `~/.claude/skills/sc-issue-protocol` does not exist (`ls` fails) while `.claude/skills/sc-issue-protocol/refs/claim.md` does, so the live claims of runbook step 5, which run in this checkout, point the Wave 4 worker at a missing file; the orchestrator's spawn job ("accuracy check and summary", `refs/claim.md:54`) does not carry the rubric bands, so the hours and complexity in `summary.md` would be estimated without the fixed scale. The same files already apply the two-surface form for templates (`:27`), so this is an omission, not a design choice | Change both lines to name both copies in the skill order, e.g. "the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md` (project `.claude/skills/sc-issue-protocol/refs/claim.md` in a checkout; read the installed copy first)", or inline the three rubric bands; add an assertion to `tests/skills/test_issue_worker_agents.py` that every `~/.claude/skills/` lookup line also names `.claude/skills/` |

### Minor (notes; do not fail the review)

| ID | Severity | Location | Evidence | Suggested fix |
|---|---|---|---|---|
| m1 | minor | `src/superclaude/skills/sc-issue-protocol/refs/claim.md:17`, `SKILL.md:80` vs `SKILL.md:141` | Claim Wave 0 has the orchestrator run `gh repo view <R> --json defaultBranchRef` before the T3 spawn, while `SKILL.md:141` says "Spawn the T3 worker before any lookup of its own" and design section 7 Wave 1 says the same. One metadata read; the T3-first intent of B13 (lookup work on T3) still holds | Let the T3 worker resolve the default branch (`git symbolic-ref refs/remotes/origin/HEAD` after its `git fetch origin`), or reword `SKILL.md:141` to exempt Wave 0 prerequisites |
| m2 | minor | `src/superclaude/skills/sc-issue-protocol/refs/create.md:66` | `gh issue create --title "<prefix><title>"`: no worker job, template or ref says who writes `<title>`; the orchestrator has to invent it. The design has the same gap (section 8 Wave 5) | Add a `Title:` line to `templates/draft-notes.md` filled by the drafting worker |
| m3 | minor | `tests/skills/test_issue_protocol.py:191-202` | Chain-flag check is a substring test against the source command file only; it would pass a flag whose name appears anywhere in the file and does not check values (for example `--research deep`). Design section 16 said "installed-or-source"; the narrowing is documented in the test docstring. I checked the flags and values by hand (section 2, item 8) | Match flags against the Options-table rows and check enumerated values |
| m4 | minor | `tests/skills/test_issue_protocol.py:142-144` | Acceptance item 7 asks for a static test that the skill never passes `model`; the test only asserts the prohibition sentence is present, not that no spawn instruction carries `model`. A grep shows none does | Add a negative scan, e.g. no `model:` / `model=` inside any spawn instruction of `SKILL.md` and `refs/*.md` |
| m5 | minor | `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:94-98,118` | The 429 retry sleeps for whatever `Retry-After` says, with no upper bound; a large value stalls the claim in Wave 3 | Cap the wait (for example 60 s) and return `rate_limited` above it |
| m6 | minor | `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:66-69` | Origin forms `ssh://git@github.com/...`, `https://user@github.com/...` and a mixed-case host (`GitHub.com`) give `E-NO-ORIGIN` (probed directly). This matches design section 13, which lists only the two accepted forms | Optional: accept the `ssh://` and userinfo forms |
| m7 | minor | `src/superclaude/skills/sc-issue-protocol/templates/issue-*.md:1` | Each issue-body template starts with an instruction comment (`<!-- /sc:issue ... template ... -->`); nothing tells the worker to remove it, so it is posted (hidden) in the issue body | Tell the drafting worker to delete line 1, or accept it as hidden |

Checked and not a defect: ClickUp uses the REST API v2 with the person's own token from the environment, no MCP (`clickup_claim.py:9-37,101-109`); the token is only sent in the `Authorization` header, never in argv or output, and a catch-all keeps tracebacks out of stdout (`clickup_claim.py:221-224`); posts go up directly with one prompt only for new material or contradictions (`refs/create.md:57-59`); all artifacts live under `.dev/issues/<N>/` from templates; the label set is fixed and never created (`refs/labels.md:7,20`); T1 or T2 for next steps via the `/model` line (`refs/claim.md:79`); claim edge cases (`refs/claim.md:35-43`); lookalike hosts (`github.com.evil.io`, `api.github.com`) give `E-FOREIGN-REPO` (probed directly).

## 6. Verdict

**FAIL**: 1 blocking finding (B1), 7 minor notes (m1 to m7).

B1 is a one-line fix in each of two agent files (name the project `.claude/` copy of `refs/claim.md` next to the installed one). Everything else checked holds: suite, lint and sync pass with the claimed counts; C1, C2 and C3 are met; items 4 and 9 of section 20 are verified, the static halves of 7 and 8 are verified, and items 1, 2, 3, 5, 6 plus the live halves of 4, 7, 8 are pending-live and all listed in the runbook. No live claim, create or GitHub write was found.
