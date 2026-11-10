review: 2 of 3

# Spec-panel report, round 2 (re-review): Orca worker contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- CANDIDATE (the `@file`, the revised text under review): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `68ce70455b6b30e6a44dbd6460d0688443a0dcdfe80ef873cfa87d79d9501aee` (285 lines, 58534 bytes)
- BASELINE (`--baseline`, the text before the revision): `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (285 lines, 57763 bytes). It is the same hash that `round1.md:7` records for the file reviewed in round 1, so the baseline is the reviewed text.
- PRIOR (`--re-review`, the previous report): `.dev/orca-command-refactor/review/round1.md`, sha256 `f70b4ef8794a328f9a1f3010f219cf1b09df367d57c08532e0c34bd9639f6b44`. Its header `round1.md:1` reads `review: 1 of 3`, so N = 1 + 1 = 2. Its last line is `verdict: FAIL` at `review: 1`, so the cap check (HALT at review 3 with FAIL) does not apply.
- Hashes taken with `sha256sum` in the sandbox. Reviewer model actually used: claude-sonnet-5-5.
- Prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; `~` is the sandbox `home/`), in order: roles, Step 1 evidence block, review number, self-check, then the brief. The README was read first.
- rf-qa Fix Cycle steps 1-5 (`.claude/agents/rf-qa.md`, then `~/.claude/agents/rf-qa.md`): neither file exists in the sandbox (the sandbox holds no `.claude/` under the workspace and `home/.claude/` holds only `rules/prompts/`), so they are unread. The rules in the command's Review Loop section stand alone and are applied as written.
- Citation shorthand: `SPEC:N` = line N of the CANDIDATE; `BASE:N` = line N of the BASELINE; `PRIOR:N` = line N of `round1.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any `path:line` into the repository outside those files (`cmd/`, `sk/`, `CLAUDE.md`, `EVIDENCE.md`) is UNVERIFIED here: the sandbox holds none of them, and I cite the inventory line that quotes the fact.
- Brief clauses overridden: none. The brief asked for no widening, no regrading of a minor finding and no edit of the candidate.
- Prior verification block: `PRIOR:2` records the coordinator's VERIFY step: B-1, B-2, B-3 confirmed; no rejected id. So all three are prior blocking findings for this re-review.

## Step 1. Evidence block

Roles are fixed as above and were not inferred from reading order. I ran `diff -w BASELINE CANDIDATE` (whitespace ignored). It is not empty: 9 changed lines in 8 hunks, at line 62, 73, 76, 92, 159, 194-196 and 198 (both files have 285 lines and the hunks are one-for-one). `<` lines are copied under BEFORE, `>` lines under AFTER, verbatim.

### BEFORE (baseline)

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

