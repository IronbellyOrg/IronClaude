# Reviewer 1 brief (persona: analyzer; model class: opus)

## T1 card excerpt

# Tier 1 reflection card (UC-1, pre-execution)

hypothesis_source: inline-fallback (the orchestrator wrote this card; the plan author is also the executor class, so this card is the part most exposed to self-confirmation and is the reason Tier 2 follows)

Spec: ./source.md (snapshot of the issue 687 spec, 381 lines). Tasklist: TASK-WF-specWorktreeClea-20261120-173546.md (20 tasks, 8 phases, depth deep).

## Coverage

- Pass 1 (labeled IDs by `ID_REGEX`): 0 parsed requirements. The spec labels nothing as R-n, REQ-n, SPEC-n or T-n.
- Pass 2 (quote-pinned inference): 82 inferred rows (`coverage-matrix.md`). Every quote was checked verbatim against its cited line by `artifacts/coverage_match.py`.
- Containment match (threshold 0.6, deterministic): 74 of 82 matched, `coverage_pct_union` 0.9024, `coverage_pct` null (parsed-only is undefined), `S_dev_density` 0.0976.
- Unmapped by the lexical rule: INF-026 (command, not a skill), INF-028 (precheck exits non-zero), INF-035 (first week report only), INF-042 (rule 5 "nothing unsaved"), INF-045 (rule 8 not pinned), INF-048 (never `git worktree prune`), INF-058 (never overwrite a folder), INF-079 (registered where the repo lists commands). The orchestrator believes each is covered in substance (Tasks 14, 18, 18, 6, 6, 2, 9, 15) but the rule is lexical and this belief is unchecked by anyone else.

## Structural signals

- S_scope 20 tasks, S_domains 5 (code, tests, docs, config, infra-like automation), S_dev_density 0.0976.
- Step 1B.2b fired: `inferred_count` 82 is greater than `parsed_count` 0, so `coverage_degraded: parsed-sparse` forbids the Tier 1 stop. Tier 2 is routed by the table-wide pre-filter and by rule 4 (S_domains at least 3).

## Self-identified risks (the orchestrator's own doubts about its plan)

- R1 Order and dependencies. Task 5 (GitHub facts) needs the Orca record from Task 3 and the git record from Task 4; Task 7 (test support) is placed after Task 6 although the fixtures it builds are used by Tasks 3 to 5 only in their acceptance criteria. A reviewer should check that no task's acceptance criteria depend on something a later task creates.
- R2 Scaffolding. Task 2 tells the executor to leave the four verb bodies as stubs that exit 64 until Tasks 11 and 12. The plan says nothing ships as a stub; check that Task 12 really replaces every stub and that its acceptance criteria prove it.
- R3 Safety. The user's run-level safety rule forbids any real removal, any real automation and any push to the evidence repo. Task 1 runs `branch-landed.sh` (which runs `git fetch`) on a real repository and Task 20 runs the script against the real workspace (which runs the same check per worktree through `gh` and `git fetch`). Check whether those are consistent with "dry run only" and with the Constraints section.
- R4 Unbuilt requirement. The spec says `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" with no format. The plan records it as not built (Constraints, Task 12). Check this is an honest reading and not a silent drop.
- R5 Decisions made by the plan where the spec is silent: `/sc:worktrees` on the never-as-worker list (Task 16), the stop outside an IronClaude checkout (Task 14), the default `--out` folder, `/sc:closeout` untouched, the run-evidence pointer prepared as text only (Task 19). Check each for a hidden conflict with a spec section or a pinned test.
- R6 The "never delete a file" constraint (no `unlink`, no `rmtree`, flock lock files left in place, failed scratch folders left in the evidence clone). Check it does not make a spec requirement impossible (for example the archive step 2 "build the folder in a scratch folder" and step 7 repeat runs).
- R7 Test count. The spec asks for about 35 cases in four groups; the plan spreads them over Tasks 7, 8, 10, 13, 18. Check that every bullet of source section 9 lands in some task's body or acceptance criteria.
- R8 Hand-written fixtures for `orca` replies (Task 7) may not match the real Orca output; the only real check is the dry run in Task 20.

## Recommendation

Hand the plan to `/sc:implement` only after a reviewer has confirmed R1, R3 and R7. No change to the plan has been made from this card.

calibration: pending (blind calibration runs in Wave 1D)

Persona lens (analyzer): root cause and deviation. Hunt for contradictions between the plan and the spec, ordering and dependency errors, unsafe steps, and facts about the repository that are wrong. Read the spec at .dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/source.md and check the plan's repo claims (file paths, line numbers, test names such as _POST_REFRESH_ADDITIONS, NEVER_AS_WORKER, _OTHER_COMMANDS, the branch-landed.sh behaviour) against the repository.

Instructions for this reviewer (read-only: do not run commands, do not edit any file; audit the evidence in this brief and what you can Read, Grep or Glob). You are reviewing a PLAN (the tasklist) against its SPEC before anyone implements it. Find concrete defects: a spec requirement the plan drops or contradicts, a task whose acceptance criteria cannot be met or depend on something a later task creates, a task that would make an executor break the constraints, a wrong repo fact (file, line, symbol, test name) that you can check with Read/Grep, or a safety problem. Grade each finding: BLOCKING only if correcting it would change a named decision, required behaviour, outcome or acceptance check the plan rests on, or a required deliverable is absent, or following the plan would lose or expose data, break a safety boundary or act outside the stated scope; MEDIUM if it is a real weakness nothing named rests on; NOTE if it is wording or form only. Every finding needs file:line evidence with a short verbatim quote, the consequence, and a suggested fix. A zero-finding result is valid only if you state what you checked. Do not invent findings. Return ONE card as plain markdown with: a `verdict:` line (PASS or FAIL; FAIL only with at least one BLOCKING finding), `self_reported_confidence:` (0.00 to 1.00), `reviewer_model_self_report:` (the model you run as), then `## Findings` (numbered F1, F2 ... each with severity, claim, evidence, consequence, fix), `## Checked and found sound` (bullets with what you verified), `## Coverage gaps` (spec requirements you think the plan misses, with source.md line). Plain English, no em or en dashes.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-20T17:38:06Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687

