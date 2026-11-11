review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (spec-panel, critique mode)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Label: whole-document audit of the final spec, a first review (no `--re-review`, no `--baseline`; baseline: none, not "missing", because neither flag was given).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 289 lines.
- sha256(candidate): `d7bacfaaecc8fff9a059e1e70fe785b1e6c52aecb2a57c161ca8d51cdcb3aa3c`
- sha256(baseline): not applicable.
- Reviewer model actually used: `claude-sonnet-5-5`
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- Date: 2026-11-10.
- Citation convention: `S:N` = line N of the candidate spec. `CAPS:N`, `INV-A:N`, `INV-B:N` = lines of `inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md`. Only the README and these three inventories exist in the sandbox, so every citation to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml` or `Makefile` is UNVERIFIED (the file is not in the workspace). I checked the spec's `INV-*` and `CAPS:*` citations that I spot-read (about 60) and found them as cited.

## Summary

The spec's central decision (Orca coordinates, commands stay workers, `--unattended` plus a report file plus resume) is coherent and well evidenced where evidence can be checked. Inventory counts conserve (21 + 22 = 43 = 10 ready + 27 needing change + 6 coordinator-only; the 27 rows of S:99-125 and the 10 rows of S:83-92 match the phase lists at S:159-162). I found 2 blocking findings, both in the acceptance and rollout text (the gates a phase must pass), and 7 Medium findings.

Blocking: 2. Medium: 7. Minor: 4.

## === REQUIREMENTS ANALYSIS ===

### F1. CRITICAL-equivalent (blocking): the Phase 0 live-baseline check cannot pass as written
- Experts: Wiegers (testability), Adzic (concrete example), Whittaker (Sequence Attack).
- Grading sentence: An implementer who follows AC-0.4 as written (S:194) runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and requires "steps 1-3 ... pass". Step 3 (S:182) passes only if the worker's `--report-path` is "the WC-4 contract path" and its outcome "matches the contract's `status`". No such contract exists in P0: the same row says "the contract arrives in P1", and S:83 and S:92 say adversarial writes it in a subdirectory and workflow at a per-run package path until the P1 fix. So step 3 is unsatisfiable in P0, the P0 acceptance check fails by construction, and S:194 says a failure here "reopens section 1" (the decision itself) while S:154 blocks every later phase on P0 passing. The result is wrong because a correct implementation of the decision is reported as having refuted it.
- Quoted conflict: S:182 "its report path is the WC-4 contract path" vs S:194 "step 4 uses the command's existing report file, since the contract arrives in P1" (the row relaxes step 4 only, not step 3).
- Concrete trace: troubleshoot worker ends with `worker_done --report-path .../REPORT.md` (S:91). Step 3 pass condition (report path = `<output-dir>/return-contract.yaml`) is false. AC-0.4 = FAIL. P1 never starts (S:154).
- Evidence: S:154, S:158, S:182, S:194, S:83, S:91, S:92.
- Recommendation: in AC-0.4 say "step 3 passes when `worker_done --report-path` equals the report file named in the S:83-92 'Report today' column, and `--outcome` matches the worker's own reading of that report". Priority: High.

### F2. MAJOR (blocking): Phase 1 scope and AC-1.1 contradict the Phase 4 hold and the recommended D3(a)
- Experts: Wiegers (consistency, traceability), Cockburn (who is the actor for the decision), Fowler (phase boundaries).
- Grading sentence: An implementer who follows S:159 ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2") and AC-1.1 (S:196: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`") adds that section to implement, post-release and pr-submit in P1. But S:154 and S:162 hold those three commands for P4 until the user answers D2-D4, S:112/S:109/S:113/S:114 give them rows whose gate text depends on those answers, and S:243 says that under the recommended D3(a) there are "no pr-submit changes". The phase list at S:159 also names only 9 new commands plus 4 fixes, so brainstorm and init-lite (3.1, no phase) are in AC-1.1 but in no P1 scope list. Either AC-1.1 fails at P1 for the P2-P4 and unlisted commands, or the P1 implementer writes gate resolutions for D2-D4 before the user decides (for implement, a safety rule per S:221), or pr-submit becomes dispatchable although D3(a) says it is coordinator-only.
- Quoted conflict: S:196 "every command in sections 3.1-3.2" vs S:154 "Phase 4 waits for answers to D2-D4" and S:243 "no pr-submit changes".
- Evidence: S:154, S:159, S:162, S:196, S:243; the 3.1/3.2 phase column S:83-125.
- Recommendation: restrict AC-1.1 to "every command whose section 3 phase is P1 or earlier (plus the 3.1 commands with a stated phase)", add brainstorm and init-lite to a named phase, and say that pr-submit gets no section unless D3(b). Priority: High.

