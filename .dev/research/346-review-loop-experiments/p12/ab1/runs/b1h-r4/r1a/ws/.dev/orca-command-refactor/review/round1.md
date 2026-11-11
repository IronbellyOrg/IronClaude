review: 1 of 3
# /sc:spec-panel critique: Orca worker contract spec, review 1

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review; no `--re-review`, so no prior report; `baseline: not given`, which is not an error for a first review)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- command definition used: `command.md` in the sandbox folder (sha256 `e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494`), cited as `command.md:N`. It is not a repo file.
- review prompt: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox copy)
- reviewer model: claude-haiku-5-5 (single reviewer). The brief asks for one first review. The MERGE of three reviews and the VERIFY step belong to the coordinator and are not run here, so the blocking list below is not final until VERIFY runs.
- output path note: `.dev/orca-command-refactor/README.md` names `review/spec-panel.md` for this output (README:19-26). The brief names `review/round1.md`. This report follows the brief.

Citation key: `spec:N` = candidate line N. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. Citations to `src/superclaude/`, `CLAUDE.md`, `.dev/evals/`, `/opt/Orca/`, `.dev/codegraph-migration/` and installed skills are outside this workspace and are marked UNVERIFIED. The brief's scope limit applies: the only evidence checked is the inventory and README files, plus `command.md`.

Coverage: read the full spec, README, the three inventories, the review-loop prompt file and `command.md`. Spot-checked about 30 spec citations into the inventories against the cited lines (sample, not exhaustive); all matched except the spec-panel evidence at INV-B:43, whose claim sits at INV-B:182 and is stale (see B1). The expert pass covers the Requirements bucket (Wiegers lead, Adzic, Cockburn) and the Architecture bucket (Fowler lead, Newman, Hohpe, Nygard). Whittaker is active in every panel review and is included under ADVERSARIAL ANALYSIS.

## Mandatory output artifacts

- **Guard Condition Boundary Table**: triggered (the spec has numeric thresholds and branch rules, spec:59, 63, 64, 68). Produced below.
- **Pipeline Dimensional Analysis**: not triggered. The flow is one Task, one worker, one contract, one `worker_done`, with no stage that changes a count (spec:73, spec:62).
- **State Variable Registry**: not required (focus is requirements and architecture, not correctness).

=== GUARD CONDITION BOUNDARY TABLE ===

