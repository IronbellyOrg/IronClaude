<!-- Provenance: merged from 3 reviewer cards (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus) + invariant probe. Base: Variant 3 (variant-3-original.md). Merge date: 2026-11-13. Plan audited: .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md (cited as plan:<line>). Severities follow the debate Scoring Matrix and Round 2 finals. -->

<!-- Source: Base (original) -->
## Verdict

PASS: no blocking finding.

Rule: only a blocking finding fails the plan audit. Medium and minor findings are reported and do not change the verdict. This merged result has 0 blocking, 3 medium (M1, M2, M3) and 8 minor or non-blocking (M4-M11).

<!-- Source: Base (original); rows M1, M2, M4-M11 merged per Changes #1-#8 -->
## Merged findings

| id | severity | claim | evidence | grounding | source |
|---|---|---|---|---|---|
| M1 | medium | T5.AC2 requires `make verify-sync` to pass but the plan has no `make sync-dev` step; `sync-dev` is needed with or without missing `.claude/` copies, and the one-line step is outside the four-file scope wording. | plan:19, plan:82; Makefile:171-178; .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t5-checks.log:28-35 | [Grounded] | V1 F1, V2 F1, V3 confirm; debate C-001 (unanimous medium) |
| M2 | medium | No task records the "before" pids of the live shims on ports 4013 and 4114 ahead of Task 1; T4.AC4 alone asks for before-and-after, so a plan:20 violation during Tasks 1-3 (Task 1 runs the real ccsession and kills a shim by pid) could not be shown. Not blocking: nothing aims at ports 4013/4114. | plan:70; plan:20; plan:29 | [Grounded] | V1 F2, V3 round 2 (V2 minor); debate C-002 (2 of 3 medium) |
| M3 | medium | Task 3 gives one reason an unconditional `os.setsid()` is harmless (it fails for a group leader); that does not cover a hand-started shim that is not its group's leader (under `uv run` or not first in a pipeline), where `setsid` succeeds and Ctrl-C from that terminal no longer reaches the shim. HEAD later added an `isatty` guard with a comment giving this reason. | plan:52; remediation-source.md:12; src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1012-1019 | [INFERRED] | V3 F1; V1 and V2 agreed in round 2; debate C-008 (unanimous medium) |
| M4 | minor | Off-path review (HC5: PR reviewers and `/sc:reflect --mode post`) is required by the source but is not a plan task; it runs after the plan, the closure verdict is advisory, and the source scope is "exactly these, nothing else". | remediation-source.md:35; remediation-source.md:9; plan:74-82 | [Grounded] | V2 F2 (V2 kept medium; V1 and V3 minor); debate C-006 (2 of 3 minor) |
| M5 | minor | Task 1 asserts the reply "contains `b"message_stop"`" where the source says the reply "ends with `message_stop`"; weaker, but `message_stop` is the last SSE event and the test also checks status 200 and the same pid. | plan:32; remediation-source.md:14 | [Grounded] | V2 F3; debate C-007 (unanimous minor after V2 conceded) |
| M6 | minor | T1.AC3 says no "shim or sleep process" is left, but `pgrep -f <tmp copy path>` cannot match `exec sleep 60`. | plan:29, plan:34 | [Grounded] | V1 F4, V2 F4, V3 reviewer notes; debate C-004 (unanimous minor) |
| M7 | minor | T2.AC2's "assert in the test" that the shim is gone after teardown cannot be written (the fixture teardown runs after the test body), and the `pgrep -f` alternative has no unique pattern because the `shim` fixture runs the shared `SKILL_DIR` script, not a per-test copy. | plan:44; tests/unit/test_ccsession_tiers.py:843-882, 855, 863 | [Grounded] | V3 F2; debate C-009 (single advocate, citation corrected) |
| M8 | minor | Plan wording does not match itself in three places: T2 declares a dependency on Task 1 it does not use while T3's real dependency on Task 1 (T3.AC2) is unstated; Task 1 cleanup says `pkill -f` the copy path while Constraints say exact pid; scope says "exactly the four files" while T4.AC3 and the ./artifacts logs write other outputs. | plan:38, 50, 56; plan:23, 29; plan:19, 69 | [Grounded] | V3 F3, V3 F4, V1 F5; debate U-004, U-005, C-005 |
| M9 | minor | Rollout caveat: following the plan alone does not protect sessions on shims that are already running; they keep the old code, are reported stale and stay exposed until they stop (plan:20 forbids install/update). Non-blocking. | plan:20; src/superclaude/skills/ccsession-tag/ccsession:1011-1013 | [Grounded] | invariant probe INV-001 |
| M10 | minor | A reparented shim goes to the nearest subreaper rather than to init; the hook scripts set a child subreaper, so the shim may stay in a governed tree. Whether ccsession is launched inside a governed Bash call was not confirmed. Non-blocking. | src/superclaude/hooks/scripts/launch-job-identity.sh:310-312, 483-484 | [INFERRED] | invariant probe INV-002 |
| M11 | minor | Session separation (`getsid`/`getpgid`) is asserted only on the direct-start path; the real-launch test checks descendant, 200, `message_stop` and pid, not session or group. A test-coverage gap, not a goal failure (`os.setsid()` lives in the shim and runs on every start). | plan:32; plan:40 | [Grounded] | invariant probe INV-003 |

<!-- Source: Variant 1, merged per Change #6 (stale anchors kept as an informational note only); Variant 3, merged per Change #6 -->
## Informational (not defects)

- Stale line anchors: plan:21, 29, 52, 64 point at line numbers that have drifted against HEAD (for example the `__main__` block is now near proxy:1009-1019). The anchors matched remediation-source.md and the executor's ledger when the plan ran, and the plan also names symbols, so this is HEAD drift and not a plan defect.
- Coverage figure is vacuous: the spec is one line (`source.md` points to remediation-source.md), so the coverage tool parsed it sparse and its number measures the tool, not the plan. Every item in remediation-source.md:9-26 maps to a task or a Constraint.

<!-- Source: Variant 2, merged per Change #3; Variant 3, merged per Change #8 -->
## Rejected or withdrawn

- V2's FAIL verdict and its "Blocking" label on the off-path-review finding: withdrawn by V2 in Round 1 (HC5 closure verdict is advisory at remediation-source.md:35; its own table rated the finding MEDIUM). Kept as minor (M4).
- Temp-HOME gap (V3 F5): withdrawn by V3, because `_real_launch` sets HOME and the plan says to mirror it.
- Stale line anchors as a plan defect (V1 F3 minor): rejected by V2 and V3, conceded by V1; kept only as the informational note above.
