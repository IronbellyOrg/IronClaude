review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit of the final spec; first review of the full document, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full).

| Header field | Value |
|---|---|
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `284cc6b74e9164675f12bdb0a33d7d0c5edf49544b271cb956ec89ae5853237e` (60530 bytes, 288 lines) |
| baseline | none given (first review; nothing to compare) |
| reviewer model | claude-sonnet-5-5 (Sonnet 5.5) |
| mode / focus | critique / requirements, architecture (panel: Wiegers lead, Adzic, Cockburn; Fowler lead, Newman, Hohpe, Nygard; Whittaker active in every review) |
| brief clauses overridden | none |

Citation shorthand: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Every citation the spec makes into `src/...`, `CLAUDE.md` or `Makefile` points outside the workspace and is UNVERIFIED here; only citations into the three inventories and the README were checked.

## Coverage

- Read in full: the candidate (288 lines), `README`, `INV-A`, `INV-B`, `CAPS`, the review-loop prompts file, and `command.md`.
- Checked: every `INV-A:`, `INV-B:`, `CAPS:` and `README:` citation in the candidate resolves to the claimed content (spot-checked every cited range, all rows 3.1/3.2/4, all E/R rows; no wrong line found). Counts: 21 + 22 = 43; 7 + 30 + 6 = 43; phase assignment 12 (P1) + 15 (P2) + 4 (P3) + 3 (P4) from section 3 plus brainstorm and init-lite with no change = 37 + 6 coordinator-only = 43 (see Quantity Flow). The inventories' 10 / 27 / 6 split to the spec's 7 / 30 / 6 reconciles with the three stated moves (`SPEC:271`; `INV-A:73`, `INV-B:278`).
- Not checked (UNVERIFIED): all `src/superclaude/...`, `CLAUDE.md:N`, `Makefile:N`, `pyproject.toml:38`, `.dev/evals/...`, `.dev/codegraph-migration/...` citations; the spec's own claim to have re-read 340 citations (`SPEC:288`) and 11 locations (`SPEC:11`).
- Not run: no live Orca, no command was run; verdicts are from reading.
- Focus buckets covered: requirements (WC-1 to WC-12, SA-1 to SA-6, section 3 rows, section 7 acceptance checks, D1 to D5) and architecture (section 1 decision and rejected alternative, section 2 contract delivery, section 6 phasing, section 4 split).

## Blocking findings

### B-1: The WC-3 relay re-invocation is refused by the F-05 non-empty-directory rule

- Severity: MAJOR. Grading sentence: an implementer who follows the stated text as written builds a worker that, after a command wrote `status: blocked`, asks the coordinator (WC-3), then re-invokes the same command line plus the answer flag, and the command refuses the run because its `--output` directory already holds the blocked `return-contract.yaml`; the relay therefore never completes for any command with no resume flag, and the worker ends `failed` after a correct answer, which is wrong because WC-3 exists to let that answer be used.
- Experts: Nygard (sequence), Whittaker (Sequence Attack), Fowler.
- Evidence:
  - WC-2(c): blocked means "the command writes its report with `status: blocked` ... and stops" (`SPEC:60`).
  - WC-4: the contract is written "including stops before any other output exists" into `<output-dir>` (`SPEC:62`); so the blocked run leaves a non-empty directory.
  - WC-3: the worker session "may instead ask ... then re-invoke or resume the command with the answer as a flag" (`SPEC:61`); the only text about where the re-invocation writes is the brief's output directory (`SPEC:73`).
  - 2.3: "a command with no resume flag refuses a non-empty `--output` directory" in unattended mode and writes no contract (`SPEC:73`); AC-1.5 pins the refusal (`SPEC:199`).
  - Section 3 lists "fresh dir" as the resume for most gate commands (cli-eval `SPEC:101`, cleanup `SPEC:100`, improve `SPEC:108`, recommend `SPEC:114`, research `SPEC:115`, spec-panel `SPEC:119`, task `SPEC:120`, post-release `SPEC:112`, and others), so they have no resume flag and fall under the refusal.
