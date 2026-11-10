review: 2 of 3

# Re-review report (spec-panel --mode critique --re-review)

command: /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md
reviewer model: claude-sonnet-5-5 (Sonnet 5.5)
review number: prior report `review: 1 of 3` (round1.md:1) plus 1 = 2
Prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; the file refers to a "re-review core below" that does not exist as a section; its roles table and the Step 1 / review number / self-check bullets were applied).

Roles (fixed by the brief, not by reading order):

| ROLE | FILE | sha256 |
|---|---|---|
| CANDIDATE | .dev/orca-command-refactor/specs/orca-worker-contract-spec.md | 51c1db2c9d50566a98e630c6d8b4017397f136684b86e1f54329e02f1d7fd5b1 |
| BASELINE | .dev/orca-command-refactor/specs/history/spec-v1.md | d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d |
| PRIOR | .dev/orca-command-refactor/review/round1.md | 6a32c108b5c44879ba5e81d6b8371dfdcefa246dba000d63141c2ff6df1d844f |

Baseline check: the BASELINE hash equals the candidate hash recorded in round1.md:5, so the baseline is the text that review 1 saw. baseline: present.

Citation key: `SPEC:n` = candidate line n; `BASE:n` = baseline line n; `INV-A:n`, `INV-B:n`, `CAPS:n` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` line n; `CMD:n` = `command.md` line n in the sandbox (the /sc:spec-panel definition). Any `cmd/...` or `sk/...` path cited inside the spec's own rows is not in the workspace: UNVERIFIED by me, taken only through the inventories.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Changed hunks: lines 62, 76, 90, 92, 116, 159, 194-196, 200 (same line numbers in both files). Whitespace-only changes: none. Size 57763 -> 58254 bytes.

### BEFORE (baseline), lines starting `<`
```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

### AFTER (candidate), lines starting `>`
```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`; `--report-dir` for `workflow`, `research` and `tdd`, whose `--output` is a file or does not exist) (M6). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command except `load` also gains the `## Unattended mode` section (section 2.1), in its own phase (M1, M5). Phase numbers refer to section 6.
> | tdd | a precise component prompt, not a bare topic; `--output <file>`; `--report-dir <dir>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | workflow | `--handoff none`; `--report-dir <dir>` (P1) | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too, into `--report-dir` since no package directory exists yet (WC-4 "every outcome"; M6) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract in `--report-dir` naming the generated `claudedocs/research_*.md` path (M6) | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every P1 command in sections 3.1 and 3.2 except `load` (a no-op where a command has no gate; M1, M5); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-2 and 5-7 pass; step 3 passes when exactly one `worker_done` arrives and its report path is the command's existing report file; step 4 uses that same file, since the contract arrives in P1 (M2). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command whose phase is P1 in sections 3.1-3.2, except `load` (M1, M4, M5), has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (M1, M5) with `--unattended --output <dir>` | all steps pass |
> | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file> --report-dir <dir>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

Self-check run: every BEFORE line (without `< `) was found with `grep -nF` in the baseline, every AFTER line (without `> `) in the candidate, and no AFTER line occurs in the baseline. Roles are not swapped.

## Prior blocking findings (round1.md:14-88; M3 was rejected by the verifier and is a note, round1.md:136, not re-checked as blocking)

| id | status | compared against AFTER text only |
|---|---|---|
| M1 | resolved | The defect was AC-1.1 requiring a `## Unattended mode` section for `load` while the load row and Decisions rule a report out (round1.md:16-22). AFTER SPEC:76 says "Every changed command except `load` also gains the `## Unattended mode` section", SPEC:159 says "every P1 command in sections 3.1 and 3.2 except `load`", and SPEC:195 asserts the section for P1 commands "except `load`". The load row (SPEC:112) and the Decisions row (SPEC:265) are unchanged and now agree with the three edited texts. |
| M2 | resolved (for the defect it names; a separate residual is N1) | The defect was step 3 of 7.2 (SPEC:182) requiring a WC-4 contract that P0 cannot produce (round1.md:26-40). AFTER SPEC:194 says "step 3 passes when exactly one `worker_done` arrives and its report path is the command's existing report file". Step 3 no longer demands the contract path or a `status` match in P0. |
| M4 | resolved | Same contradiction as M1, from round1-b B2 and round1-c F1 (round1.md:44-62). Fixed by the same AFTER texts (SPEC:76, 159, 195, 196: AC-1.2 also says "except `load`"), so both ACs that the sub-entries named (AC-1.1, AC-1.2) now exclude load. |
| M5 | resolved | The defect was AC-1.1 and the P1 flag rule covering P2-P4 commands whose gates wait on D2-D4 (round1.md:66-74). AFTER SPEC:195 limits the test to "every command whose phase is P1 in sections 3.1-3.2" and SPEC:159 to "every P1 command". The P1 population this yields in the Phase columns (SPEC:90-92, 99-123) is analyze, build, business-panel, design, document, explain, index, test (section 3.2) and adversarial, cleanup-audit, index-repo, workflow (section 3.1), which equals the P1 command list at SPEC:159 less `load`. No P1 section now depends on D2-D4 (implement, post-release, pr-submit are P4, SPEC:109, 113, 114, 162). |
| M6 | resolved (residuals are Medium F-2, F-3 and, for the check, N2) | The defect was an undefined `<output-dir>` for `workflow`, `research` and file-valued `--output` (round1.md:78-88). AFTER SPEC:62 defines "`--report-dir` for `workflow`, `research` and `tdd`, whose `--output` is a file or does not exist"; SPEC:92 sends the pre-creation workflow STOP contract "into `--report-dir` since no package directory exists yet"; SPEC:90 and SPEC:116 name the flag for tdd and research; SPEC:200 (AC-2.2) now passes `--report-dir <dir>` with tdd's file-valued `--output`. The coordinator can compute the path before dispatch for the three commands the finding named. SPEC:92 column 3 is headed "Report today" (SPEC:82), so the unchanged `.dev/tasks/to-do/<id>/return-contract.yaml` text describes today's file and WC-4 governs the unattended path. |

