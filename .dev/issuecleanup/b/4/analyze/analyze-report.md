# /sc:analyze report: src/superclaude/cli/sweep (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T22:16:00Z; degraded: none
Master: f2894fc44. Worktree: /home/coder/workspaces/worktrees/IronClaude/Realign.

## Scope

Six files, 3759 lines: `classify.py` (1009), `probes.py` (1477), `report.py` (695), `commands.py` (288), `models.py` (278), `__init__.py` (12). Chosen as the narrowest path common to #791, #792, #793: it holds the only contract reader (`read_contract`) and the worker-state classification the playbook and the status pass would sit beside.

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | Info | The sweep is read-only and has no code that sends a message or types into a terminal. A check-in sender (C10) would be new code outside this package. | Grep of `src/superclaude/cli` for `terminal send`, `--enter`, `orchestration send`: only `observe/adapter.py:45` lists "send" (not a sender in sweep). |
| A2 | Medium | `return-contract.yaml` has exactly one reader on master: `read_contract` (`probes.py:781`) over `_yaml_top` (`probes.py:722`) and `_contract_from_text` (`probes.py:737`). It requires no field; a contract with no `worker_status` is returned with `worker_status=None`. A C11 validator belongs on this reader, not in a third parser. | `classify.py:810` treats `worker_status is None` as an unknown result; `models.py:118` declares it optional. |
| A3 | Info | `read_contract` has 7 callers, all tests; the production use goes through the probe collector. Blast radius of adding a required-field check: `probes.py` plus `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_classify.py`. | codegraph_callers and codegraph_impact on `read_contract` (8 symbols affected). |
| A4 | Info | The classifier's rules are `blocked_contract`, `orca_exit_proof`, `fenced`, `waiting_signal`, `working`, `finished`, `idle`, `person_active`, `fallback` (`classify.py:345`). They are not the contract's S0-S11 states. A playbook keyed on S0-S11 (C12) therefore has no code counterpart here and must point at `WORKER-CONTRACT.md:117-130`. | `classify.py:211-330`. |
| A5 | Info | `_SETTLED_OUTCOMES = ("succeeded","partial","failed")` (`classify.py:98`) is a third list of outcome words (beside WC-5 and `complete.py:184`). A C11 definition of valid outcome words should reuse one list. | `classify.py:98`; `complete.py:184-185` per round 1. |
| A6 | Info | No hourly, cadence, check-in or `refuse(argv)` code exists anywhere in the package. | Grep of the package for `hourly`, `refuse(`: no match. |

## Recommendations

1. C11 (#792): add the required-field check on `read_contract` and share the outcome-word list; do not add a third parser.
2. C10 (#791): the sender is new code outside `sweep`; the sweep package stays read-only.
3. C12 (#793): a refs file that points at contract rows; no code counterpart in `sweep`.

## Limits

Quick depth. Dynamic behaviour not run. `complete.py` and the contract were read directly, not through this run's target.
