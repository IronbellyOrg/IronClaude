review: 2 of 3

# Spec-panel re-review, round 2: orca-worker-contract-spec.md

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Roles (fixed by the RE-REVIEW prompt table, `~/.claude/rules/prompts/document_review_loop_prompts.md:38-42`): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`.
- Review number: PRIOR's header is `review: 1 of 3` (`round1.md:1`), so N = 2.
- Candidate SHA-256: `0c0dfe399e2121731d70aeb7cfd72ce90647f551183721fbf9e5d10ed5273f3a`
- Baseline SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the Candidate SHA-256 recorded in `round1.md:8`, so the baseline is the text round 1 reviewed).
- Reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5).
- Prompt followed: RE-REVIEW prompt, `document_review_loop_prompts.md:34-47` (read in full, sandbox home copy). Brief clauses overridden: none. `~/.claude/agents/rf-qa.md` does not exist in the sandbox, so the re-check follows the rules of the command's Review Loop bullet 5 alone, which stand alone as the command allows (`command.md:262`).
- `--unattended` not passed; Unattended-mode section does not apply. `--re-review` skips the Improve step: no revised specification is written (`command.md:261`).
- Panel (focus requirements: Wiegers lead, Adzic, Cockburn; focus architecture: Fowler lead, Newman, Hohpe, Nygard; Whittaker active), in the command's fixed sequence.

## Evidence limits
Checkable inputs: `.dev/orca-command-refactor/README.md`, `inventory/{commands-a,commands-b,orca-capabilities}.md` (INV-A, INV-B, CAPS), `review/round1.md`, `review/revise1.md`, `command.md` and the prompts file. Every spec citation of the form `cmd/...`, `sk/...`, `src/...`, `CLAUDE.md:N`, `pyproject.toml:N` is UNVERIFIED here. `revise1.md` is the reviser's own account and is not treated as evidence of what changed; only the diff is. The reviser's byte figures (57,763 before, 58,197 after, `revise1.md:6`) match `wc -c` of the two files (57763 and 58197).

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)
Changed hunks: 62, 73, 120, 159, 194-196 (7 changed lines; lines 194-196 are three lines). Quoted verbatim. Some table cells are long; the quote is the whole line.

BEFORE (baseline), lines starting `<`:

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

```text
| spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
```

```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```

```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

```text
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate), lines starting `>`:

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); when the command's output flag is file-valued (tdd, init-lite, spec-panel), the contract is `<that file path>.return-contract.yaml`, beside the file (B-2). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory (or, for a file-valued `--output`, the file path), so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

```text
| spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output <file>`; contract beside it (WC-4, B-2) | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
```

```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by each command named in this row (a no-op where a command has no gate; `/sc:load` gets the flag and usage-line fix only, no contract, B-1); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; steps 3 and 4 use the command's existing report file for the path and the outcome comparison, since the contract arrives in P1 (B-3). Record the results in the phase report; a failure here reopens section 1 |
```

```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in the P1 row of section 6 except `/sc:load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command and no command of a later phase has one yet (B-1) | passes |
```

```text
| P1 | AC-1.2 | 7.2 live check on each P1 command except `/sc:load` with `--unattended --output <dir>` | all steps pass |
```

Self-check (run): each of the 7 AFTER lines was found with `grep -nF` in the candidate and each of the 7 BEFORE lines in the baseline; none was missing, so no role swap. The diff is non-empty, so prior findings are decided on the AFTER text below.

## Prior blocking findings (from `round1.md:117-119`, ids kept)

| Id | Status | Basis |
|---|---|---|
| B-1 | resolved | Defect (`round1.md:68`): P1 scope and AC-1.1 required the `## Unattended mode` section and a contract on all 37 commands of sections 3.1-3.2 in Phase 1, contradicting `/sc:load` having no report and the later-phase placement of 24 commands. AFTER P1 row (candidate line 159): the flag applies to "each command named in this row", and "`/sc:load` gets the flag and usage-line fix only, no contract, B-1". AFTER AC-1.1 (line 195) asserts the section only for "every command in the P1 row of section 6 except `/sc:load`" and that no section-4 command and no later-phase command has one yet. AFTER AC-1.2 (line 196) excludes `/sc:load`. The P1 row now supplies 12 sectioned commands (analyze, build, business-panel, design, document, explain, index, test, adversarial, cleanup-audit, index-repo, workflow) and AC-1.1 expects those same 12 (counts conserved; the 37 vs 13 mismatch of `round1.md:54-59` is gone). Consistent with the `/sc:load` row (line 112) and its Decisions row (line 265), with pr-submit/implement/post-release deferred to P4 (line 162) and with D3 (a) (line 240). |
| B-2 | resolved | Defect (`round1.md:75`): WC-4 placed the contract at `<output-dir>/return-contract.yaml`, impossible when `--output` is a file (tdd, init-lite). AFTER WC-4 (line 62): "when the command's output flag is file-valued (tdd, init-lite, spec-panel), the contract is `<that file path>.return-contract.yaml`, beside the file (B-2)". That path can be created next to a regular file, is computable before dispatch (WC-4 "known before dispatch"), and AFTER 2.3 (line 73) now has the brief state "the output directory (or, for a file-valued `--output`, the file path)". AC-2.2's `/sc:tdd "auth" --unattended --output <file>` (line 200) now has a creatable contract path. |
| B-3 | resolved | Defect (`round1.md:83`): AC-0.4 step 3 required the contract's `status` and the WC-4 contract path while AC-0.4 says the contract arrives in P1. AFTER AC-0.4 (line 194): "steps 1, 2 and 5-7 pass; steps 3 and 4 use the command's existing report file for the path and the outcome comparison, since the contract arrives in P1 (B-3)". Step 3 no longer depends on a file Phase 0 does not produce. One residual about step 4 is recorded as M-13 below; it is not the B-3 defect. |