### F3. Medium: `<output-dir>` is undefined for commands whose `--output` is a file
- Experts: Wiegers, Adzic.
- WC-4 (S:62) fixes the report at `<output-dir>/return-contract.yaml` with the directory "the coordinator passed (`--output` / `--output-dir`)". Rows S:87, S:90, S:120 give `--output <file>` for init-lite, tdd and spec-panel, and S:105/S:116 add a new `--output-dir` only for cli-portify and research. An implementer can read "the file's parent directory" or "add `--output-dir`"; nothing says which. This is a missing requirement, not a text that does harm, so Medium. Also note that the actual `/sc:spec-panel` command definition supplied to this audit already defines `--report-dir <dir>` and keeps `--output` file-valued (command.md "Unattended mode"), while S:120 plans to "add `--output`"; the S:120 row cites `cmd/spec-panel.md` lines UNVERIFIED here.
- Recommendation: one sentence in WC-4 stating the directory rule for file-valued `--output`. Priority: Medium.

### F4. Medium: "keep their fields" vs a fixed four-value `status`
- Experts: Wiegers, Fowler.
- WC-4 (S:62) says commands that already write a contract "keep their fields", while `status` must be one of four values; WC-5 (S:63) maps any other value to `--outcome failed`. The inventories record the existing contracts' field names but not their status vocabulary (workflow: `status` incl. `failed`, INV-B:272; others not recorded). If an existing contract uses another success word, a successful run maps to `failed`. The text needs a guess about the existing vocabularies, so Medium. Priority: Medium.

### F5. Medium: WC-6 "fresh output directory" vs WC-4 "known before dispatch"
- Experts: Wiegers, Nygard (retry behaviour).
- S:64 says a command without a resume flag "writes each run into a fresh output directory", while S:62 requires the report path to be known before dispatch from a coordinator-supplied directory, and S:73 never tells the coordinator to give each retry (`worker-start --retry-of`, CAPS:116) a new directory. Reading A (the command makes a subdirectory) breaks the WC-4 path; reading B (the coordinator supplies a new directory) is not stated in section 2.3. With the same brief, a retry overwrites attempt 1's `return-contract.yaml`. Priority: Medium.

### F6. Medium: acceptance for blocked gates is nondeterministic because WC-3's relay is optional and unmentioned in 2.3/7.2
- Experts: Crispin-style test view (applied by Wiegers/Adzic).
- WC-3 (S:61) lets a worker with a preamble "instead ask the coordinator once" for gates whose row names a flag. AC-2.2 (S:202) requires `--outcome failed` and `status: blocked` for gate-trigger inputs, and 7.2 step 3 (S:182) waits only on `worker_done`, `escalation` and `question` without saying how to answer a question. Section 2.3 (S:73) does not say whether the brief permits `ask`. A worker that uses the relay legitimately produces a different outcome, so the test is not deterministic. Priority: Medium.

### F7. Medium: AC-0.5 tests a mapping that no stated code performs
- AC-0.5 (S:195) runs a pytest on "planted contracts" to check the WC-5 mapping, but WC-5 is performed by the worker session (S:63, owner "Worker session"), and the spec names no helper, function or file for the test to call. An implementer cannot write the test without inventing the unit under test. Medium (a requirement the document never states).

### F8. Medium: WC-9 / D4 refer to explicit flags that do not exist for some commands
- WC-9 (S:67) turns outward actions on "only through the command's own explicit flag", and D4 (S:247) names task `commit`/`push`. S:121 gives task no such flag (only "refused unless authorized"). Priority: Medium.

