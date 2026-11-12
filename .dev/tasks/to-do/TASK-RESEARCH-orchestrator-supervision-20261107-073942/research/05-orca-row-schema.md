# Research: Orca worker-list row schema (G-A)

**Investigation type:** Integration Mapper
**Scope:** `orca-ide orchestration worker-list --help`, `orca-ide orchestration worker-show --help` (help text only); `.dev/orca-command-refactor/inventory/orca-capabilities.md` lines 9-20 and 110-130; `orca-ide skills get orchestration` and `orca-ide skills get orca-cli` (read-only guide text); captures `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc16-show-4.json`, `lc17-show-1.json`, `lc01-show-1.json`, `lc01-step7.txt`
**Status:** Complete
**Date:** 2026-11-07

---

Citation convention (same as `orca-capabilities.md:8-21`): command output is cited as numbered output lines, produced by piping the command through `cat -n`. `[H:worker-list]` = `orca-ide orchestration worker-list --help`; `[H:worker-show]` = `orca-ide orchestration worker-show --help`; `[G]` = `orca-ide skills get orchestration`; `[G:recovery]` = `orca-ide skills get orchestration --reference recovery-and-cleanup`; `[CLI]` = `orca-ide skills get orca-cli`. Captures are cited as `file:line`. All output was read on 2026-11-07.

## Source 1: `worker-list --help` and `worker-show --help` (current CLI)

**`[H:worker-list]`** (22 output lines):

- Line 3, the full usage: `orca orchestration worker-list [--run <run_id>] [--terminal-state <active|reclaimable|retained|release_pending|release_unknown|released>] [--include-remote] [--cursor <cursor>] [--limit <1-100>] [--json]`. [CODE-VERIFIED]
- Line 5, purpose: "List supervised worker terminal resource accounting". The help itself describes the row as terminal accounting; it does not list the row fields or mention `projection`, `liveness`, `attention` or `agentWait`. [CODE-VERIFIED]
- Lines 13-16, flags: `--terminal-state <state>` filter; `--include-remote` "Include connected-server worker observations"; `--cursor <cursor>` "Opaque page cursor copied from page.nextCursor"; `--limit <n>` "Maximum number of rows to return" (range `1-100` from line 3). [CODE-VERIFIED]
- Line 19: "Terminal state is process accounting and is reported separately from Task status; a completed Task can still own a live terminal." [CODE-VERIFIED]
- Line 20: "Context-only Dispatches created by orchestration dispatch are included as unsupervised with terminal state retained." [CODE-VERIFIED]
- Line 21: "Returns at most 100 local rows, newest first, by default; --include-remote adds connected-server observations when the host supports fleet listing. Continue with the opaque page.nextCursor value unchanged." So the list **pages**: at most 100 rows per call, and a `page.nextCursor` continues it. [CODE-VERIFIED]
- Line 22: "Without --run the list is scoped to the Run bound to the calling terminal, and to every Run when there is no binding; the receipt reports which in scope.source (flag, bound, or all)." [CODE-VERIFIED] This line is not quoted in `orca-capabilities.md` (see Stale Documentation).

**`[H:worker-show]`** (16 output lines):

- Line 3: `orca orchestration worker-show --dispatch <dispatch_id> [--json]`. One Dispatch per call; no batch or multi-ID form. [CODE-VERIFIED]
- Line 5: "Inspect one supervised worker Dispatch". [CODE-VERIFIED]
- Line 15: "A Dispatch created by orchestration dispatch is shown as unsupervised and reports the exact adopted terminal when its identity is still provable." [CODE-VERIFIED]
- Line 16: "observation.agentWait names a worker parked on a prompt only a human can answer, with the evidence that proved it (hook, prompt-text, or title). Null means Orca looked and found no wait. An absent field means it never looked — an older host, an unverifiable worker identity, an unreadable pane, or an agent probe that did not answer in time — and never means the worker is not waiting. A waiting worker is healthy, not failed." [CODE-VERIFIED] This defines three states for `agentWait`: object (waiting, with evidence kind `hook`, `prompt-text` or `title`), `null` (looked, no wait), absent (never looked; not evidence of anything).

Key Takeaways:

