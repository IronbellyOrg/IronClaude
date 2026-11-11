review: 3 of 3

# Spec-panel re-review: orca-worker-contract-spec, round 3 (cap reached, escalate)

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md` (re-review, `cmd:258`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, SHA-256 `f8f6302199d147a422c4ace828ab0a5bd64e8d93cc92412e2478d4460e7d27ae` (285 lines).
- Baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md`, SHA-256 `ba714118121e521fcaa6d0492fe49f39e1fe607a6399a97a6d4b5fc9f802ffdb`. This is the text round2 reviewed as its candidate (`r2` header), so the baseline is the revision before this one.
- Prior report: `.dev/orca-command-refactor/review/round2.md`, SHA-256 `f6326d6baf5eaf4f94e8ad468a485fca4674e079336257a0a630eb94b232a435`. Its header reads `review: 2 of 3`, so this is review 3 of 3 (`cmd:261`).
- Reviewer model actually used: `claude-haiku-5-5`.
- Citation shorthand: `spec:N` = line N of the candidate (line numbers are unchanged from the baseline); `r2:N` = `round2.md` line N; `cmd:N` = `command.md` line N; `prompts:N` = `document_review_loop_prompts.md` line N (sandbox home); `README:N` = `README.md` line N; `inv-A:N` = `inventory/commands-a.md` line N.

## Coverage
- Read in full: `command.md` (491 lines), `document_review_loop_prompts.md` (56 lines), `README.md` (39 lines), `round2.md` (131 lines), the candidate (285 lines), and the baseline `spec-v2.md` (285 lines).
- `diff -w BASELINE CANDIDATE` exit 1, five changed hunks: 62c62, 64c64, 73c73, 158c158, 194c194.
- Inventories: only the lines cited in this report were checked, by search (`inv-A:53`, `inv-A:107`, `inv-A:117`). The rest of both command inventories and `orca-capabilities.md` were not re-read, so every spec citation carried from them stays UNVERIFIED in this review.
- Not present in the sandbox: `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md`. The re-check rules of `cmd:262` therefore stand alone, as `cmd:262` allows. `~/.claude/WORKER-CONTRACT.md` is also absent; it is not needed, because this run passes no `--unattended` (`cmd:457`).
- The command source files under `src/superclaude/commands/` are not in the sandbox. Whether `cleanup-audit` or `index-repo` accepts an output flag is UNVERIFIED. The findings below rely only on what the spec itself lists for those commands.
- Scope: changed lines only (spec:62, 64, 73, 158, 194), plus unchanged text that quotes them (`cmd:262`, `cmd:259`). Round-1 and round-2 Medium and minor items are carried, not re-graded, except where a changed line now depends on them.

## Step 1 evidence block

Command run: `diff -w BASELINE CANDIDATE` (exit 1). Self-check (`prompts:45`): 5 of 5 quoted BEFORE lines were found in BASELINE and 5 of 5 quoted AFTER lines in CANDIDATE (`grep -cF`, each returned exactly one hit), so no role was swapped.

### BEFORE (baseline), lines starting with `<`
```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). A retry gets a new directory from the coordinator, so the coordinator reads the contract of the attempt it last dispatched (F-02). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, runs in the output directory the coordinator passes; the coordinator passes a new directory for each retry, so a re-run starts clean (F-02). In unattended mode the command never chooses its own output directory (F-02). Section 3 names which applies per command. | Coordinator picks the retry directory (F-02); command resumes | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4), and a new one for each retry (WC-6, F-02); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```

