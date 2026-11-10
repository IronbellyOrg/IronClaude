review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique mode, focus requirements,architecture)

Labelled whole-document audit of the final spec: a first review of the whole document. No `--re-review`/`--baseline` was given, so this is a first review (baseline not applicable).

| Header field | Value |
|---|---|
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `530bb94dc36fffb71a0dd0f59ecf0aa60e32ab1c485bde6cfedea040d97adda7` |
| baseline sha256 | none (no baseline given) |
| reviewer model | claude-sonnet-5-5 |
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` |
| inputs read | candidate (294 lines), `.dev/orca-command-refactor/README.md`, the three files under `inventory/` (spot-checked, see Coverage) |

Citation convention: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any `cmd/`, `sk/`, `EVIDENCE.md`, codegraph README, `install_core.py` or `CLAUDE.md` line the candidate cites is UNVERIFIED here: those files are not inside the workspace. The inventories are the only evidence checked.

## Summary
The decision (Orca coordinates, commands stay workers, `--unattended` plus a fixed report file) is consistent with the inventories (`CAPS:97-103`, `CAPS:147-150`, `INV-A:96-97`, `INV-B:292`). The 10 / 27 / 6 split adds up to 43 (`S:76`; rows 82-91, 99-125, 132-137). One blocking finding is open: the contract path rule for commands whose `--output` is a file. Nine Medium findings and seven minor notes are listed under `follow-up candidates`.

## === REQUIREMENTS ANALYSIS ===

### B-1 (MAJOR, blocking) Contract path for file-valued `--output` collides across workers
- Experts: Wiegers (consistency), Whittaker (Sentinel Collision / Accumulation).
- Grading sentence: An implementer who follows WC-4 as written makes `/sc:tdd` and `/sc:init-lite` write `<directory containing --output>/return-contract.yaml` (`S:62`, `S:87`, `S:90`, `S:208`). That is wrong because WC-11 says two workers in one worktree must never write the same file (`S:69`): two `/sc:tdd` workers given sibling files such as `docs/tdd/auth.md` and `docs/tdd/billing.md` share `docs/tdd/return-contract.yaml`. The later write replaces the earlier worker's `status` and `blocked_question`, and the earlier worker's `worker_done --report-path` then points at another worker's report. The spec's own purpose is parallel workers, and `S:73` tells the coordinator to pass "the output directory" without saying it must be unique per worker.
- Concrete attack (Sequence/Accumulation): t0 worker A (`tdd`, `--output docs/tdd/auth.md`) writes `status: blocked`; t1 worker B (`--output docs/tdd/billing.md`) writes `status: succeeded` to the same path; t2 the coordinator opens A's `--report-path` and reads `succeeded`, while A sent `--outcome failed` (WC-5, `S:63`).
- Recommendation: narrow WC-4 for file-valued `--output` to a path that cannot be shared (either require the brief to give such a command its own dedicated directory, or name the contract after the output file's basename). Update `S:87`, `S:90` and AC-2.2 (`S:208`) to match.
- Priority High.

## === ARCHITECTURE ANALYSIS ===
Fowler, Newman, Hohpe and Nygard find the boundary sound: commands stay units, the coordinator owns Tasks, the contract file is the single message from command to coordinator (`S:16`, `S:62`; `CAPS:79`: Orca treats `--report-path` as a pointer only). Two structural risks are in the follow-up list: the phase ordering against gate conversion (M-4) and heartbeat starvation by long single tool calls (M-5). The rejected alternative (commands calling Orca) is argued from `CAPS:97-103`, `CAPS:145-150` and `INV-B:285-286`, all consistent with what they cite; the "it has worked before" evidence is weaker than its headline (n-1).

## Whittaker adversarial analysis (FR-2.x; scope = specification correctness)
- Zero/Empty: WC-4 with no output directory known (M-1). WC-5 with a zero-byte or missing report maps to failed (`S:63`), which is specified.
- Divergence: WC-3 (ask, then re-invoke) against WC-2(c) (write blocked, stop) and WC-5 (blocked maps to failed) are reconciled only by "may" (`S:61`). Retry directory against the known report path (M-2).
- Sentinel Collision: `status` values (`S:62`) against statuses existing contracts already use (M-6). The fixed filename `return-contract.yaml` shared by file-valued outputs (B-1).
- Sequence: `--unattended` accepted in P1 before gates convert in P2 (M-4).
- Accumulation: one long tool call against the 5-minute heartbeat (M-5).
Corrections to the Pipeline Dimensional Analysis: not triggered. The spec describes a coordinator/worker lifecycle and a phase plan, not a multi-stage data pipeline whose stage counts differ (no filter, aggregate or fan-out stage with a downstream count consumer). No Quantity Flow Diagram is produced. `--focus correctness` was not requested, so no State Variable Registry is produced.

## Guard Condition Boundary Table
Guards found: WC-4 output directory, WC-5 status mapping, WC-10 wait size, task confidence 0.70 (`S:121`), WC-1 readiness limit. Classes left out are named in the last column of the last rows.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 output dir | S:62 | Zero/Empty | no `--output`, or unwritable | no dir | none stated; "written on every outcome" (S:62) cannot hold | GAP (M-1) |
| WC-4 output dir | S:62 | One/Minimal | `--output a.md` alone in its directory | dir = parent | contract beside it | OK |
| WC-4 output dir | S:62 | Typical | `--output <dir>` | dir | `<dir>/return-contract.yaml` | OK |
| WC-4 output dir | S:62, S:69 | Legitimate Edge Case | two file outputs in one directory | same path | silently shared; contradicts WC-11 | GAP (B-1) |
| WC-4 output dir | S:62 | Maximum/Overflow, Sentinel | left out: a path has no capacity sentinel the spec uses | n/a | n/a | n/a (reason given) |
| WC-5 status map | S:63 | Zero/Empty | `status` missing, or no report | false | `--outcome failed` | OK |
| WC-5 status map | S:63 | One/Minimal | `partial` | true | `--outcome succeeded`, body states `partial` | OK |
| WC-5 status map | S:63 | Typical | `succeeded` / `failed` / `blocked` | per value | succeeded / failed / failed | OK |
| WC-5 status map | S:63, S:201 | Sentinel Value Match | a value outside the four (existing contracts) | false | `failed`; but AC-0.4 asserts the four values for `workflow` without evidence | GAP (M-6) |
| WC-5 status map | S:63 | Legitimate Edge Case | `succeeded` with `verdict: FAIL` | true | run succeeds, coordinator gates on `verdict` | OK |
| WC-5 status map | S:63 | Maximum/Overflow | left out: the status set is a closed list of four | n/a | n/a | n/a (reason given) |
| WC-10 wait size | S:68 | Zero/Empty | no long wait | n/a | no split needed | OK |
| WC-10 wait size | S:68 | Typical | wait of 4 min | true | heartbeat between waits | OK |
| WC-10 wait size | S:68 | Maximum/Overflow | one Agent-tool call longer than 5 min | true | not addressed; only polls and evals named | GAP (M-5) |
| WC-10 wait size | S:68 | Legitimate Edge Case | wait of exactly 5 min | false | split to at most 4 min (S:274) | OK |
| task confidence | S:121 | Typical / Edge | below 0.70 | true | blocked | OK |
| task confidence | S:121 | Legitimate Edge Case | 0.70 to 0.89 band | false | not stated whether `/sc:task` presents alternatives to a person there; UNVERIFIED (INV-B:199 names only the below-0.70 prompt) | GAP (note n-8) |
| task confidence | S:121 | Zero/Empty, Sentinel | left out: confidence is computed, not supplied | n/a | n/a | n/a (reason given) |
| WC-1 readiness | S:59 | Typical / Edge | fallback of 30 s; above about 45 s fails | per value | evidence in `CAPS:49`; WC-1 says "well inside" without a number | OK (see n-3) |
| WC-1 readiness | S:59 | Zero/Empty, Maximum, Sentinel | left out: set by launch setup, not by a command | n/a | n/a | n/a (reason given) |

The table is complete under FR-10: every guard is listed and every class either has a row or a one-line reason.

## Other expert notes
- Wiegers: traceability is good (every WC row cites evidence; section 3 rows carry evidence and phase). WC-1 has an owner but no phase and no check of its own (n-3).
- Adzic: AC-2.2 gives concrete gate-trigger examples (`S:208`); a degenerate example for M-1 (no output directory) is missing.
- Cockburn: the primary actor is the coordinator and the goal is a readable report; the person-at-keyboard goal (SA-1, `S:146`) is protected by default-off `--unattended`.
- Nygard: failure modes covered include blocked, fenced consumer (`S:70`), circuit breaker (`CAPS:80`), silent stall (`S:44`); the unaddressed one is heartbeat starvation (M-5).
- Newman, Hohpe: the single file-based message with a fixed name is the right integration pattern; versioning of the contract schema is not specified (no `contract_version`; the workflow contract has one, `INV-B:272`). Minor, folded into n-5.
- Crispin: acceptance checks are executable and mostly falsifiable (`S:178-183` self-test is good practice); weaknesses are M-3, M-6, M-7.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

### Medium (warnings)
- M-1 No contract location when the output directory is missing or unusable. WC-4 requires a file "on every outcome ... including stops before any other output exists" (`S:62`), but the post-release row makes a missing `--output` itself a blocked case (`S:113`). The implementer must invent a path.
- M-2 WC-6 says a command without a resume flag "writes each run into a fresh output directory" (`S:64`), while WC-4 fixes the contract path from the directory the coordinator passed (`S:62`) and WC-3 re-invokes the command after an `ask` (`S:61`). Section 2.3 (`S:73`) does not tell the coordinator to give a retry or re-invocation a new directory.
- M-3 AC-C1 must print nothing over `src/superclaude/core` (`S:172`, `S:182`), but P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md` in that folder (`S:158`), and SA-2 allows an Orca mention inside the contract file (`S:147`). Whether those files may contain a string the pattern matches (for example the `ORCA orchestration ...` placeholder used in 7.2, `S:167`, `S:187`) is not stated.
- M-4 P1 says `--unattended` is accepted by every command in 3.1 and 3.2, "a no-op where a command has no gate" (`S:159`), and AC-1.1 requires an Unattended section for all of them (`S:202`), but gate conversion for gated commands is P2 to P4 (`S:100`, `S:160`, `S:162`) and Phase 4 waits for D2-D4 (`S:154`). Between phases a gated command accepts the flag while still prompting or posting (auggie-review, `S:100`), against WC-2 and WC-9 (`S:60`, `S:67`).
- M-5 WC-10 names only poll waits and evals (`S:68`, rows `S:104`, `S:114`). A foreground Agent-tool call from `/sc:adversarial`, `/sc:tdd` or `/sc:tasklist` can also block the top-level session for more than 5 minutes, and whether heartbeat age matters to Orca is UNVERIFIED (`CAPS:130`).
- M-6 AC-0.4 asserts `status` is one of the four values for the existing `workflow` contract (`S:201`), but the inventory lists only its field names (`INV-B:272`), and it says the adversarial contract file name is not fixed (`S:83`, `INV-A:60`) while AC-0.4 runs `test -s` on "its existing contract file".
- M-7 AC-2.4 counts `pulls/<PR>/reviews` and `pulls/<PR>/comments` (`S:210`); a PR-level issue comment (`issues/<PR>/comments`) would go uncounted. Which endpoint auggie-review uses is not in the inventory (`INV-A:38`). Row `S:100` also relies on a positive `--post-pr` flag; only `--no-post-pr` appears in the inventory (`INV-A:78`).
- M-8 Several required inputs are unnamed, so the section 2.3 brief template cannot list them: cli-eval "the safety flags" (`S:104`), review-translation "a pre-confirmed context input" (`S:117`), post-release "an explicit pre-tag choice" (`S:113`), and WC-9's "the command's own explicit flag" for commands that have none (`S:67`).
- M-9 cleanup and improve apply every non-approval item under `--unattended` while their rollback mechanism is UNVERIFIED (`S:103`, `S:110`, `INV-A:118`); the report lists changed files, but no revert step is required.

