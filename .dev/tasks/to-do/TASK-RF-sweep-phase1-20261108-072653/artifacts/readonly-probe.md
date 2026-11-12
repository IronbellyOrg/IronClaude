---
needs_human_decision: false
status: CAPTURED
---

# Step 1.0a read-only Orca capture (item 7.16)

Captured 2026-11-11 against the Run named by the owner in `phase-outputs/plans/OQ-8-run-id-decision.md` (item 7.15): `run_a4723d345399`. Binary: `orca-ide` (`/home/coder/.local/bin/orca-ide`; `ORCA_CLI_COMMAND` unset). Every command below ran in its own Bash call with a tool timeout of 30000 ms, wrapped in an inner `timeout 8`. Only the eight allowlisted templates, file reads, and the step (6) `echo` and `ls -la` were issued; none of the forbidden commands was issued. The capture created no Run, Task or Dispatch. Scratch copies of each command's output were written under `/tmp/probe-7-16/` (outside this task package) while the file was built; they are not part of the deliverable. One Orca read went beyond the item's list of allowed uses: see Deviation D1 in the last section.

Handling of large output: stdout under about 8 KB is shown in full in the section. Larger stdout is summarised in the section (shape, fields, counts, sha256 of the raw bytes) and, where it holds no other session's message text, the raw bytes are stored under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/` (named in the section). The outputs of `worktree ps --json` and `worktree list --json` are not stored raw, because `worktree ps --json` carries other sessions' prompts and assistant messages; their sections hold the shape, counts, hashes and one redacted entry. This is a deliberate reading of "stdout" in the item's Action (the first sentence of the task: paths, session ids and user names may be shown, not other sessions' message text).

## 0. Step 1: the id-learning read (extra read made only to learn the Dispatch ids)

This is the Action step (1) read: `worker-list` run once to learn the Dispatch ids before the before/after reads. It is also the first of the two `worker-list` reads; capture item 3 uses both.

Command: `orca-ide orchestration worker-list --run run_a4723d345399 --json`

Exit code: 0. Stderr: empty. Stdout: 13779 bytes, sha256 `9f72ceb93665d30ecdef6da141b4b1b84ebdc03afe1bb34ae1b9d05bee817a1d`; raw bytes stored at `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/s1.json`.

Learned from it (5 workers, 5 distinct Dispatch ids, all with `dispatchStatus: completed`, `workerState: succeeded`, `terminalState: released`):

| Dispatch id | Task id | Terminal handle |
|---|---|---|
| ctx_6a0e3e3baaee | task_d7ba23de62d2 | term_12f4e391-99b0-4528-a6dc-483bd7c20dcf |
| ctx_9a3728b21883 | task_e90102f005e0 | term_1212fabf-cde3-4350-a807-5d0aac19a520 |
| ctx_4e3237d227c3 | task_38990284224c | term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e |
| ctx_7c86fffa9716 | task_a6a2a3f9e170 | term_c2f40c56-7f46-4ba2-8f9f-4127b229d352 |
| ctx_dad78c5c1332 | task_381ac7af9ed1 | term_88360819-3622-4c35-821d-e06faf346ab4 |

Envelope: `{"counts": {"released": 5}, "page": {"limit": 100, "total": 5, "hasMore": false, "nextCursor": null}, "scope": {"run": "run_a4723d345399", "source": "flag"}}`, `_meta.runtimeId` `a7ee70a1-2e8b-4476-a228-51e9c7019b3f`.

Full stdout:

