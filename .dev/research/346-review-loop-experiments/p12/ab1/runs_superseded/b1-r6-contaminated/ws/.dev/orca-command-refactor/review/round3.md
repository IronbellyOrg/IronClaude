review: 3 of 3

# Re-review report (spec-panel --mode critique --re-review)

command: /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md
reviewer model: claude-sonnet-5-5 (Sonnet 5.5)
review number: prior report `review: 2 of 3` (round2.md:1) plus 1 = 3. The prior report's final line is `verdict: FAIL` (round2.md:142), but the prior is at review 2, not 3, so the cap check (do not review at `review: 3` + FAIL) does not fire and this review runs.
Prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; the file's "re-review core below" does not exist as a section, so its roles table and the Step 1 / review number / self-check bullets were applied). The Review Loop of `command.md` (CMD:256-264) was applied on top.

Roles (fixed by the brief, not by reading order):

| ROLE | FILE | sha256 |
|---|---|---|
| CANDIDATE | .dev/orca-command-refactor/specs/orca-worker-contract-spec.md | 5c2917118a22814ab0c7a7bbdc9726f06dce161ded89ac5b03740fd58e13abc3 |
| BASELINE | .dev/orca-command-refactor/specs/history/spec-v2.md | 51c1db2c9d50566a98e630c6d8b4017397f136684b86e1f54329e02f1d7fd5b1 |
| PRIOR | .dev/orca-command-refactor/review/round2.md | 1688e370910d7125b805c14b5a140fafa659d9cb644ef14b85f11b95fb2f4ba5 |

Baseline check: the BASELINE hash equals the candidate hash recorded in round2.md:15, so the baseline is the text review 2 saw. baseline: present.

Citation key: `SPEC:n` = candidate line n; `BASE:n` = baseline line n; `INV-A:n`, `INV-B:n` = `inventory/commands-a.md`, `commands-b.md` line n; `R2:n` = round2.md line n; `CMD:n` = `command.md` line n. Any `cmd/...` or `sk/...` path cited inside the spec's own rows is not in the workspace: UNVERIFIED by me, taken only through the inventories.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Changed hunks: lines 194 and 196 (same line numbers in both files). Whitespace-only changes: none. Size 58254 -> 58408 bytes (+154), matching revise2.md.

### BEFORE (baseline), lines starting `<`
```text
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-2 and 5-7 pass; step 3 passes when exactly one `worker_done` arrives and its report path is the command's existing report file; step 4 uses that same file, since the contract arrives in P1 (M2). Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (M1, M5) with `--unattended --output <dir>` | all steps pass |
```

### AFTER (candidate), lines starting `>`
```text
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-2 and 5-7 pass; step 3 passes when exactly one `worker_done` arrives and its report path is the command's existing report file; step 4 is `test -s` on that same file only, and its YAML assertion applies from P1, since the contract arrives in P1 (M2, N1). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (M1, M5) with `--unattended` and the command's output flag from section 3 (`--output <dir>`, or `--report-dir <dir>` for `workflow`) (N2) | all steps pass |
```

Self-check run: each BEFORE line (without `< `) was found with `grep -cF` in the baseline (count 1 each); each AFTER line (without `> `) was found in the candidate (count 1 each) and in the baseline 0 times. Roles are not swapped.

## Prior blocking findings (R2:75-87; the verification block R2:2 confirmed N1 and N2, rejected none; M1, M2, M4, M5, M6 were resolved at R2:61-65)

| id | status | compared against AFTER text only |
|---|---|---|
| N1 | resolved | The defect was AC-0.4 step 4 running the YAML assertion (SPEC:183: `d['status']`, `d['command']`) on the command's existing report file, which for troubleshoot is `REPORT.md` and has no such keys (R2:77-78; INV-B:242, 249). AFTER SPEC:194 says "step 4 is `test -s` on that same file only, and its YAML assertion applies from P1". Step 4's first half, `test -s <contract>` (SPEC:183), is the only check run in P0, and a non-empty `REPORT.md` passes it. The step-3 text kept from the M2 fix ("exactly one `worker_done` arrives and its report path is the command's existing report file") is unchanged, so M2 does not regress. SPEC:183 itself is unchanged and still reads as applying to P0-P4 (SPEC:178 header), but AC-0.4 is the per-phase check and states the narrowing, so the two do not contradict for an implementer who reads the AC row (see F-8, Medium). |
| N2 | resolved | The defect was AC-1.2 passing `--output <dir>` to `workflow`, whose WC-4 directory flag is `--report-dir` (R2:84-85; SPEC:62, 92). AFTER SPEC:196 says "with `--unattended` and the command's output flag from section 3 (`--output <dir>`, or `--report-dir <dir>` for `workflow`)". `workflow` gets `--report-dir <dir>`, which is the flag SPEC:62 and SPEC:92 define, so the WC-4 contract path that steps 3 and 4 test exists for it. It matches the tdd fix already in SPEC:200. |

