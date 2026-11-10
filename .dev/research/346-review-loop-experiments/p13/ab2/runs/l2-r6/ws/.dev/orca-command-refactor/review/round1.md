review: 1 of 3

# /sc:spec-panel critique report, round 1

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given, first review of the full document (no `--re-review`, no `--baseline`)
- reviewer model actually used: `claude-sonnet-5-5`
- lint evidence: `.dev/orca-command-refactor/review/lint-1.md:1-5`, sha256 `d3cdbe57...5200d` equals the candidate hash; "Checks: REF. Findings: 0." There is no lint id to confirm or dismiss. A lint id never fails a review by itself.
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-33`
- panel (fixed order, filtered by focus): Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (always active), Newman, Hohpe. Crispin, Gregory and Hightower were not seated because their focus areas (testing, compliance) were not requested.
- notation: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7
  clarity: 8
  completeness: 7
  testability: 7
  consistency: 6
critical_issues:
  - {id: F1, category: requirements, severity: MAJOR, expert: wiegers+whittaker, blocking: true,
     issue: "WC-4 fixes the contract at <output-dir>/return-contract.yaml with a path known before dispatch; the adversarial and workflow rows in section 3.1 put it elsewhere",
     recommendation: "make section 3 the single place that names each contract path, or change the two rows"}
expert_consensus:
  - "The decision (Orca coordinates, commands stay units of work) is supported by the inventories and the capabilities file; no expert found a reason to reverse it."
  - "The 10 / 27 / 6 split and the phase assignment reconcile (see Quantity Flow Diagram)."
  - "The report-file contract is the weak joint: one rule (WC-4) is asked to cover commands whose output flag is a directory, a file, or absent."
improvement_roadmap:
  immediate: [F1]
  short_term: [M1, M2, M3, M4, M5, M6]
  long_term: [M7, M8, M9, M10]
adversarial_analysis: "see section ADVERSARIAL ANALYSIS below"
```

## Findings table (every id used in this report)

| id | bucket | severity label | grade | expert | spec location |
|---|---|---|---|---|---|
| F1 | requirements | MAJOR | **blocking** | Wiegers, Whittaker | SPEC:62, 83, 92, 182, 196, 198 |
| M1 | requirements | MAJOR | Medium | Wiegers | SPEC:62, 87, 90, 116, 120 |
| M2 | architecture | MAJOR | Medium | Fowler | SPEC:147, 172, 52, 158 |
| M3 | requirements | MAJOR | Medium | Adzic | SPEC:62, 63, 262 |
| M4 | requirements | MAJOR | Medium | Nygard | SPEC:62, 73 |
| M5 | architecture | MAJOR | Medium | Nygard | SPEC:62, 64, 183 |
| M6 | requirements | MAJOR | Medium | Whittaker | SPEC:83-84, 89, 103, 110, 118 |
| M7 | requirements | MINOR | Medium | Cockburn | SPEC:23, 43 |
| M8 | requirements | MINOR | Medium | Adzic | SPEC:73, 183, 194 |
| M9 | requirements | MINOR | Medium | Cockburn | SPEC:154, 225, 227-230 |
| M10 | architecture | MINOR | Medium | Newman | SPEC:102, 146, 149 |
| N1 | requirements | MINOR | minor | Wiegers | SPEC:195, 158-162, 112 |
| N2 | requirements | MINOR | minor | Adzic | SPEC:59, CAPS:49 |
| N3 | architecture | MINOR | minor | Hohpe | SPEC:63, 263, CAPS:89 |
| N4 | requirements | MINOR | minor | Wiegers | SPEC:11, 285 |
| N5 | architecture | MINOR | minor | Nygard | SPEC:68 |

## Lint ids

None. `lint-1.md:5` reads "No findings."

## === REQUIREMENTS ANALYSIS ===

### F1 (blocking, MAJOR, Wiegers with Whittaker): the contract location rule contradicts two of the rows that implement it

- Stated texts that collide:
  - WC-4 says the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed", "known before dispatch", and "written ... including stops before any other output exists" (SPEC:62). Live check step 3 then requires "its report path is the WC-4 contract path" (SPEC:182), and AC-1.2 runs that check on each P1 command (SPEC:196).
  - Section 3.1 adversarial row: the brief passes `--output <dir>` and P1 "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (SPEC:83). That is one directory below `<output-dir>`. The inventory shows real runs wrote the contract in `<output>/adversarial/` and sometimes `<output>/adversarial/adversarial/` (INV-A:35, INV-A:60), and the artifacts live under `<output>/adversarial/` (INV-A:35).
  - Section 3.1 workflow row: the contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, the brief passes only `--handoff none` (no output directory), and the package is "fresh each run" (SPEC:92; INV-B:272, INV-B:273). The package `<id>` is created by the command, so the path cannot be known before dispatch. The same row asks P1 to write the contract "for pre-creation STOPs too" (SPEC:92, AC-1.4 at SPEC:198), but the inventory says the existing contract is "Not written for pre-creation STOPs" (INV-B:272) because no package directory exists yet at that point.
