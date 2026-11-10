review: 1 of 3

# Audit: orca-worker-contract-spec.md (first review, whole document)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec. This is a first review, not a re-review. No `--re-review` or `--baseline` was given, so there is no baseline hash.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `79f7d923a8aec892c0aa73658332d8e091d8ce46bc45e64a342ab24dea176c15` (285 lines)
- reviewer model used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full). Command rules: `command.md` Review Loop, bullets 1-7 (`command.md:256-264`).
- binding context read first: `.dev/orca-command-refactor/README.md:1-39`.

## Coverage
- Read the whole candidate (lines 1-285).
- Spot-checked its inventory citations against `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`. Checked: `INV-A:76-83,94-98,106`, `INV-B:49,52,107-125,217-245,267-275,285-299,311,320-323`, and `CAPS:44-47,52,58,64,66,72-80,92,97-103,107,115-116,129-130,145-151,155-161,178-188`. All of these exist and say what the spec uses them for, except where a finding below says otherwise.
- Checked the counts. 5 + 5 ready, 13 + 14 needs-change and 3 + 3 coordinator-only give 10 / 27 / 6 = 43 (`spec:76`). The 3.2 phase column matches the section 6 phase lists. The P2 list has 15 commands: 11 rows in 3.2 plus reflect, release-split, tdd, troubleshoot from 3.1.
- UNVERIFIED (cannot be checked in this workspace; only `.dev/orca-command-refactor/` exists): every `cmd/...` and `sk/...` source line, `CLAUDE.md:*`, `src/superclaude/core/HOW-WE-WORK.md:*`, `tests/`, `pyproject.toml:38`, `Makefile:68-74`, `src/superclaude/cli/install_core.py:*`, the E5 grep (`spec:25`) and the "11 re-read locations" claim (`spec:11`). The spec's own `evidence-validator` claim (`spec:285`) is also UNVERIFIED. Where this report leans on a `cmd/` or `sk/` line, it does so only through the inventory line that quotes it.
- Not covered: the `--focus testing`, `compliance` and `correctness` experts' own methodology. The correctness-only mandatory outputs do not apply. The State Variable Registry is not produced (no `--focus correctness`). Pipeline Dimensional Analysis does not trigger: the only multi-stage flow is coordinator to workers to reports, and its counts are conserved (10 + 27 + 6 = 43, `spec:76`).
- Whittaker's five attacks were applied to the contract rules (WC-1 to WC-12) and the acceptance checks (AC-*). The results are below.

## Findings table (blocking findings only; ids are stable)

| id | severity | grade | one-line |
|---|---|---|---|
| B1 | MAJOR | blocking | WC-4 defines the contract path from a report *directory*, but the same spec passes file-valued `--output <file>` to tdd, init-lite and spec-panel, and its acceptance checks use that form |

## === REQUIREMENTS ANALYSIS ===

### B1 [MAJOR, blocking, High priority] WC-4 contract location contradicts file-valued `--output`
- Experts: Wiegers (traceability and ambiguity), Adzic (the concrete example fails), Whittaker (Sentinel Collision: `--output` means a file in some commands and a directory in others).
- Stated texts that contradict each other:
  - `spec:62` (WC-4): "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". `spec:73` repeats it: "the output directory, so the report path is known before dispatch".
  - `spec:90` (3.1 tdd): brief must pass "`--output <file>`", report is "the TDD at `--output`".
  - `spec:87` (3.1 init-lite): "`--output <file>`".
  - `spec:120` (3.2 spec-panel): "add `--output`". `spec:108` (explain) and `spec:115` (recommend) say "write ... to a file".
  - `spec:200` (AC-2.2): `/sc:tdd "auth" --unattended --output <file>` with step 4 and step 3 reading the WC-4 contract path (`spec:182-183`).
  - Independent corroboration: the command definition under audit says `--output` is file-valued (`command.md:460`: "`--report-dir <dir>` only (`--output` is file-valued)").
