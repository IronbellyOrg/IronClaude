# 07 - Research gate gap-fill (fix cycle 1)

**Status:** Complete
**Date:** 2026-11-07
**Written by:** the research-gate fix agent, for blocking findings B-04, B-07, B-09 and B-24 in `qa/qa-consolidated-findings-phase3.md`.
**Method:** read-only. Sources are repository files, Orca `--help` text (CLI 1.4.245-aidev02.780594c521aa) and the installed Orca CLI handler sources under `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/`. No Orca verb was run except `--help`; no state-changing command was run.

Tag meaning in this file: [CODE-VERIFIED: <file:line>] means the claim was read in that source file today. A handler read proves what the CLI sends to the Orca runtime, not what the runtime does with it; runtime behaviour stays [UNVERIFIED] unless a capture shows it.

---

## A. Output style and job-identity hook (B-04)

### A.1 `src/superclaude/output-styles/pragmatic.md`

| Line | Rule text (verbatim excerpt) | Tag |
|---|---|---|
| `:22` | "EVERY response includes a DONE / NEXT table. No exceptions. In a wrap-up or a multi-point reply it leads the response; in any other response it closes the response." | [CODE-VERIFIED: pragmatic.md:22] |
| `:53` | "CRITICAL: Lead every wrap-up with a plain-language DONE / NEXT summary (scannable table), never buried under the work narrative." | [CODE-VERIFIED: pragmatic.md:53] |

**Exception mechanism:** none. A grep of the file for `exception|unless|except` finds only `:22` ("No exceptions"), `:111` (destructive actions "unless part of task or task file") and `:126` ("no exceptions" for fabrication). None of these carves out a coordinator, worker or orchestrator mode [CODE-VERIFIED: grep of pragmatic.md]. Consequence for the design: an orchestrator-mode reply that must not carry the table needs a new, explicit exception added to `:22`; the current text gives no route for it. Whether to add one stays an owner decision (research-notes Section "open decisions" item 6).

### A.2 `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines)

- It sets **no environment variable**. A grep for `export` and for upper-case assignments finds none; the only environment it reads is `HOME` (`:21`, `:103`, `:432`) [CODE-VERIFIED: launch-job-identity.sh:21, :103, :432].
- Identity is file state, not variables: `$HOME/.claude/state/launch-level` (`:21`, `:111`) and one file per session at `$HOME/.claude/state/launch-level/sessions/<session id>` (`:435`). "Release is deletion of sessions/SESSION" (`:6`) [CODE-VERIFIED].
- Sub-commands (header `:2-19`): `prepare SESSION COMMAND [TOOL_USE_ID]` prints a single-use token; `run TOKEN` waits for the main bash and its ordinary descendants; `identify [PID]` prints `governed`, `ordinary` or `unknown`, never command text (`:5`); with no arguments it adapts PreToolUse Bash JSON from stdin (`:10`) [CODE-VERIFIED: launch-job-identity.sh:2-19].
- If `launch-level` does not exist the hook exits 0 and creates nothing (`:19-23`) [CODE-VERIFIED].
- `:431` "do not guess from agent_id, parent fields, cwd or environment": the hook does not derive identity from environment variables at all [CODE-VERIFIED: launch-job-identity.sh:431].

Consequence for the sweep: a read-only sweep cannot learn "governed vs person-started" from environment variables; the only read path is `identify [PID]` (a read of the session files) or a direct read of `sessions/<id>`. Whether `identify` writes anything was not traced past the header comment; treat calling it from the sweep as [UNVERIFIED] until the plan reads `:425-460`.

---

## B. Other Orca read surfaces (B-07)

Help text is CLI 1.4.245; handler lines are from the installed CLI. "Plain read" means the handler calls `client.call(...)` directly; "mutation" means it goes through `callOrchestrationMutation` (`mutation-request.js:9`), which is the path every state-changing verb uses.

