review: 1 of 3

# Spec-panel review, round 1: Orca worker contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none given (first review). Prior report: none.
- Reviewer model used: claude-sonnet-5-5
- Review panel: `superclaude review panel resolve` and `superclaude review merge` are not available in this sandbox; one reviewer ran, no merge ledger exists.
- Citation convention: `S:N` = line N of the candidate. `INV-A`, `INV-B`, `CAPS` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` in the workspace. Any citation to `src/`, `~/.claude/`, `CLAUDE.md`, `orca-data.json` or Orca binaries is UNVERIFIED: those files are not in the workspace. I checked only what the three inventories and the README say.

## What I covered

Whole document (S:1-285) against the requirements it states. Checked: section arithmetic (10 + 27 + 6 = 43, and 9 + 11 + 4 + 3 = 27 phase assignments), requirement-to-acceptance-check consistency (WC-1..WC-12, SA-1..SA-6, AC-C1..AC-4.3), per-command rows against the inventory lines they cite (INV-A:35, 60, 62, 90, 95-96, 106, 113, 118, 120; INV-B:31, 36, 107-112, 242, 272, 285-286, 292, 311, 320, 323; CAPS:44-45, 52, 58, 64, 66-68, 72-73, 76, 79-80, 97-98, 103, 107-116, 129-130, 145, 149, 151, 155-161, 178, 186-188). All of these were found as cited. The README rules (README:29-38) were applied. Not covered: the source-file line citations (`sk/`, `cmd/`), which I cannot read here.

## Panel (review order per command.md)

Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture and correctness); Crispin and Gregory (acceptance checks); Hightower (operations). Whittaker is active in every review.

## Blocking findings

### F1 (CRITICAL, High): the adversarial contract path contradicts the WC-4 path rule
- Expert: Wiegers (consistency), Whittaker (Divergence Attack).
- Grading sentence: an implementer who follows the stated text as written builds an `adversarial` that writes `<output>/adversarial/return-contract.yaml` (S:83) while the coordinator, following WC-4 (S:62), WC-5 (S:63) and live check step 3-4 (S:182-183), looks for `<output-dir>/return-contract.yaml` and passes that to `worker_done --report-path`; the path does not exist, so the coordinator opens nothing and step 4 (`test -s <contract>`) fails for a command that did what the spec said. Both texts are stated; no reading choice is needed.
- Evidence: S:62 fixes the file at `<output-dir>/return-contract.yaml`, "known before dispatch". S:83 (row adversarial, P1 fix) fixes it one directory deeper. S:198 (AC-1.4) accepts "one fixed path" without saying which. INV-A:60 shows the earlier workers wrote it at two different depths, which is the defect the P1 fix is meant to close; the fix as written reintroduces a third rule.
- Recommendation: make the adversarial row name `<output>/return-contract.yaml`, or carve an explicit exception in WC-4 and in the brief template (S:73) so the coordinator computes the same path.
- Quality impact: the only P0 smoke command whose contract path is then ambiguous is also the one PR #329 proved (INV-A:35).

### F2 (MAJOR, blocking, High): AC-1.1 cannot pass for `/sc:load`
- Expert: Crispin (testability), Wiegers.
- Grading sentence: an implementer who follows the stated text builds `/sc:load` with no contract and a usage-line fix only (S:112, "P1 (usage line only)"; S:265, "a report file would be an unrequested addition"), and AC-1.1 (S:195) then fails because it asserts every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`; making it pass requires the report file that S:265 forbids. The P1 scope row (S:159) also says the flag is "accepted by every command in sections 3.1 and 3.2".
- Evidence: S:112 (load row: Report "none", Resume "n/a"); S:265 (Decisions row for `/sc:load`); S:195 (AC-1.1); S:159. INV-B:31 agrees load "writes no file; use as a brief step, not a task".
- Recommendation: exempt `load` from AC-1.1 (and from the "accepted by every command" sentence), or drop the exemption in S:265. Narrowing is preferred.

## Follow-up candidates (Medium, never trigger a revision)

