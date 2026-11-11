review: 1 of 3

# Spec panel report, round 1 (critique mode, focus requirements,architecture)

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (computed; it equals the hash printed in `review/lint-1.md:1`).
- Baseline: missing (a first review; `baseline: missing` is not an error here). Prior report: none.
- Lint file: `.dev/orca-command-refactor/review/lint-1.md`, sha256 `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`.
- Reviewer model: Sonnet 5.5 (`claude-sonnet-5-5`). This is ONE first review. The FIRST-REVIEW prompt asks for two independent first reviews plus a coordinator MERGE; the coordinator owns the second review and the merge. Findings below are `R1-` ids, not merged `M` ids.
- Evidence limits: only `README.md` and `inventory/*` could be read. Every `src/...`, `~/.claude/...`, `/opt/Orca/...` and `.dev/evals/...` line the spec cites is UNVERIFIED here unless an inventory line quotes it (marked `via INV-A/INV-B/CAPS`). The `cmd/` files were not in the sandbox.
- Coverage: whole document (sections 1-9, Decisions, UNVERIFIED items) against the requirements it states. Checked: internal consistency of WC-1..WC-12, SA-1..SA-6, section 3 tables, phase plan, acceptance checks, open decisions. Command counts were re-derived (see Requirements, item 1).

## Lint evidence
`lint-1.md:3-5`: "Checks: REF. Findings: 0. No findings." No lint id exists to confirm or dismiss. Lint covers references only, so it says nothing on the contradictions below.

## Grading note
Each blocking finding carries the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding that needs a guess about the implementer's reading is Medium and sits under follow-up candidates.

## === REQUIREMENTS ANALYSIS ===

### R1-B1. CRITICAL (blocking): AC-1.1 and the P1 scope require a P1 `## Unattended mode` section on commands that sections 3 and 6 assign to P4, and that D3 (a) says get no pr-submit change.
- Experts: Wiegers (traceability), Cockburn (goal), Whittaker (Sequence attack).
- Stated texts in conflict:
  1. Phase 1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`specs/orca-worker-contract-spec.md:159`).
  2. AC-1.1: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (`...spec.md:195`).
  3. The same section 3 table assigns `implement`, `post-release` and `pr-submit` to "P4" (`...spec.md:109,113,114`), and section 6 puts them in P4 "so it needs the user's decision first" (`...spec.md:162`).
  4. D3 recommendation (a): "The coordinator ... runs it after the workers finish; no pr-submit changes in Phase 4" (`...spec.md:240`). Section 4 also says `/sc:pr-submit` is a worker candidate "only if the user accepts open decision D3" (`...spec.md:139`).
  5. "Phases 0-3 can proceed on the recommendations; Phase 4 waits for D2-D4" (`...spec.md:225`; also `...spec.md:154`).
- Sentence: An implementer who follows the stated text as written runs P1 on the recommendations, accepts D3 (a) and D2 (a), and then must pass AC-1.1. AC-1.1 requires a `## Unattended mode` section in `pr-submit.md`, `post-release.md` and `implement.md`. That means writing those commands' gate resolutions before D2-D4 are answered, and giving `pr-submit` a worker-mode section that D3 (a) says it must not have. X is wrong because the P1 test cannot pass without either editing pr-submit against the recommended decision or failing `tests/skills/test_worker_contract.py`, and because it makes the P4 decisions in P1.
- Count check supporting this (Pipeline Dimensional Analysis, applied to the command-to-phase mapping): section 3.2 assigns 9 commands to P1, 11 to P2, 4 to P3 and 3 to P4 (27), but the P1 flag/test scope covers all 37 commands of sections 3.1 + 3.2 (10 + 27). Section 3.1 and 3.2 counts re-derive correctly (10, 27; INV-A:3 gives 21 and `INV-B:3` gives 22 commands; 10 + 27 + 6 = 43).
- Fix direction (not text to add): narrow AC-1.1 and the P1 flag sentence to the commands whose phase is P1, or state that P4 commands get no section until D2-D4 are answered.

