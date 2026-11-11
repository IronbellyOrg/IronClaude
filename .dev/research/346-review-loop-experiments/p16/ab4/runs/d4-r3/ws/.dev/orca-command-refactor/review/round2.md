review: 2 of 3

# Spec-panel re-review (critique mode, focus requirements,architecture)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, sha256 cbaee912425ccadcbc06bd6c2dd562fc87afea9b7b20dc55342bb7c482b347f0
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (equals the candidate hash recorded in round1.md:5)
- prior: .dev/orca-command-refactor/review/round1.md, sha256 d425933231599c1c40693d90ef82364e967d44dc5a34b1bed139be90fd50ff30 (header `review: 1 of 3`, round1.md:1; N = 1 + 1 = 2)
- lint: .dev/orca-command-refactor/review/lint-2.md, sha256 of the candidate cbaee912...347f0 matches the candidate (lint-2.md:1); Checks REF, Findings 0, so no lint id to address (lint-2.md:3-5)
- reviewer model: claude-sonnet-5-5
- roles (fixed by the RE-REVIEW table): CANDIDATE = the `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`
- brief clauses overridden: none
- inputs: all named files present and non-empty. The prior report has the `review: 1 of 3` header and verdict FAIL (round1.md:1,82), so the cap check (prior at review 3) does not apply.

## Step 1, the evidence block

`diff -w BASELINE CANDIDATE` gave 10 changed `<` lines and 11 changed `>` lines (not empty), copied verbatim below. Self-check run: every `>` line was found by `grep -nF` in the candidate (11 of 11) and every `<` line in the baseline (10 of 10); no roles swapped.

```text
BEFORE (baseline), lines starting <, verbatim from diff -w:
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |

AFTER (candidate), lines starting >, verbatim from diff -w:
> | WC-4 | **One report file, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at the location its section 3 row gives. Default: the directory the coordinator passed (`--output-dir`, or `--output` when it is a directory); when `--output` is a file, the directory that contains that file (so the brief passes a file in a directory of its own). A row that names another location (adversarial, workflow, implement, cleanup-audit, index-repo) or no placing flag (research, recommend, review-translation, task, save) overrides the default: the coordinator knows the path before dispatch only if the row builds it from brief values, and otherwise reads it from `worker_done --report-path` (M1, M2, M3). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output location (a directory, or a file in a directory of its own), so the report path is known before dispatch where WC-4 allows it; in P0 the brief omits `--unattended`, which arrives in P1 (M3, M4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `return-contract.yaml` at the location WC-4 gives for the row. Every changed command except load (whose row needs only a usage-line fix and has no contract) also gains the `## Unattended mode` section (section 2.1) (M1, M5). Phase numbers refer to section 6.
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` (`<id>` is made by the run; the coordinator reads the path from `worker_done`, WC-4) | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; it has no contract and no `## Unattended mode` section (M5); separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the contract path WC-4 gives for that command. In P0 (no contract yet) read it as: `--outcome` matches the command's own verdict in its existing report, and the report path is the existing report file named in section 3.1 (M4).
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 (as step 3 reads in P0) and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1 (M4). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except load has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that load and no section-4 command has one (M5) | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except load with `--unattended --output <dir>` (M5) | all steps pass |
> | P2 | AC-2.2 | Gate-trigger run for each P2 command whose section 3 row has a blocked resolution (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, release-split, tdd, troubleshoot): a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic, contract at `<directory of file>/return-contract.yaml`; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` (M6) |
> | P2 | AC-2.2b | Default-resolution run for the other P2 commands (auggie-review, cleanup, improve, research, tasklist, reflect): a 7.2 live check with `--unattended` | the row's default holds: research ran `--strategy planning`; tasklist passed `--unattended` to reflect; reflect showed no `[yes / no]` prompt; cleanup and improve applied only allowed items, listed the rest in the contract and refused `--interactive`; auggie-review posting is checked by AC-2.4; step 5 finds no `AskUserQuestion` (M6) |
```

## Prior blocking findings

Round1 records a verification block: confirmed ids M1-M6, rejected none (round1.md:11). All six are prior blocking findings.

| id | status | basis, AFTER text only |
|---|---|---|
| M1 | resolved | The defect was a contract location of `<output-dir>/return-contract.yaml` where `--output` is a file (tdd, init-lite) and where rows fix their own path. AFTER WC-4 (candidate:62) now sets the default as the `--output-dir`/directory `--output`, "when `--output` is a file, the directory that contains that file", and lets a row override it. AC-2.2 names the tdd path `<directory of file>/return-contract.yaml` (candidate:200). The contradiction between WC-4 and the tdd/init-lite rows (candidate:87,90) no longer holds. The adversarial row (candidate:83) is built from a brief value, so it is the "row builds it" case of WC-4. |
| M2 | resolved | Same repair as M1: the file case has a stated path (candidate:62) and AC-2.2 uses it (candidate:200), so `test -s <contract>` (candidate:183) has a path for tdd and init-lite. |
| M3 | resolved | The "known before dispatch" claim is removed from WC-4's heading and from section 2.3 (candidate:62,73). WC-4 now names the override rows and says the coordinator "otherwise reads it from `worker_done --report-path`" (candidate:62). The workflow row says the same (candidate:92). Step 3 now compares with "the contract path WC-4 gives for that command" (candidate:182) rather than a pre-known path. |
| M4 | resolved | Step 3 is relaxed for P0 the way step 4 was (candidate:182); AC-0.4 says "steps 1-3 (as step 3 reads in P0)" (candidate:194); section 2.3 drops `--unattended` from the P0 brief (candidate:73). For `/sc:troubleshoot` the existing `REPORT.md` is the named report (candidate:91). |
| M5 | resolved | Load is excluded by name in section 3's preface (candidate:76), its row (candidate:112), AC-1.1 (candidate:195) and AC-1.2 (candidate:196). This agrees with the unchanged note at candidate:266 ("a report file would be an unrequested addition"). |
| M6 | resolved | AC-2.2 is limited to the nine P2 commands whose row has a blocked resolution (candidate:200); AC-2.2b checks the default for the other six (candidate:201). The two lists together cover the 15 commands of candidate:160 with no overlap and no omission. Each of the nine rows has a blocked branch (candidate:88-89,90-91,104-105,115,117,120-121). |