### AFTER (candidate), lines starting with `>`
```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). A retry of a row that WC-6 lists as resuming reuses that row's directory with the resume flag; a retry of any other row gets a new directory from the coordinator (N-01). Either way the coordinator reads the contract of the attempt it last dispatched (F-02). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, runs in the output directory the coordinator passes; for a row that resumes (adversarial with `--pipeline-resume`, brainstorm, cleanup-audit, index-repo, tdd, cli-portify, implement, pr-submit, roadmap, release-split, save) the coordinator passes the same directory with the resume flag, and for every other row it passes a new directory for each retry, so a re-run starts clean (F-02, N-01). In unattended mode the command never chooses its own output directory (F-02). Section 3 names which applies per command. | Coordinator picks the retry directory for non-resuming rows (F-02, N-01); command resumes | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` (from P1 on; P0 briefs omit it, N-02) and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4), and for each retry the directory WC-6 gives the row, the same one with the resume flag or a new one (F-02, N-01); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly and without `--unattended` (accepted only from P1, N-02), to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 3, 6 and 7 pass; step 3's report-path check and step 4 use the command's existing report file, since the contract arrives in P1 (N-02); steps 2 and 5 are run and recorded, not gated, because the P0 briefs omit `--unattended` (N-02), so an `agentWait` or an `AskUserQuestion` found there is a P2 gate to convert, not a P0 failure. Record the results in the phase report; a failure of a gated step here reopens section 1 |
```

## Prior findings, re-checked (`cmd:262` steps 1-5, `prompts:45`)

| ID | Prior status (`r2`) | Status now | Basis |
|---|---|---|---|
| N-01 | blocking, open (`r2:59-66`) | resolved | spec:64 now lists the 11 resume rows (adversarial, brainstorm, cleanup-audit, index-repo, tdd, cli-portify, implement, pr-submit, roadmap, release-split, save) and gives them the same directory with the resume flag; every other row gets a new directory. spec:62 and spec:73 agree with it. The list matches the resume column of rows spec:83-92 and spec:105-119. The list still fails for two of its rows (cleanup-audit, index-repo); that defect is N-05. |
| N-02 | blocking, open (`r2:68-73`) | resolved | spec:158 runs the three P0 commands without `--unattended`, and spec:73 says P0 briefs omit it. Steps 2 and 5 of 7.2 are no longer gated in P0 (spec:194). Residual wording problem: N-06. |
| F-01 | resolved (`r2:51`) | still resolved | AC-C1 (spec:172) and SA-2 (spec:147) are unchanged. |
| F-02 | resolved (`r2:52`) | regressed, blocking | The owner conflict over the output directory is back for cleanup-audit and index-repo. spec:64 has the coordinator pass the directory, while spec:85-86 keep a command-chosen location. Same defect as N-05. |
| F-03 | resolved (`r2:53`) | still resolved | spec:79 and AC-1.1 (spec:195) are unchanged. |

## Findings on lines changed against the baseline

### N-05 BLOCKING (origin=changed; spec:62, spec:64; contradicts unchanged spec:85, spec:86, spec:196)
Texts:
- spec:64 (changed): "for a row that resumes (adversarial with `--pipeline-resume`, brainstorm, cleanup-audit, index-repo, tdd, cli-portify, implement, pr-submit, roadmap, release-split, save) the coordinator passes the same directory with the resume flag", and "In unattended mode the command never chooses its own output directory (F-02)".
- spec:62 (changed): `<output-dir>` "is the directory the coordinator passed (`--output` / `--output-dir`)", and spec:73 says the report path is "known before dispatch".
- spec:85 (unchanged): cleanup-audit brief "`--pass <N>` (single pass)", report `.claude-audit/pass<N>-summary.md`, P1 fix "output dir is fixed". No output flag is named or added.
- spec:86 (unchanged): index-repo brief "none", report `PROJECT_INDEX.md (location implied)`, P1 fix "State the output location". No output flag is named or added.
- Inventory: `inv-A:107` says the default cleanup-audit pass "writes a fixed `.claude-audit/pass1-summary.md`". `inv-A:53` and `inv-A:117` say index-repo's location is implied and not stated (UNVERIFIED).
- AC-1.2 (spec:196) runs "each P1 command with `--unattended --output <dir>`". cleanup-audit and index-repo are P1 commands (spec:159).

Sentence: An implementer who follows spec:64 gives a cleanup-audit or index-repo retry a coordinator-passed directory with the resume flag. The rows at spec:85-86 name no output flag and keep a command-chosen location, so the command writes its contract where it always has, and the coordinator, which opened the directory it passed, finds no `return-contract.yaml`. That is wrong because spec:62 requires the contract in the passed directory, known before dispatch, and spec:64 forbids a command-chosen directory in unattended mode; spec:85 and spec:86 each name one. AC-1.2 (spec:196) cannot pass for these two commands as written, because neither is given an `--output` flag.

Grade: blocking. Two stated texts contradict each other, and an acceptance criterion cannot pass as written (`prompts:31`). The spec never says whether these two commands gain an output flag or which directory their contract uses; that choice is for the user or the next revision to make in the text.

Whittaker, zero/empty attack: "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-6 (spec:64)** fails when **a resume-row command is retried with no output flag of its own**. Concrete attack: the coordinator dispatches a cleanup-audit retry and passes `<output-dir>` (spec:73); the command ignores it and writes `.claude-audit/pass1-summary.md`; the coordinator opens `<output-dir>/return-contract.yaml`, finds nothing, and cannot tell whether the retry succeeded."

### N-06 MEDIUM (origin=changed; spec:194, with spec:182-183)
AC-0.4 has two readings, and each needs a guess (`prompts:31`).
- (i) spec:194 says "steps 1, 3, 6 and 7 pass". Step 3 (spec:182) requires `worker_done`. A P0 command that parks on `AskUserQuestion`, which steps 2 and 5 now allow, never sends `worker_done`, so step 3 cannot pass. spec:194 calls such a stall "a P2 gate to convert, not a P0 failure", and in the same line says "a failure of a gated step here reopens section 1". The reader cannot tell whether a stall reopens section 1.
- (ii) Step 4 (spec:183) asserts `d['status']` and `d['command']` in YAML. The existing troubleshoot report is `REPORT.md` (spec:91), not YAML. "Step 4 uses the command's existing report file" either fails the assertion or means only `test -s`.

### N-07 MEDIUM (origin=changed; spec:64, spec:88)
WC-6 classifies rows by their resume flag. The reflect row says "Fresh dir (`--promote-resume` covers promotion only)" (spec:88), so reflect is a non-resume row and each retry gets a new directory. A retry that needs the promotion state from the first attempt does not find it. The spec does not say whether promotion state is covered by the same-directory rule. A requirement the document never states is Medium (`prompts:31`).

### N-08 MEDIUM (origin=changed; spec:64, spec:83, spec:86)
Two gaps in the same-directory rule.
- (a) Conditional resume. adversarial resumes only in pipeline mode (`--pipeline-resume`, spec:83), and index-repo only with `mode=update` (spec:86). spec:64 puts both on the same-directory list with no condition. An unconditional retry of a non-pipeline adversarial run has no resume flag to pass.
- (b) Empty resume. A resume row whose first attempt stopped before writing state (for example before the cleanup-audit checkpoint, spec:85) has nothing to resume from. spec:64 says the command "resumes from its on-disk state" but states no outcome for an empty directory.

### M-03 MEDIUM, carried from round 2, still open (origin=changed; spec:62, spec:64)
spec:64 still says "In unattended mode the command never chooses its own output directory", and spec:62 says the directory is the one passed. An unattended run with no `--output` or `--output-dir` still has no defined outcome (refuse, fail or default). Not stated, so Medium (`prompts:31`).

### N-04 MEDIUM, carried from round 2 (origin=changed now, since spec:62 changed; spec:79, spec:195)
WC-4 (spec:62) still requires `<output-dir>/return-contract.yaml` on every outcome in unattended mode, while spec:79 and AC-1.1 (spec:195) exempt `load`. The intent is clear, but the precedence is not stated. No dispatched Task is affected, because `load` is not run as its own Task (spec:112). Medium.

### N-03 MEDIUM, carried from round 2 (origin=unchanged; spec:147, spec:172)
SA-2 forbids any changed command from naming Orca, and AC-C1 (spec:172) matches only `orca(-ide)?` followed by orchestration, worktree, terminal or agent. No changed line depends on it. Not re-graded.

### Changed lines with no finding
- spec:73 (2.3) now says P0 briefs omit `--unattended`. That agrees with spec:158, spec:79 and the 7.2 brief reference (spec:180).
- spec:158 (P0) says the flag is "accepted only from P1". That agrees with spec:159 and spec:79.

## Guard Condition Boundary Table (changed guards, `cmd:309-317`)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-6 resume-row list | spec:64, spec:85 | Typical: cleanup-audit retry | `<output-dir>` passed; row names no output flag | true | coordinator passes a directory; command writes `.claude-audit/` | GAP (N-05, blocking) |
| WC-6 resume-row list | spec:64, spec:86 | Typical: index-repo retry | `<output-dir>` passed; row brief is `none` | true | same contradiction; location "implied" | GAP (N-05, blocking) |
| WC-6 resume-row list | spec:64, spec:83 | One/Minimal: adversarial retry outside pipeline mode | `--pipeline-resume` not applicable | true | rule says same directory with the resume flag; flag not valid here | GAP (N-08, Medium) |
| WC-6 resume-row list | spec:64, spec:86 | One/Minimal: index-repo retry without `mode=update` | resume condition unmet | true | resume flag not defined for this mode | GAP (N-08, Medium) |
| WC-6 resume-row list | spec:64, spec:85 | Zero/Empty: resume row whose first attempt wrote no state | empty `<output-dir>` | true | "resumes from its on-disk state" with nothing on disk; no outcome stated | GAP (N-08, Medium) |
| WC-6 non-resume row | spec:64, spec:88 | Typical: reflect retry needing promotion state | new `<output-dir>` | true (new directory) | `--promote-resume` state not reached; not stated | GAP (N-07, Medium) |
| WC-6 "never chooses" clause | spec:62, spec:64 | Zero/Empty: unattended run, no directory passed | no directory | true | not stated | GAP (M-03, Medium) |
| WC-4 contract location | spec:62, spec:73 | Typical: resume-row retry, same directory | prior contract present | true | last-dispatched attempt's contract is read | OK |
| P0 brief flag | spec:73, spec:158 | Typical: P0 run without `--unattended` | flag absent | false | P0 omits the flag, as stated | OK |
| AC-0.4 step 3 | spec:194, spec:182 | Legitimate Edge Case: P0 command parks on a question | no `worker_done` | true (stall) | "P2 gate, not a P0 failure" versus "reopens section 1" | GAP (N-06, Medium) |
| AC-0.4 step 4 | spec:194, spec:183 | Typical: troubleshoot existing report | `REPORT.md`, not YAML | false (keys absent) | "uses the existing report file" undefined | GAP (N-06, Medium) |

Input classes left out (`cmd:317`, FR-10): Maximum/Overflow, because the changed lines name no count or capacity. Sentinel Value Match, because the changed lines contain no sentinel. The table is complete under FR-10.

Other mandatory artifacts: Pipeline Dimensional Analysis (`cmd:347-372`) is not triggered, because the changed lines describe no multi-stage data flow with a count change. The State Variable Registry (`cmd:210`) is not required, because `--focus correctness` is not active. Advisory only: the retry checkpoints and on-disk resume state would meet the auto-suggestion threshold at `cmd:192`.

## Whittaker probes (active in every panel review, `cmd:83`)
- Zero/empty on resume rows: N-05 (a resume row with no output flag of its own).
- Sequence on retry: N-08(a) (a conditional resume row retried without its condition) and N-08(b) (retry after a first attempt that wrote nothing).
- Divergence on the reflect row: N-07 (`--promote-resume` state versus a new directory).
- Count check: spec:64 names 11 resume rows, all present in section 3 (3.1: adversarial, brainstorm, cleanup-audit, index-repo, release-split, tdd; 3.2: cli-portify, implement, pr-submit, roadmap, save). The count reconciles.

## Consensus and disagreement
- Consensus: N-01 and N-02 are closed, and the 11-row resume list agrees with the section 3 resume column. The only remaining blocker is the output-directory contradiction for two of those rows.
- Disagreement: none recorded in this review.

## Follow-up candidates (Medium and minor; not in any brief)
- New Medium: N-06, N-07, N-08.
- Carried Medium: M-03, N-03, N-04.
- Carried from round 1 and round 2, unchanged and not re-graded: M-01 to M-08 and m-01 to m-05 (`r2:118-119`).
- Per `cmd:259` and `prompts:31`, the session that ran this review asks the user once whether to open issues for these. No issue has been created.

## Escalation (review: 3 of 3, cap reached)
- Open blocking findings: N-05 (BLOCKING) and F-02 (regressed; same defect as N-05).
- Per `cmd:261` and `cmd:263`, no Reviser brief is written at review 3, and no fourth review runs.
- Decision needed from the user: the cleanup-audit and index-repo rows cannot take the directory that spec:64 gives them. Either (a) give each command an output flag, and state it in spec:85-86 and in the AC-1.2 brief, or (b) take both out of the spec:64 list and name their contract location, which then needs spec:64's "never chooses its own output directory" narrowed to match.

verdict: FAIL