Regressed: none. Earlier resolved blockers re-checked against the AFTER text: M1 (SPEC:76, 159, 195, 196 still say "except `load`"; SPEC:196 keeps "except `load` (M1, M5)"), M2 (SPEC:194 step-3 wording intact), M4 and M5 (SPEC:195 population filter untouched), M6 (SPEC:62, 90, 92, 116, 200 untouched). The diff touches only SPEC:194 and SPEC:196. Deferred or withdrawn by the reviser: none (revise2.md lists N1 and N2, both applied, +60 and +94 bytes, no deletions).

## Findings on lines changed against the baseline

Scope: =REQUIREMENTS ANALYSIS= and =ARCHITECTURE ANALYSIS= (focus requirements,architecture), limited to the changed lines (SPEC:194, 196) and the text they depend on (SPEC:62, 82-92, 159, 178-183, 195, 200). Expert order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin (Gregory and Hightower not engaged for this focus).

=== REQUIREMENTS ANALYSIS ===

No blocking finding. Wiegers/Crispin: the AC-0.4 step 4 pass condition is now decidable for all three smoke commands, because `test -s` needs no key in the file. Adzic example: `/sc:troubleshoot "<symptom>"` finishes, `worker_done --report-path .../REPORT.md` arrives once, `test -s REPORT.md` exits 0, steps 1-3 and 5-7 pass, AC-0.4 is green. Same trace for `/sc:workflow ... --handoff none`: the report is `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), non-empty, passes. For `/sc:adversarial ... --output <dir>` the contract filename is "not fixed" today (SPEC:83); step 3 compares against whatever path the worker reports, so it passes without the filename.

Medium observations on the changed lines are listed under follow-up candidates (F-8, F-9).

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding on the changed lines. Fowler: AC-1.2 now defers the flag name to section 3 per command, which keeps one source of truth for flags (the section 3 rows) instead of one more hard-coded flag in the check table. Newman: the spec still has two directory flag names (`--output`/`--output-dir`, `--report-dir`), chosen by prose in WC-4 (SPEC:62); already noted as R2 F-3, unchanged.

=== ADVERSARIAL ANALYSIS (Whittaker, FR-3 template; changed lines only) ===

- A1 (resolved, was N1). I tried the **Sequence Attack** on SPEC:194 with SPEC:183: run step 4 in P0 on troubleshoot's `REPORT.md`. Before: `REPORT.md` exists and is non-empty, `worker_done` sent. After: `test -s` exits 0, the YAML assertion is not run in P0. The invariant holds.
- A2 (resolved, was N2). I tried the **Divergence Attack** on SPEC:196 against SPEC:62/92: P1 command `workflow`. Before: `/sc:workflow "<change>" --handoff none --unattended --report-dir D`. After: contract at `D/return-contract.yaml`, steps 3 and 4 find it. The invariant holds.
- A4 (Medium, follow-up, origin=changed). **Sentinel Collision / Divergence Attack** on SPEC:196: "the command's output flag from section 3". Concrete attack: P1 commands `cleanup-audit` and `index-repo` have no output flag in their section 3.1 rows (SPEC:84-85: cleanup-audit "Brief must pass" is `--pass <N>`, output dir fixed; index-repo "none"). The text offers `--output <dir>` as the only generic choice. Before: AC-1.2 run for `index-repo`; after: an implementer either passes an `--output` the command does not have or finds no flag to pass and has no `<output-dir>` for WC-4. Which of these the implementer picks needs a guess about what "the command's output flag" means when none is listed, so this is Medium. The same applies to `analyze`, `build`, `design`, `index`, `test` and `business-panel`, whose rows say "add `--output`" or "add a report path" without saying directory or file (SPEC:99-123); SPEC:159 ("output flags for commands that lack one") is the phase that adds them. The gap is older than the revision (the baseline AC-1.2 had the same single `--output <dir>`), and the revision narrowed rather than widened it.

=== GUARD CONDITION BOUNDARY TABLE (re-review: guards on changed lines only) ===
Triggered by the guard in SPEC:196 (which flag is passed per P1 command) and the pass conditions in SPEC:194 (step 3 and step 4 in P0). Nygard built it, Crispin checked completeness, Whittaker attacked entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| AC-1.2 output-flag choice | SPEC:196 | Zero/Empty | P1 command with no output flag in section 3 (`index-repo`, `cleanup-audit`) | no flag to pass | not stated | GAP (Medium: A4; the implementer must guess the flag) |
| AC-1.2 output-flag choice | SPEC:196 | One/Minimal | `workflow` | `--report-dir <dir>` | contract in that directory (SPEC:62, 92) | OK |
| AC-1.2 output-flag choice | SPEC:196 | Typical | `adversarial` with `--output <dir>` | `--output <dir>` | contract in `<dir>` | OK |
| AC-1.2 output-flag choice | SPEC:196 | Sentinel Value Match | file-valued `--output` (`tdd`, not in P1) | n/a | tdd is P2 and covered by SPEC:200 | OK |
| AC-1.2 output-flag choice | SPEC:196 | Legitimate Edge Case | `load` | excluded | named exception (SPEC:196) | OK |
| AC-0.4 step 4 | SPEC:194, 183 | Zero/Empty | existing report file empty | `test -s` false | step 4 fails, AC-0.4 red (intended) | OK |
| AC-0.4 step 4 | SPEC:194, 183 | Typical | troubleshoot `REPORT.md` non-empty | `test -s` true | passes, no YAML assertion in P0 | OK |
| AC-0.4 step 4 | SPEC:194, 183 | Legitimate Edge Case | workflow's existing file is a YAML contract | `test -s` true | passes; its YAML is not asserted in P0 | OK |
| AC-0.4 step 3 | SPEC:194 | Zero/Empty | no `worker_done` | false | fail (exactly one required) | OK |
| AC-0.4 step 3 | SPEC:194 | Typical | one `worker_done`, existing report path | true | pass | OK |

Classes left out, with reason: Maximum/Overflow for every row (no count or capacity enters these guards).
FR-8 GAP rows: one, graded Medium (A4; it names no wrong outcome without a guess about the implementer's choice). FR-9 blank behaviours: the Zero/Empty "not stated" row, graded Medium. FR-10: every changed guard is enumerated, and every input class has a row or a reason above.

## Coverage

scoped PASS: changed lines + prior blockers

Covered: the whole diff (2 hunks, 2 changed lines), both prior blocking findings N1 and N2 re-checked against the AFTER text, the earlier resolved blockers M1, M2, M4, M5, M6 re-checked for regression, and the dependencies of the changed lines (SPEC:62, 76, 82-92, 99-123, 159, 178-183, 195, 200, 2.3 at SPEC:72) and the inventory lines they cite (INV-B:242, 249, 272; INV-A:53-55). Not covered: the unchanged remainder of the spec (whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review); `cmd/...`, `sk/...` and repository paths outside the workspace (UNVERIFIED). Only `command.md` and the prompts file were read outside the spec, the inventories and the review files.

## Follow-up candidates (Medium and minor; never fail the review, not in a Reviser brief)

- F-8 (Medium, origin=changed) SPEC:183 step 4 is still written as the generic check "used by P0-P4" (SPEC:178) and only the AC-0.4 row narrows it for P0. An implementer who builds the 7.2 check from the section 7.2 text alone, without the AC-0.4 row, would run the YAML assertion in P0. Needs a guess that the implementer ignores the per-phase row, so Medium. A one-clause note in step 4 would close it.
- F-9 (Medium, origin=changed) A4 above: AC-1.2 says "the command's output flag from section 3" but `cleanup-audit` and `index-repo` have none, and several P1 rows do not say whether the flag added is a directory.
- F-1 to F-7 from round 2 (R2:126-133) remain open and unchanged by this revision: the stale `/sc:spec-panel` row (SPEC:120) versus the current command (CMD:22-23, 455-465); `init-lite` file-valued `--output` with no AC; `tdd` and `research` `--report-dir` with no phase naming where the flag is added; `brainstorm` and `init-lite` with no phase; round 1 notes W1, W2, W4, FC-2, FC-4, FC-7, FC-9; round 1 M3 (rejected, noted); finding tags such as "(M1, M5)" and now "(N1)", "(N2)" embedded in normative rows (SPEC:194, 196).
- A3 from round 2 (WC-4 with no directory flag, SPEC:62) is still open and unchanged (Medium).
- Prompt note (minor): the prompts file's RE-REVIEW section points to a "re-review core below" that the file does not contain.

The session that ran this review asks the user once per loop whether to open an issue for the follow-up candidates and creates none without the user's answer. This is review 3 of 3 and no blocking finding is open, so no escalation and no fourth review.

verdict: PASS
