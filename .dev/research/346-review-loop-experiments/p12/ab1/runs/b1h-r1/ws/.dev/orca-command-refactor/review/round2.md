review: 2 of 3
> verification (coordinator, VERIFY step VF2; verifier reply .dev/orca-command-refactor/review/verify-2.md): confirmed blocking ids: N1, N2. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: N3 (verifier: Step 6 applies its pass rule only to a "report-only command". The candidate never classifies `/sc:workflow` or `/sc:troubleshoot` as report-only. spec:193 names only edit-in-place (cleanup, improve) as the other class, and neither command is placed in it. The failure needs that unstated classification. Also, spec:158 lists `/sc:adversarial --output <dir>` as a smoke run, so the finding's "P0 smoke runs use no output flag" is true only for the troubleshoot and workflow runs. The `INV-B:242` default-output claim for troubleshoot is UNVERIFIED here.). The Reviser brief below is narrowed to the confirmed ids.

# Re-review 2 of 3: orca-worker-contract-spec.md against spec-v1 (`/sc:spec-panel --mode critique --focus requirements,architecture`)

## Header and inputs

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 `260c7c0ee1cfff6f147fa7f24960981dd4f6f1f953afdeef2b24a0b090d875da`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- prior: `.dev/orca-command-refactor/review/round1.md` sha256 `33c2abcd1cd7f6f4d5f85ed9587eaed34e7771d62f7013b75081960aa4b7aeb7` (header `review: 1 of 3`, `verdict: FAIL`, blocking ids M1 to M10)
- review prompt: `~/.claude/rules/prompts/document_review_loop_prompts.md` sha256 `ed219181156e47e6d70120730063e0b00081482d8a78b3d2633da188574ca829` (read in full, RE-REVIEW prompt followed)
- reviewer model: claude-haiku-5-5
- review number: prior N = 1, so this is `review: 2 of 3`. The cap (3 reviews) is not reached, so no escalation.
- Baseline hash note: the baseline's sha256 equals the candidate hash that `round1.md` recorded. The round-1 review therefore read the text now stored as the baseline, which is consistent.
- Line references: `spec:N` = line N of the candidate; `base:N` = line N of the baseline. `INV-A:N` and `INV-B:N` = `inventory/commands-a.md` and `inventory/commands-b.md`. `CAPS:N` = `inventory/orca-capabilities.md`.
- Unattended mode was not requested, so `~/.claude/WORKER-CONTRACT.md` was not needed and was not read.
- rf-qa.md: no `.claude/agents/rf-qa.md` (project) and no `~/.claude/agents/rf-qa.md` exist in this sandbox. The fix-cycle steps 1-5 therefore cannot be applied. The rules in this report stand alone, as the Review Loop's re-review bullet allows.
- Evidence limit: the `cmd/`, `sk/` and `src/` files that the spec cites are not in this sandbox. Any citation I could check only through the inventories is marked as checked. Every other citation to those files is UNVERIFIED.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

BEFORE (baseline), lines starting `<`:

```text
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
< 6. `git status --short`. **Pass:** only files under the brief's output directory (and the command's documented artifacts) appear.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```

AFTER (candidate), lines starting `>`:

```text
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. The exception is the `/sc:implement` Ruling: a relayed answer is never accepted as a Ruling until D2 is decided [M6]. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). For a command whose output flag names a file (`--output <file>`, as in tdd and init-lite), `<output-dir>` is that file's parent directory [M1]. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` (from Phase 1 on; the P0 smoke runs omit it, section 6) [M9] and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. From Phase 1 every command in this table also gains the `--unattended` flag and the `## Unattended mode` section (section 2.1), so AC-1.1 covers them [M3, M9]. Otherwise the command changes are only the small fixes in the last column, each in the phase it names.
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | In unattended mode, write the contract to `<output-dir>/return-contract.yaml`, not the `adversarial/` subfolder, so it follows WC-4 (P1) [M5] | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; add `--output-dir` for the WC-4 contract in unattended mode (the fixed `.claude-audit/` stays the default), so one audit per worktree at a time (WC-11) (P1) [M1, M10] | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | Add `--output-dir` for the WC-4 contract in unattended mode, and state the `PROJECT_INDEX.md` location (P1) [M1, M10] | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Add `--output-dir`: in unattended mode the contract goes to `<output-dir>/return-contract.yaml`, so the coordinator knows the path before dispatch, and the package stays at `.dev/tasks/to-do/<id>/` [M5, M10]; write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly and without `--unattended` (the flag arrives in P1), to close evidence gap 1.4 (1). The Orca section of `HOW-WE-WORK.md` names the contract file and no Orca subcommand, so AC-C1 passes [M4, M9]. | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
> | AC-C1 | the scan in the code block below | prints nothing (SA-2, WC-8) [M4] |
> AC-C1 scan (written unescaped, because a `\|` inside a table cell is not an `-E` alternation; the contract file is exempt by path [M4]):
> ```bash
> grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \
>   | grep -v '^src/superclaude/skills/ccsession-tag/' \
>   | grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:'
> ```
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path (from P1; in P0, AC-0.4 applies) [M7].
> 4. (From P1; P0 uses AC-0.4 [M2].) `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
> 6. `git status --short`. **Pass:** for a report-only command, only files under the brief's output directory appear. For an edit-in-place command (cleanup and improve, P2), only files under the output directory and the files its contract lists under `artifacts` (WC-4) appear, and the contract must list every applied edit [M8].
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2, 5, 6 and 7 pass; step 3 passes on its exactly-one clause and on its outcome matching the command's own report status under WC-5, without its contract-path clause, since the WC-4 contract arrives in P1 [M7]; step 4 applies to `/sc:workflow` only, whose `return-contract.yaml` exists today (`INV-B:272`) [M2]; for `/sc:troubleshoot` and `/sc:adversarial`, step 4 is `test -s` on the command's own report file (`REPORT.md`; the report written under `--output`), with no YAML assertion [M2]. Record the results in the phase report; a failure here reopens section 1 |
```

Changed lines against the baseline, with origin: changed = spec:61, 62, 73, 79, 83, 85, 86, 92, 158, 172, 178-185 (inserted block), 190-191, 193, 202. Every other candidate line is origin=unchanged.

## Step 1 self-check (`grep -nF` of every quoted line)

- 22 AFTER lines (without `> `) all found in the candidate.
- 14 BEFORE lines (without `< `) all found in the baseline.
- No BEFORE line is found in the candidate, so the roles were not swapped.

## Prior blocking findings (M1 to M10)

| id | status | where the candidate answers it | note |
|---|---|---|---|
| M1 | resolved | WC-4 parent-directory rule (`spec:62`); cleanup-audit and index-repo rows add an output flag (`spec:85`, `spec:86`) | the flag name now conflicts with AC-1.2, see N1 |
| M2 | resolved | AC-0.4 step 4 split per command (`spec:202`) | step 4 for adversarial names no file, see F1 |
| M3 | resolved | `spec:79` says ready commands gain the flag and section in P1 | none |
| M4 | resolved | AC-C1 unescaped and exempts the contract by path (`spec:172`, `spec:178-183`); routing-guide section names no subcommand (`spec:158`) | none |
| M5 | resolved | adversarial contract at `<output-dir>/return-contract.yaml` (`spec:83`); workflow `--output-dir` (`spec:92`) | none |
| M6 | resolved | WC-3 exception: a relayed answer is never a Ruling until D2 is decided (`spec:61`) | the default is D2(a), as M6 asked |
| M7 | resolved | P0 step 3 drops the contract-path clause (`spec:190`, `spec:202`) | none |
| M8 | resolved for edit-in-place commands | step 6 split; cleanup and improve list applied edits in `artifacts` (`spec:193`) | the split removed the documented-artifacts exception for report-only commands. That defect is N3 and is new, not a regression of M8 |
| M9 | resolved | `spec:73`, `spec:79`, `spec:158` | none |
| M10 | resolved for the paths | workflow, cleanup-audit and index-repo get a contract path (`spec:85`, `spec:86`, `spec:92`); adversarial fixed (`spec:83`) | the flag mismatch is N1 |

No prior blocking finding is `regressed`.

## Findings on changed lines

### N1 (blocking, origin=changed; depends on unchanged spec:204)

- Location: `spec:85`, `spec:86` (changed); `spec:204` (AC-1.2, unchanged, quoted because it depends on the changed rows); `spec:159` (P1 lists cleanup-audit and index-repo).
- Quotes: `spec:86`: "Add `--output-dir` for the WC-4 contract in unattended mode". `spec:204`: "7.2 live check on each P1 command with `--unattended --output <dir>`".
- Grading sentence: an implementer who follows `spec:86` gives index-repo an `--output-dir` flag and no `--output` flag. The AC-1.2 run at `spec:204` passes `--output <dir>` to it, the command rejects the flag, and the criterion cannot pass. `spec:62` lists both spellings, but it does not say which one index-repo or cleanup-audit accepts, so the pass depends on a choice the spec does not make. The same holds for cleanup-audit (`spec:85`).
- Expert: Adzic (acceptance criterion that its own rule cannot satisfy); Wiegers (traceability from the row to the check).
- Recommendation: name one flag per command in `spec:85` and `spec:86`, and use that name in AC-1.2 (or state that both spellings are accepted for these commands). This is a one-line edit per row.
- Priority: High (blocks P1 for two commands).

### N2 (blocking, origin=changed; depends on unchanged WC-11 at spec:69)

- Location: `spec:62` (WC-4, new sentence on file-valued outputs); `spec:69` (WC-11, unchanged: "Two workers in one worktree must never write the same file."); `spec:87` (init-lite `--output <file>`); `spec:90` (tdd `--output <file>`).
- Quote: `spec:62`: "For a command whose output flag names a file (`--output <file>`, as in tdd and init-lite), `<output-dir>` is that file's parent directory [M1]."
- Grading sentence: an implementer who follows `spec:62` writes the contract of every file-valued run to `<parent>/return-contract.yaml`. Two runs whose outputs sit in one directory (for example two init-lite runs with `--output .dev/superclaude/a.md` and `.dev/superclaude/b.md`) write the same contract path. The second run overwrites the first contract. The coordinator then opens a contract that describes the wrong worker, and the first worker's report is lost. WC-11 forbids two workers writing one file, and this rule makes that happen.
- Caveat: that two workers share a worktree is the case WC-11 guards. The `CAPS:115` citation for "workers share the current worktree by default" is UNVERIFIED here: `inventory/orca-capabilities.md:115` says worktrees are not deleted by these verbs and does not state the placement default. The finding does not depend on that premise, because it follows from WC-11's own text.
- Expert: Newman (shared interface artifact); Whittaker (sentinel collision: a fixed filename shared across runs).
- Recommendation: give file-valued outputs a contract name that carries the output file's stem (for example `<stem>.return-contract.yaml`), or require a per-run directory for file-valued outputs. Say which.
- Priority: High (wrong contract read, lost report).

### N3 (blocking, origin=changed; regression introduced by the revision of step 6)

- Location: `spec:193` (step 6, changed); `spec:202` (AC-0.4, changed, "steps 1, 2, 5, 6 and 7 pass"); `spec:158` (P0 smoke runs use no output flag); `spec:92` (workflow `--output-dir` arrives in P1). Baseline `base:185` read "only files under the brief's output directory (and the command's documented artifacts) appear."
- Quote: `spec:193`: "for a report-only command, only files under the brief's output directory appear."
- Grading sentence: an implementer who runs AC-0.4 on `/sc:workflow "<small change>" --handoff none` gets a new package at `.dev/tasks/to-do/<id>/` (`spec:92`; `INV-B:52` and `INV-B:272` name that package as the command's output). Step 6 passes only files under "the brief's output directory", and the P0 brief has no output directory for workflow. The step therefore fails on a correct run, and `spec:202` says a failure reopens section 1. `/sc:troubleshoot "<real symptom>"` in P0 has the same problem: its default output is `.dev/troubleshoot/<slug>-<timestamp>/` (`INV-B:242`), and no output flag is passed in P0.
- Expert: Wiegers (a check that a correct run fails); Adzic (acceptance criterion that its own wording cannot pass).
- Recommendation: restore "and the command's documented artifacts" for report-only commands, or name, for each P0 command, the directory that step 6 checks. Keep the edit-in-place split (cleanup and improve) as it is.
- Priority: High (blocks P0).

### Medium follow-up candidates (not blocking)

- F1 (Medium, origin=changed, `spec:202`): for `/sc:adversarial`, step 4 is "`test -s` on the command's own report file (`REPORT.md`; the report written under `--output`)". `REPORT.md` is troubleshoot's file (`INV-B:242`). The adversarial skill "names no filename" (`INV-A:35`), and its output sits under `<output>/adversarial/` with six artifacts. An implementer must choose the file, so the check needs a guess. Medium, per the grading rule.
- F2 (Medium, UNVERIFIED, origin=changed, `spec:202` with unchanged step 4 at `spec:191`): step 4 asserts `d['command']` on the existing workflow contract. The inventory lists that contract's fields as `status`, `plan_path` and `reflect_report_path` (`INV-B:272`), with no `command` key. WC-4 adds `command` only in P1 ("add the missing ones", `spec:62`), and P0 has no command edits (`spec:158`). `sk/sc-workflow-protocol/refs/return-contract.md` is not in this sandbox, so this is UNVERIFIED. If the key is absent, step 4 fails on a correct P0 run, and the finding becomes blocking.

### Checked and not raised

- AC-C1 (`spec:178-183`): the unescaped pattern and the path exemption behave as written. The routing-guide section avoids lowercase `orca` followed by a subcommand, so it does not trip the scan.
- P0 smoke runs without `--unattended` (`spec:158`) and step 5 (no `AskUserQuestion`): troubleshoot's diagnosis never asks, its `--fix` prompt is absent without the flag (`INV-B:49`), and workflow has no prompts at `--handoff none` (`INV-B:52`, `INV-B:275`). Adversarial's `--interactive` is off by default (`INV-A:35`). No conflict found.
- WC-3 exception (`spec:61`) and the implement row (`spec:109`, unchanged) agree with D2(a).

## Guard Condition Boundary Table (changed guards only; FR-8 to FR-10)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 output-dir derivation | spec:62 | Legitimate edge case: file-valued output shared by two runs | `--output .dev/superclaude/a.md` and `b.md` | parent dir | both contracts at one path | GAP (N2, blocking) |
| WC-4 output-dir derivation | spec:62 | Typical: file-valued output (tdd, init-lite) | `--output <file>` | parent dir | contract in parent dir | OK for one run |
| Step 6 class selection | spec:193 | Typical report-only command writing outside the output dir | workflow `.dev/tasks/to-do/<id>/` | check fails | no documented-artifacts exception | GAP (N3, blocking) |
| AC-0.4 step-4 selection | spec:202 | Command without a YAML contract | troubleshoot `REPORT.md`; adversarial no name | test -s on unnamed file | adversarial file not named | GAP (F1, Medium) |
| AC-1.2 flag | spec:204 with spec:86 | P1 command with the changed flag name | index-repo `--output-dir` vs `--output <dir>` | flag rejected | check cannot pass | GAP (N1, blocking) |
| WC-3 Ruling exception | spec:61 | Relayed coordinator answer on implement | answer text | never a Ruling | matches D2(a) | OK |
| AC-C1 exemption | spec:183 | Grep hit inside `WORKER-CONTRACT.md` | path match | excluded by path | intended | OK |

## Coverage

Scoped: changed lines plus prior blockers, as the coverage line requires. I read the candidate (293 lines) and the baseline, ran `diff -w`, and read the prior report, the prompt file and the three inventories. I checked the inventory citations that changed (`INV-A:35,42,43,52,53`; `INV-B:49,52,242,272,275`), and the cited `CAPS` lines through their quoted text. I did not check the `cmd/`, `sk/` or `src/` citations, because those files are not in this sandbox. Those citations are UNVERIFIED here.

## Follow-up candidates

- F1 (Medium): adversarial's step-4 file is not named in AC-0.4 (`spec:202`).
- F2 (Medium, UNVERIFIED): workflow contract may lack the `command` key that AC-0.4 step 4 asserts (`spec:202`, `spec:191`). Blocking if confirmed.
- Not raised: no minor findings with `origin=changed`.

## Reviser brief

Blocking finding ids: N1, N2, N3. (All prior blocking ids M1 to M10 are resolved, so none is listed.)

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

Note for the coordinator: the VERIFY prompt has not been run on N1 to N3. It must run before any revision, in a fresh-context verifier that sees only the candidate and this finding list. This sandbox has no fresh-context verifier, so no verification block is written here.

verdict: FAIL
