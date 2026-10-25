# advice-4-b — escalation 2 adviser "b" (ladder entry: opus x2). Saved verbatim by the parent. Parent check: PASSED. Runner-up (escalation 3 refactors this one).

outcome: ready

T1.AC1: Attempt 3 left five wrong or ambiguous contract statements. (a) The guide's "Exactly 0.7 counts as a match" (attempt-3.diff:496) is right, but the README never states the inclusive 0.7 boundary and attempt 3 added no 0.7 worked case. (b) Five sentences contradict the source. "The lookup reads the whole file on each call" (attempt-3.diff:227, attempt-3.diff:677) is wrong because the loop returns at the first match (src/superclaude/pm_agent/reflexion.py:203-215). "Unchanged except for an added timestamp" (attempt-3.diff:173) and "adds a timestamp key" (attempt-3.diff:462) hide that a caller-supplied timestamp is overwritten (src/superclaude/pm_agent/reflexion.py:128). "No field changes whether a row can match" (attempt-3.diff:506) is false, because the three signature fields decide matching (src/superclaude/pm_agent/reflexion.py:153-170). The README says "is present" (attempt-3.diff:179) where the guide says "non-empty" (attempt-3.diff:464); the code tests truthiness (src/superclaude/pm_agent/reflexion.py:135). "Fails in its call phase" (attempt-3.diff:374, attempt-3.diff:594) is looser than the real trigger, which is `call.excinfo is not None` (src/superclaude/pytest_plugin.py:179-183). (c) The README description of the sample file was wrong (review-3.md:14), and the guide repeats the same implication (attempt-3.diff:483). The live file uses the old layout (docs/memory/reflexion.jsonl.example:1). (d) The "except the pytest recorder" sentence was ambiguous (review-3.md:17; src/superclaude/pytest_plugin.py:185-196). | Change: keep attempt 3's directory/path/signature/first-match/MindBase/exports text. Apply the exact replacements in steps 2-6.
T1.AC2: The validation recipes claim more than they detect. The guide's "Check that every line is valid JSON" (attempt-3.diff:650-651) and the README's "To find invalid lines" (attempt-3.diff:251, attempt-3.diff:254) use `jq -c .`, which parses the file as one JSON stream. A pretty-printed object spread over several lines, or `{} {}` on one line, passes jq, but the lookup's per-line `json.loads` skips it (src/superclaude/pm_agent/reflexion.py:203-217). jq also passes the rows that make the code raise (review-3.md:15; src/superclaude/pm_agent/reflexion.py:155-168, src/superclaude/pm_agent/reflexion.py:341-343). The secret-removal backup (attempt-3.diff:664) copies the secret into `docs/memory/` next to a tracked file. The guide's privacy steps (attempt-3.diff:616) also leave out the version-history check the README has (attempt-3.diff:193). | Change: replace every `jq -c .` validation block with one read-only checker that uses the same per-line `json.loads` and type tests as the lookup. Put it in the guide; the README links to it. Move the backup outside the repository and say to delete it afterwards. Make both privacy step lists the same.
T1.AC3: Attempt 3 dropped the JWT pair (attempt-3.diff:425-429) and used a port/timeout pair instead (attempt-3.diff:543-545). So the example the criterion names never appears with its corrected number, and no example shows the 0.7 boundary (src/superclaude/pm_agent/reflexion.py:241-244). | Change: use three worked pairs: 0.90 match, exactly 0.70 match, and the message-only JWT pair at 4/8 = 0.50, no match. Add a note that the earlier 87.5% figure was wrong (src/superclaude/pm_agent/reflexion.py:235-244).
T1.AC4: The README Overview rewrite was out of scope (review-3.md:16; approach-3.md:4). The same kind of out-of-scope deletion, not flagged, removed Task 4's workflow_metrics/patterns_learned lines: the Automatic Files bullets (attempt-3.diff:80-81), the gitignore line (attempt-3.diff:150) and the file-size bullets (attempt-3.diff:215-216). The plan limits edits to memory-specific claims (plan 03-memory-docs.md:15, plan 03-memory-docs.md:72-74). The non-memory FAQ footer was also deleted (attempt-3.diff:721-724). | Change: restore those lines exactly, editing only the reflexion-specific line next to them. Add claim-matrix rows for every new correction, citing live source. Re-run the hash check and a scope diff.

differs-by: Every validation recipe in both guides is replaced by one read-only checker that copies the lookup's own per-line `json.loads` and type tests (src/superclaude/pm_agent/reflexion.py:203-217). Earlier attempts kept jq, which parses the file as a JSON stream and so cannot detect the problem lines it claimed to find.