### R1-B2. CRITICAL (blocking): WC-4 puts the contract in `<output-dir>`, "the directory the coordinator passed (`--output` / `--output-dir`)", but section 3 and the acceptance checks pass `--output <file>` to the same commands.
- Experts: Wiegers (testability), Adzic (concrete example), Whittaker (Divergence attack: the same flag is a file in one branch and a directory in the other).
- Stated texts in conflict:
  1. WC-4: "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`...spec.md:62`).
  2. Section 3.1, `tdd`: brief passes "`--output <file>`" and the report is "the TDD at `--output`" (`...spec.md:90`). `init-lite`: "`--output <file>`" (`...spec.md:87`). The inventory confirms the tdd output is a file: "the final TDD at `--output` or `docs/[domain]/TDD_[COMPONENT-NAME].md`" (`inventory/commands-b.md:222`).
  3. AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked` with a non-empty `blocked_question`" (`...spec.md:200`). Live-check step 4 then runs `test -s <contract>` with no rule for where `<contract>` is when `--output` is a file (`...spec.md:183`).
  4. Section 2.3 says the output directory is passed so "the report path is known before dispatch" (`...spec.md:73`).
- Sentence: An implementer who follows WC-4 as written for `tdd` and `init-lite` takes the `--output` value (a file path such as `docs/auth/TDD_AUTH.md`) as `<output-dir>` and writes `docs/auth/TDD_AUTH.md/return-contract.yaml`, and X is wrong because that path is under an existing regular file, so the write fails, and no contract exists on the very `blocked` outcome AC-2.2 checks; the coordinator also cannot know the contract path before dispatch. No rule in the document says where the contract goes when `--output` is a file.
- Fix direction: state one rule (for example `--output` file means the contract is a sibling `<file-stem>.return-contract.yaml`, or require `--report-dir` as a separate directory flag) and apply it in 3.1, 3.2 and 7.2.

### Follow-up candidates, requirements (Medium or minor; none blocks)
- F1 (Medium, graded Medium because it needs a guess): P1 accepts `--unattended` on gated commands (`...spec.md:159`) while their gate resolutions arrive in P2 (`...spec.md:160`), and section 2.3 requires `--unattended` in every brief (`...spec.md:73`). A coordinator that dispatches `/sc:tdd "topic" --unattended` between P1 and P2 gets a flag that is accepted but does not stop the gate: a silent stall (`...spec.md:44`). The text does not say that a P1-only command must refuse or warn. Reading it the worse way is a guess, so Medium.
- F2 (Medium): WC-3 says the worker "may" ask the coordinator when a gate resolves as blocked (`...spec.md:61`); AC-2.2 requires `worker_done --outcome failed` with `status: blocked` (`...spec.md:200`). A worker that uses its option does not end failed. The brief for gate tests must forbid `ask`; the document does not say so.
- F3 (Medium): WC-4 says commands that already write a contract "keep their fields and add the missing ones" (`...spec.md:62`) but also fixes the `status` vocabulary to four values (`...spec.md:62,262`). The existing contracts' status values were not checked (`sk/sc-workflow-protocol/refs/return-contract.md:3-19` is cited via `INV-B:272`; UNVERIFIED). If they differ, the two sentences conflict.
- F4 (Medium): SA-4 lists the defect fixes that may change existing lines (`...spec.md:149`) but omits the cleanup-audit and index-repo "small fix" rows (`...spec.md:85,86`). If those edit existing lines, AC-C5 (`...spec.md:176`) fails the phase.
- F5 (Medium): section 3.1 says the ready commands run "now if the brief uses the stated flags" (`...spec.md:79`) but section 2.3 requires `--unattended` in each command line (`...spec.md:73`); the flag does not exist until P1. P0's smoke runs omit it (`...spec.md:194`), so the text is only consistent for P0.
- F6 (minor): WC-7 cites `INV-A:95` for "nesting loses tools at Claude Code's depth limit" (`...spec.md:65`); that inventory line opens "Top-level is not the blocker it looked like" (`inventory/commands-a.md:95`). The cited line mentions the depth limit as a risk, so this is a weak citation, not wrong.

## === ARCHITECTURE ANALYSIS ===
Experts: Fowler (interfaces), Nygard (failure modes), Newman (evolution), Hohpe (message exchange).

- The core decision (Orca on top, commands stay units of work, no command calls Orca) is consistent with the evidence it cites: depth 1 (`inventory/orca-capabilities.md:97-103`), `worker_done` only from the dispatched pane (`...orca-capabilities.md:150` as numbered in the spec; the inventory shows the same at its `[H:send]` line 40 entry), and no mention of Orca in the primitives today (E5, `...spec.md:25`; the grep is UNVERIFIED here). No architecture defect found.
- Evidence gaps are stated plainly (`...spec.md:41-45`, `...spec.md:271-285`); the live smoke runs in P0 are the right control. I found no overstated claim there. `inventory/commands-b.md:323` ("No command was run end to end as an Orca worker") and `inventory/orca-capabilities.md:156` back the 1.4 statement.
- Message exchange: WC-5 maps four statuses onto Orca's two outcomes (`...spec.md:63`); the Orca side accepts only `succeeded|failed` (`inventory/orca-capabilities.md:73`). The mapping is complete. A failed status of `blocked` is a failure by design, which the spec states.

### Follow-up candidates, architecture
- F7 (Medium): AC-C1 greps `src/superclaude/core` for `orca ... orchestration|worktree|terminal|agent` and expects no output (`...spec.md:172`), yet P0 adds `WORKER-CONTRACT.md` with a brief template and an Orca section to `HOW-WE-WORK.md`, both in `core/` (`...spec.md:158`). If either text spells a real Orca command (SA-2 allows an Orca example in the contract file, `...spec.md:147`), AC-C1 fails on P0 by its own artifacts. The regex also escapes `\|` inside the table cell; as a literal `grep -E` it would match a literal pipe. It needs a guess about what the files will contain, so Medium.
- F8 (Medium): WC-1 is owned by "Launch setup, not commands" (`...spec.md:59`) but no phase item or acceptance check changes or tests the launch path; P0 only runs the three smoke commands (`...spec.md:158,194`). A requirement with no owner action is untested.
- F9 (minor): the heartbeat rule of 5 minutes comes from the worker preamble, not a guide (`inventory/orca-capabilities.md:130` per the spec at `...spec.md:68`); WC-10 builds a 4-minute wait limit on it. The spec says so. Note only.

## Adversarial analysis (Whittaker, review order 6)
Not all five methodologies produced findings; only those with a concrete state trace are listed.
- **Sequence Attack** on the phase plan: "I can break this specification by Sequence Attack. The invariant at section 6 / AC-1.1 fails when P1 is executed on the recommendations. Concrete attack: step 1 D3 (a) accepted, so pr-submit stays untouched; step 2 P1 runs AC-1.1 over the 37 commands; step 3 `pr-submit.md` has no `## Unattended mode` section; step 4 the test fails. Before: pr-submit unchanged and P1 'independent'; after: P1 either blocked or pr-submit edited against D3." (R1-B1)
- **Divergence Attack** on WC-4: "...The invariant at WC-4 fails when `--output` is a file path. Concrete attack: `--output docs/auth/TDD_AUTH.md`; contract path becomes `docs/auth/TDD_AUTH.md/return-contract.yaml`; write fails; no contract, no `blocked_question`." (R1-B2)
- **Zero/Empty Attack**: WC-4 allows `report_path` "if any" and `blocked_question` "when blocked" (`...spec.md:62`); an empty `blocked_question` with `status: blocked` is not forbidden, although AC-2.2 requires non-empty (`...spec.md:200`). Medium, folded into F2 territory; no separate id.
- Sentinel Collision, Accumulation: no finding. The `--unattended` token is a flag, and section 2.1 decides the token via D1 (`...spec.md:51,227-230`); the quoted-argument rule is absent from the spec, which is a follow-up at most (minor).

