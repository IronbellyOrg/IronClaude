review: 1 of 3

# Spec-panel critique: Orca worker contract spec

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture`, FIRST-REVIEW prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 286 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: missing (first review). Prior report: none.
- Reviewer model: claude-haiku-5-5.
- Shorthand: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md` line N.

## Coverage and limits

- Read in full: the candidate, `README.md`, the three inventories, `command.md`, and the FIRST-REVIEW prompt file.
- Citations checked against files in the workspace: every `SPEC:`, `INV-A:`, `INV-B:`, `CAPS:` and `README:` citation I used. The spec's own `INV-A:`/`INV-B:`/`CAPS:` pointers resolve to the lines they describe (N2 lists the lines I checked).
- UNVERIFIED in this sandbox: every path:line citation to a file outside `.dev/orca-command-refactor/` (`src/superclaude/...`, `tests/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `/opt/Orca/...`, `CLAUDE.md`, `pyproject.toml`, `plugins/...`, `EVIDENCE.md`, `orca-data.json`). I did not treat those as evidence for or against any finding.
- Not performed: the three first reviews and the MERGE rule (this worker has no subagent tool, so it cannot brief three fresh-context reviewers), and the VERIFY pass (no fresh-context verifier). This file is one first review. Blocking findings below are provisional until a fresh-context VERIFY confirms them. My own re-reads are not a fresh-context check.
- Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data flow whose counts may diverge. The one many-to-few mapping (WC-5, four statuses to two outcomes) is covered in the Guard table.
- Adversarial probing (Whittaker) is active in every panel review and is recorded below as attack findings.

## Summary

The spec is well sourced and its central decision (Orca coordinates, commands stay units of work) is argued with evidence that I could trace in the inventories. The counts are consistent: 10 ready, 27 needs-change, 6 coordinator-only, summing to the 43 commands (`SPEC:75-76`, `INV-A:3`, `INV-B:3`). Four findings are blocking: an acceptance check that cannot pass in Phase 0 (B1), a Phase 1 state that posts to GitHub under `--unattended` (B2), a default output path that breaks the spec's own no-shared-file rule (B3), and a load contract contradiction (B4). Medium findings and minor notes follow.

## Guard Condition Boundary Table (mandatory; FR-10 synthesis gate)

Triggered by the spec's gates, thresholds and flag guards. Columns as in the command template. Input classes that cannot occur for a guard are omitted within its rows, and the omission is stated under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome map | `SPEC:63` | Zero/Empty: no report file | (absent) | `--outcome failed` | "or no report exists" (`SPEC:63`) | OK |
| WC-5 outcome map | `SPEC:63` | Zero/Empty: zero-byte contract | `""` | undefined (file exists, no `status`) | not stated; AC-0.4 needs `test -s` (`SPEC:183`) | GAP (M13) |
| WC-5 outcome map | `SPEC:63` | Typical: `status: succeeded` | `succeeded` | `--outcome succeeded` | stated | OK |
| WC-5 outcome map | `SPEC:63` | Typical: `status: blocked` | `blocked` | `--outcome failed` | stated | OK |
| WC-5 outcome map | `SPEC:63` | Sentinel: `status` outside the four values | `done` | undefined | not stated | GAP (M13) |
| WC-5 outcome map | `SPEC:63`, `SPEC:263` | Legitimate Edge: `partial`, or audit verdict FAIL | `partial` | `--outcome succeeded` | Task completes and dependents become ready (`CAPS:34`, `CAPS:90`); no rule holds them back | GAP (M2) |
| WC-2 / WC-9 gate with outward default | `SPEC:60`, `SPEC:67`, `SPEC:100` | Typical: `--unattended` on auggie-review, no `--post-pr` | flag set | posting off | `--unattended` implies `--no-post-pr` (`SPEC:100`) | OK (P2 only) |
| WC-2 / WC-9 gate with outward default | `SPEC:159` vs `SPEC:100` | Edge: `--unattended` on auggie-review under P1 alone | flag set, gate not converted | posting on | P1 accepts the flag; WC-9 says posting is off | GAP (B2) |
| WC-9 | `SPEC:67` | Sentinel: brief passes explicit `--post-pr` | both | posting on | user instruction required (D4, `SPEC:245-246`) | OK |
| WC-4 contract written | `SPEC:62` | Zero/Empty: pre-creation STOP, output dir absent | no directory | contract must still be written | "including stops before any other output exists"; creating the directory is not stated | GAP (minor, N3) |
| WC-4 contract written | `SPEC:112`, `SPEC:265`, `SPEC:195` | Zero/Empty: `load` in unattended mode | no contract | row says none; WC-4 and AC-1.1 require one | contradiction | GAP (B4) |
| WC-6 retry | `SPEC:64`, `SPEC:73` | Typical: `--retry-of` with the same `--output` (no resume flag) | same directory | first attempt's files overwritten | WC-6 forbids corruption; 2.3 gives no fresh-directory rule | GAP (M3) |
| WC-6 resume | `SPEC:109` | Typical: `implement` with a matching ledger, no flag | ledger present | implicit resume | WC-6 names resume "when given its resume flag" | GAP (minor, M3) |
| WC-10 wait | `SPEC:68` | Typical: one call of 240 s | 240 s | allowed | "at most 4 minutes" | OK |
| WC-10 wait | `SPEC:68` | Edge: one call of 241-300 s | 300 s | forbidden | stated | OK |
| WC-10 wait | `SPEC:68`, `SPEC:210` | Zero/Empty: poll-script runtime unknown | UNVERIFIED | cannot decide | acknowledged (`SPEC:283`, UNVERIFIED 12) | GAP (minor, N4) |
| WC-12 fence | `SPEC:70`, `CAPS:67` | Sentinel: `check` returns `consumer_fenced` | value | stop, no `worker_done` | stated | OK |
| WC-12 fence | `SPEC:70`, `CAPS:66-67` | Zero/Empty: empty `check` | none | keep running | `CAPS:67` | OK |
| WC-1 readiness | `SPEC:59` | Typical: prompt fallback at 30 s | 30 s | passes | `SPEC:59` cites `EVIDENCE.md:45` (UNVERIFIED path) | OK |
| WC-1 readiness | `SPEC:59` | Edge: fallback at 50 s | 50 s | inside the 60 s default | "well inside" undefined; the failure evidence was at a 45 s limit (`CAPS:49`) | GAP (M1) |
| SA-3 standalone | `SPEC:148`, `SPEC:92`, `SPEC:83` | Zero/Empty: plain run, no flags, workflow pre-creation STOP | no flags | no new file (SA-3) vs contract written (P1 fix) | contradiction | GAP (M11) |
| WC-11 default path | `SPEC:69`, `SPEC:86` | Typical: index-repo default, no output flag | `PROJECT_INDEX.md` | fixed path, no timestamp or slug | WC-11 requires a timestamp or slug | GAP (B3) |

Omitted input classes: Maximum/Overflow is omitted for every guard because the spec states no counter or capacity bound (the `--timeout-ms` upper bound is UNVERIFIED, `CAPS:54`). Sentinel is omitted for WC-1, WC-4, WC-6 and WC-10 because no sentinel value is defined for them. Zero/Empty is omitted for WC-9 because an empty brief takes the default, which the Typical row covers.

GAP count: 12 rows. Three are blocking (B2, B3, B4). Six are Medium (M1, M2, M3, M11, and M13 twice). Three are minor (N3, N4, and the WC-6 implicit-resume row under M3). FR-10 is met: the table is complete for the guards the spec states.

## Blocking findings

### B1. Phase 0 acceptance check AC-0.4 cannot pass as written. CRITICAL.
- Location: `SPEC:194` (AC-0.4), `SPEC:182` (7.2 step 3), `SPEC:183` (7.2 step 4), `SPEC:158` (P0 scope).
- Expert: Adzic (examples), Crispin (test completeness), Wiegers (testability).
- Wrong outcome: AC-0.4 says "steps 1-3 and 5-7 pass". Step 3's pass condition requires "its report path is the WC-4 contract path" (`SPEC:182`). P0 writes no WC-4 contract; the contract "arrives in P1" (`SPEC:194`). So step 3 cannot pass in P0. AC-0.4 also redefines step 4 to use "the command's existing report file" (`SPEC:194`), but step 4's pass condition requires a YAML file with `status` in four values and a `command` key (`SPEC:183`). An existing REPORT.md or a `.md` does not satisfy it.
- Grading sentence: an implementer who follows AC-0.4 as written cannot make steps 3 and 4 pass in P0, so the P0 gate is unpassable (`SPEC:158` says P0 tests the decision, and section 1.4 at `SPEC:43` makes that test the gate). Either the implementer declares a pass the check does not support, or the phase never closes.
- Recommendation: restate AC-0.4 for P0 with its own pass conditions: step 3 checks `worker_done` exactly once and its `--outcome` against the existing report's first-sentence status; step 4 is dropped in P0 and run first in P1. Delete the sentence that calls step 4 "uses the command's existing report file".
- Priority: High. Quality impact: high (the spec's gate on its central decision).

### B2. Phase 1 lets `--unattended` run with PR posting still on. CRITICAL.
- Location: `SPEC:159` (P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"), `SPEC:160` (P2 converts gates, including auggie-review), `SPEC:100` (auggie-review row: `--unattended` implies `--no-post-pr`, posting only with `--post-pr`), `SPEC:67` (WC-9).
- Expert: Fowler (interface and phase boundary), Nygard (safety under partial rollout), Cockburn (actor: the coordinator's brief).
- Wrong outcome: "a no-op where a command has no gate" implies that for a gated command the flag must do something in P1. P1 does not include gate conversion (that is P2). An implementer who follows P1 as written either (a) accepts the flag as a no-op for auggie-review, so `/sc:auggie-review <PR> --unattended` still posts to GitHub by default, or (b) implements the P2 gate inside P1, which P1's scope does not name. Both readings either violate WC-9 or contradict the phase split.
- Grading sentence: an implementer who follows `SPEC:159` as written builds auggie-review that accepts `--unattended` and still posts review comments to the PR, and that is wrong because WC-9 (`SPEC:67`) says a default that posts to GitHub is off under `--unattended`. The phase text and the P2 assignment (`SPEC:160`) contradict each other on this one command.
- Recommendation: either move auggie-review's flag acceptance to P2, or make P1 reject `--unattended` for any command whose gate is not yet converted (fail closed). State which in `SPEC:159`. Add an AC-1 check that auggie-review under `--unattended` posts nothing in P1.
- Priority: High. Quality impact: high (outward action).

### B3. Default output path breaks WC-11 for index-repo. MAJOR.
- Location: `SPEC:69` (WC-11: "Default output paths carry a timestamp or the slug the coordinator passes"), `SPEC:86` (index-repo: brief passes "none"; report `PROJECT_INDEX.md`; fix is "State the output location (P1)"), `SPEC:85` (cleanup-audit: fixed output dir, "one audit per worktree at a time (WC-11)"), `INV-A:53` (index-repo has no output parameter, default at repo root).
- Expert: Fowler (interfaces), Hohpe (shared channel), Newman (evolution).
- Wrong outcome: an implementer who follows `SPEC:86` builds index-repo with the default `PROJECT_INDEX.md` and no output flag, so the coordinator cannot pass a slug. WC-11 says a default output path carries a timestamp or a slug. The 3.1 fix ("state the output location") does not add one. cleanup-audit (`SPEC:85`) cites WC-11 but does not satisfy it either; its fix is a coordinator rule that is absent from the 2.3 brief.
- Grading sentence: an implementer who follows `SPEC:86` writes `PROJECT_INDEX.md` as a fixed default with no slug, and that is wrong because WC-11 (`SPEC:69`) says default output paths carry a timestamp or the slug the coordinator passes; the sentence needs no further assumption.
- Recommendation: give index-repo an `--output` flag (P1) and add it to the brief column, or move index-repo to needs-change. For cleanup-audit, add "one audit per worktree" to the 2.3 brief rules as a coordinator obligation.
- Priority: Medium-High. Quality impact: medium (overwrite of a shared index).

### B4. The load row contradicts WC-4 and AC-1.1. MAJOR.
- Location: `SPEC:112` (load: "Report (WC-4): none"), `SPEC:265` (Decisions: a report file for load "would be an unrequested addition"), `SPEC:76` (every changed command gains the Unattended section), `SPEC:195` (AC-1.1: every command in 3.1-3.2 has a section "naming return-contract.yaml"), `SPEC:62` (WC-4: changed commands write the contract in unattended mode).
- Expert: Wiegers (traceability), Crispin (acceptance check).
- Wrong outcome: load is listed under "Needs a change" (`SPEC:112`), so WC-4 applies to it, but its row and its Decision say it writes no file. AC-1.1 then requires a section that names a file load never writes.
- Grading sentence: an implementer who follows the load row and the Decision writes no contract, and that is wrong because WC-4 (`SPEC:62`) requires one for every changed command, and AC-1.1 (`SPEC:195`) fails for load without an invented section.
- Recommendation: remove load from the section 3.2 table and from AC-1.1 (it is a context loader, `SPEC:265`), or give it a contract that reports "loaded: <keys>". Pick one.
- Priority: Medium-High (small consequence, since `SPEC:112` also says load is not dispatched as its own Task). Quality impact: low to medium.

## Requirements analysis (=== REQUIREMENTS ANALYSIS ===)

Medium findings are follow-up candidates. They do not block.

- **M1 (Medium). WC-1 readiness margin rests on the wrong evidence.** Expert: Nygard. `SPEC:59` cites `EVIDENCE.md:45,56` ("above about 45 s it fails") for the 60 s default. The inventory quotes that run as "worker-start failed after the 45-second limit given" (`CAPS:49`, quoting EVIDENCE:39). The 45 s figure is a limit that run set, not the 60 s default (`CAPS:44-45`). A fallback at 50 s is "well inside" 60 s only by the spec's own words, and the evidence does not cover it. Recommendation: state a fallback number (e.g. 30 s, the value that passed) and remove "well inside".

- **M2 (Medium). Partial and FAIL-verdict results unblock dependents.** Expert: Hohpe, Cockburn. `SPEC:63` maps partial and an audit with verdict FAIL to `succeeded`, and `SPEC:263` justifies it as "the work is not lost". Orca completes the Task on `succeeded` and a failed Task keeps dependents blocked (`CAPS:34`, `CAPS:88-90`). The spec says the coordinator "opens the report file" (`SPEC:73`) but states no rule that stops dependents on partial or FAIL output. The spec's own ready-wave pattern (`CAPS:86`) would start them. Recommendation: add a 2.3 rule: a dependent Task starts only when the contract status is `succeeded`, or the coordinator records a decision to accept partial output.

- **M3 (Medium). Retry and resume freshness is unspecified.** Expert: Nygard. `SPEC:64` (WC-6) says a retry must not corrupt output, and a command with no resume flag "writes each run into a fresh output directory". Section 2.3 (`SPEC:73`) has the coordinator pass `--output` for each Task and says nothing about a retry. Whether the command or the coordinator chooses the fresh directory is not stated. `implement` resumes implicitly (`SPEC:109`), while WC-6 names a resume flag. Recommendation: state that the coordinator passes a new `--output` for every `--retry-of` dispatch, and reword WC-6 so a resume requires a flag (or add the implicit case as an explicit rule).

- **M4 (Medium). `ask`-then-resume within one session is undefined.** Expert: Fowler. WC-3 (`SPEC:61`) says that after `ask` the session "re-invoke[s] or resume[s] the command with the answer as a flag". The command is still running in the same session, so no re-invocation is defined and the answer's route into a mid-run gate is unspecified. Recommendation: say whether the command exits and is re-run by the same worker with the flag, or continues in-session.

- **M5 (Medium). Stall, crash and timeout have no coordinator action.** Expert: Nygard. Step 2 (`SPEC:181`) detects a parked worker (`agentWait`), and step 3 (`SPEC:182`) waits up to 900 s. No rule says what the coordinator does next. Orca forbids release on timeout or silence (`CAPS:111`) and says absence never authorizes retry (`CAPS:125`). Recommendation: add a 2.3 rule: on `agentWait`, the coordinator answers through `reply` or waits; on `exited` liveness with no `worker_done`, it may retry only after the settlement receipt; never release on timeout.

- **M6 (Medium). `--unattended` does not propagate into nested skills.** Expert: Hohpe, Fowler. Nested invocations exist: tdd calls `/task`, whose "ask the user" lines the spec says must resolve as blocked (`SPEC:90`, `INV-B:47,217-225`); tasklist's Stage 9 calls `sc:task` (`INV-B:46`); workflow calls reflect (`INV-B:52`). Only tasklist-to-reflect is stated (`SPEC:122`). Section 5 (`SPEC:149`, SA-4) and AC-C5 (`SPEC:176`) cover command files only, so skill gates can change without the additive rule. Recommendation: define the propagation channel (the flag, or an environment marker the nested skill reads), and state that edits to skill gates are covered by SA-1.

- **M7 (Medium). WC-9 does not cover file moves, and some outward defaults have no flag.** Expert: Cockburn. WC-9 (`SPEC:67`) lists push, PR, GitHub, install, provisioning and paid runs. reflect's default-on Wave 7 moves the validated work-unit folder (`INV-B:114`), and the 3.1 row (`SPEC:88`) says `--no-promote` only "when the coordinator owns folder moves". The brief list (`SPEC:73`) does not require that flag. For post-release and task's commit and push, WC-9 says the "command's own explicit flag" turns the default on (`SPEC:67`), but no flag is named (`SPEC:113`, `SPEC:121`). Recommendation: add folder moves to WC-9's list, make `--no-promote` mandatory in the brief for reflect under unattended, and name the flags for post-release and task.

- **M8 (Medium). Two claims go beyond the evidence.** Expert: Fowler, Adzic. E2 says a worker "has the same tools as a command a person runs" (`SPEC:22`). The inventory marks nested tool availability UNVERIFIED (`INV-B:314`, `INV-A:112`). The tasklist row says reflect runs "inside Claude Code's nesting limit" (`SPEC:122`), while INV-B:210 marks nested spawning UNVERIFIED. Recommendation: say "UNVERIFIED until AC-0.4" in both places.

- **M9 (Medium). Evidence for the direct route contradicts itself.** Expert: Wiegers. E3 (`SPEC:23`) cites the P3 return contract with `invocation_method: "skill-direct"` as evidence the approach has worked. Section 1.4 (`SPEC:43`) says "the only end-to-end proof is the PR #329 run" and that it used the nested route. The inventory credits the skill-direct contract to the same kind of run (`INV-A:13`, `INV-A:35`: "Proven as a direct Orca-worker skill call"). Either the P3 run is a separate direct-route proof, or E3 is wrong. Recommendation: name the run behind each `skill-direct` citation and reconcile E3 with 1.4.

- **M10 (Medium). AC-C1 would fail on the file SA-2 allows.** Expert: Quality engineering (Crispin). AC-C1 (`SPEC:172`) greps `src/superclaude/core` with no exception for the new contract. SA-2 (`SPEC:147`) allows "an example of a caller's question channel inside the contract file", and P0 (`SPEC:158`) adds an Orca section to `HOW-WE-WORK.md` in the same tree. An implementer who keeps the allowed example fails AC-C1. Recommendation: add `WORKER-CONTRACT.md` to the AC-C1 exclusion list and say whether the HOW-WE-WORK section may name `orca` commands.

- **M11 (Medium). SA-3 and the P1 fixes conflict.** Expert: Wiegers. SA-3 (`SPEC:148`) says a standalone default run writes the same files it writes today. The P1 fixes change standalone output without a flag: adversarial renames its contract (`SPEC:83`), and workflow writes a contract for pre-creation STOPs (`SPEC:92`). SA-4 (`SPEC:149`) allows defect fixes, but SA-3 has no such exception. Recommendation: put the defect-fix exception in SA-3 too, or gate the new workflow STOP write on `--unattended`.

- **M12 (Medium). cli-eval's "safety flags" are unnamed.** Expert: Adzic. The row (`SPEC:104`) says `run` "requires `--suite` and the safety flags in the brief". The inventory names the confirmation as covering "invocation and safety flags" (`INV-A:44`) without naming them. AC-2.2 (`SPEC:200`) tests only the missing `--suite`. Recommendation: list the flags in the row and add a second gate-trigger case.

- **M13 (Medium). The contract-to-outcome mapping has no rule for malformed contracts.** Expert: Hohpe, Whittaker. WC-5 (`SPEC:63`) covers "report says failed or blocked", "no report exists" and "otherwise". A zero-byte file, unparseable YAML, or a `status` outside the four values falls into "otherwise", which maps to `succeeded`. Recommendation: map any unreadable or unknown contract to `failed`.

- **M14 (Medium). Two copies of the flag table, and no contract version.** Expert: Newman. The flag list lives in the spec (section 3.1) and in the contract's brief template (P0, `SPEC:158`). They will drift, which SA-5's concern (`SPEC:150`) anticipates. WC-4 says the contract "carries at least" its listed fields (`SPEC:62`), with no version key, so a coordinator cannot tell which fields it can rely on. Recommendation: make the contract the single source for flags and add a `contract_version` field.

- **M15 (Medium). The 3.1 "brief must pass" column omits `--unattended`.** Expert: Cockburn. Section 2.3 (`SPEC:73`) says every brief includes `--unattended`. The 3.1 rows (`SPEC:83-92`) list flags without it, and WC-4 applies only in unattended mode (`SPEC:62`). A coordinator following the 3.1 column gets no contract. Recommendation: add `--unattended` to each 3.1 brief column, or state that the 3.1 column describes the P0 state only.

## Architecture analysis (=== ARCHITECTURE ANALYSIS ===)

- **M16 (Medium). Where the unattended mode is read.** Expert: Fowler. Each command's `## Unattended mode` section "lists only its own gate resolutions" (`SPEC:52`), but most gates sit in skills the command activates (for example `sk/tdd/SKILL.md:52-61`, cited at `SPEC:90`). The spec never says whether a skill reads the command's mode or its own flag. Recommendation: define the mode's channel once, in the contract, and say which file carries each gate.

- **M17 (Medium). Coordinator-only and worker boundaries are sound but the brief template is unspecified.** Expert: Newman. Section 2.3 lists what a brief must state (`SPEC:73`) but gives no template, while P0 says the contract includes "a coordinator brief template" (`SPEC:158`). Recommendation: include the template in the spec, or delete the phrase.

## Adversarial probing (Whittaker, always active)

- **W1. Retry while the first attempt is parked.** I can break this specification by a Sequence attack. The invariant at WC-6 (`SPEC:64`) fails when a retry starts while the first Dispatch is still live. Concrete attack: a worker parks in `ask` (`agentWait` non-null, `SPEC:181`); the coordinator, seeing no `worker_done`, runs `worker-start --retry-of` with the same `--output`. Orca forbids that inference: "Absence never authorizes stop, abandon, retry, or release" (`CAPS:125`), but the spec does not restate it, so both attempts write the same contract. Medium (M5).
- **W2. Zero-byte contract.** I can break this specification by a Zero/Empty attack. The invariant at WC-5 (`SPEC:63`) fails when a zero-byte `return-contract.yaml` exists: "no report exists" is false and "otherwise" maps it to `succeeded`. Concrete attack: a disk-full write leaves an empty file, and the worker reports success. Medium (M13).

## Minor notes

- N1. The 10/27/6 split and the 43-command total are consistent with both inventories (`SPEC:75-76`, `INV-A:73`, `INV-B:278`, `INV-A:3`, `INV-B:3`). Verified.
- N2. Citation check, inventory pointers: `SPEC:83-92` (3.1), `SPEC:99-125` (3.2) and `SPEC:130-137` (section 4) match their inventory rows (`INV-A:35,37-55,36,90`; `INV-B:31-52,32-49,50-51`). Verified by reading the lines.
- N3. WC-4 (`SPEC:62`) requires a contract "including stops before any other output exists", but does not say who creates the output directory when it is absent. Minor: the worker is expected to create it, and the rule should say so.
- N4. WC-10 poll-iteration runtime is UNVERIFIED (`SPEC:210`, `SPEC:283`). The spec already gates pr-submit on it in P4, so no phase is blocked by it yet.
- N5. The spec's UNVERIFIED list (`SPEC:272-285`) covers the items I checked in section 1 and section 3. No other gap found.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| One first review in this worker, not three | Brief three fresh-context reviewers, or report one | No subagent tool is available in this sandbox. The file is labelled review 1 of 3 and marked provisional. |
| Verdict FAIL | PASS with notes, or FAIL | B1-B4 each name a contradiction or an unpassable check, which is blocking under the FIRST-REVIEW grading check. |
| Guard table covers the guards the spec states | Full enumeration of every conditional sentence | FR-10 requires completeness for the stated guards. Only the spec's own guards are in scope, not every sentence in the file. |
| Pipeline Dimensional Analysis not triggered | Treat WC-5 as a count pipeline | WC-5 maps statuses to outcomes; it does not transform counts. Covered in the Guard table. |

## follow-up candidates (Medium and minor; not blocking)

M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17, W1, W2 (Medium), N1-N5 (minor). The running session asks the user once whether to open an issue for these. This worker creates none.

## Reviser brief

Revise only text the following blocking findings name: B1 (`SPEC:194`, `SPEC:182-183`), B2 (`SPEC:159`, `SPEC:100`), B3 (`SPEC:69`, `SPEC:86`), B4 (`SPEC:112`, `SPEC:265`, `SPEC:195`). Restating the command's rule: add no rule, mechanism or section that a blocking finding does not call for; prefer deleting or narrowing to adding; cite the finding id on every addition; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief and must not be edited under it.

verdict: FAIL
