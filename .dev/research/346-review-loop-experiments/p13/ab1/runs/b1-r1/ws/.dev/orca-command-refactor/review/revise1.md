# Revise 1: blocking findings L1, L2, L9, L10

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Source of the finding ids: `.dev/orca-command-refactor/review/round1.md` (Reviser brief: "Blocking finding ids: L1, L2, L9, L10"). Line numbers below are of the revised spec. No self-awarded PASS; the spec-panel was not run. I touched no file other than the spec and this report.

## Byte accounting

Spec size: before 57763 bytes (`wc -c`), after 60365 bytes (`wc -c`), net +2602. Added and deleted are the bytes of changed text per id (character-level diff of each edited fragment; the last L2 edit, the "unless the person chose that in D2 or D4" fix, is counted gross: +40 / -14).

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| L1 | 1058 | 192 | +866 |
| L2 | 1750 | 269 | +1481 |
| L9 | 181 | 57 | +124 |
| L10 | 132 | 1 | +131 |
| Total | 3121 | 519 | +2602 |

The total net equals the file-size change, so no byte is unattributed. Where one edit served two ids I assigned it to the id whose defect it answers (the `/sc:load` exclusions are L10, the rest of the P1 and AC-1.1 text is L1).

## Finding rows

| Id | Disposition | Where | Reason |
|---|---|---|---|
| L1 | applied (all sub-claims except those under "Not applied") | Spec 73 (2.3 brief wording), 76 (section 3 intro), 79 (3.1 intro), 154 (section 6 intro), 159 (P1 row), 194 (AC-0.4), 195 (AC-1.1), 67 (WC-9), 69 (WC-11), 147 (SA-2), 172 (AC-C1, shared with L9) | See L1 sub-rows. |
| L2 | applied (all sub-claims except those under "Not applied") | Spec 61 (WC-3), 62 (WC-4), 63 (WC-5), 64 (WC-6), 148 (SA-3), 87 (init-lite row), 92 (workflow row), 114 (pr-submit row), 183 (7.2 step 4) | See L2 sub-rows. |
| L9 | applied | Spec 172 (AC-C1) | The old cell held `\|` inside `grep -E`, which is a literal pipe there (and a markdown table escape in the cell), so the command could never match an Orca call (`round1.md` L9.t2-1 F3, L9.t3-2 F6). The new command has no pipe at all: four `-e` patterns, and the exclusions are `--exclude-dir=ccsession-tag --exclude=WORKER-CONTRACT.md --exclude=HOW-WE-WORK.md` instead of `grep -v`. I ran the new command on a toy tree inside the workspace (removed afterwards): it printed an `orca-ide orchestration` line under `commands/` and ignored the `ccsession-tag` file. |
| L10 | applied | Spec 112 (load row), 76 (section 3 intro), 195 (AC-1.1) | The `/sc:load` decision (no report file, `INV-B:65`, Decisions table "`/sc:load` handling") is kept and the check that contradicted it is narrowed. The load row now says it gets no flag, section or contract and is never its own Task, so WC-5's "no report exists means failed" never applies to it. AC-1.1 asserts the section for the P1 commands other than `load`, and that neither a section-4 command nor `load` has one. The P1 row keeps `load (usage line only)`. |

### L1 sub-rows (reviewer claim, then the fix)

| Claim (round1.md) | Fix | Spec line |
|---|---|---|
| AC-1.1 requires a contract for load (t1b-1 F1, t3-1 F1; also L10) | `load` excluded from AC-1.1 and from the section 3 intro (the L10 edits) | 112, 76, 195 |
| P0 gate cannot pass: step 3 needs a WC-4 contract and step 4 a YAML for troubleshoot and adversarial (t1b-1 F3, t2-1 F2, t3-1 F2, t3-2 F2) | AC-0.4 now says steps 3 and 4 use the command's existing report file from its 3.1 row (troubleshoot `REPORT.md`, workflow contract, adversarial contract under `<dir>`); step 3 checks the outcome against that file's own verdict and path; step 4 is only `test -s` | 194 |
| P0 smoke briefs lack `--unattended`, which section 2.3 requires (t3-2 F3) | 2.3 now says "including `--unattended` once the command accepts it (section 6)"; AC-0.4 states the P0 briefs omit it | 73, 194 |
| P1 flag "accepted by every command in 3.1 and 3.2" is inert for commands whose gates convert in P2-P4, and brainstorm, init-lite, tdd, release-split are in no cell (t1b-1 F5, F12; t2-1 F5; t3-2 F1) | Narrowed, not widened: a command gains the flag, its section and its contract in the phase that lists it (new sentence in the section 6 intro); P1 now lists brainstorm and init-lite and marks adversarial, cleanup-audit, index-repo and workflow as getting the flag with their small fix; tdd and release-split are already in the P2 cell; AC-1.1 asserts the section only for the P1 row | 154, 159, 79, 76, 195 |
| "paid external run" undefined (t1b-1 F14) | Replaced by "another outward action listed for the command in column (f) of the inventories", the evidence WC-9 already cites | 67 |
| cleanup-audit and index-repo fixed output paths vs WC-11 (t2-1 F9, t3-2 F15) | WC-11 exempts those two fixed paths and requires one such worker per worktree at a time, matching the 3.1 rows | 69 |
| SA-2 vs the Orca section P0 adds to HOW-WE-WORK.md and the contract file (t1b-1 F9) | SA-2 names the two files allowed to show an `orca` command line; AC-C1 excludes exactly those | 147, 172 |

