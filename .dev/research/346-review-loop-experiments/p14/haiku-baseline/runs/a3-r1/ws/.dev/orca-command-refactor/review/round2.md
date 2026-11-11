review: 2 of 3

# Spec-panel critique: orca-worker-contract-spec.md (review 2 of 3, re-review)

- candidate (SPEC): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `24081c933a7fbedd6b461f8f09d06fe7d90105a4b5e12f7221ed9cf63dc4b40e`)
- baseline (V1): `.dev/orca-command-refactor/specs/history/spec-v1.md` (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`)
- prior report (R1): `.dev/orca-command-refactor/review/round1.md` (sha256 `f2a3b79d4d70f11863179b6046729530aab7b65c66f09ec95cb36a2bebe32537`), header `review: 1 of 3`, final line `verdict: FAIL`
- reviewer model: claude-haiku-5-5
- command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`; prompt: RE-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (sandbox home copy at `home/.claude/rules/prompts/document_review_loop_prompts.md`)
- rf-qa.md: neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` exists in the sandbox, so the re-check rules in this report stand alone (review-loop bullet 5).
- R1 records its candidate hash as `d3cdbe...`. That is the hash of V1 (the current baseline), so review 1 covered the text now stored as the baseline.
- Scope: `diff -w V1 SPEC` changes 7 lines: SPEC:62, 65, 73, 122, 194, 195 and one added line at SPEC:204. This report covers those lines and the 4 prior blocking findings. It gives no whole-document assurance.
- Citation keys: paths are relative to the workspace root. INV-A = `.dev/orca-command-refactor/inventory/commands-a.md`, INV-B = `.../commands-b.md`, CAPS = `.../orca-capabilities.md`. Every `INV-*` and `CAPS` line cited below was read in the workspace. The `src/superclaude/...`, `sk/...` and `cmd/...` files named in the spec are not in the workspace, so any citation to them is UNVERIFIED here.

## Step 1: evidence block

Command: `diff -w .dev/orca-command-refactor/specs/history/spec-v1.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md`

BEFORE (baseline), lines starting `<`:

```
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| WC-7 | **Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (`heartbeat`, `ask`, `check`, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. | Worker session | `sk/sc-pr-submit-protocol/SKILL.md:37-39` (top-level rule); `CAPS:159-161`; `INV-A:95` (nesting loses tools at Claude Code's depth limit) |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
| tasklist | under `--unattended`, Stage 10.5 passes `--unattended` to each reflect so the headless rule applies; without `--unattended` Stage 10.5 is unchanged (SA-1); `--no-reflect` is ready today | contract pointing at `tasklist-index.md` and `validation/ValidationReport.md` | fresh dir | none (its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`) | `sk/sc-tasklist-protocol/SKILL.md:92,1452,1614-1631`; `cmd/tasklist.md:39`; `INV-B:46,207-215` | P2 |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |

AFTER (candidate), lines starting `>`:

```
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. Exception [F-3]: `/sc:load` writes no contract, because its only output is session context (section 3.2 `load` row; Decisions table, `/sc:load` handling row). The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| WC-7 | **Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (`heartbeat`, `ask`, `check`, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. A gate that fires inside a subagent cannot send `ask`, so the subagent returns the question to the worker's top-level session, which resolves it as blocked (WC-2 c) and writes the contract [F-4]. | Worker session | `sk/sc-pr-submit-protocol/SKILL.md:37-39` (top-level rule); `CAPS:159-161`; `INV-A:95` (nesting loses tools at Claude Code's depth limit) |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, including `--unattended` from Phase P1 on and every flag section 3 lists as required (P0 briefs omit `--unattended`, because no command accepts it before P1 [F-1]); the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
| tasklist | under `--unattended`, Stage 10.5 passes `--unattended` to each reflect so the headless rule applies; without `--unattended` Stage 10.5 is unchanged (SA-1); `--no-reflect` is ready today | contract pointing at `tasklist-index.md` and `validation/ValidationReport.md` | fresh dir | Two layers below the worker, not one [F-4]: Stage 10.5 subagents run `/sc:reflect`, which spawns `root-cause-analyst` and `confidence-calibrator` (`INV-B:210`); Claude Code allows three layers below the main conversation and withholds the `Agent` tool at the limit (`INV-A:14`); adversarial Mode A depth UNVERIFIED (`INV-B:111`). Gates that fire inside those subagents resolve as blocked (WC-7). The earlier "no change" verdict is withdrawn; check AC-2.6 applies | `sk/sc-tasklist-protocol/SKILL.md:92,1452,1614-1631`; `cmd/tasklist.md:39`; `INV-B:46,207-215` | P2 |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; step 3 passes with this P0 variant [F-2]: `worker_done` arrives exactly once, its `--outcome` is WC-5 applied to the command's existing report (`failed` if that report's status is `failed` or `blocked` or no report exists, otherwise `succeeded`), and its `--report-path` names that existing report file; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` (WC-4 exception [F-3]) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P2 | AC-2.6 | [F-4] Stage 10.5 run of `/sc:tasklist <spec> --unattended --output <dir>` on a phase that reaches reflect Tier 2 | the Tier 2 reviewers and their adversarial merge both run in the worker transcript; every subagent that runs `/sc:reflect` still has its `Agent` tool, so no fan-out is lost; a gate inside a subagent appears as `blocked` in the contract |

Self-check (run before the verdict): every AFTER line above was matched with `grep -nF` (whole-line fixed string) in SPEC, and every BEFORE line in V1. Result: 7 of 7 AFTER lines found once in SPEC, 6 of 6 BEFORE lines found once in V1. The roles are correct, so no swap was made.

## Prior blocking findings (R1)

| id | R1 status | this review | basis |
|---|---|---|---|
| F-1 | open | resolved | SPEC:73 now says P0 briefs omit `--unattended`. That matches SPEC:158 (P0 runs), SPEC:194 (AC-0.4, no flag) and the §3.1 brief column (SPEC:79-92). The two stated texts no longer contradict each other. |
| F-2 | open | resolved | SPEC:194 step 3 now has a P0 variant that takes the outcome and `--report-path` from the command's existing report. The defect R1 named (contract `status` and WC-4 path, which P0 cannot produce) is gone from step 3. The same line still has a new defect in step 4, reported as F-5 below. |
| F-3 | open | resolved | SPEC:62 (WC-4) adds the `/sc:load` exception. SPEC:195 (AC-1.1) excludes `/sc:load`. SPEC:266 (Decisions) and SPEC:112 (§3.2 load row) say the same. A residual conflict with the SPEC:76 intro is reported as M-10. |
| F-4 | open | resolved | SPEC:122 now says two layers below the worker, cites INV-A:14 and INV-B:210 (both checked, consistent), and withdraws the "no change" verdict. The tasklist P2 check is added at SPEC:204 (AC-2.6), and SPEC:65 (WC-7) adds the gate-in-subagent rule. Adversarial Mode A depth stays UNVERIFIED and is named as such. |

Regressed: none. R1 deferred or withdrew no blocking finding, and every resolved finding above matches its own defect.

## New findings (origin = changed)

### F-5 [BLOCKING] AC-0.4 step 4 cannot pass for the P0 `/sc:workflow` run, and has no fixed path for `/sc:adversarial`

- Text: SPEC:194 says "step 4 uses the command's existing report file, since the contract arrives in P1". Step 4 as defined (SPEC:183) asserts `d['status']` in the four-value set and `d['command']` on the parsed file, and this text (carried from V1:194) was not changed by the F-2 edit.
- Evidence: INV-B:272 says the workflow contract carries `status`, `plan_path` and `reflect_report_path` (contract 1.1). It has no `command` key. SPEC:92 (§3.1 workflow row) names that same file as the report today, so P0 step 4 on workflow reads a file without the key it asserts. SPEC:83 (§3.1 adversarial row) says its report filename is "not fixed", so `<contract>` in step 4 has no defined path. SPEC:91 (troubleshoot row) names `REPORT.md`, which is a markdown report; whether it has YAML frontmatter with `status` and `command` is UNVERIFIED (`sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209` is not in the workspace).
- Grading sentence: an implementer who runs AC-0.4 step 4 on `/sc:workflow` in P0 as written parses `return-contract.yaml` and asserts `d['command']`, which INV-B:272 says that file does not carry, so the assertion fails and the P0 gate cannot close. WC-4 (SPEC:62) adds the missing fields only in P1.
- Origin: the line changed (F-2 edit), but the step 4 wording is inherited from V1:194. R1 did not identify it, so it is a severe defect newly discovered in this review.
- Recommendation: give step 4 a P0 variant. It checks `test -s` on the file the command actually wrote, names that file per command (for adversarial, the run's own output file), maps `status` under WC-5 where a status exists, and states that `command` is not checked in P0. Cite the defect by id in the revision.
- Priority: High.

### F-6 [BLOCKING] AC-1.1 cannot pass at its P1 gate as written

- Text: SPEC:195 requires every command in §3.1-3.2 (except `/sc:load`) to have a `## Unattended mode` section. SPEC:159 limits P1 to analyze, build, business-panel, design, document, explain, index, test and load, plus four fixes (adversarial, cleanup-audit, index-repo, workflow). §3.2 rows for later phases (auggie-review at SPEC:100, P2; cleanup, cli-eval, and others, P2-P4 per SPEC:97-126) are not changed until their phase (SPEC:160-162). Two §3.1 rows whose small fix is "None" (brainstorm at SPEC:84, init-lite at SPEC:87) get no section under SPEC:76 and SPEC:79 ("The only command changes are the small fixes in the last column").
- Grading sentence: an implementer who writes AC-1.1 as written and runs it at the P1 gate gets failures for auggie-review (not changed until P2), for brainstorm and init-lite (no section by design), and for every other §3.2 command outside P1. P1 cannot close without either changing those commands early, which SPEC:159 does not allow, or narrowing the test on the implementer's own guess.
- Origin: the line changed (the `/sc:load` exception). The all-commands requirement is inherited from V1:195. R1 did not identify it.
- Recommendation: scope AC-1.1 by phase, so each phase asserts the section only for the commands it changes, and say in §3.1 whether brainstorm and init-lite gain a section. Name the exception by id in the revision.
- Priority: High.

### M-10 [MEDIUM] Whether `/sc:load` gains the Unattended mode section is unclear

- Text: SPEC:76 (unchanged) says "Every changed command also gains the `## Unattended mode` section". SPEC:112 (§3.2 load row) lists only a usage-line change for P1. SPEC:195 (changed) exempts load from the section check.
- Grading sentence: an implementer cannot tell from these lines whether load gets the section. Either reading contradicts one of the three lines, so it needs a guess.
- Origin: SPEC:76 unchanged, SPEC:195 changed. Medium, because it is a missing requirement, not a stated text that does harm.

### m-4 [MINOR] WC-7 states as fact an Orca behaviour the spec lists as UNVERIFIED

- SPEC:65 says "cannot send `ask`" as settled. SPEC:276 (UNVERIFIED item 4) says whether `ask` from a subagent's Bash would be accepted is unknown, and CAPS:160 says the same. The rule still holds because WC-7 forbids the call, so this is a wording issue only.

### m-5 [MINOR] AC-2.6 assumes subagent output reaches the worker transcript

- SPEC:204 requires the Tier 2 reviewers and their merge "to run in the worker transcript". Step 5 of the live check (SPEC:184) uses `worker-read --source transcript`. Whether subagent activity appears in that transcript is not in CAPS and is not listed as UNVERIFIED. Minor, because the check would only need a different source.

## Guard Condition Boundary Table (changed guards only)

Triggered by the changed lines, which add guards at SPEC:62 (load exception), SPEC:65 (gate in subagent), SPEC:194 (P0 step-3 outcome and step-4 assertions) and SPEC:204 (fan-out check). Input classes with no meaningful value are left out with the reason given in the row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 load exception | SPEC:62, SPEC:266 | Zero/Empty: `/sc:load` run, no output | none | no contract | stated | OK (AC-1.1 conflict: F-6, M-10) |
| P0 step-3 outcome | SPEC:194 | Zero/Empty: no report exists | none | failed | WC-5 (SPEC:63) | OK |
| P0 step-3 outcome | SPEC:194 | One/Minimal: `status: partial` | `partial` | succeeded | WC-5 | OK |
| P0 step-3 outcome | SPEC:194 | Sentinel Value Match: status outside the four values | `done` | undefined | not specified (carried M-8) | GAP (M-8, Medium) |
| P0 step-4 assertions | SPEC:194, SPEC:183 | Legitimate Edge: workflow contract without `command` | `status`, `plan_path`, `reflect_report_path` (INV-B:272) | assertion error | not specified | GAP (F-5) |
| WC-7 gate in subagent | SPEC:65 | Legitimate Edge: gate fires inside a subagent | none | blocked | WC-2 (c) | GAP-unverified (m-4; SPEC:276) |
| AC-2.6 fan-out at depth limit | SPEC:204, SPEC:122 | Maximum: reflect fan-out at layer three | layer 3 | Agent tool present or withheld | INV-A:14 | OK as a check; depth UNVERIFIED (SPEC:122) |

Pipeline Dimensional Analysis: not triggered on the changed lines. The added and changed text describes no new multi-stage data transformation whose count can change.

## Follow-up candidates (Medium and minor, not blocking)

- M-10 `/sc:load` section ambiguity (SPEC:76, SPEC:112, SPEC:195)
- m-4 WC-7 "cannot send ask" stated as settled (SPEC:65, SPEC:276)
- m-5 AC-2.6 transcript source (SPEC:204, SPEC:184)
- Carried from R1, origin = unchanged, not re-graded here. By review-loop bullet 5 these are minor notes unless a changed line depends on them. The coordinator should ask the user once whether to open issues for them.
  - M-1 P1 `--unattended` on gated outward commands (SPEC:159, SPEC:67)
  - M-2 retry output directory (SPEC:64, SPEC:73)
  - M-3 WC-4 presents an unverified fact as settled (SPEC:62, SPEC:274)
  - M-4 P3 run classed as nested-only but cited as direct (SPEC:43, SPEC:23, INV-A:13)
  - M-5 cli-eval safety flags undefined (SPEC:104, SPEC:200)
  - M-6 `partial` and dependent Tasks (SPEC:63, SPEC:263, SPEC:73, CAPS:77, CAPS:84-86)
  - M-7 `\|` in AC-C1 and AC-C5 (SPEC:172, SPEC:176)
  - M-8 unmapped status values (SPEC:62, SPEC:262); relevant to F-5
  - M-9 gates with no flag name (SPEC:61, SPEC:60, SPEC:103, SPEC:110, SPEC:122)
  - m-1 300-second wait boundary (SPEC:68)
  - m-2 "ready today" heading (SPEC:78-79)
  - m-3 citations outside the workspace remain UNVERIFIED

## Reviser brief

Blocking finding ids: F-5, F-6.

Restated rule (review-loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised under this brief.

verdict: FAIL
