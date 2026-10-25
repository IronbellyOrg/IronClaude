# advice-4-a — escalation 2 adviser "a" (ladder entry: opus x2). Saved verbatim by the parent. Parent check: PASSED.

outcome: ready

T1.AC1: Earlier attempts left several statements that are false against the live code. Attempt 3 says the lookup "reads the whole file on every call" (attempt-3.diff:227, :677), but `_search_local_files` returns on the first match (src/superclaude/pm_agent/reflexion.py:202-215). The README says the sample file shows the fields the recorder uses (attempt-3.diff:63; review-3.md:14), but the live rows use the ts/task/mistake layout (docs/memory/reflexion.jsonl.example:1). The guide repeats that implication at attempt-3.diff:483. "No field changes whether a row can match" (attempt-3.diff:506) is wrong, because the three signature keys decide matching (reflexion.py:153-170). The README never mentions the MindBase stub (attempt-3.diff:18-39 against reflexion.py:101-104,172-184). "Fails in its call phase" (attempt-3.diff:594) is narrower than the code, which records any call-phase exception (src/superclaude/pytest_plugin.py:179-183). Finally, D4's "who calls what" sentence (review-3.md:17). | Re-apply attempt-3.diff, then make steps 3, 4, 12-14, 16 and 18. They give stop-at-first-match wording, an accurate description of the old-layout sample file in both guides, "no other field, such as `status`", the README backend sentence, the call-phase exception wording and the D4 text.

T1.AC2: D2 was fixed by adding more jq detectors. But jq does not parse line by line the way `json.loads` does, and it stops at the first parse error. So any jq "checker" over- or under-reports which lines the lookup skips or chokes on (review-3.md:15; attempt-3.diff:115-123, :243-254, :650-651; reflexion.py:204-217). The privacy text "the same text is also written" (attempt-3.diff:179) is vague about the second output, which holds specific fields only when `root_cause`/`solution` is non-empty (reflexion.py:135,264-316). The guide's `cp` backup overwrites any earlier `.bak` (attempt-3.diff:664). | Remove every validation and duplicate-finder command from both guides. Replace them with written rules taken from reflexion.py:155-170 and :338-346, plus backup and manual review. List the mistake-file fields explicitly. Use a timestamped backup name (steps 6, 8, 10, 17).

T1.AC3: Attempt 3 replaced the JWT pair instead of showing it computed correctly (attempt-3.diff:514-546). A strict reading of the criterion expects that pair to appear as 4/8 = 0.50, no match. The math was checked by hand against the tokenizer in reflexion.py:235-244: `{jwt, token, validation, failed, missing, secret}` and `{jwt, validation, failed, secret, not, found}` share 4 of 8 words. | Keep the two 0.90/0.50 examples and add the message-only JWT pair as a no-match, plus one sentence correcting the old 87.5% claim (step 15).

T1.AC4: The scope breaches go beyond the two Overview bullets in D3 (review-3.md:16; attempt-3.diff:19-20). Attempt 3 also deleted the Automatic Files section (attempt-3.diff:75-83), the Gitignore block (attempt-3.diff:141-159) and the File Sizes bullets (attempt-3.diff:210-216), all of which make workflow_metrics/patterns_learned claims that belong to Task 4. It also rewrote the unrelated `chmod` tip (attempt-3.diff:233-238). The claim matrix has no rows for the new sentences. | Restore those passages word for word, except the lines that name reflexion.jsonl. Prove it with a `git diff -U0` check. Add matrix rows citing reflexion.py:101-104,135,153-170,172-184,202-219,238-244,264-316,338-346, pytest_plugin.py:179-196, tests/conftest.py:49-79,116-117, docs/memory/reflexion.jsonl.example:1-15 and docs/memory/solutions_learned.jsonl:1-4 (steps 2, 5, 7, 9, 10, 20-23).

differs-by: Neither guide offers any shell command that claims to check, find or count bad or duplicate rows. The only commands left are the backups and plain viewing commands (`jq .`, `grep`, `wc -l`, `tail`). Every bad-row rule is written as prose taken from reflexion.py. Separately, every README line about workflow_metrics, patterns_learned, pm_context, token_efficiency, last_session or next_actions stays exactly as in the original.

