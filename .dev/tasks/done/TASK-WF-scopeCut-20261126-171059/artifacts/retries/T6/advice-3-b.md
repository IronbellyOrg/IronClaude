model: opus (claude-gw-tier1a) family: claude rung: top family-fallback: no GPT spawn path is verified on this install
outcome: ready
| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T6.AC1 | Met (review-2.md:4). The risk is in the rebuild: the variables block (attempt-2.diff:30-32) and the hooks, keys and installations lines (attempt-2.diff:41-43) must keep `$OWNER`/`$REPO` when the page is rewritten. The check that enforces this is attempt-2.diff:152-158. | Keep that variables block and that test. Any new `gh api` line, such as the rollback line at attempt-2.diff:109, uses `$OWNER` and `$REPO`. Write the guide's commands in their variable form only (docs/developer-guide/branch-protection.md:24-26 stays unchanged). |
| T6.AC2 | The required terms were present (review-2.md:5). The failure was in the canary wording. The page said the dry run "must end with `source activity`" (attempt-2.diff:74). The text `source activity` actually sits inside each branch line (scripts/apply_org_rulesets.py:637-640), and the dry run ends with the digest and apply lines (scripts/apply_org_rulesets.py:664-668). That is F2.6 at review-2.md:13. | Keep the sentence the test needs, "The canary must show complete activity coverage before other repos rely on it" (attempt-2.diff:177-179). Change the recipe to: every line of the form `  <branch>: <result> (source activity, direct pushes n, examined n)` reads `source activity`, and none reads `incomplete`. |
| T6.AC3 | Met (review-2.md:6). One weak spot: the scan reads only `tests/org_rulesets/*.py` (attempt-2.diff:210), but the criterion covers any file in that folder. | Scan every regular file directly in `tests/org_rulesets/` and skip `__pycache__`. Keep the summary parsing (attempt-2.diff:196-200), the check for exactly 17 names (attempt-2.diff:208) and the skip when the file is absent (attempt-2.diff:203-205). |
| T6.AC4 | Met: 138 passed and ruff was clean (extras-2.log:9-15, review-2.md:7). The attempt still failed on scope. Each claim about behaviour was hand-paraphrased, and each repair added new paraphrase that was also wrong. F2.1 came from the repair (review-2.md:8, "origin=fix-induced"). F2.2 through F2.5 are wrong or missing statements at attempt-2.diff:9, 61, 81, 90-102 (review-2.md:9-12). | Rebuild the page so that each statement about behaviour matches one script line. Add a test that pulls every refusal and failure message out of the script source and requires each one on the page. Rerun the same four commands. |

differs-by: The script's own message strings and cited lines become the checked source for the page. A new test in `test_page.py` extracts every refusal and failure message from `scripts/apply_org_rulesets.py` and requires a matching line on the page, so the refusal list can no longer be paraphrased or left incomplete.

steps:
1. Start from the pre-task snapshot. Create `docs/developer-guide/branch-protection-multi-repo.md` and keep the sections of attempt-2.diff:7-120. These parts were accepted and can be reused: the variables block, the order per repo, the exit-status rule, the tag check, the rollback section, the follow-ups and the Tests section. Rewrite every sentence in steps 2 to 9 below to these facts.
2. **Intro and digest (F1.2, F2.1, F2.2).**
   - The script reads only `protect-master.json` and `protect-release-tags.json` (scripts/apply_org_rulesets.py:35-36). Every branch ruleset, including `protect-integration`, is rendered from `protect-master.json` (scripts/apply_org_rulesets.py:69-77). `protect-integration.json` is never read, so editing it changes neither the digest nor what is applied.
   - The digest is the sha256 of the rendered bodies in write order (scripts/apply_org_rulesets.py:96-107). It changes only when one of those two files changes or the branch set changes (scripts/apply_org_rulesets.py:85-93).
   - `--apply` re-reads everything (scripts/apply_org_rulesets.py:739). The push check, classic protection and the ruleset list refuse on their own rules (scripts/apply_org_rulesets.py:595-606). That list refuses only when it is unreadable or holds a protected id.
   - A same-name ruleset that appeared after the dry run is skipped and printed as `skipped, already present:` (scripts/apply_org_rulesets.py:781-783, 869). It is never refused. Its body is saved in the before state (scripts/apply_org_rulesets.py:677-681).
