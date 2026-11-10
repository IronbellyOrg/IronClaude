review: 1 of 3

# Spec-panel audit: Orca worker contract spec (whole-document, first review)

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Run type: labelled whole-document audit, first review (no `--re-review`, no `--baseline`, so no baseline note is needed).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `8fb661981967c14a5a823b50e2afa1ac31cb20523338e235d7b1b568eeb0705a` (taken with `sha256sum`; 285 lines, 61628 bytes)
- baseline sha256: not applicable (no baseline given)
- reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (lines 27-32). `README.md` read first (binding context, `.dev/orca-command-refactor/README.md:1-39`).
- Citation convention: `S:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any citation to a file outside `.dev/orca-command-refactor/` (`src/...`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `EVIDENCE.md`, Orca guide output) cannot be opened in this sandbox and is marked UNVERIFIED when I rely on it.

## Coverage (what was and was not checked)
Covered, by reading the whole candidate (S:1-285) against the three inventories:
- Section arithmetic. 21 + 22 = 43 commands (INV-A:3, INV-B:3). 10 ready (5 in INV-A:73, 5 in INV-B:278), 27 needs-change (13 in INV-A:73, 14 in INV-B:278), 6 coordinator-only (S:132-137). The section 3.1 table has 10 rows (S:83-92), the 3.2 table has 27 rows (S:99-125), and the phase rows in S:159-162 cover 14 + 15 + 4 + 3 = 36 commands. All consistent, and every 3.2 row's phase matches section 6.
- Citation resolution against the inventories. Every `CAPS:` line quoted in S:21-37, 59-70, 180-186, 214, 250, 272-284 was opened and says what the spec claims (for example CAPS:97-103 depth, CAPS:73 outcome rule, CAPS:79 report-path UNVERIFIED, CAPS:130 heartbeat cadence, CAPS:187/178/180/186/68/188 for the UNVERIFIED items). Every `INV-A:` and `INV-B:` line quoted was opened and resolves (INV-A:14, 36, 62, 90-92, 95-98, 106, 113, 118, 120; INV-B:3, 65, 105, 112, 272, 285-286, 289-301, 311, 320, 323).
- The Review Heuristics in command.md: Guard Condition Boundary Table (triggered, produced below); Pipeline Dimensional Analysis (not triggered: the spec describes a control/worker lifecycle, not a data pipeline whose stage counts N and M may differ).
Not covered / UNVERIFIED:
- Every citation into `src/superclaude/...`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `tests/`, `EVIDENCE.md` and the Orca bundle output other than through the inventories. The spec's own claims that it re-read 11 locations (S:11) and that a validator re-read about 340 citations (S:285) are also not checkable here.
- Whether the native `status` values of the four commands that already write a contract match the four-value set (see M1).
- No live run exists, so all behaviour claims remain as stated in S:43 (spec's own gap 1).

Focus areas applied: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard), plus Whittaker (always active) and Crispin for the Guard Condition Boundary Table.

## Grading summary
Zero blocking findings. No finding passes the grading check ("An implementer who follows the stated text as written builds X, and X is wrong because Y", holding with no further assumption). Each finding below needs a guess about an unread file, an undecided user choice, or a reading the text allows, or is a requirement the document never states. All are therefore Medium or minor and are listed under `follow-up candidates`; none triggers a revision.

=== REQUIREMENTS ANALYSIS ===

### M1. Status vocabulary of already-contract-writing commands is never stated (Medium, grading MAJOR label downgraded) 
- Expert: Wiegers (traceability), Adzic (examples).
- Texts: WC-4 says commands that already write a contract "keep their other fields ... `status` takes one of the four values" (S:62). Section 3.1 gives "None" or "contract filename" as the only small fix for brainstorm, reflect, workflow, adversarial and says workflow gets "flag and section only" (S:83-84, 88, 92, 159). WC-5 maps a `status` outside the four values to `--outcome failed` (S:63). AC-1.2 step 4 and 7.2 step 4 assert `status in {succeeded, partial, failed, blocked}` (S:183, 196). AC-0.4 expects workflow and adversarial to pass at P0 (S:194).
- Gap: the spec never records those four commands' native `status` value set. The only evidence it cites is that workflow's contract has a `status` field and can be `failed` (INV-B:272). If a native value such as "ok" or "success" exists, WC-5 would send a successful workflow run to `failed`, and no row owns the vocabulary change.
- Why Medium: the sentence "X is wrong" needs the guess that the native set differs; the file defining it (`sk/sc-workflow-protocol/refs/return-contract.md`) is outside the sandbox (UNVERIFIED).
- Recommendation: add one line per contract-writing command listing its native statuses and the mapping, or name the phase and row that changes them. Priority Medium. Quality impact: Testability +1.

### M2. Where the contract is written when the output argument is itself the missing input (Medium)
- Expert: Nygard, Wiegers.
- Texts: WC-4 says the contract is written "on success, failure, blocked and partial outcomes, including stops before any other output exists" and places it relative to the caller's `--output` / `--output-dir` (S:62). The post-release row makes a missing `--output` a blocked outcome (S:113); the tdd bare-topic and research cases have no output flag or a flag the brief may omit (S:90, 116).
- Gap: for "blocked because the output location is absent" there is no stated place to write the contract. WC-4's only workaround (first sentence of the `worker_done` body, no `--report-path`) is limited to workflow (S:62).
- Why Medium: a requirement the document never states (undefined fallback location), not a stated text that does harm.
- Recommendation: state a fallback (for example the default output location named in the inventory, or "body only, no report path" for every command with no resolvable location). Priority Medium.

### M3. WC-5 does not define a contract that is present but malformed or points to nothing (Medium)
- Expert: Whittaker (zero/empty, sentinel), Crispin.
- Texts: WC-5 covers "no report exists, is empty, or has a `status` outside the four values", and a Markdown report with no `status` (S:63). A YAML contract with the `status` key absent, or a `succeeded` contract whose `report_path` file does not exist, is not covered. 2.3 has the coordinator check `status` and read the verdict from `report_path` (S:73) but does not say what to do if that file is missing.
- Why Medium: unspecified edge case; no stated text does harm.
- Recommendation: one sentence in WC-5: absent `status` key = outside the four values; coordinator treats a missing `report_path` target as failed. Priority Medium.

### M4. WC-3 says implement halts "always stop blocked" while D2 leaves it open (Medium)
- Expert: Cockburn (goal/actor), Wiegers (consistency).
- Texts: WC-3 says the gate is implement's `E-HALT-QA` / `E-NO-RULING` "which always stop blocked (D2)" (S:61). D2 option (b) lets the worker record a Ruling relayed through `ask` (S:235), and AC-4.1 itself allows "a relayed one" (S:208). The spec says Phase 4 waits for D2 (S:154, 162).
- Why Medium: only bites if the user picks D2(b); recommendation (a) matches WC-3. The harm needs that one of two allowed outcomes.
- Recommendation: in WC-3 write "always stop blocked unless D2 (b) is chosen". Priority Low-Medium.

### M5. WC-10 trigger and cap do not match the pr-submit acceptance wording (Medium)
- Expert: Adzic (measurability), Nygard.
- Texts: WC-10 requires splitting only a step that blocks a single call "longer than 5 minutes" into waits "of at most 4 minutes" (S:68). The pr-submit row says each iteration must "stay under 4 minutes" (S:114) and AC-4.3 says "no single tool call exceeds 240 s" (S:210). A 4.5-minute single call is allowed by WC-10's trigger and fails AC-4.3. Also, a heartbeat "every 5 minutes" (S:68) with a 5-minute call leaves no slack.
- Why Medium: applies only to pr-submit under D3(b); the stricter AC is the safe reading.
- Recommendation: state one rule: every single blocking call is at most 4 minutes. Priority Low-Medium.

### M6. SA-3 and WC-4 disagree on whether the contract is written when only the new output flag is passed (Medium)
- Texts: WC-4 writes the contract "in unattended mode" (S:62). SA-3 says the contract and report files are written "only in unattended mode or when the caller passes the new output flag" (S:148). AC-1.3 tests only the case with neither (S:197).
- Why Medium: two readings allowed (contract with the flag alone, or not); the implementer who picks the wider one changes standalone output but SA-1 still holds for the no-flag case.
- Recommendation: say which. Priority Low-Medium.

### M7. SA-4 additive-edit rule and AC-C5 conflict with several named changes (Medium)
- Texts: SA-4 allows existing-line changes only for the listed defect fixes (S:149). AC-C5 fails any `-` line in a command diff without a named defect fix (S:176). But adding `--unattended` to a Usage line modifies an existing line; cli-eval wait splitting (S:104), roadmap's replaced "Resume? [Y/n]" prompt (S:118), the reflect `--remediate` change (S:88) and cli-portify's new `--resume` flag (S:105) are not in SA-4's list.
- Why Medium: an implementer can add a new line instead of editing the Usage line, so no forced wrong outcome; but AC-C5 as written is likely to fail honest edits.
- Recommendation: extend SA-4's list, or let AC-C5 exempt the Usage-line flag addition. Priority Medium.

### M8. tasklist row departs from the inventory's recommendation without a recorded decision (Medium)
- Expert: Fowler, Nygard.
- Texts: the inventory says Stage 10.5 should call reflect without `--remediate` and the reflect fan-out "must run at the worker's top level, not inside subagents" (INV-B:215; cf. INV-B:46, 295). The spec instead passes `--unattended` to each reflect so its headless auto-accept applies (S:122) and says the fan-out is "one layer below the worker, inside Claude Code's nesting limit" (S:122, citing INV-A:14). The Decisions row says "nothing read in this task contradicts a verdict" (S:268) and records no decision for this departure.
- Concerns: (a) reflect's headless rule "auto-accepts for auto-fixable registers" (INV-B:108), so an unattended tasklist run now triggers an automatic sc:workflow or task-builder remediation, which the spec does not describe or list as an expected artifact; (b) reflect Tier 2 fans out again beneath each reflect subagent (INV-B:110), so "one layer below" understates the depth.
- Why Medium: the effect of the auto-accept on files written is not shown in the evidence available (the reflect refs are outside the sandbox, UNVERIFIED).
- Recommendation: record the decision in Decisions, state the remediation effect under `artifacts`, and drop "one layer". Priority Medium.

### M9. Coordinator procedure after a `blocked` outcome is missing (Medium)
- Expert: Cockburn, Nygard.
- Texts: `blocked` maps to `--outcome failed` (S:63), which makes the Task `failed` and keeps dependents blocked until a `--retry-of` replacement completes (CAPS:90). WC-6 covers retry and a fresh output directory (S:64) and 2.3 says the coordinator checks `status` (S:73), but nothing says how a coordinator answers the blocked question: retry brief carries the answer as a flag, in a new output directory. WC-3's same-worker route (re-invoke after `ask`) re-runs a "fresh dir" command in a directory already holding a `blocked` contract, and WC-6's stale-contract rule is written for retries only (S:64).
- Why Medium: requirement the document never states.
- Recommendation: two sentences in 2.3. Priority Medium.

### M10. AC-2.4 can pass while the command posts (Medium)
- Texts: AC-2.4 compares `gh api repos/IronbellyOrg/IronClaude/pulls/<PR>/reviews --jq length` and `.../comments --jq length` before and after (S:202). Without `--paginate` the API returns one page (default 30 items), so on a PR with 30 or more reviews/comments the length is 30 before and after even if comments were posted.
- Why Medium: the check is weak only on large PRs; the repo-form of the call is correct.
- Recommendation: add `--paginate` with a summing `jq`, or require a fresh PR. Priority Low-Medium.

### M11. Possible stale baseline for E5, SA-2 and AC-C1 (Medium, UNVERIFIED)
- Texts: E5 says no command, skill, agent or core file calls Orca today and only `sk/ccsession-tag/` mentions it (S:25); SA-2 and AC-C1 build on that and AC-C1 requires an empty grep over `src/superclaude/{commands,skills,agents,core}` (S:147, 172). The command count is fixed at 43 (S:76).
- Observation, provenance stated: the skill catalogue shown to this reviewing session (not a file in the workspace) lists `sc:issue`, `sc:graph` and `sc:impact`, which are not among the 43 inventoried commands (INV-A:3, INV-B:3), and describes `sc:issue` as creating an Orca worktree. If that catalogue matches the repository, the inventory scope, E5 and AC-C1's "prints nothing" are out of date. Cannot be checked in this sandbox.
- Recommendation: re-run the E5 grep and the `ls src/superclaude/commands` count immediately before Phase 0 and record the dates. Priority Medium.

=== ARCHITECTURE ANALYSIS ===

### A1. Contract location is a nine-way special-case rule (minor)
- Expert: Newman, Fowler.
- WC-4 (S:62) defines the contract path with a default and eight exceptions (file-valued flag, adversarial subfolder, workflow, research, cleanup-audit, index-repo, troubleshoot). A coordinator must know the rule per command. No concrete wrong outcome follows; the risk is coordinator error. A single caller-supplied report directory for all commands would remove the table. Note only.

### A2. Concurrent coordinator duties in the live check (minor)
- Expert: Hohpe, Nygard.
- 7.2 step 2 requires `worker-show` at least every 5 minutes while step 3 runs `check --wait ... --timeout-ms 900000` (S:181-182). One coordinator session cannot do both literally. Note only: say "between waits".

### A3. D4 mechanism is used before D4 is decided (minor)
- P2 rows already depend on "authorized" outward actions (S:121, 160) while D4 (S:244-247) is decided with Phase 4 (S:154). The recommendation (a) is the working default; note the dependence.

### A4. Troubleshoot output wiring is unreconciled (minor, UNVERIFIED)
- D1's example runs `/sc:troubleshoot ... --unattended --output .dev/troubleshoot/login/` (S:228), but the section 3.1 brief for troubleshoot lists no `--output` (S:91) and AC-0.4 runs it without one (S:194). The inventory says troubleshoot defaults to a timestamped directory and writes `return-contract.yaml` only with `--caller task-unified` (INV-B:244-245 region, troubleshoot (d)). Whether `--output` exists and how WC-4 and the existing `--caller` contract interact is not stated. Cannot verify the command file here.

### A5. Standing strengths (no action)
- The decision (S:13-39) is traceable: R1-R5 each have a CAPS cite that resolves; the evidence-strength section (S:41-45) states its own gaps and Phase 0 tests the decision before anything is built on it.
- The standalone guarantees (S:141-151), the four-value outcome mapping to Orca's two outcomes (S:63; CAPS:73) and the circuit-breaker note (CAPS:80) agree with each other.

## Guard Condition Boundary Table (Nygard builds, Crispin validates, Whittaker attacks)
Guards identified: G1 outcome mapping (S:63); G2 wait cap and heartbeat cadence (S:68); G3 prompt-free launch window (S:59); G4 stale-contract on retry (S:64); G5 depth fence (S:33). Input classes left out are named per guard.
Whittaker attacks used: Zero/Empty (FR-2.1), Divergence (FR-2.2), Sentinel Collision (FR-2.3), Sequence (FR-2.4), Accumulation (FR-2.5).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 outcome mapping | S:63 | Zero/Empty | report file empty | failed branch | `--outcome failed` | OK |
| G1 | S:63 | Zero/Empty | YAML contract with no `status` key | unclear | not stated | GAP (M3, Medium) |
| G1 | S:63 | One/Minimal | non-empty Markdown report, no `status` | succeeded branch | `--outcome succeeded` (N6) | OK |
| G1 | S:63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G1 | S:63 | Sentinel Value Match | `status: partial`; audit verdict FAIL | succeeded | `--outcome succeeded`, first body sentence states status/verdict | OK |
| G1 | S:63 | Sentinel Value Match | native status such as `ok` (unknown set) | failed (outside four) | maps to failed; native set not recorded | GAP (M1, Medium) |
| G1 | S:63, 73 | Legitimate Edge Case | `succeeded` but `report_path` target missing | unclear | not stated | GAP (M3, Medium) |
| G2 wait cap | S:68 | Typical | wait of 3 minutes | no split | no change | OK |
| G2 | S:68, 114, 210 | Legitimate Edge Case | single call of 4.5 minutes | WC-10: not split; AC-4.3: fails | two thresholds | GAP (M5, Medium) |
| G2 | S:68 | Maximum/Overflow | wait of 6 minutes | split | waits of at most 4 minutes | OK |
| G3 launch prompt | S:59 | Typical | fallback 30 s | passes | evidence says passes (CAPS:49) | OK |
| G3 | S:59 | Maximum/Overflow | fallback above ~45 s | fails readiness | "well inside" with no number | GAP (minor, N1) |
| G4 stale contract | S:64, 73 | Sequence (retry) | retry of fixed-output command | old file deleted by coordinator | stated | OK |
| G4 | S:61, 64 | Sequence (ask, then re-invoke in same dir) | blocked contract still present | stale `blocked` readable | not stated | GAP (M9, Medium) |
| G5 depth fence | S:33 | Typical | command calls `worker-start` at depth 1 | refused | WC-8 forbids the call | OK |
Classes left out: G3 Zero/Empty (a launch prompt either exists or not, covered by Typical); G5 Zero (depth 0 is the coordinator only, S:97 via CAPS:97-98); G4 Maximum (the circuit breaker at 3 failures is stated at CAPS:116, not a spec guard).
FR-8/FR-9 grading: each GAP names no concrete wrong outcome that follows from the stated text without a further assumption, so each is Medium, not blocking. FR-10: all cells populated and all guards enumerated, so synthesis is not blocked.

## Minor notes
- N1. WC-1 "well inside the readiness limit" (S:59) has no number; the evidence gives 30 s passing and about 45 s failing (CAPS:49). Suggest "30 s or less".
- N2. Citations to `src/`, `CLAUDE.md`, `pyproject.toml`, `Makefile` and Orca output in S:11, 52, 62-70, 147-150, 172-175, 183, 279 could not be opened (UNVERIFIED here); the spec itself marks several of them UNVERIFIED (S:271-285).
- N3. S:222 cites `README.md:6,30`; both lines resolve (the Goal and the "Planning only" rule).
- N4. The `research` row pins `--strategy planning` under `--unattended` (S:116); if the brief also names another `--strategy` the precedence is not stated.

## follow-up candidates
Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11.
Minor: A1, A2, A3, A4, N1, N2, N3, N4.
The review loop asks the user once per loop whether to open an issue for these. This worker cannot ask the user, so it only records the list; the coordinator should put the question to the user. No issue is created.

## Briefs overridden
None. The brief did not widen scope or regrade a minor finding.

## Reviser brief
No blocking finding ids. No revision is required. (Restated for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on every addition; prefer deleting or narrowing; report byte size before and after, and bytes added and deleted per finding id.)

verdict: PASS
