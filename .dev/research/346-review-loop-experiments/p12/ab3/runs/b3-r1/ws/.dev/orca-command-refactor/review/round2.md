review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md

```yaml
specification_review:
  mode: critique
  re_review: true
  focus_areas: [requirements, architecture]
  candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  candidate_sha256: f3f06d442b7ecafec248d6a15af6b7f95431da195ed53de987f98ee1119f1751
  baseline: .dev/orca-command-refactor/specs/history/spec-v1.md
  baseline_sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
  prior: .dev/orca-command-refactor/review/round1.md
  prior_sha256: 1c80b8433cd2fec232fd1322450892d45b561149dde7ab9174d93cbb9e4afc5d
  reviewer_model: claude-sonnet-5-5 (Sonnet 5.5)
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker]
  coverage: "scoped PASS: changed lines + prior blockers"
```

## Header record

- Prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing). Roles fixed by the command line: CANDIDATE = the `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`. No role was inferred from reading order.
- Review number: the prior report's first line is `review: 1 of 3` (`round1.md:1`) and its last line is `verdict: FAIL` (`round1.md:223`), so N = 2. The prior is not at `review: 3`, so the halt rule did not fire.
- sha256 values above were taken with `sha256sum` in this run. The baseline hash equals the `candidate_sha256` recorded in the prior report (`round1.md:10`), so the baseline is the text that round 1 reviewed. Sizes: baseline 57763 bytes, candidate 58895 bytes (`wc -c`), net +1132, matching `revise1.md` byte accounting.
- Brief clauses overridden: none. The brief asks only for the RE-REVIEW prompt and this report.
- Citation forms: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `R1:N` = line N of `review/round1.md`; `REV:N` = `review/revise1.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. A citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, Orca internals, `EVIDENCE.md`, `sk/...` or `cmd/...` that no inventory file quotes is UNVERIFIED here (no such file is in the sandbox).
- The check procedure "steps 1-5 of the Process of the Fix Cycle phase in `.claude/agents/rf-qa.md`" (command Review Loop bullet 5): that file is not in the sandbox, so it was not read. The rules of the command section stand alone and were applied; the rf-qa steps are UNVERIFIED.
- Process disclosure: during this run I wrote one scratch file (a saved diff) to the session scratchpad directory, which is outside the sandbox directory named in the task. Another process overwrote it with different content, so I discarded it and redid every diff check below from the live files with the sandbox-internal `diff` pipe. Nothing in this report depends on that file. I did not delete it, because it is no longer certain to be mine alone.

## Step 1: evidence block

Command run: `diff -w BASELINE CANDIDATE` (`specs/history/spec-v1.md` against `specs/orca-worker-contract-spec.md`). Result: 14 hunks, 17 changed lines (17 `<`, 17 `>`), all in table rows or paragraphs; no whitespace-only hunk. Line numbers did not move (285 lines before and after). The lines below are copied from the diff output; long table rows are shown whole where the change is inside a cell and the changed span is quoted in bold-free text after the line number.

### BEFORE (baseline, lines starting `<`) and AFTER (candidate, lines starting `>`)

Each pair is the same line number in both files (`BASE:N` and `SPEC:N`).

1. Line 62, WC-4.
   - BEFORE: `... In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). ... It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. ...` and the title `**One report file, known before dispatch, written on every outcome.**`
   - AFTER: title `**One report file, known before dispatch (workflow: after the run), written on every outcome.**`; `In unattended mode the command writes `return-contract.yaml` into its report directory: the directory passed as `--output-dir` or as a directory-valued `--output`; the directory that holds the file when `--output` is a file (tdd, init-lite); or, for a command with no such flag, the directory its section 3.1 row names.` and `... including stops before any other output exists, except a workflow stop before its package is created: no directory exists, so it writes none and WC-5 maps it to `failed`.`
2. Line 73, section 2.3.
   - BEFORE: `the output directory, so the report path is known before dispatch (WC-4);`
   - AFTER: `the output directory, so the report path is known before dispatch (WC-4; workflow's package directory is generated, so its path is known only after the run);`
3. Line 76, section 3 intro.
   - BEFORE: `"Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1).`
   - AFTER: `"Contract" means the WC-4 file `return-contract.yaml` in the report directory. Every changed command except `load` also gains the `## Unattended mode` section (section 2.1) and the `--unattended` flag, in the phase section 6 lists it, not earlier.`
4. Line 83, adversarial row, "Other required change".
   - BEFORE: `Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)`
   - AFTER: `Fix the contract filename to `<output>/adversarial/return-contract.yaml`, its WC-4 report directory (P1)`
5. Line 85, cleanup-audit row.
   - BEFORE: `Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1)`
   - AFTER: `Name the `--pass all` final report; the report directory is the fixed `.claude-audit/`, so the contract is `.claude-audit/return-contract.yaml` and one audit per worktree runs at a time (WC-11) (P1)`
6. Line 86, index-repo row.
   - BEFORE: `State the output location (P1)`
   - AFTER: `State the output location; the contract goes beside `PROJECT_INDEX.md` (P1)`
7. Line 87, init-lite row.
   - BEFORE: `| init-lite | `--output <file>` | ...`
   - AFTER: `| init-lite | `--output <file>` (contract goes in that file's directory) | ...`
8. Line 90, tdd row.
   - BEFORE: `... `--output <file>` | the TDD at `--output` | ...`
   - AFTER: `... `--output <file>` (contract goes in that file's directory) | the TDD at `--output` | ...`
9. Line 92, workflow row, "Small fix (phase)".
   - BEFORE: `Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1)`
   - AFTER: `None: a stop before the package exists writes no contract (`sk/sc-workflow-protocol/refs/return-contract.md:39`), so WC-5 maps it to `failed`; `<id>` is generated, so the path is known only after the run`
10. Line 149, SA-4.
    - BEFORE: `(roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line)`
    - AFTER: `(roadmap and validate-roadmap drift, validate-tests target, adversarial contract gap, explain tools, business-panel frontmatter, load usage line)`
11. Line 159, P1 row.
    - BEFORE: scope `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); ...`; commands `analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow`
    - AFTER: scope `... the `--unattended` flag on the 14 commands of the flag set in the next column; every other command in sections 3.1 and 3.2 gets it in the phase that lists it, with its gate conversion, never earlier; ...`; commands `Flag set (14): analyze, build, business-panel, design, document, explain, index, test, adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow; fixes to adversarial, cleanup-audit, index-repo; load: Usage-line fix only, no flag or Unattended section`
12. Line 176, AC-C5.
    - BEFORE: `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'` ... `prints nothing: edits are additive`
    - AFTER: `git diff --numstat master...HEAD -- src/superclaude/commands/<name>.md | awk '$2 != 0'` ... `prints nothing: column 2 is the deleted-line count, so no line was deleted and edits are additive`
13. Line 193, AC-0.3.
    - BEFORE: `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md | grep -E '^-[^-]'` ... `prints nothing: no existing routing row changed (SA-5)`
    - AFTER: `git diff --numstat master...HEAD -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` ... `prints nothing: no line deleted, so no existing routing row changed (SA-5)`
14. Line 195, AC-1.1.
    - BEFORE: `the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one`
    - AFTER: `the test asserts that every command in the P1 flag set has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that neither `load` nor any section-4 command has one`
15. Line 196, AC-1.2.
    - BEFORE: `7.2 live check on each P1 command with `--unattended --output <dir>``
    - AFTER: `7.2 live check on each command in the P1 flag set with `--unattended --output <dir>``
16. Line 198, AC-1.4.
    - BEFORE: `... and the workflow return-contract ref` / pass: `adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs`
    - AFTER: `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` / pass: `adversarial names one fixed path`
17. Line 200, AC-2.2.
    - BEFORE: pass condition `worker_done --outcome failed`; contract `status: blocked` ...
    - AFTER: pass condition `worker_done --outcome failed`; contract (in the report directory; for tdd, the directory of `<file>`) `status: blocked` ...

### Self-check (roles)

Run with an exact-line membership test of every `>` line (without its marker) against the candidate and every `<` line against the baseline: all 17 AFTER lines were found in the candidate at the same line numbers (62, 73, 76, 83, 85, 86, 87, 90, 92, 149, 159, 176, 193, 195, 196, 198, 200), and none of them occurs in the baseline; all 17 BEFORE lines were found in the baseline at those same numbers, and none of them occurs in the candidate. Roles are not swapped. The diff is not empty, so no prior blocking finding is open by default.

The recorded claim in `REV:61` ("17 lines changed") matches the 17 changed lines found here. The byte claim (57763 to 58895, +1132) matches `wc -c`. The per-finding added and deleted split in `REV:21-28` was not re-derived (it depends on a hand split, `REV:19`) and carries no weight in the verdict.

## Prior blocking findings

| id | prior grade | status | one-line basis |
|---|---|---|---|
| F-01 | CRITICAL | resolved | WC-4 no longer builds `<file>/return-contract.yaml`; every row the finding named now has a path rule (`SPEC:62`, `SPEC:73`, `SPEC:83-92`, `SPEC:200`). One inherited wording conflict remains for adversarial and is graded Medium (M-15). |
| F-02 | CRITICAL | resolved | P1 now ships the flag only on a named 14-command set; the 22 gated or later commands get it with their phase (`SPEC:159`, `SPEC:76`, `SPEC:195`). |
| F-03 | MAJOR | resolved | The deleted-line check now uses `--numstat` column 2; reproduced below. |
| F-04 | MAJOR | resolved | `load` is out of the P1 flag set, the section 3 intro, AC-1.1 and AC-1.2, and agrees with its row and Decision (`SPEC:112`, `SPEC:265`). |

### F-01 resolved (decided by comparing the defect with the AFTER text only)

The round 1 defect (`R1:53-61`) was that WC-4 put the report at `<output-dir>/return-contract.yaml` with `<output-dir>` conflating a file and a directory, so for `--output <file>`, a fixed directory, or a generated directory the stated path could not exist.

AFTER text, case by case:
- File-valued `--output` (tdd, init-lite): the contract goes in "the directory that holds the file" (`SPEC:62`), repeated in both rows (`SPEC:87`, `SPEC:90`). `<file>/return-contract.yaml` is no longer produced by the text.
- Fixed directory: cleanup-audit names `.claude-audit/return-contract.yaml` (`SPEC:85`; the fixed `.claude-audit/` is from `INV-A:42`); index-repo names "beside `PROJECT_INDEX.md`" (`SPEC:86`; `INV-A:53` says the location is implied, repo root UNVERIFIED, and the row's own fix is "State the output location"). WC-4's third clause sends a command with no output flag to "the directory its section 3.1 row names" (`SPEC:62`), so the chain is closed.
- Generated directory: workflow is excepted explicitly (`SPEC:62`, `SPEC:73`, `SPEC:92`); the pre-creation stop writes no contract, matching the inventory ("Not written for pre-creation STOPs", `INV-B:272`, citing `refs/return-contract.md:39`, UNVERIFIED here). WC-5 already maps "no report exists" to `failed` (`SPEC:63`), so the outcome is defined. The unwritable "write the contract for pre-creation STOPs" instruction is gone from the row and from AC-1.4 (`SPEC:198`) and SA-4 (`SPEC:149`).
- AC-2.2 (`SPEC:200`) now says where the `blocked` contract is, so the tdd example (`/sc:tdd "auth" --unattended --output <file>`) can be run.
- The finding's recommended `--report-dir` flag was not added (`REV:51`); it was a recommendation, not a stated requirement, and the defect is repaired without it.

No wrong outcome remains that the stated text forces. One residual wording conflict (adversarial) is graded Medium below.

### F-02 resolved

The round 1 defect (`R1:87-90`) was that P1 shipped the flag on 37 commands while 19 of them had gate conversions in later phases, so an implementer who stopped after P1 had accepted-but-inactive gates (auggie-review posting, post-release prompts).

AFTER text: P1 delivers the flag on 14 named commands only (`SPEC:159`), and "every other command in sections 3.1 and 3.2 gets it in the phase that lists it, with its gate conversion, never earlier" (`SPEC:159`, repeated in `SPEC:76`). I checked the 14 against the rows:
- 8 from section 3.2 with phase P1 and no outward default: analyze, build, business-panel, design, document, explain, index, test (`SPEC:99-123`, phase column P1; `load` is the ninth P1 row and is excluded).
- 6 from section 3.1 with no `--unattended` gate to convert: adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow (`SPEC:83-92`; the "Small fix" cells name no gate for any of them).
- The 22 others are listed in P2 (15), P3 (4), P4 (3) at `SPEC:160-162`, which reconciles with the 27 in section 3.2 and the 10 in section 3.1 (see the Quantity Flow Diagram).
So after P1 no command that has a default-on gate accepts `--unattended`; `/sc:auggie-review --unattended` and `/sc:post-release --unattended` are not accepted until their phases, and the sequence attack of `R1` W-2 has no stated path left. The reviewer's alternative (refuse until the phase) was not used, which the finding allowed ("or state that...", `R1:90`).

### F-03 resolved

The round 1 defect (`R1:131`, G8 row) was that `git diff -U0 ... | grep -E '^-[^-]'` cannot see a deleted markdown bullet (shown as `-- ...`) or a deleted `---` line (shown as `----`). AFTER text in AC-C5 and AC-0.3 (`SPEC:176`, `SPEC:193`) uses `git diff --numstat ... | awk '$2 != 0'`; column 2 of `--numstat` is the deleted-line count.

Reproduced in this run with `git diff --no-index` on process-substitution inputs (git 2.43.0, no file written):
- A text with a `---` line, a second `---` line and a `- Will Not: push` bullet deleted: the new check printed `0	3	...` (one row, 3 deleted lines); the old filter printed nothing. The old defect is real and the new check closes it.
- A text whose only change is a modified Usage line: the new check printed `1	1	...`; the old filter would also print it.
The check is a pure additive-edit detector as described. Whether Usage-line edits should be allowed is the separate Medium M-14 of round 1; it is unchanged here (see follow-up candidates).

### F-04 resolved

The round 1 defect (`R1:69-75`) was that `load` was both "no report, usage line only" (`SPEC:112`, `SPEC:265`) and a member of the P1 "every command" sets that AC-1.1 required to carry an Unattended section naming `return-contract.yaml`. AFTER: `load` is excluded in the section 3 intro (`SPEC:76`: "Every changed command except `load`"), the P1 commands cell ("load: Usage-line fix only, no flag or Unattended section", `SPEC:159`), AC-1.1 ("neither `load` nor any section-4 command has one", `SPEC:195`) and AC-1.2 (the P1 flag set excludes it, `SPEC:196`). The unchanged row (`SPEC:112`: report "none (see note)", phase "P1 (usage line only)") and Decision (`SPEC:265`: "a report file would be an unrequested addition") now agree with those texts. `SA-4` still lists the `load` usage line as a defect fix (`SPEC:149`), consistent with the row. No remaining text requires `load` to carry the section or the flag (searched `SPEC` for "load"; the other hits are `SPEC:139` and `SPEC:265`, which say it is used inside a brief).

## Re-review findings on changed lines

No new or regressed blocking finding. Re-review findings, each with an id in this table (all Medium, so none appears in the Reviser brief; ids M-01 to M-14 belong to round 1 and are carried by reference only):

| id | origin | severity (graded by consequence) | one line |
|---|---|---|---|
| M-15 | changed | Medium | WC-4's directory rule and the adversarial row name different directories |
| M-16 | changed | Medium | AC-1.2 gives every flag-set command `--output <dir>` although init-lite takes a file and cleanup-audit and index-repo take no output flag |
| M-17 | changed | Medium | WC-4 does not say the command creates the report directory when it does not exist yet |

Regression scan: no prior-report finding marked resolved exists (round 1 had none), so no `regressed` entry is possible. The text outside the 14 hunks is unchanged and was not re-reviewed (`origin=unchanged`).

## Guard Condition Boundary Table (guards on changed lines only)

Changed-line guards: the WC-4 report-directory selection and its workflow exception (`SPEC:62`), the P1 flag-set membership (`SPEC:159`, `SPEC:195`, `SPEC:196`), and the `--numstat` filter (`SPEC:176`, `SPEC:193`). All cells filled; every guard enumerated (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| H1 WC-4 report directory | SPEC:62 | Typical | `--output <dir>` (brainstorm, `SPEC:84`) | directory-valued branch | `<dir>/return-contract.yaml` | OK |
| H1 | SPEC:62, SPEC:87, SPEC:90 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | file branch | contract in the file's directory | OK |
| H1 | SPEC:62, SPEC:85-86 | Zero/Empty | no output flag (cleanup-audit, index-repo) | third branch | the row names `.claude-audit/` and "beside `PROJECT_INDEX.md`" | OK |
| H1 | SPEC:62, SPEC:83 | Legitimate Edge Case | `--output <dir>` for adversarial | directory-valued branch gives `<dir>/`, the row gives `<dir>/adversarial/` | two stated directories | GAP (M-15, Medium) |
| H1 | SPEC:62 | Legitimate Edge Case | report directory does not exist when the command stops at a gate (tdd with `--output .dev/out/TDD.md`, `.dev/out/` absent) | none | creation of the directory not stated | GAP (M-17, Medium) |
| H2 workflow exception | SPEC:62, SPEC:73, SPEC:92 | Legitimate Edge Case | workflow stops before its package exists | no directory | no contract; WC-5 gives `failed` (`SPEC:63`) | OK |
| H2 | SPEC:62 | Sentinel Value Match | workflow stop after the package exists | contract written (`INV-B:272`) | stated | OK |
| H3 P1 flag-set membership | SPEC:159 | Typical | analyze (P1, no gate) | in set | flag and section land in P1 | OK |
| H3 | SPEC:159, SPEC:76 | Legitimate Edge Case | gated command in P2 to P4 (for example auggie-review) | not in set | flag lands with its phase | OK |
| H3 | SPEC:159, SPEC:195 | Sentinel Value Match | `load` | excluded everywhere | no flag, no section | OK |
| H3 | SPEC:196 | Legitimate Edge Case | init-lite, cleanup-audit, index-repo in the AC-1.2 run with `--output <dir>` | init-lite's `--output` is a file; the other two have no output flag | the criterion does not say which command line to use per command | GAP (M-16, Medium) |
| H4 additive-edit filter | SPEC:176, SPEC:193 | Typical | modified prose line | `1 1` row printed | caught | OK |
| H4 | SPEC:176, SPEC:193 | Sentinel Value Match | deleted `---` line and deleted `- Will Not: push` bullet | `0 3` row printed (reproduced) | caught | OK |
| H4 | SPEC:176 | Legitimate Edge Case | a Usage line that gains a flag | `1 1` row printed | not allowed by AC-C5; SA-4 allows "new flags" | GAP (M-14, carried, Medium) |

Classes left out, with reason: H1 One/Minimal and Maximum (no counter or size is involved); H2 Zero/Empty (no input); H3 Zero/Empty (an empty flag set cannot occur: 14 names listed); H3 Maximum (the set is a fixed list); H4 Zero/Empty (an empty diff prints nothing and passes, which is correct); H4 Maximum (a very large diff prints rows, no limit relevant).

FR-8 and FR-9 grading: none of the three GAP rows is blocking. M-15 needs the reader to pick one of two readings (the row's specific path or WC-4's general rule), so it is a guess, not a forced wrong outcome. M-16 and M-17 depend on how a command or tester fills a gap (the section 3 rows and 2.3 already direct the tester to the exact command line, `SPEC:73`). M-14 is the round 1 Medium, unchanged.

## Quantity Flow Diagram (FR-21)

```text
[inventories: 21 (INV-A:3) + 22 (INV-B:3) = 43 commands]
   --> [classification, SPEC:76]  10 ready (3.1) + 27 needs change (3.2) + 6 coordinator-only (section 4) = 43   (conserved)
   --> [3.1 + 3.2 = 37 commands that can receive --unattended]
          |-- load: 1, usage-line fix only, no flag, no section            (SPEC:112, SPEC:159, SPEC:195)
          |-- P1 flag set: 14 = 8 (3.2 P1 rows) + 6 (3.1: adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow)   (SPEC:159)
          |-- later phases: 22 = P2 15 (11 from 3.2 + reflect, release-split, tdd, troubleshoot) + P3 4 + P4 3   (SPEC:160-162)
   --> 1 + 14 + 22 = 37   (conserved; before the revision P1 accepted 37 against 18 without a gate, R1 F-02)
   --> [AC-1.1 test population, SPEC:195]  14 commands carry the section; load and the 6 section-4 commands must not   (consistent)
   --> [AC-1.2 live-check population, SPEC:196]  14 commands run with --output <dir>   <-- M-16: init-lite takes a file; cleanup-audit and index-repo take no output flag
```

No dimensional mismatch found. The 10 ready commands split 6 (P1 flag set) + 4 (P2: reflect, release-split, tdd, troubleshoot) = 10 against `SPEC:83-92`.

## Adversarial notes (Whittaker, changed lines only)

- **W-7** (supports M-15). I can break this specification by **Divergence Attack**. The invariant at **WC-4 (`SPEC:62`) versus the adversarial row (`SPEC:83`)**, "the contract is in the report directory, which is the directory passed as a directory-valued `--output`", fails when **the input is `/sc:adversarial --compare a b --output D`**. Concrete attack: before: `D/` empty. Reading 1 (WC-4's first clause): report directory = `D`, the contract goes to `D/return-contract.yaml`. Reading 2 (the row, "`<output>/adversarial/return-contract.yaml`, its WC-4 report directory"): `D/adversarial/return-contract.yaml`. A coordinator that checks the WC-4 path in 7.2 step 4 (`test -s <contract>`) finds nothing under reading 2 even though `worker_done --report-path` carries the right path. The coordinator reads the path from `worker_done` (WC-4 last sentence), so the live outcome is still correct; only the acceptance check can pick the wrong path. Graded Medium.
- **W-8** (supports M-17). I can break this specification by **Sequence Attack**. The invariant at **WC-4 "including stops before any other output exists" (`SPEC:62`)**, fails when **the report directory is created by the command's own output step and the stop happens before it**. Concrete attack: `/sc:tdd "auth" --unattended --output .dev/out/TDD.md` with `.dev/out/` absent; the bare-topic gate fires first; the contract must go to `.dev/out/`, which does not exist. Whether the command creates it is unstated. Graded Medium (the worse reading needs an implementer who does not create a directory the spec says to write into).
- The other four attack classes found no break on changed lines: Zero/Empty on the new `awk '$2 != 0'` (empty diff passes, correct); Sentinel on the `--numstat` binary-file value `-` (prints a row, which is the safe direction); Accumulation (no counter on changed lines).

## follow-up candidates

Medium and minor findings. None triggers a revision, none fails this review, and none appears in the Reviser brief. Issue offer: not made (no interactive user in this run); nothing was created.

### Medium (warnings)

- **M-15** (Wiegers, Hohpe; origin=changed) `SPEC:62` sends a command with a directory-valued `--output` to that directory, and `SPEC:83` puts adversarial's contract in `<output>/adversarial/` and calls that "its WC-4 report directory". WC-4's third clause defers to the row only for a command "with no such flag" (`SPEC:62`), and adversarial has the flag. One clause is enough: say that adversarial's report directory is `<output>/adversarial/`, or move its contract to `<output>/`. W-7. Residual of round 1 F-01 for adversarial (`R1:57`); the actual path a coordinator reads comes from `worker_done`, so the outcome is not forced.
- **M-16** (Crispin, Adzic; origin=changed) AC-1.2 (`SPEC:196`) runs every command in the P1 flag set "with `--unattended --output <dir>`". init-lite's `--output` is a file (`SPEC:87`, `INV-A:55`), and cleanup-audit and index-repo have no output flag (`SPEC:85-86`; `INV-A:42`, `INV-A:53`). The population grew from v1's list (which had no init-lite or brainstorm) by the F-02 repair. 2.3 already tells the coordinator to use the flags section 3 lists (`SPEC:73`), so a tester can adapt; add "or the command's own output flag per section 3" to AC-1.2.
- **M-17** (Nygard; origin=changed) WC-4 does not say the command creates the report directory when it is missing, which matters for tdd and init-lite with `--output <file>` in a new folder and for a gate that fires before any other write. W-8.
- **M-14** (Fowler; origin=unchanged, carried from round 1) AC-C5 (`SPEC:176`) now catches a modified Usage line, as the old filter did, while SA-4 (`SPEC:149`) calls new flags additive and the section 3 intro now says every changed command "gains the `--unattended` flag" (`SPEC:76`). Decide whether adding a flag to a Usage line is allowed under AC-C5 (a named defect-fix exemption, or an AC-C5 text that excludes the Usage line). It depends on the changed line `SPEC:76`, so it is quoted here, but its grade stays Medium because the criterion can be read either way.
- **M-01 to M-13** (origin=unchanged) not touched by the revision (`REV:62`); the open ones remain listed in `round1.md` under follow-up candidates. Two interact with changed lines and stay Medium: M-06 (no acceptance check for WC-3, WC-6 outside tests, WC-12; the new P1 flag-set landing adds no per-phase check for P2 to P4 flag acceptance, noted by `REV:63`) and M-12 (WC-3 answer flag is undefined for several gates).

### Minor (notes)

- **m-05** `SPEC:62` says the contract path for workflow is "known after the run" while 7.2 step 3 says the worker's report path is "the WC-4 contract path" (`SPEC:182`); for workflow a tester takes the path from `worker_done`. Harmless.
- **m-06** `SPEC:159` still carries the phrase "No person gate is involved" in the "Why this order" cell, although business-panel (`--mode socratic` refused), explain (`--format interactive` refused) and test (`--watch` refused) resolve flag-driven gates in P1 (`SPEC:102`, `SPEC:107`, `SPEC:121`). Unchanged text; only a wording note.
- **m-01 to m-04** of round 1 still stand: the `src/`, `CLAUDE.md`, `pyproject.toml`, `sk/`, `cmd/` and `EVIDENCE.md` citations are UNVERIFIED in this sandbox. Examples relied on here and not checkable: `sk/sc-workflow-protocol/refs/return-contract.md:39` (quoted by `INV-B:272`), `src/superclaude/cli/install_core.py:13-24`, `pyproject.toml:38`.

## Coverage statement

- Covered: all 17 changed lines of the 14 hunks (the evidence block above); each of the four prior blocking findings against the AFTER text; the dependents of the changed lines (`SPEC:112` and `SPEC:265` for `load`; `SPEC:63` for the workflow exception; `SPEC:73` and `SPEC:182-183` for the report path; `SPEC:160-162` and `SPEC:83-92` for the phase counts and the 14-command set); the numstat check, reproduced with `git diff --no-index`; counts 43, 10/27/6, 1/14/22 and 15/4/3 against the rows; the inventory lines `INV-B:272`, `INV-A:42`, `INV-A:53`, `INV-A:55` that the changed rows cite.
- Not covered (by the scoped-review rule): text outside the changed lines and prior blockers. A whole-document assurance needs a separate, labelled gate review (a first review of the full document).
- Not covered (sandbox): every citation into `src/`, `CLAUDE.md`, `pyproject.toml`, `sk/`, `cmd/`, `EVIDENCE.md` or Orca internals that no inventory file quotes (UNVERIFIED); the rf-qa fix-cycle steps; the correctness of `REV:21-28` per-finding byte splits.
- Not done by design: no edit to the candidate, no revision, no second or third review started.

## Reviser brief

None: no blocking finding is open. A reviser has nothing to repair; Medium and minor findings above are not to be edited.

verdict: PASS