| Verb | Usage (help) | Handler path | Returns | Paged | Feeds which sweep class | Tag |
|---|---|---|---|---|---|---|
| `run-list` | `[--limit <n>] [--cursor <cursor>] [--json]`, "List lightweight orchestration Runs" | plain read `orchestration.runList` (`run-handlers.js:35-48`) | Runs: `id`, `legacy`, `objective` | Yes: `limit` defaults to `ORCHESTRATION_RUN_PAGE_LIMIT` = 100 (`shared/orchestration-run-pagination.js:4`); `nextCursor` printed as "More Runs: --cursor" | Source of Run IDs for `--run <id>` on every other verb; no class by itself | [CODE-VERIFIED: run-handlers.js:35-48] |
| `run-current` | `[--from <handle>] [--json]`, "Show the Run bound to this coordinator" | plain read `orchestration.runCurrent` (`run-handlers.js:28-34`) | the bound Run or none | No | Decides `scope.source` (bound vs all) the same way `worker-list` does (`worker-list-run-scope.js:8-24`) | [CODE-VERIFIED: run-handlers.js:28-34] |
| `task-list` | `[--status <status>] [--ready] [--brief] [--run <run_id>] [--from <handle>] [--json]` | plain read `orchestration.taskList` (`task-handlers.js:32-44`) | Tasks: `id`, `status` (pending, ready, dispatched, completed, failed, blocked; `:10-17`), `display_name`/`task_title`/`spec`, `assignee_handle`, `dispatch_id`; `legacyReadOnly` | No cursor flag in help or handler; whether the runtime caps rows is [UNVERIFIED] | "Foreign ready Task" (WORKER-CONTRACT: a ready Task the coordinator did not create is reported to the person); `blocked` Tasks | [CODE-VERIFIED: task-handlers.js:10-17, :32-44] |
| `gate-list` | `[--task <task_id>] [--status <status>] [--run <run_id>] [--from <handle>] [--json]`; note "--run inspects a named Run without binding" | plain read `orchestration.gateList` (`gate-handlers.js:26-37`) | Gates: `id`, `task_id`, `status`, `question` | No cursor; cap [UNVERIFIED] | Pending decision gates (a candidate "waiting on a person" source; see 06 N-36 note) | [CODE-VERIFIED: gate-handlers.js:26-37] |
| `inbox` | `[--limit <n>] [--terminal <handle>] [--full] [--json]`, "Show messages across (or for) recipients" | plain read `orchestration.inbox` (`message-inbox-handlers.js:20-25`), not the mutation helper | messages, with a `[legacy, read-only]` tag from `formatMessageReadOnlyTag` (`:32`; `shared/orchestration-check-output.js:9-16`) | `--limit` only, no cursor | Message coverage for "waiting on a person" (`ask`) | [CODE-VERIFIED: message-inbox-handlers.js:20-25] |

