pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 6: Run the quick-depth create scenarios and record their counts
Acceptance criteria:
- `runs/quick-additions-only/summary.json` and `runs/quick-contradiction/summary.json` in the scratch directory of Task 4 exist (NEW-1) with the question counts, the `issue create` and `issue comment` counts, the expected counts and the after-run fork-activity result.
- Each run directory holds the event log, the fake `gh` call log, `issue-body.md`, `draft-notes.md`, the final output and `read-files.txt`; the `read-files.txt` hashes equal the `src/` list of Task 4 and no installed copy path appears in it.
- The additions run records, for each addition, whether it appears in the body, the notes and the final output, and whether the body was shown for approval; the contradiction run records the question text (does it name the contradicted item), the answer supplied and the body comparison, or an explicit "not evidenced" line when Task 4 found no way to supply an answer.
- No call in either fake `gh` log is an unknown call, and fork activity did not change.
AC ids in bullet order: T6.AC1, T6.AC2, T6.AC3, T6.AC4
Steps:
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
differs-by: `summary.json` holds only counts and raw lists, and every yes/no verdict about where an addition appears lives only in `record.md`. Each run folder, including the first-attempt folder, is rebuilt in one fixed pass (reanalyse, then `addition_report`, then `contradiction_report`). That pass runs only after the deep chain ends, and reanalyse never touches the control files or the saved draft folders.
