review: 3 of 3

# Re-review: orca-worker-contract-spec (focus: requirements, architecture)

Short names used for path:line citations below: SPEC = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (candidate), BASE = `.dev/orca-command-refactor/specs/history/spec-v2.md` (baseline), PRIOR = `.dev/orca-command-refactor/review/round2.md`, LINT = `.dev/orca-command-refactor/review/lint-3.md`, INV-A = `.dev/orca-command-refactor/inventory/commands-a.md`, INV-B = `.dev/orca-command-refactor/inventory/commands-b.md`.

candidate: SPEC sha256 5c1ab8696d3015841916a6b721ba37673ca41cc95d7518dd2f44d176aa42898f
baseline: BASE sha256 7c8aa27b2871ce92c01502f179de64ec96be2031fdf14b1198dc4230f55a9adc
prior: PRIOR sha256 d754efa8e5a39192118131ca95e6748f3a94e56086aeb9463825c18f680996fe (header `review: 2 of 3`, so this review is N = 3)
lint: LINT sha256 0f234547c6a9cc90e33eee26c9a0c5c8b42f79878639b7aba463b2bc1f84b593 (`Checks: REF. Findings: 0.`; its own header records the candidate hash 5c1ab869..., which matches SPEC; no lint ids to address)
reviewer model: claude-haiku-5-5 (single reviewer, fresh context for this run)
rules read: `home/.claude/rules/prompts/document_review_loop_prompts.md` read in full; RE-REVIEW prompt followed. `rf-qa.md` (project `.claude/agents/` or `~/.claude/agents/`) is not present in the sandbox, so the Review Loop section 5 rules in `command.md` stand alone. WORKER-CONTRACT.md is not read: `--unattended` is not passed in this run (`command.md` Unattended mode section).
coordinator note: the VERIFY prompt still runs on the open blocking finding N6 before escalation (prompts file, "At review: 3 with an open blocking finding the VERIFY prompt still runs"). This reviewer did not run it; the verifier must be a fresh context.

## Step 1: evidence block

`diff -w BASE SPEC` was run. Roles were fixed by the command (BASE = BEFORE, SPEC = AFTER). The diff has three hunks, at SPEC:158, SPEC:206 and SPEC:207 (baseline lines identical).

BEFORE (baseline), lines starting `<`:

```text
< | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2, 5, 6 and 7 pass, and steps 3 and 4 pass in their P0 form (M2): step 3 checks the outcome against the existing report's status and the report path against the command's existing report, and step 4 is `test -s` on that report. The WC-4 path and YAML field checks are P1 checks (AC-1.2). Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, that `load` has none (M1), and that no section-4 command has one | passes |
```

AFTER (candidate), lines starting `>`:

