review: 1 of 3

# Merged first review (coordinator; MERGE rule over two independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 39a2d875adeb7b8d312d17e90f13275c174fb95ac61c051d04075970e198a7a4
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 f84c4897b94222357b633bad77aa78f0b5a02ea18ef2cf5a91cc7b8099baaaad

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M1, M2, M3, M4, M5, M6, M7. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: none. The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M1

#### M1.a, from round1-a.md R1-B1: R1-B1. CRITICAL (blocking): AC-1.1 and the P1 scope require a P1 `## Unattended mode` section on commands that sections 3 and 6 assign to P4, and that D3 (a) says get no pr-submit change.
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

### M2

#### M2.a, from round1-a.md R1-B2: R1-B2. CRITICAL (blocking): WC-4 puts the contract in `<output-dir>`, "the directory the coordinator passed (`--output` / `--output-dir`)", but section 3 and the acceptance checks pass `--output <file>` to the same commands.
- Experts: Wiegers (testability), Adzic (concrete example), Whittaker (Divergence attack: the same flag is a file in one branch and a directory in the other).
- Stated texts in conflict:
  1. WC-4: "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`...spec.md:62`).
  2. Section 3.1, `tdd`: brief passes "`--output <file>`" and the report is "the TDD at `--output`" (`...spec.md:90`). `init-lite`: "`--output <file>`" (`...spec.md:87`). The inventory confirms the tdd output is a file: "the final TDD at `--output` or `docs/[domain]/TDD_[COMPONENT-NAME].md`" (`inventory/commands-b.md:222`).
  3. AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked` with a non-empty `blocked_question`" (`...spec.md:200`). Live-check step 4 then runs `test -s <contract>` with no rule for where `<contract>` is when `--output` is a file (`...spec.md:183`).
  4. Section 2.3 says the output directory is passed so "the report path is known before dispatch" (`...spec.md:73`).
- Sentence: An implementer who follows WC-4 as written for `tdd` and `init-lite` takes the `--output` value (a file path such as `docs/auth/TDD_AUTH.md`) as `<output-dir>` and writes `docs/auth/TDD_AUTH.md/return-contract.yaml`, and X is wrong because that path is under an existing regular file, so the write fails, and no contract exists on the very `blocked` outcome AC-2.2 checks; the coordinator also cannot know the contract path before dispatch. No rule in the document says where the contract goes when `--output` is a file.
- Fix direction: state one rule (for example `--output` file means the contract is a sibling `<file-stem>.return-contract.yaml`, or require `--report-dir` as a separate directory flag) and apply it in 3.1, 3.2 and 7.2.

### M3

#### M3.a, from round1-b.md F1: F1. CRITICAL (blocking). P1 scope names 37 commands, the P1 command list names 13, AC-1.1 asserts 37. Experts: Wiegers (lead), Fowler, Whittaker (divergence attack). Priority High. Quality impact: Completeness and Consistency drop (about -2 each).
Quoted texts:
- Spec `:159` (P1 row, Scope cell): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
- Spec `:159` (same row, Commands cell): "analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow". That is 9 commands plus 4 fixes = 13.
- Spec `:195` (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". Sections 3.1-3.2 hold 37 commands (`:78-125`).
- Spec `:84,87` (brainstorm and init-lite, column "Small fix"): "None". Spec `:76`: "Every changed command also gains the `## Unattended mode` section".
- Spec `:114` (pr-submit, phase P4) and `:109` (implement, P4): their report and gate changes are scheduled after P1.

Grading sentence: An implementer who follows the stated P1 Commands cell edits 13 command files, and AC-1.1 then fails for the other 24 (brainstorm, init-lite, reflect, release-split, tdd, troubleshoot, and the P2-P4 commands), because AC-1.1 requires the section in all 37. An implementer who follows the Scope sentence and AC-1.1 instead gives 24 gate or P2-P4 commands an `--unattended` flag in P1 while their gates (P2, `:160`) and contract writes (P2-P4, `:99-125`) do not exist yet, so a worker briefed with `--unattended` on, for example, `/sc:cli-eval run` still stalls on `AskUserQuestion`, which WC-2 (`:60`) forbids under `--unattended`. Both readings produce a wrong result with no further assumption: the three stated texts contradict each other.

