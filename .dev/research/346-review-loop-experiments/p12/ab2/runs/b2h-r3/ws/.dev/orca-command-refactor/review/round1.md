review: 1 of 3
> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: F-02, F-03, F-04, F-05. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: F-01 (verifier: The conflict between SPEC:73 and SPEC:79 is real, but the stated stall needs an assumption the candidate does not make: how a command behaves when it receives an undefined `--unattended` flag (the text never says it is ignored and gates stay interactive).). The Reviser brief below is narrowed to the confirmed ids.

# Spec-panel critique: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--re-review`, no `--baseline`)
- Prior report: none
- Review rule: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- Reviewer model: claude-haiku-5-5
- Inputs: all readable (`command.md`, `README.md`, the spec, three inventories). None incomplete.
- Panel: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Newman, Hohpe, Nygard; Whittaker (active in every panel review).
- Mandatory artifacts: Guard Condition Boundary Table triggered (the spec has gates, thresholds and outcome mappings); produced below. Pipeline Dimensional Analysis not triggered (no stage changes a data count; fan-out is task orchestration). State Variable Registry not required (focus is not correctness). TDD and PRD input steps do not apply: TDD score 0 (9 numbered headings, no TDD frontmatter or section names), no PRD headings.

## Citation scope

- `SPEC:n` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line n.
- `INV-A:n` = `.dev/orca-command-refactor/inventory/commands-a.md` line n. `INV-B:n` = `.dev/orca-command-refactor/inventory/commands-b.md` line n. `CAPS:n` = `.dev/orca-command-refactor/inventory/orca-capabilities.md` line n.
- I checked each spec-internal and INV/CAPS line I cite against the file in the workspace.
- Citations to files outside the workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...`, the repo `CLAUDE.md`, Orca app files) cannot be checked in this sandbox and are UNVERIFIED here. Where a finding depends on one, I say so. The spec's own claim (SPEC:11) that a worker re-read 11 of them is also UNVERIFIED here.

## Grading note

A finding is blocking only when a stated text yields a concrete wrong outcome with no further assumption (the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y"). Anything that needs a guess about which of two allowed readings applies is Medium, even when its label is MAJOR.

## Summary

- Blocking: 5 (F-01 to F-05).
- Medium (follow-up candidates): 16 (F-06 to F-21).
- Low: 4 (F-22 to F-25). All Medium and Low items are listed under follow-up candidates.

---

## === REQUIREMENTS ANALYSIS ===

### F-01 | MAJOR | BLOCKING | Expert: Newman (interface evolution, phased rollout)

- Location: `SPEC:73`, `SPEC:79`, `SPEC:158`, `SPEC:159`, `SPEC:194`.
- Issue: `SPEC:73` requires every brief to state "the exact command line including `--unattended`". `SPEC:79` says the ten ready-today commands run as workers "if the brief uses the stated flags", and the table at `SPEC:83-92` lists no `--unattended` flag. `SPEC:159` introduces the flag only in P1. P0 (`SPEC:158`) and its check AC-0.4 (`SPEC:194`) run the ready commands with briefs built per `SPEC:73`.
- Grading sentence: An implementer who follows `SPEC:73` for the P0 smoke runs writes `--unattended` into briefs for commands that do not yet define it, so their gates take the interactive path and the worker stalls, which is the failure WC-2 forbids (`SPEC:60`). Two stated texts conflict.
- Recommendation: Let the P0 brief omit `--unattended`, or move the flag into P0. State in `SPEC:73` that the flag is required only from the phase that adds it.
- Priority: High. Quality impact: P0 evidence could show a false stall and mislead the decision in section 1.

### F-02 | MAJOR | BLOCKING | Expert: Fowler (interface design)

- Location: `SPEC:62` (WC-4), `SPEC:73`, `SPEC:87`, `SPEC:90`, `SPEC:92`; `INV-B:47`, `INV-B:52`, `INV-B:273`; `INV-A:55`.
- Issue: WC-4 requires `<output-dir>/return-contract.yaml`, where `<output-dir>` is what the coordinator passes, and says the path is "known before dispatch" (`SPEC:62`, repeated in `SPEC:73`). Two rows break this:
  - `/sc:workflow` writes `.dev/tasks/to-do/<id>/return-contract.yaml` and "Fresh package each run" (`SPEC:92`). `INV-B:52` and `INV-B:273` describe the `<id>` and "never overwrites or reuses"; nothing in the spec says who sets `<id>` or when it is known.
  - `/sc:tdd` and `/sc:init-lite` take `--output <file>` (`SPEC:90`, `SPEC:87`; `INV-B:47`, `INV-A:55`). A file has no directory to hold `return-contract.yaml`. WC-4 never says how a file-valued output maps to `<output-dir>`.
- Grading sentence: An implementer who follows WC-4 for `tdd --output docs/x.md` writes the contract to `docs/x.md/return-contract.yaml`, and one who follows it for `workflow` cannot name the path before dispatch, so the coordinator opens a missing file and the worker's outcome becomes `failed` under WC-5 (`SPEC:63`). Two stated texts cannot both hold.
- Recommendation: Define the contract location for every command: a directory flag for each contract writer, a rule that a file-valued output uses its parent directory, and an explicit `<id>` (or contract path) passed by the coordinator for `workflow`.
- Priority: High. Quality impact: the coordinator cannot find contracts for two of the ten ready commands.

### F-03 | MAJOR | BLOCKING | Expert: Nygard (retry safety, failure modes)

- Location: `SPEC:64` (WC-6), `SPEC:69` (WC-11), `SPEC:85`, `SPEC:86`, `SPEC:87`; `INV-A:53`, `INV-A:55`, `INV-A:107`.
- Issue: WC-6 says "a retry worker must not corrupt the first attempt's output" (`SPEC:64`). WC-11 says "default output paths carry a timestamp or the slug the coordinator passes" (`SPEC:69`). The section 3.1 rows use fixed defaults:
  - `index-repo` writes a fixed `PROJECT_INDEX.md` (`SPEC:86`; `INV-A:53`).
  - `init-lite` writes a fixed `.dev/superclaude/context-audit.md` and its resume column reads "Re-run overwrites its marked report" (`SPEC:87`).
  - `cleanup-audit` writes a fixed `.claude-audit/` directory (`SPEC:85`; `INV-A:107`).
  The spec's "What changes" column adds only "State the output location" for index-repo (`SPEC:86`), not a per-run path.
- Grading sentence: An implementer who follows the section 3.1 rows builds a retry of `init-lite` that overwrites the first attempt's report, and two `index-repo` workers in one worktree that write the same `PROJECT_INDEX.md`, so the earlier output is lost. The spec's own WC-6 and WC-11 forbid both. Two stated texts conflict, and data is lost.
- Recommendation: In unattended mode, give each of these three commands a per-run path (fresh directory or coordinator-passed slug), or add an explicit coordinator rule that serializes them, written into WC-11 and the brief template.
- Priority: High. Quality impact: silent loss of earlier worker evidence.

### F-04 | MAJOR | BLOCKING | Expert: Wiegers (testability)

- Location: `SPEC:195` (AC-1.1), `SPEC:112` (`load`), `SPEC:87` (`init-lite`), `SPEC:265` (`/sc:load` decision), `SPEC:159`.
- Issue: AC-1.1 requires that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`" and that the test passes at P1. Two commands cannot meet this as the spec defines them:
  - `load` is in section 3.2 but writes no file: "None" report and "use it as a step inside another worker's brief, not as its own Task" (`SPEC:112`). The decision at `SPEC:265` says "a report file would be an unrequested addition".
  - `init-lite` reports to `.dev/superclaude/context-audit.md` or `--output` (`SPEC:87`), not `return-contract.yaml`, and no phase (`SPEC:158-162`) adds a contract to it. P1's command list (`SPEC:159`) does not name it.