- Grading sentence: an implementer who follows the stated text as written builds an adversarial worker that writes its contract at `<output>/adversarial/return-contract.yaml` (SPEC:83) and a workflow worker that writes it inside a package directory the coordinator cannot name in advance (SPEC:92). That is wrong because WC-4 and live-check step 3 require the contract at the WC-4 path known before dispatch (SPEC:62, 182), so AC-1.2 step 3 cannot pass for those two commands, and a pre-creation workflow STOP has no stated place to put the file.
- Whittaker form: I can break this specification by **Sequence Attack**. The invariant at **WC-4 "path known before dispatch" (SPEC:62)** fails when **a command creates its own output directory after the brief is written**. Concrete attack: coordinator dispatches `/sc:workflow "<change>" --handoff none` (SPEC:92). State before: no package, coordinator holds Task ID only. The command STOPs on input validation before creating `.dev/tasks/to-do/<id>/`. State after: no contract anywhere, `worker_done --report-path` has no real value (CAPS:73-74 forbids placeholders), WC-5 says "no report exists" so `--outcome failed` with nothing for the coordinator to open.
- Recommendation: narrow rather than add. State once that the contract path is the one section 3 names for each command, defaulting to `<output-dir>/return-contract.yaml` when the row is silent; make the adversarial row and WC-4 agree on one location; give workflow a coordinator-supplied directory (or state that a pre-creation STOP reports through the `worker_done` body with no `--report-path`). Priority High. Quality-impact: Consistency +1, Testability +1.

### Medium and minor requirements findings (details under `follow-up candidates`)

M1, M3, M4, M6, M7, M8, M9, N1, N2, N4. None names a concrete wrong outcome that needs no further guess.

## === ARCHITECTURE ANALYSIS ===

Fowler (lead), Nygard, Newman, Hohpe.