### L2 sub-rows

| Claim (round1.md) | Fix | Spec line |
|---|---|---|
| WC-4 location contradictory for file-valued `--output`, the adversarial subfolder and workflow (t1b-1 F2, t2-1 F7, t3-1 F3, t3-2 F4) | WC-4: `<output-file>.return-contract.yaml` where the flag takes a file; adversarial and workflow use their 3.1 row paths; the workflow row gains `--output <dir>` (P1) so the path is known before dispatch, pre-creation STOPs included | 62, 92 |
| Fresh directory vs known-before-dispatch; retry overwrite (t1b-1 F10, t2-1 F6 and F8, t3-1 F4, t3-2 F5) | WC-6: the coordinator gives each attempt a new output path in the brief; a command is never pointed at an earlier attempt's path; "Fresh dir" is defined; the init-lite row says a new `--output` per attempt | 64, 87 |
| WC-3 lets an answer reach gates reserved for the person; no flag name, cap or outcome (t1b-1 F4, t2-1 F1 and F14, t3-1 M3, t3-2 F7) | WC-3 rewritten smaller: a blocked gate ends the run as `failed`; the coordinator answers with a new Task using the flag the 3.2 row names; no self re-invocation; a relayed answer never replaces the person's Ruling or authorization unless the person chose that in D2 or D4; retries bounded by the circuit breaker (`.dev/orca-command-refactor/inventory/orca-capabilities.md:116`, read, quotes the three-failure break). The pr-submit "may use `ask` or `escalation`" aside is deleted | 61, 114 |
| Statuses undefined or clashing (t1b-1 F7) | Four values defined in WC-4; existing differing values are mapped by the command's fix, and the existing value sets are marked UNVERIFIED (the inventories name only `status`, `.dev/orca-command-refactor/inventory/commands-b.md:272`) | 62 |
| Malformed or waiting contract sent as succeeded; partial file (t2-1 F11 and F12, t3-2 F8) | WC-5: failed also on non-empty `blocked_question`, missing or unlisted `status`, unreadable report; succeeded only for `succeeded` or `partial`. WC-4: written whole in one step | 63, 62 |
| WC-4 vs SA-3 conditions differ (t1b-1 F13) | SA-3: contract only in unattended mode; a new report file also when the row's output flag is passed | 148 |
| No version field (t1b-1 F19, t2-1 F15) | `version` (`1`) added to WC-4's field list and to the 7.2 step 4 assertion | 62, 183 |

### Not applied (inside L1 or L2, with reason)

| Claim | Reason |
|---|---|
| L2 t1b-1 F8: define `--unattended` on a coordinator-only command, as a refusal, or inside quoted content | Only the missing-output-path case is added to WC-4 ("writes nothing and the worker ends `failed`"). The other cases are edge cases the spec never stated; adding rules for them goes beyond the contradictory contract location and gate handling that make L2 blocking. Left for follow-up. |
| L2 t1b-1 F10 and t2-1 F14: explicit retry and ask-cycle caps | No new cap is written. Removing the self-re-invocation loop from WC-3 leaves no unbounded ask cycle, and Orca's circuit breaker bounds retries (`orca-capabilities.md:116`). |

## Notes for the next review

1. The same literal-pipe form (`\|`) remains in AC-C4, AC-C5 and AC-0.3. No blocking finding names them (L9 names only AC-C1), so I left them alone; a reviewer may raise them.
2. Two Medium findings that touch nearby text were left alone: L3/L4 (WC-10 and pr-submit wait wording) and L11 (reflect under `--unattended`).
3. Sandbox note: early in the run I ran a shell `cp` of the spec to the session scratchpad, which is outside the sandbox. I noticed at once and deleted that copy. Nothing else outside the workspace was written.
4. Citations: I read `orca-capabilities.md:116` and `commands-b.md:272` in this run. All other `INV-*`, `CAPS:*` and `sk/`/`cmd/` citations in the spec are carried unchanged and were not re-read here, so they stay as UNVERIFIED as before. `sk/` and `cmd/` paths cannot be checked inside this workspace.

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "AC-0.4, AC-1.1, the section 6 flag scope, WC-9, WC-11, SA-2 and AC-C1 were narrowed or reworded so the P0 and P1 checks and the common check can pass (spec lines 67, 69, 73, 79, 147, 154, 159, 172, 194, 195)."}
{"id": "L2", "action": "applied", "reason": "WC-3 to WC-6 and SA-3 were rewritten so the contract location, retry path, blocked-question handling and outcome mapping no longer contradict each other (spec lines 61-64, 87, 92, 114, 148, 183)."}
{"id": "L9", "action": "applied", "reason": "AC-C1 now uses four -e patterns and --exclude options with no pipe character, so it can match an Orca command (spec line 172; tested on a toy tree)."}
{"id": "L10", "action": "applied", "reason": "The /sc:load decision stands; load is excluded from the flag, section, contract and AC-1.1 and is never its own Task, so WC-5 does not apply to it (spec lines 76, 112, 195)."}
```
