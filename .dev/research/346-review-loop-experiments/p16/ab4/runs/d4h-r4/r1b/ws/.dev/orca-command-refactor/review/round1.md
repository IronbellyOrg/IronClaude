review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

- Mode: `--mode critique`, `--focus requirements,architecture`. First review: no `--re-review`, no `--baseline`, so no baseline line applies.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (285 lines).
- Lint: `.dev/orca-command-refactor/review/lint-1.md` (review-lint/1, sha256 `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`). Its recorded candidate hash equals the candidate hash above, so the lint is not stale.
- Reviewer model: claude-haiku-5-5 (one worker, one review).
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full at the sandbox home path. Command definition read in full at `command.md`.
- Panel: Requirements (Wiegers lead, Adzic, Cockburn), Architecture (Fowler lead, Newman, Hohpe, Nygard). Whittaker is active in every panel review and is included.
- Brief addition: every acceptance criterion (AC) and every live-check step was checked one by one (section 4).

## Process deviations and limits (read first)

1. The FIRST-REVIEW prompt asks for two fresh-context first reviews, then the MERGE rule, and the VERIFY prompt asks for a fresh-context verifier. This worker cannot start fresh-context reviewers or verifiers, so this file is one review. No MERGE and no VERIFY were run. The five blocking findings below are checked by this worker against the cited lines, but they are not VERIFY-confirmed. The coordinator must run the second first review, the MERGE, and VERIFY before any revision. The verdict is provisional on that basis.
2. Evidence limits. The sandbox holds only the spec, the three inventories, lint and the run README. Citations to `src/superclaude/`, `tests/`, `pyproject.toml`, `.dev/evals/`, `.dev/codegraph-migration/`, the Orca install and the project CLAUDE.md cannot be checked here and are marked UNVERIFIED. Inventory and capability citations were checked against the file text. Spot-checked: CAPS:46, 79, 92, 129, 150, 155, 161, 187; INV-A:14, 35, 51, 60, 62, 68, 113; INV-B:49, 52, 210, 242, 272, 301, 311, 314, 322, 323.
3. Citation key: `spec:N` is line N of the candidate. `INV-A:N`, `INV-B:N` and `CAPS:N` are lines of `inventory/commands-a.md`, `inventory/commands-b.md` and `inventory/orca-capabilities.md` under `.dev/orca-command-refactor/`.

## Lint evidence

`review/lint-1.md:3-5`: "Checks: REF. Findings: 0. No findings." No lint id exists, so none is confirmed or dismissed. Lint is not a source of findings in this report.

## Guard Condition Boundary Table (mandatory artifact)