### F9. Medium: P1 makes `--unattended` a no-op on commands that still have gates
- S:159 says the flag is accepted by every 3.1/3.2 command "a no-op where a command has no gate", so between P1 and P2/P3/P4 a command such as cleanup, roadmap or implement accepts `--unattended` yet still prompts (S:103, S:118, S:109). The spec does not tell the coordinator not to dispatch a command before its phase lands, and S:73 does not require a phase check in the brief. A stall results (the "healthy" wait of CAPS:52/CAPS:129). Only the 3.1 table (S:79) carries a "run now if the brief uses the stated flags" statement. Priority: Medium.

### Minor notes (never fail the review)
- N1. S:109-110 and S:103: cleanup/improve under `--unattended` apply edits in a worktree shared with other workers (CAPS:115) while their "rollback" mechanism is UNVERIFIED (INV-A:118); the contract lists changed files, but no clean-tree precondition is stated. Safety hardening candidate.
- N2. S:80 (CAPS:80): a `blocked` outcome maps to `failed`, and a worker's own failed report does not trip the circuit breaker, but the coordinator-side handling of repeated `blocked` results is not specified.
- N3. S:11 says 11 locations were re-read by the spec's author on 2026-11-02; none is checkable here (UNVERIFIED).
- N4. S:288 (item 14) records a prior validator check; no evidence of it is in the workspace (UNVERIFIED).

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard.

- Boundaries: the coordinator / worker / command split is clean (S:16, S:50-51, S:216). The rejected alternative (S:29-37) is supported by CAPS:97-103 (depth 1, call sites not traced, flagged UNVERIFIED at S:33). Verified: CAPS:97-101 as quoted.
- Interface (Newman, Hohpe): one report file `return-contract.yaml` with a four-value status and a two-value Orca outcome (S:62-63, S:265) is a sound message contract; the gaps are F3 (directory for file-valued `--output`), F4 (vocabulary reuse) and F5 (path stability across retries).
- Failure modes (Nygard): the worker-stall failure is explicitly addressed (S:44, WC-2/WC-10, AC-2.2). Liveness during long waits depends on a worker heartbeat whose 5-minute cadence is from the preamble, not a guide (CAPS:130, UNVERIFIED whether Orca uses it); WC-10's 4-minute split is consistent with that.
- Evidence gap: the central verdicts rest on file reads, not runs (S:43, INV-B:323). The spec states this and makes P0 test it; F1 is what breaks that test.
- Coupling: SA-2 (S:147) and AC-C1 (S:172) keep Orca out of commands; AC-C1 excludes `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` (consistent with S:147/S:150). No defect found.

## === GUARD CONDITION BOUNDARY TABLE ===

Trigger: the spec contains threshold and boolean guards (readiness limit, heartbeat/wait sizes, status enum, depth limit, confidence 0.70 resolution). Rows follow the 7-column template; a class left out is stated in one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping (`status` in the four values) | S:63 | Zero/Empty | `status` missing, empty or no report file | not in set | `--outcome failed` | OK |
| WC-5 | S:63 | One/Minimal | `status: partial` | in set | `--outcome succeeded`, body states `partial` | OK |
| WC-5 | S:63 | Typical | `succeeded` / `failed` / `blocked` | in set | succeeded / failed / failed | OK |
| WC-5 | S:63, S:62 | Sentinel Value Match | existing contract using another success word (for example `complete`) | not in set | maps to `failed`; whether existing contracts use such words is not stated | GAP (F4, Medium) |
| WC-5 | S:63 | Legitimate Edge Case | audit with verdict FAIL | `succeeded`/`partial` | `--outcome succeeded` | OK |
| WC-5 | | Maximum/Overflow | left out: a status value has no capacity bound | | | n/a |
| WC-10 wait split (single tool call <= 4 min) | S:68 | Zero/Empty | step with no wait | n/a | no split needed | OK |
| WC-10 | S:68 | Typical | pr-submit iteration | UNVERIFIED runtime | confirm each iteration < 4 min (S:114, S:286) | GAP (open verification, Medium by S:286 itself) |
| WC-10 | S:68 | Maximum/Overflow | cli-eval timeout up to 3600 s | exceeds 5 min | split into waits <= 4 min (S:104) | OK |
| WC-10 | S:68 | Legitimate Edge Case | tool call exactly 240-300 s | between 4 and 5 min | rule says split above 5 min, split target 4 min; AC-4.3 uses 240 s | OK (minor ambiguity: "longer than 5 minutes" S:68 vs "no call exceeds 240 s" S:213) |
| WC-1 readiness fallback | S:59 | Typical | fallback 30 s vs limit 60 s | passes | well inside limit | OK |
| WC-1 | S:59 | Legitimate Edge Case | fallback about 45 s | fails again | "well inside" is not numeric; evidence only at EVIDENCE.md:56 (UNVERIFIED) | GAP (follow-up, no concrete wrong outcome: launch setup is out of command scope) |
| Nesting depth = 1 (WC-8) | S:66, S:33 | Zero/Empty | depth 0 coordinator | allowed | coordinator fans out | OK |
| Nesting depth | S:66 | Maximum/Overflow | depth 1 worker calls `worker-start` | refused `nested_worker_depth_exceeded` | WC-8 forbids; `task-create` at depth 1 UNVERIFIED (CAPS:103) | OK (UNVERIFIED item listed at S:279) |
| Confidence threshold (task) | S:121 | Zero/Empty | confidence undefined | n/a | not specified | GAP (Medium, not stated; below 0.70 row only) |
| Confidence threshold (task) | S:121 | Sentinel / edge | exactly 0.70 | boundary | "below 0.70 resolves as blocked" implies 0.70 proceeds | OK |
| AC-C3 "no baseline-passing test fails" | S:174 | Zero/Empty | baseline with zero passing tests | vacuously true | not stated | GAP (minor) |

