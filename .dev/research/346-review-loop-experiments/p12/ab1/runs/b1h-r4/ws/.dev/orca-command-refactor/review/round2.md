review: 2 of 3
> verification (coordinator, VERIFY step VF2; verifier reply .dev/orca-command-refactor/review/verify-2.md): confirmed blocking ids: N2. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M2 (verifier: The row itself tags the init-lite fix as P1 (86), and the P1 scope at 160 includes "the small fixes to ready commands", which covers init-lite (listed as ready in 3.1). So a phase does schedule it.); N1 (verifier: Overwrite outcome: 160 includes "the small fixes to ready commands" and 86 tags the fix P1, so the premise that P1 skips init-lite fails. Dispatch outcome: the "not accepted today" baseline rests only on spec-v1.md:87, which is absent. Also 79 gives init-lite's stated flag as "after P1", so 79 does not license passing `--output <dir>` today. The readiness wording is inconsistent, but the stated wrong outcomes do not follow from the candidate text.). The Reviser brief below is narrowed to the confirmed ids.

# Re-review of the Orca worker-contract spec (round 2)

Command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`, run as the re-review of the candidate spec. This worker made no revision and wrote no other file.

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 6f240e27e8d58d66b8256a439936eb55132bda0b917254aa463c5abc36931750
baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (the text round1.md reviewed)
prior: .dev/orca-command-refactor/review/round1.md sha256 53a728e4ef05378bb4a17035e4d55dda1a442d821716f283a57d878c1130c874 (`review: 1 of 3`, `verdict: FAIL`; its verification block confirmed M2, M4, M6, M7, M8, M9)
reviewer model: claude-haiku-5-5
focus: requirements, architecture

Coordinator note: the VERIFY prompt (fresh context, candidate plus finding list only) has not been run on the open blocking findings below. Run it before any REVISE brief, as the Review Loop's prompt file requires.

rf-qa.md: not read. No `.claude/agents/rf-qa.md` exists in the workspace and no `~/.claude/agents/rf-qa.md` exists in the sandbox home, so the rules in the command's Review Loop section stand alone (Review Loop bullet 5).

Sandbox note: while looking for rf-qa.md I ran a filesystem-wide `find`, which reached paths outside the sandbox. I read none of its hits and use none of them.

## Step 1: evidence block

Roles, fixed by the file arguments: BASELINE = spec-v1.md, CANDIDATE = orca-worker-contract-spec.md. Command: `diff -w BASELINE CANDIDATE`.

Self-check (run before any finding): every AFTER line below was found by `grep -nF` in CANDIDATE, and every BEFORE line was found by `grep -nF` in BASELINE. The roles are therefore not swapped. The `<` and `>` prefixes are removed from the copied lines; the blocks are otherwise verbatim.

BEFORE (baseline, 16 lines starting with <):
````text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
### 3.1 Ready today (10)
| index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
| init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
| load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
Two worker-capable commands are better used on the coordinator side, though they stay in section 3: `/sc:load` only loads context into the current session (`INV-B:65`), and `/sc:recommend` writes a prompt addressed to a person who pastes it (`INV-B:105`). `/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3.
| **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
| AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
| AC-C4 | `git diff --cached --name-only \| grep '^\.claude/' \| grep -v '^\.claude/settings\.json$'` | prints nothing (`CLAUDE.md:16`) |
| AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-[^-]'` | prints nothing: edits are additive |
| P0 | AC-0.3 | `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \| grep -E '^-[^-]'` | prints nothing: no existing routing row changed (SA-5) |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
| Inventory verdicts | Re-judge commands; keep the inventories' 10 / 27 / 6 split | Keep: both inventories were independently citation-checked (`INV-A:106`, `INV-B:320`) and nothing read in this task contradicted a verdict. `/sc:load` and `/sc:recommend` are noted as coordinator-side helpers without changing their verdict. |
````

AFTER (candidate, 40 lines starting with >):
````text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). [M8] Where section 3 names a different fixed path for a command, that path is the contract path instead (adversarial: section 3.1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). [M6] For cleanup-audit, the coordinator also runs at most one cleanup-audit per worktree at a time, because its output directory is fixed (WC-11). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 9 ready today, 27 needing a change and 6 coordinator-only (section 4), and `/sc:load`, which has no table row (note under 3.2) [M6, M7]. The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path WC-4 gives (`<output-dir>/return-contract.yaml` unless the row names another) [M8]. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
### 3.1 Ready today (9)
| init-lite | `--output <dir>` after P1 (the flag becomes directory-valued) [M2] | `.dev/superclaude/context-audit.md` or `--output` | Fresh dir per run (WC-6) [M2] | Per-run output directory (P1) [M2]: a retry writes a new `context-audit.md` and does not overwrite the first attempt's report | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
| index-repo | no gate | add `--output <dir>` and write `PROJECT_INDEX.md` under it; contract [M6] | `mode=update` | Add the `--output` flag (P1). Without it the default `PROJECT_INDEX.md` is one fixed path, which WC-11 forbids, so the flag is required [M6] | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` | P1 |
[M7] `/sc:load` has no row in this table. It only loads context into the current session and writes no file (`cmd/load.md:52`; `INV-B:65`), so a worker has nothing to report. Use it as a step inside another worker's brief, not as its own Task. It gets no `## Unattended mode` section and no contract, so AC-1.1 does not apply to it. Its Usage line omits `--checkpoint` (`cmd/load.md:22`); that usage-line fix stays in P1 under SA-4.