- worker-list pages at 100 rows max (`--limit 1-100`, `page.nextCursor`), newest first, and is scoped to the bound Run by default.
- worker-show takes exactly one `--dispatch`; classifying N workers through worker-show costs N calls.
- Help documents `agentWait` only on worker-show (`observation.agentWait`); worker-list help names no row fields.
- `agentWait` has three states, and "absent" must never be read as "not waiting" (matches WC-10).

## Source 2: `.dev/orca-command-refactor/inventory/orca-capabilities.md` (lines 9-20, 110-130)

- Version drift: the inventory was captured with `orca-ide` `1.4.237-aidev02.0e4491a95e92` on 2026-11-02 (`orca-capabilities.md:8`). `orca-ide --version` now prints `1.4.245-aidev02.780594c521aa`. Its line-number citations of `[G]`/`[H:*]` output are for the older version, and line 8 itself warns "another CLI version may print different lines". **[STALE DOC]** (version only; see Source 3 for which cited lines moved).
- Source-key table `orca-capabilities.md:10-21`: guide text comes from `orca-ide skills get orchestration` and its `--reference <page>` pages; help from `orca-ide orchestration <verb> --help`. Used as the citation scheme here.
- Liveness, `orca-capabilities.md:122`: "Preserve the verdicts `live` / `unverifiable` / `exited`; contact loss is not process death" (quoting `[G]` 58-60). [UNVERIFIED at inventory level; re-checked against the current guide in Source 3.]
- Two layers, `orca-capabilities.md:123`: "`worker-list`'s `projection.liveness` is the fleet verdict for the agent; `worker-show`'s `observation.status` is PTY liveness only." This is the inventory's only statement that a worker-list row carries a `projection` object; it is guide text. Checked against captures in Source 4. [UNVERIFIED: guide text via orca-capabilities.md:123]
- Outranking, `orca-capabilities.md:124`: for `unverifiable` reasons `missing_status`, `host_unavailable`, `capability_unsupported`, a host-sourced worker-show verdict outranks the row. [UNVERIFIED: guide text via orca-capabilities.md:124]
- `unverifiable` reasons, `orca-capabilities.md:125`: `missing_status`, `stale_status`, `restored_unconfirmed`, or a remote worker with no connection; "a null `agentWait` or an unchanged `worker-read` tail is that same absence seen again. Absence never authorizes stop, abandon, retry, or release". [UNVERIFIED: guide text via orca-capabilities.md:125]
- Stall proof, `orca-capabilities.md:126`: only `exited` liveness, the worker's own observation of process exit, or a transcript whose final agent turn sent no `worker_done`. [UNVERIFIED: guide text via orca-capabilities.md:126] "Final" is not defined by the guide; this research counts the transcript proof only when independent evidence proves the turn final (`research-notes.md` Section C rule 2, B-05).
- Per-row attention, `orca-capabilities.md:127`: worker-list rows expose `projection.attention` categories, `projection.attention.requiresAction` and literal `projection.nextAction` argv; "A `none` `nextAction` has no argv to run: read `liveness.reason` and keep waiting". Paging quote matches `[H:worker-list]` line 21 today. [CODE-VERIFIED for paging only]
- Remote, `orca-capabilities.md:128`: a `--on <environment>` worker reads `unverifiable` until listed with `--include-remote`. [UNVERIFIED: guide text via orca-capabilities.md:128]
- agentWait, `orca-capabilities.md:129`: quotes `[H:worker-show]` line 16; the current help prints that text at the same line 16 (the inventory elides the middle with "..."). [CODE-VERIFIED]
- Heartbeat age, `orca-capabilities.md:130`: UNVERIFIED whether Orca uses heartbeat age in the liveness verdict.
- `orca-capabilities.md:113` cites `[H:worker-list]` line 19 for the terminal-state note; current line 19 still carries that text. [CODE-VERIFIED]

Key Takeaways:

- The inventory's row schema (`projection.liveness`, `projection.attention`, `projection.nextAction`) is guide-derived, not capture-derived; it needs the captures to confirm.
- Paging and agentWait help text still match; the guide line numbers belong to an older CLI version.
- The inventory does not say whether a worker-list row carries `agentWait`; that is the crux of question (1).

## Source 3: `orca-ide skills get orchestration` (compact guide, current CLI, 215 output lines)

The compact guide is now 215 lines (the inventory recorded 202, `orca-capabilities.md:12`), so every `[G]` line number in the inventory has shifted. **[STALE DOC]**

