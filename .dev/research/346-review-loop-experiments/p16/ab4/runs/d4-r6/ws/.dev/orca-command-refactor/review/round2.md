review: 2 of 3

# Re-review of the revised candidate (mode critique, focus requirements,architecture)

- candidate (CANDIDATE): .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, sha256 969ea3c660a240d980e47aa21c5b87e0ebbb7ea61cb15bc2f7483d1290dc6ad5
- baseline (BASELINE): .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- prior (PRIOR): .dev/orca-command-refactor/review/round1.md, sha256 e472d82edca47701cd385cbb560d4c3ecf2297a50140ad3d1302d6a5c47a3b0a, header `review: 1 of 3`, so N = 2
- lint: .dev/orca-command-refactor/review/lint-2.md, produced on sha256 969ea3c6... (matches the candidate); `Checks: REF. Findings: 0.` No lint id to address.
- reviewer model used: claude-sonnet-5-5
- inputs: all four files readable and non-empty; the prior report has its `review: N of 3` header; the prior verdict is FAIL at review 1, so the review-3 halt rule does not apply.
- rf-qa Fix Cycle steps 1-5: project `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md` are not in the sandbox (unread); the Review Loop rules of the command were applied standalone, as the command allows.
- evidence limit: `cmd/`, `sk/`, `CLAUDE.md` and `INV-*` citations that the spec carries over are not re-checked here; only the three `inventory/` files and the spec text are checkable. Inventory citations I rely on are marked with their inventory line; anything else is UNVERIFIED.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`, 16 changed lines each side, verbatim)

Roles fixed from the brief: BEFORE is spec-v1.md, AFTER is the candidate. Self-check run: each of the 16 AFTER lines was found whole-line (`grep -qxF`) in the candidate and each of the 16 BEFORE lines in the baseline (16/16 and 16/16), so no role swap.

### hunk 62c62

BEFORE (baseline)
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

AFTER (candidate)
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `return-contract.yaml` in the directory the coordinator passed (`--output` / `--output-dir`); where `--output` names a file (tdd, init-lite), it writes `<file-stem>.return-contract.yaml` beside that file (M2). A section 3 row may name a different fixed path (adversarial, workflow); that path is the contract path, and workflow's `<id>` is reported by the worker's `--report-path` (M4). A ready command with no phase for a contract (init-lite) reports its section 3.1 file (M2). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

### hunk 73c73

BEFORE (baseline)
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

AFTER (candidate)
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output path (a directory, or the file for an `--output <file>` command), so the contract path is known before dispatch (WC-4) (M2); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

### hunk 76c76

BEFORE (baseline)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```

AFTER (candidate)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path WC-4 gives. Each section 3.2 command except `load`, and the four section 3.1 commands with a (P2) small fix, also gains the `## Unattended mode` section (section 2.1) in its own phase; `load`, the other section 3.1 commands and the section 4 commands get none (M1, M3, M7). Phase numbers refer to section 6.
```

### hunk 79c79

BEFORE (baseline)
```text
These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
```

AFTER (candidate)
```text
These run as workers now if the brief uses the stated flags; the worker reports the named file until the command's own phase adds the contract (M4, M5). The only command changes are the small fixes in the last column.
```

### hunk 89,91c89,91

BEFORE (baseline)
```text
| release-split | spec-shaped input; default `--r1-scope`; never `--interactive` | `<output>/release-split-report.md` | `--resume-from <split-proposal-final.md>` | Under `--unattended`, the tasklist-input "confirm with user" and `--r1-scope custom` prompt resolve as blocked (P2) | `sk/sc-release-split-protocol/SKILL.md:88,120,175,402`; `INV-B:37,117-125` |
| tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
| troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
```

AFTER (candidate)
```text
| release-split | spec-shaped input; default `--r1-scope`; never `--interactive` | `<output>/release-split-report.md` | `--resume-from <split-proposal-final.md>` | Under `--unattended`, the tasklist-input "confirm with user" and `--r1-scope custom` prompt resolve as blocked; write the contract (WC-4) (P2) (M5) | `sk/sc-release-split-protocol/SKILL.md:88,120,175,402`; `INV-B:37,117-125` |
| tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked; write `<file-stem>.return-contract.yaml` beside `--output` (P2) (M5) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
| troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked; write the contract (WC-4) (P2) (M5) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
```

### hunk 159,160c159,160

BEFORE (baseline)
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| **P2. Gate conversion** | Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval. | auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot | The main blocker class (`INV-A:96`, `INV-B:292`). These changes touch no safety rule and add no outward capability; where a command has an outward default (auggie-review posting, task's `commit`/`push` and committed TFEP report), P2 only turns it off under `--unattended` (WC-9). |
```