### .dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/TASK-WF-specWorktreeClea-20261120-173546.md:1-274

````` markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-specWorktreeClea-20261120-173546
version: "1"
priority: Medium
created_date: "2026-11-20"
---

# Daily cleanup of merged worktrees (issue 687): script, command, automation definition and tests

Source: ./source.md
Goal: A person can run `/sc:worktrees` (list, archive, retire, prune) to remove git worktrees of IronbellyOrg repos only when all eight rules of source section 6 hold, after saving untracked and ignored `.dev/` files to the evidence repo and closing the worktree's own Orca terminals; a switched-off Orca automation definition exists for the daily report-only run; the whole feature is proved by tests that use only throwaway repositories and fake `gh`, `git` and `orca` replies.

## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.

## Phase 1: Prove what can be proved, and lay the script foundation

## Task 1: Write the proofs record for source section 11

Create `.dev/research/worktree-cleanup-proofs.md` with one row for each of the ten unproved items of source section 11 (columns: item, status PROVEN or NOT PROVEN, evidence or reason, fallback used by the script). Prove only what needs no write to a real worktree, Orca, GitHub or the evidence repo: item 3 (read how `superclaude install` copies the `sc-closeout-protocol` skill under `src/superclaude/cli/`, whether #683 added a command-line verb for the landed check, and run `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh` once on pull request 700 and once on a number that does not exist, to see `MERGED` and `NONE`); item 4 (write the definition: a process that exited meanwhile is ignored, another user's entry is noted and ignored, any other error keeps everything); item 9 (read-only: take the branch and folder names from `git worktree list --porcelain` of this checkout and show which numbers of 2 to 4 digits the rule would extract). Mark items 1, 2, 5, 6, 7, 8 and 10 NOT PROVEN, because proving them needs a real Orca removal, a real push, an automation or a terminal close, which the safety constraint forbids; for each, copy the fallback of source section 11 and say what the code does because of it (items 1 and 2: remove an Orca-listed worktree with `orca worktree rm` without `--force` and read back, a refusal keeps it; item 5: stop with "saved copy failed: no credentials in the environment" when the push fails; item 6: the automation definition says the `skipped_precheck` result is UNVERIFIED; item 8: keep `0 8 * * *`; item 10: an unconfirmed or failed close keeps the worktree). Also record in the file the answer the script will use for item 3, so Task 5 can follow it: look for `branch-landed.sh` first at `~/.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh`, then at `.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh` under the checkout, then (labelled in-checkout fallback) at `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh`, and when none exists run `gh pr view <N> --json state,mergedAt` for the same MERGED-or-not answer and keep the worktree when it cannot tell.

Acceptance criteria:
- `.dev/research/worktree-cleanup-proofs.md` exists, has exactly ten rows, and every row states PROVEN or NOT PROVEN with the command or reason and the fallback.
- Items 3, 4 and 9 are PROVEN with the output of the commands run (the `MERGED` line for pull request 700 and the `NONE` line for the missing number appear verbatim); items 1, 2, 5, 6, 7, 8 and 10 are NOT PROVEN with the safety reason.
- The file names the branch-landed lookup order and the `gh pr view` fallback exactly as written above.
- No real worktree, Orca automation, Orca terminal, remote branch or evidence repo was touched to produce it (no `--apply`, no `orca worktree rm`, no push).

## Task 2: Create the script skeleton with the allowlisted command runner

Depends on: Task 1

Create `scripts/worktree_cleanup.py` (new, Python standard library only; modelled on the stdlib style of `scripts/merged_pr_log.py`, which has `parse_args` and `main`). Top of the file: Jay Wedgeworth's Apache-2.0 notice block (source `github.com/Simple-With-Us/AI-Fleet-Coordinator`, copyright 2026 Jay Wedgeworth, rules adapted from `scripts/fleet_lanes/retire.py`, `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh`, what was changed: see `scripts/worktree_cleanup_PROVENANCE.md`, which Task 19 writes). Then a plain-English module docstring and these parts: constants (idle floor from `WORKTREE_CLEANUP_IDLE_DAYS` default 7, `RUN_EVIDENCE_REPO` default `IronbellyOrg/run-evidence`, `RUN_EVIDENCE_DIR` default `~/workspaces/run-evidence`, archive part size 85 MB as a module constant so tests can lower it, owners `IronbellyOrg` and `IronbellyGroup`, the name guard `orca-port-`, `orca-recipe-`, `orca-pristine-` as prefixes and `orca-old-patched` as an exact name, the fixed build-output list of source section 6 rule 5, exit codes 0, 64, 69); one `Runner` class that is the only way the script starts an outside program (argument list, no shell, `GH_TOKEN` passed only through the environment of `gh` and `git push`) with a `check_allowed` step, adapted from Jay's runner, that refuses before any process starts: `--force` or `-f` on `orca worktree rm` or `git worktree remove`, `git branch -D`, `rm`, `git worktree prune`, `git push` with a delete flag or a `:ref` refspec, `git push` when the working folder is not the evidence clone, and `git clean` unless it is exactly `-f -x --` (run through `xargs -0` with `GIT_LITERAL_PATHSPECS=1`) and every path on its standard input is one of the paths registered as saved and verified (the registration call is added in Task 11); the runner records every command (argument list and working folder) in a list and has one overridable `_execute` hook so tests can answer `gh`, `orca` and `branch-landed.sh` from recorded shapes while real `git` runs on throwaway repos. Add `parse_args` and `main(argv, runner=None)` with the four verbs `list`, `archive <worktree>`, `retire <worktree>` and `prune`, the flags `--apply` and `--out <dir>` (default `~/.local/state/worktree-cleanup`, chosen so nothing is written inside any worktree), dry run as the default, and the verb bodies as stubs that exit 64 with "not built yet" until Tasks 11 and 12 fill them in. The file never reads `~/.config/gh/hosts.yml` or `~/.env`.

Acceptance criteria:
- `uv run --no-project python scripts/worktree_cleanup.py --help` lists the four verbs and the two flags; `main(["list"], runner=...)` can be called from a test with an injected runner.
- `Runner.check_allowed` raises a dedicated refusal error for each banned shape listed above before any process starts (these refusals are asserted in Task 13's recorder tests).
- An `ast` scan of the file finds only standard library imports and no call to `os.remove`, `os.unlink`, `shutil.rmtree` or a command named `rm`.
- The Apache-2.0 notice block and the pointer to `scripts/worktree_cleanup_PROVENANCE.md` are at the top of the file.

## Phase 2: Facts from Orca, git and GitHub

## Task 3: Add the read-only Orca facts

Depends on: Task 2

In `scripts/worktree_cleanup.py` add the Orca reads of source section 5 ("Facts come from three places"), each through the `Runner` and each returning a small typed record: `orca repo list` (the repos Orca knows, with their folders), `orca worktree ps --json` (path, `lastActivityAt`, `isPinned`, `liveTerminalCount`, `linkedPR`, `comment`, and the worktree id used as `id:<id>`), `orca reference list --worktree <selector>` and `orca terminal list --worktree <selector>`. Orca's `linkedPR` is kept only as a hint and is never used as the authority for rule 2 (source section 11, item 7). A failed or unparseable Orca read is reported as "Orca unavailable" for the facts it would have given; it never aborts the run and never makes a worktree removable: a worktree Orca does not list is treated as not in Orca (it is still found through git, Task 4), and when `orca repo list` itself fails the repo list falls back to the current checkout's repo only and the table says so. The script only ever runs the read verbs here; the close and remove verbs are added in Task 11.

Acceptance criteria:
- A parse function for each of the four reads accepts the recorded shape saved under `tests/worktree_cleanup/fixtures/` by Task 7 and returns the fields named above; a malformed reply yields "Orca unavailable", not an exception.
- No function in this task issues `orca terminal close` or `orca worktree rm`; the recorder test of Task 13 shows only read verbs for these reads.
- `linkedPR` appears in the returned record but no rule function reads it as proof of a merge.

## Task 4: Add the read-only git facts, local state classification and the process scan

Depends on: Task 3

In `scripts/worktree_cleanup.py` add, through the `Runner`: discovery of worktrees as `orca repo list` folders plus `git worktree list --porcelain` run in each repo, so worktrees Orca does not list are found, wherever they sit (source section 3, "In scope"); per worktree the main-checkout flag (first porcelain entry), locked flag, folder present or missing, branch or detached HEAD, `origin` owner (IronbellyOrg or IronbellyGroup, from `git remote get-url origin`), `git rev-parse HEAD`, `git status --porcelain` split into changed tracked files, untracked files outside `.dev/`, untracked files under `.dev/`, and the ignored files from `git status --porcelain --ignored` split into build output and generated copies (the fixed list of source section 6 rule 5, matched on path parts), ignored files under `.dev/`, and unknown ignored names; the idle time as the newest of the modification times of `HEAD`, `index` and `logs/HEAD` in the worktree's own git folder, the last commit time, and Orca's `lastActivityAt` when Orca lists it, plus the creation age; a `.worktree-keep` file check; a git operation in progress check (merge, rebase, cherry-pick, revert, bisect, `index.lock` in the worktree's git folder); a nested checkout check (a `.git` file or folder below the top of the worktree); and the process scan: read `/proc/<pid>/cwd` for every entry, ignore an entry that exited meanwhile, note and ignore an entry of another user, and treat any other error as "scan failed" which keeps every worktree (source section 11, item 4); the `/proc` root is a parameter so tests can pass a fake. The size of each worktree is computed by walking the folder read-only. The script's own folder is compared by real path. The name guard of source section 3 is anchored at the start of the folder name, so `coder-orca-port` is not caught.

Acceptance criteria:
- On a throwaway repository built by Task 7, each fact is returned correctly for a clean worktree, one with a changed tracked file, one with an untracked file outside `.dev/`, one with untracked and ignored files under `.dev/`, one with an ignored environment file outside `.dev/`, and one with only build output.
- The process scan returns "scan failed" for an unreadable-for-another-reason entry in a fake `/proc` and ignores a vanished one and another user's one.
- `orca-port-evidence`, `orca-recipe-x`, `orca-pristine-y` and `orca-old-patched` are on the name guard and `coder-orca-port` is not.
- No git command in this task changes the repository (the recorder test of Task 13 shows read verbs only: `worktree list`, `status`, `rev-parse`, `remote get-url`, `log`, `ls-files`).

## Task 5: Add the GitHub facts: own pull request, landed check and issues

Depends on: Task 4

In `scripts/worktree_cleanup.py` add, through the `Runner`: the pull request of a worktree's branch with `gh pr list --head <branch> --state all --json ...` run with the repo named explicitly (`--repo <owner>/<repo>` taken from that repo's `origin`; never the `{owner}/{repo}` placeholder), choosing the newest merged one when there are several and recording number, state, `headRefOid`, author login, merge date, title, body, closing references and branch; then the landed check by number: run `branch-landed.sh <PR>` with the repo's main checkout as the working folder (the script reads `origin` of the current directory and needs `jq` and one `git fetch`), locating the script by the order recorded in Task 1 (installed copy under `~/.claude/skills/sc-closeout-protocol/scripts/`, then the checkout's `.claude/skills/...`, then the in-checkout `src/superclaude/skills/...` labelled fallback, then `gh pr view <N> --json state,mergedAt` for the same MERGED-or-not answer); the result must be the token `MERGED` for rule 2 to pass, and `UNKNOWN`, a failed call or a missing `jq` means keep. Add issue collection for rule 4 from every place of source section 6 rule 4: the pull request's closing references, every `#N` in the pull request title and body that is an issue (a number that is a pull request is ignored, resolved in the right repo, so Coder #373 is an issue and IronClaude #373 is a merged pull request), a number of 2 to 4 digits in the branch name or folder name that must exist as an issue in the same repo, Orca's card comment (for example `sc:issue IronbellyOrg/IronClaude#669`), its `linkedIssue` and `orca reference list`; each issue's state is read with `gh issue view <N> --repo <R> --json state`; any lookup failure is "issue lookup failed" which keeps the worktree; no issue found passes with "none found". Rule 3 data: whether HEAD equals the pull request's `headRefOid` or is its ancestor (`git merge-base --is-ancestor` run read-only) and how many commits come after it.

