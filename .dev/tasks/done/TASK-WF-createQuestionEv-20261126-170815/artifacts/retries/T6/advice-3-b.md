model: opus (ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]) family: claude rung: top family-fallback: no GPT spawn path is verified on this install (refs/retry.md, Model ladder), so adviser B ran on the strongest reachable model
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T6.AC1 | Marked met (review-2.md:2). But the summary also carries the field `additions_in_posted_body`, which is a verbatim match on the first 40 characters and so disagrees with the record (review-2.md:9). Attempt 2's re-derivation tool (`--reanalyse`) also handed old data to `finish`, which writes the matrix control files (review-2.md:8). So the summaries could not be rebuilt safely while the deep chain was running. | Rename the field so its name says it is a first-40-characters verbatim match. Make `--reanalyse` a pure re-derivation that never writes STOP or PENDING-REVIEW. Re-derive both quick summaries only after the deep chain has finished, then check that the counts, expected counts and fork-activity result are unchanged. |
| T6.AC2 | Marked met (review-2.md:3). `--reanalyse` rewrites `read-files.txt` and `final-output.txt` and deletes and recopies `dev-issues/`. With no run clone, that deletes the saved `issue-body.md` and `draft-notes.md`. The self-test passing (extras-2.log:1) never covered the reanalyse path. | Only delete and recopy `dev-issues/` when the clone holds folders the run itself created. After re-deriving, check that the full file set of both runs is still present and that `installed_copy` is empty. |
| T6.AC3 | Unmet (review-2.md:4). The contradiction section was lost because the record scripts ran in the wrong order: `addition_report.py` rewrites all of `record.md` (review-2.md:6). The summary field conflicts with the record (review-2.md:9). | Run `addition_report.py` first, then `contradiction_report.py`, every time. Also make `addition_report.py` keep an existing contradiction section, so the order no longer matters. Rename the summary field. Then confirm the record holds the full question, its options, the named file, the answer and the body diff. |
| T6.AC4 | Marked met (review-2.md:5). Attempt 1, the run that hit the infrastructure failure, has no summary or record, so its gh calls and fork result are not recorded anywhere (review-2.md:7). Re-deriving could also overwrite a live pending note (review-2.md:8). | Re-derive attempt 1 into its own `summary.json` (unknown-call count from its `gh.log`). Mark its fork-activity result as "not recorded" instead of empty, and write a record that names the permission error. Never touch STOP or PENDING-REVIEW. |

differs-by: `--reanalyse` becomes a read-only re-derivation that never writes STOP or PENDING-REVIEW. It is the single path that records all three quick folders, attempt 1 included, and it runs only after the deep chain has finished. The record scripts then run in a fixed order (additions, then contradiction).

steps:
1. **Right away, before anything else:** copy `run_create.py` back from the copy under `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/retries/T6/artifacts-2/` (expected at `artifacts-2/harness/run_create.py`) to `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py`, unchanged. Check with `cmp` that the two files are identical. The deep chain starts each run through this file, so it must not stay missing. Then read `/tmp/createQuestionEv-scratch/logs/chain-deep.log`. If a run failed to start while the file was gone, report that to the lead as a Task 8 infrastructure failure. Do not restart it.
2. Make no further change to `run_create.py`, `addition_report.py` or `contradiction_report.py` until the executor confirms the deep chain has finished. That means `chain-deep.log` shows the last run's `exit=` line and no later `start` line. Then record the existence and modification time of `/tmp/createQuestionEv-scratch/STOP` and `/tmp/createQuestionEv-scratch/PENDING-REVIEW` (for example with `ls -l --time-style=full-iso`).
3. Edit `run_create.py`, the `finish()` function:
   - (a) Add a keyword argument `control: bool = True`.
   - (b) Do the `PENDING_FILE.write_text(...)` for unattributed activity and the `write_stop(...)` call only when `control` is true. When it is false, print `reanalyse: control files not written; stop reasons: <list>; pending items: <unattributed list>`.
   - (c) Replace the unconditional delete of `dev-issues` and the copy from the clone with: `own = own_issue_dirs(clone)`, and delete and copy only if `own` is not empty.
   - (d) Rename the summary key `additions_in_posted_body` to `additions_verbatim_first_40_chars_in_posted_body`, keeping the same value.
