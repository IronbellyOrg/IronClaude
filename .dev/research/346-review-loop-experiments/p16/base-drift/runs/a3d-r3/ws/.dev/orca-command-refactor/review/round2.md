review: 2 of 3

# Spec panel review, round 2 (re-review): orca-worker-contract-spec.md

- Mode: `--mode critique`, `--focus requirements,architecture`, `--re-review review/round1.md --baseline specs/history/spec-v1.md`. `--iterations` ignored, Improve step skipped, no revised specification written (Review Loop bullet 4).
- Prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full first, including its Never section). No brief clause overrode the command.
- Roles (fixed by the table in the prompt, not inferred): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`.
- sha256 CANDIDATE: `ee66feb509d270d43ad6b910ad610ca80e6ec53ce17ddf42d33226ff403c6470`
- sha256 BASELINE: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in round1.md, so the baseline is the text round 1 reviewed)
- sha256 PRIOR: `cadc37b864268dd602f3ae367a7dfbe8dac452c0d718a6dcd20179ef79883ca4` (header `review: 1 of 3`, so N = 2)
- Reviewer model actually used: claude-sonnet-5-5
- Date: 2026-11-10
- Notation: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `INV-A:N`, `INV-B:N` = lines of `inventory/commands-a.md`, `commands-b.md`; `R1:N` = line N of `review/round1.md`; `REV1:N` = line N of `review/revise1.md`.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Both files have 285 lines; the diff touches 5 lines (62, 73, 116, 120, 183), all in the same positions. Lines below are copied verbatim from the diff output.

```text
BEFORE (baseline), lines starting '<':
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
< | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output`; contract | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.

AFTER (candidate), lines starting '>':
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). When `--output` names a file, the contract is the sibling file `<file-stem>.return-contract.yaml` in that file's directory (for `docs/auth/TDD_AUTH.md`: `docs/auth/TDD_AUTH.return-contract.yaml`) (F-1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, or for a file-valued `--output` the file path, so the report path is known before dispatch (WC-4, F-1); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification); add `--output <file>` (F-1) | contract beside the `--output` file (WC-4), naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
> | spec-panel | `target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks | add `--output <file>`; contract beside it (WC-4, F-1) | fresh dir | none | `cmd/spec-panel.md:22,34-35,222,451,455`; `INV-B:43,177-185` | P2 |
> 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0. For a file-valued `--output`, `<contract>` is the WC-4 sibling path (F-1).
```

Self-check (run): every AFTER line (without its `>`) was found with `grep -cF` in the CANDIDATE and not in the BASELINE (5 of 5 each way). Four BEFORE lines (without `<`) were found in the BASELINE and not in the CANDIDATE; the fifth (the AC step 4 line, `BASE:183`) is found in both because the AFTER line (`SPEC:183`) only appends a sentence to it. No role swap.

Net change in words (what the diff shows): WC-4 gains one sentence (sibling file rule); section 2.3 gains "or for a file-valued `--output` the file path"; the research row adds `--output <file>` and "contract beside the `--output` file"; the spec-panel row says `--output <file>` and "contract beside it"; AC step 4 says `<contract>` is the WC-4 sibling path for a file-valued `--output`. Each addition cites F-1.

## What was covered

- Read in full: command definition, README, review-loop prompts, PRIOR report, `revise1.md`, the 5 changed lines and the diff.
- Read around the changed lines: `SPEC:60-76` (WC-1..WC-12, section 2.3, section 3 intro), `SPEC:83-92`, `SPEC:99-125`, `SPEC:176-200`, plus the inventory lines the changed rows cite (`INV-A:55`, `INV-B:127-135`, `INV-B:177-185`).
- Grepped the whole candidate for `return-contract`, `--output`, `output-dir`, `report-dir` to find text that depends on the changed lines (results used below).
- Not covered: whole-document assurance (the rest of the candidate is unchanged from the baseline and was reviewed in round 1). Citations to `CLAUDE.md:*`, `src/superclaude/**`, `.dev/codegraph-migration/**` remain UNVERIFIED in this sandbox, as in round 1; no finding below depends on them. No command was run beyond `diff`, `grep`, `sha256sum`; no Orca call; the candidate was not edited.

## Expert sequence (summary lines)

1. Wiegers: WC-4 now has a testable rule for both forms (directory and file). Open points are Medium (R2-M2, R2-M3).
2. Adzic: the concrete example in WC-4 (`docs/auth/TDD_AUTH.md` gives `docs/auth/TDD_AUTH.return-contract.yaml`, `SPEC:62`) makes AC-2.2 step 4 runnable (`SPEC:183`, `SPEC:200`).
3. Cockburn: no change to actor or goal.
4. Fowler: the sibling-file rule adds no flag and no mechanism; it narrows to one sentence, as round 1 asked (`R1:45`).
5. Nygard: no new failure mode on the changed lines beyond R2-M2/R2-M3.
6. Whittaker: attacks below; none breaks the changed text.
7. Newman: the contract name now has two forms; consumers that glob `return-contract.yaml` still match (suffix match), see the AC-1.1 check in the table below.
8. Hohpe: `worker_done --report-path` carries the sibling path; no change to message flow (`SPEC:62`).
9. Crispin: AC-2.2 step 4 covers the file-valued case via `SPEC:183`; no check covers the same-stem edge (R2-M3).
10. Gregory: `revise1.md` records its own open point (`REV1:24`); it is carried as R2-M2.
11. Hightower: no finding.

## Prior blocking findings (re-check against the AFTER text only)

Re-check followed the Fix Cycle steps 1-5 of `rf-qa.md` as far as they apply (that file is not in the sandbox: UNVERIFIED which steps they are; the rules of the command section stand alone): take each prior blocking finding, read its defect from PRIOR, compare with the AFTER text, grade by consequence.

| Id | Prior status | Now | Evidence (AFTER text) |
|---|---|---|---|
| F-1 | open (blocking) at `R1:41-47` | **resolved** | The defect was that WC-4 put the contract at `<output-dir>/return-contract.yaml` while tdd, init-lite, spec-panel and research pass `--output` as a file, and AC-2.2 step 4 had no path to test (`R1:37`). `SPEC:62` now says: when `--output` names a file, the contract is the sibling file `<file-stem>.return-contract.yaml` in that file's directory, with the example `docs/auth/TDD_AUTH.md` giving `docs/auth/TDD_AUTH.return-contract.yaml`. An implementer who follows this builds a contract path that is not below the deliverable's name, so deliverable and report coexist. `SPEC:73` makes the coordinator put the file path in the brief, so the path is known before dispatch. `SPEC:183` defines `<contract>` for AC-2.2 step 4. The tdd row (`SPEC:90`) and init-lite row (`SPEC:87`) already passed `--output <file>` and are now covered by WC-4; research (`SPEC:116`) and spec-panel (`SPEC:120`) now pass `--output <file>` too. The "second worker in `docs/<domain>/`" collision that WC-11 forbids (`SPEC:69`, `R1:44`) does not arise: contract names carry the deliverable stem, so two workers with different deliverables get different contract paths. |

No prior blocking finding is open or regressed. The Medium and minor items of round 1 (M-1..M-11, notes) were not blocking, were left alone by the reviser (`REV1:3`), and are not re-graded here.

## Findings on lines changed against the baseline

None is blocking. Each uses the grading sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y."; none holds without an extra guess, so all are Medium.

=== REQUIREMENTS ANALYSIS ===

- **R2-M1 [MAJOR label, Medium] origin=changed. Research row names two deliverable locations (`SPEC:116`).** The row now says "add `--output <file>`" and the report column says "contract beside the `--output` file (WC-4), naming the generated `claudedocs/research_*.md` path". The inventory says the report is `claudedocs/research_[topic]_[timestamp].md`, generated at run time, with no output flag (`INV-B:132`, `INV-B:135`). The spec does not say whether `--output` replaces the generated path or only anchors the contract. Two readings, neither causes data loss or a contradiction; the implementer picks one. Medium.
- **R2-M2 [MAJOR label, Medium] origin=changed. How a command tells a file `--output` from a directory `--output` (`SPEC:62`).** The rule keys on "when `--output` names a file". Rows state the kind per command (`<dir>` at `SPEC:83`, `SPEC:84`; `<file>` at `SPEC:87`, `SPEC:90`, `SPEC:116`, `SPEC:120`), so each command's kind is fixed by its own row; for a path that does not exist yet, the rule does not say how the command decides. `REV1:24` records the same gap. Not a wrong build as long as each command follows its row; Medium.
- **R2-M3 [MINOR label, Medium] origin=changed. Same-stem deliverables (`SPEC:62`).** Two file-valued outputs in one directory with the same stem and different extensions (for example `X.md` and `X.json`) get the same contract name `X.return-contract.yaml`. WC-11 forbids two workers writing one file (`SPEC:69`). Nothing in the inventories shows such a pair, so the failure needs an unlikely brief; Medium.

=== ARCHITECTURE ANALYSIS ===

No architecture finding. The change adds no flag, no mechanism and no section (`SPEC:62` is one added sentence). The file-valued form keeps one contract per deliverable, which is consistent with R1-R5 and WC-4's "one report file" claim.

Minor notes (origin=unchanged unless said; none quotes a changed line that makes it wrong):

- `SPEC:76` still defines "Contract" as the WC-4 file `<output-dir>/return-contract.yaml` only; read with `SPEC:62` it is clear, so this is a note (origin=unchanged; depends on the changed `SPEC:62`, wording only).
- `SPEC:120` (changed line) keeps "fresh dir" in the resume column although `--output` is now a file; `SPEC:116` has "fresh file". Wording, no wrong outcome.
- AC-1.1 (`SPEC:195`) asserts the section names `return-contract.yaml`; the sibling name `<stem>.return-contract.yaml` contains that substring, so the check still holds for a file-valued command.

## Guard Condition Boundary Table (guards on changed lines only)

One guard is on the changed lines: "`--output` names a file" (WC-4, `SPEC:62`). The guard on the output argument being absent (`--output` omitted) is on an unchanged line and is already round 1's M-2; it is not re-tabled.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--output` names a file | WC-4, SPEC:62 | Typical | `docs/auth/TDD_AUTH.md` | true | contract `docs/auth/TDD_AUTH.return-contract.yaml` (example in SPEC:62) | OK |
| `--output` names a file | WC-4, SPEC:62 | Typical | `.dev/troubleshoot/login/` (directory) | false | `<output-dir>/return-contract.yaml` (SPEC:62, SPEC:228) | OK |
| `--output` names a file | WC-4, SPEC:62 | One/Minimal | file with no extension, `out` | true | stem `out`, contract `out.return-contract.yaml` follows from the stated rule | OK |
| `--output` names a file | WC-4, SPEC:62 | Legitimate Edge Case | path that does not exist yet, kind unclear | unspecified | decided by the command's own row (SPEC:83-87, 90, 116, 120); the general rule is silent | GAP (R2-M2, Medium) |
| `--output` names a file | WC-4, SPEC:62 | Legitimate Edge Case | `X.md` and `X.json` in one directory | true | both give `X.return-contract.yaml`; not stated | GAP (R2-M3, Medium) |

Left out: Zero/Empty (the omitted-`--output` case is on an unchanged line, round 1 M-2); Maximum/Overflow and Sentinel Value Match (no numeric limit or reserved value is introduced by the changed lines). FR-8/FR-9: the two GAP rows are graded by consequence and are Medium. FR-10: the table is complete for the changed guards, so synthesis proceeded.

## Quantity Flow Diagram

The changed lines do not touch a count or a pipeline stage. Counts are unchanged from round 1: 43 = 21 + 22; 10 ready + 27 needs-change + 6 coordinator-only; 285 lines in baseline and candidate (`wc -l`). No divergence point.

## Adversarial analysis (Whittaker, changed lines only)

- I can break this specification by **Divergence Attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--output` names a path whose kind is unclear**. Concrete attack: brief says `--output docs/auth/out` for a command whose row says `<file>`; before: no `docs/auth/out`; after: the command writes the deliverable to `docs/auth/out` and the contract to `docs/auth/out.return-contract.yaml`, consistent with the file form. Because each row fixes the kind, the invariant holds when the brief follows the row (R2-M2, Medium).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 (SPEC:62)** fails when **two deliverables share a stem**. Concrete attack: worker A writes `docs/x/API.md`, worker B writes `docs/x/API.json`; both contracts are `docs/x/API.return-contract.yaml`; before: neither exists; after: the second overwrites the first (R2-M3, Medium).
- **Zero/Empty, Sequence, Accumulation:** no attack succeeds on the changed lines (the sequence concern of `R1:113` is on unchanged text and stays a note).

## Quality assessment (0-10)

Clarity 7, Completeness 7, Testability 8, Consistency 7 (round 1: 7/7/7/6). The contradiction that blocked is gone.

## Follow-up candidates (Medium and minor; no revision, no failure)

1. R2-M1 research row: `--output` versus the generated `claudedocs/research_*.md` path (`SPEC:116`).
2. R2-M2 how the command decides file versus directory for a non-existent `--output` (`SPEC:62`, `REV1:24`).
3. R2-M3 same-stem deliverables give one contract name (`SPEC:62`).
4. Minor notes: `SPEC:76` definition names only the directory form; `SPEC:120` and `SPEC:116` resume column wording.
5. Carried from round 1, unchanged and not re-graded: M-1..M-11 and the round 1 notes (`R1:125-136`).

Question for the user, once per loop: open an issue for the follow-up candidates above? This sandbox has no user channel and no GitHub access; the list is only recorded and no issue was created.

Coverage: scoped PASS: changed lines + prior blockers

## Reviser brief

None: no blocking finding is open (F-1 resolved), so nothing is handed to a reviser. Medium and minor findings never trigger a revision.

verdict: PASS
