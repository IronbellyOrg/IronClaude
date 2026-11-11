review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (repo-relative, inside the sandbox workspace)
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review, no `--baseline`, no `--re-review`)
- Prior-findings file: none
- Focus: requirements, architecture
- Prompt: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full at `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p14/haiku-baseline/runs/a3-r3/home/.claude/rules/prompts/document_review_loop_prompts.md`)
- Reviewer model: claude-haiku-5-5

## Coverage

Read in full: the candidate spec (286 lines), `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, and the command definition (`command.md` in the sandbox, which the brief names as the `/sc:spec-panel` definition; the spec cites it as `cmd/spec-panel.md`, which is not in the workspace). Checked: every `INV-A:`, `INV-B:` and `CAPS:` citation I could map (all resolve to the cited content, except where noted). Ran the AC-C1 grep pattern from spec line 172 on a piped test string (no file written).

Not covered: the repo files the spec cites outside the workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...` skills and refs, and the Orca binary). Every claim that rests only on those is UNVERIFIED here. No Orca command was run, and no git command was run.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Output file is `review/round1.md` | `review/spec-panel.md` (README output table, line 26); `review/round1.md` (brief) | The brief names `round1.md` and is the more specific instruction. The README names the shared output list; both are noted here. |
| `command.md` stands in for `cmd/spec-panel.md` | Treat the spec's `cmd/spec-panel.md` citations as UNVERIFIED; use the sandbox `command.md` | The brief names `command.md` as the `/sc:spec-panel` definition. Line numbers below are from `command.md`. |
| Test the AC-C1 pattern with a piped string | Write a scratch file; test with echo piped to grep | A piped string writes nothing, so it stays inside the rule that only assigned files are written. |
| Verdict FAIL | PASS with follow-ups | Four blocking findings (B1-B4) each name a concrete wrong outcome an implementer would produce. |

## Blocking findings

### B1. The contract path rule in WC-4 cannot hold for `/sc:workflow` (and the adversarial path disagrees)

- Spec text: WC-4 requires "in unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed", written "including stops before any other output exists" (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62`). Section 2.3 requires the report path "known before dispatch" (line 73).
- Contradicting text: the workflow row in section 3.1 gives the brief only `--handoff none` (line 92), and its contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, a per-run package path (line 92; `INV-B:272`, `INV-B:267-275`). The adversarial row names `<output>/adversarial/return-contract.yaml` (line 83), a subdirectory that WC-4 does not allow (`INV-A:60`).
- Grading sentence: an implementer who follows WC-4 as written makes `/sc:workflow` write `<output-dir>/return-contract.yaml`, but the brief supplies no output directory and the package `<id>` is created at run time, so the coordinator cannot know the path before dispatch (WC-4, line 73), and a pre-creation STOP has no `<id>` directory to write into, which AC-1.4 (line 198) requires workflow to satisfy.
- Severity: blocking, because the two stated rules cannot both be met.

### B2. Check AC-C1 is vacuous, and SA-2 contradicts it on the contract file and the HOW-WE-WORK section

- Spec text: AC-C1 (line 172) is the common gate for every phase and must "print nothing". Its pattern is `\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b` under `grep -E`. In ERE (GNU grep), `\|` matches a literal pipe, not alternation. The check therefore never matches an Orca command.
- Test run: `printf 'run orca orchestration task-create now\n' | grep -nE '<AC-C1 pattern>'` exits 1 and prints nothing. The same pattern with an unescaped `|` matches the line (exit 0). So AC-C1 cannot fail on any violation of SA-2 or WC-8.
- Contradicting text: SA-2 (line 147) allows an Orca mention "inside the contract file", and P0 (line 158) and SA-5 (line 150) require an Orca section in `src/superclaude/core/HOW-WE-WORK.md`. AC-C1 covers `src/superclaude/core` (line 172) with no exemption for either file. The spec therefore states that the contract file may mention Orca, and its own gate would flag that mention if the gate worked.
- Grading sentence: an implementer who runs AC-C1 as written on a command that calls `orca orchestration task-create` gets no output and marks the check passed, although SA-2 (line 147) and WC-8 (line 66) forbid that call; the phase gate for SA-2 and WC-8 is therefore void.
- Severity: blocking, because a gate that certifies a forbidden state is a wrong outcome of the spec as written.

### B3. AC-0.4 cannot pass in P0 as written

- Spec text: AC-0.4 (line 194) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 (line 182) requires "its report path is the WC-4 contract path". Step 4 (line 183) asserts `d['status']` in a YAML contract and `d['command']`.
- Failure on `/sc:troubleshoot`: the no-`--fix` run writes `REPORT.md` as its `report_path`, and writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:49`, `INV-B:242`). `REPORT.md` is not a YAML contract, so step 4 fails. Step 3 also fails, because the WC-4 contract path does not exist until P1.
- Failure on `/sc:workflow`: its contract has `status`, `plan_path` and `reflect_report_path` (`INV-B:272`) and no `command` key, so the `d['command']` assertion fails in P0.
- Grading sentence: an implementer who runs the P0 smoke test as written gets a failed step 3 and step 4 on two of the three named commands, and the spec says a failure "reopens section 1" (line 194), so P0 cannot pass.
- Severity: blocking, because P0 is the gate for the whole decision.

