review: 2 of 3

# Spec-panel re-review, round 2: Orca worker contract spec

## Header

| Item | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `c9e2ff995f731358d2c486eecbe202f9c810da58a248e59a7c693464e08d5a7b` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` |
| baseline sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| PRIOR | `.dev/orca-command-refactor/review/round1.md` (header `review: 1 of 3`, last line `verdict: FAIL`) |
| prior sha256 | `35ee22a371df245225b7aab7a7fb3dd96a2617760f5cbb708614ebf8c0d76976` |
| reviewer model | `claude-sonnet-5-5` (Sonnet 5.5) |
| review date | 2026-11-10 |
| prompt followed | RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full) |
| brief clauses overridden | none |
| `--iterations` | ignored (re-review: one review, Improve step skipped, no revised specification written) |
| scope | scoped re-review: changed lines + prior blocking findings |

Citation keys. `SPEC:N` = line N of the candidate. `OLD:N` = line N of the baseline. `R1:N` = line N of `round1.md`. `INV-B:N` = line N of `.dev/orca-command-refactor/inventory/commands-b.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `~/.claude/agents/rf-qa.md` and a project `.claude/agents/rf-qa.md` do not exist in this sandbox, so the rf-qa Fix Cycle steps 1-5 were not read; the re-check below follows the Review Loop bullet 5 rules, which stand alone. Citations that point outside the workspace (`src/`, `cmd/`, `sk/`, `refs/return-contract.md`, `orca-ide`) are UNVERIFIED here. This includes the baseline spec's claim that `refs/return-contract.md:39` skips pre-creation stops; I can see it only as recorded at `INV-B:272`.

Issue question: this worker has no user channel, so it does not ask whether to open an issue for the follow-up candidates and creates none. The coordinator asks once per loop.

## Step 1: evidence block

Roles were taken from the brief, not inferred: BASELINE = `specs/history/spec-v1.md`, CANDIDATE = `specs/orca-worker-contract-spec.md`, PRIOR = `review/round1.md`. Command run: `diff -w BASELINE CANDIDATE`. It reports 9 hunks, 10 lines changed (lines 52, 62, 73, 76, 92, 149, 159, 195-196, 198); the hunk headers below use diff's own numbering.

### BEFORE (baseline), lines starting `<`

```text
52c52
< - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
73c73
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
149c149
< | SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
159c159
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
195,196c195,196
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
198c198
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

(The block above holds the hunk headers and the BEFORE lines; the AFTER lines follow.)

### AFTER (candidate), lines starting `>`

```text
> - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command other than `/sc:load` (F-2) adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes its contract at the contract path, which the coordinator computes from the brief (F-1): `<output-dir>/return-contract.yaml` when `--output` / `--output-dir` names a directory; `<file>.return-contract.yaml` beside the file when `--output` names a file (tdd, init-lite); the path in the command's own section 3 row when the row names one (adversarial: `<output>/adversarial/return-contract.yaml`). Two exceptions: workflow mints its own `<id>`, so the coordinator takes its path from `worker_done --report-path` (F-1); `/sc:load` writes no contract (F-2). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists (workflow excepted, F-1). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output path, so the report path is known before dispatch (WC-4; workflow excepted); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the contract path. Every changed command except `/sc:load` (F-2) also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None: a stop before the package exists has no `<id>` directory, so it writes no contract and ends `failed` under WC-5 (F-1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial contract filename, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (F-2) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 other than `load` (F-2) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command other than load (F-2) with `--unattended --output <dir>` | all steps pass |
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states that a stop before its package exists writes no contract (F-1) |
```

Self-check, run before the verdict: each of the 10 AFTER lines (without its `>`) was found with `grep -nF` in the candidate (10 of 10 found) and found 0 times in the baseline; each of the 10 BEFORE lines (without its `<`) was found in the baseline (10 of 10). No role swap. Whitespace-only differences are ignored by `diff -w`; none of the 10 pairs is whitespace-only.

## Prior blocking findings

| Id | Status | Evidence (AFTER text only) |
|---|---|---|
| F-1 | resolved | Defect (R1:214): WC-4 gave `<output-dir>/return-contract.yaml` for every command, which has no creatable path for `--output <file>` (tdd, init-lite), differs from adversarial's fixed `<output>/adversarial/return-contract.yaml` (SPEC:83), and cannot name the runtime `<id>` of workflow before dispatch. AFTER SPEC:62 now defines the contract path in three cases: directory output gives `<output-dir>/return-contract.yaml`; file output gives `<file>.return-contract.yaml` "beside the file ... (tdd, init-lite)"; a path named in the command's section 3 row wins "(adversarial: `<output>/adversarial/return-contract.yaml`)". Workflow is an explicit exception: "the coordinator takes its path from `worker_done --report-path`". The briefs at SPEC:87 and SPEC:90 (`--output <file>`) are unchanged and now have a defined path, so AC-2.2 (SPEC:200) and steps 3-4 (SPEC:182-183) resolve to `<file>.return-contract.yaml`. SPEC:73 now says "output path ... (WC-4; workflow excepted)". The workflow sub-point is removed rather than patched: SPEC:92 now reads "a stop before the package exists has no `<id>` directory, so it writes no contract and ends `failed` under WC-5", and WC-5 (SPEC:63) already maps "no report exists" to `--outcome failed`. SPEC:62 ("including stops before any other output exists (workflow excepted, F-1)"), SPEC:198 (AC-1.4) and SPEC:149 (SA-4, workflow gap dropped) agree with SPEC:92. The workflow skill has no person gate (INV-B:266-270, item (a) "None"), so the dropped pre-creation contract loses no `blocked_question`. No remaining text asks for a workflow contract on a pre-creation stop (`grep -n "pre-creation" SPEC` returns nothing). |
| F-2 | resolved | Defect (R1:215): AC-1.1 and the P1 scope required an `## Unattended mode` section and the WC-4 contract for every 3.1-3.2 command including `/sc:load`, while SPEC:112 and SPEC:265 say load gets no report file. AFTER SPEC:195 reads "every command in sections 3.1-3.2 other than `load` (F-2)", SPEC:196 "each P1 command other than load (F-2)", SPEC:159 "every command in sections 3.1 and 3.2 except load (F-2)", SPEC:76 "Every changed command except `/sc:load` (F-2)", SPEC:52 "Each changed command other than `/sc:load` (F-2)", SPEC:62 "`/sc:load` writes no contract (F-2)". The load row (SPEC:112) and the Decision (SPEC:265) are unchanged and now agree with every gate text, so P1's check can pass and SPEC:154 no longer stalls on load. |