AFTER (candidate)
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode and the `--unattended` flag, for the eight needs-change commands named here (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. P2-P4 commands get theirs in their own phase (M1, M3). | analyze, build, business-panel, design, document, explain, index, test, load (usage line only: no flag, no section, no contract); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| **P2. Gate conversion** | Each default-on gate resolves per its section 3 row; the WC-4 contract write for release-split, tdd and troubleshoot (M5); WC-10 wait splitting for cli-eval. | auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot | The main blocker class (`INV-A:96`, `INV-B:292`). These changes touch no safety rule and add no outward capability; where a command has an outward default (auggie-review posting, task's `commit`/`push` and committed TFEP report), P2 only turns it off under `--unattended` (WC-9). |
```

### hunk 182,183c182,183

BEFORE (baseline)
```text
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
```

AFTER (candidate)
```text
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the contract path WC-4 gives, or before the command's phase adds a contract, the section 3.1 "Report today" file (M4).
4. For a command that writes a YAML contract in the phase under test: `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0. For any other command, `test -s <report file>` only (M4).
```

### hunk 194,196c194,196

BEFORE (baseline)
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate)
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 is `test -s` on the command's existing report file only (no YAML assertion), since each contract arrives in the command's own phase (M4). Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that each of the eight P1 commands that gain `--unattended` (analyze, build, business-panel, design, document, explain, index, test) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command, no `load`, and before P4 none of implement, post-release, pr-submit has one; the same assertion is added for each later phase's commands when that phase lands (M1, M3, M7) | passes |
| P1 | AC-1.2 | 7.2 live check on each of the eight P1 commands with `--unattended --output <dir>` (M7) | all steps pass |
```

### hunk 198c198

BEFORE (baseline)
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

AFTER (candidate)
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md`, the workflow return-contract ref, and `grep -n -e '--checkpoint' src/superclaude/commands/load.md` | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs; `load` lists `--checkpoint` in its Usage line (M7) |
```

### hunk 200c200

BEFORE (baseline)
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

AFTER (candidate)
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command whose section 3 row says "blocked" (recommend, cli-eval, cli-portify, review-translation, spec-panel, task, tdd, troubleshoot, release-split): a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`). For auggie-review, cleanup, improve, research, reflect and tasklist, whose rows apply a default, the same run with input that reaches the gate (M6) | blocked commands: `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`. The six default commands: `--outcome succeeded` with the row's default visible in the contract or report (flags implied, items listed unapplied, strategy pinned, headless rule followed, `--unattended` passed to reflect) (M6). Step 2 never shows `agentWait` |
```

## Prior blocking findings (re-check against the AFTER text only)

| id | status | defect (prior) | AFTER evidence |
|---|---|---|---|
| M1 | resolved | AC-1.1 and P1 scope demanded a `## Unattended mode` section on P4 commands (implement, post-release, pr-submit) before D2-D4 | AC-1.1 now lists eight named P1 commands and says "before P4 none of implement, post-release, pr-submit has one" (spec:195); P1 Scope narrowed to "the eight needs-change commands named here ... P2-P4 commands get theirs in their own phase" (spec:159); section 3 intro assigns the section "in its own phase" (spec:76). The P1 test can pass without touching a P4 command. One residual inconsistency on a changed line is recorded as follow-up F2, not blocking |
| M2 | resolved | WC-4 `<output-dir>` is a directory, but tdd and init-lite pass `--output <file>`, so the contract path would sit under a regular file | WC-4 now says "where `--output` names a file (tdd, init-lite), it writes `<file-stem>.return-contract.yaml` beside that file" (spec:62); 2.3 brief states "the output path (a directory, or the file for an `--output <file>` command)" (spec:73); tdd row repeats the rule (spec:90). A contract path now exists for the AC-2.2 tdd example at spec:200 and 7.2 step 4 (spec:183) |
| M3 | resolved | P1 Scope sentence (37 commands), P1 Commands cell (13) and AC-1.1 (37) named three different command sets | Scope sentence, Commands cell and AC-1.1 all name the same eight commands (spec:159, spec:195); count re-derived from the section 3.2 Phase column: P1 rows are analyze, build, business-panel, design, document, explain, index, test, load = 9, minus load = 8 (spec:99,101,102,106,107,108,111,112,123) |
| M4 | resolved | 7.2 steps 3 and 4 and AC-0.4 could not pass for troubleshoot (no contract in P0), workflow (`<id>` unknown) and adversarial (contract in `<output>/adversarial/`) | Step 3 accepts "the contract path WC-4 gives, or before the command's phase adds a contract, the section 3.1 'Report today' file" (spec:182); step 4 runs the YAML assertion only "for a command that writes a YAML contract in the phase under test", else `test -s <report file>` (spec:183); AC-0.4 states step 4 is `test -s` only (spec:194); WC-4 lets a section 3 row name a fixed path and reports workflow's `<id>` via `--report-path` (spec:62). Residual weakness for adversarial in P0 is follow-up F3 |
| M5 | resolved | tdd, troubleshoot and release-split were never assigned a contract write, yet AC-2.2 and AC-2.3 need one | Each of the three rows now says "write the contract" with the path (spec:89,90,91); P2 Scope lists "the WC-4 contract write for release-split, tdd and troubleshoot (M5)" (spec:160) |
| M6 | resolved | AC-2.2 demanded `blocked` from six P2 commands whose rows apply a default | AC-2.2 is split: nine commands whose row says "blocked" expect `--outcome failed` plus `blocked_question`; the six default commands (auggie-review, cleanup, improve, research, reflect, tasklist) expect `--outcome succeeded` with the row's default visible (spec:200). Count check: 9 + 6 = 15 = the P2 command list (spec:160). Row texts match: recommend, cli-eval, cli-portify, review-translation, spec-panel, task, tdd, troubleshoot, release-split say blocked (spec:115,104,105,117,120,121,90,91,89); the six default rows are spec:100,103,110,116,88,122 |
| M7 | resolved | `/sc:load` was in AC-1.1/AC-1.2 although it writes no contract or report | `load` is outside AC-1.1 and AC-1.2 (spec:195-196, "eight P1 commands"), the P1 cell says "no flag, no section, no contract" (spec:159), and AC-1.4 checks only its usage line (spec:198) |