- Grading sentence: A test written from AC-1.1 fails for `load` and for `init-lite`, so the P1 exit check cannot pass as written. Blocking because the acceptance criterion cannot be met.
- Recommendation: Exclude `load` from AC-1.1 (it is a context step, so say so in the test), and add a contract to `init-lite` in P1 with its own named path.
- Priority: High.

### F-05 | MAJOR | BLOCKING | Expert: Whittaker (zero/empty attack, FR-2.1); see Adversarial Analysis A-1

- Location: `SPEC:63` (WC-5), `SPEC:183` (7.2 step 4).
- Issue: WC-5 sends `--outcome failed` "when the report says failed or blocked, or no report exists", and `succeeded` "otherwise" (`SPEC:63`). A contract that exists but is zero bytes, truncated, or has no `status` key matches none of the failed cases, so it falls to "otherwise". The validity check is in step 4 (`SPEC:183`), which runs after the coordinator has already settled the Task.
- Grading sentence: An implementer who follows WC-5 literally sends `--outcome succeeded` for an empty or unparseable contract, and the Task settles as succeeded with no deliverable. Blocking because the stated rule produces a concrete wrong outcome.
- Recommendation: Map "exists but does not parse to one of the four `status` values" to `failed`, and require step 4's parse check before `worker_done`.
- Priority: High.