```text
> | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run two ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none` (adversarial is not a P0 smoke run, M4) | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"` and `/sc:workflow "<small change>" --handoff none`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2, 5, 6 and 7 pass, and steps 3 and 4 pass in their P0 form (M2): step 3 checks the outcome against the existing report's status and the report path against the command's existing report, and step 4 is `test -s` on that report. `/sc:adversarial` is not run in P0 (M4): the spec names no fixed report file for it before P1, because its skill names none (INV-A:35,60), so its direct-route check is AC-1.2, which runs after AC-1.4 fixes the filename. The WC-4 path and YAML field checks are P1 checks (AC-1.2). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in section 3.1, and every section 3.2 command whose Phase column reads P1, except `load`, has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (N1: the P2-P4 commands of section 3.2 get theirs in their own phase, so this test does not check them), that `load` has none (M1), and that no section-4 command has one | passes |
```

Self-check (`grep -nF`, run before the verdict): every AFTER line was found in SPEC at lines 158, 206 and 207, and every BEFORE line was found in BASE at lines 158, 206 and 207. Roles are confirmed as fixed. The text of the unchanged lines the findings below cite was read in SPEC and BASE: SPEC:62 (WC-4), SPEC:83 (adversarial row), SPEC:91-92 (troubleshoot and workflow rows), SPEC:159 (P1 scope), SPEC:194 (7.2 step 3), SPEC:208 (AC-1.2), SPEC:210 (AC-1.4), and the same line numbers in BASE, which the diff shows unchanged.

Empty-diff rule: the diff is not empty, so no prior blocking finding is held open by that rule.

## Prior blocking findings (from PRIOR, `review: 2 of 3`)

PRIOR lists M4 and N1 as the blocking findings (PRIOR:111-116, PRIOR:120-126, PRIOR:160). M3 was rejected at review 2 and is not a prior blocking finding. The other PRIOR findings (M1, M2, M5, M6, M7) were resolved at review 2 and are not open prior blockers. Regression check: no finding PRIOR marked resolved fails again on the candidate.

| id | status | evidence |
|---|---|---|
| M4 | resolved | The reviewer's own recommended option was taken: adversarial is removed from the P0 smoke set (SPEC:158 "(adversarial is not a P0 smoke run, M4)"; SPEC:206 "`/sc:adversarial` is not run in P0 (M4)"). The P0 step-3 and step-4 checks now name only troubleshoot and workflow, whose existing reports are named (SPEC:91, SPEC:92). The adversarial contract check moves to AC-1.2 (SPEC:208). Residual points are in N6 (new, blocking) and N8 (Medium). |
| N1 | resolved | AC-1.1 is now scoped to section 3.1 plus section 3.2 commands whose Phase column reads P1, except `load` (SPEC:207). That matches the P1 section scope for the ten 3.1 commands (SPEC:79) and the P1 gated and ungated 3.2 rows (SPEC:99-103, SPEC:106-108, SPEC:111, SPEC:123). P2-P4 section 3.2 commands are not checked in P1, and the spec says their sections are added in their own phase (SPEC:207 parenthesis). Phase-passing rule (SPEC:167) is unchanged. Residual point is N9 (Medium). |

## Findings on lines changed against the baseline

None of the three changed lines introduces a new blocking finding on its own. The new blocking finding below is origin=unchanged, and it is cited here because a changed line depends on it (SPEC:206, "`AC-1.4` fixes the filename"), as the re-review rule allows.

### N6 (blocking, origin=unchanged, depends on changed SPEC:206): the adversarial contract path is stated two ways

- Quoted text A (unchanged, WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62; the same text is in BASE:62).
- Quoted text B (unchanged, adversarial row): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", with the brief column "`--output <dir>`" (SPEC:83; same in BASE:83).
- Dependent changed line: "its direct-route check is AC-1.2, which runs after AC-1.4 fixes the filename" (SPEC:206). AC-1.4 (SPEC:210) only greps for "one fixed path" and names no path, so the filename fix is the SPEC:83 row, not AC-1.4.
- Also relevant: the 7.2 step 3 check requires the worker's `--report-path` to be "the WC-4 contract path in P1 and later" (SPEC:194), and AC-1.2 runs that check on each P1 command (SPEC:208), and adversarial is a P1 command (SPEC:83, SPEC:159).
- Grading sentence: An implementer who follows the adversarial row (SPEC:83) as written writes the contract to `<dir>/adversarial/return-contract.yaml`, and that is wrong because WC-4 (SPEC:62) requires `<dir>/return-contract.yaml` and the AC-1.2 step-3 check (SPEC:194) compares the report path with the WC-4 path, so the check fails for that build. An implementer who follows WC-4 instead contradicts the row. Both texts are stated, neither needs an assumption, and they name different files for the same command.
- Evidence the contract location is not settled: INV-A:60 says real runs wrote the contract in two different places, and INV-A:35 says the skill names no filename. Brainstorm, by contrast, uses `<output>/return-contract.yaml` (SPEC:84), which agrees with WC-4.
- Why this was not caught at review 2: the defect sits on unchanged lines (SPEC:62, SPEC:83) and was not in the review-2 diff scope. It is recorded here as a severe defect newly found by this review, and it comes from the baseline (BASE:62, BASE:83).
- Recommendation for the author (no reviser brief is issued at review 3): choose one path and make SPEC:62 and SPEC:83 agree, either by naming `<dir>/return-contract.yaml` for adversarial or by stating the adversarial exception in WC-4. Then AC-1.4 should name that path rather than "one fixed path".
- Priority: High. It blocks P1 for adversarial.

## Follow-up candidates (Medium and minor; not blocking; not in any brief)

- N2 (SPEC:159, SPEC:112, SPEC:207; origin=unchanged, still open): what `load` does with the accepted `--unattended` flag is not stated. Medium.
- N3 (SPEC:194, SPEC:206; origin=changed, still open): the P0 "existing report's status" for troubleshoot's `REPORT.md` (SPEC:91) has no stated source. UNVERIFIED whether `REPORT.md` carries a status field (not in the inventories read here). Medium.
- N4 (SPEC:225, SPEC:238, SPEC:241-242; origin=unchanged, still open): the AC-2.2 lead-in defines only blocked and success, so the tasklist row ("none in the row: no gate fires") is not covered, and "unapplied in `git status`" needs a baseline. Medium.
- N5 (SPEC:172-183, SPEC:147, SPEC:150; origin=changed, still open): scan 2 excludes only `WORKER-CONTRACT.md` (SPEC:181), so the routing-guide Orca-section exemption that SA-2 and SA-5 state is a manual line-range comparison. Repo scans are UNVERIFIED here (no `src/` tree in the sandbox). Medium.
- N7 (SPEC:92, SPEC:159, SPEC:208; origin=unchanged): workflow is P1 (SPEC:92), AC-1.2 requires `--output <dir>` for each P1 command (SPEC:208), but workflow's brief passes only `--handoff none` (SPEC:92), its contract today is `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92; INV-B:272), and the P1 scope's general "output flags for commands that lack one" (SPEC:159) is the only place that adds one. Passable, but whether the package path or `<dir>/return-contract.yaml` is "the WC-4 path" for workflow is unstated. Medium.
- N8 (SPEC:206, SPEC:210; origin=changed, new): the M4 text says AC-1.2 "runs after AC-1.4 fixes the filename", but AC-1.4 is a grep check that fixes nothing (the fix is SPEC:83), and the P1 block sets no order between checks. Medium; the fix belongs to N6.
- N9 (SPEC:159, SPEC:60; origin=unchanged, new): the P1 scope says the flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". For gated 3.2 commands the spec does not say whether an accepted flag must fail closed (WC-2, SPEC:60: "never calls `AskUserQuestion`") or stay inert until its phase. No P1 check tests either. Medium.
- N10 (SPEC:206, SPEC:43, SPEC:158; origin=changed, new): the M4 fix moves the only direct-route run for adversarial to P1, although SPEC:43 says P0 closes evidence gap 1.4(1). This follows from the chosen fix and is a sequencing note, not a defect. Medium.
- M3 (PRIOR:85-92): rejected at review 2; noted, unactioned.

## Coverage

- Read in full: SPEC (all 318 lines), BASE (the three diff regions and the rest of the file by diff), PRIOR (all), LINT (all), the review-loop prompts file in home, `command.md`, and `README.md`.
- Read in part: INV-A and INV-B (the adversarial, brainstorm and workflow rows, grepped at INV-A:35,39,60 and INV-B:52,267-272), to check N6 and N7.
- Checked: the diff `diff -w BASE SPEC`, the `grep -nF` self-check on every changed line, the two N6 texts at SPEC:62 and SPEC:83, and the N7 workflow citations.
- Not checked: the repo scans (no `src/` tree), other inventory citations (UNVERIFIED in this review), the rf-qa.md file (not present), and the VERIFY step on N6 (coordinator, fresh context).

## Escalation

verdict FAIL at review 3 of 3. No Reviser brief is issued at review 3 (`command.md` Review Loop, bullet 6). Open blocking finding: N6. The coordinator runs the VERIFY prompt on N6 first, then escalates to the user with the confirmed findings. No fourth review is started.

verdict: FAIL