Regressed: none. Deferred or withdrawn by the reviser: none (the reviser's change set equals the brief's ids; every changed line carries an id tag M1, M2, M4, M5 or M6 except SPEC:90, SPEC:200 and SPEC:92 column 2, which belong to M6 by content).

## Findings on lines changed against the baseline

Scope: =REQUIREMENTS ANALYSIS= and =ARCHITECTURE ANALYSIS= (focus requirements,architecture), limited to the changed lines and the text they depend on. Expert order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin (Gregory and Hightower not engaged for this focus).

=== REQUIREMENTS ANALYSIS ===

### N1 - CRITICAL (blocking) - origin=changed - Wiegers, Crispin, Whittaker (Sequence/Divergence) - AC-0.4 step 4 still cannot pass for the P0 smoke commands
Where it came from: a defect older than the revision (step 4 and the 7.2 YAML assertion are unchanged text, SPEC:183), exposed by the revision's carve-out. It quotes the changed line SPEC:194: "step 4 uses that same file, since the contract arrives in P1 (M2)".
- Stated texts: SPEC:194 (AFTER) makes step 4 run on "the command's existing report file". SPEC:183 (step 4, unchanged) runs `uv run python -c "... d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` and passes only if "both exit 0". The P0 commands' existing report files: troubleshoot `REPORT.md` (SPEC:91; INV-B:242 "`report_path` REPORT.md"; INV-B:249 "`return-contract.yaml` only when `--caller task-unified`"), workflow's contract with `status`, `plan_path`, `reflect_report_path` and no `command` field listed (INV-B:272), adversarial's contract "filename not fixed" (SPEC:83).
- Grading sentence: An implementer who follows the stated text as written runs step 4 of the AC-0.4 live check on troubleshoot's `REPORT.md`, which has no `status` key and no `command` key (it is a markdown report, INV-B:242), so `d['status']` raises and the command exits non-zero; step 4 cannot pass, so AC-0.4 cannot pass, and SPEC:154 ("later phases do not start until the earlier phase's checks ... pass") and SPEC:194 ("a failure here reopens section 1") then fire on a correct run. This is the defect class of M2 at the next step.
- Recommendation (narrowing, no new mechanism): in AC-0.4 say "step 4 is `test -s` on that file only; the YAML assertion applies from P1".
- Priority: High. Quality impact: Testability +2.

