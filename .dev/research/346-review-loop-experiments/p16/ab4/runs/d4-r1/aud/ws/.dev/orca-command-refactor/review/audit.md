review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `62a2931158ca12b901593ce928e457d6e9134501cf22528ef812325749ee0041` (285 lines)
- Baseline: none given (first review of the full document; no `--re-review`)
- Reviewer model used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full. The brief did not narrow or widen the command's scope, so no brief clause was overridden.
- Citation rule: only the three files under `.dev/orca-command-refactor/inventory/`, the README and the candidate could be opened. Every `cmd/`, `sk/`, `ag/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `install_core.py`, `EVIDENCE.md` and installed-Orca citation that the spec or the inventories make was **not checked** and is UNVERIFIED here, except where an inventory quotes it and I cite the inventory line.
- Spec shorthand: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`.

## Coverage statement
Covered: all 285 lines of the candidate; the README (binding context); the three inventories in full. Checked the 43 / 10 / 27 / 6 arithmetic, the phase-to-command allocation, every WC and SA requirement against the section 3 rows, the section 7 acceptance checks against the requirements they test, and about 60 `INV-*`/`CAPS:*` citations against the inventory lines they point to (all found as cited; the spec's `INV-A:76-83`, `INV-B:292`, `CAPS:92`, `CAPS:97-103`, `CAPS:145-151` and the rest match). Not covered: the contents of any repo or Orca file outside the sandbox (UNVERIFIED), and no command was run.

Counts verified from the inventories: A has 5 ready, 13 needs-change, 3 coordinator-only (`INV-A:73`); B has 5, 14, 3 (`INV-B:278`); totals 10 / 27 / 6 = 43, which is what `S:76` says. The section 3.2 table has 27 rows and the section 3.1 table 10; phase membership is P1 = 9 + 3 fixes, P2 = 15, P3 = 4, P4 = 3, and 27 + 10 reconcile (`S:159-162`).

## Quality metrics (0-10, advisory)
Clarity 8, Completeness 7, Testability 6, Consistency 6.

## === REQUIREMENTS ANALYSIS ===
Experts in review order: Wiegers (lead), Adzic, Cockburn. Whittaker's attacks are in the adversarial section below.

### F1 - BLOCKING - P1 forces the unattended contract onto commands whose gates and decisions come later
- Severity: CRITICAL. Expert: Wiegers, confirmed by Adzic. Priority: High.
- Grading sentence: an implementer who follows the stated text as written builds a P1 that adds `--unattended` and an `## Unattended mode` section to every command in sections 3.1 and 3.2 except load, including `pr-submit`, `implement` and `post-release`, and that is wrong because the same document says those three change only in Phase 4 after decisions D2-D4, and says `/sc:pr-submit` gets no change at all under the recommended D3(a).
- Stated texts that contradict each other:
  - `S:159`: P1 scope is "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load".
  - `S:195`: AC-1.1 passes only if "every command in sections 3.1-3.2 except load" has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`.
  - `S:154`: "Phase 4 waits for answers to D2-D4"; `S:162` puts implement, post-release and pr-submit in P4; `S:240`: under the recommended D3(a) there are "no pr-submit changes in Phase 4"; `S:139`: pr-submit "stays a worker candidate only if the user accepts D3".
  - `S:60` (WC-2): under `--unattended` the command never prompts. For the 15 P2 commands and the P3 commands the gate resolutions are scheduled after P1 (`S:160-161`), so after P1 they accept `--unattended` and still prompt.
- Concrete state trace: P1 done, D3(a) chosen. `pr-submit.md` carries an `## Unattended mode` section (required by AC-1.1) and a coordinator can dispatch `/sc:pr-submit ... --unattended`; the command still has its `--monitor 1` y/n and operator HALTs (`S:114`), which WC-2 forbids, and the recommended decision says it should not have been touched. AC-1.1 cannot pass without contradicting D3(a); with D3(a) honoured AC-1.1 fails.
- Recommendation: restrict the P1 flag, the section and AC-1.1 to the commands whose P1 row says so (the section 3.1/3.2 rows tagged P1, plus the three small fixes), and let each later phase add the flag and section together with its gate resolutions; or state that an `--unattended` flag without its gate resolutions is refused. State that D3(a) removes pr-submit from the P1 assertion.

### F2 - BLOCKING - the contract file's location is undefined or contradicted for 12 commands, so "known before dispatch" and the acceptance steps cannot hold
- Severity: CRITICAL. Expert: Wiegers and Adzic, with Fowler on the interface. Priority: High.
- Grading sentence: an implementer who follows WC-4 as written writes `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (`S:62`), and that is wrong for the commands below because for them `--output` is a file, or no output flag exists and no row adds one.
- Stated texts:
  - `S:62` WC-4: the report path is "known before dispatch"; the listed exceptions (M5) are only adversarial, cleanup-audit, index-repo and workflow.
  - `--output` is a file, not a directory: tdd, `S:90` ("`--output <file>`", report is "the TDD at `--output`"; `INV-B:225`), init-lite, `S:87` (`INV-A:55`), and spec-panel, `S:120` ("add `--output`"; `INV-B:182` says the review document has no path flag). `<file>/return-contract.yaml` is not a valid path.
  - No output flag and no exception: research (`S:116`, "Other required change: none", report path generated at run time, `INV-B:132`), recommend (`S:115`), save (`S:119`), task (`S:121`), review-translation (`S:117`, fixed `reports/localization/` names, `INV-B:142`), cli-eval (`S:104`, three fixed run directories, `INV-A:44`), cli-portify (`S:105`, "file location unnamed"), validate-tests (`S:125`), and implement (`S:109`, "beside the ledger `progress.md`", whose directory is `.dev/implement/<slug>/`, `INV-A:51`, a slug the brief cannot know before dispatch).
- Acceptance consequence: `S:182-183` (7.2 steps 3-4: "its report path is the WC-4 contract path"; `test -s <contract>`) and AC-2.3 (`S:201`), AC-3.x and AC-4.1 cannot be evaluated for these commands because no `<contract>` path exists to test.
- Recommendation: give WC-4 one rule for the location when `--output` is a file or absent (for example a sibling `<output-stem>.return-contract.yaml`, or a mandatory new `--report-dir`), and add the missing commands to the exception list with their fixed paths, or add a row entry that adds the flag.

## === ARCHITECTURE ANALYSIS ===
Experts: Fowler (lead), Newman, Hohpe, Nygard.

The central decision (Orca coordinates, commands stay units of work, section 1) is consistent with the evidence it cites: depth 1 and `nested_worker_depth_exceeded` (`CAPS:97-101`), no commands calling Orca (`S:25` E5, unverifiable here), `worker_done` bound to the dispatched pane (`CAPS:76`), and the honestly stated evidence gap that no direct-route run exists (`S:43`, `INV-B:323`). The interface split (a shared contract file plus a small per-command section, `S:52`) is sound. No blocking architecture finding beyond F1 and F2; the Medium items below are all follow-up candidates.

## === ADVERSARIAL ANALYSIS (Whittaker) ===
Review position 6, after Fowler and Nygard. Every attack below ended in a Medium or minor finding; the two blocking findings above also came from the Sequence/Divergence probes.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / SA-3 (`S:62`, `S:148`)** fails when `--unattended` is passed with no output directory on a command that has an output flag. Concrete attack: before: `/sc:analyze src/x.py --unattended`; SA-3 says the contract is written "only in unattended mode or when the caller passes the new output flag", WC-4 says it goes to `<output-dir>`; after: no `<output-dir>` exists, and the text neither refuses the run nor names a default. See M1.
2. I can break this specification by **Sequence Attack**. The invariant at **WC-3 / WC-6 / WC-4 (`S:61`, `S:64`, `S:62`)** fails when a gate resolves as blocked and the worker re-invokes the command with the answer. Concrete attack: before: the command stopped with `status: blocked` in `<dir>/return-contract.yaml`; the worker calls `ask`, gets the answer, re-invokes; WC-6 says a command with no resume flag "writes each run into a fresh output directory" (20 of the section 3.2 rows say "fresh dir"); after: the second run's contract is in a new directory the coordinator was never told, and the old directory still says `blocked`. See M2.
3. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (`S:68`)** fails when a single tool call exceeds 5 minutes for a reason other than a poll or eval wait. Concrete attack: `/sc:cleanup-audit` or `/sc:post-release` dispatches a wave of 5-8 Task agents in one message (`INV-A:42`, `INV-B:81`); the call blocks the session for longer than the 5-minute heartbeat cadence; WC-10 covers only "a poll wait, a long eval". See M3.
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 status vocabulary (`S:62`, Decisions `S:262`)** fails when an existing contract already has a `status` field with other values. Concrete attack: workflow, reflect, brainstorm and adversarial "keep their fields" (`S:62`) while `status` must be one of `succeeded|partial|failed|blocked`; their current status values are not recorded in any inventory, so either rule can be violated. See M4.
5. I can break this specification by **Divergence Attack**. The invariant at **tasklist row (`S:122`) and SA-6 (`S:151`)** fails when `--unattended` is passed to each Stage 10.5 reflect. Concrete attack: before: Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase (`INV-B:209`); after: the spec makes `--unattended` reflect "follow the existing headless auto-accept rule" (`S:88`), so the remediation offer is auto-accepted for auto-fixable registers and a remediation handoff runs without a person; `INV-B:215` had recommended dropping `--remediate` instead, and no Decisions entry records why the spec chose differently. See M5.
6. Zero/empty probe on the section 7 pass conditions: `S:183` step 3 "exactly one `worker_done`" passes vacuously on a worker killed before the first send only if `check --wait` times out; the text does not say what a coordinator does on timeout. Minor, see N1.

## Guard Condition Boundary Table
Trigger present (the spec contains many threshold and flag guards). Classes that cannot occur for a guard are left out with a reason in the last row of each guard. Responsible experts: Nygard (construction), Crispin (completeness), Whittaker (attack). FR-8/FR-9 gaps are graded as in the command: a GAP is blocking only if it names a concrete wrong outcome; the other GAPs are Medium and appear under follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` mode switch | `S:51`, WC-2 `S:60`, D1 `S:227` | Zero/Empty | flag absent | false | Today's behaviour unchanged (SA-1 `S:146`) | OK |
| `--unattended` mode switch | `S:51`, `S:148` | One/Minimal | flag present, no output dir / no report path | true | unspecified: no refusal, no default location | GAP (M1, Medium) |
| `--unattended` mode switch | `S:159`, `S:195` | Legitimate Edge Case | flag present on a command whose gates are not yet converted (P2-P4) | true | P1 requires the flag; WC-2 forbids prompting | GAP (F1, blocking) |
| output directory for contract | WC-4 `S:62` | Zero/Empty | command has no `--output`, or `--output` is a file | n/a | undefined for 12 commands | GAP (F2, blocking) |
| gate resolution (a)/(b)/(c) | WC-2 `S:60` | Typical | no default, no flag | true | blocked: contract + question, stop | OK |
| gate resolution | WC-3 `S:61` | Legitimate Edge Case | blocked, then answered and re-invoked | true | output location of the re-run unspecified | GAP (M2, Medium) |
| status to outcome map | WC-5 `S:63` | Typical | `failed` / `blocked` / none | true | `--outcome failed` | OK |
| status to outcome map | WC-5 `S:63` | Legitimate Edge Case | `partial` | false for failed | `--outcome succeeded`, first body sentence says partial | OK (see N2) |
| status to outcome map | WC-5 `S:63` | Sentinel Value Match | report exists but `status` is outside the four values or the YAML does not parse | unknown | unspecified; "no report exists" does not cover it | GAP (M6, Medium) |
| heartbeat wait split | WC-10 `S:68` | Typical | one blocking call under 4 min | false | no split needed | OK |
| heartbeat wait split | WC-10 `S:68` | Maximum/Overflow | one call longer than 5 min that is not a poll or an eval (Task-agent wave) | true | unspecified | GAP (M3, Medium) |
| `check` returns `consumer_fenced` | WC-12 `S:70` | Sentinel Value Match | `consumer_fenced` | true | stop, no `worker_done` | OK |
| task confidence | `S:121` | Maximum/Overflow | below 0.70 | true | blocked | OK |
| task confidence | `S:121` | One/Minimal | exactly 0.70 | false | not stated (inherits `INV-B:199`, "< 0.70") | OK (inherited text) |
| `--monitor` ordinal | `S:114` | Legitimate Edge Case | `--monitor 1` refused; 0, 2, 3 | n/a | only 1 is addressed; 0 not stated | minor, see N3 |
| nested-worker depth | D5 `S:249` | Typical | 1 | true | workers cannot start workers | OK |
| nested-worker depth | D5 `S:249` | Maximum/Overflow | raised above 1 | n/a | declined (non-goal) | OK |

Left out, with reason: the Zero/Empty class for the 4-minute split (a zero-length wait cannot occur); Sentinel for `--monitor` (no sentinel value).

## Pipeline Dimensional Analysis
Not triggered. The spec describes no data pipeline whose output count can differ from its input count; the only counts are the command totals (43 = 21 + 22; 10 + 27 + 6; P1 9 + 3 fixes, P2 15, P3 4, P4 3), and all conserve (checked above). No Quantity Flow Diagram is produced.

## Panel notes (non-blocking, expert-attributed)
- Wiegers: every WC and SA row carries an evidence cell, which is good traceability. The "Evidence" for WC-9 and for the `/sc:git` row cites `.dev/orca-command-refactor/README.md:31` (`S:67`, `S:133`); README line 31 is a rule for the workers of this planning run, not repo policy. It supports "this run makes no commits" but not "workers in this repo need the user's authorization". See N4.
- Adzic: AC-2.2 and AC-4.x give concrete scenarios (`/sc:tdd "auth" --unattended` with a bare topic; a plan with an unmeetable criterion). AC-0.4 and AC-1.3 are good executable examples.
- Cockburn: the primary actor (the Orca coordinator) and its goal are stated once in section 2.3; the person who runs a command by hand is protected by SA-1 to SA-6.
- Fowler: one shared contract file plus per-command sections is the right split. WC-8 and SA-2 keep Orca out of commands; this fits the evidence in `CAPS:145-149`.
- Nygard: failure modes of the worker (stall, silent block, crashed worker) are covered by WC-2, WC-3, WC-12 and the 7.2 `agentWait` check. The recovery path for a worker that dies before writing any contract is only "no report, `--outcome failed`" (`S:62` workflow exception); the general case is not stated (N1).
- Newman, Hohpe: the report-file contract is a versioned-nothing interface. No `contract_version` field is specified, so a later field change cannot be detected by the coordinator. Note only; the spec is a plan.
- Crispin, Gregory: the P0 smoke runs (`S:158`, AC-0.4) correctly test the decision before building on it. Hightower: no operational concern beyond the heartbeat item (M3).

## Follow-up candidates (Medium and minor; none triggers a revision and none is in the Reviser brief)
The session that ran this review would ask the user once whether to open an issue for these; this sandbox run has no user to ask, so no issue is created and the list is only recorded.

Medium (warnings):
- M1. `--unattended` with no output directory is not defined (`S:62`, `S:148`; Whittaker 1). Add a refusal (as a blocked contract printed in chat) or a documented default directory.
- M2. A blocked-then-answered re-invocation, and a `--retry-of` worker, write into a "fresh output directory" (`S:64`, 20 rows) that the coordinator did not name (`S:62`, `S:73`). Say that the caller supplies the fresh directory on each attempt.
- M3. WC-10 splits only poll and eval waits (`S:68`); a single Task-agent wave can exceed 5 minutes (`INV-A:42`, `INV-B:81`), so AC-4.3's "heartbeats at most 5 minutes apart" (`S:210`) is checked only for pr-submit. Also `CAPS:130` says it is UNVERIFIED whether Orca uses heartbeat age, yet WC-10 is written as a hard requirement.
- M4. Existing contracts (workflow, reflect, brainstorm, adversarial) "keep their fields" (`S:62`) but must have `status` in a fixed four-value set; their current `status` values are not in any inventory, so the two rules may collide (`S:262`).
- M5. The tasklist row sends `--unattended` into each Stage 10.5 reflect (`S:122`), which auto-accepts remediation under the headless rule (`S:88`, `S:151`). `INV-B:215` recommended dropping `--remediate`; the Decisions table (`S:268`) says "nothing read contradicts a verdict" but records no reason for departing from that recommendation. Also reflect's default UC-2 folder move and its tracked-file write (`INV-B:114`) are on under `--unattended` and WC-9 (`S:67`) lists only push, PR, post, install, provision and paid-run actions, so these stay on without comment.
- M6. A contract that exists but is unparseable or has an out-of-set `status` has no stated outcome (`S:63`, `S:183`).
- M7. AC-C1 (`S:172`) scans `src/superclaude/core` and expects no match for `orca (orchestration|worktree|terminal|agent)`, but P0 adds an Orca section to `HOW-WE-WORK.md` (`S:158`, SA-5 `S:150`) and a coordinator brief template, and SA-2 (`S:147`) explicitly allows an Orca example in the contract file. If either text names `orca orchestration ...`, AC-C1 fails on the spec's own deliverable. State that both files avoid that form or exclude them from the grep.
- M8. P3 says "reconcile" command and skill for roadmap and validate-roadmap (`S:118`, `S:124`) without choosing which side wins; `INV-B:309` records that no file says. AC-3.1 (`S:204`) passes under either choice. P3 is stated to need no user decision (`S:154`).
- M9. `S:154` says "Phases 1-3 need no user decision", but D4 (`S:244`) covers auggie-review `--post-pr` and task `commit`/`push`, both P2 rows; `S:225` says "can proceed on the recommendations". Align the two sentences.

Minor notes:
- N1. 7.2 step 3 (`S:182`) gives no action when `check --wait` times out with no `worker_done`; the general no-contract failure path is stated only for workflow.
- N2. `partial` maps to `succeeded` (`S:63`, `S:263`); Orca then treats the Task as completed and its dependents become startable (`CAPS:89-90`, `CAPS:92`). Section 2.3 has the coordinator open the report first, which mitigates this; say it must do so before starting dependents.
- N3. `--monitor 0` is not addressed in the pr-submit row (`S:114`).
- N4. README line 31 is cited for repo-wide policy in two places (`S:67`, `S:133`); cite the repo rule instead (UNVERIFIED which file).
- N5. `CAPS:40` and `CAPS:161` cite the installed pr-submit skill at `:47-49`; the spec and the inventories A and B cite the source copy at `:37-39` (`S:11`, `S:65`). Probably two different copies; confirm.
- N6. `S:261` refers to "ladder rung 2" with no definition in the spec or README.
- N7. Self-reported checks in the spec cannot be verified here: the E5 grep results (`S:25`), the 11 re-read locations (`S:11`), and the 340-citation validator run (`S:285`). Treated as UNVERIFIED, not as evidence.

## UNVERIFIED citations (could not be opened inside the sandbox)
All `cmd/*`, `sk/*`, `ag/*` lines cited in section 3 and section 9 beyond what the inventories quote; `CLAUDE.md:16,50,72-83,157,334,408`; `src/superclaude/cli/install_core.py:4,13-24,33`; `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`; `src/superclaude/core/CLAUDE.md:65`; `Makefile:68-74`; `pyproject.toml:38`; `tests/skills/*`; `.dev/codegraph-migration/**` and `.dev/evals/**` (as opened files; their content is known only through `CAPS:49`, `CAPS:156` and `INV-A:13-14`); all Orca guide, `--help` and compiled-JS lines (known only through `CAPS:*`).

## Reviser brief
Blocking finding ids: F1, F2.

Rules for the reviser (restating the command's Reviser contract; the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium findings (M1-M9) and minor notes (N1-N7) alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