Acceptance criteria:
- Every `gh` call in this task carries an explicit `--repo <owner>/<repo>` argument (asserted by the recorder test of Task 13); no call uses `gh api` with a placeholder.
- A squash-merged pull request whose commits are not on the base is returned as merged from pull request state, with no commit-ancestry question asked.
- Issue numbers come back from all four places of the spec's test list (closing reference, `#N` in the body, a number in the branch name, Orca's card comment), with pull request numbers dropped and the repo resolved per number.
- With `branch-landed.sh` absent from all three places, the `gh pr view` fallback answers, and when that also fails the result is "landed check said UNKNOWN".

## Phase 3: The eight rules and their tests

## Task 6: Implement the eight rules in order, with their reasons and the table row

Depends on: Task 5

In `scripts/worktree_cleanup.py` add one decision function that takes the facts of Tasks 3 to 5 plus a save state (`not needed`, `needed`, `verified`, `failed: <why>`) and returns a decision (`removable` or `kept`), the first failed rule and its plain-English reason, and the table row. Apply the eight rules of source section 6 in that order with exactly the reasons shown there: rule 1 (main checkout, not our repo, this is where the script runs, locked, folder missing reported only, name guard, detached HEAD), rule 2 (no pull request, open, closed not merged, landed check UNKNOWN), rule 3 (N commits after the pull request, HEAD is not the pull request's head), rule 4 (issue open, issue lookup failed), rule 5 (changed tracked files, untracked files outside `.dev`, ignored local state with names, `.dev` files allowed only when the save state is `verified`, else "saved copy failed: <why>"), rule 6 (a process inside tolerated only while the worktree has Orca terminals open; otherwise "in use: process <pid> (<name>)"; a failed `/proc` scan keeps everything; holds another checkout; git operation in progress), rule 7 (idle fewer than the floor days, created within the floor days), rule 8 (pinned in Orca, keep file present). Every rule fails closed: a fact that could not be read keeps the worktree. In a dry run a worktree that passes with untracked or ignored `.dev/` files shows `removable` with the saved-copy cell `needed`, and one with Orca terminals open shows the note "its Orca terminals will be closed first". The table row has the columns of source section 3: repo, folder, branch, in Orca, pull request and state, issue(s) and state, idle days, size, saved copy, decision and reason. Add the table renderers (markdown and the same rows as JSON).

Acceptance criteria:
- A pure function (no process started) returns the same decision for the same facts, so tests can call it with hand-built facts.
- For every rule, a worktree that fails only that rule is kept with that rule's reason, and the reasons are the strings of source section 6.
- A worktree with only Orca terminals open and a process inside passes rule 6 in the first pass and carries the note "its Orca terminals will be closed first"; a process inside with no Orca terminal fails rule 6.
- The markdown table has the eleven columns above and the JSON has the same rows.

## Task 7: Build the test support and the "facts the tests keep true" checks

Depends on: Task 6

Create `tests/worktree_cleanup/__init__.py`, `tests/worktree_cleanup/conftest.py`, `tests/worktree_cleanup/fixtures/` and `tests/worktree_cleanup/test_git_facts.py` (new; layout as `tests/merged_pr_log/` has `__init__.py`, `fixtures/` and one test module that loads the script with `importlib.util.spec_from_file_location`). `conftest.py` provides: a loader of `scripts/worktree_cleanup.py`; a recording runner built on the script's `Runner` that answers `gh`, `orca` and `branch-landed.sh` from canned replies and runs real `git`, `tar` and `xargs` only inside throwaway folders under `tmp_path`; a builder for a throwaway repository with real linked worktrees (a clean one, one with a tracked edit, one with untracked and ignored `.dev/` files, one with an ignored environment file, one with only build output, one with a detached HEAD, a locked one) whose `origin` points at a local bare repository, and a second local bare repository standing in for the evidence repo; a fake `/proc` builder. `fixtures/` holds JSON in the recorded shape of `gh pr list`, `gh pr view`, `gh issue view`, `orca repo list`, `orca worktree ps --json`, `orca reference list` and `orca terminal list`; a README line in the module docstring says the shapes are hand-written from the spec and the Orca help, not literal captures (as `tests/merged_pr_log/test_merged_pr_log.py` says). `test_git_facts.py` keeps true the facts of source section 9 "Facts the tests keep true" in a throwaway repository: `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file and removes one that holds only ignored files; `git branch -d` refuses after a squash merge and the script's removal reports "kept" not an error; `git clean -f -x --` with literal pathspecs removes exactly the listed files (including a name with a space) and leaves unlisted untracked and ignored files and tracked files alone. Use obvious placeholders for any token-shaped value, never a real one.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_git_facts.py -v` passes using only `tmp_path` repositories; no test touches a real worktree.
- The recording runner exposes the full list of commands it was asked to run, and refuses (raises) any command the real `Runner.check_allowed` would refuse.
- The fixtures folder holds one recorded shape for each of the seven replies listed above.
- The three git facts are asserted, including the file name with a space.

## Task 8: Write the removal and keep tests for the eight rules

Depends on: Task 7

Create `tests/worktree_cleanup/test_rules.py` with the first test group of source section 9, each case failing if its rule is removed. Removable case: merged own pull request, HEAD is its last commit, clean, idle 8 days, no process, no Orca terminal, issue closed, so the decision is `removable`. Kept cases, each asserting the reason text, for: the main checkout; a repo that is not ours; the folder the script runs in; a locked worktree; a missing folder (reported, never pruned); a detached HEAD; a name starting with `orca-port-`, `orca-recipe-` or `orca-pristine-` (while `coder-orca-port` is not caught); no pull request; an open pull request; a pull request closed without merging; a landed check that says `UNKNOWN` or fails; a commit after the pull request's head; a HEAD that is not the pull request's head; an issue that is open through each of the four places (closing reference, `#N` in the body, a number in the branch name, Orca's card comment); an issue lookup that fails; a changed tracked file; an untracked file outside `.dev/`; an ignored environment file outside `.dev/`; an unknown ignored name; a process with its working folder inside; a failing `/proc` scan (keeps every worktree); a process inside a worktree that has no Orca terminal open; a merge, rebase, cherry-pick and `index.lock` in progress; idle 6 days; created 3 days ago; pinned; a keep file. Also: ignored build output and generated copies (`__pycache__`, `.venv`, `.codegraph`, `uv.lock`, the `.claude/agents`, `commands`, `hooks`, `skills` and `templates` copies) are allowed and not a reason to keep; a squash-merged pull request whose commits are not on the base is judged landed from pull request state; a pull request that is merged but whose branch was later reused for new commits keeps the worktree.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_rules.py -v` passes and has at least one test for every item listed above.
- Mutation check by hand for one rule per group: temporarily making rule 4 always pass (or rule 3, or rule 6) makes at least one test in this file fail.
- Every kept case asserts the plain-English reason, not only the decision.

## Phase 4: Save before removing

## Task 9: Implement the `.dev` archive step with the names-only secret check

Depends on: Task 6

In `scripts/worktree_cleanup.py` implement source section 7 as one function used by the `archive` verb and by `retire` and `prune`. Order: needs the merged pull request of rule 2 and refuses without one; syncs the local clone of the evidence repo (`RUN_EVIDENCE_DIR`, cloned when missing with the repo from `RUN_EVIDENCE_REPO`; `git fetch` and fast-forward); builds the folder inside a scratch folder in that clone and, when complete, renames it into place (a failed save leaves its scratch folder, named in the log, and deletes nothing); copies untracked files that are not ignored at their relative paths into `files/`; packs the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of the 85 MB module constant when larger; writes `saved-paths.txt` (one exact path per line: every untracked file copied and every file inside the archive, read back with `tar -tzf`, files only) and `MANIFEST.md` (source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, SHA-256 of each archive part and of `saved-paths.txt`); commits with the message `archive(<repo>): <date> pr<N> <subject>`; runs `git fetch`, rebases onto `origin/main` when it moved, pushes, and on a refused push repeats from the fetch up to 3 times then fails with "saved copy failed: push refused"; verifies with `git fetch`, the same file count on `origin/main` and `git diff --quiet origin/main -- <folder>`, and prints `VERIFIED <folder> files=<n>`; the push uses `git -c credential.helper='!gh auth git-credential'` with only the environment `GH_TOKEN` and a failure to authenticate reads "saved copy failed: no credentials in the environment". Folder convention: `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/` with the UTC merge date and the branch name without the author prefix, slashes turned into hyphens. A repeat run verifies an existing folder again and checks every file now in the worktree is covered; new files go to a second folder with suffix `-r2` then `-r3`; an existing folder is never overwritten. Before copying, a names-only secret check scans the files to be saved for token-shaped content and secret-looking file names; a hit stops the save with "possible secret in <file name>" and never prints or logs the matched value. The step reads and copies and never edits anything inside the worktree. The function returns the verified folder path and the set of saved paths so Task 11 can register them with the runner.

Acceptance criteria:
- Run against a throwaway worktree and a local bare repository, the folder appears at `<repo>/<author>/<date>_pr<N>_<subject>/` with `MANIFEST.md` (all fields above), `files/`, `ignored.tar.gz` and `saved-paths.txt`, and `VERIFIED <folder> files=<n>` is returned.
- A refused push (three times), a folder that differs after the push and a failed copy each return a failure reason beginning "saved copy failed" and leave the worktree untouched.
- With the part size lowered by the test, an ignored archive is split into parts that join back to the same bytes; a second run with new files writes `-r2` and the first folder is byte-identical afterwards.
- A file containing a token-shaped string stops the save, the message names the file, and the string itself appears nowhere in the output, the log or the evidence clone.

## Task 10: Write the archive step tests

Depends on: Task 9, Task 7

Create `tests/worktree_cleanup/test_archive.py` covering the archive group of source section 9: a worktree with untracked and ignored `.dev/` files produces the folder at `<repo>/<author>/<date>_pr<N>_<subject>/` with `MANIFEST.md` carrying every field, `files/` and `ignored.tar.gz`, and `VERIFIED` is printed before anything else would happen; a push refused three times, a folder that differs from the remote after the push, and a failed copy each show "saved copy failed" with the cause; an ignored archive larger than the part size is split into parts that join back to the same bytes (lower the module constant to a few kilobytes); an existing folder is never overwritten and a repeat run verifies it and writes `-r2` when new files appeared; two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry (two clones of the local bare repository, the second pushing after the first); a possible secret in a file to be saved keeps the worktree, names the file and never prints the value. Build any token-shaped test string at run time from two pieces (for example a prefix plus repeated characters) so no secret-looking literal is committed, and assert the assembled value is absent from captured output and from every file of the evidence clone.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_archive.py -v` passes using only `tmp_path` repositories and local bare remotes.
- Each of the six bullets above has at least one test, and the secret test asserts the value never appears in stdout, stderr, the log or the clone.
- No test in the file pushes to a network remote or reads a credential file.

## Phase 5: Removal pipeline and the four verbs

## Task 11: Implement the removal pipeline: terminal close, second check, exact-path clear, removal, branch, read back

Depends on: Task 9

In `scripts/worktree_cleanup.py` implement steps 1 to 7 of source section 3 ("What a removal is, in order") for one removable worktree under `--apply`, each step failing closed with the reason shown: save (the archive step of Task 9 when the worktree holds untracked or ignored `.dev/` files; without `VERIFIED` stop); close the Orca terminals only when it has any, only after every other rule passed and the save is verified, with `orca terminal close --worktree id:<id> --all` (an `unverifiable` or failed close keeps the worktree: "Orca terminal close not confirmed"); the second check after the close, re-reading `git status`, the untracked and ignored lists, HEAD against the pull request's head and the process scan, where any change since the save keeps it ("changed since the terminals were closed") and any process still inside keeps it ("a process is still inside after its Orca terminals were closed"); clear exactly the saved files by registering the verified `saved-paths.txt` paths with the `Runner` and running `git clean -f -x --` on those paths through `xargs -0` with `GIT_LITERAL_PATHSPECS=1`, never a path outside the list, never `-d`, never a tracked file; remove the worktree (`orca worktree rm --worktree id:<id>` without `--force` when Orca lists it, else `git worktree remove <path>` without `--force`, run from the repo's main checkout and never from inside the worktree, and a refusal keeps it with the refusal text); remove the local branch with `git branch -d` only (check first whether Orca already removed it; a "not fully merged" refusal after a squash merge is reported as "branch kept", not an error); then read back that the folder is gone and that neither `git worktree list` nor `orca worktree list` shows it. A worktree with tracked edits or a commit after the pull request is never archived, never has terminals closed and is never cleared (decision 2). In a dry run none of these steps runs.

Acceptance criteria:
- The order of recorded commands in a test run is: archive commands, `orca terminal close`, the re-check reads, `xargs -0 git clean -f -x --`, the removal, `git branch -d`, the read-back reads.
- `git clean` is issued only after `VERIFIED` and only with paths from `saved-paths.txt`; a path not in the list is refused by the runner before any process starts.
- No recorded command contains `--force`, `-D`, `rm`, `worktree prune`, a remote delete or a push outside the evidence clone.
- A worktree with a tracked edit, or a commit after the pull request, produces no archive, no terminal close and no clear.

## Task 12: Implement the four verbs, the per-repo lock, the output files and the exit codes

Depends on: Task 11

In `scripts/worktree_cleanup.py` fill in the verb bodies: `list` prints the table for every worktree of every repo of ours and never removes; `archive <worktree>` runs only the archive step of Task 9 on one worktree (its help text states that the patch-and-bundle save of tracked edits or later commits mentioned in source section 7 is not built); `retire <worktree>` removes one worktree under `--apply` after the archive step when needed, must be run from outside the worktree, accepts a path or a unique folder name and exits 64 for an unknown or ambiguous selector or a worktree that is not removable; `prune` runs the same decision code on all worktrees in the same run and, with `--apply` only, removes the removable ones through Task 11, while without `--apply` it prints the table and writes `<out dir>/prune-<UTC timestamp>.md` and the `.json` of the same rows. One lock file per repo in the output folder using `fcntl.flock` with a non-blocking exclusive lock and no file deletion: a run that cannot take a repo's lock skips that repo and says "another run holds the lock". Print one summary (how many removed, kept and failed, and the first reason of each kept group). Exit codes: 0 when the run completed, 64 for a usage error or a `retire` of a worktree that is not removable, 69 when a lookup or a removal failed (the table still shows what happened). A second run after a removal finds nothing more to do. Folders that are not git worktrees of our repos never appear. No output names an agent or a model.

Acceptance criteria:
- `list` and `prune` without `--apply` record no removal command; with `--apply`, only rows marked removable are processed.
- Two runs started against the same repo cannot both remove the same worktree (the second reports the lock); a run after a successful removal reports nothing to do.
- The three exit codes behave as described (0 completed, 64 usage or non-removable `retire`, 69 lookup or removal failure) and the summary line carries the three counts.
- `prune` writes both output files under `--out` and writes nothing inside any worktree.

## Task 13: Write the pipeline, terminal, safety and output tests

Depends on: Task 12, Task 8

Create `tests/worktree_cleanup/test_pipeline.py` and `tests/worktree_cleanup/test_safety.py`. Pipeline file: decision 3 (a worktree that passes every rule with Orca terminals open and a process inside is removed under `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed and the second check finds nothing changed and no process inside; in a dry run the table says "its Orca terminals will be closed first" and no terminal is closed); a terminal close that is `unverifiable` or fails keeps the worktree; a process still inside after the close keeps it; a change appearing between the save and the close (a new commit, a tracked edit, an untracked file outside `.dev/`) keeps it; decision 1 (exactly the paths of `saved-paths.txt` are cleared including a name with a space, and an unlisted untracked file, an unlisted ignored file and every tracked file survive, and a path not in the list is refused by the runner); decision 2 (a merged worktree with a tracked edit or a later commit is kept, nothing cleared, no terminal closed, nothing archived by `prune`); the removed worktree's branch is removed with `-d` and a squash-merge refusal reports "branch kept"; a second run finds nothing more to do; two runs at once do not both remove the same worktree; folders that are not git worktrees of our repos never appear in the table and are never touched. Safety file: a recorder test runs every verb on every branch through the recording runner and fails if any recorded command is `--force` on a removal, `git branch -D`, `rm`, `git worktree prune`, a push to anything but the evidence remote, a remote branch delete, a `git clean` that is not `-f -x --` followed only by lines of that worktree's `saved-paths.txt` issued after `VERIFIED`, or an `orca terminal close` for a worktree before every other rule passed and its save was verified; every `gh` call carries `--repo <owner>/<repo>`; dry run is the default and the recorded commands contain no removal; `--apply` removes only rows marked removable; no output (table, summary, log, JSON) names an agent or a model (a test greps for a fixed list of such words); no secret is printed or written and the script never opens `~/.config/gh/hosts.yml` or `~/.env` (patch `open` and `Path.read_text` to fail on those paths); `GH_TOKEN` is read from the environment only; each refusal shape of `Runner.check_allowed` from Task 2 raises.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_pipeline.py tests/worktree_cleanup/test_safety.py -v` passes.
- Mutation check by hand: removing the `VERIFIED` precondition, or letting a path outside the list through, makes a safety test fail; removing the second check makes a pipeline test fail.
- The recorder test inspects the commands of every verb (`list`, `archive`, `retire`, `prune`, with and without `--apply`), not only `prune`.
- The tests together with Tasks 8 and 10 cover every case of source section 9 (about 35 cases in four groups).

## Phase 6: The command and its registrations

## Task 14: Add the `/sc:worktrees` command file and its static test

Depends on: Task 12

Create `src/superclaude/commands/worktrees.md`, modelled on `src/superclaude/commands/closeout.md` (frontmatter with name `worktrees`, version, description, category `workflow`, complexity, `mcp-servers: []`, personas, and `argument-hint: "<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"`; sections Triggers, Usage, Options, STOP rules, Examples, Outputs, Boundaries). It is a thin command and a command, not a skill (source section 5): it runs `uv run --no-project python scripts/worktree_cleanup.py <verb> ...` from the top of the current git checkout (`git rev-parse --show-toplevel`) and prints the table; no skill is activated. Decision made by this plan because `scripts/` does not install with the command: when `scripts/worktree_cleanup.py` does not exist at the top of the current checkout, the command stops, runs nothing and prints "`/sc:worktrees` runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`". It passes `--apply` only when the person typed it, never adds `--apply` or any force flag, and says in Boundaries that it never merges, never pushes to a source repo, that removal needs `--apply`, and (as `src/superclaude/commands/sweep.md` does in its line 18) that it is for a person only and is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`. Plain English, no em or en dashes, no `src/superclaude/...` path in the text (the repository rule for installed primitives). Then create `tests/commands/test_worktrees_command.py` modelled on `tests/commands/test_closeout_command.py` (static tests of the command file text).