- The boundary the spec draws is sound and checkable against the inventories: commands contain no Orca call (SPEC:147), the coordinator owns Task splitting (SPEC:39), lifecycle messages stay in the worker's top-level session (SPEC:65). The depth-1 argument for rejecting the alternative is traced to the capabilities file and is hedged where the call sites were not traced (SPEC:33; CAPS:103).
- Interface segregation: the `--unattended` switch names the condition, not a tool (SPEC:260), and the shared rules live in one installed file (SPEC:52). Newman's backward-compatibility question is answered by SA-1 to SA-4 (SPEC:146-149). One residue: M10.
- Findings: M2 (a static check that contradicts the spec's own allowance), M5 (stale contract on reused directories), N3, N5. No architecture finding is blocking.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Five attack methodologies applied to the spec's own guards (not a correctness-focus run, so one most-impactful attack per methodology where one exists).

1. **Zero/Empty Attack.** Invariant at **WC-4 (SPEC:62)** fails when **the brief names no output directory in unattended mode**. Concrete attack: coordinator sends `/sc:tdd "<component>" --unattended` and forgets `--output` (section 3.1 says the brief "must pass" it, SPEC:90, but no text says what the command does without it). Before: no `--output`, WC-4 needs `<output-dir>`. After: the spec defines neither refusal nor a default, so one implementer refuses, another writes beside the input, a third falls back to an existing default (`docs/[domain]/...`, INV-B:222). Graded M4.
2. **Divergence Attack.** Invariant at **section 3 gate rows (SPEC:83-84, 89, 103, 110, 118)** fails when **`--unattended` and `--interactive` are both passed**. Concrete attack: cleanup, improve and roadmap say `--interactive` is "refused" under `--unattended` (SPEC:103, 110, 118); adversarial, brainstorm and release-split only say "never `--interactive`" in the brief column (SPEC:83-84, 89). If a brief carries both, adversarial would run its four AskUserQuestion checkpoints (INV-A:35) while the contract says no person is present. Graded M6.
3. **Sentinel Collision Attack.** Invariant at **WC-5 (SPEC:63)** fails when **a legitimate existing `status` value equals none of the four fixed values**. Concrete attack: workflow already writes a `status` (INV-B:272); the spec fixes the vocabulary to `succeeded|partial|failed|blocked` (SPEC:62, 262) and also says existing contracts "keep their fields" (SPEC:62). If workflow's existing values differ, one of the two sentences must lose. The existing values were not inventoried. Graded M3. Minor collision N3: contract `blocked` shares its word with Orca's Task status `blocked` (CAPS:89), but WC-5 maps it to `--outcome failed`, so no behavior depends on the shared word.
4. **Sequence Attack.** F1 above, plus: Invariant at **WC-4 / 7.2 step 4 (SPEC:62, 183)** fails when **a retry worker reuses a directory that already holds a prior contract**. Concrete attack: attempt 1 of `/sc:brainstorm --resume-from <seed-brief>` writes `<out>/return-contract.yaml` with `status: succeeded`, then the retry (`--retry-of`, SPEC:64) starts in the same `<out>` (resume commands reuse their directory, WC-6) and the session dies before rewriting. The coordinator's step 4 (`test -s`, status in set) passes on the stale file. WC-4 says "written on every outcome" but says nothing about removing or stamping the previous file at start. Graded M5.
5. **Accumulation Attack.** No counter, buffer or collection in the spec grows without a stated bound that matters to its requirements; the 3600 s eval wait is bounded by the 4-minute split rule (SPEC:68). One edge only: N5.

## Guard Condition Boundary Table

Trigger present: the spec contains thresholds and guards (60 s readiness, 5 min heartbeat, 4 min wait, depth 1, 0.70 confidence, status mapping). Responsibility: Nygard builds, Crispin validates completeness, Whittaker attacks. Crispin was not seated; completeness was checked by Nygard against section 2.2 and 3, and that gap is noted in the coverage statement. Classes left out are justified inline.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome map | SPEC:63 | Zero/Empty | no contract file | no report | `--outcome failed` | OK |
| WC-5 outcome map | SPEC:63 | One/Minimal | `status: succeeded` | pass | `--outcome succeeded` | OK |
| WC-5 outcome map | SPEC:63 | Typical | `status: partial` | pass | `--outcome succeeded`, body says partial (SPEC:263) | OK |
| WC-5 outcome map | SPEC:63 | Sentinel Value Match | `status: blocked` (word also an Orca Task status, CAPS:89) | false for success | `--outcome failed` | OK (see N3) |
| WC-5 outcome map | SPEC:63 | Legitimate Edge Case | audit verdict FAIL, run completed | pass | `--outcome succeeded` | OK |
| WC-5 outcome map | SPEC:62-63 | Legitimate Edge Case | existing contract `status` outside the four values | undefined | unspecified | GAP (M3) |
| WC-5 outcome map | SPEC:63 | Maximum/Overflow | n/a: scalar field, no capacity | n/a | n/a | left out: no capacity |
| WC-4 output dir | SPEC:62 | Zero/Empty | unattended, no output flag or dir | undefined | unspecified | GAP (M4) |
| WC-4 output dir | SPEC:62 | One/Minimal | `--output <dir>` of a directory-valued command | pass | contract at `<dir>/return-contract.yaml` | OK, except adversarial and workflow (F1) |
| WC-4 output dir | SPEC:62, 87, 90, 120 | Sentinel Value Match | `--output <file>` (tdd, init-lite, spec-panel are file-valued) | undefined | contract location unspecified | GAP (M1) |
| WC-4 output dir | SPEC:62, 64 | Legitimate Edge Case | directory already holds a prior contract (resume or retry) | undefined | unspecified | GAP (M5) |
| WC-4 output dir | SPEC:62, 92 | Zero/Empty (pre-creation stop) | no package directory exists | contradicts | unspecified | GAP, blocking (F1) |
| WC-4 output dir | SPEC:62 | Maximum/Overflow | n/a: a path, no capacity | n/a | n/a | left out: no capacity |
| WC-10 wait split | SPEC:68 | Zero/Empty | no blocking call | pass | nothing to split | OK |
| WC-10 wait split | SPEC:68 | Typical | 3 min call | below 5 min | no split | OK |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | 3600 s eval | above 5 min | split to waits of at most 4 min | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | call of exactly 5 min against a 5 min heartbeat | not "longer than 5" | heartbeat falls due as the call ends | OK, minor (N5) |
| WC-2 confidence gate | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | not "below 0.70" | proceeds | OK |
| WC-2 confidence gate | SPEC:121 | Zero/Empty | confidence 0 | below 0.70 | blocked, contract written | OK |
| WC-2 gate vs flag | SPEC:83-84, 89, 103, 110, 118 | Legitimate Edge Case | `--unattended` with `--interactive` | split by command | refused for 3 commands, silent for 3 | GAP (M6) |
| Readiness limit | SPEC:59 | Typical | wrapper fallback 30 s | under 60 s | passes (CAPS:49) | OK |
| Readiness limit | SPEC:59 | Maximum/Overflow | fallback near or above the limit | fails | "well inside" with no number; evidence threshold was for a 45 s limit | OK, minor (N2) |
| Nested depth | SPEC:66 | One/Minimal | worker calls `worker-start` | depth 2 | refused, WC-8 forbids the call | OK |

Every cell is populated, every guard enumerated, every omitted class carries its reason (FR-10 satisfied). GAP rows were graded with the grading check: only the WC-4 pre-creation row is blocking (F1); the rest are Medium (FR-8, FR-9).

## Quantity Flow Diagram (pipeline: inventory to spec to phases)

```text
[Inventory A: 21 commands] --> [verdicts 5 ready / 13 change / 3 coordinator-only] (INV-A:73)
[Inventory B: 22 commands] --> [verdicts 5 ready / 14 change / 3 coordinator-only] (INV-B:278)
                                   |  sum: 43 = 10 / 27 / 6
                                   v
[Spec section 3.1: 10 rows][Spec section 3.2: 27 rows][Spec section 4: 6 rows] = 43   (SPEC:76, 78-125, 127-137)
                                   |
                                   v
[Phases: P1 9 (+4 ready-with-fix) | P2 11 (+4 ready-with-fix) | P3 4 | P4 3] (SPEC:158-162)
   change commands: 9 + 11 + 4 + 3 = 27   OK, equals section 3.2
   ready commands touched with a phase: 4 + 4 = 8 of 10
[brainstorm, init-lite: 2 ready commands in no phase's Commands list]  <-- not a count mismatch
   (covered only by the P1 sentence "the --unattended flag accepted by every command in 3.1 and 3.2", SPEC:159; AC-1.1 asserts all 37, SPEC:195)  see N1
[Section 4: 6 commands] --> [0 phases, AC-1.1 asserts none has the section]  OK
```

No dimensional mismatch: totals conserve at every stage. FR-19 CRITICAL does not apply.

## Coverage

Read in full: `command.md`, the review-loop prompts file, README, the candidate (285 lines), `lint-1.md`, `commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Checked against workspace files: all `INV-A:N`, `INV-B:N`, `CAPS:N`, `README:N` citations the spec uses to define the 10/27/6 split, the phase lists, the gate rows, the unattended-mode terms and the Orca facts (about 60 spot checks; each located and consistent, except the points in N2, N4 and M7). Counts recomputed by hand (SPEC:76, 158-162).

UNVERIFIED (cited by the spec, not present in this workspace, so not checked): every `cmd/...`, `sk/...`, `src/superclaude/...`, `tests/...`, `pyproject.toml`, `Makefile`, `CLAUDE.md:N`, `src/superclaude/core/HOW-WE-WORK.md:N` citation (for example SPEC:25, 52, 74, 146-150, 183); `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:N` (only the quotes of lines 35, 39, 45, 56 inside CAPS:49, CAPS:52 were checked); `.dev/codegraph-migration/...:N` (only the quotes in CAPS:156 and INV-A:13-14, INV-A:60); the spec's own claims at SPEC:11 and SPEC:285 about re-reads and an independent citation check; Orca guide text keyed in CAPS:10-21.

Not covered: testing and compliance focus areas (not requested); the correctness focus (State Variable Registry not required); live behavior of any command; whether the 43-command split is right beyond consistency with the inventories.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

Medium (warnings):

- **M1 (Wiegers).** WC-4 defines `<output-dir>` as the `--output` / `--output-dir` directory (SPEC:62), but tdd, init-lite and spec-panel take `--output <file>` (SPEC:87, 90, 120), and research writes a timestamped file (SPEC:116). The contract location for these is not stated. The definition file for this very command already treats `--output` as file-valued and uses `--report-dir <dir>` for the contract (`command.md:22-23, 460-461`), a different surface from the spec's `--output` for spec-panel (SPEC:120). Reconcile the flag name per command in one table.
- **M2 (Fowler).** SA-2 allows one Orca mention "inside the contract file" (SPEC:147); the contract file and the P0 HOW-WE-WORK Orca section both live in `src/superclaude/core` (SPEC:52, 158, 150), which AC-C1 scans and requires to print nothing in every phase, P0 included (SPEC:172). Any literal `orca orchestration ask` in those files would fail AC-C1. State the permitted wording or exclude those two files from the grep.
- **M3 (Adzic).** WC-4 fixes the `status` vocabulary and also says existing contracts keep their fields (SPEC:62, 262). Existing `status` values (workflow has at least `failed`, INV-B:272) were not listed, so compatibility is asserted, not shown.
- **M4 (Nygard).** Unattended run with no output flag or directory: behavior unspecified (guard table row). Say refuse, or name the default.
- **M5 (Nygard).** A reused output directory (resume, `--retry-of`) can hold a stale `return-contract.yaml` that passes 7.2 step 4 (SPEC:64, 183). Say the command removes or overwrites the file at start, or that the check compares timestamps.
- **M6 (Whittaker).** `--unattended` with `--interactive`: refused for cleanup, improve, roadmap (SPEC:103, 110, 118), only forbidden by the brief for adversarial, brainstorm, release-split (SPEC:83-84, 89). Make the refusal uniform.
- **M7 (Cockburn).** E3 cites `invocation_method: "skill-direct"` as evidence that the approach worked (SPEC:23), then section 1.4 says the same run "proves the nested route, not the direct route" (SPEC:43). Both are hedged but they point opposite ways. The scenario is evidence for Phase 0, not for the decision; say so once.
- **M8 (Adzic).** Section 2.3 says every brief carries `--unattended` (SPEC:73) and 7.2 step 4 asserts the four-value status vocabulary (SPEC:183), but P0 smoke runs use commands without that flag and with their existing contracts (SPEC:158, 194). AC-0.4 patches this for step 4 only; step 1 and the brief template still say `--unattended`.
- **M9 (Cockburn).** "Phases 1-3 need no user decision" (SPEC:154) sits beside D1, the flag-versus-detection choice that the whole contract depends on (SPEC:227-230), and the section 9 line "can proceed on the recommendations" (SPEC:225). Reword to "proceed on the recommended answers".
- **M10 (Newman).** Fixes that edit existing standalone lines (business-panel frontmatter whose load effect is UNVERIFIED, validate-tests default target) are carved out of SA-1 by SA-4 (SPEC:102, 125, 149) while SA-1 says every default stays (SPEC:146). The carve-out is stated, but the business-panel effect is unknown, so SA-1 cannot yet be claimed for it.

Minor notes:

- **N1.** brainstorm and init-lite are in no phase's Commands list (SPEC:158-162); only the P1 scope sentence reaches them. `load` (SPEC:112) is also asked to carry a section that names `return-contract.yaml` by AC-1.1 (SPEC:195) although its row and Decisions say it writes no report (SPEC:112, 265).
- **N2.** WC-1 quotes "above about 45 s it fails again" (SPEC:59); the source says the 45 s was the limit given to that test, not the default (CAPS:49). Under the 60 s default the threshold is not shown.
- **N3.** Contract status `blocked` shares its word with Orca's Task status `blocked` (CAPS:89); mapping is explicit so no behavior depends on it.
- **N4.** SPEC:11 and SPEC:285 report re-reads and an independent citation check by the author's own session; those cannot be checked here and are treated as UNVERIFIED.
- **N5.** A single tool call of exactly 5 minutes ends as the heartbeat falls due (SPEC:68); a 4-minute bound for the longest call would also cover this edge.

Issue question: the session that ran the review asks the user once per loop whether to open an issue for the follow-up candidates and creates none without an answer. This run had no user to ask, so no issue was created and the list is only recorded; the coordinator carries the question.

## Reviser brief

Applies to the blocking finding ids only: **F1**.

1. Revise only text that F1 names: SPEC:62 (WC-4), the adversarial row (SPEC:83), the workflow row (SPEC:92), live-check step 3 (SPEC:182) and AC-1.4 (SPEC:198). Make the contract location one rule that the rows and the checks share, and give the workflow pre-creation stop a stated path or a stated no-contract outcome.
2. Add no rule, mechanism or section that F1 does not call for. Prefer deleting or narrowing text to adding.
3. Each added paragraph or table cites the finding id F1.
4. Report the byte size of the candidate before and after, and the bytes added and deleted for F1.
5. Leave every Medium finding (M1 to M10) and every minor note (N1 to N5) alone, including through "apply all findings".
6. Return the candidate once; do not award yourself a PASS. The re-review (review 2 of 3) is run by the coordinator with a saved baseline copy of the current candidate and this report as the prior-findings file.

No brief clause was overridden: the coordinator's brief (FIRST-REVIEW prompt, lint, output path) did not widen the scope or regrade any minor finding.

verdict: FAIL