- Concrete attack (Whittaker, state trace): `/sc:cli-eval run --unattended --output D` with no `--suite`. Before: D empty. Run 1: gate resolves blocked, `D/return-contract.yaml` written with `blocked_question`. Worker `ask`s, coordinator answers `suite=X`. Run 2: `/sc:cli-eval run --suite X --unattended --output D`. D is non-empty and cli-eval has no resume flag, so Run 2 refuses without writing a contract; `worker_done --outcome failed`. No section 7 check exercises WC-3, so nothing catches this (`SPEC:200-213`; see M-6).
- Priority: High. Quality impact: the question-relay path (WC-3, the spec's answer to the "questions go to the coordinator" rule at `README:35`) is unusable for every gate command except those with a real resume flag.

## Medium findings (warnings, not blocking)

Each is a requirement the document never states, or needs the implementer to pick between two readings the text allows.

### M-1: Acceptance checks AC-1.1 / AC-1.2 do not match the rows they apply to
- Experts: Wiegers, Crispin.
- AC-1.1 asserts every command in 3.1 and 3.2 has a `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`); AC-1.2 runs the full 7.2 check, including `test -s <contract>`, on "each P1 command" with `--output <dir>` (`SPEC:196`). But: `load` is a P1 command (`SPEC:159`) whose row says no report ("none (see note)"), "not as its own Task" (`SPEC:111`), and Decisions say a report file "would be an unrequested addition" (`SPEC:268`); `brainstorm` and `init-lite` are "Small fix: None" and 3.1 says "The only command changes are the small fixes" (`SPEC:79,84,85`), yet AC-1.1 needs a new section in both; `pr-submit` is in 3.2 while D3(a), the recommendation, says it runs only at the coordinator or person level (`SPEC:243`, `SPEC:139`) and section 4 says commands that never run as workers "get no `--unattended` mode" (`SPEC:128`). Reading choice: exclude those commands from the checks (likely intent) or force the edits. Recommendation: state the exclusions in AC-1.1/1.2.
- Priority: Medium.

### M-2: The contract location is undefined for several rows
- Experts: Fowler, Hohpe.
- WC-4 puts the contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (`SPEC:62`) and promises the path "known before dispatch" (`SPEC:73`). Rows where that does not resolve: tdd and init-lite take `--output <file>` (`SPEC:85,88`) and spec-panel and research gain `--output` with no kind stated (`SPEC:115,119`), so `<file>/return-contract.yaml` is impossible and AC-2.2 locates a tdd contract nowhere (`SPEC:203`); cleanup-audit and index-repo gain only `--slug` (`SPEC:107,110`) and rely on the generic "output flags for commands that lack one" (`SPEC:159`); implement writes "beside the ledger" at a run-time slug (`SPEC:106`; ledger path `INV-A:51`), the same problem the spec fixed for workflow with F-04 (`SPEC:125`, `SPEC:271`); tasklist (`SPEC:121`), review-translation (`SPEC:116`), cli-portify (`SPEC:102`), save (`SPEC:118`) give no contract directory. Recommendation: one sentence in WC-4 saying how `<output-dir>` is derived when `--output` is a file or absent.
- Priority: Medium.

### M-3: "Refused" is a fourth outcome outside the three WC-2 resolutions
- Experts: Wiegers, Whittaker (Divergence Attack).
- WC-2 allows default, caller flag, or blocked (`SPEC:60`). Rows also say a flag is "refused" under `--unattended`: `--mode socratic`, `--interactive`, `--format interactive`, `--monitor 1`, `--watch`, `--remediate`-style cases (`SPEC:99,100,105,108,113,117,122`). Not stated: whether a refusal writes a contract, with which `status`, and whether `blocked_question` is required (WC-4 requires a question when blocked, `SPEC:62`). Both plausible statuses map to `--outcome failed` (`SPEC:63`), so the coordinator outcome is the same; the contract content is not.
- Related: research "pins `--strategy planning`" (`SPEC:115`) but a caller may also pass `--strategy intent`; pin versus caller flag is unspecified.
- Priority: Medium.

