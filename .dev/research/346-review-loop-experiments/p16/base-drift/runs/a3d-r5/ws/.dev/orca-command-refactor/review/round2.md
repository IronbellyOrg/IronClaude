review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` (RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full)
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `fb9100899806def3c0456f91fd02f9793207fcb28f4789f5ae6d358a15a2ce5f`
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in round1.md:7, so the baseline is the text round 1 reviewed)
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `78eb2c23a6a209e66789d3853be7ef0c869a29427ed3d9ed448033b1d3526247`; its header is `review: 1 of 3` (round1.md:1), so N = 2
- reviewer model actually used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; `--iterations` ignored; Improve step skipped; no revised specification written; `--unattended` not passed
- `rf-qa.md` (Fix Cycle steps 1-5) is not in the sandbox (no `~/.claude/agents/` and no project `.claude/agents/`); the re-check below follows the rules of the command's Review Loop section, which stand alone. Brief clauses overridden: none.
- Line numbers below are lines of the candidate unless prefixed `base:` (baseline) or `r1:` (round1.md).

## Step 1: evidence block

Roles fixed by the command line: CANDIDATE = the `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`. Command run: `diff -w BASELINE CANDIDATE`. Four lines changed (62, 105, 159, 195). Every line below is copied verbatim from the diff.

BEFORE (baseline)

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate)

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`), or the parent directory of a file-valued `--output` (F-1); a command whose section 3 row names another contract location uses that location, and the brief names it (F-1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields; it counts as approval of the gate the contract names as blocked, so the resumed run passes that gate and stops only at the next one (F-3) | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except the P4 commands, which get theirs in P4 (F-2) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` and the P4 commands (implement, post-release, pr-submit; these get theirs in P4) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (F-2), and that no section-4 command has one | passes |
```

Self-check (run): each of the 4 BEFORE lines was found by `grep -cFx` in the baseline and not in the candidate; each of the 4 AFTER lines was found in the candidate and not in the baseline. No role swap. Sizes: baseline 57763 bytes, candidate 58227 bytes (+464), matching `revise1.md:7`.

## Coverage (what was and was not checked)

- Read in full: the candidate (285 lines), the baseline diff, `README.md`, `review/round1.md`, `review/revise1.md`, the command definition and the review-loop prompts file.
- Inventory lines read for the changed text: `inventory/commands-a.md` lines 45, 68, 79, 82, 96-97, 115-116 (cli-portify evidence).
- Checked against the candidate: every line that depends on a changed line (WC-4 at 62 with 73, 76, 83-92, 120, 182-183; cli-portify row 105 with AC-2.2/2.3 at 200-201; P1 row 159 with 109, 113, 114, 162, 164; AC-1.1 at 195 with 112, 149, 265, 160, 240).
- UNVERIFIED (not reachable in this sandbox, which holds only README, the spec, round files and `inventory/`): every `cmd/...`, `sk/...`, `src/...`, `CLAUDE.md:N`, `EVIDENCE.md:N` and `CAPS` source line behind the inventories. No finding here is graded on an unreachable line.
- Scope: changed lines and the prior blocking findings (command Review Loop bullet 5). The rest of the document was not re-reviewed; this is a scoped review, not whole-document assurance.

## Panel (review order)

Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower; leads Wiegers (requirements) and Fowler (architecture).

## Prior blocking findings

| Id | Prior status | Now | Reason (compared with the AFTER text only) |
|---|---|---|---|
| F-1 | open (r1:26) | resolved | WC-4 (62) now gives a rule for the file-valued `--output` of tdd and init-lite (rows 87, 90: parent directory of the file) and lets the section 3 row name another location (adversarial 83, workflow 92). A contract path now exists for the live check (182-183) and AC-2.3 (201) to test. The wrong outcome in r1:28 (`<file>/return-contract.yaml`) can no longer be built from the stated text. |
| F-2 | open (r1:33) | resolved | AC-1.1 (195) now excludes `load` and the three P4 commands, which removes the count mismatch r1:36 recorded: `load` (row 112, Decisions 265) and the P4 commands (162, 109, 113, 114, with D2-D4 at 225) no longer need a Phase 1 section. P1 row (159) excludes the P4 commands. pr-submit under D3(a) (240) is no longer required to carry a section. |
| F-3 | open (r1:40) | resolved | Row 105 now says `--resume <contract>` counts as approval of the gate the contract names as blocked, so after three resumes a run reaches `succeeded`. The gate-then-resume sequence in r1:130 now has a stated step. The remaining wording gap in AC-2.3 is recorded as M-10 below (Medium). |

No prior blocking finding is open or regressed. Nothing was deferred or withdrawn (`revise1.md:7-17` reports all three applied).

## New findings on changed lines

### M-8 [Medium, origin=changed] WC-4's parent-directory rule can put two workers' contracts at the same path, against WC-11
- Experts: Newman, Nygard, Whittaker (Accumulation attack)
- Changed line: 62 ("or the parent directory of a file-valued `--output`"). WC-11 (69): "Two workers in one worktree must never write the same file."
- Two tdd (or init-lite) workers whose briefs say `--output .dev/tdd/a.md` and `--output .dev/tdd/b.md` get the same contract path `.dev/tdd/return-contract.yaml`; the second worker overwrites the first. The text still gives the coordinator the lever (section 2.3, 73: the brief states the output location), so the clash needs a coordinator that puts two file outputs in one directory. That is a guess about the worse of two readings, so Medium. Fix: one clause in section 2.3 ("one file-valued `--output` per directory") or name the contract `<stem>.return-contract.yaml` for file-valued outputs.

### M-9 [Medium, origin=unchanged, depends on changed line 195] Two inherited lines still treat `load` as a command that gains an `## Unattended mode` section
- Experts: Wiegers, Crispin
- Line 76 ("Every changed command also gains the `## Unattended mode` section") and the P1 sentence at 159 (the flag is accepted by every command in sections 3.1 and 3.2 except the P4 commands) do not carve out `load`, while AC-1.1 (195) now does and the load row (112) says "Report: none". An implementer who reads 76 literally adds a section to `load`; AC-1.1 does not fail it, and the load row and Decisions (265) say no report is wanted. Harmless to the acceptance test, but two readings exist. Fix: add "except load" to 76 or 159. Not blocking.

### M-10 [Medium, origin=unchanged, depends on changed line 105] AC-2.3 does not describe the cli-portify resume chain
- Experts: Cockburn, Adzic, Crispin
- AC-2.3 (201) says "Happy-path run per P2 command with every required flag in the brief ... 7.2 passes with `--outcome succeeded`". A first cli-portify dispatch has no contract to resume, so it ends blocked at gate 1 (`--outcome failed` by WC-5, 63); `succeeded` is reachable only after three resumed dispatches (row 105). The text does not forbid reading "run" as that chain, so no wrong outcome is forced; the implementer must guess. Fix: one clause in AC-2.3: "for cli-portify, the happy path is the first dispatch plus three `--resume` dispatches; the last one passes 7.2 with `--outcome succeeded`". Not blocking.

### m-5 [minor, origin=changed] Review ids ("(F-1)", "(F-2)", "(F-3)") now sit inside normative text at 62, 105, 159 and 195
- They are traceability tags for the reviser (`revise1.md:3`), not requirements. Remove them when the spec is finalized, or keep them as the reviser contract asks. No effect on behavior.

### m-6 [minor, origin=changed] AC-1.1 no longer checks that the P4 commands get a section after Phase 4
- The exclusion in 195 is justified (P4 waits for D2-D4, 225), but no P4 acceptance check (208-210) asserts the section later. Add the three commands to AC-1.1 at P4 if the user accepts D2-D4. Note only.

## Inherited findings (origin=unchanged, not re-reviewed)

M-1 to M-7 and m-1 to m-4 of round 1 (r1:53-80, r1:108-109) sit on unchanged lines (`revise1.md:3` left them alone). They stay as listed in round1.md and keep their Medium or minor grade. They do not fail this review.

## Mandatory artifacts

### Guard Condition Boundary Table (scoped to guards on changed lines, per Review Loop bullet 5)

Guards on changed lines: G6 (WC-4 output-location choice: directory-valued versus file-valued `--output`, line 62), G7 (cli-portify resume approval, line 105), G8 (AC-1.1 exclusion set, line 195). G1-G5 of round 1 sit on unchanged lines and are not repeated. One/Minimal and Overflow classes are left out where they cannot occur, with the reason in the cell.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G6 contract location | WC-4 (62) | Zero/Empty | no `--output` passed | neither branch | left out: the brief must name the output directory (73), so a worker without one is outside the contract; WC-4 states no fallback, but the brief rule (73) covers it | OK |
| G6 contract location | WC-4 (62) | Typical | `--output <dir>` | directory branch | `<dir>/return-contract.yaml` | OK |
| G6 contract location | WC-4 (62) | Typical | `--output <file>` (tdd 90, init-lite 87) | file branch | contract in the file's parent directory | OK |
| G6 contract location | WC-4 (62) | Sentinel Value Match | section 3 row names its own location (adversarial 83, workflow 92) | override branch | that location; "the brief names it" | OK |
| G6 contract location | WC-4 (62) + WC-11 (69) | Maximum/Overflow | two file-valued `--output` in one directory | file branch for both | same contract path for both workers | GAP (Medium; M-8: no stated behavior, the brief can avoid it) |
| G6 contract location | WC-4 (62) | Legitimate Edge Case | `--output` names a bare filename in the current directory | file branch | parent directory is the current directory; contract at `./return-contract.yaml`; allowed | OK |
| G7 resume approval | cli-portify row (105) | Zero/Empty | no `--resume` (first run) | gate 1 unresolved | blocked at gate 1 with the artifact named | OK |
| G7 resume approval | row 105 | One/Minimal | `--resume` with a contract naming gate 1 | gate 1 passed | stops only at gate 2 | OK |
| G7 resume approval | row 105 | Typical | `--resume` with a contract naming gate 3 | gate 3 passed | run continues to delivery, `succeeded` | OK |
| G7 resume approval | row 105 | Sentinel Value Match | `--resume` with a contract whose status is not `blocked` (for example `succeeded` or `failed`) | no gate named | unspecified | GAP (Medium; no concrete wrong outcome follows: nothing is approved because no gate is named) |
| G7 resume approval | row 105 + AC-2.3 (201) | Legitimate Edge Case | single-dispatch happy path | ends blocked at gate 1 | AC-2.3 wording does not say the chain | GAP (Medium; M-10) |
| G8 AC-1.1 exclusions | AC-1.1 (195) | Typical | a P1 command (analyze) | has a section | passes | OK |
| G8 AC-1.1 exclusions | AC-1.1 (195) | Sentinel Value Match | `load` | excluded | no section asserted; line 76 and 159 still read "every" | GAP (Medium; M-9) |
| G8 AC-1.1 exclusions | AC-1.1 (195) | Legitimate Edge Case | pr-submit under D3(a) | excluded, no pr-submit change (240) | consistent | OK |

FR-8/FR-9 grading: none of the four GAP entries names a concrete wrong outcome, a data-loss risk or a safety-boundary risk. Each is Medium and listed under follow-up candidates (M-8, M-9, M-10; the G7 non-blocked resume contract is recorded as M-11 below). FR-10: the table above is complete for the changed-line guards.

### M-11 [Medium, origin=changed] A `--resume` given a contract whose status is not `blocked` has no stated behavior
- Experts: Nygard, Whittaker (Sequence attack)
- Row 105 defines resume only for "the gate the contract names as blocked". Passing a `succeeded` or `failed` contract names no gate; the text is silent. No approval is granted, so no wrong outcome follows from the stated text. Add "otherwise it refuses and writes `status: failed`" or leave to the command. Not blocking.

### Quantity Flow Diagram (Pipeline Dimensional Analysis, triggered: AC-1.1 changes a count)

```text
[Commands in sections 3.1 + 3.2: 37] --> [AC-1.1 exclusion: load (1) + P4 commands (3)] --> [AC-1.1 asserts: 33 sections]
        |
        +--> P1 row (159) flag acceptance: 37 - 3 (P4) = 34   (load is not excluded there: M-9)
        +--> AC-1.1 consumer expects 33; P1 producer builds 33 or 34   <-- 1-command difference, load only, no failing test (M-9)
```

Count basis: 10 ready (3.1) + 27 needing a change (3.2) = 37 (spec:76); `load` row at 112; P4 commands at 109, 113, 114 and 162. The round-1 mismatch (37 expected versus 33-34 buildable, r1:124-125) is gone: the consumer now expects 33.

### Whittaker attacks on the changed lines (selected)
- Divergence Attack on WC-4 (62): the invariant "the contract path is known before dispatch" fails when `--output` is file-valued and a second worker uses the same parent directory. Concrete attack: workers A and B briefed with `--output .dev/tdd/a.md` and `--output .dev/tdd/b.md`; both write `.dev/tdd/return-contract.yaml`; before: no file; after A: A's contract; after B: B's contract replaces it; A's `worker_done --report-path` points at B's content. Recorded as M-8 (Medium: the coordinator controls the paths).
- Sequence Attack on row 105: the invariant "a resume passes only the gate the contract names" fails when `--resume` is given a contract from a different run. Concrete attack: contract of run X (blocked at gate 3) is passed to a fresh run of Y; the text says it counts as approval of gate 3 and gives no check that the contract belongs to the same input. Y's gates 1 and 2 are then not passed by the stated text, so the run stops at gate 1 again or skips ahead depending on `resume_phase`; no outward action is involved. Not graded as blocking: the text does not say gates 1-2 are skipped. Noted under M-11.
- Accumulation Attack on AC-1.1 (195): count 37 became 33 required sections; the exempt set (4) matches the commands whose rows say P4 or "none" report, so no test fails by construction.

### Downstream propagation
GAP entries G6/Maximum (M-8), G7/Sentinel (M-11), G7/Edge (M-10) and G8/Sentinel (M-9) are propagated as invariant candidates for `sc:adversarial` AD-1 (all Medium).

## Blocking findings (open): none

## Follow-up candidates (Medium and minor; none blocks, none appears in the Reviser brief)

- New this review: M-8, M-9, M-10, M-11, m-5, m-6.
- Inherited from round 1 and unchanged: M-1, M-2, M-3, M-4, M-5, M-6, M-7, m-1, m-2, m-3, m-4.
- The session that runs the review asks the user once per loop whether to open an issue for these; this sandbox run did not ask and created no issue.

Coverage line: scoped PASS: changed lines + prior blockers

## Reviser brief

None. No blocking finding is open, so there is nothing to repair. Medium and minor findings are not edited, including when a brief says "apply all findings".

verdict: PASS