### F-06 | MAJOR label, Medium grade | Expert: Wiegers

- Location: `SPEC:185` (7.2 step 6), `INV-A:43`, `INV-A:51`, `INV-A:52`, `INV-B:45`, `INV-B:48`.
- Issue: Step 6 passes only if `git status --short` shows "only files under the brief's output directory (and the command's documented artifacts)". Several in-scope commands edit product files by design: cleanup (`INV-A:43`), improve (`INV-A:52`), implement (`INV-A:51`), task (`INV-B:45`), test with `--fix` (`INV-B:48`). The spec never says whether product edits count as "documented artifacts".
- Grade: Medium. The implementer must choose a reading, and the stricter reading makes the check fail by design.
- Recommendation: List the product paths each edit-capable command may change, in section 3 or the brief template.

### F-07 | MAJOR label, Medium grade | Expert: Hohpe (message sequencing); see Adversarial A-2

- Location: `SPEC:60` (WC-2 (c)), `SPEC:61` (WC-3), `SPEC:63` (WC-5), `CAPS:58-61`, `CAPS:90`.
- Issue: For a gate with a worker preamble, WC-2(c) says the command writes `blocked` and stops, while WC-3 says the session "may instead ask the coordinator once ... wait, then re-invoke". The text does not say which path applies by default, whether the contract is written before the `ask`, or when `worker_done` is sent. WC-5 maps `blocked` to `failed` (`SPEC:63`), and a `failed` Task keeps dependents blocked (`CAPS:90`), so a worker that writes `blocked` and then gets an answer produces a Task marked failed before the answer is used.
- Grade: Medium. Two readings are allowed and the outcome depends on which one the implementer takes.
- Recommendation: Make the preamble path the only path for worker sessions: no `worker_done` until the `ask` resolves or times out, and the contract is written after that. Keep WC-2(c) for standalone runs and say what the `--retry-of` path after an answer looks like.

### F-08 | MAJOR label, Medium grade | Expert: Newman

- Location: `SPEC:60` (WC-2), `SPEC:121`, `SPEC:90`, `SPEC:114`, `SPEC:122`; `INV-B:47`, `INV-B:49`, `INV-B:34`, `INV-B:119`.
- Issue: WC-2 covers gates of the command itself. Nested skills also contain gates: `/task` inside `/tdd` asks the user (`INV-B:47`), troubleshoot runs per pr-submit finding (`INV-B:34`), and brainstorm inside release-split waits only "if `--interactive`; otherwise auto-proceed" (`INV-B:119`). Only tasklist (`SPEC:122`) states how `--unattended` reaches a nested skill. The spec has no general propagation rule.
- Grade: Medium. An implementer can pass the flag to the top command only and leave nested gates to stall.
- Recommendation: Add one WC rule: a command that calls a nested skill passes `--unattended` (or its equivalent) and the nested gates resolve as blocked.

### F-09 | MAJOR label, Medium grade | Expert: Nygard

- Location: `SPEC:122`, `SPEC:271-285` (UNVERIFIED list), `INV-A:14`, `INV-B:46`, `INV-B:210`, `INV-B:314`.
- Issue: The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit", citing `INV-A:14`. `INV-A:14` states the three-layer rule only. It does not count tasklist's layers (tasklist, Stage 10.5 subagent, reflect, reviewers, adversarial). `INV-B:210` and `INV-B:314` (UNVERIFIED #1) mark nested spawning as unknown, and the spec's own UNVERIFIED list does not carry the question.
- Grade: Medium. The row turns an open question into a verdict.
- Recommendation: Add the question to the UNVERIFIED list and make the tasklist P2 change depend on a live run.

