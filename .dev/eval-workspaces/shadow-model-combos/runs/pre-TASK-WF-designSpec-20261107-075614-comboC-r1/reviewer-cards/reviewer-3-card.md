persona: refactorer
model_class: opus
model: claude-opus-5-5

# Reviewer 3 card

I used the refactorer lens. I read the whole plan (13 tasks) and the whole spec. I checked task order, the `Depends on:` lines, tasks that edit the same file, edit order against test pins and the stale-entry rule, and scope against spec sections 4.5, 6 and 10.

What held:
- **Order of edits to shared files.** The tasks that edit the same file run in a safe order:
  - `run_log.py` and `test_run_log.py`: Task 2, then Task 5 (through Tasks 3 and 4).
  - `SKILL.md`: Task 9, then Task 10.
  - `test_static_grep.py`: Task 5 edits `CORE_PURE_FILES` and Task 7 edits `_RESOLUTION_SCRIPTS`. These are separate lists.
- **Stale classification entries.** Task 7 writes the script and Task 8 writes the ref. No later task edits either file, so no `WRITE_VERB_CLASSIFICATION` entry can go stale.
- **Pinned sentences.** Task 10 keeps the S5a sentence and the Wave 6 pre-push sentence unchanged. It checks them against string constants recorded by Task 1, not against `git show HEAD:`.
- **Dependency lines.** Task 5 depends on Tasks 3 and 4, and Task 11 depends on Tasks 3, 4, 5 and 7, which meets the spec section 10 dependency note.
- **Import cycle.** Task 5 has a fresh-interpreter import check that would catch an import cycle.
- **Scope.** The two extra test files, `test_merge_guard_protocol.py` and `test_merge_guard_scenarios.py`, are not drift. Spec section 7 asks for those protocol and scenario assertions.

On the T1 excerpt:
- I confirm T1 F2. Task 9 forbids an "L3 or `draft` condition" in the Wave 0 bullet (plan:137) and its test fails on one (plan:140), yet the bullet must carry the "at L3 with `--merge-guard off`" line.
- I confirm T1 F4. Task 1's criteria (plan:36-38) do not check the instruction that the PR-opening run passes `--merge-guard off`. I do not repeat either finding below.

My four findings are all MINOR and non-blocking:
- Tasks 9, 10, 12 and 13 use Task 1's record but have no direct `Depends on: Task 1` line; they reach it only through other tasks.
- Task 12 shares two test files with Tasks 9 and 10 but does not depend on them.
- Task 9's last criterion conflicts with its own permission to add a classification entry.
- Task 7's step for `_RESOLUTION_SCRIPTS` depends on what Task 1 finds, but its criterion does not.

## Findings block
```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Tasks 9, 10, 12 and 13 use ./artifacts/pre-build-gate.md (pins, literal start text, base-commit record) but none declares Depends on: Task 1; Task 13 lists Task 2 yet omits Task 1. Spec section 10 asks for one Depends on line per consumed output. Covered only transitively.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":132,"line_end":137,"quote":"Depends on: Task 6\nDepends on: Task 8"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":146,"line_end":154,"quote":"the literal start text recorded in `./artifacts/pre-build-gate.md`"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":177,"line_end":182,"quote":"using the pins recorded in `./artifacts/pre-build-gate.md`"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":188,"line_end":195,"quote":"compared with the base-commit record of Task 1"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":363,"line_end":363,"quote":"Declare dependencies completely, one `Depends on:` line per dependency"}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Task 12 extends test_merge_guard_protocol.py and the WRITE_VERB_CLASSIFICATION table, which Tasks 9 and 10 also edit, but depends only on Tasks 6 and 8. Only task numbering orders these edits; a scheduler that follows Depends on lines could run 12 alongside 9 or 10 on the same files.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":177,"line_end":182,"quote":"Depends on: Task 6\nDepends on: Task 8"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":137,"line_end":137,"quote":"Extend `tests/pr_submit/test_merge_guard_protocol.py` with a test for the Wave 0 bullet"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":150,"line_end":150,"quote":"Extend `tests/pr_submit/test_merge_guard_protocol.py` with one test per bullet"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 9 allows a WRITE_VERB_CLASSIFICATION entry when a gh pr line is unavoidable, but its criterion requires no edit to any existing test expectation except those of Tasks 2, 5, 7 and 8. Adding that entry would break Task 9's own criterion.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":137,"line_end":137,"quote":"if one is unavoidable, add its `WRITE_VERB_CLASSIFICATION` entry as the last step"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":142,"line_end":142,"quote":"passes with no edit to any existing test expectation other than those listed in Tasks 2, 5, 7 and 8"}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 7 adds the script to _RESOLUTION_SCRIPTS only if Task 1 O2 shows the list fits, yet its criterion requires the script to pass the _RESOLUTION_SCRIPTS origin-URL tests regardless. If O2 rules the list out, that criterion has nothing to test.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":108,"line_end":108,"quote":"Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py` only after reading the purpose of that list (Task 1 O2)"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":113,"line_end":113,"quote":"the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":299,"line_end":299,"quote":"script lists only after checking each list's purpose"}]}
```
reviewer_model_self_report: claude-gw-tier1a (Claude, Anthropic)