### N2 - CRITICAL (blocking) - origin=changed - Wiegers, Adzic, Fowler - AC-1.2 passes `--output <dir>` to `workflow`, whose contract directory is now `--report-dir`
Where it came from: the revision. It changed WC-4 (SPEC:62) and the workflow row (SPEC:92) to `--report-dir` and edited AC-2.2 (SPEC:200) for tdd, and edited AC-1.2 (SPEC:196) for `load` only, leaving its flag text unchanged.
- Stated texts: SPEC:196 (AFTER): "7.2 live check on each P1 command except `load` (M1, M5) with `--unattended --output <dir>`". `workflow` is a P1 command (SPEC:92, 159). SPEC:62: for `workflow` the `<output-dir>` is the `--report-dir` directory; SPEC:92 brief column: "`--handoff none`; `--report-dir <dir>` (P1)", with no `--output` for workflow (INV-B:52, INV-B:272 name no `--output`). SPEC:182-183: steps 3-4 test "the WC-4 contract path".
- Grading sentence: An implementer who follows the stated text as written runs the AC-1.2 live check for `workflow` with `--output <dir>` and no `--report-dir`; by SPEC:62 the contract goes to the `--report-dir` directory, which was not supplied, so the WC-4 contract path that steps 3 and 4 test does not exist for that run (and a post-creation run writes it only under `.dev/tasks/to-do/<id>/`, SPEC:92 column 3); AC-1.2 cannot pass for `workflow`. The reviser fixed the same clash for tdd in AC-2.2 (SPEC:200) but not here.
- Recommendation (narrowing): in AC-1.2 write "with `--unattended` and the command's output flag from section 3 (`--output <dir>`, or `--report-dir <dir>` for workflow)".
- Priority: High. Quality impact: Testability +1.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding on the changed lines. Fowler: adding a separate directory flag for the file-valued cases (SPEC:62) matches the pattern the current /sc:spec-panel definition already uses (`CMD:460`: "`--report-dir <dir>` only (`--output` is file-valued)"), and keeps the one-shared-core-file design (SPEC:52) intact. Newman: the spec now has two directory flag names (`--output`/`--output-dir` and `--report-dir`), chosen per command by prose in WC-4; a per-command flag column in section 3 would make it checkable (Medium, F-3).

=== ADVERSARIAL ANALYSIS (Whittaker, FR-3 template; changed lines only) ===

- A1 (blocking, = N1). I can break this specification by **Sequence Attack**. The invariant at **SPEC:194 with SPEC:183** fails when **step 4 runs on a P0 command whose existing report has no `status`/`command` key**. Concrete attack: before: P0 run of `/sc:troubleshoot "<symptom>"` finishes, `worker_done --report-path .../REPORT.md` sent, steps 1-3 pass; step 4: `yaml.safe_load` of the markdown report returns a string or raises, `d['status']` fails, exit non-zero; after: AC-0.4 red, SPEC:154 blocks P1.
- A2 (blocking, = N2). I can break this specification by **Divergence Attack**. The invariant at **SPEC:196 vs SPEC:62/92** fails when **the P1 command is `workflow`, the one command whose output directory flag differs from `--output`**. Concrete attack: before: `/sc:workflow "<change>" --handoff none --unattended --output D`; after: no file at the WC-4 path `<report-dir>/return-contract.yaml` (no `--report-dir` given); step 4 `test -s` exits 1.
- A3 (Medium, follow-up). I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62** fails when **`--unattended` is given with no directory flag for a command that has more than one candidate flag** (`/sc:tdd "x" --unattended --output f.md` without `--report-dir`). Concrete attack: before: tdd run per SPEC:90 with only `--output`; after: WC-4 has no directory, behaviour unspecified (same gap as round1 W3, round1.md:106, still open and unchanged).

