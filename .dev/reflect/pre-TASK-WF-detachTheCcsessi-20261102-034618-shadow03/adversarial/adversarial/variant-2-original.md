# Reviewer 2 card (persona: qa, model_class: haiku, model: claude-haiku-5-5, pinned alias claude-gw-tier2[1m])

reviewer_model_self_report: claude-gw-tier1b[1m]   (MISMATCH: pin is claude-gw-tier2[1m] / haiku class)

## What I checked

- Spec body source.md:1: single sentence; all four code targets and issue #341 trace to Tasks 3-5 and Constraints; nothing outside the matrix.
- Remediation required changes 1-4 -> Tasks 4, 3, 1+2, 5; Task 1 text carries every 3a detail (start_new_session, fake claude, per-test copy, ps walk, pause-stream 4, SIGTERM/SIGKILL, 200+message_stop, same-pid health, cleanup).
- AC1-AC6 -> T1/T2 before-logs, T5 test list, T4 live check (after.txt path and -I flag match), T5 lint/verify-sync, Constraints:20, Constraints:21.
- Meetability: after Task 3 alone directly_started_shim passes (Popen child is not group leader); outlives still fails (matches T3 AC); T4 -k expression satisfiable.
- HEAD cross-check: proxy setsid at :1017, ccsession start at :1037, pgrep at :932; t5-checks.log 457 passed / lint clean / sync clean after improvised sync-dev.

## Findings block

```findings-v2
F1:
  severity: minor
  blocking: false
  claim: The remediation source's Pipeline Hardening requirements (HC1 real-ccsession replay, HC5 off-path review) appear in neither the coverage matrix nor the advisory map, and the tasklist has no HC5 step or acceptance criterion.
  evidence:
    - role: spec
      ref: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:35
      quote: "HC5: off-path review required (PR reviewers and /sc:reflect --mode post)."
    - role: plan
      ref: .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:80-82
      quote: "`make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log."
F2:
  severity: minor
  blocking: false
  claim: T5 requires `make verify-sync` to pass but the plan has no `make sync-dev` step, so the criterion fails in a fresh worktree as written.
  evidence:
    - role: plan
      ref: .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:82
      quote: "`make lint` and `make verify-sync` pass"
    - role: spec
      ref: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:24
      quote: "AC4: `make lint` and `make verify-sync` pass."
F3:
  severity: minor
  blocking: false
  claim: T5 narrows the remediation AC2 test-discovery grep and drops the `SKILL_DIR / "ccsession"` alternative without saying so.
  evidence:
    - role: plan
      ref: .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:82
      quote: "grep -rlE \"local-gateway-alias-proxy|ccsession-tag\" tests/"
    - role: spec
      ref: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:22
      quote: "grep -rln \"local-gateway-alias-proxy\\|ccsession-tag/ccsession\\|SKILL_DIR / \\\"ccsession\\\"\" tests/"
F4:
  severity: minor
  blocking: false
  claim: The plan's line anchors (tests, ccsession, proxy __main__) no longer match HEAD; symbol names remain usable.
  evidence:
    - role: plan
      ref: .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:29
      quote: "`StandInGateway` (line 488), `_free_port` (568)"
    - role: spec
      ref: .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:31
      quote: "tests/unit/test_ccsession_tiers.py:488-614 (StandInGateway"
```

Related note: AC6 "ccsession never stops a running shim" has only a Constraints line + the busy_shim test in T4; acceptable.
