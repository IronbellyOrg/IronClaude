<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer 1 card, analyzer, opus class) -->
<!-- Merge date: 2026-11-25T20:50:00Z -->
persona: merged (analyzer + qa)
model_class: merged (opus + haiku)
model_alias_resolves_to: claude-gw-tier1a
reviewer_model_self_report: claude-gw-tier1a[1m] (analyzer); GPT-5.2 (qa)

## Findings

<!-- Source: Plan (Change #11) - grade summary inserted -->
Grade summary: Blocking 2 (A1, A2); Medium 2 (A3, A10); Note 10 (A4, A5, A6, A7, A8, A9, A11, A12, A13, A14). Counts for the contract: {blocking: 2, label_high: 0, medium: 2, note: 10}.

<!-- Source: Base (original, modified) - Q1 evidence and INV-004 details appended per Change #1 -->
A1. Blocking (Missing: no task adds the classification entry that `tests/skills/test_worker_contract.py` needs for the new `gh api` line. This affects Task 1 and Task 6's third acceptance check.)
- Claim: I checked the card's F1 against the files and it is true. Task 1 adds a Wave 2 line to `refs/claim.md` that contains `gh api`. The test scans every line under `src/superclaude/skills`, `commands` and `agents`, and fails for any `gh api` or `gh pr` line whose exact stripped text is not a key in `WRITE_VERB_CLASSIFICATION`. No task edits that table. There is a second risk: Task 2 does not forbid naming the call in the SKILL.md error table, and the table already does this for other calls, so an implementer copying that style would add another unclassified line.
- Consequence: after Task 1, `test_every_write_verb_hit_is_classified` fails. Task 6's check "shows no new failure compared with the same run before Task 1" cannot pass unless someone makes an edit that no task owns. The new line is a plain GET (no `-f`, `-F`, `--input` or `-X`), so a `read-only` entry would also pass `test_read_only_entries_are_not_gh_api_posts`.
- Fix: add the entry as a step in Task 1 or Task 6, after the Wave 2 line's final wording is settled. Keep `gh api` out of the SKILL.md, command and guide wording. The entry is keyed by the whole stripped line, including its leading item number, so it must be written from the final wording of the new line (in the same edit as the line, or after it); a later rewording or renumbering turns it stale (test_worker_contract.py:3171-3176). In a Python literal the jq text `\(` must be written `\\(` (ruff W605 is selected at pyproject.toml:185; the existing entry at test_worker_contract.py:2047 does this). Task 6's lint criterion names only tests/skills/test_issue_protocol.py although `make lint` is repo-wide (Makefile:48-50); it should name tests/skills/test_worker_contract.py too.
- Evidence:
  - `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:30`: "run `gh api --paginate repos/<R>/issues/<N>/dependencies/blocked_by --jq"
  - `tests/skills/test_worker_contract.py:1894-1896`: `r"|gh\s+(?:pr|api))(?![\w-])"`
  - `tests/skills/test_worker_contract.py:1952-1955`: "{(path, verb, line) for path, verb, line, _ in _scan_write_verbs()} - set(WRITE_VERB_CLASSIFICATION)"
  - `tests/skills/test_worker_contract.py:1953-1956`: "set(WRITE_VERB_CLASSIFICATION)" followed by "assert not missing"
  - `tests/skills/test_worker_contract.py:3167-3168`: "def test_every_write_verb_hit_is_classified():"
  - `src/superclaude/skills/sc-issue-protocol/SKILL.md:172`: "| `gh issue comment <N> --repo <R>` or the `gh api -X PATCH repos/<R>/issues/comments/<id>` edit fails |"
  - Plan line 91: "tests/skills/test_worker_contract.py ... shows no new failure compared with the same run before Task 1"
  - I also confirmed the card's F3: no test pins the old Wave 2 item 5 text ("Earlier claim", "re-claim is allowed").

<!-- Source: Base (original, modified) - claim, consequence and fix replaced with the verified gh probe and the refined precedence rule per Change #2 -->
A2. Blocking (Decision: Task 1's Wave 2 rule does not say which wins when the call fails but still prints something. This affects Task 1's outcome rule and the Task 6 test that pins it.)
- Claim: Task 1 gives two rules that clash: 'Any output line is an open blocker' (STOP) and 'A failed call (non-zero exit ...) means continue'. It never says which is checked first. Verified on 2026-11-25 with gh 2.103.0 (read-only GET, the exact command of plan line 30): for a missing issue (999999 on IronbellyOrg/IronClaude) the call exits 1, prints the raw error JSON `{"message":"Not Found",...,"status":"404"}` on stdout (the `--jq` filter is skipped) and `gh: Not Found (HTTP 404)` on stderr; for issue 612 it exits 0 and prints `#611 https://github.com/IronbellyOrg/IronClaude/issues/611`; for issue 590 it exits 0 with no output. So 'any output line is an open blocker' applied to a failed read stops the claim with E-BLOCKED, which the spec forbids ('continue ... when the list cannot be read'). Only a 404 was observed, not a 403 or a server without the endpoint.
- Consequence: A failed read becomes a wrong E-BLOCKED stop, and every acceptance check still passes, because Task 1's checks and Task 6's tests only look for the three outcomes in the text.
- Fix: State the precedence in Task 1 and pin it in Task 6: (1) any output line that matches `^#[0-9]+ https://` is an open blocker and stops the claim with E-BLOCKED whatever the exit status (a failed later page of a paginated read can follow earlier pages that already printed blockers; observed with a failing `--jq` on page 2: lines printed, then exit 1); (2) otherwise a non-zero exit, or any output that does not match, means 'could not run' and the claim continues; (3) otherwise there are no open blockers. The raw error JSON does not match the pattern, so the 404 case is 'could not run'. The repo's existing calls guard on exit status first (settle.sh:371-375).
- Evidence:
  - Plan line 30: "Any output line is an open blocker, and the claim STOPs `E-BLOCKED`" and "A failed call (non-zero exit, for example no access or an endpoint that is not served) means continue as today"
  - Plan line 35: "The Wave 2 item states all three outcomes"
  - `src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:371`: `tl=$(gh api --paginate "repos/$GH_REPO/issues/$ISSUE_N/timeline?per_page=100" --jq ... 2>/dev/null) ||`

<!-- Source: Base (original, modified) - claim softened to "not guaranteed", fix reworded, the assign-failure example dropped per Change #3 -->
A3. Medium: the "could not run" line is only printed when a claim finishes normally.
- Claim: the plan adds the `Blocker check: could not run (<reason>)` line only to `## Final output` item 4, which prints at a normal end. Later STOPs do not route through it, and nothing makes them print the held line. Examples after Wave 3 has assigned the issue: E-TIER-UNAVAILABLE and E-WORKER-NO-OUTPUT (Wave 4), E-POST-FAILED (Wave 6).
- Consequence: the user is not guaranteed to be told the claim went ahead without the blocker check. The spec does not cover this later-STOP path, so this is not graded blocking.
- Fix: add one sentence to Task 1: a later STOP prints the held line before the STOP message; add one Task 6 assertion for it.
- Evidence:
  - Plan line 30: "In `## Final output`, extend item 4 (the warnings item)"
  - `src/superclaude/skills/sc-issue-protocol/SKILL.md:150`: "On a STOP, also print the STOP code and its message."
  - `src/superclaude/skills/sc-issue-protocol/refs/claim.md:138`: "## Final output (replaces \"print the path and STOP\")"

<!-- Source: Base (original, modified) - regraded Medium to Note and consequence rewritten per Change #4 -->
A4. Note: Task 1 asks for wording close to a phrase an existing test forbids, and the plan does not warn about it.
- Claim: Task 1 says the new item states that "it runs for a re-claim and for every `--pipeline` value". An existing test forbids the exact string "Runs for every `--pipeline` value" anywhere in `claim.md`. The Constraints section lists other test traps but not this one.
- Consequence: a capitalised rewrite fails the test; Task 6's test run catches it.
- Evidence:
  - Plan line 30: "The item says it runs for a re-claim and for every `--pipeline` value."
  - `tests/skills/test_issue_protocol.py:625`: "assert \"Runs for every `--pipeline` value\" not in claim"

<!-- Source: Base (original, modified) - INV-005 detail appended per Change #5 -->
A5. Note: another unlisted text trap in `claim.md`.
- Claim: one test splits `claim.md` on the literal text "## Final output" and expects exactly two pieces. If the new Wave 2 item names the target as `## Final output` (the plan's own acceptance criteria write it that way), that test breaks. The edit wording at line 30 ("for the final output") is safe. Today `## Final output` occurs once in claim.md (`grep -c`); the plan's own Task 1 text uses that notation, so copying it into the new Wave 2 item would add a second occurrence.
- Evidence:
  - `tests/skills/test_issue_orca_worktree.py:1788-1790`: "wave8, final = ( (SCRIPT.parents[1] / \"refs/claim.md\").read_text().split(\"## Final output\")"
  - Plan line 36: "`## Final output` carries the `Blocker check: could not run` line rule."

<!-- Source: Base (original) -->
A6. Note: Task 3 does not warn that `issue.md` may not contain `--repo`.
- Claim: `commands/issue.md` may not contain the text `--repo` anywhere. The planned sentence is plain prose, so it is safe as written. But Constraint line 21 suggests `gh api` paths might appear in that file, and any `gh issue ... --repo <R>` example there would fail the test.
- Evidence:
  - `tests/commands/test_issue_command.py:179`: "assert \"--repo\" not in text"
  - Plan line 21: "Inside the skill files and the command file ... keep every `gh api` path spelled `repos/<R>/...`"

<!-- Source: Base (original, modified) - claim sentence corrected per Change #6 -->
A7. Note: the Wave 2 heading becomes slightly wrong.
- Claim: the heading says the orchestrator reads `<D>/scout.md`, and SKILL.md:86 names scout.md as the wave's input; after Task 1 one item reads GitHub directly. Task 1 leaves the heading unchanged. Tests match only `## Wave 2\b`, so nothing breaks.
- Evidence: `src/superclaude/skills/sc-issue-protocol/refs/claim.md:36`: "## Wave 2: edge cases (orchestrator reads `<D>/scout.md`)"

<!-- Source: Base (original, modified) - orchestrator ruling appended per Change #7 -->
A8. Note: no `make sync-dev` / `make verify-sync` step.
- Claim: the project workflow says to run both after editing skills or commands under `src/`, and the plan does neither. CI runs `make sync-dev` before `make verify-sync`, so CI is unaffected. A local `make verify-sync` would report drift for `sc-issue-protocol` and `issue.md` until sync-dev runs. Graded Note after the debate: the workflow template makes final whole-plan verification executor-owned and forbids verification-only tasks, and the plan's Constraints already name `make sync-dev` as the source of the generated copies. One advocate argued for Blocking (a required step absent); the orchestrator ruled Note.
- Evidence: `.github/workflows/test.yml:127-131`: "make sync-dev ... make verify-sync"

<!-- Source: Base (original) -->
A9. Note: Task 4's acceptance wording is loose.
- Claim: `git diff --stat` prints insertion and deletion counts, not a count of changed lines. "Exactly one changed line" should read "1 insertion(+), 1 deletion(-)".
- Evidence: plan line 68: "`git diff --stat -- src/superclaude/core/HOW-WE-WORK.md` shows exactly one changed line."

<!-- Source: Variant 2 (reviewer 2 card), Q2 - merged per Change #8 -->
A10. Medium: Task 6's ordering check does not pin the order against the assignee checks.
- Claim: the spec requires the blocker check after the closed-issue and assignee checks and before Wave 3. Task 1 states the full order in its acceptance criteria, but the Task 6 helper only diagnoses 'the blocker item is not after the closed-issue item of Wave 2' and its only mutation removes the item, so an edit that moves the item between Wave 2 item 2 (closed) and item 3 (assigned to someone else) passes every new test.
- Consequence: the order is checked once by hand, then unprotected; both orders stop with no write, only the printed message differs, so this is Medium, not Blocking.
- Fix: make the helper check the item is after the assignee items too, and add a mutation test that moves it ahead of them.
- Evidence:
  - `.dev/issues/848/issue-summary.md:11`: 'after the existing closed-issue and assignee checks and before Wave 3'
  - `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:33`: 'sits after the closed-issue item and the assignee item'
  - same plan file, line 86: 'the blocker item is not after the closed-issue item of Wave 2'
  - `src/superclaude/skills/sc-issue-protocol/refs/claim.md:41-43`: Wave 2 items 2 to 4 (closed, assigned to someone else, already assigned)

<!-- Source: Variant 2 (reviewer 2 card), Q3 - merged per Change #9 -->
A11. Note: the coverage record cites only source.md:1. The matrix rows (INF-001 to INF-005) all cite `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/source.md:1`, and the source names `.dev/issues/848/issue-summary.md`, whose extra requirements (order after the assignee checks, blocker numbers and links, no GitHub, ClickUp or Orca write, the four documentation places, regression tests, scope exclusions) are covered by plan lines 19, 30, 33 and Tasks 2 to 6 but are not traced in the record. The matrix is marked `coverage_degraded: parsed-sparse`. This concerns the review record, not the plan.

<!-- Source: Invariant probe (INV-008 and related) - merged per Change #9 -->
A12. Note: Task 4's wording must be ASCII. `tests/core/test_how_we_work_routing_table.py:329-334` fails on any non-ASCII line other than the ruling example; the issue summary uses curly quotes (`.dev/issues/848/issue-summary.md:11`); a `|` inside the new text would break the table row at `src/superclaude/core/HOW-WE-WORK.md:296`; no unknown `/sc:` token may be added (same test file, 282-298). The plan text uses straight quotes but does not say ASCII only.

<!-- Source: Invariant probe (INV-013 with the Round 2 reader omission) - merged per Change #9 -->
A13. Note: two acceptance wordings cannot be evaluated as written. Plan line 91 says 'shows no new failure compared with the same run before Task 1' but no step captures that baseline; plan line 37's `grep -n "gh api" claim.md` criterion read literally can never pass because `src/superclaude/skills/sc-issue-protocol/refs/claim.md:9` names `gh api` without a path (it should say no new non-path `gh api` line). Plan line 91 also omits tests/skills/test_issue_t1_fallback.py and tests/skills/test_issue_worker_agents.py from 'the other readers', which read SKILL.md and refs/claim.md; the planned text does not trip them.

<!-- Source: Invariant probe (INV-010) - merged per Change #9 -->
A14. Note: out of scope; the issue watcher judges a claim by the assignee and an own-login marker (`cli/issue_watch/predicates.py:171-178, 327-341`). An E-BLOCKED stop leaves neither, like the existing closed-issue stops, so a blocked issue may be re-launched on each sweep until the blocker closes (inference; the cycle code was not traced). The issue puts the watcher out of scope; a one-line note only.

<!-- Source: Base (original, modified) - checked-correct list extended per Change #10 -->
What I checked and found correct:
- **Plan references:** every section and line reference in the plan matches the files: Wave 2 items 1 to 5, Final output item 4, SKILL.md Claim mode item 3 and the error-table row, the `issue.md` `--claim` sentence, and the HOW-WE-WORK.md row at line 296.
- **Test names:** every test name the plan cites exists, and so do the helpers it reuses (`_text`, `_wave`, `REFS`, `SKILL`, `COMMANDS`, `ROOT`, `plan_section_problems`).
- **Readers of HOW-WE-WORK.md:** no reader pins the exact text of the `/sc:issue` row. The routing-refresh fixture and the onboarding deck do not depend on it. The level-table copy in `core/CLAUDE.md` is untouched.
- **SKILL.md:** it is 198 lines, so the 500-line limit is safe.
- **Spec coverage:** every spec requirement maps to a task.
- **Wave 2 renumbering and the Final output item 4 extension** break no existing test (tests/skills/test_issue_protocol.py:612-618, 639, 641; no test cites Wave 2 item numbers).
- **Keeping `gh api` out of SKILL.md, commands/issue.md and the guide** is enough: the scan covers skills, commands and agents only (tests/skills/test_worker_contract.py:1886-1890); the plan's Constraints do not state this rule yet.
- **List shapes:** empty, single, closed and many-blocker lists are handled by the filter (probes on issues 590 and 612).
- **Lookup rule:** an orchestrator-run `gh api` read in Wave 2 fits the lookup rule (claim.md:9, 16-18, 25).
- **Fix set:** the consensus fix set is sufficient for Task 6's acceptance criteria if the wording traps are avoided (gates traced at tests/skills/test_worker_contract.py:1951-1958, 3167, 3171-3194; tests/skills/test_issue_protocol.py:664-698, 936-938, 953-958; tests/skills/test_issue_orca_worktree.py:1788-1793; tests/commands/test_routing_plugin_parity.py:24-36).