~~~
{
  "id": "e1936e60-f234-47e8-8d11-cdfae1d7f85f",
  "ok": true,
  "result": {
    "workers": [
      {
        "dispatchId": "ctx_6a0e3e3baaee",
        "taskId": "task_d7ba23de62d2",
        "runId": "run_a4723d345399",
        "workerState": "succeeded",
        "dispatchStatus": "completed",
        "agentTerminalHandle": "term_12f4e391-99b0-4528-a6dc-483bd7c20dcf",
        "terminalState": "released",
        "resource": {
          "id": "wtr_e76d1735d8a2",
          "ownershipState": "released",
          "releaseState": "released",
          "retainedReason": null,
          "terminalHandle": "term_12f4e391-99b0-4528-a6dc-483bd7c20dcf",
          "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
          "endpointId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
          "endpointIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@98e8ea49:e3c1e8c5-d25e-482c-a447-ca5053e2edd3",
          "originDispatchId": "ctx_6a0e3e3baaee",
          "ownerDispatchId": "ctx_6a0e3e3baaee",
          "releaseRequestedAt": "2026-11-11 19:51:11",
          "releaseCompletedAt": "2026-11-11 19:51:13",
          "releaseError": null,
          "recoveryAttemptCount": 0,
          "lastRecoveryAt": null,
          "archive": {
            "source": "transcript",
            "status": "captured"
          }
        },
        "projection": {
          "id": "ctx_6a0e3e3baaee",
          "dispatchId": "ctx_6a0e3e3baaee",
          "taskId": "task_d7ba23de62d2",
          "runId": "run_a4723d345399",
          "role": "worker",
          "parent": null,
          "provider": null,
          "host": {
            "kind": "local",
            "id": "local"
          },
          "workspace": {
            "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
            "kind": "folder_or_worktree"
          },
          "stage": {
            "worker": "succeeded",
            "dispatch": "completed",
            "detail": "settled",
            "activity": "unknown"
          },
          "outcome": "succeeded",
          "liveness": {
            "verdict": "exited",
            "source": "resource_release"
          },
          "evidence": {
            "durable": true,
            "liveStatus": "unavailable",
            "lastObservedAt": null
          },
          "resource": {
            "state": "released"
          },
          "nextAction": {
            "kind": "none",
            "argv": []
          },
          "attention": {
            "categories": [
              "root_completion"
            ],
            "requiresAction": false
          }
        }
      },
      {
        "dispatchId": "ctx_9a3728b21883",
        "taskId": "task_e90102f005e0",
        "runId": "run_a4723d345399",
        "workerState": "succeeded",
        "dispatchStatus": "completed",
        "agentTerminalHandle": "term_1212fabf-cde3-4350-a807-5d0aac19a520",
        "terminalState": "released",
        "resource": {
          "id": "wtr_b565ff1e9a33",
          "ownershipState": "released",
          "releaseState": "released",
          "retainedReason": null,
          "terminalHandle": "term_1212fabf-cde3-4350-a807-5d0aac19a520",
          "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
          "endpointId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
          "endpointIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@846850e6:37868cf7-bb20-4ead-9528-d2331eeba154",
          "originDispatchId": "ctx_9a3728b21883",
          "ownerDispatchId": "ctx_9a3728b21883",
          "releaseRequestedAt": "2026-11-11 19:52:50",
          "releaseCompletedAt": "2026-11-11 19:52:52",
          "releaseError": null,
          "recoveryAttemptCount": 0,
          "lastRecoveryAt": null,
          "archive": {
            "source": "transcript",
            "status": "captured"
          }
        },
        "projection": {
          "id": "ctx_9a3728b21883",
          "dispatchId": "ctx_9a3728b21883",
          "taskId": "task_e90102f005e0",
          "runId": "run_a4723d345399",
          "role": "worker",
          "parent": null,
          "provider": null,
          "host": {
            "kind": "local",
            "id": "local"
          },
          "workspace": {
            "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
            "kind": "folder_or_worktree"
          },
          "stage": {
            "worker": "succeeded",
            "dispatch": "completed",
            "detail": "settled",
            "activity": "unknown"
          },
          "outcome": "succeeded",
          "liveness": {
            "verdict": "exited",
            "source": "resource_release"
          },
          "evidence": {
            "durable": true,
            "liveStatus": "unavailable",
            "lastObservedAt": null
          },
          "resource": {
            "state": "released"
          },
          "nextAction": {
            "kind": "none",
            "argv": []
          },
          "attention": {
            "categories": [
              "root_completion"
            ],
            "requiresAction": false
          }
        }
      },
      {
        "dispatchId": "ctx_4e3237d227c3",
        "taskId": "task_38990284224c",
        "runId": "run_a4723d345399",
        "workerState": "succeeded",
        "dispatchStatus": "completed",
        "agentTerminalHandle": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
        "terminalState": "released",
        "resource": {
          "id": "wtr_8fa5f5e6c0c9",
          "ownershipState": "released",
          "releaseState": "released",
          "retainedReason": null,
          "terminalHandle": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
          "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
          "endpointId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
          "endpointIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@ff748a50:d87771f2-b243-462b-b5e2-8fbf74345971",
          "originDispatchId": "ctx_4e3237d227c3",
          "ownerDispatchId": "ctx_4e3237d227c3",
          "releaseRequestedAt": "2026-11-11 19:52:23",
          "releaseCompletedAt": "2026-11-11 19:52:25",
          "releaseError": null,
          "recoveryAttemptCount": 0,
          "lastRecoveryAt": null,
          "archive": {
            "source": "transcript",
            "status": "captured"
          }
        },
        "projection": {
          "id": "ctx_4e3237d227c3",
          "dispatchId": "ctx_4e3237d227c3",
          "taskId": "task_38990284224c",
          "runId": "run_a4723d345399",
          "role": "worker",
          "parent": null,
          "provider": null,
          "host": {
            "kind": "local",
            "id": "local"
          },
          "workspace": {
            "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
            "kind": "folder_or_worktree"
          },
          "stage": {
            "worker": "succeeded",
            "dispatch": "completed",
            "detail": "settled",
            "activity": "unknown"
          },
          "outcome": "succeeded",
          "liveness": {
            "verdict": "exited",
            "source": "resource_release"
          },
          "evidence": {
            "durable": true,
            "liveStatus": "unavailable",
            "lastObservedAt": null
          },
          "resource": {
            "state": "released"
          },
          "nextAction": {
            "kind": "none",
            "argv": []
          },
          "attention": {
            "categories": [
              "root_completion"
            ],
            "requiresAction": false
          }
        }
      },
      {
        "dispatchId": "ctx_7c86fffa9716",
        "taskId": "task_a6a2a3f9e170",
        "runId": "run_a4723d345399",
        "workerState": "succeeded",
        "dispatchStatus": "completed",
        "agentTerminalHandle": "term_c2f40c56-7f46-4ba2-8f9f-4127b229d352",
        "terminalState": "released",
        "resource": {
          "id": "wtr_5a9324a2e491",
          "ownershipState": "released",
          "releaseState": "released",
          "retainedReason": null,
          "terminalHandle": "term_c2f40c56-7f46-4ba2-8f9f-4127b229d352",
          "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
          "endpointId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
          "endpointIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@389ca4c5:5bc66ec1-103f-4fab-98e0-22277f3dd9c2",
          "originDispatchId": "ctx_7c86fffa9716",
          "ownerDispatchId": "ctx_7c86fffa9716",
          "releaseRequestedAt": "2026-11-11 19:40:14",
          "releaseCompletedAt": "2026-11-11 19:40:15",
          "releaseError": null,
          "recoveryAttemptCount": 0,
          "lastRecoveryAt": null,
          "archive": {
            "source": "transcript",
            "status": "captured"
          }
        },
        "projection": {
          "id": "ctx_7c86fffa9716",
          "dispatchId": "ctx_7c86fffa9716",
          "taskId": "task_a6a2a3f9e170",
          "runId": "run_a4723d345399",
          "role": "worker",
          "parent": null,
          "provider": null,
          "host": {
            "kind": "local",
            "id": "local"
          },
          "workspace": {
            "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
            "kind": "folder_or_worktree"
          },
          "stage": {
            "worker": "succeeded",
            "dispatch": "completed",
            "detail": "settled",
            "activity": "unknown"
          },
          "outcome": "succeeded",
          "liveness": {
            "verdict": "exited",
            "source": "resource_release"
          },
          "evidence": {
            "durable": true,
            "liveStatus": "unavailable",
            "lastObservedAt": null
          },
          "resource": {
            "state": "released"
          },
          "nextAction": {
            "kind": "none",
            "argv": []
          },
          "attention": {
            "categories": [
              "root_completion"
            ],
            "requiresAction": false
          }
        }
      },
      {
        "dispatchId": "ctx_dad78c5c1332",
        "taskId": "task_381ac7af9ed1",
        "runId": "run_a4723d345399",
        "workerState": "succeeded",
        "dispatchStatus": "completed",
        "agentTerminalHandle": "term_88360819-3622-4c35-821d-e06faf346ab4",
        "terminalState": "released",
        "resource": {
          "id": "wtr_211bc168b1da",
          "ownershipState": "released",
          "releaseState": "released",
          "retainedReason": null,
          "terminalHandle": "term_88360819-3622-4c35-821d-e06faf346ab4",
          "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
          "endpointId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
          "endpointIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@773fac13:22111d74-43be-4875-965f-1da53b6a53e5",
          "originDispatchId": "ctx_dad78c5c1332",
          "ownerDispatchId": "ctx_dad78c5c1332",
          "releaseRequestedAt": "2026-11-11 19:42:24",
          "releaseCompletedAt": "2026-11-11 19:42:25",
          "releaseError": null,
          "recoveryAttemptCount": 0,
          "lastRecoveryAt": null,
          "archive": {
            "source": "transcript",
            "status": "captured"
          }
        },
        "projection": {
          "id": "ctx_dad78c5c1332",
          "dispatchId": "ctx_dad78c5c1332",
          "taskId": "task_381ac7af9ed1",
          "runId": "run_a4723d345399",
          "role": "worker",
          "parent": null,
          "provider": null,
          "host": {
            "kind": "local",
            "id": "local"
          },
          "workspace": {
            "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
            "kind": "folder_or_worktree"
          },
          "stage": {
            "worker": "succeeded",
            "dispatch": "completed",
            "detail": "settled",
            "activity": "unknown"
          },
          "outcome": "succeeded",
          "liveness": {
            "verdict": "exited",
            "source": "resource_release"
          },
          "evidence": {
            "durable": true,
            "liveStatus": "unavailable",
            "lastObservedAt": null
          },
          "resource": {
            "state": "released"
          },
          "nextAction": {
            "kind": "none",
            "argv": []
          },
          "attention": {
            "categories": [
              "root_completion"
            ],
            "requiresAction": false
          }
        }
      }
    ],
    "counts": {
      "released": 5
    },
    "page": {
      "limit": 100,
      "total": 5,
      "hasMore": false,
      "nextCursor": null
    },
    "scope": {
      "run": "run_a4723d345399",
      "source": "flag"
    }
  },
  "_meta": {
    "runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"
  }
}
~~~