## Findings on changed lines

No new blocking finding. Medium and minor findings are in `follow-up candidates`; none fails the review.

### N1 (Medium, origin=changed), the P0 report-path check names a file the adversarial row does not name
- Texts: candidate:182 "the report path is the existing report file named in section 3.1" and candidate:194 (adversarial smoke run); candidate:83 gives the adversarial report as "contract, but filename not fixed".
- Grading sentence: an implementer running AC-0.4 for `/sc:adversarial` has no file named in section 3.1 to compare with, and has to pick the contract the run happened to write. The sentence needs that guess, so it is Medium, not blocking. Troubleshoot (`REPORT.md`, candidate:91) and workflow (candidate:92) are named, so only the adversarial run is affected.
- Evidence: INV-A (the adversarial "return-contract location" note in `inventory/commands-a.md`) says the earlier run wrote the contract in two different places and the skill never names a file; the skill file itself is UNVERIFIED (not in the sandbox).

### N2 (Medium, origin=unchanged but the changed row depends on it), workflow contract path for pre-creation STOPs
- Texts: candidate:92 (changed): "`<id>` is made by the run; the coordinator reads the path from `worker_done`, WC-4", with the unchanged small fix "Write the contract for pre-creation STOPs too". A STOP before the package exists has no `<id>` directory, and no text says where that contract goes. Requirement the document never states, so Medium. `inventory/commands-b.md:272` confirms the contract is today written only after creation (`:41`, `:39` not written for pre-creation STOPs).

### N3 (minor, origin=changed), AC-1.1 closing clause
- candidate:195 "and that load and no section-4 command has one" reads correctly only as "neither load nor any section-4 command has one". Minor wording note.

### N4 (minor, origin=unchanged), AC-1.2 flag mismatch for ready commands
- candidate:196 runs "each P1 command except load" with `--unattended --output <dir>`; P1 includes fixes to cleanup-audit, index-repo and workflow (candidate:159), whose rows give no `--output` (candidate:85,86,92). A note, since the line's changed part (`except load`) does not depend on it.

### N5 (minor, origin=changed), AC-2.2b mixes two checks
- candidate:201 "cleanup and improve ... refused `--interactive`" needs a run that passes `--interactive`, which a single `--unattended` run does not. A note.

### N6 (minor, origin=unchanged), P1 flag scope vs load
- candidate:159 says `--unattended` is accepted by "every command in sections 3.1 and 3.2", while load now has no `## Unattended mode` section (candidate:112). No acceptance check tests flag acceptance for load, so no wrong build follows.

## Guard Condition Boundary Table

Re-review scope: guards on changed lines only (Review Loop bullet 5).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--output` is a file vs a directory | candidate:62 | Typical (file) | `--output tdd.md` | file branch | contract in the directory containing the file | OK |
| `--output` is a file vs a directory | candidate:62 | Typical (directory) | `--output out/` | directory branch | contract in `out/` | OK |
| `--output` is a file vs a directory | candidate:62 | Zero/Empty, Sentinel, One: not applicable beyond the two branches; a bare file name has the working directory as its container, which the text covers by "the directory that contains that file" | none | n/a | n/a | OK |
| row names an override location | candidate:62,92 | Legitimate Edge Case (workflow pre-creation STOP) | no `<id>` yet | override row | not specified (N2) | GAP (Medium, graded under FR-8: no concrete wrong build, a requirement never stated) |
| P0 step-3 read | candidate:182 | Legitimate Edge Case (adversarial) | filename not fixed | P0 branch | "existing report file named in section 3.1" names none (N1) | GAP (Medium) |
| AC-2.2 vs AC-2.2b split | candidate:200-201 | Typical | 9 + 6 commands | partition of candidate:160 | complete and disjoint | OK |

## Adversarial notes (Whittaker, changed lines only)

- Sentinel Collision: "known before dispatch" is gone, so no sentinel claims a path the run decides later (candidate:62,73); the only remaining collision is N2.
- Divergence: the two branches of the new WC-4 default (file or directory) are exhaustive for `--output`; the override list (candidate:62) matches the rows at candidate:83,85,86,92,109 and the no-flag rows at candidate:115-117,119,121.
- Sequence: P0 omits `--unattended` and P1 adds it (candidate:73,159); the order is consistent. No attack found that produces a blocking result.

## Coverage

Covered: all 21 changed lines of the diff, the six prior blocking findings, the dependent texts at candidate:60-62,73,76,83-92,112,158-162,178-186,194-201,266. Not covered: `cmd/` and `sk/` source lines, which are not in the sandbox, so every `cmd/` and `sk/` citation in the candidate is UNVERIFIED here; inventory lines read: `inventory/commands-a.md` (adversarial notes), `inventory/commands-b.md:65,272`.

scoped PASS: changed lines + prior blockers

## Follow-up candidates

N1, N2 (Medium); N3, N4, N5, N6 (minor). No issue is opened: the session that ran this review cannot ask the user in this sandbox, so the list is recorded only (the `--unattended` rule).

verdict: PASS