Acceptance criteria:
- `tests/commands/test_worktrees_command.py` passes and asserts: frontmatter fields and the exact `argument-hint`, the four verbs and the `--apply` and `--out` options in the Options table, the outside-a-checkout stop sentence, that none of `--force`, `--yes` or `--unattended` appears as an option, that no `src/superclaude/` path appears, and that the file has no em or en dash.
- `make sync-dev` copies the command to its dev copy and `make verify-sync` is clean for it (the dev copy is gitignored and is not staged).
- `superclaude install`'s glob in `src/superclaude/cli/install_commands.py` picks the file up with no list edit (no change to that file).

## Task 15: Register the command in the routing guide and its pinned tests

Depends on: Task 14

Edit `src/superclaude/core/HOW-WE-WORK.md`: add a `/sc:worktrees` row at the end of the table between the `<!-- other-commands:v1 -->` markers (after `/sc:sweep`), stating when to use it (remove merged worktrees whose pull request is merged, issue closed and idle 7 days, `list` by default, `--apply` to remove, saves `.dev` files to the evidence repo first, for a person, never a worker) and carrying the one line that answers item 4 of #289 ("when to remove a worktree after its pull request merges": after the pull request merges and every rule of the cleanup holds). Edit `tests/core/test_how_we_work_routing_table.py`: add `"sc:worktrees"` to `_OTHER_COMMANDS` (line 27). Edit `tests/recommend/test_routing_refresh.py`: add `"worktrees"` to `_POST_REFRESH_ADDITIONS` (line 36), and extend the comment above it with "and issue #687 adds /sc:worktrees". Then copy the whole guide byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; the level-table block between `<!-- level-table:v1 -->` and `<!-- /level-table -->` is unchanged, so `src/superclaude/core/CLAUDE.md` is not edited (confirm the block is identical in both).

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py -v` passes.
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- The new row contains the `#289` item 4 answer and the words "never a worker".