### AFTER (candidate)

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at the contract path: `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`), except for four commands whose section 3.1 row fixes another path (B-1): adversarial, `<output>/adversarial/return-contract.yaml`; tdd and init-lite, whose `--output` is a file, `<file>.return-contract.yaml`; workflow, `.dev/tasks/to-do/<id>/return-contract.yaml` with a generated `<id>`, so its path exists only once the package does (how the worker learns `<id>` is UNVERIFIED), and a workflow STOP before the package exists writes no contract (the worker sends `--outcome failed` with no `--report-path`, WC-5). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists (workflow's pre-creation STOP excepted). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory (for tdd and init-lite, the output file), so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the contract path. Every changed command except `load` (B-2) also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None; a STOP before the package exists writes no contract (WC-4) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; steps 3 and 4 use the command's existing report file in place of the contract, since the contract arrives in P1 (step 3: `--outcome` matches that report's own result, and the report path is that file). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` with `--unattended --output <dir>` | all steps pass |
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path (`<output>/adversarial/return-contract.yaml`) |
```

Self-check before the verdict (commands can be run here): each of the 9 AFTER lines (without its `>`) was searched in the CANDIDATE with a whole-line fixed-string match (`grep -xFf`) and found 9 of 9; the same 9 AFTER lines were found 0 times in the BASELINE. Each of the 9 BEFORE lines (without its `<`) was found 9 of 9 in the BASELINE and 0 times in the CANDIDATE. No quote is missing, so no roles were swapped and Step 1 stands. The two prior-report lines I rely on (`PRIOR:1`, `PRIOR:7`) were read directly.

## Prior blocking findings (re-check against the AFTER text only)

| id | prior status | now | Evidence from the AFTER text |
|---|---|---|---|
| B-1 | blocking, open | **resolved** | WC-4 (SPEC:62) now names the contract path for each command whose location differs: adversarial `<output>/adversarial/return-contract.yaml` (equal to the unchanged row SPEC:83 and to AC-1.4, SPEC:198); tdd and init-lite `<file>.return-contract.yaml`, with the brief stating the output file (SPEC:73) and AC-2.2 (SPEC:200, `/sc:tdd "auth" --unattended --output <file>`) now testable against that path; workflow `.dev/tasks/to-do/<id>/return-contract.yaml` (equal to SPEC:92), with a pre-creation STOP excepted in both SPEC:62 and SPEC:92. That exception matches the inventory, which says the workflow contract is "Not written for pre-creation STOPs" (INV-B:272), and `worker_done` without `--report-path` is allowed ("only when applicable", CAPS:72-74), and WC-5 (SPEC:63) already maps "no report exists" to `--outcome failed`. The rule and the four rows no longer disagree, and 7.2 step 3 ("report path is the WC-4 contract path", SPEC:182) and step 4 (SPEC:183) can pass for the three Step 7.2 commands that B-1 named. Remaining wording points are non-blocking: M-12, N-8, N-10. |
| B-2 | blocking, open | **resolved** | `load` is now excluded in all four places that tested or promised a contract for it: the section 3 lead-in (SPEC:76), the P1 scope (SPEC:159), AC-1.1 (SPEC:195) and AC-1.2 (SPEC:196). They now agree with the load row ("none (see note)", SPEC:112) and the Decision "a report file would be an unrequested addition" (SPEC:265). No other text in the AFTER candidate requires a section or contract for `load` (searched `load` and `every command` in the candidate; AC-1.3, SPEC:197, names "two P1 commands" and is not forced onto `load`). |
| B-3 | blocking, open | **resolved** | AC-0.4 (SPEC:194) now relaxes steps 3 and 4 together: "steps 3 and 4 use the command's existing report file in place of the contract ... (step 3: `--outcome` matches that report's own result, and the report path is that file)". The pass list "steps 1-3 and 5-7" (step 3 included, step 4 not) no longer demands a WC-4 contract from commands that, by SPEC:158, still write none. The "failure reopens section 1" consequence is therefore no longer reachable by a false negative on step 3. Wording points (N-11) are non-blocking. |

No prior blocking finding is `open` or `regressed`. Nothing was deferred or withdrawn by the reviser, and no id needed matching by guess.

## Coverage

Scope of this re-review: the 9 changed lines (8 hunks) and the dependencies they touch, plus the three prior blocking findings. Read in full: the CANDIDATE (285 lines), the PRIOR report (212 lines), the README, the BASELINE only through the `diff -w`, and the inventory lines quoted above. Checked by arithmetic: counts after the revision are 43 = 10 + 27 + 6 (SPEC:76, unchanged); sections: 37 dispatchable commands, 36 once `load` is excluded (SPEC:76, SPEC:159, SPEC:195, SPEC:196 agree); phase slots: P1 = 9 (3.2 commands incl. `load` usage line) + 3 ready-command fixes (adversarial SPEC:83, cleanup-audit SPEC:85, index-repo SPEC:86; workflow dropped from the list, SPEC:92 and SPEC:159 agree) = 12; P2 = 11 + 4 ready (reflect, release-split, tdd, troubleshoot) = 15; P3 = 4; P4 = 3; 12 + 15 + 4 + 3 = 34, plus the 3 ready commands with no phase (brainstorm, init-lite, now workflow) = 37. Not checked: every `cmd/`, `sk/` and repo-file citation (UNVERIFIED, absent from the sandbox); lines the revision did not touch beyond what they depend on; whole-document assurance (see the scoped line below).

## Mandatory output artifacts

### Guard Condition Boundary Table (re-review scope: guards on changed lines only; Nygard builds, Crispin checks completeness, Whittaker attacks)

Guards on changed lines: the WC-4 contract-path rule with its four exceptions (SPEC:62, SPEC:73), the workflow pre-creation exception (SPEC:62, SPEC:92), the `load` exclusion (SPEC:76, SPEC:159, SPEC:195, SPEC:196) and the AC-0.4 relaxation (SPEC:194). The other round 1 guards (G3 to G10) are on unchanged lines and are not re-tabled.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| H1 contract path = passed directory | SPEC:62 | Typical | `--output <dir>` on brainstorm or reflect | true | `<dir>/return-contract.yaml` (SPEC:84, SPEC:88) | OK |
| H1 | SPEC:62, SPEC:83 | Legitimate Edge Case | adversarial, `--output <dir>` | exception branch | `<dir>/adversarial/return-contract.yaml`, same text in the row and in AC-1.4 (SPEC:198) | OK |
| H1 | SPEC:62, SPEC:73, SPEC:200 | Legitimate Edge Case | tdd or init-lite, `--output <file>` | exception branch | `<file>.return-contract.yaml`; brief states the file | OK (N-8: the rows SPEC:87 and SPEC:90 do not themselves carry the path) |
| H1 | SPEC:62, SPEC:92 | Legitimate Edge Case | workflow, package exists | exception branch | `.dev/tasks/to-do/<id>/return-contract.yaml`; how the worker learns `<id>` is flagged UNVERIFIED in the text | OK (N-10) |
| H1 | SPEC:62, SPEC:85, SPEC:86 | Zero/Empty | no directory passed: cleanup-audit (fixed output dir, brief passes `--pass <N>` only) and index-repo (no output flag, location "implied", INV-A:53) | neither branch | unspecified: the rule says "the directory the coordinator passed" and none is passed; neither command is among the "four commands" | GAP (M-12, Medium) |
| H1 | SPEC:62, SPEC:107, SPEC:108, SPEC:115, SPEC:120 | Sentinel Value Match | `--output` or "output path" added to document, explain, recommend, spec-panel with directory-or-file form not stated (spec-panel's `--output` does not exist yet, INV-B:182) | the default branch (directory) applies by the letter | not stated whether each added flag is a directory or a file; a file-valued flag cannot hold `<output-dir>/return-contract.yaml` | GAP (M-12, Medium) |
| H2 workflow package exists | SPEC:62, SPEC:92 | Zero/Empty | STOP before the package exists | false | no contract; `--outcome failed`, no `--report-path` (WC-5, SPEC:63; CAPS:72-74; INV-B:272) | OK (N-10: the "first sentence states the report's status" rule has no report to quote) |
| H2 | SPEC:62 | One/Minimal | failure after the package exists | true | contract written with `status: failed` ("written on every post-creation outcome", INV-B:272) | OK |
| H3 `load` excluded from the contract tests | SPEC:76, 159, 195, 196 | Zero/Empty | `load` | excluded | no section, no contract, usage-line fix only (SPEC:112, SPEC:265) | OK |
| H3 | SPEC:195 | Typical | any other 3.1/3.2 command | included | section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` | OK (the P1-versus-later-phase reading of "every command" is M-4, carried) |
| H3 | SPEC:112, SPEC:195 | Legitimate Edge Case | another command with "none" in the Report column | included | none exists: every 3.1 row names a report (SPEC:84-92) and every other 3.2 row names a contract or an output path (SPEC:99-125) | OK |
| H4 AC-0.4 relaxation | SPEC:194 | Typical | troubleshoot: existing report `REPORT.md` (SPEC:91) | relaxed | step 3 path = that file; step 4 not in the pass list | OK (N-11: "that report's own result" has no defined source for a markdown report) |
| H4 | SPEC:194 | Legitimate Edge Case | workflow: existing contract 1.1 (`status`, `plan_path`, `reflect_report_path`, INV-B:272) | relaxed | step 3 outcome can be read from `status`; the step 4 assertion on `command` is not required (4 is outside the pass list) | OK |
| H4 | SPEC:194 | Legitimate Edge Case | adversarial: "contract, but filename not fixed" before P1 (SPEC:83) | relaxed | the report path is the file the worker actually reports | OK |

Omitted input classes: H1 One/Minimal and Maximum (a path rule has no cardinality); H2 Maximum and Sentinel (a package either exists or not); H3 One/Minimal, Maximum and Sentinel (a set membership on one command); H4 Zero/One/Maximum/Sentinel (a phase flag). FR-10: every guard on a changed line is enumerated and every class has a row or a reason, so synthesis was not blocked. FR-8/FR-9: the two GAP rows are graded under the findings below; neither names a concrete wrong outcome without a guess, so both are Medium (M-12), not blocking.

### Pipeline Dimensional Analysis (Fowler leads, Whittaker attacks; changed counts only)

The count flow of PRIOR:73-88 still triggers FR-17. The revision changed two counts and both conserve:

```text
[Inventory 43, SPEC:76] --> ready 10 | needs change 27 | coordinator-only 6
   needs-change section-and-contract set:   27 - load (SPEC:76,159,195,196) = 26;  with the 10 ready = 36 consumers of AC-1.1/AC-1.2
   ready-command P1 fixes:  4 -> 3 (adversarial, cleanup-audit, index-repo; workflow dropped, SPEC:92 = SPEC:159)
   phase slots: P1 12 + P2 15 + P3 4 + P4 3 = 34; phaseless ready (brainstorm, init-lite, workflow) = 3;  34 + 3 = 37 incl. load
   AC-1.1 asserts 36 sections in the P1 test; 36 includes P2-P4 commands <-- carried M-4 (Medium), not a new mismatch
```

No new count divergence. The one carried divergence (P1 test over all 36 versus the per-row phases) is graded as in PRIOR:88 and PRIOR:139: it needs a guess about which phase reading an implementer picks, so it stays Medium (M-4).

## === REQUIREMENTS ANALYSIS ===

No new blocking finding. Findings on lines changed against the baseline (each with origin):

- **M-12 (Medium, origin=changed). WC-4's "four commands" exception list is not exhaustive for commands whose output is a file or is not passed.** WC-4 (SPEC:62) lists four exceptions and otherwise defines the contract as `<output-dir>/return-contract.yaml` in "the directory the coordinator passed". Rows the B-1 fix did not name have no passed directory or no stated form: cleanup-audit "output dir is fixed" and the brief passes `--pass <N>` only (SPEC:85; INV-A:42); index-repo "State the output location" (SPEC:86; INV-A:53, location "implied, UNVERIFIED"); document "require an explicit output", explain "write the explanation to a file", recommend "write the handoff envelope to a file", spec-panel "add `--output`" (SPEC:107, SPEC:108, SPEC:115, SPEC:120; INV-B:182 says no `--output` exists yet). Grading sentence: an implementer who follows WC-4 for cleanup-audit builds a contract with no defined location (no directory is passed, the output directory is fixed), or, for a new file-valued `--output` on spec-panel, `<file>/return-contract.yaml`, and that is wrong because the coordinator cannot open it; but the text never says the new flags are file-valued, and the fixed directory of cleanup-audit is a natural reading, so the sentence needs a guess, hence Medium, a warning under `follow-up candidates`. This is the same class as the prior M-2 (a) (PRIOR:137) and as the part of B-1 the reviser could not close without touching rows B-1 did not name. Expert: Wiegers (consistency), Whittaker (Zero/Empty, Sentinel Collision). Recommendation (not for the reviser brief): one clause in WC-4 or a column in section 3 stating each command's contract path. Priority: Medium.
- **M-4 (Medium, carried, origin=changed line quoted).** AC-1.1 (SPEC:195) and the P1 scope (SPEC:159) now read "every command in sections 3.1-3.2 except `load`" (36 commands, see the pipeline analysis), while section 3 puts the gate conversion of 15 of them in P2-P4 (SPEC:160-162) and D3 (a) leaves pr-submit unchanged (SPEC:240). The revision removed `load` only. Whether the P1 test is meant to cover the later-phase commands (flag and a no-op section in P1, gates later) or only the P1 rows is a reading the text allows both ways, so it stays Medium. Quote of the changed line it depends on: SPEC:195 and SPEC:159. Unchanged otherwise from PRIOR:139.
- **N-8 (minor, origin=changed).** WC-4 says the four commands' "section 3.1 row fixes another path (B-1)" (SPEC:62), but the tdd row (SPEC:90) and init-lite row (SPEC:87) name no contract path; only SPEC:62, SPEC:73 and AC-2.2 (SPEC:200) do, and AC-1.4 (SPEC:198) checks adversarial and workflow only. The path is defined once in WC-4, so no implementer gets a wrong result.
- **N-9 (minor, origin=unchanged, depends on changed row SPEC:92).** SA-4 (SPEC:149) still lists "adversarial and workflow contract gaps" among the section 3 defect fixes; row SPEC:92 now says "None" for workflow. This only permits a non-edit.
- **N-10 (minor, origin=changed).** The WC-4 heading still says "known before dispatch" (SPEC:62) while the workflow exception says the path "exists only once the package does"; the worker's way to learn `<id>` is marked UNVERIFIED inside WC-4 but is absent from the section "UNVERIFIED items" list (SPEC:270-285); and WC-5's "first sentence of the body states the report's status and verdict" (SPEC:63) has no report in the pre-creation STOP case. AC-0.4 runs workflow at P0 (SPEC:194), so the gap is exercised.
- **N-11 (minor, origin=changed).** AC-0.4 step 3 now says the outcome "matches that report's own result" (SPEC:194), but troubleshoot's existing report is a markdown `REPORT.md` (SPEC:91) with no stated status field. The step-4 YAML assertion (SPEC:183) is outside the pass list, so no check fails.

## === ARCHITECTURE ANALYSIS ===

- **Fowler (lead).** Putting the four path exceptions into the single requirement WC-4 keeps the coordinator's only read path in one place; a per-command column would be cleaner (M-12) but is not required. The `load` exclusion removes a command from the contract boundary without touching other commands. Pipeline findings: see the Pipeline Dimensional Analysis.
- **Newman (evolution).** `<file>.return-contract.yaml` differs from the shared name `return-contract.yaml`; the P1 test asserts the substring `return-contract.yaml` (SPEC:195), which both forms contain. The carried N-3 (no schema version, PRIOR:151) is untouched.
- **Hohpe (messaging).** `worker_done` with `--outcome failed` and no `--report-path` is a valid message (CAPS:72-74), and the workflow pre-creation case now uses it consistently with WC-5.
- **Nygard (failure modes).** The P0 gate is no longer self-contradictory (B-3 resolved): a failure at step 3 can now only come from the worker, not from a missing contract. The carried M-1 (stale contract on retry), M-3 and M-8 are on unchanged lines and not reopened.
- **Whittaker (adversarial, changed lines only).** I tried each attack on the changed text. Divergence: `/sc:adversarial --compare a.md b.md --output out/ --unattended` now yields one path (`out/adversarial/return-contract.yaml`) in SPEC:62 and SPEC:83, so the round 1 attack fails. Zero/Empty: `/sc:tdd "auth" --unattended --output docs/TDD_AUTH.md` gives `docs/TDD_AUTH.md.return-contract.yaml`; the round 1 attack fails, but `/sc:cleanup-audit --pass 1 --unattended` (no directory) is the surviving case (M-12). Sequence: a workflow STOP after the package directory exists but before the worker learns `<id>` would send `--outcome failed` with no path although a contract may exist (N-10, flagged UNVERIFIED in the text and exercised by AC-0.4). Accumulation: two tdd workers with `--output docs/a.md` and `docs/b.md` get distinct contracts (an improvement over a shared directory). Sentinel Collision: a `--output` file already named `x.return-contract.yaml` is not credible. No attack breaks a changed line with a concrete wrong outcome.

## Quality metrics (0-10)

Clarity 8, Completeness 7, Testability 7, Consistency 7. Overall 7.25 (was 6.75 in round 1: the three contradictions are closed).

## Follow-up candidates (Medium and minor; none triggers a revision)

The session that ran this review has no user channel (the README forbids opening a local question prompt), so the list is only recorded and no issue is created.

- Medium, new or changed in this round: M-12 (above).
- Medium, carried from PRIOR with the text untouched by the revision unless stated: M-1, M-2 (part (a) overlaps M-12), M-3, M-4 (above, changed line quoted), M-5, M-6, M-7, M-8, M-9, M-10, M-11 (PRIOR:136-145).
- Minor: N-1 to N-7 carried (PRIOR:149-155; none is made worse by the revision); new N-8, N-9, N-10, N-11 (above).

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review: 2 of 3
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, newman, hohpe, whittaker]
  focus_areas: [requirements, architecture]
quality_assessment: {overall_score: 7.25, clarity: 8, completeness: 7, testability: 7, consistency: 7}
prior_blocking:
  - {id: B-1, status: resolved}
  - {id: B-2, status: resolved}
  - {id: B-3, status: resolved}
critical_issues: []
follow_up_candidates:
  medium: [M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12]
  minor: [N-1, N-2, N-3, N-4, N-5, N-6, N-7, N-8, N-9, N-10, N-11]
```

scoped PASS: changed lines + prior blockers

This is a scoped result: the 9 changed lines and the three prior blocking findings were re-checked. Whole-document assurance would need a separate, labelled first review, whose blockers would be escalated to the user and would never start a fourth review.

## Reviser brief

No blocking finding id is open (B-1, B-2 and B-3 are resolved; no new blocking finding). Nothing is to be revised, and Medium and minor findings are not to be touched. Contract for any reviser (restated from the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id.

verdict: PASS