### M-4: Wait-splitting threshold and its acceptance check disagree
- Experts: Nygard, Crispin.
- WC-10 splits only calls that block longer than 5 minutes into waits of at most 4 minutes (`SPEC:68`); the decision row gives 4 minutes as the margin (`SPEC:269`); AC-4.3 requires no single tool call over 240 s (`SPEC:213`). A single 280 s poll satisfies WC-10 as written and fails AC-4.3. Applies to pr-submit under D3(b) and cli-eval (`SPEC:101,113`); cli-eval has no check at all.
- Priority: Medium.

### M-5: AC-0.4 requires step 3 of the live check, which depends on a contract that does not exist in P0
- Experts: Crispin, Adzic.
- Step 3 passes only if the outcome "matches the contract's status" and the report path "is the WC-4 contract path" (`SPEC:182`). AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the existing report file since the contract arrives in P1" (`SPEC:194`). Per the rows, troubleshoot reports `REPORT.md` and adversarial writes under `<output>/adversarial/` (`SPEC:83,89`), so two of three smoke runs cannot meet step 3 literally; a failure "reopens section 1" (`SPEC:194`). Recommendation: restate step 3 for P0 against the existing report file.
- Priority: Medium.

### M-6: Worker-session duties are not tied to the brief and WC-3 / WC-12 have no acceptance check
- Experts: Cockburn, Fowler, Crispin.
- WC-3, WC-5, WC-7 and WC-12 are owned by "Worker session" (`SPEC:61,63,65,70`), but 2.3 lists what the brief carries and omits them (`SPEC:73`); WORKER-CONTRACT.md is read by commands through their `## Unattended mode` section (`SPEC:52`), not by the worker session, and P0 gives it only a brief template "listing the section 3.1 flags" (`SPEC:158`). No section 7 check covers WC-3 or WC-12 (`SPEC:166-213`); WC-7 is covered only by AC-0.4 step 5. Result: nothing states how the outcome mapping or the "never wrap in a subagent" rule reaches the worker.
- Priority: Medium.

### M-7: The `--unattended` token has no parse rule (sentinel collision)
- Experts: Whittaker (Sentinel Collision), Wiegers.
- D1(a) says the flag "cannot misfire on a person" (`SPEC:231`). The spec never says the token must be a standalone, unquoted argument. A topic such as `/sc:tdd "how --unattended mode works"` or quoted spec text containing the token has no stated treatment. The command definition under review here states that rule for itself, which shows the gap is real for the others.
- Priority: Medium.

### M-8: "No resume flag" is undefined for partially-resumable commands
- Experts: Nygard, Whittaker (Divergence Attack).
- adversarial (`--pipeline-resume`, pipeline mode only), brainstorm (`--resume-from`, dialogue only), reflect (`--promote-resume`, promotion only), release-split (`--resume-from`) are marked "fresh dir" for the uncovered part (`SPEC:83,84,86,87`). Whether F-05 refuses a non-empty directory for them is not stated; a run without the flag into a prior attempt's directory overwrites it, against WC-6 (`SPEC:64`). AC-3.2 expects roadmap (which has `--resume`) to "start fresh" in a directory that already holds `.session-memory.md` (`SPEC:208`).
- Priority: Medium.

### M-9: Authorization inputs and D4 sequencing
- Experts: Adzic, Nygard.
- WC-9 says outward actions turn on "only through the command's own explicit flag" (`SPEC:67`), but no flag is named for post-release (`SPEC:112`), task `commit`/`push` (`SPEC:120`) or the cli-eval "safety flags" (`SPEC:101`; their identity is not in `INV-A:44` either). Also P2 builds auggie-review `--post-pr` brief authorization and task's authorized-commit path (`SPEC:97,120`) although D4 governs both (`SPEC:247`) and "Phases 1-3 need no user decision" (`SPEC:154`). Under D4(b) the P2 work would be dead text; no harm results because the default stays off.
- Priority: Medium.

## Minor notes