### Minor notes
- n-1 E3 says "It has worked before" and cites `skill-direct` (`S:23`), while 1.4(1) says the earlier run proves only the nested route (`S:43`). Reconcile the wording.
- n-2 `S:11` says other section-3 lines were "carried from the inventories without a second read"; `S:293` says a validator re-read about 340 citations. Both can be true but read as inconsistent.
- n-3 WC-1 has no phase and no dedicated check (`S:59`); it also gives no number for "well inside" although `CAPS:49` supports about 30 s.
- n-4 7.2 step 5 searches the transcript for the string `AskUserQuestion` (`S:191`); the injected command text may contain that word. Check for a tool call, not the string.
- n-5 The contract schema carries no version field (compare `INV-B:272`).
- n-6 The command text points only at `~/.claude/WORKER-CONTRACT.md` (`S:52`); the repo's dual-surface rule for primitives that look up another primitive may also apply (CLAUDE.md, UNVERIFIED here).
- n-7 `S:112` lists `/sc:load` as P1 while `S:159` and `S:202` treat it as an exception in some places and not others.
- n-8 Row `S:120` says spec-panel needs `--output` added; the sandbox copy of the command (`command.md:23`) already lists `--output <file>`. Whether it is the same version as `cmd/spec-panel.md` is UNVERIFIED.