Guards enumerated: WC-1 (readiness), WC-2 (gate resolution), WC-3 (ask path), WC-4 (contract path), WC-5 (outcome mapping), WC-6 (resume and retry), WC-10 (wait size). Input classes left out: WC-7, WC-8, WC-9, WC-11, WC-12 are not threshold or branch rules and are not enumerated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | spec:63 | Zero/Empty | no contract file | `--outcome failed` | "or no report exists" | OK |
| WC-5 outcome | spec:63 | Zero/Empty | 0-byte or unparseable contract file | `succeeded` (falls into "otherwise") | not excluded | GAP (B3) |
| WC-5 outcome | spec:63 | One/Minimal | `status: partial` | `succeeded` | spec:263 | OK |
| WC-5 outcome | spec:63 | Typical | `status: succeeded`, verdict FAIL | `succeeded` | spec:63 ("including an audit whose verdict is FAIL") | OK (dependent gating is F6) |
| WC-5 outcome | spec:63 | Sentinel | `status: partial` with non-empty `blocked_question` | `succeeded` | question not represented in the outcome | GAP (F6) |
| WC-5 outcome | spec:63 | Legitimate edge | existing contract `status` value outside the four | undefined | spec:262 maps no existing values | GAP (F4) |
| WC-4 path | spec:62 | Typical | `--output` is a directory | `<dir>/return-contract.yaml` | stated | OK |
| WC-4 path | spec:62 | Sentinel | `--output` is a regular file (tdd, spec-panel) | path under a file cannot exist | contradicts spec:90, 120, 200 | GAP (B1) |
| WC-4 path | spec:62 | Max/Overflow | output directory not writable | no contract | falls to WC-5 "no report exists" | OK |
| WC-4 scope | spec:62, 92, 148 | Edge: stop before output, standalone run | no `--unattended` | write a contract or not | unattended only (spec:62); workflow row (spec:92) and SA-3 (spec:148) disagree | GAP (F10) |
| WC-6 resume | spec:64 | Zero: no resume flag, same output dir (init-lite re-run) | overwrite | must write a fresh directory | spec:87 says overwrite | GAP (B2) |
| WC-6 resume | spec:64 | One: resume flag given | resume from disk | resume | spec:84, 89, 90 | OK |
| WC-6 dir choice | spec:64 vs spec:62 | Edge: retry | who picks the new directory | unspecified | command in WC-6, coordinator in WC-4 | GAP (F9) |
| WC-1 readiness | spec:59 | Boundary: fallback 30 s, limit 60 s | "well inside" | no number | not quantified | GAP (F1) |
| WC-1 readiness | spec:59 | Sentinel: prompt with no fallback | never reaches input | start fails at readiness (CAPS:44-45) | rule stated; no owner phase (F16) | OK (owner gap in F16) |
| WC-10 wait | spec:68 | Boundary: 270 s single call | 270 s | not split (WC-10 splits only "longer than 5 minutes") | AC-4.3 requires at most 240 s (spec:210) | GAP (F2) |
| WC-10 wait | spec:68 | Boundary: 300 s single call | 300 s | not split | heartbeat cadence 5 min (CAPS:130), zero margin | GAP (F2) |
| WC-10 wait | spec:68 | Typical | 180 s | no split | stated | OK |
| WC-2 gate | spec:60 | Zero: no default, no flag | none | blocked, (c) | stated | OK |
| WC-2/3 gate | spec:60-61 | Sentinel: blocked gate, worker holds a preamble | `ask` or blocked | either ("may", spec:61) | not fixed; only blocked is tested (spec:200) | GAP (F5) |
| WC-2 gate | spec:60 | Legitimate edge: documented default and flag both absent | default value | default applies | stated | OK |

Table result: 9 GAP rows. B1, B2 and B3 are blocking under FR-8. The other GAP rows are Medium under FR-8 because they name no concrete wrong outcome beyond the follow-up candidates listed below.

=== REQUIREMENTS ANALYSIS ===

### Blocking findings

**B1. Output flag value types contradict each other (tdd, spec-panel, AC-2.2).** Expert: Fowler (lead), Wiegers. Severity: MAJOR, blocking.
- Stated texts: WC-4 says the contract goes in `<output-dir>`, "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). The tdd row gives `--output <file>` (spec:90). The AC-2.2 gate-trigger example is `/sc:tdd "auth" --unattended --output <file>` (spec:200). The spec-panel row says "add `--output`" (spec:120).
- Grading sentence: An implementer who follows WC-4 as written writes the contract to `<tdd-file>/return-contract.yaml`, and because a regular file cannot hold a child path, the contract is never written; WC-5 (spec:63) then reports every such tdd run as failed for want of a report.
- Command evidence: `command.md:23` already defines `--output <file>` for spec-panel, and `command.md:460` says "`--report-dir <dir>` only (`--output` is file-valued)". The unattended contract goes under `<report-dir>` (`command.md:461`). So spec:120 would add a directory-valued `--output` where the command already has a file-valued one.
- Stale evidence: INV-B:182 says spec-panel has "no path or `--output` flag" and cites `cmd/spec-panel.md:22`. That is out of date against `command.md:23`, `:459-461`. The spec row at spec:120 inherits the stale claim (spec:11 says only 11 locations were re-read).
- Recommendation: WC-4 must name the contract location per flag type. For file-valued outputs, the contract goes beside the file or in a named `--report-dir`. spec-panel should use its existing `--report-dir` and not a new `--output`. Fix spec:90, spec:120 and AC-2.2 (spec:200) to match.
- Priority: High. Quality impact: every tdd and spec-panel worker run.

