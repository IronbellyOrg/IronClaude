model: opus (claude-gw-tier1a alias) family: claude rung: top (escalation 2 always uses the top rung)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T1.AC1 | It was not missed. The reviewer marked it met in all three rounds (/home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/retries/T1/review-1.md:2, review-2.md:4, review-3.md:3). | Keep section 1 (the base-commit record) and section 2 (the release-gate decision and the G1 to G6 table) exactly as attempt 3 had them. |
| T1.AC2 | It was not missed. Marked met in all three rounds (review-1.md:3, review-2.md:5, review-3.md:4). | Keep O1, O2 and O4 exactly as attempt 3 had them, including the two literal sentence starts in O4. |
| T1.AC3 | Attempts 1 and 2 wrote the list by hand, starting from tests already known. Nothing proved the set of tests was closed, so each round found missing pins (review-1.md:5-6, review-2.md:7). Attempt 3 pasted raw script output. That output cannot show a rule that lives outside an `assert` line. For example, the banned-word regex and the file set of `test_tn50_core_pure_no_gh_git_tokens` sit in `token = re.compile(...)` and `CORE_PURE_FILES` (tests/pr_submit/test_static_grep.py:37-53, :136-145), while the assert reads only `assert not offenders`. The same holds for the Tier 2 rule and its `_PRE_EXISTING_VALIDATOR_LINES` exemptions (tests/pr_submit/test_conflict_sync_protocol.py:406-427). The script also dropped literals that look like paths, but some pins are paths: `name = "collect-conflict-evidence.sh"` (tests/pr_submit/test_conflict_sync_protocol.py:430-443, review-3.md:7). Its rule for deciding which tests read the files also has a gap that the reviewer did not name. `test_gh_command_lines_are_repo_scoped` reads `NEW_REFS` and the scripts through `_command_lines`, not through a read call the script recognises (tests/pr_submit/test_conflict_sync_protocol.py:459-478). That test does not appear in attempt 3's Pass B list. Both ways of building the list failed for the same reason: neither tied the record's contents to a list of tests that someone else can regenerate and check. | Remove the scan block and `o3-pin-scan.py`. Build the list of tests with recorded `rg` commands that match every test-module constant pointing at a pr-submit file, plus every use of those constants. Do not require a read call, filter by length or form, or truncate anything. For each test function on that list, write one card by hand that spells out the rule in full: files expanded from constants, every string the test requires or bans copied verbatim (path-like strings included), regexes quoted, the line scope and the exemptions. |

differs-by: The record's O3 content is one hand-written card per test, with every constant, helper and regex spelled out. The list of tests comes from a recorded grep for constants that point at pr-submit files, so script output is only a checklist and never the record's content.

steps:
1. Rebuild `/home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md`. Keep sections 1 and 2 and O1, O2 and O4 from attempt 3 unchanged. Delete the `o3-scan` block and its "Complete by construction" sentence. Delete `artifacts/o3-pin-scan.py`.
2. Add section O3.1, "How the test list was built". Paste each command and its full output. Use the Grep tool or `rg` only, with no interpreter and no network call.
   - (a) Find the binding sites: `rg -n -e 'sc-pr-submit-protocol' -e 'pr-submit\.md' tests --glob '*.py'`. Record each module-level name bound there (for example `SKILL_DIR`, `SKILL_MD`, `_SKILL_MD`, `COMMAND_MD`).
   - (b) Repeat the search with `rg -n -w` for those names to find the aliases built from them (for example `NEW_REFS`, `CORE_PURE_FILES`, `INTENT_REF`, `EVIDENCE_SCRIPT`, `MECHANICAL_REF`, `POLL_SCRIPT`, `RETRIGGER_SCRIPT`). Keep going until no new name appears.
   - (c) Find every use site of the full name set in those files with `rg -n -w`. Each enclosing `test_*` function is one card. A helper's rule goes into the card of each test that calls it.
   - (d) Find tests that scan whole folders: `rg -l -e 'rglob\(' -e 'glob\("\*/SKILL\.md"\)' -e 'AUDIT_ROOTS' tests --glob '*.py'`. Keep those whose root covers `src/superclaude/skills` or `src/superclaude/commands`, including the `WRITE_VERB_CLASSIFICATION` tests in `tests/skills/test_worker_contract.py`, and give each kept file a one-line reason.
   - Output of this section: one sorted list of `path::test_name` ids.
3. Under O3.2, write one card per id, headed `#### tests/<file>.py::<test_name>`. Each card has these fields:
   - **files:** constants expanded to repo-relative paths. For example, `CORE_PURE_FILES` becomes its four refs and five `.py` modules.
   - **lines checked:** every line, fenced lines only (`_command_lines`), the prose form (`_prose`), or logical lines of a `.sh` file joined at backslashes.
   - **rule kind:** must contain, must not contain, regex must not match, order (`A` before `B`), count (for example, exactly one python fence) or exact key-set equality.
   - **literal:** each required or banned string, copied verbatim from the function body, the constants it names and the helpers it calls. Include path-like strings such as `collect-conflict-evidence.sh` and `conflict-intent.md`. Escape newlines as `\n` and truncate nothing.
   - **exemptions:** for example, `_PRE_EXISTING_VALIDATOR_LINES` and `_GH_MESSAGE_LINES`, quoted verbatim.
   - **tasks affected:** which of Tasks 7 to 13 could break this rule.
   - Label the inputs the test feeds to its own regex (such as the `git push --force` samples) as "test input, not a pin". Write the `WRITE_VERB_CLASSIFICATION` card as before: exact stripped line key, category, stale-entry test. Quote every key whose text appears in a pr-submit file.
4. Before handing in, confirm that cards exist and spell out the rule for:
   - every item in review-3.md:6: `test_tn50_core_pure_no_gh_git_tokens` with the regex `\bgh\b|\bgit\b` and the nine files; `test_intent_and_validator_lines_say_tier_2`; `test_t1101_retrigger_gh_is_repo_scoped`; `test_evidence_script_named_only_in_conflict_intent`; and the `SKILL.md` classification keys;
   - every item in review-2.md:7 and review-1.md:5;
   - `test_gh_command_lines_are_repo_scoped`.

   If one is missing from the step 2 output, fix the grep in step 2. Do not add the card by hand.
5. Replace the completeness sentence with exactly: "Every id produced by the commands in O3.1 has exactly one card below; nothing is filtered by length or form and no text is truncated." Then add the reviewer's check:
   - run the O3.1 commands again;
   - compare their id list with `rg -o '^#### tests/\S+::\w+' pre-build-gate.md`; the two must match one for one;
   - open any card's test and confirm that every string literal in its body, and in the constants and helpers it uses, appears in the card or is labelled as test input.
6. Make no GitHub or network call. Stage with `git add .dev/tasks`.
