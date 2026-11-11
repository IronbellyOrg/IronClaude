review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec

- Mode: `--mode critique`, `--focus requirements,architecture`, first review (no `--re-review`, no `--baseline`; `baseline: missing` not applicable because neither was given).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Reviewer model: `claude-haiku-5-5` (single reviewer, fresh context). `superclaude review panel` is not installed in this sandbox (`command -v superclaude` returned nothing), so one reviewer ran and this is stated here as the loop requires.
- Brief: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, `home/.claude/rules/prompts/document_review_loop_prompts.md`).
- Panel: requirements lead Wiegers, with Adzic and Cockburn; architecture lead Fowler, with Newman, Hohpe and Nygard; Whittaker active in every panel (`src/superclaude/commands/spec-panel.md` section "Adversarial Testing Expert", as in the command file supplied).

## What was covered

- Read in full: the candidate (`orca-worker-contract-spec.md`, 286 lines), the shared context (`.dev/orca-command-refactor/README.md`, 39 lines), the three inventories (`inventory/commands-a.md` 120 lines, `inventory/commands-b.md` 323 lines, `inventory/orca-capabilities.md` 188 lines), the command definition, and the FIRST-REVIEW prompt.
- Checked against the inventories: the `INV-A:N`, `INV-B:N` and `CAPS:N` citations in sections 1-4 and 9 of the candidate were resolved against the inventory text, sampled across all sections (not every one). Most resolve to the cited topic. The exceptions are recorded below: M9 (tool equivalence not shown), M10 (the direct-route evidence contradicts 1.4) and M14 (a nesting citation the inventory marks UNVERIFIED). `CAPS:12-13` and `CAPS:98` give only weak support for their claims and are not listed separately.
- Ran one probe in the sandbox: the AC-C1 grep pattern as written in the candidate (with `\|`) against a two-line probe file. The escaped form matched nothing; the unescaped form matched the `orca orchestration ask` line (see M8).
- Not covered: `src/superclaude/...`, `.dev/codegraph-migration/...`, `.dev/evals/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `EVIDENCE.md`, the Orca bundled code and any file outside the sandbox. The sandbox rule forbids reading them, so every citation to them is UNVERIFIED here (listed at the end). No `uv run` tests or `make` targets were run.

## Verdict

**FAIL.** One blocking finding is open (F1). Grading follows the FIRST-REVIEW grading check: a finding is blocking only when a sentence holds with no further assumption. Several Medium findings carry the label MAJOR but need an assumption, so they are Medium and listed under follow-up candidates.

Summary: 1 blocking, 17 Medium (follow-up candidates), 6 minor notes. Quality (0-10): clarity 6, completeness 6, testability 6, consistency 5.

---

## F1 (blocking): AC-0.4 cannot pass in P0 as written

- Location: `orca-worker-contract-spec.md:182` (section 7.2, step 3) and `:194` (AC-0.4).
- Step 3 pass condition: "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`:182`).
- AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`:194`). Only step 4 is exempted.
- The contract arrives in P1 (`:159`, phase P1 "The WC-4 contract in unattended mode"), so in P0 there is no WC-4 contract. `/sc:troubleshoot` writes `REPORT.md` as its `report_path` (`inventory/commands-b.md:49`, citing `sk/sc-troubleshoot-protocol/SKILL.md:63-68`, UNVERIFIED here). `/sc:adversarial` writes its contract at a path the inventory calls inconsistent (`inventory/commands-a.md:60`). Only `/sc:workflow` already writes a contract (`inventory/commands-b.md:52`).
- An implementer running AC-0.4 on `/sc:troubleshoot` gets `REPORT.md`, which step 3 rejects. The P0 gate cannot pass as stated.
- Category: unpassable-check. Expert: Adzic (acceptance criteria), with Wiegers.
- Recommendation: in P0, step 3 should check that `worker_done` names the command's existing report file (for `/sc:workflow` the contract), and the WC-4 contract-path check should start in P1. Or move the WC-4 path condition from step 3 into the P1 checks (AC-1.2).
- Priority: High. Quality impact: high, because P0 is the gate that tests the decision (section 1.4, gap 1).

---

## === REQUIREMENTS ANALYSIS ===

### M1 (Medium): WC-3's "ask then re-invoke" path has no answer channel and conflicts with the live check
- Location: `:61` (WC-3 "re-invoke or resume the command with the answer as a flag"), `:181` (step 2: "a non-null value means the worker is parked on a prompt only a person can answer").
- Wiegers: WC-3 says the answer goes back "as a flag", but section 3 never names a flag for any command's gate. Only the blocked path (WC-2c) is specified per command (`:97-125`). So for a gate that needs an answer, the spec gives no flag.
- Step 2 treats any non-null `agentWait` as failure, which is what a worker parked on `ask` would show (`inventory/orca-capabilities.md:129`, "a waiting worker is healthy, not failed"). So the live check fails the legitimate ask path. Step 2's own note in the inventory calls the state healthy.
- An implementer who uses WC-3 and runs step 2 gets a failing check on a correct worker. Using the blocked path avoids this, so WC-3 is optional under WC-2.
- Assumption needed for a blocking reading: none that the author has stated. Category: missing-requirement.
- Recommendation: either drop the ask-then-re-invoke clause until a per-command answer flag exists, or define the answer flag per command in section 3 and change step 2 to accept `agentWait` while an `ask` is pending.
- Priority: Medium-high. Quality impact: medium.

### M2 (Medium): a missing `--output` under `--unattended` is not refused
- Location: `:62` (WC-4 "In unattended mode the command writes `<output-dir>/return-contract.yaml`... is the directory the coordinator passed"), `:73` (section 2.3 coordinator brief), `:83` (adversarial "Brief must pass `--output`").
- The contract path is defined only through the coordinator-passed directory. Nothing says what an unattended run does when `--output` is absent. `inventory/commands-a.md:61` records that adversarial then writes next to its input files, so the WC-4 path is unknown before dispatch, which WC-4 requires.
- Assumption needed for a blocking reading: the spec does not say the command must refuse, so the implementer chooses. Category: missing-requirement.
- Recommendation: add a WC-2 rule: under `--unattended` a missing required output flag resolves as blocked (c) and writes no output.
- Priority: Medium. Quality impact: medium.

### M3 (Medium): WC-4's fixed path and WC-6's fresh directory conflict for retries
- Location: `:62` (WC-4 path is "the directory the coordinator passed"), `:64` (WC-6 "writes each run into a fresh output directory so a re-run starts clean"), `:63` (WC-5 "no report exists" maps to failed).
- Two readings of WC-6 are allowed: (a) the coordinator passes a new `--output` for each retry (no conflict), or (b) the command creates a subdirectory per run (then the WC-4 path is not the one the coordinator passed). Section 3 writes "fresh dir" in the Resume column without saying which party makes it.
- Under reading (b) a retry's contract is not at the path the coordinator read. Under a reuse of the old directory, WC-5 reads the first attempt's report and maps it to the retry's outcome.
- Concrete trace (Whittaker, see W3): attempt 1 writes `status: succeeded`, is fenced by `check` (WC-12, `:70`) before `worker_done`; the retry uses the same directory, crashes before writing; the report already says succeeded; WC-5 maps the retry to `--outcome succeeded`.
- Assumption needed for a blocking reading: the implementer must pick reading (a) or (b). Category: contradiction (two readings). Expert: Cockburn (the actor for the fresh directory is unnamed), Nygard (stale state).
- Recommendation: state that the coordinator passes a new `--output` for every attempt (WC-6 satisfied by the brief), and make the worker delete or refuse a non-empty contract path before a retry.
- Priority: High. Quality impact: high (silent false success).

### M4 (Medium): the workflow pre-creation contract fix is not gated, which contradicts SA-3
- Location: `:92` ("Write the contract for pre-creation STOPs too (WC-4 'every outcome') (P1)") and `:148` (SA-3 "The new contract file and report files are written only in unattended mode or when the caller passes the new output flag").
- Read literally, the fix in the "ready today" table applies in every mode. A standalone `/sc:workflow` that stops before creating a package would then write `return-contract.yaml`, which SA-3 forbids.
- Same pattern in the "needs change" table: `explain` "write the explanation to a file; contract" (`:108`) and `recommend` "write the handoff envelope to a file; contract" (`:115`) have no gate. Both would write a new file in standalone runs.
- The reading that avoids conflict (the fix is gated by `--unattended`, as WC-4 `:62` says) is available, so the implementer must choose. Category: contradiction (two readings). Expert: Wiegers.
- Recommendation: put an explicit gate in the `Small fix` and `Report` column for every row in 3.1 and 3.2 that adds a file, and say so in the table header.
- Priority: High (SA-3 is a hard requirement by section 5, `:142`). Quality impact: high if read literally.

### M5 (Medium): renaming adversarial's contract file changes standalone output
- Location: `:83` ("Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"), `:148` (SA-3 "A standalone default run writes the same files it writes today").
- The skill writes its contract on every run today (`inventory/commands-a.md:60`, citing `sk/sc-adversarial-protocol/SKILL.md:427,445`, UNVERIFIED here). A fixed name changes where a standalone run writes it, which SA-3 forbids. The row is not gated.
- Category: contradiction (two readings: the rename may be read as the defect fix SA-4 allows, `:149`). Expert: Wiegers.
- Recommendation: state that the rename applies only when `--output` is given or `--unattended` is set, or name it as an allowed SA-4 defect fix with the standalone path kept.
- Priority: Medium. Quality impact: low to medium.

### M6 (Medium): the coordinator brief cannot be built for the 27 "needs change" commands
- Location: `:73` ("the exact command line including `--unattended` and every flag section 3 lists as required"), `:75-125` (section 3 tables).
- Only the 3.1 table has a "Brief must pass" column (`:81`). The 3.2 table has gate resolutions and "Other required change" but no required-flags column, so the flags a 3.2 brief must pass (for example `--output` for `analyze`, `build`, `design`; `--suite` for `cli-eval`, mentioned in `:104`) are not all stated.
- Category: missing-requirement. Expert: Cockburn (the brief is the actor's input and must be complete).
- Recommendation: add a "Brief must pass" column to 3.2, or a per-command flag list in the P0 brief template.
- Priority: Medium. Quality impact: medium (blocks P2 dispatch).

### M7 (Medium): "run as workers now" overstates the evidence
- Location: `:79` ("These run as workers now if the brief uses the stated flags"), `:43` ("The only end-to-end proof is the PR #329 run, and its brief told workers to run `/sc:adversarial` through an Agent-tool subagent").
- Section 1.4 says no command in scope has run end to end as a direct worker (`:43`). The 3.1 table nevertheless says the ten commands "run as workers now".
- `tdd` is in the ready set, but `inventory/commands-b.md:219` and `:47` show `/task` asks the user on ambiguity mid-run, and the spec's own tdd row (`:90`) moves that to P2. A mid-run question stalls a worker with no way to pass a flag.
- Category: other (overclaim). Expert: Adzic (evidence for a claim of readiness).
- Recommendation: rename the heading to "Ready to test in P0 (unverified end to end)" and note the mid-run `/task` question for `tdd`.
- Priority: Medium. Quality impact: medium.

### Minor: N6 (the P1 flag is a no-op on gate commands)
- Location: `:159` ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)").
- Between P1 and P2 a gate command accepts `--unattended` and still prompts, so a worker dispatched in that interval stalls. The phase order does not prevent dispatch. Category: other. Severity: minor.

---

## === ARCHITECTURE ANALYSIS ===

### M8 (Medium): AC-C1 can pass without checking anything; its scope conflicts with SA-2
- Location: `:172` (AC-C1) and `:147` (SA-2 "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file").
- As the candidate is written, the escaped `\|` makes the pattern a literal pipe in ERE, so the grep matches nothing. The sandbox probe confirmed it: the escaped form returned no match (exit 1), and the unescaped alternation matched `orca orchestration ask`. The `\|` before `grep -v` is also an escaped pipe on the shell side, so copied verbatim the second grep gets no input. The candidate is a markdown table, so the escapes may be table syntax and render correctly. Whether the check works depends on how the text is copied. Category: other. Expert: Fowler (architecture gates), Nygard (failure detection).
- Second conflict, once the pattern works: AC-C1 scans `src/superclaude/core` and excludes only `ccsession-tag` (`:172`), but SA-2 explicitly allows an Orca example inside `src/superclaude/core/WORKER-CONTRACT.md` (`:147`). The check would fail on the one allowed mention.
- Recommendation: write AC-C1 in a code block outside the table, with unescaped alternation; exclude `src/superclaude/core/WORKER-CONTRACT.md` or drop core from the scan; add a self-test that the pattern matches a known fixture.
- Priority: High (the only mechanical gate for SA-2 and WC-8). Quality impact: high if copied verbatim.

### M9 (Medium): "same tools as a command a person runs" is not supported by the cited evidence
- Location: `:22` (E2 "so a command run by a worker has the same tools as a command a person runs"), evidence `CAPS:161` and `EVIDENCE.md:45`.
- `inventory/orca-capabilities.md:161` describes a worker's launch and `inventory/orca-capabilities.md:40` says subagent tool availability is UNVERIFIED. Neither line states tool equivalence. Launch flags, MCP servers and permission mode for an Orca worker are not in the inventory.
- Category: other. Expert: Fowler (launch configuration), Hohpe (message contract).
- Recommendation: mark E2's "same tools" as UNVERIFIED and add a P0 check that a worker's tool list matches a person's (for example `AskUserQuestion` absent, `Bash` and `Task` present).
- Priority: Medium. Quality impact: medium.

### M10 (Medium): section 1.4 and evidence E3 contradict each other on the direct-route evidence
- Location: `:23` (E3 "It has worked before: in the codegraph planning run, Orca workers invoked `/sc:adversarial`... return contract `invocation_method: "skill-direct"`") and `:43` (1.4 "The only end-to-end proof is the PR #329 run ... so it proves the nested route, not the direct route this spec requires").
- E3 cites a `skill-direct` contract as evidence that workers invoked commands; `inventory/commands-a.md:13` records that contract as a direct Orca-worker skill call. 1.4 says the only end-to-end proof is nested. Both cannot be the whole picture. Either the P3 run is direct evidence (1.4 understates it), or E3's support is the nested run (E3 overstates the direct route).
- Category: contradiction. Expert: Adzic (evidence), Wiegers (what the decision rests on).
- Recommendation: state which run each claim rests on; if the P3 run is direct, say so in 1.4 and keep AC-0.4 as the confirmation.
- Priority: Medium. Quality impact: medium (the decision's evidence base).

### M11 (Medium): the shared contract is an installed file with no version or fallback
- Location: `:52` ("one shared document, proposed as ... installed to `~/.claude/WORKER-CONTRACT.md`"), `:62` ("Commands that already write a contract keep their fields and add the missing ones").
- Every changed command points at `~/.claude/WORKER-CONTRACT.md` (`:52`, AC-1.1 at `:195`). A user who has not re-run `superclaude install` has the commands but not the file. The spec gives no fallback and no contract version.
- Existing contracts have their own versions: the workflow contract is "contract 1.1" (`inventory/commands-b.md:52`, citing `refs/return-contract.md:3-19`, UNVERIFIED here). WC-4 says to keep fields and add missing ones, but does not say whether to bump the version or normalize `status`.
- Category: missing-requirement. Expert: Newman (API evolution), Fowler (installed coupling).
- Recommendation: add `contract_version` to WC-4, make the commands state what they do when the installed file is absent (proceed as blocked, or write the contract with `status: blocked` and the reason), and check the existing `status` vocabulary before P1.
- Priority: Medium. Quality impact: medium.

### M12 (Medium): worker-side obligations live outside the repo and no artifact in the repo states them
- Location: `:55-70` (WC-3, WC-5, WC-7, WC-10 and WC-12 each name "Worker session" as owner), `:72-73` (section 2.3 coordinator brief).
- Five of the twelve requirements bind the worker session, and the contract file covers only command behavior (`:52`). The worker-session rules come from Orca's preamble and guide (`inventory/orca-capabilities.md:64-67`, `:78`), which is outside the repo. The brief template in P0 (`:158`) is described as "section 2 rules plus a coordinator brief template listing the section 3.1 flags", but section 2.3 does not require the brief to carry WC-5, WC-7 or WC-10.
- Category: missing-requirement. Expert: Hohpe (who owns the message contract), Fowler (ownership).
- Recommendation: give each worker-session rule an owner (preamble, brief, or contract file) and require the brief to restate WC-5 and WC-7.
- Priority: Medium. Quality impact: medium.

### M13 (Medium): mid-run tool-permission prompts are not covered
- Location: `:59` ("Nothing in the launch path (wrapper, hook, startup command) may wait on a person before Claude's input box is ready") and `:60` ("No person-blocking step in unattended mode.").
- WC-1 covers the launch path only; WC-2 covers the command's own gates only. A Claude Code tool-permission prompt during the run (for example a `Bash` or `Write` approval) is neither. `inventory/orca-capabilities.md:52` says a worker waiting on a prompt is healthy, so the stall is invisible until step 2 (`:181`) runs.
- Whether Orca's worker launch uses a permission mode that cannot prompt is UNVERIFIED here (the inventory does not say).
- Category: missing-requirement. Expert: Nygard (stall detection as a failure mode).
- Recommendation: add WC-13: the worker launch sets a permission mode that cannot prompt, or the brief lists the tools each command may use, and a worker that reports an `agentWait` on a tool prompt is treated as blocked, not healthy.
- Priority: High within Medium (silent stall). Quality impact: high.

### M14 (Medium): the tasklist nested-reflect claim relies on evidence the inventory marks UNVERIFIED
- Location: `:122` (tasklist row: "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" and "Other required change: none"), `inventory/commands-b.md:210` and `:314` (nested spawning UNVERIFIED), `inventory/commands-b.md:215` (recommends the per-phase reflect fan-out run at the worker's top level).
- The spec cites `INV-A:14`, which states the three-layer nesting limit from the Claude Code docs, but the inventory's own tasklist row says nested reflect is UNVERIFIED and recommends changing it. The spec states "Other required change: none" without a Decisions entry recording the divergence.
- Category: contradiction (between the spec and its source). Expert: Newman (service boundaries), Hohpe (fan-out path).
- Recommendation: record the divergence in Decisions and add an AC that runs the tasklist reflect fan-out as a worker.
- Priority: Medium. Quality impact: medium.

### M15 (Medium): unattended reflect and tasklist auto-accept remediation, which D2's rationale forbids for Rulings
- Location: `:88` (reflect "make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt (P2)"), `:122` (tasklist "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies"), `:236` (D2 "because the rule exists to stop an agent approving its own work").
- D2 protects implement's Ruling so an agent cannot approve its own work. Under the same `--unattended` switch, reflect's headless rule auto-accepts remediation for auto-fixable findings, and the findings and the remediation come from the same agent (`inventory/commands-b.md:109`, citing `remediation-handoff.md:239-247`). The spec does not decide whether that is intended.
- Category: other (open decision not stated). Expert: Nygard (blast radius), Whittaker (divergence, see W4).
- Recommendation: add this as a decision for the user (D6), or require an explicit `--auto-accept` flag in the brief for the remediation path.
- Priority: Medium. Quality impact: medium to high.

### M16 (Medium): "well inside the readiness limit" is not quantified
- Location: `:59` ("Any such prompt must fall back on its own well inside the readiness limit (default 60 s)").
- The evidence fixes the numbers: a 30 s fallback passed and a limit above about 45 s failed again (`EVIDENCE.md:45,56` as cited in `inventory/orca-capabilities.md:49`). The spec says "well inside" with no number.
- Category: missing-requirement (unspecified boundary). Expert: Nygard.
- Recommendation: state the fallback as 30 s (or any value under 30 s) and test it in AC-0.1 or the 7.2 check.
- Priority: Medium. Quality impact: low to medium.

### M17 (Medium): cli-portify's hardcoded template path breaks the repo rule for installed primitives, and the AC list does not check it
- Location: `:105` ("dispatch only inside an IronClaude checkout (hardcoded template path)"), `:176` (AC-C5 applies to edited files without a defect fix).
- `inventory/commands-a.md:68` records that the path is `src/superclaude/examples/release-spec-template.md`, which is not installed. CLAUDE.md's "Never Hardcode src/superclaude/ Paths in Installed Primitives" rule requires a grep check of each edited primitive (CLAUDE.md, UNVERIFIED here). The spec's acceptance checks do not include that grep, and the spec does not require the path to be fixed.
- Category: other. Expert: Fowler (dependency on the source tree).
- Recommendation: add the repo's `grep -rn 'src/superclaude'` check to section 7.1 for every phase that edits a primitive, and either fix the cli-portify template path in P2 or record it as an accepted restriction.
- Priority: Medium. Quality impact: medium.

### Minor notes (architecture)
- N1 (Hohpe): WC-4 does not require the contract to be fully written before `worker_done` (`:62`, `:63`). A reader can open a partial YAML. Category: missing-requirement. Severity: minor.
- N2 (Nygard): WC-10 leaves a single wait of 4.5 minutes or exactly 5:00 unassigned: "longer than 5 minutes" must be split to 4 (`:68`), and the heartbeat is "every 5 minutes" (`:70`). Severity: minor.
- N3 (Wiegers): WC-5 maps `partial` to `succeeded` (decision at `:263`). Accepted, and the body's first sentence still carries the status, but a coordinator that reads only Orca's outcome cannot see partial runs. Severity: minor.
- N4 (Wiegers): section 9 D1 says detection by flag "cannot misfire on a person" (`:228`), but a flag inside quoted topic text is not addressed. Category: other. Severity: minor.
- N5 (Wiegers): `pr-submit` is counted among the 27 "needs change" commands (`:114`), while the recommended D3 makes it coordinator-only. Count and disposition disagree until D3 is answered (`:139`). Severity: minor.

---

## Adversarial analysis (Whittaker)

Format per the command's template. Five attacks; each finding is also in the findings block above.

- W1 (FR-2.1 Zero/Empty, Medium, M2): I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`:62`)** fails when **`--output` is omitted under `--unattended`**. Concrete attack: brief passes no `--output`; adversarial writes its contract next to its input (`inventory/commands-a.md:61`); the coordinator reads the directory it passed, finds nothing, and WC-5 reports failed while the real contract sits elsewhere.
- W2 (FR-2.4 Sequence, Medium, M1): I can break this specification by **Sequence Attack**. The invariant at **WC-3 (`:61`)** fails when **the ask answer is applied by re-invoking a command with no answer flag**. Concrete attack: run 1 blocks and writes `dir1/return-contract.yaml` with `status: blocked`; the answer arrives; run 2 with no answer flag either reuses `dir1` (clobbers run 1, breaks WC-6) or writes `dir2` (the path worker_done reports differs from the one the coordinator read, breaks WC-4).
- W3 (FR-2.5 Accumulation of state, Medium, M3): I can break this specification by **Accumulation Attack**. The invariant at **WC-5 (`:63`)** fails when **a retry writes into an output directory that holds an earlier attempt's report**. Concrete attack: attempt 1 writes `status: succeeded`, then `check` returns fenced (WC-12, `:70`) before `worker_done`; the retry starts in the same directory, crashes before writing, and sends `--outcome succeeded` because a report exists and says succeeded.
- W4 (FR-2.2 Divergence, Medium, M15): I can break this specification by **Divergence Attack**. The invariant at **section 9 D2 (`:236`)** fails when **the same `--unattended` switch resolves reflect's remediation prompt by headless auto-accept (`:88`)**. Concrete attack: `/sc:tasklist --unattended` runs Stage 10.5 (`:122`); reflect auto-accepts remediation for auto-fixable findings; the agent that found the defect also applies the fix; no decision was recorded.
- W5 (FR-2.3 Sentinel Collision, Minor, N4): I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (`:228`)** fails when **the switch token appears inside quoted topic text**. Concrete attack: `/sc:tdd "add --unattended support"` with the token inside quotes; a detector that greps the argument string enters unattended mode; D1 says detection is by brief flag, so the spec does not say which parser applies.
- W6 (FR-2.1 Zero/Empty on the report, Medium, folded into the guard table G2): a 0-byte report file "exists", so WC-5 maps it to succeeded. The spec does not say what "report exists" means. The guard table records it as GAP.

---

## === GUARD CONDITION BOUNDARY TABLE ===

Triggered: the candidate has conditional gates (WC-2), an outcome mapping (WC-5), numeric thresholds (WC-1 60 s, WC-10 4 and 5 min) and a switch (D1). Columns follow the command template. One row per input class that applies. Classes left out have a one-line reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | D1 `:228`, SA-1 `:146` | Zero/Empty (switch absent) | no flag | false | Standalone behavior unchanged | OK |
| `--unattended` switch | WC-2 `:60` | One/Minimal (switch present, required flag missing, e.g. cli-eval without `--suite`) | `--unattended`, no `--suite` | true | blocked, contract `status: blocked` (`:104`, AC-2.2 `:200`) | OK |
| `--unattended` switch | D1 `:228` | Sentinel Value Match (token inside quoted topic) | token in quotes | not specified | no parse rule given (N4, W5) | GAP |
| `--unattended` switch | WC-2 `:60` | Legitimate Edge Case (switch with all flags present) | all flags | true | documented defaults apply (WC-2a) | OK |
| WC-5 outcome | `:63` | Zero/Empty (no report) | none | true | `--outcome failed` | OK |
| WC-5 outcome | `:63` | One/Minimal (0-byte report) | empty file | true | "otherwise succeeded"; a 0-byte file is not defined as no report (W6) | GAP |
| WC-5 outcome | `:63` | Typical (`status: succeeded`) | succeeded | false | `--outcome succeeded` | OK |
| WC-5 outcome | `:263` | Sentinel Value Match (`status: partial`) | partial | false | maps to succeeded (decision; N3) | OK |
| WC-5 outcome | `:63`, `:64` | Legitimate Edge Case (stale report in reused dir) | stale succeeded | false | reads stale status (M3, W3) | GAP |
| WC-4 contract path | `:62` | Zero/Empty (no `--output`) | none | path undefined | not specified; adversarial defaults next to input (M2, W1) | GAP |
| WC-4 contract path | `:62`, `:158` | Typical (`--output` given, fixed contract name) | dir | path = dir/return-contract.yaml | OK in P1 | OK |
| WC-4 contract path | `:83`, `inventory/commands-a.md:60` | Typical before P1 (adversarial) | dir | path not fixed | fixed by the P1 rename (M5) | GAP |
| WC-4 contract path | `:64` | Legitimate Edge Case (WC-6 fresh directory for a no-resume command) | new subdir | path differs from WC-4 | conflict (M3) | GAP |
| WC-1 readiness | `:59` | Typical (prompt answered by 30 s fallback) | 30 s | ready within 60 s | OK, value from evidence outside the workspace (UNVERIFIED here) | OK |
| WC-1 readiness | `:59` | Max/Overflow (prompt unanswered 45-60 s) | 50 s | start fails above about 45 s (evidence cited in inventory) | "well inside" unquantified (M16) | GAP |
| WC-1 readiness | `:59` | Zero/Empty (`--timeout-ms` omitted) | none | default 60 s (`CAPS:44`) | OK | OK |
| WC-10 wait | `:68` | Typical (3 min wait) | 3 min | not split | OK | OK |
| WC-10 wait | `:68`, `:70` | Legitimate Edge Case (4.5 min single wait) | 270 s | not split, not over 5 min | unassigned (N2) | GAP |
| WC-10 wait | `:68`, `:70` | Sentinel Value Match (exactly 5:00) | 300 s | "every 5 minutes" vs "longer than 5 minutes" | unassigned (N2) | GAP |
| WC-10 wait | `:68`, `sk/sc-cli-eval-protocol/SKILL.md:151` | Max/Overflow (eval up to 3600 s) | 3600 s | split to at most 4 min | OK | OK |
| WC-3 ask | `:61` | Zero/Empty (no `--timeout-ms`) | none | default UNVERIFIED (`CAPS:68`) | resume by message ID (`:61`) | GAP |
| WC-3 ask / step 2 | `:61`, `:181` | Typical (ask pending) | agentWait non-null | step 2 fails | conflict (M1) | GAP |
| WC-9 outward | `:67` | Zero/Empty (no authorizing flag) | none | off | off | OK |
| WC-9 outward | `:67`, D4 `:245` | Typical (brief authorizes, explicit flag) | `--post-pr` | on | on only through the command's flag | OK |

Left out, one line each: WC-12 `consumer_fenced` (single behavior, stop without `worker_done`, `:70`); Max/Overflow for WC-5 (the mapping has no count or limit); Sentinel Value Match for WC-9 (no sentinel in the outward rule).

## Pipeline Dimensional Analysis

Not triggered. The candidate has no stage where an output count differs from its input count. The WC-5 mapping is many-to-one on status values, not counts, and no quantity flow is described. No Quantity Flow Diagram is produced.

## Correctness focus (advisory)

Not forced. The candidate has guard conditions with numeric thresholds (WC-1, WC-10), so the panel suggests `--focus correctness` in a later round. The State Variable Registry is mandatory only under that focus and is not produced here.

---

## Expert consensus and disagreements

- Consensus: the decision (commands stay units of work, Orca coordinates) is sound, and the contract is testable in principle (Wiegers, Fowler, Hohpe). The acceptance checks in section 7 are the spec's strongest part (Adzic).
- Consensus: the P0 gate must pass before P1 starts; F1 blocks that (Adzic, Nygard).
- Disagreement: Whittaker would make the stale-report and empty-report cases blocking under MAJOR labels. The FIRST-REVIEW grading check makes them Medium (M3, W6) because each needs a reading the text does not fix. The coordinator should settle this, since it changes the revision scope.
- Disagreement: Fowler reads M4 (the ungated workflow fix) as a contradiction; Wiegers reads §3.1 as gated by WC-4's `:62` scope. Recorded as Medium with both readings.

## Improvement roadmap

- Immediate (blocking): F1. Restate step 3 for P0 or move the WC-4 check to P1.
- Short term (before P1): M2, M3, M4, M5, M8 (AC-C1 as a code block), M13.
- Before P2: M1, M6, M7, M11, M12, M14, M15 (open decision D6), M17.
- Later: M9, M10, M16, N1-N6.

## Quality metrics (0-10)

- Clarity 6 (language is precise; the 3.1 vs 3.2 split and the "contract" term are used in several senses).
- Completeness 6 (missing: stale-state rule, permission prompts, brief flags for 3.2, installed-file fallback).
- Testability 6 (acceptance checks are concrete; AC-0.4 and AC-C1 do not test what they say).
- Consistency 5 (SA-3 against the 3.1 and 3.2 fixes; step 3 against AC-0.4; section 1.4 against E3; the tasklist row against its source).

---

## Follow-up candidates (Medium and minor, not blocking)

The session that ran this review must ask the user once per loop whether to open an issue for these. No issue is created without that answer. Under `--unattended` the list is only recorded.

1. M1 WC-3 ask path has no answer flag; step 2 conflicts.
2. M2 missing `--output` not refused under unattended.
3. M3 WC-4 fixed path against WC-6 fresh directory for retries; stale report.
4. M4 workflow pre-creation contract, explain and recommend file writes not gated (SA-3).
5. M5 adversarial contract rename changes standalone path.
6. M6 no per-command required flags for the 3.2 rows.
7. M7 "run as workers now" overclaim; tdd mid-run `/task` question.
8. M8 AC-C1 escaped pipes; scope against SA-2.
9. M9 "same tools" unsupported.
10. M10 section 1.4 and E3 disagree on the direct-route evidence.
11. M11 installed contract file, no version or fallback.
12. M12 worker-side obligations have no repo owner; brief omits WC-5, WC-7.
13. M13 mid-run tool-permission prompts not covered.
14. M14 tasklist nested reflect relies on UNVERIFIED evidence; divergence not recorded.
15. M15 unattended reflect and tasklist auto-accept remediation; open decision D6.
16. M16 "well inside the readiness limit" unquantified.
17. M17 cli-portify hardcoded template path; no repo grep in section 7.
18. N1 to N6 as listed above.

## Decisions (this review)

- Findings block is the last section; the Reviser brief sits directly above the final verdict line, to satisfy both the prompt ("last section") and the command ("just above the final verdict line"). The verdict is the last line.
- Standard format: no `--format` was passed, so the standard keys are rendered as the sections above (`specification_review` = header, `quality_assessment` = metrics, `critical_issues` = F1 and the Medium list, `expert_consensus`, `improvement_roadmap`, `adversarial_analysis` = Whittaker section).
- Single reviewer, because `superclaude review panel` is not installed. Stated here and in the header.
- Grading: FIRST-REVIEW grading check. A MAJOR label alone does not make a finding blocking.
- Output path: the brief names `review/round1.md`; the shared README names `review/spec-panel.md`. The brief's path was used.

## UNVERIFIED citations (outside the sandbox workspace)

- Every `src/superclaude/...` path cited in the candidate (for example `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `src/superclaude/examples/release-spec-template.md`).
- `.dev/codegraph-migration/...` (PR #329 and P3 contract, `:23`, `:43`), `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md` (`:39`, `:45`, `:56`), `CLAUDE.md` rules, `tests/skills/...`, `pyproject.toml:38`, `Makefile` targets.
- Orca bundled code (`app.asar.unpacked/out/...`) cited through the inventory.
- Skill and command files under `~/.claude/` cited through the inventories (for example `sk/sc-pr-submit-protocol/SKILL.md:37-39`).
- The inventory's own citations to `src/superclaude/...` were not checked; the inventories were read in the workspace only.

---

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "its report path is the WC-4 contract path", "anchor2": "step 4 uses the command's existing report file, since the contract arrives in P1", "refs": ["AC-0.4", "7.2 step 3", "WC-4", "P0"], "claim": "AC-0.4 requires steps 1-3 to pass in P0, but step 3 requires the WC-4 contract path and the contract arrives only in P1, so a P0 troubleshoot run that reports REPORT.md cannot pass."}
{"id": "M1", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "re-invoke or resume the command with the answer as a flag", "anchor2": "a non-null value means the worker is parked on a prompt only a person can answer", "refs": ["WC-3", "WC-4", "WC-6", "7.2 step 2"], "claim": "WC-3 requires an answer flag that no section 3 row defines, and the step 2 check fails a worker parked on an ask."}
{"id": "M2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "In unattended mode the command writes", "refs": ["WC-4", "2.3", "adversarial row"], "claim": "An unattended run without --output has no defined contract path, and nothing refuses it."}
{"id": "M3", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "is the directory the coordinator passed", "refs": ["WC-4", "WC-5", "WC-6", "WC-12"], "claim": "The fixed WC-4 path and the WC-6 fresh directory cannot both hold for a retry, and a retry in a reused directory can report a stale succeeded outcome."}
{"id": "M4", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Write the contract for pre-creation STOPs too", "anchor2": "written only in unattended mode or when the caller passes the new output flag", "refs": ["SA-3", "3.1 workflow row", "3.2 explain row", "3.2 recommend row"], "claim": "Read literally, the ungated workflow fix and the explain and recommend file writes create new files in standalone runs, which SA-3 forbids."}
{"id": "M5", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Fix the contract filename to", "anchor2": "A standalone default run writes the same files it writes today", "refs": ["SA-3", "SA-4", "adversarial row"], "claim": "Renaming the adversarial contract changes where a standalone run writes it, which SA-3 forbids unless gated."}
{"id": "M6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "every flag section 3 lists as required", "refs": ["2.3", "3.2"], "claim": "The 3.2 rows have no required-flags column, so a coordinator cannot build the brief the section requires."}
{"id": "M7", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "These run as workers now if the brief uses the stated flags", "anchor2": "The only end-to-end proof is the PR #329 run", "refs": ["1.4", "3.1", "tdd row"], "claim": "The ready-today claim overstates evidence the spec itself says is missing, and tdd can stall mid-run on a /task question."}
{"id": "M8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "grep -v '^src/superclaude/skills/ccsession-tag/'", "anchor2": "The only allowed mention of Orca in a changed command", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "The AC-C1 pattern is a literal pipe when copied verbatim so it can pass without checking, and once it works its scope fails the contract file that SA-2 allows to mention Orca."}
{"id": "M9", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "so a command run by a worker has the same tools as a command a person runs", "refs": ["E2", "CAPS:161", "EVIDENCE:45"], "claim": "The cited evidence does not show tool equivalence for an Orca worker launch."}
{"id": "M10", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "so it proves the nested route, not the direct route this spec requires", "anchor2": "It has worked before: in the codegraph planning run", "refs": ["E3", "1.4", "INV-A:13"], "claim": "E3 cites a skill-direct run as evidence while 1.4 says the only end-to-end proof is nested, so the evidence base is inconsistent."}
{"id": "M11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "one shared document, proposed as", "anchor2": "Commands that already write a contract keep their fields and add the missing ones", "refs": ["2.1", "WC-4", "INV-B:52"], "claim": "The shared installed contract has no version, no fallback when the install is missing, and no rule for existing contract versions."}
{"id": "M12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "What the coordinator owes each worker", "refs": ["WC-3", "WC-5", "WC-7", "WC-10", "WC-12", "2.3"], "claim": "Five worker-session rules have no repo artifact and the brief template does not require the coordinator to restate them."}
{"id": "M13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "No person-blocking step in unattended mode.", "anchor2": "Nothing in the launch path", "refs": ["WC-1", "WC-2", "CAPS:52"], "claim": "A mid-run tool-permission prompt stalls a worker and is treated as healthy, and neither WC-1 nor WC-2 covers it."}
{"id": "M14", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "its reflect fan-out runs one layer below the worker", "anchor2": "so the headless rule applies", "refs": ["tasklist row", "INV-A:14", "INV-B:210", "INV-B:215"], "claim": "The spec relies on a nesting citation while its inventory marks nested reflect UNVERIFIED and recommends a change, with no recorded decision."}
{"id": "M15", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "because the rule exists to stop an agent approving its own work", "anchor2": "follow the existing headless auto-accept rule instead of the", "refs": ["D2", "reflect row", "tasklist row", "SA-6"], "claim": "Unattended reflect and tasklist auto-accept remediation by the same agent that found the defects, which D2's rationale forbids for Rulings, and the spec does not decide it."}
{"id": "M16", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "well inside the readiness limit", "refs": ["WC-1", "EVIDENCE:45,56"], "claim": "The readiness fallback is not quantified, so a fallback of 50 s passes the wording and fails in practice."}
{"id": "M17", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "dispatch only inside an IronClaude checkout", "anchor2": "For every command file the phase edits without a named defect fix", "refs": ["cli-portify row", "7.1 AC-C5", "CLAUDE.md installed-primitive rule"], "claim": "The cli-portify hardcoded template path breaks the installed-primitive rule and no acceptance check covers it."}
{"id": "N1", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "The worker passes the contract path as", "refs": ["WC-4", "WC-5"], "claim": "The contract need not be fully written before worker_done, so a reader can see a partial file."}
{"id": "N2", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "must be split into waits of at most 4 minutes", "refs": ["WC-10"], "claim": "A single wait of 4.5 minutes or exactly 5 minutes is not assigned to either rule."}
{"id": "N3", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "A partial run left a usable deliverable", "refs": ["WC-5", "decisions table"], "claim": "partial maps to succeeded, so a coordinator reading only Orca's outcome cannot see partial runs."}
{"id": "N4", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "It is testable by grep and cannot misfire on a person", "refs": ["D1"], "claim": "Flag detection by grep is not guarded against the token inside quoted text."}
{"id": "N5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "stays a worker candidate only if the user accepts open decision D3", "refs": ["3.2", "section 4", "D3"], "claim": "pr-submit is counted as a needs-change worker while the recommended D3 makes it coordinator-only."}
{"id": "N6", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["P1", "P2"], "claim": "Between P1 and P2 a gate command accepts --unattended and still prompts, so an early dispatch stalls."}
```

## Reviser brief

Blocking finding ids: F1.

Restatement of the rule (Review Loop bullet 6): revise only the text a blocking finding names; add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Medium and minor findings never trigger a revision, and this brief cannot widen that scope.

Brief for F1 only: in `specs/orca-worker-contract-spec.md`, section 7.2 step 3 (line 182) and AC-0.4 (line 194), make the P0 check consistent with the P0 contract state. Step 3 must not require the WC-4 contract path before P1; in P0 it checks that `worker_done` names the command's existing report file, and the WC-4 contract-path check is assigned to P1 (AC-1.2).

verdict: FAIL
