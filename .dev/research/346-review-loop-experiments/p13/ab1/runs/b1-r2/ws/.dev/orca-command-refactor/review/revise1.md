# Revise 1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place). Blocking ids: L1, L7, L9, L11 (`review/round1.md` Reviser brief). Minor and Medium findings (L2-L6, L8, L10, L12-L29) untouched. No self-awarded PASS.

## Byte accounting

Size before: 57763 bytes. Size after: 60598 bytes. Net +2835. Added/deleted counts are character-level diff bytes inside each edited span (added minus deleted summed over ids = 3272 - 437 = 2835).

| id | bytes added | bytes deleted |
|---|---|---|
| L1 | 2227 | 256 |
| L7 | 322 | 128 |
| L9 | 447 | 0 |
| L11 | 276 | 53 |
| total | 3272 | 437 |

Every addition carries its finding id in the spec text as `[L1]`, `[L7]`, `[L9]` or `[L11]`, except in-place rewrites of AC-C1, AC-C4 and the AC-1.1/AC-1.4 phrases (L7, L1), which replace text and add no new rule. The edits grew the file because the L1 findings call for stated locations and phase ownership; deletion alone could not meet them.

## One row per finding id

| id | disposition | where applied (spec line numbers after edit) and why |
|---|---|---|
| L1 | applied | Contract location and path: WC-4 (line 62) now states `<output-dir>/return-contract.yaml`, the file-output exception `<file>.return-contract.yaml` (tdd, init-lite), adversarial's `<output-dir>/adversarial/` path (matches the 3.1 fix, line 83), and workflow/research placed beside the deliverable with the path passed as `--report-path`; adds `schema_version`, `artifacts` includes changed files, and removes "known before dispatch". Workflow stop before the package exists: WC-4 says no contract, WC-5 no-report rule applies; workflow row (line 92) and AC-1.4 changed to match. Stale contract and retry directory: WC-6 (line 64) and section 2.3 (line 73) require a new output directory in a retry brief. WC-5 (line 63) maps an empty report or out-of-set status to failed. Section 2.3 also makes the coordinator check status and verdict before a dependent starts. WC-3 (line 61): ask not used when the brief forbids it or for `E-HALT-QA`/`E-NO-RULING` (D2), so it no longer permits the relayed Ruling or contradicts AC-2.2, whose gate-trigger run is briefed not to ask (line 200). WC-2 (line 60) counts reflect's existing headless auto-accept as a documented default. Phase ownership: section 3 intro (line 76), 3.1 intro (line 79), P1 row (line 159) and AC-1.1 (line 195) give each command its flag, Unattended section and contract in its own phase and exclude `/sc:load` and the P4 commands; pr-submit is P4 only under D3 (b) (line 114, line 162). P0 gate: AC-0.4 (line 194) briefs with flags accepted today, uses the existing report file for steps 3-4 and `test -s` in place of the YAML check; step 5 (line 184) now also searches for an Agent-tool wrapper, so the no-wrapper claim has a check. Orca-checks-the-file assumption marked UNVERIFIED (`CAPS:79`) in WC-4. Not changed: F16 (existing contracts' status words) is addressed only by the "status takes one of the four values" clause; existing contracts are not checkable here (UNVERIFIED, the reviewer's own note). |
| L7 | applied | AC-C1 (line 172) rewritten with four `-e` patterns and `--exclude-dir=ccsession-tag`, `--exclude=WORKER-CONTRACT.md`, `--exclude=HOW-WE-WORK.md`: no escaped alternation bar, and the P0 contract file and routing-guide Orca section no longer trip it. AC-C4 (line 175) rewritten as one `git diff --cached --name-only -- .claude ':!.claude/settings.json'` with no pipe. SA-2 (line 147) reworded to say where Orca may be named (contract file, routing guide section) and that no command, skill or agent file names an Orca command. The edited pattern was spot-checked with `grep -E -e` on a test string only; the full command was not run (no `src/superclaude/` tree in the workspace), so it is UNVERIFIED against real files. |
| L9 | applied | Section 1.1 (line 16) now includes the defect fixes section 3 names (SA-4), so AC-3.1 and AC-3.3 are no longer excluded. SA-4 (line 149) adds the cli-portify checkout restriction to its closed list. Section 2.3 (line 73) says the command line is the first instruction after the preamble, marks "a slash command typed after a preamble loads as a command" UNVERIFIED (`inventory/orca-capabilities.md:47`: Orca types the task into the input box once ready), and AC-0.4 plus step 5 test it. |
| L11 | applied | WC-11 (line 69) no longer claims default paths are unique: the coordinator gives each worker its own output path and runs fixed-path commands (index-repo `PROJECT_INDEX.md`, cleanup-audit `.claude-audit/`, init-lite without `--output`) and source-editing commands one at a time per worktree or in separate worktrees; owner column now names the coordinator. Section 2.3 (line 73) adds the same duty to the brief. |

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "Stated contract path rules and exceptions, per-phase ownership of flag and section, P0 gate made passable, retry directory, WC-3/WC-5 gaps closed (WC-2..WC-6, 2.3, 3.1, P1, AC-0.4, AC-1.1, AC-1.4, AC-2.2)."}
{"id": "L7", "action": "applied", "reason": "AC-C1 and AC-C4 rewritten without escaped alternation bars and with excludes for the contract file and routing guide; SA-2 reworded."}
{"id": "L9", "action": "applied", "reason": "Section 1.1 and SA-4 now include the section 3 defect fixes (and the cli-portify restriction); 2.3 states how the worker starts the slash command and marks it UNVERIFIED with a test in AC-0.4."}
{"id": "L11", "action": "applied", "reason": "WC-11 now assigns the coordinator to give distinct paths and serialize fixed-path and source-editing workers per worktree."}
```
