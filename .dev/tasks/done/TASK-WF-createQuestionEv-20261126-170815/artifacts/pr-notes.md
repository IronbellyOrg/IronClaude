# Pull request notes for issue 834 (Task 11)

For the story agent to use in `/sc:pr-submit --monitor 3 --head clayphi/issue-834-rest --base integration --title "<title>" --body "<body>"`. Nothing under `./artifacts/` was staged before the secret scan of Task 9 was clean (`./secret-scan.txt`: clean, 0 findings in the final scan of `./artifacts/`); it is clean now, so `.dev/tasks` is to be staged (`git add .dev/tasks`) as the repository rule requires. `.claude/` and `.dev/issues/` are never staged.

## Title

`test(issue): cover the create-question rule with regression tests and controlled-run evidence (refs #834)`

## Body

### What this pull request does and does not deliver

Pull request 852 already merged to `integration` with `Refs #834` and delivered the rule text, the notes template, the command, the docs and the static wording tests in `tests/skills/test_issue_protocol.py`. There is no open pull request to continue. This pull request does only what 852 left undone, per the issue's acceptance criteria and test plan:

1. Regression tests for added-material-only, empty, contradiction-only and mixed notes, multiple contradictions sharing one question, all four categories, and a user flag preserved despite a worker's disagreement: `tests/skills/test_issue_create_question_scenarios.py` (46 tests).
2. Controlled-run evidence of the actual question and post counts across quick, standard and deep create runs: nine runs, recorded in `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/evidence-matrix.md` with the raw files under `artifacts/runs/`.

Nothing under `src/` changes. **No live issue was created and no live GitHub write was made by any run**: every GitHub call in the runs went to a stand-in `gh` that logs the call (and the posted body) and forwards nothing; the run clones had no push route and no credentials, and the other write paths were blocked (`artifacts/harness-feasibility.md`, `artifacts/harness/self-test.txt`). The live calls of this work are reads only, made outside the model sessions: the orchestrator's read of issue 834's state (`artifacts/issue-state.txt`), and the harness's and the orchestrator's read-only snapshots of recent fork activity before and after each run (the `fork_activity` block of every `summary.json`, `artifacts/scratch-scripts/pending-cleared.log`), which exist to detect any change by another party or by a run.

### Decided for this work (from the story, `.dev/issues/834/issue-summary.md`)

- Base branch is `integration`, not master. Pull request 852 (it replaced the closed 849) already merged and delivered the rule, template, command, docs and static tests; there is no open pull request to continue (lead's scope change of 26 Nov 2026, Clay's go). The older issue-834 worktree holds abandoned work and was not used.
- The claim (step 3) was done once before and was not repeated: a closed issue stops a claim, so nothing was posted or edited on GitHub. Reopening the issue is the lead's call.
- Rule from Clay for all E2 stories (26 Nov 2026): do not stop for plan approval or to ask Clay unless something is ambiguous or two sources conflict; answer what can be answered and record it here and in this pull request body. Never merge.
- Answers recorded under that rule: the first plan was regenerated after a review with blocking findings; the second review's merge did not finish, so its loud single-reviewer fallback (calibrated card 0.86, `merge_method: single-reviewer-fallback`, `adversarial_unavailable: true`) was used; the plan was repaired surgically in two fix cycles and re-reviewed (3 of 3 passed); print mode cannot ask the question, so the runs drive an interactive `claude` session in `tmux`, in an isolated home seeded from `src/`, answering the question screen by option label ("keep my wording"); two infrastructure failures (a harness crash on an unreadable path, an early finish from idle detection) were each repeated once and kept as raw records.
- The pull request uses `Refs #834` unless it delivers every criterion; it does not (below).

### Criterion verdicts for issue 834 (details and citations: `artifacts/evidence-matrix.md`, part two)

