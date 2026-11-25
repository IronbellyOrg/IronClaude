persona: analyzer
model_class: opus
model_alias_resolves_to: claude-gw-tier1a
reviewer_model_self_report: claude-gw-tier1a[1m]

## Findings

A1. Blocking (Missing: no task adds the classification entry that `tests/skills/test_worker_contract.py` needs for the new `gh api` line. This affects Task 1 and Task 6's third acceptance check.)
- Claim: I checked the card's F1 against the files and it is true. Task 1 adds a Wave 2 line to `refs/claim.md` that contains `gh api`. The test scans every line under `src/superclaude/skills`, `commands` and `agents`, and fails for any `gh api` or `gh pr` line whose exact stripped text is not a key in `WRITE_VERB_CLASSIFICATION`. No task edits that table. There is a second risk: Task 2 does not forbid naming the call in the SKILL.md error table, and the table already does this for other calls, so an implementer copying that style would add another unclassified line.
- Consequence: after Task 1, `test_every_write_verb_hit_is_classified` fails. Task 6's check "shows no new failure compared with the same run before Task 1" cannot pass unless someone makes an edit that no task owns. The new line is a plain GET (no `-f`, `-F`, `--input` or `-X`), so a `read-only` entry would also pass `test_read_only_entries_are_not_gh_api_posts`.
- Fix: add the entry as a step in Task 1 or Task 6, after the Wave 2 line's final wording is settled. Keep `gh api` out of the SKILL.md, command and guide wording.
- Evidence:
  - `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:30`: "run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq"
  - `tests/skills/test_worker_contract.py:1894-1896`: `r"|gh\s+(?:pr|api))(?![\w-])"`
  - `tests/skills/test_worker_contract.py:1952-1955`: "{(path, verb, line) for path, verb, line, _ in _scan_write_verbs()} - set(WRITE_VERB_CLASSIFICATION)"
  - `tests/skills/test_worker_contract.py:3167-3168`: "def test_every_write_verb_hit_is_classified():"
  - `src/superclaude/skills/sc-issue-protocol/SKILL.md:172`: "| `gh issue comment <N> --repo <R>` or the `gh api -X PATCH repos/<R>/issues/comments/<id>` edit fails |"
  - Plan line 91: "tests/skills/test_worker_contract.py ... shows no new failure compared with the same run before Task 1"
  - I also confirmed the card's F3: no test pins the old Wave 2 item 5 text ("Earlier claim", "re-claim is allowed").

A2. Blocking (Decision: Task 1's Wave 2 rule does not say which wins when the call fails but still prints something. This affects Task 1's outcome rule and the Task 6 test that pins it.)
- Claim: Task 1 gives two rules that clash: "Any output line is an open blocker" (STOP) and "A failed call (non-zero exit) means continue". It never says which one is checked first.
  - The model runs the call through the Bash tool, which shows stderr together with stdout, so a failed call shows at least a `gh:` error line.
  - From my knowledge of gh's source (not checked in this audit), `gh api` on an HTTP error also writes the raw error JSON to stdout and skips `--jq`.
  - A paginated read that fails on page 2 after page 1 printed open blockers produces both output and a non-zero exit.
- Consequence: if output is checked first, a 403 or 404 stops the claim with `E-BLOCKED`, which the spec forbids ("continue ... when the list cannot be read"). If exit code is checked first, the partial-page case ignores a known open blocker. Either way every acceptance check still passes, because Task 1's checks and Task 6's tests only look for the three outcomes in the text.
- Fix: state that the exit code is checked first. Any non-zero exit means "could not run", whatever was printed, and only stdout lines of a successful call count as blockers. Pin that order in Task 6. The repo's existing calls already guard on exit status first.
- Evidence:
  - Plan line 30: "Any output line is an open blocker, and the claim STOPs `E-BLOCKED`" and "A failed call (non-zero exit, for example no access or an endpoint that is not served) means continue as today"
  - Plan line 35: "The Wave 2 item states all three outcomes"
  - `src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:371`: `tl=$(gh api --paginate "repos/$GH_REPO/issues/$ISSUE_N/timeline?per_page=100" --jq ... 2>/dev/null) ||`

A3. Medium: the "could not run" line is only printed when a claim finishes normally.
- Claim: the plan adds the `Blocker check: could not run (<reason>)` line only to `## Final output` item 4. A claim whose blocker read failed and that later STOPs (for example `E-ASSIGN-FAILED`, `E-WORKER-NO-OUTPUT`, `E-TIER-UNAVAILABLE` or `E-POST-FAILED`) prints only the STOP code, its message and the return contract. A STOP after Wave 3 has already assigned the issue.
- Consequence: the user is never told the claim went ahead without the blocker check. The spec does not cover this later-STOP path, so this is not graded blocking.
- Evidence:
  - Plan line 30: "In `## Final output`, extend item 4 (the warnings item)"
  - `src/superclaude/skills/sc-issue-protocol/SKILL.md:150`: "On a STOP, also print the STOP code and its message."
  - `src/superclaude/skills/sc-issue-protocol/refs/claim.md:138`: "## Final output (replaces \"print the path and STOP\")"

A4. Medium: Task 1 asks for wording close to a phrase an existing test forbids, and the plan does not warn about it.
- Claim: Task 1 says the new item states that "it runs for a re-claim and for every `--pipeline` value". An existing test forbids the exact string "Runs for every `--pipeline` value" anywhere in `claim.md`. The Constraints section lists other test traps but not this one.
- Consequence: a natural wording such as "Runs for every `--pipeline` value, re-claims included." fails `test_pipeline_none_creates_no_worktree_and_wave_7_skips_it`. Task 6's test run would catch it, but only after an avoidable fix pass.
- Evidence:
  - Plan line 30: "The item says it runs for a re-claim and for every `--pipeline` value."
  - `tests/skills/test_issue_protocol.py:625`: "assert \"Runs for every `--pipeline` value\" not in claim"

A5. Note: another unlisted text trap in `claim.md`.
- Claim: one test splits `claim.md` on the literal text "## Final output" and expects exactly two pieces. If the new Wave 2 item names the target as `## Final output` (the plan's own acceptance criteria write it that way), that test breaks. The edit wording at line 30 ("for the final output") is safe.
- Evidence:
  - `tests/skills/test_issue_orca_worktree.py:1788-1790`: "wave8, final = ( (SCRIPT.parents[1] / \"refs/claim.md\").read_text().split(\"## Final output\")"
  - Plan line 36: "`## Final output` carries the `Blocker check: could not run` line rule."

A6. Note: Task 3 does not warn that `issue.md` may not contain `--repo`.
- Claim: `commands/issue.md` may not contain the text `--repo` anywhere. The planned sentence is plain prose, so it is safe as written. But Constraint line 21 suggests `gh api` paths might appear in that file, and any `gh issue ... --repo <R>` example there would fail the test.
- Evidence:
  - `tests/commands/test_issue_command.py:179`: "assert \"--repo\" not in text"
  - Plan line 21: "Inside the skill files and the command file ... keep every `gh api` path spelled `repos/<R>/...`"

A7. Note: the Wave 2 heading becomes slightly wrong.
- Claim: the heading still says the orchestrator only reads `scout.md`, while the new item 5 makes a live GitHub call. Task 1 leaves the heading unchanged. Tests match only `## Wave 2\b`, so nothing breaks.
- Evidence: `src/superclaude/skills/sc-issue-protocol/refs/claim.md:36`: "## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)"

A8. Note: no `make sync-dev` / `make verify-sync` step.
- Claim: the project workflow says to run both after editing skills or commands under `src/`, and the plan does neither. CI runs `make sync-dev` before `make verify-sync`, so CI is unaffected. A local `make verify-sync` would report drift for `sc-issue-protocol` and `issue.md` until sync-dev runs.
- Evidence: `.github/workflows/test.yml:127-131`: "make sync-dev ... make verify-sync"

A9. Note: Task 4's acceptance wording is loose.
- Claim: `git diff --stat` prints insertion and deletion counts, not a count of changed lines. "Exactly one changed line" should read "1 insertion(+), 1 deletion(-)".
- Evidence: plan line 68: "`git diff --stat -- src/superclaude/core/HOW-WE-WORK.md` shows exactly one changed line."

What I checked and found correct:
- **Plan references:** every section and line reference in the plan matches the files: Wave 2 items 1 to 5, Final output item 4, SKILL.md Claim mode item 3 and the error-table row, the `issue.md` `--claim` sentence, and the HOW-WE-WORK.md row at line 296.
- **Test names:** every test name the plan cites exists, and so do the helpers it reuses (`_text`, `_wave`, `REFS`, `SKILL`, `COMMANDS`, `ROOT`, `plan_section_problems`).
- **Readers of HOW-WE-WORK.md:** no reader pins the exact text of the `/sc:issue` row. The routing-refresh fixture and the onboarding deck do not depend on it. The level-table copy in `core/CLAUDE.md` is untouched.
- **SKILL.md:** it is 198 lines, so the 500-line limit is safe.
- **Spec coverage:** every spec requirement maps to a task.

