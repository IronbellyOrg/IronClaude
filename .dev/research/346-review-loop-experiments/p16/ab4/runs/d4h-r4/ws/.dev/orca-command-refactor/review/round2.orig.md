review: 2 of 3

# Re-review: orca-worker-contract-spec (focus: requirements, architecture)

Short names used for path:line citations below: SPEC = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (candidate), BASE = `.dev/orca-command-refactor/specs/history/spec-v1.md` (baseline), PRIOR = `.dev/orca-command-refactor/review/round1.md`, LINT = `.dev/orca-command-refactor/review/lint-2.md`, INV-A = `.dev/orca-command-refactor/inventory/commands-a.md`.

candidate: SPEC sha256 7c8aa27b2871ce92c01502f179de64ec96be2031fdf14b1198dc4230f55a9adc
baseline: BASE sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
prior: PRIOR sha256 2a940d6b61c8e33495bdfa4a181d2ff04a5d86687053fb677c4fe7965477560e (header `review: 1 of 3`, so this review is N = 2)
lint: LINT sha256 7bd33ecb8823b9f35684c3ab424e7f427969d49fd661a2fd0aee7c22e3097587 (`Checks: REF. Findings: 0.`, no lint ids to address)
reviewer model: claude-haiku-5-5 (single reviewer, fresh context for this run)
rules read: `home/.claude/rules/prompts/document_review_loop_prompts.md` read in full; RE-REVIEW prompt followed. `rf-qa.md` (project `.claude/agents/` or `~/.claude/agents/`) is not present in the sandbox, so the Review Loop section 5 rules in `command.md` stand alone.
coordinator note: the VERIFY prompt must run on the blocking ids M4 and N1 before any REVISE.

## Step 1: evidence block

`diff -w BASE SPEC` was run. Roles were fixed by the command (BASE = BEFORE, SPEC = AFTER).

