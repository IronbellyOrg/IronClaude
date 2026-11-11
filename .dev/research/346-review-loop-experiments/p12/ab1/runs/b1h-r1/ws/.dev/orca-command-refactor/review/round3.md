review: 3 of 3
> verification (coordinator, VERIFY step VF3; verifier reply .dev/orca-command-refactor/review/verify-3.md): confirmed blocking ids: N2, N4. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: none. The Reviser brief below is narrowed to the confirmed ids.

# Re-review 3 of 3: orca-worker-contract-spec.md against spec-v2 (`/sc:spec-panel --mode critique --focus requirements,architecture --re-review round2.md --baseline spec-v2.md`)

## Header and inputs

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 `1a2d2f425ac57ef3f2392d0bfdf09996e8bf26606b0e7b94ee731ab5d177867d`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md` sha256 `260c7c0ee1cfff6f147fa7f24960981dd4f6f1f953afdeef2b24a0b090d875da` (the same hash as the candidate that review 2 read, `review/round2.md:8`)
- prior: `.dev/orca-command-refactor/review/round2.md` sha256 `5e9e713cb61203c02ecd33a28c9c90d4aa149e3fe3041b7a222dcaa432480e29` (header `review: 2 of 3`, last line `verdict: FAIL`, `round2.md:1-2,162`; verifier reply `review/verify-2.md` sha256 `72a418b31f5a82b88533f89158a83773ff7900e0b97c23adf1219f9fd3249e92`, `confirmed: N1, N2`, `verify-2.md` last line)
- review prompt: `~/.claude/rules/prompts/document_review_loop_prompts.md` sha256 `ed219181156e47e6d70120730063e0b00081482d8a78b3d2633da188574ca829` (read in full; the RE-REVIEW prompt and its roles table were followed)
- reviewer model: claude-haiku-5-5
- review number: prior N = 2, so this is `review: 3 of 3`. This is the third and last review. No fourth review is run; an open blocking finding escalates to the user.
- Unattended mode: not requested; `~/.claude/WORKER-CONTRACT.md` was not needed and was not read.
- rf-qa.md: no project `.claude/agents/rf-qa.md` exists in this sandbox, and `~/.claude/agents/rf-qa.md` is absent from the sandbox home (`home/.claude/`). The fix-cycle steps 1-5 could not be applied; the rules of the Review Loop's re-review bullet stand alone.
- Line references: `spec:N` = line N of the candidate; `base:N` = line N of spec-v2; `INV-A:N`, `INV-B:N`, `CAPS:N` = the inventory files under `inventory/`.
- Evidence limit: the `cmd/`, `sk/`, `src/` and `plugins/` files that the spec cites are not in this sandbox. Any citation to them is UNVERIFIED here. Inventory citations I re-read are marked as checked.
- VERIFY: not run. This worker has no fresh-context verifier. The Review Loop's VERIFY prompt still applies at `review: 3` with an open blocking finding (`command.md` Review Loop bullet 4; prompt file, "At `review: 3`"). The coordinator must run it (step VF3) on N2 and N4 below before escalation. See the verdict section.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

`diff -w spec-v2.md orca-worker-contract-spec.md` exits 1 and has two changed hunks: `62c62` and `204c204`. Changed lines are copied verbatim.

BEFORE (baseline), lines starting `<`:

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate), lines starting `>`:

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). For a command whose output flag names a file (`--output <file>`, as in tdd and init-lite), the contract is not `<output-dir>/return-contract.yaml` but `<parent>/<stem>.return-contract.yaml`, where `<parent>` is that file's parent directory and `<stem>` is its file name without its extension, so two runs whose files share a parent directory write two contracts [M1, N2]. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended` and the one output flag section 3 names for it (`--output-dir <dir>` for cleanup-audit, index-repo and workflow; `--output <dir>` for the others) [N1] | all steps pass |
```

Changed lines against the baseline, with origin: changed = spec:62 and spec:204. Every other candidate line is origin=unchanged.

## Step 1 self-check (`grep -nF` of every quoted line)

- 2 AFTER lines (without `> `) were each found once in the candidate (`grep -cF` = 1 for both).
- 2 BEFORE lines (without `< `) were each found once in spec-v2 and 0 times in the candidate.
- The roles were not swapped.

## Prior blocking findings (from review 2) and their status

Review 2 confirmed N1 and N2 as blocking (`review/verify-2.md`, `confirmed: N1, N2`). N3 was rejected and is a note (see "Noted, unactioned"). M1 to M10 were marked resolved in review 2 and are not carried as blocking here. The only one whose text this revision touches is M1 (in spec:62), and M1 stays resolved.

| id | status | where the candidate answers it | note |
|---|---|---|---|
| N1 | resolved | spec:85 (cleanup-audit `--output-dir`), spec:86 (index-repo `--output-dir`), spec:92 (workflow `--output-dir`), spec:204 (AC-1.2 names `--output-dir` for these three) | The flag now agrees between the rows and AC-1.2 for cleanup-audit, index-repo and workflow. The residual "others" clause in spec:204 is a new finding (N4, F1), not a failure of N1. |
| N2 | open | spec:62 | The review 2 example (`--output .dev/superclaude/a.md` and `b.md`) is fixed: the contracts are now `a.return-contract.yaml` and `b.return-contract.yaml`. The defect class is not fixed: two runs with the same stem and different extensions in one directory still write one contract path (finding N2 below). |
| N3 | noted, unactioned | spec:193 and spec:202 are unchanged from spec-v2 | Rejected by the verifier (`review/verify-2.md`). A rejected id is a note, not a prior blocking finding for this re-review. |

No prior blocking finding is `regressed`.

## Findings on changed lines

### N2 (blocking, open, origin=changed; spec:62)

- Location: `spec:62` (WC-4, changed). Depends on `spec:69` (WC-11, unchanged: "Two workers in one worktree must never write the same file.").
- Quote, spec:62: "where `<parent>` is that file's parent directory and `<stem>` is its file name without its extension, so two runs whose files share a parent directory write two contracts [M1, N2]."
- Grading sentence: an implementer who follows `spec:62` as written runs `--output .dev/superclaude/a.md` for one command and `--output .dev/superclaude/a.txt` for another (both accept a file, `spec:87` and `spec:90`). Both contracts go to `.dev/superclaude/a.return-contract.yaml`. The second run overwrites the first, so the coordinator opens a contract that describes the wrong worker, and the first worker's report is lost. The sentence that says files sharing a parent directory write two contracts is false for this pair, so the stated text contradicts its own rule. No further assumption is needed for the overwrite; the input pair is the only premise, and the rule gives it no exception.
- Scope of the premise: no command in section 3 writes two extensions today. The defect is reached only through the choice of inputs, which is why this is graded with the same weight as review 2's N2 (a wrong contract read and a lost report), not as a Medium warning.
- Expert: Newman (shared interface artifact: one contract name per output stem); Whittaker (sentinel collision: a derived name shared across runs).
- Recommendation: key the contract on the full output file name (for example `a.md.return-contract.yaml`), or require a per-run directory for file-valued outputs, or reject a second run whose contract path already exists. Then correct the claim in `spec:62` to match the rule. Each option is a one-line edit to `spec:62`.
- Priority: High (wrong contract read, lost report).

### N4 (blocking, new, origin=changed; spec:204)

- Location: `spec:204` (AC-1.2, changed). Depends on `spec:112` (load row, unchanged), `spec:159` (P1 list, unchanged), `spec:186-188` (7.2 live check, unchanged), and the section 3 rows for the P1 commands (`spec:101-125`, unchanged).
- Quotes:
  - `spec:204`: "7.2 live check on each P1 command with `--unattended` and the one output flag section 3 names for it (`--output-dir <dir>` for cleanup-audit, index-repo and workflow; `--output <dir>` for the others)".
  - `spec:112`: "| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; ... | P1 (usage line only) |".
  - `spec:159`: P1 "Commands" column lists "analyze, build, business-panel, design, document, explain, index, test, load (usage line only)".
  - `spec:188`: 7.2 step 1 is "`ORCA orchestration task-create --spec ...`, then `ORCA orchestration worker-start ...`", run "For each command under test".
- Grading sentence: an implementer who follows `spec:204` as written dispatches `/sc:load --unattended --output <dir>` as its own Task (7.2 step 1), which `spec:112` forbids ("not as its own Task"). Section 3 names no output flag and no report file for load (`spec:112` "none"), so there is no `--output <dir>` to pass and no contract for the step-4 `test -s <contract>` (`spec:191`) to test. Two stated texts contradict each other, and the criterion cannot pass as written. Both points hold with no further assumption. `INV-B:31` and `INV-B:65` say load "writes no file; use as a brief step, not a task", and `INV-B:293` lists `/sc:load` among commands with no single report file, so the inventory agrees with `spec:112`.
- Origin note: the contradiction is also in spec-v2 (`base:204` names the same P1 set and "each P1 command"). Review 2 checked only the changed lines and did not raise it. It is graded here because `spec:204` is a changed line that carries it, and the new "one output flag section 3 names for it" clause depends on the same row.
- Expert: Adzic (an acceptance criterion its own scope rule cannot satisfy); Wiegers (traceability from the P1 list to the row that says the command is not a Task).
- Recommendation: either remove load from AC-1.2 and check its usage-line fix by a grep for `--checkpoint` in its Usage line (`INV-B:31`), and state that exclusion in `spec:159`; or give load its own row with a report file and a named flag, and drop the "use it as a step" wording in `spec:112`.
- Priority: High (blocks the P1 gate for one command).

### Medium follow-up candidates (not blocking)

- F1 (Medium, origin=changed, `spec:204`): the clause "`--output <dir>` for the others" names a flag that section 3 does not name for seven P1 commands: build (`spec:101`: "add a report path; contract"), design (`spec:106`: "add an output path"), business-panel (`spec:102`: "add an output path"), index (`spec:111`: "add an output path"), test (`spec:123`: "add a report path"), explain (`spec:108`: "write the explanation to a file"; a file, not a directory) and document (`spec:107`: "require an explicit output"). The spelling and the file-or-directory kind are not stated, so an implementer must guess. Medium under the grading rule (a requirement the document never states).
- F2 (Medium, origin=unchanged, quotes `spec:62`): the Decisions row at `spec:269` says "Reuse: ... `return-contract.yaml` ... so one name lets the coordinator check every worker the same way." The revised `spec:62` gives tdd and init-lite (file-valued outputs) `<stem>.return-contract.yaml` instead. The rationale and the rule now disagree. Update the row when N2 is fixed.

### Noted, unactioned

- N3 (rejected by the verifier, `review/verify-2.md`, `confirmed: N1, N2`; origin=unchanged; `spec:193` and `spec:202` are unchanged from spec-v2). The verifier's reason stands: step 6 applies its pass rule only to a "report-only command", and the candidate never places `/sc:workflow` or `/sc:troubleshoot` in either class. This is a note. A coordinator may still want the classification stated, but it does not block under the Review Loop.
- Coordinator note: `review/round2.md:156` lists "Blocking finding ids: N1, N2, N3" in its Reviser brief, although its own verification block (`round2.md:2`) says the brief is narrowed to the confirmed ids. This report treats N3 as noted, as the VERIFY rule requires.

### Checked and not raised

- N1 resolution: `spec:85`, `spec:86`, `spec:92` and `spec:204` agree on `--output-dir` for cleanup-audit, index-repo and workflow; the `--output` / `--output-dir` pair in `spec:62` is not contradicted.
- The `<stem>.return-contract.yaml` form still contains the string `return-contract.yaml`, so the AC-1.1 check at `spec:203` ("names `return-contract.yaml`") still matches.
- `spec:73` (the brief states the output directory, WC-4) is unchanged and still covers the case of no output flag.
- Pipeline Dimensional Analysis (`command.md` Review Heuristics, FR-17): not triggered by the changed lines, which add no multi-stage data flow.
- Focus is requirements and architecture, not correctness: the State Variable Registry and the Pipeline Flow Diagram are not mandatory here.

## Guard Condition Boundary Table (changed guards only; FR-8 to FR-10)

Guard 1 is the WC-4 file-valued output derivation (`spec:62`). Guard 2 is the AC-1.2 flag selection (`spec:204`). Input classes that do not apply are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 file-valued derivation | spec:62 | Zero/Empty: no output flag given | no `--output` | n/a (not file-valued) | the brief must pass the output directory (`spec:73`); no command-side fallback is stated, which the brief rule covers | OK (covered by spec:73) |
| WC-4 file-valued derivation | spec:62 | One/Minimal: one file-valued run | `--output a.md` | `<parent>/a.return-contract.yaml` | one contract in the parent directory | OK |
| WC-4 file-valued derivation | spec:62 | Typical: two runs with distinct stems in one directory | `a.md` and `b.md` | two distinct contracts | review 2 example fixed | OK |
| WC-4 file-valued derivation | spec:62 | Sentinel Value Match: the output file is itself named as the contract | `--output return-contract.yaml` | `return-contract.return-contract.yaml` | no collision | OK |
| WC-4 file-valued derivation | spec:62 | Legitimate Edge Case: same stem, different extension, same directory | `a.md` and `a.txt` | both `a.return-contract.yaml` | second run overwrites first (N2) | GAP (N2, blocking) |
| WC-4 file-valued derivation | spec:62 | Maximum/Overflow | n/a | n/a | left out: the rule has no count or capacity threshold | left out |
| AC-1.2 flag selection | spec:204 with spec:85, 86, 92 | Zero/Empty: P1 command with no output flag in section 3 | load (`spec:112` "none") | n/a | AC-1.2 still runs it, as its own Task | GAP (N4, blocking) |
| AC-1.2 flag selection | spec:204 with spec:99 | One/Minimal: a P1 command whose row adds `--output` | analyze (`spec:99`: "add `--output`") | `--output <dir>` | matches the row | OK |
| AC-1.2 flag selection | spec:204 with spec:85 | Typical: a P1 command whose row names `--output-dir` | cleanup-audit (`spec:85`) | `--output-dir <dir>` | matches the row | OK |
| AC-1.2 flag selection | spec:204 with spec:86 | Legitimate Edge Case: index-repo, given the wrong spelling | `--output <dir>` vs `--output-dir` | flag rejected | the spec now names `--output-dir` (review 2 N1) | OK after the change |
| AC-1.2 flag selection | spec:204 with spec:101, 102, 106, 107, 108, 111, 123 | Legitimate Edge Case: P1 command whose row names a report path, not a flag | build, design, business-panel, index, test, explain, document | `--output <dir>` assumed | the flag name and file-or-directory kind are not stated | GAP (F1, Medium) |
| AC-1.2 flag selection | spec:204 | Maximum/Overflow; Sentinel Value Match | n/a | n/a | left out: the rule has no numeric threshold or sentinel value | left out |

## Coverage

Scoped: changed lines (`spec:62`, `spec:204`) plus prior blockers N1 and N2, as the coverage line requires. I ran `diff -w`, the self-check, and read the prior report, the verifier reply, the prompt file and the candidate. I re-read the inventory citations for load (`INV-B:31`, `INV-B:57-65`, `INV-B:293`). I did not check the `cmd/`, `sk/`, `src/` or `plugins/` citations, because those files are not in this sandbox; those citations are UNVERIFIED here. `CAPS:72-74` and `CAPS:79`, quoted in the unchanged parts of the WC-4 row, were not re-read.

## Follow-up candidates

- F1 (Medium): AC-1.2's "`--output <dir>` for the others" names no flag for seven P1 commands (`spec:101`, `spec:102`, `spec:106`, `spec:107`, `spec:108`, `spec:111`, `spec:123`).
- F2 (Medium): the Decisions rationale at `spec:269` conflicts with the stem-based contract name at `spec:62`.
- Not raised as a finding: no minor finding has `origin=changed`.

## Escalation and verdict

- This is `review: 3 of 3`, the cap. No fourth review is run. The Reviser brief is omitted at `review: 3` (Review Loop bullet 6), and nothing is revised by this run.
- Open blocking findings to escalate to the user: N2 (open) and N4 (new).
- VERIFY (prompt file, "At `review: 3` with an open blocking finding the VERIFY prompt still runs"): not run here. The coordinator must brief a fresh-context verifier with the verify brief, the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` and the list "N2, N4" only, and write its table in a verification block after the header. A missing or unclear reply confirms both findings (prompt file, VERIFY "After the reply"). If the verifier confirms neither, the verdict becomes a PASS with the noted list and follow-up candidates given to the user, per the VERIFY rule. Until then the verdict is FAIL.

verdict: FAIL
