pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 6: Write the operator page and its test
Acceptance criteria:
- The page defines `OWNER` and `REPO` variables, and every `gh api` command in it uses `$OWNER` and `$REPO` or the placeholder `<org>`.
- The page mentions `--apply`, `--confirm`, the dry run, `-before.json`, the 90-day push check, the tag warning and the canary rule, and `test_page.py` asserts that the page states the canary must show complete activity coverage before other repos rely on it.
- The page names no real private repo. `test_page.py` reads the 17 names at test time from the untracked `.dev/issues/838/issue-summary.md` (the comma-separated names after "all with Clay admin:" in the paragraph that starts "Clay's answer for this story") and asserts none appears in the page, in `scripts/apply_org_rulesets.py` or in any file of `tests/org_rulesets/`; the test is skipped when that file does not exist, and the names are written in no tracked file.
- `uv run pytest tests/org_rulesets/ tests/docs/test_branch_protection_rulesets.py` passes, `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` report nothing.
ids: T6.AC1 T6.AC2 T6.AC3 T6.AC4 (the four bullets above, in order)

Steps:
1. Start from the pre-task snapshot. Before writing, Grep scripts/apply_org_rulesets.py for `problems.append|stop\(|fail\(|_REFUSAL_TEXT` and confirm that the message list is lines 568-572, 591, 596, 599, 601, 604, 606, 680, 738, 742, 746, 763, 789, 796, 800 and 803.
2. Intro: the script reads only `protect-master.json`, used for every branch ruleset with the name and ref changed per branch, and `protect-release-tags.json` (scripts/apply_org_rulesets.py:35-36, 69-82). It never reads `protect-integration.json`, so editing that file changes nothing the script applies. Keep the delivery boundary list from attempt-2.diff:13-23 and the variables block from attempt-2.diff:29-33.
3. Order per repo: keep the steps from attempt-2.diff:37-70 (hooks/keys/installations with `echo "exit status: $?"` and the "unknown, never "0"" sentence, dry run, manual workflow check, apply with `<digest>`, read-only check, comment on issue 838).
   - Replace the digest sentence at attempt-2.diff:61 with exactly this: "Pass the digest the dry run printed. `--apply` reads everything again (nothing carries over from the dry run) and refuses with `confirm digest does not match the rulesets rendered now` when the digest of the ruleset bodies it renders now differs; rerun the dry run." Say nothing else about what the digest covers.
   - Dry-run exit: 0 when it printed a `digest:` line, 69 otherwise (scripts/apply_org_rulesets.py:901-902).
   - Keep "Each branch must print `deletion`, `non_fast_forward` and `pull_request`" only after a Read of `.github/rulesets/protect-master.json` confirms those rule types. Otherwise drop it.
4. Canary section, on one line: "The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run (`<branch>: <result> (source <source>, direct pushes N, examined N)`) must read `(source activity, ...)`, and no branch line and no `push check` line may read `incomplete`." Add: if any branch reads `source commits` or `incomplete`, stop before a second repo (scripts/apply_org_rulesets.py:631-640).
5. Push check section, quoting scripts/apply_org_rulesets.py:420-516:
   - The feed's `push`, `force_push` and `branch_deletion` events count as direct pushes; `pr_merge` does not.
   - The commit list is the fallback whenever the feed call fails, its answer is malformed, or it runs past 10 pages.
   - In the fallback, a failed or cut-short commit list gives `incomplete`. Each of the first 200 commits is checked for a merged pull request into that branch, and a commit without one is a direct push.
   - Any direct push found gives `blocked`. With none found, more than 200 commits or a failed pull-request lookup gives `incomplete` (note `not every commit was checked`).
   - Overall result: `blocked` if any branch is blocked, `pass` only if all branches pass, `incomplete` otherwise. Keep the "no named person is excused" paragraph (attempt-2.diff:84).
6. Refusals table: it covers `refused:` on stderr with exit 69, no write and no file. Write one row per text, quoted exactly:
   - `no --out folder given`
   - `repo is archived`
   - `no admin permission on the repo`
   - `repo has no default branch`
   - `repo cannot be read (HTTP n)`
   - `a branch lookup failed`
   - `branch not supported: not a plain branch name: '<name>'` (the default branch is empty, contains `*` or `~`, or starts with `refs/`)
   - `push check is blocked` / `push check is incomplete`
   - `classic branch protection on <branch>` / `branch protection state unknown on <branch>`
   - `ruleset list cannot be read (HTTP n)`
   - `repo lists a ruleset id this script never touches`
   - `confirm digest does not match the rulesets rendered now`
   - `before-state file already exists: <path>`
   - `before-state read failed for ruleset <id>`

   Then a separate "Failures after the before-state file" list (`failed:` on stderr, exit 69, scripts/apply_org_rulesets.py:766-803, 879):
   - `POST of <name> failed (HTTP n)`
   - `POST of <name> timed out and no ruleset of that name found`
   - `read-back of <name> (id n) failed`
   - `read-back of <name> (id n) differs: ...`

   Say exactly this: if the first POST fails, only the before-state file was written and no rollback command is printed. If a later POST fails, the rulesets created before it stay in place and their DELETE commands are printed. A read-back failure includes that ruleset's own id in the rollback (lines 797-800). A ruleset whose name is already in the list read at apply time is skipped (`skipped, already present: <name>`) and never edited (lines 781-783, 869). Usage errors exit 64 with `usage error:` (line 893).
7. Rollback section: the DELETE command with `$OWNER`/`$REPO`, newest first. The before-state file `<repo>-before.json` holds `org`, `repo`, `saved_at`, `digest`, the full body of every existing ruleset by id, and `protection` per branch, which is always `none` because classic protection is refused (lines 682-689). The script never restores it. Keep the follow-ups paragraph (attempt-2.diff:116) and the tests paragraph.
8. `tests/org_rulesets/test_page.py`: keep attempt-2.diff:127-214 as written. Add `test_every_refusal_and_failure_text_is_on_the_page(orr, page)`. It asserts that each `orr._REFUSAL_TEXT` value cut at `" ("`, plus this fixed tuple, is in `" ".join(page.split())`: `"branch not supported: not a plain branch name"`, `"push check is blocked"`, `"push check is incomplete"`, `"classic branch protection on"`, `"branch protection state unknown on"`, `"ruleset list cannot be read"`, `"repo lists a ruleset id this script never touches"`, `"confirm digest does not match the rulesets rendered now"`, `"before-state file already exists"`, `"before-state read failed for ruleset"`, `"no --out folder given"`, `"timed out and no ruleset of that name found"`, `"failed (HTTP"`, `"read-back of"`, `"differs:"`. Use no fixture other than `orr` and the module-level `page`.
9. Read the page line by line against scripts/apply_org_rulesets.py. Delete any sentence that names a behaviour you cannot point to a script line for.
10. Run `uv run pytest tests/org_rulesets/ tests/docs/test_branch_protection_rulesets.py`, `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets`.

differs-by: The page's behaviour text is no longer the writer's own retelling. Each claim either quotes an exact message string from scripts/apply_org_rulesets.py or is dropped, and `test_page.py` gains a test that every refusal and failure message stem of the script is on the page. Earlier attempts wrote free prose and fixed wording one finding at a time.