Steps:
1. Check, then apply, attempt 3 to the reverted guides: `git apply --check .dev/implement/03-memory-docs-f5865990/retries/T1/attempt-3.diff`, then `git apply` the same file. Then make only the edits below.
2. README out-of-scope restores:
   - Restore Overview items 2 and 3 exactly: `2. **Workflow Metrics** - Performance tracking and optimization` and `3. **Pattern Learning** - Successful implementation patterns`.
   - Restore the "### Automatic Files" section exactly, but delete only its `reflexion.jsonl` bullet.
   - Restore the "Recommendation" line and the "### Gitignore Configuration" section exactly, with `reflexion.jsonl` changed to `solutions_learned.jsonl` on the Recommendation line and the first `echo` line. Keep the `workflow_metrics.jsonl` echo line.
   - Keep only this sentence from attempt 3's replacement: "Records may contain error text from your own code. Review them before committing."
   - In "### File Sizes", change "Expected file sizes:" to "Expected file sizes (estimates, not measured):". Delete only the `reflexion.jsonl` bullet and keep the other two exactly.
   - In the guide, restore the final `---` and the `**Questions?**` line exactly.
3. Sample-file wording:
   - README `reflexion.jsonl.example` Purpose line becomes: "**Purpose**: Synthetic sample rows in an older task/mistake/rule/fix layout; the lookup cannot match them (they have no `error_type`, `error_message` or `test_name`)".
   - Guide sentence after the example row becomes: "`docs/memory/reflexion.jsonl.example` holds synthetic rows in an older task/mistake/rule/fix layout, not the layout above, so the lookup cannot match them. It is a reference only; do not copy it into `docs/memory/solutions_learned.jsonl`."
   - Guide Related-files label becomes "**Older-layout sample rows**".
4. Recorder wording:
   - Guide write steps: step 1 becomes "sets `timestamp` in that same dictionary to the current local time (ISO format), replacing any `timestamp` the caller supplied;" and step 2 becomes "appends the dictionary to `solutions_learned.jsonl` as one JSON line;". In step 3, add "(`unknown` when there is no `test_name`)" after the file-name pattern.
   - README "What's Stored" first sentence becomes: "`record_error()` writes the dictionary it is given as one JSON line, after setting `timestamp` to the current time (a caller-supplied `timestamp` is replaced)."
   - README "When `root_cause` or `solution` is present" becomes "is non-empty".
5. Activation wording:
   - Guide Overview bullet becomes: "**Explicit API**: you (or code you write) call `get_solution()` and `record_error()`. Nothing in the framework calls `get_solution()`. The only automatic `record_error()` call is the opt-in pytest recorder described below."
   - Table row status becomes: "**Implemented, opt-in.** When a test marked `@pytest.mark.reflexion` raises an exception during its call phase (an ordinary failure is the usual case), the pytest plugin hook records it."
   - Pytest section first sentence becomes: "...records a test only when it carries `@pytest.mark.reflexion` and raises an exception during its call phase (pytest's `call.excinfo` is set)."
   - Its second paragraph becomes: "Outside this repository's own test suite, the recorder builds `ReflexionPattern()` with no argument, so it writes to `docs/memory/` under the current directory unless `REFLEXION_OUTPUT_DIR` is set. The `reflexion_pattern` fixture sets `REFLEXION_OUTPUT_DIR` and its own `memory_dir` to `tmp_path/docs/memory`, so a marked test that uses the fixture is recorded there."
   - README "Written by" parenthesis becomes: "(explicit calls, and the pytest recorder for `@pytest.mark.reflexion` tests that raise during their call phase)".
6. Matching and order wording:
   - Guide bullet "There is no `status`... no field changes whether a row can match." becomes: "Only `error_type`, `error_message` and `test_name` decide whether a row can match. Other keys, such as `status` or a \"deprecated\" marker, are stored but ignored by the lookup."
   - README sentence becomes: "A stored row matches when shared words divided by all distinct words is 0.7 or higher (exactly 0.7 counts), and the **first matching row in file order** is returned. There is no ranking and no newest-first order, and no other field (such as `status`) affects matching."
   - README duplicates sentence ending becomes: "so the row nearer the top of the file answers first."
   - Guide Performance becomes: "No token-savings, latency, file-size or error-recurrence figures have been measured for this system. Earlier versions of this guide quoted percentages and timings that were never measured; they have been removed. A lookup reads the file from the top and stops at the first match, so it reads every line when nothing matches; how long that takes has not been measured."
   - Replace the body of README "### Search Performance" with: "No search time has been measured. A lookup reads `solutions_learned.jsonl` from the top and stops at the first match, so it reads every line when nothing matches."
   - Change both `wc -l` comments to "# Count lines".