### B4. The `/sc:spec-panel` row (section 3.2) rests on a premise the command file contradicts

- Spec text: the row says `--output` must be added, that the contract must be added, that "`target_release` required as a flag for TDD inputs" (line 120), and cites `cmd/spec-panel.md:22,34-35,222,451,455`. Section 2.1 (line 52) and WC-4 (line 62) say each changed command adds one `## Unattended mode` section and that the directory flag is `--output` / `--output-dir`. `INV-B:43` states "no path or `--output` flag exists".
- Contradicting text (`command.md`, the `/sc:spec-panel` definition in the sandbox): line 23 already has `[--target-release <release>] [--output <file>] [--unattended] [--report-dir <dir>] [--improve]`. Lines 455-463 already contain a `## Unattended mode` section whose report directory is `--report-dir`, with `--output` as a file-valued flag (line 460). Line 463 already resolves the `target_release` gate as blocked.
- Grading sentence: an implementer who follows the row adds a second `--output` flag and a second `## Unattended mode` section to a command that already has both, so the command ends with two report-path flags (`--output <file>` and `--report-dir <dir>`) and two conflicting unattended definitions, one of which WC-4 does not describe.
- Citation drift (minor, same finding): `Write` is at `command.md:224`, not 222; the Will Not line about modifying specifications is at `command.md:479`, not 451; the target-release question is at `command.md:36-37`, not 35.
- Severity: blocking, because the row's stated premise is false for the file it changes.

## Medium findings (follow-up candidates; not blocking)