### F-10 | MAJOR label, Medium grade | Expert: Cockburn (standalone stakeholder)

- Location: `SPEC:146` (SA-1), `SPEC:118` (roadmap), `SPEC:119` (save), `SPEC:149` (SA-4).
- Issue: SA-1 says that without `--unattended` "every prompt, approval gate, default flag value, output path ... stays as it is today". The roadmap row replaces the `Resume? [Y/n]` prompt with a flag "(resume only when passed)" and does not scope this to unattended mode (`SPEC:118`). The save row restricts writes to per-session keys (`SPEC:119`) without the same scoping. SA-4's exemption list (`SPEC:149`) names roadmap drift but not save's shared-state change.
- Grade: Medium. SA-4 can be read to cover both changes, so the reading is a guess.
- Recommendation: Scope both changes to `--unattended`, or add save to SA-4's list and state that the roadmap prompt change is a defect fix.

### F-11 | MEDIUM | Expert: Wiegers

- Location: `SPEC:60` (WC-2 lists three resolutions), `SPEC:103`, `SPEC:108`, `SPEC:110`, `SPEC:114`, `SPEC:118`, `SPEC:123`.
- Issue: WC-2 defines three resolutions: (a) default, (b) flag, (c) blocked. Section 3 also uses "refused" (for `--interactive`, `--watch`, `--monitor 1`, `--format interactive`, `--mode socratic`). The spec does not say what status or `--outcome` a refused run produces.
- Grade: Medium (the implementer must pick a status).
- Recommendation: Define refused as `status: blocked` with the refused flag as `blocked_question`.

### F-12 | MEDIUM | Expert: Hohpe

- Location: `SPEC:63` (WC-5), `SPEC:73` (2.3), `SPEC:263` (Decisions, partial to succeeded).
- Issue: `partial` and an audit verdict of FAIL both become `--outcome succeeded` (`SPEC:63`, `SPEC:263`). The coordinator's only machine signal is `--outcome`, and `SPEC:73` tells it to open the report but gives no rule for acting on `partial` or FAIL.
- Grade: Medium. The outcome is correct by definition, but a coordinator that reads only the outcome will proceed past a failed audit.
- Recommendation: Add a coordinator rule table keyed on `status` and the verdict line.

### F-13 | MEDIUM | Expert: Hohpe

- Location: `SPEC:72-73` (2.3), `SPEC:182` (7.2 step 3), `CAPS:62-63`.
- Issue: 2.3 lists what the coordinator sends and what it does after `worker_done`. It does not say that the coordinator answers `question` or `escalation`. Step 3 waits on `check --wait --types "worker_done,escalation,question"` until `worker_done` (`SPEC:182`), but a `question` returns the wait first. The reply command is `CAPS:62` (`orca orchestration reply --id`).
- Grade: Medium. Read literally, step 3 stops at the first question.
- Recommendation: Add to 2.3: the coordinator answers each `question` with `reply --id` and keeps waiting, and handles `escalation` explicitly.

### F-14 | MEDIUM | Expert: Fowler

- Location: `SPEC:69` (WC-11), `SPEC:73`, `CAPS:115`, `INV-A:43`, `INV-A:52`, `INV-A:51`.
- Issue: WC-11 covers only two workers writing the same file. Edit-capable commands (cleanup, improve, implement, task, test `--fix`) can conflict on any file they touch. The spec leaves placement to the brief (`SPEC:73`), and the Orca default is that workers share the current worktree (`CAPS:115`).
- Grade: Medium. The rule for when to use a separate worktree is absent, so the implementer must choose.
- Recommendation: State that edit-capable workers get their own worktree unless the brief proves their scopes disjoint.

### F-15 | MEDIUM | Expert: Newman

- Location: `SPEC:159` (P1), `SPEC:154`, `SPEC:162` (P4), `SPEC:109`, `SPEC:113`, `SPEC:114`, `INV-A:51`, `INV-B:33`, `INV-B:34`.
- Issue: P1 makes `--unattended` accepted by every command in 3.1 and 3.2 "(a no-op where a command has no gate)". Three commands that keep default gates or outward defaults until P4 are `implement`, `post-release` and `pr-submit` (P4 at `SPEC:162`). Nothing says they must not be dispatched as workers before P4, and under P1 their brief looks valid.
- Grade: Medium. A stall or an outward action is possible if the coordinator dispatches them early.
- Recommendation: Add to 6 that these three are not dispatched as workers until P4 passes.

