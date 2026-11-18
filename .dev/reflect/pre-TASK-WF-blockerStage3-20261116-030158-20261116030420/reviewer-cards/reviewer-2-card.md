---
reviewer: 2
persona: qa
model_class: opus
agent_id: a3e03a12d407466bd
persisted_by: orchestrator (the reflect-reviewer agent has no Write tool; text copied from its final message, indentation of the hand-back frame removed)
---

## Findings

**F1. Blocking: yes. The stage 3 entry check reads a file that cannot contain the shadow-run count it asks for.**
Evidence: plan `:37` "`stage2-summary-for-owner.md` (read by package id) states at least 5 observed shadow runs with zero safety misses". Stage 2 plan `:114` has that file state "the number of shadow runs observed so far (zero is allowed)", and stage 2 writes it at the end of its own package, before any run has happened. `source.md:3` lists "exists and the owner has read it" and "at least 5 shadow runs have been observed" as separate conditions; the plan merged them into one.
Consequence: Task 1 fails every time. If the fix cycle tries to make the check pass, it may edit the other package's summary, which would fake the gate.
Fix: add a first step that runs stage 2's `./artifacts/shadow_summary.py` over the shadow-run folders and writes the output to this package's `./artifacts/`. Check entry conditions before spawning anything, and add the halt clause to `:37` and `:38`.

**F2. Blocking: yes. No rule says how pass or fail is judged, and advisory classes make Task 3's gate halt by construction.**
Evidence: stage 0 plan `:106` "if it cannot, the advisory fallback is the expected outcome". Plan `:62` requires "shows pass on all three requirements". Spec `merged-requirements.md:680` says "with the same reviewers", but plan `:33` only requires fresh spawns.
Consequence: a small planted set compared by exact equality is noise. An advisory class can never show "pass", so the gate on the rule switch measures nothing reliable.
Fix: define the pass rule (point estimate or interval overlap, and with what tolerance) and what an advisory class does at Task 3. Require the same model class and brief in both passes.

**F3. Blocking: yes. Tasks 4 and 5 read the frozen FAIL-trigger inventory from this package, but stage 0 writes it.**
Evidence: plan `:73` and `:85` "`./artifacts/stage0-inventory-freeze.md`". Stage 0 plan `:37` creates it. Plan `:27` says `./artifacts/` means this package.
Consequence: the acceptance line at `:77` has no input file.
Fix: read the file from the stage 0 package by package id.

**F4. Blocking: yes. The new-rule pass also receives the old rule.**
Evidence: `src/superclaude/hooks/hooks.json:173` runs `pragmatic-subagent.js`; `pragmatic-subagent.js:7` reads `~/.claude/output-styles/pragmatic.md` and injects it into every subagent. Stage 0 plan `:76` names this confound for its re-grade; this plan's Task 1 does not.
Consequence: the recall measurement that gates the rule switch is biased.
Fix: state how the injected old rule is handled in the new-rule pass, and require the result file to report the confound.

**F5. Blocking: yes. M12 has no stage 2 baseline, so "flat counts" cannot be judged.**
Evidence: spec `:974` "rf-qa FAIL count per pilot gate | ... flat counts falsify the pilot | stage 2 | down". Stage 2 plan `:110` lists the exit numbers without any rf-qa FAIL count, and a search of the stage 2 plan finds no M12 or baseline. Plan `:161` only "quotes RT1, RT2 and M12 from the spec".
Consequence: the owner has no number to compare against at the stage 4 go. This is the prior review's F8 again, still unresolved.
Fix: Task 11 names the source of the stage 2 rf-qa FAIL baseline (or measures it from the stage 2 run folders) and states the count method. Also list M10b, whose baseline is stage 3 (spec `:972`).