Regressed: none. Open: none.

## Findings on changed lines

Each carries `origin`. No new blocking finding was found; grading used the sentence test of the prompt (a blocking finding needs a sentence that holds with no further assumption).

=== REQUIREMENTS ANALYSIS ===
Wiegers, Adzic, Cockburn: the three revisions are narrowing or one-clause additions, each cites its finding id, and each prior blocking defect is closed. The new findings below all need an assumption about how an implementer reads the text, so they are Medium.

=== ARCHITECTURE ANALYSIS ===
Fowler, Newman, Hohpe, Nygard: the contract-beside-the-file rule keeps one file per run and one name suffix, and does not touch the coordinator or Orca boundary (WC-8, SA-2 unaffected). Pipeline Dimensional Analysis: the staged plan is the only multi-stage flow; counts are in the Quantity Flow Diagram.

### Medium findings (warnings; follow-up candidates)
- M-13 (Crispin/Whittaker; origin=changed, line 194, same-line carry-over of step 4) AC-0.4 step 4 still runs the YAML check (`d['status']`, `d['command']`, spec line 183) on "the command's existing report file". For `/sc:troubleshoot` that file is `REPORT.md` (spec line 91), a markdown report; whether it parses as YAML with those keys cannot be checked here (`cmd/`/`sk/` UNVERIFIED). The sentence "steps 3 and 4 use the command's existing report file" does not say the `status`/`command` assertion is relaxed for P0. Blocking only if `REPORT.md` is not YAML with those keys; that is a guess, so Medium. The same wording stood in the baseline and round 1 accepted it (`round1.md:85`).
- M-14 (Wiegers/Crispin; origin=changed, line 195) AC-1.1 asserts "no command of a later phase has one yet". The test file persists and grows (AC-2.1 adds assertions to the same file, line 199), while AC-C3 (line 174) forbids a baseline-passing test failing. If the negative clause is coded as a fixed list it fails as soon as P2 adds the section to its commands; the text allows a phase-scoped reading ("yet"), so this needs a guess that the implementer picks the fixed list. Medium.
- M-15 (Wiegers; origin=changed, line 62) WC-4 lists init-lite as writing `<file>.return-contract.yaml` in unattended mode, but init-lite is a 3.1 ready command with no small fix and no phase (`line 87`, INV-A:55 "ready-as-Orca-worker"), and the P1 row (line 159) does not name it, so no phase and no acceptance check delivers its `--unattended` section or contract. Needs a guess about which phase owns it. brainstorm has the same shape but already writes `<output>/return-contract.yaml` (line 84).
- M-16 (Nygard; origin=changed, line 62) The file-valued list "(tdd, init-lite, spec-panel)" is closed, while the P1 rows add new `--output` flags to analyze, build, design, document, explain, index and test without saying whether they take a directory or a file (lines 99-123); AC-1.2 assumes `--output <dir>` for all of them (line 196). Two readings are allowed for explain ("write the explanation to a file", line 108) and document ("require an explicit output", line 107).
- M-17 (Fowler; origin=changed, line 120) The spec-panel row says "add `--output <file>`", citing `cmd/spec-panel.md:22` and INV-B:43 (which records no `--output`). The sandbox `command.md:22-24,460-461` already has `--output <file>` and defines its own `--report-dir <dir>` contract location. That is a different copy than the inventory describes (INV-B:43 cites `:455-460` for the review document; `command.md` has it at `:483-490`), so which copy the spec targets cannot be settled here (UNVERIFIED). Carried from `round1.md:77`; unchanged by the revision except for the added clause.
- Carried from `round1.md` and not re-graded: M-1 to M-12 stay as listed there; the reviser did not touch them (`revise1.md:3`), and none is on a line this revision changed except as noted above.

