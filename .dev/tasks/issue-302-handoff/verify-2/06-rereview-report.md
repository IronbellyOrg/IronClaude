---
title: Independent re-review 2 of the /sc:issue implementation after fix round 1 (GitHub issue #302)
task_id: task_615b95f0a860
dispatch_id: ctx_aafa74f19edd
branch: ironbelly/feat-sc-issue-command
base_commit: 119622e3
date: 2026-11-04
role: independent re-reviewer (did not write the code or the fix; read-only)
verdict: PASS
blocking_findings: 0
minor_findings: 3
---

# Re-review 2: /sc:issue (issue #302)

Structure follows the task brief's OBSERVABLE ACCEPTANCE list (no registered template exists for this report type).
Inputs treated as unverified claims: `.dev/tasks/issue-302-handoff/verify/04-verification-report.md` (review 1) and `.dev/tasks/issue-302-handoff/fix-1/05-fix-report.md` (fix round 1).

## 1. B1 status

**Fixed.** Rule checked: project `CLAUDE.md:96` (name both the installed and the project `.claude/` copy; for skills, read `~/.claude/skills/` first, then `.claude/skills/`).

Every `~/.claude/skills/` mention in the three workers, read from the files on disk:

| File:line | Text (shortened) | Kind | Both copies? | Order |
|---|---|---|---|---|
| `src/superclaude/agents/issue-worker-t1.md:17` | effort estimate "using the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md` (the in-checkout copy is the project `.claude/skills/sc-issue-protocol/refs/claim.md`; read the installed copy first)" | read instruction (the B1 line) | yes | installed first: correct |
| `src/superclaude/agents/issue-worker-t2.md:17` | identical wording | read instruction (the B1 line) | yes | installed first: correct |
| `issue-worker-t1.md:27`, `-t2.md:27`, `-t3.md:26` | templates under `~/.claude/skills/sc-issue-protocol/templates/` (project `.claude/skills/sc-issue-protocol/templates/`; installed first) | read instruction | yes (unchanged since review 1) | correct |
| `issue-worker-t1.md:11`, `-t2.md:11`, `-t3.md:11` | "Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`) ..." | provenance (who spawns the worker) | no (exempted) | n/a |

The rubric target exists in both surfaces: `refs/claim.md:64-72` holds the "Effort and complexity rubric", and `diff -rq src/superclaude/skills/sc-issue-protocol .claude/skills/sc-issue-protocol` shows the trees identical apart from `scripts/__pycache__`. In this checkout `~/.claude/skills/sc-issue-protocol` still does not exist (`ls` fails), so the fallback wording is what makes the Wave 4 worker find the rubric here. `issue-worker-t3.md` has no rubric job and needed no edit. `.claude/agents/issue-worker-t{1,2,3}.md` are byte-identical to `src/` (`cmp`).

**Line-11 exemption: sound.** Line 11 tells the worker who spawned it and that no `model` parameter is passed; it asks the worker to read nothing, and no job or rule refers the worker to `SKILL.md`. A worker never needs that file (every input it needs is a named template, `refs/claim.md` or `analyze.md`, all dual-surfaced). Leaving the text unchanged kept the fix to the B1 scope. The way the test implements the exemption is looser than the decision itself (a line-prefix match); see finding N2.

## 2. Regression-test proof

Test read: `tests/skills/test_issue_worker_agents.py:122-182`. The helper `skills_lookups_missing_project_copy` (`:135-148`) returns every line that contains `~/.claude/skills/`, does not start with the provenance prefix (`:126`), and has no `.claude/skills/` that is not preceded by `~/` (regex `:123`). `test_every_skills_lookup_names_both_copies` (`:151-156`) runs it on the three real files; `test_skills_lookup_check_fails_on_old_rubric_line` (`:159-169`) pins the exact fixed rubric text once and checks that reverting it is flagged; `test_skills_lookup_helper` (`:172-182`) has 4 unit cases.

Fix-round claims checked on disk: `fix-1/pre-fix-new-test.log` shows `test_every_skills_lookup_names_both_copies[issue-worker-t1]` and `[issue-worker-t2]` FAILED on the old line 17 text, `EXIT_CODE=1`; `fix-1/full-pytest.log` ends `14839 passed, 136 skipped, 2 xpassed` and `EXIT_CODE=0`.

My own mutation run: the test file, the three agent files and `ccsession-models.json` copied to a private `mktemp -d /tmp/rereview2.*` tree (removed afterwards), each copy mutated, the test run there with `uv run pytest -c <copy>/pytest.ini --rootdir <copy>`. The real files were not touched. Log: `.dev/tasks/issue-302-handoff/verify-2/regression-probe.log`.

| Case | Mutation of the temporary copy | Result | Caught? |
|---|---|---|---|
| M0 | none (baseline) | 35 passed, exit 0 | n/a |
| M1 | t1 line 17 reverted to the pre-fix text | 2 failed (`names_both_copies[t1]`, `fails_on_old_rubric_line[t1]`), exit 1 | yes |
| M2 | t2 line 17 reverted to the pre-fix text | 2 failed (`[t2]` pair), exit 1 | yes |
| M3 | t3 templates line loses its project copy | 1 failed (`names_both_copies[t3]`), exit 1 | yes |
| M4 | t1 project copy misspelt `.claude/skill/` | 2 failed, exit 1 | yes |
| M5 | new installed-only lookup line added to t3 | 1 failed (`names_both_copies[t3]`), exit 1 | yes |
| M6 | t1 line 17 order reversed (project copy first) | 1 failed, but only `fails_on_old_rubric_line[t1]` (exact-text pin); the general check passed | only by the exact-text pin |
| M7 | installed-only lookup appended to the exempt line 11 of t3 | 35 passed, exit 0 | **no** |
| M8 | t1 line 17 project copy names a different file | 1 failed, only the exact-text pin; the general check passed | only by the exact-text pin |

Conclusion: the test really catches the B1 regression (M1, M2) and the same omission on any other line (M3 to M5). Gaps (order, same-path pairing, the prefix exemption) are recorded as minor finding N2; they do not affect B1.

## 3. Suite, lint and sync results

Run by me in this worktree on 2026-11-04 (HEAD `119622e3` plus the uncommitted change after fix round 1). Each log ends with an `EXIT_CODE=` line.

| Command | Exit code | Result | Log |
|---|---|---|---|
| `uv run pytest -q -p no:cacheprovider` (full suite) | 0 | 14839 passed, 0 failed, 0 errors, 136 skipped, 2 xpassed, 32 warnings, 449.10 s | `.dev/tasks/issue-302-handoff/verify-2/full-pytest.log` |
| `make lint` | 0 | `All checks passed!` (architecture policy PASS with 5 warnings, the same as review 1) | `.dev/tasks/issue-302-handoff/verify-2/lint.log` |
| `make verify-sync` | 0 | `All components in sync.` | `.dev/tasks/issue-302-handoff/verify-2/verify-sync.log` |

Counts agree with the fix report (14839 passed, 136 skipped, 2 xpassed) and with review 1 plus the 9 new parametrised cases (14830 + 9 = 14839). Side effect of my run: `perf.json` was rewritten again (md5 `7d073220...` before, `72ee9fa3...` after); I did not restore it (read-only constraint), see N3.

## 4. No collateral change

Reference point: review 1's report `verify/04-verification-report.md`, mtime 2026-11-04 14:28:48 UTC. I listed every tracked or untracked, non-ignored file (`git ls-files` plus `git ls-files --others --exclude-standard`, minus `.dev/tasks/issue-302-handoff/`) with a newer mtime:

| File | mtime (UTC) | Content changed? | Cause |
|---|---|---|---|
| `src/superclaude/agents/issue-worker-t1.md` | 14:30:54 | yes (line 17) | the fix, listed in `05-fix-report.md` |
| `src/superclaude/agents/issue-worker-t2.md` | 14:30:56 | yes (line 17) | the fix, listed |
| `tests/skills/test_issue_worker_agents.py` | 14:30:45 | yes (new helper and tests) | the fix, listed |
| `.dev/releases/current/cliEval/evidence/T02.15/perf.json` | 14:41:31 | yes, `git status` ` M`, 549 lines | full-suite side effect (`tests/cli/eval/test_perf_home_setup.py`): it was already modified at the start of this review (session-start `git status`), so the fix round's own full run left it dirty; my run rewrote it again. See N3 |
| `src/superclaude/cli/install_hooks.py`, `src/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 14:42:10-14:42:13 | **no** (`git diff --stat` and `git status` empty for them) | touched during my own full-suite run (hook tests), mtime only |

No other source, test or doc file changed after review 1. `.claude/**` mtimes are all 14:31 (the fix's `make sync-dev` rewrites every mirror); content is in sync (`make verify-sync` rc=0, section 3) and `.claude/` is gitignored. `git diff --cached --name-only` lists only `.dev/` paths (0 non-`.dev` staged files), so nothing under `.claude/` is staged. `git status` now shows 7 modified tracked files of the implementation (2 user and developer docs, the 2 `HOW-WE-WORK.md` copies, 3 tests), `perf.json`, and the untracked implementation files; none of the 7 tracked files has an mtime after review 1.

## 5. Single-surface sweep

Scope: `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/**` (SKILL.md, refs, templates, scripts), `src/superclaude/agents/issue-worker-t*.md`, and the new or changed tests. Method: grep for `\.claude/`, `~/`, `skill base`, `scripts/`, `templates/`, `refs/`, then read each hit in context.

| Location | Single-surface text | Read or lookup that breaks? | Grade |
|---|---|---|---|
| `commands/issue.md:93` | "The full behavioral specification is in `~/.claude/skills/sc-issue-protocol/SKILL.md`." | No. The activation is `Skill sc:issue-protocol` (`:89-90`), resolved by name in both surfaces; `:93` is a pointer, the same pattern as `commands/brainstorm.md:143` | not a defect |
| `SKILL.md:15` | "chosen by the command (`~/.claude/commands/sc/issue.md`)" | No: describes who invoked the skill | not a defect |
| `SKILL.md:56-60` | agent table, "Installed file" `~/.claude/agents/issue-worker-t*.md` | No: the next line `:62` names the project `.claude/agents/` copy first, and spawning goes by `subagent_type` | not a defect |
| `refs/tiers.md:37` | `E-TIER-UNAVAILABLE` message text naming `~/.claude/agents/issue-worker-t3.md` | No: an error message, not a read | not a defect |
| `SKILL.md:64`, `refs/claim.md:7`, `refs/create.md:7`, `refs/tiers.md:7`, `refs/chains.md:5`, `refs/labels.md:5` | workers "run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`" with no project copy | No for the orchestrator (it never opens `analyze.md`); the agent files the workers actually read name both (`issue-worker-t1.md:28`, `-t2.md:28`, `-t3.md:27`). `~/.claude/commands/sc/analyze.md` exists here and `.claude/commands/sc/analyze.md` exists in the checkout | minor, N1 |
| Skill-relative `refs/`, `templates/`, `scripts/` paths in SKILL.md and refs | relative to `<skill base>`, defined at `SKILL.md:22` with both surfaces; scripts run as `"<skill base>/scripts/origin_repo.py"` (`SKILL.md:68,80,92`, `refs/claim.md:14`, `refs/create.md:13`) and `"<skill base>/scripts/clickup_claim.py"` (`refs/claim.md:49`) | No | not a defect |
| Tests (`tests/skills/test_issue_*.py`, `test_clickup_claim.py`, `tests/commands/test_issue_command.py`, `tests/cli/test_issue_body_templates.py`) | `~/.claude/...` appears only inside asserted strings; every file read is under the repo (`ROOT`/`_REPO`), none under `Path.home()` | No (tests are not installed) | not a defect |

No blocking hit: every read or lookup instruction that an agent executes names a path that resolves in both a checkout and an install.

## 6. New findings

Minors m1 to m7 of review 1 are recorded and not re-checked here.

### Blocking

None.

### Minor (notes; do not fail the review)

| ID | Severity | Location | Evidence | Suggested fix |
|---|---|---|---|---|
| N1 | minor | `src/superclaude/skills/sc-issue-protocol/SKILL.md:64`, `refs/claim.md:7`, `refs/create.md:7`, `refs/tiers.md:7`, `refs/chains.md:5`, `refs/labels.md:5` | These lines tell the orchestrator that workers run `/sc:analyze` "by following `~/.claude/commands/sc/analyze.md`", naming only the installed copy. Nothing breaks: the orchestrator never opens the file, and the worker files the workers read name both copies (`issue-worker-t1.md:28`, `-t2.md:28`, `-t3.md:27`). It is an inconsistency with the dual-surface wording used everywhere else | Append "(project `.claude/commands/sc/analyze.md` in a checkout)" on those lines, as the worker files do |
| N2 | minor | `tests/skills/test_issue_worker_agents.py:123,126,142-148` | The general check is line-based: it passes when a line has any project `.claude/skills/` path, so a reversed order (M6) or a project path that names a different file (M8) passes it; only the exact-text pin of line 17 (`:163`) catches those, and only for that line. The exemption is a line-prefix match, so an installed-only lookup appended to line 11 passes all tests (M7, 35 passed). B1 itself is caught (M1, M2) | Pair each `~/.claude/skills/<path>` with `.claude/skills/<same path>` appearing after it on the line; exempt by the exact provenance span (`(`~/.claude/skills/sc-issue-protocol/SKILL.md`), with`) rather than the whole line |
| N3 | minor | `.dev/releases/current/cliEval/evidence/T02.15/perf.json` | Tracked file left modified (` M`, 549 lines) by full-suite runs (`tests/cli/eval/test_perf_home_setup.py`). Review 1 restored it after its run; it was dirty again at the start of this review, so fix round 1's full run left it modified, and my mandated run rewrote it again. It is not staged and is not part of the deliverable, but the fix report's "No other file was edited" (`05-fix-report.md:55`) does not mention it | Before committing, `git restore .dev/releases/current/cliEval/evidence/T02.15/perf.json` and do not stage it |

## 7. Verdict

**PASS** (with notes): B1 is fixed, 0 blocking findings, 3 new minor notes (N1 to N3).

B1: both rubric lookups (`issue-worker-t1.md:17`, `issue-worker-t2.md:17`) now name the installed and the project copy, installed first, as `CLAUDE.md:96` requires; the line-11 provenance exemption is sound. The new test fails on the old text (fix-round log and my M1/M2 mutations). Full suite 14839 passed / 0 failed, lint and sync exit 0. Only the three files the fix report lists changed in content after review 1 (plus the suite's `perf.json` side effect). The sweep found no read or lookup instruction that breaks in a checkout or an install.