**B2. init-lite re-run overwrites its report, which WC-6 forbids.** Expert: Nygard (lead), Fowler. Severity: MAJOR, blocking.
- Stated texts: section 3.1 gives init-lite "Re-run overwrites its marked report" (spec:87). WC-6 says a command either resumes from its on-disk state or "writes each run into a fresh output directory so a re-run starts clean", and that a retry "must not corrupt the first attempt's output" (spec:64). The inventory agrees on the overwrite (INV-A:55).
- Grading sentence: An implementer who follows section 3.1 leaves init-lite as it is, so a `worker-start --retry-of` re-run replaces the first attempt's `context-audit.md`; WC-6 says the retry must not corrupt that output, and the spec names no third option.
- Recommendation: give init-lite a fresh output directory per run (its report path is the only state), or state in WC-6 that overwrite is an allowed mode with its reason. The first keeps WC-6 unchanged.
- Priority: High. Quality impact: loses the first attempt's report on every retry.

**B3. The outcome mapping treats an empty or status-less contract as success.** Expert: Whittaker (FR-2.1 Zero/Empty), Wiegers. Severity: MAJOR, blocking (names a concrete wrong outcome).
- Stated text: `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise (spec:63). Acceptance check step 4 (spec:183) tests `test -s` and a `status` value, but only after `worker_done` has already settled the Task (CAPS:77).
- Grading sentence: An implementer who follows WC-5 as written sends `--outcome succeeded` for a 0-byte `return-contract.yaml` left by a worker killed mid-write, because the file exists and says neither `failed` nor `blocked`; the Task then settles as completed with no content (CAPS:77), and the ready view starts its dependents (CAPS:86).
- Recommendation: `succeeded` only when the contract parses and has `status` in {`succeeded`, `partial`}; every other state (missing, empty, unparseable, no `status`) maps to `failed`. Also move the `test -s` check into the worker's own mapping.
- Priority: High. Quality impact: silent success on crashed workers.

### Medium findings (follow-up candidates, not blocking)

| ID | Expert | Location | Finding | Recommendation |
|---|---|---|---|---|
| F1 | Wiegers | spec:59; CAPS:49 | WC-1 says the fallback must sit "well inside the readiness limit" with no number. The 30 s fallback passing and "above about 45 s" failing were measured against a 45-second start limit (CAPS:49, quoting EVIDENCE:45, 56 which is UNVERIFIED), but WC-1 applies them to the 60 s default. | State a fallback value and the limit it was measured against. |
| F2 | Adzic, Wiegers | spec:68, 210, 266 | WC-10 splits waits "longer than 5 minutes". AC-4.3 requires "no single tool call exceeds 240 s" (spec:210), and the decision row says 4 minutes (spec:266). A 270 s call passes WC-10 and fails AC-4.3; a 300 s call is not split and leaves no margin under the heartbeat cadence. | One threshold, used in WC-10, AC-4.3 and the decision row. |
| F3 | Adzic | spec:194, 183 | AC-0.4 step 4 requires `status` in four values and a `command` key in "the command's existing report file" for adversarial, troubleshoot and workflow. The inventory gives no key list for those files (INV-A:35 names only the filename; INV-B:272 names workflow fields `status`, `plan_path`, `reflect_report_path`). P0 gates the decision (spec:194), so the check cannot be run as written for most of its files. UNVERIFIED: existing schemas. | Define step 4 per command, or limit P0 to workflow, which has a known contract. |
| F4 | Wiegers | spec:62, 262 | WC-4 says commands that already write a contract "keep their fields and add the missing ones", but says nothing about existing `status` values that fall outside the fixed four (INV-B:272 contract 1.1). | Add a mapping table from each existing status vocabulary to the four values. |
| F5 | Hohpe, Nygard | spec:61, 181, 200 | WC-3 says the session "may" ask the coordinator and then "re-invoke or resume the command with the answer as a flag". No command defines an answer flag (section 3 gives only blocked behaviour), and the only tests (spec:200, spec:181 step 2) require `blocked` and no `agentWait`. The ask path is untested and fails step 2 by design. | Name the answer flag per gate, or remove the ask path until a command uses it. Add a check for the ask path. |
| F6 | Fowler, Hohpe | spec:63, 73; CAPS:86, 88 | WC-5 counts an FAIL audit and a `partial` report as successful, so the Task completes. Section 2.3 says the coordinator opens the report and "releases or reuses the worker" but says nothing about dependents. CAPS:86 starts ready Tasks. A `partial` contract with a non-empty `blocked_question` also maps to success. | State that dependents wait for a verdict (or a `blocked_question` resolution) before starting. |
| F7 | Whittaker (FR-2.4), Hohpe | spec:62, 63 | "Exactly once" `worker_done` has no rule for a lost response. CAPS:117 offers `--retry-request` for mutations, which the spec does not use. The spec also does not require the contract to be written before `worker_done` (spec:62 passes the path but gives no order). | Require the contract write to precede `worker_done`, and state the retry rule for a lost response. |
| F8 | Nygard, Whittaker (FR-2.5) | spec:63, 64; CAPS:80, 116 | A gate that always resolves blocked produces `failed` (spec:63). A worker's own `failed` report does not trip the breaker, and only failed `worker-start` attempts count (CAPS:80, 116). With a new output directory on each retry (spec:64), a coordinator can dispatch without a cap. | Add a retry cap per Task for blocked outcomes, and say who enforces it. |
| F9 | Fowler | spec:62, 64, 73 | WC-6 has the command "write each run into a fresh output directory", but WC-4 has the coordinator pass the directory before dispatch (spec:62, 73). A command given `--output X` cannot choose a new directory itself. | State that the coordinator passes a new `--output` on each retry (add to 2.3). |
| F10 | Cockburn, Hohpe | spec:92, 83, 148, 149 | SA-3 says a standalone default run "writes the same files it writes today". The workflow row adds a contract for pre-creation STOPs (spec:92), and the adversarial row changes the contract filename (spec:83). The spec does not say these changes are unattended-only, and SA-4 (spec:149) allows defect fixes only where they "keep the standalone behaviour or correct a documented defect". | Mark both changes as unattended-only, or name them as defect fixes under SA-4. |
| F11 | Whittaker (FR-2.2) | spec:84, 89, 103, 146 | Per-row rules say what happens to `--interactive` (release-split, cleanup) but there is no general rule for a brief that combines `--unattended` with `--interactive`, or for `--unattended` on a ready-today command (brainstorm, spec:84). | Add one rule: `--unattended` wins over `--interactive`, or the brief is refused. |
| F12 | Fowler, Wiegers | spec:88, 122; INV-B:114 | "Ready today" for reflect ignores the default-on Wave 7 folder move (INV-B:114). Under `--unattended` the headless auto-accept lets the worker accept remediation (spec:88, 122). WC-9 (spec:67) covers only outward actions (push, PR, post, install, provision, paid run), not local moves or code edits. | Add a local-mutation rule to WC-9, or move reflect out of "ready". |
| F13 | Whittaker (FR-2.3) | spec:228, 51; command.md:459 | D1 says `--unattended` "cannot misfire on a person". The spec's own text contains `--unattended` (spec:51, 228), so a command that scans input text for the token can misfire. command.md:459 requires a standalone argument token outside quoted arguments; the spec states no such rule. | Require argument-token parsing, as command.md:459 does, and drop "cannot misfire". |
| F14 | Newman, Fowler | spec:147, 172, 52 | SA-2 allows an Orca example "inside the contract file", which lives in `src/superclaude/core` (spec:52). AC-C1 (spec:172) forbids `orca orchestration` anywhere in `src/superclaude/core`, and excludes only `ccsession-tag`. A permitted mention fails an acceptance check. | Exclude `WORKER-CONTRACT.md` from AC-C1, or forbid the mention in SA-2. |
| F15 | Nygard | spec:44, 60, 73, 181, 182; CAPS:125, 127 | WC-2 says a stall is "invisible" (spec:60). Section 1.4 says the coordinator sees it through `agentWait` (spec:44). The `agentWait` polling duty is in the acceptance procedure (spec:181 step 2), not in the coordinator duties (spec:73). Section 2.3 gives no action on a silent stall, and the `check --wait` loop runs to `worker_done` with no stop rule (spec:182 step 3). CAPS:127 (three empty waits, then `worker-list`) and CAPS:125 (absence never authorizes retry or release) are not carried. | Move the polling duty and the stall rules into 2.3, and fix "invisible" to match 1.4. |
| F16 | Fowler, Hohpe | spec:59, 158-162, 191-210 | WC-1 assigns its rule to "Launch setup, not commands". No phase (spec:158-162) or check (spec:191-210) covers launch setup. | Name the owner of launch setup, its phase and a check. |
| F17 | Newman | spec:135, 137; INV-B:32; INV-A:36, 69 | `/sc:pm` "runs automatically at every session start" (INV-B:32), `/sc:agent` launches at session start (INV-A:36), and the session-init banner prints for Orca workers (INV-A:69). The coordinator-only rationale (spec:135, 137) keeps them out of workers, but no requirement stops a worker session from running them. | Add a requirement that worker sessions skip session-start orchestration, with a check. |
| F18 | Newman | spec:62; INV-B:272 | WC-4 adds fields to existing contracts (workflow is "contract 1.1", INV-B:272) and the new contract has no version field. No compatibility rule. | Add a version field and a compatibility rule. |

### Minor notes

- M-a: spec:271-286 omits CAPS:182 (heartbeat age and liveness, UNVERIFIED). The WC-10 margin (spec:266) depends on that premise.
- M-b: spec:162 lists pr-submit under P4, while the recommendation (spec:240) says "no pr-submit changes in Phase 4".
- M-c: WC-2 gives one `blocked_question` field (spec:63), but tasklist Stage 10.5 and cleanup can have several open gates. The spec does not say whether all are listed.
- M-d: E4 (spec:24) says Agent-tool subagents "are not counted by Orca's nesting limit". CAPS:155 supports "not counted by the depth fence" but marks "no Orca limit at all" UNVERIFIED. The sentence should carry that caveat.

=== ARCHITECTURE ANALYSIS ===

Consensus (Fowler, Newman, Hohpe, Nygard): the decision in section 1 (Orca coordinates, commands stay units of work) follows from the cited evidence, and the rejected alternative (R1 to R5) is well argued. The live-run gap (spec:43) is stated honestly. The architecture risk sits in the contract's shared rules and in the status mapping, not in the top-level decision.

Disagreement: Newman would move the contract schema into a versioned file (F18), and Fowler would keep it prose-only and enforce it by tests (F14, F16). The panel did not settle this; the coordinator should decide.

- Blocking architecture findings: B1 (flag and path types), B2 (retry overwrite), B3 (outcome mapping). See above.
- Medium architecture findings: F5 (ask path), F6 (dependents of partial and FAIL), F7 (exactly-once), F8 (retry cap), F9 (who picks a directory), F14 (AC-C1 vs SA-2), F15 (stall duty), F16 (launch setup owner), F17 (session-start hooks), F18 (versioning).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

- FR-2.1 Zero/Empty Attack: I can break this specification by **zero/empty outcome mapping**. The invariant at **WC-5 (spec:63)** fails when **the contract file is present but empty or has no `status`**. Concrete attack: **the worker is killed during its contract write, leaving a 0-byte file; WC-5's "otherwise" branch sends `--outcome succeeded`; the Task settles with no content (CAPS:77) and dependents start (CAPS:86).** Severity: MAJOR, blocking (B3).
- FR-2.2 Divergence Attack: I can break this specification by **a condition that both branches claim**. The invariant at **WC-5 (spec:63)** fails when **`status: partial` and a non-empty `blocked_question` appear together**. Concrete attack: **`partial` maps to succeeded (spec:263), so the coordinator starts dependents while a gate still waits for an answer.** Severity: MEDIUM (F6). Also: `--unattended` with `--interactive` is undefined (F11).
- FR-2.3 Sentinel Collision Attack: I can break this specification by **`--unattended` appearing in input text**. The invariant at **D1 (spec:228)** fails when **a document passed as input contains the token `--unattended`**. Concrete attack: **this specification contains `--unattended` in its own text (spec:51, 228); a command that scans its input for the token switches to unattended mode and blocks at its first interactive gate.** Severity: MEDIUM (F13).
- FR-2.4 Sequence Attack: I can break this specification by **out-of-order settlement**. The invariant at **WC-4 and WC-5 (spec:62, 63)** fails when **`worker_done` arrives before the contract is written, or is sent a second time after a lost response**. Concrete attack: **the worker sends `worker_done --report-path` for a file it has not yet written; the coordinator finds nothing and records failure, though the contract appears seconds later.** Severity: MEDIUM (F7).
- FR-2.5 Accumulation Attack: I can break this specification by **unbounded re-dispatch**. The invariant at **WC-6 and WC-5 (spec:63, 64)** fails when **a Task is re-dispatched after each blocked outcome**. Concrete attack: **a gate that always resolves blocked yields `failed` (spec:63); a worker's own failure does not trip the breaker (CAPS:80), so retries with fresh directories (spec:64) continue without a cap.** Severity: MEDIUM (F8).

=== PRIORITY-RANKED IMPROVEMENTS ===

1. Fix B3: map every state except a parseable `succeeded` or `partial` contract to `failed` (spec:63, 183).
2. Fix B1: define the contract path by flag type; move tdd and spec-panel to a file-beside or `--report-dir` rule; fix spec:90, 120, 200 (INV-B:182 is stale).
3. Fix B2: give init-lite a fresh output directory per run (spec:87).
4. Resolve F9 and F8 together: the coordinator passes a fresh `--output` per retry, with a cap (add to 2.3).
5. Resolve F6 and F7 in WC-5: state dependents' gating and the contract-before-`worker_done` order.
6. Fix F1, F2, F3 (thresholds and P0 check) before P0 runs.
7. Resolve F10 and F12 (unattended-only changes; local-mutation rule).
8. Resolve F14 and F13 (AC-C1 exclusion; argument-token rule).
9. Carry F15 and F16 into section 2.3 and an owner phase; add F17 as a requirement.

=== QUALITY METRICS (0-10) ===

- Clarity: 6. Most rules are specific, but "well inside", "may" (WC-3) and "otherwise" (WC-5) leave choices open.
- Completeness: 6. Launch setup, session-start hooks, retry directory and stall handling are missing (F15, F16, F17, F9).
- Testability: 7. Section 7 gives runnable checks, but AC-0.4 step 4 (F3), AC-C1 (F14) and AC-4.3 (F2) cannot pass as written.
- Consistency: 4. Flag types, the outcome mapping and the spec-panel row disagree with each other and with `command.md` (B1, B3, F10, F14).

=== CONSENSUS AND DISAGREEMENTS ===

- Consensus: the top-level decision (section 1) and its evidence chain are sound; the spec states its live-run gap in 1.4.
- Disagreement: contract as prose versus versioned schema (see the architecture block above).

## Follow-up candidates

Medium and minor findings, listed for the session that ran the review. The brief does not authorise creating issues from this worker.

- F1 to F18 (table above); M-a to M-d (minor notes above).

## Coverage statement

Covered: spec:1-285 in full; README:1-39; all three inventories; `review-loop` prompt file in full; `command.md` in full (its unattended section, lines 455-467, and usage line 23). Not covered: the repo sources cited by the spec (`src/superclaude/`, `CLAUDE.md`, `.dev/evals/`, `/opt/Orca/`, installed skills and commands). Every citation to those is UNVERIFIED in this review. No revised specification is written: this is a critique run with no `--improve` and no `--re-review`.

## Reviser brief

Blocking ids: B1, B2, B3.

Restated rule (review-loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing; report byte size before and after, with bytes added and deleted per finding id.

verdict: FAIL