3. **Push check (F2.5).**
   - The fallback to commits runs on any failed activity call, any malformed answer, or more than 10 pages (scripts/apply_org_rulesets.py:426-435).
   - The commit route gives `incomplete` in three cases: the commit list failed, was malformed or ran past 10 pages (scripts/apply_org_rulesets.py:462-470); a pull-request lookup failed; or there were more than 200 commits. The last two give `incomplete` only when none of the commits checked was a direct push. A direct push found gives `blocked` (scripts/apply_org_rulesets.py:471-487).
   - A commit counts as merged only when a merged pull request into that branch contains it (scripts/apply_org_rulesets.py:444-452).
4. **Canary (F2.6).** Use the wording from the T6.AC2 row, keyed to scripts/apply_org_rulesets.py:637-640.
5. **Refusals table (F2.4).** Write each message on one line, in the script's literal text, with `<name>`, `<branch>`, `<id>` and `n` as placeholders:
   - the five `_REFUSAL_TEXT` values (scripts/apply_org_rulesets.py:567-573);
   - `branch not supported: not a plain branch name: '<branch>'`, meaning the default branch name is empty, contains `*` or `~`, or starts with `refs/` (scripts/apply_org_rulesets.py:72-73, 591);
   - the messages at scripts/apply_org_rulesets.py:596, 599, 601, 604, 606, 742 and 746 (the last with `: <path>`), plus 738 and 680.
   - State that several refusals print together, joined by `; ` (scripts/apply_org_rulesets.py:733), after `refused:` with exit 69 (scripts/apply_org_rulesets.py:879-881).
   - Add a dry-run line: `no plan: the repo could not be planned` exits 69 (scripts/apply_org_rulesets.py:629, 901-902).
   - Add the usage errors with exit 64: the four messages at scripts/apply_org_rulesets.py:851, 856, 858 and 860. For the `--org:` case, show the upstream text from scripts/apply_org_rulesets.py:177.
   - Add one row for any other `refused: <text>`: the call guard blocked a call, which means a bug to report (scripts/apply_org_rulesets.py:904-908).
6. **Failures after a write (F2.3, F2.4).**
   - List all four messages: `POST of <name> timed out and no ruleset of that name found`, `POST of <name> failed (HTTP n)`, `read-back of <name> (id n) failed` and `read-back of <name> (id n) differs: <...>` (scripts/apply_org_rulesets.py:789, 796, 800, 803). They print after `failed:` (scripts/apply_org_rulesets.py:879).
   - Rulesets created before the failing step stay in place, and the printed rollback lists them newest first (scripts/apply_org_rulesets.py:766-776).
   - Only when the first POST is the one refused is the before-state file the only thing written. Drop the absolute claim "nothing else was written" (attempt-2.diff:102).
7. **Before-state file.** It holds `org`, `repo`, `saved_at`, `digest`, the full body of every existing ruleset read by id, and `none` for every branch of the set, because apply refuses on any other state (scripts/apply_org_rulesets.py:682-689). Replace "(`none` when there was none)" at attempt-2.diff:112.
8. **Check step.** Each branch's rule types must include `deletion`, `non_fast_forward` and `pull_request` (rule types in `.github/rulesets/protect-master.json`; these are only the types it adds).
9. **Recheck.** Read the final page against the script once more, line by line. Remove any sentence that matches no script line, rather than adding qualifiers to it.
10. **Write `tests/org_rulesets/test_page.py`.**
    - Keep the tests at attempt-2.diff:142-193. Change the private-name test as described in the T6.AC3 row.
    - Add `test_every_refusal_and_failure_message_is_on_the_page(orr, page)`:
      - Read `Path(orr.__file__).read_text()`.
      - Collect messages with `re.findall(r'(?:problems\.append|stop|fail|UsageError)\(\s*f?"([^"]+)"', src)`, plus `re.findall(r'return None, f"([^"]+)"', src)`, plus `orr._REFUSAL_TEXT.values()`.
      - Turn each message into a pattern with `".+?".join(map(re.escape, re.split(r"\{[^}]*\}", msg.strip())))`.
      - Search for it in the page with whitespace collapsed (`" ".join(page.split())`).
      - Assert that there are at least 20 messages and that every one matches.
    - If `orr` has no `__file__`, check how `tests/org_rulesets/conftest.py` loads the module and use the same path, `ROOT / "scripts" / "apply_org_rulesets.py"`.
11. Run `uv run pytest tests/org_rulesets/ tests/docs/test_branch_protection_rulesets.py`, `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets`. Do not change the script.

Not checked: I did not read `tests/org_rulesets/conftest.py`, so I don't know whether `orr.__file__` exists (step 10 gives a fallback). I also did not check the exact text of the summary paragraph. The new extraction test depends on the script's current call names (`problems.append`, `stop`, `fail`, `UsageError`), so a later rename in the script would break it.
