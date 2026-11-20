# Tier 1 reflection card: stage 3c plan vs request (UC-1, pre-execution)

- SPEC: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/source.md` (cited `source.md:N`)
- PLAN: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/TASK-WF-stage3CRequest-20261119-143901.md` (cited `plan:N`)
- Code: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/src/superclaude/agents/reflect-reviewer.md` (cited `agent:N`), `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/tests/skills/test_review_severity_rule.py` (cited `test:N`)
- Evidence scripts (read-only on the repo): `artifacts/coverage_match.py`, `artifacts/edit_simulation.py` in this folder.

## Summary

If `/sc:implement` runs the two tasks as written, it delivers the code change correctly. The passage, inserted where Task 1 says, reproduces the measured variant file byte for byte (sha256 `7696a2b2...ec0ed8`, the value the spec gives). Every acceptance grep goes from 0 to 1, both test needles match, and no banned-phrase scan fires. The plan drops two things the spec asks for outside the tasks. It never says to run on a fresh branch made from `origin/master`, and it has no summary carrying the spec's three known limits. One of its sentences also states as fact what the spec calls a judgment. Verdict: FAIL on two `Blocking (Missing):` findings. Both are fixed by adding text to the plan; neither task's steps need to change.

## Findings

| ID | Grade | What | Plan file:line | Spec file:line | Evidence |
|---|---|---|---|---|---|
| F1 | `Blocking (Missing):` affected action: choosing the branch that Task 1's edit and the later commit land on | The spec says to run the package on a fresh branch made from `origin/master`. No line of the plan says so. Taken literally, `/sc:implement` edits whatever branch is checked out, for example this worktree's `feature/blocker-classification-stage3b`, and every acceptance line still passes. | plan:17-27 (Constraints, no branch line); plan:31-61 (tasks, none) | source.md:3 | A case-insensitive search of the plan for `branch`, `origin/master` and `summary` returns no match. Containment ratio for this row is 0.4286, so it is unmapped (INF-001). |
| F2 | `Blocking (Missing):` affected action: the owner's go decision and the later reading of the B/E re-runs, which rest on the plan's stated evidence | The spec's section "Known limits to carry into the plan's summary" has three limits. The plan has no summary section, only a Goal line. It carries only the first limit, and only in part: the examples stay. It leaves out "its held-out result on spec B does not depend on them". It also leaves out the small-measurement limit: one model (sonnet), three reviewers per arm, one scorer, no second reader, coverage hints in the briefs. And it leaves out the limit that "plain codepoint order" is a judgment. plan:21 goes further and calls both spec B findings "two real gaps", which states as fact what source.md:69 calls a judgment. | plan:15 (Goal only); plan:21 ("raised two real gaps to Blocking"); plan:22 (limit 1, partial) | source.md:65-69 | INF-034 (ratio 0.1667), INF-037 (0.35) and INF-038 (0.2857) are unmapped. INF-036 matches at 0.75 only because it shares words with plan:21; its meaning is absent. |
| F3 | `Medium:` | Task 1's acceptance lines pin only three things: the passage's opening (`Before you write \`Medium:\``), its last sentence, and its join after the anchor sentence. A retyped passage with an error in the middle, such as a wrong grade token in "grade it `Blocking (Decision):` or `Blocking (Missing):`", passes all three greps and both needles. Only the `git diff` line catches it, and only if the reviewer compares the added text with the fenced block in `./source.md`. The plan does not carry the spec's sha256 or the variant path that would make byte identity checkable. The instruction itself is right ("copied byte for byte ... never retype it"), so following the text as written gives the correct result. | plan:22, plan:34, plan:44-45 | source.md:24, source.md:27, source.md:39-42 | `edit_simulation.py`: inserting the fenced block at the anchor in the current agent gives bytes equal to `.dev/stage3c-variants/brainstorm/reflect-reviewer.md`, sha256 `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8`. So one added check, `sha256sum src/superclaude/agents/reflect-reviewer.md` equals that value, would pin the whole passage. This holds only while the base agent on `origin/master` equals this worktree's copy. |
| F4 | `Note:` | The first grep's escaped backticks (`\``) sit inside a single-backtick Markdown code span. In rendered Markdown the span closes at the first inner backtick, so the command shows up broken. Read as raw text and run in bash, it is correct. | plan:44 | source.md:39 | Running `grep -c "Before you write \`Medium:\`"` in bash prints 1 on the variant file and 0 on the current `agent`. |
| F5 | `Note:` | "Run every test file that output names" (`git grep -n "reflect-reviewer" -- tests src`) also matches fixture YAML files that cannot be run, plus two test files beyond the four: `tests/skills/test_worker_contract.py` and `tests/unit/test_cli_install.py`. A literal executor has to tell test files from fixtures. The wording comes from the spec. | plan:41, plan:48 | source.md:34, source.md:47 | A Grep of `tests/` for `reflect-reviewer` names 10 files, including `tests/cli/reflect/fixtures/panel_lint_legacy/reviewer-cards/reviewer-{1,2,3}-card.yaml` and `tests/review/fixtures/reflect_cards/yaml-deviation-class.yaml`. |

