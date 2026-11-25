# Refactor plan

## Overview
- Base variant: Variant 1 (variant-1-original.md, reviewer 1 card, analyzer, opus class); score 0.918 against 0.736 (base-selection.md)
- Incorporated from Variant 2: Q1 evidence, Q2, Q3
- Incorporated from the debate and the invariant probe: grade corrections, the verified failed-read evidence, INV-001, INV-003, INV-004, INV-005, INV-008, INV-010, INV-013, and the Round 2 note about readers omitted from plan line 91
- Change count: 11 planned, 4 rejected
- Overall risk: Low (the merged output is a review card, not code)
- Output: `.dev/reflect/pre-addTheGitHubBloc-20261125201724/adversarial/merged-reviewer-card.md`; log: `.dev/reflect/pre-addTheGitHubBloc-20261125201724/adversarial/adversarial/merge-log.md`
- Rule for the executor: edit a COPY of variant-1-original.md; never change a path:line citation or a verbatim quote that the base already holds; every new citation below was read by an agent in this run; write the merged card only to the output path above. Keep the first lines (`persona:`, `model_class:` ...) but change them to `persona: merged (analyzer + qa)` and `model_class: merged (opus + haiku)`; keep both `reviewer_model_self_report` values on one line each (`reviewer_model_self_report: claude-gw-tier1a[1m] (analyzer); GPT-5.2 (qa)`). Use straight ASCII quotes only. No em dashes, no en dashes. Add the provenance comments of the skill.

## Planned Changes

### Change #1: A1 (Blocking, Missing): merge Q1 evidence and the INV-004 details
- Source: Variant 2 Q1; invariant probe INV-004; base A1
- Target: A1 in the base
- Approach: append
- Rationale: both cards and both advocates agree; the debate (C-001, 95 percent) kept the base text and wanted the extra detail
- Risk: Low
- Edits: (a) add to A1's Evidence list: `tests/skills/test_worker_contract.py:1953-1956`: "set(WRITE_VERB_CLASSIFICATION)" followed by "assert not missing" (from Q1). (b) add to A1's Fix paragraph these sentences: "The entry is keyed by the whole stripped line, including its leading item number, so it must be written from the final wording of the new line (in the same edit as the line, or after it); a later rewording or renumbering turns it stale (test_worker_contract.py:3171-3176). In a Python literal the jq text `\(` must be written `\\(` (ruff W605 is selected at pyproject.toml:185; the existing entry at test_worker_contract.py:2047 does this). Task 6's lint criterion names only tests/skills/test_issue_protocol.py although `make lint` is repo-wide (Makefile:48-50); it should name tests/skills/test_worker_contract.py too." (c) keep the grade text unchanged.

