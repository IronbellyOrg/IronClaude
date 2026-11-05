# Review: P0 spec fixes S1-S3 (uncommitted diff)

Scope: `git diff -- .dev/orca-command-refactor/specs/orca-worker-contract-spec.md .dev/orca-command-refactor/decisions/APPROVED.md`, against `specs/history/spec-v7-approved-969c770.md` (byte-identical to `HEAD`'s spec, checked with `cmp`). Reviewed 2026-11-03, read-only.

## Verdict

**FAIL.** S2 and S3 are correct and change nothing else. S1 has two blocking defects. First, the P0 outcome rule contradicts WC-5, which is installed in the same phase. Second, two of the three P0 smoke commands have no report file that a brief can name before dispatch, so the instruction "each P0 brief names that file" cannot be followed as written.

## Findings

### B1. Blocking: the P0 outcome rule contradicts WC-5's "never reads the command's own status"

- **File:line:** spec `orca-worker-contract-spec.md:301` (AC-0.4) against `:73` (WC-5); also `:59` and `:86`.
- **Problem:** AC-0.4 now says the `--outcome` is `failed` when "the file has its own `status` field set to `failed`". WC-5 (`:73`) says "The worker never reads the command's own `status` field for this". S1 only switches off WC-5's *no-contract* clause ("so the worker does not apply WC-5's no-contract rule"). It does not switch off the "never reads own `status`" clause, and it does not cover WC-5's "first sentence of the body states `worker_status`", which no P0 run has. WC-5 has no phase scope. P0 installs `WORKER-CONTRACT.md` with the WC-5 outcome mapping (`:59`, AC-0.1, 7.2's per-phase install). The section 2.3 brief layout (`:86`) puts a guard line in every brief, and that line sends the worker to that file. So a P0 worker that reads both its brief and the installed WC-5 gets two opposite instructions, and no text says which one wins. The override exists only in an acceptance-check cell that the worker never sees. The spec contradicts itself.
- **Suggested fix:** Scope WC-5 itself, and through it the `WORKER-CONTRACT.md` content that AC-0.1 tests. Add one sentence to WC-5: "Before P1, when no command writes a contract, a brief that states the AC-0.4 P0 outcome rule replaces this mapping, including the no-contract clause, the own-`status` clause and the `worker_status` body sentence." Alternatively, have the P0 brief say explicitly that it overrides WC-5 as a whole, and add that precedence to section 2.3.

### B2. Blocking: "the report file the command already writes" cannot be named before dispatch for adversarial and workflow, and not for troubleshoot as AC-0.4 writes its command

- **File:line:** spec `:301` (AC-0.4: "Each P0 brief names that file"; "In step 3 the report path is that file"); evidence at `:141`, `:151`, `:152`.
- **Problem:**
  - **adversarial** (`--compare ... --output <dir>`): the spec's own 3.1 row (`:141`) says its report today is "contract, but filename not fixed", and P1 is the phase that fixes it. `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:425-443` requires a contract "on every invocation" but names no path. It also frames the contract as returned "when invoked by another command" (`:429`), which a direct top-level run is not. At P0 no file name is defined. The status sits in a nested `return_contract.status` key. The merged output's name is not fixed either (`SKILL.md:375`). The brief therefore has no defined file to name.
  - **workflow** (`--handoff none`): the contract path is `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/return-contract.yaml`, generated at run time (`commands/workflow.md:12`). `--output` is banned (`workflow.md:42`), so no flag can fix the path. Pre-creation STOPs write no file (`refs/return-contract.md:39`). The brief can only name a pattern. In the disposable worktree that pattern already matches a file: the committed `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/return-contract.yaml`, which is the P0 plan package itself. A workflow run that STOPs before creating its package could then be scored `succeeded` from a stale file.
  - **troubleshoot:** AC-0.4's command line passes no `--output-dir`, so `REPORT.md` lands in `.dev/troubleshoot/<slug>-<timestamp>/` (`commands/troubleshoot.md:56`) and is not nameable before dispatch. This one can be fixed with a flag the command already has.
- **Suggested fix:** In AC-0.4, name each command's P0 file and how to find it.
  - troubleshoot: add `--output-dir <dir>`; the file is `<dir>/REPORT.md`, and its status is the `**Status**:` header line (`refs/report-template.md:14`).
  - workflow: the file is the `return-contract.yaml` inside the package directory the run prints. It must be a package that is new in step 6's `git status`, never one that already exists. A missing new package means `failed`.
  - adversarial: name one fixed-name file under `<output>/adversarial/` that the skill always writes, for example `merge-log.md`, which has no status field. Or have the brief name `<output>/adversarial/return-contract.yaml` and state that the P0 brief, not the skill, fixes that path, and that the status is `return_contract.status`.

### N1. Note: step 4 is not required to pass, so an empty report passes AC-0.4

- **File:line:** spec `:301`, `:286`.
- **Problem:** AC-0.4 requires "steps 1-3 and 5-7 pass". Step 4 is now "runs only `test -s`" and has no pass condition, and 7.2 step 4's own pass condition is replaced (`:286`). An empty file gives outcome `failed`. That matches the rule, so step 3 passes, and AC-0.4 passes. This wording was carried over from v7, but the edit rewrote the cell and kept the gap.
- **Suggested fix:** "Steps 1-7 pass, where step 4 is `test -s <file>` exiting 0."

### N2. Note: the P0 rule maps the command's own `blocked` (and `partial`) to `succeeded`

- **File:line:** spec `:301` against `:73`.
- **Problem:** troubleshoot's `**Status**:` can be `blocked` (`refs/report-template.md:14`, `SKILL.md:66`). Under the P0 rule that becomes `succeeded`, while WC-5 maps `worker_status: blocked` to `failed`. The rule is consistent with itself and the owner approved it, but it differs from the INV-002 repair, which proposed going through the WC-4 mapping. It also weakens AC-0.4 as evidence for UNVERIFIED item 1.
- **Suggested fix:** `failed` when the status is `failed` or `blocked`.

### N3. Note: "its own `status` field" has three different shapes

- **File:line:** spec `:301`.
- **Problem:** The field is a markdown `**Status**:` line for troubleshoot, top-level YAML `status:` for workflow, and nested `return_contract.status` (a quoted string) for adversarial. A literal key lookup misses two of them.
- **Suggested fix:** Name the field per command when B2 is fixed.

### N4. Note: the section 2.3 brief template has no slot for the P0 rule

- **File:line:** spec `:84-86`, `:220`.
- **Problem:** P0 ships a brief template in `WORKER-CONTRACT.md`. Section 2.3 lists what a brief states, and the P0 outcome rule and report-file line are not in that list. Coordinators who copy the template will leave them out.
- **Suggested fix:** Add "at P0 only: the report file and the AC-0.4 outcome rule" to the section 2.3 list.

### N5. Note: neighbouring `install_core.py` citations in the S3 sentence are still stale

- **File:line:** spec `:59`.
- **Problem:** S3 fixed `13-24` to `13-27`, which is correct. The same sentence still cites `install_core.py:33,53` (today a docstring opener and a blank line; the glob is at `:56`) and `:152` (today `if not claude_dir.exists()`; the `KNOWN_CORE_FILES` filter is at `:155`). Fixing them is out of S3's scope, so this is not an over-edit, but the same erratum remains.
- **Suggested fix:** Change them to `:36,56,65-70` and `:12,155`, or cite by symbol.

### N6. Note: the plan's `source.md` snapshot still has the pre-fix text

- **File:line:** `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:59,301`.
- **Problem:** The P0 plan executes against this copy, which still says `13-24` and the old AC-0.4. This is outside the reviewed diff, but P0 will not pick up S1-S3 until the plan is refreshed.
- **Suggested fix:** Re-snapshot `source.md`, or re-plan, after B1 and B2 are fixed.

### N7. Note: no link from the spec to the S1-S3 record

- **File:line:** spec `:385-396` (section 9), `APPROVED.md:39-46`.
- **Problem:** Section 9 lists only D1-D5, GIT and L1-L3. Nothing in the spec points to the new APPROVED.md entry, and AC-0.4 does not cite it.
- **Suggested fix:** Add one S1-S3 row to section 9, or cite `APPROVED.md` S1 in AC-0.4.

## Self-audit

- **Diff scope:** `diff` of the current spec (with 13-27 put back to 13-24) against the history copy shows only lines 285, 286 and 301 changed, plus the S3 range. AC-1.1 changed only in the S2 phrase. Nothing else was edited. The history copy equals `HEAD` (`cmp`).
- **S3:** `src/superclaude/cli/install_core.py:13` is `KNOWN_CORE_FILES = frozenset(` and `:27` is `)`, so 13-27 is exact. `13-24` was wrong even before #344, which added 2 entries; the pre-#344 span was 13-25.
- **S2:** In section 2.1 (`:60`), case 1 and case 2 each have an exact text, the unnumbered copies-disagree condition has an exact text (with a `<paths>` placeholder), and case 3 has only the `guard refused:` body prefix. That is four conditions, three texts and one prefix, so the erratum is accurate. No other "four ... reason texts" wording remains (grep).
- **7.2:** The P0 pointers at step 3 ("replaces the last two conditions") and step 4 ("replaces this step") match AC-0.4. Steps 2, 5, 6 and 7 do not depend on the contract.
- **Other sections:** 7.4 (WC-4 and WC-5 rows), AC-1.5 and AC-1.7 (also replace steps 3-4), the section 3.1 intro (`:137`, "the worker reports the named file until Phase 1", which supports S1), the section 6 P0 row, and section 9 D1/D4 placement. No new contradiction apart from B1.
- **Command files:** I opened `commands/troubleshoot.md`, `skills/sc-troubleshoot-protocol/SKILL.md` and `refs/report-template.md`; `commands/workflow.md` and `skills/sc-workflow-protocol/refs/return-contract.md`; `commands/adversarial.md` and `skills/sc-adversarial-protocol/SKILL.md` (return contract, output layout, variant loading).
- **APPROVED.md:** S1, S2 and S3 match the spec edits word for word in substance. Its source citation is right: INV-002 is at `REPORT.md:29,204`, D-004 at `:67`, D-011 at `:137`.

## Recheck after fix pass 1

Reviewed 2026-11-03 against the current uncommitted diff (`git diff -U0`), read-only. I opened every new citation.

### Verdict

**PASS.** B1 and B2 are fixed and N1-N5 are addressed. Nothing left in the spec contradicts itself or makes P0 unrunnable. One new factual error (R1) should be fixed before P0 runs, but it does not block.

### Disposition of earlier findings

| ID | Status | Evidence |
|---|---|---|
| B1 | Fixed | The WC-5 row (spec:73) now says that before P1 a brief stating the AC-0.4 file and rule replaces the mapping for that Task, including `--outcome`, `--report-path` and the body's first sentence. AC-0.4 (spec:301) repeats "which replaces WC-5 for that Task" in the brief itself, so the worker sees the precedence even when the installed file is read first. |
| B2 | Fixed | AC-0.4 now names a file for each command. troubleshoot gains `--output-dir <dir>`, so the file is `<dir>/REPORT.md`. workflow uses the one new `TASK-WF-*` package, and "a package that existed before dispatch never counts", which closes the stale-package hazard. adversarial uses the fixed name `<dir>/adversarial/merge-log.md`. Each path can be known before dispatch or found by a stated rule. |
| N1 | Fixed | "steps 1-7 pass", and step 4 is `test -s <file>` exiting 0. |
| N2 | Fixed | `blocked` now maps to `failed`. |
| N3 | Fixed | The status field is named for each command. For adversarial the claim is wrong (R1). |
| N4 | Fixed | Section 2.3 (spec:84) has the item "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)". |
| N5 | Fixed | `install_core.py:36` is the docstring "Copies all .md files", `:56` is `glob("*.md")`, and `:65-70` is the copy loop with the skip-if-exists branch. `:12` is the `KNOWN_CORE_FILES` comment and `:155` is the `KNOWN_CORE_FILES` filter. `:13-27` is still exact. |
| N6 | Open (outside the diff) | The plan snapshot `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md` still has the pre-fix text. Re-snapshot or re-plan before P0 executes. |
| N7 | Partly fixed | AC-0.4 now cites `decisions/APPROVED.md` S1. Section 9 has no S row, and the path is written relative to the project folder, unlike section 9's full `.dev/orca-command-refactor/decisions/APPROVED.md`. This is wording only. |

### Citation check (each opened)

- `cmd/troubleshoot.md:56`: the `--output-dir` row, default `.dev/troubleshoot/<slug>-<timestamp>/`, "Where REPORT.md ... are written". Correct.
- `sk/sc-troubleshoot-protocol/refs/report-template.md:14`: `**Status**: <success|partial|blocked|failed>`. Correct.
- `sk/sc-workflow-protocol/refs/return-contract.md:3-7`: line 3 names `.dev/tasks/to-do/<id>/return-contract.yaml` and line 7 is the top-level `status: success | partial | failed`. Correct.
- `sk/sc-adversarial-protocol/SKILL.md:2072`: `output_path: "<output-dir>/adversarial/merge-log.md"`. The path is correct, but the "no status field" claim next to it is not (R1).
- `src/superclaude/cli/install_core.py:12,13-27,36,56,65-70,155`: all correct, as listed under N5.
- APPROVED.md S1 and S3 rows match the spec edits. S3 now also records the N5 cite moves.

### New findings

#### R1. Note (should-fix before P0 runs): `merge-log.md` does have a status field

- **File:line:** spec `:301` ("`<dir>/adversarial/merge-log.md`, which has no status field"), against `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:294-298` and `SKILL.md:2075`.
- **Problem:** The merge-log template's `## Metadata` section has `- Status: success/partial/failed` (`artifact-templates.md:298`), and `SKILL.md:2075` lists "status" among the Metadata fields. On a failed check the skill records the failure in `merge-log.md` (`SKILL.md:2050-2053`). Each change entry also has its own `**Status**: Applied/Failed/Skipped` (`artifact-templates.md:304,313`). The spec tells the coordinator, and through the brief the worker, that the file has no status. A merge-log reading `Status: failed` would then score `succeeded` under the spec's description, but `failed` under the rule's literal wording ("its status is `failed`"). So for a failed adversarial merge, the step-3 match has two readings. P0 can still run, and the outcome is deterministic in every other case, so this does not block.
- **Suggested fix:** Replace "which has no status field" with "with the status in the `Status:` line of its `## Metadata` section (`sk/sc-adversarial-protocol/refs/artifact-templates.md:298`); the per-change `**Status**` lines do not count".

#### R2. Note: the installed file may not carry the WC-5 P0 sentence

- **File:line:** spec `:59` against `:73`.
- **Problem:** Section 2.1 says `WORKER-CONTRACT.md` states only "the IronClaude-specific rule (outcome mapping from `worker_status` ...)" for WC-5. It does not say whether the new P0 sentence goes into the file. This is not a contradiction, because the AC-0.4 brief itself says it replaces WC-5. But if the file leaves the sentence out, the worker sees the override only in the brief.
- **Suggested fix:** In spec:59, name "the WC-5 P0 brief override" among the worker-session rules the file states, so AC-0.1's test covers it.

### Self-audit (recheck)

- **Diff:** I read the full `-U0` diff. The changes since my first review are limited to spec lines 59, 73, 84 and 301, and the APPROVED.md S1 and S3 rows. Lines 285-286 and 306 are as already reviewed.
- **B1:** I read the WC-5 row against the AC-0.4 cell and section 2.1's file contents. The precedence is now stated in both WC-5 and the brief.
- **B2, workflow:** a pre-creation STOP leaves no new package, so the outcome is `failed` and step 4 fails, which is correct. The reflect step inside workflow writes under `.dev/reflect/`, not a second `TASK-WF-*` directory, so "the one package the run creates" is unambiguous.
- **B2, adversarial:** `merge-log.md` is produced by step 5's step 6 (`SKILL.md:324,327`). If the run aborts before merging, the file is missing, so the outcome is `failed` and step 4 fails, which is correct.
- **Other sections:** I rechecked 7.2 steps 3-4 against the new AC-0.4 cell, 7.4's WC-5 row and section 2.3's list order. I found no new contradiction.