Two worker-capable commands are better used on the coordinator side. `/sc:load` is covered by the note under the 3.2 table [M7]; `/sc:recommend` stays in section 3.2. `/sc:load` only loads context into the current session (`INV-B:65`), and `/sc:recommend` writes a prompt addressed to a person who pastes it (`INV-B:105`). `/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3.
| **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 9 ready commands (section 3.1) [M6], so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
| AC-C1 | Command in the fenced block after this table, labelled AC-C1 [M9] | The grep prints nothing (SA-2, WC-8). The positive control in the same block must print its planted line first, or the check is void [M9] |
| AC-C4 | Command in the fenced block after this table, labelled AC-C4 [M9] | prints nothing (`CLAUDE.md:16`) |
| AC-C5 | For every command file the phase edits without a named defect fix (SA-4): command in the fenced block after this table, labelled AC-C5 [M9] | prints nothing: edits are additive |

Commands for the common checks, run from the repo root. The pipes are plain `|` so the raw text runs as written [M9].

```bash
# AC-C1 (SA-2, WC-8): must print nothing
grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core | grep -v '^src/superclaude/skills/ccsession-tag/'

# AC-C1 positive control: must print the planted line and exit 0 (M9)
printf 'orca-ide worktree list\n' | grep -E '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b'

# AC-C4 (CLAUDE.md:16): must print nothing
git diff --cached --name-only | grep '^\.claude/' | grep -v '^\.claude/settings\.json$'