### Change #2: A2 (Blocking, Decision): replace the unchecked claim with the verified probe and use the refined rule
- Source: debate Round 2 (Variant 1 rebuttal, orchestrator reproduction); invariant probe INV-001, INV-002
- Target: A2 in the base
- Approach: replace
- Rationale: the base said its gh claim was "not checked in this audit"; it is now verified; INV-001 shows the exit-status-first rule alone drops a proven blocker on a later-page failure
- Risk: Medium (rewrites the base's fix)
- Replacement for the Claim bullet and sub-bullets, keep the heading line of A2 and its grade: "Task 1 gives two rules that clash: 'Any output line is an open blocker' (STOP) and 'A failed call (non-zero exit ...) means continue'. It never says which is checked first. Verified on 2026-11-25 with gh 2.103.0 (read-only GET, the exact command of plan line 30): for a missing issue (999999 on IronbellyOrg/IronClaude) the call exits 1, prints the raw error JSON `{"message":"Not Found",...,"status":"404"}` on stdout (the `--jq` filter is skipped) and `gh: Not Found (HTTP 404)` on stderr; for issue 612 it exits 0 and prints `#611 https://github.com/IronbellyOrg/IronClaude/issues/611`; for issue 590 it exits 0 with no output. So 'any output line is an open blocker' applied to a failed read stops the claim with E-BLOCKED, which the spec forbids ('continue ... when the list cannot be read'). Only a 404 was observed, not a 403 or a server without the endpoint."
- Replacement for the Consequence bullet: "A failed read becomes a wrong E-BLOCKED stop, and every acceptance check still passes, because Task 1's checks and Task 6's tests only look for the three outcomes in the text."
- Replacement for the Fix bullet: "State the precedence in Task 1 and pin it in Task 6: (1) any output line that matches `^#[0-9]+ https://` is an open blocker and stops the claim with E-BLOCKED whatever the exit status (a failed later page of a paginated read can follow earlier pages that already printed blockers; observed with a failing `--jq` on page 2: lines printed, then exit 1); (2) otherwise a non-zero exit, or any output that does not match, means 'could not run' and the claim continues; (3) otherwise there are no open blockers. The raw error JSON does not match the pattern, so the 404 case is 'could not run'. The repo's existing calls guard on exit status first (settle.sh:371-375)."
- Remove the base's sub-bullet about gh's source knowledge and the sentence about a paginated failure being a risk in the Consequence.

### Change #3: A3 (Medium): soften the claim and add the fix wording
- Source: debate Round 2 (both advocates agree on "not guaranteed to print"); invariant probe INV-003
- Target: A3 in the base
- Approach: replace
- Rationale: base said a later STOP "prints only the STOP code, its message and the return contract"; SKILL.md:150 says "also print", so "never told" overstates; the example E-ASSIGN-FAILED writes nothing
- Risk: Low
- Edits: Claim: "the plan adds the `Blocker check: could not run (<reason>)` line only to `## Final output` item 4, which prints at a normal end. Later STOPs do not route through it, and nothing makes them print the held line. Examples after Wave 3 has assigned the issue: E-TIER-UNAVAILABLE and E-WORKER-NO-OUTPUT (Wave 4), E-POST-FAILED (Wave 6)." Consequence: "the user is not guaranteed to be told the claim went ahead without the blocker check." Fix: "add one sentence to Task 1: a later STOP prints the held line before the STOP message; add one Task 6 assertion for it." Keep the grade Medium and its evidence list; drop E-ASSIGN-FAILED from the examples.

### Change #4: A4 (Medium to Note)
- Source: debate (both advocates, Round 2)
- Target: A4 in the base
- Approach: regrade
- Rationale: the plan's wording at line 30 does not contain the forbidden text; only a capitalised rewrite fails, and Task 6's test run catches it
- Risk: Low
- Edits: change "Medium" to "Note" in the A4 heading line and rewrite its Consequence to "a capitalised rewrite fails the test; Task 6's test run catches it".

### Change #5: A5 and A6 (Notes): add INV-005 detail and keep the grade
- Source: invariant probe INV-005
- Target: A5 and A6 in the base
- Approach: append
- Edits: to A5 add: "Today `## Final output` occurs once in claim.md (`grep -c`); the plan's own Task 1 text uses that notation, so copying it into the new Wave 2 item would add a second occurrence." No change to A6.

### Change #6: A7 (Note): correct the claim
- Source: debate (Variant 2 advocate, accepted by Variant 1)
- Target: A7 in the base
- Approach: replace
- Edits: replace the claim sentence with: "the heading says the orchestrator reads `<D>/scout.md`, and SKILL.md:86 names scout.md as the wave's input; after Task 1 one item reads GitHub directly. Task 1 leaves the heading unchanged. Tests match only `## Wave 2\b`, so nothing breaks." Keep the evidence line.

### Change #7: A8 (Note): add the ruling
- Source: orchestrator ruling in debate-transcript.md
- Target: A8 in the base
- Approach: append
- Edits: append: "Graded Note after the debate: the workflow template makes final whole-plan verification executor-owned and forbids verification-only tasks, and the plan's Constraints already name `make sync-dev` as the source of the generated copies. One advocate argued for Blocking (a required step absent); the orchestrator ruled Note."

### Change #8: add A10 (Medium, Missing) from Variant 2's Q2
- Source: Variant 2 Q2 (graded Medium after both advocates conceded)
- Target: new finding after A9 in the base
- Approach: insert
- Text: "A10. Medium: Task 6's ordering check does not pin the order against the assignee checks.
- Claim: the spec requires the blocker check after the closed-issue and assignee checks and before Wave 3. Task 1 states the full order in its acceptance criteria, but the Task 6 helper only diagnoses 'the blocker item is not after the closed-issue item of Wave 2' and its only mutation removes the item, so an edit that moves the item between Wave 2 item 2 (closed) and item 3 (assigned to someone else) passes every new test.
- Consequence: the order is checked once by hand, then unprotected; both orders stop with no write, only the printed message differs, so this is Medium, not Blocking.
- Fix: make the helper check the item is after the assignee items too, and add a mutation test that moves it ahead of them.
- Evidence:
  - `.dev/issues/848/issue-summary.md:11`: 'after the existing closed-issue and assignee checks and before Wave 3'
  - `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md:33`: 'sits after the closed-issue item and the assignee item'
  - same plan file, line 86: 'the blocker item is not after the closed-issue item of Wave 2'
  - `src/superclaude/skills/sc-issue-protocol/refs/claim.md:40-44`: Wave 2 items 2 to 4 (closed, assigned to someone else, already assigned)"

### Change #9: add A11 (Note) from Variant 2's Q3 and A12 to A14 (Notes) from the probe
- Source: Variant 2 Q3; INV-008; INV-013 with the Round 2 reader omission; INV-010
- Target: new findings after A10
- Approach: insert
- Text:
  - "A11. Note: the coverage record cites only source.md:1. The matrix rows (INF-001 to INF-005) all cite `.dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/source.md:1`, and the source names `.dev/issues/848/issue-summary.md`, whose extra requirements (order after the assignee checks, blocker numbers and links, no GitHub, ClickUp or Orca write, the four documentation places, regression tests, scope exclusions) are covered by plan lines 19, 30, 33 and Tasks 2 to 6 but are not traced in the record. The matrix is marked `coverage_degraded: parsed-sparse`. This concerns the review record, not the plan."
  - "A12. Note: Task 4's wording must be ASCII. `tests/core/test_how_we_work_routing_table.py:329-334` fails on any non-ASCII line other than the ruling example; the issue summary uses curly quotes (`.dev/issues/848/issue-summary.md:11`); a `|` inside the new text would break the table row at `src/superclaude/core/HOW-WE-WORK.md:296`; no unknown `/sc:` token may be added (same test file, 282-298). The plan text uses straight quotes but does not say ASCII only."
  - "A13. Note: two acceptance wordings cannot be evaluated as written. Plan line 91 says 'shows no new failure compared with the same run before Task 1' but no step captures that baseline; plan line 37's `grep -n \"gh api\" claim.md` criterion read literally can never pass because `src/superclaude/skills/sc-issue-protocol/refs/claim.md:9` names `gh api` without a path (it should say no new non-path `gh api` line). Plan line 91 also omits tests/skills/test_issue_t1_fallback.py and tests/skills/test_issue_worker_agents.py from 'the other readers', which read SKILL.md and refs/claim.md; the planned text does not trip them."
  - "A14. Note (out of scope): the issue watcher launches `/sc:issue --claim N --pipeline none` and judges a claim by the assignee and an own-login marker (`cli/issue_watch/launch.py:1-5`, `cli/issue_watch/predicates.py:171-178, 327-341`). An E-BLOCKED stop leaves neither, like the existing closed-issue stops, so a blocked issue may be re-launched on each sweep until the blocker closes (inference; the cycle code was not traced). The issue puts the watcher out of scope; a one-line note only."

### Change #10: update the "What I checked and found correct" list
- Source: invariant probe INV-006, INV-007, INV-009, INV-011, INV-012; Variant 2 (no list)
- Target: the closing list of the base
- Approach: append
- Edits: add bullets: "Wave 2 renumbering and the Final output item 4 extension break no existing test (tests/skills/test_issue_protocol.py:612-618, 639, 641; no test cites Wave 2 item numbers)", "keeping `gh api` out of SKILL.md, commands/issue.md and the guide is enough: the scan covers skills, commands and agents only (tests/skills/test_worker_contract.py:1886-1890); the plan's Constraints do not state this rule yet", "empty, single, closed and many-blocker lists are handled by the filter (probes on issues 590 and 612)", "an orchestrator-run `gh api` read in Wave 2 fits the lookup rule (claim.md:9, 16-18, 25)", "the consensus fix set is sufficient for Task 6's acceptance criteria if the wording traps are avoided (gates traced at tests/skills/test_worker_contract.py:1951-1958, 3167, 3171-3194; tests/skills/test_issue_protocol.py:664-698, 936-938, 953-958; tests/skills/test_issue_orca_worktree.py:1788-1793; tests/commands/test_routing_plugin_parity.py:24-36)".

### Change #11: add a grade summary at the top of the merged card
- Source: this plan
- Target: just under the `## Findings` heading
- Approach: insert
- Text: "Grade summary: Blocking 2 (A1, A2); Medium 2 (A3, A10); Note 10 (A4, A5, A6, A7, A8, A9, A11, A12, A13, A14). Counts for the contract: {blocking: 2, label_high: 0, medium: 2, note: 10}."

## Changes NOT Being Made
| Diff point | Non-base approach | Why the base approach stays |
|---|---|---|
| C-001 | Q1's shorter wording | A1 holds the same finding with more detail (95 percent, both advocates) |
| C-002 | Q2 graded Blocking (Decision) | both advocates conceded Medium; either order stops with no write |
| C-004 | Q3 graded Medium | graded Note: it concerns the review record, not the plan |
| C-007 | A8 graded Blocking (one advocate) | orchestrator ruling: Note (executor-owned verification) |

## Risk Summary
- Change #2 rewrites A2's fix: risk Medium, rollback: restore variant-1-original.md text of A2.
- All other changes are additive or regrades: risk Low.

## Review Status
Auto-approved (non-interactive); timestamp 2026-11-25T20:50:00Z.