The spec contains conditional logic, threshold checks and boolean guards (WC-2, WC-4, WC-5, WC-6, WC-10 and the step-4 check), so this table is triggered. The Pipeline Dimensional Analysis heuristic is not triggered: no data flow changes counts across stages. The State Variable Registry is not triggered (no `--focus correctness`). Classes left out of a guard are noted in the Specified Behavior column with the reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty | report file exists, 0 bytes | no status read | "otherwise succeeded" (spec:63); step 4 requires `test -s` (spec:183) | GAP (M16) |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: partial` | `succeeded` | spec:63, spec:263 | OK |
| WC-5 outcome mapping | spec:63 | Typical | `status: succeeded` | `succeeded` | spec:63 | OK |
| WC-5 outcome mapping | spec:63 | Maximum/Overflow | status value outside {succeeded, partial, failed, blocked} | unspecified | not stated | GAP (M16) |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | prose says "failed", field says `succeeded` | ambiguous | "when the report says failed" does not say whether the field or the prose governs | GAP (M16) |
| WC-5 outcome mapping | spec:63 | Legitimate Edge | audit verdict FAIL with `status: succeeded` | `succeeded` | spec:63 | OK |
| WC-2 gate resolution | spec:60 | Zero/Empty | required flag absent (`cli-eval run` with no `--suite`) | blocked | row spec:104 | OK |
| WC-2 gate resolution | spec:60 | Typical | caller supplies the flag | resolution (b) | rows spec:84-124 | OK |
| WC-2 gate resolution | spec:60 | Sentinel Value Match | `--unattended` with `--interactive` or `--mode socratic` | refused | rows spec:103, 110, 118, 102 | OK |
| WC-2 gate resolution | spec:60 | Legitimate Edge | gate with a documented default (cleanup, improve, auggie-review, research, roadmap) | resolution (a), not blocked | AC-2.2 expects blocked (spec:200) | GAP (B4) |
| WC-2 gate resolution | spec:60 | One/Minimal, Maximum | left out: a gate is a presence test with no count or threshold | n/a | n/a | n/a |
| WC-10 wait size | spec:68 | Boundary | one tool call of 4.5 min | neither split nor forbidden | "longer than 5 minutes" split; "at most 4 minutes" waits (spec:68, spec:266) | GAP (M17) |
| WC-10 wait size | spec:68 | Typical | one tool call of 3 min | allowed | spec:68 | OK |
| WC-6 resume | spec:64 | Zero/Empty | first attempt, no prior output | fresh run | spec:64 | OK |
| WC-6 resume | spec:64 | Sentinel Value Match | implement ledger matches a prior run | implicit resume, no flag | spec:109 ("--resume implicit when a ledger matches"); WC-6 allows only a flag or a fresh dir | GAP (M6) |
| WC-6 retry | spec:64, spec:73 | Legitimate Edge | retry brief reuses the same `--output` | overwrites first attempt's output | section 2.3 (spec:73) does not require a new output directory per attempt | GAP (M6) |
| WC-6 resume | spec:64 | One/Minimal, Maximum | left out: resume is a state choice, not a count | n/a | n/a | n/a |
| WC-4 contract path | spec:62 | Zero/Empty | command stops before any output (workflow pre-creation STOP) | no package id, so no path | spec:92 says write the contract for pre-creation STOPs; INV-B:52 puts it under `<id>/` | GAP (M5) |
| WC-4 contract path | spec:62 | Typical | `--output` given | written at `<output-dir>/return-contract.yaml` | spec:62 | OK |
| WC-4 contract path | spec:62 | One/Minimal | left out: a path is given or it is not | n/a | n/a | n/a |
| Step 4 contract check | spec:183 | Sentinel Value Match | contract with `status` but no `command` (workflow today) | assertion fails | step 4 cannot pass in P0 | GAP (B1) |

## 1. Blocking findings

Grading check for each finding is written as the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y."

### B1. AC-0.4 cannot pass in P0 as written (steps 3 and 4)
- Expert: Adzic (examples and acceptance), Wiegers (testability). Severity: MAJOR, graded blocking because an acceptance criterion cannot pass.
- Location: spec:182 (step 3), spec:183 (step 4), spec:194 (AC-0.4), spec:159 (P1 scope).
- Issue: (a) Step 3 requires the report path to be "the WC-4 contract path" (spec:182). WC-4 arrives only in P1 (spec:159), so no P0 command can satisfy it. (b) AC-0.4 says step 4 "uses the command's existing report file" (spec:194), but step 4 parses the file as YAML and asserts `status` and `command` (spec:183). The workflow contract carries `status`, `plan_path`, `reflect_report_path` and no `command` key (INV-B:52, INV-B:272). Troubleshoot writes REPORT.md, and a return contract only with `--caller task-unified` (INV-B:49, INV-B:242). Adversarial has no fixed contract name (INV-A:35, INV-A:60). Step 4 therefore fails for troubleshoot and workflow, and step 3 fails for every P0 command.
- Grading sentence: An implementer who follows AC-0.4 as written runs `/sc:workflow` and `/sc:troubleshoot` in P0, then checks steps 3 and 4 on their existing report files, and both steps fail, so the P0 gate can never pass; X is wrong because the spec's own phase gate is unreachable and the text gives no pass path.
- Recommendation: In P0, check only what exists: the report file named by each command, plus steps 1, 2, 5, 6 and 7. Move the contract-field and WC-4 path checks (steps 3 and 4) to P1. Fix the adversarial contract name first (INV-A:60).
- Priority: High. Quality impact: the phase that tests the core decision (spec:43) cannot close.

### B2. AC-1.1 and AC-1.2 cannot pass for /sc:load
- Expert: Wiegers (traceability across row, decision and check). Severity: MAJOR, graded blocking because two stated texts contradict each other.
- Location: spec:112 (load row, "Report: none (see note)"), spec:265 (decision: "a report file would be an unrequested addition"), spec:159 (P1 includes load), spec:183 (step 4), spec:195 (AC-1.1), spec:196 (AC-1.2).
- Issue: AC-1.1 requires every 3.1-3.2 command's Unattended section to name `return-contract.yaml` (spec:195). AC-1.2 runs step 4 for every P1 command (spec:196), and P1 includes load (spec:159). The load row and decision say load writes no report.
- Grading sentence: An implementer who follows the load row and the decision builds /sc:load with no contract, then AC-1.1 fails because its section cannot name a file it does not write, and AC-1.2 fails at step 4 because no contract exists; X is wrong because the spec contradicts itself on whether load reports a file.
- Recommendation: Either exempt load from AC-1.1 and AC-1.2 by name, or give load a contract. Choose one in section 3.2 and make AC-1.1 match.
- Priority: High. Quality impact: P1 cannot close with the spec as written.

### B3. Section 3.1 says the ready commands change only in the last column, but P1 and AC-1.1 require the flag on all of them
- Expert: Fowler (change scope), Wiegers (consistency). Severity: MAJOR, graded blocking because two stated texts contradict each other.
- Location: spec:79 ("The only command changes are the small fixes in the last column"), spec:84 (brainstorm, fix "None"), spec:87 (init-lite, fix "None"), spec:159 (P1: "the --unattended flag accepted by every command in sections 3.1 and 3.2"), spec:195 (AC-1.1).
- Issue: Brainstorm and init-lite have no change under spec:79, so an implementer following it adds no flag and no Unattended section to either. AC-1.1 requires the section in every 3.1 command, and P1 requires the flag.
- Grading sentence: An implementer who follows spec:79 leaves brainstorm and init-lite without `--unattended`, then AC-1.1 fails for both; X is wrong because P1 requires the flag on every 3.1 command, so the spec contradicts itself on the scope of change.
- Recommendation: Rewrite spec:79 to say that P1 adds `--unattended`, the Unattended section and the WC-4 contract to all ten 3.1 commands, and state the minimal change for brainstorm and init-lite.
- Priority: High. Quality impact: scope of change is misstated for 10 commands.

### B4. AC-2.2 cannot pass for five P2 commands whose gates resolve by default
- Expert: Adzic (examples), Nygard (failure resolution). Severity: MAJOR, graded blocking because an acceptance criterion cannot pass.
- Location: spec:200 (AC-2.2), spec:60 (WC-2 resolutions a, b, c), rows spec:100 (auggie-review), spec:103 (cleanup), spec:110 (improve), spec:116 (research), spec:118 (roadmap).
- Issue: AC-2.2 requires every P2 gate-trigger run to end `worker_done --outcome failed` with contract `status: blocked` and a non-empty `blocked_question` (spec:200). Under WC-2 resolution (a) the commands above do not block. Cleanup and improve apply non-approval items and list the rest (spec:103, spec:110). Auggie-review's `--unattended` implies `--no-post-pr` (spec:100). Research pins `--strategy planning` (spec:116). Roadmap resumes only when the flag is passed (spec:118). AC-2.2 also gives gate-trigger inputs only for tdd and cli-eval, with "for example" for the rest.
- Grading sentence: An implementer who follows AC-2.2 runs cleanup with input that hits its approval gate and expects a blocked contract and a failed outcome, but the row resolves the gate by listing the item and the run completes and reports succeeded; X is wrong because the criterion cannot pass for that command as written, and the same holds for the four others.
- Recommendation: Replace AC-2.2 with a per-command table: gate input, expected resolution (blocked, or (a)/(b) with success and a check that the listed items appear in the report), and expected `--outcome`.
- Priority: High. Quality impact: P2 acceptance is not testable for 5 of 15 commands.

### B5. AC-C1 cannot fail, and its scope conflicts with SA-2 and SA-5
- Expert: Fowler (boundary integrity), Wiegers (testability). Severity: MAJOR, graded blocking because the only check of a named safety boundary cannot detect the violation it names.
- Location: spec:172 (AC-C1), spec:147 (SA-2), spec:150 (SA-5), spec:180 (step 1, `ORCA` placeholder), spec:191-210 (phases that touch core).
- Issue: The pattern is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'`. In an -E pattern `\|` is a literal bar, not alternation. The check therefore matches only the text "orca orchestration|worktree|terminal|agent" and cannot match a real Orca call. I reproduced this by piping sample lines through the same expression (no files written): the line "orca orchestration worker-start" was not printed, and with an unescaped `|` the same line was printed. The check is also case-sensitive, so `ORCA orchestration` (the placeholder in spec:180) is missed. Second, AC-C1 scans `src/superclaude/core` (spec:172), where SA-5 requires the routing guide to gain an Orca section (spec:150) and where the contract file is allowed to mention Orca (spec:147). Once the pattern is fixed, both permitted texts would fail AC-C1 whenever they name an `orca` command.
- Grading sentence: An implementer who runs AC-C1 as written, in any phase, gets empty output whether or not a command contains `orca orchestration worker-start`, and then reports SA-2 and WC-8 as met; X is wrong because the only enforcement of the no-Orca-in-commands boundary can never fail.
- Recommendation: Use `grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b'`, scan `commands`, `skills` and `agents` for the hard rule, and scan `core` only for paths other than `WORKER-CONTRACT.md` and the routing-guide Orca section. State those two exclusions in SA-2 and SA-5. Add a self-test: the check must match a planted line.
- Priority: High. Quality impact: the boundary the spec relies on for standalone use (SA-2, spec:147) is unenforced.

