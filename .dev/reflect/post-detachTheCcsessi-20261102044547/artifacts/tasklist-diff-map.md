# UC-2 tasklist-vs-diff map (Wave 1B)

Diff: `git diff HEAD` (4 tracked files, 6 hunks, +168/-4). Untracked package/report artifacts are evidence, not audited hunks.

| Hunk (new side) | Task | AC | Classification candidate | Evidence |
|---|---|---|---|---|
| CHANGELOG.md:7-12 | T5 | T5.AC1 | mapped; heading suffix and the "shim already running keeps the old behaviour" sentence are additions | CHANGELOG.md:7, CHANGELOG.md:9, CHANGELOG.md:11 |
| ccsession:801-809 | T4 | T4.AC1, T4.AC2 | mapped, as specified | ccsession:804-809 |
| local-gateway-alias-proxy.py:859-867 | T3 | T3.AC1, T3.AC2 | mapped; adds an `if not sys.stderr.isatty():` guard the task text does not name (inline rationale at :861-862) | local-gateway-alias-proxy.py:863 |
| test_ccsession_tiers.py:16 | T1 | T1.AC1 | mapped (`import signal` used by the sweep) | test_ccsession_tiers.py:16 |
| test_ccsession_tiers.py:1423-1551 | T1 | T1.AC1-T1.AC3 | mapped; adds an `os.getsid` assertion the task AC does not list (inline comment at :1538) | test_ccsession_tiers.py:1536, 1538, 1541, 1543 |
| test_ccsession_tiers.py:1554-1563 | T2 | T2.AC1, T2.AC2 | mapped | test_ccsession_tiers.py:1562-1563 |

- Unmapped hunks: 0 of 6 → S_dev_density = 0.00.
- tasklist_completion_pct: 1.0 (5 of 5 tasks `complete verdict=compliant` in progress.md; FINAL pass at the archive gate).
- S_scope = 4 files; S_domains = 3 (code: Python + bash; tests; docs).

## Step 1B.3 cross-task interaction scan (5 tasks ≥ 3)

- /sc:impact (diff mode): no changed symbol derived (all 4 files unmapped: bash, CHANGELOG and tests not indexed; the proxy hunk is module-level) → artifacts/impact/return-contract.yaml, status partial, no `graph:*` token.
- Symbol overlap by Read: T3's `setsid` block is exercised by T2's test (fixture stderr is a file, test_ccsession_tiers.py:598, so the not-a-tty branch runs) and by T1's `os.getsid` assertion (test_ccsession_tiers.py:1538); T4's subshell is exercised by T1's descendant assertion (:1536).
- Citation check: every pair is linked through the tasklist's `Depends on:` chain (T2→T1, T3→T2, T4→T3, T5→T4) and T3's AC explicitly expects T1's test to fail until T4. No uncited interaction → interaction_effects_findings: 0.

## Step 5.6 / 5.6a reachability

- 5.6 contracted-sink gate: no requirement carries a `durable_sink:` / `@sink` annotation → reachability_skip_reason: no-side-effect-requirements.
- 5.6a required capability ("a shim keeps serving when its launching terminal closes", source.md / plan Goal): invoked at the launcher (ccsession:804-809); the result is consumed (listener wait ccsession:811-818, settings/code health match ccsession:821-829); callee is the real server loop, not a sentinel. Reachable; no Regression.