### F-16 | MEDIUM | Expert: Nygard (readiness and startup)

- Location: `SPEC:59` (WC-1), `SPEC:158-162` (phases), `CAPS:49`, `CAPS:51`, `CAPS:44-45`.
- Issue: WC-1 is owned by "Launch setup, not commands" (`SPEC:59`), but no phase or AC covers it (`SPEC:158-210`). It says the fallback must sit "well inside the readiness limit" without a number. The evidence gives a pass at 30 s and a fail above about 45 s (`CAPS:49`). The setup wait (`CAPS:51`, `setup_wait`) is not mentioned in the spec.
- Grade: Medium. The owner and the ceiling are missing.
- Recommendation: Assign WC-1 to a phase with an AC and a numeric fallback ceiling (for example 30 s); add the setup wait to WC-1.

### F-17 | MEDIUM | Expert: Fowler (contract interface)

- Location: `SPEC:62` (WC-4 "carries at least"), `SPEC:261` (Decisions, "the coordinator can check every worker the same way"), `SPEC:183`, `INV-B:272`, `INV-B:112`, `INV-A:39`.
- Issue: WC-4 lists four fields as a minimum and says commands "keep their fields and add the missing ones". The existing contracts differ (workflow has `plan_path` and `reflect_report_path`, `INV-B:272`), so the coordinator cannot check every worker the same way (`SPEC:261`). `blocked_question` is required "when blocked" (`SPEC:62`) but no rule rejects an empty value; AC-2.2 checks it only in a test (`SPEC:200`). Step 4 (`SPEC:183`) checks two fields.
- Grade: Medium (the schema is unversioned, so implementers will diverge).
- Recommendation: Publish a schema with a version field, required fields and a rule that empty `blocked_question` under `blocked` is a `failed` report.

### F-18 | MEDIUM | Expert: Whittaker (sentinel collision, FR-2.3); see Adversarial A-3

- Location: `SPEC:228` (D1), `SPEC:195` (AC-1.1 uses grep), `SPEC:51`.
- Issue: D1 says the switch "is testable by grep and cannot misfire on a person". A quoted topic that contains `--unattended` matches a grep, for example `/sc:troubleshoot "flag --unattended ignored"`. `SPEC:51` defines the switch as a flag but does not say it must be a standalone token outside quotes.
- Grade: Medium. The detection rule is not stated well enough to avoid a false positive.
- Recommendation: Define the switch as a standalone argument token outside quotes, and test it with a quoted-text case.

### F-19 | MEDIUM | Expert: Wiegers (evidence)

- Location: `SPEC:22` (E2), `SPEC:23` (E3), `SPEC:43` (1.4(1)), `CAPS:156`, `CAPS:49`.
- Issue: E2 says a command run by a worker "has the same tools as a command a person runs". The cited evidence (`EVIDENCE.md:45`, quoted at `CAPS:49`) shows readiness and an answer, not tool parity (UNVERIFIED here). E3 says the decision "has worked before", but the cited PR #329 run used Agent-tool subagents (`CAPS:156`), which WC-7 forbids (`SPEC:65`). The caveat appears only in `SPEC:43`.
- Grade: Medium. The decision in section 1 leans on these two rows.
- Recommendation: Restate E2 as readiness only, and mark E3 as evidence for nested routing, not the direct route.

### F-20 | MEDIUM | Expert: Nygard