## 1. `run-current`, no-binding shape (capture item 1)

Command: `orca-ide orchestration run-current`

Exit code: 0. Stderr: empty. Stdout:

~~~
No Run is bound to this terminal.
~~~

What it settles: the no-binding shape is one plain sentence, `No Run is bound to this terminal.`, exit code 0 (not an error exit). This is the shape for `bind_run` when no Run is bound, FR-002 fourth test and FR-026 case 4.

UNVERIFIED: the shape when a Run IS bound. No Run is bound to this terminal, and the capture never binds one (binding writes Orca state). Reason: this step is read-only by rule.

## 2. Is `run-current` output parseable without `--json`? (capture item 2)

Command: the same single `run-current` read as section 1 (no second call).

What it settles: the unbound plain output is one English sentence with no key/value fields and no id, so it can be matched as an exact string for the "no Run bound" case, but nothing in it is parseable as structured data. Whether the BOUND plain output is parseable is UNVERIFIED (see section 1). Per the design (section 15.1) the capture does not run the JSON form of this template; the open question for the owner note (M2) is therefore: bound-case plain output is unobserved, so `bind_run` cannot yet be specified from evidence for the bound case.

## 3. `worker-list --run <run> --json` schema, page size, cursor field (capture item 3)

Command: `orca-ide orchestration worker-list --run run_a4723d345399 --json`, run twice: section 0 (id-learning read) and again in the middle reads.

Middle read: exit code 0, stderr empty, stdout 13779 bytes, sha256 `8fac1f4e91e0186776c2823eeea21388dd0ff693c70dec625fbdd121a85fd539`, raw bytes at `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/m-t2-workerlist.json`. Payload (envelope `id` removed) equals the section 0 payload: yes.

Top-level shape: `{id, ok, result, _meta}`; `result` keys: `workers, counts, page, scope`. `_meta` holds `runtimeId`.

Page object (observed): `{"limit": 100, "total": 5, "hasMore": false, "nextCursor": null}`. So the page size is 100 (`limit`), the total row count is `total`, and the continuation fields are `hasMore` (bool) and `nextCursor` (null here). `counts` is a map of terminal state to row count (`{"released": 5}`). `scope` is `{run, source}` with `source: "flag"` when the Run is passed by flag.

Per-worker fields (`result.workers[]`): `agentTerminalHandle, dispatchId, dispatchStatus, projection{attention.categories[], dispatchId, evidence{durable, liveStatus}, host{id, kind}, id, liveness{source, verdict}, nextAction.kind, outcome, resource.state, role, runId, stage{activity, detail, dispatch, worker}, taskId, workspace{id, kind}}, resource{archive{source, status}, endpointId, endpointIncarnation, id, originDispatchId, ownerDispatchId, ownershipState, recoveryAttemptCount, releaseCompletedAt, releaseRequestedAt, releaseState, terminalHandle, worktreeId}, runId, taskId, terminalState, workerState`.

UNVERIFIED: the behaviour of a second page. This Run has 5 rows and `hasMore` is false, so `nextCursor` was never non-null; the flag that passes a cursor was not tried (no template for it is allowlisted in step 1.0a).

## 4. `worker-show --dispatch <dispatch> --json` fields (capture item 4)

Commands (one per Dispatch id, run before and again after the other reads): `orca-ide orchestration worker-show --dispatch <id> --json` for each of ctx_4e3237d227c3, ctx_6a0e3e3baaee, ctx_7c86fffa9716, ctx_9a3728b21883, ctx_dad78c5c1332.

