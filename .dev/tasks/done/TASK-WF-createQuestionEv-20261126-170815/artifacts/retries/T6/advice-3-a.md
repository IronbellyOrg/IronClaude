model: opus (ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]) family: claude rung: top (executor tier unknown, so adviser A is the top rung)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T6.AC1 | The review found this met (review-2.md:2). But the scope finding F5.1 says the first attempt has no `summary.json` and no record, and its permission error appears only in a shell log (review-2.md:7). F7.1 says one summary field disagrees with the record (review-2.md:9). | Rebuild the summaries only through `--reanalyse`, and only after the deep chain has finished. Take the field `additions_in_posted_body` out of `summary.json`. Add `summary.json` for the first-attempt folder. Keep every count field as it is. |
| T6.AC2 | The review found this met (review-2.md:3). Attempt 3 reruns reanalyse, so the risk is new: `finish` deletes the saved `dev-issues` folder before copying it again from the run clone. A clone that is missing would erase the saved `issue-body.md` and `draft-notes.md`. Attempt 2 only re-derived folders whose clones still existed. | Delete and recopy `dev-issues` only when the clone's `.dev/issues` folder exists. Check afterwards that each quick run folder still holds `dev-issues/990001/issue-body.md` and `draft-notes.md`, and that `read-files.txt` still matches the `src/` list. |
| T6.AC3 | F4.1: the two record scripts ran in the wrong order, so `addition_report` overwrote the section that `contradiction_report` had added (review-2.md:6). F7.1: the summary's verbatim match on the first 40 characters contradicts `record.md` (review-2.md:9). Both runs were held to the AC wording at review-2.md:4. | Run the two scripts in a fixed order for each folder: `addition_report.py <name>`, then `contradiction_report.py <name>` (the second one rebuilds only its own section, so rerunning it is safe). Do not edit either scratch script. Presence verdicts live only in `record.md`. |
| T6.AC4 | The review found this met (review-2.md:5). F6.1 shows the risk: reanalysis passes the old unattributed list to `finish`, which writes PENDING-REVIEW and STOP (review-2.md:8). So rebuilding the records could change the matrix's control files. | In reanalyse mode, `finish` must never write PENDING-REVIEW or STOP. It prints the stop reasons and the pending items instead. Check afterwards that both control files are byte for byte unchanged. |

differs-by: `summary.json` holds only counts and raw lists, and every yes/no verdict about where an addition appears lives only in `record.md`. Each run folder, including the first-attempt folder, is rebuilt in one fixed pass (reanalyse, then `addition_report`, then `contradiction_report`). That pass runs only after the deep chain ends, and reanalyse never touches the control files or the saved draft folders.

steps:
1. After the revert, copy `artifacts/retries/T6/artifacts-2/harness/run_create.py` (wherever the revert put the attempt-2 file under `artifacts-2/`) back to `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness/run_create.py`, byte for byte. Check that the sha256 of the two copies is equal. This brings back the exact file the deep chain was using, so its behaviour does not change. Make no other edit yet.
2. Wait until the executor says the deep chain (Task 8) has finished. Until then, do not edit `run_create.py` or the scratch scripts, and do not run `--reanalyse`. Read-only inspection is allowed.
3. Record the sha256 (or confirm absence) of `/tmp/createQuestionEv-scratch/STOP` and `/tmp/createQuestionEv-scratch/PENDING-REVIEW`.
4. Make the edits for F6.1 and the saved-folder guard in `run_create.py`:
   - Add a keyword parameter `write_controls: bool = True` to `finish`.
   - When it is False, skip the PENDING_FILE write (the `activity["unattributed"]` branch) and the `write_stop` call. Instead print `reanalyse: would hold: <unattributed json>` and `reanalyse: stop reasons: <list>`, still store `summary["stop_conditions"]`, and return 0.
   - In `reanalyse`, call `finish(..., write_controls=False)`.
   - In `finish`, wrap the `shutil.rmtree(run_dir / "dev-issues")` and the copy loop that follows in `if (clone / ".dev/issues").exists():`.
5. Make the F7.1 edit in `finish`. Delete the `"additions_in_posted_body"` entry and put `"addition_presence": "see record.md (approximate best-matching-line rule)"` in its place. Leave `additions`, `contradictions` and the `false_files_*` lists as they are.
6. Run `uv run python ./artifacts/harness/run_create.py --self-test` from the package directory. It must print PASS, including the line saying the STOP and PENDING-REVIEW files were left untouched. Run `uv run ruff check` on the file.
7. Reanalyse the two quick runs with the same arguments attempt 2 used. The saved summary overrides them.
   - `uv run python ./artifacts/harness/run_create.py run --name quick-additions-only --depth quick --description x --expect-questions 0 --expect-create 1 --expect-comments 0 --reanalyse`
   - The same for `quick-contradiction` with `--expect-questions 1`.
   - Use the subcommand name that `main` really defines; read it before running.
8. Reanalyse the first attempt. It has no saved summary, so pass the real values:
   - `--name quick-additions-only-attempt1-infra-failure --depth quick --mode feature --type cli --description "<the quick-additions-only description from its prompt.txt>" --expect-questions 0 --expect-create 1 --expect-comments 0 --reanalyse`
   - Its clone folder does not exist, so the guard from step 4 keeps the folder as it is. Its notes were lost when the repeat reused the clone name, so its additions list will be empty.
9. Build the records in this order, from `/tmp/createQuestionEv-scratch`, for each folder:
   - `uv run python addition_report.py quick-additions-only`
   - `uv run python addition_report.py quick-contradiction`, then `uv run python contradiction_report.py quick-contradiction`
   - `uv run python addition_report.py quick-additions-only-attempt1-infra-failure`
10. Add a section headed `## Infrastructure failure (attempt 1)` to the first attempt's `record.md`, using the Edit tool on that scratch file. It must contain:
    - the exact permission-error line, quoted with its line number from `/tmp/createQuestionEv-scratch/logs/quick-additions-only-attempt1.out`;
    - a statement that the model session completed and the crash happened in the harness's post-processing, so it was not a model choice;
    - a statement that the draft notes and body were not saved because the repeat reused the clone name, so the notes columns are "not evidenced";
    - the question, `issue create` and `issue comment` counts from its new `summary.json`;
    - the name of the folder of the repeat that replaced it.
11. Check the results by reading the files:
    - `quick-contradiction/record.md` has both the additions table and the `## Question, answer and body comparison` section, with the full question text, its options, whether it names `create_issue.py`, the answer "keep my wording", and the body diff plus `create_issue.py` counts.
    - No `summary.json` of the three quick folders contains `additions_in_posted_body`.
    - The counts in all three summaries equal the attempt-2 values.
    - `dev-issues/990001/` still exists in both quick folders.
    - STOP and PENDING-REVIEW have the hashes recorded in step 3.
12. Write nothing to GitHub, edit nothing under `src/`, do not stage `.claude/` or `.dev/issues/`, and do not start or stop any run. Leave the standard and deep run folders as they are.

Not checked, and risks:
- I could not confirm the exact subcommand name in `main`, so the executor must read it before step 7.
- The standard and deep summaries will still carry the old `additions_in_posted_body` field. Tasks 7 and 8 own that.
