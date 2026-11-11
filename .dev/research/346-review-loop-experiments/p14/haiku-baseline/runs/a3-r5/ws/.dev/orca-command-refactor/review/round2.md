review: 2 of 3

# Spec-panel critique: Orca worker-contract spec, round 2 (re-review)

- candidate (CANDIDATE, `SPEC:n`): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (291 lines; sha256 `013a84aaca6a86058868c7f7b79fe52a951e5bbb08547665cff18e7d59d845ed`)
- baseline (BASELINE, `BASE:n`): `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines; sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`)
- prior report (PRIOR, `R1:n`): `.dev/orca-command-refactor/review/round1.md` (256 lines; sha256 `9c249bd980443bc70968e12bbee854ec29fe75bc3bda9f318601ee3fb89b1407`)
- mode: critique; focus: requirements, architecture; format: standard; re-review of round 1
- reviewer model used: claude-haiku-5-5
- review prompt: RE-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox copy read in full, sha256 `3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8`)
- review number: prior report is `review: 1 of 3`, so this is `review: 2 of 3`
- rf-qa process (command step 5): neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` is in the sandbox, so the rules in the command's Review Loop section stand alone.
- shared rules: `~/.claude/WORKER-CONTRACT.md` is not in the sandbox. It governs `--unattended` runs only, and this run is not one, so it was not needed.
- citation rule: a citation is "checked" when its target is a file inside the workspace (`.dev/orca-command-refactor/`) and I read the cited line. Citations to `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `pyproject.toml`, `CLAUDE.md` and Orca's installed files are outside the workspace and are UNVERIFIED in this run.
- no revised specification was written: this is a re-review, so `--iterations` is ignored and the Improve step is skipped.

## Coverage

Read in full: CANDIDATE, BASELINE (through the diff), PRIOR, the review-loop prompt file, and the README (binding shared context). Checks run in the sandbox:

- Step 1 evidence block (below) from `diff -w BASELINE CANDIDATE`.
- Self-check: every AFTER line (`>`) was found in CANDIDATE with `grep -cF`, and every BEFORE line (`<`) in BASELINE. All quotes matched, so the roles are not swapped.
- Gate test for F-02: the AC-C1 pattern as now written in `SPEC:181` was run on sample lines with `printf` (no file written). `orca orchestration`, `orca worktree`, `orca-ide terminal` and `orca agent` each matched once; `the orca spec` matched zero times. The pattern in the prior candidate, with `\|`, matched zero times on `orca orchestration`.

Not re-read in this round: the inventories under `.dev/orca-command-refactor/inventory/` (no changed claim depends on a new inventory line). The round 1 citation checks on `CAPS:*` and `INV-*:*` stand as recorded in PRIOR; they are not repeated here.

## Step 1: evidence block (diff -w BASELINE CANDIDATE, verbatim)

`<` lines are BEFORE (baseline). `>` lines are AFTER (candidate). Hunk headers are kept.

```text
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. Exempt: `load`, which writes no file and is used as a brief step (section 3.1; F-03). | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
85,87c85,87
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
---
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report and write `return-contract.yaml` beside it. The output dir is fixed today, so under `--unattended` the output path carries a per-run slug the coordinator passes; two runs in one worktree then never share `progress.json` (WC-11) (P1; F-03, F-04) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location and write `return-contract.yaml` beside it (P1; F-03) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | Write `return-contract.yaml` beside the `--output` report (P1; F-03) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
89,91c89,91
< | release-split | spec-shaped input; default `--r1-scope`; never `--interactive` | `<output>/release-split-report.md` | `--resume-from <split-proposal-final.md>` | Under `--unattended`, the tasklist-input "confirm with user" and `--r1-scope custom` prompt resolve as blocked (P2) | `sk/sc-release-split-protocol/SKILL.md:88,120,175,402`; `INV-B:37,117-125` |
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
---
> | release-split | spec-shaped input; default `--r1-scope`; never `--interactive` | `<output>/release-split-report.md` | `--resume-from <split-proposal-final.md>` | Under `--unattended`, the tasklist-input "confirm with user" and `--r1-scope custom` prompt resolve as blocked (P2). Write `return-contract.yaml` beside `release-split-report.md` (P1; F-03) | `sk/sc-release-split-protocol/SKILL.md:88,120,175,402`; `INV-B:37,117-125` |
> | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2). Write `return-contract.yaml` beside the TDD at `--output` (P1; F-03) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2). Write `return-contract.yaml` on every outcome, not only with `--caller task-unified` (P1; F-03) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
125c125
< | validate-tests | no gate | give the skill a way to write the `--report` file (it has neither Write nor Bash) | n/a | fix the default target `tests/sc-task/`, which does not exist | `cmd/validate-tests.md:6,22,33`; `sk/sc-validate-tests-protocol/SKILL.md:4`; `INV-B:51,257-265` | P3 |
---
> | validate-tests | no gate | give the skill a way to write the `--report` file (it has neither Write nor Bash) | n/a | fix the default target `tests/sc-task/`, which does not exist; write `return-contract.yaml` beside the `--report` file (P3; F-03) | `cmd/validate-tests.md:6,22,33`; `sk/sc-validate-tests-protocol/SKILL.md:4`; `INV-B:51,257-265` | P3 |
159c159
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
---
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); init-lite, tdd, troubleshoot, release-split (contract only; their gate fixes stay in P2) (F-03); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
172c172
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
---
> | AC-C1 | the grep in the block below this table (F-02) | prints nothing (SA-2, WC-8) |
177a178,183
> AC-C1 command (F-02; `|` is alternation in `grep -E`, and `\|` matches a literal bar, so the `\|` form never matched). Gate test before first use: the three sample lines `orca orchestration`, `orca worktree` and `orca-ide terminal` must all print; keep the test as a fixture in `tests/skills/test_worker_contract.py`.
> 
> ```bash
> grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core | grep -v '^src/superclaude/skills/ccsession-tag/'
> ```
> 
182c188
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
---
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path from P1 on, and the command's existing report file in P0 (F-01).
194c200
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
---
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; steps 3 and 4 check the command's existing report file (`REPORT.md` for troubleshoot, `.dev/tasks/to-do/<id>/return-contract.yaml` for workflow, the adversarial return contract as written today), because the WC-4 path check starts in P1 (F-01). Record the results in the phase report; a failure here reopens section 1 |
```

