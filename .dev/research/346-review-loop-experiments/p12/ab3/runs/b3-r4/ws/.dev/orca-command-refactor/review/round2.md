review: 2 of 3

# /sc:spec-panel re-review, round 2: Orca worker-contract spec

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  candidate_sha256: fd9020aeb88b0fd3aa673b34de70465e3d6d2d18a0ec0245de39c5d2383e536b
  candidate_size: 285 lines, 58573 bytes
  baseline: .dev/orca-command-refactor/specs/history/spec-v1.md
  baseline_sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
  baseline_size: 285 lines, 57763 bytes
  baseline_check: baseline sha256 equals the candidate_sha256 that round1.md records (round1.md:8), so the baseline is the text round 1 reviewed
  prior_report: .dev/orca-command-refactor/review/round1.md
  prior_report_sha256: 86a19b799790db4ad823c8e2bd878addb830983b2581cc4a3bf8138a4562fe2a
  prior_header: "review: 1 of 3" (round1.md:1), prior verdict FAIL (round1.md:224); N = 1 + 1 = 2; the review-3 halt check does not apply
  reviewer_model: claude-sonnet-5-5 (Sonnet 5.5)
  mode: critique, re-review (--iterations ignored, Improve step skipped, no revised specification written)
  focus_areas: [requirements, architecture]
  panel_in_review_order: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  brief_clauses_overridden: none (the brief's fixed final reply format means the once-per-loop "open an issue?" question to the user is not asked; no issue was created)
quality_assessment:   # 0-10, advisory only; the verdict is decided by blocking findings
  clarity: 7
  completeness: 6
  testability: 6
  consistency: 6
```

Citation key. `spec:N` = line N of the candidate. `base:N` = line N of the baseline (both files have 285 lines, so a number is the same line in both). `r1:N` = line N of `review/round1.md`. `rev1:N` = line N of `review/revise1.md` (read as context only; every claim below is checked against the candidate, not against the reviser's account). `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any `sk/...`, `cmd/...`, `src/...`, `CLAUDE.md:`, `pyproject.toml:`, `Makefile:`, `EVIDENCE.md:` or `.dev/codegraph-migration/...` line that the inventories do not quote is UNVERIFIED here: those files are not inside the sandbox.

## Step 1: evidence block

Roles are fixed by the brief and the re-review table: CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`, PRIOR = `.dev/orca-command-refactor/review/round1.md`. Command run in the workspace root: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. Exit status 1 (the files differ). The diff has 6 hunks: `73c73`, `76c76`, `154c154`, `159c159`, `176c176`, `193,195c193,195`. That is 8 baseline lines and 8 candidate lines, at lines 73, 76, 154, 159, 176, 193, 194, 195. The diff is not empty, so the prior blocking findings are decided against the AFTER text below.

### BEFORE (baseline), lines starting `<`, verbatim

```text
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-[^-]'` | prints nothing: edits are additive |
< | P0 | AC-0.3 | `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \| grep -E '^-[^-]'` | prints nothing: no existing routing row changed (SA-5) |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

### AFTER (candidate), lines starting `>`, verbatim

```text
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, including `--unattended` from the phase in which the command gains it (F-1) but not in the P0 smoke briefs (F-3), and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1), in the phase its row names and not earlier (F-1). Phase numbers refer to section 6.
> Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4. A command gains `--unattended` and its `## Unattended mode` section only in the phase that resolves all of its gates (F-1): the Phase column of its 3.2 row, or the phase of its 3.1 small fix. brainstorm and init-lite have no small fix and gain neither; a P4 command that D2-D4 leave unchanged (pr-submit under D3 (a)) gains neither.
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag, on the P1 commands in the next column only (F-1); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff --numstat master...HEAD -- src/superclaude/commands/<name>.md \| awk '$2 != 0'` (F-2: prints any file with a deleted line, whatever the line starts with) | prints nothing: edits are additive |
> | P0 | AC-0.3 | `git diff --numstat master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \| awk '$2 != 0'` (F-2) | prints nothing: no existing routing row changed (SA-5) |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, read as follows because the flag and the contract arrive in P1 (F-3): the step-1 brief omits `--unattended`; in step 3 the `--outcome` is compared with the status in the command's existing report (the "Report today" column of 3.1) and the report path is that file; step 4 is `test -s` on that file only. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command of the phases up to the one under test (P1 here) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no command of a later phase and no section-4 command has one (F-1) | passes |
```

Line map, in the order of the two blocks above: 1st line = spec:73 (section 2.3), 2nd = spec:76 (section 3 intro), 3rd = spec:154 (section 6 intro), 4th = spec:159 (P1 row), 5th = spec:176 (AC-C5), 6th = spec:193 (AC-0.3), 7th = spec:194 (AC-0.4), 8th = spec:195 (AC-1.1).

### Self-check (run, not assumed)

For each of the 8 AFTER lines (without `> `) `grep -qF` found it in the candidate, and for each of the 8 BEFORE lines (without `< `) `grep -qF` found it in the baseline: 16 of 16 found, 0 missing. Roles are not swapped.

## Prior blocking findings: re-check

| id | prior grade (r1) | status now | evidence (AFTER text) |
|---|---|---|---|
| F-1 | blocking | **resolved** | spec:154, spec:159, spec:76, spec:73, spec:195 |
| F-2 | blocking | **resolved** | spec:176, spec:193 |
| F-3 | blocking | **resolved** | spec:194, spec:73 |

Blocking findings open: none. Regressed: none.

### F-1 resolved: the flag now exists only in the phase that resolves the command's gates

Defect (r1:66-67): P1 (base:159) gave `--unattended` and, through AC-1.1 (base:195), the `## Unattended mode` section to every command of 3.1 and 3.2, although the gates WC-2 (spec:60) demands are resolved only in P2 (spec:160), P3 (spec:161) and P4 (spec:162); under D3 (a) pr-submit would still need a section (spec:240).

Check against the AFTER text only:
- spec:159 now gives the flag to "the P1 commands in the next column only"; the column lists analyze, build, business-panel, design, document, explain, index, test, load, plus fixes to adversarial, cleanup-audit, index-repo, workflow (13 commands).
- spec:154 states the general rule: a command gains the flag and the section "only in the phase that resolves all of its gates: the Phase column of its 3.2 row, or the phase of its 3.1 small fix"; brainstorm and init-lite gain neither; pr-submit under D3 (a) gains neither.
- spec:76 says the section arrives "in the phase its row names and not earlier"; spec:73 says the brief carries `--unattended` "from the phase in which the command gains it".
- spec:195 (AC-1.1) now asserts the section for the commands of the phases up to the phase under test and its absence for later-phase and section-4 commands.
- Count check from the Phase column of the 3.2 rows (spec:99-125) and the 3.1 small fixes (spec:83-92): P1 = 9 + 4 = 13; P2 = 11 (3.2) + 4 (reflect, release-split, tdd, troubleshoot from 3.1) = 15, equal to the list at spec:160; P3 = 4 (roadmap, save, validate-roadmap, validate-tests; spec:161); P4 = 3 (implement, post-release, pr-submit; spec:162). 13 + 15 + 4 + 3 = 35, plus brainstorm and init-lite = 37 worker commands, equal to the 43 - 6 of spec:76 and to the count in r1:58.
- Gate check for the four P1 commands taken from 3.1: adversarial's default is non-interactive (INV-A:35), cleanup-audit has no run-time wait (INV-A:42), index-repo none (INV-A:53), workflow none (INV-B:269). The nine 3.2 P1 rows name no gate or a refusal (spec:99-123; validate-tests at spec:125 is P3). So no P1 command accepts the flag while a gate is unresolved.
- spec:154 ("Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4") stays true: no P1 to P3 text writes a D2 to D4 outcome.

Result: the wrong outcome in r1:67 (a flag that passes AC-1.1 and still stalls) no longer follows from the stated text. A residual question about `load` is recorded as M-13 below; it does not reopen F-1.

### F-2 resolved: the additive-edit check now sees deleted bullets

Defect (r1:129-130): `grep -E '^-[^-]'` skipped a deleted line whose second character is `-`, such as a bullet.

Check: spec:176 (AC-C5) and spec:193 (AC-0.3) now run `git diff --numstat master...HEAD -- <file> | awk '$2 != 0'`. Run in the sandbox, git 2.43.0:
- The old filter on a diff holding the deleted bullet `-- Will Not: edit files` printed nothing (exit 1), reproducing the defect.
- `git diff --no-index --numstat` on a rewritten bullet (`- Will Not: edit files` to `- Will Not: edit files unless asked`) printed `1	1	<path>`, so `awk '$2 != 0'` printed it: the check fails, which is correct.
- The same on a pure addition (one new line `## Unattended mode`) printed nothing: the check passes, which is correct.
- numstat rows `12	0	x.md` print nothing; a binary row `-	-	bin.png` prints (fails, acceptable for a command file); empty input prints nothing.
The `--no-index` form stands in for `master...HEAD`, because the sandbox holds no repository history; the three-dot revision syntax and the pathspec are therefore UNVERIFIED here, but they are unchanged from the baseline command and `--numstat` output is the same format in that form. The pass conditions ("prints nothing", spec:176, 193) are unchanged and now hold for the line type that carried the defect.

### F-3 resolved: AC-0.4 no longer asks P0 for what only P1 produces

Defect (r1:73-74): the P0 smoke check needed `--unattended` in the brief (via spec:73) and a WC-4 contract and `status` that troubleshoot, workflow and adversarial do not produce before P1.

Check: spec:194 now reads steps 1-3 and 5-7 as follows: the step-1 brief omits `--unattended`; in step 3 the `--outcome` is compared with the status in the command's existing report ("Report today" column of 3.1, spec:82-92) and the report path is that file; step 4 is `test -s` on that file only. spec:73 says the P0 smoke briefs do not carry the flag. The three P0 commands are troubleshoot, workflow, adversarial (spec:158); their existing reports are `REPORT.md` (spec:91), `.dev/tasks/to-do/<id>/return-contract.yaml` (spec:92; INV-B:272) and a contract at a not-fixed path (spec:83; INV-A:35), so the revised check asks only for files those commands write today. The rule "a failure here reopens section 1" (spec:194) is unchanged and is now a failure about Orca running commands as workers, not about a missing flag. One residual wording gap is recorded as M-14; it needs a guess and is Medium.

## Findings on changed lines

Grading used for each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Blocking only if that sentence holds with no further assumption. No finding below meets that bar.

| id | grade | origin | location | expert | status |
|---|---|---|---|---|---|
| M-13 | Medium | changed (depends on spec:154, 159, 195; text inherited from base:112, 195, 196) | spec:112, 154, 159, 195, 196 | Wiegers, Adzic | new |
| M-14 | Medium | changed (spec:194) | spec:194, spec:91, spec:83 | Adzic | new |
| N-6 | minor | changed (spec:176, 193) | spec:176, 193 vs spec:149 | Whittaker | note |
| N-7 | minor | changed (spec:154) | spec:79 vs spec:154 | Wiegers | note |
| N-8 | minor | changed (spec:195) | spec:195 vs spec:154 | Whittaker | note |

### M-13 (Medium): `/sc:load` is in the P1 list for the flag and the section, but its row says "usage line only" and writes no report
- Expert: Wiegers (consistency), Adzic (testable example).
- Evidence. spec:154 gives the flag and section to a command in "the Phase column of its 3.2 row"; load's Phase is "P1 (usage line only)" (spec:112). spec:159 lists "load (usage line only)" among the P1 commands that receive the flag, and AC-1.1 (spec:195) requires each P1 command's section to name `return-contract.yaml`. The load row says report "none (see note)", resume "n/a", and "use it as a step inside another worker's brief, not as its own Task" (spec:112; INV-B:31, 62, 65: it writes no file). AC-1.2 (spec:196, unchanged) runs the 7.2 check with `--unattended --output <dir>` on each P1 command, and 7.2 steps 3-4 need a contract (spec:182-183). Origin: the baseline had the same conflict (base:112, 195, 196), and its P1 row said the flag was "a no-op where a command has no gate" (base:159), a clause the revision deleted.
- Grading sentence. The guess needed: whether "(usage line only)" means load gains neither flag nor section (then AC-1.1 and AC-1.2 must exclude it) or gains both (then AC-1.2 asks a no-file command for a contract). Two readings are allowed, so this is Medium.
- Recommendation: one clause in spec:154 or spec:195 saying load is excluded from the flag and the section, or that its section states it writes no contract. Priority: Low.

### M-14 (Medium): AC-0.4 step 3 compares the outcome with "the status in the command's existing report", but troubleshoot's existing report is not documented to carry a status
- Expert: Adzic.
- Evidence. The troubleshoot row names `REPORT.md` (spec:91). The inventory says the output contract holds `report_path` and `audit_log_path`, and that `return-contract.yaml` is written only with `--caller task-unified` (INV-B:242); it does not say REPORT.md holds a status field (UNVERIFIED). adversarial's contract filename is not fixed (spec:83; INV-A:35, 60-61), so "the report path is that file" (spec:194) is known only after the run.
- Grading sentence. The guess needed: that with no status field the WC-5 fallback applies (a report exists, so `--outcome succeeded`, spec:63). That reading is natural but unstated for P0. Medium.
- Recommendation: add "or, where the existing report has no status, the WC-5 file-exists rule" to the step-3 clause of spec:194. Priority: Low.

### Minor notes
- N-6 (spec:176, 193 vs spec:149): the corrected check flags any rewritten line, so a new flag added by editing an existing Usage line (checked with `git diff --no-index --numstat`: prints `1	1`) fails AC-C5. That matches SA-4's "existing lines change only where section 3 names a defect fix" (spec:149); the phrase "new flags" in SA-4 could be read as allowing it. A new flag documented on its own line passes.
- N-7 (spec:79 vs spec:154): spec:79 says the ten ready commands report the named file "until Phase 1 adds the contract", but under spec:154 brainstorm and init-lite never gain the section and tdd, troubleshoot, reflect and release-split gain it in P2. Reword to "until the phase named in the last column".
- N-8 (spec:195 vs spec:154): AC-1.1 says "the phases up to the one under test (P1 here)". If the same test is re-run at P4 under D3 (a), pr-submit is a P4 command that gains no section. AC-1.1 sits only in the P1 block, so nothing in this document runs it at P4.

## Guard Condition Boundary Table (changed lines only)

Trigger: the changed lines hold guards and thresholds (the `awk` filter, the phase rule of spec:154, the P0 relaxation of spec:194, the phase-bounded assertion of spec:195). Construction: Nygard, completeness: Crispin-style review (done by Wiegers here), attack: Whittaker. Per the re-review rule, FR-8 to FR-10 and this table cover guards on changed lines only. Input classes that cannot occur for a guard are left out with one line each below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| AC-C5/AC-0.3 numstat filter | spec:176, 193 | Zero/Empty | no change to the file (empty numstat) | false | prints nothing, pass (verified) | OK |
| AC-C5/AC-0.3 numstat filter | spec:176, 193 | One/Minimal | one rewritten bullet (`1`, `1`) | true | prints the file, check fails (verified with git 2.43.0) | OK |
| AC-C5/AC-0.3 numstat filter | spec:176, 193 | Typical | pure addition of a section (`12`, `0`) | false | prints nothing, pass (verified) | OK |
| AC-C5/AC-0.3 numstat filter | spec:176, 193 | Sentinel Value Match | binary file, numstat `-`, `-` | true | prints the file, check fails; a command file is not binary | OK |
| AC-C5/AC-0.3 numstat filter | spec:176, 193 | Legitimate Edge Case | new flag added by editing a Usage line | true | check fails; SA-4 allows "new flags" (spec:149) | GAP (N-6, minor) |
| Phase rule "flag only where all gates resolve" | spec:154 | Zero/Empty | command with no gate (analyze) | true | gains the flag in its Phase column (P1) | OK |
| Phase rule "flag only where all gates resolve" | spec:154 | One/Minimal | 3.1 command with no small fix (brainstorm, init-lite) | false | gains neither flag nor section | OK |
| Phase rule "flag only where all gates resolve" | spec:154 | Typical | gate command (task) | true in P2 only | flag, section and gate resolution arrive together | OK |
| Phase rule "flag only where all gates resolve" | spec:154 | Sentinel Value Match | Phase cell "P1 (usage line only)" (load) | unspecified | flag and section or neither | GAP (M-13, Medium) |
| Phase rule "flag only where all gates resolve" | spec:154 | Legitimate Edge Case | P4 command left unchanged by D3 (a) (pr-submit) | false | gains neither | OK |
| AC-0.4 P0 relaxation | spec:194 | Typical | workflow, existing contract with `status` | true | outcome compared with that status | OK |
| AC-0.4 P0 relaxation | spec:194 | Legitimate Edge Case | troubleshoot, existing `REPORT.md` with no documented status | unspecified | none stated; WC-5 fallback implied | GAP (M-14, Medium) |
| AC-1.1 phase bound | spec:195 | Zero/Empty | command of a later phase | false | must not have a section | OK |
| AC-1.1 phase bound | spec:195 | Typical | command of P1 with a report (analyze) | true | section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` | OK |
| AC-1.1 phase bound | spec:195 | Legitimate Edge Case | P1 command with no report (load) | unspecified | none stated | GAP (M-13, Medium) |
| AC-1.1 phase bound | spec:195 | Maximum/Overflow | re-run at P4 with pr-submit under D3 (a) | unspecified | none stated; the check sits in the P1 block only | GAP (N-8, minor) |

Left out: a Maximum/Overflow row for the phase rule (a command belongs to exactly one phase; counts re-checked above); a Sentinel row for AC-0.4 and AC-1.1 (no sentinel value in those guards); One/Minimal rows for AC-0.4 (the relaxation is a fixed text change, not a threshold). Completion: every cell is filled and every guard on a changed line is enumerated; FR-10 satisfied. Every GAP is graded: Medium (M-13, M-14) or minor (N-6, N-8) because no concrete wrong outcome holds without a guess; no FR-8 or FR-9 blocking finding.

## Adversarial notes (Whittaker; attacks that did not become findings)

- Sequence Attack on the new phase rule: if tasklist (P2) lands its Stage 10.5 call `--unattended` to reflect (spec:122) before reflect (P2, spec:88) gains the flag, tasklist would pass an unknown flag. Both are in P2 (spec:160), so the phase-end check covers it; no ordering inside a phase is stated, and none is needed for a phase that passes only when every check passes (spec:167).
- Divergence Attack on F-1's rule: a 3.1 command whose small fix is in a later phase than its contract work (troubleshoot: small fix P2, report REPORT.md) has no phase that adds a WC-4 contract on the success path in its row (spec:91). WC-4 and the "blocked" definition (spec:62, 95) cover it generally, and the baseline had the same shape (base:91), so it is not a regression and not a new finding.
- Zero/Empty Attack on AC-0.4: with an empty `--output` for troubleshoot (no output flag in the AC-0.4 command line, spec:194) step 6 must use the "command's documented artifacts" clause (spec:185); troubleshoot's default directory is `.dev/troubleshoot/<slug>-<timestamp>/` (INV-B:242), so it holds.

## What was covered

- Read in full: `README.md`, `review/round1.md`, `review/revise1.md`, the candidate (285 lines), the baseline (285 lines), the review-loop prompts file `~/.claude/rules/prompts/document_review_loop_prompts.md` (RE-REVIEW prompt followed in order: roles, Step 1, review number, self-check), and targeted rows of `inventory/commands-a.md` (lines 33-66) and `commands-b.md` (lines 31, 49, 52, 237-245, 267-275, 293). `inventory/orca-capabilities.md` was searched, not re-read in full, because no changed line cites it.
- The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in `.claude/agents/rf-qa.md`: neither the project copy nor `~/.claude/agents/rf-qa.md` exists in the sandbox, so that file is unread. The rules of the command's Review Loop section were applied on their own, as the command says they may be.
- Re-checked: the three prior blocking findings (all resolved); all 8 changed lines and the requirements that depend on them (WC-2, WC-4, WC-5, SA-1, SA-4, the phase table of section 6, 7.2 steps 1-7, AC-1.2, AC-2.1 to AC-2.2, D2 to D4); phase membership counts recomputed from the Phase column.
- Not covered: whole-document assurance (this is a scoped re-review; the unchanged text was not re-graded); the real behaviour of any command or of Orca; `git diff ... master...HEAD` against real repository history (no history in the sandbox); `--focus correctness` (not requested), so no State Variable Registry; Pipeline Dimensional Analysis is not triggered (a rollout plan, not a multi-stage data pipeline).

## Carried forward from round 1 (not re-graded)

Medium M-1 to M-12 and minor N-1 to N-5 (r1:28-49, 78-211) sit on lines the revision did not change, except that M-1, M-4, M-8 and M-11 cite spec:73, where only the `--unattended` clause changed and the missing coordinator duties they name are still absent. All stay Medium or minor, status open, `origin=unchanged`; none quotes a changed line that depends on it, so none is a blocking candidate and none affects this verdict. One related remark on M-3: AC-1.2 (spec:196) still runs `--output <dir>` on cleanup-audit and index-repo, whose output paths are fixed (spec:85, 86); this is M-3 and M-11 over again.

## Follow-up candidates

Medium: M-13, M-14 (new this round); M-1 to M-12 (carried from round 1).
Minor: N-6, N-7, N-8 (new this round); N-1 to N-5 (carried).
The session that ran this review would ask the user once per loop whether to open an issue for them; the brief fixes the final reply format, so no question was asked and no issue was created. None of these triggers a revision.

Coverage: scoped PASS: changed lines + prior blockers. A whole-document assurance needs a separate, labelled first review (the gate review, which the coordinator runs once after this PASS).

## Reviser brief

Blocking finding ids: none. No blocking finding is open, so no revision is called for.

Reviser rules (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the spec before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone, including through "apply all findings".

verdict: PASS
