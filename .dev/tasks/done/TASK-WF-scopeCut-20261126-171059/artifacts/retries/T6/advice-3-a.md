model: opus (claude-gw-tier1a) family: claude rung: top
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T6.AC1 | It was not missed. The reviewer marked it met at review-2.md:4. The variables are at attempt-2.diff:30-32, the `gh api` lines at attempt-2.diff:41-43, 65-66 and 109, and the test that checks them at attempt-2.diff:152-158. The new rollback command must use the variables: the script prints `gh api --method DELETE {base}/rulesets/{rid}` (scripts/apply_org_rulesets.py:774), but the page writes `"repos/$OWNER/$REPO/rulesets/<id>"`. | Keep the `OWNER=`/`REPO=`/`OUT=` block and the two variable tests (attempt-2.diff:147-158) as they are. |
| T6.AC2 | The required words were present and tested (review-2.md:5, attempt-2.diff:161-179). The attempt failed on the scope findings, which all sit in prose that retells the script's behaviour in the writer's own words: the intro says the script reads `protect-integration.json` (attempt-2.diff:9, review-2.md:9); the digest explanation (attempt-2.diff:61, 97) is F1.2, F2.1 and F2.2 at review-2.md:3, 8, 9; "nothing else was written" (attempt-2.diff:102) is F2.3 at review-2.md:10; the refusal table has no `branch not supported` row and no `read-back ... failed` text (attempt-2.diff:90-102, review-2.md:11); "More than 200 commits ... gives `incomplete`" and "403 or 404" (attempt-2.diff:81) are F2.5 at review-2.md:12; "dry run must end with `source activity`" (attempt-2.diff:74) is F2.6 at review-2.md:13. Each review round found new wording errors of the same kind (origin=late or fix-induced). | Write every sentence about behaviour from the script's own output strings and quote them. Drop explanations the brief does not ask for (how the digest is built). Add a test that each refusal and failure text of the script appears on the page. |
| T6.AC3 | It was not missed (review-2.md:6). The name test (attempt-2.diff:196-214) reads the summary at test time, checks for 17 names and skips when the file is absent. | Keep `private_repo_names` and the skip test unchanged. Write no real repo name or org login anywhere, and use only synthetic names such as `acme`/`acme-one` (attempt-2.diff:187). |
| T6.AC4 | It was not missed: 138 passed, ruff check and format are clean (extras-2.log:9-15, review-2.md:7). | Run the same three commands after the rewrite. Keep new test lines under 88 characters. |

differs-by: The page's behaviour text is no longer the writer's own retelling. Each claim either quotes an exact message string from scripts/apply_org_rulesets.py or is dropped, and `test_page.py` gains a test that every refusal and failure message stem of the script is on the page. Earlier attempts wrote free prose and fixed wording one finding at a time.

steps:
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

Not checked: I did not read `.github/rulesets/protect-master.json` or the hooks/keys/installations commands in `docs/developer-guide/branch-protection.md`, so step 3's rule-type sentence and step 2's command match still need checking. The new message-text test assumes `_REFUSAL_TEXT` keeps its current values (scripts/apply_org_rulesets.py:567-573).

Files: /home/coder/workspaces/worktrees/IronClaude/issue-838/scripts/apply_org_rulesets.py, /home/coder/workspaces/worktrees/IronClaude/issue-838/.dev/tasks/to-do/TASK-WF-scopeCut-20261126-171059/artifacts/retries/T6/review-2.md, /home/coder/workspaces/worktrees/IronClaude/issue-838/.dev/tasks/to-do/TASK-WF-scopeCut-20261126-171059/artifacts/retries/T6/attempt-2.diff, /home/coder/workspaces/worktrees/IronClaude/issue-838/.dev/tasks/to-do/TASK-WF-scopeCut-20261126-171059/artifacts/retries/T6/extras-2.log