No prior blocking finding is open or regressed. The verifier-rejected list of round 1 was empty (round1.md:11,118-120), so no id is demoted to a note.

## New findings on changed lines

Experts in sequence: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker (focus requirements and architecture; Newman, Hohpe, Crispin, Gregory, Hightower raised nothing beyond the items below).

=== REQUIREMENTS ANALYSIS ===

No blocking finding. Two Medium findings, graded with the grading check:

- **F1 (Medium, origin=changed, Wiegers/Whittaker, Divergence attack).** WC-4 says init-lite "writes `<file-stem>.return-contract.yaml` beside that file" (spec:62) and, two sentences later, that init-lite "reports its section 3.1 file" because it has "no phase for a contract" (spec:62). The init-lite row has "Small fix: None" and section 3 gives it no flag or section (spec:87,76). Grading sentence: an implementer builds either a contract writer for init-lite or nothing, and the text allows both readings; the second sentence is the more specific one and the AC set never tests init-lite, so the wrong outcome needs a guess about which reading the implementer picks. Medium (follow-up candidate). Recommendation: delete "init-lite" from the first parenthetical.
- **F2 (Medium, origin=changed, Cockburn/Wiegers).** The section 3 intro now says each section 3.2 command except `load` "also gains the `## Unattended mode` section ... in its own phase" (spec:76) and AC-1.1 adds "the same assertion ... for each later phase's commands when that phase lands" (spec:195), which includes pr-submit in P4 (spec:114). D3 option (a), the recommended one, says "no pr-submit changes in Phase 4" (spec:240), and the section 4 note makes pr-submit a worker candidate "only if the user accepts open decision D3" (spec:139). Grading sentence: under D3 (a) an implementer who follows spec:76 adds a pr-submit section that D3 (a) says is not changed. The contradiction appears only after the user answers D3, and Phase 4 waits for that answer (spec:154), so no wrong build happens before the decision; the conflict depends on the decision outcome. Medium. Recommendation: state "pr-submit only under D3 (b)" in spec:76.
- **F3 (Medium, origin=changed, Adzic/Crispin).** For adversarial in P0, step 3 of 7.2 expects the report path to equal the "Report today" file (spec:182), but that cell reads "contract, but filename not fixed" (spec:83); the fixed name arrives in P1 (spec:83). The step 4 `test -s <report file>` has no path to test until the coordinator lists `<output>/adversarial/`. Grading sentence: an implementer cannot write the P0 check literally for adversarial and picks a file by listing the directory; that needs a guess, not a contradiction. Medium. Recommendation: name `<output>/adversarial/` as the directory to list in AC-0.4.

