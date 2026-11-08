| Status | Result |
|---|---|
| DONE | Re-read the disputed implementation and requirements; revised classifications and confidence below. |
| NEXT | Retain the acceptance failures; correct the late-launch path with restoration and a slow-save test. |

## Rebuttal

**Variant 2’s acceptance-based argument survives, but its confidence was overstated.** My Round-1 values of 94-99% conflated confidence in a source observation with confidence in a contested classification. Every updated value below is at most 90%.

**Late launch remains a Regression, MEDIUM and blocking.** Acceptance criterion 19 says: “A sleeping stub ends with `gh_timeout`; **no launch starts after 120 s**” ([design:892][acceptance]). The source checks the cutoff, changes the document, persists it, then invokes the launcher without another check ([cycle.py:1048-1062][launch-path]). Persistence crossing the cutoff supplies a direct counterexample. The cadence margin and preserved at-most-once protection reduce impact; neither exempts the acceptance criterion. “Blocking” follows the unmet requirement, not a demonstrated HIGH operational risk.

**Restoration is compatible with the design, with a failure qualification.** Design 647 requires “no entry” when the deadline prevents launch ([design:638-649][deadline]). Snapshot the pre-pending document, keep durable-before-spawn ordering, and restore that document durably if persistence crosses the cutoff. For a previously failed entry, restoration means returning to that prior state, not deleting it; the design expressly recognizes “no entry (or `failed`)” ([design:527-533][crash]). A bare post-save skip is wrong. If restoration fails or the process crashes, do not claim successful restoration: leave the conservative pending state and report failure. That exceptional state is already documented at crash point C3.

**The strict taxonomy preserves several disputed Regression labels.** Regression does not require previously working behavior to break when an acceptance criterion or documented invariant is contradicted.

- **Crash exit, completion reason, and reason count:** acceptance criterion 17 requires each verb’s exits to match section 4; the task also mandates exactly 57 reasons ([design:890][acceptance], [task:199][task-tests]). A required crash fallback does not itself authorize exit 1 or amend the closed table. The register explicitly calls these executor decisions without authorizing research rows ([register:43-47][register]). These remain LOW contract regressions, not three independent defects.
- **Prohibited skips:** the unconditional construction rule is violated by `skipif`; zero skips during recorded runs does not satisfy “No test may use” it ([task:188][task-tests], [test_cli.py:1070][skip]). This remains a verification Regression.
- **Kill-switch status:** I withdraw Regression for this point. The task explicitly prescribes `os.stat`; its interaction with dangling symlinks exposes an advisory contract gap, rather than an unambiguous implementation departure ([task:335][task-record], [record.py:421-431][disabled]).
- **Truncated stderr:** retain Regression, reduced to LOW. The counterexample requires exit 0, a valid id, and the unknown-outcome marker beyond byte 500. The design’s “anywhere” rule is explicit; limiting retained stderr does not exempt classification ([design:634][deadline], [runner.py:126][runner], [launch.py:322-334][outcome]).
- **Missing retry directory:** retain Regression LOW against acceptance criterion 9 and the unqualified retry-list source rule. Normal creation supplies the directory, but validation accepts null and status silently drops that schema-valid entry ([record.py:183-184][validation], [design:739][retry-contract], [cycle.py:1271-1280][status]).

**Updated view of the alternatives:** Variant 1 contributes the strongest breadth of behavioral investigation and correctly challenges severity inflation. Variant 3 contributes the strongest module-boundary explanation and operator-facing checks. Their advisory cautions improve Variant 2, but neither makes explicit requirement contradictions disappear. Conversely, my original blanket authorization of imports and Regression label for kill-switch status were too broad.

## UPDATED POINT TABLE

“Changed” marks a substantive classification or severity change since my Round 1. Confidence is recalibrated throughout. “Backs” identifies the closest substantive account, not endorsement of its original label.