Changed-line map of CANDIDATE: `SPEC:62` (WC-4), `SPEC:85-91` (3.1 rows cleanup-audit, index-repo, init-lite, release-split, tdd, troubleshoot), `SPEC:125` (validate-tests), `SPEC:159` (P1 row), `SPEC:172` (AC-C1), `SPEC:178-183` (AC-C1 command block, added), `SPEC:188` (7.2 step 3), `SPEC:200` (AC-0.4).

## Prior blocking findings

| Prior id | Prior status | Now | Basis (AFTER text only) |
|---|---|---|---|
| F-01 | open (blocking) | **open** (narrowed; see F-01 below) | `SPEC:188` fixed the report-path clause of step 3. `SPEC:189` (step 4) and `SPEC:200` (AC-0.4) still conflict for troubleshoot. |
| F-02 | open (blocking) | **resolved** | `SPEC:172` points to the block below the table. `SPEC:181` uses plain `\|`-free alternation `(orchestration|worktree|terminal|agent)`. The gate test above matched the three sample lines the spec names. |
| F-03 | open (blocking) | **open** (narrowed to cleanup-audit; see F-03 below) | Every other command in the R1 list now has a contract assignment (`SPEC:62`, `SPEC:86-91`, `SPEC:125`, `SPEC:159`). cleanup-audit (`SPEC:85`) still writes the contract only for a run the brief does not request. |
| F-04 | open (blocking) | **resolved** | `SPEC:85` gives cleanup-audit a per-run slug under `--unattended`, and removes the false WC-11 "one audit per worktree" citation. The flag that carries the slug is not named (N-5, Medium). |

### F-01 (MAJOR, BLOCKING, open): AC-0.4 still has a step that cannot pass in Phase 0

- Location: `SPEC:200` (AC-0.4) against `SPEC:189` (7.2 step 4) and `SPEC:91` (troubleshoot row, `REPORT.md`).
- Changed: yes (`SPEC:200` is in the diff, `194c200`). The step-3 clause at `SPEC:188` is changed too.
- What the fix resolved: `SPEC:188` now reads "its report path is the WC-4 contract path from P1 on, and the command's existing report file in P0". That removes the P0 path conflict that R1 F-01 named.
- What remains: `SPEC:200` says "steps 3 and 4 check the command's existing report file (`REPORT.md` for troubleshoot, ...)". `SPEC:189` (step 4), unchanged from BASE:183, runs `yaml.safe_load` and asserts `d['status']` and `d['command']`. `REPORT.md` is a markdown report (`SPEC:91`), so the YAML assertion cannot pass on it.
- Grading sentence: "An implementer who runs AC-0.4 on `/sc:troubleshoot` in P0 applies the YAML assertion of `SPEC:189` to `REPORT.md`, which has no `status` or `command` key, and the check fails on a correct run, which is wrong because `SPEC:200` says a failure there reopens section 1." This holds with no added assumption: `SPEC:200` names `REPORT.md`, and `SPEC:189` requires a YAML file with those keys.
- Grade: blocking. The wrong outcome is a correct P0 smoke run recorded as failing the gate that decides section 1.
- Recommendation: in AC-0.4, give the troubleshoot P0 check its own rule (for example "`REPORT.md` exists and its first line states the status"), and limit `SPEC:189` to YAML contracts. Name which check applies to which command.
- Origin: changed (`SPEC:200`, `SPEC:188`).
- Expert: Adzic (acceptance criteria that cannot pass), Wiegers (traceability of the gate).