=== ARCHITECTURE ANALYSIS ===

- Fowler: the phase to command mapping now conserves counts (see the Quantity Flow Diagram). The section-4/section-3 boundary is unchanged.
- Nygard: failure outcomes are covered by WC-4 "written on every outcome" (spec:62); the file-valued `--output` case no longer has an unwritable contract path.
- Whittaker attacks on changed lines:
  - Zero/Empty: tdd with `--output` omitted. Row 90 requires `--output <file>` in the brief (spec:90), so WC-4's sibling path always exists. Holds.
  - Divergence: `--output` a directory versus a file. WC-4 enumerates "(tdd, init-lite)" (spec:62) as the file cases; `/sc:spec-panel` also takes a file-valued `--output` (`command.md:24,460` in the sandbox, the command definition; the spec cites `cmd/spec-panel.md:22`, UNVERIFIED here) while its row says "add `--output`" (spec:120). The general rule "where `--output` names a file" still covers it. Minor note N1, origin=unchanged, not graded further.
  - Sentinel collision: the stem rule `<file-stem>` for a file with no extension or a dotted name is undefined. Minor note N2, no stated behaviour is contradicted.
  - Sequence: AC-1.1 asserts "before P4 none of implement, post-release, pr-submit has one" (spec:195); a P4 landing in the same change set as P1 would fail the P1 assertion. P4 waits for D2-D4 and for P1-P3 checks (spec:154), so the order is enforced. Holds.
  - Accumulation: AC-2.2 partition 9 + 6 = 15 matches the P2 list; no command falls outside both sets (spec:160, spec:200).

## Guard Condition Boundary Table (guards on changed lines only)