4. Edit `run_create.py`, the `reanalyse()` function:
   - (a) Pass `control=False` to `finish`.
   - (b) When no `summary.json` is saved, take the flags from `prompt.txt` (the text after the closing quote of the description) and the description from `prompt.txt` (the quoted text before ` [synthetic run marker`). Fall back to the command-line values only if parsing fails.
   - (c) When the saved summary has no `fork_activity`, pass the activity error `not recorded: no saved summary.json (post-processing crashed before writing it)` instead of an empty result.
5. Add one check to `self_test()`. Copy `runs/quick-contradiction` (its saved summary lists unattributed activity) into the sandbox `runs/`, call `reanalyse()` on it, and assert that the sandbox `STOP` and `PENDING-REVIEW` files do not exist afterwards. Run `uv run ruff check` on the file and `uv run python <path>/run_create.py --self-test`. Both must pass.
6. Edit `/tmp/createQuestionEv-scratch/addition_report.py`:
   - (a) Before writing, read the existing `record.md`. If it contains `\n## Question, answer and body comparison`, keep that part and append it after the new lines.
   - (b) When no `draft-notes.md` is saved, print `additions: not evidenced (no draft-notes.md was saved for this run)` instead of a count of 0, and print no table.
7. Re-derive each quick folder. Every command must include `--reanalyse`; without it the command starts a live run, so check each command before running it:
   - `run --name quick-additions-only --depth quick --description x --expect-questions 0 --expect-create 1 --expect-comments 0 --reanalyse`
   - the same command with `--name quick-contradiction --expect-questions 1`
   - the same command with `--name quick-additions-only-attempt1-infra-failure --expect-questions 0`

   Run them from the package directory.
8. Build the records in this order:
   - `addition_report.py quick-additions-only`
   - `addition_report.py quick-contradiction`, then `contradiction_report.py quick-contradiction`
   - `addition_report.py quick-additions-only-attempt1-infra-failure`
9. Append a section `## Infrastructure failure (attempt 1)` to `runs/quick-additions-only-attempt1-infra-failure/record.md`. It must say:
   - The cause: `PermissionError: [Errno 13] Permission denied: '/root/.claude/commands/sc/analyze.md'` in `read_files_report`, from `logs/quick-additions-only-attempt1.out` line 14.
   - The repeat is `runs/quick-additions-only`.
   - `draft-notes.md` and `issue-body.md` were not saved, because the crash happened before the copy and the repeat reused the clone.
   - The fork-activity result was not recorded.
   - The counts come from its `gh.log` and transcripts, as shown in `summary.json`.

   Report the unrecorded fork result to the lead as a finding. Do not write STOP.
10. Verify each of these:
    - The STOP and PENDING-REVIEW existence and times match what you recorded in step 2.
    - `grep -L additions_in_posted_body` lists all three new summaries.
    - The `quick-contradiction` `record.md` contains `## Question, answer and body comparison`, `question 1 (full text`, `options:`, `` `create_issue.py` yes ``, `answer 1`, and a filled `diff` block.
    - Both quick runs still hold `dev-issues/*/issue-body.md`, `dev-issues/*/draft-notes.md`, `final-output.txt`, `read-files.txt`, `gh.log` and `transcripts/`.
    - Every summary shows `unknown_gh_calls` 0 and `installed_copy` [], and the fork-activity result of both quick runs is unchanged.
11. Do not run `clear-pending`, do not start or stop any run, and write nothing to GitHub, `src/`, `.claude/` or `.dev/issues/`.

I did not check that the `artifacts-2/` copy exists yet or its exact sub-path; the revert has not happened. I also did not check that the `self_test()` sandbox layout accepts a copied run folder.

The main risk: if the revert moves `run_create.py` away while the deep chain sits between runs, the chain's next run can fail to start. That is why step 1 must happen at once.