- Location: `SPEC:68` (WC-10), `SPEC:114` (pr-submit row), `SPEC:283` (UNVERIFIED #12), `CAPS:130`.
- Issue: WC-10 requires each wait under 4 minutes. The pr-submit row says each poll-plus-sleep iteration must stay under 4 minutes but that the poll script's runtime is unknown (UNVERIFIED #12). The spec's acceptance (AC-4.3) depends on the answer.
- Grade: Medium. An implementer cannot confirm compliance for pr-submit.
- Recommendation: Measure the poll runtime in P0 or mark pr-submit as not dispatchable until measured.

### F-21 | MEDIUM | Expert: Fowler (mirror integrity)

- Location: `SPEC:279` (UNVERIFIED #8), `SPEC:158-162`, `SPEC:191-210`.
- Issue: UNVERIFIED #8 says each phase's plan must resolve how `plugins/superclaude/commands/` is kept in step with `src/` before editing. No phase or AC checks this.
- Grade: Medium.
- Recommendation: Add the resolution as a P1 entry gate and an AC.

### F-22 | LOW | Expert: Wiegers (dual-surface rule)

- Location: `SPEC:52`, `SPEC:62`. Project rule in the repo `CLAUDE.md` (dual-surface lookup of an installed primitive; the spec's line numbers for it are UNVERIFIED here).
- Issue: Commands point only to `~/.claude/WORKER-CONTRACT.md`. The project's dual-surface rule for a core-doc lookup asks for the project `.claude/` copy as well.
- Grade: Low.

### F-23 | LOW | Expert: Adzic (testable examples)

- Location: `SPEC:172` (AC-C1).
- Issue: The grep is written with `\|` inside a Markdown table. Rendered, it reads as `|`, but copied from the raw file it searches for literal `|` in an ERE, matches nothing, and passes vacuously. Put the command in a fenced block.
- Grade: Low.

### F-24 | LOW | Expert: Cockburn (classification)

- Location: `SPEC:79`, `SPEC:88`, `SPEC:90`, `SPEC:91`, `SPEC:89`.
- Issue: The 3.1 header says "the only command changes are the small fixes in the last column". The reflect, tdd, troubleshoot and release-split rows need the P2 gate changes, which are not small. "Ready" holds only when the brief omits the flag.
- Grade: Low.

### F-25 | LOW | Expert: Adzic

- Location: `SPEC:194` (AC-0.4 "record the results in the phase report").
- Issue: No location is given for the phase report.
- Grade: Low.

---

## === ARCHITECTURE ANALYSIS ===

Architecture findings are F-01, F-02, F-03, F-09, F-13, F-14, F-15, F-17, F-21 and F-22 above.

Additional architecture notes (no separate finding):

- Section 1 (decision): the rejection of "commands call Orca" rests on `CAPS:97-101,103`, which I checked. Its UNVERIFIED call-site question (`CAPS:103`) is correctly marked. The decision holds on the evidence it cites.
- Section 4 (coordinator-only): the six verdicts match `INV-A:90`, `INV-A:49-50`, `INV-B:285-287`, which I checked.
- Section 5 (SA rules) is consistent with section 6 except for F-10 and F-15.

---

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- A-1 (FR-2.1 Zero/Empty; `SPEC:63`): "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when **the contract exists but is zero bytes**. Concrete attack: the command runs `touch return-contract.yaml`, then crashes. 'No report exists' is false, so the worker sends `--outcome succeeded`; the Task settles succeeded; step 4 (`SPEC:183`) fails only afterwards." Merged into F-05. Severity: MAJOR.
- A-2 (FR-2.2 Divergence; `SPEC:60-61`): "I can break this specification by **Divergence Attack**. The invariant at **WC-2 (c) and WC-3 (SPEC:60-61)** fails when **the gate fires and the session holds a preamble**. Concrete attack: the command writes `status: blocked` and stops; the session calls `ask`; the ask times out; WC-5 sends `--outcome failed` (`SPEC:63`); the coordinator re-dispatches with `--retry-of`, and the first attempt's question is still pending." Merged into F-07. Severity: MAJOR.
- A-3 (FR-2.3 Sentinel Collision; `SPEC:228`): "I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (SPEC:228)** fails when **a quoted argument contains the switch text**. Concrete attack: `/sc:troubleshoot "flag --unattended ignored" --output d/`; grep for `--unattended` matches the topic, so the detection is wrong for a person's own run." Merged into F-18. Severity: MINOR (under D1's own test it is a false positive; the consequence is a silent switch to unattended).
- A-4 (FR-2.4 Sequence and FR-2.5 Accumulation; `SPEC:64`): "I can break this specification by **Sequence Attack**. The invariant at **WC-6 (SPEC:64)** fails when **a worker's `worker_done` is lost and the coordinator re-dispatches**. Concrete attack: attempt 1 writes `init-lite`'s marked report and reports success, but the message is lost; the retry overwrites the same file (`SPEC:87`); the coordinator's record of attempt 1 now points at attempt 2's content." Merged into F-03. Severity: MAJOR.

---

## GUARD CONDITION BOUNDARY TABLE

Columns: Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status. Rows for the six classes are given only where they can occur for the guard; omissions are explained below the table. Status GAP entries name their finding.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 WC-5 outcome mapping | SPEC:63 | Zero/Empty | contract 0 bytes or no `status` | exists=true, parses=false | "otherwise" gives `succeeded` | GAP, F-05 (blocking) |
| G1 WC-5 outcome mapping | SPEC:63 | One/Minimal | `status: partial` | true | `succeeded` (SPEC:263) | OK |
| G1 WC-5 outcome mapping | SPEC:63 | Typical | `status: succeeded`, audit verdict FAIL | true | `succeeded` | OK (coordinator reading: F-12) |
| G1 WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | `status: blocked`, `blocked_question` empty | true | `failed`; question rule absent | GAP, F-17 (Medium) |
| G1 WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | `status: partial`, deliverable file missing | true | `succeeded` | GAP, F-12 (Medium) |
| G2 WC-4 contract path | SPEC:62, SPEC:73 | Zero/Empty | `--output` not passed | n/a | brief "must state" the directory; no default | GAP, F-02 (Medium) |
| G2 WC-4 contract path | SPEC:62 | One/Minimal | `--output <file>` (tdd, init-lite) | file, not dir | `<output-dir>/return-contract.yaml` | GAP, F-02 (blocking) |
| G2 WC-4 contract path | SPEC:62 | Typical | `--output <dir>` (adversarial, brainstorm) | dir | path as stated | OK |
| G2 WC-4 contract path | SPEC:85-87 | Sentinel Value Match | fixed default (`PROJECT_INDEX.md`, `context-audit.md`, `.claude-audit/`) | shared across runs | overwrite | GAP, F-03 (blocking) |
| G2 WC-4 contract path | SPEC:92 | Legitimate Edge Case | `<id>` created at run time | not known before dispatch | must be known (SPEC:73) | GAP, F-02 (blocking) |
| G3 WC-2 gate resolution | SPEC:60, 99-125 | Zero/Empty | required input absent (cli-eval `--suite`) | blocked | blocked with question (SPEC:104) | OK |
| G3 WC-2 gate resolution | SPEC:103, 110 | One/Minimal | single gate with documented default | n/a | default (a) | OK |
| G3 WC-2 gate resolution | SPEC:108, 114, 118, 123 | Sentinel Value Match | `--interactive`, `--watch`, `--monitor 1` with `--unattended` | refused | status/outcome unstated | GAP, F-11 (Medium) |
| G3 WC-2 gate resolution | SPEC:90, 122 | Legitimate Edge Case | nested gate inside a called skill | n/a | rule absent except tasklist | GAP, F-08 (Medium) |
| G4 WC-10 wait split | SPEC:68 | Typical | 3-minute single call | at most 240 s | allowed | OK |
| G4 WC-10 wait split | SPEC:68, 104 | Maximum/Overflow | eval wait up to 3600 s | above 240 s | split required | OK |
| G4 WC-10 wait split | SPEC:68, 114 | Sentinel Value Match | pr-submit 600 s default, iteration length unknown | unknown | under 240 s required | GAP, F-20 (Medium) |
| G4 WC-10 wait split | SPEC:68 | Legitimate Edge Case | exactly 240 s | at limit | "at most 4 minutes" | OK |
| G5 WC-1 readiness | SPEC:59 | Typical | fallback 30 s | under 60 s | pass (CAPS:49) | OK |
| G5 WC-1 readiness | SPEC:59 | Maximum/Overflow | fallback 45-60 s | near limit | "well inside" undefined | GAP, F-16 (Medium) |
| G5 WC-1 readiness | SPEC:59 | Legitimate Edge Case | setup wait longer than readiness | fails `setup_wait` (CAPS:51) | not specified | GAP, F-16 (Medium) |
| G6 WC-3 ask timeout | SPEC:61, 281 | Zero/Empty | `--timeout-ms` omitted | default unknown (UNVERIFIED #10) | resume by message ID; no value relied on | OK |
| G6 WC-3 ask timeout | SPEC:61 | Typical | answer within 600000 ms | n/a | reply and continue | OK |
| G6 WC-3 ask timeout | SPEC:61 | Sentinel Value Match | timeout, then a new question | duplicate | "never creates a duplicate" | OK |
| G6 WC-3 ask timeout | SPEC:70 | Legitimate Edge Case | disconnect; `check` returns `consumer_fenced` | fenced | stop, no `worker_done` (CAPS:67) | OK |
| G7 `--unattended` switch | SPEC:51, 228 | Zero/Empty | no flag | attended | default behavior | OK |
| G7 `--unattended` switch | SPEC:228 | Sentinel Value Match | switch text inside a quoted topic | grep matches | standalone-token rule absent | GAP, F-18 (Medium) |
| G7 `--unattended` switch | SPEC:159 | Legitimate Edge Case | flag given to a command with no gate | no-op | P1 (SPEC:159) | OK |

Omitted classes: G2 Maximum/Overflow (no numeric path limit exists in the spec, so no guard); G4 Zero/Empty (no wait, so no guard); G5 Sentinel (Orca's own fallback when `--timeout-ms` is not positive, CAPS:45, is not a spec guard); G6 One/Minimal (the timeout is one value; covered by Typical); G7 Typical (the flag is either present or absent; covered by Zero/Empty and Sentinel).

FR-10 check: every guard is enumerated and every omitted class has a reason. FR-8 GAP entries: blocking F-02, F-03, F-05; the rest are Medium.

## Follow-up candidates (Medium and minor; not blocking; not revised)

- F-06 (MAJOR label, Medium): product-edit paths for edit-capable commands.
- F-07 (MAJOR label, Medium): WC-2(c) vs WC-3 ordering.
- F-08 (MAJOR label, Medium): propagation of `--unattended` to nested skills.
- F-09 (MAJOR label, Medium): tasklist nesting depth unverified.
- F-10 (MAJOR label, Medium): SA-1 vs roadmap and save rows.
- F-11 (Medium): undefined `refused` outcome.
- F-12 (Medium): `partial` and FAIL both `succeeded`.
- F-13 (Medium): coordinator answers `question` and `escalation`.
- F-14 (Medium): worktree placement for edit-capable workers.
- F-15 (Medium): P4 commands dispatched before P4.
- F-16 (Medium): WC-1 owner, ceiling and setup wait.
- F-17 (Medium): contract schema and empty `blocked_question`.
- F-18 (Medium): switch detection inside quoted text.
- F-19 (Medium): E2 and E3 evidence wording.
- F-20 (Medium): pr-submit poll runtime.
- F-21 (Medium): plugin mirror gate.
- F-22 (Low): dual-surface lookup of WORKER-CONTRACT (UNVERIFIED line for the project rule).
- F-23 (Low): AC-C1 escaped pipes.
- F-24 (Low): "ready today" label.
- F-25 (Low): AC-0.4 phase report location.

No user is present in this worker run, so the review did not ask whether to open issues for these; the list is recorded only, and no issue was created.

## Quality assessment (0-10)

- Clarity: 6. Most rows are precise; the contract and gate vocabulary (blocked, refused, ask, contract) drifts.
- Completeness: 7. All 43 commands are placed; contract schema and coordinator obligations are missing.
- Testability: 5. Several ACs cannot pass as written (F-04, F-06) or are vacuous (F-23).
- Consistency: 4. The `--unattended` timing (F-01), path rules (F-02, F-03) and SA rules (F-10) conflict.

## Decisions

- Panel scope: Whittaker was included because the panel's review text makes him active in every review.
- Grade of F-06 to F-10: Medium, because each needs a choice between two readings the text allows.
- Guard table: produced in full because the spec contains conditional logic; GAP rows are mapped to findings.
- Unverifiable citations: marked UNVERIFIED in the citation scope section and in the findings that depend on them.

## Coverage

Covered: the full spec (all sections, all acceptance checks, decisions D1 to D5, UNVERIFIED items 1 to 14); the three inventories as the only checkable evidence; the command file's FIRST-REVIEW rules; the review-loop prompts file. Not covered: any repo file, Orca runtime, or EVIDENCE file outside the workspace (UNVERIFIED here).

## Reviser brief

Blocking finding ids: F-01, F-02, F-03, F-04, F-05.

Restated bullet 6 of the Review Loop: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