| Point | Final classification | Backs | Confidence | Evidence file:line | Changed |
|---|---|---|---:|---|---|
| X-001 | Regression LOW: crash exit violates exit-set contract | V3 | 80% | [design:114][verbs], [design:890][acceptance], [cli.py:123-129][crash-cli] | Yes |
| X-002 | Regression LOW: added name violates closed-table contract | none | 78% | [task:199][task-tests], [audit.py:62-64][reasons] | No |
| X-003 | Authorized for three helpers and permitted type; Regression LOW for fourth helper | none | 82% | [task:332][task-record], [record.py:23-29][imports], [design:231-239][boundaries] | No |
| X-004 | Necessary LOW: isolated-module duplication; parity checking advisory | V3 | 83% | [design:237-240][boundaries], [launch.py:30][constants] | Yes |
| X-005 | Authorized LOW: runner timing expressly instructed | none | 90% | [task:193][task-tests] | No |
| X-006 | Regression MEDIUM, blocking: prohibited test constructs | V2 | 87% | [task:188][task-tests], [test_cli.py:1070][skip] | No |
| X-007 | Regression MEDIUM, blocking: deadline acceptance failure | V2 | 88% | [design:892][acceptance], [cycle.py:1048-1062][launch-path] | No |
| X-008 | Advisory LOW: option parsing unverified, not shell injection | V3 | 82% | [launch.py:36][constants], [launch.py:127-132][retry] | No |
| X-009 | Alleged single check disproved; residual window advisory | V3 | 88% | [cycle.py:693][commit], [cycle.py:1033][launch-path] | No |
| X-010 | Regression LOW: same unamended count contract as X-002 | none | 80% | [task:199][task-tests], [register:43-47][register] | No |
| C-014 | Regression MEDIUM, blocking; restore prior document before skipping | V2 | 88% | [cycle.py:1060-1062][launch-path], [design:647][deadline] | No |
| C-013 | Regression MEDIUM, blocking: same as X-006 | V2 | 87% | [task:188][task-tests], [test_cli.py:1070][skip] | No |
| C-016 | Advisory design gap: prescribed rolling window | V1 | 86% | [record.py:689-703][day-cap], [task:338][task-record] | No |
| C-017 | Advisory LOW: prescribed timestamp lookup conflicts with presence semantics | V1/V3 | 80% | [task:335][task-record], [record.py:421-431][disabled] | **Yes** |
| C-018 | Advisory recovery gap: ordinary exceptions bypass final commit | V1 | 82% | [cycle.py:685-690][commit], [design:529-530][crash] | No |
| C-019 | Advisory external-process risk, UNVERIFIED | V1 | 65% | [runner.py:91-101][runner] | No |
| C-024 | Advisory integration uncertainty; error-id semantics UNVERIFIED | none | 77% | [launch.py:39-45][constants], [launch.py:326-334][outcome] | No |
| C-026 | Regression LOW: narrow violation of “anywhere” classification | V1 | 79% | [runner.py:126][runner], [launch.py:322-334][outcome], [design:634][deadline] | **Yes** |
| C-036 | Regression LOW: schema-valid input omitted from required retry list | V3 | 79% | [record.py:183-184][validation], [cycle.py:1271-1280][status], [design:739][retry-contract] | No |
| C-037 | Advisory contract inconsistency, not demonstrated exit-pair requirement | V3 | 78% | [audit.py:393-402][fallback], [task:501][task-cli] | No |
| C-034 | Drift LOW: documentation omissions; command exits authorized | V3 | 83% | [task:498-501][task-cli], [setup:432][runbook] | No |
| C-022 | Advisory specification gap: historical ties expressly prescribed | V1 | 86% | [predicates.py:199-209][ties], [task:196][task-tests] | No |

**Recommended action:** correct the late-launch acceptance failure first, preserving durable-before-spawn ordering and testing successful restoration plus restoration failure.

Not checked: runtime reproduction, live Orca behavior, or production frequency. No files changed and no tests ran.

[acceptance]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:878
[deadline]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:625
[verbs]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:114
[boundaries]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:229
[crash]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:523
[retry-contract]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:739
[task-tests]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:188
[task-record]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332
[task-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:498
[register]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/deviation-register.md:43
[launch-path]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1007
[commit]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:685
[status]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1271
[disabled]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:421
[validation]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:183
[imports]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:23
[day-cap]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:689
[runner]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/runner.py:57
[outcome]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:311
[constants]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:30
[retry]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:119
[reasons]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:55
[fallback]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:381
[crash-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cli.py:123
[skip]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cli.py:1070
[ties]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/predicates.py:199
[runbook]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher-setup.md:432