## Task 16: Put `/sc:worktrees` on the never-as-worker list

Depends on: Task 14

Decision made by this plan: the command closes terminals and removes work, so no worker is ever dispatched to it. Edit the never-as-worker sentence so it reads "... `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard` and `/sc:worktrees`, plus `/sc:pr-submit` ..." in `src/superclaude/core/WORKER-CONTRACT.md` (line 23) and in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (line 982), and make the same change to the pinned phrase in `tests/skills/test_worker_contract.py` (the `never-as-worker` entry at line 89, which today ends "`/sc:sweep` and " followed by "`/sc:swarm-wizard`...") and add `"/sc:worktrees"` to the `NEVER_AS_WORKER` tuple at line 474. Read `src/superclaude/core/WORKER-CONTRACT.md` line 290 and the other mentions of the list in the developer guide and update any that enumerate the commands. `/sc:worktrees` gets no `## Unattended mode` section (the test `_check_no_unattended_sections` at line 830 requires only the named commands to have one).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -v` passes, including the parametrized never-as-worker check for `/sc:worktrees`.
- The sentence is identical in `WORKER-CONTRACT.md`, the developer guide and the pinned phrase of the test, and `src/superclaude/commands/worktrees.md` has no `## Unattended mode` heading.
- `make sync-dev` and `make verify-sync` are clean.