- N-1: tasklist: `SPEC:121` says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit (`INV-A:14`)" and drops the inventory's recommendation that the per-phase reflect run at the worker's top level (`INV-B:215`; nested spawning UNVERIFIED at `INV-B:314`). No Decisions row records the override; with auto-accepted remediation the chain can go deeper than one layer.
- N-2: WC-5 maps "no report exists" to failed (`SPEC:63`) but not an empty, unparsable or status-less contract file; AC step 4 only checks it in tests (`SPEC:183`).
- N-3: WC-1 says a launch prompt must fall back "well inside" 60 s (`SPEC:59`) while the evidence gives about 45 s as the failure threshold (`CAPS:49`; `EVIDENCE.md:56`, UNVERIFIED here). A number would make it testable.
- N-4: SA-3 allows new report files "when the caller passes the new output flag" (`SPEC:148`) while WC-4 writes the contract only in unattended mode (`SPEC:62`) and SA-1 freezes standalone output paths (`SPEC:146`); whether `--output` alone writes a contract is open.
- N-5: SA-2 / AC-C1 forbid core files from naming an `orca` command (`SPEC:147,172`) while P0 adds an Orca section to `HOW-WE-WORK.md` (`SPEC:158`, `SPEC:150`). It can be written without those strings, but the grep is case-sensitive and does not cover the WC-8 verbs `worker-start`, `dispatch`, `task-create` (`SPEC:66`).
- N-6: AC-C5's `grep -E '^-[^-]'` misses a deleted line that itself begins with `-` (for example a removed `---` delimiter) (`SPEC:176`). Also SA-4's list of allowed existing-line edits (`SPEC:149`) omits the cli-eval and pr-submit wait-size edits (`SPEC:101,113`).
- N-7: `SPEC:264` cites "ladder rung 2" without defining the ladder.
- N-8: How a worker runs a `/sc:` command that arrives inside a preamble-prefixed task text (slash expansion versus the Skill tool) is not stated; P0's smoke runs would show it (`SPEC:158`, `SPEC:275`).

## Adversarial analysis (Whittaker)

| # | Attack | Invariant location | Triggering condition | Result |
|---|---|---|---|---|
| A1 | Sequence | WC-3 vs 2.3 (`SPEC:61,73`) | blocked, then re-invoke into the same directory | B-1 |
| A2 | Zero/Empty | WC-5 (`SPEC:63`) | contract file exists but is empty or lacks `status` | N-2 |
| A3 | Divergence | WC-10 vs AC-4.3 (`SPEC:68,213`) | one call of 241 to 300 s | M-4 |
| A4 | Sentinel Collision | D1(a) (`SPEC:231`) | `--unattended` inside quoted topic text | M-7 |
| A5 | Accumulation | 2.3 (`SPEC:73`) | two workers of one command in one worktree before `--slug` exists | spec forbids it in the coordinator brief; nothing enforces it; accepted as stated |
| A6 | Divergence | research pin vs caller flag (`SPEC:115`) | caller passes `--strategy intent` with `--unattended` | M-3 |

## Guard Condition Boundary Table