BEFORE (baseline), lines starting `<`:

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
< | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | None | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
< | SA-5 | `src/superclaude/` stays the source of truth; `.claude/` copies come from `make sync-dev` and are never staged. The routing guide gains an Orca section without changing any existing routing row, and its two mirrored copies are updated as the repo requires. | Repo rules. | `CLAUDE.md:16,157,334` |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status`; its report path is the WC-4 contract path.
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
< | `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed. |
```

AFTER (candidate), lines starting `>`:

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Exception (M1): `/sc:load` writes no file and is exempt from WC-4, AC-1.1 and AC-1.2 (section 3.2 load row; Decisions table). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. Phase 1 adds the `--unattended` flag, its `## Unattended mode` section and the WC-4 contract to all ten commands in this table (M5). Beyond that, the only command changes are the small fixes in the last column.
> | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | P1 (M5): accept `--unattended` as a no-op (no gate), and add the Unattended section naming the existing contract | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | P1 (M5): accept `--unattended` as a no-op (no gate), add the Unattended section, and write the WC-4 contract to `<output-dir>` beside the report | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | load | no gate | none, by exception (M1; see WC-4 exception and Decisions) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. AC-C1 (section 7.1) scans `commands`, `skills` and `agents` in full and `core` except `WORKER-CONTRACT.md` and the routing guide's Orca section (M7). | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
> | SA-5 | `src/superclaude/` stays the source of truth; `.claude/` copies come from `make sync-dev` and are never staged. The routing guide gains an Orca section without changing any existing routing row, and its two mirrored copies are updated as the repo requires. Its Orca section is the one exemption from AC-C1 in `core` (M7). | Repo rules. | `CLAUDE.md:16,157,334` |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only; exempt from WC-4 per M1); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | AC-C1 | the three scans and the self-test in the block below the table (M7) | the scans print nothing outside the stated exclusions, and the self-test prints `SELFTEST-OK` (SA-2, WC-8) |
> ```bash
> # Scan 1: commands, skills, agents (hard rule). -i covers the ORCA placeholder; under -E, | is alternation.
> grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' \
>   src/superclaude/commands src/superclaude/skills src/superclaude/agents \
>   | grep -v '^src/superclaude/skills/ccsession-tag/'
> # Scan 2: core. WORKER-CONTRACT.md is excluded by name; every match in HOW-WE-WORK.md must lie inside its Orca section, whose line range the phase report records.
> grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/core \
>   | grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:'
> # Self-test: the pattern must match a planted line, or scans 1 and 2 prove nothing.
> printf 'orca orchestration worker-start\n' | grep -qiE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' && echo SELFTEST-OK
> ```
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the `status` under WC-5 of the contract (P1 and later) or of the command's existing report (P0, before any contract exists); its report path is the WC-4 contract path in P1 and later, and the command's existing report path in P0 (M2).
> 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0. In P0 only `test -s` on the command's existing report applies, because the contract fields do not exist before P1 (M4).
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2, 5, 6 and 7 pass, and steps 3 and 4 pass in their P0 form (M2, M4): step 3 checks the outcome against the existing report's status and the report path against the command's existing report, and step 4 is `test -s` on that report. The WC-4 path and YAML field checks are P1 checks (AC-1.2). Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, that `load` has none (M1), and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (M1) with `--unattended --output <dir>` | all steps pass |
> | P2 | AC-2.2 | Gate-trigger run per P2 command in the table below: a 7.2 live check with the row's gate-trigger input | each row's expected `worker_done --outcome` and contract status hold (M6); step 2 never shows `agentWait` |
> #### AC-2.2 gate-trigger table (M6)
> Every P2 command has one row. A row whose resolution is (c) blocked expects `failed` and `status: blocked` with a non-empty `blocked_question`. A row whose resolution is (a) or (b) expects `succeeded` and the check named in the last column. `roadmap` is cited in M6 but its phase is P3 (section 3.2), so it is checked by AC-3.2, not here.
> | Command | Gate-trigger input in the brief | Expected resolution (WC-2) | Expected `--outcome` | Expected contract and check |
> |---|---|---|---|---|
> | tdd | bare topic `"auth"` with `--unattended --output <file>` | (c) blocked: topic-only clarification | failed | `status: blocked`, non-empty `blocked_question` |
> | cli-eval | `run --unattended` with no `--suite` | (c) blocked | failed | `status: blocked`, non-empty `blocked_question` |
> | cli-portify | `--unattended` run that reaches an approval gate | (c) blocked, artifact to review named | failed | `status: blocked`; the artifact is named in `blocked_question` |
> | troubleshoot | `--depth deep` with a short symptom | (c) blocked: short-input STOP | failed | `status: blocked`, non-empty `blocked_question` |
> | recommend | goal too vague to route, with `--unattended` | (c) blocked: clarifying question | failed | `status: blocked`, non-empty `blocked_question` |
> | release-split | `--r1-scope custom` under `--unattended` | (c) blocked | failed | `status: blocked`, non-empty `blocked_question` |
> | review-translation | no pre-confirmed context input in the brief | (c) blocked, after writing the context summary | failed | `status: blocked`; the summary path is in `artifacts` |
> | spec-panel | TDD input without the `target_release` flag | (c) blocked | failed | `status: blocked`, non-empty `blocked_question` |
> | task | a task that reaches its TFEP "present to user" step | (c) blocked | failed | `status: blocked`, non-empty `blocked_question` |
> | tasklist | `--unattended` run (Stage 10.5 reflect) | none in the row: no gate fires | succeeded | `status: succeeded` or `partial`; AC-2.3 covers the happy path |
> | reflect | `--remediate --unattended` | (a) headless auto-accept rule | succeeded | `status: succeeded`; remediation files listed in `artifacts` |
> | auggie-review | `/sc:auggie-review <PR> --unattended` with no `--post-pr` | (a) no posting, no remediation offer | succeeded | `status: succeeded`; the report states that posting was skipped (WC-9); AC-2.4 checks the comment counts |
> | cleanup | a directory with an item under "Approval Required" | (a) apply non-approval items only; list the rest | succeeded | `status: succeeded`; every listed item is unapplied in `git status` |
> | improve | an item under "Approval Required" | (a) apply non-approval items only; list the rest | succeeded | `status: succeeded`; every listed item is unapplied in `git status` |
> | research | a topic with `--unattended` | (a) strategy pinned to `planning` | succeeded | `status: succeeded`; `artifacts` names `claudedocs/research_*.md` |
> | `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed. Exempt by name from WC-4, AC-1.1 and AC-1.2 (M1). |
```