| Criterion | Verdict | Main evidence |
|---|---|---|
| AC1: notes with additions but no contradictions post directly, zero questions; all additions kept and listed in notes and final output | partly evidenced | zero questions at quick, standard and deep (`artifacts/runs/*-additions-only/summary.json:22-26`); additions kept in notes and body by the approximate record rule; the final output groups them and, from standard depth, often does not use the literal `kept without approval:` lines (finding 2) |
| AC2: a draft that changes a flag or contradicts an instruction asks exactly one question; multiple contradictions share it; the answer is applied before posting | partly evidenced (capped) | one question and the answer applied in the quick, standard and deep contradiction runs; one question naming both files in `artifacts/runs/standard-multi-contradiction/record.md:31-34`; no controlled run for a changed flag (`tests/skills/test_issue_create_question_scenarios.py:417`) |
| AC3: the notes template separates additions from contradictions, defines the four categories, requires user text and evidence; `None` is not an item | delivered by 852 | `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15`; static tests `tests/skills/test_issue_protocol.py:1461,1505` |
| AC4: rule, SKILL, template, command and docs agree; the body is never previewed; claim's direct flow and the plan boundary unchanged | delivered by 852 | both diffs over `SKILL.md`, `refs/claim.md`, `templates/launch-prompt.md` are empty (`artifacts/ac4-diffs.txt`); texts agree (`refs/create.md:86`, `SKILL.md:76,102-103`, `commands/issue.md:19,85`, `docs/designs/sc-issue-command.md:225,460`, `docs/user-guide/commands.md:357`) |
| AC5: regression coverage of the scenarios | partly evidenced (capped) | contract tests for every scenario in this pull request; controlled runs cover added-only, contradiction-only, mixed, multiple, preserved flag; empty notes and the categories reversed choice, dropped requirement and changed flag have contract tests only |
| AC6: focused tests, full suite, lint and sync pass; PR opened and monitored through `/sc:pr-submit --monitor 3` | pending, refreshed from `artifacts/gates.md` | focused 296 passed; lint passed; sync passed after `make sync-dev`; full suite `2 failed, 25535 passed, 64 skipped`, the two failures are in `tests/cli/eval/test_claude_process_adapter.py` (`No module named ruff` in this worktree's `.venv`) and not connected to this work; the pull request opening and monitoring settle the rest |

### Controlled runs in short form (expected / observed: questions, `issue create`, `issue comment`)

| Run | q | create | comment |
|---|---|---|---|
| quick additions only | 0 / 0 | 1 / 1 | 0 / 0 |
| quick contradiction | 1 / 1 | 1 / 1 | 0 / 0 |
| standard additions only | 0 / 0 | 1 / 1 | observed 0 |
| standard contradiction | 1 / 1 | 1 / 1 | observed 1 (flag-review comment) |
| standard multi-contradiction | 1 / 1 (names both files) | 1 / 1 | observed 0 |
| standard flag preserved | 0 / 0 | 1 / 1 | 1 / 1 (filed `[BUG]`, Bug, label bug; comment after the create) |
| deep additions only | 0 / 0 | 1 / 1 | observed 1 (flag-review comment) |
| deep contradiction (repeat) | 1 / 1 | 1 / 1 | observed 0 |
| deep flag preserved | 0 / 0 | 1 / 1 | 1 / 1 (same as standard; independent variant by `issue-worker-t1`) |

Secret material: evidenced by the fixture tests only (`tests/skills/test_issue_create_question_scenarios.py:464,472-479`); no controlled run, because a run would put a fake secret into a model prompt and test no more than the fixture does.

### Gates (`artifacts/gates.md`)

`uv run pytest` focused selection: 296 passed (exit 0). `make lint`: passed (exit 0; ruff 0.17.3, not the pinned 0.15.20). `make verify-sync`: failed once in the fresh worktree (empty gitignored `.claude/`), passed after `make sync-dev` (no `src/` change). `make test`: 2 failed, 25535 passed, 64 skipped, exit 2; both failures need `ruff` as a module in the worktree's `.venv` and are not connected to this work. Nothing was skipped or relaxed.

### Secret scan (`artifacts/secret-scan.txt`)

Clean after one redaction in the copy (a false positive: path-like strings in a worker's read of a repository test file) and the removal of the fake key header literal from the harness self-test (built from two string pieces). The final scan of `artifacts/` reports 0 findings.

### Live issue state (`artifacts/issue-state.txt`, read 2026-11-26T19:15:43Z)

`{"closedAt":"2026-11-26T13:14:10Z","state":"CLOSED","stateReason":"COMPLETED"}`. The issue is closed. This pull request uses `Refs #834`, not `Fixes #834`.

### Closing keyword

`Refs #834`. AC1, AC2 and AC5 are only partly evidenced and AC6 is pending, so not every criterion is delivered with run evidence. The issue is already closed; closing or reopening it is the lead's decision.

### Findings for the lead (`artifacts/evidence-matrix.md`, part three)

1. Final output form differs from `src/superclaude/skills/sc-issue-protocol/SKILL.md:103` (one literal `kept without approval: <item>` line per retained addition): quick runs follow it; standard and deep runs mostly list retained additions under a heading or fewer lines than additions. The additions are kept and listed, no question was wrongly asked. Candidate follow-up issue; `src/` was not changed here.
2. Counts matched expectations in nine of nine runs; extra comment counts (flag-review comments) were recorded as observed.
3. Models guessed `/root/.claude/...` as the home folder, got a permission error, and used the clone's `src/` copies (hashes equal `src/`).
4. Not verified: runs are single samples; the "present in" answers are approximate; answers were chosen by label in an interactive session; no non-Claude model was used; the runs read `src/` copies, not the user's installed skills.

### Process notes and follow-up candidates (not blocking)

- Protocol deviations: the Task 5 snapshot was reconstructed after the fact; Task 7 and 8 runs were executed before their ledger start lines (they changed no repository file); reviewer prompts hold file pointers instead of inline diffs; Tasks 4 and 6 needed retries (`artifacts/retries/`); the `evidence=` and `files=` paths of the ledger lines of Tasks 6 to 8 were rewritten from scratch-directory paths to the repo copies under `artifacts/runs/` and `artifacts/logs/` before the archive gate, because the archive helper accepts only repo-relative delivery paths (the same files, copied after the secret scan; the earlier ledger is saved outside the package).
- Not repaired, listed as follow-up candidates from the plan reviews: Medium M-05 to M-16 and NEW-2, Notes N-17 to N-22 and NEW-3 (`artifacts/prior-findings.md`, `artifacts/revision-log.md`), and the task notes under `artifacts/retries/T*/notes.md`.
- The branch was fast-forwarded to `origin/integration` before the gates (nothing was committed yet).

### Generator-Constraint Considered

Does not apply. The rule of `.github/workflows/contract3-generator-constraint-lint.yml` triggers on pull requests that touch `**/gates.py`, `**/structural_checkers.py` or `**/*_validator.py` (`on.pull_request.paths`, lines 26-29). `git diff --name-only origin/integration...HEAD` printed no path (nothing is committed yet), and the 505 paths of `git ls-files --others --exclude-standard` (one test file and files under `.dev/`) contain no file with those names. No `## Generator-Constraint Considered` section is needed in the body.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