Recommendation (narrow, no new rule): make the P1 Scope sentence, the P1 Commands cell and AC-1.1 name the same command set. The smallest repair is to restrict AC-1.1 to the P1 commands listed in the Commands cell and let AC-2.1, AC-3.x and AC-4.x carry the section check for the commands of their own phase; delete the clause "every command in sections 3.1 and 3.2" from the Scope cell.

Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21; the rollout is a multi-stage filter with N != M at each stage):

```text
[Source: 43 commands (INV-A:3 = 21, INV-B:3 = 22)] --> [Stage 1: classify]
   --> 10 ready (3.1) + 27 needs-change (3.2) + 6 coordinator-only (4)      [37 worker-capable]
[37 worker-capable] --> [Stage 2: phase assignment (section 6)]
   P1 = 9 needs-change + 4 ready fixes = 13
   P2 = 11 needs-change + 4 ready (reflect, release-split, tdd, troubleshoot) = 15
   P3 = 4, P4 = 3, no phase = 2 (brainstorm, init-lite)        [13+15+4+3+2 = 37, conserved]
[P1 consumer: AC-1.1 expects 37 sections]           <-- MISMATCH (13 are scheduled in P1)
[P1 consumer: Scope sentence expects 37 flags]      <-- MISMATCH
[P2-P4 consumers: AC-2.1, AC-3.1, AC-4.x]          expect 15 / 4 / 3
```

### M4

#### M4.a, from round1-b.md F2: F2. MAJOR graded blocking. The WC-4 contract path contradicts the paths in section 3.1 and in AC-0.4, so live-check steps 3 and 4 cannot pass for the P0 smoke commands. Experts: Wiegers, Adzic, Crispin. Priority High. Quality impact: Testability -2.
Quoted texts:
- Spec `:62` (WC-4): "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed ... known before dispatch".
- Spec `:73` (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)".
- Spec `:182` (step 3): "its report path is the WC-4 contract path". Spec `:183` (step 4): `test -s <contract>` and a YAML assertion on `status` and `command`.
- Spec `:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file".
- Spec `:83`: adversarial contract is `<output>/adversarial/return-contract.yaml`. Spec `:92`: workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`. Spec `:91`: troubleshoot reports `REPORT.md`; its `return-contract.yaml` exists "only when `--caller task-unified`" (`INV-B:242`).