Classes left out are stated per guard in one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--output` names a file vs a directory | spec:62 | Zero/Empty | `--output` absent | n/a | tdd: brief must pass `--output <file>` (spec:90); other commands: brief states the output path (spec:73) | OK |
| same | spec:62 | One/Minimal | `--output x.md` (no directory part) | file branch | `x.return-contract.yaml` beside it; stem rule for dotted or extension-less names unstated | OK (note N2) |
| same | spec:62 | Typical | `docs/auth/TDD_AUTH.md` | file branch | `docs/auth/TDD_AUTH.return-contract.yaml` | OK |
| same | spec:62 | Legitimate Edge Case | spec-panel `--output <file>` | file branch by the general rule | covered by the rule, not listed in the parenthetical | OK (note N1) |
| same | spec:62 | Sentinel Value Match | init-lite listed as writing a contract and as having none | both | two sentences differ | GAP (F1, Medium: no wrong outcome without a guess) |
| Contract exists in the phase under test | spec:183 | Typical | tdd after P2 | true | YAML assertion on the sibling contract | OK |
| same | spec:183 | Legitimate Edge Case | troubleshoot or adversarial in P0 | false | `test -s <report file>` only; adversarial file name unfixed | GAP (F3, Medium) |
| P1 section membership | spec:195 | Typical | analyze | in set | section required | OK |
| same | spec:195 | Legitimate Edge Case | load | out of set | no section; usage-line grep only (spec:198) | OK |
| same | spec:195 | Maximum/Overflow | P4 command before P4 | out of set | none must have one | OK |
| same | spec:195, 76 | Legitimate Edge Case | pr-submit under D3 (a) | in "later phase's commands" | spec:240 says no pr-submit change | GAP (F2, Medium: depends on the D3 answer) |
| AC-2.2 partition | spec:200 | Typical | tdd with a bare topic | blocked set | `failed` plus non-empty `blocked_question` | OK |
| same | spec:200 | Legitimate Edge Case | research, cleanup | default set | `succeeded` with the default visible | OK |
| same | spec:200 | Zero/Empty | a P2 command in neither set | none | none exists (9 + 6 = 15 = spec:160) | OK |

Class "Maximum/Overflow" is left out for the `--output` and AC-2.2 guards because neither has a capacity.
No row is blocking under FR-8/FR-9: each GAP is graded Medium by the grading check.

## Quantity Flow Diagram (changed command-to-phase mapping)

```text
[Source: 43 commands (INV-A:3 = 21, INV-B:3 = 22)] --> [Classify: 10 ready (3.1) + 27 needs-change (3.2) + 6 coordinator-only (4)]
[37 worker-capable] --> [Phase: P1 = 9 (8 with section + load) | P2 = 11 + 4 ready (reflect, release-split, tdd, troubleshoot) = 15 | P3 = 4 | P4 = 3 | none = 2 + 4 other ready fix-only (brainstorm, init-lite, adversarial, cleanup-audit, index-repo, workflow)]
[Section consumers] AC-1.1: 8 commands       (expected 8, consistent with spec:159)
                    P2 assertions: 15 sections (11 + 4 ready; AC-2.1, 'later phase' clause, spec:195)
                    AC-2.2: 9 blocked + 6 default = 15 (consistent with spec:160)
                    P3 = 4, P4 = 3
Sections total: 8 + 15 + 4 + 3 = 30 = 26 (27 minus load) + 4 ready commands with a (P2) fix
```

No count mismatch.

## Coverage

scoped PASS: changed lines + prior blockers

Covered: all 16 changed line pairs of the diff, the seven prior blocking findings, the spec text that the changed lines depend on (spec:62-73, 76-125, 154-162, 182-183, 194-200, 238-247). Not covered: the unchanged remainder of the document; a whole-document check needs a separate, labelled first review.

## Follow-up candidates (Medium and minor; none blocks)

- F1 (Medium) init-lite named as writing a contract and as having none, spec:62.
- F2 (Medium) section-3 intro and AC-1.1 later-phase clause vs D3 (a) for pr-submit, spec:76, spec:195, spec:240.
- F3 (Medium) adversarial P0 report path unfixed for 7.2 step 3, spec:182-183 and spec:83.
- N1 (minor, origin=unchanged) spec-panel `--output` is file-valued but its row says "add `--output`", spec:120.
- N2 (minor) `<file-stem>` undefined for extension-less or dotted names, spec:62.
- N3 (minor, origin=unchanged) AC-1.4 `grep -n -e '--checkpoint'` matches any line of load.md; the pass condition is the Usage line (spec:198, `inventory/commands-b.md:63`).
- N4 (minor, origin=unchanged) 2.3 and WC-2 tell the coordinator to pass `--unattended` to every command (spec:73) although sections 3.1 gives adversarial, cleanup-audit, index-repo and workflow no such flag (spec:83,85,86,92). Inherited from the baseline.

The session that ran this review asks the user once per loop whether to open an issue for these; this worker run has no user channel, so it only records the list and creates nothing.

Brief clauses overridden: none. The brief did not widen scope or regrade a minor finding.

## Reviser brief

No blocking finding ids; nothing to revise. (Rules if a later round reopens one: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing; report byte sizes before and after with bytes added and deleted per finding id.)

verdict: PASS