- `[G]` lines 59-61: "Preserve the verdicts `live` / `unverifiable` / `exited`; contact loss is not process death." (inventory cites 58-60.) [UNVERIFIED as CLI behavior; guide text]
- `[G]` lines 62-64: "Liveness is layered: `worker-list`'s `projection.liveness` is the fleet verdict for the agent; `worker-show`'s `observation.status` is PTY liveness only. A live terminal can still hold a dead or stuck agent." (inventory cites 61-63.) The guide places `projection` on the worker-list row and `observation` on worker-show. [UNVERIFIED here; see captures in Source 4]
- `[G]` lines 66-67: "Clients and remote servers update independently. Treat unknown optional fields as absent." So a sweep must tolerate missing row fields and must not infer anything from their absence. [UNVERIFIED; guide text]
- `[G]` lines 149-152: after three empty waits, run "`ORCA orchestration worker-list --include-remote --json` (defaults to the bound Run; `--run <run_id>` overrides; the receipt's `scope` names which), acting on each row's `projection.attention` categories, `projection.attention.requiresAction`, and literal `projection.nextAction` argv." The scope clause matches `[H:worker-list]` line 22. [CODE-VERIFIED for scope; row fields UNVERIFIED here]
- `[G]` line 153: "Rows come newest first and page at 100: while `page.hasMore`, follow `page.nextCursor` with `--cursor <value>`." Adds a `page.hasMore` boolean not named in the help. [paging CODE-VERIFIED by `[H:worker-list]` 21; `page.hasMore` UNVERIFIED]
- `[G]` lines 154-155: "A `none` `nextAction` has no argv to run: read `liveness.reason` and keep waiting with `check --wait`. Absence never earns an argv; settlement and pending work still do." [UNVERIFIED]
- `[G]` lines 156-161: positive proof of stop is "`exited` liveness, the worker's own observation of process exit, or a transcript whose final agent turn sent no `worker_done`" ... "`unverifiable` is absence, including when `worker-show` reports `agentWait` null. Absence never authorizes stop, abandon, retry, or release; keep waiting or inspect." The guide again ties `agentWait` to worker-show, not to the list row. [UNVERIFIED]
- `[G]` lines 190-192: `worker-list --run <run_id> --terminal-state reclaimable --json` enumerates terminals owing a release decision. [CODE-VERIFIED: flags exist in `[H:worker-list]` line 3]
- Side finding, out of this topic's scope: `[G]` lines 130-131 now say "A dispatched worker starts its own helpers with `worker-start --spec` on the Run it works for, without `run-create`; the helpers report to that worker." `orca-capabilities.md:97-102` says workers cannot start workers at the default depth 1. The current guide text alone does not settle which is true for this machine's setting. **[STALE DOC]** candidate; flagged in Gaps. Fix cycle 1 (B-06): whatever Orca allows, the guide text also contradicts this project's contract, WC-8 and WC-13 (`WORKER-CONTRACT.md:39`, `:61`: a worker session never calls `worker-start`, at any depth setting). The contract governs: the sweep reports a worker-show row with a non-null `parent` (`lc16-show-4.json:115`, null there) as a WC-13 violation for review (`research-notes.md` C15).

Key Takeaways:

- Guide: liveness verdict lives on the list row (`projection.liveness`, with `liveness.reason`); `agentWait` is described only through worker-show.
- Paging: 100 rows per page, `page.hasMore` plus `page.nextCursor`.
- "Unknown optional fields are absent" and "absence never authorizes action" are the guide's rules a sweep must copy.

## Source 3b: `orca-ide skills get orchestration --reference recovery-and-cleanup` (current CLI)

Read because the compact guide defers liveness reasons to it (`[G]` line 210). Lines 1-80 read.

