review: 2 of 3

# /sc:spec-panel critique (re-review): orca-worker-contract-spec.md

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 58973 bytes), sha256 `361193fc0635fb15c8c62bef7845f79c10650c2ce1378fb6cefbbb9b882a7ae8` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines, 57763 bytes), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals `round1.md:9`, so the baseline is the text round 1 reviewed) |
| PRIOR | `.dev/orca-command-refactor/review/round1.md`, sha256 `3f19269286120dc47e7a653157613c507c2f4bc6ce2e2907d05e29b4ddf69262`; its header (`round1.md:1`) is `review: 1 of 3`, its last line (`round1.md:232`) is `verdict: FAIL`, so N = 2 and the review-3 halt does not apply |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Prompt followed | RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full): roles fixed from the table, Step 1 evidence block before any finding, self-check before the verdict |
| Brief clauses overridden | none (the brief names the files and asks for path:line; it neither widens the scope past changed lines and prior blockers nor regrades a minor finding) |
| Improve step | skipped: `--re-review` ignores `--iterations`, skips Improve and writes no revised specification; the candidate is untouched |
| Format | standard, critique-mode buckets |
| Evidence limits | `INV-A`, `INV-B` and `CAPS` mean the three files under `.dev/orca-command-refactor/inventory/` and were readable. Every `cmd/`, `sk/`, `ag/` (`src/superclaude/**`), `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md` and `.dev/codegraph-migration/**` citation is UNVERIFIED here (not inside the workspace); where this report leans on one it says so |

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`, verbatim)

Roles: lines starting `<` are BEFORE (baseline); lines starting `>` are AFTER (candidate). The diff has 10 hunks, 12 BEFORE lines and 12 AFTER lines. Everything outside these lines is unchanged (the revision kept 285 lines).

```diff
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-4 | **One report file, at the path its section 3 row names, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at the path its section 3 row names. The default is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); where `--output` names a file it is `<that file path>.return-contract.yaml`; adversarial and workflow keep the paths in their rows. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists (except workflow stops before its package folder exists, which write none; WC-5 reads the missing file as `failed`). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
73c73
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
---
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` where the command's phase has added it (section 6) and every flag section 3 lists as required; the output directory or file its row names, so the report path is known before dispatch (WC-4; workflow's is read from its run result, because its package `<id>` is made at run time); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
---
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path its row names, `<output-dir>/return-contract.yaml` by default. Every command in a phase scope that lists `--unattended` (section 6) gains the `## Unattended mode` section (section 2.1); the P1 small fixes to ready commands and the load usage line add none. Phase numbers refer to section 6.
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
---
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None: a stop before the package folder exists writes no contract, and WC-5 reads that as `failed` (WC-4) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
149c149
< | SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
---
> | SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, the adversarial contract gap, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
154c154
< Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.
---
> Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4. A command accepts `--unattended` only from the phase that resolves all its gates; before then the coordinator briefs it without the flag.
159c159
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
---
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode, the `--unattended` flag and the `## Unattended mode` section for the eight no-gate commands first listed, with an output flag where a command lacks one; the small fixes to ready commands (no `--unattended`). | analyze, build, business-panel, design, document, explain, index, test; load (usage line only); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
194,196c194,196
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
---
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, read for P0 as follows: step 1's brief is the command line as written, with no `--unattended` (no command accepts it before P1); step 3's `--outcome` is `succeeded` when the command's existing report file was written and `failed` otherwise, and its report path is that file (the WC-4 and WC-5 contract rules start at P1); step 4 is `test -s` on that file, without the `status` check. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that each of the eight P1 commands that take `--unattended` (analyze, build, business-panel, design, document, explain, index, test) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no other command and no section-4 command has one yet | passes |
> | P1 | AC-1.2 | 7.2 live check on each of those eight commands with `--unattended` and the output flag its row adds | all steps pass |
198c198
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
---
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | adversarial names one fixed path |
228c228
< - (a) **Explicit `--unattended` flag in the brief (recommended).** The coordinator writes it into every worker's command line; a person never types it. Example: `/sc:troubleshoot "login fails" --unattended --output .dev/troubleshoot/login/`. It is testable by grep and cannot misfire on a person.
---
> - (a) **Explicit `--unattended` flag in the brief (recommended).** The coordinator writes it into the command line of every worker whose command accepts it (section 6); a person never types it. Example: `/sc:troubleshoot "login fails" --unattended --output .dev/troubleshoot/login/`. It is testable by grep and cannot misfire on a person.
```

Self-check (run): every one of the 12 AFTER lines (without `> `) was found with `grep -cF` in the CANDIDATE and every one of the 12 BEFORE lines (without `< `) in the BASELINE; 0 misses. Roles are not swapped.

## What I covered, and what I did not

Covered: the 10 changed hunks above; each prior blocking finding (F-01, F-02, F-03, `round1.md:95-106,110-118,146-148`) re-checked against the AFTER text only; the dependencies of the changed lines: WC-4 and WC-5 (spec:62-63), section 2.3 (spec:73), section 3 intro and rows 83-92 and 99-125 (spec:76-125), SA-1 to SA-4 (spec:146-149), section 6 (spec:154-162), checks AC-C3, 7.2 and 7.3 (spec:174, 179-210), D1 (spec:228) and the leftover mentions of the contract (spec:261). Inventory lines read: `INV-B:242,245` (troubleshoot report), `INV-B:267-275` (workflow contract), `INV-A:35` (adversarial). Not covered: unchanged text that no changed line touches, except that the Medium and minor items of round 1 (F-04 to F-28) were left as they are and are not re-graded.

## Prior blocking findings

| id | Status | Why, against the AFTER text only |
|---|---|---|
| F-01 | resolved | The defect was one contract path (WC-4) against rows that deliver others. AFTER spec:62 now says the contract sits "at the path its section 3 row names", default `<output-dir>/return-contract.yaml`, file-valued `--output` gives `<that file path>.return-contract.yaml`, and "adversarial and workflow keep the paths in their rows". The adversarial row (spec:83) names `<output>/adversarial/return-contract.yaml`, brainstorm (spec:84) and reflect (spec:88) match the default, so the coordinator no longer looks in a wrong place. The workflow contradiction is removed by deletion: the row (spec:92) now writes no contract for a stop before the package folder exists, WC-4 carries the same exception, WC-5 maps the missing file to `failed` (spec:63), AC-1.4 (spec:198) and SA-4 (spec:149) no longer ask for the pre-creation contract, and section 2.3 (spec:73) has the worker read workflow's path from its run result. The three tests of the old defect (adversarial path, workflow pre-creation location, file-valued `--output`) each now have one stated answer. Remaining holes for commands with no output flag at all (cleanup-audit, index-repo, load) and for `--report` (validate-tests) were Medium in round 1 (F-08) and are not re-opened. |
| F-02 | resolved | The defect was P1 requiring `--unattended` and a section on all 37 commands while the gates convert later. AFTER spec:154 adds "A command accepts `--unattended` only from the phase that resolves all its gates; before then the coordinator briefs it without the flag", P1 (spec:159) names eight commands that take the flag (analyze, build, business-panel, design, document, explain, index, test) and lists load (usage line only) and the three ready-command fixes as taking none, AC-1.1 (spec:195) asserts the section for those eight only and that no other command has one yet, AC-1.2 (spec:196) runs those eight with the output flag "its row adds" (all eight rows add one: spec:99, 101, 102, 106-108, 111, 123), and brainstorm, init-lite, load, pr-submit, implement, post-release, auggie-review and task no longer appear in a P1 check. Each of the four listed contradictions is gone, and the interim state in which `/sc:auggie-review <PR> --unattended` posts to the PR cannot arise because the flag is not accepted before P2 (spec:154, 160). |
| F-03 | resolved | The defect was AC-0.4 step 3 needing a WC-4 contract and `--unattended` that P0 cannot produce. AFTER spec:194 reads steps 1, 3 and 4 for P0: step 1 uses the command line as written with no `--unattended`, step 3's `--outcome` is `succeeded` when the command's existing report file was written and `failed` otherwise with that file as the report path, step 4 is `test -s` on that file with no `status` check, and "the WC-4 and WC-5 contract rules start at P1". `/sc:troubleshoot` writes `REPORT.md` (`INV-B:242,245`), workflow writes its package contract today (`INV-B:272`), so P0 can reach its stated pass condition and P1 can start. |

## Guard Condition Boundary Table (changed lines only; Nygard builds, Crispin checks completeness, Whittaker attacks)

Trigger: the changed lines hold one boolean guard (`--unattended` acceptance by phase), one existence guard (workflow package folder) and one path selector (WC-4). Classes that cannot occur for a guard are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` accepted from the phase that resolves all gates | spec:154 | Zero/Empty | flag absent | not accepted/used | today's behaviour (SA-1, spec:146) | OK |
| same | spec:154, 159, 195 | Typical | `/sc:analyze ... --unattended` after P1 | accepted | section + contract (spec:159, 195) | OK |
| same | spec:154, 160 | Legitimate Edge | `/sc:auggie-review <PR> --unattended` after P1, before P2 | not accepted | coordinator briefs without the flag; outward default is today's (SA-1) | OK |
| same | spec:76, 154, 160-162 | Legitimate Edge | P2, P3 and P4 commands after their phase | accepted by section 6 intro; but the scope cells of P2-P4 (spec:160-162) do not list `--unattended`, while spec:76 grants the section to commands "in a phase scope that lists `--unattended`" | implied by spec:52 ("Each changed command adds a short `## Unattended mode` section") and spec:200, not stated in section 6 | GAP (F-29, Medium: the reader needs a guess between spec:76 literal and spec:52) |
| same | spec:195 | Legitimate Edge | the AC-1.1 test after P2 adds sections to other commands | "no other command ... has one yet" | the test fails at P2 unless edited; AC-C3 (spec:174) forbids a baseline-passing test failing | GAP (F-30, Medium) |
| same | spec:159, 195 | Sentinel Value Match | omitted: no sentinel enters this guard (the quoted-token case is F-21, unchanged) | n/a | n/a | OK |
| same | spec:159 | Maximum/Overflow | omitted: a boolean and a fixed list of eight have no capacity | n/a | n/a | OK |
| contract path selector | spec:62, 83, 84, 88 | Typical | `--output <dir>` for brainstorm, reflect; adversarial | default or row path | row path wins; matches the rows | OK |
| contract path selector | spec:62 | One/Minimal | `--output <file>` (tdd, init-lite, spec-panel after change) | file-valued | `<that file path>.return-contract.yaml` | OK |
| contract path selector | spec:62 | Zero/Empty | no `--output`, no `--output-dir`, no row path (cleanup-audit, index-repo, load; `--report` of validate-tests) | no `<output-dir>` | still not specified | GAP (carried, F-08, Medium; the changed line did not create it) |
| contract path selector | spec:62, 92 | Legitimate Edge | workflow stops before its package folder exists | file cannot exist | no contract; WC-5 reads `failed` | OK |
| contract path selector | spec:62, 73, 92 | Legitimate Edge | workflow after the package folder exists | `<id>` unknown before dispatch | worker reads the path from "its run result" (spec:73); INV-B:274 says the contract is a direct `--report-path` | OK (the phrase "run result" is loose; minor, F-31) |
| contract path selector | spec:62 | Maximum/Overflow | omitted: a path has no capacity bound here | n/a | n/a | OK |
| P0 reading of AC-0.4 | spec:194 | Typical | troubleshoot: `REPORT.md` written | existing report file present | `--outcome succeeded` | OK |
| P0 reading of AC-0.4 | spec:194 | Zero/Empty | command writes no report file | file absent | `--outcome failed`, `test -s` fails | OK |
| P0 reading of AC-0.4 | spec:83, 194 | Legitimate Edge | adversarial: "contract, but filename not fixed" | which file is the "existing report file" | not named | GAP (F-31, minor) |
| P0 reading of AC-0.4 | spec:194 | One/Minimal, Maximum/Overflow | omitted: no count or size enters the P0 reading | n/a | n/a | OK |

