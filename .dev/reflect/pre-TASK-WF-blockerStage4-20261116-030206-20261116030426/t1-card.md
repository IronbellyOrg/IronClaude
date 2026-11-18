# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md` (20 lines: the stage 4 plan request; identical to `stage-requests/stage4-request.md`)
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md` (4 phases, 7 tasks, schema workflow-plan/1.2, 116 lines). In this card `P4:n` is line n of that plan, `S3:n` and `S1:n` are lines of the stage 3 plan `TASK-WF-blockerStage3-20261116-030158` and the stage 1 plan `TASK-WF-blockerStage1-20261116-030154` (same folder level), `OLD:n` is line n of the base 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254`.
Author of this card: the orchestrator (self-review; the T2 reviewers exist to break that bias). Executor class (author of the plan) is unknown.
Codegraph run state: index_state=fresh (0 added, 0 modified, 0 removed). Codegraph indexes `.py` and `.yaml` here, not Markdown, so every Markdown claim below was checked with Grep and Read.

## Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0). Step 1B.0 Pass 2 emitted 16 quote-pinned inferred rows (`artifacts/coverage-matrix.yaml`; each quote is a verbatim substring of its cited `source.md` line, asserted by the script). The deterministic containment rule matched 10 of 16, so `coverage_pct_union` is 0.625 and the parse-density guard fired (inferred 16 greater than parsed 0: `coverage_degraded: parsed-sparse`). The six mechanical misses are all requirements that live in the Constraints block, not in a task:

- INF-002 (reuse base Tasks 41 to 46): the task bodies are the reused text; the plan does not name the base plan id. Covered by the task bodies.
- INF-012 (state stage 4, last package, strict T2 here) is at P4:20; INF-013 (end points for later-falsified acceptance lines) is at P4:24; INF-015 and INF-016 (not-to-be-done list, no Jev call) are at P4:22. Covered.
- INF-008 (two `pointer-only` rows stay; cap sentences kept by content): Task 2 holds the pointer-only statement (P4:50, P4:54); the cap kept is checked in Task 3 (P4:64) and Task 4 (P4:75) but Task 2 has no cap acceptance line even though it edits four prompts and the source says caps are kept for the old Tasks 42 to 44 (`source.md:12`). Partly covered (minor).

Every other source requirement maps to a task: templates and allow-list removal (Task 1, P4:33 to 41), rule prompts (Task 2), builders (Task 3), consumer line (Task 4), spec-panel (Task 5), plugin mirror order and the three-test acceptance (Task 6, P4:99 to 105), the owner summary (Task 7, P4:111 to 116).

## Resolution of the earlier review (`.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`, findings that touch stage 4)

- F3/F9/F13 (plugin-mirror allow-list ordering): resolved in Task 6. The plugin mirror of `refs/rule.md` is added to the `canonical` registry rows and to the "Merge-rule allow-list" of `refs/scale-map.md` by path only, then the folder is copied, then the three tests run (P4:99). The existence check on every allow-listed file (OLD:477, stage 3 request) would fail between the allow-list edit and the copy, but no test is run between them.
- F4 (analysis template): resolved. `agent_template_analysis.md` gets the merge-rule text only and the registry keeps 11 `digest` rows (P4:33, P4:38, P4:39); `S1:96` confirms the registry has no analysis row.
- F5/F12 (T3 scope): resolved in text. Task 2 states the `document_review_loop_prompts.md` row is `pointer-only`, checked by T3 and never T1 (P4:50); Task 5 leaves the `src/superclaude/examples/...` mention (`src/superclaude/commands/spec-panel.md:220`, plugin twin :218) in place (P4:87); `S1:209` defines T3 so that `pointer-only` rows are exempt from the `src/superclaude` path check.
- F6 (later tasks falsify earlier acceptance lines): the Constraints add the "until Task N" rule (P4:24). I found no acceptance line in this plan that a later task falsifies, so no end point is needed anywhere.

## Deviation and risk observations (new, from splitting the plan)