Grading sentence: An implementer who follows AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` as workers and applies step 3, and step 3 cannot pass because (a) troubleshoot writes no WC-4 contract in P0 (the contract "arrives in P1", `:194`, yet P1 does not list troubleshoot, `:159`), (b) workflow's contract path contains an `<id>` the coordinator does not know before dispatch, which WC-4 and 2.3 require, and (c) adversarial's contract sits in `<output>/adversarial/`, not `<output-dir>/`. The step-4 exception in AC-0.4 does not help: `yaml.safe_load` on the markdown `REPORT.md` has no `d['status']` to assert. The criterion that closes evidence gap 1.4(1) (`:43`) therefore cannot pass as written.

Recommendation: state per command, in section 3.1, the exact path the coordinator passes to step 3, or change step 3 to "the report path the command's section 3.1 row names"; restrict step 4 to commands that already write a YAML contract in that phase.

### M5

#### M5.a, from round1-b.md F3: F3. MAJOR graded blocking. AC-2.2 and AC-2.3 need a WC-4 contract from commands that no phase makes write one, and from commands whose `--output` is a file. Experts: Wiegers, Crispin. Priority High. Quality impact: Testability -2.
Quoted texts:
- Spec `:200` (AC-2.2): "contract `status: blocked` with a non-empty `blocked_question`", example "`/sc:tdd "auth" --unattended --output <file>`". Spec `:201` (AC-2.3): "7.2 passes with `--outcome succeeded`", which includes step 4 (`:183`).
- Spec `:89-91`: the P2 changes for release-split, tdd and troubleshoot are gate resolutions only. Spec `:79`: "the worker reports the named file until Phase 1 adds the contract". The P1 Commands cell (`:159`) names none of these three commands.
- Spec `:90` (tdd) and `:87` (init-lite): `--output <file>`. WC-4 (`:62`) writes the contract in "the directory the coordinator passed". `INV-B:222` confirms tdd's `--output` is the TDD file.

Grading sentence: An implementer who follows section 3.1 and section 6 builds tdd, troubleshoot and release-split with gate handling but no `return-contract.yaml`, because no phase assigns it; AC-2.2 (blocked contract) and AC-2.3 step 4 (`test -s <contract>`) then cannot pass. For tdd the contract directory is undefined, because `--output` names a file, so `<output-dir>` is not "the directory the coordinator passed"; with two tdd workers writing to files in one directory the one fixed filename would collide (WC-11, `:69`).

Recommendation: add the contract write to the P2 rows of release-split, tdd and troubleshoot (it is the WC-4 text, not a new rule) and state in WC-4 where the contract goes when `--output` is a file (for example `<file-stem>.return-contract.yaml` beside it).

### M6

#### M6.a, from round1-b.md F4: F4. MAJOR graded blocking. AC-2.2 requires a blocked outcome from P2 commands whose gate does not resolve as blocked. Experts: Adzic, Crispin. Priority High. Quality impact: Testability -1.
Quoted texts:
- Spec `:200` (AC-2.2): "Gate-trigger run per P2 command ... `worker_done --outcome failed`; contract `status: blocked`".
- Spec `:160`: P2 includes auggie-review, cleanup, improve, research, reflect and tasklist.
- Their gate resolutions are defaults, not blocked: auggie-review "implies `--no-post-pr` and `--no-remediation-offer`" (`:100`); cleanup and improve "apply only items the file already allows ... list every 'Approval Required' item" (`:103,110`); research "pins `--strategy planning`" (`:116`); reflect "follow the existing headless auto-accept rule" (`:88`); tasklist "passes `--unattended` to each reflect" (`:122`).

Grading sentence: An implementer who follows section 3 builds these six commands so that `--unattended` resolves the gate by default and the run succeeds; AC-2.2 then asks for `--outcome failed` with `status: blocked` and a non-empty `blocked_question`, which these commands never produce, so AC-2.2 cannot pass for six of the fifteen P2 commands.

Recommendation: scope AC-2.2 to the P2 commands whose row says "blocked" (recommend, cli-eval, cli-portify, review-translation, spec-panel, task, tdd, troubleshoot, release-split) and give the other six a check that the default was applied (flags implied, items listed, strategy pinned).

### M7

#### M7.a, from round1-b.md F5: F5. MAJOR graded blocking. `/sc:load` is a P1 command under AC-1.1 and AC-1.2 but is defined as never dispatched and as having no report. Experts: Wiegers, Cockburn. Priority Medium. Quality impact: Consistency -1.
Quoted texts:
- Spec `:112` (load): report "none (see note)", "use it as a step inside another worker's brief, not as its own Task"; P1 "(usage line only)". Spec `:268` (Decisions): "a report file would be an unrequested addition".
- Spec `:195` (AC-1.1): the section must name `return-contract.yaml`. Spec `:196` (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`", which includes steps 3 and 4 (`:182-183`).

Grading sentence: An implementer who follows `:112` writes no contract and adds no output flag for load; AC-1.2 runs load as a worker with `--output <dir>` and step 4 (`test -s <contract>`) cannot pass, and AC-1.1 requires a section that names a file the command never writes.

Recommendation: remove load from AC-1.1/AC-1.2 and check its usage-line fix only (AC-1.4-style grep for `--checkpoint`).

## Noted, unactioned (verifier rejected; not prior blocking findings)

None.

## Follow-up candidates

Listed in the two source reports above; not merged.

## Reviser brief

Blocking finding ids: M1, M2, M3, M4, M5, M6, M7.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