Completion check (FR-10): every row above has all cells populated and every omitted class has its reason. Synthesis follows.

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

No blocking finding. The three requirement defects of round 1 that concerned stated text (the path of the contract, the P0 pass condition) are repaired by narrowing, not by new rules (spec:62, 73, 92, 194). The edit adds one new class of text, the file-valued `<that file path>.return-contract.yaml` rule (spec:62); it is a derived name, it matches the AC-1.1 string test (`return-contract.yaml` is a substring) and no row contradicts it.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

No blocking finding. The phase order is now consistent: the flag, the section, the test and the live check move together per phase (spec:154, 159, 195, 196), and no command is asked to accept a flag whose gates a later phase converts.

## === ADVERSARIAL ANALYSIS === (Whittaker; one attack per methodology, changed lines only)

1. I can break this specification by **Divergence Attack**. The invariant at **spec:62 and spec:76** (the path "its section 3 row names") fails when **a row names no path**. Concrete attack: `/sc:cleanup-audit --pass 1 --output ...` has no output flag (spec:85); before: contract path = row path (none); after: the coordinator has no path to open. Not a new defect, so it stays F-08 (Medium); the changed rule does not make it worse.
2. I can break this specification by **Sequence Attack**. The invariant at **spec:154** fails when **P1 is merged and the coordinator briefs a P2 command with `--unattended`**. Concrete attack: `/sc:auggie-review 123 --unattended` after P1; before the revision: flag accepted as a no-op and the PR gets a review; after: the spec says the coordinator must not pass it (spec:154), and a command that does not know the flag is a person-mode run, which is today's behaviour. No wrong outcome beyond what a coordinator following spec:154 already avoids.
3. I can break this specification by **Zero/Empty Attack**. The invariant at **spec:62 (workflow exception)** fails when **the contract is absent**. Concrete attack: workflow stops before creating its folder; after: `worker_done --outcome failed` with no `--report-path`, which `CAPS:72-74` allows (a path only with a real value). Holds; the first body sentence still states the status (spec:63).
4. I can break this specification by **Accumulation Attack**. The invariant at **spec:195** ("no other command ... has one yet") fails when **P2 runs**: the string test must change. See F-30.
5. I can break this specification by **Sentinel Collision Attack**. The invariant at **spec:62** fails when **a legitimate output file is already named `*.return-contract.yaml`**. Concrete attack: the caller passes `--output notes.return-contract.yaml`; the derived contract path becomes `notes.return-contract.yaml.return-contract.yaml`; still unique, no collision. Holds.