| Dispatch id | Exit (before / after) | Stdout bytes | sha256 of raw before | Raw copy |
|---|---|---|---|---|
| ctx_4e3237d227c3 | 0 / 0 | 7740 | `16f72f82f86bce77...` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_4e3237d227c3.json` |
| ctx_6a0e3e3baaee | 0 / 0 | 7724 | `a20a0fcb5329ab36...` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_6a0e3e3baaee.json` |
| ctx_7c86fffa9716 | 0 / 0 | 7709 | `2ef49655c791a1d9...` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_7c86fffa9716.json` |
| ctx_9a3728b21883 | 0 / 0 | 7756 | `5fec253d0554e333...` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_9a3728b21883.json` |
| ctx_dad78c5c1332 | 0 / 0 | 7758 | `782fe237a205db51...` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_dad78c5c1332.json` |

Top-level `result` keys: `dispatch, observation, projection, terminal, terminalResource, worker`.

Fields that can carry a session join (all present for all 5 workers):

| Field | Form | Example |
|---|---|---|
| `result.dispatch.assigneePaneKey` | `<tabId>:<leafId>` (two UUIDs joined by a colon) | `9f81c468-ea33-4f83-acf2-3975a83f4307:d5c3d28c-c3c6-47a7-8ebf-9f75e2d280c4` |
| `result.dispatch.assigneeHandle` | `term_<uuid>` | `term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e` |
| `result.terminal.handle` and `result.worker.agentTerminalHandle` and `result.terminalResource.terminalHandle` | the same `term_<uuid>` | same value as `assigneeHandle` |
| `result.terminal.tabId`, `result.terminal.leafId` | the two halves of the pane key | `9f81c468-...`, `d5c3d28c-...` |
| `result.terminal.paneRuntimeId` | integer | `-1` for all 5 (these workers are exited) |

No structured `worker-show` field holds a Claude session id. The id appears only as free text in `result.terminal.preview` (`claude --resume <id>`) for all 5 exited workers; whether a live worker's preview shows it is UNVERIFIED, so it is not used as a join. Path B applies. The tab-map entry (section 13) is the structured place a session id was found.

Other requested fields, observed values:

| Item | Observed |
|---|---|
| `agentWait` | ABSENT: the key does not occur in any `worker-show` output (searched all 5 raw outputs). |
| `liveness.verdict` | at `result.projection.liveness.verdict`; value `exited` for all 5 (`result.projection.liveness.source` is also present). |
| `status` | `result.dispatch.status`; value `completed` for all 5. The five-value set (`pending`, `dispatched`, `completed`, `failed`, `circuit_broken`) was not exercised beyond `completed`. |
| `dispatch.dispatchedAt` | present, form `YYYY-MM-DD HH:MM:SS` (SQLite form), e.g. `2026-11-11 19:35:55`. |
| `dispatch.completedAt` | present, form ISO 8601 with milliseconds and `Z`, e.g. `2026-11-11T19:52:10.258Z`. This settles the `completedAt` form for completed rows: ISO 8601, not the SQLite form. |
| `dispatch.status` | present (see `status`). |
| `dispatch.lastHeartbeatAt`, `dispatch.createdAt` | present (other timestamp fields). |

UNVERIFIED sub-checks, with the reason:

- Whether `dispatchedAt` is earlier than the first transcript record of the worker's session: needs a read of a session transcript, which lies outside the one folder this step may read (the tab-map folder) and which the allowlist does not cover. Not attempted.
- Whether `completedAt` is set for `failed` and `circuit_broken` rows: this Run has only `completed` rows (all 5), so no such row was observed.

Full stdout of the first Dispatch (the other four have the same shape; raw copies are listed above):

Command: `orca-ide orchestration worker-show --dispatch ctx_4e3237d227c3 --json`

~~~
{
  "id": "59abeb89-6d4b-4f66-b9a9-6f77987c46ae",
  "ok": true,
  "result": {
    "dispatch": {
      "id": "ctx_4e3237d227c3",
      "runId": "run_a4723d345399",
      "taskId": "task_38990284224c",
      "task_id": "task_38990284224c",
      "contractVersion": 1,
      "assigneeHandle": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
      "assigneePaneKey": "9f81c468-ea33-4f83-acf2-3975a83f4307:d5c3d28c-c3c6-47a7-8ebf-9f75e2d280c4",
      "processIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@ff748a50:d87771f2-b243-462b-b5e2-8fbf74345971",
      "capabilityRevokedAt": "2026-11-11T19:52:10.258Z",
      "retryOfDispatchId": null,
      "creatorDispatchId": null,
      "hostScope": {
        "kind": "local",
        "hostId": "local"
      },
      "status": "completed",
      "failureCount": 0,
      "lastFailure": null,
      "terminationReason": null,
      "depth": 1,
      "dispatchedAt": "2026-11-11 19:35:55",
      "completedAt": "2026-11-11T19:52:10.258Z",
      "createdAt": "2026-11-11 19:35:55",
      "lastHeartbeatAt": "2026-11-11T19:40:28Z"
    },
    "worker": {
      "dispatchId": "ctx_4e3237d227c3",
      "runtimeEpoch": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
      "state": "succeeded",
      "stage": "settled",
      "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
      "agentTerminalHandle": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
      "setupState": "not_applicable",
      "effects": [
        {
          "kind": "worktree",
          "action": "reused",
          "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504"
        },
        {
          "kind": "setup",
          "action": "not_applicable",
          "state": "not_applicable"
        },
        {
          "kind": "terminal",
          "role": "agent",
          "action": "created",
          "id": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
          "surface": "background",
          "warning": "Terminal term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e is running, but Orca could not make it discoverable. Run `orca terminal focus --terminal term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e` to reveal and focus it."
        },
        {
          "kind": "dispatch_input",
          "role": "agent",
          "id": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
          "state": "accepted"
        }
      ],
      "residualResources": [
        {
          "kind": "terminal",
          "role": "agent",
          "action": "created",
          "id": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
          "surface": "background",
          "warning": "Terminal term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e is running, but Orca could not make it discoverable. Run `orca terminal focus --terminal term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e` to reveal and focus it."
        }
      ],
      "startOptions": {
        "worktree": "id:de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
        "mode": {
          "mode": "terminal",
          "preferred": "terminal",
          "reason": "user_default",
          "detail": "Started a terminal agent worker, the default for new agent tabs in your settings."
        },
        "resolvedWorktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
        "name": null,
        "repo": null,
        "baseBranch": null,
        "terminal": null,
        "agent": "claude",
        "launch": {
          "requested": {
            "agent": "claude",
            "model": null,
            "effort": null
          },
          "effective": {
            "agent": "claude",
            "model": null,
            "effort": null
          }
        },
        "timeoutMs": 60000,
        "setup": "not_applicable",
        "setupSource": "existing_worktree"
      },
      "lastError": null,
      "createdAt": "2026-11-11 19:35:55",
      "updatedAt": "2026-11-11T19:52:10.259Z"
    },
    "projection": {
      "id": "ctx_4e3237d227c3",
      "dispatchId": "ctx_4e3237d227c3",
      "taskId": "task_38990284224c",
      "runId": "run_a4723d345399",
      "role": "worker",
      "parent": null,
      "provider": null,
      "host": {
        "kind": "local",
        "id": "local"
      },
      "workspace": {
        "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
        "kind": "folder_or_worktree"
      },
      "stage": {
        "worker": "succeeded",
        "dispatch": "completed",
        "detail": "settled",
        "activity": "unknown"
      },
      "outcome": "succeeded",
      "liveness": {
        "verdict": "exited",
        "source": "resource_release"
      },
      "evidence": {
        "durable": true,
        "liveStatus": "unavailable",
        "lastObservedAt": null
      },
      "resource": {
        "state": "released",
        "id": "wtr_8fa5f5e6c0c9",
        "ownerDispatchId": "ctx_4e3237d227c3",
        "releaseState": "released",
        "terminalState": "released"
      },
      "nextAction": {
        "kind": "none",
        "argv": []
      },
      "attention": {
        "categories": [
          "root_completion"
        ],
        "requiresAction": false
      }
    },
    "terminal": {
      "handle": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
      "ptyId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@ff748a50",
      "incarnationId": "d87771f2-b243-462b-b5e2-8fbf74345971",
      "orphaned": false,
      "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
      "worktreePath": "/home/coder/workspaces/worktrees/IronClaude/issue-504",
      "branch": "refs/heads/ironbelly/issue-504",
      "tabId": "9f81c468-ea33-4f83-acf2-3975a83f4307",
      "leafId": "d5c3d28c-c3c6-47a7-8ebf-9f75e2d280c4",
      "title": "issue-504-1111-193642-2121 \u00b7 Claude Code",
      "connected": false,
      "writable": false,
      "lastOutputAt": 1794426745213,
      "preview": "[ccsession] Cached 21 curated gateway models before launch\n[ccsession] Starting new session labeled 'issue-504-1111-193642-2121'\n6 15        3 06   3  36BB\nResume this session with:\nclaude --resume 04f1e248-bb2f-451f-9372-0c3c1522822e\nissue-504 ironbelly/issue-504 !",
      "exitCause": {
        "kind": "operator_close"
      },
      "executionHostId": "local",
      "paneRuntimeId": -1,
      "rendererGraphEpoch": 0
    },
    "observation": {
      "status": "exited",
      "exactWorker": true
    },
    "terminalResource": {
      "id": "wtr_8fa5f5e6c0c9",
      "ownershipState": "released",
      "releaseState": "released",
      "retainedReason": null,
      "terminalHandle": "term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e",
      "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504",
      "endpointId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f",
      "endpointIncarnation": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-504@@ff748a50:d87771f2-b243-462b-b5e2-8fbf74345971",
      "originDispatchId": "ctx_4e3237d227c3",
      "ownerDispatchId": "ctx_4e3237d227c3",
      "releaseRequestedAt": "2026-11-11 19:52:23",
      "releaseCompletedAt": "2026-11-11 19:52:25",
      "releaseError": null,
      "recoveryAttemptCount": 0,
      "lastRecoveryAt": null,
      "archive": {
        "source": "transcript",
        "status": "captured"
      }
    }
  },
  "_meta": {
    "runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"
  }
}
~~~

## 5. `task-list` shapes and the creator field (capture item 5)

Commands: `orca-ide orchestration task-list --ready --run run_a4723d345399 --json` and `orca-ide orchestration task-list --run run_a4723d345399 --json`, each run before and after.

`--ready`: exit 0 (before) / 0 (after), stderr empty, 252 bytes. Full stdout:

~~~
{
  "id": "54df73fc-122a-475e-a4a0-58902416edb2",
  "ok": true,
  "result": {
    "runId": "run_a4723d345399",
    "legacyReadOnly": false,
    "tasks": [],
    "count": 0
  },
  "_meta": {
    "runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"
  }
}
~~~

The ready list is empty (`tasks: []`, `count: 0`): every task in this Run is `completed`.

Without `--ready`: exit 0 / 0, stderr empty, 33923 bytes, sha256 `56edebd8d79834b61942490b37d0c3cf6e1d74f41ac6bcac580a90e54c276075`, raw bytes at `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-tl-all.json`. Shape: `result` keys `runId, legacyReadOnly, tasks, count`; `count` 5; every task has `status: completed`.

Task fields: `id, run_id, parent_id, created_by_terminal_handle, created_by_pane_key, created_by_process_incarnation, created_by_run_generation, task_title, display_name, spec, status, deps, result, created_at, completed_at`.

A creator field EXISTS: `created_by_terminal_handle` (`term_<uuid>`), `created_by_pane_key` (`<tabId>:<leafId>`), `created_by_process_incarnation` and `created_by_run_generation`. These feed Rule 4 (b) and the Waiting (b) sub-heading.

Task id sample: `task_381ac7af9ed1` (`task_` plus 12 lowercase hex characters).

### Before/after comparison (the live no-change check, M4)

Compared with timestamps removed. Method: parse each stdout as JSON, drop the top-level `id` key, sort keys, hash the result. The `worker-show` and `task-list` calls were run before and after the other reads.

The raw bytes of both sides are stored under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/` (`b-...` = before, `a-...` = after). Each row gives the sha256 of the canonical payload (envelope `id` removed, keys sorted) for each side.