## Findings on changed lines

Changed lines were checked against every requirement that depends on them (SPEC:63, 73, 83, 87, 90, 92, 154, 182-183, 195-200, 262). No blocking finding was found. Medium and minor findings on the changed text are below.

| Id | Class | origin | Finding |
|---|---|---|---|
| M-14 | Medium | changed | SPEC:62 chooses the contract path by whether `--output` "names a directory" or "names a file", but lists only tdd and init-lite as file cases and gives no rule for telling the two apart for commands whose P2/P3 rows only "add `--output`" (SPEC:99-108). An implementer picking the wrong reading for such a command writes `<out>/return-contract.yaml` where the coordinator computes `<out>.return-contract.yaml`. This needs a guess about which reading a command gets, so it is Medium, not blocking. Recommendation: name the file-valued `--output` commands in one list. |
| M-15 | Medium | changed | SPEC:62 lists the adversarial row-path as a third case after the directory case, without saying the row path overrides the directory case, though adversarial's `--output <dir>` (SPEC:83) matches the first case. AC-1.4 (SPEC:198) pins adversarial to one fixed path, so the wrong outcome needs an implementer to ignore that gate. Medium. |
| M-16 | Medium | changed | Step 4 of the live check (SPEC:183) runs `test -s <contract>` unconditionally and AC-2.2 (SPEC:200) requires a contract in every gate-trigger run, while SPEC:62 and SPEC:92 now say workflow can end `failed` with no contract. No section 7 check runs a workflow pre-package stop today (AC-0.4, SPEC:194, is a happy path), so no check fails now; a later one would. Medium. |
| n-5 | minor | changed | SPEC:62 keeps the title "written on every outcome" while carrying two exceptions; the exceptions are stated in the same cell, so the text is inferrable. |
| n-6 | minor | unchanged | `<file>.return-contract.yaml` is a new sibling file beside a deliverable (tdd, init-lite); whether it should be listed in `artifacts` or ignored by the project's staging rules is not stated. It is a note: it depends on no changed line beyond the new path. |

Round-1 Medium and minor findings M-1 to M-13 and n-1 to n-4 were not reopened. They are `origin=unchanged`, none quotes a changed line that depends on it as a blocking defect, and they stay under follow-up candidates. M-1 (phase scope) and M-4 (no usable output path) still read as in `round1.md`: SPEC:159 and SPEC:73 changed only by the load and workflow exceptions, which do not create the wrong outcome those findings describe.