## 2. Medium findings (follow-up candidates, not blocking)

Each finding states why it is Medium: "needs a guess" or "a requirement the document never states".

- M1. AC-C5 (spec:176) and AC-0.3 (spec:193) miss removed lines that start with `-`. A removed markdown bullet appears as `-- ...` and a removed blank line as `-`; `^-[^-]` excludes both. I reproduced this by piping sample diff lines. The check therefore passes non-additive edits to command and routing files. Fix: `grep -E '^-' | grep -vE '^--- '`. Grade: Medium, because the wrong outcome needs a non-additive edit that the check then passes. Expert: Wiegers.
- M2. AC-C2 (spec:173) runs `make verify-sync` with no stated sync step. SA-5 (spec:150) says the `.claude/` copies come from `make sync-dev`. The `plugins/superclaude/` mirror is covered by no check, and the update rule was not read (spec:279, UNVERIFIED item 8). Grade: Medium, because the outcome depends on whether the implementer runs sync, which the text does not say. Expert: Wiegers.
- M3. AC-0.4 (spec:194) requires "no Agent-tool wrapper, verified in the step-5 transcript", but step 5 (spec:184) searches only for `AskUserQuestion`. A run wrapped in an Agent-tool subagent passes every step, which leaves the direct-route gap (spec:43) untested. Grade: Medium, because the implementer must add a check the text does not state. Expert: Adzic. Recommendation: add a step that fails if the worker's transcript shows an Agent or Task tool call before the command.
- M4. WC-2 (spec:60) lists three resolutions per gate. WC-3 (spec:61) adds a fourth: the worker may ask the coordinator and wait in `ask`. Under WC-3 a blocked gate can park the worker, so AC-2.2 steps 2 and 3 (spec:181-182) see an open question, not `agentWait` or `worker_done`. The spec does not choose. Grade: Medium, because the implementer must guess which route. Expert: Nygard, Hohpe.
- M5. WC-4 (spec:62) requires `<output-dir>/return-contract.yaml`, known before dispatch. Workflow has no output flag (spec:92) and writes its contract under `.dev/tasks/to-do/<id>/` (INV-B:52, INV-B:272), where `<id>` exists only after package creation. Pre-creation STOPs therefore have no path. AC-1.4 (spec:198) checks only the statement. Grade: Medium, because P1 could add a flag, but the spec does not say so. Expert: Hohpe.
- M6. WC-6 (spec:64) allows resume only with a resume flag, otherwise a fresh output directory. Two gaps: (a) implement resumes implicitly from a matching ledger (spec:109, INV-A:51), which WC-6 does not cover; (b) section 2.3 (spec:73) does not require a new `--output` per retry, and adversarial's default output is derived from its input directory (INV-A:60), so a retry with the same `--output` overwrites the first attempt. Grade: Medium, because a missing restriction. Expert: Nygard.
- M7. WC-9 (spec:67) gates only outward actions. Local mutations are ungated: cleanup and improve edit product files (spec:103, spec:110), implement edits product files, reflect's default-on Wave 7 moves folders (spec:88), and under `--unattended` the `--remediate` auto-accept applies to auto-fixable registers (spec:88, spec:151). The brief has no rule for which local changes it authorizes. Grade: Medium, because a missing restriction. Expert: Cockburn (actor and authority), Nygard.
- M8. AC-4.2 (spec:209) passes vacuously. Under spec:113 a run without the pre-tag choice is blocked before any outward step, so WC-9 is never exercised, and "no new PR" has no baseline capture to compare against. Grade: Medium, because the check can pass without testing its rule. Expert: Adzic.
- M9. AC-4.3 (spec:210) cannot be measured as written: "heartbeats at most 5 minutes apart" and "no single tool call exceeds 240 s" name no method, and the poll-script runtime is UNVERIFIED (spec:283). Grade: Medium, because the pass condition is undefined. Expert: Wiegers.
- M10. Step 6 (spec:185) passes only when `git status --short` lists files under the output directory. The brief uses `--worktree current` (spec:180) and WC-11 (spec:70) lets workers share the current worktree. Any other writer, including the coordinator, makes the step fail. The spec does not require a clean dedicated worktree. Grade: Medium, because it needs a guess about the environment. Expert: Nygard.
- M11. Step 3 (spec:182) waits for `worker_done,escalation,question` and says only "until worker_done arrives". A question or escalation has no defined handling, though WC-3 (spec:61) makes questions possible and P2 gates raise them. Grade: Medium, because undefined. Expert: Nygard.
- M12. AC-3.3 (spec:206) and the validate-tests row (spec:125) say to fix the default target `tests/sc-task/` but never name its replacement. `test -d` can pass by creating an arbitrary directory. Grade: Medium, because undefined. Expert: Adzic.
- M13. cli-portify's hardcoded template path (spec:105; INV-A:68) is listed as a required change, but no phase (spec:160 names cli-portify for gate conversion only) and no AC covers it. Without the fix, a worker outside an IronClaude checkout fails at Phase 3 (INV-A:68). The project CLAUDE.md rule against `src/superclaude/` paths in installed primitives (session context; not in the sandbox) applies. Grade: Medium, because a stated requirement with no owner. Expert: Fowler.
- M14. The tasklist row (spec:122) says "none" for the reflect fan-out. That rests on nested reflect runs that inventory B marks UNVERIFIED (INV-B:210, INV-B:314 item 1, INV-B:322 item 8). INV-A:14 supports the three-layer nesting limit but not that a reflect run inside a Stage 10.5 subagent works or that its remediation offer is answered. Grade: Medium, because the implementer must accept an unverified claim. Expert: Newman.
- M15. Phase order (spec:158): P0 edits HOW-WE-WORK, KNOWN_CORE_FILES and the test file before the smoke runs that can reject the decision (spec:194, "a failure here reopens section 1"). The spec gives no rollback. Grade: Medium, because the ordering commits files before the gate. Expert: Fowler.
- M16. WC-5 (spec:63) is silent on three cases: a 0-byte report (it falls to "otherwise succeeded", but step 4 needs a non-empty file, spec:183); a status value outside the four; and a conflict between prose and the status field (CAPS:73 says never encode failure only in prose). Grade: Medium, because the implementer must guess. Expert: Wiegers.
- M17. WC-10 (spec:68) splits waits "longer than 5 minutes" and asks for waits "at most 4 minutes" (spec:266). A single call of 4.5 minutes is neither split nor forbidden, which leaves the 1-minute margin under the 5-minute heartbeat (CAPS:130) unguarded. Grade: Medium, because a boundary is unspecified. Expert: Nygard.
- M18. Whittaker, sequence attack (FR-2.4). I can break this specification by a sequence attack. The invariant in WC-4 and WC-5 (spec:62-63) fails when the worker writes `return-contract.yaml` with a final status and then dies before `worker_done`. The contract says succeeded, Orca shows no `worker_done`, and a `--retry-of` run rewrites the same contract (spec:64). The spec gives no rule for which signal the coordinator trusts. Grade: Medium, because a missing rule. Expert: Whittaker, Nygard.