| Read | Raw bytes identical | Payload identical (envelope `id` removed) | Before payload sha256 | After payload sha256 | Raw before / after files |
|---|---|---|---|---|---|
| worker-show ctx_4e3237d227c3 | no | yes | `a50676e24f3cf6649de137a3859044a61edd6954b4e97b696e2b4951e518225d` | `a50676e24f3cf6649de137a3859044a61edd6954b4e97b696e2b4951e518225d` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_4e3237d227c3.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-ws-ctx_4e3237d227c3.json` |
| worker-show ctx_6a0e3e3baaee | no | yes | `38f132368466c4a8081b8fcd64b185ace1b24cf6d125e2d22397008fa897ec77` | `38f132368466c4a8081b8fcd64b185ace1b24cf6d125e2d22397008fa897ec77` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_6a0e3e3baaee.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-ws-ctx_6a0e3e3baaee.json` |
| worker-show ctx_7c86fffa9716 | no | yes | `676a42c7566b6181c8a9a485c3c31a52950885673c84c11f2c4ba157bb32f7a8` | `676a42c7566b6181c8a9a485c3c31a52950885673c84c11f2c4ba157bb32f7a8` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_7c86fffa9716.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-ws-ctx_7c86fffa9716.json` |
| worker-show ctx_9a3728b21883 | no | yes | `b67428936a7a8dd001ebd5c5a43186d7183d7abc9f3dbbcdd1a5c5a7435eee48` | `b67428936a7a8dd001ebd5c5a43186d7183d7abc9f3dbbcdd1a5c5a7435eee48` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_9a3728b21883.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-ws-ctx_9a3728b21883.json` |
| worker-show ctx_dad78c5c1332 | no | yes | `a5b19a77cae135eb558a82569abf152997221f6d73a906c75861dccb0287b807` | `a5b19a77cae135eb558a82569abf152997221f6d73a906c75861dccb0287b807` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-ws-ctx_dad78c5c1332.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-ws-ctx_dad78c5c1332.json` |
| task-list --ready | no | yes | `f08fe8f9b63b91d0098a3852ff386146a08f27efbb724014e80b41ebccbcf5c4` | `f08fe8f9b63b91d0098a3852ff386146a08f27efbb724014e80b41ebccbcf5c4` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-tl-ready.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-tl-ready.json` |
| task-list (all) | no | yes | `0d06a2cbb915ddda992dd4e590788c2a7945f9ce18a9d68c13acbc0acf5ce0d1` | `0d06a2cbb915ddda992dd4e590788c2a7945f9ce18a9d68c13acbc0acf5ce0d1` | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/b-tl-all.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw/a-tl-all.json` |

Result: the raw bytes differ in exactly one place per call, the top-level `id` (a different request id on every call, including two back-to-back identical calls). There is no timestamp in these payloads that changed, and no other field differs: every payload is identical once that request id is removed. Interpretation (made by the executor, stated openly): the request id is a response-envelope identifier, not Run, Task or Dispatch state, so it is not a difference in what the reads returned and the item's HALT rule ("differ apart from timestamps") is not applied. If the owner reads that rule as covering the envelope id, the HALT blocker text is: `Step 1.0a: worker-show or task-list output changed between the before and after reads; owner review needed (DESIGN 15.1)`.

## 6. `worktree ps --json`: the worktree path field (capture item 6)

Command: `orca-ide worktree ps --json`

Exit code: 0. Stderr: empty. Stdout: 131897 bytes, sha256 `468aa1bdb5ea9658e6e81ed5549503443e768a7a0ab4a69f6d007e4322916d40` (raw bytes not stored: they carry other sessions' prompts and messages).

Shape: `{id, ok, result{hostScope, totalCount, truncated, worktrees[]}, _meta}`; `totalCount` 28, `truncated` false.

The worktree path field is `result.worktrees[].path` (absolute path string). Other per-worktree fields: `workspaceKind, worktreeId, repoId, hostId, terminalPlatform, repo, path, branch, isArchived, isMainWorktree, hasHostSidebarActivity, defaultBranch, worktreeInstanceId, parentWorktreeId, childWorktreeIds, displayName, workspaceStatus, sortOrder, lastActivityAt, linkedIssue, linkedPR, linkedLinearIssue, linkedGitLabMR, linkedGitLabIssue, linkedItems, comment, isPinned, isActive, unread, liveTerminalCount, hasAttachedPty, unverifiableTerminalCount, lastOutputAt, preview, status, agents, sidebarStatus, terminalVerdict`. Each worktree has `agents[]` with `paneKey, parentPaneKey, state, agentType, prompt, taskTitle, displayName, lastAssistantMessage, toolName, toolInput, interrupted, mainAgent, stateStartedAt, updatedAt, subagents, hasLivePty, subagentObservation`.

Entry for this worktree, with message-text fields redacted (`prompt`, `lastAssistantMessage`, `toolInput`, `preview`, `taskTitle`):

~~~
{
  "worktreeId": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode",
  "path": "/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode",
  "branch": "refs/heads/ironbelly/issue-339-orchestrator-mode",
  "isMainWorktree": false,
  "liveTerminalCount": 3,
  "hasAttachedPty": true,
  "unverifiableTerminalCount": 0,
  "status": "working",
  "terminalVerdict": "live",
  "preview": "<redacted: terminal text>",
  "agents": [
    {
      "paneKey": "ac5bfee4-d304-4515-8858-17922034a517:2726f32a-8c5f-4c77-bfbf-4002d7a103e0",
      "state": "done",
      "agentType": "claude",
      "hasLivePty": true,
      "prompt": "<redacted>",
      "lastAssistantMessage": "<redacted>"
    },
    {
      "paneKey": "ac8308a5-c5be-4287-998e-e0fd01bea1aa:6621d0d8-ef6e-4f7c-b564-c43bce42b062",
      "state": "working",
      "agentType": "claude",
      "hasLivePty": true,
      "prompt": "<redacted>",
      "lastAssistantMessage": "<redacted>"
    }
  ]
}
~~~

## 7. `worktree list --json` and `worktree current --json` shapes (capture item 7)

Command: `orca-ide worktree list --json`

Exit code: 0. Stderr: empty. Stdout: 65339 bytes, sha256 `e87ca1551f98cb015cb3ae5fd49a8a78c37440bd788eb96f692099cbb78e6d0d`. Shape: `{id, ok, result{hostScope, totalCount, truncated, worktrees[]}, _meta}`; `totalCount` 28, `truncated` false. Per-entry fields: `id, identity, instanceId, repoId, hostId, path, head, branch, isBare, isMainWorktree, displayName, displayNameMode, comment, linkedIssue, linkedPR, linkedLinearIssue, linkedLinearIssueWorkspaceId, linkedLinearIssueOrganizationUrlKey, linkedGitLabMR, linkedGitLabIssue, linkedBitbucketPR, linkedAzureDevOpsPR, linkedGiteaPR, linkedWorkItem, linkedTaskSourceContext, isArchived, isUnread, isPinned, sortOrder, lastActivityAt, workspaceStatus, parentWorktreeId, childWorktreeIds, lineage, git, linkedItems`. Path field: `result.worktrees[].path`. (Raw bytes not stored; the listing names every Orca worktree on the host.)

Command: `orca-ide worktree current --json`

Exit code: 0. Stderr: empty. Shape: `{id, ok, result{worktree{...}}, _meta}`. Stdout in full:

~~~
{
  "id": "55a18a60-7bda-4927-825e-76b3dfc40c4e",
  "ok": true,
  "result": {
    "worktree": {
      "id": "de550e99-fa3c-42e2-abfe-1d092771c759::/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode",
      "identity": {
        "key": "wt2:local:8abd7ef3-90cf-4578-9d0e-152d565e3acd",
        "executionHostId": "local",
        "instanceId": "8abd7ef3-90cf-4578-9d0e-152d565e3acd"
      },
      "instanceId": "8abd7ef3-90cf-4578-9d0e-152d565e3acd",
      "repoId": "de550e99-fa3c-42e2-abfe-1d092771c759",
      "projectId": "github:superclaude-org/superclaude_framework",
      "hostId": "local",
      "projectHostSetupId": "de550e99-fa3c-42e2-abfe-1d092771c759",
      "creatorProvenance": {
        "kind": "host"
      },
      "path": "/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode",
      "head": "5dc29d23b15eb7db4ead50623bb409f696a0d7d3",
      "branch": "refs/heads/ironbelly/issue-339-orchestrator-mode",
      "isBare": false,
      "isMainWorktree": false,
      "displayName": "issue-339-orchestrator-mode",
      "displayNameMode": "fixed",
      "comment": "",
      "linkedIssue": null,
      "linkedPR": null,
      "linkedLinearIssue": null,
      "linkedLinearIssueWorkspaceId": null,
      "linkedLinearIssueOrganizationUrlKey": null,
      "linkedGitLabMR": null,
      "linkedGitLabIssue": null,
      "linkedBitbucketPR": null,
      "linkedAzureDevOpsPR": null,
      "linkedGiteaPR": null,
      "linkedWorkItem": null,
      "linkedTaskSourceContext": null,
      "isArchived": false,
      "isUnread": true,
      "isPinned": false,
      "sortOrder": 1794432910840,
      "lastActivityAt": 1794432847370,
      "createdAt": 1794035783506,
      "createdWithAgent": "claude",
      "baseRef": "refs/remotes/origin/master",
      "workspaceStatus": "in-progress",
      "parentWorktreeId": null,
      "childWorktreeIds": [],
      "lineage": null,
      "git": {
        "path": "/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode",
        "head": "5dc29d23b15eb7db4ead50623bb409f696a0d7d3",
        "branch": "refs/heads/ironbelly/issue-339-orchestrator-mode",
        "isBare": false,
        "isMainWorktree": false
      },
      "linkedItems": []
    }
  },
  "_meta": {
    "runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"
  }
}
~~~

These two shapes are recorded only (Phase 1 does not call them); the path field is `path` in both.

## 8. Unknown Run id (capture item 8)

Fake Run id of the same shape as the real one: `run_000000000000`.

Command: `orca-ide orchestration worker-list --run run_000000000000 --json`

Exit code: 0. Stderr: empty. Stdout:

~~~
{
  "id": "e786d84f-0336-4317-aee0-c626c6ec906e",
  "ok": true,
  "result": {
    "workers": [],
    "counts": {},
    "page": {
      "limit": 100,
      "total": 0,
      "hasMore": false,
      "nextCursor": null
    },
    "scope": {
      "run": "run_000000000000",
      "source": "flag"
    }
  },
  "_meta": {
    "runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"
  }
}
~~~

What it settles: an unknown Run id is NOT an error for `worker-list`: exit 0, `ok: true`, an empty `workers` list, `page.total` 0, `scope.run` echoing the fake id. This matches the earlier 2026-11-08 read.

Command (DEVIATION D1, see the last section: a template 5 call with the fake id, which the item's Action steps do not list; run for the second half of capture item 8): `orca-ide orchestration task-list --run run_000000000000 --json`

Exit code: 1. Stderr: empty (the error body is on stdout). Stdout:

~~~
{
  "id": "415116b4-8ea2-4088-a587-b28d9af8fb0d",
  "ok": false,
  "error": {
    "code": "run_not_found",
    "message": "Run run_000000000000 was not found."
  },
  "_meta": {
    "runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"
  }
}
~~~

What it settles: `task-list` on an unknown Run is an error: exit 1, `ok: false`, `error.code` `run_not_found`, message `Run run_000000000000 was not found.`. The error JSON is on stdout and stderr is empty.

## 9. `runtime_unavailable` shape (capture item 9)

UNVERIFIED. Orca was available during the whole capture: every read above returned a response (`_meta.runtimeId` `a7ee70a1-2e8b-4476-a228-51e9c7019b3f` in each). The item says to record this shape only if Orca is already unavailable, and never to induce it; Orca was not unavailable, so there is nothing to record.

## 10. Run id and Dispatch id samples (capture item 10)

From the reads above (all observed, none constructed):

| Kind | Samples | Shape observed |
|---|---|---|
| Run id | `run_a4723d345399` (the real Run; the fake `run_000000000000` was accepted by both templates without a format error) | `run_` plus 12 lowercase hex characters |
| Dispatch id | `ctx_4e3237d227c3`, `ctx_6a0e3e3baaee`, `ctx_7c86fffa9716`, `ctx_9a3728b21883`, `ctx_dad78c5c1332` | `ctx_` plus 12 lowercase hex characters |
| Task id | `task_381ac7af9ed1`, `task_a6a2a3f9e170`, `task_38990284224c`, `task_e90102f005e0`, `task_d7ba23de62d2` | `task_` plus 12 lowercase hex characters |
| Terminal handle | `term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e` | `term_` plus a UUID |
| Worker resource id | `wtr_8fa5f5e6c0c9` | `wtr_` plus 12 lowercase hex characters |

What it settles: the `DISPATCH_ID_RE` half of the design's open item 2 can now be written from observed samples: Dispatch ids begin `ctx_`; `RUN_ID_RE` from `run_` plus 12 hex. All 5 Dispatch ids share the one shape. Only one Run was sampled, so the hex length is evidence from 5 Dispatch ids and 1 Run id.

## 11. Does each template accept its flags as written? (capture item 11)

| # | Template | Exit | Parseable output |
|---|---|---|---|
| 1 | `orca-ide orchestration run-current` | 0 | plain sentence (no structure) |
| 2 | `orca-ide orchestration worker-list --run <run> --json` | 0 / 0 | JSON, parsed |
| 3 | `orca-ide orchestration worker-show --dispatch <dispatch> --json` | 0, 0, 0, 0, 0 | JSON, parsed |
| 4 | `orca-ide orchestration task-list --ready --run <run> --json` | 0 | JSON, parsed |
| 5 | `orca-ide orchestration task-list --run <run> --json` | 0 | JSON, parsed |
| 6 | `orca-ide worktree ps --json` | 0 | JSON, parsed |
| 7 | `orca-ide worktree list --json` | 0 | JSON, parsed |
| 8 | `orca-ide worktree current --json` | 0 | JSON, parsed |

All eight templates accepted their flags as written against a real Run (exit 0, parseable output). The only non-zero exit in the capture was the deliberate unknown-Run `task-list` read (section 8), exit 1 with a JSON error body.

## 12. Installed Orca version (capture item 12)

File read: `/opt/Orca/resources/app.asar.unpacked/out/package.json`

Content read:

~~~
{
  "name": "orca-compiled-output",
  "type": "commonjs",
  "private": true,
  "version": "1.4.245-aidev02.9cfecdd30b2a",
  "commit": "9cfecdd30b2a90c06e5178b1245cb31a97d11bac"
}
~~~

Version string: `1.4.245-aidev02.9cfecdd30b2a` (commit `9cfecdd30b2a90c06e5178b1245cb31a97d11bac`). This is the NFR-015 pin value. It differs from the string the design recorded earlier (DESIGN line 30: `1.4.245-aidev02.780594c521aa`): same version number, different build suffix, so Orca was updated between that read and this one.

## 13. Tab-map entries for the Run's workers (capture item 13)

Command (path resolution): `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"`

