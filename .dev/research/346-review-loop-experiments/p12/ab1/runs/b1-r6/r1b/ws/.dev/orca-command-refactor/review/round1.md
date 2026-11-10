review: 1 of 3

# Spec-panel review, round 1: Orca worker contract spec

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36` (read in full).

## Header

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given, so first review. This is one of the three first reviews the prompt describes (`document_review_loop_prompts.md:34`). The merge and the VERIFY step belong to the coordinator (`:35`, `:53-58`). `baseline: missing` does not apply (neither `--re-review` nor `--baseline` was passed).
- reviewer model: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
- also read: `.dev/orca-command-refactor/README.md` (sha256 `086e5b822e3ba426fa38743895713faff8aefa579650507c332b1e776852069e`); `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md` (spot checks only). The panel read `command.md` as the command definition.
- Citation scope: only the three inventory files can be checked in this sandbox. Every citation to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `~/.claude/...` or Orca internals was not checked against a file and is UNVERIFIED unless an inventory line quotes it. The inventory lines the spec cites were spot-checked and found as cited: `CAPS:97-103,130,145,147-151,155-161`, `INV-A:3,76-83,94-98,106`, `INV-B:3,177-185,320-323`.
- Focus: requirements, architecture. `--focus correctness` is not active, so no State Variable Registry is owed.
- Panel: Wiegers (lead), Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker. Crispin, Gregory and Hightower are not part of the requirements/architecture focus panels.

## Grading note

Each finding below was graded with the FIRST-REVIEW grading check (`document_review_loop_prompts.md:33`). Blocking means the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption: two stated texts contradict, or a stated acceptance check cannot pass. A finding that needs a guess about which of two readings is picked, or that is a requirement the document never states, is Medium.

## Blocking findings

### B1 (CRITICAL; Wiegers, Adzic, Whittaker) Phase 0 acceptance check AC-0.4 cannot pass as written

Stated texts that contradict:

- Spec line 182 (7.2 step 3): "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Spec line 194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
- Spec line 158 (P0): the three smoke commands are `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --output <dir>`, run before any command edit.
- Spec line 91 (3.1 troubleshoot): its report today is `REPORT.md`, with no contract. Spec line 83: adversarial's contract filename "not fixed". The WC-4 contract is added only in P1 (spec line 159).

Wrong outcome: an implementer who follows the stated text builds a P0 gate that requires step 3 to pass, so the worker's report path must be the WC-4 contract path and the outcome must match the contract's `status`. For `/sc:troubleshoot` no such contract exists in P0, and the spec says it arrives in P1. AC-0.4 carves out only step 4, not step 3. The P0 smoke runs can therefore never pass. Line 154 says later phases do not start until the earlier phase's checks pass, and line 194 says "a failure here reopens section 1", so a correct run triggers the reopen rule. Fix by relaxing step 3 for P0 to "the report path is the command's existing report file", the same carve-out given for step 4.

### B2 (MAJOR; Wiegers, Fowler) `/sc:load`: the per-command table and the P1 acceptance check contradict each other

Stated texts that contradict:

- Spec line 112 (3.2 load row): Report (WC-4) "none (see note)"; "use it as a step inside another worker's brief, not as its own Task"; Phase "P1 (usage line only)".
- Spec line 159 (P1): "`load` (usage line only)".
- Spec line 265 (Decisions): "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- Spec line 195 (AC-1.1): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `load` is in section 3.2, line 112.
- Spec line 76: "Every changed command also gains the `## Unattended mode` section". Line 159 also says `--unattended` is accepted "by every command in sections 3.1 and 3.2", including `load`.

Wrong outcome: an implementer who does exactly what the load row and the Decisions row say (fix the Usage line only, add no report) fails AC-1.1, because the test requires an Unattended-mode section naming `return-contract.yaml` in `cmd/load.md`. An implementer who satisfies AC-1.1 adds a contract and a section to `load`, which line 265 calls an unrequested addition and line 112 says is not needed. AC-1.1 has no exception for `load`, so P1 cannot pass without breaking one of the two stated texts. Fix by naming `load` as the exception in AC-1.1, or by removing `load` from the "every command in 3.1-3.2" scope.

## Medium findings (follow-up candidates, not blocking)

These are missing or ambiguous requirements, or need a guess about which reading an implementer picks.