## 3. Minor notes

- m1. AC-2.1 (spec:199) checks wording only. It passes with no behavioural change, so it cannot show the gates work; AC-2.2 must do that.
- m2. AC-1.3 (spec:197) checks only `return-contract.yaml` in a standalone run. SA-3 (spec:148) says a standalone run writes the same files as today, so a new report file would pass the check.
- m3. WC-4 (spec:62) states "Orca does not check the file" as fact. CAPS:79 marks it UNVERIFIED and UNVERIFIED item 3 (spec:274) says the spec "assumes" it. The design does not depend on it, but the status is wrong.
- m4. Non-goal 3 (spec:215) cites CAPS:12-13 for "an Orca coordinator session following Orca's own guide". Those lines are source-key rows and do not state that.
- m5. D3(a) (spec:240) leaves pr-submit's attended poll loop in the coordinator. The spec does not say the coordinator cannot dispatch or answer asks while the loop runs.
- m6. Section 1.2 E2 (spec:22) says a worker "has the same tools as a command a person runs". CAPS:161 shows top-level status, not tool parity. This is an unsupported step in the evidence for the decision.
- m7. Section 1.2 E5 and the SA-2 baseline (spec:25) rely on `grep` results from 2026-11-02 that are not reproducible in the sandbox (UNVERIFIED).