- `[G:recovery]` lines 6-14, proven-state table: `unverifiable` liveness = "Keep waiting or inspect; never stop, abandon, retry, or release"; "Proven `exited` agent" = "Enumerate with `worker-list`; follow its `nextAction`"; "Remote contact lost" = "Preserve `unverifiable`; do not stop or retry from absence alone". [UNVERIFIED; guide]
- `[G:recovery]` lines 25-29: "`worker-list` is the enumerating command and the authority on agent liveness: each row carries `projection.liveness`, `projection.attention.categories`, `projection.attention.requiresAction`, and a literal `projection.nextAction` argv to run. Always scope it with `--run <run_id>`; an unscoped list reports every Dispatch this runtime has ever recorded and buries the live ones." This is the guide's explicit list of the row's `projection` fields. It does **not** list `agentWait`. [UNVERIFIED by guide; partly confirmed by captures, Source 4]
- `[G:recovery]` lines 30-31: "`worker-show`'s `observation.status` is PTY liveness only, so a `live` terminal whose agent died at a trust prompt still reads `live` there." [UNVERIFIED]
- `[G:recovery]` lines 33-45: fleet verdict decides, except `unverifiable` with reason `missing_status` (no status row held), `host_unavailable` (could not ask the host; the only contact-loss reason) or `capability_unsupported` (peer lacks the fleet-snapshot capability); then a host-sourced worker-show verdict outranks the row. "This never promotes absence. `unverifiable` from either command still authorizes nothing — only a positive `live` or `exited` verdict does." [UNVERIFIED]
- `[G:recovery]` lines 47-50: remote (`--on`) workers read `unverifiable` until `--include-remote`; "past 100 the response pages, so follow `page.nextCursor` with `--cursor <value>` until `page.hasMore` is false." [paging CODE-VERIFIED by `[H:worker-list]` 21; `hasMore` UNVERIFIED]
- `[G:recovery]` lines 58-63: "`unverifiable` is always absence — `missing_status`, `stale_status`, `restored_unconfirmed`, or a remote worker with no connection — and a null `agentWait` or an unchanged `worker-read` tail is that same absence seen again." "A `nextAction` that names an inspecting command is asking for evidence, not for cleanup." [UNVERIFIED]

Documented liveness values (question 2), from the guide:

| Value | Meaning (guide) | Authorizes |
|---|---|---|
| `live` | Positive verdict that the agent is running (fleet verdict on the list row) | Keep waiting; nothing destructive |
| `unverifiable` | Absence of proof. Reasons named: `missing_status`, `stale_status`, `restored_unconfirmed`, `host_unavailable`, `capability_unsupported`, remote with no connection | Nothing (`[G:recovery]` 44-45, 61) |
| `exited` | Positive proof the agent stopped | Stop/abandon choice, following `nextAction` (`[G:recovery]` 14, 54-56) |

Key Takeaways:

- The guide's row schema is `projection.{liveness, attention.categories, attention.requiresAction, nextAction}`; `agentWait` is not in it.
- Six `unverifiable` reasons are named across `[G:recovery]` 34-38 and 58-59; three of them (`missing_status`, `host_unavailable`, `capability_unsupported`) make a worker-show verdict outrank the row.
- A sweep that sees `unverifiable` must report "could not determine", never "stalled".

## Source 3c: `orca-ide skills get orca-cli` (current CLI, 289 output lines)

- Searched the full output for `worker-list`, `worker-show`, `liveness`, `agentWait`, `projection`, `unverifiable`, `nextCursor`, `hasMore`, `attention`. No line mentions `worker-list`, `worker-show`, `agentWait` or `projection`.
- `[CLI]` line 161 (`reference find` output): "Check `liveness` (`live`, `unverifiable`, `exited`) and choose the intended agent". The same three-value vocabulary is used outside orchestration. [UNVERIFIED; guide]
- `[CLI]` line 223: a bulk `terminal close` that cannot confirm every PTY stopped is "`unverifiable`; do not report the processes as exited". Same absence rule. [UNVERIFIED]

Key Takeaways:

- orca-cli adds nothing to the worker-list row schema; it only confirms the three liveness values are a shared Orca vocabulary.

## Source 4: existing captures (`.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/`)

All four were captured on 2026-11-05 against runtime `f03c04aa-bfec-42ed-aad0-6d0e9c1cc7bc` (for example `lc16-show-4.json:210`), so on a CLI version between the inventory's 1.4.237 and today's 1.4.245; the exact version is not recorded in the files.

### `lc16-show-4.json` (worker-show, a live worker still working)

Top-level `result` keys: `dispatch` (lines 5-30), `worker` (31-108), `projection` (109-160), `terminal` (161-181), `observation` (182-186), `terminalResource` (187-207). [CODE-VERIFIED]