- M1 (Medium, Wiegers/Fowler): AC-C1 (S:172) scans `src/superclaude/core` and requires an empty result, but P0 adds an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `WORKER-CONTRACT.md`, both in `core` (S:158). Whether those texts contain a literal `orca orchestration ...` form is not stated, so the check may or may not pass. SA-2 (S:147) allows a mention "inside the contract file" without saying whether that is `WORKER-CONTRACT.md` or a runtime `return-contract.yaml`. Needs a guess, hence Medium.
- M2 (Medium, Nygard): WC-6 (S:64) says commands without a resume flag write "each run into a fresh output directory", but WC-4 fixes the contract at the directory passed in the brief. On a `--retry-of` worker the same brief directory is reused unless the coordinator changes it; S:73 does not tell the coordinator to pass a new directory per attempt. Both readings are allowed by the text.
- M3 (Medium, Whittaker, Sequence Attack): P1 makes `--unattended` accepted as a no-op on gated commands (S:159) while gate conversion arrives in P2 (S:160). In that window the coordinator brief (S:73) passes `--unattended` and WC-2 (S:60) promises no person-blocking step, but `/sc:task`, `/sc:cli-eval`, `/sc:cleanup` and others still prompt, which is the silent stall of S:44. The spec does not say the brief must not use `--unattended` on those commands before P2.
- M4 (Medium, Wiegers, missing requirement): `workflow` row (S:92) says write the contract "for pre-creation STOPs too", but the contract lives at `.dev/tasks/to-do/<id>/` (INV-B:272) and no package directory exists before creation (INV-B:272, ":39 not written for pre-creation STOPs"). The path for that case is unspecified, and the id is not known before dispatch (WC-4, S:62).
- M5 (Medium, Whittaker, Sentinel Collision): WC-4 fixes `status` at four values (S:62) and AC checks assert it (S:183), but "commands that already write a contract keep their fields". The existing status vocabularies of workflow, brainstorm, reflect and adversarial are not listed anywhere in the inventories (INV-B:272 names `status` only), so a clash with the four values is UNVERIFIED. `troubleshoot` writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242), which S:91 does not mention.
- M6 (Medium, Wiegers): S:154 says "Phases 1-3 need no user decision" while S:225 says "Phases 0-3 can proceed on the recommendations", and D4 (S:244) affects auggie-review and task, both P2 (S:160). D1 (S:227) is needed from P0. Two readings are possible.
- M7 (Medium, Nygard, Accumulation): `reflect` is rated ready (S:88) but by default writes a tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and moves the work-unit folder (INV-B:116, "(f)"). WC-9 (S:67) covers only push/PR/post/install/paid runs and WC-11 (S:69) covers same-file collisions only for single-owner memory keys; two reflect workers on one worktree are not addressed. The brief column only says `--no-promote` "when the coordinator owns folder moves".
- M8 (Medium, Adzic): E3 (S:23) is worded "It has worked before" and cited as evidence for the decision, while S:43 admits the prior run used the Agent-tool route (CAPS:156), not the direct route this spec requires. The section 1.4 caveat covers it; the E3 row itself overstates.
- M9 (Medium, Hohpe): WC-3 (S:61) lets a worker `ask` the coordinator for any blocked gate. For `/sc:implement` the Ruling must not come from another agent (S:233, citing `qa.md:232,238`, UNVERIFIED here). WC-3 has no carve-out; the implement row (S:109) and D2(a) cover it, but WC-3 stays generally permissive.

## Minor notes

- N1: S:11 and S:285 report citation checks (11 re-read, about 340 re-read by a validator). These counts are self-reports; INV-A:106 says about 290 and INV-B:320 about 270 for the inventories. Not checkable here.
- N2: S:33 R1 says which call sites enforce the depth check is "UNVERIFIED", matching CAPS:103; the wording is fine.
- N3: S:5 cites `README.md:11-17` for the evidence list; README:11-17 matches.
- N4: Hightower: nothing in the spec says where the `WORKER-CONTRACT.md` brief template lives for a coordinator in a non-IronClaude project; low impact.

## === REQUIREMENTS ANALYSIS ===

- Wiegers: requirements WC-1..WC-12 are stated, owned and evidenced; WC-2 (c) "blocked" is testable (AC-2.2, S:200). Defects: F1 (path), F2 (AC-1.1 vs load), M4, M5.
- Adzic: scenarios exist as live checks (S:178-186). Missing degenerate variant: a worker started with `--unattended` but no output directory (see Guard table GAP-1).
- Cockburn: primary actor is the coordinator; the person is the actor for D1-D5. Goal chain is clear (S:16, S:73). M6 is the stakeholder-timing defect.

## === ARCHITECTURE ANALYSIS ===

- Fowler: the decision (S:13-39) separates coordinator and command cleanly; the single shared contract file (S:52) keeps commands free of Orca text. Boundary leak: M1.
- Nygard: failure modes covered (blocked, partial, `consumer_fenced`, `ask` timeout). Gaps: M2 (retry), M7 (default writes), M3 (transition window).
- Whittaker attacks (all five methodologies applied):
  - Zero/Empty: `--unattended` with no output directory on a command that has none (analyze, build, design) before P1 adds one; WC-4 says the directory is "the directory the coordinator passed" and defines nothing when none is passed. Logged as GAP-1.
  - Divergence: adversarial path at the boundary between WC-4 and S:83 (F1).
  - Sentinel Collision: `status: blocked` is both a report value and, via WC-5, mapped to `--outcome failed`; a legitimate `failed` run and a `blocked` run both look the same to Orca, so only the contract file distinguishes them (spec says so at S:63; OK).
  - Sequence: P1 flag before P2 gate (M3); retry before fresh directory (M2).
  - Accumulation: three failed `worker-start` attempts trip the breaker (CAPS:80); the spec correctly notes a worker's own `failed` report does not.
- Newman/Hohpe: the contract is versionless. `contract 1.1` exists for workflow (INV-B:272) but WC-4 has no version field; adding one later is a compatibility change. Note only.

## Guard Condition Boundary Table