- **M1. The gate branch in WC-2 and WC-3 is undefined, and resume has no empty-state rule.** WC-2(c) says a blocked gate writes the report and stops (line 60). WC-3 says the session "may instead ask" and then "re-invoke or resume the command" (line 61). Re-invoking a fresh-directory command (WC-6, line 64; section 3 "Resume" column) starts a new run and loses the attempt. The ask timeout default is UNVERIFIED (line 281; `CAPS:68`). WC-6 also gives no rule for a resume flag passed with no on-disk state. Grading: an implementer must guess which branch applies, so this is Medium.
- **M2. Permission prompts and tool availability in a worker are not addressed.** WC-2 covers AskUserQuestion, chat questions and `[yes / no]` offers (line 60) and says a worker waiting on any prompt looks healthy (`CAPS:52`). It never says what happens when Claude Code asks for tool permission (Bash, Edit, Write) in a worker session, and step 5 of the live check (line 184) tests only AskUserQuestion. Decision 1.2 E2 (line 22) says a worker's command "has the same tools as a command a person runs", but its evidence (`CAPS:161`; `EVIDENCE.md:45`) shows readiness and an answer, not permission mode or tool allowlists. Grading: the missing rule is one a requirement must state, so Medium.
- **M3. Decision evidence E4 is stated more firmly than its source allows.** Line 24 gives as evidence that Agent-tool subagents "are not counted by Orca's nesting limit". `CAPS:155` (which the spec cites) says "UNVERIFIED that Orca never limits them". Section 1.4 point 3 (line 45) does state the gap, but the table row does not. Medium, because the row is the decision's stated basis.
- **M4. WC-11 conflicts with the fixed default outputs of three ready commands.** WC-11 says default output paths "carry a timestamp or the slug the coordinator passes" (line 69). Section 3.1 keeps fixed defaults: cleanup-audit `.claude-audit/` (line 85), index-repo `PROJECT_INDEX.md` (line 86), and init-lite `.dev/superclaude/context-audit.md` (line 87). The one-audit-per-worktree rule for cleanup-audit (line 85) is not in the brief template in section 2.3 (line 73), so the coordinator is not told to enforce it.
- **M5. AC-0.4 claims a check it does not run.** Line 194 says "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)". Step 5 (line 184) searches only for `AskUserQuestion`. Medium, because the no-wrapper rule (WC-7, line 65) has no pass condition.
- **M6. SA-4 and AC-C5 do not list the existing-line edits that WC-10 and the tasklist row need.** SA-4 (line 149) allows existing-line changes only for named defect fixes. The cli-eval wait split (WC-10, lines 68 and 104) and the tasklist Stage 10.5 `--remediate` removal (lines 122 and 295) change existing lines and are not on that list. AC-C5 (line 176) then fails any deletion. An additive form might pass, so the implementer must choose, and this is Medium.
- **M7. Step 3 of the live check has no coordinator reply rule.** Step 3 (line 182) waits for `worker_done`, but `check --wait` also returns `question` and `escalation` (`CAPS:63`). The spec does not say what the coordinator does with them, so the step's pass condition may never be reached. Medium.
- **M8. No rule covers a missing `~/.claude/WORKER-CONTRACT.md`.** Every `## Unattended mode` section points to the installed contract (line 52, section 2.1). A stale install has no such file. The spec does not say whether the command proceeds, blocks or fails. Medium.

## Minor notes

- Citation drift in section 3 for spec-panel is covered by B4. Other section 3 lines cite files outside the workspace and are UNVERIFIED here.
- Line 11 says eleven locations were re-read on 2026-11-02. That claim cannot be checked in the workspace.
- The README (line 26) names `review/spec-panel.md`. This report uses `review/round1.md` per the brief.

## Guard Condition Boundary Table

Triggered: the spec contains outcome, gate and resume conditions (WC-2 to WC-6, WC-12). Focus is requirements and architecture, so the correctness-only State Variable Registry is not required.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:63` | Zero/Empty | no report file exists | true | `--outcome failed` | OK |
| WC-5 outcome | same, line 63 | Typical | `status: succeeded` | false | `--outcome succeeded` | OK |
| WC-5 outcome | same, line 63; Decisions line 263 | One/Minimal (partial) | `status: partial` | false | `--outcome succeeded`, body says partial | OK |
| WC-5 outcome | same, line 63 | Legitimate Edge Case | audit with verdict FAIL, status succeeded | false | `--outcome succeeded` (explicit in text) | OK |
| WC-2 / WC-3 gate | lines 60-61 | Sentinel Value Match (gate unresolved and preamble present) | gate blocked | true | (c) stop vs "may ask" then re-invoke: not decided | GAP (M1) |
| WC-4 output path | line 62 | Zero/Empty (no output-dir flag; workflow) | no output directory passed | true | path unspecified; package path is per run | GAP (B1) |
| WC-6 resume | line 64 | Zero/Empty (resume flag given, no on-disk state) | flag set, directory absent | true | unspecified | GAP (M1) |
| WC-12 check | line 70 | Legitimate Edge Case (`consumer_fenced`) | returned | true | stop, no `worker_done` | OK |

Omitted input classes, with reasons: Maximum/Overflow (no numeric threshold in any guard). One/Minimal is covered by the partial row.

Pipeline Dimensional Analysis: not triggered. No stage changes an item count; the flow passes report paths and outcomes.

## Reviser brief

Blocking finding ids: B1, B2, B3, B4.

Restated rule (review loop, step 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

verdict: FAIL