The `projection` object worker-show returns (lines 109-160) has these fields: `id`, `dispatchId`, `taskId`, `runId`, `role` ("worker"), `parent` (null), `provider.{id, model}`, `host.{kind, id}`, `workspace.{id, kind}`, `stage.{worker, dispatch, detail, activity}` (lines 128-133: "ready", "dispatched", "input_accepted", "working"), `outcome` (line 134: "in_progress"), `liveness.{verdict, observedAt, source}` (lines 135-139: "live", epoch ms, "agent_status"), `evidence.{durable, liveStatus, lastObservedAt}` (lines 140-144: true, "fresh"), `resource.{state, id, ownerDispatchId, releaseState, terminalState}` (lines 145-151: "user_owned", "retained", "retained"), `nextAction.{kind, argv}` (lines 152-155: "none", `[]`), `attention.{categories, requiresAction}` (lines 156-159: `[]`, false). [CODE-VERIFIED]

- **No `agentWait` inside `projection`.** `agentWait` appears twice, both outside it: `terminal.agentWait` (line 180) and `observation.agentWait` (line 185), both `null`. [CODE-VERIFIED] So the guide's statement that `agentWait` is a worker-show `observation` field (`[H:worker-show]` 16) is confirmed, and a list row that carries only `projection` would not include it.
- **No `liveness.reason` here.** The guide tells the reader to "read `liveness.reason`" (`[G]` 154); this `live` verdict has only `verdict`, `observedAt`, `source` (lines 135-139). The reason field presumably appears only for `unverifiable`; no capture shows it. [UNVERIFIED]
- `dispatch.lastHeartbeatAt` (line 29) and `terminal.lastOutputAt` (line 174) and `terminal.preview` (line 175) are worker-show-only fields outside `projection`.

### `lc17-show-1.json` (worker-show, worker settled as failed, terminal not yet released)

- `projection.stage` lines 128-133: `worker` "failed", `dispatch` "failed", `detail` "settled", **`activity` "working"**; `outcome` line 134 "failed"; `liveness.verdict` line 136 "live". [CODE-VERIFIED]
- `projection.resource.terminalState` line 150 "reclaimable"; `nextAction` lines 152-160: `kind` "release", argv `["orchestration","worker-release","--dispatch","ctx_5fac5090b848"]`; `attention` lines 161-166: categories `["failure"]`, `requiresAction` true. [CODE-VERIFIED] The literal argv omits the executable, matching `[G]` "literal `projection.nextAction` argv".
- `terminal.preview` line 182 shows an idle prompt (`❯`) while `stage.activity` still says "working". **[CODE-CONTRADICTED]** for any reading of `stage.activity` as a live "working vs idle" signal: after settlement it stayed "working". A sweep must classify "finished" from `outcome`/`stage.dispatch`, not from `activity`.
- `terminal.agentWait` line 187 and `observation.agentWait` line 192: both `null`; `observation.status` line 190 "live". [CODE-VERIFIED]

### `lc01-show-1.json` (worker-show, worker settled as succeeded, terminal not yet released)

- `projection.stage` lines 128-133: "succeeded", "completed", "settled", `activity` "working"; `outcome` line 134 "succeeded"; `liveness.verdict` line 136 "live"; `resource.terminalState` line 150 "reclaimable"; `nextAction.kind` line 153 "release" with the worker-release argv (154-159); `attention` lines 161-166: categories `["root_completion"]`, `requiresAction` false. [CODE-VERIFIED] Same `activity` "working" after settlement. **[CODE-CONTRADICTED]** as above.
- `agentWait` null at lines 187 and 192. [CODE-VERIFIED]

### `lc01-step7.txt` (worker-release, then worker-list reclaimable)

- Lines 23-47: the only worker-list capture. `result.workers` is `[]` (line 28), so **no populated row was captured**. [CODE-VERIFIED]
- The list envelope is: `workers` (array), `counts` (line 29-31: `{"released": 1}`, counts per terminal state), `page.{limit, total, hasMore, nextCursor}` (lines 32-37: 100, 0, false, null), `scope.{run, source}` (lines 38-41: "run_92b0ef27e086", "flag"). [CODE-VERIFIED] This confirms `page.hasMore` exists (guide `[G]` 153) and `scope.source` (`[H:worker-list]` 22).
- `page.limit` 100 (line 33) matches the help's default cap. `counts` is a free aggregate: one call reports how many rows sit in each terminal state even when the filter returns none. [CODE-VERIFIED for `released`; other keys UNVERIFIED]

Key Takeaways:

