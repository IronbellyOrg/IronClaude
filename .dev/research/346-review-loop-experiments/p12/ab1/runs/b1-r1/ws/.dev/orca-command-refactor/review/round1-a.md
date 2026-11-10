review: 1 of 3

# Spec panel report, critique mode: Orca worker contract spec

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited below as `spec:N`)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: n/a (first review; `baseline: missing` not applicable, no `--re-review`/`--baseline` given)
- reviewer model actually used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; format: standard markdown
- reviewer role: one first-review reviewer, fresh context, no other review seen. Per the FIRST-REVIEW prompt the coordinator briefs three such reviewers and merges; this file is one of the three reports and is not the merged report. Its ids are B1, B2; the coordinator renumbers them M1... in the merge.
- evidence rules: the only checkable evidence in the sandbox is README.md and `inventory/commands-a.md` (`INV-A`), `commands-b.md` (`INV-B`), `orca-capabilities.md` (`CAPS`). Any citation into `src/`, `.dev/` outside this folder, `CLAUDE.md`, `EVIDENCE.md` or Orca's own files could not be opened and is UNVERIFIED (list at the end).

## Coverage

Read in full: the candidate (285 lines), README, the three inventories, the command definition, the review-loop prompts. Checked: every `INV-A:n`, `INV-B:n`, `CAPS:n` citation in sections 1 to 4 of the candidate against the inventory line (all resolved to the claimed content, no wrong line found); the 10 / 27 / 6 split (counted below); phase assignment of every command; internal consistency between section 2 (contract), section 3 (per-command), section 6 (phases), section 7 (acceptance) and section 9 (decisions). Not checked: any claim whose only evidence is a file outside the sandbox.

## Verification of the arithmetic (Pipeline Dimensional Analysis, Quantity Flow Diagram)

The spec describes a multi-stage flow whose counts change (43 commands, split three ways, then spread over phases), so the heuristic applies.

```text
[Source: 43 commands: 21 INV-A:3 + 22 INV-B:3]
   --> [Split, spec:76] --> 10 ready (spec:81-92, 10 rows counted)
                        --> 27 needs-change (spec:97-125, 27 rows counted)
                        -->  6 coordinator-only (spec:131-137, 6 rows counted)   10+27+6 = 43  OK
[Phase ownership, spec:156-162]
   P1 lists 9 (3.2 commands) + 4 (3.1 small fixes) = 13 commands
   P2 lists 15, P3 lists 4, P4 lists 3                                          13+15+4+3 = 35
   brainstorm, init-lite appear in no phase (3.1 "Small fix: None")             35+2 = 37 = 10+27
[Consumer: P1 scope text spec:159 says the --unattended flag is accepted by "every command in sections 3.1 and 3.2" = 37]  <-- MISMATCH (13 listed vs 37 stated)
[Consumer: AC-1.1 spec:195 asserts the Unattended-mode section on "every command in sections 3.1-3.2" = 37]                <-- MISMATCH
```

The mismatch is part of finding B2.

## === REQUIREMENTS ANALYSIS ===

### B1. CRITICAL (blocking). WC-4 fixes one contract location that the spec's own per-command rows contradict
- Experts: Wiegers (traceability of a requirement to its rows), Adzic (the acceptance step cannot be exampled), Whittaker (divergence attack).
- Quoted texts:
  - `spec:62`, WC-4: "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)."
  - `spec:83`, adversarial row: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)".
  - `spec:87` and `spec:90`, init-lite and tdd rows: brief passes `--output <file>`, report is "the TDD at `--output`" / "`.dev/superclaude/context-audit.md` or `--output`".
  - `spec:92`, workflow row: report is "`.dev/tasks/to-do/<id>/return-contract.yaml`" (the id is generated at run time).
  - `spec:73`: the brief states "the output directory, so the report path is known before dispatch (WC-4)".
  - `spec:182`, live check step 3: pass requires "its report path is the WC-4 contract path".