### Minor notes
- N-5 Section 3 intro (line 76, unchanged) still defines "Contract" as `<output-dir>/return-contract.yaml` and says every changed command gains the `## Unattended mode` section; the file-valued rule and the `/sc:load` exception live in WC-4 and the P1 row. origin=unchanged; the reviser noted the second part (`revise1.md:22`).
- N-6 7.2 step 6 (line 185) says changed files appear "under the brief's output directory"; the beside-the-file contract sits in the file's parent directory. The parenthetical "documented artifacts" covers it. origin=unchanged.
- N-7 AC-1.2 (line 196, changed) runs `--output <dir>` on cleanup-audit and index-repo, whose output location the 3.1 rows call fixed (lines 85-86). origin=unchanged text of those rows; the changed AC line does not quote them.
- N-8 `round1.md:115` says the spec is 270 lines; both files are 285 lines (`grep -c ''`). No effect on any finding.

## Guard Condition Boundary Table (changed lines only, per Review Loop bullet 5)
Trigger fired: changed lines contain guards (file-valued vs directory-valued output flag, AC-1.1 command set, AC-0.4 step selection). Classes that cannot occur are left out with the reason on the row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-4 file-valued output flag | spec line 62 | Typical | `--output .dev/tdd/auth.md` | file-valued | contract `.dev/tdd/auth.md.return-contract.yaml` | OK |
| WC-4 directory-valued output flag | spec line 62 | Typical | `--output .dev/troubleshoot/login/` | directory | `<dir>/return-contract.yaml` | OK |
| WC-4 output flag present | spec line 62 | Zero/Empty | no output flag in an `--unattended` brief | no path | unspecified (brief must supply it, line 73; no refusal stated) | GAP, Medium (carried M-5) |
| WC-4 "file-valued" membership | spec line 62 | Legitimate Edge Case | new P1 `--output` on explain or document | type not stated | unspecified (M-16) | GAP, Medium (M-16) |
| WC-4 init-lite | spec line 62 | Legitimate Edge Case | init-lite run with `--unattended` after P1 | no phase owns it | unspecified (M-15) | GAP, Medium (M-15) |
| WC-4 sentinel | spec line 62 | Sentinel Value Match | file-valued value ending in `/` | would be a directory | not applicable: a file-valued flag names a file; left out | n/a (reason given) |
| AC-1.1 command set | spec line 195 | Typical | the 12 sectioned P1 commands | asserted | section present | OK |
| AC-1.1 exclusion | spec line 195 | Legitimate Edge Case | `/sc:load` | excluded | no assertion; consistent with line 112 | OK |
| AC-1.1 negative clause | spec line 195 | Maximum/Overflow | P2 lands the section in its commands | clause turns false | unspecified whether the test is phase-scoped (M-14) | GAP, Medium (M-14) |
| AC-0.4 step 3 | spec line 194 | Typical | troubleshoot ends with `REPORT.md`, no contract | existing report used | path and outcome compared with the existing report | OK |
| AC-0.4 step 4 | spec line 194 | Legitimate Edge Case | `REPORT.md` is not YAML | YAML assertion | unspecified whether relaxed (M-13) | GAP, Medium (M-13) |
| AC-0.4 steps 1,2,5-7 | spec line 194 | Zero/Empty | none of them needs the contract | n/a | pass conditions independent of P1 | OK |

No GAP names a concrete wrong outcome an implementer would produce with no further assumption, and none is a security, data-loss or safety-boundary risk, so none is blocking (FR-8/FR-9 grading, `command.md:332-333`).

## Quantity Flow Diagram
```text
[Source: 43 commands] --> [Inventory verdicts: 10 ready | 27 needs-change | 6 coordinator-only]   (10+27+6 = 43)
  P1 row names: analyze, build, business-panel, design, document, explain, index, test (8) + adversarial, cleanup-audit, index-repo, workflow (4) = 12 sectioned, + load (flag and usage line only, no section)
  AC-1.1 expects: the same 12 (load excluded)                                 <-- consumer now matches the stage (round 1: 37 vs 13)
  P2 15 | P3 4 | P4 3 | brainstorm, init-lite carry no phase                    <-- init-lite undelivered contract: M-15
```

## Coverage
scoped PASS: changed lines + prior blockers. This is a scoped result on the 7 changed lines and the three prior blocking findings; it gives no whole-document assurance. Read in full: the 7 diff lines and their surrounding rows (spec lines 56-80, 94-135, 153-215, 236-285), `round1.md`, `revise1.md`, `README.md`, `command.md`, the prompts file; INV-A:55 and INV-B:43,177-185 for init-lite and spec-panel. Not covered: unchanged text outside the changed lines' dependencies, and every `cmd/`/`sk/` citation (UNVERIFIED).

## Follow-up candidates
Medium: M-13, M-14, M-15, M-16, M-17 (above), plus carried M-1 to M-12 from `round1.md:92-104`. Minor: N-1 to N-4 (`round1.md:107-110`) and N-5 to N-8. The user question about opening an issue for these is not asked and no issue is created: this sandbox has no user channel (`command.md:259-260` allows creating one only after the user answers).

## Reviser brief
No blocking finding is open, so no revision is requested. (Rules if one were: revise only text a blocking finding names; add nothing no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing; report bytes before and after and added and deleted per finding id.)

verdict: PASS