The guard condition boundary table is triggered (numeric thresholds and boolean guards exist). Rows are per guard; input classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` standalone token | S:51, S:12 | Zero/Empty (flag absent) | no flag | false | Today's behaviour (SA-1, S:146) | OK |
| `--unattended` + output dir | WC-4, S:62 | Zero/Empty (no dir passed) | `""` | undefined | Not stated for commands with no output flag | GAP (Medium; M-GAP-1, a missing requirement, not blocking) |
| `--unattended` + output dir | WC-4, S:62 | Typical | `--output .dev/x/` | true | Contract at `<dir>/return-contract.yaml` | OK |
| `--unattended` + output dir | WC-4, S:62 | Legitimate Edge Case (adversarial) | `<dir>/adversarial/` | conflicting | Two paths stated (S:62 vs S:83) | GAP (blocking, F1) |
| readiness limit 60 s | WC-1, S:59 | Typical | 30 s fallback | true | passes (EVIDENCE cited, S:59) | OK |
| readiness limit 60 s | WC-1, S:59 | Maximum/Overflow | above about 45 s | false | fails again (S:59) | OK |
| wait split 4 min vs heartbeat 5 min | WC-10, S:68 | Typical | 4 min wait | true | heartbeat between waits | OK |
| wait split | WC-10, S:68 | Legitimate Edge Case | 4 min 59 s of tool plus overhead | unspecified | 4 min margin chosen (S:266) | OK |
| confidence < 0.70 | task row, S:121 | Sentinel Value Match | exactly 0.70 | unspecified in spec | Inventory states threshold; spec says "below 0.70" | OK (boundary is the command's, INV-B:292) |
| nesting depth 1 | R1, S:33 | Typical | worker calls `worker-start` | refused | `nested_worker_depth_exceeded` | OK |
| nesting depth 1 | R1, S:33 | Legitimate Edge Case | worker calls `task-create` | unknown | UNVERIFIED, WC-8 forbids (S:66) | OK |
| `consumer_fenced` | WC-12, S:70 | Typical | returned | true | stop, no `worker_done` | OK |
| status vocabulary | WC-4, S:62 | One/Minimal | status outside the four | unspecified | existing contracts "keep their fields" | GAP (Medium, M5) |
| pre-creation STOP | workflow row, S:92 | Zero/Empty (no package dir) | no `<id>` | unspecified | no path stated | GAP (Medium, M4) |

Classes left out: Maximum/Overflow for the `--unattended` flag (a boolean has no overflow); One/Minimal for the readiness limit (not a count). FR-8/FR-9 grading: the two GAP rows without a concrete wrong outcome are Medium; the F1 row is blocking.

## Quantity Flow Diagram

```text
[Inventories: 21 (A) + 22 (B) = 43 commands (S:76)] --> [Classification]
    |-- ready today: 10      (S:78-92)
    |-- needs change: 27     (S:94-125)   per phase: P1 9, P2 11, P3 4, P4 3 = 27
    |-- coordinator-only: 6  (S:127-137)
[Ready 10 + P2 gate fixes for 4 of them (reflect, release-split, tdd, troubleshoot)] --> [P2 total 15]
[P0 smoke runs: 3 of the 10 ready commands (S:158)]
Total conserved: 10 + 27 + 6 = 43. No mismatch.
```

## Reviser brief

Revise only the blocking findings F1 and F2 in `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone and do not apply them. Return the file once and do not award yourself a PASS. End with the fix map (`fixmap-v1`).

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", "anchor2": "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed", "refs": ["WC-4", "WC-5", "AC-1.4", "section 3.1"], "claim": "The adversarial row puts the contract one directory below the path WC-4 tells the coordinator to read, so the report path handed to worker_done does not exist."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`", "anchor2": "a report file would be an unrequested addition", "refs": ["AC-1.1", "section 3.2 load row", "Decisions"], "claim": "AC-1.1 requires /sc:load to name a return-contract.yaml that the spec says load must not write, so the P1 check cannot pass as written."}
{"id": "M1", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "prints nothing (SA-2, WC-8)", "refs": ["AC-C1", "SA-2", "P0"], "claim": "The grep over core may fail on the Orca text P0 adds to core files, depending on a wording the spec does not fix."}
{"id": "M2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "refs": ["WC-6", "WC-4"], "claim": "A retry may reuse the brief's output directory and overwrite the first attempt's contract."}
{"id": "M3", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["WC-2", "P1", "P2"], "claim": "Between P1 and P2 a gated command accepts --unattended yet still prompts, stalling the worker."}
{"id": "M4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1)", "refs": ["workflow row", "WC-4"], "claim": "No path exists for a contract written before the package directory is created."}
{"id": "M5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "refs": ["WC-4"], "claim": "Existing contracts keep their fields, so their status values may not be in the four-value set the checks assert."}
{"id": "M6", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.", "refs": ["section 6", "section 9", "D1", "D4"], "claim": "Phase gating by user decision is stated two ways and D1 and D4 touch earlier phases."}
{"id": "M7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "no `--remediate`; `--no-promote` when the coordinator owns folder moves", "refs": ["reflect row", "WC-9", "WC-11"], "claim": "Reflect's default tracked-file write and folder move are not covered by any unattended rule."}
```

verdict: FAIL