## Task 17: Document the command in the user guide and the changelog

Depends on: Task 14

Edit `docs/user-guide/commands.md`: add a summary-table row for `/sc:worktrees` next to the `/sc:closeout` and `/sc:sweep` rows (near line 103, columns as the neighbouring rows: link, one-line purpose, file `worktrees.md`, whether it writes: "Yes with `--apply` (removes worktrees, closes their Orca terminals, writes to the evidence repo); report only without it") and a section `### /sc:worktrees - Remove Merged Worktrees` modelled on the `/sc:closeout` section (near line 373): when to use, usage line, options table (`list`, `archive`, `retire`, `prune`, `--apply`, `--out`), the eight rules in plain English, what a removal does in order, the environment names (`GH_TOKEN`, `RUN_EVIDENCE_REPO`, `RUN_EVIDENCE_DIR`, `WORKTREE_CLEANUP_IDLE_DAYS`; no values), exit codes 0, 64 and 69, the opt-in daily automation (definition only, switched off, first week report only), and the stop outside an IronClaude checkout. Edit `CHANGELOG.md` under `## [Unreleased]`: add `### New command: /sc:worktrees and scripts/worktree_cleanup.py (issue 687)` with a short plain-English entry that also names Jay Wedgeworth's adapted rules under Apache-2.0 and the evidence repo, and states that the Orca automation is written but not switched on.