Steps:
1. Run `git apply --check .dev/implement/03-memory-docs-f5865990/retries/T1/attempt-3.diff`. If it passes, run `git apply` with the same path onto the reverted guides. Make every edit below on top of that.
2. README Overview: restore bullets 2 and 3 word for word: `2. **Workflow Metrics** - Performance tracking and optimization` and `3. **Pattern Learning** - Successful implementation patterns`. Keep the new first paragraph and the new bullet 1.
3. README `### solutions_learned.jsonl`:
   - Set **Written by** to: "`ReflexionPattern.record_error()` (explicit calls, and the pytest recorder for `@pytest.mark.reflexion` tests whose call phase raises an exception)".
   - Replace the lookup paragraph with: "The lookup compares lowercase, whitespace-separated word sets built from `error_type`, `error_message` (each run of digits replaced by `N`, then cut to the first 100 characters) and `test_name`. A stored row matches when shared words divided by all distinct words is 0.7 or higher (exactly 0.7 matches). Rows are read in file order and the first matching row is returned. There is no ranking and no newest-first order, and no other field, such as `status`, affects matching."
   - Then add: "Storage is this local file only. `get_solution()` first calls a MindBase hook, but that hook is a stub that always returns `None`; no MindBase backend is implemented."
   - Keep the paragraph about the existing pattern-style rows and the example row.
4. README `### reflexion.jsonl.example`:
   - Set **Purpose** to: "Sample rows in an older layout (`ts`, `task`, `mistake`, `evidence`, `rule`, `fix`, `tests`, `status`). They have no `error_type`, `error_message` or `test_name`, so the lookup could never match them."
   - Replace the next paragraph with: "Do not copy it into `solutions_learned.jsonl`. It is a reference file only."
   - Remove "not real incidents".
5. README File Management: restore the original `### Automatic Files` section word for word, deleting only the bullet ``- `reflexion.jsonl` - Created on first error``. Keep attempt 3's "When Files Are Missing" text.
6. README Backup: change the paragraph to: "There is no supported command for truncating, deduplicating or repairing `solutions_learned.jsonl`. If it has grown too large or contains a bad line, open it, read the rows, and edit it by hand against the backup. Do not pipe it through a command that overwrites it." Delete the "**Check JSON format**" heading and its jq block.
7. README Git section:
   - Restore the original **Recommendation** line and the whole `### Gitignore Configuration` section word for word. Change only `reflexion.jsonl` to `solutions_learned.jsonl` in the Recommendation line and in the first `echo` line. Leave the workflow_metrics `echo` line and the "shared team memory" block untouched.
   - Directly after the Recommendation line, add: "Records may contain error text from your own code. Review them before committing. Ignoring a file that Git already tracks (this repository tracks `docs/memory/solutions_learned.jsonl`) does not untrack it."
   - Keep attempt 3's "Should be committed" and "Optional to commit" bullets.
8. README Privacy: replace the sentence "When `root_cause` or `solution` is present, the same text is also written..." with: "When `root_cause` or `solution` is non-empty, a Markdown file in the `mistakes/` directory also receives the test name, error type, error message, traceback, root cause, solution, prevention, `why_missed` and `lesson` text."
9. README Performance: restore the original `### File Sizes` heading, its "Expected file sizes:" line and the workflow_metrics and patterns_learned bullets word for word, deleting only the reflexion.jsonl bullet. Replace `### Search Performance` and its body with: "No size or search-time figure has been measured for `solutions_learned.jsonl`. The lookup reads the file from the top on every call and stops at the first matching row, so a lookup that finds no match reads every line."
10. README Troubleshooting:
    - Revert `### File Permission Errors` to the original text.
    - Replace the whole `### Corrupted JSON` body with: "There is no repair command. The lookup skips a line that is not valid JSON. A line that is valid JSON but not an object makes `get_statistics()` raise and can make `get_solution()` raise. A row with an `error_type`, `error_message` or `test_name` key whose value is not a string makes `get_solution()` raise when the lookup reaches it, unless an earlier row matched first. To fix any of these, back up the file, read it, and correct or remove the line by hand."
    - Replace the `### Duplicate Entries` body with: "There is no deduplication command. After a backup, read the file and decide by hand which rows to keep. The lookup returns the first matching row in file order, so an earlier duplicate answers before a later one."
11. README: keep attempt 3's Related Documentation and Quick Commands as they are.
12. Guide Overview:
    - Bullet 1 becomes: "**Explicit API**: you (or code you write) call `get_solution()` and `record_error()`. Nothing in the framework calls `get_solution()`. The only automatic `record_error()` call is the opt-in pytest recorder described below."
    - The "No setup" bullet becomes: "**No setup**: the constructor creates the memory directory and its sibling `mistakes/` directory if they are missing."