- Wrong outcome: An implementer who follows the stated text as written builds three incompatible things. For adversarial, WC-4 gives `<output>/return-contract.yaml` while the row gives `<output>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist. For tdd and init-lite, `--output` is a file, so `<output-dir>` has no value and the implementer must invent where the contract goes. For workflow, the path contains an id that cannot be known before dispatch, which contradicts `spec:73`, and the pre-creation STOP case (`spec:92`, "Write the contract for pre-creation STOPs too") has no id and therefore no stated location at all. The build is wrong because acceptance step 3 (`spec:182`) compares the worker's `--report-path` with a path that the spec defines in two incompatible ways, so it cannot pass for at least adversarial and workflow.
- Recommendation: state one rule for the contract location that every row can satisfy (for example a coordinator-supplied `--report-dir` that is always a directory, separate from file-valued `--output`), or list the exact contract path per row in section 3 and have WC-4 refer to it. Do not add a new mechanism beyond that.
- Priority: High. Quality impact: removes the only checkable link between a worker and the coordinator that reads its result.

### B2. CRITICAL (blocking). Phase 1 and its acceptance check demand work that other parts of the spec say must not happen
- Experts: Wiegers (consistency), Cockburn (who acts when), Fowler (phase boundaries).
- Quoted texts:
  - `spec:195`, AC-1.1: the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `spec:159`, P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - Against it, `spec:112`, load row: report "none (see note)"; "use it as a step inside another worker's brief, not as its own Task". And `spec:265`: "a report file would be an unrequested addition."
  - Against it, `spec:240`, D3 recommended option (a): "no pr-submit changes in Phase 4", with `spec:154`: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4", and `spec:162` placing implement, post-release and pr-submit in P4.
  - Against it, `spec:159` itself lists only 13 commands in the P1 Commands column, while reflect, release-split, tdd, troubleshoot are scheduled in P2 (`spec:160`) and brainstorm, init-lite in no phase (see the Quantity Flow above).
- Wrong outcome: An implementer who follows AC-1.1 as written must give `load` an Unattended-mode section naming `return-contract.yaml`, which the load row and decision at `spec:265` say must not exist; and must edit pr-submit, implement and post-release in Phase 1 before the user answers D2 to D4, which `spec:154` and `spec:240` forbid. An implementer who follows the load row and the D3 recommendation builds a Phase 1 that fails its own acceptance check, so the phase gate in `spec:154` ("Later phases do not start until the earlier phase's checks in section 7 pass") blocks every later phase. The two texts cannot both hold.
- Recommendation: restrict AC-1.1 and the P1 flag sentence to the commands the P1 row lists, exempt load, and state which phase adds the section for each remaining command; delete the sentence that gives P4 commands a P1 section, or make it conditional on the D2 to D4 answers.
- Priority: High. Quality impact: the rollout cannot be completed in the stated order.

## === ARCHITECTURE ANALYSIS ===

The core decision (Orca on top, commands remain units of work, no Orca calls inside commands, `spec:16`, `spec:29-39`) is internally consistent and follows the evidence it cites: depth 1 and the refusal code (`CAPS:97-101`), `runtime_unavailable` and the `--from` rule (`CAPS:147-149`), `worker_done` bound to the dispatched pane (`CAPS:76`, `CAPS:150`). The evidence-strength section (`spec:41-45`) is candid, and the P0 smoke test (`spec:158`) tests the decision before building on it. No blocking architecture finding beyond B1 and B2. Fowler and Newman on interface versioning: the contract is versioned only by convention (`status`, `command`, `report_path`); see follow-up F8.

## === GUARD CONDITION BOUNDARY TABLE (Nygard lead, Crispin completeness, Whittaker attack) ===

Guards identified: the 4-minute wait split (WC-10), the outcome mapping (WC-5), the readiness limit (WC-1), the confidence threshold carried for task (`spec:121`), the nested depth limit. Classes left out are named with a reason. Every row is graded: a GAP is blocking only if it names a concrete wrong outcome; none below does, so each GAP is Medium.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | spec:68 | Typical | single call 600 s | split required | split into waits of at most 4 min | OK |
| WC-10 wait split | spec:68 | Legitimate Edge Case | single call 270 s (between 4 and 5 min) | WC-10 does not fire (rule says "longer than 5 minutes") | AC-4.3 `spec:210` says no call may exceed 240 s, so the two texts disagree on this band | GAP (F3) |
| WC-10 wait split | spec:68 | Maximum/Overflow | cli-eval 3600 s timeout | split required | stated for cli-eval at `spec:104` | OK |
| WC-5 outcome | spec:63 | Zero/Empty | contract file exists but is empty or not parseable | "no report exists" is the only stated trigger | not specified for an existing but unreadable file | GAP (F4) |
| WC-5 outcome | spec:63 | Sentinel Value Match | `status` is a value outside the four allowed | only `failed`/`blocked`/other are mapped; "otherwise" maps to succeeded | an unknown value maps to `succeeded` by the word "otherwise" | GAP (F4) |
| WC-5 outcome | spec:63 | Legitimate Edge Case | `partial`; audit verdict FAIL | succeeded | stated | OK |
| WC-1 readiness | spec:59 | Maximum/Overflow | fallback of 45 s or more | readiness fails | stated by the evidence (`EVIDENCE.md:45,56` via `CAPS:49`) | OK |
| WC-1 readiness | spec:59 | Typical | fallback 30 s | passes | stated | OK |
| task confidence guard | spec:121 | Legitimate Edge Case | confidence exactly 0.70 | prompt does not fire (only "below 0.70") | consistent with INV-B:45 | OK |
| nested depth | spec:33 | Maximum/Overflow | user raises depth (D5 option b) | R1 no longer excludes the alternative | stated at `spec:252` | OK |

Left out, with reason: Zero/Empty and One/Minimal for WC-10 (a zero-length wait is not a wait); One/Minimal and Typical for WC-5 beyond the rows shown (they follow the Typical rows); Sentinel for WC-1 (no sentinel value).

Completion check (FR-8, FR-9, FR-10): table complete; the three GAPs name no concrete wrong outcome an implementer would produce without a guess, so they are Medium, not blocking.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Divergence Attack**. The invariant at **WC-3 and AC-2.2 (`spec:61`, `spec:200`)** fails when **a gate resolves as blocked and the worker holds a preamble**. Concrete attack: tdd is dispatched with a bare topic. Before: no contract. WC-3 says the session "may instead ask the coordinator once", so it calls `ask` and waits. AC-2.2 requires `worker_done --outcome failed` with `status: blocked`. After: the worker is parked in `ask` (a healthy wait, `CAPS:52`) and the acceptance check times out. Severity MAJOR; graded Medium (the implementer must guess between two readings the text allows). See F1.
- I can break this specification by **Sequence Attack**. The invariant at **WC-2(c) with WC-5 (`spec:60`, `spec:63`)** fails when **a blocked worker needs its answer**. Concrete attack: a worker ends `failed` with `status: blocked`. Orca marks the Task failed and keeps dependents blocked (`CAPS:90`). The spec gives no step by which the coordinator supplies the answer and re-runs (only `--retry-of` is mentioned, `spec:64`, `CAPS:116`). Severity MAJOR; Medium because the missing step is a requirement the document never states. See F2.
- I can break this specification by **Accumulation Attack**. The invariant at **WC-11 (`spec:69`)** fails when **two workers run index-repo or cleanup-audit in one worktree**. The rows give fixed output locations (`PROJECT_INDEX.md`, `.claude-audit/`, `spec:85-86`); cleanup-audit says "one audit per worktree at a time" but index-repo is silent. Severity MINOR. See F6.
- Zero/Empty and Sentinel attacks on WC-5: see the table (F4).

## Quality scores (0 to 10)

Clarity 7, Completeness 6, Testability 6, Consistency 5 (B1, B2). Overall 6.

## Follow-up candidates (Medium and minor; they never fail this review and are not in the Reviser brief)

Medium:
- F1. WC-3 allows an `ask` where AC-2.2 expects `failed` (`spec:61` vs `spec:200`); say which wins when a preamble exists, or exempt the AC-2.2 run from asking.
- F2. No procedure for answering a blocked worker and re-running it (`spec:60`, `spec:63`, `CAPS:90`).
- F3. WC-10 says calls over 5 minutes must be split to 4 minutes; AC-4.3 says no call over 240 s (`spec:68` vs `spec:210`).
- F4. WC-5 does not cover an empty or unparseable contract, or a `status` outside the four values (`spec:63`).
- F5. P0 acceptance AC-0.4 (`spec:194`) says step 4 uses the existing report file, but step 4 (`spec:183`) parses YAML and asserts `status` and `command`, which troubleshoot's REPORT.md and the existing adversarial/workflow contracts do not carry (workflow's fields: `INV-B:272`); step 3 also compares against a WC-4 contract that does not exist until P1.
- F6. WC-11 has no stated check for index-repo and cleanup-audit fixed output locations (`spec:85-86`); only save has one (AC-3.4, `spec:207`).
- F7. AC-C1 (`spec:172`) scans `src/superclaude/core` and prints must be nothing, while P0 adds an Orca section to HOW-WE-WORK.md and a contract file in that directory (`spec:158`), and SA-2 allows an Orca mention inside the contract file (`spec:147`); the grep has no exclusion for the new file. The pattern is lowercase, so an uppercase `ORCA` example would pass; the outcome depends on the implementer's wording.
- F8. WC-1, WC-6 and WC-12 have no acceptance check in section 7 (`spec:59`, `spec:64`, `spec:70`); WC-6 (resume or fresh directory) is the largest.
- F9. SA-3 (`spec:148`) says contract files are written "only in unattended mode or when the caller passes the new output flag", while WC-4 (`spec:62`) writes the contract "in unattended mode"; whether an `--output` run without `--unattended` writes a contract is open.
- F10. tasklist row (`spec:122`) passes `--unattended` to each reflect so the headless auto-accept rule applies; INV-B:215 recommended dropping `--remediate` in Stage 10.5 instead. Auto-accepting remediation under unattended runs is a new behavior chosen without a stated reason; also the reflect row (`spec:88`) tells the brief to omit `--remediate`.
- F11. AC-3.2 (`spec:205`) starts fresh in a directory that already holds a session; WC-6 (`spec:64`) says a retry must not corrupt the first attempt's output.
- F12. pr-submit: WC-10 and the row (`spec:68`, `spec:114`) reinterpret the 600 s budget as cumulative over iterations, citing `cmd/pr-submit.md:49` and `SKILL.md:46-64` (UNVERIFIED); INV-B:95 reads it as a per-wait budget needing heartbeats. The spec marks poll runtime UNVERIFIED (`spec:283`) but still concludes "can already heartbeat" (`spec:114`).
- F13. The count of coordinator-only commands is 6 in `spec:76` and `spec:128`, but under D3 option (a) pr-submit also stays with the coordinator (`spec:139`, `spec:240`); the counts are stated as fixed.

Minor (notes):
- N1. Contract-flag names differ across rows: `--output`, `--output-dir`, `--pass`, `--report` (`spec:62`, `spec:100`, `spec:85`, `spec:125`); the panel notes the command being used for this review already resolves a separate `--report-dir`, which suggests the surface should be unified (observation from `command.md`, not from the inventories).
- N2. `spec:11` and `spec:285` report counts of citations re-checked (11 and about 340) that cannot be verified from the sandbox.
- N3. 7.2 step 5 searches the transcript for the text `AskUserQuestion`; a transcript that loads a command file containing that word could match, so say "a tool call named".
- N4. `spec:25` (E5) states results of `grep` runs on `src/` that cannot be re-run here.

Per the loop rule the session that ran this review asks the user once whether to open an issue for the follow-up candidates and creates none without an answer; this reviewer could not ask and creates none (the coordinator asks).

## UNVERIFIED citations (could not be opened in the sandbox)

`CLAUDE.md:*` (`spec:34`, `spec:52`, `spec:147`, `spec:150`, `spec:175`, `spec:239`); all `cmd/`, `sk/`, `ag/` and `src/superclaude/cli/install_core.py` lines quoted directly in `spec:11`, `spec:52`, `spec:65`, `spec:68`, `spec:83-125`, `spec:132-137`; `.dev/codegraph-migration/orchestration/README.md:31,33,42` and the `return-contract.yaml:10` path (`spec:23`, `spec:174`); `EVIDENCE.md:39,45,56` (seen only as quoted at `CAPS:49`); `HOW-WE-WORK.md:22,171,249,254` (`spec:146`, `spec:164`); `pyproject.toml:38` (`spec:183`); `Makefile:68-74`. Orca guide lines were checked only through the `CAPS` quotations, not against Orca itself.

## Reviser brief

Blocking finding ids: B1, B2.

Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing text to adding it. Report the byte size of the specification before and after, and the bytes added and deleted per finding id. Leave every Medium and minor finding above alone, and do not award yourself a PASS.

- B1: `spec:62` (WC-4) against `spec:83`, `spec:87`, `spec:90`, `spec:92`, `spec:73`, `spec:182`. Make the contract location one rule that every row in 3.1 and 3.2 satisfies, or name the exact path per row.
- B2: `spec:195` (AC-1.1) and `spec:159` against `spec:112`, `spec:265`, `spec:240`, `spec:154`, `spec:160`, `spec:162`. Make the Phase 1 scope and AC-1.1 name the same command set, exempt load, and keep P4-gated commands out of Phase 1.

verdict: FAIL
