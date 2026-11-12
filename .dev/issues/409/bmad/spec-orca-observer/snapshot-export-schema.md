# Snapshot export schema (PROPOSED, not an Orca contract)

Recorded owner decision 2: R1 writes a versioned, additive-only JSON snapshot from `export(view)`, with a schema test, for a later read-only Go screen in TUIBBS. This is the observer's own contract; Orca keeps authority over its source fields. Source: tuibbs-review/architecture-options.md (option (a), chosen).

**Evidence label.** Source key names were checked read-only against live `orca orchestration worker-list --json` on Orca 1.4.245 (2026-11-08), as reported in the source. The schema built on them is PROPOSED.

## Rules

- **Additive-only:** new optional fields may appear; no field is removed, renamed or retyped without a new major `schemaVersion`.
- A value the source did not give is the string `UNKNOWN`, never a guess, an empty string, 0 or `null`.
- No message bodies, prompts, file contents or credentials in R1. Every string has passed the adapter sanitizer (`adapter-contract.md`).
- One-way by construction: the snapshot carries no write-back path (`write-back-future-stage.md`).
- A licence opinion is required before any Go (AGPL) screen reads the snapshot (summary.md decision 4, still open per owner-decisions-20261108.md item 5).
- The schema lives in one schema file beside the export function, pinned by one schema test (`acceptance-tests.md`).
- **Contents:** the snapshot serializes every collected row, including historical rows hidden on screen, regardless of the `/` filter, the `h` toggle or the selection.
- **Write rule (PROPOSED):** the path is set by a PROPOSED `--snapshot PATH` option whose default is the per-user state directory `~/.local/state/superclaude/observe/` (CD-6). The file is created with owner-only permissions (0600) and replaced atomically each live cycle, including a FAILED cycle (`source.status` `ERROR`, with the last good rows): the observer writes a temporary file in the same directory, then renames it over the target, so a reader never sees a partial file. The destination remains open owner question UX-OQ-4.

## Types (PROPOSED)

- Dotted names below denote nesting: `source.namespace` is the key `namespace` inside the object `source`. No key contains a dot.
- **Req:** `required` keys are always present; `optional` keys may be absent, and an absent optional key means "not applicable", never a value. A required key the source did not give carries `"UNKNOWN"`.
- **Type** gives the full union. `"UNKNOWN"` in a union is the literal sentinel string. The types are PROPOSED; source value types are UNVERIFIED beyond the key names until the golden samples are recorded. The schema test checks every key against its Req and its union.

## Envelope (one per cycle)

| Field | Type | Req | Meaning |
|---|---|---|---|
| `schemaVersion` | int | required | `1` for release 1. Consumers reject an unknown major. |
| `producer.name`, `producer.version` | string | required | Producer name and version (the observer package version). |
| `cycle` | int | required | Collector's monotonic cycle number. |
| `generatedAt` | string (UTC, ISO 8601) | required | When the snapshot was written. |
| `source.namespace` | string | required | Which Orca the rows came from; part of row identity. Observer-derived, not an Orca field (`adapter-contract.md`). |
| `source.status` | `"OK" \| "STALE" \| "ERROR" \| "UNKNOWN"` | required | `STALE` means older than 45 s. |
| `source.observedAt` | string (UTC, ISO 8601) \| `"UNKNOWN"` | required | Time of the last successful read; `"UNKNOWN"` before the first one. |
| `source.error` | string | optional, present only when `source.status` is `ERROR` | Short error code; no raw stderr. |
| `page.hasMore` | bool \| `"UNKNOWN"` | required | From `result.page`. |
| `page.total` | int \| `"UNKNOWN"` | required | From `result.page`; optional upstream, so it may be `"UNKNOWN"`. |
| `page.limit` | int \| `"UNKNOWN"` | required | From `result.page`. |
| `scope` | object (as given, sanitized) \| `"UNKNOWN"` | required | From `result.scope`, optional upstream. |
| `counts` | object (string to int, as given) \| `"UNKNOWN"` | required | From `result.counts`, passed through as a map of state to number (never summed). |
| `collection.state` | `"COMPLETE" \| "PARTIAL" \| "MISMATCH"` | optional (additive) | How the paged read ended (`rendering-rules.md`, partial pages). |
| `collection.collected` | int | optional (additive) | Rows collected this cycle (`collected n`). |
| `collection.changedDuringRead` | bool | optional (additive) | `page.total` changed between pages. |
| `collection.duplicatesIgnored` | int | optional (additive) | Duplicate rows dropped this cycle. |
| `rows` | array of Row | required | All collected rows (see Rules). |

