# Revision 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Blocking ids: F-1, F-2 (confirmed in `.dev/orca-command-refactor/review/verify-1.md`, last line `confirmed: F-1, F-2`; `round1.md:2`). Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Medium (M-1 to M-13) and minor (n-1 to n-4) findings were left alone. I did not run the spec-panel and I do not award a PASS.

Citation keys: `SPEC:N` = line N of the revised candidate; `OLD:N` = line N of `.dev/orca-command-refactor/specs/history/spec-v1.md` (byte-identical to the pre-revision candidate, checked with `cmp`); `R1:N` = `round1.md`; `INV-A:N`, `INV-B:N` = the inventories. Citations to `src/`, `cmd/`, `sk/` files are outside the workspace and UNVERIFIED here; I rely only on what the inventories say about them.

## Byte accounting

| Item | Bytes |
|---|---|
| Candidate before | 57763 |
| Candidate after | 58375 (sha256 `c9e2ff995f731358d2c486eecbe202f9c810da58a248e59a7c693464e08d5a7b`) |
| Net | +612 |
| Added / deleted, F-1 | +715 / -195 (net +520) |
| Added / deleted, F-2 | +92 / -0 (net +92) |

"Added" and "deleted" are character-level diff counts (difflib on the bytes of each replaced span), so a reworded phrase counts its changed bytes only. Net values sum exactly to +612. Line count unchanged (285). Twelve edits, on 9 lines (52, 62, 73, 76, 92, 149, 159, 195-196, 198; `diff` against `history/spec-v1.md`).

| # | Id | Where (SPEC line) | Added | Deleted | Net |
|---|---|---|---|---|---|
| 1 | F-2 | 52 (2.1 contract file: "other than `/sc:load`") | 28 | 0 | +28 |
| 2 | F-1 | 62 (WC-4 path rule) | 484 | 59 | +425 |
| 3 | F-1 | 62 (WC-4 "every outcome": workflow excepted) | 25 | 0 | +25 |
| 4 | F-1 | 73 (2.3: "output path", workflow excepted) | 22 | 8 | +14 |
| 5 | F-1 and F-2 | 76 (contract definition; "except `/sc:load`") | 32 | 23 | +9 |
| 6 | F-1 | 92 (workflow small fix) | 97 | 47 | +50 |
| 7 | F-2 | 159 (P1 flag scope: "except load") | 18 | 0 | +18 |
| 8 | F-1 | 159 (P1 fixes list: drop workflow) | 0 | 10 | -10 |
| 9 | F-1 | 149 (SA-4: drop workflow gap) | 7 | 16 | -9 |
| 10 | F-2 | 195 (AC-1.1) | 24 | 0 | +24 |
| 11 | F-2 | 196 (AC-1.2) | 22 | 0 | +22 |
| 12 | F-1 | 198 (AC-1.4) | 48 | 32 | +16 |

Edit 5 straddles both ids. The table gives it to F-1 in the totals above; its F-2 part ("except `/sc:load` (F-2) ", about 24 bytes added) is the only part that would move to F-2. The totals therefore overstate F-1 and understate F-2 by at most that amount.

## One row per finding id