## Guard Condition Boundary Table
Guards found in the spec: G1 the `--unattended` switch (WC-2, `...spec.md:60`), G2 status to outcome mapping (WC-5, `...spec.md:63`), G3 wait-size limit (WC-10, `...spec.md:68`), G4 nesting depth 1 (R1, `...spec.md:33`), G5 `<output-dir>` resolution (WC-4, `...spec.md:62`). Classes left out are named with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 unattended switch | WC-2 `:60`, D1 `:228` | Zero/Empty | flag absent | false | standalone behavior unchanged (SA-1 `:146`) | OK |
| G1 unattended switch | WC-2 `:60` | Sentinel Value Match | flag text inside quoted content | not specified | no rule in the spec for a quoted argument | GAP (Medium: the flag is an argument the coordinator writes; no wrong outcome follows without a guess) |
| G2 outcome mapping | WC-5 `:63` | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G2 outcome mapping | WC-5 `:63` | Legitimate Edge Case | `partial`, audit verdict FAIL | true | `succeeded`, with status in the body's first sentence | OK |
| G3 wait split | WC-10 `:68` | Typical | single wait of exactly 5 minutes | true | split into waits of at most 4 minutes | OK |
| G3 wait split | WC-10 `:68` | Maximum/Overflow | cli-eval 3600 s timeout | true | wait split rule; Dispatch total time unbounded is UNVERIFIED (`:282`) | OK (UNVERIFIED) |
| G4 depth 1 | R1 `:33` | One/Minimal | worker calls `worker-start` | true | refused `nested_worker_depth_exceeded`; enforcing call sites UNVERIFIED | OK (UNVERIFIED) |
| G5 output-dir | WC-4 `:62` | Typical | `--output <dir>` | directory | `<dir>/return-contract.yaml` | OK |
| G5 output-dir | WC-4 `:62`, `:90`, `:200` | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | file | unspecified | GAP (blocking: R1-B2) |
| G5 output-dir | WC-4 `:62` | Zero/Empty | `--output` missing | not specified | WC-4 requires a directory the coordinator passed; no rule for a missing one besides 3.2's "add `--output`" | GAP (Medium: restates F2/F1 area; no concrete wrong outcome) |