## Row (one per worker)

| Field | Type | Req | Source key |
|---|---|---|---|
| `dispatchId` (identity together with `source.namespace`) | string \| `"UNKNOWN"` | required | `dispatchId` |
| `taskId`, `runId` | string \| `"UNKNOWN"` | required | `taskId`, `runId` |
| `workerState`, `dispatchStatus`, `terminalState` | string \| `"UNKNOWN"` | required | same names |
| `role` | string \| `"UNKNOWN"` | required | `projection.role` |
| `provider` | string \| `"UNKNOWN"` | required | `projection.provider.id` |
| `hostKind`, `hostId` | string \| `"UNKNOWN"` | required | `projection.host.kind`, `projection.host.id` |
| `stage.worker`, `stage.dispatch` | string \| `"UNKNOWN"` | required | `projection.stage.worker`, `projection.stage.dispatch` (value sets UNVERIFIED; worker-reported, sanitized) |
| `stage.detail`, `stage.activity` | not present | not present | Withheld from the R1 snapshot. CONTRADICTION: architecture-options.md lists them; merged-requirements.md keeps them inspector-only because whether they carry question text is UNVERIFIED. The stricter reading applies until the open question in `SPEC.md` is answered. |
| `outcome` | string \| `"UNKNOWN"` | required | `projection.outcome` (raw) |
| `liveness.verdict`, `liveness.source` | string \| `"UNKNOWN"` | required | `projection.liveness.*` |
| `liveness.observedAt` | string (as given) \| `"UNKNOWN"` | required | `projection.liveness.observedAt` |
| `evidence.durable` | JSON value as given \| `"UNKNOWN"` | required | `projection.evidence.durable` (meaning beyond presence UNVERIFIED) |
| `evidence.liveStatus` | string \| `"UNKNOWN"` | required | `projection.evidence.liveStatus` |
| `evidence.lastObservedAt` | string (as given) \| `"UNKNOWN"` | required | `projection.evidence.lastObservedAt` (owner correction: the evidence timestamp is `projection.evidence.lastObservedAt`) |
| `nextAction` | string \| `"UNKNOWN"` | required | `projection.nextAction.kind` (raw, never classified) |
| `orderUnknown` | bool | optional (additive) | Observer flag: the row is flagged `order unknown` (`adapter-contract.md`). |
| `notReobserved` | bool | optional (additive) | Observer flag: the row was seen earlier this session and not read this cycle. |
| `absentFields` | array of string | optional (additive) | Observer list of the row's keys that carry `"UNKNOWN"` because the source omitted them, so a consumer can tell an absent field from a source value that is the text `UNKNOWN`. |

## Ordering

By `liveness.observedAt`, else `evidence.lastObservedAt`, newest first. Rows whose two timestamps are both `"UNKNOWN"` or unparsable sort after all timed rows. Ties break by `dispatchId`, then `source.namespace`.

This differs from the on-screen ledger, which keeps the source's "newest first" order. Which order is authoritative for consumers is an open question (`SPEC.md`).

## Not frozen in R1 (deliberately left out)

Terminal handles (`agentTerminalHandle`, `resource.terminalHandle`), worktree and endpoint ids, ownership and release state. They identify resources an attacker could target and are not needed to display the ledger. Attention Ledger (B) and Decision Desk (C) add their own optional field groups later, additively.

## Options considered (architecture-options.md)

| Option | Verdict |
|---|---|
| (a) Python + Rich observer, snapshot, Go screen later | Chosen |
| (b) Python gRPC plugin of TUIBBS | Refuted (plugins cannot draw; host unwired) |
| (c) PTY door | Not available (doors not built, v1 non-goal); bypasses ACS for write-back |
| (d) Go port first | Not for R1; home for the later Go screen and write-back |
| (e1) Reuse AI-session PTY spawn | Reserve only: sysop-only demo, replaces the AI spawn host-wide |
| (e2) Message Base bridge, (e3) Go program outside TUIBBS | Rejected |

Transport of the snapshot from the Coder host to the TUIBBS host is unexamined (UNVERIFIED).
