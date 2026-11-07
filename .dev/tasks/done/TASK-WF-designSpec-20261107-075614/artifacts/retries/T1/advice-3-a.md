model: opus (claude-gw-tier1a alias) family: claude rung: top (executor tier unknown, so adviser A takes the top rung)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T1.AC1 | Not missed. The reviewer marked it met in both rounds (/home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/retries/T1/review-1.md:2, .../review-2.md:4). | Keep the content as it was: the three-command base-commit record, the owner's release-gate wording and the G1 to G6 table. Only rebuild the file around it. |
| T1.AC2 | Not missed. Marked met twice (review-1.md:3, review-2.md:5). | Keep O1, O2 and O4 as they were, naming files and symbols, with no line numbers. |
| T1.AC3 | The O3 list was written by hand, test by test, starting from tests already known to read the files. Each round found pins that list had missed: A5, cosmos and byte-identical pins (review-1.md:5-6), then the wait-only sentences, the force-push rule, the silence tokens, the fallback flag, the re-trigger repo-scope rule and SKILL_EDITS E1 to E13 (review-2.md:7). A list that starts from known test names cannot be shown complete. Pins also come through shapes it does not follow: module constants (SKILL_EDITS at tests/pr_submit/test_conflict_sync_protocol.py:231), parametrized f-strings (tests/commands/test_impact_command.py:345-362), rules that apply to every file (tests/pr_submit/test_static_grep.py:761-779) and the core-pure no-gh/git rule on state-machine.md and loop-guard.md (tests/pr_submit/test_static_grep.py:37-40, 134-145). The reviewer also counts pins on refs/ci-poll.md and refs/review-retrigger.md (review-2.md:7), which are outside the brief's four files. | Produce the O3 list with a read-only scan that can be run again. Pass A treats any test string literal found verbatim in a pr-submit file as a pin. Pass B collects every assert in tests that read those files, which covers absence checks and line rules. Paste the scan output unedited into pre-build-gate.md between markers. The reviewer checks completeness by running the scan again and diffing. Scan the whole skill folder plus commands/pr-submit.md, and label each row with its file, so both the brief's four-file scope and the reviewer's wider scope are covered. |

differs-by: The list is defined by a scan that starts from the pr-submit files' text and finds every test that touches them. It does not start from tests someone picked. Its output is pasted unedited and can be checked with a diff.

steps:
1. Rebuild `.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md` with the parts already accepted (review-2.md:4-5, review-1.md:4): the base-commit record, the release-gate decision, the G1 to G6 table, O1, O2, O4, the classification-table rule (exact line key, category, stale-entry test) and the literal start text of the S5a and Wave 6 pre-push sentences.
2. Write `.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py`. It uses only the standard library (`ast`, `pathlib`, `re`), only reads files, prints to stdout and makes no network calls. Its inputs:
   - **Target files:** every `.md` and `.sh` file under `src/superclaude/skills/sc-pr-submit-protocol/`, plus `src/superclaude/commands/pr-submit.md`. For each, keep the raw text and a prose form `" ".join(raw.replace("\n> ", " ").split())`, the same form `_prose` in tests/pr_submit/test_static_grep.py uses.
   - **Scanned tests:** `tests/pr_submit/*.py` including conftest, `tests/skills/test_worker_contract.py`, `tests/commands/test_impact_command.py`, `tests/core/test_how_we_work_routing_table.py`, and every other `tests/**/*.py` whose text contains `sc-pr-submit-protocol` or `pr-submit`.
3. **Pass A (exact-text pins):** take every `ast.Constant` string of 8 or more characters, plus each fixed part of every f-string, from the scanned tests. Keep it if it appears in a target's raw or prose text and is not just a file path.
   - Emit one row per kept string: `test-file::owner | target file(s) | how it is checked (in, index, startswith, set member, other) | the literal`, with newlines escaped as `\n`.
   - The owner is the enclosing test function. If there is none, use the module constant and its key (for example `SKILL_EDITS[E3]` or a `WRITE_VERB_CLASSIFICATION` key), or the helper function name.
4. **Pass B (absence checks and line rules):**
   - A **reader** is a test function whose source, including its decorators, contains a target token (`sc-pr-submit-protocol`, `pr-submit.md`, `state-machine.md`, `loop-guard.md`, `ci-poll.md`, `review-retrigger.md`). It is also a reader if it references a module-level name whose value contains one of those tokens, following names that refer to other names (for example `SKILL_DIR`, then `_SKILL_MD`, then `CORE_PURE_FILES`), or if it calls a helper that does.
   - For every reader, emit `test-file::test-name` and the verbatim source of each assert and each `re.*` pattern literal it contains.
5. End the output with a footer: the list of scanned files, the list of target files, the row count of each pass, and the exact command used. The output must contain no line numbers, because the global constraint says to cite by symbol name.
6. Run `uv run python /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/o3-pin-scan.py`. Paste stdout unedited into O3 between `<!-- o3-scan:begin -->` and `<!-- o3-scan:end -->`. Add one sentence above the block: "Complete by construction: re-run the command in the footer and diff against this block."
7. Self-check before handing in. Each of these must appear in the block:
   - test_skill_states_the_a5_rules
   - test_protocol_refs_pin_live_boundaries_and_existing_gates
   - test_spec_byte_identical_fragments_survive
   - test_wait_only_sentences_name_the_one_sync_exception (all three files)
   - test_skill_forbids_force_push (the Will Not Do sentence and the regex)
   - test_skill_pins_inv_s1_silence_rerequest_tokens
   - test_t1115_auggie_fallback_flag_parity
   - test_t1101_retrigger_gh_is_repo_scoped
   - SKILL_EDITS E1 to E13
   - test_tn50_core_pure_no_gh_git_tokens
   - test_impact_callers_wired and test_impact_callers_may_invoke_skill
   - test_intent_and_validator_lines_say_tier_2
   - the WRITE_VERB_CLASSIFICATION SKILL.md keys

   If any is missing, fix the scan, not the pasted block.
8. Make no GitHub or network calls. Stage with `git add .dev/tasks`.