Printed path: `/home/coder/.local/state/ccsession/orca-tabs/`

Command: `ls -la /home/coder/.local/state/ccsession/orca-tabs/` (run twice: once shown on screen, cut to its first 60 lines by the caller; once saved in full for matching; both show `total 1584`)

Exit code: 0. Stderr: empty. The listing has 385 lines (the `total` line, `.`, `..`, the `.ccsession-lock` file, and 381 entries). First lines:

~~~
total 1584
drwxr-xr-x 2 coder coder 53248 Nov 11 21:34 .
drwxr-xr-x 3 coder coder  4096 Nov  3 20:26 ..
-rw-r--r-- 1 coder coder     0 Nov  3 20:26 .ccsession-lock
-rw------- 1 coder coder   140 Nov  8 13:16 0019105f-1717-42a0-b9d9-c102da26260e+774b7109-2b41-4da9-81e6-2be23b34ae99
-rw------- 1 coder coder   118 Nov  9 16:57 0158fe45-aca4-4f7a-aee9-e8a96490f238+2a52abd2-c95f-4175-ac10-c642bf8b1d8e
~~~

Each entry's name is `<tabId>+<leafId>`: the worker's `assigneePaneKey` with the colon replaced by a plus sign. The listing lines for the five workers of this Run:

~~~
-rw------- 1 coder coder   133 Nov 11 19:36 9f81c468-ea33-4f83-acf2-3975a83f4307+d5c3d28c-c3c6-47a7-8ebf-9f75e2d280c4
-rw------- 1 coder coder   133 Nov 11 19:38 23814577-5dea-41d7-b23c-21176f702aef+b574cbeb-e224-4915-aa22-ea705dcfeb16
-rw------- 1 coder coder   133 Nov 11 19:35 20ce95c1-13a5-467f-abad-3d519fee3877+14cc0699-b420-4848-873b-bcbab8e5af46
-rw------- 1 coder coder   133 Nov 11 19:37 6aed44d1-77d8-40c2-ac56-c85df77f5145+56baf805-e8ce-454c-9c59-7b05e46120cd
-rw------- 1 coder coder   133 Nov 11 19:35 b75f74b5-75c0-4698-bf8f-1c0e3da35a0d+26a253c7-010a-4e9c-ba79-55c6a108700b
~~~