What I checked that produced no finding:

- **Line-number hints.** agent:122 is the Severity column bullet ("near line 122", plan:34). test:214 is `def test_c_reflect_reviewer_grade_bullets_pinned` ("near line 214", plan:35).
- **Anchor uniqueness.** The anchor "a HIGH that is only wording is a Note. When no consumer can be established" occurs once in the agent (agent:122).
- **Acceptance greps (plan:44).** Line counts on the current agent and the simulated edit are 0→1, 0→1 and 0→1. Real `grep -c` on the variant file prints 1, 1, 1. The current agent has no other "Before you write" line, so a count of 1 means exactly this edit.
- **Diff line (plan:45).** The simulated edit changes only line 122, and the file stays at 159 lines.
- **Test needles (plan:35).** Both needles are exact substrings of the passage at source.md:27, and both pass the test's `_flat(needle) in flat` check (test:228) on the simulated edit. Neither needle contains a double quote, so a double-quoted Python string holds it with its backticks unchanged.
- **Dependents (plan:39).** On the edited text, the static scans find nothing: `BANNED_SEVERITY_PHRASES` (test:112), the sweep phrases and F1-F6 (test:408-446), unqualified zero tolerance (test:487) and cap-regression (test:306). S1-S3 are still present (test:197-204), and no `(S[1-5])` label appears (test:207-211). tests/agents/test_codegraph_rosters.py:28 and :73 read the agent's roster and `~/.claude/CODEGRAPH.md`, as plan:39 says. I did not run pytest, so the claim of 83 passing tests is not re-checked.
- **"Not to be done" items (source.md:58-63).** Neither task edits `skills/sc-reflect-protocol`, the adversarial skill, `evidence-validator.md`, `sc-implement-protocol/refs/qa.md`, the CLI or a plugin surface. There is no plugin copy of `reflect-reviewer.md`. `make sync-dev` writes only under `.claude/` (Makefile:109-163), and `make verify-sync` compares agents (Makefile:202-214). Task 2's extra check (plan:61) limits `src` and `plugins` changes to the agent file. That is a narrowing, not a departure.
- **Entry condition (source.md:20, plan:19).** `.dev/tasks/done/TASK-WF-stage3BRequest-20261117-172514/` exists. I did not check whether PR #605 was merged (no git or GitHub calls).

## Coverage summary

From `artifacts/coverage-matrix.md`:

- **Counts.** parsed_count 0, inferred_count 43 (0 dropped), matched count 39.
- **Coverage.** coverage_pct null (parsed-only), coverage_pct_union 0.9070.
- **unmapped_requirements_union:** INF-001, INF-034, INF-037, INF-038.
- **Density and guards.** S_dev_density 0.0930, at or below the 0.20 escalation line. coverage_degraded is parsed-sparse (the parse-density guard fires because inferred 43 > parsed 0).
- **Semantic carriage.** 38 of 43 rows. INF-036 is a containment false positive. INF-009 (the passage) is carried by reference to `./source.md` and not quoted in the plan; INF-027 and INF-028 are carried in Task 2 (plan:60), not in the units containment picked.

## Risks

- **Base drift.** If `origin/master`'s agent:122 differs from this worktree's copy, the anchor or the sha256 equality may not hold. The plan's re-read-by-text rule (plan:26) covers the anchor, not the hash.
- **The effect may not carry over.** The measured gain comes from a small sample (source.md:68). The merge step that kept a correct Blocking card at Medium is out of scope (source.md:60), so the full `/sc:reflect` re-run may still show Medium for the E findings.
- **Wider over-grading.** The passage raises more findings to Blocking. The measurement saw no extra over-grading on two specs, but other review kinds that use `reflect-reviewer` have not been sampled.
- **Unrelated sync failures.** `make verify-sync` checks every skill and agent. Unrelated drift between `src/superclaude/` and `.claude/` could fail Task 2. Running `make sync-dev` first makes this unlikely.

## Self-reported confidence

0.85. The code-level checks were run mechanically (byte equality with the measured variant, grep counts, needles, scans). How severe F1 and F2 are depends on reading the spec's preamble and "Known limits" section as requirements on the plan; that is how the spec words them.
