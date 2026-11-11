review: 2 of 3

# Spec-panel re-review (critique mode, focus requirements,architecture)

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`

## Header

| Role | File | sha256 |
|---|---|---|
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` | `a6e5c8f0ff0545238ba19f3f7d98a7d4329bb51a628932a5ec8669cc448da770` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| PRIOR | `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, `verdict: FAIL`) | `fe50c1dd172be7f2785a1f70bbcba6729224ff35fddff33b8a4647403e560b94` |
| LINT | `.dev/orca-command-refactor/review/lint-2.md` | `eec4ab821cead01d6ee1588d6043d29250757c4cb85e636b2f850fd3c18fa6b2` |

- Reviewer model actually used: claude-sonnet-5-5.
- Hard gate: `~/.claude/rules/prompts/document_review_loop_prompts.md` was read in full (RE-REVIEW prompt followed in order: roles, Step 1, review number, self-check).
- Evidence: only `inventory/*.md` (README.md:11-17 binding context). Spec citations use `spec:<line>` for the candidate. Citations to `cmd/...`, `sk/...` are not checkable in this sandbox and are marked UNVERIFIED where I rely on them. `rf-qa.md` (Fix Cycle steps 1-5) is not in this sandbox; the re-check below follows the Review Loop rules and stands alone.
- Review number: PRIOR header is `review: 1 of 3`, so N = 2. PRIOR is not at `review: 3`, so the escalation stop does not apply.
- Lint (lint-2.md:1-3): "Checks: REF. Findings: 0. No findings." There is no lint id to confirm or dismiss.
- Prior verification block (round1.md:7): M6 and M7 were rejected by the verifier and are notes, not prior blocking findings. They are not re-opened.

## Step 1: evidence block

`diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` gives 6 hunks (same line count, 285 each). Roles are fixed by the table above, not inferred.

### BEFORE (baseline), lines starting `<`

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern ... The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | ...
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< | P0 | AC-0.4 | ... | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

(Long table cells are abbreviated with `...` only where the text is unchanged; the changed words are quoted in full below.)

### AFTER (candidate), lines starting `>`

```text
> | WC-4 | **One report file, written on every outcome, with a path the coordinator can know.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output-dir`, or `--output` when it names a directory); when `--output` names a file (tdd, init-lite, spec-panel), `<output-dir>` is that file's parent directory; for `workflow` it is the package directory `.dev/tasks/to-do/<id>/`, or `.dev/tasks/to-do/` when a STOP comes before any `<id>` exists (M2). ... Where the command picks the directory itself (troubleshoot, workflow, `adversarial` under `<output>/adversarial/`), the coordinator reads the path from `worker_done --report-path` (M3). Orca does not check the file, so the coordinator opens it. | ...
> ... the exact command line including `--unattended` and every flag section 3 lists as required; the output directory where the command takes one, so the report path is known before dispatch (WC-4; otherwise it comes from `worker_done --report-path`) (M3); which outward actions, if any, are authorized (WC-9); ...
> 3. `ORCA orchestration check --wait ...` ... **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the command's named report (the WC-4 contract from P1 on) (M3).
> | P0 | AC-0.4 | ... | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1, and the report path is read from `worker_done --report-path` (M3). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | ... the test asserts that every command in sections 3.1-3.2 whose row adds a section (not `load`, and not a 3.1 row whose small-fix column is `None`) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one (M1) | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (it writes no contract, section 3.2) with `--unattended --output <dir>` | all steps pass (M4) |
> | P2 | AC-2.2 | Gate-trigger run per P2 command whose section 3 row resolves a gate as blocked (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, tdd, troubleshoot, release-split): a 7.2 live check ... | `worker_done --outcome failed`; contract `status: blocked` ...; step 2 never shows `agentWait` (M5). The other P2 commands (auggie-review, cleanup, improve, research, tasklist, reflect) have no blocked outcome; the same run on them must end `--outcome succeeded` with the default applied, step 2 never showing `agentWait` and step 5 showing no `AskUserQuestion` |
```

Candidate line numbers of the changed lines: spec:62 (WC-4), spec:73 (2.3), spec:182 (7.2 step 3), spec:194 (AC-0.4), spec:195 (AC-1.1), spec:196 (AC-1.2), spec:200 (AC-2.2). No other line differs; whitespace-only changes: none seen.

### Self-check (commands run)

`grep -nF` of the quoted AFTER fragments in the candidate: found at spec:62 (`when `--output` names a file (tdd, init-lite, spec-panel)` and `the coordinator reads the path from `worker_done --report-path` (M3)`), spec:195 (`(not `load`, and not a 3.1 row whose small-fix column is `None`)`), spec:200 (`The other P2 commands (auggie-review`). `grep -nF` of quoted BEFORE fragments in the baseline: found at spec-v1:182 (`its report path is the WC-4 contract path.`), spec-v1:196 (`each P1 command with `--unattended --output <dir>``). No quote was missing, so no role swap.

## Prior blocking findings

| id | prior defect (round1.md) | status | basis (AFTER text only) |
|---|---|---|---|
| M1 | AC-1.1 required a contract section on `load`, `brainstorm`, `init-lite`, which section 3 leaves without one | resolved | spec:195 now limits the test to rows that add a section and names the two exclusions. `load` row spec:112 (small fix = usage line only, "none (see note)" report) and Decision spec:265 are consistent with it; `brainstorm` (spec:84) and `init-lite` (spec:87) have "None" in the small-fix column, so they fall outside AC-1.1. The contradiction round 1 named is gone. See N1 for a separate Medium note on the same line. |
| M2 | WC-4 defined the contract location from a directory, but `tdd`, `init-lite`, `spec-panel` take a file in `--output`, and `workflow` has no `<id>` before a pre-creation STOP | resolved | spec:62 now gives a rule for each case: file-valued `--output` uses the file's parent directory (so `/sc:tdd ... --output <file>` in AC-2.2 at spec:200 has a defined contract path), and `workflow` uses `.dev/tasks/to-do/<id>/` or `.dev/tasks/to-do/` before an `<id>` exists. AC-1.4 (spec:198) can be checked against that location. The path-cannot-exist-beside-a-file outcome no longer follows. See N2 for a Medium note on shared-path collisions. |
| M3 | AC-0.4 required a Phase 0 contract that does not exist yet; "known before dispatch" could not hold for troubleshoot and workflow; adversarial name mismatch | resolved | spec:182 step 3 now reads "the command's named report (the WC-4 contract from P1 on)"; spec:194 says the report path is read from `worker_done --report-path`; spec:73 says the directory is passed "where the command takes one" and otherwise comes from `worker_done --report-path`; spec:62 names `adversarial` under `<output>/adversarial/`, which matches the adversarial row (spec:83). The report-path contradiction named in round 1 is gone. See N3 for a Medium note on the rest of step 3 and step 4. |
| M4 | AC-1.1 and AC-1.2 could not pass for `/sc:load` | resolved | spec:196 excludes `load` by name with its reason (section 3.2, spec:112); spec:195 excludes it too. |
| M5 | AC-2.2 demanded a `blocked` contract from P2 commands whose gate never resolves as blocked | resolved | spec:200 now lists the nine commands whose section 3 rows resolve a gate as blocked: cli-eval (spec:104 row text: "else blocked"), cli-portify (spec:105), recommend, review-translation, spec-panel, task, tdd (spec:90), troubleshoot (spec:91), release-split (spec:89). The six others (auggie-review, cleanup, improve, research, tasklist, reflect) are given a succeeded-with-default check. I compared each against its section 3 row (auggie-review spec:100, cleanup spec:103, improve spec:110, research spec:116, tasklist spec:122, reflect spec:88) and found no blocked outcome for any of the six. WC-5 (spec:63) maps `partial` to `--outcome succeeded`, so the cleanup/improve "apply allowed, list the rest" outcome is consistent with the new text. |

Rejected round-1 ids M6 and M7 stay noted, unactioned (round1.md:7).

## Findings on lines changed against the baseline

All are graded with the grading check ("An implementer who follows the stated text as written builds X, and X is wrong because Y") and none holds without a further guess about which of two readings the implementer picks, or each rests on a requirement the spec never states. No finding is blocking.

| id | origin | grade | summary |
|---|---|---|---|
| N1 | changed (quantifier inherited from baseline) | Medium | AC-1.1 scope spans all phases but is a P1 check (see follow-up candidates). |
| N2 | changed | Medium | WC-4's new fixed filename in a shared parent directory can collide with WC-11. |
| N3 | changed | Medium | AC-0.4 still requires contract-based clauses in step 3 and the YAML assertion in step 4 in P0. |
| N4 | changed | Medium | AC-1.2 passes `--output <dir>` to P1 commands that have no such flag, and WC-4 gives no contract directory for two of them. |
| N5 | unchanged | minor | spec:76 says every changed command gains the section; `load` is "changed" (usage line). Quotes no changed line that depends on it. |

No finding of CRITICAL or blocking MAJOR grade was found. Guard Condition Boundary Table (changed lines only; FR-8/FR-9 apply to guards on changed lines):

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--output` names a directory vs a file | spec:62 | Zero/Empty | `--output` absent (a command that takes none: troubleshoot, cleanup-audit, index-repo) | n/a | troubleshoot and workflow: path from `worker_done --report-path` (spec:62, spec:73); cleanup-audit and index-repo: not stated | GAP (N4, Medium: no stated outcome names a wrong build; the coordinator can still use `worker_done --report-path`) |
| same | spec:62 | One/Minimal | `--output out/report.md` (file) | file | parent dir `out/` | OK |
| same | spec:62 | Typical | `--output .dev/x/` (directory) | directory | `.dev/x/return-contract.yaml` | OK |
| same | spec:62 | Legitimate Edge Case | `--output` names a path that does not exist yet | unknown | file-or-directory test is not defined | GAP (N4, Medium: requirement the document never states) |
| same | spec:62 | Sentinel Value Match | two `--output` files in one parent directory | file | same `return-contract.yaml` for both | GAP (N2, Medium: depends on the coordinator choosing a shared parent, which the text allows but does not require) |
| AC-1.1 row filter "row adds a section" | spec:195 | Maximum/Overflow | rows from P2-P4 (tdd, roadmap, pr-submit) | adds a section | included although their phase is later | GAP (N1, Medium) |
| AC-2.2 "row resolves a gate as blocked" | spec:200 | Typical | nine listed commands | blocked | `--outcome failed`, `status: blocked` | OK |
| AC-2.2 same | spec:200 | Zero/Empty | six other commands | no blocked outcome | `--outcome succeeded`, default applied | OK |
| `workflow` pre-creation STOP | spec:62 | Zero/Empty | no `<id>` | true | `.dev/tasks/to-do/return-contract.yaml` | OK (collision note in N2) |

Not applicable classes: Maximum/Overflow for the `--output` directory guard (no capacity rule is stated), and Legitimate Edge Case for the AC-2.2 filter (the nine and six command sets partition the P2 list at spec:160, 15 commands, which I counted: 9 + 6 = 15).

### Adversarial pass (Whittaker, on changed lines; one probe per relevant methodology)

- Divergence (spec:62): `--output` on a file vs a directory is decided per command in section 3, and spec:62 gives examples "(tdd, init-lite, spec-panel)". Boundary case: a nonexistent path. See N4.
- Sentinel collision (spec:62): the fixed name `return-contract.yaml` is the same for every command that writes into one directory. See N2.
- Sequence (spec:194, spec:182-183): in P0 the live check's step 3 and step 4 run before any contract exists. See N3.
- Zero/empty (spec:200): the bare-topic example `/sc:tdd "auth" --unattended --output <file>` blocks before producing the TDD; the contract goes to the file's parent directory, which the text defines, so the contract is writable if the parent exists.
- Accumulation: no counter or capacity on the changed lines.

## Quantity flow

Pipeline Dimensional Analysis does not trigger: the changed lines contain no multi-stage transformation with count divergence (they are path rules and acceptance-check scoping).

## Coverage

Covered: the 7 changed hunks (spec:62, 73, 182, 194, 195, 196, 200); the rows and sections they depend on (section 3.1 rows spec:83-92, 3.2 rows spec:99-122 for the nine and six P2 commands, P1 and P2 scope spec:159-160, WC-5 spec:63, WC-11 spec:69, phase gating spec:154 and 167, Decision spec:265); all five prior blocking findings; inventory lines `INV-B:43,47,49,52` (read, match the spec rows). Not covered: the rest of the document (outside scope for a re-review); `cmd/...` and `sk/...` evidence (UNVERIFIED, no repository in this sandbox); Orca behavior (`CAPS:` citations not re-read).

coverage: scoped PASS: changed lines + prior blockers

## Follow-up candidates

Medium (warnings; none triggers a revision):

- **N1 (Medium, origin=changed; the "every command in sections 3.1-3.2" quantifier is inherited from the baseline spec-v1:195 and was missed in review 1).** AC-1.1 (spec:195) asserts the section for every row that "adds a section" across 3.1-3.2, including P2-P4 rows (tdd, auggie-review, roadmap, pr-submit). Spec:167 says a phase passes only when every check in its block passes, and spec:154 says later phases do not start until the earlier phase's checks pass; the P1 command list (spec:159) does not include those commands. An implementer who reads AC-1.1 as covering all rows at the P1 check gets a P1 check that cannot pass. Not blocking: AC-2.1 (spec:199) says the test "gains one assertion per gate" per phase, which allows the reading that the test grows by phase, so the sentence needs a guess about the worse reading. Suggested narrowing at the next revision: "every P1 command whose row adds a section".
- **N2 (Medium, origin=changed).** WC-4 (spec:62) fixes the name `return-contract.yaml` in the file's parent directory and, for a workflow STOP before an `<id>`, in `.dev/tasks/to-do/`. WC-11 (spec:69) says two workers in one worktree must never write the same file. Two `tdd` workers with sibling output files, or two workflow workers that both stop before creating an `<id>`, write the same contract path and the coordinator can open the other worker's status. This needs the coordinator to pick a shared parent (the text allows it, the brief template does not forbid it), so it is a missing restriction, not a stated contradiction.
- **N3 (Medium, origin=changed).** AC-0.4 (spec:194) says steps 1-3 pass, and step 3 (spec:182) still says the `--outcome` "matches the contract's `status` under WC-5". Step 4 (spec:183) parses the file as YAML and asserts `status` and `command`; AC-0.4 says "step 4 uses the command's existing report file", and for troubleshoot that file is `REPORT.md` (spec:91, `INV-B:49`), which has no `status` key. The M3 fix removed the report-path contradiction but left these two clauses; the plain reading is that the P0 check degrades to the existing report, so a guess about intent is needed. Suggested: say in AC-0.4 which step-3 and step-4 clauses apply in P0 (for example `test -s` only, and the outcome matches the existing report's stated status).
- **N4 (Medium, origin=changed).** AC-1.2 (spec:196) runs each P1 command with `--unattended --output <dir>`. The P1 list (spec:159) includes cleanup-audit, index-repo and workflow, whose rows say "`--pass <N>`" with a fixed output directory (spec:85), "none" (spec:86) and "`--handoff none`" (spec:92); none lists `--output`. WC-4 (spec:62) names no contract directory for cleanup-audit and index-repo (its parenthetical for "the command picks the directory itself" lists troubleshoot, workflow, adversarial). Also, spec:62 does not say how to tell a file from a directory when `--output` names a path that does not exist yet. P1 scope (spec:159) says "output flags for commands that lack one", which probably covers it, but the rows do not say so.

Minor notes:

- **N5 (minor, origin=unchanged).** Spec:76 "Every changed command also gains the `## Unattended mode` section" would include `load` (changed in its usage line, spec:112). AC-1.1 and the Decision at spec:265 govern; spec:76 could say "every changed command whose row adds a section".
- The `ORCA`/`orca-ide` convention, `INV-B` line citations and the 43-command count (spec:76) were not rechecked beyond the lines listed in Coverage.

Per the Review Loop, the session that ran this review asks the user once whether to open an issue for these Medium and minor notes and creates none without an answer; this run records the list only and creates none.

## Brief clauses overridden

The brief (PROMPT-R2) set no clause that widens scope or grades a minor finding as blocking. The brief's "Re-review per the RE-REVIEW prompt" and `--focus requirements,architecture` were followed; no clause was overridden.

## Reviser brief

Blocking finding ids: none. No revision is requested. Rules (restating the Review Loop's Reviser contract, for any later use): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings (N1-N5) are not part of any Reviser brief.

verdict: PASS