## 4. Acceptance criteria and live-check steps: can each pass as written?

"Covers" means the commands and phases the criterion names. Each row answers for every command and phase in its scope.

| ID | Spec line | Passes as written for every covered command and phase? | Finding |
|---|---|---|---|
| AC-C1 | 172 | No. Cannot fail: `\|` in -E is a literal bar, and it is case-sensitive | B5 |
| AC-C2 | 173 | Only if sync is run first, which the text does not say. Plugin mirror unchecked | M2 |
| AC-C3 | 174 | Yes | none |
| AC-C4 | 175 | Yes (staged files only) | none |
| AC-C5 | 176 | Passes, but misses removed lines that start with `-` | M1 |
| AC-0.1 | 191 | Yes (install_core.py:13-24 is UNVERIFIED here) | none |
| AC-0.2 | 192 | Yes for the byte copy; the level-table copy in core/CLAUDE.md is checked only by the existing test | none |
| AC-0.3 | 193 | Yes for changed table rows; misses removed list items | M1 |
| AC-0.4 | 194 | No. Steps 3 and 4 cannot pass for troubleshoot or workflow in P0. No check of the no-wrapper claim | B1, M3 |
| AC-1.1 | 195 | No. load cannot name a contract it does not write. Brainstorm and init-lite get no section under spec:79 | B2, B3 |
| AC-1.2 | 196 | No for load (step 4). Steps 3, 6 need M11 and M10 to be defined | B2, M10, M11 |
| AC-1.3 | 197 | Yes, for the one file it names | m2 |
| AC-1.4 | 198 | Yes as a grep. Workflow's pre-creation location is undefined | M5 |
| AC-2.1 | 199 | Yes, as a wording check only | m1 |
| AC-2.2 | 200 | No for cleanup, improve, auggie-review, research, roadmap. Inputs given for two commands only | B4, M4 |
| AC-2.3 | 201 | Yes | none |
| AC-2.4 | 202 | Yes (needs a fork PR fixture) | none |
| AC-2.5 | 203 | Yes, as a manual check, if the baseline is recorded | none |
| AC-3.1 | 204 | Yes | none |
| AC-3.2 | 205 | Yes, once the reconciliation makes the flag the only resume trigger | none |
| AC-3.3 | 206 | Only by inventing the new default target | M12 |
| AC-3.4 | 207 | Yes | none |
| AC-4.1 | 208 | Yes, under the D2 option that the run assumes | none |
| AC-4.2 | 209 | Passes vacuously; no baseline for "no new PR" | M8 |
| AC-4.3 | 210 | No. The timing checks have no measurement method | M9 |
| Step 1 | 180 | Yes | none |
| Step 2 | 181 | Yes | none |
| Step 3 | 182 | No for P0 (report-path clause, B1). No branch for question or escalation | B1, M11 |
| Step 4 | 183 | No for troubleshoot and workflow in P0 (B1); no for load (B2) | B1, B2 |
| Step 5 | 184 | Yes, but does not detect Agent wrapping | M3 |
| Step 6 | 185 | Only in a clean dedicated worktree | M10 |
| Step 7 | 186 | Yes | none |