Classes left out: One/Minimal for G1, G5 (a flag is present or absent); Maximum/Overflow for G1, G2, G5 (no numeric domain); Sentinel for G2-G5 (no sentinel value).
FR-8/FR-9 grading: the one GAP with a concrete wrong outcome is the `--output <file>` row (R1-B2); the others are Medium. FR-10: the table above is complete for the guards enumerated.

## Quality scores (0-10)
Clarity 8, Completeness 7, Testability 7, Consistency 6. Overall 7.

## Coverage statement
Covered: sections 1-9, Decisions and UNVERIFIED items; WC-1..WC-12, SA-1..SA-6, AC-C1..AC-C5, 7.2, 7.3, D1-D5; command counts (10 / 27 / 6 = 43, re-derived from the section 3 tables and `inventory/commands-a.md:3`, `commands-b.md:3`). Not covered: any `src/`, `~/.claude` or `/opt/Orca` line not quoted by an inventory (UNVERIFIED); correctness-focus artifacts (the focus was not requested).

## Follow-up candidates (all Medium and minor findings)
F1, F2, F3, F4, F5, F6, F7, F8, F9 above, plus the two Medium GAP rows of the Guard Condition Boundary Table and the minor quoted-argument note. The session that runs this loop asks the user once whether to open an issue for them; none was created by this reviewer.

## Reviser brief
Blocking finding ids: R1-B1, R1-B2. Rules for the reviser (this restates the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (F1-F9 and the GAP rows) alone. Do not award yourself a PASS.
- R1-B1 names: `...spec.md:159`, `:195`, `:109,113,114`, `:162`, `:240`, `:139`, `:225`.
- R1-B2 names: `...spec.md:62`, `:87`, `:90`, `:183`, `:200`, `:73`.

verdict: FAIL