Acceptance criteria:
- The new table row and section exist in `docs/user-guide/commands.md` and the anchor in the row matches the section heading.
- The `CHANGELOG.md` entry sits under `## [Unreleased]` and mentions the switched-off automation, the Apache-2.0 notice and the evidence repo by name.
- No em or en dash in either added text; `uv run pytest tests -k "docs or commands" -q` shows no new failure from these files.

## Phase 7: The switched-off automation and the notices

## Task 18: Write the automation definition (switched off) and its test

Depends on: Task 12

Create `scripts/worktree_cleanup_orca_automation.md`, modelled on `scripts/merged_pr_log_orca_automation.md` (it has the lines `Name:`, `Trigger (UTC):`, `Status:`, then "Why the name and the trigger are what they are", "Command to run (precheck shape)", "Environment variables (names only; no value belongs in any file)", "Human steps, in order" and "When a run fails"). Name: `worktree-cleanup-daily` (never starts with `coordinator-`). Trigger (UTC): `0 8 * * *`, with the note that this is 2:00 AM Central in winter and 3:00 AM in daylight saving time, and that whether `--timezone America/Chicago` can hold 2:00 AM all year is UNVERIFIED (source section 11, item 8). Status: `written, not switched on`. The command is the precheck shape of source section 5: `bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1`, with no `--apply` in it, and the text says the skipped run shows as `skipped_precheck` and that this is UNVERIFIED in this Orca build (item 6). Add the rollout ladder (switched on by each workspace's owner; first week report only; read the tables; then the owner edits the automation to add `--apply`; the worker does none of this), the environment names without values, and "When a run fails". Create `tests/worktree_cleanup/test_automation_definition.py` asserting these fields, that the command contains `prune` and no `--apply`, ends with `exit 1`, that the name does not start with `coordinator-`, that no token value appears, and that there is no em or en dash.

Acceptance criteria:
- `scripts/worktree_cleanup_orca_automation.md` exists with Name `worktree-cleanup-daily`, Trigger `0 8 * * *`, Status `written, not switched on`, and the command above.
- `uv run pytest tests/worktree_cleanup/test_automation_definition.py -v` passes.
- No Orca automation was created, run or switched on to produce the file (definition text only).

## Task 19: Write the provenance file, the NOTICE entry and the evidence-repo pointer text

Depends on: Task 12

Create `scripts/worktree_cleanup_PROVENANCE.md`, modelled on `src/superclaude/skills/sc-closeout-protocol/PROVENANCE.md` (sections: Source, Notices in the adopted files, What changed, What this version adds, Drift review). Its "What changed" table has one row for each of the 14 rows of the table in source section 12 (kept as is, changed or dropped, with the spec's reason). The source table lists `scripts/fleet_lanes/retire.py`, `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh` with line counts from source section 12 and writes "not recorded" for blob and commit pins, because the spec records none and no pin may be invented; `branch-landed.sh` is listed as reused through `/sc:closeout`, not adopted again. It says the Apache License text is at `src/superclaude/skills/sc-closeout-protocol/LICENSE` and the upstream repository has no NOTICE file. Edit `NOTICE` (it lists `sc-closeout-protocol` as component 2 near line 30) to add the next numbered component for `scripts/worktree_cleanup.py`, naming Jay Wedgeworth, the three files whose rules were adapted, Apache-2.0 and the provenance file. Write `./artifacts/run-evidence-pointer.md` in this package with the proposed text for `tools/archive-workspace.sh` (a short pointer to `scripts/worktree_cleanup.py archive`) and the `README.md` note for `IronbellyOrg/run-evidence`, headed "not applied: a separate change in that repo, made by the owner when this merges".

Acceptance criteria:
- `scripts/worktree_cleanup_PROVENANCE.md` has 14 rows in its changed-table, each labelled with one of the three words, and no invented commit or blob pin.
- `NOTICE` has the new component entry and still lists components 1 and 2 unchanged.
- `./artifacts/run-evidence-pointer.md` exists and states it was not applied; no file of the evidence repo was changed or pushed.
- The notice block at the top of `scripts/worktree_cleanup.py` (Task 2) points at the file name used here.

## Phase 8: Dry run in the real workspace

## Task 20: Capture the dry run of the real workspace and compare the counts

Depends on: Task 12, Task 19

Run the finished script against this workspace as a dry run only: `uv run --no-project python scripts/worktree_cleanup.py list` and `uv run --no-project python scripts/worktree_cleanup.py prune --out ./artifacts/dry-run` (never `--apply`; the output folder is inside this package, not inside any worktree being judged; the script's own worktree is on the name list as "this is where the script runs"). Save the printed table and the `prune-<UTC timestamp>.md` and `.json` under `./artifacts/dry-run/` and write `./artifacts/dry-run-report.md` with: the command lines used, that `--apply` was never passed, the count of non-main worktrees of the IronClaude repo from `git worktree list --porcelain` against the number of IronClaude rows in the table, the count of rows with "in Orca" yes against the Orca list count read by the script (this session's launch guard may block typing an Orca command directly; if it does, record that and compare only through the script's own JSON), and the rows marked `removable` listed by folder and reason with a note on how they compare with the 13 of source section 2 as of the day (UNVERIFIED differences are expected and recorded as such, not forced to match). Confirm in the report that a worktree with a commit after its pull request's head, one whose issue is open and one with an ignored environment file (whichever the real data holds, else say none exists) are kept with the right reason, and that a worktree with only an open Orca terminal shows "its Orca terminals will be closed first" if one exists.

Acceptance criteria:
- `./artifacts/dry-run-report.md` exists and states that only `list` and `prune` without `--apply` were run, and the recorded command list in the `.json` output contains no removal, no terminal close, no archive and no push.
- The report gives the git count and the table count for the IronClaude repo, with any difference explained or marked UNVERIFIED.
- Every worktree of the real workspace is still present after the run (`git worktree list --porcelain` has the same entries before and after).
- No real worktree, file or Orca object was removed, moved, cleared, created or switched on to produce the report.
- The report records the results of the regression gate of source section 9 run on the finished change: the full test suite (`uv run pytest`), `make lint`, `make verify-sync`, and a scan of every new file for em and en dashes; any failure is stated, not hidden.
`````

## Coverage slice

Rows the lexical containment rule could not map (8 of 82). Full matrix: .dev/reflect/pre-TASK-WF-specWorktreeClea-20261120174527/coverage-matrix.md

| Requirement | Cite | Matched | Quote |
|---|---|---|---|
|  INF-026  |  source.md:125  | none |  It is a command, not a skill: a skill installs for everyone and would break the opt-in schedule.  |
|  INF-028  |  source.md:131  | none |  a precheck command that exits non-zero makes Orca skip the run and start no agent session.  |
|  INF-035  |  source.md:150  | none |  Clay switches it on in his workspace and for the first week it only writes the table (no `--apply`)  |
|  INF-042  |  source.md:162  | none |  Nothing unsaved is in it.  |
|  INF-045  |  source.md:165  | none |  It is not pinned and nobody asked to keep it.  |
|  INF-048  |  source.md:173  | none |  Run `git worktree prune`, because a missing folder can mean a disk is not mounted (Jay's guard); it reports such a worktree and leaves it.  |
|  INF-058  |  source.md:192  | none |  It never overwrites a folder.  |
|  INF-079  |  source.md:375  | none |  registered where the repo lists commands. Reuse the landed check of #668.  |