## Findings on changed lines (`origin=changed`) and dependents

| id | label | graded | origin | location |
|---|---|---|---|---|
| F-29 | MAJOR | Medium | changed (spec:76, 154, 159 against P2-P4 cells spec:160-162) | follow-up |
| F-30 | MAJOR | Medium | changed (spec:195) | follow-up |
| F-31 | MINOR | minor | changed (spec:73, 194) | note |

No blocking finding is open. No severe defect older than the revision was newly discovered in the areas I inspected; the older Medium findings F-04 to F-28 are as round 1 graded them (not re-graded).

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
  review: 2 of 3
quality_assessment:
  overall_score: 7.2
  clarity: 7
  completeness: 7
  testability: 7
  consistency: 8
critical_issues: []
expert_consensus:
  - "All three round 1 blockers are resolved by narrowing (spec:62, 92, 154, 159, 194-198); no new rule or section was added beyond the file-valued contract name."
  - "Residual risk sits in the phase wording for P2-P4 and in the AC-1.1 negative assertion, both Medium."
improvement_roadmap:
  immediate: []
  short_term: [F-29, F-30]
  long_term: [F-04 to F-28, F-31]
adversarial_analysis:
  - {attack: Divergence, severity: MEDIUM, invariant: "spec:62,76", finding: F-08 (carried)}
  - {attack: Accumulation, severity: MEDIUM, invariant: "spec:195", finding: F-30}