- **M-a (Wiegers): WC-4 `<output-dir>` versus file-valued `--output`.** WC-4 (spec line 62) defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)". Section 3.1 gives `--output <file>` for init-lite (line 87) and tdd (line 90), and section 2.3 (line 73) says the report path is known before dispatch from "the output directory". Where the contract goes for a file-valued `--output` is never stated, and `<file>/return-contract.yaml` is impossible. `command.md:460` shows the live command solved this with a separate `--report-dir`, which the spec does not use. The spec row for spec-panel (line 120) says "add `--output`", yet `command.md:23` already lists `[--output <file>]`. The inventory (`INV-B:177-185`) says no `--output` flag exists, so the spec's spec-panel citations (`cmd/spec-panel.md:22,34-35,222,451,455`) appear stale against `command.md`; its line 455 is now the "Unattended mode" section, and the "Will Not: Modify specifications" text the spec cites at :451 is at `command.md:479`. Recommend deciding one flag shape (a directory flag distinct from file-valued `--output`) and re-checking the spec-panel row.
- **M-b (Hohpe): the workflow contract location is unknown before dispatch.** The 3.1 workflow row (line 92) puts the contract in `.dev/tasks/to-do/<id>/return-contract.yaml` and asks for it on "pre-creation STOPs" too. The `<id>` directory does not exist before a package is created, and WC-4 requires the path to be known before dispatch (line 62, line 73). Where a pre-creation STOP writes the file is never stated. adversarial (`<output>/adversarial/return-contract.yaml`, line 83), implement (beside `progress.md`, line 109) and pr-submit (beside the jsonl, line 114) also differ from the `<output-dir>/return-contract.yaml` shape that WC-4 sets, so the path rule is per command, not one rule.
- **M-c (Fowler, Nygard): AC-C1 against the new core text.** AC-C1 (line 172) greps `src/superclaude/core` for `orca[-ide] (orchestration|worktree|terminal|agent)` and expects no output. Yet P0 (line 158) adds an Orca section to `core/HOW-WE-WORK.md` and a new `core/WORKER-CONTRACT.md` that SA-2 (line 147) lets mention Orca "as an example of a caller's question channel". If either file writes the CLI command `orca orchestration ...` the check fails. The spec does not say how the wording must avoid the pattern, or exclude the two files from AC-C1.
- **M-d (Cockburn): D4 and Phase order.** Line 154 says Phases 1-3 need no user decision, but D4 (line 244) lists auggie-review `--post-pr` and task `commit`/`push`, both set in P2 (lines 100 and 121). Option D4 (b) "Never" would contradict the P2 rows. The recommendation (a) makes this safe if accepted.
- **M-e (Newman): P1 touches D3/D2/D4 commands.** P1 adds `--unattended` to every command in 3.1/3.2 (line 159), including implement, post-release and pr-submit, whose gates wait for P4 answers. If D3 (a) is chosen, pr-submit stays coordinator-only but still gets a P1 Unattended section under AC-1.1. The spec does not say what pr-submit's P1 section contains when D3 (a) wins.
- **M-f (Wiegers): SA-3 against WC-4.** WC-4 writes the contract "in unattended mode" (line 62); SA-3 (line 148) adds "or when the caller passes the new output flag". The two triggers differ, and AC-1.3 (line 197) tests only the no-flag case.
- **M-g (Nygard): WC-3 `ask` and acceptance check 7.2 step 2.** WC-3 (line 61) lets a blocked worker wait in `ask`, while 7.2 step 2 (line 181) and AC-2.2 (line 200) require `agentWait` never to be non-null. Whether a worker parked in `ask` shows `agentWait` is not established (`CAPS:52,129` describe prompts for a person, not `ask`).
- **M-h (Fowler): D5 wording.** D5 (b) (line 252) calls R1 "protection against runaway fan-out", but R1 (line 33) is a reason for rejecting a design, not a protection.
- **M-i (Whittaker, Sequence attack): P0 smoke commands run without `--unattended`.** The 3.1 rows tell the brief to pass the listed flags, and section 2.3 (line 73) says every brief includes `--unattended`, yet `--unattended` does not exist until P1. A worker that follows 2.3 in P0 passes an unknown flag. The spec should say 2.3 applies from P1.

## Minor notes

- Section 3's heading (line 76) says "10 ready today, 27 needing a change and 6 coordinator-only". I counted 10 rows in 3.1, 27 in 3.2 and 6 in section 4 (43 total), and the P1 to P3 command lists match the Phase column. No defect.
- Line 11 lists 11 locations the author says were re-read on 2026-11-02; none can be checked here (UNVERIFIED).
- Line 25 (E5): the `grep -rlni orca` result and the `HOW-WE-WORK.md` count of `0` are UNVERIFIED here.
- Line 14 of UNVERIFIED items says a validator found 9 defects in about 340 citations; the validator output is not in the sandbox (UNVERIFIED).

## Guard Condition Boundary Table