Files read (only these five, inside the folder above; each holds 3 lines: Claude session id, working directory, terminal handle):

| Dispatch id | Tab-map file name | Line 1 (Claude session id) | Line 2 (cwd) | Line 3 (terminal handle) | Line 3 equals `assigneeHandle` and `terminal.handle` |
|---|---|---|---|---|---|
| ctx_4e3237d227c3 | `9f81c468-ea33-4f83-acf2-3975a83f4307+d5c3d28c-c3c6-47a7-8ebf-9f75e2d280c4` | `04f1e248-bb2f-451f-9372-0c3c1522822e` | `/home/coder/workspaces/worktrees/IronClaude/issue-504` | `term_bfc93c3a-75f5-46c7-bae1-eca8cc7c646e` | yes |
| ctx_6a0e3e3baaee | `23814577-5dea-41d7-b23c-21176f702aef+b574cbeb-e224-4915-aa22-ea705dcfeb16` | `3ca57b4e-b4ee-407f-902a-7e2bf106084c` | `/home/coder/workspaces/worktrees/IronClaude/issue-504` | `term_12f4e391-99b0-4528-a6dc-483bd7c20dcf` | yes |
| ctx_7c86fffa9716 | `20ce95c1-13a5-467f-abad-3d519fee3877+14cc0699-b420-4848-873b-bcbab8e5af46` | `72f129f1-5b59-4ea9-bddc-a349c8cc11f0` | `/home/coder/workspaces/worktrees/IronClaude/issue-504` | `term_c2f40c56-7f46-4ba2-8f9f-4127b229d352` | yes |
| ctx_9a3728b21883 | `6aed44d1-77d8-40c2-ac56-c85df77f5145+56baf805-e8ce-454c-9c59-7b05e46120cd` | `09d4521f-b24f-4ed3-860c-33b6fb013bf6` | `/home/coder/workspaces/worktrees/IronClaude/issue-504` | `term_1212fabf-cde3-4350-a807-5d0aac19a520` | yes |
| ctx_dad78c5c1332 | `b75f74b5-75c0-4698-bf8f-1c0e3da35a0d+26a253c7-010a-4e9c-ba79-55c6a108700b` | `7832d8b6-85a3-4457-a2f7-b8b22b4d2bd2` | `/home/coder/workspaces/worktrees/IronClaude/issue-504` | `term_88360819-3622-4c35-821d-e06faf346ab4` | yes |

