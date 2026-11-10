review: 2 of 3

# Spec-panel re-review: Orca worker contract spec (round 2)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Prompt: RE-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (`home/.claude/rules/prompts/document_review_loop_prompts.md:38-51`). No `--unattended`, so `WORKER-CONTRACT.md` does not apply.
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 58893 bytes, sha256 `b4832d456dbf9b742b18a39e1442803bd1c9b0e19aafedbf70079e7911d839c2`.
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, 57763 bytes, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`. This is the hash `review/round1.md:7` records as its candidate, so the baseline is the text round 1 reviewed.
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `720158b420afc4ffaf0af27fecaee799336e31a114761f6247d955ac926f1c47`, header `review: 1 of 3` (`review/round1.md:1`). N = 2.
- Reviewer model: claude-haiku-5-5.
- rf-qa.md: neither `.claude/agents/rf-qa.md` in the project nor `~/.claude/agents/rf-qa.md` exists in this sandbox (checked). Steps 1-5 of the fix-cycle process cannot be read, so the rules in `command.md` Review Loop step 5 stand alone, as that bullet allows.

## Step 1: evidence block

`diff -w BASELINE CANDIDATE`. Roles fixed: `<` = BASELINE, `>` = CANDIDATE. There are 16 changed lines, at the same line numbers in both files: 52, 61, 62, 73, 76, 83, 85, 86, 92, 116, 147, 158, 159, 172, 195, 234.

```text
52c52
< - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
---
> - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command, except `load` (F-05), adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
61,62c61,62
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. An answer never supplies an outward flag (WC-9, D4) and never supplies a Ruling unless the user chooses D2(b) (F-02). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. Every command in section 3 writes to this one path; a command whose output would land elsewhere gets an output-directory flag so the path is known before dispatch (F-03). The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
73c73
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
---
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). The coordinator does not run two workers that write a fixed output path (cleanup-audit and index-repo until P1 adds their per-slug flag) in one worktree (F-01, WC-11). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
---
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command, except `load` (F-05), also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
83c83
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
---
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Move the contract to `<output>/return-contract.yaml`, not under `adversarial/`, so it sits at `<output-dir>/return-contract.yaml` (WC-4, F-03) (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
85,86c85,86
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
---
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; add a per-slug output flag (P1), until which one audit per worktree (2.3, F-01) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location and add a per-slug output flag (P1); until then one run per worktree (2.3, F-01) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
---
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome"); add `--output-dir <dir>` so the contract goes to `<dir>/return-contract.yaml`, known before dispatch (F-03) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
116c116
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
---
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract at `<output-dir>/return-contract.yaml`, naming the generated `claudedocs/research_*.md` path | fresh file | add `--output-dir <dir>` (F-03; WC-4) | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
147c147
< | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
---
> | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed `orca` command text is an example of a caller's question channel inside `src/superclaude/core/WORKER-CONTRACT.md`, which AC-C1 exempts (F-04). | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
158,159c158,159
< | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
---
> | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, written in prose with no `orca` command text (AC-C1 applies to it; F-04), and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` (F-05) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
172c172
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
---
> | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/' \| grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:'` | prints nothing (SA-2, WC-8; the contract file is exempt, F-04) |
195c195
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
---
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (F-05) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
234c234
< - (a) **Keep the rule (recommended).** The worker stops, writes the halt to its ledger and contract, and ends `failed`. The person reads the halt and gives the Ruling by running `/sc:implement <plan>` in their own session, which resumes from the ledger.
---
> - (a) **Keep the rule (recommended).** The worker stops, writes the halt to its ledger and contract, and ends `failed`. The person reads the halt and gives the Ruling by running `/sc:implement <plan>` in their own session, which resumes from the ledger. Under (a) no WC-3 answer carries a Ruling (F-02).
```

Self-check (`grep -nF`, run for all 16 pairs): every AFTER line, without its `>`, is found in CANDIDATE, and every BEFORE line, without its `<`, is found in BASELINE. The roles are correct.

## Coverage

- Read in full: the candidate, the baseline, the prior report, the prompt file, `command.md`, and `.dev/orca-command-refactor/README.md:1-39`.
- Scope: the 16 changed lines above and the five prior blocking findings F-01 to F-05 (`command.md` Review Loop step 5). Medium findings F-06 to F-18 are not re-graded; where a changed line still carries one, it is listed under follow-up candidates.
- Inventories: not reopened in this pass. The changed lines add no new INV or CAPS citation. The new text cites only spec sections, finding ids and `src/superclaude/core/WORKER-CONTRACT.md`, so the round-1 citation checks (`review/round1.md:16`) still cover them.
- Pipeline Dimensional Analysis: not triggered. No changed line adds or changes a multi-stage data flow with count divergence.
- State Variable Registry: not required (focus is not correctness).
- Read-only shell tests in `.dev/orca-command-refactor/` (for F-20): the AC-C1 pattern as written in the raw file matched no text (exit 1). The same pattern with unescaped `|` matched (exit 0). The raw pipeline printed 570 lines of spec-folder text, because the `\| grep -v` operands are read as grep options. The unescaped pipeline printed 2 lines, all from the spec's own text.

## Prior blocking findings (round 1)

| ID | Round-1 finding (`review/round1.md`) | Status | Evidence in CANDIDATE |
|---|---|---|---|
| F-01 | WC-11 contradicted by the ready-today index-repo and cleanup-audit rows (`review/round1.md:54-58`) | resolved | 2.3 rule: `SPEC:73`; rows `SPEC:85`, `SPEC:86` |
| F-02 | WC-3 answer may carry an outward flag or a Ruling (`review/round1.md:60-64`) | resolved | `SPEC:61` (an answer never supplies an outward flag, and no Ruling unless D2(b)); `SPEC:234` (D2(a): no WC-3 answer carries a Ruling) |
| F-03 | Contract path not known before dispatch for workflow, research, adversarial (`review/round1.md:66-71`) | resolved | `SPEC:62` (flag rule); `SPEC:83` (adversarial to `<output>/return-contract.yaml`); `SPEC:92` (workflow `--output-dir`); `SPEC:116` (research `--output-dir`) |
| F-04 | AC-C1 forbids the example SA-2 allows (`review/round1.md:73-77`) | resolved (the named defect) | `SPEC:147` (SA-2 names the one allowed example); `SPEC:158` (P0 requires prose with no orca command text); `SPEC:172` (exemption). A separate defect on the same AC-C1 line is F-20. |
| F-05 | AC-1.1 requires a contract for `load`, which the load row and Decisions forbid (`review/round1.md:79-83`) | resolved (the named defect) | `SPEC:52`, `SPEC:76`, `SPEC:159`, `SPEC:195` exclude load. The same conflict returns in the WC-4 sentence at `SPEC:62`; see F-19. |

Regressed: none. Round 1 marked all five open, so none can be regressed in the sense of the rule.

## Findings on changed lines

### F-19. BLOCKING. origin=changed. WC-4 says every section-3 command writes the contract, but `load` does not

- Location: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62`, the sentence "Every command in section 3 writes to this one path; ...".
- Conflicting texts: `:62` says every command in section 3 writes `<output-dir>/return-contract.yaml`. `:112` (the `load` row, Report column) says "none (see note)", and `:265` (Decisions) says a report file for `/sc:load` "would be an unrequested addition". `load` is in section 3.2 (`:112`), so `:62` covers it. The exclusions at `:52`, `:159` and `:195` are not in the WC-4 sentence.
- Grading sentence: "An implementer who follows `SPEC:62` as written gives `load` a `<output-dir>/return-contract.yaml`. `load` has no output-directory flag and no unattended mode (`SPEC:112`, `SPEC:159`), and `SPEC:265` forbids the report, so the two texts contradict each other."
- Reading note: the sentence is a separate clause and does not limit itself to commands that accept `--unattended`. The contradiction follows from the plain reading and needs no assumption about scope.
- Recommendation: limit the sentence to commands that accept `--unattended` (every section-3 row except `load`), and state the exception once.
- Priority: High. Quality impact: medium (an unrequested file in a command the Decisions table excludes).

### F-20. MEDIUM. origin=changed (the line changed; the escaping predates the revision). AC-C1 cannot pass as written in the raw markdown

- Location: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:172`.
- Evidence: the raw file writes `\|` for both the alternation and the pipes. Tested read-only (see Coverage). As written, the pattern matches nothing, and the `\| grep -v` operands are passed to the first grep, where `-v` is read as an option. The command then prints every line it searches, so the check fails on any tree. The rendered table shows plain `|`, and the check works once the reader un-escapes those pipes.
- Grading sentence: "An implementer who copies AC-C1 from the raw file runs a check that prints every searched line, so it cannot pass. The rendered form is correct, so the text allows two readings and the raw one fails the check."
- Grade: Medium, not blocking. The defect needs a reader to choose the table-escape reading, which is the guess the Medium rule covers. Because AC-C1 is the only automated gate for SA-2 (`:147`, a hard requirement under section 5 at `:142`), it should be fixed before P0. The grade is a judgment and the session may weigh it differently.
- Recommendation: put AC-C1 in a fenced code block with `|` unescaped, and add a fixture that a command containing an Orca call fails it.

### F-21. MEDIUM. origin=changed. The 2.3 two-worker rule does not say whether it covers sequential runs

- Location: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:73`, "does not run two workers that write a fixed output path ... in one worktree".
- The text says "run two workers" without saying concurrent or sequential. WC-11 (`:69`) is titled "Parallel-safe writes", but the index-repo row (`:86`) says "until then one run per worktree", which reads as a sequential rule too. A second sequential run would overwrite `PROJECT_INDEX.md` or `progress.json` (`:85`, `:86`). The text allows both readings, so this is Medium.
- Recommendation: say whether the rule covers concurrent runs only, and whether a sequential `index-repo` `mode=update` rerun is allowed.

### F-22. MEDIUM. origin=changed. The new WC-3 answer limit and the 2.3 two-worker rule have no acceptance check

- Location: `:61` and `:73`. Section 7.3 (`:189-211`) has no check for either.
- AC-2.x tests gate behaviour, and AC-3.4 (`:207`) tests two `/sc:save` workers, which is a different case from the 2.3 rule for index-repo and cleanup-audit. No check covers a WC-3 answer that is an outward flag.
- Grading: a stated requirement that no check tests. Medium (missing requirement).
- Recommendation: add a P2 check that an `ask` answer carrying an outward flag is not applied, and a P1 check that two index-repo tasks in one worktree are not dispatched together.

### N-1. minor. origin=changed. Unclear wording at `:85`

- "until which one audit per worktree" is hard to read. "Until then, one audit per worktree" would be clearer.

## Guard Condition Boundary Table (changed guards only; re-review scope)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-3 outward-flag refusal | `SPEC:61` | Sentinel Value Match | answer equals an outward flag (for example `--post-pr`) | true (refused) | answer not applied; WC-9 keeps the flag off | OK |
| WC-3 Ruling refusal | `SPEC:61`, `SPEC:234` | Typical | answer is a Ruling, D2 = (a) | true (refused) | worker stops and ends `failed` | OK |
| WC-3 Ruling refusal | `SPEC:61`, `SPEC:235` | Legitimate Edge Case | answer is a Ruling, D2 = (b) | false (allowed by the user's choice) | recorded verbatim as the Ruling | OK |
| WC-4 every-command clause | `SPEC:62`, `SPEC:112` | Legitimate Edge Case | `load` (in section 3, no output flag, no unattended mode) | true on the plain reading | contradicts `SPEC:112` and `SPEC:265` | GAP (F-19) |
| WC-4 output-directory rule | `SPEC:62`, `SPEC:83`, `SPEC:92`, `SPEC:116` | Typical | adversarial, workflow, research | flag required so the path is known before dispatch | `<output-dir>/return-contract.yaml` | OK |
| WC-4 output-directory rule | `SPEC:62`, `SPEC:85`, `SPEC:86` | Zero/Empty | cleanup-audit and index-repo before P1 (no per-slug flag) | fixed path | one run per worktree (2.3) | OK |
| 2.3 two-worker rule | `SPEC:73` | Sentinel Value Match | two workers, same fixed path, same worktree, concurrent | true (refused) | coordinator does not run both | OK |
| 2.3 two-worker rule | `SPEC:73` | One/Minimal | same fixed path, sequential runs | undefined | not stated | GAP (F-21, Medium) |
| AC-C1 exemption | `SPEC:172` | Legitimate Edge Case | match inside `src/superclaude/core/WORKER-CONTRACT.md` | true (exempt) | the example stays in the core contract (P0) | OK |
| AC-C1 pattern | `SPEC:172` | Typical | raw file text with `\|` | pattern and pipeline misread | check prints every searched line | GAP (F-20, Medium) |
| AC-1.1 load exclusion | `SPEC:195`, `SPEC:159` | Zero/Empty | `load` | excluded | no `## Unattended mode` section | OK |

Classes left out: Maximum/Overflow for every changed guard (no numeric bound is changed).

## Follow-up candidates (Medium and minor; not blocking; not in the revision brief)

- New Medium: F-20, F-21, F-22. New minor: N-1.
- Round-1 Medium findings still open where they quote a changed line: F-06 (`SPEC:73`), F-09 (`SPEC:92`: the workflow row still omits the WC-4 fields `command` and `artifacts`), F-13 and F-14 (`SPEC:62`). The other Medium findings (F-07, F-08, F-10 to F-12, F-15 to F-18) quote unchanged text and are not re-graded here.
- The session that ran this review asks the user once per loop whether to open an issue for these. No issue is created here.

## Re-review verdict summary

- Prior blocking findings: F-01, F-02, F-03, F-04 and F-05 are resolved as named. None is regressed.
- New blocking finding: F-19. The verdict is FAIL.
- Cap: this is review 2 of 3. After one fix cycle, the next re-review is `review: 3 of 3`. A FAIL there escalates to the user.
- Coverage line: not issued, because the verdict is FAIL. The scoped PASS line (`scoped PASS: changed lines + prior blockers`) applies only to a re-review with no open blocking finding.

## Reviser brief

Repair only the blocking finding F-19 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`: the WC-4 sentence at `:62` that begins "Every command in section 3 writes to this one path". Prefer deleting or narrowing text when the requirements are still met. Narrow it to the commands that accept `--unattended`, which excludes `load` (F-05, `:112`, `:159`, `:195`, `:265`). Add no rule, mechanism or section that F-19 does not call for, and cite F-19 on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone (F-20, F-21, F-22, N-1). Return the candidate once and do not award yourself a PASS.

Restated bullet 6 (`command.md` Review Loop step 6): this brief lists only the blocking id F-19 and revises only the text it names. Precedence (step 7): the brief narrows scope and overrides no clause; it does not widen the scope, and no minor or Medium finding is graded as blocking.

verdict: FAIL