| Id | Disposition | Applied where | Reasoning and evidence |
|---|---|---|---|
| F-1 | Applied, by narrowing the single path rule into a computed contract path plus two named exceptions, and by deleting the one fix that had no place to write | SPEC:62 (WC-4); SPEC:73; SPEC:76; SPEC:92; SPEC:149; SPEC:159; SPEC:198 | The finding's wrong outcome (R1:214): WC-4 gave `<file>/return-contract.yaml` for `--output <file>` (OLD:62, OLD:87, OLD:90, OLD:200), a different path for adversarial (OLD:83), and a path with a runtime `<id>` for workflow (OLD:92) against "known before dispatch" (OLD:73). Now WC-4 (SPEC:62) says: directory output gives `<output-dir>/return-contract.yaml`; a file output (tdd, init-lite, SPEC:87, SPEC:90) gives the sibling `<file>.return-contract.yaml`; a row that names a path wins, so adversarial's `<output>/adversarial/return-contract.yaml` (SPEC:83) is now consistent instead of contradictory. Workflow is an explicit exception: it mints `<id>` itself, so the coordinator reads the path from `worker_done --report-path` (SPEC:62; WC-4 already has the worker pass that path). SPEC:182-183 (7.2 steps 3-4) need no edit: "the WC-4 contract path" now resolves to a defined path, so `test -s <contract>` runs against `<file>.return-contract.yaml` in AC-2.2 (SPEC:200). Workflow's pre-creation stop: the old fix "Write the contract for pre-creation STOPs too" (OLD:92) had no directory to write into, because the inventory says the contract is "Not written for pre-creation STOPs" and lives under `<id>` (INV-B:272, citing `refs/return-contract.md:39`; the file itself is UNVERIFIED here; the verifier also flagged this sub-point as inventory-only, `verify-1.md` F-1 row). I deleted that fix rather than invent a fallback path (the REVISE prompt prefers deleting or narrowing): SPEC:92 now says a stop before the package exists writes no contract and ends `failed` under WC-5, whose "no report exists" clause already maps it to `failed` (SPEC:63). Consequent consistency edits, all deletions or narrowings: WC-4's "including stops before any other output exists" gets "(workflow excepted)" (SPEC:62); SPEC:73 "output directory" becomes "output path" with workflow excepted; SPEC:76 "Contract" is defined as the file "at the contract path"; workflow is removed from the P1 fixes list (SPEC:159) and from SA-4's list of defect fixes (SPEC:149); AC-1.4's pass condition (SPEC:198) now expects "a stop before its package exists writes no contract", replacing the old expectation that contradicted SPEC:92. Not edited: SPEC:83 (adversarial fix stays; it is now the row-named path), SPEC:87 and SPEC:90 (briefs stay `--output <file>`), SPEC:200 (AC-2.2 text stays; it now has a contract path). |
| F-2 | Applied, by narrowing scope: `/sc:load` is excluded from the `--unattended` section and WC-4 contract requirements, keeping the Decision | SPEC:62 (WC-4 exception); SPEC:52; SPEC:76; SPEC:159; SPEC:195 (AC-1.1); SPEC:196 (AC-1.2) | The finding's wrong outcome (R1:215): AC-1.1 and the P1 scope (OLD:159, OLD:195) required every command in 3.1-3.2, including `/sc:load`, to name `return-contract.yaml`, while the load row (SPEC:112, unchanged: report "none (see note)", use it "as a step inside another worker's brief, not as its own Task") and the Decision (SPEC:265, unchanged: "a report file would be an unrequested addition") say it gets no report. I kept the row and the Decision and narrowed the gate texts (the deletion-first choice among the two repairs the report offers, R1:65: exclude load, or drop the Decision). SPEC:195 now reads "every command in sections 3.1-3.2 other than `load` (F-2)", so P1's check can pass and SPEC:154 ("Later phases do not start until the earlier phase's checks in section 7 pass") no longer stalls on load. SPEC:159 says the flag is accepted by every 3.1-3.2 command "except load"; the "load (usage line only)" entry in the P1 command list stays, so its usage-line fix (SPEC:112) is unchanged. SPEC:62 (WC-4) states `/sc:load` writes no contract; SPEC:52 and SPEC:76 exempt it from the `## Unattended mode` section (the statements the finding and the verifier's row for SPEC:76 cite). AC-1.2 (SPEC:196, "each P1 command with `--unattended --output <dir>`") named load implicitly and would have failed the same way, so it carries the same exception. Not edited: the Decision text, the load row, section 4. |

## Checks run after the edits

- `diff history/spec-v1.md orca-worker-contract-spec.md` shows changes only on the 9 lines listed above; every replaced span was unique before replacement (the edit script asserted `count == 1`).
- Each added passage cites its finding id inline: `(F-1)` or `(F-2)` appears on every edit except two deletions-only spans (edits 8 and 9), which cite the id here.
- Leftover references checked with `grep -nF`: no remaining `<output-dir>/return-contract.yaml` outside WC-4's own directory case; no remaining "pre-creation STOPs" expectation in SPEC:92 or SPEC:198; no remaining "workflow" entry in the P1 fixes list or SA-4's list.
- Not run (outside the workspace, UNVERIFIED): the spec's own greps and tests over `src/`, and any check of `cmd/`, `sk/`, `refs/return-contract.md`.

## Effects to note for the next review

- Workflow now has no "write on every outcome" guarantee for pre-creation stops; WC-5's no-report rule covers it as `failed`. The coordinator learns the workflow contract path only after dispatch. This is the narrowing chosen for F-1; the alternative (a fixed fallback path) would add a mechanism no finding calls for.
- Edit 5 and the `/sc:load` exemptions touch lines also named by Medium findings M-1 (P1 scope) and M-12 (traceability). I made no change for those findings; any residual mismatch there remains a follow-up candidate.
