# Analyze report: src/superclaude/cli/issue_pipeline (focus architecture, depth quick)

Run: 2026-11-24, branch ironbelly/Realign (HEAD f2894fc44 ancestor). Items served: #794 (C13), #795 (C14), #797 (C16).
Codegraph: index_state=fresh, checked_at=2026-11-24T22:18:35Z; degraded: none (used only for the readiness check; the evidence below is from Grep and Read at quick depth)

## Layout
`src/superclaude/cli/issue_pipeline/` has 9 modules, 2122 lines: `cli.py` (489, the click group), `complete.py` (431), `approval_record.py` (416), `stage_predicates.py` (301), `reads.py` (182), `plan_hash.py` (90), `brief.py` (80), `release.py` (66), `approval_line.py` (62).

## Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Info | The group is the only coordinator verb home on master. Verbs: plan-hash, check-approval, init, adopt-create, adopt-mark, record-create, record-show, record-mark, release-worker, complete, stage-status. No `gate-*`, `answer-check`, `report-entry` or `merge-gate` verb. | `cli.py:62,77,97,109,118,135,162,180,201,226,409` |
| 2 | Info | `answer-check`, `merge-gate`, `report-entry` exist nowhere in `src/` except one caller: closeout's `settle.sh` calls `superclaude orchestrator report-entry` and falls back to `surface_absent`. | `sc-closeout-protocol/scripts/settle.sh:1037-1042` |
| 3 | Info | The only mention of an Orca decision gate on master is the coordinator wait type `decision_gate`, answered by "goes to the person". Nothing opens a gate. | `WORKER-CONTRACT.md:102,109`; pinned in `tests/skills/test_worker_contract.py:206` |
| 4 | Medium (architecture) | Approval evidence is bound to a plan hash and an issue number (`approval_record.py`, `stage_predicates.py`), not to a question key and head sha. A merge-go check (`answer-check`) is a second approval kind; it needs its own record type, not a reuse of the plan-hash row (R29: a claim-time event must not count as plan approval). | `approval_record.py`, `stage_predicates.py`; R29 in `requirements.md:55` |
| 5 | Medium (architecture) | `superclaude.pr_submit` is a pure core: it must hold no `gh` or `git` word (NFR-6). A `merge-gate` in `issue_pipeline` can import its classifiers (`ci.py`, `reviewers.py`, `merge_guard.py`) but must do its own GitHub reads or call the skill scripts. No production Python caller of that core exists today. | `pr_submit/merge_guard.py:1-18`; `pr_submit/` listing |
| 6 | Low | The new verbs would join a group whose `cli.py` already imports `issue_watch` (cycle, github, runner), so a read-only `merge-gate` sits in the same layer as the watcher reads. Coordinator-only verbs are classified by the launch-level guard by text pattern; each new verb needs its own pattern and test. | `cli.py:16-18`; R34 item 4 |

## Recommendations
1. Put C13 `answer-check`, C16 `merge-gate` and C14 `report-entry` behind one verb group decision (C6 and C1 first); do not add them to `issue_pipeline` ad hoc.
2. Keep `answer-check` a validator of entry, key, head sha and freshness only (D06 item 9).
3. Keep the pr_submit core free of `gh` and `git`.

## Not checked (quick depth)
Runtime behaviour of the verbs; Orca's recording of who resolves a gate (UNVERIFIED).