Guards in the spec are thresholds on time and counts. Input classes that cannot occur for a guard are left out with the reason in the last column of the notes below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Nesting depth limit (1) | spec line 33 (R1), line 66 (WC-8) | Typical | depth 1 worker calls `worker-start` | refused | refusal `nested_worker_depth_exceeded` (`CAPS:101`) | OK |
| Nesting depth limit (1) | line 66 (WC-8) | Legitimate edge: depth-1 worker calls `task-create` | `task-create` | unknown | UNVERIFIED (line 276, item 5); WC-8 forbids it | OK (stated as forbidden) |
| Readiness limit 60 s | line 59 (WC-1) | Maximum/overflow | fallback above about 45 s | fails | spec says WC-1 needs a fallback "well inside" the limit; the evidence cited gives 30 s passes and about 45 s fails | OK |
| Heartbeat 5 min / wait 4 min | line 68 (WC-10) | Typical | 4 min wait | heartbeat possible | split waits at most 4 minutes | OK |
| Heartbeat 5 min / wait 4 min | line 68 (WC-10) | Maximum | single tool call over 5 min | no heartbeat | split required; pr-submit per-iteration time UNVERIFIED (line 283) | OK |
| Confidence 0.70 (task) | line 121 | Sentinel value match | exactly 0.70 | not stated | not stated; the cited gate text says "below 0.70" (UNVERIFIED) | OK (inherits the command) |
| `--monitor 1` refusal | line 114 | Typical | `--monitor 1` | refused | refused under `--unattended` | OK |
| `partial` maps to `succeeded` (WC-5) | line 63 | Legitimate edge case | `partial` plus failing audit verdict | succeeded | stated: audit FAIL still succeeded | OK |
| WC-4 contract path | line 62 | Zero/Empty | no `--output` passed | none | not stated for commands whose output is a file (see M-a) or has no flag | GAP (Medium, M-a) |
| WC-4 contract path | line 62, 92 | Legitimate edge: stop before output exists | pre-creation STOP of workflow | none | location not stated (see M-b) | GAP (Medium, M-b) |
| AC-C1 grep | line 172 | Legitimate edge | the new core Orca text | match | not stated (see M-c) | GAP (Medium, M-c) |

Left out, with the reason: One/Minimal and Maximum for the depth guard and the `--monitor` guard (the values are enumerated flags, not counts); Zero/Empty for the heartbeat guard (a zero-length wait is not a wait).

## Quantity Flow Diagram

Pipeline Dimensional Analysis is not triggered: the spec describes a phase sequence, not a data pipeline whose output count differs from its input count. The 43 → 10/27/6 split was counted and conserves (10 + 27 + 6 = 43).

## Expert notes (critique mode)

=== REQUIREMENTS ANALYSIS ===

- Wiegers: the WC rows give clear owners and evidence, but AC-0.4 (B1) and AC-1.1 (B2) are acceptance checks that disagree with the requirements they check. The WC-4 path definition (M-a) is the one requirement an implementer cannot apply to file-valued `--output` commands.
- Adzic: the live check in 7.2 gives concrete steps, and the tdd bare-topic and cli-eval no-`--suite` examples (line 200) are good degenerate inputs. Add the same for the P0 carve-out (B1).
- Cockburn: the primary actor (coordinator) and goal are stated in 2.3; D1 to D5 are written as decisions for the user with a recommendation each.

=== ARCHITECTURE ANALYSIS ===

- Fowler: the separation "Orca on top, commands as units of work" is clean and the rejected alternative is argued from evidence (R1 to R5). One shared contract file with per-command sections is the right boundary. The path rule per command (M-b) should be one rule.
- Newman: backward compatibility is handled by SA-1 to SA-6 and opt-in `--unattended`. The only soft spot is the P1 scope for D-dependent commands (M-e).
- Hohpe: report-file handoff via `worker_done --report-path` is a simple message pattern; the unknown-before-dispatch path (M-b) breaks the "known before dispatch" guarantee at line 62.
- Nygard: failure modes are covered (stall, blocked, retry, ask timeout). `ask` and the `agentWait` check (M-g) is the one unstated interaction.
- Whittaker: Sequence attack on P0: run the smoke commands before P1 exists, per line 194; step 3 fails (B1). Sequence attack on 2.3 versus P0 (M-i). Divergence attack on `<output-dir>` for file-valued flags (M-a).

## Follow-up candidates

M-a, M-b, M-c, M-d, M-e, M-f, M-g, M-h, M-i (above), plus the minor notes. This run records them and does not open an issue; the session that ran the review asks the user once per loop whether to open one.

## Coverage

All 284 lines of the spec were read. Cross-checked against the three inventory files where cited (spot checks listed in the header). Not covered: any citation to a file outside the workspace (UNVERIFIED), and the per-command 3.1/3.2 evidence columns beyond the counts and the rows named above. This review did not edit the candidate and started no other review.

## Reviser brief

Blocking finding ids: B1, B2.

Rules for the reviser (restated from the command's Review Loop bullet 6):

- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone.

B1: spec line 182 (7.2 step 3 requires "its report path is the WC-4 contract path") contradicts spec line 194 (AC-0.4: the contract "arrives in P1"). Stated wrong outcome: the P0 gate cannot pass for `/sc:troubleshoot`, which has only `REPORT.md` (spec line 91).

B2: spec lines 112, 159 and 265 (`load`: no report, usage line only, a report file is an unrequested addition) contradict spec line 195 (AC-1.1 requires every command in 3.1-3.2 to have an Unattended-mode section naming `return-contract.yaml`). Stated wrong outcome: P1 cannot pass without either failing AC-1.1 or adding what lines 112 and 265 say not to add.

verdict: FAIL
