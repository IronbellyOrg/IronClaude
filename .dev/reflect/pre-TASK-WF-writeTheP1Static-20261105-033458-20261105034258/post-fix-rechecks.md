# Post-reflect fix cycles and rechecks

REPORT.md and return-contract.yaml in this folder describe the plan as it was when reflect ran (plan sha256 55ca3d35...). The plan was edited afterwards under the brief's rule (fix every blocking finding, at most 2 fix cycles). Reflect itself was not re-run; each cycle was followed by one fresh read-only reviewer (single agent, opus, adversarial). These rechecks are not a Tier 2 reflect and have no calibration or evidence-validator pass.

## Fix cycle 1 (after reflect, review 1 = reflect)

Applied to the plan: MF-01 to MF-08 (blocking) and MF-10 to MF-19 (minor); MF-09 (brainstorm step 7, handoff ref, `-i`) was applied with MF-06. MF-20 is a note and went into the Task 15 spec observations. New decisions D-P1-11 and D-P1-12. Plan gate checks re-run: pass.

## Review 2 (fresh reviewer): FAIL, 4 new blocking defects

- B-1: the `-i` and `-o` flag checks matched by substring and could never fail.
- B-2: `/sc:index` kept a consent line (`src/superclaude/commands/index.md:96`) while the plan called it no-gate.
- B-3: brainstorm refused a directory that already holds a contract but also wrote a contract there.
- B-4: a Task 2 grep expected `adversarial/return-contract.yaml` inside a file tree that lists bare names.
- MF-01 to MF-05, MF-07, MF-08 RESOLVED; MF-06 PARTLY (became B-3). Minor notes: `<name>` wording in Task 10, `nested` key optional vs required wording, Arguments vs Options table name, `Write` test satisfied by `TodoWrite`.

## Fix cycle 2

Applied: whole-token flag matching in Task 1 (and `-o` for brainstorm); D-P1-12 extended to `/sc:index` with a Task 12 statement; brainstorm directory refusal made chat-only; Task 2 grep reworded; the four minor notes. Plan gate checks re-run: pass (15 tasks, 15 acceptance sections, no numbered or checkbox lines, no absolute paths, no `.dev/tasks/to-do/` prefix).

## Review 3 (fresh reviewer): PASS

B-1 to B-4 RESOLVED; no new blocking defect. Minor notes left as notes (not applied):
- Task 1 quotes `UNATTENDED_COMMANDS = frozenset()` but the file has `UNATTENDED_COMMANDS: frozenset = frozenset()` (`tests/skills/test_worker_contract.py:255`).
- Task 3's new test asserts Wave 2A names `skipped`, which already holds today (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:194`), so that part proves nothing.
- Task 13's `grep -n '\-\-checkpoint <name>'` warns about a stray backslash on newer GNU grep; `grep -n -e '--checkpoint <name>'` avoids it.
- `src/superclaude/commands/business-panel.md:116` ("Execute decisions without user approval") is covered only by D-P1-12's general sentence, not by its command list.

Final state: reflect verdict PARTIAL on the original plan (8 blocking, all fixed); two follow-up reviews, last one PASS. Plan sha256 after the cycles is recorded by the worker report.