**F6. Blocking: yes. The spec's drift test for v2 rows never runs in the stage that creates the first v2 rows.**
Evidence: stage 1 plan `:209` (T1: "every row of kind `digest` holds ... exactly one digest whose flattened body equals the digest section"). Plan `:125` lists seven test files without `test_review_severity_registry.py`. Plan `:78` and `:90` check only "exactly one digest", not that it equals `refs/rule.md`.
Consequence: a mistyped digest in `rf-qa.md` or `rf-qa-qualitative.md` would ship in the live pilot.
Fix: add `uv run pytest tests/skills/test_review_severity_registry.py -v` to the acceptance lines of Task 8, or of Tasks 4 and 5.

**F7. Blocking: no. The ban on stage 4 edits is missing.**
Evidence: `source.md:20` "No template, rule-prompt, builder, researcher or spec-panel edit (stage 4)". Plan `:22` "Not built here" leaves it out.
Consequence: QA has no rule to flag edits to those files.
Fix: add the ban to the Constraints.

**F8. Blocking: no. Task 8 does not say what the 8 legacy rows stay pinned to.**
Evidence: `tests/skills/test_review_severity_rule.py:181-192` lists 8 stage 4 files that are checked against pragmatic's bullets. Plan `:122` makes `canonical_rule_bullets()` read the v2 digest instead.
Consequence: either the test fails on the legacy files or their pin is dropped, which goes against `:127`.
Fix: compare legacy rows against a frozen copy of the legacy text until stage 4.

**F9. Blocking: no. Task 3 runs tests that are expected to fail until Tasks 8 and 9, without saying so.**
Evidence: plan `:59` "Run `make sync-dev` and then the existing tests that Task 8 re-pins."
Consequence: the per-task check can flag Tasks 3 and 4 as failed.
Fix: state the expected failures, with "until Task 8" and "until Task 9".

**F10. Blocking: no. Task numbers left over from the base plan.**
Evidence: `:147` "after Tasks 34 to 37"; `:126` `t38-fixture-diff.md`.
Fix: change to "Tasks 4 to 7" and rename the artifact.

**F11. Blocking: no. The registry check cannot find the row it names.**
Evidence: `:116` runs `grep -n "sc-review-severity" .../registry.yaml`, which matches the skill folder name, so it cannot show or exclude a `skills/task/SKILL.md` row.
Fix: grep for `skills/task/SKILL.md`.

## Checked and sound

- R-002 is done: the gate is an acceptance line on Task 3 (`:62`), and Task 1 requires fresh spawns with alternated order (`:33`).
- R-003 is done for stage 3: the allow-list in `:144` names only files that exist now and leaves out the plugin mirror. Searching `src/superclaude` Markdown for the three phrases finds exactly 11 files: the 6 stage 4 files, the auggie file, and the 4 files Tasks 4 to 7 edit. `task/SKILL.md` hits only at lines 252 and 361.
- R-005 is not violated: no acceptance line in this package is made false by a later task.
- The cited text is where the plan says it is: `rf-qa.md:83`, `:402`, `:549`; `rf-qa-qualitative.md:84`, the eight FAIL lines, and Rule 6 at `:990`; `rf-analyst.md:75`; `pragmatic.md` lines 225 to 229. The precedence sentence (REQ-03, spec `:205`) is inside the digest, so the digest-equality line in Task 3 covers it.
- I disagree with part of T1 card's O5: the stage 0 package id is recorded in the stage ledger (`README.md:17`), and the Constraints (`:19`) say ids are read from that ledger. The blank rows for stages 1 to 3 are filled when the owner gives the go (`README.md:11`).
- I read every file I cited; none was unreadable.

## Self-reported confidence

0.80

## Blind calibration (attached by the orchestrator)

Calibrated C 0.79 (self-reported 0.80). Per-finding confidence F1 0.85, F2 0.70, F3 0.80, F4 0.90, F5 0.85, F6 0.65, F7 0.90, F8 0.75, F9 0.80, F10 0.95, F11 0.85. Calibrator: F2 and F3 graded a bit generously. Calibrator class sonnet, disjoint from reviewer classes. Full record: artifacts/reviewer-calibration.yaml.
