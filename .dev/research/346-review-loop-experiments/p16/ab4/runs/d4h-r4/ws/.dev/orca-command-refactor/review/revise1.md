review: 1 of 3 (revision 1, REVISE prompt; no re-review run)

# Revise 1: blocking findings M1, M2, M4, M5, M6, M7

Candidate revised in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
Baseline (text before the revision): `.dev/orca-command-refactor/specs/history/spec-v1.md`, byte-identical to the candidate before this revision (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`).
Input report: `.dev/orca-command-refactor/review/round1.md` (Reviser brief: ids M1, M2, M4, M5, M6, M7; verdict FAIL; M3 was rejected by the verifier and is not in the brief).
Verifier reply: `.dev/orca-command-refactor/review/verify-1.md`.

Scope: only the six ids above were repaired. `spec-panel` was not run. No other text was changed; the diff against the baseline contains only the hunks listed below. The M3 point is left alone (not in IDS).

## Byte accounting

Before: 57763 bytes. After: 62793 bytes. Net: +5030 bytes.

Method: line-level diff of `specs/history/spec-v1.md` against the revised spec. Each changed line is counted whole (including its newline), so these are line bytes, not character-level edit bytes. Totals reconcile: deleted 5697, added 10727, net +5030.

| Finding | Revised lines (after) | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|
| M1 | 62, 112, 159, 207, 208, 298 | 2653 | 2956 | +303 |
| M2 | 194 (step 3) | 275 | 431 | +156 |
| M4 | 195 (step 4) | 282 | 402 | +120 |
| M2 + M4 (shared line) | 206 (AC-0.4) | 463 | 658 | +195 |
| M5 | 79, 84, 87 | 618 | 1012 | +394 |
| M6 | 212 (AC-2.2), 224-244 (new table) | 356 | 3202 | +2846 |
| M7 | 147, 150, 172 and new code block 173-184 | 1050 | 2066 | +1016 |
| Total | | 5697 | 10727 | +5030 |

## Findings

| Id | Disposition | Where applied (revised file) | Basis |
|---|---|---|---|
| M1 | Applied. Option chosen: exempt `/sc:load` by name. The brief's "give load a contract" alternative was not taken. | WC-4 exception sentence (line 62). Load row, Report column (line 112). P1 scope cell notes the WC-4 exemption (line 159). AC-1.1 excludes load and requires it to have no Unattended section (line 207). AC-1.2 excludes load (line 208). Decisions row for load states the exemption (line 298). | `.dev/orca-command-refactor/inventory/commands-b.md:31` (`/sc:load` writes no file; context in chat) and `:62` ("None. Output is session context in chat"); `:65` (use as a brief step, not a Task). The contradiction is round1 M1 (spec:112, spec:159, spec:183, spec:195, spec:196). |
| M2 | Applied. In P0, step 3 checks the outcome against the command's existing report and the report path against the command's existing report path. The WC-4 path check moves to P1. | 7.2 step 3 pass condition (line 194). AC-0.4 (line 206). | Round1 M2 cites `REPORT.md` for troubleshoot (spec:91 before the revision) and P0 forbidding command edits (spec:158). Evidence used in the brief: `.dev/orca-command-refactor/inventory/commands-b.md:49,242`. |
| M4 | Applied. In P0, step 4 is `test -s` on the command's existing report only; the YAML field assertions (including `command`) apply from P1. | 7.2 step 4 pass condition (line 195). AC-0.4 (line 206). | The inventory-backed reason is that workflow's contract has no `command` key and troubleshoot writes `REPORT.md`: `.dev/orca-command-refactor/inventory/commands-b.md:49,52,242,272`. The adversarial contract name stays a P1 item (AC-1.4, line 210), as the finding asks; it is not changed here. |
| M5 | Applied. Section 3.1 intro now states that P1 adds the flag, the Unattended section and the WC-4 contract to all ten commands. Brainstorm and init-lite get their minimal change in their rows. | Section 3.1 intro (line 79). Brainstorm row (line 84): accept `--unattended` as a no-op, add an Unattended section naming the existing contract. Init-lite row (line 87): accept the flag as a no-op, add the section, write the WC-4 contract to `<output-dir>`. | `.dev/orca-command-refactor/inventory/commands-a.md:39` (brainstorm has `--interactive` only; it writes its own return contract per the spec row) and `:55` (init-lite writes `context-audit.md` or `--output`; no gate). Round1 M5 cites spec:79, spec:84, spec:87, spec:159, spec:195. |
| M6 | Applied. AC-2.2 now refers to a per-command table with one row for each of the 15 P2 commands, giving the gate-trigger input, the expected WC-2 resolution, the expected `--outcome`, and the expected contract and check. Roadmap is not in the table because its phase is P3 (section 3.2 row, line 118 before the revision); it is checked by AC-3.2 (line 205 in the revised file). | AC-2.2 (line 212); new table with heading at line 224 and rows 229-243. | The per-command resolutions come from the section 3 rows of the spec, which this revision does not change (for example the tdd example at line 200 before the revision; the cleanup and improve rows at spec:103 and spec:110 before the revision). Inventory evidence for those rows was not re-checked here beyond the spot checks listed under "Checks". |
| M7 | Applied. AC-C1 is moved to a fenced block with an unescaped `|` alternation under `-E`, `-i` for the ORCA placeholder, a full scan of `commands`, `skills` and `agents`, and a scan of `core` that excludes `WORKER-CONTRACT.md` and the routing guide's Orca section. A self-test requires a planted line to match. SA-2 and SA-5 now state the one exemption from AC-C1 in `core`. | AC-C1 row (line 172) and code block (lines 173-184). SA-2 (line 147). SA-5 (line 150). | Round1 M7 (spec:172, spec:147, spec:150, spec:180). The regex was re-checked here: the self-test matches `orca orchestration worker-start` and the `ORCA` placeholder (both print their OK line). |

Rejected findings: none among M1, M2, M4, M5, M6, M7.

## Checks

- Spot checks of inventory citations used in this revision: `.dev/orca-command-refactor/inventory/commands-b.md:31,62,65` and `.dev/orca-command-refactor/inventory/commands-a.md:39,55` were read and match the text cited above.
- The AC-C1 self-test was run in the sandbox on a planted line and matched; no scan over the real tree was run (no `src/` in this sandbox), so the scan result is UNVERIFIED here.
- The revised spec was checked by reading the changed regions and the `grep -n` of finding tags. Not run: `make verify-sync`, `uv run pytest`, and any live worker run (none exist in this sandbox).
- The AC-2.2 table rows marked "(a)" or "(c)" repeat the section 3 resolutions. The rows for cleanup, improve, research, auggie-review, reflect, tasklist and review-translation were not re-verified against the command files in this sandbox; they are UNVERIFIED beyond the spec's own cited lines.