The session that ran this review would ask the user once whether to open an issue for the follow-up candidates; this sandbox run has no user channel, so none was asked and none was created.

## Coverage
Read in full: the candidate (all 294 lines), the README, `command.md`, the review-loop prompts file. Checked against the inventories: the `CAPS:` lines cited in sections 1 to 2 (44-52, 58-80, 84-103, 107-116, 128-130, 145-161, 178), `INV-A:14,35,38,45,51,60-66,76-98,106,113,118,120`, `INV-B:3,31,65,105,107,112,197-206,272,285-296,301,311,320,323`. All matched what the candidate attributes to them, except where noted above. Not checked (outside the workspace, UNVERIFIED): every `cmd/`, `sk/`, `agents/` line, `EVIDENCE.md`, the codegraph README, `install_core.py`, `Makefile`, `pyproject.toml` and `CLAUDE.md` citation. Not run: any command in section 7. Counts verified: 10 ready (`S:82-91`), 27 changed (`S:99-125`), 6 coordinator-only (`S:132-137`), total 43.

## Reviser brief
Blocking finding ids: B-1.
Rules (restated from the command's Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone.
B-1: change the WC-4 contract location for commands whose `--output` names a file (`S:62`, and the rows `S:87`, `S:90`, check `S:208` that repeat it) so two workers cannot share one contract path.

verdict: FAIL