## Adversarial check on the changed lines (Whittaker)

- Sentinel Collision Attack. I can break this specification by **sentinel collision**. The invariant at **SPEC:62** fails when **a `--output` value ends in `.return-contract.yaml` or is itself a directory named like a file**. Concrete attack: `/sc:tdd "auth" --output docs/auth` where `docs/auth/` exists as a directory; before: contract path unknown; after: the coordinator computes `docs/auth.return-contract.yaml` while the command sees a directory and writes `docs/auth/return-contract.yaml` (M-14). Severity: Medium (needs the guess in M-14).
- Zero/Empty Attack. I can break this specification by **zero/empty input**. The invariant at **SPEC:62 and SPEC:92** fails when **workflow stops before its package exists**. Concrete attack: before: SPEC:63 `--outcome failed` and no report; after: same, `worker_done` carries no `--report-path`, which `CAPS:72-74` allows only with real values; consistent. No finding.
- Sequence Attack. I can break this specification by **sequence**. The invariant at **SPEC:154 with SPEC:195** fails when **P1 ends before a gate text outside the changed lines still names load**. Concrete attack: grep for load in the gate texts shows SPEC:112 and SPEC:265 only, both consistent with the exceptions. No finding.
- Divergence and Accumulation attacks produced nothing new on changed lines (M-15 is the divergence case).

## Guard Condition Boundary Table (changed lines only)

Guards on changed lines: the contract-path selector (SPEC:62) and the `/sc:load` exclusion (SPEC:195-196). Classes left out are noted under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract-path | SPEC:62 | Zero/Empty | no `--output` | not specified for the selector | none (carried M-4, unchanged) | GAP (M-4, Medium, origin unchanged) |
| contract-path | SPEC:62 | One/Minimal | `--output` names an existing directory | directory case | `<output-dir>/return-contract.yaml` | OK |
| contract-path | SPEC:62, SPEC:87, SPEC:90 | Typical | `--output <file>` for tdd or init-lite | file case | `<file>.return-contract.yaml` | OK |
| contract-path | SPEC:62, SPEC:83 | Legitimate Edge Case | adversarial `--output <dir>` | directory case and row case both match | row path wins by AC-1.4, order not stated | GAP (M-15, Medium) |
| contract-path | SPEC:62 | Sentinel Value Match | value ambiguous between file and directory | not specified | none | GAP (M-14, Medium) |
| contract-path | SPEC:62, SPEC:92 | Legitimate Edge Case | workflow | exception | path from `worker_done --report-path`; pre-package stop writes none, `failed` | OK |
| load-exclusion | SPEC:195-196, SPEC:112 | Legitimate Edge Case | `/sc:load` in 3.2 | excluded | no section, no contract | OK |
| load-exclusion | SPEC:159, SPEC:128 | Typical | other 3.1-3.2 command | included | section and contract required | OK |

Left out with reasons: contract-path Maximum/Overflow (a path has no numeric capacity; unwritable paths are M-4, unchanged); load-exclusion Zero, One and Maximum (a command is either load or not).

## Quantity Flow Diagram

The changed lines alter no command count: 43 = 10 + 27 + 6 and the 37 worker candidates stay as in `R1:186-195`. AC-1.1 now asserts 36 (37 minus load) against the 13 P1-named commands; that gap is the carried M-1 (origin unchanged, Medium), not a new mismatch.

```text
[37 worker candidates] --> [AC-1.1 excludes load: 36 asserted at P1, SPEC:195]
                              P1 names 13 commands (SPEC:159); remaining phase mapping unchanged (M-1)
```

## Coverage

Covered: every changed line (10 AFTER and 10 BEFORE lines) and each line that depends on them (SPEC:63, 73, 83, 87, 90, 92, 112, 154, 159, 182-183, 195-200, 262, 265); the prior report in full; the README; `INV-B:266-276` for the workflow claim. Panel order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower; Gregory and Hightower had nothing on changed lines. Not covered: the unchanged remainder of the candidate beyond the dependency checks above (this is a scoped re-review, not a whole-document review; whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review); any file outside the workspace; the spec's own commands. The `--focus correctness` artifacts were not requested.

## follow-up candidates

Medium (warnings): M-14, M-15, M-16, plus the carried M-1 to M-13 from `round1.md`.
Minor (notes): n-5, n-6, plus the carried n-1 to n-4.
These never trigger a revision, never fail a review and are not in a Reviser brief.

Coverage line: scoped PASS: changed lines + prior blockers

No Reviser brief is written: no blocking finding is open.

verdict: PASS