1. **Task 1 acceptance line 2 cannot be met as written.** It requires the stage 3 summary `./artifacts/stage3-summary-for-owner.md` to "state that one audit window has passed with no revert trigger tripped" (P4:37). The stage 3 plan makes that file say the opposite: it "states that the audit window runs after this package" and "that no revert trigger can be judged until the audit window has run" (S3:158, S3:162). The file is written inside stage 3, before the window, so nobody can satisfy P4:37 unless the owner edits the stage 3 file afterwards, which no package does. The owner's go row in the ledger (P4:36) is the record that exists after the window.
2. **Allow-list location is mis-named in Tasks 1 and 3.** Both say "remove ... from the allow-list of the stage 3 scan test" (P4:33, P4:59) and their acceptance lines say "passes with the two templates removed from its allow-list" (P4:41, P4:63). The scan test reads its allow-list from the "Merge-rule allow-list" section of `refs/scale-map.md` (`S1:59`, OLD:477), so the edit belongs in `scale-map.md`; the test file holds no list. Task 6 names `scale-map.md` correctly (P4:99), Tasks 1 and 3 do not.
3. **Task 3 acceptance line 3 is not literally true for one file.** It says each of the four files "still contains its 'After 2 fix cycles' sentence" (P4:64). `src/superclaude/skills/tdd/refs/build-request-template.md:125` holds the cap only as "Maximum 2 fix cycles - after 2 fix cycles (3 reviews), HALT and escalate ..." with a lowercase "after". A case-sensitive grep for "After 2 fix cycles" finds the other three files (tech-reference :538, readme :464, operational-guide :571) and misses the tdd file. The by-content pin rule (P4:24) lets an executor read it case-insensitively.
4. **Task 5 acceptance line 2 reaches an unlisted line.** `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` must print nothing (P4:89), but the phrase also sits in the FR-8 rule at `src/superclaude/commands/spec-panel.md:332` (and the plugin twin :330), outside the bullets Task 5 lists for editing (lines 259 to 261 and 372, P4:84). The sentence "its `follow-up candidates` list becomes the follow-up ledger" can be read to cover it; the edit list does not name it.
5. **Task 5 parity assertion is under-specified.** "a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`" (P4:90): the plan names three files in the edit sentence and says the source and plugin spec-panel copies "differ today" (P4:84), so whole-file parity is impossible; the assertion can only be that the pointer and ledger sentence match. Task 5's acceptance lines do not run the registry test, so the new assertion is first run in Task 6.
6. **Task 1 leaves a PASS bullet next to the rewritten FAIL bullet.** `agent_template_qa.md:157` ("No CRITICAL or IMPORTANT issues") sits directly above the FAIL bullet at :158 that Task 1 rewrites or keeps; the plan names only :158 (P4:33, P4:40).
7. **Task 4's acceptance line is not pinned by content.** "contain the consumer-line instruction" (P4:73) names no sentence to quote, although the Constraints require pins by content (P4:24); the spec gives the form `feeds item X, reads column Y` (merged-requirements.md:249, :273).
8. **Pinning tests are run in one task only.** `tests/skills/test_review_prompt_overrides.py` pins "no minimum count" and the "Independent stance" sentence in `agent_template_qa.md` and the two MDTM templates and "no minimum count" in `tech-reference/SKILL.md` (test file lines 259 to 283). Only Task 2 runs it (P4:55); Tasks 1, 3, 4 and 6 edit those files and do not.
9. **Gate checks run after the edits.** The two owner-gate checks are the first two acceptance lines of Task 1 (P4:36 to 37), which QA reads after the task has edited five templates. `/sc:implement` has a user-authorized Ruling path (`src/superclaude/skills/sc-implement-protocol/refs/ledger.md:62`), so the halt exists, but the edits are already on disk when it fires.
10. **Spec section 10.5 lists `skills/tech-research/SKILL.md` and `skills/roadmap` cap lines under "Builders and researchers"** (merged-requirements.md:867); no task of this plan touches them. The request keeps cap sentences by content (`source.md:12`), so this may be intended.

## Recommendations

- Task 1: replace acceptance line 2 so it reads the ledger go row (dated after the audit window) and checks only that the stage 3 summary exists and quotes RT1 and RT2; do not require it to state a passed window.
- Tasks 1 and 3: say "remove the file's path from the 'Merge-rule allow-list' section of `refs/scale-map.md`" and name the file.
- Task 3: restate line 3 as "each file still contains its cap sentence (2 fix cycles, 3 reviews, escalate)", quoting the tdd file's own wording.
- Task 5: list `follow-up candidates` at line 332 (and the plugin twin) in the edit scope, define the parity assertion, and run `tests/skills/test_review_severity_registry.py` in its acceptance.
- Tasks 1, 3, 4: add `tests/skills/test_review_prompt_overrides.py` to an acceptance line, or to Task 6's final run.

## Self-reported confidence

0.80 (self-review by the orchestrator, not the plan's author; Markdown claims verified by Grep and Read on 2026-11-16; the stage 1 to 3 packages are plans, not executed work, so file names they create were not checked on disk).