Incomplete-table gate (FR-10): complete; no FR-9 blank behaviors except the ones recorded as GAP. FR-8/FR-9 grading: no GAP names a concrete wrong outcome an implementer would produce or a security/data-loss risk, so each is Medium or minor and listed below.

## Quantity check (Pipeline Dimensional Analysis)
Trigger limited: the only multi-stage count flow is the inventory split. 21 + 22 = 43; 10 + 27 + 6 = 43; P1 9 + P2 11 (3.2) + P3 4 + P4 3 = 27, with 4 of the 10 ready commands assigned to P1 fixes and 4 to P2 (S:159-161, S:83-92). Count conserved; no mismatch.

## Coverage

Covered: the whole spec S:1-289 read; README read; every section-2 requirement, every section-3 table row for count and phase consistency, sections 4-9, the UNVERIFIED list. Spot-checked against inventories: INV-A:3, 14, 62, 76-83, 90, 95-97, 106, 113, 118, 120; INV-B:3, 36, 52, 267-272, 285-286, 292-301, 311, 320, 323; CAPS:44-47, 52, 58, 64-68, 72-80, 86, 92, 97-103, 107-116, 128-130, 135-139, 145-161, 178-188.
Not covered / UNVERIFIED: every citation into `src/superclaude/**`, `CLAUDE.md`, `HOW-WE-WORK.md`, `.dev/evals/...EVIDENCE.md`, `.dev/codegraph-migration/...`, `pyproject.toml`, `Makefile`, `install_core.py` (files absent from the workspace); no command was run; the Orca guides themselves were not available, only their quotations in the capabilities inventory.

## follow-up candidates (Medium and minor; none triggers a revision)

- F3 file-valued `--output` vs `<output-dir>` (S:62, S:87, S:90, S:120).
- F4 existing-contract status vocabulary (S:62-63).
- F5 fresh directory vs known-before-dispatch path on retry (S:62, S:64, S:73).
- F6 optional `ask` relay vs deterministic AC-2.2 (S:61, S:182, S:202).
- F7 AC-0.5 has no unit under test (S:195).
- F8 no explicit outward-action flag for task `commit`/`push` (S:67, S:121, S:247).
- F9 `--unattended` accepted as no-op before its phase lands (S:159).
- N1-N4 above; WC-1 numeric bound; AC-C3 empty baseline; WC-10 "5 minutes" vs "240 s" wording; confidence-undefined case for task.

Per `/sc:spec-panel` Review Loop bullet 3, the session that ran this review asks the user once per loop whether to open an issue for these candidates and creates none without an answer. This run's reply is restricted to `DONE <path>`, so the question was not asked here; the coordinator session must ask.

Brief overrides: none. The brief did not widen scope or regrade any minor finding.

## Reviser brief

Blocking finding ids: F1, F2. Rules (restated from Review Loop bullet 6, since the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id; leave Medium and minor findings alone; do not award yourself a PASS.

verdict: FAIL