=== GUARD CONDITION BOUNDARY TABLE (re-review: guards on changed lines only) ===
Triggered by the changed guards: the WC-4 directory-flag selection (SPEC:62), the AC-1.1/1.2 population filters (SPEC:195-196) and the AC-0.4 step-3/4 pass conditions (SPEC:194). Nygard built it, Crispin checked completeness, Whittaker attacked entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-4 directory flag | SPEC:62 | Zero/Empty | `--unattended`, no directory flag | unspecified | unspecified (A3) | GAP (Medium: names no wrong outcome without an extra assumption about the command's default) |
| WC-4 directory flag | SPEC:62 | One/Minimal | workflow with only `--report-dir` | true | contract in `--report-dir` (SPEC:92) | OK |
| WC-4 directory flag | SPEC:62 | Typical | analyze with `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| WC-4 directory flag | SPEC:62 | Sentinel Value Match | file-valued `--output` (tdd) | n/a | `--report-dir` required (SPEC:90, 200) | OK |
| WC-4 directory flag | SPEC:62 | Legitimate Edge Case | `init-lite` `--output <file>` (SPEC:87), not in the `--report-dir` list | `--output` taken as directory | contradiction, no AC or phase touches it | GAP (Medium, F-2) |
| AC-1.1 population | SPEC:195 | Zero/Empty | command with no phase in section 3.1 (brainstorm, init-lite: small fix "None") | not P1 | no section asserted | OK (they get no section; Medium note F-4) |
| AC-1.1 population | SPEC:195 | Typical | P1 command | true | section asserted | OK |
| AC-1.1 population | SPEC:195 | Legitimate Edge Case | `load` | excluded | named exception (SPEC:195) | OK |
| AC-1.2 flag | SPEC:196 | Legitimate Edge Case | `workflow` | `--output` passed | contract path undefined | GAP (BLOCKING, N2) |
| AC-0.4 step 3 | SPEC:194 | Typical | P0 command, one `worker_done`, existing report path | true | pass | OK |
| AC-0.4 step 3 | SPEC:194 | Zero/Empty | no `worker_done` | false | fail (step 3 requires exactly one) | OK |
| AC-0.4 step 4 | SPEC:194, 183 | Legitimate Edge Case | existing report is `REPORT.md` | assertion on `status` fails | fail | GAP (BLOCKING, N1) |

Classes left out, with reason: Maximum/Overflow for every row (no count or capacity enters these guards).
FR-8 GAP rows: N1 and N2 name a concrete wrong outcome, so they are blocking; the three others are Medium (follow-up candidates). FR-9 blank behaviours: the two "unspecified" rows, graded Medium. FR-10: every changed guard is enumerated and every input class has a row or a reason above.

## Coverage

Covered: the whole diff (9 hunks, 12 changed lines), all five prior blocking findings M1, M2, M4, M5, M6 re-checked against the AFTER text, the dependencies of the changed lines (SPEC:52, 62, 76, 82-92, 112, 116, 154-162, 182-183, 194-200, 265) and the inventory lines they cite (INV-B:52, 242, 249, 272; INV-A:55). Not covered: the unchanged remainder of the spec (whole-document assurance needs a separate, labelled first review); `cmd/...`, `sk/...` and repository paths outside the workspace (UNVERIFIED). Only `command.md` (CMD) was read outside the spec and inventories.

## Follow-up candidates (Medium and minor; never fail the review, not in the Reviser brief)

- F-1 (Medium, origin=unchanged, round1 FC-class repeat) `/sc:spec-panel` row (SPEC:120, stale): it says "add `--output`; contract", but the current command definition already has a file-valued `--output` and a `--report-dir` plus an `## Unattended mode` section (CMD:22-23, 455-465). An implementer adds a second, directory-valued `--output`. Needs a check of the real file outside the spec text, so Medium.
- F-2 (Medium, origin=unchanged) `init-lite` has `--output <file>` (SPEC:87) and no phase; WC-4's file-valued list (SPEC:62) omits it, and no AC covers it, so it never gets a contract.
- F-3 (Medium, origin=changed) `tdd` and `research` use `--report-dir`, but no row says which phase adds the flag to the command: tdd's small-fix column (SPEC:90) names only the gate change, and the P1 line "output flags for commands that lack one" (SPEC:159) lists neither. Add one clause to the tdd and research rows.
- F-4 (Medium) `brainstorm` and `init-lite` (SPEC:84, 87) have no phase, so no `## Unattended mode` section and no `--unattended` flag is asserted for them anywhere, though SPEC:76 says every changed command gains the section and WC-2/WC-4 are stated for unattended mode.
- F-5 (Medium) round1 notes still open and unchanged: W1 (`partial` undefined), W2 (stale contract after a failed second run), W4 ("refused under `--unattended`" outside WC-2's three resolutions), FC-2 (WC-10 and Agent-tool waits), FC-4, FC-7 (no contract version), FC-9 (absent `~/.claude/WORKER-CONTRACT.md`).
- F-6 (minor) round1 M3 (cli-portify all-blocked versus AC-2.3, SPEC:105, 201) was rejected by the verifier and stays a noted, unactioned item.
- F-7 (minor) the "(M1, M5)"-style finding tags are now embedded in normative spec rows and AC text (SPEC:62, 76, 92, 159, 194-196); they are review-trace residue the next reviser may strip.
- Prompt note (minor): the prompts file's RE-REVIEW section points to a "re-review core below" that the file does not contain; the roles table and bullets were applied instead.

The session that ran this review asks the user once whether to open an issue for the follow-up candidates and creates none without the user's answer.

## Reviser brief

Blocking finding ids: N1, N2. (M1, M2, M4, M5, M6 are resolved; M3 stays a note.)
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings (F-1 to F-7, A3) alone. Do not award yourself a PASS. After this fix cycle the next review is review 3 of 3; a blocker open there is escalated to the user, with no fourth review.

verdict: FAIL