- worker-show returns a full `projection` object (16 top-level fields) plus `observation`, `terminal`, `dispatch`, `worker`, `terminalResource`.
- `agentWait` lives in `observation` and `terminal`, never in `projection`; all three captures show `null`, none shows a non-null wait.
- No capture shows a populated worker-list row, so whether a row carries the whole `projection` (or anything beyond it) is not proven by capture.
- `stage.activity` reads "working" after settlement; do not use it to tell working from finished.
- The list envelope (`workers`, `counts`, `page`, `scope`) is proven.

## Answers to the five questions

**(1) Does a worker-list row carry the worker-show `projection` object, or a subset?**
The guide says each row "carries `projection.liveness`, `projection.attention.categories`, `projection.attention.requiresAction`, and a literal `projection.nextAction` argv" (`[G:recovery]` 25-28; `[G]` 62-63, 152) [UNVERIFIED]. The worker-show captures prove the full `projection` object has 16 fields (`lc16-show-4.json:109-160`) [CODE-VERIFIED]. No capture shows a populated list row (`lc01-step7.txt:28` is `[]`), so whether the row carries the whole object or only the four named fields is not proven. Either way, `agentWait` is **not** part of `projection`: it sits in worker-show's `observation` and `terminal` objects (`lc16-show-4.json:180,185`) [CODE-VERIFIED], and the guide mentions it only for worker-show (`[G]` 160; `[H:worker-show]` 16). Practical answer (fix cycle 1, B-25, B-08): what a list row carries is [UNVERIFIED], because no populated row was captured. It is therefore also UNVERIFIED that the row lacks `agentWait`; the captures only show that `agentWait` is not inside `projection`. Conservative default for the sweep: rely on nothing in a list row beyond the envelope (`workers`, `counts`, `page`, `scope`) and the Dispatch id, and call `worker-show` once per row to classify it. A cheaper list-only classification becomes possible only after a populated-row capture proves which fields the row carries.

**(2) Documented liveness values.** `live` (positive: agent running), `unverifiable` (absence of proof; reasons `missing_status`, `stale_status`, `restored_unconfirmed`, `host_unavailable`, `capability_unsupported`, or remote with no connection), `exited` (positive proof the agent stopped) (`[G]` 59-61; `[G:recovery]` 6-14, 33-45, 58-63; `[CLI]` 161) [UNVERIFIED as behavior; guide]. Captures prove only `live` with `source` "agent_status" (`lc16-show-4.json:135-139`, `lc17-show-1.json:135-139`, `lc01-show-1.json:135-139`) [CODE-VERIFIED]. Only `exited` (or a process-exit observation, or a transcript turn proved final with no `worker_done`) proves a stall (`[G]` 156-158) [UNVERIFIED: guide text]; `unverifiable` maps to "could not determine". A latest transcript turn is not "final" by being latest: a busy worker's latest turn also lacks `worker_done`, and a WC-12 fenced worker stops without one by design (`WORKER-CONTRACT.md:60`). See `research-notes.md` Section C rules 2-3 (B-05).

**(3) Shape of a non-null `agentWait`.** Not captured. The help says it "names a worker parked on a prompt only a human can answer, with the evidence that proved it (hook, prompt-text, or title)" (`[H:worker-show]` 16) [CODE-VERIFIED as help text], so it is an object carrying at least an evidence kind from {`hook`, `prompt-text`, `title`}; its field names are unknown. Three states are documented: object = waiting (healthy), `null` = looked and found no wait, absent = never looked (not evidence) (`[H:worker-show]` 16). The guide adds that `null` together with `unverifiable` is still absence (`[G]` 159-160; `[G:recovery]` 59-60).

**(4) Does worker-list page or truncate?** It pages. At most 100 rows per call, newest first (`[H:worker-list]` 21); `--limit 1-100`, `--cursor <page.nextCursor>` (`[H:worker-list]` 3, 15-16); envelope `page.{limit, total, hasMore, nextCursor}` (`lc01-step7.txt:32-37`) [CODE-VERIFIED]. Other flags: `--run`, `--terminal-state <active|reclaimable|retained|release_pending|release_unknown|released>`, `--include-remote`, `--json`, `--pairing-code`, `--environment` (`[H:worker-list]` 3, 9-14). Default scope is the bound Run, or every Run when unbound, reported in `scope.source` (`flag`/`bound`/`all`) (`[H:worker-list]` 22; `lc01-step7.txt:38-41`) [CODE-VERIFIED]. The guide warns an unscoped list "reports every Dispatch this runtime has ever recorded" (`[G:recovery]` 28-29), so a sweep should pass `--run`. Remote rows need `--include-remote` or they read `unverifiable` (`[G:recovery]` 47-49).

