# Reflect deviation patterns — issue-331-github-issue-watcher

## reflect-post-20261108T0410Z-issuewatch331 (UC-2, issue #331 issue-watch poller, 2026-11-08)
- Recurring pattern: two design rules can contradict at an extreme (durable record before the spawn, and no launch after the cutoff): the code satisfied each rule at its own check but left a window between them. When a task adds a durable write before an irreversible call, ask for a deadline or kill-switch re-check after the write and a restore path.
- Recurring pattern: an executor adds closed-enum values (reason names, exit codes) as [PROPOSAL] comments and documents them only in the runbook; the design and spec stay at the old table. Check the enum count in code, tests, runbook, design and spec together.
- Recurring pattern: process rules that ban a construct ("no skip") are met by recorded non-root runs while root-guarded skipif sites remain; grep for the construct, do not rely on the run summary.
- Process note: reviewer cards cite wrong line numbers when a context summary intervened (cycle.py:335-337 for 1060-1062); the blind calibrator caught it because it re-read the lines. Keep a spot-check of at least 12 citations in every calibration.
- Process note: the evidence-validator agents return a clean YAML list but one of three sent it by message instead of the final text; recover it from the transcript.
- Process note: Click CLI verbs always DEGRADE in the runtime-surface sweep (decorator, packaging entrypoint and registry all match the oracle), which forces needs_human_decision on every CLI change; the e2e tests are the real evidence.
