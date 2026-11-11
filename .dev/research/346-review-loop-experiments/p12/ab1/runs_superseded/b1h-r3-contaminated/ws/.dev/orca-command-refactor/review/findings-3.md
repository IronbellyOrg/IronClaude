### B2
### B2 (new in round 3, blocking, origin=changed). The load row forbids the Task that AC-1.2 requires for load
- Origin: changed. The row quotes the changed line spec:112; the conflicting AC-1.2 is unchanged (spec:197). The same two texts are also in the baseline (`spec-v2.md:112` and `spec-v2.md:197`), so this is older than the round-3 edit and was not raised in round 2. Recorded now under the rule to record a severe defect found in re-review even if older.
- Stated texts:
  1. spec:112, load row: "use it as a step inside another worker's brief, not as its own Task".
  2. spec:159 (P1 scope) puts `load` in P1; spec:196 (AC-1.1) and spec:197 (AC-1.2) apply to "each P1 command", and AC-1.2 is "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass".
  3. spec:179-180 (7.2): "For each command under test, the coordinator runs: 1. `ORCA orchestration task-create --spec "<brief per section 2.3>"`, then `worker-start`". Step 3 (spec:182) requires one `worker_done` whose report path is the WC-4 contract path.
  4. spec:167: "A phase passes only when every check in its block and every common check passes."
- Sentence that holds with no further assumption: an implementer who follows the load row never creates a Task for `/sc:load` (spec:112); AC-1.2 requires a 7.2 run on `load`, and 7.2 step 1 (spec:180) creates a Task for each command under test; so AC-1.2 cannot pass for `load` as written, and P1 cannot pass (spec:167).
- Grading: a stated text that an acceptance criterion cannot pass, and two stated texts that contradict each other, are both blocking under `command.md` Review Loop item 2 and the FIRST-REVIEW grading check (prompts file line 33).