**(5) Cost of one call per worker.** worker-show takes exactly one `--dispatch` (`[H:worker-show]` 3) [CODE-VERIFIED], so classifying N workers needs ceil(N/100) worker-list calls plus N worker-show calls whenever the "waiting on a person" state is required (because `agentWait` is only on worker-show). A cheaper shape: one worker-list page per 100 workers, then worker-show only for rows whose list verdict leaves the state open (for example `live` and not settled, or `unverifiable` with `missing_status`/`host_unavailable`/`capability_unsupported`, where worker-show outranks the row, `[G:recovery]` 33-42). Settled rows (`outcome` succeeded/failed) need no worker-show call. This narrowing depends on the row carrying `outcome`/`stage`, which is UNVERIFIED (question 1). **Until a populated-row capture exists, the sweep plans for the worst case: ceil(N/100) worker-list calls plus N worker-show calls** (B-08). Even a settled row then still needs the return contract read (`WORKER-CONTRACT.md:122-129`) before it is "finished".

Orca-side signals per class (fix cycle 1, B-01, B-28). The class names, their precedence and the full rules are in `research-notes.md` Section C, which supersedes the table this file had here (C14). This table gives only the **Orca half** of each class: an Orca signal never makes a row "finished" by itself, because "finished" also needs the return contract read (`WORKER-CONTRACT.md:122-129`), and `worker_status: blocked` (Orca outcome `failed`, WC-5 `:58`) is waiting on a person, never finished.

| Section C class (precedence order) | Orca-side signal | Source |
|---|---|---|
| 1. waiting on a person (contract) | none from Orca: `return-contract.yaml` `worker_status: blocked` is read first | contract file |
| 2. stalled (proved) | `liveness.verdict` exited, or a transcript turn proved final with no `worker_done` (`[G]` 156-158), **and no `consumer_fenced` evidence** in the transcript or `check` result (a fenced worker that exited shows the same Orca signal; Section C rule 2, NB-1) | worker-show (row UNVERIFIED) + worker-read |
| 3. fenced | none from Orca alone; the worker's `check` returned `consumer_fenced` (WC-12). Takes the row even when liveness is `exited` with no `worker_done` | transcript |
| 4. waiting on a person (a) explicit question | non-null `observation.agentWait`; a pending `ask` has no read path (G-B) | worker-show only |
| 4. waiting on a person (b) frozen/blocked by policy | frozen plan, Ruling halt, or a ready Task this coordinator did not create | ledger, contract, `task-list --ready` |
| 5. working | `liveness.verdict` live, outcome in_progress, `agentWait` null | worker-show |
| 6. finished (Orca half only) | `projection.outcome` succeeded/failed (`stage.dispatch` completed/failed) | worker-show (row UNVERIFIED) |
| 7. could not determine | `unverifiable`; `agentWait` absent **on an unsettled row**; a latest turn not proved final; a missing contract on a non-guard failure | worker-show |

`resource.terminalState` is not a class input: `lc16-show-4.json:145-151` shows a working worker with `terminalState` retained. The old row "idle = settled and terminal retained/released" is withdrawn; such a row is "finished, terminal kept" if its contract is read, and the terminal part belongs to the separate safe-to-close dimension (Section C). "Idle" is used only for person-started sessions.

Do not use `projection.stage.activity`: it stays "working" after settlement (`lc17-show-1.json:132`, `lc01-show-1.json:132`).

## Gaps and Questions