### F-03 (MAJOR, BLOCKING, open): cleanup-audit writes no contract for the run the brief requests

- Location: `SPEC:85` (cleanup-audit row) against `SPEC:62` (WC-4) and the row's own "Brief must pass" column (`--pass <N>` (single pass)).
- Changed: yes (`SPEC:85`, `85c85` in the diff).
- What the fix resolved: the other commands named in R1 F-03 (init-lite `SPEC:87`, tdd `SPEC:90`, troubleshoot `SPEC:91`, release-split `SPEC:89`, index-repo `SPEC:86`, validate-tests `SPEC:125`) now carry a contract row. `load` is exempted at `SPEC:62`. All 27 commands in the 3.2 table (`SPEC:94-126`) are assigned to a phase (P1-P4, `SPEC:158-162`).
- What remains: `SPEC:85` says "Name the `--pass all` final report and write `return-contract.yaml` beside it." The brief requires `--pass <N>`. A single-pass run therefore has no location given for the contract at all, although `SPEC:62` says the file is written "on success, failure, blocked and partial outcomes".
- Grading sentence: "An implementer who dispatches cleanup-audit with the brief's `--pass <N>` gets a run that writes no `return-contract.yaml`, which is wrong because `SPEC:62` requires the file on every outcome and `SPEC:73` has the coordinator open it." This holds with no added assumption: the row names only the `--pass all` report as the contract location, and it names `--pass <N>` as the required flag.
- Grade: blocking. A completed run leaves the coordinator with a missing file, and `SPEC:189` fails.
- Recommendation: state that a single-pass run writes `return-contract.yaml` beside its `pass<N>-summary.md`, and that `--pass all` writes it beside the final report.
- Origin: changed (`SPEC:85`).
- Expert: Fowler (interface contract coverage), Wiegers (each requirement needs an owner).

### F-04 (MINOR, MEDIUM in R1, resolved): cleanup-audit shared paths

- Location: `SPEC:85`.
- The false citation of WC-11 for a "one audit per worktree" rule is gone. The defect that two runs share `progress.json` is addressed by the per-run slug under `--unattended`. The R1 recommendation's first option (a per-run path in P1) is taken.
- Medium follow-up N-5 below: the flag that carries the slug is not named, and is not added to the brief-must-pass column or to section 2.3.

## New and narrowed findings on changed lines

### N-1 (MEDIUM, follow-up): WC-4 names a directory where init-lite and tdd pass a file

- Location: `SPEC:62` (WC-4: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)") against `SPEC:87` (init-lite `--output <file>`) and `SPEC:90` (tdd `--output <file>`).
- Grade: Medium. The row's "beside the report" reading gives the parent directory, so the implementer must choose a reading that WC-4 does not state.
- Origin: changed (`SPEC:87`, `SPEC:90`).

### N-2 (MINOR): WC-4 cites the wrong section for `load`

- Location: `SPEC:62` ("Exempt: `load`, ... (section 3.1; F-03)"). The load row is in the 3.2 table (`SPEC:112`, under the heading at `SPEC:94`), not in 3.1 (`SPEC:78`).
- Origin: changed (`SPEC:62`).

### N-3 (MEDIUM, follow-up; with R1 F-08): troubleshoot's contract path is not known before dispatch

- Location: `SPEC:91` (troubleshoot row, "write `return-contract.yaml` on every outcome") and its "Brief must pass" column (`no --fix`, no output flag).
- WC-4 (`SPEC:62`) requires the path to be known before dispatch from the directory the coordinator passed. This row passes no output flag, and the spec does not state the default directory. The contract is assigned, but its path is not determinable from the spec.
- Grade: Medium. The default directory is recorded in the inventory, so an implementer can look it up.
- Origin: changed (`SPEC:91`).

### N-5 (MEDIUM, follow-up): the cleanup-audit slug has no flag

- Location: `SPEC:85` ("the output path carries a per-run slug the coordinator passes"). The "Brief must pass" cell (`SPEC:85`, col. 2) and section 2.3 (`SPEC:73`) do not name the flag.
- Grade: Medium. The coordinator cannot pass a slug the spec does not name a flag for.
- Origin: changed (`SPEC:85`).

