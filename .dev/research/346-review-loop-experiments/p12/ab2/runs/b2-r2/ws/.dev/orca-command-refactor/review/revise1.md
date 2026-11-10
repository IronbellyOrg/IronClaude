# Revise report, round 1: Orca worker contract spec

- Prompt followed: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (SPEC:N below = line N of it; the edits add no line, so line numbers are unchanged).
- Ids repaired: B-1, B-2, B-3 (review/round1.md:2, review/round1.md:208; confirmed in review/verify-1.md last line). Medium and minor findings were not touched. No PASS is claimed; the candidate goes back for review 2.
- Citation shorthand: `INV-A:N`, `INV-B:N` = lines of `inventory/commands-a.md`, `commands-b.md`. Every `path:line` into `cmd/`, `sk/` and other repository files is UNVERIFIED here (not in the sandbox); only the inventory and spec lines were checked.

## Byte accounting

| Measure | Bytes |
|---|---|
| Candidate before (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`) | 57763 |
| Candidate after (sha256 `68ce70455b6b30e6a44dbd6460d0688443a0dcdfe80ef873cfa87d79d9501aee`) | 58534 |
| Net | +771 |

Added and deleted bytes are counted by a word-level diff of each edited span (changed words only); net per id equals added minus deleted and the three nets sum to +771.

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| B-1 | 804 | 215 | +589 |
| B-2 | 62 | 0 | +62 |
| B-3 | 136 | 16 | +120 |
| Total | 1002 | 231 | +771 |

B-1 is the largest because it replaces one location rule with a rule plus four stated exceptions; the offsetting deletions are two small-fix clauses removed (see below).

## Finding rows

| Id | Result | Where applied (SPEC lines) | What changed and why (evidence) |
|---|---|---|---|
| B-1 | applied | SPEC:62 (WC-4), SPEC:73 (2.3), SPEC:76 (section 3 intro), SPEC:92 (workflow row), SPEC:159 (P1 commands), SPEC:198 (AC-1.4) | The contract path is now one stated rule with its exceptions, so the path WC-4 gives and the paths the rows give no longer disagree. (1) adversarial: WC-4 now names `<output>/adversarial/return-contract.yaml`, matching the row at SPEC:83 and `INV-A:35` (real runs wrote that path). (2) tdd and init-lite pass `--output <file>` (SPEC:87, SPEC:90; `INV-B:222`, `INV-A:55`), so the contract is `<file>.return-contract.yaml`; SPEC:73 now says the brief fixes the output file for these two. This makes AC-2.2 (SPEC:200, `/sc:tdd ... --output <file>`) and 7.2 step 4 (SPEC:183) testable. (3) workflow: the package id is generated (`INV-B:272`) and a pre-creation STOP writes no contract (`INV-B:272`, citing `sk/sc-workflow-protocol/refs/return-contract.md:39`, UNVERIFIED), so no path can be known before dispatch for that case. Instead of adding a new location mechanism I narrowed: the SPEC:92 fix "write the contract for pre-creation STOPs too" is replaced with "None", WC-4's "every outcome" excepts that one STOP, and the worker sends `--outcome failed` with no `--report-path`, which WC-5 already maps from "no report exists" (SPEC:63) and `CAPS:72-74` allows ("`--report-path` only with real values"). The workflow row leaves the P1 fix list (SPEC:159) and AC-1.4 (SPEC:198) no longer asks for it. How the worker learns `<id>` after the package exists is marked UNVERIFIED in WC-4 (I could not check the skill). SPEC:76 now says "Contract" means the WC-4 file at the contract path, not the single form. |
| B-2 | applied | SPEC:76, SPEC:159, SPEC:195 (AC-1.1), SPEC:196 (AC-1.2) | `load` is excluded from the `## Unattended mode` section requirement and from the P1 flag sentence, and from the AC-1.2 live check, by adding "except `load`" in four places. Nothing is added to `load`: the row (SPEC:112) and the Decision (SPEC:265) keep "no report file, usage-line fix only", which agrees with `INV-B:65` ("it only loads context into the current session and writes no file"). The later-phase part of the report's recommendation (exclude commands whose phase is after P1) was not applied: the finding's grading sentence rests on `load` alone, and SPEC:159 already gives every command in 3.1-3.2 the flag in P1, so a wider narrowing would be a change no blocking finding calls for. |
| B-3 | applied | SPEC:194 (AC-0.4) | The relaxation now covers step 3 as well as step 4: steps 3 and 4 use the command's existing report file in place of the contract, with step 3's `--outcome` matched to that report's own result and its report path being that file. P0 makes no command edits (SPEC:158), so the contract that step 3's pass condition names (SPEC:182) does not exist yet for troubleshoot (`REPORT.md`, SPEC:91). The clause "a failure here reopens section 1" is kept: with the false-negative cause removed, a failure of steps 1, 2 or 5-7 or of the relaxed steps is a real signal about the decision. SPEC:182 (the 7.2 step text) is unchanged because the P1+ pass condition is right. |

## Rejected

None. All three confirmed ids were applied.

## Checks run after the edits

- `grep -c` confirmed each old span existed exactly once before it was replaced (the edit script asserted this, and failed on none).
- Line count is unchanged; the only changed lines are SPEC:62, 73, 76, 92, 159, 194, 195, 196, 198.
- The three Decisions rows that mention contracts (SPEC:261 report shape, SPEC:265 load) still agree with the edited text.
- Not checked: any `cmd/`, `sk/` or repository line (UNVERIFIED in this sandbox).