What it settles:

- All 5 workers have a tab-map entry (5 of 5). The entry name equals the worker's `assigneePaneKey` with `:` replaced by `+`; that is the join key for path B.
- The entry content line 3 equals the `term_<uuid>` handle (`assigneeHandle`, `terminal.handle`); line 1 is the Claude session id, which no structured `worker-show` field carries (it appears only as free text in `result.terminal.preview`, see section 4). So the tab-map is the only place found in this capture where the pane key or handle joins to a session id.
- Worker launch through `ccsession`: the five tab-map entries exist (an entry is written only for a `ccsession` launch, DESIGN line 32), and the terminal preview of four of the five workers shows the `[ccsession]` banner (the fifth, `ctx_9a3728b21883`, shows no banner in its preview, but it has an entry). So the workers were launched through `ccsession`, inferred from the entries; it is not stated by any `worker-show` field.
- The entry for the first worker's session (`04f1e248-bb2f-451f-9372-0c3c1522822e`) matches the resume line in that worker's terminal preview (`claude --resume 04f1e248-bb2f-451f-9372-0c3c1522822e`). The same holds for all 5 workers: each stored `worker-show` output in `readonly-probe-raw/` holds a `claude --resume <id>` line in `result.terminal.preview` (cycle-1 fix, finding DEC-F3).
- No other folder was read.

## Compliance record

- Commands issued against Orca: the eight templates, each with the Run id or Dispatch ids the item allows, plus one call outside the item's allowed uses (Deviation D1 below). The forbidden commands were not issued.
- Reads other than Orca: the Orca `package.json` (section 12), the tab-map path `echo` and `ls -la`, and the five tab-map files (section 13).
- Not captured, with reason: bound `run-current` shape (no Run bound; section 1), bound-output parseability (section 2), a second `worker-list` page (section 3), the `dispatchedAt` versus transcript comparison and `completedAt` for `failed` and `circuit_broken` rows (section 4), the `runtime_unavailable` shape (section 9).
- No write command was issued; no Run, Task or Dispatch was created by the capture. The before and after reads of `worker-show` and `task-list` matched (see the comparison under section 5), which is the only live check of that.

## Deviations

- D1: the item says the only commands allowed are the eight templates with `<run>` the recorded Run id and `<dispatch>` a Dispatch id from the first `worker-list`, and its Action uses a fake Run id for template 2 only. The executor also ran template 5 (`task-list --run`) once with the fake Run id `run_000000000000`, to record the error shape that capture item 8 asks for ("the error shape of `task-list --run <unknown id>`"). The call is read-only and it returned exit 1 with `run_not_found` (section 8), but it is outside the item's literal allowance. It is recorded here so the owner can see it; it changed nothing in Orca (the `run_not_found` reply shows it found no Run).