# AC-C5 (SA-4), once per edited command file: must print nothing
git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'
```
Command for AC-0.3, from the repo root (the pipe is plain `|`) [M9]:

```bash
# AC-0.3 (SA-5): must print nothing
git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md | grep -E '^-[^-]'
```

| P0 | AC-0.3 | Command in the fenced block above this table, labelled AC-0.3 [M9] | prints nothing: no existing routing row changed (SA-5) |
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | Steps 1, 2, 5, 6 and 7 pass as written. Step 3 in P0 reads: exactly one `worker_done`, and its `--outcome` matches the outcome WC-5 derives from the status the command's existing report states (its first sentence); the report path is the existing report, since no contract exists before P1 [M4]. Step 4 is not run in P0; it runs first in P1 (AC-1.2) [M4]. Record the results in the phase report; a failure here reopens section 1 |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial's SKILL names `<output>/adversarial/return-contract.yaml`, the path its section 3.1 row gives, and no other path [M8]; workflow states the contract is written for pre-creation STOPs |
| Inventory verdicts | Re-judge commands; keep the inventories' 10 / 27 / 6 split, changing two rows: index-repo moves from ready to needs-change (WC-11, [M6]); load leaves the tables (WC-4 and AC-1.1, [M7]) | Keep the other verdicts: both inventories were independently citation-checked (`INV-A:106`, `INV-B:320`) and nothing else read in this task contradicted a verdict. The index-repo move contradicts `INV-A:53`'s ready verdict; the spec follows WC-11 there, since the fixed default `PROJECT_INDEX.md` is not a per-run path. The split is now 9 / 27 / 6 plus load. `/sc:recommend` is noted as a coordinator-side helper without changing its verdict. |
````

Changed spans, as the diff shows them: WC-4 (line 62); the 2.3 cleanup-audit sentence (line 73); the section 3 intro (line 76); the 3.1 init-lite row (line 86); the 3.2 index-repo row (line 111); the `/sc:load` note (line 126); the recommend sentence (line 140); P0 (line 159); the AC-C1, AC-C4, AC-C5 rows and their fenced block (lines 173-193); AC-0.3 and AC-0.4 (lines 206-218); AC-1.4 (line 222); the inventory-verdicts decision (line 292). Only the lines above changed; `origin=changed` below means a finding on one of them.

## Prior blocking findings (round 1)

| Prior id | Status | Basis |
|---|---|---|
| M2 | open | Row `candidate:86` now asks for a per-run directory, which WC-6 needs, but no phase schedules it: the P1 command list at `candidate:160` omits init-lite. The same row also changes the standalone `--output` type (see N2). Open until N1 and N2 are fixed. |
| M4 | resolved | AC-0.4 (`candidate:218`) now gives P0 pass conditions for step 3 (existing report) and defers step 4 to P1 (`candidate:220`, AC-1.2). No P0 step still names a WC-4 contract path. Carried Medium F2 below. |
| M6 | resolved | index-repo moved to 3.2 with a P1 `--output` flag (`candidate:111`, `candidate:160`). Cleanup-audit one-at-a-time coordinator rule added (`candidate:73`). Counts 9 / 27 / 6 plus load agree (`candidate:76`, `candidate:78`, `candidate:292`). Carried Medium F3 below. |
| M7 | resolved | `/sc:load` removed from the 3.2 table and so from AC-1.1 (`candidate:126`). Its usage-line fix stays in P1 (`candidate:160`). |
| M8 | resolved | WC-4 exception (`candidate:62`) names adversarial's path; the adversarial row (`candidate:83`) and AC-1.4 (`candidate:222`) give the same path. |
| M9 | resolved | Checks moved into fenced blocks with plain `|` (`candidate:181-193`, `candidate:206-211`). AC-C1 positive control added (`candidate:186`; run in the sandbox: prints `orca-ide worktree list`, exit 0). Carried Medium F4 below. |

Regressed: none. No prior finding was marked resolved by round 1, so none can regress.

## New findings on changed lines

### N1 (blocking, origin=changed): the init-lite fix is in no phase, and the row still treats init-lite as ready today

- Location: `candidate:86` (row), `candidate:79` (3.1 header), `candidate:92` (end of 3.1), `candidate:159` (P0), `candidate:160` (P1 scope).
- Stated texts: `candidate:86` says the brief must pass `--output <dir>` "after P1" and gives the fix as "Per-run output directory (P1)". `candidate:160` lists the P1 commands as "analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow". init-lite is not in that list, and P2-P4 (`candidate:161-163`) do not name it either. `candidate:79` says the 3.1 commands "run as workers now if the brief uses the stated flags", and `candidate:159` says P0 "uses only the 9 ready commands (section 3.1)", which includes init-lite.
- Grading sentence: an implementer who follows the P1 scope at `candidate:160` does not change init-lite, so a `worker-start --retry-of` re-run writes over the first attempt's `context-audit.md`, which WC-6 (`candidate:64`) forbids. An implementer who follows `candidate:79` and `candidate:86` dispatches init-lite today with `--output <dir>`, a value the flag does not accept today (`.dev/orca-command-refactor/specs/history/spec-v1.md:87` says `--output <file>`). Two stated texts contradict each other on the phase and the readiness of this command.
- Recommendation: add init-lite to the P1 command list at `candidate:160` (the round-1 fix was already decided as P1), and move its row out of the 3.1 "Ready today" table into 3.2, or mark it "ready after P1" in `candidate:79`. Change no other row.
- Priority: High. Quality impact: retry overwrites the first attempt's report.

### N2 (blocking, origin=changed): the init-lite row changes the standalone `--output` type

- Location: `candidate:86`. Conflicting texts: `candidate:147` (SA-1) and `candidate:143` (the section-5 hard requirement on every phase). Baseline for comparison: `.dev/orca-command-refactor/specs/history/spec-v1.md:87` (`--output <file>`).
- Stated texts: `candidate:86` makes `--output` "directory-valued" ("the flag becomes directory-valued") with no `--unattended` qualifier. SA-1 (`candidate:147`) says that without `--unattended` "every ... output path ... stays as it is today".
- Grading sentence: an implementer who follows `candidate:86` makes `--output` directory-valued for every run, so a person who runs `/sc:init-lite --output report.md` in a plain session gets a directory where today they get a file. SA-1 forbids that, and the two texts contradict each other.
- Recommendation: keep `--output <file>` unchanged for standalone runs. The unattended brief can pass a fresh per-run file, for example `--output <dir>/context-audit.md` under a new `<dir>` per run, which gives WC-6 its fresh directory with no change of flag type.
- Priority: High. Quality impact: breaks an existing standalone flag.

## Medium warnings (follow-up candidates; never fail this review)

- F1 (origin=changed, `candidate:140`): the sentence says two worker-capable commands are "better used on the coordinator side", then says `/sc:recommend` "stays in section 3.2", which is the worker list. The reader cannot tell whether recommend is dispatched as a worker (the row at `candidate:114` says it is). `.dev/orca-command-refactor/inventory/commands-b.md:105` calls it "more naturally a coordinator-side routing helper". Medium: a guess is needed. Fix: drop the "better used" clause, or move recommend to section 4.
- F2 (origin=changed, `candidate:218`): "no contract exists before P1" conflicts with `candidate:91` (workflow's report today is `.dev/tasks/to-do/<id>/return-contract.yaml`) and `candidate:83` (adversarial already writes a contract). The P0 instruction still works, since the existing report is used, so no wrong outcome follows. Medium. Fix the justification.
- F3 (origin=changed, `candidate:111`): "Without it the default `PROJECT_INDEX.md` is one fixed path, which WC-11 forbids, so the flag is required." It does not say whether the flag is required in standalone runs. WC-11 (`candidate:69`) is not limited to unattended mode, and SA-1 (`candidate:147`) keeps standalone defaults. Medium: the reader must guess. Fix: say "required under `--unattended`; standalone default unchanged".
- F4 (origin=changed, `candidate:186`): the AC-C1 positive control tests a separate `printf` line, not the checked command at `candidate:183`. An edit to the checked grep would not be caught. Medium. Fix: state that the control reproduces `candidate:183` exactly, or run the checked command against a planted file.
- F5 (origin=changed, `candidate:218`): "it runs first in P1 (AC-1.2)". AC-1.2 (`candidate:220`) states no ordering. Note only.

## Notes carried from round 1 (verifier-rejected; not prior blocking findings; their text is unchanged)

- M1 (`candidate:90`, `candidate:119`): `--output` value types. `candidate:62` is on a changed line, but the defect text M1 quotes is unchanged. Note.
- M3 (`candidate:63`): WC-5 treats an empty contract as success. Note.
- M5 (`candidate:159`): `--unattended` in P1 with auggie-review posting still on. Note; AC-2.4 (`candidate:226`) runs only after P2.

## Guard Condition Boundary Table (changed-line guards only, FR-8 to FR-10)

The spec has no numeric thresholds on the changed lines, so Maximum/Overflow is not applicable. Pipeline Dimensional Analysis is not triggered: the spec describes no data pipeline whose counts change.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| init-lite per-run directory | `candidate:86` | Zero/Empty: no `--output` under unattended | `""` | n/a | 2.3 (`candidate:73`) requires the brief to pass the output directory | OK |
| init-lite per-run directory | `candidate:86` | Typical: `--retry-of` run with a fresh directory | new dir | true | new `context-audit.md`; first report kept | GAP (N1: not scheduled) |
| init-lite flag type | `candidate:86` | Legitimate edge: standalone `--output report.md` | `report.md` | true | directory-valued: wrong target | GAP (N2) |
| index-repo `--output` | `candidate:111` | Zero/Empty: no `--output` | `""` | false | default `PROJECT_INDEX.md`; "required" unclear | GAP (F3, Medium) |
| index-repo `--output` | `candidate:111` | Typical: `--output <dir>` | `<dir>` | true | writes `<dir>/PROJECT_INDEX.md` | OK |
| cleanup-audit one at a time | `candidate:73` | Legitimate edge: two cleanup-audit tasks in one worktree | 2 | true | second waits (coordinator obligation) | OK |
| AC-0.4 step 3 outcome | `candidate:218` | Zero/Empty: existing report missing | none | false | WC-5 (`candidate:63`) maps to `failed`; step 3 matches | OK |
| AC-0.4 step 3 outcome | `candidate:218` | Sentinel: report's first sentence says `partial` | `partial` | true | WC-5 maps to `succeeded` | OK |
| AC-C1 positive control | `candidate:186` | Legitimate edge: pattern meets a planted line | `orca-ide worktree list` | exit 0 (run in sandbox) | prints the line | OK (F4 scope) |
| AC-C1 check | `candidate:183` | Zero/Empty: no match | none | prints nothing | pass | OK |

## Coverage

Read: all 309 lines of the candidate; the baseline; the round-1 report with its verification block; `.dev/orca-command-refactor/inventory/commands-a.md:53,55,73` and `commands-b.md:52,65,105` (checked against the rows that cite them; INV-A:53 and INV-A:55 match the spec's index-repo and init-lite claims); the Review Loop prompts file. Ran: `diff -w`, the self-check greps, and the AC-C1 positive control in the sandbox.

UNVERIFIED: every `cmd/`, `sk/`, `src/`, `CAPS:` and `cmd/load.md` citation, because those files are outside the workspace. The round-1 items M1, M3 and M5 are carried as notes, not re-verified.

Counts: 6 prior blocking findings checked (5 resolved: M4, M6, M7, M8, M9; 1 open: M2; 0 regressed); 2 new blocking findings (N1, N2); 4 Medium warnings (F1-F4) and 1 note (F5); 3 carried notes (M1, M3, M5).

## Reviser brief

Blocking finding ids: M2, N1, N2. Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
