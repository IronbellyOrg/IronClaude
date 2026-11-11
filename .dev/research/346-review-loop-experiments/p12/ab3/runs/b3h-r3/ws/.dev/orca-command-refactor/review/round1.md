review: 1 of 3

# Spec-panel critique: Orca worker contract spec (round 1)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt: FIRST-REVIEW, from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). No `--unattended`, so the unattended section and `WORKER-CONTRACT.md` do not apply.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57763 bytes, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--re-review`)
- Reviewer model: claude-haiku-5-5
- Output format: standard sections (no format flag given)
- Citations: `SPEC:n` = candidate line n; `INV-A:n`, `INV-B:n`, `CAPS:n` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Files named in the spec but absent from this sandbox (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `pyproject.toml`, Orca source) are UNVERIFIED here. I checked only whether an inventory quotes them, and say so where it does.

## Coverage

- Read in full: the candidate (285 lines), `README.md`, the three inventories, the review-loop prompt file, and `command.md`.
- Checked against the inventories: section 3 counts (`SPEC:76-125`) against `INV-A` (5 ready, 13 needs-change, 3 coordinator-only) and `INV-B` (5, 14, 3). The totals 10 / 27 / 6 are consistent. Also checked the spec's Orca citations against `CAPS` (`SPEC:21-26, 33-40, 50-52, 58-70, 74-79, 84-93, 97-103, 109-115, 126-129, 145-151, 155-161`), and its inventory citations against `INV-A:14, 35, 39, 42, 53, 55, 66` and `INV-B:52, 132, 210, 215, 242, 272`. Each matches the inventory line it cites, except where a finding says otherwise.
- Not checked: any `src/` file (absent from the sandbox). `SPEC:11` says the spec's author re-read eleven of them on 2026-11-02. That is UNVERIFIED here.
- Pipeline Dimensional Analysis: not triggered. The spec has no multi-stage data flow whose counts diverge; its Task waves order work by dependency (`CAPS:86`).
- State Variable Registry: not required (focus is not correctness).

## Mandatory output artifact: Guard Condition Boundary Table

Triggered: the spec contains conditional logic (the WC-4 blocked and no-report rules, the WC-5 outcome mapping, the WC-1 and WC-10 thresholds, and the per-command gate resolutions). Every GAP cell names its finding.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | SPEC:51, SPEC:146 | Zero/Empty | flag absent | false | Interactive behaviour unchanged | OK |
| `--unattended` switch | SPEC:51 | Typical | flag present in brief | true | WC-2 applies; each gate resolves (a), (b) or (c) | OK |
| `--unattended` switch | SPEC:73 | Sentinel Value Match | flag omitted from a brief whose command has a gate | false | Command stalls on its prompt; only the coordinator's step-2 poll (SPEC:181) would see it | GAP (F-13) |
| WC-2 gate default | SPEC:60 | Legitimate Edge Case | gate whose "documented default" is not listed (cli-eval safety flags, SPEC:104) | undefined | Brief cannot tell which flags are required | GAP (F-08) |
| WC-4 contract written | SPEC:62 | Zero/Empty | no contract file written | file absent | WC-5 maps to failed (SPEC:63) | OK |
| WC-4 contract written | SPEC:62 | Sentinel Value Match | contract left by an earlier attempt in the same output dir | file present, stale | Coordinator reads the old status | GAP (F-14) |
| WC-4 contract written | SPEC:62, SPEC:182 | Legitimate Edge Case | worker never sends `worker_done` | no contract, no outcome | 7.2 step 3 waits 900000 ms and names no outcome (SPEC:182) | GAP (F-13) |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | `status` absent or outside the four values | undefined | Not mapped; step 4 (SPEC:183) fails it only at check time | GAP (F-08) |
| WC-5 outcome mapping | SPEC:63, SPEC:263 | One/Minimal | `status: partial` | true, mapped to succeeded | Dependents unblock on a partial result | GAP (F-07) |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | audit verdict FAIL with `status: succeeded` | mapped to succeeded | Task completes; dependents become ready (`CAPS:90`) | GAP (F-07) |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | `status: blocked` | mapped to failed | Dependents stay blocked (`CAPS:90`) | OK |
| WC-9 outward gate | SPEC:67 | Zero/Empty | no outward flag in brief | off | No outward action | OK |
| WC-9 outward gate | SPEC:67, SPEC:61 | Sentinel Value Match | outward flag supplied through a WC-3 answer | on, not in brief | Outward action without the brief | GAP (F-02) |
| WC-10 wait limit | SPEC:68 | Typical | 3-minute wait | below 4 min | OK | OK |
| WC-10 wait limit | SPEC:68, SPEC:283 | Maximum | one poll-plus-sleep iteration against 240 s | runtime UNVERIFIED | Heartbeat margin unknown for pr-submit and cli-eval | GAP (UNVERIFIED, SPEC:283) |
| WC-1 readiness fallback | SPEC:59, `CAPS:49` | Typical | prompt falls back at 30 s | passes | OK | OK |
| WC-1 readiness fallback | SPEC:59, `CAPS:49` | Maximum | fallback at about 45 s | fails again | "well inside" is not quantified | GAP (F-11) |
| WC-11 default output path | SPEC:69, SPEC:85-86 | Zero/Empty | no `--output` given (index-repo, cleanup-audit) | fixed shared path | Two workers in one worktree write the same file | GAP (F-01) |
| WC-6 resume or fresh | SPEC:64, `CAPS:116` | Sentinel Value Match | retry with same output dir and no resume flag | fresh dir assumed | Stale file read as the new run | GAP (F-15) |
| WC-12 `consumer_fenced` | SPEC:70, `CAPS:67` | Legitimate Edge Case | `check` returns `consumer_fenced` | stop, no `worker_done` | Whether a contract is still written is not stated | GAP (F-13) |