Guards: G1 non-empty output refusal (F-05); G2 outcome mapping (WC-5); G3 wait splitting (WC-10); G4 `--unattended` switch (D1); G5 refused person-mode flags (WC-2); G6 confidence < 0.70 (task); G7 outward default-off (WC-9). Classes left out are explained in the row that omits them.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 non-empty `--output` refusal | `SPEC:73`, `SPEC:199` | Zero/Empty | directory missing or empty | false | command writes into it | OK |
| G1 | `SPEC:73` | One/Minimal | only the prior blocked `return-contract.yaml` | true | refuse, no contract; collides with WC-3 relay | GAP (B-1) |
| G1 | `SPEC:73` | Typical | prior full run present | true | refuse, `worker_done --outcome failed` | OK |
| G1 | `SPEC:73` | Legitimate Edge Case | `--output` names a file (tdd, init-lite) | not a directory | not stated | GAP (M-2) |
| G1 | `SPEC:73` | Legitimate Edge Case | command with partial resume flag run without it | false (has a flag) | not stated | GAP (M-8) |
| G1 | | Maximum/Overflow, Sentinel | left out: no capacity or reserved value exists for a directory test | | | |
| G2 outcome mapping | `SPEC:63` | Zero/Empty | no report file | no report | `--outcome failed` | OK |
| G2 | `SPEC:63` | Zero/Empty | empty or unparsable file | | not stated | GAP (N-2) |
| G2 | `SPEC:63` | Typical | `succeeded` | | `--outcome succeeded` | OK |
| G2 | `SPEC:63` | Legitimate Edge Case | `partial`; audit verdict FAIL | | `succeeded`, status in first sentence | OK |
| G2 | `SPEC:63` | Sentinel Value Match | `blocked`; status outside the four values | | blocked is `failed`; unknown value not stated | GAP (N-2) |
| G3 wait splitting | `SPEC:68`, `SPEC:213` | Zero/Empty | no wait | false | none needed | OK |
| G3 | `SPEC:68` | Typical | 3 minutes | false | unsplit, allowed | OK |
| G3 | `SPEC:68`, `SPEC:213` | Legitimate Edge Case | 241 to 300 s | false under WC-10 | allowed by WC-10, fails AC-4.3 | GAP (M-4) |
| G3 | `SPEC:68` | Maximum/Overflow | 3600 s eval timeout (`INV-A:65`) | true | split into waits of at most 4 minutes | OK |
| G4 `--unattended` switch | `SPEC:51`, `SPEC:231` | Typical | standalone token | true | unattended mode | OK |
| G4 | `SPEC:231` | Sentinel Value Match | token inside quoted topic | | not stated | GAP (M-7) |
| G4 | | Zero/Empty | token absent | false | today's behavior (SA-1, `SPEC:146`) | OK |
| G5 refused person-mode flags | `SPEC:99,100,105,108,113,117,122` | Typical | `--watch`, `--interactive` etc. with `--unattended` | true | "refused"; contract status and content not stated | GAP (M-3) |
| G6 confidence < 0.70 | `SPEC:120` | Zero/Empty | 0 | true | blocked | OK |
| G6 | `SPEC:120` | Legitimate Edge Case | exactly 0.70 | false | proceeds (condition is "below 0.70") | OK |
| G6 | `SPEC:120` | Maximum/Overflow | 1.0 | false | proceeds | OK |
| G7 outward default-off | `SPEC:67` | Typical | no flag in brief | true | action off | OK |
| G7 | `SPEC:67`, `SPEC:112,120` | Legitimate Edge Case | brief authorizes post-release or task commit | false | flag name not defined | GAP (M-9) |

Every cell is populated; the GAP rows map to findings above (one blocking, the rest Medium or minor), so the table is complete and does not block synthesis (FR-10).

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

```text
[Commands in cmd/: 43] --> [Inventories: A 21 + B 22 = 43] --> [Spec section 3/4: 43]
   inventory verdicts: ready 10 / needs-change 27 / coordinator-only 6   (INV-A:73, INV-B:278)
   spec verdicts:      ready 7  / needs-change 30 / coordinator-only 6   (SPEC:76)
   3 moved ready -> needs-change (workflow, index-repo, cleanup-audit)   (SPEC:271)  -> conserved: 10-3 = 7, 27+3 = 30
[Phase assignment: P1 12 (3.2) + P2 11 (3.2) + P3 4 + P4 3 = 30 needs-change]
   + 3.1 ready commands with a phase fix: adversarial (P1), reflect, release-split, tdd, troubleshoot (P2) = 5
   + 3.1 ready commands with no change: brainstorm, init-lite = 2
   30 + 5 + 2 = 37 workers + 6 coordinator-only = 43   <-- no mismatch
```

No dimensional mismatch found.

## Follow-up candidates

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9 and N-1 to N-8 above. Medium and minor findings never trigger a revision or fail this review. This report was produced by a worker with no user present, so the once-per-loop question about opening an issue for them is left to the coordinator; no issue was created.

## Reviser brief

Revise only the text that blocking finding B-1 names; this section restates the contract the reviser reads instead of the command:

- Blocking finding ids: B-1.
- Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.
- Leave every Medium finding and minor note (M-1 to M-9, N-1 to N-8) alone; they are not part of this brief.
- Do not award yourself a PASS; a separate re-review decides.

verdict: FAIL
