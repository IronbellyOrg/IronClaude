review: 1 of 3

# Whole-document audit of the Orca worker-contract spec (/sc:spec-panel, critique mode)

## Header

| Field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| run kind | first review of the whole document (labelled whole-document audit of the final spec). No `--re-review`, no `--baseline` given. Prompt used: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `5d3d225a6ef33d0f0c3eb9b745dd4e780b4ca5a0b2dd745dd00ce966449d2b61` (58448 bytes, taken with `sha256sum` before review) |
| baseline sha256 | not applicable (first review) |
| reviewer model actually used | claude-sonnet-5-5 |
| format | critique-mode structure with the standard-format quality block |
| experts used | Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (adversarial, always active), Newman, Hohpe; Crispin only for guard-table completeness validation |
| citation shorthand | `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of the three inventory files, as the candidate defines them |

### What was covered, and what could not be checked

- Read in full: the candidate (286 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, `command.md`, and the review-loop prompts file.
- Checked against the inventories: every `INV-A`/`INV-B`/`CAPS` line number the candidate cites in sections 1, 2, 3, 4, 6 and the Decisions and UNVERIFIED lists. Each cited line exists and says what the candidate says it says. This includes the per-command row references (for example `INV-A:35-55`, `INV-B:31-52`, `INV-B:107-115`, `INV-A:60-61`) and the capabilities references (`CAPS:44-45`, `CAPS:97-103`, `CAPS:147-151`, `CAPS:155-161`, `CAPS:178-188`).
- Re-computed the arithmetic: 21 + 22 = 43 commands; ready 5 + 5 = 10, needs-change 13 + 14 = 27, coordinator-only 3 + 3 = 6; section 3.1 has 10 rows, section 3.2 has 27 rows, section 4 has 6 rows; the phase lists in `SPEC:158-162` cover all 37 commands that are not coordinator-only and brainstorm and init-lite are the only two with no edit (see the Quantity Flow Diagram). The "11 re-read locations" and "5 + 3 + 1 = 9 defects" counts also hold.
- UNVERIFIED (not checkable inside the sandbox, so not graded): every citation of `CLAUDE.md:*`, `src/superclaude/**` (including `install_core.py`, `HOW-WE-WORK.md`, skill and command files), `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/**`, `pyproject.toml`, `Makefile`, and the `orca-ide` guide output. Where the inventories quote those files, I relied on the inventory quote only. The candidate's own claims that an `evidence-validator` re-read about 340 citations (`SPEC:285`) is likewise unchecked.
- Issue offer: the command asks the user once whether to open an issue for the follow-up candidates. This run answers with `DONE <path>` only, so no question was asked and no issue was created.

## Quality assessment

```yaml
quality_assessment:
  overall_score: 7.0
  clarity: 8        # section numbering, evidence tables and citations are precise; a few undefined labels (N-02)
  completeness: 6.5 # contract location, refusal, blocked-resolution and propagation rules have gaps (A-01 to A-05, A-12)
  testability: 6.5  # most phases have checks, six requirements have none, three checks can pass for the wrong reason (A-09, A-10)
  consistency: 7    # no blocking contradiction found; several rows override a general rule silently (A-01, A-11, A-16)
blocking_findings: 0
medium_findings: 18
minor_notes: 7
```

## Guard Condition Boundary Table

Trigger: the spec contains conditional logic, thresholds, boolean guards and sentinel values (the `--unattended` switch, the 60 s readiness limit, depth 1, the 5 minute heartbeat and 4 minute wait, the 0.70 confidence gate, `status` values). Nygard built it, Crispin checked completeness, Whittaker attacked it. The six input classes are a menu: a class that cannot occur for a guard is left out and the reason is given in the note under the table. Every GAP row carries the id of the finding it generated (FR-8); every Specified Behavior cell is filled (FR-9); the table is complete before the synthesis below (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 `--unattended` switch | SPEC:51,146,228 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1, SPEC:146) | OK |
| G1 `--unattended` switch | SPEC:51,228 | Typical | standalone token `--unattended` | true | unattended mode (WC-2, SPEC:60) | OK |
| G1 `--unattended` switch | SPEC:228 | Sentinel Value Match | the text `--unattended` inside a quoted topic, e.g. `/sc:research "how --unattended works"` | ambiguous | none: no token-parsing rule is stated | GAP (A-13) |
| G1 `--unattended` switch | SPEC:73,158-162 | Legitimate Edge Case | flag sent to a command whose phase has not landed, or whose `~/.claude` copy is stale | n/a | spec says to pass it "once the command's phase has landed" but gives no way to tell | GAP (A-13) |
| G2 `<output-dir>` | SPEC:62 | Zero/Empty | `--unattended` with no output dir or flag | undefined | none: no refusal, default, or contract location is stated | GAP (A-01) |
| G2 `<output-dir>` | SPEC:62,87,90,200 | One/Minimal | `--output <file>` (tdd, init-lite, AC-2.2 passes a file) | undefined | none: "the directory the coordinator passed" is not a file | GAP (A-01) |
| G2 `<output-dir>` | SPEC:62 | Typical | a directory | true | `<dir>/return-contract.yaml` written on every outcome | OK |
| G2 `<output-dir>` | SPEC:62,64 | Maximum/Overflow | directory already holds attempt 1's `return-contract.yaml` (retry, `--resume`) | stale file present | none: no overwrite-first, run id or timestamp rule | GAP (A-02) |
| G2 `<output-dir>` | SPEC:62,84,92 | Sentinel Value Match | the file name `return-contract.yaml` already written there by a nested command | collision | none | GAP (A-12) |
| G2 `<output-dir>` | SPEC:83,92,109,85 | Legitimate Edge Case | adversarial `<output>/adversarial/`, workflow `.dev/tasks/to-do/<id>/`, implement beside the ledger, cleanup-audit fixed dir | row path differs from WC-4 path | the row path applies, but WC-4 says "the directory the coordinator passed" and does not say rows override it | GAP (A-01) |
| G3 WC-5 outcome | SPEC:63 | Zero/Empty | no report file exists | true | `--outcome failed` | OK |
| G3 WC-5 outcome | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G3 WC-5 outcome | SPEC:63,263 | One/Minimal | `status: partial` | true | `--outcome succeeded`, body states `partial` | OK |
| G3 WC-5 outcome | SPEC:63 | Legitimate Edge Case | `status: blocked`, or an audit with verdict FAIL | true | blocked gives `failed`; audit FAIL gives `succeeded` | OK |
| G3 WC-5 outcome | SPEC:62,261 | Sentinel Value Match | an existing contract whose `status` uses other words than the four-value set | unverified | none: spec says existing contracts "keep their fields" and never lists their values | GAP (A-08) |
| G4 WC-10 wait split | SPEC:68 | Typical | single tool call of 3 minutes | false | no split needed | OK |
| G4 WC-10 wait split | SPEC:68 | Legitimate Edge Case | single call of 4.5 minutes | false (not "longer than 5") | no split required although the cap elsewhere in the same row is 4 minutes | GAP (N-07) |
| G4 WC-10 wait split | SPEC:68,104 | Maximum/Overflow | cli-eval run of 3600 s | true | waits of at most 4 minutes | OK |
| G4 WC-10 wait split | SPEC:114,283 | Legitimate Edge Case | pr-submit poll iteration runtime unknown | unverified | declared UNVERIFIED #12 and tested by AC-4.3 | OK |
| G5 WC-3 `ask` | SPEC:61 | Zero/Empty | coordinator never answers | question stays pending | "resumes the same message ID"; no upper bound and no fallback to the blocked outcome | GAP (A-04) |
| G5 WC-3 `ask` | SPEC:61 | Typical | answer arrives | true | re-invoke or resume with the answer as a flag | OK |
| G5 WC-3 `ask` | SPEC:61,60 | Legitimate Edge Case | session has no preamble | false | gate resolves as blocked (WC-2 c) | OK |
| G6 task confidence | SPEC:121 | Typical | 0.65 | true | resolves as blocked | OK |
| G6 task confidence | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | command proceeds | OK |
| G6 task confidence | SPEC:121 | Zero/Empty | 0.00 | true | resolves as blocked | OK |
| G7 nesting depth | SPEC:33,66 | Typical | depth 1 (this machine) | true | `worker-start` from a worker is refused; commands never call it | OK |
| G7 nesting depth | SPEC:66,252 | Legitimate Edge Case | depth raised (D5 b) | false | WC-8 still forbids commands calling `worker-start`, `dispatch`, `task-create` | OK |
| G8 person-mode flag under `--unattended` | SPEC:100,102,103,108,110,114,118,123 | Legitimate Edge Case | `--interactive`, `--mode socratic`, `--format interactive`, `--watch`, `--monitor 1` | true | "refused": no status, contract content or exit behaviour is defined | GAP (A-03) |
| G9 WC-9 outward default | SPEC:67,100 | Typical | auggie-review PR posting | default on today | off under `--unattended`; on only with an explicit `--post-pr` in the brief | OK |
| G9 WC-9 outward default | SPEC:67,113,121 | Legitimate Edge Case | task `commit`/`push`, post-release VM, install, commit, PR (no flag exists) | true | "off unless the brief authorizes"; the authorizing flag is not named | GAP (A-05) |
| G10 cleanup/improve classification | SPEC:103,110 | Typical | item the file lists as auto-fix | true | applied | OK |
| G10 cleanup/improve classification | SPEC:103,110 | Legitimate Edge Case | item the file marks "If unsure, prompt user" (INV-A:43) | unclear | none: neither the auto-apply list nor the "Approval Required" list covers it | GAP (A-07) |
| G11 WC-11 write collision | SPEC:69 | Typical | per-session or timestamped path | false | no collision | OK |
| G11 WC-11 write collision | SPEC:69,85,86,115 | Maximum/Overflow | two or more workers, one worktree, fixed paths (index-repo, init-lite default, cleanup-audit) or source edits | true | "must never write the same file"; only cleanup-audit gets a constraint note | GAP (A-14) |

Classes left out: G1 Maximum (a boolean has no capacity); G4 Zero (a zero-length wait is not a step); G5 Sentinel and G6 Sentinel (the row names no sentinel); G7 Zero (depth 0 is the coordinator, which is allowed to start workers by definition, `CAPS:97`); G8 and G9 Zero/Maximum (a flag is present or not); G10 Maximum (no count limit exists); G11 Zero (nothing is written).

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered: the rollout (`SPEC:158-162`) is a multi-stage flow whose stage counts differ from the input count, and the requirements-to-checks mapping (`SPEC:57-70` to `SPEC:170-210`) is a second one. Fowler annotated counts, Whittaker attacked each divergence.

```text
[Source: 43 commands in cmd/ (INV-A:3 = 21, INV-B:3 = 22)]
   --> [Classify: SPEC:78-137]
        |-- 10 ready (3.1)             --> [no edit: 2 = brainstorm, init-lite]
        |                                   [P1 small fix: 4 = adversarial, cleanup-audit, index-repo, workflow]
        |                                   [P2 gate edit: 4 = reflect, release-split, tdd, troubleshoot]
        |-- 27 needs change (3.2)      --> [P1: 9]  [P2: 11]  [P3: 4]  [P4: 3]
        |-- 6 coordinator-only (4)     --> [no edit, no --unattended]
   P1 total 13, P2 total 15, P3 total 4, P4 total 3 = 35 edited; 35 + 2 + 6 = 43   (conserved)

[Requirements: WC-1..WC-12 = 12] --> [Acceptance checks that name the requirement or test it directly]
   WC-2 (AC-2.2), WC-4 (7.2 step 4), WC-5 (7.2 step 3), WC-7 (AC-0.4 only), WC-8 (AC-C1), WC-9 (AC-2.4, AC-4.2)  = 6 covered
   WC-1, WC-3, WC-6, WC-10 (only pr-submit, AC-4.3), WC-11 (only save, AC-3.4), WC-12 = 6 not covered or covered for one command only
   <-- MISMATCH 12 in, 6 out; consumers (phase gates) assume every requirement is checked   (A-09)

[Worker lifecycle: 1 Task --> 1 worker --> exactly 1 worker_done --> 1 contract file read by coordinator]
   retry (`--retry-of`) --> 2nd contract in same dir when no fresh dir        <-- MISMATCH 1 contract expected, 2 present   (A-02)
```

Consistency Check: the command-count flow conserves (no dimensional mismatch). The two other flows show real divergences, graded in A-09 and A-02. Neither is graded CRITICAL: FR-19 says a mismatch is CRITICAL, but the grading rule of the Review Loop (consequence, not label) applies, and neither names a concrete wrong outcome that follows with no further assumption (A-02's stale-file outcome needs a crash after a resume, A-09 is a test gap, not a stated text that does harm).

## === REQUIREMENTS ANALYSIS ===

Blocking findings: none. Every finding below was put through the grading check ("An implementer who follows the stated text as written builds X, and X is wrong because Y"). Each one needed an assumption that the implementer picks the worse of two readings the text allows, or is a requirement the document never states. So each is Medium although its label may read MAJOR.

### A-01 | label MAJOR, graded Medium | Wiegers, Cockburn | contract location rule (`SPEC:62`, `SPEC:83-92`, `SPEC:109`, `SPEC:200`)
- Issue: WC-4 says the contract is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", so "the report path is known before dispatch" (`SPEC:73`). Four stated places do not fit that rule.
  - Row paths differ: adversarial `<output>/adversarial/return-contract.yaml` (`SPEC:83`), workflow `.dev/tasks/to-do/<id>/return-contract.yaml` with an id only known at run time (`SPEC:92`), implement "beside the ledger `progress.md`" (`SPEC:109`), cleanup-audit with a fixed `.claude-audit/` and no contract (`SPEC:85`).
  - `--output` is a file for tdd (`SPEC:90`) and init-lite (`SPEC:87`), and AC-2.2 passes `--output <file>` (`SPEC:200`); a directory is then never passed.
  - Nothing says what a command does when `--unattended` is given with no output location (`SPEC:62`, "including stops before any other output exists").
  - The workflow pre-creation STOP fix (`SPEC:92`) names no location, because the package directory does not exist yet (`INV-B:272`).
- Grading sentence: an implementer who follows WC-4 literally for adversarial writes `<output-dir>/return-contract.yaml` while the row and AC-1.4 (`SPEC:198`) fix `<output>/adversarial/...`. The worker then looks at one path, finds nothing, and WC-5 (`SPEC:63`, "or no report exists") sends `--outcome failed` for a run that succeeded. That outcome needs the guess that the worker reads WC-4's path and not the per-command section (`SPEC:52` says each command's section names its own report file), so Medium.
- Recommendation: state once that a row's report file overrides the WC-4 default; say what `<output-dir>` means for a file-valued `--output`; give the no-output-location case one defined outcome; name where the workflow pre-creation contract goes. Priority High (of the Medium group). Quality impact: completeness +1, consistency +0.5.

### A-02 | label MAJOR, graded Medium | Nygard, Hohpe | stale or ambiguous contract (`SPEC:62`, `SPEC:64`)
- Issue: WC-6 says a command without a resume flag "writes each run into a fresh output directory" (`SPEC:64`; about 20 rows in section 3.2 say "fresh dir"), while WC-4 puts the contract in the directory the coordinator passed. Read literally, a command that makes its own fresh subdirectory writes the contract somewhere the coordinator did not name; read the other way, WC-6 asks nothing of the command, because only the coordinator can make the directory fresh and section 2.3 (`SPEC:73`) never tells it to. Separately, the contract has no `run_id`, `dispatch_id` or timestamp (`SPEC:62` lists `status`, `command`, `report_path`, `artifacts`, `blocked_question`), and resumable commands (brainstorm `--resume-from`, tdd `--resume`, pr-submit `--resume`, implement `--resume`) reuse a directory.
- Grading sentence: a retry worker that resumes into attempt 1's directory and stops before rewriting the file leaves attempt 1's `status` in place, and the coordinator reads it as the new result. That needs a crash or early stop after the resume plus a coordinator that does not compare timestamps, so Medium.
- Recommendation: say who makes the directory fresh (the brief, per attempt), and require the command to write the contract file first and overwrite it last, with a correlation field (the Dispatch id is in the worker's preamble, `SPEC:73`). Priority Medium. Quality impact: testability +0.5.

### A-03 | label MAJOR, graded Medium | Wiegers | "refused" has no defined outcome (`SPEC:60`, `SPEC:62`; rows `SPEC:100`, `102`, `103`, `108`, `110`, `114`, `118`, `123`)
- Issue: WC-2 gives three resolutions (default, caller flag, blocked); WC-4 makes `blocked_question` mandatory for blocked. Seven rows say a person-mode flag is "refused" under `--unattended`. A refusal of `--watch` or `--monitor 1` is not a question, so `blocked_question` has nothing true to hold, and `failed` is the only other status that fits, but no row says it.
- Grading sentence: an implementer builds a refusal that writes `status: blocked` with an invented question or `status: failed` with none; both pass WC-5, and AC-2.2 (`SPEC:200`) requires a non-empty `blocked_question` only for gate hits. The wrong outcome is a coordinator that retries a refusal as if it were an answerable question; that needs a coordinator that acts on `blocked` automatically, so Medium.
- Recommendation: define "refused" as `status: failed` with a reason field, or as a fourth resolution in WC-2. Priority Medium.

### A-04 | label MAJOR, graded Medium | Cockburn, Adzic | the blocked path has no second half (`SPEC:60-61`, `SPEC:105`, `SPEC:113`, `SPEC:117`, `SPEC:120`)
- Issue: the use case stops at "write the report with `status: blocked` and stop". It never says what the coordinator does next (section 2.3, `SPEC:73`, lists only what the brief carries and "open the report file"), and the answer-carrying flags are not named for several gates: cli-portify's three approval gates have only a new `--resume` (`SPEC:105`), review-translation needs "a pre-confirmed context input" (`SPEC:117`), post-release "an explicit pre-tag choice" (`SPEC:113`), spec-panel "`target_release` ... as a flag" (`SPEC:120`). A cli-portify run resumed with `--resume` meets the same approval gate again, and nothing says that `--resume` counts as the approval. WC-3 (`SPEC:61`) lets the worker wait with `ask` and has no upper bound or fallback to blocked, and a blocked Task is retried by the coordinator with no cap (a worker's own `failed` report does not trip the 3-failure breaker, `CAPS:80`).
- Grading sentence: an implementer builds `--resume` that re-enters the gate; each retry ends blocked again. That needs the guess that the resume flag does not itself carry the approval, so Medium.
- Recommendation: add one use-case extension for the coordinator (read `blocked_question`, get the answer, rerun with the named flag, stop after N tries) and name the flag for each gate the rows list. Priority High (of the Medium group).

### A-05 | label MAJOR, graded Medium | Wiegers | WC-9 needs a flag that does not exist for some actions (`SPEC:67`, `SPEC:113`, `SPEC:121`, `SPEC:244-247`)
- Issue: WC-9 turns an outward default on "only through the command's own explicit flag written in the brief". Task's `commit`/`push` are EXEMPT keywords, not flags (`INV-B:204`), and post-release's authorization today is "unless the user pre-authorized them this session" (`INV-B:79`), a conversational rule. D4 lists both as authorizable by a brief (`SPEC:244`) and the rows say "unless the brief authorizes" without naming a flag. Also `--post-pr` (`SPEC:100`) is a positive flag; the inventory only shows `--no-post-pr` (`INV-A:38`, `cmd/auggie-review.md:52`), so its existence is UNVERIFIED.
- Grading sentence: an implementer cannot build "off unless the brief authorizes" for task commit/push without inventing a flag name or parsing prose in the brief. Those rows sit in P4 (post-release) and P2 (task), and D4 is still open, so the cost is a missing requirement, not a stated text that does harm: Medium.
- Recommendation: name the authorizing flag per action (or say the brief text itself is the mechanism and how it is matched). Priority Medium.

### A-06 | label MAJOR, graded Medium | Nygard, Wiegers | the swarm replacement path skips the go-ahead (`SPEC:137`, `SPEC:67`, `SPEC:244`)
- Issue: swarm-wizard is coordinator-only because of "an explicit go-ahead before a real-model run" (`SPEC:137`; `INV-B:189`, real-model proxy runs `INV-B:194`). The "what the coordinator does instead" cell is "Dispatches a worker that runs `uv run superclaude swarm run ...` with explicit flags, which needs no wizard", with no authorization requirement. WC-9 lists "a paid external run" among outward actions (`SPEC:67`) but binds only commands, and D4's affected list omits it (`SPEC:244`).
- Grading sentence: a coordinator author follows the cell and dispatches a paid real-model run without the user's go-ahead. The harm needs the assumption that the user's request to the coordinator did not already authorize it, so Medium (a missing restriction).
- Recommendation: say the same authorization rule as D4(a) applies to the CLI path. Priority Medium.

### A-07 | label MAJOR, graded Medium | Nygard, Whittaker | unattended cleanup and improve rely on a classification the file does not complete (`SPEC:103`, `SPEC:110`; `INV-A:43`)
- Issue: the rows say apply "only items the file already allows without approval" and list "Approval Required" items. The files also say "If unsure, prompt user" (`cmd/cleanup.md:116-127` per `INV-A:43`). An unsure item is in neither list.
- Grading sentence: an implementer applies an item the command was unsure about because it is not in the "Approval Required" list. Whether the implementer treats unsure as approval-required is a guess between two readings, and rollback is UNVERIFIED (`SPEC:103`), so Medium.
- Recommendation: add "unsure counts as Approval Required" to both rows. Priority Medium (touches edits to product files).

### A-08 | label MAJOR, graded Medium | Newman, Wiegers | existing contracts' `status` values were never compared with the four-value set (`SPEC:62`, `SPEC:261-262`)
- Issue: WC-4 says commands with a contract "keep their fields and add the missing ones", yet fixes `status` to `succeeded|partial|failed|blocked`, and the live check asserts exactly that set (`SPEC:183`). The inventories show workflow's contract has a `status` field (`INV-B:272`) and name reflect's, brainstorm's and adversarial's contracts, but list no `status` values for any of them. The Decisions row ("reuse `return-contract.yaml`", `SPEC:261`) treats the files as compatible without a check, and this is not in the UNVERIFIED list.
- Grading sentence: if reflect or workflow uses other words for `status`, the unchanged field either breaks the check at `SPEC:183` or the command must change an existing field, which SA-4 (`SPEC:149`) treats as a defect fix only where section 3 names one. It needs the premise that the vocabularies differ, which nothing shows, so Medium.
- Recommendation: list the four existing `status` vocabularies, or add the check to UNVERIFIED. Priority Medium.

### A-09 | label MAJOR, graded Medium | Crispin, Wiegers | six requirements have no acceptance check, or one for a single command (`SPEC:57-70`, `SPEC:170-210`)
- Issue: see the Quantity Flow Diagram. WC-1 (only the generic `state: ready` of 7.2 step 1), WC-3 (nothing tests ask, wait, resume), WC-6 (nothing tests `--retry-of` against a first attempt), WC-10 (only pr-submit, AC-4.3; cli-eval's split wait has no check), WC-11 (only save, AC-3.4), WC-12 (nothing tests `check` or `consumer_fenced`).
- Grading sentence: the stated checks can all pass while a retry overwrites attempt 1's output or a cli-eval wait blocks for 40 minutes without a heartbeat. This is a requirement without a check, not a stated text that does harm, so Medium.
- Recommendation: one check per uncovered requirement, or mark the requirement as not tested in this run. Priority Medium.

### A-10 | label MAJOR, graded Medium | Crispin, Whittaker | three checks can pass for the wrong reason (`SPEC:181`, `SPEC:200`, `SPEC:206`)
- Issue 1: AC-3.3 passes when `test -d` finds the default target of validate-tests (`SPEC:206`); the defect is that `tests/sc-task/` holds no specs (`INV-B:265`), and `mkdir tests/sc-task` passes the check while validating nothing.
- Issue 2: 7.2 step 2 passes when `agentWait` is "never non-null" (`SPEC:181`), but the inventory says a null or absent `agentWait` is absence of observation, not proof of no wait (`CAPS:125`, `CAPS:129`). Step 3 (a `worker_done` must arrive) catches a real stall, so the damage is only a weaker signal.
- Issue 3: AC-2.2 requires `worker_done --outcome failed` at a gate (`SPEC:200`), but WC-3 lets the worker `ask` instead (`SPEC:61`, "may"); a worker that follows WC-3 fails the check while obeying the spec, unless the test brief forbids `ask`, which no text says.
- Grading sentence: an implementer who creates an empty directory satisfies AC-3.3 as written. It is a weak check, not a stated text that does harm: Medium.
- Recommendation: AC-3.3 should count spec files in the target; AC-2.2 should say its brief forbids `ask`; step 2 should be described as a supplement to step 3. Priority Medium.

### A-11 | label MINOR-to-MAJOR, graded Medium | Cockburn, Fowler | rollout text disagrees with its own rows (`SPEC:43`, `SPEC:158-159`, `SPEC:195-196`)
- Issue 1: section 1.4 says "Phase 0 therefore starts with live smoke runs" (`SPEC:43`), the P0 row lists the builds first and says "Then run three ready commands" (`SPEC:158`), and its "Why this order" cell says the smoke runs "test the decision before anything is built on it". The three texts give two orders.
- Issue 2: P1 says "No person gate is involved, so each change is mechanical" (`SPEC:159`), but its commands include business-panel (`--mode socratic` refused, `SPEC:102`), explain (`--format interactive` refused, `SPEC:108`), index (knowledge-base mode, `SPEC:111`) and test (`--watch` refused, `SPEC:123`), which are gate resolutions the spec elsewhere assigns to P2 (`SPEC:160`, "F-1").
- Issue 3: AC-1.1 and AC-1.2 test "every command in the P1 row" (`SPEC:195-196`); the row also lists "fixes to adversarial, cleanup-audit, index-repo, workflow". Index-repo takes no `--output` or `--unattended` (`SPEC:86`), so counting it makes AC-1.2 impossible, and nothing says to leave it out.
- Grading sentence: an implementer who starts P0 with the builds and then smoke-tests discovers a failed decision after the work the smoke test was meant to protect. That needs the reader to choose the "Then" order, so Medium.
- Recommendation: one order for P0; one sentence for P1's scope; AC-1.1/1.2 name their command lists. Priority Low.

## === ARCHITECTURE ANALYSIS ===

### A-12 | label MAJOR, graded Medium | Fowler, Hohpe, Whittaker (Sentinel Collision) | no propagation rule for nested invocations (`SPEC:122`, `SPEC:84`, `SPEC:69`, `SPEC:104`)
- I can break this specification by **Sentinel Collision**. The invariant at **WC-4 and WC-2** (one `return-contract.yaml` per run, no prompts) fails when **a command invokes another command or skill and the spec says nothing about passing `--unattended` or `--output` down**. Concrete attack: before state, directory `D` holds nothing. cli-eval `create` runs `/sc:spec-panel` and adversarial (`INV-A:44`: "create W3 runs sc:adversarial-protocol", "create W2 runs /sc:spec-panel"). If the parent passes `--unattended --output D` to the child, the child writes `D/return-contract.yaml` and the parent's own contract (also `D/return-contract.yaml`, `SPEC:104`) overwrites it or is overwritten; if the parent passes nothing, the child asks its own questions (spec-panel asks for `target_release` on a TDD input, `INV-B:179`). After state: one contract file, wrong owner, or a stalled child.
- Only two propagation rules exist: tasklist passes `--unattended` to reflect (`SPEC:122`) and tdd resolves its nested `/task` asks (`SPEC:90`). The same question applies to release-split to brainstorm and adversarial (`INV-B:121`), reflect Mode A merge to adversarial (`INV-B:111`), brainstorm Wave 4 to tasklist or task-builder (`INV-A:39`), workflow to reflect (`SPEC:92`) and roadmap's per-wave `sc:save` (`INV-B:154`), which writes the single-owner keys WC-11 says unattended runs must not write (`SPEC:69`, `SPEC:119`).
- Grading: no stated text is wrong; the rule is never stated. Medium. Recommendation: one rule in WORKER-CONTRACT.md for nested calls (propagate the flag, give each child its own subdirectory) and a list of the nested pairs. Priority High (of the Medium group).

### A-13 | label MAJOR, graded Medium | Fowler, Newman, Whittaker (Sequence Attack) | the switch has no parsing rule and no capability probe (`SPEC:51`, `SPEC:73`, `SPEC:158-162`, `SPEC:228`)
- I can break this specification by **Sequence Attack**. The invariant at **section 2.3** (the brief includes `--unattended` "once the command's phase has landed") fails when **the coordinator's installed `~/.claude` copy of a command predates its phase**. Concrete attack: the repo has landed P1; the machine's `~/.claude/commands/sc/build.md` is the old copy (install is a separate step, `SPEC:52`). The brief says `/sc:build --unattended --output D`. Before: no contract exists. The old command treats `--unattended` as unknown, ignores it or errors, may prompt, and writes no contract; the worker ends with "no report exists" and `failed`, or stalls with `agentWait` set.
- Same area, Sentinel Collision: D1(a) says the flag is "testable by grep and cannot misfire on a person" (`SPEC:228`), yet a quoted topic that contains the token (`/sc:research "how --unattended works"`) is not covered; no text says the token must be a standalone argument.
- Grading: both need an assumption (stale install; a user quoting the token), and the spec states neither as a requirement: Medium. Recommendation: say how the coordinator learns a command is converted (for example grep the installed file for `## Unattended mode`), and that the switch is a standalone unquoted token. Priority Medium.

### A-14 | label MAJOR, graded Medium | Fowler, Whittaker (Accumulation Attack) | WC-11 is a promise commands cannot keep for source edits (`SPEC:69`, `SPEC:73`, `SPEC:85-86`, `SPEC:103`, `SPEC:110`, `SPEC:115`)
- I can break this specification by **Accumulation Attack**. The invariant at **WC-11** ("Two workers in one worktree must never write the same file") fails when **N workers run edit-capable commands (cleanup, improve, document inline mode, test `--fix`, implement) in the shared worktree that Orca uses by default** (`CAPS:115`). Concrete attack: workers A and B both run cleanup on overlapping directories; both edit one file; state before: file content X; after: A's edit lost or merged by chance. The only mitigation written is the owner column "Command" (default output paths, timestamps); only cleanup-audit gets a note that one audit per worktree is allowed (`SPEC:85`), index-repo's fixed `PROJECT_INDEX.md` (`SPEC:86`) and init-lite's default report (`SPEC:87`) get none. Section 2.3 lists "the worktree placement" but gives no rule for when parallel edits need separate worktrees.
- Grading: a missing restriction, no stated text that does harm: Medium. Recommendation: give the coordinator a rule (disjoint file scope in the brief, or one worktree per editing worker) and list the fixed-path commands in WC-11. Priority Medium.

### A-15 | label MAJOR, graded Medium | Nygard, Fowler | tasklist's nested fan-out is declared safe although the inventory left it open (`SPEC:122`, `INV-B:209-210`, `INV-B:314`, `INV-B:322`)
- Issue: the tasklist row says "none (its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`)". Inventory B marked the same point UNVERIFIED twice ("UNVERIFIED whether nested spawning works", `INV-B:210`; item 1, `INV-B:314`) and noted that tdd avoids exactly this nesting (`INV-B:210`, `sk/tdd/SKILL.md:238`). The reflect subagents also spawn their own agents (Tier 1: 2 plus a reuse-auditor; Tier 2: 2-3 reviewers, `INV-B:111`), so the depth is more than "one layer". The spec's UNVERIFIED list has no matching item. Further, Stage 10.5 says `needs_human_decision` items HALT (`INV-B:209`); under `--unattended` nothing says that HALT becomes `blocked`.
- Grading sentence: an implementer builds Stage 10.5 as the row says; if nested spawning fails, the reflect step produces nothing, and the row's "none" hides it. That needs the nested spawn to fail, which nothing shows (the docs allow three layers, `INV-A:14`), so Medium.
- Recommendation: add the item to UNVERIFIED and let AC-2.3 name it; define the HALT mapping. Priority Medium.

### A-16 | label MAJOR, graded Medium | Fowler, Cockburn | section 4 rationale contradicts later sections (`SPEC:133-134`, `SPEC:241`, `SPEC:244-247`)
- Issue 1: the git row says the coordinator "runs git itself, only when the user asked; workers make no commits or pushes" and cites `README.md:31`. That README line is a rule for this planning run ("Rules for every worker", `README.md:29-31`), not standing policy. D3(b) and D4(a) then allow a worker to commit and push (pr-submit pushes, task EXEMPT `commit`/`push`, post-release commit/PR). The two texts give opposite answers for pr-submit under D3(b).
- Issue 2: the help row says a worker "would return nothing the coordinator can read" (`SPEC:134`), but the coordinator can read a worker's transcript (`CAPS:131`, `worker-read`) and the spec itself uses that in 7.2 step 5 (`SPEC:184`). The coordinator-only verdict for help stands on "adds nothing", not on invisibility.
- Grading sentence: an implementer reading the git row forbids every commit in worker mode and so blocks the authorized D4(a) cases. Section 4 is rationale, not a requirement, so the conflict does not decide behaviour without a guess: Medium.
- Recommendation: replace the absolute sentence with "workers commit or push only when D4 authorizes it"; reword the help cell. Priority Low.

### A-17 | label MAJOR, graded Medium | Nygard | D3(b) hides a stated Will Not of pr-submit (`SPEC:114`, `SPEC:238-242`; `INV-B:90`)
- Issue: the pr-submit command says "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`, per `INV-B:90`). Row `SPEC:114` and D3(b) turn it into a worker that runs under `--unattended` with blocked-on-HALT, but neither names that Will Not or says it is lifted.
- Grading sentence: an implementer who picks D3(b) builds a worker mode that contradicts a Will Not still written in the command. It only arises if the user picks (b), which the spec does not recommend, so Medium.
- Recommendation: if D3(b) stays on the page, list the Will Not as a line to change. Priority Low.

### A-18 | label MAJOR, graded Medium | Newman, Crispin | a common check can fail the spec's own P0 deliverables (`SPEC:147`, `SPEC:158`, `SPEC:172`)
- Issue: AC-C1 greps `src/superclaude/core` for `orca ... orchestration|worktree|terminal|agent` and must print nothing, every phase including P0. SA-2 allows "the only allowed mention of Orca ... as an example of a caller's question channel inside the contract file" (`SPEC:147`); P0 puts WORKER-CONTRACT.md and "an Orca section" of HOW-WE-WORK.md in `src/superclaude/core` (`SPEC:158`), and the exclusion list holds only `skills/ccsession-tag/`. The routing guide's Orca section is about how a coordinator starts workers, which naturally contains such command text. Also the grep matches four subcommands only (`orca status`, `orca open` slip through), so "none requires Orca" is not fully checked.
- Grading sentence: if the P0 text names `orca orchestration ask`, AC-C1 fails in P0. That depends on how the text is worded, so Medium.
- Recommendation: exclude WORKER-CONTRACT.md and the routing guide from AC-C1, or limit SA-2's exception to wording that does not match. Priority Low.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Five methodologies were applied to the guards in the table. Findings that reach the spec's text are the ones above; the table maps each attack to them.

| Methodology | Finding | Severity (graded) | Where recorded |
|---|---|---|---|
| FR-2.1 Zero/Empty | `--unattended` with no output location; `--output` that is a file | Medium | G2, A-01 |
| FR-2.2 Divergence | WC-3 `ask` and WC-2(c) blocked both apply when a preamble exists; AC-2.2 forbids the first | Medium | G5, A-04, A-10 |
| FR-2.3 Sentinel Collision | `--unattended` inside quoted text; `return-contract.yaml` reused by a nested command | Medium | G1, G2, A-12, A-13 |
| FR-2.4 Sequence | flag sent before the command's phase is installed; P0 build-then-test versus test-first; `--resume` re-entering an approval gate | Medium | A-04, A-11, A-13 |
| FR-2.5 Accumulation | N parallel workers in one worktree; repeated blocked retries with no cap; fresh directory per attempt with no cleanup | Medium | A-04, A-14 |

I could not construct a CRITICAL attack: every invariant I broke needed an extra condition (a crash, a stale install, a user quoting a token, an unrecommended option picked).

## Consensus and disagreements

- Consensus: the decision (Orca on top, commands as units of work), the 10/27/6 split, the phase partition and the per-row evidence are sound and internally consistent where I could check them. The rejected alternative (commands calling Orca) is supported by `CAPS:97-103`, `CAPS:145-150`.
- Wiegers and Fowler agree the weakest part is the contract's boundary (where the file is, who owns freshness, what refused/blocked mean), not the per-command rows.
- Disagreement (not resolved by the panel): Nygard would grade A-02 and A-04 as blocking once D2-D4 are decided, because blocked retries with stale contracts are a likely operating failure; Cockburn and Crispin hold that each still needs a crash or a wrong guess, so by the grading rule they stay Medium.

## Follow-up candidates

Medium (warnings; never trigger a revision): A-01, A-02, A-03, A-04, A-05, A-06, A-07, A-08, A-09, A-10, A-11, A-12, A-13, A-14, A-15, A-16, A-17, A-18.

Minor notes:
- N-01: section 1.4 (2) states as fact that a command's `AskUserQuestion` "comes after readiness" and so cannot fail `worker-start` (`SPEC:44`). The only evidence is a pre-launch wrapper question (`EVIDENCE.md:39` via `CAPS:49`), and for Claude the task is passed on the command line (`CAPS:47`), so whether an immediate question delays readiness is untested. Inventory A states the opposite concern (`INV-A:17`). Not in the UNVERIFIED list. No behaviour changes (WC-2 removes the prompts anyway).
- N-02: undefined labels in the final text: "F-1", "F-2", "F-3" (`SPEC:73`, `76`, `159`, `176`, `193-196`) point to findings of the earlier review (`review/spec-panel.md`, not part of this document); "ladder rung 2" (`SPEC:261`) is never defined; UNVERIFIED item 14 (`SPEC:285`) is a note, not an unverified item.
- N-03: the contract has no schema version, although workflow's is "contract 1.1" (`INV-B:272`). A later change to the fields has no way to be told apart from this one.
- N-04: E3 cites `invocation_method: "skill-direct"` as support for the decision (`SPEC:23`), while section 1.4 (1) says the same run proves only the Agent-tool route (`SPEC:43`). `INV-A:13` reads `skill-direct` as the direct route. The spec should say which reading it takes.
- N-05: all citations outside the three inventories and the README could not be checked (see Header); the "evidence-validator re-read about 340 citations" statement (`SPEC:285`) is unchecked.
- N-06: the existence of a positive `--post-pr` flag is assumed (`SPEC:100`, `SPEC:67`); the inventory shows only `--no-post-pr` (`INV-A:38`).
- N-07: WC-10 triggers a split for a call "longer than 5 minutes" and then caps the waits at 4 minutes (`SPEC:68`); a call of 4 to 5 minutes is neither required to split nor within the cap (guard G4). The heartbeat cadence makes it harmless; the sentence should say which number governs.

## Reviser brief

None. No blocking finding is open, so no revision is requested. (Restated rule for any later use: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings are never edited under this loop.)

Coverage: whole-document first review of the candidate, all nine sections, the Decisions table and the UNVERIFIED list, against the requirements the candidate states; inventories checked for citations; files outside the sandbox UNVERIFIED.

verdict: PASS