7. Replace the guide's worked-example block with these three pairs, headed "every number computed from the rules above":
   - "ValueError | invalid port value N in config | test_load_config" vs "...config file..." → 9/10 = 0.90, match.
   - Same stored row vs "ValueError | port value N in settings | test_load_config" → 7/10 = 0.70, match (exactly 0.7 counts).
   - Stored "JWT validation failed secret not found" vs current "JWT token validation failed missing secret" → 4/8 = 0.50, no match.
   - Then add: "In the third pair both dictionaries have only `error_message`, so each signature is just the message. Earlier versions of this guide showed this pair as 87.5%; the real overlap is 50%, below 0.7."
   - Recompute all three with a task-owned set calculation under `.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/03-memory-docs/`. Do not import the memory code.
8. Checker:
   - In the guide's read-only block, delete the `jq -c .` line and its comment.
   - After the block, add this sentence: "To list lines the lookup skips, or rows that can make it raise (read-only; it reads line by line with the same `json.loads` the lookup uses and prints nothing when no line has a problem). Rows with no signature field, such as the pattern-style rows already in this repository's file, are valid and are not reported; they simply never match."
   - Then add this block:
     ```
     uv run python - docs/memory/solutions_learned.jsonl <<'EOF'
     import json, sys
     with open(sys.argv[1]) as f:
         for n, line in enumerate(f, 1):
             try:
                 row = json.loads(line)
             except json.JSONDecodeError:
                 print(f"line {n}: not a single JSON value; the lookup skips it")
                 continue
             if not isinstance(row, dict):
                 print(f"line {n}: not an object; get_statistics() raises and get_solution() can raise")
                 continue
             bad = [k for k in ("error_type", "error_message", "test_name") if k in row and not isinstance(row[k], str)]
             if bad:
                 print(f"line {n}: {', '.join(bad)} not a string; get_solution() can raise")
     EOF
     ```
   - In the README, delete the "**Check JSON format**" block, and in Corrupted JSON delete "To find invalid lines:", its jq block and "`jq` reports the failing line...". Replace them with: "To list those lines, use the read-only checker in the [user guide](../user-guide/memory-system.md#inspecting-and-maintaining-the-data). Fix a reported line by hand after making a backup outside the repository."
9. Privacy and backup:
   - Guide backup command becomes `cp docs/memory/solutions_learned.jsonl "$HOME/solutions_learned.jsonl.bak"`, followed by "Keep the backup outside the repository so it is not committed by accident."
   - Guide secret bullet becomes: "If a secret is already stored: copy the file to a backup outside the repository, edit the row by hand, check the Markdown files in the mistakes directory for the same text, check your version-control history if the file was committed, then delete the backup, because it holds the secret too."
   - README step 1 becomes "Back up the files outside the repository." Add step 5: "Delete the backup once the edit is checked; it still holds the secret."
10. Run the checker with `uv run` against a task-owned fixture in the evidence folder. Use one valid row, a `{} {}` line, a blank line, `[1]`, `{"error_type": null}` and a two-line pretty-printed object. Confirm each bad line is reported with the right message. Then run it against a copy of `docs/memory/solutions_learned.jsonl` in that folder and confirm it prints nothing. Record both outputs as evidence of the recipe only, not of runtime behaviour.
11. Add claim-matrix rows citing live source, each with its basis:
    - first-match early return (reflexion.py:203-215)
    - timestamp overwrite (reflexion.py:128)
    - truthiness of root_cause/solution (reflexion.py:135)
    - the "unknown" file name (reflexion.py:264-266)
    - `call.excinfo` trigger and bare constructor (pytest_plugin.py:179-196)
    - fixture paths (pytest_plugin.py:90-93)
    - inclusive 0.7 and the three pairs (reflexion.py:235-244, reflexion.py:164-165)
    - the checker's match with the reader (reflexion.py:202-217, reflexion.py:338-346, reflexion.py:153-170)
    - sample-file layout (docs/memory/reflexion.jsonl.example:1-15)
    - existing data layout (docs/memory/solutions_learned.jsonl:1-4)
    - no `get_solution()` caller (pytest_plugin.py:185-196)
12. Verify:
    - Run the read-only hash check against the evidence baseline; only the two guides may differ.
    - `git status` must show only those two guides changed under `docs/`, `src/` and `tests/`.
    - `git diff docs/memory/README.md` must show no removed or added lines for the restored Overview items 2-3, the workflow_metrics/patterns_learned bullets, the workflow_metrics gitignore line or the two file-size bullets.
    - Search both guides: no `jq -c .`, no "whole file on each call", no "no field changes", no "87.5%" except inside the correction note.
    - Do not stage or commit.