## 5. Coverage

Read in full: the candidate (285 lines), `review/lint-1.md`, `README.md`, the three inventories, `command.md` and the FIRST-REVIEW prompt file. Checked: sections 1-9, WC-1 to WC-12, SA-1 to SA-6, every row of the 3.1 and 3.2 tables (10 and 27 rows; the 6 coordinator-only rows in section 4 were checked for the count and the stated reasons), the P0-P4 phase plan, all 25 ACs and 7 live-check steps, the open decisions D1-D5, the Decisions table and the UNVERIFIED list. Counts reconciled against the inventories: 21 + 22 commands; 10 ready, 27 needs-change, 6 coordinator-only, total 43. Not checkable here: any `src/`, `tests/` or `.dev/` evidence the spec cites.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| One review, not two plus MERGE and VERIFY | (1) Run two fresh-context reviewers; (2) one review, state the gap | No fresh-context reviewer or verifier is available to this worker. Stated as a process deviation; verdict provisional. |
| AC-C1 graded blocking | (1) Medium as a check defect; (2) blocking as the only enforcement of SA-2 | The check cannot fail on the boundary it names, so SA-2 and WC-8 have no working gate. |
| AC-C5 and AC-0.3 graded Medium | (1) Blocking; (2) Medium | The check misses non-additive edits, but the wrong outcome needs a deliberate edit the spec does not forbid in words. |
| B2 and B3 graded blocking | (1) Medium; (2) blocking | Stated texts contradict each other (load row vs AC-1.1; spec:79 vs P1 and AC-1.1). |
| Guard table built | (1) Omit; (2) build with GAP rows referencing findings | The spec has guard conditions, so the table is mandatory under the command's hard gate. Classes left out are reasoned. |

## Reviser brief

Blocking finding ids: B1, B2, B3, B4, B5 (the findings above, with their grading sentences). Revise only text a blocking finding names. Add no rule, mechanism or section that a blocking finding does not call for. Prefer deleting or narrowing to adding. Each added paragraph or table cites its finding id. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

Follow-up candidates (M1-M18, m1-m7) are listed for the coordinator, which asks the user once whether to open an issue for them. No issue has been created.

verdict: FAIL