```

## Follow-up candidates (Medium and minor; never trigger a revision, never in the Reviser brief)

Medium:

| id | label | expert | issue (path:line) | recommendation | priority | impact |
|---|---|---|---|---|---|---|
| F-29 | MAJOR | Fowler | Section 3 intro (spec:76) gives the `## Unattended mode` section to "every command in a phase scope that lists `--unattended`"; only the P1 cell lists it (spec:159); the P2, P3 and P4 cells (spec:160-162) say nothing of the flag, the section or the output flags, yet AC-2.1 (spec:199) needs an auggie-review section and AC-2.2 (spec:200) runs P2 commands with `--unattended`. Spec:52 ("Each changed command adds a short `## Unattended mode` section") and spec:154 point the other way. Blocking would need the guess that the implementer follows spec:76 alone. | state in each of P2-P4 that the phase adds the flag, section and output flags for its commands | Medium | build clarity |
| F-30 | MAJOR | Crispin | AC-1.1 (spec:195) asserts "no other command and no section-4 command has one yet"; from P2 that assertion is false by design, while AC-C3 (spec:174) says no baseline-passing test fails. Needs the guess that the implementer does not edit the test. | scope the negative assertion to "no section-4 command", and let each later phase extend the positive list | Medium | test consistency |

Minor (notes):

- F-31 AC-0.4 (spec:194) leaves "the command's existing report file" unnamed for adversarial, whose contract name is "not fixed" today (spec:83); and "steps 1-3 and 5-7 pass" excludes step 4, which the same cell then redefines, so whether step 4 must pass is implicit. Section 2.3 (spec:73) says workflow's path is read "from its run result" without naming the output; `INV-B:274` shows it is the package's `return-contract.yaml`.
- Still open from round 1, unchanged and not re-graded: F-04 to F-28 (see `round1.md:187-220`). Note F-08 now has two more commands in its scope question (cleanup-audit and index-repo contract location) that the revision explicitly left alone (`revise1.md:39`).

Issue question (command Review Loop 3): this is a worker run with a fixed one-line reply, so the user was not asked whether to open an issue for the follow-up candidates, and none was created. The coordinator session asks once for this loop.

Coverage: scoped PASS: changed lines + prior blockers. Whole-document assurance needs a separate, labelled first review (the gate review under the GATE prompt); its blockers would start at most one gate loop, and the document is limited to 5 reviews and 3 fix cycles in all. This is review 2 of 3, after one fix cycle.

## Reviser brief

No blocking finding is open (F-01, F-02, F-03 resolved); there is nothing to revise, and no reviser is to edit F-29, F-30 or F-31. Contract if a later review reopens this: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; do not award yourself a PASS.

verdict: PASS