Self-check (`grep -nF`, run before the verdict): every AFTER line was found in SPEC (for example SPEC:62, 79, 84, 87, 112, 147, 150, 159, 172, 175-183, 194, 195, 206, 207, 208, 212, 224-243, 298), and every BEFORE line was found in BASE (for example BASE:62, 79, 84, 87, 112, 147, 150, 159, 172, 182, 183, 194, 195, 196, 200, 265). Roles are confirmed as fixed. The blank diff lines matched the blank lines of the code blocks and carry no finding.

Empty-diff rule: the diff is not empty, so no prior blocking finding is held open by that rule.

## Prior blocking findings (from PRIOR, `review: 1 of 3`)

M3 was rejected by the verifier and kept as noted (PRIOR:11, PRIOR:85-92). It is not a prior blocking finding and is not in this table.

| id | status | evidence |
|---|---|---|
| M1 | resolved | WC-4 exception (SPEC:62); load row (SPEC:112); P1 scope marks load exempt (SPEC:159); AC-1.1 and AC-1.2 exclude load (SPEC:207-208); Decisions row (SPEC:298). Residual Medium point in N2. |
| M2 | resolved | 7.2 step 3 P0 form (SPEC:194); AC-0.4 names the P0 form (SPEC:206). |
| M4 | open (partial) | Troubleshoot and workflow are fixed: step 4 is now `test -s` in P0 (SPEC:195, SPEC:206). Adversarial is not. AC-0.4 still asks for `test -s` on "the command's existing report" for `/sc:adversarial --output <dir>` (SPEC:206), and the spec names no such file. INV-A:35 and INV-A:60 state the skill names no filename and that real runs wrote the contract in more than one location. Blocking, see M4 below. |
| M5 | resolved | Scope sentence now says Phase 1 adds the flag, section and contract to all ten 3.1 commands (SPEC:79); brainstorm and init-lite rows say P1 (SPEC:84, SPEC:87). |
| M6 | resolved | AC-2.2 is a per-command table covering all 15 P2 commands (SPEC:212, SPEC:224-243). roadmap moved to AC-3.2 (SPEC:225, SPEC:217). Residual Medium points in N4. |
| M7 | resolved | Scans use alternation under `-E` (SPEC:176, SPEC:180); the self-test is present (SPEC:183). Re-run in the sandbox against the SPEC:183 pattern: prints `SELFTEST-OK`, and an uppercase `ORCA orchestration` line also matches. Exclusions stated in SA-2 and SA-5 (SPEC:147, SPEC:150). The two repo scans could not be run here (no `src/` tree), so they are UNVERIFIED. Residual Medium point in N5. |

Regressed: none. No prior report marked a finding resolved.

### M4 (open, blocking): AC-0.4 step 4 still has no path for adversarial

- Candidate text: "step 4 is `test -s` on that report" for `/sc:adversarial --compare <two files> --depth quick --output <dir>` (SPEC:206). The P0 form of step 3 also checks "the report path against the command's existing report" (SPEC:194, SPEC:206).
- Grading sentence: An implementer who runs AC-0.4 on adversarial in P0 must pick the file that `test -s` checks, because the spec names none. INV-A:35 and INV-A:60 say the skill "names no filename" and that the contract location has varied between runs. X is wrong because the criterion cannot be evaluated as written for adversarial, and that does not require any assumption beyond the spec's own text.
- Recommendation: name the P0 report file for adversarial, or drop adversarial from AC-0.4 and leave its contract check to AC-1.4 (SPEC:210).
- Priority: High. This is the P0 gate for one of the three smoke runs.

## Findings on lines changed against the baseline

### N1 (blocking, origin=changed): AC-1.1 requires P2-P4 commands to have sections in P1