**Where Run IDs come from:** `run-list` (paged, 100 per page) or `run-current` (the caller's binding). `worker-list` without `--run` uses `run-current` and falls back to all Runs when there is no binding or the call throws (`worker-list-run-scope.js:8-24`, comment `:21` "A missing caller binding or older runtime must not prevent a full inventory") [CODE-VERIFIED].

**Read-only status:** the CLI side of all five is a plain `client.call`, not the mutation helper. Whether the runtime handler for `orchestration.inbox` marks messages read is [UNVERIFIED]; the help text says nothing about read-marking for `inbox`. Until a runtime read or capture settles it, the sweep treats `inbox` as **not proven read-only** and does not call it (see 06 Q2).

---

## C. `check` handler evidence (B-24, B-22, B-17)

All from `message-check-handler.js` (95 lines) [CODE-VERIFIED: file read 2026-11-07].

| # | Fact | Lines |
|---|---|---|
| (a) | Every `check` form, `--peek` and `--all` included, goes through `callOrchestrationMutation(client, flags, 'orchestration.check', ...)`. The CLI does not distinguish a read-only check from a draining one; the runtime decides. | `:30` |
| (b) | `unread: flags.has('unread') ? true : peek ? false : undefined`, with the comment "unread:false makes hosts that ignore peek fall back to non-consuming all mode." | `:33-34` |
| (c) | Comment "Older runtimes ignore peek, making --unread --peek destructive." More than one read mode is rejected. | `:17`, `:18-20` |
| (d) | If `result.legacyCompatibility.ackMessageIds` is non-empty, the CLI makes a **second** call `orchestration.check` with `compatibilityAck` (message ids and types): an acknowledgement side effect the caller did not ask for. | `:58-71` |
| (e) | `filterLegacyPeekResult` drops rows with `read === 1`; with `--wait` and every row read it throws `peek_wait_unsupported`; it warns "this runtime returned only its newest 100 messages for --peek; older unread messages may be missing". So on an older runtime the 100-row cap keeps the **newest** 100. | `:50-52`, `:74-95`, `:82-83` |
| (f) | `--format` is a boolean (`format: true`, no value) passed to `prepareOrchestrationCheckOutput`, which only adds a local `formatted` text field built by `formatLegacyAwareCheckMessages` when legacy read-only messages are present (`shared/orchestration-check-output.js:49-59`). It is a local text switch; the `<png|jpeg>` "Screenshot image format" label at `[H:check]:28` is a help mislabel. It still rides the same `orchestration.check` mutation call as (a), so the sweep does not use it. | `:38`, `:55`; `orchestration-check-output.js:49-59` |
| (g) | `ORCA_PANE_KEY` is read to identify the caller. | `:25` |

Consequences, recorded for 06:

- `--unread` is forbidden for the sweep: (b) and (c) show it consumes, and with `--peek` it is destructive on older runtimes.
- `--peek` may be trusted only after a runtime-version or `legacyCompatibility` probe: on an older runtime (c) it is ignored, and (d) can still send a `compatibilityAck`. The probe itself is [UNVERIFIED]: no read-only verb that reports the runtime version was found in help.
- `compatibilityAck` (d) is a gap: whether a `--peek` or `--all` result can carry `legacyCompatibility.ackMessageIds`, which would make the CLI acknowledge messages on the sweep's behalf, is [UNVERIFIED].
- The `ask` handler (`question-handler.js:61-68`) also sends `orchestration.check` with `compatibilityQuestionAck` after an answer; the sweep never calls `ask`, so this only confirms the pattern.

---

## D. Pane-key join (B-09, C12)

Verified by direct file reads:

- `lc16-show-4.json` (`.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/`): `assigneeHandle` `term_1a6fde09-00c4-42f2-9bda-edbd2b50899c` (`:11`), `assigneePaneKey` `ec61f494-038b-4c5b-a2b2-13e3139342e8:2844c731-8cec-4dee-aa0b-63ff3baac732` (`:12`), terminal `handle` same as `:11` (`:162`), `tabId` `ec61f494-...` (`:169`), `leafId` `2844c731-...` (`:170`).
- `~/.local/state/ccsession/orca-tabs/ec61f494-038b-4c5b-a2b2-13e3139342e8+2844c731-8cec-4dee-aa0b-63ff3baac732` exists; its 3 lines are the Claude session id `bd2c3553-e0a2-49ef-94c0-1052a189b459`, the launch folder `/home/coder/workspaces/worktrees/IronClaude/p1-live-workflow`, and the handle `term_1a6fde09-00c4-42f2-9bda-edbd2b50899c`.

Result: `assigneePaneKey` with `:` replaced by `+` is the orca-tabs file name, and line 3 matches `assigneeHandle` [CODE-VERIFIED: lc16-show-4.json:11-12, :162, :169-170; orca-tabs file lines 1-3]. One worker, one capture; the join holds for this sample. It requires the session to have been launched through ccsession (the file is written by ccsession, `scope-02` :160).

What stays open (owner decision, WC-14): whether the sweep reports person-started sessions at all. The join gives a read-only route (orca-tabs file plus `topics/*.txt`) without calling `ccsession --list`, which can write.

---

## Summary

- B-04: `pragmatic.md:22` says "No exceptions" and the file has no exception mechanism; `launch-job-identity.sh` sets no environment variables, it keeps identity in `~/.claude/state/launch-level/sessions/<id>` files.
- B-07: `run-list`, `run-current`, `task-list`, `gate-list` and `inbox` are plain reads on the CLI side; only `run-list` is paged (100, `--cursor`); Run IDs come from `run-list` or `run-current`; `inbox` read-marking is UNVERIFIED, so it is not used.
- B-24: every `check` is sent as a mutation; `--unread` consumes; `--peek` is ignored by older runtimes; a legacy result can trigger an automatic `compatibilityAck`; an older runtime keeps the newest 100 rows.
- B-09: the pane-key join is verified for the lc16 worker; reporting person-started sessions remains an owner decision.