Classes left out with reason: Maximum/Overflow for the `--unattended` switch and for WC-5 (boolean and enumerated values, no numeric bound); Maximum for WC-12 (a single signal). Every table row is complete for the guards it names.

## Findings

=== REQUIREMENTS ANALYSIS ===

**F-01. BLOCKING. Two rows contradict WC-11 (Wiegers; Hohpe on shared resources).**
- Issue: WC-11 says two workers in one worktree must never write the same file, and that default output paths carry a timestamp or the slug the coordinator passes (`SPEC:69`). The index-repo row passes no flag, writes a fixed `PROJECT_INDEX.md` (`SPEC:86`; `INV-A:53`), and is still ready-today. The cleanup-audit row writes a fixed `.claude-audit/` directory and `progress.json` (`SPEC:85`; `INV-A:42`) and is still ready-today. `SPEC:85` notes "one audit per worktree at a time" but no rule in 2.3 (`SPEC:73`) or section 6 enforces it. Workers share the current worktree by default (`CAPS:115`).
- Grading sentence: "An implementer who follows SPEC:85-86 as written dispatches two cleanup-audit or two index-repo workers into one worktree; both write `progress.json` or `PROJECT_INDEX.md`, so one run's output overwrites the other's, which WC-11 forbids. The two texts contradict each other, so the finding is blocking."
- Recommendation: make an output directory a required brief input for both (a per-slug flag), or move both rows to needs-change until it exists. Add to 2.3 that the coordinator does not run two of these in one worktree unless their output directories differ.
- Priority: High. Quality impact: high (silent overwrite of a run's result).

**F-02. BLOCKING. WC-3 lets a coordinator answer add outward flags and Rulings (Fowler on the flag interface; Cockburn on who authorises).**
- Issue: WC-3 lets a blocked worker ask the coordinator and then "re-invoke or resume the command with the answer as a flag" (`SPEC:61`). WC-9 says an outward action turns on "only through the command's own explicit flag written in the brief" (`SPEC:67`). D4(a) says a coordinator may authorise only what "the user's own instruction ... names" and quotes into the brief (`SPEC:245`). D2(a) says a Ruling may not come from another agent (`SPEC:234-236`, citing `INV-A:66`). WC-3 places no limit on the content of the answer.
- Grading sentence: "An implementer who follows WC-3 lets a worker whose auggie-review or post-release gate is blocked ask the coordinator, takes the coordinator's yes, and re-invokes the command with an outward flag that WC-9 says exists only in the brief. The two texts contradict each other, so the finding is blocking."
- Recommendation: WC-3 answers carry only values the brief marked askable and never outward flags or Rulings. Outward flags come from the brief or the person. Say so in WC-3 and D2.
- Priority: High. Quality impact: high (an unauthorised outward action, such as a PR or a push).

**F-03. BLOCKING. The WC-4 contract path is not known before dispatch for every command (Fowler; Newman on contract evolution).**
- Issue: WC-4 places the contract at `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed, and says the path is known before dispatch (`SPEC:62`, `SPEC:73`). Three rows break this. Workflow's brief passes only `--handoff none`, and its contract sits in `.dev/tasks/to-do/<id>/` where the run creates `<id>` (`SPEC:92`; `INV-B:52`; `INV-B:272`). Research's file name is generated at run time, and `INV-B:132` says the worker "must report the path it wrote" (`SPEC:116`). Adversarial's fixed path nests under `<output>/adversarial/`, not `<output-dir>/` (`SPEC:83`). Step 4 of 7.2 (`SPEC:183`) needs the path before the run ends.
- Grading sentence: "An implementer who follows SPEC:92 and SPEC:116 dispatches workflow and research with no output directory. The coordinator cannot name their contract path before dispatch, so it cannot open the file as SPEC:73 requires, and the 7.2 step 4 check has no file to test. The texts contradict each other, so the finding is blocking."
- Note: the fallback of reading the path from `worker_done --report-path` does not work as written: whether Orca reads that path is UNVERIFIED (`CAPS:79`), and the spec does not say how the coordinator reads a payload value.
- Recommendation: add `--output-dir` to workflow and research (P1). Put adversarial's contract at `<output-dir>/return-contract.yaml`, or change WC-4 to allow `<output-dir>/<command>/` and say so once.
- Priority: High. Quality impact: high (the coordinator cannot verify outcomes).

**F-04. BLOCKING. The acceptance check AC-C1 forbids the mention that SA-2 allows (Newman on interface evolution; Adzic on acceptance).**
- Issue: SA-2 allows "an example of a caller's question channel inside the contract file" (`SPEC:147`). P0 puts the contract in `src/superclaude/core/` and adds an Orca section to `HOW-WE-WORK.md` (`SPEC:150`, `SPEC:158`). AC-C1 runs in every phase over `src/superclaude/core` and excludes only `skills/ccsession-tag/` (`SPEC:172`). Its pattern matches `orca orchestration`, the form of the `ask` example (`CAPS:58`).
- Grading sentence: "An implementer who writes the example SA-2 allows into the core contract file, as P0 requires, makes AC-C1 print a match. AC-C1 must print nothing, so no P0 build passes its common checks (`SPEC:169`). The texts contradict each other, so the finding is blocking."
- Recommendation: exclude `src/superclaude/core/WORKER-CONTRACT.md` and the HOW-WE-WORK Orca section from AC-C1, or write the example so it does not match and say which form is allowed.
- Priority: High.

**F-05. BLOCKING. AC-1.1 requires a contract that the load row and the Decisions table forbid (Wiegers on traceability).**
- Issue: AC-1.1 requires every command in 3.1 and 3.2 to have an `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`). `load` is in 3.2 with report "none" and only a usage-line fix (`SPEC:112`). P1 gives `load` only the usage-line fix (`SPEC:159`). The Decisions table says a report file for `load` "would be an unrequested addition" (`SPEC:265`).
- Grading sentence: "An implementer who follows AC-1.1 adds a contract to `load.md`. The load row (`SPEC:112`) and the Decisions table (`SPEC:265`) forbid it, so the texts contradict each other and AC-1.1 cannot pass as written without breaking a decision. The finding is blocking."
- Recommendation: `load` is already a coordinator-side helper (`SPEC:139`). Move it out of 3.2, or drop it from AC-1.1 and say so.
- Priority: High.

**F-06. MEDIUM. The brief's `--unattended` requirement conflicts with the P0 and ready-today runs (Wiegers).**
- Issue: 2.3 says each brief states "the exact command line including `--unattended`" (`SPEC:73`). Section 3.1 says the ready-today commands "run as workers now" with the stated flags (`SPEC:77-79`), and P0 runs three commands before the flag exists (`SPEC:158`, `SPEC:159`). The spec does not say whether a P0 brief omits the flag.
- Grading: a missing requirement, since the implementer must guess that P0 briefs omit the flag. Medium.
- Recommendation: state in 2.3 that briefs for ready-today commands and for P0 omit `--unattended` until the command accepts it.

**F-07. MEDIUM. A partial or FAIL result completes the Task and releases its dependents (Nygard; Hohpe).**
- Issue: WC-5 sends `succeeded` for `partial` and for an audit whose verdict is FAIL (`SPEC:63`; rationale `SPEC:263`). Orca keeps dependents blocked only when a Task fails (`CAPS:90`). Nothing in 2.3 (`SPEC:73`) says the coordinator must gate the next wave on the contract's status.
- Grading: a stated text that lets a failed verdict unblock dependents, and no stated rule to stop it. The implementer must guess that the coordinator reads the file first. Medium.
- Recommendation: state that a `succeeded` Task with a contract status of `partial` or a FAIL verdict does not release dependents until the coordinator has read and accepted it.

**F-08. MEDIUM. Undefined terms the implementer must guess (Wiegers).**
- "safety flags" for `cli-eval run` (`SPEC:104`), "pre-confirmed context input" (`SPEC:117`), "spec-shaped input" (`SPEC:89`), and the "documented default" of WC-2(a) (`SPEC:60`). No list of defaults exists, and the table cells cannot be checked against one.
- Recommendation: define each term once, or list the exact flags per command.

**F-09. MEDIUM. The workflow row omits fields that WC-4 requires (Fowler; Newman).**
- WC-4 requires `status`, `command`, `report_path` and `artifacts` (`SPEC:62`). Step 4 of 7.2 asserts `command` (`SPEC:183`). `INV-B:272` lists only `status`, `plan_path` and `reflect_report_path`. The workflow row adds only pre-creation STOP coverage (`SPEC:92`), so following it yields a contract that fails step 4.
- Grading: a stated requirement (WC-4) and a row that does not implement it. Medium, since WC-4 says "add the missing ones" (`SPEC:62`) and the row may be read as covering it.
- Recommendation: list the added fields in the workflow row.

**F-10. MEDIUM. AC-0.4 step 4 is run against a file that cannot pass it (Adzic).**
- AC-0.4 says step 4 "uses the command's existing report file" (`SPEC:194`), but step 4 asserts `status` and `command` in a YAML file (`SPEC:183`). Troubleshoot's report is `REPORT.md` and its contract appears only with `--caller task-unified` (`INV-B:242`). The step fails for a reason unrelated to the behaviour under test.
- Recommendation: state which step-4 check P0 uses for troubleshoot, or drop troubleshoot from the P0 set.

**F-11. MEDIUM. "Well inside the readiness limit" is not quantified (Wiegers).**
- WC-1 requires a prompt fallback "well inside" the 60 s default (`SPEC:59`). The evidence in `CAPS:49` shows 30 s passes and about 45 s fails. The spec gives no threshold.
- Recommendation: state a maximum fallback, for example 30 s, and a test that proves it.

**F-12. MEDIUM. The step-2 pass condition may fail on a legitimate `ask` (Adzic; Hohpe).**
- 7.2 step 2 requires `observation.agentWait` never to be non-null (`SPEC:181`). WC-3 has the worker wait on an `ask` to the coordinator (`SPEC:61`). `CAPS:129` defines `agentWait` as a prompt "only a human can answer". Whether an `ask` answered by the coordinator sets `agentWait` is UNVERIFIED.
- Recommendation: state whether an `ask` sets `agentWait`, and exempt a worker that is waiting on an `ask`.

**F-13. MEDIUM. No outcome is defined for a worker that never reports (Nygard).**
- 7.2 step 3 waits 900000 ms and then states no outcome (`SPEC:182`). WC-4 is written "on every outcome" (`SPEC:62`) but a worker that never sends `worker_done` produces no outcome at all. `CAPS:126` says a wait ends only on positive proof of a stop. A brief that omits `--unattended` (`SPEC:73`) stalls with no timeout rule.
- Grading: a missing requirement (no timeout or stop rule). Medium.
- Recommendation: state what the coordinator does after a timeout (for example, check `worker-show` and stop on positive proof), and that a worker stopped by `consumer_fenced` writes its contract before it stops (`SPEC:70`).

**F-14. MEDIUM. A stale contract in a reused output directory is read as the new result (Whittaker; Hohpe).**
- WC-4 does not say to remove an earlier contract at start (`SPEC:62`). WC-6 allows resume into the same directory (`SPEC:64`), and WC-5 maps the file's status to the outcome (`SPEC:63`). A retry that dies before writing reports the old `succeeded`.
- Recommendation: delete or rename any contract at worker start, and put a run or dispatch ID in the contract so the coordinator can match it to the attempt.

**F-15. MEDIUM. Retries have no contract path rule (Fowler).**
- A retry uses `worker-start --retry-of` (`CAPS:116`). WC-6 says a retry must not corrupt the first attempt's output (`SPEC:64`), but the spec does not say which output directory or contract path the retry uses. That breaks WC-4's "known before dispatch" rule (`SPEC:62`) on every retry.
- Recommendation: state that a retry gets a new `--output-dir` (or a resume flag), and that the coordinator records the new path.

=== ARCHITECTURE ANALYSIS ===

**F-16. MEDIUM. Tasklist's reflect fan-out is assumed to be inside the nesting limit (Newman; Nygard).**
- Section 3.2 says tasklist's "reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, INV-A:14" and needs no change (`SPEC:122`). `INV-A:14` is a documentation quote about the depth limit, and it says that at the limit the Agent tool is withheld. `INV-B:210` marks nested spawning UNVERIFIED. `INV-B:215` lists the required change as "the per-phase reflect fan-out must run at the worker's top level". `SPEC:45` says nesting has no proven limit. The spec drops the inventory's required change without evidence.
- Grading: depends on a guess that the nesting limit is reached. Medium, and it can become blocking if a test shows the fan-out is removed.
- Recommendation: keep `INV-B:215`'s change, or add an acceptance check that proves Stage 10.5 subagents keep their Agent tool.

**F-17. MEDIUM. The rejection of the in-command fan-out rests on a presumption (Fowler).**
- R1 says a command that calls `worker-start` inside a worker "would be refused with `nested_worker_depth_exceeded`" (`SPEC:33`). The same sentence says which call sites enforce the check is UNVERIFIED (`CAPS:103`). R1's conclusion that the two designs "exclude each other" depends on that presumption.
- Recommendation: mark R1 conditional, and add a P0 check that a depth-1 worker's `worker-start` fails.

**F-18. MEDIUM. Repeated blocked outcomes are not paired with a rule to fix the brief (Nygard).**
- WC-5 maps `blocked` to `failed` (`SPEC:63`). After three consecutive failures the Task circuit-breaks (`CAPS:120-122`). A brief with a missing value (for example `target_release`, `SPEC:120`) fails three times the same way. The spec says nothing about changing the brief rather than retrying.
- Recommendation: state that a `blocked` contract's `blocked_question` must be answered in the brief before any retry.

=== ADVERSARIAL ANALYSIS (Whittaker, FR-2.1 to FR-2.5) ===

- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **the contract's `status` is an empty string**. Concrete attack: **a worker writes `status: ""`; WC-5 maps no outcome; step 4 fails only at check time (F-08).**
- I can break this specification by **Divergence Attack**. The invariant at **WC-5 (`SPEC:63`, `SPEC:263`)** fails when **the audit verdict is FAIL but the status is `succeeded`**. Concrete attack: **a standalone adversarial audit returns FAIL; the Task completes and dependents start (`CAPS:90`) (F-07).**
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-3 (`SPEC:61`) with WC-9 (`SPEC:67`)** fails when **the coordinator's answer equals an outward flag**. Concrete attack: **the worker's `ask` for "post the review?" is answered "yes", and auggie-review re-runs with `--post-pr` (F-02).**
- I can break this specification by **Sequence Attack**. The invariant at **WC-4 (`SPEC:62`) with WC-6 (`SPEC:64`)** fails when **a retry reuses the output directory and dies before writing**. Concrete attack: **the coordinator reads the first attempt's `status: succeeded` (F-14).**
- I can break this specification by **Accumulation Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **the same blocked gate recurs**. Concrete attack: **three retries hit the same missing `target_release`, the circuit-breaker fails the Task, and the spec states no fix (F-18).**

## Synthesis

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Newman, Hohpe, Nygard; Whittaker (adversarial, always active)
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 4.5
  clarity: 6
  completeness: 6
  testability: 4
  consistency: 3
critical_issues:
  - {id: F-01, category: requirements, severity: CRITICAL-BLOCKING, expert: Wiegers, issue: "WC-11 contradicted by ready-today index-repo and cleanup-audit rows", recommendation: "per-slug output dir required; coordinator never runs two in one worktree"}
  - {id: F-02, category: architecture, severity: CRITICAL-BLOCKING, expert: Fowler, issue: "WC-3 answer may be re-invoked as an outward flag, contrary to WC-9 and D2/D4", recommendation: "limit WC-3 answers; outward flags and Rulings only from brief or person"}
  - {id: F-03, category: architecture, severity: CRITICAL-BLOCKING, expert: Fowler, issue: "WC-4 contract path not known before dispatch for workflow, research, adversarial", recommendation: "single output-dir rule; add --output-dir to workflow and research"}
  - {id: F-04, category: architecture, severity: CRITICAL-BLOCKING, expert: Newman, issue: "AC-C1 forbids the contract mention SA-2 allows", recommendation: "exempt the core contract and HOW-WE-WORK section, or change the example"}
  - {id: F-05, category: requirements, severity: CRITICAL-BLOCKING, expert: Wiegers, issue: "AC-1.1 requires a contract for load, which the load row and Decisions forbid", recommendation: "move load out of 3.2 or drop it from AC-1.1"}
expert_consensus:
  - "Wiegers, Fowler and Nygard agree that the contract needs one path rule and one outcome rule; the spec has two of each and they disagree (F-01, F-03, F-07)."
  - "Whittaker and Fowler agree that the coordinator's answer channel (WC-3) must not carry authority it does not hold (F-02)."
improvement_roadmap:
  immediate: [F-01, F-02, F-03, F-04, F-05]
  short_term: [F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15, F-16, F-17, F-18]
  long_term: [N-1, N-2, N-3]
```

## Follow-up candidates (Medium and minor; not blocking; not in any revision brief)

- F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15, F-16, F-17, F-18 (Medium).
- N-1: `SPEC:11` says eleven `src/` locations were re-read on 2026-11-02. Not checkable in this sandbox (UNVERIFIED here).
- N-2: `SPEC:24` (E5 grep result), `SPEC:74` (`CLAUDE.md:74`), and `SPEC:183` (`pyproject.toml:38`, PyYAML) cite files absent from the sandbox (UNVERIFIED here). The 10 / 27 / 6 totals and the per-command rows agree with the inventories.
- N-3: `SPEC:105` says `cli-portify` runs only inside an IronClaude checkout. That is a standalone-use limit that section 5 does not mention.
- The session that ran this review asks the user once, per loop, whether to open an issue for these. No issue is created here.

## Reviser brief

Revise only the text that blocking findings F-01 to F-05 name. Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

verdict: FAIL