13. Guide, after the example row: replace the "See `docs/memory/reflexion.jsonl.example`..." sentence with: "`docs/memory/reflexion.jsonl.example` currently holds sample rows in an older layout (`ts`, `task`, `mistake`, `evidence`, `rule`, `fix`, `tests`, `status`). The lookup could never match them, because they have no `error_type`, `error_message` or `test_name`. Do not copy it into `docs/memory/solutions_learned.jsonl`." In Related files, rename that bullet to "**Sample rows (older layout)**".
14. Guide "What this means" bullets:
    - "An older row that matches wins over a newer one." becomes "A row earlier in the file wins over a later one."
    - Replace the status bullet with: "No other field, such as `status` or a \"deprecated\" marker, affects whether a row matches."
    - Add the bullet: "If the error you look up has none of `error_type`, `error_message` or `test_name`, nothing matches."
15. Guide worked example:
    - Retitle it: "**Worked examples** (all computed from the rules above; the third pair is `error_message` only, with no `error_type` or `test_name`):"
    - Inside the code block, append: `Stored:   JWT validation failed secret not found` / `Current:  JWT token validation failed missing secret` / `Shared 4 words / 8 distinct words = 0.50  -> no match`.
    - After the block, add: "Earlier versions of this guide called the third pair an 87.5% match; it is 50% and does not match."
16. Guide pytest recorder:
    - Replace "records a failure only when the test carries `@pytest.mark.reflexion` and fails in its call phase." with "records a test only when it carries `@pytest.mark.reflexion` and its call phase ends with an exception (`call.excinfo` is set). That covers an ordinary failure and can also cover a skip or xfail raised inside the test body."
    - Change "unless `REFLEXION_OUTPUT_DIR` is set" to "unless `REFLEXION_OUTPUT_DIR` is set and not empty".
17. Guide "Inspecting and maintaining the data":
    - Delete the "# Check that every line is valid JSON" comment and its jq line.
    - Rename "# Count rows" to "# Count lines".
    - Change the backup command to `cp docs/memory/solutions_learned.jsonl "docs/memory/solutions_learned.jsonl.$(date +%Y%m%d-%H%M%S).bak"`.
    - Replace the last three sentences of the "Do not delete, deduplicate..." paragraph with the step-10 Corrupted JSON sentences, from "The lookup skips" through "unless an earlier row matched first."
18. Guide Performance: replace its last two sentences with: "Earlier versions of this guide quoted percentages and timings that no measurement in this repository supports; they have been removed. The lookup reads the file from the top on every call and stops at the first matching row, so a lookup with no match reads every line; how long that takes has not been measured."
19. Leave every other hunk of attempt-3.diff as applied.
20. Grep both guides and confirm:
    - `jq -c`, `uniq`, `whole file`, `Synthetic sample rows showing`, `not real incidents` and `no field changes` do not appear.
    - `87.5%` appears only in the step-15 sentence.
    - `>>` appears only in the two restored `.gitignore` echo lines.
    - Any other `>` appears only inside prose, with no redirect to a data file.
    - Every `reflexion.jsonl` is followed by `.example`, except the restored Gitignore lines, which now say `solutions_learned.jsonl`.
21. Run `git diff -U0 docs/memory/README.md` and confirm that no added or removed line contains `workflow_metrics`, `patterns_learned`, `pm_context`, `token_efficiency`, `last_session` or `next_actions`.
22. Update `.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/03-memory-docs/t1-claim-matrix.md` with one row for each new or changed claim, citing only live source:
    - stop at first match: reflexion.py:202-219
    - MindBase stub: reflexion.py:101-104,172-184
    - empty query signature: reflexion.py:238-239
    - JWT 4/8: reflexion.py:235-244
    - call-phase exception: pytest_plugin.py:179-196
    - mistake-file fields: reflexion.py:135,264-316
    - bad-row raise rules: reflexion.py:155-170,338-346
    - non-empty environment variable: reflexion.py:69-71
    - constructor creates directories: reflexion.py:80-82
    - sample-file layout: docs/memory/reflexion.jsonl.example:1-15
    - existing pattern rows: docs/memory/solutions_learned.jsonl:1-4
23. Re-run the read-only protected-hash check against the task's baseline file. Then run `git status` and confirm that only `docs/user-guide/memory-system.md` and `docs/memory/README.md` are modified under `docs/`, `src/` and `tests/`. Stage and commit nothing.