- Quoted text: "the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` ..." (SPEC:207). The "except `load`" clause is the changed part. The rest of the sentence is inherited from BASE:195.
- Conflict: P1 scope (SPEC:159) adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". It adds the section only for the ten 3.1 commands (SPEC:79). Eighteen of the 27 section 3.2 rows are phased P2 to P4 (SPEC:100 auggie-review P2, SPEC:109 implement P4, SPEC:118 roadmap P3, SPEC:124 validate-roadmap P3, and the others in the Phase column at SPEC:99-125). AC-1.1 is a P1 check (SPEC:207), and a phase passes only when every check in its block passes (SPEC:167).
- Grading sentence: An implementer who follows the P1 scope (SPEC:159) adds the flag to auggie-review (SPEC:100) but no `## Unattended mode` section, because P1 scope does not name sections for 3.2 commands. AC-1.1 then fails on auggie-review, so P1 cannot pass. X is wrong because the P1 check requires a section that the P1 scope does not add, and the spec does not say which phase adds it.
- Recommendation: either scope the section check in AC-1.1 to the commands whose phase is P1 (and the 3.1 commands), or state in SPEC:159 that P1 adds the section to every 3.2 command. Choose one and make SPEC:79, SPEC:159 and SPEC:207 match.
- Priority: High. P1 cannot close while this stands.

### N2 (Medium, origin=changed): load accepts `--unattended` but its behaviour is not stated

- SPEC:159 says load accepts the flag, SPEC:112 says load has no change beyond the usage line, and SPEC:207 says load has no section. The text does not say what load does with the flag. Implementers can accept it as a no-op. No stated text is contradicted, so this is a Medium follow-up.

### N3 (Medium, origin=changed): AC-0.4 step 3 reads "status" from a Markdown report without a rule

- SPEC:194 and SPEC:206 require the P0 outcome to match "the status of the command's existing report". For troubleshoot, the existing report is `REPORT.md` (SPEC:91). The spec does not say how a status is read from it. UNVERIFIED whether `REPORT.md` carries a status field (not read in this run). An implementer must pick a reading, which makes this Medium.

### N4 (Medium, origin=changed): AC-2.2 table has an expected result the lead-in does not cover, and one check git status cannot make

- The lead-in (SPEC:225) defines only (c) blocked and (a) or (b) success. The tasklist row (SPEC:238) says "none in the row: no gate fires", which is neither. The cleanup and improve rows (SPEC:241-242) require "every listed item is unapplied in `git status`", which git status cannot establish without a baseline. Medium, testability.

### N5 (Medium, origin=changed): AC-C1 scan 2 does not apply the routing-guide exemption that SA-5 names

- Scan 2 (SPEC:180-181) excludes only `WORKER-CONTRACT.md`. The Orca section of the routing guide is exempt in SA-5 (SPEC:150) and in the scan comment (SPEC:179), but the command does not exclude it. The pass condition ("prints nothing outside the stated exclusions", SPEC:172) therefore needs a manual line-range comparison that the phase report records. The self-test (SPEC:183) passes in the sandbox. Repo scans UNVERIFIED (no `src/` tree in the sandbox). Medium.

## Follow-up candidates (Medium and minor; not blocking; not in the Reviser brief)

- N2 (SPEC:159, SPEC:207): load's behaviour under the flag.
- N3 (SPEC:194, SPEC:206): status source for a Markdown report.
- N4 (SPEC:225, SPEC:238, SPEC:241-242): AC-2.2 expected-result wording.
- N5 (SPEC:172-183, SPEC:150): scan 2 exemption is manual.
- M3 (PRIOR:85-92): rejected by the verifier; noted, unactioned. Its concern is partly covered by SPEC:79, but the P1 Commands cell (SPEC:159) still lists only some of the ten 3.1 commands.

## Coverage

- Read in full: SPEC (all 319 lines), BASE (the diff region and the prompts file), PRIOR (all), LINT (all), the review-loop prompts file in home, `command.md`, and `README.md`.
- Checked: the diff `diff -w BASE SPEC` (all changed blocks), the self-check on every changed line, the M7 self-test regex in the sandbox, and INV-A:33-60 for the adversarial row (M4).
- Not checked: other inventory citations (UNVERIFIED in this review), the repo scans (no `src/` tree), and the rf-qa.md file (not present).

## Reviser brief

Blocking finding ids: M4, N1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Run the VERIFY prompt on M4 and N1 before REVISE.

verdict: FAIL