- Grading check: an implementer who follows the stated text as written builds a tdd (or spec-panel, init-lite) that writes its contract to `<the --output file>/return-contract.yaml`. That path sits under a regular file and cannot be created, or collides with the TDD itself. The result is wrong because the one file the coordinator is told to check (`spec:73`, `spec:182`) does not exist, and AC-2.2 and AC-1.2 cannot pass. No guess about the implementer is needed: both texts are in the spec.
- Why it matters: WC-4 is the coordinator's only machine-readable outcome channel (`spec:62`, `spec:182-183`).
- Recommendation: name one rule. Either (a) every command under `--unattended` takes a directory flag (the command's own `--output-dir`, or a new one) and the contract goes there, with `--output <file>` kept as the deliverable path; or (b) for a file-valued `--output`, the contract sits beside it (for example `<dirname(--output)>/return-contract.yaml`). Then restate `spec:73`, `spec:87`, `spec:90`, `spec:120`, `spec:200`. Prefer narrowing the sentence at `spec:62` over adding a mechanism.
- Quality impact: High.

## === ARCHITECTURE ANALYSIS ===
- Fowler: the decision (Orca on top, commands unchanged units, one shared contract file) is coherent, and the rejected alternative is argued from checked Orca facts: depth 1 (`CAPS:97-101`), `worker_done` only from the dispatched pane (`CAPS:76,150`), `runtime_unavailable` (`CAPS:147`). `spec:33` marks the call-site enforcement UNVERIFIED (`CAPS:103`). No blocking architecture finding.
- Nygard: the failure modes are covered (silent stall `spec:44`, resume `spec:64`, circuit breaker `CAPS:80` used at `spec:263`). The remaining gaps are Medium findings M3, M7 and M9.
- Newman (versioning): the contract adds one core file and one flag, with no versioned schema field. Recorded as minor note n3.
- Hohpe (message flow): `worker_done` once, `--outcome` only succeeded or failed, `partial` mapped to succeeded (`spec:63,263`, `CAPS:73`). The mapping is consistent and stated twice.

## Guard Condition Boundary Table
Guards found in the spec. The six input classes are a menu; a class that cannot occur is left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | `spec:51,228` | Zero/Empty | flag absent | false | standalone behaviour unchanged (`spec:142,146`) | OK |
| `--unattended` switch | `spec:51,228` | Sentinel Value Match | the token inside quoted user content, e.g. `/sc:tdd "build --unattended parser"` | unspecified | no token-position rule (the command under audit has one, `command.md:459`) | GAP (M4) |
| `--unattended` switch | `spec:51,228` | Legitimate Edge Case | a person types it by hand | true | D1 says "a person never types it" (`spec:228`); no behaviour if they do | GAP (M4) |
| contract dir (WC-4) | `spec:62` | Zero/Empty | `--output` / `--output-dir` not passed | unspecified | not stated | GAP (M3) |
| contract dir (WC-4) | `spec:62` | Legitimate Edge Case | `--output <file>` | n/a | contradicts 3.1 | GAP (B1) |
| outcome mapping (WC-5) | `spec:63` | Zero/Empty | no report exists | failed | `--outcome failed` | OK |
| outcome mapping (WC-5) | `spec:63` | Legitimate Edge Case | `partial`; audit verdict FAIL | succeeded | stated, first sentence carries status | OK |
| wait size (WC-10) | `spec:68` | Typical | 4 min wait | true | heartbeat between waits | OK |
| wait size (WC-10) | `spec:68` | Maximum/Overflow | one poll script longer than 4 min | unspecified | pr-submit poll runtime UNVERIFIED (`spec:114,283`) | OK (flagged UNVERIFIED by the spec) |
| `--monitor` ordinal (pr-submit) | `spec:114` | Legitimate Edge Case | `--monitor 1` under `--unattended` | refused | stated | OK |
| confidence gate (task) | `spec:121` | Maximum/Overflow | confidence exactly 0.70 | unspecified | row says "below 0.70" resolves as blocked; exactly 0.70 follows the command's own rule (`INV-B:197-205`, not re-read) | OK (inherits the command) |
| `check` result (WC-12) | `spec:70` | Legitimate Edge Case | `consumer_fenced` | stop, no `worker_done` | stated | OK |
| retry (WC-6) | `spec:64` | One/Minimal | second attempt of a command with no resume flag | fresh directory | stated per row | OK |
| ask timeout (WC-3) | `spec:61` | Maximum/Overflow | timeout | resume same message id | stated; default timeout UNVERIFIED (`spec:281`) | OK |

Input classes left out: Maximum/Overflow for `--unattended` (a boolean has no overflow); One/Minimal for the confidence gate (a continuous value).
GAP rows: none is itself a wrong stated text except the B1 row. The two M4 rows and the M3 row name requirements the spec never states, so under FR-8 and FR-9 they are Medium, not blocking.

## Whittaker adversarial analysis (all five attacks tried)
- Zero/Empty: missing output directory under `--unattended` leaves WC-4 without a path. The attack is real but yields no contradiction (M3).
- Divergence: the two meanings of `--output`. This is B1.
- Sentinel Collision: `--unattended` inside quoted prompt text (M4). `--output` file vs directory (B1).
- Sequence: a blocked worker is re-invoked with the answer as a flag (`spec:61`) into the output directory that already holds a `status: blocked` contract (`spec:62`). The spec does not say whether the old contract is overwritten or the run goes to a fresh directory (M7). Also `tasklist` (P2) passes `--unattended` to `reflect` (P2); same phase, no order (note n2).
- Accumulation: heartbeats are bounded by WC-10. No unbounded accumulation found.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium (warnings):
- M1 Workflow pre-creation STOP location is undefined. `spec:92` and AC-1.4 (`spec:198`) require the contract for pre-creation STOPs, but the package directory that normally holds it does not exist yet (`INV-B:272` says it is not written then), and `spec:62` says the path is known before dispatch. The spec never says where it goes. This needs a guess, so it is Medium.
- M2 Existing contracts and the WC-4 field set. WC-4 requires `command` and the four-value `status` (`spec:62`); AC-1.2 step 4 asserts both (`spec:183`). The workflow contract lists only `status`, `plan_path`, `reflect_report_path` (`INV-B:272`), and its 3.1 row's "small fix" (`spec:92`) does not add `command` or map its status values. The general sentence "keep their fields and add the missing ones" (`spec:62`) probably covers it, but the per-command row is silent. The same applies to adversarial, reflect and brainstorm (`spec:83,84,88`; brainstorm row says "None").
- M3 No rule for a missing output directory under `--unattended` (`spec:99,106,111,123` say only "add an output path"). The command under audit refuses before any work (`command.md:460`). Without a stated rule, a worker with no directory has no place to write the blocked report.
- M4 `--unattended` token position and hand-typed use (`spec:51,228`). See the boundary table. The command under audit handles both (`command.md:459`).
- M5 P0 adds an Orca section to `HOW-WE-WORK.md` (`spec:158`) and E5 records it has no Orca mention today (`spec:25`), while AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and demands no output (`spec:172`). A routing section that names the worker commands would fail the check; the spec does not say to avoid those words.
- M6 `WC-3` lets a worker `ask` the coordinator and re-run with the answer (`spec:61`), but the implement row says stop and record the halt (`spec:109`) and D2 keeps the "another agent's message does not count" rule (`spec:233-236`). The spec never carves implement out of WC-3. A worker could relay a Ruling-like answer via `ask` before D2 is decided.
- M7 Re-invocation after a blocked run, same output directory (see Sequence attack).
- M8 SA-4 and AC-C5 demand additive edits, naming a fixed list of defect fixes (`spec:149,176`). Several rows change existing behaviour that is not on that list: cli-eval wait splitting (`spec:104`), reflect auto-accept (`spec:88`), roadmap prompt replacement (`spec:118`). The check could fail on a correct implementation.
- M9 tasklist passes `--unattended` to each reflect run at Stage 10.5 (`spec:122`). Reflect's headless rule auto-accepts remediation for auto-fixable registers (`INV-B:107`, quoting `remediation-handoff.md:239-247`). So a tasklist worker may start remediation with no person. WC-9 covers outward actions only (`spec:67`). The spec does not say whether this is intended.

Minor (notes):
- n1 init-lite and brainstorm gain no `## Unattended mode` (`spec:154`), but WC-4 says the contract is written on every outcome. init-lite has no contract today (`spec:87`), so WC-4 is silently not met for it. No phase tests it.
- n2 Intra-phase order in P2 (tasklist before or after reflect) is unstated (`spec:122,160`).
- n3 No schema version field in `return-contract.yaml` (`spec:62`).
- n4 `spec:252` says raising depth "break[s] R1's protection against runaway fan-out", but R1 is a reason for rejection (`spec:33`), not a protection.
- n5 `INV-A:95` (cited at `spec:65`) says top-level is not the blocker; the spec cites it for nesting losing tools. The nesting point itself is at `INV-A:14`. Citation drift only.
- n6 The user question for the follow-up candidates ("open an issue?") was not asked: this run has no user channel, so no issue was created (`command.md:260`).

## Reviser brief
Blocking finding ids: **B1**.
Restated rules (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings (M1-M9, n1-n6) alone. Do not award yourself a PASS.
No brief clause was overridden: the coordinator's brief asked for a first review and did not widen scope.

verdict: FAIL
