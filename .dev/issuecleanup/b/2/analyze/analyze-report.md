# /sc:analyze report: src/superclaude/cli/sweep (focus architecture, depth quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T22:15:07Z; degraded: none (status only; reads below are Read/Grep, confirmed on disk)

Why this path: it is the only existing Python package that calls Orca `orchestration` verbs through a closed allowlist, so it is the nearest code to issues 785 (load Orca's guide), 786 (Run lifecycle) and 787 (verb list per step).

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Info | The sweep keeps a closed allowlist of 10 read-only call templates (7 verbs). `orchestration run-current` is the only Run verb in it; `run-use` and `run-create` are absent. A coordinator `run-use` step (issue 786) must not be added here. | src/superclaude/cli/sweep/probes.py:45-58 |
| 2 | Info | The observer forbids `run-use`, `run-create`, `send`, `ask`, `check`, `dispatch` by prefix. Any new Run-binding code must live outside `cli/observe` and `cli/sweep`. | src/superclaude/cli/observe/adapter.py:34-50 (run-use line 43, run-create line 44) |
| 3 | Medium | Two separate verb lists already exist (sweep allowlist, observer forbidden list) plus a third in the launch-level guard; issue 787 would add a fourth (per-step lists) and FR-26 a fifth (`refuse(argv)`, not built). Risk of drift between lists. | probes.py:49-58; adapter.py:34-50; src/superclaude/hooks/scripts/launch-level-guard.sh:495-506 |
| 4 | Low | The sweep calls the binary `orca-ide` (never bare `orca`), while coordinator text and the launch guard use `orca`. A per-step verb check (issue 787) must say which binary name it matches. | probes.py:43 (ORCA_BINARY_DEFAULT) |
| 5 | Info | No module under `src/superclaude/skills` or `src/superclaude/cli` loads `orca skills get`; the only mention is documentation (docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:645). | grep over src and docs |
| 6 | Info | The package imports only stdlib, click and yaml; it has no import from observe, issue_pipeline or issue_watch (layering is clean). | grep of `^import|^from` in cli/sweep/*.py |

## Recommendations

1. Keep Run-binding code out of `cli/sweep` and `cli/observe` (finding 1, 2).
2. When issue 787 is built, derive its allowed-verb table from one source and have the sweep, guard and per-step test read or mirror it (finding 3).
3. State the Orca binary name the per-step check matches (finding 4).