1. **No populated worker-list row capture.** Whether a row carries the full 16-field `projection`, only the four guide-named fields, or extra fields (for example `observation` or `agentWait`) is unproven. Needs one `orca-ide orchestration worker-list --run <id> --json` capture with a live worker (a read-only call, but not allowed in this task). [UNVERIFIED] Consequence until captured (B-08): the row shape is treated as unknown, the sweep falls back to one `worker-show` per row, and the worst-case cost is ceil(N/100) list calls plus N show calls.
2. **Non-null `agentWait` shape** unknown beyond "evidence kind hook / prompt-text / title" (`[H:worker-show]` 16). [UNVERIFIED]
3. **`liveness.reason`** is named by the guide (`[G]` 154) but absent from every captured `live` verdict; its presence for `unverifiable`/`exited` is unverified. [UNVERIFIED]
4. **`unverifiable` and `exited` verdicts** were never captured; their meanings and the six reason codes are guide text only (`[G:recovery]` 34-38, 58-59). [UNVERIFIED]
5. **`page.hasMore` semantics past 100** proven only for an empty page (`lc01-step7.txt:35`); real multi-page behavior unverified. [UNVERIFIED]
6. **`counts` keys** other than `released` (`lc01-step7.txt:30`) unverified. [UNVERIFIED]
7. **`stage.activity` "working" after settlement** (`lc17-show-1.json:132`, `lc01-show-1.json:132`) contradicts any reading of activity as a working/idle signal; whether it ever changes (for example to "waiting") is unknown. [CODE-CONTRADICTED]
8. **Nested workers:** current `[G]` 130-131 says a dispatched worker starts helpers with `worker-start --spec`; `orca-capabilities.md:97-102` says depth 1 forbids it. Which is true for Orca is [UNVERIFIED]. For the sweep it does not matter: the guide text contradicts WC-8/WC-13 (`WORKER-CONTRACT.md:39`, `:61`), which govern this project's workers, so a non-null worker-show `parent` (`lc16-show-4.json:115`) is reported as a WC-13 violation for review (B-06; `research-notes.md` C15).
10. **Other read surfaces** (B-07): `run-list`, `run-current`, `task-list`, `gate-list` and `inbox` are covered in `07-gate-gap-fill.md` B: all plain reads on the CLI side, only `run-list` paged (100, `--cursor`); Run IDs come from `run-list` or `run-current`; `task-list --ready` feeds the "foreign ready Task" case; `inbox` read-marking is UNVERIFIED so it is not used.
9. **CLI version of the captures** is not recorded in the files; they predate 1.4.245. [UNVERIFIED]

## Stale Documentation Found

- **[STALE DOC]** `orca-capabilities.md:8,12`: CLI version 1.4.237 and a 202-line compact guide; today the CLI is 1.4.245 and the guide is 215 lines, so every `[G]` line number in the inventory is off (for example liveness layering is `[G]` 62-64 now, cited as 61-63; the three-empty-waits paragraph is 149-155, cited as 136-142).
- **[STALE DOC]** `orca-capabilities.md:127` quotes the paging rule without `page.hasMore`; the current guide (`[G]` 153, `[G:recovery]` 49-50) and the capture (`lc01-step7.txt:35`) both have it.
- **[STALE DOC]** The inventory does not record `[H:worker-list]` line 22 (default scope = bound Run, `scope.source`), which the current help and the capture (`lc01-step7.txt:38-41`) show.
- **[STALE DOC]** candidate: `orca-capabilities.md:97-102` (workers cannot start workers) versus current `[G]` 130-131 (a dispatched worker starts its own helpers). Which matches Orca is not resolved here; the guide text in any case contradicts WC-8/WC-13, which the sweep enforces by reporting a non-null `parent` as a WC-13 violation for review (B-06).

## Summary

worker-list pages at 100 rows (`--limit`, `--cursor`, `page.hasMore`/`page.nextCursor`), is scoped to the bound Run by default, and per the guide each row carries `projection.liveness`, `projection.attention` and `projection.nextAction`; no capture shows a populated row, so whether it carries the full 16-field `projection` that worker-show returns is unproven. The documented liveness values are `live`, `unverifiable` (always absence, with six named reasons) and `exited` (positive stop proof); only `live` has been captured. `agentWait` is not part of `projection`: it lives in worker-show's `observation` and `terminal` objects, is null in every capture, and per the help is an object naming its evidence (hook, prompt-text or title) when set, `null` when Orca looked and found nothing, and absent when Orca never looked. Whether a list row carries `agentWait` (or anything beyond the envelope) is UNVERIFIED, so the conservative default is one worker-show call per row, plus ceil(N/100) list calls (B-25, B-08). Orca's `outcome`, never `stage.activity` (which stays "working" after settlement) and never `terminalState`, gives only the Orca half of "finished"; the class also needs the return contract read, and the single class mapping with precedence is `research-notes.md` Section C (fix cycle 1).