### Sentence-level note on F-01 (MINOR): step 3 still names the contract for its outcome

- Location: `SPEC:188` ("its `--outcome` matches the contract's `status` under WC-5"). In P0 there is no contract, and `SPEC:200` does not redirect this clause to the report's status.
- Grade: Medium follow-up. The reading "use the report's status" is likely, but the text does not state it.
- Origin: changed (`SPEC:188`).

### Other changed lines checked, no finding

- `SPEC:159` (P1 row): now lists init-lite, tdd, troubleshoot, release-split as "contract only; their gate fixes stay in P2". Consistent with `SPEC:89-91` and `SPEC:125` (P3). No new defect. The scope/command-list disagreement of R1 F-14 is unchanged and stays a follow-up.
- `SPEC:125` (validate-tests, P3): contract beside the `--report` file. The skill's lack of a write tool is covered by the same row's fix. No new defect.
- `SPEC:178-183` (AC-C1 block, added): the command runs and matches the three sample lines. No new defect.

## Unchanged findings (origin=unchanged, minor notes unless they quote a changed line)

All R1 findings F-05 to F-20 except F-03, F-04, F-08 (see N-3) and F-14 (line 159 changed) point to lines this round did not change, so they carry as minor notes. Where a finding depends on a changed line, it is listed with that dependency under follow-up candidates. Nothing in those findings was re-graded to blocking.

## follow-up candidates (Medium and minor; not blocking)

- F-05 E3 mixes two runs (`SPEC:23`; origin=unchanged)
- F-06 E2 tool-parity overclaim (`SPEC:22`; origin=unchanged)
- F-07 WC-4 states as fact an UNVERIFIED point (`SPEC:62`, `SPEC:274`; origin=unchanged text, WC-4 line changed; minor)
- F-08 contract path rule vs per-command paths (`SPEC:62`, `SPEC:83`, `SPEC:91`, `SPEC:92`, `SPEC:228`; origin=changed through N-3 at `SPEC:91`)
- F-09 Phase 0 and 3.1 briefs omit `--unattended` (`SPEC:73`, `SPEC:79`, `SPEC:81-92`, `SPEC:158`, `SPEC:200`; origin=unchanged; `SPEC:200` quotes P0 runs without the flag)
- F-10 worker-session rules have no stated loader (`SPEC:52`, `SPEC:61-70`, `SPEC:73`; origin=unchanged)
- F-11 AC-C5 checks command files only (`SPEC:149`, `SPEC:159-161`, `SPEC:176`; origin=unchanged)
- F-12 WC-1, WC-5 first sentence, WC-6, WC-12 without an AC; WC-1 unquantified (`SPEC:59`, `SPEC:63`, `SPEC:64`, `SPEC:70`; origin=unchanged)
- F-13 AC-C1 scope covers `src/superclaude/core`, against the P0 routing-guide section (`SPEC:147`, `SPEC:150`, `SPEC:158`, `SPEC:172`; origin=unchanged, depends on the changed block `SPEC:178-183`)
- F-14 P1 scope vs P1 commands vs AC-1.1 (`SPEC:159`, `SPEC:195`, `SPEC:196`; origin=changed at `SPEC:159`; the disagreement remains)
- F-15 WC-5 undefined status combinations (`SPEC:62`, `SPEC:63`, `SPEC:263`; origin=unchanged)
- F-16 re-invocation after an answer vs fresh-directory default (`SPEC:61`, `SPEC:64`; origin=unchanged)
- F-17 WC-10 threshold and cadence (`SPEC:68`, `SPEC:181`; origin=unchanged)
- F-18 D4 outward authorization is not checkable (`SPEC:67`, `SPEC:244-247`; origin=unchanged)
- F-19 plugin command mirror has no check (`SPEC:168`, `SPEC:173`, `SPEC:279`; origin=unchanged)
- F-20 D3 counts (`SPEC:114`, `SPEC:128`, `SPEC:139`, `SPEC:240`; origin=unchanged)
- N-1 WC-4 directory vs file-valued `--output` (`SPEC:62`, `SPEC:87`, `SPEC:90`)
- N-2 WC-4 cites section 3.1 for `load`, which is in 3.2 (`SPEC:62`, `SPEC:112`)
- N-3 troubleshoot contract path not known before dispatch (`SPEC:91`)
- N-5 cleanup-audit slug flag not named (`SPEC:85`, `SPEC:73`)
- step 3 outcome clause still names the contract in P0 (`SPEC:188`)

## Reviser brief

Revise only the blocking finding ids listed here: **F-01, F-03**. Restating the review-loop rule for the reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited under it. F-02 and F-04 are resolved and are not part of it.

Brief clauses overridden: none.

verdict: FAIL
